# -*- coding: utf-8 -*-
"""Figures de la notion 277 (5e : solides, disques et volumes), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion> [--planche]

Perspective cavalière (angle 40°, coefficient 0,6), reprise de la notion 4e 289.
Les faces visibles d'un solide convexe sont calculées (normale extérieure tournée
vers l'observateur) : toute arête qui ne borde aucune face visible est tracée en
pointillés. Empilements de cubes dessinés du fond vers l'avant (peintre).
Un solide transparent (aquarium) a ses arêtes visibles tracées DEVANT ce qu'il contient.
Énoncés : données en orange. Corrigés : base et hauteur en vert.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  solide/.style={otNavy,line width=.9pt,line join=round},
  cache/.style={otNavy,line width=.6pt,dash pattern=on 2.5pt off 2pt},
  fin/.style={otNavy!60,line width=.45pt},
  face/.style={fill=otSky},
  rep/.style={otGreenDark,line width=1.5pt,line join=round,line cap=round},
  repc/.style={otGreenDark,line width=1.1pt,dash pattern=on 3pt off 2pt},
  vert/.style={otGreenDark,line width=.95pt,line join=round},
  vertc/.style={otGreenDark,line width=.7pt,dash pattern=on 2.5pt off 2pt},
  donnee/.style={otOrange!85!black,line width=1.1pt},
  hauteurT/.style={otOrange!85!black,line width=.8pt,dash pattern=on 3pt off 2pt},
  lien/.style={otMuted,line width=.4pt},
  cube/.style={draw=otNavy!80,line width=.45pt,line join=round},
}
"""

K, ALPHA = 0.6, math.radians(40)
CX, CY = K * math.cos(ALPHA), K * math.sin(ALPHA)
VUE = (CX, -1.0, CY)          # direction de l'observateur (devant, à droite, au-dessus)
OR = "otOrange!80!black"      # texte des données
VE = "otGreenDark"            # texte des réponses
NV = "otNavy"
ANG = "otNavy,line width=.5pt"
ANGO = "otOrange!85!black,line width=.5pt"
ANGV = "otGreenDark,line width=.5pt"
BASE_E = "otOrange!22"        # base colorée (cours)
BASE_V = "otGreen!30"         # base colorée (corrigé)

FIGURES = {}
TOLERE = {}   # aucune tolérance : aucun texte n'est posé sur un trait


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


def nd(p, texte, theta, d=0.06, color="otInk", extra=""):
    """Texte posé dans la direction theta (degrés) du point 2D p, à la distance d."""
    t = math.radians(theta)
    x, y = p[0] + d * math.cos(t), p[1] + d * math.sin(t)
    return rf"\node[anchor={ancre(theta)},text={color},inner sep=1.6pt{extra}] at ({f(x)},{f(y)}) {{{texte}}};"


def txt(p, texte, anchor="center", color="otInk", extra=""):
    return rf"\node[anchor={anchor},text={color},inner sep=1.6pt{extra}] at {Q(p)} {{{texte}}};"


def titre(p, texte, anchor="north", color=NV):
    return txt(p, texte, anchor, color, r",align=center,font=\bfseries")


def milieu(p, q, texte, side=1, d=0.08, color="otInk", extra="", t=0.5):
    """Texte à côté du segment [pq] (2D) : à gauche (side=1) ou à droite (side=-1) du sens p→q."""
    m = lerp(p, q, t)
    ang = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) + (90 if side > 0 else -90)
    return nd(m, texte, ang, d, color, extra)


def pt(p, color=NV, r=1.4):
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


def codage(p, q, n=1, color=NV):
    """n petits traits perpendiculaires au milieu de [pq] (longueurs égales)."""
    m = lerp(p, q, 0.5)
    u = unit(sub(q, p))
    nrm = (-u[1], u[0])
    L = []
    for k in range(n):
        dk = (k - (n - 1) / 2) * 0.07
        c = add(m, mul(dk, u))
        L.append(seg(add(c, mul(0.09, nrm)), add(c, mul(-0.09, nrm)), f"{color},line width=.7pt"))
    return L


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

    def cachees(self):
        return sorted(e for e, v in self.aretes.items() if not v)

    def dessin(self, fond="face", vis="solide", cach="cache", speciaux=None, sans=(), remplis=None):
        """speciaux = {("A","B"): style} remplace le style d'une arête ; sans = arêtes non tracées ;
        remplis = {face: couleur} colore une face VISIBLE (une face cachée n'est jamais remplie)."""
        speciaux = {tuple(sorted(k)): v for k, v in (speciaux or {}).items()}
        sans = [tuple(sorted(k)) for k in sans]
        remplis = remplis or {}
        L = []
        if fond:
            for fa in self.faces_visibles():
                L.append(fill2([self.p(k) for k in fa], remplis.get(fa, fond)))
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


def pave(a, b, c, vue, noms="ABCDEFGH"):
    """(0,0,0) (a,0,0) (a,b,0) (0,b,0) puis les mêmes à l'altitude c."""
    A, B, C, D, E, F_, G, H = noms
    V = {A: (0, 0, 0), B: (a, 0, 0), C: (a, b, 0), D: (0, b, 0),
         E: (0, 0, c), F_: (a, 0, c), G: (a, b, c), H: (0, b, c)}
    F = [(A, B, C, D), (E, F_, G, H), (A, B, F_, E), (B, C, G, F_), (C, D, H, G), (D, A, E, H)]
    return Solide(V, F, vue)


def prisme_vertical(base, h, vue, bas=None, haut=None):
    """Prisme droit debout : base = [(x, y)] dans le plan z = 0, hauteur h (axe z)."""
    n = len(base)
    bas = bas or [f"a{i}" for i in range(n)]
    haut = haut or [f"b{i}" for i in range(n)]
    V = {bas[i]: (base[i][0], base[i][1], 0) for i in range(n)}
    V.update({haut[i]: (base[i][0], base[i][1], h) for i in range(n)})
    F = [tuple(bas), tuple(haut)] + [(bas[i], bas[(i + 1) % n], haut[(i + 1) % n], haut[i]) for i in range(n)]
    return Solide(V, F, vue)


def prisme_couche(base, L, vue, av=None, ar=None):
    """Prisme droit couché : base = [(x, z)] dans le plan de face y = 0, longueur L vers l'arrière."""
    n = len(base)
    av = av or [f"a{i}" for i in range(n)]
    ar = ar or [f"b{i}" for i in range(n)]
    V = {av[i]: (base[i][0], 0, base[i][1]) for i in range(n)}
    V.update({ar[i]: (base[i][0], L, base[i][1]) for i in range(n)})
    F = [tuple(av), tuple(ar)] + [(av[i], av[(i + 1) % n], ar[(i + 1) % n], ar[i]) for i in range(n)]
    return Solide(V, F, vue)


# ---------------------------------------------------------------- cylindres (axe vertical)
RY = 0.3  # aplatissement des ellipses


def arc_ellipse(xc, yb, r, a0, a1, style):
    return (rf"\draw[{style}] ({f(xc + r*math.cos(math.radians(a0)))},{f(yb + RY*r*math.sin(math.radians(a0)))}) "
            rf"arc[start angle={f(a0)},end angle={f(a1)},x radius={f(r)},y radius={f(RY*r)}];")


def ellipse(c, r, style, fill=False):
    op = "fill" if fill else "draw"
    return rf"\{op}[{style}] {Q(c)} ellipse[x radius={f(r)},y radius={f(RY*r)}];"


def cylindre(xc, yb, r, h, fond="face", vis="solide", cach="cache", dessus=None, dessus_trait=None):
    """Cylindre d'axe vertical, base inférieure centrée en (xc, yb). dessus = couleur du disque du haut."""
    yt = yb + h
    L = []
    if fond:
        L.append(rf"\fill[{fond}] ({f(xc-r)},{f(yb)}) -- ({f(xc-r)},{f(yt)}) -- ({f(xc+r)},{f(yt)}) -- ({f(xc+r)},{f(yb)}) "
                 rf"arc[start angle=0,end angle=-180,x radius={f(r)},y radius={f(RY*r)}] -- cycle;")
        L.append(ellipse((xc, yt), r, fond, fill=True))
    if dessus:
        L.append(ellipse((xc, yt), r, dessus, fill=True))
    L += [arc_ellipse(xc, yb, r, 0, 180, cach), arc_ellipse(xc, yb, r, 180, 360, vis),
          ellipse((xc, yt), r, dessus_trait or vis),
          rf"\draw[{vis}] ({f(xc-r)},{f(yb)}) -- ({f(xc-r)},{f(yt)}) ({f(xc+r)},{f(yb)}) -- ({f(xc+r)},{f(yt)});"]
    return L


def haut_ellipse(xc, yt, r, t=0.5, marge=0.03):
    """Point juste au-dessus de l'arc arrière de l'ellipse du haut, à l'abscisse xc + t r."""
    return (xc + t * r, yt + RY * r * math.sqrt(1 - t * t) + marge)


def sous_ellipse(xc, yb, r, t=0.5, marge=0.05):
    """Point juste sous l'arc avant de l'ellipse du bas, à l'abscisse xc + t r."""
    return (xc + t * r, yb - RY * r * math.sqrt(1 - t * t) - marge)


def cyl_donnees(xc, yb, r, h, lab_r=None, lab_d=None, lab_h=None, corrige=False, h_gauche=True,
                lab_b=None, fond="face"):
    """Cylindre avec ses données (orange). Corrigé : disque du haut (base) et hauteur en vert."""
    yt = yb + h
    L = cylindre(xc, yb, r, h, fond=fond, dessus=BASE_V if corrige else None,
                 dessus_trait="vert" if corrige else None)
    if lab_r:
        L += [seg((xc, yt), (xc + r, yt), "donnee"), pt((xc, yt), OR, 1.2),
              txt(haut_ellipse(xc, yt, r, 0.5), lab_r, "south", OR)]
    if lab_d:
        L += [seg((xc - r, yt), (xc + r, yt), "donnee"), pt((xc, yt), OR, 1.2),
              txt(haut_ellipse(xc, yt, r, 0.0), lab_d, "south", OR)]
    xg = xc - r if h_gauche else xc + r
    if corrige:
        L.append(seg((xg, yb), (xg, yt), "rep"))
        if lab_h:
            L.append(nd((xg, yb + h / 2), lab_h, 180 if h_gauche else 0, 0.1, VE))
    elif lab_h:
        L += cote2((xg, yb), (xg, yt), lab_h, 1 if h_gauche else -1, 0.22, OR)
    if lab_b:
        L.append(txt(sous_ellipse(xc, yb, r, 0.0, 0.08), lab_b, "north", VE))
    return L


# ---------------------------------------------------------------- empilements de cubes
COUL_CUBE = {  # (avant, dessus, droite)
    "bleu": ("otNavy!13", "otNavy!5", "otNavy!24"),
    "vert": ("otGreen!38", "otGreen!20", "otGreen!55"),
}


def empilement(vue, H, couleur=None):
    """H = {(i, j): hauteur} (i : colonne vers la droite, j : rangée vers l'arrière).
    couleur(i, j, k) -> "bleu" | "vert". Dessin du fond vers l'avant, du bas vers le haut, de gauche à droite."""
    L = []
    cells = sorted(H, key=lambda c: (-c[1], c[0]))
    hmax = max(H.values()) if H else 0
    for j in sorted({c[1] for c in H}, reverse=True):
        for k in range(hmax):
            for i in sorted({c[0] for c in H}):
                if (i, j) not in H or k >= H[(i, j)]:
                    continue
                c = (couleur(i, j, k) if couleur else None) or "bleu"
                av, de, dr = COUL_CUBE[c]
                P = lambda x, y, z: vue(i + x, j + y, k + z)
                L.append(rf"\filldraw[cube,fill={av}] " + " -- ".join(Q(P(*p)) for p in ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1))) + " -- cycle;")
                L.append(rf"\filldraw[cube,fill={de}] " + " -- ".join(Q(P(*p)) for p in ((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1))) + " -- cycle;")
                L.append(rf"\filldraw[cube,fill={dr}] " + " -- ".join(Q(P(*p)) for p in ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1))) + " -- cycle;")
    return L


def vue_colonnes(x0, y0, hauteurs, u, couleur="otNavy!13", trait="otNavy!80"):
    """Vue de face / de côté : colonnes de carrés posées sur la ligne y0."""
    L = []
    for i, n in enumerate(hauteurs):
        for k in range(n):
            L.append(rf"\filldraw[fill={couleur},draw={trait},line width=.5pt] ({f(x0+i*u)},{f(y0+k*u)}) rectangle ({f(x0+(i+1)*u)},{f(y0+(k+1)*u)});")
    return L


def plan_cote(x0, y0, grille, u, color="otInk", fond="otNavy!5"):
    """Vue de dessus codée : grille[r][c] (r = 0 : rangée du fond, en haut du dessin)."""
    L = []
    nr = len(grille)
    for r, ligne in enumerate(grille):
        for c, n in enumerate(ligne):
            x, y = x0 + c * u, y0 + (nr - 1 - r) * u
            L.append(rf"\filldraw[fill={fond},draw=otNavy!80,line width=.5pt] ({f(x)},{f(y)}) rectangle ({f(x+u)},{f(y+u)});")
            if n is not None:
                L.append(txt((x + u / 2, y + u / 2), f"${n}$", "center", color))
    return L


# ---------------------------------------------------------------- patrons (2D)
def rect(x0, y0, w, h, fill="otSky", draw="solide"):
    pts = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    return [fill2(pts, fill), poly2(pts, draw)]


def carres(cases, u, x0=0.0, y0=0.0, couleurs=None, nums=None, fond="otSky", num_color="otInk"):
    """Assemblage de carrés : cases = [(colonne, ligne)] (ligne vers le haut)."""
    L = []
    for idx, (c, r) in enumerate(cases):
        fc = (couleurs or {}).get(idx, fond)
        L += rect(x0 + c * u, y0 + r * u, u, u, fc, "otNavy,line width=.8pt")
    if nums:
        for idx, (c, r) in enumerate(cases):
            if idx in nums:
                L.append(txt((x0 + (c + .5) * u, y0 + (r + .5) * u), nums[idx], "center", num_color))
    return L


def base_triangle(o, tri, s, lab_base, lab_h, fill=BASE_E, trait="solide", col=OR, legende=None,
                  cotes_cotes=None):
    """Triangle de base dessiné à part (apex au-dessus du côté horizontal) : hauteur en pointillés
    orange, cote verticale à gauche pour la hauteur, côté horizontal coté dessous."""
    P = lambda q: (o[0] + s * q[0], o[1] + s * q[1])
    A, B, C = (P(q) for q in tri)
    Hf = (C[0], A[1])
    L = [fill2([A, B, C], fill), poly2([A, B, C], trait), seg(C, Hf, "hauteurT"),
         angle_droit2(Hf, (1, 0), (0, 1), 0.11, ANGO),
         txt(lerp(A, B, 0.5), lab_base, "north", col, ",yshift=-1pt")]
    xg = A[0] - 0.22
    L += [rf"\draw[cote] ({f(xg)},{f(A[1])}) -- ({f(xg)},{f(C[1])});",
          rf"\draw[otMuted!70,line width=.4pt] {Q(C)} -- ({f(xg-0.06)},{f(C[1])});",
          nd((xg, (A[1] + C[1]) / 2), lab_h, 180, 0.05, col)]
    for (p, q, lab, side) in (cotes_cotes or []):
        L.append(milieu(P(p), P(q), lab, side, 0.07, col))
    if legende:
        L.append(txt(((A[0] + B[0]) / 2, C[1] + 0.08), legende, "south", "otMuted"))
    return L


# ======================================================================== COURS
def c_solides():
    L = []
    y1 = 2.95
    # cube
    v = Vue(1, (0.0, y1))
    cu = pave(1.5, 1.5, 1.5, v)
    L += cu.dessin()
    L.append(titre((0.75, y1 - 0.12), "Cube"))
    # pavé
    v = Vue(1, (3.1, y1))
    pv = pave(2.7, 1.5, 1.3, v)
    L += pv.dessin()
    L.append(titre((3.1 + 1.35, y1 - 0.12), "Pavé droit"))
    # prisme droit à base triangulaire
    v = Vue(1, (0.0, 0.0))
    pr = prisme_vertical([(0, 0), (2.2, 0), (0.7, 1.6)], 1.55, v)
    L += pr.dessin(remplis={("b0", "b1", "b2"): BASE_E})
    L.append(titre((1.1, -0.12), "Prisme droit"))
    # cylindre
    xc, r, h = 4.5, 0.78, 1.65
    L += cylindre(xc, 0, r, h, dessus=BASE_E)
    L.append(titre((xc, -RY * r - 0.1), r"Cylindre\\de révolution"))
    return tikz(L)


FIGURES["c_solides"] = c_solides()


def c_perspective():
    s = 0.8
    v = Vue(s, (0, 0))
    a, b, c = 3.4, 2.3, 1.9
    pv = pave(a, b, c, v)
    L = pv.dessin(remplis={("A", "B", "F", "E"): "otOrange!22"})
    # fuyante [EH] : texte au-dessus, trait de rappel vertical hors du solide
    m = lerp(pv.p("E"), pv.p("H"), 0.45)
    ytop = pv.p("H")[1] + 0.4
    L += [lien(m, (m[0], ytop)), txt((m[0], ytop), r"fuyante : oblique et raccourcie", "south", NV)]
    L.append(txt((s * a / 2, -0.1), r"face avant : en vraie grandeur", "north", OR))
    y = -0.72
    L += [rf"\draw[cache] (0.1,{f(y)}) -- (0.8,{f(y)});",
          txt((0.9, y), r"arête cachée : en pointillés", "west", NV)]
    return tikz(L)


FIGURES["c_perspective"] = c_perspective()


def c_empilement():
    u = 0.62
    v = Vue(u, (0, 0))
    H = {(0, 0): 1, (1, 0): 2, (0, 1): 2, (1, 1): 3}
    L = empilement(v, H)
    L.append(titre((u, -0.12), "Empilement"))
    x0 = 2.75
    L += plan_cote(x0, 0.0, [[2, 3], [1, 2]], u)
    L.append(titre((x0 + u, -0.12), r"Vue de dessus\\(nombre de cubes)"))
    x1 = 5.0
    L += vue_colonnes(x1, 0.0, [2, 3], u)
    L.append(titre((x1 + u, -0.12), "Vue de face"))
    return tikz(L)


FIGURES["c_empilement"] = c_empilement()


def c_patron_cube():
    u = 0.72
    cases = [(0, 1), (1, 1), (2, 1), (3, 1), (1, 2), (1, 0)]
    coul = {0: "otNavy!18", 2: "otNavy!18", 1: "otGreen!32", 3: "otGreen!32", 4: "otOrange!30", 5: "otOrange!30"}
    L = carres(cases, u, 0, 0, coul)
    L.append(titre((2 * u, -0.12), "Un patron du cube"))
    # cube en perspective, faces visibles de mêmes couleurs
    v = Vue(1, (4.0, 0.25))
    cu = pave(1.45, 1.45, 1.45, v)
    L += cu.dessin(remplis={("A", "B", "F", "E"): "otGreen!32", ("E", "F", "G", "H"): "otOrange!30",
                            ("B", "C", "G", "F"): "otNavy!18"})
    L.append(titre((4.0 + 0.72 + 0.33, -0.12), "Le cube obtenu"))
    return tikz(L)


FIGURES["c_patron_cube"] = c_patron_cube()


def c_patron_prisme():
    L = []
    s = 0.42
    t = 0.36
    # solide au-dessus du patron (figure étroite, lisible sur téléphone)
    v = Vue(s, (1.35, 9 * t + 0.75))
    # triangle rectangle en A : AB = 4 (vers la droite), AC = 3 (vers l'arrière), BC = 5 ; hauteur 6
    pr = prisme_vertical([(0, 0), (4, 0), (0, 3)], 6, v, bas=["A", "B", "C"], haut=["D", "E", "F"])
    L += pr.dessin(remplis={("D", "E", "F"): BASE_E})
    L += [txt(lerp(pr.p("A"), pr.p("B"), 0.5), r"$4$ cm", "north", "otInk", ",yshift=-1pt"),
          milieu(pr.p("D"), pr.p("F"), r"$3$ cm", 1, 0.08),
          milieu(pr.p("E"), pr.p("F"), r"$5$ cm", -1, 0.08)]
    L += cote2(pr.p("A"), pr.p("D"), r"$6$ cm", 1, 0.22)
    # patron : bandes 3, 4, 5 (hauteur 6) ; triangles sur la bande de 4, angle droit côté bande de 3
    x0, y0 = 0.0, 0.0
    P = lambda x, y: (x0 + t * x, y0 + t * y)
    for xa, w in ((0, 3), (3, 4), (7, 5)):
        L += [fill2([P(xa, 0), P(xa + w, 0), P(xa + w, 6), P(xa, 6)], "otSky")]
    for tri in (((3, 6), (7, 6), (3, 9)), ((3, 0), (7, 0), (3, -3))):
        L.append(fill2([P(*q) for q in tri], BASE_E))
    L.append(poly2([P(0, 0), P(3, 0), P(3, -3), P(7, 0), P(12, 0), P(12, 6), P(7, 6), P(3, 9), P(3, 6), P(0, 6)], "solide"))
    L += [seg(P(3, 0), P(3, 6), "fin"), seg(P(7, 0), P(7, 6), "fin"), seg(P(3, 6), P(7, 6), "fin"), seg(P(3, 0), P(7, 0), "fin")]
    for xa, w in ((0, 3), (3, 4), (7, 5)):
        L.append(txt(P(xa + w / 2, 3), rf"${w}$ cm", "center"))
    L += cote2(P(12, 0), P(12, 6), r"$6$ cm", -1, 0.22)
    yb = -3.0
    L += [rf"\draw[cote] {Q(P(0, yb - 0.6))} -- {Q(P(12, yb - 0.6))};",
          rf"\draw[otMuted!70,line width=.4pt] {Q(P(0, 0))} -- {Q(P(0, yb - 0.8))} {Q(P(12, 0))} -- {Q(P(12, yb - 0.8))};",
          txt(P(6, yb - 0.75), r"$3 + 4 + 5 = 12$ cm :\\le périmètre de la base", "north", OR, ",align=center")]
    return tikz(L)


FIGURES["c_patron_prisme"] = c_patron_prisme()


def c_patron_cylindre():
    L = []
    xc, r, h = 0.8, 0.62, 1.6
    yb = 0.85
    L += cylindre(xc, yb, r, h, dessus=BASE_E)
    L += [seg((xc, yb + h), (xc + r, yb + h), "otNavy,line width=.7pt"), pt((xc, yb + h)),
          txt(haut_ellipse(xc, yb + h, r, 0.5), "$r$", "south")]
    L += cote2((xc - r, yb), (xc - r, yb + h), "$h$", 1, 0.2)
    # patron : rectangle 2πr × h, deux disques
    x0 = 2.35
    Lr = 2 * math.pi * r
    y0 = yb
    L += rect(x0, y0, Lr, h, "otSky")
    for cy in (y0 + h + r, y0 - r):
        cx = x0 + Lr / 2
        L += [rf"\fill[{BASE_E}] {Q((cx, cy))} circle ({f(r)});", rf"\draw[solide] {Q((cx, cy))} circle ({f(r)});"]
    cx, cy = x0 + Lr / 2, y0 + h + r
    L += [seg((cx, cy), (cx + r, cy), "otNavy,line width=.7pt"), pt((cx, cy)), txt((cx + r / 2, cy + 0.03), "$r$", "south")]
    ya = y0 + h * 0.42
    L += [rf"\draw[cote] ({f(x0+0.06)},{f(ya)}) -- ({f(x0+Lr-0.06)},{f(ya)});",
          txt((x0 + Lr / 2, ya + 0.05), r"$2 \times \pi \times r$", "south", OR)]
    L += cote2((x0 + Lr, y0), (x0 + Lr, y0 + h), "$h$", -1, 0.2)
    L.append(txt((x0 + Lr / 2, y0 - 2 * r - 0.12), r"longueur du rectangle\\= périmètre du disque", "north", OR, ",align=center"))
    return tikz(L)


FIGURES["c_patron_cylindre"] = c_patron_cylindre()


def c_pave_cubes():
    u = 0.55
    v = Vue(u, (0, 0))
    H = {(i, j): 2 for i in range(4) for j in range(3)}
    L = empilement(v, H, lambda i, j, k: "vert" if k == 1 else "bleu")
    xm = v(2, 1.5, 0)[0]
    L += [txt((xm, -0.1), r"chaque petit cube : $1$ cm³", "north", "otMuted"),
          txt((xm, -0.62), r"une couche : $4 \times 3 = 12$ cubes", "north", VE),
          txt((xm, -1.12), r"deux couches : $12 \times 2 = 24$ cubes", "north"),
          txt((xm, -1.62), r"$V = 4 \times 3 \times 2 = 24$ cm³", "north", NV)]
    return tikz(L)


FIGURES["c_pave_cubes"] = c_pave_cubes()


def c_volumes():
    L = []
    v = Vue(0.5, (0, 0))
    pv = pave(4, 3, 3, v)
    L += pv.dessin(remplis={("E", "F", "G", "H"): BASE_E})
    L.append(txt(moy([pv.p(k) for k in "EFGH"]), r"$\mathcal{B}$"))
    L += cote2(pv.p("A"), pv.p("E"), "$h$", 1, 0.22, OR)
    L.append(titre(v(2, 0, 0), r"Pavé droit"))
    v2 = Vue(0.5, (3.35, 0))
    pr = prisme_vertical([(0, 0), (4, 0), (1, 3)], 3, v2)
    L += pr.dessin(remplis={("b0", "b1", "b2"): BASE_E})
    L.append(txt(moy([pr.p(k) for k in ("b0", "b1", "b2")]), r"$\mathcal{B}$"))
    L += cote2(pr.p("a1"), pr.p("b1"), "$h$", -1, 0.22, OR)
    L.append(titre(v2(2, 0, 0), r"Prisme droit"))
    # cylindre sur une deuxième ligne, centré (figure étroite pour le téléphone)
    xc, r, h = 3.2, 0.7, 1.5
    yc = -2.75
    L += cylindre(xc, yc, r, h, dessus=BASE_E)
    L += [txt((xc, yc + h), r"$\mathcal{B}$"), ]
    L += cote2((xc + r, yc), (xc + r, yc + h), "$h$", -1, 0.22, OR)
    L.append(titre((xc, yc - RY * r - 0.02), r"Cylindre"))
    return tikz(L)


FIGURES["c_volumes"] = c_volumes()


def c_dm3():
    v = Vue(0.3, (0, 0))
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


FIGURES["c_dm3"] = c_dm3()


# ======================================================================== EXERCICES
# ---------------------------------------------------------------- 3050 : reconnaître des solides
MAISON = [(0, 0), (1.5, 0), (1.5, 0.95), (0.75, 1.55), (0, 0.95)]


def e3050_solides(corrige):
    L = []
    y1 = 3.3
    bf = BASE_V if corrige else None
    noms = {"1": "cube", "2": "prisme droit", "3": r"cylindre\\de révolution", "4": "pavé droit", "5": "prisme droit"}

    def lab(p, k):
        if corrige:
            return txt(p, r"\textbf{" + k + r"} : " + noms[k], "north", VE, ",align=center")
        return titre(p, k)

    v = Vue(1, (0, y1))
    L += pave(1.35, 1.35, 1.35, v).dessin()
    L.append(lab((0.68, y1 - 0.12), "1"))
    v = Vue(1, (2.45, y1))
    pr = prisme_vertical([(0, 0), (1.9, 0), (0.5, 1.4)], 1.4, v)
    L += pr.dessin(remplis={("b0", "b1", "b2"): bf} if corrige else None)
    if corrige:
        L.append(poly2([pr.p(k) for k in ("b0", "b1", "b2")], "vert"))
    L.append(lab((2.45 + 0.95, y1 - 0.12), "2"))
    xc, r = 5.6, 0.62
    L += cylindre(xc, y1, r, 1.45, dessus=bf, dessus_trait="vert" if corrige else None)
    L.append(lab((xc, y1 - RY * r - 0.08), "3"))
    v = Vue(1, (0.3, 0))
    L += pave(2.5, 1.2, 1.05, v).dessin()
    L.append(lab((0.3 + 1.25, -0.12), "4"))
    v = Vue(1, (3.75, 0))
    pm = prisme_couche(MAISON, 1.9, v)
    av = tuple(f"a{i}" for i in range(5))
    L += pm.dessin(remplis={av: bf} if corrige else None)
    if corrige:
        L.append(poly2([pm.p(k) for k in av], "vert"))
    L.append(lab((3.75 + 0.75, -0.12), "5"))
    return tikz(L)


FIGURES["e3050_solides"] = e3050_solides(False)
FIGURES["e3050_solides_corrige"] = e3050_solides(True)

PR3050 = ([(0, 0), (3.2, 0), (1.1, 2.4)], 3.0)


def e3050_prisme(corrige):
    base, h = PR3050
    v = Vue(0.8, (0, 0))
    pr = prisme_vertical(base, h, v, bas=["A", "B", "C"], haut=["D", "E", "F"])
    if not corrige:
        L = pr.dessin()
    else:
        # les deux bases en vert (arêtes cachées de la base ABC en vert pointillé)
        sp = {e: ("vertc" if not pr.visible(*e) else "vert") for e in (("A", "B"), ("B", "C"), ("A", "C"))}
        L = pr.dessin(remplis={("D", "E", "F"): BASE_V}, speciaux=sp)
        L.append(poly2([pr.p(k) for k in "DEF"], "vert"))
        for a, b in (("A", "D"), ("B", "E"), ("C", "F")):
            L += codage(pr.p(a), pr.p(b), 2, VE)
    L += [nd(pr.p("A"), "$A$", 225), nd(pr.p("B"), "$B$", 315), nd(pr.p("C"), "$C$", 15, 0.07),
          nd(pr.p("D"), "$D$", 135), nd(pr.p("E"), "$E$", 0, 0.08), nd(pr.p("F"), "$F$", 90)]
    return tikz(L)


FIGURES["e3050_prisme"] = e3050_prisme(False)
FIGURES["e3050_prisme_corrige"] = e3050_prisme(True)


# ---------------------------------------------------------------- 3054 : empilement et vues
H3054 = {(0, 0): 1, (1, 0): 2, (2, 0): 1, (0, 1): 3, (1, 1): 2, (2, 1): 2}


def e3054_enonce():
    u = 0.75
    v = Vue(u, (0, 0))
    L = empilement(v, H3054)
    fl = r"otMuted,line width=.8pt,-{Stealth[length=2.2mm]}"
    # flèche « face » devant, flèche « droite » à droite
    L += [rf"\draw[{fl}] ({f(1.5*u)},-0.75) -- ({f(1.5*u)},-0.2);",
          txt((1.5 * u, -0.78), "vue de face", "north", "otMuted"),
          rf"\draw[{fl}] ({f(v(3, 1, 0)[0] + 1.0)},{f(v(3, 1, 0.6)[1])}) -- ({f(v(3, 1, 0)[0] + 0.45)},{f(v(3, 1, 0.6)[1])});",
          txt((v(3, 1, 0)[0] + 1.03, v(3, 1, 0.6)[1]), r"vue de\\droite", "west", "otMuted", ",align=left")]
    return tikz(L)


FIGURES["e3054_enonce"] = e3054_enonce()


def e3054_vues():
    u = 0.55
    L = plan_cote(0, 0, [[3, 2, 2], [1, 2, 1]], u, VE)
    L.append(titre((1.5 * u, -0.12), r"Vue de dessus\\(nombre de cubes)"))
    x1 = 2.65
    L += vue_colonnes(x1, 0, [3, 2, 2], u, "otGreen!30", "otGreenDark")
    L.append(titre((x1 + 1.5 * u, -0.12), "Vue de face"))
    x2 = 5.15
    L += vue_colonnes(x2, 0, [2, 3], u, "otGreen!30", "otGreenDark")
    L.append(titre((x2 + u, -0.12), "Vue de droite"))
    return tikz(L)


FIGURES["e3054_vues"] = e3054_vues()


def e3054_pave(corrige):
    u = 0.5
    v = Vue(u, (0, 0))
    H = {(i, j): 3 for i in range(5) for j in range(2)}
    L = empilement(v, H, (lambda i, j, k: "vert" if k == 0 else "bleu") if corrige else None)
    if corrige:
        xm = v(2.5, 1, 0)[0]
        L += [txt((xm, -0.1), r"une couche : $5 \times 2 = 10$ cubes", "north", VE),
              txt((xm, -0.6), r"$3$ couches : $10 \times 3 = 30$ cubes", "north")]
    return tikz(L)


FIGURES["e3054_pave"] = e3054_pave(False)
FIGURES["e3054_pave_corrige"] = e3054_pave(True)


# ---------------------------------------------------------------- 3047 : patrons de cube et de pavé
PATRONS_3047 = {
    "A": [(0, 1), (1, 1), (2, 1), (3, 1), (1, 2), (1, 0)],
    "B": [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (3, 1)],
    "C": [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2)],
    "D": [(0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (3, 1)],
}
NUMS_3047 = {0: "$1$", 1: "$2$", 2: "$3$", 3: "$4$", 4: "$5$", 5: "$6$"}


def e3047_patrons(corrige):
    u = 0.5
    L = []
    pos = {"A": (0, 2.25), "B": (3.0, 2.25 + 0.5 * u), "C": (0, 0), "D": (3.0, 0.5 * u)}
    for k, cases in PATRONS_3047.items():
        x0, y0 = pos[k]
        coul, nums = None, (NUMS_3047 if k == "A" else None)
        if corrige:
            if k == "A":
                coul = {0: "otNavy!18", 2: "otNavy!18", 1: "otGreen!32", 3: "otGreen!32", 4: "otOrange!30", 5: "otOrange!30"}
            elif k == "C":
                # pliage : (0,0) et (1,1) opposées ? calcul dans verif ; paires : {0,3}, {1,4}, {2,5}
                coul = {0: "otNavy!18", 3: "otNavy!18", 1: "otGreen!32", 4: "otGreen!32", 2: "otOrange!30", 5: "otOrange!30"}
            elif k == "B":
                coul = {4: "otRed!25", 5: "otRed!25"}
            else:
                coul = {0: "otRed!25", 1: "otRed!25", 2: "otRed!25", 3: "otRed!25"}
        L += carres(cases, u, x0, y0, coul, nums)
        L.append(titre((x0 - 0.12, y0 + max(c[1] for c in cases) * u + u), k, "north east"))
        if corrige:
            ok = k in ("A", "C")
            ytxt = y0 - 0.1 if k in ("A", "C") else pos[k][1] - 0.1
            L.append(txt((x0 + 2 * u, ytxt), "patron" if ok else "pas un patron", "north", VE if ok else "otRed!85!black"))
    return tikz(L)


FIGURES["e3047_patrons"] = e3047_patrons(False)
FIGURES["e3047_patrons_corrige"] = e3047_patrons(True)


def e3047_pave(corrige):
    L = []
    s = 0.36
    v = Vue(s, (0, 1.0))
    pv = pave(5, 3, 2, v)
    L += pv.dessin()
    L += [txt(lerp(pv.p("A"), pv.p("B"), 0.5), r"$5$ cm", "north", OR, ",yshift=-1pt"),
          milieu(pv.p("B"), pv.p("C"), r"$3$ cm", -1, 0.07, OR),
          ]
    L += cote2(pv.p("A"), pv.p("E"), r"$2$ cm", 1, 0.2, OR)
    # patron en croix : fond 5 × 3 au centre
    t = 0.3
    x0, y0 = 3.55, 0.0
    P = lambda x, y: (x0 + t * x, y0 + t * y)
    faces = [(2, 2, 5, 3), (2, 0, 5, 2), (2, 5, 5, 2), (2, 7, 5, 3), (0, 2, 2, 3), (7, 2, 2, 3)]
    for (xa, ya, w, h) in faces:
        L.append(fill2([P(xa, ya), P(xa + w, ya), P(xa + w, ya + h), P(xa, ya + h)], "otSky"))
    for (xa, ya, w, h) in faces:
        L.append(poly2([P(xa, ya), P(xa + w, ya), P(xa + w, ya + h), P(xa, ya + h)], "otNavy,line width=.8pt"))
    col = VE if corrige else OR
    L.append(txt(lerp(P(2, 0), P(7, 0), 0.5), r"$5$ cm", "north", OR, ",yshift=-1pt"))
    if corrige:
        La, Lb, Lc = r"$a = 2$ cm", r"$b = 3$ cm", r"$c = 5$ cm"
    else:
        La, Lb, Lc = "$a$", "$b$", "$c$"
    L += [txt((P(2, 2)[0] - 0.04, P(2, 2)[1] - 0.03), La, "north east", col),
          nd(lerp(P(7, 7), P(7, 10), 0.5), Lb, 0, 0.08, col),
          txt(lerp(P(2, 10), P(7, 10), 0.5), Lc, "south", col)]
    return tikz(L)


FIGURES["e3047_pave"] = e3047_pave(False)
FIGURES["e3047_pave_corrige"] = e3047_pave(True)


# ---------------------------------------------------------------- 3045 : brique de jus
def e3045(corrige):
    s = 0.13
    v = Vue(s, (0, 0))
    pv = pave(9, 6, 20, v)
    if corrige:
        L = pv.dessin(remplis={("E", "F", "G", "H"): BASE_V}, speciaux={("A", "E"): "rep"})
        L.append(poly2([pv.p(k) for k in "EFGH"], "vert"))
        L.append(nd(lerp(pv.p("A"), pv.p("E"), 0.5), r"$h = 20$ cm", 180, 0.12, VE))
        L += [lien(lerp(pv.p("E"), pv.p("G"), 0.5), (pv.p("G")[0] + 0.35, pv.p("G")[1] + 0.25)),
              txt((pv.p("G")[0] + 0.37, pv.p("G")[1] + 0.25), r"base : $9 \times 6 = 54$ cm²", "west", VE)]
    else:
        L = pv.dessin()
        L += cote2(pv.p("A"), pv.p("E"), r"$20$ cm", 1, 0.2, OR)
    L += [txt(lerp(pv.p("A"), pv.p("B"), 0.5), r"$9$ cm", "north", OR, ",yshift=-1pt"),
          milieu(pv.p("B"), pv.p("C"), r"$6$ cm", -1, 0.07, OR)]
    return tikz(L)


FIGURES["e3045_brique"] = e3045(False)
FIGURES["e3045_brique_corrige"] = e3045(True)


# ---------------------------------------------------------------- 3055 : volumes de prismes droits
TRI_3055 = [(0, 0), (6, 0), (4, 4)]   # côté 6, hauteur relative 4


def e3055(corrige):
    L = []
    s = 0.3
    # A : pavé 6 × 4 × 2,5
    v = Vue(s, (0, 3.2))
    pv = pave(6, 4, 2.5, v)
    if corrige:
        L += pv.dessin(remplis={("E", "F", "G", "H"): BASE_V}, speciaux={("A", "E"): "rep"})
        L.append(poly2([pv.p(k) for k in "EFGH"], "vert"))
        L.append(nd(lerp(pv.p("A"), pv.p("E"), 0.5), r"$h$", 180, 0.1, VE))
    else:
        L += pv.dessin()
        L += cote2(pv.p("A"), pv.p("E"), r"$2{,}5$ cm", 1, 0.2, OR)
    L += [txt(lerp(pv.p("A"), pv.p("B"), 0.5), r"$6$ cm", "north", OR, ",yshift=-1pt"),
          milieu(pv.p("B"), pv.p("C"), r"$4$ cm", -1, 0.07, OR),
          titre((pv.p("A")[0] - 0.75, pv.p("E")[1] + 0.3), "A", "north")]
    # B : prisme debout, base triangle rectangle 5 × 4, hauteur 9
    v = Vue(s, (3.8, 3.2 - 0.55))
    pr = prisme_vertical([(0, 0), (5, 0), (0, 4)], 9, v, bas=["P", "Q", "R"], haut=["S", "T", "U"])
    if corrige:
        L += pr.dessin(remplis={("S", "T", "U"): BASE_V}, speciaux={("Q", "T"): "rep"})
        L.append(poly2([pr.p(k) for k in "STU"], "vert"))
        L.append(nd(lerp(pr.p("Q"), pr.p("T"), 0.5), r"$h$", 0, 0.1, VE))
    else:
        L += pr.dessin()
        L += cote2(pr.p("Q"), pr.p("T"), r"$9$ cm", -1, 0.2, OR)
    S_, T_, U_ = pr.p("S"), pr.p("T"), pr.p("U")
    L += [angle_droit2(S_, sub(T_, S_), sub(U_, S_), 0.13, ANGO),
          txt(lerp(pr.p("P"), pr.p("Q"), 0.5), r"$5$ cm", "north", OR, ",yshift=-1pt"),
          milieu(S_, U_, r"$4$ cm", 1, 0.07, OR),
          titre((pr.p("P")[0] - 0.3, (pr.p("P")[1] + S_[1]) / 2), "B", "east")]
    # C : prisme couché, base triangle (côté 6, hauteur 4), longueur 10 ; base redessinée à droite
    v = Vue(s, (0.25, 0))
    pc = prisme_couche(TRI_3055, 10, v, av=["K", "L", "M"], ar=["N", "O", "P2"])
    if corrige:
        L += pc.dessin(remplis={("K", "L", "M"): BASE_V}, speciaux={("L", "O"): "rep"})
        L.append(poly2([pc.p(k) for k in "KLM"], "vert"))
        L.append(milieu(pc.p("L"), pc.p("O"), r"$h = 10$ cm", -1, 0.1, VE))
    else:
        L += pc.dessin()
        L.append(milieu(pc.p("L"), pc.p("O"), r"$10$ cm", -1, 0.1, OR))
    L.append(titre((pc.p("K")[0] - 0.05, pc.p("M")[1] + 0.3), "C", "north east"))
    L += base_triangle((4.7, 0.05), TRI_3055, 0.3, r"$6$ cm", r"$4$ cm",
                       fill=BASE_V if corrige else "otSky", trait="vert" if corrige else "solide",
                       legende="une base de C" if corrige else "la face avant de C")
    return tikz(L)


FIGURES["e3055_enonce"] = e3055(False)
FIGURES["e3055_corrige"] = e3055(True)


# ---------------------------------------------------------------- 3051 : volumes de cylindres
def e3051(corrige):
    s = 0.2
    L = []
    # 1 : r = 3, h = 10
    xc = 0.85
    L += cyl_donnees(xc, 0, 3 * s, 10 * s, lab_r=r"$3$ cm", lab_h=r"$10$ cm", corrige=corrige)
    L.append(titre((xc, -RY * 3 * s - 0.1), "1"))
    # 2 : d = 8, h = 5
    xc = 3.35
    L += cyl_donnees(xc, 0, 4 * s, 5 * s, lab_d=r"$8$ cm", lab_h=r"$5$ cm", corrige=corrige)
    L.append(titre((xc, -RY * 4 * s - 0.1), "2"))
    # 3 : r = 2 cm, h = 1,5 dm = 15 cm
    xc = 5.95
    L += cyl_donnees(xc, 0, 2 * s, 15 * s, lab_r=r"$2$ cm", lab_h=r"$1{,}5$ dm", corrige=corrige)
    L.append(titre((xc, -RY * 2 * s - 0.1), "3"))
    return tikz(L)


FIGURES["e3051_enonce"] = e3051(False)
FIGURES["e3051_corrige"] = e3051(True)


# ---------------------------------------------------------------- 3061 : boîte en prisme, patron
TRI_3061 = [(0, 0), (6, 0), (0, 8)]   # triangle rectangle : côtés 6 et 8, troisième côté 10


def e3061_solide(corrige):
    s = 0.25
    v = Vue(s, (0, 0))
    pc = prisme_couche(TRI_3061, 15, v, av=["A", "B", "C"], ar=["D", "E", "F"])
    if corrige:
        L = pc.dessin(remplis={("A", "B", "C"): BASE_V}, speciaux={("B", "E"): "rep"})
        L.append(poly2([pc.p(k) for k in "ABC"], "vert"))
        L.append(milieu(pc.p("B"), pc.p("E"), r"$h = 15$ cm", -1, 0.1, VE))
        L.append(txt(moy([pc.p(k) for k in "ABC"]), r"$\mathcal{B}$", "center", VE, ",xshift=-3pt,yshift=-4pt"))
    else:
        L = pc.dessin()
        L.append(milieu(pc.p("B"), pc.p("E"), r"$15$ cm", -1, 0.1, OR))
    L += [angle_droit2(pc.p("A"), (1, 0), (0, 1), 0.14, ANGO),
          txt(lerp(pc.p("A"), pc.p("B"), 0.5), r"$6$ cm", "north", OR, ",yshift=-1pt"),
          nd(lerp(pc.p("A"), pc.p("C"), 0.5), r"$8$ cm", 180, 0.08, OR),
          milieu(pc.p("C"), pc.p("B"), r"$10$ cm", 1, 0.07, OR, "", 0.3)]
    return tikz(L)


FIGURES["e3061_solide"] = e3061_solide(False)
FIGURES["e3061_solide_corrige"] = e3061_solide(True)


def e3061_patron(corrige):
    t = 0.24
    P = lambda x, y: (t * x, t * y)
    L = []
    for xa, w in ((0, 6), (6, 8), (14, 10)):
        L.append(fill2([P(xa, 0), P(xa + w, 0), P(xa + w, 15), P(xa, 15)], "otSky"))
    tri = (((6, 15), (14, 15), (6, 21)), ((6, 0), (14, 0), (6, -6)))
    for tr in tri:
        L.append(fill2([P(*q) for q in tr], BASE_V if corrige else BASE_E))
    L.append(poly2([P(0, 0), P(6, 0), P(6, -6), P(14, 0), P(24, 0), P(24, 15), P(14, 15), P(6, 21), P(6, 15), P(0, 15)],
                   "solide"))
    L += [seg(P(6, 0), P(6, 15), "fin"), seg(P(14, 0), P(14, 15), "fin"), seg(P(6, 15), P(14, 15), "fin"), seg(P(6, 0), P(14, 0), "fin")]
    if corrige:
        L += [poly2([P(*q) for q in tr], "vert") for tr in tri]
        L += [angle_droit2(P(6, 15), (1, 0), (0, 1), 0.13, ANGV), angle_droit2(P(6, 0), (1, 0), (0, -1), 0.13, ANGV)]
        la, lb, lc = r"$a = 8$ cm", r"$b = 10$ cm", r"$c = 15$ cm"
        col = VE
        L.append(seg(P(24, 0), P(24, 15), "rep"))
    else:
        L += [angle_droit2(P(6, 15), (1, 0), (0, 1), 0.13, ANG), angle_droit2(P(6, 0), (1, 0), (0, -1), 0.13, ANG)]
        la, lb, lc = "$a$", "$b$", "$c$"
        col = OR
    L += [txt(P(3, 7.5), r"$6$ cm", "center", OR),
          txt(P(10, 7.5), la, "center", col),
          txt(P(19, 7.5), lb, "center", col),
          nd(P(24, 7.5), lc, 0, 0.1, col),
          nd(P(6, 18), r"$6$ cm", 180, 0.08, OR)]
    return tikz(L)


FIGURES["e3061_patron"] = e3061_patron(False)
FIGURES["e3061_patron_corrige"] = e3061_patron(True)


# ---------------------------------------------------------------- 3052 : boîte de conserve
def e3052_enonce():
    s = 0.2
    xc, r, h = 1.1, 5 * s, 11 * s
    L = cylindre(xc, 0, r, h)
    # étiquette : bande colorée sur la surface latérale
    y0, y1 = 0.18, h - 0.18
    L.insert(2, rf"\fill[otOrange!22] ({f(xc-r)},{f(y0)}) -- ({f(xc-r)},{f(y1)}) "
                rf"arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(RY*r)}] -- ({f(xc+r)},{f(y0)}) "
                rf"arc[start angle=0,end angle=-180,x radius={f(r)},y radius={f(RY*r)}] -- cycle;")
    L += [arc_ellipse(xc, y0, r, 180, 360, "fin"), arc_ellipse(xc, y1, r, 180, 360, "fin"),
          txt((xc, (y0 + y1) / 2 - 0.12), r"\textit{étiquette}", "center", "otOrange!70!black")]
    L += [seg((xc - r, h), (xc + r, h), "donnee"), pt((xc, h), OR, 1.2),
          txt(haut_ellipse(xc, h, r, 0.0), r"$10$ cm", "south", OR)]
    L += cote2((xc + r, 0), (xc + r, h), r"$11$ cm", -1, 0.22, OR)
    return tikz(L)


FIGURES["e3052_enonce"] = e3052_enonce()


def e3052_patron():
    s = 0.19
    r = 5 * s
    Lr = math.pi * 10 * s
    h = 11 * s
    x0, y0 = 0, 0
    L = rect(x0, y0, Lr, h, "otOrange!22")
    for cy, cx in ((y0 + h + r, x0 + Lr * 0.25), (y0 - r, x0 + Lr * 0.75)):
        L += [rf"\fill[otSky] {Q((cx, cy))} circle ({f(r)});", rf"\draw[solide] {Q((cx, cy))} circle ({f(r)});"]
    cx, cy = x0 + Lr * 0.25, y0 + h + r
    L += [seg((cx, cy), (cx + r, cy), "donnee"), pt((cx, cy), OR, 1.2), txt((cx + r / 2, cy + 0.03), r"$5$ cm", "south", OR)]
    ya = y0 + h * 0.4
    L += [rf"\draw[otGreenDark,line width=.8pt,{{Stealth[length=1.8mm]}}-{{Stealth[length=1.8mm]}}] ({f(x0+0.06)},{f(ya)}) -- ({f(x0+Lr-0.06)},{f(ya)});",
          txt((x0 + Lr / 2, ya + 0.06), r"$\pi \times 10 \approx 31{,}4$ cm", "south", VE)]
    L += cote2((x0 + Lr, y0), (x0 + Lr, y0 + h), r"$11$ cm", -1, 0.22, OR)
    return tikz(L)


FIGURES["e3052_patron"] = e3052_patron()


def e3052_volume():
    s = 0.2
    xc, r, h = 1.1, 5 * s, 11 * s
    L = cyl_donnees(xc, 0, r, h, lab_r=r"$5$ cm", lab_h=r"$h = 11$ cm", corrige=True)
    L.append(txt(sous_ellipse(xc, 0, r, 0.0, 0.1), r"base : disque de rayon $5$ cm", "north", VE))
    return tikz(L)


FIGURES["e3052_volume"] = e3052_volume()


# ---------------------------------------------------------------- 3059 : aquarium et décor
AQ = (60, 30, 40)       # longueur, profondeur, hauteur (cm)
DECOR = (5, 20)         # rayon, hauteur du cylindre (cm)


def e3059(corrige):
    s = 0.056
    v = Vue(s, (0, 0))
    a, b, c = AQ
    aq = pave(a, b, c, v)
    L = []
    # décor : cylindre posé au fond, au centre ; ellipse vue de face (approximation cavalière des cylindres du chapitre)
    rD, hD = DECOR
    xc3, yc3 = 44, 15
    base = v(xc3, yc3, 0)
    if not corrige:
        L += [fill2([aq.p(k) for k in fa], "otSky!55") for fa in aq.faces_visibles()]
        for e in aq.cachees():
            L.append(seg(aq.p(e[0]), aq.p(e[1]), "cache"))
        L += cylindre(base[0], base[1], rD * s, hD * s, fond="otSky")
        for e, vis in aq.aretes.items():
            if vis:
                L.append(seg(aq.p(e[0]), aq.p(e[1]), "solide"))
        L += cote2(aq.p("A"), aq.p("E"), r"$40$ cm", 1, 0.2, OR)
        L += [txt(lerp(aq.p("A"), aq.p("B"), 0.5), r"$60$ cm", "north", OR, ",yshift=-1pt"),
              milieu(aq.p("B"), aq.p("C"), r"$30$ cm", -1, 0.07, OR)]
        # décor seul, à droite, avec ses dimensions
        xr = aq.p("C")[0] + 1.5
        L += cyl_donnees(xr, 0.35, rD * 0.1, hD * 0.1, lab_r=r"$5$ cm", lab_h=r"$20$ cm", h_gauche=False)
        L.append(titre((xr, 0.35 - RY * rD * 0.1 - 0.1), "le décor"))
        return tikz(L)
    # corrigé : eau sur 30 cm (base en vert), décor immergé, arêtes de l'aquarium devant
    he = 30
    eau = pave(a, b, he, v, noms="abcdefgh")
    for fa in aq.faces_visibles():
        L.append(fill2([aq.p(k) for k in fa], "otSky!45"))
    for e in aq.cachees():
        L.append(seg(aq.p(e[0]), aq.p(e[1]), "cache"))
    L += cylindre(base[0], base[1], rD * s, hD * s, fond="otSky")
    L += [fill2([eau.p(k) for k in fa], "otNavy!10,fill opacity=.55") for fa in eau.faces_visibles() if fa != ("e", "f", "g", "h")]
    L.append(fill2([eau.p(k) for k in "efgh"], "otGreen!30,fill opacity=.8"))
    L.append(poly2([eau.p(k) for k in "efgh"], "vert"))
    for e, vis in aq.aretes.items():
        if vis:
            L.append(seg(aq.p(e[0]), aq.p(e[1]), "solide"))
    L.append(seg(aq.p("A"), eau.p("e"), "rep"))
    L.append(nd(lerp(aq.p("A"), eau.p("e"), 0.5), r"$30$ cm", 180, 0.1, VE))
    L += [txt((v(30, 0, 0)[0], -0.55), r"surface de l'eau (en vert) : $60 \times 30 = 1\,800$ cm²", "north", VE)]
    L += [txt(lerp(aq.p("A"), aq.p("B"), 0.5), r"$60$ cm", "north", OR, ",yshift=-1pt"),
          milieu(aq.p("B"), aq.p("C"), r"$30$ cm", -1, 0.07, OR)]
    return tikz(L)


FIGURES["e3059_enonce"] = e3059(False)
FIGURES["e3059_corrige"] = e3059(True)


# ---------------------------------------------------------------- 3041 : deux emballages
TRI_3041 = [(0, 0), (6, 0), (3, 4)]   # triangle isocèle : base 6, côtés 5, hauteur 4


def e3041(corrige):
    L = []
    s = 0.17
    v = Vue(s, (0, 0))
    pc = prisme_couche(TRI_3041, 25, v, av=["A", "B", "C"], ar=["D", "E", "F"])
    if corrige:
        L += pc.dessin(remplis={("A", "B", "C"): BASE_V}, speciaux={("B", "E"): "rep"})
        L.append(poly2([pc.p(k) for k in "ABC"], "vert"))
        L.append(milieu(pc.p("B"), pc.p("E"), r"$h = 25$ cm", -1, 0.1, VE))
    else:
        L += pc.dessin()
        L.append(milieu(pc.p("B"), pc.p("E"), r"$25$ cm", -1, 0.1, OR))
    L.append(titre((v(12.5, 0, 0)[0] + 0.35, -0.3), "Emballage A"))
    # face avant de A redessinée à part, en haut à gauche
    L += base_triangle((0.05, 1.85), TRI_3041, 0.2, r"$6$ cm", r"$4$ cm",
                       fill=BASE_V if corrige else "otSky", trait="vert" if corrige else "solide",
                       legende="une base de A" if corrige else "la face avant de A",
                       cotes_cotes=[((3, 4), (6, 0), r"$5$ cm", 1)])
    T = [(0.05 + 0.2 * x, 1.85 + 0.2 * y) for x, y in TRI_3041]
    L += codage(T[0], T[2], 1, NV) + codage(T[1], T[2], 1, NV)
    # cylindre : diamètre 5, hauteur 15
    xc, r, h = 4.75, 2.5 * s, 15 * s
    L += cyl_donnees(xc, 0, r, h, lab_d=r"$5$ cm", lab_h=(r"$h = 15$ cm" if corrige else r"$15$ cm"),
                     corrige=corrige, h_gauche=False)
    L.append(titre((xc, -0.3), "Emballage B"))
    return tikz(L)


FIGURES["e3041_enonce"] = e3041(False)
FIGURES["e3041_corrige"] = e3041(True)
