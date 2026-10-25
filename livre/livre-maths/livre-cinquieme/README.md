# OptiTAB - Mathématiques - Cinquième

Édition France 2026-2027. Nouveau programme du BO n° 10 du 5 mars 2026
(arrêté du 18 février 2026, application en Cinquième à la rentrée 2026).
Édition revue le 23 octobre 2026.

## Audit de conformité du 23 octobre 2026

Le livre a été comparé, attendu par attendu, à l'annexe 2 du BO
(programme de mathématiques du cycle 4, rubriques de Cinquième) et au
document Éduscol « Exemples pour la mise en œuvre des programmes 2026,
cycle 4 ». La matrice complète (117 attendus, emplacements dans le livre,
écarts, corrections, points à décider) est dans
build/qa/audit-programme-2026-10-23.json.

Corrections principales : valeur absolue vue comme distance à zéro sans
notation exigible, définition de l'opposé, rangement décroissant,
équations x/3 = 1 et 2x = 0, tableau de proportionnalité contextualisé,
statut admis ou démontré des propriétés de géométrie, démonstration par
le demi-tour, cas des angles droits, cercle circonscrit du triangle
rectangle, concours des médianes, perspective cavalière à compléter,
aire du disque justifiée, moyenne quand toutes les données augmentent,
échelle de probabilité. Les exercices 15.6 et 15.15 n'utilisent plus
d'outils de Seconde. Le nombre d'exercices et la pagination (328 pages)
sont inchangés.

Les textes officiels consultés sont conservés hors du livre, dans
tmp/pdfs/recherche-cinquieme-audit/.

20 chapitres, 300 exercices progressifs, 20 défis facultatifs, deux bilans
annuels originaux avec leurs corrigés. Les cours, exercices et solutions
sont rédigés dans les fichiers contenu, approfondissements, bilans et
ressources. Les références officielles et la matrice de correspondance
figurent dans liminaires_contenu.py.

Les sources sont autonomes : le modèle de la collection et les logos sont
inclus. Aucun autre dossier de livre n'est nécessaire pour reconstruire.

Prérequis : Python avec sympy, pymupdf et pillow ; LuaLaTeX avec les
polices et paquets de la collection ; Poppler (pdftoppm).

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

Après le rendu de toutes les pages, les planches et pages critiques doivent
être relues. Le fichier build/qa/relecture-visuelle.json consigne cette
relecture pour le SHA-256 du PDF concerné. Une régénération isolée des
sources est également consignée dans build/controle-reproduction.json.

La livraison est effectuée par livrer.py après ces vérifications. Les
rapports décrivent la portée réelle des contrôles : ils accompagnent la
relecture sans prétendre prouver formellement chaque phrase du livre.
