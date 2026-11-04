# Rapport — Terminale, notion 82 « Limites des fonctions »

**État : prêt.** Cours 95, fiche 73, 11 exercices (Id inchangés, titres inchangés).

## Texte

- **Cours** restructuré en 7 parties : limites en l’infini (définitions, asymptote horizontale), limite infinie en un réel (gauche/droite, asymptote verticale, exemple détaillé), tableau des limites de référence, tableaux d’opérations (somme, produit, quotient) et formes indéterminées, méthodes pour lever une F.I. (terme dominant, $(x-a)$, conjugué, taux d’accroissement) avec exemples alignés, composition, comparaison et gendarmes, croissances comparées avec démonstration complète (cas $n = 1$ puis cas général). Asymptote oblique signalée « Pour aller plus loin » (hors programme, utilisée dans les exercices 867 et DS).
- **Fiche** réécrite (1–2 écrans) : asymptotes, formes indéterminées, outils, croissances comparées, 4 pièges.
- **Exercices** : tous réécrits au modèle du pilote (méthode / étapes / résultat, encadrés attention-retenir), DS restructuré en `## Partie A…E` + `## Question A1…`.
- **Erreurs de maths corrigées** :
  - 867 Q4 : limites de $k(x) = \frac{x^2+2x}{x+1}$ en $-1$ inversées en ligne (numérateur $\to -1 \lt 0$) : $-1^+ \to -\infty$, $-1^- \to +\infty$.
  - 1192 Q3 : utilisait des **équivalents** (hors programme) → composition avec la limite rappelée $\frac{1-\cos X}{X^2} \to \frac12$.
  - 1191 Q3 : « multiplier par $x$ » sans tenir compte du signe → encadrement par $|x|$.
  - Passages à la limite incorrects (« $\frac{1}{x(\sqrt{1+0}+1)} = \frac{1}{2x}$ », « $\to \frac{1+0}{x(1-0)}$ ») réécrits (DS B3, 1190 Q5) ; minorations maladroites ou fausses dans 1196 (Q1 « $x \ge 1$ » justifié pour $x \ge 0$, Q2, Q4, Q5) refaites proprement ; vocabulaire « discontinuité amovible » remplacé (867 Q3 : point exclu, limite finie, pas d’asymptote) ; 1195 Q2 : la limite à gauche de $\sqrt{x}$ « n’a pas de sens » (et non « n’existe pas »).
  - Asymptotes obliques (867, DS D2) désormais guidées par l’écriture $f(x) = ax + b + r(x)$, conforme au programme.
- `verif_limites.py` : 145 contrôles sympy/numpy, 0 erreur.

## Figures

- **13 figures neuves** au style des livres (`figures/figures.py`), aucune étiquette sur un trait (contrôle automatique OK, 0 avertissement).
- **Refaites (10 images en ligne remplacées)** : cours 1–3 (asymptotes, gendarmes, croissances comparées), fiche 1–2, exercice 867 Q1–Q5 (matplotlib, légendes minuscules).
- **Ajoutées (6 places)** : DS D1 et D2 (asymptotes), 1195 Q4 ($|x|/x$), 1191 Q1 ($x^2\sin\frac1x$ entre deux paraboles) et Q2 (réutilise la figure du cours), 1194 Q3 (asymptote $y = \frac12$).
- **Conservées : 0. Retirées : 0.**

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème** (16 nouvelles places d’images, 0 image en ligne conservée ; contrôle Chrome téléphone + ordinateur sans débordement ni erreur de formule).
- Chaque PNG regardé (planches de relecture) ; étiquettes déplacées jusqu’à 0 avertissement.

## Remarques pour l’orchestrateur

- Exercice 867 : la ligne `Image:` d’origine est conservée (5 positions, toutes remplacées par les nouvelles figures).
- Les exercices 1193 et DS E3 utilisent $\ln$ (croissances comparées de $\ln$) : à placer après le chapitre logarithme dans la progression, ou à garder tel quel (le cours le signale en remarque).


## Finition 2026-11-02

**État : prêt.** Passe de finition (consignes du 2026-11-02 : figures revérifiées, figures partout où elles aident, titres, qualité).

**Figures existantes revérifiées (13).** Détecteur passé, puis chaque image regardée à l'œil ; toutes les courbes correspondent à leur fonction (asymptotes, point exclu, signes en −1 et en −3).
- **Refaite : `cours_gendarmes`** (cours, et corrigé de 1191 Q2). La figure était trop aplatie, et les graduations « 1/2 » étaient ambiguës, placées entre deux traits. La courbe −1/x débordait sous le cadre, les étiquettes 1/x étaient minuscules, et les graduations 2π et 4π touchaient la courbe. Le repère est maintenant plus haut, avec des graduations 0,5 et 1 et des étiquettes à la taille du texte. Les graduations de x sont reportées sous le graphique.
- **Retouchée : `conj_sqrt`**, dont l'étiquette « asymptote y = 1/2 » utilisait une fraction minuscule.

**Figures ajoutées (8), toutes dans les corrigés, éléments de réponse en vert.**

| Exercice | Question | Figure |
|---|---|---|
| 1188 | Q5 | exponentielle, asymptote y = 0 en −∞ |
| 1189 | Q1 | 1/x + 3 et son asymptote y = 3 |
| 1190 | Q1 | droite y = x + 1 privée du point (1 ; 2) |
| 1192 | Q4 | courbe du sinus et tangente en π, de pente −1 |
| 1193 | Q4 | ln x / x, maximum 1/e, limite 0 |
| 1196 | Q1 | x + sin x au-dessus de la minorante y = x − 1 |
| 1195 | Q5 | (2x + 1)/(1 − x), asymptotes x = 1 et y = −2 |
| 1197 | C1 | (2x + sin x)/(x + 1) entre ses gendarmes |

**Les 11 exercices ont maintenant au moins une figure** (il en manquait 6).

**Titres.** Le nom du chapitre répété et les majuscules abusives sont retirés :

| Id | Nouveau titre |
|---|---|
| 1188 | Découverte - Limites de référence |
| 1189 | Découverte - Opérations sur les limites |
| 1197 | DS - Limites, asymptotes et croissances comparées |
| 867 | Entraînement - Asymptotes d’une courbe |
| 1190 | Entraînement - Formes indéterminées |
| 1195 | Entraînement - Limites à gauche et à droite |
| 1194 | Entraînement - Racines carrées et quantité conjuguée |
| 1193 | Entraînement - Exponentielle, logarithme et croissances comparées |
| 1192 | Entraînement - Limites avec sinus et cosinus |
| 1196 | Entraînement - Théorème de comparaison |
| 1191 | Entraînement - Théorème des gendarmes |

Le titre du cours et celui de la fiche étaient déjà conformes.

**Exercices réécrits.**
- **1192 (hors programme).**
  - L'ancienne Q3 utilisait la limite admise (1 − cos x)/x² → 1/2, et l'ancienne Q4 la fonction tangente : les deux sont hors programme de spécialité.
  - Nouvelle Q3 : (cos x − 1)/x → 0, comme taux d'accroissement de cos en 0.
  - Nouvelle Q4 : sin x/(x − π) → −1, interprétée comme la pente de la tangente en π (avec une figure).
  - Le rappel porte maintenant sur « taux d'accroissement et nombre dérivé ».
- **1196 (faible, réécrit entièrement).**
  - Le théorème de comparaison y était appliqué à des polynômes, dont la limite se calcule directement.
  - Les nouvelles questions portent sur des cas où le théorème est indispensable, avec des termes en sin et cos sans limite : x + sin x, x + 2 cos x en −∞ (majorer), √(x² + x), x² − x sin x (multiplication par un négatif), eˣ + 3 cos x.
- **1195, question 5.** Elle reprenait la question 3, et l'exercice 1190 Q1 traitait la même fonction. Elle est remplacée par g(x) = (2x + 1)/(1 − x) en 1⁺ et en 1⁻ (piège du dénominateur 1 − x), avec une figure.

**Contrôles.**
- `verif_limites.py` : 164 contrôles réussis, 0 erreur (145 auparavant). Il couvre les questions réécrites et les données des nouvelles figures.
- `verifier_notion.py --navigateur` : OK, 0 problème.
- Captures téléphone regardées : la fiche et les étapes de 1191 (questions 1 à 3, avec les deux figures de gendarmes).

**Reprise du 2026-11-02 (après interruption).** Les 21 figures ont été recompilées : le détecteur texte/trait ne signale aucune erreur et aucun avertissement. Chaque planche a été relue à l'œil, et `inv_plus3` et `ds_gend_x` ont été contrôlées en taille réelle (asymptotes exactement en y = 3 et y = 2). Retouches :
- `gend_x2sin` (1191 Q1) : les étiquettes y = x² et y = −x² passent de 8,5 pt à la taille du texte, et la fraction 1/x de l'étiquette bleue n'est plus minuscule.
- Fiche, encadré « Formes indéterminées » : sur téléphone, un « ; » commençait une ligne. Les séparateurs sont maintenant des virgules, collées aux formules.

**Remarque pour l'orchestrateur.** Le détecteur texte/trait de `figures_livre.py` a laissé passer trois défauts que j'ai vus à l'œil et corrigés :
- l'étiquette « y = ln x / x » posée sur la courbe ;
- une légende posée sur l'axe des abscisses ;
- une étiquette collée à une tangente.

La relecture à l'œil reste indispensable.
