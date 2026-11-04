"""Retouches finales de vocabulaire et d'accord ; aucune source modifiée."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPLACEMENTS = {
    15: {
        'sur (d)': 'sur la droite (d)',
        'avec (d)': 'avec la droite (d)',
        'à (d)': 'à la droite (d)',
        'et (d)': 'et la droite (d)',
        'de (d)': 'de la droite (d)',
        'depuis (d)': 'depuis la droite (d)',
        'entre (d1) et (d3)': 'entre les droites (d1) et (d3)',
        'perpendiculaire à (d1)': 'perpendiculaire à la droite (d1)',
        'perpendiculaire (d3) à (d2)': 'droite (d3) perpendiculaire à la droite (d2)',
        'point P de (d2)': 'point P de la droite (d2)',
        'sur (d1)': 'sur la droite (d1)',
        'on trace (d2)': 'on trace la droite (d2)',
        'puis à (d3)': 'puis à la droite (d3)',
        'perpendiculaires à (d2)': 'perpendiculaires à la droite (d2)',
    },
    18: {'donne-tu': 'donnes-tu'},
}
for number, changes in REPLACEMENTS.items():
    directory = next(ROOT.glob(f'{number:02}_*'))
    for name in ('exercices.txt', 'donnees_questions.json'):
        path = directory / name
        text = path.read_text(encoding='utf-8')
        for old, new in changes.items():
            text = text.replace(old, new)
        path.write_text(text, encoding='utf-8')
