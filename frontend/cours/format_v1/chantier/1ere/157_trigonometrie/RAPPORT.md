# Rapport — 1ère / 157 Trigonométrie

**État : prêt.** Aucune écriture en base, aucun `manage.py`, aucun `git`.

## Programme (Première spécialité, 2019)

Couvert : cercle trigonométrique, longueur d’arc, radian, enroulement, point image,
cosinus et sinus d’un réel, lien avec le triangle rectangle, valeurs remarquables
(démonstrations de $\sin\frac{\pi}{4}$, $\cos\frac{\pi}{3}$, $\sin\frac{\pi}{3}$),
angles associés, fonctions cosinus et sinus (parité, périodicité, courbes), algorithme
d’Archimède pour approcher $\pi$ (exemple d’algorithme du programme).
Retiré car Terminale : changements de variable ($\cos 2x$, $\sin(x + \frac{\pi}{6})$),
inéquations formelles, étude de $1 + 2\cos(x - \frac{\pi}{3})$, modèle $a + b\sin(\omega t + \varphi)$.
Les équations $\cos x = a$, $\sin x = a$ restent, limitées aux valeurs remarquables
et résolues **par lecture du cercle** (capacité « lecture du cercle »).

## Texte

- **Cours** réécrit : objectifs + prérequis, 5 parties (cercle et radian, cos/sin et
  triangle rectangle, valeurs remarquables avec démonstrations, angles associés
  y compris $\frac{\pi}{2} \pm x$, fonctions cos/sin), méthodes, exemples, erreurs fréquentes.
- **Fiche** réécrite (formules, tableaux des valeurs et des angles associés, pièges).
- **Exercices** : les 9 blocs réécrits au format v1 (méthode / étapes / résultat /
  erreur fréquente), Ids inchangés.
  - 1390 (DS) : inéquation $\cos x \lt -\frac{\sqrt{2}}{2}$ et $\cos 2x = \frac{1}{2}$ remplacées par deux
    équations lues sur le cercle ; formulation fausse « $g$ impaire par rapport au point
    $(0;2)$ » corrigée en « courbe symétrique par rapport à $A(0;2)$ » ; ajout $g(x) = \frac{7}{2}$.
  - 1387 : question 3 (changements de variable, Terminale) remplacée par $\cos x = 2$
    (aucune solution) et $\cos x = \sin x$.
  - 1389 : inéquation $f(x) \ge 0$ remplacée par parité/périodicité pour compléter la
    courbe ; tableau de variations vérifié : `+/1, =/0, -/-3` est **juste**
    ($f$ décroissante sur $[0;\pi]$, $f(\frac{\pi}{3}) = 0$ en valeur intermédiaire).
  - 1391 **remplacé** (étude de $1 + 2\cos(x - \frac{\pi}{3})$, hors programme) par
    « Type Examen - Angles associés et valeur exacte de cos(π/5) ».
  - 1388 (grande roue) : modèle $a + b\sin(\omega t + \varphi)$ remplacé par une
    démarche de Première ($\theta = \pi t$, angle associé, $h = 15 - 12\cos\theta$).
  - 1392 : les appels [IMAGE_1] et [IMAGE_2] sans image ont maintenant leurs figures.
- **Ajouts** : nouveau-1 « Problème - Approximation de π par la méthode d'Archimède »
  (géométrie + Python) ; nouveau-2 « Entraînement - Du cercle aux courbes de cosinus et
  sinus » (lien cercle/courbes, parité, périodicité graphiques).
- Aucune erreur de calcul trouvée dans la source ; toutes les valeurs vérifiées :
  `verif_trigo.py` (149 vérifications sympy/numpy, tout juste).

## Figures (`figures/figures.py`, 18 figures, 21 emplacements)

- 4 images en ligne du cours et 2 de la fiche **refaites** (anciennes non conservées).
- Ajoutées : cours (enroulement, cercle complet des valeurs remarquables), et
  11 figures d’exercices (corrigés avec points-réponses en vert).
- 0 conservée, 0 retirée sans remplacement. Contrôle texte/trait du compilateur : OK
  (seules les cotes de la grande roue ont un fond blanc, comme prévu).

## Contrôles

- `verifier_notion.py --navigateur` : OK, 0 problème.
- `controle_apercu.mjs` : 0 débordement, 0 erreur de formule, 0 élément trop large
  (téléphone et ordinateur, 11 exercices × 3 onglets). Captures regardées : cours
  (5 vues téléphone), fiche, exercices 1389, 1391, 1392, nouveau-1, nouveau-2.
  Corrigé après capture : formules longues mises en `aligned` (plus de défilement),
  tableaux trop larges transposés (valeurs remarquables, angles associés, Archimède),
  intervalles $]-\pi\,;\pi]$ écrits avec `\left] … \right]` (signe moins bien rendu).

## Remarques pour l’orchestrateur

- Le titre de l’Id 1391 change (exercice remplacé) : signalé par le vérificateur.


## Finition 2026-11-02

**État : prêt.** Mise en conformité avec les deux consignes du 2026-11-02 (figures partout où elles aident, titres).

**Titres.** Cours : « Fonctions trigonométriques » ; fiche : « Résumé : Fonctions trigonométriques ». Exercices : 1384 « Découverte - Radians, longueurs d'arc et points images » ; 1385 « Découverte - Valeurs remarquables de cosinus et sinus » ; 1390 « DS - Valeurs exactes, équations et étude d'une fonction » ; 1389 « Problème - Parité, périodicité et courbe de 2 cos x − 1 » ; 1391 « Type examen - … » (majuscule de « Examen » retirée). Les autres titres étaient déjà conformes.

**Figures : 14 nouvelles** + 1 figure du cours réutilisée, 0 refus du détecteur de chevauchement.
- Corrigés des trois exercices signalés : 1388 « La grande roue » (roue complétée : positions à 21 m, θ = 2π/3 et 4π/3, arc vert où h ≥ 21 m ; courbe de h(t) et intervalle [2/3 ; 4/3]) ; nouveau-1 Archimède (triangles OHA et AHC avec AH = c/2, HC = 1 − OH, c′, angle π/n) ; nouveau-2 (courbes avec les 4 intersections de y = 0,3 et les 4 points où cos x = sin x).
- Autres corrigés : 1385 (M(π/4) sur y = x ; symétriques de M(π/6)), 1386 (points 7π/6, 3π/4, 11π/6, −π/3), 1387 (cos x = −1/2), 1390 (sin x = √3/2 ; cos x = −√2/2 ; courbe de 3 sin x + 2 avec centre de symétrie, extremums et droite y = 7/2), 1391 (symétries des points π/5 … 4π/5).
- Énoncés : 1384 (enroulement de la droite des réels), 1385 (triangle OIM et H), 1392 (cercle gradué vierge pour placer les points).
- Les 11 exercices ont maintenant au moins une figure.

**Contrôle de qualité.** Erreur corrigée : nouveau-2 Q6a disait que la droite y = 0,3 coupe la sinusoïde « une fois sur chaque arche positive » alors qu’elle la coupe deux fois par arche (4 solutions) ; texte réécrit. Valeurs des nouvelles figures vérifiées dans `verif_trigo.py` : **177 vérifications justes**.

**Contrôles.** `verifier_notion.py --navigateur` : OK, 0 problème. `controle_apercu.mjs` : 70 vues (téléphone et ordinateur) sans débordement ni erreur. Captures téléphone regardées : 1390, 1388 et nouveau-1 (corrigés complets). Corrigé après capture : deux-points isolés en début de ligne dans 1388 (phrases terminées par un point).

**Remarques pour l’orchestrateur.**
- nouveau-1 et nouveau-2 sont **déjà en ligne** (Id 4606 et 4607, sauvegarde d’import) : avant réimport, nouvel export et remplacement des `Id: nouveau-N` et des clés de `correspondance.json`, sinon doublons.
- Moteur : un point qui suit une formule passe parfois seul en début de ligne sur téléphone (1388 Q3 c, « … = −1/2 » puis « . Dans [0 ; 2π] ») ; la typographie automatique ne colle pas toujours la ponctuation à la formule.
- `controle_apercu.mjs` bloqué à la fermeture de Chrome : mon processus arrêté, mon verrou supprimé.
