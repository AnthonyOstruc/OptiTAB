# -*- coding: utf-8 -*-
"""Figures de la notion 278 (5e : organiser et interpréter des données), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Bleu marine = données ; orange = seconde série ; vert foncé = éléments de réponse
(corrigés). L'énoncé montre seulement les données ; le corrigé montre la
construction ou la lecture en vert.
Les données (DONNEES) sont relues par verif_278.py : figures, énoncés et
corrigés utilisent exactement les mêmes valeurs.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=1pt,text=otInk},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,inner sep=1pt,text=otMuted},
  cellule/.style={font=\otRegular\fontsize{9}{11}\selectfont,text=otNavy},
  barre/.style={fill=otNavy!55,draw=otNavy,line width=.6pt},
  barreV/.style={fill=otGreen!60,draw=otGreenDark,line width=.6pt},
  barreO/.style={fill=otOrange!70,draw=otOrange!80!black,line width=.6pt},
  grille/.style={otRule,line width=.35pt},
  axeS/.style={otMuted,line width=.7pt},
  lecture/.style={otGreenDark,line width=.8pt,dash pattern=on 2.5pt off 1.8pt},
  moy/.style={otGreenDark,line width=1pt,dash pattern=on 4pt off 2.5pt},
  baton/.style={line width=1.1pt,line cap=round},
}
"""

# --------------------------------------------------------------------------- données
DONNEES = {
    # cours
    "cours_boissons": [("Jus de fruits", 8), ("Eau", 5), ("Chocolat chaud", 4), ("Lait", 3)],
    "cours_buts": ([0, 1, 2, 3, 4], [4, 7, 5, 3, 1]),
    "cours_judo": ([2020, 2021, 2022, 2023, 2024, 2025], [40, 30, 35, 50, 60, 65]),
    # exercices
    "3062": [("Fraise", 9), ("Pomme", 6), ("Banane", 5), ("Orange", 4)],
    "3062_brut": ["F P B F O F", "P F B O F P", "B F P F O B", "F P O B F P"],
    "3071": [("Sport", 14), ("Musique", 6), ("Lecture", 8), ("Écrans", 12)],
    "3066": (["Lun", "Mar", "Mer", "Jeu", "Ven"], [12, 18, 15, 9, 6]),
    "3063": ([0, 1, 2, 3, 4], [7, 10, 5, 2, 1]),
    "3073": [("À pied", 10), ("Vélo", 18), ("Bus", 12)],
    "3072": ([12, 9, 15, 10, 14], [12, 11, 13, 12, 12]),
    "3075": (["janv.", "févr.", "mars", "avr.", "mai", "juin"], [800, 1000, 1000, 1400, 2000, 2800]),
    "3065": (["Lun", "Mar", "Mer", "Jeu", "Ven"], [18, 24, 12, 30, 36]),
    "3064": [("Parc", 12), ("Zoo", 9), ("Musée", 6), ("Cinéma", 3)],
    "3064_brut": ["P Z P M P C", "Z P M Z P Z", "P M P Z C P", "Z P M Z P M", "P Z C M Z P"],
    "3064_B": [("Parc", 11), ("Zoo", 6), ("Musée", 5), ("Cinéma", 3)],
    "3082": (["Lundi", "Mardi", "Jeudi", "Vendredi"], [280, 300, 290, 330]),
}

FIGURES = {}


def figure(corps, opt="line cap=round"):
    return "\n".join([r"\begin{tikzpicture}[%s]" % opt] + corps + [r"\end{tikzpicture}"])


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def num(x):
    """Nombre au format français dans une formule : 1\\,500 ; 27{,}5."""
    if isinstance(x, float) and x == int(x):
        x = int(x)
    s = ("%s" % x)
    if "." in s:
        e, d = s.split(".")
        return e + "{,}" + d
    if len(s) > 3:
        return s[:-3] + r"\," + s[-3:]
    return s


# ======================================================== DIAGRAMME EN BARRES / BÂTONS
def axe_vertical(s, ymax, pas, unite, W, y0=0, lab_pas=None):
    lab_pas = lab_pas or pas
    k = y0
    while k <= ymax + 1e-9:
        y = (k - y0) * unite
        if k > y0:
            s.append(r"\draw[grille] (0,%s) -- (%s,%s);" % (f(y), f(W), f(y)))
        if abs((k - y0) / lab_pas - round((k - y0) / lab_pas)) < 1e-6:
            s.append(r"\draw[axeS] (-.08,%s) -- (0,%s);" % (f(y), f(y)))
            s.append(r"\node[petit,anchor=east] at (-.12,%s) {%s};" % (f(y), num(k)))
        k += pas


def barres(etiq, hauteurs, ymax, pas, unite=.3, dx=1.1, larg=.3, titre_x="", titre_y="",
           valeurs=False, style="barre", lab_pas=None, couleur_val="otGreenDark", y0=0, batons=False):
    """Diagramme vertical : etiq sous l'axe, hauteurs = effectifs.
    batons=True : bâtons (traits épais) au lieu de barres. y0 : début de l'axe vertical."""
    s = []
    n = len(etiq)
    W = (n + .2) * dx
    H = (ymax - y0) * unite
    axe_vertical(s, ymax, pas, unite, W, y0=y0, lab_pas=lab_pas)
    for i, (e, h) in enumerate(zip(etiq, hauteurs)):
        x = (i + .7) * dx
        hy = (h - y0) * unite
        if batons:
            col = "otGreenDark" if style == "barreV" else "otNavy"
            s.append(r"\draw[baton,%s,line width=2.6pt,line cap=butt] (%s,0) -- (%s,%s);" % (col, f(x), f(x), f(hy)))
        else:
            s.append(r"\draw[%s] (%s,0) rectangle (%s,%s);" % (style, f(x - larg), f(x + larg), f(hy)))
        s.append(r"\node[txt,anchor=north] at (%s,-.12) {%s};" % (f(x), e))
        if valeurs:
            s.append(r"\node[txt,anchor=south,text=%s] at (%s,%s) {%s};" % (couleur_val, f(x), f(hy + .06), num(h)))
    s.append(r"\draw[axeS] (0,0) -- (%s,0);" % f(W))
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (0,%s);" % f(H + .35))
    if titre_y:
        s.append(r"\node[petit,anchor=south west] at (.1,%s) {%s};" % (f(H + .3), titre_y))
    if titre_x:
        s.append(r"\node[petit,anchor=north] at (%s,-.6) {%s};" % (f(W / 2), titre_x))
    return s


# ======================================================== DIAGRAMMES CIRCULAIRE ET SEMI-CIRCULAIRE
COULEURS = ["otNavy!55", "otGreen!60", "otOrange!70", "otMuted!40", "otRed!45"]


def _ancre(m):
    m = m % 360
    if 80 <= m < 100:
        return "south"
    if 260 <= m < 280:
        return "north"
    if m < 10 or m >= 350:
        return "west"
    if 170 <= m < 190:
        return "east"
    if m < 90:
        return "south west"
    if m < 180:
        return "south east"
    if m < 270:
        return "north east"
    return "north west"


def secteurs(parts, r=1.6, vert=False, depart=90, demi=False):
    """parts : liste (étiquette, angle en degrés, texte sous l'étiquette).
    Les secteurs tournent dans le sens des aiguilles d'une montre à partir de « depart »."""
    s = []
    a = depart
    for i, (lab, ang, txt) in enumerate(parts):
        b = a - ang
        s.append(r"\fill[%s] (0,0) -- (%s:%s) arc[start angle=%s,end angle=%s,radius=%s] -- cycle;"
                 % (COULEURS[i], f(a), f(r), f(a), f(b), f(r)))
        a = b
    a = depart
    for i, (lab, ang, txt) in enumerate(parts):
        if not (demi and i == 0):
            s.append(r"\draw[white,line width=1.2pt] (0,0) -- (%s:%s);" % (f(a), f(r)))
        a -= ang
    if demi:
        s.append(r"\draw[otNavy,line width=.8pt] (%s,0) arc[start angle=0,end angle=180,radius=%s] -- cycle;"
                 % (f(r), f(r)))
    else:
        s.append(r"\draw[otNavy,line width=.8pt] (0,0) circle (%s);" % f(r))
    a = depart
    for i, (lab, ang, txt) in enumerate(parts):
        m = a - ang / 2
        c = "otGreenDark" if vert else "otInk"
        lab2 = lab + (r"\\\textcolor{%s}{%s}" % (c, txt) if txt else "")
        s.append(r"\node[txt,align=center,anchor=%s] at (%s:%s) {%s};" % (_ancre(m), f(m), f(r + .15), lab2))
        a -= ang
    return s


# ======================================================== TABLEAU DE DÉPOUILLEMENT (bâtonnets)
def batonnets(x0, yc, n, coul):
    """n bâtonnets groupés par 5 (4 traits + 1 barre en travers), centrés en hauteur sur yc."""
    s = []
    x = x0
    h = .34
    while n > 0:
        k = min(n, 5)
        nv = min(k, 4)
        for j in range(nv):
            xx = x + j * .13
            s.append(r"\draw[%s,line width=1pt] (%s,%s) -- (%s,%s);" % (coul, f(xx), f(yc - h / 2), f(xx), f(yc + h / 2)))
        if k == 5:
            s.append(r"\draw[%s,line width=1pt] (%s,%s) -- (%s,%s);"
                     % (coul, f(x - .08), f(yc - h / 2 + .04), f(x + 3 * .13 + .08), f(yc + h / 2 - .04)))
        x += 4 * .13 + .22
        n -= k
    return s


def depouillement(lignes, entetes, largeurs, vert=False, total=None, h=.56):
    """lignes : (catégorie, effectif). Colonnes : catégorie | comptage | effectif."""
    s = []
    xs = [0.0]
    for w in largeurs:
        xs.append(xs[-1] + w)
    R = len(lignes) + 1 + (1 if total is not None else 0)
    s.append(r"\fill[otSky] (0,0) rectangle (%s,%s);" % (f(xs[-1]), f(-h)))
    for k, e in enumerate(entetes):
        s.append(r"\node[cellule] at (%s,%s) {%s};" % (f((xs[k] + xs[k + 1]) / 2), f(-h / 2), e))
    coul = "otGreenDark" if vert else "otNavy"
    for r, (cat, n) in enumerate(lignes):
        y = -(r + 1) * h - h / 2
        s.append(r"\node[txt,anchor=west] at (%s,%s) {%s};" % (f(xs[0] + .15), f(y), cat))
        s += batonnets(xs[1] + .25, y, n, coul)
        s.append(r"\node[txt,text=%s] at (%s,%s) {%d};" % (coul, f((xs[2] + xs[3]) / 2), f(y), n))
    if total is not None:
        y = -(len(lignes) + 1) * h - h / 2
        s.append(r"\node[txt,anchor=west] at (%s,%s) {Total};" % (f(xs[0] + .15), f(y)))
        s.append(r"\node[txt,text=%s] at (%s,%s) {%d};" % (coul, f((xs[2] + xs[3]) / 2), f(y), total))
    for r in range(R + 1):
        lw = ".8pt" if r in (0, 1, R) else ".45pt"
        s.append(r"\draw[otMuted!70,line width=%s] (0,%s) -- (%s,%s);" % (lw, f(-r * h), f(xs[-1]), f(-r * h)))
    for x in xs:
        s.append(r"\draw[otMuted!70,line width=.45pt] (%s,0) -- (%s,%s);" % (f(x), f(x), f(-R * h)))
    return s


# ======================================================== FEUILLE DE TABLEUR (dessin des notions 268 et 272)
def tableur(colonnes, lignes, largeurs, active=None, barre=None, vert=None, h=.52):
    """lignes : la 1re = ligne 1 du tableur ; active = (ligne, colonne) ; barre = (nom, formule) ;
    vert = ensemble de (ligne, colonne) écrits en vert (colonne 0 = A)."""
    L = []
    wn = .55
    xs = [0.0, wn]
    for w in largeurs:
        xs.append(xs[-1] + w)
    R = len(lignes) + 1
    top = 0.0
    if barre:
        nomc, formule = barre
        yb = .2 + h
        L.append(r"\filldraw[fill=white,draw=otMuted!70,line width=.5pt] (0,%s) rectangle (%s,%s);" % (f(.2), f(xs[-1]), f(yb)))
        L.append(r"\draw[otMuted!70,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(1.05), f(.2), f(1.05), f(yb)))
        L.append(r"\node[cellule] at (%s,%s) {%s};" % (f(.525), f(.2 + h / 2), nomc))
        L.append(r"\node[petit,text=otMuted,font=\itshape] at (%s,%s) {fx};" % (f(1.35), f(.2 + h / 2)))
        if formule:
            coul = "otGreenDark" if vert and "barre" in vert else "otInk"
            L.append(r"\node[anchor=west,font=\otRegular\fontsize{9.5}{11}\selectfont,text=%s] at (%s,%s) {%s};"
                     % (coul, f(1.62), f(.2 + h / 2), formule))
    L.append(r"\fill[otSky] (0,%s) rectangle (%s,%s);" % (f(top), f(xs[-1]), f(top - h)))
    L.append(r"\fill[otSky] (0,%s) rectangle (%s,%s);" % (f(top), f(xs[1]), f(top - R * h)))
    for k, c in enumerate(colonnes):
        L.append(r"\node[cellule] at (%s,%s) {%s};" % (f((xs[k + 1] + xs[k + 2]) / 2), f(top - h / 2), c))
    for r, ligne in enumerate(lignes):
        y = top - (r + 1) * h - h / 2
        L.append(r"\node[cellule] at (%s,%s) {%d};" % (f(wn / 2), f(y), r + 1))
        for k, v in enumerate(ligne):
            if not v:
                continue
            coul = "otGreenDark" if vert and (r + 1, k) in vert else "otInk"
            L.append(r"\node[text=%s] at (%s,%s) {%s};" % (coul, f((xs[k + 1] + xs[k + 2]) / 2), f(y), v))
    for r in range(R + 1):
        L.append(r"\draw[otMuted!70,line width=.5pt] (0,%s) -- (%s,%s);" % (f(top - r * h), f(xs[-1]), f(top - r * h)))
    for x in xs:
        L.append(r"\draw[otMuted!70,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(x), f(top), f(x), f(top - R * h)))
    if active:
        r, k = active
        L.append(r"\draw[otNavy,line width=1.4pt] (%s,%s) rectangle (%s,%s);"
                 % (f(xs[k + 1]), f(top - r * h), f(xs[k + 2]), f(top - (r + 1) * h)))
    return L


# ======================================================== GRAPHIQUE CARTÉSIEN (évolution)
def cartesien(xlabs, ys, ymax, ypas, ylab_pas, ux, uy, titre_x, titre_y, lectures=(), moyenne=None,
              moy_txt=""):
    s = []
    n = len(xlabs)
    W = (n - .4) * ux
    H = ymax * uy
    k = 0
    while k <= ymax + 1e-9:
        y = k * uy
        if k > 0:
            s.append(r"\draw[grille] (0,%s) -- (%s,%s);" % (f(y), f(W), f(y)))
        if abs(k / ylab_pas - round(k / ylab_pas)) < 1e-6:
            s.append(r"\draw[axeS] (-.08,%s) -- (0,%s);" % (f(y), f(y)))
            s.append(r"\node[petit,anchor=east] at (-.12,%s) {%s};" % (f(y), num(k)))
        k += ypas
    X = lambda i: (i + .4) * ux
    for i, lab in enumerate(xlabs):
        s.append(r"\draw[grille] (%s,0) -- (%s,%s);" % (f(X(i)), f(X(i)), f(H)))
        s.append(r"\draw[axeS] (%s,0) -- (%s,-.08);" % (f(X(i)), f(X(i))))
        s.append(r"\node[petit,anchor=north] at (%s,-.12) {%s};" % (f(X(i)), lab))
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (%s,0);" % f(W + .35))
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (0,%s);" % f(H + .35))
    s.append(r"\node[petit,anchor=south west] at (.1,%s) {%s};" % (f(H + .3), titre_y))
    s.append(r"\node[petit,anchor=north] at (%s,-.55) {%s};" % (f(W / 2), titre_x))
    if moyenne is not None:
        ym = moyenne * uy
        s.append(r"\draw[moy] (0,%s) -- (%s,%s);" % (f(ym), f(W), f(ym)))
        s.append(r"\node[txt,text=otGreenDark,anchor=west,align=left] at (%s,%s) {%s};" % (f(W + .1), f(ym), moy_txt))
    pts = " -- ".join("(%s,%s)" % (f(X(i)), f(y * uy)) for i, y in enumerate(ys))
    s.append(r"\draw[otNavy,line width=1.2pt,line join=round] %s;" % pts)
    for i, y in enumerate(ys):
        s.append(r"\fill[otNavy] (%s,%s) circle (2.3pt);" % (f(X(i)), f(y * uy)))
    for (i, txt, ancre, tx, ty) in lectures:
        px, py = X(i), ys[i] * uy
        s.append(r"\draw[lecture] (%s,0) -- (%s,%s) -- (0,%s);" % (f(px), f(px), f(py), f(py)))
        s.append(r"\fill[otGreenDark] (%s,%s) circle (2.5pt);" % (f(px), f(py)))
        s.append(r"\node[txt,text=otGreenDark,anchor=%s] at (%s,%s) {%s};" % (ancre, f(tx), f(ty), txt))
    return s


# =============================================================================== COURS
BO = DONNEES["cours_boissons"]
FIGURES["cours_depouillement"] = figure(depouillement(BO, ["Boisson", "Comptage", "Effectif"], [2.8, 2.2, 1.6],
                                                      total=sum(e for _, e in BO)))
FIGURES["cours_barres"] = figure(barres(["Jus", "Eau", "Chocolat", "Lait"], [e for _, e in BO], 9, 1, unite=.36,
                                        dx=1.5, larg=.36, titre_x="boisson préférée", titre_y="effectif",
                                        valeurs=True, couleur_val="otInk", lab_pas=2))
BU = DONNEES["cours_buts"]
FIGURES["cours_batons"] = figure(barres([str(v) for v in BU[0]], BU[1], 8, 1, unite=.36, dx=1.2,
                                        titre_x="nombre de buts marqués", titre_y="nombre de matchs",
                                        valeurs=True, couleur_val="otInk", lab_pas=2, batons=True))
_tot = sum(e for _, e in BO)
COURT = {"Jus de fruits": "Jus de fruits", "Eau": "Eau", "Chocolat chaud": "Chocolat", "Lait": "Lait"}
FIGURES["cours_circulaire"] = figure(secteurs([(COURT[n], e * 360 / _tot, r"%d°" % (e * 360 // _tot)) for n, e in BO],
                                              r=1.45))
FIGURES["cours_semi"] = figure(secteurs([(COURT[n], e * 180 / _tot, r"%d°" % (e * 180 // _tot)) for n, e in BO],
                                        r=2.0, depart=180, demi=True))
JX, JY = DONNEES["cours_judo"]
FIGURES["cours_cartesien"] = figure(cartesien([str(a) for a in JX], JY, 70, 5, 10, 1.0, .05, "année",
                                              "nombre de licenciés"))
_tb = [["Boisson", "Effectif", "Fréquence"],
       ["Jus de fruits", "8", "0,4"], ["Eau", "5", "0,25"], ["Chocolat chaud", "4", "0,2"], ["Lait", "3", "0,15"],
       ["Total", "20", "1"]]
FIGURES["cours_tableur"] = figure(tableur(["A", "B", "C"], _tb, [2.7, 1.7, 1.9], active=(2, 2),
                                          barre=("C2", "=B2/B6")))

# =============================================================================== EXERCICES
# --- 3062 : dépouillement des fruits (corrigé)
FR = DONNEES["3062"]
FIGURES["ex3062_corrige"] = figure(depouillement(FR, ["Fruit", "Comptage", "Effectif"], [2.1, 2.2, 1.6], vert=True,
                                                 total=sum(e for _, e in FR)))


# --- 3071 : barre des pourcentages (corrigé)
def barre_pourcent(parts, L=6.6, h=.7, hauts=(1,)):
    """Barre de 100 % partagée ; les étiquettes d'indice dans « hauts » sont placées un rang plus haut,
    reliées à leur segment par un petit trait (segments étroits)."""
    s = []
    x = 0.0
    for i, (lab, p) in enumerate(parts):
        w = L * p / 100
        s.append(r"\fill[%s] (%s,0) rectangle (%s,%s);" % (COULEURS[i], f(x), f(x + w), f(h)))
        if i in hauts:
            s.append(r"\draw[otMuted,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(x + w / 2), f(h + .05), f(x + w / 2), f(h + .45)))
            s.append(r"\node[txt,anchor=south] at (%s,%s) {%s};" % (f(x + w / 2), f(h + .48), lab))
        else:
            s.append(r"\node[txt,anchor=south] at (%s,%s) {%s};" % (f(x + w / 2), f(h + .1), lab))
        s.append(r"\node[txt,text=otGreenDark,anchor=north] at (%s,-.1) {%d\,\%%};" % (f(x + w / 2), p))
        x += w
        if i < len(parts) - 1:
            s.append(r"\draw[white,line width=1.2pt] (%s,0) -- (%s,%s);" % (f(x), f(x), f(h)))
    s.append(r"\draw[otNavy,line width=.8pt] (0,0) rectangle (%s,%s);" % (f(L), f(h)))
    s.append(r"\draw[otGreenDark,line width=.7pt,{Stealth[length=1.8mm]}-{Stealth[length=1.8mm]}] (0,-.75) -- (%s,-.75);"
             % f(L))
    s.append(r"\node[txt,text=otGreenDark,anchor=north] at (%s,-.9) {total : 40 élèves = 100\,\%%};" % f(L / 2))
    return s


AC = DONNEES["3071"]
_ta = sum(e for _, e in AC)
FIGURES["ex3071_corrige"] = figure(barre_pourcent([(n, e * 100 // _ta) for n, e in AC]))

# --- 3066 : bibliothèque (barres)
BJ, BE = DONNEES["3066"]
FIGURES["ex3066_enonce"] = figure(barres(BJ, BE, 21, 3, unite=.17, dx=1.3, larg=.34, titre_y="nombre de livres empruntés",
                                         titre_x="jour de la semaine"))
FIGURES["ex3066_corrige"] = figure(barres(BJ, BE, 21, 3, unite=.17, dx=1.3, larg=.34, titre_y="nombre de livres empruntés",
                                          titre_x="jour de la semaine", valeurs=True, style="barreV"))

# --- 3063 : animaux (bâtons, corrigé)
AV, AE = DONNEES["3063"]
FIGURES["ex3063_corrige"] = figure(barres([str(v) for v in AV], AE, 11, 1, unite=.3, dx=1.2,
                                          titre_x="nombre d'animaux de compagnie", titre_y="nombre d'élèves",
                                          valeurs=True, lab_pas=2, batons=True, style="barreV"))

# --- 3073 : transports (circulaire et semi-circulaire, corrigé)
TR = DONNEES["3073"]
_tt = sum(e for _, e in TR)
FIGURES["ex3073_circulaire"] = figure(secteurs([(n, e * 360 / _tt, r"%d°" % (e * 360 // _tt)) for n, e in TR], vert=True))
FIGURES["ex3073_semi"] = figure(secteurs([(n, e * 180 / _tt, r"%d°" % (e * 180 // _tt)) for n, e in TR],
                                         r=2.0, depart=180, demi=True, vert=True))


# --- 3072 : notes de Yanis et d'Inès, moyenne en vert (corrigé)
def panneau(notes, nom, y0, moyenne, unite=.11, dx=.78, larg=.24):
    s = []
    W = (len(notes) + .2) * dx
    H = 20 * unite
    k = 0
    while k <= 20:
        y = y0 + k * unite
        if k > 0:
            s.append(r"\draw[grille] (0,%s) -- (%s,%s);" % (f(y), f(W), f(y)))
        if k % 5 == 0:
            s.append(r"\draw[axeS] (-.08,%s) -- (0,%s);" % (f(y), f(y)))
            s.append(r"\node[petit,anchor=east] at (-.12,%s) {%d};" % (f(y), k))
        k += 1
    for i, v in enumerate(notes):
        x = (i + .7) * dx
        s.append(r"\draw[barre] (%s,%s) rectangle (%s,%s);" % (f(x - larg), f(y0), f(x + larg), f(y0 + v * unite)))
        s.append(r"\node[petit,anchor=north] at (%s,%s) {C%d};" % (f(x), f(y0 - .1), i + 1))
    s.append(r"\draw[axeS] (0,%s) -- (%s,%s);" % (f(y0), f(W), f(y0)))
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,%s) -- (0,%s);" % (f(y0), f(y0 + H + .3)))
    s.append(r"\node[txt,text=otNavy,anchor=south west] at (.1,%s) {%s};" % (f(y0 + H + .25), nom))
    ym = y0 + moyenne * unite
    s.append(r"\draw[moy] (0,%s) -- (%s,%s);" % (f(ym), f(W + .1), f(ym)))
    s.append(r"\node[txt,text=otGreenDark,anchor=west] at (%s,%s) {moyenne : %s};" % (f(W + .15), f(ym), num(moyenne)))
    return s


NY, NI = DONNEES["3072"]
FIGURES["ex3072_corrige"] = figure(panneau(NY, "Notes de Yanis", 0, sum(NY) / len(NY))
                                   + panneau(NI, "Notes d'Inès", -3.4, sum(NI) / len(NI)))

# --- 3075 : piscine (graphique cartésien)
PM, PE = DONNEES["3075"]
_ux, _uy = .82, .0019
_W75 = (len(PM) - .4) * _ux
FIGURES["ex3075_enonce"] = figure(cartesien(PM, PE, 3000, 200, 400, _ux, _uy, "mois", "nombre d'entrées"))
FIGURES["ex3075_corrige"] = figure(cartesien(PM, PE, 3000, 200, 400, _ux, _uy, "mois", "nombre d'entrées",
                                             lectures=[(2, r"1\,000", "south east", 2.4 * _ux - .1, 1000 * _uy + .03),
                                                       (5, r"2\,800", "west", _W75 + .1, 2800 * _uy)],
                                             moyenne=sum(PE) / len(PE), moy_txt=r"moyenne :\\1\,500"))

# --- 3065 : tableur des ventes de gâteaux
GJ, GV = DONNEES["3065"]
_gt = sum(GV)
JOURS = {"Lun": "Lundi", "Mar": "Mardi", "Mer": "Mercredi", "Jeu": "Jeudi", "Ven": "Vendredi"}
_cols = ["A", "B", "C"]
_larg = [2.3, 1.7, 2.0]
_e = [["Jour", "Ventes", "Fréquence"]] + [[JOURS[j], str(v), ""] for j, v in zip(GJ, GV)] + [["Total", "", ""]]
FIGURES["ex3065_tableur"] = figure(tableur(_cols, _e, _larg, active=(7, 1), barre=("B7", "")))
_c = [["Jour", "Ventes", "Fréquence"]] + [[JOURS[j], str(v), r"%d\,\%%" % (v * 100 // _gt)] for j, v in zip(GJ, GV)] \
    + [["Total", str(_gt), "100\\,\\%"]]
FIGURES["ex3065_tableur_corrige"] = figure(tableur(_cols, _c, _larg, active=(2, 2), barre=("C2", "=B2/B7"),
                                                   vert={(7, 1)} | {(r, 2) for r in range(2, 8)} | {"barre"}))
_g1 = barres(GJ, GV, 40, 5, unite=.075, dx=.76, larg=.24, titre_y="ventes", lab_pas=10)
_g2 = ["\\begin{scope}[xshift=5.95cm,yshift=1.45cm]"] + secteurs([(j, v * 360 / _gt, "") for j, v in zip(GJ, GV)], r=.95) \
    + ["\\end{scope}"]
_g1 += [r"\node[txt,text=otNavy] at (1.95,-.75) {Graphique 1};", r"\node[txt,text=otNavy] at (5.95,-.75) {Graphique 2};"]
FIGURES["ex3065_graphiques"] = figure(_g1 + _g2)

# --- 3064 : sondage (circulaire, comparaison des deux classes)
SA = DONNEES["3064"]
_sa = sum(e for _, e in SA)
FIGURES["ex3064_circulaire"] = figure(secteurs([(n, e * 360 / _sa, r"%d°" % (e * 360 // _sa)) for n, e in SA], vert=True))
SB = DONNEES["3064_B"]
_sb = sum(e for _, e in SB)


def barres_doubles(etiq, h1, h2, ymax, pas, noms, unite=.07, dx=1.62, larg=.31, lab_pas=10, titre_y=""):
    s = []
    n = len(etiq)
    W = (n + .2) * dx
    H = ymax * unite
    axe_vertical(s, ymax, pas, unite, W, lab_pas=lab_pas)
    for i, e in enumerate(etiq):
        x = (i + .7) * dx
        for j, (h, st) in enumerate(((h1[i], "barre"), (h2[i], "barreO"))):
            xa = x - 2 * larg - .05 if j == 0 else x + .05
            s.append(r"\draw[%s] (%s,0) rectangle (%s,%s);" % (st, f(xa), f(xa + 2 * larg), f(h * unite)))
            s.append(r"\node[text=otGreenDark,font=\otMedium\fontsize{8}{9}\selectfont,inner sep=1pt,anchor=south]"
                     r" at (%s,%s) {%d\,\%%};" % (f(xa + larg), f(h * unite + .05), h))
        s.append(r"\node[txt,anchor=north] at (%s,-.12) {%s};" % (f(x), e))
    s.append(r"\draw[axeS] (0,0) -- (%s,0);" % f(W))
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (0,%s);" % f(H + .35))
    s.append(r"\node[petit,anchor=south west] at (.1,%s) {%s};" % (f(H + .3), titre_y))
    yl = H + .75
    xl = W - 3.9
    s.append(r"\draw[barre] (%s,%s) rectangle ++(.3,.22);" % (f(xl), f(yl)))
    s.append(r"\node[txt,anchor=west] at (%s,%s) {%s};" % (f(xl + .38), f(yl + .11), noms[0]))
    s.append(r"\draw[barreO] (%s,%s) rectangle ++(.3,.22);" % (f(xl + 2.0), f(yl)))
    s.append(r"\node[txt,anchor=west] at (%s,%s) {%s};" % (f(xl + 2.38), f(yl + .11), noms[1]))
    return s


FIGURES["ex3064_comparaison"] = figure(barres_doubles([n for n, _ in SA], [e * 100 // _sa for _, e in SA],
                                                      [e * 100 // _sb for _, e in SB], 50, 5, ("5e A", "5e B"),
                                                      titre_y=r"fréquence (\%)"))

# --- 3082 : diagramme trompeur de la cantine
CJ, CR = DONNEES["3082"]
FIGURES["ex3082_enonce"] = figure(barres(CJ, CR, 340, 10, unite=.05, dx=1.5, larg=.36, y0=270,
                                         titre_y="nombre de repas servis", style="barreO"))
FIGURES["ex3082_corrige"] = figure(barres(CJ, CR, 350, 50, unite=.0095, dx=1.5, larg=.36,
                                          titre_y="nombre de repas servis", valeurs=True, style="barreV", lab_pas=50))
