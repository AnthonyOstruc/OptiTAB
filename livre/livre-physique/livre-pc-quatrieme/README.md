# Physique-chimie - Quatrième

Manuel complet OptiTAB, France, édition 2026-2027. La charte est celle du livre de Terminale : Libertinus pour le texte et les mathématiques, Montserrat pour les titres, ouvertures bleues, méthodes vertes et figures vectorielles.

**Révision du 24 octobre 2026 : 289 pages.** Les 1 419 contrôles ont réussi, dont 209 calculs enregistrés. Les 289 pages ont été relues en planches, puis 21 pages critiques contrôlées avec Poppler. Les longueurs demandées à l’échelle ont aussi été mesurées dans le PDF. Le PDF final et sa copie sur le Bureau sont identiques au fichier validé.

## Contenu

- 20 chapitres dans les quatre thèmes du cycle 4.
- 4 sections de cours, un exemple résolu, une investigation corrigée et une synthèse par chapitre.
- 300 exercices corrigés : 600 questions, réparties en trois niveaux.
- 20 défis corrigés, 209 figures vectorielles originales : 40 dans les cours et 169 pour les exercices, défis, bilans et évaluations.
- 54 énoncés et 111 corrigés d’exercices ou défis illustrés ; 71 démarches supplémentaires, ainsi que trois explications ajoutées aux bilans et évaluations.
- 4 bilans de thème et 2 évaluations de synthèse, tous corrigés avec barèmes sur 20.
- Diagnostic, fiches méthodes, conversions, répertoire d'éléments, lexique et concordance du programme.

Les réponses aux investigations, les conditions des calculs et les limites des modèles sont explicitées. Les expériences sont destinées à un travail en classe sous conduite de l'enseignant.

La révision a porté sur les 300 exercices, les 20 défis et les six bilans et évaluations. Les illustrations accompagnent les lectures de graphiques, constructions de forces, connexions électriques, inventaires moléculaires et trajets de signaux qui en ont besoin. Les modèles et données ajoutés à titre illustratif sont annoncés. Les dessins à mesurer portent la mention « impression à 100 % » ; les frises réduites sont signalées. L’édition de 236 pages est conservée dans `output/archives/physique-chimie-quatrieme-avant-illustrations-exercices-20261024.pdf`.

## Recherche et périmètre

Les pages Éduscol consultées le **24 octobre 2026** confirment le programme de physique-chimie du cycle 4 publié au BO du 30 juillet 2020 pour l'année 2026-2027. Le programme permet différentes progressions annuelles : le découpage de Quatrième est un choix pédagogique, clairement annoncé dans le livre. Le projet de programme du CSP ne se substitue pas au programme en vigueur.

Le manuel approfondit les modèles particulaires, les atomes et molécules, les transformations, les forces et les lois de l'électricité. Les relations énergétiques de fin de cycle sont signalées comme approfondissements ; la structure interne de l'atome, les calculs ioniques détaillés et la loi de gravitation formelle sont réservés à la suite du cycle.

Sources primaires : Éduscol et Bulletin officiel, BIPM, IUPAC, Agence spatiale canadienne, INRS et Santé publique France. Les liens et la concordance figurent en fin de manuel. Les PDF officiels conservés dans `recherche/` proviennent de l'archive documentaire du manuel de Cinquième, après vérification de leur référence sur les pages officielles actuelles ; le serveur de téléchargement Éduscol a refusé le nouveau téléchargement direct.

Cours, exercices et schémas sont des créations éditoriales originales. Le manuel est indépendant du ministère. Aucun exercice n'est faussement présenté comme un sujet officiel ; aucun ISBN ni agrément n'est inventé.

## Construction

Depuis la racine du projet :

```powershell
python livre-pc-quatrieme/figures.py
python livre-pc-quatrieme/figures_revision.py
python livre-pc-quatrieme/auditer_revision.py
python livre-pc-quatrieme/construire.py
python livre-pc-quatrieme/compiler.py
python livre-pc-quatrieme/verifier.py
python livre-pc-quatrieme/preuves_revision.py
```

Les dépendances sont Python avec NumPy, Matplotlib, PyMuPDF et Pillow ; LuaLaTeX avec les polices et paquets de la charte ; Poppler pour la seconde lecture du rendu. Le texte n'est pas transformé en image ni réduit pour faire entrer une page. Les figures sont ajustées proportionnellement.

## Vérification et livraison

`verifier.py` contrôle structure, réponses, calculs enregistrés, bilans atomiques, concordance, caractères, débordements, renvois, liens, format et métadonnées. Il vérifie aussi l’intégration des nouvelles figures, les trajets aller-retour, les fréquences et les bilans énergétiques. Il rend toutes les pages en PNG et produit les planches dans `tmp/pdfs/qa-pc-quatrieme-revision/`. `preuves_revision.py` mesure les longueurs imprimées et crée les preuves Poppler. Les contrôles numériques ciblés complètent la relecture scientifique ; ils ne remplacent pas l'examen des raisonnements.

Après relecture des planches et des pages critiques rendues avec Poppler, `build/validation-visuelle.json` enregistre l'empreinte du PDF validé. `livrer.py` exige une empreinte identique et des contrôles réussis avant copie dans `output/pdf/France/Physique-chimie/` et dans la bibliothèque du Bureau. Le rapport final est dans `output/verification/physique-chimie-quatrieme-livraison.json`.

```powershell
python livre-pc-quatrieme/livrer.py
python outils/organiser_pdf.py
```
