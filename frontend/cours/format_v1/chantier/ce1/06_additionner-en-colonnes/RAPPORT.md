# Rapport — Additionner en colonnes

État : **prêt**. Contrôles locaux terminés, aucun point en suspens.

Neuf sources sur neuf conservées et développées en `nouveau-1` à `nouveau-9`, cinq vraies questions par exercice : **45 questions**, chacune avec méthode calculatoire, raisonnement détaillé, résultat encadré et solution strictement identique. Cours et fiche entièrement réécrits en format v1. Correspondance des compétences : [COUVERTURE.md](COUVERTURE.md).

Chiffres alignés par rang, retenues expliquées comme échanges ; les additions à trois termes et l’arrivée à mille sont conservées. Espace insécable dans 1 000.

Les nombres et résultats restent au plus égaux à 1 000. Les multiplications utilisent le sens, les tables, les doubles et la décomposition ; les partages utilisent le sens et les produits. Aucune multiplication ni division posée introduite. Les conseils s’adressent à l’enfant.

Figures : **10 ajoutées**, 0 ancienne conservée, 0 retirée. TikZ et palette officielle du livre, colonnes pour les opérations posées, résultat en vert ; correspondances `cours:nouveau`, `fiches:nouvelle`, `exercices:nouveau-N`. Compilation séquentielle officielle `--jobs 1`, retour 0 conservé dans `compilation_figures.log`. Chaque PNG a été regardé individuellement : chiffres alignés, étiquettes lisibles et aucun chevauchement.

Contrôles effectués :

- `verif_math.py` autonome : **188 égalités recalculées dans les vrais fichiers finaux**, doubles et moitiés contrôlés, calculs à trou résolus depuis les questions finales, présence des calculs numériques sources, neuf blocs et 45 questions vérifiés, solutions identiques aux résultats.
- Validation officielle adaptée aux créations CE1 : **0 problème**, empreintes des sources intactes (`validation_ce1.json` et journal).
- Chrome : **58 vues distinctes**, mobile et ordinateur, **0 anomalie** ; aucun débordement, image cassée ou erreur MathJax (`audit_navigateur_ce1.json`).
- Relecture personnelle du cours mobile entier, de la fiche et des exercices 1,5,9 : énoncé et toutes les étapes. 9 captures conservées, trois planches de relecture lues. Les retouches de typographie et de cohérence texte/schéma ont été revalidées et relues.

Les preuves réelles et empreintes des fichiers finaux sont conservées dans `PREUVES_FINALES.json`. Programme de référence : programme officiel du cycle 2 applicable depuis 2025, périmètre vérifié par l’orchestrateur. Aucune source modifiée, aucune commande `manage.py`, aucun accès en base ni import effectué.

## Publication CE1 vérifiée

Cours, fiche, exercices et images importés et relus. Accès local et public contrôlés. Sauvegardes et sources d’origine conservées.
