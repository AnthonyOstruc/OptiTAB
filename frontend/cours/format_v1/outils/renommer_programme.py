# -*- coding: utf-8 -*-
"""Aligne les titres des thèmes et notions sur les intitulés du programme officiel.

Depuis backend/ :
  manage.py shell -c "import sys; sys.argv=['x']; exec(open(r'<chemin>', encoding='utf-8').read())"
  (ajouter '--appliquer' pour écrire). Anciens titres sauvegardés dans format_v1/sauvegardes/.
"""
import datetime
import json
import sys
from pathlib import Path

from django.db import transaction

from cours.models import Cours
from curriculum.models import Notion, Theme
from synthesis.models import SynthesisSheet

SORTIE = Path(r"c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend\cours\format_v1\sauvegardes")

THEMES = {
    70: "Algorithmique et programmation",   # Première
    45: "Algorithmique et programmation",   # Terminale
    42: "Algèbre et géométrie",
}
NOTIONS = {
    # Première (programme 2019)
    153: "Suites numériques, modèles discrets",
    155: "Dérivation, variations et courbes représentatives",
    157: "Fonctions trigonométriques",
    164: "Notion de liste",
    163: "Algorithmes du programme de Première",
    # Terminale (programme 2020)
    81: "Limites et convergence des suites",
    83: "Continuité des fonctions d’une variable réelle",
    84: "Fonctions sinus et cosinus",
    87: "Dérivation et convexité",
    92: "Orthogonalité et distances dans l’espace",
    97: "Schéma de Bernoulli et loi binomiale",
    98: "Concentration, loi des grands nombres",
    99: "Notion de liste",
    100: "Algorithmes du programme de Terminale",
}

appliquer = "--appliquer" in sys.argv
avant = {"themes": {}, "notions": {}, "cours": {}, "fiches": {}}
for tid, titre in THEMES.items():
    t = Theme.objects.get(id=tid)
    avant["themes"][tid] = t.titre
    print(f"thème {tid} : {t.titre!r} → {titre!r}")
for nid, titre in NOTIONS.items():
    n = Notion.objects.get(id=nid)
    avant["notions"][nid] = n.titre
    print(f"notion {nid} : {n.titre!r} → {titre!r}")
    for c in Cours.objects.filter(notion=n):
        avant["cours"][c.id] = c.titre
        print(f"   cours {c.id} : {c.titre!r}")
    for f in SynthesisSheet.objects.filter(notion=n):
        avant["fiches"][f.id] = f.titre
        print(f"   fiche {f.id} : {f.titre!r}")

if not appliquer:
    print("Simulation : rien n'a été écrit.")
else:
    chemin = SORTIE / f"renommer_programme_{datetime.datetime.now():%Y%m%d-%H%M%S}.json"
    chemin.write_text(json.dumps(avant, ensure_ascii=False, indent=1), encoding="utf-8")
    with transaction.atomic():
        for tid, titre in THEMES.items():
            Theme.objects.filter(id=tid).update(titre=titre)
        for nid, titre in NOTIONS.items():
            Notion.objects.filter(id=nid).update(titre=titre)
    print(f"Renommé. Anciens titres : {chemin}")
