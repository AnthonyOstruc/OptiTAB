# Notion 154 — Équations et fonctions polynômes du second degré (Première spécialité)

**État : prêt.** Aucun point en suspens.

## Texte

**Cours** (refondu, programme 2019) : 5 parties — trinôme et forme canonique (méthode, variations en
`::: tableau` natifs pour $a > 0$ et $a < 0$, lien avec la translation de $y = ax^2$) ; équation et
discriminant avec la **démonstration du programme** dans un encadré `demonstration` ; factorisation,
somme et produit des racines (avec preuve), **stratégies diversifiées** (identité remarquable, racine
évidente, somme-produit, formules), trinômes de racines données ; signe et inéquations (tableau de
signes natif, méthode, erreurs fréquentes) ; choix de la forme adaptée (exemple de la balle, tableau
« quelle forme pour quelle question »), changement de variable en « Pour aller plus loin ».

**Fiche** : tableaux des trois formes et des trois cas de $\Delta$, formules encadrées, tableau de
signes générique, 5 pièges classiques.

**Exercices** : les 19 blocs ont été entièrement réécrits (la conversion avait cassé la structure des DS
et sujets type examen : questions fusionnées dans des encadrés `methode`, solutions mal numérotées).
Structure `## Partie` / `## Question`, méthode, étapes détaillées, résultat, erreurs fréquentes,
tableaux de signes natifs. Titres harmonisés (« Polynômes du second degré »).

Erreurs de maths ou défauts corrigés :
- 1325 (DS 2) : durée au-dessus de 6 m donnée à 0,64 s → **0,63 s** ($\sqrt{10}/5$, piège de l’arrondi
  signalé) ; question « même signe » ambiguë reformulée (non nuls et de même signe) ; solutions
  numérotées n’importe comment et inégalités tronquées (« $f(x) 0$ ») ;
- 1426 (paraboles) : les réponses ne correspondaient pas à l’image (B de sommet $(0;2)$ annoncée
  $x^2 + 3$, D de sommet $(2;-2)$ annoncée $(x+1)^2 + 2$) ; exercice refait avec une figure juste ;
- 1320 : réponse « $m 2$ » tronquée (question remplacée) ; 1322, 1330 : « $f(x) 0$ » tronqués.

Remplacements (même Id) :
- 1323 : boîte de volume fixé (degré 3) et enclos de 200 m² (fonction $x + 200/x$) **hors programme
  du chapitre** → entiers consécutifs, projectile, allée autour d’un parterre, fenêtre (gardée) ;
- 1326 : exercice 2 « carton » ($S(x) = 4x^2 + 96/x$, hors chapitre) → bénéfice d’un artisan ;
- 1327 B5 : aire $\ge 2\,400$ m² impossible (question vide) → $\ge 1\,200$ m², solution $[20;30]$ ;
- 1329 ex. 3 : paramètre dont le discriminant valait toujours 16 (questions sans objet) → $P_m$ avec
  $\Delta_m = 4(m+1)(m-2)$, discussion complète ;
- 1316 : factorisations toutes au discriminant → stratégies diversifiées (programme) ;
- 1320 Q3–Q4 (exercices techniques dans un « Problème ») → recette d’un théâtre, jardin ;
- 1330 A2 : même trinôme que 1324 et 1321 → $2x^2 - 2x - 12$ ; ajouts mineurs (1315 Q6–Q7,
  1318 Q6, 1319 Q6 racine évidente).

Ajouts : `nouveau-1` (Découverte — lire une parabole : signe de $a$, sommet, racines, forme canonique) ;
`nouveau-2` (Problème — parabole et droite : intersections, position relative, droite tangente selon
$m$) ; `nouveau-3` (Entraînement — changement de variable, équations bicarrées, « Pour aller plus loin »).

Tous les résultats sont vérifiés par `verif_154.py` (sympy) : **156 vérifications justes**.

## Figures

- 13 figures neuves au style des livres (`figures/figures.py`), toutes contrôlées par le détecteur de
  chevauchement et regardées une à une.
- Cours : 4 refaites (formes, discriminant, signe, projectile) + 1 neuve (variations $a > 0$ / $a < 0$) ;
  l’ancien tableau de variations en image est remplacé par des `::: tableau` natifs.
- Fiche : 2 refaites (grille des cas de $\Delta$, signe générique).
- Exercices : 1 refaite (1426) ; 7 places ajoutées (1325 projectile dans le corrigé, 1323 parterre et
  fenêtre, 1327 et 1330 enclos, nouveau-1 lecture de paraboles, nouveau-2 parabole et droite).
- 0 conservée, 0 retirée.

## Contrôles

- `verifier_notion.py --navigateur` : OK, 0 problème ; `controle_apercu.mjs` : aucun problème.
- Captures téléphone regardées : cours (5 vues), fiche, exercice 1325 (étapes). Corrigé après lecture :
  formules trop larges coupées en `aligned` ou en lignes séparées (20 formules), tableaux de signes à
  libellé long renommés $T(x)$, tableau P/Q à cinq valeurs scindé en deux, tableaux de la fiche passés
  à deux colonnes.

## Remarques pour l’orchestrateur

- La consigne « figures dans `::: etape` » : les tableaux de signes à $\pm\infty$ sont placés hors des
  étapes, comme demandé.
- Le bloc 1426 garde sa ligne `Image: paraboles_transformations_comparaison.png` ; la position 1 est
  remplacée par `paraboles_translations.png` via `correspondance.json`.

## Finition 2026-11-02

**État : prêt** (mise en conformité avec les consignes du 2026-11-02 : figures partout où elles aident, titres).

### Titres
- Cours : « Équations, fonctions polynômes du second degré » ; fiche : « Résumé : Équations, fonctions polynômes du second degré ».
- 19 titres d'exercices changés : « Polynômes du second degré » / « Second degré » retirés, titres raccourcis ; les « Type 1 à 4 » (DS, Type examen) reçoivent un titre qui dit leur contenu (ex. « Type examen - Techniques et champ le long d'un mur »). Les trois exercices `nouveau-N` gardent leur titre (déjà conforme).

### Figures (27 nouvelles, toutes regardées, 0 chevauchement ; réponses en vert)
- Fiche I : parabole avec sommet, axe et racines (figure du cours).
- Corrigés manquants signalés : 1426 (vecteurs des trois translations), 1323 (projectile au-dessus de 40 m, parterre avec x = 1 m et 10 m × 8 m, fenêtre optimale à l'échelle), 1327 (champ 25 m × 50 m ; parabole de l'aire avec seuil 1 200 et [20 ; 30]), 1330 (enclos 7 m × 14 m), nouveau-1 (racines et intervalles des inéquations sur les quatre paraboles).
- Énoncés ajoutés : 1324 (rectangle ABCD), 1320 (jardin initial et agrandi), 1322 (triangle rectangle a, b, c), 1329 (carré inscrit).
- Autres corrigés : 1314 (trois paraboles, Δ > 0, = 0, < 0), 1324 (signe de f sur la courbe ; aire maximale 16), 1321 (même trinôme que 1324), 1325 (signe de f, maximum 1), 1328 (h ≤ 0 sur [2 ; 4] ; trajectoire du ballon), 1318 (k ≤ 0 sur [1 ; 3], g < 0 sauf en 2), 1317 (même sommet, ouvertures différentes), 1322 (f > 0 sur ]2 ; 4[ ; triangle 6-8-10), 1320 (recette maximale 6 400 €), 1326 (bénéfice ≥ 0 sur [10 ; 30]), 1329 (carré inscrit pour x = 5 ; trois valeurs de m), nouveau-2 (droite tangente en T(2 ; −1) et deux autres droites).
- Sans figure (algèbre pure) : 1313, 1315, 1316, 1319, nouveau-3.

### Exercices réécrits
- 1320, question 2 : c'était exactement l'exemple de la balle du cours (h(t) = −5t² + 20t + 10) → distance d'arrêt d(v) = 0,005v² + 0,3v : calculs, puis inéquation d(v) ≤ 50, v ≤ −30 + 10√109 ≈ 74,4, soit 74 km/h (piège de l'arrondi par excès signalé : d(75) = 50,625).
- 1329, exercice 2 : troisième « rectangle de périmètre fixé → carré » de la notion (doublon de 1324 B et 1320 Q1) → carré inscrit dans un carré : S(x) = x² + (10 − x)² = 2x² − 20x + 100 (Pythagore), minimum 50 cm² pour x = 5, S(x) ≤ 58 ⟺ x ∈ [3 ; 7]. Travaille un minimum (a > 0), absent jusque-là des problèmes.

### Contrôles
- `verif_154.py` (sympy) : 189 vérifications justes (34 nouvelles : deux réécritures + valeurs de toutes les figures ; la vérification de l'ancien exercice 2 de 1329 est retirée).
- `verifier_notion.py` : OK, 0 problème (44 nouvelles figures, 0 image en ligne conservée). Même blocage de `controle_apercu.mjs` à la fermeture de Chrome qu'en 153 : contrôle relancé à part avec délai maximal, mon seul processus arrêté.
- `controle_apercu.mjs` (captures) : 136 vues sur 136 sans défaut (téléphone et ordinateur).
- Formules coupées : contrôle complémentaire de largeur au téléphone + captures regardées (fiche, 1320, 1329). Corrigé : 1323 Q4 (aire de la fenêtre, formule en ligne trop longue → chaîne alignée), 1320 Q2 (lignes v₁ / v₂ et d(50) / d(90) redécoupées). Résultat final : 0 formule trop large (les seuls signalements restants sont les signes « + / − » des tableaux de signes, faux positifs de la mesure).

### Remarque pour l'orchestrateur
- Les exercices `nouveau-1`, `nouveau-2`, `nouveau-3` existent déjà en production (Id **4284**, **4285**, **4286**, voir `sauvegardes/avant_import_20261102-082125.json`) mais le fichier garde `Id: nouveau-N` : ré-exporter la notion (ou remplacer les clés par les vrais Id dans `exercices.txt` et `correspondance.json`) **avant** le prochain import, sinon ils seront créés une seconde fois.
- Dans 1325 et 1322, la numérotation `[IMAGE_N]` ne suit pas l'ordre du texte (positions ajoutées après coup) : sans effet sur l'affichage.
