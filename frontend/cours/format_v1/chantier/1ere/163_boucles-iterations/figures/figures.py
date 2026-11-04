# -*- coding: utf-8 -*-
"""Figures de la notion « Algorithmes du programme de Première » (style des livres OptiTAB).

Compilation : python ../../../outils/figures_livre.py <dossier_notion> [nom …] [--planche]

Toutes les valeurs sont celles du texte, contrôlées par ../verif_algorithmes.py.
L'histogramme des deux dés lit les effectifs dans l'affichage du programme du
cours (bloc console), lui-même comparé à une exécution réelle par la vérification.
"""
import math
import re
from fractions import Fraction
from pathlib import Path

ICI = Path(__file__).resolve().parent

PREAMBULE_EXTRA = r"""
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
  evt/.style={font=\normalsize, text=otNavy, inner sep=2.4pt},
  branche/.style={otNavy!65, line width=0.8pt, line cap=round},
  poids/.style={font=\small, text=otInk, inner sep=1.7pt},
  poidsV/.style={poids, text=otGreenDark},
  issue/.style={font=\small, text=otMuted, anchor=west, inner sep=1.5pt},
  issueV/.style={issue, text=otGreenDark},
  racine/.style={fill=otNavy},
  legende/.style={font=\otRegular\fontsize{9}{10}\selectfont, text=otMuted, inner sep=1.5pt},
  legendeV/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otGreenDark, inner sep=1.5pt},
  legendeO/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otOrange!75!black, inner sep=1.5pt},
  euler/.style={otGreenDark,line width=1.2pt,line join=round},
}
"""

FIGURES = {}


def pts(points, couleur="otNavy"):
    return "\n  ".join(rf"\pnt[{couleur}]{{{x}}}{{{y:.5f}}}" for x, y in points)


# ================================================================ suites
def suite_seuil():
    u = [(n, 2 * 1.5 ** n) for n in range(10)]
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=7.4cm, height=4.6cm, xmin=-0.4, xmax=9.8, ymin=0, ymax=86,
  xtick={0,1,...,9}, ytick={0,20,40,60,80}, xlabel={$n$}, ylabel={$u_n$}]
  \draw[seuil] (axis cs:-0.4,50) -- (axis cs:9.6,50);
  \node[legendeO,anchor=south west] at (axis cs:0.1,51.5) {seuil $A = 50$};
  \draw[guide] (axis cs:8,0) -- (axis cs:8,51.26);
  """ + pts([p for p in u if p[0] != 8]) + r"""
  \fill[otGreenDark] (axis cs:8,51.2578) circle (2.6pt);
  \node[legendeV,anchor=east] at (axis cs:7.7,62) {$u_8 \approx 51{,}26 > 50$};
  \node[legende,anchor=east] at (axis cs:6.8,34.17) {$u_7 \approx 34{,}17$};
\end{axis}
\end{tikzpicture}"""


FIGURES["suite_seuil"] = suite_seuil()


def suite_bornee():
    u = [(n, 4 - 4 * 0.5 ** n) for n in range(11)]
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=7.4cm, height=4.4cm, xmin=-0.4, xmax=10.8, ymin=0, ymax=5.9,
  xtick={0,1,...,10}, ytick={0,1,2,3,4,5}, xlabel={$n$}, ylabel={$u_n$}]
  \draw[seuil] (axis cs:-0.4,5) -- (axis cs:10.6,5);
  \node[legendeO,anchor=south east] at (axis cs:10.5,5.1) {seuil $5$ : jamais dépassé};
  \draw[otNavy!70,line width=0.8pt,dash pattern=on 2.5pt off 2pt] (axis cs:-0.4,4) -- (axis cs:10.6,4);
  \node[legende,anchor=north east] at (axis cs:10.5,3.82) {$u_n < 4$};
  """ + pts(u) + r"""
\end{axis}
\end{tikzpicture}"""


FIGURES["suite_bornee"] = suite_bornee()


# ---------------------------------------------------------------- 1060 : population
def ville(corrige):
    u = [20000.0]
    for _ in range(12):
        u.append(1.03 * u[-1] + 400)
    p = [(n, v / 1000) for n, v in enumerate(u)]
    vert = r"""
  \draw[guide] (axis cs:9,18) -- (axis cs:9,30.159);
  \fill[otGreenDark] (axis cs:9,30.15911) circle (2.6pt);
  \node[legendeV,anchor=east] at (axis cs:8.7,32.4) {$u_9 \approx 30\,159$ : année 2034};""" if corrige else ""
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=7.4cm, height=4.6cm, xmin=-0.4, xmax=12.6, ymin=18, ymax=36,
  xtick={0,1,...,12}, ytick={18,20,...,36}, xlabel={$n$}, ylabel={$u_n$ (milliers)}]
  \draw[seuil] (axis cs:-0.4,30) -- (axis cs:12.4,30);
  \node[legendeO,anchor=north west] at (axis cs:9.6,29.7) {seuil $30\,000$};
  """ + pts([q for q in p if not (corrige and q[0] == 9)]) + vert + r"""
\end{axis}
\end{tikzpicture}"""


FIGURES["ville_enonce"] = ville(False)
FIGURES["ville_corrige"] = ville(True)


# ---------------------------------------------------------------- 1061 : u_{n+1} = 0,8 u_n + 3
def bornee15(corrige):
    u = [(n, 15 - 14 * 0.8 ** n) for n in range(21)]
    extra = r"""
  \draw[seuil] (axis cs:-0.5,16) -- (axis cs:20.6,16);
  \node[legendeO,anchor=south east] at (axis cs:20.5,16.15) {seuil $16$ : jamais dépassé};
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:-0.5,15) -- (axis cs:20.6,15);
  \node[legendeV,anchor=north west] at (axis cs:0.3,14.7) {$u_n < 15$ pour tout $n$};""" if corrige else ""
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=7.6cm, height=4.6cm, xmin=-0.5, xmax=20.8, ymin=0, ymax=18,
  xtick={0,2,...,20}, ytick={0,2,...,18}, xlabel={$n$}, ylabel={$u_n$}]""" + extra + r"""
  """ + pts(u) + r"""
\end{axis}
\end{tikzpicture}"""


FIGURES["bornee_enonce"] = bornee15(False)
FIGURES["bornee_corrige"] = bornee15(True)


# ================================================================ Euler
def euler(h, n, largeur, label_h, ymax, yticks, nom_points):
    p = [(k * h, (1 + h) ** k) for k in range(n + 1)]
    ligne = " -- ".join(f"(axis cs:{x:.4f},{y:.5f})" for x, y in p)
    pnts = "\n  ".join(rf"\fill[otGreenDark] (axis cs:{x:.4f},{y:.5f}) circle (2.1pt);" for x, y in p)
    xe, ye = p[-1]
    return r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=""" + largeur + r""", height=5.2cm, xmin=-0.15, xmax=2.75, ymin=-0.4, ymax=""" + str(ymax) + r""",
  xtick={0.5,1,1.5,2}, xticklabels={$0{,}5$,$1$,$1{,}5$,$2$}, ytick={""" + yticks + r"""}]
  \addplot[courbe, domain=0:2.05, samples=120] {exp(x)};
  \draw[euler] """ + ligne + r""";
  """ + pnts + r"""
  \node[text=otNavy,anchor=east] at (axis cs:1.88,7.05) {$y = e^x$};
  \node[legendeV,anchor=west] at (axis cs:""" + f"{xe + 0.08:.3f},{ye:.4f}" + r""") {Euler, """ + label_h + r"""};
  \node[legende,anchor=west] at (axis cs:2.1,7.389) {$e^2 \approx 7{,}39$};
  \fill[otNavy] (axis cs:2,7.389) circle (2.1pt);
\end{axis}
\end{tikzpicture}"""


FIGURES["euler_cours"] = euler(0.25, 8, "6.4cm", r"$h = 0{,}25$", 8.2, "1,2,...,8", None)
FIGURES["euler_exo"] = euler(0.5, 4, "6.4cm", r"$h = 0{,}5$", 8.2, "1,2,...,8", None)


# ================================================================ dérivation : sécante et tangente
FIGURES["secante_cube"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=5.6cm, xmin=-0.35, xmax=2.55, ymin=-1.3, ymax=5.9,
  xtick={1,1.5}, xticklabels={$1$,$1+h$}, ytick={1,2,3,4,5}]
  \addplot[courbe, domain=-0.3:1.76, samples=120] {x^3};
  \addplot[otOrange!85!black, line width=1pt, domain=0.62:1.72] {4.75*(x-1)+1};
  \addplot[otGreenDark, line width=1pt, dash pattern=on 4pt off 2.5pt, domain=0.4:1.82] {3*x-2};
  \draw[guide] (axis cs:1,0) -- (axis cs:1,1);
  \draw[otMuted,line width=0.7pt] (axis cs:1,1) -- (axis cs:1.5,1) -- (axis cs:1.5,3.375);
  \draw[guide] (axis cs:1.5,0) -- (axis cs:1.5,1);
  \fill[otNavy] (axis cs:1,1) circle (2.3pt);
  \fill[otNavy] (axis cs:1.5,3.375) circle (2.3pt);
  \node[text=otNavy,anchor=south east] at (axis cs:0.97,1.05) {$A$};
  \node[text=otNavy,anchor=south east] at (axis cs:1.47,3.42) {$M$};
  \node[text=otInk,anchor=north,font=\small] at (axis cs:1.25,0.95) {$h$};
  \node[text=otInk,anchor=west,font=\small] at (axis cs:1.53,1.75) {$f(1+h)-f(1)$};
  \node[text=otNavy,anchor=west] at (axis cs:1.78,5.5) {$y = x^3$};
  \node[legendeO,anchor=west] at (axis cs:1.75,4.45) {sécante $(AM)$};
  \node[legendeV,anchor=west] at (axis cs:1.85,3.45) {tangente en $A$};
\end{axis}
\end{tikzpicture}"""


# ================================================================ second degré : balayage
FIGURES["parabole_balayage"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=5cm, xmin=-0.6, xmax=6.8, ymin=-4.9, ymax=6.4,
  xtick={1,2,...,6}, ytick={-4,-2,2,4}]
  \addplot[courbe, domain=-0.12:6.12, samples=160] {-x^2+6*x-4};
  \sol{0}{1}
  \sol{5}{6}
  """ + pts([(k, -k * k + 6 * k - 4) for k in range(7)]) + r"""
  \fill[otGreenDark] (axis cs:0.76393,0) circle (2.4pt);
  \fill[otGreenDark] (axis cs:5.23607,0) circle (2.4pt);
  \node[text=otNavy,anchor=west] at (axis cs:3.55,5.6) {$y = f(x)$};
  \node[legendeV,anchor=south] at (axis cs:0.5,0.35) {$x_1$};
  \node[legendeV,anchor=south] at (axis cs:5.5,0.35) {$x_2$};
\end{axis}
\end{tikzpicture}"""


# ================================================================ Archimède
def archimede(corrige):
    R = 3.4
    s3 = math.sqrt(3)
    A = (-R / 2, R * s3 / 2)
    B = (R / 2, R * s3 / 2)
    hexa = " -- ".join(f"({R * math.cos(math.radians(60 * k)):.4f},{R * math.sin(math.radians(60 * k)):.4f})"
                       for k in range(6)) + " -- cycle"
    plus = r"""
  \node[text=otGreenDark,anchor=north] at (-0.85,""" + f"{A[1] - 0.07:.4f}" + r""") {$c_n/2$};
  \node[text=otGreenDark,anchor=east] at (-1.0,1.38) {$1$};
  \node[text=otGreenDark,anchor=west] at (0.1,1.4) {$OI$};""" if corrige else ""
    return r"""
\begin{tikzpicture}
  \coordinate (O) at (0,0);
  \coordinate (A) at (""" + f"{A[0]:.4f},{A[1]:.4f}" + r""");
  \coordinate (B) at (""" + f"{B[0]:.4f},{B[1]:.4f}" + r""");
  \coordinate (I) at (0,""" + f"{A[1]:.4f}" + r""");
  \coordinate (C) at (0,""" + f"{R:.4f}" + r""");
  \draw[otNavy!45,line width=0.8pt] (O) circle (""" + f"{R}" + r"""cm);
  \draw[geoTrait] """ + hexa + r""";
  \draw[otNavy,line width=0.7pt] (O) -- (A) (O) -- (B);
  \draw[guide] (O) -- (C);
  \draw[otGreenDark,line width=1.5pt] (A) -- (C) -- (B);
  \angledroit[0.2]{O}{I}{A}
  \foreach \p in {O,A,B,I,C} \fill[otNavy] (\p) circle (1.9pt);
  \node[text=otInk,anchor=north] at (0,-0.08) {$O$};
  \node[text=otInk,anchor=south east] at ($(A)+(-0.04,0.04)$) {$A$};
  \node[text=otInk,anchor=south west] at ($(B)+(0.04,0.04)$) {$B$};
  \node[text=otInk,anchor=south] at ($(C)+(0,0.06)$) {$C$};
  \node[text=otInk,anchor=north west,inner sep=1pt] at ($(I)+(0.05,-0.04)$) {$I$};""" + plus + r"""
\end{tikzpicture}"""


FIGURES["archimede"] = archimede(False)
FIGURES["archimede_corrige"] = archimede(True)


# ================================================================ histogramme des deux dés
def effectifs_cours():
    t = (ICI.parent / "cours_151.txt").read_text(encoding="utf-8")
    m = re.search(r"eff\[s\] = eff\[s\] \+ 1.*?```console\n(.*?)```", t, re.S)
    eff = {}
    for ligne in m.group(1).strip().splitlines():
        s, e = ligne.split()
        eff[int(s)] = int(e)
    assert sorted(eff) == list(range(2, 13)) and sum(eff.values()) == 1000
    return eff


def histo_des():
    eff = effectifs_cours()
    barres = " ".join(f"({s},{eff[s] / 1000:.3f})" for s in range(2, 13))
    proba = "\n  ".join(
        rf"\draw[otOrange!85!black,line width=1.8pt] (axis cs:{s - 0.36},{float(Fraction(6 - abs(s - 7), 36)):.5f}) -- (axis cs:{s + 0.36},{float(Fraction(6 - abs(s - 7), 36)):.5f});"
        for s in range(2, 13))
    return r"""
\begin{tikzpicture}
\begin{axis}[otBarres, width=7.6cm, height=4.4cm, bar width=12pt, ymax=0.2, enlarge x limits=0.06,
  xtick={2,3,...,12}, ytick={0.05,0.1,0.15}, yticklabel style={/pgf/number format/fixed,/pgf/number format/precision=2},
  xlabel={somme $s$}, ylabel={fréquence}, clip=false,
  every axis y label/.style={at={(current axis.north west)},anchor=south,yshift=4pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  every axis x label/.style={at={(current axis.south east)},anchor=north east,yshift=-14pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}]
  \addplot[fill=otNavy!55,draw=otNavy] coordinates {""" + barres + r"""};
  """ + proba + r"""
\end{axis}
  \fill[otNavy!55,draw=otNavy] (4.55,4.22) rectangle ++(0.26,0.2);
  \node[legende,anchor=west] at (4.86,4.32) {fréquence observée};
  \draw[otOrange!85!black,line width=1.8pt] (4.52,3.9) -- ++(0.32,0);
  \node[legende,anchor=west] at (4.86,3.9) {probabilité};
\end{tikzpicture}"""


FIGURES["histo_des"] = histo_des()


# ================================================================ arbres
def N(nom, poids, *enfants, droite=None):
    return {"nom": nom, "poids": poids, "enfants": list(enfants), "droite": droite}


def _placer(n, prof, y, dy, L):
    n["x"] = prof * L
    if not n["enfants"]:
        n["y"] = y
        return y - dy
    ys = []
    for c in n["enfants"]:
        y = _placer(c, prof + 1, y, dy, L)
        ys.append(c["y"])
    n["y"] = (ys[0] + ys[-1]) / 2
    return y


def arbre(enfants, L=2.4, dy=1.0, squelette=False, couleur_poids="poidsV", couleur_droite="issueV"):
    racine = {"nom": None, "poids": None, "enfants": enfants, "droite": None}
    _placer(racine, 0, 0.0, dy, L)
    noeuds, aretes, poids, droites = [], [], [], []
    k = [0]

    def visiter(n, parent_ref, parent_y):
        for c in n["enfants"]:
            k[0] += 1
            nom = f"n{k[0]}"
            noeuds.append(rf"\node[evt] ({nom}) at ({c['x']:.3f},{c['y']:.3f}) {{${c['nom']}$}};")
            aretes.append(rf"\draw[branche] {parent_ref} -- ({nom}.west);")
            if c["poids"] is not None and not squelette:
                ecart = c["y"] - parent_y
                anc = "south east" if ecart > 1e-6 else ("north east" if ecart < -1e-6 else "south")
                poids.append(rf"\path {parent_ref} -- ({nom}.west) node[{couleur_poids},pos=0.5,anchor={anc}] {{${c['poids']}$}};")
            if not c["enfants"] and c["droite"] and not squelette:
                droites.append(rf"\node[{couleur_droite}] at ([xshift=4pt]{nom}.east) {{{c['droite']}}};")
            visiter(c, f"({nom}.east)", c["y"])

    lignes = [r"\begin{tikzpicture}[x=1cm,y=1cm]", rf"\coordinate (r) at (0,{racine['y']:.3f});"]
    visiter(racine, "(r)", racine["y"])
    lignes += noeuds + aretes + [r"\fill[racine] (r) circle (1.9pt);"] + poids + droites
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


def F(p, q):
    return rf"\dfrac{{{p}}}{{{q}}}"


# ---------------------------------------------------------------- cours : urne 3 R, 2 V sans remise
FIGURES["arbre_urne"] = arbre([
    N("R_1", F(3, 5),
      N("R_2", F(2, 4), droite=rf"$R_1 \cap R_2$ : ${F(6, 20)}$"),
      N("V_2", F(2, 4), droite=rf"$R_1 \cap V_2$ : ${F(6, 20)}$")),
    N("V_1", F(2, 5),
      N("R_2", F(3, 4), droite=rf"$V_1 \cap R_2$ : ${F(6, 20)}$"),
      N("V_2", F(1, 4), droite=rf"$V_1 \cap V_2$ : ${F(2, 20)}$")),
], L=2.15, dy=1.05, couleur_poids="poids", couleur_droite="issue")


# ---------------------------------------------------------------- 1062 : dé puis urne
def arbre_de(squelette):
    S, nS = "S", r"\overline{S}"
    return arbre([
        N(S, F(1, 6),
          N("R", F(3, 4), droite=rf"$P(S \cap R) = {F(1, 8)}$"),
          N("V", F(1, 4), droite=rf"$P(S \cap V) = {F(1, 24)}$")),
        N(nS, F(5, 6),
          N("R", F(1, 4), droite=rf"$P(\overline{{S}} \cap R) = {F(5, 24)}$"),
          N("V", F(3, 4), droite=rf"$P(\overline{{S}} \cap V) = {F(5, 8)}$")),
    ], L=2.15, dy=1.05, squelette=squelette)


FIGURES["arbre_de_enonce"] = arbre_de(True)
FIGURES["arbre_de_corrige"] = arbre_de(False)
