# -*- coding: utf-8 -*-
"""Vérification (sympy) de tous les résultats du cours, de la fiche et des exercices
de la notion 102 « Nombres complexes ».  python verif_nombres-complexes.py"""
from sympy import (I, sqrt, pi, exp, cos, sin, simplify, expand, symbols, Abs, arg, conjugate,
                   Rational as R, binomial, solve, Poly, nsimplify, expand_complex, re, im, Eq)

ok = 0
def eq(a, b, nom):
    global ok
    d = simplify(expand_complex(expand(a - b)))
    if d != 0 and not d.free_symbols:  # identité trigonométrique non simplifiée : contrôle à 50 chiffres
        d = 0 if abs(d.evalf(50)) < 1e-40 else d
    assert d == 0, f"ÉCHEC {nom} : {a} != {b} (diff {d})"
    ok += 1

def argu(z, theta, nom):
    """theta est un argument de z (modulo 2pi)."""
    global ok
    w = simplify(expand_complex(z / Abs(z)))
    eq(w, cos(theta) + I * sin(theta), nom)

x, y, t, a, b = symbols("x y t a b", real=True)
z = x + I * y

# ------------------------------------------------------------------ COURS
eq((2 + 3*I) * (1 - 2*I), 8 - I, "produit")
eq(I**2026, -1, "i^2026")
eq((1 + I)**4, -4, "binome (1+i)^4")
eq((3 + 4*I) / (1 - 2*I), -1 + 2*I, "quotient cours")
eq((1 - I) / (2 + 3*I), R(-1, 13) - R(5, 13)*I, "az=b")
zz = 1 - 4*I
eq(zz + 2*conjugate(zz), 3 + 4*I, "z+2conj z")
eq((5 - I) - (1 + 2*I), 4 - 3*I, "vecteur AB")
eq(((1 + 2*I) + (5 - I)) / 2, 3 + I/2, "milieu")
eq(Abs((3 + 4*I) * (1 - I)), 5*sqrt(2), "module produit")
eq(Abs((1 + I)**10), 32, "module puissance")
eq(Abs(R(3, 5) + R(4, 5)*I), 1, "U")
eq(1 / (R(3, 5) + R(4, 5)*I), R(3, 5) - R(4, 5)*I, "1/z = conj")
# médiatrice |z-2i| = |z+2|  <=>  y = -x
eq(expand(x**2 + (y-2)**2 - (x+2)**2 - y**2), -4*y - 4*x, "médiatrice cours")
argu(-1 + I*sqrt(3), 2*pi/3, "arg -1+i√3"); eq(Abs(-1 + I*sqrt(3)), 2, "mod -1+i√3")
argu(1 - I, -pi/4, "arg 1-i")
argu(-1 - I, -3*pi/4, "arg -1-i")
argu(-sqrt(3) + I, 5*pi/6, "arg -√3+i"); eq(Abs(-sqrt(3) + I), 2, "mod -√3+i")
eq(4*(cos(-pi/3) + I*sin(-pi/3)), 2 - 2*sqrt(3)*I, "trigo -> alg")
eq(-2*(cos(pi/6) + I*sin(pi/6)), 2*(cos(7*pi/6) + I*sin(7*pi/6)), "module négatif")
eq(cos(pi/12), (sqrt(2) + sqrt(6))/4, "cos pi/12")
eq((1 + I)**8, 16, "(1+i)^8")
eq(sqrt(2)*exp(I*pi/4), 1 + I, "1+i expo")
eq((1 + I*sqrt(3)) / (1 - I), sqrt(2)*exp(7*I*pi/12), "quotient expo")
eq(cos(t)**3, cos(3*t)/4 + 3*cos(t)/4, "linéarisation cos^3")
eq(cos(3*t), 4*cos(t)**3 - 3*cos(t), "cos 3t")
eq(sin(3*t), 3*sin(t) - 4*sin(t)**3, "sin 3t")
eq(expand((cos(t) + I*sin(t))**3), cos(t)**3 + 3*I*cos(t)**2*sin(t) - 3*cos(t)*sin(t)**2 - I*sin(t)**3, "Moivre dev")
w = symbols("w")
s = solve(w**2 - 2*w + 5); assert set(s) == {1 - 2*I, 1 + 2*I}; ok += 1
eq(expand((w - 1 + 2*I) * (w - 1 - 2*I)), w**2 - 2*w + 5, "factorisation")
eq(expand((w - 2) * (w**2 + 2*w + 4)), w**3 - 8, "z^3-8")
assert set(solve(w**3 - 8)) == {2, -1 + I*sqrt(3), -1 - I*sqrt(3)}; ok += 1
P = w**3 - 3*w**2 + 4*w - 2
eq(P.subs(w, 1), 0, "P(1)")
eq(expand((w - 1) * (w**2 - 2*w + 2)), P, "factorisation P")
assert set(solve(P)) == {1, 1 + I, 1 - I}; ok += 1
A, B, C = 1 + I, 3 + 2*I, -1 + 5*I
eq((C - A) / (B - A), 2*I, "quotient géométrie")
eq(Abs(C - A), 2*Abs(B - A), "AC = 2AB")
j = exp(2*I*pi/3)
eq(j, -R(1, 2) + sqrt(3)/2*I, "j"); eq(j**2, conjugate(j), "j^2 = conj j"); eq(1 + j + j**2, 0, "1+j+j^2")
for n in range(2, 9):
    om = exp(2*I*pi/n)
    eq(sum(om**k for k in range(n)), 0, f"somme U_{n}")
    eq(Abs(om - 1), 2*sin(pi/n), f"côté polygone {n}")
eq(2*sin(pi/6), 1, "hexagone")
for k, v in ((0, 1 + I*sqrt(3)), (1, -2), (2, 1 - I*sqrt(3))):
    eq(2*exp(I*(pi + 2*k*pi)/3), v, f"z^3=-8 k={k}"); eq(v**3, -8, f"(z_{k})^3")

# ------------------------------------------------------------------ EXERCICES
# 955
z1, z2, z3 = 3 + 4*I, 1 - 2*I, -2 + 5*I
eq(Abs(z1), 5, "955 q1"); eq(Abs(z2), sqrt(5), "955 q1b")
eq(conjugate(z3), -2 - 5*I, "955 q2")
eq(z1/z2, -1 + 2*I, "955 q3"); eq(1/z1, R(3, 25) - R(4, 25)*I, "955 q4"); eq(z1*conjugate(z1), 25, "955 q5")
# 954
z1, z2, z3, z4 = 2 + 3*I, -1 + 4*I, 5 - 2*I, 3*I
eq(z1 + z2, 1 + 7*I, "954 q1"); eq(z1 - z3, -3 + 5*I, "954 q2"); eq(z1*z2, -14 + 5*I, "954 q3")
eq(z2*conjugate(z2), 17, "954 q5"); eq(Abs(z2)**2, 17, "954 q5b")
# 1133
f = lambda u: ((3 + I)*u + (3 - I)*conjugate(u)) / 6
eq(f(I), -R(1, 3), "1133 A'"); eq(f(2 + I), R(5, 3), "1133 B'"); eq(f(-1 + 3*I), -2, "1133 C'")
eq(f(z), x - y/3, "1133 q2")
eq((f(z) - z) / (1 + 3*I), -y/3, "1133 q5")
eq(f(3 + 2*I), R(7, 3), "1133 figure N(3;2) -> N'(7/3;0)")
# 963
eq(expand((x-1)**2 + (y+1)**2 - (x+2)**2 - (y-1)**2), -(6*x - 4*y + 3), "963 q2")
eq(6*R(-1, 2) + 3, 0, "963 milieu")
eq(Abs(z)**2 - (z + conjugate(z)), (x - 1)**2 + y**2 - 1, "963 q5")
# 958
for (aa, bb, cc), sols in (((1, -2, 5), {1 - 2*I, 1 + 2*I}), ((1, 4, 13), {-2 - 3*I, -2 + 3*I}),
                           ((2, -6, 5), {R(3, 2) - I/2, R(3, 2) + I/2})):
    S = solve(aa*w**2 + bb*w + cc); assert set(S) == sols, S; ok += 1
    eq(sum(S), R(-bb, aa), f"958 somme {aa,bb,cc}"); eq(S[0]*S[1], R(cc, aa), f"958 produit {aa,bb,cc}")
# 961
z1 = -1 + I*sqrt(3)
eq(z1, 2*exp(2*I*pi/3), "961 q1"); eq(z1**10, -512 + 512*sqrt(3)*I, "961 q2")
eq(((1 + I)/(1 - I))**20, 1, "961 q5"); eq((1 + I)/(1 - I), I, "961 quotient")
# 956
argu(1 + I, pi/4, "956 z1"); argu(sqrt(3) + I, pi/6, "956 z2")
argu(-2 + 2*I, 3*pi/4, "956 z3"); eq(Abs(-2 + 2*I), 2*sqrt(2), "956 |z3|")
argu(-sqrt(3) + I, 5*pi/6, "956 z4")
# 957
z1, z2 = 1 + I, sqrt(3) + I
eq(z1**4, -4, "957 q2"); eq(z1**8, 16, "957 q3"); eq(z2**6, -64, "957 q4"); eq((z1*z2)**3, -16 - 16*I, "957 q5")
eq((2*sqrt(2))**3, 16*sqrt(2), "957 (2√2)^3")
argu(z1*z2, 5*pi/12, "957 arg produit")
# 960
for k in range(3):
    eq(exp(2*I*k*pi/3)**3, 1, f"960 U3 {k}")
eq(exp(4*I*pi/3), -R(1, 2) - sqrt(3)/2*I, "960 j^2")
eq(sum(exp(I*k*pi/2) for k in range(4)), 0, "960 somme U4")
# 962
zA, zB, zC = 1, I, -I
q = (zB - zA) / (zC - zA)
eq(q, -I, "962 q1"); eq(q, exp(-I*pi/2), "962 expo"); eq(Abs(q), 1, "962 q3")
eq(Abs(zC - zB), 2, "962 BC"); eq(Abs(zB - zA)**2 + Abs(zC - zA)**2, 4, "962 Pythagore")
zM = zA + exp(I*pi/3)*(zB - zA)
eq(zM, (1 - sqrt(3))/2*(1 + I), "962 q5"); eq(Abs(zM - zA), Abs(zB - zA), "962 AM=AB")
argu((zM - zA)/(zB - zA), pi/3, "962 angle pi/3")
# 959
zA, zB, zC = 1 + 2*I, 3 - I, -2 + 3*I
eq((zA + zB)/2, 2 + I/2, "959 q1"); eq(Abs(zB - zA), sqrt(13), "959 q2")
eq(expand((x-1)**2 + (y-2)**2 - (x-3)**2 - (y+1)**2), 4*x - 6*y - 5, "959 q4")
eq(zC - zB + zA, -4 + 6*I, "959 q5")

# Finition 2026-11-02 : valeurs écrites sur les nouvelles figures
eq(Abs(3 + 4*I), 5, "fig ex955_module |z1|"); eq(Abs(1 - 2*I), sqrt(5), "fig ex955_module |z2|")
for z, zb in ((3 + 4*I, 3 - 4*I), (1 - 2*I, 1 + 2*I), (-2 + 5*I, -2 - 5*I)):
    eq(conjugate(z), zb, "fig ex955_conjugues")
eq((2 + 3*I) + (-1 + 4*I), 1 + 7*I, "fig ex954_somme")
eq(re(2 + 3*I), 2, "fig ex954 Re"); eq(im(2 + 3*I), 3, "fig ex954 Im z1"); eq(im(3*I), 3, "fig ex954 Im z4")
for k, v in ((1, 1 + I), (2, 2*I), (3, -2 + 2*I), (4, -4)):
    eq(expand((1 + I)**k), v, f"fig ex957 z1^{k}")
    eq(Abs((1 + I)**k), sqrt(2)**k, f"fig ex957 module {k}")
for k, v in ((1, pi/4), (2, pi/2), (3, 3*pi/4), (4, pi)):
    argu((1 + I)**k, v, f"fig ex957 arg {k}")

print(f"{ok} vérifications : toutes justes")
