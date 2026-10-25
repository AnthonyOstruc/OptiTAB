# OptiTAB — Mathématiques — Maternelle (PS, MS, GS)

Trois cahiers d’activités, un par année de maternelle, conformes au programme
de l’école maternelle (BO n° 41 du 31 octobre 2024, applicable à la rentrée
2025, version consolidée intégrant le BO n° 19 du 7 mai 2026). Chaque cahier
reprend les objectifs d’une tranche d’âge du programme :

| Cahier | Tranche du programme | Activités | Pages |
|---|---|---|---|
| Petite Section | « à aborder avant 4 ans » | 40 | 67 |
| Moyenne Section | « à partir de 4 ans » | 53 | 85 |
| Grande Section | « à partir de 5 ans » | 56 | 88 |

Une activité tient sur une page : bandeau, consigne lue par l’adulte, grande
illustration, étoile à colorier. Chaque cahier comprend aussi les pages
liminaires, des ouvertures de partie, un guide de l’adulte (objectif,
manipulation préalable, mots à faire dire, réponse avec vignette corrigée),
un repérage des objectifs du programme et les sources.

Choix pédagogiques imposés par le programme : aucun solide dessiné en
perspective (empreintes et faces à plat), formes dans toutes les orientations,
pas de zéro, comparaisons globales seulement quand une collection a au moins
deux fois plus d’objets que l’autre, manipulation avant la fiche.

## Organisation

- `commun/` : mise en page (`maternelle.sty`), bibliothèque d’illustrations
  TikZ (`objets.sty`), couverture, liminaires et 4e de couverture.
- `outils.py`, `gabarits.py` : fonctions de dessin et gabarits de figures.
- `ps.py`, `ms.py`, `gs.py` : contenu de chaque cahier (activités, rubriques du
  programme, textes du guide). Chaque activité déclare ses quantités et ses
  contrôles, vérifiés à la construction.
- `construire.py` : vérifie le contenu (limites de quantités par niveau,
  rubriques toutes travaillées, contrôles) et écrit les fichiers LaTeX.
- `compiler.py` : compile avec LuaLaTeX jusqu’à stabilité des renvois et refuse
  débordements, caractères manquants et activités sur plus d’une page.
- `rendre.py` : planches de pages pour la relecture visuelle (Poppler).
- `livrer.py` : copie les PDF et archive les sources.

## Reconstruire

Prérequis : Python 3 avec Pillow ; LuaLaTeX (MiKTeX) avec Montserrat ;
Poppler (`pdftoppm`).

    python construire.py ps
    python compiler.py ps
    python rendre.py ps
    (idem avec ms et gs)
    python livrer.py
