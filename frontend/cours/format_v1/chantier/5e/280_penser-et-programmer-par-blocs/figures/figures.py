# -*- coding: utf-8 -*-
"""Figures de la notion 280 « Penser et programmer par blocs » (5e), style des livres.

Les scripts sont de vrais blocs Scratch 3 dessinés par le module scratch.py (copie NON
modifiée du module de la notion 4e 290, lui-même copie de la notion 3e 248) : formes et
couleurs officielles des familles, textes mesurés (jamais coupés).
Chaque script est décrit une seule fois dans SCRIPTS ; verif_280.py le traduit en Python et
l'exécute ; les tracés du lutin des corrigés sont produits par cette exécution (en vert).
Énoncé : script (ou script à trous, cases en pointillés bleus).
Corrigé : cases complétées et blocs modifiés en vert, tracé obtenu en vert sur le repère.
"""
import math
from scratch import *
from scratch import _n, _tex

PREAMBULE_EXTRA = PREAMBULE_SCRATCH
FIGURES = {}
TOLERE = {}
TEXTE_BLOC = "textes blancs écrits sur le fond coloré des blocs Scratch : aucun trait sous le texte " \
             "(contrôlé par controle_scratch.py sur une version à fonds blancs)"


def scripts_fig(nom, scripts, corrige=False, **kw):
    FIGURES[nom] = figure_scripts(scripts, corrige=corrige, **kw)
    TOLERE[nom] = TEXTE_BLOC


# ======================================================================== SCRIPTS
# Un « projet » = {lutin: [script, …]} ; un script = [chapeau, blocs…]
SCRIPTS = {}

# ---------------------------------------------------------------- cours
SCRIPTS["cours_calcul"] = {"Lutin": [[
    Drapeau(), Demander("Choisis un nombre"), Mettre("nombre", Reponse()),
    Mettre("résultat", Op(V("nombre"), "+", 5)), Mettre("résultat", Op(V("résultat"), "*", 2)),
    Dire(V("résultat"))]]}
SCRIPTS["cours_L"] = {"Lutin": [[
    Drapeau(), EffacerTout(), AllerA(0, 80), Orienter(180), StyloBas(),
    Avancer(80), TournerG(90), Avancer(40)]]}
SCRIPTS["cours_carre"] = {"Lutin": [[
    Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
    Repeter(4, [Avancer(60), TournerG(90)])]]}
SCRIPTS["cours_si"] = {"Lutin": [[
    Drapeau(), Demander("Combien de points ?"), Mettre("score", Reponse()),
    Si(Cmp(V("score"), ">", 50), [Dire("Niveau réussi !", 2)]), Dire("Fin de la partie")]]}
SCRIPTS["cours_touches"] = {"Lutin": [
    [Drapeau(), AllerA(0, 0)],
    [ToucheHat("flèche droite"), AjouterX(10)],
    [ToucheHat("flèche gauche"), AjouterX(-10)]]}

# ---------------------------------------------------------------- exercices
# 3104 : exécuter un programme de calcul (4x + 6)
SCRIPTS["3104"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("nombre", Reponse()),
                              Mettre("résultat", Op(V("nombre"), "*", 4)), Ajouter("résultat", 6),
                              Dire(V("résultat"))]]}
SCRIPTS["3104_mettre"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("nombre", Reponse()),
                                     Mettre("résultat", Op(V("nombre"), "*", 4)),
                                     Mettre("résultat", Op(V("résultat"), "+", 6), hl=True),
                                     Dire(V("résultat"))]]}
SCRIPTS["3104_faux"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("nombre", Reponse()),
                                   Mettre("résultat", Op(V("nombre"), "*", 4)), Mettre("résultat", 6),
                                   Dire(V("résultat"))]]}

# 3105 : un carré tracé avec une boucle (tourner ↻)
SCRIPTS["3105"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                              Repeter(4, [Avancer(50), TournerD(90)])]]}
SCRIPTS["3105_sans_stylo"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90),
                                         Repeter(4, [Avancer(50), TournerD(90)])]]}


# 3110 : compléter une séquence de déplacements (rectangle 80 × 40)
def s3110(trous=True):
    def t(lettre, v):
        return Trou(lettre, v) if trous else v
    return {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                       Avancer(80), TournerG(90), Avancer(t("A", 40)), TournerG(t("B", 90)),
                       Avancer(t("C", 80)), TournerG(90), Avancer(t("D", 40))]]}


SCRIPTS["3110"] = s3110()
SCRIPTS["3110_boucle"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                                     Repeter(2, [Avancer(80), TournerG(90), Avancer(40), TournerG(90)], hl=True)]]}


# 3108 : des blocs opérateurs emboîtés
def s3108(calcul, hl=False):
    return {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("nombre", Reponse()),
                       Mettre("résultat", calcul, hl=hl), Dire(V("résultat"))]]}


SCRIPTS["3108_lea"] = s3108(Op(Op(V("nombre"), "*", 4), "+", 3))
SCRIPTS["3108_tom"] = s3108(Op(4, "*", Op(V("nombre"), "+", 3)))
SCRIPTS["3108_trou"] = s3108(Op(Trou("A", Op(V("nombre"), "+", 5)), "*", 2))
SCRIPTS["3108_tom_corrige"] = s3108(Op(Op(4, "*", V("nombre")), "+", 3), hl=True)

# 3117 : polygones réguliers, choisir l'angle
SCRIPTS["3117"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                              Repeter(3, [Avancer(80), TournerG(60)])]]}
SCRIPTS["3117_triangle"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                                       Repeter(3, [Avancer(80), TournerG(Trou("", 120))])]]}


def s3117_hexagone():
    return {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                       Repeter(Trou("A", 6), [Avancer(50), TournerG(Trou("B", 60))])]]}


SCRIPTS["3117_hexagone"] = s3117_hexagone()


# 3106 : une instruction « si … alors » (tarif du cinéma)
def s3106(seuil=12, senior=False):
    test = Cmp(Reponse(), "<", Trou("", seuil) if seuil != 12 else seuil)
    blocs = [Drapeau(), Demander("Quel est ton âge ?"), Mettre("prix", 9), Si(test, [Mettre("prix", 6)])]
    if senior:
        blocs.append(Si(Cmp(Reponse(), ">", 64), [Mettre("prix", 7)], hl=True))
    blocs.append(Dire(V("prix")))
    return {"Lutin": [blocs]}


SCRIPTS["3106"] = s3106()
SCRIPTS["3106_13"] = s3106(13)
SCRIPTS["3106_senior"] = s3106(13, senior=True)


# 3114 : piloter le lutin au clavier (événements)
def touche(nom, orientation):
    return [ToucheHat(nom), Orienter(orientation), Avancer(20)]


SCRIPTS["3114"] = {"Lutin": [
    [Drapeau(), EffacerTout(), AllerA(0, 0), StyloBas()],
    touche("flèche droite", 90),
    touche("flèche haut", 0),
    touche("flèche gauche", -90),
    touche("flèche bas", 180)]}
SCRIPTS["3114_espace"] = {"Lutin": [[ToucheHat("espace", ), StyloHaut(hl=True)]]}
SEQUENCE_3114 = ["flèche droite", "flèche droite", "flèche haut", "flèche haut", "flèche haut", "flèche gauche"]
RETOUR_3114 = ["flèche gauche", "flèche bas", "flèche bas", "flèche bas"]


# 3122 : un escalier (boucle, rotations alternées)
def s3122(n=4, droite=True):
    tour2 = TournerD(90) if droite else TournerG(90, hl=True)
    return {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                       Repeter(Trou("", n) if n != 4 else n, [Avancer(30), TournerG(90), Avancer(20), tour2])]]}


SCRIPTS["3122"] = s3122()
SCRIPTS["3122_7"] = s3122(7)
SCRIPTS["3122_gauche"] = s3122(droite=False)


# 3115 : la tirelire de Lina (synthèse : variables, boucle, condition)
def s3115(n=8, seuil=150, corr=False):
    rep = Trou("", n) if corr and n != 8 else n
    cond = Cmp(V("tirelire"), ">", Trou("", seuil) if corr and seuil != 150 else seuil)
    return {"Lutin": [[Drapeau(), Mettre("semaine", 0), Mettre("tirelire", 30),
                       Repeter(rep, [Ajouter("semaine", 1), Ajouter("tirelire", 15)]),
                       Dire(V("tirelire"), 2),
                       Si(cond, [Dire("Objectif atteint !", 2)])]]}


SCRIPTS["3115"] = s3115()
SCRIPTS["3115_149"] = s3115(seuil=149, corr=True)
SCRIPTS["3115_velo"] = s3115(n=12, seuil=199, corr=True)


# 3124 : la clôture du potager (synthèse)
def s3124(budget=False, trous=True):
    blocs = [Drapeau(), EffacerTout(), Demander("Longueur en mètres ?"), Mettre("longueur", Reponse()),
             Demander("Largeur en mètres ?"), Mettre("largeur", Reponse()),
             Mettre("clôture", Op(V("longueur"), "+", V("largeur"))),
             Mettre("clôture", Op(V("clôture"), "*", 2)),
             Dire(V("clôture"), 2)]
    if budget:
        a = Trou("A", 4) if trous else 4
        b = Trou("B", 150) if trous else 150
        blocs += [Mettre("prix", Op(V("clôture"), "*", a), hl=not trous),
                  Si(Cmp(V("prix"), ">", b), [Dire("Budget dépassé !")], hl=not trous)]
    blocs += [AllerA(0, 0), Orienter(90), StyloBas(),
              Repeter(2, [Avancer(Op(V("longueur"), "*", 10)), TournerG(90),
                          Avancer(Op(V("largeur"), "*", 10)), TournerG(90)])]
    return {"Lutin": [blocs]}


SCRIPTS["3124"] = s3124()
SCRIPTS["3124_budget"] = s3124(budget=True)


def piles(cle, titres=None):
    p = SCRIPTS[cle]
    out = []
    for lutin, scripts in p.items():
        for k, sc in enumerate(scripts):
            t = ""
            if titres:
                t = titres.get((lutin, k), "")
            out.append((t, sc))
    return out


# ======================================================================== figures de scripts
# cours
scripts_fig("cours_calcul", piles("cours_calcul"))
scripts_fig("cours_L", piles("cours_L"))
scripts_fig("cours_carre", piles("cours_carre"))
scripts_fig("cours_si", piles("cours_si"))
scripts_fig("cours_touches", piles("cours_touches", {("Lutin", 0): "Script 1", ("Lutin", 1): "Script 2",
                                                      ("Lutin", 2): "Script 3"}), ecart=12.0)

# blocs emboîtés (cours) : deux reporters seuls
FIGURES["cours_emboites"] = figure_scripts([
    ("Bloc 1", [Seul(Op(Op(V("n"), "*", 2), "+", 1))]),
    ("Bloc 2", [Seul(Op(Op(V("n"), "+", 1), "*", 2))])], ecart=12.0)
TOLERE["cours_emboites"] = TEXTE_BLOC

# exercices
scripts_fig("ex3104_script", piles("3104"))
scripts_fig("ex3104_mettre", piles("3104_mettre"), corrige=True)
scripts_fig("ex3105_script", piles("3105"))
scripts_fig("ex3110_script", piles("3110"))
scripts_fig("ex3110_corrige", piles("3110"), corrige=True)
scripts_fig("ex3110_boucle", piles("3110_boucle"), corrige=True)
scripts_fig("ex3108_scripts", [("Script de Léa", SCRIPTS["3108_lea"]["Lutin"][0]),
                               ("Script de Tom", SCRIPTS["3108_tom"]["Lutin"][0])])
scripts_fig("ex3108_trou", piles("3108_trou"))
scripts_fig("ex3108_trou_corrige", piles("3108_trou"), corrige=True)
scripts_fig("ex3108_tom_corrige", [("Script de Tom corrigé", SCRIPTS["3108_tom_corrige"]["Lutin"][0])], corrige=True)
scripts_fig("ex3117_script", piles("3117"))
scripts_fig("ex3117_triangle", piles("3117_triangle"), corrige=True)
scripts_fig("ex3117_hexagone", piles("3117_hexagone"))
scripts_fig("ex3117_hexagone_corrige", piles("3117_hexagone"), corrige=True)
scripts_fig("ex3106_script", piles("3106"))
scripts_fig("ex3106_13", piles("3106_13"), corrige=True)
scripts_fig("ex3106_senior", piles("3106_senior"), corrige=True)
scripts_fig("ex3114_scripts", piles("3114", {("Lutin", k): "Script %d" % (k + 1) for k in range(5)}), ecart=12.0)
scripts_fig("ex3114_espace", [("Script 6", SCRIPTS["3114_espace"]["Lutin"][0])], corrige=True)
scripts_fig("ex3122_script", piles("3122"))
scripts_fig("ex3122_7", piles("3122_7"), corrige=True)
scripts_fig("ex3122_gauche", piles("3122_gauche"), corrige=True)
scripts_fig("ex3115_script", piles("3115"))
scripts_fig("ex3115_149", piles("3115_149"), corrige=True)
scripts_fig("ex3115_velo", piles("3115_velo"), corrige=True)
scripts_fig("ex3124_script", piles("3124"))
BUDGET_3124 = SCRIPTS["3124_budget"]["Lutin"][0][9:11]
scripts_fig("ex3124_budget", [("Blocs ajoutés après « dire clôture »", BUDGET_3124)])
scripts_fig("ex3124_budget_corrige", [("Blocs ajoutés, complétés", BUDGET_3124)], corrige=True)


# ======================================================================== palette des familles (cours, fiche)
def figure_familles():
    lignes = [
        ("Événements", Drapeau()),
        ("Contrôle", Repeter(10, [])),
        ("Variables", Mettre("x", 0)),
        ("Opérateurs", Seul(Op(V("x"), "+", 5))),
        ("Capteurs", Demander("Âge ?")),
        ("Apparence", Dire("Bonjour !")),
        ("Mouvement", Avancer(10)),
        ("Stylo", StyloBas()),
    ]
    s = []
    y = 0.0
    xb = 68.0
    for nom, b in lignes:
        h = b.hauteur()
        haut = y
        if b.genre == "chapeau":
            s += dessin_pile([b], xb, y)
            ym = y - CAP - (h - CAP) / 2
        else:
            s += b.dessin(xb, y)
            ym = y - (h / 2 if b.genre != "C" else b.ligne()[2] / 2)
        s.append(r"\node[anchor=base west,inner sep=0pt,text=otInk,font=\otMedium\fontsize{9}{10}\selectfont] at (0,%s) {%s};"
                 % (_n(ym - 3.2), _tex(nom)))
        y = haut - h - 7
    return "\n".join([r"\begin{tikzpicture}[x=1pt,y=1pt,line cap=round]"] + s + [r"\end{tikzpicture}"])


FIGURES["cours_familles"] = figure_familles()
TOLERE["cours_familles"] = TEXTE_BLOC


# ======================================================================== tracés (exécution des scripts)
def trace(cle, **kw):
    r = executer(SCRIPTS[cle], **kw)
    return r.lutins["lutin"]


def C(x, y):
    """Coordonnées affichées « (x ; y) »."""
    return "(%s ; %s)" % (nombre_fr(x), nombre_fr(y))


def ajoute(fig, lignes):
    return fig.replace(r"\end{tikzpicture}", "\n".join(lignes) + "\n" + r"\end{tikzpicture}")


def points_verts(pts, u):
    return [r"\fill[otGreenDark] (%s,%s) circle (1.9pt);" % (_n(x * u), _n(y * u)) for (x, y) in pts]


# --- cours : la scène et les orientations
def figure_scene(u=.0155):
    s = [r"\begin{tikzpicture}[line cap=round,line join=round]"]

    def P(x, y):
        return "(%s,%s)" % (_n(x * u), _n(y * u))
    s.append(r"\fill[otSky!60] %s rectangle %s;" % (P(-240, -180), P(240, 180)))
    for k in range(-180, 181, 60):
        s.append(r"\draw[otRule,line width=.35pt] %s -- %s;" % (P(-240, k), P(240, k)))
    for k in range(-240, 241, 60):
        s.append(r"\draw[otRule,line width=.35pt] %s -- %s;" % (P(k, -180), P(k, 180)))
    s.append(r"\draw[otNavy,line width=.8pt] %s rectangle %s;" % (P(-240, -180), P(240, 180)))
    s.append(r"\draw[otMuted,line width=.6pt,-{Stealth[length=2.2mm]}] %s -- %s;" % (P(-240, 0), P(262, 0)))
    s.append(r"\draw[otMuted,line width=.6pt,-{Stealth[length=2.2mm]}] %s -- %s;" % (P(0, -180), P(0, 202)))
    s.append(r"\node[font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=west,inner sep=1pt] at %s {$x$};" % P(266, 0))
    s.append(r"\node[font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=south,inner sep=1pt] at %s {$y$};" % P(0, 206))
    txt = r"\node[anchor=%s,inner sep=1.5pt,font=\otMedium\fontsize{8.5}{10}\selectfont,text=otInk] at %s {%s};"
    s.append(txt % ("north east", P(226, 166), C(240, 180)))
    s.append(txt % ("south west", P(-226, -166), C(-240, -180)))
    s.append(txt % ("north west", P(-226, 166), C(-240, 180)))
    s.append(txt % ("south east", P(226, -166), C(240, -180)))
    s.append(r"\fill[otNavy] %s circle (2.2pt);" % P(0, 0))
    s.append(txt % ("north west", P(10, -10), "centre " + C(0, 0)))
    L = .78
    cx, cy = 0.0, -180 * u - 2.05
    s.append(r"\node[font=\otMedium\bfseries\fontsize{9}{10}\selectfont,text=otNavy,anchor=south] at (%s,%s) {Orientation du lutin};"
             % (_n(cx), _n(cy + L + .5)))
    for ang, t, anc in ((0, "0 (haut)", "south"), (90, "90 (droite)", "west"), (180, "180 (bas)", "north"),
                        (-90, "−90 (gauche)", "east")):
        a = math.radians(ang)
        tx, ty = cx + L * math.sin(a), cy + L * math.cos(a)
        s.append(r"\draw[otNavy,line width=.9pt,-{Stealth[length=2.2mm]}] (%s,%s) -- (%s,%s);" % (_n(cx), _n(cy), _n(tx), _n(ty)))
        s.append(r"\node[anchor=%s,inner sep=2pt,font=\otMedium\fontsize{9}{10}\selectfont,text=otInk] at (%s,%s) {%s};"
                 % (anc, _n(tx), _n(ty), t))
    s.append(r"\fill[otOrange] (%s,%s) circle (2.6pt);" % (_n(cx), _n(cy)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_scene"] = figure_scene()

# --- cours : la lettre L, le carré
lu = trace("cours_L")
FIGURES["cours_L_trace"] = figure_trace(
    lu.segments, (-20, 60, -10, 90), 10, .06, depart=(0, 80), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 80, C(0, 80), "west,xshift=2pt"), (0, 0, C(0, 0), "south west"), (40, 0, C(40, 0), "south")])
lu = trace("cours_carre")
FIGURES["cours_carre_trace"] = figure_trace(
    lu.segments, (-30, 100, -15, 80), 10, .062, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(60, 0, C(60, 0), "north west"), (60, 60, C(60, 60), "south west"), (0, 60, C(0, 60), "south east")])

# --- 3105 : carré sous l'axe
lu = trace("3105")
FIGURES["ex3105_trace"] = figure_trace(
    lu.segments, (-30, 90, -70, 20), 10, .065, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 0, C(0, 0), "south east"), (50, 0, C(50, 0), "south west"),
            (50, -50, C(50, -50), "north west"), (0, -50, C(0, -50), "north east")])

# --- 3110 : rectangle 80 × 40
lu = trace("3110")
FIGURES["ex3110_trace"] = figure_trace(
    lu.segments, (-20, 120, -20, 60), 10, .058, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 0, C(0, 0), "north east"), (80, 0, C(80, 0), "north west"),
            (80, 40, C(80, 40), "south west"), (0, 40, C(0, 40), "south east")])

# --- 3117 : la ligne ouverte, le triangle, l'hexagone
lu = trace("3117")
FIGURES["ex3117_trace"] = figure_trace(
    lu.segments, (-40, 160, -20, 160), 10, .04, depart=(0, 0), pas_lab=40, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 0, "départ", "south east")])
lu = trace("3117_triangle")
FIGURES["ex3117_triangle_trace"] = figure_trace(
    lu.segments, (-20, 100, -20, 90), 10, .058, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 0, C(0, 0), "north east"), (80, 0, C(80, 0), "north west")])
lu = trace("3117_hexagone")
FIGURES["ex3117_hexagone_trace"] = figure_trace(
    lu.segments, (-50, 100, -20, 110), 10, .052, depart=(0, 0), pas_lab=50, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 0, C(0, 0), "north east"), (50, 0, C(50, 0), "north west")])

# --- 3114 : trajet au clavier
r = executer(SCRIPTS["3114"], touches=SEQUENCE_3114)
lu = r.lutins["lutin"]
FIGURES["ex3114_trace"] = ajoute(figure_trace(
    lu.segments, (-20, 60, -20, 80), 10, .075, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 0, C(0, 0), "north east"), (40, 0, C(40, 0), "north west"),
            (40, 60, C(40, 60), "south west"), (20, 60, C(20, 60), "south east")]),
    points_verts([(20, 0), (40, 20), (40, 40)], .075))

# --- 3122 : l'escalier, l'escalier de 7 marches, le rectangle parcouru deux fois
lu = trace("3122")
FIGURES["ex3122_trace"] = ajoute(figure_trace(
    lu.segments, (-10, 140, -10, 100), 10, .052, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(30, 20, C(30, 20), "south east"), (60, 40, C(60, 40), "south east"), (90, 60, C(90, 60), "south east"),
            (120, 80, C(120, 80), "south east")]),
    points_verts([(30, 20), (60, 40), (90, 60), (120, 80)], .052))
lu = trace("3122_gauche")
FIGURES["ex3122_gauche_trace"] = figure_trace(
    lu.segments, (-20, 50, -10, 40), 10, .11, depart=(0, 0), pas_lab=10, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 0, C(0, 0), "north east"), (30, 0, C(30, 0), "north west"), (30, 20, C(30, 20), "south west"),
            (0, 20, C(0, 20), "south east")])

# --- 3124 : le potager 12 m × 8 m
r = executer(SCRIPTS["3124"], entrees=[12, 8])
lu = r.lutins["lutin"]
FIGURES["ex3124_trace"] = figure_trace(
    lu.segments, (-20, 160, -20, 100), 10, .045, depart=(0, 0), pas_lab=40, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 0, C(0, 0), "north east"), (120, 0, C(120, 0), "north west"),
            (120, 80, C(120, 80), "south west"), (0, 80, C(0, 80), "south east")])
