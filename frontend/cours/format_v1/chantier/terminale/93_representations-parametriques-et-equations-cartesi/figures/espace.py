# -*- coding: utf-8 -*-
"""Outil de figures de géométrie dans l'espace (style des livres OptiTAB).

Perspective cavalière : x vers la droite, y en profondeur (0,42 ; 0,34), z vers le haut.
- parties cachées CALCULÉES : un segment est échantillonné et, pour chaque point,
  un rayon est lancé vers l'observateur ; s'il traverse une face déclarée opaque,
  la portion est tracée dans le style « caché » (pointillés) ;
- étiquettes placées AUTOMATIQUEMENT dans l'espace libre : 36 directions testées
  autour du point, on garde celle qui laisse le plus de marge avec les traits,
  les points et les autres étiquettes (aucun nom ne touche une arête).

Copie identique dans les notions 180, 92 et 93 (figures/espace.py).
"""
import math

import numpy as np

STYLES = r"""
\tikzset{
  eArete/.style={otNavy,line width=0.85pt,line join=round,line cap=round},
  eCachee/.style={otNavy!60,line width=0.7pt,dash pattern=on 3pt off 2pt},
  eAreteL/.style={otNavy!45,line width=0.7pt,line join=round,line cap=round},
  eCacheeL/.style={otNavy!35,line width=0.6pt,dash pattern=on 3pt off 2pt},
  eDroite/.style={otNavy,line width=1.2pt,line cap=round},
  eDroiteC/.style={otNavy!70,line width=0.8pt,dash pattern=on 3pt off 2pt},
  eDroiteV/.style={otGreenDark,line width=1.3pt,line cap=round},
  eDroiteVC/.style={otGreenDark,line width=0.9pt,dash pattern=on 3pt off 2pt},
  eDroiteO/.style={otOrange,line width=1.3pt,line cap=round},
  eDroiteOC/.style={otOrange,line width=0.9pt,dash pattern=on 3pt off 2pt},
  eRep/.style={otGreenDark,line width=1.3pt,line join=round,line cap=round},
  eRepC/.style={otGreenDark,line width=1pt,dash pattern=on 3pt off 2pt},
  eGuide/.style={otMuted,line width=0.6pt,dash pattern=on 2.5pt off 1.8pt},
  eFin/.style={otMuted,line width=0.6pt},
  eVec/.style={otNavy,line width=1.3pt,-{Stealth[length=2.6mm,width=2mm]}},
  eVecC/.style={otNavy,line width=1.1pt,dash pattern=on 3.2pt off 2pt,-{Stealth[length=2.6mm,width=2mm]}},
  eVecV/.style={otGreenDark,line width=1.4pt,-{Stealth[length=2.7mm,width=2.1mm]}},
  eVecVC/.style={otGreenDark,line width=1.2pt,dash pattern=on 3.2pt off 2pt,-{Stealth[length=2.7mm,width=2.1mm]}},
  eVecO/.style={otOrange,line width=1.4pt,-{Stealth[length=2.7mm,width=2.1mm]}},
  eAxe/.style={otMuted,line width=0.6pt,-{Stealth[length=2.1mm]}},
  eAngle/.style={otNavy,line width=0.6pt},
  eAngleV/.style={otGreenDark,line width=0.7pt},
  eArc/.style={otGreenDark,line width=0.8pt},
  eLbl/.style={inner sep=1pt,text=otInk,font=\normalsize},
  eLblV/.style={inner sep=1pt,text=otGreenDark,font=\normalsize},
  eLblN/.style={inner sep=1pt,text=otNavy,font=\normalsize},
  eLblO/.style={inner sep=1pt,text=otOrange!80!black,font=\normalsize},
  eLblM/.style={inner sep=1pt,text=otMuted,font=\normalsize},
  eNote/.style={inner sep=1pt,text=otMuted,font=\otRegular\fontsize{8.5}{10}\selectfont},
  ePlanB/.style={fill=otSky},
  ePlanV/.style={fill=otGreen!17},
  ePlanO/.style={fill=otOrange!13},
  eBordB/.style={otNavy!45,line width=0.6pt},
  eBordBC/.style={otNavy!35,line width=0.5pt,dash pattern=on 2.4pt off 1.8pt},
  eBordV/.style={otGreenDark!55,line width=0.6pt},
  eBordO/.style={otOrange!85!black,line width=0.6pt},
  eSection/.style={fill=otGreen!24},
}
"""

UY = (0.42, 0.34)


def f2(v):
    return f"{v:.3f}".rstrip("0").rstrip(".") if abs(v) > 1e-9 else "0"


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


def norme(a):
    return math.sqrt(dot(a, a))


def unit(a):
    n = norme(a)
    return mul(1 / n, a)


def mil(a, b, t=0.5):
    return tuple(a[i] + t * (b[i] - a[i]) for i in range(len(a)))


class Fig:
    """Une figure : faces opaques, traits (vus / cachés), points, étiquettes automatiques."""

    def __init__(self, s=1.0, uy=UY, repere=False):
        """repere=True : repère « classique » des manuels (x vers l'observateur, y vers la droite, z vers le haut)."""
        self.s, self.uy, self.repere = s, uy, repere
        # direction vers l'observateur (noyau de la projection)
        self.vue = (1.0, 0.5, 0.4) if repere else (uy[0], -1.0, uy[1])
        self.ecrans = []
        self.fonds, self.traits, self.dessus = [], [], []
        self.echant, self.points, self.etiq, self.boites = [], [], [], []

    # ------------------------------------------------------------ projection
    def p(self, q):
        if len(q) == 2:
            return (self.s * q[0], self.s * q[1])
        x, y, z = q
        if self.repere:
            return (self.s * (-0.5 * x + y), self.s * (-0.4 * x + z))
        return (self.s * (x + y * self.uy[0]), self.s * (y * self.uy[1] + z))

    def c(self, q):
        x, y = self.p(q)
        return f"({f2(x)},{f2(y)})"

    def _echantillonne(self, a, b):
        (x1, y1), (x2, y2) = self.p(a), self.p(b)
        n = max(2, int(math.hypot(x2 - x1, y2 - y1) / 0.03) + 1)
        for k in range(n):
            t = k / (n - 1)
            self.echant.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))

    # ------------------------------------------------------------ parties cachées
    def opaque(self, *polys):
        for poly in polys:
            self.ecrans.append([tuple(float(v) for v in q) for q in poly])

    @staticmethod
    def _dedans(q, poly, n):
        signes = []
        for i in range(len(poly)):
            a, b = poly[i], poly[(i + 1) % len(poly)]
            c = dot(cross(sub(b, a), sub(q, a)), n)
            if abs(c) < 1e-9:
                return False
            signes.append(c > 0)
        return all(signes) or not any(signes)

    def cache(self, q):
        for poly in self.ecrans:
            n = cross(sub(poly[1], poly[0]), sub(poly[2], poly[0]))
            den = dot(n, self.vue)
            if abs(den) < 1e-12:
                continue
            t = dot(n, sub(poly[0], q)) / den
            if t <= 1e-6:
                continue
            if self._dedans(add(q, mul(t, self.vue)), poly, n):
                return True
        return False

    # ------------------------------------------------------------ dessin
    def fill(self, pts, style):
        self.fonds.append(f"\\fill[{style}] " + " -- ".join(self.c(q) for q in pts) + " -- cycle;")

    def ligne(self, pts, style, ferme=False, dessus=False, compte=True):
        chemin = " -- ".join(self.c(q) for q in pts) + (" -- cycle" if ferme else "")
        (self.dessus if dessus else self.traits).append(f"\\draw[{style}] {chemin};")
        if compte:
            suite = list(pts) + ([pts[0]] if ferme else [])
            for a, b in zip(suite, suite[1:]):
                self._echantillonne(a, b)

    def seg(self, a, b, vu, cache=None, dessus=False, n=400):
        """Segment 3D : parties vues en style « vu », cachées en style « cache » (None : non tracées)."""
        if not self.ecrans:
            self.ligne([a, b], vu, dessus=dessus)
            return
        etats = [self.cache(mil(a, b, i / n)) for i in range(n + 1)]
        for i in range(1, n):
            if etats[i - 1] == etats[i + 1] != etats[i]:
                etats[i] = etats[i - 1]
        bornes = [0.0]
        for i in range(n):
            if etats[i] != etats[i + 1]:
                lo, hi = i / n, (i + 1) / n
                for _ in range(40):
                    m = (lo + hi) / 2
                    if self.cache(mil(a, b, m)) == etats[i]:
                        lo = m
                    else:
                        hi = m
                bornes.append((lo + hi) / 2)
        bornes.append(1.0)
        for t0, t1 in zip(bornes, bornes[1:]):
            if t1 - t0 < 1e-4:
                continue
            style = cache if self.cache(mil(a, b, (t0 + t1) / 2)) else vu
            if style is None:
                continue
            self.ligne([mil(a, b, t0), mil(a, b, t1)], style, dessus=dessus)

    def poly(self, pts, vu, cache=None, dessus=False):
        for i in range(len(pts)):
            self.seg(pts[i], pts[(i + 1) % len(pts)], vu, cache, dessus)

    def vec(self, a, b, style="eVec"):
        self.dessus.append(f"\\draw[{style}] {self.c(a)} -- {self.c(b)};")
        self._echantillonne(a, b)

    def point(self, q, style="ptN"):
        coul = {"ptN": "otNavy", "ptV": "otGreenDark", "ptO": "otOrange!90!black", "ptM": "otMuted"}[style]
        self.dessus.append(f"\\fill[{coul}] {self.c(q)} circle (2.3pt);")
        self.points.append(self.p(q))

    def angle_droit(self, S, a, b, q=0.22, style="eAngle"):
        """Petit carré d'angle droit en S (3D) entre les directions S→a et S→b (q en unités de la figure)."""
        ua, ub = unit(sub(a, S)), unit(sub(b, S))
        p1, p3 = add(S, mul(q, ua)), add(S, mul(q, ub))
        p2 = add(p1, mul(q, ub))
        self.dessus.append(f"\\draw[{style}] {self.c(p1)} -- {self.c(p2)} -- {self.c(p3)};")
        for u, v in ((p1, p2), (p2, p3)):
            self._echantillonne(u, v)

    def arc(self, S, a, b, r=0.4, style="eArc", n=24):
        """Arc d'angle en S (3D ou 2D) entre S→a et S→b, rayon r (unités de la figure)."""
        plan2d = len(S) == 2
        if plan2d:
            S, a, b = (S[0], S[1], 0.0), (a[0], a[1], 0.0), (b[0], b[1], 0.0)
        ua = unit(sub(a, S))
        w = sub(sub(b, S), mul(dot(sub(b, S), ua), ua))
        ub = unit(w)
        th = math.acos(max(-1.0, min(1.0, dot(ua, unit(sub(b, S))))))
        pts = [add(S, add(mul(r * math.cos(th * k / n), ua), mul(r * math.sin(th * k / n), ub))) for k in range(n + 1)]
        milieu = add(S, add(mul(r * math.cos(th / 2), ua), mul(r * math.sin(th / 2), ub)))
        if plan2d:
            pts = [q[:2] for q in pts]
            milieu = milieu[:2]
        self.ligne(pts, style, dessus=True)
        return milieu

    def codage(self, a, b, n=1, style="otNavy,line width=0.75pt"):
        (x1, y1), (x2, y2) = self.p(a), self.p(b)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        nx, ny = -uy, ux
        for k in range(n):
            d = (k - (n - 1) / 2) * 0.085
            cx, cy = mx + d * ux, my + d * uy
            self.dessus.append(f"\\draw[{style}] ({f2(cx - 0.11 * nx)},{f2(cy - 0.11 * ny)}) -- ({f2(cx + 0.11 * nx)},{f2(cy + 0.11 * ny)});")

    def label(self, q, texte, n=1, style="eLbl", pref=None, r=0.08, h=0.42, w=None, dirs=None):
        """Étiquette près de q (n ≈ nombre de caractères visibles), placée dans l'espace libre."""
        self.etiq.append((self.p(q), texte, w if w else 0.14 + 0.21 * n, h, style, pref, r, dirs))

    def texte(self, q, texte, style="eLbl", anchor="center", n=1, h=0.42, w=None):
        """Texte à une place fixe (légende, nom de plan…)."""
        x, y = self.p(q)
        self.dessus.append(f"\\node[{style},anchor={anchor}] at ({f2(x)},{f2(y)}) {{{texte}}};")
        ww = w if w else 0.14 + 0.21 * n
        dx = dy = 0.0
        if "west" in anchor:
            dx = ww / 2
        if "east" in anchor:
            dx = -ww / 2
        if "north" in anchor:
            dy = -h / 2
        if "south" in anchor:
            dy = h / 2
        cx, cy = x + dx, y + dy
        self.boites.append((cx - ww / 2, cy - h / 2, cx + ww / 2, cy + h / 2))

    # ------------------------------------------------------------ placement
    def _place(self):
        E = np.array(self.echant) if self.echant else np.zeros((0, 2))
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
            for th in (dirs if dirs is not None else range(0, 360, 10)):
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


# ---------------------------------------------------------------- solides usuels
def sommets_pave(L=1, W=1, H=1, o=(0, 0, 0)):
    x, y, z = o
    return {"A": (x, y, z), "B": (x + L, y, z), "C": (x + L, y + W, z), "D": (x, y + W, z),
            "E": (x, y, z + H), "F": (x + L, y, z + H), "G": (x + L, y + W, z + H), "H": (x, y + W, z + H)}


VISIBLES = ["AB", "BC", "CG", "GH", "HE", "EA", "BF", "FE", "FG"]
CACHEES = ["AD", "DC", "DH"]


def pave(f, S, leger=False, noms=True, pref=None, sauf=()):
    """Pavé ABCDEFGH (face avant ABFE) : arêtes cachées [AD], [DC], [DH] en pointillés."""
    for a, b in VISIBLES:
        if a + b not in sauf:
            f.ligne([S[a], S[b]], "eAreteL" if leger else "eArete")
    for a, b in CACHEES:
        if a + b not in sauf:
            f.ligne([S[a], S[b]], "eCacheeL" if leger else "eCachee")
    if noms:
        centre = tuple(sum(S[k][i] for k in "ABCDEFGH") / 8 for i in range(3))
        cx, cy = f.p(centre)
        for k in "ABCDEFGH":
            x, y = f.p(S[k])
            pr = (pref or {}).get(k, math.degrees(math.atan2(y - cy, x - cx)))
            f.label(S[k], f"${k}$", pref=pr)


def plan(f, coins, style="ePlanB", bord="eBordB", opaque=True, nom=None, pos_nom=None, style_nom="eLblN"):
    """Plan représenté par un parallélogramme (coins 3D)."""
    if opaque:
        f.opaque(coins)
    f.fill(coins, style)
    f.ligne(coins, bord, ferme=True)
    if nom:
        f.texte(pos_nom, nom, style=style_nom, n=1)
