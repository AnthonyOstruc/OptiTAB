# -*- coding: utf-8 -*-
"""Figures de la notion 174 (Seconde : information chiffrée et statistique descriptive).

Style des livres OptiTAB ; compiler avec outils/figures_livre.py.
Les diagrammes (histogrammes, bâtons, boîtes, nuages de points, chaînes
d'évolutions, arbres d'effectifs) sont produits par de petits générateurs
Python pour que les valeurs soient exactement celles des énoncés ; les mêmes
données sont contrôlées par ../verif_174.py.

Finition du 2026-11-02 : étiquettes des effectifs sur fond blanc (elles étaient
coupées par les lignes du quadrillage), noms des séries à gauche des boîtes,
nouvelles figures dans les corrigés.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  grad/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt},
  valeur/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otInk,inner sep=1.2pt,fill=white},
  axe/.style={otMuted,line width=.6pt},
  tic/.style={otMuted,line width=.5pt},
  barre/.style={fill=otNavy!22,draw=otNavy,line width=.7pt},
  boite/.style={fill=otSky,draw=otNavy,line width=.9pt},
  boite2/.style={fill=otGreen!15,draw=otGreenDark,line width=.9pt},
  case/.style={draw=otNavy,fill=otSky,line width=.9pt,rounded corners=3pt,minimum width=1.25cm,minimum height=.75cm,inner xsep=4pt},
  caseV/.style={case,draw=otGreenDark,fill=otGreen!12},
}
"""


def nb(x, dec=None):
    """Nombre au format français (virgule décimale, espace des milliers)."""
    if dec is not None:
        s = f"{x:.{dec}f}"
    else:
        s = "%g" % x if abs(x) < 1e6 else str(int(x))
    ent, _, fr = s.partition(".")
    signe = ""
    if ent.startswith("-"):
        signe, ent = "-", ent[1:]
    if len(ent) > 3:
        ent = ent[:-3] + r"\," + ent[-3:]
    return ("−" if signe else "") + ent + ("{,}" + fr if fr else "")


def axe_gradue(y, a, b, pas_tic, pas_num, u, ox=0.0, fleche=0.45, sauf=()):
    """Axe horizontal de a à b (unité u cm), graduations et nombres sous l'axe."""
    out = [r"\draw[axe,-{Stealth[length=2mm]}] (%.3f,%.3f) -- (%.3f,%.3f);"
           % (ox, y, ox + (b - a) * u + fleche, y)]
    v = a
    while v <= b + 1e-9:
        x = ox + (v - a) * u
        out.append(r"\draw[tic] (%.3f,%.3f) -- (%.3f,%.3f);" % (x, y, x, y - 0.09))
        if abs((v - a) / pas_num - round((v - a) / pas_num)) < 1e-9 and all(abs(v - w) > 1e-9 for w in sauf):
            out.append(r"\node[grad,anchor=north] at (%.3f,%.3f) {%s};" % (x, y - 0.13, nb(round(v, 6))))
        v += pas_tic
    return out


# ---------------------------------------------------------------- histogrammes, bâtons
def histogramme(bornes, effectifs, ux, uy, pas_y, titre_x, titre_y):
    """Histogramme à classes de même amplitude ; effectif écrit au-dessus de chaque rectangle."""
    a = bornes[0]
    L = [r"\begin{tikzpicture}"]
    ymax = max(effectifs)
    haut = (ymax // pas_y + 1) * pas_y
    largeur = (bornes[-1] - a) * ux
    v = pas_y
    while v <= haut:
        L.append(r"\draw[otRule,line width=.35pt] (0,%.3f) -- (%.3f,%.3f);" % (v * uy, largeur + 0.2, v * uy))
        v += pas_y
    v = 0
    while v <= haut:
        L.append(r"\draw[tic] (0,%.3f) -- (-0.09,%.3f);" % (v * uy, v * uy))
        L.append(r"\node[grad,anchor=east] at (-0.13,%.3f) {%s};" % (v * uy, nb(v)))
        v += pas_y
    for i, e in enumerate(effectifs):
        x0 = (bornes[i] - a) * ux
        x1 = (bornes[i + 1] - a) * ux
        L.append(r"\draw[barre] (%.3f,0) rectangle (%.3f,%.3f);" % (x0, x1, e * uy))
    for i, e in enumerate(effectifs):
        x0 = (bornes[i] - a) * ux
        x1 = (bornes[i + 1] - a) * ux
        L.append(r"\node[valeur,anchor=south] at (%.3f,%.3f) {%s};" % ((x0 + x1) / 2, e * uy + 0.05, nb(e)))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (haut * uy + 0.45))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (%.3f,0);" % (largeur + 0.55))
    for b in bornes:
        x = (b - a) * ux
        L.append(r"\draw[tic] (%.3f,0) -- (%.3f,-0.09);" % (x, x))
        L.append(r"\node[grad,anchor=north] at (%.3f,-0.13) {%s};" % (x, nb(b)))
    L.append(r"\node[grad,anchor=south west] at (0.08,%.3f) {%s};" % (haut * uy + 0.5, titre_y))
    L.append(r"\node[grad,anchor=north east] at (%.3f,-0.55) {%s};" % (largeur + 0.55, titre_x))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def batons(valeurs, effectifs, dx, uy, pas_y, titre_x, titre_y):
    """Diagramme en bâtons : un bâton par valeur (abscisses régulièrement espacées)."""
    L = [r"\begin{tikzpicture}"]
    haut = (max(effectifs) // pas_y + 1) * pas_y
    n = len(valeurs)
    largeur = (n + 0.2) * dx
    v = pas_y
    while v <= haut:
        L.append(r"\draw[otRule,line width=.35pt] (0,%.3f) -- (%.3f,%.3f);" % (v * uy, largeur, v * uy))
        v += pas_y
    v = 0
    while v <= haut:
        L.append(r"\draw[tic] (0,%.3f) -- (-0.09,%.3f);" % (v * uy, v * uy))
        L.append(r"\node[grad,anchor=east] at (-0.13,%.3f) {%s};" % (v * uy, nb(v)))
        v += pas_y
    for i, (x, e) in enumerate(zip(valeurs, effectifs)):
        X = (i + 0.7) * dx
        L.append(r"\draw[otNavy,line width=3.2pt] (%.3f,0) -- (%.3f,%.3f);" % (X, X, e * uy))
        L.append(r"\node[valeur,anchor=south] at (%.3f,%.3f) {%s};" % (X, e * uy + 0.05, nb(e)))
        L.append(r"\node[grad,anchor=north] at (%.3f,-0.13) {%s};" % (X, nb(x)))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (haut * uy + 0.45))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (%.3f,0);" % (largeur + 0.3))
    L.append(r"\node[grad,anchor=south west] at (0.08,%.3f) {%s};" % (haut * uy + 0.5, titre_y))
    L.append(r"\node[grad,anchor=north east] at (%.3f,-0.55) {%s};" % (largeur + 0.3, titre_x))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ---------------------------------------------------------------- boîtes
def boites(series, a, b, u, pas_tic, pas_num, titre_x, ecart=1.0, marge=1.55):
    """Diagrammes en boîte horizontaux ; series = [(nom, min, Q1, Me, Q3, max)], de haut en bas.
    Le nom de chaque série est écrit à gauche de l'axe, en face de sa boîte."""
    L = [r"\begin{tikzpicture}"]
    ox = marge
    k = len(series)
    for j, (nom, mn, q1, me, q3, mx) in enumerate(series):
        y = (k - j) * ecart - 0.1
        st = "boite" if j % 2 == 0 else "boite2"
        col = "otNavy" if j % 2 == 0 else "otGreenDark"
        X = lambda v: ox + (v - a) * u
        L.append(r"\draw[%s,line width=.9pt] (%.3f,%.3f) -- (%.3f,%.3f) (%.3f,%.3f) -- (%.3f,%.3f);"
                 % (col, X(mn), y, X(q1), y, X(q3), y, X(mx), y))
        L.append(r"\draw[%s,line width=.9pt] (%.3f,%.3f) -- (%.3f,%.3f) (%.3f,%.3f) -- (%.3f,%.3f);"
                 % (col, X(mn), y - 0.16, X(mn), y + 0.16, X(mx), y - 0.16, X(mx), y + 0.16))
        L.append(r"\draw[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (st, X(q1), y - 0.28, X(q3), y + 0.28))
        L.append(r"\draw[otOrange!85!black,line width=1.6pt] (%.3f,%.3f) -- (%.3f,%.3f);"
                 % (X(me), y - 0.28, X(me), y + 0.28))
        L.append(r"\node[anchor=east,inner sep=1pt,text=%s] at (%.3f,%.3f) {%s};"
                 % (col, ox + (min(mn, a + 0.0) - a) * u - 0.2, y, nom))
    L += axe_gradue(0, a, b, pas_tic, pas_num, u, ox)
    L.append(r"\node[grad,anchor=north east] at (%.3f,-0.55) {%s};" % (ox + (b - a) * u + 0.45, titre_x))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def boite_annotee(stats, a, b, u, pas_tic, pas_num, points=None, iqr=True, moyenne=None,
                  cote=None, titre_x=None):
    """Une boîte détaillée : min, Q1, Me, Q3, max nommés au-dessus ; points de la série
    (empilés) au-dessus ; écart interquartile (cote) sous l'axe.
    moyenne = (valeur, texte) : repère triangulaire sous l'axe.
    cote = (v1, v2, texte) : flèche de cote verte sous l'axe (remplace l'écart interquartile)."""
    mn, q1, me, q3, mx = stats
    X = lambda v: (v - a) * u
    L = [r"\begin{tikzpicture}"]
    L += axe_gradue(0, a, b, pas_tic, pas_num, u)
    if points:
        vus = {}
        for v in sorted(points):
            h = vus.get(v, 0)
            vus[v] = h + 1
            L.append(r"\fill[otNavy] (%.3f,%.3f) circle (2.2pt);" % (X(v), 2.05 + 0.21 * h))
    L.append(r"\draw[otNavy,line width=.9pt] (%.3f,0.85) -- (%.3f,0.85) (%.3f,0.85) -- (%.3f,0.85);"
             % (X(mn), X(q1), X(q3), X(mx)))
    L.append(r"\draw[otNavy,line width=.9pt] (%.3f,0.69) -- (%.3f,1.01) (%.3f,0.69) -- (%.3f,1.01);"
             % (X(mn), X(mn), X(mx), X(mx)))
    L.append(r"\draw[boite] (%.3f,0.55) rectangle (%.3f,1.15);" % (X(q1), X(q3)))
    L.append(r"\draw[otOrange!85!black,line width=1.6pt] (%.3f,0.55) -- (%.3f,1.15);" % (X(me), X(me)))
    L.append(r"\draw[guide] (%.3f,0.5) -- (%.3f,0.04) (%.3f,0.5) -- (%.3f,0.04) (%.3f,0.5) -- (%.3f,0.04);"
             % (X(q1), X(q1), X(me), X(me), X(q3), X(q3)))
    L.append(r"\node[anchor=south,inner sep=1pt,text=otMuted,font=\small] at (%.3f,1.08) {min};" % X(mn))
    L.append(r"\node[anchor=south,inner sep=1pt,text=otNavy] at (%.3f,1.2) {$Q_1$};" % X(q1))
    L.append(r"\node[anchor=south,inner sep=1pt,text=otOrange!85!black] at (%.3f,1.2) {$\mathrm{Me}$};" % X(me))
    L.append(r"\node[anchor=south,inner sep=1pt,text=otNavy] at (%.3f,1.2) {$Q_3$};" % X(q3))
    L.append(r"\node[anchor=south,inner sep=1pt,text=otMuted,font=\small] at (%.3f,1.08) {max};" % X(mx))
    y = -0.72
    if moyenne is not None:
        v, txt = moyenne
        L.append(r"\fill[otRed!85!black] (%.3f,-0.62) -- ++(-0.11,-0.17) -- ++(0.22,0) -- cycle;" % X(v))
        L.append(r"\node[anchor=north,inner sep=1pt,text=otRed!85!black] at (%.3f,-0.82) {%s};" % (X(v), txt))
        y = -1.45
    if cote is not None:
        v1, v2, txt = cote
        L.append(r"\draw[cote,otGreenDark] (%.3f,%.3f) -- (%.3f,%.3f);" % (X(v1), y, X(v2), y))
        L.append(r"\node[anchor=north,inner sep=1pt,text=otGreenDark] at (%.3f,%.3f) {%s};"
                 % ((X(v1) + X(v2)) / 2, y - 0.1, txt))
    elif iqr:
        L.append(r"\draw[cote] (%.3f,%.3f) -- (%.3f,%.3f);" % (X(q1), y, X(q3), y))
        L.append(r"\node[anchor=north,inner sep=1pt,text=otGreenDark] at (%.3f,%.3f) {écart interquartile : $Q_3 - Q_1 = %s$};"
                 % ((X(q1) + X(q3)) / 2, y - 0.1, nb(q3 - q1)))
    if titre_x:
        L.append(r"\node[grad,anchor=south east] at (%.3f,0.1) {%s};" % (X(b) + 0.45, titre_x))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ---------------------------------------------------------------- nuages de points
def points_empiles(rangs, a, b, u, pas_tic, pas_num, moyenne=None, legende_moyenne="", titre_gauche=False):
    """Nuages de points sur des axes parallèles ; rangs = [(titre, valeurs, couleur)], de haut en bas.
    Les valeurs égales sont empilées."""
    L = [r"\begin{tikzpicture}"]
    hauteur_rang = 2.15
    k = len(rangs)
    for j, (titre, valeurs, col) in enumerate(rangs):
        y = (k - 1 - j) * hauteur_rang
        L += axe_gradue(y, a, b, pas_tic, pas_num, u, sauf=(moyenne,) if moyenne is not None else ())
        vus = {}
        for v in sorted(valeurs):
            h = vus.get(v, 0)
            vus[v] = h + 1
            L.append(r"\fill[%s] (%.3f,%.3f) circle (2.4pt);" % (col, (v - a) * u, y + 0.2 + 0.2 * h))
        if titre_gauche:
            L.append(r"\node[anchor=south west,inner sep=1pt,text=%s] at (0,%.3f) {%s};" % (col, y + 0.95, titre))
        else:
            L.append(r"\node[anchor=south east,inner sep=1pt,text=%s] at (%.3f,%.3f) {%s};"
                     % (col, (b - a) * u + 0.45, y + 0.95, titre))
    if moyenne is not None:
        X = (moyenne - a) * u
        top = (k - 1) * hauteur_rang + 1.5
        L.append(r"\draw[otRed!85,line width=.8pt,dash pattern=on 3pt off 2pt] (%.3f,-0.62) -- (%.3f,%.3f);" % (X, X, top))
        L.append(r"\node[anchor=south,inner sep=1.5pt,text=otRed!85!black] at (%.3f,%.3f) {%s};" % (X, top + 0.03, legende_moyenne))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def nuage_intervalle(valeurs, a, b, u, pas_tic, pas_num, bas, haut, txt_bas, txt_haut, titre):
    """Valeurs (empilées) sur un axe ; intervalle [bas ; haut] en vert au-dessus ;
    les valeurs hors de l'intervalle sont en orange."""
    X = lambda v: (v - a) * u
    L = [r"\begin{tikzpicture}"]
    L += axe_gradue(0, a, b, pas_tic, pas_num, u)
    vus = {}
    hmax = 0
    for v in sorted(valeurs):
        h = vus.get(v, 0)
        vus[v] = h + 1
        hmax = max(hmax, h)
        col = "otNavy" if bas <= v <= haut else "otOrange!90!black"
        L.append(r"\fill[%s] (%.3f,%.3f) circle (2.4pt);" % (col, X(v), 0.22 + 0.21 * h))
    yb = 0.22 + 0.21 * hmax + 0.45
    L.append(r"\fill[otGreen!18] (%.3f,0.02) rectangle (%.3f,%.3f);" % (X(bas), X(haut), yb))
    L.append(r"\draw[otGreenDark,line width=1pt] (%.3f,0.02) -- (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,0.02);"
             % (X(bas), X(bas), yb, X(haut), yb, X(haut)))
    # les points sont redessinés par-dessus la zone verte
    vus = {}
    for v in sorted(valeurs):
        h = vus.get(v, 0)
        vus[v] = h + 1
        col = "otNavy" if bas <= v <= haut else "otOrange!90!black"
        L.append(r"\fill[%s] (%.3f,%.3f) circle (2.4pt);" % (col, X(v), 0.22 + 0.21 * h))
    L.append(r"\node[anchor=south,inner sep=1.2pt,text=otGreenDark] at (%.3f,%.3f) {%s};" % (X(bas), yb + 0.03, txt_bas))
    L.append(r"\node[anchor=south,inner sep=1.2pt,text=otGreenDark] at (%.3f,%.3f) {%s};" % (X(haut), yb + 0.03, txt_haut))
    L.append(r"\node[anchor=south,inner sep=1.2pt,text=otInk] at (%.3f,%.3f) {%s};" % ((X(bas) + X(haut)) / 2, yb + 0.55, titre))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ---------------------------------------------------------------- information chiffrée
def emboites(p1, p2, nom_E, nom_B, nom_A, conclusion, W=7.2, H=4.4):
    """Proportion de proportion, aires proportionnelles : B occupe p2 de E,
    A occupe p1 de B ; donc A occupe p1 × p2 de E."""
    wb = W * p2
    ha = H * p1
    L = [r"\begin{tikzpicture}"]
    L.append(r"\draw[otNavy,line width=1pt,fill=white] (0,0) rectangle (%.3f,%.3f);" % (W, H))
    L.append(r"\draw[otOrange!85!black,line width=1pt,fill=otOrange!10] (0,0) rectangle (%.3f,%.3f);" % (wb, H))
    L.append(r"\draw[otGreenDark,line width=1pt,fill=otGreen!28] (0,0) rectangle (%.3f,%.3f);" % (wb, ha))
    L.append(r"\node[anchor=north,text=otNavy,align=center,inner sep=2pt] at (%.3f,%.3f) {%s};" % ((wb + W) / 2, H - 0.12, nom_E))
    L.append(r"\node[anchor=north,text=otOrange!85!black,align=center,inner sep=2pt] at (%.3f,%.3f) {%s};" % (wb / 2, H - 0.12, nom_B))
    L.append(r"\node[text=otGreenDark,align=center,inner sep=1pt] at (%.3f,%.3f) {%s};" % (wb / 2, ha / 2, nom_A))
    L.append(r"\node[anchor=north,text=otInk,inner sep=2pt,align=center] at (%.3f,-0.15) {%s};" % (W / 2, conclusion))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def chaine(valeurs, coefs, taux, bilan, pas=3.3, couleurs=None, verte=None, retour=True, largeur_case=1.25):
    """Chaîne d'évolutions successives : cases (valeurs) reliées par des flèches ×CM ;
    taux sous chaque flèche ; arc de retour avec le coefficient global (bilan)."""
    n = len(valeurs)
    def _val(c):
        return c if isinstance(c, (int, float)) else float(c.replace("{,}", "."))
    couleurs = couleurs or ["otGreenDark" if _val(c) >= 1 else "otOrange!90!black" for c in coefs]
    L = [r"\begin{tikzpicture}"]
    for i, v in enumerate(valeurs):
        st = "caseV" if verte is not None and i in verte else "case"
        L.append(r"\node[%s,minimum width=%.2fcm] (c%d) at (%.3f,0) {$%s$};" % (st, largeur_case, i, i * pas, v))
    for i in range(n - 1):
        col = couleurs[i]
        xm = (i + 0.5) * pas
        L.append(r"\draw[%s,line width=1pt,-{Stealth[length=2.4mm]}] (c%d.east) -- (c%d.west);" % (col, i, i + 1))
        L.append(r"\node[anchor=south,text=%s,inner sep=2pt] at (%.3f,0.1) {$\times %s$};" % (col, xm, nb(coefs[i]) if isinstance(coefs[i], (int, float)) else coefs[i]))
        L.append(r"\node[anchor=north,text=%s,font=\small,inner sep=2pt] at (%.3f,-0.1) {%s};" % (col, xm, taux[i]))
    if retour:
        xf = (n - 1) * pas
        L.append(r"\draw[otMuted,line width=.7pt,-{Stealth[length=2.2mm]}] (0,-0.42) .. controls (0.3,-1.45) and (%.3f,-1.45) .. (%.3f,-0.42);" % (xf - 0.3, xf))
        L.append(r"\node[anchor=north,text=otInk,inner sep=2pt] at (%.3f,-1.27) {%s};" % (xf / 2, bilan))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def axe_cm(points, a, b, u, legende=True, sym="CM"):
    """Coefficients multiplicateurs sur un axe gradué de a à b : 1 = pas d'évolution,
    baisse à gauche (orange), hausse à droite (vert).
    points = [(cm, texte_cm, texte_taux, 'h' ou 'b')] : étiquette au-dessus ou au-dessous."""
    X = lambda v: (v - a) * u
    L = [r"\begin{tikzpicture}"]
    L.append(r"\draw[otOrange!90!black,line width=2.2pt] (0,0) -- (%.3f,0);" % X(1))
    L.append(r"\draw[otGreenDark,line width=2.2pt] (%.3f,0) -- (%.3f,0);" % (X(1), X(b)))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (%.3f,0) -- (%.3f,0);" % (X(b), X(b) + 0.45))
    L.append(r"\draw[otInk,line width=.8pt] (%.3f,-0.2) -- (%.3f,0.2);" % (X(1), X(1)))
    L.append(r"\node[anchor=north,text=otInk,inner sep=1.5pt,align=center] at (%.3f,-0.25) {$1$\\[-1pt]$0\,\%%$};" % X(1))
    for cm, tcm, tt, pos in points:
        col = "otGreenDark" if cm > 1 else "otOrange!90!black"
        L.append(r"\fill[%s] (%.3f,0) circle (3pt);" % (col, X(cm)))
        if pos == "h":
            L.append(r"\node[anchor=south,text=%s,inner sep=1.5pt,align=center] at (%.3f,0.22) {%s\\[-1pt]$\times %s$};" % (col, X(cm), tt, tcm))
        else:
            L.append(r"\node[anchor=north,text=%s,inner sep=1.5pt,align=center] at (%.3f,-0.25) {$\times %s$\\[-1pt]%s};" % (col, X(cm), tcm, tt))
    if legende:
        L.append(r"\node[anchor=north west,text=otOrange!90!black,inner sep=1pt] at (0,-1.35) {$\leftarrow$ baisse : $%s < 1$};" % sym)
        L.append(r"\node[anchor=north east,text=otGreenDark,inner sep=1pt] at (%.3f,-1.35) {hausse : $%s > 1$ $\rightarrow$};" % (X(b) + 0.45, sym))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def arbre_effectifs():
    """1992 : répartition des 800 tickets (effectifs dans les cases, proportions sur les branches)."""
    L = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    L.append(r"\tikzset{noeud/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=3pt,inner sep=3.5pt,align=center,font=\small},"
             r"noeudV/.style={noeud,draw=otGreenDark,fill=otGreen!12},"
             r"br/.style={otNavy!70,line width=.8pt},"
             r"pc/.style={font=\small,text=otMuted,inner sep=1.5pt}}")
    L.append(r"\node[noeud] (R) at (0,0) {$800$\\tickets};")
    L.append(r"\node[noeud] (E) at (3.1,1.55) {étudiants\\$280$};")
    L.append(r"\node[noeud] (P) at (3.1,-1.55) {plein tarif\\$520$};")
    L.append(r"\node[noeudV] (E1) at (6.6,2.35) {en ligne : $112$};")
    L.append(r"\node[noeud] (E2) at (6.6,0.85) {guichet : $168$};")
    L.append(r"\node[noeudV] (P1) at (6.6,-0.85) {en ligne : $312$};")
    L.append(r"\node[noeud] (P2) at (6.6,-2.35) {guichet : $208$};")
    for a, b in (("R", "E"), ("R", "P"), ("E", "E1"), ("E", "E2"), ("P", "P1"), ("P", "P2")):
        L.append(r"\draw[br] (%s.east) -- (%s.west);" % (a, b))
    L.append(r"\node[pc,anchor=south east] at ($(R.east)!0.5!(E.west)+(0.02,0.08)$) {$35\,\%$};")
    L.append(r"\node[pc,anchor=north east] at ($(R.east)!0.5!(P.west)+(0.02,-0.08)$) {$65\,\%$};")
    L.append(r"\node[pc,anchor=south east] at ($(E.east)!0.5!(E1.west)+(0.0,0.08)$) {$40\,\%$};")
    L.append(r"\node[pc,anchor=north east] at ($(E.east)!0.5!(E2.west)+(0.0,-0.08)$) {$60\,\%$};")
    L.append(r"\node[pc,anchor=south east] at ($(P.east)!0.5!(P1.west)+(0.0,0.08)$) {$60\,\%$};")
    L.append(r"\node[pc,anchor=north east] at ($(P.east)!0.5!(P2.west)+(0.0,-0.08)$) {$40\,\%$};")
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


def salaires():
    """3758 : salaires rangés (un bâton par personne), avant et après la hausse de la dirigeante."""
    sal = [1500, 1550, 1600, 1600, 1700, 1750, 1800, 1900, 2000, 2400]
    uy = 0.42 / 1000          # cm par euro
    dx = 0.34
    L = [r"\begin{tikzpicture}"]
    haut = 10000
    for v in range(2000, haut + 1, 2000):
        L.append(r"\draw[otRule,line width=.35pt] (0,%.3f) -- (%.3f,%.3f);" % (v * uy, 12 * dx, v * uy))
    for v in range(0, haut + 1, 2000):
        L.append(r"\draw[tic] (0,%.3f) -- (-0.09,%.3f);" % (v * uy, v * uy))
        L.append(r"\node[grad,anchor=east] at (-0.13,%.3f) {%s};" % (v * uy, nb(v)))
    for i, s in enumerate(sal):
        X = (i + 0.75) * dx
        L.append(r"\fill[otNavy!55] (%.3f,0) rectangle (%.3f,%.3f);" % (X - 0.13, X + 0.13, s * uy))
    X = 10.75 * dx
    L.append(r"\fill[otNavy!55] (%.3f,0) rectangle (%.3f,%.3f);" % (X - 0.13, X + 0.13, 6400 * uy))
    L.append(r"\draw[otOrange!90!black,line width=.8pt,dash pattern=on 2.5pt off 1.5pt,fill=otOrange!18] (%.3f,%.3f) rectangle (%.3f,%.3f);"
             % (X - 0.13, 6400 * uy, X + 0.13, 9700 * uy))
    xr = 11.5 * dx
    # lignes : médiane (verte), moyennes avant / après (orange)
    L.append(r"\draw[otGreenDark,line width=1.1pt] (0,%.3f) -- (%.3f,%.3f);" % (1750 * uy, xr, 1750 * uy))
    L.append(r"\draw[otRed!85!black,line width=1pt,dash pattern=on 4pt off 2pt] (0,%.3f) -- (%.3f,%.3f);" % (2200 * uy, xr, 2200 * uy))
    L.append(r"\draw[otOrange!90!black,line width=1pt,dash pattern=on 1.5pt off 1.5pt] (0,%.3f) -- (%.3f,%.3f);" % (2500 * uy, xr, 2500 * uy))
    # étiquettes à droite, reliées à leur ligne
    for y_ligne, y_txt, col, txt in ((2500, 3500, "otOrange!90!black", r"moyenne après : $2\,500$"),
                                     (2200, 2400, "otRed!85!black", r"moyenne avant : $2\,200$"),
                                     (1750, 1200, "otGreenDark", r"médiane : $1\,750$")):
        L.append(r"\draw[%s,line width=.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, xr, y_ligne * uy, xr + 0.3, y_txt * uy))
        L.append(r"\node[anchor=west,text=%s,inner sep=1.5pt] at (%.3f,%.3f) {%s};" % (col, xr + 0.32, y_txt * uy, txt))
    L.append(r"\node[anchor=west,text=otOrange!90!black,inner sep=1.5pt] at (%.3f,%.3f) {$6\,400 \to 9\,700$};" % (X + 0.25, 8800 * uy))
    L.append(r"\draw[axe,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (haut * uy + 0.4))
    L.append(r"\draw[axe] (0,0) -- (%.3f,0);" % (11.5 * dx))
    L.append(r"\node[grad,anchor=south west] at (0.08,%.3f) {salaire (€)};" % (haut * uy + 0.42))
    L.append(r"\node[grad,anchor=north] at (%.3f,-0.12) {les $11$ salaires, rangés};" % (5.75 * dx))
    L.append(r"\end{tikzpicture}")
    return "\n".join(L)


# ================================================================ FIGURES
FIGURES = {
    # ---- cours et fiche
    "evolutions": chaine(["80", "100", "80"], [1.25, 0.8], [r"hausse de $25\,\%$", r"baisse de $20\,\%$"],
                         r"coefficient global : $1{,}25 \times 0{,}8 = 1$", pas=3.8, largeur_case=1.3),
    "proportion_cours": emboites(0.3, 0.4, r"lycée\\(tous les élèves)", r"Seconde\\$40\,\%$ du lycée",
                                 r"latin : $30\,\%$\\de la Seconde",
                                 r"latin en Seconde : $0{,}3 \times 0{,}4 = 0{,}12$,\\soit $12\,\%$ du lycée"),
    "axe_cm_cours": axe_cm([(0.8, "0{,}8", r"$-20\,\%$", "b"), (1.15, "1{,}15", r"$+15\,\%$", "h"),
                            (1.25, "1{,}25", r"$+25\,\%$", "b")], 0.7, 1.35, 10.5),
    "boite_cours": boite_annotee((4, 8, 11, 14, 19), 0, 20, 0.42, 1, 2,
                                 points=[4, 7, 8, 9, 10, 11, 12, 12, 14, 15, 19]),
    "dispersion_cours": points_empiles(
        [(r"Série $A$ : $\sigma \approx 1{,}2$", [9, 10, 10, 11, 11, 11, 12, 12, 13], "otNavy"),
         (r"Série $B$ : $\sigma \approx 4{,}2$", [4, 6, 8, 10, 11, 13, 14, 16, 17], "otGreenDark")],
        2, 18, 0.45, 1, 2, moyenne=11, legende_moyenne=r"même moyenne : $\bar{x} = 11$"),
    # ---- exercices (figures existantes, revues)
    "hist_appels": histogramme([0, 2, 4, 6, 8, 10], [6, 14, 15, 10, 5], 0.75, 0.2, 5,
                               "Durée (min)", "Effectif"),
    "hist_sport": histogramme([0, 2, 4, 6, 8, 10, 12], [12, 28, 44, 50, 34, 12], 0.62, 0.065, 10,
                              "Temps (h par semaine)", "Effectif"),
    "batons_masses": batons([248, 248.5, 249, 249.5, 250, 250.5, 251, 251.5, 252],
                            [2, 8, 18, 34, 52, 40, 26, 14, 6], 0.88, 0.062, 10, "Masse (g)", "Effectif"),
    "boites_3series": boites([(r"Série 1", 3, 4, 10.5, 13, 20), (r"Série 2", 2, 5, 9, 11, 18),
                              (r"Série 3", 6, 9, 13, 17, 20)], 0, 20, 0.36, 1, 2, "Valeurs"),
    "boites_AB": boites([(r"Série $A$", 0, 1, 2, 4, 5), (r"Série $B$", 8, 10, 12, 14, 16)],
                        0, 16, 0.44, 1, 2, "Valeurs"),
    "groupes_AB": points_empiles(
        [(r"Groupe $A$ : $\sigma_A \approx 2{,}05$", [8, 8, 10, 10, 10, 12, 12, 12, 14, 14], "otNavy"),
         (r"Groupe $B$ : $\sigma_B = 4$", [5, 5, 8, 8, 12, 12, 14, 14, 16, 16], "otGreenDark")],
        4, 18, 0.52, 1, 2, moyenne=11, legende_moyenne=r"même moyenne : $\bar{x} = 11$"),
    # ---- exercices (nouvelles figures, 2026-11-02)
    "e1976_emboites": emboites(0.25, 0.4, r"lycée\\(tous les élèves)", r"Seconde\\$40\,\%$ du lycée",
                               r"latin : $25\,\%$\\de la Seconde",
                               r"Seconde latin : $0{,}25 \times 0{,}40 = 0{,}10$,\\soit $10\,\%$ du lycée"),
    "e1984_axe": axe_cm([(0.88, "0{,}88", r"$-12\,\%$", "b"), (0.90, "0{,}90", r"$-10\,\%$", "h"),
                         (1.08, "1{,}08", r"$+8\,\%$", "b"), (1.15, "1{,}15", r"$+15\,\%$", "h")], 0.8, 1.2, 17, sym="C"),
    "e1985_chaine": chaine(["100", "120", "102"], ["1{,}20", "0{,}85"], [r"hausse de $20\,\%$", r"baisse de $15\,\%$"],
                           r"coefficient global : $1{,}20 \times 0{,}85 = 1{,}02$, soit $+2\,\%$", pas=3.8,
                           verte={2}, largeur_case=1.3),
    "e1985_salaire": chaine([r"1\,500", r"1\,575", r"1\,653{,}75", r"1\,736{,}44"], [1.05, 1.05, 1.05],
                            [r"$+5\,\%$", r"$+5\,\%$", r"$+5\,\%$"],
                            r"coefficient global : $1{,}05^3 = 1{,}157\,625$", pas=2.5, verte={3},
                            largeur_case=1.5),
    "e1986_reciproque": chaine(["100", "70", "100"], [0.7, r"\dfrac{10}{7}"],
                               [r"baisse de $30\,\%$", r"hausse $\approx 42{,}9\,\%$"],
                               r"coefficient global : $0{,}7 \times \dfrac{10}{7} = 1$", pas=4.0,
                               couleurs=["otOrange!90!black", "otGreenDark"], largeur_case=1.3),
    "e1989_boite": boite_annotee((5, 8, 10.5, 14, 20), 4, 20, 0.5, 1, 2,
                                 points=[5, 7, 8, 9, 10, 10, 11, 12, 14, 15, 18, 20]),
    "e1990_villes": points_empiles(
        [(r"Ville $A$ : $\sigma_A \approx 1{,}22$", [22, 23, 23, 24, 24, 25, 25, 26], "otNavy"),
         (r"Ville $B$ : $\sigma_B \approx 3{,}74$", [18, 20, 22, 24, 24, 26, 28, 30], "otGreenDark")],
        16, 32, 0.5, 1, 2, moyenne=24, legende_moyenne=r"même moyenne : $24\,^\circ\mathrm{C}$",
        titre_gauche=True),
    "e1990_canicule": nuage_intervalle([18, 20, 22, 24, 24, 26, 28, 42], 8, 44, 0.225, 2, 4,
                                       11.68, 39.32, r"$11{,}68$", r"$39{,}32$",
                                       r"$[\bar{x} - 2\sigma\,;\,\bar{x} + 2\sigma]$ : $7$ valeurs sur $8$"),
    "e1991_intervalle": nuage_intervalle([0, 0, 0, 0, 0, 10], -8, 12, 0.4, 1, 2,
                                         -5.79, 9.12, r"$m - 2s \approx -5{,}79$", r"$m + 2s \approx 9{,}12$",
                                         r"$5$ valeurs sur $6$ dans l’intervalle"),
    "e1982_boite": boite_annotee((6, 10, 13, 15, 19), 4, 20, 0.5, 1, 2, iqr=False,
                                 moyenne=(12.6, r"$\bar{x} = 12{,}6$"),
                                 cote=(10, 15, r"notes de rang $7$ à $21$ : au moins $15$ notes")),
    "e1983_boite": boite_annotee((5, 9, 11, 12, 16), 4, 17, 0.62, 1, 1,
                                 points=[5] + [7] * 2 + [8] * 3 + [9] * 3 + [10] * 4 + [11] * 5 + [12] * 6
                                 + [13] * 4 + [14] * 2 + [15, 16]),
    "e1992_arbre": arbre_effectifs(),
    "e3758_salaires": salaires(),
}
