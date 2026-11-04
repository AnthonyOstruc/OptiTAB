# -*- coding: utf-8 -*-
"""Vérification des résultats de la notion 157 (Première, trigonométrie)."""
import math
from sympy import (pi, cos, sin, sqrt, Rational, simplify, nsimplify, solveset, Interval, S,
                   Eq, symbols, acos, Union)

x = symbols("x", real=True)
ok = 0


def eq(a, b, msg):
    global ok
    assert simplify(a - b) == 0, (msg, a, b)
    ok += 1


def sols(expr, a, b, attendu, msg, left_open=False):
    global ok
    I = Interval(a, b, left_open=left_open)
    s = solveset(expr, x, I)
    assert s == attendu, (msg, s, attendu)
    ok += 1


# ---- cours
eq(45 * pi / 180, pi / 4, "45°"); eq(120 * pi / 180, 2 * pi / 3, "120°"); eq(pi / 5 * 180 / pi, 36, "pi/5")
eq(Rational(17, 3) * pi, -pi / 3 + 3 * 2 * pi, "17pi/3")
for t, c, s_ in [(0, 1, 0), (pi / 6, sqrt(3) / 2, Rational(1, 2)), (pi / 4, sqrt(2) / 2, sqrt(2) / 2),
                 (pi / 3, Rational(1, 2), sqrt(3) / 2), (pi / 2, 0, 1), (pi, -1, 0)]:
    eq(cos(t), c, ("cos", t)); eq(sin(t), s_, ("sin", t))
eq(cos(5 * pi / 6), -sqrt(3) / 2, "cos 5pi/6"); eq(sin(7 * pi / 6), -Rational(1, 2), "sin 7pi/6")
eq(sin(2 * pi / 3), sqrt(3) / 2, "sin 2pi/3"); eq(cos(-3 * pi / 4), -sqrt(2) / 2, "cos -3pi/4")
eq(cos(2 * pi / 3), -Rational(1, 2), "cos(pi/3+pi/3)")
# cours : exemple cos t = 3/5, t dans [-pi/2 ; 0]
eq(-sqrt(1 - Rational(9, 25)), -Rational(4, 5), "sin t = -4/5")
sols(cos(x) - Rational(1, 2), -pi, pi, {-pi / 3, pi / 3}, "cos=1/2 ]-pi;pi]", True)
sols(sin(x) - sqrt(2) / 2, 0, 2 * pi, {pi / 4, 3 * pi / 4}, "sin = rac2/2")
# angles associés (identités)
for e1, e2 in [(cos(-x), cos(x)), (sin(-x), -sin(x)), (cos(pi - x), -cos(x)), (sin(pi - x), sin(x)),
               (cos(pi + x), -cos(x)), (sin(pi + x), -sin(x)), (cos(pi / 2 - x), sin(x)),
               (sin(pi / 2 - x), cos(x)), (cos(pi / 2 + x), -sin(x)), (sin(pi / 2 + x), cos(x))]:
    eq(e1, e2, ("associe", e1))

# ---- 1384
eq(60 * pi / 180, pi / 3, "60°"); eq(2 * pi / 3 * 180 / pi, 120, "2pi/3")
eq(Rational(1, 4) * 2 * pi, pi / 2, "arc quart"); eq(Rational(1, 8) * 2 * pi, pi / 4, "arc huitième")
eq(3 * pi / 2 * 2, 3 * pi, "arc rayon 2")

# ---- 1385
eq(cos(pi / 4) ** 2 * 2, 1, "2a^2=1")
eq(sqrt(1 - Rational(1, 4)), sqrt(3) / 2, "sin pi/3")
eq(cos(pi / 6) ** 2 + sin(pi / 6) ** 2, 1, "rel fond pi/6")
eq(cos(-pi / 6), sqrt(3) / 2, "cos -pi/6"); eq(sin(-pi / 6), -Rational(1, 2), "sin -pi/6")
eq(cos(5 * pi / 6), -sqrt(3) / 2, ""); eq(sin(5 * pi / 6), Rational(1, 2), "")
for t, c, s_ in [(0, 1, 0), (pi / 2, 0, 1), (pi, -1, 0), (3 * pi / 2, 0, -1)]:
    eq(cos(t), c, t); eq(sin(t), s_, t)

# ---- 1390 (DS)
eq(cos(5 * pi / 4) + sin(7 * pi / 6), (-sqrt(2) - 1) / 2, "DS 1a")
eq(cos(pi / 6) ** 2 - sin(pi / 6) ** 2, Rational(1, 2), "DS 1b")
eq(-sqrt(1 - Rational(4, 25)), -sqrt(21) / 5, "DS 2")
xx = math.pi + math.acos(0.4)
assert math.pi <= xx <= 1.5 * math.pi and abs(math.sin(xx) + math.sqrt(21) / 5) < 1e-12
sols(2 * sin(x) - sqrt(3), 0, 2 * pi, {pi / 3, 2 * pi / 3}, "DS 3a")
sols(2 * cos(x) + sqrt(2), -pi, pi, {-3 * pi / 4, 3 * pi / 4}, "DS 3b", True)
g = 3 * sin(x) + 2
eq(g.subs(x, -x) + g, 4, "DS g sym"); eq(g.subs(x, x + 2 * pi), g, "DS g période")
eq(g.subs(x, pi / 2), 5, "g max"); eq(g.subs(x, -pi / 2), -1, "g min")
sols(g - 2, 0, 2 * pi, {0, pi, 2 * pi}, "DS g=2")
sols(g - Rational(7, 2), 0, 2 * pi, {pi / 6, 5 * pi / 6}, "DS g=7/2")

# ---- 1386
for t, c, s_ in [(7 * pi / 6, -sqrt(3) / 2, -Rational(1, 2)), (3 * pi / 4, -sqrt(2) / 2, sqrt(2) / 2),
                 (11 * pi / 6, sqrt(3) / 2, -Rational(1, 2)), (-pi / 3, Rational(1, 2), -sqrt(3) / 2)]:
    eq(cos(t), c, t); eq(sin(t), s_, t)
eq(cos(13 * pi / 6), sqrt(3) / 2, "13pi/6"); eq(sin(17 * pi / 4), sqrt(2) / 2, "17pi/4")
eq(cos(-7 * pi / 3), Rational(1, 2), "-7pi/3")
eq(sqrt(1 - Rational(9, 25)), Rational(4, 5), "3a"); eq(-sqrt(1 - Rational(4, 9)), -sqrt(5) / 3, "3b")
eq(sqrt(Rational(5, 9)), sqrt(5) / 3, "")

# ---- 1387
sols(cos(x) - Rational(1, 2), 0, 2 * pi, {pi / 3, 5 * pi / 3}, "1a")
sols(sin(x) + sqrt(2) / 2, 0, 2 * pi, {5 * pi / 4, 7 * pi / 4}, "1b")
sols(cos(x) + 1, 0, 2 * pi, {pi}, "1c")
sols(sin(x), 0, 2 * pi, {0, pi, 2 * pi}, "1d")
sols(cos(x) - sqrt(3) / 2, -pi, pi, {-pi / 6, pi / 6}, "2a", True)
sols(sin(x) - Rational(1, 2), -pi, pi, {pi / 6, 5 * pi / 6}, "2b", True)
sols(2 * cos(x) + 1, -pi, pi, {-2 * pi / 3, 2 * pi / 3}, "2c", True)
sols(cos(x) - 2, 0, 2 * pi, S.EmptySet, "3a")
sols(cos(x) - sin(x), 0, 2 * pi, {pi / 4, 5 * pi / 4}, "3b")

# ---- 1392
for t, r in [(13 * pi / 6, pi / 6), (-5 * pi / 4, 3 * pi / 4), (19 * pi / 3, pi / 3), (-pi / 3, 5 * pi / 3)]:
    k = simplify((t - r) / (2 * pi)); assert k.is_integer, (t, r); ok += 1
eq(5 * pi / 4 * 180 / pi, 225, ""); eq(7 * pi / 6 * 180 / pi, 210, "")

# ---- 1389 : f = 2cos x - 1
f = 2 * cos(x) - 1
eq(f.subs(x, -x), f, "pair"); eq(f.subs(x, x + 2 * pi), f, "période")
vals = {0: 1, pi / 3: 0, pi / 2: -1, 2 * pi / 3: -2, pi: -3}
for a, v in vals.items():
    eq(f.subs(x, a), v, ("f", a))
# décroissance sur [0 ; pi] et valeur intermédiaire 0 en pi/3 (tableau : +/1, =/0, -/-3)
import numpy as np
X = np.linspace(0, math.pi, 2001); Y = 2 * np.cos(X) - 1
assert np.all(np.diff(Y) < 0); ok += 1
sols(f, -pi, pi, {-pi / 3, pi / 3}, "f=0 ]-pi;pi]", True)
sols(f + 3, -pi, pi, {pi}, "f=-3 ]-pi;pi]", True)
eq(f.subs(x, -pi / 3), 0, ""); eq(f.subs(x, 7 * pi / 3), 0, "")

# ---- 1391 (remplacé) : cos(pi/5) = (1 + sqrt5)/4
c5 = (1 + sqrt(5)) / 4
eq(cos(pi / 5), c5, "cos pi/5")
s5 = sqrt(10 - 2 * sqrt(5)) / 4
eq(1 - c5 ** 2, (10 - 2 * sqrt(5)) / 16, "1-c^2")
assert abs(float(sin(pi / 5)) - float(s5)) < 1e-14; ok += 1
assert abs(float(cos(4 * pi / 5)) + float(c5)) < 1e-14; ok += 1
assert abs(float(sin(6 * pi / 5)) + float(s5)) < 1e-14; ok += 1
assert abs(float(cos(-pi / 5)) - float(c5)) < 1e-14; ok += 1
assert abs(float(cos(3 * pi / 10)) - float(s5)) < 1e-14; ok += 1
assert abs(float(sin(3 * pi / 10)) - float(c5)) < 1e-14; ok += 1
assert abs(float(cos(pi / 5) + cos(2 * pi / 5) + cos(3 * pi / 5) + cos(4 * pi / 5))) < 1e-14; ok += 1
A = cos(pi - x) + cos(pi + x) + sin(pi / 2 - x) + 3 * cos(-x)
eq(A, 2 * cos(x), "A(x)")
B = sin(pi - x) + sin(-x) + cos(pi / 2 - x)
eq(B, sin(x), "B(x)")
C = sin(x + pi) + cos(pi / 2 + x)
eq(C, -2 * sin(x), "C(x)")
eq(A.subs(x, pi / 5), (1 + sqrt(5)) / 2, "A(pi/5)")
assert 0 < float(c5) < 1; ok += 1

# ---- 1388 grande roue : h(t) = 15 - 12 cos(pi t)
t = symbols("t", real=True)
h = 15 - 12 * cos(pi * t)
eq(h.subs(t, 0), 3, "h0"); eq(h.subs(t, 1), 27, "h1"); eq(h.subs(t, 2), 3, "h2")
eq(h.subs(t, Rational(1, 3)), 9, "h(1/3)"); eq(h.subs(t, Rational(1, 2)), 15, "h(1/2)")
eq(h.subs(t, Rational(2, 3)), 21, "h(2/3)"); eq(h.subs(t, Rational(4, 3)), 21, "h(4/3)")
eq(h.subs(t, Rational(3, 2)), 15, "h(3/2)")
s = solveset(h - 15, t, Interval(0, 2)); assert s == {Rational(1, 2), Rational(3, 2)}, s; ok += 1
s = solveset(h - 21, t, Interval(0, 2)); assert s == {Rational(2, 3), Rational(4, 3)}, s; ok += 1
T = np.linspace(0, 2, 200001); H = 15 - 12 * np.cos(np.pi * T)
duree = (H >= 21).sum() * (T[1] - T[0]) * 60
assert abs(duree - 40) < 0.01, duree; ok += 1
# figure : position de la nacelle après un angle theta depuis B : (12 sin θ ; 15 - 12 cos θ)
th = 1.1; assert abs(math.hypot(12 * math.sin(th), 15 - 12 * math.cos(th) - 15) - 12) < 1e-12; ok += 1

# ---- nouveau-1 : Archimède, c' = sqrt(2 - sqrt(4 - c^2))
c = 1.0; n = 6
res = []
for _ in range(5):
    res.append((n, n * c / 2))
    c = math.sqrt(2 - math.sqrt(4 - c * c)); n *= 2
res.append((n, n * c / 2))
attendus = {6: 3.0, 12: 3.105828541, 24: 3.132628613, 48: 3.139350203, 96: 3.141031951, 192: 3.141452472}
for n_, v in res:
    assert abs(v - attendus[n_]) < 1e-8, (n_, v); ok += 1
c12 = sqrt(2 - sqrt(3)); eq(c12 ** 2, 2 - sqrt(3), "c12")
eq(2 * sin(pi / 12), c12, "c12 = 2 sin(pi/12)")
assert abs(float(sqrt(2 - sqrt(3))) - 0.5176380902) < 1e-9; ok += 1
eq(sqrt(1 - Rational(1, 4)), sqrt(3) / 2, "OH")
eq(Rational(1, 4) + (1 - sqrt(3) / 2) ** 2, 2 - sqrt(3), "AC^2")

# ---- nouveau-2 : courbes
eq(cos(0), 1, ""); eq(sin(0), 0, "")
sols(cos(x) - sin(x), -2 * pi, 2 * pi, {-7 * pi / 4, -3 * pi / 4, pi / 4, 5 * pi / 4}, "cos=sin [-2pi;2pi]")
X = np.linspace(-2 * np.pi, 2 * np.pi, 400001); Y = np.sin(X) - 0.3
nb = int((np.diff(np.sign(Y)) != 0).sum()); assert nb == 4, nb; ok += 1
eq(sin(pi / 2), 1, ""); eq(cos(pi), -1, "")

# ---- finition 2026-11-02 : valeurs portées sur les nouvelles figures
import math as _m
# 1390 : g(x) = 3 sin x + 2, A(0 ; 2), extremums, y = 7/2 en pi/6 et 5pi/6
g = 3 * sin(x) + 2
eq(g.subs(x, 0), 2, "g(0)"); eq(g.subs(x, pi / 2), 5, "g(pi/2)"); eq(g.subs(x, -pi / 2), -1, "g(-pi/2)")
eq(g.subs(x, pi / 6), Rational(7, 2), "g(pi/6)"); eq(g.subs(x, 5 * pi / 6), Rational(7, 2), "g(5pi/6)")
sols(g - Rational(7, 2), 0, 2 * pi, {pi / 6, 5 * pi / 6}, "g=7/2")
sols(2 * sin(x) - sqrt(3), 0, 2 * pi, {pi / 3, 2 * pi / 3}, "2sin=√3")
sols(2 * cos(x) + sqrt(2), -pi + Rational(1, 10**6), pi, {-3 * pi / 4, 3 * pi / 4}, "2cos+√2=0")
# 1387 2c : cos x = -1/2 dans ]-pi ; pi]
sols(2 * cos(x) + 1, -pi + Rational(1, 10**6), pi, {-2 * pi / 3, 2 * pi / 3}, "cos=-1/2")
# 1385 : pi/4 et symétriques de pi/6
eq(cos(pi / 4), sqrt(2) / 2, "cos pi/4"); eq(cos(-pi / 6), sqrt(3) / 2, ""); eq(sin(5 * pi / 6), Rational(1, 2), "")
# 1391 : symétries des points de pi/5 à 4pi/5
eq(cos(4 * pi / 5) + cos(pi / 5), 0, "cos 4pi/5"); eq(cos(3 * pi / 5) + cos(2 * pi / 5), 0, "cos 3pi/5")
eq(sin(4 * pi / 5) - sin(pi / 5), 0, "même ordonnée")
# 1388 : roue, positions à 21 m, courbe de h
th = symbols("th")
h = 15 - 12 * cos(th)
eq(h.subs(th, 2 * pi / 3), 21, "h(2pi/3)"); eq(h.subs(th, 4 * pi / 3), 21, "h(4pi/3)")
assert abs(_m.sqrt(144 - 36) - 12 * _m.sin(2 * _m.pi / 3)) < 1e-12; ok += 1   # abscisse de la nacelle à 21 m
eq((Rational(4, 3) - Rational(2, 3)) * 60, 40, "40 s")
for tt in (0, 1, 2):
    assert abs(15 - 12 * _m.cos(_m.pi * tt) - (3 if tt != 1 else 27)) < 1e-12; ok += 1
# nouveau-2 : abscisses des intersections avec y = 0,3 tracées sur la figure
for v in (_m.asin(0.3), _m.pi - _m.asin(0.3), _m.asin(0.3) - 2 * _m.pi, -_m.pi - _m.asin(0.3)):
    assert abs(_m.sin(v) - 0.3) < 1e-12 and -2 * _m.pi <= v <= 2 * _m.pi; ok += 1
assert abs(_m.asin(0.3) - 0.3047) < 1e-4 and abs(_m.pi - _m.asin(0.3) - 2.8369) < 1e-4; ok += 1
assert abs(_m.asin(0.3) - 2 * _m.pi + 5.9785) < 1e-4 and abs(-_m.pi - _m.asin(0.3) + 3.4463) < 1e-4; ok += 1

print(f"{ok} vérifications : tout est juste.")
