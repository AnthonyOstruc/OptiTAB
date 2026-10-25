"""Contrôles du PDF compilé : format A4, renvois non résolus (« ?? »), pages vides, pages « Notes », signets.

Usage, depuis livre-terminale-2027 : python -I -X utf8 outils/controler_pdf.py [main.pdf]
"""
import re
import sys
from pathlib import Path

import fitz

R = Path(__file__).resolve().parent.parent
doc = fitz.open(sys.argv[1] if len(sys.argv) > 1 else R / "main.pdf")
problemes = []
notes = []
for i, p in enumerate(doc):
    w, h = p.rect.width, p.rect.height
    if abs(w - 595.28) > 1 or abs(h - 841.89) > 1:
        problemes.append(f"p.{i + 1} : format {w:.0f} x {h:.0f}")
    t = p.get_text()
    if "??" in t:
        problemes.append(f"p.{i + 1} : renvoi non résolu « ?? »")
    if "�" in t:
        problemes.append(f"p.{i + 1} : caractère de remplacement")
    if t.strip().startswith("Notes") and len(t.strip()) < 12:
        notes.append(i + 1)
    elif not t.strip() and not p.get_images():
        problemes.append(f"p.{i + 1} : page sans texte")
toc = doc.get_toc()
print(f"{doc.page_count} pages ; {len(toc)} signets ; pages « Notes » : {notes}")
print("titre PDF :", doc.metadata.get("title"))
print("Problèmes :", len(problemes))
for x in problemes:
    print("   ", x)
