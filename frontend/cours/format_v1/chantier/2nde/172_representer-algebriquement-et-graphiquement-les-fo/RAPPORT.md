# Rapport — 2nde / 172 « Représenter algébriquement et graphiquement les fonctions »

**État : prêt** (verifier_notion --navigateur : OK, 0 problème ; controle_apercu : aucun problème).

## Programme (Seconde 2019)
Contenus couverts : image, antécédent, ensemble de définition, courbe représentative, parité et traduction géométrique, résolution graphique de f(x) = k, f(x) < k, f(x) = g(x), f(x) < g(x), résolution algébrique (inéquations produit / quotient par tableau de signes), modélisation. Pas d'empiètement sur 171 (fonctions de référence), 173 (variations, extremums) ni 178.

## Texte
- **Cours** restructuré : propriété M(a ; b) ∈ Cf encadrée, méthode de lecture graphique, deux propriétés de résolution graphique (droite horizontale / deux courbes, inégalités strictes), confirmation par le calcul en `aligned`, propriété « traduction géométrique » de la parité, méthode en 4 étapes pour les inéquations, tableau de signes en `::: tableau` natif (image retirée), encadré « définition » mal employé remplacé par « résultat », « À retenir » en liste.
- **Fiche** : ajout de f(x) < k, tableau de signes natif avec exemple.
- **Exercices** : tous remis en forme (plus de `\displaystyle`, intervalles `{]a\,;b[}`, résultats longs en formule centrée, tableaux de signes natifs).
  - **2039 remplacé** (titre changé) : l'ancien résolvait f(x) = g(x) « d'après une table » (non rigoureux) ; nouveau : résolution graphique puis démonstration de la factorisation et tableau de signes.
  - 2038 : résolution graphique d'abord, calcul (pentes des segments) en vérification ; point isolé x = 5 signalé.
  - 2036 : l'énoncé montrait la courbe à tracer → remplacée par un repère vide ; la courbe est dans le corrigé.
  - 2040 : figures déplacées dans le corrigé (elles donnaient la réponse) ; contre-exemple numérique pour h.
  - 2041 : question 6 ajoutée (g impaire ⇒ g(0) = 0).
  - 2042, 2043 : tableaux de signes natifs, signe de x + 1 ajouté (2043), attention sur les crochets / valeur interdite.
  - 2044 : l'ancienne figure Q5 avait les étiquettes des intersections inversées → refaite.
- **Ajouts** : `nouveau-1` « Résolution graphique sur une courbe : f(x) = k et f(x) < k » (cubique lue graphiquement, point de tangence à exclure, aucune solution, confirmation exacte ±√3) ; `nouveau-2` « Enclos rectangulaire : résoudre A(x) ≥ 21 de deux façons » (modélisation, graphique puis tableau de signes avec un facteur 7 − x).
- Aucune erreur de maths dans la source, hormis la figure 2044 Q5 ; tous les résultats vérifiés par `verif_172.py` (70 contrôles sympy).

## Figures
- 29 images en ligne : **toutes remplacées ou retirées** (style matplotlib, légendes minuscules, une erreur d'étiquette) ; 0 conservée.
- 33 figures neuves style livre (`figures/figures.py`) : 3 cours (2 reprises dans la fiche), 30 exercices ; solutions en vert sur l'axe (bornes pleines / vides), seuils orange en pointillés, graduations placées à la main (XLAB) pour éviter les courbes. Image cours n° 4 (tableau de signes) retirée.
- Avertissements restants du compilateur : seulement des étiquettes à fond blanc sur la grille ou sur une graduation (aucun refus).

## Contrôles
Captures téléphone regardées : cours (4 vues), fiche, exercices 2039, 2042, 2043, nouveau-2 (énoncé + étapes). Tableaux de signes sortis des encadrés « étape » : à l'intérieur, la colonne +∞ était coupée sur téléphone.

## Remarques pour l'orchestrateur
- Moteur : un `::: tableau` à 4 valeurs avec −∞ / +∞ imbriqué dans un `::: etape` déborde (+∞ coupé) en largeur téléphone sans être signalé par controle_apercu ; libellés de ligne longs (« (x+1)(x−3) ») idem. Contournement : tableau hors de l'étape, libellé « Produit ».
- Titres de 2039 et 2038 en texte simple (plus de `$…$`).

## Finition 2026-11-02

**État : prêt** (agent-finition-S3). 12 exercices (aucun ajout) ; **12 sur 12 ont une figure** (2037 et 2041 n'en avaient pas).

### Revérification des 33 figures existantes
- Toutes recompilées avec le détecteur texte/trait et regardées une par une ; justesse contrôlée (chaque point tracé est sur sa courbe et correspond à l'énoncé : x² − 2x − 3, x² − 3x + 1, x² − 4, x² − 5, x³ − x, x³ + x², x² − 2 et y = x, ligne brisée ABCD, (x − 2)(x + 3), (2x − 3)/(x + 1), tarifs 2x + 3 et x + 8, (x³ − 3x)/2, x(10 − x)) : **aucune erreur mathématique**.
- **9 refaites** pour des défauts de lisibilité :
  - `cours_lecture`, `cours_resolution` (cours et fiche) : l'étiquette 𝒞f était posée sur la parabole (alerte du détecteur) → déplacée ; graduation 6 collée à la flèche « y » → retirée ;
  - `ex_inter_enonce`, `ex_inter_points`, `ex_inter_sup` (2039) : la graduation −2 touchait le sommet de la parabole et la graduation −1 coupait la droite y = x → −2 retirée (ligne de quadrillage gardée), −1 placée au-dessus de l'axe ;
  - `ex_appart_enonce`, `ex_appart_corrige` (2035), `ex_quotient_q4`, `ex_quotient_q5` (2043) : graduation du haut collée à la flèche « y » → retirée.
- 24 conservées (justes, lisibles, sans alerte).

### Figures ajoutées (3)
- 2037 : `ex_table_q4` (les sept points de la table et la droite y = 2 : antécédents −2 et 2) et `ex_table_q5` (points sur ou sous l'axe : f(x) ≤ 0 pour −1, 0, 1) — points seuls, sans courbe, puisque seule la table est connue.
- 2041 : `ex_parite_table` (f paire : symétriques par rapport à l'axe des ordonnées ; g impaire : symétriques par rapport à l'origine, en vert).

### Titres
- Cours et fiche : intitulé officiel déjà en place.
- 11 titres d'exercices réécrits (« Maîtrise » supprimé, sujet explicite), par exemple : « Découverte - Savoir si un point appartient à une courbe », « Découverte - Tracer une courbe à partir d’une table de valeurs », « Entraînement - Reconnaître une fonction paire ou impaire », « Entraînement - Résoudre f(x) = k et f(x) ≥ k sur une ligne brisée » (l'ancien titre annonçait f(x) ≤ k alors que la question porte sur f(x) ≥ 1), « Entraînement - Résoudre une inéquation produit avec un tableau de signes », « Problème - Comparer deux tarifs de taxi », « Problème - Enclos rectangulaire d’aire au moins 21 m² ».

### Contrôles
- `verif_172.py` : **89 contrôles** (sympy), dont les points de toutes les figures.
- `verifier_notion.py --navigateur` : sur le dossier réel, les 2 seuls signalements sont les Id 3748 et 3749 (créés à l'import du 29/10, absents de `meta.json`) ; sur une copie de travail dont `meta.json` les déclare : **OK, 0 problème**, contrôle Chrome compris.
- `controle_apercu.mjs` avec captures : aucun problème (téléphone et ordinateur).

### Remarque pour l'orchestrateur
- Ré-exporter `meta.json` (Id 3748 et 3749 absents) avant l'import.
