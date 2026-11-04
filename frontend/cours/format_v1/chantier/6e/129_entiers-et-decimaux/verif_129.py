# -*- coding: utf-8 -*-
"""Vérification mathématique de la notion 129 (6e : entiers et décimaux).

    python verif_129.py

Contrôle avec sympy (nombres rationnels exacts) chaque résultat du cours, de la
fiche et des 10 exercices, l'écriture en lettres des grands nombres (règles de
l'orthographe recommandée : traits d'union entre mots-nombres, « million » et
« milliard » noms), la cohérence des figures avec les textes et la structure
des corrigés.
"""
import re
import sys
from pathlib import Path

from sympy import Rational as R, floor

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI / "figures"))
import figures as FIG  # noqa: E402

N_OK = 0
ECHECS = []


def ok(cond, msg):
    global N_OK
    if cond:
        N_OK += 1
    else:
        ECHECS.append(msg)


def dec(s):
    """« 63,507 » ou « 4 207 350 018 » → Rational exact."""
    s = s.replace(" ", "").replace(" ", "").replace(",", ".")
    if "." in s:
        e, d = s.split(".")
        return R(int(e + d), 10 ** len(d))
    return R(int(s))


def fr(n, d):
    return R(n, d)


# ------------------------------------------------------------------ nombres en lettres
U = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix",
     "onze", "douze", "treize", "quatorze", "quinze", "seize"]
D = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}


def moins_de_cent(n, final):
    if n <= 16:
        return U[n]
    if n < 20:
        return "dix-" + U[n - 10]
    dz, u = divmod(n, 10)
    if dz in (7, 9):
        base = "soixante" if dz == 7 else "quatre-vingt"
        reste = 10 + u
        if dz == 7 and u == 1:
            return "soixante-et-onze"
        return base + "-" + moins_de_cent(reste, False)
    if dz == 8:
        return "quatre-vingts" if (u == 0 and final) else ("quatre-vingt" if u == 0 else "quatre-vingt-" + U[u])
    if u == 0:
        return D[dz]
    if u == 1:
        return D[dz] + "-et-un"
    return D[dz] + "-" + U[u]


def moins_de_mille(n, final):
    """final : le groupe termine le nombre ou précède « millions »/« milliards » (accord de cent, vingt)."""
    c, r = divmod(n, 100)
    morceaux = []
    if c:
        if c == 1:
            morceaux.append("cent")
        else:
            morceaux.append(U[c] + "-" + ("cents" if (r == 0 and final) else "cent"))
    if r:
        morceaux.append(moins_de_cent(r, final))
    return "-".join(morceaux)


def en_lettres(n):
    if n == 0:
        return "zéro"
    mrd, reste = divmod(n, 10 ** 9)
    mil, reste = divmod(reste, 10 ** 6)
    k, u = divmod(reste, 1000)
    mots = []
    if mrd:
        mots.append(("un" if mrd == 1 else moins_de_mille(mrd, True)) + (" milliard" if mrd == 1 else " milliards"))
    if mil:
        mots.append(("un" if mil == 1 else moins_de_mille(mil, True)) + (" million" if mil == 1 else " millions"))
    bas = []
    if k:
        bas.append("mille" if k == 1 else moins_de_mille(k, False) + "-mille")
    if u:
        bas.append(moins_de_mille(u, True))
    if bas:
        mots.append("-".join(bas))
    return " ".join(mots)


LETTRES = {
    4207350018: "quatre milliards deux-cent-sept millions trois-cent-cinquante-mille-dix-huit",
    5040000600: "cinq milliards quarante millions six-cents",
    6052708300: "six milliards cinquante-deux millions sept-cent-huit-mille-trois-cents",
    40605: "quarante-mille-six-cent-cinq",
    3200000: "trois millions deux-cent-mille",
    9018000700: "neuf milliards dix-huit millions sept-cents",
    70080: "soixante-dix-mille-quatre-vingts",
    200000000: "deux-cents millions",
    150000000: "cent-cinquante millions",
    4500000000: "quatre milliards cinq-cents millions",
    8000000000: "huit milliards",
    4000000000: "quatre milliards",
    2009040000: "deux milliards neuf millions quarante-mille",
}
for n, txt in LETTRES.items():
    ok(en_lettres(n) == txt, f"en lettres {n} : attendu « {en_lettres(n)} », écrit « {txt} »")
# contrôles de la fonction elle-même (règles du cours)
for n, txt in {82: "quatre-vingt-deux", 305: "trois-cent-cinq", 300: "trois-cents", 21: "vingt-et-un",
               6000: "six-mille", 80: "quatre-vingts", 2_000_000: "deux millions"}.items():
    ok(en_lettres(n) == txt, f"règle d'écriture {n} : {en_lettres(n)} ≠ {txt}")

# ------------------------------------------------------------------ outils « chiffre des / nombre de »
RANG = {"unités": 0, "dizaines": 1, "centaines": 2, "mille": 3, "dizaines de mille": 4,
        "centaines de mille": 5, "millions": 6, "milliards": 9}


def chiffre(n, rang):
    return (n // 10 ** RANG[rang]) % 10


def nombre_de(n, rang):
    return n // 10 ** RANG[rang]


# ------------------------------------------------------------------ COURS
N = 4207350018
ok(N == 4 * 10**9 + 207 * 10**6 + 350 * 1000 + 18, "cours : décomposition par classes")
ok(350018 == 3 * 100000 + 5 * 10000 + 1 * 10 + 8, "cours : décomposition par rangs")
ok(chiffre(N, "millions") == 7 and nombre_de(N, "millions") == 4207, "cours : millions")
ok(chiffre(N, "mille") == 0 and nombre_de(N, "mille") == 4207350, "cours : milliers")
ok(chiffre(N, "centaines") == 0 and nombre_de(N, "centaines") == 42073500, "cours : centaines")
ok(4 * 10**9 == 4000 * 10**6, "cours : 4 milliards = 4 000 millions")
ok(10**6 == 1000 * 1000 and 10**9 == 1000 * 10**6, "cours : classes ×1000")
ok(dec("5 040 000 600") == 5040000600, "cours : écriture en chiffres")
ok(fr(1, 1) == fr(10, 10) == fr(100, 100) == fr(1000, 1000), "cours : unité")
ok(fr(1, 10) == fr(10, 100) and fr(1, 100) == fr(10, 1000), "cours : dixième/centième")
ok(fr(1, 10) == dec("0,1") and fr(1, 100) == dec("0,01") and fr(1, 1000) == dec("0,001"), "cours : virgule")
x = dec("63,507")
ok(x == 63 + dec("0,507") and floor(x) == 63, "cours : partie entière / décimale")
ok(x == fr(63507, 1000) == 63 + fr(507, 1000) == 60 + 3 + fr(5, 10) + fr(7, 1000), "cours : écritures de 63,507")
ok([60, 3, fr(5, 10), 0, fr(7, 1000)] == [6 * 10, 3, dec("0,5"), 0, dec("0,007")], "cours : valeurs des chiffres")
ok(12 == fr(120, 10) == fr(1200, 100) == dec("12,0"), "cours : entier décimal")
ok(fr(7, 100) == dec("0,07"), "cours : pourcentage 7 %")
ok(dec("0,58") == fr(58, 100) and dec("7,04") == fr(704, 100) and dec("0,009") == fr(9, 1000), "cours : virgule → fraction")
ok(fr(4127, 100) == dec("41,27") and fr(9, 100) == dec("0,09") and fr(350, 10) == 35, "cours : fraction → virgule")
ok(fr(4127, 100) == fr(4100, 100) + fr(27, 100) == 41 + fr(27, 100), "cours : nombre mixte")
ok(dec("2,4") == fr(24, 10) and dec("2,47") == fr(247, 100) == 2 + fr(47, 100) and floor(dec("2,47")) == 2, "cours : droite")
ok(dec("3,5") == dec("3,50") == dec("3,500") and dec("3,05") != dec("3,5") and dec("07,2") == dec("7,2"), "cours : zéros")
ok(4 * 1000 + 60 == 4060 and fr(4060, 1000) == dec("4,06"), "cours : 4 kg 60 g")
ok(fr(12, 100) == dec("0,12"), "cours : 12 cm")
ok(dec("1,5") == 1 + fr(5, 10) and fr(5, 10) * 1000 == 500, "cours : 1,5 L")
ok(dec("4,60") == dec("4,6") and dec("4,6") * 1000 == 4600 and dec("4,060") == dec("4,06"), "cours : erreur 4,60 kg")

# ------------------------------------------------------------------ 3167
N1 = 6052708300
ok([N1 // 10**9, (N1 // 10**6) % 1000, (N1 // 1000) % 1000, N1 % 1000] == [6, 52, 708, 300], "3167 : classes")
ok(FIG.FIGURES["ex3167_tableau_corrige"].count("{$") >= 10 and str(N1) == "6052708300", "3167 : figure")
ok(dec("40 605") == 40 * 1000 + 605 and dec("3 200 000") == 3 * 10**6 + 200 * 1000
   and dec("9 018 000 700") == 9 * 10**9 + 18 * 10**6 + 700, "3167 : en chiffres")

# ------------------------------------------------------------------ 3170
ok(fr(7, 10) == dec("0,7"), "3170 : A")
ok(3 * 10 + 6 == 36 and fr(36, 100) == dec("0,36") == 3 * fr(1, 10) + 6 * fr(1, 100), "3170 : B")
ok(fr(4, 100) == dec("0,04"), "3170 : D")
ok(1 + fr(4 * 10 + 5, 100) == fr(145, 100) == dec("1,45") == fr(100, 100) + fr(45, 100), "3170 : C")
ok(dec("0,6") / fr(1, 100) == 60 and dec("0,06") / fr(1, 100) == 6, "3170 : cases")
src_fig = (ICI / "figures" / "figures.py").read_text(encoding="utf-8")
for motif in ("bande(0, .9, 7,", "colonnes=3, cases=6", "carre(0, yb, colonnes=10", "colonnes=4, cases=5", "colonnes=0, cases=4"):
    ok(motif in src_fig, f"3170 : figure ({motif})")
ok(r"\frac{36}{100} = 0{,}36" in FIG.FIGURES["ex3170_figures_corrige"], "3170 : figure corrigée")

# ------------------------------------------------------------------ 3169
for f_, v in ((fr(3, 10), "0,3"), (fr(27, 100), "0,27"), (fr(9, 1000), "0,009"), (fr(47, 10), "4,7"),
              (fr(2305, 100), "23,05"), (fr(6, 100), "0,06")):
    ok(f_ == dec(v), f"3169 Q1 : {f_} ≠ {v}")
for v, f_ in (("0,7", fr(7, 10)), ("0,25", fr(25, 100)), ("0,048", fr(48, 1000)), ("3,6", fr(36, 10)),
              ("12,09", fr(1209, 100)), ("5,002", fr(5002, 1000))):
    ok(dec(v) == f_, f"3169 Q2 : {v}")
ok(dec("0,5") == fr(5, 10) == fr(50, 100) == fr(500, 1000), "3169 Q3")
ok(fr(6, 100) == dec("0,06") and dec("0,6") == fr(6, 10) and fr(6, 100) != dec("0,6"), "3169 Q4")

# ------------------------------------------------------------------ 3168
y = dec("306,048")
ok(floor(y) == 306 and y - 306 == dec("0,048"), "3168 : parties")
chiffres = [3, 0, 6, 0, 4, 8]
ok(sum(c * R(10) ** (2 - k) for k, c in enumerate(chiffres)) == y, "3168 : tableau")
ok("{$0$}" in FIG.FIGURES["ex3168_tableau_corrige"] and r"{$3$}" in FIG.FIGURES["ex3168_tableau_corrige"], "3168 : figure")
ok(y == 300 + 6 + fr(4, 100) + fr(8, 1000), "3168 : décomposition")
ok(fr(4, 100) == dec("0,04") and fr(8, 1000) == dec("0,008"), "3168 : valeurs")
ok(5 * 10 + 2 + fr(7, 100) == dec("52,07"), "3168 Q5a")
ok(4 + fr(3, 10) + fr(9, 1000) == dec("4,309") and dec("4,39") != dec("4,309"), "3168 Q5b")

# ------------------------------------------------------------------ 3171
N2 = 7485213906
ok(chiffre(N2, "millions") == 5 and nombre_de(N2, "millions") == 7485, "3171 : millions")
ok(chiffre(N2, "centaines de mille") == 2 and nombre_de(N2, "mille") == 7485213, "3171 : mille")
ok(chiffre(N2, "milliards") == 7, "3171 : milliards")
z = dec("52,836")
ok(floor(z * 10) == 528 and (z * 10) % 10 // 1 == 8 and 52 * 10 + 8 == 528, "3171 : dixièmes")
ok(floor(z * 100) == 5283 and z * 1000 - 5283 * 10 == 6, "3171 : centièmes")
w = dec("6,25")
ok(floor(w * 10) == 62 and w * 100 == 625 and w == 6 + fr(2, 10) + fr(5, 100), "3171 : Léa")
ok(7 * 1000 == 7000, "3171 : 7 milliards = 7 000 millions")

# ------------------------------------------------------------------ 3172
c = dec("3,4")
egales = {"34/10": fr(34, 10), "340/100": fr(340, 100), "3+4/10": 3 + fr(4, 10), "3,40": dec("3,40"), "3+40/100": 3 + fr(40, 100)}
differentes = {"3+4/100": 3 + fr(4, 100), "34/100": fr(34, 100), "3,04": dec("3,04")}
for k, v in egales.items():
    ok(v == c, f"3172 Q1 : {k} devrait valoir 3,4")
for k, v in differentes.items():
    ok(v != c, f"3172 Q1 : {k} ne devrait pas valoir 3,4")
ok(3 + fr(4, 100) == dec("3,04") and fr(34, 100) == dec("0,34"), "3172 Q1 : valeurs des intrus")
lettres = {"a": fr(34, 10), "b": 3 + fr(4, 100), "c": fr(340, 100), "d": 3 + fr(4, 10),
           "e": fr(34, 100), "f": dec("3,40"), "g": dec("3,04"), "h": 3 + fr(40, 100)}
ok("".join(k for k, v in sorted(lettres.items()) if v == c) == "acdfh", "3172 Q1 : réponses a, c, d, f, h")
ok(fr(2375, 1000) == 2 + fr(375, 1000) == dec("2,375"), "3172 Q2a")
ok(fr(1204, 100) == 12 + fr(4, 100) == dec("12,04"), "3172 Q2b")
ok(fr(89, 10) == 8 + fr(9, 10) == dec("8,9"), "3172 Q2c")
ok(5 + fr(7, 100) == fr(507, 100) == dec("5,07"), "3172 Q3a")
ok(18 + fr(3, 10) == fr(183, 10) == dec("18,3"), "3172 Q3b")
ok(1 + fr(25, 1000) == fr(1025, 1000) == dec("1,025"), "3172 Q3c")
ok(dec("05,30") == dec("5,3") and dec("40,050") == dec("40,05") and dec("300,0") == 300 and dec("0,700") == dec("0,7"), "3172 Q4")
ok(dec("40,05") != dec("4,5") and dec("40,05") != dec("40,5"), "3172 Q4 : zéros intérieurs")
ok(14 == fr(140, 10) == fr(1400, 100), "3172 Q5a")
ok(fr(35, 100) == dec("0,35"), "3172 Q5b")

# ------------------------------------------------------------------ 3177
lus = dict((nm, R(str(v))) for v, nm in FIG.LUS_3177)
places = dict((nm, R(str(v))) for v, nm in FIG.PLACES_3177)
ok(lus == {"A": fr(7, 10), "B": fr(23, 10), "C": fr(38, 10)}, "3177 : points lus de la figure")
ok(fr(23, 10) == 2 + fr(3, 10) == dec("2,3") and fr(38, 10) == 3 + fr(8, 10) == dec("3,8") and fr(7, 10) == dec("0,7"), "3177 Q2")
ok(places == {"D": fr(46, 10), "E": 1 + fr(5, 10)}, "3177 : points placés de la figure")
ok(fr(46, 10) == 4 + fr(6, 10) == dec("4,6") and 1 + fr(5, 10) == dec("1,5"), "3177 Q3")
F = dec("3,2") + 6 * fr(1, 100)
ok(F == dec("3,26") == fr(326, 100) == 3 + fr(26, 100) and floor(F) == 3, "3177 Q4")
ok("X2(3.26)" in src_fig and "droite(3.2, 3.3" in src_fig, "3177 : loupe 3,2 – 3,3 et point F")
ok(fr(38, 10) * 10 == 38, "3177 Q5 : 38 mm")
ok(fr(1, 10) / 10 == fr(1, 100), "3177 Q1 : graduation de la loupe")

# ------------------------------------------------------------------ 3173
ok(1 * 1000 + 250 == 1250 and 2 * 1000 + 75 == 2075 and 3 * 100 + 8 == 308, "3173 Q1")
ok(fr(1250, 1000) == 1 + fr(250, 1000) == dec("1,25") == dec("1,250"), "3173 Q2 jus")
ok(fr(2075, 1000) == 2 + fr(75, 1000) == dec("2,075"), "3173 Q2 farine")
ok(fr(308, 100) == 3 + fr(8, 100) == dec("3,08"), "3173 Q2 ruban")
ok(dec("2,75") != dec("2,075") and dec("2,75") * 1000 == 2750 and fr(75, 1000) == dec("0,075"), "3173 Q3")
ok(dec("0,33") == fr(33, 100) == fr(330, 1000) and dec("0,33") * 1000 == 330, "3173 Q4 canette")
ok(dec("0,8") == fr(8, 10) == fr(800, 1000) and dec("0,8") * 1000 == 800, "3173 Q4 sucre")
ok(2000 - 1250 == 750 and fr(750, 1000) == fr(75, 100) == dec("0,75"), "3173 Q5")

# ------------------------------------------------------------------ 3174
ok(dec("4,5") * 10**9 == 4500000000 and 10**9 // 10 == 100000000 and 5 * 10**8 == 500 * 10**6, "3174 Q1a")
ok(nombre_de(4500000000, "millions") == 4500, "3174 Q1b")
ok(8 * 10**9 - 4 * 10**9 == 4000 * 10**6, "3174 Q2")
ok(dec("68,6") * 10**6 == 68600000 and 6 * 100000 == 600000 and nombre_de(68600000, "mille") == 68600, "3174 Q3")
ok(2450000000 // 1000 == 2450000 and 2450000 // 1000 == 2450 and 2450000000 % 10**6 == 0, "3174 Q4")
ok(nombre_de(2450000000, "millions") == 2450, "3174 Q4 : nombre de millions")

# ------------------------------------------------------------------ 3181
N3 = 2 * 10**9 + 9 * 10**6 + 40 * 1000
ok(N3 == 2009040000 and N3 % 1000 == 0, "3181 A1")
ok(nombre_de(N3, "millions") == 2009 and chiffre(N3, "dizaines de mille") == 4, "3181 A3")
m = 3 + fr(4, 10) + 0 * fr(1, 100) + fr(2 * 4, 1000)
ok(m == dec("3,408"), "3181 B4")
ok(floor(m) == 3 and m - 3 == dec("0,408"), "3181 B5")
ok(m == fr(3408, 1000) == fr(3000, 1000) + fr(408, 1000) == 3 + fr(408, 1000), "3181 B6")
ok(floor(m * 100) == 340 and 300 + 40 == 340, "3181 B7")
ok(dec("3,48") != m and (dec("3,48") * 100) % 10 == 8, "3181 B8")
ok("2009040000" in src_fig and '["", "", "3", "4", "0", "8"]' in src_fig, "3181 : figures")

# ------------------------------------------------------------------ figures du cours
ok('fig_tableau_entiers("4207350018"' in src_fig and 'chiffre_et_nombre(\n    "4207350018", 3' in src_fig, "cours : figures du grand nombre")
ok('["", "6", "3", "5", "0", "7"]' in src_fig, "cours : tableau 63,507")
ok('"7485213906", 3' in src_fig, "3171 : figure (rang des millions = 4e chiffre)")
ok("7485213906"[3] == "5" and "4207350018"[3] == "7", "figures : chiffre mis en valeur")

# ------------------------------------------------------------------ structure des textes
texte_ex = (ICI / "exercices.txt").read_text(encoding="utf-8")
cours = (ICI / "cours_132.txt").read_text(encoding="utf-8")
fiche = (ICI / "fiche_198.txt").read_text(encoding="utf-8")
blocs = [b for b in re.split(r"^===[ \t]*$", texte_ex, flags=re.M) if b.strip()]
ok(len(blocs) == 10, f"10 exercices (trouvé {len(blocs)})")
types = [re.match(r"=== (\S+)", b.strip()).group(1) for b in blocs]
ok(types == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 3 + ["Synthèse"], f"progression {types}")
retires = [int(l.split()[0]) for l in (ICI / "exercices_retires.txt").read_text(encoding="utf-8").splitlines()
           if l.strip() and not l.startswith("#")]
gardes = [int(re.search(r"^Id: (\d+)", b, re.M).group(1)) for b in blocs]
ok(sorted(gardes + retires) == list(range(3167, 3188)), "Id gardés + retirés = les 21 Id en ligne")
for b in blocs:
    t = b.strip().splitlines()[0]
    etapes = b.split("Étapes:")[1].split("Solution:")[0]
    nq = len(re.findall(r"^## Question", etapes, re.M))
    ok(nq >= 3, f"{t} : au moins 3 questions corrigées")
    ok(etapes.count("::: methode") >= nq and etapes.count("::: resultat") >= nq, f"{t} : méthode et résultat par question")
    ok("::: attention" in etapes or "::: retenir" in etapes, f"{t} : erreur fréquente ou à retenir")
tout = (texte_ex + cours + fiche).lower()
for n, txt in LETTRES.items():
    ok(txt in tout, f"l'écriture en lettres de {n} (« {txt} ») figure bien dans les textes")
for nom, t in (("exercices", texte_ex), ("cours", cours), ("fiche", fiche)):
    ok("brevet" not in t.lower(), f"{nom} : aucune mention du brevet")
    ok("\x01" not in t, f"{nom} : aucun caractère de contrôle")
    ok(not re.search(r"\$ (mL|L|g|kg|cm|m|mm|km)\b", t), f"{nom} : unités séparées par une espace insécable")

print(f"{N_OK} contrôles justes, {len(ECHECS)} échec(s)")
for e in ECHECS:
    print("  ✗", e)
sys.exit(1 if ECHECS else 0)
