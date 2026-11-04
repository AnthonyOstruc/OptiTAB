# -*- coding: utf-8 -*-
"""Vérification (sympy / numpy) de tous les résultats de la notion 84
« Fonctions sinus et cosinus » (cours, fiche, exercices et figures), finition 2026-11-02.

    python verif_trigo.py   →  « TOUT EST JUSTE » ou la liste des échecs
"""
import numpy as np
import sympy as sp
from sympy import pi, sin, cos, sqrt, Rational as Q, simplify, integrate, limit, oo, diff, Interval, S

x, t, n = sp.symbols("x theta n", real=True)
ECHECS, NB = [], [0]


def ok(nom, cond):
    NB[0] += 1
    if not bool(cond):
        ECHECS.append(nom)


def egal(nom, a, b):
    ok(nom, simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0)


def ineg(nom, cond, a, b, attendu, bornes=()):
    """cond : fonction booléenne numpy ; attendu : ensemble sympy. Contrôle sur une grille
    fine (hors voisinage des bornes) puis contrôle exact (sympy) aux bornes."""
    xs = np.linspace(float(a), float(b), 40001)
    pts = [float(p) for p in bornes]
    loin = np.all([np.abs(xs - p) > 1e-6 for p in pts], axis=0) if pts else np.ones_like(xs, bool)
    dans = np.array([bool(attendu.contains(sp.Float(v))) for v in xs[loin][::50]])
    ok(nom + " (grille)", np.array_equal(cond(xs[loin][::50]), dans))


def sols(expr, dom):
    """Solutions de expr = 0 sur dom (numérique fin + nsimplify)."""
    return sp.solveset(expr, x, dom)


# ------------------------------------------------------------------ cours
egal("cours dérivée cos(3x-1)", diff(cos(3 * x - 1), x), -3 * sin(3 * x - 1))
egal("cours (x sin x)'", diff(x * sin(x), x), sin(x) + x * cos(x))
egal("cours (sin² x)'", diff(sin(x) ** 2, x), 2 * sin(x) * cos(x))
ok("cours lim sin x / x", limit(sin(x) / x, x, 0) == 1)
ineg("cours cos x >= 1/2 sur [-pi,pi]", lambda v: np.cos(v) >= 0.5, -pi, pi, Interval(-pi / 3, pi / 3), [-pi / 3, pi / 3])
egal("cours cos(pi/3)", cos(pi / 3), Q(1, 2))
egal("cours cos(2x) période pi", cos(2 * (x + pi)), cos(2 * x))
ineg("cours sin(2x) variations", lambda v: 2 * np.cos(2 * v) >= 0, 0, pi, Interval(0, pi / 4) | Interval(3 * pi / 4, pi), [pi / 4, 3 * pi / 4])
ok("cours lim cos x / x", limit(cos(x) / x, x, oo) == 0)
for a, c, s in [(0, 1, 0), (pi / 6, sqrt(3) / 2, Q(1, 2)), (pi / 4, sqrt(2) / 2, sqrt(2) / 2),
                (pi / 3, Q(1, 2), sqrt(3) / 2), (pi / 2, 0, 1), (pi, -1, 0)]:
    egal(f"tableau cos {a}", cos(a), c)
    egal(f"tableau sin {a}", sin(a), s)

# ------------------------------------------------------------------ 1198
egal("1198 Q1 cos", cos(2 * pi / 3), -Q(1, 2)); egal("1198 Q1 sin", sin(2 * pi / 3), sqrt(3) / 2)
egal("1198 Q2 cos", cos(-pi / 4), sqrt(2) / 2); egal("1198 Q2 sin", sin(-pi / 4), -sqrt(2) / 2)
egal("1198 Q3 cos", cos(7 * pi / 6), -sqrt(3) / 2); egal("1198 Q3 sin", sin(7 * pi / 6), -Q(1, 2))
egal("1198 Q4", cos(13 * pi / 3), Q(1, 2))
x5 = -sp.acos(Q(3, 5))
egal("1198 Q5", sin(x5), -Q(4, 5))
ok("1198 Q5 intervalle", -pi / 2 <= x5 <= 0)

# ------------------------------------------------------------------ 1199
egal("1199 Q1", diff(sin(3 * x), x), 3 * cos(3 * x))
egal("1199 Q2", diff(x ** 2 * cos(x), x), 2 * x * cos(x) - x ** 2 * sin(x))
egal("1199 Q3", diff(cos(x ** 2 + 1), x), -2 * x * sin(x ** 2 + 1))
egal("1199 Q4", diff(sin(x) * cos(x), x), cos(x) ** 2 - sin(x) ** 2)
egal("1199 Q5", diff(sin(x) / x, x), (x * cos(x) - sin(x)) / x ** 2)
a = pi / 3
T = cos(a) * (x - a) + sin(a)
egal("1199 Q6 tangente", T, x / 2 + sqrt(3) / 2 - pi / 6)

# ------------------------------------------------------------------ 1200
I02 = Interval.Ropen(0, 2 * pi)
ok("1200 Q1", sols(sin(x) - Q(1, 2), I02) == sp.FiniteSet(pi / 6, 5 * pi / 6))
ok("1200 Q2", sols(cos(x) + sqrt(2) / 2, Interval.Lopen(-pi, pi)) == sp.FiniteSet(-3 * pi / 4, 3 * pi / 4))
ok("1200 Q3", sols(cos(x) - sin(x), I02) == sp.FiniteSet(pi / 4, 5 * pi / 4))
ok("1200 Q4", sols(2 * sin(x) ** 2 - 3 * sin(x) + 1, I02) == sp.FiniteSet(pi / 6, pi / 2, 5 * pi / 6))
ok("1200 Q5", sols(sin(2 * x) - sin(x), I02) == sp.FiniteSet(0, pi / 3, pi, 5 * pi / 3))

# ------------------------------------------------------------------ 1201
f = cos(x) ** 2 + sin(x)
egal("1201 Q1", f.subs(x, x + 2 * pi), f)
egal("1201 Q2", f.subs(x, pi - x), f)
egal("1201 Q3", diff(f, x), cos(x) * (1 - 2 * sin(x)))
I0 = Interval(0, 2 * pi)
ok("1201 zéros f'", sols(diff(f, x), I0) == sp.FiniteSet(pi / 6, pi / 2, 5 * pi / 6, 3 * pi / 2))
for v, val in [(0, 1), (pi / 6, Q(5, 4)), (pi / 2, 1), (5 * pi / 6, Q(5, 4)), (3 * pi / 2, -1), (2 * pi, 1)]:
    egal(f"1201 f({v})", f.subs(x, v), val)
fp = sp.lambdify(x, diff(f, x), "numpy")
for (a_, b_), sg in [((0, np.pi / 6), 1), ((np.pi / 6, np.pi / 2), -1), ((np.pi / 2, 5 * np.pi / 6), 1),
                     ((5 * np.pi / 6, 3 * np.pi / 2), -1), ((3 * np.pi / 2, 2 * np.pi), 1)]:
    xs = np.linspace(a_, b_, 200)[1:-1]
    ok(f"1201 signe f' {a_:.2f}", np.all(np.sign(fp(xs)) == sg))
ok("1201 Q5", sols(f - 1, I0) == sp.FiniteSet(0, pi / 2, pi, 2 * pi))
xs = np.linspace(0, 2 * np.pi, 20001)
fv = np.cos(xs) ** 2 + np.sin(xs)
ok("1201 Q6 max", abs(fv.max() - 1.25) < 1e-6)
ok("1201 Q6 min", abs(fv.min() + 1) < 1e-6)

# ------------------------------------------------------------------ 1202
A = (1 + cos(t)) * sin(t)
c_, s_ = cos(t), sin(t)
egal("1202 Q2 aire", (2 + 2 * c_) / 2 * s_, A)
egal("1202 Q3 dérivée", diff(A, t), (2 * cos(t) - 1) * (cos(t) + 1))
egal("1202 Q3 forme", diff(A, t), 2 * cos(t) ** 2 + cos(t) - 1)
ok("1202 Q4 zéro", sp.solveset(diff(A, t), t, Interval(0, pi / 2)) == sp.FiniteSet(pi / 3))
egal("1202 A(pi/3)", A.subs(t, pi / 3), 3 * sqrt(3) / 4)
egal("1202 A(0)", A.subs(t, 0), 0)
egal("1202 A(pi/2)", A.subs(t, pi / 2), 1)
ok("1202 A max ≈ 1,30", abs(float(3 * sqrt(3) / 4) - 1.299) < 1e-3)
egal("1202 CD = 1 en pi/3", 2 * cos(pi / 3), 1)

# ------------------------------------------------------------------ 1203
ok("1203 Q1", limit(sin(x) / x, x, 0) == 1)
ok("1203 Q2", limit(sin(3 * x) / x, x, 0) == 3)
ok("1203 Q3", limit((1 - cos(x)) / x ** 2, x, 0) == Q(1, 2))
egal("1203 Q3 transformation", (sin(x) / x) ** 2 / (1 + cos(x)) - (1 - cos(x)) / x ** 2, 0)
ok("1203 Q4", limit(sin(x) / x, x, oo) == 0)
ok("1203 Q5", limit(x + 2 * cos(x), x, oo) == oo)

# ------------------------------------------------------------------ 1204
egal("1204 Q1", cos(3 * (x + 2 * pi / 3)), cos(3 * x))
egal("1204 Q2 g paire", (x * sin(x)).subs(x, -x), x * sin(x))
h = x + cos(x)
ok("1204 Q2 h non paire", simplify(h.subs(x, -pi) - h.subs(x, pi)) != 0)
ok("1204 Q2 h(0)=1", h.subs(x, 0) == 1)
k = sin(x) ** 2
egal("1204 Q3 paire", k.subs(x, -x), k)
egal("1204 Q3 période", k.subs(x, x + pi), k)
for v, val in [(-pi, 0), (-pi / 2, 1), (0, 0), (pi / 2, 1), (pi, 0)]:
    egal(f"1204 k({v})", k.subs(x, v), val)
ineg("1204 k croissante sur [0,pi/2]", lambda v: 2 * np.sin(v) * np.cos(v) >= -1e-12, 0, pi / 2, Interval(0, pi / 2))

# ------------------------------------------------------------------ 1205
ineg("1205 Q1", lambda v: np.sin(v) >= np.sqrt(3) / 2, 0, 2 * pi, Interval(pi / 3, 2 * pi / 3), [pi / 3, 2 * pi / 3])
egal("1205 Q1 bornes", sin(pi / 3) - sin(2 * pi / 3), 0)
ineg("1205 Q2", lambda v: np.cos(v) <= 0.5, -pi, pi, Interval(-pi, -pi / 3) | Interval(pi / 3, pi), [-pi / 3, pi / 3])
ineg("1205 Q3", lambda v: np.cos(2 * v) < 0.5, 0, pi, Interval.open(pi / 6, 5 * pi / 6), [pi / 6, 5 * pi / 6])
egal("1205 Q3 bornes", cos(2 * pi / 6), Q(1, 2))
P = (2 * cos(x) - 1) * sin(x)
Pn = sp.lambdify(x, P, "numpy")
for (a_, b_), sg in [((0, np.pi / 3), 1), ((np.pi / 3, np.pi), -1), ((np.pi, 5 * np.pi / 3), 1), ((5 * np.pi / 3, 2 * np.pi), -1)]:
    xs = np.linspace(a_, b_, 300)[1:-1]
    ok(f"1205 Q4 signe {a_:.2f}", np.all(np.sign(Pn(xs)) == sg))
ok("1205 Q4 zéros", sols(P, I0) == sp.FiniteSet(0, pi / 3, pi, 5 * pi / 3, 2 * pi))
ineg("1205 Q5", lambda v: (2 * np.cos(v) - 1) * np.sin(v) >= 0, 0, 2 * pi,
     Interval(0, pi / 3) | Interval(pi, 5 * pi / 3) | sp.FiniteSet(2 * pi), [0, pi / 3, pi, 5 * pi / 3, 2 * pi])
ok("1205 Q5 P(2pi)=0", P.subs(x, 2 * pi) == 0)

# ------------------------------------------------------------------ 1206
u = cos(pi / 2 ** n)
egal("1206 u0", u.subs(n, 0), -1); egal("1206 u1", u.subs(n, 1), 0); egal("1206 u2", u.subs(n, 2), sqrt(2) / 2)
ok("1206 lim u", limit(u, n, oo) == 1)
vv = [sin(k_ * pi / 4) for k_ in range(16)]
ok("1206 v période 8", all(simplify(vv[i] - vv[i + 8]) == 0 for i in range(8)))
for k_, val in enumerate([0, sqrt(2) / 2, 1, sqrt(2) / 2, 0, -sqrt(2) / 2, -1, -sqrt(2) / 2]):
    egal(f"1206 v{k_}", vv[k_], val)
w = (2 * n + sin(n)) / n
ok("1206 w encadrement", all(2 - 1 / m - 1e-12 <= (2 * m + np.sin(m)) / m <= 2 + 1 / m + 1e-12 for m in range(1, 500)))
ok("1206 lim w", limit(2 - 1 / n, n, oo) == 2 and limit(2 + 1 / n, n, oo) == 2)
cs = [cos(k_ * pi / 3) for k_ in range(40)]
tt = [sum(cs[:m + 1]) for m in range(30)]
egal("1206 t1", tt[1], Q(3, 2)); egal("1206 t2", tt[2], 1); egal("1206 t6", tt[6], 1)
ok("1206 t période 6", all(simplify(tt[m + 6] - tt[m]) == 0 for m in range(20)))
ok("1206 somme 6 termes nulle", simplify(sum(cs[:6])) == 0)
ok("1206 lim z", limit(n * sin(1 / n), n, oo) == 1)

# ------------------------------------------------------------------ 1207
ok("1207 Q1", integrate(sin(x), (x, 0, pi)) == 2)
ok("1207 Q2", integrate(x * sin(x), (x, 0, pi)) == pi)
egal("1207 Q3", diff(sin(x) ** 2 / 2, x), sin(x) * cos(x))
ok("1207 Q4", integrate(sin(2 * x), (x, 0, pi)) == 0)
ok("1207 Q4 moitiés", integrate(sin(2 * x), (x, 0, pi / 2)) == 1 and integrate(sin(2 * x), (x, pi / 2, pi)) == -1)
egal("1207 Q5", integrate(sin(x) - cos(x), (x, pi / 4, 5 * pi / 4)), 2 * sqrt(2))
ineg("1207 Q5 position", lambda v: np.sin(v) - np.cos(v) >= 0, 0, 2 * pi, Interval(pi / 4, 5 * pi / 4), [pi / 4, 5 * pi / 4])
ok("1207 Q5 ≈ 2,83", abs(float(2 * sqrt(2)) - 2.83) < 0.005)

# ------------------------------------------------------------------ figures (valeurs codées en dur)
ok("fig tangente ordonnée origine", abs(np.sqrt(3) / 2 - np.pi / 6 - (0.86603 - 0.5236)) < 1e-4)
ok("fig 1202 max", abs((1 + np.cos(np.pi / 3)) * np.sin(np.pi / 3) - 1.299) < 1e-3)
ok("fig 1200 Q5 point", abs(np.sin(5 * np.pi / 3) + 0.86603) < 1e-4)
ok("fig 1198 Q5 angle", abs(np.cos(-np.arccos(0.6)) - 0.6) < 1e-12 and abs(np.sin(-np.arccos(0.6)) + 0.8) < 1e-12)
# reprise de la finition (2026-11-02, après-midi) : figures retouchées
egal("fig 1205 Q2 : M(pi) = M(-pi)", cos(pi) - cos(-pi) + sin(pi) - sin(-pi), 0)
ineg("fig 1205 Q2 arc vert", lambda v: np.cos(v) <= 0.5, -pi, pi,
     Interval(-pi, -pi / 3) | Interval(pi / 3, pi), [-pi / 3, pi / 3])
egal("fig 1198 cos(2pi/3) (étiquette -1/2)", cos(2 * pi / 3), -Q(1, 2))
egal("fig 1198 cos(7pi/6) (étiquette -racine(3)/2)", cos(7 * pi / 6), -sqrt(3) / 2)
egal("fig 1202 A max (étiquette 3racine(3)/4)", (1 + cos(pi / 3)) * sin(pi / 3), 3 * sqrt(3) / 4)
ok("fig 1203 gendarmes : sin x / x entre -1/x et 1/x", all(abs(np.sin(v) / v) <= 1 / v + 1e-15 for v in np.linspace(1, 20, 4001)))
ok("fig 1203 limite (1 - cos x)/x² = 1/2", limit((1 - cos(x)) / x ** 2, x, 0) == Q(1, 2))
ok("fig 1206 w1 = 2 + sin 1 ≈ 2,84", abs(2 + np.sin(1) - 2.84) < 5e-3)
ok("fig 1200 Q5 : sin(2x) = sin x en pi", sin(2 * pi) == sin(pi) == 0)

print(f"{NB[0]} vérifications")
if ECHECS:
    print("ÉCHECS :", *ECHECS, sep="\n  ")
else:
    print("TOUT EST JUSTE")
