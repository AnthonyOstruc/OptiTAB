# -*- coding: utf-8 -*-
"""Vérifications sympy du quiz « Fonction exponentielle » (notion 85).

    python verif_quiz.py

Pour chaque question : la bonne réponse est juste, chaque distracteur est faux,
la clé du quiz (bonne / bonnes / reponse / ordre) correspond au calcul, les
exemples de saisie « acceptees » / « refusees » ont la valeur attendue (lecture
sympy indépendante du correcteur du site), et les points dessinés sur les
figures sont exacts. Sortie : une ligne par contrôle, puis le bilan.
"""
import importlib.util
import re
from pathlib import Path

import sympy as sp
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application,
                                        parse_expr, standard_transformations)

ICI = Path(__file__).resolve().parent
x, n, t = sp.symbols("x n t", real=True)
E = sp.E
R = sp.S.Reals


def charger(chemin, nom):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


QUIZ = charger(ICI / "quiz.py", "quiz85").QUIZ
FIG = charger(ICI / "figures" / "figures.py", "fig85").FIGURES
Q = {q["id"]: q for q in QUIZ["questions"]}

bilan = {"ok": 0, "ko": 0}


def ok(cond, msg):
    bilan["ok" if cond else "ko"] += 1
    print(("  ✓ " if cond else "  ✗ ") + msg)


def egal(a, b):
    return sp.simplify(sp.expand(a - b)) == 0


def egal_num(a, b, pts=(-1.3, -0.4, 0.3, 0.9, 1.7, 2.6)):
    """Égalité de deux expressions en x (contrôle numérique en plus de simplify)."""
    return all(abs(complex(sp.N((a - b).subs(x, p)))) < 1e-9 for p in pts)


TRANS = standard_transformations + (implicit_multiplication_application, convert_xor)


def lire(saisie):
    """Lecture sympy d'une saisie d'élève (indépendante de quizMath.js)."""
    s = saisie.replace("×", "*").replace("−", "-").replace(" ", "")
    s = re.sub(r"(\d),(\d)", r"\1.\2", s)
    # « e^2x » : l'exposant s'arrête au premier facteur (comme sur une calculatrice)
    s = re.sub(r"e\^(-?\d+(?:\.\d+)?)([a-z(])", r"(e^\1)*\2", s)
    s = re.sub(r"e\^(-?)([a-z])", r"e^(\1\2)", s)      # e^-x, e^x
    s = s.replace("exp", "EXP")
    s = re.sub(r"(?<![A-Z])e", "E", s)                  # constante e
    s = s.replace("EXP", "exp")
    s = re.sub(r"xE", "x*E", s)
    return parse_expr(s, local_dict={"x": x, "E": E, "exp": sp.exp}, transformations=TRANS)


def saisies(q, attendu, tol=None):
    for s in q["acceptees"]:
        v = lire(s)
        juste = egal_num(v, attendu) if tol is None else abs(float(v) - float(attendu)) <= tol + 1e-12
        ok(juste, f"{q['id']} acceptée « {s} » = {sp.sstr(v)} est juste")
    for s in q["refusees"]:
        v = lire(s)
        juste = egal_num(v, attendu) if tol is None else abs(float(v) - float(attendu)) <= tol + 1e-12
        ok(not juste, f"{q['id']} refusée « {s} » = {sp.sstr(v)} est fausse")


def cle_qcm(q, verites):
    bonnes = [i for i, v in enumerate(verites) if v]
    if q["type"] == "qcm":
        ok(bonnes == [q["bonne"]], f"{q['id']} : seule la réponse n° {q['bonne']} est juste (calcul : {bonnes})")
    else:
        ok(sorted(q["bonnes"]) == bonnes, f"{q['id']} : bonnes = {q['bonnes']} (calcul : {bonnes})")


def courbe_de(nom):
    """Expression pgfplots de la (première) courbe tracée dans une figure."""
    m = re.search(r"\\addplot\[courbe[^\]]*\]\s*\{(.+?)\};", FIG[nom])
    return m.group(1).replace(" ", "") if m else None


def points(nom):
    return [(float(a), float(b)) for a, b in re.findall(r"\\pnt(?:\[[^\]]*\])?\{([-\d.]+)\}\{([-\d.]+)\}", FIG[nom])]


f_exp = sp.exp(x)

# ---------------------------------------------------------------- q01
print("q01 — e^x = -2")
q = Q["q01"]
ok(sp.solveset(sp.Eq(sp.exp(x), -2), x, R) == sp.S.EmptySet, "e^x = -2 n'a aucune solution réelle")
ok(q["reponse"] is False, "clé : Faux")

# ---------------------------------------------------------------- q02
print("q02 — courbe de exp parmi 4")
q = Q["q02"]
cands = {"q02_a": sp.exp(-x), "q02_b": sp.exp(x) - 1, "q02_c": sp.exp(x), "q02_d": sp.exp(x) + 1}
attendu_fig = {"q02_a": "exp(-x)", "q02_b": "exp(x)-1", "q02_c": "exp(x)", "q02_d": "exp(x)+1"}
for nom, e in attendu_fig.items():
    ok(courbe_de(nom) == e, f"figure {nom} trace bien {e}")
verites = []
for nom in q["choix_figures"]:
    g = cands[nom]
    est_exp = egal(g, f_exp)
    verites.append(est_exp)
    if not est_exp:
        raisons = []
        if g.subs(x, 0) != 1:
            raisons.append(f"g(0) = {g.subs(x, 0)} ≠ 1")
        if sp.simplify(sp.diff(g, x) - sp.exp(-x) * -1) == 0 or sp.diff(g, x).subs(x, 0) < 0:
            raisons.append("décroissante")
        ok(bool(raisons), f"{nom} ({g}) n'est pas exp : {', '.join(raisons)}")
cle_qcm(q, verites)
ok(points("q02_corrige") == [(0.0, 1.0), (1.0, 2.71828)], "q02_corrige : points (0;1) et (1;e)")
ok(abs(2.71828 - float(E)) < 1e-5, "e ≈ 2,71828")

# ---------------------------------------------------------------- q03
print("q03 — (e^x)^3 × e^(-x)")
q = Q["q03"]
v = sp.exp(x) ** 3 * sp.exp(-x)
ok(egal(sp.powsimp(v), sp.exp(2 * x)), "(e^x)^3 × e^(-x) = e^(2x)")
ok(egal_num(lire(q["reponses"][0]), sp.exp(2 * x)), "réponse de référence exp(2*x)")
saisies(q, sp.exp(2 * x))

# ---------------------------------------------------------------- q04
print("q04 — tangente en 0")
q = Q["q04"]
T = sp.diff(f_exp, x).subs(x, 0) * x + f_exp.subs(x, 0)
ok(egal(T, x + 1), f"tangente en 0 : y = {T}")
choix = [x + 1, x, E * x, x - 1]
cle_qcm(q, [egal(c, T) for c in choix])
ok(sp.minimum(sp.exp(x) - x - 1, x, R) == 0, "e^x - (x+1) ≥ 0 sur R (minimum 0) : courbe au-dessus de T")
ok(points("q04_corrige") == [(0.0, 1.0)] and points("q04_enonce") == [(0.0, 1.0)], "figures q04 : point (0;1)")

# ---------------------------------------------------------------- q05
print("q05 — égalités vraies pour tout x")
q = Q["q05"]
egalites = [
    (sp.exp(2 * x), sp.exp(x) ** 2),
    (sp.exp(-x), 1 / sp.exp(x)),
    (sp.exp(x + 1), sp.exp(x) + E),
    (sp.exp(x ** 2), sp.exp(x) ** 2),
    (sp.exp(3 * x) / sp.exp(x), sp.exp(2 * x)),
    (sp.exp(x) * sp.exp(2), sp.exp(2 * x)),
]
verites = [egal_num(a, b) for a, b in egalites]
for (a, b), vr in zip(egalites, verites):
    print(f"     {a} = {b} : {'vrai' if vr else 'faux'}")
cle_qcm(q, verites)

# ---------------------------------------------------------------- q06
print("q06 — variations de e^(-2x+1)")
q = Q["q06"]
fp = sp.diff(sp.exp(-2 * x + 1), x)
ok(egal(fp, -2 * sp.exp(-2 * x + 1)), f"f'(x) = {fp}")
ok(sp.solveset(fp >= 0, x, R) == sp.S.EmptySet, "f'(x) < 0 pour tout x : f décroissante")
ok(q["reponse"] is False, "clé : Faux")
ok(courbe_de("q06_corrige") is None and "exp(-2*x+1)" in FIG["q06_corrige"], "figure q06 : courbe e^(-2x+1)")
ok(points("q06_corrige") == [(0.0, 2.71828)], "figure q06 : point (0;e)")

# ---------------------------------------------------------------- q07
print("q07 — dérivée de e^(-3x+1)")
q = Q["q07"]
fp = sp.diff(sp.exp(-3 * x + 1), x)
choix = [-3 * sp.exp(-3 * x + 1), sp.exp(-3 * x + 1), (-3 * x + 1) * sp.exp(-3 * x), 3 * sp.exp(-3 * x + 1)]
cle_qcm(q, [egal_num(c, fp) for c in choix])

# ---------------------------------------------------------------- q08
print("q08 — dérivée de (x-1)e^x")
q = Q["q08"]
fp = sp.diff((x - 1) * sp.exp(x), x)
ok(egal(fp, x * sp.exp(x)), f"f'(x) = {sp.factor(fp)}")
saisies(q, x * sp.exp(x))

# ---------------------------------------------------------------- q09
print("q09 — e^(2x-1) = e^(x+3)")
q = Q["q09"]
S = sp.solveset(sp.Eq(sp.exp(2 * x - 1), sp.exp(x + 3)), x, R)
ok(S == sp.FiniteSet(4), f"S = {S}")
saisies(q, sp.Integer(4), tol=0)

# ---------------------------------------------------------------- q10
print("q10 — e^(3x-2) < e^(x+4)")
q = Q["q10"]
S = sp.solve_univariate_inequality(sp.exp(3 * x - 2) < sp.exp(x + 4), x, relational=False)
ok(S == sp.Interval.open(-sp.oo, 3), f"S = {S}")
for ineg in (3 * x - 2 < x + 4, 2 * x < 6, x < 3):
    ok(sp.solve_univariate_inequality(ineg, x, relational=False) == S, f"étape « {ineg} » équivalente")
ok(len(q["etapes"]) == 5 and "S =" in q["etapes"][-1], "5 étapes, la dernière donne S")

# ---------------------------------------------------------------- q11
print("q11 — limites")
q = Q["q11"]
lims = [
    (sp.limit(sp.exp(x), x, -sp.oo), 0),
    (sp.limit(x * sp.exp(-x), x, sp.oo), sp.oo),
    (sp.limit(sp.exp(x) / x ** 3, x, sp.oo), sp.oo),
    (sp.limit((sp.exp(x) - 1) / x, x, 0), 0),
    (sp.limit(x ** 2 * sp.exp(x), x, -sp.oo), 0),
]
for (calc, affiche) in lims:
    print(f"     calcul {calc}, affiché {affiche}")
cle_qcm(q, [calc == affiche for calc, affiche in lims])

# ---------------------------------------------------------------- q12
print("q12 — associer fonctions et courbes")
q = Q["q12"]
fonctions = [sp.exp(-x), sp.exp(-x ** 2), sp.exp(x ** 2), x * sp.exp(x)]
traces = {"q12_a": "exp(-x)", "q12_b": "exp(-x^2)", "q12_c": "exp(x^2)", "q12_d": "x*exp(x)"}
for nom, fct in zip(q["droite_figures"], fonctions):
    expr_fig = parse_expr(courbe_de(nom).replace("^", "**"), local_dict={"x": x, "exp": sp.exp})
    ok(egal(expr_fig, fct) and courbe_de(nom) == traces[nom], f"{nom} trace bien {fct}")
ok(sp.solveset(sp.diff(sp.exp(-x), x) >= 0, x, R) == sp.S.EmptySet, "e^(-x) strictement décroissante")
ok(sp.maximum(sp.exp(-x ** 2), x, R) == 1, "e^(-x²) : maximum 1 (en 0)")
ok(sp.minimum(sp.exp(x ** 2), x, R) == 1, "e^(x²) : minimum 1 (en 0)")
ok(sp.minimum(x * sp.exp(x), x, R) == -1 / E, "x e^x : minimum -1/e < 0, nulle en 0")
ok(all(sp.minimum(g, x, R) >= 0 for g in fonctions[:3]), "les trois autres sont positives")

# ---------------------------------------------------------------- q13
print("q13 — u_n = e^(-0,5n)")
q = Q["q13"]
u = sp.exp(-sp.Rational(1, 2) * n)
raison = sp.simplify(u.subs(n, n + 1) / u)
ok(raison == sp.exp(-sp.Rational(1, 2)), f"u(n+1)/u(n) = {raison} (constante)")
ok(sp.simplify(u.subs(n, 1) - u.subs(n, 0) - (u.subs(n, 2) - u.subs(n, 1))) != 0, "différences non constantes : pas arithmétique")
choix = ["geo", "ari", "geo", "ari"]
raisons = [sp.exp(-sp.Rational(1, 2)), -sp.Rational(1, 2), -sp.Rational(1, 2), sp.exp(-sp.Rational(1, 2))]
cle_qcm(q, [c == "geo" and r == raison for c, r in zip(choix, raisons)])
ok(round(float(raison), 2) == 0.61, f"raison ≈ {float(raison):.4f} → 0,61")
pts = points("q13_corrige")
ok(len(pts) == 9 and all(abs(b - float(u.subs(n, int(a)))) < 1e-4 for a, b in pts), "figure q13 : 9 points u_0 … u_8 exacts")

# ---------------------------------------------------------------- q14
print("q14 — maximum de x e^(-x)")
q = Q["q14"]
f = x * sp.exp(-x)
fp = sp.diff(f, x)
ok(egal(fp, (1 - x) * sp.exp(-x)), f"f'(x) = {sp.factor(fp)}")
ok(sp.solveset(fp, x, R) == sp.FiniteSet(1), "f' s'annule seulement en 1")
ok(sp.maximum(f, x, R) == 1 / E, "maximum de f = 1/e")
ok(sp.limit(f, x, -sp.oo) == -sp.oo and sp.limit(f, x, sp.oo) == 0, "limites -∞ et 0 (tableau)")
saisies(q, 1 / E, tol=0)
ok(points("q14_corrige") == [(1.0, 0.36788)] and abs(0.36788 - float(1 / E)) < 1e-5, "figure q14 : point (1;1/e)")
ok(points("q14_enonce") == [], "figure d'énoncé q14 : aucun point (ne donne pas la réponse)")

# ---------------------------------------------------------------- q15
print("q15 — condensateur u(4)")
q = Q["q15"]
uu = 5 * (1 - sp.exp(-sp.Rational(1, 2) * t))
v4 = uu.subs(t, 4)
ok(egal(v4, 5 * (1 - sp.exp(-2))), f"u(4) = {v4}")
ok(round(float(v4), 2) == 4.32, f"u(4) ≈ {float(v4):.5f} → 4,32")
ok(abs(float(lire(q["reponses"][0])) - float(v4)) < 1e-12, "réponse de référence")
saisies(q, v4, tol=q["tolerance"])
ok(abs(float(5 * sp.exp(-2)) - 0.68) < 0.005 and abs(float(5 * (1 - sp.exp(2))) + 31.95) < 0.005,
   "distracteurs : 5e^(-2) ≈ 0,68 (oubli de « 1 - ») et 5(1 - e^2) ≈ -31,95 (erreur de signe)")
ok(sp.limit(uu, t, sp.oo) == 5, "limite 5 V (asymptote)")
ok(points("q15_corrige") == [(4.0, 4.3233)] and points("q15_enonce") == [], "figures q15 : point (4;4,32) au corrigé seulement")

# ---------------------------------------------------------------- q11b (ajoutée le 2026-11-03)
print("q11b — limite de e^(2x) - 3e^x en +oo")
q = Q["q11b"]
g = sp.exp(2 * x) - 3 * sp.exp(x)
ok(egal(sp.exp(x) * (sp.exp(x) - 3), g), "factorisation e^x(e^x - 3)")
ok(sp.limit(g, x, sp.oo) == sp.oo, "limite +oo")
ok(q["bonne"] == 0 and q["choix"][0] == r"$+\infty$", "clé : +oo")

# ---------------------------------------------------------------- parties du cours
print("parties du cours")
ok(all(qq.get("partie") in QUIZ["parties"] for qq in QUIZ["questions"]), "chaque question a une partie du cours connue")
ok(all(any(qq.get("partie") == p for qq in QUIZ["questions"]) for p in QUIZ["parties"]), "chaque partie du cours a au moins une question")

# ---------------------------------------------------------------- figures q01 / q10
print("figures q01 et q10")
ok("{exp(x)}" in FIG["q01_corrige"] and "(axis cs:-3.3,-2)" in FIG["q01_corrige"], "q01 : courbe de exp et droite y = -2")
ok("(3.14,0.2) -- (3,0.2) -- (3,-0.2) -- (3.14,-0.2)" in FIG["q10_corrige"], "q10 : crochet ouvert en 3 (tourné vers l'extérieur)")

print(f"\nBilan : {bilan['ok']} contrôle(s) juste(s), {bilan['ko']} erreur(s).")
raise SystemExit(1 if bilan["ko"] else 0)
