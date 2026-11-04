# -*- coding: utf-8 -*-
"""Sujets type brevet 01 à 05 (contenu + contrôles)."""
import math
from fractions import Fraction as F

from brevet_3e import A, Q, X, S

R = F


# ============================================================== SUJET 01

def check01():
    assert -7 + 3 * 5 == 8 and F(2, 3) + F(1, 6) == F(5, 6) and 4.5e5 == 450000
    assert 3 * (2 - 4) == 3 * 2 - 12 and 35 / 5 == 7 and R("0.15") * 80 == 12
    assert 2 * (-2) + 1 == -3 and R("0.25") * 60 == 15 and sorted([2, 4, 5, 8, 11])[2] == 5
    assert 168 == 2 ** 3 * 3 * 7 and 126 == 2 * 3 ** 2 * 7 and math.gcd(168, 126) == 42
    assert (168 // 42, 126 // 42) == (4, 3) and 42 * R("4.5") == 189 and 189 - 78 == 111
    assert 5 * R("0.9") == R("4.5")
    assert 12 ** 2 + 9 ** 2 == 15 ** 2 and F(4, 12) * 9 == 3 and F(4, 12) * 15 == 5
    assert 12 * 9 / 2 == 54 and 4 * 3 / 2 == 6 and 54 - 6 == 48 and F(6, 54) == F(1, 3) ** 2
    assert 18 + 7 * 4 == 46 and 10 * 4 == 40 and 18 + 7 * 6 == 10 * 6 == 60
    assert 18 + 7 * 10 == 88 <= 90 < 18 + 7 * 11 and 10 * 9 <= 90 < 10 * 10
    assert 2 + 5 + 8 + 5 == 20 and F(0 * 2 + 1 * 5 + 2 * 8 + 3 * 5, 20) == R("1.8")
    assert F(3, 4) ** 2 == F(9, 16) and 2 * F(3, 4) * F(1, 4) == F(3, 8)


S01 = S("01", "Carnets, voile, locations et tirages", [
    A(r"Calculer §-7 + 3 \times 5§.", r"§-7 + 15 = 8§ (la multiplication est prioritaire)", "8"),
    A(r"Calculer §\frac{2}{3} + \frac{1}{6}§.",
      r"§\frac{4}{6} + \frac{1}{6} = \frac{5}{6}§", r"§\frac{5}{6}§"),
    A(r"Donner l'écriture scientifique de 450 000.", r"§4{,}5 \times 10^5§",
      r"§4{,}5 \times 10^5§"),
    A(r"Donner la valeur de §\sqrt{81}§.", r"§9§, car §9^2 = 81§ et §9 \geq 0§", "9"),
    A(r"Développer §3(x - 4)§.", r"§3x - 12§", r"§3x - 12§"),
    A(r"Résoudre l'équation §5x = 35§.", r"§x = \frac{35}{5} = 7§", r"§x = 7§"),
    A(r"Calculer 15 % de 80.", r"§0{,}15 \times 80 = 12§", "12"),
    A(r"On donne §f(x) = 2x + 1§. Calculer §f(-2)§.", r"§2 \times (-2) + 1 = -3§", "-3"),
    A(r"Convertir 0,25 h en minutes.", r"§0{,}25 \times 60 = 15§ min", "15 min"),
    A(r"Donner la médiane de la série : 2 ; 4 ; 5 ; 8 ; 11.",
      r"La série est rangée et compte 5 valeurs : la médiane est la 3e, soit 5", "5"),
], [
    X("Un atelier de carnets",
      r"Un atelier possède 168 feuilles bleues et 126 feuilles blanches. Il veut fabriquer le plus grand nombre possible de carnets identiques en utilisant toutes les feuilles : chaque carnet contient le même nombre de feuilles bleues et le même nombre de feuilles blanches.", [
        Q("Décomposer 168 et 126", r"Décomposer 168 et 126 en produits de facteurs premiers.",
          [r"R: §168 = 2^3 \times 3 \times 7§ et §126 = 2 \times 3^2 \times 7§"],
          r"§2^3 \times 3 \times 7§ et §2 \times 3^2 \times 7§"),
        Q("Le nombre maximal de carnets",
          r"Déterminer le nombre maximal de carnets et la composition d'un carnet.",
          [r"M: Le nombre de carnets doit diviser 168 et 126 : on cherche leur plus grand diviseur commun.",
           r"E: Facteurs communs : §2 \times 3 \times 7 = 42§",
           r"R: 42 carnets, contenant chacun §168 \div 42 = 4§ feuilles bleues et §126 \div 42 = 3§ feuilles blanches"],
          "42 carnets (4 bleues, 3 blanches)"),
        Q("Le bénéfice",
          r"Chaque carnet est vendu 4,50 € et les fournitures ont coûté 78 €. Calculer le bénéfice si tous les carnets sont vendus.",
          [r"E: Recette : §42 \times 4{,}50 = 189§ €", r"R: Bénéfice : §189 - 78 = 111§ €"],
          "111 €"),
        Q("Une comparaison de prix",
          r"Un autre atelier vend son carnet 5 € mais accorde une réduction de 10 %. Lequel est le moins cher ?",
          [r"E: §5 \times (1 - 0{,}10) = 5 \times 0{,}9 = 4{,}50§ €",
           r"R: Les deux carnets coûtent le même prix : 4,50 €"], "même prix (4,50 €)"),
    ], r"Le plus grand nombre de lots identiques est le PLUS GRAND DIVISEUR COMMUN des quantités."),
    X("Une voile divisée",
      r"Une voile a la forme du triangle §ABC§ rectangle en §A§, avec §AB = 12§ m et §AC = 9§ m. Le point §M§ appartient à §[AB]§ avec §AM = 4§ m, le point §N§ appartient à §[AC]§ et les droites §(MN)§ et §(BC)§ sont parallèles. [IMG:s01_voile]", [
        Q("Calculer §BC§", r"Calculer la longueur §BC§.",
          [r"M: Le triangle §ABC§ est rectangle en §A§ : on applique le théorème de Pythagore.",
           r"E: §BC^2 = AB^2 + AC^2 = 144 + 81 = 225§", r"R: §BC = \sqrt{225} = 15§ m"],
          "15 m"),
        Q("Calculer §AN§ et §MN§", r"Calculer les longueurs §AN§ et §MN§.",
          [r"M: §M \in [AB]§, §N \in [AC]§ et §(MN) \parallel (BC)§ : on applique le théorème de Thalès.",
           r"E: §\frac{AM}{AB} = \frac{AN}{AC} = \frac{MN}{BC}§, soit §\frac{4}{12} = \frac{AN}{9} = \frac{MN}{15}§",
           r"R: §AN = \frac{9}{3} = 3§ m et §MN = \frac{15}{3} = 5§ m"], "3 m et 5 m"),
        Q("Les aires de §ABC§ et §AMN§",
          r"Calculer l'aire du triangle §ABC§, puis celle du triangle §AMN§.",
          [r"E: §\mathcal{A}_{ABC} = \frac{12 \times 9}{2} = 54§ m²",
           r"R: §AMN§ est rectangle en §A§ : §\mathcal{A}_{AMN} = \frac{4 \times 3}{2} = 6§ m²"],
          "54 m² et 6 m²"),
        Q("L'aire de §MBCN§",
          r"En déduire l'aire du quadrilatère §MBCN§. Vérifier que le rapport des aires des triangles §AMN§ et §ABC§ est le carré du rapport des longueurs.",
          [r"E: §54 - 6 = 48§ m²",
           r"R: §\frac{6}{54} = \frac{1}{9} = \left(\frac{1}{3}\right)^2§ ✔️"], "48 m²"),
    ], r"Dans une réduction de rapport §k§, les aires sont multipliées par §k^2§."),
    X("Deux loueurs de matériel",
      r"Pour §n§ journées de location (§1 \leq n \leq 15§), le loueur A facture §18 + 7n§ euros et le loueur B facture §10n§ euros. Les deux tarifs sont représentés ci-dessous. [IMG:s01_tarifs]", [
        Q("Quatre jours de location", r"Calculer le prix de 4 jours de location chez A et chez B.",
          [r"E: A : §18 + 7 \times 4 = 46§ €", r"R: B : §10 \times 4 = 40§ € : B est moins cher"],
          "A : 46 € ; B : 40 €"),
        Q("Un tarif proportionnel",
          r"Lequel des deux tarifs est proportionnel au nombre de jours ? Justifier.",
          [r"R: Le tarif B : §n \mapsto 10n§ est une fonction linéaire, sa représentation est une droite passant par l'origine"],
          "B"),
        Q("Des tarifs égaux", r"Résoudre l'équation §18 + 7n = 10n§ et interpréter le résultat.",
          [r"E: §18 = 3n§, donc §n = 6§",
           r"R: Pour 6 jours, les deux loueurs demandent le même prix : §10 \times 6 = 60§ € ; c'est l'abscisse du point d'intersection des deux droites"],
          "§n = 6§ (60 €)"),
        Q("Un budget de 90 €",
          r"Avec un budget de 90 €, quelle est la durée maximale de location chez chacun des loueurs ?",
          [r"E: Chez A : 10 jours coûtent §18 + 70 = 88§ € et 11 jours §95§ € : 10 jours au maximum",
           r"R: Chez B : 9 jours coûtent 90 € et 10 jours 100 € : 9 jours au maximum"],
          "A : 10 jours ; B : 9 jours"),
    ], r"Pour comparer deux tarifs, on résout une équation : la solution donne le « point de bascule »."),
    X("Des scores et un tirage",
      r"Lors d'un jeu, 20 joueurs ont obtenu les scores suivants. [IMG:s01_scores] Ensuite, chaque joueur tire une boule dans un sac contenant 3 boules rouges (R) et 1 boule bleue (B), la remet dans le sac, puis en tire une seconde. Les tirages sont équiprobables. [IMG:s01_arbre]", [
        Q("Le score moyen", r"Calculer le score moyen.",
          [r"E: §0 \times 2 + 1 \times 5 + 2 \times 8 + 3 \times 5 = 36§",
           r"R: §\frac{36}{20} = 1{,}8§"], "1,8"),
        Q("Le score médian", r"Déterminer le score médian.",
          [r"M: Effectif 20 : la médiane est entre la 10e et la 11e valeur.",
           r"E: Effectifs cumulés : 2 ; 7 ; 15 ; 20", r"R: Les 10e et 11e valeurs valent 2 : médiane 2"],
          "2"),
        Q("Deux boules rouges", r"Calculer la probabilité d'obtenir deux boules rouges.",
          [r"R: §\frac{3}{4} \times \frac{3}{4} = \frac{9}{16}§"], r"§\frac{9}{16}§"),
        Q("Exactement une boule bleue",
          r"Calculer la probabilité d'obtenir exactement une boule bleue.",
          [r"E: Chemins R-B et B-R : §\frac{3}{4} \times \frac{1}{4} + \frac{1}{4} \times \frac{3}{4}§",
           r"R: §\frac{3}{16} + \frac{3}{16} = \frac{6}{16} = \frac{3}{8}§"], r"§\frac{3}{8}§"),
    ], r"Sur un arbre, on MULTIPLIE les probabilités le long d'un chemin et on ADDITIONNE les chemins."),
], check01)


# ============================================================== SUJET 02

def check02():
    import scratch3e as Sc
    from scripts_brevet import SCRIPTS
    assert 18 - 4 * 3 == 6 and F(3, 5) / F(9, 10) == F(2, 3) and 3 + (-5) == -2
    assert 60 == 2 ** 2 * 3 * 5 and 3 - 8 == -5 and 50 * R("1.12") == 56 and -3 * -4 == 12
    assert R("2.4") * 1000 == 2400 and 9 - (-2) == 11
    bc = math.sqrt(4 ** 2 + 2.5 ** 2)
    assert round(bc, 2) == 4.72 and round(math.degrees(math.atan(2.5 / 4))) == 32
    assert round(6 * bc, 2) == 28.30 and round(6 * bc * 1.08, 2) == 30.57
    assert math.ceil(6 * bc * 1.08 / 2) == 16 and 15 * 2 < 6 * bc * 1.08
    assert round(320 * math.pi) == 1005 and round(0.9 * 320 * math.pi / 50, 1) == 18.1
    assert 320 * F(3, 4) ** 3 == 135 and round(135 * math.pi) == 424
    assert F(3, 4) ** 3 == R("0.421875")
    r = Sc.run(SCRIPTS["s02"])
    assert sum(math.dist(a, b) for a, b in r["segs"]) == 280 and r["pos"] == (90, 0)
    assert r["env"]["c"] == 30 and 15 + 20 + 25 + 30 == 90
    assert F(3, 4) * F(1, 2) == F(3, 8) and F(1, 4) * F(1, 2) == F(1, 8)
    assert F(3, 8) + F(1, 8) == F(1, 2) and 50 * 4 - 50 * 2 == 100


S02 = S("02", "Abri, bouteille, script et jeu de hasard", [
    A(r"Calculer §18 - 4 \times 3§.", r"§18 - 12 = 6§", "6"),
    A(r"Calculer §\frac{3}{5} \div \frac{9}{10}§.",
      r"§\frac{3}{5} \times \frac{10}{9} = \frac{30}{45} = \frac{2}{3}§", r"§\frac{2}{3}§"),
    A(r"Écrire §10^3 \times 10^{-5}§ sous la forme d'une puissance de 10.",
      r"§10^{3 + (-5)} = 10^{-2}§", r"§10^{-2}§"),
    A(r"Décomposer 60 en produit de facteurs premiers.", r"§60 = 2^2 \times 3 \times 5§",
      r"§2^2 \times 3 \times 5§"),
    A(r"Factoriser §x^2 - 49§.", r"§x^2 - 7^2 = (x - 7)(x + 7)§", r"§(x - 7)(x + 7)§"),
    A(r"Résoudre l'équation §x + 8 = 3§.", r"§x = 3 - 8 = -5§", r"§x = -5§"),
    A(r"Augmenter 50 de 12 %.", r"§50 \times 1{,}12 = 56§", "56"),
    A(r"On donne §g(x) = -3x§. Déterminer l'antécédent de 12 par §g§.",
      r"§-3x = 12§ donne §x = -4§", "-4"),
    A(r"Convertir 2,4 m³ en litres.", r"§1§ m³ §= 1\,000§ L, donc §2\,400§ L", "2 400 L"),
    A(r"Donner l'étendue de la série : §-2§ ; 1 ; 4 ; 9.", r"§9 - (-2) = 11§", "11"),
], [
    X("Un abri de jardin",
      r"Le toit d'un abri est représenté par le triangle §ABC§ rectangle en §A§ : §AB = 4§ m est horizontal, §AC = 2{,}5§ m est vertical et §[BC]§ est le versant. L'abri mesure 6 m de long (perpendiculairement au dessin). [IMG:s02_abri]", [
        Q("La longueur du versant", r"Calculer §BC§, arrondie au centimètre.",
          [r"E: Pythagore dans §ABC§ rectangle en §A§ : §BC^2 = 4^2 + 2{,}5^2 = 22{,}25§",
           r"R: §BC = \sqrt{22{,}25} \approx 4{,}72§ m"], "4,72 m"),
        Q("L'angle du toit", r"Calculer l'angle §\widehat{ABC}§, arrondi au degré.",
          [r"E: §\tan \widehat{ABC} = \frac{AC}{AB} = \frac{2{,}5}{4} = 0{,}625§",
           r"R: §\widehat{ABC} \approx 32^\circ§"], "32°"),
        Q("L'aire du versant",
          r"Le versant est un rectangle de 6 m sur §BC§. Calculer son aire, arrondie au centième (utiliser §BC§ non arrondie).",
          [r"R: §6 \times \sqrt{22{,}25} \approx 28{,}30§ m²"], "28,30 m²"),
        Q("Le nombre de plaques",
          r"On ajoute 8 % à cette aire pour les découpes. Chaque plaque couvre 2 m². Combien de plaques faut-il acheter au minimum ?",
          [r"E: §28{,}30 \times 1{,}08 \approx 30{,}57§ m²",
           r"E: §30{,}57 \div 2 \approx 15{,}3§",
           r"R: Il faut 16 plaques (15 plaques ne couvrent que 30 m²)"], "16 plaques"),
    ], r"Pour couvrir un besoin, on arrondit à l'entier SUPÉRIEUR."),
    X("Une bouteille",
      r"Une bouteille est modélisée par un cylindre de rayon intérieur 4 cm et de hauteur 20 cm. Une machine la remplit avec un débit constant de 50 mL par seconde. [IMG:s02_bouteille]", [
        Q("La capacité", r"Calculer la capacité exacte de la bouteille en cm³, puis l'arrondir au mL.",
          [r"E: §V = \pi \times 4^2 \times 20 = 320\pi§ cm³",
           r"R: §320\pi \approx 1\,005§ mL (car §1§ cm³ §= 1§ mL)"], r"§320\pi§ cm³ ≈ 1 005 mL"),
        Q("La durée de remplissage",
          r"Calculer la durée nécessaire pour remplir 90 % de la bouteille, au dixième de seconde.",
          [r"E: §0{,}9 \times 320\pi = 288\pi§ mL", r"R: §\frac{288\pi}{50} \approx 18{,}1§ s"],
          "18,1 s"),
        Q("Une version réduite",
          r"Une version réduite de la bouteille a toutes ses longueurs multipliées par 0,75. Calculer sa capacité, arrondie au mL.",
          [r"E: Les volumes sont multipliés par §0{,}75^3 = 0{,}421\,875§",
           r"R: §320\pi \times 0{,}421\,875 = 135\pi \approx 424§ mL"], "424 mL"),
        Q("Pourquoi pas 75 % ?",
          r"Expliquer pourquoi cette capacité n'est pas égale à 75 % de la capacité initiale.",
          [r"R: 0,75 est le coefficient des LONGUEURS ; le volume est multiplié par §0{,}75^3 \approx 0{,}42§, soit environ 42 %"],
          "volume × 0,75³ ≈ 42 %"),
    ], r"Agrandissement ou réduction de rapport §k§ : longueurs §\times k§, aires §\times k^2§, volumes §\times k^3§."),
    X("Un script de figures",
      r"Le lutin part du point §(0\ ;\ 0)§, orienté vers la droite. Le bloc « carré » trace un carré et ramène le lutin à son point de départ, avec la même orientation. [IMG:s02_script]", [
        Q("Les côtés des carrés", r"Donner les longueurs des côtés des quatre carrés tracés.",
          [r"M: La variable c est utilisée pour tracer, PUIS augmentée de 5.",
           r"R: 10, 15, 20 et 25"], "10 ; 15 ; 20 ; 25"),
        Q("La somme des périmètres", r"Calculer la somme des périmètres des quatre carrés.",
          [r"R: §4 \times (10 + 15 + 20 + 25) = 4 \times 70 = 280§"], "280"),
        Q("La distance stylo relevé",
          r"Calculer la distance totale parcourue par le lutin stylo relevé.",
          [r"E: Au tour n, le lutin avance de c + 5 : §15 + 20 + 25 + 30§",
           r"R: §90§"], "90"),
        Q("La valeur finale de c",
          r"Quelle est la valeur de c à la fin du script ? Un carré de côté 30 est-il tracé ?",
          [r"R: c vaut §10 + 4 \times 5 = 30§, mais la boucle s'arrête après le 4e tour : aucun carré de côté 30 n'est tracé"],
          "30 ; non"),
        Q("La position finale", r"Quelle est la position finale du lutin ?",
          [r"R: Il a avancé de 90 vers la droite (les carrés le ramènent à chaque fois au point de départ) : §(90\ ;\ 0)§"],
          r"§(90\ ;\ 0)§"),
    ], r"Dans une boucle, l'ORDRE des blocs compte : ici le tracé utilise c avant son augmentation."),
    X("Un jeu à deux étapes",
      r"Une roue est partagée en 4 secteurs égaux : 3 portent la lettre A et 1 porte la lettre B. Un sac contient une boule rouge et une boule bleue. On fait tourner la roue, puis on tire une boule au hasard. Le joueur gagne s'il obtient « A et rouge » ou « B et bleue ». [IMG:s02_arbre]", [
        Q("Les deux chemins gagnants",
          r"Calculer la probabilité de chacun des deux chemins gagnants.",
          [r"E: « A et rouge » : §\frac{3}{4} \times \frac{1}{2} = \frac{3}{8}§",
           r"R: « B et bleue » : §\frac{1}{4} \times \frac{1}{2} = \frac{1}{8}§"],
          r"§\frac{3}{8}§ et §\frac{1}{8}§"),
        Q("La probabilité de gagner", r"En déduire la probabilité de gagner.",
          [r"R: §\frac{3}{8} + \frac{1}{8} = \frac{4}{8} = \frac{1}{2}§"], r"§\frac{1}{2}§"),
        Q("Cent parties", r"Sur 100 parties, est-on certain de gagner exactement 50 fois ?",
          [r"R: Non : une probabilité de §\frac{1}{2}§ indique qu'on gagne ENVIRON une fois sur deux sur un grand nombre de parties, sans garantie"],
          "non"),
        Q("Le bilan en points",
          r"Une partie coûte 2 points ; un gain rapporte 6 points. Un joueur fait 100 parties et gagne 50 fois. Calculer son bilan, puis le bilan moyen par partie.",
          [r"E: Gains : §50 \times 6 = 300§ points ; participations : §100 \times 2 = 200§ points",
           r"R: Bilan : §300 - 200 = 100§ points, soit 1 point par partie en moyenne"],
          "100 points (1 par partie)"),
    ], r"Des chemins INCOMPATIBLES menant au même événement : on additionne leurs probabilités."),
], check02)


# ============================================================== SUJET 03

def check03():
    assert (-3) * (-4) + 2 == 14 and F(3, 4) - F(1, 3) == F(5, 12) and 2 ** 3 * 2 ** 4 == 2 ** 7
    assert 91 == 7 * 13 and 3 * (2 * 5 + 3) == 6 * 5 + 9 and 2 * 7 - 5 == 9
    assert 40 * R("0.75") == 30 and -2 * 3 + 5 == -1 and 72000 / 3600 == 20
    assert F(3, 6) == F(1, 2)
    assert 12600 / 45 == 280 and R("0.15") * 12600 == 1890 and (12600 - 1890) / 45 == 238
    assert R(238) / 4 == R("59.5") and R(10710, 40) == R("267.75") and R("267.75") / 238 == R("1.125")
    assert 90 * 2 == 180 and 300 / 4 == 75 and 180 + 80 * 1.5 == 300
    assert F(2, R("9.6")) * R("7.2") == R("1.5") and R("1.5") * R("9.6") / 2 == R("7.2")
    assert R("9.6") ** 2 + R("7.2") ** 2 == 144 and round(math.degrees(math.atan(0.75))) == 37
    assert 18 + 12 + 10 + 8 == 48 and F(18, 48) == R("0.375") and R("0.375") * 360 == 135
    assert F(40, 48) == F(5, 6) and F(22, 48) == F(11, 24)


S03 = S("03", "Le voyage scolaire", [
    A(r"Calculer §(-3) \times (-4) + 2§.", r"§12 + 2 = 14§", "14"),
    A(r"Calculer §\frac{3}{4} - \frac{1}{3}§.", r"§\frac{9}{12} - \frac{4}{12} = \frac{5}{12}§",
      r"§\frac{5}{12}§"),
    A(r"Écrire §2^3 \times 2^4§ sous la forme d'une puissance de 2.", r"§2^{3 + 4} = 2^7§",
      r"§2^7§"),
    A(r"Le nombre 91 est-il premier ?", r"Non : §91 = 7 \times 13§", "non (7 × 13)"),
    A(r"Factoriser §6x + 9§.", r"§3 \times 2x + 3 \times 3 = 3(2x + 3)§", r"§3(2x + 3)§"),
    A(r"Résoudre l'équation §2x - 5 = 9§.", r"§2x = 14§, donc §x = 7§", r"§x = 7§"),
    A(r"Un article à 40 € baisse de 25 %. Quel est son nouveau prix ?",
      r"§40 \times 0{,}75 = 30§ €", "30 €"),
    A(r"On donne §f(x) = -2x + 5§. Calculer l'image de 3.", r"§-6 + 5 = -1§", "-1"),
    A(r"Convertir 72 km/h en m/s.", r"§\frac{72\,000 \text{ m}}{3\,600 \text{ s}} = 20§ m/s",
      "20 m/s"),
    A(r"On lance un dé équilibré à 6 faces. Quelle est la probabilité d'obtenir un nombre pair ?",
      r"3 issues favorables (2 ; 4 ; 6) sur 6 : §\frac{1}{2}§", r"§\frac{1}{2}§"),
], [
    X("Le budget du voyage",
      r"Un voyage scolaire coûte 12 600 € au total pour 45 élèves.", [
        Q("Le coût par élève", r"Calculer le coût du voyage par élève.",
          [r"R: §\frac{12\,600}{45} = 280§ €"], "280 €"),
        Q("La subvention",
          r"La région prend en charge 15 % du coût total. Calculer le montant de la subvention, puis la somme payée par chaque élève.",
          [r"E: Subvention : §0{,}15 \times 12\,600 = 1\,890§ €",
           r"E: Reste à payer : §12\,600 - 1\,890 = 10\,710§ €",
           r"R: Par élève : §\frac{10\,710}{45} = 238§ €"], "1 890 € ; 238 €"),
        Q("Les mensualités",
          r"Chaque famille paie en 4 mensualités égales. Calculer le montant d'une mensualité.",
          [r"R: §\frac{238}{4} = 59{,}50§ €"], "59,50 €"),
        Q("Cinq élèves de moins",
          r"Finalement, seuls 40 élèves partent ; le coût total et la subvention ne changent pas. Calculer la nouvelle somme payée par élève et le pourcentage d'augmentation.",
          [r"E: §\frac{10\,710}{40} = 267{,}75§ €",
           r"R: §\frac{267{,}75}{238} = 1{,}125§ : augmentation de 12,5 %"],
          "267,75 € ; +12,5 %"),
    ], r"Augmenter de §t\ \%§ revient à multiplier par §1 + \frac{t}{100}§ ; un coefficient de 1,125 correspond à +12,5 %."),
    X("Le trajet en car",
      r"Le car part à 7 h 00. Le graphique donne la distance parcourue en fonction de la durée du trajet. [IMG:s03_trajet]", [
        Q("La distance après 2 h", r"Quelle distance le car a-t-il parcourue au bout de 2 h ?",
          [r"R: Lecture graphique : 180 km"], "180 km"),
        Q("La pause", r"Le car fait une pause. Combien de temps dure-t-elle ?",
          [r"R: La distance reste égale à 180 km entre 2 h et 2 h 30 : la pause dure 30 min"],
          "30 min"),
        Q("La vitesse au départ", r"Calculer la vitesse moyenne du car pendant les deux premières heures.",
          [r"R: §\frac{180}{2} = 90§ km/h"], "90 km/h"),
        Q("L'heure d'arrivée", r"Le trajet mesure 300 km. À quelle heure le car arrive-t-il ?",
          [r"E: La distance 300 km est atteinte après 4 h de trajet", r"R: §7 \text{ h} + 4 \text{ h} = 11§ h 00"],
          "11 h 00"),
        Q("La vitesse moyenne totale", r"Calculer la vitesse moyenne sur l'ensemble du trajet, pause comprise.",
          [r"R: §\frac{300}{4} = 75§ km/h"], "75 km/h"),
    ], r"Sur un graphique distance–temps, un palier horizontal correspond à un ARRÊT."),
    X("La hauteur d'une statue",
      r"Au même instant, l'ombre d'une statue verticale §[ST]§ et celle d'un bâton vertical §[BH]§ de 1,5 m se terminent au même point §O§. On mesure §SO = 9{,}6§ m et §BO = 2§ m. Les points §S§, §B§, §O§ sont alignés, ainsi que §T§, §H§, §O§. [IMG:s03_statue]", [
        Q("Des droites parallèles", r"Justifier que les droites §(BH)§ et §(ST)§ sont parallèles.",
          [r"R: Elles sont toutes deux perpendiculaires au sol (verticales) : elles sont donc parallèles"],
          "toutes deux ⟂ au sol"),
        Q("La hauteur de la statue", r"Calculer la hauteur §ST§ de la statue.",
          [r"M: Théorème de Thalès dans les triangles §OBH§ et §OST§.",
           r"E: §\frac{OB}{OS} = \frac{BH}{ST}§, soit §\frac{2}{9{,}6} = \frac{1{,}5}{ST}§",
           r"R: §ST = \frac{1{,}5 \times 9{,}6}{2} = 7{,}2§ m"], "7,2 m"),
        Q("La longueur §OT§", r"Calculer la longueur §OT§.",
          [r"E: Le triangle §OST§ est rectangle en §S§ : §OT^2 = 9{,}6^2 + 7{,}2^2 = 92{,}16 + 51{,}84 = 144§",
           r"R: §OT = 12§ m"], "12 m"),
        Q("La hauteur du soleil", r"Calculer l'angle §\widehat{SOT}§, arrondi au degré.",
          [r"E: §\tan \widehat{SOT} = \frac{ST}{SO} = \frac{7{,}2}{9{,}6} = 0{,}75§",
           r"R: §\widehat{SOT} \approx 37^\circ§"], "37°"),
    ], r"Deux droites perpendiculaires à une même droite sont parallèles : c'est souvent l'hypothèse cachée de Thalès."),
    X("Le choix des activités",
      r"Les 48 élèves ont choisi une activité. Les résultats sont saisis dans une feuille de calcul. [IMG:s03_tableur]", [
        Q("La formule du total", r"Quelle formule saisir en B6 pour obtenir le nombre total d'élèves ?",
          [r"R: =SOMME(B2:B5) (ou =B2+B3+B4+B5), qui affiche 48"], "=SOMME(B2:B5)"),
        Q("La fréquence du musée", r"Calculer la fréquence de l'activité « Musée », en pourcentage.",
          [r"R: §\frac{18}{48} = 0{,}375§, soit 37,5 %"], "37,5 %"),
        Q("Le diagramme circulaire",
          r"Dans un diagramme circulaire, quel angle correspond à l'activité « Musée » ?",
          [r"R: §0{,}375 \times 360 = 135^\circ§"], "135°"),
        Q("Un élève au hasard",
          r"On choisit un élève au hasard. Quelle est la probabilité qu'il n'ait pas choisi la plage ?",
          [r"R: §\frac{48 - 8}{48} = \frac{40}{48} = \frac{5}{6}§"], r"§\frac{5}{6}§"),
        Q("Parc ou spectacle",
          r"Quelle est la probabilité qu'il ait choisi le parc ou le spectacle ?",
          [r"R: §\frac{12 + 10}{48} = \frac{22}{48} = \frac{11}{24}§"], r"§\frac{11}{24}§"),
    ], r"Diagramme circulaire : angle = fréquence §\times 360^\circ§."),
], check03)


# ============================================================== SUJET 04

def check04():
    import scratch3e as Sc
    from scripts_brevet import SCRIPTS
    assert 5 - 2 * (3 - 7) == 13 and F(2, 5) * F(15, 4) == F(3, 2) and 3.2e-4 == 0.00032
    assert 4 * 3 == 12 and 3 * -5 + 4 == -5 - 6 and 64 / R("0.8") == 80 and (-4) ** 2 == 16
    assert R("3.5") * 10000 == 35000 and (8 + 12 + 10 + 14) / 4 == 11
    assert 12 ** 2 + 9 ** 2 == 15 ** 2 and 9 * 6 / 2 == 27 and 12 * 9 - 27 == 81
    assert math.ceil(81 / 25) == 4 and 4 * R("7.9") == R("31.6") and 2 * (12 + 9) == 42
    assert math.ceil(42 / 10) == 5
    v = math.pi * 0.8 ** 2 * 1.5
    assert round(v, 3) == 3.016 and round(v * 1000) == 3016 and 60 * 12 == 720
    assert round(3016 / 60, 1) == 50.3 and round(0.72 / (math.pi * 0.64), 2) == 0.36
    assert round(5.2 * math.sin(math.radians(35)), 2) == 2.98
    gf = 5.2 * math.cos(math.radians(35))
    assert round(gf, 2) == 4.26 and round(2 * gf, 2) == 8.52 and 180 - 2 * 35 == 110
    for x, r in [("5", 16), ("-3", 0), ("3", 0), ("7", 40), ("-7", 40)]:
        assert Sc.run(SCRIPTS["s04"], [x])["out"] == [r]


S04 = S("04", "La maison et le jardin", [
    A(r"Calculer §5 - 2 \times (3 - 7)§.", r"§5 - 2 \times (-4) = 5 + 8 = 13§", "13"),
    A(r"Calculer §\frac{2}{5} \times \frac{15}{4}§.", r"§\frac{30}{20} = \frac{3}{2}§",
      r"§\frac{3}{2}§"),
    A(r"Donner l'écriture scientifique de 0,000 32.", r"§3{,}2 \times 10^{-4}§",
      r"§3{,}2 \times 10^{-4}§"),
    A(r"Calculer §(2\sqrt{3})^2§.", r"§2^2 \times (\sqrt{3})^2 = 4 \times 3 = 12§", "12"),
    A(r"Développer et réduire §(x + 2)(x - 3)§.", r"§x^2 - 3x + 2x - 6 = x^2 - x - 6§",
      r"§x^2 - x - 6§"),
    A(r"Résoudre l'équation §3x + 4 = x - 6§.", r"§2x = -10§, donc §x = -5§", r"§x = -5§"),
    A(r"Après une remise de 20 %, un article coûte 64 €. Quel était son prix initial ?",
      r"§64 \div 0{,}8 = 80§ €", "80 €"),
    A(r"On donne §f(x) = x^2§. Calculer §f(-4)§.", r"§(-4)^2 = 16§", "16"),
    A(r"Convertir 3,5 m² en cm².", r"§1§ m² §= 10\,000§ cm², donc §35\,000§ cm²",
      "35 000 cm²"),
    A(r"Calculer la moyenne de 8 ; 12 ; 10 ; 14.", r"§\frac{44}{4} = 11§", "11"),
], [
    X("Le jardin",
      r"Un jardin a la forme du rectangle §ABCD§ avec §AB = 12§ m et §BC = 9§ m. Le point §E§ est le milieu de §[CD]§. Le triangle §ADE§ est un massif de fleurs, le reste est en pelouse ; une allée suit la diagonale §[AC]§. [IMG:s04_jardin]", [
        Q("La longueur de l'allée", r"Calculer la longueur de l'allée §[AC]§.",
          [r"E: Pythagore dans §ABC§ rectangle en §B§ : §AC^2 = 12^2 + 9^2 = 225§",
           r"R: §AC = 15§ m"], "15 m"),
        Q("L'aire du massif", r"Calculer l'aire du massif §ADE§.",
          [r"E: §ADE§ est rectangle en §D§, avec §AD = 9§ m et §DE = 6§ m",
           r"R: §\frac{9 \times 6}{2} = 27§ m²"], "27 m²"),
        Q("L'aire de la pelouse", r"Calculer l'aire de la pelouse.",
          [r"R: §12 \times 9 - 27 = 108 - 27 = 81§ m²"], "81 m²"),
        Q("Le gazon",
          r"Il faut 1 kg de graines pour 25 m² de pelouse ; les graines sont vendues en sacs de 1 kg à 7,90 €. Calculer la dépense.",
          [r"E: §81 \div 25 = 3{,}24§ : il faut 4 sacs", r"R: §4 \times 7{,}90 = 31{,}60§ €"],
          "31,60 €"),
        Q("La clôture",
          r"On clôture tout le tour du jardin avec des rouleaux de grillage de 10 m. Combien de rouleaux faut-il ?",
          [r"E: Périmètre : §2 \times (12 + 9) = 42§ m", r"R: §42 \div 10 = 4{,}2§ : 5 rouleaux"],
          "5 rouleaux"),
    ], r"Aire d'un triangle rectangle : produit des côtés de l'angle droit divisé par 2."),
    X("La citerne de récupération",
      r"Une citerne cylindrique a pour rayon 0,8 m et pour hauteur 1,5 m. Elle recueille l'eau de pluie d'un toit de 60 m². Une pluie de 1 mm apporte 1 L d'eau par m² de toit. [IMG:s04_citerne]", [
        Q("Le volume de la citerne",
          r"Calculer le volume exact de la citerne en m³, puis sa contenance arrondie au litre.",
          [r"E: §V = \pi \times 0{,}8^2 \times 1{,}5 = 0{,}96\pi§ m³", r"R: §\approx 3{,}016§ m³, soit 3 016 L"],
          r"§0{,}96\pi§ m³ ≈ 3 016 L"),
        Q("Une pluie de 12 mm", r"Combien de litres une pluie de 12 mm apporte-t-elle ?",
          [r"R: §60 \times 12 = 720§ L"], "720 L"),
        Q("La fonction volume",
          r"On note §V(p)§ le volume (en L) recueilli pour §p§ mm de pluie. Exprimer §V(p)§ ; de quel type de fonction s'agit-il ?",
          [r"R: §V(p) = 60p§ : c'est une fonction linéaire"], r"§V(p) = 60p§ (linéaire)"),
        Q("Remplir la citerne", r"Quelle hauteur de pluie remplit la citerne vide ?",
          [r"R: §60p = 3\,016§ donne §p \approx 50{,}3§ mm"], "≈ 50,3 mm"),
        Q("La hauteur d'eau",
          r"Après une pluie de 12 mm (citerne vide au départ), quelle est la hauteur d'eau dans la citerne, au centimètre ?",
          [r"E: §720§ L §= 0{,}72§ m³ et l'aire de la base vaut §0{,}64\pi§ m²",
           r"R: §h = \frac{0{,}72}{0{,}64\pi} \approx 0{,}36§ m, soit 36 cm"], "36 cm"),
    ], r"Volume d'un cylindre : §\pi r^2 h§ ; §1§ m³ §= 1\,000§ L."),
    X("La charpente",
      r"La section du toit est le triangle §GSD§ isocèle en §S§, avec §GS = 5{,}2§ m et §\widehat{SGD} = 35^\circ§. §F§ est le milieu de §[GD]§. [IMG:s04_toit]", [
        Q("Une hauteur", r"Pourquoi la droite §(SF)§ est-elle perpendiculaire à §(GD)§ ?",
          [r"R: Dans un triangle isocèle, la médiane issue du sommet principal est aussi une hauteur : §(SF) \perp (GD)§"],
          "médiane = hauteur"),
        Q("La hauteur du toit", r"Calculer §SF§, arrondie au centimètre.",
          [r"E: Dans §SGF§ rectangle en §F§ : §\sin \widehat{SGF} = \frac{SF}{GS}§",
           r"R: §SF = 5{,}2 \times \sin 35^\circ \approx 2{,}98§ m"], "2,98 m"),
        Q("La largeur du toit", r"Calculer §GF§ puis §GD§, arrondies au centimètre.",
          [r"E: §GF = 5{,}2 \times \cos 35^\circ \approx 4{,}26§ m",
           r"R: §GD = 2 \times GF \approx 8{,}52§ m"], "4,26 m et 8,52 m"),
        Q("L'angle au sommet", r"Calculer l'angle §\widehat{GSD}§.",
          [r"R: Les angles à la base sont égaux : §180 - 2 \times 35 = 110^\circ§"], "110°"),
    ], r"Triangle isocèle : angles à la base égaux, et la hauteur issue du sommet coupe la base en son milieu."),
    X("Un programme de calcul",
      r"On considère le script suivant. [IMG:s04_script]", [
        Q("Avec 5", r"Quel résultat le lutin dit-il si l'on choisit 5 ?",
          [r"R: a = 2, b = 8 et §r = 2 \times 8 = 16§"], "16"),
        Q("Avec §-3§", r"Quel résultat obtient-on avec §-3§ ?",
          [r"R: a = §-6§, b = 0 et §r = 0§"], "0"),
        Q("L'expression", r"Exprimer le résultat en fonction du nombre §x§ choisi, puis développer.",
          [r"R: §r = (x - 3)(x + 3) = x^2 - 9§"], r"§x^2 - 9§"),
        Q("Obtenir 0", r"Quels nombres faut-il choisir pour obtenir 0 ?",
          [r"R: Un produit est nul si l'un des facteurs est nul : §x = 3§ ou §x = -3§"],
          r"§3§ et §-3§"),
        Q("Obtenir 40", r"Quels nombres faut-il choisir pour obtenir 40 ?",
          [r"E: §x^2 - 9 = 40§, soit §x^2 = 49§", r"R: §x = 7§ ou §x = -7§"], r"§7§ et §-7§"),
    ], r"Une équation produit nul se résout facteur par facteur ; §x^2 = a§ (avec §a > 0§) a deux solutions."),
], check04)


# ============================================================== SUJET 05

def check05():
    assert -2 - (-9) == 7 and F(7, 8) * 64 == 56 and (10 ** 2) ** 3 == 10 ** 6
    assert [d for d in range(1, 19) if 18 % d == 0] == [1, 2, 3, 6, 9, 18]
    assert R("2.5") * 4 == 10 and R("0.3") * 250 == 75 and F(7, 2) * 2 == 7
    assert R("1.75") == 1 + F(45, 60) and F(5, 10) == F(1, 2)
    A_, B_, C_ = (lambda n: 15 * n), (lambda n: 20 + 10 * n), (lambda n: 60)
    assert (A_(3), B_(3), C_(3)) == (45, 50, 60) and [n for n in range(1, 11) if B_(n) < A_(n)][0] == 5
    assert (A_(7), B_(7), C_(7)) == (105, 90, 60) and A_(4) == B_(4) == C_(4) == 60
    assert all(C_(n) < min(A_(n), B_(n)) for n in range(5, 11))
    assert 1200 / 50 == 24 and 800 / 50 == 16 and 12 * 8 == 96 and 24 * 16 == 384
    assert 960000 / 2500 == 384 and 6 ** 2 + 8 ** 2 == 10 ** 2
    assert round(math.degrees(math.atan(8 / 6))) == 53
    t = 4200 + 6800 + 5400
    assert t == 16400 and round(t / 3) == 5467 and round(2600 / 4200 * 100, 1) == 61.9
    assert round(5400 / t * 100, 1) == 32.9 and t * R("1.08") == 17712
    assert F(1, 500) == R("0.002") and F(50, 500) == F(1, 10)
    assert 300 + 9 * 40 + 40 * 5 == 860 and 500 * 2 - 860 == 140
    assert math.ceil(F(1260, 500) * 100) / 100 == 2.52 and 500 * R("2.52") - 860 >= 400
    assert 500 * R("2.51") - 860 < 400


S05 = S("05", "Le festival de musique", [
    A(r"Calculer §-2 - (-9)§.", r"§-2 + 9 = 7§", "7"),
    A(r"Calculer les §\frac{7}{8}§ de 64.", r"§64 \div 8 \times 7 = 56§", "56"),
    A(r"Écrire §(10^2)^3§ sous la forme d'une puissance de 10.", r"§10^{2 \times 3} = 10^6§",
      r"§10^6§"),
    A(r"Donner la liste des diviseurs de 18.", r"1 ; 2 ; 3 ; 6 ; 9 ; 18", "1 ; 2 ; 3 ; 6 ; 9 ; 18"),
    A(r"Factoriser §x^2 + 5x§.", r"§x(x + 5)§", r"§x(x + 5)§"),
    A(r"Résoudre l'équation §\frac{x}{4} = 2{,}5§.", r"§x = 2{,}5 \times 4 = 10§", r"§x = 10§"),
    A(r"Calculer 30 % de 250.", r"§0{,}3 \times 250 = 75§", "75"),
    A(r"§f§ est une fonction linéaire telle que §f(2) = 7§. Donner l'expression de §f(x)§.",
      r"§f(x) = ax§ avec §2a = 7§ : §f(x) = 3{,}5x§", r"§f(x) = 3{,}5x§"),
    A(r"Convertir 1 h 45 min en heures (écriture décimale).",
      r"§45§ min §= \frac{45}{60}§ h §= 0{,}75§ h, donc 1,75 h", "1,75 h"),
    A(r"Une urne contient 3 boules rouges, 5 vertes et 2 jaunes. On tire une boule au hasard. Probabilité qu'elle soit verte ?",
      r"§\frac{5}{10} = \frac{1}{2}§", r"§\frac{1}{2}§"),
], [
    X("Trois formules de billetterie",
      r"Un festival propose trois formules pour §n§ concerts : formule A, 15 € par concert ; formule B, une carte à 20 € puis 10 € par concert ; formule C, un pass illimité à 60 €. [IMG:s05_tarifs]", [
        Q("Trois concerts", r"Calculer le prix de 3 concerts avec chaque formule.",
          [r"R: A : §45§ € ; B : §20 + 30 = 50§ € ; C : §60§ €"], "45 € ; 50 € ; 60 €"),
        Q("Les expressions", r"Exprimer le prix de §n§ concerts avec chaque formule.",
          [r"R: §A(n) = 15n§ ; §B(n) = 20 + 10n§ ; §C(n) = 60§"],
          r"§15n§ ; §20 + 10n§ ; §60§"),
        Q("Comparer A et B", r"Résoudre l'inéquation §20 + 10n < 15n§ et interpréter.",
          [r"E: §20 < 5n§, donc §n > 4§",
           r"R: La formule B est moins chère que la formule A à partir de 5 concerts"],
          r"§n > 4§"),
        Q("Sept concerts", r"Quelle est la formule la plus avantageuse pour 7 concerts ?",
          [r"R: A : 105 € ; B : 90 € ; C : 60 € : la formule C"], "C (60 €)"),
        Q("Le pass illimité",
          r"À partir de combien de concerts le pass C est-il strictement le moins cher ?",
          [r"E: Pour 4 concerts, les trois formules coûtent 60 €",
           r"R: À partir de 5 concerts, C est strictement la moins chère"], "5 concerts"),
    ], r"Graphiquement, la formule la moins chère correspond à la droite la plus BASSE."),
    X("La scène et sa maquette",
      r"La scène est un rectangle de 12 m sur 8 m. Le régisseur en construit une maquette à l'échelle §\frac{1}{50}§. Un projecteur est fixé à 6 m au-dessus du sol de la scène.", [
        Q("Les dimensions de la maquette",
          r"Calculer les dimensions de la maquette, en centimètres.",
          [r"R: §1\,200 \div 50 = 24§ cm et §800 \div 50 = 16§ cm"], "24 cm × 16 cm"),
        Q("Les aires", r"Calculer l'aire réelle de la scène, puis l'aire de la maquette.",
          [r"E: Réelle : §12 \times 8 = 96§ m²", r"R: Maquette : §24 \times 16 = 384§ cm²"],
          "96 m² ; 384 cm²"),
        Q("Le rapport des aires",
          r"Par quel nombre faut-il diviser l'aire réelle pour obtenir l'aire de la maquette ? Vérifier.",
          [r"E: §50^2 = 2\,500§",
           r"R: §96§ m² §= 960\,000§ cm² et §960\,000 \div 2\,500 = 384§ cm² ✔️"], "2 500"),
        Q("La longueur du faisceau",
          r"Le projecteur éclaire un point de la scène situé à 8 m (horizontalement) du pied de son support vertical. Calculer la longueur du faisceau.",
          [r"R: Pythagore : §\sqrt{6^2 + 8^2} = \sqrt{100} = 10§ m"], "10 m"),
        Q("L'angle du faisceau",
          r"Calculer l'angle entre le faisceau et le support vertical, au degré.",
          [r"R: §\tan \alpha = \frac{8}{6}§, donc §\alpha \approx 53^\circ§"], "53°"),
    ], r"Échelle §\frac{1}{50}§ : longueurs divisées par 50, aires divisées par §50^2 = 2\,500§."),
    X("La fréquentation",
      r"Le diagramme donne le nombre de spectateurs pour chacun des trois jours du festival. [IMG:s05_frequentation]", [
        Q("Le total", r"Calculer le nombre total de spectateurs.",
          [r"R: §4\,200 + 6\,800 + 5\,400 = 16\,400§"], "16 400"),
        Q("La moyenne", r"Calculer le nombre moyen de spectateurs par jour, arrondi à l'unité.",
          [r"R: §\frac{16\,400}{3} \approx 5\,467§"], "5 467"),
        Q("Du vendredi au samedi",
          r"Calculer le pourcentage d'augmentation du vendredi au samedi, arrondi au dixième.",
          [r"E: Augmentation : §6\,800 - 4\,200 = 2\,600§",
           r"R: §\frac{2\,600}{4\,200} \approx 0{,}619§, soit environ 61,9 %"], "61,9 %"),
        Q("La part du dimanche",
          r"Quel pourcentage des spectateurs est venu le dimanche ? Arrondir au dixième.",
          [r"R: §\frac{5\,400}{16\,400} \approx 32{,}9§ %"], "32,9 %"),
        Q("L'an prochain",
          r"Les organisateurs prévoient 8 % de spectateurs en plus l'an prochain. Combien en attendent-ils ?",
          [r"R: §16\,400 \times 1{,}08 = 17\,712§"], "17 712"),
    ], r"Pourcentage d'évolution : §\frac{\text{valeur finale} - \text{valeur initiale}}{\text{valeur initiale}}§."),
    X("La tombola",
      r"Une tombola met en vente 500 billets à 2 € chacun. Les lots sont : 1 gros lot de 300 €, 9 lots de 40 € et 40 lots de 5 €. On achète un billet au hasard ; tous les billets sont vendus.", [
        Q("Le gros lot", r"Quelle est la probabilité de gagner le gros lot ?",
          [r"R: §\frac{1}{500} = 0{,}002§"], r"§\frac{1}{500}§"),
        Q("Gagner un lot", r"Quelle est la probabilité de gagner un lot ?",
          [r"R: §\frac{1 + 9 + 40}{500} = \frac{50}{500} = \frac{1}{10}§"], r"§\frac{1}{10}§"),
        Q("Ne rien gagner", r"Quelle est la probabilité de ne rien gagner ?",
          [r"R: Événement contraire : §1 - \frac{1}{10} = \frac{9}{10}§"], r"§\frac{9}{10}§"),
        Q("Le bénéfice", r"Calculer la recette, le coût des lots et le bénéfice de l'organisateur.",
          [r"E: Recette : §500 \times 2 = 1\,000§ € ; lots : §300 + 360 + 200 = 860§ €",
           r"R: Bénéfice : §1\,000 - 860 = 140§ €"], "140 €"),
        Q("Le prix minimal du billet",
          r"Quel prix minimal, au centime, faudrait-il fixer pour un bénéfice d'au moins 400 € ?",
          [r"E: §500p - 860 \geq 400§, soit §p \geq 2{,}52§",
           r"R: 2,52 € (avec 2,51 €, le bénéfice ne serait que 395 €)"], "2,52 €"),
    ], r"La probabilité d'un événement contraire est §1 - p§."),
], check05)


SUJETS = [S01, S02, S03, S04, S05]
