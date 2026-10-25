# OptiTAB - Mathématiques de Seconde

Livre complet de Seconde générale et technologique française, édition du 23 octobre 2026.
Charte issue du livre de Première de la même collection.

16 chapitres, 240 exercices de chapitre corrigés, 16 défis facultatifs avec deux indications chacun,
40 questions flash d’automatismes corrigées, 13 démonstrations, deux bilans corrigés
(20 automatismes et six problèmes), ateliers numériques, lecture d’un nuage de points,
culture mathématique et matrice de couverture.

Les quatre thèmes et les trois parties transversales du
[programme de 2026-2027](https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602914A)
sont repérés dans le livre. Toutes les pistes d’approfondissement de l’annexe sont traitées,
sans les présenter comme des attendus obligatoires.

## Audit de conformité du 23 octobre 2026

Texte relu intégralement : arrêté du 26-2-2026, BO n° 14 du 2 avril 2026, NOR MENE2602914A,
annexe pages 333 à 345 du [PDF officiel du BO](https://www.education.gouv.fr/sites/default/files/document/Bulletin%20officiel%20n%C2%B0%2014%20du%202%20avril%202026-515432.pdf)
(copie de travail : ../tmp/pdfs/recherche-seconde-audit/).
auditer_programme.py contient la matrice des 178 attendus officiels (dont les 30 capacités
« Automatismes »), chacun rattaché à des lieux du livre contrôlés dans les sources.

Corrections apportées : filet supérieur des tableaux (« oprule » visible sur 14 pages),
questions flash d’automatismes, affectation notée par une flèche et passage langage naturel / Python,
vocabulaire ensembliste (réunion, intersection, complémentaire, Card, proposition),
signe et taux d’accroissement des fonctions affines, comparaison par quotient, vecteur position
et représentants, filtres sur deux listes, notations hors programme retirées.
Le détail figure dans ../output/verification/verification-seconde-complet.md.
Version précédente : ../output/archives/optitab-seconde-complet-avant-audit-2026-10-23.pdf.

Les 103 fichiers de visuels sont vectoriels (TikZ), avec versions d’énoncé et de corrigé.
Les données réelles sont sourcées dans les exercices concernés.
Les autres données sont construites ; les exercices sont originaux.

## Reproduction

Les fichiers contenu_01_02.py à contenu_15_16.py contiennent cours, exercices, méthodes et contrôles.
Les modules approfondissements.py, bilans.py, demonstrations.py, ateliers.py et automatismes.py
contiennent les compléments. generer_figures.py crée les constructions ; construire.py génère les sources LaTeX.
La charte est lue dans gabarit/ (copie figée) : la construction ne dépend plus de livre-premiere.

Python 3, SymPy, PyMuPDF, Pillow et LuaLaTeX sont nécessaires.
Polices : Libertinus, Montserrat et Fira Mono.

    python construire.py
    python verifier_contenu.py
    python verifier_complements.py
    python auditer_programme.py
    python compiler.py
    python controler_pdf.py

compiler.py travaille sur une copie isolée et contrôle que les sources restent identiques.
controler_pdf.py rend toutes les pages et vérifie liens, blocs, association des figures à leur texte
et absence de fragments de commandes LaTeX visibles.
Après la relecture visuelle, livrer.py prépare les livrables.

La boucle volontairement erronée de l’exercice 15.13 est exclue de l’exécution automatique.
Les tests finis soutiennent la relecture des preuves, mais ne remplacent pas leurs arguments généraux.

## Livraison

- PDF : ../output/pdf/France/Mathématiques/OptiTAB - Mathématiques - Seconde générale et technologique - Manuel complet.pdf
- Copie : Bureau, Livres OptiTAB - Lycée, OptiTAB - Mathématiques - Seconde.pdf
- Sources : ../output/sources/optitab-seconde-complet-sources.zip
- Rapport : ../output/verification/verification-seconde-complet.md

Les livres de Terminale et de Première ne sont pas modifiés par ces scripts.
