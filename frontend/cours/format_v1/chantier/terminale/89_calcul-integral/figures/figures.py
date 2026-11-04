# -*- coding: utf-8 -*-
"""Figures de la notion « Calcul intégral » (Terminale), style des livres OptiTAB.

Compilation : python ../../../outils/figures_livre.py <dossier_notion> [--planche]
Conventions : domaine compté positivement en vert (otGreen!30), partie comptée
négativement en orange (otOrange!35), aire « sous la courbe » d'une valeur
moyenne en bleu pâle et rectangle de même aire en vert, courbe principale en
bleu marine, seconde courbe en vert.
"""

V = r"fill=otGreen!30, draw=none"          # domaine compté positivement
O = r"fill=otOrange!35, draw=none"         # partie sous l'axe
B = r"fill=otNavy!14, draw=none"           # aire sous la courbe (valeur moyenne)
RECT = r"otGreen, fill opacity=0.24"       # rectangle de même aire
TIRETS = r"otGreenDark, line width=1pt, dash pattern=on 4pt off 2.5pt"


def fig(options, corps, trig=False):
    style = "otTrig" if trig else "otWeb"
    return ("\\begin{tikzpicture}\n\\begin{axis}[" + style + ", " + options + "]\n"
            + corps + "\n\\end{axis}\n\\end{tikzpicture}")


def sous(f, a, b, style=V):
    """Domaine entre la courbe de f et l'axe des abscisses sur [a ; b]."""
    return f"  \\addplot[{style}, domain={a}:{b}, samples=160] {{{f}}} \\closedcycle;\n"


def entre(f, g, a, b, nom="r"):
    """Domaine entre deux courbes sur [a ; b]."""
    return (f"  \\addplot[name path={nom}1, draw=none, domain={a}:{b}, samples=200] {{{f}}};\n"
            f"  \\addplot[name path={nom}2, draw=none, domain={a}:{b}, samples=200] {{{g}}};\n"
            f"  \\addplot[otGreen!30] fill between[of={nom}1 and {nom}2];\n")


def borne(x, y1, y2=0, couleur="otGreenDark"):
    return f"  \\draw[{couleur}, line width=0.7pt] (axis cs:{x},{y2}) -- (axis cs:{x},{y1});\n"


def courbe(f, a, b, style="courbe"):
    return f"  \\addplot[{style}, domain={a}:{b}, samples=200] {{{f}}};\n"


def etiq(x, y, texte, ancre, couleur="otNavy"):
    return f"  \\node[etiq, text={couleur}, anchor={ancre}] at (axis cs:{x},{y}) {{{texte}}};\n"


def region(x, y, texte, couleur="otGreenDark"):
    return f"  \\node[text={couleur}] at (axis cs:{x},{y}) {{{texte}}};\n"


def moyenne(a, b, mu, f, extra=""):
    """Aire sous la courbe (bleu pâle) et rectangle de même aire (vert)."""
    return (sous(f, a, b, B)
            + f"  \\fill[{RECT}] (axis cs:{a},0) rectangle (axis cs:{b},{mu});\n"
            + f"  \\draw[{TIRETS}] (axis cs:{a},0) -- (axis cs:{a},{mu}) -- (axis cs:{b},{mu}) -- (axis cs:{b},0);\n"
            + extra)


def legende(lignes, long):
    """Légende : petit trait de la couleur de la courbe, puis le texte à droite."""
    return "".join(
        f"  \\draw[{style}] (axis cs:{x},{y}) -- (axis cs:{x + long},{y});\n"
        f"  \\node[anchor=west, text=otInk] at (axis cs:{x + long + 0.01},{y}) {{{texte}}};\n"
        for x, y, style, texte in lignes)


TIR = "otNavy, line width=1.35pt, dash pattern=on 5pt off 2.5pt"
POI = "otNavy, line width=1.5pt, dash pattern=on 1.2pt off 1.8pt"

P2, P4, PI = r"\frac{\pi}{2}", r"\frac{\pi}{4}", r"\pi"
X2 = "x^2"

FIGURES = {
# ================================================================== cours
"cours_aire_def": fig(
    r"width=6.6cm, height=3.8cm, xmin=-0.3, xmax=5.4, ymin=-0.3, ymax=3.1, grid=none, xtick={1,4}, xticklabels={$a$,$b$}, ytick=\empty",
    sous("1.2+0.9*sin(1.3*x)+0.25*x", 1, 4)
    + borne(1, 2.317) + borne(4, 1.405)
    + courbe("1.2+0.9*sin(1.3*x)+0.25*x", 0.15, 5.1)
    + region(2.5, 0.75, r"$\mathcal{D}$")
    + etiq(1.8, 2.47, r"$\mathcal{C}_f$", "south west"), trig=True),

"cours_demo": fig(
    r"width=6.6cm, height=4cm, xmin=-0.3, xmax=4.7, ymin=-0.25, ymax=2.9, grid=none, xtick={0.6,2.2,3.2}, xticklabels={$a$,$x$,$x+h$}, ytick={0.9808,1.6288}, yticklabels={$f(x)$,$f(x+h)$}",
    sous("0.4+0.12*x^2", 0.6, 2.2, B)
    + r"  \fill[otOrange!30] (axis cs:2.2,0) rectangle (axis cs:3.2,1.6288);" + "\n"
    + r"  \draw[otOrange, line width=0.8pt] (axis cs:2.2,0) rectangle (axis cs:3.2,1.6288);" + "\n"
    + r"  \fill[otGreen!45] (axis cs:2.2,0) rectangle (axis cs:3.2,0.9808);" + "\n"
    + r"  \draw[otGreenDark, line width=0.8pt] (axis cs:2.2,0) rectangle (axis cs:3.2,0.9808);" + "\n"
    + r"  \draw[guide] (axis cs:0,0.9808) -- (axis cs:2.2,0.9808);" + "\n"
    + r"  \draw[guide] (axis cs:0,1.6288) -- (axis cs:2.2,1.6288);" + "\n"
    + borne(0.6, 0.4432, couleur="otNavy!60")
    + courbe("0.4+0.12*x^2", 0, 4.4)
    + region(1.4, 0.38, r"$F(x)$", "otNavy")
    + etiq(3.95, 2.45, r"$\mathcal{C}_f$", "south east")),

"cours_sin_signe": fig(
    r"width=7.2cm, height=3cm, xmin=-0.3, xmax=6.95, ymin=-1.45, ymax=1.55, xtick={3.1416,6.2832}, xticklabels={$\pi$,$2\pi$}, ytick={-1,1}",
    sous("sin(x)", 0, 3.1416) + sous("sin(x)", 3.1416, 6.2832, O)
    + courbe("sin(x)", 0, 6.6)
    + r"  \node[text=otGreenDark, font=\Large] at (axis cs:1.5708,0.42) {$+$};" + "\n"
    + r"  \node[text=otOrange!80!black, font=\Large] at (axis cs:4.7124,-0.42) {$-$};" + "\n"
    + etiq(4.75, 0.3, r"$y=\sin x$", "south"), trig=True),

"cours_entre": fig(
    r"width=5.6cm, height=4.4cm, xmin=-0.15, xmax=1.4, ymin=-0.15, ymax=1.4, xtick={0.5,1}, ytick={0.5,1}",
    entre("x", "x^2", 0, 1)
    + courbe("x", -0.1, 1.3, "courbe2") + courbe(X2, -0.1, 1.15)
    + r"  \pnt{0}{0} \pnt{1}{1}" + "\n"
    + region(0.5, 0.375, r"$\mathcal{A}$")
    + etiq(0.52, 0.75, r"$y=x$", "south east", "otGreenDark")
    + etiq(0.75, 0.42, r"$y=x^2$", "north west")),

"cours_moyenne": fig(
    r"width=6cm, height=4.4cm, xmin=-0.35, xmax=3.8, ymin=-0.6, ymax=10.4, xtick={1,2,3}, ytick={3,6,9}",
    moyenne(0, 3, 3, X2)
    + courbe(X2, 0, 3.22)
    + etiq(3.1, 3, r"$\mu=3$", "west", "otGreenDark")
    + etiq(2.55, 7.5, r"$y=x^2$", "east")),

"cours_rectangles": fig(
    r"width=6cm, height=4.2cm, xmin=-0.25, xmax=2.45, ymin=-0.35, ymax=4.7, xtick={0.5,1,1.5,2}, ytick={1,2,3,4}",
    "".join(
        f"  \\filldraw[fill=otGreen!40, draw=otGreenDark, line width=0.5pt] (axis cs:{k/4},0) rectangle (axis cs:{(k+1)/4},{(k/4)**2});\n"
        f"  \\filldraw[fill=otOrange!30, draw=otOrange, line width=0.5pt] (axis cs:{k/4},{(k/4)**2}) rectangle (axis cs:{(k+1)/4},{((k+1)/4)**2});\n"
        for k in range(8))
    + courbe(X2, 0, 2.15)
    + etiq(1.45, 3.45, r"$y=x^2$", "east")),

# ================================================================== fiche
"fiche_aire_x2": fig(
    r"width=6cm, height=4.2cm, xmin=-0.3, xmax=2.5, ymin=-0.4, ymax=4.8, xtick={0.5,1,1.5,2}, ytick={1,2,3,4}",
    sous(X2, 0, 2) + borne(2, 4)
    + courbe(X2, -0.2, 2.15)
    + etiq(0.06, 3.4, r"$\displaystyle\int_0^2 x^2\,\mathrm{d}x=\frac{8}{3}$ u.a.", "west", "otGreenDark")
    + etiq(2.0, 4.5, r"$y=x^2$", "east")),

# ================================================================== 1235 aires entre deux courbes
"e1235_q1": fig(
    r"width=6cm, height=4.4cm, xmin=-0.4, xmax=2.7, ymin=-0.5, ymax=5.4, xtick={1,2}, ytick={1,2,3,4}",
    entre("2*x", X2, 0, 2)
    + courbe("2*x", -0.25, 2.6, "courbe2") + courbe(X2, -0.4, 2.3)
    + r"  \guidev{2}{4} \pnt{0}{0} \pnt{2}{4}" + "\n"
    + region(1.0, 1.5, r"$\mathcal{A}$")
    + etiq(1.05, 2.5, r"$y=2x$", "south east", "otGreenDark")
    + etiq(1.65, 2.0, r"$y=x^2$", "north west")),

"e1235_q3": fig(
    r"width=6cm, height=4cm, xmin=-0.15, xmax=2.05, ymin=-0.2, ymax=1.38, xtick={0.7854,1.5708}, xticklabels={$\frac{\pi}{4}$,$\frac{\pi}{2}$}, ytick={0.7071}, yticklabels={$\dfrac{\sqrt2}{2}$}",
    entre("sin(x)", "cos(x)", 0, 1.5708)
    + courbe("cos(x)", 0, 1.75, "courbe2") + courbe("sin(x)", 0, 1.95)
    + r"  \guides{0.7854}{0.7071} \pnt{0.7854}{0.7071}" + "\n"
    + etiq(0.06, 1.1, r"$y=\cos x$", "south west", "otGreenDark")
    + etiq(1.5708, 1.09, r"$y=\sin x$", "south"), trig=True),

"e1235_q4": fig(
    r"width=5.6cm, height=4.4cm, xmin=-1.3, xmax=1.6, ymin=-0.3, ymax=3.4, xtick={-1,1}, ytick={1,2.7183}, yticklabels={$1$,$e$}",
    entre("exp(x)", "1", 0, 1)
    + courbe("1", -1.3, 1.5, "courbe2") + courbe("exp(x)", -1.3, 1.2)
    + r"  \guidev{1}{1} \draw[guide] (axis cs:0,2.7183) -- (axis cs:1,2.7183);" + "\n"
    + borne(1, 2.7183, 1)
    + region(0.62, 1.3, r"$\mathcal{A}$")
    + etiq(0.7, 2.3, r"$y=e^x$", "east")
    + etiq(-1.2, 1.06, r"$y=1$", "south west", "otGreenDark")),

"e1235_q5": fig(
    r"width=5.6cm, height=4.6cm, xmin=-1.45, xmax=1.55, ymin=-1.5, ymax=1.6, xtick={-1,1}, ytick={-1,1}",
    entre("x^3", "x", -1, 1)
    + courbe("x", -1.35, 1.4, "courbe2") + courbe("x^3", -1.1, 1.1)
    + r"  \pnt{-1}{-1} \pnt{0}{0} \pnt{1}{1}" + "\n"
    + etiq(0.95, 1.2, r"$y=x$", "south east", "otGreenDark")
    + etiq(-0.85, -1.25, r"$y=x^3$", "west")),

# ================================================================== 1234 aires sous la courbe
"e1234_q1": fig(
    r"width=5.6cm, height=4.4cm, xmin=-0.5, xmax=3.7, ymin=-0.8, ymax=10.6, xtick={1,2,3}, ytick={3,6,9}",
    sous(X2, 0, 3) + borne(3, 9)
    + courbe(X2, -0.3, 3.25)
    + region(2.3, 2.0, r"$\mathcal{A}$")
    + etiq(2.4, 8.0, r"$y=x^2$", "east")),

"e1234_q2": fig(
    r"width=5.8cm, height=4.4cm, xmin=-1.5, xmax=2.6, ymin=-1.6, ymax=6.0, xtick={-1,-0.5,1,2}, xticklabels={}, ytick={1,3,5}",
    sous("2*x+1", -0.5, 2) + sous("2*x+1", -1, -0.5, O)
    + borne(2, 5) + borne(-1, -1, couleur="otOrange!80!black")
    + courbe("2*x+1", -1.3, 2.45)
    + etiq(1.55, 4.9, r"$y=2x+1$", "east")),

"e1234_q3": fig(
    r"width=6cm, height=3.6cm, xmin=-0.4, xmax=4.8, ymin=-0.35, ymax=2.6, xtick={1,2,3,4}, ytick={1,2}",
    sous("sqrt(x)", 0, 4) + borne(4, 2)
    + courbe("sqrt(x)", 0, 4.6)
    + region(2.5, 0.7, r"$\mathcal{A}$")
    + etiq(2.2, 1.75, r"$y=\sqrt{x}$", "south east")),

"e1234_q4": fig(
    r"width=6cm, height=3.4cm, xmin=-0.3, xmax=3.75, ymin=-0.3, ymax=1.45, xtick={1.5708,3.1416}, xticklabels={$\frac{\pi}{2}$,$\pi$}, ytick={1}",
    sous("sin(x)", 0, 3.1416)
    + courbe("sin(x)", 0, 3.45)
    + region(1.5708, 0.45, r"$\mathcal{A}$")
    + etiq(2.35, 0.95, r"$y=\sin x$", "south west"), trig=True),

"e1234_q5": fig(
    r"width=5.4cm, height=4.4cm, xmin=-1.4, xmax=1.6, ymin=-0.3, ymax=3.4, xtick={-1,1}, ytick={1,2.7183}, yticklabels={$1$,$e$}",
    sous("exp(x)", 0, 1) + borne(1, 2.7183)
    + r"  \draw[guide] (axis cs:0,2.7183) -- (axis cs:1,2.7183);" + "\n"
    + courbe("exp(x)", -1.4, 1.2)
    + region(0.5, 0.65, r"$\mathcal{A}$")
    + etiq(0.7, 2.3, r"$y=e^x$", "east")),

# ================================================================== 1239 applications géométriques
"e1239_q1": fig(
    r"width=5.8cm, height=4.8cm, xmin=-1.5, xmax=2.5, ymin=-1.7, ymax=9.4, xtick={-1,1,2}, xticklabels={}, ytick={2,4,6,8}",
    sous("x^3", 0, 2) + sous("x^3", -1, 0, O)
    + borne(2, 8) + borne(-1, -1, couleur="otOrange!80!black")
    + courbe("x^3", -1.18, 2.09)
    + region(1.55, 1.4, r"$\mathcal{A}_2$")
    + etiq(-0.42, -0.25, r"$\mathcal{A}_1$", "north", "otOrange!80!black")
    + etiq(1.6, 6.0, r"$y=x^3$", "east")),

"e1239_q2": fig(
    r"width=5.8cm, height=4.4cm, xmin=-0.5, xmax=2.9, ymin=-0.7, ymax=5.3, xtick={1,2}, ytick={1,2,3,4}",
    entre("4*x-x^2", X2, 0, 2)
    + courbe("4*x-x^2", -0.15, 2.75, "courbe2") + courbe(X2, -0.45, 2.25)
    + r"  \guidev{2}{4} \pnt{0}{0} \pnt{2}{4}" + "\n"
    + region(1.0, 2.0, r"$\mathcal{A}$")
    + etiq(1.95, 4.5, r"$y=x^2$", "east")
    + etiq(2.3, 3.2, r"$y=4x-x^2$", "north west", "otGreenDark")),

"e1239_q3": fig(
    r"width=7.4cm, height=3.4cm, xmin=-0.3, xmax=6.9, ymin=-1.6, ymax=1.65, xtick={0.7854,3.927,6.2832}, xticklabels={$\frac{\pi}{4}$,$\frac{5\pi}{4}$,$2\pi$}, ytick={-1,1}",
    entre("sin(x)", "cos(x)", 0, 6.2832)
    + courbe("cos(x)", -0.2, 6.6, "courbe2") + courbe("sin(x)", -0.2, 6.6)
    + r"  \guidev{0.7854}{0.7071} \guidev{3.927}{-0.7071} \pnt{0.7854}{0.7071} \pnt{3.927}{-0.7071}" + "\n"
    + region(0.25, 0.6, r"$\mathcal{A}_1$") + region(2.36, 0.35, r"$\mathcal{A}_2$") + region(5.5, -0.3, r"$\mathcal{A}_3$")
    + etiq(1.5708, 1.09, r"$y=\sin x$", "south")
    + etiq(6.2832, 1.09, r"$y=\cos x$", "south", "otGreenDark"), trig=True),

"e1239_q4": fig(
    r"width=5.6cm, height=4.4cm, xmin=-1.2, xmax=1.6, ymin=-0.3, ymax=3.4, xtick={-1,1}, ytick={1,2.7183}, yticklabels={$1$,$e$}",
    entre("exp(x)", "exp(-x)", 0, 1)
    + courbe("exp(-x)", -1.2, 1.5, "courbe2") + courbe("exp(x)", -1.2, 1.2)
    + r"  \draw[guide] (axis cs:0,2.7183) -- (axis cs:1,2.7183); \guidev{1}{0.3679} \pnt{0}{1}" + "\n"
    + borne(1, 2.7183, 0.3679)
    + region(0.75, 1.3, r"$\mathcal{A}$")
    + etiq(0.7, 2.3, r"$y=e^x$", "east")
    + etiq(-1.15, 1.62, r"$y=e^{-x}$", "north west", "otGreenDark")),

"e1239_q5": fig(
    r"width=6.4cm, height=4.8cm, xmin=-2.6, xmax=2.7, ymin=-1.6, ymax=9.8, xtick={-2,2}, ytick={2,4,6,8}",
    entre("2*x^2", "x^4-2*x^2", -2, 2)
    + courbe("2*x^2", -2.15, 2.15, "courbe2") + courbe("x^4-2*x^2", -2.06, 2.06)
    + r"  \guidev{-2}{8} \guidev{2}{8} \pnt{-2}{8} \pnt{0}{0} \pnt{2}{8}" + "\n"
    + etiq(0.12, 7.2, r"$y=2x^2$", "south west", "otGreenDark")
    + etiq(2.12, 4.0, r"$y=x^4-2x^2$", "west")),

# ================================================================== 1236 valeur moyenne (Q1 = cours_moyenne)
"e1236_q2": fig(
    r"width=6cm, height=3.4cm, xmin=-0.3, xmax=3.75, ymin=-0.3, ymax=1.45, xtick={1.5708,3.1416}, xticklabels={$\frac{\pi}{2}$,$\pi$}, ytick={0.6366}, yticklabels={$\dfrac{2}{\pi}$}",
    moyenne(0, 3.1416, 0.6366, "sin(x)")
    + courbe("sin(x)", 0, 3.35)
    + etiq(3.25, 0.6366, r"$\mu=\dfrac{2}{\pi}$", "west", "otGreenDark")
    + etiq(2.35, 0.95, r"$y=\sin x$", "south west"), trig=True),

"e1236_q3": fig(
    r"width=5.4cm, height=4.4cm, xmin=-1.3, xmax=1.9, ymin=-0.3, ymax=3.4, xtick={-1,1}, ytick={1,1.7183}, yticklabels={$1$,$e-1$}",
    moyenne(0, 1, 1.7183, "exp(x)")
    + courbe("exp(x)", -1.3, 1.2)
    + etiq(1.07, 1.7183, r"$\mu=e-1$", "west", "otGreenDark")
    + etiq(0.62, 2.3, r"$y=e^x$", "east")),

"e1236_q4": fig(
    r"width=6cm, height=4.4cm, xmin=-0.4, xmax=4.9, ymin=-0.6, ymax=10.2, xtick={1,2.5,4}, ytick={3,6,9}",
    moyenne(1, 4, 6, "2*x+1")
    + r"  \draw[guide] (axis cs:0,6) -- (axis cs:1,6);" + "\n"
    + courbe("2*x+1", -0.2, 4.5)
    + r"  \pnt[otGreenDark]{2.5}{6}" + "\n"
    + etiq(4.08, 6, r"$\mu=6$", "west", "otGreenDark")
    + etiq(2.2, 7.2, r"$y=2x+1$", "south east")),

"e1236_q5": fig(
    r"width=5.4cm, height=3.6cm, xmin=-0.25, xmax=2.3, ymin=-0.28, ymax=1.38, xtick={1.5708}, xticklabels={$\frac{\pi}{2}$}, ytick={0.6366}, yticklabels={$\dfrac{2}{\pi}$}",
    moyenne(0, 1.5708, 0.6366, "cos(x)")
    + courbe("cos(x)", 0, 1.82)
    + etiq(1.66, 0.6366, r"$\mu=\dfrac{2}{\pi}$", "west", "otGreenDark")
    + etiq(0.55, 0.95, r"$y=\cos x$", "south west"), trig=True),

# ================================================================== 1241 fonctions de signe quelconque (Q3 = cours_sin_signe)
"e1241_q1": fig(
    r"width=5.8cm, height=4.2cm, xmin=-2.5, xmax=1.6, ymin=-1.5, ymax=3.8, xtick={-2,-1,1}, xticklabels={}, ytick={1,2,3}",
    sous("x^2-1", -2, -1) + sous("x^2-1", -1, 1, O)
    + borne(-2, 3)
    + courbe("x^2-1", -2.15, 1.45)
    + region(-1.68, 0.6, r"$\mathcal{A}_1$") + region(0.45, -0.45, r"$\mathcal{A}_2$", "otOrange!80!black")
    + etiq(0.85, 1.55, r"$y=x^2-1$", "south west")),

"e1241_q2": fig(
    r"width=5.8cm, height=4.4cm, xmin=-1.5, xmax=2.5, ymin=-1.0, ymax=7.2, xtick={-1,1,2}, xticklabels={}, ytick={2,4,6}",
    sous("x^3-x", -1, 0) + sous("x^3-x", 0, 1, O) + sous("x^3-x", 1, 2)
    + borne(2, 6)
    + courbe("x^3-x", -1.2, 2.08)
    + etiq(1.75, 4.5, r"$y=x^3-x$", "east")),

"e1241_q4": fig(
    r"width=5.8cm, height=4cm, xmin=-2.7, xmax=2.8, ymin=-4.8, ymax=1.6, xtick={-2,2}, xticklabels={}, ytick=\empty",
    sous("x^2-4", -2, 2, O)
    + courbe("x^2-4", -2.35, 2.35)
    + r"  \pnt{0}{-4}" + "\n"
    + etiq(0.12, -4.1, r"$-4$", "north west", "otMuted")
    + region(-1.0, -1.6, r"$\mathcal{A}$", "otOrange!80!black")
    + etiq(0.5, 0.35, r"$y=x^2-4$", "south west")),

"e1241_q5": fig(
    r"width=5.8cm, height=4.2cm, xmin=-0.5, xmax=3.6, ymin=-1.6, ymax=3.9, xtick={1,3}, xticklabels={}, ytick={1,2,3}",
    sous("x^2-4*x+3", 0, 1) + sous("x^2-4*x+3", 1, 3, O)
    + courbe("x^2-4*x+3", 0, 3.4)
    + region(0.3, 0.8, r"$\mathcal{A}_1$") + region(2.0, -0.5, r"$\mathcal{A}_2$", "otOrange!80!black")
    + etiq(1.6, 1.5, r"$y=x^2-4x+3$", "south west")),

# ================================================================== 1242 type bac
"e1242_q1": fig(
    r"width=5.8cm, height=4cm, xmin=-0.4, xmax=3.6, ymin=-0.5, ymax=4.8, xtick={1,2,3}, ytick={2,3,4}",
    sous("(x-1)^2", 0, 3) + borne(3, 4)
    + courbe("(x-1)^2", -0.15, 3.15)
    + region(2.0, 0.45, r"$\mathcal{A}$")
    + etiq(2.4, 3.3, r"$y=(x-1)^2$", "east")),

"e1242_q4": fig(
    r"width=5.4cm, height=4.4cm, xmin=-0.2, xmax=1.55, ymin=-0.25, ymax=1.45, xtick={0.5,1}, ytick={0.5,1}",
    entre("2*x-x^2", X2, 0, 1)
    + courbe("2*x-x^2", -0.1, 1.5, "courbe2") + courbe(X2, -0.15, 1.18)
    + r"  \pnt{0}{0} \pnt{1}{1}" + "\n"
    + region(0.5, 0.5, r"$\mathcal{A}$")
    + etiq(0.72, 0.42, r"$y=x^2$", "north west")
    + etiq(1.12, 0.62, r"$y=2x-x^2$", "north west", "otGreenDark")),

# 1242 Q2 et Q5 : valeurs moyennes
"e1242_q2": fig(
    r"width=5.6cm, height=4.6cm, xmin=-0.35, xmax=2.9, ymin=-0.6, ymax=7.2, xtick={1,2}, ytick={2,4,6}",
    moyenne(0, 2, 2.1945, "exp(x)-1")
    + courbe("exp(x)-1", -0.3, 2.12)
    + etiq(2.06, 2.1945, r"$\mu=\dfrac{e^2-3}{2}$", "west", "otGreenDark")
    + etiq(1.45, 4.6, r"$y=e^x-1$", "east")),

"e1242_q5": fig(
    r"width=6cm, height=3.8cm, xmin=-0.3, xmax=3.3, ymin=-0.15, ymax=1.3, xtick={1,2}, ytick={0.5,1}, yticklabels={$0{,}5$,$1$}",
    moyenne(0, 2, 0.5493, "1/(x+1)")
    + courbe("1/(x+1)", 0, 3.1)
    + etiq(2.06, 0.5493, r"$\mu=\dfrac{\ln 3}{2}$", "west", "otGreenDark")
    + etiq(0.62, 0.86, r"$y=\dfrac{1}{x+1}$", "south west")),

# ================================================================== cours : encadrement, suite d'intégrales, IPP
"cours_encadre": fig(
    r"width=6cm, height=4.4cm, xmin=-0.15, xmax=1.6, ymin=-0.36, ymax=1.32, xtick={0.5,1}, xticklabels={}, ytick={0.5,1}",
    sous("exp(-x^2)", 0, 1, B)
    + courbe("1", 0, 1.45, "courbe2")
    + courbe("1-x^2", 0, 1.08, "otOrange, line width=1.35pt")
    + courbe("exp(-x^2)", 0, 1.45)
    + etiq(1.45, 1.03, r"$y=1$", "south east", "otGreenDark")
    + etiq(1.2, 0.27, r"$y=e^{-x^2}$", "south west")
    + etiq(1.12, -0.07, r"$y=1-x^2$", "north west", "otOrange!80!black")),

"cours_suite": fig(
    r"width=6.8cm, height=4.6cm, xmin=-0.08, xmax=1.3, ymin=-0.05, ymax=0.66, xtick={0.5,1}, ytick={0.25,0.5}, yticklabels={$0{,}25$,$0{,}5$}",
    sous("x/(1+x)", 0, 1, B) + sous("x^3/(1+x)", 0, 1, V) + sous("x^8/(1+x)", 0, 1, "fill=otGreen!60, draw=none")
    + borne(1, 0.5, couleur="otNavy!60")
    + courbe("x/(1+x)", 0, 1) + courbe("x^3/(1+x)", 0, 1, TIR) + courbe("x^8/(1+x)", 0, 1, POI)
    + legende([(0.04, 0.6, "courbe", r"$n=1$"), (0.04, 0.53, TIR, r"$n=3$"), (0.04, 0.46, POI, r"$n=8$")], 0.09)),

"cours_ipp": fig(
    r"width=7cm, height=3.6cm, xmin=-0.3, xmax=3.55, ymin=-0.3, ymax=1.42, xtick={1,2.7183}, xticklabels={$1$,$e$}, ytick={1}",
    "  \\addplot[fill=otNavy!14, draw=none, domain=0:1, samples=120] ({exp(x)},{x}) -- (axis cs:0,1) -- (axis cs:0,0) -- cycle;\n"
    + sous("ln(x)", 1, 2.7183)
    + r"  \draw[otGreenDark, line width=0.9pt, dash pattern=on 4pt off 2.5pt] (axis cs:0,1) -- (axis cs:2.7183,1) -- (axis cs:2.7183,0);" + "\n"
    + courbe("ln(x)", 0.75, 3.35)
    + region(2.15, 0.27, r"$\mathcal{A}_1$")
    + region(0.75, 0.55, r"$\mathcal{A}_2$", "otNavy")
    + etiq(3.35, 1.22, r"$y=\ln x$", "south east")),

# ================================================================== exercices sans figure jusqu'ici
"e1231_q4": fig(
    r"width=5.8cm, height=5cm, xmin=-1.5, xmax=2.7, ymin=-1.1, ymax=6.8, xtick={-1,1,2}, xticklabels={}, ytick={2,4,6}",
    sous("x^2-3*x+2", -1, 1) + sous("x^2-3*x+2", 1, 2, O)
    + borne(-1, 6)
    + courbe("x^2-3*x+2", -1.15, 2.55)
    + region(0.05, 1.0, r"$\dfrac{14}{3}$")
    + r"  \draw[otOrange!80!black, line width=0.5pt] (axis cs:1.5,-0.17) -- (axis cs:1.5,-0.55);" + "\n"
    + etiq(1.5, -0.55, r"$-\dfrac{1}{6}$", "north", "otOrange!80!black")
    + etiq(0.45, 4.2, r"$y=x^2-3x+2$", "west")),

"e1232_q2": fig(
    r"width=5.8cm, height=4.6cm, xmin=-0.35, xmax=2.6, ymin=-0.5, ymax=4.9, xtick={1,2}, ytick={1,2,3,4}",
    sous(X2, 0, 1) + sous(X2, 1, 2, B)
    + borne(1, 1) + borne(2, 4, couleur="otNavy!60")
    + courbe(X2, -0.3, 2.18)
    + region(0.84, 0.3, r"$\frac{1}{3}$")
    + region(1.62, 1.1, r"$\dfrac{7}{3}$", "otNavy")
    + etiq(1.75, 3.35, r"$y=x^2$", "east")),

"e1233_q3": fig(
    r"width=6.4cm, height=3.4cm, xmin=-0.3, xmax=3.9, ymin=-1.45, ymax=1.45, xtick={1.5708,3.1416}, xticklabels={$\frac{\pi}{2}$,$\pi$}, ytick={-1,1}",
    sous("cos(x)", 0, 1.5708) + sous("cos(x)", 1.5708, 3.1416, O)
    + courbe("cos(x)", 0, 3.6)
    + region(0.6, 0.38, r"$+1$")
    + region(2.55, -0.38, r"$-1$", "otOrange!80!black")
    + etiq(3.25, -0.62, r"$y=\cos x$", "west"), trig=True),

"e1240_q2": fig(
    r"width=6cm, height=5.2cm, xmin=-0.3, xmax=3.6, ymin=-2, ymax=12, xtick={0.4226,1.5774,3}, xticklabels={}, ytick={2,5,10}",
    sous("3*x^2-6*x+2", 0, 0.4226) + sous("3*x^2-6*x+2", 0.4226, 1.5774, O) + sous("3*x^2-6*x+2", 1.5774, 3)
    + borne(3, 11)
    + courbe("3*x^2-6*x+2", 0, 3.12)
    + r"  \pnt{1}{-1}" + "\n"
    + etiq(1.0, -1.15, r"$-1$", "north", "otMuted")
    + region(2.62, 2.6, r"$+$")
    + etiq(2.35, 8.5, r"$v(t)=3t^2-6t+2$", "east")),

"e1240_q4": fig(
    r"width=6cm, height=4.4cm, xmin=-0.8, xmax=14.6, ymin=-8, ymax=112, xtick={5,10}, ytick={20,40,60,80,100}, xlabel={$t$}, ylabel={$T$}",
    moyenne(0, 10, 70.57, "20+80*exp(-0.1*x)")
    + courbe("20+80*exp(-0.1*x)", 0, 13.5)
    + r"  \pnt{0}{100}" + "\n"
    + etiq(10.25, 70.57, r"$\mu\approx70{,}6$", "west", "otGreenDark")
    + etiq(4.2, 96, r"$T(t)=20+80e^{-0{,}1t}$", "west")),

# ================================================================== nouveaux exercices
"en1_suite": fig(
    r"width=6cm, height=4.6cm, xmin=-0.08, xmax=1.3, ymin=-0.15, ymax=3.05, xtick={0.5,1}, ytick={1,2,2.7183}, yticklabels={$1$,$2$,$e$}",
    sous("x*exp(x)", 0, 1, B) + sous("x^3*exp(x)", 0, 1, V) + sous("x^8*exp(x)", 0, 1, "fill=otGreen!60, draw=none")
    + r"  \draw[guide] (axis cs:0,2.7183) -- (axis cs:1,2.7183);" + "\n"
    + borne(1, 2.7183, couleur="otNavy!60")
    + courbe("x*exp(x)", 0, 1) + courbe("x^3*exp(x)", 0, 1, TIR) + courbe("x^8*exp(x)", 0, 1, POI)
    + r"  \pnt{1}{2.7183}" + "\n"
    + legende([(0.04, 2.3, "courbe", r"$n=1$"), (0.04, 1.95, TIR, r"$n=3$"), (0.04, 1.6, POI, r"$n=8$")], 0.09)),

"en2_rect": fig(
    r"width=6cm, height=4.2cm, xmin=-0.08, xmax=1.3, ymin=-0.08, ymax=1.22, xtick={0.25,0.5,0.75,1}, xticklabels={}, ytick={0.5,1}, yticklabels={$0{,}5$,$1$}",
    "".join(
        f"  \\filldraw[fill=otOrange!30, draw=otOrange, line width=0.5pt] (axis cs:{k/4},0) rectangle (axis cs:{(k+1)/4},{1/(1+(k/4)**2):.4f});\n"
        f"  \\filldraw[fill=otGreen!40, draw=otGreenDark, line width=0.5pt] (axis cs:{k/4},0) rectangle (axis cs:{(k+1)/4},{1/(1+((k+1)/4)**2):.4f});\n"
        for k in range(4))
    + courbe("1/(1+x^2)", 0, 1.22)
    + etiq(1.02, 0.6, r"$y=\dfrac{1}{1+x^2}$", "south west")),
}

# Graduations des abscisses placées à la main, du côté libre de la courbe.
XLAB = {
    "cours_sin_signe": [(3.1416, "g", PI), (6.2832, "d", r"2\pi")],
    "e1234_q2": [(-1, "g", "-1"), (-0.5, "d", "-0{,}5"), (1, "c", "1"), (2, "c", "2")],
    "e1234_q4": [(1.5708, "c", P2), (3.1416, "g", PI)],
    "e1235_q3": [(0.7854, "c", P4), (1.5708, "c", P2)],
    "e1239_q1": [(-1, "g", "-1"), (1, "c", "1"), (2, "c", "2")],
    "e1239_q3": [(0.7854, "c", P4), (3.927, "h", r"\frac{5\pi}{4}"), (6.2832, "d", r"2\pi")],
    "e1236_q2": [(1.5708, "c", P2), (3.1416, "g", PI)],
    "e1236_q5": [(1.5708, "g", P2)],
    "e1241_q1": [(-2, "c", "-2"), (-1, "g", "-1"), (1, "d", "1")],
    "e1241_q2": [(-1, "d", "-1"), (1, "d", "1"), (2, "c", "2")],
    "e1241_q4": [(-2, "g", "-2"), (2, "d", "2")],
    "e1241_q5": [(1, "g", "1"), (3, "d", "3")],
    "e1231_q4": [(-1, "c", "-1"), (1, "g", "1"), (2, "d", "2")],
    "cours_encadre": [(0.5, "c", "0{,}5"), (1, "g", "1")],
    "e1233_q3": [(1.5708, "g", P2), (3.1416, "h", PI)],
    "en2_rect": [(0.25, "c", r"\frac{1}{4}"), (0.5, "c", r"\frac{1}{2}"), (0.75, "c", r"\frac{3}{4}"), (1, "c", "1")],
    "e1240_q2": [(0.4226, "g", "t_1"), (1.5774, "d", "t_2"), (3, "c", "3")],
}
