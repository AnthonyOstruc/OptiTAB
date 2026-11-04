# -*- coding: utf-8 -*-
"""Vérification mathématique de la notion 271 (5e : proportionnalité et pourcentages).

    python verif_271.py

1. Contrôles explicites (sympy, valeurs exactes) de chaque réponse des exercices,
   du cours, de la fiche et des valeurs écrites sur les figures.
2. Contrôle automatique : toute égalité purement numérique écrite entre $…$ dans
   les fichiers (chaînes « a = b = c », « ≠ », pourcentages, fractions, unités de
   longueur, de masse et de volume converties) est recalculée exactement.
3. Structure : 10 exercices, progression, corrigés complets, Id gardés / retirés,
   aucune mention du brevet, aucun ratio ni produit en croix (hors programme de 5e).
"""
import re
import sys
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
ok, ko = 0, []
R = sp.Rational


def check(cond, msg):
    global ok
    if cond:
        ok += 1
    else:
        ko.append(msg)


def pc(p, q):
    """p % de q, exact."""
    return R(p, 100) * q


def d(s):
    """Décimal exact à partir d'une chaîne « 4,50 »."""
    return sp.nsimplify(s.replace(",", "."), rational=True)


def proportionnel(l1, l2):
    q = [R(b) / R(a) for a, b in zip(l1, l2)]
    return all(x == q[0] for x in q), q


# ===================================================================== cours
p, q = proportionnel([1, 2, d("3,5"), 5], [6, 12, 21, 30])
check(p and q[0] == 6, "cours : tissu 6 €/m")
check(2 * 6 == 12 and d("3,5") * 6 == 21, "cours : tissu 2 m et 3,5 m")
taxi = lambda k: 4 + 2 * k
check(taxi(1) == 6 and taxi(2) == 8 and taxi(2) != 2 * taxi(1), "cours : taxi non proportionnel")
check([taxi(k) for k in (1, 2, 3, 5)] == [6, 8, 10, 14], "figure cours : points du taxi")
check(R(86) * 2 == 172, "cours : taille 2 ans / 4 ans")
u = d("4,50") / 5
check(u == d("0,90") and 8 * u == d("7,20") and 12 * u == d("10,80") and d("2,70") / u == 3, "cours : baguettes unité")
check(3 * d("4,50") == d("13,50") and d("13,50") + d("4,50") == 18 and 20 * u == 18 and 15 * u == d("13,50"),
      "cours : baguettes linéarité")
check(d("4,50") + 3 != 8 * u and d("4,50") + 3 == d("7,50"), "cours : erreur +3")
check(R(18) / 2 == 9 and 2 * 18 + 9 == 45 and R(45) / R(5, 2) == 18, "cours : cycliste 18 km/h")
check(R(9, 25) == R(36, 100), "cours : 9 sur 25 = 36 %")
check(R(12, 20) == R(60, 100) and R(14, 25) == R(56, 100) and R(60) > 56 and 14 > 12, "cours : clubs A et B")
check(pc(10, 60) == 6 and pc(30, 60) == 18 and 3 * 6 == 18, "cours : 30 % de 60 €")
check(pc(15, 80) == 12 and 80 - 12 == 68, "cours : sac soldé")
check(pc(2, 500) == 10 and 500 + 10 == 510, "cours : loyer")
check(pc(10, 80) == 8 and pc(10, 68) == d("6,80"), "cours : 10 % de 80 et de 68")
check(4 * 1000 == 4000 and 4000 / 100 == 40 and 2 * 1000 / 100 == 20, "cours : terrain 40 m × 20 m")
check(R(300, 1000) == d("0,3"), "cours : but 3 m")
check(R(100 * 100, 5) == 2000, "cours : trouver l'échelle 1/2000")
check(R(4, 4000) == R(1, 1000), "cours : 4 cm pour 40 m")
check(R(1000 * 2, 100) == 20, "figure cours : 2 cm de l'échelle graphique = 20 m")

# ===================================================================== fiche (mêmes exemples)
check(R(12, 2) == 6 and d("21") / d("3,5") == 6, "fiche : quotients du tissu")

# ===================================================================== 2920
A = ([1, 2, 4, 5], [d("2,50"), 5, 10, d("12,50")])
B = ([1, 2, 3, 5], [5, 8, 11, 17])
C = ([2, 4, 8], [86, 102, 128])
pA, qA = proportionnel(*A)
pB, qB = proportionnel(*B)
pC, qC = proportionnel(*C)
check(pA and qA[0] == d("2,5"), "2920 : tableau A proportionnel, coef 2,5")
check(not pB and qB[0] == 5 and qB[1] == 4, "2920 : tableau B non proportionnel")
check(not pC and qC[0] == 43 and qC[1] == d("25,5"), "2920 : tableau C non proportionnel")
check(3 * d("2,5") == d("7,5") and 7 * d("2,5") == d("17,5") and 20 / d("2,5") == 8, "2920 : Q2")
liv = lambda m: 2 + 3 * m
check([liv(m) for m in B[0]] == B[1], "2920 : tarif 2 € + 3 €/kg reproduit le tableau B")
check(liv(10) == 32 and 2 * liv(5) == 34 and liv(10) != 2 * liv(5), "2920 : 10 kg")
check(liv(0) == 2, "2920 : la droite B coupe l'axe à 2")

# ===================================================================== 2921
far = R(250, 4)
check(far == d("62,5") and 6 * far == 375 and 10 * far == 625 and R(1000) / far == 16, "2921 : farine")
check((2 * 250, 2 * 3, 2 * 50, 2 * 40) == (500, 6, 100, 80), "2921 : pour 8 personnes")
check(500 + 250 == 750 == 3 * 250 and 100 + 50 == 150 == 3 * 50, "2921 : pour 12 personnes")
check(R(6, 4) == d("1,5") and d("1,5") * 250 == 375, "2921 : coefficient 1,5 de 4 à 6 personnes")

# ===================================================================== 2917
check(R(14, 40) == R(7, 20) == R(35, 100), "2917 : 14/40 = 35 %")
check(40 - 14 == 26 and R(26, 40) == R(13, 20) == R(65, 100), "2917 : 26 = 65 %")
check(pc(30, 40) == 12 and pc(25, 40) == 10 and R(40, 10) * 3 == 12, "2917 : 30 % et 25 % de 40")

# ===================================================================== 2915
coef = R(18, 10)
vol = [10, 20, 5, 25, 1, 42]
prix = [coef * v for v in vol]
check(prix == [18, 36, 9, 45, d("1,8"), d("75,6")], "2915 : tableau du gazole")
check(36 + 9 == 45 and R(54) / coef == 30, "2915 : 25 L et 54 €")
check(coef * 15 == 27 == 18 + 9 and 18 + 5 == 23, "2915 : erreur de Tom")
check([coef * v for v in (5, 10, 20, 25)] == [9, 18, 36, 45], "figure 2915")

# ===================================================================== 2927
check([pc(p_, 80) for p_ in (10, 5, 50, 25, 75)] == [8, 4, 40, 20, 60], "2927 : calcul mental")
check(pc(30, 80) == 24 and 80 - 24 == 56, "2927 : blouson")
check(pc(12, 50) == 6 and 50 + 6 == 56, "2927 : abonnement")
check(pc(12, 56) == d("6,72") and 56 - d("6,72") == d("49,28") and d("49,28") != 50, "2927 : Lina")

# ===================================================================== 2924 (1/50)
check((8 * 50, 6 * 50) == (400, 300), "2924 : chambre 4 m × 3 m")
check((4 * 50, d("1,8") * 50) == (200, 90), "2924 : lit 2 m × 90 cm")
check(R(120, 50) == d("2,4"), "2924 : bureau 2,4 cm")
check(R(400, 5) == 80 and R(5, 400) == R(1, 80), "2924 : échelle 1/80")

# ===================================================================== 2934
check(d("4,50") / 3 == d("1,5") and R(7, 5) == d("1,4") and d("1,4") < d("1,5"), "2934 : prix unitaires")
check(30 % 3 == 0 and 30 % 5 == 0 and 10 * d("4,50") == 45 and 6 * 7 == 42, "2934 : 30 cahiers")
check(pc(10, 45) == d("4,5") and 45 - d("4,5") == d("40,5") and 42 - d("40,5") == d("1,5"), "2934 : remise")
lotsA = max(k for k in range(20) if k * d("4,50") <= 20)
lotsB = max(k for k in range(20) if k * 7 <= 20)
check((lotsA, lotsB, 3 * lotsA, 5 * lotsB) == (4, 2, 12, 10), "2934 : avec 20 €")
check(4 * d("4,50") == 18 and 5 * d("4,50") == d("22,5") and 3 * 7 == 21, "2934 : bornes des lots")

# ===================================================================== 2918 (1/25 000)
cm_reel = 25000
check(R(cm_reel, 100) == 250, "2918 : 1 cm = 250 m")
longueurs = [4, d("6,4"), d("5,6")]
reels_km = [R(l_) * cm_reel / 100000 for l_ in longueurs]
check(reels_km == [1, d("1,6"), d("1,4")] and sum(reels_km) == 4 and sum(longueurs) == 16, "2918 : boucle 4 km")
check(4 + d("5,6") > d("6,4") and 4 + d("6,4") > d("5,6") and d("6,4") + d("5,6") > 4, "2918 : triangle possible")
duree = R(60, 3) * 4
check(duree == 80, "2918 : 80 min")
retour = 9 * 60 + 45 + duree + 30
check(divmod(retour, 60) == (11, 35), "2918 : retour à 11 h 35")
check(R(2000, 250) == 8 and R(200000, cm_reel) == 8, "2918 : 2 km = 8 cm")

# ===================================================================== 2935
part = R(600, 8)
check(part == 75 and 20 * part == 1500, "2935 : 1 500 g")
check(R(1500, 500) == 3 and d("0,5") * d("4,80") == d("2,40") and 3 * d("2,40") == d("7,20") == d("1,5") * d("4,80"),
      "2935 : sachets")
check(pc(25, d("7,20")) == d("1,80") and (d("7,20") - d("1,80")) / 20 == d("0,27"), "2935 : part de chaque élève")
check(pc(80, 20) == 16 and 16 * part == 1200 and 2 * 500 < 1200 and 1500 - 1200 == 300, "2935 : 80 %")
check(sp.ceiling(R(1200, 500)) == 3, "2935 : arrondi au sachet supérieur")

# ===================================================================== 2931
check(R(18, 24) == R(3, 4) == R(75, 100) and R(21, 30) == R(7, 10) == R(70, 100), "2931 : proportions")
check(R(18, 24) > R(21, 30) and 21 > 18, "2931 : comparaison")
check(pc(72, 150) == 108 and 150 - 108 == 42 and pc(28, 150) == 42, "2931 : niveau de 5e")
check(42 * d("1,50") == 63 and pc(20, 63) == d("12,6") and 63 - d("12,6") == d("50,4"), "2931 : petit déjeuner")

# ===================================================================== contrôle automatique des égalités numériques
UNITES = {"mm": ("L", R(1, 10)), "cm": ("L", 1), "m": ("L", 100), "km": ("L", 100000),
          "g": ("M", 1), "kg": ("M", 1000), "cl": ("V", 1), "L": ("V", 100), "min": ("T", 1), "h": ("T", 60)}


def frac(s):
    while True:
        n = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
        if n == s:
            return s
        s = n


def tex_vers_py(s):
    """Convertit un membre LaTeX en (expression Python, unité) ; unité = None si absente."""
    unite = None
    m = re.search(r"\\text\{\s*([a-zA-Z]+)\s*\}\s*$", s.strip())
    if m and m.group(1) in UNITES:
        unite = UNITES[m.group(1)]
        s = s.strip()[:m.start()]
    s = s.replace("{,}", ".").replace(r"\times", "*").replace(r"\div", "/")
    s = s.replace(r"\,\%", "/100").replace(r"\%", "/100")
    s = s.replace(r"\left", "").replace(r"\right", "").replace(r"\,", "").replace(r"\quad", " ")
    s = frac(s)
    s = re.sub(r"\\text\{[^}]*\}", " ", s)
    s = s.replace("€", "")
    return s.strip(), unite


NUM = re.compile(r"^[\d.\s+\-*/()]+$")


def valeur(expr):
    try:
        v = sp.sympify(expr, rational=True)
        return v if v.is_Rational else None
    except Exception:
        return None


def egalites(texte, ou):
    global ok
    vus = 0
    blocs = re.findall(r"\$\$(.+?)\$\$", texte, re.S) + re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", texte)
    for m in blocs:
        for ligne in re.split(r"\\\\|\\qquad", m):
            ligne = ligne.replace("&", "")
            ligne = re.sub(r"\\begin\{aligned\}|\\end\{aligned\}", "", ligne)
            for rel in (r"\neq", r"\ne"):
                if rel in ligne:
                    g, dd = ligne.split(rel, 1)
                    (g, _), (dd, _) = tex_vers_py(g.split("=")[-1]), tex_vers_py(dd.split("=")[0])
                    if g and dd and NUM.match(g) and NUM.match(dd):
                        a, b = valeur(g), valeur(dd)
                        if a is not None and b is not None:
                            vus += 1
                            if a == b:
                                ko.append(f"{ou} : « {ligne.strip()} » (≠ faux)")
                            else:
                                ok += 1
                    ligne = ""
                    break
            membres = [tex_vers_py(x) for x in ligne.split("=")]
            membres = [x for x in membres if x[0]]
            if len(membres) < 2 or not all(NUM.match(x[0]) for x in membres):
                continue
            vals = []
            u0 = next((un for _, un in membres if un), None)
            for expr, un in membres:
                v = valeur(expr)
                if v is None:
                    break
                un = un or u0          # un nombre nu est exprimé dans l'unité du premier membre qui en a une
                vals.append((v * (un[1] if un else 1), un[0] if un else None))
            else:
                if len({dm for _, dm in vals}) > 1:
                    ko.append(f"{ou} : « {ligne.strip()} » unités incompatibles")
                    continue
                vus += 1
                if all(v == vals[0][0] for v, _ in vals):
                    ok += 1
                else:
                    ko.append(f"{ou} : « {ligne.strip()} » → {[str(v) for v, _ in vals]}")
    return vus


total_auto = 0
for nom in ("cours_266.txt", "fiche_186.txt", "exercices.txt"):
    t = (ICI / nom).read_text(encoding="utf-8")
    total_auto += egalites(t, nom)
check(total_auto >= 120, f"contrôle automatique : seulement {total_auto} égalités lues")

# ===================================================================== structure
ex = (ICI / "exercices.txt").read_text(encoding="utf-8")
blocs = [b.strip() for b in re.split(r"^===[ \t]*$", ex, flags=re.M) if b.strip()]
check(len(blocs) == 10, f"{len(blocs)} exercices (10 attendus)")
types = [re.match(r"=== (\w+)", b).group(1) for b in blocs]
check(types == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 2 + ["Synthèse"] * 2, f"progression {types}")
titres = [b.splitlines()[0] for b in blocs]
check(len(set(titres)) == 10, "titres uniques")
retires = {int(m) for m in re.findall(r"^(\d+)", (ICI / "exercices_retires.txt").read_text(encoding="utf-8"), re.M)}
ids = [int(re.search(r"^Id: (\d+)", b, re.M).group(1)) for b in blocs]
check(len(retires) == 11 and not (retires & set(ids)) and set(ids) | retires == set(range(2915, 2936)),
      "Id gardés / retirés (2915 à 2935)")
for b in blocs:
    eid = re.search(r"^Id: (\S+)", b, re.M).group(1)
    en = b.split("Énoncé:", 1)[1].split("Étapes:", 1)[0]
    et = b.split("Étapes:", 1)[1].split("Solution:", 1)[0]
    nq = len(re.findall(r"^\d+\. ", en, re.M))
    check(len(re.findall(r"^## Question", et, re.M)) == nq, f"{eid} : {nq} questions / corrigés")
    check(et.count("::: methode") >= nq and et.count("::: resultat") >= nq, f"{eid} : méthode et résultat par question")
    check("::: attention" in et, f"{eid} : erreur fréquente")
    sol = b.split("Solution:", 1)[1]
    check(len(re.findall(r"^\d+\. ", sol, re.M)) == nq, f"{eid} : solution courte complète")
    imgs = set(re.findall(r"\[IMAGE_(\d+)\]", b))
    check(len(imgs) == len(re.findall(r"\[IMAGE_\d+\]", b)), f"{eid} : images appelées une seule fois")
for nom in ("cours_266.txt", "fiche_186.txt", "exercices.txt"):
    t = (ICI / nom).read_text(encoding="utf-8").lower()
    check("brevet" not in t, f"{nom} : mention du brevet")
    check("ratio" not in t and "produit en croix" not in t and "produits en croix" not in t,
          f"{nom} : ratio / produit en croix (hors programme de 5e 2026)")

print(f"{ok} contrôles justes, {len(ko)} erreur(s) ; {total_auto} égalités numériques recalculées automatiquement")
for e in ko:
    print("  ✗", e)
sys.exit(1 if ko else 0)
