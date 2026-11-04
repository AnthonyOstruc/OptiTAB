"""Restauration explicite des sauvegardes 6e, incluant les nouveaux documents.

Ne s'exécute qu'avec --restaurer suivi du chemin d'une sauvegarde précise.
"""
from pathlib import Path
import os,sys,json
if len(sys.argv)!=3 or sys.argv[1]!='--restaurer':raise SystemExit('Usage : python restaurer_publication_6e.py --restaurer <sauvegarde_precise.json>')
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent.resolve();BACKEND=ICI.parents[5]/'backend';OUTILS=ROOT.parents[1]/'outils'
p=Path(sys.argv[2]).resolve();assert p.is_relative_to(ROOT) and p.parent.name=='sauvegardes'
data=json.loads(p.read_text(encoding='utf-8'));assert 129<=data['notion']<=152 or data['notion'] in (284,285)
os.chdir(BACKEND);sys.path.insert(0,str(BACKEND));os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
import django
django.setup()
from django.db import transaction
from cours.models import Cours
from synthesis.models import SynthesisSheet
from curriculum.models import Notion
source=(OUTILS/'importer_v1.py').read_text(encoding='utf-8');ns={'__file__':str(OUTILS/'importer_v1.py'),'__name__':'restauration_6e'}
exec(compile(source.rstrip()[:-len('main()')],str(OUTILS/'importer_v1.py'),'exec'),ns)
with transaction.atomic():
 ns['restaurer'](p)
 for record in data.get('activations_cours',[]):
  Cours.objects.filter(id=record['id'],notion_id=data['notion']).update(est_actif=record['est_actif'])
 for record in data.get('activations_notions',[]):
  assert record['id']==data['notion']
  Notion.objects.filter(id=record['id']).update(est_actif=record['est_actif'])
 for doc in data.get('documents_crees',[]):
  Model=Cours if doc['genre']=='cours' else SynthesisSheet
  Model.objects.filter(id=doc['id'],notion_id=data['notion']).delete()
print('Notion restauree :',data['notion'])
