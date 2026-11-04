# -*- coding: utf-8 -*-
"""Vérification de la notion 280 « Penser et programmer par blocs » (5e).

Chaque script Scratch du cours, de la fiche et des exercices (figures/figures.py, dictionnaire
SCRIPTS) est TRADUIT EN PYTHON (figures/scratch.py, fonction traduire) puis EXÉCUTÉ : toutes
les valeurs annoncées (nombres dits, positions, orientations, longueurs tracées, tableaux
d'exécution) sont contrôlées. Les expressions des programmes de calcul sont vérifiées avec
sympy en exécutant le script avec une entrée symbolique. La traduction Python de tous les
scripts est écrite dans programmes_280.txt. Contrôles de structure des textes à la fin.

    python verif_280.py
"""
import math
import re
import sys
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI / "figures"))
import figures as FG          # noqa: E402
from scratch import *         # noqa: E402,F401,F403

SC = FG.SCRIPTS
ok = 0
x = sp.Symbol("x")


def chk(nom, val, attendu, tol=1e-6):
    global ok
    if isinstance(attendu, sp.Basic) and not isinstance(attendu, sp.Number):
        bon = sp.simplify(sp.sympify(val) - attendu) == 0
    elif isinstance(attendu, (int, float)) and not isinstance(attendu, bool) and isinstance(val, (int, float, sp.Basic)):
        bon = abs(float(val) - attendu) <= tol
    else:
        bon = val == attendu
    if not bon:
        raise AssertionError("%s : obtenu %r, attendu %r" % (nom, val, attendu))
    ok += 1
    print("OK %-60s %s" % (nom, val if not isinstance(val, float) else round(val, 6)))


def run(projet, **kw):
    return executer(SC[projet] if isinstance(projet, str) else projet, **kw)


def dit(cle, *entrees, **kw):
    return run(cle, entrees=list(entrees), **kw).dits


def lutin(cle, **kw):
    return run(cle, **kw).lutins["lutin"]


def longueur(segs):
    return sum(math.dist(a, b) for a, b in segs)


def P(p, k=6):
    return tuple(round(c, k) + 0.0 for c in p)


def etats(script, debut, entrees=()):
    """(position, orientation) après chaque bloc du script, à partir du bloc n° debut."""
    out = []
    for k in range(debut, len(script) + 1):
        lu = executer({"Lutin": [script[:k]]}, entrees=list(entrees)).lutins["lutin"]
        out.append((P((lu.x, lu.y)), lu.direction))
    return out


def var_apres(script, var, debut, entrees=()):
    """Valeur de var après chaque bloc (scripts sans boucle)."""
    out = []
    for k in range(debut, len(script) + 1):
        r = executer({"Lutin": [script[:k] + [Dire(V(var))]]}, entrees=list(entrees))
        out.append(r.dits[-1])
    return out


def sommets_ferme(lu):
    return [P(a) for a, b in lu.segments]


# ======================================================================== traductions
with open(ICI / "programmes_280.txt", "w", encoding="utf-8") as fh:
    fh.write("# Traduction Python des scripts Scratch de la notion 280 (générée par verif_280.py)\n")
    for cle, projet in SC.items():
        fh.write("\n# " + "=" * 70 + "\n# %s\n# " % cle + "=" * 70 + "\n")
        fh.write(traduire(projet) + "\n")
print("Traductions écrites dans programmes_280.txt (%d scripts)" % len(SC))

# ======================================================================== cours
chk("cours calcul : 7 -> 24", dit("cours_calcul", 7), [24])
chk("cours calcul : tableau (nombre)", var_apres(SC["cours_calcul"]["Lutin"][0][:5], "nombre", 3, [7]), [7, 7, 7])
chk("cours calcul : tableau (résultat)", var_apres(SC["cours_calcul"]["Lutin"][0][:5], "résultat", 4, [7]), [12, 24])
chk("cours calcul : expression (x + 5) * 2", dit("cours_calcul", x)[0], (x + 5) * 2)
for n, b1, b2 in ((6, 13, 14),):
    r1 = executer({"Lutin": [[Drapeau(), Mettre("n", n), Dire(Op(Op(V("n"), "*", 2), "+", 1))]]}).dits[0]
    r2 = executer({"Lutin": [[Drapeau(), Mettre("n", n), Dire(Op(Op(V("n"), "+", 1), "*", 2))]]}).dits[0]
    chk("cours blocs emboîtés : bloc 1 pour n = 6", r1, b1)
    chk("cours blocs emboîtés : bloc 2 pour n = 6", r2, b2)
sL = SC["cours_L"]["Lutin"][0]
e = etats(sL, 3)
chk("cours L : tableau position / orientation", [e[0][0], e[1], e[3], e[4], e[5]],
    [(0.0, 80.0), ((0.0, 80.0), 180.0), ((0.0, 0.0), 180.0), ((0.0, 0.0), 90.0), ((40.0, 0.0), 90.0)])
lu = lutin("cours_L")
chk("cours L : deux segments de 80 et 40", [round(math.dist(a, b), 6) for a, b in lu.segments], [80.0, 40.0])


def carre_tours(cote, droite, n=4):
    tours = []
    for k in range(1, n + 1):
        t = TournerD(90) if droite else TournerG(90)
        lu = executer({"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                                  Repeter(k - 1, [Avancer(cote), t]), Avancer(cote)]]}).lutins["lutin"]
        pos = P((lu.x, lu.y))
        lu2 = executer({"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                                   Repeter(k, [Avancer(cote), t])]]}).lutins["lutin"]
        tours.append((pos, lu2.direction))
    return tours


chk("cours carré : tableau des tours", carre_tours(60, False),
    [((60.0, 0.0), 0.0), ((60.0, 60.0), -90.0), ((0.0, 60.0), 180.0), ((0.0, 0.0), 90.0)])
lu = lutin("cours_carre")
chk("cours carré : 4 segments de 60, retour au départ vers la droite",
    ([round(math.dist(a, b), 6) for a, b in lu.segments], P((lu.x, lu.y)), lu.direction), ([60.0] * 4, (0.0, 0.0), 90.0))
chk("cours carré : 2 blocs de mouvement dans la boucle, 8 sans boucle", 2 * 4, 8)
chk("cours polygone : 360/4 et 360/3", (360 / 4, 360 / 3), (90.0, 120.0))
chk("cours angle : 180 - 60", 180 - 60, 120)
chk("cours si : réponse 72", dit("cours_si", 72), ["Niveau réussi !", "Fin de la partie"])
chk("cours si : réponse 50 (frontière)", dit("cours_si", 50), ["Fin de la partie"])
chk("cours si : 50 > 49 vrai (correction proposée)", 50 > 49, True)
xs = []
for k in range(1, 5):
    seq = ["flèche droite", "flèche droite", "flèche gauche", "flèche droite"][:k]
    xs.append(run("cours_touches", touches=seq).lutins["lutin"].x)
chk("cours touches : abscisses 10, 20, 10, 20", xs, [10, 20, 10, 20])

# fiche : tableau d'exécution (réponse 3)
fiche = [Drapeau(), Demander("?"), Mettre("n", Reponse()), Mettre("r", Op(V("n"), "*", 4)), Ajouter("r", 1)]
chk("fiche : r après chaque bloc", var_apres(fiche, "r", 4, [3]), [12, 13])
chk("fiche : expression 4n + 1", executer({"Lutin": [fiche + [Dire(V("r"))]]}, entrees=[x]).dits[0], 4 * x + 1)
chk("fiche : polygones (carré, triangle, hexagone)", (360 / 4, 360 / 3, 360 / 6), (90.0, 120.0, 60.0))

# ======================================================================== 3104
s = SC["3104"]["Lutin"][0]
chk("3104 Q2 : tableau (résultat) pour 5", var_apres(s[:5], "résultat", 4, [5]), [20, 26])
chk("3104 Q2 : 5 -> 26", dit("3104", 5), [26])
chk("3104 Q3 : 2,5 -> 16", dit("3104", 2.5), [16])
chk("3104 Q3 : 0 -> 6", dit("3104", 0), [6])
chk("3104 Q4 : expression 4x + 6", dit("3104", x)[0], 4 * x + 6)
sol = sp.solve(sp.Eq(dit("3104", x)[0], 50), x)
chk("3104 Q5 : 4x + 6 = 50", sol, [11])
chk("3104 Q5 : 44 et 44 / 4", (50 - 6, (50 - 6) / 4), (44, 11.0))
chk("3104 Q5 : vérification 11 -> 50", dit("3104", 11), [50])
for v in (5, 2.5, 0, 11, -3, x):
    chk("3104 Q6 : « mettre résultat à résultat + 6 » équivalent (%s)" % v, dit("3104_mettre", v)[0], dit("3104", v)[0])
chk("3104 erreur : « mettre résultat à 6 » dit toujours 6", [dit("3104_faux", v)[0] for v in (5, 2.5, 0)], [6, 6, 6])

# ======================================================================== 3105
chk("3105 Q3 : tableau des tours", carre_tours(50, True),
    [((50.0, 0.0), 180.0), ((50.0, -50.0), -90.0), ((0.0, -50.0), 0.0), ((0.0, 0.0), 90.0)])
lu = lutin("3105")
chk("3105 Q2 : 4 segments", len(lu.segments), 4)
chk("3105 Q3 : sommets", sommets_ferme(lu), [(0.0, 0.0), (50.0, 0.0), (50.0, -50.0), (0.0, -50.0)])
chk("3105 Q3 : retour au départ vers la droite", (P((lu.x, lu.y)), lu.direction), ((0.0, 0.0), 90.0))
chk("3105 Q4 : longueur tracée", longueur(lu.segments), 200)
chk("3105 Q5 : 8 blocs sans boucle", 4 * 2, 8)
lu = lutin("3105_sans_stylo")
chk("3105 Q6 : sans stylo, rien n'est tracé", (len(lu.segments), P((lu.x, lu.y)), lu.direction), (0, (0.0, 0.0), 90.0))

# ======================================================================== 3110
s = SC["3110"]["Lutin"][0]
e = etats(s, 6)
chk("3110 Q1 : (80 ; 0) puis orientation 0", (e[0], e[1][1]), (((80.0, 0.0), 90.0), 0.0))
chk("3110 Q3 : tableau des 7 blocs", e,
    [((80.0, 0.0), 90.0), ((80.0, 0.0), 0.0), ((80.0, 40.0), 0.0), ((80.0, 40.0), -90.0),
     ((0.0, 40.0), -90.0), ((0.0, 40.0), 180.0), ((0.0, 0.0), 180.0)])
lu = lutin("3110")
chk("3110 Q3 : sommets", sommets_ferme(lu), [(0.0, 0.0), (80.0, 0.0), (80.0, 40.0), (0.0, 40.0)])
chk("3110 Q4 : longueur 240, orientation finale 180", (longueur(lu.segments), lu.direction), (240.0, 180.0))
chk("3110 Q2 : solutions des trous", [t.sol.v for b in s for t in b.items if isinstance(t, Trou)], [40, 90, 80, 40])
lb = lutin("3110_boucle")
chk("3110 Q5 : la boucle trace le même rectangle", sommets_ferme(lb), sommets_ferme(lu))
chk("3110 Q5 : avec la boucle, le lutin finit vers la droite", lb.direction, 90.0)

# ======================================================================== 3108
chk("3108 Q1 : Léa, 2 -> 11", dit("3108_lea", 2), [11])
chk("3108 Q1 : Tom, 2 -> 20", dit("3108_tom", 2), [20])
chk("3108 Q2 : Léa (n * 4) + 3", dit("3108_lea", x)[0], x * 4 + 3)
chk("3108 Q2 : Tom 4 * (n + 3)", dit("3108_tom", x)[0], 4 * (x + 3))
chk("3108 Q3 : le script de Tom corrigé = celui de Léa", sp.expand(dit("3108_tom_corrige", x)[0] - dit("3108_lea", x)[0]), 0)
chk("3108 Q4 : développement 4(n + 3) = 4n + 12", sp.expand(4 * (x + 3)), 4 * x + 12)
chk("3108 Q4 : Tom - Léa = 9", sp.expand(dit("3108_tom", x)[0] - dit("3108_lea", x)[0]), 9)
for v in range(-5, 21):
    if dit("3108_tom", v)[0] - dit("3108_lea", v)[0] != 9:
        raise AssertionError("3108 écart différent de 9 pour %d" % v)
ok += 1
print("OK 3108 Q4 : écart de 9 vérifié de -5 à 20 par exécution")
chk("3108 Q5 : (n + 5) * 2", dit("3108_trou", x)[0], (x + 5) * 2)
chk("3108 Q5 : 4 -> 18", dit("3108_trou", 4), [18])

# ======================================================================== 3117
tot = [60 * k for k in range(1, 4)]
chk("3117 Q1 : rotations totales 60, 120, 180", tot, [60, 120, 180])
lu = lutin("3117")
chk("3117 Q1 : 3 segments, tracé non fermé", (len(lu.segments), P((lu.x, lu.y)) != (0.0, 0.0)), (3, True))
chk("3117 Q1 : à la fin, le lutin regarde vers la gauche", lu.direction, -90.0)
chk("3117 Q2 : 360 / 3", 360 / 3, 120.0)
chk("3117 Q2 : 60 + 120 = 180", 60 + 120, 180)
lu = lutin("3117_triangle")
cotes = [round(math.dist(a, b), 6) for a, b in lu.segments]
chk("3117 Q3 : triangle fermé, 3 côtés de 80", (cotes, P((lu.x, lu.y)), lu.direction), ([80.0] * 3, (0.0, 0.0), 90.0))
pts = sommets_ferme(lu)
chk("3117 Q3 : triangle équilatéral (3 côtés égaux)", len(set(round(math.dist(pts[i], pts[(i + 1) % 3]), 6) for i in range(3))), 1)
dirs = []
for k in range(1, 4):
    l2 = executer({"Lutin": [[Drapeau(), AllerA(0, 0), Orienter(90), Repeter(k, [Avancer(80), TournerG(120)])]]}).lutins["lutin"]
    dirs.append(l2.direction)
chk("3117 Q3 : orientations après chaque tour (haut à gauche, bas à gauche, droite)", dirs, [-30.0, -150.0, 90.0])
s = SC["3117_hexagone"]["Lutin"][0]
chk("3117 Q4 : trous A = 6, B = 60", [s[-1].items[1].sol.v, s[-1].branches[0][1][1].items[3].sol.v], [6, 60])
lu = lutin("3117_hexagone")
chk("3117 Q4 : hexagone fermé, 6 côtés de 50", ([round(math.dist(a, b), 6) for a, b in lu.segments], P((lu.x, lu.y)), lu.direction),
    ([50.0] * 6, (0.0, 0.0), 90.0))
chk("3117 Q5 : longueur 300", longueur(lu.segments), 300)
chk("3117 erreur : angle intérieur de l'hexagone 120", (6 - 2) * 180 / 6, 120.0)

# ======================================================================== 3106
chk("3106 Q1 : 10 ans -> 6", dit("3106", 10), [6])
chk("3106 Q1 : tableau (prix) pour 10", var_apres(SC["3106"]["Lutin"][0][:3], "prix", 3, [10]) +
    [executer({"Lutin": [SC["3106"]["Lutin"][0][:4] + [Dire(V("prix"))]]}, entrees=[10]).dits[-1]], [9, 6])
chk("3106 Q2 : 15 ans -> 9", dit("3106", 15), [9])
chk("3106 Q3 : 12 ans -> 9 (12 < 12 faux)", dit("3106", 12), [9])
chk("3106 Q4 : seuil 13 : 12 ans -> 6, 13 ans -> 9", (dit("3106_13", 12), dit("3106_13", 13)), ([6], [9]))
fam = [dit("3106_senior", a)[0] for a in (8, 12, 40, 70)]
chk("3106 Q6 : prix de la famille", fam, [6, 6, 9, 7])
chk("3106 Q6 : total 28", sum(fam), 28)
chk("3106 Q5 : frontières 64 -> 9, 65 -> 7", (dit("3106_senior", 64), dit("3106_senior", 65)), ([9], [7]))
# bloc senior placé APRÈS « dire prix » : le prix dit serait faux
mauvais = SC["3106_13"]["Lutin"][0] + [Si(Cmp(Reponse(), ">", 64), [Mettre("prix", 7)])]
chk("3106 Q5 : bloc placé après « dire » : 70 ans -> 9 (trop tard)", executer({"Lutin": [mauvais]}, entrees=[70]).dits, [9])

# ======================================================================== 3114
r = run("3114", touches=FG.SEQUENCE_3114)
lu = r.lutins["lutin"]
pos = []
dirs = []
for k in range(1, 7):
    l2 = run("3114", touches=FG.SEQUENCE_3114[:k]).lutins["lutin"]
    pos.append(P((l2.x, l2.y)))
    dirs.append(l2.direction)
chk("3114 Q2 : positions", pos, [(20.0, 0.0), (40.0, 0.0), (40.0, 20.0), (40.0, 40.0), (40.0, 60.0), (20.0, 60.0)])
chk("3114 Q2 : orientations", dirs, [90.0, 90.0, 0.0, 0.0, 0.0, -90.0])
chk("3114 Q3 : longueur 120", longueur(lu.segments), 120)
chk("3114 Q4 : nombre minimal d'appuis", int(abs(lu.x) / 20 + abs(lu.y) / 20), 4)
l3 = run("3114", touches=FG.SEQUENCE_3114 + FG.RETOUR_3114).lutins["lutin"]
chk("3114 Q4 : retour en (0 ; 0), tourné vers le bas", (P((l3.x, l3.y)), l3.direction), ((0.0, 0.0), 180.0))
proj = {"Lutin": SC["3114"]["Lutin"] + SC["3114_espace"]["Lutin"]}
l4 = executer(proj, touches=["flèche droite", "espace", "flèche haut"]).lutins["lutin"]
chk("3114 Q5 : après espace, le déplacement n'est plus tracé", (len(l4.segments), P((l4.x, l4.y))), (1, (20.0, 20.0)))

# ======================================================================== 3122
s = SC["3122"]["Lutin"][0]
premier = s[:5] + s[5].branches[0][1]
chk("3122 Q1 : premier tour pas à pas", etats(premier, 6),
    [((30.0, 0.0), 90.0), ((30.0, 0.0), 0.0), ((30.0, 20.0), 0.0), ((30.0, 20.0), 90.0)])
fins = []
for k in range(1, 5):
    l2 = executer({"Lutin": [s[:5] + [Repeter(k, s[5].branches[0][1])]]}).lutins["lutin"]
    fins.append(P((l2.x, l2.y)))
chk("3122 Q2 : fins de tours", fins, [(30.0, 20.0), (60.0, 40.0), (90.0, 60.0), (120.0, 80.0)])
lu = lutin("3122")
chk("3122 Q3 : longueur 200", longueur(lu.segments), 200)
l7 = lutin("3122_7")
chk("3122 Q4 : 7 marches, arrivée (210 ; 140)", P((l7.x, l7.y)), (210.0, 140.0))
chk("3122 Q4 : 140 / 20", 140 / 20, 7.0)


def dans_scene(lu):
    return all(-240 <= px <= 240 and -180 <= py <= 180 for (px, py) in lu.positions)


l8 = executer({"Lutin": [s[:5] + [Repeter(8, s[5].branches[0][1])]]}).lutins["lutin"]
l9 = executer({"Lutin": [s[:5] + [Repeter(9, s[5].branches[0][1])]]}).lutins["lutin"]
chk("3122 Q4 : 8 marches -> (240 ; 160), sur la scène", (P((l8.x, l8.y)), dans_scene(l8)), ((240.0, 160.0), True))
chk("3122 Q4 : 9 marches -> (270 ; 180), hors de la scène", (P((l9.x, l9.y)), dans_scene(l9)), ((270.0, 180.0), False))
sg = SC["3122_gauche"]["Lutin"][0]
deux = sg[:5] + sg[5].branches[0][1] * 2
chk("3122 Q5 : tableau des deux premiers tours", etats(deux, 6),
    [((30.0, 0.0), 90.0), ((30.0, 0.0), 0.0), ((30.0, 20.0), 0.0), ((30.0, 20.0), -90.0),
     ((0.0, 20.0), -90.0), ((0.0, 20.0), 180.0), ((0.0, 0.0), 180.0), ((0.0, 0.0), 90.0)])
lg = lutin("3122_gauche")
chk("3122 Q5 : rectangle 30 × 20 parcouru deux fois",
    (sommets_ferme(lg)[:4], sommets_ferme(lg)[4:], P((lg.x, lg.y)), lg.direction),
    ([(0.0, 0.0), (30.0, 0.0), (30.0, 20.0), (0.0, 20.0)], [(0.0, 0.0), (30.0, 0.0), (30.0, 20.0), (0.0, 20.0)],
     (0.0, 0.0), 90.0))

# ======================================================================== 3115
s = SC["3115"]["Lutin"][0]
vals = []
for k in range(0, 9):
    rr = executer({"Lutin": [s[:3] + [Repeter(k, s[3].branches[0][1]), Dire(V("semaine")), Dire(V("tirelire"))]]})
    vals.append(tuple(rr.dits))
chk("3115 Q1 : tableau de la boucle", vals, [(k, 30 + 15 * k) for k in range(9)])
chk("3115 Q2 : le lutin dit seulement 150", dit("3115"), [150])
chk("3115 Q2 : condition « > 149 »", dit("3115_149"), [150, "Objectif atteint !"])
chk("3115 Q3 : formule 30 + 15n (0 à 8)", [30 + 15 * k for k in range(9)], [v[1] for v in vals])
chk("3115 Q4 : 11 semaines -> 195, 12 -> 210", (30 + 15 * 11, 30 + 15 * 12), (195, 210))
n_min = next(n for n in range(100) if 30 + 15 * n >= 200)
chk("3115 Q4 : premier n tel que 30 + 15n >= 200", n_min, 12)
chk("3115 Q4 : script modifié", dit("3115_velo"), [210, "Objectif atteint !"])
avec11 = FG.s3115(n=11, seuil=199, corr=True)
chk("3115 Q4 : avec 11 tours, pas d'objectif", executer(avec11).dits, [195])
chk("3115 erreur : 200 - 30 = 170 ; 170 / 15", (200 - 30, round(170 / 15, 1)), (170, 11.3))

# ======================================================================== 3124
s = SC["3124"]["Lutin"][0]
chk("3124 Q1 : 12 et 8 -> 40", dit("3124", 12, 8), [40])
chk("3124 Q1 : tableau (clôture)", var_apres(s[:8], "clôture", 7, [12, 8]), [20, 40])
chk("3124 Q1 : périmètre 2(L + l)", executer({"Lutin": [s[:9]]}, entrees=[x, sp.Symbol("l")]).dits[0], 2 * (x + sp.Symbol("l")))
lu = run("3124", entrees=[12, 8]).lutins["lutin"]
chk("3124 Q2 : sommets", sommets_ferme(lu), [(0.0, 0.0), (120.0, 0.0), (120.0, 80.0), (0.0, 80.0)])
chk("3124 Q2 : retour vers la droite", (P((lu.x, lu.y)), lu.direction), ((0.0, 0.0), 90.0))
b = s[:-1] + [s[-1].branches[0][1][0], s[-1].branches[0][1][1], s[-1].branches[0][1][2], s[-1].branches[0][1][3]]
chk("3124 Q2 : premier tour pas à pas", etats(b, len(s), [12, 8]),
    [((120.0, 0.0), 90.0), ((120.0, 0.0), 0.0), ((120.0, 80.0), 0.0), ((120.0, 80.0), -90.0)])
chk("3124 Q3 : budget", dit("3124_budget", 12, 8), [40, "Budget dépassé !"])
chk("3124 Q3 : prix 160", 40 * 4, 160)
chk("3124 Q4 : 15 et 3 -> 36, sans message", dit("3124_budget", 15, 3), [36])
chk("3124 Q4 : prix 144", 36 * 4, 144)
l2 = run("3124", entrees=[15, 3]).lutins["lutin"]
chk("3124 Q4 : rectangle 150 × 30", sommets_ferme(l2), [(0.0, 0.0), (150.0, 0.0), (150.0, 30.0), (0.0, 30.0)])
chk("3124 erreur : aire 12 × 8", 12 * 8, 96)

# ======================================================================== structure des textes
txt = (ICI / "exercices.txt").read_text(encoding="utf-8")
blocs = [b for b in re.split(r"^===[ \t]*$", txt, flags=re.M) if b.strip()]
chk("structure : 10 exercices", len(blocs), 10)
types = [b.strip().splitlines()[0].replace("===", "").strip().split(" - ")[0] for b in blocs]
chk("structure : progression", types, ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 2 + ["Synthèse"] * 2)
for b in blocs:
    titre = b.strip().splitlines()[0]
    en = b[b.index("Énoncé:"):b.index("Étapes:")]
    et = b[b.index("Étapes:"):b.index("Solution:")]
    so = b[b.index("Solution:"):]
    nq = len(re.findall(r"^\d+\. ", en, re.M))
    nqe = len(re.findall(r"^## Question \d+", et, re.M))
    nso = len(re.findall(r"^\d+\. ", so, re.M))
    if not (nq == nqe == nso):
        raise AssertionError("%s : questions %d / étapes %d / solutions %d" % (titre, nq, nqe, nso))
    sections = re.split(r"^## Question \d+", et, flags=re.M)[1:]
    if any("::: resultat" not in sct for sct in sections):
        raise AssertionError("%s : une question sans résultat" % titre)
    if "::: methode" not in et or ("::: attention" not in et and "::: retenir" not in et):
        raise AssertionError("%s : méthode ou erreur fréquente absente" % titre)
    if "|---|" not in et:
        raise AssertionError("%s : pas de tableau d'exécution" % titre)
    ok += 1
    print("OK structure %-50s %d questions" % (titre[4:54], nq))
for f in ("cours_275.txt", "fiche_195.txt", "exercices.txt"):
    t = (ICI / f).read_text(encoding="utf-8")
    chk("aucune mention du brevet dans %s" % f, "brevet" in t.lower(), False)
ids = re.findall(r"^Id:\s*(\d+)", txt, re.M)
ret = [l.split()[0] for l in (ICI / "exercices_retires.txt").read_text(encoding="utf-8").splitlines()
       if l.strip() and not l.startswith("#")]
chk("10 gardés + 11 retirés = 21 exercices en ligne, sans recouvrement",
    (len(set(ids) | set(ret)), len(set(ids) & set(ret))), (21, 0))

print("\n%d contrôles OK, 0 erreur" % ok)
