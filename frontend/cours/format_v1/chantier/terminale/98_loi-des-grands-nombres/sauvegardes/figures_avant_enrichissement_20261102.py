# -*- coding: utf-8 -*-
"""Figures de la notion « Loi des grands nombres » (Terminale), style des livres OptiTAB.

Compilation : python ../../../../outils/figures_livre.py <dossier_notion> [--planche]

- bt_binomiale        : loi B(20 ; 0,5), écarts |X - 10| >= 4 en orange (probabilité 0,115 <= 5/16) ;
- lgn_convergence     : fréquence de pile pour 3 simulations de 1 000 lancers et bande
                        0,5 ± 1/sqrt(0,2 n) garantie à 95 % par l'inégalité de concentration ;
- roulette_intervalle : exercice 824, intervalle [0,024 ; 0,031] non centré sur p = 1/37.
Valeurs vérifiées par verif_lgn.py.
"""
import random
from math import comb, sqrt

# ---------------------------------------------------------------- loi B(20 ; 0,5)
_P = [comb(20, k) / 2 ** 20 for k in range(21)]
_ORANGE = " ".join(f"({k},{_P[k]:.5f})" for k in range(21) if abs(k - 10) >= 4)
_BLEU = " ".join(f"({k},{_P[k]:.5f})" for k in range(21) if abs(k - 10) < 4)

# ---------------------------------------------------------------- simulations (graine fixée)
def _trajectoire(graine, n_max=1000, pas=10):
    gen = random.Random(graine)
    nb, pts = 0, []
    for n in range(1, n_max + 1):
        nb += gen.random() < 0.5
        if n >= 20 and n % pas == 0:
            pts.append((n, nb / n))
    return pts


GRAINES = (16, 22, 5)
_TRAJ = [_trajectoire(g) for g in GRAINES]
_COUL = ("otNavy", "otGreenDark", "otOrange")
_COURBES = "\n  ".join(
    rf"\addplot[{c},line width=0.9pt] coordinates {{" + " ".join(f"({n},{f:.4f})" for n, f in t) + "};"
    for c, t in zip(_COUL, _TRAJ)
)

# ---------------------------------------------------------------- roulette (exercice 824)
_p = 1 / 37
_d = _p - 0.024
_X = lambda v: (v - 0.0205) * 650  # noqa: E731  (cm)
_R = {k: f"{_X(v):.3f}" for k, v in
      {"g": 0.0205, "a": 0.024, "pp": _p, "pd": _p + _d, "b": 0.031, "fin": 0.0328}.items()}

# ---------------------------------------------------------------- exercice 821 : une simulation (graine 2)
def _simulation(graine=2, n_max=1000):
    gen = random.Random(graine)
    nb, pts = 0, []
    for n in range(1, n_max + 1):
        nb += gen.random() < 0.5
        if (5 <= n <= 100) or n % 10 == 0:
            pts.append((n, nb / n))
    return pts


SIM821 = _simulation()
_SIM = " ".join(f"({n},{f:.4f})" for n, f in SIM821)


def _fig821(corrige):
    bande = (r"""
  \fill[otGreen!18] (axis cs:0,0.4) rectangle (axis cs:1000,0.6);
  \draw[otGreen,line width=0.6pt] (axis cs:0,0.4) -- (axis cs:1000,0.4);
  \draw[otGreen,line width=0.6pt] (axis cs:0,0.6) -- (axis cs:1000,0.6);
  \node[anchor=south,text=otGreenDark] at (axis cs:640,0.62) {$|f_n-0{,}5|<0{,}1$};""" if corrige else "")
    return r"""
\begin{tikzpicture}
\begin{axis}[otWeb, axis lines=left, width=7.3cm, height=4.6cm, xmin=0, xmax=1040, ymin=0.2, ymax=0.8,
  xtick={200,400,600,800,1000}, xticklabels={$200$,$400$,$600$,$800$,$1\,000$},
  ytick={0.3,0.4,0.5,0.6,0.7}, yticklabels={$0{,}3$,$0{,}4$,$0{,}5$,$0{,}6$,$0{,}7$},
  xlabel={$n$}, ylabel={$f_n$},
  every axis x label/.style={at={(rel axis cs:1,0)},anchor=west,font=\normalsize,text=otMuted},
  every axis y label/.style={at={(rel axis cs:0,1)},anchor=south,font=\normalsize,text=otMuted},
  xticklabel style={anchor=north,yshift=-2.5pt}]""" + bande + r"""
  \draw[otInk!75,line width=0.8pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,0.5) -- (axis cs:1000,0.5);
  \addplot[otNavy,line width=0.9pt] coordinates {""" + _SIM + r"""};
  \node[anchor=west,text=otInk] at (axis cs:1022,0.5) {$0{,}5$};
\end{axis}
\end{tikzpicture}"""


# ---------------------------------------------------------------- exercice 822 : boulons (question 3)
def _fig822(corrige):
    # échelle : 4,5 -> 1,2 cm ; 5 -> 3 cm ; 5,5 -> 4,8 cm (0,1 cm de longueur = 0,36 cm)
    s = [r"\begin{tikzpicture}[font=\normalsize]",
         r"  \fill[otOrange!22] (0,-0.25) rectangle (1.2,0.25);",
         r"  \fill[otOrange!22] (4.8,-0.25) rectangle (6,0.25);",
         r"  \draw[otMuted,line width=.6pt,-{Stealth[length=2.3mm]}] (0,0) -- (6.3,0);",
         r"  \foreach \x in {1.2,3,4.8} \draw[otMuted,line width=.6pt] (\x,-0.09) -- (\x,0.09);",
         r"  \node[anchor=north,text=otMuted] at (1.2,-0.3) {$4{,}5$};",
         r"  \node[anchor=north,text=otMuted] at (4.8,-0.3) {$5{,}5$};",
         r"  \node[anchor=west,text=otMuted] at (6.35,0) {$L$};",
         r"  \node[anchor=south east,text=otOrange!80!black] at (1.08,0.3) {$L<4{,}5$};",
         r"  \node[anchor=south west,text=otOrange!80!black] at (4.92,0.3) {$L>5{,}5$};"]
    if corrige:
        s += [r"  \node[anchor=north,text=otGreenDark] at (3,-0.3) {$\mu=5$};",
              r"  \fill[otGreenDark] (3,0) circle (2.3pt);",
              r"  \draw[guide] (1.2,0.3) -- (1.2,1.25);",
              r"  \draw[guide] (4.8,0.3) -- (4.8,1.25);",
              r"  \draw[guide] (3,0.12) -- (3,1.25);",
              r"  \draw[cote,draw=otGreenDark] (1.2,1.1) -- (3,1.1);",
              r"  \draw[cote,draw=otGreenDark] (3,1.1) -- (4.8,1.1);",
              r"  \node[anchor=south,text=otGreenDark] at (2.1,1.15) {$\delta=0{,}5$};",
              r"  \node[anchor=south,text=otGreenDark] at (3.9,1.15) {$\delta=0{,}5$};"]
    else:
        s += [r"  \node[anchor=north,text=otMuted] at (3,-0.3) {$5$};"]
    s.append(r"\end{tikzpicture}")
    return "\n".join(s)


# ---------------------------------------------------------------- exercice 823 : majorant 25/n (question 1)
def _fig823(corrige):
    vert = (r"""
  \draw[otGreenDark,line width=0.6pt,dash pattern=on 3pt off 2pt] (axis cs:500,0.05) -- (axis cs:500,0);
  \draw[otGreenDark,line width=2.4pt] (axis cs:500,0) -- (axis cs:1500,0);
  \fill[otGreenDark] (axis cs:500,0.05) circle (2.3pt);
  \node[anchor=south west,text=otGreenDark] at (axis cs:520,0.056) {$(500\,;0{,}05)$};
  \node[anchor=south,text=otGreenDark] at (axis cs:1150,0.0255) {$n\geqslant 500$};""" if corrige else "")
    return r"""
\begin{tikzpicture}
\begin{axis}[otWeb, axis lines=left, width=7.3cm, height=4.6cm, xmin=0, xmax=1560, ymin=0, ymax=0.155,
  xtick={250,500,750,1000,1250,1500}, xticklabels={$250$,$500$,$750$,$1\,000$,$1\,250$,$1\,500$},
  ytick={0.05,0.1}, yticklabels={$0{,}05$,$0{,}10$},
  xlabel={$n$},
  every axis x label/.style={at={(rel axis cs:1,0)},anchor=west,font=\normalsize,text=otMuted},
  xticklabel style={anchor=north,yshift=-2.5pt}]
  \draw[otOrange,line width=0.8pt] (axis cs:0,0.05) -- (axis cs:1500,0.05);
  \node[anchor=south,text=otOrange!80!black] at (axis cs:1300,0.054) {$y=0{,}05$};
  \addplot[otNavy,line width=1pt,domain=170:1500,samples=120] {25/x};
  \node[anchor=west,text=otNavy] at (axis cs:330,0.11) {$y=\dfrac{25}{n}$};""" + vert + r"""
\end{axis}
\end{tikzpicture}"""


# ---------------------------------------------------------------- exercice 825 : p(1 - p) <= 1/4 (question 4)
def _fig825(corrige):
    vert = (r"""
  \draw[otGreenDark,line width=0.6pt,dash pattern=on 3pt off 2pt] (axis cs:0.5,0.25) -- (axis cs:0.5,0);
  \fill[otGreenDark] (axis cs:0.5,0.25) circle (2.3pt);
  \node[anchor=south,text=otGreenDark] at (axis cs:0.5,0.262) {maximum $\dfrac{1}{4}$ en $p=\dfrac{1}{2}$};""" if corrige else "")
    return r"""
\begin{tikzpicture}
\begin{axis}[otWeb, axis lines=left, width=7.3cm, height=4.4cm, xmin=0, xmax=1.08, ymin=0, ymax=0.33,
  xtick={0.5,1}, xticklabels={$\dfrac{1}{2}$,$1$},
  ytick={0.25}, yticklabels={$\dfrac{1}{4}$},
  xlabel={$p$},
  every axis x label/.style={at={(rel axis cs:1,0)},anchor=west,font=\normalsize,text=otMuted},
  xticklabel style={anchor=north,yshift=-2.5pt}]
  \draw[otOrange,line width=0.8pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,0.25) -- (axis cs:1,0.25);
  \addplot[otNavy,line width=1pt,domain=0:1,samples=101] {x*(1-x)};
  \node[text=otNavy] at (axis cs:0.3,0.08) {$y=p(1-p)$};""" + vert + r"""
\end{axis}
\end{tikzpicture}"""


FIGURES = {
"ex821_simulation": _fig821(False),
"ex821_simulation_corrige": _fig821(True),
"ex822_boulons": _fig822(False),
"ex822_boulons_corrige": _fig822(True),
"ex823_majorant": _fig823(False),
"ex823_majorant_corrige": _fig823(True),
"ex825_parabole": _fig825(False),
"ex825_parabole_corrige": _fig825(True),
# ---------------------------------------------------------------- cours, partie I
"bt_binomiale": r"""
\begin{tikzpicture}
\begin{axis}[otBarres, width=7.8cm, height=4.4cm, bar width=6.5pt, bar shift=0pt, enlarge x limits=0.035,
  xmin=0, xmax=20, ymax=0.235, xtick={0,2,4,6,8,10,12,14,16,18,20},
  ytick={0.05,0.1,0.15}, yticklabels={$0{,}05$,$0{,}10$,$0{,}15$},
  xlabel={$k$}, xlabel style={at={(rel axis cs:1,0)},anchor=west,xshift=4pt}]
  \addplot[fill=otOrange!75,draw=otOrange!80!black] coordinates {""" + _ORANGE + r"""};
  \addplot[fill=otNavy!60,draw=otNavy] coordinates {""" + _BLEU + r"""};
  \draw[cote] (axis cs:6,0.205) -- (axis cs:10,0.205);
  \draw[cote] (axis cs:10,0.205) -- (axis cs:14,0.205);
  \draw[otMuted,line width=.5pt] (axis cs:10,0.192) -- (axis cs:10,0.218);
  \node[anchor=south,text=otInk] at (axis cs:8,0.211) {$\delta=4$};
  \node[anchor=south,text=otInk] at (axis cs:12,0.211) {$\delta=4$};
  \node[anchor=south,text=otOrange!80!black] at (axis cs:3.2,0.052) {$|X-10|\geqslant 4$};
  \node[anchor=south,text=otOrange!80!black] at (axis cs:16.8,0.052) {$|X-10|\geqslant 4$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- cours, partie IV
"lgn_convergence": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, axis lines=left, width=7.3cm, height=4.6cm, xmin=0, xmax=1040, ymin=0.25, ymax=0.76,
  xtick={200,400,600,800,1000}, xticklabels={$200$,$400$,$600$,$800$,$1\,000$},
  ytick={0.3,0.4,0.5,0.6,0.7}, yticklabels={$0{,}3$,$0{,}4$,$0{,}5$,$0{,}6$,$0{,}7$},
  xlabel={$n$}, ylabel={$f_n$},
  every axis x label/.style={at={(rel axis cs:1,0)},anchor=west,font=\normalsize,text=otMuted},
  every axis y label/.style={at={(rel axis cs:0,1)},anchor=south,font=\normalsize,text=otMuted},
  xticklabel style={anchor=north,yshift=-2.5pt}]
  \addplot[name path=H,draw=none,domain=80:1000,samples=90] {0.5+1/sqrt(0.2*x)};
  \addplot[name path=B,draw=none,domain=80:1000,samples=90] {0.5-1/sqrt(0.2*x)};
  \addplot[otGreen!18] fill between[of=H and B];
  \addplot[otGreen,line width=0.6pt,domain=80:1000,samples=90] {0.5+1/sqrt(0.2*x)};
  \addplot[otGreen,line width=0.6pt,domain=80:1000,samples=90] {0.5-1/sqrt(0.2*x)};
  \draw[otInk!75,line width=0.8pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,0.5) -- (axis cs:1000,0.5);
  """ + _COURBES + r"""
  \node[anchor=west,text=otInk] at (axis cs:1022,0.5) {$p=0{,}5$};
  \node[note,anchor=south] at (axis cs:640,0.64) {bande $0{,}5\pm\dfrac{1}{\sqrt{0{,}2\,n}}$};
\end{axis}
\end{tikzpicture}""",

# ---------------------------------------------------------------- exercice 824, question 2
"roulette_intervalle": r"""
\begin{tikzpicture}[font=\normalsize]
  \draw[otMuted,line width=.6pt,-{Stealth[length=2.3mm]}] (""" + _R["g"] + r""",0) -- (""" + _R["fin"] + r""",0);
  \foreach \x in {""" + f'{_R["a"]},{_R["pp"]},{_R["b"]}' + r"""} \draw[otMuted,line width=.6pt] (\x,-0.09) -- (\x,0.09);
  \node[anchor=north,text=otMuted] at (""" + _R["a"] + r""",-0.12) {$0{,}024$};
  \node[anchor=north,text=otGreenDark] at (""" + _R["pp"] + r""",-0.12) {$p=\frac{1}{37}$};
  \node[anchor=north,text=otMuted] at (""" + _R["b"] + r""",-0.12) {$0{,}031$};
  \draw[guide] (""" + _R["a"] + r""",0.1) -- (""" + _R["a"] + r""",1.6);
  \draw[guide] (""" + _R["b"] + r""",0.1) -- (""" + _R["b"] + r""",1.6);
  \draw[guide] (""" + _R["pp"] + r""",0.1) -- (""" + _R["pp"] + r""",0.95);
  \fill[otGreenDark] (""" + _R["pp"] + r""",0) circle (2.3pt);
  \draw[cote] (""" + _R["a"] + r""",0.45) -- (""" + _R["pp"] + r""",0.45);
  \node[anchor=south,text=otInk] at (""" + f'{(float(_R["a"]) + float(_R["pp"])) / 2:.3f}' + r""",0.5) {$\delta$};
  \draw[otGreenDark,line width=2.4pt] (""" + _R["a"] + r""",0.95) -- (""" + _R["pd"] + r""",0.95);
  \node[anchor=east,text=otGreenDark] at (""" + f'{float(_R["a"]) - 0.12:.3f}' + r""",0.95) {$[p-\delta\,;p+\delta]$};
  \node[anchor=south,text=otGreenDark] at (""" + _R["pd"] + r""",1.02) {$p+\delta$};
  \draw[otNavy,line width=2.4pt] (""" + _R["a"] + r""",1.6) -- (""" + _R["b"] + r""",1.6);
  \node[anchor=south,text=otNavy] at (""" + f'{(float(_R["a"]) + float(_R["b"])) / 2:.3f}' + r""",1.7) {intervalle de l'énoncé};
\end{tikzpicture}""",
}

if __name__ == "__main__":
    for g, t in zip(GRAINES, _TRAJ):
        print(g, min(f for _, f in t), max(f for _, f in t),
              sum(abs(f - 0.5) >= 1 / sqrt(0.2 * n) for n, f in t if n >= 80), t[-1])
