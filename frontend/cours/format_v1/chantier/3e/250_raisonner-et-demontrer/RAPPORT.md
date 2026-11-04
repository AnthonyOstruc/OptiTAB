# Notion 250 (3e) : Raisonner et démontrer

**État : prêt** (agent-3e-250, 2026-11-03).

Programme du cycle 4, compétence « Raisonner » (attendus de fin de 3e) : conjecture et démonstration, contre-exemple, vrai ou faux justifié, hypothèse / conclusion / réciproque / contraposée (Pythagore, Thalès), démonstration géométrique rédigée (« On sait que… Or… Donc… »), démonstration en calcul littéral (pairs, impairs, multiples, entiers consécutifs, programmes de calcul). Aucune logique formelle de lycée (ni quantificateurs, ni tables de vérité, ni récurrence).

## Cours 245 et fiche 165
- **Cours réécrit** (l'ancien mêlait « contrôler les unités », « arrondir », et le format de l'épreuve du brevet, hors sujet ; peu de géométrie) :
  - I. Conjecture, démonstration, contre-exemple : définitions, propriété (un contre-exemple suffit / des exemples ne prouvent rien), contre-exemple numérique et **géométrique** (losange), méthode du « vrai ou faux » au brevet.
  - II. Hypothèse et conclusion, réciproque (exemple d'une réciproque fausse : trapèze isocèle à diagonales égales), contraposée en mots simples, tableau théorème / réciproque / contraposée, exemple de contraposée de Pythagore.
  - III. Démontrer en géométrie : schéma « On sait que → Or → Donc », méthode de rédaction, exemple rédigé (5, 12, 13), **démonstration** de la somme des angles d'un triangle (alternes-internes), tableau « Pour démontrer que… on peut utiliser… » (quadrilatères, parallèles, perpendiculaires, isocèle), erreurs.
  - IV. Calcul littéral : tableau des écritures ($2n$, $2n + 1$, $d \times n$, consécutifs), figure en points, méthode en 4 étapes, 3 exemples (consécutifs, multiples de 5, programme de calcul démontré), raisonnement par cas, erreurs fréquentes ; `retenir` final.
- **Fiche réécrite** : tableau prouver / réfuter, vrai ou faux, réciproque / contraposée, rédaction, propriétés utiles, écritures littérales, 5 erreurs classiques.
- Titres inchangés (= intitulé de la notion).

## Exercices (21, tous relus et réécrits)
Chaque corrigé : méthode, étapes détaillées (rédaction « On sait que… Or… Donc… » en géométrie, calculs alignés), résultat encadré, erreur fréquente (et « à retenir » quand utile) ; solution courte. Titres « Type - Sujet ». Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 Type brevet.

- **Remplacés (9, même Id)** — exercices hors sujet ou doublons :
  - 2488 « Contrôler les unités » → « Découverte - Une conjecture qui tombe en défaut » ($n^2 + n + 41$, premier de 0 à 39, $1\,681 = 41^2$) ;
  - 2489 « Arrondir selon le contexte » → « Découverte - Contre-exemples en géométrie » (losange, cerf-volant, triangles équilatéraux ; deux affirmations vraies justifiées) ;
  - 2490 « Comparer exactement » → « Découverte - Hypothèse, conclusion, réciproque et contraposée » ;
  - 2494 « Vérifier une solution » (équations) → « Entraînement - Prouver ou réfuter une égalité » ;
  - 2498 « Une copie à corriger » (formules diverses) → « Entraînement - Démontrer qu'un parallélogramme est un rectangle » (réciproque et contraposée de Pythagore, propriétés des quadrilatères) ;
  - 2499 « Le bassin » (volumes) → « Problème - Démontrer le théorème de Pythagore avec des aires » (repris de l'ancien 2505, avec la preuve de l'angle droit du carré central) ;
  - 2500 « La commande au meilleur prix » → « Problème - Deux programmes de calcul » (identité, équation produit nul, minimum $-9$) ;
  - 2504 « Les poignées de main » → « Type brevet - Vrai ou faux justifié » (5 affirmations : calcul littéral, pourcentages, Pythagore, contraposée de Thalès) ;
  - 2505 → « Type brevet - Une démonstration en géométrie » (réciproque de Pythagore, réciproque de Thalès, parallèles et perpendiculaires, Thalès, aire, contraposée).
- **Conservés et enrichis** : 2485, 2486, 2487, 2491 (contraposée, angle droit en B), 2492, 2493, 2495, 2496, 2497 (contraposée avec un point $P$ visible), 2501, 2502 (rédaction « On sait que… Or… Donc… » à chaque étape), 2503.
- Aucune erreur de mathématiques dans l'ancienne version ; les défauts étaient le hors-sujet (6 exercices de « contrôle de résultats »), l'absence de quadrilatères, de contraposée et de vrai ou faux type brevet, et des corrigés trop courts.
- `verif_250.py` : **92 contrôles sympy** (chaque identité démontrée, chaque calcul, chaque triplet pythagoricien, chaque rapport de Thalès, les angles du triangle d'or, $n^2 + n + 41$ premier de 0 à 39), tous OK.

## Figures (style des livres, `figures/figures.py`)
- **30 figures neuves** pour 33 positions ; les 11 images matplotlib en ligne sont toutes remplacées ou retirées (0 conservée).
  - Cours (6) : losange contre-exemple, trapèze (réciproque fausse), schéma « On sait que / Or / Donc », triangle 5-12-13, somme des angles (alternes-internes codés), points pair / impair. Fiche : losange et schéma.
  - Exercices : énoncé (données seules, sans angle droit ni réponse) et corrigé (éléments de la déduction en vert) pour 2491, 2496, 2497, 2498, 2499, 2501, 2502, 2504, 2505 ; figures de contre-exemple dans les corrigés de 2485, 2489 (×3), 2490, 2497 (point $P$), 2504 (point $P$ de la parallèle) ; figure en points pour 2486 ; courbe de l'aire pour 2501.
- Détecteur texte / trait : 0 erreur (seuls avertissements : cotes à fond blanc, usage normal). Chaque PNG regardé ; corrections faites : côtés d'étiquettes mal placés (2485, 2491, 2498), codage des angles égaux de la bissectrice (2502), étiquettes $N$ / $P$ (2497, 2504), schéma ramené sous 900 px.

## Contrôles
- `verifier_notion.py --navigateur` : **OK, 0 problème** (33 nouvelles figures, 0 image en ligne conservée ; seules notes : titres d'exercices changés, voulu).
- `controle_apercu.mjs` avec captures : « Aucun problème détecté ». Vues téléphone regardées : cours en entier (5 captures), fiche, exercices 2489, 2497, 2505 (étapes). Corrections faites après ces vues : schéma « On sait que / Or / Donc » passé en vertical (texte trop petit en horizontal), tableau « Pour démontrer que… » resserré, essais du programme de calcul du cours mis en liste, 7 formules « … donc … » côte à côte découpées sur deux lignes, point final isolé (2505 Q1) supprimé par un calcul aligné.

## Remarques pour l'orchestrateur
- Les en-têtes `Image:` des blocs d'exercices sont laissés tels quels (non utilisés par l'import).
- Le contenu de l'ancien 2505 (preuve de Pythagore par les aires) est passé dans le bloc 2499, pour que les deux « Type brevet » soient en fin de liste (ordre d'affichage = ordre des blocs).
- Le format de l'épreuve du brevet (20 min sans calculatrice…) a été retiré du cours : il relève de la notion 253 « Sujets type brevet ».
