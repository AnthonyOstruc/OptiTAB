# Vérification du livre OptiTAB de Première

Édition du 23 octobre 2026, après audit de conformité. Première générale, spécialité mathématiques.

## Contenu livré

- 319 pages, 14 chapitres et 224 exercices corrigés : 210 exercices de chapitre et 14 défis d'approfondissement.
- Deux sujets blancs originaux au format de l'épreuve anticipée (session 2028) : 24 automatismes à réponses courtes issus des listes officielles, dont 6 lectures graphiques ou de tableau, et 4 exercices, corrigés et barème d'entraînement.
- Cours, méthodes, problèmes progressifs, 18 démonstrations de référence.
- 259 représentations dans les cours, exercices et annexes : figures, graphiques, arbres et tableaux, en plus des couvertures et décors d'ouverture.
- Les 30 exercices des deux chapitres de géométrie ont chacun leur figure, également reprise et complétée dans le corrigé ; six exercices géométriques de trigonométrie sont aussi illustrés.
- Pages de garde, avant-propos, mode d'emploi, parcours de travail, sommaire et suivi des exercices.
- 95 signets et 702 liens contrôlés.

## Programme

Référence : [BO du 2 avril 2026, NOR MENE2602917A](https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602917A), applicable à la rentrée 2026-2027.

La matrice éditoriale repère 60 groupes de contenus, capacités, démonstrations et exemples d'algorithmes dans les cours, exercices, sujets et annexes. Les approfondissements facultatifs sont sélectionnés ; le livre ne prétend pas les inclure tous. Les ressources transversales sont destinées à être utilisées au fil de l'année.

## Vérifications effectuées

- Correspondance des 210 énoncés avec 210 corrigés et progression de difficulté.
- 222 groupes de contrôles de résultats, répartis sur tous les exercices : calculs symboliques ou exacts, valeurs numériques, énumérations probabilistes et cas limites.
- Exécution des 23 blocs Python des chapitres, tests des fonctions et contrôle de la reproductibilité des simulations à graine fixée.
- Contrôle des 28 programmes extraits du PDF lui-même : syntaxe valide sans substitution de caractères, structure syntaxique fidèle aux sources, exécution et tests ciblés sur les neuf anomalies de l’audit fourni. L’indentation est reconstruite à partir des positions des glyphes ; le contrôle ne garantit pas le comportement de copie de tous les lecteurs PDF.
- 85 contrôles complémentaires de structure et de calcul.
- 352 contrôles de présence et de cohérence des figures : incidences sur les cercles, équations des droites et codages des angles droits.
- Passe éditoriale documentée pour les 210 couples énoncé/corrigé : choix de représentation et démarche de résolution indiqués dans la matrice jointe.
- 55 corrigés réécrits et 14 explications complémentaires ciblées, avec une démarche explicite dans chaque corrigé.
- 2804 contrôles supplémentaires de relecture, dont les poids des 11 arbres et les calculs de 15 tableaux de variations.
- 415 contrôles de l'édition France : 14 défis, 24 automatismes, 4 problèmes et exécution des 5 nouveaux programmes Python. Les 17 nouveaux visuels donnent 28 insertions supplémentaires.
- Modalités de l'épreuve vérifiées sur la [note de service du 11 septembre 2026](https://www.education.gouv.fr/bo/2026/Special4/MENE2622640N) (BO spécial n° 4 du 17 septembre 2026) : application en 2026-2027, baccalauréat session 2028 ; 2 heures, coefficient 2, sans calculatrice ; automatismes à réponses courtes sur 6 points, deux ou trois exercices sur 14 points, maîtrise de la langue sur 2 points. Les sujets sont des créations et leur barème détaillé est un choix pédagogique.
- Renvois et pagination stabilisés ; absence d'avertissement de débordement, de référence non résolue ou de caractère manquant.
- Rendu de toutes les pages en PNG ; comparaison au pixel à 80 dpi avec la version précédente : 32 pages identiques, 287 pages modifiées toutes relues. Absence de texte hors page. Les pages de notes lignées sont intentionnelles.
- 420 blocs de lecture vérifiés ; les 198 représentations liées aux exercices restent sur la même page que le texte correspondant.
- 54 pages de parcours avancé et de sujets contrôlées ; les 28 figures de ces pages restent avec le texte correspondant.

Les contrôles informatiques soutiennent la relecture mathématique ; ils ne constituent pas une preuve formelle automatique de tout le texte.

## Audit de conformité du 23 octobre 2026

Le détail des écarts et des corrections figure dans `corrections-audit-premiere-20261023.md` et `revision-audit-premiere-20261023.json`. La version précédente est archivée dans `output/archives/optitab-premiere-complet-avant-audit-2026-10-23.pdf`.

## Révision du 21 octobre 2026 sur l’audit fourni

Les neuf anomalies signalées ont été reproduites dans le PDF de 317 pages :
neuf blocs échouaient à l’analyse syntaxique, à cause de douze signes moins
mathématiques U+2212. Les sources Python utilisaient déjà le signe ASCII U+002D.
La correction du style supprime cette conversion lors du rendu.

Les passages concernés sont l’énoncé 12.1, les corrigés 5.12, 11.12, 11.13,
12.3, 12.11 et 12.12, et les défis D05 et D12.
Les résultats et explications de ces passages ont été revérifiés. Le corrigé
12.11 précise les conditions sur les deux listes : non vides, de même longueur,
une probabilité par valeur, probabilités positives ou nulles de somme 1.

## Reproduire les contrôles

Depuis le dossier des sources, avec LuaLaTeX et les dépendances Python SymPy, PyMuPDF et Pillow :

```powershell
python verifier_livre.py
python auditer_exercices.py
python auditer_programme.py
python verifier_figures.py
python verifier_relecture.py
python verifier_edition_france.py
python compiler.py
python controler_pdf.py
python verifier_code_pdf.py
```

Empreinte SHA-256 du PDF livré : `3040f3a2de2b82050655c6f9cb9de6a0b1814e9385259d93b3aacbec1c088448`.
