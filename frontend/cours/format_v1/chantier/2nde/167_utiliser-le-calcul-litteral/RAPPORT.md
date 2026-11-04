# Rapport — 167 Utiliser le calcul littéral (Seconde)

**État : prêt.** Vérificateur (`--navigateur`) : voir § Contrôles.

## Programme (Seconde 2019, « Utiliser le calcul littéral »)
Capacités couvertes après reprise : puissances entières relatives, racines carrées
(dont √(a²) = |a| et les deux démonstrations du programme), fractions et fractions
littérales, identités remarquables (illustration géométrique de (a+b)²), choisir la
forme adaptée, exprimer une variable en fonction des autres, comparer par
différence ou par quotient, modéliser par une inéquation, inéquations du 1er degré,
équations/inéquations produit ou quotient par tableau de signes, x² = a et
représentation graphique de x² < a.

## Texte
- **Cours** remanié en 6 parties (I Puissances, II Racines, III Fractions — nouvelle,
  IV Développer/factoriser/choisir la forme, V Équations, VI Inéquations, signe,
  comparaison) ; démonstrations au programme en encadré `demonstration` ;
  ajouts : √(a²) = |a|, quotient nul, exprimer une variable, comparaison
  différence/quotient, factorisation complète 3(x+1)(x−1) ; tableau de signes natif.
- **Fiche** : identités en formules séparées, tableau de signes natif, fractions,
  quotient nul, comparaison, 5e piège (valeur interdite).
- **Exercices** (14 en ligne, Id inchangés, aucun bloc retiré) :
  - 1907 : texte perdu à la conversion (« $x2$ », signes < disparus) en Q2, Q3 et
    Solution → rétabli ; Q5 (doublon de Q4, résultat constant −1) **remplacée** par
    une comparaison par quotient 3²⁰ / 2³⁰ ; titre → « Entraînement - Comparaison -
    Différence ou quotient ».
  - 1913 Q2 : **hors programme** (discriminant Δ, programme de Première) →
    remplacée par une équation quotient résolue par produit en croix (S = {5/3}),
    avec vérification des valeurs interdites.
  - 1908 : Solution Q4 tronquée (« 2(1-x) -2/5 ») rétablie ; intervalles au format
    {]a\,;b]} ; erreur fréquente (sens de l'inégalité) ajoutée.
  - 1909 : résultat Q3 et Solution 3 tronqués (« C_A(x)10 ») rétablis ; énoncé
    reformulé (Q3/Q5 n'étaient plus distinctes) ; lecture graphique (figure) et
    contrôle autour de la valeur frontière ; erreur fréquente (10 séances : égalité).
  - 1900, 1905, 1906 : titres d'étapes coupés sur deux lignes par la conversion
    réparés ; mises en garde (simplification par un facteur, valeur interdite).
  - 1911 : virgules décimales {,}.
  - 1901, 1902, 1903, 1904, 1910, 1912 : justes, conservés.
  - **Ajouts** : `nouveau-1` (tableau de signes : produit nul, inéquations produit et
    quotient, x² ≤ 4x) ; `nouveau-2` (x² = a, lecture graphique de x² < 9 et
    x² ≥ 9, x² ≤ 2, 2 figures) ; `nouveau-3` (Problème : trois formes de
    (x−1)² − 4, choisir la forme adaptée, minimum par la différence).
- Tous les résultats (110 contrôles) vérifiés avec sympy :
  `verif_calcul_litteral.py`.

## Figures
- 3 refaites (cours : carré (a+b)², parabole x² = a, droite graduée x ≥ 3) ;
  fiche : carré refait (même figure).
- 2 images en ligne retirées (tableau de signes en image, cours 4 et fiche 2) :
  remplacées par un `::: tableau` natif.
- 3 ajoutées (1909 : droites des coûts ; nouveau-2 : énoncé et corrigé).
- 0 conservée.
- `TOLERE` : carre_identite (étiquettes a, b des cotes, fond blanc).

## Contrôles
- verifier_notion --navigateur : **OK, 0 problème** (17 exercices, 7 figures,
  2 images en ligne non appelées → supprimées à l'import).
- controle_apercu avec captures : aucun problème (téléphone + ordinateur).
- Vues regardées au téléphone : cours (4 parties), fiche, exercices 1909, 1907
  (via le vérificateur), nouveau-1, nouveau-2. Corrigé après relecture :
  formules longues mises en `aligned` (démonstration, factorisation,
  comparaison), règles en liste (plus de `\qquad` qui s'empilait mal),
  tableaux de signes sortis des encadrés (libellé « Produit » / « Quotient »)
  pour qu'ils tiennent en largeur, figures sorties des étapes.
- Piège rencontré : un `<` puis un `>` sur la même ligne (« $x<2$ … $x>2$ »)
  est pris pour une balise HTML → écrits `\lt` / `\gt`.

## Remarques pour l'orchestrateur
- **Défaut d'outil** : `verifier_notion.py` plante dès qu'un exercice `nouveau-N`
  coexiste avec des Id numériques (ligne 127 : `sorted(appels.items())` compare
  `str` et `int` → TypeError). Contourné sans modifier l'outil (lancement via un
  `sorted` tolérant injecté par runpy). Correctif suggéré :
  `sorted(appels.items(), key=lambda kv: (kv[0][0], str(kv[0][1])))`.

## Vérification des figures 2026-11-02

- **6 figures vues** (8 appels : 3 du cours, 1 de la fiche — reprise du cours —, 1 du corrigé 1909, 2 de l'exercice 3737), à l'œil et avec le détecteur texte/trait de `figures_livre.py` : 6/6 sans chevauchement (seule alerte : les cotes a et b du carré, sur fond blanc, déjà tolérées).
- Contrôles : (a + b)² découpé en a², 2ab, b² ; x² = 4 → −2 et 2, ]−2 ; 2[ en vert, y = −1 sans intersection ; −2x + 6 ≤ 0 → [3 ; +∞[ crochet fermé ; C_A = 30 + 5x et C_B = 8x sécantes en (10 ; 80) ; parabole et y = 9 sécantes en ±3, a) ]−3 ; 3[ et b) ]−∞ ; −3] ∪ [3 ; +∞[. Style des livres, largeur ≤ 880 px.
- `ex_x2_corrige` (corrigé 3737, question 2) avait été refaite par la session interrompue (partie b en orange) : vérifiée, conforme.
- **Défaut trouvé** : la question 3 de l'exercice 3737 (x² ≤ 2) raisonnait « sur la parabole » sans la montrer. **Figure ajoutée** `ex_x2_q3_corrige` (parabole, droite y = 2, points d'abscisses ±√2, [−√2 ; √2] bornes incluses en vert) : appel `[IMAGE_3]` dans l'étape « Lecture sur la parabole » + entrée dans `correspondance.json`. Aucun autre texte modifié.
- Contrôles finaux : `verifier_notion.py --navigateur` → les 3 seuls « problèmes » sont les Id 3736, 3737, 3738, créés à l'import du 29/10 mais absents de `source_en_ligne/meta.json` (export antérieur). Sur une copie de travail dont `meta.json` déclare ces 3 Id : **OK, 0 problème**, contrôle Chrome compris. Captures téléphone de l'exercice 3737 regardées : figure nette, lisible, sans débordement.
- Pour l'orchestrateur : ré-exporter `meta.json` après un import qui crée des exercices, sinon `verifier_notion.py` signale ces Id comme inconnus.

## Finition 2026-11-02

**État : prêt** (agent-finition-S1). 17 exercices (aucun ajout : nombre déjà suffisant).

### Titres
- Cours « Utiliser le calcul littéral » et fiche « Résumé : Utiliser le calcul littéral » : intitulé officiel, conservés.
- 17 titres « Type - Chapitre - Sujet » (majuscules abusives « Calcul Littéral », type « Maîtrise ») → « Type - sujet », par exemple « Découverte - Réduire une expression puis calculer sa valeur », « Entraînement - Comparer par la différence ou par le quotient », « Entraînement - Développer et factoriser avec les identités remarquables », « Problème - Choisir un abonnement grâce à une inéquation », « Entraînement - Tableau de signes : produits et quotients », « Découverte - Résoudre x² = a et lire sur la parabole », « Problème - Choisir la forme adaptée d’une expression ».

### Exercices
- **1905 Q5 réécrite (hors programme)** : factoriser x² + 5x + 6 demande une technique de Première → (x² + 6x + 9)/(x² − 9) = (x + 3)/(x − 3), avec les deux identités remarquables, valeurs interdites ±3 et erreur fréquente (−3 reste interdite après simplification).
- **434 `\displaystyle` retirés** (fractions inline démesurées sur téléphone).
- 1903 Q1 : erreur fréquente (oubli du double produit) ajoutée ; 1904 Q3 : « Simplifier » → « Factoriser » (le résultat attendu est 4(x − 2)), corrigé par facteur commun + vérification en développant.
- Corrigés redécoupés après captures téléphone (formules coupées ou réduites) : 1900 Q3, 1904 (Q1, Q2, Q3, Q4, Q5), 1905 Q5, 1907 Q3, 1912 Q1 et Q3.

### Figures (7 nouvelles)
- Aires : `ex_carre_x1` (1900 Q4 : (x+1)² − x² − 1 = 2x), `ex_carre_x4` (1903 Q1 : (x+4)²), `ex_factorisation_aires` (1904 Q5 : (x+1)(3x+1), pour x > 3/2), `distributivite` (cours IV : k(a + b) = ka + kb).
- Courbes et droites : `ex_comparaison` (1907 Q1 : y = (x+1)² et y = x² + 3 sécantes en (1 ; 4)), `ex_forme_canonique` (3738 Q3 : minimum −4 en 1, racines −1 et 3), `ex_droite_q4` (1908 Q4 : ]−2/5 ; +∞[).
- 8 exercices sur 17 ont une figure ; sans figure : puissances, puissances de 10, fractions, racines, équations quotients, exprimer une variable (calculs purs) et 3736 (tableaux de signes natifs).
- `figures_livre.py` : 0 erreur ; alertes = étiquettes de cotes sur fond blanc (tolérées, `TOLERE`).

### Contrôles
- `verif_calcul_litteral.py` : **137 contrôles** (sympy), tout juste.
- `verifier_notion.py --navigateur` : OK ; `controle_apercu.mjs` avec captures : aucun problème.
- Captures téléphone regardées : 1900, 1904, 1905, 1907, 1909, 1911, 1912, 1913 (étapes).
- Après les derniers redécoupages (résultats de 1904 Q2/Q5, vérification Q3) : `verifier_notion.py --navigateur` OK et `controle_apercu.mjs --rapide` : aucun problème. Lors du passage avec captures, Chrome est resté bloqué à la fermeture (défaut connu) : seul mon processus a été arrêté et son verrou `chrome_2.lock` libéré.
