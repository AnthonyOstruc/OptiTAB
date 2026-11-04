# -*- coding: utf-8 -*-
"""Figures de la notion 159 (Première, géométrie repérée), style des livres OptiTAB.

Compilées par outils/figures_livre.py :
    python figures_livre.py ../chantier/1ere/159_geometrie-reperee-dans-le-plan [nom …]

Repères orthonormés tracés en TikZ pur (fonction repere) : quadrillage clair,
axes gris fléchés, graduations Montserrat sur fond blanc. Points en
\\fill … circle, étiquettes posées dans l'espace libre (ancre choisie à la
main). Couleurs : données en bleu marine, constructions et réponses en vert
foncé, axe de symétrie en orange.
"""
import math

N = "otNavy"
V = "otGreenDark"
O_ = "otOrange"


def f(v):
    return f"{v:.4f}".rstrip("0").rstrip(".")


def repere(xmin, xmax, ymin, ymax, corps, u=0.6, uy=None, xs=None, ys=None, origine="O",
           pas=1):
    """Repère avec quadrillage. xs / ys : graduations écrites (par défaut tous les entiers non nuls)."""
    uy = uy or u
    if xs is None:
        xs = [k for k in range(math.ceil(xmin), math.floor(xmax) + 1) if k != 0 and k % pas == 0]
    if ys is None:
        ys = [k for k in range(math.ceil(ymin), math.floor(ymax) + 1) if k != 0 and k % pas == 0]
    s = [r"\begin{tikzpicture}[x=" + f(u) + "cm,y=" + f(uy) + r"cm,line cap=round,line join=round,"
         r"grad/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt}]"]
    s.append(r"\draw[otRule!75,line width=0.35pt] (" + f(xmin) + "," + f(ymin) + ") grid (" + f(xmax) + "," + f(ymax) + ");")
    s.append(r"\draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (" + f(xmin) + ",0) -- (" + f(xmax + 0.35) + ",0);")
    s.append(r"\draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (0," + f(ymin) + ") -- (0," + f(ymax + 0.35) + ");")
    s.append(r"\node[anchor=west,text=otMuted,inner sep=2pt] at (" + f(xmax + 0.35) + r",0) {$x$};")
    s.append(r"\node[anchor=south,text=otMuted,inner sep=2pt] at (0," + f(ymax + 0.35) + r") {$y$};")
    for k in xs:
        s.append(r"\draw[otMuted,line width=0.5pt] (" + f(k) + ",0) ++(0,-2.2pt) -- ++(0,4.4pt);")
        s.append(r"\node[grad,anchor=north] at (" + f(k) + r",0) [yshift=-2.6pt] {$" + str(k) + "$};")
    for k in ys:
        s.append(r"\draw[otMuted,line width=0.5pt] (0," + f(k) + ") ++(-2.2pt,0) -- ++(4.4pt,0);")
        s.append(r"\node[grad,anchor=east] at (0," + f(k) + r") [xshift=-2.6pt] {$" + str(k) + "$};")
    if origine:
        s.append(r"\node[anchor=north east,inner sep=1.6pt,text=otInk] at (0,0) {$" + origine + "$};")
    s.append(corps)
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


def pt(x, y, lab="", anc="south west", col=N, nom=None, sep="1.8pt", tc=None):
    """Point (disque plein) + étiquette ; nom = coordonnée TikZ créée."""
    s = ""
    if nom:
        s += r"\coordinate (" + nom + ") at (" + f(x) + "," + f(y) + ");"
    s += r"\fill[" + col + "] (" + f(x) + "," + f(y) + ") circle (2.1pt);"
    if lab:
        s += r"\node[anchor=" + anc + ",inner sep=" + sep + ",text=" + (tc or ("otInk" if col == N else col)) + "] at (" + f(x) + "," + f(y) + ") {" + lab + "};"
    return s + "\n"


def lab(x, y, texte, anc="center", col="otInk"):
    return r"\node[anchor=" + anc + ",inner sep=1.5pt,text=" + col + "] at (" + f(x) + "," + f(y) + ") {" + texte + "};" + "\n"


def droite(a, b, c, box, style="geoTrait", marge=0.0):
    """Segment de la droite ax + by + c = 0 dans la boîte (x0, x1, y0, y1)."""
    x0, x1, y0, y1 = box
    pts = []
    if b != 0:
        for xx in (x0, x1):
            yy = (-c - a * xx) / b
            if y0 - 1e-9 <= yy <= y1 + 1e-9:
                pts.append((xx, yy))
    if a != 0:
        for yy in (y0, y1):
            xx = (-c - b * yy) / a
            if x0 - 1e-9 <= xx <= x1 + 1e-9:
                pts.append((xx, yy))
    uniq = []
    for p in pts:
        if all(abs(p[0] - q[0]) > 1e-6 or abs(p[1] - q[1]) > 1e-6 for q in uniq):
            uniq.append(p)
    (xa, ya), (xb, yb) = uniq[:2]
    return r"\draw[" + style + "] (" + f(xa) + "," + f(ya) + ") -- (" + f(xb) + "," + f(yb) + ");" + "\n"


def courbe(expr, d0, d1, style="courbe", n=120):
    return (r"\draw[" + style + "] plot[domain=" + f(d0) + ":" + f(d1) + ",samples=" + str(n) + r",smooth] (\x,{" + expr + "});" + "\n")


def cercle(a, b, r, style="geoTrait"):
    return r"\draw[" + style + "] (" + f(a) + "," + f(b) + ") circle (" + f(r) + ");" + "\n"


def seg(p, q, style="geoTrait"):
    return r"\draw[" + style + "] (" + f(p[0]) + "," + f(p[1]) + ") -- (" + f(q[0]) + "," + f(q[1]) + ");" + "\n"


def vect(p, q, col=V):
    return r"\draw[" + col + r",line width=1.1pt,-{Stealth[length=2.6mm]}] (" + f(p[0]) + "," + f(p[1]) + ") -- (" + f(q[0]) + "," + f(q[1]) + ");" + "\n"


def angle_droit(nA, nB, nC, t="0.2"):
    return r"\angledroit[" + t + "]{" + nA + "}{" + nB + "}{" + nC + "}" + "\n"


AIDE = "otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt"
REP = "otGreenDark,line width=1.1pt"
AXE = "otOrange,line width=1pt,dash pattern=on 5pt off 3pt"
GUIDE = "otMuted,line width=0.6pt,dash pattern=on 2pt off 1.6pt"

FIGURES = {}

# ================================================================== cours
# I. Vecteur normal : figure sans repère
FIGURES["cours_normal"] = (
    r"\begin{tikzpicture}[x=1cm,y=1cm,line cap=round,line join=round]" "\n"
    r"\coordinate (A) at (2,1.5); \coordinate (M) at ($(A)+(-2.2,-1.1)$); \coordinate (P) at ($(A)+(1.8,0.9)$);" "\n"
    r"\draw[geoTrait] ($(A)+(-3.4,-1.7)$) -- ($(A)+(3.0,1.5)$);" "\n"
    r"\node[anchor=north west,inner sep=2pt,text=otNavy] at ($(A)+(2.6,1.3)$) {$d$};" "\n"
    r"\draw[otOrange,line width=1.3pt,-{Stealth[length=2.6mm]}] (A) -- (P);" "\n"
    r"\node[anchor=north west,inner sep=2pt,text=otOrange!85!black] at ($(A)+(1.25,0.45)$) {$\vec{u}$};" "\n"
    r"\draw[otGreenDark,line width=1.3pt,-{Stealth[length=2.6mm]}] (A) -- ($(A)+(-0.8,1.6)$) coordinate (N);" "\n"
    r"\node[anchor=east,inner sep=2pt,text=otGreenDark] at ($(A)+(-0.75,1.35)$) {$\vec{n}$};" "\n"
    r"\angledroit[0.24]{N}{A}{P}" "\n"
    r"\fill[otNavy] (A) circle (2.1pt); \node[anchor=north west,inner sep=2.5pt] at (A) {$A$};" "\n"
    r"\fill[otNavy] (M) circle (2.1pt); \node[anchor=north west,inner sep=2.5pt] at (M) {$M$};" "\n"
    r"\node[anchor=west,align=left,font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted] at (2.7,-0.6) {$M\in d \iff \overrightarrow{AM}\cdot\vec{n}=0$};" "\n"
    r"\end{tikzpicture}"
)

# II. Projeté orthogonal : M(4;3), d : y = -2x + 4, H(6/5 ; 8/5)
_H = (1.2, 1.6)
FIGURES["cours_projete"] = repere(
    -1.2, 5.2, -1.2, 4.4,
    droite(2, 1, -4, (-0.2, 2.5, -1.0, 4.4))
    + lab(2.5, -0.75, "$d$", "west", "otNavy")
    + seg((4, 3), _H, REP)
    + r"\coordinate (H) at (1.2,1.6); \coordinate (M) at (4,3); \coordinate (D) at (2,0);" "\n"
    + angle_droit("M", "H", "D")
    + pt(4, 3, "$M(4\\,;3)$", "south west")
    + pt(*_H, "$H$", "north east", V, sep="2.5pt")
    + lab(2.75, 2.05, "$MH$", "north west", V),
    u=0.95,
)

# III. Cercle (x-1)^2 + (y+1)^2 = 25, point M, tangente en A(4;3) : 3x + 4y - 24 = 0
FIGURES["cours_cercle"] = repere(
    -4.6, 7.4, -6.6, 5.4,
    cercle(1, -1, 5)
    + seg((1, -1), (-2, 3), "otOrange,line width=1.1pt")
    + lab(-1.0, 0.75, "$r=5$", "north east", "otOrange!85!black")
    + droite(3, 4, -24, (1.6, 7.4, -1.5, 5.4), REP)
    + lab(6.6, 1.5, "$T$", "south west", V)
    + seg((1, -1), (4, 3), "otNavy,line width=0.7pt,dash pattern=on 3pt off 2pt")
    + r"\coordinate (W) at (1,-1); \coordinate (A) at (4,3); \coordinate (T) at (8,0);" "\n"
    + angle_droit("W", "A", "T")
    + pt(1, -1, r"$\Omega(1\,;-1)$", "north west")
    + pt(-2, 3, r"$M(x\,;y)$", "south east")
    + pt(4, 3, "$A(4\\,;3)$", "south west", sep="2.5pt"),
    u=0.62, xs=[-2, 2, 4], ys=[-4, -2, 2], pas=2,
)

# IV. Parabole y = x^2 - 4x + 3
FIGURES["cours_parabole"] = repere(
    -1.2, 6.2, -1.8, 4.4,
    seg((2, -1.8), (2, 4.4), AXE)
    + lab(2.1, 4.2, "axe $x=2$", "north west", "otOrange!85!black")
    + seg((0, 3), (4, 3), GUIDE)
    + courbe(r"\x*\x-4*\x+3", -0.25, 4.25)
    + pt(0, 3, "", col=N) + pt(4, 3, "", col=N)
    + pt(1, 0, "", col=V) + pt(3, 0, "", col=V)
    + pt(2, -1, "", col=V)
    + lab(2.14, -1.12, "$S(2\\,;-1)$", "north west", V)
    + lab(3.55, -1.05, "$y=x^2-4x+3$", "west", "otNavy"),
    u=0.95, xs=[1, 3, 4, 5, 6], ys=[-1, 1, 2, 3],
)

# ================================================================== exercices
# 1409 : M(3;1), Δ : x - 2y + 4 = 0, perpendiculaire 2x + y - 7 = 0, H(2;3)
FIGURES["ex1409_projete"] = repere(
    -1.2, 5.2, -1.2, 5.2,
    droite(1, -2, 4, (-1.2, 2.4, -1.2, 5.2))
    + lab(-0.9, 1.85, r"$\Delta$", "south", "otNavy")
    + droite(2, 1, -7, (1.2, 4.3, -1.2, 5.2), AIDE)
    + lab(1.35, 4.6, "$d$", "west", V)
    + seg((3, 1), (2, 3), REP)
    + r"\coordinate (H) at (2,3); \coordinate (M) at (3,1); \coordinate (Q) at (0,2);" "\n"
    + angle_droit("M", "H", "Q")
    + pt(3, 1, "$M(3\\,;1)$", "west", sep="3pt")
    + pt(2, 3, "$H(2\\,;3)$", "south east", V, sep="2.5pt"),
    u=0.82,
)

# 1411 : P1 : y = 2x^2 - 8x + 5, axe x = 2, S(2;-3), points (1;-1) et (3;-1)
FIGURES["ex1411_symetrie"] = repere(
    -0.8, 4.8, -3.6, 5.4,
    seg((2, -3.6), (2, 5.4), AXE)
    + lab(2.1, 5.2, "$x=2$", "north west", "otOrange!85!black")
    + seg((1, -1), (3, -1), GUIDE)
    + courbe(r"2*\x*\x-8*\x+5", 0, 4)
    + pt(1, -1, "$M$", "east", V, sep="3pt")
    + pt(3, -1, "$M'$", "west", V, sep="3pt")
    + pt(2, -3, "", N)
    + lab(2.14, -3.1, "$S(2\\,;-3)$", "north west", "otInk"),
    u=0.62, xs=[1, 3, 4], ys=[-3, -2, -1, 1, 2, 3, 4, 5],
)

# 1412 : A(0;0), B(3;4), C(-4;3), cercle de centre I(-1/2 ; 7/2), r = 5√2/2
_r1412 = 5 * math.sqrt(2) / 2
FIGURES["ex1412_triangle"] = repere(
    -5.2, 4.2, -1.2, 7.6,
    cercle(-0.5, 3.5, _r1412, REP)
    + r"\draw[geoTrait,fill=otSky,fill opacity=0.5] (0,0) -- (3,4) -- (-4,3) -- cycle;" "\n"
    + r"\coordinate (A) at (0,0); \coordinate (B) at (3,4); \coordinate (C) at (-4,3);" "\n"
    + angle_droit("B", "A", "C")
    + pt(0, 0, "")
    + pt(3, 4, "$B$", "west", sep="3pt")
    + pt(-4, 3, "$C$", "east", sep="3pt")
    + pt(-0.5, 3.5, "$I$", "north", V, sep="3pt"),
    u=0.62, origine="A", xs=[-4, -2, 2, 4], ys=[2, 6], pas=2,
)

# 1422 : A(-1;5), B(1;-3), C(4;0), cercle Ω(0;1) r = √17, H(8/17 ; -15/17), parabole y = x² - 4x
_H22 = (8 / 17, -15 / 17)
FIGURES["ex1422_configuration"] = repere(
    -5.0, 5.6, -4.4, 6.2,
    cercle(0, 1, math.sqrt(17), REP)
    + r"\draw[geoTrait] (-1,5) -- (1,-3) -- (4,0) -- cycle;" "\n"
    + seg((4, 0), _H22, AIDE)
    + r"\coordinate (A) at (-1,5); \coordinate (B) at (1,-3); \coordinate (C) at (4,0); \coordinate (H) at (" + f(_H22[0]) + "," + f(_H22[1]) + ");" "\n"
    + angle_droit("A", "C", "B")
    + angle_droit("C", "H", "B", "0.18")
    + pt(-1, 5, "$A$", "south east", sep="2.5pt")
    + pt(1, -3, "$B$", "north west", sep="2.5pt")
    + pt(4, 0, "$C$", "north west", sep="2.5pt")
    + pt(*_H22, "$H$", "north east", V, sep="2pt")
    + pt(0, 1, r"$\Omega$", "north east", V, sep="2.5pt")
    + lab(-2.9, -2.6, r"$\mathcal{C}$", "north east", V),
    u=0.7, xs=[-2, 2], ys=[-4, -2, 6], pas=2,
)

# 1421 : cercle Ω(3;-2) R = 5, A(8;-2), T : x = 8, B(3;5), C(1;-3), hauteur x + 4y = 0, H(28/17 ; -7/17)
_H21 = (28 / 17, -7 / 17)
FIGURES["ex1421_configuration"] = repere(
    -2.6, 9.6, -7.6, 6.0,
    cercle(3, -2, 5)
    + seg((8, -7.6), (8, 6.0), REP)
    + lab(8.1, 5.8, "$T$", "north west", V)
    + r"\draw[geoTrait,line width=0.8pt] (8,-2) -- (3,5) -- (1,-3) -- cycle;" "\n"
    + seg((8, -2), _H21, AIDE)
    + r"\coordinate (A) at (8,-2); \coordinate (B) at (3,5); \coordinate (C) at (1,-3); \coordinate (W) at (3,-2); \coordinate (H) at (" + f(_H21[0]) + "," + f(_H21[1]) + ");" "\n"
    + angle_droit("W", "A", "B", "0.22")
    + angle_droit("A", "H", "B", "0.18")
    + seg((3, -2), (8, -2), "otNavy,line width=0.7pt,dash pattern=on 3pt off 2pt")
    + pt(8, -2, "$A$", "north west", sep="2.5pt")
    + pt(3, 5, "$B$", "south east", sep="2.5pt")
    + pt(1, -3, "$C$", "north east", sep="2.5pt")
    + pt(3, -2, r"$\Omega$", "north", sep="3pt")
    + pt(*_H21, "", col=V)
    + lab(1.95, -0.75, "$H$", "north west", V)
    + lab(-1.3, -5.7, r"$\mathcal{C}$", "north east", "otNavy"),
    u=0.55, xs=[4, 6], ys=[-4, -2, 4], pas=2,
)

# 1414 : cercle Ω(2;-1) R = 5, A(5;3), tangente 3x + 4y - 27 = 0, M(7;4)
FIGURES["ex1414_tangente"] = repere(
    -3.6, 9.6, -6.6, 6.6,
    cercle(2, -1, 5)
    + droite(3, 4, -27, (0.6, 9.6, -6.6, 6.6), REP)
    + lab(1.6, 5.9, "$T$", "south west", V)
    + seg((2, -1), (5, 3), "otNavy,line width=0.7pt,dash pattern=on 3pt off 2pt")
    + seg((2, -1), (7, 4), "otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt")
    + r"\coordinate (W) at (2,-1); \coordinate (A) at (5,3); \coordinate (T) at (9,0);" "\n"
    + angle_droit("W", "A", "T")
    + pt(2, -1, r"$\Omega$", "north", sep="3pt")
    + pt(5, 3, "$A$", "south west", sep="2.5pt")
    + pt(7, 4, "$M$", "south west", "otOrange", sep="2.5pt", tc="otOrange!85!black")
    + lab(-2.4, -4.7, r"$\mathcal{C}$", "north east", "otNavy"),
    u=0.55, xs=[-2, 2, 4, 6, 8], ys=[-6, -4, -2, 2, 4, 6], pas=2,
)

# 1413 : Δ : 2x + 3y - 6 = 0, M(4;1), d : 3x - 2y - 10 = 0, H(42/13 ; -2/13), A(3;0), B(0;2)
_H13 = (42 / 13, -2 / 13)
FIGURES["ex1413_projete"] = repere(
    -1.4, 5.6, -1.6, 3.8,
    r"\fill[otSky] (4,1) -- (3,0) -- (0,2) -- cycle;" "\n"
    + droite(2, 3, -6, (-1.4, 5.0, -1.4, 3.8))
    + lab(-1.2, 3.65, r"$\Delta$", "north west", "otNavy")
    + droite(3, -2, -10, (2.6, 5.4, -1.6, 3.6), AIDE)
    + lab(5.3, 3.25, "$d$", "east", V)
    + seg((4, 1), _H13, REP)
    + r"\draw[otNavy,line width=0.6pt] (4,1) -- (3,0); \draw[otNavy,line width=0.6pt] (4,1) -- (0,2);" "\n"
    + r"\coordinate (H) at (" + f(_H13[0]) + "," + f(_H13[1]) + "); \\coordinate (M) at (4,1); \\coordinate (P) at (0,2);" "\n"
    + angle_droit("M", "H", "P", "0.18")
    + pt(4, 1, "$M$", "west", sep="3pt")
    + pt(3, 0, "", N)
    + lab(2.85, -0.05, "$A$", "north east")
    + pt(0, 2, "$B$", "south west", sep="2.5pt")
    + pt(*_H13, "", col=V)
    + lab(3.33, -0.4, "$H$", "north", V),
    u=0.95, xs=[-1, 1, 2, 4, 5], ys=[-1, 1, 2, 3],
)

# 1418 : y = x^2 - 6x + 8
FIGURES["ex1418_parabole"] = repere(
    -0.8, 6.8, -1.8, 8.8,
    seg((3, -1.8), (3, 8.8), AXE)
    + lab(3.1, 8.6, "$x=3$", "north west", "otOrange!85!black")
    + courbe(r"\x*\x-6*\x+8", -0.05, 6.05)
    + pt(2, 0, "", col=V) + pt(4, 0, "", col=V)
    + pt(3, -1, "", N)
    + lab(3.12, -1.15, "$S(3\\,;-1)$", "north west")
    + pt(0, 8, "$(0\\,;8)$", "west", N, sep="3pt"),
    u=0.95, uy=0.5, xs=[1, 2, 4, 5, 6], ys=[-1, 2, 4, 6, 8],
)

# 1417 : cercle Ω(1;2) R = 3, Δ : x + y - 6 = 0, E(1;5), F(4;2), H(5/2 ; 7/2)
FIGURES["ex1417_intersection"] = repere(
    -2.6, 6.6, -1.6, 6.6,
    cercle(1, 2, 3)
    + droite(1, 1, -6, (-0.2, 6.6, -0.6, 6.4))
    + lab(5.6, 0.9, r"$\Delta$", "south west", "otNavy")
    + seg((1, 2), (2.5, 3.5), AIDE)
    + r"\coordinate (W) at (1,2); \coordinate (H) at (2.5,3.5); \coordinate (F) at (4,2);" "\n"
    + angle_droit("W", "H", "F", "0.18")
    + pt(1, 2, r"$\Omega$", "north", sep="3pt")
    + pt(2.5, 3.5, "", col=V)
    + lab(2.5, 3.05, "$H$", "north", V)
    + pt(1, 5, "$E$", "south west", V, sep="2.5pt")
    + pt(4, 2, "$F$", "south west", V, sep="2.5pt")
    + lab(-1.4, 4.4, r"$\mathcal{C}$", "south east", "otNavy"),
    u=0.62, xs=[-2, 1, 2, 4, 5, 6], ys=[1, 2, 3, 4, 6],
)

# 1416 : A(-1;2), B(3;4), C(1;-2), I(1;3), Ω(2;1), r = √10, médiatrice 2x + y - 5 = 0
FIGURES["ex1416_triangle"] = repere(
    -2.4, 6.2, -2.8, 5.4,
    cercle(2, 1, math.sqrt(10), REP)
    + droite(2, 1, -5, (-0.2, 4.0, -2.8, 5.4), AIDE)
    + lab(3.9, -2.3, "$m$", "west", V)
    + r"\draw[geoTrait] (-1,2) -- (3,4) -- (1,-2) -- cycle;" "\n"
    + r"\coordinate (A) at (-1,2); \coordinate (B) at (3,4); \coordinate (C) at (1,-2); \coordinate (I) at (1,3); \coordinate (W) at (2,1);" "\n"
    + angle_droit("B", "A", "C")
    + angle_droit("A", "I", "W", "0.16")
    + pt(-1, 2, "$A$", "east", sep="3pt")
    + pt(3, 4, "$B$", "south west", sep="2.5pt")
    + pt(1, -2, "$C$", "north east", sep="2.5pt")
    + pt(1, 3, "", col=V) + lab(1.25, 3.3, "$I$", "south", V)
    + pt(2, 1, r"$\Omega$", "south west", V, sep="2.5pt"),
    u=0.72, xs=[-2, 1, 2, 3, 4, 6], ys=[-2, -1, 1, 2, 3, 4],
)

# 1420 : A(1;3), B(5;1), C(3;-1), m1 : 2x - y - 4 = 0, m2 : x - 2y = 0, Ω(8/3 ; 4/3)
_W20 = (8 / 3, 4 / 3)
FIGURES["ex1420_mediatrices"] = repere(
    -0.8, 6.2, -1.8, 4.6,
    cercle(_W20[0], _W20[1], math.sqrt(50) / 3, REP)
    + droite(2, -1, -4, (-0.8, 6.2, -1.8, 4.4), AIDE)
    + lab(4.4, 4.2, "$m_1$", "north west", V)
    + droite(1, -2, 0, (-0.8, 6.2, -0.4, 3.1), AIDE)
    + lab(6.0, 2.8, "$m_2$", "north", V)
    + r"\draw[geoTrait] (1,3) -- (5,1) -- (3,-1) -- cycle;" "\n"
    + pt(1, 3, "$A$", "south east", sep="2.5pt")
    + pt(5, 1, "$B$", "west", sep="3pt")
    + pt(3, -1, "$C$", "north east", sep="2.5pt")
    + pt(3, 2, "", col=V) + lab(2.85, 2.25, "$I_1$", "south", V)
    + pt(2, 1, "", col=V) + lab(1.85, 0.72, "$I_2$", "north", V)
    + pt(*_W20, r"$\Omega$", "south east", V, sep="2pt")
    + lab(-0.05, 0.05, "$O$", "south east"),
    u=0.9, origine="",
)

# 1419 : losange A(1;1), B(5;2), C(4;6), D(0;5), I = H(5/2 ; 7/2)
FIGURES["ex1419_losange"] = repere(
    -0.8, 6.2, -0.8, 6.8,
    r"\draw[geoTrait,fill=otSky,fill opacity=0.5] (1,1) -- (5,2) -- (4,6) -- (0,5) -- cycle;" "\n"
    + seg((1, 1), (4, 6), "otNavy,line width=0.7pt")
    + seg((5, 2), (0, 5), AIDE)
    + r"\coordinate (A) at (1,1); \coordinate (B) at (5,2); \coordinate (I) at (2.5,3.5);" "\n"
    + angle_droit("A", "I", "B", "0.18")
    + pt(1, 1, "$A$", "north east", sep="2.5pt")
    + pt(5, 2, "$B$", "west", sep="3pt")
    + pt(4, 6, "$C$", "south west", sep="2.5pt")
    + pt(0, 5, "$D$", "east", sep="3.5pt")
    + pt(2.5, 3.5, "$I=H$", "east", V, sep="4pt"),
    u=0.8, ys=[1, 2, 3, 4, 6],
)

# 1423 : cercle x² + y² - 6x - 8y = 0 (Ω(3;4), R = 5), A(6;0), B(0;8), tangente en O : 3x + 4y = 0,
#        Δ : 3x + 4y - 50 = 0 tangente en H(6;8), parabole y = -x² + 6x, S(3;9)
FIGURES["ex1423_synthese"] = repere(
    -3.4, 10.4, -3.4, 11.4,
    cercle(3, 4, 5)
    + courbe(r"-\x*\x+6*\x", -0.45, 6.45, "otOrange,line width=1.2pt")
    + lab(6.6, -2.4, r"$\mathcal{P}$", "west", "otOrange!85!black")
    + droite(3, 4, 0, (-3.4, 3.2, -3.4, 2.6), REP)
    + lab(-2.6, 2.2, "$T$", "south west", V)
    + droite(3, 4, -50, (2.6, 10.4, 3.4, 11.4), REP)
    + lab(10.3, 5.1, r"$\Delta$", "south west", V)
    + seg((0, 0), (6, 8), "otNavy,line width=0.7pt,dash pattern=on 3pt off 2pt")
    + seg((3, 9), (3, 4), GUIDE)
    + r"\coordinate (O) at (0,0); \coordinate (W) at (3,4); \coordinate (H) at (6,8); \coordinate (T) at (4,-3); \coordinate (D) at (10,0.5);" "\n"
    + angle_droit("W", "O", "T", "0.22")
    + angle_droit("W", "H", "D", "0.22")
    + pt(0, 0, "", sep="2pt")
    + pt(6, 0, "", N) + lab(5.75, -0.75, "$A$", "north east")
    + pt(0, 8, "$B$", "south east", sep="2.5pt")
    + pt(3, 4, r"$\Omega$", "west", sep="3pt")
    + pt(6, 8, "$H$", "south west", V, sep="3pt")
    + pt(3, 9, "$S$", "south", "otOrange", sep="3pt", tc="otOrange!85!black")
    + lab(-1.0, 8.5, r"$\mathcal{C}$", "south east", "otNavy"),
    u=0.5, xs=[-2, 2, 4, 8, 10], ys=[-2, 2, 4, 6, 10], pas=2,
)

# nouveau-1 : parabole de sommet S(-1;4) passant par A(1;0) : y = -(x+1)² + 4
FIGURES["nouveau1_parabole"] = repere(
    -4.6, 2.6, -2.6, 5.4,
    courbe(r"-(\x+1)*(\x+1)+4", -3.55, 1.55)
    + pt(-1, 4, "$S$", "south", sep="3pt")
    + pt(1, 0, "$A$", "south west", sep="2.5pt")
    + lab(1.75, -1.4, r"$\mathcal{P}$", "west", "otNavy"),
    u=0.82, xs=[-4, -2, -1, 2],
)

# ================================================================== finition 2026-11-02
# --- corrigés qui n'avaient pas de figure
# 1407 Q1 a) et Q2 : Δ1 : 2x + 5y + 4 = 0 par A(3;-2), n1(2;5), E(-2;0) ∈ Δ1
FIGURES["ex1407_delta1"] = repere(
    -3.0, 6.0, -3.4, 3.6,
    droite(2, 5, 4, (-3.0, 6.0, -3.4, 3.6))
    + lab(-2.8, 0.62, r"$\Delta_1$", "south", "otNavy")
    + vect((3, -2), (5, 3))
    + lab(4.15, 0.5, r"$\vec{n}_1$", "west", V)
    + r"\coordinate (A) at (3,-2); \coordinate (N) at (5,3); \coordinate (P) at (8,-4);" "\n"
    + angle_droit("N", "A", "P", "0.2")
    + pt(3, -2, "$A$", "north east", sep="2pt")
    + pt(-2, 0, "$E$", "south west", V, sep="2pt"),
    u=0.62, xs=[1, 2, 3, 4, 5], ys=[-3, -2, -1, 1, 2, 3],
)

# 1407 Q3 : d : 3x - 4y + 1 = 0 dirigée par u(4;3) ; Δ : 4x + 3y - 10 = 0 par M(1;2), perpendiculaire à d
FIGURES["ex1407_perp"] = repere(
    -1.6, 4.6, -1.4, 4.4,
    droite(3, -4, 1, (-1.6, 4.4, -1.4, 4.4))
    + lab(4.0, 3.1, "$d$", "north west", "otNavy")
    + vect((-1, -0.5), (3, 2.5), "otOrange!90!black")
    + lab(-0.5, -0.6, r"$\vec{u}$", "north west", "otOrange!85!black")
    + droite(4, 3, -10, (-0.3, 3.2, -1.2, 4.2), REP)
    + lab(2.9, -0.75, r"$\Delta$", "north east", V)
    + r"\coordinate (K) at (1.48,1.36); \coordinate (M) at (1,2); \coordinate (U) at (3,2.5);" "\n"
    + angle_droit("M", "K", "U", "0.18")
    + pt(1, 2, "$M$", "south west", sep="2pt"),
    u=0.9, xs=[1, 2, 3, 4], ys=[1, 2, 3, 4],
)

# 1410 Q1 a) : cercle C1 de centre Ω1(2;-3) et de rayon 4
_R = 4 / math.sqrt(2)
FIGURES["ex1410_cercle"] = repere(
    -2.6, 6.6, -7.6, 1.8,
    cercle(2, -3, 4)
    + seg((2, -3), (2 + _R, -3 - _R), "otGreenDark,line width=1.1pt")
    + lab(3.55, -4.3, "$r=4$", "south west", V)
    + pt(2, -3, r"$\Omega_1$", "south east", sep="2pt")
    + lab(-1.2, -5.9, r"$\mathcal{C}_1$", "north east", "otNavy"),
    u=0.55, xs=[-2, 2, 4, 6], ys=[-4, -2],
)

# 1408 Q2 : Δ3 : x + 2y - 3 = 0 et Δ4 : 3x - y - 2 = 0 se coupent en K(1;1)
FIGURES["ex1408_intersection"] = repere(
    -1.5, 3.5, -1.5, 3.0,
    droite(1, 2, -3, (-1.5, 3.5, -1.5, 3.0))
    + lab(-1.4, 2.35, r"$\Delta_3$", "south west", "otNavy")
    + droite(3, -1, -2, (-1.5, 3.5, -1.5, 3.0), "otOrange!90!black,line width=.9pt")
    + lab(1.7, 2.9, r"$\Delta_4$", "west", "otOrange!85!black")
    + pt(1, 1, "", col=V)
    + lab(1.19, 0.59, "$K$", "center", V),
    u=0.9, xs=[-1, 1, 2], ys=[-1, 1, 2],
)

# 1408 Q3 : d1 : 3x + 2y - 5 = 0 et d2 : 2x - 3y + 1 = 0, perpendiculaires en (1;1)
FIGURES["ex1408_perp"] = repere(
    -1.5, 3.5, -1.5, 3.0,
    droite(3, 2, -5, (-0.4, 3.5, -1.5, 3.0))
    + lab(0.15, 3.0, "$d_1$", "north west", "otNavy")
    + droite(2, -3, 1, (-1.5, 3.5, -1.5, 3.0), "otOrange!90!black,line width=.9pt")
    + lab(3.4, 2.55, "$d_2$", "north", "otOrange!85!black")
    + r"\coordinate (K) at (1,1); \coordinate (P) at (2.5,2); \coordinate (Q) at (2,-0.5);" "\n"
    + r"\draw[otGreenDark,line width=0.8pt] ($(K)!0.3cm!(P)$) -- ($($(K)!0.3cm!(P)$)+($(K)!0.3cm!(Q)$)-(K)$) -- ($(K)!0.3cm!(Q)$);" "\n"
    + pt(1, 1, ""),
    u=0.9, xs=[1, 2], ys=[-1, 1, 2],
)

# 1406 Q3 : Δ par A(2;-1), vecteur directeur v(4;3), vecteur normal n(3;-4) : 3x - 4y - 10 = 0
FIGURES["ex1406_normal"] = repere(
    -1.0, 6.6, -5.6, 2.8,
    droite(3, -4, -10, (-1.0, 6.6, -5.6, 2.8))
    + lab(6.5, 2.1, r"$\Delta$", "north west", "otNavy")
    + vect((2, -1), (6, 2), "otOrange!90!black")
    + lab(3.9, 0.6, r"$\vec{v}$", "south east", "otOrange!85!black")
    + vect((2, -1), (5, -5))
    + lab(3.7, -3.0, r"$\vec{n}$", "west", V)
    + r"\coordinate (A) at (2,-1); \coordinate (U) at (6,2); \coordinate (N) at (5,-5);" "\n"
    + angle_droit("U", "A", "N", "0.22")
    + pt(2, -1, "$A$", "south east", sep="2pt"),
    u=0.55, xs=[4, 6], ys=[-4, -2, 2],
)

# 1415 : f(x) = -2x² + 12x - 10 = -2(x - 3)² + 8, S(3;8), racines 1 et 5, f(2) = f(4) = 6
FIGURES["ex1415_parabole"] = repere(
    -0.6, 6.6, -3.0, 9.6,
    seg((3, -3.0), (3, 9.6), AXE)
    + lab(3.1, -2.4, "$x=3$", "south west", "otOrange!85!black")
    + seg((2, 6), (4, 6), GUIDE)
    + courbe(r"-2*\x*\x+12*\x-10", 0.7, 5.3)
    + pt(1, 0, "", col=V) + pt(5, 0, "", col=V)
    + pt(2, 6, r"$(2\,;6)$", "south east", V, sep="2pt")
    + pt(4, 6, r"$(4\,;6)$", "south west", V, sep="2pt")
    + pt(3, 8, r"$S(3\,;8)$", "south west", sep="2pt"),
    u=0.75, uy=0.42, xs=[2, 4, 6], ys=[2, 4, 6, 8],
)

# nouveau-1 corrigé : y = -(x+1)² + 4 = -x² - 2x + 3, axe x = -1, B(-3;0), C(0;3), C'(-2;3)
FIGURES["nouveau1_corrige"] = repere(
    -4.6, 2.6, -2.6, 5.4,
    seg((-1, -2.6), (-1, 5.4), AXE)
    + lab(-1.1, 5.3, "$x=-1$", "north east", "otOrange!85!black")
    + seg((-2, 3), (0, 3), GUIDE)
    + courbe(r"-(\x+1)*(\x+1)+4", -3.55, 1.55)
    + pt(-1, 4, "$S$", "south west", sep="2pt")
    + pt(1, 0, "$A$", "south west", sep="2.5pt")
    + pt(-3, 0, "$B$", "south east", V, sep="2.5pt")
    + pt(0, 3, "$C$", "south west", V, sep="2pt")
    + pt(-2, 3, "$C'$", "south east", V, sep="2pt")
    + lab(1.75, -1.4, r"$\mathcal{P}$", "west", "otNavy"),
    u=0.82, xs=[-4, -2, 2], ys=[-2, -1, 1, 2, 4, 5],
)

# --- énoncés : les données seules (points, droites, cercles), sans éléments de réponse
FIGURES["ex1409_enonce"] = repere(
    -1.2, 5.2, -1.2, 5.2,
    droite(1, -2, 4, (-1.2, 5.2, -1.2, 5.2))
    + lab(-0.9, 1.85, r"$\Delta$", "south", "otNavy")
    + pt(3, 1, "$M(3\\,;1)$", "west", sep="3pt"),
    u=0.82,
)

FIGURES["ex1413_enonce"] = repere(
    -1.4, 5.6, -1.6, 3.8,
    droite(2, 3, -6, (-1.4, 5.0, -1.4, 3.8))
    + lab(-1.2, 3.65, r"$\Delta$", "north west", "otNavy")
    + pt(4, 1, "$M(4\\,;1)$", "west", sep="3pt"),
    u=0.95, xs=[-1, 1, 2, 3, 4, 5], ys=[-1, 1, 2, 3],
)

FIGURES["ex1417_enonce"] = repere(
    -2.6, 6.6, -1.6, 6.6,
    cercle(1, 2, 3)
    + droite(1, 1, -6, (-0.2, 6.6, -0.6, 6.4))
    + lab(5.6, 0.9, r"$\Delta$", "south west", "otNavy")
    + pt(1, 2, r"$\Omega$", "north", sep="3pt")
    + lab(-1.4, 4.4, r"$\mathcal{C}$", "south east", "otNavy"),
    u=0.62, xs=[-2, 1, 2, 4, 5, 6], ys=[1, 2, 3, 4, 6],
)

FIGURES["ex1412_enonce"] = repere(
    -5.2, 4.2, -1.2, 5.6,
    r"\draw[geoTrait,fill=otSky,fill opacity=0.5] (0,0) -- (3,4) -- (-4,3) -- cycle;" "\n"
    + pt(0, 0, "")
    + pt(3, 4, "$B$", "west", sep="3pt")
    + pt(-4, 3, "$C$", "east", sep="3pt"),
    u=0.62, origine="A", xs=[-4, -2, 2, 4], ys=[2, 4], pas=2,
)

FIGURES["ex1416_enonce"] = repere(
    -2.4, 4.6, -2.8, 5.2,
    r"\draw[geoTrait] (-1,2) -- (3,4) -- (1,-2) -- cycle;" "\n"
    + pt(-1, 2, "$A$", "east", sep="3pt")
    + pt(3, 4, "$B$", "south west", sep="2.5pt")
    + pt(1, -2, "$C$", "north east", sep="2.5pt"),
    u=0.72, xs=[-2, 1, 2, 3, 4], ys=[-2, -1, 1, 2, 3, 4],
)

FIGURES["ex1420_enonce"] = repere(
    -0.8, 6.2, -1.8, 4.6,
    r"\draw[geoTrait] (1,3) -- (5,1) -- (3,-1) -- cycle;" "\n"
    + pt(1, 3, "$A$", "south east", sep="2.5pt")
    + pt(5, 1, "$B$", "west", sep="3pt")
    + pt(3, -1, "$C$", "north east", sep="2.5pt")
    + lab(-0.05, 0.05, "$O$", "south east"),
    u=0.9, origine="",
)

FIGURES["ex1419_enonce"] = repere(
    -0.8, 6.2, -0.8, 6.8,
    r"\draw[geoTrait,fill=otSky,fill opacity=0.5] (1,1) -- (5,2) -- (4,6) -- (0,5) -- cycle;" "\n"
    + pt(1, 1, "$A$", "north east", sep="2.5pt")
    + pt(5, 2, "$B$", "west", sep="3pt")
    + pt(4, 6, "$C$", "south west", sep="2.5pt")
    + pt(0, 5, "$D$", "east", sep="3.5pt"),
    u=0.8, ys=[1, 2, 3, 4, 6],
)

FIGURES["ex1422_enonce"] = repere(
    -2.4, 5.6, -4.0, 6.0,
    r"\draw[geoTrait] (-1,5) -- (1,-3) -- (4,0) -- cycle;" "\n"
    + pt(-1, 5, "$A$", "south east", sep="2.5pt")
    + pt(1, -3, "$B$", "north west", sep="2.5pt")
    + pt(4, 0, "$C$", "north west", sep="2.5pt"),
    u=0.62, xs=[-2, 2], ys=[-2], pas=2,
)
