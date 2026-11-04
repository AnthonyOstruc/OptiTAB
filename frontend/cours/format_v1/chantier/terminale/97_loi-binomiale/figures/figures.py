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

    def tex_chemin(c):
        # petite espace entre les lettres : deux barres consécutives restent séparées
        return r"\,".join(tex_issue(l) for l in c)

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
        issue = tex_chemin(c)
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


# ------------------------------------------------------------------ finition 2026-11-02
# Diagrammes des corrigés : P(X <= k) ou P(X >= k) colorié. Toutes les valeurs (barres ET
# étiquettes) sont calculées ici ; verif_loi_binomiale.py recalcule les mêmes nombres.


def fr(x, d=3):
    """Nombre arrondi à d décimales, virgule française pour LaTeX."""
    return f"{x:.{d}f}".replace(".", "{,}")


def somme(n, p, ks):
    v = loi(n, p)
    return sum(v[k] for k in ks)


def diagramme(n, p, kmax, groupes, ymax, yticks, xticks, notes, bar_width, kmin=0,
              width="7.25cm", height="4.1cm", minor=None, prec=2):
    """groupes : [(style, liste de k)] ; notes : code TikZ (axis cs) des étiquettes."""
    v = loi(n, p)
    plots = "\n".join(rf"  \addplot[{st}] coordinates {{{coords(v, ks)}}};" for st, ks in groupes if ks)
    mi = f", minor xtick={{{minor}}}" if minor else ""
    return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[{BARRES}, width={width}, height={height}, bar width={bar_width}pt,
  xmin={kmin - 0.7}, xmax={kmax + 0.7}, ymin=0, ymax={ymax}, xtick={{{xticks}}}{mi},
  ytick={{{yticks}}}, yticklabel style={{/pgf/number format/precision={prec}}}, ylabel={{$P(X=k)$}}]
{plots}
{notes}
\end{{axis}}
\end{{tikzpicture}}"""


def legende(x, y, style_fill, couleur, tex):
    """Petit carré de couleur + texte, dans le repère (axis cs)."""
    return (rf"  \fill[{style_fill}] ([xshift=-10pt,yshift=-3.5pt]axis cs:{x},{y}) rectangle ++(7pt,7pt);" "\n"
            rf"  \node[anchor=west,inner sep=1.2pt,font=\normalsize,text={couleur}] at (axis cs:{x},{y}) {{{tex}}};")


LEG_VERT = "otGreen!75,draw=otGreenDark,line width=0.5pt"
LEG_ORANGE = "otOrange!75,draw=otOrange!80!black,line width=0.5pt"
TV, TO = "otGreenDark", "otOrange!80!black"


def cours_complement():
    a, b = somme(10, 0.25, range(5)), somme(10, 0.25, range(5, 11))
    notes = (legende(6.3, 0.272, LEG_ORANGE, TO, rf"$P(X\le4)\approx{fr(a)}$") + "\n"
             + legende(6.3, 0.228, LEG_VERT, TV, rf"$P(X\ge5)\approx{fr(b)}$") + "\n"
             + rf"  \node[anchor=west,inner sep=1.2pt,font=\normalsize,text=otGreenDark] at (axis cs:6.08,0.18) {{$=1-P(X\le4)$}};")
    return diagramme(10, 0.25, 10, [(ORANGE, range(0, 5)), (VERT, range(5, 11))], 0.32, "0,0.1,0.2,0.3",
                     "0,1,2,3,4,5,6,7,8,9,10", notes, 9, prec=1)


def e1111_loi():
    a, b = somme(5, 0.6, range(3)), somme(5, 0.6, range(4, 6))
    notes = (legende(-0.35, 0.435, LEG_ORANGE, TO, rf"$P(X\le2)\approx{fr(a)}$") + "\n"
             + legende(-0.35, 0.355, LEG_VERT, TV, rf"$P(X\ge4)\approx{fr(b)}$"))
    return diagramme(5, 0.6, 5, [(ORANGE, range(0, 3)), (BLEU_PALE, [3]), (VERT, range(4, 6))], 0.46,
                     "0,0.1,0.2,0.3,0.4", "0,1,2,3,4,5", notes, 16, width="6.6cm", height="4.3cm", prec=1)


def e1120_b14():
    a = somme(14, 0.6, range(7, 15))
    notes = (legende(0.0, 0.222, LEG_ORANGE, TO, r"$P(X\le6)$") + "\n"
             + legende(0.0, 0.175, LEG_VERT, TV, rf"$P(X\ge7)\approx{fr(a)}$"))
    return diagramme(14, 0.6, 14, [(ORANGE, range(0, 7)), (VERT, range(7, 15))], 0.24, "0,0.05,0.1,0.15,0.2",
                     "0,2,4,6,8,10,12,14", notes, 8, minor="1,3,5,7,9,11,13")


def e1118_b20():
    a = somme(20, 0.82, range(18, 21))
    notes = legende(1.0, 0.222, LEG_VERT, TV, rf"$P(X\ge18)\approx{fr(a)}$")
    return diagramme(20, 0.82, 20, [(BLEU_PALE, range(0, 18)), (VERT, range(18, 21))], 0.25, "0,0.05,0.1,0.15,0.2",
                     "0,2,4,6,8,10,12,14,16,18,20", notes, 6, kmin=0, minor="1,3,5,7,9,11,13,15,17,19")


def e1115_b12():
    a = somme(12, 0.75, range(8, 13))
    notes = (legende(0.0, 0.265, LEG_ORANGE, TO, r"$P(X\le7)$") + "\n"
             + legende(0.0, 0.225, LEG_VERT, TV, rf"$P(X\ge8)\approx{fr(a)}$"))
    return diagramme(12, 0.75, 12, [(ORANGE, range(0, 8)), (VERT, range(8, 13))], 0.29, "0,0.1,0.2",
                     "0,1,2,3,4,5,6,7,8,9,10,11,12", notes, 9, prec=1)


def e1113_b25():
    a = somme(25, 0.35, range(10, 26))
    notes = (legende(13.6, 0.138, LEG_ORANGE, TO, r"$P(X\le9)$") + "\n"
             + legende(13.6, 0.112, LEG_VERT, TV, rf"$P(X\ge10)\approx{fr(a)}$"))
    return diagramme(25, 0.35, 25, [(ORANGE, range(0, 10)), (VERT, range(10, 26))], 0.18, "0,0.05,0.1,0.15",
                     "0,5,10,15,20,25", notes, 5, minor="1,2,3,4,6,7,8,9,11,12,13,14,16,17,18,19,21,22,23,24")


def e1116_b40():
    a = somme(40, 0.15, range(0, 5))
    notes = legende(9.3, 0.175, LEG_VERT, TV, rf"$P(X\le4)\approx{fr(a)}$")
    return diagramme(40, 0.15, 16, [(VERT, range(0, 5)), (BLEU_PALE, range(5, 17))], 0.19, "0,0.05,0.1,0.15",
                     "0,2,4,6,8,10,12,14,16", notes, 8, minor="1,3,5,7,9,11,13,15")


def e1112_decision():
    a, b = somme(50, 0.06, range(0, 7)), 1 - somme(50, 0.06, range(0, 7))
    notes = (legende(7.6, 0.225, LEG_VERT, TV, rf"$P(X\le6)\approx{fr(a)}$") + "\n"
             + legende(7.6, 0.175, LEG_ORANGE, TO, rf"$P(X\ge7)\approx{fr(b)}$") + "\n"
             + rf"  \node[anchor=west,inner sep=1.2pt,font=\otRegular\fontsize{{8.5}}{{10}}\selectfont,text=otMuted] at (axis cs:7.38,0.135) {{arrêt à tort}};"
             + "\n" + r"  \draw[seuil] (axis cs:6.5,0) -- (axis cs:6.5,0.25);")
    return diagramme(50, 0.06, 14, [(VERT, range(0, 7)), (ORANGE, range(7, 15))], 0.27, "0,0.05,0.1,0.15,0.2,0.25",
                     "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14", notes, 8)


def e1121_seuil_n():
    """Probabilité d'au moins un rendez-vous, 1 - 0,85^n, pour n = 10 à 24, et seuil 0,95."""
    pts_b = " ".join(f"({n},{1 - 0.85 ** n:.5f})" for n in range(10, 19))
    pts_v = " ".join(f"({n},{1 - 0.85 ** n:.5f})" for n in range(19, 25))
    return rf"""
\begin{{tikzpicture}}
\begin{{axis}}[{BARRES}, width=7.0cm, height=4.1cm, bar width=8pt,
  xmin=9.3, xmax=24.7, ymin=0.75, ymax=1.0, xtick={{10,12,14,16,18,19,20,22,24}},
  ytick={{0.75,0.8,0.85,0.9,0.95,1}}, xlabel={{$n$}}, ylabel={{$1-0{{,}}85^n$}}]
  \addplot[{BLEU}] coordinates {{{pts_b}}};
  \addplot[{VERT}] coordinates {{{pts_v}}};
  \draw[seuil] (axis cs:9.3,0.95) -- (axis cs:24.7,0.95);
  \node[anchor=west,inner sep=1.2pt,font=\normalsize,text=otOrange!80!black] at (axis cs:24.75,0.95) {{$0{{,}}95$}};
  \node[anchor=south west,inner sep=1.2pt,font=\normalsize,text=otGreenDark] at (axis cs:9.6,0.955) {{dès $n=19$ : $1-0{{,}}85^{{19}}\approx{fr(1 - 0.85 ** 19)}$}};
\end{{axis}}
\end{{tikzpicture}}"""


def arbre_lancers(corrige):
    """Schéma de Bernoulli à 3 lancers francs (réussite R, p = 0,7).
    Énoncé : seul le premier poids 0,7 est donné, cases vides ailleurs ; corrigé : tout en vert."""
    lx = [0.0, 1.6, 3.2, 4.8]
    dy = [1.6, 0.8, 0.4]
    pos = {"": (0.0, 0.0)}
    for niveau in range(1, 4):
        for chemin in [c for c in list(pos) if len(c) == niveau - 1]:
            x, y = pos[chemin]
            pos[chemin + "R"] = (lx[niveau], y + dy[niveau - 1])
            pos[chemin + "E"] = (lx[niveau], y - dy[niveau - 1])

    def nom(c):
        return "n" + (c or "0")

    def tex(l):
        return "R" if l == "R" else r"\overline{R}"

    L = [r"\begin{tikzpicture}[font=\normalsize]",
         r"\node[circle,fill=otNavy,inner sep=0pt,minimum size=4pt] (n0) at (0,0) {};"]
    for c, (x, y) in pos.items():
        if c:
            L.append(rf"\node[inner sep=2.2pt,text=otNavy] ({nom(c)}) at ({x},{y}) {{${tex(c[-1])}$}};")
    for c in pos:
        if not c:
            continue
        parent = c[:-1]
        a = f"{nom(parent)}.east" if parent else "n0"
        b = f"{nom(c)}.west"
        deux = corrige and len(c) == 3 and c.count("R") == 2
        trait = r"otGreenDark,line width=1.3pt" if deux else r"otNavy!65,line width=0.6pt"
        L.append(rf"\draw[{trait}] ({a}) -- ({b});")
        poids = "0{,}7" if c[-1] == "R" else "0{,}3"
        ancre = "south east" if c[-1] == "R" else "north east"
        dec = "yshift=0.6pt" if c[-1] == "R" else "yshift=-0.6pt"
        donne = (c == "R")
        if corrige or donne:
            couleur = "otInk" if donne else "otGreenDark"
            L.append(rf"\node[anchor={ancre},{dec},inner sep=1.3pt,font=\small,text={couleur}] at ($({a})!0.5!({b})$) {{${poids}$}};")
        else:
            L.append(rf"\node[anchor={ancre},{dec},draw=otMuted,line width=0.5pt,minimum width=0.62cm,minimum height=0.36cm,inner sep=0pt] at ($({a})!0.5!({b})$) {{}};")
    feuilles = sorted([c for c in pos if len(c) == 3], key=lambda c: -pos[c][1])
    # corrigé : sans la colonne « issue » (déjà lisible sur les nœuds) pour rester lisible au téléphone
    if corrige:
        L.append(r"\node[anchor=south,inner sep=1pt,font=\otMedium\fontsize{8.5}{10}\selectfont,text=otMuted] at (5.55,3.1) {$X$};")
        L.append(r"\node[anchor=south west,inner sep=1pt,font=\otMedium\fontsize{8.5}{10}\selectfont,text=otMuted] at (5.95,3.1) {probabilité};")
    else:
        L.append(r"\node[anchor=south west,inner sep=1pt,font=\otMedium\fontsize{8.5}{10}\selectfont,text=otMuted] at (5.3,3.1) {issue};")
    for c in feuilles:
        x, y = pos[c]
        k = c.count("R")
        if not corrige:
            L.append(rf"\node[anchor=west,inner sep=1pt,text=otInk] at (5.3,{y}) {{${r'\,'.join(tex(l) for l in c)}$}};")
        else:
            pr = 0.7 ** k * 0.3 ** (3 - k)
            coul = "otOrange!80!black" if k == 2 else "otInk"
            L.append(rf"\node[inner sep=1pt,text={coul}] at (5.55,{y}) {{${k}$}};")
            L.append(rf"\node[anchor=west,inner sep=1pt,text=otGreenDark] at (5.95,{y}) {{${fr(pr)}$}};")
    if corrige:
        L.append(rf"\node[anchor=north west,inner sep=1pt,text=otGreenDark,align=left] at (-0.1,-3.2) "
                 rf"{{$3$ chemins à $2$ réussites :\\$P(X=2)=3\times{fr(0.7 ** 2 * 0.3)}={fr(3 * 0.7 ** 2 * 0.3)}$}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def n1_loi():
    a = somme(3, 0.7, [2, 3])
    v = loi(3, 0.7)
    notes = (legende(-0.35, 0.535, LEG_VERT, TV, rf"$P(X\ge2)={fr(a)}$") + "\n"
             + "\n".join(rf"  \node[anchor=south,inner sep=1.5pt,font=\otRegular\fontsize{{8.5}}{{10}}\selectfont,text=otInk] at (axis cs:{k},{v[k]:.5f}) {{{fr(v[k])}}};" for k in range(4)))
    return diagramme(3, 0.7, 3, [(BLEU_PALE, [0, 1]), (VERT, [2, 3])], 0.56, "0,0.1,0.2,0.3,0.4,0.5", "0,1,2,3",
                     notes, 20, width="5.6cm", height="4.3cm", prec=1)


FIGURES = {
    "cours_complement": cours_complement(),
    "e1111_loi": e1111_loi(),
    "e1120_b14": e1120_b14(),
    "e1118_b20": e1118_b20(),
    "e1115_b12": e1115_b12(),
    "e1113_b25": e1113_b25(),
    "e1116_b40": e1116_b40(),
    "e1112_decision": e1112_decision(),
    "e1121_seuil_n": e1121_seuil_n(),
    "n1_arbre_enonce": arbre_lancers(False),
    "n1_arbre_corrige": arbre_lancers(True),
    "n1_loi": n1_loi(),
    "arbre_schema": arbre_schema(),
    "loi_qcm": loi_qcm(),
    "formes_n20": formes_n20(),
    "cumul_qcm": cumul_qcm(),
    "pois_b16": pois_b16(),
    "resistance_b30": resistance_b30(),
    "recyclage_b35": recyclage_b35(),
}
