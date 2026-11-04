# -*- coding: utf-8 -*-
"""Supprime d'une notion les exercices qui ne sont plus dans son exercices.txt
(passage à 10 exercices par chapitre, consigne du 2026-11-04), avec sauvegarde.

Depuis backend/ :
  simulation : manage.py shell -c "import sys; sys.argv=['x', r'<dossier_notion>']; exec(open(r'<chemin>', encoding='utf-8').read())"
  exécution  : … sys.argv=['x', r'<dossier_notion>', '--appliquer'] …

Les Id gardés sont les lignes « Id: <nombre> » de <dossier>/exercices.txt (les
« nouveau-N » ne sont pas encore en base). Tous les autres exercices de la notion
(meta.json de source_en_ligne) sont supprimés, avec TOUT ce qui part en cascade
(images, suivis d'élèves…) sauvegardé au format du sérialiseur Django dans
format_v1/sauvegardes/. Restauration : manage.py loaddata <sauvegarde>.json
Refus si exercices.txt garde moins de 1 exercice ou plus de 10.
"""
import datetime
import json
import re
import sys
from collections import Counter
from pathlib import Path

from django.contrib.admin.utils import NestedObjects
from django.core import serializers
from django.db import router, transaction

from curriculum.models import Exercice

SORTIE = Path(r"c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend\cours\format_v1\sauvegardes")
MAX = 10

args = sys.argv[1:]
dossier = Path(next(a for a in args if not a.startswith("--"))).resolve()
texte = (dossier / "exercices.txt").read_text(encoding="utf-8")
blocs = re.findall(r"^Id:\s*(\S+)\s*$", texte, flags=re.M)
gardes = {int(b) for b in blocs if b.isdigit()}
meta = json.loads((dossier / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))
notion = meta["notion"]
en_base = list(Exercice.objects.filter(notion_id=notion))
a_retirer = [e for e in en_base if e.id not in gardes]
print(f"notion {notion} : {len(en_base)} exercice(s) en base, {len(blocs)} bloc(s) dans exercices.txt "
      f"({len(gardes)} existants gardés), {len(a_retirer)} à supprimer")
for e in a_retirer:
    print(f"  - {e.id} {e.titre}")
if not 1 <= len(blocs) <= MAX:
    print(f"ARRÊT : exercices.txt doit avoir entre 1 et {MAX} exercices ({len(blocs)}).")
elif not a_retirer:
    print("Rien à supprimer.")
else:
    collecteur = NestedObjects(using=router.db_for_write(Exercice))
    collecteur.collect(a_retirer)
    tout = [o for objets in collecteur.data.values() for o in objets]
    for nom, nb in sorted(Counter(type(o).__name__ for o in tout).items()):
        print(f"  emporté : {nom} × {nb}")
    if collecteur.protected:
        print("ARRÊT : objets protégés", len(collecteur.protected))
    elif "--appliquer" not in args:
        print("Simulation : rien n'a été supprimé.")
    else:
        SORTIE.mkdir(exist_ok=True)
        chemin = SORTIE / f"retirer_exercices_{notion}_{datetime.datetime.now():%Y%m%d-%H%M%S}.json"
        chemin.write_text(serializers.serialize("json", tout, indent=1), encoding="utf-8")
        with transaction.atomic():
            Exercice.objects.filter(id__in=[e.id for e in a_retirer]).delete()
        print(f"Supprimé(s). Sauvegarde : {chemin}")
