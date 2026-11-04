# Notion 244 (3e) : Théorème de Pythagore

**État : prêt** (agent-3e-C1, 2026-11-03).

Programme du cycle 4 : théorème de Pythagore, réciproque, triangle non rectangle (égalité fausse), calculs de longueurs (valeur exacte avec la racine carrée, arrondi), situations concrètes, repère orthonormé et espace.

## Texte
- **Titres** : cours et fiche s'appelaient « Théorème de Pythagore et distances » ; ramenés à l'intitulé de la notion : « Théorème de Pythagore » et « Résumé : Théorème de Pythagore » (à appliquer en base avec `titres_docs.py`).
- **Cours 239** : réécrit (il était très court et ses exemples étaient rangés dans des encadrés `definition`).
  - I. Hypoténuse, théorème, figure des carrés, **démonstration par les aires ajoutée** (carré de côté $a + b$, figure).
  - II. Méthode (additionner / soustraire), trois exemples rédigés en `aligned` (hypoténuse, côté de l'angle droit, valeur exacte $\sqrt{65}$), erreurs fréquentes.
  - III. Réciproque, propriété « triangle non rectangle », méthode, deux exemples, piège de rédaction.
  - IV. Angles droits concrets, repère orthonormé (figure), espace (figure du pavé), `retenir`.
  - La « formule » de distance dans un repère n'est plus présentée comme une formule générale (Seconde) : on construit le triangle rectangle.
- **Fiche 159** : réécrite (puces « • » de la conversion supprimées ; tableau additionner / soustraire ; méthode de la réciproque ; où trouver un angle droit ; 5 erreurs classiques).
- **Exercices** : les 21 sont réécrits au format complet (méthode, étapes, résultat, erreur fréquente, solution). Questions de remplissage supprimées (périmètres et aires sans intérêt, « vérifier la cohérence » sans contenu), questions regroupées en 3 ou 4 vraies questions. Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 Type brevet.
  - **Remplacés** (même Id) :
    - 2365 « Carrés et racines en série » (calculs sans figure ni contexte) → « Découverte - Additionner ou soustraire ? » (trois triangles rectangles, l'hypoténuse cherchée ou connue) ;
    - 2372 « Un triangle dans un repère » (doublon exact de 2368 : triangle 6-8-10 dans un repère) → « Entraînement - Rectangle ou presque rectangle ? » ($28{,}09 = 28{,}09$ mais $46{,}24 \neq 46{,}25$ : le dessin ne peut pas trancher) ;
    - 2369 : données 6-8-10 (déjà vues 4 fois) → $7{,}5$ ; $4{,}5$ ; $6$, angle droit en $C$, hauteur $CH = 3{,}6$ cm par deux calculs d'aire.
  - **Valeurs exactes** : diagonales du carré et du cube données en $\sqrt{450}$, $\sqrt{200}$, $\sqrt{300}$ (la simplification $15\sqrt{2}$, $10\sqrt{3}$ n'est pas un attendu de 3e).
  - **Type brevet** : 2373 (rampe : Pythagore, pente, norme de $5\ \%$) et 2378 (écran : diagonale, pouces, format $16/9$, aire en m²).
  - Aucune erreur de calcul dans les résultats en ligne.
- `verif_244.py` : **89 contrôles sympy OK** (chaque carré, racine, arrondi, aire, durée ; preuve par les aires).

## Figures
- **45 figures neuves** pour **48 positions** ; les 8 images en ligne (matplotlib) sont toutes remplacées ; 0 conservée.
  - Cours (4) : carrés sur les côtés, démonstration par les aires, distance dans un repère, pavé droit. Fiche (2) : carrés, repère.
  - Exercices : figure d'énoncé (sans la réponse) **et** figure de corrigé (réponse en vert) pour les **21** exercices.
- Détecteur texte/trait : 0 erreur ; seules alertes : cotes à fond blanc. Toutes ≤ 900 px sauf ex2365 (945 px, trois triangles côte à côte, sous la limite de 1100 px). Chaque PNG regardé.

## Contrôles
- `verifier_notion.py --navigateur` : **OK, 0 problème**.
- `controle_apercu.mjs` avec captures : toutes les vues sans défaut (0 débordement, 0 erreur de formule, 0 image manquante) ; Chrome est resté bloqué à la fermeture : seul mon processus (PID 41500) a été arrêté, après la dernière capture.
- Vues regardées sur téléphone : cours (parties I à III), fiche, exercices 2369 et 2378 (étapes). Corrections faites après ces vues : colonne « Exemple » du tableau de la fiche coupée → tableau à deux colonnes et exemples en encadré ; conversion cm² → m² de 2378 (« = » rejeté en début de ligne) → formule centrée.
- Calculs en chaîne écrits en `aligned` (une égalité par ligne) pour éviter les formules réduites sur téléphone (2369, 2372 notamment).

## Remarques pour l'orchestrateur
- Appliquer les nouveaux titres du cours et de la fiche (`titres_docs.py`).
