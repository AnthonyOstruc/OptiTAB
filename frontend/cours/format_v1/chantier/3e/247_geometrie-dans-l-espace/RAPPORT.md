# Notion 247 — Géométrie dans l'espace (3e)

**État : prêt** (agent-3e-247, 2026-11-03).

## Cours et fiche

- **Titres** inchangés (déjà l'intitulé du programme) : « Géométrie dans l'espace » et « Résumé : Géométrie dans l'espace ».
- **Cours réécrit** (façon manuel, programme du cycle 4) : I. solides usuels (vocabulaire, pavé, cube, prisme droit, cylindre, pyramide, cône, sphère et boule, hauteur perpendiculaire à la base) ; II. représenter un solide (méthode de la perspective cavalière, patrons du pavé, du cube — 11 patrons — et du cylindre avec exemple $2\pi r$) ; III. volumes et aires (tableau, aire de la sphère, unités de volume et contenances, exemple du cône, méthode des solides composés, erreurs) ; IV. sections planes du pavé, du cylindre (parallèle à la base et à l'axe), de la pyramide, du cône et de la sphère ($r^2 = R^2 - d^2$, grand cercle) ; V. agrandissement-réduction ($k$, $k^2$, $k^3$, deux exemples) ; VI. repérage dans un pavé ($M(3 ; 2 ; 2)$) et sur la sphère terrestre (équateur, méridiens, parallèles, latitude, longitude, écarts de longitude) ; « À retenir ».
- **Fiche refaite** : tableau des volumes, aire de la sphère, conversions, tableau des sections planes, formule de la section de sphère, rapport $k$, repérage, 5 erreurs classiques, réflexe brevet.
- `\displaystyle` retirés, fractions en `\dfrac`, degrés en `^\circ` dans les formules.

## Exercices (21 + 1 ajouté = 22)

- Tous **réécrits** : méthode, étapes détaillées (calculs alignés), résultat encadré, **erreur fréquente** dans chaque exercice (+ « À retenir » quand utile) ; titres « Type - Espace - n. Sujet » → « Type - Sujet ».
- **Remplacé (1)** : 2428 « Les trois vues » (doublon de 2422 : même pavé, mêmes aires) → « Découverte - Le patron d'un cylindre » (longueur $2\pi r$, aires latérale et totale, volume, section par un plan contenant l'axe).
- **Corrigé (1)** : 2437 Q5 comparait un volume (216 cm³) et une aire (216 cm²) — non-sens d'unités → boule inscrite dans le cube ($\frac{\pi}{6} \approx 52{,}4$ %).
- **Ajouté (1)** : `nouveau-1` « Type brevet - Une pyramide coupée par un plan » (section d'une pyramide, $k = \frac{1}{3}$, $k^2$, $k^3$ vérifié par la formule, tronc $\frac{26}{27}$) : la section de pyramide n'était travaillée nulle part.
- **Type brevet** : 2441 (verre conique) et 2442 (aquarium) passent de « Problème » à « Type brevet » (même contenu enrichi).
- Retravaillés : 2427 (règle des faces opposées), 2431 (écarts de longitude E/O), 2433 (durée en h min), 2436 (arrondi à l'entier supérieur des camions), 2440 (énoncé avec deux villes $V_1$, $V_2$ et figure).
- Progression : 7 Découverte, 7 Entraînement, 5 Problème, 3 **Type brevet**.

## Figures (39 PNG, style livre, aucune ancienne image conservée)

- **Refaites (toutes les images matplotlib en ligne, 26 emplacements)** : solides, sections, repère, globe (cours) ; solides (fiche) ; toutes les figures d'exercices.
- **Ajoutées** : patron du cylindre et sections pyramide/cône, section de sphère (cours) ; 3 figures de la fiche ; **figures de corrigé en vert** pour 2427 (faces opposées colorées), 2428 ($L = 4\pi$), 2429 (section $IJKL$), 2432 (rayon 4 cm), 2435 (section de rayon 3 cm), 2437 (triangle $AFG$ rectangle en $F$), 2439 (triangle $SOI$, $SI$), 2440 (arc de 30°), 2441 (rayon $\frac{10}{3}$ cm), `nouveau-1` (section, $k$).
- Perspective cavalière (40°, coefficient 0,6), arêtes cachées en pointillés, données en orange dans les énoncés, sphères avec équateur et méridien de Greenwich, patrons nets.
- `figures_livre.py` : 0 chevauchement, 0 refus.

## Contrôles

- `verif_247.py` : **154 contrôles** sympy (valeurs exactes et arrondis écrits dans les corrigés), tout juste.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (0 image en ligne conservée, 26 emplacements remplacés).
- `controle_apercu.mjs` (captures téléphone + ordinateur) : **« Aucun problème détecté »**, toutes les vues à 0 (débordement, formules, images, largeur). Captures regardées : cours (parties II, IV-VI), fiche, corrigés 2437 et `nouveau-1` en téléphone.

## Remarques pour l'orchestrateur

- `nouveau-1` à relier par `relier_nouveaux.py` (publier_lot.ps1 le fait).
- Pyramide coupée (`nouveau-1`) : le point $O'$ est marqué sur $[SO]$ mais non nommé sur la figure (place insuffisante) ; l'énoncé le définit.
