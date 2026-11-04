# -*- coding: utf-8 -*-
"""Figures de la notion 239 (3e : grandeurs et mesures), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Solides en perspective cavalière (arêtes cachées en pointillés), cotes en gris,
tableau de conversion, graphiques distance-temps. Éléments de réponse en vert.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  solide/.style={otNavy,line width=.9pt,line join=round},
  cache/.style={otNavy,line width=.6pt,dash pattern=on 2.5pt off 2pt},
  face/.style={fill=otSky},
  hauteur/.style={otOrange!85!black,line width=.75pt,dash pattern=on 3pt off 2pt},
  ligne/.style={otNavy,line width=1.35pt,line join=round},
}
\pgfplotsset{gm/.style={grid=both, minor grid style={otRule!75,line width=0.35pt}, minor tick length=0pt}}
"""


def f(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------ solides
def pave(x0, w, h, d, la, lb, lc, titre=None):
    """Pavé : face avant w × h (cm), profondeur d (oblique). la = longueur (bas),
    lb = largeur (oblique, à droite), lc = hauteur (à gauche)."""
    dx, dy = 0.55 * d, 0.4 * d
    A, B, C, D = (x0, 0), (x0 + w, 0), (x0 + w, h), (x0, h)
    E, F, G, H = (x0 + dx, dy), (x0 + w + dx, dy), (x0 + w + dx, h + dy), (x0 + dx, h + dy)
    P = lambda p: f"({f(p[0])},{f(p[1])})"
    L = [rf"\fill[face] {P(A)} -- {P(B)} -- {P(F)} -- {P(G)} -- {P(H)} -- {P(D)} -- cycle;",
         rf"\draw[cache] {P(A)} -- {P(E)} -- {P(F)} {P(E)} -- {P(H)};",
         rf"\draw[solide] {P(A)} -- {P(B)} -- {P(C)} -- {P(D)} -- cycle;",
         rf"\draw[solide] {P(B)} -- {P(F)} -- {P(G)} -- {P(H)} -- {P(D)} {P(C)} -- {P(G)};",
         # cotes
         rf"\draw[cote] ({f(x0)},-0.3) -- ({f(x0+w)},-0.3);",
         rf"\node[anchor=north,text=otInk] at ({f(x0+w/2)},-0.36) {{{la}}};",
         rf"\draw[cote] ({f(x0+w+0.3)},-0.12) -- ({f(x0+w+dx+0.3)},{f(dy-0.12)});",
         rf"\node[anchor=north west,text=otInk] at ({f(x0+w+dx/2+0.38)},{f(dy/2-0.12)}) {{{lb}}};",
         rf"\draw[cote] ({f(x0-0.3)},0) -- ({f(x0-0.3)},{f(h)});",
         rf"\node[anchor=east,text=otInk] at ({f(x0-0.36)},{f(h/2)}) {{{lc}}};"]
    if titre:
        L.append(rf"\node[anchor=south,text=otNavy,font=\bfseries] at ({f(x0+(w+dx)/2)},{f(h+dy+0.25)}) {{{titre}}};")
    return L


def cylindre(xc, r, h, lr, lh, titre=None):
    ry = 0.32 * r
    L = [rf"\fill[face] ({f(xc-r)},0) -- ({f(xc-r)},{f(h)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- ({f(xc+r)},0) arc[start angle=0,end angle=-180,x radius={f(r)},y radius={f(ry)}] -- cycle;",
         rf"\fill[otSky!60!white] ({f(xc)},{f(h)}) ellipse[x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[solide] ({f(xc)},{f(h)}) ellipse[x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[solide] ({f(xc-r)},{f(h)}) -- ({f(xc-r)},0) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- ({f(xc+r)},{f(h)});",
         rf"\draw[cache] ({f(xc+r)},0) arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(ry)}];",
         # rayon (sur la base supérieure) et hauteur (cote à droite)
         rf"\draw[hauteur] ({f(xc)},{f(h)}) -- ({f(xc+r)},{f(h)});",
         rf"\fill[otNavy] ({f(xc)},{f(h)}) circle (1.6pt);",
         rf"\node[anchor=south,text=otInk] at ({f(xc+r/2)},{f(h+ry+0.05)}) {{{lr}}};",
         rf"\draw[cote] ({f(xc+r+0.32)},0) -- ({f(xc+r+0.32)},{f(h)});",
         rf"\node[anchor=west,text=otInk] at ({f(xc+r+0.4)},{f(h/2)}) {{{lh}}};"]
    if titre:
        L.append(rf"\node[anchor=south,text=otNavy,font=\bfseries] at ({f(xc)},{f(h+ry+0.6)}) {{{titre}}};")
    return L


def pyramide(x0, c, h, lc, lh, titre=None, dehors=False):
    """Pyramide à base carrée de côté c (cm), hauteur h."""
    d = c
    dx, dy = 0.5 * d, 0.36 * d
    A, B, C, D = (x0, 0), (x0 + c, 0), (x0 + c + dx, dy), (x0 + dx, dy)
    O = (x0 + (c + dx) / 2, dy / 2)
    S = (O[0], O[1] + h)
    P = lambda p: f"({f(p[0])},{f(p[1])})"
    L = [rf"\fill[face] {P(A)} -- {P(B)} -- {P(C)} -- {P(S)} -- cycle;",
         rf"\draw[cache] {P(A)} -- {P(D)} -- {P(C)} {P(D)} -- {P(S)};",
         rf"\draw[hauteur] {P(S)} -- {P(O)};",
         rf"\fill[otOrange!85!black] {P(O)} circle (1.5pt);",
         rf"\draw[solide] {P(A)} -- {P(B)} -- {P(C)} -- {P(S)} -- cycle {P(B)} -- {P(S)};",
         rf"\draw[cote] ({f(x0)},-0.3) -- ({f(x0+c)},-0.3);",
         rf"\node[anchor=north,text=otInk] at ({f(x0+c/2)},-0.36) {{{lc}}};",
         (rf"\node[anchor=west,text=otOrange!75!black] at ({f(x0+c+dx+0.15)},{f(O[1]+h*0.55)}) {{hauteur {lh}}};" if dehors else
          rf"\node[anchor=west,text=otOrange!75!black] at ({f(O[0]+0.08)},{f(O[1]+h*0.62)}) {{{lh}}};")]
    if titre:
        L.append(rf"\node[anchor=south,text=otNavy,font=\bfseries] at {P((S[0], S[1]+0.2))} {{{titre}}};")
    return L


def cone(xc, r, h, lr, lh, titre=None, dehors=False):
    ry = 0.32 * r
    P = lambda a, b: f"({f(a)},{f(b)})"
    L = [rf"\fill[face] {P(xc-r,0)} arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- {P(xc,h)} -- cycle;",
         rf"\draw[cache] {P(xc+r,0)} arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[hauteur] {P(xc,h)} -- {P(xc,0)};",
         rf"\draw[hauteur] {P(xc,0)} -- {P(xc+r,0)};",
         rf"\fill[otOrange!85!black] {P(xc,0)} circle (1.5pt);",
         rf"\draw[solide] {P(xc-r,0)} arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- {P(xc,h)} -- cycle;",
         rf"\node[anchor=north,text=otInk] at {P(xc+r/2,-ry-0.05)} {{{lr}}};",
         (rf"\node[anchor=west,text=otOrange!75!black] at {P(xc+r*0.55+0.15,h*0.5)} {{hauteur {lh}}};" if dehors else
          rf"\node[anchor=west,text=otOrange!75!black] at {P(xc+0.08,h*0.45)} {{{lh}}};")]
    if titre:
        L.append(rf"\node[anchor=south,text=otNavy,font=\bfseries] at {P(xc,h+0.2)} {{{titre}}};")
    return L


def boule(xc, r, lr, titre=None):
    yc = r
    P = lambda a, b: f"({f(a)},{f(b)})"
    L = [rf"\fill[face] {P(xc,yc)} circle ({f(r)});",
         rf"\draw[cache] {P(xc+r,yc)} arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(0.3*r)}];",
         rf"\draw[solide] {P(xc-r,yc)} arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(0.3*r)}];",
         rf"\draw[solide] {P(xc,yc)} circle ({f(r)});",
         rf"\draw[hauteur] {P(xc,yc)} -- {P(xc+r*0.866,yc+r*0.5)};",
         rf"\fill[otOrange!85!black] {P(xc,yc)} circle (1.5pt);",
         rf"\node[anchor=south east,text=otOrange!75!black] at {P(xc+r*0.38,yc+r*0.3)} {{{lr}}};"]
    if titre:
        L.append(rf"\node[anchor=south,text=otNavy,font=\bfseries] at {P(xc,2*r+0.2)} {{{titre}}};")
    return L


def tikz(L, opts=""):
    return "\\begin{tikzpicture}[" + opts + "]\n" + "\n".join(L) + "\n\\end{tikzpicture}"


FIGURES = {}

FIGURES["solides_droits"] = tikz(
    pave(0, 2.6, 1.6, 1.6, "$L$", "$\\ell$", "$h$", "Pavé droit")
    + cylindre(6.0, 0.95, 2.0, "$r$", "$h$", "Cylindre"))

FIGURES["solides_pointus"] = tikz(
    pyramide(0, 2.2, 2.4, "base $\\mathcal{B}$", "$h$", "Pyramide")
    + cone(4.9, 1.0, 2.6, "$r$", "$h$", "Cône")
    + boule(7.6, 1.0, "$r$", "Boule"))

# 2259 : pavé 6 cm × 4 cm × 2,5 cm et cylindre r = 3 cm, h = 10 cm
FIGURES["pave_cylindre_2259"] = tikz(
    pave(0, 2.7, 1.12, 1.8, "$6$ cm", "$4$ cm", "$2{,}5$ cm")
    + cylindre(5.7, 0.9, 3.0, "$3$ cm", "$10$ cm"))

# 2260 : pyramide base carrée 6 cm, hauteur 10 cm ; cône r = 3 cm, h = 8 cm
FIGURES["pyramide_cone_2260"] = tikz(
    pyramide(0, 2.4, 3.2, "$6$ cm", "$10$ cm", dehors=True)
    + cone(6.8, 1.15, 2.9, "$3$ cm", "$8$ cm", dehors=True))

# 2273 : piscine 8 m × 4 m × 1,5 m
FIGURES["piscine_2273"] = tikz(pave(0, 4.8, 0.9, 2.4, "$8$ m", "$4$ m", "$1{,}5$ m"))


# ------------------------------------------------------------ verre conique (2274)
def verre(corrige):
    R, H, k = 1.6, 4.0, 0.5           # rayon 4 cm, hauteur 12 cm, niveau 6 cm (échelle 0,4)
    ry = 0.3 * R
    P = lambda a, b: f"({f(a)},{f(b)})"
    r2, h2 = R * k, H * k
    L = [
        # liquide (petit cône)
        rf"\fill[otGreen!25] {P(-r2,h2)} -- {P(0,0)} -- {P(r2,h2)} arc[start angle=0,end angle=-180,x radius={f(r2)},y radius={f(0.3*r2)}] -- cycle;",
        rf"\fill[otGreen!40] {P(0,h2)} ellipse[x radius={f(r2)},y radius={f(0.3*r2)}];",
        rf"\draw[otGreenDark,line width=.7pt] {P(0,h2)} ellipse[x radius={f(r2)},y radius={f(0.3*r2)}];",
        # verre
        rf"\draw[solide] {P(0,H)} ellipse[x radius={f(R)},y radius={f(ry)}];",
        rf"\draw[solide] {P(-R,H)} -- {P(0,0)} -- {P(R,H)};",
        rf"\draw[hauteur] {P(0,H)} -- {P(R,H)};",
        rf"\fill[otNavy] {P(0,H)} circle (1.5pt);",
        rf"\node[anchor=south,text=otInk] at {P(R/2,H+ry+0.02)} {{$4$ cm}};",
        rf"\draw[cote] {P(R+0.5,0)} -- {P(R+0.5,H)};",
        rf"\node[anchor=west,text=otInk] at {P(R+0.58,H*0.72)} {{$12$ cm}};",
        rf"\draw[cote] {P(-R-0.4,0)} -- {P(-R-0.4,h2)};",
        rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] {P(-R-0.5,h2)} -- {P(-r2-0.1,h2)};",
        rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] {P(-R-0.5,0)} -- {P(-0.1,0)};",
        rf"\node[anchor=east,text=otInk] at {P(-R-0.48,h2/2)} {{$6$ cm}};",
    ]
    if corrige:
        L.append(rf"\draw[hauteur,otGreenDark] {P(0,h2)} -- {P(r2,h2)};")
        L.append(rf"\node[anchor=south,text=otGreenDark] at {P(r2/2,h2+0.3*r2+0.04)} {{$2$ cm}};")
    return tikz(L)


FIGURES["verre_enonce"] = verre(False)
FIGURES["verre_corrige"] = verre(True)


# ------------------------------------------------------------ tableau de conversion des aires
def tableau_aires():
    unites = ["dam²", "m²", "dm²", "cm²"]
    cw, hh = 1.6, 0.7                  # largeur d'une unité (2 colonnes), hauteur des lignes
    n = len(unites)
    L = []
    W = n * cw
    L.append(rf"\fill[otSky] (0,0) rectangle ({f(W)},{f(hh)});")
    L.append(rf"\draw[otNavy,line width=.8pt] (0,{f(-hh)}) rectangle ({f(W)},{f(hh)});")
    L.append(rf"\draw[otNavy,line width=.6pt] (0,0) -- ({f(W)},0);")
    for i, u in enumerate(unites):
        x = i * cw
        if i:
            L.append(rf"\draw[otNavy,line width=.6pt] ({f(x)},{f(-hh)}) -- ({f(x)},{f(hh)});")
        L.append(rf"\draw[otRule,line width=.5pt] ({f(x+cw/2)},{f(-hh)}) -- ({f(x+cw/2)},0);")
        L.append(rf"\node[text=otNavy,font=\otMedium\small] at ({f(x+cw/2)},{f(hh/2)}) {{{u}}};")
    # 0,42 m² = 4 200 cm² : chiffres 0 | 4 2 | 0 0 (colonne des unités m² = 2e demi-colonne de m²)
    def case(k):                       # k-ième demi-colonne (0 = 1re demi-colonne de km²)
        return k * cw / 2 + cw / 4
    m2 = 1 * 2 + 1                     # demi-colonne des unités de m²
    chiffres = [(m2, "0{,}", "otInk"), (m2 + 1, "4", "otInk"), (m2 + 2, "2", "otInk"),
                (m2 + 3, "0", "otGreenDark"), (m2 + 4, "0", "otGreenDark")]
    for k, c, col in chiffres:
        L.append(rf"\node[text={col}] at ({f(case(k))},{f(-hh/2)}) {{${c}$}};")
    L.append(r"\node[anchor=north,text=otInk,align=center] at (" + f(W / 2) + "," + f(-hh - 0.12) + r") {$0{,}42$ m² $= 4\,200$ cm²\\{\small deux colonnes par unité d'aire}};")
    return tikz(L)


FIGURES["tableau_aires"] = tableau_aires()


# ------------------------------------------------------------ graphiques distance-temps
def graphe_vitesse_cours():
    return r"""\begin{tikzpicture}
\begin{axis}[otWeb, gm, width=7cm, height=5.2cm, xmin=0, xmax=2.7, ymin=0, ymax=250,
  xtick={0.5,1,1.5,2,2.5}, xticklabels={$0{,}5$,$1$,$1{,}5$,$2$,$2{,}5$}, ytick={50,100,150,200},
  xlabel={$t$ (h)}, ylabel={$d$ (km)}]
  \addplot[courbe, domain=0:2.5] {90*x};
  \draw[guide] (axis cs:2,0) -- (axis cs:2,180) -- (axis cs:0,180);
  \fill[otGreenDark] (axis cs:2,180) circle (2.1pt);
  \node[note,text=otGreenDark,anchor=north west,align=left] at (axis cs:2.05,170) {$2$ h $\to 180$ km\\$v = 90$ km/h};
\end{axis}
\end{tikzpicture}"""


FIGURES["vitesse_cours"] = graphe_vitesse_cours()

# 2266 : trajet en voiture (0;0) (1;80) (1,5;80) (3;200)
P66 = (r"width=7.4cm, height=5.4cm, xmin=0, xmax=3.3, ymin=0, ymax=268, "
       r"xtick={0.5,1,1.5,2,2.5,3}, xticklabels={$0{,}5$,$1$,$1{,}5$,$2$,$2{,}5$,$3$}, ytick={20,40,60,80,100,120,140,160,180,200,220,240}, "
       r"yticklabels={,$40$,,$80$,,$120$,,$160$,,$200$,,$240$}, xlabel={$t$ (h)}, ylabel={$d$ (km)}")
B66 = r"""
  \draw[ligne] (axis cs:0,0) -- (axis cs:1,90) -- (axis cs:1.5,90) -- (axis cs:3,240);
  \fill[otNavy] (axis cs:0,0) circle (2.1pt); \fill[otNavy] (axis cs:1,90) circle (2.1pt);
  \fill[otNavy] (axis cs:1.5,90) circle (2.1pt); \fill[otNavy] (axis cs:3,240) circle (2.1pt);
"""
FIGURES["trajet_enonce"] = r"\begin{tikzpicture}" + "\n" + r"\begin{axis}[otWeb, gm, " + P66 + "]\n" + B66 + "\\end{axis}\n\\end{tikzpicture}"
FIGURES["trajet_corrige"] = r"\begin{tikzpicture}" + "\n" + r"\begin{axis}[otWeb, gm, " + P66 + "]\n" + B66 + r"""
  \node[note,text=otGreenDark,anchor=west] at (axis cs:0.55,30) {$90$ km/h};
  \node[note,text=otGreenDark,anchor=south] at (axis cs:1.25,95) {arrêt};
  \node[note,text=otGreenDark,anchor=west] at (axis cs:2.3,140) {$100$ km/h};
\end{axis}
\end{tikzpicture}"""
