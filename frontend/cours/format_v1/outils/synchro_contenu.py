# -*- coding: utf-8 -*-
"""Recopie l'énoncé v1 (question) dans l'ancien champ « contenu » des exercices.

Depuis backend/ :
  manage.py shell -c "import sys; sys.argv=['x']; exec(open(r'<chemin>', encoding='utf-8').read())"
  (ajouter '--appliquer' pour écrire)

La page des exercices lit « contenu » avant « question » : un exercice v1 dont
« contenu » a gardé l'ancien texte affiche l'ancien énoncé. Les anciens
« contenu » sont sauvegardés dans format_v1/sauvegardes/ avant écriture.
"""
import datetime
import json
import sys
from collections import Counter
from pathlib import Path

from django.db import transaction

from curriculum.models import Exercice

SORTIE = Path(r"c:\Users\SWEELCO-AT\Desktop\SWINDER\OptiTABV2\frontend\cours\format_v1\sauvegardes")

cibles = [e for e in Exercice.objects.select_related("notion__theme__contexte__niveau")
          if (e.question or "").lstrip().startswith("<!-- optitab:1 -->") and (e.contenu or "") != (e.question or "")]
par_notion = Counter((e.notion.theme.contexte.niveau.nom if e.notion_id else "?", e.notion_id) for e in cibles)
for (niv, nid), n in sorted(par_notion.items(), key=lambda kv: (kv[0][0], kv[0][1] or 0)):
    print(f"  {niv:10} notion {nid} : {n}")
print(len(cibles), "exercice(s) à synchroniser")
if "--appliquer" in sys.argv and cibles:
    chemin = SORTIE / f"synchro_contenu_{datetime.datetime.now():%Y%m%d-%H%M%S}.json"
    chemin.write_text(json.dumps([{"id": e.id, "contenu": e.contenu} for e in cibles], ensure_ascii=False, indent=1),
                      encoding="utf-8")
    with transaction.atomic():
        for e in cibles:
            Exercice.objects.filter(id=e.id).update(contenu=e.question)
    reste = sum(1 for e in Exercice.objects.filter(id__in=[c.id for c in cibles]) if e.contenu != e.question)
    print(f"Synchronisé. Restants différents : {reste}. Sauvegarde : {chemin}")
elif cibles:
    print("Simulation : rien n'a été écrit.")
