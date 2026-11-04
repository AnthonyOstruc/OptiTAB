# -*- coding: utf-8 -*-
"""Figures de la notion 93 (Terminale) : représentations paramétriques et
équations cartésiennes. Style des livres OptiTAB.

Compilation : python ../../../../outils/figures_livre.py <dossier_notion> [noms…]

Géométrie dans l'espace : perspective cavalière des livres (axe des y fuyant
vers la droite et vers le haut). Les parties cachées (arêtes, droites qui
passent sous un plan) sont calculées, pas dessinées à l'œil : chaque segment
est échantillonné et un rayon est lancé vers l'observateur ; s'il traverse
une face opaque, la portion est tracée en pointillés.
"""
import math

PREAMBULE_EXTRA = r"""
\colorlet{otNavyTint}{otNavy!7}
\tikzset{
  vu/.style={draw=otNavy,line width=0.85pt,line cap=round},
  cache/.style={draw=otNavy!60,line width=0.6pt,dash pattern=on 2.4pt off 1.8pt},
  droiteVue/.style={draw=otNavy,line width=1.1pt,line cap=round},
  droiteCachee/.style={draw=otNavy!70,line width=0.75pt,dash pattern=on 2.4pt off 1.8pt},
  repVue/.style={draw=otGreenDark,line width=1.4pt,line cap=round},
  repCachee/.style={draw=otGreenDark,line width=0.9pt,dash pattern=on 2.6pt off 1.8pt},
  planBord/.style={draw=otNavy!55,line width=0.6pt},
  planBordCache/.style={draw=otNavy!45,line width=0.5pt,dash pattern=on 2.2pt off 1.8pt},
  plan2Bord/.style={draw=otOrange!85!black,line width=0.6pt},
  plan2BordCache/.style={draw=otOrange!75!black,line width=0.5pt,dash pattern=on 2.2pt off 1.8pt},
  axeVu/.style={draw=otMuted,line width=0.55pt,-{Stealth[length=1.9mm]}},
  axeCache/.style={draw=otMuted!80,line width=0.45pt,dash pattern=on 2pt off 1.6pt},
  lab/.style={text=otInk,inner sep=1.5pt,font=\normalsize},
  labN/.style={text=otNavy,inner sep=1.5pt,font=\normalsize},
  labV/.style={text=otGreenDark,inner sep=1.5pt,font=\normalsize},
  labO/.style={text=otOrange!80!black,inner sep=1.5pt,font=\normalsize},
  labAxe/.style={text=otMuted,inner sep=1.2pt,font=\normalsize},
  legende/.style={font=\otRegular\fontsize{8.5}{10.5}\selectfont,text=otMuted,align=center,inner sep=1pt},
  vecVert/.style={draw=otGreenDark,line width=1.25pt,-{Stealth[length=2.4mm]}},
  vecNavy/.style={draw=otNavy,line width=1.05pt,-{Stealth[length=2.2mm]}},
}
"""


# ---------------------------------------------------------------- outils 3D
def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _mul(k, a):
    return (k * a[0], k * a[1], k * a[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _lerp(a, b, t):
    return _add(a, _mul(t, _sub(b, a)))


class Scene:
    """Scène 3D projetée en perspective cavalière (unités : cm après échelle)."""

    def __init__(self, kx=0.45, kz=0.36, ech=1.0):
        self.kx, self.kz, self.ech = kx, kz, ech
        self.vue = (kx, -1.0, kz)          # direction vers l'observateur
        self.ecrans = []                   # faces opaques
        self.lignes = []

    # projection
    def xy(self, p):
        x, y, z = p
        return ((x + self.kx * y) * self.ech, (self.kz * y + z) * self.ech)

    def c(self, p):
        x, y = self.xy(p)
        return f"({x:.3f},{y:.3f})"

    # faces opaques
    def opaque(self, *polys):
        for poly in polys:
            self.ecrans.append([tuple(float(v) for v in p) for p in poly])

    def _dedans(self, q, poly, n):
        signes = []
        for i in range(len(poly)):
            a, b = poly[i], poly[(i + 1) % len(poly)]
            c = _dot(_cross(_sub(b, a), _sub(q, a)), n)
            if abs(c) < 1e-9:
                return False                # sur un bord : pas « derrière »
            signes.append(c > 0)
        return all(signes) or not any(signes)

    def cache(self, p):
        for poly in self.ecrans:
            n = _cross(_sub(poly[1], poly[0]), _sub(poly[2], poly[0]))
            den = _dot(n, self.vue)
            if abs(den) < 1e-12:
                continue
            s = _dot(n, _sub(poly[0], p)) / den
            if s <= 1e-6:
                continue
            if self._dedans(_add(p, _mul(s, self.vue)), poly, n):
                return True
        return False

    # tracés
    def raw(self, s):
        self.lignes.append(s)

    def remplir(self, poly, style):
        self.raw(f"\\fill[{style}] " + " -- ".join(self.c(p) for p in poly) + " -- cycle;")

    def segment(self, a, b, vu, cache=None, n=480):
        """Segment [ab] : parties vues en style « vu », cachées en style « cache » (None : non tracées)."""
        etats = [self.cache(_lerp(a, b, i / n)) for i in range(n + 1)]
        # lissage : un échantillon isolé prend l'état de ses voisins
        for i in range(1, n):
            if etats[i - 1] == etats[i + 1] != etats[i]:
                etats[i] = etats[i - 1]
        bornes = [0.0]
        for i in range(n):
            if etats[i] != etats[i + 1]:
                lo, hi = i / n, (i + 1) / n
                for _ in range(40):
                    mid = (lo + hi) / 2
                    if self.cache(_lerp(a, b, mid)) == etats[i]:
                        lo = mid
                    else:
                        hi = mid
                bornes.append((lo + hi) / 2)
        bornes.append(1.0)
        morceaux, k = [], 0
        for j in range(len(bornes) - 1):
            t0, t1 = bornes[j], bornes[j + 1]
            etat = self.cache(_lerp(a, b, (t0 + t1) / 2))
            morceaux.append((t0, t1, etat))
        for t0, t1, etat in morceaux:
            style = cache if etat else vu
            if style is None or t1 - t0 < 1e-4:
                continue
            self.raw(f"\\draw[{style}] {self.c(_lerp(a, b, t0))} -- {self.c(_lerp(a, b, t1))};")
        return morceaux

    def polygone(self, poly, vu, cache):
        for i in range(len(poly)):
            self.segment(poly[i], poly[(i + 1) % len(poly)], vu, cache)

    def point(self, p, couleur="otNavy", r=1.7):
        self.raw(f"\\fill[{couleur}] {self.c(p)} circle ({r}pt);")

    def etiquette(self, p, texte, ancre, style="lab", decalage=""):
        opt = f"{style},anchor={ancre}" + (f",{decalage}" if decalage else "")
        self.raw(f"\\node[{opt}] at {self.c(p)} {{{texte}}};")

    def code(self, avant="", apres=""):
        return "\\begin{tikzpicture}\n" + avant + "\n".join(self.lignes) + "\n" + apres + "\\end{tikzpicture}"


# ======================================================================
#  COURS
# ======================================================================

# --------------------------------------------- I. droite et paramètre t
def fig_param_droite():
    ux, uy = 1.5, 0.6                      # vecteur u (cm)
    ax, ay = 2.3, 1.05                     # point A
    pt = lambda t: (ax + t * ux, ay + t * uy)
    L = []
    x0, y0 = pt(-1.6)
    x1, y1 = pt(2.75)
    L.append(f"\\draw[droiteVue] ({x0:.3f},{y0:.3f}) -- ({x1:.3f},{y1:.3f});")
    L.append(f"\\node[labN,anchor=south east] at ({x1:.3f},{y1:.3f}) {{$d$}};")
    # vecteur u, posé sur la droite entre t = 0 et t = 1
    xa, ya = pt(0)
    xb, yb = pt(1)
    L.append(f"\\draw[vecVert] ({xa:.3f},{ya:.3f}) -- ({xb:.3f},{yb:.3f});")
    xm, ym = pt(0.5)
    L.append(f"\\node[labV,anchor=south east] at ({xm - 0.06:.3f},{ym + 0.1:.3f}) {{$\\vec{{u}}$}};")
    for t, nom in ((-1, r"t=-1"), (0, r"t=0"), (1, r"t=1"), (2, r"t=2")):
        x, y = pt(t)
        coul = "otGreenDark" if t == 0 else "otNavy"
        L.append(f"\\fill[{coul}] ({x:.3f},{y:.3f}) circle (1.9pt);")
        L.append(f"\\node[legende,anchor=north west] at ({x + 0.04:.3f},{y - 0.12:.3f}) {{${nom}$}};")
    L.append(f"\\node[lab,anchor=south east] at ({xa - 0.05:.3f},{ya + 0.05:.3f}) {{$A$}};")
    # point M générique
    xmm, ymm = pt(2.45)
    L.append(f"\\fill[otNavy] ({xmm:.3f},{ymm:.3f}) circle (1.9pt);")
    L.append(f"\\node[lab,anchor=south east] at ({xmm - 0.05:.3f},{ymm + 0.05:.3f}) {{$M$}};")
    L.append(r"\node[legende,anchor=north west,align=left] at (-0.05,2.75) {$M \in d \iff \overrightarrow{AM} = t\,\vec{u}$\\pour un réel $t$};")
    return "\\begin{tikzpicture}\n" + "\n".join(L) + "\n\\end{tikzpicture}"


# --------------------------------------------- III. droite et plan (3 cas)
def _panneau_droite_plan(cas, dx):
    sc = Scene(kx=0.45, kz=0.36)
    W, D = 1.9, 2.3
    plan = [(0, 0, 0), (W, 0, 0), (W, D, 0), (0, D, 0)]
    sc.opaque(plan)
    sc.remplir(plan, "otNavyTint")
    sc.polygone(plan, "planBord", "planBordCache")
    if cas == "secants":
        I = (0.75, 1.55, 0)
        u = (0.22, -0.12, 1.0)
        a, b = _add(I, _mul(-1.05, u)), _add(I, _mul(1.2, u))
        sc.segment(a, b, "droiteVue", "droiteCachee")
        sc.point(I, "otGreenDark", 1.9)
        sc.etiquette(I, "$I$", "east", "labV", "xshift=-4pt,yshift=3pt")
        sc.etiquette(b, "$d$", "south", "labN")
        titre = r"sécants"
    elif cas == "paralleles":
        a, b = (-0.1, 0.6, 0.85), (1.95, 1.6, 0.85)
        sc.segment(a, b, "droiteVue", "droiteCachee")
        sc.segment((0.15, 0.72, 0), (1.7, 1.48, 0), "draw=otNavy!40,line width=0.6pt", None)
        sc.etiquette(b, "$d$", "west", "labN")
        titre = r"strictement\\parallèles"
    else:
        a, b = (0.55, 0.5, 0), (1.8, 2.1, 0)
        sc.segment(a, b, "droiteVue", "droiteCachee")
        sc.etiquette(b, "$d$", "south", "labN", "yshift=1pt")
        titre = r"$d$ incluse\\dans $\mathcal{P}$"
    # nom du plan dans un coin libre (finition 2026-11-02 : il touchait la droite)
    sc.etiquette((0, 0.9, 0), r"$\mathcal{P}$", "east", "labN", "xshift=-2.5pt")
    sc.etiquette((W / 2 + 0.45 * D / 2, 0, -0.95), titre, "north", "legende")
    return f"\\begin{{scope}}[xshift={dx}cm]\n" + "\n".join(sc.lignes) + "\n\\end{scope}"


def fig_droite_plan():
    return ("\\begin{tikzpicture}\n" + _panneau_droite_plan("secants", 0) + "\n"
            + _panneau_droite_plan("paralleles", 3.0) + "\n"
            + _panneau_droite_plan("incluse", 6.0) + "\n\\end{tikzpicture}")


# --------------------------------------------- IV. cube et droites non coplanaires
def fig_cube(nom_ab=r"$(AB)$", nom_cg=r"$(CG)$"):
    a = 2.3
    sc = Scene(kx=0.45, kz=0.36)
    S = {"A": (0, 0, 0), "B": (a, 0, 0), "C": (a, a, 0), "D": (0, a, 0),
         "E": (0, 0, a), "F": (a, 0, a), "G": (a, a, a), "H": (0, a, a)}
    faces = ["ABCD", "EFGH", "ABFE", "BCGF", "CDHG", "DAEH"]
    sc.opaque(*[[S[v] for v in f] for f in faces])
    aretes = ["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"]
    for ar in aretes:
        if ar in ("AB", "CG"):
            continue
        sc.segment(S[ar[0]], S[ar[1]], "vu", "cache")
    # droites (AB) et (CG), prolongées
    sc.segment((-0.75, 0, 0), (a + 0.95, 0, 0), "droiteVue", "droiteCachee")
    sc.segment((a, a, -0.75), (a, a, a + 0.85), "repVue", "repCachee")
    for v in "ABCDEFGH":
        sc.point(S[v], "otNavy" if v not in "CG" else "otGreenDark", 1.6)
    anc = {"A": ("north", "yshift=-1pt"), "B": ("north", "yshift=-1pt"), "C": ("west", "xshift=1pt,yshift=-4pt"),
           "D": ("south east", ""), "E": ("east", ""), "F": ("north west", "xshift=1pt"),
           "G": ("west", "xshift=1pt,yshift=4pt"), "H": ("south east", "")}
    for v, (an, dec) in anc.items():
        sc.etiquette(S[v], f"${v}$", an, "lab", dec)
    sc.etiquette((-0.75, 0, 0), nom_ab, "east", "labN")
    sc.etiquette((a, a, a + 0.85), nom_cg, "south", "labV")
    return sc.code()


# --------------------------------------------- V. deux plans sécants
def fig_deux_plans(n1=r"$\mathcal{P}_1$", n2=r"$\mathcal{P}_2$", nd=r"$\Delta$"):
    sc = Scene(kx=0.45, kz=0.36)
    X, Y = 4.3, 3.0
    x0, pente = 2.0, 0.42
    P1 = [(0, 0, 0), (X, 0, 0), (X, Y, 0), (0, Y, 0)]
    zb, zh = -1.25, 1.85
    P2 = [(x0 + pente * zb, 0, zb), (x0 + pente * zb, Y, zb), (x0 + pente * zh, Y, zh), (x0 + pente * zh, 0, zh)]
    P2bas = [P2[0], P2[1], (x0, Y, 0), (x0, 0, 0)]
    P2haut = [(x0, 0, 0), (x0, Y, 0), P2[2], P2[3]]
    sc.opaque(P1, P2)
    # remplissages dans l'ordre du peintre : bas de P2, P1, haut de P2
    sc.remplir(P2bas, "otOrange!13")
    sc.remplir(P1, "otSky")
    sc.remplir(P2haut, "otOrange!13")
    sc.polygone(P1, "planBord", "planBordCache")
    sc.polygone(P2, "plan2Bord", "plan2BordCache")
    sc.segment((x0, -0.0, 0), (x0, Y, 0), "repVue", "repCachee")
    sc.etiquette((X, 0, 0), n1, "south east", "labN", "xshift=-2pt,yshift=1pt")
    sc.etiquette(P2[2], n2, "west", "labO", "xshift=2pt")
    sc.etiquette((x0, Y, 0), nd, "west", "labV", "xshift=8pt,yshift=6pt")
    return sc.code()


# --------------------------------------------- VI. projeté orthogonal sur un plan
def fig_projete(nom_m=r"$M$", nom_plan=r"$\mathcal{P}$", nom_droite=r"$\Delta$"):
    sc = Scene(kx=0.45, kz=0.36)
    X, Y = 4.4, 2.8
    plan = [(0, 0, 0), (X, 0, 0), (X, Y, 0), (0, Y, 0)]
    sc.opaque(plan)
    sc.remplir(plan, "otSky")
    sc.polygone(plan, "planBord", "planBordCache")
    H = (2.3, 1.2, 0)
    M = (2.3, 1.2, 1.85)
    # droite passant par M dirigée par n (prolongée sous le plan)
    sc.segment((2.3, 1.2, -0.95), (2.3, 1.2, 2.55), "draw=otNavy,line width=0.7pt", "draw=otNavy!60,line width=0.55pt,dash pattern=on 2.2pt off 1.8pt")
    sc.segment(H, M, "repVue", "repCachee")
    # droite du plan passant par H et angle droit
    sc.segment((0.55, 1.2, 0), (4.05, 1.2, 0), "draw=otMuted,line width=0.55pt", None)
    q = 0.27
    sc.raw(f"\\draw[otGreenDark,line width=0.6pt] {sc.c((2.3 + q, 1.2, 0))} -- {sc.c((2.3 + q, 1.2, q))} -- {sc.c((2.3, 1.2, q))};")
    # vecteur normal n en un autre point du plan
    N0 = (0.75, 0.45, 0)
    sc.raw(f"\\draw[vecNavy] {sc.c(N0)} -- {sc.c((0.75, 0.45, 0.95))};")
    sc.etiquette((0.75, 0.45, 0.7), r"$\vec{n}$", "east", "labN", "xshift=-1pt")
    sc.point(M, "otNavy", 1.9)
    sc.point(H, "otGreenDark", 1.9)
    sc.etiquette(M, nom_m, "east", "lab", "xshift=-2pt")
    sc.etiquette(H, "$H$", "north east", "labV", "xshift=-1pt,yshift=-1pt")
    sc.etiquette((X, 0, 0), nom_plan, "south east", "labN", "xshift=-2pt,yshift=1pt")
    sc.etiquette((2.3, 1.2, 2.55), nom_droite, "west", "labN", "xshift=1pt")
    return sc.code()


# ======================================================================
#  EXERCICES
# ======================================================================

# --------------------------------------------- 983 : points d'une droite du plan
FIG_983 = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=4.8cm, height=7.56cm, xmin=-0.6, xmax=7.4, ymin=-7.2, ymax=5.4,
  xtick={1,2,3,4,5,6,7}, xticklabels={}, ytick={-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5},
  yticklabels={,$-6$,,$-4$,,$-2$,,,$2$,,$4$,}]
  \addplot[courbe, domain=0.4:6.7, samples=2] {2*x-8};
  \draw[vecVert] (axis cs:3,-2) -- (axis cs:4,0);
  \node[labV,anchor=south east] at (axis cs:3.45,-0.95) {$\vec{u}$};
  \fill[otNavy] (axis cs:3,-2) circle (2pt);
  \fill[otNavy] (axis cs:5,2) circle (2pt);
  \fill[otGreenDark] (axis cs:1,-6) circle (2.1pt);
  \fill[otGreenDark] (axis cs:6,4) circle (2.1pt);
  \node[lab,anchor=north west] at (axis cs:3.1,-2.15) {$A$};
  \node[legende,anchor=north west] at (axis cs:3.75,-2.3) {$t=0$};
  \node[lab,anchor=north west] at (axis cs:5.1,1.85) {$B$};
  \node[legende,anchor=north west] at (axis cs:5.75,1.7) {$t=2$};
  \node[labV,anchor=north west] at (axis cs:1.12,-6.15) {$(1\,;-6)$};
  \node[legende,anchor=north west] at (axis cs:1.2,-6.95) {$t=-2$};
  \node[labV,anchor=north west] at (axis cs:6.12,3.85) {$(6\,;4)$};
  \node[legende,anchor=north west] at (axis cs:6.2,3.05) {$t=3$};
  \node[labN,anchor=south east] at (axis cs:6.55,4.7) {$(d)$};
\end{axis}
\end{tikzpicture}"""

# --------------------------------------------- 985 : distance de deux droites parallèles
FIG_985 = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=4.2cm, height=5.88cm, xmin=-1.7, xmax=4.3, ymin=-2.7, ymax=5.7,
  xtick={1,2,3}, xticklabels={$1$,$2$,$3$}, ytick={1,2,3,4}, yticklabels={$1$,$2$,$3$,$4$}]
  \addplot[courbe, domain=-0.3:3.6, samples=2] {-2*x+5};
  \addplot[courbe2, domain=-1.55:1.3, samples=2] {-2*x};
  \draw[otGreenDark,line width=1.4pt] (axis cs:0,0) -- (axis cs:2,1);
  \draw[otGreenDark,line width=0.6pt] (axis cs:1.6522,0.8261) -- (axis cs:1.8261,0.4783) -- (axis cs:2.1739,0.6522);
  \fill[otNavy] (axis cs:0,0) circle (2pt);
  \fill[otGreenDark] (axis cs:2,1) circle (2.1pt);
  \node[lab,anchor=north east] at (axis cs:-0.05,-0.1) {$O$};
  \node[labV,anchor=south west] at (axis cs:2.08,1.1) {$H$};
  \node[labV,anchor=south east] at (axis cs:0.85,0.55) {$\sqrt{5}$};
  \node[labN,anchor=south west] at (axis cs:3.1,0.2) {$(d)$};
  \node[labV,anchor=north east] at (axis cs:1.25,-2.55) {$(d')$};
\end{axis}
\end{tikzpicture}"""


# --------------------------------------------- 1110 : pyramide SABCD
def _pyramide(section=False, axes=True):
    sc = Scene(kx=0.5, kz=0.4, ech=1.25)
    A, B, C, D, S = (0, 0, 0), (3, 0, 0), (3, 2, 0), (0, 2, 0), (1, 1, 3)
    faces = [[A, B, C, D], [S, A, B], [S, B, C], [S, C, D], [S, D, A]]
    sc.opaque(*faces)
    P = (0.75, 1.25, 2.25)
    Q = (0.75, 0.75, 2.25)
    if section:
        sc.remplir([B, C, P, Q], "otGreen!22")
    if axes:
        sc.segment(B, (3.85, 0, 0), "axeVu", "axeCache")
        sc.segment(D, (0, 3.0, 0), "axeVu", "axeCache")
        sc.segment(A, (0, 0, 3.55), "axeVu", "axeCache")
        sc.etiquette((3.85, 0, 0), "$x$", "west", "labAxe")
        sc.etiquette((0, 3.0, 0), "$y$", "west", "labAxe")
        sc.etiquette((0, 0, 3.55), "$z$", "east", "labAxe")
    for a, b in ((A, B), (B, C), (C, D), (D, A), (S, A), (S, B), (S, C), (S, D)):
        sc.segment(a, b, "vu", "cache")
    if section:
        sc.segment(B, Q, "repVue", "repCachee")
        sc.segment(Q, P, "repVue", "repCachee")
        sc.segment(P, C, "repVue", "repCachee")
    for p in (A, B, C, D, S):
        sc.point(p, "otNavy", 1.7)
    sc.etiquette(A, "$A$", "north east", "lab", "xshift=1pt")
    sc.etiquette(B, "$B$", "north", "lab", "yshift=-1pt")
    sc.etiquette(C, "$C$", "west", "lab", "xshift=1pt,yshift=-3pt")
    sc.etiquette(D, "$D$", "south east", "lab", "xshift=1pt,yshift=-1pt")
    sc.etiquette(S, "$S$", "south", "lab", "yshift=1pt")
    if section:
        sc.point(P, "otGreenDark", 1.9)
        sc.point(Q, "otGreenDark", 1.9)
        sc.etiquette(P, "$P$", "south west", "labV", "xshift=2pt")
        sc.etiquette(Q, "$Q$", "east", "labV", "xshift=-2pt")
    return sc.code()


FIGURES = {
    # cours
    "cours_param_droite": fig_param_droite(),
    "cours_droite_plan": fig_droite_plan(),
    "cours_cube_non_coplanaires": fig_cube(),
    "cours_deux_plans": fig_deux_plans(),
    "cours_projete_plan": fig_projete(),
    # exercices
    "ex983_points": FIG_983,
    "ex985_distance": FIG_985,
    "ex988_projete": fig_projete(nom_m=r"$A$", nom_plan=r"$\mathcal{P}$", nom_droite=r"$\Delta$"),
    "ex990_deux_plans": fig_deux_plans(nd=r"$(d)$"),
    "ex1110_pyramide": _pyramide(section=False, axes=False),
    "ex1110_section": _pyramide(section=True, axes=False),
    "ex1110_projete": fig_projete(nom_m=r"$S$", nom_plan=r"$(PBC)$", nom_droite=r"$\Delta$"),
}
FIGURES.pop("ex985_distance")      # exercice 985 réécrit dans l'espace (finition 2026-11-02)

# ======================================================================
#  FINITION 2026-11-02 — outil commun espace.py
#  (parties cachées calculées, étiquettes placées hors des traits)
# ======================================================================
import espace as es  # noqa: E402

PREAMBULE_EXTRA += es.STYLES


def plan_horizontal(f, X, Y, nom=r"$\mathcal{P}$", z=0.0, style="ePlanB", bord="eBordB", sty_nom="eLblN", coin="avant"):
    cadre = [(0, 0, z), (X, 0, z), (X, Y, z), (0, Y, z)]
    es.plan(f, cadre, style=style, bord=bord)
    if nom:
        if coin == "avant":
            f.texte((X - 0.15, 0.12, z), nom, style=sty_nom, anchor="south east", n=1)
        elif coin == "gauche":
            f.texte((0.18, 0.1, z), nom, style=sty_nom, anchor="south west", n=1)
        else:
            f.texte((X - 0.12, Y - 0.1, z), nom, style=sty_nom, anchor="north east", n=1)
    return cadre


# --------------------------------------------- cours II : plan et vecteur normal
f = es.Fig(1.0)
plan_horizontal(f, 5.0, 3.0)
A, M, N = (1.5, 1.0, 0), (3.6, 1.9, 0), (1.5, 1.0, 1.8)
f.vec(A, M); f.vec(A, N, "eVecV")
f.angle_droit(A, M, N, 0.3, "eAngleV")
f.point(A); f.point(M)
f.label(A, "$A$", pref=200); f.label(M, "$M$", pref=-20)
f.label(N, r"$\vec{n}$", h=0.5, style="eLblV", pref=90)
FIGURES["cours_plan_normal"] = f.tikz()


# --------------------------------------------- 984 : points d'une droite, paramètre t
def droite_param(points, hors=None, s=1.0):
    f = es.Fig(s)
    A = (0.6, 0.5)
    u = (1.3, 0.55)
    P = lambda t: (A[0] + t * u[0], A[1] + t * u[1])
    f.ligne([P(-0.45), P(2.6)], "eDroite")
    f.vec(P(0), P(1), "eVecV")
    f.label(P(0.5), r"$\vec{u}$", h=0.5, style="eLblV", pref=110, r=0.06)
    for t, nom, txt, st in points:
        f.point(P(t), st)
        f.label(P(t), nom, n=len(nom) // 3 + 1, pref=110)
        f.label(P(t), txt, n=len(txt) // 2, style="eNote", h=0.36, pref=-70)
    if hors:
        q = (P(1.55)[0] - 0.25, P(1.55)[1] + 1.0)
        f.point(q, "ptO")
        f.label(q, hors, n=7, style="eLblO", pref=90)
    f.label(P(2.6), "$(d)$", n=3, style="eLblN", pref=30)
    return f.tikz()


FIGURES["n984_droite"] = droite_param([(0, "$A$", "$t=0$", "ptN"), (1, "$B$", "$t=1$", "ptN"),
                                       (2, r"$(5\,;0\,;5)$", "$t=2$", "ptV")], hors=r"$C(0\,;3\,;-7)$")

# --------------------------------------------- 986 : vecteur normal et vecteurs directeurs ; plans parallèles
f = es.Fig(1.0)
plan_horizontal(f, 5.2, 3.2)
A = (1.6, 1.0, 0)
u1, u2, n = (0.75, 1.6, 0), (2.0, 0.9, 0), (0, 0, 1.75)
f.vec(A, es.add(A, u1), "eVecV"); f.vec(A, es.add(A, u2), "eVecV")
f.vec(A, es.add(A, n))
f.angle_droit(A, es.add(A, u1), es.add(A, n), 0.28)
f.angle_droit(A, es.add(A, u2), es.add(A, n), 0.28)
f.point(A); f.label(A, "$A$", pref=200)
f.label(es.add(A, n), r"$\vec{n}$", h=0.5, pref=90)
f.label(es.add(A, u1), r"$\vec{u}_1$", n=2, h=0.5, style="eLblV", pref=90)
f.label(es.add(A, u2), r"$\vec{u}_2$", n=2, h=0.5, style="eLblV", pref=0)
FIGURES["n986_directeurs"] = f.tikz()

f = es.Fig(0.95)
X, Y = 5.0, 2.6
haut = [(0, 0, 1.9), (X, 0, 1.9), (X, Y, 1.9), (0, Y, 1.9)]
bas = [(0, 0, 0), (X, 0, 0), (X, Y, 0), (0, Y, 0)]
f.opaque(haut)
f.fill(bas, "ePlanV"); f.ligne(bas, "eBordV", ferme=True)
f.fill(haut, "ePlanB"); f.ligne(haut, "eBordB", ferme=True)
O_, A_ = (1.4, 1.1, 0), (3.3, 1.4, 1.9)
f.vec(O_, es.add(O_, (0, 0, 1.0)))
f.vec(A_, es.add(A_, (0, 0, 1.0)))
f.point(O_, "ptV"); f.point(A_)
f.label(O_, "$O$", style="eLblV", pref=200); f.label(A_, "$A$", pref=200)
f.label((1.4, 1.1, 1.0), r"$\vec{n}$", h=0.5, pref=180, r=0.05)
f.label(es.add(A_, (0, 0, 1.0)), r"$\vec{n}$", h=0.5, pref=0, r=0.05)
f.texte((X - 0.15, 0.12, 1.9), r"$\mathcal{P}$", style="eLblN", anchor="south east")
f.texte((X - 0.15, 0.12, 0), r"$\mathcal{P}'$", style="eLblV", anchor="south east", n=2)
FIGURES["n986_paralleles"] = f.tikz()

# --------------------------------------------- 989 : deux droites sécantes en I, angle des vecteurs directeurs
f = es.Fig(1.0)
cadre = [(0, 0), (5.6, 0), (6.8, 2.9), (1.2, 2.9)]
f.fill(cadre, "ePlanB"); f.ligne(cadre, "eBordB", ferme=True)
I = (3.0, 1.35)
d1 = (1.0, 0.62); d2 = (1.0, 0.12)
f.ligne([es.add(I, es.mul(-2.4, d2)), es.add(I, es.mul(2.9, d2))], "eDroite")
f.ligne([es.add(I, es.mul(-2.0, d1)), es.add(I, es.mul(2.15, d1))], "eDroite")
f.vec(I, es.add(I, es.mul(1.15, d1)), "eVecV"); f.vec(I, es.add(I, es.mul(1.3, d2)), "eVecV")
pa = f.arc(I, es.add(I, d2), es.add(I, d1), 0.75)
f.point(I, "ptV"); f.label(I, "$I$", style="eLblV", pref=290, r=0.08, dirs=range(250, 331, 10))
f.label(pa, r"$\theta$", style="eLblV", pref=0, r=0.06)
f.label(es.add(I, es.mul(1.15, d1)), r"$\vec{u}_1$", n=2, h=0.5, style="eLblV", pref=110)
f.label(es.add(I, es.mul(1.3, d2)), r"$\vec{u}_2$", n=2, h=0.5, style="eLblV", pref=-70)
f.label(es.add(I, es.mul(2.15, d1)), "$(d_1)$", n=4, style="eLblN", pref=30)
f.label(es.add(I, es.mul(2.9, d2)), "$(d_2)$", n=4, style="eLblN", pref=-20)
FIGURES["n989_secantes"] = f.tikz()

# --------------------------------------------- 1109 : d1 // d4 dans un plan Q ; d3 coupe d1 en E ; d2 coupe d4 en G
f = es.Fig(1.0)
X, Y = 5.6, 3.2
plan_horizontal(f, X, Y, nom=r"$\mathcal{Q}$", style="ePlanV", bord="eBordV", sty_nom="eLblV", coin="gauche")
dirp = (1.0, 0.2, 0)
P1, P4 = (0.75, 0.75, 0), (0.45, 2.15, 0)
f.ligne([P1, es.add(P1, es.mul(5.0, dirp))], "eDroite")
f.ligne([P4, es.add(P4, es.mul(5.0, dirp))], "eDroite")
E_ = es.add(P1, es.mul(1.7, dirp)); G_ = es.add(P4, es.mul(3.6, dirp))
w3 = (0.35, -0.25, 1.0); v2 = (-0.3, 0.25, 1.0)
f.seg(es.add(E_, es.mul(-0.9, w3)), es.add(E_, es.mul(1.45, w3)), "eDroiteO", "eDroiteOC")
f.seg(es.add(G_, es.mul(-1.0, v2)), es.add(G_, es.mul(1.4, v2)), "eDroiteO", "eDroiteOC")
f.point(E_, "ptV"); f.point(G_, "ptV")
f.label(E_, "$E$", style="eLblV", pref=-60); f.label(G_, "$G$", style="eLblV", pref=-30)
f.label(es.add(P1, es.mul(5.0, dirp)), "$d_1$", n=2, style="eLblN", pref=0)
f.label(es.add(P4, es.mul(5.0, dirp)), "$d_4$", n=2, style="eLblN", pref=0)
f.label(es.add(E_, es.mul(1.45, w3)), "$d_3$", n=2, style="eLblO", pref=90)
f.label(es.add(G_, es.mul(1.4, v2)), "$d_2$", n=2, style="eLblO", pref=90)
FIGURES["n1109_bilan"] = f.tikz()

# --------------------------------------------- 992 : plan (ABC), D hors du plan, d sécante en I
f = es.Fig(1.0)
X, Y = 5.6, 3.3
cadre = plan_horizontal(f, X, Y, nom=None)
A, B, C = (0.9, 0.7, 0), (3.6, 0.5, 0), (2.1, 2.5, 0)
f.fill([A, B, C], "ePlanV")
f.ligne([A, B, C], "eArete", ferme=True)
Dd = (4.4, 2.3, 1.25)
f.ligne([Dd, (4.4, 2.3, 0)], "eGuide")
I = (4.2, 1.3, 0)
w = (-0.3, 0.3, 1.0)
f.seg(es.add(I, es.mul(-0.95, w)), es.add(I, es.mul(1.6, w)), "eDroiteV", "eDroiteVC")
for q, nom in ((A, "A"), (B, "B"), (C, "C")):
    f.point(q); f.label(q, f"${nom}$")
f.point(Dd, "ptO"); f.label(Dd, "$D$", style="eLblO", pref=0)
f.point((4.4, 2.3, 0), "ptM")
f.point(I, "ptV"); f.label(I, "$I$", style="eLblV", pref=-20)
f.label(es.add(I, es.mul(1.6, w)), "$(d)$", n=3, style="eLblV", pref=90)
f.label((X, Y, 0), "$(ABC)$", n=4, style="eLblN", pref=0)
FIGURES["n992_bilan"] = f.tikz()

# --------------------------------------------- 988, Q3 : la droite d perce le plan P en I
f = es.Fig(1.0)
plan_horizontal(f, 5.0, 3.0)
I = (2.6, 1.4, 0)
w = (-0.45, 0.25, 1.0)
A = es.add(I, es.mul(1.15, w))
f.seg(es.add(I, es.mul(-0.95, w)), es.add(I, es.mul(1.75, w)), "eDroite", "eDroiteC")
f.vec(A, es.add(A, es.mul(-0.55, w)), "eVec")
f.point(A); f.point(I, "ptV")
f.label(A, "$A$", pref=0)
f.label(es.add(A, es.mul(-0.3, w)), r"$\vec{u}$", h=0.5, pref=0, r=0.08)
f.label(I, "$I$", style="eLblV", pref=-20)
f.label(es.add(I, es.mul(1.75, w)), "$(d)$", n=3, style="eLblN", pref=90)
FIGURES["n988_intersection"] = f.tikz()


# --------------------------------------------- 985 : même droite (d = d') ; droite parallèle Δ
def fig_985(avec_delta):
    f = es.Fig(1.0)
    A = (0.6, 0.6)
    u = (1.05, 0.42)
    P = lambda t, o=A: (o[0] + t * u[0], o[1] + t * u[1])
    f.ligne([P(-0.5), P(3.1)], "eDroite")
    f.label(P(3.1), "$d$", style="eLblN", pref=20)
    f.vec(P(0), P(1), "eVecV")
    if not avec_delta:
        f.label(P(0.5), r"$\vec{u}$", h=0.5, style="eLblV", pref=-70, r=0.05)
        f.point(P(0)); f.label(P(0), "$A$", pref=-110)
        nrm = (-0.42 / 1.13, 1.05 / 1.13)
        dec = lambda q, k: (q[0] + k * nrm[0], q[1] + k * nrm[1])
        f.vec(dec(P(2), 0.38), dec(P(0), 0.38), "eVecO")
        f.label(dec(P(1), 0.38), r"$\vec{u}\,' = -2\vec{u}$", n=8, h=0.5, style="eLblO", pref=110, r=0.4)
        f.point(P(2), "ptV"); f.label(P(2), "$A'$", n=2, style="eLblV", pref=-60)
    else:
        f.label(P(0.5), r"$\vec{u}$", h=0.5, style="eLblV", pref=120, r=0.05)
        f.point(P(0)); f.label(P(0), "$A$", pref=110)
        E = (P(0)[0] - 0.35, P(0)[1] + 1.45)
        f.ligne([P(-0.3, E), P(3.0, E)], "eDroiteV")
        f.label(P(3.0, E), r"$\Delta$", style="eLblV", pref=20)
        f.vec(E, P(1, E), "eVecV")
        f.label(P(0.5, E), r"$\vec{u}$", h=0.5, style="eLblV", pref=120, r=0.05)
        f.point(E, "ptV"); f.label(E, "$E$", style="eLblV", pref=110)
    return f.tikz()


FIGURES["n985_confondues"] = fig_985(False)
FIGURES["n985_paralleles"] = fig_985(True)
