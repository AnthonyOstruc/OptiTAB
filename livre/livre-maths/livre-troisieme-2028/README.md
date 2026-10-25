# OptiTAB — Troisième, édition 2028-2029 · Nouveau programme · Brevet 2029

Livre original de mathématiques pour la Troisième en France, année 2028-2029,
série générale du DNB. La charte de la collection est conservée.

Cette édition suit le programme de mathématiques du cycle 4 fixé par l’arrêté
du 18 février 2026 (BO n° 10 du 5 mars 2026), applicable en Troisième à la
rentrée 2028. Elle a été construite à partir de l’édition 2026-2027
(dossier livre-troisieme, brevet 2027), qui reste valable et n’est pas modifiée.

18 chapitres, 270 exercices progressifs, 18 défis avec deux indications chacun,
24 automatismes et 8 problèmes répartis dans deux brevets blancs corrigés.
Les exercices sont originaux ; les sources officielles définissent le périmètre.

## Brevet 2029

Au 23 octobre 2026, aucun texte propre à la session 2029 n’était publié. Les
brevets blancs suivent la définition de l’épreuve en vigueur à compter de la
session 2027 (note de service du 11-9-2026, NOR MENE2623228N, BO spécial n° 4
du 17-9-2026). Ce point est signalé dans le livre et doit être revérifié avant
la session 2029.

## Correspondance avec le programme

- MATRICE-PROGRAMME-2028.md : matrice ancien livre → programme 2026, contenus
  ajoutés, retirés, réactivés, vocabulaire, brevet, détail par chapitre.
- Dans le livre : page « Nouveau programme », correspondance rubrique par
  rubrique et 72 repères reliés aux exercices (liminaires_contenu.py).
- Textes officiels consultés : copies locales dans tmp/pdfs/recherche-troisieme-2028/.

## Reconstruire

Prérequis : Python 3, SymPy, PyMuPDF, Pillow, LuaLaTeX (MiKTeX), polices
Libertinus, Montserrat et Fira Mono, Poppler (pdftoppm). Les éléments de charte
nécessaires sont inclus dans _modele_collection : aucun autre livre de la
collection n’est nécessaire.

Depuis ce dossier :

    python verifier_contenu.py
    python verifier_figures.py
    python construire.py
    python compiler.py
    python controler_pdf.py
    python rendre_poppler.py

construire.py régénère entièrement chapitres/, corriges/, figures/, annexes/,
liminaires/, couverture/, main.tex, plan.tex et le manifeste à partir des
fichiers Python (contenu_*.py, approfondissements.py, bilans.py, ressources.py,
liminaires_contenu.py, donnees_*.py, generer_figures.py).

Le compilateur travaille dans un instantané isolé et refuse une modification
des sources LaTeX pendant la compilation. Il stabilise les renvois et la
pagination, puis refuse tout débordement, caractère manquant ou étiquette en double.

controler_pdf.py vérifie le PDF (renvois, figures sur la page de leur texte,
hauteur des blocs, pages blanches, texte hors page, mentions de l’édition
précédente) et rend toutes les pages en planches de six (build/qa/planche-*.png),
qui doivent être relues. reproduire.py reconstruit le livre dans un dossier
isolé et compare sources et rendus. livrer.py n’accepte de livrer qu’un PDF
dont la relecture visuelle est consignée dans build/qa/relecture-visuelle.json.

Les scripts par blocs sont définis dans donnees_scripts.py ; la même structure
sert à afficher les blocs et à exécuter les tests de trace. Les figures sur
quadrillage du chapitre 15 sont décrites dans donnees_vecteurs.py et contrôlées
par verifier_figures.py.

Les contrôles numériques et de structure soutiennent la relecture ; ils ne
constituent pas une preuve formelle automatique de l’intégralité du texte.
Les pages lignées intitulées Notes sont intentionnelles.
