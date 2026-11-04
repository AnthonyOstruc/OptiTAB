# -*- coding: utf-8 -*-
"""Figures de la notion 289 (4e : pyramides, cônes et volumes), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion> [--planche]

Perspective cavalière (angle 40°, coefficient 0,6). Les faces visibles d'un
solide convexe sont calculées (normale extérieure tournée vers l'observateur) :
toute arête qui ne borde aucune face visible est tracée en pointillés.
Énoncés : données en orange (hauteur, cotes) ; corrigés : élément cherché en vert.
Quand un triangle rectangle « caché » sert au calcul, le corrigé le redessine
en vraie grandeur à côté du solide.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  solide/.style={otNavy,line width=.9pt,line join=round},
  cache/.style={otNavy,line width=.6pt,dash pattern=on 2.5pt off 2pt},
  face/.style={fill=otSky},
  hauteur/.style={otOrange!85!black,line width=.8pt,dash pattern=on 3pt off 2pt},
  rep/.style={otGreenDark,line width=1.25pt,line join=round},
  repc/.style={otGreenDark,line width=1pt,dash pattern=on 3pt off 2pt},
  donnee/.style={otOrange!85!black,line width=1.1pt},
  lien/.style={otMuted,line width=.4pt},
  vert/.style={otGreenDark,line width=.9pt,line join=round},
  vertc/.style={otGreenDark,line width=.7pt,dash pattern=on 2.5pt off 2pt},
}
"""

K, ALPHA = 0.6, math.radians(40)
CX, CY = K * math.cos(ALPHA), K * math.sin(ALPHA)
VUE = (CX, -1.0, CY)          # direction de l'observateur
OR = "otOrange!80!black"      # texte des données
VE = "otGreenDark"            # texte des réponses
ORT = "otOrange!85!black"     # traits orange
ANG = "otNavy,line width=.5pt"
ANGO = "otOrange!85!black,line width=.5pt"
ANGV = "otGreenDark,line width=.5pt"


def f(x):
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def Q(p):
    return f"({f(p[0])},{f(p[1])})"


def tikz(L, opts=""):
    return "\\begin{tikzpicture}[" + opts + "]\n" + "\n".join(x for x in L if x) + "\n\\end{tikzpicture}"


# ---------------------------------------------------------------- vecteurs
def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(k, a):
    return tuple(k * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def unit(a):
    n = math.sqrt(dot(a, a))
    return tuple(x / n for x in a)


def moy(pts):
    return tuple(sum(c) / len(pts) for c in zip(*pts))


def lerp(p, q, t):
    return tuple(a + t * (b - a) for a, b in zip(p, q))


# ---------------------------------------------------------------- étiquettes
ANCRES = ["west", "south west", "south", "south east", "east", "north east", "north", "north west"]


def ancre(theta):
    return ANCRES[round((theta % 360) / 45) % 8]


def nd(p, txt, theta, d=0.06, color="otInk", extra=""):
    """Texte posé dans la direction theta (degrés) du point 2D p, à la distance d."""
    t = math.radians(theta)
    x, y = p[0] + d * math.cos(t), p[1] + d * math.sin(t)
    return rf"\node[anchor={ancre(theta)},text={color},inner sep=1.6pt{extra}] at ({f(x)},{f(y)}) {{{txt}}};"


def txt(p, texte, anchor="center", color="otInk", extra=""):
    return rf"\node[anchor={anchor},text={color},inner sep=1.6pt{extra}] at {Q(p)} {{{texte}}};"


def milieu(p, q, texte, side=1, d=0.08, color="otInk", extra="", t=0.5):
    """Texte à côté du segment [pq] (2D) : à gauche (side=1) ou à droite (side=-1) du sens p→q."""
    m = lerp(p, q, t)
    ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) + (90 if side > 0 else -90)
    return nd(m, texte, ang, d, color, extra)


def pt(p, color="otNavy", r=1.5):
    return rf"\fill[{color}] {Q(p)} circle ({r}pt);"


def seg(p, q, style):
    return rf"\draw[{style}] {Q(p)} -- {Q(q)};"


def poly2(pts, style, cycle=True):
    return rf"\draw[{style}] " + " -- ".join(Q(p) for p in pts) + (" -- cycle;" if cycle else ";")


def fill2(pts, style):
    return rf"\fill[{style}] " + " -- ".join(Q(p) for p in pts) + " -- cycle;"


def lien(p, q):
    return seg(p, q, "lien")


def cote2(p, q, texte, side=1, d=0.3, color="otInk", ext=True):
    """Flèche de cote parallèle à [pq], décalée de d du côté side, texte à l'extérieur."""
    vx, vy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(vx, vy)
    nx, ny = (-vy / n, vx / n) if side > 0 else (vy / n, -vx / n)
    a = (p[0] + d * nx, p[1] + d * ny)
    b = (q[0] + d * nx, q[1] + d * ny)
    L = [rf"\draw[cote] {Q(a)} -- {Q(b)};"]
    if ext:
        L.append(rf"\draw[otMuted!70,line width=.4pt] {Q(p)} -- ({f(p[0]+(d+0.06)*nx)},{f(p[1]+(d+0.06)*ny)}) "
                 rf"{Q(q)} -- ({f(q[0]+(d+0.06)*nx)},{f(q[1]+(d+0.06)*ny)});")
    L.append(milieu(a, b, texte, side, 0.05, color))
    return L


def angle_droit2(o, u, v, e=0.16, style=ANG):
    """Angle droit en o (2D) entre les directions u et v."""
    u, v = unit(u), unit(v)
    a = (o[0] + e * u[0], o[1] + e * u[1])
    b = (a[0] + e * v[0], a[1] + e * v[1])
    c = (o[0] + e * v[0], o[1] + e * v[1])
    return rf"\draw[{style}] {Q(a)} -- {Q(b)} -- {Q(c)};"


# ---------------------------------------------------------------- projection et solides convexes
class Vue:
    def __init__(self, s=1.0, o=(0.0, 0.0)):
        self.s, self.o = s, o

    def __call__(self, x, y=None, z=None):
        if y is None:
            x, y, z = x
        return (self.o[0] + self.s * (x + CX * y), self.o[1] + self.s * (z + CY * y))


class Solide:
    """Polyèdre convexe : V = {nom: (x, y, z)}, F = [(noms des sommets d'une face)]."""

    def __init__(self, V, F, vue):
        self.V, self.F, self.vue = V, F, vue
        c = moy(list(V.values()))
        self.vis = {}
        for face in F:
            p0, p1, p2 = (V[k] for k in face[:3])
            n = cross(sub(p1, p0), sub(p2, p0))
            if dot(n, sub(moy([V[k] for k in face]), c)) < 0:
                n = mul(-1, n)
            self.vis[face] = dot(n, VUE) > 1e-9
        self.aretes = {}
        for face in F:
            for i in range(len(face)):
                e = tuple(sorted((face[i], face[(i + 1) % len(face)])))
                self.aretes[e] = self.aretes.get(e, False) or self.vis[face]

    def p(self, k):
        return self.vue(self.V[k]) if isinstance(k, str) else self.vue(k)

    def faces_visibles(self):
        return [fa for fa in self.F if self.vis[fa]]

    def dessin(self, fond="face", vis="solide", cach="cache", speciaux=None, sans=()):
        """speciaux = {("A","B"): style} remplace le style d'une arête ; sans = arêtes non tracées."""
        speciaux = {tuple(sorted(k)): v for k, v in (speciaux or {}).items()}
        sans = [tuple(sorted(k)) for k in sans]
        L = []
        if fond:
            for fa in self.faces_visibles():
                L.append(fill2([self.p(k) for k in fa], fond))
        for e, v in self.aretes.items():
            if not v and e not in speciaux and e not in sans:
                L.append(seg(self.p(e[0]), self.p(e[1]), cach))
        for e, v in self.aretes.items():
            if v and e not in speciaux and e not in sans:
                L.append(seg(self.p(e[0]), self.p(e[1]), vis))
        for e, st in speciaux.items():
            L.append(seg(self.p(e[0]), self.p(e[1]), st))
        return L

    def visible(self, a, b):
        return self.aretes[tuple(sorted((a, b)))]


def pyramide(a, b, h, vue, apex=None, noms="ABCD"):
    A, B, C, D = noms
    V = {A: (0, 0, 0), B: (a, 0, 0), C: (a, b, 0), D: (0, b, 0), "S": apex or (a / 2, b / 2, h)}
    F = [(A, B, C, D), ("S", A, B), ("S", B, C), ("S", C, D), ("S", D, A)]
    return Solide(V, F, vue)


def pave(a, b, c, vue, noms="ABCDEFGH"):
    """Dans l'ordre des noms : (0,0,0) (a,0,0) (a,b,0) (0,b,0) puis les mêmes à l'altitude c."""
    A, B, C, D, E, F_, G, H = noms
    V = {A: (0, 0, 0), B: (a, 0, 0), C: (a, b, 0), D: (0, b, 0),
         E: (0, 0, c), F_: (a, 0, c), G: (a, b, c), H: (0, b, c)}
    F = [(A, B, C, D), (E, F_, G, H), (A, B, F_, E), (B, C, G, F_), (C, D, H, G), (D, A, E, H)]
    return Solide(V, F, vue)


# ---------------------------------------------------------------- cônes et cylindres (axe vertical)
RY = 0.3  # aplatissement des ellipses


def tangentes(xc, yb, r, ys):
    """Points de tangence, sur l'ellipse de centre (xc, yb), des droites issues de (xc, ys)."""
    ry = RY * r
    yt = ry * ry / (ys - yb)
    xt = r * math.sqrt(max(0.0, 1 - (yt / ry) ** 2))
    return (xc - xt, yb + yt), (xc + xt, yb + yt)


def arc_ellipse(xc, yb, r, a0, a1, style):
    return (rf"\draw[{style}] ({f(xc + r*math.cos(math.radians(a0)))},{f(yb + RY*r*math.sin(math.radians(a0)))}) "
            rf"arc[start angle={f(a0)},end angle={f(a1)},x radius={f(r)},y radius={f(RY*r)}];")


def ang_tan(xc, yb, r, p):
    return math.degrees(math.atan2((p[1] - yb) / (RY * r), (p[0] - xc) / r))


def ellipse(c, r, style, fill=False):
    op = "fill" if fill else "draw"
    return rf"\{op}[{style}] {Q(c)} ellipse[x radius={f(r)},y radius={f(RY*r)}];"


def cone(xc, yb, r, h, fond="face", vis="solide", cach="cache", pointe_bas=False):
    """Cône d'axe vertical. Pointe en haut : base en yb, sommet en yb + h.
    Pointe en bas : sommet en yb, ouverture en yb + h (ellipse entièrement visible).
    Renvoie (lignes, S, O, gauche, droite) : gauche/droite = extrémités du diamètre horizontal."""
    L = []
    if not pointe_bas:
        S, O = (xc, yb + h), (xc, yb)
        t1, t2 = tangentes(xc, yb, r, yb + h)
        a1, a2 = ang_tan(xc, yb, r, t1), ang_tan(xc, yb, r, t2)
        if fond:
            L.append(rf"\fill[{fond}] {Q(t1)} -- {Q(S)} -- {Q(t2)} "
                     rf"arc[start angle={f(a2)},end angle={f(a1 - 360)},x radius={f(r)},y radius={f(RY*r)}] -- cycle;")
        L.append(arc_ellipse(xc, yb, r, a2, a1, cach))
        L.append(arc_ellipse(xc, yb, r, a1, a2 + 360, vis))
        L.append(rf"\draw[{vis}] {Q(t1)} -- {Q(S)} -- {Q(t2)};")
    else:
        S, O = (xc, yb), (xc, yb + h)
        t1, t2 = tangentes(xc, yb + h, r, yb)
        if fond:
            L.append(fill2([t1, S, t2], fond))
            L.append(ellipse(O, r, fond, fill=True))
        L.append(ellipse(O, r, vis))
        L.append(rf"\draw[{vis}] {Q(t1)} -- {Q(S)} -- {Q(t2)};")
    return L, S, O, (xc - r, O[1]), (xc + r, O[1])


def cylindre(xc, yb, r, h, fond="face", vis="solide", cach="cache"):
    yt = yb + h
    L = []
    if fond:
        L.append(rf"\fill[{fond}] ({f(xc-r)},{f(yb)}) -- ({f(xc-r)},{f(yt)}) -- ({f(xc+r)},{f(yt)}) -- ({f(xc+r)},{f(yb)}) "
                 rf"arc[start angle=0,end angle=-180,x radius={f(r)},y radius={f(RY*r)}] -- cycle;")
        L.append(ellipse((xc, yt), r, fond, fill=True))
    L += [arc_ellipse(xc, yb, r, 0, 180, cach), arc_ellipse(xc, yb, r, 180, 360, vis), ellipse((xc, yt), r, vis),
          rf"\draw[{vis}] ({f(xc-r)},{f(yb)}) -- ({f(xc-r)},{f(yt)}) ({f(xc+r)},{f(yb)}) -- ({f(xc+r)},{f(yt)});"]
    return L


def sous_ellipse(xc, yb, r, t=0.5, marge=0.05):
    """Point juste sous l'arc avant de l'ellipse, à l'abscisse xc + t r (pour une cote de rayon)."""
    return (xc + t * r, yb - RY * r * math.sqrt(1 - t * t) - marge)


def triangle_rect(o, a, b, s, noms, labels, cible, couleurs=None, titre=None):
    """Triangle rectangle en vraie grandeur : angle droit en o (2D), côté vertical a (vers le haut),
    côté horizontal b (vers la droite). noms = (sommet haut, angle droit, sommet droit).
    labels = (vertical, horizontal, hypoténuse) ; cible ∈ {"v", "h", "hyp"} tracé en vert."""
    P0 = o
    Ph = (o[0], o[1] + a * s)
    Pd = (o[0] + b * s, o[1])
    st = {"v": "solide", "h": "solide", "hyp": "solide"}
    st[cible] = "rep"
    col = {"v": OR, "h": OR, "hyp": OR}
    col[cible] = VE
    if couleurs:
        col.update(couleurs)
    L = [fill2([P0, Ph, Pd], "otGreen!14"),
         seg(P0, Ph, st["v"]), seg(P0, Pd, st["h"]), seg(Ph, Pd, st["hyp"]),
         angle_droit2(P0, (1, 0), (0, 1), 0.16, ANG),
         nd(Ph, f"${noms[0]}$", 90, 0.05), nd(P0, f"${noms[1]}$", 225, 0.05), nd(Pd, f"${noms[2]}$", 0, 0.06)]
    if labels[0]:
        L.append(nd(lerp(P0, Ph, 0.5), labels[0], 180, 0.08, col["v"]))
    if labels[1]:
        L.append(nd(lerp(P0, Pd, 0.5), labels[1], 270, 0.07, col["h"]))
    if labels[2]:
        L.append(milieu(Ph, Pd, labels[2], 1, 0.08, col["hyp"]))
    if titre:
        L.append(txt((o[0] + b * s / 2, o[1] - 0.5), titre, "north", "otMuted", ",font=\\small,align=center"))
    return L


FIGURES = {}
TOLERE = {}

# ======================================================================== COURS
# ---------------------------------------------------------------- 1. solides droits
def solides_droits():
    L = []
    v = Vue(0.5, (0, 0))
    pv = pave(4, 3, 3, v)
    L += pv.dessin()
    L += [fill2([pv.p(k) for k in "EFGH"], "otOrange!25"), poly2([pv.p(k) for k in "EFGH"], "solide"),
          txt(moy([pv.p(k) for k in "EFGH"]), r"$\mathcal{B}$")]
    L += cote2(pv.p("A"), pv.p("E"), "$h$", 1, 0.22, OR)
    L.append(txt(v(2, 0, 0), r"\textbf{Pavé droit}", "north", "otNavy", ",yshift=-6pt"))
    v2 = Vue(0.5, (3.55, 0))
    V = {"A": (0, 0, 0), "B": (4, 0, 0), "C": (1, 3, 0), "D": (0, 0, 3), "E": (4, 0, 3), "F": (1, 3, 3)}
    F = [("A", "B", "C"), ("D", "E", "F"), ("A", "B", "E", "D"), ("B", "C", "F", "E"), ("C", "A", "D", "F")]
    pr = Solide(V, F, v2)
    L += pr.dessin()
    L += [fill2([pr.p(k) for k in "DEF"], "otOrange!25"), poly2([pr.p(k) for k in "DEF"], "solide"),
          txt(moy([pr.p(k) for k in "DEF"]), r"$\mathcal{B}$")]
    L += cote2(pr.p("B"), pr.p("E"), "$h$", -1, 0.22, OR)
    L.append(txt(v2(2, 0, 0), r"\textbf{Prisme droit}", "north", "otNavy", ",yshift=-6pt"))
    xc, r, h = 7.2, 0.7, 1.5
    L += cylindre(xc, 0.0, r, h)
    L += [ellipse((xc, h), r, "otOrange!25", fill=True), ellipse((xc, h), r, "solide"), txt((xc, h), r"$\mathcal{B}$")]
    L += cote2((xc + r, 0), (xc + r, h), "$h$", -1, 0.22, OR)
    L.append(txt((xc, -RY * r), r"\textbf{Cylindre}", "north", "otNavy", ",yshift=-4pt"))
    return tikz(L)


FIGURES["c_solides_droits"] = solides_droits()


# ---------------------------------------------------------------- 2. vocabulaire de la pyramide
def pyramide_vocab():
    v = Vue(0.6, (0, 0))
    py = pyramide(5, 5, 5.6, v)
    O = v(2.5, 2.5, 0)
    S = py.p("S")
    L = py.dessin()
    L += [fill2([py.p(k) for k in ("S", "B", "C")], "otOrange!22"),
          seg(S, py.p("B"), "solide"), seg(S, py.p("C"), "solide"), seg(py.p("B"), py.p("C"), "solide"),
          seg(S, O, "hauteur"), angle_droit2(O, (1, 0), (0, 1), 0.16, ANGO), pt(O, ORT),
          nd(py.p("A"), "$A$", 225), nd(py.p("B"), "$B$", 300), nd(py.p("C"), "$C$", 30),
          nd(py.p("D"), "$D$", 150), nd(S, "$S$", 90), nd(O, "$O$", 300, 0.07),
          txt((S[0] + 0.3, S[1] + 0.02), "sommet", "west", "otNavy")]
    m = lerp(S, py.p("C"), 0.45)
    L += [lien(m, (m[0] + 0.55, m[1] + 0.3)), txt((m[0] + 0.55, m[1] + 0.3), r"arête\\latérale", "west", "otNavy", ",align=left")]
    c = moy([S, py.p("B"), py.p("C")])
    p = (py.p("C")[0] + 0.2, py.p("C")[1] - 0.75)
    L += [lien(c, p), txt(p, r"face\\latérale", "west", "otOrange!75!black", ",align=left")]
    m = lerp(O, S, 0.45)
    p = (-0.4, m[1] + 0.35)
    L += [lien((m[0] - 0.03, m[1]), p), txt(p, r"hauteur\\$[SO]$", "east", "otOrange!75!black", ",align=right")]
    b = v(1.5, 1.8, 0)
    p = (-0.4, b[1] - 0.25)
    L += [lien(b, p), txt(p, r"base\\$ABCD$", "east", "otNavy", ",align=right")]
    return tikz(L)


FIGURES["c_pyramide"] = pyramide_vocab()


# ---------------------------------------------------------------- 3. vocabulaire du cône
def cone_vocab():
    r, h = 1.5, 3.4
    L, S, O, g, A = cone(0, 0, r, h)
    L.insert(1, fill2([S, O, A], "otOrange!22"))
    L += [seg(S, O, "hauteur"), seg(O, A, "otGreenDark,line width=.9pt"), angle_droit2(O, (1, 0), (0, 1), 0.16, ANGO),
          pt(O, ORT), pt(A), pt(S), nd(S, "$S$", 90), nd(O, "$O$", 250, 0.08), nd(A, "$A$", 0, 0.08),
          txt((S[0] + 0.3, S[1] + 0.02), "sommet", "west", "otNavy")]
    m = lerp(O, S, 0.5)
    p = (-r - 0.3, m[1] + 0.5)
    L += [lien((m[0] - 0.03, m[1]), p), txt(p, "hauteur", "east", "otOrange!75!black")]
    m = lerp(S, A, 0.45)
    p = (m[0] + 0.6, m[1] + 0.35)
    L += [lien(m, p), txt(p, "génératrice", "west", "otNavy")]
    m = (r / 2, 0)
    p = (r / 2 + 0.25, -0.75)
    L += [lien(m, p), txt(p, r"rayon $r$", "west", VE)]
    b = sous_ellipse(0, 0, r, -0.6, -0.02)
    p = (-r - 0.3, -0.75)
    L += [lien(b, p), txt(p, r"base :\\un disque", "east", "otNavy", ",align=right")]
    L += [rf"\draw[otMuted,line width=.5pt,-{{Stealth[length=1.8mm]}}] (-0.32,{f(h+0.42)}) "
          rf"arc[start angle=200,end angle=-20,x radius=0.34,y radius=0.11];",
          rf"\draw[otMuted,line width=.45pt,dash pattern=on 1.5pt off 1.5pt] (0,{f(h+0.2)}) -- (0,{f(h+0.6)});"]
    return tikz(L)


FIGURES["c_cone"] = cone_vocab()


# ---------------------------------------------------------------- 4. patrons
def patron_pyramide(c, a, o=(0, 0)):
    """Carré de côté c centré en o, quatre triangles isocèles de côtés égaux a."""
    hc = math.sqrt(a * a - (c / 2) ** 2)
    x0, y0 = o[0] - c / 2, o[1] - c / 2
    A, B, C, D = (x0, y0), (x0 + c, y0), (x0 + c, y0 + c), (x0, y0 + c)
    E, F_, G, H = (o[0], y0 - hc), (x0 + c + hc, o[1]), (o[0], y0 + c + hc), (x0 - hc, o[1])
    L = [fill2([A, B, C, D], "otSky")] + [fill2(t, "otOrange!20") for t in ([A, B, E], [B, C, F_], [C, D, G], [D, A, H])]
    L += [poly2([A, E, B, F_, C, G, D, H], "solide"), poly2([A, B, C, D], "solide")]
    return L, dict(A=A, B=B, C=C, D=D, E=E, F=F_, G=G, H=H, hc=hc)


def patrons():
    L, P_ = patron_pyramide(1.1, 1.5, (0, 0))
    L.append(txt((0, 0), "base", "center", "otInk", ",font=\\small"))
    yc = -2.1
    L.append(txt((0, yc), r"\textbf{Patron d'une pyramide}", "north", "otNavy"))
    g, r = 1.7, 0.5
    th = 360 * r / g
    cx, cy = 4.1, 0.95
    a0, a1 = 270 - th / 2, 270 + th / 2
    p0 = (cx + g * math.cos(math.radians(a0)), cy + g * math.sin(math.radians(a0)))
    p1 = (cx + g * math.cos(math.radians(a1)), cy + g * math.sin(math.radians(a1)))
    sect = rf"({f(cx)},{f(cy)}) -- {Q(p0)} arc[start angle={f(a0)},end angle={f(a1)},radius={f(g)}] -- cycle;"
    dc = (cx, cy - g - r)
    L += [rf"\fill[otOrange!20] " + sect, rf"\draw[solide] " + sect,
          rf"\fill[otSky] {Q(dc)} circle ({f(r)});", rf"\draw[solide] {Q(dc)} circle ({f(r)});",
          pt(dc, "otNavy", 1.2), seg(dc, (dc[0] + r, dc[1]), "otGreenDark,line width=.8pt"),
          nd((dc[0] + r / 2, dc[1]), "$r$", 90, 0.03, VE),
          milieu((cx, cy), p1, "$g$", 1, 0.08, VE),
          txt((dc[0] - r - 0.1, dc[1]), "base", "east", "otInk", ",font=\\small"),
          txt((cx, yc), r"\textbf{Patron d'un cône}", "north", "otNavy"),
          txt((cx, yc - 0.45), r"$g$ : génératrice ; $r$ : rayon", "north", "otInk", ",font=\\small")]
    return tikz(L)


FIGURES["c_patrons"] = patrons()


# ---------------------------------------------------------------- 5. le tiers du prisme / du cylindre
def pyr_dans_pave(c, h, s, o=(0, 0)):
    v = Vue(s, o)
    pv = pave(c, c, h, v)
    py = pyramide(c, c, h, v)
    L = pv.dessin(fond="otSky!60")
    L += [fill2([py.p(k) for k in fa], "otGreen!28") for fa in py.faces_visibles()]
    L += py.dessin(fond=None, vis="vert", cach="vertc")
    # Le pavé est transparent : ses arêtes visibles passent DEVANT la pyramide (sauf
    # celles de la base, communes avec la pyramide et laissées en vert).
    base = {tuple(round(c, 6) for c in py.p(k)) for k in "ABCD"}
    for (a, b), visible in pv.aretes.items():
        pa, pb = (tuple(round(c, 6) for c in pv.p(x)) for x in (a, b))
        if not (pa in base and pb in base):
            L.append(seg(pv.p(a), pv.p(b), "solide" if visible else "cache"))
    return L, v


def cone_dans_cyl(xc, r, h):
    L = cylindre(xc, 0, r, h, fond="otSky!60")
    L += cone(xc, 0, r, h, fond="otGreen!28", vis="vert", cach="vertc")[0]
    return L


def tiers():
    L, v = pyr_dans_pave(2.6, 2.6, 1.0)
    L.append(txt((v(1.3, 0, 0)[0], -0.12), r"$V_{\text{pyramide}} = \dfrac{1}{3}\,V_{\text{prisme}}$", "north"))
    L += cone_dans_cyl(5.1, 1.0, 2.6)
    L.append(txt((5.1, -RY - 0.12), r"$V_{\text{cône}} = \dfrac{1}{3}\,V_{\text{cylindre}}$", "north"))
    return tikz(L)


FIGURES["c_tiers"] = tiers()


# ---------------------------------------------------------------- 6. exemple : génératrice 10, rayon 6
def cone_exemple():
    s = 0.3
    r, h = 6 * s, 8 * s
    L, S, O, g, A = cone(0, 0, r, h)
    L += [seg(S, O, "rep"), seg(O, A, "donnee"), seg(S, A, "donnee"), angle_droit2(O, (1, 0), (0, 1), 0.16, ANGV),
          pt(O), pt(A), pt(S), nd(S, "$S$", 90), nd(O, "$O$", 235, 0.08), nd(A, "$A$", 0, 0.08),
          milieu(S, A, r"$10$ cm", 1, 0.1, OR),
          txt(sous_ellipse(0, 0, r, 0.5), r"$6$ cm", "north", OR),
          nd(lerp(O, S, 0.55), r"$8$ cm", 180, 0.1, VE)]
    return tikz(L)


FIGURES["c_ex_cone"] = cone_exemple()


# ---------------------------------------------------------------- 7. un décimètre cube
def dm3():
    v = Vue(0.32, (0, 0))
    n = 10
    pv = pave(n, n, n, v)
    L = [fill2([pv.p(k) for k in fa], "otSky") for fa in pv.faces_visibles()]
    for quad in (((9, 0, 9), (10, 0, 9), (10, 0, 10), (9, 0, 10)),
                 ((9, 0, 10), (10, 0, 10), (10, 1, 10), (9, 1, 10)),
                 ((10, 0, 9), (10, 1, 9), (10, 1, 10), (10, 0, 10))):
        L.append(fill2([v(p) for p in quad], "otGreen!60"))
    gr = "otNavy!30,line width=.3pt"
    for i in range(1, n):
        L += [seg(v(i, 0, 0), v(i, 0, n), gr), seg(v(0, 0, i), v(n, 0, i), gr),
              seg(v(i, 0, n), v(i, n, n), gr), seg(v(0, i, n), v(n, i, n), gr),
              seg(v(n, i, 0), v(n, i, n), gr), seg(v(n, 0, i), v(n, n, i), gr)]
    L += pv.dessin(fond=None)
    L += cote2(v(0, 0, 0), v(n, 0, 0), r"$10$ cm", -1, 0.25)
    L += cote2(v(0, 0, 0), v(0, 0, n), r"$10$ cm", 1, 0.25)
    L += cote2(v(n, 0, 0), v(n, n, 0), r"$10$ cm", -1, 0.25)
    x = v(n, n, n)[0] + 0.35
    L.append(txt((x, v(n, n, n)[1]), r"$1$ dm³ $= 1\,000$ cm³\\$1$ dm³ $= 1$ L", "north west", "otInk", ",align=left"))
    c1 = v(10, 0.5, 9.5)
    L += [lien((c1[0] + 0.05, c1[1]), (x, c1[1])), txt((x, c1[1]), r"$1$ cm³ $= 1$ mL", "west", VE)]
    return tikz(L)


FIGURES["c_dm3"] = dm3()


# ---------------------------------------------------------------- 8. repère dans un pavé droit
def repere(Lx, Ly, Lz, s, noms, axe_y=True):
    v = Vue(s, (0, 0))
    pv = pave(Lx, Ly, Lz, v, noms=noms)
    out = [fill2([pv.p(k) for k in fa], "otSky") for fa in pv.faces_visibles()]
    for i in range(1, Lx):
        out.append(seg(v(i, 0, 0), v(i, Ly, 0), "otRule,line width=.4pt"))
    for j in range(1, Ly):
        out.append(seg(v(0, j, 0), v(Lx, j, 0), "otRule,line width=.4pt"))
    out += pv.dessin(fond=None)
    fl = r"solide,-{Stealth[length=2mm]}"
    out += [seg(v(Lx, 0, 0), v(Lx + 1.2, 0, 0), fl), seg(v(0, 0, Lz), v(0, 0, Lz + 1.1), fl),
            nd(v(Lx + 1.2, 0, 0), "$x$", 0, 0.04), nd(v(0, 0, Lz + 1.1), "$z$", 90, 0.04)]
    if axe_y:
        out += [seg(v(0, Ly, 0), v(0, Ly + 2.0, 0), fl), nd(v(0, Ly + 2.0, 0), "$y$", 90, 0.05)]
    tk = "otNavy,line width=.6pt"
    for i in range(1, Lx):
        out += [seg(v(i, 0, 0), add(v(i, 0, 0), (0, -0.07)), tk), nd(v(i, 0, 0), rf"\otRegular\footnotesize {i}", 270, 0.08, "otMuted")]
    for j in range(1, Ly):
        out += [seg(v(0, j, 0), add(v(0, j, 0), (-0.08, 0)), tk), nd(v(0, j, 0), rf"\otRegular\footnotesize {j}", 180, 0.1, "otMuted")]
    for k in range(1, Lz):
        out += [seg(v(0, 0, k), add(v(0, 0, k), (-0.08, 0)), tk), nd(v(0, 0, k), rf"\otRegular\footnotesize {k}", 180, 0.1, "otMuted")]
    return out, v, pv


def chemin(v, x, y, z):
    """Trajet O → (x;0;0) → (x;y;0) → (x;y;z) en vert."""
    fl = r"otGreenDark,line width=1pt,-{Stealth[length=1.6mm]}"
    return [seg(v(0, 0, 0), v(x, 0, 0), fl), seg(v(x, 0, 0), v(x, y, 0), fl), seg(v(x, y, 0), v(x, y, z), fl)]


def repere_cours():
    out, v, pv = repere(5, 3, 4, 0.62, noms="OIJKLMNP")
    out += chemin(v, 3, 1, 2)
    out += [pt(v(3, 1, 2), "otNavy", 2.0), nd(v(3, 1, 2), r"$M(3\,;\,1\,;\,2)$", 0, 0.1, "otNavy"),
            nd(v(0, 0, 0), "$O$", 225, 0.05),
            nd(v(5, 0, 0), r"\otRegular\footnotesize 5", 270, 0.08, "otMuted"),
            nd(v(0, 3, 0), r"\otRegular\footnotesize 3", 180, 0.1, "otMuted"),
            nd(v(0, 0, 4), r"\otRegular\footnotesize 4", 180, 0.1, "otMuted")]
    return tikz(out)


FIGURES["c_repere"] = repere_cours()


# ======================================================================== FICHE
def fiche_vocab():
    v = Vue(0.5, (0, 0))
    py = pyramide(5, 5, 5.6, v)
    O = v(2.5, 2.5, 0)
    S = py.p("S")
    L = py.dessin()
    L += [seg(S, O, "hauteur"), angle_droit2(O, (1, 0), (0, 1), 0.15, ANGO), pt(O, ORT),
          nd(S, "$S$", 90), nd(O, "$O$", 300, 0.07),
          milieu(S, py.p("A"), r"$h$ : hauteur", -1, 0.1, OR, ",font=\\small", 0.5),
          txt(v(2.5, 0, 0), r"base : un polygone", "north", "otNavy", ",font=\\small,yshift=-3pt")]
    xc, r, h = 5.9, 1.25, 2.8
    Lc, Sc, Oc, g, A = cone(xc, 0, r, h)
    L += Lc
    L += [seg(Sc, Oc, "hauteur"), seg(Oc, A, "otGreenDark,line width=.9pt"), angle_droit2(Oc, (1, 0), (0, 1), 0.15, ANGO),
          pt(Oc, ORT), pt(A), nd(Sc, "$S$", 90), nd(Oc, "$O$", 235, 0.08), nd(A, "$A$", 0, 0.07),
          nd(lerp(Oc, Sc, 0.45), "$h$", 180, 0.1, OR), nd((xc + r / 2, 0), "$r$", 90, 0.03, VE),
          milieu(Sc, A, "génératrice", 1, 0.08, "otNavy", ",font=\\small", 0.42),
          txt(sous_ellipse(xc, 0, r, 0), r"base : un disque", "north", "otNavy", ",font=\\small")]
    return tikz(L)


FIGURES["f_vocab"] = fiche_vocab()


# ======================================================================== EXERCICES
def pyr_figure(c, h, s, b=None, noms=True, hstyle="hauteur", ang=ANGO, opt=None, o=(0, 0), angO=300, angD=165):
    """Pyramide SABCD (base c × b, sommet au-dessus du centre O)."""
    b = c if b is None else b
    v = Vue(s, o)
    py = pyramide(c, b, h, v)
    O = v(c / 2, b / 2, 0)
    L = py.dessin(speciaux=(opt or {}).get("aretes"))
    L += [seg(py.p("S"), O, hstyle), angle_droit2(O, (1, 0), (0, 1), 0.15, ang),
          pt(O, VE if "otGreen" in ang else ORT if "Orange" in ang else "otNavy")]
    if noms:
        L += [nd(py.p("A"), "$A$", 225), nd(py.p("B"), "$B$", 315), nd(py.p("C"), "$C$", 15),
              nd(py.p("D"), "$D$", angD), nd(py.p("S"), "$S$", 90), nd(O, "$O$", angO, 0.07)]
    return L, py, v, O


def lab_AB(py, texte, color="otInk"):
    return milieu(py.p("A"), py.p("B"), texte, -1, 0.1, color)


def lab_gauche(py, texte, color=OR, t=0.5):
    """Texte à l'extérieur, à gauche de l'arête [SA]."""
    return milieu(py.p("S"), py.p("A"), texte, -1, 0.1, color, "", t)


# ---------------------------------------------------------------- 3692
def e3692(corrige):
    if not corrige:
        return tikz(pyr_figure(5, 5.6, 0.6, hstyle="cache", ang=ANG)[0])
    L, py, v, O = pyr_figure(5, 5.6, 0.6, hstyle="repc", ang=ANGV,
                             opt={"aretes": {("A", "D"): "repc", ("D", "C"): "repc", ("S", "D"): "repc"}})
    m = lerp(O, py.p("S"), 0.55)
    p = (py.p("C")[0] + 0.15, m[1] + 0.35)
    L += [lien((m[0] + 0.03, m[1]), p), txt(p, r"hauteur $[SO]$", "west", VE)]
    return tikz(L)


FIGURES["e3692_enonce"] = e3692(False)
FIGURES["e3692_corrige"] = e3692(True)


# ---------------------------------------------------------------- cône pointe en haut (S, O, A)
def cone_fig(r, h, xc=0.0, lab_r=None, lab_h_=None, h_dehors=False, lab_g=None, gstyle="solide",
             hstyle="hauteur", rstyle="donnee", col_h=OR, col_g=OR, col_r=OR, noms=True, fond="face"):
    L, S, O, g, A = cone(xc, 0, r, h, fond=fond)
    L += [seg(S, O, hstyle), seg(O, A, rstyle), seg(S, A, gstyle),
          angle_droit2(O, (1, 0), (0, 1), 0.15, ANG), pt(O), pt(A), pt(S)]
    if noms:
        L += [nd(S, "$S$", 90), nd(O, "$O$", 195, 0.09), nd(A, "$A$", 0, 0.08)]
    if lab_r:
        L.append(txt(sous_ellipse(xc, 0, r, 0.5), lab_r, "north", col_r))
    if lab_h_:
        if h_dehors:
            L.append(milieu(S, g, lab_h_, -1, 0.1, col_h, "", 0.5))
        else:
            L.append(nd(lerp(O, S, 0.5), lab_h_, 180, 0.1, col_h))
    if lab_g:
        L.append(milieu(S, A, lab_g, 1, 0.1, col_g))
    return L, S, O, A, g


# ---------------------------------------------------------------- 3693
s93 = 0.62
FIGURES["e3693_enonce"] = tikz(cone_fig(3 * s93, 4 * s93, lab_r=r"$3$ cm", lab_h_=r"$4$ cm")[0])
FIGURES["e3693_corrige"] = tikz(cone_fig(3 * s93, 4 * s93, lab_r=r"$3$ cm", lab_h_=r"$4$ cm",
                                         lab_g=r"$SA = 5$ cm", gstyle="rep", col_g=VE)[0])


# ---------------------------------------------------------------- 3694
def e3694_enonce():
    L, py, v, O = pyr_figure(6, 5, 0.55)
    L += [lab_AB(py, r"$6$ cm", OR), lab_gauche(py, r"$SO = 5$ cm")]
    return tikz(L)


def e3694_corrige():
    L, v = pyr_dans_pave(6, 5, 0.5)
    L.append(txt((v(3, 0, 0)[0], -0.12), r"pyramide : $60$ cm³\\pavé : $180$ cm³", "north", "otInk", ",align=center"))
    return tikz(L)


FIGURES["e3694_enonce"] = e3694_enonce()
FIGURES["e3694_corrige"] = e3694_corrige()

# ---------------------------------------------------------------- 3695
s95 = 0.36
FIGURES["e3695_enonce"] = tikz(cone_fig(3 * s95, 10 * s95, lab_r=r"$3$ cm", lab_h_=r"$h = 10$ cm", h_dehors=True)[0])


def e3695_corrige():
    r, h = 3 * s95, 10 * s95
    L = cone_dans_cyl(0, r, h)
    L += cote2((r, 0), (r, h), r"$10$ cm", -1, 0.25, OR)
    L.append(txt((0, -RY * r - 0.1), r"cône : $30\pi$ cm³\\cylindre : $90\pi$ cm³", "north", "otInk", ",align=center"))
    return tikz(L)


FIGURES["e3695_corrige"] = e3695_corrige()


# ---------------------------------------------------------------- 3696 : tétraèdre SABC, [SA] perpendiculaire à la base
def tetra(corrige):
    s = 0.55
    v = Vue(s, (0, 0))
    V = {"B": (0, 0, 0), "A": (4, 0, 0), "C": (4, 3, 0), "S": (4, 0, 6)}
    F = [("A", "B", "C"), ("S", "A", "B"), ("S", "B", "C"), ("S", "C", "A")]
    so = Solide(V, F, v)
    sp = {("S", "B"): "rep", ("B", "C"): "repc" if not so.visible("B", "C") else "rep"} if corrige else {}
    L = so.dessin(speciaux=sp)
    e = 0.45
    L += [poly2([v(4 - e, 0, 0), v(4 - e, e, 0), v(4, e, 0)], ANG, cycle=False),
          poly2([v(4 - e, 0, 0), v(4 - e, 0, e), v(4, 0, e)], ANG, cycle=False),
          nd(so.p("A"), "$A$", 300), nd(so.p("B"), "$B$", 225), nd(so.p("C"), "$C$", 0),
          nd(so.p("S"), "$S$", 90),
          txt(lerp(so.p("A"), so.p("B"), 0.5), r"$4$ cm", "north", OR, ",yshift=-2pt"),
          milieu(so.p("A"), so.p("C"), r"$3$ cm", -1, 0.08, OR),
          nd(lerp(so.p("A"), so.p("S"), 0.62), r"$6$ cm", 180, 0.1, OR)]
    if corrige:
        L.append(milieu(so.p("B"), so.p("S"), r"$SB \approx 7{,}21$ cm", 1, 0.1, VE))
    return tikz(L)


FIGURES["e3696_base"] = tikz(triangle_rect((0, 0), 3, 4, 0.75, ("C", "A", "B"), (r"$3$ cm", r"$4$ cm", r"$BC = 5$ cm"), "hyp",
                                           titre=r"base $ABC$ en vraie grandeur"))


FIGURES["e3696_enonce"] = tetra(False)
FIGURES["e3696_corrige"] = tetra(True)


# ---------------------------------------------------------------- 3697 : aquarium 50 × 30 × 40
def aquarium():
    v = Vue(0.065, (0, 0))
    pv = pave(50, 30, 40, v)
    L = [fill2([pv.p(k) for k in fa], "otSky") for fa in pv.faces_visibles()]
    L.append(fill2([v(0, 0, 0), v(50, 0, 0), v(50, 30, 0), v(50, 30, 32), v(0, 30, 32), v(0, 0, 32)], "otSky!40!otGreen!35"))
    L += pv.dessin(fond=None)
    L += [poly2([v(0, 0, 32), v(50, 0, 32), v(50, 30, 32)], "otGreenDark,line width=.5pt", cycle=False),
          poly2([v(50, 30, 32), v(0, 30, 32), v(0, 0, 32)], "otGreenDark,line width=.45pt,dash pattern=on 2pt off 1.5pt", cycle=False),
          lab_AB(pv, r"$50$ cm", OR), milieu(pv.p("B"), pv.p("C"), r"$30$ cm", -1, 0.1, OR),
          milieu(pv.p("A"), pv.p("E"), r"$40$ cm", 1, 0.1, OR)]
    return tikz(L)


FIGURES["e3697_enonce"] = aquarium()


# ---------------------------------------------------------------- 3698 : patron
def patron_3698(corrige):
    L, P_ = patron_pyramide(4 * 0.42, 5 * 0.42, (0, 0))
    A, B, C, D, E, F_, G, H = (P_[k] for k in "ABCDEFGH")
    L += [nd(A, "$A$", 225, 0.07), nd(B, "$B$", 315, 0.07), nd(C, "$C$", 45, 0.07), nd(D, "$D$", 135, 0.07),
          nd(E, "$E$", 270, 0.06), nd(F_, "$F$", 0, 0.06), nd(G, "$G$", 90, 0.06), nd(H, "$H$", 180, 0.06),
          txt(lerp(C, D, 0.5), r"$4$ cm", "north", OR, ",yshift=-2pt"),
          milieu(C, G, r"$5$ cm", -1, 0.08, OR)]
    if corrige:
        I = lerp(A, B, 0.5)
        L += [seg(I, E, "rep"), seg(A, I, "otGreenDark,line width=1.2pt"),
              angle_droit2(I, (1, 0), (0, -1), 0.15, ANGV), pt(I, VE, 1.4), nd(I, "$I$", 60, 0.06, VE),
              milieu(A, E, r"$AI = 2$ cm\\$EI \approx 4{,}58$ cm", -1, 0.1, VE, ",align=right", 0.55)]
        L += [pt(p, VE, 2.0) for p in (E, F_, G, H)]
    return tikz(L)


FIGURES["e3698_enonce"] = patron_3698(False)
FIGURES["e3698_corrige"] = patron_3698(True)


# ---------------------------------------------------------------- 3699 : Louvre (H milieu de [BC])
def louvre(corrige):
    c, h, s = 35, 21.6, 0.12
    L, py, v, O = pyr_figure(c, h, s, hstyle="repc" if corrige else "hauteur", ang=ANGV if corrige else ANGO, angD=300)
    Hh = v(c, c / 2, 0)
    S = py.p("S")
    if corrige:
        L.insert(0, "")
        L += [fill2([S, O, Hh], "otGreen!25"), seg(S, O, "repc"), seg(O, Hh, "repc"), seg(S, Hh, "rep")]
    else:
        L.append(seg(S, Hh, "solide,line width=.6pt"))
    L += [pt(Hh, VE if corrige else "otNavy", 1.5), nd(Hh, "$H$", 330, 0.07),
          lab_AB(py, r"$35$ m", OR), lab_gauche(py, r"$SO = 21{,}6$ m", OR, 0.32)]
    return tikz(L)


FIGURES["e3699_triangle"] = tikz(triangle_rect((0, 0), 21.6, 17.5, 0.13, ("S", "O", "H"),
                                               (r"$21{,}6$ m", r"$17{,}5$ m", r"$SH \approx 27{,}80$ m"), "hyp",
                                               titre=r"triangle $SOH$ en vraie grandeur"))


FIGURES["e3699_enonce"] = louvre(False)
FIGURES["e3699_corrige"] = louvre(True)


# ---------------------------------------------------------------- cône pointe en bas (S en bas, ouverture en haut)
def cone_bas(r, h, lab_r=None, lab_g=None, gstyle="solide", fond="face", xc=0.0, hstyle="hauteur",
             col_g=VE, noms=True):
    L, S, O, g, A = cone(xc, 0, r, h, fond=fond, pointe_bas=True)
    L += [seg(S, O, hstyle), seg(O, A, "donnee"), seg(S, A, gstyle),
          angle_droit2(O, (1, 0), (0, -1), 0.15, ANG), pt(O), pt(A), pt(S)]
    if noms:
        L += [nd(S, "$S$", 270, 0.06), nd(O, "$O$", 195, 0.09), nd(A, "$A$", 0, 0.07)]
    if lab_r:
        L.append(txt((xc + r / 2, O[1] + RY * r * math.sqrt(0.75) + 0.04), lab_r, "south", OR))
    if lab_g:
        L.append(milieu(S, A, lab_g, -1, 0.1, col_g))
    return L, S, O, A, g


def e3700(corrige):
    r, h = 2.5 * 0.36, 12 * 0.36
    L, S, O, A, g = cone_bas(r, h, r"$2{,}5$ cm", r"$SA \approx 12{,}26$ cm" if corrige else None,
                             "rep" if corrige else "solide", fond="otOrange!20")
    L.append(milieu(S, g, r"$SO = 12$ cm", 1, 0.1, OR))
    return tikz(L)


FIGURES["e3700_enonce"] = e3700(False)
FIGURES["e3700_corrige"] = e3700(True)


# ---------------------------------------------------------------- 3701 : tas de sable
def tas(corrige):
    s = 1.15
    r, h = 2 * s, 1.5 * s
    L, S, O, A, g = cone_fig(r, h, rstyle="otNavy,line width=.6pt" if not corrige else "otNavy,line width=.8pt",
                             gstyle="rep" if corrige else "solide",
                             lab_g=r"$SA = 2{,}5$ m" if corrige else None, col_g=VE, fond="otOrange!20")
    L.append(milieu(S, g, r"$SO = 1{,}5$ m", -1, 0.1, OR))
    yb = -RY * r - 0.3
    L += [rf"\draw[cote] ({f(-r)},{f(yb)}) -- ({f(r)},{f(yb)});",
          rf"\draw[otMuted!70,line width=.4pt] ({f(-r)},-0.06) -- ({f(-r)},{f(yb-0.06)}) ({f(r)},-0.06) -- ({f(r)},{f(yb-0.06)});",
          txt((0, yb), r"diamètre $4$ m", "north", OR, ",yshift=-1pt")]
    if corrige:
        a = math.degrees(math.atan2(S[1] - A[1], S[0] - A[0]))
        R_ = 0.55
        mid = math.radians((180 + a) / 2)
        pm = (A[0] + R_ * math.cos(mid), A[1] + R_ * math.sin(mid))
        p = (A[0] + 0.35, A[1] + 0.55)
        L += [rf"\draw[otGreenDark,line width=1pt] ({f(A[0]-R_)},{f(A[1])}) arc[start angle=180,end angle={f(a)},radius={R_}];",
              lien(pm, p), txt(p, r"$\widehat{SAO} \approx 36{,}9^\circ$", "west", VE)]
    return tikz(L)


FIGURES["e3701_enonce"] = tas(False)
FIGURES["e3701_corrige"] = tas(True)


# ---------------------------------------------------------------- 3702 : retrouver une hauteur
def e3702(corrige):
    L, py, v, O = pyr_figure(5, 9, 0.36, noms=False, hstyle="repc" if corrige else "hauteur",
                             ang=ANGV if corrige else ANGO)
    L += [lab_AB(py, r"$5$ cm", OR),
          lab_gauche(py, r"$h = 9$ cm" if corrige else r"$h = ?$", VE if corrige else OR),
          txt((v(2.5, 0, 0)[0], -0.45), r"$V = 75$ cm³", "north")]
    xc, r, h = 5.3, 4 * 0.36, 5.968 * 0.36
    Lc, S, Oc, A, g = cone_fig(r, h, xc=xc, lab_r=r"$4$ cm", noms=False, hstyle="repc" if corrige else "hauteur",
                               lab_h_=r"$h \approx 5{,}97$ cm" if corrige else r"$h = ?$", h_dehors=True,
                               col_h=VE if corrige else OR)
    L += Lc
    L.append(txt((xc, -0.8), r"$V = 100$ cm³", "north"))
    return tikz(L)


FIGURES["e3702_enonce"] = e3702(False)
FIGURES["e3702_corrige"] = e3702(True)


# ---------------------------------------------------------------- 3703 : quatre solides
def e3703(corrige):
    L = []
    s = 0.3
    bf = "otGreen!40"
    hc = VE if corrige else OR
    # (a) pavé 5 × 4 × 3
    v = Vue(s, (0, 0))
    pv = pave(5, 4, 3, v)
    L += pv.dessin()
    if corrige:
        L += [fill2([pv.p(k) for k in "EFGH"], bf), poly2([pv.p(k) for k in "EFGH"], "solide")]
    L += [lab_AB(pv, r"$5$ cm", OR), milieu(pv.p("B"), pv.p("C"), r"$4$ cm", -1, 0.08, OR),
          milieu(pv.p("A"), pv.p("E"), r"$3$ cm", 1, 0.08, hc),
          txt((v(2.5, 0, 0)[0], -0.45), r"\textbf{(a)}", "north", "otNavy")]
    # (b) prisme couché : bases triangulaires dans le plan avant, longueur 8 en profondeur
    v = Vue(s, (3.6, 0))
    V = {"A": (0, 0, 0), "B": (3, 0, 0), "C": (0, 0, 4), "D": (0, 8, 0), "E": (3, 8, 0), "F": (0, 8, 4)}
    F = [("A", "B", "C"), ("D", "E", "F"), ("A", "B", "E", "D"), ("B", "C", "F", "E"), ("A", "C", "F", "D")]
    pr = Solide(V, F, v)
    L += pr.dessin()
    if corrige:
        L += [fill2([pr.p(k) for k in "ABC"], bf), poly2([pr.p(k) for k in "ABC"], "solide"),
              poly2([pr.p(k) for k in "DEF"], "vertc")]
    L += [poly2([v(0.45, 0, 0), v(0.45, 0, 0.45), v(0, 0, 0.45)], ANG, cycle=False),
          txt(lerp(pr.p("A"), pr.p("B"), 0.5), r"$3$ cm", "north", OR, ",yshift=-2pt"),
          milieu(pr.p("A"), pr.p("C"), r"$4$ cm", 1, 0.08, OR),
          milieu(pr.p("B"), pr.p("E"), r"$8$ cm", -1, 0.08, hc),
          txt((v(1.5, 0, 0)[0], -0.45), r"\textbf{(b)}", "north", "otNavy")]
    # (c) cylindre r = 2, h = 5
    xc, r, h = 1.0, 2 * s, 5 * s
    yb = -3.0
    L += cylindre(xc, yb, r, h)
    if corrige:
        L += [ellipse((xc, yb + h), r, bf, fill=True), ellipse((xc, yb + h), r, "solide")]
    L += [seg((xc, yb + h), (xc + r, yb + h), "otNavy,line width=.6pt"), pt((xc, yb + h), "otNavy", 1.2),
          txt((xc + r / 2, yb + h + RY * r * 0.87 + 0.03), r"$2$ cm", "south", OR)]
    L += cote2((xc + r, yb), (xc + r, yb + h), r"$5$ cm", -1, 0.22, hc)
    L.append(txt((xc, yb - RY * r - 0.12), r"\textbf{(c)}", "north", "otNavy"))
    # (d) pyramide 6 × 6, hauteur 4
    v = Vue(s, (3.6, -3.0))
    py = pyramide(6, 6, 4, v)
    O = v(3, 3, 0)
    L += py.dessin()
    L += [seg(py.p("S"), O, "repc" if corrige else "hauteur"), pt(O, VE if corrige else ORT, 1.3),
          angle_droit2(O, (1, 0), (0, 1), 0.13, ANGV if corrige else ANGO),
          lab_AB(py, r"$6$ cm", OR), lab_gauche(py, r"$4$ cm", hc),
          txt((v(3, 0, 0)[0], -3.45), r"\textbf{(d)}", "north", "otNavy")]
    return tikz(L)


FIGURES["e3703_enonce"] = e3703(False)
FIGURES["e3703_corrige"] = e3703(True)


# ---------------------------------------------------------------- 3704 : pyramide 8 × 6, SO = 12, arêtes 13 ; cône r = 3, h = 4
def e3704(corrige):
    s = 0.24
    L, py, v, O = pyr_figure(8, 12, s, b=6, angO=200, hstyle="repc" if corrige else "hauteur", ang=ANGV if corrige else ANGO,
                             opt={"aretes": {("S", "C"): "donnee" if corrige else "solide"}})
    L += [lab_AB(py, r"$8$ cm"), milieu(py.p("B"), py.p("C"), r"$6$ cm", -1, 0.08),
          milieu(py.p("S"), py.p("C"), r"$13$ cm", 1, 0.1, OR, "", 0.45),
          lab_gauche(py, r"$SO = 12$ cm", VE if corrige else OR, 0.45)]
    xc, r, h = 5.0, 3 * 0.42, 4 * 0.42
    Lc, S, Oc, A, g = cone_fig(r, h, xc=xc, noms=False, rstyle="rep" if corrige else "donnee",
                               lab_h_=r"$4$ cm", h_dehors=True)
    L += Lc
    if corrige:
        L += [seg((xc - r, 0), (xc, 0), "otOrange!85!black,line width=.8pt,dash pattern=on 2pt off 1.5pt"),
              txt(sous_ellipse(xc, 0, r, 0.5), r"rayon $3$ cm", "north", VE)]
    else:
        L.append(txt(sous_ellipse(xc, 0, r, 0.5), r"$3$ cm", "north", OR))
    return tikz(L)


FIGURES["e3704_enonce"] = e3704(False)
FIGURES["e3704_corrige"] = e3704(True)


# ---------------------------------------------------------------- 3705 : repère dans le pavé OABCDEFG (6 × 4 × 3)
def e3705(corrige):
    out, v, pv = repere(6, 4, 3, 0.62, noms="OABCDEFG", axe_y=False)
    ang = {"O": 225, "A": 300, "B": 330, "C": 300, "D": 135, "E": 300, "F": 30, "G": 135}
    out += [nd(pv.p(k), f"${k}$", a, 0.06) for k, a in ang.items()]
    if corrige:
        Sx = v(3, 2, 3)
        py = pyramide(6, 4, 3, v, apex=(3, 2, 3), noms="OABC")
        out += py.dessin(fond=None, vis="vert", cach="vertc", sans=[("O", "A"), ("A", "B"), ("B", "C"), ("C", "O")])
        out += [seg(Sx, v(3, 2, 0), "vertc"), pt(v(3, 2, 0), VE, 1.3), pt(Sx, VE, 2.0),
                txt((Sx[0] - 0.1, v(0, 4, 3)[1] + 0.55), r"$S(3\,;\,2\,;\,3)$", "south", VE),
                lien((Sx[0], Sx[1] + 0.06), (Sx[0] - 0.1, v(0, 4, 3)[1] + 0.55))]
    return tikz(out)


FIGURES["e3705_enonce"] = e3705(False)
FIGURES["e3705_corrige"] = e3705(True)


# ---------------------------------------------------------------- 3706 : sablier
def sablier(corrige):
    r, h = 3 * 0.42, 4 * 0.42
    Lb, Sb, Ob, gb, Ab = cone(0, 0, r, h)
    Lh, Sh, Oh, gh, Ah = cone(0, h, r, h, pointe_bas=True)
    k = 0.8 ** (1 / 3)              # 80 % du volume depuis la pointe
    hs, rs = k * h, k * r
    t1, t2 = tangentes(0, h + hs, rs, h)
    L = Lb + Lh
    L += [fill2([t1, (0, h), t2], "otOrange!45"), ellipse((0, h + hs), rs, "otOrange!45", fill=True),
          ellipse((0, h + hs), rs, "otOrange!85!black,line width=.5pt"),
          ellipse((0, 2 * h), r, "solide"),
          poly2([tangentes(0, 2 * h, r, h)[0], (0, h), tangentes(0, 2 * h, r, h)[1]], "solide", cycle=False)]
    Ot, At = (0, 2 * h), (r, 2 * h)
    L += [seg(Ot, At, "donnee"), pt(Ot, "otNavy", 1.3), seg((0, h), Ot, "hauteur"),
          txt((r / 2, 2 * h + RY * r * 0.87 + 0.04), r"$3$ cm", "south", OR)]
    L += cote2((r + 0.12, h), (r + 0.12, 2 * h), r"$4$ cm", -1, 0.3, OR, ext=False)
    L += [rf"\draw[otMuted!70,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] (0.1,{f(h)}) -- ({f(r+0.48)},{f(h)});",
          rf"\draw[otMuted!70,line width=.4pt] ({f(r)},{f(2*h)}) -- ({f(r+0.48)},{f(2*h)});",
          txt((-r - 0.35, h + hs * 0.55), "sable", "east", "otOrange!75!black"),
          lien((-r - 0.35, h + hs * 0.55), (-rs * 0.3, h + hs * 0.55))]
    if corrige:
        L += [seg((0, h), At, "rep"), milieu((0, h), At, r"$5$ cm", -1, 0.08, VE, "", 0.3)]
    return tikz(L)


FIGURES["e3706_enonce"] = sablier(False)
FIGURES["e3706_corrige"] = sablier(True)


# ---------------------------------------------------------------- 3707 : maison (pavé + toit en pyramide)
def maison(corrige):
    s = 0.36
    v = Vue(s, (0, 0))
    a, b, c, h = 10, 8, 2.5, 3
    V = {"A": (0, 0, 0), "B": (a, 0, 0), "C": (a, b, 0), "D": (0, b, 0),
         "E": (0, 0, c), "F": (a, 0, c), "G": (a, b, c), "H": (0, b, c), "S": (a / 2, b / 2, c + h)}
    F = [("A", "B", "C", "D"), ("A", "B", "F", "E"), ("B", "C", "G", "F"), ("C", "D", "H", "G"), ("D", "A", "E", "H"),
         ("S", "E", "F"), ("S", "F", "G"), ("S", "G", "H"), ("S", "H", "E")]
    so = Solide(V, F, v)
    L = [fill2([so.p(k) for k in fa], ("otGreen!30" if corrige else "otOrange!25") if "S" in fa else "otSky")
         for fa in so.faces_visibles()]
    L += so.dessin(fond=None)
    Ot = v(a / 2, b / 2, c)
    S = so.p("S")
    m = lerp(Ot, S, 0.5)
    p = (so.p("E")[0] - 0.2, m[1] + 0.25)
    L += [seg(S, Ot, "repc" if corrige else "hauteur"), pt(Ot, VE if corrige else ORT, 1.3),
          lien((m[0] - 0.03, m[1]), p), txt(p, r"$3$ m", "east", OR),
          lab_AB(so, r"$10$ m", OR), milieu(so.p("B"), so.p("C"), r"$8$ m", -1, 0.08, OR),
          milieu(so.p("A"), so.p("E"), r"$2{,}5$ m", 1, 0.08, OR)]
    if corrige:
        q = lerp(so.p("G"), S, 0.35)
        p2 = (so.p("G")[0] + 0.3, q[1] + 0.45)
        L += [txt(v(a / 2, 0, c / 2), r"$200$ m³", "center", "otNavy"),
              lien(q, p2), txt(p2, r"toit : $80$ m³", "west", VE)]
    return tikz(L)


FIGURES["e3707_enonce"] = maison(False)
FIGURES["e3707_corrige"] = maison(True)


# ---------------------------------------------------------------- 3708 : verre à cocktail
def verre(corrige):
    s = 0.42
    r, h = 4 * s, 9 * s
    hl, rl = h / 2, r / 2
    t1, t2 = tangentes(0, hl, rl, 0)
    L = [fill2([t1, (0, 0), t2], "otSky!50!otNavy!20"), ellipse((0, hl), rl, "otSky!50!otNavy!20", fill=True)]
    L += cone(0, 0, r, h, fond=None, pointe_bas=True)[0]
    S, O, A = (0, 0), (0, h), (r, h)
    O2, A2 = (0, hl), (rl, hl)
    L += [ellipse(O2, rl, "otNavy!70,line width=.5pt"),
          rf"\draw[otMuted,line width=1.1pt] (0,-0.03) -- (0,-1.0) (-0.75,-1.0) -- (0.75,-1.0);",
          seg(S, O, "hauteur"), seg(O, A, "donnee"), seg(O2, A2, "rep" if corrige else "otNavy,line width=.8pt"),
          seg(S, A, "solide"), pt(O), pt(A), pt(S), pt(O2), pt(A2),
          angle_droit2(O, (1, 0), (0, -1), 0.15, ANG),
          nd(S, "$S$", 200, 0.08), nd(O, "$O$", 150, 0.07), nd(A, "$A$", 45, 0.06),
          nd(O2, "$O'$", 165, 0.08), nd(A2, "$A'$", 0, 0.08),
          txt((r / 2, h + RY * r * 0.87 + 0.04), r"$4$ cm", "south", OR)]
    L += cote2((r + 0.05, 0), (r + 0.05, h), r"$9$ cm", -1, 0.25, OR, ext=False)
    L += [rf"\draw[otMuted!70,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] (0.08,0) -- ({f(r+0.36)},0);",
          rf"\draw[otMuted!70,line width=.4pt] ({f(r)},{f(h)}) -- ({f(r+0.36)},{f(h)});"]
    L += cote2((-rl - 0.1, hl), (-rl - 0.1, 0), r"$4{,}5$ cm", -1, 0.2, OR, ext=False)
    L += [rf"\draw[otMuted!70,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] (-0.08,0) -- ({f(-rl-0.36)},0);",
          rf"\draw[otMuted!70,line width=.4pt] ({f(-rl-0.08)},{f(hl)}) -- ({f(-rl-0.36)},{f(hl)});"]
    if corrige:
        p = (r * 0.62, hl - 0.5)
        L += [lien((rl * 0.6, hl), p), txt(p, r"$O'A' = 2$ cm", "west", VE)]
    return tikz(L)


FIGURES["e3708_enonce"] = verre(False)
FIGURES["e3708_corrige"] = verre(True)


# ---------------------------------------------------------------- 3709 : grande pyramide (demi-diagonale OA, arête SA)
def kheops(corrige):
    c, h, s = 230, 146, 0.019
    L, py, v, O = pyr_figure(c, h, s, hstyle="repc" if corrige else "hauteur", ang=ANGO, angD=300,
                             opt={"aretes": {("S", "A"): "rep"}} if corrige else None)
    A, C, S = py.p("A"), py.p("C"), py.p("S")
    if corrige:
        L.insert(0, fill2([S, O, A], "otGreen!25"))
        L += [seg(A, C, "vertc"), seg(A, O, "repc"), seg(S, O, "repc")]
    L += [lab_AB(py, r"$230$ m", OR), milieu(py.p("S"), py.p("C"), r"$SO = 146$ m", 1, 0.1, OR, "", 0.4)]
    if corrige:
        L.append(milieu(A, O, r"$OA$", 1, 0.06, VE, "", 0.4))
    return tikz(L)


FIGURES["e3709_enonce"] = kheops(False)
FIGURES["e3709_corrige"] = kheops(True)
FIGURES["e3709_triangle"] = tikz(triangle_rect((0, 0), 146, 162.63, 0.0165, ("S", "O", "A"),
                                               (r"$146$ m", r"$OA \approx 162{,}63$ m", r"$SA \approx 218{,}6$ m"), "hyp",
                                               couleurs={"h": VE}, titre=r"triangle $SOA$ en vraie grandeur"))


# ---------------------------------------------------------------- 3710 : silo
def silo(corrige):
    s = 0.48
    r, hc, hk = 2 * s, 6 * s, 1.5 * s
    col_cone = "otGreen!30" if corrige else "otOrange!20"
    t1, t2 = tangentes(0, hk, r, 0)
    L = [rf"\fill[otSky] ({f(-r)},{f(hk)}) -- ({f(-r)},{f(hk+hc)}) -- ({f(r)},{f(hk+hc)}) -- ({f(r)},{f(hk)}) "
         rf"arc[start angle=0,end angle=-180,x radius={f(r)},y radius={f(RY*r)}] -- cycle;",
         rf"\fill[{col_cone}] {Q(t1)} -- (0,0) -- {Q(t2)} arc[start angle={f(ang_tan(0,hk,r,t2))},"
         rf"end angle={f(ang_tan(0,hk,r,t1)-360)},x radius={f(r)},y radius={f(RY*r)}] -- cycle;",
         ellipse((0, hk + hc), r, "otSky", fill=True), ellipse((0, hk + hc), r, "solide"),
         arc_ellipse(0, hk, r, 0, 180, "cache"), arc_ellipse(0, hk, r, 180, 360, "solide,line width=.7pt"),
         rf"\draw[solide] ({f(-r)},{f(hk+hc)}) -- ({f(-r)},{f(hk)}) -- {Q(t1)} -- (0,0) -- {Q(t2)} -- ({f(r)},{f(hk)}) -- ({f(r)},{f(hk+hc)});",
         seg((0, hk + hc), (r, hk + hc), "donnee"), pt((0, hk + hc), "otNavy", 1.3),
         txt((r / 2, hk + hc + RY * r * 0.87 + 0.04), r"$2$ m", "south", OR),
         seg((0, 0), (0, hk), "hauteur"), pt((0, hk), "otNavy", 1.2)]
    L += cote2((r, hk), (r, hk + hc), r"$6$ m", -1, 0.3, OR)
    L += cote2((r, 0), (r, hk), r"$1{,}5$ m", -1, 0.3, OR, ext=False)
    L.append(rf"\draw[otMuted!70,line width=.4pt] (0.06,0) -- ({f(r+0.36)},0);")
    if corrige:
        p = (-r - 0.35, hk * 0.42)
        L += [txt((0, hk + hc * 0.5), r"cylindre\\$24\pi$ m³", "center", "otNavy", ",align=center"),
              lien((-r * 0.25, hk * 0.42), p), txt(p, r"cône\\$2\pi$ m³", "east", VE, ",align=right")]
    return tikz(L)


FIGURES["e3710_enonce"] = silo(False)
FIGURES["e3710_corrige"] = silo(True)


# ---------------------------------------------------------------- 3711 : bougies
def bougies():
    s = 0.3
    L, py, v, O = pyr_figure(6, 9, s, noms=False)
    S = py.p("S")
    L += [seg(S, (S[0], S[1] + 0.3), "otInk,line width=1.2pt"), lab_AB(py, r"$6$ cm", OR),
          lab_gauche(py, r"$9$ cm", OR, 0.5),
          txt((v(3, 0, 0)[0], -0.75), r"bougie « pyramide »", "north", "otNavy", ",font=\\small")]
    xc, r, h = 4.7, 3 * s, 9 * s
    Lc, Sc, Oc, A, g = cone_fig(r, h, xc=xc, noms=False, lab_r=r"$3$ cm", lab_h_=r"$9$ cm", h_dehors=True)
    L += Lc
    L += [seg(Sc, (Sc[0], Sc[1] + 0.3), "otInk,line width=1.2pt"),
          txt((xc, -0.75), r"bougie « cône »", "north", "otNavy", ",font=\\small")]
    return tikz(L)


FIGURES["e3711_enonce"] = bougies()


def vue_dessus():
    a = 2.4
    L = [rf"\fill[otOrange!20] (0,0) rectangle ({a},{a});", rf"\draw[solide] (0,0) rectangle ({a},{a});",
         rf"\fill[otGreen!30] ({a/2},{a/2}) circle ({a/2});", rf"\draw[vert] ({a/2},{a/2}) circle ({a/2});",
         pt((a / 2, a / 2), "otNavy", 1.3), seg((a / 2, a / 2), (a, a / 2), "otGreenDark,line width=.8pt"),
         txt((a * 0.75, a / 2), r"$3$ cm", "south", VE),
         txt((a / 2, 0), r"$6$ cm", "north", OR, ",yshift=-1pt"),
         txt((a + 0.3, a * 0.72), r"vue de dessus :", "west", "otInk", ",font=\\small"),
         txt((a + 0.3, a * 0.47), r"base de la pyramide", "west", "otOrange!75!black", ",font=\\small"),
         txt((a + 0.3, a * 0.22), r"base du cône", "west", VE, ",font=\\small")]
    return tikz(L)


FIGURES["e3711_corrige"] = vue_dessus()


# ---------------------------------------------------------------- 3712 : gobelet
def gobelet(corrige):
    s = 0.42
    r = 3.5 * s
    h = math.sqrt(9 ** 2 - 3.5 ** 2) * s
    L, S, O, A, g = cone_bas(r, h, r"$3{,}5$ cm", None, "solide", fond="otSky", hstyle="repc" if corrige else "cache")
    L.append(milieu(S, A, r"$9$ cm", -1, 0.1, OR))
    if corrige:
        a = math.degrees(math.atan2(A[1] - S[1], A[0] - S[0]))
        R_ = 0.75
        mid = math.radians((90 + a) / 2)
        pm = (R_ * math.cos(mid), R_ * math.sin(mid))
        p = (r * 0.75, 0.55)
        L += [rf"\draw[otGreenDark,line width=1pt] (0,{f(R_)}) arc[start angle=90,end angle={f(a)},radius={R_}];",
              milieu(S, g, r"$SO \approx 8{,}29$ cm", 1, 0.1, VE, "", 0.55),
              lien(pm, p), txt(p, r"$\widehat{OSA} \approx 22{,}9^\circ$", "west", VE)]
    return tikz(L)


FIGURES["e3712_enonce"] = gobelet(False)
FIGURES["e3712_corrige"] = gobelet(True)
