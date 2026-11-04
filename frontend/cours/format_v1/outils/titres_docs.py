# -*- coding: utf-8 -*-
"""Aligne en base le titre des cours et fiches sur la ligne « Titre: » des fichiers finaux.

Depuis backend/ :
  manage.py shell -c "import sys; sys.argv=['x', r'<dossier>', …]; exec(open(r'<chemin>', encoding='utf-8').read())"
  (ajouter '--appliquer' pour écrire ; importer_v1.py ne touche pas à ces titres)
"""
import re
import sys
from pathlib import Path

from cours.models import Cours
from synthesis.models import SynthesisSheet

appliquer = "--appliquer" in sys.argv
for d in (Path(a) for a in sys.argv[1:] if not a.startswith("--")):
    for f in sorted(d.glob("cours_*.txt")) + sorted(d.glob("fiche_*.txt")):
        m = re.match(r"Titre:\s*(.+)", f.read_text(encoding="utf-8").split("\n", 1)[0])
        oid = int(re.search(r"_(\d+)\.txt$", f.name).group(1))
        modele = Cours if f.name.startswith("cours_") else SynthesisSheet
        obj = modele.objects.filter(id=oid).first()
        if not (m and obj) or obj.titre == m.group(1).strip():
            continue
        print(f"{d.name[:30]} {f.name} : « {obj.titre} » → « {m.group(1).strip()} »")
        if appliquer:
            modele.objects.filter(id=oid).update(titre=m.group(1).strip())
