# -*- coding: utf-8 -*-
"""Figures de la notion 290 « Algorithmique et programmation » (4e), style des livres.

Les scripts sont de vrais blocs Scratch 3 dessinés par le module scratch.py (copie NON
modifiée du module de la notion 3e 248) : formes et couleurs officielles des familles,
textes mesurés (jamais coupés).
Chaque script est décrit une seule fois dans SCRIPTS ; verif_290.py le traduit en Python et
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
    Drapeau(), Demander("Choisis un nombre"), Mettre("n", Reponse()),
    Mettre("r", Op(V("n"), "-", 2)), Mettre("r", Op(V("r"), "*", 5)), Dire(V("r"))]]}
SCRIPTS["cours_si"] = {"Lutin": [[
    Drapeau(), Demander("Ta note sur 20 ?"), Mettre("note", Reponse()),
    Si(Cmp(V("note"), "<", 10), [Dire("À retravailler")], sinon=[Dire("Validé !")])]]}
SCRIPTS["cours_repeter"] = {"Lutin": [[
    Drapeau(), Mettre("x", 0), Repeter(5, [Ajouter("x", 3)]), Dire(V("x"))]]}
SCRIPTS["cours_jusqua"] = {"Lutin": [[
    Drapeau(), Mettre("x", 100), JusquA(Cmp(V("x"), "<", 0), [Ajouter("x", -30)]), Dire(V("x"))]]}
SCRIPTS["cours_carre"] = {"Lutin": [[
    Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
    Repeter(4, [Avancer(60), TournerG(90)])]]}
DEF_TRIANGLE = [Definir("triangle", ["côté"]), Repeter(3, [Avancer(Param("côté")), TournerG(120)])]
SCRIPTS["cours_bloc"] = {"Lutin": [DEF_TRIANGLE, [
    Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
    Appel("triangle", [30]), Appel("triangle", [60]), Appel("triangle", [90])]]}
SCRIPTS["cours_touches"] = {"Lutin": [
    [ToucheHat("flèche droite"), AjouterX(10)],
    [ToucheHat("flèche gauche"), AjouterX(-10)]]}
SCRIPTS["cours_messages"] = {
    "Chat": [[Drapeau(), Mettre("total", 0), Envoyer("compter", attendre=True), Dire(V("total"))]],
    "Chien": [[Recoit("compter"), Repeter(3, [Ajouter("total", 4)])]]}

# ---------------------------------------------------------------- exercices
# 3713 : lire un script de tracé (carré, tourner ↻)
SCRIPTS["3713"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                              Repeter(4, [Avancer(100), TournerD(90)])]]}
SCRIPTS["3713_gauche"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(),
                                     Repeter(4, [Avancer(100), TournerG(90, hl=True)])]]}

# 3714 : programme de calcul 3x − 5
SCRIPTS["3714"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("x", Reponse()),
                              Mettre("y", Op(V("x"), "*", 3)), Mettre("y", Op(V("y"), "-", 5)), Dire(V("y"), 2)]]}
SCRIPTS["3714_ajouter"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("x", Reponse()),
                                      Mettre("y", Op(V("x"), "*", 3)), Ajouter("y", -5, hl=True), Dire(V("y"), 2)]]}
SCRIPTS["3714_faux"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("x", Reponse()),
                                   Mettre("y", Op(V("x"), "*", 3)), Mettre("y", -5), Dire(V("y"), 2)]]}


# 3715 : une boucle qui additionne
def s3715(n=5, hl=False):
    return {"Lutin": [[Drapeau(), Mettre("compteur", 0), Mettre("somme", 0),
                       Repeter(n, [Ajouter("compteur", 1), Ajouter("somme", V("compteur"))], hl=hl),
                       Dire(V("somme"), 2)]]}


SCRIPTS["3715"] = s3715()
SCRIPTS["3715_10"] = s3715(10, hl=True)
SCRIPTS["3715_inverse"] = {"Lutin": [[Drapeau(), Mettre("compteur", 0), Mettre("somme", 0),
                                      Repeter(5, [Ajouter("somme", V("compteur")), Ajouter("compteur", 1)]),
                                      Dire(V("somme"), 2)]]}

# 3716 : si … alors … sinon
SCRIPTS["3716"] = {"Lutin": [[Drapeau(), Demander("Quel âge as-tu ?"),
                              Si(Cmp(Reponse(), ">", 17), [Dire("Tu es majeur.")], sinon=[Dire("Tu es mineur.")])]]}
SCRIPTS["3716_non"] = {"Lutin": [[Drapeau(), Demander("Quel âge as-tu ?"),
                                  Si(Trou("", Non(Cmp(Reponse(), "<", 18))), [Dire("Tu es majeur.")],
                                     sinon=[Dire("Tu es mineur.")])]]}
SCRIPTS["3716_senior"] = {"Lutin": [[Drapeau(), Demander("Quel âge as-tu ?"),
                                     Si(Cmp(Reponse(), ">", 17),
                                        [Si(Cmp(Reponse(), ">", 64), [Dire("Tarif senior")],
                                            sinon=[Dire("Tu es majeur.")], hl=True)],
                                        sinon=[Dire("Tu es mineur.")])]]}

# 3717 : un triangle tracé avec « aller à »
SCRIPTS["3717"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(-100, 0), StyloBas(),
                              AllerA(0, 100), AllerA(100, 0), AllerA(-100, 0), StyloHaut()]]}

# 3718 : répéter jusqu'à (doublements)
SCRIPTS["3718"] = {"Lutin": [[Drapeau(), Mettre("n", 1), Mettre("étapes", 0),
                              JusquA(Cmp(V("n"), ">", 100), [Mettre("n", Op(V("n"), "*", 2)), Ajouter("étapes", 1)]),
                              Dire(V("n"), 2)]]}
SCRIPTS["3718_1000"] = {"Lutin": [[Drapeau(), Mettre("n", 1), Mettre("étapes", 0),
                                   JusquA(Cmp(V("n"), ">", 1000), [Mettre("n", Op(V("n"), "*", 2)), Ajouter("étapes", 1)]),
                                   Dire(V("n"), 2)]]}
SCRIPTS["3718_oubli"] = {"Lutin": [[Drapeau(), Mettre("n", 1), Mettre("étapes", 0),
                                    JusquA(Cmp(V("n"), ">", 100), [Ajouter("étapes", 1)]), Dire(V("n"), 2)]]}

# 3719 : orientation et déplacements
SCRIPTS["3719"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(0), StyloBas(),
                              Avancer(80), TournerD(90), Avancer(60), Orienter(180), Avancer(40),
                              TournerD(90), Avancer(20)]]}
SCRIPTS["3719_tourner"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(0), StyloBas(),
                                      Avancer(80), TournerD(90), Avancer(60), TournerD(90, hl=True), Avancer(40),
                                      TournerD(90), Avancer(20)]]}


# 3720 : bloc personnalisé « polygone »
def def_polygone():
    return [Definir("polygone", ["n", "côté"]),
            Repeter(Param("n"), [Avancer(Param("côté")), TournerG(Op(360, "/", Param("n")))])]


def main_polygone(n, c):
    return [Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(), Appel("polygone", [n, c])]


SCRIPTS["3720"] = {"Lutin": [def_polygone(), main_polygone(5, 80)]}
SCRIPTS["3720_6"] = {"Lutin": [def_polygone(), main_polygone(6, 70)]}
SCRIPTS["3720_8"] = {"Lutin": [def_polygone(), main_polygone(8, 55)]}
SCRIPTS["3720_36"] = {"Lutin": [def_polygone(), main_polygone(36, 10)]}

# 3721 : étoile à cinq branches
SCRIPTS["3721"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(-75, 20), Orienter(90), StyloBas(),
                              Repeter(5, [Avancer(150), TournerD(144)])]]}
SCRIPTS["3721_72"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(-75, 20), Orienter(90), StyloBas(),
                                 Repeter(5, [Avancer(150), TournerD(72)])]]}

# 3722 : frise de carrés (boucles imbriquées)
SCRIPTS["3722"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(-200, 0), Orienter(90),
                              Repeter(6, [StyloBas(), Repeter(4, [Avancer(30), TournerG(90)]),
                                          StyloHaut(), Avancer(60)])]]}
SCRIPTS["3722_sans_relever"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(-200, 0), Orienter(90),
                                           Repeter(6, [StyloBas(), Repeter(4, [Avancer(30), TournerG(90)]),
                                                       Avancer(60)])]]}

# 3723 : deux programmes de calcul
SCRIPTS["3723_A"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("x", Reponse()),
                                Mettre("r", Op(Op(V("x"), "+", 3), "*", 2)), Dire(V("r"), 2)]]}
SCRIPTS["3723_B"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("x", Reponse()),
                                Mettre("r", Op(Op(2, "*", V("x")), "+", 6)), Dire(V("r"), 2)]]}
SCRIPTS["3723_C"] = {"Lutin": [[Drapeau(), Demander("Choisis un nombre"), Mettre("x", Reponse()),
                                Mettre("r", Op(Op(V("x"), "*", V("x")), "+", 6)), Dire(V("r"), 2)]]}

# 3724 : piloter le lutin au clavier (événements)
SCRIPTS["3724"] = {"Lutin": [
    [Drapeau(), EffacerTout(), AllerA(0, 0), StyloBas()],
    [ToucheHat("flèche droite"), AjouterX(20)],
    [ToucheHat("flèche haut"), AjouterY(20)],
    [ToucheHat("flèche gauche"), AjouterX(-20)],
    [ToucheHat("espace"), StyloHaut()]]}
SCRIPTS["3724_bas"] = {"Lutin": [[ToucheHat("flèche bas"), AjouterY(-20, hl=True)]]}

# 3725 : déboguer un script de tracé
SCRIPTS["3725"] = {"Lutin": [[Drapeau(), AllerA(0, 0), Orienter(90),
                              Repeter(4, [Avancer(100), TournerD(60)])]]}
SCRIPTS["3725_stylo"] = {"Lutin": [[Drapeau(), AllerA(0, 0), Orienter(90), StyloBas(),
                                    Repeter(4, [Avancer(100), TournerD(60)])]]}
SCRIPTS["3725_corrige"] = {"Lutin": [[Drapeau(), EffacerTout(hl=True), AllerA(0, 0), Orienter(90), StyloBas(hl=True),
                                      Repeter(Trou("", 3), [Avancer(100), TournerD(Trou("", 120))])]]}

# 3726 : des lutins qui se parlent (messages)
SCRIPTS["3726"] = {
    "Chat": [[Drapeau(), Dire("Bonjour !", 2), Envoyer("à toi")],
             [Recoit("fin"), Dire("Au revoir !", 2)]],
    "Chien": [[Recoit("à toi"), Dire("Salut !", 2), Envoyer("fin")]]}

# 3727 : le nombre mystère
SCRIPTS["3727"] = {"Lutin": [[
    Drapeau(), Mettre("mystère", Alea(1, 100)), Mettre("essais", 0),
    JusquA(Cmp(Reponse(), "=", V("mystère")), [
        Demander("Propose un nombre"), Ajouter("essais", 1),
        Si(Cmp(Reponse(), "<", V("mystère")), [Dire("Trop petit !", 1)]),
        Si(Cmp(Reponse(), ">", V("mystère")), [Dire("Trop grand !", 1)])]),
    Dire("Gagné !", 2)]]}

# 3728 : la spirale
SCRIPTS["3728"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), Mettre("longueur", 10),
                              StyloBas(), Repeter(10, [Avancer(V("longueur")), TournerG(90), Ajouter("longueur", 10)])]]}


# 3729 : rendre la monnaie
def s3729(billets=False):
    debut = [Drapeau(), Demander("Somme à rendre ?"), Mettre("reste", Reponse())]
    if billets:
        debut += [Mettre("billets5", 0, hl=True),
                  JusquA(Cmp(V("reste"), "<", 5), [Ajouter("reste", -5), Ajouter("billets5", 1)], hl=True)]
    suite = [Mettre("pièces2", 0),
             JusquA(Cmp(V("reste"), "<", 2), [Ajouter("reste", -2), Ajouter("pièces2", 1)]),
             Mettre("pièces1", V("reste"))]
    fin = ([Dire(V("billets5"), 2, hl=True)] if billets else []) + [Dire(V("pièces2"), 2), Dire(V("pièces1"), 2)]
    return {"Lutin": [debut + suite + fin]}


SCRIPTS["3729"] = s3729()
SCRIPTS["3729_billets"] = s3729(billets=True)

# 3730 : convertir des températures
SCRIPTS["3730"] = {"Lutin": [[Drapeau(), Demander("Température en °C ?"), Mettre("C", Reponse()),
                              Mettre("F", Op(V("C"), "*", 1.8)), Ajouter("F", 32), Dire(V("F"), 2)]]}
SCRIPTS["3730_inverse"] = {"Lutin": [[Drapeau(), Demander("Température en °F ?", hl=True), Mettre("F", Reponse(), hl=True),
                                      Mettre("C", Op(V("F"), "-", 32), hl=True), Mettre("C", Op(V("C"), "/", 1.8), hl=True),
                                      Dire(V("C"), 2, hl=True)]]}

# 3731 : le robot du jardin
SCRIPTS["3731"] = {"Lutin": [[Drapeau(), EffacerTout(), AllerA(0, 0), StyloBas(),
                              Repeter(3, [AjouterX(40), AjouterY(30)]), Repeter(2, [AjouterX(-60)])]]}

# 3732 : des carrés emboîtés (type brevet)
DEF_CARRE = [Definir("carré", ["côté"]), Repeter(4, [Avancer(Param("côté")), TournerG(90)])]


def s3732(n=4, depart=(0, 0), grandit=True, cote_a_cote=False, hl=False):
    corps = [Appel("carré", [V("longueur")])]
    if cote_a_cote:
        corps += [StyloHaut(), Avancer(Op(V("longueur"), "+", 10)), StyloBas()]
    if grandit:
        corps.append(Ajouter("longueur", 30))
    return {"Lutin": [DEF_CARRE, [Drapeau(), EffacerTout(), AllerA(depart[0], depart[1], hl=hl), Orienter(90),
                                  StyloBas(), Mettre("longueur", 20), Repeter(n, corps, hl=hl)]]}


SCRIPTS["3732"] = s3732()
SCRIPTS["3732_A"] = s3732(grandit=False, cote_a_cote=True)
SCRIPTS["3732_C"] = s3732(cote_a_cote=True)
SCRIPTS["3732_7"] = s3732(n=7)
SCRIPTS["3732_7_scene"] = s3732(n=7, depart=(-200, -170), hl=True)

# 3733 : un programme de calcul à deux lutins (type brevet)
SCRIPTS["3733"] = {
    "Chat": [[Drapeau(), Demander("Choisis un nombre"), Mettre("x", Reponse()), Mettre("r", Op(V("x"), "+", 4)),
              Envoyer("calcule", attendre=True), Dire(V("r"))]],
    "Chien": [[Recoit("calcule"), Mettre("r", Op(V("r"), "*", V("x"))),
               Mettre("r", Op(V("r"), "-", Op(V("x"), "*", V("x"))))]]}
SCRIPTS["3733_simple"] = {"Chat": [[Drapeau(), Demander("Choisis un nombre"), Mettre("x", Reponse()),
                                    Mettre("r", Op(4, "*", V("x")), hl=True), Dire(V("r"))]]}


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


BLOC_PRINCIPAL = {("Lutin", 0): "Bloc personnalisé", ("Lutin", 1): "Script principal"}

# ======================================================================== figures de scripts
# cours
scripts_fig("cours_calcul", piles("cours_calcul"))
scripts_fig("cours_si", piles("cours_si"))
scripts_fig("cours_repeter", piles("cours_repeter"))
scripts_fig("cours_jusqua", piles("cours_jusqua"))
scripts_fig("cours_carre", piles("cours_carre"))
scripts_fig("cours_bloc", piles("cours_bloc", BLOC_PRINCIPAL))
scripts_fig("cours_touches", piles("cours_touches", {("Lutin", 0): "Script 1", ("Lutin", 1): "Script 2"}))
scripts_fig("cours_messages", piles("cours_messages", {("Chat", 0): "Lutin Chat", ("Chien", 0): "Lutin Chien"}))

# exercices
scripts_fig("ex3713_script", piles("3713"))
scripts_fig("ex3714_script", piles("3714"))
scripts_fig("ex3714_ajouter", piles("3714_ajouter"), corrige=True)
scripts_fig("ex3715_script", piles("3715"))
scripts_fig("ex3715_10", piles("3715_10"), corrige=True)
scripts_fig("ex3716_script", piles("3716"))
scripts_fig("ex3716_non", piles("3716_non"), corrige=True)
scripts_fig("ex3716_senior", piles("3716_senior"), corrige=True)
scripts_fig("ex3717_script", piles("3717"))
scripts_fig("ex3718_script", piles("3718"))
scripts_fig("ex3719_script", piles("3719"))
scripts_fig("ex3720_scripts", piles("3720", BLOC_PRINCIPAL))
scripts_fig("ex3721_script", piles("3721"))
scripts_fig("ex3722_script", piles("3722"))
scripts_fig("ex3723_scripts", [("Programme A", SCRIPTS["3723_A"]["Lutin"][0]),
                               ("Programme B", SCRIPTS["3723_B"]["Lutin"][0])])
scripts_fig("ex3724_scripts", piles("3724", {("Lutin", k): "Script %d" % (k + 1) for k in range(5)}), ecart=12.0)
scripts_fig("ex3724_bas", [("Script 6", SCRIPTS["3724_bas"]["Lutin"][0])], corrige=True)
scripts_fig("ex3725_script", piles("3725"))
scripts_fig("ex3725_corrige", piles("3725_corrige"), corrige=True)
scripts_fig("ex3726_scripts", [("Lutin Chat : script 1", SCRIPTS["3726"]["Chat"][0]),
                               ("Lutin Chien", SCRIPTS["3726"]["Chien"][0]),
                               ("Lutin Chat : script 2", SCRIPTS["3726"]["Chat"][1])])
scripts_fig("ex3727_script", piles("3727"))
scripts_fig("ex3728_script", piles("3728"))
scripts_fig("ex3729_script", piles("3729"))
scripts_fig("ex3729_billets", piles("3729_billets"), corrige=True)
scripts_fig("ex3730_script", piles("3730"))
scripts_fig("ex3730_inverse", piles("3730_inverse"), corrige=True)
scripts_fig("ex3731_script", piles("3731"))
scripts_fig("ex3732_scripts", piles("3732", BLOC_PRINCIPAL))
scripts_fig("ex3732_scene_script", [("Script principal modifié", SCRIPTS["3732_7_scene"]["Lutin"][1])], corrige=True)
scripts_fig("ex3733_scripts", piles("3733", {("Chat", 0): "Lutin Chat", ("Chien", 0): "Lutin Chien"}))
scripts_fig("ex3733_simple", [("Lutin Chat, en un seul calcul", SCRIPTS["3733_simple"]["Chat"][0])], corrige=True)


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
def figure_scene(contenu=None, u=.0155, rose=True):
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
    if contenu is None:
        s.append(txt % ("south west", P(-226, -166), C(-240, -180)))
    s.append(txt % ("north west", P(-226, 166), C(-240, 180)))
    s.append(txt % ("south east", P(226, -166), C(240, -180)))
    if contenu is None:
        s.append(r"\fill[otNavy] %s circle (2.2pt);" % P(0, 0))
        s.append(txt % ("north west", P(10, -10), "centre " + C(0, 0)))
    else:
        s += contenu(P)
    if rose:
        L = .78
        cx, cy = 0.0, -180 * u - 2.05
        s.append(r"\node[font=\otMedium\bfseries\fontsize{9}{10}\selectfont,text=otNavy,anchor=south] at (%s,%s) {Orientation du lutin};"
                 % (_n(cx), _n(cy + L + .5)))
        for ang, t, anc in ((0, "0", "south"), (90, "90", "west"), (180, "180", "north"), (-90, "−90", "east")):
            a = math.radians(ang)
            tx, ty = cx + L * math.sin(a), cy + L * math.cos(a)
            s.append(r"\draw[otNavy,line width=.9pt,-{Stealth[length=2.2mm]}] (%s,%s) -- (%s,%s);" % (_n(cx), _n(cy), _n(tx), _n(ty)))
            s.append(r"\node[anchor=%s,inner sep=2pt,font=\otMedium\fontsize{9}{10}\selectfont,text=otInk] at (%s,%s) {%s};"
                     % (anc, _n(tx), _n(ty), t))
        s.append(r"\fill[otOrange] (%s,%s) circle (2.6pt);" % (_n(cx), _n(cy)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_scene"] = figure_scene()

# --- cours : carré et bloc personnalisé
lu = trace("cours_carre")
FIGURES["cours_carre_trace"] = figure_trace(lu.segments, (-30, 100, -15, 80), 10, .062, depart=(0, 0), pas_lab=20,
                                            fleche=(lu.x, lu.y, lu.direction),
                                            points=[(60, 0, C(60, 0), "north west"), (60, 60, C(60, 60), "south west"),
                                                    (0, 60, C(0, 60), "south east")])
lu = trace("cours_bloc")
FIGURES["cours_bloc_trace"] = figure_trace(lu.segments, (-20, 100, -10, 90), 10, .06, depart=(0, 0), pas_lab=30)

# --- 3713
lu = trace("3713")
FIGURES["ex3713_trace"] = figure_trace(
    lu.segments, (-20, 140, -130, 30), 10, .045, depart=(0, 0), pas_lab=50, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 0, C(0, 0), "south west,yshift=2pt"), (100, 0, C(100, 0), "south east"),
            (100, -100, C(100, -100), "north east"), (0, -100, C(0, -100), "north west")])
lu2 = trace("3713_gauche")
FIGURES["ex3713_gauche"] = figure_trace(
    lu2.segments, (-70, 170, -130, 130), 10, .033, depart=(0, 0), pas_lab=50, fleche=(lu2.x, lu2.y, lu2.direction),
    autres=[(lu.segments, "otMuted,line width=1pt,dash pattern=on 3.5pt off 2.5pt")],
    points=[(100, 0, C(100, 0), "north west"), (100, 100, C(100, 100), "south west"), (0, 100, C(0, 100), "south east")])

# --- 3717
lu = trace("3717")
FIGURES["ex3717_trace"] = figure_trace(
    lu.segments, (-160, 160, -40, 140), 20, .025, depart=(-100, 0), pas_lab=50,
    points=[(-100, 0, r"$A$ " + C(-100, 0), "north"), (100, 0, r"$B$ " + C(100, 0), "north"),
            (0, 100, r"$C$ " + C(0, 100), "south west")])

# --- 3719
lu = trace("3719")
FIGURES["ex3719_trace"] = figure_trace(
    lu.segments, (-30, 100, -20, 110), 10, .06, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 0, C(0, 0), "north west"), (0, 80, C(0, 80), "south east"), (60, 80, C(60, 80), "south west"),
            (60, 40, C(60, 40), "north west"), (40, 40, C(40, 40), "north east,yshift=-2pt")])

# --- 3720 : pentagone, puis polygone à 36 côtés
lu = trace("3720")
FIGURES["ex3720_trace"] = figure_trace(
    lu.segments, (-50, 130, -20, 140), 10, .045, depart=(0, 0), pas_lab=50, fleche=(lu.x, lu.y, lu.direction),
    points=[(80, 0, C(80, 0), "north")])
lu = trace("3720_36")
FIGURES["ex3720_36"] = figure_trace(
    lu.segments, (-70, 70, -20, 130), 10, .045, depart=(0, 0), pas_lab=50)

# --- 3721 : étoile
lu = trace("3721")
FIGURES["ex3721_trace"] = figure_trace(
    lu.segments, (-100, 100, -100, 100), 10, .04, depart=(-75, 20), pas_lab=50, fleche=(lu.x, lu.y, lu.direction))

# --- 3722 : frise de carrés
lu = trace("3722")
FIGURES["ex3722_trace"] = figure_trace(
    lu.segments, (-220, 180, -30, 50), 10, .021, depart=(-200, 0), pas_lab=100, grille=False,
    fleche=(lu.x, lu.y, lu.direction),
    points=[(-200, 0, C(-200, 0), "north west"), (160, 0, C(160, 0), "north east")])

# --- 3724 : trajet au clavier
r = executer(SCRIPTS["3724"], touches=["flèche droite"] * 2 + ["flèche haut"] * 2 + ["flèche gauche"])
lu = r.lutins["lutin"]
FIGURES["ex3724_trace"] = ajoute(figure_trace(
    lu.segments, (-20, 80, -20, 60), 10, .075, depart=(0, 0), pas_lab=20, fleche=None,
    points=[(0, 0, C(0, 0), "north west"), (40, 0, C(40, 0), "north west"), (40, 40, C(40, 40), "south west"),
            (20, 40, C(20, 40), "south east")]), points_verts([(20, 0), (40, 20)], .075))
r = executer(SCRIPTS["3724"], touches=["flèche droite", "espace", "flèche haut", "flèche droite"])
lu = r.lutins["lutin"]
pos = lu.positions[1:]
FIGURES["ex3724_espace"] = ajoute(figure_trace(
    lu.segments, (-20, 80, -20, 50), 10, .075, depart=(0, 0), pas_lab=20,
    autres=[(list(zip(pos[1:-1], pos[2:])), "otMuted,line width=1.1pt,dash pattern=on 3pt off 2pt")],
    points=[(20, 0, C(20, 0), "north west"), (40, 20, C(40, 20), "south west")]),
    [r"\fill[otMuted] (%s,%s) circle (1.9pt);" % (_n(x * .075), _n(y * .075)) for (x, y) in ((20, 20), (40, 20))])

# --- 3725 : la ligne brisée, puis le triangle
lu = trace("3725_stylo")
FIGURES["ex3725_trace"] = figure_trace(
    lu.segments, (-30, 180, -200, 30), 10, .037, depart=(0, 0), pas_lab=50, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 0, C(0, 0), "south west")])
lu = trace("3725_corrige")
FIGURES["ex3725_triangle"] = figure_trace(
    lu.segments, (-30, 130, -110, 30), 10, .048, depart=(0, 0), pas_lab=50, fleche=(lu.x, lu.y, lu.direction),
    points=[(0, 0, C(0, 0), "south west,yshift=2pt"), (100, 0, C(100, 0), "south east")])

# --- 3728 : spirale
lu = trace("3728")
FIGURES["ex3728_trace"] = ajoute(figure_trace(
    lu.segments, (-60, 70, -60, 80), 10, .055, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(10, 0, "1", "south west"), (10, 20, "2", "south west"), (-20, 20, "3", "south east"),
            (-20, -20, "4", "north east"), (50, 60, C(50, 60), "south east")]),
    points_verts([(10, 0), (10, 20), (-20, 20), (-20, -20)], .055))

# --- 3731 : robot
lu = trace("3731")
FIGURES["ex3731_trace"] = ajoute(figure_trace(
    lu.segments, (-20, 140, -20, 110), 10, .05, depart=(0, 0), pas_lab=20,
    autres=[([((0, 0), (120, 90))], "otOrange,line width=1.1pt,dash pattern=on 4pt off 2.5pt")],
    points=[(0, 0, r"$O$", "north east"), (40, 30, C(40, 30), "north west"), (120, 90, r"$A$ " + C(120, 90), "south east"),
            (0, 90, r"$B$ " + C(0, 90), "south west")]), points_verts([(40, 30), (120, 90), (0, 90)], .05))


# --- 3732 : dessins candidats, tracé, figure sur la scène
def figure_dessins(dessins, u=.022):
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


FIGURES["ex3732_dessins"] = figure_dessins([("Dessin A", trace("3732_A").segments),
                                            ("Dessin B", trace("3732").segments),
                                            ("Dessin C", trace("3732_C").segments)])
lu = trace("3732")
FIGURES["ex3732_trace"] = figure_trace(
    lu.segments, (-20, 130, -20, 130), 10, .05, depart=(0, 0), pas_lab=20, fleche=(lu.x, lu.y, lu.direction),
    points=[(20, 0, "20", "north"), (50, 0, "50", "north"), (80, 0, "80", "north"), (110, 0, "110", "north")])
lu = trace("3732_7_scene")


def contenu_scene(P):
    out = [r"\draw[otGreenDark,line width=1.4pt] %s;" % " -- ".join(P(*p) for p in [a] + b)
           for a, b in _fusion_segs(lu.segments)]
    out.append(r"\fill[otNavy] %s circle (2.2pt);" % P(-200, -170))
    out.append(r"\node[anchor=south west,inner sep=1.5pt,font=\otMedium\fontsize{8.5}{10}\selectfont,text=otGreenDark] at %s {%s};"
               % (P(4, 32), C(0, 30)))
    return out


def _fusion_segs(segments):
    out = []
    for a, b in segments:
        if out and out[-1][1][-1] == a:
            out[-1][1].append(b)
        else:
            out.append((a, [b]))
    return out


FIGURES["ex3732_scene"] = figure_scene(contenu_scene, rose=False)
