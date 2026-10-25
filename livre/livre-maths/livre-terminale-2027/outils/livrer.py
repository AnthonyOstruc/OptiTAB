"""Livraison de l'édition 2027-2028 : PDF complet et archive des sources (nouveaux fichiers uniquement).

Usage, depuis livre-terminale-2027 : python -I -X utf8 outils/livrer.py
"""
import shutil
import zipfile
from pathlib import Path

R = Path(__file__).resolve().parent.parent
DEPOT = R.parent
PDF = R / "main.pdf"
CIBLES = [
    DEPOT / "output/pdf/France/Mathématiques/OptiTAB - Mathématiques - Terminale spécialité - Programme 2027 - Manuel complet.pdf",
    Path.home() / "Desktop" / "Livres OptiTAB - Lycée" / "OptiTAB - Mathématiques - Terminale spécialité (programme 2027).pdf",
]
ZIP = DEPOT / "output" / "sources" / "optitab-terminale-2027-sources.zip"

for c in CIBLES:
    c.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PDF, c)
    print("PDF :", c)

EXCLUS_DOSSIERS = {"build", "__pycache__"}
with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED) as z:
    n = 0
    for f in sorted(R.rglob("*")):
        rel = f.relative_to(R)
        if f.is_dir() or rel.parts[0] in EXCLUS_DOSSIERS or f.suffix in {".synctex", ".gz", ".log", ".aux"} or f.name == "main.pdf":
            continue
        z.write(f, Path("livre-terminale-2027") / rel)
        n += 1
print("Sources :", ZIP, f"({n} fichiers)")
