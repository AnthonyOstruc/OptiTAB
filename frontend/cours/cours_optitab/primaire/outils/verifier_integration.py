"""Relit chaque texte et chaque attachement effectivement enregistré dans le site."""
import hashlib
import json
import re
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,str(Path(__file__).resolve().parent))
import requests
from config import GRADE,LABEL,ROOT,FRONT,LEVEL_ID
from integrer import parse_exos,image_names
from curriculum.models import Notion,Exercice,ExerciceImage
from cours.models import Cours,CoursImage
from synthesis.models import SynthesisSheet,SynthesisImage
from pays.models import Niveau

def main():
    result=json.loads((ROOT/'verifications/integration.json').read_text(encoding='utf-8'))
    ids=[c['notion'] for c in result['chapitres']];count=len(ids);assert len(set(ids))==count
    niveau=Niveau.objects.get(pk=LEVEL_ID)
    assert niveau.est_actif and niveau.demo_notion_id==ids[0] and niveau.demo_exercices.count()==2
    assert Notion.objects.filter(theme__contexte_id=result['contexte'],est_actif=True).count()==count
    assert Cours.objects.filter(notion_id__in=ids,est_actif=True).count()==count
    assert SynthesisSheet.objects.filter(notion_id__in=ids,est_actif=True).count()==count
    assert Exercice.objects.filter(notion_id__in=ids,est_actif=True).count()==count*21
    courses={c.notion_id:c for c in Cours.objects.filter(notion_id__in=ids).prefetch_related('images')}
    sheets={s.notion_id:s for s in SynthesisSheet.objects.filter(notion_id__in=ids).prefetch_related('images')}
    exos={}
    for e in Exercice.objects.filter(notion_id__in=ids).prefetch_related('images'):exos.setdefault(e.notion_id,{})[e.titre]=e
    questions=0;image_count=0
    def check_images(owner,names,directory):
        nonlocal image_count
        actual={im.position:im for im in owner.images.all()}
        assert set(actual)==set(range(1,len(names)+1)),owner.pk
        for pos,name in enumerate(names,1):
            digest=hashlib.sha256((directory/name).read_bytes()).hexdigest()[:20]
            assert digest in actual[pos].image.name and actual[pos].width>0 and actual[pos].height>0,(owner.pk,name)
            image_count+=1
    for chapter in result['chapitres']:
        slug,nid=chapter['slug'],chapter['notion']
        raw=(ROOT/f'cours_{slug}_{GRADE}.txt').read_text(encoding='utf-8');fiche=(FRONT/f'cours/resume/{GRADE}/resume_{slug}_{GRADE}.txt').read_text(encoding='utf-8')
        assert courses[nid].contenu==raw[raw.index('<div'):].strip(),slug
        assert sheets[nid].summary==fiche[fiche.index('<div'):].strip(),slug
        check_images(courses[nid],image_names(raw),ROOT/'images');check_images(sheets[nid],image_names(fiche),ROOT/'images')
        expected=parse_exos(FRONT/f'exercices/{GRADE}/exercice_{slug}_{GRADE}.txt')
        assert set(exos[nid])=={e['titre'] for e in expected}
        for e in expected:
            live=exos[nid][e['titre']]
            assert (live.question,live.etapes,live.reponse_correcte)==(e['question'],e['etapes'],e['solution']),live.pk
            qs=len(re.findall(r'^\*\*Question \d+ :',live.question,re.M));assert qs>=6;questions+=qs
            check_images(live,e['images'],FRONT/f'exercices/{GRADE}/images')
    assert questions==result['questions']
    samples=[next(iter(courses[ids[0]].images.all())),next(iter(exos[ids[-1]].values())).images.get(position=2)]
    def fetch(im):
        response=requests.get(im.image.url,timeout=35);assert response.status_code==200 and response.content[:8]==b'\x89PNG\r\n\x1a\n'
        return dict(id=im.pk,http=200,octets=len(response.content))
    with ThreadPoolExecutor(max_workers=2) as pool:downloads=list(pool.map(fetch,samples))
    response=requests.get(f'https://optitab-backend.onrender.com/api/niveaux/{LEVEL_ID}/',timeout=40)
    assert response.status_code==200 and response.json()['est_actif'] is True
    report=dict(niveau=LABEL,actif=True,chapitres=count,cours=count,fiches=count,exercices=count*21,questions=questions,images_verifiees=image_count,correspondance_sources=True,telechargements=downloads,api_http=200,erreurs=[])
    (ROOT/'verifications/verification-en-ligne.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2));return report
