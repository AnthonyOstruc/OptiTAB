# -*- coding: utf-8 -*-
"""Figures de la notion « Notion de liste » (Terminale), style des livres OptiTAB.

Compilation : python ../../../outils/figures_livre.py <dossier_notion> [nom …] [--planche]

Les valeurs sont celles du texte (contrôlées par ../verif_listes.py). Les figures
de simulation EXÉCUTENT le programme imprimé dans le texte (même graine) ou
lisent son affichage : figure et texte ne peuvent pas diverger.
"""
import re
from math import comb
from pathlib import Path

ICI = Path(__file__).resolve().parent
NOTION = ICI.parent

PREAMBULE_EXTRA = r"""
\newfontfamily\otMono{FiraMono}[Extension=.otf, UprightFont=*-Regular, BoldFont=*-Medium]
\colorlet{otNavyTint}{otNavy!7}
\colorlet{otGreenTint}{otGreen!18}
\pgfplotsset{otSuite/.style={
  axis lines=left,
  axis line style={otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}},
  tick style={otMuted,line width=0.5pt}, major tick length=3pt, tick align=outside,
  ticklabel style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  grid=major, grid style={otRule!75,line width=0.35pt},
  every axis x label/.style={at={(current axis.south east)},anchor=west,font=\normalsize,text=otMuted,xshift=3pt},
  every axis y label/.style={at={(current axis.north west)},anchor=south,font=\normalsize,text=otMuted,yshift=4pt},
  scale only axis, clip=false, axis on top=false,
  /pgf/number format/use comma, /pgf/number format/1000 sep={\,},
}}
\tikzset{
  caseL/.style={draw=otNavy,fill=otNavyTint,line width=0.7pt},
  caseV/.style={draw=otGreenDark,fill=otGreenTint,line width=0.9pt},
  caseO/.style={draw=otMuted,fill=otRule!45,line width=0.6pt},
  caseB/.style={draw=otMuted,fill=white,line width=0.6pt},
  val/.style={font=\otMono\fontsize{10}{12}\selectfont,text=otInk},
  valV/.style={font=\otMono\bfseries\fontsize{10}{12}\selectfont,text=otGreenDark},
  idx/.style={font=\otMono\fontsize{9}{10}\selectfont,text=otNavy},
  idxV/.style={font=\otMono\bfseries\fontsize{9}{10}\selectfont,text=otGreenDark},
  lib/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},
  nomvar/.style={font=\otMono\fontsize{10}{12}\selectfont,text=otInk},
  legende/.style={font=\otRegular\fontsize{9}{10}\selectfont, text=otMuted, inner sep=1.5pt},
  legendeV/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otGreenDark, inner sep=1.5pt},
  legendeO/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otOrange!75!black, inner sep=1.5pt},
  legendeN/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otNavy, inner sep=1.5pt},
  fleche/.style={otMuted,line width=0.7pt,-{Stealth[length=2mm]}},
  ensemble/.style={draw=otNavy,line width=0.9pt},
  nombre/.style={font=\otRegular\fontsize{9.5}{11}\selectfont,text=otInk,inner sep=1pt},
  nombreV/.style={font=\otMedium\fontsize{9.5}{11}\selectfont,text=otGreenDark,inner sep=1pt},
  branche/.style={otNavy!65, line width=0.8pt, line cap=round},
  evt/.style={font=\normalsize, text=otNavy, inner sep=2pt},
}
"""

FIGURES = {}


def programme(fichier, motif):
    t = (NOTION / fichier).read_text(encoding="utf-8")
    for m in re.finditer(r"```python[ \t]*\n(.*?)\n[ \t]*```", t, re.S):
        if motif in m.group(1):
            return m.group(1)
    raise ValueError(f"programme introuvable : {motif}")


def executer(*codes):
    ns = {"__name__": "__main__"}
    for c in codes:
        exec(compile(c, "<texte>", "exec"), ns)
    return ns


def console_apres(fichier, motif):
    t = (NOTION / fichier).read_text(encoding="utf-8")
    k = t.index(motif)
    m = re.search(r"```console[ \t]*\n(.*?)\n[ \t]*```", t[k:], re.S)
    return [l.strip() for l in m.group(1).splitlines()]


def fr(v):
    return str(v).replace(".", "{,}")


def pts(points, couleur="otNavy", r=2.1):
    return "\n  ".join(rf"\fill[{couleur}] (axis cs:{x},{y:.5f}) circle ({r}pt);" for x, y in points)


# ================================================================ schémas de listes
def liste_termes(nom, valeurs, indices=True, rangs=True, vert=False, vide=False, largeur=1.15):
    """Cases d'une liste ; indices au-dessus, rangs u_n au-dessous."""
    L = [r"\begin{tikzpicture}[x=" + f"{largeur}" + r"cm,y=10mm]"]
    for i, v in enumerate(valeurs):
        L.append(rf"\draw[{'caseV' if vert else 'caseL'}] ({i},0) rectangle ++(1,0.8);")
        if not vide:
            L.append(rf"\node[val] at ({i}+0.5,0.4) {{{v}}};")
        if indices:
            L.append(rf"\node[{'idxV' if vert else 'idx'}] at ({i}+0.5,1.12) {{{i}}};")
        if rangs:
            L.append(rf"\node[{'legendeV' if vert else 'legendeN'}] at ({i}+0.5,-0.36) {{$u_{i}$}};")
    L.append(rf"\node[nomvar,anchor=east] at (-0.12,0.4) {{{nom} =}};")
    if indices:
        L.append(r"\node[lib,anchor=east] at (-0.12,1.12) {indice};")
    if rangs:
        L.append(r"\node[lib,anchor=east] at (-0.12,-0.36) {terme};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["liste_suite"] = liste_termes("u", [3, 5, 9, 17, 33])
FIGURES["e836_corrige"] = liste_termes("u", ["100", "70.0", "55.0", "47.5", "43.75"], vert=True, largeur=1.35)


def urne_remove():
    """urne = [1, 2, 3, 4, 5], t = [] ; tirage de 1 puis de 4 (affichage du cours)."""
    etats = [([1, 2, 3, 4, 5], [], None), ([2, 3, 4, 5], [1], 1), ([2, 3, 5], [1, 4], 4)]
    L = [r"\begin{tikzpicture}[x=8mm,y=10mm]"]
    for r, (urne, t, b) in enumerate(etats):
        y = -r * 1.55
        L.append(rf"\node[nomvar,anchor=east] at (-0.1,{y + 0.4}) {{urne}};")
        for i, v in enumerate(urne):
            L.append(rf"\draw[caseL] ({i},{y}) rectangle ++(1,0.8);")
            L.append(rf"\node[val] at ({i}+0.5,{y + 0.4}) {{{v}}};")
        if not urne:
            pass
        x0 = 6.6
        L.append(rf"\node[nomvar,anchor=east] at ({x0 - 0.1},{y + 0.4}) {{t}};")
        if t:
            for i, v in enumerate(t):
                style = "caseV" if i == len(t) - 1 else "caseL"
                txt = "valV" if i == len(t) - 1 else "val"
                L.append(rf"\draw[{style}] ({x0 + i},{y}) rectangle ++(1,0.8);")
                L.append(rf"\node[{txt}] at ({x0 + i}+0.5,{y + 0.4}) {{{v}}};")
        else:
            L.append(rf"\node[val,anchor=west] at ({x0},{y + 0.4}) {{[ ]}};")
        if b is not None:
            L.append(rf"\node[legendeV,anchor=south west] at (0,{y + 0.86}) {{boule {b} tirée : remove({b}), puis append({b})}};")
        else:
            L.append(rf"\node[legende,anchor=south west] at (0,{y + 0.86}) {{au départ}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["urne_remove"] = urne_remove()


# ================================================================ diagrammes de Venn
def venn(seulA, deux, seulB, nomA, nomB, titreE, remplir, autres=None, cols=2):
    """Deux ensembles A et B dans E ; nombres placés en grille dans chaque zone."""
    L = [r"\begin{tikzpicture}"]
    L.append(r"\draw[otMuted,line width=0.7pt,rounded corners=2mm] (-3.4,-2.1) rectangle (3.4,1.95);")
    L.append(rf"\node[legende,anchor=south west] at (-3.4,2.0) {{{titreE}}};")
    L.append(r"\fill[otNavy!6] (-0.85,-0.1) circle (1.75);")
    L.append(r"\fill[otGreen!10] (0.85,-0.1) circle (1.75);")
    L.append(r"\draw[ensemble] (-0.85,-0.1) circle (1.75);")
    L.append(r"\draw[ensemble,draw=otGreenDark] (0.85,-0.1) circle (1.75);")
    L.append(rf"\node[text=otNavy,anchor=east] at (-2.55,1.25) {{${nomA}$}};")
    L.append(rf"\node[text=otGreenDark,anchor=west] at (2.55,1.25) {{${nomB}$}};")
    if remplir:
        def grille(nombres, xs, ytop, style):
            for k, v in enumerate(nombres):
                c, r = k % len(xs), k // len(xs)
                L.append(rf"\node[{style}] at ({xs[c]:.3f},{ytop - r * 0.45:.3f}) {{{v}}};")
        rA = (len(seulA) + 1) // 2
        grille(seulA, [-2.1, -1.5], -0.1 + 0.225 * (rA - 1), "nombre")
        grille(deux, [0], -0.1 + 0.225 * (len(deux) - 1), "nombreV")
        rB = (len(seulB) + 1) // 2
        grille(seulB, [1.5, 2.1], -0.1 + 0.225 * (rB - 1), "nombre")
        if autres:
            L.append(rf"\node[legende,anchor=north east] at (3.4,-2.15) {{{autres}}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["venn_cours"] = venn([2, 4, 8, 10, 14, 16, 20], [6, 12, 18], [3, 9, 15], "A", "B",
                             r"$E = \{1, …, 20\}$", True, autres=r"hors de $A \cup B$ : 7 nombres")
FIGURES["venn_enonce"] = venn([], [], [], "A", "B", r"$E = \{1, …, 30\}$", False)
FIGURES["venn_corrige"] = venn([3, 6, 9, 12, 18, 21, 24, 27], [15, 30], [5, 10, 20, 25], "A", "B",
                               r"$E = \{1, …, 30\}$", True, autres=r"hors de $A \cup B$ : 16 nombres")


# ================================================================ suites
def nuage(u, ymin, ymax, ytick, xtick, largeur="7cm", hauteur="4.5cm", extra="", vert=None, ylabel="$u_n$"):
    p = [(n, v) for n, v in enumerate(u) if n != vert]
    v_pts = "" if vert is None else "\n  " + rf"\fill[otGreenDark] (axis cs:{vert},{u[vert]:.5f}) circle (2.7pt);"
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=""" + largeur + r""", height=""" + hauteur + r""", xmin=-0.5, xmax=""" + str(len(u) - 0.2) + r""",
  ymin=""" + str(ymin) + r""", ymax=""" + str(ymax) + r""", xtick=""" + xtick + r""", ytick=""" + ytick + r""",
  xlabel={$n$}, ylabel={""" + ylabel + r"""}]""" + extra + r"""
  """ + pts(p) + v_pts + r"""
\end{axis}
\end{tikzpicture}"""


_u = [2 * 1.5 ** n for n in range(12)]
FIGURES["seuil_liste"] = nuage(_u, 0, 190, "{0,50,100,150}", "{0,1,...,11}", extra=r"""
  \draw[seuil] (axis cs:-0.5,100) -- (axis cs:11.6,100);
  \node[legendeO,anchor=south west] at (axis cs:0,103) {seuil $100$};
  \draw[guide] (axis cs:10,0) -- (axis cs:10,115.33);
  \node[legendeV,anchor=east] at (axis cs:9.7,128) {$u_{10} \approx 115{,}33$};
  \node[legende,anchor=east] at (axis cs:8.7,76.9) {$u_9 \approx 76{,}89$};""", vert=10)

_u = [1000.0]
for _ in range(10):
    _u.append(1.02 * _u[-1] + 100)
_k = [v / 1000 for v in _u]
FIGURES["e840_enonce"] = nuage(_k, 0.8, 2.6, "{1,1.5,2,2.5}", "{0,1,...,10}", ylabel="$u_n$ (milliers d'euros)")
FIGURES["e840_corrige"] = nuage(_k, 0.8, 2.6, "{1,1.5,2,2.5}", "{0,1,...,10}", ylabel="$u_n$ (milliers d'euros)",
                                extra=r"""
  \draw[seuil] (axis cs:-0.5,2) -- (axis cs:10.6,2);
  \node[legendeO,anchor=south west] at (axis cs:0,2.04) {seuil $2\,000$ €};
  \draw[guide] (axis cs:8,0.8) -- (axis cs:8,2.03);
  \node[legendeV,anchor=north west] at (axis cs:8.2,1.95) {$u_8 \approx 2\,030$};""", vert=8)

_S = [2 - 0.5 ** n for n in range(11)]
FIGURES["e839_enonce"] = nuage(_S, 0.8, 2.3, "{1,1.5,2}", "{0,1,...,10}", ylabel="$S_n$")
FIGURES["e839_corrige"] = nuage(_S, 0.8, 2.3, "{1,1.5,2}", "{0,1,...,10}", ylabel="$S_n$", extra=r"""
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:-0.5,2) -- (axis cs:10.6,2);
  \node[legendeV,anchor=south east] at (axis cs:10.6,2.04) {limite $2$};""")


# ================================================================ histogrammes
def barres(freqs, probas, couleur_p, xmin, xmax, ymax, ytick, leg_x, largeur="7cm", hauteur="4.2cm", bw="16pt"):
    bars = " ".join(f"({k},{v:.4f})" for k, v in freqs)
    marques = ""
    leg = r"""
  \fill[otNavy!55,draw=otNavy] (""" + f"{leg_x}" + r""",3.92) rectangle ++(0.26,0.2);
  \node[legende,anchor=west] at (""" + f"{leg_x + 0.31}" + r""",4.02) {fréquence observée};"""
    if probas:
        marques = "\n  ".join(
            rf"\draw[{couleur_p},line width=1.8pt] (axis cs:{k - 0.38},{p:.5f}) -- (axis cs:{k + 0.38},{p:.5f});"
            for k, p in probas)
        leg += r"""
  \draw[""" + couleur_p + r""",line width=1.8pt] (""" + f"{leg_x - 0.03}" + r""",3.6) -- ++(0.32,0);
  \node[legende,anchor=west] at (""" + f"{leg_x + 0.31}" + r""",3.6) {probabilité $P(X = k)$};"""
    return r"""
\begin{tikzpicture}
\begin{axis}[otBarres, width=""" + largeur + r""", height=""" + hauteur + r""", bar width=""" + bw + r""", ymax=""" + str(ymax) + r""",
  enlarge x limits=0.05, xmin=""" + str(xmin) + r""", xmax=""" + str(xmax) + r""",
  xtick={""" + ",".join(str(k) for k, _ in freqs) + r"""}, ytick={""" + ytick + r"""},
  yticklabel style={/pgf/number format/fixed,/pgf/number format/precision=2},
  xlabel={$k$}, ylabel={fréquence}, clip=false,
  every axis y label/.style={at={(current axis.north west)},anchor=south,yshift=4pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  every axis x label/.style={at={(current axis.south east)},anchor=west,xshift=3pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}]
  \addplot[fill=otNavy!55,draw=otNavy] coordinates {""" + bars + r"""};
  """ + marques + r"""
\end{axis}""" + leg + r"""
\end{tikzpicture}"""


def histo_cours():
    lignes = console_apres("cours_105.txt", "E = [R.count(k)")
    eff = {int(l.split()[0]): int(l.split()[1]) for l in lignes}
    assert sum(eff.values()) == 10000
    freqs = [(k, eff[k] / 10000) for k in range(7)]
    probas = [(k, comb(6, k) / 64) for k in range(7)]
    return barres(freqs, probas, "otOrange!85!black", -0.5, 6.5, 0.36, "0.1,0.2,0.3", 4.3)


FIGURES["histo_binom6"] = histo_cours()


def e_n3(corrige):
    ns = executer(programme("exercices.txt", "R.append(x)\n") if False else programme("exercices.txt", "if random() < 0.4:"))
    R = ns["R"]
    freqs = [(k, R.count(k) / 10000) for k in range(6)]
    probas = [(k, comb(5, k) * 0.4 ** k * 0.6 ** (5 - k)) for k in range(6)] if corrige else None
    return barres(freqs, probas, "otGreenDark", -0.5, 5.5, 0.4, "0.1,0.2,0.3,0.4", 3.9)


FIGURES["e_n3_enonce"] = e_n3(False)
FIGURES["e_n3_corrige"] = e_n3(True)


# ================================================================ dénombrement
def grille(E, cond_vert, nom_cond, montrer=True, taille=0.95, vides=False, coin="x, y"):
    n = len(E)
    L = [r"\begin{tikzpicture}[x=" + f"{taille * 1.5}" + "cm,y=" + f"{taille * 0.8}" + "cm]"]
    for i, a in enumerate(E):
        L.append(rf"\node[idx] at (-0.5,{-i - 0.5}) {{{a}}};")
        L.append(rf"\node[idx] at ({i + 0.5},0.42) {{{a}}};")
    L.append(rf"\node[lib,anchor=south east] at (-0.1,0.15) {{{coin}}};")
    for i, a in enumerate(E):
        for j, b in enumerate(E):
            if vides:
                style, txt = "caseB", None
            elif i == j:
                style, txt = "caseO", "val"
            elif cond_vert(i, j):
                style, txt = "caseV", "valV"
            else:
                style, txt = "caseB", "val"
            L.append(rf"\draw[{style}] ({j},{-i - 1}) rectangle ++(1,1);")
            if txt and montrer:
                q = '"' if isinstance(a, str) else ""
                L.append(rf"\node[{txt},font=\otMono\fontsize{{8.5}}{{10}}\selectfont] at ({j + 0.5},{-i - 0.5}) {{[{a}, {b}]}};")
    if not vides:
        L.append(rf"\node[legendeV,anchor=north west] at (0,{-n - 0.15}) {{{nom_cond}}};")
        L.append(rf"\node[legende,anchor=north west] at (0,{-n - 0.62}) {{en gris : {coin[0]} = {coin[-1]}}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["grille_couples"] = grille(["a", "b", "c"], lambda i, j: i < j, "en vert : x < y (parties à 2 éléments)")
FIGURES["e_n2_enonce"] = grille([1, 2, 3, 4, 5], lambda i, j: False, "", vides=True, taille=0.82, coin="a, b")
FIGURES["e_n2_corrige"] = grille([1, 2, 3, 4, 5], lambda i, j: i < j, "en vert : a < b, les 10 parties", taille=0.82, coin="a, b")


def arbre_pf(corrige):
    """Arbre de trois lancers d'une pièce ; feuilles = triplets."""
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    dx = 1.8
    feuilles = []
    ys = {}
    n_f = 0
    for a in "PF":
        for b in "PF":
            for c in "PF":
                ys[a + b + c] = -n_f * 0.62
                n_f += 1
    for b2 in [a + b for a in "PF" for b in "PF"]:
        ys[b2] = (ys[b2 + "P"] + ys[b2 + "F"]) / 2
    for a in "PF":
        ys[a] = (ys[a + "P"] + ys[a + "F"]) / 2
    racine = (ys["P"] + ys["F"]) / 2
    L.append(rf"\fill[otNavy] (0,{racine:.3f}) circle (1.9pt);")
    for nom, y in ys.items():
        x = len(nom) * dx
        L.append(rf"\node[evt] (n{nom}) at ({x},{y:.3f}) {{{nom[-1]}}};")
    for nom, y in ys.items():
        if len(nom) == 1:
            L.append(rf"\draw[branche] (0,{racine:.3f}) -- (n{nom}.west);")
        else:
            L.append(rf"\draw[branche] (n{nom[:-1]}.east) -- (n{nom}.west);")
    if corrige:
        for nom in [k for k in ys if len(k) == 3]:
            style = "legendeV" if nom.count("P") == 2 else "legende"
            txt = ", ".join(f"'{c}'" for c in nom)
            L.append(rf"\node[{style},anchor=west,font=\otMono\fontsize{{8.5}}{{10}}\selectfont] at ([xshift=6pt]n{nom}.east) {{[{txt}]}};")
    L.append(rf"\node[lib] at ({dx},{racine + 2.75:.3f}) {{lancer 1}};")
    L.append(rf"\node[lib] at ({2 * dx},{racine + 2.75:.3f}) {{lancer 2}};")
    L.append(rf"\node[lib] at ({3 * dx},{racine + 2.75:.3f}) {{lancer 3}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["arbre_pf_enonce"] = arbre_pf(False)
FIGURES["arbre_pf_corrige"] = arbre_pf(True)


# ================================================================ sondages (nouveau-4)
def sondages(corrige):
    ns = executer(programme("exercices.txt", "def frequence(n, p):"))
    L = ns["L"]
    p = pts([(j, f) for j, f in enumerate(L)], r=1.5)
    if corrige:
        dedans = [(j, f) for j, f in enumerate(L) if abs(f - 0.52) <= 0.05]
        dehors = [(j, f) for j, f in enumerate(L) if abs(f - 0.52) > 0.05]
        p = pts(dedans, "otGreenDark", 1.5) + "\n  " + pts(dehors, "otOrange!85!black", 1.9)
    bande = r"""
  \fill[otGreen!14] (axis cs:0,0.47) rectangle (axis cs:200,0.57);
  \draw[otGreenDark,line width=0.7pt] (axis cs:0,0.47) -- (axis cs:200,0.47) (axis cs:0,0.57) -- (axis cs:200,0.57);
  \node[legendeV,anchor=west] at (axis cs:203,0.57) {$0{,}57$};
  \node[legendeV,anchor=west] at (axis cs:203,0.47) {$0{,}47$};""" if corrige else ""
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=7cm, height=4.6cm, xmin=0, xmax=205, ymin=0.42, ymax=0.62,
  xtick={0,50,100,150,200}, ytick={0.45,0.5,0.55,0.6},
  yticklabel style={/pgf/number format/fixed,/pgf/number format/precision=2},
  xlabel={$j$}, ylabel={fréquence}]""" + bande + r"""
  \draw[otNavy!60,line width=0.8pt,dash pattern=on 3pt off 2pt] (axis cs:0,0.52) -- (axis cs:200,0.52);
  \node[legendeN,anchor=west] at (axis cs:203,0.52) {$p = 0{,}52$};
  """ + p + r"""
\end{axis}
\end{tikzpicture}"""


FIGURES["sondages_enonce"] = sondages(False)
FIGURES["sondages_corrige"] = sondages(True)


# ================================================================ fréquences successives (nouveau-5)
def frequences(corrige):
    ns = executer(programme("exercices.txt", "f.append(c / n)"))
    f = ns["f"]
    coords = " ".join(f"({n},{f[n - 1]:.4f})" for n in list(range(1, 200)) + list(range(200, 2001, 5)))
    plus = r"""
  \fill[otGreen!14] (axis cs:100,0.1167) rectangle (axis cs:2000,0.2167);
  \draw[otGreenDark,line width=1pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,0.16667) -- (axis cs:2000,0.16667);
  \node[legendeV,anchor=west] at (axis cs:2030,0.16667) {$\frac{1}{6}$};
  \node[legendeV,anchor=south east] at (axis cs:2000,0.2167) {écart $\le 0{,}05$ dès $n = 100$};""" if corrige else ""
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=7cm, height=4.4cm, xmin=0, xmax=2000, ymin=0, ymax=0.42,
  xtick={0,500,1000,1500,2000}, ytick={0,0.1,0.2,0.3,0.4},
  yticklabel style={/pgf/number format/fixed,/pgf/number format/precision=1},
  xlabel={$n$}, ylabel={fréquence des 6}]""" + plus + r"""
  \addplot[courbe, line width=1pt] coordinates {""" + coords + r"""};
\end{axis}
\end{tikzpicture}"""


FIGURES["frequences_enonce"] = frequences(False)
FIGURES["frequences_corrige"] = frequences(True)


# ================================================================ marche aléatoire (nouveau-6)
def marche(corrige):
    ns = executer(programme("exercices.txt", "P.append(P[-1] + 1)"))
    P = ns["P"]
    chemin = " -- ".join(f"(axis cs:{k},{v})" for k, v in enumerate(P))
    plus = ""
    if corrige:
        zeros = [k for k in range(1, 21) if P[k] == 0]
        plus = "\n  " + "\n  ".join(rf"\fill[otGreenDark] (axis cs:{k},0) circle (2.8pt);" for k in zeros)
        plus += r"""
  \node[legendeV,anchor=south west] at (axis cs:8.5,0.45) {retours en $0$ : étapes $2$ et $6$};
  \node[legendeN,anchor=west] at (axis cs:1.5,1.45) {maximum $1$};
  \node[legendeO,anchor=north east] at (axis cs:19.8,-8.3) {position finale $-8$};"""
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=7.2cm, height=4.8cm, xmin=0, xmax=20.8, ymin=-9.6, ymax=2.6,
  xtick={0,2,...,20}, ytick={-8,-6,-4,-2,0,2}, xlabel={$k$}, ylabel={position $P[k]$}]
  \draw[otMuted,line width=0.7pt] (axis cs:0,0) -- (axis cs:20.8,0);
  \draw[otNavy,line width=1.1pt,line join=round] """ + chemin + r""";
  """ + "\n  ".join(rf"\fill[otNavy] (axis cs:{k},{v}) circle (1.5pt);" for k, v in enumerate(P)) + plus + r"""
\end{axis}
\end{tikzpicture}"""


FIGURES["marche_enonce"] = marche(False)
FIGURES["marche_corrige"] = marche(True)
