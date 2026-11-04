# -*- coding: utf-8 -*-
"""Figures de la notion « Résoudre des problèmes de géométrie » (Seconde), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = éléments
de réponse, orange = angles et constructions d'aide. Repères : quadrillage pâle,
axes gris, graduations Montserrat. Étiquettes posées dans l'espace libre
(ancre = direction opposée au décalage).
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grille/.style={otRule!75,line width=.35pt},
  grad/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt},
  lab/.style={text=otInk,inner sep=0pt},
  aide/.style={otMuted,line width=.65pt,dash pattern=on 3pt off 2pt},
  aideV/.style={otGreenDark,line width=.85pt,dash pattern=on 3.5pt off 2pt},
  cache/.style={otNavy,line width=.6pt,dash pattern=on 2.5pt off 2pt},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt},
}
"""


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


def repere(x0, x1, y0, y1, xt=(), yt=(), origine=True, noms=True):
    """Quadrillage [x0;x1]×[y0;y1], axes, graduations étiquetées xt / yt."""
    # step=1 (sans unité) : un carreau = une unité du repère, quel que soit x=U cm
    # (le pas par défaut de « grid » est 1 cm, décalé du repère dès que U ≠ 1).
    s = [r"\draw[grille,step=1] (%s,%s) grid (%s,%s);" % (f(x0), f(y0), f(x1), f(y1))]
    s.append(r"\draw[axe] (%s,0) -- (%s,0);" % (f(x0), f(x1 + .5)))
    s.append(r"\draw[axe] (0,%s) -- (0,%s);" % (f(y0), f(y1 + .5)))
    # pas de graduation sur l'extrémité de départ d'un axe
    for k in range(int(math.ceil(x0)), int(x1) + 1):
        if k and k != x0:
            s.append(r"\draw[otMuted,line width=.5pt] (%d,-.07) -- (%d,.07);" % (k, k))
    for k in range(int(math.ceil(y0)), int(y1) + 1):
        if k and k != y0:
            s.append(r"\draw[otMuted,line width=.5pt] (-.07,%d) -- (.07,%d);" % (k, k))
    for k in xt:
        s.append(r"\node[grad,anchor=north] at (%d,-.12) {$%d$};" % (k, k))
    for k in yt:
        s.append(r"\node[grad,anchor=east] at (-.12,%d) {$%d$};" % (k, k))
    if origine:
        s.append(r"\node[grad,anchor=north east] at (-.08,-.08) {$0$};")
    if noms:
        s.append(r"\node[text=otMuted,anchor=west,inner sep=2pt] at (%s,0) {$x$};" % f(x1 + .5))
        s.append(r"\node[text=otMuted,anchor=south,inner sep=2pt] at (0,%s) {$y$};" % f(y1 + .5))
    return s


def pt(p, nom, ang, coul="otNavy", d=.13, U=1.0, texte=None):
    """Point plein + nom placé dans la direction ang (degrés), à d cm du point."""
    a = math.radians(ang)
    q = (p[0] + d / U * math.cos(a), p[1] + d / U * math.sin(a))
    s = [r"\fill[%s] %s circle (2.1pt);" % (coul, P(p))]
    if nom:
        s.append(r"\node[lab,text=%s,anchor=%d] at %s {$%s$};"
                 % (texte or ("otInk" if coul == "otNavy" else coul), (ang + 180) % 360, P(q), nom))
    return s


def lab(p, txt, ang, d=.13, U=1.0, coul="otInk", maths=True):
    """Texte seul posé à d cm de p dans la direction ang."""
    a = math.radians(ang)
    q = (p[0] + d / U * math.cos(a), p[1] + d / U * math.sin(a))
    t = ("$%s$" % txt) if maths else txt
    return [r"\node[lab,text=%s,anchor=%d] at %s {%s};" % (coul, (ang + 180) % 360, P(q), t)]


def lseg(p, q, txt, cote=1, t=.5, d=.14, U=1.0, coul="otInk", maths=True):
    """Étiquette d'un segment [pq], à gauche (cote=1) ou à droite (cote=-1) de p→q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * cote, dx / L * cote
    m = (p[0] + t * dx + d / U * nx, p[1] + t * dy + d / U * ny)
    ang = math.degrees(math.atan2(ny, nx))
    tt = ("$%s$" % txt) if maths else txt
    # ancre « boussole » : pour une étiquette large, un coin entier reste du côté libre
    noms = ["east", "north east", "north", "north west", "west", "south west", "south", "south east"]
    anc = noms[int(round(((ang + 180) % 360) / 45)) % 8]
    return [r"\node[lab,text=%s,anchor=%s] at %s {%s};" % (coul, anc, P(m), tt)]


def coord(**pts):
    return [" ".join(r"\coordinate (%s) at %s;" % (k, P(v)) for k, v in pts.items())]


def arc(c, a1, a2, r, txt=None, rl=None, U=1.0, coul="otOrange!90!black"):
    """Arc d'angle de centre c, de a1 à a2 (degrés), rayon r (cm) ; texte à rl (cm)."""
    r_u = r / U
    dep = (c[0] + r_u * math.cos(math.radians(a1)), c[1] + r_u * math.sin(math.radians(a1)))
    s = [r"\draw[%s,line width=.75pt] %s arc (%s:%s:%s);" % (coul, P(dep), f(a1), f(a2), f(r_u))]
    if txt:
        am = (a1 + a2) / 2
        s += lab(c, txt, am, d=rl or r + .12, U=U, coul=coul)
    return s


def figure(U, corps, extra=""):
    return "\n".join([r"\begin{tikzpicture}[x=%scm,y=%scm,line cap=round%s]" % (f(U), f(U), extra)]
                     + corps + [r"\end{tikzpicture}"])


FIGURES = {}

# ================================================================== COURS
# ------------------------------------------------------------------ projeté orthogonal (cours, fiche)
def projete(nd, nn, nom_n):
    M, H, N = (2, 2.8), (2, 0), (5.6, 0)
    c = coord(M=M, H=H, N=N)
    c += [r"\draw[geoTrait] (-.6,0) -- (7,0);",
          r"\draw[aide,otOrange!90!black] (M) -- (N);",
          r"\draw[geoReponse] (M) -- (H);", r"\angledroit{M}{H}{N}"]
    c += lab((7, 0), nd, 0, d=.12)
    c += lseg(M, H, "MH", 1, d=.14, coul="otGreenDark")
    c += lseg(M, N, nn, 1, t=.55, coul="otOrange!80!black")
    c += pt(M, "M", 90) + pt(H, "H", 270, "otGreenDark") + pt(N, nom_n, 270)
    return figure(1.0, c)


FIGURES["projete"] = projete("d", "MN", "N")

# ------------------------------------------------------------------ triangle rectangle et trigonométrie
A, B, C = (0, 0), (5.2, 0), (5.2, 3.1)
c = coord(A=A, B=B, C=C)
c += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;",
      r"\draw[otGreenDark,line width=1.3pt] (A) -- (B);",
      r"\draw[otOrange,line width=1.3pt] (B) -- (C);",
      r"\draw[otNavy,line width=1.3pt] (A) -- (C);", r"\angledroit{A}{B}{C}"]
c += arc(A, 0, math.degrees(math.atan2(3.1, 5.2)), .85, r"\alpha", rl=1.15, coul="otNavy")
c += [r"\node[txt,text=otNavy,anchor=south east] at (2.35,1.6) {hypoténuse};"]
c += [r"\node[txt,text=otGreenDark,anchor=north] at (2.6,-.2) {côté adjacent à $\alpha$};"]
c += [r"\node[txt,text=otOrange!80!black,anchor=west,align=left] at (5.42,1.55) {côté opposé\\à $\alpha$};"]
c += pt(A, "A", 200) + pt(B, "B", 315) + pt(C, "C", 60)
FIGURES["trigo"] = figure(1.0, c)

# ------------------------------------------------------------------ hauteur d'un arbre
O, H, S = (0, 0), (6, 0), (6, 4.2)
c = coord(O=O, H=H, S=S)
c += [r"\draw[otMuted,line width=.8pt] (-.6,0) -- (7.4,0);",
      r"\fill[otGreen!35] (6,3.45) circle (.78);",
      r"\draw[otOrange!60!black,line width=2.6pt] (6,0) -- (6,2.75);",
      r"\draw[aide,otOrange!90!black] (O) -- (S);", r"\angledroit{O}{H}{S}"]
c += arc(O, 0, 35, 1.25, r"35°", rl=1.62)
c += [r"\cote[.6]{H}{O}{$20$ m}", r"\cote[1.25]{S}{H}{$HS$}"]
c += pt(O, "O", 135) + pt(H, "H", 315) + pt(S, "S", 140, "otGreenDark")
FIGURES["arbre"] = figure(1.0, c)

# ------------------------------------------------------------------ solides usuels
c = []
# pyramide
c += [r"\fill[otSky] (0,0) -- (1.9,0) -- (1.2,2.5) -- cycle;",
      r"\fill[otSky!60] (1.9,0) -- (2.5,.6) -- (1.2,2.5) -- cycle;",
      r"\draw[geoTrait] (0,0) -- (1.9,0) -- (2.5,.6) (0,0) -- (1.2,2.5) -- (1.9,0) (1.2,2.5) -- (2.5,.6);",
      r"\draw[cache] (0,0) -- (.6,.6) -- (2.5,.6) (.6,.6) -- (1.2,2.5);",
      r"\draw[aideV] (1.2,2.5) -- (1.25,.3);"]
# cône
cx = 4.2
c += [r"\fill[otSky] (%s,0) -- (%s,2.5) -- (%s,0) arc (0:-180:.85 and .24) -- cycle;" % (f(cx - .85), f(cx), f(cx + .85)),
      r"\draw[geoTrait] (%s,0) -- (%s,2.5) -- (%s,0);" % (f(cx - .85), f(cx), f(cx + .85)),
      r"\draw[geoTrait] (%s,0) arc (0:-180:.85 and .24);" % f(cx + .85),
      r"\draw[cache] (%s,0) arc (0:180:.85 and .24);" % f(cx + .85),
      r"\draw[aideV] (%s,0) -- (%s,2.5) (%s,0) -- (%s,0);" % (f(cx), f(cx), f(cx), f(cx + .85))]
# légendes de la première rangée
for x0, nom, form in ((1.25, "pyramide", r"V = \frac{1}{3}\,\mathcal{B}h"),
                      (4.2, "cône", r"V = \frac{1}{3}\,\pi r^2 h")):
    c += [r"\node[txt,text=otNavy,anchor=north] at (%s,-.45) {%s};" % (f(x0), nom),
          r"\node[lab,anchor=north] at (%s,-.88) {$%s$};" % (f(x0), form)]
# seconde rangée (2 × 2 : lisible sur téléphone)
c += [r"\begin{scope}[shift={(0,-4.7)}]"]
# cylindre
cx = 1.25
c += [r"\fill[otSky] (%s,0) -- (%s,2.2) arc (180:360:.8 and .23) -- (%s,0) arc (0:-180:.8 and .23) -- cycle;" % (f(cx - .8), f(cx - .8), f(cx + .8)),
      r"\draw[geoTrait] (%s,0) -- (%s,2.2) (%s,0) -- (%s,2.2);" % (f(cx - .8), f(cx - .8), f(cx + .8), f(cx + .8)),
      r"\draw[geoTrait,fill=otSky!60] (%s,2.2) ellipse (.8 and .23);" % f(cx),
      r"\draw[geoTrait] (%s,0) arc (0:-180:.8 and .23);" % f(cx + .8),
      r"\draw[cache] (%s,0) arc (0:180:.8 and .23);" % f(cx + .8),
      r"\draw[aideV] (%s,0) -- (%s,2.2);" % (f(cx), f(cx))]
# boule
cx, cy = 4.2, 1.05
c += [r"\fill[otSky] (%s,%s) circle (1);" % (f(cx), f(cy)),  # aplat des livres (plus de dégradé gris)
      r"\draw[geoTrait] (%s,%s) circle (1);" % (f(cx), f(cy)),
      r"\draw[geoTrait,line width=.6pt] (%s,%s) arc (0:-180:1 and .28);" % (f(cx + 1), f(cy)),
      r"\draw[cache] (%s,%s) arc (0:180:1 and .28);" % (f(cx + 1), f(cy)),
      r"\draw[aideV] (%s,%s) -- (%s,%s);" % (f(cx), f(cy), f(cx + .98), f(cy + .2))]
c += [r"\fill[otGreenDark] (%s,%s) circle (1.5pt);" % (f(cx), f(cy))]
for x0, nom, form in ((1.25, "cylindre", r"V = \pi r^2 h"),
                      (4.2, "boule", r"V = \frac{4}{3}\,\pi r^3")):
    c += [r"\node[txt,text=otNavy,anchor=north] at (%s,-.45) {%s};" % (f(x0), nom),
          r"\node[lab,anchor=north] at (%s,-.88) {$%s$};" % (f(x0), form)]
c += [r"\end{scope}"]
FIGURES["solides"] = figure(1.0, c)

# ------------------------------------------------------------------ enclos le long d'un mur
c = [r"\fill[pattern=north east lines,pattern color=otMuted] (-.7,2.5) rectangle (6.7,2.8);",
     r"\draw[otMuted,line width=1.2pt] (-.7,2.5) -- (6.7,2.5);",
     r"\fill[otSky] (0,0) rectangle (6,2.5);",
     r"\draw[geoTrait,line width=1.2pt] (0,2.5) -- (0,0) -- (6,0) -- (6,2.5);"]
c += [r"\node[txt,text=otMuted,anchor=south] at (3,2.92) {mur};",
      r"\node[txt,text=otNavy] at (3,1.25) {enclos};",
      r"\node[lab,anchor=east] at (-.14,1.25) {$x$};",
      r"\node[lab,anchor=west] at (6.14,1.25) {$x$};",
      r"\node[lab,anchor=north] at (3,-.14) {$40 - 2x$};"]
FIGURES["enclos"] = figure(.9, c)

# ================================================================== EXERCICES
# ------------------------------------------------------------------ 2057 : carré ACBD
U = .72
A, B, C, D, M = (-1, 1), (3, 5), (3, 1), (-1, 5), (1, 3)
c = coord(A=A, B=B, C=C, D=D) + [r"\fill[otSky] (A) -- (C) -- (B) -- (D) -- cycle;"]
c += repere(-2, 4, -1, 6, xt=(-1, 1, 2, 3), yt=(3, 6))
c += [r"\draw[aide] (A) -- (B) (C) -- (D);",
      r"\draw[geoTrait] (B) -- (C) -- (A);", r"\draw[geoReponse] (A) -- (D) -- (B);",
      r"\angledroit{A}{C}{B}", r"\codage{A}{C}", r"\codage{C}{B}"]
c += pt(A, "A", 225, U=U) + pt(C, "C", 315, U=U) + pt(B, "B", 45, U=U)
c += pt(D, "D", 135, "otGreenDark", U=U) + pt(M, "M", 0, d=.2, U=U)
FIGURES["ex_carre_acbd"] = figure(U, c)

# ------------------------------------------------------------------ 2058 : projeté dans un repère
def ex_projete(corrige):
    U = .62
    Pp, Q, M, H = (-2, 4), (4, 1), (4, 6), (2, 2)
    c = repere(-3, 5, -1, 7, xt=(-2, -1, 1, 2, 3, 4), yt=(1, 2, 3, 4, 5, 6))
    c += coord(P=Pp, Q=Q, M=M, H=H)
    c += [r"\draw[geoTrait] (-3,4.5) -- (5.4,.3);"]
    c += lab((5.4, .3), "(PQ)", 20, d=.1, U=U, coul="otNavy")
    if corrige:
        c += [r"\draw[aide] (M) -- (P) (M) -- (Q);", r"\draw[geoReponse] (M) -- (H);", r"\angledroit{M}{H}{Q}"]
        c += pt(H, "H", 225, "otGreenDark", U=U)
    c += pt(Pp, "P", 225, U=U) + pt(Q, "Q", 225, U=U) + pt(M, "M", 45, U=U)
    return figure(U, c)


FIGURES["ex_projete_enonce"] = ex_projete(False)
FIGURES["ex_projete_corrige"] = ex_projete(True)

# ------------------------------------------------------------------ 2069 : aire maximale (courbe)
FIGURES["ex_aire_max"] = r"""\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.6cm, xmin=0, xmax=21.5, ymin=0, ymax=118,
  xtick={5,10,15,20}, ytick={25,50,75,100}, ylabel={$\mathcal{A}(x)$},
  xticklabels={}, ]
\addplot[courbe,domain=0:20] {x*(20-x)};
\draw[guide] (axis cs:10,0) -- (axis cs:10,100) -- (axis cs:0,100);
\pnt[otGreenDark]{10}{100}
\node[lab,text=otGreenDark,anchor=south] at (axis cs:10,103) {maximum $(10\,;100)$};
\end{axis}
\end{tikzpicture}"""
XLAB = {"ex_aire_max": [(5, "c", "5"), (10, "c", "10"), (15, "c", "15"), (20, "c", "20")]}

# ------------------------------------------------------------------ 2056 : parallélogramme et hauteur
U = .8
A, B, C, D, K, E = (-2, 1), (2, 1), (3, 4), (-1, 4), (.5, 2.5), (-1, 1)
c = coord(A=A, B=B, C=C, D=D, E=E) + [r"\fill[otSky] (A) -- (B) -- (C) -- (D) -- cycle;"]
c += repere(-3, 4, -1, 5, xt=(-2, -1, 1, 2, 3), yt=(5,))
c += [r"\draw[aide] (A) -- (C) (B) -- (D);",
      r"\draw[geoTrait] (D) -- (A) -- (B);", r"\draw[geoReponse] (B) -- (C) -- (D);",
      r"\draw[otOrange,line width=.9pt,dash pattern=on 3pt off 2pt] (D) -- (E);", r"\angledroit{D}{E}{B}"]
c += lseg(D, E, "3", 1, d=.12, U=U, coul="otOrange!80!black")
c += pt(A, "A", 225, U=U) + pt(B, "B", 315, U=U) + pt(D, "D", 135, U=U)
c += pt(C, "C", 45, "otGreenDark", U=U) + pt(K, "K", 83, "otGreenDark", d=.2, U=U)
c += pt(E, "E", 270, "otGreenDark", U=U)
FIGURES["ex_parallelogramme"] = figure(U, c)

# ------------------------------------------------------------------ 2060 : cercle de diamètre [AB]
U = .6
A, B, C, D, E, M = (-2, 1), (4, 3), (4, 1), (-2, 3), (1, 5), (1, 2)
c = coord(A=A, B=B, C=C, D=D, M=M) + [r"\fill[otGreen!14] (A) -- (C) -- (B) -- (D) -- cycle;"]
c += repere(-3, 5, -2, 6, xt=(-2, 2, 4), yt=(2, 4))  # pas de « 3 » : le cercle passe dessus
c += [r"\draw[otNavy,line width=1pt] (M) circle (%s);" % f(math.sqrt(10)),
      r"\draw[aide] (A) -- (B) (C) -- (D);",
      r"\draw[geoReponse] (A) -- (C) -- (B) -- (D) -- cycle;",
      r"\angledroit{A}{C}{B}", r"\angledroit{B}{D}{A}"]
c += lab((1 + math.sqrt(10) * math.cos(math.radians(120)), 2 + math.sqrt(10) * math.sin(math.radians(120))),
         r"\mathcal{C}", 120, d=.14, U=U, coul="otNavy")
c += pt(A, "A", 198, U=U) + pt(B, "B", 18, U=U) + pt(C, "C", 342, U=U) + pt(D, "D", 162, U=U)
c += pt(E, "E", 270, U=U) + pt(M, "M", 270, d=.2, U=U)
FIGURES["ex_cercle_diametre"] = figure(U, c)

# ------------------------------------------------------------------ 2072 : cercle circonscrit
U = .42
A, B, C, D, O = (0, 0), (6, 0), (0, 8), (6, 8), (3, 4)
c = coord(A=A, B=B, C=C, D=D, O=O)
c += [r"\draw[otNavy,line width=.9pt] (O) circle (5);",
      r"\fill[otSky] (A) -- (B) -- (C) -- cycle;",
      r"\draw[aideV] (B) -- (D) -- (C) (A) -- (D);",
      r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;", r"\angledroit{B}{A}{C}"]
c += [r"\node[lab,anchor=south] at (3,.12) {$6$ cm};",
      r"\node[lab,anchor=west] at (.16,4.6) {$8$ cm};"]
c += pt(A, "A", 233, U=U) + pt(B, "B", 307, U=U) + pt(C, "C", 127, U=U)
c += pt(D, "D", 53, "otGreenDark", U=U) + pt(O, "O", 0, "otGreenDark", d=.2, U=U)
FIGURES["ex_circonscrit"] = figure(U, c)

# ------------------------------------------------------------------ 2061 : triangle AMB et projeté H
U = .55
A, B, M, H = (0, 0), (13, 0), (25 / 13, 60 / 13), (25 / 13, 0)
c = coord(A=A, B=B, M=M, H=H)
c += [r"\fill[otSky] (A) -- (B) -- (M) -- cycle;",
      r"\draw[geoTrait] (A) -- (B) -- (M) -- cycle;",
      r"\draw[aideV] (M) -- (H);", r"\angledroit{A}{M}{B}", r"\angledroit{M}{H}{B}"]
c += lseg(A, M, "5 \\text{ cm}", 1, U=U) + lseg(M, B, "12 \\text{ cm}", 1, U=U)
c += [r"\cote[.85]{B}{A}{$13$ cm}"]
c += pt(A, "A", 180, U=U) + pt(B, "B", 0, U=U) + pt(M, "M", 90, U=U) + pt(H, "H", 300, "otGreenDark", U=U)
FIGURES["ex_triangle_amb"] = figure(U, c)

# ------------------------------------------------------------------ 2055 : milieu et symétries
U = .5
A, B, Ap, M, O, C = (-3, 1), (1, 5), (5, 9), (-1, 3), (0, 0), (-2, 6)
# AB = BA' : la marque du milieu de [AB] tomberait sous le point M ; on code donc
# AM = MB et les deux moitiés de [BA'] (milieu N(3 ; 7), non nommé) du même trait simple.
N = (3, 7)
c = coord(A=A, B=B, Ap=Ap, M=M, O=O, C=C, N=N) + [r"\fill[otGreen!14] (O) -- (A) -- (C) -- (B) -- cycle;"]
c += repere(-4, 6, -1, 10, xt=(-3, -2, -1, 1, 3, 5), yt=(5, 6, 9), origine=False)
c += [r"\draw[geoReponse] (O) -- (A) -- (C) -- (B) -- cycle;",
      r"\draw[aide] (O) -- (C);",
      r"\draw[geoTrait] (A) -- (B);", r"\draw[aideV] (B) -- (Ap);",
      r"\codage{A}{M}", r"\codage{M}{B}", r"\codage{B}{N}", r"\codage{N}{Ap}",
      r"\codage[2]{O}{M}", r"\codage[2]{M}{C}"]
c += pt(A, "A", 225, U=U) + pt(B, "B", 330, U=U) + pt(M, "M", 345, d=.2, U=U) + pt(O, "O", 315, U=U)
c += pt(Ap, "A'", 135, "otGreenDark", U=U) + pt(C, "C", 135, "otGreenDark", U=U)
FIGURES["ex_symetries"] = figure(U, c)

# ------------------------------------------------------------------ 2063 : échelle contre un mur
U = .72
Pd, W, T = (0, 0), (4 * math.sqrt(3), 0), (4 * math.sqrt(3), 4)
c = coord(P=Pd, W=W, T=T)
c += [r"\fill[pattern=north east lines,pattern color=otMuted] (%s,-.35) rectangle (%s,5);" % (f(W[0]), f(W[0] + .35)),
      r"\draw[otMuted,line width=1pt] (%s,0) -- (%s,5);" % (f(W[0]), f(W[0])),
      r"\fill[pattern=north east lines,pattern color=otMuted!70] (-.8,-.3) rectangle (%s,0);" % f(W[0]),
      r"\draw[otMuted,line width=1pt] (-.8,0) -- (%s,0);" % f(W[0]),
      r"\draw[otOrange!70!black,line width=2.2pt] (P) -- (T);", r"\angledroit{P}{W}{T}"]
c += arc(Pd, 0, 30, 1.3, "30°", rl=1.7)
c += lseg(Pd, T, "8 \\text{ m}", 1, U=U, coul="otOrange!70!black")
c += [r"\node[lab,anchor=east] at (%s,2) {$h$};" % f(W[0] - .18),
      r"\node[lab,anchor=south] at (4.6,.12) {$d$};",
      r"\node[txt,text=otMuted,anchor=west,rotate=90] at (%s,1.2) {mur};" % f(W[0] + .62),
      r"\node[txt,text=otMuted,anchor=north] at (2,-.45) {sol};"]
FIGURES["ex_echelle"] = figure(U, c)

# ------------------------------------------------------------------ 2065 : triangle ABC et hauteur CH
U = .4
A, B, C, H = (0, 0), (14, 0), (9, 12), (9, 0)
c = coord(A=A, B=B, C=C, H=H)
c += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;",
      r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;",
      r"\draw[aideV] (C) -- (H);", r"\angledroit{C}{H}{B}"]
c += lseg(A, C, "15 \\text{ cm}", 1, U=U)
c += [r"\cote[.6]{H}{A}{$9$ cm}", r"\cote[1.3]{B}{A}{$14$ cm}"]
c += pt(A, "A", 180, U=U) + pt(B, "B", 0, U=U) + pt(C, "C", 90, U=U) + pt(H, "H", 150, "otGreenDark", d=.16, U=U)
FIGURES["ex_triangle_ch"] = figure(U, c)

# ------------------------------------------------------------------ 2066 : corde et distance au centre
U = .45
O, A, B, H = (0, 0), (-4, 3), (4, 3), (0, 3)
c = coord(O=O, A=A, B=B, H=H)
c += [r"\draw[otNavy,line width=1pt] (O) circle (5);",
      r"\fill[otSky] (O) -- (A) -- (B) -- cycle;",
      r"\draw[geoTrait] (O) -- (A) -- (B) -- cycle;",
      r"\draw[aideV] (O) -- (H);", r"\angledroit{O}{H}{B}",
      r"\codage{A}{H}", r"\codage{H}{B}"]
c += lseg(O, A, "5", -1, U=U) + lseg(O, H, "3", -1, t=.45, U=U, coul="otGreenDark")
c += pt(O, "O", 270, U=U) + pt(A, "A", 143, U=U) + pt(B, "B", 37, U=U) + pt(H, "H", 90, "otGreenDark", U=U)
FIGURES["ex_corde"] = figure(U, c)

# ------------------------------------------------------------------ 2067 : Thalès
U = .3
xc = 243 / 24
yc = math.sqrt(324 - xc ** 2)
A, B, C = (0, 0), (12, 0), (xc, yc)
D, E = (8, 0), (2 / 3 * xc, 2 / 3 * yc)
c = coord(A=A, B=B, C=C, D=D, E=E)
c += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;", r"\fill[otGreen!16] (A) -- (D) -- (E) -- cycle;",
      r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;", r"\draw[geoReponse] (D) -- (E);"]
# AC = 18 cm en cote sur toute la longueur [AC] (une étiquette posée près de [AE] se lisait « AE = 18 cm »)
c += lseg(B, C, "15 \\text{ cm}", -1, U=U)
c += [r"\cote[.7]{A}{C}{$18$ cm}", r"\cote[.55]{D}{A}{$8$ cm}", r"\cote[1.2]{B}{A}{$12$ cm}"]
c += pt(A, "A", 225, U=U) + pt(B, "B", 315, U=U) + pt(C, "C", 20, U=U)
c += pt(D, "D", 315, U=U) + pt(E, "E", 165, U=U)
FIGURES["ex_thales"] = figure(U, c)

# ------------------------------------------------------------------ 2064 : triangle 9-12-15
U = .42
A, B, C = (0, 0), (12, 0), (12, 9)
c = coord(A=A, B=B, C=C)
c += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;",
      r"\draw[geoTrait] (A) -- (C);",
      r"\draw[geoReponse] (A) -- (B) -- (C);", r"\angledroit{A}{B}{C}"]
c += arc(A, 0, math.degrees(math.atan2(9, 12)), .9, r"\alpha", rl=1.2, U=U, coul="otNavy")
c += lseg(A, C, "15 \\text{ cm}", 1, U=U)
c += lseg(A, B, "12 \\text{ cm}", -1, U=U, coul="otGreenDark")
c += lseg(B, C, "9 \\text{ cm}", -1, U=U, coul="otGreenDark")
FIGURES["ex_trigo_15"] = figure(U, c)

# ------------------------------------------------------------------ 2068 : cylindre et cône
U = .2
c = []
cx, R, Hh = 0, 6, 15
c += [r"\fill[otSky] (-6,0) -- (-6,15) arc (180:360:6 and 1.7) -- (6,0) arc (0:-180:6 and 1.7) -- cycle;",
      r"\draw[geoTrait] (-6,0) -- (-6,15) (6,0) -- (6,15);",
      r"\draw[geoTrait,fill=otSky!60] (0,15) ellipse (6 and 1.7);",
      r"\draw[geoTrait] (6,0) arc (0:-180:6 and 1.7);",
      r"\draw[cache] (6,0) arc (0:180:6 and 1.7);",
      r"\draw[aideV] (0,0) -- (0,15) (0,0) -- (6,0);"]
c += [r"\node[lab,anchor=west] at (.6,8) {$h$};", r"\node[lab,anchor=north] at (3,-.5) {$r$};"]
c += [r"\fill[otSky] (12,0) -- (18,15) -- (24,0) arc (0:-180:6 and 1.7) -- cycle;",
      r"\draw[geoTrait] (12,0) -- (18,15) -- (24,0);",
      r"\draw[geoTrait] (24,0) arc (0:-180:6 and 1.7);",
      r"\draw[cache] (24,0) arc (0:180:6 and 1.7);",
      r"\draw[aideV] (18,0) -- (18,15) (18,0) -- (24,0);"]
c += [r"\node[lab,anchor=west] at (18.6,6) {$h$};", r"\node[lab,anchor=north] at (21,-.5) {$r$};"]
c += [r"\node[txt,text=otNavy,anchor=north] at (0,-3.2) {cylindre};",
      r"\node[txt,text=otNavy,anchor=north] at (18,-3.2) {cône};",
      r"\node[lab,anchor=west] at (26,9) {$r = 6$ cm};",
      r"\node[lab,anchor=west] at (26,5.5) {$h = 15$ cm};"]
FIGURES["ex_cylindre_cone"] = figure(U, c)

# ------------------------------------------------------------------ 2071 : triangle avec un angle de 60°
U = .55
A, C, B, H = (0, 0), (9, 0), (3.5, 7 * math.sqrt(3) / 2), (3.5, 0)
c = coord(A=A, B=B, C=C, H=H)
c += [r"\fill[otSky] (A) -- (C) -- (B) -- cycle;",
      r"\draw[geoTrait] (A) -- (C) -- (B) -- cycle;",
      r"\draw[aideV] (B) -- (H);", r"\angledroit{B}{H}{C}"]
c += arc(A, 0, 60, .8, "60°", rl=1.15, U=U)
c += lseg(A, B, "7 \\text{ cm}", 1, U=U)
c += [r"\cote[.75]{C}{A}{$9$ cm}"]
c += pt(A, "A", 200, U=U) + pt(C, "C", 340, U=U) + pt(B, "B", 90, U=U) + pt(H, "H", 300, "otGreenDark", U=U)
FIGURES["ex_triangle_60"] = figure(U, c)

# ------------------------------------------------------------------ 2062 : point le plus proche
FIGURES["ex_delta"] = projete(r"\Delta", "MP", "P")

# ------------------------------------------------------------------ 2059 : carré dans un repère
U = .62
A, B, C, D, K = (1, 1), (5, 2), (4, 6), (0, 5), (2.5, 3.5)
c = coord(A=A, B=B, C=C, D=D, K=K) + [r"\fill[otSky] (A) -- (B) -- (C) -- (D) -- cycle;"]
c += repere(-1, 6, -1, 7, xt=(1, 2, 3, 4, 5), yt=(1, 6))
c += [r"\draw[aideV] (K) circle (%s);" % f(math.sqrt(34) / 2),
      r"\draw[aide] (A) -- (C) (B) -- (D);",
      r"\draw[geoTrait] (A) -- (B) -- (C) -- (D) -- cycle;", r"\angledroit{A}{B}{C}",
      r"\codage{A}{B}", r"\codage{B}{C}", r"\codage{C}{D}", r"\codage{D}{A}"]
c += pt(A, "A", 225, U=U) + pt(B, "B", 0, d=.17, U=U) + pt(C, "C", 45, U=U) + pt(D, "D", 180, d=.17, U=U)
c += pt(K, "K", 14, "otGreenDark", d=.25, U=U)
FIGURES["ex_carre_repere"] = figure(U, c)

# ------------------------------------------------------------------ nouveau-1 : pyramide régulière
U = .9
A, B, C, D = (0, 0), (4, 0), (5.4, 1.5), (1.4, 1.5)
O = (2.7, .75)
S = (2.7, 5)
c = coord(A=A, B=B, C=C, D=D, O=O, S=S)
c += [r"\fill[otSky] (A) -- (B) -- (S) -- cycle;", r"\fill[otSky!60] (B) -- (C) -- (S) -- cycle;",
      r"\draw[cache] (A) -- (D) -- (C) (D) -- (S) (A) -- (C) (B) -- (D);",
      r"\draw[aideV] (S) -- (O) -- (A);", r"\angledroit{S}{O}{A}",
      r"\draw[geoTrait] (A) -- (B) -- (C) -- (S) -- cycle (B) -- (S);"]
c += lseg(A, S, "9 \\text{ cm}", 1, U=U)
c += [r"\cote[.4]{B}{A}{$6$ cm}"]
c += pt(A, "A", 225, U=U) + pt(B, "B", 315, U=U) + pt(C, "C", 0, U=U) + pt(D, "D", 155, U=U)
c += pt(S, "S", 90, U=U) + pt(O, "O", 265, "otGreenDark", d=.2, U=U)
FIGURES["ex_pyramide"] = figure(U, c)

# ------------------------------------------------------------------ nouveau-2 : carré inscrit
U = .46
A, B, C, D = (0, 0), (10, 0), (10, 10), (0, 10)
M, N, Pp, Q = (3, 0), (10, 3), (7, 10), (0, 7)
c = coord(A=A, B=B, C=C, D=D, M=M, N=N, P=Pp, Q=Q)
c += [r"\fill[otGreen!16] (M) -- (N) -- (P) -- (Q) -- cycle;",
      r"\draw[geoTrait] (A) -- (B) -- (C) -- (D) -- cycle;",
      r"\draw[geoReponse] (M) -- (N) -- (P) -- (Q) -- cycle;"]
c += [r"\cote[.4]{M}{A}{$x$}", r"\cote[.4]{N}{B}{$x$}", r"\cote[.4]{P}{C}{$x$}", r"\cote[.4]{Q}{D}{$x$}"]
c += pt(A, "A", 225, U=U) + pt(B, "B", 315, U=U) + pt(C, "C", 45, U=U) + pt(D, "D", 135, U=U)
c += pt(M, "M", 60, U=U) + pt(N, "N", 150, U=U) + pt(Pp, "P", 240, U=U) + pt(Q, "Q", 330, U=U)
FIGURES["ex_carre_inscrit"] = figure(U, c)


# ================================================================== FINITION 2026-11-02
# Figures d'énoncé (données seules, sans la réponse) et figures de corrigé (réponse en vert).
def vert(t):
    return r"\textcolor{otGreenDark}{%s}" % t


# ------------------------------------------------------------------ 2057 (énoncé) : A, B, C
U = .72
A, B, C = (-1, 1), (3, 5), (3, 1)
c = coord(A=A, B=B, C=C)
c += repere(-2, 4, -1, 6, xt=(-1, 1, 2, 3), yt=(3, 6))
c += [r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;"]
c += pt(A, "A", 225, U=U) + pt(C, "C", 315, U=U) + pt(B, "B", 45, U=U)
FIGURES["ex_carre_acbd_enonce"] = figure(U, c)

# ------------------------------------------------------------------ 2069 (énoncé) : rectangle de périmètre 40 cm
c = [r"\fill[otSky] (0,0) rectangle (6,3.2);", r"\draw[geoTrait] (0,0) rectangle (6,3.2);",
     r"\angledroit{6,0}{0,0}{0,3.2}"]
c += [r"\node[lab,anchor=north] at (3,-.14) {$x$};", r"\node[lab,anchor=west] at (6.14,1.6) {$y$};",
      r"\node[txt,text=otNavy] at (3,1.6) {périmètre : 40 cm};"]
FIGURES["ex_rectangle_enonce"] = figure(1.0, c)

# ------------------------------------------------------------------ 2056 (énoncé) : A, B, D
U = .8
A, B, D = (-2, 1), (2, 1), (-1, 4)
c = coord(A=A, B=B, D=D)
c += repere(-3, 4, -1, 5, xt=(-2, -1, 1, 2, 3), yt=(4,))
c += [r"\draw[geoTrait] (D) -- (A) -- (B);"]
c += pt(A, "A", 225, U=U) + pt(B, "B", 315, U=U) + pt(D, "D", 135, U=U)
FIGURES["ex_parallelogramme_enonce"] = figure(U, c)

# ------------------------------------------------------------------ 2060 (énoncé) : les cinq points et [AB]
U = .6
A, B, C, D, E = (-2, 1), (4, 3), (4, 1), (-2, 3), (1, 5)
c = coord(A=A, B=B)
c += repere(-3, 5, -2, 6, xt=(-2, 1, 4), yt=(3, 5))
c += [r"\draw[geoTrait] (A) -- (B);"]
c += pt(A, "A", 198, U=U) + pt(B, "B", 18, U=U) + pt(C, "C", 342, U=U) + pt(D, "D", 162, U=U)
c += pt(E, "E", 90, U=U)
FIGURES["ex_cercle_diametre_enonce"] = figure(U, c)

# ------------------------------------------------------------------ 2072 (énoncé) : triangle rectangle et milieu O
U = .42
A, B, C, O = (0, 0), (6, 0), (0, 8), (3, 4)
c = coord(A=A, B=B, C=C, O=O)
c += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;",
      r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;", r"\angledroit{B}{A}{C}",
      r"\codage{B}{O}", r"\codage{O}{C}"]
c += [r"\node[lab,anchor=north] at (3,-.14) {$6$ cm};",
      r"\node[lab,anchor=east] at (-.16,4) {$8$ cm};"]
c += pt(A, "A", 225, U=U) + pt(B, "B", 315, U=U) + pt(C, "C", 135, U=U) + pt(O, "O", 37, U=U)
FIGURES["ex_circonscrit_enonce"] = figure(U, c)

# ------------------------------------------------------------------ 2055 (énoncé) : O, A, B
U = .5
A, B, O = (-3, 1), (1, 5), (0, 0)
c = coord(A=A, B=B)
c += repere(-4, 6, -1, 10, xt=(-3, -2, -1, 1, 3, 5), yt=(5, 6, 9), origine=False)
c += [r"\draw[geoTrait] (A) -- (B);"]
c += pt(A, "A", 225, U=U) + pt(B, "B", 330, U=U) + pt(O, "O", 315, U=U)
FIGURES["ex_symetries_enonce"] = figure(U, c)

# ------------------------------------------------------------------ 2066 (énoncé) : cercle, corde [AB], milieu H
U = .45
O, A, B, H = (0, 0), (-4, 3), (4, 3), (0, 3)
c = coord(O=O, A=A, B=B, H=H)
c += [r"\draw[otNavy,line width=1pt] (O) circle (5);",
      r"\draw[geoTrait] (A) -- (B) (O) -- (A);",
      r"\codage{A}{H}", r"\codage{H}{B}"]
c += lseg(O, A, "5 \\text{ cm}", -1, U=U)
c += pt(O, "O", 270, U=U) + pt(A, "A", 143, U=U) + pt(B, "B", 37, U=U) + pt(H, "H", 90, U=U)
FIGURES["ex_corde_enonce"] = figure(U, c)

# ------------------------------------------------------------------ 2064 (énoncé) : hypoténuse 15 cm, angle α
U = .42
A, B, C = (0, 0), (12, 0), (12, 9)
c = coord(A=A, B=B, C=C)
c += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;",
      r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;", r"\angledroit{A}{B}{C}"]
c += arc(A, 0, math.degrees(math.atan2(9, 12)), .9, r"\alpha", rl=1.2, U=U, coul="otNavy")
c += lseg(A, C, "15 \\text{ cm}", 1, U=U)
FIGURES["ex_trigo_15_enonce"] = figure(U, c)

# ------------------------------------------------------------------ 2059 (énoncé) : quadrilatère ABCD
U = .62
A, B, C, D = (1, 1), (5, 2), (4, 6), (0, 5)
c = coord(A=A, B=B, C=C, D=D)
c += repere(-1, 6, -1, 7, xt=(1, 2, 3, 4, 5), yt=(1, 6))
c += [r"\draw[geoTrait] (A) -- (B) -- (C) -- (D) -- cycle;"]
c += pt(A, "A", 225, U=U) + pt(B, "B", 0, d=.17, U=U) + pt(C, "C", 45, U=U) + pt(D, "D", 180, d=.17, U=U)
FIGURES["ex_carre_repere_enonce"] = figure(U, c)

# ------------------------------------------------------------------ 2061 (corrigé) : MH = 60/13
U = .55
A, B, M, H = (0, 0), (13, 0), (25 / 13, 60 / 13), (25 / 13, 0)
c = coord(A=A, B=B, M=M, H=H)
c += [r"\fill[otSky] (A) -- (B) -- (M) -- cycle;",
      r"\draw[geoTrait] (A) -- (B) -- (M) -- cycle;",
      r"\draw[geoReponse,line width=1.3pt] (M) -- (H);", r"\angledroit{A}{M}{B}", r"\angledroit{M}{H}{B}"]
c += lseg(A, M, "5 \\text{ cm}", 1, U=U) + lseg(M, B, "12 \\text{ cm}", 1, U=U)
c += [r"\node[lab,text=otGreenDark,anchor=west] at (%s,%s) {$MH = \dfrac{60}{13}$ cm};" % (f(H[0] + .35), f(2.1))]
c += [r"\cote[.85]{B}{A}{$13$ cm}"]
c += pt(A, "A", 180, U=U) + pt(B, "B", 0, U=U) + pt(M, "M", 90, U=U) + pt(H, "H", 300, "otGreenDark", U=U)
FIGURES["ex_triangle_amb_corrige"] = figure(U, c)

# ------------------------------------------------------------------ 2063 (corrigé) : h = 4 m, d ≈ 6,93 m
U = .72
Pd, W, T = (0, 0), (4 * math.sqrt(3), 0), (4 * math.sqrt(3), 4)
c = coord(P=Pd, W=W, T=T)
c += [r"\fill[pattern=north east lines,pattern color=otMuted] (%s,-.35) rectangle (%s,5);" % (f(W[0]), f(W[0] + .35)),
      r"\draw[otMuted,line width=1pt] (%s,0) -- (%s,5);" % (f(W[0]), f(W[0])),
      r"\fill[pattern=north east lines,pattern color=otMuted!70] (-.8,-.3) rectangle (%s,0);" % f(W[0]),
      r"\draw[otMuted,line width=1pt] (-.8,0) -- (%s,0);" % f(W[0]),
      r"\draw[geoReponse,line width=1.6pt] (W) -- (T);",
      r"\draw[otOrange!70!black,line width=2.2pt] (P) -- (T);", r"\angledroit{P}{W}{T}"]
c += arc(Pd, 0, 30, 1.3, "30°", rl=1.7)
c += lseg(Pd, T, "8 \\text{ m}", 1, U=U, coul="otOrange!70!black")
c += [r"\node[lab,text=otGreenDark,anchor=east] at (%s,2) {$h = 4$ m};" % f(W[0] - .18),
      r"\node[lab,text=otGreenDark,anchor=south] at (4.9,.12) {$d \approx 6{,}93$ m};",
      r"\node[txt,text=otMuted,anchor=west,rotate=90] at (%s,1.2) {mur};" % f(W[0] + .62),
      r"\node[txt,text=otMuted,anchor=north] at (2,-.45) {sol};"]
FIGURES["ex_echelle_corrige"] = figure(U, c)

# ------------------------------------------------------------------ 2065 (corrigé) : CH = 12, BH = 5, BC = 13
U = .4
A, B, C, H = (0, 0), (14, 0), (9, 12), (9, 0)
c = coord(A=A, B=B, C=C, H=H)
c += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;",
      r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;",
      r"\draw[geoReponse,line width=1.3pt] (C) -- (H) (B) -- (C);", r"\angledroit{C}{H}{B}"]
c += lseg(A, C, "15 \\text{ cm}", 1, U=U)
c += lseg(C, H, "12 \\text{ cm}", -1, t=.45, U=U, coul="otGreenDark")
c += lseg(B, C, "13 \\text{ cm}", -1, U=U, coul="otGreenDark")
c += [r"\node[lab,text=otGreenDark,anchor=south] at (11.6,.2) {$5$ cm};"]
c += [r"\cote[.6]{H}{A}{$9$ cm}", r"\cote[1.3]{B}{A}{$14$ cm}"]
c += pt(A, "A", 180, U=U) + pt(B, "B", 0, U=U) + pt(C, "C", 90, U=U) + pt(H, "H", 150, "otGreenDark", d=.16, U=U)
FIGURES["ex_triangle_ch_corrige"] = figure(U, c)

# ------------------------------------------------------------------ 2067 (corrigé) : AE = 12, DE = 10
U = .3
xc = 243 / 24
yc = math.sqrt(324 - xc ** 2)
A, B, C = (0, 0), (12, 0), (xc, yc)
D, E = (8, 0), (2 / 3 * xc, 2 / 3 * yc)
c = coord(A=A, B=B, C=C, D=D, E=E)
c += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;", r"\fill[otGreen!16] (A) -- (D) -- (E) -- cycle;",
      r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;", r"\draw[geoReponse,line width=1.3pt] (A) -- (E) -- (D);"]
c += lseg(B, C, "15 \\text{ cm}", -1, U=U)
c += lseg(A, E, "12 \\text{ cm}", -1, t=.42, U=U, coul="otGreenDark")
c += lseg(D, E, "10 \\text{ cm}", -1, t=.5, U=U, coul="otGreenDark")
c += [r"\cote[.7]{A}{C}{$18$ cm}", r"\cote[.55]{D}{A}{$8$ cm}", r"\cote[1.2]{B}{A}{$12$ cm}"]
c += pt(A, "A", 225, U=U) + pt(B, "B", 315, U=U) + pt(C, "C", 20, U=U)
c += pt(D, "D", 315, U=U) + pt(E, "E", 165, "otGreenDark", U=U)
FIGURES["ex_thales_corrige"] = figure(U, c)

# ------------------------------------------------------------------ 2068 (corrigé) : volumes
U = .2
c = []
c += [r"\fill[otSky] (-6,0) -- (-6,15) arc (180:360:6 and 1.7) -- (6,0) arc (0:-180:6 and 1.7) -- cycle;",
      r"\draw[geoTrait] (-6,0) -- (-6,15) (6,0) -- (6,15);",
      r"\draw[geoTrait,fill=otSky!60] (0,15) ellipse (6 and 1.7);",
      r"\draw[geoTrait] (6,0) arc (0:-180:6 and 1.7);",
      r"\draw[cache] (6,0) arc (0:180:6 and 1.7);",
      r"\draw[aideV] (0,0) -- (0,15) (0,0) -- (6,0);"]
c += [r"\node[lab,anchor=west] at (.6,8) {$h$};", r"\node[lab,anchor=north] at (3,-.5) {$r$};"]
c += [r"\fill[otSky] (12,0) -- (18,15) -- (24,0) arc (0:-180:6 and 1.7) -- cycle;",
      r"\draw[geoTrait] (12,0) -- (18,15) -- (24,0);",
      r"\draw[geoTrait] (24,0) arc (0:-180:6 and 1.7);",
      r"\draw[cache] (24,0) arc (0:180:6 and 1.7);",
      r"\draw[aideV] (18,0) -- (18,15) (18,0) -- (24,0);"]
c += [r"\node[lab,anchor=west] at (18.6,6) {$h$};", r"\node[lab,anchor=north] at (21,-.5) {$r$};"]
c += [r"\node[txt,text=otNavy,anchor=north] at (0,-3.2) {cylindre};",
      r"\node[txt,text=otNavy,anchor=north] at (18,-3.2) {cône};",
      r"\node[lab,text=otGreenDark,anchor=north] at (0,-5.6) {$V = 540\pi$ cm³};",
      r"\node[lab,text=otGreenDark,anchor=north] at (18,-5.6) {$V = 180\pi$ cm³};",
      r"\node[lab,anchor=west] at (26,9) {$r = 6$ cm};",
      r"\node[lab,anchor=west] at (26,5.5) {$h = 15$ cm};"]
FIGURES["ex_cylindre_cone_corrige"] = figure(U, c)

# ------------------------------------------------------------------ 2071 (corrigé) : AH, HC, BH, BC
U = .55
A, C, B, H = (0, 0), (9, 0), (3.5, 7 * math.sqrt(3) / 2), (3.5, 0)
c = coord(A=A, B=B, C=C, H=H)
c += [r"\fill[otSky] (A) -- (C) -- (B) -- cycle;",
      r"\draw[geoTrait] (A) -- (C) -- (B) -- cycle;",
      r"\draw[geoReponse,line width=1.3pt] (B) -- (H) (B) -- (C);", r"\angledroit{B}{H}{C}"]
c += arc(A, 0, 60, .8, "60°", rl=1.15, U=U)
c += lseg(A, B, "7 \\text{ cm}", 1, U=U)
c += [r"\node[lab,text=otGreenDark,anchor=west] at (3.75,2.7) {$\dfrac{7\sqrt{3}}{2}$};"]
c += lseg(B, C, "\\sqrt{67} \\approx 8{,}2 \\text{ cm}", 1, U=U, coul="otGreenDark")
c += [r"\node[lab,text=otGreenDark,anchor=north] at (1.75,-.16) {$3{,}5$};",
      r"\node[lab,text=otGreenDark,anchor=north] at (6.25,-.16) {$5{,}5$};"]
c += [r"\cote[1.3]{C}{A}{$9$ cm}"]
c += pt(A, "A", 200, U=U) + pt(C, "C", 340, U=U) + pt(B, "B", 90, U=U) + pt(H, "H", 300, "otGreenDark", U=U)
FIGURES["ex_triangle_60_corrige"] = figure(U, c)

# ------------------------------------------------------------------ 2062 (corrigé) : MP² = MH² + HP²
M, H, N = (2, 2.8), (2, 0), (5.6, 0)
c = coord(M=M, H=H, N=N)
c += [r"\fill[otGreen!14] (M) -- (H) -- (N) -- cycle;",
      r"\draw[geoTrait] (-.6,0) -- (7,0);",
      r"\draw[otOrange!90!black,line width=1pt] (M) -- (N);",
      r"\draw[geoReponse,line width=1.3pt] (M) -- (H) -- (N);", r"\angledroit{M}{H}{N}"]
c += lab((7, 0), r"\Delta", 0, d=.12)
c += lseg(M, H, "MH", 1, d=.14, coul="otGreenDark")
c += lseg(H, N, "HP", -1, d=.16, coul="otGreenDark")
c += lseg(M, N, "MP", 1, t=.55, coul="otOrange!80!black")
c += [r"\node[lab,text=otGreenDark,anchor=north] at (3.3,-.62) {$MP^2 = MH^2 + HP^2 > MH^2$};"]
c += pt(M, "M", 90) + pt(H, "H", 210, "otGreenDark") + pt(N, "P", 330)
FIGURES["ex_delta_corrige"] = figure(1.0, c)

# ------------------------------------------------------------------ 3750 (corrigé) : triangle SOA et hauteur SO
U = .9
A, B, C, D = (0, 0), (4, 0), (5.4, 1.5), (1.4, 1.5)
O = (2.7, .75)
S = (2.7, 5)
c = coord(A=A, B=B, C=C, D=D, O=O, S=S)
c += [r"\fill[otSky] (A) -- (B) -- (S) -- cycle;", r"\fill[otSky!60] (B) -- (C) -- (S) -- cycle;",
      r"\fill[otGreen!22] (S) -- (O) -- (A) -- cycle;",
      r"\draw[cache] (A) -- (D) -- (C) (D) -- (S) (A) -- (C) (B) -- (D);",
      r"\draw[geoReponse,line width=1.3pt] (S) -- (O) -- (A);", r"\angledroit{S}{O}{A}",
      r"\draw[geoTrait] (A) -- (B) -- (C) -- (S) -- cycle (B) -- (S);"]
c += lseg(A, S, "9 \\text{ cm}", 1, U=U)
c += [r"\node[lab,text=otGreenDark,anchor=east] at (2.6,2.45) {$3\sqrt{7}$};"]
c += [r"\cote[.4]{B}{A}{$6$ cm}"]
c += pt(A, "A", 225, U=U) + pt(B, "B", 315, U=U) + pt(C, "C", 0, U=U) + pt(D, "D", 155, U=U)
c += pt(S, "S", 90, U=U) + pt(O, "O", 265, "otGreenDark", d=.2, U=U)
FIGURES["ex_pyramide_corrige"] = figure(U, c)

# ------------------------------------------------------------------ 3751 (corrigé) : x = 5, aire minimale 50 cm²
U = .46
A, B, C, D = (0, 0), (10, 0), (10, 10), (0, 10)
M, N, Pp, Q = (5, 0), (10, 5), (5, 10), (0, 5)
c = coord(A=A, B=B, C=C, D=D, M=M, N=N, P=Pp, Q=Q)
c += [r"\fill[otGreen!16] (M) -- (N) -- (P) -- (Q) -- cycle;",
      r"\draw[geoTrait] (A) -- (B) -- (C) -- (D) -- cycle;",
      r"\draw[geoReponse,line width=1.3pt] (M) -- (N) -- (P) -- (Q) -- cycle;"]
c += [r"\cote[.4]{M}{A}{%s}" % vert("$5$"), r"\cote[.4]{N}{B}{%s}" % vert("$5$"),
      r"\cote[.4]{P}{C}{%s}" % vert("$5$"), r"\cote[.4]{Q}{D}{%s}" % vert("$5$")]
c += [r"\node[lab,text=otGreenDark,align=center] at (5,5) {aire minimale\\$50$ cm²};"]
c += pt(A, "A", 225, U=U) + pt(B, "B", 315, U=U) + pt(C, "C", 45, U=U) + pt(D, "D", 135, U=U)
c += pt(M, "M", 90, "otGreenDark", d=.3, U=U) + pt(N, "N", 180, "otGreenDark", d=.3, U=U)
c += pt(Pp, "P", 270, "otGreenDark", d=.3, U=U) + pt(Q, "Q", 0, "otGreenDark", d=.3, U=U)
FIGURES["ex_carre_inscrit_corrige"] = figure(U, c)
