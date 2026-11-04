# -*- coding: utf-8 -*-
"""Rend visibles aux élèves des chapitres de Physique-Chimie de Terminale prêts.

Depuis backend/ :
  manage.py shell -c "import sys; sys.argv=['x','432']; exec(open(r'<chemin>', encoding='utf-8').read())"
  (ajouter '--appliquer' pour écrire ; ids = notions à activer)

Active la matière 5, le contexte 55, le thème de chaque notion et les notions
données ; les chapitres encore vides restent invisibles. État d'avant
sauvegardé dans format_v1/sauvegardes/activer_pc_*.json.
"""
import datetime
import json
import sys
from pathlib import Path

from django.db import transaction

from curriculum.models import Matiere, MatiereContexte, Notion

SORTIE = Path(r"c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend\cours\format_v1\sauvegardes")
ids = [int(a) for a in sys.argv[1:] if a.isdigit()]
matiere = Matiere.objects.get(id=5)
ctx = MatiereContexte.objects.get(id=55)
notions = list(Notion.objects.filter(id__in=ids, theme__contexte=ctx).select_related("theme"))
themes = {n.theme for n in notions}
avant = {
    "matiere": {matiere.id: matiere.est_actif}, "contexte": {ctx.id: ctx.est_actif},
    "themes": {t.id: t.est_actif for t in themes}, "notions": {n.id: n.est_actif for n in notions},
}
print("à activer :", matiere.titre, "| contexte", ctx.id, "| thèmes", sorted(t.id for t in themes),
      "| notions", [(n.id, n.titre) for n in notions])
if "--appliquer" not in sys.argv:
    print("Simulation : rien n'a été écrit.")
else:
    chemin = SORTIE / f"activer_pc_{datetime.datetime.now():%Y%m%d-%H%M%S}.json"
    chemin.write_text(json.dumps(avant, indent=1), encoding="utf-8")
    with transaction.atomic():
        Matiere.objects.filter(id=matiere.id).update(est_actif=True)
        MatiereContexte.objects.filter(id=ctx.id).update(est_actif=True)
        for t in themes:
            type(t).objects.filter(id=t.id).update(est_actif=True)
        Notion.objects.filter(id__in=[n.id for n in notions]).update(est_actif=True)
    print("Activé. Sauvegarde de l'état d'avant :", chemin)
