# -*- coding: utf-8 -*-
"""Figures de la notion « Modéliser le hasard, calculer des probabilités » (Seconde).

Compilation (style des livres OptiTAB, contrôle des chevauchements) :

    python ../../../outils/figures_livre.py <dossier_notion> [nom …] [--planche]

Programme de Seconde : arbres de DÉNOMBREMENT (pas de probabilités sur les
branches, réservées aux arbres pondérés de Première), diagrammes de Venn,
diagramme des fréquences observées. Moteur d'arbre repris de la notion
Terminale 179 : coordonnées calculées en Python, issues écrites à droite des
feuilles, jamais sur un trait ; chemins de la réponse en vert (otGreenDark).
Toutes les valeurs sont vérifiées par ../verif_probas.py.
"""
from itertools import permutations

PREAMBULE_EXTRA = r"""
\tikzset{
  evt/.style={font=\normalsize, text=otNavy, inner sep=2.4pt},
  evtV/.style={evt, text=otGreenDark},
  branche/.style={otNavy!65, line width=0.8pt, line cap=round},
  brancheV/.style={otGreenDark, line width=1.6pt, line cap=round},
  issue/.style={font=\small, text=otMuted, anchor=west, inner sep=1.5pt},
  issueV/.style={issue, text=otGreenDark},
  racine/.style={fill=otNavy},
  ensemble/.style={line width=1pt},
  cadre/.style={otInk!80, line width=0.8pt},
  region/.style={font=\normalsize, text=otInk},
  titreCol/.style={font=\otRegular\fontsize{8.5}{10}\selectfont, text=otMuted, anchor=south},
}
"""


# ---------------------------------------------------------------- arbres
def N(nom, *enfants, droite=None, vert=False):
    """Nœud d'arbre de dénombrement : nom (LaTeX, sans $), sous-arbres ;
    pour une feuille, texte « droite » (l'issue) et vert=True pour la mettre en évidence."""
    return {"nom": nom, "enfants": list(enfants), "droite": droite, "vert": vert}


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


def arbre(enfants, L=2.0, dy=0.8, ecarts=None, titres=None, ecart_droite="4pt"):
    """Arbre de dénombrement horizontal (racine à gauche).
    titres : textes placés au-dessus de chaque niveau (« 1er lancer »…)."""
    racine = {"nom": None, "enfants": enfants, "droite": None, "vert": False}
    _vert(racine)
    _placer(racine, 0, 0.0, dy, ecarts or {}, L)
    lignes = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    noeuds, aretes, droites = [], [], []
    compteur = [0]

    def visiter(n, parent_ref):
        for c in n["enfants"]:
            compteur[0] += 1
            nom = f"n{compteur[0]}"
            style = "evtV" if c["vert"] else "evt"
            noeuds.append(rf"\node[{style}] ({nom}) at ({c['x']:.3f},{c['y']:.3f}) {{${c['nom']}$}};")
            st = "brancheV" if c["vert"] else "branche"
            aretes.append((st, rf"\draw[{st}] {parent_ref} -- ({nom}.west);"))
            if not c["enfants"] and c["droite"]:
                si = "issueV" if c["vert"] else "issue"
                droites.append(rf"\node[{si}] at ([xshift={ecart_droite}]{nom}.east) {{{c['droite']}}};")
            visiter(c, f"({nom}.east)")

    lignes.append(rf"\coordinate (r) at (0,{racine['y']:.3f});")
    visiter(racine, "(r)")
    lignes += noeuds
    lignes += [a for s, a in aretes if s == "branche"] + [a for s, a in aretes if s == "brancheV"]
    lignes.append(r"\fill[racine] (r) circle (1.9pt);")
    lignes += droites
    if titres:
        haut = max(_tous_y(racine)) + 0.45
        for k, t in enumerate(titres, start=1):
            lignes.append(rf"\node[titreCol] at ({k * L:.3f},{haut:.3f}) {{{t}}};")
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


def _tous_y(n):
    ys = [n["y"]]
    for c in n["enfants"]:
        ys += _tous_y(c)
    return ys


def pieces(n, verts=()):
    """n lancers d'une pièce : arbre P / F, issue écrite à droite (« PFP »)."""
    def sous(prefixe, k):
        enfants = []
        for e in "PF":
            issue = prefixe + e
            if k == n:
                txt = "$(" + r"\,;".join(issue) + ")$"
                enfants.append(N(e, droite=txt, vert=issue in verts))
            else:
                enfants.append(N(e, *sous(issue, k + 1)))
        return enfants
    return sous("", 1)


FIGURES = {}

# ================================================================ COURS
# Diagramme de Venn : A, B et leur intersection (en vert)
FIGURES["cours_venn"] = r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \begin{scope}
    \clip (-0.75,0) circle (1.45);
    \fill[otGreen!30] (0.75,0) circle (1.45);
  \end{scope}
  \draw[cadre] (-3.3,-1.85) rectangle (3.3,1.85);
  \draw[ensemble,otNavy] (-0.75,0) circle (1.45);
  \draw[ensemble,otOrange!85!black] (0.75,0) circle (1.45);
  \node[region,text=otNavy] at (-1.5,0) {$A$};
  \node[region,text=otOrange!85!black] at (1.5,0) {$B$};
  \node[region,text=otGreenDark] at (0,0) {$A\cap B$};
  \node[region,text=otMuted,anchor=north west] at (-3.2,1.75) {$\Omega$};
\end{tikzpicture}"""

# Contraire (gauche) et événements incompatibles (droite)
FIGURES["cours_contraire_incompatibles"] = r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  % --- contraire
  \fill[otGreen!25] (0,0) rectangle (4.1,3);
  \fill[white] (1.75,1.5) circle (1.0);
  \draw[cadre] (0,0) rectangle (4.1,3);
  \draw[ensemble,otNavy] (1.75,1.5) circle (1.0);
  \node[region,text=otNavy] at (1.75,1.5) {$A$};
  \node[region,text=otGreenDark] at (3.35,0.55) {$\overline{A}$};
  \node[region,text=otMuted,anchor=north west] at (0.08,2.92) {$\Omega$};
  \node[note,anchor=north] at (2.05,-0.12) {$A$ et son contraire $\overline{A}$};
  % --- incompatibles
  \begin{scope}[xshift=4.8cm]
    \draw[cadre] (0,0) rectangle (4.1,3);
    \draw[ensemble,otNavy] (1.1,1.35) circle (0.8);
    \draw[ensemble,otOrange!85!black] (3.0,1.35) circle (0.8);
    \node[region,text=otNavy] at (1.1,1.35) {$A$};
    \node[region,text=otOrange!85!black] at (3.0,1.35) {$B$};
    \node[region,text=otMuted,anchor=north west] at (0.08,2.92) {$\Omega$};
    \node[note,anchor=north] at (2.05,-0.12) {$A\cap B=\varnothing$ : incompatibles};
  \end{scope}
\end{tikzpicture}"""

# Deux lancers d'une pièce : arbre de dénombrement
FIGURES["cours_arbre_pieces"] = arbre(pieces(2), L=2.0, dy=0.85, ecarts={1: 0.25},
                                      titres=[r"1\textsuperscript{er} lancer", r"2\textsuperscript{e} lancer"])

# ================================================================ EXERCICES
# 1999 : deux tirages sans remise, jetons numérotés R1, R2, B1, B2, B3
_jetons = ["R_1", "R_2", "B_1", "B_2", "B_3"]


def _sans_remise():
    enfants = []
    for a in _jetons:
        feuilles = [N(b, droite=rf"${a[0]}{b[0]}$") for b in _jetons if b != a]
        enfants.append(N(a, *feuilles))
    return enfants


FIGURES["e1999_arbre"] = arbre(_sans_remise(), L=1.9, dy=0.5, ecarts={1: 0.3},
                               titres=[r"1\textsuperscript{er} jeton", r"2\textsuperscript{e} jeton"])

# 1997 : diagramme de Venn des effectifs (Espagnol S, Allemand G)
FIGURES["e1997_venn"] = r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \begin{scope}
    \clip (-0.8,0) circle (1.5);
    \fill[otGreen!30] (0.8,0) circle (1.5);
  \end{scope}
  \draw[cadre] (-3.4,-1.9) rectangle (3.4,1.9);
  \draw[ensemble,otNavy] (-0.8,0) circle (1.5);
  \draw[ensemble,otOrange!85!black] (0.8,0) circle (1.5);
  \node[region,text=otNavy,anchor=south] at (-2.05,1.22) {$S$};
  \node[region,text=otOrange!85!black,anchor=south] at (2.05,1.22) {$G$};
  \node[region] at (-1.55,0) {$32$};
  \node[region,text=otGreenDark] at (0,0) {$20$};
  \node[region] at (1.55,0) {$28$};
  \node[region] at (2.75,-1.45) {$40$};
\end{tikzpicture}"""

# 2003 : trois lancers d'une pièce
FIGURES["e2003_arbre"] = arbre(pieces(3), L=1.7, dy=0.62, ecarts={1: 0.2, 2: 0.1},
                               titres=[r"1\textsuperscript{er} lancer", r"2\textsuperscript{e} lancer", r"3\textsuperscript{e} lancer"])
FIGURES["e2003_deux_pile"] = arbre(pieces(3, verts={"PPF", "PFP", "FPP"}), L=1.7, dy=0.62,
                                   ecarts={1: 0.2, 2: 0.1},
                                   titres=[r"1\textsuperscript{er} lancer", r"2\textsuperscript{e} lancer", r"3\textsuperscript{e} lancer"])

# ================================================================ FINITION 2026-11-02
# Styles communs aux nouvelles figures (mêmes graduations que les diagrammes de la notion 174).
STY = (r"\tikzset{grad/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt},"
       r"valeur/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otInk,inner sep=1.2pt,fill=white},"
       r"axe/.style={otMuted,line width=.6pt},tic/.style={otMuted,line width=.5pt}}")


def fr(x, dec=None):
    s = (f"{x:.{dec}f}" if dec is not None else "%g" % x)
    return s.replace(".", "{,}")


# nouveau-1 (3754) : fréquences observées du dé truqué et repère 1/6 (refaite : style des diagrammes)
def barres_frequences(faces, freqs, ref, dx=1.0, uy=9.0):
    L = [r"\begin{tikzpicture}", STY]
    haut = 0.45
    for v in (0.1, 0.2, 0.3, 0.4):
        L.append(r"\draw[otRule,line width=.35pt] (0,%.3f) -- (%.3f,%.3f);" % (v * uy, (len(faces) + 0.4) * dx, v * uy))
    for v in (0, 0.1, 0.2, 0.3, 0.4):
        L.append(r"\draw[tic] (0,%.3f) -- (-0.09,%.3f);" % (v * uy, v * uy))
        L.append(r"\node[grad,anchor=east] at (-0.13,%.3f) {%s};" % (v * uy, fr(v)))
    for i, (f, q) in enumerate(zip(faces, freqs)):
        X = (i + 0.75) * dx
        L.append(r"\draw[fill=otNavy!22,draw=otNavy,line width=.7pt] (%.3f,0) rectangle (%.3f,%.3f);" % (X - 0.3, X + 0.3, q * uy))
        L.append(r"\node[grad,anchor=north] at (%.3f,-0.13) {%s};" % (X, f))
    xr = (len(faces) + 0.4) * dx
    L.append(r"\draw[seuil] (0,%.4f) -- (%.3f,%.4f);" % (ref * uy, xr, ref * uy))
    L.append(r"\node[anchor=west,text=otOrange!85!black,inner sep=1.5pt] at (%.3f,%.4f) {$\frac{1}{6} \approx 0{,}17$};" % (xr + 0.05, ref * uy))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (haut * uy + 0.35))
    L.append(r"\draw[axe] (0,0) -- (%.3f,0);" % xr)
    L.append(r"\node[grad,anchor=south west] at (0.08,%.3f) {Fréquence};" % (haut * uy + 0.4))
    L.append(r"\node[grad,anchor=north east] at (%.3f,-0.55) {Face};" % xr)
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["n1_frequences"] = barres_frequences([1, 2, 3, 4, 5, 6], [0.12, 0.11, 0.13, 0.115, 0.125, 0.4], 1 / 6)


# Tableau à double entrée dessiné : cases favorables en vert
def grille(lignes, colonnes, f, verts, nom_l, nom_c, w=0.95, h=0.62):
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


DE4, DE6 = [1, 2, 3, 4], [1, 2, 3, 4, 5, 6]
FIGURES["e1998_somme8"] = grille(DE4, DE6, lambda a, b: a + b,
                                 {(a, b) for a in DE4 for b in DE6 if a + b >= 8},
                                 r"dé à $4$ faces : $a$", r"dé à $6$ faces : $b$")
FIGURES["e1998_un1"] = grille(DE4, DE6, lambda a, b: a + b,
                              {(a, b) for a in DE4 for b in DE6 if a == 1 or b == 1},
                              r"dé à $4$ faces : $a$", r"dé à $6$ faces : $b$")
FIGURES["cours_au_moins_un6"] = grille(DE6, DE6, lambda a, b: a + b,
                                       {(a, b) for a in DE6 for b in DE6 if a == 6 or b == 6},
                                       r"premier dé", r"second dé", w=0.82, h=0.56)

# 1994 : diagramme de Venn des trois événements, nombres de 1 à 15 placés
FIGURES["e1994_venn"] = r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \draw[cadre] (-3.6,-3.0) rectangle (3.6,2.55);
  \draw[ensemble,otNavy] (-0.85,0.35) circle (1.5);
  \draw[ensemble,otOrange!85!black] (0.85,0.35) circle (1.5);
  \draw[ensemble,otGreenDark] (0,-1.05) circle (1.5);
  \node[region,text=otNavy] at (-2.1,1.75) {$A$};
  \node[region,text=otOrange!85!black] at (2.1,1.75) {$B$};
  \node[region,text=otGreenDark] at (1.75,-2.35) {$C$};
  \node[region,text=otMuted,anchor=north west] at (-3.5,2.45) {$\Omega$};
  % A seul, B seul, C seul
  \node[region] at (-1.55,0.75) {$6$};
  \node[region] at (1.55,0.95) {$1$};
  \node[region] at (1.95,0.35) {$5$};
  \node[region] at (1.6,-0.2) {$7$};
  \node[region] at (-0.45,-1.95) {$10$};
  \node[region] at (0.45,-1.95) {$14$};
  % A et B seulement, A et C seulement, B et C seulement, les trois
  \node[region] at (-0.25,0.95) {$3$};
  \node[region] at (0.25,0.95) {$9$};
  \node[region] at (-0.8,-0.6) {$12$};
  \node[region] at (1.0,-0.3) {$11$};
  \node[region] at (0.6,-0.85) {$13$};
  \node[region] at (0,0.0) {$15$};
  % hors des trois
  \node[region] at (-3.0,-1.5) {$2$};
  \node[region] at (-3.0,-2.3) {$4$};
  \node[region] at (2.95,-0.9) {$8$};
\end{tikzpicture}"""

# 1996 : la roue dessinée à l'échelle (angles proportionnels aux probabilités)
def roue():
    probs = [("1", 0.12), ("2", 0.35), ("3", 0.28), ("4", 0.25)]
    couleurs = ["otNavy!25", "otOrange!30", "otSky", "otGreen!35"]
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    a = 90.0
    R = 1.75
    for (num, p), col in zip(probs, couleurs):
        b = a - 360 * p
        L.append(r"\fill[%s] (0,0) -- (%.2f:%.2f) arc[start angle=%.2f,end angle=%.2f,radius=%.2f] -- cycle;" % (col, a, R, a, b, R))
        L.append(r"\draw[otNavy,line width=.8pt] (0,0) -- (%.2f:%.2f);" % (a, R))
        m = (a + b) / 2
        L.append(r"\node[text=otNavy,font=\large] at (%.2f:%.2f) {$%s$};" % (m, 0.62 * R, num))
        txt = (r"$p = 0{,}25$" if num == "4" else "$" + fr(p) + "$")
        col_t = "otGreenDark" if num == "4" else "otInk"
        anc = "west" if (m % 360) < 90 or (m % 360) > 270 else "east"
        L.append(r"\node[text=%s,anchor=%s,inner sep=2pt] at (%.2f:%.2f) {%s};" % (col_t, anc, m, R + 0.12, txt))
        a = b
    L.append(r"\draw[otNavy,line width=1pt] (0,0) circle (%.2f);" % R)
    L.append(r"\fill[otNavy] (0,0) circle (1.6pt);")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["e1996_roue"] = roue()


# 2000 : les deux fréquences et la probabilité 0,5 sur un axe
def axe_frequences():
    a, b, u = 0.40, 0.70, 26.0
    X = lambda v: (v - a) * u
    L = [r"\begin{tikzpicture}", STY]
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (%.3f,0);" % (X(b) + 0.4))
    v = a
    while v <= b + 1e-9:
        L.append(r"\draw[tic] (%.3f,0) -- (%.3f,-0.09);" % (X(v), X(v)))
        L.append(r"\node[grad,anchor=north] at (%.3f,-0.13) {%s};" % (X(v), fr(round(v, 2))))
        v += 0.05
    L.append(r"\draw[seuil] (%.3f,-0.05) -- (%.3f,1.75);" % (X(0.5), X(0.5)))
    L.append(r"\node[anchor=south,text=otOrange!85!black,inner sep=1.5pt] at (%.3f,1.78) {modèle : $p = 0{,}5$};" % X(0.5))
    for f, y, nom, col, e in ((0.54, 0.55, "B", "otGreenDark", "0{,}04"), (0.65, 1.15, "A", "otNavy", "0{,}15")):
        L.append(r"\fill[%s] (%.3f,0) circle (2.6pt);" % (col, X(f)))
        L.append(r"\draw[%s,line width=.5pt,dash pattern=on 1.5pt off 1.5pt] (%.3f,0.1) -- (%.3f,%.3f);" % (col, X(f), X(f), y))
        L.append(r"\draw[%s,line width=.8pt,{Stealth[length=1.6mm]}-{Stealth[length=1.6mm]}] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, X(0.5), y, X(f), y))
        if f - 0.5 > 0.08:
            L.append(r"\node[anchor=south,text=%s,inner sep=1.5pt,font=\small] at (%.3f,%.3f) {écart $%s$};" % (col, (X(0.5) + X(f)) / 2, y + 0.03, e))
        else:
            L.append(r"\node[anchor=east,text=%s,inner sep=1.5pt,font=\small] at (%.3f,%.3f) {écart $%s$};" % (col, X(0.5) - 0.08, y, e))
        L.append(r"\node[anchor=west,text=%s,inner sep=2pt] at (%.3f,%.3f) {$f_%s = %s$};" % (col, X(f) + 0.05, y, nom, fr(f)))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


FIGURES["e2000_axe"] = axe_frequences()

# 3755 : diagramme de Venn des effectifs (F : filles, D : demi-pensionnaires)
FIGURES["e3755_venn"] = r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \begin{scope}
    \clip (-0.8,0) circle (1.5);
    \fill[otGreen!30] (0.8,0) circle (1.5);
  \end{scope}
  \draw[cadre] (-3.4,-1.9) rectangle (3.4,1.9);
  \draw[ensemble,otNavy] (-0.8,0) circle (1.5);
  \draw[ensemble,otOrange!85!black] (0.8,0) circle (1.5);
  \node[region,text=otNavy,anchor=south] at (-2.05,1.22) {$F$};
  \node[region,text=otOrange!85!black,anchor=south] at (2.05,1.22) {$D$};
  \node[region] at (-1.55,0) {$46$};
  \node[region,text=otGreenDark] at (0,0) {$84$};
  \node[region] at (1.55,0) {$66$};
  \node[region] at (2.75,-1.45) {$54$};
  \node[region,text=otMuted,anchor=north west] at (-3.3,1.8) {$\Omega$};
\end{tikzpicture}"""
