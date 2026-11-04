"""Lever l’ambiguïté sur le signe de zéro dans les questions 263."""
from pathlib import Path
p=next(Path(__file__).resolve().parent.parent.glob('263_*'))/'exercices.txt'
t=p.read_text(encoding='utf8')
t=t.replace('une abscisse négative ?', 'une abscisse strictement négative ?')
p.write_text(t,encoding='utf8')
