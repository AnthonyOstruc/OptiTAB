"""Raccourcit le libellé de saisie pour garder les blocs lisibles sur mobile."""
from pathlib import Path
import re
D=Path(__file__).resolve().parent
for p in [*D.glob('cours_*.txt'),*D.glob('fiche_*.txt'),D/'exercices.txt']:
    text=p.read_text(encoding='utf-8')
    text=re.sub(r'^demander .+ et attendre$', 'demander « Nombre ? » et attendre', text,flags=re.M)
    p.write_text(text,encoding='utf-8')
