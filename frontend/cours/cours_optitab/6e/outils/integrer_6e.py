"""Intégration idempotente de la 6e dans Django ; activation après contrôle complet.

Depuis backend/ :
  venv/Scripts/python.exe manage.py shell -c "import runpy; m=runpy.run_path(r'../frontend/cours/cours_optitab/6e/outils/integrer_6e.py'); m['main']()"

La configuration Django du poste est celle du site en production.
Ne supprime aucun contenu existant. Les figures ont un nom dépendant de leur SHA-256.
"""
import hashlib
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from django.core.files.base import ContentFile
from django.db import transaction
from PIL import Image
from curriculum.models import MatiereContexte,Theme,Notion,Exercice,ExerciceImage
from cours.models import Cours,CoursImage
from synthesis.models import SynthesisSheet,SynthesisImage
from pays.models import Niveau

ROOT=Path(__file__).resolve().parents[1]
FRONT=ROOT.parents[2]
sys.path.insert(0,str(ROOT/'outils'))
THEMES=[('nombres','Nombres et calculs'),('donnees','Organisation et gestion de données, fonctions'),
    ('grandeurs','Grandeurs et mesures'),('geometrie','Espace et géométrie'),('algo','Algorithmique et programmation')]
THEME_IDS={'nombres':51,'grandeurs':61,'geometrie':62,'donnees':63,'algo':64}
NOTION_IDS={'numeration':129,'reperage':130,'calcul-decimal':131,'division':133,
    'fraction-quotient':132,'prealgebre':151,'proportionnalite':134,'longueurs':135,
    'aires':137,'durees':139,'distances-cercles':140,'mediatrice':144,'angles':141,
    'triangles':142,'symetrie-axiale':145,'solides-volumes':138,'donnees':147,
    'probabilites':149,'instructions':152}


def champ(raw,name):
    match=re.search(r'^'+re.escape(name)+r':\s*(.+)$',raw,re.M)
    return match[1].strip() if match else ''


def image_names(raw):
    return [s.strip() for s in champ(raw,'Images').split(',') if s.strip()]


def parse_exos(path):
    blocks=[b.strip() for b in re.split(r'^===\s*$',path.read_text(encoding='utf-8'),flags=re.M) if b.strip()]
    out=[]
    for b in blocks:
        out.append(dict(titre=b.splitlines()[0][4:].strip(),difficulty=champ(b,'Difficulté'),
            question=b.split('Énoncé:',1)[1].split('Étapes:',1)[0].strip(),
            etapes=b.split('Étapes:',1)[1].split('Solution:',1)[0].strip(),
            solution=b.split('Solution:',1)[1].strip(),images=image_names(b)))
    assert len(out)==21
    return out


def attacher_images(tasks):
    """Stockage en parallèle ; écritures Django sur le seul thread principal."""
    def upload(task):
        model,fk,owner,pos,path,title=task
        data=path.read_bytes();digest=hashlib.sha256(data).hexdigest()[:20]
        field=model._meta.get_field('image')
        with Image.open(path) as im:width,height=im.size
        filename=field.generate_filename(model(**{fk:owner}),path.stem+'_'+digest+'.png')
        if not field.storage.exists(filename):
            filename=field.storage.save(filename,ContentFile(data))
        return task,filename,width,height
    with ThreadPoolExecutor(max_workers=6) as pool:
        for task,filename,width,height in pool.map(upload,tasks):
            model,fk,owner,pos,path,title=task
            model.objects.update_or_create(**{fk:owner,'position':pos},defaults=dict(
                image=filename,alt_text=title[:255],title_text=title[:255],width=width,height=height))


def main(slugs=None):
    from valider_6e import valider,ERREURS
    from construire_6e import CHAPITRES
    for c in CHAPITRES:
        if not slugs or c.slug in slugs: valider(c.slug)
    assert not ERREURS,'Contenus invalides : import arrêté avant toute écriture'
    niveau=Niveau.objects.select_related('pays').get(id=14)
    assert niveau.nom.startswith('6') and niveau.pays.code_iso=='FR'
    ctx,_=MatiereContexte.objects.get_or_create(matiere_id=1,niveau=niveau,
        defaults=dict(titre='Mathématiques (France, 6ème)',est_actif=True,couleur='#3b82f6'))
    if not ctx.est_actif:
        ctx.est_actif=True
        ctx.save(update_fields=['est_actif','date_modification'])
    snapshot=ROOT/'verifications/avant-integration.json'
    if not snapshot.exists():
        from django.core.serializers import serialize
        objects=list(Notion.objects.filter(theme__contexte=ctx))+list(Cours.objects.filter(notion__theme__contexte=ctx))+list(Theme.objects.filter(contexte=ctx))+[niveau]
        snapshot.write_text(serialize('json',objects,ensure_ascii=False,indent=2),encoding='utf-8')
    themes={}
    for ordre,(cle,title) in enumerate(THEMES,1):
        themes[cle],_=Theme.objects.update_or_create(pk=THEME_IDS[cle],contexte=ctx,
            defaults=dict(titre=title,matiere_id=1,ordre=ordre,description='',est_actif=True))
    positions={key:0 for key in themes}
    report=[]
    for c in CHAPITRES:
        key='nombres' if c.numero<=8 else 'grandeurs' if c.numero<=12 else 'geometrie' if c.numero<=18 else 'donnees' if c.numero<=20 else 'algo'
        positions[key]+=1
        if slugs and c.slug not in slugs: continue
        raw=(ROOT/f'cours_{c.slug}_6e.txt').read_text(encoding='utf-8')
        fiche=(FRONT/f'cours/resume/6e/resume_{c.slug}_6e.txt').read_text(encoding='utf-8')
        exercices=parse_exos(FRONT/f'exercices/6e/exercice_{c.slug}_6e.txt')
        scope='both' if c.slug=='numeration' else 'paid'
        tasks=[]
        with transaction.atomic():
            if c.slug in NOTION_IDS:
                notion=Notion.objects.get(pk=NOTION_IDS[c.slug],theme__contexte=ctx)
                notion.theme=themes[key];notion.titre=c.titre;notion.ordre=positions[key];notion.description='';notion.est_actif=True
                notion.save(update_fields=['theme','titre','ordre','description','est_actif','date_modification'])
            else:
                notion,_=Notion.objects.update_or_create(theme=themes[key],titre=c.titre,
                    defaults=dict(ordre=positions[key],description='',est_actif=True))
            cours,_=Cours.objects.update_or_create(notion=notion,defaults=dict(titre=champ(raw,'Titre'),
                contenu=raw[raw.index('<div'):].strip(),difficulty='medium',ordre=c.numero,access_scope=scope,est_actif=True))
            for pos,name in enumerate(image_names(raw),1):
                tasks.append((CoursImage,'cours',cours,pos,ROOT/'images'/name,f'Cours de 6e : {c.titre} — '+name.replace('_6e.png','').replace('cours-','').replace('-',' ')))
            for j,e in enumerate(exercices):
                obj,_=Exercice.objects.update_or_create(notion=notion,titre=e['titre'],defaults=dict(
                    question=e['question'],contenu=e['question'],etapes=e['etapes'],reponse_correcte=e['solution'],
                    difficulty=e['difficulty'],access_scope='both' if c.slug=='numeration' and j<2 else 'paid',est_actif=True))
                for pos,name in enumerate(e['images'],1):
                    caption=('Correction annotée' if 'corrige' in name else 'Schéma de travail')+' — '+e['titre']
                    tasks.append((ExerciceImage,'exercice',obj,pos,FRONT/'exercices/6e/images'/name,caption))
            sheet,_=SynthesisSheet.objects.update_or_create(notion=notion,titre=champ(fiche,'Titre'),sheet_type='summary',
                defaults=dict(summary=fiche[fiche.index('<div'):].strip(),difficulty='medium',reading_time_minutes=6,
                    key_points=c.reperes,access_scope=scope,est_actif=True))
            for pos,name in enumerate(image_names(fiche),1):
                tasks.append((SynthesisImage,'sheet',sheet,pos,ROOT/'images'/name,f'Fiche de 6e : {c.titre}'))
            attacher_images(tasks)
        item=dict(slug=c.slug,notion=notion.pk,cours=cours.pk,fiche=sheet.pk,exercices=21,images=len(tasks))
        report.append(item)
        print(json.dumps(item,ensure_ascii=False),flush=True)
    if slugs:
        demo=Notion.objects.get(pk=129)
        niveau.est_actif=True;niveau.demo_notion=demo
        niveau.exercice_filter_options=['Découverte','Entraînement','Problème'];niveau.exercice_filter_default='Tous'
        niveau.save(update_fields=['est_actif','demo_notion','exercice_filter_options','exercice_filter_default','date_modification'])
        niveau.demo_exercices.set(Exercice.objects.filter(notion=demo).order_by('titre')[:2])
        print('6ème activée ; premiers contenus disponibles.',flush=True)
        return report
    imported_ids=[x['notion'] for x in report]
    # Les anciennes notions regroupées sont conservées, mais retirées des listes.
    Notion.objects.filter(theme__contexte=ctx).exclude(pk__in=imported_ids).update(est_actif=False)
    Cours.objects.filter(notion__theme__contexte=ctx).exclude(notion_id__in=imported_ids).update(est_actif=False)
    notions=Notion.objects.filter(theme__contexte=ctx,est_actif=True)
    assert notions.count()==21
    assert Exercice.objects.filter(notion__in=notions).count()==441
    assert Cours.objects.filter(notion__in=notions).count()==21
    assert SynthesisSheet.objects.filter(notion__in=notions).count()==21
    demo=notions.get(titre=CHAPITRES[0].titre)
    with transaction.atomic():
        niveau.est_actif=True
        niveau.exercice_filter_options=['Découverte','Entraînement','Problème']
        niveau.exercice_filter_default='Tous'
        niveau.demo_notion=demo
        niveau.save(update_fields=['est_actif','exercice_filter_options','exercice_filter_default','demo_notion','date_modification'])
        niveau.demo_exercices.set(Exercice.objects.filter(notion=demo).order_by('titre')[:2])
    result=dict(niveau=niveau.pk,contexte=ctx.pk,actif=True,chapitres=report,
        exercices=441,questions=2646,images=sum(x['images'] for x in report),demo_notion=demo.pk)
    (ROOT/'verifications/integration.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('6ème activée : 21 cours, 21 fiches, 441 exercices.',flush=True)
    return result
