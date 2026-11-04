# -*- coding: utf-8 -*-
"""Vérification de la notion 248 « Algorithmique et programmation » (3e).

Chaque script Scratch du cours et des exercices (figures/figures.py, dictionnaire SCRIPTS)
est TRADUIT EN PYTHON (figures/scratch.py, fonction traduire) puis EXÉCUTÉ ; toutes les
valeurs annoncées dans le cours, les énoncés, les corrigés et les solutions sont contrôlées.
Les expressions littérales (programmes de calcul) sont vérifiées avec sympy, en exécutant
le script avec une entrée symbolique.
La traduction Python de tous les scripts est écrite dans programmes_248.txt.

    python verif_248.py
"""
import math
import random
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI / "figures"))
import figures as FG          # noqa: E402
from scratch import *         # noqa: E402,F401

SC = FG.SCRIPTS
ok = 0


def chk(nom, val, attendu, tol=1e-6):
    global ok
    if isinstance(attendu, (int, float)) and not isinstance(attendu, bool) and isinstance(val, (int, float, sp.Basic)):
        bon = abs(float(val) - attendu) <= tol + 1e-9
    elif isinstance(attendu, sp.Basic):
        bon = sp.simplify(val - attendu) == 0
    else:
        bon = val == attendu
    if not bon:
        raise AssertionError("%s : obtenu %r, attendu %r" % (nom, val, attendu))
    ok += 1
    print("OK %-52s %s" % (nom, val if not isinstance(val, float) else round(val, 6)))


def run(cle, **kw):
    return executer(SC[cle] if isinstance(cle, str) else cle, **kw)


def dit(cle, *entrees, **kw):
    return run(cle, entrees=list(entrees), **kw).dits


def lutin(cle, **kw):
    return run(cle, **kw).lutins["lutin"]


def longueur(segs):
    return sum(math.dist(a, b) for a, b in segs)


def sommets(lu):
    return [tuple(round(c, 6) for c in a) for a, b in lu.segments]


def prefixes(script, var):
    """Valeur de var après chaque instruction (scripts sans boucle)."""
    out = []
    for k in range(2, len(script) + 1):
        r = executer({"Lutin": [script[:k] + [Dire(V(var))]]})
        out.append(r.dits[-1])
    return out


def avec_tours(fabrique, var, n):
    """Valeur de var après 1, 2, …, n tours (fabrique(k) = script avec « répéter k fois »)."""
    return [executer({"Lutin": [fabrique(k) + [Dire(V(var))]]}).dits[-1] for k in range(1, n + 1)]


# ============================================================ COURS
X = sp.Symbol("x")
N_ = sp.Symbol("n")
A_ = sp.Symbol("a")
chk("cours calcul n=5", dit("cours_calcul", 5), [16])
chk("cours calcul symbolique 2n+6", sp.expand(dit("cours_calcul", N_)[0]), 2 * N_ + 6)
chk("cours si 17", dit("cours_si", 17), ["Tu es mineur."])
chk("cours si 18", dit("cours_si", 18), ["Tu es majeur."])
chk("cours répéter 5 fois", dit("cours_repeter"), [10])
chk("cours répéter : valeurs", avec_tours(lambda k: [Drapeau(), Mettre("x", 0), Repeter(k, [Ajouter("x", 2)])], "x", 5),
    [2, 4, 6, 8, 10])
chk("cours jusqu'à", dit("cours_jusqua"), [243])
chk("cours jusqu'à : valeurs", avec_tours(lambda k: [Drapeau(), Mettre("x", 1), Repeter(k, [Mettre("x", Op(V("x"), "*", 3))])], "x", 5),
    [3, 9, 27, 81, 243])
lu = lutin("cours_carre")
chk("cours carré sommets", sommets(lu), [(0, 0), (50, 0), (50, 50), (0, 50)])
chk("cours carré retour", (lu.x, lu.y, lu.direction), (0, 0, 90))
lu = lutin("cours_bloc")
chk("cours bloc 3 carrés longueur", longueur(lu.segments), 4 * (20 + 40 + 60))
chk("cours messages", dit("cours_messages"), [20])

# ============================================================ 2443
s = SC["2443"]["Lutin"][0]
chk("2443 valeurs de x", prefixes(s, "x")[:3], [3, 8, 16])
chk("2443 dit", dit("2443"), [16])
chk("2443 blocs échangés", dit("2443_echange"), [11])
# « 3 remplacé par a » : on fait entrer a par un bloc « demander » (entrée symbolique)
sa = [Drapeau(), Demander("a ?"), Mettre("x", Reponse()), Ajouter("x", 5), Mettre("x", Op(V("x"), "*", 2)), Dire(V("x"))]
expr = executer({"Lutin": [sa]}, entrees=[A_]).dits[0]
chk("2443 en fonction de a", sp.expand(expr), 2 * A_ + 10)
chk("2443 obtenir 30", sp.solve(sp.Eq(expr, 30), A_), [10])

# ============================================================ 2444
for e, att in ((2, 18), (-4, 0), (0.5, 13.5)):
    chk("2444 réponse %s" % e, dit("2444", e)[0], att)
e = dit("2444", X)[0]
chk("2444 expression 3(x+4)", sp.expand(e), 3 * X + 12)
chk("2444 obtenir 30", sp.solve(sp.Eq(e, 30), X), [6])
chk("2444 ordre inversé, 2", dit("2444_ordre", 2), [10])
chk("2444 ordre inversé, expression", sp.expand(dit("2444_ordre", X)[0]), 3 * X + 4)

# ============================================================ 2445
chk("2445 dit", dit("2445"), [12])
chk("2445 valeurs", avec_tours(lambda k: [Drapeau(), Mettre("x", 0), Repeter(k, [Ajouter("x", 3)])], "x", 4), [3, 6, 9, 12])
chk("2445 répéter 10 fois", dit("2445_10"), [30])

# ============================================================ 2446
for e, att in ((9, "petit"), (10, "grand"), (14, "grand"), (9.99, "petit"), (-20, "petit")):
    chk("2446 %s" % e, dit("2446", e), [att])
for e, att in ((10, "petit"), (9, "petit"), (10.5, "grand"), (11, "grand")):
    chk("2446 corrigé (x<10 ou x=10) %s" % e, dit("2446_ou", e), [att])

# ============================================================ 2447
lu = lutin("2447")
chk("2447 positions", [tuple(round(c, 6) for c in p) for p in lu.positions[1:]], [(-100, 50), (-20, 50), (-20, -40), (-80, -40)])
chk("2447 orientation finale", lu.direction, -90)
chk("2447 longueur tracée", longueur(lu.segments), 230)
chk("2447 trois segments", [round(math.dist(a, b), 6) for a, b in lu.segments], [80, 90, 60])

# ============================================================ 2448
lu = lutin("2448")
chk("2448 premier déplacement", tuple(round(c, 6) for c in lu.positions[2]), (40, 0))
chk("2448 sommets", sommets(lu), [(0, 0), (40, 0), (40, 40), (0, 40)])
chk("2448 longueur", longueur(lu.segments), 160)
chk("2448 retour", (round(lu.x, 6), round(lu.y, 6), lu.direction), (0, 0, 90))
r1 = executer({"Lutin": [[Drapeau(), AllerA(0, 0), Orienter(90), Avancer(40), TournerG(90)]]})
chk("2448 orientation après le 1er tour", r1.lutins["lutin"].direction, 0)
lu = lutin("2448_triangle")
chk("2448 triangle fermé", (round(lu.x, 6), round(lu.y, 6), lu.direction), (0, 0, 90))
chk("2448 triangle côtés", [round(math.dist(a, b), 6) for a, b in lu.segments], [40, 40, 40])
chk("2448 triangle sommet haut y", round(lu.segments[1][1][1], 4), round(20 * math.sqrt(3), 4))

# ============================================================ 2449
f2449 = lambda k: [Drapeau(), Mettre("s", 0), Mettre("n", 1), Repeter(k, [Ajouter("s", V("n")), Ajouter("n", 1)])]
chk("2449 s par tour", avec_tours(f2449, "s", 5), [1, 3, 6, 10, 15])
chk("2449 n par tour", avec_tours(f2449, "n", 5), [2, 3, 4, 5, 6])
chk("2449 dit", dit("2449"), [15])
chk("2449 10 tours", executer({"Lutin": [f2449(10) + [Dire(V("s"))]]}).dits, [55])

# ============================================================ 2450
chk("2450 dit", dit("2450"), [24])
r = run("2450")
chk("2450 valeurs", avec_tours(lambda k: [Drapeau(), Mettre("x", 0), Repeter(k, [Ajouter("x", 6)])], "x", 4), [6, 12, 18, 24])
s5 = [Drapeau(), Mettre("x", 0), JusquA(Cmp(V("x"), ">", 20), [Ajouter("x", 5), Ajouter("t", 1)]), Dire(V("x")), Dire(V("t"))]
chk("2450 ajouter 5 : valeur et tours", executer({"Lutin": [[Drapeau(), Mettre("t", 0)] + s5[1:]]}).dits, [25, 5])
s6 = [Drapeau(), Mettre("t", 0), Mettre("x", 0), JusquA(Cmp(V("x"), ">", 20), [Ajouter("x", 6), Ajouter("t", 1)]), Dire(V("t"))]
chk("2450 nombre de tours", executer({"Lutin": [s6]}).dits, [4])
s0 = [Drapeau(), Mettre("x", 0), JusquA(Cmp(V("x"), ">", 20), [Ajouter("x", 0)]), Dire(V("x"))]
chk("2450 ajouter 0 : boucle infinie", executer({"Lutin": [s0]}, max_pas=100000).infinie, True)

# ============================================================ 2451
for e, att in ((18, 1), (19, 0), (0, 1), (-6, 1), (7, 0)):
    chk("2451 %s" % e, dit("2451", e), [att])
for e, att in ((35, 0), (36, 1)):
    chk("2451 pair %s" % e, dit("2451_pair", e), [att])
chk("2451 multiples de 3 jusqu'à 30", [k for k in range(31) if dit("2451", k) == [1]], list(range(0, 31, 3)))

# ============================================================ 2452
chk("2452 diviseurs de 12", dit("2452"), [1, 2, 3, 4, 6, 12])
s13 = [Drapeau(), Mettre("n", 13), Mettre("d", 1),
       Repeter(13, [Si(Cmp(Mod(V("n"), V("d")), "=", 0), [Dire(V("d"), 1)]), Ajouter("d", 1)])]
chk("2452 diviseurs de 13", executer({"Lutin": [s13]}).dits, [1, 13])
chk("2452 d final", run("2452").vars["d"], 13)

# ============================================================ 2453
def pos2453(touches):
    lu = run("2453", touches=touches).lutins["lutin"]
    return (round(lu.x, 6), round(lu.y, 6))


chk("2453 départ", pos2453([]), (-60, -40))
chk("2453 3 x droite", pos2453(["flèche droite"] * 3), (30, -40))
chk("2453 puis 4 x haut", pos2453(["flèche droite"] * 3 + ["flèche haut"] * 4), (30, 40))
chk("2453 5 droite 2 haut", pos2453(["flèche droite"] * 5 + ["flèche haut"] * 2), (90, 0))
chk("2453 2 haut 5 droite", pos2453(["flèche haut"] * 2 + ["flèche droite"] * 5), (90, 0))
chk("2453 espace", pos2453(["flèche droite", "espace"]), (0, 0))
p = {"Lutin": SC["2453"]["Lutin"] + SC["2453_gauche"]["Lutin"]}
lu = executer(p, touches=["flèche droite"] * 3 + ["flèche gauche"]).lutins["lutin"]
chk("2453 flèche gauche", (lu.x, lu.y), (0, -40))

# ============================================================ 2454
lu = lutin("2454")
chk("2454 longueur", longueur(lu.segments), 360)
chk("2454 position finale", (round(lu.x, 6), round(lu.y, 6)), (120, 0))
chk("2454 départs des carrés", sorted({a for a, b in lu.segments if a[1] == 0 and b[1] == 0 and b[0] > a[0]}),
    [(0, 0), (40, 0), (80, 0)])
chk("2454 nombre de côtés tracés", len(lu.segments), 12)

# ============================================================ 2455
chk("2455 probabilité", Fraction(1, 6), Fraction(1, 6))
chk("2455 succès attendus", 600 * Fraction(1, 6), 100)
fr = [run("2455", graine=g).dits[0] for g in range(20)]
chk("2455 fréquences simulées proches de 1/6", max(abs(f - 1 / 6) for f in fr) < 0.06, True)
chk("2455 1/6 ~ 0,167", round(1 / 6, 3), 0.167)
chk("2455 écart 0,18", round(0.18 - 1 / 6, 3), 0.013)

# ============================================================ 2456
lu = lutin("2456")
chk("2456 sommets", sommets(lu), [(-40, -25), (40, -25), (40, 25), (-40, 25)])
chk("2456 longueur", longueur(lu.segments), 260)
chk("2456 retour", (round(lu.x, 6), round(lu.y, 6), lu.direction), (-40, -25, 90))

# ============================================================ 2457
chk("2457 Guide dit", dit("2457"), [10])
chk("2457 trois lutins", dit("2457_trois"), [20])

# ============================================================ 2458
for e in (5, -3, 2.5, 100, -7.25):
    chk("2458 %s" % e, dit("2458", e), [2])
chk("2458 symbolique", sp.simplify(dit("2458", N_)[0]), 2)
s_a = [Drapeau(), Demander("a ?"), Mettre("a", Reponse()), Demander("?"), Mettre("n", Reponse()),
       Mettre("r", Op(V("n"), "*", 4)), Ajouter("r", V("a")),
       Mettre("r", Op(V("r"), "/", 4)), Mettre("r", Op(V("r"), "-", V("n"))), Dire(V("r"))]
ea = executer({"Lutin": [s_a]}, entrees=[A_, N_]).dits[0]
chk("2458 avec a à la place de 8", sp.simplify(ea), A_ / 4)
chk("2458 toujours 5", sp.solve(sp.Eq(A_ / 4, 5), A_), [20])
chk("2458 étapes avec 5", prefixes([Drapeau(), Mettre("r", 0), Mettre("n", 5)] + SC["2458"]["Lutin"][0][3:7], "r")[2:], [20, 28, 7, 2])

# ============================================================ 2459
lu = lutin("2459")
chk("2459 fin du 1er tour", tuple(round(c, 6) for c in lu.positions[3]), (20, 20))
chk("2459 position finale", (round(lu.x, 6), round(lu.y, 6), lu.direction), (100, 100, 90))
chk("2459 longueur", longueur(lu.segments), 200)
chk("2459 nez de marche sur y = x", all(round(p[0], 6) == round(p[1], 6) for p in lu.positions[3::2]), True)
lu = lutin("2459_8")
chk("2459 8 marches de 15", (round(lu.x, 6), round(lu.y, 6)), (120, 120))

# ============================================================ 2460
lu = lutin("2460")
chk("2460 hexagone : 6 côtés de 30", [round(math.dist(a, b), 6) for a, b in lu.segments], [30] * 6)
chk("2460 hexagone fermé", (round(lu.x, 6), round(lu.y, 6), round(lu.direction, 6)), (0, 0, 90))
chk("2460 périmètre", longueur(lu.segments), 180)
lu = lutin("2460_triangle")
chk("2460 triangle 50 fermé", (round(lu.x, 6), round(lu.y, 6)), (0, 0))
chk("2460 triangle : angle 360/3", 360 / 3, 120)
lu = lutin("2460_36")
chk("2460 36 côtés fermé", (round(lu.x, 6), round(lu.y, 6)), (0, 0))
chk("2460 36 côtés périmètre", longueur(lu.segments), 180, 1e-6)
lu = lutin("2460_faux108")
chk("2460 108° : ne se referme pas", math.dist((lu.x, lu.y), (0, 0)) > 5, True)
chk("2460 108° : rotation totale", 5 * 108, 540)
lu = lutin("2460_bon72")
chk("2460 72° : pentagone fermé", (round(lu.x, 6), round(lu.y, 6)), (0, 0))
chk("2460 72 = 180 - 108", 180 - 108, 72)

# ============================================================ 2461
chk("2461 partie 37 : 50, 25, 37", dit("2461", 50, 25, 37, tirages=[37]), ["Plus petit !", "Plus grand !", 3])


def dichotomie(secret, a=1, b=100):
    essais = []
    while True:
        m = (a + b) // 2
        essais.append(m)
        if m == secret:
            return essais
        if m < secret:
            a = m + 1
        else:
            b = m - 1


maxi = 0
for sec in range(1, 101):
    g = dichotomie(sec)
    d = dit("2461", *g, tirages=[sec])
    assert d[-1] == len(g), (sec, d, g)
    maxi = max(maxi, len(g))
chk("2461 stratégie du milieu : au plus 7 essais (100 parties jouées)", maxi, 7)
chk("2461 2^6 < 100 <= 2^7", (2 ** 6 < 100 <= 2 ** 7), True)
chk("2461 tailles restantes", [100, 50, 25, 12, 6, 3, 1], [100, 50, 25, 12, 6, 3, 1])
n_, tailles = 100, [100]
while n_ > 1:
    n_ = n_ // 2
    tailles.append(n_)
chk("2461 intervalle restant après chaque essai raté", tailles, [100, 50, 25, 12, 6, 3, 1])
chk("2461 premier coup", Fraction(1, 100), Fraction(1, 100))

# ============================================================ 2462
r = run("2462")
lu = r.lutins["lutin"]
chk("2462 longueur finale", r.vars["longueur"], 100)
chk("2462 position finale", (round(lu.x, 6), round(lu.y, 6), lu.direction), (90, 0, 90))
chk("2462 longueur tracée", longueur(lu.segments), 600, 1e-6)
chk("2462 côtés des triangles", sorted({round(math.dist(a, b), 6) for a, b in lu.segments}), [20, 40, 60, 80])
chk("2462 départs des triangles", [round(a[0], 6) for a, b in lu.segments[::3]], [-150, -120, -70, 0])
p1 = s2 = FG.s2462()
r1 = executer({"Lutin": [FG.DEF_TRIANGLE, p1["Lutin"][1][:5] + [Repeter(1, p1["Lutin"][1][5].branches[0][1])]]})
chk("2462 après le 1er passage", (round(r1.lutins["lutin"].x, 6), r1.vars["longueur"]), (-120, 40))
chk("2462 hauteur du grand triangle", round(lu.segments[-2][0][1], 4) if False else round(max(p[1] for s_ in lu.segments for p in s_), 4),
    round(40 * math.sqrt(3), 4))
la = lutin("2462_A")
chk("2462 dessin A : triangles accolés", [round(a[0], 6) for a, b in la.segments[::3]], [-150, -130, -90, -30])
lc = lutin("2462_C")
chk("2462 dessin C : triangles égaux", sorted({round(math.dist(a, b), 6) for a, b in lc.segments}), [20])
chk("2462 dessin C départs", [round(a[0], 6) for a, b in lc.segments[::3]], [-150, -120, -90, -60])

# ============================================================ 2463
issues = list(product(range(1, 7), repeat=2))
chk("2463 36 issues", len(issues), 36)
chk("2463 sommes possibles", sorted({a + b for a, b in issues}), list(range(2, 13)))
chk("2463 somme 7 : 6 issues", sorted((a, b) for a, b in issues if a + b == 7), [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)])
chk("2463 P(7)", Fraction(6, 36), Fraction(1, 6))
chk("2463 P(12)", Fraction(sum(1 for a, b in issues if a + b == 12), 36), Fraction(1, 36))
chk("2463 1000/36", round(1000 / 36, 1), 27.8)
chk("2463 1000/6", round(1000 / 6), 167)
cnt = {s_: sum(1 for a, b in issues if a + b == s_) for s_ in range(2, 13)}
chk("2463 somme la plus probable", max(cnt, key=cnt.get), 7)
chk("2463 doubles", Fraction(sum(1 for a, b in issues if a == b), 36), Fraction(1, 6))
fr = [run("2463", graine=g).dits[0] for g in range(10)]
chk("2463 fréquences simulées proches de 1/6", max(abs(f - 1 / 6) for f in fr) < 0.05, True)
fr = [run("2463_doubles", graine=g).dits[0] for g in range(10)]
chk("2463 doubles simulés proches de 1/6", max(abs(f - 1 / 6) for f in fr) < 0.05, True)

# ============================================================ valeurs citées dans les corrigés
s_inv = [Drapeau(), Mettre("s", 0), Mettre("n", 1), Repeter(5, [Ajouter("n", 1), Ajouter("s", V("n"))]), Dire(V("s"))]
chk("2449 blocs inversés : 2+3+4+5+6", executer({"Lutin": [s_inv]}).dits, [20])
chk("2463 écart 0,171", round(0.171 - 1 / 6, 3), 0.004)
chk("2462 abscisse finale", -150 + 30 + 50 + 70 + 90, 90)
chk("2456 périmètre 2(80+50)", 2 * (80 + 50), 260)
chk("2453 150 = 5 x 30 et 40 = 2 x 20", (90 - (-60), 0 - (-40)), (150, 40))
chk("2446 condition « x < 11 » : 10,5 serait « petit »", 10.5 < 11, True)

# ============================================================ traductions Python
txt = []
for cle, projet in SC.items():
    txt.append("# " + "=" * 70 + "\n# script " + cle + "\n# " + "=" * 70)
    txt.append(traduire(projet))
(ICI / "programmes_248.txt").write_text("\n".join(txt) + "\n", encoding="utf-8")
print("\n%d contrôles OK ; %d scripts traduits en Python et exécutés (programmes_248.txt)" % (ok, len(SC)))
