# Notion 81 : Limites et convergence des suites (Terminale)

**État : prêt** (cours 86, fiche 28, 10 exercices).

## Texte

- **Cours** restructuré selon le modèle du pilote : théorème de récurrence, méthode de rédaction, exemple détaillé (calculs alignés), mise en garde sur l’initialisation (4^n + 1). Les démonstrations au programme sont maintenant dans de vrais encadrés `demonstration` : Bernoulli, comparaison, q^n avec q > 1, suite croissante non majorée. Ajouts conformes au programme : tableaux d’opérations sur les limites (somme, produit, quotient), suites majorées, minorées et bornées, somme géométrique et sa limite, propriété f(ℓ) = ℓ (f continue) avec méthode d’étude de u_{n+1} = f(u_n). Le code Python « seuil » a été exécuté (31 vérifié).
- **Fiche** réécrite : récurrence, limites, formes indéterminées, gendarmes, tableau de q^n, suites monotones, pièges.
- **Exercices** : tous les corrigés suivent maintenant le schéma méthode / étapes / résultat (il manquait les encadrés `resultat`). Le devoir (1171) avait des encadrés cassés à la conversion : il a été restructuré en Parties A, B, C et questions A1 à C3.
- **Corrections de fond** :
  - 1162 : n^{1/2} et « n^k pour k réel » sont hors programme ; remplacés par les limites de référence.
  - 1169 : l’énoncé de la question 3 n’était pas une inégalité, la consigne a été reformulée. Les initialisations doublées (deux rangs, ce qui est trompeur) ont été réduites à un seul rang. L’hérédité de la question 4 passe maintenant par (k − 1)² − 2 ≥ 7, sans discriminant.
  - 1168 : les formules 1, 2 et 4 sont posées pour n ≥ 1 (au lieu d’une somme vide en n = 0). Un conflit de notation entre l’indice k et l’entier de récurrence a été levé.
  - 1171 B2 : le passage aux inverses est maintenant justifié (fonction inverse décroissante).
  - 1170 et 1171 C3 : le passage à la limite est justifié (continuité, unicité de la limite).
- Aucune erreur de résultat dans la source : **toutes les limites, identités et récurrences sont vérifiées** par `verif_limites_suites.py` (sympy + contrôles numériques), qui affiche « TOUT EST JUSTE ».

## Figures (style des livres, `figures/figures.py`)

- **Refaites, 4** : les 4 images du cours (dominos, bande de convergence, gendarmes, q^n en 4 panneaux). La figure q^n sert aussi dans la fiche, en position 2.
- **Ajoutées, 5** :
  - dans le cours, l’escalier de u_{n+1} = 0,5 u_n + 1 ;
  - dans les corrigés, le nuage de points de (−2)^n (1164) et l’encadrement sin(n)/n (1165) ;
  - les escaliers en vert du problème (1170) et du devoir (1171).
- **Conservées : 0.** **Retirée : 1**, le dessin des dominos de la fiche (décoratif, la fiche reste courte).
- Aucun texte posé sur un trait (détecteur sans erreur), toutes les figures font 900 px de large au plus. Les graduations de (−2)^n sont placées du côté libre de l’axe ; pour sin(n)/n, elles sont reportées sous le graphique.

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème**. Le bloc de code était trop large sur téléphone : il a été corrigé en déplaçant les commentaires dans le texte.
- Vues regardées en téléphone : le cours (parties I à VI), la fiche, l’énoncé de l’exercice 1162 et les étapes du devoir 1171. Les tableaux d’opérations ont été compactés avec ±∞ pour la lecture sur téléphone.

## Remarques pour l’orchestrateur

- La figure q^n (4 panneaux, environ 880 px) s’affiche un peu réduite sur téléphone, mais reste lisible.
- Le titre « ## Question A1 : … » n’a pas de pastille numérotée : l’expression régulière de `optitabDoc.js` n’accepte que des numéros entiers. Le rendu reste correct. On pourrait accepter `[A-Z]\d+` dans la regex de `renderHeading`.


## Finition 2026-11-02

**État : prêt.** Passe de finition (consignes du 2026-11-02 : figures revérifiées, figures partout où elles aident, titres, qualité).

**Figures existantes revérifiées (9).** Contrôle du détecteur, puis relecture à l'œil de chaque image (justesse des termes, des escaliers, lisibilité sur téléphone). Toutes sont justes. Trois ont été retouchées :
- `suites_qn` (cours et fiche) : dans les panneaux q = −0,8 et q = −1,2, les graduations de n tombaient au milieu des points. Elles sont maintenant reportées sous les panneaux.
- `escalier_cours`, `escalier_pb` et `escalier_ds` : il y avait un pointillé de trop, sans nom (u₃). Il est retiré, et l'étiquette u₂ du problème, décalée et ambiguë, est maintenant centrée.

**Figures ajoutées (7), toutes dans les corrigés, éléments de réponse en vert.**

| Exercice | Question | Figure |
|---|---|---|
| 1162 | Q5 | s_n = 5 + 2/n, qui tend vers 5 par valeurs supérieures |
| 1163 | Q4 | 2 − 5/n², qui tend vers 2 par valeurs inférieures |
| 1167 | Q6 | √(n² + n) − n, qui tend vers 1/2 |
| 1168 | Q1 | deux escaliers de Gauss, 2 × 15 = 5 × 6 |
| 1169 | Q4 | 2ⁿ et n², avec la zone n ≥ 4 et le contre-exemple n = 3 |
| 1166 | Q1 | termes qui alternent entre les deux gendarmes |
| 1171 | B1 | (2n + sin n)/(n + 1) entre ses gendarmes |

Chaque figure est accompagnée d'un encadré « À retenir » ou d'une étape d'interprétation. **Les 10 exercices ont maintenant au moins une figure** (il en manquait 6). La légende de la figure de Gauss est placée sous la figure, pour garder une largeur de 480 px et rester lisible sur téléphone.

**Titres.** Le nom du chapitre répété et les majuscules abusives sont retirés :

| Id | Nouveau titre |
|---|---|
| 1162 | Découverte - Limites de référence |
| 1163 | Découverte - Opérations sur les limites |
| 1171 | DS - Limites, gendarmes et suite récurrente |
| 1167 | Entraînement - Formes indéterminées |
| 1169 | Entraînement - Récurrence : inégalités et divisibilité |
| 1168 | Entraînement - Récurrence : formules de sommes |
| 1164 | Entraînement - Limites des suites géométriques |
| 1165 | Entraînement - Théorème des gendarmes : premiers encadrements |
| 1166 | Entraînement - Théorème des gendarmes : encadrements plus fins |
| 1170 | Problème - Suite récurrente et convergence monotone |

Le titre du cours et celui de la fiche étaient déjà conformes à l'intitulé officiel.

**Exercice réécrit.** 1170, question 4 : « vérifier que ℓ = √(ℓ + 2) » répétait la question 3. Elle est remplacée par un algorithme de seuil en Python (fonction à compléter, puis tableau des valeurs) : `seuil(0.001)` renvoie 6.

**Contrôles.**
- `verif_limites_suites.py` affiche « TOUT EST JUSTE ». Il couvre désormais l'algorithme de seuil, le tableau des valeurs et toutes les données des nouvelles figures.
- `verifier_notion.py --navigateur` : OK, 0 problème.
- Captures téléphone regardées : cours (partie V, gendarmes et q^n), fiche, exercices 1162, 1168 (Gauss), 1171 (partie B, avec la figure) et 1170 (code Python et tableau).

**Reprise du 2026-11-02 (après interruption).** Les 16 figures ont été recompilées : le détecteur texte/trait ne signale aucune erreur et aucun avertissement. Chaque planche a été relue à l'œil, et les valeurs des termes ont été recontrôlées ((−2)ⁿ, 2ⁿ et n², escaliers, gendarmes). Retouches pour la lecture sur téléphone :
- `suites_qn` (cours et fiche) : la figure faisait 873 px et était réduite à 70 % sur téléphone. Les panneaux sont resserrés et les titres passent sur deux lignes (« q = 1,2 » / « qⁿ → +∞ »), ce qui donne 702 px. Les titres ont maintenant la taille du texte.
- `escalier_cours`, `escalier_pb` et `escalier_ds` : le repère passe de 6,2 à 5,6 cm, pour que les étiquettes u₀, u₁, u₂, ℓ et les équations soient moins réduites sur téléphone.
- Captures téléphone regardées après retouche : la fiche (qⁿ) et les étapes du DS 1171 (partie C, avec l'escalier).

**Remarque.** `controle_apercu.mjs` est resté bloqué à la fermeture de Chrome alors que toutes les vues étaient écrites. J'ai arrêté uniquement mon processus et supprimé mon seul verrou (`chrome_0.lock`).
