# -*- coding: utf-8 -*-
"""Figures de la notion 166 (multiples, diviseurs, nombres premiers), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
"""
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


# ------------------------------------------------------------ diviseurs de 36
def rectangles_36():
    u = 0.16                       # côté d'un carreau (cm)
    formes = [(36, 1, "otSky"), (18, 2, "otGreen!14"), (12, 3, "otOrange!14"),
              (9, 4, "otSky"), (6, 6, "otGreen!14")]
    lignes = [r"\begin{tikzpicture}"]
    y = 0.0
    for (l, h, coul) in formes:
        y -= h * u
        x1, y1 = l * u, y + h * u
        lignes.append(rf"\fill[{coul}] (0,{f(y)}) rectangle ({f(x1)},{f(y1)});")
        for i in range(1, l):
            lignes.append(rf"\draw[otNavy!35,line width=.3pt] ({f(i*u)},{f(y)}) -- ({f(i*u)},{f(y1)});")
        for j in range(1, h):
            lignes.append(rf"\draw[otNavy!35,line width=.3pt] (0,{f(y+j*u)}) -- ({f(x1)},{f(y+j*u)});")
        lignes.append(rf"\draw[otNavy,line width=.75pt] (0,{f(y)}) rectangle ({f(x1)},{f(y1)});")
        lignes.append(rf"\node[anchor=west,text=otInk] at ({f(x1+0.18)},{f(y+h*u/2)}) {{${l} \times {h}$}};")
        y -= 0.28
    lignes.append(rf"\node[anchor=north west,text=otNavy,inner sep=0pt,align=left] at (0,{f(y-0.05)}) "
                  r"{Diviseurs de $36$ :\\ $1$, $2$, $3$, $4$, $6$, $9$, $12$, $18$, $36$};")
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


# ------------------------------------------------------------ nombres premiers < 100
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
    # légende
    yl = -10 * c - 0.55
    L.append(rf"\fill[otSky] (0,{f(yl-0.2)}) rectangle (0.4,{f(yl+0.2)});")
    L.append(rf"\draw[otNavy,line width=.9pt] (0,{f(yl-0.2)}) rectangle (0.4,{f(yl+0.2)});")
    L.append(rf"\node[anchor=west,text=otInk] at (0.55,{f(yl)}) {{nombre premier ($25$ nombres)}};")
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
    # légende en haut à droite, résultat en bas à gauche (espaces libres)
    L.append(rf"\node[noeudP,minimum width=.45cm,minimum height=.38cm] (lg) at ({f((k+1)*dx - 2.6)},0) {{}};")
    L.append(r"\node[anchor=west,text=otInk] at ($(lg.east)+(.12,0)$) {facteur premier};")
    L.append(rf"\node[anchor=west,text=otGreenDark,font=\large] at (-0.35,{f(-(k)*dy - 1.0)}) {{${resultat}$}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ------------------------------------------------------------ guirlandes (exercice 1925)
def frise():
    s = 0.03                       # cm par seconde
    T = 180
    L = [r"\begin{tikzpicture}"]
    yA, yB = 1.0, 0.5
    for t in range(0, T + 1, 36):
        L.append(rf"\draw[otGreenDark,line width=.8pt,dash pattern=on 2.5pt off 1.8pt] ({f(t*s)},0) -- ({f(t*s)},{f(yA+0.3)});")
    L.append(rf"\draw[otMuted,line width=.7pt,-{{Stealth[length=2.3mm]}}] (0,0) -- ({f(T*s+0.55)},0);")
    L.append(rf"\node[anchor=west,text=otMuted] at ({f(T*s+0.6)},0) {{$t$ (s)}};")
    for t in range(0, T + 1, 36):
        L.append(rf"\draw[otGreenDark,line width=.8pt] ({f(t*s)},-0.09) -- ({f(t*s)},0.09);")
        L.append(rf"\node[anchor=north,text=otGreenDark,font=\otMedium\bfseries\fontsize{{9.5}}{{11}}\selectfont] at ({f(t*s)},-0.16) {{{t}}};")
    for t in range(0, T + 1, 12):
        L.append(rf"\fill[otNavy] ({f(t*s)},{f(yA)}) circle (2.4pt);")
    for t in range(0, T + 1, 18):
        L.append(rf"\fill[otOrange] ({f(t*s)},{f(yB)}) circle (2.4pt);")
    # légende au-dessus
    L.append(rf"\fill[otNavy] (0.1,2.35) circle (2.4pt);")
    L.append(r"\node[anchor=west,text=otInk] at (0.25,2.35) {guirlande 1 : toutes les $12$ s};")
    L.append(rf"\fill[otOrange] (0.1,1.85) circle (2.4pt);")
    L.append(r"\node[anchor=west,text=otInk] at (0.25,1.85) {guirlande 2 : toutes les $18$ s};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# =================================================================== finition 2026-11-02

def rectangles(n, formes, u=0.2):
    """Rangements de n carreaux en rectangles l × h ; formes = [(l, h, couleur), …]."""
    lignes = [r"\begin{tikzpicture}"]
    y = 0.0
    for (l, h, coul) in formes:
        y -= h * u
        x1, y1 = l * u, y + h * u
        lignes.append(rf"\fill[{coul}] (0,{f(y)}) rectangle ({f(x1)},{f(y1)});")
        for i in range(1, l):
            lignes.append(rf"\draw[otNavy!35,line width=.3pt] ({f(i*u)},{f(y)}) -- ({f(i*u)},{f(y1)});")
        for j in range(1, h):
            lignes.append(rf"\draw[otNavy!35,line width=.3pt] (0,{f(y+j*u)}) -- ({f(x1)},{f(y+j*u)});")
        lignes.append(rf"\draw[otNavy,line width=.75pt] (0,{f(y)}) rectangle ({f(x1)},{f(y1)});")
        lignes.append(rf"\node[anchor=west,text=otInk] at ({f(x1+0.18)},{f(y+h*u/2)}) {{${n} = {l} \times {h}$}};")
        y -= 0.3
    divs = sorted({d for (l, h, _) in formes for d in (l, h)})
    txt = ", ".join(f"${d}$" for d in divs)
    lignes.append(rf"\node[anchor=north west,text=otGreenDark,inner sep=0pt,align=left] at (0,{f(y-0.05)}) "
                  rf"{{Diviseurs positifs de ${n}$ :\\ {txt}}};")
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


def somme_multiples():
    """35 + 56 = 91 : 5 colonnes de 7 carreaux + 8 colonnes de 7 = 13 colonnes de 7."""
    u = 0.36
    L = [r"\begin{tikzpicture}"]
    for c in range(13):
        coul, bord = ("otSky", "otNavy") if c < 5 else ("otOrange!20", "otOrange!85!black")
        for r in range(7):
            L.append(rf"\filldraw[fill={coul},draw={bord},line width=.45pt] ({f(c*u+.03)},{f(r*u+.03)}) rectangle ({f((c+1)*u-.03)},{f((r+1)*u-.03)});")
    H = 7 * u
    br = r"decorate,decoration={brace,amplitude=5pt,raise=3pt}"
    L.append(rf"\draw[otNavy,line width=.7pt,{br}] (0,{f(H)}) -- ({f(5*u)},{f(H)});")
    L.append(rf"\node[anchor=south,text=otNavy] at ({f(2.5*u)},{f(H+.32)}) {{$35 = 7 \times 5$}};")
    L.append(rf"\draw[otOrange!85!black,line width=.7pt,{br}] ({f(5*u)},{f(H)}) -- ({f(13*u)},{f(H)});")
    L.append(rf"\node[anchor=south,text=otOrange!80!black] at ({f(9*u)},{f(H+.32)}) {{$56 = 7 \times 8$}};")
    L.append(rf"\draw[otGreenDark,line width=.7pt,{br}] ({f(13*u)},0) -- (0,0);")
    L.append(rf"\node[anchor=north,text=otGreenDark] at ({f(6.5*u)},-.34) {{$35 + 56 = 7 \times 13 = 91$}};")
    L.append(rf"\draw[cote] ({f(-.3)},0) -- ({f(-.3)},{f(H)});")
    L.append(rf"\node[anchor=east,text=otInk] at ({f(-.4)},{f(H/2)}) {{$7$}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def multiples_8():
    """Multiples de 8 sur une droite : 64 ≤ 70 < 72."""
    s = 0.15
    L = [r"\begin{tikzpicture}[shift={(-5.1,0)}]"]
    L.append(rf"\draw[otMuted,line width=.6pt,dash pattern=on 2pt off 2pt] ({f(34*s)},0) -- ({f(37*s)},0);")
    L.append(rf"\draw[otMuted,line width=.6pt,-{{Stealth[length=2.2mm]}}] ({f(37*s)},0) -- ({f(76*s)},0);")
    for m in range(40, 73, 8):
        coul = "otGreenDark" if m == 64 else ("otOrange!85!black" if m == 72 else "otNavy")
        L.append(rf"\fill[{coul}] ({f(m*s)},0) circle (2.3pt);")
        L.append(rf"\node[anchor=north,text={coul},font=\otRegular\fontsize{{9}}{{10}}\selectfont] at ({f(m*s)},-.15) {{{m}}};")
    L.append(rf"\draw[otInk,line width=.9pt] ({f(70*s)},-.16) -- ({f(70*s)},.16);")
    L.append(rf"\node[anchor=south,text=otInk] at ({f(70*s)},.2) {{$70$}};")
    L.append(rf"\draw[otGreenDark,line width=.5pt] ({f(64*s)},.12) -- ({f(64*s)},.55);")
    L.append(rf"\node[anchor=south east,text=otGreenDark] at ({f(64*s+.05)},.55) {{$8 \times 8 = 64 \le 70$}};")
    L.append(rf"\draw[otOrange!85!black,line width=.5pt] ({f(72*s)},.12) -- ({f(72*s)},1.15);")
    L.append(rf"\node[anchor=south east,text=otOrange!80!black] at ({f(72*s+.05)},1.15) {{$8 \times 9 = 72 > 70$}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def crible_20_39():
    c = 0.82
    L = [r"\begin{tikzpicture}"]
    for n in range(20, 40):
        r, k = divmod(n - 20, 10)
        x0, y0 = k * c, -(r + 1) * c
        if isprime(n):
            L.append(rf"\fill[otSky] ({f(x0)},{f(y0)}) rectangle ({f(x0+c)},{f(y0+c)});")
    L.append(rf"\draw[otRule,line width=.6pt] (0,{f(-2*c)}) grid[step={f(c)}] ({f(10*c)},0);")
    for n in range(20, 40):
        r, k = divmod(n - 20, 10)
        if isprime(n):
            L.append(rf"\draw[otNavy,line width=.9pt] ({f(k*c)},{f(-(r+1)*c)}) rectangle ({f((k+1)*c)},{f(-r*c)});")
    for n in range(20, 40):
        r, k = divmod(n - 20, 10)
        x, y = (k + .5) * c, -(r + .5) * c
        if isprime(n):
            L.append(rf"\node[text=otNavy,font=\otMedium\bfseries\fontsize{{10.5}}{{12}}\selectfont] at ({f(x)},{f(y)}) {{{n}}};")
        else:
            L.append(rf"\node[text=otMuted!70,font=\otRegular\fontsize{{10}}{{12}}\selectfont] at ({f(x)},{f(y)}) {{{n}}};")
    yl = -2 * c - 0.5
    L.append(rf"\node[anchor=west,text=otInk,align=left] at (0,{f(yl-0.25)}) "
             r"{en gris : multiples de $2$, de $3$ ou de $5$\\ en bleu : nombres premiers ($7^2 = 49 > 39$ : inutile de tester $7$)};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def parite_cours():
    """8 = 2 × 4 (pair) ; 9 = 2 × 4 + 1 (impair) : points rangés par deux."""
    e = 0.42
    L = [r"\begin{tikzpicture}"]
    for j, (nom, n) in enumerate([(r"$8 = 2 \times 4$ : pair", 8), (r"$9 = 2 \times 4 + 1$ : impair", 9)]):
        y0 = -j * 1.45
        for i in range(n // 2):
            for r in range(2):
                L.append(rf"\fill[otNavy] ({f(i*e)},{f(y0 + r*e)}) circle (4.2pt);")
        if n % 2:
            L.append(rf"\fill[otOrange] ({f((n//2)*e)},{f(y0)}) circle (4.2pt);")
        L.append(rf"\node[anchor=west,text=otInk] at ({f(5*e+.2)},{f(y0 + e/2)}) {{{nom}}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def somme_impairs():
    """7 + 5 = 12 : les deux points isolés forment une nouvelle paire."""
    e = 0.42
    L = [r"\begin{tikzpicture}"]
    # 7 = 2 × 3 + 1
    for i in range(3):
        for r in range(2):
            L.append(rf"\fill[otNavy] ({f(i*e)},{f(r*e)}) circle (4.2pt);")
    L.append(rf"\fill[otOrange] ({f(3*e)},0) circle (4.2pt);")
    L.append(rf"\node[anchor=south,text=otInk] at ({f(1.5*e)},{f(e+.25)}) {{$7 = 2 \times 3 + 1$}};")
    L.append(rf"\node[text=otInk,font=\Large] at ({f(5.0*e)},{f(e/2)}) {{$+$}};")
    x0 = 6.4 * e
    for i in range(2):
        for r in range(2):
            L.append(rf"\fill[otNavy] ({f(x0+i*e)},{f(r*e)}) circle (4.2pt);")
    L.append(rf"\fill[otOrange] ({f(x0+2*e)},0) circle (4.2pt);")
    L.append(rf"\node[anchor=south,text=otInk] at ({f(x0+1*e)},{f(e+.25)}) {{$5 = 2 \times 2 + 1$}};")
    L.append(rf"\node[text=otInk,font=\Large] at ({f(x0+3.3*e)},{f(e/2)}) {{$=$}};")
    x1 = x0 + 4.4 * e
    for i in range(5):
        for r in range(2):
            L.append(rf"\fill[otNavy] ({f(x1+i*e)},{f(r*e)}) circle (4.2pt);")
    L.append(rf"\fill[otGreenDark] ({f(x1+5*e)},0) circle (4.2pt);")
    L.append(rf"\fill[otGreenDark] ({f(x1+5*e)},{f(e)}) circle (4.2pt);")
    L.append(rf"\draw[otGreenDark,line width=.8pt,rounded corners=4pt] ({f(x1+5*e-.2)},-.2) rectangle ({f(x1+5*e+.2)},{f(e+.2)});")
    L.append(rf"\node[anchor=south,text=otGreenDark] at ({f(x1+2.5*e)},{f(e+.25)}) {{$12 = 2 \times 6$ : pair}};")
    L.append(rf"\node[anchor=north,text=otGreenDark,align=center] at ({f(x1+5*e)},-.3) {{les deux points isolés\\forment une paire}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def frise_feux():
    """Feux toutes les 45 s et toutes les 60 s : ensemble à 0 et 180 s."""
    s = 0.04
    T = 190
    L = [r"\begin{tikzpicture}"]
    yA, yB = 1.0, 0.5
    for t in (0, 180):
        L.append(rf"\draw[otGreenDark,line width=.8pt,dash pattern=on 2.5pt off 1.8pt] ({f(t*s)},0) -- ({f(t*s)},{f(yA+0.3)});")
    L.append(rf"\draw[otMuted,line width=.7pt,-{{Stealth[length=2.3mm]}}] (0,0) -- ({f(T*s+0.3)},0);")
    L.append(rf"\node[anchor=west,text=otMuted] at ({f(T*s+0.35)},0) {{$t$ (s)}};")
    for t in range(0, 181, 15):
        coul = "otGreenDark" if t in (0, 180) else "otMuted"
        L.append(rf"\draw[{coul},line width=.6pt] ({f(t*s)},-0.08) -- ({f(t*s)},0.08);")
    for t in (0, 45, 60, 90, 120, 135, 180):
        coul = "otGreenDark" if t in (0, 180) else "otMuted"
        L.append(rf"\node[anchor=north,text={coul},font=\otMedium\fontsize{{9}}{{11}}\selectfont] at ({f(t*s)},-0.14) {{{t}}};")
    for t in range(0, 181, 45):
        L.append(rf"\fill[otNavy] ({f(t*s)},{f(yA)}) circle (2.6pt);")
    for t in range(0, 181, 60):
        L.append(rf"\fill[otOrange] ({f(t*s)},{f(yB)}) circle (2.6pt);")
    L.append(r"\fill[otNavy] (0.1,2.35) circle (2.6pt);")
    L.append(r"\node[anchor=west,text=otInk] at (0.25,2.35) {feu 1 : toutes les $45$ s};")
    L.append(r"\fill[otOrange] (0.1,1.85) circle (2.6pt);")
    L.append(r"\node[anchor=west,text=otInk] at (0.25,1.85) {feu 2 : toutes les $60$ s};")
    L.append(rf"\node[anchor=south,text=otGreenDark] at ({f(180*s)},{f(yA+0.35)}) {{ensemble à $180$ s}};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES = {
    "ex_diviseurs_24": rectangles(24, [(24, 1, "otSky"), (12, 2, "otGreen!14"), (8, 3, "otOrange!14"),
                                       (6, 4, "otSky")]),
    "ex_somme_multiples": somme_multiples(),
    "ex_multiples_8": multiples_8(),
    "ex_crible_20_39": crible_20_39(),
    "parite_cours": parite_cours(),
    "ex_somme_impairs": somme_impairs(),
    "ex_feux": frise_feux(),
    "diviseurs_36": rectangles_36(),
    "crible_100": crible(),
    "arbre_360": arbre(360, [(2, 180), (2, 90), (2, 45), (3, 15), (3, 5)],
                       resultat=r"360 = 2^3 \times 3^2 \times 5"),
    "arbre_120": arbre(120, [(2, 60), (2, 30), (2, 15), (3, 5)],
                       resultat=r"120 = 2^3 \times 3 \times 5"),
    "guirlandes": frise(),
}
