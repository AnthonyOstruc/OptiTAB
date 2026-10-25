# Première : audit de conformité du 23 octobre 2026

Audit indépendant du livre de Première spécialité (programme et épreuve anticipée),
mené sur les textes officiels téléchargés dans `tmp/pdfs/recherche-premiere-audit/`.

## Textes officiels consultés

- Programme d'enseignement de spécialité de mathématiques de la classe de première de la voie générale — Arrêté du 26-2-2026, JO du 27-3-2026, NOR MENE2602917A, BO n° 14 du 2 avril 2026 — <https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602917A>
- Programme de mathématiques de seconde générale et technologique (liste des automatismes de Seconde) — NOR MENE2602914A, BO n° 14 du 2 avril 2026 — <https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602914A>
- Épreuve terminale anticipée de mathématiques de la classe de première des voies générale et technologique — Note de service du 11-9-2026, NOR MENE2622640N, BO spécial n° 4 du 17 septembre 2026 — <https://www.education.gouv.fr/bo/2026/Special4/MENE2622640N>
- Exigences en matière de maîtrise de la langue à tous les examens à compter de la session 2027 — Note de service du 11-9-2026, NOR MENE2623195N, même BO spécial — <https://www.education.gouv.fr/sites/default/files/document/20260917boenjsspe4pdf-520753.pdf>
- Sujets zéro de l’épreuve anticipée, voie générale, spécialité (format 2025 avec QCM) — Éduscol, 2025 — <https://eduscol.education.gouv.fr/sites/default/files/document/sujet-specialite-1pdf-112050.pdf>

## Écarts constatés

- Sujets blancs : 9 automatismes sur 24 portaient sur des notions de spécialité (dérivée, tangente, cosinus, loi de Bernoulli, suites, exponentielle, cercle, produit scalaire, liste Python) et non sur la rubrique Automatismes du programme ; aucune lecture graphique n'était proposée.
- Sujets blancs : la deuxième partie était intitulée « problèmes » et le point de « rédaction » ne reprenait pas les critères officiels de maîtrise de la langue.
- Guide de l'épreuve : coefficient, trois sujets distincts, oral de contrôle, grille de maîtrise de la langue, liste de référence des automatismes et abrogation de la note du 10 juin 2025 non mentionnés.
- Exemple d'algorithme absent : liste des coefficients directeurs des sécantes pour un pas donné.
- Méthode de Newton (exercice 12.14) : récurrence donnée sans lien avec la tangente.
- Méthode d'Archimède (exercice 6.15) : le programme calculait le périmètre avec math.pi, ce qui ne constitue pas une approximation de pi.
- Cours : nombre dérivé nul en un extremum, calcul du produit scalaire à l'aide de normes, translation de la courbe de x ↦ f(x − m), fonctions du second degré s'annulant en deux réels donnés, notations u(n) et (u_n), lien entre suites arithmétiques et fonctions affines, valeur approchée de e par (1 + 1/n)^n : non explicités.
- Typographie : 10 espaces parasites après une apostrophe (« d’ un ») et 184 apostrophes droites imprimées dans les chapitres 6 à 14, ainsi que dans les titres en Montserrat.
- Rendu (relecture visuelle) : décimales des graduations avec un point (0.5, 1.5) et milliers sans espace ; espace de soustraction après le crochet ouvrant des intervalles de borne négative (« ] − 4; 1[ ») ; expression débordant de sa case dans deux tableaux de signes (cours 1 et corrigé 14.12) ; intitulé « Analyse » isolé en bas de page dans les repères du programme ; colonnes inégales du tableau des valeurs remarquables.

## Corrections

- **Sujets blancs A et B.** Les 24 automatismes sont réécrits dans la rubrique
  « Automatismes » du programme de Première et dans celle de Seconde : évolutions
  et taux réciproques, calcul numérique et algébrique, signe, coefficient directeur,
  isoler une variable, moyenne pondérée, médiane, boîte à moustaches, tableau croisé
  et probabilités conditionnelles, résolution graphique, signe lu sur une courbe,
  équation de droite lue sur un graphique. Deux figures quadrillées sont ajoutées,
  complétées en vert au corrigé. La deuxième partie est intitulée « Deuxième partie
  (14 points) » avec deux exercices de 7 points, dont 1 point de maîtrise de la langue.
  En-tête conforme : 2 heures, calculatrice non autorisée.
- **Guide de l’épreuve.** Coefficient 2, sujet propre à la spécialité, tableau des
  deux parties, maîtrise de la langue (2 points sur 20, quatre critères officiels),
  oral de contrôle (20 + 20 minutes, au moins deux exercices, sans calculatrice),
  automatismes de référence, différence avec les sujets zéro de 2025 (QCM) et
  abrogation de la note du 10 juin 2025.
- **Exemples d’algorithmes du programme.** 3.6 : fonction `secantes(h, n)`
  (liste des coefficients directeurs des sécantes pour un pas donné) ;
  6.15 : méthode d’Archimède sans `math.pi` (96 côtés : 3,14103) ;
  12.14 : récurrence de Newton déduite de la tangente à x² − 2 ;
  5.11 : lien explicite avec la suite ((1 + 1/n)^n).
- **Cours.** Chapitre 1 : trinômes s’annulant en deux réels donnés, racine évidente,
  courbe de x ↦ f(x − m). Chapitre 2 : notations u(n) et (u_n), lien avec les
  fonctions affines. Chapitre 4 : f′(a) = 0 en un extremum intérieur, étude d’un
  trinôme par sa dérivée. Chapitre 5 : dérivée de t ↦ e^(at). Chapitre 7 : produit
  scalaire à l’aide des normes.
- **Typographie et rendu.** Apostrophes harmonisées (« ’ ») dans le texte et les titres,
  espaces parasites après élision supprimées, crochets d’intervalles de borne
  négative composés sans espace de soustraction, virgule décimale et espace des
  milliers sur toutes les graduations, première colonne élargie dans deux tableaux
  de signes, colonnes égales pour les valeurs remarquables, intitulés de domaine
  solidaires de leur première ligne dans les repères du programme.
- **Repères du programme.** Matrice portée de 54 à 60 groupes,
  avec renvois vers les sujets blancs.

## Contrôles

- 222 groupes de contrôles de résultats sur les 210 exercices
  et 23 blocs Python exécutés.
- 2804 contrôles de relecture et 415
  contrôles de l’édition France (dont les 24 nouveaux automatismes recalculés avec SymPy).
- 28 programmes extraits du PDF compilé, valides, identiques aux sources et exécutés.
- Compilation stabilisée : aucun Overfull, aucun caractère manquant, aucun renvoi indéfini.
- 319 pages ; 32 pages identiques au pixel à 80 dpi
  et 287 pages modifiées, toutes relues :
  2, 3, 4, 5, 8, 10, 11, 12, 13, 16, 17, 18, 19, 20, 23, 24, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 75, 76, 78, 79, 80, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 120, 121, 122, 123, 124, 125, 126, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 162, 163, 164, 165, 166, 167, 168, 171, 172, 173, 174, 175, 176, 178, 181, 184, 185, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318.
- Défauts visuels restants : aucun.

Empreinte SHA-256 du PDF livré : `3040f3a2de2b82050655c6f9cb9de6a0b1814e9385259d93b3aacbec1c088448`.
