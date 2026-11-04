# Notion 239 — Grandeurs et mesures (3e)

**État : prêt** (agent-3e-C5, 2026-11-03).

## Cours et fiche

- **Titres** : « Grandeurs composées et conversions » → « Grandeurs et mesures » (cours) et « Résumé : Grandeurs et mesures » (fiche).
- **Programme** : l'ancien cours ne traitait que les conversions et les grandeurs composées. Ajouté (attendus de fin de 3e) : **volumes des solides** (pavé, prisme, cylindre, pyramide, cône, boule, aire de la sphère) et **effet d'un agrandissement / d'une réduction** sur longueurs, aires ($k^2$) et volumes ($k^3$).
- **Cours réécrit** : I. conversions (facteurs, tableau de conversion des aires, contenances, durées en base 60) ; II. volumes des solides (propriétés, deux figures de solides, exemple du cône, erreurs) ; III. agrandissement et réduction ; IV. grandeurs composées (vitesse, graphique distance-temps, conversion km/h ↔ m/s justifiée, vitesse moyenne d'un trajet ; débit, masse volumique, énergie) ; V. contrôler un résultat ; à retenir.
- **Fiche refaite** : tableau des conversions, tableau de conversion des aires, tableau des volumes, rapport $k$, formules des grandeurs composées, 5 erreurs classiques.

## Exercices (21)

- Tous relus et **réécrits** : méthode, étapes détaillées, résultat encadré, **erreur fréquente** dans chaque exercice ; `\displaystyle` retirés, fractions en `\dfrac`.
- **Titres** « Type - Grandeurs - n. Sujet » → « Type - Sujet ».
- **Remplacés (5)** — doublons ou exercices faibles, remplacés pour couvrir tout le programme :
  - 2259 « Masses et tonnes » (conversions seules) → « Découverte - Volumes d'un pavé et d'un cylindre » (figure) ;
  - 2260 « Chasse aux pièges » (doublon de 2254–2256) → « Découverte - Volumes d'une pyramide et d'un cône » (figure, comparaison avec le pavé) ;
  - 2266 « Distance, vitesse, durée » (doublon de 2257) → « Entraînement - Lire un graphique distance-temps » (énoncé + corrigé annoté) ;
  - 2267 « Un record de sprint » (doublon de 2261) → « Entraînement - Agrandissement et réduction » (aquarium, $k^2$ et $k^3$) ;
  - 2274 « La traversée en train » (doublon de 2268) → « Type brevet - Un verre conique » (volume du cône, réduction de rapport $\frac{1}{2}$, $\frac{1}{8}$ du volume ; figure énoncé + corrigé).
- **Retravaillés** : 2254 (km² → m², tableau au corrigé) ; 2255 (m³ → dm³) ; 2263 (marbre : identifier un matériau) ; 2269 (vérification avec les débits en L/min) ; 2271 (coût de la fuite) ; 2273 (jour et heure de fin du remplissage, figure).
- Progression : 7 Découverte, 7 Entraînement, 5 Problème, 2 **Type brevet** (2273, 2274).

## Figures (13 PNG, style livre, aucune ancienne image conservée)

- **Refaite (1 image en ligne)** : vitesse du cours et de la fiche → graphique distance-temps (cours) et tableau de conversion des aires (fiche).
- **Ajoutées** : tableau de conversion des aires (cours, fiche, corrigé 2254, zéros ajoutés en vert) ; pavé et cylindre, pyramide, cône et boule (cours) ; solides cotés de 2259 et 2260 ; piscine 2273 ; graphique distance-temps 2266 (énoncé + corrigé avec vitesses en vert) ; verre conique 2274 (énoncé + corrigé avec le rayon de 2 cm en vert).
- `figures_livre.py` : 0 chevauchement, 0 refus (3 figures à 903–941 px, sous la limite de 1 100 px).

## Contrôles

- `verif_239.py` : **34 contrôles** sympy (valeurs exactes), tout juste.
- `verifier_notion.py --navigateur` : **OK, 0 problème**.
- `controle_apercu.mjs` (version finale, captures téléphone + ordinateur) : **130 vues, toutes à 0**. Chrome bloqué à la fermeture lors d'une seconde passe : contrôle refait comme pour 240 (vérificateur sans navigateur OK + `controle_apercu.mjs` seul), mes seuls processus et verrous arrêtés. Captures regardées : cours (parties I à IV), exercices 2266 et 2274. Corrigé après captures : tableau de conversion trop petit sur téléphone (réduit à 4 unités, agrandi), fractions en ligne illisibles (`\dfrac`), formules de la fiche sur deux lignes.

## Remarques pour l'orchestrateur

- Les figures de solides du cours sont larges (trois solides côte à côte) : lisibles sur téléphone mais petites ; à scinder si le propriétaire le souhaite.
