# -*- coding: utf-8 -*-
"""Remplace les « Id: nouveau-N » déjà créés en base par leur vrai Id.

    python relier_nouveaux.py <dossier_notion> [<dossier_notion> …]

Lit les sauvegardes d'import (sauvegardes/avant_import_*.json, clé
« exercices_crees ») et met à jour exercices.txt et figures/correspondance.json,
pour qu'un nouvel import modifie ces exercices au lieu de les recréer.
Appelé automatiquement par importer_v1.py après « --appliquer ».
"""
import json
import re
import sys
from pathlib import Path


def relier(dossier):
    dossier = Path(dossier)
    lien = {}
    for s in sorted((dossier / "sauvegardes").glob("avant_import_*.json")):
        for c in json.loads(s.read_text(encoding="utf-8")).get("exercices_crees", []):
            lien[c["cle"]] = c["id"]
    if not lien:
        return {}
    ex = dossier / "exercices.txt"
    texte = ex.read_text(encoding="utf-8")
    faits = {}
    for cle, eid in lien.items():
        texte, n = re.subn(rf"^Id:[ \t]*{re.escape(cle)}[ \t]*$", f"Id: {eid}", texte, flags=re.M)
        if n:
            faits[cle] = eid
    ex.write_text(texte, encoding="utf-8")
    corr = dossier / "figures" / "correspondance.json"
    if corr.exists():
        data = json.loads(corr.read_text(encoding="utf-8"))
        zone = data.get("exercices", {})
        for cle, eid in lien.items():
            if cle in zone:
                zone[str(eid)] = zone.pop(cle)
                faits[cle] = eid
        corr.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return faits


if __name__ == "__main__":
    for d in sys.argv[1:]:
        print(Path(d).name, relier(d))
