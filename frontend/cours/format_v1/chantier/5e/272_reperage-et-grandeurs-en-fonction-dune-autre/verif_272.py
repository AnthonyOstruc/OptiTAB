# -*- coding: utf-8 -*-
"""Vérification exacte (sympy) de la notion 272 (5e) : réponses des exercices, cours, fiche,
et concordance des figures (DONNEES et code TikZ de figures/figures.py) avec les énoncés.

Lancement : python verif_272.py   (depuis le dossier de la notion)
"""
import importlib.util
import re
import sys
from pathlib import Path

from sympy import Rational as R, Symbol, solve, sqrt, Eq, nsimplify

ICI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("fig272", ICI / "figures" / "figures.py")
FIG = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FIG)
D, F = FIG.DONNEES, FIG.FIGURES

EX = (ICI / "exercices.txt").read_text(encoding="utf-8")
COURS = (ICI / "cours_267.txt").read_text(encoding="utf-8")
FICHE = (ICI / "fiche_187.txt").read_text(encoding="utf-8")

n_ok = 0
echecs = []


def ok(cond, msg):
    global n_ok
    if cond:
        n_ok += 1
    else:
        echecs.append(msg)


def interp(pts, x):
    """Valeur exacte d'une ligne brisée (liste de points triés en abscisse) en x."""
    x = R(x)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        x0, y0, x1, y1 = R(x0), R(y0), R(x1), R(y1)
        if x0 <= x <= x1 and x1 != x0:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    raise ValueError(x)


def antecedents(pts, y):
    """Toutes les abscisses où la ligne brisée vaut y (segments non horizontaux)."""
    y = R(y)
    out = set()
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        x0, y0, x1, y1 = R(x0), R(y0), R(x1), R(y1)
        if y0 == y1:
            if y0 == y:
                out.add(("palier", x0, x1))
            continue
        if min(y0, y1) <= y <= max(y0, y1):
            out.add(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
    return out


def bloc(ident):
    m = re.search(r"Id: %s\n(.*?)\n===\n" % ident, EX, re.S)
    assert m, ident
    return m.group(1)


def dans(ident, *morceaux):
    b = bloc(ident)
    for t in morceaux:
        ok(t in b, "Id %s : texte attendu absent : %r" % (ident, t))


def tikz_contient(nom, *morceaux):
    for t in morceaux:
        ok(t in F[nom], "figure %s : %r absent" % (nom, t))


t, n, c, L, m, d = (Symbol(s) for s in "tncLmd")

# ======================================================================= COURS ET FICHE
asc = D["ascenseur"]
ok(interp(asc, 10) == 15, "ascenseur 10 s")
ok(antecedents(asc, 45) == {45, 80}, "ascenseur 45 m : %s" % antecedents(asc, 45))
ok(max(y for _, y in asc) == 60 and [x for x, y in asc if y == 60] == [55, 70], "ascenseur maximum")
ok(min(y for _, y in asc) == 0, "ascenseur minimum")
ok(asc[1] == (20, 30) and asc[2] == (35, 30), "ascenseur arrêt 20-35 s à 30 m")
for p in ["$15$ m", "$45$ s", "$80$ s", "$60$ m", "entre $55$ s et $70$ s", "De $20$ à $35$ s", "$110$ s"]:
    ok(p in COURS, "cours : %r" % p)
ok(D["ressort"] == [(0, 12), (1, 15), (2, 18), (3, 21), (4, 24)], "ressort données")
for mm, LL in D["ressort"]:
    ok(12 + 3 * mm == LL, "ressort formule %s" % mm)
    ok(("$%d$" % LL) in COURS, "cours tableau ressort %s" % LL)
ok(R(15, 1) == 15 and R(18, 2) == 9, "cours quotients ressort")
ok(r"\dfrac{15}{1} = 15" in COURS and r"\dfrac{18}{2} = 9" in COURS, "cours quotients écrits")
ok("=12+3*A2" in F["cours_tableur"] and "`=12+3*A2`" in COURS and "`=12+3*A2`" in FICHE, "tableur cours / fiche")
ok(all(2 * mm == p for mm, p in D["pommes"]), "pommes proportionnelles")
ok("{2*x}" in F["cours_proportionnalite"] and "{12+3*x}" in F["cours_proportionnalite"], "figure proportionnalité")
ok("{12+3*x}" in F["cours_ressort"], "figure ressort")
for p in ["$15$ m", "$45$ s", "$80$ s", "$60$ m", "$0$ m", "$L = 12 + 3 \\times 2 = 18$", "$12$ cm"]:
    ok(p in FICHE, "fiche : %r" % p)

# ======================================================================= 2940 cuve
V = D["cuve"]
ok(V(4) == 10 and V(10) == 25 and V(12) == 30 and V(0) == 0, "cuve lectures")
ok(solve(Eq(R(5, 2) * t, 15), t) == [6], "cuve 15 L")
tab = {0: 0, 2: 5, 4: 10, 6: 15, 8: 20, 12: 30}
ok(all(R(5, 2) * k == v for k, v in tab.items()), "cuve tableau")
ok(all(R(v, k) == R(5, 2) for k, v in tab.items() if k), "cuve quotients 2,5")
tikz_contient("ex2940_enonce", "{2.5*x}", "domain=0:12", "xtick={2,4,6,8,10,12}", "ytick={5,10,15,20,25,30}")
tikz_contient("ex2940_corrige", r"\lirev{4}{10}", r"\lirev{10}{25}", r"\liry{6}{15}", r"\lirex{6}{15}")
dans(2940, "$10$ L", "$25$ L", "$6$ min", "$0$ | $5$ | $10$ | $15$ | $20$ | $30$", "$2{,}5$",
     r"$5 \div 2 = 2{,}5", r"30 \div 12 = 2{,}5")

# ======================================================================= 2938 température
T = D["temperature"]
ok(dict(T)[10] == 9 and dict(T)[18] == 12, "température 10 h / 18 h")
ok(antecedents(T, 9) == {10, 20}, "température 9 °C : %s" % antecedents(T, 9))
ok(max(T, key=lambda p: p[1]) == (14, 16) and min(T, key=lambda p: p[1]) == (6, 3), "max / min")
ok(sum(1 for _, y in T if y == 16) == 1 and sum(1 for _, y in T if y == 3) == 1, "max / min uniques")
ys = [y for _, y in T]
ok(all(a > b for a, b in zip(ys[0:4], ys[1:4])), "diminue 0-6 h")
ok(all(a < b for a, b in zip(ys[3:8], ys[4:8])), "augmente 6-14 h")
ok(all(a > b for a, b in zip(ys[7:], ys[8:])), "diminue 14-24 h")
ok(16 - 3 == 13, "écart")
ok(interp(T, 11) == 11, "estimation à 11 h")
tikz_contient("ex2938_corrige", r"\lirev{18}{12}", r"\lirex{10}{9}", r"\lirex{20}{9}", r"\pv{14}{16}", r"\pv{6}{3}")
dans(2938, "$9$ °C à $10$ h et $12$ °C à $18$ h", "à $10$ h et à $20$ h", "$16$ °C à $14$ h", "$3$ °C à $6$ h",
     "$16 - 3 = 13$", "$11$ °C")

# ======================================================================= 2937 parc de loisirs
Pn = lambda k: 3 + 2 * k
ok(D["parcours"] == [(k, Pn(k)) for k in range(7)], "parcours données")
ok([Pn(k) for k in range(7)] == [3, 5, 7, 9, 11, 13, 15], "parcours tableau")
nmax = max(k for k in range(20) if Pn(k) <= 12)
ok(nmax == 4 and 12 - Pn(4) == 1 and Pn(5) == 13, "parcours budget")
tikz_contient("ex2937_corrige", "(axis cs:0,12)", "(axis cs:4,11) circle")
ok("addplot" not in F["ex2937_corrige"] and r"\draw[ligne]" not in F["ex2937_corrige"], "parcours : points non reliés")
dans(2937, "$P = 3 + 2n$", "$3$ ; $5$ ; $7$ ; $9$ ; $11$ ; $13$ ; $15$", "$4$ activités", "$12 - 11 = 1$")

# ======================================================================= 2946 carré
A = lambda x: x * x
ok(D["carre"] == [(k, k * k) for k in range(6)], "carré données")
ok(A(R(5, 2)) == R(25, 4), "carré 2,5 → 6,25")
racine = [s for s in solve(Eq(c ** 2, 20), c) if s > 0][0]
ok(racine == 2 * sqrt(5) and abs(float(racine) - 4.4721) < 1e-4, "carré 20 cm² → √20")
ok(abs(float(racine) - 4.5) < 0.05 and A(R(9, 2)) == R(81, 4), "carré environ 4,5 (4,5² = 20,25)")
ok(R(1, 1) != R(4, 2) and A(4) == 4 * A(2), "carré non proportionnel, ×4")
tikz_contient("ex2946_corrige", "{x^2}", r"\lirev{2.5}{6.25}", r"\liry{4.4721}{20}")
dans(2946, "$A = c^2$", "$0$ ; $1$ ; $4$ ; $9$ ; $16$ ; $25$", "$6{,}25$", "$4{,}5$", "= 20{,}25$", r"$4 \div 2 = 2$")

# ======================================================================= 2949 vélo
Vl = D["velo"]
ok(interp(Vl, 10) == 3 and interp(Vl, 50) == 10, "vélo lectures")
ok(antecedents(Vl, 9) == {45}, "vélo 9 km")
ok(antecedents(Vl, 6) == {20, ("palier", 20, 30)} or ("palier", 20, 30) in antecedents(Vl, 6), "vélo pause")
ok(Vl[-1] == (60, 12), "vélo total")
ok(R(6, 2) == 3 and R(6, 3) == 2, "vélo 3 km / 2 km par 10 min")
tikz_contient("ex2949_corrige", r"\lirev{10}{3}", r"\lirev{50}{10}", r"\liry{45}{9}", "(axis cs:20,6) -- (axis cs:30,6)")
dans(2949, "$3$ km au bout de $10$ min", "$10$ km au bout de $50$ min", "$45$ min", "$10$ minutes",
     "$12$ km en $60$ min", "$12 - 6 = 6$ km", r"$6 \div 2 = 3$", r"$6 \div 3 = 2$")

# ======================================================================= 2944 périmètre
Pr = lambda l: 2 * l + 6
ok(D["perimetre"] == [(l, Pr(l)) for l in range(3, 9)], "périmètre données")
ok(Pr(6) == 18 and solve(Eq(2 * L + 6, 20), L) == [7], "périmètre B5, P = 20")
ok(R(12, 3) == 4 and R(14, 4) == R(7, 2), "périmètre quotients")
ok(Pr(0) == 6, "périmètre en 0")
tikz_contient("ex2944_corrige", "=2*A2+6", "$12$", "$22$")
tikz_contient("ex2944_graphique", "(axis cs:0,6) -- (axis cs:3,12)", "{2*x+6}")
ok("$7$" in F["ex2944_corrige"], "périmètre ligne 7")
# la ligne surlignée (6) est celle de L = 7 : ligne 1 = en-têtes, ligne 2 = L = 3
ok(3 + (6 - 2) == 7, "périmètre ligne surlignée")
dans(2944, "$P = L + 3 + L + 3 = 2L + 6$", "`=2*A2+6`", "`=2*A5+6`", "$12$ ; $14$ ; $16$ ; $18$ ; $20$ ; $22$",
     "$L = 7$ cm", r"$12 \div 3 = 4$", r"$14 \div 4 = 3{,}5$")

# ======================================================================= 2954 kayak
PA, PB = D["kayakA"], D["kayakB"]
ok(PA(2) == 12 and PB(2) == 18, "kayak 2 h")
ok(PA(0) == 0 and PB(0) == 10, "kayak 0 h")
ok(solve(Eq(6 * t, 10 + 4 * t), t) == [5] and PA(5) == 30, "kayak intersection")
ok(solve(Eq(6 * t, 42), t) == [7] and solve(Eq(10 + 4 * t, 42), t) == [8], "kayak budget 42")
ok(PA(3) == 18 and PB(3) == 22 and PA(7) == 42 and PB(7) == 38, "kayak 3 h / 7 h")
ok(all(PA(k) < PB(k) for k in range(0, 5)) and all(PA(k) > PB(k) for k in range(6, 9)), "kayak règle")
ok(PA(8) == 48 and PB(8) == 42, "kayak fenêtre")
tikz_contient("ex2954_enonce", "{10+4*x}", "{6*x}", "$(d_1)$", "$(d_2)$")
# (d1) navy = B (10+4x) ; (d2) orange = A (6x)
ok(F["ex2954_enonce"].index("{10+4*x}") < F["ex2954_enonce"].index("courbeB"), "kayak : (d1) bleue = B")
tikz_contient("ex2954_corrige", r"\pv{2}{18}", r"\pv{2}{12}", r"\lirev{5}{30}", r"\lirex{7}{42}", r"\lirex{8}{42}")
dans(2954, "$12$ € avec la formule A et $18$ € avec la formule B", "$(5\\ ;\\ 30)$", "$7$ heures avec la formule A",
     "$8$ heures avec la formule B", "$38$ €", "$22$ €")

# ======================================================================= 2956 Tom
Tm = D["tom"]
ok(max(Tm[:3], key=lambda p: p[1]) == (4, 400), "Tom demi-tour")
ok(Tm[2] == (8, 0) and Tm[3] == (10, 0), "Tom à la maison 8-10")
ok(Tm[-1] == (22, 1200), "Tom arrivée")
ok(antecedents(Tm, 200) == {2, 6, 12}, "Tom 200 m : %s" % antecedents(Tm, 200))
ok(400 + 400 + 1200 == 2000, "Tom distance totale")
sit = {t_: l for t_, _, l in FIG.SITUATIONS}
ok(sit == {"Graphique 1": "c", "Graphique 2": "a", "Graphique 3": "d", "Graphique 4": "b"}, "Tom associations")
tikz_contient("ex2956_trajet_corrige", r"\lirex{2}{200}", r"\lirex{6}{200}", r"\lirex{12}{200}", r"\liry{4}{400}",
              r"\lirev{22}{1200}")
dans(2956, "Graphique 1 : situation c ; graphique 2 : situation a ; graphique 3 : situation d ; graphique 4 : situation b",
     "$400$ m de sa maison, au bout de $4$ minutes", "$2$ minutes", "$1\\,200$ m", "$22$ minutes",
     "à $2$ min, à $6$ min et à $12$ min", "$400 + 400 + 1\\,200 = 2\\,000$")

# ======================================================================= 2945 bougie
h = lambda x: 15 - 2 * x
ok(D["bougie"] == [(k, h(k)) for k in range(5)], "bougie données = formule")
ok(h(R(5, 2)) == 10, "bougie 2,5 h")
ok(solve(Eq(15 - 2 * t, 5), t) == [5] and solve(Eq(15 - 2 * t, 0), t) == [R(15, 2)], "bougie 5 cm / 0 cm")
ok(h(3) == 9 and h(8) == -1, "bougie t = 3 et t = 8")
ok(R(13, 1) == 13 and R(11, 2) == R(11, 2) and R(13, 1) != R(11, 2), "bougie quotients")
tikz_contient("ex2945_corrige", "{15-2*x}", "domain=0:7.5", r"\lirev{2.5}{10}", r"\liry{5}{5}", r"\pv{7.5}{0}")
tikz_contient("ex2945_tableur", "=15-2*A2", "$8$")
tikz_contient("ex2945_tableur_corrige", "$-1$", "$15$", "$1$")
dans(2945, "$10$ cm", "$5$ h", "$7{,}5$ h", "$7$ h $30$ min", "$h = 15 - 2 \\times 3 = 15 - 6 = 9$",
     "$15 - 2 \\times 8 = 15 - 16 = -1$", "$11 \\div 2 = 5{,}5$")

# ======================================================================= 2952 randonnée
Pf = D["profil"]
ok(Pf[0] == (0, 1200) and Pf[-1] == (10, 1400), "profil départ / arrivée")
ok(max(Pf, key=lambda p: p[1]) == (5, 1850), "profil sommet")
ys = [y for _, y in Pf]
ok(all(a < b for a, b in zip(ys[0:6], ys[1:6])), "profil monte 0-5")
ok(all(a > b for a, b in zip(ys[5:9], ys[6:9])), "profil descend 5-8")
ok(ys[8] == ys[9] and ys[9] > ys[10], "profil plat 8-9, descend 9-10")
ok(antecedents(Pf, 1600) == {3, 7}, "profil 1 600 m : %s" % antecedents(Pf, 1600))
ok(1850 - 1200 == 650, "dénivelé")
ok([20 * k for k in (1, 3, 5, 10)] == [20, 60, 100, 200], "durée tableau")
ok(200 + 30 == 230 and divmod(230, 60) == (3, 50), "durée totale 3 h 50")
ok((9 * 60 + 230) == 12 * 60 + 50, "arrivée 12 h 50")
tikz_contient("ex2952_corrige", "(axis cs:3,1600)", "(axis cs:7,1600)", r"\pv{5}{1850}", "(axis cs:8,1500) -- (axis cs:9,1500)")
dans(2952, "$1\\,200$ m au départ", "$1\\,850$ m", "$3$ km et à $7$ km", "$1\\,850 - 1\\,200 = 650$", "$D = 20d$",
     "$20$ ; $60$ ; $100$ ; $200$", "$12$ h $50$")

# ======================================================================= STRUCTURE
ids = re.findall(r"^Id: (\d+)$", EX, re.M)
ok(len(ids) == 10 and len(set(ids)) == 10, "10 exercices distincts")
titres = re.findall(r"^=== (.+)$", EX, re.M)
types = [x.split(" - ")[0] for x in titres]
ok(types == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 2 + ["Synthèse"] * 2, "progression %s" % types)
ok(len(set(titres)) == 10, "titres uniques")
retires = [l.split()[0] for l in (ICI / "exercices_retires.txt").read_text(encoding="utf-8").splitlines()
           if l.strip() and not l.startswith("#")]
ok(len(retires) == 11 and not set(retires) & set(ids), "11 retirés, disjoints des gardés")
ok(set(retires) | set(ids) == {str(k) for k in range(2936, 2957)}, "21 Id d'origine couverts")
for i in ids:
    b = bloc(i)
    et = b.split("Étapes:")[1].split("Solution:")[0]
    nq_en = len(re.findall(r"^\d+\. ", b.split("Énoncé:")[1].split("Étapes:")[0], re.M))
    nq_et = len(re.findall(r"^## Question \d+ :", et, re.M))
    nq_so = len(re.findall(r"^\d+\. ", b.split("Solution:")[1], re.M))
    ok(nq_en == nq_et == nq_so, "Id %s : questions %d / %d / %d" % (i, nq_en, nq_et, nq_so))
    ok(et.count("::: methode") >= nq_et and et.count("::: resultat") == nq_et, "Id %s : méthode / résultat" % i)
    ok("::: attention" in et or "::: retenir" in et, "Id %s : erreur fréquente ou à retenir" % i)
    imgs = set(re.findall(r"\[IMAGE_(\d+)\]", b))
    ok(imgs == set(FIG_corr := __import__("json").loads((ICI / "figures" / "correspondance.json").read_text(encoding="utf-8"))["exercices"][i].keys()),
       "Id %s : images %s" % (i, imgs))
for texte, nom in ((EX, "exercices"), (COURS, "cours"), (FICHE, "fiche")):
    ok("brevet" not in texte.lower(), "%s : mot « brevet »" % nom)
ok(set(re.findall(r"\[IMAGE_(\d+)\]", COURS)) == {"1", "2", "3", "4"}, "images du cours")
ok(set(re.findall(r"\[IMAGE_(\d+)\]", FICHE)) == {"1", "2"}, "images de la fiche")

print("%d contrôles réussis, %d échec(s)" % (n_ok, len(echecs)))
for e in echecs:
    print("  ÉCHEC :", e)
sys.exit(1 if echecs else 0)
