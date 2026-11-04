# -*- coding: utf-8 -*-
"""Figures de la notion 369 « Sujets type bac » (Terminale), style des livres OptiTAB.

Compilation (depuis frontend/cours/format_v1/outils/) :

    python figures_livre.py ../chantier/terminale/369_sujets-type-bac [nom …] --planche

Toutes les valeurs tracées sont CALCULÉES ici (math.comb, math.exp) : elles
sont identiques à celles du texte, elles-mêmes contrôlées par ../verif_bac.py.

Conventions : énoncé en bleu marine (squelettes à compléter), éléments de
réponse du corrigé en vert (otGreenDark), point remarquable en orange.
Les arbres pondérés reprennent la fonction `arbre` de la notion 179, les
solides la classe `Fig` de la notion 180 (étiquettes placées automatiquement
dans l'espace libre).
"""
import math
from math import comb, exp

import numpy as np

PREAMBULE_EXTRA = r"""
\tikzset{
  evt/.style={font=\normalsize, text=otNavy, inner sep=2.4pt},
  evtV/.style={evt, text=otGreenDark},
  branche/.style={otNavy!65, line width=0.8pt, line cap=round},
  brancheV/.style={otGreenDark, line width=1.6pt, line cap=round},
  poids/.style={font=\small, text=otInk, inner sep=1.7pt},
  poidsV/.style={poids, text=otGreenDark},
  issue/.style={font=\small, text=otMuted, anchor=west, inner sep=1.5pt},
  issueV/.style={issue, text=otGreenDark},
  racine/.style={fill=otNavy},
  arete/.style={otNavy,line width=0.85pt,line join=round,line cap=round},
  cachee/.style={otNavy!60,line width=0.7pt,dash pattern=on 3pt off 2pt},
  areteL/.style={otNavy!45,line width=0.7pt,line join=round,line cap=round},
  cacheeL/.style={otNavy!35,line width=0.6pt,dash pattern=on 3pt off 2pt},
  vecN/.style={otNavy,line width=1.35pt,-{Stealth[length=2.7mm,width=2.1mm]}},
  vecV/.style={otGreenDark,line width=1.45pt,-{Stealth[length=2.8mm,width=2.2mm]}},
  droiteV/.style={otGreenDark,line width=1.3pt},
  droiteVC/.style={otGreenDark,line width=1.1pt,dash pattern=on 3pt off 2pt},
  tetra/.style={otNavy,line width=1.15pt,line join=round},
  tetraC/.style={otNavy,line width=1pt,dash pattern=on 3pt off 2pt},
  guideF/.style={otMuted,line width=0.6pt,dash pattern=on 2.5pt off 1.8pt},
  lbl/.style={inner sep=1pt,text=otInk,font=\normalsize},
  lblV/.style={inner sep=1pt,text=otGreenDark,font=\normalsize},
  lblN/.style={inner sep=1pt,text=otNavy,font=\normalsize},
  lblO/.style={inner sep=1pt,text=otOrange!80!black,font=\normalsize},
  lblM/.style={inner sep=1pt,text=otMuted,font=\normalsize},
  planB/.style={fill=otSky},
  planV/.style={fill=otGreen!20},
  bordB/.style={otNavy!45,line width=0.55pt},
  frise/.style={font=\otRegular\fontsize{8.5}{10}\selectfont, text=otInk, align=center, inner sep=1pt},
}
"""


# ====================================================================== arbres
def N(nom, poids, *enfants, droite=None, vert=False, pos=0.5):
    return {"nom": nom, "poids": poids, "enfants": list(enfants), "droite": droite,
            "vert": vert, "pos": pos}


def _vert(n):
    if not n["enfants"]:
        return n["vert"]
    n["vert"] = n["vert"] or any([_vert(c) for c in n["enfants"]])
    return n["vert"]


def _placer(n, prof, y, dy, ecarts, L):
    n["x"] = prof * L
    if not n["enfants"]:
        n["y"] = y
        return y - dy
    ys = []
    for k, c in enumerate(n["enfants"]):
        if k and c["enfants"]:
            y -= ecarts.get(prof + 1, 0)
        y = _placer(c, prof + 1, y, dy, ecarts, L)
        ys.append(c["y"])
    n["y"] = (ys[0] + ys[-1]) / 2
    return y


def arbre(enfants, L=2.2, dy=1.0, ecarts=None, ecart_droite="4pt"):
    """Arbre pondéré horizontal ; probabilités posées à côté des branches."""
    racine = {"nom": None, "poids": None, "enfants": enfants, "droite": None, "vert": False, "pos": 0.5}
    _vert(racine)
    _placer(racine, 0, 0.0, dy, ecarts or {}, L)
    lignes = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    noeuds, aretes, poids, droites = [], [], [], []
    compteur = [0]

    def visiter(n, parent_ref, parent_y):
        for c in n["enfants"]:
            compteur[0] += 1
            nom = f"n{compteur[0]}"
            style = "evtV" if (c["vert"] and not c["enfants"]) else "evt"
            noeuds.append(rf"\node[{style}] ({nom}) at ({c['x']:.3f},{c['y']:.3f}) {{${c['nom']}$}};")
            st = "brancheV" if c["vert"] else "branche"
            aretes.append((st, rf"\draw[{st}] {parent_ref} -- ({nom}.west);"))
            if c["poids"] is not None:
                ecart = c["y"] - parent_y
                anc = "south east" if ecart > 1e-6 else ("north east" if ecart < -1e-6 else "south")
                sp = "poidsV" if c["vert"] else "poids"
                poids.append(rf"\path {parent_ref} -- ({nom}.west) node[{sp},pos={c['pos']},anchor={anc}] {{${c['poids']}$}};")
            if not c["enfants"] and c["droite"]:
                si = "issueV" if c["vert"] else "issue"
                droites.append(rf"\node[{si}] at ([xshift={ecart_droite}]{nom}.east) {{{c['droite']}}};")
            visiter(c, f"({nom}.east)", c["y"])

    lignes.append(rf"\coordinate (r) at (0,{racine['y']:.3f});")
    visiter(racine, "(r)", racine["y"])
    lignes += noeuds
    lignes += [a for s, a in aretes if s == "branche"] + [a for s, a in aretes if s == "brancheV"]
    lignes.append(r"\fill[racine] (r) circle (1.9pt);")
    lignes += poids + droites
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


def binaire(a, pa, b, pb, a1, pa1, a2, pa2, b1, pb1, b2, pb2, droites=None, verts=(), **kw):
    d = droites or [None] * 4
    return arbre([
        N(a, pa, N(a1, pa1, droite=d[0], vert=0 in verts), N(a2, pa2, droite=d[1], vert=1 in verts)),
        N(b, pb, N(b1, pb1, droite=d[2], vert=2 in verts), N(b2, pb2, droite=d[3], vert=3 in verts)),
    ], **kw)


def bar(e):
    return rf"\overline{{{e}}}"


def virg(x, nd=3):
    """Nombre décimal à la française pour LaTeX : 0.035 → 0{,}035."""
    s = f"{x:.{nd}f}".rstrip("0").rstrip(".")
    return s.replace(".", "{,}")


# ====================================================================== espace
UX, UY, UZ = (1.0, 0.0), (0.42, 0.34), (0.0, 1.0)


def f2(v):
    return f"{v:.3f}".rstrip("0").rstrip(".") if abs(v) > 1e-9 else "0"


class Fig:
    """Une figure : traits, remplissages, points, étiquettes placées automatiquement."""

    def __init__(self, s=3.4, uy=None):
        self.s = s
        self.uy = uy or UY
        self.fonds, self.traits, self.dessus = [], [], []
        self.echant, self.points, self.etiq, self.boites = [], [], [], []

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
        self.etiq.append((self.p(q), texte, w if w else 0.14 + 0.21 * n, h, style, pref, r, dirs))

    def texte(self, q, texte, style="lbl", anchor="center", n=1, h=0.42, w=None):
        x, y = self.p(q)
        self.dessus.append(f"\\node[{style},anchor={anchor}] at ({f2(x)},{f2(y)}) {{{texte}}};")
        ww = w if w else 0.14 + 0.21 * n
        self.boites.append((x - ww / 2, y - h / 2, x + ww / 2, y + h / 2))

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


S = {"A": (0, 0, 0), "B": (1, 0, 0), "C": (1, 1, 0), "D": (0, 1, 0),
     "E": (0, 0, 1), "F": (1, 0, 1), "G": (1, 1, 1), "H": (0, 1, 1)}
VISIBLES = ["AB", "BC", "CG", "GH", "HE", "EA", "BF", "FE", "FG"]
CACHEES = ["AD", "DC", "DH"]


def cube(f, leger=False, pref=None):
    for a, b in VISIBLES:
        f.ligne([S[a], S[b]], "areteL" if leger else "arete")
    for a, b in CACHEES:
        f.ligne([S[a], S[b]], "cacheeL" if leger else "cachee")
    cx, cy = f.p((0.5, 0.5, 0.5))
    for k in "ABCDEFGH":
        x, y = f.p(S[k])
        pr = (pref or {}).get(k, math.degrees(math.atan2(y - cy, x - cx)))
        f.label(S[k], f"${k}$", pref=pr)


def mil(a, b, t=0.5):
    return tuple(a[i] + t * (b[i] - a[i]) for i in range(len(a)))


# ====================================================================== courbes
def f_num(x):
    """f(x) = x e^{-x} (exercice 4)."""
    return x * exp(-x)


F_PGF = "x*exp(-x)"


def axe(options, corps):
    return ("\\begin{tikzpicture}\n\\begin{axis}[otWeb, " + options + "]\n"
            + corps + "\n\\end{axis}\n\\end{tikzpicture}")


def courbe(expr, a, b, style="courbe", n=220):
    return f"  \\addplot[{style}, domain={a}:{b}, samples={n}] {{{expr}}};\n"


def noeud(x, y, texte, ancre, couleur="otNavy", extra=""):
    return f"  \\node[inner sep=1.4pt, text={couleur}, anchor={ancre}{extra}] at (axis cs:{x},{y}) {{{texte}}};\n"


def loi(n, p):
    return [comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]


def coords(valeurs, ks):
    return " ".join(f"({k},{valeurs[k]:.5f})" for k in ks)


BLEU = r"fill=otNavy!60,draw=otNavy,line width=0.5pt"
VERT = r"fill=otGreen!75,draw=otGreenDark,line width=0.5pt"
BARRES = (r"otBarres, bar shift=0pt, enlarge x limits=false, clip=false, scaled y ticks=false, "
          r"yticklabel style={/pgf/number format/fixed,/pgf/number format/precision=2}, "
          r"xlabel={$k$}, every axis x label/.style={at={(current axis.south east)},anchor=north west,"
          r"font=\normalsize,text=otMuted,xshift=2pt,yshift=-1pt}")

FIGURES = {}

# ############################################################################
#                                   SUJET
# ############################################################################

# ---------------------------------------------------------------- Exercice 1
P_R, P_RL, P_NL = 0.7, 0.05, 0.12
FIGURES["ex1_arbre_enonce"] = binaire(
    "R", r"\ldots", bar("R"), r"\ldots",
    "L", r"\ldots", bar("L"), r"\ldots",
    "L", r"\ldots", bar("L"), r"\ldots",
    L=2.3, dy=0.95, ecarts={1: 0.4})

FIGURES["ex1_arbre"] = binaire(
    "R", virg(P_R, 1), bar("R"), virg(1 - P_R, 1),
    "L", virg(P_RL, 2), bar("L"), virg(1 - P_RL, 2),
    "L", virg(P_NL, 2), bar("L"), virg(1 - P_NL, 2),
    droites=[f"$P(R\\cap L)={virg(P_R * P_RL)}$",
             f"$P(R\\cap \\overline{{L}})={virg(P_R * (1 - P_RL))}$",
             f"$P(\\overline{{R}}\\cap L)={virg((1 - P_R) * P_NL)}$",
             f"$P(\\overline{{R}}\\cap \\overline{{L}})={virg((1 - P_R) * (1 - P_NL))}$"],
    verts=(0, 2), L=2.3, dy=1.0, ecarts={1: 0.4})

P_L = P_R * P_RL + (1 - P_R) * P_NL          # 0,071
V50 = loi(50, P_L)
FIGURES["ex1_binomiale"] = rf"""
\begin{{tikzpicture}}
\begin{{axis}}[{BARRES}, width=5.9cm, height=4.2cm, bar width=6.5pt,
  xmin=-0.7, xmax=12.7, ymin=0, ymax=0.26, xtick={{0,2,4,6,8,10,12}}, minor xtick={{1,3,5,7,9,11}}, ytick={{0,0.05,0.1,0.15,0.2}},
  ylabel={{$P(X=k)$}}]
  \addplot[{BLEU}] coordinates {{{coords(V50, range(3, 13))}}};
  \addplot[{VERT}] coordinates {{{coords(V50, range(0, 3))}}};
  \node[anchor=north east,inner sep=1.4pt,font=\normalsize,text=otGreenDark] at (axis cs:12.6,0.222) {{$P(X\leqslant 2)\approx {virg(sum(V50[:3]))}$}};
  \node[anchor=north east,inner sep=1.4pt,font=\normalsize,text=otNavy] at (axis cs:12.6,0.258) {{$\mathcal{{B}}(50\,;0{{,}}071)$}};
\end{{axis}}
\end{{tikzpicture}}"""

# ---------------------------------------------------------------- Exercice 2 (vrai / faux)
# Affirmation 2 : y' = -2y + 2, y(0) = 4 ; proposée 4e^{-2x}, vraie 3e^{-2x} + 1
FIGURES["ex2_equa_diff"] = axe(
    r"width=6.4cm, height=4.4cm, xmin=-0.35, xmax=3.1, ymin=-0.3, ymax=4.7, xtick={1,2,3}, ytick={1,2,3,4}",
    r"  \draw[asymptote] (axis cs:-0.35,1) -- (axis cs:3.1,1);" + "\n"
    + courbe("4*exp(-2*x)", -0.05, 3.05, "otOrange, line width=1.2pt, dash pattern=on 5pt off 2.5pt")
    + courbe("3*exp(-2*x)+1", -0.05, 3.05, "otGreenDark, line width=1.4pt")
    + r"  \pnt[otNavy]{0}{4}" + "\n"
    + noeud(0.08, 4.12, r"$(0\,;4)$", "south west")
    + noeud(0.62, 2.9, r"$y=3e^{-2x}+1$", "south west", "otGreenDark")
    + noeud(2.1, 0.55, r"$y=4e^{-2x}$", "center", "otOrange!80!black")
    + noeud(3.05, 1.08, r"$y=1$", "south east", "otRed!85"))

# Affirmation 3 : ln(x) + ln(x - 2) ≤ ln 3
def bande(y, a, b, coul, ga, gd, texte):
    """Intervalle [a ; b] sur une droite graduée, crochets ga / gd (« [ » ou « ] »), à la hauteur y."""
    larg = 2.2 if coul == "otGreenDark" else 1.6
    s = rf"\draw[{coul}, line width={larg}pt] ({a},{y}) -- ({b},{y});" + "\n"
    for x, g in ((a, ga), (b, gd)):
        if g is None:
            continue
        sens = 1 if (g == "[") == (x == a) else -1  # crochet tourné vers l'intérieur ou l'extérieur
        s += (rf"\draw[{coul}, line width=1.3pt] ({x + 0.12 * sens},{y + 0.17}) -- ({x},{y + 0.17}) -- "
              rf"({x},{y - 0.17}) -- ({x + 0.12 * sens},{y - 0.17});" + "\n")
    s += rf"\node[anchor=west, text={coul}, inner sep=1pt] at (4.85,{y}) {{{texte}}};" + "\n"
    return s


def X(v):
    """Abscisse TikZ d'un réel v sur la droite graduée de -2 à 4 (1 unité = 0,85 cm)."""
    return round(0.3 + (v + 2) * 0.7, 3)


FIGURES["ex2_ln"] = (
    r"\begin{tikzpicture}[x=1cm,y=1cm]" + "\n"
    + r"\draw[otMuted, line width=0.6pt, -{Stealth[length=2.3mm]}] (0,0) -- (4.75,0);" + "\n"
    + "".join(rf"\draw[guide] ({X(v)},{y0}) -- ({X(v)},0.12);" + "\n"
              for v, y0 in ((-1, 0.9), (2, 1.55), (3, 0.9)))
    + "".join(rf"\draw[otMuted, line width=0.5pt] ({X(v)},0.08) -- ({X(v)},-0.08);" + "\n"
              + rf"\node[anchor=north, text=otMuted, inner sep=1pt, font=\otRegular\fontsize{{9}}{{10}}\selectfont] at ({X(v)},-0.12) {{${v}$}};" + "\n"
              for v in (-1, 0, 2, 3))
    + bande(1.75, X(2), 4.55, "otNavy", "]", None, r"$x>2$")
    + bande(1.1, X(-1), X(3), "otOrange!85!black", "[", "]", r"$x^2-2x-3\leqslant 0$")
    + bande(0.45, X(2), X(3), "otGreenDark", "]", "]", r"$S=\,]2\,;3]$")
    + r"\end{tikzpicture}")

# ---------------------------------------------------------------- Exercice 3 (espace)
f = Fig(3.5, uy=(0.5, 0.28))
f.fill([S["B"], S["E"], S["G"]], "planV, fill opacity=0.75")
cube(f, leger=True)
f.ligne([S["B"], S["E"], S["G"]], "tetra", ferme=True, dessus=True)
for a in "BEG":
    f.ligne([S["D"], S[a]], "tetraC", dessus=True)
FIGURES["ex3_cube_enonce"] = f.tikz()

K = (2 / 3, 1 / 3, 2 / 3)
f = Fig(3.5, uy=(0.5, 0.28))
f.fill([S["B"], S["E"], S["G"]], "planV, fill opacity=0.75")
cube(f, leger=True)
f.ligne([S["B"], S["E"], S["G"]], "tetra", ferme=True, dessus=True)
for a in "BEG":
    f.ligne([S["D"], S[a]], "tetraC", dessus=True)
# Δ passe par D, K et F (D + t(1 ; -1 ; 1) avec t = 2/3 puis t = 1) : c'est la diagonale (DF)
f.ligne([S["D"], K], "droiteVC", dessus=True)
fin = tuple(S["F"][i] + 0.6 * d for i, d in enumerate((1, -1, 1)))
f.ligne([K, fin], "droiteV", dessus=True)
f.point(K, "ptV")
f.label(K, "$K$", style="lblV", pref=-150)
f.label(fin, r"$\Delta$", style="lblV", pref=45)
FIGURES["ex3_cube"] = f.tikz()

# ---------------------------------------------------------------- Exercice 4 (fonction, suite, intégrale)
# graduations positives à gauche de l'axe (zone vide), négatives à droite (la courbe est à gauche)
YT = (r"ytick={0.2,0.4}, yticklabels={$0{,}2$,$0{,}4$}, "
      r"extra y ticks={-1.2,-0.8,-0.4}, extra y tick labels={$-1{,}2$,$-0{,}8$,$-0{,}4$}, "
      r"extra y tick style={yticklabel style={anchor=south west, xshift=4.5pt, yshift=1pt}}")
FIGURES["ex4_courbe_enonce"] = axe(
    r"width=7.3cm, height=5cm, xmin=-0.75, xmax=6.4, ymin=-1.45, ymax=0.62, xtick={1,2,3,4,5,6}, "
    + YT + r", minor ytick={-1.4,-1,-0.6,-0.2,0.6}, minor grid style={otRule!45,line width=0.3pt}, minor tick length=0pt",
    courbe(F_PGF, -0.68, 6.3)
    + noeud(1.7, 0.36, r"$\mathcal{C}_f$", "south west"))

# zoom : courbe et droite y = x (construction des termes de la suite)
ZOOM = (r"width=6.2cm, height=6.2cm, xmin=-0.04, xmax=1.12, ymin=-0.04, ymax=1.12, "
        r"xtick={0.2,0.4,0.6,0.8,1}, ytick={0.2,0.4,0.6,0.8,1}, "
        r"xticklabels={$0{,}2$,$0{,}4$,$0{,}6$,$0{,}8$,$1$}, yticklabels={$0{,}2$,$0{,}4$,$0{,}6$,$0{,}8$,$1$}, "
        r"minor xtick={0.1,0.3,0.5,0.7,0.9}, minor ytick={0.1,0.3,0.5,0.7,0.9}, "
        r"minor grid style={otRule!45,line width=0.3pt}, minor tick length=0pt")
FIGURES["ex4_zoom_enonce"] = axe(
    ZOOM,
    courbe("x", 0, 1.08, "otMuted, line width=0.9pt")
    + courbe(F_PGF, 0, 1.08)
    + noeud(0.83, 0.88, r"$y=x$", "south east", "otMuted")
    + noeud(1.02, 0.37, r"$\mathcal{C}_f$", "south"))

# corrigé Q3 : solution alpha de f(x) = 1/4 sur [0 ; 1]
ALPHA = 0.357403
FIGURES["ex4_alpha"] = axe(
    r"width=6.6cm, height=4.4cm, xmin=-0.3, xmax=4.4, ymin=-0.1, ymax=0.47, xtick={1,2,3,4}, "
    r"ytick={0.1,0.2,0.3}, yticklabels={$0{,}1$,$0{,}2$,$0{,}3$}, extra y ticks={0.25}, extra y tick labels={}, "
    r"extra y tick style={grid=none}",
    r"  \draw[seuil] (axis cs:-0.3,0.25) -- (axis cs:4.4,0.25);" + "\n"
    + courbe(F_PGF, -0.08, 4.35)
    + r"  \draw[guide] (axis cs:1,0) -- (axis cs:1,0.367879);" + "\n"
    + rf"  \draw[otGreenDark, line width=0.8pt, dash pattern=on 2.5pt off 1.6pt] (axis cs:{ALPHA},0.25) -- (axis cs:{ALPHA},0);" + "\n"
    + r"  \pnt{1}{0.367879}" + "\n"
    + rf"  \pnt[otGreenDark]{{{ALPHA}}}{{0.25}}" + "\n"
    + rf"  \fill[otGreenDark] (axis cs:{ALPHA},0) circle (2.3pt);" + "\n"
    + noeud(ALPHA, -0.012, r"$\alpha$", "north", "otGreenDark", ", yshift=-2pt")
    + noeud(1.08, 0.375, r"$\left(1\,;\dfrac{1}{e}\right)$", "south west")
    + noeud(4.35, 0.258, r"$y=\dfrac{1}{4}$", "south east", "otOrange!80!black")
    + noeud(3.3, 0.165, r"$\mathcal{C}_f$", "south west"))

# corrigé Q4-Q5 : tangente en 0, point d'inflexion
YI = 2 * exp(-2)
FIGURES["ex4_tangente"] = axe(
    r"width=7.3cm, height=5cm, xmin=-0.75, xmax=6.4, ymin=-1.45, ymax=0.62, xtick={1,3,4,5,6}, "
    + YT,
    r"  \draw[guide] (axis cs:2,-1.45) -- (axis cs:2,0.62);" + "\n"
    + courbe("x", -0.75, 0.6, "otGreenDark, line width=1.3pt")
    + courbe(F_PGF, -0.68, 6.3)
    + rf"  \fill[otOrange!90!black] (axis cs:2,{YI:.5f}) circle (2.4pt);" + "\n"
    + rf"  \node[inner sep=1.4pt, text=otOrange!80!black, anchor=south west] at (axis cs:2.05,{YI + 0.02:.5f}) {{$I$}};" + "\n"
    + noeud(2, -0.02, r"$2$", "north west", "otMuted", r", xshift=1.5pt, font=\otRegular\fontsize{9}{10}\selectfont")
    + noeud(0.64, 0.55, r"$T$", "west", "otGreenDark")
    + noeud(3.6, 0.17, r"$\mathcal{C}_f$", "south west")
    + noeud(1.1, -0.55, r"concave", "center", "otNavy", r", font=\otRegular\fontsize{9}{10}\selectfont")
    + noeud(4.2, -0.6, r"convexe", "center", "otNavy", r", font=\otRegular\fontsize{9}{10}\selectfont"))

# corrigé Q6 : construction des premiers termes (escalier)
U = [1.0]
for _ in range(4):
    U.append(f_num(U[-1]))
esc = ""
for k in range(2):
    a, b = U[k], U[k + 1]
    depart = 0 if k == 0 else a
    esc += rf"  \draw[otGreenDark, line width=0.9pt] (axis cs:{a:.5f},{depart:.5f}) -- (axis cs:{a:.5f},{b:.5f}) -- (axis cs:{b:.5f},{b:.5f});" + "\n"
for k in range(2):
    esc += rf"  \draw[guide] (axis cs:{U[k + 1]:.5f},{U[k + 1]:.5f}) -- (axis cs:{U[k + 1]:.5f},0);" + "\n"
pts = "".join(rf"  \fill[otGreenDark] (axis cs:{U[k]:.5f},0) circle (2.2pt);" + "\n" for k in range(3))
# u_1, u_2 sous l'axe (centrées) ; u_0 = 1 à gauche du trait vertical, au-dessus de l'axe
etq = "".join(noeud(f"{U[k]:.5f}", 0.0, f"$u_{k}$", "north", "otGreenDark", ", yshift=-2pt") for k in (1, 2))
FIGURES["ex4_escalier"] = axe(
    ZOOM.replace(r"xticklabels={$0{,}2$,$0{,}4$,$0{,}6$,$0{,}8$,$1$}", r"xticklabels={,,$0{,}6$,$0{,}8$,}"),
    courbe("x", 0, 1.08, "otMuted, line width=0.9pt")
    + courbe(F_PGF, 0, 1.08)
    + esc + pts + etq
    + noeud(1.0, 0.0, r"$u_0$", "north", "otGreenDark", ", yshift=-2pt")
    + noeud(0.83, 0.88, r"$y=x$", "south east", "otMuted")
    + noeud(1.02, 0.37, r"$\mathcal{C}_f$", "south"))

# corrigé Q10 : aire sous C_f (I) et aire entre T et C_f
FIGURES["ex4_aire"] = axe(
    ZOOM,
    r"  \addplot[fill=otNavy!14, draw=none, domain=0:1, samples=120] {x*exp(-x)} \closedcycle;" + "\n"
    + r"  \addplot[name path=t, draw=none, domain=0:1] {x};" + "\n"
    + r"  \addplot[name path=c, draw=none, domain=0:1, samples=120] {x*exp(-x)};" + "\n"
    + r"  \addplot[otGreen!32] fill between[of=t and c];" + "\n"
    + r"  \draw[otGreenDark, line width=0.7pt] (axis cs:1,0) -- (axis cs:1,1);" + "\n"
    + courbe("x", 0, 1.08, "otGreenDark, line width=1.3pt")
    + courbe(F_PGF, 0, 1.08)
    + noeud(0.71, 0.47, r"$\mathcal{A}$", "center", "otGreenDark")
    + noeud(0.74, 0.17, r"$I$", "center", "otNavy")
    + noeud(0.62, 0.69, r"$T$", "south east", "otGreenDark")
    + noeud(1.02, 0.37, r"$\mathcal{C}_f$", "south west"))

# ############################################################################
#                                   COURS
# ############################################################################
# Frise des 4 heures (sujet 4 + 4 + 4 + 6 points, 2 points de langue)
def frise():
    L = 7.0 / 240  # cm par minute
    police = r"\otRegular\fontsize{10.5}{12.5}\selectfont"
    blocs = [(0, 15, "otMuted!18", None), (15, 60, "otNavy!9", "Ex. 1\\\\4 pts"), (60, 105, "otNavy!9", "Ex. 2\\\\4 pts"),
             (105, 150, "otNavy!9", "Ex. 3\\\\4 pts"), (150, 225, "otNavy!15", "Ex. 4\\\\6 pts"), (225, 240, "otGreen!28", None)]
    s = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    for a, b, coul, txt in blocs:
        s.append(rf"\fill[{coul}] ({a * L:.3f},0) rectangle ({b * L:.3f},1.05);")
    for a, b, coul, txt in blocs:
        s.append(rf"\draw[white, line width=1.2pt] ({b * L:.3f},0) -- ({b * L:.3f},1.05);")
        if txt:
            s.append(rf"\node[frise, font={police}] at ({(a + b) / 2 * L:.3f},0.525) {{{txt}}};")
    s.append(rf"\draw[otNavy!60, line width=0.6pt] (0,0) rectangle ({240 * L:.3f},1.05);")
    # axe des heures sous la frise
    for m, t in ((0, "0"), (60, "1 h"), (120, "2 h"), (180, "3 h"), (240, "4 h")):
        s.append(rf"\draw[otMuted, line width=0.5pt] ({m * L:.3f},0) -- ({m * L:.3f},-0.12);")
        s.append(rf"\node[anchor=north, inner sep=1pt, text=otMuted, font={police}] at ({m * L:.3f},-0.16) {{{t}}};")
    s.append(rf"\draw[otMuted!80, line width=0.5pt] ({7.5 * L:.3f},1.1) -- ({7.5 * L:.3f},1.37);")
    s.append(rf"\node[anchor=south west, inner sep=1pt, frise, font={police}, text=otMuted] at ({0:.3f},1.39) {{Lecture (15 min)}};")
    s.append(rf"\draw[otGreenDark, line width=0.5pt] ({232.5 * L:.3f},1.1) -- ({232.5 * L:.3f},1.37);")
    s.append(rf"\node[anchor=south east, inner sep=1pt, frise, font={police}, text=otGreenDark] at ({240 * L:.3f},1.39) {{Relecture (15 min)}};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_frise"] = frise()

# Corollaire du théorème des valeurs intermédiaires
FIGURES["cours_tvi"] = axe(
    r"width=6.6cm, height=4.4cm, xmin=-0.3, xmax=5.2, ymin=-0.3, ymax=3.6, grid=none, "
    r"xtick={1,2.6,4.4}, xticklabels={$a$,$\alpha$,$b$}, ytick={0.6,1.7,3.05}, yticklabels={$f(a)$,$k$,$f(b)$}",
    r"  \draw[seuil] (axis cs:0,1.7) -- (axis cs:5.0,1.7);" + "\n"
    + r"  \draw[guide] (axis cs:1,0) -- (axis cs:1,0.6) -- (axis cs:0,0.6);" + "\n"
    + r"  \draw[guide] (axis cs:4.4,0) -- (axis cs:4.4,3.05) -- (axis cs:0,3.05);" + "\n"
    + r"  \draw[otGreenDark, line width=0.8pt, dash pattern=on 2.5pt off 1.6pt] (axis cs:2.6,0) -- (axis cs:2.6,1.7);" + "\n"
    + r"  \addplot[courbe, domain=1:4.4, samples=120] {0.6+2.45*((x-1)/3.4)^1.6};" + "\n"
    + r"  \pnt{1}{0.6} \pnt{4.4}{3.05}" + "\n"
    + r"  \pnt[otGreenDark]{2.6}{1.7}" + "\n"
    + noeud(2.3, 2.4, r"$\mathcal{C}_f$", "center"))

# Convexité : tangentes au-dessus / au-dessous, point d'inflexion
def g(x):
    return 0.25 * x ** 3 + 0.5 * x


def gp(x):
    return 0.75 * x ** 2 + 0.5


def tangente(a, d1, d2):
    return rf"  \addplot[otGreenDark, line width=1pt, domain={a + d1}:{a + d2}] {{{gp(a):.5f}*(x-({a}))+({g(a):.5f})}};" + "\n"


FIGURES["cours_convexite"] = axe(
    r"width=7.4cm, height=5cm, xmin=-2.6, xmax=2.6, ymin=-3.4, ymax=3.4, grid=none, xtick={-2,2}, ytick={-2,2}",
    tangente(-1.4, -0.95, 0.95) + tangente(1.4, -0.95, 0.95) + tangente(0, -1.15, 1.15)
    + courbe("0.25*x^3+0.5*x", -2.35, 2.35)
    + rf"  \pnt[otGreenDark]{{-1.4}}{{{g(-1.4):.5f}}} \pnt[otGreenDark]{{1.4}}{{{g(1.4):.5f}}}" + "\n"
    + r"  \fill[otOrange!90!black] (axis cs:0,0) circle (2.4pt);" + "\n"
    + r"  \node[inner sep=1.4pt, text=otOrange!80!black, anchor=north west] at (axis cs:0.12,-0.12) {$I$};" + "\n"
    + noeud(-1.55, 2.35, r"concave", "center", "otNavy", r", font=\otRegular\fontsize{9}{10}\selectfont")
    + noeud(-1.55, 2.08, r"courbe sous\\ses tangentes", "north", "otMuted", r", font=\otRegular\fontsize{8.5}{10}\selectfont, align=center")
    + noeud(1.45, -1.6, r"convexe", "center", "otNavy", r", font=\otRegular\fontsize{9}{10}\selectfont")
    + noeud(1.45, -1.83, r"courbe au-dessus\\de ses tangentes", "north", "otMuted", r", font=\otRegular\fontsize{8.5}{10}\selectfont, align=center")
    + noeud(1.75, 3.25, r"$\mathcal{C}_f$", "east"))

# Loi binomiale B(10 ; 0,3) : P(X <= 2) en vert
V10 = loi(10, 0.3)
FIGURES["cours_binomiale"] = rf"""
\begin{{tikzpicture}}
\begin{{axis}}[{BARRES}, width=5.9cm, height=4.1cm, bar width=7.5pt,
  xmin=-0.7, xmax=10.7, ymin=0, ymax=0.33, xtick={{0,2,4,6,8,10}}, minor xtick={{1,3,5,7,9}}, ytick={{0,0.1,0.2,0.3}},
  ylabel={{$P(X=k)$}}]
  \addplot[{BLEU}] coordinates {{{coords(V10, range(3, 11))}}};
  \addplot[{VERT}] coordinates {{{coords(V10, range(0, 3))}}};
  \node[anchor=north east,inner sep=1.4pt,font=\normalsize,text=otNavy] at (axis cs:10.6,0.328) {{$\mathcal{{B}}(10\,;0{{,}}3)$}};
  \node[anchor=north east,inner sep=1.4pt,font=\normalsize,text=otGreenDark] at (axis cs:10.6,0.292) {{$P(X\leqslant 2)\approx {virg(sum(V10[:3]))}$}};
\end{{axis}}
\end{{tikzpicture}}"""

# Projeté orthogonal d'un point sur un plan
f = Fig()
cadre = [(0, 0), (5.6, 0), (7.0, 2.3), (1.4, 2.3)]
f.fill(cadre, "planB")
f.ligne(cadre, "bordB", ferme=True)
Hp = (3.6, 1.05)
Mp = (3.6, 3.45)
f.ligne([Mp, Hp], "otGreenDark, line width=1pt, dash pattern=on 3pt off 2pt")
f.vec(Hp, (3.6, 2.1), "vecN")
f.dessus.append(r"\draw[otNavy, line width=0.6pt] (3.6,1.27) -- (3.82,1.31) -- (3.82,1.09);")
f.point(Hp, "ptV")
f.point(Mp, "ptN")
f.label(Hp, "$H$", style="lblV", pref=-135)
f.label(Mp, "$M$", style="lblN", pref=0)
f.label((3.6, 1.75), r"$\vec{n}$", h=0.5, style="lblN", pref=180, r=0.06, dirs=[170, 180, 190])
f.label((3.6, 2.75), r"$MH$", n=2, style="lblV", pref=0, r=0.08, dirs=[0, 10, -10])
f.texte((6.25, 0.38), r"$\mathcal{P}$", style="lblN")
FIGURES["cours_projete"] = f.tikz()
