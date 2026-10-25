# OptiTAB — Mathématiques — CM2

Édition France 2026-2027. Programme du cycle 3 publié au BO n° 16 du
17 avril 2025, rubriques « cours moyen deuxième année », applicable
en CM2 depuis la rentrée 2026 (article 3 de l’arrêté du 10 avril 2025).

21 chapitres, 315 exercices progressifs, 21 défis facultatifs, deux
bilans originaux avec leurs corrigés. Les cours, exercices et solutions
sont rédigés dans les fichiers contenu, approfondissements, bilans et
ressources. Les références officielles et la matrice de correspondance
figurent dans liminaires_contenu.py.

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

La livraison est effectuée par livrer.py après ces vérifications. Les
rapports décrivent la portée réelle des contrôles : ils accompagnent la
relecture sans prétendre prouver formellement chaque phrase du livre.

Limites du CM2 respectées : entiers jusqu'à 999 999 999 ; diviseurs et
multiples communs dans les bornes du programme ; fractions de
dénominateur au plus 60 et fractions décimales jusqu'aux millièmes ;
divisions décimales par un diviseur à un chiffre ; programmes de calcul
jusqu'à trois instructions ; conversions raisonnées sans tableau ; aires
du carré et du rectangle en cm², dm² et m² ; angle droit de 90 degrés,
sans rapporteur ; durées jusqu'à la seconde ; trapèzes, pentagones et
hexagones ; symétrie sur quadrillage, y compris le long d'une diagonale ;
patrons du cube et du pavé ; proportionnalité en langage naturel, sans
tableau ni produit en croix ; probabilités « a chances sur b ».
