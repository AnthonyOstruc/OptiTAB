"""Séparer les raisonnements composés conservés, sans changer leurs calculs."""
from pathlib import Path
import re
BASE=Path(__file__).resolve().parent.parent
p=next(BASE.glob('264_*'))/'exercices.txt'
t=p.read_text(encoding='utf8')
t=t.replace('Contrôle par les variations : ', ':::\n\n::: etape Contrôler avec les variations de la journée\n')
p.write_text(t,encoding='utf8')
p=next(BASE.glob('262_*'))/'exercices.txt'
t=p.read_text(encoding='utf8')
pat=re.compile(r'::: etape Organiser toutes les possibilités\n(Diviseurs de [^\n]+)\n\n(Diviseurs de [^\n]+)\n\n(On conserve seulement[^\n]+)\n:::')
t=pat.sub(lambda m:'::: etape Lister les diviseurs du premier effectif\n'+m[1]+'\n:::\n\n::: etape Lister les diviseurs du second effectif\n'+m[2]+'\n:::\n\n::: etape Garder les diviseurs communs\n'+m[3]+'\n:::',t)
p.write_text(t,encoding='utf8')
