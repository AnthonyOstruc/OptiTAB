# Notion 180 — Vecteurs, droites et plans de l’espace (Terminale)

**État : prêt.** `verifier_notion.py --navigateur` : OK (0 problème) ; captures téléphone/ordinateur regardées (cours, fiche, exercices).

## Texte
- Cours réécrit et complété (ancien, très mince) : vecteurs, combinaisons linéaires, droites, plans, vecteurs coplanaires (caractérisation + méthode), bases et repères, calculs en coordonnées, positions relatives (deux droites, droite/plan, deux plans), théorème du toit avec démonstration vectorielle, section d’un cube (méthode + exemple). Fiche refaite (tableau natif des positions relatives, pièges).
- Exercices : rédaction pédagogique complète (méthode / étapes / résultat), notation française des points $A(1\,;2\,;3)$, doublons de « résultat » supprimés.
- **Erreurs de fond corrigées :**
  - 1098 et 1101 : la « loi des toits » était appliquée à tort (simple transitivité du parallélisme). 1101 Q4 reformulée (droites parallèles à une même troisième) ; 1098 Q5 remplacée par une vraie application du théorème du toit (plans (ADG) et (BCE), Δ parallèle à (BC) par K), comme dans le livre Terminale.
  - 1102 (section du cube) : I, J, K n’étaient pas définis précisément (la section n’est pas toujours un hexagone) → milieux de [AD], [AE], [FG] (version du livre) ; le point S « sur [BF] » était faux (hors du cube) ; construction refaite par les faces parallèles.
  - 1104 : « supposer les arêtes de longueur 1 » remplacé par l’explication correcte (repère non orthonormé, coordonnées identiques).
  - 1097 Q5, 1095 : vocabulaire hors programme (« linéairement indépendants ») remplacé par la méthode du programme.
- Tous les résultats vérifiés en calcul exact : `verif_vecteurs_espace.py` → « TOUT EST JUSTE ».

## Figures (TikZ, perspective cavalière des livres, arêtes cachées en pointillés, étiquettes placées automatiquement hors des traits)
- 19 images en ligne : toutes refaites ou remplacées (0 conservée, 0 retirée sans remplacement).
- 23 figures produites, 26 emplacements : cours 9 (6 ajoutées), fiche 2, exercices 15 (dont 1 ajoutée : 1098 Q5, plans du toit dans le cube).

## Finition 2026-11-02

**État : prêt** (agent-finition-T5). 12 exercices (aucun ajouté : la notion couvre les capacités du programme).

### Titres
- Cours et fiche : intitulé officiel « Manipulation des vecteurs, des droites et des plans de l’espace » (fiche : « Résumé : … »).
- 8 titres d’exercices : « Combinaisons linéaires et indépendance » → « Combinaisons linéaires de vecteurs » (vocabulaire hors programme) ; « Coplanarité de points et de vecteurs » → « Coplanarité de quatre points » ; « Configuration dans un cube » → « Repère et coplanarité dans un cube » ; « loi des toits » → « théorème du toit » ; « Section d’un cube par un plan $(IJK)$ » → « … par un plan passant par trois milieux » (pas de formule dans un titre) ; les trois « Type Bac - … » → « Type bac - Quatre points non coplanaires : un tétraèdre », « … Positions relatives de deux droites et d’un plan », « … Vecteurs coplanaires dans un pavé droit ».

### Exercices
- Les 12 relus : justes, au programme, complets ; aucun à réécrire. Ajouts de texte liés aux nouvelles figures : lecture du chemin $+3$, $-3$, $+2$ (1093), construction de $\vec{w}$ et candidat $3\vec{u} + 2\vec{v}(3\,;8\,;2) \neq \vec{t}$ (1095), bilan des questions 5 à 7 (1100).

### Figures (outil commun `figures/espace.py` : parties cachées calculées, étiquettes placées hors des traits)
- **Revérifiées** : les 23 existantes (détecteur + à l’œil) : justes et lisibles, conservées.
- **Ajoutées (9 fichiers, 12 emplacements)** — les 6 exercices qui n’en avaient pas :
  - 1093 Q5 : pavé 3 × 3 × 2, chemin $A \to B$ ($+3$, $-3$, $+2$) et $\overrightarrow{AB}$ en vert, trièdre $x, y, z$ ;
  - 1094 Q4 : $A$, $C$, $B$ alignés, codage $AC = CB$, $\overrightarrow{AC}$ en vert ;
  - 1095 Q3 et Q5 : plan dirigé par $\vec{u}$, $\vec{v}$, $\vec{w} = 2\vec{u} + \vec{v}$ en vert ; puis $\vec{t}$ (orange) qui sort du plan ;
  - 1096 Q4 et Q5 : parallélogramme $ABDC$ dans $(ABC)$ ; puis $E$ hors du plan ;
  - 1099 Q5 : plan $(ABC)$ et tétraèdre $ABCD$ (arêtes issues de $D$ en vert, $[AC]$ cachée) ;
  - 1100 Q5, Q6 et Q7 : $(d_1)$ strictement parallèle à $\mathcal{P}$ ; $(d_2)$ (vert) qui perce $\mathcal{P}$ en $M$, partie cachée en pointillés.
  - fiche : figure du cube « parallèles / non coplanaires » ajoutée sous le tableau des positions relatives.
- Aucune figure retirée.

### Contrôles
- `verif_vecteurs_espace.py` : TOUT EST JUSTE (102 contrôles, 10 ajoutés pour les valeurs des nouvelles figures et textes).
- `figures_livre.py` : 32/32 figures, 0 erreur, 0 avertissement ; chaque PNG regardé (planches + pleine taille).
- `verifier_notion.py --navigateur` : OK, 0 problème. `controle_apercu.mjs` avec captures : captures téléphone regardées (1093, 1100, fiche) ; 8 formules « X, soit Y » réduites sur téléphone allégées (le résultat encadré redonne Y). Chrome est resté bloqué à la fermeture après la dernière capture (défaut connu) : seul mon processus a été arrêté et son verrou libéré.

## Remarques pour l’orchestrateur
- Les lignes `Image:` des en-têtes d’exercices sont celles de l’export (non modifiées) ; la correspondance fait foi.
- figures_livre.py : un point dessiné en `\node` disparaît dans la version « sans texte » et fausse le contrôle (faux « texte sur un trait ») → points tracés en `\fill … circle`.
