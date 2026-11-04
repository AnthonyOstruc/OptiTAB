# -*- coding: utf-8 -*-
"""Figures de la notion « Notion de fonction (Python) », Seconde.

Compilées par outils/figures_livre.py (style des livres OptiTAB).
- machine_fonction : schéma argument -> fonction -> valeur renvoyée ;
- frequence_six : fréquence du 6 en fonction du nombre n de lancers
  (simulation reproductible, graine fixée) ;
- frequence_tir : fréquence de réussite d'un tir réussi avec la
  probabilité 0,7 (exercice nouveau-1).
"""
import random

GRAINE_SIX = 2019
GRAINE_TIR = 7


def frequences(graine, nmax, succes, pas=10, debut=10):
    """Fréquences cumulées de succès pour n = debut, debut+pas, …, nmax."""
    gen = random.Random(graine)
    k = 0
    points = []
    for n in range(1, nmax + 1):
        if succes(gen):
            k += 1
        if n >= debut and n % pas == 0:
            points.append((n, k / n))
    return points


def coords(points):
    return " ".join(f"({n},{f:.4f})" for n, f in points)


SIX = frequences(GRAINE_SIX, 3000, lambda g: g.randint(1, 6) == 6)
TIR = frequences(GRAINE_TIR, 3000, lambda g: g.random() < 0.7)


MACHINE = r"""
\begin{tikzpicture}[font=\normalsize]
  \node[draw=otNavy,fill=otSky,line width=0.9pt,rounded corners=3pt,
        minimum width=1.5cm,minimum height=1.05cm,text=otNavy] (a) at (0,0) {$4$};
  \node[fill=otNavy,rounded corners=4pt,minimum width=3.1cm,minimum height=1.45cm,
        text=white,align=center] (f) at (3.45,0)
        {\texttt{f}\\[2pt]{\small renvoie $3\times x+2$}};
  \node[draw=otGreenDark,fill=otGreen!15,line width=0.9pt,rounded corners=3pt,
        minimum width=1.5cm,minimum height=1.05cm,text=otGreenDark] (r) at (6.9,0) {$14$};
  \draw[otMuted,line width=0.9pt,-{Stealth[length=2.6mm]}] (a.east) -- (f.west);
  \draw[otMuted,line width=0.9pt,-{Stealth[length=2.6mm]}] (f.east) -- (r.west);
  \node[note,text=otNavy,anchor=south] at ($(a.north)+(0,0.12)$) {argument};
  \node[note,text=otNavy,anchor=south] at ($(f.north)+(0,0.12)$) {fonction};
  \node[note,text=otGreenDark,anchor=south] at ($(r.north)+(0,0.12)$) {valeur renvoyée};
  \node[anchor=north,text=otInk] at ($(f.south)+(0,-0.22)$)
        {l'appel \texttt{f(4)} renvoie $3\times 4+2=14$};
\end{tikzpicture}
"""


def courbe_frequence(points, p, etiquette, ylabel, ymax, yticks):
    return r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.0cm, height=4.3cm,
  xmin=0, xmax=3150, ymin=0, ymax=%(ymax)s,
  xtick={1000,2000,3000}, ytick={%(yt)s},
  xlabel={$n$}, ylabel={%(ylabel)s},
  every axis y label/.style={at={(current axis.above origin)},anchor=south west,xshift=-4pt,
    font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,yshift=2pt}]
  \draw[asymptote] (axis cs:0,%(p)s) -- (axis cs:3150,%(p)s);
  \node[anchor=west,text=otRed!85!black] at (axis cs:3180,%(p)s) {%(etiq)s};
  \addplot[courbe,line width=1.1pt,mark=none] coordinates {%(c)s};
\end{axis}
\end{tikzpicture}
""" % {"ymax": ymax, "yt": ",".join(yticks), "ylabel": ylabel,
       "p": p, "etiq": etiquette, "c": coords(points)}


# ====================================================== finition 2026-11-02
# Les données des figures d'exercices sont obtenues en EXÉCUTANT le code
# Python écrit dans exercices.txt (blocs ```python), avec une graine fixée
# quand il y a du hasard : la figure montre exactement ce que calcule la
# fonction de l'énoncé.
import re
import textwrap
from pathlib import Path

NOTION = Path(__file__).resolve().parent.parent


def bloc(nom_def, contient=None, fichier="exercices.txt"):
    """Premier bloc ```python du fichier qui définit `nom_def` (et contient `contient`)."""
    texte = (NOTION / fichier).read_text(encoding="utf-8")
    for b in re.findall(r"```python\n(.*?)```", texte, re.S):
        code = textwrap.dedent(b)
        if re.search(rf"^def {nom_def}\(", code, re.M) and (contient is None or contient in code):
            return code
    raise KeyError(nom_def)


def executer(*codes, graine=None):
    """Exécute les blocs dans un même espace de noms (randint, random importés)."""
    ns = {}
    exec("from random import randint, random", ns)
    if graine is not None:
        random.seed(graine)
    for c in codes:
        exec(c, ns)
    return ns


# 1938 : table de valeurs calculée par mystere
NS_MYSTERE = executer(bloc("mystere"))
PTS_MYSTERE = [(x, NS_MYSTERE["mystere"](x)) for x in range(-6, 2)]
# 1939 : f et g (exercice)
NS_1939 = executer(bloc("f", "y = y + 3"), bloc("g", "y = y + 7"))
PTS_F = [(x, NS_1939["f"](x)) for x in range(-1, 6)]
PTS_G = [(x, NS_1939["g"](x)) for x in range(-1, 6)]
# 1940 : 10 000 appels de deux_des()
GRAINE_DEUX = 1940
NS_DEUX = executer(bloc("deux_des"), graine=GRAINE_DEUX)
_sommes = [NS_DEUX["deux_des"]() for _ in range(10000)]
FREQ_DEUX = [(s, _sommes.count(s) / 10000) for s in range(2, 13)]
# 1941 : stats_des(10000) avec la graine 41 (couple annoncé dans l'énoncé) ;
# la même graine redonne les mêmes 10 000 lancers, dont on compte les faces.
GRAINE_STATS = 41
NS_STATS = executer(bloc("stats_des"), graine=GRAINE_STATS)
M_STATS, E_STATS = NS_STATS["stats_des"](10000)
random.seed(GRAINE_STATS)
_faces = [random.randint(1, 6) for _ in range(10000)]
FREQ_FACES = [(k, _faces.count(k) / 10000) for k in range(1, 7)]
# 1942 : frequence_pair(n) pour n = 10, 20, ..., 3000 (un appel par valeur de n)
NS_PAIR = executer(bloc("frequence_pair"), graine=1942)
PAIR = [(n, NS_PAIR["frequence_pair"](n)) for n in range(10, 3001, 10)]
# 1943 : nb_gagnants(n) / n pour n = 10, 20, ..., 3000
NS_TOMBOLA = executer(bloc("tirage"), bloc("nb_gagnants"), graine=1943)
GAGNANTS = [(n, NS_TOMBOLA["nb_gagnants"](n) / n) for n in range(10, 3001, 10)]


def machine(entree, nom, regle, sortie, legende):
    return r"""
\begin{tikzpicture}[font=\normalsize]
  \node[draw=otNavy,fill=otSky,line width=0.9pt,rounded corners=3pt,
        minimum width=1.5cm,minimum height=1.05cm,text=otNavy] (a) at (0,0) {%(e)s};
  \node[fill=otNavy,rounded corners=4pt,minimum width=3.1cm,minimum height=1.45cm,
        text=white,align=center] (f) at (3.45,0)
        {\texttt{%(n)s}\\[2pt]{\small %(r)s}};
  \node[draw=otGreenDark,fill=otGreen!15,line width=0.9pt,rounded corners=3pt,
        minimum width=1.5cm,minimum height=1.05cm,text=otGreenDark] (s) at (6.9,0) {%(s)s};
  \draw[otMuted,line width=0.9pt,-{Stealth[length=2.6mm]}] (a.east) -- (f.west);
  \draw[otMuted,line width=0.9pt,-{Stealth[length=2.6mm]}] (f.east) -- (s.west);
  \node[note,text=otNavy,anchor=south] at ($(a.north)+(0,0.12)$) {argument};
  \node[note,text=otNavy,anchor=south] at ($(f.north)+(0,0.12)$) {fonction};
  \node[note,text=otGreenDark,anchor=south] at ($(s.north)+(0,0.12)$) {valeur renvoyée};
  \node[anchor=north,text=otInk] at ($(f.south)+(0,-0.22)$) {%(l)s};
\end{tikzpicture}
""" % {"e": entree, "n": nom, "r": regle, "s": sortie, "l": legende}


def print_return(appel_r, corps_r, appel_p, corps_p, val, nom_r, nom_p):
    """Deux lignes : la fonction qui renvoie (return) et celle qui affiche (print)."""
    return r"""
\begin{tikzpicture}[font=\normalsize,
  appel/.style={draw=otNavy,fill=otSky,line width=0.9pt,rounded corners=3pt,minimum width=2.4cm,minimum height=0.95cm,text=otNavy},
  corps/.style={fill=otNavy,rounded corners=4pt,minimum width=2.9cm,minimum height=0.95cm,text=white},
  fl/.style={otMuted,line width=0.9pt,-{Stealth[length=2.4mm]}}]
  \node[appel] (a1) at (0,0) {\texttt{%(ar)s}};
  \node[corps] (c1) at (3.55,0) {\texttt{%(cr)s}};
  \node[draw=otGreenDark,fill=otGreen!15,line width=0.9pt,rounded corners=3pt,minimum width=1.5cm,minimum height=0.95cm,text=otGreenDark] (r1) at (6.75,0) {$%(v)s$};
  \draw[fl] (a1.east) -- (c1.west); \draw[fl] (c1.east) -- (r1.west);
  \node[note,text=otGreenDark,anchor=south] at ($(r1.north)+(0,0.1)$) {renvoie};
  \node[anchor=north,text=otInk,font=\small] at ($(c1.south)+(0,-0.15)$) {\texttt{y = %(ar)s} : \texttt{y} vaut $%(v)s$};
  \node[appel] (a2) at (0,-2.45) {\texttt{%(ap)s}};
  \node[corps] (c2) at (3.55,-2.45) {\texttt{%(cp)s}};
  \node[draw=otRed,fill=otRed!8,line width=0.9pt,rounded corners=3pt,minimum width=1.5cm,minimum height=0.95cm,text=otRed!85!black] (r2) at (6.75,-2.45) {\texttt{None}};
  \draw[fl] (a2.east) -- (c2.west); \draw[fl] (c2.east) -- (r2.west);
  \node[note,text=otRed!85!black,anchor=south] at ($(r2.north)+(0,0.1)$) {renvoie};
  \node[note,text=otOrange!80!black,anchor=south] at ($(c2.north)+(0,0.1)$) {affiche $%(v)s$ à l'écran};
  \node[anchor=north,text=otInk,font=\small] at ($(c2.south)+(0,-0.15)$) {\texttt{y = %(ap)s} : \texttt{y} vaut \texttt{None}};
  \node[note,text=otNavy,anchor=south west] at ($(a1.north west)+(0,0.1)$) {avec \texttt{return}};
  \node[note,text=otNavy,anchor=south west] at ($(a2.north west)+(0,0.1)$) {avec \texttt{print}};
\end{tikzpicture}
""" % {"ar": appel_r.replace("_", r"\_"), "cr": corps_r, "ap": appel_p.replace("_", r"\_"),
       "cp": corps_p, "v": val}


MACHINE_AFFINE = r"""
\begin{tikzpicture}[font=\normalsize,
  arg/.style={draw=otNavy,fill=otSky,line width=0.8pt,rounded corners=2pt,minimum width=1.55cm,minimum height=0.62cm,text=otNavy,inner sep=2pt},
  fl/.style={otMuted,line width=0.8pt,-{Stealth[length=2.2mm]}}]
""" + "".join(r"""
  \node[anchor=west,text=otInk] at (-0.8,%(y0)s) {appel \texttt{%(appel)s}};
  \node[arg] (a%(k)s) at (0,%(ya)s) {$a = %(a)s$};
  \node[arg] (b%(k)s) at (0,%(yb)s) {$b = %(b)s$};
  \node[arg] (x%(k)s) at (0,%(yx)s) {$x = %(x)s$};
  \node[fill=otNavy,rounded corners=4pt,minimum width=2.7cm,minimum height=1.9cm,text=white,align=center] (f%(k)s) at (3.3,%(yb)s)
     {\texttt{affine}\\[3pt]{\small renvoie}\\{\small $a\times x+b$}};
  \draw[fl] (a%(k)s.east) -- (f%(k)s.west |- a%(k)s.east);
  \draw[fl] (b%(k)s.east) -- (f%(k)s.west |- b%(k)s.east);
  \draw[fl] (x%(k)s.east) -- (f%(k)s.west |- x%(k)s.east);
  \node[draw=otGreenDark,fill=otGreen!15,line width=0.9pt,rounded corners=3pt,minimum width=1.3cm,minimum height=0.9cm,text=otGreenDark] (r%(k)s) at (6.4,%(yb)s) {$%(r)s$};
  \draw[fl] (f%(k)s.east) -- (r%(k)s.west);
  \node[anchor=north,text=otGreenDark,font=\small] at ($(r%(k)s.south)+(0,-0.12)$) {$%(calc)s$};
""" % dict(k=k, appel=appel, a=a, b=b, x=x, r=r, calc=calc, y0=y0, ya=y0 - 0.65, yb=y0 - 1.45, yx=y0 - 2.25)
    for k, (appel, a, b, x, r, calc, y0) in enumerate([
        ("affine(3, -1, 4)", "3", "-1", "4", "11", r"3\times 4+(-1)", 0),
        ("affine(-1, 4, 3)", "-1", "4", "3", "1", r"(-1)\times 3+4", -3.3)])
) + r"""
\end{tikzpicture}
"""


def nuage(points, opts, extra=""):
    pts = " ".join(rf"\pnt{{{x}}}{{{y}}}" for x, y in points)
    return r"""
\begin{tikzpicture}
\begin{axis}[otWeb, %s]
%s
  %s
\end{axis}
\end{tikzpicture}
""" % (opts, extra, pts)


def barres(donnees, opts, extra=""):
    c = " ".join(f"({k},{f:.4f})" for k, f in donnees)
    return r"""
\begin{tikzpicture}
\begin{axis}[otBarres, clip=false, scaled y ticks=false,
  yticklabel style={/pgf/number format/fixed, /pgf/number format/precision=2}, %s]
%s
  \addplot[fill=otNavy!60,draw=otNavy] coordinates {%s};
\end{axis}
\end{tikzpicture}
""" % (opts, extra, c)


FIGURES = {
    "machine_fonction": MACHINE,
    "frequence_six": courbe_frequence(
        SIX, f"{1/6:.5f}", r"$\frac{1}{6}$", r"fréquence du 6", "0.35",
        ["0.1", "0.2", "0.3"]),
    "frequence_tir": courbe_frequence(
        TIR, "0.7", r"$0{,}7$", r"fréquence de réussite", "1.1",
        ["0.2", "0.4", "0.6", "0.8", "1"]),
    # ---------------------------------------------- finition 2026-11-02
    "machine_triple": machine("$4$", "triple", r"renvoie $3\times x$", "$12$",
                              r"l'appel \texttt{triple(4)} renvoie $3\times 4=12$"),
    "print_return_triple": print_return("triple(4)", "return 3 * x", "triple_b(4)", "print(3 * x)",
                                        "12", "triple", "triple_b"),
    "print_return_double": print_return("double(5)", "return 2 * x", "double(5)", "print(2 * x)",
                                        "10", "double", "double"),
    "machine_affine": MACHINE_AFFINE,
    "points_mystere": nuage(PTS_MYSTERE,
        r"width=5.8cm, height=6cm, xmin=-6.8, xmax=1.8, ymin=-4.6, ymax=20.5, xtick={-6,-5,-4,-3,-2,-1,1}, ytick={-3,3,6,9,12,15,18}, xticklabels={}, yticklabels={}",
        r"""  \addplot[pale, dashed, domain=-6.6:1.6] {3*x+15};
  \node[note,anchor=north] at ([yshift=-3pt]axis cs:-6,0) {$-6$};
  \node[note,anchor=north] at ([yshift=-3pt]axis cs:-4,0) {$-4$};
  \node[note,anchor=south] at ([yshift=3pt]axis cs:-5,0) {$-5$};
  \node[note,anchor=north] at ([yshift=-3pt]axis cs:-2,0) {$-2$};
  \node[note,anchor=north] at ([yshift=-3pt]axis cs:-1,0) {$-1$};
  \node[note,anchor=north] at ([yshift=-3pt]axis cs:1,0) {$1$};
  \node[note,anchor=east] at ([xshift=-3pt]axis cs:0,6) {$6$};
  \node[note,anchor=east] at ([xshift=-3pt]axis cs:0,12) {$12$};
  \node[note,anchor=east] at ([xshift=-3pt]axis cs:0,18) {$18$};
  \node[text=otNavy,anchor=west] at (axis cs:-5.6,15.5) {$y=3x+15$};"""),
    "points_f_1939": nuage(PTS_F,
        r"width=5.6cm, height=5.2cm, xmin=-1.6, xmax=5.6, ymin=-2.2, ymax=9.4, xtick={-1,1,2,3,4,5}, ytick={-1,1,2,3,4,5,6,7,8}, xticklabels={}, yticklabels={}",
        r"""  \addplot[courbe, domain=-1.15:5.15] {x^2-4*x+3};
  \node[note,anchor=north east] at ([xshift=-2pt,yshift=-3pt]axis cs:-1,0) {$-1$};
  \node[note,text=otGreenDark,anchor=south] at ([yshift=3pt]axis cs:1,0) {$1$};
  \node[note,anchor=south] at ([yshift=3pt]axis cs:2,0) {$2$};
  \node[note,text=otGreenDark,anchor=south] at ([yshift=3pt]axis cs:3,0) {$3$};
  \node[note,anchor=north] at ([yshift=-3pt]axis cs:4,0) {$4$};
  \node[note,anchor=north] at ([yshift=-3pt]axis cs:5,0) {$5$};
  \node[note,anchor=east] at ([xshift=-3pt]axis cs:0,8) {$8$};
  \node[note,anchor=west] at ([xshift=3pt]axis cs:0,3) {$3$};
  \node[note,anchor=east] at ([xshift=-3pt]axis cs:0,-1) {$-1$};
  \node[text=otNavy,anchor=west] at (axis cs:5.2,8.6) {$\mathcal{C}_f$};"""),
    "points_g_1939": nuage(PTS_G,
        r"width=5.6cm, height=6cm, xmin=-1.6, xmax=5.6, ymin=-2.2, ymax=13.4, xtick={-1,1,2,3,4,5}, ytick={-1,1,2,3,4,5,6,7,8,9,10,11,12}, xticklabels={}, yticklabels={}",
        r"""  \addplot[pale, domain=-1.15:5.15] {x^2-4*x+3};
  \addplot[courbe2, domain=-1.15:5.15] {x^2-4*x+7};
  \draw[otOrange!85!black,line width=0.9pt,-{Stealth[length=2mm]}] (axis cs:2,-1) -- (axis cs:2,2.85);
  \node[note,text=otOrange!80!black,anchor=west] at (axis cs:2.1,0.9) {$+4$};
  \node[note,anchor=north] at ([yshift=-3pt]axis cs:-1,0) {$-1$};
  \node[note,anchor=north] at ([yshift=-3pt]axis cs:1,0) {$1$};
  \node[note,anchor=north] at ([yshift=-3pt]axis cs:3,0) {$3$};
  \node[note,anchor=north] at ([yshift=-3pt]axis cs:4,0) {$4$};
  \node[note,anchor=north] at ([yshift=-3pt]axis cs:5,0) {$5$};
  \node[note,anchor=west] at ([xshift=3pt]axis cs:0,4) {$4$};
  \node[note,anchor=east] at ([xshift=-3pt]axis cs:0,12) {$12$};
  \node[note,anchor=west] at ([xshift=3pt]axis cs:0,8) {$8$};
  \node[text=otGreenDark,anchor=west] at (axis cs:5.2,12.4) {$\mathcal{C}_g$};
  \node[text=otNavy!55,anchor=west] at (axis cs:5.2,8.6) {$\mathcal{C}_f$};"""),
    "somme_deux_des": barres(FREQ_DEUX,
        r"width=7.4cm, height=4.4cm, bar width=11pt, xtick={2,3,4,5,6,7,8,9,10,11,12}, ymax=0.2, ytick={0.05,0.1,0.15,0.2}, xlabel={somme des deux dés}, ylabel={fréquence}, enlarge x limits=0.06, ylabel style={at={(axis description cs:0,1)},anchor=south west,rotate=-90,xshift=-6pt,yshift=2pt}"),
    "stats_des_1941": barres(FREQ_FACES,
        r"width=7cm, height=4.4cm, bar width=18pt, xtick={1,2,3,4,5,6}, xmin=0.4, xmax=6.6, enlarge x limits=false, ymax=0.255, ytick={0.05,0.1,0.15}, xlabel={face du dé}, ylabel={fréquence}, ylabel style={at={(axis description cs:0,1)},anchor=south east,rotate=-90,xshift=4pt,yshift=2pt}",
        r"""  \fill[otGreen,opacity=0.13] (axis cs:%(a).4f,0) rectangle (axis cs:%(b).4f,0.255);
  \draw[otGreenDark,line width=1.1pt] (axis cs:%(m).4f,0) -- (axis cs:%(m).4f,0.255);
  \draw[otGreenDark,line width=0.6pt,dash pattern=on 3pt off 2pt] (axis cs:%(a).4f,0) -- (axis cs:%(a).4f,0.255);
  \draw[otGreenDark,line width=0.6pt,dash pattern=on 3pt off 2pt] (axis cs:%(b).4f,0) -- (axis cs:%(b).4f,0.255);
  \node[note,text=otGreenDark,fill=none,anchor=south] at (axis cs:%(m).4f,0.257) {$m\approx 3{,}48$};
  \node[note,text=otGreenDark,fill=none,anchor=south] at (axis cs:%(a).4f,0.257) {$m-\sigma$};
  \node[note,text=otGreenDark,fill=none,anchor=south] at (axis cs:%(b).4f,0.257) {$m+\sigma$};""" % {
            "m": M_STATS, "a": M_STATS - E_STATS, "b": M_STATS + E_STATS}),
    "freq_pair_1942": courbe_frequence(
        PAIR, "0.5", r"$0{,}5$", r"\texttt{frequence\_pair(n)}", "1.05",
        ["0.25", "0.5", "0.75", "1"]),
    "freq_gagnants_1943": courbe_frequence(
        GAGNANTS, "0.2", r"$0{,}2$", r"\texttt{nb\_gagnants(n) / n}", "0.62",
        ["0.1", "0.2", "0.3", "0.4", "0.5"]),
}
