# OptiTAB — Mathématiques de Quatrième · Édition 2027-2028 · Nouveau programme

Nouvelle édition du 23 octobre 2026, conforme au programme de mathématiques
du cycle 4 fixé par l’arrêté du 18 février 2026 (BO n° 10 du 5 mars 2026,
NOR MENE2602912A, annexe 2), applicable en Quatrième à la rentrée 2027-2028.
L’édition 2026-2027 (programme 2020), dans `livre-quatrieme/`, reste celle de
l’année en cours ; ce dossier est une copie autonome, entièrement reprise.

18 chapitres, 270 exercices progressifs (15 par chapitre : 5 de découverte,
5 d’entraînement, 5 problèmes), 18 défis, deux bilans annuels, tous corrigés.
Page « Ce qui change », démonstrations, fiches outils, repérage des exercices
et matrice des objectifs officiels de Quatrième en fin de livre.

## Sources officielles

- Arrêté et calendrier : https://www.education.gouv.fr/bo/2026/Hebdo10/MENE2602912A
- Annexe 2, programme du cycle 4 : https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf
- Exemples pour la mise en œuvre des programmes 2026, cycle 4 (Éduscol) : https://eduscol.education.gouv.fr/sites/default/files/document/exemple-mise-en-oeuvre-c4-mathematiques0pdf-126080.pdf

Les copies téléchargées et leurs textes extraits sont dans
`tmp/pdfs/recherche-quatrieme-2027/`.

## Fichiers de données

- `contenu_01_03.py` … `contenu_16_18.py` : cours, exercices, corrigés et
  contrôles SymPy de chaque exercice.
- `approfondissements.py` (défis), `bilans.py`, `ressources.py` (preuves,
  fiches outils), `liminaires_contenu.py` (liminaires, sources, matrice).
- `generer_figures.py`, `outils_figures.py`, `donnees_scripts.py` : figures
  TikZ et scripts par blocs, avec leurs données géométriques contrôlées.
- `matrice_programme.py` : matrice ancien livre → nouveau programme
  (`build/matrice-programme.md`).

## Reproduction

Python 3 avec SymPy, PyMuPDF et Pillow ; LuaLaTeX (MiKTeX, paquets et polices
de la collection) ; Poppler (`pdftoppm`). Le modèle de la collection et les
logos sont inclus ; aucun autre dossier de livre n’est nécessaire.

Depuis ce dossier :

    python verifier_contenu.py
    python verifier_figures.py
    python construire.py
    python compiler.py
    python controler_pdf.py
    python rendre_poppler.py
    python matrice_programme.py

Le constructeur efface puis régénère les dossiers produits (chapitres,
corrigés, figures, annexes, liminaires, couverture). Le compilateur travaille
sur une copie isolée, stabilise les renvois et refuse tout débordement ou
caractère manquant. Ne pas modifier les sources pendant la compilation.

Après le rendu de toutes les pages, les planches et les pages critiques sont
relues ; `build/qa/relecture-visuelle.json` consigne cette relecture pour le
SHA-256 du PDF concerné, et `build/controle-reproduction.json` une
régénération isolée des sources. `livrer.py` exige ces contrôles, puis écrit
uniquement des fichiers nouveaux suffixés « 2027 » :

- `output/pdf/optitab-quatrieme-2027-complet.pdf`
- `output/sources/optitab-quatrieme-2027-sources.zip`
- `output/verification/*-quatrieme-2027.*`
- `Desktop/Livres OptiTAB - Lycée/OptiTAB - Mathématiques - Quatrième (programme 2027).pdf`

Les empreintes des fichiers de l’édition 2026-2027 sont vérifiées avant et
après la copie. Les contrôles informatiques soutiennent une relecture
pédagogique et visuelle ; ils ne remplacent pas une expertise humaine
indépendante.
