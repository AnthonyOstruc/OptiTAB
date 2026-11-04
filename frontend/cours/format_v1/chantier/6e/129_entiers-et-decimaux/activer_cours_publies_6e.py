"""Activation des seuls cours 6e importés, avec sauvegarde du drapeau précédent."""
from pathlib import Path
import os,sys,json,datetime
ICI=Path(__file__).resolve().parent;BACKEND=ICI.parents[5]/'backend'
os.chdir(BACKEND);sys.path.insert(0,str(BACKEND));os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
import django
django.setup()
from django.db import transaction
from cours.models import Cours
from synthesis.models import SynthesisSheet
from curriculum.models import Exercice,Notion
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
pub=load(ICI/'publication_6e.json');assert pub['statut']=='importe_et_relu'
if '--lecture' in sys.argv:
 ids_notions=[r['notion'] for r in pub['imports']]
 hidden=Notion.objects.filter(id__in=ids_notions).exclude(est_actif=True,theme__est_actif=True,theme__matiere__est_actif=True)
 print('notions ou parents inactifs',list(hidden.values('id','est_actif','theme__est_actif','theme__matiere__est_actif')))
 for genre,Model in [('cours',Cours),('fiches',SynthesisSheet),('exercices',Exercice)]:
  if any(f.name=='est_actif' for f in Model._meta.fields):
   ids=[oid for r in pub['imports'] for oid in r[genre].values()]
   print(genre,list(Model.objects.filter(id__in=ids,est_actif=False).values('id','notion_id')))
 raise SystemExit(0)
previous=load(ICI/'activation_cours_6e.json') if (ICI/'activation_cours_6e.json').exists() else {}
records=previous.get('modifications',[]);notions_records=previous.get('notions_activees',[])
with transaction.atomic():
 for r in pub['imports']:
  d=ICI.parent/r['dossier'];backup=Path(r['sauvegarde']);data=load(backup)
  notion=Notion.objects.select_related('theme','theme__matiere').get(id=r['notion'])
  assert notion.theme.est_actif and notion.theme.matiere.est_actif
  if not notion.est_actif:
   data.setdefault('activations_notions',[]).append({'id':notion.id,'est_actif':False})
   save(backup,data)
   Notion.objects.filter(id=notion.id,est_actif=False).update(est_actif=True)
   notions_records.append({'notion':notion.id,'avant':False,'apres':True})
  for key,oid in r['cours'].items():
   obj=Cours.objects.get(id=oid,notion_id=r['notion'])
   text=(d/f'cours_{key}.txt').read_text(encoding='utf-8')
   assert obj.contenu==text[text.index('<!-- optitab:1 -->'):].strip()
   if not obj.est_actif:
    data.setdefault('activations_cours',[]).append({'id':obj.id,'est_actif':False})
    save(backup,data)
    Cours.objects.filter(id=obj.id,est_actif=False).update(est_actif=True)
    records.append({'notion':r['notion'],'cours':obj.id,'avant':False,'apres':True})
  for genre,Model in [('fiches',SynthesisSheet),('exercices',Exercice)]:
   ids=list(r[genre].values())
   if any(f.name=='est_actif' for f in Model._meta.fields):
    assert not Model.objects.filter(id__in=ids,est_actif=False).exists(),(r['notion'],genre,'inactif')
assert Cours.objects.filter(id__in=[oid for r in pub['imports'] for oid in r['cours'].values()],est_actif=True).count()==26
assert Notion.objects.filter(id__in=[r['notion'] for r in pub['imports']],est_actif=True).count()==26
save(ICI/'activation_cours_6e.json',{'date':datetime.datetime.now().isoformat(timespec='seconds'),'statut':'OK','cours_actifs':26,'notions_actives':26,'modifications':records,'notions_activees':notions_records})
print(json.dumps({'cours_actifs':26,'notions_actives':26,'activations':records,'notions_activees':notions_records}))
