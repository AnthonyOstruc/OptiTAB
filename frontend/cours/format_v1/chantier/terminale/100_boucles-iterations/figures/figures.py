# -*- coding: utf-8 -*-
"""Figures de la notion « Algorithmes du programme de Terminale » (style des livres OptiTAB).

Compilation : python ../../../outils/figures_livre.py <dossier_notion> [nom …] [--planche]

Les valeurs sont celles du texte (contrôlées par ../verif_algorithmes.py).
Les figures de simulation EXÉCUTENT le programme imprimé dans le texte
(même graine) ou lisent son affichage : figure et texte ne peuvent pas diverger.
"""
import math
import re
from math import comb
from pathlib import Path

ICI = Path(__file__).resolve().parent
NOTION = ICI.parent

PREAMBULE_EXTRA = r"""
\pgfplotsset{otSuite/.style={
  axis lines=left,
  axis line style={otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}},
  tick style={otMuted,line width=0.5pt}, major tick length=3pt, tick align=outside,
  ticklabel style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  grid=major, grid style={otRule!75,line width=0.35pt},
  every axis x label/.style={at={(current axis.south east)},anchor=west,font=\normalsize,text=otMuted,xshift=3pt},
  every axis y label/.style={at={(current axis.north west)},anchor=south,font=\normalsize,text=otMuted,yshift=4pt},
  scale only axis, clip=false, axis on top=false,
  /pgf/number format/use comma, /pgf/number format/1000 sep={\,},
}}
\tikzset{
  legende/.style={font=\otRegular\fontsize{9}{10}\selectfont, text=otMuted, inner sep=1.5pt},
  legendeV/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otGreenDark, inner sep=1.5pt},
  legendeO/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otOrange!75!black, inner sep=1.5pt},
  legendeN/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otNavy, inner sep=1.5pt},
  tangente/.style={otOrange!85!black, line width=1pt},
  tangenteV/.style={otGreenDark, line width=1pt},
  intervalle/.style={otNavy, line width=2.2pt, line cap=butt},
  intervalleV/.style={otGreenDark, line width=2.2pt, line cap=butt},
  borne/.style={otNavy, line width=0.8pt},
  rectG/.style={draw=otNavy, line width=0.8pt, fill=otNavy!10},
  rectV/.style={draw=otGreenDark, line width=0.8pt, fill=otGreen!28},
  rectO/.style={draw=otOrange!85!black, line width=0.9pt, dash pattern=on 3pt off 2pt},
  escalier/.style={otGreenDark, line width=1pt, line join=round},
  pascal/.style={font=\normalsize, text=otInk, minimum size=4.6mm, inner sep=0pt},
  pascalV/.style={pascal, text=otGreenDark, font=\bfseries},
  caseP/.style={draw=otMuted, line width=0.6pt, rounded corners=1mm, minimum size=6.2mm, inner sep=0pt},
  flecheP/.style={otGreenDark, line width=0.8pt, -{Stealth[length=1.8mm]}},
}
"""

FIGURES = {}


def fr(v, d=2):
    """Nombre au format français pour TikZ ({,} décimale)."""
    s = f"{v:.{d}f}".rstrip("0").rstrip(".") if d else f"{v:.0f}"
    return s.replace(".", "{,}")


def pts(points, couleur="otNavy", r=2.1):
    return "\n  ".join(rf"\fill[{couleur}] (axis cs:{x},{y:.5f}) circle ({r}pt);" for x, y in points)


def programme(fichier, motif):
    """Code du bloc ```python du fichier qui contient `motif`."""
    t = (NOTION / fichier).read_text(encoding="utf-8")
    for m in re.finditer(r"```python[ \t]*\n(.*?)\n[ \t]*```", t, re.S):
        if motif in m.group(1):
            return m.group(1)
    raise ValueError(f"programme introuvable : {motif}")


def executer(*codes):
    ns = {"__name__": "__main__"}
    for c in codes:
        exec(compile(c, "<texte>", "exec"), ns)
    return ns


def console_apres(fichier, motif):
    t = (NOTION / fichier).read_text(encoding="utf-8")
    k = t.index(motif)
    m = re.search(r"```console[ \t]*\n(.*?)\n[ \t]*```", t[k:], re.S)
    return [l.strip() for l in m.group(1).splitlines()]


# ================================================================ suites
def nuage_suite(u0, a, b, nmax, ymax, ytick, largeur="7.4cm", hauteur="4.6cm", extra="", vert=None, ymin=0,
                xtick="{0,1,...,14}"):
    u = [u0]
    for _ in range(nmax):
        u.append(a * u[-1] + b)
    pp = [(n, v) for n, v in enumerate(u) if n != vert]
    v_pts = "" if vert is None else "\n  " + rf"\fill[otGreenDark] (axis cs:{vert},{u[vert]:.5f}) circle (2.7pt);"
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=""" + largeur + r""", height=""" + hauteur + r""", xmin=-0.5, xmax=""" + str(nmax + 0.8) + r""",
  ymin=""" + str(ymin) + r""", ymax=""" + str(ymax) + r""", xtick=""" + xtick + r""", ytick=""" + ytick + r""",
  xlabel={$n$}, ylabel={$u_n$}]""" + extra + r"""
  """ + pts(pp) + v_pts + r"""
\end{axis}
\end{tikzpicture}""", u


# cours (et fiche) : u0 = 1, u_{n+1} = 0,8 u_n + 2, seuil 9 atteint en n = 10, limite 10 jamais atteinte
_extra = r"""
  \draw[seuil] (axis cs:-0.5,9) -- (axis cs:14.6,9);
  \node[legendeO,anchor=north west] at (axis cs:0.4,8.75) {seuil $A = 9$};
  \draw[otNavy!70,line width=0.8pt,dash pattern=on 2.5pt off 2pt] (axis cs:-0.5,10) -- (axis cs:14.6,10);
  \node[legendeN,anchor=south west] at (axis cs:0.4,10.15) {$y = 10$ : jamais atteint};
  \draw[guide] (axis cs:10,0) -- (axis cs:10,9.0336);
  \node[legendeV,anchor=north west] at (axis cs:10.25,8.7) {$u_{10} \approx 9{,}03$};"""
FIGURES["suite_seuil"], _u = nuage_suite(1, 0.8, 2, 14, 11.6, "{0,2,...,10}", extra=_extra, vert=10)

# 832 (corrigé) : u0 = 5, u_{n+1} = 0,5 u_n + 1 → 2
_extra = r"""
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:-0.5,2) -- (axis cs:10.6,2);
  \node[legendeV,anchor=north east] at (axis cs:10.5,1.8) {limite $2$};
  \node[legende,anchor=west] at (axis cs:0.25,5) {$u_0 = 5$};"""
FIGURES["e832_limite"], _ = nuage_suite(5, 0.5, 1, 10, 5.8, "{0,1,...,5}", largeur="6.8cm", hauteur="4cm",
                                        extra=_extra, xtick="{0,1,...,10}")


# 831 : u_n = 20 × 0,7^n, seuil 1 ; énoncé : vue d'ensemble ; corrigé : zoom sur n = 4 … 12
FIGURES["e831_enonce"], _ = nuage_suite(20, 0.7, 0, 12, 21.5, "{0,5,...,20}", largeur="7.2cm", hauteur="4.6cm",
                                        xtick="{0,1,...,12}")


def e831_corrige():
    u = [20 * 0.7 ** n for n in range(13)]
    p = [(n, u[n]) for n in range(4, 13) if n != 9]
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=7.2cm, height=4.6cm, xmin=3.5, xmax=12.8, ymin=0, ymax=5.4,
  xtick={4,5,...,12}, ytick={0,1,...,5}, xlabel={$n$}, ylabel={$u_n$}]
  \draw[seuil] (axis cs:3.5,1) -- (axis cs:12.6,1);
  \node[legendeO,anchor=south east] at (axis cs:12.6,1.12) {seuil $1$};
  """ + pts(p) + r"""
  \fill[otGreenDark] (axis cs:9,""" + f"{u[9]:.5f}" + r""") circle (2.7pt);
  \node[legende,anchor=south west] at (axis cs:8.12,1.22) {$u_8 \approx 1{,}15$};
  \node[legendeV,anchor=north] at (axis cs:9,0.62) {$u_9 \approx 0{,}81$};
\end{axis}
\end{tikzpicture}"""


FIGURES["e831_corrige"] = e831_corrige()


# 835 : u0 = 2, u_{n+1} = 0,7 u_n + 2 → 20/3
def e835(corrige):
    extra = r"""
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:-0.5,6.6667) -- (axis cs:15.6,6.6667);
  \node[legendeV,anchor=west] at (axis cs:15.7,6.6667) {$y = \frac{20}{3}$};
  \draw[seuil] (axis cs:-0.5,7) -- (axis cs:15.6,7);
  \node[legendeO,anchor=south east] at (axis cs:15.6,7.08) {seuil $7$ : jamais dépassé};
  \draw[seuil] (axis cs:-0.5,6) -- (axis cs:15.6,6);
  \node[legendeO,anchor=north east] at (axis cs:15.6,5.9) {seuil $6$ : dépassé dès $n = 6$};""" if corrige else ""
    fig, _u = nuage_suite(2, 0.7, 2, 15, 7.6, "{2,3,...,7}", largeur="6.4cm", hauteur="5.4cm", ymin=1.5,
                          extra=extra, vert=6 if corrige else None, xtick="{0,1,...,15}")
    return fig


FIGURES["e835_enonce"] = e835(False)
FIGURES["e835_corrige"] = e835(True)


# ================================================================ dichotomie
def dicho(fonction, expr_tikz, a0, b0, tours, alpha, ymin, ymax, ytick, y0_barres, pas_barres, label_f,
          pos_label, montrer_intervalles=True, largeur="7cm", hauteur="6cm", xticks=None):
    a, b = a0, b0
    barres = []
    for k in range(tours + 1):
        barres.append((a, b))
        m = (a + b) / 2
        if fonction(a) * fonction(m) <= 0:
            b = m
        else:
            a = m
    lignes = []
    if montrer_intervalles:
        for k, (a, b) in enumerate(barres):
            y = y0_barres - k * pas_barres
            style = "intervalleV" if k == len(barres) - 1 else "intervalle"
            lignes.append(rf"\draw[{style}] (axis cs:{a},{y}) -- (axis cs:{b},{y});")
            lignes.append(rf"\draw[borne] (axis cs:{a},{y - 0.07}) -- (axis cs:{a},{y + 0.07}) (axis cs:{b},{y - 0.07}) -- (axis cs:{b},{y + 0.07});")
            lignes.append(rf"\node[legende,anchor=west] at (axis cs:{b0 + 0.05},{y}) {{{k}}};")
        ybas = y0_barres - tours * pas_barres - 0.12
        lignes.append(rf"\draw[guide] (axis cs:{alpha},0) -- (axis cs:{alpha},{ybas});")
        lignes.append(rf"\fill[otGreenDark] (axis cs:{alpha},0) circle (2.4pt);")
        lignes.append(rf"\node[legendeV,anchor=south east] at (axis cs:{alpha - 0.01},0.06) {{$\alpha$}};")
        lignes.append(rf"\node[legende,anchor=south west] at (axis cs:{b0 + 0.02},{y0_barres + 0.13}) {{tour}};")
    xt = xticks or (r"xtick={0,0.25,0.5,0.75,1}, xticklabels={$0$,$0{,}25$,$0{,}5$,$0{,}75$,$1$}")
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=""" + largeur + r""", height=""" + hauteur + r""", xmin=-0.1, xmax=1.2, ymin=""" + str(ymin) + r""", ymax=""" + str(ymax) + r""",
  """ + xt + r""", ytick=""" + ytick + r""", xlabel={$x$}, ylabel={$y$}]
  \draw[otMuted,line width=0.7pt] (axis cs:-0.1,0) -- (axis cs:1.2,0);
  \addplot[courbe, domain=0:1.08, samples=160] {""" + expr_tikz + r"""};
  \node[text=otNavy,anchor=""" + pos_label[0] + r"""] at (axis cs:""" + pos_label[1] + r""") {""" + label_f + r"""};
  """ + "\n  ".join(lignes) + r"""
\end{axis}
\end{tikzpicture}"""


FIGURES["dichotomie"] = dicho(lambda x: x ** 3 + x - 1, "x^3+x-1", 0, 1, 4, 0.6823278, -2.85, 1.45,
                              "{-1,0,1}", -1.35, 0.33, r"$y = x^3 + x - 1$", ("east", "0.98,1.25"))
FIGURES["e833_enonce"] = dicho(lambda x: math.exp(x) + x - 3, "exp(x)+x-3", 0, 1, 3, 0.7921, -2.25, 1.05,
                               "{-2,-1,0,1}", -2.6, 0.33, r"$y = f(x)$", ("east", "0.98,0.92"),
                               montrer_intervalles=False, hauteur="5cm")
FIGURES["e833_corrige"] = dicho(lambda x: math.exp(x) + x - 3, "exp(x)+x-3", 0, 1, 3, 0.7921, -3.65, 1.05,
                                "{-2,-1,0,1}", -2.45, 0.36, r"$y = f(x)$", ("east", "0.98,0.92"), hauteur="6.4cm")


# ================================================================ Newton
def newton_cours():
    f = lambda x: x ** 3 + x - 1  # noqa: E731
    fp = lambda x: 3 * x ** 2 + 1  # noqa: E731
    x0 = 1.0
    x1 = x0 - f(x0) / fp(x0)
    x2 = x1 - f(x1) / fp(x1)
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=7cm, height=5.6cm, xmin=0.55, xmax=1.12, ymin=-0.45, ymax=1.3,
  xtick={0.6,0.7,0.8,0.9,1}, xticklabels={$0{,}6$,$0{,}7$,$0{,}8$,$0{,}9$,$1$}, ytick={0,0.5,1},
  yticklabels={$0$,$0{,}5$,$1$}, xlabel={$x$}, ylabel={$y$}]
  \draw[otMuted,line width=0.7pt] (axis cs:0.55,0) -- (axis cs:1.12,0);
  \addplot[courbe, domain=0.55:1.065, samples=160] {x^3+x-1};
  \addplot[tangente, domain=0.7:1.07] {4*(x-1)+1};
  \addplot[tangenteV, domain=0.62:0.86] {""" + f"{fp(x1):.6f}*(x-{x1})+{f(x1):.6f}" + r"""};
  \draw[guide] (axis cs:1,0) -- (axis cs:1,1);
  \draw[guide] (axis cs:""" + f"{x1}" + r""",0) -- (axis cs:""" + f"{x1},{f(x1):.6f}" + r""");
  \fill[otNavy] (axis cs:1,1) circle (2.2pt);
  \fill[otNavy] (axis cs:""" + f"{x1},{f(x1):.6f}" + r""") circle (2.2pt);
  \fill[otOrange!85!black] (axis cs:""" + f"{x1}" + r""",0) circle (2.2pt);
  \fill[otGreenDark] (axis cs:""" + f"{x2:.6f}" + r""",0) circle (2.2pt);
  \node[legendeO,anchor=north west] at (axis cs:0.755,-0.03) {$x_1 = 0{,}75$};
  \node[legendeV,anchor=south east] at (axis cs:0.682,0.03) {$x_2$};
  \node[legende,anchor=north] at (axis cs:1,-0.03) {$x_0$};
  \node[text=otNavy,anchor=west] at (axis cs:0.565,1.13) {$y = x^3 + x - 1$};
  \node[legendeO,anchor=west] at (axis cs:0.565,0.9) {tangente en $x_0$};
  \node[legendeV,anchor=west] at (axis cs:0.565,0.72) {tangente en $x_1$};
\end{axis}
\end{tikzpicture}"""


FIGURES["newton"] = newton_cours()


def newton_racine2(corrige):
    plus = r"""
  \addplot[tangenteV, domain=1.3:1.75] {3*(x-1.5)+0.25};
  \draw[guide] (axis cs:1.5,0) -- (axis cs:1.5,0.25);
  \fill[otNavy] (axis cs:1.5,0.25) circle (2.2pt);
  \fill[otOrange!85!black] (axis cs:1.5,0) circle (2.2pt);
  \fill[otGreenDark] (axis cs:1.416667,0) circle (2.2pt);
  \node[legendeO,anchor=north west] at (axis cs:1.505,-0.04) {$x_1 = 1{,}5$};
  \node[legendeV,anchor=south east] at (axis cs:1.41,0.04) {$x_2 = \frac{17}{12}$};
  \node[legendeV,anchor=west] at (axis cs:1.215,1.55) {tangente en $x_1$};""" if corrige else ""
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=6.6cm, height=5.8cm, xmin=1.2, xmax=2.25, ymin=-0.75, ymax=2.65,
  xtick={1.25,1.5,1.75,2}, xticklabels={$1{,}25$,$1{,}5$,$1{,}75$,$2$}, ytick={0,1,2},
  xlabel={$x$}, ylabel={$y$}]
  \draw[otMuted,line width=0.7pt] (axis cs:1.2,0) -- (axis cs:2.25,0);
  \addplot[courbe, domain=1.2:2.15, samples=160] {x^2-2};
  \addplot[tangente, domain=1.4:2.12] {4*x-6};
  \draw[guide] (axis cs:2,0) -- (axis cs:2,2);
  \fill[otNavy] (axis cs:2,2) circle (2.2pt);
  \node[text=otNavy,anchor=south east] at (axis cs:1.97,2.04) {$A$};
  \node[text=otNavy,anchor=west] at (axis cs:1.215,2.35) {$\mathcal{C} : y = x^2 - 2$};
  \node[legendeO,anchor=west] at (axis cs:1.215,1.95) {tangente en $A$};""" + plus + r"""
\end{axis}
\end{tikzpicture}"""


FIGURES["newton_racine2_enonce"] = newton_racine2(False)
FIGURES["newton_racine2_corrige"] = newton_racine2(True)


# ================================================================ rectangles
def rect_inverse():
    n, h = 4, 0.25
    lignes = []
    for k in range(n):
        a = 1 + k * h
        lignes.append(rf"\draw[rectG] (axis cs:{a},0) rectangle (axis cs:{a + h},{1 / a:.5f});")
    for k in range(n):
        a = 1 + k * h
        lignes.append(rf"\draw[rectV] (axis cs:{a},0) rectangle (axis cs:{a + h},{1 / (a + h):.5f});")
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=6.8cm, height=4.8cm, xmin=0.88, xmax=2.2, ymin=0, ymax=1.32,
  xtick={1,1.25,1.5,1.75,2}, xticklabels={$1$,$1{,}25$,$1{,}5$,$1{,}75$,$2$}, ytick={0.5,1},
  yticklabels={$0{,}5$,$1$}, xlabel={$x$}, ylabel={$y$}]
  """ + "\n  ".join(lignes) + r"""
  \addplot[courbe, domain=0.95:2.12, samples=120] {1/x};
  \node[text=otNavy,anchor=south west] at (axis cs:1.62,0.67) {$y = \frac{1}{x}$};
  \node[legendeN,anchor=south west] at (axis cs:1.3,1.07) {à gauche : $S$};
  \node[legendeV,anchor=west] at (axis cs:2.03,0.3) {à droite : $s$};
\end{axis}
\end{tikzpicture}"""


FIGURES["rectangles"] = rect_inverse()


def rect_carre(corrige):
    n, h = 4, 0.25
    lignes = []
    if corrige:
        for k in range(n):
            a = k * h
            lignes.append(rf"\draw[rectO] (axis cs:{a},0) rectangle (axis cs:{a + h},{(a + h) ** 2:.5f});")
    for k in range(n):
        a = k * h
        style = "rectV" if corrige else "rectG"
        lignes.append(rf"\draw[{style}] (axis cs:{a},0) rectangle (axis cs:{a + h},{a * a:.5f});")
    plus = r"""
  \node[legendeV,anchor=north west] at (axis cs:1.06,0.38) {$s_4 = 0{,}21875$};
  \node[legendeO,anchor=south west] at (axis cs:1.06,0.42) {$S_4 = 0{,}46875$};""" if corrige else ""
    return r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=5.6cm, xmin=-0.12, xmax=1.32, ymin=-0.1, ymax=1.22,
  xtick={0.25,0.5,0.75,1}, xticklabels={$0{,}25$,$0{,}5$,$0{,}75$,$1$}, ytick={0.5,1}, yticklabels={$0{,}5$,$1$}]
  """ + "\n  ".join(lignes) + r"""
  \addplot[courbe, domain=0:1.08, samples=120] {x^2};
  \node[text=otNavy,anchor=east] at (axis cs:0.93,1.05) {$y = x^2$};""" + plus + r"""
\end{axis}
\end{tikzpicture}"""


FIGURES["rect_carre_enonce"] = rect_carre(False)
FIGURES["rect_carre_corrige"] = rect_carre(True)


# ================================================================ exponentielle : le café
def cafe(corrige):
    plus = r"""
  \draw[seuil] (axis cs:0,30) -- (axis cs:41,30);
  \node[legendeO,anchor=south west] at (axis cs:26,31) {seuil $30$ °C};
  \draw[asymptote] (axis cs:0,20) -- (axis cs:41,20);
  \node[text=otRed!85!black,font=\otRegular\fontsize{9}{10}\selectfont,anchor=north east] at (axis cs:40.5,18.5) {asymptote $y = 20$};
  \draw[guide] (axis cs:18,0) -- (axis cs:18,29.918);
  \fill[otGreenDark] (axis cs:18,29.918) circle (2.6pt);
  \node[legendeV,anchor=south west] at (axis cs:18.6,36) {$T(18) \approx 29{,}9$};
  \draw[otGreenDark,line width=0.5pt] (axis cs:18.9,35.8) -- (axis cs:18.3,30.6);""" if corrige else ""
    return r"""
\begin{tikzpicture}
\begin{axis}[otSuite, width=7.2cm, height=4.8cm, xmin=0, xmax=41, ymin=0, ymax=88,
  xtick={0,5,...,40}, ytick={0,20,40,60,80}, xlabel={$t$}, ylabel={$T(t)$}]
  \addplot[courbe, domain=0:40, samples=160] {20+60*exp(-0.1*x)};
  \node[text=otNavy,anchor=south west] at (axis cs:4.5,65) {$T(t) = 20 + 60\,e^{-0{,}1t}$};""" + plus + r"""
\end{axis}
\end{tikzpicture}"""


FIGURES["cafe_enonce"] = cafe(False)
FIGURES["cafe_corrige"] = cafe(True)


# ================================================================ probabilités
def barres(freqs, probas, couleur_p, legende_p, xmin, xmax, ymax, ytick, largeur="7.6cm", hauteur="4.4cm",
           bar_width="11pt", xlabel="$k$", ylabel="fréquence", legende_f="fréquence observée", xtick=None,
           yfmt="fixed,/pgf/number format/precision=2", leg_x=None):
    bars = " ".join(f"({k},{v:.4f})" for k, v in freqs)
    marques = ""
    if probas:
        marques = "\n  ".join(
            rf"\draw[{couleur_p},line width=1.8pt] (axis cs:{k - 0.36},{p:.5f}) -- (axis cs:{k + 0.36},{p:.5f});"
            for k, p in probas)
    lx = leg_x if leg_x is not None else 4.55
    leg = r"""
  \fill[otNavy!55,draw=otNavy] (""" + f"{lx}" + r""",4.22) rectangle ++(0.26,0.2);
  \node[legende,anchor=west] at (""" + f"{lx + 0.31}" + r""",4.32) {""" + legende_f + r"""};"""
    if probas:
        leg += r"""
  \draw[""" + couleur_p + r""",line width=1.8pt] (""" + f"{lx - 0.03}" + r""",3.9) -- ++(0.32,0);
  \node[legende,anchor=west] at (""" + f"{lx + 0.31}" + r""",3.9) {""" + legende_p + r"""};"""
    xt = xtick or ",".join(str(k) for k, _ in freqs)
    return r"""
\begin{tikzpicture}
\begin{axis}[otBarres, width=""" + largeur + r""", height=""" + hauteur + r""", bar width=""" + bar_width + r""", ymax=""" + str(ymax) + r""", enlarge x limits=0.05,
  xmin=""" + str(xmin) + r""", xmax=""" + str(xmax) + r""", xtick={""" + xt + r"""}, ytick={""" + ytick + r"""},
  yticklabel style={/pgf/number format/""" + yfmt + r"""},
  xlabel={""" + xlabel + r"""}, ylabel={""" + ylabel + r"""}, clip=false,
  every axis y label/.style={at={(current axis.north west)},anchor=south,yshift=4pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  every axis x label/.style={at={(current axis.south east)},anchor=north east,yshift=-14pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}]
  \addplot[fill=otNavy!55,draw=otNavy] coordinates {""" + bars + r"""};
  """ + marques + r"""
\end{axis}""" + leg + r"""
\end{tikzpicture}"""


# cours : effectifs lus dans l'affichage du programme du cours, probabilités de B(10 ; 0,3)
def histo_binom_cours():
    lignes = console_apres("cours_104.txt", "E[x] = E[x] + 1")
    eff = {int(l.split()[0]): int(l.split()[1]) for l in lignes}
    assert sum(eff.values()) == 1000
    freqs = [(k, eff[k] / 1000) for k in range(11)]
    probas = [(k, comb(10, k) * 0.3 ** k * 0.7 ** (10 - k)) for k in range(11)]
    return barres(freqs, probas, "otOrange!85!black", r"probabilité $P(X = k)$", -0.5, 10.5, 0.3,
                  "0.1,0.2,0.3")


FIGURES["histo_binom"] = histo_binom_cours()


# 834 : le programme de l'énoncé est exécuté (seed(2026))
def e834(corrige):
    ns = executer(programme("exercices.txt", "def serie():"))
    E = ns["E"]
    freqs = [(k, E[k] / 1000) for k in range(11)]
    probas = [(k, comb(10, k) * 0.7 ** k * 0.3 ** (10 - k)) for k in range(11)] if corrige else None
    return barres(freqs, probas, "otGreenDark", r"probabilité $P(X = k)$", -0.5, 10.5, 0.33, "0.1,0.2,0.3",
                  leg_x=0.25)


FIGURES["e834_enonce"] = e834(False)
FIGURES["e834_corrige"] = e834(True)


# nouveau-4 : loi B(210 ; 0,92), queue X > 200
def surbook(corrige):
    p = {k: comb(210, k) * 0.92 ** k * 0.08 ** (210 - k) for k in range(178, 211)}
    gauche = " ".join(f"({k},{p[k]:.5f})" for k in range(178, 211) if not (corrige and k > 200))
    queue = " ".join(f"({k},{p[k]:.5f})" for k in range(201, 211))
    plus = r"""
  \addplot[fill=otGreen!75,draw=otGreenDark] coordinates {""" + queue + r"""};
  \node[legendeV,anchor=south west] at (axis cs:201.3,0.046) {$P(X > 200) \approx 0{,}024$};
  \draw[otGreenDark,line width=0.5pt] (axis cs:202.6,0.045) -- (axis cs:201.6,0.016);""" if corrige else ""
    return r"""
\begin{tikzpicture}
\begin{axis}[otBarres, width=7.6cm, height=4.2cm, bar width=4.2pt, ymax=0.105, xmin=177, xmax=211,
  enlarge x limits=0.02, xtick={180,185,...,210}, ytick={0.02,0.04,0.06,0.08,0.1},
  yticklabel style={/pgf/number format/fixed,/pgf/number format/precision=2},
  xlabel={$k$}, ylabel={$P(X = k)$}, clip=false,
  every axis y label/.style={at={(current axis.north west)},anchor=south,yshift=4pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  every axis x label/.style={at={(current axis.south east)},anchor=north east,yshift=-14pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}]
  \addplot[fill=otNavy!55,draw=otNavy] coordinates {""" + gauche + r"""};""" + plus + r"""
  \draw[seuil] (axis cs:200.5,0) -- (axis cs:200.5,0.1);
  \node[legendeO,anchor=south west] at (axis cs:200.7,0.088) {$200$ places};
\end{axis}
\end{tikzpicture}"""


FIGURES["surbook_enonce"] = surbook(False)
FIGURES["surbook_corrige"] = surbook(True)


# nouveau-5 : histogramme des 1 000 moyennes (programme de l'énoncé exécuté)
def moyennes(corrige):
    ns = executer(programme("exercices.txt", "M.append(moyenne(100))"))
    M = ns["M"]
    # classes [2,85 ; 2,95[, [2,95 ; 3,05[, …, [4,05 ; 4,15[ (calcul en centièmes entiers)
    eff = [sum(1 for x in M if 285 + 10 * k <= round(x * 100) < 295 + 10 * k) for k in range(13)]
    assert sum(eff) == len(M) == 1000, "une moyenne hors des classes"
    centres = [round(2.9 + 0.1 * k, 1) for k in range(13)]
    bars = " ".join(f"({c},{e})" for c, e in zip(centres, eff))
    d = 2 * math.sqrt(35 / 12) / 10
    plus = r"""
  \draw[otGreenDark,line width=2.4pt,line cap=butt] (axis cs:""" + f"{3.5 - d:.4f}" + r""",-62) -- (axis cs:""" + f"{3.5 + d:.4f}" + r""",-62);
  \draw[otGreenDark,line width=0.8pt] (axis cs:""" + f"{3.5 - d:.4f}" + r""",-70) -- (axis cs:""" + f"{3.5 - d:.4f}" + r""",-54) (axis cs:""" + f"{3.5 + d:.4f}" + r""",-70) -- (axis cs:""" + f"{3.5 + d:.4f}" + r""",-54);
  \node[legendeV,anchor=north] at (axis cs:3.5,-74) {$95{,}4\,\%$ des moyennes dans $[3{,}158\,;3{,}842]$};
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 3pt off 2pt] (axis cs:3.5,0) -- (axis cs:3.5,262);
  \node[legendeV,anchor=south] at (axis cs:3.5,262) {$\mu = 3{,}5$};""" if corrige else ""
    return r"""
\begin{tikzpicture}
\begin{axis}[otBarres, width=6.3cm, height=4.4cm, bar width=11.5pt, ymin=0, ymax=280, xmin=2.85, xmax=4.15,
  enlarge x limits=0.02, xtick={3,3.5,4}, xticklabels={$3$,$3{,}5$,$4$}, ytick={50,100,150,200,250},
  xlabel={moyenne}, ylabel={effectif}, clip=false,
  every axis y label/.style={at={(current axis.north west)},anchor=south,yshift=4pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  every axis x label/.style={at={(current axis.south east)},anchor=west,xshift=3pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}]
  \addplot[fill=otNavy!55,draw=otNavy] coordinates {""" + bars + r"""};""" + plus + r"""
\end{axis}
\end{tikzpicture}"""


FIGURES["moyennes_enonce"] = moyennes(False)
FIGURES["moyennes_corrige"] = moyennes(True)


# ================================================================ triangle de Pascal
def pascal(nlig, vide=None, verte=None, fleches=None, dx=0.9, dy=1.05, verts=()):
    """Lignes 0 à nlig ; ligne `vide` en cases vides ; ligne `verte` en vert ;
    fleches = [(ligne, k)] : flèches de (ligne-1, k-1) et (ligne-1, k) vers (ligne, k)."""
    lignes = []
    for n in range(nlig + 1):
        y = -n * dy
        lignes.append(rf"\node[legende,anchor=east] at ({-nlig * dx / 2 - 0.55:.3f},{y:.3f}) {{$n = {n}$}};")
        for k in range(n + 1):
            x = (k - n / 2) * dx
            nom = f"p{n}x{k}"
            if n == vide:
                lignes.append(rf"\node[caseP] ({nom}) at ({x:.3f},{y:.3f}) {{}};")
            elif n == verte or (n, k) in verts:
                lignes.append(rf"\node[pascalV] ({nom}) at ({x:.3f},{y:.3f}) {{{comb(n, k)}}};")
            else:
                lignes.append(rf"\node[pascal] ({nom}) at ({x:.3f},{y:.3f}) {{{comb(n, k)}}};")
    for (n, k) in (fleches or []):
        lignes.append(rf"\draw[flecheP,shorten <=1pt,shorten >=1pt] (p{n - 1}x{k - 1}.south east) -- (p{n}x{k}.north);")
        lignes.append(rf"\draw[flecheP,shorten <=1pt,shorten >=1pt] (p{n - 1}x{k}.south west) -- (p{n}x{k}.north);")
    return "\\begin{tikzpicture}\n" + "\n".join(lignes) + "\n\\end{tikzpicture}"


FIGURES["pascal_cours"] = pascal(5, fleches=[(5, 2)], verts=((4, 1), (4, 2), (5, 2)))
FIGURES["pascal_enonce"] = pascal(6, vide=6)
FIGURES["pascal_corrige"] = pascal(6, verte=6, fleches=[(6, 3)], verts=((5, 2), (5, 3)))


# ================================================================ escalier u_{n+1} = f(u_n)
def escalier(corrige):
    f = lambda x: 4 * x / (x + 1)  # noqa: E731
    u = [0.5]
    for _ in range(4):
        u.append(f(u[-1]))
    plus = ""
    if corrige:
        chemin = [f"(axis cs:{u[0]},0)"]
        for k in range(4):
            chemin.append(f"(axis cs:{u[k]:.5f},{u[k + 1]:.5f})")
            chemin.append(f"(axis cs:{u[k + 1]:.5f},{u[k + 1]:.5f})")
        plus = r"""
  \draw[escalier] """ + " -- ".join(chemin) + r""";
  """ + "\n  ".join(rf"\draw[guide] (axis cs:{u[k]:.5f},0) -- (axis cs:{u[k]:.5f},{u[k]:.5f});" for k in range(1, 3)) + r"""
  """ + "\n  ".join(rf"\draw[otGreenDark,line width=0.5pt] (axis cs:{u[k]:.5f},-0.08) -- (axis cs:{u[k]:.5f},-0.5);" for k in range(3)) + r"""
  """ + "\n  ".join(rf"\fill[otGreenDark] (axis cs:{u[k]:.5f},0) circle (2.2pt);" for k in range(3)) + r"""
  \node[legendeV,anchor=north] at (axis cs:0.5,-0.55) {$u_0$};
  \node[legendeV,anchor=north] at (axis cs:""" + f"{u[1]:.4f}" + r""",-0.55) {$u_1$};
  \node[legendeV,anchor=north] at (axis cs:""" + f"{u[2]:.4f}" + r""",-0.55) {$u_2$};
  \fill[otNavy] (axis cs:3,3) circle (2.2pt);
  \node[legendeN,anchor=north west] at (axis cs:3.06,2.94) {$(3\,;3)$};"""
    return r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=6.6cm, xmin=-0.3, xmax=4.4, ymin=-0.3, ymax=4.4,
  xtick={1,2,3,4}, ytick={1,2,3,4}]
  \addplot[courbe, domain=0:4.2, samples=160] {4*x/(x+1)};
  \addplot[otMuted, line width=0.9pt, domain=-0.1:4.2] {x};
  \node[text=otNavy,anchor=south east] at (axis cs:1.2,2.55) {$y = f(x)$};
  \node[text=otMuted,anchor=north west] at (axis cs:3.75,3.55) {$y = x$};""" + plus + r"""
\end{axis}
\end{tikzpicture}"""


FIGURES["escalier_enonce"] = escalier(False)
FIGURES["escalier_corrige"] = escalier(True)
