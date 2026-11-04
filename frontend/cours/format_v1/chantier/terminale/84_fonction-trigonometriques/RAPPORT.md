# Notion 84 — Fonctions trigonométriques (Terminale)

Prêt. Reprise du chapitre pilote validé par le propriétaire (`pilote_trigo_terminale/`) :
cours 91, fiche 29 et 10 exercices au format v1, 26 corrections de fond, 13 tableaux
vérifiés numériquement, 22 figures style livre (sources : `figures/figures_pilote.py`).

## Finition 2026-11-02

**État : prêt** (passe commencée par un premier agent, interrompue vers 14 h, reprise et terminée).

### Titres
- Cours « Fonctions sinus et cosinus », fiche « Résumé : Fonctions sinus et cosinus » : intitulé officiel, inchangés.
- 10 titres d'exercices : « Type - Fonctions Trigonométriques - … » → « Type - sujet » (ex. 1198 « Découverte - Valeurs remarquables sur le cercle », 1202 « Problème - Aire maximale d'un trapèze », 1207 « Problème - Intégrales et aires avec sinus et cosinus »).

### Exercices réécrits
- Les 10 exercices (contenu hérité du pilote) sont réécrits : la fonction tangente, hors programme de Terminale spécialité, est retirée ; calculs isolés remplacés par des exercices complets (valeurs remarquables lues sur le cercle, dérivées et tangente, équations et inéquations sur le cercle, étude de cos² x + sin x, aire maximale d'un trapèze, limites, parité et périodicité, suites, intégrales et aires).

### Figures (35 fichiers, 37 emplacements, toutes au style des livres)
- Toutes refaites (`figures_pilote.py` n'est plus utilisé) ; figures dans le cours (5), la fiche (2), les énoncés (1198, 1202, 1204, 1207) et les corrigés (complétés en vert).
- **Revérification à l'œil (reprise) : 13 figures retouchées**
  - `cours_courbes` : graduations −π, π, 2π posées sur la sinusoïde (signalées par le détecteur) → placées du côté libre ;
  - `ex1198_points` : « −√3/2 » coincé entre deux pointillés (ambigu) → chaque abscisse contre son propre pointillé ;
  - `ex1205_q2` : « π » au-dessus et « −π » au-dessous de l'axe, lus comme une fraction → une seule étiquette « π et −π » ;
  - `ex1206_q2` : « n = 0 » collé à l'axe → décollé ;
  - `ex1200_q5` : graduation π posée sur les deux courbes (détecteur) → descendue sous les courbes avec un repère pointillé ;
  - `ex1202_aire` : graduation 3√3/4 minuscule → étiquette verte « 𝒜max = 3√3/4 » au-dessus du maximum ;
  - `lim_gendarmes` : graduations 2π, 4π, 6π posées sur la courbe et sur y = −1/x (détecteur) → placées sous les enveloppes ; ±1/2 agrandis ; « limite 0 en +∞ » ajouté ;
  - `lim_1mcos`, `ineq_cos2x`, `ex1206_suite` : fractions 1/2, 1/x agrandies (illisibles au téléphone) ; `ineq_cos2x` : π/2 posé sur la droite y = 1/2 (détecteur) → retiré ;
  - `ex1207_enonce`, `ex1207_q5` : π et π/2 posés sur les courbes → du côté libre, sans carré blanc dans le domaine.
- Toutes les figures à graduations placées à la main : suppression des petits carrés blancs laissés par les graduations automatiques vides (ils coupaient la grille ou une courbe).
- `figures_livre.py` : 35/35, **0 erreur, 0 avertissement** (4 avertissements avant reprise).

### Contrôles
- `verif_trigo.py` : 140 vérifications, TOUT EST JUSTE (9 nouvelles sur les figures retouchées).
- `verifier_notion.py --navigateur` : OK, 0 problème (37 nouvelles figures, 0 image en ligne conservée, 6 anciennes images non appelées → supprimées à l'import).
- `controle_apercu.mjs` avec captures : aucun problème détecté (téléphone et ordinateur). Captures regardées : cours (3 vues), fiche, 1202 et 1205 (étapes).
- **Formules coupées au téléphone** (non signalées par l'outil, qui ne compte pas les formules qui défilent) : mesure dans Chrome à 390 px (script de travail hors du dépôt), puis corrections :
  - cours : identité cos² + sin² et encadrements séparés, formules (sin(ax + b))′ et (cos(ax + b))′ sur deux lignes, tableau des valeurs remarquables passé en colonnes (il défilait), (x sin x)′ et l'étude de sin(2x) reformulées ;
  - exercices : 1200 Q1 et Q5, 1201 (valeurs de f), 1202 (factorisation, valeurs de 𝒜, solution 3), 1204 (parité de g et de k), 1205 Q4, 1206 (u₀, u₁, u₂ ; tableaux de vₙ et de cos(kπ/3) remis en colonnes), 1207 Q2 (intégration par parties) : chaînes redécoupées en lignes alignées.
  - Résultat : 0 formule qui défile, 0 formule réduite sous 80 %. Restent les tableaux de signes à 5 valeurs ou plus (1201, 1204, 1205), qui défilent dans leur cadre : rendu normal du moteur.

### Remarques pour l'orchestrateur
- **Nom de la notion en base** : « Fonction trigonométriques » (faute d'accord, visible en tête de page) → à renommer « Fonctions sinus et cosinus » (intitulé officiel, titre du cours). Le cours 85 et le cours 86 n'ont pas ce défaut.
- **Outils** : `controle_apercu.mjs` ne compte pas les formules qui défilent (`mjx-scrollable`) ni les formules réduites à 70-80 % : sur ces trois notions, une vingtaine de chaînes étaient coupées au téléphone sans être signalées. Un contrôle de la largeur naturelle des formules serait utile dans l'outil.
- `figures_livre.py` : une compilation a échoué une fois (cache de polices luaotfload, sans doute deux compilations simultanées) ; relancée seule, elle passe.
