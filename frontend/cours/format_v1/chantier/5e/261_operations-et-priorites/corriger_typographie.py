"""Correction locale de neuf retours littéraux échappés repérés par l’audit."""
from pathlib import Path
p=next(Path(__file__).resolve().parent.parent.glob('265_*'))/'exercices.txt'
t=p.read_text(encoding='utf8')
t=t.replace(r'\n\nPartager la même unité', '\n\nPartager la même unité')
p.write_text(t,encoding='utf8')
