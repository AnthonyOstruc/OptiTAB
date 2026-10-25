# Manuels OptiTAB — Options de Terminale

Deux manuels autonomes reprennent la charte LaTeX du manuel de Terminale : polices Libertinus et Montserrat, cours structurés, figures vectorielles, exercices progressifs et navigation entre énoncés et corrigés.

| Manuel | Chapitres | Exercices corrigés | Questions | Figures | Dossiers | Évaluations | Pages |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Mathématiques complémentaires | 13 | 156 | 468 | 18 | 9 | 3 | 133 |
| Mathématiques expertes | 12 | 144 | 432 | 19 | 9 | 3 | 126 |

Les questions des dossiers et des évaluations s'ajoutent aux questions des exercices. Les trois évaluations de chaque manuel comportent un corrigé et un barème sur 20.

## Programmes et recherche

Références consultées le 23 octobre 2026 :

- [Éduscol — Programmes et ressources en mathématiques, voie générale et technologique](https://eduscol.education.gouv.fr/5817/programmes-et-ressources-en-mathematiques-voie-gt).
- [Mathématiques complémentaires — programme 2019](https://www.education.gouv.fr/bo/19/Special8/MENE1921265A.htm), applicable pendant l'année scolaire 2026-2027.
- [Mathématiques expertes — programme 2019](https://www.education.gouv.fr/bo/19/Special8/MENE1921264A.htm), programme de référence de l'option.
- [Nouveau programme de mathématiques complémentaires](https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2902920A), applicable à la rentrée 2027 : concordance supplémentaire dans le manuel de complémentaires.

Les PDF officiels et leur extraction textuelle sont conservés dans le dossier `recherche/` de chaque manuel. Chaque livre contient une correspondance entre les attendus, les chapitres et les exercices. Les neuf thèmes du programme de complémentaires ont chacun leur dossier. Les démonstrations et les trois ensembles du programme d'expertes sont repérés dans sa concordance.

Les cours, exercices, dossiers et évaluations sont des créations éditoriales OptiTAB. Les livres sont indépendants du ministère et ne présentent pas leurs exercices comme des sujets officiels. Aucun ISBN ni agrément n'est inventé.

## Reconstruire un manuel

Depuis la racine du projet, avec Python, LuaLaTeX, les polices de la charte et les bibliothèques Python utilisées par les scripts :

```powershell
python livres-options-terminale/construire.py complementaires
python livres-options-terminale/figures.py complementaires
python livres-options-terminale/compiler.py complementaires
python livres-options-terminale/verifier.py complementaires
python livres-options-terminale/controler_calculs.py complementaires
```

Remplacer `complementaires` par `expertes` pour le second manuel. La compilation doit se terminer avant la vérification. La génération des figures n'est nécessaire que lorsque leur source change.

## Vérification et livraison

La vérification contrôle la présence des réponses, les niveaux de difficulté, les renvois, les liens internes, les caractères, les débordements et les programmes Python. Elle produit les images de toutes les pages et les planches de relecture dans `tmp/pdfs/qa-<option>/`.

Les calculs clés sont contrôlés séparément avec des fractions exactes, SymPy et des calculs numériques : 90 contrôles pour complémentaires et 173 pour expertes. Le rapport précise chaque valeur vérifiée ; ces contrôles ciblés complètent la relecture du contenu.

Après inspection des planches et des pages critiques rendues par Poppler, `build/validation-visuelle.json` enregistre l'empreinte SHA-256 du PDF relu. Toute modification du PDF impose une nouvelle vérification et une nouvelle validation visuelle.

```powershell
python livres-options-terminale/livrer.py complementaires
python livres-options-terminale/livrer.py expertes
python outils/organiser_pdf.py
```

La livraison refuse un PDF dont les contrôles ou l'empreinte ne correspondent pas au fichier validé. Les copies sont déposées dans `output/pdf/France/Mathématiques/` et dans `Desktop/Livres OptiTAB - Lycée/`. Les rapports de livraison sont dans `output/verification/`.
