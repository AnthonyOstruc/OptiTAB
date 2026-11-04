# -*- coding: utf-8 -*-
"""Figures de la notion 243 (3e : probabilités), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>

Moteurs repris des notions 2nde 175 (arbre de dénombrement, tableau à double
entrée) et 1ère 183 (arbre pondéré : « … » dans l'énoncé, valeurs vertes dans
le corrigé ; courbe de fréquences). Valeurs vérifiées par ../verif_243.py.
"""
import random
from fractions import Fraction as Fr

PREAMBULE_EXTRA = r"""
\tikzset{
  evt/.style={font=\normalsize, text=otNavy, inner sep=2.4pt},
  branche/.style={otNavy!65, line width=0.8pt, line cap=round},
  brancheV/.style={otGreenDark, line width=1.6pt, line cap=round},
  poids/.style={font=\small, text=otInk, inner sep=1.7pt},
  poidsV/.style={poids, text=otGreenDark},
  issue/.style={font=\small, text=otMuted, anchor=west, inner sep=1.5pt},
  issueV/.style={issue, text=otGreenDark},
  racine/.style={fill=otNavy},
  titreCol/.style={font=\otRegular\fontsize{8.5}{10}\selectfont, text=otMuted, anchor=south},
  grad/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt},
  legendeV/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otGreenDark, inner sep=1.5pt},
}
\pgfplotsset{otLoi/.style={
  axis lines=left,
  axis line style={otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}},
  tick style={otMuted,line width=0.5pt}, major tick length=3pt, tick align=outside,
  ticklabel style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  xticklabel style={yshift=-1pt},
  every axis x label/.style={at={(current axis.right of origin)},anchor=west,font=\normalsize,text=otMuted,xshift=2pt},
  every axis y label/.style={at={(current axis.north west)},anchor=south,font=\normalsize,text=otMuted,yshift=4pt},
  scale only axis, clip=false,
  /pgf/number format/use comma, /pgf/number format/1000 sep={\,},
}}
"""

FIGURES = {}


def frac(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else rf"\dfrac{{{x.numerator}}}{{{x.denominator}}}"


# ================================================================ arbres
def N(nom, p=None, *enfants, donne=True, vert=False, droite=None):
    """Nœud : nom (LaTeX), p = probabilité de la branche (Fraction) ou None
    (arbre de dénombrement) ; donne=False : « … » dans l'énoncé, vert au corrigé."""
    return {"nom": nom, "p": p, "enfants": list(enfants), "donne": donne,
            "vert": vert, "droite": droite}


def _vert(n):
    if not n["enfants"]:
        return n["vert"]
    n["vert"] = n["vert"] or any([_vert(c) for c in n["enfants"]])
    return n["vert"]


def _placer(n, prof, y, dy, ecarts, L):
    n["x"] = prof * L
    if not n["enfants"]:
        n["y"] = y
        return y - dy
    ys = []
    for k, c in enumerate(n["enfants"]):
        if k and c["enfants"]:
            y -= ecarts.get(prof + 1, 0)
        y = _placer(c, prof + 1, y, dy, ecarts, L)
        ys.append(c["y"])
    n["y"] = (ys[0] + ys[-1]) / 2
    return y


def _tous_y(n):
    ys = [n["y"]]
    for c in n["enfants"]:
        ys += _tous_y(c)
    return ys


def arbre(enfants, mode="corrige", L=2.2, dy=0.95, ecarts=None, titres=None, produits=True):
    """mode : "enonce" (poids inconnus « … », pas d'issues), "corrige" (poids
    trouvés et chemins favorables en vert, issues à droite)."""
    racine = {"nom": None, "p": None, "enfants": enfants, "droite": None, "vert": False, "donne": True}
    if mode == "corrige":
        _vert(racine)
    _placer(racine, 0, 0.0, dy, ecarts or {}, L)
    noeuds, aretes, poids, droites = [], [], [], []
    k = [0]

    def visiter(n, parent_ref, parent_y, prod):
        for c in n["enfants"]:
            k[0] += 1
            nom = f"n{k[0]}"
            v = mode == "corrige" and c["vert"]
            noeuds.append(rf"\node[{'evt,text=otGreenDark' if v else 'evt'}] ({nom}) at ({c['x']:.3f},{c['y']:.3f}) {{${c['nom']}$}};")
            st = "brancheV" if v else "branche"
            aretes.append((st, rf"\draw[{st}] {parent_ref} -- ({nom}.west);"))
            pr = None
            if c["p"] is not None:
                ecart = c["y"] - parent_y
                anc = "south east" if ecart > 1e-6 else ("north east" if ecart < -1e-6 else "south")
                if mode == "enonce" and not c["donne"]:
                    t, sp = r"\ldots", "poids"
                else:
                    t = frac(c["p"])
                    sp = "poidsV" if (mode == "corrige" and not c["donne"]) else "poids"
                poids.append(rf"\path {parent_ref} -- ({nom}.west) node[{sp},pos=0.5,anchor={anc}] {{${t}$}};")
                pr = prod * c["p"] if prod is not None else None
            if not c["enfants"] and mode == "corrige":
                txt = c["droite"] or ""
                if produits and pr is not None:
                    txt = (txt + r"\quad " if txt else "") + "$" + frac(pr) + "$"
                if txt:
                    si = "issueV" if c["vert"] else "issue"
                    droites.append(rf"\node[{si}] at ([xshift=4pt]{nom}.east) {{{txt}}};")
            visiter(c, f"({nom}.east)", c["y"], pr)

    lignes = [r"\begin{tikzpicture}[x=1cm,y=1cm]", rf"\coordinate (r) at (0,{racine['y']:.3f});"]
    visiter(racine, "(r)", racine["y"], Fr(1))
    lignes += noeuds
    lignes += [a for s, a in aretes if s == "branche"] + [a for s, a in aretes if s == "brancheV"]
    lignes.append(r"\fill[racine] (r) circle (1.9pt);")
    lignes += poids + droites
    if titres:
        haut = max(_tous_y(racine)) + 0.45
        for i, t in enumerate(titres, start=1):
            lignes.append(rf"\node[titreCol] at ({i * L:.3f},{haut:.3f}) {{{t}}};")
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


T2 = [r"1\textsuperscript{er} tirage", r"2\textsuperscript{e} tirage"]
TL = [r"1\textsuperscript{er} lancer", r"2\textsuperscript{e} lancer"]


def deux_etapes(e1, e2, p1, p2, donnes, verts, droites=True):
    """e1, e2 : noms des issues de chaque étape ; p1[a] ; p2[a][b] (Fractions) ;
    donnes : poids donnés (('1', a) ou ('2', a, b)) ; verts : chemins (a, b)."""
    res = []
    for a in e1:
        enf = []
        for b in e2:
            enf.append(N(b, p2[a][b], donne=("2", a, b) in donnes, vert=(a, b) in verts,
                         droite=(f"${a}{b}$" if droites else None)))
        res.append(N(a, p1[a], *enf, donne=("1", a) in donnes))
    return res


def pieces(verts=()):
    return [N(a, Fr(1, 2), *[N(b, Fr(1, 2), donne=False, vert=(a + b) in verts, droite=f"${a}{b}$") for b in "PF"],
              donne=False) for a in "PF"]


FIGURES["arbre_pieces_enonce"] = arbre(pieces(), "enonce", L=2.0, dy=0.85, ecarts={1: 0.25}, titres=TL)
FIGURES["arbre_pieces"] = arbre(pieces({"PF", "FP"}), "corrige", L=2.0, dy=0.85, ecarts={1: 0.25}, titres=TL)

# 2346 / cours : 3 R et 2 B, avec remise
P1 = {"R": Fr(3, 5), "B": Fr(2, 5)}
AVEC = {"R": {"R": Fr(3, 5), "B": Fr(2, 5)}, "B": {"R": Fr(3, 5), "B": Fr(2, 5)}}
SANS = {"R": {"R": Fr(2, 4), "B": Fr(2, 4)}, "B": {"R": Fr(3, 4), "B": Fr(1, 4)}}
DON1 = {("1", "R"), ("1", "B")}
FIGURES["arbre_remise_enonce"] = arbre(deux_etapes("RB", "RB", P1, AVEC, DON1, set()), "enonce", ecarts={1: 0.3}, titres=T2)
FIGURES["arbre_remise"] = arbre(deux_etapes("RB", "RB", P1, AVEC, DON1, {("R", "B"), ("B", "R")}), "corrige", ecarts={1: 0.3}, titres=T2)
FIGURES["arbre_sans_remise_enonce"] = arbre(deux_etapes("RB", "RB", P1, SANS, DON1, set()), "enonce", ecarts={1: 0.3}, titres=T2)
FIGURES["arbre_sans_remise"] = arbre(deux_etapes("RB", "RB", P1, SANS, DON1, {("R", "R")}), "corrige", ecarts={1: 0.3}, titres=T2)

# 2353 : U1 (2 blanches, 3 noires), U2 (4 blanches, 1 noire)
U1 = {"B": Fr(2, 5), "N": Fr(3, 5)}
U2 = {a: {"B": Fr(4, 5), "N": Fr(1, 5)} for a in "BN"}
TU = [r"urne $U_1$", r"urne $U_2$"]
FIGURES["arbre_urnes_enonce"] = arbre(deux_etapes("BN", "BN", U1, U2, set(), set()), "enonce", ecarts={1: 0.3}, titres=TU)
FIGURES["arbre_urnes"] = arbre(deux_etapes("BN", "BN", U1, U2, set(), {("B", "B"), ("N", "N")}), "corrige", ecarts={1: 0.3}, titres=TU)

# 2356 : menus (dénombrement : 3 entrées, 2 plats)
ENT = [r"\text{soupe}", r"\text{melon}", r"\text{taboulé}"]
PLA = [r"\text{poisson}", r"\text{pâtes}"]


def menus():
    return [N(e, Fr(1, 3), *[N(p, Fr(1, 2), donne=False, vert=(k == 0)) for k, p in enumerate(PLA)],
              donne=False) for e in ENT]


FIGURES["arbre_menus"] = arbre(menus(), "corrige", L=2.4, dy=1.0, ecarts={1: 0.55},
                               titres=["entrée", "plat"], produits=True)


# ================================================================ tableaux à double entrée
STY = (r"\tikzset{grad/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt}}")


def grille(lignes, colonnes, f, verts, nom_l, nom_c, w=0.82, h=0.56):
    L = [r"\begin{tikzpicture}", STY]
    nl, nc = len(lignes), len(colonnes)
    for i, a in enumerate(lignes):
        for j, b in enumerate(colonnes):
            x0, y0 = (j + 1) * w, -(i + 1) * h
            v = (a, b) in verts
            fond = "otGreen!30" if v else "white"
            L.append(r"\draw[otRule,line width=.6pt,fill=%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (fond, x0, y0, x0 + w, y0 - h))
            L.append(r"\node[text=%s,inner sep=0pt] at (%.3f,%.3f) {$%s$};" % ("otGreenDark" if v else "otInk", x0 + w / 2, y0 - h / 2, f(a, b)))
    for j, b in enumerate(colonnes):
        L.append(r"\node[text=otNavy,inner sep=0pt] at (%.3f,%.3f) {$%s$};" % ((j + 1.5) * w, -h / 2, b))
    for i, a in enumerate(lignes):
        L.append(r"\node[text=otNavy,inner sep=0pt] at (%.3f,%.3f) {$%s$};" % (w / 2, -(i + 1.5) * h, a))
    L.append(r"\draw[otNavy,line width=.8pt] (%.3f,0.05) -- (%.3f,%.3f);" % (w, w, -(nl + 1) * h))
    L.append(r"\draw[otNavy,line width=.8pt] (-0.05,%.3f) -- (%.3f,%.3f);" % (-h, (nc + 1) * w, -h))
    L.append(r"\node[grad,anchor=south] at (%.3f,0.08) {%s};" % ((nc / 2 + 1) * w, nom_c))
    L.append(r"\node[grad,anchor=south,rotate=90] at (-0.1,%.3f) {%s};" % (-(nl / 2 + 1) * h, nom_l))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


D6 = [1, 2, 3, 4, 5, 6]
som = lambda a, b: a + b
FIGURES["tableau_sommes"] = grille(D6, D6, som, set(), "premier dé", "second dé")
FIGURES["tableau_somme7"] = grille(D6, D6, som, {(a, b) for a in D6 for b in D6 if a + b == 7}, "premier dé", "second dé")
FIGURES["tableau_somme10"] = grille(D6, D6, som, {(a, b) for a in D6 for b in D6 if a + b >= 10}, "premier dé", "second dé")
FIGURES["tableau_six"] = grille(D6, D6, som, {(a, b) for a in D6 for b in D6 if 6 in (a, b)}, "premier dé", "second dé")
C4 = [0, 1, 2, 3]
FIGURES["tableau_codes"] = grille(C4, C4, lambda a, b: f"{a}{b}", {(a, b) for a in C4 for b in C4 if a + b == 3},
                                  "premier chiffre", "second chiffre")
FIGURES["tableau_produits"] = grille(D6, D6, lambda a, b: a * b, {(a, b) for a in D6 for b in D6 if a * b % 2 == 0},
                                     "dé de Léa", "dé de Tom")
J3, R4 = [1, 2, 3], [1, 2, 3, 4]
FIGURES["tableau_kermesse"] = grille(J3, R4, som, {(a, b) for a in J3 for b in R4 if a + b == 5}, "jeton", "roue")


# ================================================================ urne, roue, dé
def urne(boules):
    """boules : liste de (couleur TikZ, nombre, texte légende)."""
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    L.append(r"\draw[otNavy,line width=1pt,fill=otSky!60] (-1.9,1.9) -- (-1.9,0.25) "
             r"arc[start angle=180,end angle=360,x radius=1.9,y radius=0.45] -- (1.9,1.9);")
    pos = []
    for r in range(3):
        for c in range(4):
            pos.append((-1.2 + c * 0.8 + (0.4 if r % 2 else 0), 0.35 + r * 0.55))
    i = 0
    for col, n, _ in boules:
        for _ in range(n):
            x, y = pos[i]
            L.append(rf"\fill[{col}] ({x:.2f},{y:.2f}) circle (0.24);")
            L.append(rf"\fill[white,opacity=.55] ({x-0.08:.2f},{y+0.08:.2f}) circle (0.06);")
            i += 1
    y = -0.6
    for col, n, txt in boules:
        L.append(rf"\fill[{col}] (-1.6,{y:.2f}) circle (0.13);")
        L.append(rf"\node[anchor=west,text=otInk] at (-1.4,{y:.2f}) {{{txt}}};")
        y -= 0.45
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["urne_10"] = urne([("otRed", 5, "$5$ boules rouges"), ("otNavy", 3, "$3$ boules bleues"),
                           ("otGreen", 2, "$2$ boules vertes")])


def roue(n, R=1.7, verts=()):
    import math
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    for k in range(n):
        a = 90 - k * 360 / n
        b = a - 360 / n
        fond = "otGreen!30" if (k + 1) in verts else ("otSky" if k % 2 == 0 else "white")
        L.append(r"\fill[%s] (0,0) -- (%.2f:%.2f) arc[start angle=%.2f,end angle=%.2f,radius=%.2f] -- cycle;" % (fond, a, R, a, b, R))
        L.append(r"\draw[otNavy,line width=.8pt] (0,0) -- (%.2f:%.2f);" % (a, R))
        m = (a + b) / 2
        col = "otGreenDark" if (k + 1) in verts else "otNavy"
        L.append(r"\node[text=%s,font=\large] at (%.2f:%.2f) {$%d$};" % (col, m, 0.66 * R, k + 1))
    L.append(r"\draw[otNavy,line width=1pt] (0,0) circle (%.2f);" % R)
    L.append(r"\fill[otNavy] (0,0) circle (1.6pt);")
    L.append(r"\fill[otOrange] (0,%.2f) -- (-0.17,%.2f) -- (0.17,%.2f) -- cycle;" % (R + 0.05, R + 0.38, R + 0.38))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["roue_8"] = roue(8)
FIGURES["roue_8_pairs"] = roue(8, verts=(2, 4, 6, 8))
FIGURES["roue_4"] = roue(4, R=1.3)


# ================================================================ fréquences qui se stabilisent
def simulation(p, n, graine):
    r = random.Random(graine)
    s, pts = 0, []
    for k in range(1, n + 1):
        s += r.random() < p
        if k % 20 == 0:
            pts.append((k, s / k))
    return pts


def courbe_frequence(points, cible, cible_tex, xmax, yticks, ymin, ymax, ylabel):
    coords = " ".join(f"({x},{y:.4f})" for x, y in points)
    yt = ",".join(str(v) for v, _ in yticks)
    ytl = ",".join("{$" + t + "$}" for _, t in yticks)
    return rf"""\begin{{tikzpicture}}
\begin{{axis}}[otLoi, width=6.1cm, height=4.0cm, xmin=0, xmax={xmax}, ymin={ymin}, ymax={ymax},
  scaled x ticks=false, scaled y ticks=false,
  xtick={{0,500,1000,1500,2000}}, xticklabels={{$0$,$500$,$1\,000$,$1\,500$,$2\,000$}},
  ytick={{{yt}}}, yticklabels={{{ytl}}},
  xlabel={{essais}}, ylabel={{{ylabel}}}]
\draw[otGreenDark, line width=0.9pt, dash pattern=on 4pt off 2.5pt] (axis cs:0,{cible}) -- (axis cs:{xmax},{cible});
\node[anchor=north east, legendeV, yshift=-3pt] at (axis cs:{xmax},{cible}) {{{cible_tex}}};
\addplot[courbe, line width=1pt] coordinates {{{coords}}};
\end{{axis}}
\end{{tikzpicture}}"""


FIGURES["frequences_piece"] = courbe_frequence(simulation(0.5, 2000, 11), 0.5, r"probabilité $0{,}5$", 2000,
                                               [(0.3, "0{,}3"), (0.4, "0{,}4"), (0.5, "0{,}5"), (0.6, "0{,}6"), (0.7, "0{,}7")],
                                               0.3, 0.75, "fréquence de « face »")
FIGURES["frequences_tiers"] = courbe_frequence(simulation(1 / 3, 2000, 5), 1 / 3, r"probabilité $1/3$", 2000,
                                               [(0.2, "0{,}2"), (0.3, "0{,}3"), (0.4, "0{,}4"), (0.5, "0{,}5")],
                                               0.15, 0.55, "fréquence du succès")
