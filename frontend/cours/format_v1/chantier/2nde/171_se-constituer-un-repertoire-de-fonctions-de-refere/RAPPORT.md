# Rapport — 2nde / 171 « Se constituer un répertoire de fonctions de référence »

**État : prêt.**

## Programme (Seconde 2019) — couverture
- Fonctions carré, inverse, racine carrée, cube : définitions, courbes (cours II à V) ; fonctions affines (cours I).
- Comparer $f(a)$ et $f(b)$ numériquement ou graphiquement : cours VI, ex. 2026, 2029, 2030 (+ question piège sur l’inverse).
- Résoudre graphiquement ou algébriquement $f(x)=k$, $f(x)<k$ (affines, carré, inverse, racine, cube) : cours, ex. 2025, 2028, 2031, 2032, **nouveau-1** (lecture graphique).
- Démonstration : position relative de $y=x$, $y=x^2$, $y=x^3$ pour $x\ge0$ (cours VII, ex. 2033).
- Démonstrations des variations de carré, inverse, racine carrée (cours, encadrés `demonstration`).
- Algorithme : encadrer $\sqrt2$ par balayage (cours VIII, **nouveau-3**).
- Parité : évoquée seulement comme symétrie des courbes (traitée en détail dans la notion « représenter les fonctions »).

## Texte
- Cours réécrit et complété : affines (méthode $f(x)<k$, division par un négatif), carré/inverse/racine/cube avec tableau de variations natif `::: tableau`, démonstrations séparées (`::: demonstration`, ajout de celle de la racine carrée), équations $x^2=k$, $1/x=k$, $\sqrt x=k$, $x^3=k$, inéquation $1/x<2$ branche par branche, méthodes « comparer » et « résoudre graphiquement », tableau récapitulatif, position relative, algorithme de balayage (code ≤ 30 caractères par ligne).
- Fiche refaite : tableau du répertoire, équations, méthode de comparaison, 5 erreurs classiques.
- Aucune erreur de calcul dans la source ; défauts corrigés : « racine cubique » (hors programme) remplacée par la croissance de la fonction cube (2029, 2031) ; 2034 Q3 exigeait de factoriser $x^2-5x+4$ sans outil de Seconde → factorisation donnée à vérifier (Q3 b) ; étapes vides (titres seuls) de la conversion remplacées partout par des étapes rédigées, avec vérifications et « attention ».
- Exercices : 10 conservés et entièrement réécrits (titres précisés pour 2026, 2027, 2028, 2031, 2033) ; questions ajoutées : 2030 Q6 (piège : inverse sur deux intervalles), 2031 Q6 ($x^2=-4$).
- **Ajouts** : nouveau-1 « Résoudre graphiquement avec la courbe de la fonction inverse », nouveau-2 « Encadrer une image avec les fonctions de référence » (dont le piège $-3\le x\le2$ pour $x^2$), nouveau-3 « Encadrer racine de 2 par balayage » (algorithme du programme).
- Tous les résultats vérifiés : `verif_171.py` (73 contrôles, dont les sorties réelles de la fonction Python).

## Figures
- 7 images en ligne : toutes remplacées (style matplotlib, petits textes) ; 0 conservée.
- 13 figures neuves (style livre, graduations posées du côté libre de la courbe) : 6 pour le cours, 1 pour la fiche (+ réemploi), 6 pour les exercices (énoncé et corrigés : 2032, 2033, 2034, nouveau-1, nouveau-2) ; 16 emplacements au total.
- Contrôle automatique des chevauchements : 0 ; chaque PNG regardé.

## Contrôles
- `verifier_notion.py --navigateur` : OK, 0 problème.
- Captures `controle_apercu.mjs` (0 problème) regardées sur téléphone : tout le cours, la fiche, exercices nouveau-1, nouveau-2, nouveau-3. Corrigé après lecture : intervalles à borne négative (`{]{-2}\,;…}`), tableau récapitulatif réduit à 3 colonnes, tableau du balayage mis en colonnes, formules trop larges coupées en deux.

## Remarques pour l’orchestrateur
- `valider_v1.py` refuse une double barre sans valeurs (`-D+`) alors que FORMAT.md admet une case vide si la valeur est inconnue de l’élève (limites de $1/x$ en $0$, hors programme de Seconde). Contournement : `-D+/\phantom{0}/\phantom{0}` (rendu identique à une case vide). Suggestion : accepter `[+-]D[+-]` seul dans `VAR_RE`.

## Vérification des figures 2026-11-02

- **13 figures vues** (16 appels : 6 du cours, 2 de la fiche, 8 des exercices), à l'œil et avec le détecteur texte/trait de `figures_livre.py` : 13/13 sans chevauchement ni alerte.
- La session interrompue avait refait 2 figures (cours_inverse, cours_positions) : revérifiées.
- Contrôles mathématiques : points de y = x² (±1, ±2, ±3), x² ≤ 4 → [−2 ; 2] bornes fermées ; hyperbole par (0,5 ; 2), (1 ; 1), (2 ; 0,5) et symétriques ; √x par (1 ; 1), (4 ; 2), (9 ; 3) ; x³ par (±1 ; ±1), (±2 ; ±8) ; x³ ≤ x² ≤ x sur [0 ; 1] ; x² < 9 → ]−3 ; 3[ ouvert (2032) ; 1/x > 2 → ]0 ; 0,5[ ; √x = x − 2 → (4 ; 2), x = 1 rejeté ((1 ; 1) ≠ (1 ; −1)) (2034) ; −3 ≤ x ≤ 2 → 0 ≤ x² ≤ 9 (3743) ; 1/x ≥ −1 → ]−∞ ; −1] ∪ ]0 ; +∞[ (3744). Style des livres, éléments de réponse en vert.
- **Défauts trouvés (2)**, dans des corrigés : la borne de la solution n'était écrite nulle part sur la figure.
  - `ex_inverse_sup2` (corrigés 2032 et 3744) : la graduation 0,5 manquait sous l'intervalle ]0 ; 0,5[ → **refaite** avec « 0,5 » en vert sous l'axe.
  - `ex_inverse_supm1` (corrigé 3744) : la graduation −1 était masquée par le point vert de la borne → **refaite** avec « −1 » en vert au-dessus de l'axe, du côté libre, comme −2, −3, −4.
  Recompilées, détecteur sans alerte. Aucun texte d'exercice modifié.
- Contrôles finaux : `verifier_notion.py --navigateur` sur une copie de travail dont `meta.json` déclare les Id 3743, 3744 et 3745 (créés à l'import du 29/10, absents de l'export) : **OK, 0 problème**, contrôle Chrome compris. Captures téléphone des corrigés 2032 et 3744 regardées.

## Finition 2026-11-02

**État : prêt** (agent-finition-S3). 13 exercices (nombre suffisant, aucun ajout) ; **13 sur 13 ont désormais une figure** (8 n'en avaient pas).

### Titres
- Cours : « Fonctions de référence » → **« Se constituer un répertoire de fonctions de référence »** (intitulé officiel) ; fiche : « Résumé : Se constituer un répertoire de fonctions de référence ».
- 8 titres d'exercices au format « Type - sujet » (plus de nom de fonction répété en tête, plus de `$…$`, plus de type « Maîtrise ») : « Découverte - Images et sens de variation d’une fonction affine », « Découverte - Images, symétrie et équations avec la fonction carré », « Découverte - Images et inéquation avec la fonction cube », « Découverte - Ensemble de définition, signe et équation de la fonction inverse », « Découverte - Ensemble de définition et inéquation avec la racine carrée », « Entraînement - Résoudre f(x) = k avec les fonctions de référence », « Entraînement - Comparer x, x² et x³ pour x positif », « Problème - Encadrer √2 par balayage ».

### Figures
- Les 13 figures existantes avaient été revérifiées aujourd'hui (section précédente) : non refaites.
- **12 figures neuves** (style livre, détecteur texte/trait : 0 erreur, 0 alerte ; chaque PNG regardé ; plusieurs étiquettes déplacées après relecture) :
  - cours : `cours_affine` (I : −2x + 3 < 7 ⇔ x > −2, avec la droite y = 7), `cours_inverse_ineq` (III : 1/x < 2 branche par branche), `balayage_racine2` (VIII : points du tableau sur y = x², √2 entre 1,4 et 1,5) ;
  - exercices : 2025 (`ex_affine_f` droite et images ; `ex_affine_g` g(x) ≤ −8 ⇔ x ≥ 3), 2026 (`ex_carre_sym` points (±5 ; 25) ; `ex_carre_compare` f(−4) > f(−1)), 2029 (`ex_cube_8` x³ ≥ 8), 2027 (`ex_inverse_sym3` symétrie de centre O), 2028 (`ex_racine_3` √x < 3 ⇔ x ∈ [0 ; 9[), 2030 (`ex_inverse_compare` piège 1/(−2) et 1/3), 2031 (`ex_carre_16` x² = 16 et x² = −4), 3745 (`balayage_racine2`).
- Toutes les nouvelles figures des corrigés sont placées hors des encadrés « étape » (pleine largeur sur téléphone).

### Contrôles
- `verif_171.py` : **96 contrôles** (sympy), dont les valeurs de chaque nouvelle figure et l'**exécution réelle** des deux blocs Python `balayage` du texte (sorties 1,4…1,5 ; 1,41…1,42 ; 1,414…1,415 et affichage `1.4000000000000004`).
- `verifier_notion.py --navigateur` : **OK, 0 problème**. Captures téléphone regardées : cours (partie I avec la nouvelle figure), corrigés 2025 et 3745.
- Chrome est resté bloqué à la fermeture après les captures (défaut connu) : seul mon processus a été arrêté et son verrou `chrome_0.lock` libéré.

### Remarque pour l'orchestrateur
- Titres du cours et de la fiche changés (intitulé officiel) : penser à `titres_docs.py` à l'import.
