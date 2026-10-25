"""Oublie les prises mémorisées contenant un motif, pour qu'elles soient rejugées.

  python -X utf8 outils/oublier_prises.py "Lyon" "The US."
"""
import json
import pathlib
import sys

f = pathlib.Path(__file__).resolve().parent.parent / "build" / "prises.json"
d = json.loads(f.read_text(encoding="utf-8"))
avant = len(d)
d = {k: v for k, v in d.items() if not any(m in k for m in sys.argv[1:])}
f.write_text(json.dumps(d, ensure_ascii=False, indent=0), encoding="utf-8")
print(f"{avant - len(d)} prise(s) oubliée(s)")
