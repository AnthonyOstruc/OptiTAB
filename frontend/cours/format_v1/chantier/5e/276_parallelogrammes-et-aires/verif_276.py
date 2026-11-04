# -*- coding: utf-8 -*-
"""Vérification mathématique de la notion 276 (5e : parallélogrammes et aires).

    python verif_276.py

1. Contrôles explicites (sympy, valeurs exactes) de chaque réponse du cours, des
   exercices, et des coordonnées des figures (figures/figures.py, DONNEES) :
   longueurs, angles, milieux, perpendicularités, aires (formule de Gauss), positions.
2. Contrôle automatique : toute égalité ou valeur approchée purement numérique écrite
   entre $…$ dans les trois fichiers est recalculée (π compris ; « ≈ » contrôlé à la
   précision affichée ; « ≠ » contrôlé).
3. Structure : 10 exercices, progression, corrigés complets, Id gardés / retirés,
   aucune mention du brevet, rien de 4e (Pythagore, racine carrée, produit en croix).
"""
import importlib.util
import re
import sys
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
ok, ko = 0, []
R = sp.Rational
pi = sp.pi


def check(cond, msg):
    global ok
    if bool(cond):
        ok += 1
    else:
        ko.append(msg)


def P(p):
    """Point flottant de figures.py → point sympy (rationnel approché à 1e-9)."""
    return sp.Matrix([sp.nsimplify(p[0], rational=True, tolerance=1e-9),
                      sp.nsimplify(p[1], rational=True, tolerance=1e-9)])


def fl(p):
    return (float(p[0]), float(p[1]))


def d2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def proche(a, b, eps=1e-6):
    return abs(float(a) - float(b)) < eps


def aire(pts):
    """Aire (formule de Gauss) d'un polygone."""
    s = 0
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def milieu(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def scal(u, v):
    return u[0] * v[0] + u[1] * v[1]


def vec(p, q):
    return (q[0] - p[0], q[1] - p[1])


def para(u, v):
    return abs(u[0] * v[1] - u[1] * v[0]) < 1e-9


def dist_droite(p, a, b):
    u = vec(a, b)
    return abs(u[0] * (p[1] - a[1]) - u[1] * (p[0] - a[0])) / (u[0] ** 2 + u[1] ** 2) ** 0.5


# ===================================================================== figures (coordonnées)
spec = importlib.util.spec_from_file_location("fig276", ICI / "figures" / "figures.py")
fig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fig)
DN = fig.DONNEES


def est_para(A, B, C, D):
    return para(vec(A, B), vec(D, C)) and para(vec(A, D), vec(B, C)) and proche(d2(A, B), d2(D, C))


# cours : RSTU (RS = 10, ST = 6, R = 60°), diagonale RT = 14
g = DN["cours_parallelogramme"]
check(est_para(g["R"], g["S"], g["T"], g["U"]), "figure cours : RSTU parallélogramme")
check(proche(d2(g["R"], g["S"]), 100) and proche(d2(g["S"], g["T"]), 36) and proche(d2(g["R"], g["T"]), 196),
      "figure cours : RS = 10, ST = 6, RT = 14")
U = sp.Matrix([3, 3 * sp.sqrt(3)])
T = sp.Matrix([10, 0]) + U
check(T.dot(T) == 196 and U.dot(U) == 36, "cours exemple : RT = 14 exact (RS = 10, ST = 6, R = 60°)")
check(R(14, 2) == 7 and 180 - 60 == 120, "cours exemple : OR = 7, angle S = 120°")
check(d2(g["R"], g["T"]) > d2(g["S"], g["U"]), "cours : [RT] plus longue que [SU]")
g = DN["cours_construction"]
check(est_para(g["A"], g["B"], g["C"], g["D"]), "figure cours : construction au compas")
g = DN["cours_particuliers"]
r1, l2, c3 = g["rectangle"], g["losange"], g["carre"]
check(est_para(*r1) and proche(d2(r1[0], r1[2]), d2(r1[1], r1[3])) and abs(scal(vec(r1[0], r1[1]), vec(r1[0], r1[3]))) < 1e-9,
      "figure cours : rectangle")
check(est_para(*l2) and abs(scal(vec(l2[0], l2[2]), vec(l2[1], l2[3]))) < 1e-9 and proche(d2(l2[0], l2[1]), d2(l2[1], l2[2])),
      "figure cours : losange")
check(est_para(*c3) and proche(d2(c3[0], c3[2]), d2(c3[1], c3[3])) and abs(scal(vec(c3[0], c3[2]), vec(c3[1], c3[3]))) < 1e-9,
      "figure cours : carré")
g = DN["cours_aire_para"]
check(est_para(g["A"], g["B"], g["C"], g["D"]) and proche(aire([g["A"], g["B"], g["C"], g["D"]]), aire([g["H"], g["H2"], g["C"], g["D"]])),
      "figure cours : parallélogramme et rectangle de même aire")
g = DN["cours_aire_triangle"]
check(proche(aire([g["A"], g["B"], g["C"]]) * 2, aire([g["A"], g["B"], g["D"], g["C"]])), "figure cours : triangle moitié")
check(g["H"][0] > g["F"][0] and proche(g["H"][0], g["G"][0]), "figure cours : pied sur le prolongement")
g = DN["cours_disque"]
check(abs(g["base"] / (float(pi) * g["r"]) - 1) < 0.01, "figure cours : base des parts ≈ π × r")
check(abs(sp.N(6 * pi) - 18.8) < 0.05 and abs(sp.N(9 * pi) - 28.3) < 0.05, "cours : disque de rayon 3 cm")
check(abs(sp.N(16 - pi) - 12.86) < 0.005, "cours : logo")
check(9 * 4 == 36 and R(7 * 5, 2) == R(35, 2) == sp.Rational("17.5"), "cours : aires exemples")
check(sp.Rational("3.5") * 100 == 350 and 350 * 100 == 35000 and R(2400, 10000) == sp.Rational("0.24")
      and sp.Rational("2.5") * 10000 == 25000, "cours : conversions")

# 3020
g = DN["ex3020"]
A, B, C, D, O = g["A"], g["B"], g["C"], g["D"], g["O"]
check(est_para(A, B, C, D), "3020 : parallélogramme")
check(proche(d2(A, B), 64) and proche(d2(A, D), 25) and proche(d2(O, D), 3.5 ** 2) and proche(d2(B, D), 49),
      "3020 : AB = 8, AD = 5, OD = 3,5, BD = 7")
Ae, Be, De = sp.Matrix([0, 0]), sp.Matrix([8, 0]), 5 * sp.Matrix([R(1, 2), sp.sqrt(3) / 2])
check((Be - De).dot(Be - De) == 49, "3020 : BD = 7 exactement (loi exacte avec 60°)")
check(2 * (8 + 5) == 26 and (360 - 2 * 60) / 2 == 120 and 60 + 120 == 180, "3020 : périmètre et angles")

# 3026
g = DN["ex3026"]
A, B, C, D, O = g["A"], g["B"], g["C"], g["D"], g["O"]
check(est_para(A, B, C, D) and proche(d2(A, D), 3.5 ** 2) and proche(d2(C, D), 25), "3026 : AD = 3,5, CD = 5")
check(proche(d2(O, B), d2(O, D)) and proche(milieu(B, D)[0], O[0]) and proche(milieu(B, D)[1], O[1]), "3026 : O milieu de [BD]")
ang = sp.acos(sp.Rational(1) * scal(vec(B, A), vec(B, C)) / (5 * 3.5))
check(abs(float(ang) * 180 / float(pi) - 70) < 1e-6, "3026 : angle ABC = 70°")
# D et B de part et d'autre de (AC)
s1 = vec(A, C)[0] * (B[1] - A[1]) - vec(A, C)[1] * (B[0] - A[0])
s2 = vec(A, C)[0] * (D[1] - A[1]) - vec(A, C)[1] * (D[0] - A[0])
check(s1 * s2 < 0, "3026 : D de l'autre côté de (AC)")

# 3024
g = DN["ex3024"]
for nom, S in g.items():
    m1, m2 = milieu(S[0], S[2]), milieu(S[1], S[3])
    check(proche(m1[0], m2[0]) and proche(m1[1], m2[1]), f"3024 : {nom} diagonales de même milieu")
    eg = proche(d2(S[0], S[2]), d2(S[1], S[3]))
    pe = abs(scal(vec(S[0], S[2]), vec(S[1], S[3]))) < 1e-9
    attendu = {"ABCD": (False, False), "EFGH": (True, False), "IJKL": (False, True), "MNPQ": (True, True)}[nom]
    check((eg, pe) == attendu, f"3024 : nature de {nom}")

# 3031
g = DN["ex3031"]
Rr, Dd, Oo, Ll, Ee = g["R"], g["D"], g["O"], g["L"], g["E"]
check(milieu(Dd, Ll) == Rr and milieu(Oo, Ee) == Rr, "3031 : R milieu des diagonales")
check(scal(vec(Dd, Ll), vec(Oo, Ee)) == 0 and scal(vec(Rr, Dd), vec(Rr, Oo)) == 0, "3031 : perpendiculaires")
check(d2(Rr, Dd) == 9 and d2(Rr, Oo) == 4 and d2(Dd, Ll) == 36 and d2(Oo, Ee) == 16, "3031 : RD = 3, RO = 2, DL = 6, OE = 4")
check(proche(d2(Dd, Oo), d2(Oo, Ll)) and proche(d2(Oo, Ll), d2(Ll, Ee)), "3031 : DOLE losange")
g = DN["ex3031_trapeze"]
I, J, K, L = g["I"], g["J"], g["K"], g["L"]
check(proche(d2(I, J), 16) and proche(d2(K, L), 16), "3031 : IJ = KL = 4")
check(not para(vec(I, J), vec(L, K)) and not proche(d2(J, K), d2(L, I)), "3031 : trapèze non parallélogramme")
S = g["S"]
check(abs(vec(I, J)[0] * (S[1] - I[1]) - vec(I, J)[1] * (S[0] - I[0])) < 1e-9
      and abs(vec(L, K)[0] * (S[1] - L[1]) - vec(L, K)[1] * (S[0] - L[0])) < 1e-9, "3031 : (IJ) et (KL) se coupent en S")

# 3021
g = DN["ex3021"]
A, B, C, D, H, K = g["A"], g["B"], g["C"], g["D"], g["H"], g["K"]
check(est_para(A, B, C, D) and d2(A, B) == 36 and d2(A, D) == 25 and d2(D, H) == 16, "3021 : AB = 6, AD = 5, DH = 4")
check(proche(aire([A, B, C, D]), 24) and 6 * 4 == 24, "3021 : aire 24")
check(proche(dist_droite(B, A, D), 4.8) and R(24, 5) == sp.Rational("4.8"), "3021 : BK = 4,8")
t = scal(vec(A, K), vec(A, D)) / d2(A, D)
check(0.2 < t < 0.8, "3021 : K bien à l'intérieur de [AD] (lisible sur la figure)")
check(6 * 5 == 30 and 30 != 24, "3021 : erreur de Lina")
E_, F_, G_, H_, P_ = g["E"], g["F"], g["G"], g["Hh"], g["P"]
check(est_para(E_, F_, G_, H_) and proche(aire([E_, F_, G_, H_]), 12) and P_[0] > F_[0] and d2(H_, P_) == 16,
      "3021 : EFGH aire 12, P hors de [EF]")
check(24 * 100 == 2400 and 12 * 100 == 1200 and R(24, 100) == sp.Rational("0.24") and R(12, 100) == sp.Rational("0.12"),
      "3021 : conversions")

# 3033
g = DN["ex3033"]
check(proche(aire([g["R"], g["S"], g["T"]]), 12) and proche(aire([g["U"], g["V"], g["W"]]), 6), "3033 : triangles 12 et 6")
check(g["P"][0] > g["V"][0] and g["W"][1] == 4 and g["T"][1] == 4, "3033 : hauteurs 4, P hors de [UV]")
check(est_para(g["A"], g["B"], g["C"], g["D"]) and proche(aire([g["A"], g["B"], g["C"], g["D"]]), 15), "3033 : parallélogramme 15")
check(proche(aire([g["D"], g["C"], g["E"]]), 6) and proche(d2(g["D"], g["C"]), 36), "3033 : triangle DCE 6, DC = 6")
check(15 + 6 == 21 and 21 * 100 == 2100, "3033 : total 21 m² = 2 100 dm²")

# 3040
g = DN["ex3040"]
M, N, Pm, Q = g["M"], g["N"], g["P"], g["Q"]
check(est_para(M, N, Pm, Q) and proche(aire([M, N, Pm, Q]), 6) and d2(M, N) == 9, "3040 : massif base 3, aire 6")
check(all(0 <= p[0] <= 6 and 0 <= p[1] <= 4 for p in (M, N, Pm, Q)), "3040 : massif dans la terrasse")
check(6 * 4 - 3 * 2 == 18 and 50 * 50 == 2500 and R(2500, 10000) == R(1, 4), "3040 : 18 m², dalle 0,25 m²")
check(18 / R(1, 4) == 72 and 180000 / 2500 == 72, "3040 : 72 dalles")
check(72 * R(10, 100) == sp.Rational("7.2") and 72 + sp.Rational("7.2") == sp.Rational("79.2") and sp.ceiling(sp.Rational("79.2")) == 80,
      "3040 : 80 dalles")
check(80 * sp.Rational("2.5") == 200, "3040 : 200 €")

# 3038
L_, l_ = 90, 60
per = 2 * L_ + pi * l_
air = L_ * l_ + pi * 30 ** 2
check(abs(sp.N(per) - 368.5) < 0.05 and abs(sp.N(pi * 60) - 188.5) < 0.05, "3038 : tour 368,5 m")
check(abs(sp.N(air) - 8227.4) < 0.05 and abs(sp.N(900 * pi) - 2827.4) < 0.05, "3038 : aire 8 227,4 m²")
check(abs(sp.N(air) / 10000 - 0.8) < 0.05, "3038 : 0,8 ha")
check(sp.ceiling(air / 400) == 21 and 20 * 400 < sp.N(air), "3038 : 21 sacs")
check(sp.simplify((pi * 60 ** 2) / (pi * 30 ** 2)) == 4, "3038 : diamètre au lieu du rayon : ×4")

# 3022
g = DN["ex3022"]
A, B, C, D, O, H, Fa = g["A"], g["B"], g["C"], g["D"], g["O"], g["H"], g["F"]
check(est_para(A, B, C, D) and proche(aire([A, B, C, D]), 84) and d2(A, B) == 144 and d2(D, H) == 49, "3022 : 84 m²")
check(proche(aire([A, B, D]), 42), "3022 : ABD 42")
for tri in ([A, O, B], [B, O, C], [C, O, D], [D, O, A]):
    check(proche(aire(tri), 21), "3022 : parcelle 21 m²")
check(proche(dist_droite(O, A, B), 3.5), "3022 : O à 3,5 m de (AB)")
t = scal(vec(B, Fa), vec(B, D)) / d2(B, D)
check(0.5 < t < 1, "3022 : pied de la hauteur issue de A sur [OD]")
check(21 * 100 == 2100 and 2100 / 50 == 42 and 4 * 21 == 84, "3022 : 42 sachets")

# 3023
g = DN["ex3023"]
A, B, C, D, O = g["A"], g["B"], g["C"], g["D"], g["O"]
check(est_para(A, B, C, D) and d2(A, C) == 36 and d2(B, D) == 16 and scal(vec(A, C), vec(B, D)) == 0, "3023 : losange 6 × 4")
check(proche(aire([A, B, C]), 6) and proche(aire([A, B, C, D]), 12), "3023 : aires 6 et 12")
check(dist_droite(O, A, B) > 1, "3023 : la fontaine tient dans le losange")
plant = 12 - pi
check(abs(sp.N(plant) - 8.86) < 0.005 and abs(sp.N(plant * 100) - 886) < 0.5, "3023 : 8,86 m² ≈ 886 dm²")
check(sp.floor(plant * 100 / 25) == 35 and 36 * 25 == 900 and 900 > sp.N(plant * 100), "3023 : 35 fleurs")
check(abs(sp.N(2 * pi) - 6.28) < 0.005 and sp.ceiling(2 * pi / R(1, 2)) == 13 and 12 * R(1, 2) == 6, "3023 : 13 éléments")


# ===================================================================== contrôle automatique
def frac(s):
    while True:
        n = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
        if n == s:
            return s
        s = n


def tex_vers_py(s):
    s = re.sub(r"\\text\{[^}]*\}(\^\{?2\}?)?", " ", s)
    s = s.replace(r"\mathcal{A}", "AIRE")
    s = s.replace("^\\circ", "").replace("{,}", ".").replace(r"\times", "*").replace(r"\div", "/")
    s = s.replace(r"\,\%", "/100").replace(r"\%", "/100")
    s = s.replace(r"\left", "").replace(r"\right", "").replace(r"\,", "").replace(r"\ ", " ")
    s = frac(s)
    s = re.sub(r"(\d)\s*\\pi", r"\1*pi", s)
    s = s.replace(r"\pi", "pi")
    s = re.sub(r"\^\{?(\d)\}?", r"**\1", s)
    s = s.replace("€", "")
    return s.strip()


NUM = re.compile(r"^[\d.\s+\-*/()pi]+$")


def valeur(expr):
    if not expr or not NUM.match(expr) or not re.search(r"\d", expr):
        return None
    try:
        v = sp.sympify(expr, locals={"pi": sp.pi}, rational=True)
        return v if v.is_number else None
    except Exception:
        return None


def precision(expr):
    m = re.search(r"\.(\d+)\s*$", expr.replace(" ", ""))
    return R(1, 2 * 10 ** len(m.group(1))) if m else R(1, 2)


def egalites(texte, ou):
    global ok
    vus = 0
    blocs = re.findall(r"\$\$(.+?)\$\$", texte, re.S) + re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", texte)
    for m in blocs:
        m = re.sub(r"\\begin\{aligned\}|\\end\{aligned\}", "", m)
        for ligne in re.split(r"\\\\|\\qquad|\\quad", m):
            ligne = ligne.replace("&", "")
            if r"\neq" in ligne or r"\ne " in ligne:
                g_, d_ = re.split(r"\\neq?", ligne, maxsplit=1)
                a, b = valeur(tex_vers_py(g_.split("=")[-1])), valeur(tex_vers_py(d_.split("=")[0]))
                if a is not None and b is not None:
                    vus += 1
                    check(sp.simplify(a - b) != 0, f"{ou} : « {ligne.strip()} » (≠ faux)")
                continue
            morceaux = re.split(r"(=|\\approx)", ligne)
            membres, rels = [], []
            for i, x in enumerate(morceaux):
                if i % 2 == 0:
                    membres.append(tex_vers_py(x))
                else:
                    rels.append(x)
            # on ne garde que la suite finale de membres numériques
            vals = [valeur(x) for x in membres]
            k = len(vals)
            while k > 0 and vals[k - 1] is not None:
                k -= 1
            if len(vals) - k < 2:
                continue
            for i in range(k, len(vals) - 1):
                a, b, rel = vals[i], vals[i + 1], rels[i]
                vus += 1
                if rel == "=":
                    check(sp.simplify(a - b) == 0, f"{ou} : « {ligne.strip()} » → {sp.N(a)} ≠ {sp.N(b)}")
                else:
                    check(abs(sp.N(a - b)) <= precision(membres[i + 1]),
                          f"{ou} : « {ligne.strip()} » → {sp.N(a)} ≉ {membres[i + 1]}")
    return vus


total_auto = 0
for nom in ("cours_271.txt", "fiche_191.txt", "exercices.txt"):
    total_auto += egalites((ICI / nom).read_text(encoding="utf-8"), nom)
check(total_auto >= 80, f"contrôle automatique : seulement {total_auto} égalités lues")

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
check(len(retires) == 11 and not (retires & set(ids)) and set(ids) | retires == set(range(3020, 3041)),
      "Id gardés / retirés (3020 à 3040)")
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
    imgs = re.findall(r"\[IMAGE_(\d+)\]", b)
    check(len(set(imgs)) == len(imgs) and sorted(int(i) for i in imgs) == list(range(1, len(imgs) + 1)),
          f"{eid} : images numérotées 1..n, appelées une fois")
    check("[IMAGE_1]" in en, f"{eid} : figure dans l'énoncé")
    check(len(imgs) >= 2, f"{eid} : figure dans le corrigé")
for nom in ("cours_271.txt", "fiche_191.txt", "exercices.txt"):
    t = (ICI / nom).read_text(encoding="utf-8").lower()
    check("brevet" not in t, f"{nom} : mention du brevet")
    check("pythagore" not in t and "\\sqrt" not in t and "racine" not in t and "produit en croix" not in t
          and "translation" not in t, f"{nom} : notion de 4e")

print(f"{ok} contrôles justes, {len(ko)} erreur(s) ; {total_auto} égalités numériques recalculées automatiquement")
for e in ko:
    print("  ✗", e)
sys.exit(1 if ko else 0)
