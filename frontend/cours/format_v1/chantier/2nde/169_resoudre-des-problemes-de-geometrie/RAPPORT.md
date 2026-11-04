# Notion 169 (Seconde) : Résoudre des problèmes de géométrie

**État : prêt.**

Programme de Seconde (2019), partie « Résoudre des problèmes de géométrie » : projeté orthogonal ;
problèmes sur triangles, quadrilatères, cercles ; longueurs, angles, aires, volumes ; optimisation ;
démonstrations « le projeté orthogonal est le point le plus proche » et « $\cos^2\alpha + \sin^2\alpha = 1$ ».

## Texte
- **Cours 223** : trop maigre ; il a été remis à niveau.
  - I. Projeté orthogonal : définition (cas $M \in d$ compris), théorème du point le plus proche avec une vraie
    `demonstration` complète, définition de la distance point-droite, hauteur d’un triangle, méthode « deux calculs
    d’aire » avec exemple (6-8-10, $AH = 4{,}8$).
  - II. Triangle rectangle : Pythagore et réciproque (encadré `attention` sur le plus grand côté), définitions de
    cosinus, sinus et tangente, $\cos^2 + \sin^2 = 1$ et $\tan = \sin / \cos$ démontrés, tableau des valeurs
    remarquables, méthode « longueur ou angle » (touches $\cos^{-1}$…), exemple de l’arbre, exemple de calcul d’angle.
  - III. Configurations utiles (nouveau) : cercle et triangle rectangle, médiatrice d’une corde, tableau des
    quadrilatères, Thalès, distance et milieu dans un repère ; l’exemple « coordonnées » était rangé à tort dans un
    encadré `definition` : il est devenu un `exemple`.
  - IV. Aires et volumes en tableaux, exemple du cône, unités (1 mL = 1 cm³), piège du $\frac{1}{3}$.
  - V. Optimisation (nouveau, capacité du programme absente) : méthode + exemple de l’enclos le long d’un mur
    ($\mathcal{A}(x) = 200 - 2(x - 10)^2$).
  - VI. Démarche de résolution ; `retenir` en liste (les puces « • » de la conversion sont supprimées).
- **Fiche 139** : projeté, Pythagore, trigonométrie (formules, valeurs remarquables), aires/volumes en liste,
  optimisation, 5 erreurs classiques, réflexe en `conseil`.
- **Exercices** : 18 en ligne, tous réécrits au format du pilote (méthode en une ligne, étapes titrées, calculs
  alignés, résultat, `attention` sur les erreurs fréquentes) ; `\displaystyle` retirés ; les « Question 4 (bonus) »
  mal convertis (glissés dans un encadré `resultat`) sont devenus de vraies questions.
  - **Remplacés** (même bloc, même Id) :
    - 2058 « Droites du plan - Pente, équation… » : hors sujet (c’est la notion 170) → « Application - Projeté
      orthogonal - Distance d’un point à une droite dans un repère » (mêmes points $P$, $Q$ ; alignement par
      colinéarité, réciproque de Pythagore, distance $2\sqrt{5}$, cohérence $MQ \gt MH$, aire $15$).
    - 2071 « Al-Kashi » : **hors programme** (Première) → « Problème - Triangle quelconque - Une longueur et une aire
      grâce à une hauteur » : mêmes données ($7$, $9$, $60°$), on trace la hauteur $[BH]$ et on retrouve
      $BC = \sqrt{67}$ par trigonométrie et Pythagore, puis l’aire et la distance de $A$ à $(BC)$.
  - **Questions corrigées ou remplacées** :
    - 2060 Q5 « équation du cercle » : hors programme → « $ACBD$ est un rectangle, aire $12$ ».
    - 2059 Q5 « équation de la diagonale » (hors notion) → rayon du cercle circonscrit $\frac{\sqrt{34}}{2}$ ; Q2 conclut au losange.
    - 2056 Q3 circulaire (vérifier le parallélogramme qui venait d’être construit) → « est-ce un losange ? » ; Q5 :
      hauteur justifiée par le projeté $E(-1\,;1)$.
    - 2055 Q4 circulaire → « $OACB$ est un parallélogramme ».
    - 2072 Q2 : la justification « théorème de Thalès » (appellation non française) est remplacée par une preuve
      complète (symétrique $D$, rectangle $ABDC$, diagonales égales).
    - 2069 : la forme canonique « à trouver » est remplacée par « démontrer que $\mathcal{A}(x) = 100 - (x - 10)^2$ ».
    - 2063 : Q4 ajoutée (calcul d’un angle, $\approx 76°$) ; 2064 : Q5 ajoutée ($\alpha \approx 36{,}9°$) ;
      2068 : nombre de cônes et conversion en litres ; 2070 : 6e affirmation (5-12-13), structure en questions.
  - **Ajouts** :
    - `nouveau-1` « Entraînement - Volumes - Pyramide régulière à base carrée » (volumes et Pythagore dans un solide :
      $SO = 3\sqrt{7}$, $V = 36\sqrt{7} \approx 95$ mL) ;
    - `nouveau-2` « Problème - Optimisation - Carré inscrit dans un carré » (minimum $50$ cm² en $x = 5$, deux
      méthodes, équation $f(x) = 58$).
  - Aucune erreur de calcul dans les résultats en ligne ; seules erreurs de fond : contenus hors programme ci-dessus.
- `verif_169.py` : 152 contrôles (sympy), tous OK : chaque longueur, aire, volume, angle et arrondi écrit.

## Figures
- **25 figures neuves** (figures.py, style des livres), servant 29 positions. Les 20 images en ligne ont toutes été
  refaites : les 14 d’exercices étaient au style matplotlib (couleurs criardes, texte minuscule, grands vides,
  repère −10…10), celles du cours/fiche étaient d’un autre style (bleu vif, rouge) et trop larges (1 020 à 1 320 px).
  - Cours (5) : projeté, triangle rectangle et trigonométrie, arbre, solides, **enclos (ajoutée)**.
    La fiche réutilise trigonométrie et solides, et **ajoute** le projeté (position 3).
  - Exercices : 14 refaites ; ajoutées : 2058 (figure d’énoncé + figure de corrigé), 2064, 2068, 2062,
    nouveau-1, nouveau-2.
- 0 image conservée, 0 retirée. Toutes ≤ 900 px, aucun chevauchement texte/trait (les seuls avertissements du
  compilateur concernent des cotes à fond blanc) ; chaque PNG regardé. Graduations choisies pour qu’aucune ne soit
  coupée par un tracé (d’où certains axes peu gradués : la grille reste à l’unité).

## Contrôles
- `verifier_notion.py --navigateur` : OK, 0 problème (relancé après les dernières retouches).
- `controle_apercu.mjs` : 124 vues (téléphone et ordinateur), aucun débordement, aucune erreur de formule, aucun `$`
  brut, aucune image manquante. Dossier `captures/` laissé en place.
- Vues regardées sur téléphone : le cours en entier (5 captures), la fiche, les exercices 2058 (énoncé et étapes)
  et nouveau-2 (étapes). Corrections faites après ces captures :
  - formules qui défilaient coupées : exemple « deux calculs d’aire », trois carrés de longueurs (cours III),
    $MQ^2$ (2058 Q5), comparaison en ligne de nouveau-2 Q3 → passées en `aligned` ou sur deux lignes ; la même
    règle appliquée par précaution aux calculs longs de 2058, 2069, 2056, 2060, 2059 et nouveau-2 ;
  - cosinus et sinus de la définition sur deux lignes (ils étaient réduits) ; milieu en formule centrée ;
  - fractions empilées qui se chevauchaient dans le `retenir` du cours et la liste des aires de la fiche
    (`\dfrac` en ligne) : `\frac` dans le `retenir`, tableaux dans la fiche ;
  - figure des solides refaite en 2 × 2 (trop petite sur téléphone en une rangée) ;
  - « ; » rejeté en début de ligne dans l’exemple de l’arbre : phrase reformulée.

## Remarques pour l’orchestrateur
- Les titres de type « Application », « Approfondissement », « Bonus », « Maîtrise » ont été gardés (types existants).
- `lseg` (étiquette de segment) utilise une ancre « boussole » : avec une ancre numérique, une étiquette large posée
  contre un segment oblique le chevauchait sans que le contrôle automatique le signale toujours (vu à l’œil sur
  2065, 2067, 2071).

## Vérification des figures 2026-11-02

- **25 figures vues** (28 appels : 5 du cours, 3 de la fiche — reprises du cours —, 20 des exercices), à l'œil et avec le détecteur texte/trait de `figures_livre.py` : 25/25 acceptées ; les seules alertes portent sur des cotes ou longueurs sur fond blanc (arbre, ex_triangle_amb, ex_triangle_ch, ex_thales, ex_triangle_60, ex_pyramide), usage normal d'une cote.
- La session interrompue avait refait 9 figures (solides, ex_carre_acbd, ex_carre_repere, ex_cercle_diametre, ex_parallelogramme, ex_projete_enonce, ex_projete_corrige, ex_symetries, ex_thales) : toutes revérifiées.
- Contrôles mathématiques (coordonnées relues contre les énoncés ; proportions mesurées sur les images) : D(−1 ; 5), M(1 ; 3) (2057) ; H(2 ; 2) sur (PQ) (2058) ; sommet (10 ; 100) (2069) ; C(3 ; 4), K(0,5 ; 2,5), E(−1 ; 1), hauteur 3 (2056) ; E(1 ; 5) intérieur au cercle (MA = √10) (2060) ; 6 et 8 cm (2072) ; AH = 25/13 (2061) ; angle 35° (atan(397/567) ≈ 35,0°) ; CH = 12 (2065) ; OH = 3, AH = 4 (2066) ; AD = 8, AC = 18, BC = 15, DE ∥ BC (2067) ; 9 / 12 / 15 (2064) ; r/h = 6/15 (2068) ; 60° (≈ 59,9°), AH = 3,5 (2071) ; K(2,5 ; 3,5) (2059) ; x reporté 4 fois (3751).
- **Défaut trouvé (1)** : `ex_symetries` (corrigé 2055) — le codage « AB = BA′ » n'était visible que sur [BA′] : la marque du milieu de [AB] tombait sous le point M. **Refaite** : AM = MB et les deux moitiés de [BA′] portent le même trait simple (B milieu de [AA′], M milieu de [AB]) ; codage double inchangé pour OM = MC. Recompilée, détecteur sans alerte.
- Contrôles finaux : `verifier_notion.py --navigateur` sur copie de travail (Id 3750 et 3751, créés à l'import du 29/10, ajoutés à son `meta.json`) : toutes les vues propres, mais Chrome bloqué à la fermeture → relancé sans navigateur : **OK, 0 problème** ; puis `controle_apercu.mjs` avec délai maximal : **124 vues, 0 défaut** (seul mon processus bloqué a été arrêté). Captures téléphone de 2055, 2057 et 2058 regardées : figures lisibles, sans débordement.

## Finition 2026-11-02

**État : prêt** (agent-finition-S2). 20 exercices (pas d'ajout nécessaire).

### Exercice réécrit
- 2070 « Entraînement - Vrai ou faux sur les pièges classiques » : il n'avait ni méthode ni étapes détaillées, et l'affirmation 4 était vague (« on peut donner à x n'importe quelle valeur »). Réécrit dans son bloc (même Id) : méthode, étape, résultat et erreur fréquente pour chaque affirmation ; affirmations chiffrées (cos α = 0,2 au lieu de 0,6 ; x = 25 pour un rectangle de périmètre 40 cm ; cône de volume 12π et non 36π cm³). Calculs ajoutés dans `verif_169.py`.

### Figures (18 ajoutées + 2 figures du cours réutilisées, aucune refaite ni retirée)
- **Énoncés (9, données seules)** : 2057, 2069 (rectangle de périmètre 40 cm), 2056, 2060 (points sans le cercle), 2072, 2055, 2066, 2064, 2059.
- **Corrigés (9, réponse en vert)** : 2061 (MH = 60/13), 2063 (h = 4 m, d ≈ 6,93 m), 2065 (CH = 12, HB = 5, BC = 13), 2067 (AE = 12, DE = 10), 2068 (volumes 540π et 180π cm³), 2071 (AH, HC, BH, BC = √67), 2062 (MP² = MH² + HP²), 3750 (triangle SOA, SO = 3√7), 3751 (cas x = 5, aire minimale 50 cm²).
- 2070 (qui n'avait aucune figure) : figures du cours `projete.png` (Q1) et `trigo.png` (Q2) dans le corrigé.
- Chaque exercice a maintenant une figure d'énoncé et une figure de corrigé, sauf les exercices sans donnée géométrique à montrer dans l'énoncé (2070, 2058 en avait déjà deux). Détecteur texte/trait : 18/18 sans erreur après correction (étiquettes de BC, SO et des sommets du carré déplacées) ; seuls avertissements = cotes à fond blanc ; chaque PNG regardé.

### Titres
- 19 titres au format « Type - Sujet » (le sujet intermédiaire répété est retiré). Les types hors liste ont été remplacés : « Application » → Entraînement ; « Approfondissement », « Bonus » → Problème ; « Maîtrise » → Entraînement. Le titre de 2059 était déjà correct. Cours et fiche : intitulé officiel déjà en place.

### Contrôles
- `verif_169.py` : 157 contrôles OK.
- `verifier_notion.py --navigateur` : les 124 vues Chrome (téléphone et ordinateur) n'ont aucun débordement, aucune erreur de formule, aucun `$` brut et aucune image manquante. Chrome est resté bloqué à la fermeture : j'ai arrêté mon seul processus node et retiré mon verrou abandonné. Ensuite, `verifier_notion.py` sans navigateur donne **OK, 0 problème**, et `controle_apercu.mjs` avec captures et délai donne de nouveau 124 vues sans problème.
- Capture téléphone de 2070 regardée : la double formule sinus/cosinus était réduite, elle est maintenant sur deux lignes.
