# -*- coding: utf-8 -*-
"""Figures de la notion 259 (4e : relier des grandeurs et lire des graphiques), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Courbes en bleu marine (seconde courbe en orange) ; dans les corrigés, les
lectures (pointillés vers les axes, points, valeurs lues) sont en vert.
Les données (DONNEES) sont relues par verif_259.py : figures et énoncés
utilisent les mêmes valeurs.
"""
from math import cos, pi

PREAMBULE_EXTRA = r"""
\pgfplotsset{gr/.style={otWeb, grid=both,
  major grid style={otRule!80,line width=0.4pt}, minor grid style={otRule!45,line width=0.3pt},
  minor tick length=0pt,
  every axis x label/.style={at={(current axis.right of origin)},anchor=west,xshift=2pt,
    font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  every axis y label/.style={at={(current axis.above origin)},anchor=south west,xshift=-4pt,yshift=1pt,
    font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}}}
\tikzset{
  courbeB/.style={otOrange,line width=1.35pt},
  ligne/.style={otNavy,line width=1.35pt,line join=round},
  ligneB/.style={otOrange,line width=1.35pt,line join=round},
  lecture/.style={otGreenDark,line width=0.8pt,dash pattern=on 2.5pt off 1.8pt},
  niveau/.style={otGreenDark,line width=0.8pt,dash pattern=on 4pt off 2.5pt},
  vert/.style={note,text=otGreenDark},
  bleu/.style={note,text=otNavy},
  orange/.style={note,text=otOrange!85!black},
  petitG/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},
}
\newcommand{\lirev}[2]{\draw[lecture] (axis cs:#1,0) -- (axis cs:#1,#2) -- (axis cs:0,#2);}
\newcommand{\lirex}[2]{\draw[lecture] (axis cs:#1,#2) -- (axis cs:#1,0);}
\newcommand{\liry}[2]{\draw[lecture] (axis cs:#1,#2) -- (axis cs:0,#2);}
\newcommand{\pv}[2]{\fill[otGreenDark] (axis cs:#1,#2) circle (2.3pt);}
\newcommand{\zero}{\node[anchor=north east,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:0,0) {0};}
"""


def lst(a, b, s):
    """Liste de graduations a, a+s, …, b (sans 0)."""
    v, out = a, []
    while v <= b + 1e-9:
        if abs(v) > 1e-9:
            out.append(("%g" % round(v, 6)))
        v += s
    return "{" + ",".join(out) + "}"


def G(opts, corps, xlab="", ylab=""):
    o = "gr, " + opts
    if xlab:
        o += ", xlabel={" + xlab + "}"
    if ylab:
        o += ", ylabel={" + ylab + "}"
    return (r"\begin{tikzpicture}" + "\n" + r"\begin{axis}[" + o + "]\n" + corps + "\n" + r"\zero"
            + "\n\\end{axis}\n\\end{tikzpicture}")


def poly(pts, style="ligne", points=True, couleur="otNavy"):
    s = r"\draw[%s] " % style + " -- ".join("(axis cs:%g,%g)" % p for p in pts) + ";\n"
    if points:
        s += "".join(r"\fill[%s] (axis cs:%g,%g) circle (2.1pt);" % (couleur, x, y) + "\n" for x, y in pts)
    return s


def nuage(pts, couleur="otNavy"):
    return "".join(r"\fill[%s] (axis cs:%g,%g) circle (2.1pt);" % (couleur, x, y) + "\n" for x, y in pts)


FIGURES = {}
XLAB = {}
DONNEES = {}

# =============================================================== COURS
# Marée : h(t) = 3 - 2 cos(pi t / 6)
DONNEES["maree"] = {t: 3 - 2 * cos(pi * t / 6) for t in range(0, 13)}
FIGURES["cours_maree"] = G(
    r"width=6.6cm, height=4.6cm, xmin=0, xmax=12.8, ymin=0, ymax=6.4, xtick=" + lst(1, 12, 1)
    + r", ytick=" + lst(1, 6, 1) + r", minor y tick num=1",
    r"""
  \addplot[courbe, domain=0:12, samples=120] {3-2*cos(30*x)};
  \lirev{2}{2} \pv{2}{2}
  \draw[niveau] (axis cs:0,4) -- (axis cs:10.4,4);
  \lirex{4}{4} \lirex{8}{4} \pv{4}{4} \pv{8}{4}
  \pv{6}{5}
  \node[vert,anchor=south] at (axis cs:6,5.25) {maximum : $5$ m à $6$ h};
  \node[vert,anchor=west] at (axis cs:10.5,4) {$4$ m};
  \node[vert,anchor=north west,align=left] at (axis cs:2.15,1.9) {à $2$ h :\\$2$ m};
""", "heure (h)", "hauteur d'eau (m)")

# Piscine : V = 5 + 2t
DONNEES["piscine"] = [(t, 5 + 2 * t) for t in range(0, 6)]
FIGURES["cours_piscine"] = G(
    r"width=5.6cm, height=4.6cm, xmin=0, xmax=5.7, ymin=0, ymax=17.5, xtick=" + lst(1, 5, 1)
    + r", ytick=" + lst(2, 16, 2) + r", minor x tick num=1",
    r"""
  \addplot[courbe, domain=0:5.4] {5+2*x};
""" + nuage(DONNEES["piscine"], "otGreenDark") + r"""
  \node[bleu,anchor=north west] at (axis cs:2.9,8.6) {$V = 5 + 2t$};
  \node[vert,anchor=west] at (axis cs:0.25,3.2) {$5$ m³ au départ};
""", "durée $t$ (h)", "volume $V$ (m³)")

# Trois graphiques : proportionnalité ?
def mini(y0, titre, couleur, corps, legende):
    """Une ligne de la figure : petit repère à gauche, conclusion à droite."""
    return (r"\begin{scope}[yshift=%gcm]" % y0 + "\n"
            + r"\draw[otMuted,line width=0.6pt,-{Stealth[length=2mm]}] (0,0) -- (2.2,0);" + "\n"
            + r"\draw[otMuted,line width=0.6pt,-{Stealth[length=2mm]}] (0,0) -- (0,1.75);" + "\n"
            + r"\node[petitG,anchor=north east,inner sep=1pt] at (0,0) {0};" + "\n"
            + corps + "\n"
            + r"\node[font=\otMedium\fontsize{10}{12}\selectfont,text=%s,anchor=south west] at (2.75,0.85) {%s};" % (couleur, titre) + "\n"
            + r"\node[text=otInk,anchor=north west,align=left] at (2.75,0.8) {%s};" % legende + "\n"
            + r"\end{scope}")


FIGURES["cours_proportionnalite"] = (r"\begin{tikzpicture}" + "\n"
    + mini(0, "proportionnelles", "otGreenDark",
           r"\draw[otNavy,line width=1.3pt] (0,0) -- (1.95,1.5); \fill[otNavy] (0,0) circle (1.9pt);",
           r"droite passant\\par l'origine")
    + mini(-2.35, "non proportionnelles", "otOrange!85!black",
           r"\draw[otNavy,line width=1.3pt] (0,0.6) -- (1.95,1.55); \fill[otNavy] (0,0.6) circle (1.9pt);",
           r"droite ne passant pas\\par l'origine")
    + mini(-4.7, "non proportionnelles", "otOrange!85!black",
           r"\draw[otNavy,line width=1.3pt] plot[domain=0:1.9,samples=40] (\x,{0.42*\x*\x});",
           r"courbe qui n'est pas\\une droite")
    + "\n" + r"\end{tikzpicture}")

# =============================================================== 2663 température
DONNEES["temperature"] = [(0, 4), (3, 2), (6, 1), (9, 6), (12, 12), (15, 14), (18, 10), (21, 7), (24, 5)]
P63 = (r"width=6.6cm, height=4.8cm, xmin=0, xmax=25.5, ymin=0, ymax=16.9, xtick=" + lst(3, 24, 3)
       + r", minor x tick num=2, ytick=" + lst(2, 16, 2) + r", minor y tick num=1")
B63 = poly(DONNEES["temperature"])
FIGURES["temperature_enonce"] = G(P63, B63, "heure (h)", "température (°C)")
FIGURES["temperature_corrige"] = G(P63, B63 + r"""
  \lirev{9}{6} \pv{9}{6}
  \draw[niveau] (axis cs:0,10) -- (axis cs:20.5,10);
  \lirex{11}{10} \lirex{18}{10} \pv{11}{10} \pv{18}{10}
  \pv{15}{14} \pv{6}{1}
  \node[vert,anchor=south] at (axis cs:15,14.35) {max : $14$ °C};
  \node[vert,anchor=north west,align=left] at (axis cs:0.4,16.6) {$9$ h : $6$ °C\\$10$ °C : $11$ h et $18$ h\\min : $1$ °C à $6$ h};
""", "heure (h)", "température (°C)")

# =============================================================== 2664 carré
DONNEES["carre"] = [(c, 4 * c, c * c) for c in range(1, 6)]
P64 = (r"width=5.4cm, height=6.2cm, xmin=0, xmax=5.6, ymin=0, ymax=27.5, xtick=" + lst(1, 5, 1)
       + r", minor x tick num=1, ytick=" + lst(2, 26, 2))
FIGURES["carre_enonce"] = G(P64, "", "côté $c$ (cm)", "")
FIGURES["carre_corrige"] = G(P64, r"""
  \addplot[courbe, domain=0:5.4] {4*x};
  \addplot[courbeB, domain=0:5.2] {x^2};
""" + nuage([(c, p) for c, p, a in DONNEES["carre"]]) + nuage([(c, a) for c, p, a in DONNEES["carre"]], "otOrange")
    + r"""
  \lirev{4}{16} \pv{4}{16}
  \node[bleu,anchor=south east] at (axis cs:2.4,11) {$P = 4c$};
  \node[orange,anchor=north west] at (axis cs:2.7,6.4) {$A = c^2$};
  \node[vert,anchor=north west,align=left] at (axis cs:4.1,15.2) {$c = 4$ :\\$P = A = 16$};
""", "côté $c$ (cm)", "")

# =============================================================== 2665 plante
DONNEES["plante"] = [(0, 2), (1, 3), (2, 5), (3, 8), (4, 12), (5, 15), (6, 17), (7, 18), (8, 18.5)]
P65 = (r"width=6cm, height=5.2cm, xmin=0, xmax=8.7, ymin=0, ymax=20.8, xtick=" + lst(1, 8, 1)
       + r", ytick=" + lst(2, 20, 2) + r", minor y tick num=1")
B65 = poly(DONNEES["plante"])
FIGURES["plante_enonce"] = G(P65, B65, "semaines", "hauteur (cm)")
FIGURES["plante_corrige"] = G(P65, B65 + r"""
  \draw[otGreenDark,line width=2.6pt] (axis cs:3,8) -- (axis cs:4,12);
  \lirev{4}{12} \pv{4}{12}
  \liry{5}{15} \lirex{5}{15} \pv{5}{15}
  \node[vert,anchor=west] at (axis cs:3.65,8.6) {$+4$ cm};
""", "semaines", "hauteur (cm)")

# =============================================================== 2666 baignoire
DONNEES["baignoire"] = [(0, 0), (10, 30), (12, 30), (12, 38), (24, 38), (24, 30), (28, 30), (40, 0)]
P66 = (r"width=6.3cm, height=4.8cm, xmin=0, xmax=42.5, ymin=0, ymax=43, xtick=" + lst(4, 40, 4)
       + r", minor x tick num=1, ytick=" + lst(10, 40, 10) + r", minor y tick num=4")
B66 = poly(DONNEES["baignoire"])
FIGURES["baignoire_enonce"] = G(P66, B66, "temps (min)", "hauteur d'eau (cm)")
FIGURES["baignoire_corrige"] = G(P66, B66 + r"""
  \lirev{10}{30} \pv{10}{30}
  \draw[niveau] (axis cs:0,15) -- (axis cs:36,15);
  \lirex{5}{15} \lirex{34}{15} \pv{5}{15} \pv{34}{15}
  \node[vert,anchor=south] at (axis cs:18,38.6) {bain : $12$ min};
  \node[vert,anchor=east] at (axis cs:11.4,34) {$+8$ cm};
  \node[vert,anchor=north] at (axis cs:20,13.8) {$15$ cm : $5$ min et $34$ min};
""", "temps (min)", "hauteur d'eau (cm)")

# =============================================================== 2667 taxi
DONNEES["taxi"] = [(d, 2.5 + 1.2 * d) for d in (0, 5, 10, 15, 20)]
P67 = (r"width=6.1cm, height=5.4cm, xmin=0, xmax=22.5, ymin=0, ymax=29.5, xtick=" + lst(5, 20, 5)
       + r", minor x tick num=4, ytick=" + lst(4, 28, 4) + r", minor y tick num=1")
XL67 = [(x, "c", str(x)) for x in range(2, 23, 2)]
FIGURES["taxi_enonce"] = G(P67, "", "distance (km)", "prix (€)")
FIGURES["taxi_corrige"] = G(P67, r"""
  \addplot[courbe, domain=0:21.5] {2.5+1.2*x};
""" + nuage(DONNEES["taxi"]) + r"""
  \lirev{7}{10.9} \pv{7}{10.9}
  \node[vert,anchor=north west] at (axis cs:7.5,9.6) {$7$ km : environ $11$ €};
  \node[bleu,anchor=north west] at (axis cs:12.5,15.5) {prix $= 2{,}50 + 1{,}20 \times d$};
""", "distance (km)", "prix (€)")

# =============================================================== 2668 associer
def petit_axe(x0, y0, titre, opts, corps, xl, yl):
    return (r"\begin{axis}[gr, at={(%gcm,%gcm)}, width=3.0cm, height=2.2cm, " % (x0, y0) + opts
            + r", title={%s}, title style={font=\otMedium\fontsize{9}{10}\selectfont,text=otNavy,yshift=9pt}" % titre
            + r", xlabel={%s}, ylabel={%s}]" % (xl, yl) + "\n" + corps + "\n" + r"\zero" + "\n" + r"\end{axis}" + "\n")


A68 = [
    ("Graphique 1", r"xmin=0, xmax=10.5, ymin=0, ymax=118, xtick={5,10}, ytick={50,100}",
     r"\draw[ligne] (axis cs:0,20) -- (axis cs:4,100) -- (axis cs:10,100);", "min", "°C"),
    ("Graphique 2", r"xmin=0, xmax=6.8, ymin=0, ymax=14, xtick={2,4,6}, ytick={4,8,12}",
     r"\draw[ligne] (axis cs:0,12) -- (axis cs:6,0);", "h", "cm"),
    ("Graphique 3", r"xmin=0, xmax=6.8, ymin=0, ymax=1420, xtick={2,4,6}, ytick={400,800,1200}",
     r"\draw[ligne] (axis cs:0,400) -- (axis cs:3,1200) -- (axis cs:6,400);", "h", "m"),
    ("Graphique 4", r"xmin=0, xmax=3.4, ymin=0, ymax=70, xtick={1,2,3}, ytick={20,40,60}",
     r"\draw[ligne] (axis cs:0,0) -- (axis cs:3,60);", "h", "km"),
]


def associer(corrige=False):
    noms = ["bouilloire (d)", "bougie (b)", "randonneur (c)", "cycliste (a)"]
    s = r"\begin{tikzpicture}" + "\n"
    pos = [(0, 3.9), (4.6, 3.9), (0, 0), (4.6, 0)]
    for k, (t, o, c, xl, yl) in enumerate(A68):
        titre = t + (r" : \textcolor{otGreenDark}{%s}" % noms[k] if corrige else "")
        s += petit_axe(pos[k][0], pos[k][1], titre, o, c, xl, yl)
    return s + r"\end{tikzpicture}"


FIGURES["associer_enonce"] = associer()
FIGURES["associer_corrige"] = associer(True)

# =============================================================== 2669 vitesse
DONNEES["vitesse"] = [(0, 0), (10, 50), (40, 50), (50, 0), (60, 0)]
P69 = (r"width=6.8cm, height=4.4cm, xmin=0, xmax=63, ymin=0, ymax=58, xtick=" + lst(10, 60, 10)
       + r", minor x tick num=1, ytick=" + lst(10, 50, 10) + r", minor y tick num=1")
B69 = poly(DONNEES["vitesse"])
FIGURES["vitesse_enonce"] = G(P69, B69, "temps (s)", "vitesse (km/h)")
FIGURES["vitesse_corrige"] = G(P69, B69 + r"""
  \draw[niveau] (axis cs:0,25) -- (axis cs:49,25);
  \lirex{5}{25} \lirex{45}{25} \pv{5}{25} \pv{45}{25}
  \node[vert,anchor=north] at (axis cs:25,47.5) {vitesse constante};
  \node[vert,anchor=south] at (axis cs:25,26) {$25$ km/h};
  \node[vert,anchor=south] at (axis cs:55.5,1.5) {arrêt};
""", "temps (s)", "vitesse (km/h)")

# =============================================================== 2670 récipients
FIGURES["recipients"] = r"""
\begin{tikzpicture}
  \fill[otSky] (0,0) rectangle (1.8,3);
  \draw[otNavy,line width=1pt] (0,3) -- (0,0) -- (1.8,0) -- (1.8,3);
  \fill[otOrange!15] (3.6,3) -- (5.1,0) -- (6.6,3) -- cycle;
  \draw[otOrange!85!black,line width=1pt] (3.6,3) -- (5.1,0) -- (6.6,3);
  \draw[cote] (-0.35,0) -- (-0.35,3);
  \node[anchor=east,text=otInk] at (-0.45,1.5) {$20$ cm};
  \draw[otMuted!70,line width=.4pt] (-0.5,0) -- (-0.05,0) (-0.5,3) -- (-0.05,3);
  \node[anchor=north,text=otNavy] at (0.9,-0.15) {récipient A};
  \node[anchor=north,text=otOrange!85!black] at (5.1,-0.15) {récipient B};
  \node[petitG,anchor=north] at (0.9,-0.65) {cylindre};
  \node[petitG,anchor=north] at (5.1,-0.65) {cône, pointe en bas};
\end{tikzpicture}
"""
DONNEES["recipients"] = {"A": lambda v: v / 80, "B": lambda v: 20 * (v / 1600) ** (1 / 3)}
P70 = (r"width=6.1cm, height=5cm, xmin=0, xmax=1720, ymin=0, ymax=22.5, xtick=" + lst(200, 1600, 200)
       + r", xticklabels={,400,,800,,1200,,1600}, minor x tick num=1, ytick=" + lst(2, 20, 2) + r", minor y tick num=1")
B70 = r"""
  \addplot[courbe, domain=0:1600] {x/80};
  \addplot[courbeB, domain=0:1600, samples=200] {20*(x/1600)^(1/3)};
  \node[bleu,anchor=north west] at (axis cs:1250,13.6) {$\mathcal{C}_1$};
  \node[orange] at (axis cs:260,18.6) {$\mathcal{C}_2$};
"""
FIGURES["recipients_courbes"] = G(P70, B70, "volume (cm³)", "hauteur (cm)")
FIGURES["recipients_corrige"] = G(P70, B70 + r"""
  \lirex{800}{15.874} \liry{800}{15.874} \pv{800}{15.874}
  \lirev{800}{10} \pv{800}{10}
  \liry{1200}{15} \lirex{1200}{15} \pv{1200}{15}
  \liry{200}{10} \lirex{200}{10} \pv{200}{10}
""", "volume (cm³)", "hauteur (cm)")

# =============================================================== 2671 course
DONNEES["ana"] = lambda t: 4 * t
DONNEES["ben"] = lambda t: 5 * (t - 20)
P71 = (r"width=6.6cm, height=5.2cm, xmin=0, xmax=162, ymin=0, ymax=680, xtick=" + lst(20, 160, 20)
       + r", minor x tick num=1, ytick=" + lst(100, 600, 100) + r", minor y tick num=1")
B71 = r"""
  \addplot[courbe, domain=0:150] {4*x};
  \addplot[courbeB, domain=20:140] {5*(x-20)};
  \node[bleu,anchor=south east] at (axis cs:58,250) {Ana};
  \node[orange,anchor=north west] at (axis cs:62,170) {Ben};
"""
FIGURES["course_enonce"] = G(P71, B71, "temps (s)", "distance (m)")
FIGURES["course_corrige"] = G(P71, B71 + r"""
  \lirev{100}{400} \pv{100}{400}
  \draw[niveau] (axis cs:0,600) -- (axis cs:150,600);
  \lirex{140}{600} \lirex{150}{600} \pv{140}{600} \pv{150}{600}
  \node[vert,anchor=north west] at (axis cs:103,380) {$(100\ ;\ 400)$};
  \node[vert,anchor=south] at (axis cs:70,605) {arrivée : $600$ m};
""", "temps (s)", "distance (m)")

# =============================================================== 2672 population
DONNEES["population"] = [(0, 8), (10, 9), (20, 11), (30, 15), (40, 17), (50, 16), (60, 18), (70, 21)]
P72 = (r"width=5.3cm, height=5cm, xmin=0, xmax=74, ymin=0, ymax=23, xtick=" + lst(10, 70, 10)
       + r", ytick=" + lst(2, 22, 2) + r", minor y tick num=1, minor x tick num=1")
B72 = poly(DONNEES["population"])
FIGURES["population_enonce"] = G(P72, B72, "années après 1950", "habitants (milliers)")
FIGURES["population_corrige"] = G(P72, B72 + r"""
  \draw[otGreenDark,line width=2.6pt] (axis cs:20,11) -- (axis cs:30,15);
  \lirev{30}{15} \pv{30}{15}
  \lirex{50}{16} \pv{50}{16}
  \lirex{25}{13} \pv{25}{13}
  \node[vert,anchor=west] at (axis cs:31,11) {$+4$ milliers};
""", "années après 1950", "habitants (milliers)")

# =============================================================== 2673 rectangle
DONNEES["rectangle"] = {x: x * (10 - x) for x in range(0, 11)}
P73 = (r"width=6cm, height=5.2cm, xmin=0, xmax=10.8, ymin=0, ymax=28, xtick=" + lst(1, 10, 1)
       + r", ytick=" + lst(2, 26, 2) + r", minor y tick num=1")
B73 = r"""
  \addplot[courbe, domain=0:10, samples=100] {x*(10-x)};
""" + nuage([(x, v) for x, v in DONNEES["rectangle"].items()])
FIGURES["rectangle_enonce"] = G(P73, B73, "largeur $x$ (cm)", "aire (cm²)")
FIGURES["rectangle_corrige"] = G(P73, B73 + r"""
  \lirev{5}{25} \pv{5}{25}
  \draw[niveau] (axis cs:0,16) -- (axis cs:9.6,16);
  \lirex{2}{16} \lirex{8}{16} \pv{2}{16} \pv{8}{16}
  \node[vert,anchor=south] at (axis cs:5,25.4) {maximum : $25$ cm²};
""", "largeur $x$ (cm)", "aire (cm²)")

# =============================================================== 2674 vélo
P74 = (r"width=6.4cm, height=5.4cm, xmin=0, xmax=11.6, ymin=0, ymax=30, xtick=" + lst(1, 11, 1)
       + r", ytick=" + lst(2, 28, 2))
B74 = r"""
  \addplot[courbe, domain=0:9.6] {3*x};
  \addplot[courbeB, domain=0:11.2] {10+x};
  \node[bleu,anchor=east] at (axis cs:8.4,26.5) {tarif A};
  \node[orange,anchor=south east] at (axis cs:10.3,21.3) {tarif B};
"""
FIGURES["velo_enonce"] = G(P74, B74, "durée (h)", "prix (€)")
FIGURES["velo_corrige"] = G(P74, B74 + r"""
  \lirev{5}{15} \pv{5}{15}
  \node[vert,anchor=north west,align=left] at (axis cs:0.3,29.6) {avant $5$ h :\\A moins cher};
  \node[vert,anchor=north west,align=left] at (axis cs:8.6,17.6) {après $5$ h :\\B moins cher};
  \node[vert,anchor=north west] at (axis cs:5.2,13.8) {$(5\ ;\ 15)$};
""", "durée (h)", "prix (€)")

# =============================================================== 2675 ballon
DONNEES["ballon"] = lambda t: -5 * t ** 2 + 20 * t
P75 = (r"width=6cm, height=4.8cm, xmin=0, xmax=4.4, ymin=0, ymax=23, xtick=" + lst(0.5, 4, 0.5)
       + r", ytick=" + lst(2, 22, 2) + r", minor y tick num=1")
B75 = r"""
  \addplot[courbe, domain=0:4, samples=100] {-5*x^2+20*x};
"""
FIGURES["ballon_enonce"] = G(P75, B75, "temps (s)", "hauteur (m)")
FIGURES["ballon_corrige"] = G(P75, B75 + r"""
  \lirev{2}{20} \pv{2}{20}
  \draw[niveau] (axis cs:0,15) -- (axis cs:3.6,15);
  \lirex{1}{15} \lirex{3}{15} \pv{1}{15} \pv{3}{15}
  \pv{4}{0}
  \node[vert,anchor=south] at (axis cs:2,20.4) {maximum : $20$ m};
  \node[vert,anchor=west] at (axis cs:3.65,15) {$15$ m};
""", "temps (s)", "hauteur (m)")

# =============================================================== 2676 freinage
DONNEES["freinage"] = [(v, v * v / 200) for v in range(0, 121, 20)]
P76 = (r"width=6.1cm, height=5.4cm, xmin=0, xmax=132, ymin=0, ymax=80, xtick=" + lst(20, 120, 20)
       + r", minor x tick num=1, ytick=" + lst(10, 70, 10) + r", minor y tick num=1")
FIGURES["freinage_enonce"] = G(P76, "", "vitesse (km/h)", "distance de freinage (m)")
FIGURES["freinage_corrige"] = G(P76, r"""
  \addplot[courbe, domain=0:122, samples=100] {x^2/200};
""" + nuage(DONNEES["freinage"]) + r"""
  \liry{89.44}{40} \lirex{89.44}{40} \pv{89.44}{40}
  \node[vert,anchor=north west] at (axis cs:91,37) {environ $90$ km/h};
""", "vitesse (km/h)", "distance de freinage (m)")

# =============================================================== 2677 Léa
DONNEES["lea"] = [(0, 0), (15, 4), (25, 4), (45, 9), (60, 9), (90, 0)]
P77 = (r"width=6.3cm, height=4.8cm, xmin=0, xmax=95, ymin=0, ymax=10.6, xtick=" + lst(15, 90, 15)
       + r", minor x tick num=2, ytick=" + lst(1, 10, 1))
B77 = poly(DONNEES["lea"])
FIGURES["lea_enonce"] = G(P77, B77, "temps (min)", "distance à la maison (km)")
FIGURES["lea_corrige"] = G(P77, B77 + r"""
  \draw[niveau] (axis cs:0,6) -- (axis cs:75,6);
  \lirex{33}{6} \lirex{70}{6} \pv{33}{6} \pv{70}{6}
  \node[vert,anchor=south] at (axis cs:20,4.15) {arrêt};
  \node[vert,anchor=north] at (axis cs:52.5,8.85) {arrêt};
  \node[vert,anchor=north] at (axis cs:51.5,3.0) {$33$ et $70$ min};
""", "temps (min)", "distance à la maison (km)")

# =============================================================== 2678 plongée
DONNEES["plongee"] = lambda d: 1 + d / 10
P78 = (r"width=5.9cm, height=4.8cm, xmin=0, xmax=43, ymin=0, ymax=5.6, xtick=" + lst(5, 40, 5)
       + r", minor x tick num=4, ytick=" + lst(0.5, 5, 0.5)
       + r", yticklabels={,1,,2,,3,,4,,5}")
B78 = r"""
  \addplot[courbe, domain=0:40] {1+x/10};
"""
FIGURES["plongee_enonce"] = G(P78, B78, "profondeur (m)", "pression (bar)")
FIGURES["plongee_corrige"] = G(P78, B78 + r"""
  \liry{25}{3.5} \lirex{25}{3.5} \pv{25}{3.5}
  \liry{12}{2.2} \lirex{12}{2.2} \pv{12}{2.2}
  \pv{0}{1}
  \node[vert,anchor=north west] at (axis cs:25.6,3.42) {$3{,}5$ bar};
  \node[vert,anchor=north west] at (axis cs:12.6,2.12) {$2{,}2$ bar};
""", "profondeur (m)", "pression (bar)")

# =============================================================== 2679 four
DONNEES["four"] = lambda t: (20 + 18 * t) if t <= 10 else (200 if t <= 40 else 20 + 180 * 2 ** (-(t - 40) / 15))
P79 = (r"width=6.2cm, height=5cm, xmin=0, xmax=92, ymin=0, ymax=228, xtick=" + lst(10, 90, 10)
       + r", minor x tick num=1, ytick=" + lst(20, 220, 20) + r", minor y tick num=1")
B79 = r"""
  \draw[ligne] (axis cs:0,20) -- (axis cs:10,200) -- (axis cs:40,200);
  \addplot[courbe, domain=40:85, samples=100] {20+180*2^(-(x-40)/15)};
"""
FIGURES["four_enonce"] = G(P79, B79, "temps (min)", "température (°C)")
FIGURES["four_corrige"] = G(P79, B79 + r"""
  \lirev{55}{110} \pv{55}{110}
  \lirev{70}{65} \pv{70}{65}
  \draw[niveau] (axis cs:0,100) -- (axis cs:57.5,100);
  \lirex{57.5}{100} \pv{57.5}{100}
  \node[vert,anchor=south] at (axis cs:25,200.5) {palier : $30$ min};
  \node[vert,anchor=south west] at (axis cs:61,112) {$110$ °C};
  \node[vert,anchor=south west] at (axis cs:72,67) {$65$ °C};
""", "temps (min)", "température (°C)")

# =============================================================== 2680 boîte
FIGURES["boite_patron"] = r"""
\begin{tikzpicture}
  \def\a{3.6} \def\x{0.68}
  \fill[otOrange!18] (0,0) rectangle (\x,\x) (\a-\x,0) rectangle (\a,\x) (0,\a-\x) rectangle (\x,\a) (\a-\x,\a-\x) rectangle (\a,\a);
  \fill[otSky] (\x,\x) rectangle (\a-\x,\a-\x);
  \draw[otNavy,line width=0.9pt] (0,0) rectangle (\a,\a);
  \draw[otOrange!85!black,line width=0.8pt] (\x,0) -- (\x,\x) -- (0,\x) (\a-\x,0) -- (\a-\x,\x) -- (\a,\x)
     (0,\a-\x) -- (\x,\a-\x) -- (\x,\a) (\a-\x,\a) -- (\a-\x,\a-\x) -- (\a,\a-\x);
  \draw[otNavy!60,line width=0.6pt,dash pattern=on 3pt off 2pt] (\x,\x) rectangle (\a-\x,\a-\x);
  \node[text=otOrange!85!black] at (\x/2,\x/2) {$x$};
  \draw[cote] (0,-0.4) -- (\a,-0.4) node[midway,coteTexte] {$20$ cm};
  \draw[otMuted!70,line width=.4pt] (0,-0.55) -- (0,-0.05) (\a,-0.55) -- (\a,-0.05);
  \draw[cote] (-0.4,0) -- (-0.4,\a) node[midway,coteTexte] {$20$ cm};
  \draw[otMuted!70,line width=.4pt] (-0.55,0) -- (-0.05,0) (-0.55,\a) -- (-0.05,\a);
  % boîte
  \begin{scope}[xshift=5.0cm,yshift=0.9cm]
    \def\b{2.4} \def\h{0.7} \def\px{0.8} \def\py{0.55}
    \fill[otSky] (0,0) -- (\b,0) -- (\b,\h) -- (0,\h) -- cycle;
    \fill[otSky!60] (\b,0) -- (\b+\px,\py) -- (\b+\px,\py+\h) -- (\b,\h) -- cycle;
    \draw[otNavy,line width=0.9pt,line join=round] (0,\h) -- (0,0) -- (\b,0) -- (\b,\h) -- cycle
      (\b,0) -- (\b+\px,\py) -- (\b+\px,\py+\h) -- (\b,\h)
      (0,\h) -- (\px,\py+\h) -- (\b+\px,\py+\h);
    \draw[otNavy!50,line width=0.6pt,dash pattern=on 3pt off 2pt] (0,0) -- (\px,\py) -- (\b+\px,\py) (\px,\py) -- (\px,\py+\h);
    \draw[cote] (0,-0.35) -- (\b,-0.35) node[midway,coteTexte] {$20 - 2x$};
    \draw[otMuted!70,line width=.4pt] (0,-0.5) -- (0,-0.05) (\b,-0.5) -- (\b,-0.05);
    \draw[cote] (-0.35,0) -- (-0.35,\h);
    \draw[otMuted!70,line width=.4pt] (-0.5,0) -- (-0.05,0) (-0.5,\h) -- (-0.05,\h);
    \node[anchor=east,text=otInk] at (-0.5,\h/2) {$x$};
  \end{scope}
  \draw[otMuted,line width=0.8pt,-{Stealth[length=2.2mm]}] (3.9,2.1) -- (4.75,2.1);
  \node[petitG,anchor=south] at (4.32,2.2) {pliage};
\end{tikzpicture}
"""
DONNEES["boite"] = lambda x: x * (20 - 2 * x) ** 2
P80 = (r"width=6.4cm, height=5.2cm, xmin=0, xmax=10.7, ymin=0, ymax=680, xtick=" + lst(1, 10, 1)
       + r", minor x tick num=1, ytick=" + lst(100, 600, 100) + r", minor y tick num=1")
B80 = r"""
  \addplot[courbe, domain=0:10, samples=150] {x*(20-2*x)^2};
"""
FIGURES["boite_enonce"] = G(P80, B80, "$x$ (cm)", "volume (cm³)")
FIGURES["boite_corrige"] = G(P80, B80 + r"""
  \lirev{3.333}{592.6} \pv{3.333}{592.6}
  \draw[niveau] (axis cs:0,500) -- (axis cs:6.2,500);
  \lirex{1.91}{500} \lirex{5}{500} \pv{1.91}{500} \pv{5}{500}
  \node[vert,anchor=south west] at (axis cs:3.6,600) {maximum : environ $593$ cm³};
  \node[vert,anchor=west] at (axis cs:6.3,500) {$500$ cm³};
""", "$x$ (cm)", "volume (cm³)")

# =============================================================== 2681 rentabilité
P81 = (r"width=6.6cm, height=5.2cm, xmin=0, xmax=106, ymin=0, ymax=960, xtick=" + lst(10, 100, 10)
       + r", xticklabels={,20,,40,,60,,80,,100}, ytick=" + lst(100, 900, 100) + r", minor y tick num=1")
B81 = r"""
  \addplot[courbe, domain=0:100] {200+5*x};
  \addplot[courbeB, domain=0:100] {9*x};
  \node[bleu,anchor=south east] at (axis cs:28,345) {coût};
  \node[orange,anchor=north west] at (axis cs:30,240) {recette};
"""
FIGURES["rentabilite_enonce"] = G(P81, B81, "objets", "montant (€)")
FIGURES["rentabilite_corrige"] = G(P81, B81 + r"""
  \lirev{50}{450} \pv{50}{450}
  \draw[otGreenDark,line width=1pt,{Stealth[length=2mm]}-{Stealth[length=2mm]}] (axis cs:90,650) -- (axis cs:90,810);
  \node[vert,anchor=west] at (axis cs:91.5,745) {bénéfice};
  \node[vert,anchor=north west] at (axis cs:52,430) {$(50\ ;\ 450)$};
""", "objets", "montant (€)")

# =============================================================== 2682 cardiaque
DONNEES["cardiaque"] = [(0, 70), (5, 72), (10, 150), (30, 158), (35, 180), (40, 120), (45, 90)]
P82 = (r"width=6.2cm, height=5.2cm, xmin=0, xmax=48, ymin=0, ymax=205, xtick=" + lst(5, 45, 5)
       + r", minor x tick num=4, ytick=" + lst(20, 200, 20) + r", minor y tick num=1")
B82 = poly(DONNEES["cardiaque"])
FIGURES["cardiaque_enonce"] = G(P82, B82, "temps (min)", "battements par minute")
FIGURES["cardiaque_corrige"] = G(P82, r"""
  \fill[otGreen!18] (axis cs:0,123.6) rectangle (axis cs:46,154.5);
  \draw[otGreenDark,line width=0.7pt] (axis cs:0,123.6) -- (axis cs:46,123.6) (axis cs:0,154.5) -- (axis cs:46,154.5);
""" + B82 + r"""
  \lirex{21.25}{154.5} \pv{21.25}{154.5}
  \pv{35}{180}
  \node[vert,anchor=north west,align=left] at (axis cs:23,72) {zone d'endurance :\\de $123{,}6$ à $154{,}5$};
  \node[vert,anchor=south] at (axis cs:35,182) {$180$};
""", "temps (min)", "battements par minute")

# =============================================================== 2683 basket
DONNEES["basket"] = lambda x: -0.2 * x ** 2 + 1.6 * x + 2
P83 = (r"width=6.4cm, height=4.6cm, xmin=0, xmax=9.9, ymin=0, ymax=6.4, xtick=" + lst(1, 9, 1)
       + r", minor x tick num=1, ytick=" + lst(1, 6, 1) + r", minor y tick num=1")
B83 = r"""
  \addplot[courbe, domain=0:9.099, samples=120] {-0.2*x^2+1.6*x+2};
  \draw[otOrange!85!black,line width=1.6pt] (axis cs:7.05,3.05) -- (axis cs:7.45,3.05);
  \node[orange,anchor=west] at (axis cs:7.55,3.2) {panier};
"""
FIGURES["basket_enonce"] = G(P83, B83, "distance (m)", "hauteur (m)")
FIGURES["basket_corrige"] = G(P83, B83 + r"""
  \lirev{4}{5.2} \pv{4}{5.2}
  \draw[otOrange!85!black,line width=1.6pt] (axis cs:1,0) -- (axis cs:1,3);
  \pv{1}{3.4}
  \node[vert,anchor=south] at (axis cs:4,5.35) {maximum : $5{,}2$ m};
  \node[orange,anchor=west] at (axis cs:1.15,1.3) {bras : $3$ m};
  \node[vert,anchor=north west] at (axis cs:1.15,3.25) {$3{,}4$ m};
""", "distance (m)", "hauteur (m)")
