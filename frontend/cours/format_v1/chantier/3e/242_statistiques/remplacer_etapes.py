# -*- coding: utf-8 -*-
"""Remplace Étapes + Solution d'un exercice : python remplacer_etapes.py ID fichier."""
import sys
from pathlib import Path

ident, src = sys.argv[1], sys.argv[2]
p = Path(__file__).with_name("exercices.txt")
t = p.read_text(encoding="utf-8")
i = t.index("Id: %s\n" % ident)
f = t.index("\n===\n", i)
e = t.index("\nÉtapes:\n", i)
assert e < f
neuf = Path(src).read_text(encoding="utf-8").rstrip("\n") + "\n"
t = t[:e + 1] + neuf + t[f:]
p.write_text(t, encoding="utf-8")
print("ok", ident)
