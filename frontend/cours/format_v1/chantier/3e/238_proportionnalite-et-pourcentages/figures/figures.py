# -*- coding: utf-8 -*-
"""Figures de la notion « Proportionnalité et pourcentages » (3e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données, vert foncé = éléments
de réponse (corrigés), orange = éléments d'alerte (partie fixe, etc.).
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt,text=otInk},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,inner sep=0pt,text=otMuted},
  case/.style={draw=otNavy,line width=.7pt,minimum height=.75cm,inner sep=2pt,text=otInk},
  valeur/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=2pt,minimum height=.8cm,minimum width=1.75cm,text=otInk},
  valeurV/.style={valeur,draw=otGreenDark,fill=otGreen!15,text=otGreenDark},
  fl/.style={otNavy,line width=.9pt,-{Stealth[length=2.3mm]}},
  flV/.style={otGreenDark,line width=.9pt,-{Stealth[length=2.3mm]}},
  flO/.style={otOrange!85!black,line width=.9pt,-{Stealth[length=2.3mm]}},
  accol/.style={decorate,decoration={brace,amplitude=5pt},otMuted,line width=.7pt},
}
"""


def figure(corps, opt="line cap=round"):
    return "\n".join([r"\begin{tikzpicture}[%s]" % opt] + corps + [r"\end{tikzpicture}"])


def axe(opts, corps):
    return "\n".join([r"\begin{tikzpicture}", r"\begin{axis}[otWeb, %s]" % opts] + corps
                     + [r"\end{axis}", r"\end{tikzpicture}"])


LAB = (r"every axis x label/.style={at={(current axis.right of origin)},anchor=north east,yshift=-15pt,"
       r"font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},"
       r"every axis y label/.style={at={(current axis.above origin)},anchor=south west,"
       r"font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted}")


# ================================================================== TABLEAU DE PROPORTIONNALITÉ
def tableau(entetes, l1, l2, coef, vert=False):
    w0, w, h = 2.6, 1.25, .75
    s = []
    x = 0
    for r, (ent, ligne) in enumerate(((entetes[0], l1), (entetes[1], l2))):
        y = -r * h
        s.append(r"\fill[otSky] (0,%.2f) rectangle (%.2f,%.2f);" % (y, w0, y - h))
        s.append(r"\node[txt,text=otNavy] at (%.2f,%.2f) {%s};" % (w0 / 2, y - h / 2, ent))
        for k, v in enumerate(ligne):
            s.append(r"\node[text=otInk] at (%.2f,%.2f) {$%s$};" % (w0 + (k + .5) * w, y - h / 2, v))
    n = len(l1)
    W = w0 + n * w
    s += [r"\draw[otNavy,line width=.7pt] (0,0) rectangle (%.2f,%.2f);" % (W, -2 * h),
          r"\draw[otNavy,line width=.7pt] (0,%.2f) -- (%.2f,%.2f);" % (-h, W, -h)]
    for k in range(n):
        s.append(r"\draw[otNavy,line width=.7pt] (%.2f,0) -- (%.2f,%.2f);" % (w0 + k * w, w0 + k * w, -2 * h))
    st = "flV" if vert else "fl"
    c = "otGreenDark" if vert else "otNavy"
    s += [r"\draw[%s] (%.2f,%.2f) to[out=0,in=0,looseness=1.6] (%.2f,%.2f);" % (st, W + .1, -h / 2, W + .1, -1.5 * h),
          r"\node[text=%s,anchor=west] at (%.2f,%.2f) {$\times %s$};" % (c, W + .62, -h, coef)]
    return figure(s)


FIGURES = {}
FIGURES["cours_tableau"] = tableau(("masse (kg)", "prix (€)"), ("2", "5", "8"), ("7", "17{,}5", "28"), "3{,}5")
FIGURES["ex2234_corrige"] = tableau(("masse (kg)", "prix (€)"), ("2", "5", "8", "11"), ("7", "17{,}5", "28", "38{,}5"), "3{,}5", vert=True)


# ================================================================== CHAÎNES DE COEFFICIENTS
def chaine(vals, coefs, retour=None, glob=None, vert_fin=False, y=0, dx=3.2, notes=None):
    """vals : valeurs en boîtes ; coefs : étiquettes des flèches du haut ;
    retour : étiquette de la flèche de retour (dernier -> premier) ; glob : flèche globale (premier -> dernier)."""
    s = []
    for i, v in enumerate(vals):
        st = "valeurV" if (vert_fin and i == len(vals) - 1) else "valeur"
        s.append(r"\node[%s] (v%d%s) at (%.2f,%.2f) {%s};" % (st, i, "a" if y == 0 else "b", i * dx, y, v))
    t = "a" if y == 0 else "b"
    for i, c in enumerate(coefs):
        col, st = (("otGreenDark", "flV") if c.startswith("!") else ("otNavy", "fl"))
        c = c.lstrip("!")
        s.append(r"\draw[%s] (v%d%s.north) to[bend left=38] node[midway,above=2pt,text=%s] {%s} (v%d%s.north);"
                 % (st, i, t, col, c, i + 1, t))
    if retour:
        col, st = (("otGreenDark", "flV") if retour.startswith("!") else ("otOrange!85!black", "flO"))
        s.append(r"\draw[%s] (v%d%s.south) to[bend left=38] node[midway,below=2pt,text=%s] {%s} (v0%s.south);"
                 % (st, len(vals) - 1, t, col, retour.lstrip("!"), t))
    if glob:
        s.append(r"\draw[flV] (v0%s.south) to[bend right=22] node[midway,below=2pt,text=otGreenDark] {%s} (v%d%s.south);"
                 % (t, glob, len(vals) - 1, t))
    return s


FIGURES["cours_coef"] = figure(chaine(("$75$ €", "$81$ €"), ("hausse de $8\\ \\%$ : $\\times 1{,}08$",),
                                      retour="retour : $\\div 1{,}08$", dx=4.6))
FIGURES["cours_successives"] = figure(chaine(("$100$", "$120$", "$96$"), ("$+20\\ \\%$ : $\\times 1{,}2$", "$-20\\ \\%$ : $\\times 0{,}8$"),
                                             glob="$\\times 0{,}96$ : baisse de $4\\ \\%$", vert_fin=True, dx=3.5))
FIGURES["ex2236_corrige"] = figure(
    chaine(("$64$ €", "$48$ €"), ("!$-25\\ \\%$ : $\\times 0{,}75$",), vert_fin=True, dx=4.2)
    + [r"\begin{scope}[xshift=0cm]"]
    + chaine(("$160$", "$184$"), ("!$\\times 1{,}15$ : $+15\\ \\%$",), vert_fin=True, dx=4.2, y=-2.7)
    + [r"\end{scope}",
       r"\node[petit,anchor=east] at (-1.1,0) {sac};",
       r"\node[petit,anchor=east] at (-1.1,-2.7) {effectif};"])
FIGURES["ex2240_corrige"] = figure(
    chaine(("$75$ €", "$81$ €"), ("$+8\\ \\%$ : $\\times 1{,}08$",), retour="!$\\div 1{,}08$", dx=4.2)
    + chaine(("$120$ €", "$84$ €"), ("$-30\\ \\%$ : $\\times 0{,}7$",), retour="!$\\div 0{,}7$", dx=4.2, y=-4))
FIGURES["ex2241_corrige"] = figure(chaine(("$250$ €", "$225$ €", "$180$ €"), ("$\\times 0{,}9$", "$\\times 0{,}8$"),
                                          glob="$\\times 0{,}72$ : baisse de $28\\ \\%$", vert_fin=True, dx=3.2))
FIGURES["ex2253_corrige"] = figure(chaine(("$2{,}5$ M", "$2$ M", "$2{,}4$ M"), ("$-20\\ \\%$ : $\\times 0{,}8$", "$+20\\ \\%$ : $\\times 1{,}2$"),
                                          glob="$\\times 0{,}96$ : baisse de $4\\ \\%$", vert_fin=True, dx=3.5))


# ================================================================== GRAPHIQUES
def graphe_cours():
    return axe(
        r"width=5.8cm, height=5cm, xmin=0, xmax=8.6, ymin=0, ymax=13.4, xtick={1,...,8}, ytick={2,4,...,12},"
        r"xlabel={}, ylabel={}",
        [r"\addplot[courbe,domain=0:8] {1.5*x};",
         r"\addplot[otOrange!85!black,line width=1.35pt,domain=0:8] {.75*x+4};",
         r"\fill[otOrange!85!black] (axis cs:0,4) circle (2.4pt);",
         r"\node[text=otNavy,anchor=west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:8.2,12) {proportionnel};",
         r"\node[text=otOrange!80!black,anchor=west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:8.2,10) {non proportionnel};"])


FIGURES["cours_graphique"] = graphe_cours()


def graphe_2238():
    return axe(
        r"width=7cm, height=5cm, xmin=0, xmax=320, ymin=0, ymax=20, xtick={50,100,...,300}, ytick={3,6,...,18},"
        r"xlabel={distance (km)}, ylabel={essence (L)}," + LAB,
        [r"\addplot[courbe,domain=0:300] {0.06*x};",
         r"\fill[otGreenDark] (axis cs:100,6) circle (2.5pt);",
         r"\fill[otGreenDark] (axis cs:150,9) circle (2.5pt);",
         r"\fill[otGreenDark] (axis cs:250,15) circle (2.5pt);",
         r"\node[text=otGreenDark,anchor=north west] at (axis cs:104,5.6) {$(100\,;6)$};",
         r"\node[text=otGreenDark,anchor=north west] at (axis cs:154,8.6) {$(150\,;9)$};",
         r"\node[text=otGreenDark,anchor=north west] at (axis cs:254,14.6) {$(250\,;15)$};",
         r"\fill[otGreenDark] (axis cs:0,0) circle (2.5pt);"])


FIGURES["ex2238_corrige"] = graphe_2238()


def graphe_2243():
    pts = "".join("(%d,%d)" % (n, 5 + 2 * n) for n in range(1, 7))
    return axe(
        r"width=6cm, height=5.2cm, xmin=0, xmax=7, ymin=0, ymax=19, xtick={1,...,6}, ytick={5,10,15},"
        r"xlabel={colis}, ylabel={coût (€)}," + LAB,
        [r"\draw[otNavy!45,line width=1pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,5) -- (axis cs:6.6,18.2);",
         r"\addplot[only marks,mark=*,mark size=2.4pt,otNavy] coordinates {%s};" % pts,
         r"\fill[otOrange!85!black] (axis cs:0,5) circle (2.6pt);",
         r"\node[text=otOrange!80!black,anchor=west,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:.25,2.6) {frais fixes : $5$ € pour $0$ colis};",
         r"\node[text=otGreenDark,anchor=north west,align=left,font=\otMedium\fontsize{8.5}{10}\selectfont] at (axis cs:3.4,7.4) {la droite ne passe\\pas par l'origine};"])


FIGURES["ex2243_corrige"] = graphe_2243()


def graphe_2245(corr):
    c = [r"\addplot[%s,domain=0:6] {2*x};" % ("otGreenDark,line width=1.6pt" if corr else "courbe"),
         r"\addplot[courbe,domain=0:6] {.5*x+4};",
         r"\addplot[courbe,domain=0:6] {.25*x^2};",
         r"\node[text=%s,anchor=west] at (axis cs:6.15,12) {$\mathcal{D}_1$};" % ("otGreenDark" if corr else "otNavy"),
         r"\node[text=otNavy,anchor=west] at (axis cs:6.15,7) {$\mathcal{D}_2$};",
         r"\node[text=otNavy,anchor=west] at (axis cs:6.15,9) {$\mathcal{C}_3$};"]
    if corr:
        c += [r"\draw[guide] (axis cs:4,0) -- (axis cs:4,8) -- (axis cs:0,8);",
              r"\fill[otGreenDark] (axis cs:4,8) circle (2.6pt);",
              r"\node[text=otGreenDark,anchor=south east] at (axis cs:3.85,8.3) {$(4\,;8)$};"]
    return axe(
        r"width=6cm, height=5.6cm, xmin=0, xmax=6.6, ymin=0, ymax=13, xtick={1,...,6}, ytick={2,4,...,12}",
        c)


FIGURES["ex2245_enonce"] = graphe_2245(False)
FIGURES["ex2245_corrige"] = graphe_2245(True)


# ================================================================== RATIO
def ratio(corr):
    u = .95
    s = []
    for k in range(8):
        f = "otSky" if k < 3 else "otOrange!18"
        s.append(r"\fill[%s] (%.2f,0) rectangle (%.2f,.8);" % (f, k * u, (k + 1) * u))
        if corr:
            s.append(r"\node[text=otGreenDark] at (%.2f,.4) {$7$};" % ((k + .5) * u))
    s.append(r"\draw[otNavy,line width=.8pt] (0,0) rectangle (%.2f,.8);" % (8 * u))
    for k in range(1, 8):
        w = "1.4pt" if k == 3 else ".6pt"
        s.append(r"\draw[otNavy,line width=%s] (%.2f,0) -- (%.2f,.8);" % (w, k * u, k * u))
    s += [r"\draw[accol] (0,.92) -- (%.2f,.92);" % (3 * u),
          r"\draw[accol] (%.2f,.92) -- (%.2f,.92);" % (3 * u, 8 * u),
          r"\draw[accol] (%.2f,-.12) -- (0,-.12);" % (8 * u)]
    if corr:
        s += [r"\node[text=otGreenDark,anchor=south] at (%.2f,1.2) {$3 \times 7 = 21$ billes};" % (1.5 * u),
              r"\node[text=otGreenDark,anchor=south] at (%.2f,1.2) {$5 \times 7 = 35$ billes};" % (5.5 * u),
              r"\node[text=otGreenDark,anchor=north] at (%.2f,-.42) {$8$ parts de $56 \div 8 = 7$ billes};" % (4 * u)]
    else:
        s += [r"\node[anchor=south] at (%.2f,1.2) {$3$ parts};" % (1.5 * u),
              r"\node[anchor=south] at (%.2f,1.2) {$5$ parts};" % (5.5 * u),
              r"\node[anchor=north] at (%.2f,-.42) {$56$ billes en tout};" % (4 * u)]
    return figure(s)


FIGURES["ex2237_enonce"] = ratio(False)
FIGURES["ex2237_corrige"] = ratio(True)
