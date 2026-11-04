# -*- coding: utf-8 -*-
"""Vide des parcours entiers (cours, fiches, exercices) avec sauvegarde complète.

Depuis backend/ :
  simulation : manage.py shell -c "import sys; sys.argv=['x','46','41','42']; exec(open(r'<chemin>', encoding='utf-8').read())"
  exécution  : … sys.argv=['x','46','41','42','--appliquer'] …

Sauvegarde JSON (sérialiseur Django) de TOUT ce que la suppression emporte en
cascade (images, suivis d'élèves…) dans format_v1/sauvegardes/, puis :
cours, fiches et exercices supprimés ; notions désactivées (est_actif = False)
pour qu'aucun chapitre vide n'apparaisse. Les fichiers S3 ne sont pas effacés.
Restauration : manage.py loaddata <sauvegarde>.json puis réactiver les notions.
"""
import datetime
import sys
from collections import Counter
from pathlib import Path

from django.contrib.admin.utils import NestedObjects
from django.core import serializers
from django.db import router, transaction

from cours.models import Cours
from curriculum.models import Exercice, Notion
from synthesis.models import SynthesisSheet

SORTIE = Path(r"c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend\cours\format_v1\sauvegardes")

args = sys.argv[1:]
contextes = [int(a) for a in args if a.isdigit()]
notions = Notion.objects.filter(theme__contexte_id__in=contextes)
groupes = [list(Cours.objects.filter(notion__in=notions)), list(SynthesisSheet.objects.filter(notion__in=notions)),
           list(Exercice.objects.filter(notion__in=notions))]
racines = [o for g in groupes for o in g]
tout, protegés = [], []
for g in groupes:
    if not g:
        continue
    collecteur = NestedObjects(using=router.db_for_write(type(g[0])))
    collecteur.collect(g)
    for modele, objets in collecteur.data.items():
        tout.extend(objets)
    protegés += list(collecteur.protected)


class _C:
    protected = protegés


collecteur = _C()
compte = Counter(type(o).__name__ for o in tout)
print("Contextes", contextes, "—", notions.count(), "notions")
for nom, n in sorted(compte.items()):
    print(f"  {nom} : {n}")
if collecteur.protected:
    print("ARRÊT : objets protégés", len(collecteur.protected))
elif "--appliquer" not in args:
    print("Simulation : rien n'a été supprimé.")
else:
    SORTIE.mkdir(exist_ok=True)
    chemin = SORTIE / f"vider_parcours_{'-'.join(map(str, contextes))}_{datetime.datetime.now():%Y%m%d-%H%M%S}.json"
    objets_notions = list(notions)
    chemin.write_text(serializers.serialize("json", objets_notions + tout, indent=1), encoding="utf-8")
    with transaction.atomic():
        for r in racines:
            r.delete()
        n = notions.update(est_actif=False)
    print(f"Supprimé ; {n} notions désactivées. Sauvegarde : {chemin}")
