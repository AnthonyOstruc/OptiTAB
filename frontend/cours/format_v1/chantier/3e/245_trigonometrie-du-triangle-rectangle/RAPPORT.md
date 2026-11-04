# Notion 245 (3e) : Trigonométrie du triangle rectangle

**État : prêt** (claude-245, 2026-11-03).

Programme du cycle 4 : hypoténuse, côté adjacent et côté opposé à un angle aigu ; cosinus, sinus, tangente ; calcul d'une longueur ou d'un angle (calculatrice en mode degrés, arrondis) ; problèmes concrets (échelle, rampe, angle d'élévation, pente) ; enchaînements de type brevet avec Pythagore et Thalès. Hors programme non abordé : $\cos^2 + \sin^2 = 1$, radians (le mode radians n'apparaît que comme erreur de calculatrice à repérer).

## Texte
- **Titres** : cours « Trigonométrie du triangle rectangle », fiche « Résumé : Trigonométrie du triangle rectangle » (inchangés, conformes à la notion).
- **Cours 240** : réécrit façon manuel. Objectifs et prérequis ; I. Vocabulaire (définition, exemple, l'échange adjacent/opposé quand on change d'angle, 2 figures) ; II. Cosinus, sinus, tangente (définition, exemple, CAH SOH TOA, propriétés : entre 0 et 1, angles complémentaires ; mode degrés) ; III. Calculer une longueur (méthode en 4 étapes, inconnue au numérateur / au dénominateur rédigées en `aligned`, erreurs fréquentes) ; IV. Calculer un angle (touches $\cos^{-1}$…, arrondis) ; V. Problèmes concrets (angle d'élévation, hauteur d'un arbre avec figure, hauteur des yeux, pente en %) ; À retenir. L'ancien exemple rangé dans un encadré `definition` et le tableau à trois colonnes (coupé sur téléphone) sont supprimés ; les trois formules sont sur trois lignes.
- **Fiche 160** : réécrite (côtés, CAH SOH TOA, tableau « on connaît → rapport », longueur, angle, problèmes concrets, 5 erreurs classiques).
- **Exercices** : les **21 réécrits entièrement** (méthode, étapes détaillées, résultat encadré, erreur fréquente ou à retenir, solution courte), titres « Type - Sujet » sans le nom du chapitre. Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 Type brevet. Les anciens corrigés n'avaient souvent qu'un résultat sans étape (« Cohérent », « Opposé ») et aucun ne travaillait les arrondis ni l'inconnue au dénominateur de façon guidée.
  - **Remplacés / refondus (même Id)** :
    - 2386 « Choisir le bon rapport » : un même triangle, trois cas (sinus, tangente, cosinus avec inconnue au dénominateur) ;
    - 2388 « Changer d'angle » → « Travailler avec l'autre angle aigu » (le côté $[AB]$ devient opposé ; vérification par l'angle complémentaire) ;
    - 2389 « Un câble » → « Une échelle contre un mur » (consigne : échelle ; condition de sécurité 65°–75°) ;
    - 2390 « Diagnostiquer une erreur » → « Trouver et corriger les erreurs » (confusion adjacent/opposé + calculatrice en radians, résultat négatif) ;
    - 2391 rampe (tangente, cosinus, confort ≤ 3°) ; 2396 rivière (tangente + cosinus + contrôle par Pythagore) ; 2398 phare (angle de dépression, angles alternes-internes) ;
    - 2399 « Le panneau de pente » → **Type brevet** « La pente d'une route » (pourcentage, Pythagore, $\tan^{-1}(0{,}1)$, retour par le cosinus) ;
    - 2400 « L'échelle de pompier » (doublon de l'échelle) → **Type brevet** « Pythagore, trigonométrie et Thalès » (triangle 6-8-10, angle, parallèles, Thalès, contrôle par la tangente).
  - Valeurs toutes recalculées ; aucune erreur de calcul trouvée dans les résultats en ligne, mais plusieurs corrigés étaient incomplets.
- `verif_245.py` : **83 contrôles sympy OK** (chaque longueur, angle, arrondi, contrôle de Pythagore, valeurs d'erreurs citées : $8\sin(40\ \text{rad})$, $6/\cos(40\ \text{rad})$…).

## Figures
- **44 figures neuves** (style livre, `figures/figures.py`) pour **47 positions** ; les 8 images en ligne (matplotlib) sont toutes remplacées ; 0 conservée.
  - Cours (3) : vocabulaire pour $\widehat{ABC}$, pour $\widehat{ACB}$ (côtés nommés en vert), observateur et arbre (angle d'élévation). Fiche (1) : vocabulaire.
  - Exercices : figure d'énoncé (données seules, angle droit codé, angle marqué) **et** figure de corrigé (hypoténuse / côté adjacent / côté opposé nommés en vert, côtés utilisés tracés en vert, résultat en vert) pour les **21** exercices ; 2380 a deux figures de corrigé (un angle puis l'autre).
  - Schémas concrets sobres : échelle et mur, rampe et entrée, cerf-volant, toboggan, immeuble, toit sur façade, rivière, avion, phare et bateau, route. Les angles trop petits pour être lisibles (3°, 8°, 12°, pente de 10 %) sont agrandis ; l'énoncé le signale (« schéma pas à l'échelle »).
- Détecteur texte/trait : 0 erreur ; seules alertes : cotes à fond blanc (2395, 2400). Toutes ≤ 900 px. Chaque PNG regardé (planches).

## Contrôles
- `verif_245.py` : 83 contrôles sympy OK.
- `verifier_notion.py` : **OK, 0 problème** (47 positions de figures, 0 image en ligne conservée).
- `--navigateur` / `controle_apercu.mjs` avec captures : **130 vues sur 130 sans défaut** (0 débordement, 0 erreur de formule, 0 image manquante, 0 élément trop large), téléphone et ordinateur. Chrome est resté bloqué à la fermeture (cas connu) : seuls mes processus (node 19568, puis 17324) ont été arrêtés, après la dernière vue.
- Vues regardées sur téléphone : cours (I à V), fiche, exercices 2380, 2389, 2394, 2398, 2400 (étapes). Corrections faites après ces vues : ligne de Thalès de 2400 réduite → deux formules centrées ; « m » rejeté seul en début de ligne (exemple de l'arbre du cours, 2398) → phrases reformulées. Les trois formules CAH SOH TOA sont sur trois lignes (cours et fiche).

## Remarques pour l'orchestrateur
- Le dossier temporaire (scratchpad) de cette session est **partagé** avec un autre agent (notion 247 : il y a écrit `ex1.txt`… sous les mêmes noms que moi). Mes fichiers de notion n'ont pas été touchés (vérifié), mais il faut prévoir des noms uniques par agent.
