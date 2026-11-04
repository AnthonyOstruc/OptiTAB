# -*- coding: utf-8 -*-
"""Vérification (sympy, valeurs exactes) de tous les résultats de la notion 130 (6e).

    python verif_130.py
"""
import json
import re
import sys
from pathlib import Path

from sympy import Rational as R, floor, pi, N as Nnum

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI / "figures"))
NB = 0
ECHECS = []


def ok(cond, msg):
    global NB
    NB += 1
    if not cond:
        ECHECS.append(msg)


def q(s):
    """'4,738' -> Rational exact."""
    return R(str(s).replace(",", "."))


def arrondi(x, rang):
    """Arrondi au plus proche, 5 vers le haut (nombres positifs). rang : 0 unité, 1 dixième, 2 centième."""
    p = R(10) ** rang
    return floor(x * p + R(1, 2)) / p


def troncature(x, rang):
    p = R(10) ** rang
    return floor(x * p) / p


def decroissant(L):
    return sorted(L, reverse=True)


# ------------------------------------------------------------------ cours / fiche
ok(R(1, 10) == q("0,1") and 7 * R(1, 10) == q("0,7") and 1 + 2 * R(1, 10) == q("1,2"), "cours lecture A, B")
ok(1 + 6 * R(1, 10) == q("1,6"), "cours placer P(1,6)")
ok(q("2,6") + 4 * R(1, 100) == q("2,64") and q("2,6") < q("2,64") < q("2,7"), "cours zoom 2,64")
ok((q("2,64") + q("2,65")) / 2 == q("2,645"), "cours milieu 2,645")
ok(q("14,2") < q("15,08") and q("6,3") > q("6,25") and q("9,1") > q("9,09"), "cours comparaisons")
ok(q("4,8") <= q("4,80") and q("4,8") <= 5 and q("7,02") >= q("7,02") and q("7,02") >= 7, "cours symboles larges")
cinq = [q(x) for x in "5,8 5,08 5,18 5,801 5,80".split()]
ok(sorted(cinq) == [q(x) for x in "5,08 5,18 5,8 5,80 5,801".split()], "cours rangement 5 nombres")
x = q("8,463")
ok(8 < x < 9 and q("8,4") < x < q("8,5") and q("8,46") < x < q("8,47"), "cours encadrement 8,463")
ok(q("1,7") < q("1,75") < q("1,8") and q("0,52") < q("0,525") < q("0,53"), "cours intercaler")
ok(q("1,7") < q("1,71") < q("1,799") < q("1,8"), "cours attention intercaler")
ok(arrondi(q("3,47"), 1) == q("3,5") and q("3,47") - q("3,4") == R(7, 100) and q("3,5") - q("3,47") == R(3, 100), "cours figure arrondi 3,47")
y = q("15,382")
ok([arrondi(y, r) for r in (0, 1, 2)] == [15, q("15,4"), q("15,38")], "cours arrondis 15,382")
ok(arrondi(q("7,96"), 1) == 8, "cours retenue 7,96")
ok(troncature(R(1, 7), 6) == q("0,142857") and arrondi(R(1, 7), 2) == q("0,14"), "cours 1/7")
ok(arrondi(pi, 2) == q("3,14") and troncature(pi, 5) == q("3,14159"), "cours pi")
ok(arrondi(q("2,46"), 0) == 2 and arrondi(arrondi(q("2,46"), 1), 0) == 3, "cours piège arrondi en cascade")
panier = [q("3,98"), q("12,3"), q("5,15")]
ok(sum(arrondi(p, 0) for p in panier) == 21 and sum(panier) == q("21,43"), "cours ordre de grandeur panier")
ok(sum(panier) > 21, "cours budget 21 € insuffisant")

# ------------------------------------------------------------------ 3209
pas = R(1, 10)
ok(1 / R(10) == pas, "3209 Q1")
ok(4 * pas == q("0,4") and 1 + 3 * pas == q("1,3") and 1 + 8 * pas == q("1,8") and 2 - 2 * pas == q("1,8"), "3209 Q2")
ok(q("0,9") / pas == 9 and (q("1,5") - 1) / pas == 5 and q("1,5") == R(3, 2), "3209 Q3")
ok(1 < q("1,05") < q("1,1") and q("1,05") == (1 + q("1,1")) / 2, "3209 Q4 milieu")
six = {"A": q("0,4"), "B": q("1,3"), "C": q("1,8"), "D": q("0,9"), "E": q("1,5"), "F": q("1,05")}
ok(sorted(six, key=six.get) == ["A", "D", "F", "B", "E", "C"], "3209 Q5 ordre")

# ------------------------------------------------------------------ 3210
paires = [("2,5", "2,15", ">"), ("0,8", "0,75", ">"), ("12,09", "12,1", "<"), ("3,4", "3,40", "="),
          ("7", "6,99", ">"), ("0,305", "0,35", "<")]
for a, b, s in paires:
    va, vb = q(a), q(b)
    ok({">": va > vb, "<": va < vb, "=": va == vb}[s], "3210 Q1 %s %s %s" % (a, s, b))
ok(q("2,15") < q("2,5") and q("2,1") < q("2,15") < q("2,2") and q("2,15") == (q("2,1") + q("2,2")) / 2, "3210 Q2")
ok(R(15, 100) < R(50, 100), "3210 Q2 centièmes")
ok(bool(q("4,7") <= q("4,70")) and bool(q("5,1") >= q("5,09")), "3210 Q3 a b vrais")
ok(not bool(q("6,3") < q("6,3")) and not bool(q("0,9") <= q("0,89")), "3210 Q3 c d faux")

# ------------------------------------------------------------------ 3213
tab = {"4,738": ("5", "4,7", "4,74"), "12,451": ("12", "12,5", "12,45"),
       "9,96": ("10", "10", "9,96"), "0,295": ("0", "0,3", "0,30")}
for n, rep in tab.items():
    ok([arrondi(q(n), r) for r in (0, 1, 2)] == [q(v) for v in rep], "3213 Q1 %s" % n)
ok(q("4,738") < q("4,75") and q("4,738") - q("4,7") == R(38, 1000) and q("4,8") - q("4,738") == R(62, 1000), "3213 Q2")
ok(arrondi(R(1, 3), 1) == q("0,3") and arrondi(R(1, 3), 2) == q("0,33"), "3213 Q3 1/3")
ok(arrondi(R(2, 3), 1) == q("0,7") and arrondi(R(2, 3), 2) == q("0,67"), "3213 Q3 2/3")
ok(arrondi(R(5, 6), 1) == q("0,8") and arrondi(R(5, 6), 2) == q("0,83"), "3213 Q3 5/6")
ok(troncature(R(5, 6), 4) == q("0,8333") and troncature(R(2, 3), 4) == q("0,6666"), "3213 Q3 écritures")
ok(arrondi(q("6,48"), 0) == 6 and arrondi(arrondi(q("6,48"), 1), 0) == 7, "3213 Q4 Sam")
ok(q("6,48") - 6 == q("0,48") and 7 - q("6,48") == q("0,52"), "3213 Q4 distances")

# ------------------------------------------------------------------ 3216
ok(q("5,3") < q("5,37") < q("5,4"), "3216 Q1")
ok(R(1, 10) / 10 == R(1, 100), "3216 Q2a")
ok(q("5,3") + R(1, 100) == q("5,31") and q("5,3") + R(7, 100) == q("5,37"), "3216 Q2b")
ok(q("5,3") + R(5, 100) == q("5,35") and q("5,325") == (q("5,32") + q("5,33")) / 2, "3216 Q3")
ok(arrondi(q("5,37"), 1) == q("5,4") and q("5,4") - q("5,37") == R(3, 100) and q("5,37") - q("5,3") == R(7, 100), "3216 Q4")
ok(q("5,3") + 7 * R(1, 10) == 6, "3216 erreur fréquente (6)")

# ------------------------------------------------------------------ 3217
temps = {"Inès": q("31,5"), "Bastien": q("31,05"), "Chloé": q("30,98"), "Malik": q("31,50"), "Zoé": q("31,4"), "Hugo": q("31,45")}
ok(sorted(temps.values()) == [q(v) for v in "30,98 31,05 31,4 31,45 31,5 31,50".split()], "3217 Q1")
ok(sorted(temps, key=temps.get)[:4] == ["Chloé", "Bastien", "Zoé", "Hugo"] and temps["Inès"] == temps["Malik"], "3217 Q2")
ok([n for n, t in temps.items() if t <= q("31,45")] == ["Bastien", "Chloé", "Zoé", "Hugo"], "3217 Q3")
lg = [q(v) for v in "4,09 4,9 4,19 4,091 4,1".split()]
ok(decroissant(lg) == [q(v) for v in "4,9 4,19 4,1 4,091 4,09".split()], "3217 Q4")

# ------------------------------------------------------------------ 3211
x = q("23,186")
ok(23 < x < 24 and q("23,1") < x < q("23,2") and q("23,18") < x < q("23,19"), "3211 Q1")
ok(troncature(x, 0) == 23 and troncature(x, 1) == q("23,1") and troncature(x, 2) == q("23,18"), "3211 Q1 méthode")
ok(q("4,6") < q("4,65") < q("4,7") and q("0,39") < q("0,395") < q("0,4") and 12 < q("12,005") < q("12,01"), "3211 Q2")
ok(q("4,6") < q("4,6025") < q("4,605") < q("4,61") < q("4,7"), "3211 Q3")
cent = [R(k, 100) for k in range(400, 500) if q("4,6") < R(k, 100) < q("4,7")]
ok(len(cent) == 9 and cent[0] == q("4,61") and cent[-1] == q("4,69"), "3211 Q4")

# ------------------------------------------------------------------ 3215
ok(47 == 3 * 15 + 2 and 20 == 3 * 6 + 2, "3215 Q1 division")
part = R(47, 3)
ok(troncature(part, 3) == q("15,666") and part - troncature(part, 3) > 0, "3215 Q1 non décimal (reste)")
ok([arrondi(part, r) for r in (0, 1, 2)] == [16, q("15,7"), q("15,67")], "3215 Q2")
ok(q("15,66") < part < q("15,67"), "3215 Q2 encadrement")
ok(3 * q("15,67") == q("47,01") and 3 * q("0,67") == q("2,01"), "3215 Q3")
ok(3 * q("15,66") == q("46,98") and 47 - q("46,98") == q("0,02"), "3215 Q4")
ok(2 * q("15,67") + q("15,66") == 47, "3215 Q5")

# ------------------------------------------------------------------ 3214
prix = [q("2,95"), q("4,10"), q("6,85"), q("8,49")]
ok([arrondi(p, 0) for p in prix] == [3, 4, 7, 8], "3214 Q1")
ok(sum(arrondi(p, 0) for p in prix) == 22, "3214 Q2")
ok(sum(prix) == q("22,39") and q("2,95") + q("4,10") == q("7,05") and q("7,05") + q("6,85") == q("13,90"), "3214 Q3")
ok(q("22,39") / 10 == q("2,239") and q("22,39") * 10 == q("223,9"), "3214 Q3 virgules")
ok(sum(prix) > 22 and sum(prix) - 22 == q("0,39"), "3214 Q4")
ok(3 * q("9,80") < 30 < 35 and 3 * q("9,80") == q("29,40"), "3214 Q5")

# ------------------------------------------------------------------ 3212
cand = [R(k, 100) for k in range(600, 700)]
i1 = [c for c in cand if q("6,4") < c < q("6,6")]
ok(len(i1) == 19 and i1[0] == q("6,41") and i1[-1] == q("6,59"), "3212 Q1")
i2 = [c for c in i1 if arrondi(c, 1) == q("6,5")]
ok(len(i2) == 10 and i2[0] == q("6,45") and i2[-1] == q("6,54"), "3212 Q2")
ok(arrondi(q("6,44"), 1) == q("6,4") and arrondi(q("6,55"), 1) == q("6,6"), "3212 Q2 limites")
i3 = [c for c in i2 if arrondi(c, 0) == 6]
ok(i3 == [q(v) for v in "6,45 6,46 6,47 6,48 6,49".split()], "3212 Q3")
i4 = [c for c in i3 if int(c * 100) % 2 == 0]
ok(i4 == [q("6,46"), q("6,48")], "3212 Q4 indice 4")
i5 = [c for c in i4 if c > q("6,47")]
ok(i5 == [q("6,48")], "3212 Q4 unicité")

# ------------------------------------------------------------------ 3229
ok(R(1, 10) / 10 == R(1, 100), "3229 Q1 intervalle")
ok(q("3,3") + 6 * R(1, 100) == q("3,36") and q("3,4") + 7 * R(1, 100) == q("3,47"), "3229 Q1 lecture")
sauts = {"Léa": q("3,36"), "Nathan": q("3,47"), "Sami": q("3,4"), "Jade": q("3,09"), "Yanis": q("3,40"), "Emma": q("3,5")}
ok(decroissant(sauts.values()) == [q(v) for v in "3,5 3,47 3,4 3,40 3,36 3,09".split()], "3229 Q2 ordre")
ok(sorted(sauts, key=sauts.get, reverse=True)[:2] == ["Emma", "Nathan"] and sauts["Sami"] == sauts["Yanis"], "3229 Q2 podium")
arr = {k: arrondi(v, 1) for k, v in sauts.items()}
ok(arr == {"Léa": q("3,4"), "Nathan": q("3,5"), "Sami": q("3,4"), "Jade": q("3,1"), "Yanis": q("3,4"), "Emma": q("3,5")}, "3229 Q3")
ok(arr["Emma"] == arr["Nathan"] and sauts["Emma"] > sauts["Nathan"], "3229 Q4")
paul = [R(k, 100) for k in range(300, 400) if q("3,47") < R(k, 100) < q("3,5")]
ok(paul == [q("3,48"), q("3,49")], "3229 Q5")
ok(3 < q("3,36") < 4 and q("3,3") < q("3,36") < q("3,4"), "3229 Q6")

# ------------------------------------------------------------------ figures : positions = valeurs du texte
import figures as FG  # noqa: E402

ok(FG.F("2,64") == q("2,64") and FG.nb(q("5,325")) == "5{,}325" and FG.nb(q("10")) == "10", "figures outils")
for nom, attendus in {
    "ex3209_corrige": ["{$0{,}4$}", "{$1{,}3$}", "{$1{,}8$}", "{$D$}", "{$E$}", "{$F$}"],
    "ex3216_corrige": ["{$5{,}31$}", "{$5{,}37$}"],
    "ex3229_corrige": ["$3{,}36$ m", "$3{,}47$ m"],
    "ex3211_corrige": ["23{,}18 < 23{,}186 < 23{,}19", "23{,}1 < 23{,}186 < 23{,}2"],
    "ex3212_corrige": ["{$6{,}48$}", "de $6{,}45$ à $6{,}54$", "jusqu'à $6{,}49$"],
    "ex3213_corrige": ["$38$ millièmes", "$62$ millièmes", "milieu : $4{,}75$"],
    "cours_arrondi": ["$7$ centièmes", "$3$ centièmes", "milieu : $3{,}45$"],
    "cours_encadrer": ["8{,}4 < 8{,}463 < 8{,}5", "8{,}46 < 8{,}463 < 8{,}47"],
    "cours_zoom": ["C(2{,}64)"],
    "cours_droite": ["A(0{,}7)", "B(1{,}2)"],
}.items():
    ok(all(a in FG.FIGURES[nom] for a in attendus), "figure %s : textes" % nom)
# les énoncés ne donnent pas la réponse
ok("0{,}4" not in FG.FIGURES["ex3209_enonce"] and "5{,}37" not in FG.FIGURES["ex3216_enonce"]
   and "3{,}36" not in FG.FIGURES["ex3229_enonce"] and "2{,}15" not in FG.FIGURES["ex3210_enonce"], "énoncés sans réponse")

# ------------------------------------------------------------------ structure des fichiers
ex = (ICI / "exercices.txt").read_text(encoding="utf-8")
blocs = [b for b in re.split(r"^===[ \t]*$", ex, flags=re.M) if b.strip()]
ids = [int(re.search(r"^Id:\s*(\d+)", b, re.M).group(1)) for b in blocs]
titres = [b.strip().splitlines()[0][4:] for b in blocs]
ok(len(blocs) == 10, "10 exercices")
ok([t.split(" - ")[0] for t in titres] == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 3 + ["Synthèse"], "progression des types")
ok(len(set(titres)) == 10, "titres uniques")
for b, i in zip(blocs, ids):
    etapes = b.split("Étapes:")[1].split("Solution:")[0]
    ok("::: methode" in etapes and "::: etape" in etapes and "::: resultat" in etapes, "%d structure du corrigé" % i)
    ok("::: attention" in etapes or "::: retenir" in etapes, "%d erreur fréquente" % i)
    ok("Solution:" in b and "Énoncé:" in b, "%d rubriques" % i)
ret = [int(l.split()[0]) for l in (ICI / "exercices_retires.txt").read_text(encoding="utf-8").splitlines()
       if l.strip() and not l.startswith("#")]
meta = json.loads((ICI / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))
tous = sorted(e["id"] for e in meta["exercices"])
ok(sorted(ids + ret) == tous and len(ret) == 11 and not set(ids) & set(ret), "10 gardés + 11 retirés = 21 en ligne")
txt = ex + (ICI / "cours_133.txt").read_text(encoding="utf-8") + (ICI / "fiche_200.txt").read_text(encoding="utf-8")
ok("brevet" not in txt.lower(), "aucune mention du brevet")
corr = json.loads((ICI / "figures" / "correspondance.json").read_text(encoding="utf-8"))
for i in ids:
    b = blocs[ids.index(i)]
    n_img = set(re.findall(r"\[IMAGE_(\d+)\]", b))
    ok(n_img == set(corr["exercices"].get(str(i), {}).keys()), "%d images déclarées" % i)

print("%d contrôles, %d échec(s)" % (NB, len(ECHECS)))
for e in ECHECS:
    print("  ÉCHEC :", e)
sys.exit(1 if ECHECS else 0)
