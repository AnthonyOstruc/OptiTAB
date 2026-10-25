# OptiTAB — Troisième, brevet 2027

Livre original de mathématiques pour la Troisième en France, année 2026-2027,
série générale du DNB. La charte de la collection de lycée est conservée.

18 chapitres, 270 exercices progressifs, 18 défis avec deux indications chacun,
24 automatismes et 8 problèmes répartis dans deux brevets blancs corrigés.
Les exercices sont originaux ; les sources officielles définissent le périmètre.

Le programme publié en 2026 s'appliquera en Troisième en 2028-2029.
Cette édition suit les attendus annuels actuellement applicables, ainsi que la
définition de l'épreuve publiée en septembre 2026, applicable au brevet 2027.
Les références et la matrice de repérage sont intégrées au livre.

## Reconstruire

Prérequis : Python 3, SymPy, PyMuPDF, Pillow, LuaLaTeX, polices Libertinus,
Montserrat et Fira Mono. Utiliser un environnement LaTeX contenant les
extensions mentionnées dans les fichiers de style.
Les éléments de charte nécessaires sont inclus dans _modele_collection :
aucun autre livre de la collection n’est nécessaire pour reconstruire ce volume.

Depuis ce dossier :

    python verifier_contenu.py
    python verifier_figures.py
    python construire.py
    python compiler.py
    python controler_pdf.py

Le compilateur travaille dans un instantané isolé et refuse une modification
des sources LaTeX pendant la compilation. Il stabilise les renvois et la
pagination, puis contrôle les avertissements typographiques.

Les scripts par blocs sont définis dans donnees_scripts.py. La même structure
sert à afficher les blocs et à exécuter les tests de trace. La syntaxe graphique
est une représentation pédagogique de type Scratch, sans dépendance à Python
pour l'élève et sans prétendre être une capture de l'interface Scratch.

Les contrôles numériques et de structure soutiennent la relecture ; ils ne
constituent pas une preuve formelle automatique de l'intégralité du texte.
La livraison nécessite aussi la lecture des planches de rendu et des pages
critiques. Les pages lignées intitulées Notes sont intentionnelles.
