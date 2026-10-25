# Livre d'exercices OptiTAB — Terminale spécialité, édition 2027-2028

Nouvelle édition du livre `../livre` (programme de 2019), adaptée au programme de spécialité mathématiques de Terminale
applicable à la **rentrée 2027** (baccalauréat 2028). Le livre `../livre` n'est pas modifié et reste valable en 2026-2027.

## Textes officiels suivis

- Programme de Terminale, spécialité mathématiques : arrêté du 26 février 2026 (JO du 27 mars 2026), NOR MENE2602919A,
  BO n° 14 du 2 avril 2026, applicable à la rentrée 2027-2028.
- Programme de Première, spécialité mathématiques (continuité) : NOR MENE2602917A, même BO, rentrée 2026-2027.
- Épreuve de spécialité mathématiques : note de service du 11 septembre 2026, NOR MENE2622642N, BO spécial n° 4 du
  17 septembre 2026 (4 h, 4 exercices de 4 à 8 points, 2 points sur 20 de maîtrise de la langue).
- Maîtrise de la langue à tous les examens à compter de la session 2027 : note de service NOR MENE2623195N, même BO.

Les textes téléchargés et la comparaison avec 2019 sont dans `../tmp/pdfs/recherche-terminale-2027/` (voir `ETAT.md`).

## Ce qui change par rapport à l'édition 2019

- Chapitre 6 : les fonctions sinus et cosinus (parité, périodicité, courbes, lien avec le cercle) ne sont plus vues en
  Première ; section 2 de « L'essentiel » réécrite, exercices 3 et 4 nouveaux (15 exercices).
- Chapitre 13 : plans perpendiculaires (théorème, démonstration, figure), exercice 9 nouveau (12 exercices).
- Chapitre 23, nouveau : « Ensembles, logique et raisonnement » (partie transversale du programme), 12 exercices.
- Chapitre 20 : affectation notée ← en langage naturel, programmation modulaire.
- Prérequis des chapitres 3, 6, 16, 17 et 18 alignés sur la Première 2026.
- Sujets type bac : exercices sur 18 points + 2 points de maîtrise de la langue, QCM justifiés, page « La maîtrise de la
  langue » avec la grille officielle (`bac/maitrise-langue.tex`).
- Liminaires : page « Nouveau programme » et correspondance programme / chapitres (`liminaires/nouveau-programme.tex`),
  avant-propos, titre, mentions légales et couvertures « Édition 2027-2028 · Nouveau programme ».
- Les nouveautés sont signalées dans le livre par la pastille « Programme 2027 » (`\otNouveau`).

## Structure

- `main.tex` : le livre ; `optitab-livre.sty` : le template ; `plan.tex` : plan (23 chapitres, 289 exercices)
- `chapitres/`, `corriges/` : énoncés et corrigés ; `bac/` : 10 sujets type bac, corrigés avec barème, page de langue
- `liminaires/`, `couverture/`, `images/`
- `outils/compiler.py` : compilation jusqu'à stabilisation + contrôle du journal
- `outils/bareme_2027.py`, `outils/qcm_justifies_2027.py` : transformations appliquées une fois aux sujets de 2019
  (conservées pour traçabilité ; ne pas relancer)
- `verifier_edition_2027.py` : contrôles (structure, barèmes, calculs SymPy des contenus nouveaux)

## Compiler

Depuis ce dossier :

```
python -I -X utf8 outils/compiler.py
python -I -X utf8 verifier_edition_2027.py
```

ou à la main, quatre passes (onglets, renvois de pages et images positionnées) :

```
lualatex -interaction=nonstopmode -aux-directory=build main.tex
```

## État au 23 octobre 2026

- Copie de départ recompilée à l'identique de `../livre/main.pdf` (374 pages, texte et rendu identiques page à page).
- Édition 2027-2028 : 398 pages, 23 chapitres, 289 exercices, 10 sujets type bac ; zéro « Overfull », zéro caractère
  manquant, zéro renvoi indéfini ; toutes les pages rendues en planches et relues.
- Livraison (`python -I -X utf8 outils/livrer.py`) :
  `../output/pdf/France/Mathématiques/OptiTAB - Mathématiques - Terminale spécialité - Programme 2027 - Manuel complet.pdf`,
  `~/Desktop/Livres OptiTAB - Lycée/OptiTAB - Mathématiques - Terminale spécialité (programme 2027).pdf`,
  `../output/sources/optitab-terminale-2027-sources.zip`.

## Reste à compléter par l'éditeur

ISBN et dépôt légal (page de mentions légales et 4e de couverture) : une nouvelle édition demande un nouvel ISBN.
