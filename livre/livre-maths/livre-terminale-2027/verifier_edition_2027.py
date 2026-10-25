"""Contrôles de l'édition 2027-2028 du livre de Terminale.

1. Structure : nombre d'exercices de chaque chapitre = plan.tex ; corrigés numérotés 1..n dans le même ordre.
2. Sujets type bac : quatre exercices de 4 à 8 points totalisant 18 points (2 points de maîtrise de la langue),
   barème détaillé de chaque corrigé égal au total de l'exercice, en-têtes cohérents avec les énoncés.
3. Calculs des contenus nouveaux (chapitres 6, 13 et 23), vérifiés avec SymPy.

Usage, depuis livre-terminale-2027 : python -I -X utf8 verifier_edition_2027.py
"""
import re
from fractions import Fraction
from pathlib import Path

import sympy as sp

R = Path(__file__).resolve().parent
OK = []


def ok(msg):
    OK.append(msg)


# ---------------------------------------------------------------- 1. structure
plan = re.findall(r"\\otPlanChap\{(\d+)\}\{([^}]*)\}\{(\d+)\}", (R / "plan.tex").read_text(encoding="utf-8"))
chap_files = sorted((R / "chapitres").glob("*.tex"))
cor_files = sorted((R / "corriges").glob("*.tex"))
assert len(plan) == 23 == len(chap_files) == len(cor_files), (len(plan), len(chap_files), len(cor_files))
for (num, titre, n), fc, fk in zip(plan, chap_files, cor_files):
    tc = fc.read_text(encoding="utf-8")
    tk = fk.read_text(encoding="utf-8")
    m = re.search(r"\\begin\{ouverture\}(?:\[[^\]]*\])?\{(\d+)\}\{([^}]*)\}", tc)
    assert m and m.group(1) == num and m.group(2) == titre, (fc.name, m.groups() if m else None)
    n_exo = len(re.findall(r"\\begin\{exercice\}", tc))
    nums = [int(x) for x in re.findall(r"\\begin\{corrige\}\{(\d+)\}", tk)]
    assert n_exo == int(n), (fc.name, n_exo, n)
    assert nums == list(range(1, int(n) + 1)), (fk.name, nums)
    titres_e = re.findall(r"\\begin\{exercice\}(?:\[\d\])?\{(.*)\}\s*$", tc, flags=re.M)
    titres_c = re.findall(r"\\begin\{corrige\}\{\d+\}\{(.*)\}\s*$", tk, flags=re.M)
    norm = lambda s: re.sub(r"\\enspace\\otNouveau", "", s).strip()
    assert [norm(t) for t in titres_e] == [norm(t) for t in titres_c], (fc.name, titres_e, titres_c)
ok(f"Structure : 23 chapitres, {sum(int(p[2]) for p in plan)} exercices, corrigés appariés (numéros et titres).")

# ---------------------------------------------------------------- 2. sujets type bac
def val(s):
    return Fraction(s.replace(",", "."))

for k in range(1, 11):
    ts = (R / "bac" / f"sujet-{k:02d}.tex").read_text(encoding="utf-8")
    tk = (R / "bac" / f"corrige-{k:02d}.tex").read_text(encoding="utf-8")
    entete = re.search(r"\\sujetBac\{%d\}\{([^\n]*)\}\n" % k, ts).group(1).split(",")
    pts_entete = [int(x.rsplit("/", 1)[1]) for x in entete]
    pts_enonce = [int(x) for x in re.findall(r"\\begin\{exoBac\}\{(\d+)\}", ts)]
    blocs = re.split(r"\\begin\{corrigeBac\}\{(\d+)\}", tk)[1:]
    pts_corrige = [int(blocs[i]) for i in range(0, len(blocs), 2)]
    assert pts_entete == pts_enonce == pts_corrige, (k, pts_entete, pts_enonce, pts_corrige)
    assert len(pts_enonce) == 4 and sum(pts_enonce) == 18 and all(4 <= p <= 8 for p in pts_enonce), (k, pts_enonce)
    for i in range(0, len(blocs), 2):
        total = int(blocs[i])
        detail = sum(val(v) for v in re.findall(r"\\pts\{([0-9]+(?:,[0-9]+)?) pt\}", blocs[i + 1]))
        assert detail == total, (k, i // 2 + 1, detail, total)
    assert "Aucune justification" not in ts, k
ok("Sujets type bac : 4 exercices de 4 à 8 points, 18 points + 2 points de langue, barèmes détaillés exacts, QCM justifiés.")

# ---------------------------------------------------------------- 3a. chapitre 6
x = sp.symbols("x", real=True)
pi = sp.pi
assert sp.sin(pi / 6) == sp.Rational(1, 2) == sp.sin(5 * pi / 6) and sp.sin(-pi / 6) == -sp.Rational(1, 2)
assert sp.simplify(sp.sin(pi - x) - sp.sin(x)) == 0
sol = sp.solveset(sp.Eq(sp.cos(x), sp.Rational(1, 2)), x, sp.Interval(-pi, pi))
assert sol == sp.FiniteSet(-pi / 3, pi / 3), sol
attendu = sp.Union(sp.Interval(-pi, -pi / 3), sp.Interval(pi / 3, pi))
for j in range(-3000, 3001):  # contrôle sur une grille fine de [-pi ; pi] (solveset est incomplet ici)
    xv = sp.pi * sp.Rational(j, 3000)
    assert (sp.cos(xv).evalf() <= 0.5 + 1e-12) == bool(attendu.contains(xv)), xv
f, g, h, k = sp.cos(2 * x), x * sp.sin(x), sp.sin(x) + sp.cos(x), sp.sin(x) * sp.cos(x)
assert sp.simplify(f.subs(x, -x) - f) == 0 and sp.simplify(g.subs(x, -x) - g) == 0
assert sp.simplify(k.subs(x, -x) + k) == 0
assert h.subs(x, pi / 4) == sp.sqrt(2) and sp.simplify(h.subs(x, -pi / 4)) == 0
assert sp.simplify(f.subs(x, x + pi) - f) == 0 and sp.simplify(k.subs(x, x + pi) - k) == 0
assert sp.simplify(h.subs(x, x + 2 * pi) - h) == 0
assert sp.maximum(k, x, sp.Interval(0, 2 * pi)) == sp.Rational(1, 2)
assert sp.maximum(h, x, sp.Interval(0, 2 * pi)) == sp.sqrt(2)
assert f.subs(x, 0) == 1 and g.subs(x, 0) == 0 and k.subs(x, 0) == 0 and h.subs(x, 0) == 1
ok("Chapitre 6 : exercices 3 et 4 (valeurs, équation, inéquation, parités, périodes, maxima).")

# ---------------------------------------------------------------- 3b. chapitre 13, exercice 9
n1, n2, u = sp.Matrix([1, -2, 2]), sp.Matrix([2, 2, 1]), sp.Matrix([-2, 1, 2])
A, M = sp.Matrix([1, 0, 1]), sp.Matrix([4, 0, 4])
P1 = lambda P: P[0] - 2 * P[1] + 2 * P[2] - 3
P2 = lambda P: 2 * P[0] + 2 * P[1] + P[2] - 3
assert n1.dot(n2) == 0 and P1(A) == 0 and P2(A) == 0 and u.dot(n1) == 0 and u.dot(n2) == 0
t = sp.symbols("t")
t1 = sp.solve(P1(M + t * n1), t)[0]
t2 = sp.solve(P2(M + t * n2), t)[0]
H1, H2 = M + t1 * n1, M + t2 * n2
assert t1 == -1 and t2 == -1 and list(H1) == [3, 2, 2] and list(H2) == [2, -2, 3]
assert (H1 - M).norm() == 3 and (H2 - M).norm() == 3
assert H1 - M == A - H2 and (A - H1).dot(M - H1) == 0 and (A - H1).norm() == 3
assert (M - A).dot(u) == 0 and (M - A).norm() == 3 * sp.sqrt(2)
assert P1(A + t * u) == 0 and P2(A + t * u) == 0
ok("Chapitre 13 : exercice 9 (plans perpendiculaires, projetés, carré, distance 3√2).")

# ---------------------------------------------------------------- 3c. chapitre 23
E = set(range(1, 11))
Aset = {n for n in E if n % 2 == 0}
Bset = {n for n in E if n % 3 == 0}
assert Aset == {2, 4, 6, 8, 10} and Bset == {3, 6, 9} and Aset & Bset == {6}
assert Aset | Bset == {2, 3, 4, 6, 8, 9, 10} and E - Aset == {1, 3, 5, 7, 9}
assert len(Aset | Bset) == len(Aset) + len(Bset) - len(Aset & Bset) == 7
assert E - (Aset | Bset) == (E - Aset) & (E - Bset) == {1, 5, 7}
assert [n for n in range(1, 11) if n % 2 == 0 or n % 3 == 0] == [2, 3, 4, 6, 8, 9, 10]
assert sp.Rational(1, 2) ** 2 < sp.Rational(1, 2) and 0 ** 2 == 2 * 0 and 2 ** 2 == 2 * 2
assert not (2 ** 2 > 2 ** 2) and 2 ** 3 < 3 ** 2
X = sp.symbols("X", positive=True)
assert sp.simplify(X + 1 / X - 2 - (X - 1) ** 2 / X) == 0
for n in range(0, 200):
    assert (n * n + n + 1) % 2 == 1 and (n * (n + 1) * (2 * n + 1)) % 3 == 0 and (4 ** n + 2) % 3 == 0
    assert (10 ** n + 1) % 9 == 2
    if n % 2 == 1:
        assert (n * n - 1) % 8 == 0
    if n >= 4:
        assert 2 ** n >= n * n
assert [n for n in range(0, 10) if not 2 ** n >= n * n] == [3]
xr = sp.symbols("x", real=True)
assert sp.solveset(sp.Abs(xr - 1) + sp.Abs(xr + 2) - 5, xr, sp.S.Reals) == sp.FiniteSet(-3, 2)
assert sp.solveset(sp.sqrt(xr + 2) - xr, xr, sp.S.Reals) == sp.FiniteSet(2)
assert sp.solveset(sp.log(xr) + sp.log(xr - 2) - sp.log(3), xr, sp.Interval.open(2, sp.oo)) == sp.FiniteSet(3)
assert sp.simplify(sp.exp(2 * xr) - 3 * sp.exp(xr) + 2 - (sp.exp(xr) - 1) * (sp.exp(xr) - 2)) == 0
assert sp.solveset(sp.exp(2 * xr) - 3 * sp.exp(xr) + 2 <= 0, xr, sp.S.Reals) == sp.Interval(0, sp.log(2))
nn = sp.symbols("n", integer=True)
assert sp.expand(nn ** 2 - 3 * nn - (nn - 3) - (nn - 1) * (nn - 3)) == 0
assert sp.expand(2 * nn ** 2 - (nn + 1) ** 2 - ((nn - 1) ** 2 - 2)) == 0
assert sp.expand(4 ** (nn + 1) + 2 - (4 * (4 ** nn + 2) - 6)) == 0
assert sp.expand(10 ** (nn + 1) + 1 - (10 * (10 ** nn + 1) - 9)) == 0
fx = xr * sp.exp(-xr)
assert sp.simplify(sp.diff(fx, xr) - (1 - xr) * sp.exp(-xr)) == 0 and fx.subs(xr, 1) == sp.exp(-1)
gx = 1 - sp.exp(-xr)
assert sp.diff(gx, xr) == sp.exp(-xr) and sp.limit(gx, xr, -sp.oo) == -sp.oo and sp.limit(gx, xr, sp.oo) == 1
lx = sp.log(xr) - xr + 1
assert sp.simplify(sp.diff(lx, xr) - (1 - xr) / xr) == 0 and lx.subs(xr, 1) == 0
assert sp.maximum(lx, xr, sp.Interval.open(0, sp.oo)) == 0
assert sp.diff((xr - 1) ** 3, xr).subs(xr, 1) == 0
ok("Chapitre 23 : ensembles, contre-exemples, disjonctions, récurrences, équations et inégalités vérifiés.")

for m in OK:
    print("OK  " + m)
