# -*- coding: utf-8 -*-
"""Figures de la page « Électricité : toutes les lois et formules ».

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/physique-chimie/lois-de-l-electricite --planche

Symboles normalisés du collège et du lycée : pile (grand trait fin = borne +),
lampe (cercle barré), résistance (rectangle), appareils de mesure (cercle et
lettre). Les fils s'arrêtent toujours au bord des symboles.
"""

NOTE = r"\otMedium\fontsize{10.5}{12}\selectfont"
FIL = "otInk,line width=0.9pt"
R_ROND = 0.28  # rayon des lampes, moteurs et appareils de mesure


def legende(x, y, texte, ancre="north"):
    return rf"  \node[anchor={ancre},align=center,font={NOTE},text=otMuted] at ({x},{y}) {{{texte}}};" + "\n"


def fil(*points):
    return rf"  \draw[{FIL}] " + " -- ".join(f"({x},{y})" for x, y in points) + ";\n"


def rond(x, y, lettre=None, croix=False):
    s = rf"  \draw[{FIL},fill=white] ({x},{y}) circle ({R_ROND});" + "\n"
    if croix:
        d = round(R_ROND * 0.7071, 3)
        s += rf"  \draw[otInk,line width=0.75pt] ({x - d},{y - d}) -- ({x + d},{y + d}) ({x - d},{y + d}) -- ({x + d},{y - d});" + "\n"
    if lettre:
        s += rf"  \node[text=otInk,font=\otMedium\fontsize{{11}}{{12}}\selectfont] at ({x},{y}) {{{lettre}}};" + "\n"
    return s


def pile_h(x, y, plus=True):
    """Pile sur un fil horizontal : grand trait fin (+) à gauche, petit trait épais (−) à droite."""
    s = rf"  \draw[otInk,line width=0.9pt] ({x - 0.09},{y - 0.3}) -- ({x - 0.09},{y + 0.3});" + "\n"
    s += rf"  \draw[otInk,line width=2.4pt] ({x + 0.09},{y - 0.15}) -- ({x + 0.09},{y + 0.15});" + "\n"
    if plus:
        s += rf"  \node[anchor=south east,text=otInk,font=\small,inner sep=1pt] at ({x - 0.13},{y + 0.3}) {{$+$}};" + "\n"
    return s


def pile_v(x, y):
    """Pile sur un fil vertical : grand trait fin (+) en haut."""
    s = rf"  \draw[otInk,line width=0.9pt] ({x - 0.3},{y + 0.09}) -- ({x + 0.3},{y + 0.09});" + "\n"
    s += rf"  \draw[otInk,line width=2.4pt] ({x - 0.15},{y - 0.09}) -- ({x + 0.15},{y - 0.09});" + "\n"
    s += rf"  \node[anchor=east,text=otInk,font=\small] at ({x - 0.34},{y + 0.26}) {{$+$}};" + "\n"
    return s


def resistance_h(x, y):
    return rf"  \draw[{FIL},fill=white] ({x - 0.4},{y - 0.14}) rectangle ({x + 0.4},{y + 0.14});" + "\n"


def resistance_v(x, y):
    return rf"  \draw[{FIL},fill=white] ({x - 0.14},{y - 0.4}) rectangle ({x + 0.14},{y + 0.4});" + "\n"


def point(x, y):
    return rf"  \fill[otInk] ({x},{y}) circle (2pt);" + "\n"


def courant(x, y, sens, nom, cote):
    dx, dy = {"droite": (0.18, 0), "gauche": (-0.18, 0), "bas": (0, -0.18), "haut": (0, 0.18)}[sens]
    ancre, ex, ey = {"above": ("south", 0, 0.14), "below": ("north", 0, -0.14),
                     "right": ("west", 0.16, 0), "left": ("east", -0.16, 0)}[cote]
    return (
        rf"  \draw[otOrange!85!black,line width=1.1pt,-{{Stealth[length=2.4mm]}}] ({x - dx},{y - dy}) -- ({x + dx},{y + dy});" + "\n"
        + rf"  \node[anchor={ancre},text=otOrange!75!black,font=\large] at ({x + ex},{y + ey}) {{${nom}$}};" + "\n"
    )


def tension(x1, y1, x2, y2, nom, ancre):
    """Flèche de tension (pointe vers la borne de plus haut potentiel, convention du lycée)."""
    xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
    return (
        rf"  \draw[otGreenDark,line width=1pt,-{{Stealth[length=2.4mm]}}] ({x1},{y1}) -- ({x2},{y2});" + "\n"
        + rf"  \node[anchor={ancre},text=otGreenDark,font=\large,inner sep=2pt] at ({xm},{ym}) {{${nom}$}};" + "\n"
    )


# ---------------------------------------------------------------- 1. symboles normalisés
PAS = 2.65


def case(i, ligne):
    return i * PAS, -ligne * 2.0


def symbole(i, ligne, dessin, nom):
    x, y = case(i, ligne)
    return dessin(x, y) + legende(x, y - 0.5, nom)


def s_pile(x, y):
    return fil((x - 0.8, y), (x - 0.09, y)) + fil((x + 0.09, y), (x + 0.8, y)) + pile_h(x, y)


def s_lampe(x, y):
    return fil((x - 0.8, y), (x - R_ROND, y)) + fil((x + R_ROND, y), (x + 0.8, y)) + rond(x, y, croix=True)


def s_resistance(x, y):
    return fil((x - 0.8, y), (x - 0.4, y)) + fil((x + 0.4, y), (x + 0.8, y)) + resistance_h(x, y)


def s_interrupteur(ouvert):
    def dessin(x, y):
        s = fil((x - 0.8, y), (x - 0.35, y)) + fil((x + 0.35, y), (x + 0.8, y))
        s += point(x - 0.35, y) + point(x + 0.35, y)
        fin = (x + 0.3, y + 0.34) if ouvert else (x + 0.35, y)
        s += rf"  \draw[{FIL}] ({x - 0.35},{y}) -- {fin};" + "\n"
        return s
    return dessin


def s_diode(del_=False):
    def dessin(x, y):
        s = fil((x - 0.8, y), (x - 0.2, y)) + fil((x + 0.2, y), (x + 0.8, y))
        s += rf"  \draw[{FIL},fill=white] ({x - 0.2},{y - 0.22}) -- ({x - 0.2},{y + 0.22}) -- ({x + 0.2},{y}) -- cycle;" + "\n"
        s += rf"  \draw[{FIL}] ({x + 0.2},{y - 0.22}) -- ({x + 0.2},{y + 0.22});" + "\n"
        if del_:
            for d in (0, 0.17):
                s += rf"  \draw[otOrange!85!black,line width=0.8pt,-{{Stealth[length=1.6mm]}}] ({x + 0.02 + d},{y + 0.3}) -- ({x + 0.24 + d},{y + 0.52});" + "\n"
        return s
    return dessin


def s_rond(lettre):
    def dessin(x, y):
        return fil((x - 0.8, y), (x - R_ROND, y)) + fil((x + R_ROND, y), (x + 0.8, y)) + rond(x, y, lettre)
    return dessin


SYMBOLES = (
    "\n\\begin{tikzpicture}\n"
    + symbole(0, 0, s_pile, r"Pile\\(générateur)")
    + symbole(1, 0, s_lampe, "Lampe")
    + symbole(2, 0, s_resistance, "Résistance")
    + symbole(3, 0, s_rond("M"), "Moteur")
    + symbole(0, 1, s_interrupteur(True), r"Interrupteur\\ouvert")
    + symbole(1, 1, s_interrupteur(False), r"Interrupteur\\fermé")
    + symbole(2, 1, s_diode(), "Diode")
    + symbole(3, 1, s_diode(True), r"DEL\\(diode lumineuse)")
    + symbole(1, 2, s_rond("A"), "Ampèremètre")
    + symbole(2, 2, s_rond("V"), "Voltmètre")
    + "\\end{tikzpicture}"
)


# ---------------------------------------------------------------- 2. série et dérivation
def circuit_serie(x0):
    L, H, yp = 3.4, 2.3, 1.15
    s = fil((x0, yp - 0.09), (x0, 0), (x0 + L, 0), (x0 + L, H), (x0 + 2.4 + R_ROND, H))
    s += fil((x0 + 2.4 - R_ROND, H), (x0 + 1.1 + R_ROND, H))
    s += fil((x0 + 1.1 - R_ROND, H), (x0, H), (x0, yp + 0.09))
    s += pile_v(x0, yp)
    s += rond(x0 + 1.1, H, croix=True) + rond(x0 + 2.4, H, croix=True)
    s += rf"  \node[anchor=south,text=otInk,font=\large] at ({x0 + 1.1},{H + 0.34}) {{$\mathrm{{L_1}}$}};" + "\n"
    s += rf"  \node[anchor=south,text=otInk,font=\large] at ({x0 + 2.4},{H + 0.34}) {{$\mathrm{{L_2}}$}};" + "\n"
    s += rf"  \node[anchor=north,text=otGreenDark,font=\large] at ({x0 + 1.1},{H - 0.4}) {{$U_1$}};" + "\n"
    s += rf"  \node[anchor=north,text=otGreenDark,font=\large] at ({x0 + 2.4},{H - 0.4}) {{$U_2$}};" + "\n"
    s += rf"  \node[anchor=west,text=otGreenDark,font=\large] at ({x0 + 0.38},{yp}) {{$U$}};" + "\n"
    s += courant(x0 + 1.7, 0, "gauche", "I", "below")
    s += courant(x0 + L, 1.15, "bas", "I", "right")
    s += legende(x0 + L / 2, -0.62, "En série")
    return s


def circuit_derivation(x0):
    L, xm, H, yp = 4.0, 2.1, 2.3, 1.15
    s = fil((x0, yp - 0.09), (x0, 0), (x0 + L, 0), (x0 + L, yp - R_ROND))
    s += fil((x0 + L, yp + R_ROND), (x0 + L, H), (x0, H), (x0, yp + 0.09))
    s += fil((x0 + xm, 0), (x0 + xm, yp - R_ROND)) + fil((x0 + xm, yp + R_ROND), (x0 + xm, H))
    s += pile_v(x0, yp)
    s += rond(x0 + xm, yp, croix=True) + rond(x0 + L, yp, croix=True)
    s += rf"  \node[anchor=east,text=otInk,font=\large] at ({x0 + xm - 0.36},{yp}) {{$\mathrm{{L_1}}$}};" + "\n"
    s += rf"  \node[anchor=west,text=otInk,font=\large] at ({x0 + L + 0.36},{yp}) {{$\mathrm{{L_2}}$}};" + "\n"
    s += point(x0 + xm, H) + point(x0 + xm, 0)
    s += courant(x0 + 1.0, H, "droite", "I", "above")
    s += courant(x0 + xm, 1.85, "bas", "I_1", "right")
    s += courant(x0 + L, 1.85, "bas", "I_2", "left")
    s += legende(x0 + L / 2, -0.62, "En dérivation")
    return s


SERIE_DERIVATION = "\n\\begin{tikzpicture}\n" + circuit_serie(0) + circuit_derivation(5.1) + "\\end{tikzpicture}"


# ---------------------------------------------------------------- 3. brancher les appareils de mesure
def mesures():
    L, H, yp, xl, ya = 3.6, 2.0, 1.0, 1.6, 1.0
    s = fil((0, yp - 0.09), (0, 0), (L, 0), (L, ya - R_ROND))
    s += fil((L, ya + R_ROND), (L, H), (xl + R_ROND, H))
    s += fil((xl - R_ROND, H), (0, H), (0, yp + 0.09))
    s += pile_v(0, yp)
    s += rond(xl, H, croix=True)
    s += rond(L, ya, "A")
    # voltmètre en dérivation aux bornes de la lampe
    xg, xd, yv = xl - 0.75, xl + 0.75, H + 1.05
    s += fil((xg, H), (xg, yv), (xl - R_ROND, yv)) + fil((xl + R_ROND, yv), (xd, yv), (xd, H))
    s += point(xg, H) + point(xd, H)
    s += rond(xl, yv, "V")
    s += rf"  \node[anchor=north,text=otInk,font=\large] at ({xl},{H - 0.34}) {{$\mathrm{{L}}$}};" + "\n"
    s += legende(xd + 0.35, yv, r"Voltmètre :\\en dérivation", "west")
    s += legende(L + 0.45, ya, r"Ampèremètre :\\en série", "west")
    return "\n\\begin{tikzpicture}\n" + s + "\\end{tikzpicture}"


MESURES = mesures()


# ---------------------------------------------------------------- 4. nœud et maille
def noeud():
    s = point(1.4, 1.2)
    s += fil((0, 1.2), (1.4, 1.2)) + fil((1.4, 1.2), (2.6, 2.1)) + fil((1.4, 1.2), (2.6, 0.3))
    s += courant(0.65, 1.2, "droite", "I_1", "above")
    s += rf"  \draw[otOrange!85!black,line width=1.1pt,-{{Stealth[length=2.4mm]}}] (1.86,1.545) -- (2.14,1.755);" + "\n"
    s += rf"  \node[anchor=south east,text=otOrange!75!black,font=\large] at (1.95,1.75) {{$I_2$}};" + "\n"
    s += rf"  \draw[otOrange!85!black,line width=1.1pt,-{{Stealth[length=2.4mm]}}] (1.86,0.855) -- (2.14,0.645);" + "\n"
    s += rf"  \node[anchor=north east,text=otOrange!75!black,font=\large] at (1.95,0.65) {{$I_3$}};" + "\n"
    s += legende(1.3, -0.2, r"Nœud : $I_1 = I_2 + I_3$")
    return s


def maille(x0):
    L, H, yp = 3.4, 2.4, 1.2
    s = fil((x0, yp - 0.09), (x0, 0), (x0 + L, 0), (x0 + L, yp - 0.4))
    s += fil((x0 + L, yp + 0.4), (x0 + L, H), (x0 + 1.7 + 0.4, H))
    s += fil((x0 + 1.7 - 0.4, H), (x0, H), (x0, yp + 0.09))
    s += pile_v(x0, yp)
    s += resistance_h(x0 + 1.7, H) + resistance_v(x0 + L, yp)
    s += rf"  \node[anchor=east,text=otInk,font=\large] at ({x0 - 0.08},{H + 0.02}) {{$\mathrm{{P}}$}};" + "\n"
    s += rf"  \node[anchor=east,text=otInk,font=\large] at ({x0 - 0.08},{-0.02}) {{$\mathrm{{N}}$}};" + "\n"
    s += rf"  \node[anchor=north,text=otInk,font=\large] at ({x0 + 1.7},{H - 0.2}) {{$R_1$}};" + "\n"
    s += rf"  \node[anchor=east,text=otInk,font=\large] at ({x0 + L - 0.22},{yp}) {{$R_2$}};" + "\n"
    s += courant(x0 + 0.75, H, "droite", "I", "above")
    # Tensions : générateur dans le sens du courant, récepteurs en sens inverse.
    s += tension(x0 - 1.0, yp - 0.45, x0 - 1.0, yp + 0.45, r"U_{\mathrm{PN}}", "east")
    s += tension(x0 + 2.15, H + 0.45, x0 + 1.25, H + 0.45, "U_1", "south")
    s += tension(x0 + L + 0.5, yp - 0.45, x0 + L + 0.5, yp + 0.45, "U_2", "west")
    s += legende(x0 + L / 2, -0.2, r"Maille : $U_{\mathrm{PN}} = U_1 + U_2$")
    return s


NOEUD_MAILLE = "\n\\begin{tikzpicture}\n" + noeud() + maille(5.0) + "\\end{tikzpicture}"


# ---------------------------------------------------------------- 5. caractéristiques
AXES = r"otWeb, width=4.6cm, height=3.6cm, xlabel={$I$ (A)}, ylabel={$U$ (V)}, grid=none"

# Résistance (droite passant par l'origine) et lampe (courbe : sa résistance
# augmente quand son filament chauffe).
CARACTERISTIQUES = r"""
\begin{tikzpicture}
\begin{axis}[""" + AXES + r""", xmin=0, xmax=0.33, ymin=0, ymax=7.4,
  xtick={0.1,0.2,0.3}, ytick={2,4,6}]
  \addplot[courbe, domain=0:0.3] {20*x};
  \addplot[courbe2, domain=0:0.22, samples=80] {10*x + 430*x^3};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:0.305,6.0) {résistance};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:0.226,6.78) {lampe};
\end{axis}
\end{tikzpicture}"""

# Source réelle U = E − r I (E = 4,5 V, r = 1,5 Ω) branchée sur une résistance
# de 3 Ω : point de fonctionnement F (1 A ; 3 V).
SOURCE_REELLE = r"""
\begin{tikzpicture}
\begin{axis}[""" + AXES + r""", xmin=0, xmax=1.65, ymin=0, ymax=5.4,
  xtick={0.5,1,1.5}, ytick={1,2,3,4}]
  \addplot[courbe, domain=0:1.5] {4.5 - 1.5*x};
  \addplot[courbe2, domain=0:1.5] {3*x};
  \draw[guide] (axis cs:1,0) -- (axis cs:1,3) -- (axis cs:0,3);
  \pnt{1}{3}
  \pnt{0}{4.5}
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:0.05,4.62) {$E$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:1.52,2.25) {source};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:1.52,4.5) {résistance};
  \node[etiq,text=otInk,anchor=west] at (axis cs:1.17,3.0) {$F$};
\end{axis}
\end{tikzpicture}"""


# ---------------------------------------------------------------- 6. charge et décharge du condensateur
CHARGE_RC = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=8.4cm, height=3.6cm, xmin=0, xmax=6.4, ymin=0, ymax=5.9,
  xlabel={$t$}, ylabel={$u_C$}, grid=none,
  xtick={1,5}, xticklabels={$\tau$,$5\tau$}, ytick={3.16,5}, yticklabels={$0{,}63\,E$,$E$}]
  \draw[asymptote] (axis cs:0,5) -- (axis cs:6.4,5);
  \draw[seuil] (axis cs:0,0) -- (axis cs:1,5);
  \draw[guide] (axis cs:1,0) -- (axis cs:1,3.16) -- (axis cs:0,3.16);
  \addplot[courbe, domain=0:6.3, samples=200] {5*(1 - exp(-x))};
  \addplot[courbe2, domain=0:6.3, samples=200] {5*exp(-x)};
  \pnt{1}{3.16}
  \node[etiq,text=otNavy,anchor=south] at (axis cs:3.9,5.05) {charge : $u_C = E\left(1 - \mathrm{e}^{-t/\tau}\right)$};
  \node[etiq,text=otGreenDark,anchor=south west] at (axis cs:1.75,1.0) {décharge : $u_C = E\,\mathrm{e}^{-t/\tau}$};
\end{axis}
\end{tikzpicture}"""


FIGURES = {
    "symboles_electriques": SYMBOLES,
    "circuits_serie_derivation": SERIE_DERIVATION,
    "mesures_ampere_volt": MESURES,
    "noeud_maille": NOEUD_MAILLE,
    "caracteristiques": CARACTERISTIQUES,
    "source_reelle": SOURCE_REELLE,
    "charge_condensateur": CHARGE_RC,
}
