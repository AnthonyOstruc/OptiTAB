# -*- coding: utf-8 -*-
"""Figures de la notion « Fonction exponentielle » (Première spécialité).

Compilation (style des livres OptiTAB, contrôle des chevauchements) :

    python ../../../outils/figures_livre.py <dossier_notion> [nom …] [--planche]

- Courbes : pgfplots (style otWeb), courbe étudiée en bleu marine ; dans les
  corrigés, les éléments de réponse (points, tangentes, solutions) en vert.
- Énoncé / corrigé : même repère, même fenêtre ; la version corrigé ajoute
  les réponses en vert.
- Graduations x placées à la main (XLAB) quand une courbe ou un pointillé
  passe sous l'étiquette par défaut.
"""
import math

FIGURES = {}
XLAB = {}


def axe(opts, corps):
    return ("\\begin{tikzpicture}\n\\begin{axis}[otWeb, " + opts + "]\n"
            + corps + "\n\\end{axis}\n\\end{tikzpicture}")


def pts(liste, couleur="otGreenDark"):
    return " ".join(f"\\pnt[{couleur}]{{{x:.4f}}}{{{y:.4f}}}" for x, y in liste)


E = math.e

# ================================================================== cours
# Méthode d'Euler, pas 0,5, sur [0 ; 2]
euler05 = [(0.5 * k, 1.5 ** k) for k in range(5)]
FIGURES["cours_euler"] = axe(
    r"width=6.4cm, height=5.6cm, xmin=-0.25, xmax=2.25, ymin=-0.4, ymax=7.9,"
    r" xtick={0.5,1,1.5,2}, ytick={1,2,3,4,5,6,7}",
    r"""  \addplot[courbe, domain=0:2] {exp(x)};
  \addplot[otGreenDark, line width=1.1pt, mark=none] coordinates {"""
    + " ".join(f"({x},{y})" for x, y in euler05) + r"""};
  """ + pts(euler05) + r"""
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.45,6.4) {$y=e^x$};
  \node[note,text=otGreenDark,anchor=north west] at (axis cs:1.05,1.75) {Euler, pas $h=0{,}5$};
  \node[note,text=otGreenDark,anchor=west] at (axis cs:2.06,5.06) {$5{,}06$};
  \node[note,text=otNavy,anchor=west] at (axis cs:2.06,7.39) {$e^2\approx 7{,}39$};""")

# Courbe de exp et tangente en 0
FIGURES["cours_courbe"] = axe(
    r"width=7cm, height=6cm, xmin=-3.2, xmax=2.3, ymin=-1.9, ymax=7.6,"
    r" xtick={-3,-2,-1,1,2}, ytick={1,4,5,6,7}",
    r"""  \addplot[courbe, domain=-3.2:1.98] {exp(x)};
  \addplot[otGreenDark, line width=1.1pt, domain=-2.85:2.2] {x+1};
  \guides{1}{2.71828}
  \pnt{0}{1} \pnt{1}{2.71828}
  \node[etiq,text=otMuted,anchor=east] at (axis cs:-0.06,2.71828) {$e$};
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.5,6.3) {$y=e^x$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:0.92,2.85) {$(1\,;e)$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:0.1,0.85) {$(0\,;1)$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:1.35,1.65) {$y=x+1$};""")

# t -> e^{kt} et e^{-kt}
FIGURES["cours_ekt"] = axe(
    r"width=6cm, height=5cm, xmin=-2.75, xmax=2.75, ymin=-0.35, ymax=5.4,"
    r" xlabel={$t$}, xtick={-2,-1,1,2}, ytick={1,2,3,4,5}",
    r"""  \addplot[courbe, domain=-2.6:1.65] {exp(x)};
  \addplot[courbe2, domain=-2.6:2.6] {exp(0.5*x)};
  \addplot[otNavy, line width=1.35pt, dash pattern=on 5pt off 2.5pt, domain=-1.65:2.6] {exp(-x)};
  \addplot[otGreen, line width=1.35pt, dash pattern=on 5pt off 2.5pt, domain=-2.6:2.6] {exp(-0.5*x)};
  \pnt{0}{1}
  \node[etiq,text=otNavy,anchor=south] at (axis cs:1.65,5.25) {$e^{t}$};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:-1.65,5.25) {$e^{-t}$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:2.65,3.67) {$e^{0{,}5t}$};
  \node[etiq,text=otGreenDark,anchor=east] at (axis cs:-2.65,3.67) {$e^{-0{,}5t}$};""")

# Étude de (2x - 1)e^x sur [-2 ; 1]
FIGURES["cours_etude"] = axe(
    r"width=6.6cm, height=5cm, xmin=-2.3, xmax=1.35, ymin=-2.0, ymax=3.1,"
    r" xtick={-2,-1,-0.5,0.5,1}, xticklabels={}, ytick={-1,1,2}",
    r"""  \addplot[courbe, domain=-2:1] {(2*x-1)*exp(x)};
  \guides{-0.5}{-1.21306}
  \pnt{-0.5}{-1.21306} \pnt{-2}{-0.67668} \pnt{1}{2.71828}
  \node[note,anchor=north] at (axis cs:-0.95,-1.36) {minimum $\approx-1{,}21$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:-2.1,2.3) {$y=(2x-1)e^x$};""")
XLAB["cours_etude"] = [(-2, "c", "-2"), (-1, "c", "-1"), (-0.5, "h", r"-0{,}5"),
                       (0.5, "d", "0{,}5"), (1, "c", "1")]

# Décroissance radioactive m(t) = 100 e^{-0,1 t}
mod = [(n, 100 * math.exp(-0.1 * n)) for n in range(0, 21)]
FIGURES["cours_modele"] = axe(
    r"width=7.4cm, height=4.6cm, xmin=-0.8, xmax=21.5, ymin=-6, ymax=112,"
    r" xlabel={$t$}, ylabel={$m$}, xtick={5,7,10,15,20}, ytick={25,50,75,100}",
    r"""  \addplot[courbe, domain=0:20.5] {100*exp(-0.1*x)};
  \draw[seuil] (axis cs:0,50) -- (axis cs:20.5,50);
  \guidev{7}{49.66}
  """ + pts(mod) + r"""
  \fill[otGreenDark] (axis cs:7,49.66) circle (3pt);
  \node[etiq,text=otNavy,anchor=west] at (axis cs:8.5,96) {$m(t)=100\,e^{-0{,}1t}$};
  \node[note,text=otOrange!80!black,anchor=south west] at (axis cs:14.5,52) {seuil $50$ g};""")

# ================================================================== exercices
# --- 1290 : courbe de exp et tangente en 0
base1290 = (r"width=6.6cm, height=5.6cm, xmin=-3.2, xmax=2.3, ymin=-1.9, ymax=7.6,"
            r" xtick={-3,-2,-1,1,2}, ytick={1,2,3,4,5,6,7}")
FIGURES["ex1290_enonce"] = axe(base1290, r"""  \addplot[courbe, domain=-3.2:1.98] {exp(x)};
  \addplot[otOrange, line width=1.1pt, domain=-2.85:2.2] {x+1};
  \pnt{0}{1}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.5,6.3) {$\mathcal{C}$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:0.08,0.9) {$A$};
  \node[etiq,text=otOrange!85!black,anchor=north west] at (axis cs:1.45,1.85) {$T$};""")
FIGURES["ex1290"] = axe(base1290, r"""  \addplot[courbe, domain=-3.2:1.98] {exp(x)};
  \addplot[otGreenDark, line width=1.1pt, domain=-2.85:2.2] {x+1};
  \draw[otGreenDark, line width=0.8pt, dash pattern=on 3pt off 2pt] (axis cs:0,1) -- (axis cs:1,1) -- (axis cs:1,2);
  \pnt[otGreenDark]{0}{1}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.5,6.3) {$\mathcal{C}$};
  \node[note,text=otGreenDark,anchor=north] at (axis cs:0.5,0.92) {$+1$};
  \node[note,text=otGreenDark,anchor=west] at (axis cs:1.06,1.5) {$+1$};
  \node[etiq,text=otGreenDark,anchor=east] at (axis cs:-0.1,1.45) {$A(0\,;1)$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:1.55,2.05) {$T : y=x+1$};""")

# --- 1293 : e^x = -3 n'a pas de solution
FIGURES["ex1293"] = axe(
    r"width=6.6cm, height=5cm, xmin=-3.2, xmax=2.3, ymin=-4.0, ymax=7.6,"
    r" xtick={-3,-2,-1,1,2}, ytick={-3,2,4,6}",
    r"""  \addplot[courbe, domain=-3.2:1.98] {exp(x)};
  \draw[seuil] (axis cs:-3.2,-3) -- (axis cs:2.2,-3);
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.5,6.3) {$y=e^x$};
  \node[etiq,text=otOrange!80!black,anchor=south east] at (axis cs:2.2,-2.9) {$y=-3$};
  \node[note,text=otGreenDark,anchor=north west] at (axis cs:-2.9,-1.0) {aucun point commun};""")

# --- 1298 : f(x) = e^x - x
base1298 = (r"width=6.4cm, height=5cm, xmin=-2.3, xmax=2.3, ymin=-0.5, ymax=5.9,"
            r" xtick={-2,-1,1,2}, ytick={1,2,3,4,5}")
f1298 = r"\addplot[courbe, domain=-2:2] {exp(x)-x};"
FIGURES["ex1298_enonce"] = axe(base1298, "  " + f1298 + r"""
  \node[etiq,text=otNavy,anchor=west] at (axis cs:0.75,4.6) {$\mathcal{C}_f$};""")
FIGURES["ex1298"] = axe(base1298, "  " + f1298 + r"""
  \pnt[otGreenDark]{0}{1}
  \node[etiq,text=otNavy,anchor=west] at (axis cs:0.75,4.6) {$\mathcal{C}_f$};
  \node[note,text=otGreenDark,anchor=north west] at (axis cs:0.1,0.85) {minimum $f(0)=1$};""")
FIGURES["ex1298_tangente"] = axe(
    r"width=6.4cm, height=5cm, xmin=-2.7, xmax=2.3, ymin=-1.9, ymax=6.4,"
    r" xtick={-2,-1,1,2}, ytick={2,4,6}",
    r"""  \addplot[name path=C, courbe, domain=-2.5:1.85] {exp(x)};
  \addplot[name path=T, otGreenDark, line width=1.1pt, domain=-2.5:1.85] {x+1};
  \addplot[otGreen!22] fill between[of=C and T];
  \pnt{0}{1}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.4,5.6) {$y=e^x$};
  \node[etiq,text=otGreenDark,anchor=north west] at (axis cs:1.15,1.4) {$y=x+1$};
  \node[note,text=otGreenDark,anchor=west] at (axis cs:-2.6,3.6) {$e^x\geqslant x+1$};""")

# --- 1294 : g(x) = x e^x
base1294 = (r"width=7cm, height=4.8cm, xmin=-4.7, xmax=1.45, ymin=-1.15, ymax=4.2,"
            r" xtick={-4,-3,-2,-1,1}, xticklabels={}, ytick={1,2,3,4}")
g1294 = r"\addplot[courbe, domain=-4.6:1.2] {x*exp(x)};"
FIGURES["ex1294_enonce"] = axe(base1294, "  " + g1294 + r"""
  \node[etiq,text=otNavy,anchor=east] at (axis cs:0.8,3.4) {$\mathcal{C}_g$};""")
FIGURES["ex1294"] = axe(base1294, "  " + g1294 + r"""
  \addplot[otGreenDark, line width=1.1pt, domain=-0.9:1.35] {x};
  \guides{-1}{-0.36788}
  \pnt[otGreenDark]{-1}{-0.36788} \pnt[otGreenDark]{0}{0}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:0.8,3.4) {$\mathcal{C}_g$};
  \node[note,text=otGreenDark,anchor=north east] at (axis cs:-1.1,-0.5) {minimum $-\tfrac{1}{e}\approx-0{,}368$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:1.38,1.25) {$T : y=x$};""")
XLAB["ex1294"] = [(-4, "h", "-4"), (-3, "h", "-3"), (-2, "h", "-2"), (-1, "h", "-1"), (1, "c", "1")]
XLAB["ex1294_enonce"] = XLAB["ex1294"]

# --- 1297 : y = x^2 - 4x + 3 >= 0
FIGURES["ex1297"] = axe(
    r"width=6.4cm, height=4.8cm, xmin=-0.7, xmax=4.8, ymin=-1.6, ymax=4.6,"
    r" xtick={1,2,3,4}, xticklabels={}, ytick={-1,1,2}",
    r"""  \addplot[courbe, domain=-0.35:4.35] {x^2-4*x+3};
  \sol{-0.6}{1} \sol{3}{4.7}
  \borneF{1} \borneF{3}
  \node[etiq,text=otNavy,anchor=south] at (axis cs:2,3.9) {$y=x^2-4x+3$};
  \node[note,text=otGreenDark,anchor=south] at (axis cs:2,1.6) {$\geqslant 0$ hors de $]1\,;3[$};""")
XLAB["ex1297"] = [(1, "g", "1"), (2, "c", "2"), (3, "d", "3"), (4, "c", "4")]

# --- 1299 : u_n = e^{-0,5 n}
base1299 = (r"width=7.4cm, height=4cm, xmin=-0.4, xmax=9.8, ymin=-0.08, ymax=1.3,"
            r" xlabel={$t$}, xtick={1,2,3,4,5,6,7,8,9}, ytick={0.5,1}")
c1299 = r"\addplot[courbe, domain=0:9.5] {exp(-0.5*x)};"
FIGURES["ex1299_enonce"] = axe(base1299, "  " + c1299 + r"""
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:3.2,0.5) {$y=e^{-0{,}5t}$};""")
u1299 = [(n, math.exp(-0.5 * n)) for n in range(10)]
FIGURES["ex1299"] = axe(base1299, "  " + c1299 + r"""
  """ + pts(u1299) + r"""
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:3.2,0.5) {$y=e^{-0{,}5t}$};
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:0.12,1.03) {$u_0=1$};
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:1.1,0.64) {$u_1\approx0{,}607$};
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:2.1,0.39) {$u_2\approx0{,}368$};""")

# --- 1292 : f(x) = (x^2 - 3) e^x sur [-5 ; 2]
base1292 = (r"width=7cm, height=6cm, xmin=-5.4, xmax=2.5, ymin=-6.7, ymax=7.9,"
            r" xtick={-5,-4,-3,1,2}, xticklabels={}, ytick={-4,2,4,6}")
f1292 = r"\addplot[courbe, domain=-5:2] {(x^2-3)*exp(x)};"
FIGURES["ex1292_enonce"] = axe(base1292.replace("xtick={-5,-4,-3,1,2}", "xtick={-5,-4,-3,-2,-1,1,2}"), "  " + f1292 + r"""
  \pnt{-5}{0.14823} \pnt{2}{7.38906}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.4,5.4) {$\mathcal{C}_f$};""")
XLAB["ex1292_enonce"] = [(-5, "c", "-5"), (-4, "c", "-4"), (-3, "c", "-3"), (-2, "c", "-2"),
                         (-1, "h", "-1"), (1, "h", "1"), (2, "c", "2")]
FIGURES["ex1292"] = axe(base1292, "  " + f1292 + r"""
  \addplot[otGreenDark, line width=1.1pt, domain=-2.2:0.6] {-3*x-3};
  \guides{1}{-5.43656}
  \pnt{-5}{0.14823} \pnt{2}{7.38906}
  \pnt[otGreenDark]{-3}{0.29872} \pnt[otGreenDark]{1}{-5.43656}
  \pnt[otGreenDark]{-1.73205}{0} \pnt[otGreenDark]{1.73205}{0} \pnt[otGreenDark]{0}{-3}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.4,5.4) {$\mathcal{C}_f$};
  \node[note,text=otGreenDark,anchor=south] at (axis cs:-3,0.75) {max. local $6e^{-3}$};
  \node[note,text=otGreenDark,anchor=north] at (axis cs:1,-5.65) {min. $-2e$};
  \node[etiq,text=otGreenDark,anchor=east] at (axis cs:-2.3,3.6) {$T$};""")
XLAB["ex1292"] = [(-5, "c", "-5"), (-4, "c", "-4"), (-3, "c", "-3"),
                  (-1.73205, "g", r"-\sqrt{3}"), (1, "h", "1"), (1.73205, "d", r"\sqrt{3}")]

# --- 1301 : méthode d'Euler sur [0 ; 1]
base1301 = (r"width=6.4cm, height=5.4cm, xmin=-0.08, xmax=1.12, ymin=-0.15, ymax=3.15,"
            r" xtick={0.25,0.5,0.75,1}, ytick={0.5,1,1.5,2,2.5,3}")
c1301 = r"\addplot[courbe, domain=0:1.07] {exp(x)};"
FIGURES["ex1301_enonce"] = axe(base1301, "  " + c1301 + r"""
  \node[etiq,text=otNavy,anchor=east] at (axis cs:0.86,2.75) {$y=e^x$};""")
e05 = [(0.5 * k, 1.5 ** k) for k in range(3)]
e025 = [(0.25 * k, 1.25 ** k) for k in range(5)]
FIGURES["ex1301"] = axe(base1301, "  " + c1301 + r"""
  \addplot[otOrange, line width=1.1pt] coordinates {""" + " ".join(f"({x},{y})" for x, y in e05) + r"""};
  \addplot[otGreenDark, line width=1.1pt] coordinates {""" + " ".join(f"({x},{y})" for x, y in e025) + r"""};
  """ + pts(e05, "otOrange") + " " + pts(e025) + r"""
  \node[etiq,text=otNavy,anchor=east] at (axis cs:0.86,2.75) {$y=e^x$};
  \node[note,text=otGreenDark,anchor=west] at (axis cs:1.03,2.49) {$h=0{,}25$};
  \node[note,text=otOrange!80!black,anchor=west] at (axis cs:1.03,2.2) {$h=0{,}5$};""")

# --- 1295 : quatre courbes e^{kt}
base1295 = (r"width=5.6cm, height=5cm, xmin=-2.75, xmax=2.75, ymin=-0.35, ymax=5.4,"
            r" xlabel={$t$}, xtick={-2,-1,1,2}, ytick={1,2,3,4,5}")
c1295 = r"""  \addplot[courbe, domain=-2.6:2.6] {exp(-0.5*x)};
  \addplot[courbe, domain=-2.6:1.65] {exp(x)};
  \addplot[courbe, domain=-1.65:2.6] {exp(-x)};
  \addplot[courbe, domain=-2.6:2.6] {exp(0.5*x)};
  \pnt{0}{1}"""
FIGURES["ex1295_enonce"] = axe(base1295, c1295 + r"""
  \node[etiq,text=otNavy,anchor=east] at (axis cs:-2.65,3.67) {$\mathcal{C}_1$};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:1.65,5.25) {$\mathcal{C}_2$};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:-1.65,5.25) {$\mathcal{C}_3$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:2.65,3.67) {$\mathcal{C}_4$};""")
FIGURES["ex1295"] = axe(base1295, c1295 + r"""
  \node[etiq,anchor=east] at (axis cs:-2.65,3.67) {$\textcolor{otNavy}{\mathcal{C}_1}\,\textcolor{otGreenDark}{: e^{-0{,}5t}}$};
  \node[etiq,anchor=south] at (axis cs:1.65,5.25) {$\textcolor{otNavy}{\mathcal{C}_2}\,\textcolor{otGreenDark}{: e^{t}}$};
  \node[etiq,anchor=south] at (axis cs:-1.65,5.25) {$\textcolor{otNavy}{\mathcal{C}_3}\,\textcolor{otGreenDark}{: e^{-t}}$};
  \node[etiq,anchor=west] at (axis cs:2.65,3.67) {$\textcolor{otNavy}{\mathcal{C}_4}\,\textcolor{otGreenDark}{: e^{0{,}5t}}$};""")

# --- 1300 : N(t) = 1000 e^{0,02 t}
base1300 = (r"width=7cm, height=4.8cm, xmin=-4, xmax=126, ymin=-500, ymax=12000,"
            r" xlabel={$t$}, ylabel={$N$}, scaled ticks=false,"
            r" xtick={20,35,50,80,100,120}, ytick={2000,4000,6000,8000,10000}")
c1300 = r"\addplot[courbe, domain=0:120] {1000*exp(0.02*x)};"
FIGURES["ex1300_enonce"] = axe(base1300.replace("xtick={20,35,50,80,100,120}", "xtick={20,40,60,80,100,120}"),
                               "  " + c1300 + r"""
  \node[etiq,text=otNavy,anchor=west] at (axis cs:6,9800) {$N(t)=1\,000\,e^{0{,}02t}$};""")
FIGURES["ex1300"] = axe(base1300, "  " + c1300 + r"""
  \draw[seuil] (axis cs:0,2000) -- (axis cs:120,2000);
  \guidev{35}{2013.75}
  \guides{50}{2718.28}
  \pnt[otGreenDark]{35}{2013.75} \pnt[otGreenDark]{50}{2718.28}
  \node[etiq,text=otNavy,anchor=west] at (axis cs:6,9800) {$N(t)=1\,000\,e^{0{,}02t}$};
  \node[note,text=otGreenDark,anchor=south east] at (axis cs:48,3000) {$N(50)\approx 2\,718$};
  \node[note,text=otOrange!80!black,anchor=north west] at (axis cs:58,1850) {doublement : $2\,000$};""")

# --- 1296 : C(t) = 4 t e^{-0,5 t}
base1296 = (r"width=7cm, height=4.4cm, xmin=-0.4, xmax=10.6, ymin=-0.2, ymax=3.6,"
            r" xlabel={$t$}, ylabel={$C$}, xtick={2,6,8,10}, ytick={1,2,3}")
# (le corrigé ajoute t1 et t2 : graduations à la main, voir XLAB)
c1296 = r"""\addplot[courbe, domain=0:10] {4*x*exp(-0.5*x)};
  \draw[seuil] (axis cs:0,2) -- (axis cs:10.3,2);"""
FIGURES["ex1296_enonce"] = axe(base1296.replace("xtick={2,6,8,10}", "xtick={2,4,6,8,10}"), "  " + c1296 + r"""
  \node[etiq,text=otNavy,anchor=west] at (axis cs:5.2,2.75) {$C(t)=4t\,e^{-0{,}5t}$};
  \node[note,text=otOrange!80!black,anchor=south east] at (axis cs:10.3,2.05) {seuil d'efficacité};""")
FIGURES["ex1296"] = axe(base1296.replace("xtick={2,6,8,10}", "xtick={0.7148,2,4.3066,6,8,10}, xticklabels={}"), "  " + c1296 + r"""
  \sol{0.7148}{4.3066}
  \draw[otGreenDark, line width=0.7pt, dash pattern=on 2pt off 1.6pt] (axis cs:0.7148,0) -- (axis cs:0.7148,2) (axis cs:4.3066,0) -- (axis cs:4.3066,2);
  \guidev{2}{2.94304}
  \pnt[otGreenDark]{2}{2.94304} \pnt[otGreenDark]{0.7148}{2} \pnt[otGreenDark]{4.3066}{2}
  \node[note,text=otGreenDark,anchor=south] at (axis cs:2,3.02) {max. $\tfrac{8}{e}\approx2{,}94$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:5.2,2.75) {$C(t)=4t\,e^{-0{,}5t}$};
  \node[note,text=otGreenDark,anchor=north west] at (axis cs:4.9,1.25) {efficace pendant $\approx 3{,}6$ h};""")
XLAB["ex1296"] = [(0.7148, "c", "t_1"), (2, "c", "2"), (4.3066, "c", "t_2"), (6, "c", "6"), (8, "c", "8"), (10, "c", "10")]

# --- nouveau-1 : A(t) = 5000 e^{-0,2 t}
basen1 = (r"width=7cm, height=4.6cm, xmin=-0.6, xmax=15.8, ymin=-250, ymax=5700,"
          r" xlabel={$t$}, ylabel={$A$}, scaled ticks=false,"
          r" xtick={2,4,6,8,10,12,14}, ytick={1000,2000,2500,3000,4000,5000}")
cn1 = r"\addplot[courbe, domain=0:15] {5000*exp(-0.2*x)};"
FIGURES["n1_enonce"] = axe(basen1.replace("ytick={1000,2000,2500,3000,4000,5000}", "ytick={1000,2000,3000,4000,5000}"),
                           "  " + cn1 + r"""
  \node[etiq,text=otNavy,anchor=west] at (axis cs:5,4300) {$A(t)=5\,000\,e^{-0{,}2t}$};""")
an1 = [(n, 5000 * math.exp(-0.2 * n)) for n in range(16)]
FIGURES["n1_corrige"] = axe(basen1.replace("ytick={1000,2000,2500,3000,4000,5000}", "ytick={1000,2500,4000,5000}"),
                            "  " + cn1 + r"""
  \draw[seuil] (axis cs:0,2500) -- (axis cs:15,2500);
  \guidev{4}{2246.64}
  """ + pts(an1) + r"""
  \fill[otGreenDark] (axis cs:4,2246.64) circle (3pt);
  \node[etiq,text=otNavy,anchor=west] at (axis cs:5,4300) {$A(t)=5\,000\,e^{-0{,}2t}$};
  \node[note,text=otGreenDark,anchor=south west] at (axis cs:6.5,2750) {$A(4)\approx 2\,247\leqslant 2\,500$};""")
