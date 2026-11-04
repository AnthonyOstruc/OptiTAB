# Rapport — Terminale, notion 87 « Dérivation » (cours 88, fiche 32, 10 exercices)

## État

Prêt. Aucun point en suspens.

## Texte

**Cours** (ancien HTML → v1, restructuré façon livre) : objectifs ; I. rappels (tableaux des dérivées
usuelles et des opérations) ; II. composée (définition, schéma, théorème, tableau des cas usuels dont
$\ln u$, méthode, exemples détaillés, erreur fréquente) ; III. dérivée seconde et convexité ;
IV. point d'inflexion (exemple $x^3 - 3x$ avec tableau natif « Convexité de $f$ », contre-exemple $x^4$,
méthode de lecture graphique sur $f$, $f'$, $f''$) ; V. inégalités de convexité ($e^x \ge x + 1$,
$\ln x \le x - 1$, sécante de exp) ; VI. courbe de Lorenz ; encadré « retenir ».

Corrections de fond :
- **définition de la convexité** : l'ancien cours la définissait par les tangentes ; le programme la
  définit par les **sécantes**, l'équivalence avec tangentes / $f'$ croissante / $f'' \ge 0$ étant
  admise → corrigé (définition + théorème « admis ») ;
- démonstration au programme (« si $f'' \ge 0$, la courbe est au-dessus de ses tangentes ») rédigée en
  entier dans un encadré `demonstration` ;
- Lorenz : « à $x$ % de la population » alors que $x$ est une proportion → reformulé.

**Fiche** : formule, tableau des cas usuels, convexité / inflexion avec tableau natif, inégalités,
4 pièges.

**Exercices** (10, rédaction des corrigés reprise question par question : méthode, étapes, résultat) :
- texte perdu à la conversion (« Pour $x 0$ », « Comme $\Delta 0$ »…, 6 endroits) → rétabli ;
- 1258 : « $f$ strictement décroissante sur $D_f$ » **faux** (réunion d'intervalles ; $f(0) = -3 \lt f(2) = 5$)
  → « sur chacun des intervalles » + encadré attention ; ligne $(x - 1)^3$ du tableau de signes fausse
  (double barre en $-1$ où le facteur vaut $-8$, pas de zéro en $1$) → corrigée ;
- 1259 et 1260 : tableaux de variations faux à la 2ᵉ borne (`+D/…` au lieu de `D+/…`, `-D/0` au lieu
  de `D-/0` : valeur du mauvais côté de la double barre, zone interdite non hachurée) → corrigés ;
- 1260 : $f''$ calculée avec des exposants $-\frac{1}{2}$, $-\frac{3}{2}$ (hors programme) → refaite avec
  la formule du quotient ; « concave sur une réunion » → « sur chacun des intervalles » ;
- 1257 : valeurs approchées $\approx 10{,}0$ dans le tableau → $h(x_1)$, $h(x_2)$ (valeurs en texte) ;
  question 4 sans conclusion → ajoutée ; deux tableaux séparés (signe / convexité) fusionnés ;
- 1256 : ordonnée des points d'inflexion ajoutée ($e^{-1/2}$) ; 1261 : non-dérivabilité aux bornes
  justifiée par le taux d'accroissement ; 1254 : signe d'un quotient en tableau natif ;
- tous les tableaux de convexité : une seule ligne « Convexité de $f$ » (`concave` / `convexe`, `t` au
  point d'inflexion, `d` + `h` hors domaine) — vérifiés un par un.

Tous les résultats sont vérifiés par `verif_derivation.py` (sympy, 134 contrôles, 0 échec).

## Figures

- **12 images en ligne, toutes remplacées** (aucune conservée) : les 4 du cours et les 2 de la fiche
  étaient au style matplotlib ; les 6 des exercices étaient des tracés matplotlib par défaut
  (légendes minuscules, grands vides) et **2 étaient fausses** : 1255 traçait une autre fonction
  (maximum $(-1\,;12)$, minimum $(2\,;-15)$ au lieu de $(1\,;5)$ et $(3\,;1)$) ; 1257 sans point d'inflexion.
- **11 figures neuves** (style livre, `figures/figures.py`) : 5 pour le cours (schéma de composée,
  convexe / concave avec sécante et tangente, inflexion de $x^3 - 3x$, Lorenz, et **1 ajoutée** :
  exp et ln avec leurs tangentes $y = x + 1$ et $y = x - 1$), réutilisées 2 fois dans la fiche ;
  6 pour les exercices, éléments de réponse en vert (points d'inflexion, tangente $y = 5$).
- 0 retirée ; contrôle des chevauchements texte / trait : 0 erreur.

## Contrôles

- `verif_derivation.py` : tous les contrôles bons.
- `verifier_notion.py --navigateur` : 0 problème.
- Captures téléphone regardées : cours (toutes les parties), fiche, exercices 1257, 1260, 1258
  (énoncé + étapes).

## Remarques pour l'orchestrateur

- Libellé de ligne de tableau : un mot seul (ex. `Convexité`) est rendu comme une formule (italique) ;
  il faut un libellé de la forme `Convexité de $f$` (règle de `optitabDoc.js`, libellé texte = 3 lettres
  puis espace).
- Le titre de l'exercice 1258 parle d'« Optimisation », sans question d'optimisation (titre non modifiable).
  → corrigé lors de la finition du 2026-11-02 (« Problème - Fonction rationnelle : asymptotes et convexité »).

## Finition 2026-11-02

**État : prêt** (agent-finition-T3). 13 exercices (10 existants + 3 ajoutés).

### Titres
- Cours « Dérivation et convexité » (conservé : correspond exactement au contenu, composée + convexité) ; fiche « Résumé : Dérivation et convexité ».
- 10 titres d'exercices « Type - Dérivation - … » / « Fonctions Composées - … » (majuscules abusives, « Entrainement » sans accent) → « Type - sujet » : « Découverte - Composer des fonctions et trouver l'ensemble de définition », « Entraînement - Dériver des fonctions composées », « Entraînement - Produit, quotient et point d'inflexion », « Entraînement - Rappels : polynômes, produits et quotients », « Entraînement - Composées avec racines et valeurs absolues », « Problème - Courbe en cloche et points d'inflexion », « Problème - Racine d'un trinôme : variations et concavité », « Problème - Logarithme d'un quotient : étude complète », « Problème - Polynôme de degré 3 : extremums et inflexion », « Problème - Fonction rationnelle : asymptotes et convexité ».

### Exercices
- Les 10 existants relus : justes, au programme ; aucun à réécrire.
- **3 ajoutés** (compétences du programme qu'aucun exercice ne travaillait : lecture graphique de la convexité, inégalité de convexité, convexité dans un problème concret) :
  - `nouveau-1` « Entraînement - Lire la convexité sur la courbe de la dérivée » : signe de f' → variations, variations de f' → convexité, extremums de f' → inflexion ; puis f(x) = x⁴/4 − 3x²/2, signe de f'', tangente en I et position (f − T = ¼(x − 1)³(x + 3)) : la courbe traverse sa tangente ;
  - `nouveau-2` « Type bac - Inégalité de convexité : comparer deux puissances » : ln concave, tangente en e passant par O, ln x ≤ x/e (stricte si x ≠ e via g), d'où πᵉ < eᵖⁱ et xᵉ ≤ eˣ ;
  - `nouveau-3` « Type bac - Propagation d'une information et point d'inflexion » : modèle logistique N(t) = 10/(1 + 9e^(−0,5t)), signe de N'', point d'inflexion I(4 ln 3 ; 5), vitesse maximale 1,25 millier/jour, position par rapport à la tangente.
- Chaque ajout : méthode, étapes détaillées, résultats encadrés, erreurs fréquentes, « à retenir ».

### Figures (19 fichiers, 22 emplacements)
- **Revérifiées** : les 11 existantes, au détecteur (0 erreur) et à l'œil (justesse des courbes et des valeurs, lisibilité).
- **Refaite (1)** : `ex1257_h` — zones concave (orange) / convexe (bleu) de part et d'autre de I, « maximum local » / « minimum local » (l'étiquette « maximum » seule était inexacte : h tend vers +∞).
- **Ajoutées (8)** :
  - corrigés d'exercices existants : `ex1253_chaine` (schéma de f∘g, valeur interdite 2x − 3 ≠ −1 en vert), `ex1261_h` (demi-tangente verticale de √(2x − 1) en 0,5) ;
  - nouveaux exercices : `n1_fprime` (énoncé : courbe de f'), `n1_fprime_corr` (corrigé : parties croissante/décroissante de f' en vert/orange), `n1_f` (courbe de f, inflexions I et J, tangente T), `n2_ln` (ln sous sa tangente y = x/e passant par O), `n3_courbe` (énoncé : courbe en S), `n3_inflexion` (corrigé : I, tangente, asymptote N = 10, zones convexe/concave) ;
  - cours : `n1_fprime_corr` réutilisée (nouvel exemple « Lecture sur la courbe de f' » dans IV).
- Exercices sans figure (2) : 1262 (calculs de dérivées, rappels de Première) et 1254 (expressions de composées) — une figure y serait décorative.
- `figures_livre.py` : 19/19, 0 erreur, 0 avertissement.

### Contrôles
- `verif_derivation.py` : TOUT EST JUSTE, **169 contrôles** (35 ajoutés : nouveaux exercices et valeurs écrites sur les figures).
- `verifier_notion.py --navigateur` : OK, 0 problème ; `controle_apercu.mjs` avec captures : 0 défaut sur toutes les vues (téléphone et ordinateur) — Chrome est resté bloqué à la fermeture après la dernière capture (défaut connu) : seul mon processus a été arrêté et son verrou libéré.
- Captures téléphone regardées : nouveau-1, nouveau-2, nouveau-3 (étapes). Corrigé : 2 tableaux qui défilaient (tableau de signes à 5 valeurs supprimé, redondant avec la liste ; libellé « f(x) − y_T » remplacé par d(x)), 4 formules réduites ou coupées redécoupées (f'(x) et f''(x), développement de (x − 1)³(x + 3), inéquation exponentielle, équation de T) ; N''(t) de l'énoncé de nouveau-3 allégé (v(t) = 9e^(−0,5t) − 1).
- À l'import : 3 exercices `nouveau-N` à relier (relier_nouveaux).
