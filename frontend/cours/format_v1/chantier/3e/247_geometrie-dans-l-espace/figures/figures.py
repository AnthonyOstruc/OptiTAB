# -*- coding: utf-8 -*-
"""Figures de la notion 247 (3e : géométrie dans l'espace), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Perspective cavalière (angle 40°, coefficient 0,6), arêtes cachées en pointillés,
hauteurs en orange, éléments de réponse (sections, longueurs cherchées) en vert.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  solide/.style={otNavy,line width=.9pt,line join=round},
  cache/.style={otNavy,line width=.6pt,dash pattern=on 2.5pt off 2pt},
  face/.style={fill=otSky},
  hauteur/.style={otOrange!85!black,line width=.75pt,dash pattern=on 3pt off 2pt},
  rep/.style={otGreenDark,line width=1.2pt,line join=round},
  repc/.style={otGreenDark,line width=1pt,dash pattern=on 3pt off 2pt},
  donnee/.style={otOrange!85!black,line width=1.1pt},
  donneec/.style={otOrange!85!black,line width=1pt,dash pattern=on 3pt off 2pt},
}
"""

K, ALPHA = 0.6, math.radians(40)
CX, CY = K * math.cos(ALPHA), K * math.sin(ALPHA)


def f(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


def P(x, y, z, s=1.0):
    """Projection cavalière d'un point (x : largeur, y : profondeur, z : hauteur)."""
    return f"({f(s * (x + CX * y))},{f(s * (z + CY * y))})"


def Q(p):
    return f"({f(p[0])},{f(p[1])})"


def tikz(L, opts=""):
    return "\\begin{tikzpicture}[" + opts + "]\n" + "\n".join(L) + "\n\\end{tikzpicture}"


def lab(pt, txt, anchor, color="otInk"):
    return rf"\node[anchor={anchor},text={color},inner sep=2pt] at {pt} {{{txt}}};"


# ------------------------------------------------------------ pavé nommé ABCDEFGH
# A(0,0,0) B(L,0,0) C(L,0,H) D(0,0,H) E(0,W,0) F(L,W,0) G(L,W,H) H(0,W,H) ; E caché.
def pave_nomme(L, W, H, s=1.0, noms=True, cotes=None, eau=None):
    S = {"A": (0, 0, 0), "B": (L, 0, 0), "C": (L, 0, H), "D": (0, 0, H),
         "E": (0, W, 0), "F": (L, W, 0), "G": (L, W, H), "H": (0, W, H)}
    p = {k: P(*v, s=s) for k, v in S.items()}
    out = [rf"\fill[face] {p['A']} -- {p['B']} -- {p['F']} -- {p['G']} -- {p['H']} -- {p['D']} -- cycle;"]
    if eau is not None:
        e = eau
        out.append(rf"\fill[otSky!40!otGreen!30] {P(0,0,0,s)} -- {P(L,0,0,s)} -- {P(L,W,0,s)} -- {P(L,W,e,s)} -- {P(0,W,e,s)} -- {P(0,0,e,s)} -- cycle;")
        out.append(rf"\draw[otGreenDark,line width=.6pt] {P(0,0,e,s)} -- {P(L,0,e,s)} -- {P(L,W,e,s)};")
        out.append(rf"\draw[otGreenDark,line width=.5pt,dash pattern=on 2pt off 1.5pt] {P(L,W,e,s)} -- {P(0,W,e,s)} -- {P(0,0,e,s)};")
    out += [rf"\draw[cache] {p['A']} -- {p['E']} -- {p['F']} {p['E']} -- {p['H']};",
            rf"\draw[solide] {p['A']} -- {p['B']} -- {p['C']} -- {p['D']} -- cycle;",
            rf"\draw[solide] {p['B']} -- {p['F']} -- {p['G']} -- {p['H']} -- {p['D']} {p['C']} -- {p['G']};"]
    if noms:
        anc = {"A": "north east", "B": "north west", "C": "north west", "D": "east",
               "E": "north west", "F": "west", "G": "south west", "H": "south east"}
        if cotes and "BF" in cotes:
            anc["F"] = "south west"
        for k, a in anc.items():
            out.append(lab(p[k], f"${k}$", a))
    if cotes:
        if "AB" in cotes:
            out.append(rf"\node[anchor=north,text=otInk] at {P(L/2,0,0,s)} [yshift=-{'11' if noms else '2'}pt] {{{cotes['AB']}}};")
        if "BF" in cotes:
            out.append(rf"\node[anchor=north west,text=otInk] at {P(L,W/2,0,s)} [xshift=1pt] {{{cotes['BF']}}};")
        if "FG" in cotes:
            out.append(rf"\node[anchor=west,text=otInk] at {P(L,W,H/2,s)} [xshift=2pt] {{{cotes['FG']}}};")
        if "AD" in cotes:
            out.append(rf"\node[anchor=east,text=otInk] at {P(0,0,H/2,s)} [xshift=-2pt] {{{cotes['AD']}}};")
    return out


# ------------------------------------------------------------ solides du cours (repris de la notion 239)
def pave(x0, w, h, d, la, lb, lc, titre=None):
    dx, dy = 0.55 * d, 0.4 * d
    A, B, C, D = (x0, 0), (x0 + w, 0), (x0 + w, h), (x0, h)
    E, F, G, H = (x0 + dx, dy), (x0 + w + dx, dy), (x0 + w + dx, h + dy), (x0 + dx, h + dy)
    L = [rf"\fill[face] {Q(A)} -- {Q(B)} -- {Q(F)} -- {Q(G)} -- {Q(H)} -- {Q(D)} -- cycle;",
         rf"\draw[cache] {Q(A)} -- {Q(E)} -- {Q(F)} {Q(E)} -- {Q(H)};",
         rf"\draw[solide] {Q(A)} -- {Q(B)} -- {Q(C)} -- {Q(D)} -- cycle;",
         rf"\draw[solide] {Q(B)} -- {Q(F)} -- {Q(G)} -- {Q(H)} -- {Q(D)} {Q(C)} -- {Q(G)};",
         rf"\node[anchor=north,text=otInk] at ({f(x0+w/2)},-0.05) {{{la}}};",
         rf"\node[anchor=north west,text=otInk] at ({f(x0+w+dx/2)},{f(dy/2)}) {{{lb}}};",
         rf"\node[anchor=east,text=otInk] at ({f(x0-0.05)},{f(h/2)}) {{{lc}}};"]
    if titre:
        L.append(rf"\node[anchor=south,text=otNavy,font=\bfseries] at ({f(x0+(w+dx)/2)},{f(h+dy+0.25)}) {{{titre}}};")
    return L


def cylindre(xc, r, h, lr, lh, titre=None, y0=0.0, cote=True):
    ry = 0.32 * r
    a, b = y0, y0 + h
    L = [rf"\fill[face] ({f(xc-r)},{f(a)}) -- ({f(xc-r)},{f(b)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- ({f(xc+r)},{f(a)}) arc[start angle=0,end angle=-180,x radius={f(r)},y radius={f(ry)}] -- cycle;",
         rf"\fill[otSky!60!white] ({f(xc)},{f(b)}) ellipse[x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[solide] ({f(xc)},{f(b)}) ellipse[x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[solide] ({f(xc-r)},{f(b)}) -- ({f(xc-r)},{f(a)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- ({f(xc+r)},{f(b)});",
         rf"\draw[cache] ({f(xc+r)},{f(a)}) arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(ry)}];"]
    if lr:
        L += [rf"\draw[hauteur] ({f(xc)},{f(b)}) -- ({f(xc+r)},{f(b)});",
              rf"\fill[otNavy] ({f(xc)},{f(b)}) circle (1.6pt);",
              rf"\node[anchor=south,text=otInk] at ({f(xc+r/2)},{f(b+ry+0.05)}) {{{lr}}};"]
    if lh and cote:
        L += [rf"\draw[cote] ({f(xc+r+0.32)},{f(a)}) -- ({f(xc+r+0.32)},{f(b)});",
              rf"\node[anchor=west,text=otInk] at ({f(xc+r+0.4)},{f((a+b)/2)}) {{{lh}}};"]
    if titre:
        L.append(rf"\node[anchor=south,text=otNavy,font=\bfseries] at ({f(xc)},{f(b+ry+0.6)}) {{{titre}}};")
    return L


def cone(xc, r, h, lr, lh, titre=None, diametre=False, yh=0.42):
    ry = 0.32 * r
    L = [rf"\fill[face] ({f(xc-r)},0) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- ({f(xc)},{f(h)}) -- cycle;",
         rf"\draw[cache] ({f(xc+r)},0) arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[hauteur] ({f(xc)},{f(h)}) -- ({f(xc)},0);"]
    if diametre:
        L.append(rf"\draw[hauteur] ({f(xc-r)},0) -- ({f(xc+r)},0);")
    else:
        L.append(rf"\draw[hauteur] ({f(xc)},0) -- ({f(xc+r)},0);")
    L += [rf"\fill[otOrange!85!black] ({f(xc)},0) circle (1.5pt);",
          rf"\draw[solide] ({f(xc-r)},0) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- ({f(xc)},{f(h)}) -- cycle;"]
    if lr:
        L.append(rf"\node[anchor=north,text=otInk] at ({f(xc + (0 if diametre else r/2))},{f(-ry-0.05)}) {{{lr}}};")
    if lh:
        L.append(rf"\node[anchor=west,text=otOrange!75!black] at ({f(xc+0.06)},{f(h*yh)}) {{{lh}}};")
    if titre:
        L.append(rf"\node[anchor=south,text=otNavy,font=\bfseries] at ({f(xc)},{f(h+0.2)}) {{{titre}}};")
    return L


def boule(xc, r, lr, titre=None, yc=None, centre=None):
    yc = r if yc is None else yc
    L = [rf"\fill[face] ({f(xc)},{f(yc)}) circle ({f(r)});",
         rf"\draw[cache] ({f(xc+r)},{f(yc)}) arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(0.3*r)}];",
         rf"\draw[solide] ({f(xc-r)},{f(yc)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(0.3*r)}];",
         rf"\draw[solide] ({f(xc)},{f(yc)}) circle ({f(r)});",
         rf"\draw[hauteur] ({f(xc)},{f(yc)}) -- ({f(xc+r*0.866)},{f(yc+r*0.5)});",
         rf"\fill[otOrange!85!black] ({f(xc)},{f(yc)}) circle (1.5pt);",
         rf"\node[anchor=south east,text=otOrange!75!black] at ({f(xc+r*0.42)},{f(yc+r*0.26)}) {{{lr}}};"]
    if centre:
        L.append(rf"\node[anchor=north,text=otInk] at ({f(xc)},{f(yc-0.05)}) [yshift=-1pt,xshift=-4pt] {{{centre}}};")
    if titre:
        L.append(rf"\node[anchor=south,text=otNavy,font=\bfseries] at ({f(xc)},{f(yc+r+0.2)}) {{{titre}}};")
    return L


FIGURES = {}

FIGURES["solides_droits"] = tikz(
    pave(0, 2.6, 1.6, 1.6, "$L$", "$\\ell$", "$h$", "Pavé droit")
    + cylindre(6.0, 0.95, 2.0, "$r$", "$h$", "Cylindre"))

FIGURES["solides_pointus"] = tikz(
    [r"\fill[face] (0,0) -- (2.2,0) -- (3.3,0.79) -- (1.65,3.2) -- cycle;",
       r"\draw[cache] (0,0) -- (1.1,0.79) -- (3.3,0.79) (1.1,0.79) -- (1.65,3.2);",
       r"\draw[hauteur] (1.65,3.2) -- (1.65,0.395);",
       r"\fill[otOrange!85!black] (1.65,0.395) circle (1.5pt);",
       r"\draw[solide] (0,0) -- (2.2,0) -- (3.3,0.79) -- (1.65,3.2) -- cycle (2.2,0) -- (1.65,3.2);",
       r"\node[anchor=north,text=otInk] at (1.1,-0.05) {base $\mathcal{B}$};",
       r"\node[anchor=east,text=otOrange!75!black] at (1.6,1.45) {$h$};",
       r"\node[anchor=south,text=otNavy,font=\bfseries] at (1.65,3.4) {Pyramide};"]
    + cone(4.9, 1.0, 2.6, "$r$", "$h$", "Cône")
    + boule(7.6, 1.0, "$r$", "Boule"))


# ------------------------------------------------------------ 2422 : pavé 8 × 5 × 3
FIGURES["pave_2422"] = tikz(pave_nomme(8, 5, 3, s=0.55, cotes={"AB": "$8$ cm", "BF": "$5$ cm", "FG": "$3$ cm"}))

# ------------------------------------------------------------ 2423 : cylindre r = 3, h = 10
FIGURES["cylindre_2423"] = tikz(cylindre(0, 1.2, 4.0, "$3$ cm", "$10$ cm"))

# ------------------------------------------------------------ 2425 : cône de diamètre 8, hauteur 9
FIGURES["cone_2425"] = tikz(cone(0, 1.6, 3.6, "$8$ cm", "$9$ cm", diametre=True))

# ------------------------------------------------------------ 2426 : boule de rayon 3
FIGURES["boule_2426"] = tikz(boule(0, 1.6, "$3$ cm", centre="$O$"))


# ------------------------------------------------------------ pyramide SABCD
def pyramide_nommee(c, h, s, cotes=True, corrige=False, louvre=False):
    A, B, C, D = (0, 0, 0), (c, 0, 0), (c, c, 0), (0, c, 0)
    O, S, I = (c / 2, c / 2, 0), (c / 2, c / 2, h), (c / 2, 0, 0)
    p = {k: P(*v, s=s) for k, v in dict(A=A, B=B, C=C, D=D, O=O, S=S, I=I).items()}
    L = [rf"\fill[face] {p['A']} -- {p['B']} -- {p['C']} -- {p['S']} -- cycle;",
         rf"\draw[cache] {p['A']} -- {p['D']} -- {p['C']} {p['D']} -- {p['S']};",
         rf"\draw[hauteur] {p['S']} -- {p['O']};"]
    if louvre:
        L.append(rf"\draw[cache] {p['O']} -- {p['I']};")
        if corrige:
            L += [rf"\draw[repc] {p['O']} -- {p['I']};",
                  rf"\draw[repc] {p['S']} -- {p['O']};"]
    L += [rf"\fill[otOrange!85!black] {p['O']} circle (1.5pt);",
          rf"\draw[solide] {p['A']} -- {p['B']} -- {p['C']} -- {p['S']} -- cycle {p['B']} -- {p['S']};"]
    if louvre:
        L.append(rf"\draw[{'rep' if corrige else 'solide'}] {p['S']} -- {p['I']};")
        L.append(rf"\fill[otNavy] {p['I']} circle (1.4pt);")
    L += [lab(p["A"], "$A$", "north east"), lab(p["B"], "$B$", "north west"),
          lab(p["C"], "$C$", "west"), lab(p["D"], "$D$", "east"),
          lab(p["S"], "$S$", "south"), lab(p["O"], "$O$", "north", "otInk")]
    if louvre:
        L.append(lab(p["I"], "$I$", "north"))
    sx, sy = s * (c / 2 + CX * c / 2), s * (h + CY * c / 2)
    if cotes:
        L.append(rf"\node[anchor=north,text=otInk] at {P(c*0.78,0,0,s)} [yshift=-1pt] {{{cotes[0]}}};")
        L.append(rf"\node[anchor=south west,text=otOrange!75!black] at ({f(sx+0.45)},{f(sy-0.15)}) {{{cotes[1]}}};")
    if corrige and louvre:
        ox, oy = s * (c / 2 + CX * c / 2), s * (CY * c / 2)
        ix, iy = s * (c / 2), 0.0
        n = math.hypot(ix - ox, iy - oy)
        ux, uy = 0.2 * (ix - ox) / n, 0.2 * (iy - oy) / n
        L.append(rf"\draw[otGreenDark,line width=.6pt] ({f(ox)},{f(oy+0.2)}) -- ({f(ox+ux)},{f(oy+0.2+uy)}) -- ({f(ox+ux)},{f(oy+uy)});")
        L.append(rf"\node[anchor=south east,text=otGreenDark] at ({f(sx-0.45)},{f(sy-0.15)}) {{$SI \approx 27{{,}}8$ m}};")
    return L


FIGURES["pyramide_2424"] = tikz(pyramide_nommee(6, 9, 0.42, cotes=("$6$ cm", "$SO = 9$ cm")))
FIGURES["louvre_enonce"] = tikz(pyramide_nommee(35, 21.6, 0.12, cotes=("$35$ m", "$SO = 21{,}6$ m"), louvre=True))
FIGURES["louvre_corrige"] = tikz(pyramide_nommee(35, 21.6, 0.12, cotes=("$35$ m", "$SO = 21{,}6$ m"), louvre=True, corrige=True))


# ------------------------------------------------------------ nouveau-1 : pyramide 9 × 9, hauteur 12, coupée à SO' = 4
def pyramide_coupee(corrige):
    c, h, s, k = 9, 12, 0.36, 1 / 3
    A, B, C, D = (0, 0, 0), (c, 0, 0), (c, c, 0), (0, c, 0)
    O, S = (c / 2, c / 2, 0), (c / 2, c / 2, h)
    m = lambda X: tuple(S[i] + k * (X[i] - S[i]) for i in range(3))
    p = {n: P(*X, s=s) for n, X in dict(A=A, B=B, C=C, D=D, O=O, S=S).items()}
    q = {n: P(*m(X), s=s) for n, X in dict(A=A, B=B, C=C, D=D, O=O).items()}
    st, stc = ("rep", "repc") if corrige else ("donnee", "donneec")
    L = [rf"\fill[face] {p['A']} -- {p['B']} -- {p['C']} -- {p['S']} -- cycle;"]
    if corrige:
        L.append(rf"\fill[otGreen!30] {q['A']} -- {q['B']} -- {q['C']} -- {q['D']} -- cycle;")
    L += [rf"\draw[cache] {p['A']} -- {p['D']} -- {p['C']} {p['D']} -- {p['S']};",
          rf"\draw[hauteur] {p['S']} -- {p['O']};",
          rf"\fill[otOrange!85!black] {p['O']} circle (1.5pt);",
          rf"\fill[otOrange!85!black] {q['O']} circle (1.3pt);",
          rf"\draw[solide] {p['A']} -- {p['B']} -- {p['C']} -- {p['S']} -- cycle {p['B']} -- {p['S']};",
          rf"\draw[{st}] {q['D']} -- {q['A']} -- {q['B']} -- {q['C']};", rf"\draw[{stc}] {q['C']} -- {q['D']};",
          lab(p["A"], "$A$", "north east"), lab(p["B"], "$B$", "north west"),
          lab(p["C"], "$C$", "west"), lab(p["D"], "$D$", "south east"),
          lab(p["S"], "$S$", "south"), lab(p["O"], "$O$", "north"),
          lab(q["A"], "$A'$", "east"), lab(q["B"], "$B'$", "west"),
          rf"\node[anchor=north,text=otInk] at {P(c*0.5,0,0,s)} [yshift=-1pt] {{$9$ cm}};"]
    sx, sy = s * (c / 2 + CX * c / 2), s * (h + CY * c / 2)
    L.append(rf"\node[anchor=south west,text=otOrange!75!black,align=left] at ({f(sx+0.45)},{f(sy-0.55)}) {{$SO = 12$ cm\\$SO' = 4$ cm}};")
    if corrige:
        L.append(rf"\node[anchor=south east,text=otGreenDark,align=right] at ({f(sx-0.45)},{f(sy-0.55)}) {{$k = \frac{{1}}{{3}}$\\$A'B' = 3$ cm}};")
    return tikz(L)


FIGURES["pyramide_coupee_enonce"] = pyramide_coupee(False)
FIGURES["pyramide_coupee_corrige"] = pyramide_coupee(True)


# ------------------------------------------------------------ 2427 : patron du cube
def patron_cube(corrige):
    a = 1.1
    cases = {"B": (1, 3), "C": (1, 2), "D": (1, 1), "E": (1, 0), "A": (0, 2), "F": (2, 2)}
    coul = {"B": "otGreen!35", "D": "otGreen!35", "C": "otOrange!30", "E": "otOrange!30",
            "A": "otSky", "F": "otSky"}
    L = []
    for k, (i, j) in cases.items():
        fill = coul[k] if corrige else "otSky"
        L.append(rf"\fill[{fill}] ({f(i*a)},{f(j*a)}) rectangle ({f((i+1)*a)},{f((j+1)*a)});")
    for k, (i, j) in cases.items():
        L.append(rf"\draw[solide] ({f(i*a)},{f(j*a)}) rectangle ({f((i+1)*a)},{f((j+1)*a)});")
        L.append(rf"\node[text=otNavy,font=\bfseries\large] at ({f((i+.5)*a)},{f((j+.5)*a)}) {{{k}}};")
    L.append(rf"\node[anchor=west,text=otInk] at ({f(2*a)},{f(3.5*a)}) [xshift=2pt] {{côté $2$ cm}};")
    return tikz(L)


FIGURES["patron_cube_enonce"] = patron_cube(False)
FIGURES["patron_cube_corrige"] = patron_cube(True)


# ------------------------------------------------------------ 2428 : patron du cylindre r = 2, h = 5
def patron_cylindre(corrige):
    s = 0.42
    r, h = 2 * s, 5 * s
    Lr = 2 * math.pi * 2 * s
    L = [rf"\fill[face] (0,0) rectangle ({f(Lr)},{f(h)});",
         rf"\draw[solide] (0,0) rectangle ({f(Lr)},{f(h)});",
         rf"\fill[face] ({f(Lr/2)},{f(h+r)}) circle ({f(r)});",
         rf"\draw[solide] ({f(Lr/2)},{f(h+r)}) circle ({f(r)});",
         rf"\fill[face] ({f(Lr/2)},{f(-r)}) circle ({f(r)});",
         rf"\draw[solide] ({f(Lr/2)},{f(-r)}) circle ({f(r)});",
         rf"\draw[hauteur] ({f(Lr/2)},{f(h+r)}) -- ({f(Lr/2+r)},{f(h+r)});",
         rf"\fill[otNavy] ({f(Lr/2)},{f(h+r)}) circle (1.4pt);",
         rf"\node[anchor=south,text=otInk] at ({f(Lr/2+r/2)},{f(h+r)}) {{$2$ cm}};",
         rf"\draw[cote] ({f(Lr+0.3)},0) -- ({f(Lr+0.3)},{f(h)});",
         rf"\node[anchor=west,text=otInk] at ({f(Lr+0.38)},{f(h/2)}) {{$5$ cm}};",
         rf"\draw[otMuted!70,line width=.4pt] (0,-0.08) -- (0,{f(-2*r-0.4)}) ({f(Lr)},-0.08) -- ({f(Lr)},{f(-2*r-0.4)});",
         rf"\draw[cote] (0,{f(-2*r-0.3)}) -- ({f(Lr)},{f(-2*r-0.3)});"]
    if corrige:
        L.append(rf"\draw[rep] (0,0) -- ({f(Lr)},0);")
        L.append(rf"\node[anchor=north,text=otGreenDark] at ({f(Lr/2)},{f(-2*r-0.38)}) {{$L = 4\pi \approx 12{{,}}6$ cm}};")
    else:
        L.append(rf"\node[anchor=north,text=otInk] at ({f(Lr/2)},{f(-2*r-0.38)}) {{$L$}};")
    return tikz(L)


FIGURES["patron_cylindre_enonce"] = patron_cylindre(False)
FIGURES["patron_cylindre_corrige"] = patron_cylindre(True)


# ------------------------------------------------------------ 2429 : section d'un pavé 8 × 5 × 6 à 2 cm de la base
def section_pave(corrige):
    s, L_, W, H, z = 0.5, 8, 5, 6, 2
    out = pave_nomme(L_, W, H, s=s, cotes={"AB": "$8$ cm", "BF": "$5$ cm", "FG": "$6$ cm"})
    I, J, K_, Lp = P(0, 0, z, s), P(L_, 0, z, s), P(L_, W, z, s), P(0, W, z, s)
    st, stc = ("rep", "repc") if corrige else ("donnee", "donneec")
    if corrige:
        out.insert(1, rf"\fill[otGreen!30] {I} -- {J} -- {K_} -- {Lp} -- cycle;")
    out += [rf"\draw[{st}] {Lp} -- {I} -- {J} -- {K_};", rf"\draw[{stc}] {K_} -- {Lp};",
            lab(I, "$I$", "east"), lab(J, "$J$", "north west"), lab(K_, "$K$", "west"), lab(Lp, "$L$", "south east"),
            rf"\draw[cote] {P(-1.4,0,0,s)} -- {P(-1.4,0,z,s)};",
            rf"\draw[otMuted!70,line width=.4pt] {P(-0.8,0,0,s)} -- {P(-1.6,0,0,s)} {P(-0.8,0,z,s)} -- {P(-1.6,0,z,s)};",
            rf"\node[anchor=east,text=otInk] at {P(-1.5,0,z/2,s)} {{$2$ cm}};"]
    if corrige:
        out.append(rf"\node[text=otGreenDark,font=\small] at {P(L_*0.62,W/2,z,s)} {{$40$ cm²}};")
    return tikz(out)


FIGURES["section_pave_enonce"] = section_pave(False)
FIGURES["section_pave_corrige"] = section_pave(True)


# ------------------------------------------------------------ repère dans un pavé
def repere_pave(L_, W, H, pt, nom, s=0.62, axes=("x", "y", "z")):
    out = [rf"\fill[face] {P(0,0,0,s)} -- {P(L_,0,0,s)} -- {P(L_,W,0,s)} -- {P(L_,W,H,s)} -- {P(0,W,H,s)} -- {P(0,0,H,s)} -- cycle;"]
    # quadrillage léger de la base
    for i in range(1, L_):
        out.append(rf"\draw[otRule,line width=.4pt] {P(i,0,0,s)} -- {P(i,W,0,s)};")
    for j in range(1, W):
        out.append(rf"\draw[otRule,line width=.4pt] {P(0,j,0,s)} -- {P(L_,j,0,s)};")
    out += [rf"\draw[solide] {P(L_,0,0,s)} -- {P(L_,0,H,s)} -- {P(0,0,H,s)} (0,0) -- {P(L_,0,0,s)} -- {P(L_,W,0,s)} -- {P(L_,W,H,s)} -- {P(0,W,H,s)} -- {P(0,0,H,s)} {P(L_,0,H,s)} -- {P(L_,W,H,s)};",
            rf"\draw[cache] {P(0,W,0,s)} -- {P(L_,W,0,s)} {P(0,W,0,s)} -- {P(0,W,H,s)};",
            rf"\draw[solide,-{{Stealth[length=2mm]}}] (0,0) -- {P(L_+1.4,0,0,s)};",
            rf"\draw[solide,-{{Stealth[length=2mm]}}] (0,0) -- {P(0,W+1.6,0,s)};",
            rf"\draw[solide,-{{Stealth[length=2mm]}}] (0,0) -- {P(0,0,H+1.3,s)};",
            lab(P(L_ + 1.4, 0, 0, s), f"${axes[0]}$", "west"),
            lab(P(0, W + 1.6, 0, s), f"${axes[1]}$", "south east"),
            lab(P(0, 0, H + 1.3, s), f"${axes[2]}$", "east"),
            lab("(0,0)", "$O$", "north east")]
    for i in range(1, L_ + 1):
        out.append(rf"\node[anchor=north,text=otMuted,font=\otRegular\footnotesize] at {P(i,0,0,s)} {{{i}}};")
    for j in range(1, W + 1):
        out.append(rf"\node[anchor=south east,text=otMuted,font=\otRegular\footnotesize,inner sep=1.5pt] at {P(0,j,0,s)} {{{j}}};")
    for k in range(1, H + 1):
        out.append(rf"\node[anchor=east,text=otMuted,font=\otRegular\footnotesize] at {P(0,0,k,s)} {{{k}}};")
    x, y, z = pt
    out += [rf"\draw[otGreenDark,line width=.6pt,dash pattern=on 2pt off 1.5pt] {P(x,0,0,s)} -- {P(x,y,0,s)} -- {P(0,y,0,s)};",
            rf"\draw[otGreenDark,line width=.7pt,dash pattern=on 2pt off 1.5pt] {P(x,y,0,s)} -- {P(x,y,z,s)};",
            rf"\fill[otGreenDark] {P(x,y,0,s)} circle (1.3pt);",
            rf"\fill[otNavy] {P(x,y,z,s)} circle (1.8pt);",
            lab(P(x, y, z, s), nom, "south west", "otNavy")]
    return tikz(out)


FIGURES["repere_cours"] = repere_pave(5, 3, 4, (3, 2, 2), "$M$")
FIGURES["repere_2430"] = repere_pave(6, 4, 3, (2, 3, 1), "$P$")


# ------------------------------------------------------------ sphère et globe (projection orthogonale)
def proj_sphere(lat, lon, R, lon0=-25.0, el=18.0):
    """Point (lat, lon en degrés) → (x, y, profondeur). lon0 = longitude face à l'observateur."""
    la, lo = math.radians(lat), math.radians(lon - lon0)
    x = math.cos(la) * math.sin(lo)
    y = math.sin(la)
    z = math.cos(la) * math.cos(lo)
    e = math.radians(el)
    y2 = y * math.cos(e) - z * math.sin(e)
    z2 = y * math.sin(e) + z * math.cos(e)
    return R * x, R * y2, z2


def courbe(points, R, epais="solide", cache="cache"):
    """Trace une courbe sur la sphère : partie visible en trait plein, cachée en pointillés."""
    out, seg, vis = [], [], None
    for (x, y, d) in points:
        v = d >= 0
        if vis is None or v == vis:
            seg.append((x, y))
        else:
            seg.append((x, y))
            out.append((vis, seg))
            seg = [(x, y)]
        vis = v
    out.append((vis, seg))
    L = []
    for v, sg in out:
        if len(sg) > 1:
            L.append(rf"\draw[{epais if v else cache}] " + " -- ".join(Q(p) for p in sg) + ";")
    return L


EL = 22.0


def sp(lat, lon, R, lon0):
    return proj_sphere(lat, lon, R, lon0, EL)


def pt_label(lat, lon, R, lon0, nom, sp_, sm, color="otGreenDark", d=0.36):
    """Étiquette d'un point de la sphère placée dans le quadrant (sp_ : +1 est / -1 ouest,
    sm : +1 nord / -1 sud) entre son parallèle et son méridien."""
    x, y, _ = sp(lat, lon, R, lon0)
    a, b = sp(lat, lon + 4, R, lon0), sp(lat, lon - 4, R, lon0)
    c, e = sp(min(lat + 4, 90), lon, R, lon0), sp(max(lat - 4, -90), lon, R, lon0)
    dp = (a[0] - b[0], a[1] - b[1]); n = math.hypot(*dp); dp = (dp[0] / n, dp[1] / n)
    dm = (c[0] - e[0], c[1] - e[1]); n = math.hypot(*dm); dm = (dm[0] / n, dm[1] / n)
    v = (sp_ * dp[0] + sm * dm[0], sp_ * dp[1] + sm * dm[1]); n = math.hypot(*v); v = (v[0] / n, v[1] / n)
    return [rf"\fill[{color}] {Q((x, y))} circle (1.8pt);",
            rf"\node[text={color},inner sep=1pt] at {Q((x + d * v[0], y + d * v[1]))} {{{nom}}};"]


def globe(R, lon0, points=(), meridiens=(), paralleles=(), arc=None, legendes=True):
    L = [rf"\fill[face] (0,0) circle ({f(R)});"]
    leger, legerc = "otNavy!55,line width=.6pt", "otNavy!55,line width=.5pt,dash pattern=on 2pt off 2pt"
    for lo in meridiens:
        L += courbe([sp(la, lo, R, lon0) for la in range(-90, 91, 2)], R, leger, legerc)
    for la in paralleles:
        L += courbe([sp(la, lo, R, lon0) for lo in range(-180, 181, 2)], R, leger, legerc)
    L += courbe([sp(0, lo, R, lon0) for lo in range(-180, 181, 2)], R,
                "otNavy,line width=1pt", "otNavy,line width=.6pt,dash pattern=on 2.5pt off 2pt")
    L += courbe([sp(la, 0, R, lon0) for la in range(-90, 91, 2)], R,
                "otOrange!85!black,line width=1pt", "otOrange!85!black,line width=.6pt,dash pattern=on 2.5pt off 2pt")
    if arc:
        la, a, b = arc
        L += courbe([sp(la, lo, R, lon0) for lo in range(a, b + 1)], R, "otGreenDark,line width=2.2pt", "otGreenDark,line width=1.2pt")
    L.append(rf"\draw[solide] (0,0) circle ({f(R)});")
    N = sp(90, 0, R, lon0)
    L += [rf"\fill[otNavy] {Q(N[:2])} circle (1.5pt);",
          rf"\node[anchor=south,text=otNavy,font=\small] at ({f(N[0])},{f(R)}) [yshift=1pt] {{pôle Nord}};",
          rf"\fill[otNavy] (0,0) circle (1.3pt);"]
    if legendes:
        e = sp(0, lon0 - 62, R, lon0)
        L += [rf"\node[anchor=north east,text=otNavy,font=\small] at ({f(-0.72*R)},{f(-0.8*R)}) {{équateur}};",
              rf"\draw[otNavy,line width=.4pt] ({f(-0.74*R)},{f(-0.82*R)}) -- {Q(e[:2])};"]
        g = sp(58, 0, R, lon0)
        L += [rf"\node[anchor=south west,text=otOrange!75!black,font=\small,align=left] at ({f(0.62*R)},{f(0.86*R)}) {{méridien de\\Greenwich}};",
              rf"\draw[otOrange!75!black,line width=.4pt] ({f(0.64*R)},{f(0.88*R)}) -- {Q(g[:2])};"]
    for p in points:
        L += pt_label(*p[:2], R, lon0, *p[2:])
    return L


def globe_cours():
    R, lon0, la, lo = 2.3, -10.0, 40, 40
    L = globe(R, lon0, meridiens=[lo])
    M, Mq, G0 = sp(la, lo, R, lon0), sp(0, lo, R, lon0), sp(0, 0, R, lon0)
    L.append(rf"\draw[otMuted,line width=.5pt] (0,0) -- {Q(G0[:2])} (0,0) -- {Q(Mq[:2])} (0,0) -- {Q(M[:2])};")
    r1, r2 = 1.45, 1.6
    arc_lo = [sp(0, t, r1, lon0) for t in range(0, lo + 1, 2)]
    arc_la = [sp(t, lo, r2, lon0) for t in range(0, la + 1, 2)]
    L.append(rf"\draw[otGreenDark,line width=1.1pt] " + " -- ".join(Q(p[:2]) for p in arc_lo) + ";")
    L.append(rf"\draw[otGreenDark,line width=1.1pt] " + " -- ".join(Q(p[:2]) for p in arc_la) + ";")
    mlo, mla = arc_lo[len(arc_lo) // 2], arc_la[len(arc_la) // 2]
    L += [rf"\node[anchor=west,text=otGreenDark,font=\small] at ({f(1.1*R)},{f(0.2*R)}) {{latitude}};",
          rf"\draw[otGreenDark,line width=.4pt] ({f(1.1*R)},{f(0.2*R)}) -- {Q(mla[:2])};",
          rf"\node[anchor=west,text=otGreenDark,font=\small] at ({f(0.92*R)},{f(-0.62*R)}) {{longitude}};",
          rf"\draw[otGreenDark,line width=.4pt] ({f(0.92*R)},{f(-0.6*R)}) -- {Q(mlo[:2])};",
          rf"\node[anchor=north east,text=otInk,inner sep=1.5pt] at (0,0) {{$O$}};"]
    L += pt_label(la, lo, R, lon0, "$M$", 1, 1, color="otNavy")
    return tikz(L)


FIGURES["globe_cours"] = globe_cours()
FIGURES["globe_2431"] = tikz(globe(2.3, -15.0, points=[(35, 20, "$A$", 1, 1), (35, -50, "$B$", -1, 1), (-35, 20, "$C$", 1, -1)],
                                   meridiens=[20, -50], paralleles=[35, -35]))
FIGURES["globe_2440_enonce"] = tikz(globe(2.3, -5.0, points=[(0, 10, "$V_1$", 1, 1), (0, -20, "$V_2$", -1, 1)]))
FIGURES["globe_2440_corrige"] = tikz(globe(2.3, -5.0, points=[(0, 10, "$V_1$", 1, 1), (0, -20, "$V_2$", -1, 1)], arc=(0, -20, 10)))


# ------------------------------------------------------------ section d'une sphère (cours, 2432)
def section_sphere(R, d, labels, corrige, s=0.42):
    Rs = R * s
    r = math.sqrt(R * R - d * d) * s
    ds = d * s
    ry = 0.3 * r
    sty = "otGreenDark,line width=1.1pt" if corrige else "otNavy,line width=.9pt"
    styc = "otGreenDark,line width=.8pt,dash pattern=on 2.5pt off 2pt" if corrige else "cache"
    L = [rf"\fill[face] (0,0) circle ({f(Rs)});"]
    if corrige:
        L.append(rf"\fill[otGreen!30] (0,{f(ds)}) ellipse[x radius={f(r)},y radius={f(ry)}];")
    L += [rf"\draw[{styc}] ({f(r)},{f(ds)}) arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(ry)}];",
          rf"\draw[{sty}] ({f(-r)},{f(ds)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}];",
          rf"\draw[solide] (0,0) circle ({f(Rs)});",
          rf"\draw[hauteur] (0,0) -- (0,{f(ds)});",
          rf"\draw[otNavy,line width=.75pt] (0,0) -- ({f(r)},{f(ds)});",
          rf"\draw[{'rep' if corrige else 'otNavy,line width=.75pt'}] (0,{f(ds)}) -- ({f(r)},{f(ds)});",
          rf"\draw[otNavy,line width=.5pt] (0.17,{f(ds)}) -- (0.17,{f(ds-0.17)}) -- (0,{f(ds-0.17)});",
          rf"\fill[otNavy] (0,0) circle (1.4pt);", rf"\fill[otNavy] (0,{f(ds)}) circle (1.4pt);",
          rf"\fill[otNavy] ({f(r)},{f(ds)}) circle (1.4pt);",
          lab("(0,0)", labels["O"], "north"),
          lab(f"(0,{f(ds)})", labels["H"], "south east"),
          lab(f"({f(r)},{f(ds)})", labels["M"], "west"),
          rf"\node[anchor=east,text=otOrange!75!black] at (0,{f(ds*0.5)}) [xshift=-1pt] {{{labels['d']}}};",
          rf"\node[anchor=north west,text=otInk] at ({f(r*0.55)},{f(ds*0.55)}) [xshift=1pt] {{{labels['R']}}};"]
    if corrige and labels.get("r"):
        L.append(rf"\node[anchor=north,text=otGreenDark] at ({f(r*0.42)},{f(ds)}) [yshift=-1pt] {{{labels['r']}}};")
    return tikz(L)


FIGURES["section_sphere_cours"] = section_sphere(5, 3, {"O": "$O$", "H": "$H$", "M": "$M$", "d": "$d$", "R": "$R$", "r": "$r$"}, True, s=0.42)
FIGURES["section_sphere_enonce"] = section_sphere(5, 3, {"O": "$O$", "H": "$H$", "M": "$M$", "d": "$3$ cm", "R": "$5$ cm"}, False, s=0.48)
FIGURES["section_sphere_corrige"] = section_sphere(5, 3, {"O": "$O$", "H": "$H$", "M": "$M$", "d": "$3$ cm", "R": "$5$ cm", "r": "$4$ cm"}, True, s=0.48)


# ------------------------------------------------------------ sections du cours : pavé, cylindre ; pyramide, cône
def sections_cours_1():
    L = []
    # pavé (petit, sans noms) coupé parallèlement à la base
    s, a, b, c, z = 0.42, 6, 4, 5, 2.2
    pts = [P(0, 0, z, s), P(a, 0, z, s), P(a, b, z, s), P(0, b, z, s)]
    L += [rf"\fill[face] {P(0,0,0,s)} -- {P(a,0,0,s)} -- {P(a,b,0,s)} -- {P(a,b,c,s)} -- {P(0,b,c,s)} -- {P(0,0,c,s)} -- cycle;",
          rf"\fill[otGreen!30] {pts[0]} -- {pts[1]} -- {pts[2]} -- {pts[3]} -- cycle;",
          rf"\draw[cache] {P(0,0,0,s)} -- {P(0,b,0,s)} -- {P(a,b,0,s)} {P(0,b,0,s)} -- {P(0,b,c,s)};",
          rf"\draw[solide] {P(0,0,0,s)} -- {P(a,0,0,s)} -- {P(a,0,c,s)} -- {P(0,0,c,s)} -- cycle {P(a,0,0,s)} -- {P(a,b,0,s)} -- {P(a,b,c,s)} -- {P(0,b,c,s)} -- {P(0,0,c,s)} {P(a,0,c,s)} -- {P(a,b,c,s)};",
          rf"\draw[rep] {pts[3]} -- {pts[0]} -- {pts[1]} -- {pts[2]};",
          rf"\draw[repc] {pts[2]} -- {pts[3]};",
          rf"\node[anchor=north,text=otNavy,font=\small,align=center] at {P(a/2,0,0,s)} [yshift=-2pt] {{rectangle identique\\à la base}};"]
    # cylindre coupé parallèlement à la base
    xc, r, h, z = 5.3, 0.95, 2.2, 1.2
    L += cylindre(xc, r, h, None, None)
    ry = 0.32 * r
    L += [rf"\fill[otGreen!30] ({f(xc)},{f(z)}) ellipse[x radius={f(r)},y radius={f(ry)}];",
          rf"\draw[rep] ({f(xc-r)},{f(z)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}];",
          rf"\draw[repc] ({f(xc+r)},{f(z)}) arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(ry)}];",
          rf"\node[anchor=north,text=otNavy,font=\small,align=center] at ({f(xc)},{f(-ry)}) [yshift=-2pt] {{disque de même\\rayon que la base}};"]
    return tikz(L)


def sections_cours_2():
    L = []
    # pyramide à base carrée coupée parallèlement à la base
    c, h, s, k = 6, 7, 0.42, 0.5
    A, B, C, D = (0, 0, 0), (c, 0, 0), (c, c, 0), (0, c, 0)
    S = (c / 2, c / 2, h)
    m = lambda X: tuple(S[i] + k * (X[i] - S[i]) for i in range(3))
    pA, pB, pC, pD, pS = (P(*X, s=s) for X in (A, B, C, D, S))
    qA, qB, qC, qD = (P(*m(X), s=s) for X in (A, B, C, D))
    L += [rf"\fill[face] {pA} -- {pB} -- {pC} -- {pS} -- cycle;",
          rf"\fill[otGreen!30] {qA} -- {qB} -- {qC} -- {qD} -- cycle;",
          rf"\draw[cache] {pA} -- {pD} -- {pC} {pD} -- {pS};",
          rf"\draw[solide] {pA} -- {pB} -- {pC} -- {pS} -- cycle {pB} -- {pS};",
          rf"\draw[rep] {qD} -- {qA} -- {qB} -- {qC};", rf"\draw[repc] {qC} -- {qD};",
          rf"\node[anchor=north,text=otNavy,font=\small,align=center] at {P(c/2,0,0,s)} [yshift=-2pt] {{réduction\\de la base}};"]
    # cône coupé parallèlement à la base
    xc, r, h2 = 5.6, 1.15, 2.9
    L += cone(xc, r, h2, None, None)
    z = h2 * 0.5
    r2 = r * 0.5
    ry = 0.32 * r2
    L += [rf"\fill[otGreen!30] ({f(xc)},{f(z)}) ellipse[x radius={f(r2)},y radius={f(ry)}];",
          rf"\draw[rep] ({f(xc-r2)},{f(z)}) arc[start angle=180,end angle=360,x radius={f(r2)},y radius={f(ry)}];",
          rf"\draw[repc] ({f(xc+r2)},{f(z)}) arc[start angle=0,end angle=180,x radius={f(r2)},y radius={f(ry)}];",
          rf"\node[anchor=north,text=otNavy,font=\small,align=center] at ({f(xc)},{f(-0.32*r)}) [yshift=-2pt] {{disque, réduction\\de la base}};"]
    return tikz(L)


FIGURES["sections_pave_cylindre"] = sections_cours_1()
FIGURES["sections_pyramide_cone"] = sections_cours_2()


# ------------------------------------------------------------ 2433 : réservoir (cylindre + demi-boule)
def reservoir():
    r, h = 1.3, 2.6
    ry = 0.32 * r
    L = [rf"\fill[face] ({f(-r)},0) -- ({f(-r)},{f(h)}) arc[start angle=180,end angle=0,radius={f(r)}] -- ({f(r)},0) arc[start angle=0,end angle=-180,x radius={f(r)},y radius={f(ry)}] -- cycle;",
         rf"\draw[cache] ({f(r)},0) arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[cache] ({f(r)},{f(h)}) arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[solide,line width=.6pt] ({f(-r)},{f(h)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[solide] ({f(-r)},0) -- ({f(-r)},{f(h)}) arc[start angle=180,end angle=0,radius={f(r)}] -- ({f(r)},0);",
         rf"\draw[solide] ({f(-r)},0) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[hauteur] (0,0) -- ({f(r)},0);", rf"\fill[otNavy] (0,0) circle (1.4pt);",
         rf"\node[anchor=north,text=otInk] at ({f(r/2)},{f(-ry)}) {{$1$ m}};",
         rf"\draw[cote] ({f(r+0.32)},0) -- ({f(r+0.32)},{f(h)});",
         rf"\node[anchor=west,text=otInk] at ({f(r+0.4)},{f(h/2)}) {{$2$ m}};",
         rf"\node[text=otNavy,font=\small] at (0,{f(h+0.78)}) {{demi-boule}};",
         rf"\node[text=otNavy,font=\small] at (0,{f(h/2)}) {{cylindre}};"]
    return tikz(L)


FIGURES["reservoir_2433"] = reservoir()


# ------------------------------------------------------------ 2434 : boule creusée
FIGURES["cavite_2434"] = tikz([
    r"\fill[face] (0,0) circle (2.4);",
    r"\draw[cache] (2.4,0) arc[start angle=0,end angle=180,x radius=2.4,y radius=0.72];",
    r"\draw[solide,line width=.6pt] (-2.4,0) arc[start angle=180,end angle=360,x radius=2.4,y radius=0.72];",
    r"\draw[solide] (0,0) circle (2.4);",
    r"\fill[white] (-0.95,0.6) circle (0.96);",
    r"\draw[cache] (-0.95,0.6) circle (0.96);",
    r"\draw[hauteur] (0,0) -- (2.078,-1.2);", r"\fill[otNavy] (0,0) circle (1.4pt);",
    r"\node[anchor=north east,text=otInk] at (1.75,-1.12) {$5$ cm};",
    r"\draw[hauteur] (-0.95,0.6) -- (-1.91,0.6);", r"\fill[otNavy] (-0.95,0.6) circle (1.3pt);",
    r"\node[anchor=south,text=otInk] at (-1.43,0.63) {$2$ cm};",
    r"\node[anchor=north,text=otMuted,font=\small] at (-0.95,0.4) {cavité};",
    r"\node[anchor=north east,text=otInk,inner sep=2pt] at (0,0) {$O$};",
])


# ------------------------------------------------------------ 2435 : cône coupé à mi-hauteur
def cone_coupe(corrige):
    r, h = 1.5, 3.6
    L = cone(0, r, h, "$6$ cm", "$12$ cm", yh=0.22)
    z, r2 = h / 2, r / 2
    ry = 0.32 * r2
    if corrige:
        L += [rf"\fill[otGreen!30] (0,{f(z)}) ellipse[x radius={f(r2)},y radius={f(ry)}];",
              rf"\draw[rep] ({f(-r2)},{f(z)}) arc[start angle=180,end angle=360,x radius={f(r2)},y radius={f(ry)}];",
              rf"\draw[repc] ({f(r2)},{f(z)}) arc[start angle=0,end angle=180,x radius={f(r2)},y radius={f(ry)}];",
              rf"\draw[rep] ({f(-r2)},{f(z)}) -- (0,{f(z)});",
              rf"\node[anchor=east,text=otGreenDark] at ({f(-r2)},{f(z)}) [xshift=-3pt] {{$3$ cm}};"]
    else:
        L += [rf"\draw[donnee] ({f(-r2)},{f(z)}) arc[start angle=180,end angle=360,x radius={f(r2)},y radius={f(ry)}];",
              rf"\draw[donneec] ({f(r2)},{f(z)}) arc[start angle=0,end angle=180,x radius={f(r2)},y radius={f(ry)}];"]
    L += [rf"\node[anchor=south west,text=otInk] at (0,{f(h)}) [xshift=1pt] {{$S$}};",
          rf"\draw[cote] ({f(r+0.35)},{f(z)}) -- ({f(r+0.35)},{f(h)});",
          rf"\node[anchor=west,text=otInk] at ({f(r+0.43)},{f(z+h/4)}) {{$6$ cm}};",
          rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] ({f(r2+0.1)},{f(z)}) -- ({f(r+0.45)},{f(z)});",
          rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] (0.12,{f(h)}) -- ({f(r+0.45)},{f(h)});"]
    return tikz(L)


FIGURES["cone_coupe_enonce"] = cone_coupe(False)
FIGURES["cone_coupe_corrige"] = cone_coupe(True)


# ------------------------------------------------------------ 2436 : silo (cylindre sur cône, pointe en bas)
def silo():
    r, hc, hk = 1.2, 3.2, 0.8
    ry = 0.32 * r
    L = [rf"\fill[face] (0,0) -- ({f(-r)},{f(hk)}) -- ({f(-r)},{f(hk+hc)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- ({f(r)},{f(hk)}) -- cycle;",
         rf"\fill[otSky!60!white] (0,{f(hk+hc)}) ellipse[x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[solide] (0,{f(hk+hc)}) ellipse[x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[cache] ({f(r)},{f(hk)}) arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[solide,line width=.6pt] ({f(-r)},{f(hk)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[solide] ({f(-r)},{f(hk+hc)}) -- ({f(-r)},{f(hk)}) -- (0,0) -- ({f(r)},{f(hk)}) -- ({f(r)},{f(hk+hc)});",
         rf"\draw[hauteur] (0,{f(hk+hc)}) -- ({f(r)},{f(hk+hc)});", rf"\fill[otNavy] (0,{f(hk+hc)}) circle (1.4pt);",
         rf"\node[anchor=south,text=otInk] at ({f(r/2)},{f(hk+hc+ry)}) {{$3$ m}};",
         rf"\draw[cote] ({f(r+0.32)},{f(hk)}) -- ({f(r+0.32)},{f(hk+hc)});",
         rf"\node[anchor=west,text=otInk] at ({f(r+0.4)},{f(hk+hc/2)}) {{$8$ m}};",
         rf"\draw[cote] ({f(r+0.32)},0) -- ({f(r+0.32)},{f(hk)});",
         rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] (0.1,0) -- ({f(r+0.42)},0);",
         rf"\node[anchor=west,text=otInk] at ({f(r+0.4)},{f(hk/2)}) {{$2$ m}};"]
    return tikz(L)


FIGURES["silo_2436"] = silo()


# ------------------------------------------------------------ 2437 : cube, diagonales [AF] et [AG]
def cube(corrige):
    a, s = 6, 0.5
    out = pave_nomme(a, a, a, s=s, cotes={"AB": "$6$ cm"})
    A, F, G = P(0, 0, 0, s), P(a, a, 0, s), P(a, a, a, s)
    if corrige:
        out.insert(1, rf"\fill[otGreen!25] {A} -- {F} -- {G} -- cycle;")
        out += [rf"\draw[repc] {A} -- {F};", rf"\draw[repc] {A} -- {G};", rf"\draw[rep] {F} -- {G};",
                rf"\draw[otGreenDark,line width=.6pt] {P(a,a,0.55,s)} -- {P(a-0.55*0.7071,a-0.55*0.7071,0.55,s)} -- {P(a-0.55*0.7071,a-0.55*0.7071,0,s)};",
                rf"\node[anchor=north,text=otGreenDark] at {P(a*0.62,a*0.62,0,s)} [yshift=-1pt] {{$6\sqrt{{2}}$}};"]
    else:
        out += [rf"\draw[donneec] {A} -- {F};", rf"\draw[donneec] {A} -- {G};"]
    return tikz(out)


FIGURES["cube_enonce"] = cube(False)
FIGURES["cube_corrige"] = cube(True)


# ------------------------------------------------------------ 2438 : cornet (cône pointe en bas + demi-boule)
def cornet():
    r, h = 1.2, 4.0
    ry = 0.32 * r
    L = [rf"\fill[otOrange!25] (0,0) -- ({f(-r)},{f(h)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- cycle;",
         rf"\fill[face] ({f(-r)},{f(h)}) arc[start angle=180,end angle=0,radius={f(r)}] arc[start angle=0,end angle=-180,x radius={f(r)},y radius={f(ry)}] -- cycle;",
         rf"\draw[cache] ({f(r)},{f(h)}) arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[solide] ({f(-r)},{f(h)}) arc[start angle=180,end angle=0,radius={f(r)}];",
         rf"\draw[solide] ({f(-r)},{f(h)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[solide] ({f(-r)},{f(h)}) -- (0,0) -- ({f(r)},{f(h)});",
         rf"\draw[hauteur] (0,{f(h)}) -- ({f(r)},{f(h)});", rf"\fill[otNavy] (0,{f(h)}) circle (1.4pt);",
         rf"\node[anchor=west,text=otInk] at ({f(r)},{f(h)}) [xshift=2pt] {{$3$ cm}};",
         rf"\draw[cote] ({f(-r-0.32)},0) -- ({f(-r-0.32)},{f(h)});",
         rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] (-0.1,0) -- ({f(-r-0.42)},0);",
         rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] ({f(-r-0.1)},{f(h)}) -- ({f(-r-0.42)},{f(h)});",
         rf"\node[anchor=east,text=otInk] at ({f(-r-0.4)},{f(h/2)}) {{$10$ cm}};"]
    return tikz(L)


FIGURES["cornet_2438"] = cornet()


# ------------------------------------------------------------ 2441 : verre conique r = 4, h = 12, liquide 10 cm
def verre(corrige):
    s = 0.33
    R, H, hl = 4 * s, 12 * s, 10 * s
    rl = R * hl / H
    ry = 0.3 * R
    L = [rf"\fill[otGreen!25] ({f(-rl)},{f(hl)}) -- (0,0) -- ({f(rl)},{f(hl)}) arc[start angle=0,end angle=-180,x radius={f(rl)},y radius={f(0.3*rl)}] -- cycle;",
         rf"\fill[otGreen!40] (0,{f(hl)}) ellipse[x radius={f(rl)},y radius={f(0.3*rl)}];",
         rf"\draw[otGreenDark,line width=.7pt] (0,{f(hl)}) ellipse[x radius={f(rl)},y radius={f(0.3*rl)}];",
         rf"\draw[solide] (0,{f(H)}) ellipse[x radius={f(R)},y radius={f(ry)}];",
         rf"\draw[solide] ({f(-R)},{f(H)}) -- (0,0) -- ({f(R)},{f(H)});",
         rf"\draw[hauteur] (0,{f(H)}) -- ({f(R)},{f(H)});",
         rf"\fill[otNavy] (0,{f(H)}) circle (1.5pt);",
         rf"\node[anchor=south,text=otInk] at ({f(R/2)},{f(H+ry+0.02)}) {{$4$ cm}};",
         rf"\draw[cote] ({f(R+0.5)},0) -- ({f(R+0.5)},{f(H)});",
         rf"\node[anchor=west,text=otInk] at ({f(R+0.58)},{f(H*0.6)}) {{$12$ cm}};",
         rf"\draw[cote] ({f(-R-0.4)},0) -- ({f(-R-0.4)},{f(hl)});",
         rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] ({f(-R-0.5)},{f(hl)}) -- ({f(-rl-0.1)},{f(hl)});",
         rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] ({f(-R-0.5)},0) -- (-0.1,0);",
         rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] ({f(R+0.6)},0) -- (0.1,0);",
         rf"\node[anchor=east,text=otInk] at ({f(-R-0.48)},{f(hl/2)}) {{$10$ cm}};"]
    if corrige:
        L.append(rf"\draw[rep] (0,{f(hl)}) -- ({f(rl)},{f(hl)});")
        L.append(rf"\node[anchor=north,text=otGreenDark] at (0,{f(hl-0.3*rl)}) [yshift=-2pt] {{$\frac{{10}}{{3}}$ cm}};")
    return tikz(L)


FIGURES["verre_enonce"] = verre(False)
FIGURES["verre_corrige"] = verre(True)


# ------------------------------------------------------------ 2442 : aquarium 80 × 40 × 50, eau sur 45 cm
FIGURES["aquarium_2442"] = tikz(pave_nomme(80, 40, 50, s=0.065, noms=False, eau=45,
                                           cotes={"AB": "$80$ cm", "BF": "$40$ cm", "FG": "$50$ cm"})
                                + [rf"\draw[cote] {P(-6,0,0,0.065)} -- {P(-6,0,45,0.065)};",
                                   rf"\node[anchor=east,text=otGreenDark] at {P(-6.5,0,22.5,0.065)} {{$45$ cm}};"])
