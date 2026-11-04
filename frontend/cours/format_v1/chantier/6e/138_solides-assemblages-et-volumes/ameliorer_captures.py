# -*- coding: utf-8 -*-
"""Évite que l’en-tête d’aperçu collant masque les cartes photographiées."""
from pathlib import Path
R=Path(__file__).resolve().parent.parent
needle="  await page.click('.ap-tab[data-tab=\"exercices\"]')"
line="\n  // Prise de vue seulement : l’en-tête ne doit pas recouvrir la carte.\n  await page.addStyleTag({content:'.ap-top{position:static!important}'})"
for n in (138,139,146,147,148,149,152):
    p=next(R.glob(f'{n}_*'))/'captures_complementaires.mjs'
    text=p.read_text(encoding='utf8')
    assert needle in text
    if 'Prise de vue seulement' not in text:
        p.write_text(text.replace(needle,needle+line),encoding='utf8')
    print(n,'cadrage complet des cartes')
