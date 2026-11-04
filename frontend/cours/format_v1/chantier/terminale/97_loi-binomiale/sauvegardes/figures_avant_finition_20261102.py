# -*- coding: utf-8 -*-
"""Figures de la notion « Loi binomiale » (Terminale), style des livres OptiTAB.

Compilation (depuis frontend/cours/format_v1/outils/) :

    python figures_livre.py ../chantier/terminale/97_loi-binomiale [nom …] --planche

Toutes les probabilités tracées sont calculées ici exactement (math.comb) :
elles sont donc identiques à celles du texte (vérifiées par verif_loi_binomiale.py).
"""
from math import comb

# ------------------------------------------------------------------ outils


def loi(n, p):
    return [comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]


def cumul(n, p):
    s, out = 0.0, []
    for v in loi(n, p):
        s += v
        out.append(s)
    return out


def coords(valeurs, ks):
    return " ".join(f"({k},{valeurs[k]:.5f})" for k in ks)


BLEU = r"fill=otNavy!60,draw=otNavy,line width=0.5pt"
BLEU_PALE = r"fill=otNavy!22,draw=otNavy!55,line width=0.5pt"
VERT = r"fill=otGreen!75,draw=otGreenDark,line width=0.5pt"
ORANGE = r"fill=otOrange!75,draw=otOrange!80!black,line width=0.5pt"

# Réglages communs des diagrammes en bâtons (graduations y à virgule, pas de facteur 10^n)
BARRES = (r"otBarres, bar shift=0pt, enlarge x limits=false, clip=false, scaled y ticks=false, "
          r"yticklabel style={/pgf/number format/fixed,/pgf/number format/precision=2}, "
          r"xlabel={$k$}, every axis x label/.style={at={(current axis.south east)},anchor=north west,"
          r"font=\normalsize,text=otMuted,xshift=2pt,yshift=-1pt}")


# ------------------------------------------------------------------ arbre n = 3


def arbre_schema():
    """Arbre pondéré d'un schéma de Bernoulli à 3 épreuves (cas général p, 1 - p)."""
    lx = [0.0, 1.75, 3.5, 5.25]
    dy = [1.6, 0.8, 0.4]
    pos = {"": (0.0, 0.0)}
    for niveau in range(1, 4):
        for chemin in [c for c in list(pos) if len(c) == niveau - 1]:
            x, y = pos[chemin]
            pos[chemin + "S"] = (lx[niveau], y + dy[niveau - 1])
            pos[chemin + "E"] = (lx[niveau], y - dy[niveau - 1])

    def nom(c):
        return "n" + (c or "R")

    def tex_issue(lettre):
        return r"S" if lettre == "S" else r"\overline{S}"

    proba = {
        3: r"p^3", 2: r"p^2(1-p)", 1: r"p\,(1-p)^2", 0: r"(1-p)^3",
    }
    lignes = [r"\begin{tikzpicture}[font=\normalsize]"]
    lignes.append(r"\node[circle,fill=otNavy,inner sep=0pt,minimum size=4pt] (nR) at (0,0) {};")
    for c, (x, y) in pos.items():
        if not c:
            continue
        lignes.append(rf"\node[inner sep=2.2pt,text=otNavy] ({nom(c)}) at ({x},{y}) {{${tex_issue(c[-1])}$}};")
    for c in pos:
        if not c:
            continue
        parent = c[:-1]
        a = f"{nom(parent)}.east" if parent else "nR"
        b = f"{nom(c)}.west"
        lignes.append(rf"\draw[otNavy!65,line width=0.6pt] ({a}) -- ({b});")
        poids = "p" if c[-1] == "S" else "1-p"
        ancre = "south east" if c[-1] == "S" else "north east"
        dec = "yshift=0.6pt" if c[-1] == "S" else "yshift=-0.6pt"
        lignes.append(rf"\node[anchor={ancre},{dec},inner sep=1.3pt,font=\small,text=otInk] "
                      rf"at ($({a})!0.5!({b})$) {{${poids}$}};")
    # feuilles : issue et probabilité ; en vert, les 3 chemins à 2 succès
    feuilles = [c for c in pos if len(c) == 3]
    feuilles.sort(key=lambda c: -pos[c][1])
    for c in feuilles:
        x, y = pos[c]
        k = c.count("S")
        couleur = "otGreenDark" if k == 2 else "otInk"
        issue = "".join(tex_issue(l) for l in c)
        lignes.append(rf"\node[anchor=west,inner sep=1pt,text={couleur}] at (5.75,{y}) {{${issue}$}};")
        lignes.append(rf"\node[anchor=west,inner sep=1pt,text={couleur}] at (7.0,{y}) {{${proba[k]}$}};")
    lignes.append(r"\node[anchor=north west,inner sep=1pt,text=otGreenDark] at (-0.1,-3.25) "
                  r"{$3$ chemins à $2$ succès : $P(X=2)=3\,p^2(1-p)$};")
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


# ------------------------------------------------------------------ QCM : B(10 ; 0,25)

QCM = loi(10, 0.25)
QCM_CUMUL = cumul(10, 0.25)


def loi_qcm():
    return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[{BARRES}, width=7.4cm, height=4.1cm, bar width=9pt,
  xmin=-0.7, xmax=10.7, ymin=0, ymax=0.32, xtick={{0,1,2,3,4,5,6,7,8,9,10}}, ytick={{0,0.1,0.2,0.3}},
  ylabel={{$P(X=k)$}}]
  \addplot[{BLEU}] coordinates {{{coords(QCM, range(11))}}};
  \draw[seuil] (axis cs:2.5,0) -- (axis cs:2.5,0.305);
  \node[anchor=south,yshift=1pt,inner sep=1.2pt,font=\normalsize,text=otOrange!80!black] at (axis cs:2.5,0.305) {{$E(X)=2{{,}}5$}};
  \node[anchor=east,inner sep=1.2pt,font=\normalsize,text=otNavy] at (axis cs:10.5,0.2) {{$\mathcal{{B}}(10\,;0{{,}}25)$}};
\end{{axis}}
\end{{tikzpicture}}"""


def cumul_qcm():
    return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[{BARRES}, width=7.1cm, height=4.4cm, bar width=9pt,
  xmin=-0.7, xmax=10.7, ymin=0, ymax=1.08, xtick={{0,1,2,3,4,5,6,7,8,9,10}}, ytick={{0,0.2,0.4,0.6,0.8,1}},
  yticklabel style={{/pgf/number format/precision=1}}, ylabel={{$P(X\le k)$}}]
  \addplot[{BLEU}] coordinates {{{coords(QCM_CUMUL, [0, 1, 2, 3, 4] + list(range(6, 11)))}}};
  \addplot[{VERT}] coordinates {{{coords(QCM_CUMUL, [5])}}};
  \draw[seuil] (axis cs:-0.7,0.95) -- (axis cs:10.7,0.95);
  \node[anchor=west,inner sep=1.2pt,font=\normalsize,text=otOrange!80!black] at (axis cs:10.75,0.95) {{$0{{,}}95$}};
\end{{axis}}
\end{{tikzpicture}}"""


def formes_n20():
    """Trois lois B(20 ; p) l'une sous l'autre : la position dépend de p."""
    blocs = []
    for i, (p, ptex, e) in enumerate([(0.2, "0{,}2", 4), (0.5, "0{,}5", 10), (0.8, "0{,}8", 16)]):
        v = loi(20, p)
        if p < 0.5:
            etiq = rf"\node[anchor=north east,inner sep=1.2pt,font=\normalsize,text=otNavy] at (axis cs:20.4,0.235) {{$\mathcal{{B}}(20\,;{ptex})$}};"
        else:
            etiq = rf"\node[anchor=north west,inner sep=1.2pt,font=\normalsize,text=otNavy] at (axis cs:-0.4,0.235) {{$\mathcal{{B}}(20\,;{ptex})$}};"
        xl = "" if i == 2 else ", xlabel={}"
        if p > 0.5:
            etiq_e = rf"\node[anchor=east,inner sep=1.2pt,font=\normalsize,text=otOrange!80!black] at (axis cs:{e - 0.55},0.222) {{$E(X)={e}$}};"
        else:
            etiq_e = rf"\node[anchor=west,inner sep=1.2pt,font=\normalsize,text=otOrange!80!black] at (axis cs:{e + 0.35},0.215) {{$E(X)={e}$}};"
        blocs.append(rf"""\begin{{axis}}[{BARRES}{xl}, at={{(0,{-2.75 * i}cm)}}, width=7.6cm, height=1.95cm, bar width=5pt,
  xmin=-0.6, xmax=20.6, ymin=0, ymax=0.25, xtick={{0,5,10,15,20}}, minor xtick={{1,2,3,4,6,7,8,9,11,12,13,14,16,17,18,19}},
  ytick={{0,0.1,0.2}}, yticklabel style={{/pgf/number format/precision=1}}]
  \addplot[{BLEU}] coordinates {{{coords(v, range(21))}}};
  \draw[seuil] (axis cs:{e},0) -- (axis cs:{e},0.235);
  {etiq_e}
  {etiq}
\end{{axis}}""")
    return "\\begin{tikzpicture}\n" + "\n".join(blocs) + "\n\\end{tikzpicture}"


# ------------------------------------------------------------------ exercices


def pois_b16():
    v = loi(16, 0.5)
    return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[{BARRES}, width=7.3cm, height=4.1cm, bar width=7pt,
  xmin=-0.6, xmax=16.6, ymin=0, ymax=0.23, xtick={{0,2,4,6,8,10,12,14,16}}, minor xtick={{1,3,5,7,9,11,13,15}},
  ytick={{0,0.05,0.1,0.15,0.2}}, ylabel={{$P(X=k)$}}]
  \addplot[{BLEU}] coordinates {{{coords(v, range(11))}}};
  \addplot[{VERT}] coordinates {{{coords(v, range(11, 17))}}};
  \draw[seuil] (axis cs:8,0) -- (axis cs:8,0.216);
  \node[anchor=south,yshift=1pt,inner sep=1.2pt,font=\normalsize,text=otOrange!80!black] at (axis cs:8,0.216) {{$E(X)=8$}};
  \node[anchor=south,inner sep=1.2pt,font=\normalsize,text=otGreenDark] at (axis cs:13.5,0.135) {{$P(X>10)\approx0{{,}}105$}};
\end{{axis}}
\end{{tikzpicture}}"""


def resistance_b30():
    v = loi(30, 0.08)
    return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[{BARRES}, width=7.4cm, height=4.1cm, bar width=10pt,
  xmin=-0.7, xmax=12.7, ymin=0, ymax=0.3, xtick={{0,1,2,3,4,5,6,7,8,9,10,11,12}},
  ytick={{0,0.1,0.2,0.3}}, yticklabel style={{/pgf/number format/precision=1}}, ylabel={{$P(X=k)$}}]
  \addplot[{ORANGE}] coordinates {{{coords(v, range(0, 3))}}};
  \addplot[{VERT}] coordinates {{{coords(v, range(3, 6))}}};
  \addplot[{BLEU_PALE}] coordinates {{{coords(v, range(6, 13))}}};
  \fill[otGreen!75,draw=otGreenDark,line width=0.5pt] (axis cs:6.3,0.232) rectangle (axis cs:6.75,0.262);
  \node[anchor=west,inner sep=1.2pt,font=\normalsize,text=otGreenDark] at (axis cs:6.95,0.247) {{$P(3\le X\le5)$}};
  \fill[otOrange!75,draw=otOrange!80!black,line width=0.5pt] (axis cs:6.3,0.162) rectangle (axis cs:6.75,0.192);
  \node[anchor=west,inner sep=1.2pt,font=\normalsize,text=otOrange!80!black] at (axis cs:6.95,0.177) {{$P(X\le2)$}};
\end{{axis}}
\end{{tikzpicture}}"""


def recyclage_b35():
    v = loi(35, 0.25)
    return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[{BARRES}, width=7.3cm, height=4.1cm, bar width=6pt,
  xmin=-0.6, xmax=20.6, ymin=0, ymax=0.17, xtick={{0,2,4,6,8,10,12,14,16,18,20}}, minor xtick={{1,3,5,7,9,11,13,15,17,19}},
  ytick={{0,0.05,0.1,0.15}}, ylabel={{$P(X=k)$}}]
  \addplot[{BLEU_PALE}] coordinates {{{coords(v, list(range(0, 6)) + list(range(13, 21)))}}};
  \addplot[{VERT}] coordinates {{{coords(v, range(6, 13))}}};
  \node[anchor=south,inner sep=1.2pt,font=\normalsize,text=otGreenDark] at (axis cs:16.6,0.075) {{$P(6\le X\le12)$}};
  \node[anchor=north,inner sep=1.2pt,font=\normalsize,text=otGreenDark] at (axis cs:16.6,0.072) {{$\approx0{{,}}827$}};
\end{{axis}}
\end{{tikzpicture}}"""


FIGURES = {
    "arbre_schema": arbre_schema(),
    "loi_qcm": loi_qcm(),
    "formes_n20": formes_n20(),
    "cumul_qcm": cumul_qcm(),
    "pois_b16": pois_b16(),
    "resistance_b30": resistance_b30(),
    "recyclage_b35": recyclage_b35(),
}
