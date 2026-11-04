# -*- coding: utf-8 -*-
"""Figures de la notion 235 (3e : arithmétique et nombres premiers), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
"""
import math
from sympy import isprime

PREAMBULE_EXTRA = r"""
\tikzset{
  noeudC/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=3pt,
    minimum width=1.05cm,minimum height=.62cm,inner sep=2pt,text=otNavy,font=\bfseries},
  noeudP/.style={draw=otOrange!85!black,fill=otOrange!16,line width=.8pt,rounded corners=3pt,
    minimum width=.7cm,minimum height=.62cm,inner sep=2pt,text=otInk,font=\bfseries},
  branche/.style={otMuted,line width=.7pt},
}
"""


def f(x):
    """Nombre décimal pour TikZ (point décimal, 3 chiffres)."""
    return f"{x:.3f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------ rectangles de diviseurs
def rectangles(n, formes, u=0.2):
    """Rangements de n carreaux en rectangles l × h ; formes = [(l, h, couleur), …]."""
    L = [r"\begin{tikzpicture}"]
    y = 0.0
    for (l, h, coul) in formes:
        if l * u > 3.2:            # rectangle long : étiquette au-dessus (figure moins large)
            L.append(rf"\node[anchor=north west,text=otInk,inner sep=1pt] at (0,{f(y)}) {{${n} = {l} \times {h}$}};")
            y -= 0.5 + h * u
            x1, y1 = l * u, y + h * u
            L.append(rf"\fill[{coul}] (0,{f(y)}) rectangle ({f(x1)},{f(y1)});")
            for i in range(1, l):
                L.append(rf"\draw[otNavy!35,line width=.3pt] ({f(i*u)},{f(y)}) -- ({f(i*u)},{f(y1)});")
            for j in range(1, h):
                L.append(rf"\draw[otNavy!35,line width=.3pt] (0,{f(y+j*u)}) -- ({f(x1)},{f(y+j*u)});")
            L.append(rf"\draw[otNavy,line width=.75pt] (0,{f(y)}) rectangle ({f(x1)},{f(y1)});")
            y -= 0.3
            continue
        y -= h * u
        x1, y1 = l * u, y + h * u
        L.append(rf"\fill[{coul}] (0,{f(y)}) rectangle ({f(x1)},{f(y1)});")
        for i in range(1, l):
            L.append(rf"\draw[otNavy!35,line width=.3pt] ({f(i*u)},{f(y)}) -- ({f(i*u)},{f(y1)});")
        for j in range(1, h):
            L.append(rf"\draw[otNavy!35,line width=.3pt] (0,{f(y+j*u)}) -- ({f(x1)},{f(y+j*u)});")
        L.append(rf"\draw[otNavy,line width=.75pt] (0,{f(y)}) rectangle ({f(x1)},{f(y1)});")
        L.append(rf"\node[anchor=west,text=otInk] at ({f(x1+0.18)},{f(y+h*u/2)}) {{${n} = {l} \times {h}$}};")
        y -= 0.3
    divs = sorted({d for (l, h, _) in formes for d in (l, h)})
    txt = ", ".join(f"${d}$" for d in divs)
    L.append(rf"\node[anchor=north west,text=otGreenDark,inner sep=0pt,align=left] at (0,{f(y-0.05)}) "
             rf"{{Diviseurs positifs de ${n}$ :\\ {txt}}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ------------------------------------------------------------ crible (nombres premiers < 100)
def crible():
    c = 0.86
    L = [r"\begin{tikzpicture}"]
    for n in range(1, 101):
        r, k = divmod(n - 1, 10)
        x0, y0 = k * c, -(r + 1) * c
        if isprime(n):
            L.append(rf"\fill[otSky] ({f(x0)},{f(y0)}) rectangle ({f(x0+c)},{f(y0+c)});")
    L.append(rf"\draw[otRule,line width=.6pt] (0,{f(-10*c)}) grid[step={f(c)}] ({f(10*c)},0);")
    for n in range(1, 101):
        r, k = divmod(n - 1, 10)
        if isprime(n):
            L.append(rf"\draw[otNavy,line width=.9pt] ({f(k*c)},{f(-(r+1)*c)}) rectangle ({f((k+1)*c)},{f(-r*c)});")
    for n in range(1, 101):
        r, k = divmod(n - 1, 10)
        x, y = (k + .5) * c, -(r + .5) * c
        if isprime(n):
            L.append(rf"\node[text=otNavy,font=\otMedium\bfseries\fontsize{{10.5}}{{12}}\selectfont] at ({f(x)},{f(y)}) {{{n}}};")
        else:
            L.append(rf"\node[text=otMuted!75,font=\otRegular\fontsize{{10}}{{12}}\selectfont] at ({f(x)},{f(y)}) {{{n}}};")
    yl = -10 * c - 0.55
    L.append(rf"\fill[otSky] (0,{f(yl-0.2)}) rectangle (0.4,{f(yl+0.2)});")
    L.append(rf"\draw[otNavy,line width=.9pt] (0,{f(yl-0.2)}) rectangle (0.4,{f(yl+0.2)});")
    L.append(rf"\node[anchor=west,text=otInk] at (0.55,{f(yl)}) {{nombre premier ($25$ nombres inférieurs à $100$)}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ------------------------------------------------------------ arbres de décomposition
def arbre(n, etapes, dx=1.08, dy=0.95, resultat=""):
    """etapes = [(p, quotient), …] : n = p × quotient, puis quotient = p' × …"""
    L = [r"\begin{tikzpicture}"]
    L.append(rf"\node[noeudC] (c0) at ({f(dx)},0) {{{n}}};")
    for i, (p, q) in enumerate(etapes, start=1):
        dernier = i == len(etapes)
        L.append(rf"\node[noeudP] (p{i}) at ({f((i-1)*dx)},{f(-i*dy)}) {{{p}}};")
        style = "noeudP" if dernier else "noeudC"
        L.append(rf"\node[{style}] (c{i}) at ({f((i+1)*dx)},{f(-i*dy)}) {{{q}}};")
        L.append(rf"\draw[branche] (c{i-1}) -- (p{i}); \draw[branche] (c{i-1}) -- (c{i});")
    k = len(etapes)
    L.append(rf"\node[noeudP,minimum width=.45cm,minimum height=.38cm] (lg) at ({f((k+1)*dx - 2.6)},0) {{}};")
    L.append(r"\node[anchor=west,text=otInk] at ($(lg.east)+(.12,0)$) {facteur premier};")
    L.append(rf"\node[anchor=west,text=otGreenDark,font=\large] at (-0.35,{f(-(k)*dy - 1.0)}) {{${resultat}$}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ------------------------------------------------------------ 47 billes en sachets de 6
def billes():
    e = 0.28                     # pas entre deux billes
    L = [r"\begin{tikzpicture}"]
    w = 2 * e + 0.36             # largeur d'un sachet (2 colonnes × 3 lignes)
    pas = w + 0.22
    for s in range(7):
        x0 = s * pas
        L.append(rf"\draw[otNavy,line width=.8pt,rounded corners=4pt,fill=otSky] ({f(x0)},0) rectangle ({f(x0+w)},{f(3*e+0.36)});")
        for i in range(6):
            L.append(rf"\fill[otNavy] ({f(x0 + 0.33 + (i % 2) * e)},{f(0.33 + (i // 2) * e)}) circle (3.3pt);")
    x0 = 7 * pas + 0.15
    for i in range(5):
        L.append(rf"\fill[otOrange] ({f(x0 + 0.18 + (i % 2) * e)},{f(0.33 + (i // 2) * e)}) circle (3.3pt);")
    H = 3 * e + 0.36
    br = r"decorate,decoration={brace,amplitude=5pt,raise=3pt,mirror}"
    L.append(rf"\draw[otNavy,line width=.7pt,{br}] (0,0) -- ({f(7*pas-0.22)},0);")
    L.append(rf"\node[anchor=north,text=otNavy] at ({f((7*pas-0.22)/2)},-.32) {{$7$ sachets de $6$ billes : $42$}};")
    L.append(rf"\node[anchor=south,text=otOrange!80!black,align=center] at ({f(x0+0.33)},{f(H+0.12)}) {{reste\\$5$}};")
    L.append(rf"\node[anchor=south west,text=otGreenDark] at (0,{f(H+0.95)}) {{$47 = 6 \times 7 + 5$}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ------------------------------------------------------------ bus toutes les 12 et 18 min
def frise_bus():
    s = 0.068                    # cm par minute
    T = 108
    L = [r"\begin{tikzpicture}"]
    yA, yB = 1.0, 0.5
    for t in range(0, T + 1, 36):
        L.append(rf"\draw[otGreenDark,line width=.8pt,dash pattern=on 2.5pt off 1.8pt] ({f(t*s)},0) -- ({f(t*s)},{f(yA+0.3)});")
    L.append(rf"\draw[otMuted,line width=.7pt,-{{Stealth[length=2.3mm]}}] (0,0) -- ({f(T*s+0.45)},0);")
    L.append(rf"\node[anchor=west,text=otMuted] at ({f(T*s+0.5)},0) {{min}};")
    for t in range(0, T + 1, 6):
        L.append(rf"\draw[otMuted,line width=.5pt] ({f(t*s)},-0.06) -- ({f(t*s)},0.06);")
    for t in range(0, T + 1, 36):
        L.append(rf"\node[anchor=north,text=otGreenDark,font=\otMedium\bfseries\fontsize{{9.5}}{{11}}\selectfont] at ({f(t*s)},-0.14) {{{t}}};")
    for t in range(0, T + 1, 12):
        L.append(rf"\fill[otNavy] ({f(t*s)},{f(yA)}) circle (2.6pt);")
    for t in range(0, T + 1, 18):
        L.append(rf"\fill[otOrange] ({f(t*s)},{f(yB)}) circle (2.6pt);")
    L.append(r"\fill[otNavy] (0.1,2.35) circle (2.6pt);")
    L.append(r"\node[anchor=west,text=otInk] at (0.25,2.35) {ligne A : toutes les $12$ min};")
    L.append(r"\fill[otOrange] (0.1,1.85) circle (2.6pt);")
    L.append(r"\node[anchor=west,text=otInk] at (0.25,1.85) {ligne B : toutes les $18$ min};")
    L.append(r"\node[anchor=north,text=otGreenDark,align=center] at (" + f(54*s) + r",-0.62) {départs communs : toutes les $36$ min};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ------------------------------------------------------------ dallage 252 × 180
def dallage(corrige):
    k = 5.4 / 252                # cm par cm réel
    W, H = 252 * k, 180 * k
    L = [r"\begin{tikzpicture}"]
    if corrige:
        d = 36 * k
        L.append(rf"\fill[otGreen!14] (0,0) rectangle ({f(W)},{f(H)});")
        for i in range(1, 7):
            L.append(rf"\draw[otGreenDark,line width=.6pt] ({f(i*d)},0) -- ({f(i*d)},{f(H)});")
        for j in range(1, 5):
            L.append(rf"\draw[otGreenDark,line width=.6pt] (0,{f(j*d)}) -- ({f(W)},{f(j*d)});")
        L.append(rf"\fill[otGreen!45] (0,{f(H-d)}) rectangle ({f(d)},{f(H)});")
        L.append(rf"\draw[otGreenDark,line width=.6pt] (0,{f(H-d)}) rectangle ({f(d)},{f(H)});")
    else:
        L.append(rf"\fill[otSky] (0,0) rectangle ({f(W)},{f(H)});")
    L.append(rf"\draw[otNavy,line width=1pt] (0,0) rectangle ({f(W)},{f(H)});")
    # cotes
    L.append(rf"\draw[cote] (0,-0.35) -- ({f(W)},-0.35);")
    L.append(rf"\node[anchor=north,text=otInk] at ({f(W/2)},-0.45) {{$252$ cm}};")
    L.append(rf"\draw[cote] (-0.35,0) -- (-0.35,{f(H)});")
    L.append(rf"\node[anchor=east,text=otInk] at (-0.45,{f(H/2)}) {{$180$ cm}};")
    if corrige:
        L.append(rf"\draw[cote,otGreenDark] (0,{f(H+0.3)}) -- ({f(36*k)},{f(H+0.3)});")
        L.append(rf"\node[anchor=south,text=otGreenDark] at ({f(18*k)},{f(H+0.38)}) {{$36$ cm}};")
        L.append(rf"\node[anchor=south east,text=otGreenDark] at ({f(W)},{f(H+0.38)}) {{$7 \times 5 = 35$ dalles}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ------------------------------------------------------------ engrenages 24 et 40 dents
def roue(cx, n, r, coul, phase):
    """Roue dentée : n dents trapézoïdales autour d'un cercle de rayon r (cm)."""
    h = 0.17
    pts = []
    for i in range(n):
        a0 = phase + 360 * i / n
        da = 360 / n
        for (a, rr) in ((a0 - 0.30 * da, r), (a0 - 0.18 * da, r + h), (a0 + 0.18 * da, r + h), (a0 + 0.30 * da, r)):
            pts.append(f"({f(cx + rr*math.cos(math.radians(a)))},{f(rr*math.sin(math.radians(a)))})")
    return rf"\draw[{coul},line width=.8pt,fill={coul}!10] " + " -- ".join(pts) + " -- cycle;"


def engrenages():
    r1 = 1.2
    r2 = r1 * 40 / 24
    h = 0.17
    c1, c2 = 0.0, r1 + r2 + h
    L = [r"\begin{tikzpicture}"]
    # petite roue : une dent pointe vers 0°, grande roue : un creux vers 180°
    L.append(roue(c1, 24, r1, "otNavy", 0))
    L.append(roue(c2, 40, r2, "otOrange!85!black", 180 + 360 / 80))
    L.append(rf"\fill[otNavy] ({f(c1)},0) circle (2.4pt);")
    L.append(rf"\fill[otOrange!85!black] ({f(c2)},0) circle (2.4pt);")
    # dents marquées (en vert) au point de contact
    # dents marquées : remplies en vert (petite roue : dent à 0° ; grande roue : dent à 180° + 4,5°)
    for (cx, n, r, a0) in ((c1, 24, r1, 0.0), (c2, 40, r2, 180 + 360 / 80)):
        da = 360 / n
        pts = []
        for (a, rr) in ((a0 - 0.30 * da, r), (a0 - 0.18 * da, r + h), (a0 + 0.18 * da, r + h), (a0 + 0.30 * da, r)):
            pts.append(f"({f(cx + rr*math.cos(math.radians(a)))},{f(rr*math.sin(math.radians(a)))})")
        L.append(r"\fill[otGreenDark] " + " -- ".join(pts) + " -- cycle;")
    L.append(rf"\draw[otGreenDark,line width=.7pt,-{{Stealth[length=2mm]}}] ({f(c1 + r1 - 0.1)},{f(r2 + 0.55)}) -- ({f(c1 + r1 + h/2)},{f(0.22)});")
    L.append(rf"\node[anchor=south,text=otGreenDark] at ({f(c1 + r1 - 0.1)},{f(r2 + 0.55)}) {{dents marquées}};")
    L.append(rf"\node[anchor=north,text=otNavy] at ({f(c1)},{f(-r1-0.35)}) {{$24$ dents}};")
    L.append(rf"\node[anchor=north,text=otOrange!80!black] at ({f(c2)},{f(-r2-0.35)}) {{$40$ dents}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES = {
    "diviseurs_36": rectangles(36, [(36, 1, "otSky"), (18, 2, "otGreen!14"), (12, 3, "otOrange!14"),
                                    (9, 4, "otSky"), (6, 6, "otGreen!14")], u=0.16),
    "diviseurs_48": rectangles(48, [(48, 1, "otSky"), (24, 2, "otGreen!14"), (16, 3, "otOrange!14"),
                                    (12, 4, "otSky"), (8, 6, "otGreen!14")], u=0.135),
    "crible_100": crible(),
    "arbre_360": arbre(360, [(2, 180), (2, 90), (2, 45), (3, 15), (3, 5)],
                       resultat=r"360 = 2^3 \times 3^2 \times 5"),
    "arbre_420": arbre(420, [(2, 210), (2, 105), (3, 35), (5, 7)],
                       resultat=r"420 = 2^2 \times 3 \times 5 \times 7"),
    "billes_47": billes(),
    "frise_bus": frise_bus(),
    "dallage_enonce": dallage(False),
    "dallage_corrige": dallage(True),
    "engrenages": engrenages(),
}
