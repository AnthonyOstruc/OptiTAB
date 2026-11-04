"""Import idempotent d'un niveau primaire ; toutes les entrées sont validées d'abord.

Depuis backend : OPTITAB_NIVEAU=cm2, puis manage.py shell et runpy.run_path.
Les images sont adressées par empreinte ; aucune donnée existante n'est supprimée.
"""
import hashlib
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from config import ROOT,FRONT,GRADE,LABEL,LEVEL_ID,chapters
from parcours import theme
from django.core.files.base import ContentFile
from django.db import transaction
from PIL import Image
from curriculum.models import MatiereContexte,Theme,Notion,Exercice,ExerciceImage
from cours.models import Cours,CoursImage
from synthesis.models import SynthesisSheet,SynthesisImage
from pays.models import Niveau

THEMES=[('nombres','Nombres et calculs'),('mesures','Grandeurs et mesures'),('geometrie','Espace et géométrie'),('donnees','Organisation des données et hasard')]

def champ(raw,name):
    match=re.search(r'^'+re.escape(name)+r':\s*(.+)$',raw,re.M)
    return match[1].strip() if match else ''

def image_names(raw):return [x.strip() for x in champ(raw,'Images').split(',') if x.strip()]

def parse_exos(path):
    blocks=[b.strip() for b in re.split(r'^===\s*$',path.read_text(encoding='utf-8'),flags=re.M) if b.strip()]
    out=[]
    for b in blocks:
        out.append(dict(titre=b.splitlines()[0][4:].strip(),difficulty=champ(b,'Difficulté'),
            question=b.split('Énoncé:',1)[1].split('Étapes:',1)[0].strip(),etapes=b.split('Étapes:',1)[1].split('Solution:',1)[0].strip(),
            solution=b.split('Solution:',1)[1].strip(),images=image_names(b)))
    assert len(out)==21
    return out

def attacher_images(tasks):
    def upload(task):
        model,fk,owner,pos,path,title=task;data=path.read_bytes();digest=hashlib.sha256(data).hexdigest()[:20]
        field=model._meta.get_field('image')
        with Image.open(path) as im:width,height=im.size
        filename=field.generate_filename(model(**{fk:owner}),path.stem+'_'+digest+'.png')
        if not field.storage.exists(filename):filename=field.storage.save(filename,ContentFile(data))
        return task,filename,width,height
    with ThreadPoolExecutor(max_workers=8) as pool:
        for task,filename,width,height in pool.map(upload,tasks):
            model,fk,owner,pos,path,title=task
            model.objects.update_or_create(**{fk:owner,'position':pos},defaults=dict(image=filename,alt_text=title[:255],title_text=title[:255],width=width,height=height))

def activate(niveau,demo):
    niveau.est_actif=True;niveau.demo_notion=demo
    niveau.exercice_filter_options=['Découverte','Entraînement','Problème'];niveau.exercice_filter_default='Tous'
    niveau.save(update_fields=['est_actif','demo_notion','exercice_filter_options','exercice_filter_default','date_modification'])
    niveau.demo_exercices.set(Exercice.objects.filter(notion=demo).order_by('titre')[:2])

def main():
    from valider import valider,ERREURS
    from verifier_calculs import main as calculs
    cs=chapters()
    for ch in cs:valider(ch.slug)
    assert not ERREURS,'Import arrêté avant toute écriture : contenus invalides.'
    calculs()
    mj=json.loads((ROOT/'verifications/mathjax.json').read_text(encoding='utf-8'));assert mj['erreurs']==0
    rendu=json.loads((ROOT/'verifications/rendu.json').read_text(encoding='utf-8'))
    assert len(rendu)==len(cs)*4 and not any(x['erreurs'] or x['imagesManquantes'] or x['debordement'] for x in rendu)
    niveau=Niveau.objects.select_related('pays').get(pk=LEVEL_ID)
    assert niveau.nom==LABEL and niveau.pays.code_iso=='FR'
    ctx,_=MatiereContexte.objects.get_or_create(matiere_id=1,niveau=niveau,defaults=dict(titre=f'Mathématiques (France, {LABEL})',est_actif=True,couleur='#3b82f6'))
    snapshot=ROOT/'verifications/avant-integration.json'
    if not snapshot.exists():
        from django.core.serializers import serialize
        objects=[niveau]+list(Theme.objects.filter(contexte=ctx))+list(Notion.objects.filter(theme__contexte=ctx))+list(Cours.objects.filter(notion__theme__contexte=ctx))
        snapshot.write_text(serialize('json',objects,ensure_ascii=False,indent=2),encoding='utf-8')
    themes={}
    for ordre,(key,title) in enumerate(THEMES,1):
        themes[key],_=Theme.objects.update_or_create(contexte=ctx,titre=title,defaults=dict(matiere_id=1,ordre=ordre,description='',est_actif=True))
    positions={key:0 for key in themes};report=[];demo=None
    for ch in cs:
        key=theme(ch);positions[key]+=1;tasks=[]
        raw=(ROOT/f'cours_{ch.slug}_{GRADE}.txt').read_text(encoding='utf-8')
        fiche=(FRONT/f'cours/resume/{GRADE}/resume_{ch.slug}_{GRADE}.txt').read_text(encoding='utf-8')
        exercices=parse_exos(FRONT/f'exercices/{GRADE}/exercice_{ch.slug}_{GRADE}.txt')
        scope='both' if ch.numero==1 else 'paid'
        with transaction.atomic():
            notion,_=Notion.objects.update_or_create(theme=themes[key],titre=ch.titre,defaults=dict(ordre=positions[key],description='',est_actif=True))
            cours,_=Cours.objects.update_or_create(notion=notion,defaults=dict(titre=champ(raw,'Titre'),contenu=raw[raw.index('<div'):].strip(),difficulty='medium',ordre=ch.numero,access_scope=scope,est_actif=True))
            for pos,name in enumerate(image_names(raw),1):tasks.append((CoursImage,'cours',cours,pos,ROOT/'images'/name,f'Cours de {LABEL} : {ch.titre}'))
            for j,e in enumerate(exercices):
                obj,_=Exercice.objects.update_or_create(notion=notion,titre=e['titre'],defaults=dict(question=e['question'],contenu=e['question'],etapes=e['etapes'],reponse_correcte=e['solution'],difficulty=e['difficulty'],access_scope='both' if ch.numero==1 and j<2 else 'paid',est_actif=True))
                for pos,name in enumerate(e['images'],1):
                    caption=('Correction annotée' if pos==2 else 'Situation complémentaire' if pos==3 else 'Schéma de travail')+' — '+e['titre']
                    tasks.append((ExerciceImage,'exercice',obj,pos,FRONT/f'exercices/{GRADE}/images'/name,caption))
            sheet,_=SynthesisSheet.objects.update_or_create(notion=notion,titre=champ(fiche,'Titre'),sheet_type='summary',defaults=dict(summary=fiche[fiche.index('<div'):].strip(),difficulty='medium',reading_time_minutes=5,key_points=ch.reperes,access_scope=scope,est_actif=True))
            for pos,name in enumerate(image_names(fiche),1):tasks.append((SynthesisImage,'sheet',sheet,pos,ROOT/'images'/name,f'Fiche de {LABEL} : {ch.titre}'))
            attacher_images(tasks)
        if ch.numero==1:
            demo=notion
            with transaction.atomic():activate(niveau,demo)
            print(f'{LABEL} activé : le premier chapitre complet est disponible.',flush=True)
        report.append(dict(slug=ch.slug,notion=notion.pk,cours=cours.pk,fiche=sheet.pk,exercices=21,images=len(tasks)))
        print(json.dumps(report[-1],ensure_ascii=False),flush=True)
        (ROOT/'verifications/integration-en-cours.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    ids=[r['notion'] for r in report]
    Notion.objects.filter(theme__contexte=ctx).exclude(pk__in=ids).update(est_actif=False)
    Cours.objects.filter(notion__theme__contexte=ctx).exclude(notion_id__in=ids).update(est_actif=False)
    for key,t in themes.items():
        if not positions[key]:t.est_actif=False;t.save(update_fields=['est_actif','date_modification'])
    ctx.est_actif=True;ctx.save(update_fields=['est_actif','date_modification'])
    assert Notion.objects.filter(theme__contexte=ctx,est_actif=True).count()==len(cs)
    assert Exercice.objects.filter(notion_id__in=ids,est_actif=True).count()==len(cs)*21
    result=dict(niveau=niveau.pk,contexte=ctx.pk,actif=True,chapitres=report,exercices=len(cs)*21,questions=len(cs)*21*7,images=sum(x['images'] for x in report),demo_notion=demo.pk)
    (ROOT/'verifications/integration.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{LABEL} terminé : {len(cs)} cours et fiches, {len(cs)*21} exercices.',flush=True)
    return result
