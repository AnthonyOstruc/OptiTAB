# Notion 83 — Continuité des fonctions (Terminale)

**État : prêt.** Cours 107, fiche 12 et 5 exercices (868, 870, 872, 869, 871) au format v1.
Tous les résultats sont recalculés dans `verif_continuite.py` (63 vérifications sympy/numpy, toutes justes).

## Texte

**Cours** : structure revue (I. Fonction continue en 5 sous-parties, II. Suites, III. TVI,
IV. Dichotomie). Ajouts : exemple de la partie entière (programme), démonstration
« dérivable ⇒ continue », méthode du raccord (limites à gauche / à droite), prolongement par
continuité (utilisé dans 3 exercices, absent du cours), théorème du point fixe avec sa
justification, tableau de variations natif avec α, pièges du TVI (intervalle, unicité,
racines doubles), algorithme de dichotomie détaillé. Le « Corollaire » était un encadré
`definition` → `theoreme`.

**Fiche** : refondue (continuité, raccord, prolongement, point fixe, TVI, unicité, dichotomie, 4 pièges).

**Erreurs de fond corrigées dans les exercices** :
- 870 : la Solution annonçait « discontinuité évitable » pour $1/(x-1)$ (Q1) et pour $\sin(1/x)$ (Q4) ;
  c'est une limite infinie (asymptote) et une absence de limite. La justification de Q4
  (« $1/x$ oscille ») était fausse : remplacée par deux suites $x_n$, $y_n$ (images $1$ et $-1$).
- 869 Q2 : « $e^x = 2x$ n'a pas de solution » n'était pas démontré (deux valeurs testées) :
  étude de $e^x - 2x$, minimum $2 - 2\ln 2 > 0$ en $\ln 2$, tableau de variations natif.
- 871 Q4 : limite en $+\infty$ obtenue par « $+\infty - (+\infty) = +\infty$ » (forme
  indéterminée) : levée par factorisation et croissances comparées.
- 871 Q2 / Q4 : tableaux de signes erronés (lignes parasites « $e^x : +, 1, +$ », facteurs) et
  lignes « Analyse du tableau » tronquées par l'ancienne conversion (« pour $x 1$ ») : tableaux
  natifs propres, application du corollaire du TVI intervalle par intervalle, solutions localisées
  et valeurs approchées ajoutées.
- 868 / 872 : « $f(2) = \frac{0}{0}$ → indéterminée » et « discontinuité évitable » (hors programme)
  remplacés par « $f$ n'est pas définie en $2$ » et « prolongeable par continuité » ; les limites
  $\frac{\sin x}{x}$, $\frac{\ln(1+x)}{x}$, $\frac{e^x - 1}{x}$ sont justifiées par un taux d'accroissement.
- 869 Q1 : $f(0)$ et $f(2)$ de même signe → explication du point intermédiaire, deux solutions localisées.
- Notation des intervalles harmonisée ($[0\,;2]$), énoncé de 870 complété par la définition des
  trois types de discontinuité (saut, limite infinie, absence de limite).

## Figures (31 images en ligne, toutes au style matplotlib ancien ou non conforme)

- **refaites : 29 positions** (style livre, `figures/figures.py`, 28 figures distinctes, toutes
  sans texte sur un trait d'après le contrôle de `figures_livre.py`) : cours 1 à 4
  (continuité / partie entière, TVI, unicité, dichotomie), fiche 1 et 2, 23 positions d'exercices
  (fenêtres resserrées sur ce qui compte, trous en rond vide, prolongements en vert, sauts et
  asymptotes signalés).
- **ajoutée : 1** — cours [IMAGE_2] : construction en escalier de la suite $u_{n+1} = \sqrt{u_n + 2}$
  (la dichotomie passe en [IMAGE_5] ; toutes les positions du cours sont de nouvelles figures).
- **fiche** : réutilise les figures TVI et unicité du cours.
- **retirées : 2** — 868 [IMAGE_4] (droite + point, doublon visuel de 868 Q1 / 871 Q1) et
  871 [IMAGE_5] ($\frac{\sin x}{x}$, même fonction que 868 Q3).
- **conservées : 0**.

## Contrôles

- `valider_v1.py` : 0 problème ; `verifier_notion.py --navigateur` : **OK** (30 nouvelles figures,
  0 conservée, 2 images en ligne non appelées → supprimées à l'import).
- `controle_apercu.mjs` avec captures : aucun problème (téléphone et ordinateur) ; vues regardées :
  cours en téléphone (dont tableau de variations avec α), fiche, exercice 870 (étapes) en téléphone.

## Remarques pour l'orchestrateur

- Les lignes `Image:` des exercices sont laissées telles quelles (en-tête informatif).
- 870 garde le mot « Classifier » (titre imposé) : l'énoncé définit les trois cas (saut, limite
  infinie, absence de limite) pour rester dans le vocabulaire du programme.


## Finition 2026-11-02

**État : prêt.** Passe de finition (consignes du 2026-11-02 : figures revérifiées, figures partout où elles aident, titres, qualité).

**Figures existantes revérifiées (28).** Détecteur passé, puis chaque image regardée à l'œil : valeurs (α, β, c, extremums, sauts, prolongements) et lisibilité. Retouchées :
- `ex871_raccord_ab` : un pointillé était superposé à la droite orange y = 1 ; il ne reste que le pointillé vertical.
- `ex872_racine` : l'étiquette m̃(0) = 1/2 utilisait une fraction minuscule.
- `ex869_exp_2x` : l'étiquette « écart minimal ≈ 0,61 », loin de sa flèche, est placée à côté d'elle.
- `ex870_sin_inv` : le quadrillage passait devant le « 1 » du haut, qu'on pouvait lire « −1 ». Le quadrillage est retiré de cette figure.
- `ex869_ln` : refaite pour la nouvelle question 3.
- `ex871_prolong` : retirée (question supprimée), son fichier est supprimé.

**Figures ajoutées (2), dans le corrigé de 871, éléments de réponse en vert.**
- Q1 : escalier de la méthode de Héron vers √2.
- Q5 : intervalles successifs de la dichotomie autour de β.

Les 5 exercices avaient déjà une figure dans chaque question où elle aide. La question 868 Q4 reste sans figure : k(x) = x + 1 partout, une simple droite n'apporterait rien.

**Titres.**
- Cours : « Continuité des fonctions d’une variable réelle ». Fiche : « Résumé : Continuité des fonctions d’une variable réelle ».
- Exercices :

| Id | Nouveau titre |
|---|---|
| 868 | Découverte - Continuité en un point |
| 870 | Entraînement - Fonctions non continues en un point (au lieu de « Classification des discontinuités », vocabulaire hors programme) |
| 872 | Entraînement - Prolongement par continuité |
| 869 | Entraînement - Théorème des valeurs intermédiaires |
| 871 | Problème - Continuité, suites et équations |

**Exercices réécrits.**
- **869, question 3 (faible).** La solution x = 1 de « ln x = 1 − x sur ]0 ; 1] » était évidente, et c'était une borne. La nouvelle question est un vrai corollaire du TVI : ln x = 2 − x a une unique solution α dans [1 ; 2], avec 1,5 < α < 1,6.
- **871, questions 1 et 5 (doublons).** Elles reprenaient mot pour mot 868 Q1 et Q3, avec les mêmes fonctions. Elles sont remplacées par deux points explicites du programme :
  - Q1 : méthode de Héron, image d'une suite convergente par une fonction continue, ℓ = h(ℓ), d'où ℓ = √2 ;
  - Q5 : dichotomie en Python sur l'équation de Q4, fonction à compléter et tableau des 7 étapes. `dichotomie(1, 2, 0.01)` renvoie `(1.140625, 1.1484375)`.
- L'énoncé de 871 précise que Q5 utilise Q4. La fonction de Héron s'appelle h, pour ne pas la confondre avec f(x) = eˣ − x − 2.

**Contrôles.**
- `verif_continuite.py` : 74 vérifications, toutes justes (63 auparavant).
- `verifier_notion.py --navigateur` : OK, 0 problème.
- Captures téléphone regardées : cours (parties II à IV : point fixe, TVI, unicité, dichotomie), fiche, exercice 871 (étapes, de la question 1 à la question 5).

**Reprise du 2026-11-02 (après interruption).** Les 29 figures ont été recompilées : le détecteur texte/trait ne signale aucune erreur et aucun avertissement. Chaque planche a été relue à l'œil, puis les figures à petits détails en taille réelle. Quatre figures ont été retouchées pour la lecture sur téléphone :
- `cours_tvi` (cours et fiche) : les étiquettes a, b, c₁, c₂, c₃, f(a), k, f(b) et y = f(x) sont agrandies (`\large`) et le repère est resserré (806 → 763 px). Sur téléphone, elles ont maintenant la taille du texte.
- `cours_point_fixe` : u₀, u₁, u₂ et ℓ = 2 passent de 8,5 pt à la taille du texte. La graduation 2 est placée à droite de son trait pour ne pas toucher u₂.
- `cours_dichotomie` et `ex871_dicho` : les bornes des intervalles et le m passent de 8,5 à 10,5 pt. La colonne « étape 0 … étape 7 » est remplacée par un en-tête « étape » et des numéros. Les figures sont resserrées (854 → 635 px et 836 → 703 px), donc moins réduites sur téléphone. Les étapes de la dichotomie de 871 ont été recontrôlées (signe de f au milieu à chaque étape).

Point laissé tel quel : le tableau de l'étape 2 de 871 Q5 (4 colonnes de décimales) défile dans son cadre sur téléphone, comme le prévoit le format.

**Remarque pour l'orchestrateur.** La question 871 Q5 occupe la position [IMAGE_5], dont l'image en ligne avait été retirée lors de la première passe : la nouvelle figure la remplace.

## Enrichissement 2026-11-02

**État : prêt** (non importé). 5 → **11 exercices** : 6 blocs ajoutés à la fin de `exercices.txt` (`Id: nouveau-1` à `nouveau-6`). Les 5 exercices existants sont identiques à l'octet près (comparés à `sauvegardes/exercices_avant_enrichissement_20261102.txt`). Sauvegardes : `sauvegardes/*_avant_enrichissement_20261102.*` (exercices, figures.py, correspondance.json, verif_continuite.py).

### Exercices ajoutés
| Id | Titre | Difficulté | Compétence |
|---|---|---|---|
| nouveau-1 | Découverte - Continuité par lecture graphique | easy | Lire images et limites latérales, repérer un saut et un point déplacé, continuité sans dérivabilité (pointe), TVI inapplicable sans continuité (f(x) = 2 sans solution sur [2 ; 5]) |
| nouveau-2 | Découverte - Fonctions de référence et partie entière | easy | Continuité par opérations et composées (polynôme, e^(−x), ln(x² + 1), √(4 − x)), fonction rationnelle et piège du TVI sur [0 ; 4], partie entière (E(−0,5) = −1), d(x) = x − E(x) non continue en 2 |
| nouveau-3 | Entraînement - Fonction définie par morceaux et paramètre | medium | Paramètre de raccord : a = 5 (polynômes), m = 2 (exponentielle / rationnelle), tarif de taxi b = 6,5, C(25) = 36,50 €, course de 20 km |
| nouveau-4 | Entraînement - Nombre de solutions et encadrement par balayage | medium | f(x) = 2x³ − 3x² − 1 : limites, variations, aucune solution sur ]−∞ ; 1], unique α (corollaire du TVI sur un intervalle non borné), balayage 1,6 < α < 1,7 puis 1,67 < α < 1,68, trois solutions de f(x) = −1,5 |
| nouveau-5 | Problème - Suite récurrente et point fixe | hard | u(n+1) = (5u(n) + 4)/(u(n) + 2), u0 = 0 : construction graphique, récurrence 0 ≤ u(n) ≤ u(n+1) ≤ 4, convergence monotone, ℓ = f(ℓ) par continuité → ℓ = 4, programme Python de seuil (renvoie 6) |
| nouveau-6 | Type examen - Fonction auxiliaire, TVI et minimum | hard | Sujet type bac en 3 parties : g(x) = x² − 4 + 2 ln x (limites, variations, unique α, 1,71 < α < 1,72, signe) ; f(x) = x/2 + (1 − ln x)/x (limites, f' = g/(2x²), variations, f(α) = α − 1/α, 1,12 < f(α) < 1,14) ; f(x) = 2 a exactement deux solutions |

Chaque exercice : énoncé avec contexte et questions numérotées ; corrigé « méthode / étapes / résultat » avec erreurs fréquentes (`attention`) et `retenir` ; solution courte. Rien hors programme (programme de Terminale spécialité 2020 : continuité, image d'une suite convergente, point fixe, TVI et corollaire, balayage).

### Figures (11 nouvelles, style livre, `figures_livre.py` : 11/11, 0 refus)
- Énoncé (ne donnent pas la réponse) : `n1_lecture` (courbe à lire), `n2_partie_entiere` (courbe de E), `n5_escalier` (courbe de f et droite y = x, u0 seul).
- Corrigé, complétées en vert : `n1_lecture_corrige` (saut, point déplacé, pointe, droite y = 2) ; `n2_dents_corrige` (d(x) = x − E(x)) ; `n3_raccord_corrige` (a = 5 en vert, a = 3 en pointillés : saut) ; `n3_taxi_corrige` (raccord en 10 km) ; `n4_solutions_corrige` (α et les trois solutions de f(x) = −1,5) ; `n5_escalier_corrige` (escalier u0 → u3, ℓ = 4) ; `n6_g_corrige` (α et signe de g) ; `n6_f_corrige` (minimum f(α), solutions β et γ de f(x) = 2).
- Retouches après relecture des PNG : étiquettes déplacées hors des traits (graduations −3 et 4 de `n1_lecture`, ordonnées à droite de l'axe, notes de `n4`, `n5`, `n6_g`), axes en bord de cadre pour `n3_raccord_corrige` (graduations 3 et 5 posées sur les paraboles).
- Clés `nouveau-1` à `nouveau-6` ajoutées dans `figures/correspondance.json` (alt descriptifs).

### Contrôles
- `verif_continuite.py` : nouvelle section « Enrichissement 2026-11-02 » (une partie par exercice + données des figures), 55 contrôles sympy/numpy, dont le programme `seuil` exécuté réellement ; **129 vérifications : tout est juste**.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (42 figures, 6 exercices à créer).
- `controle_apercu.mjs` avec captures : aucun problème. Captures téléphone des 6 nouveaux énoncés et corrigés regardées. Corrigé : tableau de variations de nouveau-4 sorti de son encadré `point` (il défilait), tableaux de balayage passés en colonnes, phrases réécrites là où « ; » ou « : » tombait seul en début de ligne après une formule.

### Remarque pour l'orchestrateur (moteur)
Le moteur ne protège la ponctuation que collée à la formule (`$x$;`). Avec l'espace français (`$x$ :`), le « : » ou le « ; » peut passer seul à la ligne au téléphone. Contourné ici en reformulant ; une correction dans `optitabDoc.js` (inclure l'espace insécable dans `otm-nb`) réglerait tous les contenus.
