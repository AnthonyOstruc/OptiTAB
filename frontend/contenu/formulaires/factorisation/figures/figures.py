# -*- coding: utf-8 -*-
"""Figures de « Factorisation » : facteur commun et différence de deux carrés (aires)."""

FACTEUR = r"""
\begin{tikzpicture}
  \coordinate (O) at (0,0); \coordinate (A) at (2.8,0); \coordinate (B) at (4.6,0);
  \coordinate (K) at (0,1.5); \coordinate (KA) at (2.8,1.5); \coordinate (KB) at (4.6,1.5);
  \fill[otSky] (O) rectangle (KA);
  \fill[otGreen!22] (A) rectangle (KB);
  \draw[geoTrait] (O) rectangle (KB);
  \draw[geoTrait] (A) -- (KA);
  \node[text=otNavy] at (1.4,0.75) {\large $ka$};
  \node[text=otGreenDark] at (3.7,0.75) {\large $kb$};
  \cote[0.32]{K}{KA}{$a$}
  \cote[0.32]{KA}{KB}{$b$}
  \cote[0.32]{O}{K}{$k$}
  \cote[0.32]{B}{O}{$a + b$}
\end{tikzpicture}"""

A, B = 2.6, 1.0
D = A - B
DIFF = rf"""
\begin{{tikzpicture}}
  % carré a² privé du carré b² (coin en haut à droite)
  \fill[otSky] (0,0) rectangle ({A},{D});
  \fill[otGreen!22] (0,{D}) rectangle ({D},{A});
  \draw[otMuted,line width=0.6pt,dash pattern=on 3pt off 2pt] ({D},{D}) rectangle ({A},{A});
  \draw[geoTrait] (0,0) -- ({A},0) -- ({A},{D}) -- ({D},{D}) -- ({D},{A}) -- (0,{A}) -- cycle;
  \draw[geoTrait] (0,{D}) -- ({D},{D});
  \node[text=otMuted] at ({(A + D) / 2},{(A + D) / 2}) {{$b^2$}};
  \coordinate (P) at (0,0); \coordinate (Q) at ({A},0); \coordinate (R) at (0,{A});
  \coordinate (S) at ({D},{A}); \coordinate (T) at ({A},{A});
  \cote[0.32]{{Q}}{{P}}{{$a$}}
  \cote[0.32]{{P}}{{R}}{{$a$}}
  \cote[0.32]{{S}}{{T}}{{$b$}}
  % flèche
  \draw[otGreenDark,line width=1pt,-{{Stealth[length=2.6mm]}}] ({A + 0.4},{D / 2}) -- ({A + 1.2},{D / 2});
  % rectangle (a − b)(a + b)
  \begin{{scope}}[xshift={A + 2.5}cm]
    \fill[otSky] (0,0) rectangle ({A},{D});
    \fill[otGreen!22] ({A},0) rectangle ({A + B},{D});
    \draw[geoTrait] (0,0) rectangle ({A + B},{D});
    \draw[geoTrait] ({A},0) -- ({A},{D});
    \coordinate (P2) at (0,0); \coordinate (Q2) at ({A + B},0); \coordinate (R2) at (0,{D});
    \cote[0.32]{{Q2}}{{P2}}{{$a + b$}}
    \cote[0.62]{{P2}}{{R2}}{{$a - b$}}
  \end{{scope}}
\end{{tikzpicture}}"""

FIGURES = {"facteur_commun": FACTEUR, "difference_carres": DIFF}
