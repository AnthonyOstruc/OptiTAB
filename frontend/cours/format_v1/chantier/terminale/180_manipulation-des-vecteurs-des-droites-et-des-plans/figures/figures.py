# -*- coding: utf-8 -*-
"""Figures de la notion 180 « Vecteurs, droites et plans de l'espace ».

Perspective cavalière des livres OptiTAB (style otEspace : x vers la droite,
y en profondeur (0,42 ; 0,34), z vers le haut), arêtes cachées en pointillés.
Les étiquettes sont placées automatiquement dans l'espace libre : pour chaque
étiquette, on teste 36 directions autour du point et on garde celle qui laisse
le plus de marge avec tous les traits, points et autres étiquettes.

Compilation : python ../../../../outils/figures_livre.py <dossier_notion>
"""
import math

import numpy as np

UX, UY, UZ = (1.0, 0.0), (0.42, 0.34), (0.0, 1.0)

PREAMBULE_EXTRA = r"""
\tikzset{
  arete/.style={otNavy,line width=0.85pt,line join=round,line cap=round},
  cachee/.style={otNavy!60,line width=0.7pt,dash pattern=on 3pt off 2pt},
  areteL/.style={otNavy!45,line width=0.7pt,line join=round,line cap=round},
  cacheeL/.style={otNavy!35,line width=0.6pt,dash pattern=on 3pt off 2pt},
  vecN/.style={otNavy,line width=1.35pt,-{Stealth[length=2.7mm,width=2.1mm]}},
  vecNC/.style={otNavy,line width=1.2pt,dash pattern=on 3.5pt off 2pt,-{Stealth[length=2.7mm,width=2.1mm]}},
  vecV/.style={otGreenDark,line width=1.45pt,-{Stealth[length=2.8mm,width=2.2mm]}},
  vecO/.style={otOrange,line width=1.45pt,-{Stealth[length=2.8mm,width=2.2mm]}},
  droiteN/.style={otNavy,line width=1.3pt},
  droiteV/.style={otGreenDark,line width=1.3pt},
  droiteO/.style={otOrange,line width=1.3pt},
  droiteNC/.style={otNavy,line width=1.1pt,dash pattern=on 3pt off 2pt},
  droiteVC/.style={otGreenDark,line width=1.1pt,dash pattern=on 3pt off 2pt},
  droiteOC/.style={otOrange,line width=1.1pt,dash pattern=on 3pt off 2pt},
  constr/.style={otOrange,line width=0.8pt},
  constrC/.style={otOrange,line width=0.75pt,dash pattern=on 3pt off 2pt},
  rep/.style={otGreenDark,line width=1.25pt,line join=round},
  repC/.style={otGreenDark,line width=1.05pt,dash pattern=on 3pt off 2pt},
  guideF/.style={otMuted,line width=0.6pt,dash pattern=on 2.5pt off 1.8pt},
  axe/.style={otMuted,line width=0.7pt,-{Stealth[length=2.3mm]}},
  ptN/.style={circle,fill=otNavy,inner sep=0pt,minimum size=4.2pt},
  ptV/.style={circle,fill=otGreenDark,inner sep=0pt,minimum size=4.6pt},
  ptO/.style={circle,fill=otOrange!90!black,inner sep=0pt,minimum size=4.6pt},
  lbl/.style={inner sep=1pt,text=otInk,font=\normalsize},
  lblV/.style={inner sep=1pt,text=otGreenDark,font=\normalsize},
  lblN/.style={inner sep=1pt,text=otNavy,font=\normalsize},
  lblO/.style={inner sep=1pt,text=otOrange!80!black,font=\normalsize},
  lblM/.style={inner sep=1pt,text=otMuted,font=\normalsize},
  planB/.style={fill=otSky},
  planV/.style={fill=otGreen!17},
  planO/.style={fill=otOrange!14},
  bordB/.style={otNavy!45,line width=0.55pt},
  bordV/.style={otGreenDark!55,line width=0.55pt},
  section/.style={fill=otGreen!24},
}
"""


def f2(v):
    return f"{v:.3f}".rstrip("0").rstrip(".") if abs(v) > 1e-9 else "0"


class Fig:
    """Une figure : traits, remplissages, points, étiquettes placées automatiquement."""

    def __init__(self, s=3.4, uy=None):
        self.s = s
        self.uy = uy or UY
        self.fonds, self.traits, self.dessus = [], [], []
        self.echant = []          # échantillons des traits (pour les marges)
        self.points = []          # (x, y)
        self.etiq = []            # demandes d'étiquettes
        self.boites = []          # boîtes déjà placées

    # ------------------------------------------------------------ projection
    def p(self, q):
        if len(q) == 2:
            return (q[0], q[1])
        x, y, z = q
        s = self.s
        return (s * (x * UX[0] + y * self.uy[0] + z * UZ[0]), s * (x * UX[1] + y * self.uy[1] + z * UZ[1]))

    def c(self, q):
        x, y = self.p(q)
        return f"({f2(x)},{f2(y)})"

    def _echantillonne(self, a, b):
        (x1, y1), (x2, y2) = self.p(a), self.p(b)
        n = max(2, int(math.hypot(x2 - x1, y2 - y1) / 0.03) + 1)
        for k in range(n):
            t = k / (n - 1)
            self.echant.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))

    # ------------------------------------------------------------ dessin
    def fill(self, pts, style):
        self.fonds.append(f"\\fill[{style}] " + " -- ".join(self.c(q) for q in pts) + " -- cycle;")

    def ligne(self, pts, style, ferme=False, dessus=False):
        chemin = " -- ".join(self.c(q) for q in pts) + (" -- cycle" if ferme else "")
        (self.dessus if dessus else self.traits).append(f"\\draw[{style}] {chemin};")
        suite = list(pts) + ([pts[0]] if ferme else [])
        for a, b in zip(suite, suite[1:]):
            self._echantillonne(a, b)

    def vec(self, a, b, style="vecN"):
        self.dessus.append(f"\\draw[{style}] {self.c(a)} -- {self.c(b)};")
        self._echantillonne(a, b)

    def point(self, q, style="ptN"):
        coul = {"ptN": "otNavy", "ptV": "otGreenDark", "ptO": "otOrange!90!black"}[style]
        self.dessus.append(f"\\fill[{coul}] {self.c(q)} circle (2.3pt);")
        self.points.append(self.p(q))

    def label(self, q, texte, n=1, style="lbl", pref=None, r=0.08, h=0.42, w=None, dirs=None):
        """Étiquette près de q (n ≈ nombre de caractères visibles), placée dans l'espace libre."""
        self.etiq.append((self.p(q), texte, w if w else 0.14 + 0.21 * n, h, style, pref, r, dirs))

    def texte(self, q, texte, style="lbl", anchor="center", n=1, h=0.42, w=None):
        """Texte à une place fixe (légende, nom de plan…)."""
        x, y = self.p(q)
        self.dessus.append(f"\\node[{style},anchor={anchor}] at ({f2(x)},{f2(y)}) {{{texte}}};")
        ww = w if w else 0.14 + 0.21 * n
        dx = {"center": 0, "west": ww / 2, "east": -ww / 2}.get(anchor.split()[-1] if anchor != "center" else "center", 0)
        dy = 0
        if "north" in anchor:
            dy = -h / 2
        if "south" in anchor:
            dy = h / 2
        if anchor in ("north", "south"):
            dx = 0
        cx, cy = x + dx, y + dy
        self.boites.append((cx - ww / 2, cy - h / 2, cx + ww / 2, cy + h / 2))

    # ------------------------------------------------------------ placement
    def _place(self):
        E = np.array(self.echant) if self.echant else np.zeros((0, 2))
        P = np.array(self.points) if self.points else np.zeros((0, 2))
        allx = [x for x, _ in self.echant] + [x for x, _ in self.points]
        ally = [y for _, y in self.echant] + [y for _, y in self.points]
        cx, cy = (np.mean(allx), np.mean(ally)) if allx else (0, 0)
        sortie = []
        for (x, y), texte, w, h, style, pref, r, dirs in self.etiq:
            P = np.array([q for q in self.points if math.hypot(q[0] - x, q[1] - y) > 1e-6]) if self.points else np.zeros((0, 2))
            if P.size == 0:
                P = np.zeros((0, 2))
            if pref is None:
                pref = math.degrees(math.atan2(y - cy, x - cx))
            meilleur = None
            angles = dirs if dirs is not None else range(0, 360, 10)
            for th in angles:
                t = math.radians(th)
                ux, uy = math.cos(t), math.sin(t)
                ax, ay = x + r * ux, y + r * uy
                k = min((w / 2) / abs(ux) if abs(ux) > 1e-9 else 1e9, (h / 2) / abs(uy) if abs(uy) > 1e-9 else 1e9)
                bx, by = ax + k * ux, ay + k * uy
                x0, y0, x1, y1 = bx - w / 2, by - h / 2, bx + w / 2, by + h / 2
                d = 9.0
                if len(E):
                    dx = np.maximum(np.maximum(x0 - E[:, 0], 0), E[:, 0] - x1)
                    dy = np.maximum(np.maximum(y0 - E[:, 1], 0), E[:, 1] - y1)
                    d = min(d, float(np.min(np.hypot(dx, dy))))
                if len(P):
                    dx = np.maximum(np.maximum(x0 - P[:, 0], 0), P[:, 0] - x1)
                    dy = np.maximum(np.maximum(y0 - P[:, 1], 0), P[:, 1] - y1)
                    dd = np.hypot(dx, dy)
                    d = min(d, float(np.min(dd)) - 0.05 if np.min(dd) > 0 else -1)
                for (a0, b0, a1, b1) in self.boites:
                    ex = max(a0 - x1, 0, x0 - a1)
                    ey = max(b0 - y1, 0, y0 - b1)
                    d = min(d, math.hypot(ex, ey) - 0.04)
                score = min(d, 0.16) + 0.03 * math.cos(t - math.radians(pref))
                if meilleur is None or score > meilleur[0]:
                    meilleur = (score, th, ax, ay, (x0, y0, x1, y1))
            _, th, ax, ay, boite = meilleur
            self.boites.append(boite)
            sortie.append(f"\\node[{style},anchor={(th + 180) % 360}] at ({f2(ax)},{f2(ay)}) {{{texte}}};")
        return sortie

    def tikz(self):
        corps = self.fonds + self.traits + self.dessus + self._place()
        return "\\begin{tikzpicture}\n" + "\n".join(corps) + "\n\\end{tikzpicture}"


# ---------------------------------------------------------------- cube / pavé
def sommets(L=1, W=1, H=1):
    return {"A": (0, 0, 0), "B": (L, 0, 0), "C": (L, W, 0), "D": (0, W, 0),
            "E": (0, 0, H), "F": (L, 0, H), "G": (L, W, H), "H": (0, W, H)}


VISIBLES = ["AB", "BC", "CG", "GH", "HE", "EA", "BF", "FE", "FG"]
CACHEES = ["AD", "DC", "DH"]


def cube(f, S, leger=False, sauf=(), noms=True, pref=None):
    for a, b in VISIBLES:
        if a + b not in sauf:
            f.ligne([S[a], S[b]], "areteL" if leger else "arete")
    for a, b in CACHEES:
        if a + b not in sauf:
            f.ligne([S[a], S[b]], "cacheeL" if leger else "cachee")
    if noms:
        centre = tuple(sum(S[k][i] for k in S) / 8 for i in range(3))
        cx, cy = f.p(centre)
        for k in "ABCDEFGH":
            x, y = f.p(S[k])
            pr = (pref or {}).get(k, math.degrees(math.atan2(y - cy, x - cx)))
            f.label(S[k], f"${k}$", pref=pr)


def mil(a, b, t=0.5):
    return tuple(a[i] + t * (b[i] - a[i]) for i in range(len(a)))


def ext(a, b, t0, t1):
    """Points a + t0 (b - a) et a + t1 (b - a) (prolongement d'une droite)."""
    return mil(a, b, t0), mil(a, b, t1)


S = sommets()
FIGURES = {}

# ================================================================ COURS
# I. Relation de Chasles dans le cube (sert aussi à l'exercice 1097, Q2)
f = Fig(3.5)
cube(f, S, leger=True)
f.vec(S["A"], S["B"]); f.vec(S["B"], S["C"]); f.vec(S["C"], S["G"])
f.vec(S["A"], S["G"], "vecV")
FIGURES["cube_chasles"] = f.tikz()

# II. Plan défini par A, u, v : AM = 2u + 1,5v
f = Fig()
cadre = [(0, 0), (6.1, 0), (7.5, 2.55), (1.4, 2.55)]
f.fill(cadre, "planB"); f.ligne(cadre, "bordB", ferme=True)
A = (1.15, 0.55); u = (1.2, 0); v = (0.5, 0.6)
U = (A[0] + u[0], A[1] + u[1]); Vv = (A[0] + v[0], A[1] + v[1])
U2 = (A[0] + 2 * u[0], A[1]); V15 = (A[0] + 1.5 * v[0], A[1] + 1.5 * v[1])
M = (U2[0] + 1.5 * v[0], U2[1] + 1.5 * v[1])
f.ligne([U, U2], "guideF"); f.ligne([Vv, V15], "guideF")
f.ligne([U2, M], "guideF"); f.ligne([V15, M], "guideF")
f.vec(A, U); f.vec(A, Vv)
f.vec(A, M, "vecV")
f.point(A); f.point(M, "ptV"); f.point(U2, "ptN"); f.point(V15, "ptN")
f.label(A, "$A$", pref=200); f.label(M, "$M$", style="lblV", pref=30)
f.label(((A[0] + U[0]) / 2, A[1]), r"$\vec{u}$", h=0.5, pref=-90, r=0.04)
f.label(((A[0] + Vv[0]) / 2, (A[1] + Vv[1]) / 2), r"$\vec{v}$", h=0.5, pref=150, r=0.04)
f.label(U2, r"$2\vec{u}$", n=2, h=0.5, style="lblM", pref=-60)
f.label(V15, r"$1{,}5\,\vec{v}$", n=4, h=0.5, style="lblM", pref=150)
f.texte((6.6, 0.35), r"$\mathcal{P}$", style="lblN")
FIGURES["plan_point_vecteurs"] = f.tikz()

# II. Vecteurs coplanaires dans le cube : EF, EH, EG dans (EFG) ; EA hors du plan
f = Fig(3.5)
f.fill([S["E"], S["F"], S["G"], S["H"]], "planV")
cube(f, S, leger=True, pref={"F": 250})
f.vec(S["E"], S["F"]); f.vec(S["E"], S["H"]); f.vec(S["E"], S["G"], "vecV"); f.vec(S["E"], S["A"], "vecO")
FIGURES["cube_coplanaires"] = f.tikz()

# III. Repère de l'espace et coordonnées de M(2 ; 3 ; 2)
def R(x, y, z, s=1.3):
    """Repère « classique » : x vers l'observateur, y vers la droite, z vers le haut."""
    return (s * (-0.5 * x + y), s * (-0.4 * x + z))


f = Fig()
O = R(0, 0, 0)
f.ligne([R(-0.5, 0, 0), R(3.2, 0, 0)], "axe"); f.ligne([R(0, -0.5, 0), R(0, 4.4, 0)], "axe"); f.ligne([R(0, 0, -0.5), R(0, 0, 3.0)], "axe")
X2, Y3, Z2, Mp, Mm, YZ = R(2, 0, 0), R(0, 3, 0), R(0, 0, 2), R(2, 3, 0), R(2, 3, 2), R(0, 3, 2)
for a, b in ((X2, Mp), (Y3, Mp), (Mp, Mm), (Z2, YZ), (YZ, Mm), (Y3, YZ)):
    f.ligne([a, b], "guideF")
f.vec(O, R(1, 0, 0)); f.vec(O, R(0, 1, 0)); f.vec(O, R(0, 0, 1))
f.vec(O, Mm, "vecV")
for q in (X2, Y3, Z2):
    f.point(q, "ptN")
f.point(Mm, "ptV")
f.label(O, "$O$", pref=150)
f.label(R(0.6, 0, 0), r"$\vec{\imath}$", h=0.5, pref=-51, r=0.12, dirs=[-60, -51, -40, -30])
f.label(R(0, 0.5, 0), r"$\vec{\jmath}$", h=0.55, pref=-90, r=0.03)
f.label(R(0, 0, 0.5), r"$\vec{k}$", h=0.5, pref=180, r=0.03)
f.label(X2, "$2$", style="lblM", pref=0); f.label(Y3, "$3$", style="lblM", pref=-90); f.label(Z2, "$2$", style="lblM", pref=180)
f.label(Mm, "$M$", style="lblV", pref=45)
f.label(R(3.2, 0, 0), "$x$", style="lblM", pref=225); f.label(R(0, 4.4, 0), "$y$", style="lblM", pref=0); f.label(R(0, 0, 3.0), "$z$", style="lblM", pref=90)
FIGURES["repere_espace"] = f.tikz()

# IV.1 Deux droites dans un cube : (AB) // (HG) ; (AB), (CG) non coplanaires
f = Fig(3.3)
cube(f, S, leger=True)
f.ligne(list(ext(S["A"], S["B"], -0.28, 1.28)), "droiteN", dessus=True)
f.ligne(list(ext(S["H"], S["G"], -0.28, 1.28)), "droiteV", dessus=True)
f.ligne(list(ext(S["C"], S["G"], -0.3, 1.3)), "droiteO", dessus=True)
FIGURES["cube_deux_droites"] = f.tikz()

# IV.2 Droite et plan : trois cas
f = Fig()
def plan2d(f, dx, style="planB", bord="bordB"):
    pts = [(dx, 0), (dx + 2.1, 0), (dx + 2.85, 1.3), (dx + 0.75, 1.3)]
    f.fill(pts, style); f.ligne(pts, bord, ferme=True)
plan2d(f, 0)
f.ligne([(0.3, 0.28), (2.45, 0.78)], "droiteN")
f.label((2.45, 0.78), "$d$", style="lblN", pref=60)
f.texte((0.95, 1.0), r"$\mathcal{P}$", style="lblN")
plan2d(f, 3.05)
I2 = (4.4, 0.55)
f.ligne([I2, (4.66, 2.3)], "droiteN"); f.ligne([I2, (4.33, 0.09)], "droiteNC"); f.ligne([(4.33, 0.09), (4.22, -0.62)], "droiteN")
f.point(I2)
f.label(I2, "$I$", pref=200)
f.label((4.66, 2.3), "$d$", style="lblN", pref=0)
f.texte((4.0, 1.0), r"$\mathcal{P}$", style="lblN")
plan2d(f, 6.1)
f.ligne([(6.45, 2.0), (8.6, 2.45)], "droiteN")
f.ligne([(6.45, 0.3), (8.6, 0.75)], "guideF")
f.label((8.6, 2.45), "$d$", style="lblN", pref=0)
f.texte((7.05, 1.0), r"$\mathcal{P}$", style="lblN")
f.texte((1.37, -0.95), r"$d \subset \mathcal{P}$", n=4)
f.texte((4.42, -0.95), r"$d \cap \mathcal{P} = \{I\}$", n=8)
f.texte((7.47, -0.95), r"$d \parallel \mathcal{P}$", n=4)
FIGURES["droite_et_plan"] = f.tikz()

# IV.3 Deux plans : sécants selon une droite / parallèles
f = Fig()
P_ = [(0, 0), (3.0, 0), (3.8, 1.2), (0.8, 1.2)]
Lq, Rq = (0.95, 0.55), (3.15, 0.78)
haut = 1.15
Qbas = [Lq, Rq, (Rq[0], Rq[1] - 1.05), (Lq[0], Lq[1] - 1.05)]
Qhaut = [Lq, Rq, (Rq[0], Rq[1] + haut), (Lq[0], Lq[1] + haut)]
f.fill(Qbas, "planV"); f.fill(P_, "planB"); f.fill(Qhaut, "planV")
f.ligne([(0, 0), (3.0, 0), (3.8, 1.2)], "bordB"); f.ligne([(0, 0), (0.8, 1.2), (0.95, 1.2)], "bordB")
f.ligne([(0.95, 1.2), (3.15, 1.2)], "bordB, dash pattern=on 2.5pt off 1.8pt"); f.ligne([(3.15, 1.2), (3.8, 1.2)], "bordB")
f.ligne([(Lq[0], Lq[1] + haut), (Rq[0], Rq[1] + haut)], "bordV")
f.ligne([(Lq[0], Lq[1] + haut), Lq], "bordV"); f.ligne([(Rq[0], Rq[1] + haut), Rq], "bordV")
f.ligne([Lq, (Lq[0], 0)], "bordV, dash pattern=on 2.5pt off 1.8pt"); f.ligne([(Lq[0], 0), (Lq[0], Lq[1] - 1.05)], "bordV")
f.ligne([Rq, (Rq[0], 0.225)], "bordV, dash pattern=on 2.5pt off 1.8pt"); f.ligne([(Rq[0], 0.225), (Rq[0], Rq[1] - 1.05)], "bordV")
f.ligne([(Lq[0], Lq[1] - 1.05), (Rq[0], Rq[1] - 1.05)], "bordV")
dl = ((Rq[0] - Lq[0]), (Rq[1] - Lq[1]))
f.ligne([(Lq[0] - 0.2 * dl[0], Lq[1] - 0.2 * dl[1]), (Rq[0] + 0.25 * dl[0], Rq[1] + 0.25 * dl[1])], "droiteO", dessus=True)
f.label((Rq[0] + 0.25 * dl[0], Rq[1] + 0.25 * dl[1]), r"$\Delta$", style="lblO", pref=0)
f.texte((0.5, 0.28), r"$\mathcal{P}$", style="lblN")
f.texte((1.35, 1.62), r"$\mathcal{Q}$", style="lblV")
x0 = 4.75
Pp = [(x0, 0), (x0 + 3.0, 0), (x0 + 3.8, 1.0), (x0 + 0.8, 1.0)]
Qp = [(x, y + 1.45) for x, y in Pp]
f.fill(Pp, "planB"); f.ligne(Pp, "bordB", ferme=True)
f.fill(Qp, "planV"); f.ligne(Qp, "bordV", ferme=True)
f.texte((x0 + 0.55, 0.25), r"$\mathcal{P}$", style="lblN")
f.texte((x0 + 0.55, 1.7), r"$\mathcal{Q}$", style="lblV")
f.texte((1.9, -0.95), r"sécants selon $\Delta$", n=13)
f.texte((x0 + 1.9, -0.95), "parallèles", n=10)
FIGURES["deux_plans"] = f.tikz()

# IV.4 Théorème du toit
f = Fig()
k = 1.45
O_, T_ = (0, 0), (0, 2.5 * k)
P1 = [O_, T_, (-1.9 * k, 3.0 * k), (-1.9 * k, 0.5 * k)]
P2 = [O_, T_, (1.8 * k, 3.25 * k), (1.8 * k, 0.75 * k)]
f.fill(P1, "planB"); f.fill(P2, "planV")
f.ligne([P1[1], P1[2], P1[3], P1[0]], "bordB"); f.ligne([P2[1], P2[2], P2[3], P2[0]], "bordV")
f.ligne([(-0.95 * k, 0.15 * k), (-0.95 * k, 2.85 * k)], "droiteN", dessus=True)
f.ligne([(0.9 * k, 0.27 * k), (0.9 * k, 2.97 * k)], "droiteV", dessus=True)
f.ligne([(0, -0.35 * k), (0, 2.85 * k)], "droiteO", dessus=True)
f.label((0, 2.85 * k), r"$\Delta$", style="lblO", pref=90)
f.label((-0.95 * k, 2.85 * k), "$d_1$", n=2, style="lblN", pref=90)
f.label((0.9 * k, 2.97 * k), "$d_2$", n=2, style="lblV", pref=90)
f.texte((-1.45 * k, 0.95 * k), r"$\mathcal{P}_1$", style="lblN", n=2)
f.texte((1.38 * k, 1.2 * k), r"$\mathcal{P}_2$", style="lblV", n=2)
FIGURES["theoreme_toit"] = f.tikz()

# V. Section du cube par (IJG) : trapèze IJGE
f = Fig(3.5)
Ic, Jc = mil(S["A"], S["B"]), mil(S["B"], S["C"])
f.fill([Ic, Jc, S["G"], S["E"]], "section")
cube(f, S)
f.ligne([Jc, S["G"], S["E"], Ic], "rep", dessus=True); f.ligne([Ic, Jc], "repC", dessus=True)
f.point(Ic, "ptV"); f.point(Jc, "ptV")
f.label(Ic, "$I$", style="lblV", pref=-90); f.label(Jc, "$J$", style="lblV", pref=-20)
FIGURES["section_trapeze"] = f.tikz()

# ================================================================ EXERCICES
# 1097 : repère (A ; AB, AD, AE)
f = Fig(3.5)
cube(f, S, leger=True)
f.vec(S["A"], S["B"]); f.vec(S["A"], S["D"], "vecNC"); f.vec(S["A"], S["E"])
FIGURES["cube_repere_A"] = f.tikz()

# 1098 : plans (ABCD), (BCGF) et droites d1, d2
f = Fig(3.3)
f.fill([S["A"], S["B"], S["C"], S["D"]], "planB"); f.fill([S["B"], S["C"], S["G"], S["F"]], "planV")
cube(f, S)
a0, _ = ext(S["A"], S["D"], -0.55, 0)
f.ligne([a0, S["A"]], "droiteN", dessus=True); f.ligne([S["A"], mil(S["A"], S["D"], 1.3)], "droiteNC", dessus=True)
f.ligne(list(ext(S["F"], S["G"], -0.55, 1.45)), "droiteV", dessus=True)
f.label(a0, "$(d_1)$", n=4, style="lblN", pref=200)
f.label(mil(S["F"], S["G"], 1.45), "$(d_2)$", n=4, style="lblV", pref=30)
f.texte(mil(mil(S["A"], S["B"], 0.62), mil(S["D"], S["C"], 0.62), 0.5), r"$\mathcal{P}_1$", style="lblN", n=2)
f.texte(mil(mil(S["B"], S["C"], 0.5), mil(S["F"], S["G"], 0.5), 0.3), r"$\mathcal{P}_2$", style="lblV", n=2)
FIGURES["cube_deux_plans_droites"] = f.tikz()

# 1098, Q5 : plans (ADGF) et (BCHE), droite Δ = (KL)
f = Fig(3.4, uy=(0.56, 0.22))
f.fill([S["A"], S["D"], S["G"], S["F"]], "planV, fill opacity=0.75")
f.fill([S["B"], S["C"], S["H"], S["E"]], "planB, fill opacity=0.75")
cube(f, S, leger=True)
f.ligne([S["A"], S["F"]], "bordV, line width=0.8pt"); f.ligne([S["D"], S["G"]], "bordV, line width=0.75pt, dash pattern=on 3pt off 2pt")
f.ligne([S["B"], S["E"]], "bordB, line width=0.8pt"); f.ligne([S["C"], S["H"]], "bordB, line width=0.75pt, dash pattern=on 3pt off 2pt")
Kc, Lc = (0.5, 0, 0.5), (0.5, 1, 0.5)
f.ligne([mil(Kc, Lc, -0.55), Kc], "droiteO", dessus=True); f.ligne([Kc, mil(Kc, Lc, 1.3)], "droiteOC", dessus=True)
f.point(Kc, "ptO"); f.point(Lc, "ptO")
f.label(Kc, "$K$", style="lblO", pref=-90); f.label(Lc, "$L$", style="lblO", pref=90)
f.label(mil(Kc, Lc, -0.55), r"$\Delta$", style="lblO", pref=200)
FIGURES["cube_toit"] = f.tikz()

# 1102 : section du cube par (IJK), I, J, K milieux de [AD], [AE], [FG]
Is, Js, Ks = mil(S["A"], S["D"]), mil(S["A"], S["E"]), mil(S["F"], S["G"])
Ps, Rs, Ns, Ms = (0, -0.5, 1), mil(S["E"], S["F"]), mil(S["C"], S["G"]), mil(S["C"], S["D"])


def base_1102(f, etape):
    if etape >= 3:
        f.fill([Is, Js, Rs, Ks, Ns, Ms], "section")
    cube(f, S, leger=etape >= 1, pref={"E": 150, "D": -60})
    if etape >= 1:
        f.ligne([Is, Js], "constrC", dessus=True); f.ligne([Js, Ps], "constr", dessus=True)
        f.ligne([S["E"], Ps], "constr", dessus=True)
    if etape >= 2:
        f.ligne([Ps, Rs], "constr" if etape >= 3 else "rep", dessus=True)
        f.ligne([Rs, Ks], "rep", dessus=True); f.ligne([Ks, mil(Rs, Ks, 1.35)], "constr" if etape >= 3 else "rep", dessus=True)
    if etape >= 3:
        f.ligne([Js, Rs], "rep", dessus=True); f.ligne([Ks, Ns], "rep", dessus=True)
        f.ligne([Ns, Ms], "repC", dessus=True); f.ligne([Ms, Is], "repC", dessus=True); f.ligne([Is, Js], "repC", dessus=True)
    for q, nom in ((Is, "I"), (Js, "J"), (Ks, "K")):
        f.point(q, "ptN")
        f.label(q, f"${nom}$", style="lblN", pref={"I": -40, "J": 180, "K": 70}[nom])
    if etape >= 1:
        f.point(Ps, "ptV" if etape == 1 else "ptO")
        f.label(Ps, "$P$", style="lblV" if etape == 1 else "lblO", pref=150)
    if etape >= 2:
        f.point(Rs, "ptV"); f.label(Rs, "$R$", style="lblV", pref=110)
    if etape >= 3:
        f.point(Ns, "ptV"); f.label(Ns, "$N$", style="lblV", pref=0)
        f.point(Ms, "ptV"); f.label(Ms, "$M$", style="lblV", pref=-60)


for k, nom in enumerate(["section_cube_enonce", "section_cube_q1", "section_cube_q2", "section_cube_q3"]):
    f = Fig(3.3)
    base_1102(f, k)
    FIGURES[nom] = f.tikz()

# 1101 : tétraèdre ABCD, milieux I, J, K, L de [AB], [AC], [CD], [BD]
TA, TB, TC, TD = (1.6, 3.4), (0, 1.4), (3.6, 1.15), (1.9, -0.25)   # arête cachée : [AD]
sc = 1.35
TA, TB, TC, TD = [(x * sc, y * sc) for x, y in (TA, TB, TC, TD)]
TI, TJ, TK, TL = mil(TA, TB), mil(TA, TC), mil(TC, TD), mil(TB, TD)


def tetra(f, section):
    if section:
        f.fill([TI, TJ, TK, TL], "section")
    for a, b in ((TA, TB), (TA, TC), (TB, TD), (TB, TC), (TC, TD)):
        f.ligne([a, b], "arete")
    f.ligne([TA, TD], "cachee")
    if section:
        f.ligne([TI, TJ], "rep", dessus=True); f.ligne([TK, TL], "rep", dessus=True)
        f.ligne([TJ, TK], "repC", dessus=True); f.ligne([TL, TI], "repC", dessus=True)
    for q, n in ((TA, "A"), (TB, "B"), (TC, "C"), (TD, "D")):
        f.label(q, f"${n}$")
    for q, n in ((TI, "I"), (TJ, "J"), (TK, "K"), (TL, "L")):
        f.point(q, "ptV" if section else "ptN")
        f.label(q, f"${n}$", style="lblV" if section else "lblN")


f = Fig(); tetra(f, False); FIGURES["tetraedre_milieux"] = f.tikz()
f = Fig(); tetra(f, True); FIGURES["tetraedre_section"] = f.tikz()

# 1103 : cube, I milieu de [EF], J milieu de [BC]
I3, J3 = mil(S["E"], S["F"]), mil(S["B"], S["C"])
f = Fig(3.5)
cube(f, S)
f.point(I3, "ptN"); f.point(J3, "ptN")
f.label(I3, "$I$", style="lblN", pref=90); f.label(J3, "$J$", style="lblN", pref=-30)
FIGURES["cube_milieux_IJ"] = f.tikz()
f = Fig(3.5)
cube(f, S, leger=True)
f.vec(S["C"], S["E"]); f.vec(S["C"], S["G"]); f.vec(I3, J3, "vecV")
f.point(I3, "ptV"); f.point(J3, "ptV")
f.label(I3, "$I$", style="lblV", pref=90); f.label(J3, "$J$", style="lblV", pref=-30)
FIGURES["cube_IJ_CE_CG"] = f.tikz()

# 1104 : pavé droit, I milieu de [BF]
SP = sommets(2.2, 1.3, 1.2)
IP = mil(SP["B"], SP["F"])


def pave(f, leger):
    cube(f, SP, leger=leger)


f = Fig(2.05)
pave(f, False)
f.point(IP, "ptN"); f.label(IP, "$I$", style="lblN", pref=0)
FIGURES["pave_I"] = f.tikz()
f = Fig(2.05)
pave(f, True)
f.vec(SP["D"], SP["E"]); f.vec(SP["D"], SP["G"]); f.vec(SP["C"], SP["A"], "vecV")
FIGURES["pave_CA_DE_DG"] = f.tikz()
f = Fig(2.05)
pave(f, True)
f.vec(SP["D"], SP["F"]); f.vec(SP["H"], SP["E"]); f.vec(SP["A"], IP, "vecO")
f.point(IP, "ptO"); f.label(IP, "$I$", style="lblO", pref=0)
FIGURES["pave_AI_DF_HE"] = f.tikz()

# ================================================================ FINITION 2026-11-02
# Figures des corrigés des exercices calculatoires (outil commun espace.py :
# parties cachées calculées, étiquettes placées hors des traits).
import espace as es  # noqa: E402

PREAMBULE_EXTRA += es.STYLES


def triedre(f, o, k=0.55):
    """Petit trièdre d'orientation (x vers l'observateur, y à droite, z en haut) en o."""
    for d, nom, pr in (((k, 0, 0), "x", 225), ((0, k, 0), "y", 0), ((0, 0, k), "z", 90)):
        f.vec(o, es.add(o, d), "eAxe")
        f.label(es.add(o, d), f"${nom}$", style="eLblM", pref=pr, r=0.04)


# 1093, Q5 : AB(3 ; -3 ; 2) = « avancer de 3 selon x, reculer de 3 selon y, monter de 2 selon z »
f = es.Fig(1.05, repere=True)
A0 = (0, 0, 0)
P1, P2, B0 = (3, 0, 0), (3, -3, 0), (3, -3, 2)
boite = es.sommets_pave(3, 3, 2, o=(0, -3, 0))       # boîte x ∈ [0 ; 3], y ∈ [-3 ; 0], z ∈ [0 ; 2]
cachees = {((0, -3, 0), (3, -3, 0)), ((0, -3, 0), (0, 0, 0)), ((0, -3, 0), (0, -3, 2))}
for a, b in ("AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"):
    pa, pb = boite[a], boite[b]
    f.ligne([pa, pb], "eCacheeL" if (pa, pb) in cachees or (pb, pa) in cachees else "eAreteL")
f.vec(A0, P1, "eVecO"); f.vec(P1, P2, "eVecO"); f.vec(P2, B0, "eVecO")
f.vec(A0, B0, "eVecV")
f.point(A0); f.point(B0, "ptV")
f.label(A0, r"$A(1\,;2\,;3)$", n=8, pref=0)
f.label(B0, r"$B(4\,;-1\,;5)$", n=9, style="eLblV", pref=180)
f.label(es.mil(A0, P1), r"$+3$", n=2, style="eLblO", pref=-120, r=0.05)
f.label(es.mil(P1, P2), r"$-3$", n=2, style="eLblO", pref=-90, r=0.05)
f.label(es.mil(P2, B0), r"$+2$", n=2, style="eLblO", pref=180, r=0.05)
triedre(f, (3.3, 3.2, 0))
FIGURES["n1093_chemin_AB"] = f.tikz()

# 1094, Q4 : A, C, B alignés, C milieu de [AB] (direction (1 ; 1 ; 1) en perspective)
f = es.Fig(2.1, repere=True)
Aa, Cc, Bb = (1, 2, 3), (2, 3, 4), (3, 4, 5)
f.ligne([es.mil(Aa, Bb, -0.45), es.mil(Aa, Bb, 1.4)], "eDroite")
f.label(es.mil(Aa, Bb, 1.4), "$(AB)$", n=4, style="eLblN", pref=60)
# vecteurs décalés de part et d'autre de la droite (dans le plan de la figure)
(xa, ya), (xb, yb), (xc, yc) = f.p(Aa), f.p(Bb), f.p(Cc)
L = ((xb - xa) ** 2 + (yb - ya) ** 2) ** 0.5
nx, ny = -(yb - ya) / L * 0.36 / f.s, (xb - xa) / L * 0.36 / f.s
q = lambda x, y, k: (x / f.s + k * nx, y / f.s + k * ny)
f.vec(q(xa, ya, -1), q(xb, yb, -1), "eVec")
f.vec(q(xa, ya, -2.1), q(xc, yc, -2.1), "eVecV")
f.label(es.mil(q(xa, ya, -1), q(xb, yb, -1), 0.8), r"$\overrightarrow{AB}$", n=3, h=0.55, style="eLblN", pref=-20, r=0.08)
f.label(es.mil(q(xa, ya, -2.1), q(xc, yc, -2.1)), r"$\overrightarrow{AC}$", n=3, h=0.55, style="eLblV", pref=-20, r=0.08)
f.codage(Aa, Cc, 1); f.codage(Cc, Bb, 1)
f.point(Aa); f.point(Bb); f.point(Cc, "ptV")
f.label(Aa, r"$A(1\,;2\,;3)$", n=8, pref=170)
f.label(Bb, r"$B(3\,;4\,;5)$", n=8, pref=170)
f.label(Cc, r"$C(2\,;3\,;4)$", n=8, style="eLblV", pref=170)
FIGURES["n1094_alignes"] = f.tikz()


# 1095 : vecteurs u, v (non colinéaires) d'origine O dans un plan ; w = 2u + v ; t hors du plan
def plan_uv(f, avec_t):
    cadre = [(0, 0), (6.3, 0), (7.5, 2.6), (1.2, 2.6)]
    f.fill(cadre, "ePlanB"); f.ligne(cadre, "eBordB", ferme=True)
    O = (1.0, 0.45); u = (1.15, 0.0); v = (0.42, 0.48)
    pt = lambda a, b: (O[0] + a * u[0] + b * v[0], O[1] + a * u[1] + b * v[1])
    U, V, U2, W = pt(1, 0), pt(0, 1), pt(2, 0), pt(2, 1)
    f.ligne([U, U2], "eGuide"); f.ligne([U2, W], "eGuide"); f.ligne([V, W], "eGuide")
    f.vec(O, U); f.vec(O, V)
    f.vec(O, W, "eVecV")
    f.point(O); f.point(U2, "ptM")
    f.label(O, "$O$", pref=200)
    f.label(es.mil(O, U), r"$\vec{u}$", h=0.5, pref=-90, r=0.04)
    f.label(es.mil(O, V), r"$\vec{v}$", h=0.5, pref=150, r=0.04)
    f.label(U2, r"$2\vec{u}$", n=2, h=0.5, style="eLblM", pref=-70)
    f.label(W, r"$\vec{w} = 2\vec{u} + \vec{v}$", n=8, h=0.5, style="eLblV", pref=60)
    f.texte((7.0, 0.3), r"$\mathcal{P}$", style="eLblN")
    if avec_t:
        T2 = pt(3, 2)                       # 3u + 2v, dans le plan
        T = (T2[0], T2[1] + 1.55)            # pointe de t : hors du plan
        f.ligne([T2, T], "eGuide")
        f.vec(O, T, "eVecO")
        f.point(T2, "ptM")
        f.label(T2, r"$3\vec{u} + 2\vec{v}$", n=7, h=0.5, style="eLblM", pref=-30)
        f.label(T, r"$\vec{t}$", h=0.5, style="eLblO", pref=60)


f = es.Fig(); plan_uv(f, False); FIGURES["n1095_w"] = f.tikz()
f = es.Fig(); plan_uv(f, True); FIGURES["n1095_t"] = f.tikz()


# 1096 : ABDC parallélogramme dans le plan (ABC) ; E hors du plan
def plan_abdc(f, avec_e):
    cadre = [(0, 0), (5.6, 0), (6.9, 2.75), (1.3, 2.75)]
    f.fill(cadre, "ePlanB"); f.ligne(cadre, "eBordB", ferme=True)
    A, B, C = (1.0, 0.5), (3.6, 0.75), (2.0, 2.05)
    D = (B[0] + C[0] - A[0], B[1] + C[1] - A[1])
    f.fill([A, B, D, C], "ePlanV")
    f.ligne([B, D], "eRep"); f.ligne([C, D], "eRep")
    f.vec(A, B); f.vec(A, C)
    f.vec(A, D, "eVecV")
    for q, nom, st, pr in ((A, "A", "eLbl", 200), (B, "B", "eLbl", -30), (C, "C", "eLbl", 150), (D, "D", "eLblV", 30)):
        f.point(q, "ptV" if nom == "D" else "ptN")
        f.label(q, f"${nom}$", style=st, pref=pr)
    f.texte((5.35, 0.12), r"$(ABC)$", style="eLblN", n=4, anchor="south east", w=1.05)
    if avec_e:
        E = (1.45, 3.9)
        Ep = (1.45, 1.3)                    # pied de la verticale, dans le plan
        f.ligne([E, Ep], "eGuide")
        f.vec(A, E, "eVecO")
        f.point(E, "ptO"); f.point(Ep, "ptM")
        f.label(E, "$E$", style="eLblO", pref=30)


f = es.Fig(); plan_abdc(f, False); FIGURES["n1096_abdc"] = f.tikz()
f = es.Fig(); plan_abdc(f, True); FIGURES["n1096_e"] = f.tikz()

# 1099, Q5 : D hors du plan (ABC) — tétraèdre ABCD
f = es.Fig(1.05)
cadre = [(-0.6, -0.5, 0), (4.4, -0.5, 0), (4.4, 3.2, 0), (-0.6, 3.2, 0)]
es.plan(f, cadre)
Ta, Tb, Tc, Td = (0.2, 0.2, 0), (3.4, 0.4, 0), (2.6, 2.6, 0), (1.0, 1.3, 2.4)
f.fill([Ta, Tb, Tc], "ePlanV")
f.ecrans = []                              # seules les faces du tétraèdre cachent
f.opaque([Td, Ta, Tb], [Td, Tb, Tc], [Td, Tc, Ta])
for a, b in ((Ta, Tb), (Tb, Tc), (Tc, Ta)):
    f.seg(a, b, "eArete", "eCachee")
for a in (Ta, Tb, Tc):
    f.seg(Td, a, "eRep", "eRepC")
for q, nom in ((Ta, "A"), (Tb, "B"), (Tc, "C")):
    f.point(q); f.label(q, f"${nom}$")
f.point(Td, "ptV"); f.label(Td, "$D$", style="eLblV", pref=90)
f.label((4.4, 3.2, 0), r"$(ABC)$", n=4, style="eLblN", pref=0)
FIGURES["n1099_tetraedre"] = f.tikz()


# 1100 : plan P (C ; v1, v2), d1 strictement parallèle à P, d2 sécante à P en M
def plan_1100(f, avec_d2):
    X, Y = 5.2, 3.0
    cadre = [(0, 0, 0), (X, 0, 0), (X, Y, 0), (0, Y, 0)]
    es.plan(f, cadre)
    f.texte((X - 0.12, 0.12, 0), r"$\mathcal{P}$", style="eLblN", anchor="south east")
    C = (0.6, 0.45, 0)
    v1, v2 = (0.95, 0.0, 0), (0.05, 1.2, 0)
    f.vec(C, es.add(C, v1)); f.vec(C, es.add(C, v2))
    f.point(C); f.label(C, "$C$", pref=200)
    f.label(es.add(C, v1), r"$\vec{v_1}$", n=2, h=0.5, pref=-30, r=0.06)
    f.label(es.add(C, v2), r"$\vec{v_2}$", n=2, h=0.5, pref=150, r=0.04)
    u1 = (1.0, 0.25, 0)
    d0 = (1.8, 2.0, 0)
    f.ligne([es.add(d0, es.mul(-0.5, u1)), es.add(d0, es.mul(2.7, u1))], "eGuide")
    A = (1.8, 2.0, 1.35)
    f.seg(es.add(A, es.mul(-1.3, u1)), es.add(A, es.mul(3.0, u1)), "eDroite", "eDroiteC")
    f.vec(A, es.add(A, u1), "eVecV")
    f.point(A); f.label(A, "$A$", pref=120)
    f.label(es.add(A, es.mul(3.0, u1)), "$(d_1)$", n=4, style="eLblN", pref=0)
    f.label(es.add(A, es.mul(0.55, u1)), r"$\vec{u_1}$", n=2, h=0.5, style="eLblV", pref=90, r=0.06)
    if avec_d2:
        M = (3.6, 0.9, 0)
        u2 = (-0.35, 0.3, 1.0)
        f.seg(es.add(M, es.mul(-0.95, u2)), es.add(M, es.mul(1.0, u2)), "eDroiteV", "eDroiteVC")
        f.point(M, "ptV"); f.label(M, "$M$", style="eLblV", pref=-20)
        f.label(es.add(M, es.mul(1.0, u2)), "$(d_2)$", n=4, style="eLblV", pref=20)


f = es.Fig(1.0); plan_1100(f, False); FIGURES["n1100_d1"] = f.tikz()
f = es.Fig(1.0); plan_1100(f, True); FIGURES["n1100_bilan"] = f.tikz()
