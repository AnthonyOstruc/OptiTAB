# Livre OptiTAB - Première générale, spécialité mathématiques

Livre complet : cours, méthodes, démonstrations, 224 exercices originaux corrigés (210 dans les chapitres et 14 défis), deux sujets blancs et figures vectorielles, dans la charte du livre `../livre` de Terminale.

L'édition France 2026-2027 ajoute un parcours facultatif de recherche, des indications progressives séparées et deux sujets blancs originaux de deux heures sans calculatrice. Chaque sujet suit la note de service du 11 septembre 2026 (NOR MENE2622640N, BO spécial n° 4 du 17 septembre 2026), applicable en 2026-2027 pour le baccalauréat session 2028 : une première partie de 12 automatismes à réponses courtes (6 points), choisis dans la rubrique « Automatismes » du programme de Première et dans celle de Seconde, avec des lectures graphiques ; une deuxième partie de deux exercices indépendants (14 points). Le barème détaillé (7 points par exercice, dont 1 point de maîtrise de la langue) est présenté comme un choix pédagogique.

**Édition du 23 octobre 2026 — audit de conformité.** Un audit indépendant du livre a été mené sur le programme (BO n° 14 du 2 avril 2026) et sur la définition de l'épreuve anticipée. Il a conduit à réécrire les 24 automatismes des sujets blancs, à compléter le guide de l'épreuve (coefficient, oral de contrôle, grille de maîtrise de la langue), à ajouter ou corriger trois exemples d'algorithmes du programme (pentes des sécantes en 3.6, Archimède sans `math.pi` en 6.15, Newton relié à la tangente en 12.14), à préciser six points de cours et à harmoniser la typographie des apostrophes. Le détail est dans `revision-audit-20261023.json` et dans `../output/verification/corrections-audit-premiere-20261023.md`. La version précédente du PDF est archivée dans `../output/archives/optitab-premiere-complet-avant-audit-2026-10-23.pdf`.

Le PDF final de cette édition est `../output/pdf/France/Mathématiques/OptiTAB - Mathématiques - Première spécialité - Manuel complet.pdf`. Les fichiers `edition_france_*.py` contiennent les textes et les figures des compléments ; `python enrichir_edition_france.py` les régénère, sans réécrire les 210 exercices de chapitre. Le style est dans `edition-france.sty` et le manifeste dans `edition-france-manifeste.json`.

## Contenu

1. Polynômes du second degré
2. Suites numériques
3. Dérivation
4. Variations et optimisation
5. Fonction exponentielle
6. Trigonométrie
7. Vecteurs et produit scalaire
8. Géométrie repérée
9. Probabilités conditionnelles et indépendance
10. Variables aléatoires
11. Statistiques et simulations
12. Algorithmique et programmation
13. Ensembles et raisonnement
14. Automatismes et synthèses

Chaque chapitre comporte une ouverture, une synthèse de cours, cinq exercices de découverte, six d'entraînement et quatre problèmes. Couvertures, page de titre, mentions d'édition, avant-propos, mode d'emploi, parcours de travail, sommaire, tableau de bord et références sont inclus. Les annexes rassemblent des démonstrations et des repères du programme.

Le programme de référence est celui de Première générale spécialité, BO du 2 avril 2026, applicable depuis la rentrée 2026-2027. Les liens officiels figurent dans `liminaires/references.tex`.

La révision du 21 octobre 2026 traite les neuf anomalies de copie du code relevées
dans l’audit fourni. Le style conserve le moins ASCII dans les blocs Python et
les affichages. Le corrigé 12.11 précise aussi les conditions sur les listes.
Les changements sont tracés dans revision-audit-20261021.json.

## Compiler

Depuis ce dossier :

La commande `python compiler.py` effectue les passes nécessaires jusqu'à stabilisation des renvois et contrôle les principaux avertissements typographiques.

On peut aussi utiliser directement :

```powershell
New-Item -ItemType Directory -Force build | Out-Null
lualatex -interaction=nonstopmode -halt-on-error -aux-directory=build main.tex
lualatex -interaction=nonstopmode -halt-on-error -aux-directory=build main.tex
lualatex -interaction=nonstopmode -halt-on-error -aux-directory=build main.tex
```

Trois passes stabilisent les sommaires et les renvois. Le PDF de lecture est `main.pdf`. Une copie de livraison est dans `../output/pdf/France/Mathématiques/OptiTAB - Mathématiques - Première spécialité - Manuel complet.pdf`.

Les sources sont autonomes : `optitab-livre.sty`, `figures-geometrie.sty`, `figures/`, `images/`, `chapitres/`, `corriges/`, `liminaires/`, `annexes/` et `couverture/`. Le livre de Terminale n'est pas modifié.

Les 30 exercices des chapitres 7 et 8 possèdent chacun une figure vectorielle dans l'énoncé et une version accompagnant le corrigé. Les constructions et les indications de solution sont ajoutées en vert. Six exercices de trigonométrie sont aussi illustrés, ainsi que les configurations de cours et les démonstrations géométriques.

La passe éditoriale complète est documentée dans `revision-editoriale.json` : les 210 couples énoncé/corrigé y sont recensés avec la démarche de résolution et le choix des représentations. Elle ajoute notamment les arbres de probabilités, les tableaux d'issues et de lois, les tracés statistiques, les tableaux de signes et de variations et les tables de trace utiles. Les simples calculs et preuves gardent une rédaction épurée lorsque le dessin n'ajoute rien à la résolution.

Les blocs `blocLivre` gardent chaque énoncé ou corrigé avec ses représentations. Leur hauteur est contrôlée lors de la compilation. Le style complémentaire est dans `relecture-livre.sty` et les nouveaux visuels dans `figures/r*.tex`.

## Vérifications

`python verifier_livre.py` contrôle les comptes d'exercices, la correspondance des corrigés et les calculs structurants avec SymPy.

`python auditer_exercices.py` effectue des contrôles de résultats pour chacun des 210 exercices des chapitres, exécute leurs blocs Python et vérifie les principales fonctions sur des cas usuels ou limites. Les rapports décrivent les contrôles et leur portée ; ils ne constituent pas une preuve formelle automatique de tout le texte.

`python auditer_programme.py` contrôle les références de 60 groupes de contenus, capacités, démonstrations et exemples d'algorithmes, et génère la matrice de couverture dans `annexes/couverture-programme.tex`.

`python controler_pdf.py` vérifie les renvois, les signets, les liens et les limites des pages, puis rend toutes les pages dans `build/qa/` pour la relecture visuelle (PyMuPDF et Pillow).

`python verifier_figures.py` vérifie la présence des figures dans tous les exercices de géométrie, la version des corrigés, les équations des droites, les points sur les cercles et la cohérence des codages d'angles droits.

`python verifier_relecture.py` vérifie la matrice des 210 exercices, les textes relus, les représentations requises, les feuilles des arbres et les valeurs et signes des tableaux de variations. Cette passe est intégrée au PDF livré `../output/pdf/France/Mathématiques/OptiTAB - Mathématiques - Première spécialité - Manuel complet.pdf`.

`python verifier_edition_france.py` vérifie les 14 défis, les 24 automatismes et les quatre problèmes des sujets, y compris les paramètres frontières, les probabilités des chemins, les projections et les cinq nouveaux programmes Python. Il vérifie la conservation des énoncés et corrigés de la base relue, avec la révision pédagogique 12.11 explicitement tracée.

python verifier_code_pdf.py extrait les 28 programmes du PDF compilé, reconstruit
leur indentation à partir des positions des glyphes et vérifie leur syntaxe sans
remplacer les caractères. Il compare leur structure syntaxique aux sources,
les exécute, puis teste les fonctions concernées par l’audit. Cette vérification
complète les contrôles des sources ; elle ne certifie pas le comportement de
copie de tous les logiciels de lecture PDF.
