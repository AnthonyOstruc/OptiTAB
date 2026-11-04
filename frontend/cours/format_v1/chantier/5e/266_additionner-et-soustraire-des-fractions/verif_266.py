# -*- coding: utf-8 -*-
"""Vérification des calculs de la notion 266 (5e : additionner et soustraire des fractions).

1. Chaque résultat du cours, de la fiche, des 10 exercices et des figures est
   recalculé en fractions exactes (sympy.Rational).
2. Contrôle automatique de TOUTES les égalités écrites dans les trois fichiers :
   chaque membre calculable (nombres, \\dfrac, +, -, \\times, \\div) doit donner
   la même valeur. Les seules égalités fausses admises sont les erreurs d'élèves
   citées volontairement (liste FAUSSES_VOULUES).
3. Programme de 5e : toute somme ou différence de deux fractions écrite dans les
   fichiers a des dénominateurs égaux ou multiples l'un de l'autre.
4. Textes : 10 titres uniques « Type - Sujet », progression 3/3/3/1, pas de
   « brevet », 10 gardés + 11 retirés = 21, images déclarées.
Lancer : python verif_266.py
"""
import json
import re
from pathlib import Path

from sympy import Rational as R, gcd

ICI = Path(__file__).resolve().parent
n_ok = 0


def ok(cond, msg):
    global n_ok
    assert cond, msg
    n_ok += 1


def de(fr, q):
    """fr de la quantité q, par les deux ordres de calcul."""
    r1 = R(q) / fr.q * fr.p
    r2 = R(q) * fr.p / fr.q
    ok(r1 == r2 == fr * q, f"{fr} de {q}")
    return fr * q


def irr(fr):
    return gcd(fr.p, fr.q) == 1


def multiples(b, d):
    return b % d == 0 or d % b == 0


# ================================================================== COURS
ok(R(3, 8) + R(2, 8) == R(5, 8), "cours : 3/8 + 2/8")
ok(R(4, 13) + R(7, 13) == R(11, 13) and R(9, 5) - R(3, 5) == R(6, 5) and R(11, 6) - R(5, 6) == 1, "cours : exemples même dénominateur")
ok(1 - R(4, 9) == R(5, 9) and 2 + R(3, 5) == R(13, 5) and R(10, 5) == 2, "cours : entiers")
ok(R(5, 16) < R(3, 8) == R(6, 16), "cours : 5/16 < 3/8")
ok(R(2, 3) == R(4, 6) and R(2, 3) + R(1, 6) == R(5, 6), "cours : 2/3 + 1/6")
ok(R(4, 5) == R(8, 10) and R(7, 10) + R(4, 5) == R(15, 10) == R(3, 2), "cours : 7/10 + 4/5")
ok(R(5, 6) == R(10, 12) and R(5, 6) - R(7, 12) == R(3, 12) == R(1, 4), "cours : 5/6 - 7/12")
ok(R(4, 5) != R(4, 10), "cours : 4/5 ≠ 4/10")
ok(R(3, 10) + R(1, 5) == R(5, 10) == R(1, 2), "cours : 3/10 + 1/5")
ok(R(13, 5) == 2 + R(3, 5), "cours : 13/5 = 2 + 3/5")
ok(R(1, 6) + R(1, 3) == R(3, 6) == R(1, 2) and 1 - R(1, 2) == R(1, 2), "cours : gâteau")
pot, pel = R(2, 5), R(3, 10)
ok(pot + pel == R(7, 10) and 1 - (pot + pel) == R(3, 10), "cours : terrain fractions")
ok(de(pot, 300) == 120 and de(pel, 300) == 90 and de(R(3, 10), 300) == 90 and 120 + 90 + 90 == 300, "cours : terrain m²")
ok(300 / 10 == 30, "cours : un dixième = 30 m²")

# ================================================================== FICHE
ok(R(1, 1) - R(3, 7) == R(4, 7) and R(6, 9) == R(2, 3) and R(5, 10) == R(1, 2), "fiche : exemples")

# ================================================================== 2812
ok(R(2, 9) + R(4, 9) == R(6, 9) == R(2, 3), "2812 Q1")
ok(R(5, 11) + R(4, 11) == R(9, 11) and irr(R(9, 11)), "2812 Q2a")
ok(R(13, 7) - R(6, 7) == 1, "2812 Q2b")
ok(R(7, 12) + R(1, 12) == R(8, 12) == R(2, 3), "2812 Q2c")
ok(R(17, 15) - R(8, 15) == R(9, 15) == R(3, 5), "2812 Q2d")
ok(1 - R(3, 10) == R(7, 10), "2812 Q3")
ok(R(3, 10) < R(2, 5) == R(4, 10) and R(2, 5) + R(1, 5) == R(3, 5), "2812 Q4 (Lina)")

# ================================================================== 2814
ok(R(1, 4) == R(2, 8) and R(1, 4) + R(3, 8) == R(5, 8), "2814 Q1-Q3")
ok(R(1, 5) + R(7, 10) == R(9, 10), "2814 Q4a")
ok(R(7, 10) - R(1, 2) == R(2, 10) == R(1, 5), "2814 Q4b")
ok(R(3, 4) - R(5, 12) == R(4, 12) == R(1, 3), "2814 Q4c")
ok(2 - R(3, 4) == R(5, 4) and R(8, 4) == 2, "2814 Q4d")

# ================================================================== 2810
m, a = R(1, 4), R(5, 12)
ok(m == R(3, 12) and m + a == R(8, 12) == R(2, 3), "2810 Q1-Q2")
ok(1 - (m + a) == R(1, 3) == R(4, 12), "2810 Q3")
ok(de(R(1, 3), 60) == 20, "2810 Q4")
ok(de(m, 60) == 15 and de(a, 60) == 25 and 60 - 15 - 25 == 20 and R(40, 60) == R(2, 3), "2810 Q5")
ok(60 / 12 == 5, "2810 figure : 12 parts de 5 L")

# ================================================================== 2817
ok(R(5, 12) + R(1, 12) == R(1, 2) and R(11, 8) - R(3, 8) == 1 and R(13, 15) - R(4, 15) == R(9, 15) == R(3, 5), "2817 Q1")
ok(R(3, 7) == R(6, 14) and R(3, 7) + R(9, 14) == R(15, 14) and irr(R(15, 14)), "2817 Q2a")
ok(R(5, 6) - R(2, 3) == R(1, 6), "2817 Q2b")
ok(R(7, 9) + R(1, 3) == R(10, 9), "2817 Q2c")
ok(R(11, 12) - R(1, 4) == R(8, 12) == R(2, 3), "2817 Q2d")
ok(R(1, 2) + R(3, 8) + R(1, 4) == R(9, 8) and [R(1, 2) * 8, R(1, 4) * 8] == [4, 2], "2817 Q2e")
ok(3 - R(5, 4) == R(7, 4) and R(4, 3) - 1 == R(1, 3), "2817 Q3")
res = [R(1, 2), R(1), R(3, 5), R(15, 14), R(1, 6), R(10, 9), R(2, 3), R(9, 8), R(7, 4), R(1, 3)]
ok([x for x in res if x > 1] == [R(15, 14), R(10, 9), R(9, 8), R(7, 4)], "2817 Q4 : résultats > 1")
ok(R(15, 14) == 1 + R(1, 14) and R(10, 9) == 1 + R(1, 9) and R(9, 8) == 1 + R(1, 8) and R(7, 4) == 1 + R(3, 4), "2817 Q4 décompositions")

# ================================================================== 2818
ok(R(3, 8) + R(4, 8) == R(7, 8), "2818 Q1a")
ok(R(5, 6) - R(3, 6) == R(1, 3) == R(2, 6), "2818 Q1b")
ok(R(1, 5) + R(4, 5) == 1, "2818 Q1c")
ok(R(1, 2) + R(4, 10) == R(9, 10) and R(1, 2) == R(5, 10), "2818 Q1d")
A = R(1, 2) + R(3, 4) - R(5, 8)
ok(A == R(5, 8) and R(4, 8) + R(6, 8) == R(10, 8), "2818 Q2 A")
B = 2 - R(1, 3) - R(5, 6)
ok(B == R(5, 6) and R(12, 6) - R(2, 6) == R(10, 6), "2818 Q2 B")
b1, b2, b3 = R(1, 6), R(1, 3), R(5, 12)
m1, m2 = b1 + b2, b2 + b3
ok(m1 == R(1, 2) == R(3, 6) and m2 == R(3, 4) == R(9, 12) and m1 + m2 == R(5, 4), "2818 Q3 pyramide")

# ================================================================== 2819
ok(R(3 + 1, 4 + 8) == R(4, 12) == R(1, 3) < R(3, 4), "2819 Q1 erreur de Tom")
ok(R(3, 4) + R(1, 8) == R(7, 8), "2819 Q1 correction")
ok(R(5 - 1, 6 - 3) == R(4, 3) > 1 > R(5, 6), "2819 Q2 erreur de Sara")
ok(R(5, 6) - R(1, 3) == R(3, 6) == R(1, 2), "2819 Q2 correction")
ok(R(3, 10) == R(3, 5) / 2 and R(3, 5) + R(1, 10) == R(7, 10) and irr(R(7, 10)), "2819 Q3 Noé")
ok(R(5, 6) + R(1, 3) == R(7, 6) > 1 and R(5, 6) + R(1, 6) == 1 and R(1, 3) > R(1, 6), "2819 Q4 Inès")
ok(1 - R(3, 7) == R(4, 7) and R(4, 7) + R(3, 7) == 1, "2819 Q5 Malo")

# ================================================================== 2830
ok(R(1, 2) == R(4, 8) and R(3, 2) == R(12, 8), "2830 Q1")
servi = R(1, 2) + R(3, 8)
ok(servi == R(7, 8), "2830 Q2")
reste = R(3, 2) - servi
ok(reste == R(5, 8), "2830 Q3")
ok(R(1, 4) == R(2, 8) and 2 * R(1, 4) <= reste < 3 * R(1, 4), "2830 Q4 : 2 verres")
ok(max(k for k in range(10) if k * R(1, 4) <= reste) == 2 and reste - 2 * R(1, 4) == R(1, 8), "2830 Q4 reste")
ok(de(R(1, 8), 100) == R(25, 2) == R(125, 10), "2830 Q5 : 12,5 cL")
ok(R(4, 10) < R(1, 2), "2830 : 4/10 < 1/2 (erreur)")

# ================================================================== 2824
lu, ma = R(1, 3), R(5, 12)
ok(lu == R(4, 12) < ma, "2824 Q1")
ok(lu + ma == R(9, 12) == R(3, 4), "2824 Q2")
ok(de(R(3, 4), 240) == 180 and de(lu, 240) == 80 and de(ma, 240) == 100 and 80 + 100 == 180, "2824 Q3")
ok(R(40, 240) == R(1, 6) == R(2, 12) and 240 / 12 == 20, "2824 Q4")
ok(1 - lu - ma - R(1, 6) == R(1, 12) and de(R(1, 12), 240) == 20 and 240 - 180 - 40 == 20, "2824 Q5")
ok(R(1 + 5, 3 + 12) == R(6, 15), "2824 : erreur 6/15 citée")

# ================================================================== 2815
sp, th, mu = R(1, 2), R(1, 4), R(1, 8)
ok([sp * 8, th * 8, mu * 8] == [4, 2, 1], "2815 Q1")
ok(sp + th + mu == R(7, 8), "2815 Q2")
ok(1 - R(7, 8) == R(1, 8) and de(R(1, 8), 40) == 5, "2815 Q3")
ok(sp - th == R(1, 4) and de(R(1, 4), 40) == 10, "2815 Q4")
eff = [de(sp, 40), de(th, 40), de(mu, 40), de(R(1, 8), 40)]
ok(eff == [20, 10, 5, 5] and sum(eff) == 40 and eff[0] - eff[1] == 10, "2815 Q5")
ok(R(1 + 1 + 1, 2 + 4 + 8) == R(3, 14), "2815 : erreur 3/14 citée")

# ================================================================== 2811
mat, apm = R(4, 9), R(1, 3)
ok(apm == R(3, 9) and mat + apm == R(7, 9) and irr(R(7, 9)), "2811 Q1-Q2")
ok(1 - R(7, 9) == R(2, 9) and 18 / 9 == 2 and de(R(2, 9), 18) == 4, "2811 Q3")
ok(de(mat, 18) == 8 and de(apm, 18) == 6 and 18 / 2 == 9 and 8 < 9, "2811 Q4 et figure")
ok(8 + 6 + 4 == 18, "2811 figure : total 18 km")
bu = R(3, 10) + R(1, 2)
ok(bu == R(8, 10) == R(4, 5), "2811 Q5")
ok(1 - bu == R(1, 5) and de(R(1, 5), 100) == 20, "2811 Q6")
ok(de(R(1, 4), 100) == 25 > 20 and 25 - 20 == 5, "2811 Q7")
ok(R(4 + 1, 9 + 3) == R(5, 12), "2811 : erreur 5/12 citée")

# ================================================================== CONTRÔLE AUTOMATIQUE DES ÉGALITÉS
FICHIERS = ["cours_261.txt", "fiche_181.txt", "exercices.txt"]
TEXTES = {n: (ICI / n).read_text(encoding="utf-8") for n in FICHIERS}

# Erreurs d'élèves volontairement citées (membres de gauche et de droite inégaux)
FAUSSES_VOULUES = {
    r"\dfrac{2}{5} + \dfrac{1}{5} = \dfrac{3}{10}",
    r"\dfrac{3}{4} + \dfrac{1}{8} = \dfrac{4}{12}",
    r"\dfrac{5}{6} - \dfrac{1}{3} = \dfrac{4}{3}",
    r"\dfrac{3}{5} + \dfrac{1}{10} = \dfrac{3}{10} + \dfrac{1}{10} = \dfrac{4}{10} = \dfrac{2}{5}",
    r"\dfrac{3}{5} = \dfrac{3}{10}",  # « Noé a écrit … » (erreur expliquée)
    r"\dfrac{1}{3} = \dfrac{1}{9}",   # 2811 : erreur fréquente citée
    r"\dfrac{4}{9} + \dfrac{1}{3} = \dfrac{5}{12}",  # 2811 : erreur fréquente citée
}

FRAC = re.compile(r"\\dfrac\{(\d+)\}\{(\d+)\}")


def valeur(expr):
    """Valeur exacte d'un membre, ou None s'il contient autre chose que des calculs."""
    e = expr.strip()
    e = re.sub(r"\\(qquad|quad|,|;|!)", " ", e)
    e = e.replace(r"\left", "").replace(r"\right", "")
    e = re.sub(r"\\text\{[^}]*\}", "§", e)
    if "§" in e or not e:
        return None
    e = FRAC.sub(lambda m: f"R({m.group(1)},{m.group(2)})", e)
    e = re.sub(r"\\dfrac\{([^{}]+)\}\{([^{}]+)\}", r"((\1)/(\2))", e)
    e = e.replace(r"\times", "*").replace(r"\div", "/").replace("{,}", ".")
    e = e.replace("{", "(").replace("}", ")")
    if re.search(r"[^0-9R(),.+\-*/ ]", e):
        return None
    if not re.search(r"\d", e):
        return None
    e = re.sub(r"(?<![\w.'])(\d+\.\d+)", r"R('\1')", e)  # décimaux exacts
    e = re.sub(r"(?<![\w.'])(\d+)(?![\d.,']|\s*,)", r"R(\1)", e)
    try:
        return eval(e, {"R": R})
    except Exception:
        return None


def formules(texte):
    """Toutes les formules ($…$ et $$…$$), lignes d'aligned séparées."""
    out = []
    for m in re.finditer(r"\$\$(.+?)\$\$|\$(.+?)\$", texte, re.S):
        f = m.group(1) or m.group(2)
        f = re.sub(r"\\begin\{aligned\}|\\end\{aligned\}", "", f)
        for ligne in re.split(r"\\\\", f):
            ligne = ligne.replace("&", "").strip()
            if ligne:
                out.append(ligne)
    return out


n_egalites = 0
n_sommes = 0
for nom, texte in TEXTES.items():
    for ligne in formules(texte):
        if "\\neq" in ligne or "\\approx" in ligne or "\\dots" in ligne:
            continue
        # contrôle du programme : a/b ± c/d avec b, d égaux ou multiples
        for m in re.finditer(r"\\dfrac\{(\d+)\}\{(\d+)\}\s*([+-])\s*\\dfrac\{(\d+)\}\{(\d+)\}", ligne):
            b, d = int(m.group(2)), int(m.group(5))
            ok(multiples(b, d), f"{nom} : dénominateurs {b} et {d} non multiples dans « {ligne} »")
            n_sommes += 1
        for seg in re.split(r"[;:]|(?<!\\)\\qquad|\\quad|\bet\b", ligne):
            if seg.count("=") == 0:
                continue
            membres = [x for x in seg.split("=")]
            vals = [valeur(x) for x in membres]
            vals = [v for v in vals if v is not None]
            if len(vals) < 2:
                continue
            juste = all(v == vals[0] for v in vals)
            if not juste:
                ok(seg.strip() in FAUSSES_VOULUES or ligne.strip() in FAUSSES_VOULUES,
                   f"{nom} : égalité fausse « {seg.strip()} » ({vals})")
            else:
                ok(True, "")
            n_egalites += 1
ok(n_egalites > 150, f"au moins 150 égalités contrôlées ({n_egalites})")
ok(n_sommes > 100, f"au moins 100 sommes ou différences contrôlées ({n_sommes})")

# ================================================================== TEXTES
TYPES = ("Découverte - ", "Entraînement - ", "Problème - ", "Synthèse - ")
ex = TEXTES["exercices.txt"]
titres = re.findall(r"^=== (.+)$", ex, re.M)
ok(len(titres) == 10 and len(set(titres)) == 10, "10 titres uniques")
ok(all(t.startswith(TYPES) for t in titres), "types de titres")
ok([t.split(" - ")[0] for t in titres] == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 3 + ["Synthèse"],
   "progression 3 / 3 / 3 / 1")
for nom, t in TEXTES.items():
    ok("brevet" not in t.lower(), f"pas de « brevet » dans {nom}")
    ok("\\times \\dfrac" not in t and "\\dfrac{1}{4} \\times" not in t, f"pas de produit de fractions dans {nom}")
ids = [int(x) for x in re.findall(r"^Id:\s*(\d+)", ex, re.M)]
retires = [int(m) for m in re.findall(r"^(\d+)", (ICI / "exercices_retires.txt").read_text(encoding="utf-8"), re.M)]
meta = json.loads((ICI / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))
en_ligne = {e["id"] for e in meta["exercices"]}
ok(len(ids) == 10 and len(retires) == 11 and not set(ids) & set(retires), "10 gardés, 11 retirés, disjoints")
ok(set(ids) | set(retires) == en_ligne and len(en_ligne) == 21, "10 + 11 = les 21 exercices en ligne")

# chaque exercice : méthode, étape, résultat, attention ou retenir, solution
blocs = re.split(r"^===\s*$", ex, flags=re.M)
blocs = [b for b in blocs if "Id:" in b]
ok(len(blocs) == 10, "10 blocs")
for b in blocs:
    i = re.search(r"Id:\s*(\d+)", b).group(1)
    et = b.split("Étapes:")[1].split("Solution:")[0]
    ok("::: methode" in et and "::: etape" in et and "::: resultat" in et, f"{i} : méthode, étapes, résultat")
    ok("::: attention" in et or "::: retenir" in et, f"{i} : erreur fréquente ou à retenir")
    nq = len(re.findall(r"^\d+\.", b.split("Énoncé:")[1].split("Étapes:")[0], re.M))
    nr = len(re.findall(r"^## Question", et, re.M))
    ns = len(re.findall(r"^\d+\.", b.split("Solution:")[1], re.M))
    ok(nq == nr == ns, f"{i} : {nq} questions, {nr} corrigés, {ns} solutions")

# images : chaque [IMAGE_N] a sa figure, et réciproquement
corr = json.loads((ICI / "figures" / "correspondance.json").read_text(encoding="utf-8"))
imgs = ICI / "figures" / "images"


def positions(t):
    return sorted({int(n) for n in re.findall(r"^\[IMAGE_(\d+)\]\s*$", t, re.M)})


ok(positions(TEXTES["cours_261.txt"]) == sorted(int(k) for k in corr["cours"]["261"]), "images du cours")
ok(positions(TEXTES["fiche_181.txt"]) == sorted(int(k) for k in corr["fiches"]["181"]), "images de la fiche")
for b in blocs:
    i = re.search(r"Id:\s*(\d+)", b).group(1)
    ok(positions(b) == sorted(int(k) for k in corr["exercices"].get(i, {})), f"images de {i}")
for groupe in corr.values():
    for places in groupe.values():
        for v in places.values():
            ok((imgs / v["fichier"]).exists() and len(v["alt"]) >= 15, f"figure {v['fichier']}")

print(f"verif_266 : {n_ok} contrôles, tous justes ({n_egalites} égalités et {n_sommes} sommes/différences lues dans les textes).")
