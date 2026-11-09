# -*- coding: utf-8 -*-
"""Figure « Table trigonométrique » : cos, sin et tan d'un angle sur le cercle de rayon 1."""
from math import cos, radians, sin, tan

A = 35
R = 3.6
CX, SY, TY = R * cos(radians(A)), R * sin(radians(A)), R * tan(radians(A))

CERCLE = rf"""
\begin{{tikzpicture}}
  \draw[otMuted,line width=0.6pt,-{{Stealth[length=2.3mm]}}] (-0.3,0) -- ({R + 1.0},0);
  \draw[otMuted,line width=0.6pt,-{{Stealth[length=2.3mm]}}] (0,-0.3) -- (0,{R + 0.6});
  \draw[otNavy,line width=1.1pt] ({R},0) arc (0:90:{R});
  \draw[otRule,line width=0.7pt] ({R},-0.25) -- ({R},{TY + 0.5});
  \draw[otNavy!55,line width=0.8pt] (0,0) -- ({R},{TY:.4f});
  \draw[guide] ({CX:.4f},{SY:.4f}) -- (0,{SY:.4f});
  \draw[otGreenDark,line width=2.4pt,line cap=butt] (0,0) -- ({CX:.4f},0);
  \draw[otOrange!85!black,line width=2.4pt,line cap=butt] ({CX:.4f},0) -- ({CX:.4f},{SY:.4f});
  \draw[otRed,line width=2.4pt,line cap=butt] ({R},0) -- ({R},{TY:.4f});
  \fill[otNavy] ({CX:.4f},{SY:.4f}) circle (2.4pt);
  \draw[otNavy,line width=0.7pt] (0.75,0) arc (0:{A}:0.75);
  \node[text=otNavy] at ({A / 2}:1.08) {{$\alpha$}};
  \node[anchor=north,text=otGreenDark,inner sep=2pt] at ({CX / 2:.4f},-0.08) {{$\cos\alpha$}};
  \node[anchor=east,text=otOrange!75!black,inner sep=2pt] at ({CX - 0.06:.4f},{SY / 2:.4f}) {{$\sin\alpha$}};
  \node[anchor=west,text=otRed,inner sep=2pt] at ({R + 0.08},{TY / 2:.4f}) {{$\tan\alpha$}};
  \node[anchor=north east,inner sep=2pt] at (0,0) {{$O$}};
  \node[anchor=north,inner sep=2pt] at ({R + 0.18},-0.05) {{$1$}};\end{{tikzpicture}}"""

FIGURES = {"cercle_cos_sin_tan": CERCLE}
