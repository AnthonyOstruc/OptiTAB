# -*- coding: utf-8 -*-
"""Sujets type brevet 06 à 10 (contenu + contrôles)."""
import math
from fractions import Fraction as F

from brevet_3e import A, Q, X, S

R = F


# ============================================================== SUJET 06

def check06():
    import scratch3e as Sc
    from scripts_brevet import SCRIPTS
    assert 4 * R("-2.5") == -10 and 1 - F(3, 7) == F(4, 7) and 5 * 10 ** 3 + 2 * 10 ** 2 == 5200
    assert math.sqrt(9 + 16) == 5 and 4 * (4 - 1) == 12 and 150 / 2 == 75 and 3 * 5 - 4 == 11
    assert 1 - R("0.35") == R("0.65")
    v = 80 * 35 * 40
    assert v == 112000 and R("0.9") * 112 == R("100.8") and R("100.8") + 25 + 12 == R("137.8")
    assert R("100.8") / R("0.8") == 126 and 126 == 2 * 60 + 6 and 100800 / (80 * 35) == 36
    assert 5000 * 2 ** 3 == 40000 and 5000 * 2 ** 9 == 2560000
    assert math.isclose(2.56e6 * 2e-6, 5.12)
    assert R("0.015") * 400 == 6 and R("9.2") / 400 == R("0.023") and 400 ** 2 == 160000
    assert R("1.5e-4") * 160000 == 24 and R("0.015") / 1000 == R("1.5e-5")
    r = Sc.run(SCRIPTS["s06"])
    assert r["out"] == [160] and r["env"]["n"] == 1280000
    n, t, etats = 5000, 0, []
    for _ in range(3):
        n, t = n * 2, t + 20
        etats.append((n, t))
    assert etats == [(10000, 20), (20000, 40), (40000, 60)]
    k = 0
    while 5000 * 2 ** k <= 10 ** 7:
        k += 1
    assert k == 11 and 20 * k == 220


S06 = S("06", "Aquarium et laboratoire", [
    A(r"Calculer §4 \times (-2{,}5)§.", r"§-10§", r"§-10§"),
    A(r"Calculer §1 - \frac{3}{7}§.", r"§\frac{7}{7} - \frac{3}{7} = \frac{4}{7}§",
      r"§\frac{4}{7}§"),
    A(r"Calculer §5 \times 10^3 + 2 \times 10^2§.", r"§5\,000 + 200 = 5\,200§", "5 200"),
    A(r"Calculer §\sqrt{9 + 16}§.", r"§\sqrt{25} = 5§", "5"),
    A(r"Développer §(x - 5)^2§.", r"§x^2 - 10x + 25§", r"§x^2 - 10x + 25§"),
    A(r"Résoudre l'équation §4(x - 1) = 12§.", r"§x - 1 = 3§, donc §x = 4§", r"§x = 4§"),
    A(r"Un train parcourt 150 km en 2 h. Quelle est sa vitesse moyenne ?",
      r"§\frac{150}{2} = 75§ km/h", "75 km/h"),
    A(r"On donne §f(x) = 3x - 4§. Déterminer l'antécédent de 11.",
      r"§3x - 4 = 11§, §3x = 15§, §x = 5§", "5"),
    A(r"Combien de cm³ y a-t-il dans 1 L ?", r"§1§ L §= 1§ dm³ §= 1\,000§ cm³", "1 000"),
    A(r"Un événement a une probabilité de 0,35. Quelle est la probabilité de l'événement contraire ?",
      r"§1 - 0{,}35 = 0{,}65§", "0,65"),
], [
    X("L'aquarium",
      r"Un aquarium a la forme d'un pavé droit de 80 cm de long, 35 cm de large et 40 cm de haut. [IMG:s06_aquarium]", [
        Q("Le volume", r"Calculer le volume de l'aquarium en cm³, puis en litres.",
          [r"R: §80 \times 35 \times 40 = 112\,000§ cm³ §= 112§ L"], "112 L"),
        Q("Rempli à 90 %", r"On le remplit à 90 %. Quel volume d'eau contient-il ?",
          [r"R: §0{,}9 \times 112 = 100{,}8§ L"], "100,8 L"),
        Q("Le meuble",
          r"1 L d'eau pèse 1 kg. L'aquarium vide pèse 25 kg et le gravier 12 kg. Le meuble supporte au maximum 150 kg. Est-ce suffisant ?",
          [r"E: Masse totale : §100{,}8 + 25 + 12 = 137{,}8§ kg",
           r"R: §137{,}8 < 150§ : le meuble convient"], "oui (137,8 kg)"),
        Q("La vidange",
          r"Pour le nettoyer, on vide l'eau avec une pompe de débit 0,8 L/min. Combien de temps faut-il ?",
          [r"R: §\frac{100{,}8}{0{,}8} = 126§ min, soit 2 h 06 min"], "2 h 06 min"),
        Q("La hauteur d'eau", r"Quelle est la hauteur de l'eau quand l'aquarium est rempli à 90 % ?",
          [r"R: §\frac{100\,800}{80 \times 35} = 36§ cm"], "36 cm"),
    ], r"§1§ L §= 1\,000§ cm³ ; volume = aire de la base §\times§ hauteur."),
    X("Des bactéries",
      r"Une culture contient 5 000 bactéries au départ. Leur nombre double toutes les 20 minutes.", [
        Q("Après une heure", r"Combien y a-t-il de bactéries au bout d'une heure ?",
          [r"E: Une heure = 3 périodes de 20 min", r"R: §5\,000 \times 2^3 = 40\,000 = 4 \times 10^4§"],
          r"§4 \times 10^4§"),
        Q("Après trois heures",
          r"Combien y en a-t-il au bout de 3 heures ? Donner l'écriture scientifique.",
          [r"R: 9 périodes : §5\,000 \times 2^9 = 2\,560\,000 = 2{,}56 \times 10^6§"],
          r"§2{,}56 \times 10^6§"),
        Q("L'expression", r"Exprimer le nombre de bactéries après §n§ périodes de 20 minutes.",
          [r"R: §5\,000 \times 2^n§"], r"§5\,000 \times 2^n§"),
        Q("Mises bout à bout",
          r"Une bactérie mesure §2 \times 10^{-6}§ m. Quelle longueur obtiendrait-on en alignant les bactéries présentes au bout de 3 heures ?",
          [r"R: §2{,}56 \times 10^6 \times 2 \times 10^{-6} = 5{,}12§ m"], "5,12 m"),
    ], r"Doubler §n§ fois revient à multiplier par §2^n§ : la croissance est très rapide."),
    X("Au microscope",
      r"Un microscope agrandit les objets 400 fois.", [
        Q("Une cellule de 0,015 mm", r"Une cellule mesure 0,015 mm. Quelle est sa taille sur l'image ?",
          [r"R: §0{,}015 \times 400 = 6§ mm"], "6 mm"),
        Q("La taille réelle",
          r"Sur l'image, une autre cellule mesure 9,2 mm. Quelle est sa taille réelle, en mm puis en µm ?",
          [r"E: §\frac{9{,}2}{400} = 0{,}023§ mm", r"R: §0{,}023§ mm §= 23§ µm (car 1 mm = 1 000 µm)"],
          "0,023 mm = 23 µm"),
        Q("Les aires", r"Par quel nombre les aires sont-elles multipliées sur l'image ?",
          [r"R: §400^2 = 160\,000§"], "160 000"),
        Q("Une aire sur l'image",
          r"Une cellule a une aire réelle de §1{,}5 \times 10^{-4}§ mm². Quelle est son aire sur l'image ?",
          [r"R: §1{,}5 \times 10^{-4} \times 160\,000 = 24§ mm²"], "24 mm²"),
        Q("En mètres", r"Écrire 0,015 mm en mètres, en notation scientifique.",
          [r"R: §0{,}015§ mm §= 0{,}000\,015§ m §= 1{,}5 \times 10^{-5}§ m"],
          r"§1{,}5 \times 10^{-5}§ m"),
    ], r"Agrandissement de rapport §k§ : longueurs §\times k§, aires §\times k^2§."),
    X("Simuler la croissance",
      r"Pour savoir quand la culture de l'exercice 2 dépasse un million de bactéries, on écrit le script suivant. [IMG:s06_script]", [
        Q("Le rôle des variables", r"Que représentent les variables n et t ?",
          [r"R: n est le nombre de bactéries et t le temps écoulé en minutes"],
          "nombre de bactéries ; temps (min)"),
        Q("Les trois premiers tours", r"Donner les valeurs de n et de t après chacun des trois premiers tours de boucle.",
          [r"R: §(10\,000\ ;\ 20)§, §(20\,000\ ;\ 40)§, §(40\,000\ ;\ 60)§"],
          "(10 000 ; 20), (20 000 ; 40), (40 000 ; 60)"),
        Q("La valeur dite", r"Quelle valeur le lutin dit-il ? Interpréter.",
          [r"E: §5\,000 \times 2^7 = 640\,000 \leq 10^6§ et §5\,000 \times 2^8 = 1\,280\,000 > 10^6§ : la boucle fait 8 tours",
           r"R: Le lutin dit 160 : la culture dépasse un million de bactéries au bout de 160 min, soit 2 h 40 min"],
          "160 (2 h 40 min)"),
        Q("Dix millions",
          r"On remplace 1000000 par 10000000. Quelle valeur le lutin dira-t-il ?",
          [r"E: §5\,000 \times 2^{10} = 5\,120\,000 \leq 10^7§ et §5\,000 \times 2^{11} = 10\,240\,000 > 10^7§",
           r"R: 11 tours : le lutin dit §11 \times 20 = 220§"], "220"),
    ], r"« répéter jusqu'à » s'arrête dès que la condition devient VRAIE : on cherche le premier dépassement."),
], check06)


# ============================================================== SUJET 07

def check07():
    assert (-5) ** 2 - 3 ** 2 == 16 and F(5, 6) * F(3, 10) == F(1, 4)
    assert math.isclose(2.4e5 * 5e-2, 1.2e4) and (2 + 0 + 2 + 5) % 9 == 0
    assert 60 * R("1.05") == 63 and (-3) ** 2 - 1 == 8 and 2 * 60 + 20 == 140 and 10 - 3 == 7
    assert 27 - 25 == 2 and 27 + 25 == 52 and round(50 * math.pi) == 157
    assert round(50 * math.pi / 10, 1) == 15.7 and round(50 * math.pi / 10 * 60 / 1000, 2) == 0.94
    assert math.isclose(25 * math.cos(math.radians(60)), 12.5) and 27 - 12.5 == 14.5
    h = lambda t: -0.5 * t * t + 6 * t + 2  # noqa: E731
    assert h(0) == 2 and h(6) == 20 and max(h(t / 10) for t in range(121)) == 20
    assert h(4) == 18 and h(8) == 18 and h(10) == 12 and 8 - 4 == 4
    n = 3 + 6 + 8 + 5 + 3
    s = 5 * 3 + 10 * 6 + 15 * 8 + 20 * 5 + 30 * 3
    assert n == 25 and s == 385 and s / n == 15.4 and F(8, 25) == R("0.32") and 30 - 5 == 25
    serie = [5] * 3 + [10] * 6 + [15] * 8 + [20] * 5 + [30] * 3
    assert sorted(serie)[12] == 15 and sum(v > 15 for v in serie) == 8
    p = 2 * 32 + 3 * 24
    assert p == 136 and p * R("0.85") == R("115.6") and 136 * 2 < 390 < 136 * 3
    assert 4 * 136 - 390 == 154 and round(72 / 136 * 100, 1) == 52.9


S07 = S("07", "Le parc d'attractions", [
    A(r"Calculer §(-5)^2 - 3^2§.", r"§25 - 9 = 16§", "16"),
    A(r"Calculer §\frac{5}{6} \times \frac{3}{10}§.", r"§\frac{15}{60} = \frac{1}{4}§",
      r"§\frac{1}{4}§"),
    A(r"Calculer §2{,}4 \times 10^5 \times 5 \times 10^{-2}§ et donner l'écriture scientifique.",
      r"§12 \times 10^3 = 1{,}2 \times 10^4§", r"§1{,}2 \times 10^4§"),
    A(r"Le nombre 2 025 est-il divisible par 9 ?",
      r"Oui : la somme de ses chiffres §2 + 0 + 2 + 5 = 9§ est divisible par 9", "oui"),
    A(r"Développer §(2x + 1)^2§.", r"§4x^2 + 4x + 1§", r"§4x^2 + 4x + 1§"),
    A(r"Résoudre l'équation §(x + 2)(x - 5) = 0§.", r"§x = -2§ ou §x = 5§",
      r"§-2§ et §5§"),
    A(r"Un billet à 60 € augmente de 5 %. Quel est son nouveau prix ?", r"§60 \times 1{,}05 = 63§ €",
      "63 €"),
    A(r"On donne §g(x) = x^2 - 1§. Calculer §g(-3)§.", r"§9 - 1 = 8§", "8"),
    A(r"Convertir 2 h 20 min en minutes.", r"§120 + 20 = 140§ min", "140 min"),
    A(r"Donner l'étendue de la série : 3 ; 7 ; 7 ; 8 ; 10.", r"§10 - 3 = 7§", "7"),
], [
    X("La grande roue",
      r"Une grande roue a un rayon de 25 m ; son centre §O§ est à 27 m du sol. Elle fait un tour complet en 10 minutes. §P§ est le point le plus bas de la roue. [IMG:s07_roue]", [
        Q("Les hauteurs extrêmes",
          r"À quelle hauteur se trouvent le point le plus bas §P§ et le point le plus haut de la roue ?",
          [r"R: §27 - 25 = 2§ m et §27 + 25 = 52§ m"], "2 m et 52 m"),
        Q("La distance en un tour",
          r"Quelle distance une nacelle parcourt-elle en un tour ? Arrondir au mètre.",
          [r"R: §2 \times \pi \times 25 = 50\pi \approx 157§ m"], "157 m"),
        Q("La vitesse", r"Calculer la vitesse d'une nacelle en m/min, puis en km/h (au centième).",
          [r"E: §\frac{50\pi}{10} \approx 15{,}7§ m/min",
           r"R: §15{,}7 \times 60 \approx 942§ m/h, soit environ 0,94 km/h"], "15,7 m/min ≈ 0,94 km/h"),
        Q("La longueur §OH§",
          r"Une nacelle §M§ est telle que §\widehat{POM} = 60^\circ§ ; §H§ est le pied de la perpendiculaire à §(OP)§ passant par §M§. Calculer §OH§.",
          [r"E: Dans §OHM§ rectangle en §H§ : §\cos \widehat{HOM} = \frac{OH}{OM}§",
           r"R: §OH = 25 \times \cos 60^\circ = 12{,}5§ m"], "12,5 m"),
        Q("La hauteur de la nacelle", r"En déduire la hauteur de la nacelle §M§ au-dessus du sol.",
          [r"R: §27 - 12{,}5 = 14{,}5§ m"], "14,5 m"),
    ], r"Dans un triangle rectangle, §\cos = \frac{\text{adjacent}}{\text{hypoténuse}}§."),
    X("Le grand huit",
      r"La hauteur (en m) d'un wagon en fonction du temps §t§ (en s) est donnée par §h(t) = -0{,}5t^2 + 6t + 2§ pour §t§ entre 0 et 12. [IMG:s07_grand_huit]", [
        Q("Au départ", r"Quelle est la hauteur du wagon au départ ?",
          [r"R: §h(0) = 2§ m"], "2 m"),
        Q("Le sommet", r"Lire la hauteur maximale atteinte et l'instant correspondant.",
          [r"R: 20 m, au bout de 6 s"], "20 m à 6 s"),
        Q("Deux calculs", r"Calculer §h(4)§ et §h(10)§.",
          [r"E: §h(4) = -8 + 24 + 2 = 18§", r"R: §h(10) = -50 + 60 + 2 = 12§"], "18 et 12"),
        Q("Une hauteur de 18 m", r"À quels instants le wagon est-il à 18 m de hauteur ?",
          [r"R: Lecture graphique (et calcul : §h(8) = -32 + 48 + 2 = 18§) : à 4 s et à 8 s"],
          "4 s et 8 s"),
        Q("Au-dessus de 18 m", r"Pendant combien de temps le wagon est-il au-dessus de 18 m ?",
          [r"R: Entre 4 s et 8 s, soit 4 s"], "4 s"),
    ], r"Les antécédents d'un nombre se lisent sur l'axe des abscisses, aux points de la courbe d'ordonnée ce nombre."),
    X("L'attente aux manèges",
      r"On a relevé le temps d'attente de 25 visiteurs à l'entrée d'un manège. [IMG:s07_attente]", [
        Q("L'effectif", r"Vérifier que l'effectif total est 25.",
          [r"R: §3 + 6 + 8 + 5 + 3 = 25§"], "25"),
        Q("La moyenne", r"Calculer le temps d'attente moyen.",
          [r"E: §5 \times 3 + 10 \times 6 + 15 \times 8 + 20 \times 5 + 30 \times 3 = 385§",
           r"R: §\frac{385}{25} = 15{,}4§ min"], "15,4 min"),
        Q("La médiane", r"Déterminer le temps d'attente médian.",
          [r"E: La médiane est la 13e valeur ; effectifs cumulés : 3 ; 9 ; 17",
           r"R: La 13e valeur vaut 15 : médiane 15 min"], "15 min"),
        Q("Plus de 15 minutes",
          r"Quel pourcentage des visiteurs a attendu plus de 15 minutes ?",
          [r"R: §\frac{5 + 3}{25} = 0{,}32§, soit 32 %"], "32 %"),
        Q("L'étendue", r"Calculer l'étendue des temps d'attente.", [r"R: §30 - 5 = 25§ min"],
          "25 min"),
    ], r"Médiane d'une série de 25 valeurs : la 13e valeur de la série rangée."),
    X("Les tarifs du parc",
      r"L'entrée coûte 32 € pour un adulte et 24 € pour un enfant. Une famille comprend 2 adultes et 3 enfants.", [
        Q("Le prix d'une visite", r"Calculer le prix d'une visite pour la famille.",
          [r"R: §2 \times 32 + 3 \times 24 = 64 + 72 = 136§ €"], "136 €"),
        Q("La réduction de groupe",
          r"Le parc accorde 15 % de réduction aux groupes. Que paierait la famille avec cette réduction ?",
          [r"R: §136 \times 0{,}85 = 115{,}60§ €"], "115,60 €"),
        Q("Le pass annuel",
          r"Un pass famille annuel coûte 390 €. À partir de combien de visites dans l'année est-il plus avantageux ?",
          [r"E: 2 visites : 272 € ; 3 visites : 408 €", r"R: À partir de 3 visites"], "3 visites"),
        Q("Quatre visites", r"Quelle économie le pass permet-il pour 4 visites ?",
          [r"R: §4 \times 136 - 390 = 544 - 390 = 154§ €"], "154 €"),
        Q("La part des enfants",
          r"Quelle part du prix d'une visite correspond aux billets des enfants ? Arrondir au dixième de pourcentage.",
          [r"R: §\frac{72}{136} \approx 52{,}9§ %"], "52,9 %"),
    ], r"Réduction de 15 % : on multiplie par §1 - 0{,}15 = 0{,}85§."),
], check07)


# ============================================================== SUJET 08

def check08():
    import copy
    import scratch3e as Sc
    from scripts_brevet import SCRIPTS
    from scratch3e import V, cmp
    assert 12 / -4 + 7 == 4 and F(3, 4) / F(3, 8) == 2 and 7e-2 == 0.07
    assert 84 == 2 ** 2 * 3 * 7 and -10 / -2 == 5 and F(18, 24) == R("0.75") and -8 / 4 == -2
    assert 10 / (50 / 60) == 12 and F(1, 2) ** 2 == F(1, 4)
    assert R("1.2") ** 2 + R("0.9") ** 2 == R("1.5") ** 2 and R("1.2") + R("0.9") + R("1.5") == R("3.6")
    assert 3 * R("3.6") == R("10.8") and R("10.8") / 12 == R("0.9") and R("0.9") * 60 == 54
    assert 10 * 60 + 15 + 54 == 11 * 60 + 9 and round(math.degrees(math.atan(0.9 / 1.2))) == 37
    D = lambda x: R("1.5") * x + 8  # noqa: E731
    assert D(R("10.8")) == R("24.2") and (20 - 8) / R("1.5") == 8
    assert 245 * (8 + R("1.5") * 9) == R("5267.5") > 5000
    t = [42, 45, 47, 48, 50, 51, 53, 55, 58, 60, 66]
    assert sorted(t)[5] == 51 and sum(t) == 575 and round(575 / 11, 1) == 52.3
    assert 66 - 42 == 24 and sum(v < 575 / 11 for v in t) == 6 and round(10.8 / (42 / 60), 1) == 15.4
    run = lambda p, x: Sc.run(p, [x])["out"]  # noqa: E731
    p = SCRIPTS["s08"]
    assert run(p, "54") == [12, "Objectif manqué"] and run(p, "45") == [14.4, "Objectif atteint !"]
    q = copy.deepcopy(p)
    q[0][5] = ("ifelse", ("not", cmp("<", V("v"), 12)), q[0][5][2], q[0][5][3])
    assert run(q, "54")[1] == "Objectif atteint !" and run(q, "55")[1] == "Objectif manqué"


S08 = S("08", "La course solidaire", [
    A(r"Calculer §12 \div (-4) + 7§.", r"§-3 + 7 = 4§", "4"),
    A(r"Calculer §\frac{3}{4} \div \frac{3}{8}§.", r"§\frac{3}{4} \times \frac{8}{3} = 2§", "2"),
    A(r"Donner l'écriture scientifique de 0,07.", r"§7 \times 10^{-2}§", r"§7 \times 10^{-2}§"),
    A(r"Décomposer 84 en produit de facteurs premiers.", r"§84 = 2^2 \times 3 \times 7§",
      r"§2^2 \times 3 \times 7§"),
    A(r"Développer et réduire §3x - 2(x - 4)§.", r"§3x - 2x + 8 = x + 8§", r"§x + 8§"),
    A(r"Résoudre l'équation §-2x = 10§.", r"§x = \frac{10}{-2} = -5§", r"§x = -5§"),
    A(r"Exprimer 18 sur 24 en pourcentage.", r"§\frac{18}{24} = 0{,}75§, soit 75 %", "75 %"),
    A(r"On donne §f(x) = 4x§. Déterminer l'antécédent de §-8§.", r"§4x = -8§, donc §x = -2§",
      "-2"),
    A(r"Un coureur parcourt 10 km en 50 min. Quelle est sa vitesse moyenne en km/h ?",
      r"§50§ min §= \frac{5}{6}§ h et §10 \div \frac{5}{6} = 12§ km/h", "12 km/h"),
    A(r"On lance deux fois une pièce équilibrée. Probabilité d'obtenir deux fois « pile » ?",
      r"§\frac{1}{2} \times \frac{1}{2} = \frac{1}{4}§", r"§\frac{1}{4}§"),
], [
    X("Le parcours",
      r"Le parcours d'une course solidaire est la boucle §A \to B \to C \to A§, où §ABC§ est un triangle rectangle en §B§ avec §AB = 1{,}2§ km et §BC = 0{,}9§ km. [IMG:s08_parcours]", [
        Q("La longueur §CA§", r"Calculer la longueur §CA§.",
          [r"E: §CA^2 = 1{,}2^2 + 0{,}9^2 = 1{,}44 + 0{,}81 = 2{,}25§", r"R: §CA = 1{,}5§ km"],
          "1,5 km"),
        Q("Un tour", r"Calculer la longueur d'un tour.", [r"R: §1{,}2 + 0{,}9 + 1{,}5 = 3{,}6§ km"],
          "3,6 km"),
        Q("La durée de la course",
          r"Inès effectue 3 tours à la vitesse moyenne de 12 km/h. Combien de temps court-elle ?",
          [r"E: Distance : §3 \times 3{,}6 = 10{,}8§ km",
           r"R: §\frac{10{,}8}{12} = 0{,}9§ h §= 54§ min"], "54 min"),
        Q("L'heure d'arrivée", r"Elle part à 10 h 15. À quelle heure arrive-t-elle ?",
          [r"R: §10§ h §15 + 54§ min §= 11§ h §09§"], "11 h 09"),
        Q("L'angle au départ", r"Calculer l'angle §\widehat{BAC}§, arrondi au degré.",
          [r"R: §\tan \widehat{BAC} = \frac{BC}{AB} = \frac{0{,}9}{1{,}2} = 0{,}75§, donc §\widehat{BAC} \approx 37^\circ§"],
          "37°"),
    ], r"Durée = distance ÷ vitesse ; 0,9 h = 0,9 × 60 min = 54 min."),
    X("Les dons",
      r"Chaque participant paie une inscription de 8 € et un sponsor verse 1,50 € par kilomètre parcouru ; tout est reversé à une association.", [
        Q("Le don d'Inès", r"Inès a parcouru 10,8 km. Quelle somme sa participation rapporte-t-elle ?",
          [r"R: §8 + 1{,}50 \times 10{,}8 = 8 + 16{,}20 = 24{,}20§ €"], "24,20 €"),
        Q("La fonction", r"Exprimer la somme §D(x)§ rapportée par un participant qui parcourt §x§ km. Quel type de fonction est-ce ?",
          [r"R: §D(x) = 1{,}5x + 8§ : une fonction affine"], r"§D(x) = 1{,}5x + 8§"),
        Q("Rapporter 20 €", r"Combien de kilomètres faut-il parcourir pour rapporter 20 € ?",
          [r"E: §1{,}5x + 8 = 20§, §1{,}5x = 12§", r"R: §x = 8§ km"], "8 km"),
        Q("L'objectif collectif",
          r"Il y a 245 participants, qui parcourent en moyenne 9 km chacun. L'objectif de 5 000 € est-il atteint ?",
          [r"E: Par participant : §8 + 1{,}5 \times 9 = 21{,}50§ €",
           r"R: §245 \times 21{,}50 = 5\,267{,}50§ € : objectif atteint"], "oui (5 267,50 €)"),
        Q("Proportionnalité ?", r"La somme rapportée est-elle proportionnelle à la distance parcourue ?",
          [r"R: Non : à cause des 8 € fixes, §D(0) = 8 \neq 0§ ; la droite ne passe pas par l'origine"],
          "non"),
    ], r"Fonction affine §ax + b§ : proportionnelle seulement si §b = 0§."),
    X("Les temps de course",
      r"Voici les temps, en minutes, de 11 coureurs : 42 ; 45 ; 47 ; 48 ; 50 ; 51 ; 53 ; 55 ; 58 ; 60 ; 66.", [
        Q("La médiane", r"Déterminer le temps médian.",
          [r"R: 11 valeurs rangées : la médiane est la 6e, soit 51 min"], "51 min"),
        Q("La moyenne", r"Calculer le temps moyen, arrondi au dixième.",
          [r"R: §\frac{575}{11} \approx 52{,}3§ min"], "52,3 min"),
        Q("L'étendue", r"Calculer l'étendue.", [r"R: §66 - 42 = 24§ min"], "24 min"),
        Q("Une affirmation",
          r"« Plus de la moitié des coureurs ont un temps inférieur au temps moyen. » Vrai ou faux ?",
          [r"R: Vrai : 6 coureurs sur 11 ont un temps inférieur à 52,3 min"], "vrai (6 sur 11)"),
        Q("Le plus rapide",
          r"Le plus rapide a parcouru 10,8 km. Calculer sa vitesse moyenne, arrondie au dixième de km/h.",
          [r"R: §42§ min §= 0{,}7§ h et §\frac{10{,}8}{0{,}7} \approx 15{,}4§ km/h"], "15,4 km/h"),
    ], r"Moyenne et médiane sont deux indicateurs différents : ici la moyenne (52,3) dépasse la médiane (51)."),
    X("Un script de chronométrage",
      r"Le script suivant aide les coureurs du parcours de 10,8 km (3 tours). [IMG:s08_script]", [
        Q("Ce que calcule le script", r"Que représente la variable v ? Justifier la formule.",
          [r"R: La vitesse moyenne en km/h : §v = \frac{10{,}8}{t \div 60} = \frac{10{,}8 \times 60}{t}§, car §t§ minutes valent §\frac{t}{60}§ heures"],
          "la vitesse en km/h"),
        Q("Une durée de 54 min", r"Qu'affiche le script pour une durée de 54 minutes ?",
          [r"E: §v = \frac{648}{54} = 12§", r"R: Il dit 12, puis « Objectif manqué » car §12 > 12§ est faux"],
          "12 ; « Objectif manqué »"),
        Q("Une durée de 45 min", r"Qu'affiche-t-il pour une durée de 45 minutes ?",
          [r"R: §v = \frac{648}{45} = 14{,}4§ ; il dit 14,4 puis « Objectif atteint ! »"],
          "14,4 ; « Objectif atteint ! »"),
        Q("La durée maximale", r"Pour quelles durées l'objectif est-il atteint ?",
          [r"R: §\frac{648}{t} > 12§ équivaut à §t < 54§ : durée strictement inférieure à 54 min"],
          r"§t < 54§ min"),
        Q("Inclure 12 km/h",
          r"Comment modifier le test pour qu'une vitesse de 12 km/h atteigne l'objectif ?",
          [r"R: Remplacer « v > 12 » par « non (v < 12) » : le test devient vrai pour toute vitesse supérieure ou égale à 12"],
          "non (v < 12)"),
    ], r"Un test « > » exclut la valeur frontière : toujours tester la frontière."),
], check08)


# ============================================================== SUJET 09

def check09():
    assert 2 * 3 ** 2 == 18 and F(2, 3) + F(3, 4) == F(17, 12) and R("4.5e-3") == R("0.0045")
    assert math.isclose(math.sqrt(50), 5 * math.sqrt(2)) and 7 - (-3) == 10
    assert 120 * R("0.25") == 30 and 2500 * 3 / 1000 == 7.5 and F(4, 32) == F(1, 8)
    assert 4.5 * 6 == 27 and math.isclose(4.5 * math.sin(math.radians(30)), 2.25)
    assert round(4.5 * math.cos(math.radians(30)), 2) == 3.90
    assert 27 * 150 == 4050 and 4050 * R("0.25") == R("1012.5") and round(9000 / 1012.5, 1) == 8.9
    a = lambda x: R("0.22") * x + 12  # noqa: E731
    b = lambda x: R("0.19") * x + 18  # noqa: E731
    assert a(300) == 78 and b(300) == 75 and a(200) == b(200) == 56
    assert a(150) == 45 and b(150) == R("46.5")
    v = math.pi * 0.25 ** 2 * 1.2
    assert round(v * 1000) == 236 and 7 * 8 == 56 and 236 // 56 == 4
    assert round(236 * 0.046, 1) == 10.9 and round(236 * 0.046 * 0.25, 2) == 2.71
    c = [420, 380, 330, 260, 200, 150, 140, 130, 180, 270, 350, 410]
    s = sorted(c)
    assert sum(c) == 3220 and round(3220 / 12) == 268 and (s[5] + s[6]) / 2 == 265
    assert max(c) - min(c) == 290 and round((410 + 420 + 380) / 3220 * 100, 1) == 37.6


S09 = S("09", "L'énergie à la maison", [
    A(r"Calculer §2 \times 3^2§.", r"§2 \times 9 = 18§", "18"),
    A(r"Calculer §\frac{2}{3} + \frac{3}{4}§.", r"§\frac{8}{12} + \frac{9}{12} = \frac{17}{12}§",
      r"§\frac{17}{12}§"),
    A(r"Donner l'écriture décimale de §4{,}5 \times 10^{-3}§.", r"§0{,}004\,5§", "0,0045"),
    A(r"Écrire §\sqrt{50}§ sous la forme §a\sqrt{2}§.",
      r"§\sqrt{25 \times 2} = 5\sqrt{2}§", r"§5\sqrt{2}§"),
    A(r"Factoriser §4x^2 - 25§.", r"§(2x)^2 - 5^2 = (2x - 5)(2x + 5)§", r"§(2x - 5)(2x + 5)§"),
    A(r"Résoudre l'équation §7 - x = 10§.", r"§-x = 3§, donc §x = -3§", r"§x = -3§"),
    A(r"Quel est le coût de 120 kWh à 0,25 € le kWh ?", r"§120 \times 0{,}25 = 30§ €", "30 €"),
    A(r"§f§ est une fonction affine avec §f(0) = 3§ et §f(1) = 5§. Donner §f(x)§.",
      r"Ordonnée à l'origine 3, coefficient §5 - 3 = 2§ : §f(x) = 2x + 3§", r"§2x + 3§"),
    A(r"Un appareil de 2 500 W fonctionne pendant 3 h. Quelle énergie consomme-t-il, en kWh ?",
      r"§2{,}5§ kW §\times 3§ h §= 7{,}5§ kWh", "7,5 kWh"),
    A(r"On tire une carte au hasard dans un jeu de 32 cartes. Probabilité d'obtenir un roi ?",
      r"§\frac{4}{32} = \frac{1}{8}§", r"§\frac{1}{8}§"),
], [
    X("Des panneaux solaires",
      r"Des panneaux solaires couvrent un pan de toit rectangulaire de 6 m de large ; sa longueur §PR = 4{,}5§ m est inclinée de §30^\circ§ par rapport à l'horizontale. [IMG:s09_toit]", [
        Q("La surface des panneaux", r"Calculer la surface couverte par les panneaux.",
          [r"R: §4{,}5 \times 6 = 27§ m²"], "27 m²"),
        Q("La hauteur §RH§", r"Calculer la hauteur §RH§.",
          [r"R: §RH = 4{,}5 \times \sin 30^\circ = 4{,}5 \times 0{,}5 = 2{,}25§ m"], "2,25 m"),
        Q("La distance §PH§", r"Calculer §PH§, arrondie au centimètre.",
          [r"R: §PH = 4{,}5 \times \cos 30^\circ \approx 3{,}90§ m"], "3,90 m"),
        Q("La production",
          r"Chaque m² produit 150 kWh par an, que l'on n'achète plus 0,25 € le kWh. Calculer l'économie annuelle.",
          [r"E: Production : §27 \times 150 = 4\,050§ kWh",
           r"R: Économie : §4\,050 \times 0{,}25 = 1\,012{,}50§ € par an"], "1 012,50 €"),
        Q("La rentabilité",
          r"L'installation a coûté 9 000 €. Au bout de combien d'années est-elle rentabilisée ?",
          [r"E: §\frac{9\,000}{1\,012{,}50} \approx 8{,}9§",
           r"R: Au cours de la 9e année"], "9e année"),
    ], r"§\sin = \frac{\text{opposé}}{\text{hypoténuse}}§ et §\cos = \frac{\text{adjacent}}{\text{hypoténuse}}§."),
    X("Deux offres d'électricité",
      r"L'offre A coûte 12 € par mois plus 0,22 € par kWh ; l'offre B coûte 18 € par mois plus 0,19 € par kWh. [IMG:s09_offres]", [
        Q("Pour 300 kWh", r"Calculer la facture mensuelle de chaque offre pour 300 kWh.",
          [r"R: A : §12 + 0{,}22 \times 300 = 78§ € ; B : §18 + 0{,}19 \times 300 = 75§ €"],
          "A : 78 € ; B : 75 €"),
        Q("Les expressions", r"Exprimer la facture §A(x)§ et §B(x)§ pour §x§ kWh.",
          [r"R: §A(x) = 0{,}22x + 12§ et §B(x) = 0{,}19x + 18§"],
          r"§0{,}22x + 12§ ; §0{,}19x + 18§"),
        Q("Égalité des factures", r"Résoudre §A(x) = B(x)§ et interpréter.",
          [r"E: §0{,}22x + 12 = 0{,}19x + 18§, soit §0{,}03x = 6§",
           r"R: §x = 200§ kWh : les deux factures valent alors 56 €"], "200 kWh"),
        Q("Pour 150 kWh", r"Quelle offre choisir pour 150 kWh par mois ?",
          [r"R: A : 45 € ; B : 46,50 € : l'offre A"], "A"),
        Q("Conclusion", r"Conclure : quelle offre choisir selon la consommation ?",
          [r"R: L'offre A en dessous de 200 kWh, l'offre B au-dessus (égalité à 200 kWh)"],
          "A si < 200 kWh, B sinon"),
    ], r"Le point d'intersection de deux droites donne la valeur pour laquelle deux tarifs sont égaux."),
    X("Le ballon d'eau chaude",
      r"Un ballon d'eau chaude est un cylindre de rayon 0,25 m et de hauteur 1,2 m. [IMG:s09_ballon]", [
        Q("La contenance", r"Calculer sa contenance, arrondie au litre.",
          [r"R: §\pi \times 0{,}25^2 \times 1{,}2 = 0{,}075\pi \approx 0{,}236§ m³, soit 236 L"],
          "236 L"),
        Q("Une douche", r"Une douche dure 7 min avec un débit de 8 L/min. Quel volume utilise-t-elle ?",
          [r"R: §7 \times 8 = 56§ L"], "56 L"),
        Q("Le nombre de douches", r"Combien de douches complètes un ballon plein permet-il ?",
          [r"R: §236 \div 56 \approx 4{,}2§ : 4 douches"], "4"),
        Q("L'énergie de chauffe",
          r"Chauffer 1 L d'eau de 15 °C à 55 °C demande 0,046 kWh. Quelle énergie faut-il pour tout le ballon ? Quel est le coût à 0,25 € le kWh ?",
          [r"E: §236 \times 0{,}046 \approx 10{,}9§ kWh", r"R: §10{,}856 \times 0{,}25 \approx 2{,}71§ €"],
          "≈ 10,9 kWh ; ≈ 2,71 €"),
    ], r"Pour un nombre d'utilisations COMPLÈTES, on arrondit à l'entier inférieur."),
    X("La consommation mensuelle",
      r"Le diagramme donne la consommation d'électricité d'un foyer pour chaque mois de l'année. [IMG:s09_conso]", [
        Q("Sur l'année", r"Calculer la consommation annuelle.", [r"R: §3\,220§ kWh"], "3 220 kWh"),
        Q("La moyenne", r"Calculer la consommation mensuelle moyenne, arrondie au kWh.",
          [r"R: §\frac{3\,220}{12} \approx 268§ kWh"], "268 kWh"),
        Q("La médiane", r"Déterminer la consommation médiane.",
          [r"E: Série rangée : 130 ; 140 ; 150 ; 180 ; 200 ; 260 ; 270 ; 330 ; 350 ; 380 ; 410 ; 420",
           r"R: Moyenne des 6e et 7e valeurs : §\frac{260 + 270}{2} = 265§ kWh"], "265 kWh"),
        Q("L'étendue", r"Calculer l'étendue.", [r"R: §420 - 130 = 290§ kWh"], "290 kWh"),
        Q("L'hiver", r"Quelle part de la consommation annuelle représentent décembre, janvier et février ? Arrondir au dixième de pourcentage.",
          [r"R: §\frac{410 + 420 + 380}{3\,220} = \frac{1\,210}{3\,220} \approx 37{,}6§ %"],
          "37,6 %"),
    ], r"Avec un effectif pair (12), la médiane est la moyenne des deux valeurs centrales."),
], check09)


# ============================================================== SUJET 10

def check10():
    assert -8 + 5 * -2 == -18 and F(5, 12) - F(1, 4) == F(1, 6) and 6e4 / 3e-2 == 2e6
    assert math.gcd(24, 36) == 12 and -2 * 3 == -6 and 7 ** 2 == 49 == (-7) ** 2
    assert 4 * 25000 == 100000 and 5 - 8 == -3 and math.isclose(10 * 1.852, 18.52)
    ap = 45 / math.tan(math.radians(8))
    bp = 45 / math.tan(math.radians(15))
    assert round(ap) == 320 and round(bp) == 168 and round(ap - bp) == 152
    v = (ap - bp) / 2 * 60 / 1000
    assert round(v, 1) == 4.6 and round(v / 1.852, 1) == 2.5
    d = 2 * math.pi * 6371 * 30 / 360
    assert round(d) == 3336 and math.isclose(8 * 1.852, 14.816)
    hrs = d / 14.816
    assert round(hrs, 1) == 225.2 and int(hrs // 24) == 9 and round(hrs - 9 * 24) == 9
    assert 6 * 4 / 2 == 12 and round(math.sqrt(52), 2) == 7.21 and round(12 * 1.1 * 35, 2) == 462
    assert 600 / 20 == 30 and 400 / 20 == 20 and 30 * 20 / 2 == 300 and 120000 / 400 == 300
    h = lambda t: 3.5 + 2.5 * math.cos(math.pi * t / 6)  # noqa: E731
    assert math.isclose(h(0), 6) and math.isclose(h(6), 1) and 6 - 1 == 5
    assert math.isclose(h(4), 2.25) and math.isclose(h(8), 2.25)
    assert all(h(t / 100) < 2.25 for t in range(401, 800)) and math.isclose(h(3), 3.5)


S10 = S("10", "En mer", [
    A(r"Calculer §-8 + 5 \times (-2)§.", r"§-8 - 10 = -18§", "-18"),
    A(r"Calculer §\frac{5}{12} - \frac{1}{4}§.", r"§\frac{5}{12} - \frac{3}{12} = \frac{2}{12} = \frac{1}{6}§",
      r"§\frac{1}{6}§"),
    A(r"Calculer §\frac{6 \times 10^4}{3 \times 10^{-2}}§.", r"§2 \times 10^{4 - (-2)} = 2 \times 10^6§",
      r"§2 \times 10^6§"),
    A(r"Déterminer le plus grand diviseur commun de 24 et 36.", r"§24 = 2^3 \times 3§ et §36 = 2^2 \times 3^2§ : §2^2 \times 3 = 12§",
      "12"),
    A(r"Développer §-2(3x - 5)§.", r"§-6x + 10§", r"§-6x + 10§"),
    A(r"Résoudre l'équation §x^2 = 49§.", r"§x = 7§ ou §x = -7§", r"§7§ et §-7§"),
    A(r"Sur une carte à l'échelle §\frac{1}{25\,000}§, quelle distance réelle représentent 4 cm ?",
      r"§4 \times 25\,000 = 100\,000§ cm §= 1§ km", "1 km"),
    A(r"On donne §f(x) = 5 - x§. Calculer l'image de 8.", r"§5 - 8 = -3§", "-3"),
    A(r"Un nœud vaut 1,852 km/h. Convertir 10 nœuds en km/h.", r"§10 \times 1{,}852 = 18{,}52§ km/h",
      "18,52 km/h"),
    A(r"Quelle transformation correspond à un demi-tour autour d'un point ?",
      r"La symétrie centrale (ou rotation de 180°)", "symétrie centrale"),
], [
    X("Le phare",
      r"Un phare §[PS]§ vertical mesure 45 m. Depuis un bateau au point §A§, on voit le sommet §S§ sous un angle de §8^\circ§ avec l'horizontale ; un peu plus tard, depuis le point §B§, sous un angle de §15^\circ§. Les points §A§, §B§, §P§ sont alignés. [IMG:s10_phare]", [
        Q("La distance §AP§", r"Calculer §AP§, arrondie au mètre.",
          [r"E: Dans §APS§ rectangle en §P§ : §\tan 8^\circ = \frac{PS}{AP}§",
           r"R: §AP = \frac{45}{\tan 8^\circ} \approx 320§ m"], "320 m"),
        Q("La distance §BP§", r"Calculer §BP§, arrondie au mètre.",
          [r"R: §BP = \frac{45}{\tan 15^\circ} \approx 168§ m"], "168 m"),
        Q("La distance §AB§", r"En déduire la distance §AB§ parcourue par le bateau.",
          [r"R: §AB = AP - BP \approx 152§ m (calcul avec les valeurs non arrondies)"], "152 m"),
        Q("La vitesse en km/h",
          r"Le bateau a parcouru §AB§ en 2 minutes. Calculer sa vitesse en km/h, arrondie au dixième.",
          [r"E: §\frac{152{,}25}{2} \approx 76{,}1§ m/min", r"R: §76{,}1 \times 60 \approx 4\,570§ m/h, soit environ 4,6 km/h"],
          "4,6 km/h"),
        Q("En nœuds", r"Convertir cette vitesse en nœuds, arrondie au dixième.",
          [r"R: §\frac{4{,}57}{1{,}852} \approx 2{,}5§ nœuds"], "2,5 nœuds"),
    ], r"Quand on connaît l'opposé et l'angle, la tangente donne l'adjacent : §\text{adj} = \frac{\text{opp}}{\tan}§."),
    X("Une traversée",
      r"Un voilier navigue sur l'équateur, de la longitude §10^\circ§ O à la longitude §20^\circ§ E. On assimile la Terre à une sphère de rayon 6 371 km.", [
        Q("La latitude", r"Quelle est la latitude du voilier pendant tout le trajet ?",
          [r"R: §0^\circ§ : tous les points de l'équateur ont une latitude nulle"], "0°"),
        Q("L'écart de longitude", r"Quel est l'écart de longitude entre le départ et l'arrivée ?",
          [r"R: Les deux points sont de part et d'autre de Greenwich : §10 + 20 = 30^\circ§"], "30°"),
        Q("La distance parcourue", r"Calculer la distance parcourue, arrondie au km.",
          [r"E: Longueur de l'équateur : §2\pi \times 6\,371§ km",
           r"R: §\frac{30}{360} \times 2\pi \times 6\,371 \approx 3\,336§ km"], "3 336 km"),
        Q("La vitesse du voilier", r"Le voilier avance à 8 nœuds. Convertir cette vitesse en km/h.",
          [r"R: §8 \times 1{,}852 = 14{,}816§ km/h"], "14,816 km/h"),
        Q("La durée", r"Calculer la durée de la traversée, en heures, puis en jours et heures.",
          [r"E: §\frac{3\,336}{14{,}816} \approx 225§ h", r"R: §225 = 9 \times 24 + 9§ : environ 9 jours et 9 heures"],
          "≈ 9 jours et 9 h"),
    ], r"Sur un grand cercle, la longueur d'un arc est proportionnelle à l'angle."),
    X("La voile",
      r"La voile d'un bateau est le triangle §MTB§ rectangle en §M§ : le mât mesure §MT = 6§ m et la bôme §MB = 4§ m. [IMG:s10_voile]", [
        Q("L'aire de la voile", r"Calculer l'aire de la voile.", [r"R: §\frac{6 \times 4}{2} = 12§ m²"],
          "12 m²"),
        Q("La longueur §TB§", r"Calculer §TB§, arrondie au centimètre.",
          [r"R: §TB = \sqrt{6^2 + 4^2} = \sqrt{52} \approx 7{,}21§ m"], "7,21 m"),
        Q("Le prix du tissu",
          r"Le tissu coûte 35 € le m² et on prévoit 10 % de tissu en plus pour les coutures. Calculer le prix du tissu.",
          [r"R: §12 \times 1{,}1 \times 35 = 462§ €"], "462 €"),
        Q("La maquette", r"On construit une maquette au §\frac{1}{20}§. Donner les longueurs du mât et de la bôme de la maquette.",
          [r"R: §600 \div 20 = 30§ cm et §400 \div 20 = 20§ cm"], "30 cm et 20 cm"),
        Q("L'aire sur la maquette", r"Calculer l'aire de la voile de la maquette, de deux façons.",
          [r"E: Directement : §\frac{30 \times 20}{2} = 300§ cm²",
           r"R: Avec le rapport : §12§ m² §= 120\,000§ cm² et §120\,000 \div 20^2 = 300§ cm² ✔️"],
          "300 cm²"),
    ], r"Réduction au §\frac{1}{20}§ : aires divisées par §20^2 = 400§."),
    X("Les marées",
      r"Le graphique donne la hauteur d'eau dans un port en fonction de l'heure, entre 0 h et 12 h. [IMG:s10_marees]", [
        Q("À minuit", r"Quelle est la hauteur d'eau à 0 h ?", [r"R: 6 m (c'est la pleine mer)"], "6 m"),
        Q("La basse mer", r"À quelle heure a lieu la basse mer ? Quelle est alors la hauteur d'eau ?",
          [r"R: À 6 h, avec 1 m d'eau"], "6 h ; 1 m"),
        Q("Le marnage", r"Le marnage est la différence entre pleine mer et basse mer. Le calculer.",
          [r"R: §6 - 1 = 5§ m"], "5 m"),
        Q("Un bateau bloqué",
          r"Un bateau a besoin d'au moins 2,25 m d'eau pour manœuvrer. Pendant quelle période ne peut-il pas sortir du port ?",
          [r"R: La courbe est sous 2,25 m entre 4 h et 8 h : il ne peut pas sortir entre 4 h et 8 h"],
          "entre 4 h et 8 h"),
        Q("Entre 0 h et 3 h", r"De combien la mer a-t-elle baissé entre 0 h et 3 h ?",
          [r"R: §6 - 3{,}5 = 2{,}5§ m"], "2,5 m"),
    ], r"Lire « quand la hauteur est inférieure à… » revient à repérer où la courbe est SOUS une droite horizontale."),
], check10)


SUJETS = [S06, S07, S08, S09, S10]
