# -*- coding: utf-8 -*-
"""Figures du chapitre pilote, dans le style des livres OptiTAB.

    python figures.py            # toutes les figures
    python figures.py nom1 nom2  # quelques figures

Chaîne des livres : LuaLaTeX + TikZ/pgfplots, Libertinus (texte, maths) et
Montserrat (graduations), palette du logo (otNavy, otGreen…). Réglages web :
largeur ~9,5 cm et textes agrandis, pour rester lisibles sur téléphone.
Sortie : images/<nom>.png (240 ppp, fond blanc), à afficher à la moitié de
sa taille en pixels (double résolution) : même taille de texte sur toutes les figures.
"""
import re
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
BUILD = ICI / "build"
SORTIE = ICI / "images"

PREAMBULE = r"""
\documentclass[border=6pt]{standalone}
\usepackage{amsmath}
\usepackage{unicode-math}
\setmainfont{LibertinusSerif}[Extension=.otf, UprightFont=*-Regular, ItalicFont=*-Italic,
  BoldFont=*-Semibold, BoldItalicFont=*-SemiboldItalic]
\setmathfont{LibertinusMath-Regular.otf}
\newfontfamily\otRegular{Montserrat}[Extension=.otf, UprightFont=*-Regular, BoldFont=*-SemiBold]
\newfontfamily\otMedium{Montserrat}[Extension=.otf, UprightFont=*-Medium, BoldFont=*-SemiBold]
\usepackage{xcolor}
\definecolor{otNavy}{HTML}{1B3C8E}
\definecolor{otGreen}{HTML}{5FAC60}
\definecolor{otGreenDark}{HTML}{3B8544}
\definecolor{otInk}{HTML}{1C2130}
\definecolor{otMuted}{HTML}{6B7385}
\definecolor{otRule}{HTML}{D5DAE3}
\definecolor{otOrange}{HTML}{F0A23B}
\definecolor{otRed}{HTML}{E0574C}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,calc}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepgfplotslibrary{fillbetween}
\pgfplotsset{otWeb/.style={
  trig format plots=rad,
  axis lines=middle,
  axis line style={otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}},
  tick style={otMuted,line width=0.5pt}, major tick length=3pt,
  ticklabel style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,fill=white,inner sep=1pt},
  grid=major, grid style={otRule!75,line width=0.35pt},
  xlabel={$x$}, ylabel={$y$},
  every axis x label/.style={at={(current axis.right of origin)},anchor=west,font=\normalsize,text=otMuted},
  every axis y label/.style={at={(current axis.above origin)},anchor=south,font=\normalsize,text=otMuted},
  clip=false, scale only axis, axis on top=false,
  yticklabel style={anchor=south east,inner sep=1.2pt,xshift=-1pt,yshift=1pt},
  xticklabel style={anchor=north,yshift=-2.5pt},
  samples=240,
}}
\tikzset{
  courbe/.style={otNavy,line width=1.35pt},
  courbe2/.style={otGreen,line width=1.35pt},
  pale/.style={otNavy!35,line width=1.1pt},
  seuil/.style={otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt},
  asymptote/.style={otRed!85,line width=0.75pt,dash pattern=on 4pt off 2.5pt},
  guide/.style={otMuted,line width=0.5pt,dash pattern=on 2pt off 1.6pt},
  etiq/.style={fill=white,inner sep=1.4pt,font=\normalsize},
  note/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted,fill=white,inner sep=1.2pt},
}
% points : plein, vide ; solution sur l'axe des abscisses
\newcommand{\pnt}[3][otNavy]{\fill[#1] (axis cs:#2,#3) circle (2.1pt);}
\newcommand{\pntv}[3][otNavy]{\draw[#1,fill=white,line width=0.9pt] (axis cs:#2,#3) circle (2.3pt);}
\newcommand{\guides}[2]{\draw[guide] (axis cs:#1,0) -- (axis cs:#1,#2) -- (axis cs:0,#2);}
\newcommand{\guidev}[2]{\draw[guide] (axis cs:#1,0) -- (axis cs:#1,#2);}
\newcommand{\sol}[2]{\draw[otGreen,line width=3pt,line cap=butt,opacity=0.9] (axis cs:#1,0) -- (axis cs:#2,0);}
\newcommand{\borneF}[1]{\fill[otGreenDark] (axis cs:#1,0) circle (2.5pt);}
\newcommand{\borneO}[1]{\draw[otGreenDark,fill=white,line width=1pt] (axis cs:#1,0) circle (2.5pt);}
\begin{document}
"""

PI = "3.14159"
X_2PI = r"xtick={1.5708,3.1416,4.7124,6.2832}, xticklabels={$\frac{\pi}{2}$,$\pi$,$\frac{3\pi}{2}$,$2\pi$}"

FIGURES = {
# ---------------------------------------------------------------- cours
"cours_courbes": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=8cm, height=2.88cm, xmin=-6.9, xmax=7.3, ymin=-1.55, ymax=1.95,
  xtick={-6.2832,-3.1416,3.1416,6.2832}, xticklabels={$-2\pi$,$-\pi$,$\pi$,$2\pi$},
  minor xtick={-4.7124,-1.5708,1.5708,4.7124}, minor grid style={otRule!45,line width=0.3pt}, minor tick length=0pt,
  ytick={-1,1}]
  \addplot[courbe2, domain=-6.9:7.1] {cos(x)};
  \addplot[courbe, domain=-6.9:7.1] {sin(x)};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:1.5708,1.12) {$y=\sin x$};
  \node[etiq,text=otGreenDark,anchor=south] at (axis cs:-3.1416,1.12) {$y=\cos x$};
  \draw[otMuted,line width=0.6pt,{Stealth[length=1.8mm]}-{Stealth[length=1.8mm]}] (axis cs:0,-1.32) -- (axis cs:6.2832,-1.32)
    node[note,midway] {période $2\pi$};
\end{axis}
\end{tikzpicture}""",

"cours_derivees": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.2cm, xmin=-1.9, xmax=5.0, ymin=-1.5, ymax=1.75,
  xtick={-1.5708,1.5708,3.1416,4.7124}, xticklabels={$-\frac{\pi}{2}$,$\frac{\pi}{2}$,$\pi$,$\frac{3\pi}{2}$}, ytick={-1,1}]
  \addplot[otGreen,line width=1.1pt,dash pattern=on 4pt off 2.5pt, domain=-1.9:4.9] {cos(x)};
  \addplot[courbe, domain=-1.9:4.9] {sin(x)};
  \draw[otOrange,line width=1.1pt] (axis cs:-0.75,-0.75) -- (axis cs:0.75,0.75);
  \draw[otOrange,line width=1.1pt] (axis cs:0.8,1) -- (axis cs:2.34,1);
  \draw[otOrange,line width=1.1pt] (axis cs:2.39,0.75) -- (axis cs:3.89,-0.75);
  \pnt{0}{0} \pnt{1.5708}{1} \pnt{3.1416}{0}
  \pnt[otGreenDark]{0}{1} \pnt[otGreenDark]{1.5708}{0} \pnt[otGreenDark]{3.1416}{-1}
  \node[note,anchor=north west] at (axis cs:0.12,-0.12) {pente $1$};
  \node[note,anchor=south] at (axis cs:1.5708,1.08) {pente $0$};
  \node[note,anchor=south west] at (axis cs:3.25,0.05) {pente $-1$};
  \node[etiq,text=otNavy,anchor=west] at (axis cs:3.6,-1.18) {$y=\sin x$};
  \node[etiq,text=otGreenDark,anchor=east] at (axis cs:-0.15,1.32) {$y=\cos x=(\sin x)'$};
\end{axis}
\end{tikzpicture}""",

"cours_etude_sin2x": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=2.88cm, xmin=-3.4, xmax=3.7, ymin=-1.55, ymax=1.6,
  xtick={-3.1416,-1.5708,0.7854,1.5708,2.3562,3.1416},
  xticklabels={$-\pi$,$-\frac{\pi}{2}$,$\frac{\pi}{4}$,$\frac{\pi}{2}$,$\frac{3\pi}{4}$,$\pi$}, ytick={-1,1}]
  \addplot[pale, domain=-3.3:0] {sin(2*x)};
  \addplot[pale, domain=3.1416:3.5] {sin(2*x)};
  \addplot[courbe, domain=0:3.1416] {sin(2*x)};
  \guides{0.7854}{1} \guidev{2.3562}{-1}
  \pnt{0.7854}{1} \pnt{2.3562}{-1}
  \node[note,anchor=south] at (axis cs:0.7854,1.07) {maximum $1$};
  \node[note,anchor=north] at (axis cs:2.3562,-1.07) {minimum $-1$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:-1.7,0.95) {$y=\sin(2x)$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------- exercice « Étude de fonctions »
"etude_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.52cm, xmin=-0.3, xmax=6.9, ymin=-1.85, ymax=1.9,
  xtick={0.7854,3.1416,3.927,6.2832}, xticklabels={$\frac{\pi}{4}$,$\pi$,$\frac{5\pi}{4}$,$2\pi$}, ytick={-1,1}]
  \addplot[courbe, domain=0:6.2832] {sin(x)+cos(x)};
  \guides{0.7854}{1.4142} \guides{3.927}{-1.4142}
  \pnt{0.7854}{1.4142} \pnt{3.927}{-1.4142} \pnt{0}{1} \pnt{6.2832}{1}
  \node[etiq,anchor=east,text=otMuted] at (axis cs:-0.05,1.4142) {$\sqrt2$};
  \node[etiq,anchor=east,text=otMuted] at (axis cs:-0.05,-1.4142) {$-\sqrt2$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:4.75,-1.15) {$y=\sin x+\cos x$};
\end{axis}
\end{tikzpicture}""",

"etude_g": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=2.88cm, xmin=-0.3, xmax=6.9, ymin=-1.5, ymax=1.9, """ + X_2PI + r""", ytick={-1,1}]
  \addplot[courbe, domain=0:6.2832] {-cos(2*x)};
  \pnt{1.5708}{1} \pnt{4.7124}{1} \pnt{0}{-1} \pnt{3.1416}{-1} \pnt{6.2832}{-1}
  \node[etiq,text=otNavy,anchor=south] at (axis cs:3.1416,1.12) {$y=\sin^2 x-\cos^2 x=-\cos(2x)$};
\end{axis}
\end{tikzpicture}""",

"etude_h": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4.16cm, xmin=-0.3, xmax=6.9, ymin=-5.2, ymax=5.4, """ + X_2PI + r""", ytick={-4,-2,2,4}]
  \addplot[courbe, domain=0:2.745] {sin(x)/(1+cos(x))};
  \addplot[courbe, domain=3.538:6.2832] {sin(x)/(1+cos(x))};
  \draw[asymptote] (axis cs:3.1416,-5.2) -- (axis cs:3.1416,5.2);
  \node[note,anchor=south west] at (axis cs:3.2,4.3) {asymptote $x=\pi$};
  \pnt{0}{0} \pntv{6.2832}{0}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:0.35,4.6) {$y=\dfrac{\sin x}{1+\cos x}$};
\end{axis}
\end{tikzpicture}""",

"etude_k": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=2.72cm, xmin=-0.3, xmax=6.9, ymin=-0.85, ymax=0.95, """ + X_2PI + r""",
  ytick={-0.5,0.5}, yticklabels={$-\dfrac12$,$\dfrac12$}]
  \addplot[courbe, domain=0:6.2832] {sin(x)*cos(x)};
  \pnt{0.7854}{0.5} \pnt{3.927}{0.5} \pnt{2.3562}{-0.5} \pnt{5.4978}{-0.5}
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:4.3,0.55) {$y=\sin x\cos x$};
\end{axis}
\end{tikzpicture}""",

"etude_m": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.2cm, height=4cm, xmin=-0.15, xmax=1.85, ymin=-0.4, ymax=4.4,
  xtick={0.7854,1.5708}, xticklabels={$\frac{\pi}{4}$,$\frac{\pi}{2}$}, ytick={1,2,3,4}]
  \addplot[courbe, domain=0:1.384] {tan(x)-x};
  \draw[asymptote] (axis cs:1.5708,-0.3) -- (axis cs:1.5708,4.3);
  \node[note,anchor=north west] at (axis cs:1.6,4.3) {$x=\frac{\pi}{2}$};
  \pnt{0}{0}
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.25,2.6) {$y=\tan x-x$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------- exercice « Applications avancées »
"appli_sin3x": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=2.88cm, xmin=-0.3, xmax=6.9, ymin=-1.5, ymax=1.65, """ + X_2PI + r""", ytick={-1,1}]
  \addplot[courbe2, domain=0:6.2832] {sin(3*x)};
  \addplot[courbe, domain=0:6.2832] {sin(x)};
  \pnt[otRed]{0}{0} \pnt[otRed]{0.7854}{0.7071} \pnt[otRed]{2.3562}{0.7071} \pnt[otRed]{3.1416}{0} \pnt[otRed]{3.927}{-0.7071} \pnt[otRed]{5.4978}{-0.7071} \pnt[otRed]{6.2832}{0}
  \node[etiq,text=otNavy,anchor=south] at (axis cs:1.5708,1.02) {$y=\sin x$};
  \node[etiq,text=otGreenDark,anchor=north] at (axis cs:4.7124,1.45) {$y=\sin(3x)$};
\end{axis}
\end{tikzpicture}""",

"appli_f": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4cm, xmin=-0.3, xmax=6.9, ymin=-5.3, ymax=1.3, """ + X_2PI + r""",
  ytick={-4,-2,0.5}, yticklabels={$-4$,$-2$,$\dfrac12$}]
  \addplot[courbe, domain=0:4.1267] {sin(x)/(1+sin(x))};
  \addplot[courbe, domain=5.2981:6.2832] {sin(x)/(1+sin(x))};
  \draw[asymptote] (axis cs:4.7124,-5.3) -- (axis cs:4.7124,1.2);
  \node[note,anchor=north east] at (axis cs:4.65,-4.4) {asymptote $x=\frac{3\pi}{2}$};
  \guides{1.5708}{0.5}
  \pnt{1.5708}{0.5} \pnt{0}{0} \pnt{6.2832}{0}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:0.4,-1.6) {$y=\dfrac{\sin x}{1+\sin x}$};
\end{axis}
\end{tikzpicture}""",

"appli_cos2x": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=2.88cm, xmin=-0.3, xmax=6.9, ymin=-1.5, ymax=1.65,
  xtick={0.5236,2.618,3.6652,5.7596,6.2832}, xticklabels={$\frac{\pi}{6}$,$\frac{5\pi}{6}$,$\frac{7\pi}{6}$,$\frac{11\pi}{6}$,$2\pi$},
  ytick={-1,0.5}, yticklabels={$-1$,$\dfrac12$}]
  \addplot[courbe, domain=0:6.2832, name path=c] {cos(2*x)};
  \path[name path=s] (axis cs:0,0.5) -- (axis cs:6.2832,0.5);
  \addplot[otGreen!30] fill between[of=c and s, soft clip={domain=0:0.5236}];
  \addplot[otGreen!30] fill between[of=c and s, soft clip={domain=2.618:3.6652}];
  \addplot[otGreen!30] fill between[of=c and s, soft clip={domain=5.7596:6.2832}];
  \draw[seuil] (axis cs:0,0.5) -- (axis cs:6.6,0.5);
  \sol{0}{0.5236} \sol{2.618}{3.6652} \sol{5.7596}{6.2832}
  \borneF{0} \borneF{0.5236} \borneF{2.618} \borneF{3.6652} \borneF{5.7596} \borneF{6.2832}
  \node[etiq,text=otNavy,anchor=north] at (axis cs:1.5708,-1.05) {$y=\cos(2x)$};
\end{axis}
\end{tikzpicture}""",

"appli_tan2x": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4cm, xmin=-0.15, xmax=3.5, ymin=-4.3, ymax=4.5,
  xtick={0.5236,0.7854,2.0944,2.3562,3.1416}, xticklabels={$\frac{\pi}{6}$,$\frac{\pi}{4}$,$\frac{2\pi}{3}$,$\frac{3\pi}{4}$,$\pi$},
  ytick={-2,1.7321,4}, yticklabels={$-2$,$\sqrt3$,$4$}]
  \addplot[courbe, domain=0:0.6629] {tan(2*x)};
  \addplot[courbe, domain=0.9079:2.2337] {tan(2*x)};
  \addplot[courbe, domain=2.4787:3.1416] {tan(2*x)};
  \draw[asymptote] (axis cs:0.7854,-4.3) -- (axis cs:0.7854,4.4);
  \draw[asymptote] (axis cs:2.3562,-4.3) -- (axis cs:2.3562,4.4);
  \draw[seuil] (axis cs:0,1.7321) -- (axis cs:3.3,1.7321);
  \guidev{0.5236}{1.7321} \guidev{2.0944}{1.7321}
  \pnt[otRed]{0.5236}{1.7321} \pnt[otRed]{2.0944}{1.7321}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:1.15,-2.7) {$y=\tan(2x)$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------- exercice « Limites et continuité »
"lim_sinx_x": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=2.88cm, xmin=-9.9, xmax=10.3, ymin=-0.45, ymax=1.35,
  xtick={-6.2832,-3.1416,3.1416,6.2832}, xticklabels={$-2\pi$,$-\pi$,$\pi$,$2\pi$}, ytick={1}]
  \addplot[courbe, domain=-9.6:-0.01] {sin(x)/x};
  \addplot[courbe, domain=0.01:9.6] {sin(x)/x};
  \pntv{0}{1}
  \node[note,anchor=south west] at (axis cs:0.25,1.03) {la limite en $0$ vaut $1$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:4.2,0.25) {$y=\dfrac{\sin x}{x}$};
\end{axis}
\end{tikzpicture}""",

"lim_1mcos": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=2.88cm, xmin=-6.9, xmax=7.3, ymin=-0.08, ymax=0.68,
  xtick={-6.2832,-3.1416,3.1416,6.2832}, xticklabels={$-2\pi$,$-\pi$,$\pi$,$2\pi$}, ytick={0.5}, yticklabels={$\dfrac12$}]
  \addplot[courbe, domain=-6.8:-0.01] {(1-cos(x))/x^2};
  \addplot[courbe, domain=0.01:6.8] {(1-cos(x))/x^2};
  \pntv{0}{0.5}
  \node[note,anchor=south west] at (axis cs:0.3,0.53) {la limite en $0$ vaut $\frac12$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:3.6,0.2) {$y=\dfrac{1-\cos x}{x^2}$};
\end{axis}
\end{tikzpicture}""",

"lim_tan": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=4cm, xmin=-0.15, xmax=3.55, ymin=-8.6, ymax=1.3,
  xtick={1.5708,3.1416}, xticklabels={$\frac{\pi}{2}$,$\pi$}, ytick={-8,-6,-4,-2},
  restrict y to domain=-9:2]
  \addplot[courbe, domain=0:1.37] {tan(x)/(x-1.5708)};
  \addplot[courbe, domain=1.7716:3.1416] {tan(x)/(x-1.5708)};
  \draw[asymptote] (axis cs:1.5708,-8.6) -- (axis cs:1.5708,1.2);
  \node[note,anchor=south west] at (axis cs:1.62,0.35) {$x=\frac{\pi}{2}$};
  \pnt{0}{0} \pnt{3.1416}{0}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.05,-5.2) {$y=\dfrac{\tan x}{x-\frac{\pi}{2}}$};
\end{axis}
\end{tikzpicture}""",

"lim_prolongement": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=2.88cm, xmin=-6.9, xmax=7.3, ymin=-0.4, ymax=1.35,
  xtick={-6.2832,-3.1416,3.1416,6.2832}, xticklabels={$-2\pi$,$-\pi$,$\pi$,$2\pi$}, ytick={1}]
  \addplot[courbe, domain=-6.8:6.8] {x==0 ? 1 : sin(x)/x};
  \pnt[otGreenDark]{0}{1}
  \node[note,anchor=south west] at (axis cs:0.3,1.03) {$\tilde f(0)=1$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:3.7,0.3) {$y=\tilde f(x)$};
\end{axis}
\end{tikzpicture}""",

"lim_gendarmes": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.04cm, xmin=-0.6, xmax=20.2, ymin=-0.85, ymax=1.15,
  xtick={6.2832,12.566,18.85}, xticklabels={$2\pi$,$4\pi$,$6\pi$}, ytick={-0.5,0.5}, yticklabels={$-\dfrac12$,$\dfrac12$}]
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=1.15:19.8] {1/x};
  \addplot[otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt, domain=1.15:19.8] {-1/x};
  \addplot[courbe, domain=0.05:19.8] {sin(x)/x};
  \node[note,anchor=south west,text=otOrange!70!black] at (axis cs:2.7,0.5) {$y=\frac{1}{x}$};
  \node[note,anchor=north west,text=otOrange!70!black] at (axis cs:2.2,-0.46) {$y=-\frac{1}{x}$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:12.9,0.3) {$y=\dfrac{\sin x}{x}$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------- exercice « Inéquations et optimisation »
"ineq_sin": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=2.88cm, xmin=-0.3, xmax=6.9, ymin=-1.5, ymax=1.65,
  xtick={1.0472,2.0944,3.1416,6.2832}, xticklabels={$\frac{\pi}{3}$,$\frac{2\pi}{3}$,$\pi$,$2\pi$},
  ytick={-1,0.866}, yticklabels={$-1$,$\dfrac{\sqrt3}{2}$}]
  \addplot[courbe, domain=0:6.2832, name path=c] {sin(x)};
  \path[name path=s] (axis cs:0,0.866) -- (axis cs:6.2832,0.866);
  \addplot[otGreen!30] fill between[of=c and s, soft clip={domain=1.0472:2.0944}];
  \draw[seuil] (axis cs:0,0.866) -- (axis cs:6.6,0.866);
  \sol{1.0472}{2.0944} \borneF{1.0472} \borneF{2.0944}
  \node[etiq,text=otNavy,anchor=north] at (axis cs:4.7124,-1.05) {$y=\sin x$};
\end{axis}
\end{tikzpicture}""",

"ineq_cos2x": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=2.88cm, xmin=-0.15, xmax=3.5, ymin=-1.5, ymax=1.65,
  xtick={0.5236,1.5708,2.618,3.1416}, xticklabels={$\frac{\pi}{6}$,$\frac{\pi}{2}$,$\frac{5\pi}{6}$,$\pi$},
  ytick={-1,0.5}, yticklabels={$-1$,$\dfrac12$}]
  \addplot[courbe, domain=0:3.1416, name path=c] {cos(2*x)};
  \path[name path=s] (axis cs:0,0.5) -- (axis cs:3.1416,0.5);
  \draw[seuil] (axis cs:0,0.5) -- (axis cs:3.35,0.5);
  \sol{0.5236}{2.618} \borneO{0.5236} \borneO{2.618}
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:2.75,0.95) {$y=\cos(2x)$};
\end{axis}
\end{tikzpicture}""",

"optim_max": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.52cm, xmin=-0.3, xmax=6.9, ymin=-1.85, ymax=1.95,
  xtick={0.7854,3.1416,3.927,6.2832}, xticklabels={$\frac{\pi}{4}$,$\pi$,$\frac{5\pi}{4}$,$2\pi$}, ytick={-1,1}]
  \addplot[courbe, domain=0:6.2832] {sin(x)+cos(x)};
  \guides{0.7854}{1.4142}
  \pnt[otGreenDark]{0.7854}{1.4142} \pnt{0}{1} \pnt{6.2832}{1} \pnt{3.927}{-1.4142}
  \node[etiq,anchor=east,text=otMuted] at (axis cs:-0.05,1.4142) {$\sqrt2$};
  \node[note,anchor=south west] at (axis cs:0.9,1.45) {maximum $\sqrt2$ en $\frac{\pi}{4}$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:4.75,-1.15) {$y=\sin x+\cos x$};
\end{axis}
\end{tikzpicture}""",

"ineq_tan": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=4cm, xmin=-0.3, xmax=6.9, ymin=-4.3, ymax=4.5,
  xtick={0.7854,1.5708,3.927,4.7124,6.2832}, xticklabels={$\frac{\pi}{4}$,$\frac{\pi}{2}$,$\frac{5\pi}{4}$,$\frac{3\pi}{2}$,$2\pi$},
  ytick={-2,1,4}, yticklabels={$-2$,$1$,$4$}]
  \addplot[courbe, domain=0:1.3258] {tan(x)};
  \addplot[courbe, domain=1.8158:4.4674] {tan(x)};
  \addplot[courbe, domain=4.9574:6.2832] {tan(x)};
  \draw[asymptote] (axis cs:1.5708,-4.3) -- (axis cs:1.5708,4.4);
  \draw[asymptote] (axis cs:4.7124,-4.3) -- (axis cs:4.7124,4.4);
  \draw[seuil] (axis cs:0,1) -- (axis cs:6.6,1);
  \sol{0}{0.7854} \sol{1.5708}{3.927} \sol{4.7124}{6.2832}
  \borneF{0} \borneF{0.7854} \borneO{1.5708} \borneF{3.927} \borneO{4.7124} \borneO{6.2832}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:2.15,-2.7) {$y=\tan x$};
\end{axis}
\end{tikzpicture}""",

"ineq_sinpcos": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.6cm, height=3.52cm, xmin=-0.3, xmax=6.9, ymin=-1.85, ymax=1.95, """ + X_2PI + r""", ytick={-1,1}]
  \addplot[courbe, domain=0:6.2832, name path=c] {sin(x)+cos(x)};
  \path[name path=s] (axis cs:0,1) -- (axis cs:6.2832,1);
  \addplot[otGreen!30] fill between[of=c and s, soft clip={domain=0:1.5708}];
  \draw[seuil] (axis cs:0,1) -- (axis cs:6.6,1);
  \sol{0}{1.5708} \borneF{0} \borneF{1.5708} \borneF{6.2832}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:4.75,-1.15) {$y=\sin x+\cos x$};
\end{axis}
\end{tikzpicture}""",
}


# Graduations de l'axe des abscisses placées à la main, du côté libre de la
# courbe : « g » sous l'axe à gauche du trait, « d » à droite, « c » centrée
# dessous, « h » au-dessus de l'axe. Leur fond blanc efface les asymptotes et
# les pointillés qui passent par la graduation, jamais une courbe.
P2, P3, P4, P6 = r"\frac{\pi}{2}", r"\frac{\pi}{3}", r"\frac{\pi}{4}", r"\frac{\pi}{6}"
XLAB = {
    "cours_courbes": [(-6.2832, "d", r"-2\pi"), (-3.1416, "g", r"-\pi"), (3.1416, "g", r"\pi"), (6.2832, "d", r"2\pi")],
    "cours_derivees": [(-1.5708, "d", "-" + P2), (1.5708, "g", P2), (3.1416, "g", r"\pi"), (4.7124, "d", r"\frac{3\pi}{2}")],
    "cours_etude_sin2x": [(-3.1416, "d", r"-\pi"), (-1.5708, "g", "-" + P2), (0.7854, "c", P4), (1.5708, "g", P2),
                          (2.3562, "h", r"\frac{3\pi}{4}"), (3.1416, "d", r"\pi")],
    "etude_f": [(0.7854, "c", P4), (3.1416, "c", r"\pi"), (3.927, "h", r"\frac{5\pi}{4}"), (6.2832, "c", r"2\pi")],
    "etude_g": [(1.5708, "c", P2), (3.1416, "c", r"\pi"), (4.7124, "c", r"\frac{3\pi}{2}"), (6.2832, "c", r"2\pi")],
    "etude_h": [(1.5708, "c", P2), (3.1416, "c", r"\pi"), (4.7124, "h", r"\frac{3\pi}{2}"), (6.2832, "d", r"2\pi")],
    "etude_k": [(1.5708, "g", P2), (3.1416, "d", r"\pi"), (4.7124, "g", r"\frac{3\pi}{2}"), (6.2832, "d", r"2\pi")],
    "etude_m": [(0.7854, "c", P4), (1.5708, "c", P2)],
    "appli_sin3x": [(1.5708, "c", P2), (3.1416, "g", r"\pi"), (4.7124, "c", r"\frac{3\pi}{2}"), (6.2832, "d", r"2\pi")],
    "appli_f": [(1.5708, "c", P2), (3.1416, "g", r"\pi"), (4.7124, "c", r"\frac{3\pi}{2}"), (6.2832, "d", r"2\pi")],
    "appli_cos2x": [(0.5236, "c", P6), (2.618, "c", r"\frac{5\pi}{6}"), (3.6652, "c", r"\frac{7\pi}{6}"),
                    (5.7596, "c", r"\frac{11\pi}{6}"), (6.2832, "d", r"2\pi")],
    "appli_tan2x": [(0.5236, "c", P6), (0.7854, "c", P4), (2.0944, "c", r"\frac{2\pi}{3}"), (2.3562, "c", r"\frac{3\pi}{4}"),
                    (3.1416, "d", r"\pi")],
    "lim_sinx_x": [(-6.2832, "g", r"-2\pi"), (-3.1416, "d", r"-\pi"), (3.1416, "g", r"\pi"), (6.2832, "d", r"2\pi")],
    "lim_1mcos": [(-6.2832, "c", r"-2\pi"), (-3.1416, "c", r"-\pi"), (3.1416, "c", r"\pi"), (6.2832, "c", r"2\pi")],
    "lim_tan": [(1.5708, "c", P2), (3.1416, "d", r"\pi")],
    "lim_prolongement": [(-6.2832, "g", r"-2\pi"), (-3.1416, "d", r"-\pi"), (3.1416, "g", r"\pi"), (6.2832, "d", r"2\pi")],
    "lim_gendarmes": [(6.2832, "d", r"2\pi"), (12.566, "d", r"4\pi"), (18.85, "d", r"6\pi")],
    "ineq_sin": [(1.0472, "c", P3), (2.0944, "c", r"\frac{2\pi}{3}"), (3.1416, "g", r"\pi"), (6.2832, "d", r"2\pi")],
    "ineq_cos2x": [(0.5236, "c", P6), (1.5708, "c", P2), (2.618, "c", r"\frac{5\pi}{6}"), (3.1416, "c", r"\pi")],
    "optim_max": [(0.7854, "c", P4), (3.1416, "c", r"\pi"), (3.927, "c", r"\frac{5\pi}{4}"), (6.2832, "c", r"2\pi")],
    "ineq_tan": [(0.7854, "c", P4), (1.5708, "c", P2), (3.927, "c", r"\frac{5\pi}{4}"), (4.7124, "c", r"\frac{3\pi}{2}"),
                 (6.2832, "d", r"2\pi")],
    "ineq_sinpcos": [(1.5708, "c", P2), (3.1416, "c", r"\pi"), (4.7124, "c", r"\frac{3\pi}{2}"), (6.2832, "c", r"2\pi")],
}
ANCRES = {"g": "north east", "d": "north west", "c": "north", "h": "south"}
DECALAGES = {"g": "xshift=-1.5pt,yshift=-2pt", "d": "xshift=1.5pt,yshift=-2pt", "c": "yshift=-2.5pt", "h": "yshift=2.5pt"}


def graduations_x(code, nom):
    """Remplace les étiquettes automatiques par des étiquettes placées."""
    if nom not in XLAB:
        return code
    code = re.sub(r"xticklabels=\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}", "xticklabels={}", code)
    nodes = "".join(
        f"  \\node[anchor={ANCRES[cote]},{DECALAGES[cote]},font=\\otRegular\\fontsize{{9}}{{10}}\\selectfont,"
        f"text=otMuted,fill=white,inner sep=1.3pt] at (axis cs:{x},0) {{$\\displaystyle {tex}$}};\n"
        for x, cote, tex in XLAB[nom]
    )
    return code.replace("\\end{axis}", nodes + "\\end{axis}")


def compiler(nom):
    BUILD.mkdir(exist_ok=True)
    SORTIE.mkdir(exist_ok=True)
    tex = BUILD / f"{nom}.tex"
    tex.write_text(PREAMBULE + graduations_x(FIGURES[nom], nom) + "\n\\end{document}\n", encoding="utf-8")
    r = subprocess.run(["lualatex", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                       cwd=BUILD, capture_output=True, text=True, encoding="utf-8", errors="replace")
    pdf = BUILD / f"{nom}.pdf"
    if r.returncode != 0 or not pdf.exists():
        log = (BUILD / f"{nom}.log").read_text(encoding="utf-8", errors="replace")
        erreurs = [l for l in log.splitlines() if l.startswith("!") or "Error" in l][:6]
        return False, erreurs
    subprocess.run(["pdftocairo", "-png", "-r", "240", "-singlefile", pdf.name, str(SORTIE / nom)],
                   cwd=BUILD, check=True)
    return True, []


if __name__ == "__main__":
    noms = sys.argv[1:] or list(FIGURES)
    ok = 0
    for nom in noms:
        bon, erreurs = compiler(nom)
        ok += bon
        print(("✓ " if bon else "✗ ") + nom + ("" if bon else " : " + " | ".join(erreurs)))
    print(f"{ok}/{len(noms)} figures produites dans {SORTIE}")
