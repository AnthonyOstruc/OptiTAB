# -*- coding: utf-8 -*-
"""Figures de la notion « Utiliser le calcul littéral » (Seconde), style des livres.

Compilées par outils/figures_livre.py.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  axe/.style={otMuted,line width=.6pt,-{Stealth[length=2.2mm]}},
  grad/.style={otMuted,line width=.5pt},
  gradTexte/.style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=north,inner sep=1pt},
  bande/.style={line width=3.2pt,line cap=butt},
  crochet/.style={line width=1.3pt,line join=miter},
  zone/.style={font=\Large,text=otInk},
}
"""


def f(v):
    """Nombre TikZ (point décimal)."""
    return ("%.4f" % v).rstrip("0").rstrip(".")


def crochet(x, y, sens, couleur="otGreenDark", h=.2, l=.11):
    """Crochet en x : sens=+1 « [ » (ouvert vers la droite), -1 « ] »."""
    return r"\draw[crochet,%s] ([xshift=%scm]%s,%s) -- (%s,%s) -- (%s,%s) -- ([xshift=%scm]%s,%s);" % (
        couleur, f(sens * l), f(x), f(y + h), f(x), f(y + h), f(x), f(y - h), f(sens * l), f(x), f(y - h))


# ------------------------------------------------------------------ carré (a+b)^2
A, B = 3.0, 1.7
S = A + B
CARRE = r"""
\begin{tikzpicture}
\fill[otSky] (0,%(b)s) rectangle (%(a)s,%(s)s);
\fill[otOrange!16] (%(a)s,%(b)s) rectangle (%(s)s,%(s)s);
\fill[otOrange!16] (0,0) rectangle (%(a)s,%(b)s);
\fill[otGreen!16] (%(a)s,0) rectangle (%(s)s,%(b)s);
\draw[geoTrait] (0,0) rectangle (%(s)s,%(s)s);
\draw[geoTrait] (%(a)s,0) -- (%(a)s,%(s)s);
\draw[geoTrait] (0,%(b)s) -- (%(s)s,%(b)s);
\node[zone] at (%(ma)s,%(mta)s) {$a^2$};
\node[zone] at (%(mb)s,%(mta)s) {$ab$};
\node[zone] at (%(ma)s,%(mtb)s) {$ab$};
\node[zone] at (%(mb)s,%(mtb)s) {$b^2$};
\coordinate (H0) at (0,%(s)s); \coordinate (H1) at (%(a)s,%(s)s); \coordinate (H2) at (%(s)s,%(s)s);
\coordinate (V0) at (0,0); \coordinate (V1) at (0,%(b)s); \coordinate (V2) at (0,%(s)s);
\cote[0.45]{H0}{H1}{\large $a$}
\cote[0.45]{H1}{H2}{\large $b$}
\cote[0.45]{V1}{V2}{\large $a$}
\cote[0.45]{V0}{V1}{\large $b$}
\node[text=otGreenDark,font=\large,anchor=north] at (%(m)s,-0.3) {$(a+b)^2=a^2+2ab+b^2$};
\end{tikzpicture}""" % {"a": f(A), "b": f(B), "s": f(S), "ma": f(A / 2), "mb": f(A + B / 2),
                         "mta": f(B + A / 2), "mtb": f(B / 2), "m": f(S / 2)}

# ------------------------------------------------------------------ droite graduée x >= 3
def droite_x_ge_3():
    s = [r"\begin{tikzpicture}[x=0.75cm]"]
    s.append(r"\draw[bande,otGreen!85] (3,0) -- (6.55,0);")
    s.append(r"\draw[axe] (-1.5,0) -- (6.8,0);")
    for t in range(-1, 7):
        s.append(r"\draw[grad] (%d,-.07) -- (%d,.07);" % (t, t))
        s.append(r"\node[gradTexte] at (%d,-.3) {$%d$};" % (t, t))
    s.append(crochet(3, 0, +1))
    s.append(r"\node[text=otGreenDark,anchor=south,font=\large] at (4.75,0.35) {$S=[3\,;+\infty[$};")
    s.append(r"\node[text=otInk,anchor=south,font=\large] at (0.75,0.35) {$x\ge 3$};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


TOLERE = {"carre_identite": "étiquettes a et b des flèches de cote, sur fond blanc (usage normal d'une cote)"}

FIGURES = {
"carre_identite": CARRE,

"parabole_x2_egal_a": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.8cm, height=5.2cm, xmin=-3.4, xmax=3.4, ymin=-1.9, ymax=7.4,
  xtick={-3,-2,-1,1,2,3}, ytick={1,2,3,5,6}]
  \addplot[courbe, domain=-2.68:2.68] {x^2};
  \draw[otGreenDark,line width=1pt] (axis cs:-3.4,4) -- (axis cs:3.4,4);
  \draw[otOrange,line width=1pt] (axis cs:-3.4,-1) -- (axis cs:3.4,-1);
  \guidev{-2}{4} \guidev{2}{4}
  \sol{-2}{2}
  \borneO{-2} \borneO{2}
  \pnt[otGreenDark]{-2}{4} \pnt[otGreenDark]{2}{4}
  \node[etiq,text=otNavy,anchor=west] at (axis cs:2.72,7.15) {$y=x^2$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:3.45,4) {$y=4$};
  \node[etiq,text=otOrange!80!black,anchor=west] at (axis cs:3.45,-1) {$y=-1$};
\end{axis}
\end{tikzpicture}""",

"droite_x_ge_3": droite_x_ge_3(),

"ex_abonnement": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.3cm, height=4.8cm, xmin=0, xmax=16.5, ymin=0, ymax=140,
  xtick={2,4,6,8,10,12,14,16}, ytick={20,40,60,80,100,120},
  xlabel={séances}, ylabel={coût en euros},
  every axis x label/.style={at={(current axis.right of origin)},anchor=west,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  every axis y label/.style={at={(current axis.above origin)},anchor=south,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}]
  \addplot[courbe, domain=0:16] {30+5*x};
  \addplot[courbe2, domain=0:16] {8*x};
  \guides{10}{80}
  \sol{10}{16}
  \borneO{10}
  \pnt[otGreenDark]{10}{80}
  \node[etiq,text=otNavy,anchor=west] at (axis cs:16.1,108) {$C_A$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:16.1,130) {$C_B$};
\end{axis}
\end{tikzpicture}""",

"ex_x2_enonce": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.8cm, height=5.6cm, xmin=-4.3, xmax=4.3, ymin=-1, ymax=12.4,
  xtick={-4,-3,-2,-1,1,2,3,4}, ytick={2,4,6,8,10}]
  \addplot[courbe, domain=-3.45:3.45] {x^2};
  \draw[otGreenDark,line width=1pt] (axis cs:-4.3,9) -- (axis cs:4.3,9);
  \node[etiq,text=otNavy,anchor=west] at (axis cs:3.5,11.9) {$y=x^2$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:4.35,9) {$y=9$};
\end{axis}
\end{tikzpicture}""",

"ex_x2_corrige": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.8cm, height=5.6cm, xmin=-4.3, xmax=4.3, ymin=-1, ymax=12.4,
  xtick={-4,-3,-2,-1,1,2,3,4}, ytick={2,4,6,8,10}]
  % a) partie de la parabole sous la droite (vert) ; b) sur ou au-dessus (orange)
  \addplot[otOrange!90!black, line width=2pt, domain=-3.45:-3] {x^2};
  \addplot[otOrange!90!black, line width=2pt, domain=3:3.45] {x^2};
  \addplot[otGreenDark, line width=2pt, domain=-3:3] {x^2};
  \draw[otGreenDark,line width=1pt] (axis cs:-4.3,9) -- (axis cs:4.3,9);
  \guidev{-3}{9} \guidev{3}{9}
  % ensembles de solutions, sous l'axe : a) x^2 < 9 ; b) x^2 >= 9
  \draw[guide] (axis cs:-3,-1.45) -- (axis cs:-3,-4.3);
  \draw[guide] (axis cs:3,-1.45) -- (axis cs:3,-4.3);
  \draw[otMuted,line width=.6pt] (axis cs:-4.3,-2.7) -- (axis cs:4.3,-2.7);
  \draw[otMuted,line width=.6pt] (axis cs:-4.3,-4.3) -- (axis cs:4.3,-4.3);
  \draw[otGreen,line width=3pt,line cap=butt,opacity=0.9] (axis cs:-3,-2.7) -- (axis cs:3,-2.7);
  \draw[otOrange,line width=3pt,line cap=butt,opacity=0.9] (axis cs:-4.3,-4.3) -- (axis cs:-3,-4.3);
  \draw[otOrange,line width=3pt,line cap=butt,opacity=0.9] (axis cs:3,-4.3) -- (axis cs:4.3,-4.3);
  \draw[otGreenDark,fill=white,line width=1pt] (axis cs:-3,-2.7) circle (2.5pt);
  \draw[otGreenDark,fill=white,line width=1pt] (axis cs:3,-2.7) circle (2.5pt);
  \fill[otOrange!90!black] (axis cs:-3,-4.3) circle (2.5pt);
  \fill[otOrange!90!black] (axis cs:3,-4.3) circle (2.5pt);
  \node[text=otGreenDark,anchor=west] at (axis cs:4.45,-2.7) {a) $x^2<9$};
  \node[text=otOrange!80!black,anchor=west] at (axis cs:4.45,-4.3) {b) $x^2\ge 9$};
  \pnt[otGreenDark]{-3}{9} \pnt[otGreenDark]{3}{9}
  \node[etiq,text=otInk,anchor=west] at (axis cs:3.5,11.9) {$y=x^2$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:4.35,9) {$y=9$};
\end{axis}
\end{tikzpicture}""",

# question 3 : x^2 <= 2, bornes -sqrt(2) et sqrt(2) incluses
"ex_x2_q3_corrige": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=5cm, xmin=-2.7, xmax=2.7, ymin=-0.6, ymax=5.6,
  xtick={-2,-1,1,2}, ytick={1,2,3,4,5}]
  \addplot[courbe, domain=-2.28:2.28] {x^2};
  \addplot[otGreenDark, line width=2pt, domain=-1.41421:1.41421] {x^2};
  \draw[otGreenDark,line width=1pt] (axis cs:-2.7,2) -- (axis cs:2.7,2);
  \draw[guide] (axis cs:-1.41421,2) -- (axis cs:-1.41421,-1.75);
  \draw[guide] (axis cs:1.41421,2) -- (axis cs:1.41421,-1.75);
  \draw[otMuted,line width=.6pt] (axis cs:-2.7,-1.75) -- (axis cs:2.7,-1.75);
  \draw[otGreen,line width=3pt,line cap=butt,opacity=0.9] (axis cs:-1.41421,-1.75) -- (axis cs:1.41421,-1.75);
  \fill[otGreenDark] (axis cs:-1.41421,-1.75) circle (2.5pt);
  \fill[otGreenDark] (axis cs:1.41421,-1.75) circle (2.5pt);
  \node[text=otGreenDark,anchor=north,yshift=-3pt] at (axis cs:-1.41421,-1.75) {$-\sqrt{2}$};
  \node[text=otGreenDark,anchor=north,yshift=-3pt] at (axis cs:1.41421,-1.75) {$\sqrt{2}$};
  \node[text=otGreenDark,anchor=west] at (axis cs:2.8,-1.75) {$x^2\le 2$};
  \pnt[otGreenDark]{-1.41421}{2} \pnt[otGreenDark]{1.41421}{2}
  \node[etiq,text=otNavy,anchor=west] at (axis cs:2.3,5.3) {$y=x^2$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:2.8,2) {$y=2$};
\end{axis}
\end{tikzpicture}""",
}


# =================================================================== finition 2026-11-02

def carre_somme(A, B, la, lb, aires, couleurs, bas):
    """Carré de côté A + B découpé : aires = (haut-gauche, haut-droite, bas-gauche, bas-droite)."""
    S = A + B
    s = [r"\begin{tikzpicture}"]
    rects = [((0, B), (A, S)), ((A, B), (S, S)), ((0, 0), (A, B)), ((A, 0), (S, B))]
    for ((x0, y0), (x1, y1)), c in zip(rects, couleurs):
        s.append(r"\fill[%s] (%s,%s) rectangle (%s,%s);" % (c, f(x0), f(y0), f(x1), f(y1)))
    s.append(r"\draw[geoTrait] (0,0) rectangle (%s,%s);" % (f(S), f(S)))
    s.append(r"\draw[geoTrait] (%s,0) -- (%s,%s);" % (f(A), f(A), f(S)))
    s.append(r"\draw[geoTrait] (0,%s) -- (%s,%s);" % (f(B), f(S), f(B)))
    centres = [(A / 2, B + A / 2), (A + B / 2, B + A / 2), (A / 2, B / 2), (A + B / 2, B / 2)]
    for (x, y), (txt, col) in zip(centres, aires):
        s.append(r"\node[zone,text=%s] at (%s,%s) {%s};" % (col, f(x), f(y), txt))
    s.append(r"\coordinate (H0) at (0,%s); \coordinate (H1) at (%s,%s); \coordinate (H2) at (%s,%s);"
             % (f(S), f(A), f(S), f(S), f(S)))
    s.append(r"\coordinate (V0) at (0,0); \coordinate (V1) at (0,%s); \coordinate (V2) at (0,%s);" % (f(B), f(S)))
    s.append(r"\cote[0.45]{H0}{H1}{%s}" % la)
    s.append(r"\cote[0.45]{H1}{H2}{%s}" % lb)
    s.append(r"\cote[0.45]{V1}{V2}{%s}" % la)
    s.append(r"\cote[0.45]{V0}{V1}{%s}" % lb)
    s.append(r"\node[text=otGreenDark,font=\large,anchor=north] at (%s,-0.3) {%s};" % (f(S / 2), bas))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


def factorisation_aires():
    """(x+1)(x+4) + (x+1)(2x-3) = (x+1)(3x+1) : deux rectangles de même hauteur x+1."""
    H, L1, L2 = 2.2, 3.8, 2.6
    s = [r"\begin{tikzpicture}"]
    s.append(r"\fill[otSky] (0,0) rectangle (%s,%s);" % (f(L1), f(H)))
    s.append(r"\fill[otOrange!16] (%s,0) rectangle (%s,%s);" % (f(L1), f(L1 + L2), f(H)))
    s.append(r"\draw[geoTrait] (0,0) rectangle (%s,%s);" % (f(L1 + L2), f(H)))
    s.append(r"\draw[geoTrait] (%s,0) -- (%s,%s);" % (f(L1), f(L1), f(H)))
    s.append(r"\node[zone,font=\normalsize] at (%s,%s) {$(x+1)(x+4)$};" % (f(L1 / 2), f(H / 2)))
    s.append(r"\node[zone,font=\normalsize] at (%s,%s) {$(x+1)(2x-3)$};" % (f(L1 + L2 / 2), f(H / 2)))
    s.append(r"\coordinate (a) at (0,%s); \coordinate (b) at (%s,%s); \coordinate (c) at (%s,%s);"
             % (f(H), f(L1), f(H), f(L1 + L2), f(H)))
    s.append(r"\coordinate (o) at (0,0);")
    s.append(r"\cote[0.45]{a}{b}{$x+4$}")
    s.append(r"\cote[0.45]{b}{c}{$2x-3$}")
    s.append(r"\cote[0.45]{o}{a}{$x+1$}")
    s.append(r"\draw[otGreenDark,line width=.8pt,decorate,decoration={brace,amplitude=6pt,mirror,raise=4pt}] "
             r"(0,0) -- (%s,0);" % f(L1 + L2))
    s.append(r"\node[anchor=north,text=otGreenDark] at (%s,-.42) {$(x+4)+(2x-3) = 3x+1$};" % f((L1 + L2) / 2))
    s.append(r"\node[anchor=north,text=otGreenDark,font=\large] at (%s,-1.05) {aire totale : $(x+1)(3x+1)$};"
             % f((L1 + L2) / 2))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


def distributivite():
    """k(a + b) = ka + kb."""
    H, L1, L2 = 1.9, 3.4, 2.2
    s = [r"\begin{tikzpicture}"]
    s.append(r"\fill[otSky] (0,0) rectangle (%s,%s);" % (f(L1), f(H)))
    s.append(r"\fill[otGreen!16] (%s,0) rectangle (%s,%s);" % (f(L1), f(L1 + L2), f(H)))
    s.append(r"\draw[geoTrait] (0,0) rectangle (%s,%s);" % (f(L1 + L2), f(H)))
    s.append(r"\draw[geoTrait] (%s,0) -- (%s,%s);" % (f(L1), f(L1), f(H)))
    s.append(r"\node[zone] at (%s,%s) {$ka$};" % (f(L1 / 2), f(H / 2)))
    s.append(r"\node[zone] at (%s,%s) {$kb$};" % (f(L1 + L2 / 2), f(H / 2)))
    s.append(r"\coordinate (a) at (0,%s); \coordinate (b) at (%s,%s); \coordinate (c) at (%s,%s);"
             % (f(H), f(L1), f(H), f(L1 + L2), f(H)))
    s.append(r"\coordinate (o) at (0,0);")
    s.append(r"\cote[0.45]{a}{b}{$a$}")
    s.append(r"\cote[0.45]{b}{c}{$b$}")
    s.append(r"\cote[0.45]{o}{a}{$k$}")
    s.append(r"\node[anchor=north,text=otGreenDark,font=\large,align=center] at (%s,-.3) "
             r"{$k(a+b) = ka + kb$\\[2pt]{\normalsize développer $\longrightarrow$ \quad $\longleftarrow$ factoriser}};"
             % f((L1 + L2) / 2))
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


def droite_q4():
    """]-2/5 ; +inf[ sur la droite graduée."""
    s = [r"\begin{tikzpicture}[x=1.25cm]"]
    s.append(r"\draw[bande,otGreen!85] (-0.4,0) -- (3.55,0);")
    s.append(r"\draw[axe] (-2.5,0) -- (3.75,0);")
    for t in range(-2, 4):
        s.append(r"\draw[grad] (%d,-.07) -- (%d,.07);" % (t, t))
        s.append(r"\node[gradTexte] at (%d,-.3) {$%d$};" % (t, t))
    s.append(crochet(-0.4, 0, -1))
    s.append(r"\draw[guide] (-0.4,.25) -- (-0.4,.62);")
    s.append(r"\node[anchor=south,text=otGreenDark] at (-0.4,.62) {$-\dfrac{2}{5}$};")
    s.append(r"\node[anchor=south,text=otGreenDark,font=\large] at (1.9,.3) {$S=\left]-\dfrac{2}{5}\,;+\infty\right[$};")
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


TOLERE.update({
    "ex_carre_x1": "étiquettes x et 1 des flèches de cote, sur fond blanc (usage normal d'une cote)",
    "ex_carre_x4": "étiquettes x et 4 des flèches de cote, sur fond blanc (usage normal d'une cote)",
    "ex_factorisation_aires": "longueurs x+4, 2x−3, x+1 sur leurs flèches de cote, fond blanc (usage normal d'une cote)",
    "distributivite": "longueurs k, a, b sur leurs flèches de cote, fond blanc (usage normal d'une cote)",
})

FIGURES.update({
    "ex_carre_x1": carre_somme(
        3.2, 1.1, r"\large $x$", r"\large $1$",
        [(r"$x^2$", "otInk"), (r"$x$", "otGreenDark"), (r"$x$", "otGreenDark"), (r"$1$", "otInk")],
        ["otSky", "otGreen!22", "otGreen!22", "otOrange!16"],
        r"$(x+1)^2-x^2-1 = x+x = 2x$"),
    "ex_carre_x4": carre_somme(
        2.9, 1.9, r"\large $x$", r"\large $4$",
        [(r"$x^2$", "otInk"), (r"$4x$", "otInk"), (r"$4x$", "otInk"), (r"$16$", "otInk")],
        ["otSky", "otOrange!16", "otOrange!16", "otGreen!16"],
        r"$(x+4)^2 = x^2+8x+16$"),
    "ex_factorisation_aires": factorisation_aires(),
    "distributivite": distributivite(),
    "ex_droite_q4": droite_q4(),

    # 1907 Q1 : (x+1)^2 et x^2+3 se coupent en x = 1
    "ex_comparaison": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=5.4cm, xmin=-3.3, xmax=3.3, ymin=-0.8, ymax=13.5,
  xtick={-3,-2,-1,1,2,3}, ytick={2,4,6,8,10,12}]
  \addplot[courbe, domain=-3.3:2.6] {(x+1)^2};
  \addplot[courbe2, domain=-3.2:3.2] {x^2+3};
  \guidev{1}{4}
  \sol{1}{3.3}
  \borneO{1}
  \pnt[otGreenDark]{1}{4}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:2.25,12.9) {$y=(x+1)^2$};
  \node[etiq,text=otGreenDark,anchor=west] at (axis cs:3.0,10.2) {$y=x^2+3$};
  \node[text=otGreenDark,anchor=north west,font=\otRegular\fontsize{9}{10}\selectfont] at (axis cs:1.5,-0.9) {$A>B$};
  \node[etiq,text=otGreenDark,anchor=south east] at (axis cs:0.85,4.15) {$(1\,;4)$};
\end{axis}
\end{tikzpicture}""",

    # 3738 Q3 : f(x) = (x-1)^2 - 4, minimum -4 en 1, racines -1 et 3
    "ex_forme_canonique": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=5.6cm, xmin=-2.6, xmax=4.6, ymin=-5.4, ymax=6.4,
  xtick={-2,-1,1,2,3,4}, xticklabels={}, ytick={-4,2,4}]
  \addplot[courbe, domain=-2.05:4.05] {(x-1)^2-4};
  \guidev{1}{-4}
  \draw[guide] (axis cs:0,-4) -- (axis cs:1,-4);
  \pnt[otGreenDark]{1}{-4}
  \pnt[otOrange!85!black]{-1}{0} \pnt[otOrange!85!black]{3}{0}
  \node[anchor=north east,xshift=-1.5pt,yshift=-2pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otOrange!80!black,fill=white,inner sep=1.3pt] at (axis cs:-1,0) {$-1$};
  \node[anchor=north west,xshift=1.5pt,yshift=-2pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otOrange!80!black,fill=white,inner sep=1.3pt] at (axis cs:3,0) {$3$};
  \node[anchor=south,yshift=2.5pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1.3pt] at (axis cs:1,0) {$1$};
  \node[anchor=north,yshift=-2.5pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1.3pt] at (axis cs:-2,0) {$-2$};
  \node[anchor=north,yshift=-2.5pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1.3pt] at (axis cs:4,0) {$4$};
  \node[text=otGreenDark,anchor=north west] at (axis cs:1.15,-4.15) {minimum $-4$ en $x=1$};
  \node[text=otNavy,anchor=west] at (axis cs:4.12,5.3) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}""",
})
