# -*- coding: utf-8 -*-
"""Vérification (sympy) de tous les résultats de la notion 159 « Géométrie repérée ».

    python verif_geometrie.py      -> « OK » si tout est juste
"""
from sympy import Rational as Q, sqrt, symbols, solve, expand, simplify, Eq, nsimplify

x, y, t = symbols("x y t", real=True)
NB = 0


def ok(cond, msg):
    global NB
    assert cond, msg
    NB += 1


def eq(a, b, msg):
    ok(simplify(a - b) == 0, f"{msg} : {a} != {b}")


def droite_normal(P, n):
    """Équation a x + b y + c (= 0) de la droite passant par P, de vecteur normal n."""
    return expand(n[0] * (x - P[0]) + n[1] * (y - P[1]))


def projete(M, a, b, c):
    """Projeté orthogonal de M sur ax + by + c = 0 (M + t n, n = (a ; b))."""
    tt = solve(a * (M[0] + t * a) + b * (M[1] + t * b) + c, t)[0]
    return (M[0] + tt * a, M[1] + tt * b)


def dist(P, R):
    return sqrt((P[0] - R[0]) ** 2 + (P[1] - R[1]) ** 2)


def ps(u, v):
    return u[0] * v[0] + u[1] * v[1]


def vec(P, R):
    return (R[0] - P[0], R[1] - P[1])


def cercle(expr):
    """Centre et r² de x² + y² + px + qy + s = 0."""
    p = expr.coeff(x, 1)
    q = expr.coeff(y, 1)
    s = expr.subs({x: 0, y: 0})
    a, b = -p / 2, -q / 2
    return (a, b), a ** 2 + b ** 2 - s


def sommet(a, b, c):
    al = Q(-b, 2 * a)
    return al, a * al ** 2 + b * al + c


# ------------------------------------------------------------------ cours
eq(droite_normal((1, 2), (2, 1)), 2 * x + y - 4, "cours I exemple")
# hauteur issue de A dans A(0;0) B(4;0) C(1;3) : normal BC(-3;3)
eq(droite_normal((0, 0), vec((4, 0), (1, 3))), -3 * x + 3 * y, "cours hauteur")
H = projete((4, 3), 2, 1, -4)
ok(H == (Q(6, 5), Q(8, 5)), "cours projeté")
eq(dist((4, 3), H), 7 * sqrt(5) / 5, "cours MH")
ok(abs(float(7 * sqrt(5) / 5) - 3.13) < 0.005, "cours MH approx")
eq(expand((x - 2) ** 2 - 4 + (y + 3) ** 2 - 9 - 3), x ** 2 + y ** 2 - 4 * x + 6 * y - 3, "cours cercle")
ok(cercle(x ** 2 + y ** 2 - 4 * x + 6 * y - 3) == ((2, -3), 16), "cours cercle centre")
ok(sommet(1, -4, 3) == (2, -1), "cours parabole")
eq(expand((x - 2) ** 2 - 1), x ** 2 - 4 * x + 3, "cours canonique")
# cours : cercle (x-1)² + (y+1)² = 25, tangente en A(4;3), point M(-2;3)
eq(expand((x - 1) ** 2 + (y + 1) ** 2 - 25), x ** 2 + y ** 2 - 2 * x + 2 * y - 23, "cours cercle développé")
ok(cercle(x ** 2 + y ** 2 - 2 * x + 2 * y - 23) == ((1, -1), 25), "cours cercle reconnu")
ok((4 - 1) ** 2 + (3 + 1) ** 2 == 25 and (-2 - 1) ** 2 + (3 + 1) ** 2 == 25, "cours A, M sur cercle")
eq(droite_normal((4, 3), (3, 4)), 3 * x + 4 * y - 24, "cours tangente")
# cours : perpendiculaire à d passant par M(4;3)
eq(droite_normal((4, 3), (-1, 2)), -x + 2 * y - 2, "cours perpendiculaire")
ok(solve([2 * x + y - 4, -x + 2 * y - 2], [x, y]) == {x: Q(6, 5), y: Q(8, 5)}, "cours système")
ok(Q(196, 25) + Q(49, 25) == Q(245, 25), "cours MH²")
# cours : vecteur directeur (-b ; a)
ok(ps((2, 1), (-1, 2)) == 0, "cours n.u")

# ------------------------------------------------------------------ 1411
ok(sommet(2, -8, 5) == (2, -3), "1411 P1")
ok(sommet(-1, 6, -4) == (3, 5), "1411 P2")
ok(sommet(3, 12, 7) == (-2, -5), "1411 P3")
f = lambda v: 2 * v ** 2 - 8 * v + 5
ok(f(1) == f(3) == -1, "1411 Q3")

# ------------------------------------------------------------------ 1407
eq(droite_normal((3, -2), (2, 5)), 2 * x + 5 * y + 4, "1407 a")
eq(droite_normal((-1, 4), (1, -3)), x - 3 * y + 13, "1407 b")
eq(droite_normal((0, 0), (4, 7)), 4 * x + 7 * y, "1407 c")
eq(droite_normal((1, 2), (4, 3)), 4 * x + 3 * y - 10, "1407 Q3")
ok(ps((4, 3), (3, -4)) == 0, "1407 directeur de d")

# ------------------------------------------------------------------ 1410
eq(expand((x - 2) ** 2 + (y + 3) ** 2 - 16), x ** 2 + y ** 2 - 4 * x + 6 * y - 3, "1410 Q2")
ok(cercle(x ** 2 + y ** 2 - 6 * x + 4 * y - 3) == ((3, -2), 16), "1410 3a")
ok(cercle(x ** 2 + y ** 2 + 2 * x - 8 * y + 17) == ((-1, 4), 0), "1410 3b")
ok(cercle(x ** 2 + y ** 2 - 4 * x + 2 * y + 10) == ((2, -1), -5), "1410 3c")

# ------------------------------------------------------------------ 1408
ok(2 * (-6) - 4 * (-3) == 0 and 2 * 1 != 5, "1408 a")
ok(1 * (-1) - 3 * 2 == -7, "1408 b det")
ok(solve([x + 2 * y - 3, 3 * x - y - 2], [x, y]) == {x: 1, y: 1}, "1408 Q2")
ok(ps((3, 2), (2, -3)) == 0, "1408 Q3")

# ------------------------------------------------------------------ 1409
eq(droite_normal((3, 1), (2, 1)), 2 * x + y - 7, "1409 perp")
ok(solve([x - 2 * y + 4, 2 * x + y - 7], [x, y]) == {x: 2, y: 3}, "1409 H")
ok(projete((3, 1), 1, -2, 4) == (2, 3), "1409 H bis")
eq(dist((3, 1), (2, 3)), sqrt(5), "1409 MH")
ok(ps(vec((3, 1), (2, 3)), (2, 1)) == 0, "1409 ortho")
ok(projete((0, 0), 5, 12, -13) == (Q(5, 13), Q(12, 13)), "1409 Q4 H")
eq(dist((0, 0), (Q(5, 13), Q(12, 13))), 1, "1409 Q4 OH")
ok(solve([5 * x + 12 * y - 13, 12 * x - 5 * y], [x, y]) == {x: Q(5, 13), y: Q(12, 13)}, "1409 Q4 syst")

# ------------------------------------------------------------------ 1412
A, B, C = (0, 0), (3, 4), (-4, 3)
ok(ps(vec(A, B), vec(A, C)) == 0, "1412 rect")
eq(dist(A, B), 5, "1412 AB")
I = (Q(-1, 2), Q(7, 2))
eq(dist(I, B) ** 2, Q(25, 2), "1412 R2")
eq(dist(I, A) ** 2, Q(25, 2), "1412 A sur cercle")
eq(dist(I, C) ** 2, Q(25, 2), "1412 C sur cercle")

# ------------------------------------------------------------------ 1406
ok(ps((3, -2), (2, 3)) == 0, "1406 Q2")
eq(droite_normal((2, -1), (3, -4)), 3 * x - 4 * y - 10, "1406 Q3")
ok(ps((4, 3), (3, -4)) == 0, "1406 n.d")

# ------------------------------------------------------------------ 1422 (DS, remplacé)
A, B, C = (-1, 5), (1, -3), (4, 0)
ok(ps(vec(C, A), vec(C, B)) == 0, "1422 rect C")
ok(ps(vec(A, B), vec(A, C)) != 0 and ps(vec(B, A), vec(B, C)) != 0, "1422 non rect A,B")
eq(dist(C, A), 5 * sqrt(2), "1422 CA")
eq(dist(C, B), 3 * sqrt(2), "1422 CB")
eq(dist(C, A) * dist(C, B) / 2, 15, "1422 aire")
eq(dist(A, B), 2 * sqrt(17), "1422 AB")
W = (0, 1)
for P in (A, B, C):
    eq(dist(W, P) ** 2, 17, "1422 cercle")
eq(expand(x ** 2 + (y - 1) ** 2 - 17), x ** 2 + y ** 2 - 2 * y - 16, "1422 développée")
eq(droite_normal(A, (4, 1)), 4 * x + y - 1, "1422 (AB)")
ok(4 * B[0] + B[1] - 1 == 0, "1422 B sur (AB)")
ok(ps(vec(A, B), (4, 1)) == 0, "1422 normal (AB)")
Hc = projete(C, 4, 1, -1)
ok(Hc == (Q(8, 17), Q(-15, 17)), "1422 H")
eq(dist(C, Hc), 15 * sqrt(17) / 17, "1422 CH")
eq(dist(A, B) * dist(C, Hc) / 2, 15, "1422 aire bis")
a, b, c = symbols("a b c")
s = solve([a - b + c - 5, a + b + c + 3, 16 * a + 4 * b + c], [a, b, c])
ok(s == {a: 1, b: -4, c: 0}, "1422 parabole")
ok(sommet(1, -4, 0) == (2, -4), "1422 sommet")
eq(dist(W, (2, -4)) ** 2, 29, "1422 S ext")

# ------------------------------------------------------------------ 1421 (DS)
ok(cercle(x ** 2 + y ** 2 - 6 * x + 4 * y - 12) == ((3, -2), 25), "1421 cercle")
A, B, C = (8, -2), (3, 5), (1, -3)
ok((8 - 3) ** 2 + 0 == 25, "1421 A sur C")
ok(ps(vec(A, B), vec(A, C)) == 28, "1421 en A")
ok(ps(vec(B, A), vec(B, C)) == 46, "1421 en B")
ok(ps(vec(C, A), vec(C, B)) == 22, "1421 en C")
eq(droite_normal(A, (1, 4)), x + 4 * y, "1421 hauteur")
eq(droite_normal(B, (4, -1)), 4 * x - y - 7, "1421 (BC)")
ok(4 * C[0] - C[1] - 7 == 0 and ps((4, -1), vec(B, C)) == 0, "1421 (BC) check")
Ha = projete(A, 4, -1, -7)
ok(Ha == (Q(28, 17), Q(-7, 17)), "1421 H")
ok(Ha[0] + 4 * Ha[1] == 0, "1421 H sur hauteur")
eq(dist(A, Ha), 27 * sqrt(17) / 17, "1421 AH")
ok(abs(float(27 * sqrt(17) / 17) - 6.55) < 0.005, "1421 AH approx")
ok(sommet(-1, 4, 5) == (2, 9), "1421 sommet")
eq(expand(-(x - 2) ** 2 + 9), -x ** 2 + 4 * x + 5, "1421 canonique")
ok(set(solve(-x ** 2 + 4 * x + 5, x)) == {-1, 5}, "1421 racines")

# ------------------------------------------------------------------ 1414
ok(cercle(x ** 2 + y ** 2 - 4 * x + 2 * y - 20) == ((2, -1), 25), "1414 cercle")
ok(5 ** 2 + 3 ** 2 - 20 + 6 - 20 == 0, "1414 A sur C")
eq(droite_normal((5, 3), (3, 4)), 3 * x + 4 * y - 27, "1414 tangente")
eq(dist((2, -1), (7, 4)), 5 * sqrt(2), "1414 OmegaM")
ok(abs(float(5 * sqrt(2)) - 7.07) < 0.005, "1414 approx")
ok(3 * 7 + 4 * 4 - 27 == 10, "1414 M pas sur T")
ok(solve(3 * x - 27, x) == [9], "1414 T coupe l'axe des abscisses en 9")

# ------------------------------------------------------------------ 1413
eq(droite_normal((4, 1), (-3, 2)), -3 * x + 2 * y + 10, "1413 d")
Hm = projete((4, 1), 2, 3, -6)
ok(Hm == (Q(42, 13), Q(-2, 13)), "1413 H")
ok(3 * Hm[0] - 2 * Hm[1] - 10 == 0, "1413 H sur d")
eq(dist((4, 1), Hm), 5 * sqrt(13) / 13, "1413 MH")
ok(abs(float(5 * sqrt(13) / 13) - 1.39) < 0.005, "1413 approx")
eq(dist((3, 0), (0, 2)), sqrt(13), "1413 AB")
eq(dist((3, 0), (0, 2)) * dist((4, 1), Hm) / 2, Q(5, 2), "1413 aire")
ok(abs((1 * 2 - 1 * (-3))) == 5, "1413 aire contrôle (déterminant)")

# ------------------------------------------------------------------ 1418
eq(expand((x - 2) * (x - 4)), x ** 2 - 6 * x + 8, "1418 facto")
ok(sommet(1, -6, 8) == (3, -1), "1418 sommet")

# ------------------------------------------------------------------ 1417
Ho = projete((1, 2), 1, 1, -6)
ok(Ho == (Q(5, 2), Q(7, 2)), "1417 H")
eq(dist((1, 2), Ho), 3 * sqrt(2) / 2, "1417 OmegaH")
ok(float(3 * sqrt(2) / 2) < 3 and abs(float(3 * sqrt(2) / 2) - 2.12) < 0.005, "1417 compar")
eq(expand((x - 1) ** 2 + (6 - x - 2) ** 2 - 9), 2 * x ** 2 - 10 * x + 8, "1417 substitution")
ok(set(solve((x - 1) ** 2 + (4 - x) ** 2 - 9, x)) == {1, 4}, "1417 racines")
ok(((1 + 4) / Q(2), (5 + 2) / Q(2)) == Ho, "1417 H milieu")

# ------------------------------------------------------------------ 1415
ok(sommet(-2, 12, -10) == (3, 8), "1415 sommet")
eq(expand(-2 * (x - 3) ** 2 + 8), -2 * x ** 2 + 12 * x - 10, "1415 canonique")
g = lambda v: -2 * v ** 2 + 12 * v - 10
ok(g(2) == g(4) == 6, "1415 Q6")

# ------------------------------------------------------------------ 1416
A, B, C = (-1, 2), (3, 4), (1, -2)
eq(dist(A, B), 2 * sqrt(5), "1416 AB")
eq(dist(A, C), 2 * sqrt(5), "1416 AC")
eq(dist(B, C), 2 * sqrt(10), "1416 BC")
ok(ps(vec(A, B), vec(A, C)) == 0, "1416 rect")
eq(droite_normal((1, 3), (4, 2)), 4 * x + 2 * y - 10, "1416 médiatrice")
for P in (A, B, C):
    eq(dist((2, 1), P) ** 2, 10, "1416 cercle")
ok(2 * 2 + 1 - 5 == 0, "1416 centre sur médiatrice")
eq(expand((x - 2) ** 2 + (y - 1) ** 2 - 10), x ** 2 + y ** 2 - 4 * x - 2 * y - 5, "1416 développée")

# ------------------------------------------------------------------ 1420
A, B, C = (1, 3), (5, 1), (3, -1)
eq(dist(A, B), 2 * sqrt(5), "1420 AB")
eq(dist(A, C), 2 * sqrt(5), "1420 AC")
eq(dist(B, C), 2 * sqrt(2), "1420 BC")
ok(ps(vec(A, B), vec(A, C)) == 16, "1420 A")
ok(ps(vec(B, A), vec(B, C)) == 4 and ps(vec(C, A), vec(C, B)) == 4, "1420 B, C")
eq(droite_normal((3, 2), (4, -2)), 4 * x - 2 * y - 8, "1420 m1")
eq(droite_normal((2, 1), (2, -4)), 2 * x - 4 * y, "1420 m2")
ok(solve([2 * x - y - 4, x - 2 * y], [x, y]) == {x: Q(8, 3), y: Q(4, 3)}, "1420 centre")
W = (Q(8, 3), Q(4, 3))
for P in (A, B, C):
    eq(dist(W, P) ** 2, Q(50, 9), "1420 rayon")

# ------------------------------------------------------------------ 1419
A, B, C, D = (1, 1), (5, 2), (4, 6), (0, 5)
ok(vec(A, B) == vec(D, C) == (4, 1), "1419 parallélogramme")
ok(((1 + 4) / Q(2), (1 + 6) / Q(2)) == ((5 + 0) / Q(2), (2 + 5) / Q(2)) == (Q(5, 2), Q(7, 2)), "1419 milieux")
eq(droite_normal(A, (5, -3)), 5 * x - 3 * y - 2, "1419 (AC)")
ok(5 * 4 - 3 * 6 - 2 == 0, "1419 C sur (AC)")
Hb = projete(B, 5, -3, -2)
ok(Hb == (Q(5, 2), Q(7, 2)), "1419 H = I")
eq(dist(B, Hb), sqrt(34) / 2, "1419 BH")
eq(dist(A, C), sqrt(34), "1419 AC")
eq(dist(A, C) * dist(B, Hb) / 2, Q(17, 2), "1419 aire ABC")
ok(ps(vec(A, C), vec(B, D)) == 0, "1419 diagonales perp")
eq(dist(A, B), sqrt(17), "1419 AB")
eq(dist(A, D), sqrt(17), "1419 AD")
eq(dist(A, C) * dist(B, D) / 2, 17, "1419 aire losange")

# ------------------------------------------------------------------ 1423 (examen, remplacé)
ok(cercle(x ** 2 + y ** 2 - 6 * x - 8 * y) == ((3, 4), 25), "1423 cercle")
ok(set(solve(x ** 2 - 6 * x, x)) == {0, 6} and set(solve(y ** 2 - 8 * y, y)) == {0, 8}, "1423 axes")
ok(((0 + 6) / Q(2), (8 + 0) / Q(2)) == (3, 4), "1423 diamètre")
eq(dist((6, 0), (0, 8)), 10, "1423 AB")
eq(droite_normal((0, 0), (3, 4)), 3 * x + 4 * y, "1423 tangente en O")
Hd = projete((3, 4), 3, 4, -50)
ok(Hd == (6, 8), "1423 H")
eq(dist((3, 4), Hd), 5, "1423 OmegaH = R")
ok((6 - 3) ** 2 + (8 - 4) ** 2 == 25, "1423 H sur C")
ok(sommet(-1, 6, 0) == (3, 9), "1423 sommet")
ok((3 - 3) ** 2 + (9 - 4) ** 2 == 25, "1423 S sur C")
ok(-0 ** 2 + 6 * 0 == 0 and -36 + 36 == 0, "1423 O et A sur P")
eq(droite_normal((3, 9), (0, 5)), 5 * y - 45, "1423 tangente en S")

# ------------------------------------------------------------------ nouveau-1
h = lambda v: -(v + 1) ** 2 + 4
ok(h(1) == 0 and h(-1) == 4, "nouveau-1 a = -1")
eq(expand(-(x + 1) ** 2 + 4), -x ** 2 - 2 * x + 3, "nouveau-1 développée")
ok(sommet(-1, -2, 3) == (-1, 4), "nouveau-1 sommet")
ok(set(solve(-x ** 2 - 2 * x + 3, x)) == {-3, 1}, "nouveau-1 racines")
ok(h(0) == 3 and h(-2) == 3, "nouveau-1 symétrique")
a_ = symbols("a_")
ok(solve(a_ * (1 + 1) ** 2 + 4, a_) == [-1], "nouveau-1 calcul de a")

# ------------------------------------------------------------------ compléments (énoncés réécrits)
ok(2 * 0 - 3 * Q(1, 3) + 1 == 0 and 4 * 0 - 6 * Q(1, 3) + 5 == 3, "1408 point test")
ok(2 * (-2) + 5 * 0 + 4 == 0, "1407 E sur Delta1")
eq(droite_normal((4, 0), (1, -4)), x - 4 * y - 4, "1422 perpendiculaire")
ok(Hc[0] - 4 * Hc[1] - 4 == 0, "1422 H sur perpendiculaire")
ok(abs(float(15 * sqrt(17) / 17) - 3.64) < 0.005, "1422 CH approx")
ok(Q(25, 9) + Q(25, 9) == Q(50, 9), "1420 r²")
eq(droite_normal((3, 2), (2, -1)), 2 * x - y - 4, "1420 m1 simplifiée")
eq(droite_normal((2, 1), (1, -2)), x - 2 * y, "1420 m2 simplifiée")
ok(set(solve(-2 * x ** 2 + 12 * x - 10, x)) == {1, 5}, "1415 racines")
ok(36 - 36 + 8 == 8, "1418 f(6)")
ok(set(solve(x ** 2 - 5 * x + 4, x)) == {1, 4} and (-5) ** 2 - 16 == 9, "1417 discriminant")
eq(dist((6, 0), (0, 8)), 10, "1423 AB = 2r")
ok(projete((5, 2), 5, -3, -2) == (Q(5, 2), Q(7, 2)), "1419 t = -1/2")
eq(droite_normal((1, 1), (5, -3)), 5 * x - 3 * y - 2, "1419 (AC)")
eq(dist((5, 2), (0, 5)), sqrt(34), "1419 BD")

# ---- finition 2026-11-02 : données des nouvelles figures
X, Y = symbols("X Y")
ok((2 * 3 + 5 * (-2) + 4 == 0) and (2 * (-2) + 5 * 0 + 4 == 0), "fig 1407 A et E sur Δ1")
ok(2 * (-2) + 5 * (-5) != 0 and (5 - 3, 3 - (-2)) == (2, 5), "fig 1407 n1 tracé de A(3;-2) à (5;3)")
ok(3 * (-1) - 4 * (-0.5) + 1 == 0 and 3 * 3 - 4 * 2.5 + 1 == 0 and (3 - (-1), 2.5 - (-0.5)) == (4, 3), "fig 1407 u porté par d")
s = solve([3 * X - 4 * Y + 1, 4 * X + 3 * Y - 10], [X, Y])
ok(s == {X: Q(37, 25), Y: Q(34, 25)} and 4 * 1 + 3 * 2 - 10 == 0, "fig 1407 pied (1,48 ; 1,36), M ∈ Δ")
ok(abs(4 / sqrt(2) - 2 * sqrt(2)) == 0 and (2 * sqrt(2)) ** 2 * 2 == 16, "fig 1410 rayon tracé de longueur 4")
ok(solve([X + 2 * Y - 3, 3 * X - Y - 2], [X, Y]) == {X: 1, Y: 1}, "fig 1408 K(1;1)")
ok(solve([3 * X + 2 * Y - 5, 2 * X - 3 * Y + 1], [X, Y]) == {X: 1, Y: 1} and 3 * 2 + 2 * (-3) == 0, "fig 1408 d1 ⊥ d2 en (1;1)")
ok((2.5 - 1, 2 - 1) == (1.5, 1.0) and (2 - 1, -0.5 - 1) == (1, -1.5), "fig 1408 n1 = (3;2)/2, n2 = (2;-3)/2")
ok(3 * 2 - 4 * (-1) - 10 == 0 and 3 * 6 - 4 * 2 - 10 == 0 and (5 - 2, -5 + 1) == (3, -4), "fig 1406 A, v, n")
fx = -2 * x ** 2 + 12 * x - 10
ok(expand(-2 * (x - 3) ** 2 + 8 - fx) == 0 and fx.subs(x, 2) == 6 and fx.subs(x, 4) == 6, "fig 1415 forme canonique")
ok(set(solve(fx, x)) == {1, 5} and fx.subs(x, 3) == 8, "fig 1415 racines et sommet")
g = -(x + 1) ** 2 + 4
ok(expand(g) == -x ** 2 - 2 * x + 3 and set(solve(g, x)) == {-3, 1}, "fig nouveau-1 B(-3;0)")
ok(g.subs(x, 0) == 3 and g.subs(x, -2) == 3 and g.subs(x, -1) == 4, "fig nouveau-1 C, C', S")

print(f"OK : {NB} vérifications")
