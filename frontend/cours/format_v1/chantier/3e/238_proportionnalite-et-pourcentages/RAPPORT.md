# Notion 238 (3e) : Proportionnalité et pourcentages

**État : prêt** (agent-3e-C4, 2026-11-03).

Programme du cycle 4 : reconnaître la proportionnalité (tableau, graphique), quatrième proportionnelle, ratios, échelles, pourcentages, coefficient multiplicateur, valeur initiale, pourcentage d'évolution, évolutions successives.

## Texte
- **Titres** : cours « Proportionnalité, ratios et pourcentages » → « Proportionnalité et pourcentages » ; fiche → « Résumé : Proportionnalité et pourcentages » (à appliquer avec `titres_docs.py`).
- **Cours 233** : réécrit. I. Reconnaître (tableau avec figure du coefficient, graphique avec droite par l'origine et contre-exemple à partie fixe) ; II. Quatrième proportionnelle (passage à l'unité, coefficient, produit en croix, exemple) ; III. Ratios et échelles ; IV. Pourcentages, coefficient multiplicateur (figure aller-retour $\times 1{,}08$ / $\div 1{,}08$), valeur initiale et piège de la référence ; V. Pourcentage d'évolution, évolutions successives (figure), points ou pourcentage.
- **Fiche 153** : réécrite (puces « • » de la conversion supprimées, tableau des coefficients, 5 erreurs classiques, réflexe brevet).
- **Exercices** : les 21 réécrits au format complet (méthode, étapes, résultat, erreur fréquente, solution). Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 Type brevet.
  - **Remplacé** (même Id) : 2245 « Augmentations successives » (doublon de 2241 et 2253) → « Entraînement - Lire la proportionnalité sur un graphique » (droite par l'origine, droite qui n'y passe pas, courbe ; lecture du coefficient).
  - **Restructurés** : questions de remplissage fusionnées (3 à 5 vraies questions par exercice) ; 2233 complété par un tableau à remplir ; 2235 : question sur le calcul d'un pourcentage (partie / total) ajoutée ; 2234 : le tableau en image devient un tableau natif ; 2247 : prix équivalent obtenu par une équation ($p - 30 = 0{,}8p - 10$).
  - **Type brevet** : 2251 « TVA et soldes » ($\times 1{,}2 \times 0{,}7 = 0{,}84$) et 2253 « L'évolution d'une audience » ($-20\ \%$ puis $+20\ \%$ = $-4\ \%$).
  - Aucune erreur de calcul dans les résultats en ligne.
- `verif_238.py` : **114 contrôles sympy exacts OK** (rationnels exacts, chaque pourcentage, coefficient, échelle et contre-exemple).

## Figures
- **15 figures neuves** pour **18 positions** ; les 3 images en ligne (matplotlib : graphique du cours et de la fiche, tableau 2234) sont remplacées ; 0 conservée.
  - Cours (4) : tableau de proportionnalité ($\times 3{,}5$), graphique proportionnel / non proportionnel, coefficient multiplicateur aller-retour, évolutions successives. Fiche (3) : tableau, graphique, coefficient.
  - Exercices : 2237 (barre du ratio, énoncé et corrigé), 2245 (graphique, énoncé et corrigé) ; corrigés en vert : 2234 (tableau), 2236 (coefficients), 2238 (droite de consommation), 2240 (aller-retour), 2241 (baisses successives), 2243 (tarif à partie fixe), 2253 (audience).
- Détecteur texte/trait : 0 erreur. Toutes ≤ 900 px sauf cours_graphique (≈ 950 px, sous la limite de 1100 px). Chaque PNG regardé.

## Contrôles
- `verifier_notion.py` : **OK, 0 problème**. Avec `--navigateur`, Chrome est resté bloqué à la fermeture (« contrôle navigateur en échec » avec tous les compteurs à 0) : contrôle refait avec `controle_apercu.mjs` (captures) puis `--rapide` après les dernières retouches : **130 vues, 0 débordement, 0 erreur de formule, 0 image manquante**. Seul mon processus node (PID 20840) a été arrêté, après la dernière capture.
- Vues regardées sur téléphone : cours (parties I à IV), fiche, exercices 2233 et 2245 (étapes). Corrections faites après ces vues : en-tête « Nombre de cahiers » trop long (tableau de 2233) raccourci ; ligne « ratio » de la fiche réécrite (deux-points ambigus).

## Remarques pour l'orchestrateur
- Appliquer les nouveaux titres du cours et de la fiche (`titres_docs.py`).
- Les évolutions successives et le pourcentage d'évolution sont traités comme dans les sujets de brevet (coefficients multiplicateurs), sans formule de taux réciproque.
