# -*- coding: utf-8 -*-
"""Figures de la notion 261 (5e : opérations et priorités), style des livres OptiTAB.

Compilées par outils/figures_livre.py. Arbres de calcul (valeurs calculées ici en
fractions exactes : la figure ne peut pas contredire le texte), schéma des
priorités, modèles d'aire de la distributivité, divisions posées, schémas en
barres des problèmes, écrans de calculatrice, bouteilles.
Énoncé : arbre vide ou partiel ; corrigé : valeurs en vert foncé (otGreenDark).
"""
from fractions import Fraction

PREAMBULE_EXTRA = r"""
\tikzset{
  feuille/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=2pt,
    minimum width=.95cm,minimum height=.6cm,inner sep=2pt,text=otInk},
  operation/.style={circle,draw=otNavy,fill=white,line width=.8pt,minimum size=.56cm,inner sep=0pt,text=otNavy},
  resVide/.style={draw=otMuted,dash pattern=on 2.5pt off 1.8pt,line width=.6pt,rounded corners=2pt,
    minimum width=1.05cm,minimum height=.6cm,inner sep=2pt},
  resVert/.style={draw=otGreenDark,line width=.9pt,rounded corners=2pt,fill=otGreen!10,
    minimum width=1.05cm,minimum height=.6cm,inner sep=2pt,text=otGreenDark},
  resDonne/.style={draw=otNavy,line width=.8pt,rounded corners=2pt,fill=white,
    minimum width=1.05cm,minimum height=.6cm,inner sep=2pt,text=otInk},
  branche/.style={otNavy!70,line width=.75pt},
  boite/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=3pt,
    minimum width=5.4cm,minimum height=.8cm,inner sep=3pt,text=otInk,align=center},
  fleche/.style={otMuted,line width=.8pt,-{Stealth[length=2.2mm]}},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont},
  accol/.style={otMuted,line width=.6pt,decorate,decoration={brace,amplitude=5pt}},
  accolV/.style={otGreenDark,line width=.8pt,decorate,decoration={brace,amplitude=5pt}},
  seg/.style={draw=otNavy,line width=.8pt},
  ecran/.style={draw=otNavy,line width=.9pt,rounded corners=4pt,fill=otSky,
    minimum width=6.4cm,minimum height=1.45cm},
  chiffre/.style={anchor=base,inner sep=0pt,text=otInk},
}
"""

VERT = "otGreenDark"
FIGURES = {}


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def fr(q):
    """Fraction décimale -> écriture LaTeX française (virgule, espace des milliers)."""
    q = Fraction(q)
    neg = q < 0
    q = abs(q)
    k = 0
    while (q * 10 ** k).denominator != 1:
        k += 1
        assert k < 8, "nombre non décimal"
    entier = int(q)
    dec = q - entier
    s_ent = str(entier)
    if len(s_ent) > 3:
        groupes = []
        while s_ent:
            groupes.insert(0, s_ent[-3:])
            s_ent = s_ent[:-3]
        s_ent = r"\,".join(groupes)
    s = s_ent
    if k:
        s += "{,}" + str(int(dec * 10 ** k)).rjust(k, "0")
    return ("-" if neg else "") + s


def num(s):
    return Fraction(s.replace(",", "."))


# ===================================================================== arbres de calcul
SYMB = {"+": "+", "-": "-", "*": r"\times", "/": r"\div"}


def evalue(e):
    if isinstance(e, str):
        return num(e)
    op, a, b = e
    a, b = evalue(a), evalue(b)
    return {"+": a + b, "-": a - b, "*": a * b, "/": a / b}[op]


def arbre(expr, mode="corrige", montres=(), sep=1.4, dy=1.75, x0=0.0, pref="n"):
    """Arbre de calcul : nombres en bas, chaque opération dans un cercle, son résultat
    dans la case au-dessus. mode : "enonce" (cases vides, sauf les nœuds de `montres`,
    numérotés dans l'ordre de calcul) ou "corrige" (toutes les valeurs en vert)."""
    feuilles = []
    noeuds = []

    def place(e):
        if isinstance(e, str):
            n = {"feuille": True, "txt": e, "x": x0 + len(feuilles) * sep, "niv": 0}
            n["nom"] = "%sF%d" % (pref, len(feuilles))
            feuilles.append(n)
            return n
        op, a, b = e
        na, nb_ = place(a), place(b)
        n = {"feuille": False, "op": op, "enfants": (na, nb_), "x": (na["x"] + nb_["x"]) / 2,
             "niv": max(na["niv"], nb_["niv"]) + 1, "val": evalue(e)}
        n["nom"] = "%sN%d" % (pref, len(noeuds))
        n["rang"] = len(noeuds)
        noeuds.append(n)
        return n

    racine = place(expr)
    s = []
    for n in feuilles:
        s.append(r"\node[feuille] (%s) at (%s,0) {$%s$};" % (n["nom"], f(n["x"]), n["txt"].replace(",", "{,}")))
    for n in noeuds:
        yr = n["niv"] * dy
        yo = yr - .78
        s.append(r"\node[operation] (%sO) at (%s,%s) {$%s$};" % (n["nom"], f(n["x"]), f(yo), SYMB[n["op"]]))
        if mode == "corrige":
            style, txt = "resVert", "$%s$" % fr(n["val"])
        elif n["rang"] in montres:
            style, txt = "resDonne", "$%s$" % fr(n["val"])
        else:
            style, txt = "resVide", ""
        s.append(r"\node[%s] (%s) at (%s,%s) {%s};" % (style, n["nom"], f(n["x"]), f(yr), txt))
        s.append(r"\draw[branche] (%sO) -- (%s);" % (n["nom"], n["nom"]))
        for c in n["enfants"]:
            s.append(r"\draw[branche] (%s.north) -- (%sO);" % (c["nom"], n["nom"]))
    return "\n".join(s), racine, feuilles


def fig_arbre(expr, mode="corrige", montres=(), titre=None, **kw):
    code, racine, feuilles = arbre(expr, mode, montres, **kw)
    s = [r"\begin{tikzpicture}", code]
    if titre:
        s.append(r"\node[anchor=south,text=otNavy] at (%s,%s) {%s};"
                 % (f((feuilles[0]["x"] + feuilles[-1]["x"]) / 2), f(racine["niv"] * kw.get("dy", 1.75) + .5), titre))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


# Cours : 2 × (9 − 4) + 6
COURS_ARBRE = ("+", ("*", "2", ("-", "9", "4")), "6")
FIGURES["cours_arbre"] = fig_arbre(COURS_ARBRE, "corrige")

# 2709 : E = 7 × 8 − 6 × 9 + 4
E_2709 = ("+", ("-", ("*", "7", "8"), ("*", "6", "9")), "4")
FIGURES["ex_ordre_arbre_enonce"] = fig_arbre(E_2709, "enonce")
FIGURES["ex_ordre_arbre_corrige"] = fig_arbre(E_2709, "corrige")

# 2710 : (20 − 2 × 3) ÷ 7
A_2710 = ("/", ("-", "20", ("*", "2", "3")), "7")
FIGURES["ex_parentheses_arbre_enonce"] = fig_arbre(A_2710, "enonce")
FIGURES["ex_parentheses_arbre_corrige"] = fig_arbre(A_2710, "corrige")


# 2716 : 8 + 2 × 5 et (8 + 2) × 5, côte à côte
def deux_arbres():
    c1, r1, f1 = arbre(("+", "8", ("*", "2", "5")), "corrige", sep=1.15, pref="a")
    c2, r2, f2 = arbre(("*", ("+", "8", "2"), "5"), "corrige", x0=3.6, sep=1.15, pref="b")
    s = [r"\begin{tikzpicture}", c1, c2]
    for fe, r, t, nat in ((f1, r1, r"$8 + 2 \times 5$", "une somme"), (f2, r2, r"$(8 + 2) \times 5$", "un produit")):
        xm = (fe[0]["x"] + fe[-1]["x"]) / 2
        s.append(r"\node[anchor=south,text=otNavy] at (%s,%s) {%s};" % (f(xm), f(2 * 1.75 + .5), t))
        s.append(r"\node[anchor=north,text=%s] at (%s,-.55) {c'est %s};" % (VERT, f(xm), nat))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_vocabulaire_arbres_corrige"] = deux_arbres()

# 2724 : 4 × 6 × 1,75 − 3 + 5 (énoncé : la première case est donnée)
F_2724 = ("+", ("-", ("*", ("*", "4", "6"), "1,75"), "3"), "5")
FIGURES["ex_facture_arbre_enonce"] = fig_arbre(F_2724, "enonce", montres=(0,), sep=1.3, dy=1.6)
FIGURES["ex_facture_arbre_corrige"] = fig_arbre(F_2724, "corrige", sep=1.3, dy=1.6)


# ===================================================================== schéma des priorités
def priorites():
    lignes = [(r"\textbf{1.} Parenthèses, crochets", "les plus intérieurs d'abord"),
              (r"\textbf{2.} Multiplications, divisions", "de gauche à droite"),
              (r"\textbf{3.} Additions, soustractions", "de gauche à droite")]
    s = [r"\begin{tikzpicture}"]
    for k, (a, b) in enumerate(lignes):
        s.append(r"\node[boite] (p%d) at (0,%s) {%s\\[-1pt]{\otRegular\fontsize{9.5}{11}\selectfont %s}};" % (k, f(-k * 1.3), a, b))
        if k:
            s.append(r"\draw[fleche] (p%d.south) -- (p%d.north);" % (k - 1, k))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["priorites"] = priorites()


# ===================================================================== modèle d'aire (distributivité)
def aire(k, a, b, corrige, w1=3.5, w2=2.3, h=1.7):
    s = [r"\begin{tikzpicture}"]
    s.append(r"\fill[otSky] (0,0) rectangle (%s,%s);" % (f(w1), f(h)))
    s.append(r"\fill[otOrange!14] (%s,0) rectangle (%s,%s);" % (f(w1), f(w1 + w2), f(h)))
    s.append(r"\draw[seg] (0,0) rectangle (%s,%s);" % (f(w1 + w2), f(h)))
    s.append(r"\draw[seg] (%s,0) -- (%s,%s);" % (f(w1), f(w1), f(h)))
    # longueurs : accolades au-dessus, largeur à gauche
    s.append(r"\draw[accol] (.05,%s) -- (%s,%s) node[midway,above=5pt,text=otInk] {$%s$};" % (f(h + .12), f(w1 - .05), f(h + .12), a))
    s.append(r"\draw[accol] (%s,%s) -- (%s,%s) node[midway,above=5pt,text=otInk] {$%s$};" % (f(w1 + .05), f(h + .12), f(w1 + w2 - .05), f(h + .12), b))
    s.append(r"\draw[accol] (-.12,.05) -- (-.12,%s) node[midway,left=6pt,text=otInk] {$%s$};" % (f(h - .05), k))
    va, vb = num(k) * num(a), num(k) * num(b)
    if corrige:
        s.append(r"\node[text=%s,align=center] at (%s,%s) {$%s \times %s$\\$= %s$};" % (VERT, f(w1 / 2), f(h / 2), k, a, fr(va)))
        s.append(r"\node[text=%s,align=center] at (%s,%s) {$%s \times %s$\\$= %s$};" % (VERT, f(w1 + w2 / 2), f(h / 2), k, b, fr(vb)))
        s.append(r"\node[anchor=north,text=%s] at (%s,-.18) {aire totale : $%s + %s = %s$};" % (VERT, f((w1 + w2) / 2), fr(va), fr(vb), fr(va + vb)))
    else:
        s.append(r"\node[text=otMuted] at (%s,%s) {aire $?$};" % (f(w1 / 2), f(h / 2)))
        s.append(r"\node[text=otMuted] at (%s,%s) {aire $?$};" % (f(w1 + w2 / 2), f(h / 2)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_aire"] = aire("7", "100", "2", True)
FIGURES["ex_mental_aire_enonce"] = aire("8", "100", "5", False)
FIGURES["ex_mental_aire_corrige"] = aire("8", "100", "5", True)


# ===================================================================== divisions posées
CW, RH = .31, .62


def rangee(txt, col_fin, ligne, coul="otInk"):
    """Écrit txt (chiffres et virgule) en finissant à la colonne col_fin, sur la ligne donnée."""
    s = []
    col = col_fin
    y = -ligne * RH
    for ch in reversed(txt):
        if ch == ",":
            s.append(r"\node[chiffre,text=%s] at (%s,%s) {,};" % (coul, f((col + .5) * CW), f(y)))
            continue
        s.append(r"\node[chiffre,text=%s] at (%s,%s) {$%s$};" % (coul, f(col * CW), f(y), ch))
        col -= 1
    return s, col + 1


def division(dividende, ncol, diviseur, quotient, soustr, corrige=True):
    """soustr : liste de (texte, col_fin, est_soustraction). Lignes successives sous le dividende."""
    qc = VERT if corrige else "otInk"
    s = [r"\begin{tikzpicture}"]
    r, _ = rangee(dividende, ncol - 1, 0)
    s += r
    for i, (txt, cf, moins) in enumerate(soustr, start=1):
        r, c0 = rangee(txt, cf, i)
        s += r
        if moins:
            y = -i * RH
            s.append(r"\node[chiffre,text=otInk] at (%s,%s) {$-$};" % (f((c0 - 1) * CW), f(y)))
            s.append(r"\draw[otMuted,line width=.6pt] (%s,%s) -- (%s,%s);" % (f((c0 - 1.5) * CW), f(y - .17), f((cf + .5) * CW), f(y - .17)))
    xb = (ncol - .5) * CW + .12
    nb_lignes = len(soustr)
    s.append(r"\draw[otNavy,line width=.9pt] (%s,.4) -- (%s,%s);" % (f(xb), f(xb), f(-nb_lignes * RH - .2)))
    s.append(r"\draw[otNavy,line width=.9pt] (%s,-.2) -- (%s,-.2);" % (f(xb), f(xb + 1.75)))
    s.append(r"\node[anchor=base west,text=otInk,inner sep=0pt] at (%s,0) {$%s$};" % (f(xb + .22), diviseur))
    s.append(r"\node[anchor=base west,text=%s,inner sep=0pt] at (%s,%s) {$%s$};" % (qc, f(xb + .22), f(-RH), quotient.replace(",", "{,}")))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


# 75,6 ÷ 6 = 12,6 (cours)
FIGURES["cours_division"] = division("75,6", 3, "6", "12,6",
                                     [("6", 0, True), ("15", 1, False), ("12", 1, True), ("36", 2, False), ("36", 2, True), ("0", 2, False)])
# 91,2 ÷ 24 = 3,8 (2706)
FIGURES["ex_division_corrige"] = division("91,2", 3, "24", "3,8",
                                          [("72", 1, True), ("192", 2, False), ("192", 2, True), ("0", 2, False)])


# ===================================================================== bouteilles (2706)
def bouteilles():
    s = [r"\begin{tikzpicture}"]
    L, H, dx = .42, 1.0, .63
    for i in range(10):
        x = i * dx
        niveau = H if i < 9 else H * .4
        s.append(r"\fill[otNavy!28] (%s,0) rectangle (%s,%s);" % (f(x), f(x + L), f(niveau)))
        pts = [(x, 0), (x, H), (x + .14, H + .2), (x + .14, H + .42), (x + L - .14, H + .42),
               (x + L - .14, H + .2), (x + L, H), (x + L, 0)]
        s.append(r"\draw[otNavy,line width=.75pt,line join=round] %s -- cycle;"
                 % " -- ".join("(%s,%s)" % (f(a), f(b)) for a, b in pts))
    s.append(r"\draw[accolV] (%s,-.12) -- (0,-.12);" % f(8 * dx + L))
    s.append(r"\node[anchor=north,text=%s,align=center] at (%s,-.45) {$9$ bouteilles pleines\\$9 \times 0{,}25 = 2{,}25$ L};" % (VERT, f((8 * dx + L) / 2)))
    xd = 9 * dx + L / 2
    s.append(r"\node[anchor=north,text=%s,align=center] at (%s,-.12) {$0{,}1$ L\\[-1pt]{\otRegular\fontsize{8.5}{10}\selectfont reste}};" % (VERT, f(xd)))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_bouteilles_corrige"] = bouteilles()


# ===================================================================== écrans de calculatrice (2714)
def ecran(nom, x, y, saisie, resultat, coul_res="otInk", titre=None, coul_titre="otNavy"):
    s = [r"\node[ecran] (%s) at (%s,%s) {};" % (nom, f(x), f(y))]
    s.append(r"\node[anchor=north west,text=otInk,inner sep=0pt,font=\otMedium\fontsize{11}{13}\selectfont] at ($(%s.north west)+(.25,-.22)$) {%s};" % (nom, saisie))
    s.append(r"\node[anchor=south east,text=%s,inner sep=0pt,font=\otMedium\bfseries\fontsize{13}{15}\selectfont] at ($(%s.south east)+(-.25,.18)$) {%s};" % (coul_res, nom, resultat))
    if titre:
        s.append(r"\node[anchor=south west,text=%s,inner sep=0pt] at ($(%s.north west)+(0,.12)$) {%s};" % (coul_titre, nom, titre))
    return "\n".join(s)


FIGURES["ex_calculatrice_enonce"] = "\n".join([r"\begin{tikzpicture}",
                                               ecran("e1", 0, 0, r"36+24÷4+2", "44", titre="Saisie de Hugo"),
                                               r"\end{tikzpicture}"])
FIGURES["ex_calculatrice_corrige"] = "\n".join([r"\begin{tikzpicture}",
                                                ecran("e1", 0, 0, r"36+24÷4+2", "44", titre="Saisie de Hugo : $36 + 6 + 2$"),
                                                ecran("e2", 0, -2.35, r"(36+24)÷(4+2)", "10", coul_res=VERT,
                                                      titre=r"Bonne saisie : $60 \div 6$", coul_titre=VERT),
                                                r"\end{tikzpicture}"])


# ===================================================================== schémas en barres
def barre(segments, y=0.0, h=.8, x0=0.0):
    """segments : liste de (largeur, texte, remplissage, couleur du texte). Renvoie (code, x_fin)."""
    s = []
    x = x0
    for w, t, rem, ct in segments:
        s.append(r"\fill[%s] (%s,%s) rectangle (%s,%s);" % (rem, f(x), f(y), f(x + w), f(y + h)))
        s.append(r"\draw[seg] (%s,%s) rectangle (%s,%s);" % (f(x), f(y), f(x + w), f(y + h)))
        if t:
            s.append(r"\node[text=%s,align=center,inner sep=1pt] at (%s,%s) {%s};" % (ct, f(x + w / 2), f(y + h / 2), t))
        x += w
    return "\n".join(s), x


def cours_probleme():
    seg = [(.95, r"$9{,}50$", "otNavy!22", "otInk")] * 3 + [(.66, r"$6$", "otSky", "otInk")] * 4 + [(.66, r"$2$", "otOrange!30", "otInk")]
    code, xf = barre(seg)
    s = [r"\begin{tikzpicture}", code]
    s.append(r"\draw[accol] (0,.92) -- (2.85,.92) node[midway,above=6pt,text=otInk] {$3$ adultes};")
    s.append(r"\draw[accol] (2.85,.92) -- (5.49,.92) node[midway,above=6pt,text=otInk] {$4$ enfants};")
    s.append(r"\node[anchor=south,text=otInk,align=center] at (5.82,.92) {frais};")
    s.append(r"\draw[accolV] (%s,-.12) -- (0,-.12) node[midway,below=6pt,text=%s] {total : $54{,}50$ €};" % (f(xf), VERT))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["cours_probleme"] = cours_probleme()


def ateliers(corrige):
    s = [r"\begin{tikzpicture}"]
    # un atelier : 5 carnets + feutres
    # un atelier : 5 carnets + feutres (titre à gauche, au-dessus de la barre)
    code, xf = barre([(.55, "", "otNavy!30", "otInk")] * 3 + [(.55, "", "otGreen!35", "otInk")] * 2 + [(1.3, r"$4{,}60$", "otOrange!30", "otInk")], y=2.6, h=.7)
    s.append(code)
    s.append(r"\node[anchor=south west,text=otNavy,inner sep=0pt] at (0,4.4) {Un atelier};")
    s.append(r"\draw[accol] (0,3.42) -- (2.75,3.42) node[midway,above=6pt,text=otInk] {$5$ carnets à $2{,}50$ €};")
    s.append(r"\node[anchor=south,text=otInk] at (3.4,3.42) {feutres};")
    if corrige:
        s.append(r"\draw[accolV] (4.05,2.48) -- (0,2.48) node[midway,below=6pt,text=%s] {$(3 + 2) \times 2{,}50 + 4{,}60 = 17{,}10$ €};" % VERT)
    # la commande
    t = r"$17{,}10$" if corrige else "atelier"
    ct = VERT if corrige else "otInk"
    code, xf = barre([(1.32, t, "otSky", ct)] * 4 + [(.8, r"$6$", "otOrange!30", "otInk")], y=0, h=.8)
    s.append(code)
    s.append(r"\node[anchor=south west,text=otNavy,inner sep=0pt] at (0,.98) {La commande};")
    s.append(r"\node[anchor=south,text=otInk] at (5.68,.92) {livraison};")
    if corrige:
        s.append(r"\draw[accolV] (%s,-.12) -- (0,-.12) node[midway,below=6pt,text=%s] {$4 \times 17{,}10 + 6 = 74{,}40$ €};" % (f(xf), VERT))
    else:
        s.append(r"\draw[accol] (%s,-.12) -- (0,-.12) node[midway,below=6pt,text=otInk] {total : $?$};" % f(xf))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_ateliers_enonce"] = ateliers(False)
FIGURES["ex_ateliers_corrige"] = ateliers(True)


def sortie():
    k = 6.6 / 1903
    s = [r"\begin{tikzpicture}"]
    code, xf = barre([(420 * k, r"car\\$420$", "otOrange!30", "otInk"),
                      (950 * k, r"entrées\\$950$", "otSky", "otInk"),
                      (533 * k, r"repas\\$533$", "otNavy!22", "otInk")], y=2.1, h=1.1)
    s.append(code)
    s.append(r"\draw[accolV] (0,3.32) -- (%s,3.32) node[midway,above=6pt,text=%s] {coût total : $1\,903$ €};" % (f(xf), VERT))
    code, xf2 = barre([(725 * k, r"foyer\\$725$", "otOrange!14", "otInk"),
                       (1178 * k, r"part des élèves\\$1\,178$", "otGreen!14", VERT)], y=0, h=1.1)
    s.append(code)
    s.append(r"\draw[accolV] (%s,-.12) -- (%s,-.12) node[midway,below=6pt,text=%s] {$1\,178 \div 76 = 15{,}50$ € par élève};" % (f(xf2), f(725 * k), VERT))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


FIGURES["ex_sortie_corrige"] = sortie()
