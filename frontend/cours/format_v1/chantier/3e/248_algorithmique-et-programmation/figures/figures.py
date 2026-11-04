# -*- coding: utf-8 -*-
"""Figures de la notion 248 « Algorithmique et programmation » (3e), style des livres.

Les scripts sont de vrais blocs Scratch 3 dessinés par le module scratch.py (même dossier) :
formes et couleurs officielles des familles, textes mesurés (jamais coupés).
Chaque script est décrit une seule fois dans SCRIPTS ; verif_248.py le traduit en Python et
l'exécute ; les tracés du lutin des corrigés sont produits par cette exécution (en vert).
Énoncé : script (ou script à trous, cases A, B, C… en pointillés bleus).
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
    Drapeau(), Demander("Choisis un nombre"), Mettre("n", Reponse()),
    Mettre("r", Op(V("n"), "+", 3)), Mettre("r", Op(V("r"), "*", 2)), Dire(V("r"))]]}
SCRIPTS["cours_si"] = {"Lutin": [[
    Drapeau(), Demander("Quel est ton âge ?"), Mettre("âge", Reponse()),
    Si(Cmp(V("âge"), "<", 18), [Dire("Tu es mineur.")], sinon=[Dire("Tu es majeur.")])]]}
SCRIPTS["cours_repeter"] = {"Lutin": [[
    Drapeau(), Mettre("x", 0), Repeter(5, [Ajouter("x", 2)]), Dire(V("x"))]]}
SCRIPTS["cours_jusqua"] = {"Lutin": [[
    Drapeau(), Mettre("x", 1), JusquA(Cmp(V("x"), ">", 100), [Mettre("x", Op(V("x"), "*", 3))]), Dire(V("x"))]]}
SCRIPTS["cours_carre"] = {"Lutin": [[
    Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
    Repeter(4, [Avancer(50), TournerG(90)])]]}
COURS_DEF = [Definir("carré", ["côté"]), Repeter(4, [Avancer(Param("côté")), TournerG(90)])]
SCRIPTS["cours_bloc"] = {"Lutin": [COURS_DEF, [
    Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
    Appel("carré", [20]), Appel("carré", [40]), Appel("carré", [60])]]}
SCRIPTS["cours_messages"] = {
    "Chat": [[Drapeau(), Mettre("score", 0), Envoyer("compter", attendre=True), Dire(V("score"))]],
    "Balle": [[Recoit("compter"), Repeter(4, [Ajouter("score", 5)])]]}

# ---------------------------------------------------------------- exercices
SCRIPTS["2443"] = {"Lutin": [[Drapeau(), Mettre("x", 3), Ajouter("x", 5), Mettre("x", Op(V("x"), "*", 2)), Dire(V("x"))]]}
SCRIPTS["2443_echange"] = {"Lutin": [[Drapeau(), Mettre("x", 3), Mettre("x", Op(V("x"), "*", 2), hl=True),
                                       Ajouter("x", 5, hl=True), Dire(V("x"))]]}


def s2444(trous=True):
    def T(l, s):
        return Trou(l, s) if trous else s
    return {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("x", T("A", Reponse())),
                       Ajouter("x", T("B", 4)), Mettre("x", Op(V("x"), "*", T("C", 3))), Dire(V("x"))]]}


SCRIPTS["2444"] = s2444()
SCRIPTS["2444_ordre"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("x", Reponse()),
                                     Mettre("x", Op(V("x"), "*", 3)), Ajouter("x", 4), Dire(V("x"))]]}
SCRIPTS["2445"] = {"Lutin": [[Drapeau(), Mettre("x", 0), Repeter(4, [Ajouter("x", 3)]), Dire(V("x"))]]}
SCRIPTS["2445_10"] = {"Lutin": [[Drapeau(), Mettre("x", 0), Repeter(10, [Ajouter("x", 3)], hl=True), Dire(V("x"))]]}
SCRIPTS["2446"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("x", Reponse()),
                              Si(Cmp(V("x"), "<", 10), [Dire("petit")], sinon=[Dire("grand")])]]}
SCRIPTS["2446_ou"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("x", Reponse()),
                                 Si(Trou("?", Ou(Cmp(V("x"), "<", 10), Cmp(V("x"), "=", 10))),
                                    [Dire("petit")], sinon=[Dire("grand")])]]}
SCRIPTS["2447"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(-100, 50), Orienter(90), StyloBas(),
                              Avancer(80), AjouterY(-90), Orienter(-90), Avancer(60)]]}
SCRIPTS["2448"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                              Repeter(4, [Avancer(40), TournerG(90)])]]}
SCRIPTS["2448_triangle"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                                       Repeter(Trou("", 3), [Avancer(40), TournerG(Trou("", 120))])]]}
SCRIPTS["2449"] = {"Lutin": [[Drapeau(), Mettre("s", 0), Mettre("n", 1),
                              Repeter(5, [Ajouter("s", V("n")), Ajouter("n", 1)]), Dire(V("s"))]]}
SCRIPTS["2450"] = {"Lutin": [[Drapeau(), Mettre("x", 0), JusquA(Cmp(V("x"), ">", 20), [Ajouter("x", 6)]), Dire(V("x"))]]}
SCRIPTS["2451"] = {"Lutin": [[Drapeau(), Demander("Choisis un entier"), Mettre("x", Reponse()), Mettre("y", 0),
                              Si(Cmp(Mod(V("x"), 3), "=", 0), [Mettre("y", 1)]), Dire(V("y"))]]}
SCRIPTS["2451_pair"] = {"Lutin": [[Drapeau(), Demander("Choisis un entier"), Mettre("x", Reponse()), Mettre("y", 0),
                                   Si(Cmp(Mod(V("x"), Trou("", 2)), "=", 0), [Mettre("y", 1)]), Dire(V("y"))]]}
SCRIPTS["2452"] = {"Lutin": [[Drapeau(), Mettre("n", 12), Mettre("d", 1),
                              Repeter(12, [Si(Cmp(Mod(V("n"), V("d")), "=", 0), [Dire(V("d"), 1)]), Ajouter("d", 1)])]]}
SCRIPTS["2453"] = {"Lutin": [
    [Drapeau(), AllerA(-60, -40)],
    [ToucheHat("flèche droite"), AjouterX(30)],
    [ToucheHat("flèche haut"), AjouterY(20)],
    [ToucheHat("espace"), AllerA(0, 0)]]}
SCRIPTS["2453_gauche"] = {"Lutin": [[ToucheHat("flèche gauche", ), AjouterX(-30, hl=True)]]}
DEF_CARRE = [Definir("carré", ["côté"]), Repeter(4, [Avancer(Param("côté")), TournerG(90)])]
SCRIPTS["2454"] = {"Lutin": [DEF_CARRE, [
    Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
    Repeter(3, [Appel("carré", [30]), StyloHaut(), Avancer(40), StyloBas()])]]}
SCRIPTS["2455"] = {"Lutin": [[Drapeau(), Mettre("succès", 0),
                              Repeter(600, [Mettre("dé", Alea(1, 6)), Si(Cmp(V("dé"), "=", 6), [Ajouter("succès", 1)])]),
                              Dire(Op(V("succès"), "/", 600))]]}


def s2456(trous=True):
    def T(l, s):
        return Trou(l, s) if trous else s
    return {"Lutin": [[Drapeau(), EffacerTout(), AllerA(T("A", -40), T("B", -25)), Orienter(90), StyloBas(),
                       Repeter(T("C", 2), [Avancer(80), TournerG(90), Avancer(T("D", 50)), TournerG(T("E", 90))])]]}


SCRIPTS["2456"] = s2456()
SCRIPTS["2457"] = {
    "Guide": [[Drapeau(), Mettre("score", 0), Envoyer("départ", attendre=True), Dire(V("score"))]],
    "Joueur": [[Recoit("départ"), Repeter(10, [Ajouter("score", 1)])]]}
SCRIPTS["2457_trois"] = dict(SCRIPTS["2457"], Joueur2=[[Recoit("départ"), Repeter(10, [Ajouter("score", 1)])]])
SCRIPTS["2458"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("n", Reponse()),
                              Mettre("r", Op(V("n"), "*", 4)), Ajouter("r", 8), Mettre("r", Op(V("r"), "/", 4)),
                              Mettre("r", Op(V("r"), "-", V("n"))), Dire(V("r"))]]}
SCRIPTS["2459"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                              Repeter(5, [Avancer(20), TournerG(90), Avancer(20), TournerD(90)])]]}
SCRIPTS["2459_8"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                                Repeter(8, [Avancer(15), TournerG(90), Avancer(15), TournerD(90)])]]}


def def_polygone(angle=None):
    a = Op(360, "/", Param("n")) if angle is None else angle
    return [Definir("polygone", ["n", "côté"]), Repeter(Param("n"), [Avancer(Param("côté")), TournerG(a)])]


def main_polygone(n, c):
    return [Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(), Appel("polygone", [n, c])]


SCRIPTS["2460"] = {"Lutin": [def_polygone(), main_polygone(6, 30)]}
SCRIPTS["2460_triangle"] = {"Lutin": [def_polygone(), main_polygone(3, 50)]}
SCRIPTS["2460_36"] = {"Lutin": [def_polygone(), main_polygone(36, 5)]}
SCRIPTS["2460_faux108"] = {"Lutin": [def_polygone(108), main_polygone(5, 30)]}
SCRIPTS["2460_bon72"] = {"Lutin": [def_polygone(), main_polygone(5, 30)]}
SCRIPTS["2461"] = {"Lutin": [[
    Drapeau(), Mettre("secret", Alea(1, 100)), Mettre("essais", 0),
    JusquA(Cmp(Reponse(), "=", V("secret")), [
        Demander("Propose un nombre"), Ajouter("essais", 1),
        Si(Cmp(Reponse(), "<", V("secret")), [Dire("Plus grand !", 1)],
           sinon=[Si(Cmp(Reponse(), ">", V("secret")), [Dire("Plus petit !", 1)])])]),
    Dire(V("essais"))]]}
DEF_TRIANGLE = [Definir("triangle", ["côté"]), Repeter(3, [Avancer(Param("côté")), TournerG(120)])]


def s2462(grandit=True, ecart=True):
    corps = [StyloBas(), Appel("triangle", [V("longueur")]), StyloHaut(),
             Avancer(Op(V("longueur"), "+", 10) if ecart else V("longueur"))]
    if grandit:
        corps.append(Ajouter("longueur", 20))
    return {"Lutin": [DEF_TRIANGLE, [Drapeau(), EffacerTout(), AllerA(-150, 0), Orienter(90), Mettre("longueur", 20),
                                     Repeter(4, corps)]]}


SCRIPTS["2462"] = s2462()
SCRIPTS["2462_A"] = s2462(ecart=False)
SCRIPTS["2462_C"] = s2462(grandit=False)
SCRIPTS["2463"] = {"Lutin": [[Drapeau(), Mettre("compteur", 0),
                              Repeter(1000, [Mettre("d1", Alea(1, 6)), Mettre("d2", Alea(1, 6)),
                                             Si(Cmp(Op(V("d1"), "+", V("d2")), "=", 7), [Ajouter("compteur", 1)])]),
                              Dire(Op(V("compteur"), "/", 1000))]]}
SCRIPTS["2463_doubles"] = {"Lutin": [[Drapeau(), Mettre("compteur", 0),
                                      Repeter(1000, [Mettre("d1", Alea(1, 6)), Mettre("d2", Alea(1, 6)),
                                                     Si(Trou("", Cmp(V("d1"), "=", V("d2"))), [Ajouter("compteur", 1)])]),
                                      Dire(Op(V("compteur"), "/", 1000))]]}


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
scripts_fig("cours_si", piles("cours_si"))
scripts_fig("cours_repeter", piles("cours_repeter"))
scripts_fig("cours_jusqua", piles("cours_jusqua"))
scripts_fig("cours_carre", piles("cours_carre"))
scripts_fig("cours_bloc", piles("cours_bloc", {("Lutin", 0): "Bloc personnalisé", ("Lutin", 1): "Script principal"}))
scripts_fig("cours_messages", piles("cours_messages", {("Chat", 0): "Lutin Chat", ("Balle", 0): "Lutin Balle"}))

# exercices
scripts_fig("ex2443_script", piles("2443"))
scripts_fig("ex2443_echange", piles("2443_echange"), corrige=True)
scripts_fig("ex2444_trous", piles("2444"))
scripts_fig("ex2444_complete", piles("2444"), corrige=True)
scripts_fig("ex2445_script", piles("2445"))
scripts_fig("ex2445_10", piles("2445_10"), corrige=True)
scripts_fig("ex2446_script", piles("2446"))
scripts_fig("ex2446_ou", piles("2446_ou"), corrige=True)
scripts_fig("ex2447_script", piles("2447"))
scripts_fig("ex2448_script", piles("2448"))
scripts_fig("ex2448_triangle", piles("2448_triangle"), corrige=True)
scripts_fig("ex2449_script", piles("2449"))
scripts_fig("ex2450_script", piles("2450"))
scripts_fig("ex2451_script", piles("2451"))
scripts_fig("ex2451_pair", piles("2451_pair"), corrige=True)
scripts_fig("ex2452_script", piles("2452"))
scripts_fig("ex2453_scripts", piles("2453", {("Lutin", 0): "Script 1", ("Lutin", 1): "Script 2",
                                              ("Lutin", 2): "Script 3", ("Lutin", 3): "Script 4"}))
scripts_fig("ex2453_gauche", [("Script 5", SCRIPTS["2453_gauche"]["Lutin"][0])], corrige=True)
scripts_fig("ex2454_scripts", piles("2454", {("Lutin", 0): "Bloc personnalisé", ("Lutin", 1): "Script principal"}))
scripts_fig("ex2455_script", piles("2455"))
scripts_fig("ex2456_trous", piles("2456"))
scripts_fig("ex2456_complete", piles("2456"), corrige=True)
scripts_fig("ex2457_scripts", piles("2457", {("Guide", 0): "Lutin Guide", ("Joueur", 0): "Lutin Joueur"}))
scripts_fig("ex2458_script", piles("2458"))
scripts_fig("ex2459_script", piles("2459"))
scripts_fig("ex2460_scripts", piles("2460", {("Lutin", 0): "Bloc personnalisé", ("Lutin", 1): "Script principal"}))
scripts_fig("ex2461_script", piles("2461"))
scripts_fig("ex2462_scripts", piles("2462", {("Lutin", 0): "Bloc personnalisé", ("Lutin", 1): "Script principal"}))
scripts_fig("ex2463_script", piles("2463"))
scripts_fig("ex2463_doubles", piles("2463_doubles"), corrige=True)


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
        ("Mes blocs", Appel("carré", [30])),
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
    r = executer(SCRIPTS[cle])
    return r.lutins["lutin"]


def fenetre_auto(segs, pas, marge=1):
    xs = [p[0] for s in segs for p in s] + [0]
    ys = [p[1] for s in segs for p in s] + [0]
    return (pas * (math.floor(min(xs) / pas) - marge), pas * (math.ceil(max(xs) / pas) + marge),
            pas * (math.floor(min(ys) / pas) - marge), pas * (math.ceil(max(ys) / pas) + marge))


def C(x, y):
    """Coordonnées affichées « (x ; y) »."""
    return "(%s ; %s)" % (nombre_fr(x), nombre_fr(y))


# --- cours : la scène et les orientations
def figure_scene():
    u = .0155
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
    s.append(r"\fill[otNavy] %s circle (2.2pt);" % P(0, 0))
    txt = r"\node[anchor=%s,inner sep=1.5pt,font=\otMedium\fontsize{8.5}{10}\selectfont,text=otInk] at %s {%s};"
    s.append(txt % ("north west", P(10, -10), "centre " + C(0, 0)))
    s.append(txt % ("north east", P(226, 166), C(240, 180)))
    s.append(txt % ("south west", P(-226, -166), C(-240, -180)))
    s.append(txt % ("north west", P(-226, 166), C(-240, 180)))
    s.append(txt % ("south east", P(226, -166), C(240, -180)))
    # rose des orientations, sous la scène
    L = .78
    cx, cy = 0.0, -180 * u - 2.05
    s.append(r"\node[font=\otMedium\bfseries\fontsize{9}{10}\selectfont,text=otNavy,anchor=south] at (%s,%s) {Orientation du lutin};" % (_n(cx), _n(cy + L + .5)))
    for ang, txt, anc in ((0, "0", "south"), (90, "90", "west"), (180, "180", "north"), (-90, "−90", "east")):
        a = math.radians(ang)
        tx, ty = cx + L * math.sin(a), cy + L * math.cos(a)
        s.append(r"\draw[otNavy,line width=.9pt,-{Stealth[length=2.2mm]}] (%s,%s) -- (%s,%s);" % (_n(cx), _n(cy), _n(tx), _n(ty)))
        s.append(r"\node[anchor=%s,inner sep=2pt,font=\otMedium\fontsize{9}{10}\selectfont,text=otInk] at (%s,%s) {%s};" % (anc, _n(tx), _n(ty), txt))
    s.append(r"\fill[otOrange] (%s,%s) circle (2.6pt);" % (_n(cx), _n(cy)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_scene"] = figure_scene()

# --- cours : carré et bloc personnalisé
lu = trace("cours_carre")
FIGURES["cours_carre_trace"] = figure_trace(lu.segments, (-10, 70, -15, 65), 10, .07, depart=(0, 0), pas_lab=20,
                                            fleche=(lu.x, lu.y, lu.direction),
                                            points=[(50, 0, C(50, 0), "north west"), (50, 50, C(50, 50), "south west")])
lu = trace("cours_bloc")
FIGURES["cours_bloc_trace"] = figure_trace(lu.segments, (-10, 70, -10, 70), 10, .07, depart=(0, 0), pas_lab=20)

# --- exercices
lu = trace("2447")
FIGURES["ex2447_trace"] = figure_trace(
    lu.segments, (-120, 20, -60, 70), 10, .056, depart=(-100, 50), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(-100, 50, "A " + C(-100, 50), "south"), (-20, 50, "B " + C(-20, 50), "south"),
            (-20, -40, "C " + C(-20, -40), "north east"), (-80, -40, "D " + C(-80, -40), "north")])

lu = trace("2448")
FIGURES["ex2448_trace"] = figure_trace(
    lu.segments, (-20, 60, -15, 55), 10, .075, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(40, 0, C(40, 0), "north west"), (40, 40, C(40, 40), "south west"), (0, 40, C(0, 40), "south east")])
lu = trace("2448_triangle")
FIGURES["ex2448_triangle_trace"] = figure_trace(
    lu.segments, (-20, 60, -15, 50), 10, .075, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(40, 0, C(40, 0), "north west")])

# 2453 : trajet (sans stylo) du lutin piloté au clavier
r = executer(SCRIPTS["2453"], touches=["flèche droite"] * 3 + ["flèche haut"] * 4)
pos = r.lutins["lutin"].positions[1:]
segs = list(zip(pos[:-1], pos[1:]))
FIGURES["ex2453_trajet"] = figure_trace(
    [], (-80, 50, -60, 60), 10, .062, depart=(-60, -40), pas_lab=20,
    autres=[(segs, "otGreenDark,line width=1.3pt,dash pattern=on 3.5pt off 2pt")],
    points=[(-60, -40, C(-60, -40), "north"), (30, -40, C(30, -40), "north"), (30, 40, C(30, 40), "south")])
# points intermédiaires
FIGURES["ex2453_trajet"] = FIGURES["ex2453_trajet"].replace(
    r"\end{tikzpicture}", "\n".join(r"\fill[otGreenDark] (%s,%s) circle (1.8pt);" % (_n(x * .062), _n(y * .062))
                                     for (x, y) in pos[1:]) + "\n" + r"\end{tikzpicture}")

lu = trace("2454")
FIGURES["ex2454_trace"] = figure_trace(
    lu.segments, (-10, 130, -20, 45), 10, .056, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(120, 0, C(120, 0), "north")])

# 2456 : rectangle cible (énoncé) et tracé obtenu (corrigé)
rect = [((-40, -25), (40, -25)), ((40, -25), (40, 25)), ((40, 25), (-40, 25)), ((-40, 25), (-40, -25))]
FIGURES["ex2456_cible"] = figure_trace(rect, (-60, 60, -40, 40), 10, .065, vert=False, pas_lab=20)
lu = trace("2456")
FIGURES["ex2456_trace"] = figure_trace(
    lu.segments, (-60, 60, -40, 40), 10, .065, depart=(-40, -25), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(-40, -25, C(-40, -25), "north"), (40, -25, C(40, -25), "north"), (40, 25, C(40, 25), "south"),
            (-40, 25, C(-40, 25), "south")])

lu = trace("2459")
FIGURES["ex2459_trace"] = figure_trace(
    lu.segments, (-10, 110, -10, 110), 10, .062, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(20, 20, C(20, 20), "south east"), (100, 100, C(100, 100), "north west")])

lu = trace("2460")
FIGURES["ex2460_trace"] = figure_trace(
    lu.segments, (-30, 60, -15, 65), 10, .075, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(30, 0, C(30, 0), "north west")])
faux = trace("2460_faux108").segments
bon = trace("2460_bon72").segments
FIGURES["ex2460_pentagone"] = figure_trace(
    bon, fenetre_auto(faux + bon, 10), 10, .06, depart=(0, 0), pas_lab=20,
    autres=[(faux, "otOrange,line width=1.3pt,dash pattern=on 4pt off 2.5pt")])

lu = trace("2462")
FIGURES["ex2462_trace"] = figure_trace(
    lu.segments, (-160, 100, -20, 80), 10, .031, depart=(-150, 0), pas_lab=50, fleche=(lu.x, lu.y, lu.direction),
    points=[(-150, -5, C(-150, 0), "north"), (90, -5, C(90, 0), "north")])


def figure_dessins(dessins, u=.03):
    """Dessins candidats (sans repère), les uns sous les autres, titrés « Dessin A »…"""
    s = [r"\begin{tikzpicture}[line cap=round,line join=round]"]
    y0 = 0.0
    for titre, segs in dessins:
        xs = [p[0] for sg in segs for p in sg]
        ys = [p[1] for sg in segs for p in sg]
        x0, h = min(xs), max(ys) - min(ys)
        s.append(r"\node[anchor=north west,inner sep=0pt,font=\otMedium\bfseries\fontsize{9}{10}\selectfont,text=otNavy] at (0,%s) {%s};"
                 % (_n(y0), titre))
        base = y0 - .5 - h * u
        for a, b in segs:
            s.append(r"\draw[otNavy,line width=1.3pt] (%s,%s) -- (%s,%s);"
                     % (_n((a[0] - x0) * u + 1.6), _n(base + (a[1] - min(ys)) * u), _n((b[0] - x0) * u + 1.6),
                        _n(base + (b[1] - min(ys)) * u)))
        y0 = base - .45
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex2462_dessins"] = figure_dessins([("Dessin A", trace("2462_A").segments),
                                            ("Dessin B", trace("2462").segments),
                                            ("Dessin C", trace("2462_C").segments)])
