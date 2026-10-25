# OptiTAB — Mathématiques — CM1

Édition France 2026-2027. Programme du cycle 3 publié au BO n° 16 du
17 avril 2025, rubriques « cours moyen première année », applicable
depuis la rentrée 2025.

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

Limites du CM1 respectées : entiers jusqu'à 999 999 ; fractions de
dénominateur au plus 20 et fractions décimales ; décimaux aux
centièmes ; division euclidienne par un diviseur à un chiffre ;
conversions raisonnées sans tableau de conversion ; pas de calculatrice ;
angles comparés sans rapporteur ; symétrie sur quadrillage (axes
horizontaux et verticaux) ; patron du cube ; proportionnalité en
langage naturel, sans tableau ni produit en croix ; hasard qualitatif.
