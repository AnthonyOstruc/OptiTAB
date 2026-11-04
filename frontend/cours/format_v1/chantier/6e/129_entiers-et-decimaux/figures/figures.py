# -*- coding: utf-8 -*-
"""Figures de la notion 129 (6e : entiers et décimaux), style des livres.

Compilées par outils/figures_livre.py. Tableaux de numération (entiers par
classes, décimaux avec partie entière / partie décimale), bandes et carrés
partagés en 10 et en 100, droites graduées au dixième avec loupe au centième,
chiffre et « nombre de » repérés sur un grand nombre.
Énoncé : jamais la réponse. Corrigé : éléments de réponse en vert (otGreenDark).
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grad/.style={otMuted,line width=.5pt},
  gradTexte/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=north,inner sep=1pt},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont},
  entete/.style={font=\otMedium\fontsize{8.5}{10}\selectfont,text=otNavy,inner sep=1pt},
  rang/.style={font=\otRegular\fontsize{7.5}{9}\selectfont,text=otMuted,inner sep=1pt},
  loupe/.style={otMuted!80,line width=.5pt,dash pattern=on 2.5pt off 1.8pt},
  accol/.style={line width=.75pt,decorate,decoration={brace,amplitude=5pt}},
}
"""

VERT = "otGreenDark"
NAVY = "otNavy"
ORANGE = "otOrange!90!black"


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def nb(v, dec=3):
    """Nombre décimal écrit en LaTeX (virgule décimale)."""
    s = ("%.*f" % (dec, v)).rstrip("0").rstrip(".")
    return s.replace(".", "{,}")


FIGURES = {}


# ===================================================================== tableau des entiers
CLASSES = ["milliards", "millions", "mille", "unités"]


def tableau_entiers(chiffres="", couleur=NAVY, w=.58, x0=0.0, y0=0.0):
    """Tableau de numération des entiers : 4 classes × (c, d, u).

    chiffres : écriture du nombre sans espace, alignée à droite (vide = tableau vierge).
    """
    n = 12
    h1, h2, h3 = .52, .42, .62
    W = n * w
    s = []
    # fonds des en-têtes
    s.append(r"\fill[otSky] (%s,%s) rectangle (%s,%s);" % (f(x0), f(y0 + h3), f(x0 + W), f(y0 + h3 + h2 + h1)))
    # filets horizontaux
    for yy in (0, h3, h3 + h2, h3 + h2 + h1):
        s.append(r"\draw[otNavy!45,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(x0), f(y0 + yy), f(x0 + W), f(y0 + yy)))
    # filets verticaux : fins entre rangs, épais entre classes
    for k in range(n + 1):
        x = x0 + k * w
        if k % 3 == 0:
            s.append(r"\draw[otNavy,line width=.9pt] (%s,%s) -- (%s,%s);" % (f(x), f(y0), f(x), f(y0 + h3 + h2 + h1)))
        else:
            s.append(r"\draw[otNavy!35,line width=.4pt] (%s,%s) -- (%s,%s);" % (f(x), f(y0), f(x), f(y0 + h3 + h2)))
    for c, nom in enumerate(CLASSES):
        s.append(r"\node[entete] at (%s,%s) {%s};" % (f(x0 + (3 * c + 1.5) * w), f(y0 + h3 + h2 + h1 / 2), nom))
        for j, r in enumerate("cdu"):
            s.append(r"\node[rang] at (%s,%s) {%s};" % (f(x0 + (3 * c + j + .5) * w), f(y0 + h3 + h2 / 2), r))
    if chiffres:
        dep = n - len(chiffres)
        for k, ch in enumerate(chiffres):
            s.append(r"\node[text=%s,inner sep=1pt,font=\large] at (%s,%s) {$%s$};"
                     % (couleur, f(x0 + (dep + k + .5) * w), f(y0 + h3 / 2), ch))
    return "\n".join(s)


def fig_tableau_entiers(chiffres="", couleur=NAVY, note=None):
    s = [r"\begin{tikzpicture}", tableau_entiers(chiffres, couleur)]
    if note:
        s.append(r"\node[anchor=north,text=%s,inner sep=1pt] at (%s,-.18) {%s};" % (note[1], f(12 * .58 / 2), note[0]))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


# ===================================================================== tableau des décimaux
RANGS_DEC = ["centaines", "dizaines", "unités", "dixièmes", "centièmes", "millièmes"]
VALEURS_DEC = [r"100", r"10", r"1", r"\dfrac{1}{10}", r"\dfrac{1}{100}", r"\dfrac{1}{1\,000}"]


def tableau_decimal(chiffres=None, couleur=NAVY, w=1.0, x0=0.0, y0=0.0):
    """Tableau de numération décimal : 3 rangs entiers | 3 rangs décimaux.

    chiffres : liste de 6 chaînes (ou "" pour une case vide), de centaines à millièmes.
    La virgule est écrite dans la case des unités, à droite du chiffre.
    """
    h1, h2, h3, h4 = .5, 1.68, .8, .64
    W = 6 * w
    H = h4 + h3 + h2 + h1
    s = []
    s.append(r"\fill[otSky] (%s,%s) rectangle (%s,%s);" % (f(x0), f(y0 + h4), f(x0 + W), f(y0 + H)))
    for yy in (0, h4, h4 + h3, h4 + h3 + h2, H):
        s.append(r"\draw[otNavy!45,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(x0), f(y0 + yy), f(x0 + W), f(y0 + yy)))
    for k in range(7):
        x = x0 + k * w
        if k in (0, 3, 6):
            s.append(r"\draw[otNavy,line width=%s] (%s,%s) -- (%s,%s);" % ("1.3pt" if k == 3 else ".9pt", f(x), f(y0), f(x), f(y0 + H)))
        else:
            s.append(r"\draw[otNavy!35,line width=.4pt] (%s,%s) -- (%s,%s);" % (f(x), f(y0), f(x), f(y0 + h4 + h3 + h2)))
    s.append(r"\node[entete] at (%s,%s) {Partie entière};" % (f(x0 + 1.5 * w), f(y0 + h4 + h3 + h2 + h1 / 2)))
    s.append(r"\node[entete] at (%s,%s) {Partie décimale};" % (f(x0 + 4.5 * w), f(y0 + h4 + h3 + h2 + h1 / 2)))
    for j, (r, v) in enumerate(zip(RANGS_DEC, VALEURS_DEC)):
        s.append(r"\node[rang,rotate=90,font=\otRegular\fontsize{8}{9}\selectfont] at (%s,%s) {%s};" % (f(x0 + (j + .5) * w), f(y0 + h4 + h3 + h2 / 2), r))
        s.append(r"\node[text=otMuted,inner sep=1pt,font=\small] at (%s,%s) {$%s$};" % (f(x0 + (j + .5) * w), f(y0 + h4 + h3 / 2), v))
    if chiffres:
        for j, ch in enumerate(chiffres):
            if ch == "":
                continue
            xc = x0 + (j + .5) * w
            s.append(r"\node[text=%s,inner sep=1pt,font=\large] (d%d) at (%s,%s) {$%s$};" % (couleur, j, f(xc), f(y0 + h4 / 2), ch))
            if j == 2:
                s.append(r"\node[text=%s,inner sep=0pt,font=\large,anchor=base west] at ([xshift=-1pt]d2.base east) {$,$};" % couleur)
    return "\n".join(s)


def fig_tableau_decimal(chiffres=None, couleur=NAVY, note=None):
    s = [r"\begin{tikzpicture}", tableau_decimal(chiffres, couleur)]
    if note:
        s.append(r"\node[anchor=north,text=%s,inner sep=1pt,align=center] at (%s,-.2) {%s};" % (note[1], f(3 * 1.0), note[0]))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


# ===================================================================== bandes et carrés
def bande(x0, y0, parts_col, L=3.2, h=.55, coul="otNavy!40"):
    """Bande unité partagée en 10 ; parts_col premières parts coloriées."""
    p = L / 10
    s = []
    if parts_col:
        s.append(r"\fill[%s] (%s,%s) rectangle (%s,%s);" % (coul, f(x0), f(y0), f(x0 + parts_col * p), f(y0 + h)))
    for k in range(1, 10):
        s.append(r"\draw[otNavy!45,line width=.4pt] (%s,%s) -- (%s,%s);" % (f(x0 + k * p), f(y0), f(x0 + k * p), f(y0 + h)))
    s.append(r"\draw[otNavy,line width=.9pt] (%s,%s) rectangle (%s,%s);" % (f(x0), f(y0), f(x0 + L), f(y0 + h)))
    return "\n".join(s)


def carre(x0, y0, colonnes=0, cases=0, c=.22, coul="otNavy!40", coul_cases=None, cases_col=None):
    """Carré unité partagé en 100 : « colonnes » colonnes pleines puis « cases » cases
    dans la colonne suivante (de bas en haut)."""
    coul_cases = coul_cases or coul
    s = []
    if colonnes:
        s.append(r"\fill[%s] (%s,%s) rectangle (%s,%s);" % (coul, f(x0), f(y0), f(x0 + colonnes * c), f(y0 + 10 * c)))
    for k in range(cases):
        xx = x0 + (colonnes if cases_col is None else cases_col) * c
        s.append(r"\fill[%s] (%s,%s) rectangle (%s,%s);" % (coul_cases, f(xx), f(y0 + k * c), f(xx + c), f(y0 + (k + 1) * c)))
    for k in range(1, 10):
        s.append(r"\draw[otNavy!30,line width=.3pt] (%s,%s) -- (%s,%s);" % (f(x0 + k * c), f(y0), f(x0 + k * c), f(y0 + 10 * c)))
        s.append(r"\draw[otNavy!30,line width=.3pt] (%s,%s) -- (%s,%s);" % (f(x0), f(y0 + k * c), f(x0 + 10 * c), f(y0 + k * c)))
    s.append(r"\draw[otNavy,line width=.9pt] (%s,%s) rectangle (%s,%s);" % (f(x0), f(y0), f(x0 + 10 * c), f(y0 + 10 * c)))
    return "\n".join(s)


# ===================================================================== droites graduées
def droite(a, b, U, y=0.0, pas=.1, labels=(), x0=0.0, fleche=True, lab_dec=1):
    """Droite graduée horizontale de a à b (U cm par unité), graduations tous les « pas ».
    Graduations longues aux multiples de 10 × pas (et aux bornes), moyennes à 5 × pas.
    Renvoie (code, X)."""
    X = lambda v: x0 + U * (v - a)
    s = []
    fin = X(b) + (.45 if fleche else 0)
    s.append(r"\draw[%s] (%s,%s) -- (%s,%s);" % ("axe" if fleche else "grad", f(X(a) - .25), f(y), f(fin), f(y)))
    n = int(round((b - a) / pas))
    for i in range(n + 1):
        v = a + i * pas
        k = int(round(v / pas))
        if k % 10 == 0 or i in (0, n):
            h = .14
        elif k % 5 == 0:
            h = .1
        else:
            h = .065
        s.append(r"\draw[grad] (%s,%s) -- (%s,%s);" % (f(X(v)), f(y - h), f(X(v)), f(y + h)))
    for v in labels:
        s.append(r"\node[gradTexte] at (%s,%s) {$%s$};" % (f(X(v)), f(y - .2), nb(v)))
    return "\n".join(s), X


def point(x, y, coul=NAVY, r=2.6):
    return r"\fill[%s] (%s,%s) circle (%spt);" % (coul, f(x), f(y), f(r))


def nom_dessus(x, y, texte, coul=NAVY, h=.2):
    return r"\node[anchor=south,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (coul, f(x), f(y + h), texte)


def nom_dessous(x, y, texte, coul=NAVY, h=.62):
    """Étiquette sous la droite (sous les graduations écrites), reliée par un trait de rappel."""
    return (r"\draw[%s!60,line width=.4pt] (%s,%s) -- (%s,%s);" % (coul, f(x), f(y - .15), f(x), f(y - h + .03))
            + "\n" + r"\node[anchor=north,text=%s,inner sep=1.5pt] at (%s,%s) {%s};" % (coul, f(x), f(y - h), texte))


def loupe(X1, a, b, y_haut, y_bas, X2):
    """Pointillés reliant l'intervalle [a ; b] de la droite du haut à la droite agrandie."""
    return (r"\draw[loupe] (%s,%s) -- (%s,%s);" % (f(X1(a)), f(y_haut - .2), f(X2(a)), f(y_bas + .2)) + "\n"
            + r"\draw[loupe] (%s,%s) -- (%s,%s);" % (f(X1(b)), f(y_haut - .2), f(X2(b)), f(y_bas + .2)))


# ===================================================================== chiffre et « nombre de »
def nombre_espace(chiffres, x0=0.0, y0=0.0, dx=.3, gap=.3, couleurs=None, fond=None):
    """Écrit un grand nombre chiffre par chiffre (classes séparées).
    Renvoie (code, positions x des chiffres)."""
    n = len(chiffres)
    xs = []
    x = x0
    for k in range(n):
        reste = n - k
        xs.append(x)
        x += dx
        if reste > 1 and (reste - 1) % 3 == 0:
            x += gap
    s = []
    for k, ch in enumerate(chiffres):
        c = (couleurs or {}).get(k, "otInk")
        if fond and k in fond:
            s.append(r"\fill[%s,rounded corners=2pt] (%s,%s) rectangle (%s,%s);"
                     % (fond[k], f(xs[k] - .17), f(y0 - .27), f(xs[k] + .17), f(y0 + .29)))
        s.append(r"\node[text=%s,inner sep=1pt,font=\Large] at (%s,%s) {$%s$};" % (c, f(xs[k]), f(y0), ch))
    return "\n".join(s), xs


def chiffre_et_nombre(chiffres, idx_rang, nom_rang, coul_nb, coul_ch, nom_nb):
    """Accolade au-dessus des chiffres jusqu'au rang choisi (nombre de …) et
    chiffre de ce rang mis en valeur dessous (chiffre des …)."""
    code, xs = nombre_espace(chiffres, couleurs={idx_rang: coul_ch}, fond={idx_rang: "otGreen!22"})
    s = [r"\begin{tikzpicture}", code]
    xa, xb = xs[0] - .2, xs[idx_rang] + .2
    s.append(r"\draw[accol,%s] (%s,.42) -- (%s,.42);" % (coul_nb, f(xa), f(xb)))
    s.append(r"\node[anchor=south,text=%s,inner sep=1.5pt] at (%s,.62) {%s};" % (coul_nb, f((xa + xb) / 2), nom_nb))
    s.append(r"\draw[%s,line width=.7pt,-{Stealth[length=2mm]}] (%s,-1.0) -- (%s,-.36);" % (coul_ch, f(xs[idx_rang]), f(xs[idx_rang])))
    s.append(r"\node[anchor=north,text=%s,inner sep=1.5pt] at (%s,-1.04) {%s};" % (coul_ch, f(xs[idx_rang]), nom_rang))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


# ===================================================================== COURS
FIGURES["cours_classes"] = fig_tableau_entiers("4207350018", NAVY)

FIGURES["cours_chiffre_nombre"] = chiffre_et_nombre(
    "4207350018", 3, r"chiffre des millions : $7$", "otNavy", VERT, r"nombre de millions : $4\,207$")


def cours_unites():
    s = [r"\begin{tikzpicture}"]
    # bande : un dixième
    s.append(bande(0, 1.65, 1, L=3.3))
    s.append(r"\node[anchor=south west,text=otInk,inner sep=1pt] at (0,2.3) {l'unité partagée en $10$};")
    s.append(r"\node[anchor=north west,text=otNavy,inner sep=1pt] at (0,1.5) {une part : un dixième, $\frac{1}{10} = 0{,}1$};")
    # carré : une colonne = un dixième, une case = un centième
    c = .22
    yb = -1.9
    s.append(carre(0, yb, colonnes=1, cases=1, c=c, coul="otNavy!40", coul_cases="otOrange!80", cases_col=4))
    s.append(r"\node[anchor=south west,text=otInk,inner sep=1pt] at (0,%s) {l'unité partagée en $100$};" % f(yb + 10 * c + .08))
    s.append(r"\fill[otNavy!40] (0,%s) rectangle (.22,%s);" % (f(yb - .5), f(yb - .28)))
    s.append(r"\node[anchor=west,text=otNavy,inner sep=1pt] at (.34,%s) {une colonne : $\frac{1}{10} = \frac{10}{100}$};" % f(yb - .39))
    s.append(r"\fill[otOrange!80] (0,%s) rectangle (.22,%s);" % (f(yb - 1.15), f(yb - .93)))
    s.append(r"\node[anchor=west,text=otOrange!70!black,inner sep=1pt] at (.34,%s) {une case : un centième, $\frac{1}{100} = 0{,}01$};" % f(yb - 1.04))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_unites"] = cours_unites()

FIGURES["cours_tableau_decimal"] = fig_tableau_decimal(["", "6", "3", "5", "0", "7"], NAVY,
                                                       (r"$63{,}507 = 63 + 0{,}507$\\[2pt]partie entière : $63$ ; partie décimale : $0{,}507$", "otInk"))


def cours_droite():
    U1 = 6.2
    c1, X1 = droite(2, 3, U1, y=1.9, pas=.1, labels=(2, 3))
    U2 = 62
    c2, X2 = droite(2.4, 2.5, U2, y=0, pas=.01, labels=(2.4, 2.5), x0=0)
    s = [r"\begin{tikzpicture}", c1, c2, loupe(X1, 2.4, 2.5, 1.9, 0, X2)]
    s.append(point(X1(2.4), 1.9, ORANGE))
    s.append(nom_dessus(X1(2.4), 1.9, r"$2{,}4 = \frac{24}{10}$", "otInk"))
    s.append(r"\node[anchor=south west,petit,text=otMuted,inner sep=1pt] at (%s,2.55) {graduée au dixième};" % f(X1(2.6)))
    s.append(point(X2(2.47), 0, ORANGE))
    s.append(nom_dessous(X2(2.47), 0, r"$2{,}47 = \frac{247}{100} = 2 + \frac{47}{100}$", "otInk", h=.62))
    s.append(r"\node[anchor=north,petit,text=otMuted,inner sep=1pt] at (%s,-1.55) {loupe entre $2{,}4$ et $2{,}5$ : graduée au centième};" % f(X2(2.45)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_droite"] = cours_droite()


# ===================================================================== 3167 : tableau des entiers
FIGURES["ex3167_tableau_enonce"] = fig_tableau_entiers("")
FIGURES["ex3167_tableau_corrige"] = fig_tableau_entiers("6052708300", VERT)


# ===================================================================== 3170 : bandes et carrés
def figures_3170(corrige):
    c = .2
    s = [r"\begin{tikzpicture}"]
    # ligne du haut : A (bande) et B (carré)
    s.append(r"\node[anchor=south west,entete,text=otInk] at (0,2.12) {Figure A};")
    s.append(bande(0, .9, 7, L=3.0, h=.5))
    s.append(r"\node[anchor=south west,entete,text=otInk] at (4.0,2.12) {Figure B};")
    s.append(carre(4.0, .0, colonnes=3, cases=6, c=c))
    # ligne du bas : C (deux carrés) et D (carré)
    yb = -3.1
    s.append(r"\node[anchor=south west,entete,text=otInk] at (0,%s) {Figure C};" % f(yb + 10 * c + .12))
    s.append(carre(0, yb, colonnes=10, c=c))
    s.append(carre(2.25, yb, colonnes=4, cases=5, c=c))
    s.append(r"\node[anchor=south west,entete,text=otInk] at (5.0,%s) {Figure D};" % f(yb + 10 * c + .12))
    s.append(carre(5.0, yb, colonnes=0, cases=4, c=c))
    if corrige:
        s.append(r"\node[anchor=north west,text=%s,inner sep=1pt] at (0,.75) {$\frac{7}{10} = 0{,}7$};" % VERT)
        s.append(r"\node[anchor=north west,text=%s,inner sep=1pt] at (4.0,-.12) {$\frac{36}{100} = 0{,}36$};" % VERT)
        s.append(r"\node[anchor=north west,text=%s,inner sep=1pt] at (0,%s) {$1 + \frac{45}{100} = \frac{145}{100} = 1{,}45$};" % (VERT, f(yb - .12)))
        s.append(r"\node[anchor=north west,text=%s,inner sep=1pt] at (5.0,%s) {$\frac{4}{100} = 0{,}04$};" % (VERT, f(yb - .12)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3170_figures_enonce"] = figures_3170(False)
FIGURES["ex3170_figures_corrige"] = figures_3170(True)


# ===================================================================== 3168 : tableau décimal
FIGURES["ex3168_tableau_enonce"] = fig_tableau_decimal(None)
FIGURES["ex3168_tableau_corrige"] = fig_tableau_decimal(["3", "0", "6", "0", "4", "8"], VERT)


# ===================================================================== 3171 : chiffre ou nombre de
FIGURES["ex3171_nombre_corrige"] = chiffre_et_nombre(
    "7485213906", 3, r"chiffre des millions : $5$", VERT, VERT, r"nombre de millions : $7\,485$")


# ===================================================================== 3177 : règle graduée et loupe
LUS_3177 = [(.7, "A"), (2.3, "B"), (3.8, "C")]
PLACES_3177 = [(4.6, "D"), (1.5, "E")]


def regle_3177(corrige):
    U1 = 1.25
    yh = 2.1
    c1, X1 = droite(0, 5, U1, y=yh, pas=.1, labels=range(0, 6))
    U2 = 60
    c2, X2 = droite(3.2, 3.3, U2, y=0, pas=.01, labels=(3.2, 3.3), x0=.3)
    s = [r"\begin{tikzpicture}", c1, c2, loupe(X1, 3.2, 3.3, yh, 0, X2)]
    s.append(r"\node[anchor=south west,petit,text=otMuted,inner sep=1pt] at (%s,%s) {cm};" % (f(X1(5) + .5), f(yh + .05)))
    for v, nm in LUS_3177:
        s.append(point(X1(v), yh, NAVY))
        s.append(nom_dessus(X1(v), yh, r"$%s$" % nm, NAVY))
    s.append(point(X2(3.26), 0, NAVY))
    s.append(nom_dessus(X2(3.26), 0, r"$F$", NAVY))
    if corrige:
        for v, nm in LUS_3177:
            s.append(r"\node[anchor=south,text=%s,inner sep=1pt] at (%s,%s) {$%s$};" % (VERT, f(X1(v)), f(yh + .62), nb(v)))
        for v, nm in PLACES_3177:
            s.append(point(X1(v), yh, VERT))
            s.append(nom_dessus(X1(v), yh, r"$%s$" % nm, VERT))
        s.append(r"\node[anchor=south,text=%s,inner sep=1pt] at (%s,.6) {$3{,}26$};" % (VERT, f(X2(3.26))))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex3177_regle_enonce"] = regle_3177(False)
FIGURES["ex3177_regle_corrige"] = regle_3177(True)


# ===================================================================== 3181 : synthèse
FIGURES["ex3181_entiers_corrige"] = fig_tableau_entiers("2009040000", VERT)
FIGURES["ex3181_decimal_corrige"] = fig_tableau_decimal(["", "", "3", "4", "0", "8"], VERT)
