# Notion 289 (4e) : Pyramides, cônes et volumes

**État : prêt** (agent-289, 2026-11-04). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée ; 2 exercices remplacés, 3 refondus, les 16 autres réécrits). Aucune écriture en base, aucun git.

Programme de 4e (cycle 4) : pyramide et cône de révolution (vocabulaire, perspective cavalière, patrons) ; volume $\frac{1}{3} \times \mathcal{B} \times h$ ; rappels pavé droit, prisme droit, cylindre ; conversions de volumes et de contenances ; Pythagore pour une hauteur, une génératrice, une arête ou la hauteur d'une face ; repérage dans un pavé droit. Le cosinus (4e) sert dans 2 exercices, Thalès en triangles emboîtés (4e) dans 1. Sphère, sections planes et effet $k^3$ (3e) : **aucune mention** (le verre à cocktail calcule directement le petit cône, sans propriété de réduction).

## Cours 288 et fiche 223

- **Titres** inchangés : « Pyramides, cônes et volumes » et « Résumé : Pyramides, cônes et volumes ».
- **Cours réécrit** façon manuel (l'ancien : 4 parties courtes, formule rangée dans un encadré `definition`, renvoi « onglet Fiches », exemples identiques aux exercices 3694 et 3695) : objectifs et prérequis ; I. rappels pavé / prisme droit / cylindre ($V = \mathcal{B} \times h$, exemple $28\pi$, piège de la base du prisme) ; II. pyramide (définition, régulière, propriété $n + 1$ faces, $2n$ arêtes, exemple hexagonal, tétraèdre et hauteur-arête) ; III. cône (révolution du triangle $SOA$, $SA^2 = SO^2 + OA^2$, exemple 5-12-13) ; IV. perspective cavalière (méthode en 4 points) et patrons (pyramide, cône) ; V. volume (propriété, origine du tiers, deux exemples, méthode « hauteur inconnue » avec exemple génératrice 10 / rayon 6, $h = \frac{3V}{\mathcal{B}}$, erreurs fréquentes) ; VI. unités et contenances (tableau natif à la place de l'image) ; VII. repère d'un pavé ($M(3 ; 1 ; 2)$) ; « À retenir ». Exemples tous différents des exercices.
- **Fiche refaite** : vocabulaire + figure, $SA^2 = SO^2 + OA^2$, tableau des volumes, figure du tiers, conversions, repérage, 5 erreurs classiques, réflexe.

## Exercices (21)

- **Progression** dans l'ordre des Id : 7 Découverte (3692-3698), 7 Entraînement (3699-3705), 5 Problème (3706-3710), **2 Type brevet** (3711-3712 ; il n'y en avait aucun). Titres « Type - Espace - n. Sujet » → « Type - Sujet » (21).
- **Tous relus et réécrits** : questions numérotées ; corrigé avec méthode, étapes détaillées (calculs en `aligned`), résultat encadré à chaque question, « Erreur fréquente » (encadré `attention`) dans les 21, « À retenir » quand utile ; `Solution:` courte et cohérente. Retirés : `\displaystyle`, « **Erreur fréquente :** » en gras hors encadré, lignes `Image:`, étapes cassées par la conversion (formule prise pour titre d'étape).
- **Remplacés (même Id)** :
  - 3703 « Solides emboîtés » (doublon des questions « tiers du pavé / du cylindre » de 3694 et 3695) → « Entraînement - Choisir la bonne formule de volume » : pavé, prisme couché (piège de la base), cylindre, pyramide ; rappels du programme, classement ($48 = 48 < 60 < 20\pi$).
  - 3705 « La tente » (même déroulé que le Louvre : $OH$, $SH$, aire des faces) → « Entraînement - Se repérer dans un pavé droit » (compétence du programme absente) : coordonnées, centre d'une face, pyramide $SOABC$ et tiers du pavé.
- **Retouches de contenu** : 3692, la relation d'Euler (hors programme) est remplacée par une question sur la perspective cavalière (pourquoi la base carrée devient un parallélogramme).
- **Refondus** : 3709 « La grande pyramide » (troisième calcul de $SH$ après le Louvre et la tente) → diagonale de la base, demi-diagonale $OA$ et arête $SA$ (double Pythagore) ; 3711 et 3712 passés en **Type brevet** (document, prix au kilogramme, affirmation du fabricant à vérifier) ; 3693 (question sur la révolution du triangle).
- **Erreur de données corrigée** : 3704 donnait une base de $6 \times 4$ cm, une hauteur de $5$ cm et des arêtes latérales de $7$ cm : impossible (l'arête vaut alors $\sqrt{38} \approx 6{,}2$ cm). Données refaites cohérentes : base $8 \times 6$, hauteur $12$, arête $13$ cm (vérifié), volumes $192$ / $576$ / $112$ / $208$ cm³.
- **Valeurs précisées** : 3708 Q6 « environ 80 % » → $79{,}6$ % ; 3706 erreur fréquente fausse (« diviser par 2 au lieu de 0,5 ») → « multiplier par 0,5 au lieu de diviser » ; 3710 Q6 : reste de 5 t justifié.
- Espaces insécables entre nombre et unité : 546 (cours 49, fiche 16, exercices 481).
- `verif_289.py` : **222 contrôles sympy**, tous justes (chaque volume, aire, longueur, arrondi, conversion, angle du cours, de la fiche et des 21 corrigés ; cohérence des données des figures : sable à $0{,}8^{1/3}$ de la hauteur, hauteur du gobelet $\sqrt{68{,}75}$).

## Figures (style livre, `figures/figures.py`)

- **53 figures neuves** pour **55 positions** ; les **36 images matplotlib en ligne sont toutes remplacées** (0 conservée, 0 non appelée). L'image du tableau de conversions du cours devient un tableau natif.
- Moteur de perspective cavalière (40°, coefficient 0,6) : les faces visibles d'un solide convexe sont **calculées** (normale extérieure vers l'observateur), donc toutes les arêtes cachées sont en pointillés sans erreur possible ; cônes avec les vraies tangentes à l'ellipse de base, moitié arrière en pointillés.
- Cours (8) : solides droits, vocabulaire de la pyramide et du cône (légendes avec traits de rappel), patrons (pyramide, cône), tiers du prisme et du cylindre, exemple de cône (hauteur en vert), décimètre cube quadrillé ($1$ dm³ $= 1\,000$ cm³ $= 1$ L), repère avec le trajet vert vers $M$. Fiche (2).
- Exercices : figure d'énoncé (données en orange, sans la réponse) **et** figure de corrigé (élément cherché en vert) pour les 21 exercices. Pour 3696, 3699 et 3709, le corrigé redessine **en vraie grandeur**, dans une seconde figure, le triangle rectangle utilisé (base $ABC$, triangle $SOH$, triangle $SOA$), coloré dans le solide (d'abord côte à côte, séparés après la relecture des captures téléphone, où le texte était trop petit).
- `figures_livre.py` : 0 texte sur un trait, aucune tolérance (`TOLERE` vide) ; toutes ≤ 906 px. Chaque PNG regardé (planches) ; corrections après relecture : étiquettes passées à l'extérieur des solides (« $SO = …$ » à gauche de l'arête), tétraèdre réorienté (deux faces visibles au lieu d'une), noms $O$ et $D$ déplacés hors des pointillés, sablier sans planches décoratives.

## Contrôles

- `verif_289.py` : 222 contrôles justes.
- `verifier_notion.py --navigateur` : **OK** (55 positions de figures, 0 image en ligne conservée ; notes : 21 titres changés, voulu).
- `controle_apercu.mjs` avec captures : toutes les vues à 0 (débordement, formule, `$` brut, image, largeur) ; Chrome est resté bloqué à la fermeture après la dernière vue (cas connu) : seul mon processus `node` (42104) a été arrêté et mon verrou `chrome_0.lock` retiré.
- **Captures téléphone regardées** (deux passes groupées) : cours en entier (6 vues), fiche (2), corrigés 3699, 3709, 3711. Formules entières, tableaux lisibles. Correction faite : les corrigés 3696, 3699 et 3709 (solide + triangle côte à côte) étaient trop réduits sur téléphone → deux figures séparées, plus grandes.
- Sauvegardes : `sauvegardes/289_*_conversion_auto.txt`.

## Remarques pour l'orchestrateur

- Aucune remarque d'outil ou de moteur (une compilation LuaTeX « sans texte » a échoué une fois au démarrage, erreur passagère du cache partagé ; recompilée sans problème).
