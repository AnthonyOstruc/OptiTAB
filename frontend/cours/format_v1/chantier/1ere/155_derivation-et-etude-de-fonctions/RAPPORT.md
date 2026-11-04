# Notion 155 — Dérivation et étude de fonctions (Première spécialité)

**État : prêt.** Aucun point en suspens.

## Texte

**Cours** (refondu, programme 2019) : 5 parties — taux de variation et nombre dérivé (définition avec
la notation lim, exemple détaillé, méthode, interprétations vitesse / coût marginal) ; tangente
(définition, équation réduite et **démonstration du programme**, lecture graphique) ; fonction dérivée
(tableau des dérivées usuelles avec $x^3$, démonstrations du programme : carré, inverse, **racine carrée
non dérivable en 0** ; **valeur absolue non dérivable en 0**, qui manquait) ; opérations (tableau,
$g(ax + b)$, démonstration du produit, exemples en calculs alignés, erreurs fréquentes) ; variations
(théorème admis, définition d’extremum local, propriété extremum ⇔ changement de signe, contre-exemple
$x^3$, méthode, exemple $x^3 - 3x$ avec `::: tableau` natif, lien avec le second degré, applications :
optimisation, inégalité / position de deux courbes avec exemple $x + \frac{1}{x} \ge 2$).
Rien de hors programme (ni convexité, ni composée générale, ni limites en $\pm\infty$ : les tableaux
sur $\mathbb{R}$ laissent les extrémités vides).

**Fiche** : formule du nombre dérivé et de la tangente, figure, deux tableaux de formules, théorème,
tableau natif, 5 pièges.

**Exercices** : les 10 blocs ont été restructurés (la conversion avait cassé les DS / sujets type
examen : questions fusionnées dans des encadrés, `::: etape s`, solutions tronquées « $g'(x) 0$ »,
« $t 0$ »). `## Partie` / `## Question`, méthode, étapes, résultat, erreurs fréquentes ; tableaux de
signes et de variations natifs, hors des encadrés `etape`.

Erreurs et hors-programme corrigés :
- **tous les tableaux** affichaient des limites $\pm\infty$ (notion de Terminale) → extrémités vides ;
- 1370 B5 : « point d’inflexion » (convexité, Terminale) supprimé ; question réécrite (« extremum en 2 ? » :
  non, $f'$ ne change pas de signe) ; théorème A3 ramené à l’énoncé du programme ;
- 1374 A3 et B4 : $(u^n)' = nu^{n-1}u'$ et $(3x^2 - x)^4$ **hors programme** → dérivée de $g(ax + b)$ et
  $k(x) = \sqrt{5 - 2x}$ ; D4 : racine cubique $\sqrt[3]{\;}$ (hors programme) remplacée par $r_0$ admis,
  signe de $S'$ justifié par la croissance de la fonction cube, ajout D5 ($h = 2r_0$) ;
- 1371 A4, 1367 Q3c : « règle de la chaîne » → formule $\big(g(ax + b)\big)' = a\,g'(ax + b)$ du programme ;
- 1368 Q3 : « admet-elle un maximum ? » ambigu (pas de maximum sur $\mathbb{R}$) → extremums locaux,
  ajout de $f(5) = 21 \gt 5$ pour le faire comprendre ;
- 1373 : coûts pour « $x$ objets » avec $x \in [0;15]$ → centaines d’objets ; tableau $s(t)$ ajouté ;
- domaines manquants ou faux (« pour $x \neq -2$ » pour un quotient étudié sur un intervalle) précisés.

Remplacements (même Id) :
- **1372** « Fonctions composées » : $(x^2 - 3)^2$ par la règle de la chaîne et $(x^2 + 2x)^3$ **hors
  programme** → titre « g(ax + b), produits et quotients » : quatre fonctions $g(ax + b)$ (puissances,
  racine, inverse), produits / quotients gardés, et étude complète de $(x^2 - 3)^2$ en développant.
- **1366** : ajout de la question 3 (calcul exact $6 + h$) et de la question 4 (**programme Python**
  des taux de variation, capacité « algorithmique » du programme).
- **1365** : ajout des équations des tangentes et de la cohérence signe de $f'$ / sens de variation.

Ajouts (compétences du programme non travaillées) :
- **nouveau-1** « Problème - Inégalité et position d’une courbe et d’une tangente » : cube et sa tangente
  en 1, étude de $d = f - g$, inégalité $x^3 + 2 \ge 3x$ (figure dans le corrigé) ;
- **nouveau-2** « Entraînement - Inverse, racine carrée et valeur absolue » : $x + \frac{4}{x}$ et
  encadrement, $x\sqrt{x}$ (dérivable en 0 malgré $\sqrt{\;}$), non-dérivabilité de $\sqrt{\;}$ et de $|\cdot|$ en 0 ;
- **nouveau-3** « Découverte - De la courbe de f' aux variations de f » : lecture du signe de $f'$ sur
  sa courbe, variations de $f$, tangente.

Tous les résultats sont vérifiés par `verif_155.py` (sympy) : **125 vérifications justes**.

## Figures

Les 8 images en ligne (style matplotlib, couleurs criardes, légendes minuscules, tableaux en image)
sont toutes abandonnées : **11 figures refaites / ajoutées** au style des livres (`figures/figures.py`),
aucune conservée.
- refaites : sécantes → tangente, tangente à la parabole, courbe $x^3 - 3x$ et extremums,
  courbes des exercices 1366 et 1365 (avec la même fonction et les mêmes points que l’énoncé) ;
- ajoutées : non-dérivabilité ($|x|$ et $\sqrt{x}$), corrigés de 1366 et 1365 (triangles de pente en
  vert / orange), courbe de 1368 (extremums), cube et tangente (nouveau-1), courbe de $f'$ (nouveau-3) ;
- retirées : les deux tableaux de variations en image (cours, fiche) → `::: tableau` natifs.
Détecteur de chevauchement : 0 refus ; graduations déplacées du côté libre (XLAB) là où un pointillé
de lecture passait ; une graduation masquée dans le corrigé de 1365 (sous le pointillé, point $D$ nommé).

## Contrôles

- `verifier_notion.py --navigateur` : **OK, 0 problème**.
- `controle_apercu` : 0 débordement, 0 erreur de formule, 0 élément trop large (téléphone et ordinateur).
- Captures téléphone regardées : cours (toutes les parties), fiche, exercices 1374, nouveau-1, nouveau-3
  (énoncé + étapes). Corrections faites après relecture : tableaux de formules du cours passés de 3 à
  2 colonnes (la 3e était coupée), chaînes de calcul trop longues mises en `aligned`, moins unaire
  dans les intervalles (`{]{-1}\,;3[}` au lieu d’un « ] − 1 » espacé), figure de non-dérivabilité
  agrandie ; recapture faite.

## Remarques pour l’orchestrateur

- Exercice 1374 D4 : le tableau de variations utilise `D+/` (double barre en 0, valeur vide) ;
  rendu vérifié sur capture.
- L’image en ligne n° 2 de la fiche (tableau en image) n’est plus appelée : supprimée à l’import.


## Finition 2026-11-02

**État : prêt.** Mise en conformité avec les deux consignes du 2026-11-02 (figures partout où elles aident, titres).

**Titres.** Cours : « Dérivation, variations et courbes représentatives » ; fiche : « Résumé : Dérivation, variations et courbes représentatives ». Exercices : nom du chapitre retiré, « Type 1 / Type 2 » remplacés par un vrai titre :
1366 « Découverte - Du taux de variation au nombre dérivé » ; 1365 « Découverte - Lire des nombres dérivés sur des tangentes » ; 1369 « DS - Sujet A : dérivées, tangentes et variations » ; 1371 « DS - Sujet B : dérivées, tangentes et extremums » ; 1373 « Entraînement - Optimisation : aire, coût et vitesse » ; 1367 « Entraînement - Calculs de dérivées et tangente » ; 1372 « Entraînement - Dérivées de g(ax + b), produits et quotients » ; 1368 « Problème - Étude d’une fonction polynôme de degré 3 » ; 1370 « Type examen - Sujet A : tangente et boîte de volume maximal » ; 1374 « Type examen - Sujet B : étude de fonction et boîte cylindrique » ; nouveau-1 « Problème - Position d’une courbe et de sa tangente » ; nouveau-2 « Entraînement - Inverse, racine carrée et valeur absolue » ; nouveau-3 « Découverte - De la courbe de f' aux variations de f ».

**Figures : 21 nouvelles** (style livres, `figures/figures.py`, section « finition »), 0 refus du détecteur de chevauchement.
- Énoncés : rectangle de périmètre 40 m (1373), boîte sans couvercle (1370), boîte cylindrique (1374), courbe du cube et point A (nouveau-1).
- Corrigés (éléments de réponse en vert) : 1369 (parabole + tangente T et tangente horizontale ; courbe de g et extremums), 1371 (idem), 1373 (courbes de l’aire, du coût et de la position, tangentes horizontales), 1367 (tangente horizontale y = −1), 1372 (courbe de (x² − 3)², trois tangentes horizontales), 1370 (tangente horizontale sans extremum ; courbe du volume avec V(2), V(8)), 1374 (courbe, extremums et tangente T ; aire minimale en r₀), nouveau-2 (encadrement 4 ≤ f(x) ≤ 20/3), nouveau-3 (courbe de f' en vert / orange selon le signe : le corrigé montre désormais la figure complétée).
- Cours : exemple d’optimisation ajouté (enclos le long d’un mur, tableau natif + courbe), figure de l’inégalité x + 1/x ≥ 2. Fiche : courbe de x³ − 3x et ses extremums (figure du cours).
- Les 13 exercices ont maintenant au moins une figure, dans le corrigé quand le raisonnement porte sur une courbe.

**Contrôle de qualité.** Aucun exercice faux ou hors programme trouvé. Correction : 1373 Q2, coût exprimé en centaines d’euros (le coût minimal de 500 objets valait 25 € : irréaliste) → 2 500 €. Tous les nombres portés sur les figures et les calculs nouveaux sont vérifiés dans `verif_155.py` : **163 vérifications justes** (125 → 163 ; une valeur approchée de r₀ corrigée dans la figure grâce au script).

**Contrôles.** `verifier_notion.py --navigateur` : OK, 0 problème. `controle_apercu.mjs` : 0 débordement, 0 erreur de formule, 0 élément trop large (téléphone et ordinateur). Captures téléphone regardées : cours (parties V et applications), exercices 1370 (énoncé et corrigé complets), fiche.

**Remarques pour l’orchestrateur.**
- Les exercices nouveau-1, nouveau-2 et nouveau-3 sont **déjà en ligne** (Id 4603, 4604, 4605, d’après la sauvegarde d’import). Avant de réimporter : nouvel export, puis remplacer `Id: nouveau-N` et les clés `"nouveau-N"` de `correspondance.json` par ces Id, sinon l’import créerait des doublons. Je n’ai pas modifié les lignes `Id:` (règle du guide).
- `controle_apercu.mjs` reste bloqué à la fermeture de Chrome après la dernière vue (toutes les vues écrites) : j’ai arrêté mon seul processus et supprimé mon verrou `chrome_0.lock`.
