# -*- coding: utf-8 -*-
"""Figures de la notion « Équations et fonctions polynômes du second degré »
(Première spécialité), style des livres OptiTAB.

Compilation : python ../../../outils/figures_livre.py <ce dossier de notion>
"""

# ------------------------------------------------------------------ outils
NOTE = r"\otRegular\fontsize{8.5}{10}\selectfont"


def panneau_delta(cx, cy, signe, cas):
    """Petit cadre : axe des abscisses et parabole (a > 0 si signe = 1)."""
    k = 1.3 * signe
    m = {"pos": -0.55, "nul": 0.0, "neg": 0.3}[cas] * signe
    dom = {"pos": 1.0, "nul": 0.92, "neg": 0.75}[cas]
    haut, bas = (1.2, -0.75) if signe > 0 else (0.75, -1.2)
    code = (
        rf"  \draw[otRule,line width=0.6pt,rounded corners=1.5mm] ({cx - 1.2},{cy + bas}) rectangle ({cx + 1.2},{cy + haut});" "\n"
        rf"  \draw[otMuted,line width=0.6pt,-{{Stealth[length=1.6mm]}}] ({cx - 1.08},{cy}) -- ({cx + 1.08},{cy});" "\n"
        rf"  \draw[courbe] plot[domain=-{dom}:{dom},samples=60] ({{{cx}+\x}},{{{cy}+{k}*\x*\x+{m}}});" "\n"
    )
    if cas == "pos":
        r = (0.55 / 1.3) ** 0.5
        code += rf"  \fill[otGreenDark] ({cx - r:.4f},{cy}) circle (2pt); \fill[otGreenDark] ({cx + r:.4f},{cy}) circle (2pt);" "\n"
    elif cas == "nul":
        code += rf"  \fill[otGreenDark] ({cx},{cy}) circle (2pt);" "\n"
    return code


def grille_delta():
    code = r"\begin{tikzpicture}" "\n"
    entetes = [("pos", r"\Delta > 0", "deux racines"), ("nul", r"\Delta = 0", "une racine double"),
               ("neg", r"\Delta < 0", "aucune racine")]
    for j, (cas, delta, texte) in enumerate(entetes):
        cx = 2.65 * j
        code += (rf"  \node[anchor=south,align=center] at ({cx},1.3) {{${delta}$\\[-1pt]{{{NOTE}\color{{otMuted}}{texte}}}}};" "\n")
        code += panneau_delta(cx, 0, 1, cas)
        code += panneau_delta(cx, -2.3, -1, cas)
    code += r"  \node[anchor=east,text=otNavy] at (-1.4,0.2) {$a > 0$};" "\n"
    code += r"  \node[anchor=east,text=otNavy] at (-1.4,-2.5) {$a < 0$};" "\n"
    code += r"\end{tikzpicture}"
    return code


ENCLOS = r"""
\begin{tikzpicture}
  \fill[otMuted!25] (-0.4,3.0) rectangle (6.4,3.35);
  \fill[pattern=north east lines,pattern color=otMuted!80] (-0.4,3.0) rectangle (6.4,3.35);
  \draw[otMuted,line width=0.8pt] (-0.4,3.0) -- (6.4,3.0);
  \node[anchor=south,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted] at (3,3.4) {mur existant (pas de clôture)};
  \fill[otGreen!12] (0,0) rectangle (6,3.0);
  \draw[otNavy,line width=1.6pt,line join=round] (0,3.0) -- (0,0) -- (6,0) -- (6,3.0);
  \node[anchor=east,text=otInk] at (-0.12,1.5) {$x$};
  \node[anchor=west,text=otInk] at (6.12,1.5) {$x$};
  \node[anchor=north,text=otInk] at (3,-0.12) {$y$};
  \node[note,fill=none,text=otNavy] at (3,1.25) {clôture en bleu : $x + y + x$};
\end{tikzpicture}"""


def quatre_paraboles(titre, courbes, ymin, ymax, yticks):
    """Quatre repères 2 × 2 encadrés : graduations sur le cadre, jamais sur une courbe.

    courbes : [(indice, expression, domaine, [(x, y) points marqués])].
    """
    style = (
        r"\pgfplotsset{mini/.style={otWeb, axis lines=box, axis line style={otMuted!60,line width=0.5pt,-},"
        r" tick pos=left, major tick length=2pt, xlabel={}, ylabel={},"
        r" yticklabel style={anchor=east,xshift=-1.5pt,yshift=0pt}, xticklabel style={anchor=north,yshift=-1.5pt},"
        rf" width=3.3cm, height=3.3cm, xmin=-4.4, xmax=4.4, ymin={ymin}, ymax={ymax},"
        rf" xtick={{-4,-2,0,2,4}}, ytick={{{yticks}}}, minor tick num=1, grid=both,"
        r" minor grid style={otRule!60,line width=0.3pt}, minor tick length=0pt}}" "\n"
    )
    code = r"\begin{tikzpicture}" "\n" + style
    places = ["", ", at={(A.east)}, anchor=west, xshift=1.25cm", ", at={(A.south)}, anchor=north, yshift=-1.55cm",
              ", at={(C.east)}, anchor=west, xshift=1.25cm"]
    for nom, place, (indice, expr, dom, points) in zip("ABCD", places, courbes):
        code += rf"\begin{{axis}}[mini, name={nom}{place}]" "\n"
        code += (rf"  \draw[otMuted,line width=0.7pt,-{{Stealth[length=1.5mm]}}] (axis cs:-4.4,0) -- (axis cs:4.4,0);" "\n"
                 rf"  \draw[otMuted,line width=0.7pt,-{{Stealth[length=1.5mm]}}] (axis cs:0,{ymin}) -- (axis cs:0,{ymax});" "\n")
        code += rf"  \addplot[courbe, domain={dom}] {{{expr}}};" "\n"
        code += "".join(rf"  \pnt{{{x}}}{{{y}}}" "\n" for x, y in points)
        code += r"\end{axis}" "\n"
        code += rf"\node[anchor=south,text=otNavy] at ($({nom}.north)+(0,0.12)$) {{{titre} ${indice}$}};" "\n"
    return code + r"\end{tikzpicture}"


QUATRE_TRANSLATIONS = quatre_paraboles("Parabole", [
    (r"\mathcal{P}_A", "x^2", "-2.5:2.5", [(0, 0)]),
    (r"\mathcal{P}_B", "x^2-3", "-3.0:3.0", [(0, -3)]),
    (r"\mathcal{P}_C", "(x-2)^2", "-0.5:4.4", [(2, 0)]),
    (r"\mathcal{P}_D", "(x+1)^2+2", "-3.0:1.0", [(-1, 2)]),
], -4.4, 6.4, "-4,-2,0,2,4,6")

QUATRE_LECTURE = quatre_paraboles("Courbe", [
    (r"\mathcal{C}_1", "(x-1)^2-4", "-2.0:4.0", [(1, -4), (3, 0)]),
    (r"\mathcal{C}_2", "-(x-2)^2", "-0.3:4.4", [(2, 0), (0, -4)]),
    (r"\mathcal{C}_3", "0.5*(x+1)^2+1", "-4.0:2.0", [(-1, 1), (1, 3)]),
    (r"\mathcal{C}_4", "-(x+1)^2+4", "-4.0:2.0", [(-1, 4), (1, 0)]),
], -5.4, 5.4, "-4,-2,0,2,4")


FIGURES = {
# ------------------------------------------------------------------ cours
"cours_formes": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.4cm, height=6.2cm, xmin=-4.4, xmax=2.6, ymin=-9.6, ymax=7.2,
  xtick={-3,-2,-1,1}, xticklabels={}, ytick={-4,4}]
  \draw[seuil] (axis cs:-1,-8) -- (axis cs:-1,6.9);
  \addplot[courbe, domain=-3.74:1.74] {2*x^2+4*x-6};
  \pnt[otOrange!90!black]{-1}{-8}
  \pnt[otGreenDark]{-3}{0} \pnt[otGreenDark]{1}{0}
  \pnt[otRed]{0}{-6}
  \node[note,fill=none,anchor=south east,text=otOrange!75!black] at (axis cs:-1.1,6.95) {axe de symétrie $x = -1$};
  \node[note,fill=none,anchor=north,text=otOrange!75!black,align=center] at (axis cs:-1,-8.35) {sommet\\$S(-1\,;-8)$};
  \node[note,fill=none,anchor=west,text=otRed!85!black] at (axis cs:0.15,-6.6) {$f(0) = c = -6$};
  \node[note,fill=none,anchor=south east,text=otGreenDark] at (axis cs:-3.2,0.2) {racine $-3$};
  \node[note,fill=none,anchor=south west,text=otGreenDark] at (axis cs:1.1,0.25) {racine $1$};
  \node[etiq,fill=none,text=otNavy,anchor=west] at (axis cs:1.75,4.6) {$y = f(x)$};
\end{axis}
\end{tikzpicture}""",

"cours_variations": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, name=g, width=3.5cm, height=2.9cm, xmin=-0.5, xmax=4.4, ymin=-0.5, ymax=3.6,
  xtick=\empty, ytick=\empty, grid=none]
  \addplot[courbe, domain=0.05:3.95] {0.6*(x-2)^2+0.9};
  \guides{2}{0.9}
  \pnt{2}{0.9}
  \node[etiq,fill=none,anchor=north west] at (axis cs:2.08,0.85) {$S$};
  \node[anchor=north,text=otMuted,inner sep=1.3pt] at (axis cs:2,-0.05) {$\alpha$};
  \node[anchor=east,text=otMuted,inner sep=1.3pt] at (axis cs:-0.05,0.9) {$\beta$};
\end{axis}
\node[anchor=south,align=center] at ($(g.north)+(0,0.3)$) {$a > 0$\\[-1pt]{\otRegular\fontsize{8.5}{10}\selectfont\color{otMuted}minimum $\beta$ en $\alpha$}};
\begin{axis}[otWeb, at={(g.east)}, anchor=west, xshift=1.3cm, name=d, width=3.5cm, height=2.9cm,
  xmin=-0.5, xmax=4.4, ymin=-0.5, ymax=3.6, xtick=\empty, ytick=\empty, grid=none]
  \addplot[courbe, domain=0.05:3.95] {-0.6*(x-2)^2+2.9};
  \guides{2}{2.9}
  \pnt{2}{2.9}
  \node[etiq,fill=none,anchor=south] at (axis cs:2,2.98) {$S$};
  \node[anchor=north,text=otMuted,inner sep=1.3pt] at (axis cs:2,-0.05) {$\alpha$};
  \node[anchor=east,text=otMuted,inner sep=1.3pt] at (axis cs:-0.05,2.9) {$\beta$};
\end{axis}
\node[anchor=south,align=center] at ($(d.north)+(0,0.3)$) {$a < 0$\\[-1pt]{\otRegular\fontsize{8.5}{10}\selectfont\color{otMuted}maximum $\beta$ en $\alpha$}};
\end{tikzpicture}""",

"cours_discriminant": grille_delta(),

"cours_signe": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.8cm, height=5.2cm, xmin=-5.7, xmax=3.7, ymin=-9.2, ymax=7.6,
  xtick={-3,1}, xticklabels={}, ytick={4}]
  \addplot[courbe, domain=-3.74:1.74] {2*x^2+4*x-6};
  \node[anchor=north east,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:-3.08,-0.42) {$-3$};
  \node[anchor=north west,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:1.08,-0.42) {$1$};
  \draw[otGreen,line width=3pt,line cap=butt] (axis cs:-5.5,0) -- (axis cs:-3,0);
  \draw[otGreen,line width=3pt,line cap=butt] (axis cs:1,0) -- (axis cs:3.5,0);
  \draw[otOrange,line width=3pt,line cap=butt] (axis cs:-3,0) -- (axis cs:1,0);
  \borneF{-3} \borneF{1}
  \node[note,fill=none,anchor=south,text=otGreenDark] at (axis cs:-4.6,0.5) {$f(x) > 0$};
  \node[note,fill=none,anchor=south,text=otGreenDark] at (axis cs:2.6,0.5) {$f(x) > 0$};
  \node[note,fill=none,anchor=center,text=otOrange!75!black] at (axis cs:-1,-3) {$f(x) < 0$};
  \node[etiq,fill=none,text=otNavy,anchor=west] at (axis cs:1.75,5.6) {$y = 2x^2 + 4x - 6$};
\end{axis}
\end{tikzpicture}""",

"cours_projectile": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.6cm, xmin=0, xmax=5.3, ymin=0, ymax=35.5,
  xtick={1,2,3,4}, ytick={10,20,30}, xlabel={$t$}, ylabel={$h$}]
  \addplot[courbe, domain=0:4.4495] {-5*x^2+20*x+10};
  \guides{2}{30}
  \pnt{0}{10} \pnt[otOrange!90!black]{2}{30} \pnt[otGreenDark]{4.4495}{0}
  \node[note,fill=none,anchor=south,text=otOrange!75!black] at (axis cs:2,30.8) {maximum : $30$ m à $t = 2$ s};
  \node[note,fill=none,anchor=north west] at (axis cs:0.12,9.2) {départ : $10$ m};
  \node[note,fill=none,anchor=south west,text=otGreenDark] at (axis cs:4.5,0.8) {sol : $t \approx 4{,}45$ s};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------------------------ fiche
"fiche_signe": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=3.6cm, xmin=-4.2, xmax=6.2, ymin=-3.3, ymax=3.4,
  xtick=\empty, ytick=\empty, grid=none, ylabel={}, axis y line=none]
  \addplot[courbe, domain=-1.9:3.9] {0.5*(x-1)^2-2};
  \draw[otGreen,line width=3pt,line cap=butt] (axis cs:-4,0) -- (axis cs:-1,0);
  \draw[otGreen,line width=3pt,line cap=butt] (axis cs:3,0) -- (axis cs:5.9,0);
  \draw[otOrange,line width=3pt,line cap=butt] (axis cs:-1,0) -- (axis cs:3,0);
  \borneF{-1} \borneF{3}
  \node[anchor=north east,text=otGreenDark,inner sep=1.3pt] at (axis cs:-1.1,-0.3) {$x_1$};
  \node[anchor=north west,text=otGreenDark,inner sep=1.3pt] at (axis cs:3.1,-0.3) {$x_2$};
  \node[note,fill=none,anchor=south,text=otGreenDark] at (axis cs:-3,0.35) {signe de $a$};
  \node[note,fill=none,anchor=south,text=otGreenDark] at (axis cs:4.9,0.35) {signe de $a$};
  \node[note,fill=none,anchor=north,text=otOrange!75!black] at (axis cs:1,-2.15) {signe de $-a$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------------------------ exercices
"paraboles_translations": QUATRE_TRANSLATIONS,

"lecture_paraboles": QUATRE_LECTURE,

"parabole_droite": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=5.4cm, xmin=-2.6, xmax=5.6, ymin=-2.8, ymax=9.3,
  xtick={-1,4}, ytick={7}]
  \addplot[courbe, domain=-2.0:4.3, name path=p] {x^2-2*x-1};
  \addplot[courbe2, domain=-2.5:5.4, name path=d] {x+3};
  \addplot[otGreen!25] fill between[of=d and p, soft clip={domain=-1:4}];
  \guides{4}{7} \guidev{-1}{2}
  \pnt[otGreenDark]{-1}{2} \pnt[otGreenDark]{4}{7}
  \node[etiq,fill=none,anchor=north west,text=otGreenDark] at (axis cs:-0.85,1.75) {$A$};
  \node[etiq,fill=none,anchor=north west,text=otGreenDark] at (axis cs:4.1,6.6) {$B$};
  \node[etiq,fill=none,anchor=east,text=otNavy] at (axis cs:-1.95,6.6) {$\mathcal{P}$};
  \node[etiq,fill=none,anchor=north west,text=otGreenDark] at (axis cs:4.9,7.7) {$\mathcal{D}$};
\end{axis}
\end{tikzpicture}""",

"projectile_ds2": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.4cm, xmin=0, xmax=2.55, ymin=0, ymax=7.9,
  xtick={0.6838,1,1.3162,2}, xticklabels={}, ytick={2,4,6}, xlabel={$t$}, ylabel={$h$}]
  \addplot[courbe, domain=0:2.1402, name path=c] {-5*x^2+10*x+1.5};
  \draw[seuil] (axis cs:0,6) -- (axis cs:2.4,6);
  \guidev{0.6838}{6} \guidev{1.3162}{6}
  \sol{0.6838}{1.3162} \borneF{0.6838} \borneF{1.3162}
  \pnt[otOrange!90!black]{1}{6.5} \pnt{0}{1.5} \pnt[otGreenDark]{2.1402}{0}
  \node[note,fill=none,anchor=south,text=otOrange!75!black] at (axis cs:1,6.75) {maximum $6{,}5$ m};
  \node[note,fill=none,anchor=south west,text=otGreenDark] at (axis cs:2.17,0.35) {$t \approx 2{,}14$};
  \node[note,fill=none,anchor=south east,text=otOrange!75!black] at (axis cs:2.45,6.15) {$h = 6$};
\end{axis}
\end{tikzpicture}""",

"enclos_mur": ENCLOS,

"fenetre": r"""
\begin{tikzpicture}
  \fill[otSky] (0,0) rectangle (3,2.6);
  \fill[otSky] (3,2.6) arc[start angle=0,end angle=180,radius=1.5];
  \draw[otNavy,line width=1.2pt,line join=round] (0,2.6) -- (0,0) -- (3,0) -- (3,2.6) arc[start angle=0,end angle=180,radius=1.5];
  \draw[otNavy!45,line width=0.6pt,dash pattern=on 3pt off 2pt] (0,2.6) -- (3,2.6);
  \cote[0.45]{3,0}{0,0}{$x$}
  \cote[0.45]{3,2.6}{3,0}{$h$}
  \node[note,fill=none] at (1.5,3.35) {demi-cercle};
  \node[note,fill=none] at (1.5,1.3) {rectangle};
\end{tikzpicture}""",

"parterre_allee": r"""
\begin{tikzpicture}
  \fill[otMuted!18] (0,0) rectangle (5.6,4.4);
  \fill[otGreen!25] (0.8,0.8) rectangle (4.8,3.6);
  \draw[otMuted,line width=0.9pt] (0,0) rectangle (5.6,4.4);
  \draw[otGreenDark,line width=0.9pt] (0.8,0.8) rectangle (4.8,3.6);
  \node[text=otGreenDark] at (2.8,2.45) {parterre};
  \node[note,fill=none] at (2.8,1.95) {$8$ m sur $6$ m};
  \node[note,fill=none] at (2.8,4.0) {allée};
  \draw[cote] (4.8,2.2) -- (5.6,2.2);
  \node[anchor=south,text=otInk,inner sep=1.5pt] at (5.2,2.3) {$x$};
  \draw[cote] (2.0,0) -- (2.0,0.8);
  \node[anchor=west,text=otInk,inner sep=1.5pt] at (2.1,0.4) {$x$};
\end{tikzpicture}""",
}

# Graduations de l'axe des abscisses placées à la main (côté libre de la courbe).
XLAB = {
    "cours_formes": [(-3, "g", "-3"), (-2, "c", "-2"), (-1, "d", "-1"), (1, "d", "1")],
    "projectile_ds2": [(0.6838, "c", "0{,}68"), (1, "c", "1"), (1.3162, "c", "1{,}32"), (2, "c", "2")],
}


# =====================================================================
# Finition du 2026-11-02 : figures ajoutées (fiche, énoncés, corrigés)
# Réponses en vert foncé (otGreenDark), sommets en orange, signes : bande
# verte (> 0 ou réponse) / orange (< 0) posée sur l'axe des abscisses.
# =====================================================================
VERT = "otGreenDark"
ORANGE_T = "otOrange!80!black"
PETIT = r"\otRegular\fontsize{8.5}{10}\selectfont"
GRAD = r"\otRegular\fontsize{9}{10}\selectfont"


def bande(a, b, couleur):
    return rf"  \draw[{couleur},line width=3pt,line cap=butt,opacity=0.9] (axis cs:{a},0) -- (axis cs:{b},0);" "\n"


def lab_racine(x, y, ancre, texte, couleur=VERT):
    """Étiquette d'une racine, placée du côté libre de la courbe."""
    return rf"\node[anchor={ancre},text={couleur},font={GRAD},inner sep=1pt] at (axis cs:{x},{y}) {{{texte}}};"


def parabole(expr, dom, fen, xt, yt, taille=(6.4, 4.6), bandes=(), bornes=(), points=(), noeuds=(),
             legende=(), axes=("$x$", "$y$"), avant="", options="", sans_xlab=False):
    xmin, xmax, ymin, ymax = fen
    opt = rf"otWeb, name=ax, width={taille[0]}cm, height={taille[1]}cm, xmin={xmin}, xmax={xmax}, ymin={ymin}, ymax={ymax}, xtick={{{xt}}}, ytick={{{yt}}}, xlabel={{{axes[0]}}}, ylabel={{{axes[1]}}}"
    if sans_xlab:
        opt += ", xticklabels={}"
    if options:
        opt += ", " + options
    code = r"\begin{tikzpicture}" "\n" + rf"\begin{{axis}}[{opt}]" "\n" + avant
    code += rf"  \addplot[courbe, domain={dom}] {{{expr}}};" "\n"
    for a, b, c in bandes:
        code += bande(a, b, c)
    for x, ferme in bornes:
        code += (rf"  \borneF{{{x}}}" if ferme else rf"  \borneO{{{x}}}") + "\n"
    for x, y, c in points:
        code += rf"  \pnt[{c}]{{{x}}}{{{y}}}" "\n"
    for n in noeuds:
        code += "  " + n + "\n"
    code += r"\end{axis}" "\n"
    for i, (texte, c) in enumerate(legende):
        code += rf"\node[anchor=north west,text={c},font={PETIT}] at ($(ax.outer south west)+(0.1,{-0.05 - 0.48 * i:.2f})$) {{{texte}}};" "\n"
    return code + r"\end{tikzpicture}"


# ------------------------------------------------------------------ 1314 : trois paraboles, trois cas
def _mini_delta(nom, place, expr, dom, titre, sous_titre, racines, etiquettes):
    code = (rf"\begin{{axis}}[otWeb, name={nom}{place}, width=2.55cm, height=2.9cm, xmin=-0.5, xmax=4.5, ymin=-1.7, ymax=4.3,"
            r" xtick={1,2,3}, xticklabels={}, ytick={1,2,3,4}, yticklabels={}, xlabel={}, ylabel={}]" "\n")
    code += rf"  \addplot[courbe, domain={dom}] {{{expr}}};" "\n"
    for x in racines:
        code += rf"  \borneF{{{x}}}" "\n"
    for x, y, ancre, t in etiquettes:
        code += "  " + lab_racine(x, y, ancre, t) + "\n"
    code += r"\end{axis}" "\n"
    code += (rf"\node[anchor=south,align=center,text=otNavy] at ($({nom}.north)+(0,0.12)$) {{{titre}\\[-1pt]"
             rf"{{{PETIT}\color{{otMuted}}{sous_titre}}}}};" "\n")
    return code


FIGURES["trois_paraboles"] = (r"\begin{tikzpicture}" "\n"
    + _mini_delta("F", "", "(x-2)^2-1", "-0.26:4.26", r"$f$ : $\Delta = 4$", "deux racines", [1, 3],
                  [(0.9, -0.2, "north east", "1"), (3.1, -0.2, "north west", "3")])
    + _mini_delta("G", ", at={(F.east)}, anchor=west, xshift=0.55cm", "(x-2)^2", "-0.02:4.02", r"$g$ : $\Delta = 0$",
                  "racine double", [2], [(2, -0.25, "north", "2")])
    + _mini_delta("H", ", at={(G.east)}, anchor=west, xshift=0.55cm", "(x-2)^2+1", "0.24:3.76", r"$h$ : $\Delta = -4$",
                  "aucune racine", [], [])
    + r"\end{tikzpicture}")

# ------------------------------------------------------------------ 1324 (DS 1)
FIGURES["ds1_rectangle"] = r"""
\begin{tikzpicture}
  \coordinate (A) at (0,0); \coordinate (B) at (4.4,0); \coordinate (C) at (4.4,2.4); \coordinate (D) at (0,2.4);
  \fill[otSky] (A) rectangle (C);
  \draw[geoTrait] (A) -- (B) -- (C) -- (D) -- cycle;
  \cote[0.4]{B}{A}{$x$}
  \cote[0.85]{C}{B}{$8 - x$}
  \node[anchor=north east] at ($(A)+(-0.06,-0.06)$) {$A$};
  \node[anchor=north west] at ($(B)+(0.06,-0.06)$) {$B$};
  \node[anchor=south west] at ($(C)+(0.06,0.06)$) {$C$};
  \node[anchor=south east] at ($(D)+(-0.06,0.06)$) {$D$};
\end{tikzpicture}"""

FIGURES["ds1_f"] = parabole(
    "2*(x-2)^2-2", "-0.12:4.12", (-0.8, 4.8, -3.0, 7.2), "1,2,3", "-2,2,4", sans_xlab=True,
    bandes=[(-0.7, 1, "otGreen"), (1, 3, "otOrange"), (3, 4.7, "otGreen")], bornes=[(1, True), (3, True)],
    points=[(2, -2, "otOrange!90!black")],
    noeuds=[lab_racine(0.92, -0.3, "north east", "1"), lab_racine(3.08, -0.3, "north west", "3"),
            rf"\node[note,fill=none,anchor=north,text={ORANGE_T}] at (axis cs:2,-2.3) {{sommet $S(2\,;-2)$}};"],
    legende=[(r"en vert : $f(x) > 0$ ; en orange : $f(x) < 0$", "otInk")])

FIGURES["ds1_aire"] = parabole(
    "-x^2+8*x", "0:8", (-0.8, 9.2, -2, 19.5), "2,4,6,8", "4,8,12,16", axes=("$x$", r"$\mathcal{A}(x)$"),
    avant=r"  \guides{4}{16}" "\n", points=[(4, 16, VERT)],
    noeuds=[rf"\node[note,fill=none,anchor=south,text={VERT}] at (axis cs:4,16.5) {{maximum $16$ pour $x = 4$}};"],
    legende=[(r"$AB = 4$ et $BC = 8 - 4 = 4$ : le rectangle est un carré", VERT)])

# ------------------------------------------------------------------ 1325 (DS 2) partie B
FIGURES["ds2_f"] = parabole(
    "-(x-2)^2+1", "-0.24:4.24", (-0.7, 4.7, -4.3, 2.4), "1,2,3", "-3,-2,-1,1", sans_xlab=True,
    bandes=[(-0.6, 1, "otOrange"), (1, 3, "otGreen"), (3, 4.6, "otOrange")], bornes=[(1, True), (3, True)],
    points=[(2, 1, VERT)],
    noeuds=[lab_racine(1.08, -0.3, "north west", "1"), lab_racine(2.92, -0.3, "north east", "3"),
            rf"\node[note,fill=none,anchor=south,text={VERT}] at (axis cs:2,1.2) {{maximum $1$ en $x = 2$}};"],
    legende=[(r"en vert : $f(x) > 0$ ; en orange : $f(x) < 0$", "otInk")])

# ------------------------------------------------------------------ 1328 (DS 3)
FIGURES["ds3_h"] = parabole(
    "(x-3)^2-1", "0.6:5.4", (-0.6, 6.4, -2.6, 5.6), "2,3,4", "2,4", sans_xlab=True,
    bandes=[(2, 4, "otGreen")], bornes=[(2, True), (4, True)], points=[(3, -1, "otOrange!90!black")],
    noeuds=[lab_racine(1.92, -0.3, "north east", "2"), lab_racine(4.08, -0.3, "north west", "4"),
            rf"\node[note,fill=none,anchor=north,text={ORANGE_T}] at (axis cs:3,-1.3) {{sommet $S(3\,;-1)$}};"],
    legende=[(r"en vert : $h(x) \le 0$ pour $x \in [2\,;4]$", VERT)])

FIGURES["ds3_ballon"] = parabole(
    "-5*x^2+20*x+5", "0:4.2361", (0, 5.4, 0, 30), "1,2,3,4", "5,10,15,20,25", axes=("$t$", "$H$"),
    avant=r"  \guides{2}{25}" "\n", points=[(0, 5, "otNavy"), (2, 25, VERT), (4.2361, 0, VERT)],
    noeuds=[rf"\node[note,fill=none,anchor=south,text={VERT}] at (axis cs:2,25.7) {{maximum : $25$ m à $t = 2$ s}};",
            r"\node[note,fill=none,anchor=west] at (axis cs:0.2,3.6) {départ : $5$ m};",
            rf"\node[note,fill=none,anchor=south west,text={VERT}] at (axis cs:4.3,1.0) {{sol : $t \approx 4{{,}}24$ s}};"])

# ------------------------------------------------------------------ 1318 : signe de k et de g
FIGURES["signe_kg"] = (r"\begin{tikzpicture}" "\n"
    r"\begin{axis}[otWeb, name=L, width=3.4cm, height=3.6cm, xmin=-0.5, xmax=4.5, ymin=-2.6, ymax=4.6,"
    r" xtick={1,2,3}, xticklabels={}, ytick={-2,2,4}, xlabel={$x$}, ylabel={}]" "\n"
    r"  \addplot[courbe, domain=0.21:3.79] {2*(x-1)*(x-3)};" "\n"
    + bande(1, 3, "otGreen") + r"  \borneF{1} \borneF{3}" "\n"
    + "  " + lab_racine(0.92, -0.3, "north east", "1") + "\n"
    + "  " + lab_racine(3.08, -0.3, "north west", "3") + "\n"
    r"\end{axis}" "\n"
    rf"\node[anchor=south,text={VERT},font={PETIT}] at ($(L.north)+(0,0.12)$) {{$k(x) \le 0$ sur $[1\,;3]$}};" "\n"
    r"\begin{axis}[otWeb, name=R, at={(L.east)}, anchor=west, xshift=1.2cm, width=3.4cm, height=3.6cm, xmin=-0.5, xmax=4.5,"
    r" ymin=-4.6, ymax=1.6, xtick={1,2,3}, xticklabels={}, ytick={-4,-2}, xlabel={$x$}, ylabel={}]" "\n"
    r"  \addplot[courbe, domain=-0.1:4.1] {-(x-2)^2};" "\n"
    + bande(-0.45, 2, "otGreen") + bande(2, 4.4, "otGreen") + r"  \borneO{2}" "\n"
    + "  " + lab_racine(2, 0.3, "south", "2") + "\n"
    r"\end{axis}" "\n"
    rf"\node[anchor=south,text={VERT},font={PETIT}] at ($(R.north)+(0,0.12)$) {{$g(x) < 0$ pour $x \neq 2$}};" "\n"
    r"\end{tikzpicture}")

# ------------------------------------------------------------------ 1317 : même sommet, deux paraboles
FIGURES["canon_fg"] = parabole(
    "(x-2)^2-3", "-0.5:4.5", (-0.8, 5.4, -4.4, 4.6), "1,2,3,4", "-3,-1,1,3", sans_xlab=True,
    avant=r"  \addplot[otOrange,line width=1.35pt, domain=0.4:3.6] {2*(x-2)^2-3};" "\n",
    points=[(2, -3, VERT)],
    noeuds=[r"\node[etiq,fill=none,anchor=west,text=otNavy] at (axis cs:4.55,3.25) {$\mathcal{C}_f$};",
            r"\node[etiq,fill=none,anchor=west,text=otOrange!80!black] at (axis cs:3.65,2.1) {$\mathcal{C}_g$};",
            rf"\node[note,fill=none,anchor=north,text={VERT}] at (axis cs:2,-3.3) {{même sommet $S(2\,;-3)$}};"],
    legende=[(r"$f(x) = (x - 2)^2 - 3$ (bleu) ; $g(x) = 2(x - 2)^2 - 3$ (orange)", "otInk")])

# ------------------------------------------------------------------ 1322 : f(x) = -2(x-3)^2 + 2
FIGURES["synthese_f"] = parabole(
    "-2*(x-3)^2+2", "1.5:4.5", (-0.5, 5.8, -2.9, 3.3), "2,3,4", "-2,2", sans_xlab=True,
    bandes=[(-0.4, 2, "otOrange"), (2, 4, "otGreen"), (4, 5.7, "otOrange")], bornes=[(2, False), (4, False)],
    points=[(3, 2, VERT)],
    noeuds=[lab_racine(2.08, -0.3, "north west", "2"), lab_racine(3.92, -0.3, "north east", "4"),
            rf"\node[note,fill=none,anchor=south,text={VERT}] at (axis cs:3,2.2) {{maximum $2$ en $x = 3$}};"],
    legende=[(r"en vert : $f(x) > 0$ pour $x \in {]2\,;4[}$", VERT)])


def triangle(corrige):
    c = VERT if corrige else "otInk"
    a_, b_, c_ = (r"$a = 6$", r"$b = 8$", r"$c = 10$") if corrige else ("$a$", "$b$", "$c$")
    return rf"""
\begin{{tikzpicture}}
  \coordinate (R) at (0,0); \coordinate (P) at (4.8,0); \coordinate (Q) at (0,3.6);
  \fill[otSky] (R) -- (P) -- (Q) -- cycle;
  \draw[geoTrait] (R) -- (P) -- (Q) -- cycle;
  \angledroit{{P}}{{R}}{{Q}}
  \node[anchor=east,text={c}] at (-0.12,1.8) {{{a_}}};
  \node[anchor=north,text={c}] at (2.4,-0.12) {{{b_}}};
  \node[anchor=south west,text={c}] at (2.52,1.95) {{{c_}}};
  \node[anchor=north west,text=otMuted,font={PETIT}] at (-0.3,-0.65) {{périmètre $24$ cm ; aire $24$ cm²}};
\end{{tikzpicture}}"""


FIGURES["triangle_enonce"] = triangle(False)
FIGURES["triangle_corrige"] = triangle(True)


# ------------------------------------------------------------------ 1426 et nouveau-1 : corrigés en 2 × 2
def quatre_corrige(titre, courbes, ymin, ymax, yticks, extras):
    style = (
        r"\pgfplotsset{mini/.style={otWeb, axis lines=box, axis line style={otMuted!60,line width=0.5pt,-},"
        r" tick pos=left, major tick length=2pt, xlabel={}, ylabel={},"
        r" yticklabel style={anchor=east,xshift=-1.5pt,yshift=0pt}, xticklabel style={anchor=north,yshift=-1.5pt},"
        rf" width=3.3cm, height=3.3cm, xmin=-4.4, xmax=4.4, ymin={ymin}, ymax={ymax},"
        rf" xtick={{-4,-2,0,2,4}}, ytick={{{yticks}}}, minor tick num=1, grid=both,"
        r" minor grid style={otRule!60,line width=0.3pt}, minor tick length=0pt}}" "\n"
    )
    code = r"\begin{tikzpicture}" "\n" + style
    places = ["", ", at={(A.east)}, anchor=west, xshift=1.25cm", ", at={(A.south)}, anchor=north, yshift=-1.55cm",
              ", at={(C.east)}, anchor=west, xshift=1.25cm"]
    for nom, place, (indice, expr, dom, pts), ext in zip("ABCD", places, courbes, extras):
        code += rf"\begin{{axis}}[mini, name={nom}{place}]" "\n"
        code += (rf"  \draw[otMuted,line width=0.7pt,-{{Stealth[length=1.5mm]}}] (axis cs:-4.4,0) -- (axis cs:4.4,0);" "\n"
                 rf"  \draw[otMuted,line width=0.7pt,-{{Stealth[length=1.5mm]}}] (axis cs:0,{ymin}) -- (axis cs:0,{ymax});" "\n")
        code += ext.get("avant", "")
        code += rf"  \addplot[courbe, domain={dom}] {{{expr}}};" "\n"
        code += "".join(rf"  \pnt{{{x}}}{{{y}}}" "\n" for x, y in pts)
        code += ext.get("apres", "")
        code += r"\end{axis}" "\n"
        code += rf"\node[anchor=south,text=otNavy] at ($({nom}.north)+(0,0.12)$) {{{titre} ${indice}$}};" "\n"
    return code + r"\end{tikzpicture}"


def vecteur(x, y):
    return (rf"  \draw[otGreenDark,line width=1.1pt,-{{Stealth[length=2.2mm]}}] (axis cs:0,0) -- (axis cs:{x},{y});" "\n"
            rf"  \pnt[otGreenDark]{{{x}}}{{{y}}}" "\n")


PALE_A = r"  \addplot[pale, domain=-2.5:2.5] {x^2};" "\n"
FIGURES["translations_corrige"] = quatre_corrige("Parabole", [
    (r"\mathcal{P}_A", "x^2", "-2.5:2.5", []),
    (r"\mathcal{P}_B", "x^2-3", "-3.0:3.0", []),
    (r"\mathcal{P}_C", "(x-2)^2", "-0.5:4.4", []),
    (r"\mathcal{P}_D", "(x+1)^2+2", "-3.0:1.0", []),
], -4.4, 6.4, "-4,-2,0,2,4,6", [
    {"apres": r"  \pnt[otGreenDark]{0}{0}" "\n"},
    {"avant": PALE_A, "apres": vecteur(0, -3)},
    {"avant": PALE_A, "apres": vecteur(2, 0)},
    {"avant": PALE_A, "apres": vecteur(-1, 2)},
])

FIGURES["lecture_corrige"] = quatre_corrige("Courbe", [
    (r"\mathcal{C}_1", "(x-1)^2-4", "-2.0:4.0", [(1, -4)]),
    (r"\mathcal{C}_2", "-(x-2)^2", "-0.3:4.4", [(0, -4)]),
    (r"\mathcal{C}_3", "0.5*(x+1)^2+1", "-4.0:2.0", [(-1, 1), (1, 3)]),
    (r"\mathcal{C}_4", "-(x+1)^2+4", "-4.0:2.0", [(-1, 4)]),
], -5.4, 5.4, "-4,-2,0,2,4", [
    {"apres": bande(-1, 3, "otGreen") + r"  \borneO{-1} \borneO{3}" "\n"},
    {"apres": r"  \borneF{2}" "\n"},
    {},
    {"apres": bande(-3, 1, "otGreen") + r"  \borneF{-3} \borneF{1}" "\n"},
])

# ------------------------------------------------------------------ 1323 : corrigés des quatre situations
FIGURES["parterre_corrige"] = r"""
\begin{tikzpicture}
  \fill[otMuted!18] (0,0) rectangle (5.6,4.4);
  \fill[otGreen!25] (0.8,0.8) rectangle (4.8,3.6);
  \draw[otMuted,line width=0.9pt] (0,0) rectangle (5.6,4.4);
  \draw[otGreenDark,line width=0.9pt] (0.8,0.8) rectangle (4.8,3.6);
  \node[text=otGreenDark] at (2.8,2.45) {parterre};
  \node[note,fill=none] at (2.8,1.95) {$8$ m sur $6$ m};
  \node[note,fill=none] at (2.8,4.0) {allée};
  \draw[cote] (4.8,2.2) -- (5.6,2.2);
  \node[anchor=south,text=otGreenDark,inner sep=1.5pt] at (5.2,2.3) {$x$};
  \draw[cote] (2.0,0) -- (2.0,0.8);
  \node[anchor=west,text=otGreenDark,inner sep=1.5pt] at (2.1,0.4) {$x = 1$ m};
  \cote[0.45]{5.6,0}{0,0}{{\color{otGreenDark}$10$ m}}
  \cote[0.45]{0,0}{0,4.4}{{\color{otGreenDark}$8$ m}}
  \node[anchor=north west,text=otGreenDark,font=""" + PETIT + r"""] at (-0.6,-0.85) {aire totale : $10 \times 8 = 80$ m²};
\end{tikzpicture}"""

FIGURES["fenetre_corrige"] = r"""
\begin{tikzpicture}
  \fill[otSky] (0,0) rectangle (4.03,2.02);
  \fill[otSky] (4.03,2.02) arc[start angle=0,end angle=180,radius=2.015];
  \draw[otNavy,line width=1.2pt,line join=round] (0,2.02) -- (0,0) -- (4.03,0) -- (4.03,2.02) arc[start angle=0,end angle=180,radius=2.015];
  \draw[otNavy!45,line width=0.6pt,dash pattern=on 3pt off 2pt] (0,2.02) -- (4.03,2.02);
  \cote[0.45]{4.03,0}{0,0}{$x$}
  \cote[0.45]{4.03,2.02}{4.03,0}{$h$}
  \node[text=otGreenDark,align=center,font=""" + PETIT + r"""] at (2.015,1.0) {aire maximale\\$\approx 2{,}52$ m²};
  \node[anchor=north west,text=otGreenDark,font=""" + PETIT + r"""] at (-0.3,-0.85) {$x = \frac{12}{4 + \pi} \approx 1{,}68$ m et $h = \frac{6}{4 + \pi} \approx 0{,}84$ m};
\end{tikzpicture}"""

FIGURES["projectile_1323"] = parabole(
    "-5*x^2+30*x", "0:6", (0, 6.9, 0, 53), "1,2,3,4,5,6", "10,20,30,40", sans_xlab=True, axes=("$t$", "$h$"),
    avant=r"  \draw[seuil] (axis cs:0,40) -- (axis cs:6.7,40);" "\n" r"  \guidev{2}{40} \guidev{4}{40}" "\n"
          r"  \guidev{3}{45}" "\n",
    bandes=[(2, 4, "otGreen")], bornes=[(2, False), (4, False)], points=[(3, 45, VERT), (6, 0, VERT)],
    noeuds=[rf"\node[note,fill=none,anchor=south,text={VERT}] at (axis cs:3,45.8) {{maximum : $45$ m}};",
            rf"\node[note,fill=none,anchor=south east,text={ORANGE_T}] at (axis cs:6.7,40.8) {{$h = 40$}};",
            rf"\node[note,fill=none,anchor=south west,text={VERT}] at (axis cs:6.08,1.2) {{sol}};"],
    legende=[(r"plus de $40$ m pour $t \in {]2\,;4[}$, soit pendant $2$ s", VERT)])

# ------------------------------------------------------------------ 1320 : jardin (énoncé) et recette (corrigé)
FIGURES["jardin_enonce"] = r"""
\begin{tikzpicture}
  \fill[otGreen!12] (0,0) rectangle (5.4,3.1);
  \fill[otGreen!35] (0,0) rectangle (4,2.4);
  \draw[otGreenDark,line width=0.9pt] (0,0) rectangle (4,2.4);
  \draw[otNavy,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (0,0) rectangle (5.4,3.1);
  \node[text=otGreenDark,align=center] at (2,1.2) {jardin initial\\[-1pt]{""" + PETIT + r""" aire $24$ m²}};
  \node[text=otNavy,font=""" + PETIT + r"""] at (2.4,2.75) {jardin agrandi : aire $40$ m²};
  \cote[0.45]{4,0}{0,0}{$L$}
  \cote[0.45]{5.4,0}{4,0}{$2$}
  \cote[0.45]{0,0}{0,2.4}{$\ell$}
  \cote[0.45]{0,2.4}{0,3.1}{$1$}
\end{tikzpicture}"""

FIGURES["theatre_recette"] = parabole(
    "-25*x^2+200*x+6000", "0:20", (-1, 21.5, -500, 7700), "4,8,12,16,20", "2000,4000,6000",
    axes=("$x$", "$R(x)$"), options="scaled y ticks=false",
    avant=r"  \guides{4}{6400}" "\n", points=[(0, 6000, "otNavy"), (4, 6400, VERT)],
    noeuds=[rf"\node[note,fill=none,anchor=south west,text={VERT}] at (axis cs:4.4,6550) {{maximum : $6\,400$ € pour $x = 4$}};"],
    legende=[(r"baisse de $4$ € : place à $16$ €, $400$ spectateurs", VERT)])

# ------------------------------------------------------------------ 1326 : bénéfice de l'artisan
FIGURES["benefice"] = parabole(
    "-x^2+40*x-300", "0:42", (-2, 45, -430, 175), "10,20,30,40", "-300,-200,-100,100", sans_xlab=True,
    axes=("$q$", "$B(q)$"), options="scaled y ticks=false",
    avant=r"  \guidev{20}{100}" "\n",
    bandes=[(10, 30, "otGreen")], bornes=[(10, True), (30, True)], points=[(20, 100, VERT)],
    noeuds=[rf"\node[note,fill=none,anchor=south,text={VERT}] at (axis cs:20,112) {{maximum : $100$ €}};"],
    legende=[(r"en vert : $B(q) \ge 0$ (pas de perte) pour $q \in [10\,;30]$", VERT)])

# ------------------------------------------------------------------ 1327 : champ le long d'un mur
FIGURES["champ_aire"] = parabole(
    "-2*x^2+100*x", "0:50", (-2, 54, -90, 1480), "10,20,30,40,50", "400,800,1200", sans_xlab=True,
    axes=("$x$", r"$\mathcal{A}(x)$"), options="scaled y ticks=false",
    avant=r"  \draw[seuil] (axis cs:0,1200) -- (axis cs:53,1200);" "\n" r"  \guidev{20}{1200} \guidev{30}{1200}" "\n",
    bandes=[(20, 30, "otGreen")], bornes=[(20, True), (30, True)], points=[(25, 1250, VERT)],
    noeuds=[rf"\node[note,fill=none,anchor=south,text={VERT}] at (axis cs:25,1285) {{maximum : $1\,250$ m² pour $x = 25$}};",
            rf"\node[note,fill=none,anchor=north east,text={ORANGE_T}] at (axis cs:53,1180) {{$1\,200$ m²}};"],
    legende=[(r"en vert : $\mathcal{A}(x) \ge 1\,200$ pour $x \in [20\,;30]$", VERT)])


def enclos_corrige(xv, yv, aire):
    return r"""
\begin{tikzpicture}
  \fill[otMuted!25] (-0.4,3.0) rectangle (6.4,3.35);
  \fill[pattern=north east lines,pattern color=otMuted!80] (-0.4,3.0) rectangle (6.4,3.35);
  \draw[otMuted,line width=0.8pt] (-0.4,3.0) -- (6.4,3.0);
  \node[anchor=south,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted] at (3,3.4) {mur existant (pas de clôture)};
  \fill[otGreen!12] (0,0) rectangle (6,3.0);
  \draw[otNavy,line width=1.6pt,line join=round] (0,3.0) -- (0,0) -- (6,0) -- (6,3.0);
  \node[anchor=east,text=otGreenDark] at (-0.12,1.5) {$x = """ + xv + r"""$ m};
  \node[anchor=west,text=otGreenDark] at (6.12,1.5) {$""" + xv + r"""$ m};
  \node[anchor=north,text=otGreenDark] at (3,-0.12) {$y = """ + yv + r"""$ m};
  \node[text=otGreenDark] at (3,1.5) {aire maximale : $""" + aire + r"""$ m²};
\end{tikzpicture}"""


FIGURES["enclos_25"] = enclos_corrige("25", "50", r"1\,250")
FIGURES["enclos_7"] = enclos_corrige("7", "14", "98")


# ------------------------------------------------------------------ 1329 : carré inscrit (exercice 2 réécrit)
def carre_inscrit(xv, corrige):
    s = 4.2
    a = xv * s / 10
    remplissage = "otGreen!22" if corrige else "otSky"
    trait = "otGreenDark,line width=1.1pt,line join=round" if corrige else "geoTrait"
    lab = (rf"${xv}$" if corrige else "$x$")
    lc = VERT if corrige else "otInk"
    code = rf"""
\begin{{tikzpicture}}
  \coordinate (A) at (0,0); \coordinate (B) at ({s},0); \coordinate (C) at ({s},{s}); \coordinate (D) at (0,{s});
  \coordinate (M) at ({a:.3f},0); \coordinate (N) at ({s},{a:.3f}); \coordinate (P) at ({s - a:.3f},{s}); \coordinate (Q) at (0,{s - a:.3f});
  \fill[{remplissage}] (M) -- (N) -- (P) -- (Q) -- cycle;
  \draw[geoTrait] (A) -- (B) -- (C) -- (D) -- cycle;
  \draw[{trait}] (M) -- (N) -- (P) -- (Q) -- cycle;
  \cote[0.38]{{M}}{{A}}{{{{\color{{{lc}}}{lab}}}}}
  \cote[0.38]{{N}}{{B}}{{{{\color{{{lc}}}{lab}}}}}
  \cote[0.38]{{P}}{{C}}{{{{\color{{{lc}}}{lab}}}}}
  \cote[0.38]{{Q}}{{D}}{{{{\color{{{lc}}}{lab}}}}}
  \node[anchor=north east] at ($(A)+(-0.06,-0.06)$) {{$A$}};
  \node[anchor=north west] at ($(B)+(0.06,-0.06)$) {{$B$}};
  \node[anchor=south west] at ($(C)+(0.06,0.06)$) {{$C$}};
  \node[anchor=south east] at ($(D)+(-0.06,0.06)$) {{$D$}};
  \node[anchor=north west,inner sep=1pt] at ($(M)+(0.12,-0.08)$) {{$M$}};
  \node[anchor=south west,inner sep=1pt] at ($(N)+(0.08,0.12)$) {{$N$}};
  \node[anchor=south east,inner sep=1pt] at ($(P)+(-0.12,0.08)$) {{$P$}};
  \node[anchor=north east,inner sep=1pt] at ($(Q)+(-0.08,-0.12)$) {{$Q$}};
"""
    if corrige:
        code += rf"  \node[text={VERT},align=center,font={PETIT}] at ({s / 2},{s / 2}) {{aire minimale\\$50$ cm²}};" "\n"
        code += rf"  \node[anchor=north west,text={VERT},font={PETIT}] at (-0.4,-0.95) {{$x = 5$ : $M$, $N$, $P$, $Q$ sont les milieux des côtés}};" "\n"
    return code + r"\end{tikzpicture}"


FIGURES["carre_inscrit_enonce"] = carre_inscrit(3, False)
FIGURES["carre_inscrit_corrige"] = carre_inscrit(5, True)


# ------------------------------------------------------------------ 1329 exercice 3 : trois valeurs de m
def _mini_m(nom, place, expr, dom, titre, sous_titre, racines, etiquettes=()):
    code = (rf"\begin{{axis}}[otWeb, name={nom}{place}, width=2.4cm, height=2.9cm, xmin=-4.8, xmax=1.8, ymin=-4.6, ymax=5.2,"
            r" xtick={-4,-2}, xticklabels={}, ytick={-4,-2,2,4}, yticklabels={}, xlabel={}, ylabel={}]" "\n")
    code += rf"  \addplot[courbe, domain={dom}] {{{expr}}};" "\n"
    for x in racines:
        code += rf"  \borneF{{{x}}}" "\n"
    for x, y, ancre, t in etiquettes:
        code += "  " + lab_racine(x, y, ancre, t) + "\n"
    code += r"\end{axis}" "\n"
    code += (rf"\node[anchor=south,align=center,text=otNavy] at ($({nom}.north)+(0,0.12)$) {{{titre}\\[-1pt]"
             rf"{{{PETIT}\color{{otMuted}}{sous_titre}}}}};" "\n")
    return code


FIGURES["param_cas"] = (r"\begin{tikzpicture}" "\n"
    + _mini_m("U", "", "x^2+4*x", "-4.8:1", r"$m = -2$ : $\Delta_m > 0$", "deux racines", [-4, 0],
              [(-4.1, -0.35, "north east", "$-4$"), (0.12, -0.35, "north west", "$0$")])
    + _mini_m("V", ", at={(U.east)}, anchor=west, xshift=0.85cm", "(x+1)^2", "-3.24:1.24", r"$m = -1$ : $\Delta_m = 0$",
              "racine double", [-1], [(-1, -0.4, "north", "$-1$")])
    + _mini_m("W", ", at={(V.east)}, anchor=west, xshift=0.85cm", "x^2+2", "-1.73:1.73", r"$m = 0$ : $\Delta_m < 0$",
              "aucune racine", [])
    + r"\end{tikzpicture}")

# ------------------------------------------------------------------ nouveau-2 : droite tangente
FIGURES["parabole_tangente"] = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, name=ax, width=6.4cm, height=5.4cm, xmin=-1.8, xmax=4.8, ymin=-4.2, ymax=6.4,
  xtick={-1,1,2,3,4}, ytick={-2,2,4,6}]
  \addplot[pale, domain=-1:4] {2*x-2};
  \addplot[pale, domain=2:4.6] {2*x-8};
  \addplot[courbe, domain=-1.5:3.83] {x^2-2*x-1};
  \addplot[otGreenDark,line width=1.2pt, domain=0.5:4.6] {2*x-5};
  \pnt[otGreenDark]{2}{-1}
  \node[etiq,fill=none,anchor=north west,text=otGreenDark] at (axis cs:2.08,-1.12) {$T$};
  \node[etiq,fill=none,anchor=east,text=otNavy] at (axis cs:-1.55,4.6) {$\mathcal{P}$};
  \node[note,fill=none,anchor=west,text=otNavy!60] at (axis cs:4.05,6.0) {$\mathcal{D}_{-2}$};
  \node[note,fill=none,anchor=west,text=otGreenDark] at (axis cs:4.65,4.2) {$\mathcal{D}_{-5}$};
  \node[note,fill=none,anchor=west,text=otNavy!60] at (axis cs:4.65,1.2) {$\mathcal{D}_{-8}$};
\end{axis}
\node[anchor=north west,text=otGreenDark,font=""" + PETIT + r"""] at ($(ax.outer south west)+(0.1,-0.05)$) {$\mathcal{D}_{-5}$ touche $\mathcal{P}$ en un seul point : $T(2\,;-1)$};
\node[anchor=north west,text=otNavy!70,font=""" + PETIT + r"""] at ($(ax.outer south west)+(0.1,-0.53)$) {$\mathcal{D}_{-2}$ : deux points communs ; $\mathcal{D}_{-8}$ : aucun};
\end{tikzpicture}"""

XLAB.update({
    "projectile_1323": [(1, "c", "1"), (2, "c", "2"), (3, "c", "3"), (4, "c", "4"), (5, "c", "5"), (6, "d", "6")],
    "benefice": [(10, "d", "10"), (20, "c", "20"), (30, "g", "30"), (40, "c", "40")],
    "champ_aire": [(10, "c", "10"), (20, "c", "20"), (30, "c", "30"), (40, "c", "40"), (50, "d", "50")],
    "canon_fg": [(2, "c", "2"), (4, "c", "4")],
})
