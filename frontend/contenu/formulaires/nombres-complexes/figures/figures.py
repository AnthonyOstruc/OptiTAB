# -*- coding: utf-8 -*-
"""Figures de « Nombres complexes » : plan complexe, racines sixièmes de l'unité."""
import math

# Repère à échelle égale (1 unité = 1,24 cm sur les deux axes) : l'arc de θ est juste.
PLAN = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.46cm, height=6.2cm, xmin=-0.8, xmax=3.6, ymin=-2.4, ymax=2.6,
  xtick={2.6}, xticklabels={}, ytick={1.7}, yticklabels={$b$}, xlabel={}, ylabel={}]
  \draw[guide] (axis cs:2.6,0) -- (axis cs:2.6,1.7) -- (axis cs:0,1.7);
  \draw[otMuted,line width=0.6pt,dash pattern=on 3pt off 2pt] (axis cs:2.6,1.7) -- (axis cs:2.6,-1.7);
  \draw[otNavy,line width=1.2pt] (axis cs:0,0) -- (axis cs:2.6,1.7);
  \addplot[otOrange!85!black,line width=1pt,domain=0:33.18,samples=40,variable=\t] ({0.8*cos(\t)},{0.8*sin(\t)});
  \node[text=otOrange!75!black] at (axis cs:1.05,0.3) {$\theta$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:1.2,0.85) {$r$};
  \pnt{2.6}{1.7}
  \fill[otMuted] (axis cs:2.6,-1.7) circle (2.1pt);
  \node[anchor=west,text=otNavy] at (axis cs:2.7,1.85) {$M(z)$};
  \node[anchor=west,text=otMuted] at (axis cs:2.7,-1.85) {$M'(\overline{z})$};
  \node[anchor=north west,text=otMuted,font=\small] at (axis cs:3.25,-0.05) {Re};
  \node[anchor=south west,text=otMuted,font=\small] at (axis cs:0.05,2.4) {Im};
\end{axis}
\end{tikzpicture}"""

XLAB = {"plan_complexe": [(2.6, "d", r"a")]}

R = 1.7
NOMS = ["1", r"\mathrm{e}^{\mathrm{i}\pi/3}", r"\mathrm{e}^{2\mathrm{i}\pi/3}", "-1",
        r"\mathrm{e}^{4\mathrm{i}\pi/3}", r"\mathrm{e}^{5\mathrm{i}\pi/3}"]
ANCRES = ["north west", "south west", "south east", "north east", "north east", "north west"]


def racines():
    l = [r"\begin{tikzpicture}",
         rf"  \draw[otMuted,line width=0.6pt,-{{Stealth[length=2.3mm]}}] ({-R - 0.9},0) -- ({R + 0.9},0);",
         rf"  \draw[otMuted,line width=0.6pt,-{{Stealth[length=2.3mm]}}] (0,{-R - 0.6}) -- (0,{R + 0.6});",
         rf"  \draw[otRule,line width=0.8pt] (0,0) circle ({R});"]
    pts = [(R * math.cos(k * math.pi / 3), R * math.sin(k * math.pi / 3)) for k in range(6)]
    l.append(r"  \draw[otNavy,line width=1.1pt,fill=otSky,fill opacity=0.6] " +
             " -- ".join(f"({x:.4f},{y:.4f})" for x, y in pts) + " -- cycle;")
    for (x, y), nom, ancre in zip(pts, NOMS, ANCRES):
        l.append(rf"  \fill[otNavy] ({x:.4f},{y:.4f}) circle (2.2pt);")
        dx = 0.08 * (1 if 'west' in ancre else -1 if 'east' in ancre else 0)
        dy = 0.08 * (1 if 'south' in ancre else -1 if 'north' in ancre else 0)
        l.append(rf"  \node[anchor={ancre},text=otInk,fill=white,inner sep=1.2pt] at ({x + dx:.4f},{y + dy:.4f}) {{${nom}$}};")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


FIGURES = {"plan_complexe": PLAN, "racines_unite": racines()}
