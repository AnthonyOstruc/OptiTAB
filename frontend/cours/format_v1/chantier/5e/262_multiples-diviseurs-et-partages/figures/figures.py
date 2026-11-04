# -*- coding: utf-8 -*-
"""Figures de la notion 262 (5e : multiples, diviseurs et partages), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Convention : énoncé = données seules ; corrigé = éléments de réponse en vert (otGreenDark).
"""
from sympy import isprime

VERT = "otGreenDark"


def f(x):
    """Nombre décimal pour TikZ (point décimal, 3 chiffres)."""
    return f"{x:.3f}".rstrip("0").rstrip(".")


def tikz(lignes):
    return "\\begin{tikzpicture}\n" + "\n".join(lignes) + "\n\\end{tikzpicture}"


# ====================================================================== division posée
def etapes_division(a, b):
    """Étapes de la division posée « à la française » de a par b.

    Renvoie (q, r, etapes) avec etapes = [(fin, partiel, produit, reste)] :
    fin = indice (dans les chiffres de a) du dernier chiffre utilisé par le partiel.
    """
    ch = str(a)
    k = 1
    while int(ch[:k]) < b and k < len(ch):
        k += 1
    partiel = int(ch[:k])
    fin = k - 1
    etapes, qs = [], ""
    while True:
        qd = partiel // b
        prod = qd * b
        reste = partiel - prod
        etapes.append((fin, partiel, prod, reste))
        qs += str(qd)
        if fin == len(ch) - 1:
            break
        fin += 1
        partiel = reste * 10 + int(ch[fin])
    q, r = int(qs), etapes[-1][3]
    assert divmod(a, b) == (q, r), (a, b, q, r)
    return q, r, etapes


def division(a, b, mode="cours", xs=0.33, ys=0.56):
    """Division posée de a par b.

    mode : 'annote'  (cours, fiche : noms des termes autour de la potence)
           'enonce'  (tout est écrit, sans les noms)
           'corrige' (calculs, quotient et reste en vert, égalité finale)
           'corrige_noms' (comme 'annote', noms et résultats en vert)
    """
    q, r, etapes = etapes_division(a, b)
    ch = str(a)
    n = len(ch)
    vert = mode.startswith("corrige")
    cc = VERT if vert else "otInk"          # couleur des calculs
    cr = VERT if vert else "otNavy"         # couleur du quotient et du reste
    police = r"\fontsize{12.5}{14}\selectfont"
    L = []

    def chiffres(nombre, fin, row, coul, gras=False):
        s = str(nombre)
        for i, c in enumerate(s):
            col = fin - (len(s) - 1) + i
            g = r"\bfseries" if gras else ""
            L.append(rf"\node[text={coul},font={police}{g}] at ({f(col*xs)},{f(-row*ys)}) {{${c}$}};")

    # dividende
    for i, c in enumerate(ch):
        L.append(rf"\node[text=otInk,font={police}] at ({f(i*xs)},0) {{${c}$}};")
    row = 0
    for j, (fin, partiel, prod, reste) in enumerate(etapes):
        if j > 0:
            # partiel = reste précédent suivi du chiffre abaissé
            chiffres(partiel if etapes[j-1][3] else f"0{ch[fin]}", fin, row, cc)
        row += 1
        chiffres(prod, fin, row, cc)
        debut = fin - (len(str(prod)) - 1)
        L.append(rf"\node[text={cc},font={police}] at ({f((debut-1)*xs)},{f(-row*ys)}) {{$-$}};")
        L.append(rf"\draw[{cc},line width=.6pt] ({f((debut-1.45)*xs)},{f(-row*ys-0.29)}) -- ({f((fin+0.45)*xs)},{f(-row*ys-0.29)});")
        row += 1
    # dernier reste
    fin = etapes[-1][0]
    chiffres(r, fin, row, cr, gras=True)
    rows = row
    # potence
    xb = (n - 0.35) * xs + 0.12
    larg = max(len(str(b)), len(str(q))) * xs + 0.55
    L.append(rf"\draw[otNavy,line width=.9pt] ({f(xb)},0.32) -- ({f(xb)},{f(-rows*ys-0.25)});")
    L.append(rf"\draw[otNavy,line width=.9pt] ({f(xb)},-0.29) -- ({f(xb+larg)},-0.29);")
    for i, c in enumerate(str(b)):
        L.append(rf"\node[text=otInk,font={police}] at ({f(xb+0.3+i*xs)},0) {{${c}$}};")
    for i, c in enumerate(str(q)):
        L.append(rf"\node[text={cr},font={police}\bfseries] at ({f(xb+0.3+i*xs)},{f(-ys)}) {{${c}$}};")
    xq = xb + 0.3 + (len(str(q)) - 1) * xs      # dernier chiffre du quotient
    if mode in ("annote", "corrige_noms"):
        cl = VERT if vert else "otNavy"
        fl = rf"{cl},line width=.6pt,-{{Stealth[length=1.6mm]}}"
        xg = -0.55                               # bord gauche des chiffres
        # dividende (à gauche de la 1re ligne)
        L.append(rf"\node[anchor=east,text={cl}] (ld) at ({f(xg-0.3)},0) {{dividende}};")
        L.append(rf"\draw[{fl}] (ld.east) -- ({f(-0.2)},0);")
        # reste (à gauche de la dernière ligne)
        xr = (fin - len(str(r)) + 1) * xs
        L.append(rf"\node[anchor=east,text={cl}] (lr) at ({f(xg-0.3)},{f(-rows*ys)}) {{reste}};")
        L.append(rf"\draw[{fl}] (lr.east) -- ({f(xr-0.2)},{f(-rows*ys)});")
        # diviseur et quotient (à droite)
        xd = xb + 0.3 + (len(str(b)) - 1) * xs
        xdroite = xb + larg + 0.4
        L.append(rf"\node[anchor=west,text={cl}] (lb) at ({f(xdroite)},0) {{diviseur}};")
        L.append(rf"\draw[{fl}] (lb.west) -- ({f(xd+0.2)},0);")
        L.append(rf"\node[anchor=west,text={cl}] (lq) at ({f(xdroite)},{f(-ys)}) {{quotient}};")
        L.append(rf"\draw[{fl}] (lq.west) -- ({f(xq+0.2)},{f(-ys)});")
    if mode != "enonce":
        coul = VERT if vert else "otNavy"
        ytxt = -rows * ys - 0.75
        L.append(rf"\node[anchor=north,text={coul}] at ({f((xb)/2 + 0.6)},{f(ytxt)}) "
                 rf"{{${a} = {b} \times {q} + {r}$ \quad avec \quad ${r} < {b}$}};")
    return tikz(L)


# ====================================================================== jetons en paquets
def paquets_cours():
    """23 jetons : 4 paquets de 5 et un reste de 3."""
    e = 0.32
    L = []
    w = e + 0.28                 # paquets verticaux : 5 jetons empilés
    pas = w + 0.3
    H = 5 * e + 0.2
    for s in range(4):
        x0 = s * pas
        L.append(rf"\draw[otNavy,line width=.8pt,rounded corners=4pt,fill=otSky] ({f(x0)},0) rectangle ({f(x0+w)},{f(H)});")
        for i in range(5):
            L.append(rf"\fill[otNavy] ({f(x0 + w/2)},{f(0.26 + i*e)}) circle (3.8pt);")
    x0 = 4 * pas + 0.2
    for i in range(3):
        L.append(rf"\fill[otOrange] ({f(x0 + w/2)},{f(0.26 + i*e)}) circle (3.8pt);")
    br = r"decorate,decoration={brace,amplitude=5pt,raise=3pt,mirror}"
    L.append(rf"\draw[otNavy,line width=.7pt,{br}] (0,0) -- ({f(4*pas-0.3)},0);")
    L.append(rf"\node[anchor=north,text=otNavy,align=center] at ({f((4*pas-0.3)/2)},-0.32) {{$4$ paquets de $5$\\$= 20$ jetons}};")
    L.append(rf"\node[anchor=north,text=otOrange!80!black,align=center] at ({f(x0+w/2)},-0.32) {{reste\\$3$}};")
    L.append(rf"\node[anchor=south west,text=otInk] at (0,{f(H+0.2)}) {{$23 = 5 \times 4 + 3$}};")
    return tikz(L)


# ====================================================================== rectangles de diviseurs
def rectangles(n, formes, u=0.2, corrige=False):
    """Rangements de n carreaux en rectangles l × h ; formes = [(l, h, couleur), …]."""
    trait = VERT if corrige else "otNavy"
    grille = "otGreenDark!35" if corrige else "otNavy!35"
    L = []
    y = 0.0
    for (l, h, coul) in formes:
        long = l * u > 3.2
        if long:
            L.append(rf"\node[anchor=north west,text=otInk,inner sep=1pt] at (0,{f(y)}) {{${n} = {l} \times {h}$}};")
            y -= 0.5
        y -= h * u
        x1, y1 = l * u, y + h * u
        L.append(rf"\fill[{coul}] (0,{f(y)}) rectangle ({f(x1)},{f(y1)});")
        for i in range(1, l):
            L.append(rf"\draw[{grille},line width=.3pt] ({f(i*u)},{f(y)}) -- ({f(i*u)},{f(y1)});")
        for j in range(1, h):
            L.append(rf"\draw[{grille},line width=.3pt] (0,{f(y+j*u)}) -- ({f(x1)},{f(y+j*u)});")
        L.append(rf"\draw[{trait},line width=.75pt] (0,{f(y)}) rectangle ({f(x1)},{f(y1)});")
        if not long:
            L.append(rf"\node[anchor=west,text=otInk] at ({f(x1+0.18)},{f(y+h*u/2)}) {{${n} = {l} \times {h}$}};")
        y -= 0.3
    divs = sorted({d for (l, h, _) in formes for d in (l, h)})
    txt = " ; ".join(f"${d}$" for d in divs)
    coul = VERT if corrige else "otNavy"
    L.append(rf"\node[anchor=north west,text={coul},inner sep=0pt,align=left] at (0,{f(y-0.05)}) "
             rf"{{Diviseurs de ${n}$ :\\ {txt}}};")
    return tikz(L)


# ====================================================================== crible
def crible(nmax, mode, c=0.8):
    """mode : 'cours' (premiers sur fond bleu), 'enonce' (sans marquage), 'corrige' (premiers en vert)."""
    L = []
    lignes = (nmax + 9) // 10
    for n in range(1, nmax + 1):
        r, k = divmod(n - 1, 10)
        x0, y0 = k * c, -(r + 1) * c
        if isprime(n) and mode != "enonce":
            fond = "otSky" if mode == "cours" else "otGreen!22"
            L.append(rf"\fill[{fond}] ({f(x0)},{f(y0)}) rectangle ({f(x0+c)},{f(y0+c)});")
    L.append(rf"\draw[otRule,line width=.6pt] (0,{f(-lignes*c)}) grid[step={f(c)}] ({f(10*c)},0);")
    if mode != "enonce":
        bord = "otNavy" if mode == "cours" else VERT
        for n in range(1, nmax + 1):
            if isprime(n):
                r, k = divmod(n - 1, 10)
                L.append(rf"\draw[{bord},line width=.9pt] ({f(k*c)},{f(-(r+1)*c)}) rectangle ({f((k+1)*c)},{f(-r*c)});")
    for n in range(1, nmax + 1):
        r, k = divmod(n - 1, 10)
        x, y = (k + .5) * c, -(r + .5) * c
        if mode == "enonce":
            L.append(rf"\node[text=otInk,font=\otRegular\fontsize{{10}}{{12}}\selectfont] at ({f(x)},{f(y)}) {{{n}}};")
        elif isprime(n):
            coul = "otNavy" if mode == "cours" else VERT
            L.append(rf"\node[text={coul},font=\otMedium\bfseries\fontsize{{10.5}}{{12}}\selectfont] at ({f(x)},{f(y)}) {{{n}}};")
        else:
            L.append(rf"\node[text=otMuted!70,font=\otRegular\fontsize{{10}}{{12}}\selectfont] at ({f(x)},{f(y)}) {{{n}}};")
    if mode != "enonce":
        nb = sum(1 for n in range(2, nmax + 1) if isprime(n))
        fond = "otSky" if mode == "cours" else "otGreen!22"
        bord = "otNavy" if mode == "cours" else VERT
        yl = -lignes * c - .55
        L.append(rf"\fill[{fond}] (0,{f(yl-.2)}) rectangle (.4,{f(yl+.2)});")
        L.append(rf"\draw[{bord},line width=.9pt] (0,{f(yl-.2)}) rectangle (.4,{f(yl+.2)});")
        coul = "otInk" if mode == "cours" else VERT
        L.append(rf"\node[anchor=west,text={coul}] at (.55,{f(yl)}) {{nombre premier : il y en a ${nb}$ inférieurs à ${nmax}$}};")
    return tikz(L)


# ====================================================================== lots identiques
def jeton(x, y, sorte):
    """'rond' (orange) ou 'carre' (bleu)."""
    if sorte == "rond":
        return rf"\fill[otOrange] ({f(x)},{f(y)}) circle (3.6pt);"
    return rf"\fill[otNavy] ({f(x-0.1)},{f(y-0.1)}) rectangle ({f(x+0.1)},{f(y+0.1)});"


def stock(n, sorte, cols, x0, y0, e=0.3):
    """n jetons en grille de cols colonnes, coin haut gauche (x0, y0)."""
    L = []
    for i in range(n):
        r, k = divmod(i, cols)
        L.append(jeton(x0 + 0.15 + k * e, y0 - 0.15 - r * e, sorte))
    return L


def lots(n1, n2, nb, noms, corrige, cols1, cols2, par_ligne=3, cadre="otNavy", fond="otSky"):
    """Énoncé : les deux stocks ; corrigé (ou cours) : nb lots identiques encadrés."""
    e = 0.3
    L = []
    if not corrige:
        h1 = ((n1 + cols1 - 1) // cols1) * e
        h2 = ((n2 + cols2 - 1) // cols2) * e
        L += stock(n1, "rond", cols1, 0, 0)
        L.append(rf"\node[anchor=north,text=otInk] at ({f(cols1*e/2)},{f(-h1-0.15)}) {{${n1}$ {noms[0]}}};")
        x2 = cols1 * e + 1.0
        L += stock(n2, "carre", cols2, x2, 0)
        L.append(rf"\node[anchor=north,text=otInk] at ({f(x2+cols2*e/2)},{f(-h2-0.15)}) {{${n2}$ {noms[1]}}};")
        return tikz(L)
    a, b = n1 // nb, n2 // nb
    largeur = max(a, b) * e + 0.3
    hauteur = 2 * e + 0.3
    for s in range(nb):
        r, k = divmod(s, par_ligne)
        x0, y0 = k * (largeur + 0.3), -r * (hauteur + 0.3)
        L.append(rf"\draw[{cadre},line width=.8pt,rounded corners=4pt,fill={fond}] ({f(x0)},{f(y0)}) rectangle ({f(x0+largeur)},{f(y0-hauteur)});")
        for i in range(a):
            L.append(jeton(x0 + 0.3 + i * e, y0 - 0.3, "rond"))
        for i in range(b):
            L.append(jeton(x0 + 0.3 + i * e, y0 - 0.3 - e, "carre"))
    rangs = (nb + par_ligne - 1) // par_ligne
    ybas = -rangs * (hauteur + 0.3) + 0.15
    coul = VERT if cadre == VERT else "otNavy"
    L.append(rf"\node[anchor=north west,text={coul},align=left] at (0,{f(ybas)}) "
             rf"{{${nb}$ lots identiques :\\ ${a}$ {noms[0]} et ${b}$ {noms[1]} dans chaque lot}};")
    return tikz(L)


# ====================================================================== œufs en boîtes
def oeuf(x, y, coul="otOrange!80!black", fond="otOrange!18"):
    return rf"\draw[{coul},line width=.6pt,fill={fond}] ({f(x)},{f(y)}) ellipse (0.105 and 0.135);"


def oeufs(corrige):
    """38 œufs ; boîtes de 6 (2 rangées de 3)."""
    e = 0.34
    L = []
    if not corrige:
        for i in range(38):
            r, k = divmod(i, 10)
            L.append(oeuf(0.2 + k * e, -0.2 - r * e))
        L.append(rf"\node[anchor=north,text=otInk] at ({f(0.2 + 4.5*e)},{f(-0.2 - 3*e - 0.25)}) {{$38$ œufs}};")
        # une boîte vide de 6
        x0 = 10 * e + 0.9
        L.append(rf"\draw[otNavy,line width=.8pt,rounded corners=3pt,fill=otSky] ({f(x0)},-0.25) rectangle ({f(x0+3*e+0.2)},{f(-0.25-2*e-0.2)});")
        for i in range(6):
            r, k = divmod(i, 3)
            L.append(rf"\draw[otNavy!45,line width=.5pt,fill=white] ({f(x0+0.1+e/2+k*e)},{f(-0.35-e/2-r*e)}) circle (0.12);")
        L.append(rf"\node[anchor=north,text=otInk,align=center] at ({f(x0+(3*e+0.2)/2)},{f(-0.25-2*e-0.3)}) {{une boîte :\\ $6$ places}};")
        return tikz(L)
    lb, hb = 3 * e + 0.2, 2 * e + 0.2          # taille d'une boîte
    pas, pasy = lb + 0.25, hb + 0.25
    for s in range(6):                          # 2 rangées de 3 boîtes
        r0, k0 = divmod(s, 3)
        x0, y0 = k0 * pas, -r0 * pasy
        L.append(rf"\draw[{VERT},line width=.8pt,rounded corners=3pt,fill=otGreen!12] ({f(x0)},{f(y0)}) rectangle ({f(x0+lb)},{f(y0-hb)});")
        for i in range(6):
            r, k = divmod(i, 3)
            L.append(oeuf(x0 + 0.1 + e/2 + k*e, y0 - 0.1 - e/2 - r*e))
    x0 = 3 * pas + 0.25
    ym = -(hb + pasy) / 2                       # milieu vertical des deux rangées
    for i in range(2):
        L.append(oeuf(x0 + 0.15 + i * e, ym + 0.25))
    L.append(rf"\node[anchor=north,text=otOrange!80!black,align=center] at ({f(x0+0.15+e/2)},{f(ym)}) {{reste\\$2$ œufs}};")
    br = r"decorate,decoration={brace,amplitude=5pt,raise=3pt,mirror}"
    yb = -pasy - hb
    L.append(rf"\draw[{VERT},line width=.7pt,{br}] (0,{f(yb)}) -- ({f(3*pas-0.25)},{f(yb)});")
    L.append(rf"\node[anchor=north,text={VERT},align=center] at ({f((3*pas-0.25)/2)},{f(yb-0.32)}) {{$6$ boîtes pleines\\$= 36$ œufs}};")
    L.append(rf"\node[anchor=south west,text={VERT}] at (0,0.15) {{$38 = 6 \times 6 + 2$}};")
    return tikz(L)


# ====================================================================== navettes (frise)
def navettes():
    s = 0.1                        # cm par minute ; t = minutes après 9 h 10
    T = 64
    L = []
    yA, yB = 1.05, 0.55
    communs = [16, 40, 64]
    for t in communs:
        L.append(rf"\draw[{VERT},line width=.8pt,dash pattern=on 2.5pt off 1.8pt] ({f(t*s)},0) -- ({f(t*s)},{f(yA+0.3)});")
    L.append(rf"\draw[otMuted,line width=.7pt,-{{Stealth[length=2.3mm]}}] (-0.1,0) -- ({f(T*s+0.5)},0);")
    for t in range(0, T + 1, 4):
        L.append(rf"\draw[otMuted,line width=.5pt] ({f(t*s)},-0.06) -- ({f(t*s)},0.06);")
    L.append(rf"\node[anchor=north,text=otMuted,font=\otRegular\fontsize{{9}}{{10}}\selectfont] at (0,-0.14) {{9 h 10}};")
    for t, h in zip(communs, ["9 h 26", "9 h 50", "10 h 14"]):
        L.append(rf"\node[anchor=north,text={VERT},font=\otMedium\bfseries\fontsize{{9.5}}{{11}}\selectfont] at ({f(t*s)},-0.14) {{{h}}};")
    for t in range(0, T + 1, 8):
        L.append(rf"\fill[otNavy] ({f(t*s)},{f(yA)}) circle (2.6pt);")
    for t in range(4, T + 1, 12):
        L.append(rf"\fill[otOrange] ({f(t*s)},{f(yB)}) circle (2.6pt);")
    L.append(rf"\node[anchor=east,text=otNavy] at (-0.2,{f(yA)}) {{A}};")
    L.append(rf"\node[anchor=east,text=otOrange!80!black] at (-0.2,{f(yB)}) {{B}};")
    L.append(r"\fill[otNavy] (0.1,2.4) circle (2.6pt);")
    L.append(r"\node[anchor=west,text=otInk] at (0.25,2.4) {navette A : toutes les $8$ min};")
    L.append(r"\fill[otOrange] (0.1,1.9) circle (2.6pt);")
    L.append(r"\node[anchor=west,text=otInk] at (0.25,1.9) {navette B : toutes les $12$ min};")
    L.append(rf"\node[anchor=north,text={VERT}] at ({f(T*s/2)},-0.65) {{départs simultanés : toutes les $24$ min}};")
    return tikz(L)


FIGURES = {
    # cours et fiche
    "division_cours": division(158, 7, "annote"),
    "paquets_cours": paquets_cours(),
    "diviseurs_24": rectangles(24, [(24, 1, "otSky"), (12, 2, "otGreen!14"), (8, 3, "otOrange!14"),
                                    (6, 4, "otSky")], u=0.2),
    "crible_50": crible(50, "cours"),
    "lots_cours": lots(12, 18, 6, ("billes", "cubes"), True, 6, 6, par_ligne=3),
    # exercices
    "div347_enonce": division(347, 9, "enonce"),
    "div347_corrige": division(347, 9, "corrige_noms"),
    "div254_corrige": division(254, 6, "corrige"),
    "div213_corrige": division(213, 9, "corrige"),
    "diviseurs_36": rectangles(36, [(36, 1, "otGreen!14"), (18, 2, "otGreen!14"), (12, 3, "otGreen!14"),
                                    (9, 4, "otGreen!14"), (6, 6, "otGreen!14")], u=0.17, corrige=True),
    "crible50_enonce": crible(50, "enonce"),
    "crible50_corrige": crible(50, "corrige"),
    "oeufs_enonce": oeufs(False),
    "oeufs_corrige": oeufs(True),
    "bonbons_enonce": lots(18, 30, 6, ("sucettes", "caramels"), False, 6, 10),
    "bonbons_corrige": lots(18, 30, 6, ("sucettes", "caramels"), True, 6, 10, par_ligne=3,
                            cadre=VERT, fond="otGreen!12"),
    "navettes_corrige": navettes(),
}
