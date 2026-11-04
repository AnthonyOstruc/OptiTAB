# Notion 282 (4e) : Construire et comparer des triangles

**État : prêt** (claude-282, 2026-11-04). 21 exercices (aucun ajout, aucun bloc supprimé, aucune ligne `Id:` modifiée ; 5 exercices remplacés). Aucune écriture en base, aucun git.

Programme de 4e (cycle 4) : inégalité triangulaire et construction possible ; constructions (trois côtés ; deux côtés et l'angle compris ; un côté et les deux angles adjacents) ; somme des angles ; triangles particuliers ; triangles égaux (cas d'égalité) ; triangles semblables au niveau 4e (angles égaux, longueurs proportionnelles, sans le formalisme $k$, $k^2$, $k^3$ de 3e) ; médiatrices, hauteurs, cercle circonscrit ; démonstrations courtes « On sait que… Or… Donc… ». Thalès et Pythagore ne sont pas utilisés (notions 283 et 286).

## Cours 277 et fiche 197

- **Titres** inchangés : « Construire et comparer des triangles » et « Résumé : Construire et comparer des triangles ».
- **Cours réécrit** (l'ancien ne traitait que l'inégalité, les constructions et les cas d'égalité ; ni triangles particuliers, ni médiatrices, ni hauteurs, ni cercle circonscrit, ni triangles semblables ; renvoi « onglet Fiches ») : objectifs ; I. inégalité triangulaire (propriété, cas d'égalité = aplati, méthode « tester la plus grande », exemple, erreur fréquente) ; II. somme des angles (démonstration par les alternes-internes), tableau des triangles particuliers, réciproque « deux angles égaux ⇒ isocèle » ; III. trois méthodes de construction (données différentes de celles des exercices), « à retenir » (triangle unique), piège de l'angle non compris ; IV. médiatrice (définition, équidistance et réciproque, construction au compas), cercle circonscrit avec sa démonstration, hauteurs (cas obtus), aire ; V. triangles égaux (définition, notation dans l'ordre de la correspondance, trois cas, méthode, pièges) ; VI. triangles semblables (définition, deux angles suffisent, longueurs proportionnelles, exemple en tableau, égaux / semblables) ; VII. rédaction « On sait que… Or… Donc… » avec un exemple rédigé et un tableau « Pour démontrer que… » ; « à retenir » final.
- **Fiche réécrite** : existence et angles, triangles particuliers, constructions (tableau), médiatrices et hauteurs, tableau comparatif égaux / semblables, rédaction, 5 erreurs classiques, réflexe.

## Exercices (21)

- **Progression** dans l'ordre des Id : 7 Découverte (3146-3152), 7 Entraînement (3153-3159), 5 Problème (3160-3164), 2 **Type brevet** (3165-3166 ; il n'y en avait aucun). Titres « Type - Triangles - n. Sujet » → « Type - Sujet » (21).
- **Tous relus et réécrits** : 6 questions numérotées chacun ; corrigé avec méthode (21/21), étapes détaillées (démonstrations rédigées « On sait que / Or / Donc »), résultat encadré à chaque question (126/126), « Erreur fréquente » dans 21/21, « À retenir » quand utile ; `Solution:` courte et cohérente. `\displaystyle`, lignes `Image:`, « **À retenir :** » en gras, majuscules d'insistance retirés ; étapes cassées par la conversion réparées (« il faut $9 3$ », « $x 1$ », formules prises pour titres d'étape).
- **Remplacés (5)**, pour couvrir le programme :
  - 3155 « Le cerf-volant » (doublon de 3161 et 3165 : diagonale commune, bissectrice) → « Entraînement - Médiatrices et cercle circonscrit » (construction au compas, démonstration $OA = OB = OC$, troisième médiatrice, rayon ≈ 3,6 cm) ;
  - 3158 « Un programme de construction » (doublon de 3148 et 3151) → « Entraînement - Tracer les hauteurs d'un triangle » (aire avec deux bases, $BK = 4{,}8$ cm, concours des hauteurs, cas obtus) ;
  - 3159 « Des constructions impossibles » (doublon de 3146 et 3157) → « Entraînement - Reconnaître des triangles semblables » (angles ; côtés proportionnels avec le piège du 3e quotient) ;
  - 3161 « Les angles d'un losange » (troisième « diagonale commune » après 3153 et 3155) → « Problème - La hauteur d'un arbre grâce aux ombres » (angles correspondants, triangles semblables, coefficient 5, arbre de 6 m) ;
  - 3163 « Distances entre villes » (encore l'inégalité triangulaire) → « Problème - Une antenne à égale distance de trois villages » (médiatrices sur quadrillage, 5 km, portée 6 km).
- **Enrichis** : 3150 (correspondance non alphabétique : $ABC$ et $EFD$), 3147 (angle mesuré au lieu d'un périmètre trivial), 3164 (cas 0 / 1 solution dessinés), 3165 (parties A, B, C : triangles égaux, **médiatrice**, toile et prix), 3166 (M sur la médiatrice de $[DC]$), 3153 (vérification 360° expliquée).
- **Erreurs corrigées** : 3150 (angles « 78° et 57° » incompatibles avec les côtés 5, 6, 7 : $180 - 78 - 57 = 45$ alors que le vrai angle vaut 44,4° → triangle 5, 6, 4 aux angles 83°, 41°, 56° exacts au degré) ; 3162 (périmètre « $3 \times 3{,}5 \approx 10{,}4$ » → $10{,}5$ cm, cohérent avec la mesure) ; 3146 Q5 et 3159 Q6 (étapes illisibles).

## Figures (style livre, `figures/figures.py`)

- **54 figures neuves** pour **57 positions** ; les **22 images matplotlib en ligne sont toutes remplacées** (0 conservée).
  - Cours (12) : inégalité (arcs qui se coupent / se touchent / ne se rencontrent pas), somme des angles, triangles particuliers, trois constructions au compas et au rapporteur, médiatrice au compas, cercle circonscrit, hauteurs (aigu et obtus), cas d'égalité, triangles semblables, figure de la démonstration rédigée. Fiche : 3 figures du cours.
  - Énoncés : données seules (figures **à main levée** d'un trait irrégulier pour les constructions 3147, 3151, 3152, 3155), sans la réponse.
  - Corrigés : **construction complète en vert**, arcs de compas visibles (3147 avec $C'$, 3151, 3152, 3155, 3164), éléments démontrés en vert (côtés et angles correspondants, angles droits, médiatrices, hauteurs, longueurs trouvées).
- Toutes les constructions sont calculées en vraie grandeur puis réduites ; `verif_282.py` relit `DONNEES` et contrôle longueurs, angles, alignements, perpendicularités.
- `figures_livre.py` : 0 texte sur un trait, aucune tolérance ; avertissements restants = cotes à fond blanc (usage normal) ; toutes ≤ 900 px. Chaque PNG regardé (planches) ; corrections faites après relecture : noms de points posés sur des arcs de compas ou des demi-droites (placés dans le secteur libre), longueurs collées aux côtés (ancrage par coins), codages qui touchaient des étiquettes, légendes superposées, arc de 3164 tracé dans le mauvais sens, figure des hauteurs du cours passée en vertical (trop petite sur téléphone).

## Contrôles

- `verif_282.py` : **118 contrôles sympy justes** (chaque résultat du cours et des 21 corrigés, arrondis compris, et les coordonnées des figures : longueurs, angles, alignements, perpendicularités).
- `verifier_notion.py` : **OK** (57 nouvelles figures, 0 image en ligne conservée, 0 non appelée ; notes : 21 titres changés, voulu).
- Navigateur : avec `--navigateur`, Chrome est resté bloqué à la fermeture (cas connu ; toutes les vues à 0) → mon seul processus `node` arrêté et mon verrou `chrome_0.lock` retiré, puis contrôle refait avec `controle_apercu.mjs` et captures : **130 vues (téléphone + ordinateur), 0 débordement, 0 erreur de formule, 0 `$` brut, 0 image manquante** (même blocage à la fermeture après la dernière vue, même traitement).
- **Captures téléphone regardées** : cours en entier (7 vues), fiche (2 vues), corrigés 3158 et 3165. Aucune formule coupée ni réduite.
- Espaces insécables avant les unités : 218 dans les exercices, 20 dans le cours.
- Sauvegardes de la conversion automatique : `sauvegardes/282_*_conversion_auto.txt`.

## Remarques pour l'orchestrateur

- Aucune remarque d'outil ou de moteur.
