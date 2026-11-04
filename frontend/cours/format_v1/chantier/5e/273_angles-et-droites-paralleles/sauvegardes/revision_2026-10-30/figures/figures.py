# -*- coding: utf-8 -*-
"""Schémas de travail mutualisés, sans échelle numérique."""
FIGURES = {
'rosace_schema': r"""

\begin{tikzpicture}
\coordinate(O) at (0,0);\coordinate(A) at (-3,0);\coordinate(B) at (3,0);
\coordinate(C) at (220:2.6);\coordinate(D) at (40:2.6);\coordinate(E) at (200.0:2.8);
\draw[geoTrait] (A)--(B) (C)--(D);\draw[geoAide] (O)--(E);\draw[otOrange,line width=.8pt] (-.8,0) arc[start angle=180,end angle=220,radius=.8];

\node[anchor=south east,text=otInk,inner sep=3pt] at (-3,0) {$ A $};
\node[anchor=south west,text=otInk,inner sep=3pt] at (3,0) {$ B $};
\node[anchor=south east,text=otInk,inner sep=3pt] at (0,0) {$ O $};
\node[anchor=north east,inner sep=4pt] at (C) {$C$};\node[anchor=south west,inner sep=4pt] at (D) {$D$};\node[anchor=north west,inner sep=4pt,text=otGreenDark] at (E) {$E$};

\end{tikzpicture}

""",
'rosace_schema_corrige': r"""

\begin{tikzpicture}
\coordinate(O) at (0,0);\coordinate(A) at (-3,0);\coordinate(B) at (3,0);
\coordinate(C) at (220:2.6);\coordinate(D) at (40:2.6);\coordinate(E) at (200.0:2.8);
\draw[geoTrait] (A)--(B) (C)--(D);\draw[geoAide] (O)--(E);\draw[otOrange,line width=.8pt] (-.8,0) arc[start angle=180,end angle=220,radius=.8];

\node[anchor=south east,text=otInk,inner sep=3pt] at (-3,0) {$ A $};
\node[anchor=south west,text=otInk,inner sep=3pt] at (3,0) {$ B $};
\node[anchor=south east,text=otInk,inner sep=3pt] at (0,0) {$ O $};
\node[anchor=north east,inner sep=4pt] at (C) {$C$};\node[anchor=south west,inner sep=4pt] at (D) {$D$};\node[anchor=north west,inner sep=4pt,text=otGreenDark] at (E) {$E$};
\draw[geoReponse] (.7,0) arc[start angle=0,end angle=40,radius=.7];
\end{tikzpicture}

""",
'paralleles_schema': r"""

\begin{tikzpicture}
\coordinate(A) at (1.0000000000000002,1);\coordinate(B) at (-1.0000000000000002,-1);
\draw[geoTrait] (-3.3,1)--(3.3,1) (-3.3,-1)--(3.3,-1);\draw[geoTrait] (-1.5000000000000004,-1.5)--(1.7000000000000002,1.7);
\node[anchor=south west,text=otInk,inner sep=3pt] at (-3.3,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=3pt] at (-3.3,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=3pt] at (1.0000000000000002,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=3pt] at (-1.0000000000000002,-1) {$ B $};
\draw[otOrange] (1.6,1) arc[start angle=0,end angle=45,radius=.6];\node[anchor=north west,text=otMuted] at (-3.3,-1.8) {$(d)\parallel(e)$};
\end{tikzpicture}

""",
'paralleles_schema_corrige': r"""

\begin{tikzpicture}
\coordinate(A) at (1.0000000000000002,1);\coordinate(B) at (-1.0000000000000002,-1);
\draw[geoTrait] (-3.3,1)--(3.3,1) (-3.3,-1)--(3.3,-1);\draw[geoTrait] (-1.5000000000000004,-1.5)--(1.7000000000000002,1.7);
\node[anchor=south west,text=otInk,inner sep=3pt] at (-3.3,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=3pt] at (-3.3,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=3pt] at (1.0000000000000002,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=3pt] at (-1.0000000000000002,-1) {$ B $};
\draw[otOrange] (1.6,1) arc[start angle=0,end angle=45,radius=.6];\node[anchor=north west,text=otMuted] at (-3.3,-1.8) {$(d)\parallel(e)$};\draw[geoReponse] (-0.40000000000000024,-1) arc[start angle=0,end angle=45,radius=.6];
\end{tikzpicture}

""",
}
