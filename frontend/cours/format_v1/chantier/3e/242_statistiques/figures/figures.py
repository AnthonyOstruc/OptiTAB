# -*- coding: utf-8 -*-
"""Figures de la notion « Statistiques » (3e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = éléments
de réponse (corrigés), orange = éléments d'alerte.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=1pt,text=otInk},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,inner sep=1pt,text=otMuted},
  barre/.style={fill=otNavy!55,draw=otNavy,line width=.6pt},
  barreV/.style={fill=otGreen!60,draw=otGreenDark,line width=.6pt},
  barreO/.style={fill=otOrange!70,draw=otOrange!80!black,line width=.6pt},
  grille/.style={otRule,line width=.35pt},
  axeS/.style={otMuted,line width=.7pt},
}
"""


def figure(corps, opt="line cap=round"):
    return "\n".join([r"\begin{tikzpicture}[%s]" % opt] + corps + [r"\end{tikzpicture}"])


# ================================================================== DIAGRAMME EN BÂTONS / BARRES
def barres(etiq, hauteurs, ymax, pas, unite=.32, dx=1.1, larg=.22, titre_x="", titre_y="",
           valeurs=False, vert=(), y0=0, style="barre"):
    """Diagramme vertical : etiq = étiquettes sous l'axe, hauteurs = effectifs."""
    s = []
    n = len(etiq)
    W = (n + .2) * dx
    H = (ymax - y0) * unite
    k = y0
    while k <= ymax:
        y = (k - y0) * unite
        if k > y0:
            s.append(r"\draw[grille] (0,%.3f) -- (%.3f,%.3f);" % (y, W, y))
        s.append(r"\draw[axeS] (-.08,%.3f) -- (0,%.3f);" % (y, y))
        s.append(r"\node[petit,anchor=east] at (-.12,%.3f) {%s};" % (y, k))
        k += pas
    for i, (e, h) in enumerate(zip(etiq, hauteurs)):
        x = (i + .7) * dx
        st = "barreV" if i in vert else style
        s.append(r"\draw[%s] (%.3f,0) rectangle (%.3f,%.3f);" % (st, x - larg, x + larg, (h - y0) * unite))
        s.append(r"\node[txt,anchor=north] at (%.3f,-.12) {%s};" % (x, e))
        if valeurs:
            c = "otGreenDark" if i in vert else "otInk"
            s.append(r"\node[txt,anchor=south,text=%s] at (%.3f,%.3f) {%s};" % (c, x, (h - y0) * unite + .06, h))
    s.append(r"\draw[axeS] (0,0) -- (%.3f,0);" % W)
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (H + .35))
    if titre_y:
        s.append(r"\node[petit,anchor=south west] at (.1,%.3f) {%s};" % (H + .3, titre_y))
    if titre_x:
        s.append(r"\node[petit,anchor=north] at (%.3f,-.62) {%s};" % (W / 2, titre_x))
    return s


FIGURES = {}
NOTES = ["6", "8", "10", "12", "16"]
EFF = [2, 3, 6, 5, 4]
FIGURES["cours_batons"] = figure(barres(NOTES, EFF, 7, 1, titre_x="note sur 20", titre_y="effectif"))
FIGURES["ex2322_corrige"] = figure(barres(NOTES, EFF, 7, 1, titre_x="note sur 20", titre_y="effectif",
                                          valeurs=True, vert=(3, 4)))

# Histogramme : classes accolées
def histo(classes_bornes, eff, ymax, pas, unite=.36, dx=1.6, titre_x="", titre_y="", valeurs=False):
    s = []
    n = len(eff)
    W = (n + .3) * dx
    H = ymax * unite
    k = 0
    while k <= ymax:
        y = k * unite
        if k > 0:
            s.append(r"\draw[grille] (0,%.3f) -- (%.3f,%.3f);" % (y, W, y))
        s.append(r"\draw[axeS] (-.08,%.3f) -- (0,%.3f);" % (y, y))
        s.append(r"\node[petit,anchor=east] at (-.12,%.3f) {%s};" % (y, k))
        k += pas
    for i, h in enumerate(eff):
        x0, x1 = (i + .15) * dx, (i + 1.15) * dx
        s.append(r"\draw[barre] (%.3f,0) rectangle (%.3f,%.3f);" % (x0, x1, h * unite))
        if valeurs:
            s.append(r"\node[txt,anchor=south,text=otGreenDark] at (%.3f,%.3f) {%s};" % ((x0 + x1) / 2, h * unite + .06, h))
    for i, b in enumerate(classes_bornes):
        x = (i + .15) * dx
        s.append(r"\draw[axeS] (%.3f,0) -- (%.3f,-.08);" % (x, x))
        s.append(r"\node[petit,anchor=north] at (%.3f,-.12) {%s};" % (x, b))
    s.append(r"\draw[axeS] (0,0) -- (%.3f,0);" % W)
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (H + .35))
    s.append(r"\node[petit,anchor=south west] at (.1,%.3f) {%s};" % (H + .3, titre_y))
    s.append(r"\node[petit,anchor=north] at (%.3f,-.55) {%s};" % (W / 2, titre_x))
    return s


FIGURES["ex2325_enonce"] = figure(histo(["0", "10", "20", "30", "40"], [4, 8, 6, 2], 9, 1,
                                        titre_x="durée du trajet (min)", titre_y="effectif"))
FIGURES["cours_histo"] = FIGURES["ex2325_enonce"]


# ================================================================== DIAGRAMME CIRCULAIRE
def camembert(parts, r=1.7, vert=False, deux_lignes=False):
    """parts : liste (étiquette, angle en degrés, texte de l'angle).
    deux_lignes : angle sous l'étiquette (figure plus étroite, lisible sur téléphone)."""
    cols = ["otNavy!55", "otGreen!60", "otOrange!70", "otMuted!40"]
    s = []
    a = 90
    for i, (lab, ang, txt) in enumerate(parts):
        b = a - ang
        s.append(r"\fill[%s] (0,0) -- (%.3f:%.2f) arc[start angle=%.3f,end angle=%.3f,radius=%.2f] -- cycle;"
                 % (cols[i], a, r, a, b, r))
        a = b
    a = 90
    for i, (lab, ang, txt) in enumerate(parts):
        s.append(r"\draw[white,line width=1.2pt] (0,0) -- (%.3f:%.2f);" % (a, r))
        a -= ang
    s.append(r"\draw[otNavy,line width=.8pt] (0,0) circle (%.2f);" % r)
    a = 90
    for i, (lab, ang, txt) in enumerate(parts):
        m = a - ang / 2
        c = "otGreenDark" if vert else "otInk"
        sep = r"\\" if deux_lignes else " : "
        lab2 = lab + (r"%s\textcolor{%s}{%s}" % (sep, c, txt) if txt else "")
        s.append(r"\node[txt,align=center,anchor=%s] at (%.3f:%.2f) {%s};" % (_ancre(m), m, r + .15, lab2))
        a -= ang
    return s


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


FIGURES["ex2324_corrige"] = figure(camembert([("A", 90, "90°"), ("B", 162, "162°"),
                                              ("C", 108, "108°")], vert=True))
FIGURES["ex2336_corrige"] = figure(camembert([("moins de 1 h", 54, "54°"), ("1 h à 2 h", 126, "126°"),
                                              ("2 h à 3 h", 108, "108°"), ("3 h ou plus", 72, "72°")],
                                             vert=True, deux_lignes=True))
FIGURES["cours_circulaire"] = figure(camembert([("A", 90, r"25\,\%"), ("B", 162, r"45\,\%"),
                                                ("C", 108, r"30\,\%")]))


# ================================================================== TABLEAUX
def tableau(lignes, w0=2.6, w=1.15, h=.62, vert_lignes=(), vert_cases=(), fs=9.5):
    """lignes : liste de (en-tête, [cases]). vert_lignes : indices des lignes en vert.
    Largeur totale ≤ 6,6 cm pour un affichage sans réduction sur téléphone."""
    s = []
    n = len(lignes[0][1])
    W = w0 + n * w
    for r, (ent, cases) in enumerate(lignes):
        y = -r * h
        fond = "otGreen!15" if r in vert_lignes else "otSky"
        s.append(r"\fill[%s] (0,%.3f) rectangle (%.3f,%.3f);" % (fond, y, w0, y - h))
        ce = "otGreenDark" if r in vert_lignes else "otNavy"
        s.append(r"\node[txt,align=center,text=%s] at (%.3f,%.3f) {%s};" % (ce, w0 / 2, y - h / 2, ent))
        for k, v in enumerate(cases):
            c = "otGreenDark" if (r in vert_lignes or (r, k) in vert_cases) else "otInk"
            if (r, k) in vert_cases:
                s.append(r"\fill[otGreen!15] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (w0 + k * w, y, w0 + (k + 1) * w, y - h))
            s.append(r"\node[text=%s,align=center,font=\fontsize{%s}{%s}\selectfont] at (%.3f,%.3f) {%s};"
                     % (c, fs, fs + 1.5, w0 + (k + .5) * w, y - h / 2, v))
    R = len(lignes)
    s.append(r"\draw[otNavy,line width=.7pt] (0,0) rectangle (%.3f,%.3f);" % (W, -R * h))
    for r in range(1, R):
        s.append(r"\draw[otNavy,line width=.6pt] (0,%.3f) -- (%.3f,%.3f);" % (-r * h, W, -r * h))
    for k in range(n):
        s.append(r"\draw[otNavy,line width=.6pt] (%.3f,0) -- (%.3f,%.3f);" % (w0 + k * w, w0 + k * w, -R * h))
    return s


FIGURES["ex2323_enonce"] = figure(tableau([("Note", ["$6$", "$8$", "$10$", "$12$", "$16$"]),
                                           ("Effectif", ["$2$", "$3$", "$6$", "$5$", "$4$"])],
                                          w0=2.1, w=.9, h=.8, fs=11))
FIGURES["ex2323_corrige"] = figure(tableau([("Note", ["$6$", "$8$", "$10$", "$12$", "$16$"]),
                                            ("Effectif", ["$2$", "$3$", "$6$", "$5$", "$4$"]),
                                            (r"Effectif\\cumulé", ["$2$", "$5$", "$11$", "$16$", "$20$"])],
                                           w0=2.1, w=.9, h=.8, fs=11, vert_lignes=(2,), vert_cases=((0, 2),)))
FIGURES["ex2336_enonce"] = figure(tableau([(r"Temps\\d'écran", [r"moins\\de 1 h", r"1 h\\à 2 h", r"2 h\\à 3 h", r"3 h\\ou plus"]),
                                           ("Effectif", ["$30$", "$70$", "$60$", "$?$"])], w0=1.9, w=1.2, h=.95, fs=10))


# ================================================================== TABLEUR
def tableur():
    s = []
    cols = ["", "A", "B", "C"]
    wc = [.6, 2.0, 2.0, 2.6]
    xs = [0]
    for w in wc:
        xs.append(xs[-1] + w)
    h = .55
    data = [["1", "Valeur", "Effectif", ""], ["2", "$4$", "$3$", ""], ["3", "$7$", "$5$", ""],
            ["4", "$12$", "$2$", ""], ["5", "", "", ""]]
    R = len(data) + 1
    s.append(r"\fill[otSky] (0,0) rectangle (%.3f,%.3f);" % (xs[-1], -h))
    s.append(r"\fill[otSky] (0,0) rectangle (%.3f,%.3f);" % (xs[1], -R * h))
    for k, c in enumerate(cols):
        if c:
            s.append(r"\node[petit,text=otNavy] at (%.3f,%.3f) {%s};" % ((xs[k] + xs[k + 1]) / 2, -h / 2, c))
    for r, ligne in enumerate(data):
        y = -(r + 1) * h - h / 2
        for k, v in enumerate(ligne):
            if not v:
                continue
            st = "petit,text=otNavy" if k == 0 else ("txt" if r == 0 else "text=otInk")
            s.append(r"\node[%s] at (%.3f,%.3f) {%s};" % (st, (xs[k] + xs[k + 1]) / 2, y, v))
    for r in range(R + 1):
        s.append(r"\draw[otMuted!70,line width=.5pt] (0,%.3f) -- (%.3f,%.3f);" % (-r * h, xs[-1], -r * h))
    for x in xs:
        s.append(r"\draw[otMuted!70,line width=.5pt] (%.3f,0) -- (%.3f,%.3f);" % (x, x, -R * h))
    return s


FIGURES["ex2326_enonce"] = figure(tableur())


# ================================================================== GRAPHIQUE TROMPEUR
def trompeur(corrige=False):
    s = []
    # gauche : axe à partir de 78
    u = .5
    for k in range(78, 86, 2):
        y = (k - 78) * u
        s.append(r"\draw[grille] (0,%.3f) -- (2.6,%.3f);" % (y, y))
        s.append(r"\node[petit,anchor=east] at (-.1,%.3f) {%d};" % (y, k))
    for i, (an, v) in enumerate((("2025", 80), ("2026", 84))):
        x = .75 + i * 1.1
        s.append(r"\draw[barreO] (%.3f,0) rectangle (%.3f,%.3f);" % (x - .3, x + .3, (v - 78) * u))
        s.append(r"\node[txt,anchor=north] at (%.3f,-.12) {%s};" % (x, an))
    s.append(r"\draw[axeS] (0,0) -- (2.6,0);")
    s.append(r"\draw[axeS] (0,0) -- (0,%.3f);" % (7 * u))
    s.append(r"\node[txt,text=otOrange!80!black,anchor=south] at (1.3,%.3f) {Graphique 1};" % (7 * u + .2))
    # droite : axe à partir de 0
    ox = 4.4
    u2 = 3.5 / 90
    for k in range(0, 91, 20):
        y = k * u2
        s.append(r"\draw[grille] (%.3f,%.3f) -- (%.3f,%.3f);" % (ox, y, ox + 2.6, y))
        s.append(r"\node[petit,anchor=east] at (%.3f,%.3f) {%d};" % (ox - .1, y, k))
    for i, (an, v) in enumerate((("2025", 80), ("2026", 84))):
        x = ox + .75 + i * 1.1
        s.append(r"\draw[barre] (%.3f,0) rectangle (%.3f,%.3f);" % (x - .3, x + .3, v * u2))
        s.append(r"\node[txt,anchor=north] at (%.3f,-.12) {%s};" % (x, an))
    s.append(r"\draw[axeS] (%.3f,0) -- (%.3f,0);" % (ox, ox + 2.6))
    s.append(r"\draw[axeS] (%.3f,0) -- (%.3f,%.3f);" % (ox, ox, 3.5))
    s.append(r"\node[txt,text=otNavy,anchor=south] at (%.3f,%.3f) {Graphique 2};" % (ox + 1.3, 3.7))
    if not corrige:
        s.append(r"\node[petit,anchor=north] at (3.3,-.62) {nombre d'inscrits au club};")
        return s
    # corrigé : hauteurs visibles (graphique 1) et valeurs (graphique 2) en vert
    fl = r"otGreenDark,line width=.8pt,{Stealth[length=1.6mm]}-{Stealth[length=1.6mm]}"
    for i, v in enumerate((80, 84)):
        x = .75 + i * 1.1 + .4
        h = (v - 78) * u
        s.append(r"\draw[%s] (%.3f,0) -- (%.3f,%.3f);" % (fl, x, x, h))
        s.append(r"\node[txt,text=otGreenDark,anchor=west] at (%.3f,%.3f) {%d};" % (x + .05, h / 2, v - 78))
    for i, v in enumerate((80, 84)):
        x = ox + .75 + i * 1.1
        s.append(r"\node[txt,text=otGreenDark,anchor=south] at (%.3f,%.3f) {%d};" % (x, v * u2 + .06, v))
    s.append(r"\node[txt,text=otGreenDark,align=center,anchor=north] at (1.3,-.62)"
             r" {rapport visuel\\$6 \div 2 = 3$};")
    s.append(r"\node[txt,text=otGreenDark,align=center,anchor=north] at (%.3f,-.62)"
             r" {rapport réel\\$84 \div 80 = 1{,}05$};" % (ox + 1.3))
    return s


FIGURES["ex2332_enonce"] = figure(trompeur())
FIGURES["ex2332_corrige"] = figure(trompeur(corrige=True))


# ================================================================== SÉRIE TRIÉE, MÉDIANE EN VERT
def serie(vals, med_idx, med_txt, rangs=True, w=.66, rang_haut=False):
    """rang_haut : le mot « rang » au-dessus des rangs (figure plus étroite, pour 12 valeurs)."""
    s = []
    n = len(vals)
    for i, v in enumerate(vals):
        x = i * w
        st = "draw=otGreenDark,fill=otGreen!18,text=otGreenDark" if i in med_idx else "draw=otNavy,fill=otSky,text=otInk"
        s.append(r"\node[%s,line width=.7pt,minimum width=%.2fcm,minimum height=.6cm,inner sep=0pt,rounded corners=1.5pt]"
                 r" at (%.3f,0) {$%s$};" % (st, w - .02, x, v))
        if rangs:
            s.append(r"\node[petit] at (%.3f,.55) {%d};" % (x, i + 1))
    xm = sum(i * w for i in med_idx) / len(med_idx)
    s.append(r"\draw[otGreenDark,line width=.9pt,-{Stealth[length=2.2mm]}] (%.3f,-1.05) -- (%.3f,-.4);" % (xm, xm))
    s.append(r"\node[txt,text=otGreenDark,anchor=north] at (%.3f,-1.1) {%s};" % (xm, med_txt))
    if rangs and rang_haut:
        s.append(r"\node[petit,anchor=south west] at (%.3f,.85) {rang};" % (-w / 2))
    elif rangs:
        s.append(r"\node[petit,anchor=east] at (-.45,.55) {rang};")
    return s


FIGURES["cours_mediane"] = figure(serie(["2", "3", "5", "6", "6", "9", "11", "12"], (3, 4),
                                        r"médiane $=\dfrac{6+6}{2}=6$"))
FIGURES["ex2334_corrige"] = figure(serie(["22", "30", "38", "48", "51", "54", "55", "62", "66", "70", "72", "78"],
                                         (5, 6), r"médiane $=\dfrac{54+55}{2}=54{,}5$ mm",
                                         w=.52, rang_haut=True))


# ================================================================== COMPARAISON DE DEUX SÉRIES
def comparaison():
    s = []
    # deux séries de notes représentées sur une même droite graduée
    u = .34
    A = [10, 10, 11, 12, 12]
    B = [4, 8, 12, 14, 17]
    for k in range(0, 21, 2):
        x = k * u
        s.append(r"\draw[axeS] (%.3f,-.06) -- (%.3f,.06);" % (x, x))
        s.append(r"\node[petit,anchor=north] at (%.3f,-.12) {%d};" % (x, k))
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (%.3f,0);" % (20.6 * u))
    for nom, ser, y, col in (("Série A", A, 1.9, "otNavy"), ("Série B", B, .9, "otOrange!85!black")):
        vu = {}
        for v in ser:
            j = vu.get(v, 0)
            vu[v] = j + 1
            s.append(r"\fill[%s] (%.3f,%.3f) circle (2.4pt);" % (col, v * u, y + j * .2))
        s.append(r"\draw[%s,line width=1.6pt,opacity=.45] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, min(ser) * u, y - .22, max(ser) * u, y - .22))
        s.append(r"\node[txt,text=%s,anchor=south west] at (0,%.3f) {%s};" % (col, y + .25, nom))
    s.append(r"\node[petit,anchor=west] at (%.3f,1.9) {étendue 2};" % (13 * u))
    s.append(r"\node[petit,anchor=west] at (%.3f,.9) {étendue 13};" % (17.6 * u))
    return s


FIGURES["cours_comparaison"] = figure(comparaison())


def joueurs():
    """Exercice 2337 : points de A et B sur une droite graduée, étendues en vert."""
    s = []
    u = .28
    A = [12, 14, 15, 13, 16, 14]
    B = [5, 25, 8, 22, 6, 24]
    for k in range(0, 27, 5):
        x = k * u
        s.append(r"\draw[axeS] (%.3f,-.06) -- (%.3f,.06);" % (x, x))
        s.append(r"\node[petit,anchor=north] at (%.3f,-.12) {%d};" % (x, k))
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (%.3f,0);" % (26.8 * u))
    s.append(r"\node[petit,anchor=north west] at (%.3f,-.5) {points};" % (21 * u))
    for nom, ser, y, col in (("Joueur A", A, 2.0, "otNavy"), ("Joueur B", B, .95, "otOrange!85!black")):
        vu = {}
        for v in ser:
            j = vu.get(v, 0)
            vu[v] = j + 1
            s.append(r"\fill[%s] (%.3f,%.3f) circle (2.4pt);" % (col, v * u, y + j * .2))
        lo, hi = min(ser) * u, max(ser) * u
        s.append(r"\draw[otGreenDark,line width=.8pt,{Bar[width=5pt]}-{Bar[width=5pt]}] (%.3f,%.3f) -- (%.3f,%.3f);"
                 % (lo, y - .25, hi, y - .25))
        s.append(r"\node[txt,text=%s,anchor=south west] at (0,%.3f) {%s};" % (col, y + .25, nom))
    s.append(r"\node[txt,text=otGreenDark,anchor=west] at (%.3f,2.0) {étendue 4};" % (17 * u))
    s.append(r"\node[txt,text=otGreenDark,anchor=south] at (%.3f,.98) {étendue 20};" % (15 * u))
    return s


FIGURES["ex2337_corrige"] = figure(joueurs())
