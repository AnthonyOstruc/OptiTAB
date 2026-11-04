"""Relit les contenus effectivement enregistrés dans Django après l'import."""
import hashlib
import json
import re
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests
from curriculum.models import Notion,Exercice,ExerciceImage
from cours.models import Cours,CoursImage
from synthesis.models import SynthesisSheet
from pays.models import Niveau

ROOT=Path(__file__).resolve().parents[1]
FRONT=ROOT.parents[2]
sys.path.insert(0,str(ROOT/'outils'))
from integrer_6e import parse_exos


def main():
    result=json.loads((ROOT/'verifications/integration.json').read_text(encoding='utf-8'))
    ids=[c['notion'] for c in result['chapitres']]
    assert len(ids)==len(set(ids))==21
    niveau=Niveau.objects.get(pk=14)
    assert niveau.est_actif and niveau.demo_notion_id==129 and niveau.demo_exercices.count()==2
    assert Notion.objects.filter(theme__contexte_id=43,est_actif=True).count()==21
    assert Cours.objects.filter(notion_id__in=ids,est_actif=True).count()==21
    assert SynthesisSheet.objects.filter(notion_id__in=ids,est_actif=True).count()==21
    assert Exercice.objects.filter(notion_id__in=ids,est_actif=True).count()==441
    course_map={c.notion_id:c for c in Cours.objects.filter(notion_id__in=ids)}
    sheet_map={s.notion_id:s for s in SynthesisSheet.objects.filter(notion_id__in=ids)}
    ex_map={}
    for e in Exercice.objects.filter(notion_id__in=ids).prefetch_related('images'):
        ex_map.setdefault(e.notion_id,{})[e.titre]=e
    questions=0
    for chapter in result['chapitres']:
        slug,nid=chapter['slug'],chapter['notion']
        course=(ROOT/f'cours_{slug}_6e.txt').read_text(encoding='utf-8')
        fiche=(FRONT/f'cours/resume/6e/resume_{slug}_6e.txt').read_text(encoding='utf-8')
        assert course_map[nid].contenu==course[course.index('<div'):].strip(),slug
        assert sheet_map[nid].summary==fiche[fiche.index('<div'):].strip(),slug
        expected=parse_exos(FRONT/f'exercices/6e/exercice_{slug}_6e.txt')
        assert set(ex_map[nid])=={e['titre'] for e in expected},slug
        for e in expected:
            live=ex_map[nid][e['titre']]
            assert (live.question,live.etapes,live.reponse_correcte)==(e['question'],e['etapes'],e['solution']),live.pk
            qs=len(re.findall(r'^\*\*Question \d+ :',live.question,re.M))
            assert qs>=6
            questions+=qs
            ims={im.position:im for im in live.images.all()}
            for pos,name in enumerate(e['images'],1):
                local=FRONT/'exercices/6e/images'/name
                digest=hashlib.sha256(local.read_bytes()).hexdigest()[:20]
                assert pos in ims and digest in ims[pos].image.name and ims[pos].width>0
    assert questions==2646
    # Contrôle de téléchargement sur des figures de cours et de correction.
    samples=[CoursImage.objects.filter(cours__notion_id=129,position=1).get(),
        ExerciceImage.objects.filter(exercice__notion_id=138,position=2).first(),
        ExerciceImage.objects.filter(exercice__notion_id=142,position=2).first()]
    def fetch(im):
        assert im
        response=requests.get(im.image.url,timeout=35)
        assert response.status_code==200 and response.content[:8]==b'\x89PNG\r\n\x1a\n'
        return dict(modele=type(im).__name__,id=im.pk,http=response.status_code,octets=len(response.content))
    with ThreadPoolExecutor(max_workers=3) as pool:images=list(pool.map(fetch,samples))
    report=dict(niveau=14,actif=True,chapitres=21,cours=21,fiches=21,exercices=441,questions=questions,
        images_exercices=ExerciceImage.objects.filter(exercice__notion_id__in=ids).count(),
        correspondance_sources=True,echantillon_images_telechargees=images,erreurs=[])
    (ROOT/'verifications/verification-en-ligne.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report
