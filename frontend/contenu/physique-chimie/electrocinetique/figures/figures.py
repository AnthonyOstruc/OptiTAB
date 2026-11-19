# -*- coding: utf-8 -*-
"""Figures du formulaire « Électrocinétique » (prépa, école d'ingénieur).

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/physique-chimie/electrocinetique --planche

Conventions françaises : source idéale de tension = cercle traversé par un trait
dans le sens du fil ; source idéale de courant = cercle barré d'un trait
perpendiculaire au fil. Flèches de tension vertes, courants orange.
"""

NOTE = r"\otMedium\fontsize{10.5}{12}\selectfont"
FIL = "otInk,line width=0.9pt"
RS = 0.3  # rayon des sources


def legende(x, y, texte):
    return rf"  \node[anchor=north,align=center,font={NOTE},text=otMuted] at ({x},{y}) {{{texte}}};" + "\n"


def fil(*points):
    return rf"  \draw[{FIL}] " + " -- ".join(f"({x},{y})" for x, y in points) + ";\n"


def borne(x, y):
    return rf"  \draw[{FIL},fill=white] ({x},{y}) circle (2.2pt);" + "\n"


def point(x, y):
    return rf"  \fill[otInk] ({x},{y}) circle (2pt);" + "\n"


def r_v(x, y, nom, cote="east"):
    """Résistance verticale centrée en (x, y) et son nom à gauche (east) ou à droite (west)."""
    dx = -0.22 if cote == "east" else 0.22
    return (rf"  \draw[{FIL},fill=white] ({x - 0.14},{y - 0.4}) rectangle ({x + 0.14},{y + 0.4});" + "\n"
            + rf"  \node[anchor={cote},text=otInk,font=\large] at ({x + dx},{y}) {{${nom}$}};" + "\n")


def r_h(x, y, nom):
    return (rf"  \draw[{FIL},fill=white] ({x - 0.4},{y - 0.14}) rectangle ({x + 0.4},{y + 0.14});" + "\n"
            + rf"  \node[anchor=south,text=otInk,font=\large] at ({x},{y + 0.2}) {{${nom}$}};" + "\n")


def courant(x, y, sens, nom, cote):
    dx, dy = {"droite": (0.18, 0), "gauche": (-0.18, 0), "bas": (0, -0.18), "haut": (0, 0.18)}[sens]
    ancre, ex, ey = {"above": ("south", 0, 0.14), "below": ("north", 0, -0.14),
                     "right": ("west", 0.16, 0), "left": ("east", -0.16, 0)}[cote]
    return (rf"  \draw[otOrange!85!black,line width=1.1pt,-{{Stealth[length=2.4mm]}}] ({x - dx},{y - dy}) -- ({x + dx},{y + dy});" + "\n"
            + rf"  \node[anchor={ancre},text=otOrange!75!black,font=\large] at ({x + ex},{y + ey}) {{${nom}$}};" + "\n")


def tension(x, y1, y2, nom, ancre):
    """Flèche de tension verticale de y1 vers y2 (pointe vers le potentiel le plus haut)."""
    return (rf"  \draw[otGreenDark,line width=1pt,-{{Stealth[length=2.4mm]}}] ({x},{y1}) -- ({x},{y2});" + "\n"
            + rf"  \node[anchor={ancre},text=otGreenDark,font=\large,inner sep=2pt] at ({x},{(y1 + y2) / 2}) {{${nom}$}};" + "\n")


# ---------------------------------------------------------------- 1. ponts diviseurs
def diviseur_tension():
    s = fil((0, 2.4), (1.4, 2.4), (1.4, 2.2)) + fil((1.4, 1.4), (1.4, 1.0)) + fil((1.4, 0.2), (1.4, 0), (0, 0))
    s += fil((1.4, 1.2), (2.7, 1.2)) + fil((1.4, 0), (2.7, 0))
    s += point(1.4, 1.2) + point(1.4, 0)
    s += borne(0, 2.4) + borne(0, 0) + borne(2.7, 1.2) + borne(2.7, 0)
    s += r_v(1.4, 1.8, "R_1", "west") + r_v(1.4, 0.6, "R_2", "west")
    s += tension(-0.3, 0.12, 2.28, "u", "east")
    s += tension(3.0, 0.12, 1.08, "u_2", "west")
    s += courant(0.7, 2.4, "droite", "i", "above")
    s += legende(1.35, -0.32, "Diviseur de tension")
    return s


def diviseur_courant(x0):
    s = fil((x0, 2.2), (x0 + 2.8, 2.2), (x0 + 2.8, 1.6)) + fil((x0 + 2.8, 0.8), (x0 + 2.8, 0.2), (x0, 0.2))
    s += fil((x0 + 1.4, 2.2), (x0 + 1.4, 1.6)) + fil((x0 + 1.4, 0.8), (x0 + 1.4, 0.2))
    s += point(x0 + 1.4, 2.2) + point(x0 + 1.4, 0.2)
    s += borne(x0, 2.2) + borne(x0, 0.2)
    s += r_v(x0 + 1.4, 1.2, "R_1", "east") + r_v(x0 + 2.8, 1.2, "R_2", "east")
    s += courant(x0 + 0.65, 2.2, "droite", "i", "above")
    s += courant(x0 + 1.4, 1.9, "bas", "i_1", "right")
    s += courant(x0 + 2.8, 1.9, "bas", "i_2", "right")
    s += legende(x0 + 1.4, -0.32, "Diviseur de courant")
    return s


PONTS = "\n\\begin{tikzpicture}\n" + diviseur_tension() + diviseur_courant(4.6) + "\\end{tikzpicture}"


# ---------------------------------------------------------------- 2. Thévenin et Norton
def source_tension(x, y):
    return (rf"  \draw[{FIL},fill=white] ({x},{y}) circle ({RS});" + "\n"
            + rf"  \draw[{FIL}] ({x},{y - RS}) -- ({x},{y + RS});" + "\n")


def source_courant(x, y):
    return (rf"  \draw[{FIL},fill=white] ({x},{y}) circle ({RS});" + "\n"
            + rf"  \draw[{FIL}] ({x - RS},{y}) -- ({x + RS},{y});" + "\n")


def thevenin():
    s = fil((0, 1.2 + RS), (0, 2.4), (0.8, 2.4)) + fil((1.6, 2.4), (2.6, 2.4)) + fil((0, 1.2 - RS), (0, 0), (2.6, 0))
    s += source_tension(0, 1.2) + r_h(1.2, 2.4, r"R_{\mathrm{th}}")
    s += borne(2.6, 2.4) + borne(2.6, 0)
    s += tension(-0.55, 0.85, 1.55, r"E_{\mathrm{th}}", "east")
    s += tension(2.95, 0.15, 2.25, "u", "west")
    s += courant(2.05, 2.4, "droite", "i", "below")
    s += rf"  \node[anchor=south,text=otInk,font=\large] at (2.6,2.5) {{$\mathrm{{A}}$}};" + "\n"
    s += rf"  \node[anchor=north,text=otInk,font=\large] at (2.6,-0.1) {{$\mathrm{{B}}$}};" + "\n"
    s += legende(1.3, -0.62, "Modèle de Thévenin")
    return s


def norton(x0):
    s = fil((x0, 1.2 + RS), (x0, 2.4), (x0 + 2.8, 2.4)) + fil((x0, 1.2 - RS), (x0, 0), (x0 + 2.8, 0))
    s += fil((x0 + 1.3, 2.4), (x0 + 1.3, 1.6)) + fil((x0 + 1.3, 0.8), (x0 + 1.3, 0))
    s += point(x0 + 1.3, 2.4) + point(x0 + 1.3, 0)
    s += source_courant(x0, 1.2) + r_v(x0 + 1.3, 1.2, r"R_{\mathrm{N}}", "west")
    s += borne(x0 + 2.8, 2.4) + borne(x0 + 2.8, 0)
    s += rf"  \draw[otOrange!85!black,line width=1.1pt,-{{Stealth[length=2.4mm]}}] ({x0 - 0.55},0.85) -- ({x0 - 0.55},1.55);" + "\n"
    s += rf"  \node[anchor=east,text=otOrange!75!black,font=\large] at ({x0 - 0.6},1.2) {{$I_{{\mathrm{{N}}}}$}};" + "\n"
    s += tension(x0 + 3.15, 0.15, 2.25, "u", "west")
    s += courant(x0 + 2.2, 2.4, "droite", "i", "below")
    s += rf"  \node[anchor=south,text=otInk,font=\large] at ({x0 + 2.8},2.5) {{$\mathrm{{A}}$}};" + "\n"
    s += rf"  \node[anchor=north,text=otInk,font=\large] at ({x0 + 2.8},-0.1) {{$\mathrm{{B}}$}};" + "\n"
    s += legende(x0 + 1.4, -0.62, "Modèle de Norton")
    return s


THEVENIN_NORTON = "\n\\begin{tikzpicture}\n" + thevenin() + norton(5.0) + "\\end{tikzpicture}"


# ---------------------------------------------------------------- 3. réponse du RLC série à un échelon
# u_C / E en fonction de ω0 t, pour Q = 5, Q = 1/2 et Q = 0,2.
RLC_REGIMES = r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8.6cm, height=3.6cm, xmin=0, xmax=15, ymin=0, ymax=1.9,
  xlabel={$\omega_0 t$}, ylabel={$u_C/E$}, grid=none, xtick={5,10}, ytick={1},
  legend style={at={(0.5,-0.3)}, anchor=north, legend columns=3, draw=none, fill=none,
    font=\otRegular\fontsize{9.5}{11}\selectfont, column sep=8pt},
  legend cell align=left]
  \draw[asymptote] (axis cs:0,1) -- (axis cs:15,1);
  \addplot[courbe, domain=0:14.8, samples=300] {1 - exp(-0.1*x)*(cos(0.99499*x) + 0.1005*sin(0.99499*x))};
  \addlegendentry{$Q = 5$}
  \addplot[courbe2, domain=0:14.8] {1 - (1 + x)*exp(-x)};
  \addlegendentry{$Q = 1/2$}
  \addplot[otOrange!90!black, line width=1.35pt, domain=0:14.8] {1 + (-4.79129*exp(-0.20871*x) + 0.20871*exp(-4.79129*x))/4.58258};
  \addlegendentry{$Q = 0{,}2$}
\end{axis}
\end{tikzpicture}"""


# ---------------------------------------------------------------- 4. Bode : passe-bas du premier ordre
BODE = r"""
\begin{tikzpicture}
\begin{semilogxaxis}[otWeb, width=8.4cm, height=3.8cm, xmin=0.01, xmax=100, ymin=-42, ymax=6,
  axis x line=bottom, axis y line=left, xlabel={$\omega/\omega_c$}, ylabel={$G_{\mathrm{dB}}$}, grid=none,
  every axis x label/.style={at={(current axis.south east)},anchor=west,font=\normalsize,text=otMuted},
  every axis y label/.style={at={(current axis.north west)},anchor=south,font=\normalsize,text=otMuted},
  xtick={0.01,0.1,1,10,100}, xticklabels={$0{,}01$,$0{,}1$,$1$,$10$,$100$},
  ytick={-40,-20,0}, yticklabels={$-40$,$-20$,$0$}]
  \addplot[seuil, domain=0.01:1] {0};
  \addplot[seuil, domain=1:100] {-20*log10(x)};
  \addplot[courbe, domain=0.01:100, samples=200] {-10*log10(1 + x^2)};
  \pnt{1}{-3.01}
  \node[etiq,text=otNavy,anchor=north east] at (axis cs:0.9,-3.6) {$-3$ dB};
  \node[etiq,text=otOrange!80!black,anchor=south west] at (axis cs:12,-17) {$-20$ dB/décade};
\end{semilogxaxis}
\end{tikzpicture}"""


FIGURES = {
    "ponts_diviseurs": PONTS,
    "thevenin_norton": THEVENIN_NORTON,
    "rlc_regimes": RLC_REGIMES,
    "bode_passe_bas": BODE,
}
