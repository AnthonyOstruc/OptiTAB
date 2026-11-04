# -*- coding: utf-8 -*-
"""Figures de la notion 84 « Fonctions sinus et cosinus » (Terminale), style des livres.

Compilation (depuis outils/) :
    python figures_livre.py ../chantier/terminale/84_fonction-trigonometriques [nom …] [--planche]

Finition du 2026-11-02 : toutes les figures sont refaites (les anciennes, issues de
figures_pilote.py, étaient encombrées ou portaient sur la fonction tangente, hors
programme). Les cercles trigonométriques sont produits par cercle() : rayon = unité,
étiquettes posées radialement à l'extérieur du cercle, donc jamais sur un trait.
"""
import math

# graduation de l'axe des abscisses placée AU-DESSUS de l'axe, à droite du trait (côté libre des courbes)
PREAMBULE_EXTRA = r"""
\newcommand{\gradHD}[2]{\node[anchor=south west,xshift=1.5pt,yshift=2pt,font=\otRegular\fontsize{9}{10}\selectfont,
  text=otMuted,fill=white,inner sep=1.3pt] at (axis cs:#1,0) {$#2$};}
"""

PI = math.pi
V = "otGreenDark"
N = "otNavy"


def _n(v):
    return f"{v:.4f}"


def _pt(t, r=1.0):
    return "(" + _n(r * math.cos(t)) + "," + _n(r * math.sin(t)) + ")"


def cercle(R=2.4, points=(), ticks=(), avant="", apres="", O=True, I=True, J=True,
           xmin=-1.3, xmax=1.38, ymin=-1.3, ymax=1.38):
    """Cercle trigonométrique (repris de la notion 157 de Première).

    points : tuples (t, étiquette, couleur, ancre|None, écart) ; ancre None =
    radiale (étiquette à l'extérieur, dans la direction du point).
    """
    s = [r"\begin{tikzpicture}[x=" + str(R) + "cm,y=" + str(R) + "cm,line cap=round,line join=round]"]
    s.append(r"\draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (" + _n(xmin) + ",0) -- (" + _n(xmax) + ",0);")
    s.append(r"\draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (0," + _n(ymin) + ") -- (0," + _n(ymax) + ");")
    s.append(avant)
    s.append(r"\draw[otNavy,line width=1pt] (0,0) circle (1);")
    for t in ticks:
        s.append(r"\draw[otMuted,line width=0.55pt] " + _pt(t, 0.955) + " -- " + _pt(t, 1.045) + ";")
    if O:
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


def arc_vert(t1, t2):
    """Arc solution (vert épais) de t1 à t2 (radians, sens direct)."""
    return (r"\draw[otGreen,line width=3pt,line cap=butt] " + _pt(t1) + " arc (" +
            f"{math.degrees(t1):.3f}:{math.degrees(t2):.3f}" + ":1);")


def seuil_h(y, x1=-1.22, x2=1.22):
    return r"\draw[seuil] (" + _n(x1) + "," + _n(y) + ") -- (" + _n(x2) + "," + _n(y) + ");"


def seuil_v(x, y1=-1.2, y2=1.2):
    return r"\draw[seuil] (" + _n(x) + "," + _n(y1) + ") -- (" + _n(x) + "," + _n(y2) + ");"


def lab(x, y, texte, ancre, couleur="otMuted", extra=""):
    return (r"\node[anchor=" + ancre + ",inner sep=1.5pt,text=" + couleur + (("," + extra) if extra else "") +
            "] at (" + _n(x) + "," + _n(y) + ") {" + texte + "};")


def guides(t):
    """Projections pointillées du point M(t) sur les deux axes."""
    c, s = math.cos(t), math.sin(t)
    return (r"\draw[guide] " + _pt(t) + " -- (" + _n(c) + ",0);" "\n"
            r"\draw[guide] " + _pt(t) + " -- (0," + _n(s) + ");")


S3, S2 = math.sqrt(3) / 2, math.sqrt(2) / 2
PI6 = [k * PI / 6 for k in range(12)]
PI4 = [PI / 4 + k * PI / 2 for k in range(4)]

# =============================================================== cours
T_CS = 0.9
C_CERCLE = cercle(
    R=2.5,
    avant=(r"\draw[otNavy,line width=0.9pt] (0,0) -- " + _pt(T_CS) + ";" "\n"
           + guides(T_CS) + "\n"
           r"\draw[otGreenDark,line width=0.7pt,-{Stealth[length=1.6mm]}] (0.24,0) arc (0:" + f"{math.degrees(T_CS):.1f}" + ":0.24);" "\n"
           r"\node[text=otGreenDark,inner sep=1pt] at " + _pt(T_CS / 2, 0.34) + " {$x$};" "\n"
           r"\fill[otNavy] (" + _n(math.cos(T_CS)) + ",0) circle (1.6pt);" "\n"
           r"\fill[otNavy] (0," + _n(math.sin(T_CS)) + ") circle (1.6pt);" "\n"
           + lab(math.cos(T_CS), -0.03, r"$\cos x$", "north", "otGreenDark") + "\n"
           + lab(-0.03, math.sin(T_CS), r"$\sin x$", "east", "otGreenDark")),
    points=[(T_CS, r"$M(x)$", N)],
)

C_INEQ = cercle(
    R=2.4,
    avant=seuil_v(0.5) + "\n" + arc_vert(-PI / 3, PI / 3) + "\n"
    + lab(0.47, -0.03, F("1", "2"), "north east"),
    points=[(PI / 3, F(r"\pi", "3"), V, "south west", 0.08), (-PI / 3, F(r"\pi", "3", "-"), V, "north west", 0.08)],
    I=False,
)

COURS = {
"c_cercle": C_CERCLE,
"c_ineq_cercle": C_INEQ,

"cours_courbes": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8.2cm, height=3.1cm, xmin=-6.9, xmax=7.3, ymin=-1.75, ymax=1.75,
  xtick={-6.2832,-3.1416,3.1416,6.2832}, xticklabels={},
  minor xtick={-4.7124,-1.5708,1.5708,4.7124}, minor grid style={otRule!45,line width=0.3pt}, minor tick length=0pt,
  ytick={-1,1}]
  \addplot[courbe2, domain=-6.9:7.1] {cos(x)};
  \addplot[courbe, domain=-6.9:7.1] {sin(x)};
  \draw[otMuted,line width=0.6pt,{Stealth[length=1.8mm]}-{Stealth[length=1.8mm]}] (axis cs:-4.7124,1.42) -- (axis cs:1.5708,1.42);
  \node[note,anchor=south] at (axis cs:-1.5708,1.47) {période $2\pi$};
  \node[etiq,text=otNavy,anchor=north] at (axis cs:4.7124,-1.12) {$y=\sin x$};
  \node[etiq,text=otGreenDark,anchor=north] at (axis cs:-3.1416,-1.12) {$y=\cos x$};
\end{axis}
\end{tikzpicture}""",

"cours_derivees": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=3.6cm, xmin=-1.2, xmax=4.6, ymin=-1.45, ymax=1.75,
  xtick={1.5708,3.1416}, xticklabels={}, ytick={-1,1}]
  \addplot[courbe, domain=-1.2:4.4] {sin(x)};
  \draw[otOrange,line width=1.1pt] (axis cs:-0.85,-0.85) -- (axis cs:0.85,0.85);
  \draw[otOrange,line width=1.1pt] (axis cs:0.75,1) -- (axis cs:2.39,1);
  \draw[otOrange,line width=1.1pt] (axis cs:2.29,0.85) -- (axis cs:3.99,-0.85);
  \pnt[otGreenDark]{0}{0} \pnt[otGreenDark]{1.5708}{1} \pnt[otGreenDark]{3.1416}{0}
  \node[note,anchor=south east] at (axis cs:-0.12,0.08) {pente $1$};
  \node[note,anchor=south] at (axis cs:1.5708,1.07) {pente $0$};
  \node[note,anchor=south west] at (axis cs:3.05,0.42) {pente $-1$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:-1.15,-0.95) {$y=\sin x$};
\end{axis}
\end{tikzpicture}""",

"cours_etude_sin2x": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=3.4cm, xmin=-3.5, xmax=3.75, ymin=-1.75, ymax=1.75,
  xtick={-3.1416,-1.5708,0.7854,2.3562,3.1416}, xticklabels={}, ytick={-1,1}]
  \addplot[pale, domain=-3.4:0] {sin(2*x)};
  \addplot[pale, domain=3.1416:3.6] {sin(2*x)};
  \addplot[courbe, domain=0:3.1416] {sin(2*x)};
  \guidev{0.7854}{1} \guidev{2.3562}{-1}
  \pnt[otGreenDark]{0.7854}{1} \pnt[otGreenDark]{2.3562}{-1}
  \node[note,anchor=south] at (axis cs:0.7854,1.08) {maximum $1$};
  \node[note,anchor=north] at (axis cs:2.3562,-1.08) {minimum $-1$};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:-2.4,1.05) {$y=\sin(2x)$};
\end{axis}
\end{tikzpicture}""",
}

# =============================================================== 1198 valeurs remarquables
TICKS = sorted(set([round(t, 6) for t in PI6 + PI4]))
EX1198_VIERGE = cercle(
    R=2.5, ticks=TICKS,
    points=[(PI / 6, F(r"\pi", "6"), N), (PI / 4, F(r"\pi", "4"), N), (PI / 3, F(r"\pi", "3"), N),
            (PI, r"$\pi$", N, "south east", 0.03)],
    J=True,
)

_A, _B, _C = 2 * PI / 3, -PI / 4, 7 * PI / 6
EX1198_POINTS = cercle(
    R=2.7, ticks=TICKS,
    avant=(guides(_A) + "\n" + guides(_B) + "\n" + guides(_C) + "\n"
           + lab(-0.475, 0.03, F("1", "2", "-"), "south west", "otGreenDark") + "\n"
           + lab(S2, 0.03, F(r"\sqrt{2}", "2"), "south", "otGreenDark") + "\n"
           + lab(-0.835, -0.03, F(r"\sqrt{3}", "2", "-"), "north west", "otGreenDark") + "\n"
           + lab(0.03, 0.84, F(r"\sqrt{3}", "2"), "north west", "otGreenDark") + "\n"
           + lab(-0.03, -S2, F(r"\sqrt{2}", "2", "-"), "east", "otGreenDark") + "\n"
           + lab(0.03, -0.5, F("1", "2", "-"), "west", "otGreenDark")),
    points=[(_A, F(r"2\pi", "3"), V), (_B, F(r"\pi", "4", "-"), V), (_C, F(r"7\pi", "6"), V)],
    I=False, J=False, O=False,
)

_T5 = -math.acos(3 / 5)
EX1198_Q5 = cercle(
    R=2.4,
    avant=(r"\draw[otNavy,line width=0.9pt] (0,0) -- " + _pt(_T5) + ";" "\n" + guides(_T5) + "\n"
           + lab(0.6, 0.03, F("3", "5"), "south", "otNavy") + "\n"
           + lab(-0.03, -0.8, F("4", "5", "-"), "east", "otGreenDark")),
    points=[(_T5, r"$M(x)$", V)],
)

# =============================================================== 1200 équations
EX1200_Q1 = cercle(
    R=2.4,
    avant=seuil_h(0.5) + "\n" + lab(-0.03, 0.53, F("1", "2"), "south east"),
    points=[(PI / 6, F(r"\pi", "6"), V), (5 * PI / 6, F(r"5\pi", "6"), V)],
)
EX1200_Q2 = cercle(
    R=2.4,
    avant=seuil_v(-S2) + "\n" + lab(-S2 + 0.03, -0.03, F(r"\sqrt{2}", "2", "-"), "north west"),
    points=[(3 * PI / 4, F(r"3\pi", "4"), V), (-3 * PI / 4, F(r"3\pi", "4", "-"), V)],
)
EX1200_Q3 = cercle(
    R=2.4,
    avant=(r"\draw[seuil] (-0.7071,-0.7071) -- (0.7071,0.7071);" "\n"
           + lab(0.5, 0.25, r"$y=x$", "west", "otOrange!80!black") + "\n"
           + lab(-0.02, 0.02, r"$O$", "south east", "otInk")),
    points=[(PI / 4, F(r"\pi", "4"), V), (5 * PI / 4, F(r"5\pi", "4"), V)],
    O=False,
)
EX1200_Q4 = cercle(
    R=2.4,
    avant=(seuil_h(0.5) + "\n" + seuil_h(1, -0.75, 0.75) + "\n"
           + lab(-0.03, 0.53, F("1", "2"), "south east")),
    points=[(PI / 6, F(r"\pi", "6"), V), (5 * PI / 6, F(r"5\pi", "6"), V),
            (PI / 2, F(r"\pi", "2"), V, "south west", 0.04)],
    J=False,
)

# =============================================================== 1205 inéquations sur le cercle
EX1205_Q1 = cercle(
    R=2.4,
    avant=(seuil_h(S3) + "\n" + arc_vert(PI / 3, 2 * PI / 3) + "\n"
           + lab(-0.03, S3 - 0.03, F(r"\sqrt{3}", "2"), "north east")),
    points=[(PI / 3, F(r"\pi", "3"), V), (2 * PI / 3, F(r"2\pi", "3"), V)],
    J=False,
)
EX1205_Q2 = cercle(
    R=2.4,
    avant=(seuil_v(0.5) + "\n" + arc_vert(PI / 3, 5 * PI / 3) + "\n"
           + lab(0.53, -0.03, F("1", "2"), "north west") + "\n"
           + lab(-1.035, 0.07, r"$\pi$ et $-\pi$", "south east", V)),
    points=[(PI / 3, F(r"\pi", "3"), V), (-PI / 3, F(r"\pi", "3", "-"), V), (PI, "", V)],
    I=False,
)

# =============================================================== 1206 suite périodique
_PTS8 = []
for k in range(8):
    t = k * PI / 4
    _PTS8.append((t, "" if k == 0 else f"${k}$", N))
EX1206_Q2 = cercle(
    R=2.3,
    avant=(r"\draw[guide] (-0.7071,0.7071) -- (0.7071,0.7071);" "\n"
           r"\draw[guide] (-0.7071,-0.7071) -- (0.7071,-0.7071);" "\n"
           + lab(1.035, 0.07, r"$n=0$", "south west", N) + "\n"),
    points=[(t, l, c, {0: "south west", 2: "south west", 4: "south east", 6: "north west"}.get(k), 0.04 if k in (0, 2, 4, 6) else 0.06)
            for k, (t, l, c) in enumerate(_PTS8)],
    I=False, J=False, O=False,
)

EXOS_CERCLE = {
    "ex1198_vierge": EX1198_VIERGE,
    "ex1198_points": EX1198_POINTS,
    "ex1198_q5": EX1198_Q5,
    "ex1200_q1": EX1200_Q1,
    "ex1200_q2": EX1200_Q2,
    "ex1200_q3": EX1200_Q3,
    "ex1200_q4": EX1200_Q4,
    "ex1205_q1": EX1205_Q1,
    "ex1205_q2": EX1205_Q2,
    "ex1206_q2": EX1206_Q2,
}

# =============================================================== courbes des exercices
X_2PI = r"xtick={1.5708,3.1416,4.7124,6.2832}, xticklabels={}"
COURBES = {
# ---------------------------------------------------------------- 1199 tangente
"ex1199_tangente": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7.8cm, height=3.6cm, xmin=-0.7, xmax=3.9, ymin=-0.9, ymax=1.75,
  xtick={1.0472,3.1416}, xticklabels={}, ytick={1}]
  \addplot[courbe, domain=-0.6:3.6] {sin(x)};
  \addplot[otGreenDark, line width=1.1pt, domain=-0.45:2.55] {0.5*x+0.86603-0.5236};
  \guidev{1.0472}{0.86603}
  \pnt[otGreenDark]{1.0472}{0.86603}
  \node[etiq,text=otGreenDark,anchor=south east] at (axis cs:1.2,1.12) {$T$};
  \node[etiq,text=otNavy,anchor=north east] at (axis cs:2.3,0.5) {$y=\sin x$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1200 Q5
"ex1200_q5": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=3.2cm, xmin=-0.3, xmax=6.95, ymin=-1.45, ymax=1.7,
  xtick={1.0472,3.1416,5.236,6.2832}, xticklabels={}, ytick={-1,1}, xticklabel style={fill=none}]
  \addplot[courbe2, domain=0:6.2832] {sin(2*x)};
  \addplot[courbe, domain=0:6.2832] {sin(x)};
  \pnt[otGreenDark]{0}{0} \pnt[otGreenDark]{1.0472}{0.86603} \pnt[otGreenDark]{3.1416}{0} \pnt[otGreenDark]{5.236}{-0.86603}
  \pntv{6.2832}{0}
  \draw[guide] (axis cs:3.1416,-0.1) -- (axis cs:3.1416,-0.4);
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1.3pt] at (axis cs:3.1416,-0.42) {$\pi$};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:1.95,1.06) {$y=\sin x$};
  \node[etiq,text=otGreenDark,anchor=north] at (axis cs:3.95,-1.06) {$y=\sin(2x)$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1201 f(x) = cos² x + sin x
"ex1201_courbe": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=3.6cm, xmin=-0.3, xmax=6.95, ymin=-1.35, ymax=1.8,
  xtick={0.5236,1.5708,2.618,4.7124,6.2832}, xticklabels={}, ytick={-1,1.25}, yticklabels={$-1$,$\dfrac54$}]
  \draw[otMuted,line width=0.6pt,dash pattern=on 5pt off 2pt on 1pt off 2pt] (axis cs:1.5708,-1.3) -- (axis cs:1.5708,1.65);
  \addplot[courbe, domain=0:6.2832] {cos(x)^2+sin(x)};
  \draw[guide] (axis cs:0,1.25) -- (axis cs:2.618,1.25);
  \guidev{4.7124}{-1}
  \pnt[otGreenDark]{0.5236}{1.25} \pnt[otGreenDark]{2.618}{1.25} \pnt[otGreenDark]{4.7124}{-1}
  \node[note,anchor=south west] at (axis cs:1.62,1.4) {axe $x=\frac{\pi}{2}$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:4.2,0.45) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

"ex1201_egal1": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=3.6cm, xmin=-0.3, xmax=6.95, ymin=-1.35, ymax=1.8,
  xtick={1.5708,3.1416,4.7124,6.2832}, xticklabels={}, ytick={-1,1}]
  \addplot[courbe, domain=0:6.2832] {cos(x)^2+sin(x)};
  \draw[seuil] (axis cs:0,1) -- (axis cs:6.7,1);
  \guidev{3.1416}{1} \guidev{6.2832}{1}
  \pnt[otGreenDark]{0}{1} \pnt[otGreenDark]{1.5708}{1} \pnt[otGreenDark]{3.1416}{1} \pnt[otGreenDark]{6.2832}{1}
  \node[etiq,text=otOrange!80!black,anchor=south east] at (axis cs:6.7,1.04) {$y=1$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:4.2,0.45) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1202 aire du trapèze
"ex1202_aire": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7cm, height=3.9cm, xmin=-0.12, xmax=1.85, ymin=-0.25, ymax=1.65,
  xlabel={$\theta$}, ylabel={$\mathcal{A}$},
  xtick={0.5236,1.0472,1.5708}, xticklabels={}, ytick={0.5,1}, yticklabels={$0{,}5$,$1$}]
  \addplot[courbe, domain=0:1.5708] {(1+cos(x))*sin(x)};
  \guidev{1.0472}{1.299}
  \pnt[otGreenDark]{1.0472}{1.299} \pnt{0}{0} \pnt{1.5708}{1}
  \node[etiq,text=otGreenDark,anchor=south] at (axis cs:1.0472,1.36) {$\mathcal{A}_{\max}=\dfrac{3\sqrt{3}}{4}$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1203 limites
"lim_sinx_x": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=3.1cm, xmin=-10.2, xmax=10.6, ymin=-0.45, ymax=1.4,
  xtick={-6.2832,-3.1416,3.1416,6.2832}, xticklabels={}, ytick={1}]
  \addplot[courbe, domain=-9.9:-0.01] {sin(x)/x};
  \addplot[courbe, domain=0.01:9.9] {sin(x)/x};
  \pntv[otGreenDark]{0}{1}
  \node[note,anchor=west] at (axis cs:1.6,1.12) {limite $1$ en $0$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:4.3,0.3) {$y=\dfrac{\sin x}{x}$};
\end{axis}
\end{tikzpicture}""",

"lim_1mcos": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=3.3cm, xmin=-7.2, xmax=7.6, ymin=-0.1, ymax=0.68,
  xtick={-6.2832,-3.1416,3.1416,6.2832}, xticklabels={}, ytick={0.5}, yticklabels={$\dfrac{1}{2}$}]
  \addplot[courbe, domain=-7:-0.01] {(1-cos(x))/x^2};
  \addplot[courbe, domain=0.01:7] {(1-cos(x))/x^2};
  \pntv[otGreenDark]{0}{0.5}
  \node[note,anchor=west,text=otGreenDark] at (axis cs:1.5,0.575) {limite $\dfrac{1}{2}$ en $0$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:3.7,0.22) {$y=\dfrac{1-\cos x}{x^2}$};
\end{axis}
\end{tikzpicture}""",

"lim_gendarmes": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=4.4cm, xmin=-0.6, xmax=20.3, ymin=-0.62, ymax=1.12,
  xtick={6.2832,12.566,18.85}, xticklabels={}, ytick={-0.5,0.5}, yticklabels={$-\dfrac{1}{2}$,$\dfrac{1}{2}$}, xticklabel style={fill=none}]
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=1:19.9] {1/x};
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=1.72:19.9] {-1/x};
  \addplot[courbe, domain=0.05:19.9] {sin(x)/x};
  \node[etiq,anchor=west,text=otOrange!80!black] at (axis cs:1.6,0.84) {$y=\dfrac{1}{x}$};
  \node[etiq,anchor=north west,text=otOrange!80!black] at (axis cs:3.0,-0.4) {$y=-\dfrac{1}{x}$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:12.5,0.3) {$y=\dfrac{\sin x}{x}$};
  \node[note,anchor=south east,text=otGreenDark] at (axis cs:20.2,-0.6) {limite $0$ en $+\infty$};
  \draw[guide] (axis cs:6.2832,-0.04) -- (axis cs:6.2832,-0.2);
  \draw[guide] (axis cs:12.566,-0.04) -- (axis cs:12.566,-0.2);
  \draw[guide] (axis cs:18.85,-0.04) -- (axis cs:18.85,-0.2);
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1.3pt] at (axis cs:6.2832,-0.21) {$2\pi$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1.3pt] at (axis cs:12.566,-0.21) {$4\pi$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1.3pt] at (axis cs:18.85,-0.21) {$6\pi$};
\end{axis}
\end{tikzpicture}""",

"lim_comparaison": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7cm, height=4.2cm, xmin=-0.6, xmax=13.2, ymin=-2.6, ymax=15.2,
  xtick={2,4,6,8,10,12}, ytick={5,10}]
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=0:12.8] {x+2};
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=0:12.8] {x-2};
  \addplot[courbe, domain=0:12.8] {x+2*cos(x)};
  \node[etiq,anchor=south east,text=otOrange!80!black] at (axis cs:9.4,11.6) {$y=x+2$};
  \node[etiq,anchor=north west,text=otOrange!80!black] at (axis cs:9.6,6.6) {$y=x-2$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:0.5,14.6) {$y=x+2\cos x$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1204 sin² x : parité et périodicité
"ex1204_enonce": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=2.9cm, xmin=-3.6, xmax=3.85, ymin=-0.3, ymax=1.4,
  xtick={-3.1416,-1.5708,1.5708,3.1416}, xticklabels={}, ytick={1}]
  \addplot[courbe, domain=0:1.5708] {sin(x)^2};
  \pnt{0}{0} \pnt{1.5708}{1}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:1.7,0.85) {$y=\sin^2 x$};
\end{axis}
\end{tikzpicture}""",

"ex1204_corrige": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=3.1cm, xmin=-3.6, xmax=3.85, ymin=-0.3, ymax=1.55,
  xtick={-3.1416,-1.5708,1.5708,3.1416}, xticklabels={}, ytick={1}]
  \addplot[otGreen, line width=1.35pt, domain=-1.5708:0] {sin(x)^2};
  \addplot[otGreen, line width=1.35pt, dash pattern=on 5pt off 2.5pt, domain=1.5708:3.1416] {sin(x)^2};
  \addplot[otGreen, line width=1.35pt, dash pattern=on 5pt off 2.5pt, domain=-3.1416:-1.5708] {sin(x)^2};
  \addplot[courbe, domain=0:1.5708] {sin(x)^2};
  \pnt{1.5708}{1} \pnt[otGreenDark]{-1.5708}{1}
  \node[note,anchor=south] at (axis cs:-0.7854,1.12) {parité};
  \node[note,anchor=south] at (axis cs:2.6,1.12) {période $\pi$};
  \node[note,anchor=south] at (axis cs:-2.6,1.12) {période $\pi$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1205 Q3 et Q5
"ineq_cos2x": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7cm, height=3.4cm, xmin=-0.15, xmax=3.6, ymin=-1.45, ymax=1.6,
  xtick={0.5236,2.618,3.1416}, xticklabels={}, ytick={-1,0.5}, yticklabels={$-1$,$\dfrac{1}{2}$}, yticklabel style={anchor=east,yshift=0pt}]
  \addplot[courbe, domain=0:3.1416] {cos(2*x)};
  \draw[seuil] (axis cs:0,0.5) -- (axis cs:3.45,0.5);
  \guidev{0.5236}{0.5} \guidev{2.618}{0.5}
  \sol{0.5236}{2.618} \borneO{0.5236} \borneO{2.618}
  \node[etiq,text=otNavy,anchor=north] at (axis cs:1.5708,-1.08) {$y=\cos(2x)$};
\end{axis}
\end{tikzpicture}""",

"ex1205_produit": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7.6cm, height=3.6cm, xmin=-0.3, xmax=6.85, ymin=-1.6, ymax=2.1,
  xtick={1.0472,3.1416,5.236,6.2832}, xticklabels={}, ytick={-1,1}]
  \addplot[courbe, domain=0:6.2832] {(2*cos(x)-1)*sin(x)};
  \sol{0}{1.0472} \sol{3.1416}{5.236}
  \borneF{0} \borneF{1.0472} \borneF{3.1416} \borneF{5.236} \borneF{6.2832}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:0.15,2.05) {$y=(2\cos x-1)\sin x$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1206 Q3
"ex1206_suite": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.8cm, height=3.6cm, xmin=-0.6, xmax=21.2, ymin=-0.3, ymax=3.25,
  xlabel={$n$}, ylabel={}, xtick={5,10,15,20}, ytick={1,2,3}]
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=1:20.6, samples=120] {2+1/x};
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=1:20.6, samples=120] {2-1/x};
  \addplot[only marks, mark=*, mark size=1.7pt, otNavy, samples at={1,2,...,20}] {2+sin(deg(x))/x};
  \node[etiq,anchor=south west,text=otOrange!80!black] at (axis cs:3.2,2.42) {$y=2+\dfrac{1}{x}$};
  \node[etiq,anchor=north west,text=otOrange!80!black] at (axis cs:3.2,1.6) {$y=2-\dfrac{1}{x}$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- 1207 intégrales et aires
"ex1207_q1": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7cm, height=3cm, xmin=-0.3, xmax=3.9, ymin=-0.35, ymax=1.4,
  xtick={1.5708,3.1416}, xticklabels={}, ytick={1}]
  \addplot[draw=none, fill=otGreen!30, domain=0:3.1416] {sin(x)} \closedcycle;
  \addplot[courbe, domain=0:3.5] {sin(x)};
  \node[text=otGreenDark,font=\normalsize] at (axis cs:1.5708,0.4) {aire $=2$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:2.45,0.72) {$y=\sin x$};
\end{axis}
\end{tikzpicture}""",

"ex1207_q4": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7.4cm, height=3.2cm, xmin=-0.3, xmax=3.9, ymin=-1.4, ymax=1.5,
  xtick={0.7854,1.5708,2.3562,3.1416}, xticklabels={}, ytick={-1,1}]
  \addplot[draw=none, fill=otGreen!30, domain=0:1.5708] {sin(2*x)} \closedcycle;
  \addplot[draw=none, fill=otOrange!30, domain=1.5708:3.1416] {sin(2*x)} \closedcycle;
  \addplot[courbe, domain=0:3.1416] {sin(2*x)};
  \node[text=otGreenDark] at (axis cs:0.7854,0.38) {$+1$};
  \node[text=otOrange!70!black] at (axis cs:2.3562,-0.38) {$-1$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:2.55,0.72) {$y=\sin(2x)$};
\end{axis}
\end{tikzpicture}""",

"ex1207_enonce": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=3.3cm, xmin=-0.3, xmax=4.7, ymin=-1.45, ymax=1.55,
  xtick={0.7854,1.5708,3.1416,3.927}, xticklabels={}, ytick={-1,1}, xticklabel style={fill=none}]
  \addplot[draw=none, name path=s, domain=0.7854:3.927] {sin(x)};
  \addplot[draw=none, name path=c, domain=0.7854:3.927] {cos(x)};
  \addplot[otSky] fill between[of=s and c];
  \addplot[courbe2, domain=0:4.5] {cos(x)};
  \addplot[courbe, domain=0:4.5] {sin(x)};
  \gradHD{3.1416}{\pi}
  \node[text=otNavy] at (axis cs:2.3,0.38) {$\mathcal{D}$};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:1.5708,1.05) {$y=\sin x$};
  \node[etiq,text=otGreenDark,anchor=north] at (axis cs:3.1416,-1.05) {$y=\cos x$};
\end{axis}
\end{tikzpicture}""",

"ex1207_q5": r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8cm, height=3.3cm, xmin=-0.3, xmax=4.7, ymin=-1.45, ymax=1.55,
  xtick={0.7854,1.5708,3.1416,3.927}, xticklabels={}, ytick={-1,1}, xticklabel style={fill=none}]
  \addplot[draw=none, name path=s, domain=0.7854:3.927] {sin(x)};
  \addplot[draw=none, name path=c, domain=0.7854:3.927] {cos(x)};
  \addplot[otGreen!30] fill between[of=s and c];
  \addplot[courbe2, domain=0:4.5] {cos(x)};
  \addplot[courbe, domain=0:4.5] {sin(x)};
  \guidev{0.7854}{0.70711} \guidev{3.927}{-0.70711}
  \gradHD{3.1416}{\pi}
  \pnt[otGreenDark]{0.7854}{0.70711} \pnt[otGreenDark]{3.927}{-0.70711}
  \node[text=otGreenDark] at (axis cs:2.15,0.3) {$\mathcal{A}=2\sqrt{2}$};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:1.5708,1.05) {$y=\sin x$};
  \node[etiq,text=otGreenDark,anchor=north] at (axis cs:3.1416,-1.05) {$y=\cos x$};
\end{axis}
\end{tikzpicture}""",
}


# =============================================================== 1202 trapèze (géométrie)
def trapeze(theta, corrige=False):
    """Trapèze ABCD inscrit dans le demi-cercle de centre O et de rayon 1."""
    R = 3.0
    c, s = math.cos(theta), math.sin(theta)
    L = [r"\begin{tikzpicture}[x=" + str(R) + "cm,y=" + str(R) + "cm,line cap=round,line join=round]",
         r"\coordinate (O) at (0,0); \coordinate (A) at (-1,0); \coordinate (B) at (1,0);",
         r"\coordinate (C) at (" + _n(c) + "," + _n(s) + r"); \coordinate (D) at (" + _n(-c) + "," + _n(s) + ");",
         r"\coordinate (H) at (" + _n(c) + ",0);",
         r"\fill[otSky] (A) -- (B) -- (C) -- (D) -- cycle;",
         r"\draw[otMuted,line width=0.6pt] (1,0) arc (0:180:1);"]
    if corrige:
        L.append(r"\draw[otGreenDark,line width=0.9pt] (O) -- (C) (O) -- (D);")
    else:
        L.append(r"\draw[otNavy,line width=0.7pt] (O) -- (C);")
        L.append(r"\draw[guide] (C) -- (H);")
        L.append(r"\angledroit[0.16]{C}{H}{B}")
    L.append(r"\draw[geoTrait] (A) -- (B) -- (C) -- (D) -- cycle;")
    if corrige:
        L.append(r"\codage{O}{B} \codage{B}{C} \codage{C}{D} \codage{D}{A} \codage{O}{A} \codage{O}{C} \codage{O}{D}")
    L.append(r"\draw[otGreenDark,line width=0.7pt,-{Stealth[length=1.6mm]}] (0.22,0) arc (0:" + f"{math.degrees(theta):.2f}" + ":0.22);")
    L.append(r"\node[text=otGreenDark,inner sep=1pt] at " + _pt(theta / 2, 0.33) + (r" {$\dfrac{\pi}{3}$};" if corrige else r" {$\theta$};"))
    pts = [("A", "north"), ("B", "north"), ("O", "north"), ("C", "south west"), ("D", "south east")]
    if not corrige:
        pts.append(("H", "north"))
    for nom, anc in pts:
        if nom != "H":
            L.append(r"\fill[otNavy] (" + nom + ") circle (1.8pt);")
        L.append(r"\node[anchor=" + anc + ",inner sep=2.5pt,text=otInk] at (" + nom + ") {$" + nom + "$};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


GEO = {
    "ex1202_enonce": trapeze(1.0),
    "ex1202_optimal": trapeze(PI / 3, corrige=True),
}

FIGURES = {}
FIGURES.update(COURS)
FIGURES.update(EXOS_CERCLE)
FIGURES.update(COURBES)
FIGURES.update(GEO)

# Graduations de l'axe des abscisses placées à la main (côté libre de la courbe) :
# « g » sous l'axe à gauche du trait, « d » à droite, « c » centrée dessous, « h » au-dessus.
P2, P3, P4, P6 = r"\frac{\pi}{2}", r"\frac{\pi}{3}", r"\frac{\pi}{4}", r"\frac{\pi}{6}"
XLAB = {
    "cours_courbes": [(-6.2832, "d", r"-2\pi"), (-3.1416, "g", r"-\pi"), (3.1416, "g", r"\pi"), (6.2832, "d", r"2\pi")],
    "cours_derivees": [(1.5708, "c", P2), (3.1416, "g", r"\pi")],
    "cours_etude_sin2x": [(-3.1416, "d", r"-\pi"), (-1.5708, "g", "-" + P2), (0.7854, "c", P4),
                          (2.3562, "h", r"\frac{3\pi}{4}"), (3.1416, "d", r"\pi")],
    "ex1199_tangente": [(1.0472, "c", P3), (3.1416, "g", r"\pi")],
    "ex1200_q5": [(1.0472, "c", P3), (5.236, "h", r"\frac{5\pi}{3}"), (6.2832, "d", r"2\pi")],
    "ex1201_courbe": [(0.5236, "c", P6), (1.5708, "d", P2), (2.618, "c", r"\frac{5\pi}{6}"),
                      (4.7124, "h", r"\frac{3\pi}{2}"), (6.2832, "c", r"2\pi")],
    "ex1201_egal1": [(1.5708, "c", P2), (3.1416, "c", r"\pi"), (4.7124, "h", r"\frac{3\pi}{2}"), (6.2832, "c", r"2\pi")],
    "ex1202_aire": [(0.5236, "c", P6), (1.0472, "c", P3), (1.5708, "c", P2)],
    "lim_sinx_x": [(-6.2832, "g", r"-2\pi"), (-3.1416, "d", r"-\pi"), (3.1416, "g", r"\pi"), (6.2832, "d", r"2\pi")],
    "lim_1mcos": [(-6.2832, "c", r"-2\pi"), (-3.1416, "c", r"-\pi"), (3.1416, "c", r"\pi"), (6.2832, "c", r"2\pi")],
    "ex1204_enonce": [(-3.1416, "c", r"-\pi"), (-1.5708, "c", "-" + P2), (1.5708, "c", P2), (3.1416, "c", r"\pi")],
    "ex1204_corrige": [(-3.1416, "c", r"-\pi"), (-1.5708, "c", "-" + P2), (1.5708, "c", P2), (3.1416, "c", r"\pi")],
    "ineq_cos2x": [(0.5236, "c", P6), (2.618, "c", r"\frac{5\pi}{6}"), (3.1416, "c", r"\pi")],
    "ex1205_produit": [(1.0472, "g", P3), (3.1416, "d", r"\pi"), (5.236, "g", r"\frac{5\pi}{3}"), (6.2832, "d", r"2\pi")],
    "ex1207_q1": [(1.5708, "c", P2), (3.1416, "g", r"\pi")],
    "ex1207_q4": [(0.7854, "c", P4), (1.5708, "g", P2), (2.3562, "h", r"\frac{3\pi}{4}"), (3.1416, "d", r"\pi")],
    "ex1207_enonce": [(0.7854, "c", P4), (1.5708, "g", P2), (3.927, "h", r"\frac{5\pi}{4}")],
    "ex1207_q5": [(0.7854, "c", P4), (1.5708, "g", P2), (3.927, "h", r"\frac{5\pi}{4}")],
}

# Graduations placées à la main (XLAB) : les étiquettes automatiques de l'axe des abscisses
# sont vides ; sans fond, elles ne laissent plus de petit carré blanc sur la grille ou une courbe.
for _nom in XLAB:
    FIGURES[_nom] = FIGURES[_nom].replace(r"\begin{axis}[", r"\begin{axis}[xticklabel style={fill=none}, ", 1)
