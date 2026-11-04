# Notion 165 (Seconde) : Manipuler les nombres réels

**État : prêt.**

## Texte
- Cours 160 : la conversion avait laissé des puces « • » collées, deux démonstrations au programme
  dans une « définition », un `retenir` en pavé et du code avec une ligne > 30 caractères. Corrections :
  vraies listes, objectifs en liste, deux encadrés `demonstration` (1/3 non décimal, √2 irrationnel,
  argument « le carré d’un impair est impair » ajouté), tableau inégalités ↔ intervalles (7 cas),
  ℝ = ]−∞ ; +∞[, remarque sur l’intersection (utilisée par l’exercice 1929), |x| = x ou −x,
  méthode d’arrondi en encadré, code de balayage raccourci.
- Fiche 133 : puces en listes, tableau inégalités ↔ intervalles, « Réflexe » en `conseil`.
- Exercices (10) : tout réécrit au format pilote (méthode / étapes / résultat, un seul résultat par question).
  - 1934 : code de l’énoncé **cassé** (`$\ast\ast$` dans le bloc Python) → réparé ; justification
    u² ≤ v² ⇔ u ≤ v ; remarque sur l’affichage `1.4100000000000004`.
  - 1927 : la liste « Rappel (méthode) » se mélangeait à la numérotation des questions → encadré `rappel` ;
    Q3 refaite proprement (100x − 10x = 15, sans décimal intermédiaire) ; simplifications justifiées.
  - 1926, 1929, 1932 : listes de nombres séparées par « ; » (les virgules étaient ambiguës avec la virgule décimale).
  - 1933 : « à 10⁻ⁿ près » harmonisé avec le cours (amplitude 10⁻ⁿ) ; ajout d’un `attention` :
    avec la touche π on obtient 72,4 cm² et non 72,3.
  - `\displaystyle` retirés, notations `[a\,;b]`, intervalles « ]… » et « …[ » entre accolades et
    `\lvert -5\rvert` (sinon KaTeX espace le signe moins comme une soustraction).
- Aucune erreur de maths trouvée dans les résultats ; 48 contrôles dans `verif_165.py` (fractions, arrondis
  en Decimal, exécution réelle de la fonction de balayage pour n = 1 à 5 et pour √3).

## Figures
- 6 refaites (cours ; anciennes figures matplotlib multicolores) : ensembles emboîtés, droite des réels,
  intervalles, distance, intervalle centré, zooms d’encadrement de √2. La fiche réutilise ensembles + intervalles.
- 4 ajoutées dans les corrigés : intersection (1929 Q1), deux solutions de |x − 3| = 2 (1930 Q5),
  ]−5 ; 1[ centré en −2 (1931 Q4), tolérance [29,7 ; 30,3] (1935 Q2).
- 0 conservée ; les 8 images en ligne ne sont plus appelées (remplacées aux mêmes positions).
- Toutes ≤ 900 px, aucun chevauchement signalé, chaque PNG regardé.

## Contrôles
- `verifier_notion.py --navigateur` : OK, 0 problème ; `controle_apercu.mjs` : aucun problème.
- Vues regardées (téléphone) : cours en entier, fiche, exercices 1934, 1929, 1931, 1935 (étapes).
  Formules centrées : aucune coupée ; deux lignes `\qquad` trop réduites sur téléphone mises en liste.

## Remarques pour l’orchestrateur
- Moteur (KaTeX) : `x \in ]a;b[`, `= ]2;4]` ou `= |-5|` sont mal espacés ; contournement par
  `{]a\,;b[}` et `\lvert -5\rvert`. Une règle globale dans le moteur ou le convertisseur serait utile
  pour les autres notions sur les intervalles.
- Sur téléphone, les figures larges (droites graduées) sont réduites : graduations petites mais lisibles.

## Vérification des figures 2026-11-02

- **10 figures vues** (toutes celles appelées : 6 du cours, 2 de la fiche — reprises du cours —, 4 des corrigés 1929, 1930, 1931, 1935), à l'œil et avec le détecteur texte/trait de `figures_livre.py` : 10/10 sans chevauchement ni avertissement.
- Contrôles : valeurs et bornes conformes aux énoncés (]2 ; 4], x = 1 ou 5, ]−5 ; 1[, [29,7 ; 30,3]), crochets dans le bon sens, √2 bien placé à chaque zoom (1,4142), éléments de réponse en vert, style des livres, largeur ≤ 880 px.
- **Défauts trouvés : aucun. Figures refaites : aucune.** Notion inchangée : statut remis à « importe ».

## Finition 2026-11-02

**État : prêt** (agent-finition-S1). 12 exercices (10 existants + 2 ajoutés).

### Titres
- Cours « Manipuler les nombres réels » et fiche « Résumé : Manipuler les nombres réels » : intitulé officiel, conservés.
- 10 titres « Type - Chapitre - Sujet » (avec `\displaystyle` dans 3 d'entre eux, types « Algorithmique », « Approfondissement », « Maîtrise ») → « Type - sujet » : « Entraînement - Encadrer racine de 2 par balayage en Python », « Entraînement - Écriture décimale périodique et fraction », « Découverte - Dire si un nombre appartient à un intervalle », « Découverte - Passer d’une inégalité à un intervalle », « Entraînement - Décimal, rationnel ou irrationnel », « Entraînement - Intervalle centré et valeur absolue », « Entraînement - Intersection de deux intervalles », « Découverte - Valeur absolue et distance entre deux réels », « Entraînement - Encadrer et arrondir un nombre réel », « Problème - Tolérance de fabrication et valeur absolue ».

### Exercices
- **1932 Q4 réécrite** : « 1/6 est-il décimal ? justifier avec l'écriture décimale » était faible (voir 0,1666… à l'écran ne prouve rien) → démonstration guidée du programme « 1/3 n'est pas décimal » (10ⁿ = 3k, somme des chiffres de 10ⁿ = 1), avec erreur fréquente.
- **2 ajoutés** (capacités du programme non travaillées) :
  - `nouveau-1` « Découverte - Lire et placer des réels sur une droite graduée » : lecture d'abscisses en quarts, placement de −3/4, 2,5 et √2 (encadrement par les carrés), appartenance à [−1 ; 1], distance AD = 3,25 ;
  - `nouveau-2` « Problème - Arrondir avec le bon nombre de chiffres significatifs » : terrain 23,4 m × 15,7 m, chiffres significatifs, aire 367 m², encadrement 365,4 ≤ A ≤ 369,4 (pourquoi 367,38 est trompeur), diagonale ≈ 28,2 m, grillage arrondi par excès (79 m).
- Cours : méthode « Chiffres significatifs » ajoutée en IV (capacité du programme absente) ; objectif complété.

### Figures (8 nouvelles, 7 exercices de plus avec figure)
- Corrigés : `ex_balayage` (1934 : pas de 0,01, 1,41 accepté / 1,42 refusé, √2), `ex_appartenance` (1926 : ]3,5 ; 4]), `ex_traduire` (1928 : trois ensembles), `ex_classer` (1932 : D ⊂ Q ⊂ R avec les 5 nombres), `ex_cinq_septiemes` (1933 : 5/7 dans [0,7 ; 0,8]), `n1_droite_corrige` (nouveau-1, points placés en vert et [−1 ; 1]).
- Énoncés : `n1_droite_enonce` (nouveau-1), `n2_terrain` (nouveau-2, données).
- 11 exercices sur 12 ont une figure ; seul 1927 (écriture périodique → fraction, calcul pur) n'en a pas.
- `figures_livre.py` : 0 erreur ; seule alerte : la cote « 23,4 m » sur sa flèche (fond blanc, tolérée).

### Contrôles
- `verif_165.py` : **69 contrôles** (21 ajoutés), tout juste.
- `verifier_notion.py --navigateur` : OK ; `controle_apercu.mjs` avec captures : aucun problème (téléphone et ordinateur).
- Captures téléphone regardées : nouveau-1, nouveau-2, 1932 (étapes) : rien de coupé.
- À l'import : 2 exercices `nouveau-N` à relier.
