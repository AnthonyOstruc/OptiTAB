# -*- coding: utf-8 -*-
"""Supprime définitivement des notions (chapitres) avec sauvegarde complète.

Depuis backend/ :
  simulation : manage.py shell -c "import sys; sys.argv=['x','162','101']; exec(open(r'<chemin>', encoding='utf-8').read())"
  exécution  : … sys.argv=['x','162','101','--appliquer'] …

Sauvegarde JSON (sérialiseur Django) de la notion et de TOUT ce que la
suppression emporte en cascade, dans format_v1/sauvegardes/.
Restauration : manage.py loaddata <sauvegarde>.json
"""
import datetime
import sys
from collections import Counter
from pathlib import Path

from django.contrib.admin.utils import NestedObjects
from django.core import serializers
from django.db import router, transaction

from curriculum.models import Notion

SORTIE = Path(r"c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend\cours\format_v1\sauvegardes")

args = sys.argv[1:]
notions = list(Notion.objects.filter(id__in=[int(a) for a in args if a.isdigit()]))
collecteur = NestedObjects(using=router.db_for_write(Notion))
collecteur.collect(notions)
tout = [o for objets in collecteur.data.values() for o in objets]
for n in notions:
    print(f"notion {n.id} : {n.theme.titre} – {n.titre}")
for nom, nb in sorted(Counter(type(o).__name__ for o in tout).items()):
    print(f"  {nom} : {nb}")
if collecteur.protected:
    print("ARRÊT : objets protégés", len(collecteur.protected))
elif "--appliquer" not in args:
    print("Simulation : rien n'a été supprimé.")
else:
    SORTIE.mkdir(exist_ok=True)
    chemin = SORTIE / f"supprimer_notion_{'-'.join(str(n.id) for n in notions)}_{datetime.datetime.now():%Y%m%d-%H%M%S}.json"
    chemin.write_text(serializers.serialize("json", tout, indent=1), encoding="utf-8")
    with transaction.atomic():
        for n in notions:
            n.delete()
    print(f"Supprimé. Sauvegarde : {chemin}")
