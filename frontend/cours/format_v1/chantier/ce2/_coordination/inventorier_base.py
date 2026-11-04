from pathlib import Path
import os,sys,json
ICI=Path(__file__).resolve().parent;REPO=ICI.parents[5]
os.chdir(REPO/'backend');sys.path.insert(0,str(REPO/'backend'));os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
import django
django.setup()
from pays.models import Niveau
from curriculum.models import MatiereContexte,Notion
levels=list(Niveau.objects.filter(pays__nom='France',nom__iexact='CE2').values('id','nom','est_actif'))
contexts=list(MatiereContexte.objects.filter(niveau__nom__iexact='CE2',niveau__pays__nom='France',matiere_id=1).values('id','niveau_id','est_actif'))
data={'niveaux':levels,'contextes':contexts}
if contexts:data['notions']=list(Notion.objects.filter(theme__contexte_id__in=[c['id'] for c in contexts]).values('id','titre','est_actif'))
(ICI/'inventaire_base_ce2.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(data,ensure_ascii=False))
