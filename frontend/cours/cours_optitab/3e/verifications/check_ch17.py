# -*- coding: utf-8 -*-
"""Contrôles du chapitre 17 (Algorithmique) : les scripts des figures sont EXÉCUTÉS."""
import copy
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "graphe"))
import scratch3e as S                     # noqa: E402
from scratch3e import V, op, cmp          # noqa: E402
from scripts_ch17 import SCRIPTS          # noqa: E402


def prog(nom):
    return copy.deepcopy(SCRIPTS[nom][0])


def out(nom, inputs=(), p=None, seed=0):
    return S.run(p if p is not None else prog(nom), inputs, seed=seed)["out"]


def remplace(blocks, old, new):
    """Remplace récursivement un bloc par un autre dans une liste de blocs."""
    res = []
    for b in blocks:
        if b == old:
            res.append(new)
        elif b[0] in ("repeat", "until", "if"):
            res.append((b[0], b[1], remplace(b[2], old, new)))
        elif b[0] == "ifelse":
            res.append((b[0], b[1], remplace(b[2], old, new), remplace(b[3], old, new)))
        else:
            res.append(b)
    return res


def infinie(p):
    try:
        S.run(p, max_steps=20000)
    except S.Stop:
        return True
    return False


def longueur(res):
    return sum(math.dist(a, b) for a, b in res["segs"])


# Cours
assert out("cours_test", ["17"]) == ["Tu es mineur."] and out("cours_test", ["18"]) == ["Tu es majeur."]
c = SCRIPTS["cours_boucles"][0]
assert S.run([c[0]])["out"] == [10] and S.run([c[1]])["out"] == [243]
r = S.run(prog("cours_bloc"))
assert {p for s in r["segs"] for p in s} == {(0, 0), (50, 0), (50, 50), (0, 50)}

# Découverte
assert out("trois_operations") == [16]                                               # D1
p = prog("trois_operations")
p[0][2], p[0][3] = p[0][3], p[0][2]
assert out(None, p=p) == [11]                                                        # D1 Q3
p = prog("trois_operations"); p[0][1] = ("set", "x", 10)
assert out(None, p=p) == [30]                                                        # D1 Q5
assert [out("nombre_demande", [v]) for v in ["2", "-4", "0,5", "6"]] == [[18], [0], [13.5], [30]]  # D2
assert out("boucle") == [12]                                                         # D3
p = prog("boucle"); p[0][2] = ("repeat", 10, p[0][2][2])
assert out(None, p=p) == [30]                                                        # D3 Q5
assert [out("test", [v]) for v in ["9", "10", "14", "9,99", "-20"]] == \
    [["petit"], ["grand"], ["grand"], ["petit"], ["petit"]]                          # D4
assert out("doubler") == [16] and 2 + 3 * 2 == 8                                     # D5
p = prog("doubler"); p[0][2] = ("repeat", 9, p[0][2][2])
assert out(None, p=p) == [1024]                                                      # D5 Q5
r = S.run(prog("carre"))
assert r["segs"][0] == ((0, 0), (40, 0)) and longueur(r) == 160 and r["pos"] == (0, 0)  # D6
assert {p for s in r["segs"] for p in s} == {(0, 0), (40, 0), (40, 40), (0, 40)}     # D6
p = prog("carre"); p[0][5] = ("repeat", 3, [("move", 40), ("left", 120)])
assert S.run(p)["pos"] == (0, 0)                                                     # D6 Q5
assert out("somme") == [15] and S.run(prog("somme"))["env"]["n"] == 6                # D7
p = prog("somme"); p[0][3] = ("repeat", 10, p[0][3][2])
assert out(None, p=p) == [55]                                                        # D7 Q5

# Entraînement
assert out("jusqua") == [24]                                                         # E1
p = [remplace(prog("jusqua")[0], ("until", cmp(">", V("x"), 20), [("change", "x", 6)]),
              ("until", cmp(">", V("x"), 20), [("change", "x", 5)]))]
assert out(None, p=p) == [25]                                                        # E1 Q4
p = [remplace(prog("jusqua")[0], ("until", cmp(">", V("x"), 20), [("change", "x", 6)]),
              ("until", cmp(">", V("x"), 20), [("change", "x", 0)]))]
assert infinie(p)                                                                    # E1 Q5
assert [out("multiple", [v]) for v in ["18", "19", "0"]] == [[1], [0], [1]]          # E2
p = prog("multiple")
p[0][4] = ("if", cmp("=", op("mod", V("x"), 2), 0), [("set", "y", 1)])
assert out(None, ["35"], p=p) == [0] and out(None, ["36"], p=p) == [1]               # E2 Q5
assert out("diviseurs") == [1, 2, 3, 4, 6, 12]                                       # E3
p = prog("diviseurs"); p[0][1] = ("set", "n", 13); p[0][3] = ("repeat", 13, p[0][3][2])
assert out(None, p=p) == [1, 13]                                                     # E3 Q5
assert out("depasse") == [64]                                                        # E4
p = prog("depasse"); p[0][2] = ("until", cmp(">", V("x"), 1000), p[0][2][2])
assert out(None, p=p) == [1024]                                                      # E4 Q4
p = prog("depasse"); p[0][2] = ("until", cmp(">", V("x"), 50), [("set", "x", op("*", V("x"), 1))])
assert infinie(p)                                                                    # E4 Q5
r = S.run(prog("carres"))
assert longueur(r) == 360 and r["pos"] == (120, 0)                                   # E5
assert sorted({s[0][0] for s in r["segs"] if s[0][1] == 0 and s[1][1] == 0}) == [0, 40, 80]  # E5
f = out("de", seed=2027)[0]
assert abs(f - 1 / 6) < 0.05 and round(1 / 6, 3) == 0.167 and 600 / 6 == 100         # E6
B = [3 * a + 5 for a in range(5)]
assert B == [5, 8, 11, 14, 17] and 3 * 1 + 0 == 3 and 3 * 10 + 5 == 35               # E7

# Problèmes
assert out("lutins") == [10]                                                         # P1
p = prog("lutins") + [copy.deepcopy(SCRIPTS["lutins"][0][1])]
assert out(None, p=p) == [20]                                                        # P1 Q5
assert [out("programme", [v]) for v in ["5", "-3", "2,5", "123"]] == [[2], [2], [2], [2]]  # P2
p = [remplace(prog("programme")[0], ("change", "r", 8), ("change", "r", 20))]
assert out(None, ["7"], p=p) == [5] and out(None, ["-1,5"], p=p) == [5]              # P2 Q5
r = S.run(prog("escalier"))
assert r["segs"][1][1] == (20, 20) and r["pos"] == (100, 100) and r["dir"] % 360 == 90  # P3
assert longueur(r) == 200                                                            # P3
p = prog("escalier")
p[0][5] = ("repeat", 8, [("move", 15), ("left", 90), ("move", 15), ("right", 90)])
assert S.run(p)["pos"] == (120, 120)                                                 # P3 Q5
r = S.run(prog("polygone"))
assert len(r["segs"]) == 6 and round(longueur(r), 6) == 180 and r["pos"] == (0, 0)   # P4
p = prog("polygone"); p[1][5] = ("call", "polygone", [3, 50])
assert S.run(p)["pos"] == (0, 0)                                                     # P4 Q3
p = prog("polygone"); p[0][1] = ("repeat", ("param", "n"), [("move", ("param", "côté")),
                                                           ("left", 108)])
p[1][5] = ("call", "polygone", [5, 50])
assert S.run(p)["pos"] != (0, 0)                                                     # P4 Q4
p = prog("polygone"); p[1][5] = ("call", "polygone", [5, 50])
assert S.run(p)["pos"] == (0, 0) and 360 / 5 == 72 == 180 - 108                      # P4 Q4
p = prog("polygone"); p[1][5] = ("call", "polygone", [36, 5])
r = S.run(p)
assert r["pos"] == (0, 0) and round(longueur(r), 6) == 180                           # P4 Q5
p = prog("devinette"); p[0][1] = ("set", "secret", 37)
assert out(None, ["50", "25", "37"], p=p) == ["Plus petit !", "Plus grand !", 3]     # P5
assert 2 ** 7 == 128 >= 100 > 2 ** 6                                                 # P5
assert 20 + 15 * 10 == 170 and math.floor(280 / 15) + 1 == 19 and 20 + 15 * 19 == 305  # P6
assert 20 + 15 * 18 == 290 < 300                                                     # P6
issues = [(a, b) for a in range(1, 7) for b in range(1, 7)]
assert len(issues) == 36 and sum(a + b == 7 for a, b in issues) == 6                 # P7
assert sum(a + b == 12 for a, b in issues) == 1 and round(1000 / 36) == 28           # P7
assert max(range(2, 13), key=lambda s: sum(a + b == s for a, b in issues)) == 7      # P7
f = out("deux_des", seed=2027)[0]
assert abs(f - 1 / 6) < 0.04                                                         # P7

print("check_ch17 : tous les contrôles passent.")
