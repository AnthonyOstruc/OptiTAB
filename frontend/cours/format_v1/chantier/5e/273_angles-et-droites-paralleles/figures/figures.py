# -*- coding: utf-8 -*-
r"""Figures de la notion 273 (5e : angles et droites parallèles), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>

Conventions :
- traits des figures en bleu marine ; angles DONNÉS en orange dans les énoncés ;
- dans les corrigés, angles trouvés ou égaux en vert foncé (otGreenDark) ;
- une paire d'angles = une couleur (cours) ; un arc simple pour les angles aigus,
  un arc double pour les angles obtus d'une même configuration ;
- rapporteur dessiné degré par degré (deux graduations, intérieure et extérieure).

Toutes les figures sont construites en vraie grandeur (cm) à partir des mesures
de l'énoncé. Chaque arc qui porte une mesure est enregistré dans DONNEES
(sommet, un point de chaque côté, mesure annoncée) ; verif_273.py recalcule
avec sympy l'angle dessiné et le compare à la mesure écrite. Les droites
annoncées parallèles (ou non) sont aussi enregistrées.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  lab/.style={text=otInk,inner sep=0pt},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,inner sep=0pt},
  grad/.style={font=\otRegular\fontsize{8}{9.5}\selectfont,text=otMuted,inner sep=0pt},
  rep/.style={otGreenDark,line width=1.1pt,line join=round},
  aide/.style={otGreenDark,line width=.8pt,dash pattern=on 4pt off 2.5pt},
  bord/.style={otMuted,line width=.6pt},
  tic/.style={otMuted,line width=.35pt},
}
"""

OR = "otOrange!90!black"
VE = "otGreenDark"
NA = "otNavy"
RG = "otRed!85!black"

FIGURES = {}
DONNEES = {}


# ====================================================================== outils
def f(v):
    s = ("%.3f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def pol(p, L, deg):
    a = math.radians(deg)
    return (p[0] + L * math.cos(a), p[1] + L * math.sin(a))


def direc(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def deg(v):
    return r"$%s^{\circ}$" % v


def vert(t):
    return r"\textcolor{otGreenDark}{%s}" % t


def secteur(P, t_ligne, t_sec, pos):
    """Deux points (un sur chaque côté) de l'angle formé en P par une droite de direction
    t_ligne (vers la droite) et une sécante de direction t_sec (vers le haut).
    pos : hd (haut-droite), hg, bg, bd ; l'angle va de p à q dans le sens direct."""
    a1, a2 = {"hd": (t_ligne, t_sec), "hg": (t_sec, t_ligne + 180),
              "bg": (t_ligne + 180, t_sec + 180), "bd": (t_sec + 180, t_ligne + 360)}[pos]
    return pol(P, 1, a1), pol(P, 1, a2)


class Fig:
    """Figure TikZ en cm. Les arcs portant une mesure sont enregistrés pour verif_273.py."""

    def __init__(self, nom):
        self.ident = nom
        self.s = []
        self.d = DONNEES.setdefault(nom, {"angles": [], "paralleles": [], "secantes": []})

    def P(self, p):
        return "(%s,%s)" % (f(p[0]), f(p[1]))

    def add(self, *l):
        self.s += list(l)

    def code(self):
        FIGURES[self.ident] = "\n".join([r"\begin{tikzpicture}[line cap=round,line join=round]"]
                                      + self.s + [r"\end{tikzpicture}"])
        return FIGURES[self.ident]

    # ---------------------------------------------------------------- tracés
    def seg(self, p, q, style="geoTrait"):
        self.add(r"\draw[%s] %s -- %s;" % (style, self.P(p), self.P(q)))

    def droite(self, p, t, a, b, style="geoTrait"):
        """Morceau de droite passant par p, de direction t (degrés), de -a à +b."""
        p1, p2 = pol(p, -a, t), pol(p, b, t)
        self.seg(p1, p2, style)
        return p1, p2

    def fill(self, pts, coul="otSky"):
        self.add(r"\fill[%s] %s -- cycle;" % (coul, " -- ".join(self.P(p) for p in pts)))

    def texte(self, p, txt, anchor="center", style="lab", coul=None):
        c = (",text=%s" % coul) if coul else ""
        self.add(r"\node[%s%s,anchor=%s] at %s {%s};" % (style, c, anchor, self.P(p), txt))

    def nom(self, p, txt, ang, d=0.14, coul="otInk"):
        """Étiquette posée à distance d de p, dans la direction ang (ancre opposée)."""
        q = pol(p, d, ang)
        noms = ["west", "south west", "south", "south east", "east", "north east", "north", "north west"]
        anc = noms[int(round((ang % 360) / 45)) % 8]
        self.add(r"\node[lab,text=%s,anchor=%s] at %s {%s};" % (coul, anc, self.P(q), txt))

    def pt(self, p, txt=None, ang=90, d=0.15, coul=NA, tc="otInk"):
        self.add(r"\fill[%s] %s circle (1.8pt);" % (coul, self.P(p)))
        if txt:
            self.nom(p, "$%s$" % txt, ang, d, tc)

    def bout(self, p, t, txt, coul="otInk", d=0.1):
        """Nom d'une droite écrit dans son prolongement (au-delà de l'extrémité p, direction t)."""
        self.nom(p, txt, t, d, coul)

    # ---------------------------------------------------------------- angles
    def arc(self, o, p, q, r=0.45, txt=None, n=1, coul=OR, plein=True, lr=None, am=None, val=None, op=.16):
        """Angle de sommet o, de [op) à [oq) dans le sens direct ; texte sur la bissectrice
        (ou dans la direction am) à la distance lr ; val = mesure annoncée (contrôlée)."""
        a1, a2 = direc(o, p), direc(o, q)
        sw = (a2 - a1) % 360
        assert 0 < sw <= 180.0001, (self.ident, sw)
        a2 = a1 + sw
        if val is not None:
            self.d["angles"].append((o, p, q, val))
        if plein:
            self.add(r"\fill[%s,opacity=%s] %s -- %s arc (%s:%s:%s) -- cycle;"
                     % (coul, op, self.P(o), self.P(pol(o, r, a1)), f(a1), f(a2), f(r)))
        for i in range(n):
            rr = r + 0.075 * i
            self.add(r"\draw[%s,line width=.8pt] %s arc (%s:%s:%s);"
                     % (coul, self.P(pol(o, rr, a1)), f(a1), f(a2), f(rr)))
        if txt:
            if am is None:
                am = a1 + sw / 2
            if lr is None:
                lr = max(r + 0.075 * (n - 1) + 0.3, 0.36 / math.sin(math.radians(max(sw, 8) / 2)))
                lr = min(lr, r + 1.2)
            self.add(r"\node[lab,text=%s,anchor=center] at %s {%s};" % (coul, self.P(pol(o, lr, am)), txt))

    def num(self, o, p, q, txt, r=0.3, lr=0.62, coul=NA, arc=True):
        """Angle numéroté : petit arc (facultatif) et numéro sur la bissectrice."""
        a1, a2 = direc(o, p), direc(o, q)
        sw = (a2 - a1) % 360
        if arc:
            self.add(r"\draw[%s,line width=.6pt] %s arc (%s:%s:%s);" % (coul, self.P(pol(o, r, a1)), f(a1), f(a1 + sw), f(r)))
        self.add(r"\node[lab,text=%s,font=\bfseries,anchor=center] at %s {%s};"
                 % (coul, self.P(pol(o, lr, a1 + sw / 2)), txt))

    def droit(self, o, t1, t2, s=0.24, coul=NA):
        """Codage d'angle droit en o entre les directions t1 et t2."""
        u, v = pol(o, s, t1), pol(o, s, t2)
        w = (u[0] + v[0] - o[0], u[1] + v[1] - o[1])
        self.add(r"\draw[%s,line width=.6pt] %s -- %s -- %s;" % (coul, self.P(u), self.P(w), self.P(v)))

    # ---------------------------------------------------------------- relations de droites
    def paralleles(self, t1, t2, *noms):
        self.d["paralleles"].append((t1, t2, noms))

    def secantes(self, t1, t2, *noms):
        self.d["secantes"].append((t1, t2, noms))


def legende(F, p, txt, coul="otMuted"):
    F.texte(p, txt, "north", "petit", coul)


def titre(F, p, txt, coul=NA):
    F.texte(p, txt, "south", "txt", coul)


# ====================================================================== rapporteur
def rapporteur(F, R=3.4, lab_ext=0.5, lab_int=0.95):
    """Rapporteur centré en (0,0), ligne du zéro sur l'axe horizontal.
    Graduation extérieure : 0 à droite ; graduation intérieure : 0 à gauche."""
    O = (0.0, 0.0)
    F.add(r"\fill[otSky,opacity=.55] (%s,0) arc (0:180:%s) -- (%s,-.22) -- (%s,-.22) -- cycle;"
          % (f(R), f(R), f(-R), f(R)))
    F.add(r"\draw[bord] (%s,-.22) -- (%s,0) arc (0:180:%s) -- (%s,-.22) -- cycle;"
          % (f(R), f(R), f(R), f(-R)))
    F.add(r"\draw[bord] (%s,0) arc (0:180:%s);" % (f(R - 1.35), f(R - 1.35)))
    for t in range(0, 181):
        L = 0.3 if t % 10 == 0 else (0.2 if t % 5 == 0 else 0.11)
        F.seg(pol(O, R, t), pol(O, R - L, t), "tic")
    for t in range(0, 181, 20):   # nombres de 20 en 20 (lisibles sur téléphone)
        for rr, v in ((R - lab_ext, t), (R - lab_int, 180 - t)):
            p = pol(O, rr, t)
            if t in (0, 180):   # graduations 0 et 180 : au-dessus de la ligne du zéro
                F.texte((p[0], 0.2), str(v), "center", "grad")
            else:
                F.texte(p, str(v), "center", "grad")
    # repère du centre
    F.seg((0, 0), (0, 0.32), "tic")
    F.seg((-0.18, 0), (0.18, 0), "tic")


def fig_rapporteur(nom, t_x, t_y, val, corr=False, x="x", y="y", coulA=OR, montre=False):
    """Angle xOy posé sur le rapporteur : [Ox) sur la ligne du zéro (direction t_x = 0 ou 180)."""
    F = Fig(nom)
    R = 3.4
    O = (0.0, 0.0)
    rapporteur(F, R)
    X = pol(O, R + 0.55, t_x)
    Y = pol(O, R + 0.75, t_y)
    F.seg(O, X, "geoTrait,line width=1.1pt")
    F.seg(O, Y, "geoTrait,line width=1.1pt")
    p, q = (X, Y) if (t_y - t_x) % 360 <= 180 else (Y, X)
    coul = VE if corr else coulA
    F.arc(O, p, q, 0.55, (vert(deg(val)) if corr else (deg(val) if montre else None)), 1, coul, True, lr=1.05, val=val)
    F.bout(X, t_x, "$%s$" % x)
    F.bout(Y, t_y, "$%s$" % y)
    F.pt(O)
    F.nom((0, -0.22), "$O$", 270, 0.1)
    return F.code()


# ====================================================================== COURS
def cours_rapporteur():
    return fig_rapporteur("cours_rapporteur", 0, 128, 128, x="x", y="y", montre=True)


def cours_vocabulaire():
    F = Fig("cours_vocabulaire")
    # --- adjacents
    O = (0.0, 0.0)
    A, B, C = pol(O, 2.1, 0), pol(O, 2.1, 38), pol(O, 2.1, 92)
    for P in (A, B, C):
        F.seg(O, P)
    F.arc(O, A, B, 0.6, None, 1, OR)
    F.arc(O, B, C, 0.6, None, 1, NA)
    F.seg(O, B, "geoTrait,line width=1.6pt")
    F.pt(O, "O", 225)
    F.nom(A, "$A$", 0, 0.1)
    F.nom(B, "$B$", 38, 0.1)
    F.nom(C, "$C$", 92, 0.1)
    legende(F, (1.0, -0.42), "adjacents")
    # --- complémentaires
    O2 = (3.6, 0.0)
    A2, B2, C2 = pol(O2, 2.1, 0), pol(O2, 2.1, 28), pol(O2, 2.1, 90)
    for P in (A2, B2, C2):
        F.seg(O2, P)
    F.arc(O2, A2, B2, 0.75, deg(28), 1, OR, lr=1.45, val=28)
    F.arc(O2, B2, C2, 0.75, deg(62), 1, NA, lr=1.2, val=62)
    F.pt(O2)
    legende(F, (4.6, -0.42), "complémentaires")
    # --- supplémentaires
    O3 = (2.6, -2.6)
    A3, B3, C3 = pol(O3, 2.3, 0), pol(O3, 2.3, 28), pol(O3, 2.3, 180)
    F.seg(C3, A3)
    F.seg(O3, B3)
    F.arc(O3, A3, B3, 0.75, deg(28), 1, OR, lr=1.45, val=28)
    F.arc(O3, B3, C3, 0.55, deg(152), 1, NA, lr=0.95, val=152)
    F.pt(O3)
    legende(F, (O3[0], O3[1] - 0.3), "supplémentaires")
    return F.code()


def cours_opposes():
    F = Fig("cours_opposes")
    O = (0.0, 0.0)
    B, C, A, D = pol(O, 2.3, 0), pol(O, 2.3, 40), pol(O, 2.3, 180), pol(O, 2.3, 220)
    F.seg(A, B)
    F.seg(D, C)
    F.arc(O, B, C, 0.5, deg(40), 1, OR, val=40)
    F.arc(O, A, D, 0.5, deg(40), 1, OR, val=40)
    F.arc(O, C, A, 0.42, deg(140), 2, NA, lr=0.95, val=140)
    F.arc(O, D, B, 0.42, deg(140), 2, NA, lr=0.95, val=140)
    F.pt(O)
    F.nom(O, "$O$", 70, 0.62)
    for P, n, t in ((A, "A", 180), (B, "B", 0), (C, "C", 40), (D, "D", 220)):
        F.nom(P, "$%s$" % n, t, 0.1)
    F.secantes(0, 40, "(AB)", "(CD)")
    return F.code()


def config(F, A, B, td, te, ext_d=(2.2, 2.2), ext_e=(2.2, 2.2), ext_s=(1.2, 1.2),
           noms=("$(d)$", "$(e)$", "$(s)$"), style="geoTrait"):
    """Droite (d) par A (direction td), (e) par B (direction te), sécante (s) = (AB)."""
    ts = direc(B, A)
    d1, d2 = F.droite(A, td, ext_d[0], ext_d[1], style)
    e1, e2 = F.droite(B, te, ext_e[0], ext_e[1], style)
    s2 = pol(A, ext_s[0], ts)
    s1 = pol(B, ext_s[1], ts + 180)
    F.seg(s1, s2, style)
    if noms[0]:
        F.bout(d2, td, noms[0])
    if noms[1]:
        F.bout(e2, te, noms[1])
    if noms[2]:
        F.bout(s2, ts, noms[2])
    return ts


def cours_secante():
    """Deux droites non parallèles et une sécante : alternes-internes, puis correspondants."""
    F = Fig("cours_secante")
    td, ts = -9, 56
    for k, (dy, nomfig) in enumerate(((0.0, "Angles alternes-internes"), (-5.2, "Angles correspondants"))):
        B = (0.0, dy)
        A = pol(B, 2.5, ts)
        if k == 0:
            # bande intérieure entre (d) et (e)
            xs = (-2.2, A[0] + 2.4)
            yd = [A[1] + (x - A[0]) * math.tan(math.radians(td)) for x in xs]
            F.fill([(xs[0], dy), (xs[1], dy), (xs[1], yd[1]), (xs[0], yd[0])], "otSky")
        config(F, A, B, td, 0, ext_d=(A[0] + 2.2, 2.4), ext_e=(2.2, A[0] + 2.4))
        if k == 0:
            p, q = secteur(A, td, ts, "bg")
            F.arc(A, p, q, 0.42, None, 1, OR)
            p, q = secteur(B, 0, ts, "hd")
            F.arc(B, p, q, 0.42, None, 1, OR)
            F.texte((-2.0, dy + 0.3), "intérieur", "west", "petit")
        else:
            p, q = secteur(A, td, ts, "hd")
            F.arc(A, p, q, 0.42, None, 1, VE)
            p, q = secteur(B, 0, ts, "hd")
            F.arc(B, p, q, 0.42, None, 1, VE)
        F.pt(A, "A", 120, 0.2)
        F.pt(B, "B", 300, 0.2)
        F.texte((-2.2, dy + 3.55), nomfig, "south west", "txt", OR if k == 0 else VE)
        F.secantes(td, 0, "(d)", "(e)")
    return F.code()


def cours_paralleles():
    F = Fig("cours_paralleles")
    ts = 50
    B = (0.0, 0.0)
    A = (2.3 / math.tan(math.radians(ts)), 2.3)
    config(F, A, B, 0, 0, ext_d=(A[0] + 2.0, 2.2), ext_e=(2.0, A[0] + 2.2), ext_s=(1.4, 1.4))
    for P in (A, B):
        for pos in ("hd", "bg"):
            p, q = secteur(P, 0, ts, pos)
            F.arc(P, p, q, 0.42, deg(50), 1, OR, val=50)
        for pos in ("hg", "bd"):
            p, q = secteur(P, 0, ts, pos)
            F.arc(P, p, q, 0.36, deg(130), 2, NA, lr=0.82, val=130)
    F.paralleles(0, 0, "(d)", "(e)")
    return F.code()


def cours_construire():
    """Construire la parallèle à (d) passant par M en reportant un angle correspondant."""
    F = Fig("cours_construire")
    ts = 60
    A = (0.0, 0.0)
    M = pol(A, 2.6, ts)
    F.droite(A, 0, 2.0, 3.6)
    F.bout(pol(A, 3.6, 0), 0, "$(d)$")
    s2 = pol(M, 1.1, ts)
    F.seg(pol(A, 1.0, ts + 180), s2)
    F.droite(M, 0, 2.0 + M[0], 3.6 - M[0], "rep")
    F.bout(pol(M, 3.6 - M[0], 0), 0, vert("$(e)$"))
    p, q = secteur(A, 0, ts, "hd")
    F.arc(A, p, q, 0.5, deg(60), 1, OR, val=60)
    p, q = secteur(M, 0, ts, "hd")
    F.arc(M, p, q, 0.5, vert(deg(60)), 1, VE, val=60)
    F.pt(A, "A", 300, 0.2)
    F.pt(M, "M", 120, 0.2)
    F.paralleles(0, 0, "(d)", "(e)")
    return F.code()


# ====================================================================== EXERCICES
# --- 2959 : vocabulaire (adjacents, complémentaires, supplémentaires)
def ex2959(corr):
    F = Fig("ex2959_" + ("corrige" if corr else "enonce"))
    O = (0.0, 0.0)
    L = 2.5
    A, B, C, D = pol(O, L, 0), pol(O, L, 34), pol(O, L, 90), pol(O, L, 180)
    F.seg(D, A)
    F.seg(O, B)
    F.seg(O, C)
    F.droit(O, 90, 180)
    F.arc(O, A, B, 0.62, deg(34), 1, OR, lr=1.32, val=34)
    if corr:
        F.arc(O, B, C, 0.62, vert(deg(56)), 1, VE, lr=1.3, val=56)
        F.arc(O, B, D, 1.0, vert(deg(146)), 2, VE, plein=False, lr=1.55, am=148, val=146)
    F.pt(O, "O", 270, 0.18)
    for P, n, t in ((A, "A", 0), (B, "B", 34), (C, "C", 90), (D, "D", 180)):
        F.nom(P, "$%s$" % n, t, 0.1)
    return F.code()


# --- 2957 : angles opposés par le sommet
def ex2957(corr):
    F = Fig("ex2957_" + ("corrige" if corr else "enonce"))
    O = (0.0, 0.0)
    L = 2.4
    B, C, A, D = pol(O, L, 0), pol(O, L, 142), pol(O, L, 180), pol(O, L, 322)
    F.seg(A, B)
    F.seg(C, D)
    F.arc(O, C, A, 0.55, deg(38), 1, OR, val=38)
    if corr:
        F.arc(O, D, B, 0.55, vert(deg(38)), 1, VE, val=38)
        F.arc(O, B, C, 0.42, vert(deg(142)), 2, VE, lr=0.95, val=142)
        F.arc(O, A, D, 0.42, vert(deg(142)), 2, VE, lr=0.95, val=142)
    F.pt(O)
    F.nom(O, "$O$", 40, 0.6)
    for P, n, t in ((A, "A", 180), (B, "B", 0), (C, "C", 142), (D, "D", 322)):
        F.nom(P, "$%s$" % n, t, 0.1)
    F.secantes(0, 142, "(AB)", "(CD)")
    return F.code()


# --- 2958 : reconnaître les angles (droites non parallèles), angles numérotés
TD58, TS58 = -12, 52


def base2958(F):
    B = (0.0, 0.0)
    A = pol(B, 2.9, TS58)
    config(F, A, B, TD58, 0, ext_d=(A[0] + 2.3, 2.3), ext_e=(2.3, A[0] + 2.3), ext_s=(1.2, 1.2))
    F.secantes(TD58, 0, "(d)", "(e)")
    return A, B


def ex2958_enonce():
    F = Fig("ex2958_enonce")
    A, B = base2958(F)
    for P, t, base in ((A, TD58, 0), (B, 0, 4)):
        for k, pos in enumerate(("hd", "hg", "bg", "bd")):
            p, q = secteur(P, t, TS58, pos)
            F.num(P, p, q, str(base + k + 1), lr=0.5, arc=False)
    return F.code()


def ex2958_corrige(paires, nom, interieur=False):
    """paires : liste de (couleur, [(sommet 'A'|'B', pos, numéro), …])."""
    F = Fig(nom)
    B0 = (0.0, 0.0)
    A0 = pol(B0, 2.9, TS58)
    if interieur:
        xs = (-2.3, A0[0] + 2.3)
        yd = [A0[1] + (x - A0[0]) * math.tan(math.radians(TD58)) for x in xs]
        F.fill([(xs[0], 0), (xs[1], 0), (xs[1], yd[1]), (xs[0], yd[0])], "otSky")
    A, B = base2958(F)
    sommets = {"A": (A, TD58), "B": (B, 0)}
    vus = {n for _, liste in paires for (_, _, n) in liste}
    for P, t, base in ((A, TD58, 0), (B, 0, 4)):
        for k, pos in enumerate(("hd", "hg", "bg", "bd")):
            if base + k + 1 not in vus:
                p, q = secteur(P, t, TS58, pos)
                F.num(P, p, q, str(base + k + 1), lr=0.5, coul="otMuted", arc=False)
    for coul, liste in paires:
        for (s, pos, n) in liste:
            P, t = sommets[s]
            p, q = secteur(P, t, TS58, pos)
            F.arc(P, p, q, 0.32, None, 1, coul, op=.22)
            F.num(P, p, q, str(n), r=0.32, coul=coul)
    return F.code()


# --- 2960 : rapporteur puis parallèle construite au rapporteur
def ex2960_construction(corr):
    F = Fig("ex2960_" + ("constr_corrige" if corr else "constr_enonce"))
    ts = 70
    A = (0.0, 0.0)
    B = pol(A, 3.0, ts)
    F.droite(A, 0, 2.2, 3.4)
    F.bout(pol(A, 3.4, 0), 0, "$(d)$")
    s2 = pol(B, 1.0, ts)
    F.seg(pol(A, 1.0, ts + 180), s2)
    F.bout(s2, ts, "$(s)$")
    p, q = secteur(A, 0, ts, "hd")
    F.arc(A, p, q, 0.5, deg(70), 1, OR, val=70)
    if corr:
        F.droite(B, 0, 2.2 + B[0], 3.4 - B[0], "rep")
        F.bout(pol(B, 3.4 - B[0], 0), 0, vert("$(e)$"))
        p, q = secteur(B, 0, ts, "hd")
        F.arc(B, p, q, 0.5, vert(deg(70)), 1, VE, val=70)
        p, q = secteur(B, 0, ts, "hg")
        F.arc(B, p, q, 0.38, vert(deg(110)), 2, VE, plein=False, lr=0.85, val=110)
        F.paralleles(0, 0, "(d)", "(e)")
    F.pt(A, "A", 240, 0.2)
    F.pt(B, "B", 205, 0.25)
    return F.code()


# --- 2962 : calculer les huit angles (parallèles), points nommés
def ex2962(corr):
    F = Fig("ex2962_" + ("corrige" if corr else "enonce"))
    ts = 62
    B = (0.0, 0.0)
    A = (2.5 / math.tan(math.radians(ts)), 2.5)
    M, N = (A[0] - 1.7, A[1]), (A[0] + 1.8, A[1])
    P, Q = (-1.8, 0.0), (1.7, 0.0)
    S, T = pol(A, 1.25, ts), pol(B, 1.25, ts + 180)
    config(F, A, B, 0, 0, ext_d=(2.25, 2.35), ext_e=(2.35, 2.25), ext_s=(1.75, 1.75))
    p, q = secteur(A, 0, ts, "hg")
    F.arc(A, p, q, 0.36, deg(118), 2, OR, lr=0.85, val=118)
    if corr:
        for (X, pos, v) in ((A, "hd", 62), (A, "bg", 62), (B, "hd", 62), (B, "bg", 62),
                            (A, "bd", 118), (B, "hg", 118), (B, "bd", 118)):
            p, q = secteur(X, 0, ts, pos)
            if v == 62:
                F.arc(X, p, q, 0.42, vert(deg(62)), 1, VE, val=62)
            else:
                F.arc(X, p, q, 0.36, vert(deg(118)), 2, VE, lr=0.85, val=118)
        F.paralleles(0, 0, "(d)", "(e)")
    for X, n, t in ((M, "M", 90), (N, "N", 90), (P, "P", 270), (Q, "Q", 270)):
        F.pt(X, n, t, 0.17)
    F.pt(S, "S", ts - 90, 0.17)
    F.pt(T, "T", ts - 90, 0.17)
    F.pt(A)
    F.nom(A, "$A$", 158, 0.75)
    F.pt(B)
    F.nom(B, "$B$", -22, 0.75)
    return F.code()


# --- 2961 : démontrer (ou non) un parallélisme
def ex2961(corr):
    F = Fig("ex2961_" + ("corrige" if corr else "enonce"))
    # figure 1 : alternes-internes 58° et 58°
    ts = 58
    B = (0.0, 0.0)
    A = (2.2 / math.tan(math.radians(ts)), 2.2)
    config(F, A, B, 0, 0, ext_d=(A[0] + 1.9, 2.1), ext_e=(1.9, A[0] + 2.1), ext_s=(1.0, 1.0))
    c = VE if corr else OR
    t = (lambda s: vert(s)) if corr else (lambda s: s)
    p, q = secteur(A, 0, ts, "bg")
    F.arc(A, p, q, 0.45, t(deg(58)), 1, c, val=58)
    p, q = secteur(B, 0, ts, "hd")
    F.arc(B, p, q, 0.45, t(deg(58)), 1, c, val=58)
    F.pt(A, "A", 120, 0.2)
    F.pt(B, "B", 300, 0.2)
    F.texte((-2.0, 3.0), "Figure 1", "south west", "txt", NA)
    if corr:
        F.paralleles(0, 0, "(d)", "(e)")
    # figure 2 : correspondants 73° et 75° (les droites ne sont pas parallèles)
    dy = -4.9
    ts2, td2 = 75, 2
    D = (0.0, dy)
    C = pol(D, 2.4, ts2)
    config(F, C, D, td2, 0, ext_d=(C[0] + 1.9, 2.1), ext_e=(1.9, C[0] + 2.1), ext_s=(1.0, 1.0),
           noms=("$(d')$", "$(e')$", "$(t)$"))
    c2 = RG if corr else OR
    p, q = secteur(C, td2, ts2, "hd")
    F.arc(C, p, q, 0.45, deg(73), 1, c2, val=73)
    p, q = secteur(D, 0, ts2, "hd")
    F.arc(D, p, q, 0.45, deg(75), 1, c2, val=75)
    F.pt(C, "C", 135, 0.2)
    F.pt(D, "D", 225, 0.2)
    F.texte((-2.0, dy + 3.0), "Figure 2", "south west", "txt", NA)
    F.secantes(td2, 0, "(d')", "(e')")
    return F.code()


# --- 2974 : deux angles intérieurs du même côté (112° et 68°)
def ex2974(corr):
    F = Fig("ex2974_" + ("corrige" if corr else "enonce"))
    ts = 68
    B = (0.0, 0.0)
    A = (2.4 / math.tan(math.radians(ts)), 2.4)
    config(F, A, B, 0, 0, ext_d=(2.3, 2.5), ext_e=(2.3, A[0] + 2.5), ext_s=(1.2, 1.2))
    p, q = secteur(A, 0, ts, "bd")
    F.arc(A, p, q, 0.36, deg(112), 2, OR, lr=0.85, val=112)
    p, q = secteur(B, 0, ts, "hd")
    F.arc(B, p, q, 0.45, deg(68), 1, OR, val=68)
    if corr:
        p, q = secteur(A, 0, ts, "bg")
        F.arc(A, p, q, 0.45, vert(deg(68)), 1, VE, val=68)
        F.paralleles(0, 0, "(d)", "(e)")
    F.pt(A, "A", 120, 0.2)
    F.pt(B, "B", 300, 0.2)
    return F.code()


# --- 2965 : la rampe d'escalier
def ex2965(corr):
    F = Fig("ex2965_" + ("corrige" if corr else "enonce"))
    t = 34
    P, Q = (0.0, 0.0), (3.6, 0.0)
    A = (0.0, 1.0)
    B = (3.6, 1.0 + 3.6 * math.tan(math.radians(t)))
    D, E = (0.0, 2.5), (3.6, B[1] + 1.1)
    R = pol(B, 1.15, t)
    # sol hachuré
    F.add(r"\fill[pattern=north east lines,pattern color=otMuted!70] (-0.9,-0.28) rectangle (5.0,0);")
    F.seg((-0.9, 0), (5.0, 0))
    F.bout((5.0, 0), 0, "$(s)$")
    # poteaux et rampe
    F.seg(P, (0.0, 2.95))
    F.bout((0.0, 2.95), 90, "$(d)$")
    F.seg(Q, (3.6, E[1] + 0.45))
    F.bout((3.6, E[1] + 0.45), 90, "$(e)$")
    r0 = pol(A, 0.8, t + 180)
    F.seg(r0, R, "geoTrait,line width=1.6pt")
    F.bout(R, t, "$(r)$")
    F.droit(P, 0, 90, coul=(VE if corr else NA))
    F.droit(Q, 0, 90, coul=(VE if corr else NA))
    F.arc(A, B, D, 0.5, deg(56), 1, OR, val=56)
    if corr:
        F.arc(B, R, E, 0.5, vert(deg(56)), 1, VE, val=56)
        F.arc(B, E, A, 0.4, vert(deg(124)), 2, VE, lr=0.9, val=124)
        H = (2.3, 1.0)
        F.seg((-0.7, 1.0), H, "aide")
        F.bout((-0.7, 1.0), 180, vert("$(h)$"))
        F.arc(A, H, B, 1.15, vert(deg(34)), 1, VE, lr=1.6, am=12, val=34)
        F.paralleles(90, 90, "(d)", "(e)")
    F.pt(P, "P", 135, 0.18)
    F.pt(Q, "Q", 135, 0.18)
    F.pt(A, "A", 135, 0.18)
    F.pt(B, "B", 340, 0.2)
    F.pt(D, "D", 180, 0.18)
    F.pt(E, "E", 0, 0.18)
    F.pt(R, "R", t - 90, 0.18)
    return F.code()


# --- 2971 : parallèle à la base d'un triangle
def ex2971(corr):
    F = Fig("ex2971_" + ("corrige" if corr else "enonce"))
    angB, angC = 48, 67
    L = 5.0
    B, C = (0.0, 0.0), (L, 0.0)
    BA = L * math.sin(math.radians(angC)) / math.sin(math.radians(180 - angB - angC))
    A = pol(B, BA, angB)
    D, E = (A[0] - 2.0, A[1]), (A[0] + 1.7, A[1])
    F.fill([A, B, C], "otSky")
    F.seg((A[0] - 2.55, A[1]), (A[0] + 2.25, A[1]))
    F.bout((A[0] + 2.25, A[1]), 0, "$(d)$")
    F.add(r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (F.P(A), F.P(B), F.P(C)))
    F.arc(B, C, A, 0.55, deg(48), 1, OR, val=48)
    F.arc(C, A, B, 0.5, deg(67), 2, OR, lr=1.05, val=67)
    if corr:
        F.arc(A, D, B, 0.5, vert(deg(48)), 1, VE, val=48)
        F.arc(A, C, E, 0.42, vert(deg(67)), 2, VE, lr=1.0, val=67)
        F.arc(A, B, C, 0.85, vert(deg(65)), 1, VE, op=.1, lr=1.3, val=65)
        F.paralleles(0, 0, "(d)", "(BC)")
    F.pt(A, "A", 90, 0.18)
    F.pt(B, "B", 225, 0.18)
    F.pt(C, "C", 315, 0.18)
    F.pt(D, "D", 90, 0.18)
    F.pt(E, "E", 90, 0.18)
    return F.code()


# --- 2972 : un point entre deux parallèles (synthèse)
def ex2972(corr):
    F = Fig("ex2972_" + ("corrige" if corr else "enonce"))
    h = 3.6
    A = (0.0, h)
    M = (2.4, h - 2.4 * math.tan(math.radians(42)))
    B = (M[0] - M[1] / math.tan(math.radians(31)), 0.0)
    Dp, Ep = (A[0] + 3.3, h), (B[0] + 3.3, 0.0)
    F.droite(A, 0, 1.3, 4.3)
    F.bout(pol(A, 4.3, 0), 0, "$(d)$")
    F.droite(B, 0, 1.3, 4.3)
    F.bout(pol(B, 4.3, 0), 0, "$(e)$")
    F.seg(A, M)
    F.seg(B, M)
    F.arc(A, M, Dp, 0.55, deg(42), 1, OR, val=42)
    F.arc(B, Ep, M, 0.55, deg(31), 1, OR, val=31)
    if corr:
        N = (M[0] - 1.9, M[1])
        F.seg((M[0] - 2.75, M[1]), (M[0] + 1.6, M[1]), "aide")
        F.bout((M[0] + 1.6, M[1]), 0, vert(r"$(\Delta)$"))
        F.arc(M, A, N, 0.55, vert(deg(42)), 1, VE, val=42)
        F.arc(M, N, B, 0.42, vert(deg(31)), 2, VE, lr=1.4, val=31)
        F.pt(N, "N", 90, 0.17, coul=VE)
        F.paralleles(0, 0, "(d)", "(e)")
        F.paralleles(0, 0, "(Delta)", "(d)")
    F.pt(A, "A", 120, 0.18)
    F.pt(B, "B", 240, 0.18)
    F.pt(M, "M", 45, 0.2)
    F.pt(Dp, "D", 90, 0.17)
    F.pt(Ep, "E", 270, 0.17)
    return F.code()


# ====================================================================== appels
cours_rapporteur()
cours_vocabulaire()
cours_opposes()
cours_secante()
cours_paralleles()
cours_construire()

ex2959(False)
ex2959(True)
ex2957(False)
ex2957(True)
ex2958_enonce()
ex2958_corrige([(OR, [("A", "bg", 3), ("B", "hd", 5)]), (VE, [("A", "bd", 4), ("B", "hg", 6)])],
               "ex2958_alternes", interieur=True)
ex2958_corrige([(VE, [("A", "hd", 1), ("B", "hd", 5)]), (OR, [("A", "hg", 2), ("B", "hg", 6)]),
                (NA, [("A", "bg", 3), ("B", "bg", 7)]), (RG, [("A", "bd", 4), ("B", "bd", 8)])],
               "ex2958_correspondants")
fig_rapporteur("ex2960_rapporteur", 180, 147, 33)
fig_rapporteur("ex2960_rapporteur_corrige", 180, 147, 33, corr=True)
ex2960_construction(False)
ex2960_construction(True)
ex2962(False)
ex2962(True)
ex2961(False)
ex2961(True)
ex2974(False)
ex2974(True)
ex2965(False)
ex2965(True)
ex2971(False)
ex2971(True)
ex2972(False)
ex2972(True)
