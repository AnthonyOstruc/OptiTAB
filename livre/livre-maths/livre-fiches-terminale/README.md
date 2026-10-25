# OptiTAB — L'essentiel · Mathématiques Terminale spécialité

Collection de **fiches de révision** : une fiche de 3 à 4 pages par chapitre, avec
le cours essentiel, les formules, les schémas, les méthodes, les pièges, la
rédaction type bac et une check-list. Programme de référence : Terminale
spécialité, BO spécial n°8 du 25/07/2019 (en vigueur en 2026-2027).

## Structure

- `main.tex` : couverture, sommaire, mode d'emploi, puis les fiches.
- `plan.tex` : les 23 fiches (même numérotation que le livre OptiTAB de Terminale
  `livre/`, plus la fiche 23 « Ensembles, logique et raisonnement ») ; le sommaire
  affiche la page des fiches rédigées et « à paraître » pour les autres.
- `fiches/NN-titre.tex` : une fiche ; `\partieFiches{Analyse}{otNavy}` avant la
  première fiche de chaque partie (Géométrie `otGreenDark`, Probabilités
  `otOrangeDark`, Algorithmique et logique `otViolet`).
- `optitab-fiches.sty` : le gabarit (charte OptiTAB, marges resserrées, 10 pt).
- `verifications/fiche_NN.py` : toutes les valeurs et formules de la fiche NN.

## Macros du gabarit

- `\fiche[décor]{n}{titre}{mots-clés séparés par \sepmot}` : bandeau d'ouverture.
- `\sect{titre}` : section numérotée de la fiche.
- Encadrés : `definition`, `theoreme`, `propriete`, `methode`, `attention`,
  `exemple`, `redaction` (rédiger au bac), `demonstration` (preuves exigibles),
  chacun avec un intitulé facultatif `[...]` ; `\formule{...}` (formule clé) ;
  `paire` (deux encadrés côte à côte, de même hauteur).
- `\strategie{titre}{{situation}/{démarche},...}` : schéma de décision.
- `python` (code), `jesais` (check-list), `\pourAllerPlusLoin{...}` (renvoi au
  livre et au site, avec QR code), tableaux avec `\otTableau`, colonnes `L{largeur}`
  pour les intitulés, `\otTH{...}` pour les en-têtes.

## Règles

- Une fiche = 3 ou 4 pages, jamais plus (vérifier après compilation).
- Chaque valeur numérique est vérifiée par le script de la fiche avant impression.
- Recompiler (deux passes) puis inspecter les pages rendues : 0 erreur,
  0 débordement, 0 caractère manquant.

## Compilation

```
"$LOCALAPPDATA/Programs/MiKTeX/miktex/bin/x64/lualatex.exe" -interaction=nonstopmode \
  -file-line-error -aux-directory=build main.tex
```

## État

- [x] Gabarit, couverture, sommaire, mode d'emploi
- [x] Fiche 01 — Suites numériques (4 pages, 48 vérifications) — en attente de validation
- [ ] Fiches 02 à 23
