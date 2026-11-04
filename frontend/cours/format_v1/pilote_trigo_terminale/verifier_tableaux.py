# -*- coding: utf-8 -*-
"""Vérification numérique des tableaux de signes et de variations du pilote.

    python verifier_tableaux.py

Chaque `::: tableau` des fichiers du chapitre est relu ; la fonction de
chaque ligne est donnée ci-dessous (FONCTIONS, par libellé et par fichier).
Contrôles : signe au milieu de chaque intervalle, zéros (z), sens de
variation sur chaque intervalle, valeurs annoncées aux bornes (limites
latérales pour les doubles barres), signe des infinis.
"""
import math
import re
from pathlib import Path

ICI = Path(__file__).resolve().parent

sin, cos, tan = math.sin, math.cos, math.tan

# (fichier, numéro du tableau dans le fichier) -> {libellé: fonction}
FONCTIONS = {
    ("cours.txt", 1): {r"-\sin(x)": lambda x: -sin(x), r"\cos(x)": cos},
    ("fiche.txt", 1): {r"-\sin(x)": lambda x: -sin(x), r"\cos(x)": cos},
    ("exercices.txt", 1): {"f'(x)": lambda x: cos(x) - sin(x), "f(x)": lambda x: sin(x) + cos(x)},
    ("exercices.txt", 2): {"g'(x)": lambda x: 2 * sin(2 * x), "g(x)": lambda x: sin(x) ** 2 - cos(x) ** 2},
    ("exercices.txt", 3): {"h'(x)": lambda x: 1 / (1 + cos(x)), "h(x)": lambda x: sin(x) / (1 + cos(x))},
    ("exercices.txt", 4): {"k'(x)": lambda x: cos(2 * x), "k(x)": lambda x: sin(x) * cos(x)},
    ("exercices.txt", 5): {"m'(x)": lambda x: tan(x) ** 2, "m(x)": lambda x: tan(x) - x},
    ("exercices.txt", 6): {"f'(x)": lambda x: cos(x) / (1 + sin(x)) ** 2, "f(x)": lambda x: sin(x) / (1 + sin(x))},
    ("exercices.txt", 7): {r"\cos(2x) - \frac{1}{2}": lambda x: cos(2 * x) - 0.5},
    ("exercices.txt", 8): {r"\sin(x) - \frac{\sqrt{3}}{2}": lambda x: sin(x) - math.sqrt(3) / 2},
    ("exercices.txt", 9): {r"\cos(2x) - \frac{1}{2}": lambda x: cos(2 * x) - 0.5},
    ("exercices.txt", 10): {r"\tan(x) - 1": lambda x: tan(x) - 1},
    ("exercices.txt", 11): {r"\sin(x) + \cos(x) - 1": lambda x: sin(x) + cos(x) - 1},
}


def tex_value(tex):
    """LaTeX simple -> nombre (π, fractions, racines, ±∞)."""
    t = tex.strip().replace(r"\dfrac", r"\frac").replace(r"\tfrac", r"\frac")
    t = t.replace(r"\left", "").replace(r"\right", "")
    if t in (r"+\infty", r"\infty"):
        return math.inf
    if t == r"-\infty":
        return -math.inf
    for _ in range(6):
        t = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", t)
        t = re.sub(r"\\frac(\d)(\d)", r"((\1)/(\2))", t)
        t = re.sub(r"\\sqrt\{([^{}]*)\}", r"math.sqrt(\1)", t)
    t = t.replace(r"\pi", "math.pi").replace("{", "(").replace("}", ")")
    t = re.sub(r"(\d)\s*(math\.)", r"\1*\2", t)
    t = re.sub(r"\)\s*(math\.|\()", r")*\1", t)
    return eval(t, {"math": math})  # noqa: S307 — expressions du fichier, contrôlées


def split_top(s):
    parts, depth, buf = [], 0, ""
    for c in s:
        if c in "{(":
            depth += 1
        elif c in "})":
            depth -= 1
        if c == "," and depth == 0:
            parts.append(buf.strip())
            buf = ""
        else:
            buf += c
    parts.append(buf.strip())
    return parts


def tables(path):
    lignes = path.read_text(encoding="utf-8").split("\n")
    res, cur = [], None
    for ln in lignes:
        if re.match(r"^:{3,}\s*tableau\b", ln.strip()):
            cur = []
        elif cur is not None and ln.strip() == ":::":
            res.append(cur)
            cur = None
        elif cur is not None and ln.strip():
            label, spec = re.match(r"^(.+?)\s*:\s*(.*)$", ln.strip()).groups()
            cur.append((label.strip(), split_top(spec)))
    return res


def safe(f, x):
    try:
        return f(x)
    except (ZeroDivisionError, ValueError, OverflowError):
        return math.nan


def verifier(nom, k, rows, fonctions, erreurs):
    try:
        xs = [tex_value(v) for v in rows[0][1]]
    except (SyntaxError, NameError, TypeError):
        erreurs.append(f"{nom} tableau {k} : valeurs de x illisibles ({', '.join(rows[0][1])})")
        return
    n = len(xs)
    eps = 1e-6
    for label, entries in rows[1:]:
        f = fonctions.get(label)
        where = f"{nom} tableau {k} « {label} »"
        if f is None:
            erreurs.append(f"{where} : fonction non déclarée")
            continue
        if len(entries) == 2 * n - 1:  # signes
            for s, tok in enumerate(entries):
                if s % 2 == 1:
                    a, b = xs[s // 2], xs[s // 2 + 1]
                    for t in (0.25, 0.5, 0.75):
                        y = safe(f, a + t * (b - a))
                        if tok == "+" and not y > 0 or tok == "-" and not y < 0:
                            erreurs.append(f"{where} : signe {tok} faux sur ]{a:.3f};{b:.3f}[ (valeur {y:.3g})")
                            break
                elif tok == "z":
                    y = safe(f, xs[s // 2])
                    if not abs(y) < 1e-9:
                        erreurs.append(f"{where} : zéro annoncé en x={xs[s // 2]:.4f}, valeur {y:.3g}")
        elif len(entries) == n:  # variations
            for i in range(n - 1):
                a, b = xs[i], xs[i + 1]
                ya, yb = safe(f, a + eps * (b - a) * 10), safe(f, b - eps * (b - a) * 10)
                pa = entries[i].split("/")[0].replace(" ", "")
                pb = entries[i + 1].split("/")[0].replace(" ", "")
                side_a = pa[-1] if pa else ""
                side_b = pb[0] if pb and pb[0] in "+-" else (pb[1] if len(pb) > 1 else "")
                if side_a == "-" and side_b == "+" and not yb > ya:
                    erreurs.append(f"{where} : devrait croître sur [{a:.3f};{b:.3f}]")
                if side_a == "+" and side_b == "-" and not yb < ya:
                    erreurs.append(f"{where} : devrait décroître sur [{a:.3f};{b:.3f}]")
            for i, e in enumerate(entries):
                parts = e.split("/")
                prefix, vals = parts[0].replace(" ", ""), parts[1:]
                if prefix in ("R", ""):
                    continue
                x = xs[i]
                if "D" in prefix:
                    left = prefix.split("D")[0]
                    right = prefix.split("D")[1]
                    checks = []
                    if left:
                        checks.append((vals[0], x - 1e-7))
                    if right:
                        checks.append((vals[-1], x + 1e-7))
                else:
                    checks = [(vals[0], x)]
                for tex, xx in checks:
                    try:
                        want = tex_value(tex)
                    except (SyntaxError, NameError, TypeError):
                        erreurs.append(f"{where} : valeur illisible « {tex} » en x={x:.4f}")
                        continue
                    got = safe(f, xx)
                    if math.isinf(want):
                        if not (abs(got) > 1e5 and math.copysign(1, got) == math.copysign(1, want)):
                            erreurs.append(f"{where} : {tex} annoncé en x≈{x:.4f}, valeur {got:.3g}")
                    elif not abs(got - want) < 1e-6:
                        erreurs.append(f"{where} : valeur {tex} annoncée en x={x:.4f}, calculée {got:.6g}")
        else:
            erreurs.append(f"{where} : nombre d'éléments incohérent")


if __name__ == "__main__":
    erreurs, total = [], 0
    for nom in ("cours.txt", "fiche.txt", "exercices.txt"):
        for k, rows in enumerate(tables(ICI / nom), start=1):
            total += 1
            fonctions = FONCTIONS.get((nom, k))
            if fonctions is None:
                erreurs.append(f"{nom} tableau {k} : aucune fonction déclarée pour le vérifier")
                continue
            verifier(nom, k, rows, fonctions, erreurs)
    for e in erreurs:
        print("  ✗", e)
    print(f"{total} tableaux vérifiés, {len(erreurs)} problème(s)")
    raise SystemExit(1 if erreurs else 0)
