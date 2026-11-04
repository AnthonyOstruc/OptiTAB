# -*- coding: utf-8 -*-
"""Figures de la notion 157 (Première, trigonométrie), style des livres OptiTAB.

Compilées par outils/figures_livre.py :
    python figures_livre.py ../chantier/1ere/157_trigonometrie [nom …]

Les cercles trigonométriques sont produits par la fonction cercle() : unité
= rayon du cercle (x = y = R cm), points en \\fill … circle, étiquettes
posées radialement à l'extérieur du cercle (ancre opposée à la direction du
point), donc jamais sur un trait.
"""
import math

PI = math.pi


def _n(v):
    return f"{v:.4f}"


def _pt(t, r=1.0):
    return "(" + _n(r * math.cos(t)) + "," + _n(r * math.sin(t)) + ")"


def cercle(R=2.4, points=(), ticks=(), avant="", apres="", O=True, I=True, J=True,
           xmin=-1.3, xmax=1.38, ymin=-1.3, ymax=1.38):
    """Cercle trigonométrique.

    points : tuples (t, étiquette, couleur, ancre|None, écart) ; ancre None =
    radiale (étiquette à l'extérieur, dans la direction du point).
    ticks : angles (rad) marqués d'un petit trait radial gris.
    """
    s = [r"\begin{tikzpicture}[x=" + str(R) + "cm,y=" + str(R) + "cm,line cap=round,line join=round]"]
    s.append(r"\draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (" + _n(xmin) + ",0) -- (" + _n(xmax) + ",0);")
    s.append(r"\draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (0," + _n(ymin) + ") -- (0," + _n(ymax) + ");")
    s.append(avant)
    s.append(r"\draw[otNavy,line width=1pt] (0,0) circle (1);")
    for t in ticks:
        s.append(r"\draw[otMuted,line width=0.55pt] " + _pt(t, 0.955) + " -- " + _pt(t, 1.045) + ";")
    if O == "bas":
        s.append(r"\node[anchor=north west,inner sep=1.5pt,text=otInk] at (0.02,-0.02) {$O$};")
    elif O:
        s.append(r"\node[anchor=north east,inner sep=1.5pt,text=otInk] at (-0.02,-0.02) {$O$};")
    if I:
        s.append(r"\fill[otNavy] (1,0) circle (1.9pt);")
        s.append(r"\node[anchor=north west,inner sep=1.5pt,text=otInk] at (1.02,-0.02) {$I$};")
    if J:
        s.append(r"\fill[otNavy] (0,1) circle (1.9pt);")
        s.append(r"\node[anchor=south west,inner sep=1.5pt,text=otInk] at (0.03,1.02) {$J$};")
    s.append(apres)
    for p in points:
        t, lab, col = p[0], p[1], p[2]
        anc = p[3] if len(p) > 3 else None
        ecart = p[4] if len(p) > 4 else 0.06
        s.append(r"\fill[" + col + "] " + _pt(t) + " circle (2.2pt);")
        if lab:
            if anc is None:
                deg = (math.degrees(t) + 180) % 360
                s.append(r"\node[anchor=" + f"{deg:.0f}" + ",inner sep=1.2pt,text=" + col + "] at " + _pt(t, 1 + ecart) + " {" + lab + "};")
            else:
                s.append(r"\node[anchor=" + anc + ",inner sep=1.2pt,text=" + col + "] at " + _pt(t, 1 + ecart) + " {" + lab + "};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(x for x in s if x)


def F(num, den, signe=""):
    return "$" + signe + r"\dfrac{" + num + "}{" + den + "}$"


V = "otGreenDark"
N = "otNavy"
PI6 = [k * PI / 6 for k in range(12)]
PI4 = [PI / 4 + k * PI / 2 for k in range(4)]

# ------------------------------------------------------------------ cours
# Enroulement de la droite des réels (tangente en I) sur le cercle
T_ENR = 0.9
ENROULEMENT = (
    r"\begin{tikzpicture}[x=1.9cm,y=1.9cm,line cap=round,line join=round]" "\n"
    r"\draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (-1.3,0) -- (1.55,0);" "\n"
    r"\draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (0,-1.3) -- (0,1.45);" "\n"
    r"\draw[otNavy,line width=1pt] (0,0) circle (1);" "\n"
    r"\draw[otInk,line width=0.8pt,-{Stealth[length=2.3mm]}] (1,-1.35) -- (1,2.35);" "\n"
    r"\foreach \k in {-1,1,2} {\draw[otInk,line width=0.6pt] (0.95,\k) -- (1.05,\k);}" "\n"
    r"\node[anchor=east,inner sep=1.5pt,text=otMuted,font=\otRegular\fontsize{9}{10}\selectfont] at (0.93,1) {$1$};" "\n"
    r"\node[anchor=east,inner sep=1.5pt,text=otMuted,font=\otRegular\fontsize{9}{10}\selectfont] at (0.93,2) {$2$};" "\n"
    r"\node[anchor=east,inner sep=1.5pt,text=otMuted,font=\otRegular\fontsize{9}{10}\selectfont] at (0.93,-1) {$-1$};" "\n"
    r"\draw[otGreen,line width=2.6pt,line cap=butt] (1,0) -- (1," + _n(T_ENR) + ");" "\n"
    r"\draw[otGreen,line width=2.6pt,line cap=butt] (1,0) arc (0:" + f"{math.degrees(T_ENR):.2f}" + ":1);" "\n"
    r"\fill[otGreenDark] (1," + _n(T_ENR) + ") circle (2.2pt);" "\n"
    r"\node[anchor=west,inner sep=1.5pt,text=otGreenDark] at (1.05," + _n(T_ENR) + ") {$N(t)$};" "\n"
    r"\fill[otGreenDark] " + _pt(T_ENR) + " circle (2.2pt);" "\n"
    r"\node[anchor=north east,inner sep=1.2pt,text=otGreenDark] at " + _pt(T_ENR, 0.95) + " {$M(t)$};" "\n"
    r"\fill[otNavy] (1,0) circle (1.9pt);" "\n"
    r"\node[anchor=north west,inner sep=1.5pt,text=otInk] at (1.02,-0.02) {$I$};" "\n"
    r"\node[anchor=north east,inner sep=1.5pt,text=otInk] at (-0.02,-0.02) {$O$};" "\n"
    r"\node[anchor=south east,inner sep=1.5pt,text=otInk] at (-0.03,1.02) {$J$};" "\n"
    r"\fill[otNavy] (0,1) circle (1.9pt);" "\n"
    r"\node[note,anchor=west] at (1.08,2.15) {droite des réels};" "\n"
    r"\end{tikzpicture}"
)

T_CS = 0.9
COS_SIN = cercle(
    R=2.6,
    avant=(r"\draw[otNavy,line width=0.9pt] (0,0) -- " + _pt(T_CS) + ";" "\n"
           r"\draw[guide] " + _pt(T_CS) + " -- (" + _n(math.cos(T_CS)) + ",0);" "\n"
           r"\draw[guide] " + _pt(T_CS) + " -- (0," + _n(math.sin(T_CS)) + ");" "\n"
           r"\draw[otNavy,line width=0.6pt] (" + _n(math.cos(T_CS) - 0.07) + ",0) -- (" + _n(math.cos(T_CS) - 0.07) + ",0.07) -- (" + _n(math.cos(T_CS)) + ",0.07);" "\n"
           r"\draw[otGreenDark,line width=0.7pt,-{Stealth[length=1.6mm]}] (0.24,0) arc (0:" + f"{math.degrees(T_CS):.1f}" + ":0.24);" "\n"
           r"\node[text=otGreenDark,inner sep=1pt] at " + _pt(T_CS / 2, 0.34) + " {$t$};" "\n"
           r"\fill[otNavy] (" + _n(math.cos(T_CS)) + ",0) circle (1.6pt);" "\n"
           r"\fill[otNavy] (0," + _n(math.sin(T_CS)) + ") circle (1.6pt);" "\n"
           r"\node[anchor=north,inner sep=2pt,text=otGreenDark] at (" + _n(math.cos(T_CS)) + r",-0.02) {$\cos t$};" "\n"
           r"\node[anchor=east,inner sep=2pt,text=otGreenDark] at (-0.02," + _n(math.sin(T_CS)) + r") {$\sin t$};" "\n"
           r"\node[anchor=south west,inner sep=1.2pt,text=otInk] at (" + _n(math.cos(T_CS) + 0.01) + ",0.01) {$H$};"),
    points=[(T_CS, r"$M(t)$", N)],
)

# Premier quadrant agrandi : coordonnées des points de pi/6, pi/4, pi/3
def quadrant():
    R = 6.0
    s = [r"\begin{tikzpicture}[x=" + str(R) + "cm,y=" + str(R) + "cm,line cap=round,line join=round]"]
    s.append(r"\draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (-0.06,0) -- (1.2,0);")
    s.append(r"\draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (0,-0.06) -- (0,1.2);")
    s.append(r"\draw[otNavy,line width=1pt] (1,0) arc (0:90:1);")
    vals = [(PI / 6, r"\dfrac{\pi}{6}"), (PI / 4, r"\dfrac{\pi}{4}"), (PI / 3, r"\dfrac{\pi}{3}")]
    for t, lab in vals:
        c, sn = math.cos(t), math.sin(t)
        s.append(r"\draw[guide] (" + _n(c) + ",0) -- (" + _n(c) + "," + _n(sn) + ") -- (0," + _n(sn) + ");")
        s.append(r"\draw[otRule,line width=0.6pt] (0,0) -- " + _pt(t) + ";")
    gx = [(0.5, r"\dfrac{1}{2}"), (math.sqrt(2) / 2, r"\dfrac{\sqrt{2}}{2}"), (math.sqrt(3) / 2, r"\dfrac{\sqrt{3}}{2}"), (1, "1")]
    for v, lab in gx:
        s.append(r"\draw[otMuted,line width=0.5pt] (" + _n(v) + ",0) -- (" + _n(v) + ",-0.012);")
        s.append(r"\node[anchor=north,inner sep=1.5pt,text=otMuted] at (" + _n(v) + ",-0.014) {$" + lab + "$};")
        s.append(r"\draw[otMuted,line width=0.5pt] (0," + _n(v) + ") -- (-0.012," + _n(v) + ");")
        s.append(r"\node[anchor=east,inner sep=1.5pt,text=otMuted] at (-0.014," + _n(v) + ") {$" + lab + "$};")
    s.append(r"\node[anchor=north east,inner sep=1.5pt,text=otInk] at (-0.01,-0.01) {$O$};")
    for t, lab in vals:
        s.append(r"\fill[otGreenDark] " + _pt(t) + " circle (2.3pt);")
        deg = (math.degrees(t) + 180) % 360
        s.append(r"\node[anchor=" + f"{deg:.0f}" + ",inner sep=1.2pt,text=otGreenDark] at " + _pt(t, 1.035) + " {$" + lab + "$};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


# Cercle complet des valeurs remarquables (mesures dans ]-pi ; pi])
def _lab_angle(k, d):
    """k/d * pi en LaTeX."""
    from fractions import Fraction
    f = Fraction(k, d)
    if f == 0:
        return "$0$"
    sg = "-" if f < 0 else ""
    f = abs(f)
    num = "" if f.numerator == 1 else str(f.numerator)
    if f.denominator == 1:
        return "$" + sg + num + r"\pi$"
    return "$" + sg + r"\dfrac{" + num + r"\pi}{" + str(f.denominator) + "}$"


def cercle_complet():
    pts = []
    for k, d in [(1, 6), (1, 4), (1, 3), (2, 3), (3, 4), (5, 6), (-1, 6), (-1, 4), (-1, 3), (-2, 3), (-3, 4), (-5, 6)]:
        pts.append((k * PI / d, _lab_angle(k, d), N))
    pts.append((0, "$0$", V, "south west", 0.03))
    pts.append((PI, r"$\pi$", V, "south east", 0.03))
    pts.append((PI / 2, r"$\dfrac{\pi}{2}$", V, "south west", 0.03))
    pts.append((-PI / 2, r"$-\dfrac{\pi}{2}$", V, "north west", 0.03))
    rayons = "\n".join(r"\draw[otRule,line width=0.5pt] (0,0) -- " + _pt(p[0]) + ";" for p in pts[:12])
    return cercle(R=2.7, points=pts, avant=rayons, I=False, J=False, xmin=-1.32, xmax=1.4, ymin=-1.32, ymax=1.42)


X_AS = 0.55
def associes():
    x = X_AS
    av = (r"\draw[otRule,line width=0.6pt,dash pattern=on 3pt off 2pt] (-0.42,-0.42) -- (1.06,1.06);" "\n"
          r"\node[note,anchor=north west] at (1.0,0.98) {$y=x$};" "\n"
          r"\draw[guide] " + _pt(x) + " -- " + _pt(-x) + ";" "\n"
          r"\draw[guide] " + _pt(x) + " -- " + _pt(PI - x) + ";" "\n"
          r"\draw[guide] " + _pt(x) + " -- " + _pt(PI + x) + ";" "\n"
          r"\draw[guide] " + _pt(x) + " -- " + _pt(PI / 2 - x) + ";")
    pts = [(x, r"$M(x)$", N),
           (-x, r"$M(-x)$", V),
           (PI - x, r"$M(\pi-x)$", V, None, 0.1),
           (PI + x, r"$M(\pi+x)$", V, None, 0.1),
           (PI / 2 - x, r"$M\left(\dfrac{\pi}{2}-x\right)$", V)]
    return cercle(R=2.5, points=pts, avant=av, I=False, J=False)


def courbes(lab1, lab2, nom_cos, nom_sin):
    return (r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=2.88cm, xmin=-6.9, xmax=7.3, ymin=-1.62, ymax=1.95,
  xtick={-6.2832,-3.1416,3.1416,6.2832}, xticklabels={$-2\pi$,$-\pi$,$\pi$,$2\pi$},
  minor xtick={-4.7124,-1.5708,1.5708,4.7124}, minor grid style={otRule!45,line width=0.3pt}, minor tick length=0pt,
  ytick={-1,1}]
  \addplot[courbe2, domain=-6.9:7.1] {cos(x)};
  \addplot[courbe, domain=-6.9:7.1] {sin(x)};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:1.5708,1.12) {""" + nom_sin + r"""};
  \node[etiq,text=otGreenDark,anchor=south] at (axis cs:-3.1416,1.12) {""" + nom_cos + r"""};
""" + lab1 + lab2 + r"""\end{axis}
\end{tikzpicture}""")


PERIODE = (r"  \draw[otMuted,line width=0.6pt,{Stealth[length=1.8mm]}-{Stealth[length=1.8mm]}] (axis cs:0,-1.42) -- (axis cs:6.2832,-1.42)" "\n"
           r"    node[note,midway,below=1.5pt] {période $2\pi$};" "\n")

# ------------------------------------------------------------------ exercices
EX1384 = cercle(
    R=2.3,
    points=[(PI / 2, "", V), (PI, r"$M(\pi)$", V, "south east", 0.03), (0, "", V),
            (-PI / 2, r"$M\left(-\dfrac{\pi}{2}\right)$", V, "north west", 0.03)],
    I=False, J=False,
    apres=(r"\node[anchor=south west,inner sep=1.2pt,text=otGreenDark] at (0.03,1.03) {$M\left(\dfrac{\pi}{2}\right)=J$};" "\n"
           r"\node[anchor=north west,inner sep=1.2pt,text=otGreenDark] at (1.03,-0.03) {$M(2\pi)=I$};" "\n"
           r"\node[anchor=south west,inner sep=1.2pt,text=otGreenDark] at (1.03,0.03) {$M(0)$};"),
)

def _pi3_equilateral():
    c, s = 0.5, math.sqrt(3) / 2
    av = (r"\draw[otNavy,line width=0.9pt] (0,0) -- (" + _n(c) + "," + _n(s) + ") -- (1,0);" "\n"
          r"\draw[otNavy,line width=0.9pt] (0,0) -- (1,0);" "\n"
          r"\draw[geoAide] (" + _n(c) + "," + _n(s) + ") -- (" + _n(c) + ",0);" "\n"
          r"\draw[otGreenDark,line width=0.6pt] (0.44,0) -- (0.44,0.06) -- (0.5,0.06);" "\n"
          r"\coordinate (O) at (0,0); \coordinate (I) at (1,0); \coordinate (M) at (" + _n(c) + "," + _n(s) + ");" "\n"
          r"\codage[2]{O}{M} \codage[2]{M}{I}" "\n"
          r"\draw[otGreenDark,line width=0.7pt] (0.2,0) arc (0:60:0.2);" "\n"
          r"\node[text=otGreenDark,inner sep=1pt,font=\small] at " + _pt(PI / 6, 0.32) + r" {$\frac{\pi}{3}$};" "\n"
          r"\fill[otNavy] (0.5,0) circle (1.6pt);" "\n"
          r"\node[anchor=north,inner sep=2pt,text=otInk] at (0.5,-0.02) {$H$};")
    return cercle(R=2.6, points=[(PI / 3, r"$M\left(\dfrac{\pi}{3}\right)$", V)], avant=av)


EX1385_PI3 = _pi3_equilateral()

TICKS = sorted(set([round(a, 6) for a in PI6 + PI4]))

EX1392_Q1 = cercle(
    R=2.6, ticks=TICKS,
    points=[(PI / 6, F(r"\pi", "6"), V), (5 * PI / 4, F(r"5\pi", "4"), V, "north east", 0.06),
            (7 * PI / 6, F(r"7\pi", "6"), V, "east", 0.07), (-PI / 3, F(r"\pi", "3", "-"), V)],
)

EX1392_Q2 = cercle(
    R=2.6, ticks=TICKS,
    points=[(PI / 6, F(r"13\pi", "6"), V), (3 * PI / 4, F(r"5\pi", "4", "-"), V), (PI / 3, F(r"19\pi", "3"), V)],
)

EX1387_COS = cercle(
    R=2.3,
    avant=(r"\draw[seuil] (0.5,-1.0) -- (0.5,1.0);" "\n"
           r"\node[anchor=north west,inner sep=1.5pt,text=otOrange!80!black] at (0.52,-0.02) {$\dfrac{1}{2}$};"),
    points=[(PI / 3, F(r"\pi", "3"), V), (5 * PI / 3, F(r"5\pi", "3"), V)],
)

EX1387_SIN = cercle(
    R=2.3,
    avant=(r"\draw[seuil] (-1.0," + _n(-math.sqrt(2) / 2) + ") -- (1.0," + _n(-math.sqrt(2) / 2) + ");" "\n"
           r"\node[anchor=south east,inner sep=1.5pt,text=otOrange!80!black] at (-0.02," + _n(-math.sqrt(2) / 2 + 0.02) + r") {$-\dfrac{\sqrt{2}}{2}$};"),
    points=[(5 * PI / 4, F(r"5\pi", "4"), V), (7 * PI / 4, F(r"7\pi", "4"), V)],
)

EX1387_BIS = cercle(
    R=2.3,
    avant=(r"\draw[seuil] (-0.7071,-0.7071) -- (0.7071,0.7071);" "\n"
           r"\node[note,anchor=north west] at (0.3,0.2) {$y=x$};"),
    points=[(PI / 4, F(r"\pi", "4"), V), (5 * PI / 4, F(r"5\pi", "4"), V)], O="bas",
)

A_1390 = PI + math.acos(0.4)
EX1390 = cercle(
    R=2.6,
    avant=(r"\draw[otGreen!45,line width=4pt,line cap=butt] (-1,0) arc (180:270:1);" "\n"
           r"\draw[seuil] (-0.4,-1.12) -- (-0.4,1.12);" "\n"
           r"\draw[guide] " + _pt(A_1390) + " -- (0," + _n(math.sin(A_1390)) + ");" "\n"
           r"\node[anchor=north east,inner sep=1.5pt,text=otOrange!80!black] at (-0.42,-0.02) {$-\dfrac{2}{5}$};" "\n"
           r"\node[anchor=west,inner sep=1.5pt,text=otGreenDark] at (0.03," + _n(math.sin(A_1390)) + r") {$\sin x$};" "\n"
           r"\draw[otNavy,fill=white,line width=0.9pt] " + _pt(PI - math.acos(0.4)) + " circle (2.2pt);"),
    points=[(A_1390, r"$M(x)$", V, "north east", 0.05)],
)

# Grande roue : centre C(0 ; 15), rayon 12, nacelle N après un angle theta depuis B
TH = 1.1
NX, NY = 12 * math.sin(TH), 15 - 12 * math.cos(TH)
ROUE = (
    r"\begin{tikzpicture}[x=0.19cm,y=0.19cm,line cap=round,line join=round]" "\n"
    r"\fill[otRule!60] (-18,-1.3) rectangle (18,0);" "\n"
    r"\draw[otInk,line width=0.8pt] (-18,0) -- (18,0);" "\n"
    r"\draw[otMuted,line width=1.1pt] (-6.5,0) -- (0,15) -- (6.5,0);" "\n"
    r"\draw[otNavy,line width=1.1pt] (0,15) circle (12);" "\n"
    r"\draw[guide] (0,15) -- (0,3);" "\n"
    r"\draw[otNavy,line width=0.9pt] (0,15) -- (" + _n(NX) + "," + _n(NY) + ");" "\n"
    r"\draw[otGreenDark,line width=0.8pt,-{Stealth[length=1.8mm]}] (0,11) arc (-90:" + f"{math.degrees(TH) - 90:.1f}" + ":4);" "\n"
    r"\node[text=otGreenDark,inner sep=1pt] at (" + _n(5.6 * math.sin(TH / 2)) + "," + _n(15 - 5.6 * math.cos(TH / 2)) + r") {$\theta$};" "\n"
    r"\draw[guide] (" + _n(NX) + "," + _n(NY) + ") -- (16.5," + _n(NY) + ");" "\n"
    r"\draw[cote] (16.5,0) -- (16.5," + _n(NY) + ") node[midway,coteTexte] {$h$};" "\n"
    r"\draw[guide] (0,15) -- (-16.5,15);" "\n"
    r"\draw[cote] (-16.5,0) -- (-16.5,15) node[midway,coteTexte] {$15$ m};" "\n"
    r"\draw[cote] (0.9,15) -- (0.9,27) node[midway,coteTexte] {$12$ m};" "\n"
    r"\fill[otNavy] (0,15) circle (2pt);" "\n"
    r"\node[anchor=south east,inner sep=1.5pt,text=otInk] at (-0.2,15.2) {$C$};" "\n"
    r"\fill[otNavy] (0,3) circle (2pt);" "\n"
    r"\node[anchor=north west,inner sep=1.5pt,text=otInk] at (0.3,2.8) {$B$};" "\n"
    r"\fill[otGreenDark] (" + _n(NX) + "," + _n(NY) + ") circle (2.6pt);" "\n"
    r"\node[anchor=south west,inner sep=1.5pt,text=otGreenDark] at (" + _n(NX + 0.4) + "," + _n(NY + 0.3) + ") {$N$};" "\n"
    r"\node[note,anchor=north west] at (-17.5,-1.6) {sol};" "\n"
    r"\end{tikzpicture}"
)

# f(x) = 2 cos x - 1 : étude sur [0 ; pi], parité, périodicité
EX1389 = r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8.4cm, height=3.9cm, xmin=-3.75, xmax=10.1, ymin=-3.6, ymax=1.9,
  xtick={-3.1416,3.1416,6.2832,9.4248}, xticklabels={$-\pi$,$\pi$,$2\pi$,$3\pi$},
  minor xtick={-1.5708,1.5708,4.7124,7.854}, minor grid style={otRule!45,line width=0.3pt}, minor tick length=0pt,
  ytick={-3,-2,-1,1}]
  \addplot[otOrange,line width=1.35pt, domain=3.1416:9.4248] {2*cos(x)-1};
  \addplot[courbe2, domain=-3.1416:0] {2*cos(x)-1};
  \addplot[courbe, domain=0:3.1416] {2*cos(x)-1};
  \pnt{0}{1} \pnt{1.0472}{0} \pnt{3.1416}{-3}
  \node[note,text=otNavy,anchor=north west] at (axis cs:1.75,-0.35) {étude};
  \node[note,text=otGreenDark,anchor=north east] at (axis cs:-1.75,-0.35) {parité};
  \node[note,text=otOrange!80!black,anchor=south] at (axis cs:6.2832,1.15) {périodicité};
\end{axis}
\end{tikzpicture}"""


def archimede():
    R = 2.8
    s = [r"\begin{tikzpicture}[x=" + str(R) + "cm,y=" + str(R) + "cm,line cap=round,line join=round]"]
    s.append(r"\draw[otNavy,line width=1pt] (0,0) circle (1);")
    hexa = " -- ".join(_pt(PI / 6 + k * PI / 3) for k in range(6)) + " -- cycle"
    s.append(r"\draw[otNavy!55,line width=0.8pt] " + hexa + ";")
    dodeca = " -- ".join(_pt(k * PI / 6) for k in range(12)) + " -- cycle"
    s.append(r"\draw[otGreen!70,line width=0.6pt] " + dodeca + ";")
    A, B = _pt(-PI / 6), _pt(PI / 6)
    h = math.cos(PI / 6)
    s.append(r"\draw[otNavy,line width=1.2pt] " + A + " -- " + B + ";")
    s.append(r"\draw[otGreenDark,line width=1.5pt] " + A + " -- (1,0);")
    s.append(r"\draw[geoAide] (0,0) -- (1,0);")
    s.append(r"\draw[otMuted,line width=0.6pt] (0,0) -- " + A + ";")
    s.append(r"\draw[otGreenDark,line width=0.6pt] (" + _n(h - 0.06) + ",0) -- (" + _n(h - 0.06) + ",0.06) -- (" + _n(h) + ",0.06);")
    s.append(r"\fill[otNavy] (0,0) circle (1.8pt);")
    s.append(r"\node[anchor=east,inner sep=2pt,text=otInk] at (-0.02,0) {$O$};")
    s.append(r"\fill[otNavy] " + A + " circle (2pt);")
    s.append(r"\node[anchor=north,inner sep=2pt,text=otInk] at " + _pt(-PI / 6, 1.05) + " {$A$};")
    s.append(r"\fill[otNavy] " + B + " circle (2pt);")
    s.append(r"\node[anchor=south,inner sep=2pt,text=otInk] at " + _pt(PI / 6, 1.05) + " {$B$};")
    s.append(r"\fill[otGreenDark] (1,0) circle (2pt);")
    s.append(r"\node[anchor=west,inner sep=2pt,text=otGreenDark] at (1.03,0) {$C$};")
    s.append(r"\fill[otNavy] (" + _n(h) + ",0) circle (1.6pt);")
    s.append(r"\node[anchor=north east,inner sep=1.5pt,text=otInk] at (" + _n(h - 0.01) + ",-0.01) {$H$};")
    s.append(r"\node[anchor=east,inner sep=1.5pt,text=otNavy] at (" + _n(h - 0.02) + ",0.3) {$c$};")
    s.append(r"\node[anchor=west,inner sep=1.5pt,text=otGreenDark] at (1.0,-0.33) {$c'$};")
    s.append(r"\node[anchor=north,inner sep=1.5pt,text=otMuted] at (0.42,-0.27) {$1$};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES = {
    "cours_enroulement": ENROULEMENT,
    "cours_cos_sin": COS_SIN,
    "cours_quadrant": quadrant(),
    "cours_cercle_complet": cercle_complet(),
    "cours_associes": associes(),
    "cours_courbes": courbes(PERIODE, "", r"$y=\cos x$", r"$y=\sin x$"),
    "ex1384_points": EX1384,
    "ex1385_pi3": EX1385_PI3,
    "ex1392_q1": EX1392_Q1,
    "ex1392_q2": EX1392_Q2,
    "ex1387_cos": EX1387_COS,
    "ex1387_sin": EX1387_SIN,
    "ex1387_bissectrice": EX1387_BIS,
    "ex1390_sinus": EX1390,
    "ex1388_roue": ROUE,
    "ex1389_courbe": EX1389,
    "nouveau1_archimede": archimede(),
    "nouveau2_courbes": courbes("", "", r"$\mathcal{C}_1$", r"$\mathcal{C}_2$"),
}

# ------------------------------------------------------------------ finition 2026-11-02
def _pi3(corrige):
    """Exercice 1385 Q3 : énoncé (triangle OIM, H) ou corrigé (codage du triangle équilatéral)."""
    if corrige:
        return _pi3_equilateral()
    c, s = 0.5, math.sqrt(3) / 2
    av = (r"\draw[otNavy,line width=0.9pt] (0,0) -- (" + _n(c) + "," + _n(s) + ") -- (1,0);" "\n"
          r"\draw[otNavy,line width=0.9pt] (0,0) -- (1,0);" "\n"
          r"\draw[guide] (" + _n(c) + "," + _n(s) + ") -- (" + _n(c) + ",0);" "\n"
          r"\draw[otNavy,line width=0.6pt] (0.44,0) -- (0.44,0.06) -- (0.5,0.06);" "\n"
          r"\draw[otNavy,line width=0.7pt] (0.2,0) arc (0:60:0.2);" "\n"
          r"\node[text=otNavy,inner sep=1pt,font=\small] at " + _pt(PI / 6, 0.32) + r" {$\frac{\pi}{3}$};" "\n"
          r"\fill[otNavy] (0.5,0) circle (1.6pt);" "\n"
          r"\node[anchor=north,inner sep=2pt,text=otInk] at (0.5,-0.02) {$H$};")
    return cercle(R=2.6, points=[(PI / 3, r"$M\left(\dfrac{\pi}{3}\right)$", N)], avant=av)


def _pi4():
    """Exercice 1385 Q2 : M(π/4) sur la droite y = x, coordonnées √2/2."""
    a = math.sqrt(2) / 2
    av = (r"\draw[otRule,line width=0.7pt,dash pattern=on 3pt off 2pt] (-0.62,-0.62) -- (0.7071,0.7071);" "\n"
          r"\node[note,anchor=north west] at (-0.4,-0.47) {$y=x$};" "\n"
          r"\draw[guide] " + _pt(PI / 4) + " -- (" + _n(a) + ",0);" "\n"
          r"\draw[guide] " + _pt(PI / 4) + " -- (0," + _n(a) + ");" "\n"
          r"\fill[otGreenDark] (" + _n(a) + ",0) circle (1.6pt);" "\n"
          r"\fill[otGreenDark] (0," + _n(a) + ") circle (1.6pt);" "\n"
          r"\node[anchor=north,inner sep=2pt,text=otGreenDark] at (" + _n(a) + r",-0.03) {$\dfrac{\sqrt{2}}{2}$};" "\n"
          r"\node[anchor=east,inner sep=2pt,text=otGreenDark] at (-0.03," + _n(a) + r") {$\dfrac{\sqrt{2}}{2}$};")
    return cercle(R=2.4, points=[(PI / 4, r"$M\left(\dfrac{\pi}{4}\right)$", V, "south west", 0.05)], avant=av, J=False)


def _pi6():
    """Exercice 1385 Q4 : M(π/6) et ses symétriques M(−π/6) et M(5π/6)."""
    av = (r"\draw[guide] " + _pt(PI / 6) + " -- " + _pt(-PI / 6) + ";" "\n"
          r"\draw[guide] " + _pt(PI / 6) + " -- " + _pt(5 * PI / 6) + ";")
    pts = [(PI / 6, r"$M\left(\dfrac{\pi}{6}\right)$", N),
           (-PI / 6, r"$M\left(-\dfrac{\pi}{6}\right)$", V),
           (5 * PI / 6, r"$M\left(\dfrac{5\pi}{6}\right)$", V)]
    return cercle(R=2.4, points=pts, avant=av)


def _droite_cos(a, t1, t2, lab_a, l1, l2, R=2.3, cote_a="north west"):
    """Droite verticale d'abscisse a et ses deux points d'intersection avec le cercle."""
    dx = 0.02 if "west" in cote_a else -0.02
    return cercle(
        R=R,
        avant=(r"\draw[seuil] (" + _n(a) + ",-1.0) -- (" + _n(a) + ",1.0);" "\n"
               r"\node[anchor=" + cote_a + ",inner sep=1.5pt,text=otOrange!80!black] at (" + _n(a + dx) + ",-0.02) {" + lab_a + "};"),
        points=[(t1, l1, V), (t2, l2, V)],
    )


def _droite_sin(b, t1, t2, lab_b, l1, l2, R=2.3):
    """Droite horizontale d'ordonnée b (étiquette à gauche de la droite) et ses deux points d'intersection."""
    return cercle(
        R=R,
        avant=(r"\draw[seuil] (-1.0," + _n(b) + ") -- (1.0," + _n(b) + ");" "\n"
               r"\node[anchor=east,inner sep=1.5pt,text=otOrange!80!black] at (-1.03," + _n(b) + ") {" + lab_b + "};"),
        points=[(t1, l1, V), (t2, l2, V)], J=False,
    )


EX1390_COURBE = r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8.2cm, height=5.0cm, xmin=-3.75, xmax=7.2, ymin=-1.9, ymax=6.1,
  xtick={-3.1416,-1.5708,1.5708,3.1416,4.7124,6.2832}, xticklabels={},
  ytick={-1,1,2,3,4,5}, yticklabels={$-1$,$1$,,$3$,$4$,$5$}]
  \draw[seuil] (axis cs:-3.6,3.5) -- (axis cs:6.6,3.5);
  \addplot[courbe, domain=-3.1416:6.2832] {3*sin(x)+2};
  \guidev{0.5236}{3.5} \guidev{2.618}{3.5}
  \draw[guide] (axis cs:1.5708,5) -- (axis cs:0,5);
  \pnt{0}{2} \pnt{1.5708}{5} \pnt{-1.5708}{-1}
  \pnt[otGreenDark]{0.5236}{3.5} \pnt[otGreenDark]{2.618}{3.5}
  \node[etiq, fill=none, anchor=south east] at (axis cs:-0.12,2.1) {$A$};
  \node[note, fill=none, anchor=west, text=otOrange!80!black] at (axis cs:6.65,3.5) {$y = \frac{7}{2}$};
  \node[note, fill=none, anchor=north] at (axis cs:-1.5708,-1.15) {minimum $-1$};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:-3.6,2.85) {$\mathcal{C}_g$};
\end{axis}
\end{tikzpicture}"""


def ex1386_points():
    pts = [(7 * PI / 6, F(r"7\pi", "6"), V, "east", 0.07),
           (3 * PI / 4, F(r"3\pi", "4"), V),
           (11 * PI / 6, F(r"11\pi", "6"), V),
           (-PI / 3, F(r"\pi", "3", "-"), V)]
    return cercle(R=2.6, ticks=TICKS, points=pts)


def ex1391_symetrie():
    av = (r"\draw[guide] " + _pt(PI / 5) + " -- " + _pt(4 * PI / 5) + ";" "\n"
          r"\draw[guide] " + _pt(2 * PI / 5) + " -- " + _pt(3 * PI / 5) + ";" "\n"
          r"\draw[otGreenDark,line width=0.7pt,dash pattern=on 2pt off 1.6pt] " + _pt(PI / 5) + " -- (" + _n(math.cos(PI / 5)) + ",0);" "\n"
          r"\draw[otGreenDark,line width=0.7pt,dash pattern=on 2pt off 1.6pt] " + _pt(4 * PI / 5) + " -- (" + _n(math.cos(4 * PI / 5)) + ",0);" "\n"
          r"\fill[otGreenDark] (" + _n(math.cos(PI / 5)) + ",0) circle (1.6pt);" "\n"
          r"\fill[otGreenDark] (" + _n(math.cos(4 * PI / 5)) + ",0) circle (1.6pt);")
    pts = [(PI / 5, F(r"\pi", "5"), N), (2 * PI / 5, F(r"2\pi", "5"), N),
           (3 * PI / 5, F(r"3\pi", "5"), V), (4 * PI / 5, F(r"4\pi", "5"), V)]
    return cercle(R=2.6, points=pts, avant=av, J=False)


# Grande roue, corrigé : positions à 21 m (θ = 2π/3 et 4π/3), arc où h ≥ 21 m
X21 = math.sqrt(144 - 36)
ROUE_CORRIGE = (
    r"\begin{tikzpicture}[x=0.19cm,y=0.19cm,line cap=round,line join=round]" "\n"
    r"\fill[otRule!60] (-18,-1.3) rectangle (18,0);" "\n"
    r"\draw[otInk,line width=0.8pt] (-18,0) -- (18,0);" "\n"
    r"\draw[otMuted,line width=1.1pt] (-6.5,0) -- (0,15) -- (6.5,0);" "\n"
    r"\draw[otNavy,line width=1.1pt] (0,15) circle (12);" "\n"
    r"\draw[otGreen,line width=3.4pt,line cap=butt] (" + _n(X21) + ",21) arc (30:150:12);" "\n"
    r"\draw[seuil] (-14.5,21) -- (14.5,21);" "\n"
    r"\draw[guide] (0,15) -- (0,3);" "\n"
    r"\draw[otNavy,line width=0.8pt] (0,15) -- (" + _n(X21) + ",21);" "\n"
    r"\draw[otNavy,line width=0.8pt] (0,15) -- (" + _n(-X21) + ",21);" "\n"
    r"\draw[otGreenDark,line width=0.8pt,-{Stealth[length=1.8mm]}] (0,11.2) arc (-90:30:3.8);" "\n"
    r"\node[text=otGreenDark,inner sep=1pt,anchor=west] at (4.2,13.2) {$\dfrac{2\pi}{3}$};" "\n"
    r"\draw[cote] (16.5,0) -- (16.5,21) node[midway,coteTexte] {$21$ m};" "\n"
    r"\draw[otMuted!70,line width=.4pt] (14.6,21) -- (17.2,21);" "\n"
    r"\fill[otNavy] (0,15) circle (2pt);" "\n"
    r"\node[anchor=north east,inner sep=1.5pt,text=otInk] at (-0.3,14.6) {$C$};" "\n"
    r"\fill[otNavy] (0,3) circle (2pt);" "\n"
    r"\node[anchor=north west,inner sep=1.5pt,text=otInk] at (0.3,2.8) {$B$};" "\n"
    r"\fill[otGreenDark] (" + _n(X21) + ",21) circle (2.6pt);" "\n"
    r"\fill[otGreenDark] (" + _n(-X21) + ",21) circle (2.6pt);" "\n"
    r"\node[anchor=south west,inner sep=1.5pt,text=otGreenDark] at (" + _n(X21 + 0.8) + r",21.5) {$\theta = \dfrac{2\pi}{3}$};" "\n"
    r"\node[anchor=south east,inner sep=1.5pt,text=otGreenDark] at (" + _n(-X21 - 0.8) + r",21.5) {$\theta = \dfrac{4\pi}{3}$};" "\n"
    r"\node[note,anchor=south,text=otGreenDark] at (0,27.6) {$h \geq 21$ m sur l’arc vert};" "\n"
    r"\node[note,anchor=north west] at (-17.5,-1.6) {sol};" "\n"
    r"\end{tikzpicture}"
)

EX1388_COURBE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=5.2cm, xmin=-0.15, xmax=2.3, ymin=-3.5, ymax=33.5,
  xtick={0.6667,1,1.3333,2}, xticklabels={}, ytick={3,9,15,21,27}, xlabel={$t$}, ylabel={$h$}]
  \sol{0.6667}{1.3333}
  \draw[seuil] (axis cs:0,21) -- (axis cs:2.05,21);
  \addplot[courbe, domain=0:2] {15-12*cos(deg(pi*x))};
  \guidev{0.6667}{21} \guidev{1.3333}{21}
  \pnt[otGreenDark]{0.6667}{21} \pnt[otGreenDark]{1.3333}{21}
  \pnt{0}{3} \pnt{1}{27} \pnt{2}{3}
  \node[note, fill=none, anchor=west, text=otOrange!80!black] at (axis cs:2.07,21) {$21$ m};
  \node[note, fill=none, anchor=north west, text=otGreenDark] at (axis cs:0.1,33) {$h \geq 21$ m pendant $40$ s};
  \node[etiq, fill=none, text=otNavy, anchor=west] at (axis cs:1.75,12) {$\mathcal{C}_h$};
\end{axis}
\end{tikzpicture}"""


def archimede_corrige():
    """Triangle OHA rectangle en H, triangle AHC : longueurs du corrigé (cas général)."""
    R = 4.5
    a = math.radians(50)
    ca, sa = math.cos(a), math.sin(a)
    s = [r"\begin{tikzpicture}[x=" + str(R) + "cm,y=" + str(R) + "cm,line cap=round,line join=round]"]
    s.append(r"\draw[otNavy,line width=1pt] " + _pt(-a - 0.12) + " arc (" + f"{math.degrees(-a - 0.12):.2f}" + ":" + f"{math.degrees(a + 0.12):.2f}" + ":1);")
    s.append(r"\draw[otMuted,line width=0.6pt] (0,0) -- " + _pt(a) + ";")
    s.append(r"\draw[otNavy,line width=1.2pt] " + _pt(-a) + " -- " + _pt(a) + ";")
    s.append(r"\draw[otNavy,line width=0.9pt] (0,0) -- " + _pt(-a) + ";")
    s.append(r"\draw[otNavy,line width=0.9pt] (0,0) -- (" + _n(ca) + ",0);")
    s.append(r"\draw[otGreenDark,line width=1.6pt] (" + _n(ca) + ",0) -- (1,0);")
    s.append(r"\draw[otGreenDark,line width=1.6pt] " + _pt(-a) + " -- (1,0);")
    s.append(r"\draw[otNavy,line width=0.6pt] (" + _n(ca + 0.045) + ",0) -- (" + _n(ca + 0.045) + ",-0.045) -- (" + _n(ca) + ",-0.045);")
    s.append(r"\draw[otGreenDark,line width=0.7pt] (0.2,0) arc (0:" + f"{-math.degrees(a):.2f}" + ":0.2);")
    s.append(r"\node[text=otGreenDark,inner sep=1pt] at " + _pt(-a / 2, 0.3) + r" {$\frac{\pi}{n}$};")
    s.append(r"\fill[otNavy] (0,0) circle (1.8pt);")
    s.append(r"\node[anchor=east,inner sep=2pt,text=otInk] at (-0.01,0) {$O$};")
    s.append(r"\fill[otNavy] " + _pt(-a) + " circle (2pt);")
    s.append(r"\node[anchor=north,inner sep=2pt,text=otInk] at " + _pt(-a, 1.02) + " {$A$};")
    s.append(r"\fill[otNavy] " + _pt(a) + " circle (2pt);")
    s.append(r"\node[anchor=south,inner sep=2pt,text=otInk] at " + _pt(a, 1.02) + " {$B$};")
    s.append(r"\fill[otGreenDark] (1,0) circle (2pt);")
    s.append(r"\node[anchor=west,inner sep=2pt,text=otGreenDark] at (1.01,0) {$C$};")
    s.append(r"\fill[otNavy] (" + _n(ca) + ",0) circle (1.6pt);")
    s.append(r"\node[anchor=south east,inner sep=1.5pt,text=otInk] at (" + _n(ca - 0.012) + ",0.012) {$H$};")
    s.append(r"\node[anchor=south,inner sep=2pt,text=otNavy,font=\small] at (" + _n(ca / 2 + 0.04) + r",0.01) {$OH$};")
    s.append(r"\node[anchor=south,inner sep=2pt,text=otGreenDark,font=\small] at (" + _n((ca + 1) / 2) + r",0.01) {$1 - OH$};")
    s.append(r"\node[anchor=east,inner sep=2pt,text=otGreenDark] at (" + _n(ca - 0.012) + "," + _n(-sa / 2) + r") {$\frac{c}{2}$};")
    s.append(r"\node[text=otGreenDark,inner sep=1pt] at (" + _n(ca + 0.13) + "," + _n(-sa / 2 + 0.12) + r") {$c'$};")
    s.append(r"\node[anchor=north east,inner sep=2pt,text=otMuted] at " + _pt(-a, 0.5) + " {$1$};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


NOUVEAU2_CORRIGE = courbes(
    r"""  \draw[seuil] (axis cs:-6.9,0.3) -- (axis cs:7.1,0.3);
  \node[note, fill=none, anchor=west, text=otOrange!80!black] at (axis cs:7.15,0.3) {$y = 0{,}3$};
  \pnt[otOrange!85!black]{-5.9785}{0.3} \pnt[otOrange!85!black]{-3.4463}{0.3}
  \pnt[otOrange!85!black]{0.3047}{0.3} \pnt[otOrange!85!black]{2.8369}{0.3}
""",
    r"""  \guidev{-5.4978}{0.7071} \guidev{-2.3562}{-0.7071} \guidev{0.7854}{0.7071} \guidev{3.927}{-0.7071}
  \pnt[otGreenDark]{-5.4978}{0.7071} \pnt[otGreenDark]{-2.3562}{-0.7071}
  \pnt[otGreenDark]{0.7854}{0.7071} \pnt[otGreenDark]{3.927}{-0.7071}
""",
    r"$\mathcal{C}_1$", r"$\mathcal{C}_2$")

FIGURES.update({
    "ex1385_enonce": _pi3(False),
    "ex1385_pi4": _pi4(),
    "ex1385_pi6": _pi6(),
    "ex1386_points": ex1386_points(),
    "ex1387_moins_demi": _droite_cos(-0.5, 2 * PI / 3, -2 * PI / 3, r"$-\dfrac{1}{2}$",
                                     F(r"2\pi", "3"), F(r"2\pi", "3", "-"), cote_a="north east"),
    "ex1392_vierge": cercle(R=2.6, ticks=TICKS),
    "ex1390_sin": _droite_sin(math.sqrt(3) / 2, PI / 3, 2 * PI / 3, r"$\dfrac{\sqrt{3}}{2}$",
                              F(r"\pi", "3"), F(r"2\pi", "3")),
    "ex1390_cos": _droite_cos(-math.sqrt(2) / 2, 3 * PI / 4, -3 * PI / 4, r"$-\dfrac{\sqrt{2}}{2}$",
                              F(r"3\pi", "4"), F(r"3\pi", "4", "-"), cote_a="north west"),
    "ex1390_courbe": EX1390_COURBE,
    "ex1391_symetrie": ex1391_symetrie(),
    "ex1388_roue_corrige": ROUE_CORRIGE,
    "ex1388_courbe": EX1388_COURBE,
    "nouveau1_corrige": archimede_corrige(),
    "nouveau2_corrige": NOUVEAU2_CORRIGE,
})

XLAB = {
    "nouveau2_corrige": [(-6.2832, "d", r"-2\pi"), (-3.1416, "g", r"-\pi"), (3.1416, "g", r"\pi"), (6.2832, "d", r"2\pi")],
    "ex1390_courbe": [(-3.1416, "c", r"-\pi"), (-1.5708, "h", r"-\frac{\pi}{2}"), (0.5236, "c", r"\frac{\pi}{6}"),
                      (2.618, "c", r"\frac{5\pi}{6}"), (4.7124, "h", r"\frac{3\pi}{2}"), (6.2832, "c", r"2\pi")],
    "ex1388_courbe": [(0.6667, "c", r"\frac{2}{3}"), (1, "c", "1"), (1.3333, "c", r"\frac{4}{3}"), (2, "c", "2")],
    "cours_courbes": [(-6.2832, "d", r"-2\pi"), (-3.1416, "g", r"-\pi"), (3.1416, "g", r"\pi"), (6.2832, "d", r"2\pi")],
    "nouveau2_courbes": [(-6.2832, "d", r"-2\pi"), (-3.1416, "g", r"-\pi"), (3.1416, "g", r"\pi"), (6.2832, "d", r"2\pi")],
    "ex1389_courbe": [(-3.1416, "c", r"-\pi"), (3.1416, "h", r"\pi"),
                      (6.2832, "c", r"2\pi"), (9.4248, "h", r"3\pi")],
}
