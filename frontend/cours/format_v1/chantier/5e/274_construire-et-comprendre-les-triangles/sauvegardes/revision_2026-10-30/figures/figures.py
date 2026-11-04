# -*- coding: utf-8 -*-
"""Schémas de travail mutualisés, sans échelle numérique."""
FIGURES = {
'cours_angles': r"""

\begin{tikzpicture}
\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at (2.9408174517711623,2.0591825482288373);
\draw[geoTrait] (A)--(B)--(C)--cycle;\node[anchor=north east,text=otInk,inner sep=3pt] at (0,0) {$ A $};
\node[anchor=north west,text=otInk,inner sep=3pt] at (5,0) {$ B $};
\node[anchor=south,text=otInk,inner sep=3pt] at (2.9408174517711623,2.0591825482288373) {$ C $};
\draw[otOrange] (.7,0) arc[start angle=0,end angle=35,radius=.7];\draw[otOrange] (4.3,0) arc[start angle=180,end angle=135,radius=.7];\node[anchor=south west,text=otOrange,inner sep=3pt] at (1.0,0.12) {$ 35^\circ $};
\node[anchor=south east,text=otOrange,inner sep=3pt] at (4,0.12) {$ 45^\circ $};
\node[anchor=north,text=otInk,inner sep=3pt] at (2.5,-0.35) {$ 5\text{ cm} $};
\node[anchor=south,text=otGreenDark,inner sep=3pt] at (2.9408174517711623,2.459182548228837) {$ 180^\circ-35^\circ-45^\circ=100^\circ $};

\end{tikzpicture}

""",
'triangle_schema': r"""

\begin{tikzpicture}
\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at (2.9408174517711623,2.0591825482288373);
\draw[geoTrait] (A)--(B)--(C)--cycle;\node[anchor=north east,text=otInk,inner sep=3pt] at (0,0) {$ A $};
\node[anchor=north west,text=otInk,inner sep=3pt] at (5,0) {$ B $};
\node[anchor=south,text=otInk,inner sep=3pt] at (2.9408174517711623,2.0591825482288373) {$ C $};
\draw[otOrange] (.7,0) arc[start angle=0,end angle=35,radius=.7];\draw[otOrange] (4.3,0) arc[start angle=180,end angle=135,radius=.7];



\end{tikzpicture}

""",
'aire_schema': r"""

\begin{tikzpicture}
\coordinate(B) at (0,0);\coordinate(C) at (6,0);\coordinate(A) at (2,2.6);\coordinate(H) at (2,0);\coordinate(M) at (3,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoAide] (A)--(H);\draw[geoReponse] (A)--(M);\angledroit{A}{H}{C}\codage{B}{M}\codage{M}{C}\node[anchor=north east,text=otInk,inner sep=3pt] at (0,0) {$ B $};
\node[anchor=north west,text=otInk,inner sep=3pt] at (6,0) {$ C $};
\node[anchor=south,text=otInk,inner sep=3pt] at (2,2.6) {$ A $};
\node[anchor=north,text=otInk,inner sep=3pt] at (2,0) {$ H $};
\node[anchor=north,text=otInk,inner sep=3pt] at (3,0) {$ M $};



\end{tikzpicture}

""",
}
