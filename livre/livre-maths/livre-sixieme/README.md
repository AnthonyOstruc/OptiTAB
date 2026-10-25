# OptiTAB — Mathématiques — Sixième

Édition France 2026-2027. Programme de mathématiques du cycle 3 publié
au BO n° 16 du 17 avril 2025, rubriques « Sixième », applicable en
Sixième depuis la rentrée 2025.

21 chapitres en quatre parties, 84 sections de cours, 315 exercices
progressifs, 21 défis facultatifs, deux bilans originaux avec leurs
corrigés. Les cours, exercices et solutions sont rédigés dans les
fichiers contenu, approfondissements, bilans et ressources. Les figures
sont produites par generer_figures.py et figures_suite.py. Les
références officielles et la matrice de correspondance figurent dans
liminaires_contenu.py.

La maquette précédente (structure sans contenu) est archivée dans
build/maquette-initiale.

Les sources sont autonomes : le modèle de la collection et les logos
sont inclus. Aucun autre dossier de livre n'est nécessaire pour
reconstruire ce volume.

Prérequis : Python avec sympy, pymupdf et pillow ; LuaLaTeX avec les
polices et paquets de la collection (Libertinus, Montserrat, Fira Mono) ;
Poppler (pdftoppm).

Depuis ce dossier :

    python verifier_contenu.py
    python verifier_figures.py
    python construire.py
    python compiler.py
    python controler_pdf.py
    python rendre_poppler.py

Le compilateur travaille sur une copie isolée. Ne pas régénérer les
sources LaTeX, styles et images pendant la compilation. Il stabilise les
renvois et refuse les débordements ou caractères manquants.

Après le rendu de toutes les pages, les planches et pages critiques
doivent être relues. Le fichier build/qa/relecture-visuelle.json
consigne cette relecture pour le SHA-256 du PDF concerné. Une
régénération isolée des sources est consignée dans
build/controle-reproduction.json.

La livraison est effectuée par livrer.py après ces vérifications.

Limites de la Sixième respectées : entiers jusqu'aux milliards ;
écritures d'un décimal (virgule, fraction décimale, nombre mixte,
pourcentage) ; arrondis, y compris de nombres non décimaux ; produit de
deux décimaux ; division euclidienne par un entier inférieur à 100 et
division décimale par un entier inférieur à 10 ; fraction quotient,
égalités à trous, guide-âne ; sommes de fractions et produit par un
entier ; pourcentages ; schémas en barres et motifs évolutifs sans
lettres formelles ; périmètre du disque ; conversions d'aires entre m²,
dm² et cm² ; cm³ par dénombrement ; durées en base soixante et heures
décimales ; distances, cercle, médiatrice, angles et rapporteur,
bissectrice, triangles, cercle circonscrit ; symétrie axiale sur
quadrillage, papier pointé et papier uni ; assemblages de cubes ;
proportionnalité dans le cadre des grandeurs, sans produit en croix ;
probabilités entre 0 et 1 et fréquences ; instructions, entrées,
sorties, répétitions et chemins.
