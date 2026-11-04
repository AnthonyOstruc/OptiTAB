"""Reprendre exclusivement la relecture d'un import deja valide en base."""
from pathlib import Path
import os, sys, json, datetime
from urllib.request import urlopen
sys.stdout.reconfigure(encoding='utf-8')
ICI=Path(__file__).resolve().parent
BACKEND=ICI.parents[5]/'backend'
OUTILS=ICI.parents[2]/'outils'
os.chdir(BACKEND);sys.path.insert(0,str(BACKEND))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
import django
django.setup()
from django.core.files.storage import default_storage
from cours.models import Cours
from synthesis.models import SynthesisSheet
from curriculum.models import Exercice

def load(p):return json.loads(p.read_text(encoding='utf-8'))
script=OUTILS/'importer_v1.py';source=script.read_text(encoding='utf-8')
ns={'__file__':str(script),'__name__':'controle_publication_5e'}
exec(compile(source.rstrip()[:-len('main()')],str(script),'exec'),ns)
bilan=load(ICI/'bilan_5e.json');images=[];imports=[]
for r in bilan['detail']:
    d=ICI.parent/r['dossier'];meta=load(d/'source_en_ligne/meta.json');state=load(d/'etat.json')
    assert state['statut']=='importe' and Path(state['sauvegarde']).exists()
    imports.append({'notion':r['notion'],'sauvegarde':state['sauvegarde'],'statut':'importe'})
    finaux=ns['exercices_finaux'](d/'exercices.txt')
    for genre,Model,field,prefix in [('cours',Cours,'contenu','cours_'),('fiches',SynthesisSheet,'summary','fiche_')]:
        for item in meta[genre]:
            obj=Model.objects.get(id=item['id'])
            assert getattr(obj,field)==ns['corps_doc'](d/(prefix+str(obj.id)+'.txt'))
    for eid,e in finaux.items():
        obj=Exercice.objects.get(id=eid)
        assert (obj.titre,obj.difficulty)==(e['titre'],e['difficulty'])
        assert all(getattr(obj,k)==v for k,v in e['champs'].items())
    for genre,ids in [('cours',[x['id'] for x in meta['cours']]),('fiches',[x['id'] for x in meta['fiches']]),('exercices',list(finaux))]:
        for oid in ids:
            for im in ns['images_en_base'](genre,oid):
                assert im.width and im.height and im.alt_text
                if '--diagnostic' in sys.argv:
                    storage=im.image.storage
                    print(json.dumps({'notion':r['notion'],'genre':genre,'id':im.id,'position':im.position,'name':im.image.name,'default_storage':str(type(default_storage._wrapped)),'field_storage':str(type(storage)),'default_exists':default_storage.exists(im.image.name),'field_exists':storage.exists(im.image.name)},ensure_ascii=True),flush=True)
                    try:
                        with urlopen(im.image.url,timeout=30) as response:print('HTTP image:',response.status,'octets:',len(response.read()),flush=True)
                    except Exception as exc:print('HTTP image:',type(exc).__name__,getattr(exc,'code',''),flush=True)
                    raise SystemExit(0)
                images.append({'notion':r['notion'],'genre':genre,'id':im.id,'proprietaire':oid,'position':im.position,'url':im.image.url,'width':im.width,'height':im.height})
    print('Textes et sauvegarde relus :',r['notion'],flush=True)
report=load(ICI/'simulation_import_5e.json')
report.update(date=datetime.datetime.now().isoformat(timespec='seconds'),ecriture=True,statut='importe_et_relu',sauvegardes=imports,images_a_verifier_http=len(images))
(ICI/'publication_5e.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ICI/'images_publiees_5e.json').write_text(json.dumps(images,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'statut':'textes_importes_et_relus','notions':20,'images_a_verifier_http':len(images)}),flush=True)
