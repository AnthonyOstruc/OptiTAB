# Rapport : notion 85, Fonction exponentielle (Terminale)

## État
Prêt. `verifier_notion.py --navigateur` : OK, 0 problème. Toutes les valeurs sont vérifiées dans `verif_fonction_exponentielle.py` (sympy), qui affiche « TOUT EST JUSTE ».

## Texte
- **Cours 89, restructuré.** Nouveaux encadrés : définition, propriétés, théorèmes. Ajout des démonstrations du programme : limites en ±∞, limite de (eˣ−1)/x, croissances comparées pour n = 1 puis dans le cas général. Ajout de la méthode « lever une indétermination », des erreurs fréquentes et du plan d'étude. Les tableaux de variations et de convexité de x·e⁻ˣ sont désormais natifs. Les longues chaînes de calcul sont alignées.
- **Fiche 30.** Le tableau en image est remplacé par un tableau natif. La formule des croissances comparées est découpée en deux lignes pour le téléphone.
- **Exercices (13), réécrits.** Chacun suit le schéma méthode / étapes / résultat, avec des encadrés « Attention » et « À retenir » quand c'est utile.

Erreurs et défauts corrigés dans les exercices :
- **Contenu perdu à la conversion** (les signes < et > avaient avalé du texte) :
  - 1212 Q4 : « −x −4 » ;
  - 1213, solution 2 : « g'(x) 0 » ;
  - 1220 Q4 : « x 0 » ;
  - 1215 Q2 : « 0 ≤ x 0 ».
- **Tableaux** :
  - deux tableaux en barres verticales mal formés (1216 Q3, 1211 Q5) sont remplacés par des tableaux natifs ;
  - le tableau de 1211 Q2 contenait « min » au lieu d'une valeur ;
  - il manquait la ligne de signe de x dans 1215 ;
  - la double barre en 0 manquait pour g dans 1217.
- **Raisonnements faux ou imprécis** :
  - 1213 Q4 : en +∞, il n'y a pas de forme indéterminée ; l'ancienne justification « l'exponentielle l'emporte » était inadaptée ;
  - 1220 Q3 : un point d'inflexion exige que f'' s'annule **en changeant de signe** ;
  - 1209 Q3 : la remarque « limite admise en Première » est remplacée par la preuve par le taux d'accroissement.
- **Réponses incomplètes** : la solution 2 de 1217 n'abordait pas g ; 1218 vérifie maintenant l'ensemble de définition à chaque question.
- **Typographie** : virgule décimale `{,}`, intervalles notés `\left]…\right[`, symboles `\lt` et `\gt`.

## Figures
- **24 nouvelles figures au style des livres** (23 fichiers ; la courbe de exp est utilisée dans le cours et dans la fiche). Le contrôle des chevauchements n'a signalé aucune erreur ni aucun avertissement.
- **Refaites (17)** :
  - cours : 3 ;
  - exercices : 1212 ×3, 1217 ×1, 1213 ×2, 1216 ×4, 1218 ×2, 1211 ×2, 1220 ×2, 1214 ×1, 1215 ×1.
- **Ajoutées (5)** :
  - 1217 : courbe de g (en plus de celle de f) ;
  - 1219 : croissance des bactéries ;
  - 1212 Q3 et Q5, 1216 Q4 : courbes refaites à une position déjà appelée, comptées ci-dessus.
- **Retirées** : 2 tableaux en image (cours et fiche), 1212 Q1 et Q4, 1216 Q2, 1218 Q1, Q2 et Q4, 1211 (doublon), 1220 Q5. Ces figures étaient illisibles (intersection invisible à l'échelle), sans apport ou en doublon.
- **Conservées : 0.** Toutes les images en ligne étaient au style matplotlib par défaut.

## Contrôles
- verifier_notion OK.
- Vues regardées en téléphone : cours (4 captures), fiche, exercices 1212 et 1220.
- Les formules trop larges ont été réparties sur plusieurs lignes après relecture.

## Remarques pour l'orchestrateur
- **Défaut du moteur `optitabDoc.js`.** Dans un libellé de ligne de `::: tableau` qui mêle du texte et une formule (« Convexité de $f$ »), l'espace placé avant la formule disparaît : on lit « Convexité def ». Cause probable : la cellule est un conteneur flex, qui supprime cet espace. Contournement appliqué ici : une espace insécable avant `$f$`.
- **Programme.** Les exercices utilisent `ln`, comme le livre, où l'exponentielle vient après le logarithme. Un encadré de rappel sur le logarithme est ajouté en 1212 Q2.
- **valider_v1.** Il signale « [IMAGE_N] utilisée mais déclarée », car aucune ligne `Image:` n'existe en 1219 et une seule en 1217. verifier_notion filtre ce message ; les lignes `Image:` sont laissées telles quelles.

## Finition 2026-11-02

**État : prêt** (passe commencée par un premier agent, interrompue vers 14 h, reprise et terminée).

### Titres
- Cours « Fonction exponentielle » (était « Fonction exponentielle : limites et études »), fiche « Résumé : Fonction exponentielle » : intitulé officiel.
- 13 titres d'exercices : « Type - Fonction Exponentielle - … » → « Type - sujet », sans majuscules abusives (ex. « Découverte - Dérivées de base », « Problème - Modélisation d'une population de bactéries », « Problème - Équations avec exponentielle et logarithme »).

### Exercices
- Les 13 exercices sont relus : justes, au programme, corrigés complets. Aucun n'a eu besoin d'être réécrit dans cette passe.

### Figures (27 fichiers, 29 emplacements)
- **Ajoutées (4)** : `cours_croissances` (eˣ et x³, eˣ > x³ dès x > 4,54 ; cours II.3 et fiche), `ex1209_limites` (asymptote en −∞ et tangente y = x + 1), `ex1209_taux` (taux d'accroissement en 0 : sécante (AM) et tangente de pente 1), `ex1210_variations` (e^{3x} croissante, e^{−2x+1} décroissante).
- **Revérification à l'œil des 27 figures (reprise) : 2 retouchées**
  - `cours_croissances` : l'étiquette « y = eˣ » touchait la courbe → déplacée dans l'espace libre ;
  - `ex1209_taux` : l'étiquette du point A cachait la graduation 1 → placée sous le point.
- Toutes les figures à graduations placées à la main : suppression des petits carrés blancs laissés par les graduations automatiques vides.
- `figures_livre.py` : 27/27, **0 erreur, 0 avertissement**.

### Contrôles
- `verif_fonction_exponentielle.py` : TOUT EST JUSTE (155 contrôles, dont les valeurs écrites sur les nouvelles figures).
- `verifier_notion.py --navigateur` : OK, 0 problème (29 nouvelles figures, 0 image en ligne conservée, 8 anciennes images non appelées → supprimées à l'import).
- `controle_apercu.mjs` avec captures : 82 vues sur 82 sans défaut (téléphone et ordinateur) ; il est resté bloqué à la fermeture de Chrome (défaut connu) après la dernière capture : seul mon processus a été arrêté et son verrou libéré. Captures regardées : cours (partie croissances comparées), 1218 (étapes).
- **Formules au téléphone** (mesure dans Chrome à 390 px, script de travail hors du dépôt) : 1218 Q1, chaîne de l'ensemble de définition qui défilait → redécoupée ; 1218 Q3, point isolé en début de ligne après une formule → formule centrée. Résultat : 0 formule qui défile.
