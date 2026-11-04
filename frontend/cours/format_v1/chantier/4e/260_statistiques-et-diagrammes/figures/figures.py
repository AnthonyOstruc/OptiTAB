# -*- coding: utf-8 -*-
"""Figures de la notion « Statistiques et diagrammes » (4e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, orange = seconde
série ou alerte, vert foncé = éléments de réponse (corrigés).
Les données (DONNEES) sont relues par verif_260.py.
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

DONNEES = {
    "cours_livres": ([0, 1, 2, 3, 4], [2, 6, 9, 5, 3]),
    "cours_mediane_impair": [8, 8, 10, 12, 13, 15, 17],
    "cours_mediane_pair": [4, 7, 7, 9, 12, 14, 15, 20],
    "cours_activites": [("Sport", 15), ("Jeux vidéo", 9), ("Lecture", 6), ("Musique", 6)],
    "cours_tailles": ([140, 150, 160, 170, 180], [4, 10, 8, 3]),
    "cours_temperatures": ([6, 8, 10, 12, 14, 16, 18, 20], [8, 10, 14, 18, 21, 20, 16, 12]),
    "cours_comparaison": ([9, 10, 10, 10, 11], [2, 6, 11, 14, 17]),
    "2684": [("Football", 8), ("Basket", 5), ("Natation", 4), ("Danse", 6), ("Tennis", 2)],
    "2685": ([0, 1, 2, 3, 4], [4, 9, 7, 3, 2]),
    "2686": [8, 12, 13, 15, 17],
    "2687": ([5, 7, 9, 9, 11, 12, 15], [5, 7, 9, 9, 11, 12, 15, 20]),
    "2689": [("À pied", 30), ("Vélo", 15), ("Bus", 40), ("Voiture", 15)],
    "2690": ([36, 37, 38, 39, 40], [3, 5, 8, 6, 3]),
    "2691": (["lun", "mar", "mer", "jeu", "ven", "sam", "dim"],
             [12, 14, 15, 13, 16, 14, 14], [6, 10, 18, 22, 20, 12, 10]),
    "2692": ([6, 8, 10, 12, 14, 16, 18], [2, 3, 5, 6, 4, 3, 2]),
    "2693": [38, 45, 52, 57, 61, 70, 84],
    "2695": [1500, 1500, 1500, 1500, 1800, 1800, 2100, 2600, 8000],
    "2697": ([0, 1, 2, 3, 4, 5], [12, 25, 30, 18, 15]),
    "2698": (["À pied", "Vélo", "Bus", "Voiture"], [26, 12, 42, 20], [32, 15, 32, 21]),
    "2699": [("Mer", "154,8", 154.8, 43, 86), ("Montagne", "86,4", 86.4, 24, 48),
             ("Campagne", "64,8", 64.8, 18, 36), ("Ville", "54", 54, 15, 30)],
    "2701": (102, 106),
    "2702": (["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"],
             [52, 45, 48, 55, 68, 50, 35, 30, 55, 70, 80, 65]),
    "2703": ([24, 25, 26, 25, 25, 24, 26, 25, 25, 25], [18, 19, 35, 20, 18, 40, 19, 18, 21, 22]),
    "2704": ([12, 13, 14, 15, 16, 17], [5, 8, 10, 7, 6, 4]),
}


def figure(corps, opt="line cap=round"):
    return "\n".join([r"\begin{tikzpicture}[%s]" % opt] + corps + [r"\end{tikzpicture}"])


def num(x):
    """Nombre au format français pour une formule : 1\\,500 ; 54{,}42."""
    s = ("%s" % x)
    if "." in s:
        e, d = s.split(".")
        return e + "{,}" + d
    if len(s) > 3:
        return s[:-3] + r"\," + s[-3:]
    return s


# ================================================================== DIAGRAMME EN BÂTONS / BARRES
def axe_vertical(s, ymax, pas, unite, W, y0=0, lab_pas=None):
    lab_pas = lab_pas or pas
    k = y0
    while k <= ymax + 1e-9:
        y = (k - y0) * unite
        if k > y0:
            s.append(r"\draw[grille] (0,%.3f) -- (%.3f,%.3f);" % (y, W, y))
        if round((k - y0) / lab_pas, 6) == int(round((k - y0) / lab_pas, 6)):
            s.append(r"\draw[axeS] (-.08,%.3f) -- (0,%.3f);" % (y, y))
            s.append(r"\node[petit,anchor=east] at (-.12,%.3f) {%s};" % (y, num(k)))
        k += pas


def barres(etiq, hauteurs, ymax, pas, unite=.36, dx=1.1, larg=.22, titre_x="", titre_y="",
           valeurs=False, vert=(), style="barre", lab_pas=None, couleur_val="otGreenDark", fs_etiq="txt"):
    """Diagramme vertical : etiq = étiquettes sous l'axe, hauteurs = effectifs.
    larg = demi-largeur (petite pour des bâtons, grande pour des barres)."""
    s = []
    n = len(etiq)
    W = (n + .2) * dx
    H = ymax * unite
    axe_vertical(s, ymax, pas, unite, W, lab_pas=lab_pas)
    for i, (e, h) in enumerate(zip(etiq, hauteurs)):
        x = (i + .7) * dx
        st = "barreV" if i in vert else style
        s.append(r"\draw[%s] (%.3f,0) rectangle (%.3f,%.3f);" % (st, x - larg, x + larg, h * unite))
        s.append(r"\node[%s,anchor=north] at (%.3f,-.12) {%s};" % (fs_etiq, x, e))
        if valeurs and (valeurs != "vert" or i in vert):
            c = couleur_val if (valeurs == "tous" or i in vert) else "otInk"
            s.append(r"\node[txt,anchor=south,text=%s] at (%.3f,%.3f) {%s};" % (c, x, h * unite + .06, h))
    s.append(r"\draw[axeS] (0,0) -- (%.3f,0);" % W)
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (H + .35))
    if titre_y:
        s.append(r"\node[petit,anchor=south west] at (.1,%.3f) {%s};" % (H + .3, titre_y))
    if titre_x:
        s.append(r"\node[petit,anchor=north] at (%.3f,-.6) {%s};" % (W / 2, titre_x))
    return s


FIGURES = {}

# --- cours : livres lus (bâtons)
LIV = DONNEES["cours_livres"]
FIGURES["cours_batons"] = figure(barres([str(v) for v in LIV[0]], LIV[1], 10, 1, unite=.3, dx=1.2, larg=.09,
                                        titre_x="nombre de livres lus", titre_y="effectif", lab_pas=2,
                                        valeurs="tous", couleur_val="otInk"))

# --- 2684 : sports (barres), corrigé
SP = DONNEES["2684"]
FIGURES["ex2684_corrige"] = figure(barres([n for n, _ in SP], [e for _, e in SP], 9, 1, unite=.4, dx=1.45, larg=.42,
                                          titre_x="sport préféré", titre_y="effectif", valeurs="tous",
                                          vert=tuple(range(5)), fs_etiq="petit"))

# --- 2685 : fratrie (bâtons)
FR = DONNEES["2685"]
FIGURES["ex2685_enonce"] = figure(barres([str(v) for v in FR[0]], FR[1], 10, 1, unite=.3, dx=1.2, larg=.09,
                                         titre_x="nombre de frères et sœurs", titre_y="effectif", lab_pas=2))
FIGURES["ex2685_corrige"] = figure(barres([str(v) for v in FR[0]], FR[1], 10, 1, unite=.3, dx=1.2, larg=.09,
                                          titre_x="nombre de frères et sœurs", titre_y="effectif",
                                          valeurs="tous", couleur_val="otInk", vert=(2, 3, 4), lab_pas=2))

# --- 2692 : notes (bâtons), corrigé
NO = DONNEES["2692"]
FIGURES["ex2692_corrige"] = figure(barres([str(v) for v in NO[0]], NO[1], 7, 1, unite=.42, dx=1.0, larg=.08,
                                          titre_x="note sur 20", titre_y="effectif", valeurs="tous",
                                          vert=tuple(range(7))))


# ================================================================== BARRES GROUPÉES (deux séries)
def barres_doubles(etiq, h1, h2, ymax, pas, noms, unite=.14, dx=1.1, larg=.2, valeurs=True,
                   couleur_val="otInk", suffixe="", titre_y="", lab_pas=None, fs_val=8, leg_dx=2.0):
    s = []
    n = len(etiq)
    W = (n + .2) * dx
    H = ymax * unite
    axe_vertical(s, ymax, pas, unite, W, lab_pas=lab_pas)
    for i, e in enumerate(etiq):
        x = (i + .7) * dx
        for j, (h, st) in enumerate(((h1[i], "barre"), (h2[i], "barreO"))):
            xa = x - 2 * larg if j == 0 else x
            s.append(r"\draw[%s] (%.3f,0) rectangle (%.3f,%.3f);" % (st, xa, xa + 2 * larg, h * unite))
            if valeurs:
                s.append(r"\node[text=%s,font=\otMedium\fontsize{%s}{%s}\selectfont,inner sep=1pt,anchor=south]"
                         r" at (%.3f,%.3f) {%s%s};" % (couleur_val, fs_val, fs_val + 1, xa + larg, h * unite + .05, h, suffixe))
        s.append(r"\node[txt,anchor=north] at (%.3f,-.12) {%s};" % (x, e))
    s.append(r"\draw[axeS] (0,0) -- (%.3f,0);" % W)
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (H + .35))
    if titre_y:
        s.append(r"\node[petit,anchor=south west] at (.1,%.3f) {%s};" % (H + .3, titre_y))
    # légende au-dessus, à droite
    yl = H + .55
    xl = W - leg_dx - 1.9
    s.append(r"\draw[barre] (%.3f,%.3f) rectangle ++(.3,.22);" % (xl, yl))
    s.append(r"\node[txt,anchor=west] at (%.3f,%.3f) {%s};" % (xl + .38, yl + .11, noms[0]))
    s.append(r"\draw[barreO] (%.3f,%.3f) rectangle ++(.3,.22);" % (xl + leg_dx, yl))
    s.append(r"\node[txt,anchor=west] at (%.3f,%.3f) {%s};" % (xl + leg_dx + .38, yl + .11, noms[1]))
    return s


V = DONNEES["2691"]
FIGURES["ex2691_enonce"] = figure(barres_doubles(V[0], V[1], V[2], 24, 2, ("ville A", "ville B"), unite=.15,
                                                 dx=1.12, larg=.22, lab_pas=4, titre_y="température (°C)"))

C2 = DONNEES["2698"]
FIGURES["ex2698_corrige"] = figure(barres_doubles(C2[0], C2[1], C2[2], 45, 5, ("Jean-Moulin", "Pasteur"),
                                                  unite=.085, dx=1.9, larg=.36, couleur_val="otGreenDark",
                                                  suffixe=r"\,\%", lab_pas=10, titre_y=r"fréquence (\%)", fs_val=8.5,
                                                  leg_dx=2.5))


# ================================================================== HISTOGRAMME
def histo(bornes, eff, ymax, pas, unite=.12, dx=1.45, titre_x="", titre_y="", valeurs=True,
          vert=(), rangs=None, lab_pas=None):
    s = []
    n = len(eff)
    W = (n + .3) * dx
    H = ymax * unite
    axe_vertical(s, ymax, pas, unite, W, lab_pas=lab_pas)
    for i, h in enumerate(eff):
        x0, x1 = (i + .15) * dx, (i + 1.15) * dx
        st = "barreV" if i in vert else "barre"
        s.append(r"\draw[%s] (%.3f,0) rectangle (%.3f,%.3f);" % (st, x0, x1, h * unite))
        if valeurs:
            c = "otGreenDark" if i in vert else "otInk"
            s.append(r"\node[txt,anchor=south,text=%s] at (%.3f,%.3f) {%s};" % (c, (x0 + x1) / 2, h * unite + .06, h))
    for i, b in enumerate(bornes):
        x = (i + .15) * dx
        s.append(r"\draw[axeS] (%.3f,0) -- (%.3f,-.08);" % (x, x))
        s.append(r"\node[petit,anchor=north] at (%.3f,-.12) {%s};" % (x, b))
    s.append(r"\draw[axeS] (0,0) -- (%.3f,0);" % W)
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (H + .35))
    s.append(r"\node[petit,anchor=south west] at (.1,%.3f) {%s};" % (H + .3, titre_y))
    yt = -.6
    if rangs:
        s.append(r"\node[petit,anchor=east] at (-.12,-.75) {rangs};")
        for i, r in enumerate(rangs):
            c = "otGreenDark" if i in vert else "otMuted"
            s.append(r"\node[petit,text=%s] at (%.3f,-.75) {%s};" % (c, (i + .65) * dx, r))
        yt = -1.1
    s.append(r"\node[petit,anchor=north] at (%.3f,%.3f) {%s};" % (W / 2, yt, titre_x))
    return s


TA = DONNEES["cours_tailles"]
FIGURES["cours_histo"] = figure(histo([str(b) for b in TA[0]], TA[1], 12, 1, unite=.27, dx=1.5, lab_pas=2,
                                      titre_x="taille (cm)", titre_y="effectif"))
EC = DONNEES["2697"]
FIGURES["ex2697_enonce"] = figure(histo([str(b) for b in EC[0]], EC[1], 35, 5, unite=.1, dx=1.45,
                                        titre_x="temps d'écran par jour (h)", titre_y="effectif"))
FIGURES["ex2697_corrige"] = figure(histo([str(b) for b in EC[0]], EC[1], 35, 5, unite=.1, dx=1.45,
                                         titre_x="temps d'écran par jour (h)", titre_y="effectif", vert=(2,),
                                         rangs=["1–12", "13–37", "38–67", "68–85", "86–100"]))


# ================================================================== DIAGRAMME CIRCULAIRE
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


def camembert(parts, r=1.6, vert=False):
    """parts : liste (étiquette, angle en degrés, texte sous l'étiquette)."""
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
        lab2 = lab + (r"\\\textcolor{%s}{%s}" % (c, txt) if txt else "")
        s.append(r"\node[txt,align=center,anchor=%s] at (%.3f:%.2f) {%s};" % (_ancre(m), m, r + .15, lab2))
        a -= ang
    return s


ACT = DONNEES["cours_activites"]
FIGURES["cours_circulaire"] = figure(camembert([(n, e * 10, r"%d°" % (e * 10)) for n, e in ACT]))
TR = DONNEES["2689"]
FIGURES["ex2689_corrige"] = figure(camembert([(n, p * 3.6, r"%s°" % num(round(p * 3.6, 1)).replace("{,}0", ""))
                                              for n, p in TR], vert=True))
VA = DONNEES["2699"]
FIGURES["ex2699_enonce"] = figure(camembert([(n, a, r"%s°" % t.replace(",", "{,}")) for n, t, a, _, _ in VA]))
FIGURES["ex2699_corrige"] = figure(camembert([(n, a, r"%d\,\%% : %d pers." % (p, e)) for n, t, a, p, e in VA],
                                             vert=True))


# ================================================================== SÉRIE RANGÉE, MÉDIANE EN VERT
def serie(vals, med_idx, med_txt, w=.66, y=0, rang_haut=False, nom=None, fs=None):
    s = []
    for i, v in enumerate(vals):
        x = i * w
        st = ("draw=otGreenDark,fill=otGreen!18,text=otGreenDark" if i in med_idx
              else "draw=otNavy,fill=otSky,text=otInk")
        f = (r",font=\fontsize{%s}{%s}\selectfont" % (fs, fs + 2)) if fs else ""
        s.append(r"\node[%s,line width=.7pt,minimum width=%.2fcm,minimum height=.6cm,inner sep=0pt,"
                 r"rounded corners=1.5pt%s] at (%.3f,%.3f) {$%s$};" % (st, w - .04, f, x, y, num(v)))
        s.append(r"\node[petit] at (%.3f,%.3f) {%d};" % (x, y + .55, i + 1))
    xm = sum(i * w for i in med_idx) / len(med_idx)
    s.append(r"\draw[otGreenDark,line width=.9pt,-{Stealth[length=2.2mm]}] (%.3f,%.3f) -- (%.3f,%.3f);"
             % (xm, y - 1.0, xm, y - .4))
    s.append(r"\node[txt,text=otGreenDark,anchor=north] at (%.3f,%.3f) {%s};" % (xm, y - 1.05, med_txt))
    if rang_haut:
        s.append(r"\node[petit,anchor=south west] at (%.3f,%.3f) {rang};" % (-w / 2, y + .85))
    else:
        s.append(r"\node[petit,anchor=east] at (%.3f,%.3f) {rang};" % (-w / 2 - .05, y + .55))
    if nom:
        s.append(r"\node[txt,text=otNavy,anchor=south west] at (%.3f,%.3f) {%s};" % (-w / 2, y + .85, nom))
    return s


MI, MP = DONNEES["cours_mediane_impair"], DONNEES["cours_mediane_pair"]
FIGURES["cours_mediane"] = figure(
    serie(MI, (3,), r"$N = 7$ : 4\textsuperscript{e} valeur, médiane $= 12$", y=0, nom=r"Effectif impair")
    + serie(MP, (3, 4), r"$N = 8$ : médiane $= \dfrac{9 + 12}{2} = 10{,}5$", y=-3.1, nom=r"Effectif pair"))

FIGURES["ex2686_corrige"] = figure(serie(DONNEES["2686"], (2,), r"3\textsuperscript{e} valeur : médiane $= 13$"))
S7, S8 = DONNEES["2687"]
FIGURES["ex2687_corrige"] = figure(
    serie(S7, (3,), r"7 valeurs : médiane $= 9$", y=0, nom="Question 2")
    + serie(S8, (3, 4), r"8 valeurs : médiane $= \dfrac{9 + 11}{2} = 10$", y=-3.1, nom="Question 3"))
FIGURES["ex2693_corrige"] = figure(serie(DONNEES["2693"], (3,), r"4\textsuperscript{e} valeur : médiane $= 57$"))
FIGURES["ex2695_corrige"] = figure(serie(DONNEES["2695"], (4,), r"5\textsuperscript{e} valeur : médiane $= 1\,800$ €",
                                         w=.93, rang_haut=True, fs=9.5))
PL = DONNEES["2702"][1]
FIGURES["ex2702_mediane"] = figure(serie(sorted(PL), (5, 6), r"médiane $= \dfrac{52 + 55}{2} = 53{,}5$ mm",
                                         w=.56, rang_haut=True))
IA, IB = DONNEES["2703"]
FIGURES["ex2703_mediane"] = figure(
    serie(sorted(IA), (4, 5), r"médiane de A $= \dfrac{25 + 25}{2} = 25$", w=.6, y=0, nom="Itinéraire A")
    + serie(sorted(IB), (4, 5), r"médiane de B $= \dfrac{19 + 20}{2} = 19{,}5$", w=.6, y=-3.1, nom="Itinéraire B"))


# ================================================================== RANGS D'UN TABLEAU D'EFFECTIFS
def rangs_tableau(valeurs, effectifs, med_rangs, med_txt, w=1.05, unite_val=""):
    """Une case par valeur (valeur, ×effectif), rangs occupés en dessous ; case de la médiane en vert."""
    s = []
    debut = 1
    for i, (v, e) in enumerate(zip(valeurs, effectifs)):
        fin = debut + e - 1
        contient = any(debut <= r <= fin for r in med_rangs)
        x = i * w
        st = ("draw=otGreenDark,fill=otGreen!18" if contient else "draw=otNavy,fill=otSky")
        s.append(r"\draw[%s,line width=.7pt,rounded corners=1.5pt] (%.3f,-.45) rectangle (%.3f,.45);"
                 % (st, x + .03, x + w - .03))
        c = "otGreenDark" if contient else "otInk"
        s.append(r"\node[text=%s] at (%.3f,.12) {$%s$};" % (c, x + w / 2, v))
        s.append(r"\node[petit,text=%s] at (%.3f,-.24) {$\times %d$};" % (c if contient else "otMuted", x + w / 2, e))
        s.append(r"\node[petit,text=%s] at (%.3f,-.75) {%d–%d};" % (c if contient else "otMuted", x + w / 2, debut, fin))
        if contient:
            xm = x + w / 2
        debut = fin + 1
    s.append(r"\node[petit,anchor=east] at (-.08,-.75) {rangs};")
    s.append(r"\node[petit,anchor=east] at (-.08,.12) {%s};" % unite_val if unite_val else "")
    s.append(r"\draw[otGreenDark,line width=.9pt,-{Stealth[length=2.2mm]}] (%.3f,-1.65) -- (%.3f,-1.0);" % (xm, xm))
    s.append(r"\node[txt,text=otGreenDark,anchor=north] at (%.3f,-1.7) {%s};" % (xm, med_txt))
    return s


PO = DONNEES["2690"]
FIGURES["ex2690_corrige"] = figure(rangs_tableau(PO[0], PO[1], (13,), r"13\textsuperscript{e} valeur : médiane $= 38$",
                                                 unite_val="pointure"))
FIGURES["ex2692_mediane"] = figure(rangs_tableau(NO[0], NO[1], (13,), r"13\textsuperscript{e} note : médiane $= 12$",
                                                 w=.95, unite_val="note"))
AG = DONNEES["2704"]
FIGURES["ex2704_corrige"] = figure(rangs_tableau(AG[0], AG[1], (20, 21),
                                                 r"20\textsuperscript{e} et 21\textsuperscript{e} : médiane $= 14$ ans",
                                                 unite_val="âge"))


# ================================================================== COMPARAISON SUR UNE DROITE GRADUÉE
def comparaison(A, B, noms, vmax, pas_lab, u, unite="", etendues=None, vert=False):
    s = []
    k = 0
    while k <= vmax:
        x = k * u
        s.append(r"\draw[axeS] (%.3f,-.06) -- (%.3f,.06);" % (x, x))
        s.append(r"\node[petit,anchor=north] at (%.3f,-.12) {%d};" % (x, k))
        k += pas_lab
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (%.3f,0);" % ((vmax + .8) * u))
    if unite:
        s.append(r"\node[petit,anchor=west] at (%.3f,0) {%s};" % ((vmax + .9) * u, unite))
    for nom, ser, y, col in ((noms[0], A, 2.0, "otNavy"), (noms[1], B, .95, "otOrange!85!black")):
        vu = {}
        for v in ser:
            j = vu.get(v, 0)
            vu[v] = j + 1
            s.append(r"\fill[%s] (%.3f,%.3f) circle (2.4pt);" % (col, v * u, y + j * .2))
        lo, hi = min(ser) * u, max(ser) * u
        cl = "otGreenDark" if vert else "otMuted"
        s.append(r"\draw[%s,line width=.8pt,{Bar[width=5pt]}-{Bar[width=5pt]}] (%.3f,%.3f) -- (%.3f,%.3f);"
                 % (cl, lo, y - .25, hi, y - .25))
        s.append(r"\node[txt,text=%s,anchor=south west] at (0,%.3f) {%s};" % (col, y + .55, nom))
        txt = r"étendue %s" % num(max(ser) - min(ser))
        s.append(r"\node[txt,text=%s,anchor=west] at (%.3f,%.3f) {%s};" % (cl, hi + .2, y - .25, txt))
    return s


CA, CB = DONNEES["cours_comparaison"]
FIGURES["cours_comparaison"] = figure(comparaison(CA, CB, ("Série A", "Série B"), 20, 2, .3))
FIGURES["ex2691_corrige"] = figure(comparaison(V[1], V[2], ("Ville A", "Ville B"), 24, 2, .27, unite="°C", vert=True))


# ================================================================== COURBES
def courbe(xs, series, xmin, xmax, xpas, ymin, ymax, ypas, ux, uy, titre_x, titre_y, ylab_pas=None,
           seuil=None, marques=(), lectures=(), legende=None, xfmt="%d"):
    s = []
    ylab_pas = ylab_pas or ypas
    W = (xmax - xmin) * ux
    H = (ymax - ymin) * uy
    k = ymin
    while k <= ymax + 1e-9:
        y = (k - ymin) * uy
        if k > ymin:
            s.append(r"\draw[grille] (0,%.3f) -- (%.3f,%.3f);" % (y, W, y))
        if round((k - ymin) / ylab_pas, 6) == int(round((k - ymin) / ylab_pas, 6)):
            s.append(r"\draw[axeS] (-.08,%.3f) -- (0,%.3f);" % (y, y))
            s.append(r"\node[petit,anchor=east] at (-.12,%.3f) {%d};" % (y, k))
        k += ypas
    k = xmin
    while k <= xmax + 1e-9:
        x = (k - xmin) * ux
        if k > xmin:
            s.append(r"\draw[grille] (%.3f,0) -- (%.3f,%.3f);" % (x, x, H))
        s.append(r"\draw[axeS] (%.3f,0) -- (%.3f,-.08);" % (x, x))
        s.append(r"\node[petit,anchor=north] at (%.3f,-.12) {%s};" % (x, xfmt % k))
        k += xpas
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (%.3f,0);" % (W + .35))
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (H + .35))
    s.append(r"\node[petit,anchor=south west] at (.1,%.3f) {%s};" % (H + .3, titre_y))
    s.append(r"\node[petit,anchor=north] at (%.3f,-.55) {%s};" % (W / 2, titre_x))
    P = lambda x, y: ((x - xmin) * ux, (y - ymin) * uy)
    if seuil:
        v, lab = seuil
        s.append(r"\draw[seuil] (0,%.3f) -- (%.3f,%.3f);" % (P(0, v)[1] if False else (v - ymin) * uy, W, (v - ymin) * uy))
        s.append(r"\node[petit,text=otOrange!80!black,anchor=west] at (%.3f,%.3f) {%s};" % (W + .08, (v - ymin) * uy, lab))
    for ys, col, forme in series:
        pts = " -- ".join("(%.3f,%.3f)" % P(x, y) for x, y in zip(xs, ys))
        s.append(r"\draw[%s,line width=1.2pt,line join=round] %s;" % (col, pts))
        for x, y in zip(xs, ys):
            px, py = P(x, y)
            if forme == "carre":
                s.append(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, px - .06, py - .06, px + .06, py + .06))
            else:
                s.append(r"\fill[%s] (%.3f,%.3f) circle (2.2pt);" % (col, px, py))
    for (x, y) in marques:
        px, py = P(x, y)
        s.append(r"\draw[otGreenDark,line width=1pt] (%.3f,%.3f) circle (5pt);" % (px, py))
    for (x, y, txt, ancre) in lectures:
        px, py = P(x, y)
        s.append(r"\draw[otGreenDark,line width=.6pt,dash pattern=on 2pt off 1.6pt] (%.3f,0) -- (%.3f,%.3f) -- (0,%.3f);"
                 % (px, px, py, py))
        s.append(r"\fill[otGreenDark] (%.3f,%.3f) circle (2.4pt);" % (px, py))
        dy = .12 if "south" in ancre else -.14
        dx = .1 if "west" in ancre else 0
        s.append(r"\node[txt,text=otGreenDark,anchor=%s] at (%.3f,%.3f) {%s};" % (ancre, px + dx, py + dy, txt))
    if legende:
        yl = -1.25
        xl = W / 2 - 2.55
        for j, (nom, col, forme) in enumerate(legende):
            xx = xl + j * 2.75
            s.append(r"\draw[%s,line width=1.2pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, xx, yl, xx + .45, yl))
            if forme == "carre":
                s.append(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, xx + .165, yl - .06, xx + .285, yl + .06))
            else:
                s.append(r"\fill[%s] (%.3f,%.3f) circle (2.2pt);" % (col, xx + .225, yl))
            s.append(r"\node[txt,anchor=west] at (%.3f,%.3f) {%s};" % (xx + .52, yl, nom))
    return s


TX, TY = DONNEES["cours_temperatures"]
FIGURES["cours_courbe"] = figure(courbe(TX, [(TY, "otNavy", "rond")], 6, 20, 2, 0, 24, 2, .5, .15,
                                        "heure de la journée (h)", "température (°C)", ylab_pas=4,
                                        lectures=[(14, 21, r"max : 21\,°C", "south"),
                                                  (6, 8, r"min : 8\,°C", "north west")]))
JOURS = list(range(1, 11))
FIGURES["ex2703_enonce"] = figure(courbe(JOURS, [(IA, "otNavy", "rond"), (IB, "otOrange!85!black", "carre")],
                                         1, 10, 1, 0, 45, 5, .68, .085, "jour", "durée du trajet (min)", ylab_pas=10,
                                         seuil=(30, "30 min"),
                                         legende=[("itinéraire A", "otNavy", "rond"),
                                                  ("itinéraire B", "otOrange!85!black", "carre")]))
FIGURES["ex2703_corrige"] = figure(courbe(JOURS, [(IA, "otNavy", "rond"), (IB, "otOrange!85!black", "carre")],
                                          1, 10, 1, 0, 45, 5, .68, .085, "jour", "durée du trajet (min)", ylab_pas=10,
                                          seuil=(30, "30 min"), marques=[(3, 35), (6, 40)],
                                          legende=[("itinéraire A", "otNavy", "rond"),
                                                   ("itinéraire B", "otOrange!85!black", "carre")])
                                   + [r"\node[txt,text=otGreenDark,anchor=south] at (%.3f,%.3f) {retard};"
                                      % ((3 - 1) * .68, 35 * .085 + .2),
                                      r"\node[txt,text=otGreenDark,anchor=south] at (%.3f,%.3f) {retard};"
                                      % ((6 - 1) * .68, 40 * .085 + .2)])


# ================================================================== PLUIE (12 mois)
MOIS, PLUIE = DONNEES["2702"]
FIGURES["ex2702_enonce"] = figure(barres(MOIS, PLUIE, 90, 10, unite=.042, dx=.64, larg=.2, titre_x="mois",
                                         titre_y="précipitations (mm)", valeurs="tous", couleur_val="otInk",
                                         lab_pas=20))
MOY = 653 / 12
_haut = tuple(i for i, p in enumerate(PLUIE) if p > MOY)
_c = barres(MOIS, PLUIE, 90, 10, unite=.042, dx=.64, larg=.2, titre_x="mois", titre_y="précipitations (mm)",
            valeurs="vert", vert=_haut, lab_pas=20)
_W = (12 + .2) * .64
_c.append(r"\draw[seuil] (0,%.3f) -- (%.3f,%.3f);" % (MOY * .042, _W, MOY * .042))
_c.append(r"\draw[seuil] (%.3f,%.3f) -- ++(.5,0);" % (_W - 3.3, 90 * .042 + .55))
_c.append(r"\node[txt,text=otOrange!80!black,anchor=west] at (%.3f,%.3f) {moyenne $\approx 54{,}42$ mm};"
          % (_W - 2.72, 90 * .042 + .55))
FIGURES["ex2702_corrige"] = figure(_c)


# ================================================================== GRAPHIQUE TROMPEUR
def trompeur(corrige=False):
    v1, v2 = DONNEES["2701"]
    s = []
    u = .5
    for k in range(100, 108):
        y = (k - 100) * u
        if k > 100:
            s.append(r"\draw[grille] (0,%.3f) -- (2.6,%.3f);" % (y, y))
        s.append(r"\node[petit,anchor=east] at (-.1,%.3f) {%d};" % (y, k))
    for i, (an, v) in enumerate((("2022", v1), ("2023", v2))):
        x = .75 + i * 1.1
        s.append(r"\draw[barreO] (%.3f,0) rectangle (%.3f,%.3f);" % (x - .3, x + .3, (v - 100) * u))
        s.append(r"\node[txt,anchor=north] at (%.3f,-.12) {%s};" % (x, an))
    s.append(r"\draw[axeS] (0,0) -- (2.6,0);")
    s.append(r"\draw[axeS] (0,0) -- (0,%.3f);" % (7 * u + .2))
    s.append(r"\node[petit,anchor=south west] at (-.6,%.3f) {ventes (milliers d'articles)};" % (7 * u + .3))
    if not corrige:
        return s
    s.append(r"\node[txt,text=otOrange!80!black,anchor=south] at (1.3,%.3f) {graphique publié};" % (7 * u + .8))
    fl = r"otGreenDark,line width=.8pt,{Stealth[length=1.6mm]}-{Stealth[length=1.6mm]}"
    for i, v in enumerate((v1, v2)):
        x = .75 + i * 1.1 + .4
        h = (v - 100) * u
        s.append(r"\draw[%s] (%.3f,0) -- (%.3f,%.3f);" % (fl, x, x, h))
        s.append(r"\node[txt,text=otGreenDark,anchor=west] at (%.3f,%.3f) {%d};" % (x + .05, h / 2, v - 100))
    s.append(r"\node[txt,text=otGreenDark,align=center,anchor=north] at (1.3,-.62) {rapport visuel\\$6 \div 2 = 3$};")
    # graphique honnête : axe à partir de 0
    ox = 4.6
    u2 = 3.5 / 120
    for k in range(0, 121, 20):
        y = k * u2
        if k > 0:
            s.append(r"\draw[grille] (%.3f,%.3f) -- (%.3f,%.3f);" % (ox, y, ox + 2.6, y))
        s.append(r"\node[petit,anchor=east] at (%.3f,%.3f) {%d};" % (ox - .1, y, k))
    for i, (an, v) in enumerate((("2022", v1), ("2023", v2))):
        x = ox + .75 + i * 1.1
        s.append(r"\draw[barre] (%.3f,0) rectangle (%.3f,%.3f);" % (x - .3, x + .3, v * u2))
        s.append(r"\node[txt,anchor=north] at (%.3f,-.12) {%s};" % (x, an))
        s.append(r"\node[txt,text=otGreenDark,anchor=south] at (%.3f,%.3f) {%d};" % (x, v * u2 + .06, v))
    s.append(r"\draw[axeS] (%.3f,0) -- (%.3f,0);" % (ox, ox + 2.6))
    s.append(r"\draw[axeS] (%.3f,0) -- (%.3f,%.3f);" % (ox, ox, 3.7))
    s.append(r"\node[txt,text=otNavy,anchor=south] at (%.3f,%.3f) {axe à partir de 0};" % (ox + 1.3, 4.3))
    s.append(r"\node[txt,text=otGreenDark,align=center,anchor=north] at (%.3f,-.62)"
             r" {rapport réel\\$106 \div 102 \approx 1{,}04$};" % (ox + 1.3))
    return s


FIGURES["ex2701_enonce"] = figure(trompeur())
FIGURES["ex2701_corrige"] = figure(trompeur(corrige=True))
