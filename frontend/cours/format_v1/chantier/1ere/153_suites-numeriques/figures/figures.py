# -*- coding: utf-8 -*-
"""Figures de la notion « Suites numériques » (Première), style des livres OptiTAB.

Compilées par outils/figures_livre.py : nuages de points en bleu marine (seconde
suite en vert), constructions en escalier en vert foncé, repères de lecture en
pointillés gris, seuils en orange.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  escalier/.style={otGreenDark,line width=1.1pt,line join=round},
  diag/.style={otMuted,line width=0.9pt},
  allu/.style={otOrange!85!black,line width=2.6pt,line cap=round},
  tete/.style={fill=otRed},
  ulab/.style={font=\normalsize,text=otGreenDark,inner sep=1pt},
}
\pgfplotsset{boite/.style={axis lines=left,
  every axis x label/.style={at={(axis description cs:1,0)},anchor=west,font=\normalsize,text=otMuted},
  every axis y label/.style={at={(axis description cs:0,1)},anchor=south,font=\normalsize,text=otMuted}}}
\newcommand{\carre}[3][otNavy]{\fill[#1] ($(axis cs:#2,#3)+(-2.1pt,-2.1pt)$) rectangle ++(4.2pt,4.2pt);}
\newcommand{\allumette}[4]{\draw[allu] (#1,#2) -- (#3,#4); \fill[tete] (#3,#4) circle (2.3pt);}
\newcommand{\allumetteV}[4]{\draw[otGreenDark,line width=2.6pt,line cap=round] (#1,#2) -- (#3,#4); \fill[tete] (#3,#4) circle (2.3pt);}
"""


def nuage(points, couleur="otNavy", carre=False):
    cmd = r"\carre" if carre else r"\pnt"
    return "\n".join(f"  {cmd}[{couleur}]{{{x}}}{{{y}}}" for x, y in points)


def escalier(f, u0, k):
    """Chemin de l'escalier : (u0,0) puis verticales / horizontales."""
    pts, u = [(u0, 0)], u0
    for _ in range(k):
        v = f(u)
        pts += [(u, v), (v, v)]
        u = v
    return " -- ".join(f"(axis cs:{x:g},{y:g})" for x, y in pts)


FIGURES = {}

# ---------------------------------------------------------------- cours
FIGURES["cours_nuage"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.6cm, xmin=-0.4, xmax=6.8, ymin=-5.6, ymax=13.6,
  xtick={1,2,3,4,5,6}, ytick={-4,4,8,12}, xlabel={$n$}, ylabel={$u_n$}]
""" + nuage([(k, k * k - 4 * k) for k in range(7)]) + r"""
  \node[etiq,anchor=west,text=otNavy] at (axis cs:0.6,10.6) {$u_n = n^2 - 4n$};
  \node[note,anchor=west] at (axis cs:0.6,7.6) {points $(n\,;u_n)$ non reliés};
\end{axis}
\end{tikzpicture}"""

FIGURES["cours_arith"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.8cm, xmin=-0.4, xmax=7.6, ymin=-0.8, ymax=12.6,
  xtick={1,2,3,4,5,6,7}, ytick={2,4,6,8,10,12}, xlabel={$n$}, ylabel={$u_n$}]
  \addplot[pale, dash pattern=on 4pt off 2.5pt, domain=-0.3:7.4] {1.5*x+1};
  \draw[otOrange,line width=1.1pt] (axis cs:3,5.5) -- (axis cs:4,5.5) -- (axis cs:4,7);
""" + nuage([(k, 1 + 1.5 * k) for k in range(8)]) + r"""
  \node[note,anchor=north,text=otOrange!80!black] at (axis cs:3.5,5.2) {$+1$};
  \node[note,anchor=west,text=otOrange!80!black] at (axis cs:4.12,6.1) {$+r$};
  \node[etiq,anchor=west,text=otNavy] at (axis cs:0.3,11.2) {$u_n = 1 + 1{,}5n$};
  \node[note,anchor=west] at (axis cs:0.3,9.3) {points alignés, pente $r = 1{,}5$};
\end{axis}
\end{tikzpicture}"""

_somme = []
for k in range(1, 7):
    x = (k - 1) * 0.6
    _somme.append(rf"\fill[otNavy!22] ({x},0) rectangle ({x + 0.6},{k * 0.6});")
    _somme.append(rf"\fill[otOrange!30] ({x},{k * 0.6}) rectangle ({x + 0.6},4.2);")
    _somme.append(rf"\node[note,anchor=north] at ({x + 0.3},-0.08) {{${k}$}};")
_grille = r"\draw[white,line width=1.2pt] (0,0) grid[step=0.6] (3.6,4.2);"
_escalier = r"\draw[otNavy,line width=1pt] (0,0) |- (0.6,0.6) |- (1.2,1.2) |- (1.8,1.8) |- (2.4,2.4) |- (3,3) |- (3.6,3.6) -- (3.6,0) -- cycle;"
_escalier2 = r"\draw[otOrange!85!black,line width=1pt] (0,0.6) |- (0.6,1.2) |- (1.2,1.8) |- (1.8,2.4) |- (2.4,3) |- (3,3.6) |- (3.6,4.2) -- (0,4.2) -- cycle;"
FIGURES["cours_somme"] = r"""
\begin{tikzpicture}
""" + "\n".join(_somme) + "\n" + _grille + "\n" + _escalier + "\n" + _escalier2 + r"""
\draw[cote] (0,-0.75) -- (3.6,-0.75) node[midway,coteTexte] {$n = 6$};
\draw[cote] (4.45,0) -- (4.45,4.2) node[midway,coteTexte] {$n + 1 = 7$};
\node[anchor=west,text=otNavy] at (-0.1,-1.45) {bleu : $S = 1 + 2 + \cdots + 6$};
\node[anchor=west,text=otOrange!80!black] at (-0.1,-2.05) {orange : la même somme};
\node[anchor=west,text=otGreenDark] at (-0.1,-2.85) {$2S = 6 \times 7$, donc $S = 21$};
\end{tikzpicture}"""

FIGURES["cours_geom"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.8cm, xmin=-0.4, xmax=7.6, ymin=-0.6, ymax=9.6,
  xtick={1,2,3,4,5,6,7}, ytick={2,4,6,8}, xlabel={$n$}, ylabel={$u_n$}]
""" + nuage([(k, round(0.5 * 1.5 ** k, 4)) for k in range(8)], "otGreenDark") + "\n" + \
    nuage([(k, 8 * 0.5 ** k) for k in range(8)], "otNavy", carre=True) + r"""
  \node[anchor=east,text=otGreenDark,align=right,font=\normalsize] at (axis cs:6.6,8.2) {$v_n = 0{,}5 \times 1{,}5^n$\\[1pt]{\otRegular\fontsize{8.5}{10}\selectfont $q > 1$ : croissante}};
  \node[anchor=west,text=otNavy,align=left,font=\normalsize] at (axis cs:0.45,6.2) {$w_n = 8 \times 0{,}5^n$\\[1pt]{\otRegular\fontsize{8.5}{10}\selectfont $0 < q < 1$ : décroissante}};
\end{axis}
\end{tikzpicture}"""

FIGURES["cours_toile"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=6.6cm, xmin=-0.2, xmax=5.2, ymin=-0.2, ymax=5.2,
  xtick={1,2,3,4,5}, ytick={1,2,3,4,5}]
  \addplot[diag, domain=0:5] {x};
  \addplot[courbe, domain=0:5] {0.5*x+2};
  \draw[guide] (axis cs:2.5,2.5) -- (axis cs:2.5,0);
  \draw[guide] (axis cs:3.25,3.25) -- (axis cs:3.25,0);
  \draw[escalier] """ + escalier(lambda u: 0.5 * u + 2, 1, 4) + r""";
  \pnt[otGreenDark]{1}{0} \pnt{4}{4}
  \node[ulab,anchor=north] at (axis cs:1,-0.62) {$u_0$};
  \node[ulab,anchor=north] at (axis cs:2.5,-0.62) {$u_1$};
  \node[ulab,anchor=north] at (axis cs:3.25,-0.62) {$u_2$};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:0.55,2.4) {$\mathcal{C}_f$};
  \node[etiq,text=otMuted,anchor=south west] at (axis cs:5.05,5.05) {$y = x$};
  \node[note,anchor=north west] at (axis cs:4.08,3.9) {$(4\,;4)$};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- 1424 (toile convergente)
_toile1 = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=7cm, xmin=-0.1, xmax=3.25, ymin=-0.1, ymax=3.25,
  xtick={0.5,1,1.5,2,2.5,3}, ytick={0.5,1,1.5,2,2.5,3},
  minor xtick={0.25,0.75,1.25,1.75,2.25,2.75}, minor ytick={0.25,0.75,1.25,1.75,2.25,2.75},
  grid=both, minor grid style={otRule!45,line width=0.3pt}, minor tick length=0pt]
  \addplot[diag, domain=0:3.1] {x};
  \addplot[courbe, domain=0:3.1] {0.5*x+1};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:0.3,1.2) {$\mathcal{C}_f$};
  \node[etiq,text=otMuted,anchor=west] at (axis cs:3.12,3.0) {$\Delta$};
%CORRIGE%
\end{axis}
\end{tikzpicture}"""
FIGURES["toile1_enonce"] = _toile1.replace("%CORRIGE%", "")
FIGURES["toile1_corrige"] = _toile1.replace("%CORRIGE%", r"""
  \draw[guide] (axis cs:1.5,1.5) -- (axis cs:1.5,0);
  \draw[guide] (axis cs:1.75,1.75) -- (axis cs:1.75,0);
  \draw[escalier] """ + escalier(lambda u: 0.5 * u + 1, 1, 3) + r""";
  \pnt[otGreenDark]{1}{0} \pnt{2}{2}
  \node[ulab,anchor=north] at (axis cs:1,-0.2) {$u_0$};
  \node[ulab,anchor=north] at (axis cs:1.5,-0.2) {$u_1$};
  \node[ulab,anchor=north] at (axis cs:1.75,-0.2) {$u_2$};
  \node[note,anchor=north west] at (axis cs:2.06,1.94) {$(2\,;2)$};""")

# ---------------------------------------------------------------- 1425 (toile divergente)
_toile2 = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.4cm, height=6.6cm, xmin=-0.2, xmax=6.4, ymin=-0.4, ymax=10.4,
  xtick={1,2,3,4,5,6}, ytick={2,4,6,8,10}]
  \addplot[diag, domain=0:6.2] {x};
  \addplot[courbe, domain=0.5:5.6] {2*x-1};
  \node[etiq,text=otNavy,anchor=east] at (axis cs:5.35,10.1) {$\mathcal{C}_f$};
  \node[etiq,text=otMuted,anchor=west] at (axis cs:6.2,6.0) {$y = x$};
%CORRIGE%
\end{axis}
\end{tikzpicture}"""
FIGURES["toile2_enonce"] = _toile2.replace("%CORRIGE%", "")
FIGURES["toile2_corrige"] = _toile2.replace("%CORRIGE%", r"""
  \draw[guide] (axis cs:2,2) -- (axis cs:2,0);
  \draw[guide] (axis cs:3,3) -- (axis cs:3,0);
  \draw[guide] (axis cs:5,5) -- (axis cs:5,0);
  \draw[escalier] """ + escalier(lambda u: 2 * u - 1, 1.5, 3) + r""" -- (axis cs:5,9);
  \pnt[otGreenDark]{1.5}{0} \pnt{1}{1}
  \node[ulab,anchor=north] at (axis cs:1.5,-1.05) {$u_0$};
  \node[ulab,anchor=north] at (axis cs:2,-1.05) {$u_1$};
  \node[ulab,anchor=north] at (axis cs:3,-1.05) {$u_2$};
  \node[ulab,anchor=north] at (axis cs:5,-1.05) {$u_3$};
  \node[note,anchor=south east] at (axis cs:0.95,1.25) {$(1\,;1)$};""")

# ---------------------------------------------------------------- 1349 (nuage qui se rapproche de 6)
_u = [2.0]
for _ in range(7):
    _u.append(_u[-1] / 3 + 4)
FIGURES["etude_nuage"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.2cm, xmin=-0.4, xmax=7.8, ymin=-0.6, ymax=7.4,
  xtick={1,2,3,4,5,6,7}, ytick={2,4,6}, xlabel={$n$}, ylabel={$u_n$}]
  \draw[seuil] (axis cs:0,6) -- (axis cs:7.5,6);
""" + nuage([(k, round(v, 4)) for k, v in enumerate(_u)]) + r"""
  \node[note,anchor=south,text=otOrange!80!black] at (axis cs:7.1,6.15) {$y = 6$};
  \node[note,anchor=west] at (axis cs:1.6,2.6) {$u_0 = 2$, $u_{n+1} = \frac{1}{3}u_n + 4$};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- 1362 (contrats A et B)
_a = [(k, 24000 + 1000 * k) for k in range(7)]
_b = [(k, round(24000 * 1.04 ** k, 1)) for k in range(7)]
FIGURES["salaires"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, boite, width=7.2cm, height=5cm, xmin=-0.3, xmax=6.5, ymin=23300, ymax=31400,
  xtick={0,1,2,3,4,5,6}, ytick={24000,26000,28000,30000}, scaled y ticks=false,
  yticklabel style={anchor=east,xshift=-2pt,yshift=0pt},
  xlabel={$n$}, ylabel={salaire annuel (€)}]
""" + nuage(_b, "otGreenDark", carre=True) + "\n" + "\n".join(
    rf"  \draw[otNavy,line width=1pt] (axis cs:{x},{y}) circle (3.4pt);" for x, y in _a) + r"""
  \node[anchor=west,text=otNavy,font=\normalsize] at (axis cs:0,30800) {A : $a_n = 24\,000 + 1\,000n$};
  \node[anchor=west,text=otGreenDark,font=\normalsize] at (axis cs:0,29700) {B : $b_n = 24\,000 \times 1{,}04^n$};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- nouveau-1 (allumettes)
def motif(x0, k, c=1.15, e=0.17):
    """k carrés d'allumettes (côté c cm) à partir de l'abscisse x0, avec un jeu de e cm aux coins."""
    lignes = []
    for i in range(k):
        x = x0 + i * c
        lignes.append(rf"\allumette{{{x + e:.3f}}}{{0}}{{{x + c - e:.3f}}}{{0}}")
        lignes.append(rf"\allumette{{{x + e:.3f}}}{{{c}}}{{{x + c - e:.3f}}}{{{c}}}")
    for i in range(k + 1):
        x = x0 + i * c
        lignes.append(rf"\allumette{{{x:.3f}}}{{{e}}}{{{x:.3f}}}{{{c - e:.3f}}}")
    lignes.append(rf"\node[note,anchor=north] at ({x0 + k * c / 2:.3f},-0.3) {{motif {k}}};")
    return "\n".join(lignes)


FIGURES["allumettes"] = ("\\begin{tikzpicture}\n" + motif(0, 1) + "\n" + motif(2.0, 2) + "\n"
                         + motif(5.15, 3) + "\n\\end{tikzpicture}")


# =====================================================================
# Finition du 2026-11-02 : figures ajoutées (cours, fiche, énoncés, corrigés)
# =====================================================================
import math  # noqa: E402

# ---------------------------------------------------------------- cours V + fiche IV : seuil
_cap = [(k, round(1000 * 1.03 ** k, 2)) for k in range(27)]
FIGURES["cours_seuil"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, boite, width=7.4cm, height=4.6cm, xmin=-0.8, xmax=27.4, ymin=800, ymax=2300,
  xtick={0,4,8,12,16,20,24}, ytick={1000,1500,2000}, scaled y ticks=false,
  yticklabel style={anchor=east,xshift=-2pt,yshift=0pt},
  xlabel={$n$}, ylabel={capital $u_n$ (€)}]
  \draw[seuil] (axis cs:0,2000) -- (axis cs:27,2000);
  \draw[otGreenDark,line width=0.7pt,dash pattern=on 2pt off 1.6pt] (axis cs:24,800) -- (axis cs:24,2032.79);
""" + nuage(_cap) + r"""
  \pnt[otGreenDark]{24}{2032.79}
  \node[note,fill=none,anchor=south,text=otOrange!80!black] at (axis cs:4.5,2030) {seuil : $2\,000$ €};
  \node[note,fill=none,anchor=south east,text=otGreenDark] at (axis cs:23.4,860) {premier rang : $n = 24$};
  \node[note,fill=none,anchor=west,text=otNavy] at (axis cs:0.6,1640) {$u_n = 1\,000 \times 1{,}03^n$};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- 1351 (DS 1)
FIGURES["ds1_nuage"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.6cm, xmin=-0.4, xmax=7.6, ymin=-5.8, ymax=13.6,
  xtick={1,2,3,4,5,6,7}, ytick={-4,4,8,12}, xlabel={$n$}, ylabel={$u_n$}]
""" + nuage([(k, k * k - 6 * k + 5) for k in range(8)]) + r"""
  \pnt[otGreenDark]{3}{-4}
  \node[note,fill=none,anchor=north,text=otGreenDark] at (axis cs:3,-4.3) {minimum : $u_3 = -4$};
  \node[etiq,fill=none,anchor=west,text=otNavy] at (axis cs:0.6,10.6) {$u_n = n^2 - 6n + 5$};
\end{axis}
\end{tikzpicture}"""


def rebonds(corrige):
    """Trajectoire d'une balle lâchée de 2 m qui remonte à 80 % : 5 rebonds."""
    sy, c = 1.5, 1.15                       # cm par mètre (vertical), largeur d'un arc = c * sqrt(h)
    h = [2 * 0.8 ** k for k in range(6)]
    lignes = []
    demi0 = c * math.sqrt(h[0]) / 2
    lignes.append(rf"\fill[pattern=north east lines,pattern color=otMuted!70] (-0.3,-0.2) rectangle ({demi0 + sum(c * math.sqrt(v) for v in h[1:]) + 0.3:.3f},0);")
    lignes.append(rf"\draw[otMuted,line width=0.8pt] (-0.3,0) -- ({demi0 + sum(c * math.sqrt(v) for v in h[1:]) + 0.3:.3f},0);")
    lignes.append(rf"\draw[courbe] plot[domain=0:{demi0:.4f},samples=40] (\x,{{{h[0] * sy:.4f}*(1-(\x/{demi0:.4f})^2)}});")
    lignes.append(rf"\fill[otNavy] (0,{h[0] * sy:.3f}) circle (0.11);")
    contacts, x0 = [demi0], demi0
    sommets = []
    for k in range(1, 6):
        w = c * math.sqrt(h[k])
        xc = x0 + w / 2
        lignes.append(rf"\draw[courbe] plot[domain={x0:.4f}:{x0 + w:.4f},samples=50] (\x,{{{h[k] * sy:.4f}*(1-((\x-{xc:.4f})/{w / 2:.4f})^2)}});")
        sommets.append((xc, h[k] * sy))
        x0 += w
        contacts.append(x0)
    lignes.append(rf"\draw[cote] (-0.5,0) -- (-0.5,{h[0] * sy:.3f});")
    lignes.append(rf"\node[anchor=east,text=otInk] at (-0.62,{h[0] * sy / 2:.3f}) {{$h_0 = 2$ m}};")
    couleur = "otGreenDark" if corrige else "otNavy"
    for k, (xc, yc) in enumerate(sommets, start=1):
        if corrige or k <= 2:
            lignes.append(rf"\node[anchor=south,text={couleur},inner sep=1.5pt] at ({xc:.3f},{yc + 0.06:.3f}) {{$h_{k}$}};")
    if corrige:
        for k, xk in enumerate(contacts, start=1):
            lignes.append(rf"\fill[otGreenDark] ({xk:.3f},0) circle (1.9pt);")
            lignes.append(rf"\node[anchor=north,text=otGreenDark,font=\otRegular\fontsize{{9}}{{10}}\selectfont,inner sep=1pt] at ({xk:.3f},-0.26) {{{k}}};")
        lignes.append(rf"\node[anchor=north west,text=otMuted,font=\otRegular\fontsize{{8.5}}{{10}}\selectfont] at (-0.3,-0.75) {{contacts avec le sol numérotés de 1 à 6}};")
        lignes.append(rf"\node[anchor=north west,text=otGreenDark] at (-0.3,-1.3) {{$D = 2 + 2(h_1 + h_2 + h_3 + h_4 + h_5) \approx 12{{,}}76$ m}};")
    return "\\begin{tikzpicture}\n" + "\n".join(lignes) + "\n\\end{tikzpicture}"


FIGURES["rebonds_enonce"] = rebonds(False)
FIGURES["rebonds_corrige"] = rebonds(True)

# ---------------------------------------------------------------- 1352 (DS 2) : deux villes
_p = [(k, round(50000 * 0.98 ** k, 1)) for k in range(17)]
_v = [(k, 30000 + 600 * k) for k in range(17)]
FIGURES["ds2_villes"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, boite, width=7.4cm, height=5cm, xmin=-0.6, xmax=16.8, ymin=28000, ymax=52000,
  xtick={0,2,4,6,8,10,12,14,16}, ytick={30000,35000,40000,45000,50000}, scaled y ticks=false,
  yticklabel style={anchor=east,xshift=-2pt,yshift=0pt},
  xlabel={$n$}, ylabel={habitants}]
  \draw[seuil] (axis cs:0,40000) -- (axis cs:16.6,40000);
  \draw[otGreenDark,line width=0.7pt,dash pattern=on 2pt off 1.6pt] (axis cs:12,28000) -- (axis cs:12,39236);
  \draw[otGreenDark,line width=0.7pt,dash pattern=on 2pt off 1.6pt] (axis cs:14,28000) -- (axis cs:14,38400);
""" + nuage(_p, "otNavy", carre=True) + "\n" + nuage(_v, "otNavy!45") + r"""
  \carre[otGreenDark]{12}{39236}
  \pnt[otGreenDark]{14}{38400} \carre[otGreenDark]{14}{37682}
  \node[note,fill=none,anchor=west,text=otNavy] at (axis cs:3,50500) {$p_n$ (carrés) : $-2\,\%$ par an};
  \node[note,fill=none,anchor=west,text=otNavy!70] at (axis cs:0.4,36800) {$v_n$ (ronds) : $+600$ par an};
  \node[note,fill=none,anchor=north west,text=otOrange!80!black] at (axis cs:0.2,39600) {seuil $40\,000$};
  \node[note,fill=none,anchor=east,text=otGreenDark] at (axis cs:11.8,32200) {$n = 12$};
  \node[note,fill=none,anchor=west,text=otGreenDark] at (axis cs:14.2,32200) {$n = 14$};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- 1364 (DS 3) : épargne
_C = [200.0]
for _ in range(17):
    _C.append(1.02 * _C[-1] + 50)
FIGURES["ds3_epargne"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, boite, width=6.8cm, height=5cm, xmin=-0.6, xmax=17.8, ymin=100, ymax=1300,
  xtick={0,2,4,6,8,10,12,14,16}, ytick={200,400,600,800,1000,1200}, scaled y ticks=false,
  yticklabel style={anchor=east,xshift=-2pt,yshift=0pt},
  xlabel={$n$ (mois)}, ylabel={capital (€)}]
  \draw[seuil] (axis cs:0,1000) -- (axis cs:17.6,1000);
  \draw[otGreenDark,line width=0.7pt,dash pattern=on 2pt off 1.6pt] (axis cs:14,100) -- (axis cs:14,1062.59);
  \draw[otGreenDark,line width=0.7pt,dash pattern=on 2pt off 1.6pt] (axis cs:16,100) -- (axis cs:16,1000);
""" + nuage([(k, round(v, 2)) for k, v in enumerate(_C)]) + "\n" + \
    nuage([(k, 200 + 50 * k) for k in range(18)], "otNavy!45", carre=True) + r"""
  \pnt[otGreenDark]{14}{1062.59} \carre[otGreenDark]{16}{1000}
  \node[note,fill=none,anchor=west,text=otNavy] at (axis cs:0.6,1200) {$C_n$ (ronds) : avec intérêts};
  \node[note,fill=none,anchor=west,text=otNavy!70] at (axis cs:0.6,1095) {$D_n$ (carrés) : sans intérêts};
  \node[note,fill=none,anchor=north west,text=otOrange!80!black] at (axis cs:0.2,985) {seuil $1\,000$ €};
  \node[note,fill=none,anchor=east,text=otGreenDark] at (axis cs:13.8,300) {$n = 14$};
  \node[note,fill=none,anchor=west,text=otGreenDark] at (axis cs:16.2,300) {$n = 16$};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- 1361 (Type examen 1) : bactéries
FIGURES["te1_bacteries"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, boite, width=6.6cm, height=4.6cm, xmin=-0.4, xmax=7.6, ymin=0, ymax=14000,
  xtick={0,1,2,3,4,5,6,7}, ytick={2000,4000,6000,8000,10000,12000}, scaled y ticks=false,
  yticklabel style={anchor=east,xshift=-2pt,yshift=0pt},
  xlabel={$n$ (jours)}, ylabel={bactéries}]
  \draw[seuil] (axis cs:0,10000) -- (axis cs:7.4,10000);
""" + nuage([(k, 100 * 2 ** k) for k in range(7)]) + r"""
  \pnt[otGreenDark]{7}{12800}
  \node[note,fill=none,anchor=east,text=otGreenDark] at (axis cs:6.8,12800) {$b_7 = 12\,800$};
  \node[note,fill=none,anchor=east,text=otNavy] at (axis cs:5.8,6400) {$b_6 = 6\,400$};
  \node[note,fill=none,anchor=south west,text=otOrange!80!black] at (axis cs:0.2,10150) {seuil $10\,000$};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- 1347 : club d'adhérents
_club = [100.0]
for _ in range(15):
    _club.append(0.8 * _club[-1] + 40)
FIGURES["club"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, boite, width=7.4cm, height=4.8cm, xmin=-0.6, xmax=15.8, ymin=90, ymax=215,
  xtick={0,2,4,6,8,10,12,14}, ytick={100,120,140,160,180,200}, scaled y ticks=false,
  yticklabel style={anchor=east,xshift=-2pt,yshift=0pt},
  xlabel={$n$}, ylabel={adhérents $u_n$}]
  \draw[guide] (axis cs:0,200) -- (axis cs:15.6,200);
  \draw[seuil] (axis cs:0,190) -- (axis cs:15.6,190);
  \draw[otGreenDark,line width=0.7pt,dash pattern=on 2pt off 1.6pt] (axis cs:11,90) -- (axis cs:11,191.41);
""" + nuage([(k, round(v, 2)) for k, v in enumerate(_club)]) + r"""
  \pnt[otGreenDark]{11}{191.41}
  \node[note,fill=none,anchor=south west] at (axis cs:0.3,201) {$y = 200$};
  \node[note,fill=none,anchor=north east,text=otOrange!80!black] at (axis cs:15.5,189) {seuil $190$};
  \node[note,fill=none,anchor=west,text=otGreenDark] at (axis cs:11.2,120) {$n = 11$ : en 2036};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- 1350 : valeur d'équilibre 600
_b5 = [(k, 600 - 100 * 1.5 ** k) for k in range(6)]
_b7 = [(k, 600 + 100 * 1.5 ** k) for k in range(7)]
FIGURES["bacteries_equilibre"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, boite, width=6.6cm, height=5cm, xmin=-0.4, xmax=6.6, ymin=-300, ymax=1900,
  xtick={0,1,2,3,4,5,6}, ytick={0,600,1200,1800}, scaled y ticks=false,
  yticklabel style={anchor=east,xshift=-2pt,yshift=0pt},
  xlabel={$n$ (jours)}, ylabel={bactéries}]
  \draw[guide] (axis cs:0,600) -- (axis cs:6.4,600);
""" + nuage([(k, round(v, 2)) for k, v in _b5], "otNavy", carre=True) + "\n" + \
    nuage([(k, round(v, 2)) for k, v in _b7]) + r"""
  \carre[otGreenDark]{5}{-159.38}
  \node[note,fill=none,anchor=south east] at (axis cs:6.4,620) {équilibre : $600$};
  \node[note,fill=none,anchor=east,text=otNavy] at (axis cs:3.7,1450) {$u_0 = 700$ : croissance};
  \node[note,fill=none,anchor=east,text=otNavy] at (axis cs:3.6,-110) {$u_0 = 500$ : déclin};
  \node[note,fill=none,anchor=west,text=otGreenDark] at (axis cs:5.15,-159) {$u_5 < 0$};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- 1355 : deux comportements
FIGURES["comportements"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, name=g, width=3.6cm, height=3.4cm, xmin=-0.6, xmax=14.6, ymin=-0.2, ymax=2.5,
  xtick={5,10}, ytick={1,2}, xlabel={$n$}, ylabel={}]
  \draw[seuil] (axis cs:0,2) -- (axis cs:14.4,2);
""" + nuage([(k, round((2 * k + 1) / (k + 3), 4)) for k in range(15)]) + r"""
  \node[note,fill=none,anchor=south east,text=otOrange!80!black] at (axis cs:14.4,2.04) {$y = 2$};
\end{axis}
\node[anchor=south,text=otNavy] at ($(g.north)+(0,0.15)$) {$t_n = \dfrac{2n + 1}{n + 3}$};
\begin{axis}[otWeb, at={(g.east)}, anchor=west, xshift=1.1cm, name=d, width=3.6cm, height=3.4cm,
  xmin=-0.6, xmax=8.6, ymin=-1.6, ymax=1.6, xtick={2,4,6,8}, ytick={-1,1}, xlabel={$n$}, ylabel={}]
""" + nuage([(k, (-1) ** k) for k in range(9)]) + r"""
\end{axis}
\node[anchor=south,text=otNavy] at ($(d.north)+(0,0.15)$) {$a_n = (-1)^n$};
\end{tikzpicture}"""

# ---------------------------------------------------------------- 1348 : sens de variation de w_n
FIGURES["variation_w"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.6cm, xmin=-0.4, xmax=6.8, ymin=-5.8, ymax=13.6,
  xtick={1,2,3,4,5,6}, ytick={-4,4,8,12}, xlabel={$n$}, ylabel={$w_n$}]
""" + nuage([(k, k * k - 4 * k) for k in range(7)]) + r"""
  \pnt[otGreenDark]{2}{-4}
  \node[note,fill=none,anchor=north,text=otGreenDark] at (axis cs:2,-4.3) {minimum : $w_2 = -4$};
  \node[note,fill=none,anchor=west,text=otGreenDark] at (axis cs:0.5,8.4) {décroît jusqu’au rang $2$,};
  \node[note,fill=none,anchor=west,text=otGreenDark] at (axis cs:0.5,6.2) {puis croît};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- 1342 : deux termes, quatre pas
FIGURES["arith_t"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.8cm, xmin=-0.4, xmax=8.6, ymin=-0.8, ymax=18.6,
  xtick={1,2,3,4,5,6,7,8}, ytick={4,8,12,16}, xlabel={$n$}, ylabel={$t_n$}]
  \draw[otGreenDark,line width=1.1pt,line join=round] (axis cs:3,7) -- (axis cs:4,7) -- (axis cs:4,9) -- (axis cs:5,9)
    -- (axis cs:5,11) -- (axis cs:6,11) -- (axis cs:6,13) -- (axis cs:7,13) -- (axis cs:7,15);
""" + nuage([(k, 1 + 2 * k) for k in range(9)], "otNavy!45") + r"""
  \pnt{3}{7} \pnt{7}{15} \pnt[otGreenDark]{0}{1}
  \node[note,fill=none,anchor=east,text=otNavy] at (axis cs:2.8,7.6) {$t_3 = 7$};
  \node[note,fill=none,anchor=east,text=otNavy] at (axis cs:6.75,15.4) {$t_7 = 15$};
  \node[note,fill=none,anchor=west,text=otGreenDark] at (axis cs:5.3,7.6) {$4r = 8$, donc $r = 2$};
  \node[note,fill=none,anchor=east,text=otGreenDark] at (axis cs:-0.15,1.2) {$t_0 = 1$};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- 1343 : raison négative
FIGURES["alternance"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.8cm, xmin=-0.4, xmax=5.6, ymin=-36, ymax=21,
  xtick={1,2,3,4,5}, ytick={-32,-16,16}, xlabel={$n$}, ylabel={$s_n$}]
""" + nuage([(k, (-2) ** k) for k in range(4)]) + r"""
  \pnt[otGreenDark]{4}{16} \pnt[otGreenDark]{5}{-32}
  \node[note,fill=none,anchor=east,text=otGreenDark] at (axis cs:3.8,16) {$s_4 = 16$};
  \node[note,fill=none,anchor=east,text=otGreenDark] at (axis cs:4.8,-32) {$s_5 = -32$};
  \node[note,fill=none,anchor=west,text=otNavy] at (axis cs:0.3,-21) {$q = -2 < 0$ : le signe};
  \node[note,fill=none,anchor=west,text=otNavy] at (axis cs:0.3,-26.5) {change à chaque rang};
\end{axis}
\end{tikzpicture}"""

# ---------------------------------------------------------------- 1356 : 1 + 1/2 + ... + 1/16
_u1 = 3.2
_pieces = [((0, 0), (1, 1), r"$1$", "otNavy!24"), ((1, 0), (2, 0.5), r"$\dfrac{1}{2}$", "otNavy!19"),
           ((1, 0.5), (1.5, 1), r"$\dfrac{1}{4}$", "otNavy!14"), ((1.5, 0.5), (2, 0.75), r"$\dfrac{1}{8}$", "otNavy!10"),
           ((1.5, 0.75), (1.75, 1), r"$\dfrac{1}{16}$", "otNavy!6")]
_lignes = []
for (a, b), (c, d), lab, col in _pieces:
    _lignes.append(rf"\fill[{col}] ({a * _u1:.3f},{b * _u1:.3f}) rectangle ({c * _u1:.3f},{d * _u1:.3f});")
for (a, b), (c, d), lab, col in _pieces:
    _lignes.append(rf"\draw[white,line width=1.4pt] ({a * _u1:.3f},{b * _u1:.3f}) rectangle ({c * _u1:.3f},{d * _u1:.3f});")
    taille = r"\normalsize" if (c - a) >= 0.5 else r"\small"
    _lignes.append(rf"\node[text=otInk,font={taille},inner sep=0.5pt] at ({(a + c) / 2 * _u1:.3f},{(b + d) / 2 * _u1:.3f}) {{{lab}}};")
_lignes.append(rf"\fill[pattern=north east lines,pattern color=otOrange] ({1.75 * _u1:.3f},{0.75 * _u1:.3f}) rectangle ({2 * _u1:.3f},{_u1:.3f});")
_lignes.append(rf"\draw[otNavy,line width=0.9pt] (0,0) rectangle ({2 * _u1:.3f},{_u1:.3f});")
_lignes.append(rf"\draw[otOrange!85!black,line width=0.6pt,-{{Stealth[length=1.6mm]}}] ({2 * _u1 + 0.75:.3f},{0.875 * _u1:.3f}) -- ({2 * _u1 + 0.08:.3f},{0.875 * _u1:.3f});")
_lignes.append(rf"\node[anchor=west,text=otOrange!80!black,align=left,font=\otRegular\fontsize{{8.5}}{{10}}\selectfont] at ({2 * _u1 + 0.8:.3f},{0.875 * _u1:.3f}) {{il manque\\{{\normalsize$\dfrac{{1}}{{16}}$}}}};")
_lignes.append(rf"\node[anchor=north,text=otMuted,font=\otRegular\fontsize{{8.5}}{{10}}\selectfont] at ({_u1:.3f},-0.12) {{rectangle d’aire $2$}};")
_lignes.append(rf"\node[anchor=north,text=otGreenDark] at ({_u1:.3f},-0.62) {{$S_5 = 2 - \frac{{1}}{{16}} = \frac{{31}}{{16}}$}};")
FIGURES["moities"] = "\\begin{tikzpicture}\n" + "\n".join(_lignes) + "\n\\end{tikzpicture}"


# ---------------------------------------------------------------- nouveau-1 : corrigés
def motif_corrige(x0, k, c=1.15, e=0.17):
    """Motif de k carrés ; les 3 allumettes du dernier carré (haut, bas, droite) en vert."""
    lignes = []
    for i in range(k):
        x = x0 + i * c
        cmd = r"\allumetteV" if i == k - 1 else r"\allumette"
        lignes.append(rf"{cmd}{{{x + e:.3f}}}{{0}}{{{x + c - e:.3f}}}{{0}}")
        lignes.append(rf"{cmd}{{{x + e:.3f}}}{{{c}}}{{{x + c - e:.3f}}}{{{c}}}")
    for i in range(k + 1):
        x = x0 + i * c
        cmd = r"\allumetteV" if i == k else r"\allumette"
        lignes.append(rf"{cmd}{{{x:.3f}}}{{{e}}}{{{x:.3f}}}{{{c - e:.3f}}}")
    return "\n".join(lignes)


FIGURES["allumettes_corrige"] = ("\\begin{tikzpicture}\n" + motif_corrige(0, 4) + "\n"
    + r"\node[note,anchor=north east] at (3.25,-0.3) {motif 3 (10 allumettes)};" + "\n"
    + r"\draw[otGreenDark,line width=0.6pt] (3.45,-0.2) -- (3.45,-1.2);" + "\n"
    + r"\node[anchor=north west,text=otGreenDark,align=left,font=\otRegular\fontsize{8.5}{10}\selectfont] at (3.62,-0.3) {nouveau carré :\\$+3$ allumettes};" + "\n"
    + r"\node[anchor=north,text=otGreenDark] at (2.3,-1.3) {motif 4 : $a_4 = 10 + 3 = 13$};" + "\n"
    + "\\end{tikzpicture}")

FIGURES["poignees"] = r"""
\begin{tikzpicture}
  \coordinate (A) at (0,0); \coordinate (B) at (2.2,0); \coordinate (C) at (2.2,2.2); \coordinate (D) at (0,2.2);
  \coordinate (E) at (4.4,1.1);
  \draw[otNavy,line width=0.9pt] (A) -- (B) -- (C) -- (D) -- cycle (A) -- (C) (B) -- (D);
  \draw[otGreenDark,line width=1.2pt] (E) -- (A) (E) -- (B) (E) -- (C) (E) -- (D);
  \foreach \p in {A,B,C,D} {\fill[otNavy] (\p) circle (2.6pt);}
  \fill[otGreenDark] (E) circle (3pt);
  \node[anchor=north east,text=otNavy] at ($(A)+(-0.05,-0.05)$) {$A$};
  \node[anchor=north,text=otNavy] at ($(B)+(-0.15,-0.08)$) {$B$};
  \node[anchor=south,text=otNavy] at ($(C)+(-0.15,0.08)$) {$C$};
  \node[anchor=south east,text=otNavy] at ($(D)+(-0.05,0.05)$) {$D$};
  \node[anchor=west,text=otGreenDark] at ($(E)+(0.12,0)$) {$E$};
  \node[anchor=north west,text=otNavy,font=\otRegular\fontsize{8.5}{10}\selectfont] at (-0.3,-0.7) {groupe de $4$ : $p_4 = 6$ poignées (en bleu)};
  \node[anchor=north west,text=otGreenDark] at (-0.3,-1.2) {$E$ arrive : $p_5 = p_4 + 4 = 10$};
\end{tikzpicture}"""
