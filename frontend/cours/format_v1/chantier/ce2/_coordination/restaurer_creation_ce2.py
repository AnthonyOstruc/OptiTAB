"""Retour arrière explicite et borné à la hiérarchie CE2 créée par ce chantier."""
from pathlib import Path
import os,sys,json
ICI=Path(__file__).resolve().parent;REPO=ICI.parents[5]
if len(sys.argv)!=3 or sys.argv[1]!='--restaurer':raise SystemExit('Indiquer --restaurer et une sauvegarde précise.')
p=Path(sys.argv[2]).resolve();assert p.parent==(ICI/'sauvegardes').resolve()
data=json.loads(p.read_text(encoding='utf-8'));assert data['statut']=='creation_validee' and data['niveau']==11 and data['contexte_existant_avant'] is False
os.chdir(REPO/'backend');sys.path.insert(0,str(REPO/'backend'));os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
import django
django.setup()
from django.db import transaction
from pays.models import Niveau
from curriculum.models import MatiereContexte,Notion,Theme
with transaction.atomic():
 ctx=MatiereContexte.objects.get(id=data['contexte_cree'],niveau_id=11,matiere_id=1)
 assert set(Notion.objects.filter(theme__contexte=ctx).values_list('id',flat=True))==set(data['notions_creees'])
 assert set(Theme.objects.filter(contexte=ctx).values_list('id',flat=True))==set(data['themes_crees'])
 ctx.delete()
 Niveau.objects.filter(id=11).update(est_actif=data['niveau_actif_avant'])
print('Création CE2 restaurée ; sauvegardes et fichiers conservés.')
