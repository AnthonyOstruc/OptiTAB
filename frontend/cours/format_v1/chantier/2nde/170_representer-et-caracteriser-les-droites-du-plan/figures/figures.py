# -*- coding: utf-8 -*-
"""Figures de la notion « Représenter et caractériser les droites du plan » (Seconde).

Compilées par outils/figures_livre.py, style des livres : quadrillage pâle,
axes gris, graduations Montserrat ; droites épaisses (bleu marine, vert,
orange, rouge) ; éléments de réponse en vert foncé ; pas de pente en
pointillés orange. Les étiquettes sont posées perpendiculairement aux
droites, dans l'espace libre (ancre numérique = direction opposée au décalage).
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grille/.style={otRule!75,line width=.35pt},
  grad/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt},
  dr/.style={line width=1.3pt,line cap=round},
  vec/.style={line width=1.3pt,line cap=round,-{Stealth[length=2.8mm,width=2.2mm]}},
  pas/.style={otOrange,line width=1pt,dash pattern=on 3.5pt off 2pt},
  aide/.style={otMuted,line width=.6pt,dash pattern=on 2.5pt off 1.8pt},
  lab/.style={text=otInk,inner sep=1pt},
  tit/.style={font=\otMedium\bfseries\fontsize{10}{12}\selectfont,text=otNavy},
  leg/.style={font=\otRegular\fontsize{9.5}{11.5}\selectfont,align=center},
}
"""

COUL = {"n": "otNavy", "v": "otGreen", "o": "otOrange", "r": "otRed", "g": "otGreenDark"}
TEXTE = {"n": "otNavy", "v": "otGreenDark", "o": "otOrange!85!black", "r": "otRed!90!black",
         "g": "otGreenDark"}


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


class Fig:
    def __init__(self, x0, x1, y0, y1, ux=0.7, uy=None, xt=None, yt=None, sx=1, sy=1,
                 noms=("$x$", "$y$"), axes=True):
        self.w = (x0, x1, y0, y1)
        self.ux, self.uy = ux, (uy if uy else ux)
        self.c = []
        self.c.append(r"\draw[grille,xstep=%s,ystep=%s] (%s,%s) grid (%s,%s);"
                      % (f(sx), f(sy), f(x0), f(y0), f(x1), f(y1)))
        if not axes:
            return
        ex, ey = 0.45 / self.ux, 0.45 / self.uy
        self.c.append(r"\draw[axe] (%s,0) -- (%s,0);" % (f(x0), f(x1 + ex)))
        self.c.append(r"\draw[axe] (0,%s) -- (0,%s);" % (f(y0), f(y1 + ey)))
        if xt is None:
            xt = [k for k in range(math.ceil(x0), int(x1) + 1, sx) if k]
        if yt is None:
            yt = [k for k in range(math.ceil(y0), int(y1) + 1, sy) if k]
        tx, ty = 0.07 / self.uy, 0.07 / self.ux
        for k in xt:
            self.c.append(r"\draw[otMuted,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(k), f(-tx), f(k), f(tx)))
            self.c.append(r"\node[grad,anchor=north] at ([yshift=-3pt]%s,0) {$%s$};" % (f(k), lab(k)))
        for k in yt:
            self.c.append(r"\draw[otMuted,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(-ty), f(k), f(ty), f(k)))
            self.c.append(r"\node[grad,anchor=east] at ([xshift=-3pt]0,%s) {$%s$};" % (f(k), lab(k)))
        self.c.append(r"\node[grad,anchor=north east] at ([xshift=-2pt,yshift=-2pt]0,0) {$0$};")
        self.c.append(r"\node[text=otMuted,anchor=west,inner sep=2pt] at (%s,0) {%s};" % (f(x1 + ex), noms[0]))
        self.c.append(r"\node[text=otMuted,anchor=south,inner sep=2pt] at (0,%s) {%s};" % (f(y1 + ey), noms[1]))

    # ---------------------------------------------------------------- droites
    def bornes(self, a, b, c):
        x0, x1, y0, y1 = self.w
        pts = []
        if b:
            for x in (x0, x1):
                y = -(a * x + c) / b
                if y0 - 1e-9 <= y <= y1 + 1e-9:
                    pts.append((x, y))
        if a:
            for y in (y0, y1):
                x = -(b * y + c) / a
                if x0 - 1e-9 <= x <= x1 + 1e-9:
                    pts.append((x, y))
        best, dm = None, -1
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                d = math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
                if d > dm:
                    best, dm = (pts[i], pts[j]), d
        return best

    def droite(self, a, b, c, k="n", style="dr", nom=None, t=None, cote=1, d=4):
        """Droite ax + by + c = 0 dans la fenêtre ; étiquette à l'abscisse t
        (à l'ordonnée t si la droite est verticale), du côté cote (1 = gauche du sens p→q)."""
        p, q = self.bornes(a, b, c)
        if p[0] > q[0] or (p[0] == q[0] and p[1] > q[1]):
            p, q = q, p
        self.c.append(r"\draw[%s,%s] %s -- %s;" % (style, COUL.get(k, k), P(p), P(q)))
        if nom:
            if b:
                m = (t, -(a * t + c) / b)
            else:
                m = (-c / a, t)
            dx, dy = (q[0] - p[0]) * self.ux, (q[1] - p[1]) * self.uy
            L = math.hypot(dx, dy)
            nx, ny = -dy / L * cote, dx / L * cote
            ang = math.degrees(math.atan2(ny, nx))
            self.c.append(r"\node[lab,text=%s,anchor=%s] at ([shift={(%d:%spt)}]%s,%s) {%s};"
                          % (TEXTE.get(k, k), coin(nx, ny), round(ang), f(d), f(m[0]), f(m[1]), nom))

    def deux_points(self, p, q, **kw):
        a = q[1] - p[1]
        b = p[0] - q[0]
        c = -(a * p[0] + b * p[1])
        self.droite(a, b, c, **kw)

    # ---------------------------------------------------------------- points, vecteurs, textes
    def pt(self, p, nom=None, ang=45, k="n", d=3.5):
        self.c.append(r"\fill[%s] %s circle (2.2pt);" % (COUL.get(k, k), P(p)))
        if nom:
            self.c.append(r"\node[lab,text=%s,anchor=%s] at ([shift={(%d:%spt)}]%s,%s) {%s};"
                          % (TEXTE.get(k, "otInk") if k != "n" else "otInk",
                             coin(math.cos(math.radians(ang)), math.sin(math.radians(ang))), ang, f(d),
                             f(p[0]), f(p[1]), nom))

    def vec(self, p, q, k="o", nom=None, cote=1, d=4, t=0.5):
        self.c.append(r"\draw[vec,%s] %s -- %s;" % (COUL.get(k, k), P(p), P(q)))
        if nom:
            dx, dy = (q[0] - p[0]) * self.ux, (q[1] - p[1]) * self.uy
            L = math.hypot(dx, dy)
            nx, ny = -dy / L * cote, dx / L * cote
            ang = math.degrees(math.atan2(ny, nx))
            m = (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
            self.c.append(r"\node[lab,text=%s,anchor=%s] at ([shift={(%d:%spt)}]%s,%s) {%s};"
                          % (TEXTE.get(k, k), coin(nx, ny), round(ang), f(d), f(m[0]), f(m[1]), nom))

    def pas(self, p, dx, dy, tx, ty, cx="below", cy="right", k="o"):
        """Pas de pente depuis p : horizontal dx puis vertical dy, avec étiquettes."""
        q = (p[0] + dx, p[1])
        r = (p[0] + dx, p[1] + dy)
        self.c.append(r"\draw[pas,%s] %s -- %s -- %s;" % (COUL.get(k, k), P(p), P(q), P(r)))
        ax = {"below": "north", "above": "south"}[cx]
        sy = -3 if cx == "below" else 3
        self.c.append(r"\node[lab,text=%s,anchor=%s] at ([yshift=%dpt]%s,%s) {%s};"
                      % (TEXTE.get(k, k), ax, sy, f(p[0] + dx / 2), f(p[1]), tx))
        ay = {"right": "west", "left": "east"}[cy]
        sx = 3 if cy == "right" else -3
        self.c.append(r"\node[lab,text=%s,anchor=%s] at ([xshift=%dpt]%s,%s) {%s};"
                      % (TEXTE.get(k, k), ay, sx, f(q[0]), f(p[1] + dy / 2), ty))

    def guides(self, p):
        self.c.append(r"\draw[aide] (%s,0) -- %s -- (0,%s);" % (f(p[0]), P(p), f(p[1])))

    def txt(self, p, s, anchor="center", k="otInk"):
        self.c.append(r"\node[lab,text=%s,anchor=%s] at %s {%s};" % (k, anchor, P(p), s))

    def code(self):
        return "\n".join([r"\begin{tikzpicture}[x=%scm,y=%scm]" % (f(self.ux), f(self.uy))]
                         + self.c + [r"\end{tikzpicture}"])


def lab(k):
    return str(k) if k >= 0 else "-%d" % (-k)


def coin(nx, ny):
    """Ancre qui place toute l'étiquette du côté (nx, ny) de la droite :
    le coin de la boîte le plus proche de la droite est posé au point décalé."""
    if abs(nx) < 0.15:
        return "south" if ny > 0 else "north"
    if abs(ny) < 0.15:
        return "west" if nx > 0 else "east"
    return ("south" if ny > 0 else "north") + " " + ("west" if nx > 0 else "east")


FIGURES = {}

# ====================================================================== COURS
# 1. vecteur directeur : d : 2x - 3y - 1 = 0, A(2;1), M(8;5), u(3;2)
F = Fig(-1, 9, -1, 6, ux=0.8)
F.droite(2, -3, -1, "n", nom=r"$d$", t=8.6, cote=-1)
F.vec((2, 1), (8, 5), "o", nom=r"$\overrightarrow{AM}$", cote=-1, d=5, t=0.55)
F.vec((1, 3), (4, 5), "g", nom=r"$\vec{u}\,(3\,;2)$", cote=1, d=4)
F.pt((2, 1), r"$A(2\,;1)$", 315, d=4)
F.pt((8, 5), r"$M(x\,;y)$", 120)
FIGURES["cours_vecteur_directeur"] = F.code()

# 2. pente : A(2;1), B(5;5)
F = Fig(-1, 7, -2, 6, ux=0.75, xt=[-1, 2, 3, 4, 5, 6, 7], yt=[-1, 1, 2, 3, 4, 5, 6])
F.deux_points((2, 1), (5, 5), k="n", nom=r"$(AB)$", t=5.6, cote=1)
F.pas((2, 1), 3, 4, r"$\Delta x = 3$", r"$\Delta y = 4$")
F.pt((2, 1), r"$A(2\,;1)$", 150)
F.pt((5, 5), r"$B(5\,;5)$", 150, d=4)
FIGURES["cours_pente"] = F.code()

# 3. panorama : d1 : y = 2x + 1 ; d2 : y = -x/2 + 2 ; d3 : y = -2 ; d4 : x = -3
F = Fig(-4, 6, -4, 6, ux=0.7, xt=[-4, -2, -1, 1, 2, 3, 4, 5, 6], yt=[-4, -3, -1, 3, 4, 5, 6])
F.droite(2, -1, 1, "n", nom=r"$d_1$", t=2.2, cote=-1)
F.droite(0.5, 1, -2, "v", nom=r"$d_2$", t=5.3, cote=-1)
F.droite(0, 1, 2, "o", nom=r"$d_3$", t=5.5, cote=-1)
F.droite(1, 0, 3, "r", nom=r"$d_4$", t=5.4, cote=-1)
FIGURES["cours_panorama"] = F.code()

# 4. trois cas d'un système
parts = []
cas = [("Sécantes", r"une seule\\solution", [((0.0, 0.2), (2.4, 1.9), "otNavy", ""), ((0.1, 2.0), (2.3, 0.1), "otOrange", "")], (1.2, 1.05)),
       ("Parallèles", r"aucune\\solution", [((0.0, 0.9), (2.4, 2.1), "otNavy", ""), ((0.0, 0.1), (2.4, 1.3), "otOrange", "")], None),
       ("Confondues", r"une infinité\\de solutions", [((0.0, 0.4), (2.4, 2.0), "otNavy", "line width=2.6pt"), ((0.0, 0.4), (2.4, 2.0), "otOrange", "dash pattern=on 4pt off 3pt")], None)]
for i, (titre, legende, droites, inter) in enumerate(cas):
    ox = i * 2.5
    parts.append(r"\begin{scope}[xshift=%scm]" % f(ox))
    parts.append(r"\draw[grille] (-.2,-.2) grid (2.4,2.2);")
    parts.append(r"\draw[axe] (-.2,0) -- (2.6,0);")
    parts.append(r"\draw[axe] (0,-.2) -- (0,2.4);")
    for p, q, col, extra in droites:
        parts.append(r"\draw[dr,%s%s] %s -- %s;" % (col, "," + extra if extra else "", P(p), P(q)))
    if inter:
        parts.append(r"\fill[otGreenDark] %s circle (2.4pt);" % P(inter))
    parts.append(r"\node[tit,anchor=south] at (1.1,2.55) {%s};" % titre)
    parts.append(r"\node[leg,text=otGreenDark,anchor=north] at (1.1,-.35) {%s};" % legende)
    parts.append(r"\end{scope}")
FIGURES["cours_trois_cas"] = "\n".join([r"\begin{tikzpicture}[x=0.8cm,y=0.8cm]"] + parts + [r"\end{tikzpicture}"])

# 5. intersection : y = 2x - 1 et x + y = 5, I(2;3)
F = Fig(-1, 6, -2, 6, ux=0.7, xt=[1, 3, 4, 5, 6], yt=[1, 2, 4, 5, 6])
F.droite(2, -1, -1, "n", nom=r"$y=2x-1$", t=3.1, cote=-1)
F.droite(1, 1, -5, "v", nom=r"$x+y=5$", t=4.6, cote=1)
F.guides((2, 3))
F.c.append(r"\node[grad,anchor=north,text=otGreenDark] at ([yshift=-3pt]2,0) {$2$};")
F.c.append(r"\node[grad,anchor=east,text=otGreenDark] at ([xshift=-3pt]0,3) {$3$};")
F.pt((2, 3), r"$I(2\,;3)$", 8, "g", d=7)
FIGURES["cours_intersection"] = F.code()

# ====================================================================== EXERCICES
# 2046 (remplacé) : lecture graphique, d1 : y = 2x - 1 ; d2 : y = -2x/3 + 2 ; d3 : x = -3
def lecture(corrige):
    F = Fig(-4, 5, -4, 5, ux=0.7, xt=[-2, -1, 1, 2, 3, 4, 5], yt=[-2, -1, 1, 3, 4, 5])
    # graduations utiles à la lecture (2 et -3 sur l'axe des ordonnées, -3 sur l'axe des
    # abscisses), décalées du côté libre des droites qui passent par ces graduations
    F.c.append(r"\draw[otMuted,line width=.5pt] (-.1,2) -- (.1,2) (-.1,-3) -- (.1,-3);")
    F.c.append(r"\node[grad,anchor=north east] at ([xshift=-3pt,yshift=-1pt]0,2) {$2$};")
    F.c.append(r"\node[grad,anchor=south east] at ([xshift=-3pt,yshift=1pt]0,-3) {$-3$};")
    F.c.append(r"\node[grad,anchor=north east] at ([xshift=-2pt,yshift=-3pt]-3,0) {$-3$};")
    F.droite(2, -1, -3, "n", nom=r"$d_1$", t=3.6, cote=-1)
    F.droite(2, 3, -6, "v", nom=r"$d_2$", t=4.3, cote=-1, d=5)
    F.droite(1, 0, 3, "o", nom=r"$d_3$", t=4.4, cote=-1)
    if corrige:
        F.pas((0, -3), 1, 2, r"$+1$", r"$+2$")
        F.pas((0, 2), 3, -2, r"$+3$", r"$-2$", cx="above")
        F.pt((0, -3), None, k="g")
        F.pt((0, 2), None, k="g")
    return F.code()


FIGURES["ex_lecture_enonce"] = lecture(False)
FIGURES["ex_lecture_corrige"] = lecture(True)

# 2045 : A(-2;3), B(4;-1), C(2;-5), D(2;4)
F = Fig(-3, 5, -6, 5, ux=0.6, xt=[-3, -2, -1, 1, 4, 5], yt=[-6, -5, -4, -3, -2, -1, 1, 3, 4, 5])
F.deux_points((-2, 3), (4, -1), k="n", nom=r"$(AB)$", t=4.6, cote=1)
F.droite(1, 0, -2, "v", nom=r"$(CD)$", t=2.6, cote=-1)
F.vec((-2, 3), (1, 1), "o", nom=r"$\vec{u}$", cote=-1, d=4, t=0.3)
F.pt((-2, 3), r"$A$", 60)
F.pt((4, -1), r"$B$", 240)
F.pt((2, -5), r"$C$", 0)
F.pt((2, 4), r"$D$", 0)
FIGURES["ex_vecteur_pente"] = F.code()

# 2051 q1 : A(-1;2), B(2;8), C(5;14) sur y = 2x + 4
F = Fig(-2, 6, -2, 16, ux=0.8, uy=0.36, sy=2, xt=[-2, 1, 2, 3, 4, 5, 6], yt=[2, 6, 8, 10, 12, 14, 16])
F.droite(2, -1, 4, "g")
F.pt((-1, 2), r"$A$", 135, d=4)
F.pt((2, 8), r"$B$", 135, d=4)
F.pt((5, 14), r"$C$", 135, d=4)
FIGURES["ex_align_q1"] = F.code()

# 2051 q2 : D(0;1), E(2;3), F(4;6) ; (DE) : y = x + 1
F = Fig(-1, 5, -1, 7, ux=0.75, yt=[-1, 2, 3, 4, 5, 6, 7], xt=[1, 2, 3, 4, 5])
F.deux_points((0, 1), (2, 3), k="n", nom=r"$(DE)$", t=4.6, cote=-1)
F.deux_points((0, 1), (4, 6), k="o", style="aide,line width=1pt")
F.pt((0, 1), r"$D$", 160)
F.pt((2, 3), r"$E$", 300)
F.pt((4, 6), r"$F$", 180, d=5)
FIGURES["ex_align_q2"] = F.code()

# 2051 q3 : G(1;-2), H(4;1), K(6;3) sur y = x - 3
F = Fig(-1, 7, -3, 4, ux=0.75, xt=[-1, 1, 2, 4, 5, 6, 7], yt=[-2, -1, 1, 2, 4])
F.droite(1, -1, -3, "n")
F.pt((1, -2), r"$G$", 135)
F.pt((4, 1), r"$H$", 135)
F.pt((6, 3), r"$K(6\,;3)$", 180, "g", d=5)
FIGURES["ex_align_q3"] = F.code()

# 2049 q1 : A(1;2), B(5;4) : y = x/2 + 3/2
F = Fig(-4, 6, -1, 5, ux=0.72, xt=[-4, -2, -1, 1, 2, 3, 4, 5, 6], yt=[-1, 1, 2, 3, 4, 5])
F.deux_points((1, 2), (5, 4), k="g", nom=r"$(AB)$", t=-2.6, cote=1)
F.pas((1, 2), 4, 2, r"$+4$", r"$+2$")
F.pt((1, 2), r"$A$", 135)
F.pt((5, 4), r"$B$", 135)
FIGURES["ex_eq_q1"] = F.code()

# 2049 q2 : C(-3;1), pente -3 : y = -3x - 8
F = Fig(-5, 1, -3, 6, ux=0.72, xt=[-5, -4, -3, -2, -1, 1], yt=[-3, -2, -1, 1, 2, 3, 4, 5, 6])
F.droite(3, 1, 8, "g", nom=r"$y=-3x-8$", t=-4.5, cote=1, d=5)
F.pas((-4, 4), 1, -3, r"$+1$", r"$-3$", cx="above")
F.pt((-4, 4), None)
F.pt((-3, 1), r"$C$", 180, d=5)
FIGURES["ex_eq_q2"] = F.code()

# 2049 q3 : D(2;-1), u(4;-2) : x + 2y = 0
F = Fig(-3, 6, -3, 3, ux=0.75, xt=[-3, -2, -1, 1, 2, 3, 4, 5], yt=[-3, -2, -1, 1, 2, 3])
F.droite(1, 2, 0, "g", nom=r"$x+2y=0$", t=4.3, cote=1, d=5)
F.vec((2, -1), (6, -3), "o", nom=r"$\vec{u}\,(4\,;-2)$", cote=-1, d=5, t=0.45)
F.pt((2, -1), r"$D$", 225, d=4)
FIGURES["ex_eq_q3"] = F.code()

# 2049 q4 : E(-5;3), F(-5;-2) : x = -5
F = Fig(-6, 1, -3, 4, ux=0.75, xt=[-6, -4, -3, -2, -1, 1], yt=[-3, -2, -1, 1, 2, 3, 4])
F.droite(1, 0, 5, "g", nom=r"$x=-5$", t=-2.6, cote=-1, d=5)
F.pt((-5, 3), r"$E$", 0, d=5)
F.pt((-5, -2), r"$F$", 0, d=5)
FIGURES["ex_eq_q4"] = F.code()

# 2049 q5 : I(-2;4), J(3;-1) : x + y - 2 = 0
F = Fig(-3, 4, -2, 5, ux=0.75, xt=[-3, -2, -1, 1, 3, 4], yt=[-2, -1, 1, 3, 4, 5])
F.droite(1, 1, -2, "g", nom=r"$x+y-2=0$", t=3.2, cote=-1, d=5)
F.pt((-2, 4), r"$I$", 45, d=4)
F.pt((3, -1), r"$J$", 45, d=4)
FIGURES["ex_eq_q5"] = F.code()

# 2047 : d : y = -3x + 2 ; parallèle par B(0;5) : y = -3x + 5 ; C(3;-4)
F = Fig(-2, 4, -5, 6, ux=0.62, xt=[-2, -1, 1, 2, 3, 4], yt=[-5, -4, -3, -2, -1, 1, 4])
F.droite(3, 1, -2, "n", nom=r"$d$", t=-0.9, cote=-1, d=5)
F.droite(3, 1, -5, "g", nom=r"$d'$", t=2.4, cote=1, d=5)
F.pt((0, 5), r"$B$", 30, "g", d=5)
F.pt((3, -4), r"$C$", 0, "g", d=5)
FIGURES["ex_parallele"] = F.code()

# 2052 q1 : d1 : 2x - 3y + 1 = 0 ; d2 : 4x - 6y - 5 = 0
F = Fig(-3, 5, -3, 4, ux=0.75, xt=[-3, -2, 1, 2, 3, 4, 5], yt=[-3, -2, 1, 2, 3, 4])
F.droite(2, -3, 1, "n", nom=r"$d_1$", t=4, cote=1, d=5)
F.droite(4, -6, -5, "o", nom=r"$d_2$", t=3.8, cote=-1, d=5)
FIGURES["ex_pos_q1"] = F.code()

# 2052 q2 : d3 = d4 : y = x/2 - 1
F = Fig(-3, 5, -3, 3, ux=0.75, xt=[-3, -2, -1, 1, 3, 4, 5], yt=[-3, -2, 1, 2, 3])
F.droite(1, -2, -2, "n", style="dr,line width=2.8pt", nom=r"$d_3$", t=-1.4, cote=1, d=5)
F.droite(1, -2, -2, "o", style="dr,dash pattern=on 4pt off 3pt", nom=r"$d_4$", t=3.6, cote=-1, d=5)
FIGURES["ex_pos_q2"] = F.code()

# 2052 q3 : x = -3 et x = 1/2
F = Fig(-4, 2, -2, 3, ux=0.8, xt=[-2, -1, 2], yt=[-2, -1, 1, 2, 3])  # sans « -4 », collé à « -3 »
F.droite(1, 0, 3, "n", nom=r"$d_5$", t=2.4, cote=-1, d=4)
F.droite(2, 0, -1, "o", nom=r"$d_6$", t=2.4, cote=-1, d=4)
F.c.append(r"\node[grad,anchor=north east] at ([xshift=-1pt,yshift=-3pt]-3,0) {$-3$};")
F.c.append(r"\node[grad,anchor=north west] at ([xshift=1pt,yshift=-3pt]0.5,0) {$\dfrac{1}{2}$};")  # \dfrac : lisible sur téléphone
FIGURES["ex_pos_q3"] = F.code()

# 2052 q4 : d7 : 3x + y - 4 = 0 ; parallèle par P(2;-1) : 3x + y - 5 = 0
F = Fig(-1, 5, -3, 6, ux=0.7, xt=[-1, 1, 3, 4, 5], yt=[-3, -2, -1, 1, 2, 3])
F.droite(3, 1, -4, "n", nom=r"$d_7$", t=-0.4, cote=-1, d=5)
F.droite(3, 1, -5, "g", nom=r"$3x+y-5=0$", t=2.62, cote=1, d=5)
F.pt((2, -1), r"$P$", 20, "g", d=5)
FIGURES["ex_pos_q4"] = F.code()

# 2052 q5 : d8 : y = -x + 4 ; d9 : y = 2x - 2 ; intersection (2;2)
F = Fig(-1, 5, -3, 5, ux=0.72, xt=[-1, 1, 3, 4, 5], yt=[-1, 1, 3, 5])
F.droite(1, 1, -4, "n", nom=r"$d_8$", t=-0.5, cote=-1, d=5)
F.droite(2, -1, -2, "o", nom=r"$d_9$", t=3.25, cote=-1, d=5)
F.guides((2, 2))
F.c.append(r"\node[grad,anchor=north,text=otGreenDark] at ([yshift=-3pt]2,0) {$2$};")
F.c.append(r"\node[grad,anchor=east,text=otGreenDark] at ([xshift=-3pt]0,2) {$2$};")
F.pt((2, 2), r"$(2\,;2)$", 8, "g", d=7)
FIGURES["ex_pos_q5"] = F.code()

# 2050 q1 : y = 3x/2 - 1, points (0;-1), (2;2)
F = Fig(-2, 4, -3, 4, ux=0.75, xt=[-2, -1, 1, 2, 3, 4], yt=[-3, 1, 2, 3, 4])
F.droite(3, -2, -2, "n", nom=r"$d_1$", t=-1.2, cote=1, d=5)
F.pt((0, -1), r"$(0\,;-1)$", 340, "g", d=6)
F.pt((2, 2), r"$(2\,;2)$", 340, "g", d=6)
FIGURES["ex_trace_q1"] = F.code()

# 2050 q2 : 4x + 2y - 8 = 0, points (2;0), (0;4)
F = Fig(-1, 4, -2, 5, ux=0.75, xt=[-1, 1, 3, 4], yt=[-2, -1, 1, 2, 3, 5])
F.droite(4, 2, -8, "n", nom=r"$d_2$", t=3.2, cote=1, d=5)
F.pt((2, 0), r"$(2\,;0)$", 30, "g", d=5)
F.pt((0, 4), r"$(0\,;4)$", 30, "g", d=5)
FIGURES["ex_trace_q2"] = F.code()

# 2050 q3 : x = 3, points (3;0), (3;2)
F = Fig(-1, 5, -2, 4, ux=0.75, xt=[-1, 1, 2, 4, 5], yt=[-2, -1, 1, 2, 3, 4])
F.droite(1, 0, -3, "n", nom=r"$d_3$", t=3.5, cote=-1, d=5)
F.pt((3, 0), r"$(3\,;0)$", 45, "g", d=5)
F.pt((3, 2), r"$(3\,;2)$", 0, "g", d=5)
FIGURES["ex_trace_q3"] = F.code()

# 2050 q4 : y = -x + 5, P(4;1)
F = Fig(-1, 6, -1, 6, ux=0.72, xt=[-1, 1, 2, 3, 4, 6], yt=[-1, 1, 2, 3, 4, 6])
F.droite(1, 1, -5, "n", nom=r"$d_4$", t=1.2, cote=-1, d=5)
F.pt((4, 1), r"$P(4\,;1)$", 45, "g", d=5)
FIGURES["ex_trace_q4"] = F.code()

# 2050 q5 : x - 2y + 6 = 0, points (0;3), (4;5)
F = Fig(-3, 6, -1, 6, ux=0.72, xt=[-3, -2, -1, 1, 2, 3, 4, 5, 6], yt=[-1, 1, 2, 4, 5, 6])
F.droite(1, -2, 6, "n", nom=r"$d_5$", t=-2.2, cote=1, d=5)
F.pt((0, 3), r"$(0\,;3)$", 300, "g", d=5)
F.pt((4, 5), r"$(4\,;5)$", 300, "g", d=5)
FIGURES["ex_trace_q5"] = F.code()

# nouveau-1 : 5a + 3e = 63 et 2a + 4e = 42, solution (9;6)
F = Fig(0, 14, 0, 12, ux=0.52, xt=[2, 4, 6, 8, 10, 12, 14], yt=[2, 4, 8, 10, 12], sx=1, sy=1,
        noms=(r"$a$", r"$e$"))
F.c = [c for c in F.c if "{$0$}" not in c]
F.c.append(r"\node[grad,anchor=north east] at ([xshift=-2pt,yshift=-2pt]0,0) {$0$};")
F.droite(5, 3, -63, "n", nom=r"$5a+3e=63$", t=11.3, cote=1, d=5)
F.droite(2, 4, -42, "o", nom=r"$2a+4e=42$", t=2.5, cote=1, d=5)
F.guides((9, 6))
F.c.append(r"\node[grad,anchor=north,text=otGreenDark] at ([yshift=-3pt]9,0) {$9$};")
F.c.append(r"\node[grad,anchor=east,text=otGreenDark] at ([xshift=-3pt]0,6) {$6$};")
F.pt((9, 6), r"$(9\,;6)$", 20, "g", d=7)
FIGURES["ex_systeme_tarifs"] = F.code()

# nouveau-2 : tarif A : y = 1,5x + 12 ; tarif B : y = 3x ; croisement (8;24)
F = Fig(0, 12, 0, 36, ux=0.5, uy=0.16, sx=1, sy=3, xt=[2, 4, 6, 10, 12], yt=[6, 12, 18, 30, 36],
        noms=(r"\otRegular\small durée (h)", r"\otRegular\small prix (€)"))
F.droite(1.5, -1, 12, "n", nom=r"tarif A", t=11, cote=-1, d=5)
F.droite(3, -1, 0, "o", nom=r"tarif B", t=10.5, cote=1, d=6)
F.guides((8, 24))
F.c.append(r"\node[grad,anchor=north,text=otGreenDark] at ([yshift=-3pt]8,0) {$8$};")
F.c.append(r"\node[grad,anchor=east,text=otGreenDark] at ([xshift=-3pt]0,24) {$24$};")
F.pt((8, 24), None, k="g")
FIGURES["ex_location"] = F.code()

# ====================================================================== FINITION 2026-11-02
# Figures d'énoncé (données seules) et figures de corrigé (réponse en vert).

# 2045 (énoncé) : les quatre points A, B, C, D
F = Fig(-3, 5, -6, 5, ux=0.6, xt=[-3, -2, -1, 1, 4, 5], yt=[-6, -5, -4, -3, -2, -1, 1, 3, 4, 5])
F.pt((-2, 3), r"$A$", 60)
F.pt((4, -1), r"$B$", 240)
F.pt((2, -5), r"$C$", 0)
F.pt((2, 4), r"$D$", 0)
FIGURES["ex_vecteur_pente_enonce"] = F.code()

# 2047 (énoncé) : la droite d, les points B et C
F = Fig(-2, 4, -5, 6, ux=0.62, xt=[-2, -1, 1, 2, 3, 4], yt=[-5, -4, -3, -2, -1, 1, 4])
F.droite(3, 1, -2, "n", nom=r"$d$", t=-0.9, cote=-1, d=5)
F.pt((0, 5), r"$B$", 30, d=5)
F.pt((3, -4), r"$C$", 0, d=5)
FIGURES["ex_parallele_enonce"] = F.code()

# 2054 q1 et q3 (corrigé) : (-1;0), (2;3), (5;6) sur la droite y = x + 1
F = Fig(-2, 6, -1, 7, ux=0.62, xt=[1, 3, 4, 6], yt=[-1, 2, 4, 5, 7])
F.droite(1, -1, 1, "g", nom=r"$y = x + 1$", t=4.6, cote=-1, d=5)
F.pt((-1, 0), r"$(-1\,;0)$", 120, d=4)
F.pt((2, 3), r"$(2\,;3)$", 135, d=4)
F.pt((5, 6), r"$(5\,;6)$", 135, d=4)
FIGURES["ex_python_q1"] = F.code()

# 2054 q2 (corrigé) : (0;1), (2;2) et (4;6) non alignés
F = Fig(-1, 5, -1, 7, ux=0.7, xt=[1, 2, 3, 4, 5], yt=[-1, 2, 3, 4, 5, 6, 7])
F.deux_points((0, 1), (2, 2), k="n")
F.deux_points((0, 1), (4, 6), k="o", style="aide,line width=1pt")
F.pt((0, 1), r"$(0\,;1)$", 120, d=4)
F.pt((2, 2), r"$(2\,;2)$", 300, d=4)
F.pt((4, 6), r"$(4\,;6)$", 180, "o", d=5)
FIGURES["ex_python_q2"] = F.code()

# 2054 q5 (corrigé) : (2;-1) et (2;5) sur la droite x = 2
F = Fig(-1, 4, -2, 6, ux=0.7, xt=[-1, 1, 3, 4], yt=[-2, -1, 1, 2, 3, 4, 5, 6])
F.droite(1, 0, -2, "g", nom=r"$x = 2$", t=2.6, cote=-1, d=5)
F.c.append(r"\node[grad,anchor=north west] at ([xshift=1pt,yshift=-3pt]2,0) {$2$};")
F.pt((2, -1), r"$(2\,;-1)$", 0, d=5)
F.pt((2, 5), r"$(2\,;5)$", 0, d=5)
FIGURES["ex_python_q5"] = F.code()

# 2048 (corrigé) : d1 : y = -2x + 3 ; d2 : y = 3x/2 + 3 ; d3 : y = -x/2 + 3/2 ; d4 : x = -4
F = Fig(-5, 4, -3, 6, ux=0.62, xt=[-3, -1, 1, 2, 4], yt=[-3, -2, -1, 1, 2, 5, 6])
F.droite(2, 1, -3, "n", nom=r"$d_1$", t=2.6, cote=1, d=5)
F.droite(3, -2, 6, "v", nom=r"$d_2$", t=1.6, cote=1, d=5)
F.droite(1, 2, -3, "o", nom=r"$d_3$", t=-2.5, cote=1, d=5)
F.droite(1, 0, 4, "r", nom=r"$d_4$", t=5.4, cote=1, d=4)
F.c.append(r"\node[grad,anchor=north east] at ([xshift=-2pt,yshift=-3pt]-4,0) {$-4$};")
F.c.append(r"\node[grad,anchor=east,text=otGreenDark] at ([xshift=-3pt]0,3) {$3$};")
F.pt((0, 3), None, k="g")
F.pt((0, 1.5), None, k="g")
FIGURES["ex_lire_eq"] = F.code()

# 2053 q1 (corrigé) : 2x + y = 8 et x - y = 1, solution (3;2)
F = Fig(-1, 6, -2, 8, ux=0.6, xt=[-1, 2, 5, 6], yt=[-2, 1, 3, 4, 5, 6, 7, 8])
F.droite(2, 1, -8, "n", nom=r"$2x + y = 8$", t=0.8, cote=1, d=5)
F.droite(1, -1, -1, "o", nom=r"$x - y = 1$", t=5.3, cote=-1, d=5)
F.guides((3, 2))
F.c.append(r"\node[grad,anchor=north,text=otGreenDark] at ([yshift=-3pt]3,0) {$3$};")
F.c.append(r"\node[grad,anchor=east,text=otGreenDark] at ([xshift=-3pt]0,2) {$2$};")
F.pt((3, 2), r"$(3\,;2)$", 0, "g", d=7)
FIGURES["ex_sys_q1"] = F.code()

# 2053 q2 (corrigé) : y = -2x + 3 et y = -2x + 5, parallèles distinctes
F = Fig(-1, 4, -3, 6, ux=0.62, xt=[-1, 1, 2, 3, 4], yt=[-3, -2, -1, 1, 2, 5])
F.droite(2, 1, -3, "n", nom=r"$d$", t=2.6, cote=-1, d=5)
F.droite(2, 1, -5, "o", nom=r"$d'$", t=3.4, cote=1, d=5)
FIGURES["ex_sys_q2"] = F.code()

# 2053 q3 (corrigé) : 3x - y + 6 = 0 et 6x - 2y + 12 = 0, une seule droite y = 3x + 6
F = Fig(-4, 2, -3, 8, ux=0.62, xt=[-4, -3, -1, 1, 2], yt=[-3, -2, -1, 1, 2, 3, 4, 5, 7, 8])
F.droite(3, -1, 6, "n", style="dr,line width=2.8pt", nom=r"$3x - y + 6 = 0$", t=-3.1, cote=-1, d=5)
F.droite(6, -2, 12, "o", style="dr,dash pattern=on 4pt off 3pt", nom=r"$6x - 2y + 12 = 0$", t=0.15, cote=-1, d=5)
FIGURES["ex_sys_q3"] = F.code()
