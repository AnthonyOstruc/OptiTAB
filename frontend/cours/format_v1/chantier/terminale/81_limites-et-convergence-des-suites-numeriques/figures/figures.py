# -*- coding: utf-8 -*-
"""Figures de la notion « Limites et convergence des suites » (Terminale).

Compilées par outils/figures_livre.py (préambule commun des livres OptiTAB) :

    python figures_livre.py <dossier_notion> [nom …] [--planche]

Cours : dominos de la récurrence, définition de la convergence (bande),
théorème des gendarmes, comportement de (q^n), escalier d'une suite
u_{n+1} = f(u_n). Exercices : (-2)^n, sin(n)/n encadrée, escaliers des
suites récurrentes du problème et du devoir (éléments de réponse en vert).
"""

# Suite de l'illustration de la convergence : écarts à la limite choisis pour
# que le rang N = 6 soit net (|u_5 - l| = 0,5 > eps = 0,38 > |u_6 - l| = 0,25).
ECARTS = [1.5, -1.2, 1.0, -0.8, 0.62, -0.5, 0.25, -0.2, 0.16, -0.13, 0.1, -0.08,
          0.065, -0.05, 0.04, -0.03, 0.025, -0.02, 0.015, -0.012]
LIMITE, EPS, RANG = 2.0, 0.38, 6


def _coords(points):
    return " ".join(f"({x},{y:.4f})" for x, y in points)


AVANT = _coords((n, LIMITE + d) for n, d in enumerate(ECARTS) if n < RANG)
APRES = _coords((n, LIMITE + d) for n, d in enumerate(ECARTS) if n >= RANG)


def escalier(f, u0, etapes):
    """Chemin de l'escalier (ou de la toile) : (u0,0) -> (u0,u1) -> (u1,u1) -> (u1,u2) …"""
    pts = [(u0, 0.0)]
    u = u0
    for _ in range(etapes):
        v = f(u)
        pts += [(u, v), (v, v)]
        u = v
    return pts


def _chemin(pts):
    return " -- ".join(f"(axis cs:{x:.4f},{y:.4f})" for x, y in pts)


def _termes(f, u0, n):
    t = [u0]
    for _ in range(n):
        t.append(f(t[-1]))
    return t


# Cours : u_{n+1} = 0,5 u_n + 1, u_0 = 1 (limite 2)
F_COURS = lambda x: 0.5 * x + 1
T_COURS = _termes(F_COURS, 1.0, 5)
ESC_COURS = _chemin(escalier(F_COURS, 1.0, 4))
# Problème : u_{n+1} = sqrt(u_n + 2), u_0 = 1 (limite 2)
F_PB = lambda x: (x + 2) ** 0.5
T_PB = _termes(F_PB, 1.0, 5)
ESC_PB = _chemin(escalier(F_PB, 1.0, 4))
# Devoir, partie C : v_{n+1} = (v_n + 3)/4, v_0 = 0 (limite 1)
F_DS = lambda x: (x + 3) / 4
T_DS = _termes(F_DS, 0.0, 5)
ESC_DS = _chemin(escalier(F_DS, 0.0, 4))


def _pointilles(termes, k_max):
    """Pointillés de lecture : de (u_k, u_k) sur y = x jusqu'à l'axe des abscisses."""
    return "\n".join(f"  \\draw[guide] (axis cs:{u:.4f},{u:.4f}) -- (axis cs:{u:.4f},0);"
                     for u in termes[1:k_max + 1])


# Graduations placées à la main (outil commun) : pour (-2)^n, les termes d'indice
# impair sont sous l'axe, leur graduation passe donc au-dessus (« h »).
XLAB = {
    "geo_moins2": [(1, "h", "1"), (2, "c", "2"), (3, "h", "3"), (4, "c", "4"), (5, "h", "5"), (6, "c", "6")],
}

FIGURES = {
# ------------------------------------------------------------------ cours
"rec_dominos": r"""
\begin{tikzpicture}[line join=round]
  \tikzset{domino/.style={line width=0.9pt},
           annot/.style={font=\otRegular\fontsize{9}{11.5}\selectfont,align=center}}
  \draw[otMuted,line width=0.8pt] (-0.2,0) -- (8.2,0);
  % domino P(n0) : il tombe (initialisation)
  \begin{scope}[rotate around={-27:(0.85,0)}]
    \filldraw[domino,fill=otGreen!45,draw=otGreenDark] (0.55,0) rectangle (0.85,1.6);
  \end{scope}
  % domino P(n0+1) : il bascule à son tour
  \begin{scope}[rotate around={-13:(2.55,0)}]
    \filldraw[domino,fill=otNavy!28,draw=otNavy] (2.25,0) rectangle (2.55,1.6);
  \end{scope}
  \node[text=otMuted] at (4.0,0.8) {$\cdots$};
  \filldraw[domino,fill=otNavy!12,draw=otNavy] (5.45,0) rectangle (5.75,1.6);
  \filldraw[domino,fill=otNavy!12,draw=otNavy] (7.15,0) rectangle (7.45,1.6);
  % hérédité : la chute de P(k) entraîne celle de P(k+1)
  \draw[otNavy,line width=0.9pt,-{Stealth[length=2.2mm]}] (5.7,1.85) to[bend left=55] (7.2,1.85);
  \node[annot,text=otGreenDark,anchor=south] at (0.95,2.15) {\textbf{initialisation}\\$P(n_0)$ est vraie};
  \node[annot,text=otNavy,anchor=south] at (6.45,2.5) {\textbf{hérédité} : si $P(k)$ est vraie,\\alors $P(k+1)$ est vraie};
  % noms sous les dominos
  \node[anchor=north] at (0.7,-0.12) {$P(n_0)$};
  \node[anchor=north] at (2.4,-0.12) {$P(n_0+1)$};
  \node[anchor=north] at (5.6,-0.12) {$P(k)$};
  \node[anchor=north] at (7.3,-0.12) {$P(k+1)$};
\end{tikzpicture}""",

"conv_bande": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.2cm, xmin=-0.6, xmax=21.2, ymin=-0.1, ymax=3.95,
  xtick={""" + str(RANG) + r"""}, xticklabels={rang $N$}, ytick={2}, yticklabels={$\ell$},
  xlabel={$n$}, ylabel={}, grid=none]
  \fill[otGreen!14] (axis cs:0,""" + f"{LIMITE - EPS}" + r""") rectangle (axis cs:20.4,""" + f"{LIMITE + EPS}" + r""");
  \draw[otGreen,line width=0.6pt] (axis cs:0,""" + f"{LIMITE + EPS}" + r""") -- (axis cs:20.4,""" + f"{LIMITE + EPS}" + r""");
  \draw[otGreen,line width=0.6pt] (axis cs:0,""" + f"{LIMITE - EPS}" + r""") -- (axis cs:20.4,""" + f"{LIMITE - EPS}" + r""");
  \draw[otNavy!70,line width=0.6pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,2) -- (axis cs:20.4,2);
  \draw[guide] (axis cs:""" + str(RANG) + r""",0) -- (axis cs:""" + str(RANG) + r""",3.75);
  \addplot[only marks,mark=*,mark size=1.9pt,otOrange] coordinates {""" + AVANT + r"""};
  \addplot[only marks,mark=*,mark size=1.9pt,otNavy] coordinates {""" + APRES + r"""};
  \node[anchor=west,text=otGreenDark,inner sep=1.5pt] at (axis cs:20.5,""" + f"{LIMITE + EPS + 0.1}" + r""") {$\ell+\varepsilon$};
  \node[anchor=west,text=otGreenDark,inner sep=1.5pt] at (axis cs:20.5,""" + f"{LIMITE - EPS - 0.1}" + r""") {$\ell-\varepsilon$};
  \node[anchor=south west,align=left,font=\otRegular\fontsize{9}{11.5}\selectfont,text=otInk] at (axis cs:7.3,2.75)
    {à partir du rang $N$, tous les termes\\sont dans l’intervalle $]\ell-\varepsilon\,;\ell+\varepsilon[$};
\end{axis}
\end{tikzpicture}""",

"gendarmes": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.4cm, xmin=-0.6, xmax=31.5, ymin=-0.12, ymax=2.25,
  xtick={5,10,15,20,25,30}, ytick={0.5,1,1.5,2}, xlabel={$n$}, ylabel={}]
  \draw[otMuted,line width=0.6pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,1) -- (axis cs:31,1);
  \addplot[only marks,mark=*,mark size=1.35pt,otOrange,samples at={1,...,30}] {1+1/x};
  \addplot[only marks,mark=*,mark size=1.35pt,otGreenDark,samples at={1,...,30}] {1-1/x};
  \addplot[only marks,mark=*,mark size=1.9pt,otNavy,samples at={1,...,30}] {1+sin(deg(x))/x};
  \node[anchor=south east,text=otOrange!80!black,inner sep=1.5pt] at (axis cs:31,1.12) {$w_n=1+\dfrac{1}{n}$};
  \node[anchor=north east,text=otGreenDark,inner sep=1.5pt] at (axis cs:31,0.88) {$v_n=1-\dfrac{1}{n}$};
  \node[anchor=south west,text=otNavy,inner sep=1.5pt] at (axis cs:9,1.55) {$u_n=1+\dfrac{\sin n}{n}$};
\end{axis}
\end{tikzpicture}""",

"suites_qn": r"""
\begin{tikzpicture}
\pgfplotsset{qn/.style={otWeb, width=2.6cm, height=2.3cm, xmin=-0.8, xmax=13.2, xtick={4,8,12},
  xlabel={$n$}, ylabel={}, grid=none,
  title style={font=\normalsize,yshift=-1pt,align=center}}}
\begin{axis}[qn, name=a, ymin=-0.6, ymax=10, ytick={5}, title={$q=1{,}2$\\$q^n\to+\infty$}]
  \addplot[only marks,mark=*,mark size=1.5pt,otNavy,samples at={0,...,12}] {1.2^x};
\end{axis}
\begin{axis}[qn, name=b, at={($(a.east)+(0.8cm,0)$)}, anchor=west, ymin=-0.07, ymax=1.15, ytick={0.5},
  title={$q=0{,}8$\\$q^n\to0$}]
  \addplot[only marks,mark=*,mark size=1.5pt,otGreenDark,samples at={0,...,12}] {0.8^x};
\end{axis}
% panneaux du bas : les termes sont des deux côtés de l'axe, les graduations de n
% sont donc reportées sous le panneau (aucune graduation au milieu des points)
\begin{axis}[qn, name=c, at={($(a.south)+(0,-1.9cm)$)}, anchor=north, ymin=-1.15, ymax=1.15, ytick={-0.5,0.5},
  xticklabels={}, title={$q=-0{,}8$\\$q^n\to0$}]
  \addplot[only marks,mark=*,mark size=1.5pt,otGreenDark,samples at={0,...,12}] {(-0.8)^x};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:4,-1.15) {$4$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:8,-1.15) {$8$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:12,-1.15) {$12$};
\end{axis}
\begin{axis}[qn, name=d, at={($(c.east)+(0.8cm,0)$)}, anchor=west, ymin=-10, ymax=10, ytick={-5,5},
  xticklabels={}, title={$q=-1{,}2$\\pas de limite}]
  \addplot[only marks,mark=*,mark size=1.5pt,otOrange,samples at={0,...,12}] {(-1.2)^x};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:4,-10) {$4$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:8,-10) {$8$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:12,-10) {$12$};
\end{axis}
\end{tikzpicture}""",

"escalier_cours": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.6cm, height=5.6cm, xmin=-0.12, xmax=2.55, ymin=-0.12, ymax=2.55,
  xtick={2}, ytick={1,2}, xlabel={$x$}, ylabel={$y$}]
  \addplot[otMuted,line width=0.8pt,domain=0:2.45] {x};
  \addplot[courbe,domain=0:2.45] {0.5*x+1};
""" + _pointilles(T_COURS, 2) + r"""
  \draw[otGreenDark,line width=1.1pt,line join=round] """ + ESC_COURS + r""";
  \pnt[otGreenDark]{1}{0}
  \pnt[otNavy]{2}{2}
  \node[anchor=north,yshift=-2pt] at (axis cs:""" + f"{T_COURS[0]}" + r""",0) {$u_0$};
  \node[anchor=north,yshift=-2pt] at (axis cs:""" + f"{T_COURS[1]}" + r""",0) {$u_1$};
  \node[anchor=north,yshift=-2pt] at (axis cs:""" + f"{T_COURS[2]}" + r""",0) {$u_2$};
  \node[anchor=south west,text=otMuted,inner sep=1.5pt] at (axis cs:2.45,2.45) {$y=x$};
  \node[anchor=north west,text=otNavy,inner sep=1.5pt] at (axis cs:2.45,2.2) {$y=0{,}5x+1$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------------------------ exercices
"geo_moins2": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.6cm, xmin=-0.5, xmax=7.3, ymin=-40, ymax=74,
  xtick={1,2,3,4,5,6}, xticklabels={}, xticklabel style={fill=none}, ytick={-32,16,64}, xlabel={$n$}, ylabel={}]
  \addplot[otNavy!35,line width=0.7pt,samples at={0,...,6}] {(-2)^x};
  \addplot[only marks,mark=*,mark size=2pt,otNavy,samples at={0,...,6}] {(-2)^x};
  \node[anchor=south west,text=otNavy,inner sep=1.5pt] at (axis cs:0.4,42) {$t_n=(-2)^n$};
\end{axis}
\end{tikzpicture}""",

"gend_sin_n": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.2cm, xmin=-0.6, xmax=26.2, ymin=-1.15, ymax=1.2,
  xtick={5,10,15,20,25}, xticklabels={}, xticklabel style={fill=none}, ytick={-1,-0.5,0.5,1}, xlabel={$n$}, ylabel={}]
  % graduations de l'axe des n reportées sous le graphique : les termes occupent les deux côtés de l'axe
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:5,-1.15) {$5$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:10,-1.15) {$10$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:15,-1.15) {$15$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:20,-1.15) {$20$};
  \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt] at (axis cs:25,-1.15) {$25$};
  \addplot[only marks,mark=*,mark size=1.35pt,otOrange,samples at={1,...,25}] {1/x};
  \addplot[only marks,mark=*,mark size=1.35pt,otOrange,samples at={1,...,25}] {-1/x};
  \addplot[only marks,mark=*,mark size=1.9pt,otGreenDark,samples at={1,...,25}] {sin(deg(x))/x};
  \node[anchor=south east,text=otOrange!80!black,inner sep=1.5pt] at (axis cs:26,0.14) {$\dfrac{1}{n}$};
  \node[anchor=north east,text=otOrange!80!black,inner sep=1.5pt] at (axis cs:26,-0.14) {$-\dfrac{1}{n}$};
  \node[anchor=south west,text=otGreenDark,inner sep=1.5pt] at (axis cs:7,0.45) {$\dfrac{\sin n}{n}$};
\end{axis}
\end{tikzpicture}""",

"escalier_pb": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.6cm, height=5.6cm, xmin=-0.12, xmax=2.6, ymin=-0.12, ymax=2.6,
  xtick=\empty, ytick={1,2}, xlabel={$x$}, ylabel={$y$}]
  \addplot[otMuted,line width=0.8pt,domain=0:2.5] {x};
  \addplot[courbe,domain=0:2.5] {sqrt(x+2)};
""" + _pointilles(T_PB, 2) + r"""
  \draw[otGreenDark,line width=1.1pt,line join=round] """ + ESC_PB + r""";
  \pnt[otGreenDark]{1}{0}
  \pnt[otGreenDark]{2}{2}
  \node[anchor=north,yshift=-2pt] at (axis cs:""" + f"{T_PB[0]:.4f}" + r""",0) {$u_0$};
  \node[anchor=north,yshift=-2pt] at (axis cs:""" + f"{T_PB[1]:.4f}" + r""",0) {$u_1$};
  \node[anchor=north,yshift=-2pt] at (axis cs:""" + f"{T_PB[2]:.4f}" + r""",0) {$u_2$};
  \node[anchor=south east,text=otGreenDark,inner sep=1.5pt] at (axis cs:1.93,2.07) {$\ell=2$};
  \node[anchor=south west,text=otMuted,inner sep=1.5pt] at (axis cs:2.5,2.5) {$y=x$};
  \node[anchor=north west,text=otNavy,inner sep=1.5pt] at (axis cs:2.5,2.06) {$y=\sqrt{x+2}$};
\end{axis}
\end{tikzpicture}""",

"escalier_ds": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.6cm, height=5.6cm, xmin=0, xmax=1.42, ymin=0, ymax=1.42,
  xtick=\empty, ytick={0.5,1}, xlabel={$x$}, ylabel={$y$}]
  \addplot[otMuted,line width=0.8pt,domain=0:1.35] {x};
  \addplot[courbe,domain=0:1.35] {(x+3)/4};
""" + _pointilles(T_DS, 2) + r"""
  \draw[otGreenDark,line width=1.1pt,line join=round] """ + ESC_DS + r""";
  \pnt[otGreenDark]{0}{0}
  \pnt[otGreenDark]{1}{1}
  \node[anchor=north,yshift=-2pt] at (axis cs:""" + f"{T_DS[0]:.4f}" + r""",0) {$v_0$};
  \node[anchor=north,yshift=-2pt] at (axis cs:""" + f"{T_DS[1]:.4f}" + r""",0) {$v_1$};
  \node[anchor=north,yshift=-2pt] at (axis cs:""" + f"{T_DS[2]:.4f}" + r""",0) {$v_2$};
  \node[anchor=south east,text=otGreenDark,inner sep=1.5pt] at (axis cs:0.97,1.04) {$\ell=1$};
  \node[anchor=south west,text=otMuted,inner sep=1.5pt] at (axis cs:1.35,1.35) {$y=x$};
  \node[anchor=north west,text=otNavy,inner sep=1.5pt] at (axis cs:1.35,1.06) {$y=\dfrac{x+3}{4}$};
\end{axis}
\end{tikzpicture}""",
}

# =================================================================== finition 2026-11-02
# Figures des corrigés ajoutées (éléments de réponse en vert).
GRAD = r"font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.3pt"


def _xlab_bas(valeurs, y):
    """Graduations de l'axe des n reportées sous le graphique (termes des deux côtés de l'axe)."""
    return "\n".join(f"  \\node[anchor=north,{GRAD}] at (axis cs:{v},{y}) {{${v}$}};" for v in valeurs)


FIGURES.update({
# 1162 Q5 : s_n = 5 + 2/n converge vers 5 par valeurs supérieures
"decouv_sn": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4cm, xmin=-0.6, xmax=21.5, ymin=-0.4, ymax=7.8,
  xtick={5,10,15,20}, ytick={1,2,3,4,5,6,7}, xlabel={$n$}, ylabel={}]
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,5) -- (axis cs:21,5);
  \addplot[only marks,mark=*,mark size=1.8pt,otNavy,samples at={1,...,20}] {5+2/x};
  \node[anchor=north east,text=otGreenDark,inner sep=1.5pt] at (axis cs:21,4.7) {$\ell=5$};
  \node[anchor=south west,text=otNavy,inner sep=1.5pt] at (axis cs:4,6.2) {$s_n=5+\dfrac{2}{n}$};
\end{axis}
\end{tikzpicture}""",

# 1163 Q4 : 2 - 5/n^2 converge vers 2 par valeurs inférieures
"decouv_2moins": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4.2cm, xmin=-0.6, xmax=16.5, ymin=-3.6, ymax=3.2,
  xtick={5,10,15}, ytick={-3,-2,-1,1,2}, xlabel={$n$}, ylabel={}]
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,2) -- (axis cs:16,2);
  \addplot[only marks,mark=*,mark size=1.8pt,otNavy,samples at={1,...,15}] {2-5/x^2};
  \node[anchor=south east,text=otGreenDark,inner sep=1.5pt] at (axis cs:16,2.15) {$\ell=2$};
  \node[anchor=north west,text=otNavy,inner sep=1.5pt] at (axis cs:4,-0.9) {$u_n=2-\dfrac{5}{n^2}$};
\end{axis}
\end{tikzpicture}""",

# 1167 Q6 : sqrt(n^2 + n) - n converge vers 1/2
"fi_racine": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=3.8cm, xmin=-0.6, xmax=21.5, ymin=-0.06, ymax=0.66,
  xtick={5,10,15,20}, ytick={0.1,0.2,0.3,0.4}, xlabel={$n$}, ylabel={}]
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,0.5) -- (axis cs:21,0.5);
  \addplot[only marks,mark=*,mark size=1.8pt,otNavy,samples at={1,...,20}] {sqrt(x^2+x)-x};
  \node[anchor=south east,text=otGreenDark,inner sep=1.5pt] at (axis cs:21,0.52) {$\ell=\dfrac{1}{2}$};
  \node[anchor=north west,text=otNavy,inner sep=1.5pt] at (axis cs:5,0.4) {$u_n=\sqrt{n^2+n}-n$};
\end{axis}
\end{tikzpicture}""",

# 1168 Q1 : deux escaliers de 1 + 2 + ... + 5 forment un rectangle 5 x 6
"gauss_escalier": r"""
\begin{tikzpicture}[x=0.55cm,y=0.55cm]
  \foreach \i in {1,...,5}{
    \foreach \j in {1,...,\i}{\filldraw[fill=otNavy!70,draw=white,line width=1.2pt] (\i-1,\j-1) rectangle (\i,\j);}
    \foreach \j in {\i,...,5}{\filldraw[fill=otGreen!65,draw=white,line width=1.2pt] (\i-1,\j) rectangle (\i,\j+1);}
  }
  \draw[decorate,decoration={brace,mirror,amplitude=4pt},otMuted,line width=0.6pt] (0,-0.3) -- (5,-0.3);
  \node[anchor=north] at (2.5,-0.75) {$n=5$};
  \draw[decorate,decoration={brace,amplitude=4pt},otMuted,line width=0.6pt] (-0.3,0) -- (-0.3,6);
  \node[anchor=east] at (-0.75,3) {$n+1=6$};
  % légende sous la figure (largeur réduite pour le téléphone)
  \filldraw[fill=otNavy!70,draw=white] (-3.2,-2.75) rectangle (-2.6,-2.15);
  \node[anchor=west] at (-2.4,-2.45) {$1+2+3+4+5=15$};
  \filldraw[fill=otGreen!65,draw=white] (-3.2,-3.85) rectangle (-2.6,-3.25);
  \node[anchor=west,text=otGreenDark] at (-2.4,-3.55) {le même escalier, retourné};
  \node[anchor=west,text=otGreenDark] at (-3.2,-4.75) {donc $2\times 15=5\times 6=30$};
\end{tikzpicture}""",

# 1169 Q4 : 2^n et n^2, l'inégalité est vraie à partir de n = 4
"rec_2n_n2": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.6cm, xmin=-0.4, xmax=7.4, ymin=-4, ymax=74,
  xtick={1,2,3,4,5,6}, ytick={16,32,48,64}, xlabel={$n$}, ylabel={}]
  \fill[otGreen!13] (axis cs:3.65,0) rectangle (axis cs:6.6,70);
  \addplot[only marks,mark=square*,mark size=2.1pt,otOrange,samples at={0,...,6}] {x^2};
  \addplot[only marks,mark=*,mark size=1.8pt,otNavy,samples at={0,...,6}] {2^x};
  \node[anchor=west,text=otNavy,inner sep=1.5pt] at (axis cs:6.2,64) {$2^n$};
  \node[anchor=west,text=otOrange!80!black,inner sep=1.5pt] at (axis cs:6.2,36) {$n^2$};
  \node[anchor=north,text=otGreenDark,align=center,font=\otRegular\fontsize{9}{11}\selectfont] at (axis cs:5.1,69)
    {$2^n\ge n^2$\\pour $n\ge4$};
  \node[anchor=south,text=otOrange!80!black,align=center,font=\otRegular\fontsize{9}{11}\selectfont] at (axis cs:2.4,15)
    {$n=3$ :\\$8<9$};
\end{axis}
\end{tikzpicture}""",

# 1166 Q1 : (n + (-1)^n sqrt n)/(n + 1) entre ses deux gendarmes
"gend_racine": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.6cm, xmin=-0.8, xmax=41.5, ymin=-0.08, ymax=1.5,
  xtick={10,20,30,40}, ytick={0.5,1}, xlabel={$n$}, ylabel={}]
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,1) -- (axis cs:41,1);
  \addplot[only marks,mark=*,mark size=1.1pt,otOrange,samples at={1,...,40}] {(x+sqrt(x))/(x+1)};
  \addplot[only marks,mark=*,mark size=1.1pt,otOrange,samples at={1,...,40}] {(x-sqrt(x))/(x+1)};
  \addplot[only marks,mark=*,mark size=1.7pt,otNavy,samples at={1,...,40}] {(x+(-1)^x*sqrt(x))/(x+1)};
  \node[anchor=south east,text=otOrange!80!black,inner sep=1.5pt] at (axis cs:41,1.21) {$\dfrac{n+\sqrt{n}}{n+1}$};
  \node[anchor=north east,text=otOrange!80!black,inner sep=1.5pt] at (axis cs:41,0.74) {$\dfrac{n-\sqrt{n}}{n+1}$};
  \node[anchor=west,text=otGreenDark,inner sep=1.5pt] at (axis cs:41.2,1) {$1$};
\end{axis}
\end{tikzpicture}""",

# 1171 B1 : (2n + sin n)/(n + 1) entre (2n - 1)/(n + 1) et (2n + 1)/(n + 1)
"ds_gend": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.4cm, xmin=-0.6, xmax=31.5, ymin=-0.12, ymax=2.4,
  xtick={5,10,15,20,25,30}, ytick={0.5,1,1.5,2}, xlabel={$n$}, ylabel={}]
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 4pt off 2.5pt] (axis cs:0,2) -- (axis cs:31,2);
  \addplot[only marks,mark=*,mark size=1.1pt,otOrange,samples at={1,...,30}] {(2*x+1)/(x+1)};
  \addplot[only marks,mark=*,mark size=1.1pt,otOrange,samples at={1,...,30}] {(2*x-1)/(x+1)};
  \addplot[only marks,mark=*,mark size=1.7pt,otNavy,samples at={1,...,30}] {(2*x+sin(deg(x)))/(x+1)};
  \node[anchor=south east,text=otGreenDark,inner sep=1.5pt] at (axis cs:31,2.05) {$\ell=2$};
  \node[anchor=north east,align=right,inner sep=1.5pt] at (axis cs:31,1.4)
    {\textcolor{otOrange!80!black}{gendarmes : $\dfrac{2n-1}{n+1}$ et $\dfrac{2n+1}{n+1}$}\\[2pt]
     \textcolor{otNavy}{$u_n=\dfrac{2n+\sin n}{n+1}$}};
\end{axis}
\end{tikzpicture}""",
})
