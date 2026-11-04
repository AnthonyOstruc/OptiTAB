# -*- coding: utf-8 -*-
"""Figures de la notion « Probabilités conditionnelles et indépendance » (Première).

Compilation (style des livres OptiTAB, contrôle des chevauchements) :

    python ../../../outils/figures_livre.py <dossier_notion> [nom …] [--planche]

- Arbres pondérés : coordonnées calculées en Python (moteur repris de la
  notion Terminale 179), probabilités posées à côté des branches, jamais sur
  un trait. Les probabilités sont des Fraction : les probabilités des chemins
  sont calculées ici (produit le long du chemin), jamais recopiées à la main.
  Trois modes :
    « cours »   : tout en noir, chemins utiles en vert épais ;
    « enonce »  : probabilités données par l'énoncé, « … » pour les autres ;
    « corrige » : probabilités trouvées et probabilités des chemins en vert.
- Tableaux croisés : énoncé en tableau du site (cases « … »), corrigé en
  figure, cases trouvées en vert sur fond vert pâle.
- Simulations : graines fixes ; les mêmes fonctions servent au script
  ../verif_probas_conditionnelles.py, qui contrôle les nombres cités.
"""
import random
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

getcontext().prec = 40

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
  legende/.style={font=\otRegular\fontsize{9}{10}\selectfont, text=otMuted, inner sep=1.5pt},
  legendeV/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otGreenDark, inner sep=1.5pt},
  tete/.style={font=\normalsize, text=otNavy, inner sep=1pt},
  case/.style={font=\normalsize, text=otInk, inner sep=1pt},
  caseV/.style={case, text=otGreenDark},
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


# ================================================================ nombres
def dec(x):
    """Écriture décimale exacte (virgule LaTeX) d'une fraction décimale."""
    x = Fr(x)
    q = x.denominator
    for f in (2, 5):
        while q % f == 0:
            q //= f
    if q != 1:
        raise ValueError(f"{x} n'est pas un nombre décimal")
    s = format((Decimal(x.numerator) / Decimal(x.denominator)).normalize(), "f")
    ent, _, frac = s.partition(".")
    neg = ent.startswith("-")
    ent = ent.lstrip("-")
    if len(ent) > 4:  # espace fine des milliers
        g = []
        while ent:
            g.insert(0, ent[-3:])
            ent = ent[:-3]
        ent = r"\,".join(g)
    return ("-" if neg else "") + ent + ("{,}" + frac if frac else "")


def frac(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else rf"\dfrac{{{x.numerator}}}{{{x.denominator}}}"


def fmt(x, mode):
    return dec(x) if mode == "d" else frac(x)


def bar(e):
    return rf"\overline{{{e}}}"


# ================================================================ arbres
def N(nom, p, *enfants, donne=True, vert=False, droite=None, pos=0.5):
    """Nœud : nom (LaTeX sans $), p = probabilité de la branche qui y mène
    (Fraction, ou chaîne LaTeX pour un arbre « littéral » du cours) ;
    donne=False : valeur à trouver (« … » dans l'énoncé, verte dans le corrigé)."""
    return {"nom": nom, "p": p, "enfants": list(enfants), "donne": donne,
            "vert": vert, "droite": droite, "pos": pos}


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


def arbre(enfants, mode="corrige", nombres="d", L=2.2, dy=1.0, ecarts=None, ecart_droite="4pt"):
    """Arbre pondéré horizontal. mode : "cours" | "enonce" | "corrige" ;
    nombres : "d" (décimaux) ou "f" (fractions)."""
    racine = {"nom": None, "p": None, "enfants": enfants, "droite": None, "vert": False,
              "donne": True, "pos": 0.5}
    if mode == "cours":
        _vert(racine)
    _placer(racine, 0, 0.0, dy, ecarts or {}, L)
    noeuds, aretes, poids, droites = [], [], [], []
    k = [0]

    def texte_p(c):
        if isinstance(c["p"], str):
            return c["p"]
        if mode == "enonce" and not c["donne"]:
            return r"\ldots"
        return fmt(c["p"], nombres)

    def visiter(n, parent_ref, parent_y, chemin, prod):
        for c in n["enfants"]:
            k[0] += 1
            nom = f"n{k[0]}"
            noeuds.append(rf"\node[evt] ({nom}) at ({c['x']:.3f},{c['y']:.3f}) {{${c['nom']}$}};")
            st = "brancheV" if (mode == "cours" and c["vert"]) else "branche"
            aretes.append((st, rf"\draw[{st}] {parent_ref} -- ({nom}.west);"))
            ecart = c["y"] - parent_y
            anc = "south east" if ecart > 1e-6 else ("north east" if ecart < -1e-6 else "south")
            if mode == "cours":
                sp = "poidsV" if c["vert"] else "poids"
            elif mode == "corrige" and not c["donne"]:
                sp = "poidsV"
            else:
                sp = "poids"
            poids.append(rf"\path {parent_ref} -- ({nom}.west) node[{sp},pos={c['pos']},anchor={anc}] {{${texte_p(c)}$}};")
            ch = chemin + [c["nom"]]
            pr = None if (prod is None or isinstance(c["p"], str)) else prod * c["p"]
            if not c["enfants"]:
                txt = c["droite"]
                if txt is None and mode == "corrige" and pr is not None:
                    # corrigé : seule la probabilité du chemin (figure étroite, lisible sur téléphone)
                    txt = "$" + fmt(pr, nombres) + "$"
                if txt and mode != "enonce":
                    si = "issueV" if (mode == "corrige" or c["vert"]) else "issue"
                    if mode == "corrige":
                        si += r", font=\normalsize"
                    droites.append(rf"\node[{si}] at ([xshift={ecart_droite}]{nom}.east) {{{txt}}};")
            visiter(c, f"({nom}.east)", c["y"], ch, pr)

    lignes = [r"\begin{tikzpicture}[x=1cm,y=1cm]", rf"\coordinate (r) at (0,{racine['y']:.3f});"]
    visiter(racine, "(r)", racine["y"], [], Fr(1))
    lignes += noeuds
    lignes += [a for s, a in aretes if s == "branche"] + [a for s, a in aretes if s == "brancheV"]
    lignes.append(r"\fill[racine] (r) circle (1.9pt);")
    lignes += poids + droites
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


def binaire(a, pa, b, pb, a1, pa1, a2, pa2, b1, pb1, b2, pb2, donnes=(), droites=None, verts=()):
    """Arbre 2 × 2. Les poids sont des Fraction (ou du LaTeX) ; donnes : indices
    0..5 des poids donnés par l'énoncé (0 : pa, 1 : pb, 2 : pa1, 3 : pa2, 4 : pb1, 5 : pb2)."""
    d = droites or [None] * 4
    return [
        N(a, pa, N(a1, pa1, donne=2 in donnes, droite=d[0], vert=0 in verts),
          N(a2, pa2, donne=3 in donnes, droite=d[1], vert=1 in verts), donne=0 in donnes),
        N(b, pb, N(b1, pb1, donne=4 in donnes, droite=d[2], vert=2 in verts),
          N(b2, pb2, donne=5 in donnes, droite=d[3], vert=3 in verts), donne=1 in donnes),
    ]


def paire(nom, ex, construire, nombres="d", **kw):
    """Version énoncé (…) et version corrigé (vert) d'un même arbre."""
    FIGURES[f"{nom}_enonce"] = arbre(construire(), "enonce", nombres, **kw)
    FIGURES[nom] = arbre(construire(), "corrige", nombres, **kw)


def m(t):
    return f"${t}$"


# ================================================================ tableaux croisés
def tableau(entetes, lignes, mode="corrige", l0=1.3, l=1.45, h=0.8):
    """entetes : en-têtes de colonnes (LaTeX sans $) ; lignes : [(en-tête, [(valeur, donnée)])].
    Corrigé : cases trouvées en vert sur fond vert pâle."""
    nc, nl = len(entetes), len(lignes)
    largeur = l0 + nc * l
    hauteur = (nl + 1) * h
    out = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    # fonds des cases trouvées (en retrait des filets)
    for i, (_, cases) in enumerate(lignes):
        y0 = hauteur - (i + 2) * h
        for j, (v, donne) in enumerate(cases):
            if not donne and mode == "corrige":
                x0 = l0 + j * l
                out.append(rf"\fill[otGreen!14] ({x0 + 0.07:.3f},{y0 + 0.07:.3f}) rectangle ({x0 + l - 0.07:.3f},{y0 + h - 0.07:.3f});")
    # filets horizontaux (style des livres)
    out.append(rf"\draw[otNavy, line width=0.9pt] (0,{hauteur:.3f}) -- ({largeur:.3f},{hauteur:.3f});")
    out.append(rf"\draw[otNavy, line width=0.6pt] (0,{hauteur - h:.3f}) -- ({largeur:.3f},{hauteur - h:.3f});")
    for i in range(1, nl):
        y = hauteur - (i + 1) * h
        st = "otMuted, line width=0.6pt" if i == nl - 1 else "otRule, line width=0.5pt"
        out.append(rf"\draw[{st}] (0,{y:.3f}) -- ({largeur:.3f},{y:.3f});")
    out.append(rf"\draw[otNavy, line width=0.9pt] (0,0) -- ({largeur:.3f},0);")
    out.append(rf"\draw[otRule, line width=0.5pt] ({l0:.3f},0) -- ({l0:.3f},{hauteur:.3f});")
    out.append(rf"\draw[otRule, line width=0.5pt] ({l0 + (nc - 1) * l:.3f},0) -- ({l0 + (nc - 1) * l:.3f},{hauteur:.3f});")
    for j, t in enumerate(entetes):
        out.append(rf"\node[tete] at ({l0 + (j + 0.5) * l:.3f},{hauteur - h / 2:.3f}) {{{t}}};")
    for i, (t, cases) in enumerate(lignes):
        yc = hauteur - (i + 1.5) * h
        out.append(rf"\node[tete] at ({l0 / 2:.3f},{yc:.3f}) {{{t}}};")
        for j, (v, donne) in enumerate(cases):
            st = "caseV" if (not donne and mode == "corrige") else "case"
            out.append(rf"\node[{st}] at ({l0 + (j + 0.5) * l:.3f},{yc:.3f}) {{${v}$}};")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


# ================================================================ grilles de deux dés / jetons
def grille(n, valeur, mode, ombre=lambda a, b: False, cadre_ligne=None, cadres=(), c=0.74,
           titre_l="dé rouge", titre_c="dé bleu", legendes=()):
    """Tableau à double entrée n × n : ligne a (premier), colonne b (second).
    mode "enonce" : cases vides ; "corrige" : valeurs vertes, cases ombrées,
    cadre_ligne : numéro de la ligne encadrée ; cadres : cases encadrées (retrait)."""
    out = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    H = (n + 1) * c
    # fonds
    out.append(rf"\fill[otSky] ({c:.3f},{n * c:.3f}) rectangle ({H:.3f},{H:.3f});")
    out.append(rf"\fill[otSky] (0,0) rectangle ({c:.3f},{n * c:.3f});")
    if mode == "corrige":
        for a in range(1, n + 1):
            for b in range(1, n + 1):
                if ombre(a, b):
                    x0, y0 = b * c, (n - a) * c
                    out.append(rf"\fill[otGreen!22] ({x0:.3f},{y0:.3f}) rectangle ({x0 + c:.3f},{y0 + c:.3f});")
    # quadrillage
    for k in range(n + 2):
        x = k * c
        y0 = 0 if k else 0
        out.append(rf"\draw[otRule, line width=0.5pt] ({x:.3f},{0 if k else 0:.3f}) -- ({x:.3f},{n * c if k == 0 else H:.3f});")
    for k in range(n + 2):
        y = k * c
        out.append(rf"\draw[otRule, line width=0.5pt] ({0 if k <= n else c:.3f},{y:.3f}) -- ({H:.3f},{y:.3f});")
    for k in range(1, n + 1):
        out.append(rf"\node[tete] at ({(k + 0.5) * c:.3f},{(n + 0.5) * c:.3f}) {{${k}$}};")
        out.append(rf"\node[tete] at ({0.5 * c:.3f},{(n - k + 0.5) * c:.3f}) {{${k}$}};")
    if mode == "corrige":
        for a in range(1, n + 1):
            for b in range(1, n + 1):
                out.append(rf"\node[caseV] at ({(b + 0.5) * c:.3f},{(n - a + 0.5) * c:.3f}) {{${valeur(a, b)}$}};")
        if cadre_ligne:
            y0 = (n - cadre_ligne) * c
            out.append(rf"\draw[otNavy, line width=1.5pt] ({c:.3f},{y0:.3f}) rectangle ({H:.3f},{y0 + c:.3f});")
        for a, b in cadres:
            x0, y0 = b * c, (n - a) * c
            out.append(rf"\draw[otNavy, line width=1.1pt] ({x0 + 0.06:.3f},{y0 + 0.06:.3f}) rectangle ({x0 + c - 0.06:.3f},{y0 + c - 0.06:.3f});")
    out.append(rf"\node[legende, anchor=south] at ({(n + 2) * c / 2:.3f},{H + 0.06:.3f}) {{{titre_c}}};")
    out.append(rf"\node[legende, anchor=south, rotate=90] at ({-0.06:.3f},{n * c / 2:.3f}) {{{titre_l}}};")
    y = -0.12
    for txt in legendes:
        if mode == "corrige":
            out.append(rf"\node[legende, anchor=north west] at (0,{y:.3f}) {{{txt}}};")
            y -= 0.45
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


# ================================================================ simulations (graines fixes)
def simulation_depistage(n, graine=2026):
    """Code du cours : personne() puis freq(n). Renvoie la liste des fréquences
    cumulées (n_k, nb_mt / nb_t) tous les 500 tirages et la valeur finale."""
    r = random.Random(graine)
    nb_t = nb_mt = 0
    points = []
    for k in range(1, n + 1):
        mal = r.random() < 0.02
        if mal:
            t = r.random() < 0.95
        else:
            t = r.random() < 0.05
        if t:
            nb_t += 1
            if mal:
                nb_mt += 1
        if k % 500 == 0 and nb_t:
            points.append((k, nb_mt / nb_t))
    return points, nb_mt / nb_t, nb_t, nb_mt


def simulation_lancers(n, graine=7):
    """Code de nouveau-2 : deux_lancers() puis simulation(n)."""
    r = random.Random(graine)
    nb_r2 = nb_r1r2 = 0
    points = []
    for k in range(1, n + 1):
        r1 = r.random() < 0.7
        if r1:
            r2 = r.random() < 0.8
        else:
            r2 = r.random() < 0.6
        if r2:
            nb_r2 += 1
            if r1:
                nb_r1r2 += 1
        if k % 50 == 0:
            points.append((k, nb_r2 / k))
    return points, nb_r2 / n, nb_r1r2 / nb_r2


def courbe_frequence(points, cible, ymin, ymax, yticks, xticks, xticklabels, xmax, cible_tex,
                     ylabel, corrige=True, largeur=6.0, dessous=True):
    """dessous=True : valeur cible écrite sous la droite pointillée, à droite
    (là où la courbe est au-dessus) ; sinon au-dessus."""
    coords = " ".join(f"({x},{y:.4f})" for x, y in points)
    yt = ",".join(str(v) for v, _ in yticks)
    ytl = ",".join("{$" + t + "$}" for _, t in yticks)
    xt = ",".join(str(v) for v in xticks)
    xtl = ",".join("{$" + t + "$}" for t in xticklabels)
    ligne = ""
    if corrige:
        anc, dec_y = ("north east", "-3pt") if dessous else ("south east", "3pt")
        ligne = rf"""\draw[otGreenDark, line width=0.9pt, dash pattern=on 4pt off 2.5pt] (axis cs:0,{cible}) -- (axis cs:{xmax},{cible});
\node[anchor={anc}, legendeV, yshift={dec_y}] at (axis cs:{xmax},{cible}) {{{cible_tex}}};"""
    return rf"""\begin{{tikzpicture}}
\begin{{axis}}[otLoi, width={largeur}cm, height=4.2cm, xmin=0, xmax={xmax}, ymin={ymin}, ymax={ymax},
  scaled x ticks=false, scaled y ticks=false,
  xtick={{{xt}}}, xticklabels={{{xtl}}}, ytick={{{yt}}}, yticklabels={{{ytl}}},
  xlabel={{$n$}}, ylabel={{{ylabel}}}]
{ligne}
\addplot[courbe, line width=1pt] coordinates {{{coords}}};
\end{{axis}}
\end{{tikzpicture}}"""


# ================================================================ COURS
FIGURES["cours_arbre_general"] = arbre(binaire(
    "A", "P(A)", bar("A"), r"P(\overline{A})",
    "B", "P_A(B)", bar("B"), r"P_A(\overline{B})",
    "B", r"P_{\overline{A}}(B)", bar("B"), r"P_{\overline{A}}(\overline{B})",
    droites=[m(r"P(A\cap B)"), m(r"P(A\cap \overline{B})"),
             m(r"P(\overline{A}\cap B)"), m(r"P(\overline{A}\cap \overline{B})")]),
    "cours", L=2.2, dy=1.05, ecarts={1: 0.45})


def _bus():
    return binaire("A", Fr(3, 10), bar("A"), Fr(7, 10),
                   "B", Fr(8, 10), bar("B"), Fr(2, 10),
                   "B", Fr(1, 10), bar("B"), Fr(9, 10),
                   droites=[m(r"P(A\cap B) = 0{,}24"), m(r"P(A\cap \overline{B}) = 0{,}06"),
                            m(r"P(\overline{A}\cap B) = 0{,}07"), m(r"P(\overline{A}\cap \overline{B}) = 0{,}63")],
                   verts=(0, 2))


FIGURES["cours_arbre_bus"] = arbre(_bus(), "cours", L=2.0, dy=1.0, ecarts={1: 0.4})

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


def _depistage():
    return binaire("M", Fr(2, 100), bar("M"), Fr(98, 100),
                   "T", Fr(95, 100), bar("T"), Fr(5, 100),
                   "T", Fr(5, 100), bar("T"), Fr(95, 100),
                   droites=[m(r"P(M\cap T) = 0{,}019"), m(r"P(M\cap \overline{T}) = 0{,}001"),
                            m(r"P(\overline{M}\cap T) = 0{,}049"), m(r"P(\overline{M}\cap \overline{T}) = 0{,}931")],
                   verts=(0, 2))


FIGURES["cours_depistage"] = arbre(_depistage(), "cours", L=2.0, dy=1.0, ecarts={1: 0.4})


def _remise():
    t = Fr(3, 5)
    d = Fr(2, 5)
    return binaire("R_1", t, "B_1", d, "R_2", t, "B_2", d, "R_2", t, "B_2", d,
                   droites=[m(r"P(R_1\cap R_2) = \dfrac{9}{25}"), m(r"P(R_1\cap B_2) = \dfrac{6}{25}"),
                            m(r"P(B_1\cap R_2) = \dfrac{6}{25}"), m(r"P(B_1\cap B_2) = \dfrac{4}{25}")],
                   verts=(0, 3))


FIGURES["cours_remise"] = arbre(_remise(), "cours", "f", L=2.0, dy=1.2, ecarts={1: 0.45})

_pts_dep, _f_dep, _, _ = simulation_depistage(100000)
FIGURES["cours_simulation"] = courbe_frequence(
    _pts_dep, 0.2794, 0.18, 0.40, [(0.2, "0{,}2"), (0.25, "0{,}25"), (0.3, "0{,}3"), (0.35, "0{,}35")],
    [25000, 50000, 75000, 100000], [r"25\,000", r"50\,000", r"75\,000", r"100\,000"], 100000,
    r"$P_T(M) \approx 0{,}279$", r"fréquence", largeur=5.4)


# ================================================================ EXERCICES
# ---- nouveau-1 : tableau croisé (salle de sport)
_n1 = [(r"$A$", [("120", True), ("80", False), ("200", True)]),
       (r"$\overline{A}$", [("105", False), ("195", True), ("300", False)]),
       ("Total", [("225", False), ("275", False), ("500", True)])]
FIGURES["n1_tableau"] = tableau([r"$M$", r"$\overline{M}$", "Total"], _n1)

# ---- nouveau-3 : lire et compléter un arbre (internes, sport)
paire("n3_arbre", "nouveau-3", lambda: binaire(
    "I", Fr(35, 100), bar("I"), Fr(65, 100),
    "S", Fr(6, 10), bar("S"), Fr(4, 10),
    "S", Fr(3, 10), bar("S"), Fr(7, 10), donnes=(0, 2, 4)), L=2.2, dy=1.0, ecarts={1: 0.4})

# ---- nouveau-2 : deux lancers francs
paire("n2_arbre", "nouveau-2", lambda: binaire(
    "R_1", Fr(7, 10), bar("R_1"), Fr(3, 10),
    "R_2", Fr(8, 10), bar("R_2"), Fr(2, 10),
    "R_2", Fr(6, 10), bar("R_2"), Fr(4, 10), donnes=(0, 2, 4)), L=2.2, dy=1.0, ecarts={1: 0.4})

_pts_l, _f_r2, _f_r1 = simulation_lancers(10000)
for _suf, _corr in (("_enonce", False), ("", True)):
    FIGURES["n2_frequence" + _suf] = courbe_frequence(
        _pts_l, 0.74, 0.6, 0.9, [(0.6, "0{,}6"), (0.7, "0{,}7"), (0.8, "0{,}8"), (0.9, "0{,}9")],
        [2500, 5000, 7500, 10000], [r"2\,500", r"5\,000", r"7\,500", r"10\,000"], 10000,
        r"$P(R_2) = 0{,}74$", r"fréquence de $R_2$", corrige=_corr, largeur=5.4)

# ---- 1302 : somme de deux dés
for _suf, _mode in (("_enonce", "enonce"), ("", "corrige")):
    FIGURES["ex1302_des" + _suf] = grille(
        6, lambda a, b: a + b, _mode, ombre=lambda a, b: a + b >= 9, cadre_ligne=6,
        legendes=[r"cases vertes : $S$ (somme $\geqslant 9$)", r"ligne encadrée : $D$ (dé rouge sur $6$)"])

# ---- 1303 : tableau de probabilités + arbre d'événements indépendants
_t1303 = [(r"$A$", [("0{,}2", True), ("0{,}2", False), ("0{,}4", True)]),
          (r"$\overline{A}$", [("0{,}3", False), ("0{,}3", False), ("0{,}6", False)]),
          ("Total", [("0{,}5", True), ("0{,}5", False), ("1", True)])]
FIGURES["ex1303_tableau"] = tableau([r"$B$", r"$\overline{B}$", "Total"], _t1303)
paire("ex1303_arbre", "1303", lambda: binaire(
    "A", Fr(1, 2), bar("A"), Fr(1, 2),
    "B", Fr(4, 10), bar("B"), Fr(6, 10),
    "B", Fr(4, 10), bar("B"), Fr(6, 10), donnes=(0,)), L=2.2, dy=1.0, ecarts={1: 0.4})

# ---- 1310 : deux détecteurs indépendants
paire("ex1310_arbre", "1310", lambda: binaire(
    "D_1", Fr(9, 10), bar("D_1"), Fr(1, 10),
    "D_2", Fr(8, 10), bar("D_2"), Fr(2, 10),
    "D_2", Fr(8, 10), bar("D_2"), Fr(2, 10), donnes=(0,)), L=2.2, dy=1.0, ecarts={1: 0.4})

# ---- 1309 : commandes en ligne
paire("ex1309_arbre", "1309", lambda: binaire(
    "T", Fr(4, 10), bar("T"), Fr(6, 10),
    "R", Fr(15, 100), bar("R"), Fr(85, 100),
    "R", Fr(5, 100), bar("R"), Fr(95, 100), donnes=(0, 2, 4)), L=2.2, dy=1.0, ecarts={1: 0.4})


# ---- 1311 : trois chaînes de production
def _t1311():
    return [N(c, p, N("D", q, donne=True), N(bar("D"), 1 - q, donne=False))
            for c, p, q in (("A", Fr(5, 10), Fr(1, 100)), ("B", Fr(3, 10), Fr(2, 100)), ("C", Fr(2, 10), Fr(4, 100)))]


paire("ex1311_arbre", "1311", _t1311, L=2.2, dy=0.9, ecarts={1: 0.4})
_q = Fr(19, 1000)
# dans l'énoncé de la partie B, aucune valeur n'est sur l'arbre (toutes à trouver)
FIGURES["ex1311_deux_enonce"] = arbre(binaire(
    "D_1", _q, bar("D_1"), 1 - _q, "D_2", _q, bar("D_2"), 1 - _q, "D_2", _q, bar("D_2"), 1 - _q),
    "enonce", L=2.0, dy=1.0, ecarts={1: 0.4})
FIGURES["ex1311_deux"] = arbre(binaire(
    "D_1", _q, bar("D_1"), 1 - _q, "D_2", _q, bar("D_2"), 1 - _q, "D_2", _q, bar("D_2"), 1 - _q),
    "corrige", L=2.0, dy=1.0, ecarts={1: 0.4})

# ---- 1308 : urne 3 R, 2 B, sans remise
paire("ex1308_arbre", "1308", lambda: binaire(
    "R_1", Fr(3, 5), "B_1", Fr(2, 5), "R_2", Fr(2, 4), "B_2", Fr(2, 4), "R_2", Fr(3, 4), "B_2", Fr(1, 4)),
    nombres="f", L=2.2, dy=1.2, ecarts={1: 0.45})

# ---- 1305 : dépistage, prévalence 1 % puis 20 %
paire("ex1305_arbre", "1305", lambda: binaire(
    "M", Fr(1, 100), bar("M"), Fr(99, 100),
    "T", Fr(98, 100), bar("T"), Fr(2, 100),
    "T", Fr(3, 100), bar("T"), Fr(97, 100), donnes=(0, 2, 5)), L=2.2, dy=1.0, ecarts={1: 0.4})
paire("ex1305_arbre_c", "1305", lambda: binaire(
    "M", Fr(2, 10), bar("M"), Fr(8, 10),
    "T", Fr(98, 100), bar("T"), Fr(2, 100),
    "T", Fr(3, 100), bar("T"), Fr(97, 100), donnes=(0, 2, 5)), L=2.2, dy=1.0, ecarts={1: 0.4})
_t1305 = [(r"$M$", [(r"980", False), (r"20", False), (r"1\,000", False)]),
          (r"$\overline{M}$", [(r"2\,970", False), (r"96\,030", False), (r"99\,000", False)]),
          ("Total", [(r"3\,950", False), (r"96\,050", False), (r"100\,000", True)])]
FIGURES["ex1305_tableau"] = tableau([r"$T$", r"$\overline{T}$", "Total"], _t1305, l0=1.3, l=1.75)


# ---- 1304 : trajets (vélo, bus, à pied) et retards
def _t1304():
    # P(A) = 0,2 n'est pas écrit dans l'énoncé (« les autres à pied ») : valeur à trouver
    return [N(c, p, N("R", q, donne=True), N(bar("R"), 1 - q, donne=False), donne=(c != "A"))
            for c, p, q in (("V", Fr(45, 100), Fr(4, 100)), ("B", Fr(35, 100), Fr(12, 100)),
                            ("A", Fr(2, 10), Fr(6, 100)))]


paire("ex1304_arbre", "1304", _t1304, L=2.2, dy=0.9, ecarts={1: 0.4})

# ---- 1306 : 5 R, 3 B, sans puis avec remise
paire("ex1306_sans", "1306", lambda: binaire(
    "R_1", Fr(5, 8), "B_1", Fr(3, 8), "R_2", Fr(4, 7), "B_2", Fr(3, 7), "R_2", Fr(5, 7), "B_2", Fr(2, 7)),
    nombres="f", L=2.2, dy=1.2, ecarts={1: 0.45})
paire("ex1306_avec", "1306", lambda: binaire(
    "R_1", Fr(5, 8), "B_1", Fr(3, 8), "R_2", Fr(5, 8), "B_2", Fr(3, 8), "R_2", Fr(5, 8), "B_2", Fr(3, 8)),
    nombres="f", L=2.2, dy=1.2, ecarts={1: 0.45})

# ---- 1307 : jetons 1 à 4, avec remise
for _suf, _mode in (("_enonce", "enonce"), ("", "corrige")):
    FIGURES["ex1307_somme" + _suf] = grille(
        4, lambda a, b: a + b, _mode, ombre=lambda a, b: a + b == 5,
        cadres=[(k, k) for k in range(1, 5)], c=0.8, titre_l="premier jeton", titre_c="second jeton",
        legendes=[r"cases vertes : somme égale à $5$", r"cases encadrées : numéros identiques"])
paire("ex1307_parite", "1307", lambda: binaire(
    "A", Fr(1, 2), bar("A"), Fr(1, 2), "B", Fr(1, 2), bar("B"), Fr(1, 2), "B", Fr(1, 2), bar("B"), Fr(1, 2)),
    nombres="f", L=2.2, dy=1.2, ecarts={1: 0.45})

# ---- 1312 : DS
_t1312 = [(r"$C$", [("168", True), ("112", False), ("280", True)]),
          (r"$\overline{C}$", [("72", False), ("48", False), ("120", False)]),
          ("Total", [("240", True), ("160", False), ("400", True)])]
FIGURES["ex1312_tableau"] = tableau([r"$B$", r"$\overline{B}$", "Total"], _t1312)
paire("ex1312_arbre", "1312", lambda: binaire(
    "M_1", Fr(6, 10), "M_2", Fr(4, 10),
    "D", Fr(1, 100), bar("D"), Fr(99, 100),
    "D", Fr(3, 100), bar("D"), Fr(97, 100), donnes=(0, 2, 4)), L=2.2, dy=1.0, ecarts={1: 0.4})
_q2 = Fr(18, 1000)
FIGURES["ex1312_deux_enonce"] = arbre(binaire(
    "D_1", _q2, bar("D_1"), 1 - _q2, "D_2", _q2, bar("D_2"), 1 - _q2, "D_2", _q2, bar("D_2"), 1 - _q2),
    "enonce", L=2.0, dy=1.0, ecarts={1: 0.4})
FIGURES["ex1312_deux"] = arbre(binaire(
    "D_1", _q2, bar("D_1"), 1 - _q2, "D_2", _q2, bar("D_2"), 1 - _q2, "D_2", _q2, bar("D_2"), 1 - _q2),
    "corrige", L=2.0, dy=1.0, ecarts={1: 0.4})
