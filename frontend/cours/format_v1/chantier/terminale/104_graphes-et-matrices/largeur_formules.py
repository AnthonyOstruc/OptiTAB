# -*- coding: utf-8 -*-
"""Repère les formules centrées trop larges pour un téléphone (estimation grossière).

    python largeur_formules.py [--couper]

--couper : une formule centrée d'une ligne contenant plusieurs « = » au niveau
principal est réécrite en aligned (un « = » par ligne).
"""
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
LIMITE = 21


def largeur(tex):
    t = tex
    # matrices : largeur de la ligne la plus large
    def mat(m):
        lignes = m.group(1).split(r"\\")
        return "(" + max((" ".join(c.strip() for c in l.split("&")) for l in lignes), key=lambda s: largeur(s)) + ")"
    for _ in range(3):
        t = re.sub(r"\\begin\{[pv]matrix\}((?:(?!\\begin).)*?)\\end\{[pv]matrix\}", mat, t)
    t = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}", lambda m: max(m.group(1), m.group(2), key=len), t)
    t = re.sub(r"\\(times|neq|to|cdot|leq|geq|iff)", "x", t)
    t = re.sub(r"\\text\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"[_^]\{[^{}]*\}", "", t)
    t = re.sub(r"[_^].", "", t)
    t = re.sub(r"\\[a-zA-Z]+", "", t)
    t = re.sub(r"[{}&\s]|\{,\}", "", t)
    return len(t) * 1.0


def niveau0_egal(s):
    prof, pos = 0, []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "{":
            prof += 1
        elif c == "}":
            prof -= 1
        elif s.startswith(r"\begin", i):
            prof += 1
        elif s.startswith(r"\end", i):
            prof -= 1
        elif c == "=" and prof == 0:
            pos.append(i)
        i += 1
    return pos


def traiter(chemin, couper):
    lignes = chemin.read_text(encoding="utf-8").split("\n")
    sortie, n = [], 0
    i = 0
    while i < len(lignes):
        l = lignes[i]
        s = l.strip()
        if s.startswith("$$") and s.endswith("$$") and len(s) > 4:
            tex = s[2:-2].strip()
            if largeur(tex) > LIMITE:
                pos = niveau0_egal(tex)
                if couper and len(pos) >= 2 and "aligned" not in tex:
                    morceaux, d = [], 0
                    for p in pos:
                        morceaux.append(tex[d:p].strip())
                        d = p + 1
                    morceaux.append(tex[d:].strip())
                    corps = [morceaux[0] + " &= " + morceaux[1]] + ["&= " + m for m in morceaux[2:]]
                    sortie += ["$$", r"\begin{aligned}"] + [c + r" \\" for c in corps[:-1]] + [corps[-1], r"\end{aligned}", "$$"]
                    i += 1
                    continue
                n += 1
                print(f"{chemin.name}:{i + 1}: {largeur(tex):.0f} : {tex[:90]}")
        elif s == "$$" or s.startswith(r"\begin{aligned}"):
            pass
        elif i > 0 and lignes[i - 1].strip() in ("$$", r"\begin{aligned}") or (s.endswith(r"\\") and "&" in s) or (s.startswith("&") or "&=" in s):
            if "&" in s and largeur(s) > LIMITE:
                k = s.find("&=")
                fin = s.endswith(r"\\")
                corps = s[:-2].rstrip() if fin else s
                if couper and k >= 0:
                    pos = [p for p in niveau0_egal(corps) if p > k + 1]
                    if pos:
                        morceaux, d = [], 0
                        for p in pos:
                            morceaux.append(corps[d:p].rstrip())
                            d = p + 1
                        morceaux.append(corps[d:].strip())
                        neuf = [morceaux[0] + r" \\"] + ["&= " + m + r" \\" for m in morceaux[1:]]
                        if not fin:
                            neuf[-1] = neuf[-1][:-3]
                        sortie += neuf
                        i += 1
                        continue
                n += 1
                print(f"{chemin.name}:{i + 1}: {largeur(s):.0f} (aligned) : {s[:90]}")
        sortie.append(l)
        i += 1
    if couper:
        chemin.write_text("\n".join(sortie), encoding="utf-8")
    return n


couper = "--couper" in sys.argv
total = sum(traiter(ICI / f, couper) for f in ("cours_112.txt", "fiche_49.txt", "exercices.txt"))
print(total, "formule(s) à revoir")
