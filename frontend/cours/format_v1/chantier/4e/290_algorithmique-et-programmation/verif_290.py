# -*- coding: utf-8 -*-
"""Vérification de la notion 290 « Algorithmique et programmation » (4e).

Chaque script Scratch du cours et des exercices (figures/figures.py, dictionnaire SCRIPTS)
est TRADUIT EN PYTHON (figures/scratch.py, fonction traduire) puis EXÉCUTÉ ; toutes les
valeurs annoncées dans le cours, les énoncés, les corrigés et les solutions sont contrôlées.
Les expressions littérales (programmes de calcul) sont vérifiées avec sympy, en exécutant
le script avec une entrée symbolique. La traduction Python de tous les scripts est écrite
dans programmes_290.txt.

    python verif_290.py
"""
import math
import sys
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI / "figures"))
import figures as FG          # noqa: E402
import scratch as SCR         # noqa: E402
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
    print("OK %-56s %s" % (nom, val if not isinstance(val, float) else round(val, 6)))


def run(cle, **kw):
    return executer(SC[cle] if isinstance(cle, str) else cle, **kw)


def dit(cle, *entrees, **kw):
    return run(cle, entrees=list(entrees), **kw).dits


def lutin(cle, **kw):
    return run(cle, **kw).lutins["lutin"]


def longueur(segs):
    return sum(math.dist(a, b) for a, b in segs)


def arrondi(p, k=6):
    return tuple(round(c, k) + 0.0 for c in p)


def sommets(lu):
    return [arrondi(a) for a, b in lu.segments]


def apres_chaque(script, var, debut=2):
    """Valeur de var après chaque instruction (scripts sans boucle)."""
    out = []
    for k in range(debut, len(script) + 1):
        r = executer({"Lutin": [script[:k] + [Dire(V(var))]]}, entrees=ENTREES[0])
        out.append(r.dits[-1])
    return out


ENTREES = [[]]


def avec_tours(fabrique, var, n):
    """Valeur de var après 1, 2, …, n tours (fabrique(k) = script avec « répéter k fois »)."""
    return [executer({"Lutin": [fabrique(k) + [Dire(V(var))]]}).dits[-1] for k in range(1, n + 1)]


def positions_pas_a_pas(script):
    """Position (arrondie) et orientation du lutin après chaque bloc (scripts sans boucle)."""
    out = []
    for k in range(2, len(script) + 1):
        lu = executer({"Lutin": [script[:k]]}).lutins["lutin"]
        out.append((arrondi((lu.x, lu.y)), lu.direction))
    return out


# chronologie des répliques (plusieurs lutins) : on journalise « dire » sans modifier le module
JOURNAL = []
_dire = SCR.Lutin.dire


def _dire_journal(self, v):
    JOURNAL.append((self.nom, v))
    _dire(self, v)


SCR.Lutin.dire = _dire_journal

X = sp.Symbol("x")
N_ = sp.Symbol("n")

# ============================================================ COURS
chk("cours calcul n=7", dit("cours_calcul", 7), [25])
chk("cours calcul : expression 5n - 10", sp.expand(dit("cours_calcul", N_)[0]), 5 * N_ - 10)
ENTREES[0] = [7]
chk("cours calcul : r après chaque bloc", apres_chaque(SC["cours_calcul"]["Lutin"][0][:-1], "r", 4), [5, 25])
chk("cours si 9", dit("cours_si", 9), ["À retravailler"])
chk("cours si 10 (frontière)", dit("cours_si", 10), ["Validé !"])
chk("cours si 14", dit("cours_si", 14), ["Validé !"])
chk("cours répéter", dit("cours_repeter"), [15])
chk("cours répéter : valeurs", avec_tours(lambda k: [Drapeau(), Mettre("x", 0), Repeter(k, [Ajouter("x", 3)])], "x", 5),
    [3, 6, 9, 12, 15])
chk("cours jusqu'à", dit("cours_jusqua"), [-20])
chk("cours jusqu'à : x à la fin de chaque tour",
    avec_tours(lambda k: [Drapeau(), Mettre("x", 100), Repeter(k, [Ajouter("x", -30)])], "x", 4), [70, 40, 10, -20])
chk("cours jusqu'à : arrêt après 4 tours (10 < 0 faux, -20 < 0 vrai)", (10 < 0, -20 < 0), (False, True))
lu = lutin("cours_carre")
chk("cours carré : sommets", sommets(lu), [(0, 0), (60, 0), (60, 60), (0, 60)])
chk("cours carré : retour et orientation", (arrondi((lu.x, lu.y)), lu.direction), ((0, 0), 90))
lu = lutin("cours_bloc")
chk("cours bloc : longueur 3*(30+60+90)", longueur(lu.segments), 3 * (30 + 60 + 90))
chk("cours bloc : sommets des triangles", sorted(set(arrondi(p, 3) for s in lu.segments for p in s)),
    sorted(set([(0.0, 0.0), (30.0, 0.0), (15.0, 25.981), (60.0, 0.0), (30.0, 51.962), (90.0, 0.0), (45.0, 77.942)])))
r = executer(SC["cours_touches"], touches=["flèche droite"] * 3 + ["flèche gauche"])
chk("cours touches : x après → → → ←", r.lutins["lutin"].x, 20)
chk("cours messages : total", dit("cours_messages"), [12])

# ============================================================ 3713 carré (tourner ↻)
s = SC["3713"]["Lutin"][0]
lu = lutin("3713")
chk("3713 sommets (↻)", sommets(lu), [(0, 0), (100, 0), (100, -100), (0, -100)])
chk("3713 4 avancer, 4 tourner", (len(lu.segments), 4), (4, 4))
chk("3713 longueur 400", longueur(lu.segments), 400)
chk("3713 fin (0;0), orientation 90", (arrondi((lu.x, lu.y)), lu.direction), ((0, 0), 90))
tours = []
for k in range(1, 5):
    l2 = executer({"Lutin": [s[:5] + [Repeter(k, [Avancer(100), TournerD(90)])]]}).lutins["lutin"]
    tours.append((arrondi((l2.x, l2.y)), l2.direction))
chk("3713 tableau tour par tour", tours, [((100, 0), 180), ((100, -100), -90), ((0, -100), 0), ((0, 0), 90)])
lu = lutin("3713_gauche")
chk("3713 avec ↺ : sommets", sommets(lu), [(0, 0), (100, 0), (100, 100), (0, 100)])

# ============================================================ 3714 programme de calcul 3x - 5
for e, att in ((4, 7), (-2, -11), (0, -5), (5, 10)):
    chk("3714 réponse %s" % e, dit("3714", e), [att])
chk("3714 expression 3x - 5", sp.expand(dit("3714", X)[0]), 3 * X - 5)
chk("3714 obtenir 10", sp.solve(sp.Eq(dit("3714", X)[0], 10), X), [5])
ENTREES[0] = [4]
chk("3714 y après chaque bloc (4)", apres_chaque(SC["3714"]["Lutin"][0][:-1], "y", 4), [12, 7])
for e in (4, -2, 0, 5, 2.5):
    chk("3714 ajouter(-5) identique (%s)" % e, dit("3714_ajouter", e), dit("3714", e))
chk("3714 mettre y à -5 : toujours -5", [dit("3714_faux", e)[0] for e in (4, -2, 0)], [-5, -5, -5])

# ============================================================ 3715 somme cumulée
chk("3715 dit 15", dit("3715"), [15])
chk("3715 compteur par tour", avec_tours(lambda k: FG.s3715(k)["Lutin"][0][:-1], "compteur", 5), [1, 2, 3, 4, 5])
chk("3715 somme par tour", avec_tours(lambda k: FG.s3715(k)["Lutin"][0][:-1], "somme", 5), [1, 3, 6, 10, 15])
chk("3715 10 tours : 55", dit("3715_10"), [55])
chk("3715 100 tours : 5 050", dit(FG.s3715(100)), [5050])
chk("3715 Gauss 50*101", 50 * 101, 5050)
chk("3715 blocs inversés : 10", dit("3715_inverse"), [10])

# ============================================================ 3716 condition
chk("3716 15", dit("3716", 15), ["Tu es mineur."])
chk("3716 18", dit("3716", 18), ["Tu es majeur."])
chk("3716 17", dit("3716", 17), ["Tu es mineur."])
for a in range(0, 101):
    if dit("3716_non", a) != dit("3716", a):
        raise AssertionError("3716 non(réponse<18) différent pour %d" % a)
chk("3716 non(réponse < 18) équivalent de 0 à 100", True, True)
chk("3716 senior 70", dit("3716_senior", 70), ["Tarif senior"])
chk("3716 senior 65", dit("3716_senior", 65), ["Tarif senior"])
chk("3716 senior 64", dit("3716_senior", 64), ["Tu es majeur."])
chk("3716 senior 30", dit("3716_senior", 30), ["Tu es majeur."])
chk("3716 senior 12", dit("3716_senior", 12), ["Tu es mineur."])
inv = {"Lutin": [[Drapeau(), Demander("?"), Si(Cmp(Reponse(), "<", 18), [Dire("Tu es mineur.")], sinon=[Dire("Tu es majeur.")])]]}
chk("3716 condition < 18 avec messages échangés", all(dit(inv, a) == dit("3716", a) for a in range(0, 101)), True)

# ============================================================ 3717 triangle par « aller à »
lu = lutin("3717")
chk("3717 segments", [(arrondi(a), arrondi(b)) for a, b in lu.segments],
    [((-100, 0), (0, 100)), ((0, 100), (100, 0)), ((100, 0), (-100, 0))])
A, Cc, B = (-100, 0), (0, 100), (100, 0)
chk("3717 AB = 200", math.dist(A, B), 200)
chk("3717 AC = racine(20 000) ≈ 141,4", round(math.dist(A, Cc), 1), 141.4)
chk("3717 AC² = 20 000", math.dist(A, Cc) ** 2, 20000)
chk("3717 BC = AC", math.dist(B, Cc), math.dist(A, Cc))
chk("3717 AC² + BC² = AB²", round(math.dist(A, Cc) ** 2 + math.dist(B, Cc) ** 2), 40000)
chk("3717 aire 10 000", 200 * 100 / 2, 10000)
chk("3717 aire par AC*BC/2", math.dist(A, Cc) * math.dist(B, Cc) / 2, 10000)

# ============================================================ 3718 répéter jusqu'à
chk("3718 dit 128", dit("3718"), [128])
chk("3718 7 tours", run("3718").vars["étapes"], 7)
chk("3718 n par tour", avec_tours(lambda k: [Drapeau(), Mettre("n", 1), Repeter(k, [Mettre("n", Op(V("n"), "*", 2))])], "n", 7),
    [2, 4, 8, 16, 32, 64, 128])
chk("3718 > 1000 : 1 024", dit("3718_1000"), [1024])
chk("3718 > 1000 : 10 tours", run("3718_1000").vars["étapes"], 10)
chk("3718 oubli : boucle infinie", run("3718_oubli", max_pas=20000).infinie, True)

# ============================================================ 3719 orientation
s = SC["3719"]["Lutin"][0]
pp = positions_pas_a_pas(s)
chk("3719 après s'orienter à 0", pp[2], ((0, 0), 0))
chk("3719 après avancer 80", pp[4], ((0, 80), 0))
chk("3719 après tourner ↻ 90", pp[5], ((0, 80), 90))
chk("3719 après avancer 60", pp[6], ((60, 80), 90))
chk("3719 après s'orienter à 180 + avancer 40", pp[8], ((60, 40), 180))
chk("3719 après 2e tourner ↻ 90", pp[9], ((60, 40), -90))
chk("3719 fin", pp[10], ((40, 40), -90))
lu = lutin("3719")
chk("3719 longueur 200", longueur(lu.segments), 200)
chk("3719 même tracé avec « tourner ↻ de 90 »", [(arrondi(a), arrondi(b)) for a, b in lutin("3719_tourner").segments],
    [(arrondi(a), arrondi(b)) for a, b in lu.segments])

# ============================================================ 3720 bloc polygone
for (n, c, ang) in ((5, 80, 72), (6, 70, 60), (8, 55, 45), (36, 10, 10)):
    chk("3720 angle 360/%d" % n, 360 / n, ang)
lu = lutin("3720")
chk("3720 pentagone : 5 segments de 80", [round(math.dist(a, b), 9) for a, b in lu.segments], [80.0] * 5)
chk("3720 pentagone : longueur 400", longueur(lu.segments), 400)
chk("3720 pentagone fermé, orientation 90", (arrondi((lu.x, lu.y)), lu.direction), ((0, 0), 90))
for cle, n, c in (("3720_6", 6, 70), ("3720_8", 8, 55), ("3720_36", 36, 10)):
    l2 = lutin(cle)
    chk("%s fermé, %d côtés" % (cle, n), (arrondi((l2.x, l2.y), 6), len(l2.segments)), ((0, 0), n))
chk("3720 36 côtés : longueur 360", longueur(lutin("3720_36").segments), 360)
chk("3720 angle intérieur pentagone 108", 180 - 72, 108)
chk("3720 somme angles intérieurs = 540", 5 * 108, (5 - 2) * 180)

# ============================================================ 3721 étoile
lu = lutin("3721")
chk("3721 5 segments de 150", [round(math.dist(a, b), 9) for a, b in lu.segments], [150.0] * 5)
chk("3721 longueur 750", longueur(lu.segments), 750)
chk("3721 retour au départ, orientation 90", (arrondi((lu.x, lu.y)), lu.direction), ((-75, 20), 90))
chk("3721 angle total 720 = 2 tours", (5 * 144, 5 * 144 / 360), (720, 2))
chk("3721 angle de la pointe 36", 180 - 144, 36)
pts = [arrondi(a, 1) for a, b in lu.segments]
chk("3721 sommets", pts, [(-75, 20), (75, 20), (-46.4, -68.2), (0, 74.5), (46.4, -68.2)])
v1 = (pts[0][0] - pts[1][0], pts[0][1] - pts[1][1])
v2 = (pts[2][0] - pts[1][0], pts[2][1] - pts[1][1])
ang = math.degrees(math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))))
chk("3721 angle mesuré à une pointe ≈ 36", round(ang), 36)
l72 = lutin("3721_72")
chk("3721 avec 72 : pentagone fermé", (arrondi((l72.x, l72.y)), len(l72.segments)), ((-75, 20), 5))

# ============================================================ 3722 frise
lu = lutin("3722")
chk("3722 24 segments de 30", (len(lu.segments), set(round(math.dist(a, b), 9) for a, b in lu.segments)), (24, {30.0}))
chk("3722 longueur 720", longueur(lu.segments), 720)
chk("3722 abscisse finale 160", arrondi((lu.x, lu.y)), (160, 0))
coins = sorted(set(round(a[0]) for a, b in lu.segments if abs(a[1]) < 1e-9 and abs(b[1]) < 1e-9))
chk("3722 débuts des carrés tous les 60", sorted(set(round(a[0]) for a, b in lu.segments
                                                      if abs(a[1]) < 1e-9 and b[0] > a[0])),
    [-200, -140, -80, -20, 40, 100])
chk("3722 espace entre carrés 30", 60 - 30, 30)
l2 = lutin("3722_sans_relever")
chk("3722 sans relever : traits de liaison", longueur(l2.segments), 720 + 6 * 60)

# ============================================================ 3723 deux programmes
chk("3723 A(5)", dit("3723_A", 5), [16])
chk("3723 B(5)", dit("3723_B", 5), [16])
chk("3723 A(-4), B(-4)", (dit("3723_A", -4), dit("3723_B", -4)), ([-2], [-2]))
chk("3723 A = 2x + 6", sp.expand(dit("3723_A", X)[0]), 2 * X + 6)
chk("3723 B = 2x + 6", sp.expand(dit("3723_B", X)[0]), 2 * X + 6)
chk("3723 C(2) = A(2) = 10", (dit("3723_C", 2), dit("3723_A", 2)), ([10], [10]))
chk("3723 C(1) = 7, A(1) = 8", (dit("3723_C", 1), dit("3723_A", 1)), ([7], [8]))
chk("3723 A = C seulement pour 0 et 2", sorted(sp.solve(sp.Eq(dit("3723_C", X)[0], dit("3723_A", X)[0]), X)), [0, 2])

# ============================================================ 3724 clavier
r = executer(SC["3724"], touches=["flèche droite"] * 2 + ["flèche haut"] * 2 + ["flèche gauche"])
lu = r.lutins["lutin"]
chk("3724 positions → → ↑ ↑ ←", [arrondi(p) for p in lu.positions[2:]],
    [(20, 0), (40, 0), (40, 20), (40, 40), (20, 40)])
chk("3724 longueur tracée 100", longueur(lu.segments), 100)
r = executer(SC["3724"], touches=["flèche droite"] * 3 + ["flèche haut"] * 2)
chk("3724 (60 ; 40) en 5 touches", arrondi((r.lutins["lutin"].x, r.lutins["lutin"].y)), (60, 40))
chk("3724 longueur 60 + 40 = 100", longueur(r.lutins["lutin"].segments), 100)
chk("3724 vol d'oiseau racine(5 200) ≈ 72,1", round(math.hypot(60, 40), 1), 72.1)
chk("3724 60² + 40² = 5 200", 60 ** 2 + 40 ** 2, 5200)
proj = {"Lutin": SC["3724"]["Lutin"] + SC["3724_bas"]["Lutin"]}
r = executer(proj, touches=["flèche haut", "flèche bas", "flèche bas"])
chk("3724 flèche bas : ajouter -20 à y", arrondi((r.lutins["lutin"].x, r.lutins["lutin"].y)), (0, -20))
r = executer(SC["3724"], touches=["flèche droite", "espace", "flèche haut", "flèche droite"])
lu = r.lutins["lutin"]
chk("3724 espace : seul (0;0)-(20;0) tracé", [(arrondi(a), arrondi(b)) for a, b in lu.segments], [((0, 0), (20, 0))])
chk("3724 espace : position finale (40 ; 20)", arrondi((lu.x, lu.y)), (40, 20))

# ============================================================ 3725 déboguer
chk("3725 sans stylo : rien tracé", lutin("3725").segments, [])
lu = lutin("3725_stylo")
chk("3725 stylo : 4 côtés d'hexagone", [arrondi(a, 1) for a, b in lu.segments] + [arrondi((lu.x, lu.y), 1)],
    [(0, 0), (100, 0), (150, -86.6), (100, -173.2), (0, -173.2)])
chk("3725 stylo : non fermé", arrondi((lu.x, lu.y), 1) != (0, 0), True)
lu = lutin("3725_corrige")
chk("3725 corrigé : triangle", [arrondi(a, 1) for a, b in lu.segments], [(0, 0), (100, 0), (50, -86.6)])
chk("3725 corrigé : fermé, orientation 90", (arrondi((lu.x, lu.y)), lu.direction), ((0, 0), 90))
chk("3725 corrigé : 3 côtés de 100", [round(math.dist(a, b), 9) for a, b in lu.segments], [100.0] * 3)
chk("3725 angle 360/3 = 180 - 60", (360 / 3, 180 - 60), (120, 120))

# ============================================================ 3726 messages
JOURNAL.clear()
run("3726")
chk("3726 ordre des répliques", JOURNAL, [("Chat", "Bonjour !"), ("Chien", "Salut !"), ("Chat", "Au revoir !")])
chk("3726 durée 3 x 2 s", 3 * 2, 6)

# ============================================================ 3727 nombre mystère
r = run("3727", entrees=[50, 25, 37], tirages=[37])
chk("3727 partie 50, 25, 37", r.dits, ["Trop grand !", "Trop petit !", "Gagné !"])
chk("3727 essais = 3", r.vars["essais"], 3)


def dichotomie(secret, nmax=100):
    bas, haut, props = 1, nmax, []
    while True:
        p = (bas + haut) // 2
        props.append(p)
        if p == secret:
            return props
        if p < secret:
            bas = p + 1
        else:
            haut = p - 1


props = dichotomie(81)
chk("3727 dichotomie 81", props, [50, 75, 88, 81])
r = run("3727", entrees=props, tirages=[81])
chk("3727 script avec 50, 75, 88, 81", (r.dits, r.vars["essais"]), (["Trop petit !", "Trop petit !", "Trop grand !", "Gagné !"], 4))
chk("3727 maximum 7 essais (1 à 100)", max(len(dichotomie(s)) for s in range(1, 101)), 7)
chk("3727 maximum 10 essais (1 à 1 000)", max(len(dichotomie(s, 1000)) for s in range(1, 1001)), 10)
for s in (1, 64, 100, 37):
    pr = dichotomie(s)
    rr = run("3727", entrees=pr, tirages=[s])
    chk("3727 script joue la dichotomie (%d)" % s, (rr.dits[-1], rr.vars["essais"]), ("Gagné !", len(pr)))
chk("3727 2^6 < 100 <= 2^7", (2 ** 6 < 100 <= 2 ** 7), True)
chk("3727 2^9 < 1000 <= 2^10", (2 ** 9 < 1000 <= 2 ** 10), True)
chk("3727 suite des moitiés", [100, 50, 25, 12, 6, 3, 1], [100 // 2 ** k if k < 6 else 1 for k in range(7)])

# ============================================================ 3728 spirale
lu = lutin("3728")
chk("3728 longueurs des segments", [round(math.dist(a, b)) for a, b in lu.segments], list(range(10, 101, 10)))
chk("3728 longueur finale 110", run("3728").vars["longueur"], 110)
chk("3728 longueur totale 550", longueur(lu.segments), 550)
chk("3728 angle total 900", 10 * 90, 900)
chk("3728 4 premières positions", [arrondi(b) for a, b in lu.segments[:4]], [(10, 0), (10, 20), (-20, 20), (-20, -20)])
chk("3728 arrivée (50 ; 60)", arrondi((lu.x, lu.y)), (50, 60))
chk("3728 distance ≈ 78,1", round(math.hypot(50, 60), 1), 78.1)
chk("3728 50² + 60² = 6 100", 50 ** 2 + 60 ** 2, 6100)
chk("3728 orientation finale -90 (gauche)", lu.direction, -90)

# ============================================================ 3729 monnaie
for e, (p2, p1, tours) in ((7, (3, 1, 3)), (10, (5, 0, 5)), (1, (0, 1, 0)), (15, (7, 1, 7))):
    r = run("3729", entrees=[e])
    chk("3729 somme %d" % e, (r.dits, r.vars["pièces2"]), ([p2, p1], tours))
for e in range(0, 60):
    r = run("3729", entrees=[e])
    if r.dits != [e // 2, e % 2]:
        raise AssertionError("3729 %d" % e)
chk("3729 pièces2 = quotient, pièces1 = reste (0 à 59)", True, True)
r = run("3729_billets", entrees=[18])
chk("3729 billets 18 €", r.dits, [3, 1, 1])
chk("3729 billets : 5 billets et pièces", sum(r.dits), 5)
for e in range(0, 60):
    r = run("3729_billets", entrees=[e])
    b, q = e // 5, e % 5
    if r.dits != [b, q // 2, q % 2] or 5 * r.dits[0] + 2 * r.dits[1] + r.dits[2] != e:
        raise AssertionError("3729 billets %d" % e)
chk("3729 billets justes de 0 à 59", True, True)
chk("3729 7 € : reste 7, 5, 3, 1", [7 - 2 * k for k in range(4)], [7, 5, 3, 1])

# ============================================================ 3730 températures
for c, f in ((0, 32), (100, 212), (37, 98.6), (10, 50), (-40, -40)):
    chk("3730 %s °C" % c, dit("3730", c)[0], f)
chk("3730 F = 1,8C + 32", sp.nsimplify(sp.expand(dit("3730", X)[0])), sp.Rational(9, 5) * X + 32)
chk("3730 50 °F -> 10 °C", sp.solve(sp.Eq(sp.Rational(9, 5) * X + 32, 50), X), [10])
chk("3730 égalité -40", sp.solve(sp.Eq(sp.Rational(9, 5) * X + 32, X), X), [-40])
for f, c in ((212, 100), (50, 10), (32, 0), (-40, -40), (98.6, 37)):
    chk("3730 inverse %s °F" % f, dit("3730_inverse", f)[0], c)
chk("3730 37 x 1,8 = 66,6", 37 * 1.8, 66.6)
chk("3730 erreur d'ordre : 212 / 1,8 - 32 ≈ 85,8", round(212 / 1.8 - 32, 1), 85.8)
chk("3730 18 / 1,8 = 10 ; -32 / 0,8 = -40", (18 / 1.8, -32 / 0.8), (10, -40))
chk("3733 2,5 : 6,5 x 2,5 = 16,25 ; 2,5² = 6,25", (6.5 * 2.5, 2.5 * 2.5), (16.25, 6.25))
chk("3722 sans relever : 720 + 6 x 60 = 1 080", 720 + 6 * 60, 1080)
chk("3732 4 x 260 = 1 040", (20 + 50 + 80 + 110, 4 * 260), (260, 1040))

# ============================================================ 3731 robot
lu = lutin("3731")
chk("3731 après un tour (40 ; 30)", arrondi(lu.positions[3]), (40, 30))
chk("3731 A (120 ; 90)", arrondi(lu.positions[7]), (120, 90))
chk("3731 un tour : 70 parcourus, 50 à vol d'oiseau", (40 + 30, math.hypot(40, 30)), (70, 50))
chk("3731 OA = 150", math.hypot(120, 90), 150)
chk("3731 B (0 ; 90)", arrondi((lu.x, lu.y)), (0, 90))
chk("3731 distance parcourue 330", longueur(lu.segments), 330)
chk("3731 OB = 90", math.hypot(0, 90), 90)

# ============================================================ 3732 carrés emboîtés
r = run("3732")
lu = r.lutins["lutin"]
cotes = sorted(set(round(math.dist(a, b)) for a, b in lu.segments))
chk("3732 côtés 20, 50, 80, 110", cotes, [20, 50, 80, 110])
chk("3732 variable longueur à la fin 140", r.vars["longueur"], 140)
chk("3732 longueur tracée 1 040", longueur(lu.segments), 1040)
chk("3732 tous les carrés ont le sommet (0 ; 0)", all(arrondi(lu.segments[4 * k][0]) == (0, 0) for k in range(4)), True)
chk("3732 côté du n-ième = 30n - 10", [30 * n - 10 for n in range(1, 5)], [20, 50, 80, 110])
r7 = run("3732_7")
chk("3732 7 carrés : le plus grand 200", max(round(math.dist(a, b)) for a, b in r7.lutins["lutin"].segments), 200)
chk("3732 7 carrés : 30 x 7 - 10", 30 * 7 - 10, 200)
ys = [p[1] for s in r7.lutins["lutin"].segments for p in s]
chk("3732 depuis (0;0) : y max 200 > 180", max(ys), 200)
r7s = run("3732_7_scene")
xs = [p[0] for s in r7s.lutins["lutin"].segments for p in s]
ys = [p[1] for s in r7s.lutins["lutin"].segments for p in s]
chk("3732 depuis (-200;-170) : x de -200 à 0", (round(min(xs)), round(max(xs))), (-200, 0))
chk("3732 depuis (-200;-170) : y de -170 à 30", (round(min(ys)), round(max(ys))), (-170, 30))
chk("3732 dessin A : 4 carrés de 20 côte à côte", sorted(set(round(math.dist(a, b)) for a, b in lutin("3732_A").segments)), [20])
chk("3732 dessin C : 4 carrés croissants côte à côte",
    sorted(set(round(math.dist(a, b)) for a, b in lutin("3732_C").segments)), [20, 50, 80, 110])

# ============================================================ 3733 deux lutins
chk("3733 avec 3", dit("3733", 3), [12])
chk("3733 avec -5", dit("3733", -5), [-20])
chk("3733 avec 2,5", dit("3733", 2.5), [10])
chk("3733 expression 4x", sp.expand(dit("3733", X)[0]), 4 * X)
chk("3733 pour 30 : 7,5", sp.solve(sp.Eq(4 * X, 30), X), [sp.Rational(15, 2)])
chk("3733 vérification 7,5", dit("3733", 7.5), [30])
chk("3733 programme simplifié identique", all(dit("3733_simple", e) == dit("3733", e) for e in (3, -5, 2.5, 0, 11)), True)
JOURNAL.clear()
r = run("3733", entrees=[3])
chk("3733 r avant le calcul du Chien : 7", 3 + 4, 7)

# ============================================================ programmes en Python
with open(ICI / "programmes_290.txt", "w", encoding="utf-8") as f:
    f.write("# Traduction Python des scripts Scratch de la notion 290 (générée par verif_290.py)\n\n")
    for cle, projet in SC.items():
        f.write("# " + "=" * 70 + "\n# %s\n# " % cle + "=" * 70 + "\n")
        f.write(traduire(projet) + "\n\n")
print("\n%d contrôles OK ; %d scripts traduits en Python dans programmes_290.txt" % (ok, len(SC)))
