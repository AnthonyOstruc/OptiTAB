# -*- coding: utf-8 -*-
"""Remplace le contenu d'un bloc d'exercice (après la ligne Id:) : python remplacer_bloc.py ID fichier [nouveau titre]."""
import sys
from pathlib import Path

ident, src = sys.argv[1], sys.argv[2]
titre = sys.argv[3] if len(sys.argv) > 3 else None
p = Path(__file__).with_name("exercices.txt")
t = p.read_text(encoding="utf-8")
i = t.index("Id: %s\n" % ident) + len("Id: %s\n" % ident)
f = t.index("\n===\n", i)
neuf = Path(src).read_text(encoding="utf-8").rstrip("\n") + "\n"
t = t[:i] + neuf + t[f:]
if titre:
    d = t.rfind("=== ", 0, i)
    e = t.index("\n", d)
    t = t[:d] + "=== " + titre + t[e:]
p.write_text(t, encoding="utf-8")
print("ok", ident)
