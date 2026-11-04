# Notion 168 (Seconde) : Manipuler les vecteurs du plan

**État : prêt.**

## Texte
- **Cours 224** : il était trop maigre pour le programme 2019 ; je l’ai remis à niveau.
  - Ajouts : vecteurs égaux, notation $\vec{u}$, égalité ⇔ diagonales de même milieu, méthode de construction
    de la somme (bout à bout ou parallélogramme), différence, règles de calcul de $k\vec{u}$, base et repère
    orthonormés avec $\vec{u} = x\vec{i} + y\vec{j}$, égalité des coordonnées, **norme $\sqrt{x^2 + y^2}$
    (absente avant)**, méthode « lire ou représenter un vecteur », méthode alignement / parallélisme, remarque
    « parallèles ou confondues ».
  - Définition de la colinéarité corrigée : elle excluait les vecteurs nuls. Elle dit maintenant « $\vec{v} = k\vec{u}$
    ou $\vec{u} = k\vec{v}$ », et le vecteur nul est colinéaire à tout vecteur.
  - La démonstration au programme (critère du déterminant) était glissée dans une « définition » : elle est
    maintenant dans un vrai encadré `demonstration`, complète (cas $\vec{u} = \vec{0}$ et cas $x = 0$ rédigés).
  - Le `retenir` en pavé est devenu une liste.
- **Fiche 138** : puces « • » remplacées par de vraies listes, tableau des formules (vecteur, somme, norme,
  distance, milieu), partie « Déterminant », réflexes en `conseil`.
- **Exercices** (10 en ligne + 2 ajoutés) : tous réécrits au format du pilote (méthode en une ligne, étapes
  titrées en texte, calculs alignés, résultat), avec des `attention` sur les erreurs fréquentes. Les `\displaystyle`
  sont retirés et les coordonnées notées $\overrightarrow{AB}\,(3\,;3)$ comme dans le cours.
  - Aucune erreur de maths dans les résultats en ligne. Améliorations de fond :
    - 1966 : « base orthonormée » ajoutée (sinon la norme n’a pas de sens) ; Q5 faite de deux façons.
    - 1956 : traduction en translation et nature de $ABDC$.
    - 1963 : test de Pythagore justifié par le plus long côté ; contrôle $BM^2 + AM^2 = AB^2$.
    - 1964 : mise en garde sur $ABCD$ / $ABDC$ ; Q3 allégée (une seule égalité vérifiée).
    - 1962 et 1961 : parallèles **distinctes** prouvées (déterminant avec $\overrightarrow{AC}$).
    - 1959 : unité km, distance à vol d’oiseau comparée au trajet réel ($\approx 12{,}7$ km).
    - 1957 : hypothèse $\vec{v} \neq \vec{0}$ posée dans l’énoncé ; le cas du vecteur nul est traité en remarque.
  - **Ajouts** (compétences du programme qui n’étaient pas travaillées) :
    - `nouveau-1` « Découverte - Lecture graphique - Coordonnées de vecteurs » : lire des coordonnées sur un
      quadrillage, vecteurs égaux ou opposés, parallélogramme, norme ;
    - `nouveau-2` « Entraînement - Construction - Somme et différence de vecteurs » : construire $\vec{u} + \vec{v}$ et
      $\vec{u} - \vec{v}$ bout à bout, comparer avec le calcul, colinéarité par le déterminant.
  - Aucun remplacement d’exercice : tous étaient au programme et justes.
- `verif_168.py` : 195 contrôles, tous OK (tous les résultats, les relations de Chasles testées sur des points
  au hasard, et les relations vectorielles de 1958 et 1960 testées dans deux triangles différents).

## Figures
- **19 positions servies par 17 figures neuves** (figures.py, style des livres). Les 11 images en ligne étaient
  toutes au style matplotlib (couleurs criardes, texte minuscule, noms de points en gras sans serif) : refaites.
  - Cours (6) : égalité de vecteurs et parallélogramme, Chasles avec règle du parallélogramme, produit par un réel,
    base orthonormée (nouvelle), coordonnées/distance/milieu, points alignés. La fiche réutilise Chasles et coordonnées.
  - Exercices : 4 refaites (1964, 1960, 1959, 1958) et 3 ajoutées dans les corrigés (1956, 1963, 1962).
    Les deux nouveaux exercices ont chacun une figure d’énoncé et une figure de corrigé.
- 0 image conservée, 0 retirée (toutes remplacées aux mêmes positions). Toutes ≤ 900 px, aucun chevauchement
  signalé par le compilateur, chaque PNG regardé.

## Contrôles
- `verifier_notion.py --navigateur` : OK, 0 problème (lancé depuis une copie corrigée, voir ci-dessous).
- Vues regardées sur téléphone : le cours en entier (4 captures), la fiche, les exercices 1967 (énoncé et étapes)
  et nouveau-2 (étapes, avec la figure de construction). Corrections faites après ces captures :
  - le tableau de formules de la fiche défilait sur téléphone : il est devenu une liste, avec la distance en formule centrée ;
  - « $ABDC$ est un parallélogramme » est sorti de `\text{}` dans une formule centrée (il était réduit) ;
  - trois formules trop longues ont été passées en `aligned` (1967 Q4, nouveau-2 Q5, 1962 Q5) ;
  - aucune formule n’est coupée.
- `controle_apercu.mjs` : relancé après ces corrections. Les 88 vues (téléphone et ordinateur) n’ont aucun
  débordement, aucune erreur de formule, aucun `$` brut, aucune image manquante. Le dossier `captures/` est laissé en place.

## Remarques pour l’orchestrateur
- **Défaut d’outil** (`verifier_notion.py`, lignes 127 et 145) : dès qu’une notion contient un exercice
  `nouveau-N`, `sorted(appels.items())` et `sorted(nouvelles.items())` mélangent des Id `int` et `str`.
  Résultat : `TypeError: '<' not supported between instances of 'str' and 'int'`. Correctif proposé :
  `sorted(..., key=lambda kv: (kv[0][0], str(kv[0][1])))`, et l’équivalent pour `nouvelles`. Je ne l’ai pas
  modifié : j’ai lancé une copie corrigée depuis mon dossier temporaire.
  J’ai regardé `importer_v1.py` : ses tris se font par position (des entiers), il ne devrait donc pas être touché.
- Les figures Chasles (cours, fiche) et produit sont larges (≈ 830 px) : sur téléphone, elles sont un peu
  réduites mais restent lisibles.
- Les lignes `Image:` des exercices 1964, 1960, 1959 et 1958 rappellent les anciens noms de fichiers ; elles sont
  laissées telles quelles, car l’importeur les régénère.

## Vérification des figures 2026-11-02

- **17 figures vues** (19 appels : 6 du cours, 2 de la fiche — reprises du cours —, 11 des exercices), à l'œil et avec le détecteur texte/trait de `figures_livre.py` : 17/17 sans chevauchement ni alerte.
- La session interrompue avait refait 13 figures (alignes, base, coordonnees, produit, ex_alignement, ex_drone, ex_isocele, ex_parallelogramme, ex_translation, n1_enonce, n1_corrige, n2_enonce, n2_corrige) : toutes revérifiées.
- Contrôles mathématiques, figure par figure, contre les énoncés et corrigés : 2u = (4 ; 2) et −1,5u = (−3 ; −1,5) ; u = 3i + 2j ; A(1 ; 1), B(5 ; 4), AB(4 ; 3), I(3 ; 2,5) ; A, B, C alignés avec AC = 3AB ; D(1 ; 6) (1956) ; triangle isocèle en B, M(1 ; 0) (1963) ; D(0 ; −3), I(3 ; 0) (1964) ; k = −7, P(−7 ; −3), (AB) ∥ (CD) (1962) ; AM = AN = 2/5 (1960) ; A(2 ; 1), B(0 ; 5), T(1 ; 2), ST(4 ; 0) (1959) ; BD = BC/3 et D milieu de [AE] (1958) ; AB = CD = (3 ; 2), EF = (−3 ; −2) (3734) ; u + v = (2 ; 3), u − v = (4 ; −1) (3735). Éléments de réponse en vert, style des livres, largeur ≤ 872 px.
- **Défauts trouvés : aucun. Figures refaites dans cette reprise : aucune.**
- Contrôles finaux : `verifier_notion.py --navigateur` sur une copie de travail dont `meta.json` déclare les Id 3734 et 3735 (créés à l'import du 29/10, absents de l'export) : **OK, 0 problème**, contrôle Chrome compris. Captures téléphone des figures refaites regardées.

## Finition 2026-11-02

**État : prêt** (agent-finition-S2). 14 exercices (aucun ajout : la notion en avait déjà 14, tous au programme de Seconde 2019 et justes).

### Figures (12 ajoutées, aucune refaite ni retirée)
- **Corrigés (5 figures, réponse en vert)** : 1966 `ex_somme_colineaire` (u + v par le parallélogramme, w = 2u) ; 1967 `ex_chasles_chemin` (AD + DC + CB = AB) ; 1965 `ex_milieu` (M milieu, AM = MB) ; 1961 `ex_parallele_t_corrige` (D(1 ; −1), (CD) ∥ (AB)) ; 1957 `ex_colineaires` (x = kx′, y = ky′).
- **Énoncés (7 figures, données seules)** : 1956, 1963, 1964, 1962, 1961, 1960, 1958 (points, triangle ou quadrilatère sans le point cherché ni le tracé de la réponse).
- Plus aucun exercice sans figure ; les 7 exercices dont la figure n'était qu'au corrigé ont maintenant aussi leur figure d'énoncé.
- Détecteur texte/trait : 12/12 sans erreur après correction (« O » sur l'axe, « D » sur (CD), graduations coupées par un tracé retirées) ; chaque PNG regardé ; valeurs contrôlées contre les corrigés.

### Titres
- Les 14 titres passent au format « Type - Sujet » (plus de sujet intermédiaire répété) ; « Maîtrise » remplacé par Entraînement (1962, 1961) ou Problème (1960). Répartition : 4 Découverte, 6 Entraînement, 4 Problème. Cours et fiche : intitulé officiel déjà en place.

### Contrôles
- `verif_168.py` : 195 contrôles OK (aucun calcul modifié).
- `verifier_notion.py --navigateur` : **OK, 0 problème**. `controle_apercu.mjs` avec captures : aucun problème ; capture téléphone de 1966 (étapes, nouvelle figure) regardée.
