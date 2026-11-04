# -*- coding: utf-8 -*-
"""Figures de la notion « Probabilités conditionnelles et indépendance » (Terminale).

Compilation (style des livres OptiTAB, contrôle des chevauchements) :

    python ../../../outils/figures_livre.py <dossier_notion> [nom …] [--planche]

Les arbres pondérés sont produits par la fonction `arbre` ci-dessous :
coordonnées calculées en Python, probabilités posées À CÔTÉ des branches
(au-dessus et à gauche du milieu d'une branche montante, au-dessous et à
gauche d'une branche descendante, au-dessus d'une branche horizontale),
jamais sur un trait. Chemins de la réponse en vert (otGreenDark), avec les
probabilités de leurs branches en vert : ce sont les facteurs multipliés.
Toutes les valeurs sont vérifiées par ../verif_probas.py.
"""
from fractions import Fraction
from itertools import product

PREAMBULE_EXTRA = r"""
\tikzset{
  evt/.style={font=\normalsize, text=otNavy, inner sep=2.4pt},
  evtV/.style={evt, text=otGreenDark},
  branche/.style={otNavy!65, line width=0.8pt, line cap=round},
  brancheV/.style={otGreenDark, line width=1.6pt, line cap=round},
  poids/.style={font=\small, text=otInk, inner sep=1.7pt},
  poidsV/.style={poids, text=otGreenDark},
  issue/.style={font=\small, text=otMuted, anchor=west, inner sep=1.5pt},
  issueV/.style={issue, text=otGreenDark},
  racine/.style={fill=otNavy},
}
"""


# ---------------------------------------------------------------- arbres
def N(nom, poids, *enfants, droite=None, vert=False, pos=0.5):
    """Nœud d'arbre : nom (LaTeX, sans $), poids de la branche qui y mène (LaTeX,
    sans $), sous-arbres ; pour une feuille, texte « droite » (probabilité du
    chemin) et vert=True pour mettre le chemin en évidence."""
    return {"nom": nom, "poids": poids, "enfants": list(enfants), "droite": droite,
            "vert": vert, "pos": pos}


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


def arbre(enfants, L=2.2, dy=1.0, ecarts=None, ecart_droite="4pt"):
    """Arbre pondéré horizontal (racine à gauche).

    L : distance entre deux niveaux (cm) ; dy : écart entre deux feuilles (cm) ;
    ecarts : {niveau: écart supplémentaire (cm) entre deux sous-arbres de ce niveau}.
    """
    racine = {"nom": None, "poids": None, "enfants": enfants, "droite": None, "vert": False, "pos": 0.5}
    _vert(racine)
    _placer(racine, 0, 0.0, dy, ecarts or {}, L)
    lignes = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    noeuds, aretes, poids, droites = [], [], [], []
    compteur = [0]

    def visiter(n, parent_ref, parent_y):
        for c in n["enfants"]:
            compteur[0] += 1
            nom = f"n{compteur[0]}"
            style = "evtV" if (c["vert"] and not c["enfants"]) else "evt"
            noeuds.append(rf"\node[{style}] ({nom}) at ({c['x']:.3f},{c['y']:.3f}) {{${c['nom']}$}};")
            st = "brancheV" if c["vert"] else "branche"
            aretes.append((st, rf"\draw[{st}] {parent_ref} -- ({nom}.west);"))
            if c["poids"] is not None:
                ecart = c["y"] - parent_y
                anc = "south east" if ecart > 1e-6 else ("north east" if ecart < -1e-6 else "south")
                sp = "poidsV" if c["vert"] else "poids"
                poids.append(rf"\path {parent_ref} -- ({nom}.west) node[{sp},pos={c['pos']},anchor={anc}] {{${c['poids']}$}};")
            if not c["enfants"] and c["droite"]:
                si = "issueV" if c["vert"] else "issue"
                droites.append(rf"\node[{si}] at ([xshift={ecart_droite}]{nom}.east) {{{c['droite']}}};")
            visiter(c, f"({nom}.east)", c["y"])

    lignes.append(rf"\coordinate (r) at (0,{racine['y']:.3f});")
    visiter(racine, "(r)", racine["y"])
    lignes += noeuds
    lignes += [a for s, a in aretes if s == "branche"] + [a for s, a in aretes if s == "brancheV"]
    lignes.append(r"\fill[racine] (r) circle (1.9pt);")
    lignes += poids + droites
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


def binaire(a, pa, b, pb, a1, pa1, a2, pa2, b1, pb1, b2, pb2, droites=None, verts=(), **kw):
    """Arbre à deux niveaux et quatre feuilles.
    droites : 4 textes (feuilles de haut en bas) ; verts : indices 0..3 des feuilles en vert."""
    d = droites or [None] * 4
    return arbre([
        N(a, pa, N(a1, pa1, droite=d[0], vert=0 in verts), N(a2, pa2, droite=d[1], vert=1 in verts)),
        N(b, pb, N(b1, pb1, droite=d[2], vert=2 in verts), N(b2, pb2, droite=d[3], vert=3 in verts)),
    ], **kw)


def F(p, q):
    return rf"\dfrac{{{p}}}{{{q}}}"


def fr_tex(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else F(x.numerator, x.denominator)


def m(txt):
    return f"${txt}$"


def bar(e):
    return rf"\overline{{{e}}}"


def urne(effectifs, n, noms, verts=(), droite=True, **kw):
    """Tirages successifs SANS remise dans une urne : effectifs = {couleur: nombre},
    n tirages, noms = {couleur: lettre}. Poids = proportions de boules restantes
    (fractions non simplifiées, comme dans les calculs) ; à droite : issue et
    probabilité du chemin (simplifiée). verts : issues à mettre en vert ("RRB"…)."""
    couleurs = list(effectifs)

    def sous(reste, prefixe, k):
        enfants = []
        total = sum(reste.values())
        for c in couleurs:
            if reste[c] == 0:
                continue
            r2 = dict(reste)
            r2[c] -= 1
            issue = prefixe + c
            p = F(reste[c], total)
            nom = f"{noms[c]}_{k}"
            if k == n:
                pr = Fraction(1)
                rr = dict(effectifs)
                for l in issue:
                    pr *= Fraction(rr[l], sum(rr.values()))
                    rr[l] -= 1
                txt = (rf"{issue} : ${fr_tex(pr)}$") if droite else None
                enfants.append(N(nom, p, droite=txt, vert=issue in verts))
            else:
                enfants.append(N(nom, p, *sous(r2, issue, k + 1)))
        return enfants

    return arbre(sous(dict(effectifs), "", 1), **kw)


def repetees(issues, probas, n, verts=(), droite_fn=None, indices=False, **kw):
    """n épreuves indépendantes identiques : issues = ["S","E"], probas = ["0{,}6","0{,}4"].
    droite_fn(issue) → texte de droite ; verts : issues en vert ("SSE"…)."""
    def sous(prefixe, k):
        enfants = []
        for e, p in zip(issues, probas):
            issue = prefixe + e
            nom = f"{e}_{k}" if indices else e
            if k == n:
                enfants.append(N(nom, p, droite=droite_fn(issue) if droite_fn else None, vert=issue in verts))
            else:
                enfants.append(N(nom, p, *sous(issue, k + 1)))
        return enfants
    return arbre(sous("", 1), **kw)


FIGURES = {}

# ================================================================ COURS
FIGURES["cours_partition"] = r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \fill[otGreen!22] (4.2,1.5) ellipse (3.55 and 0.92);
  \draw[otNavy,line width=0.9pt] (0,0) rectangle (8.4,3.3);
  \draw[otNavy,line width=0.9pt] (2.8,0) -- (2.8,3.3) (5.6,0) -- (5.6,3.3);
  \draw[otGreenDark,line width=1.1pt] (4.2,1.5) ellipse (3.55 and 0.92);
  \node[evt,anchor=north west] at (0.08,3.24) {$A_1$};
  \node[evt,anchor=north west] at (2.88,3.24) {$A_2$};
  \node[evt,anchor=north west] at (5.68,3.24) {$A_3$};
  \node[evt,text=otGreenDark] at (7.72,2.62) {$B$};
  \node[evt,text=otMuted,anchor=south east] at (8.4,3.33) {$\Omega$};
  \node[evt,text=otInk] at (1.78,1.5) {$A_1\cap B$};
  \node[evt,text=otInk] at (4.2,1.5) {$A_2\cap B$};
  \node[evt,text=otInk] at (6.62,1.5) {$A_3\cap B$};
\end{tikzpicture}"""

FIGURES["cours_arbre_general"] = binaire(
    "A", "P(A)", bar("A"), r"P(\overline{A})",
    "B", "P_A(B)", bar("B"), r"P_A(\overline{B})",
    "B", r"P_{\overline{A}}(B)", bar("B"), r"P_{\overline{A}}(\overline{B})",
    droites=[m(r"P(A\cap B)"), m(r"P(A\cap \overline{B})"),
             m(r"P(\overline{A}\cap B)"), m(r"P(\overline{A}\cap \overline{B})")],
    L=2.6, dy=1.05, ecarts={1: 0.45})

FIGURES["cours_depistage"] = binaire(
    "M", "0{,}02", bar("M"), "0{,}98",
    "T", "0{,}95", bar("T"), "0{,}05",
    "T", "0{,}1", bar("T"), "0{,}9",
    droites=[m(r"P(M\cap T)=0{,}019"), m(r"P(M\cap \overline{T})=0{,}001"),
             m(r"P(\overline{M}\cap T)=0{,}098"), m(r"P(\overline{M}\cap \overline{T})=0{,}882")],
    verts=(0, 2), L=2.2, dy=1.0, ecarts={1: 0.4})

_pen = {"SSS": "0{,}216", "SSE": "0{,}144", "SES": "0{,}144", "SEE": "0{,}096",
        "ESS": "0{,}144", "ESE": "0{,}096", "EES": "0{,}096", "EEE": "0{,}064"}
FIGURES["cours_penalties"] = repetees(
    ["S", "E"], ["0{,}6", "0{,}4"], 3, verts=("SSE", "SES", "ESS"),
    droite_fn=lambda i: rf"{i} : ${_pen[i]}$", L=1.95, dy=0.66, ecarts={1: 0.3, 2: 0.16})

# ================================================================ EXERCICES
# ---- 1283 : DS
FIGURES["ds_b1"] = binaire(
    "R_1", F(4, 10), "B_1", F(6, 10),
    "R_2", F(3, 9), "B_2", F(6, 9),
    "R_2", F(4, 9), "B_2", F(5, 9),
    droites=[m(r"P(R_1\cap R_2)=" + F(2, 15)), m(r"P(R_1\cap B_2)=" + F(4, 15)),
             m(r"P(B_1\cap R_2)=" + F(4, 15)), m(r"P(B_1\cap B_2)=" + F(1, 3))],
    verts=(1, 2), L=2.2, dy=1.2, ecarts={1: 0.45})

_ds_b2 = {"FFP", "FPF", "PFF"}
FIGURES["ds_b2"] = repetees(
    ["F", "P"], [F(1, 2), F(1, 2)], 3, verts=_ds_b2, indices=True,
    droite_fn=lambda i: rf"{i} : ${F(1, 8)}$", L=2.0, dy=0.86, ecarts={1: 0.4, 2: 0.32})

FIGURES["ds_d1"] = binaire(
    "M_1", "0{,}6", "M_2", "0{,}4",
    "D", "0{,}01", bar("D"), "0{,}99",
    "D", "0{,}03", bar("D"), "0{,}97",
    droites=[m(r"P(M_1\cap D)=0{,}006"), m(r"P(M_1\cap \overline{D})=0{,}594"),
             m(r"P(M_2\cap D)=0{,}012"), m(r"P(M_2\cap \overline{D})=0{,}388")],
    verts=(0, 2), L=2.2, dy=1.0, ecarts={1: 0.4})

FIGURES["ds_d2"] = binaire(
    "F", "0{,}55", "G", "0{,}45",
    "S", "0{,}75", bar("S"), "0{,}25",
    "S", "0{,}6", bar("S"), "0{,}4",
    droites=[m(r"P(F\cap S)=0{,}4125"), m(r"P(F\cap \overline{S})=0{,}1375"),
             m(r"P(G\cap S)=0{,}27"), m(r"P(G\cap \overline{S})=0{,}18")],
    verts=(0, 2), L=2.2, dy=1.0, ecarts={1: 0.4})

FIGURES["ds_e2"] = binaire(
    "M", "0{,}04", bar("M"), "0{,}96",
    "T", "0{,}97", bar("T"), "0{,}03",
    "T", "0{,}08", bar("T"), "0{,}92",
    droites=[m(r"P(M\cap T)=0{,}0388"), m(r"P(M\cap \overline{T})=0{,}0012"),
             m(r"P(\overline{M}\cap T)=0{,}0768"), m(r"P(\overline{M}\cap \overline{T})=0{,}8832")],
    verts=(0, 2), L=2.2, dy=1.0, ecarts={1: 0.4})

# ---- 1280 : arbres pondérés et applications
FIGURES["e1280_q1"] = binaire(
    "R_1", F(5, 8), "V_1", F(3, 8),
    "R_2", F(4, 7), "V_2", F(3, 7),
    "R_2", F(5, 7), "V_2", F(2, 7),
    droites=[m(r"P(R_1\cap R_2)=" + F(5, 14)), m(r"P(R_1\cap V_2)=" + F(15, 56)),
             m(r"P(V_1\cap R_2)=" + F(15, 56)), m(r"P(V_1\cap V_2)=" + F(3, 28))],
    verts=(1,), L=2.2, dy=1.2, ecarts={1: 0.45})

FIGURES["e1280_q3"] = binaire(
    "F", F(3, 5), "G", F(2, 5),
    "S", F(5, 9), bar("S"), F(4, 9),
    "S", F(2, 3), bar("S"), F(1, 3),
    droites=[m(r"P(F\cap S)=" + F(1, 3)), m(r"P(F\cap \overline{S})=" + F(4, 15)),
             m(r"P(G\cap S)=" + F(4, 15)), m(r"P(G\cap \overline{S})=" + F(2, 15))],
    verts=(0, 2), L=2.2, dy=1.2, ecarts={1: 0.45})

FIGURES["e1280_q4"] = binaire(
    "M", "0{,}05", bar("M"), "0{,}95",
    "T", "0{,}98", bar("T"), "0{,}02",
    "T", "0{,}05", bar("T"), "0{,}95",
    droites=[m(r"P(M\cap T)=0{,}049"), m(r"P(M\cap \overline{T})=0{,}001"),
             m(r"P(\overline{M}\cap T)=0{,}0475"), m(r"P(\overline{M}\cap \overline{T})=0{,}9025")],
    verts=(0, 2), L=2.2, dy=1.0, ecarts={1: 0.4})

# ---- 1281 : indépendance et applications
FIGURES["e1281_q2"] = binaire(
    "R_1", F(3, 5), "B_1", F(2, 5),
    "R_2", F(3, 5), "B_2", F(2, 5),
    "R_2", F(3, 5), "B_2", F(2, 5),
    droites=[m(r"P(R_1\cap R_2)=" + F(9, 25)), m(r"P(R_1\cap B_2)=" + F(6, 25)),
             m(r"P(B_1\cap R_2)=" + F(6, 25)), m(r"P(B_1\cap B_2)=" + F(4, 25))],
    verts=(0,), L=2.2, dy=1.2, ecarts={1: 0.45})

FIGURES["e1281_q3"] = repetees(
    ["P", "F"], [F(1, 2), F(1, 2)], 3, verts={"PPF", "PFP", "FPP"}, indices=True,
    droite_fn=lambda i: rf"{i} : ${F(1, 8)}$", L=2.0, dy=0.86, ecarts={1: 0.4, 2: 0.32})

FIGURES["e1281_q5"] = binaire(
    "C_1", "0{,}9", bar("C_1"), "0{,}1",
    "C_2", "0{,}8", bar("C_2"), "0{,}2",
    "C_2", "0{,}8", bar("C_2"), "0{,}2",
    droites=[m(r"P(C_1\cap C_2)=0{,}72"), m(r"P(C_1\cap \overline{C_2})=0{,}18"),
             m(r"P(\overline{C_1}\cap C_2)=0{,}08"), m(r"P(\overline{C_1}\cap \overline{C_2})=0{,}02")],
    verts=(0,), L=2.2, dy=1.0, ecarts={1: 0.4})

# ---- 1282 : applications complexes
FIGURES["e1282_q1"] = arbre([
    N("A", "0{,}5", N("D", "0{,}01", droite=m(r"P(A\cap D)=0{,}005"), vert=True),
      N(bar("D"), "0{,}99", droite=m(r"P(A\cap \overline{D})=0{,}495"))),
    N("B", "0{,}3", N("D", "0{,}02", droite=m(r"P(B\cap D)=0{,}006"), vert=True),
      N(bar("D"), "0{,}98", droite=m(r"P(B\cap \overline{D})=0{,}294"))),
    N("C", "0{,}2", N("D", "0{,}04", droite=m(r"P(C\cap D)=0{,}008"), vert=True),
      N(bar("D"), "0{,}96", droite=m(r"P(C\cap \overline{D})=0{,}192"))),
], L=2.2, dy=0.9, ecarts={1: 0.4})

FIGURES["e1282_q3"] = binaire(
    "M", "0{,}03", bar("M"), "0{,}97",
    "T", "0{,}96", bar("T"), "0{,}04",
    "T", "0{,}06", bar("T"), "0{,}94",
    droites=[m(r"P(M\cap T)=0{,}0288"), m(r"P(M\cap \overline{T})=0{,}0012"),
             m(r"P(\overline{M}\cap T)=0{,}0582"), m(r"P(\overline{M}\cap \overline{T})=0{,}9118")],
    verts=(0, 2), L=2.2, dy=1.0, ecarts={1: 0.4})

FIGURES["e1282_q4"] = urne({"R": 5, "B": 3}, 3, {"R": "R", "B": "B"}, verts={"RRR"},
                           L=2.0, dy=0.86, ecarts={1: 0.4, 2: 0.32})

# ---- 1279 : arbres pondérés
FIGURES["e1279_q1"] = urne({"R": 3, "B": 2}, 2, {"R": "R", "B": "B"}, verts={"RR"},
                           L=2.4, dy=1.2, ecarts={1: 0.45})

FIGURES["e1279_q2"] = repetees(
    ["P", "F"], [F(1, 2), F(1, 2)], 2, verts={"PF", "FP"}, indices=True,
    droite_fn=lambda i: rf"{i} : ${F(1, 4)}$", L=2.4, dy=1.2, ecarts={1: 0.45})

FIGURES["e1279_q3"] = repetees(
    ["B", "N"], [F(2, 5), F(3, 5)], 2, verts={"BN", "NB"}, indices=True,
    droite_fn=lambda i: rf"{i} : ${fr_tex(Fraction(2 if i[0] == 'B' else 3, 5) * Fraction(2 if i[1] == 'B' else 3, 5))}$",
    L=2.4, dy=1.2, ecarts={1: 0.45})

_pj = {"V": Fraction(2, 5), "J": Fraction(2, 5), "R": Fraction(1, 5)}


def _q4():
    # nœuds à trois branches : fractions en ligne (\tfrac, corps normal) et poids de la
    # branche du milieu rapproché de l'extrémité, là où l'angle entre branches est le plus ouvert
    t = lambda x: rf"\tfrac{{{x.numerator}}}{{{x.denominator}}}"
    enfants = []
    for a in "VJR":
        sous = []
        for b in "VJR":
            sous.append(N(f"{b}_2", t(_pj[b]), droite=rf"{a}{b} : ${fr_tex(_pj[a] * _pj[b])}$",
                          vert=(a == b), pos=0.74 if b == "J" else 0.5))
        enfants.append(N(f"{a}_1", t(_pj[a]), *sous))
    return enfants


FIGURES["e1279_q4"] = arbre(_q4(), L=2.6, dy=0.95, ecarts={1: 0.4}).replace(
    r"\begin{tikzpicture}[x=1cm,y=1cm]", r"\begin{tikzpicture}[x=1cm,y=1cm,poids/.append style={font=\normalsize}]")

FIGURES["e1279_q5"] = urne({"R": 4, "B": 6}, 3, {"R": "R", "B": "B"}, verts={"BBB"},
                           L=2.0, dy=0.86, ecarts={1: 0.4, 2: 0.32})

# ---- 1276 (énoncé : données) et 1275 (corrigés : chemins)
FIGURES["bayes_q1_donnees"] = arbre([
    N("M_1", "0{,}4", N("D", "0{,}02"), N(bar("D"), "0{,}98")),
    N("M_2", "0{,}35", N("D", "0{,}03"), N(bar("D"), "0{,}97")),
    N("M_3", "0{,}25", N("D", "0{,}05"), N(bar("D"), "0{,}95")),
], L=2.4, dy=0.9, ecarts={1: 0.4})

FIGURES["bayes_q2_donnees"] = binaire(
    "M", "0{,}02", bar("M"), "0{,}98",
    "T", "0{,}95", bar("T"), "0{,}05",
    "T", "0{,}1", bar("T"), "0{,}9", L=2.4, dy=1.0, ecarts={1: 0.4})

FIGURES["bayes_q3_donnees"] = binaire(
    "A", F(1, 2), "B", F(1, 2),
    "R", F(3, 5), bar("R"), F(2, 5),
    "R", F(1, 5), bar("R"), F(4, 5), L=2.4, dy=1.2, ecarts={1: 0.45})

FIGURES["bayes_q4_donnees"] = binaire(
    "R", "0{,}7", bar("R"), "0{,}3",
    "S", "0{,}9", bar("S"), "0{,}1",
    "S", "0{,}3", bar("S"), "0{,}7", L=2.4, dy=1.0, ecarts={1: 0.4})

FIGURES["pt_q1"] = arbre([
    N("M_1", "0{,}4", N("D", "0{,}02", droite=m(r"P(M_1\cap D)=0{,}008"), vert=True),
      N(bar("D"), "0{,}98", droite=m(r"P(M_1\cap \overline{D})=0{,}392"))),
    N("M_2", "0{,}35", N("D", "0{,}03", droite=m(r"P(M_2\cap D)=0{,}0105"), vert=True),
      N(bar("D"), "0{,}97", droite=m(r"P(M_2\cap \overline{D})=0{,}3395"))),
    N("M_3", "0{,}25", N("D", "0{,}05", droite=m(r"P(M_3\cap D)=0{,}0125"), vert=True),
      N(bar("D"), "0{,}95", droite=m(r"P(M_3\cap \overline{D})=0{,}2375"))),
], L=2.2, dy=0.9, ecarts={1: 0.4})

FIGURES["pt_q2"] = binaire(
    "F", "0{,}6", "G", "0{,}4",
    "M", "0{,}7", bar("M"), "0{,}3",
    "M", "0{,}5", bar("M"), "0{,}5",
    droites=[m(r"P(F\cap M)=0{,}42"), m(r"P(F\cap \overline{M})=0{,}18"),
             m(r"P(G\cap M)=0{,}2"), m(r"P(G\cap \overline{M})=0{,}2")],
    verts=(0, 2), L=2.2, dy=1.0, ecarts={1: 0.4})

FIGURES["pt_q4"] = binaire(
    "A", F(1, 2), "B", F(1, 2),
    "R", F(3, 5), bar("R"), F(2, 5),
    "R", F(1, 5), bar("R"), F(4, 5),
    droites=[m(r"P(A\cap R)=" + F(3, 10)), m(r"P(A\cap \overline{R})=" + F(1, 5)),
             m(r"P(B\cap R)=" + F(1, 10)), m(r"P(B\cap \overline{R})=" + F(2, 5))],
    verts=(0, 2), L=2.2, dy=1.2, ecarts={1: 0.45})

FIGURES["pt_q5"] = binaire(
    "R", "0{,}7", bar("R"), "0{,}3",
    "S", "0{,}9", bar("S"), "0{,}1",
    "S", "0{,}3", bar("S"), "0{,}7",
    droites=[m(r"P(R\cap S)=0{,}63"), m(r"P(R\cap \overline{S})=0{,}07"),
             m(r"P(\overline{R}\cap S)=0{,}09"), m(r"P(\overline{R}\cap \overline{S})=0{,}21")],
    verts=(0, 2), L=2.2, dy=1.0, ecarts={1: 0.4})

# ---- 1277 : tirages successifs (5 R, 3 B, sans remise)
FIGURES["e1277_arbre"] = urne({"R": 5, "B": 3}, 3, {"R": "R", "B": "B"},
                              L=2.0, dy=0.86, ecarts={1: 0.4, 2: 0.32})
FIGURES["e1277_q5"] = urne({"R": 5, "B": 3}, 3, {"R": "R", "B": "B"}, verts={"RRR", "RBR", "BRR", "BBR"},
                           L=2.0, dy=0.86, ecarts={1: 0.4, 2: 0.32})
