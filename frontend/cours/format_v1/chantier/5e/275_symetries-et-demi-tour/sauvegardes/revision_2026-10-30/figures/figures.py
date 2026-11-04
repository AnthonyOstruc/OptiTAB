# -*- coding: utf-8 -*-
"""Schémas de travail mutualisés, sans échelle numérique."""
FIGURES = {
'centrale_enonce': r"""

\begin{tikzpicture}
\begin{scope}[x=.6cm,y=.6cm]

\draw[geoVecteur] (-5,0)--(5.4,0);\draw[geoVecteur] (0,-4)--(0,4.5);


















\node[anchor=north east,text=otInk,inner sep=3pt] at (0,0) {$ O $};
\draw[geoTrait,fill=otSky] (2,1)--(4,1)--(2,3)--cycle;\node[anchor=north east,text=otInk,inner sep=3pt] at (2,1) {$ A $};
\node[anchor=south west,text=otInk,inner sep=3pt] at (4,1) {$ B $};
\node[anchor=south east,text=otInk,inner sep=3pt] at (2,3) {$ C $};
\end{scope}
\end{tikzpicture}

""",
'centrale_corrige': r"""

\begin{tikzpicture}
\begin{scope}[x=.6cm,y=.6cm]

\draw[geoVecteur] (-5,0)--(5.4,0);\draw[geoVecteur] (0,-4)--(0,4.5);


















\node[anchor=north east,text=otInk,inner sep=3pt] at (0,0) {$ O $};
\draw[geoTrait,fill=otSky] (2,1)--(4,1)--(2,3)--cycle;\node[anchor=north east,text=otInk,inner sep=3pt] at (2,1) {$ A $};
\node[anchor=south west,text=otInk,inner sep=3pt] at (4,1) {$ B $};
\node[anchor=south east,text=otInk,inner sep=3pt] at (2,3) {$ C $};
\draw[geoReponse,fill=otGreen!12] (-2,-1)--(-4,-1)--(-2,-3)--cycle;\node[anchor=south west,text=otGreenDark,inner sep=3pt] at (-2,-1) {$ A' $};
\node[anchor=south east,text=otGreenDark,inner sep=3pt] at (-4,-1) {$ B' $};
\node[anchor=north west,text=otGreenDark,inner sep=3pt] at (-2,-3) {$ C' $};
\end{scope}
\end{tikzpicture}

""",
'axiale_enonce': r"""

\begin{tikzpicture}
\begin{scope}[x=.6cm,y=.6cm]

\draw[geoVecteur] (-6,0)--(6.4,0);\draw[geoVecteur] (0,-.6)--(0,4.1);




















\node[anchor=north east,text=otInk,inner sep=3pt] at (0,0) {$ O $};
\draw[geoTrait,fill=otSky] (3,1)--(5,1)--(3,3)--cycle;\node[anchor=north east,text=otInk,inner sep=3pt] at (3,1) {$ A $};
\node[anchor=south west,text=otInk,inner sep=3pt] at (5,1) {$ B $};
\node[anchor=south east,text=otInk,inner sep=3pt] at (3,3) {$ C $};
\draw[otOrange,line width=1pt] (0,-.6)--(0,3.9);\end{scope}
\end{tikzpicture}

""",
'axiale_corrige': r"""

\begin{tikzpicture}
\begin{scope}[x=.6cm,y=.6cm]

\draw[geoVecteur] (-6,0)--(6.4,0);\draw[geoVecteur] (0,-.6)--(0,4.1);




















\node[anchor=north east,text=otInk,inner sep=3pt] at (0,0) {$ O $};
\draw[geoTrait,fill=otSky] (3,1)--(5,1)--(3,3)--cycle;\node[anchor=north east,text=otInk,inner sep=3pt] at (3,1) {$ A $};
\node[anchor=south west,text=otInk,inner sep=3pt] at (5,1) {$ B $};
\node[anchor=south east,text=otInk,inner sep=3pt] at (3,3) {$ C $};
\draw[otOrange,line width=1pt] (0,-.6)--(0,3.9);\draw[geoReponse,fill=otGreen!12] (-3,1)--(-5,1)--(-3,3)--cycle;\node[anchor=north west,text=otGreenDark,inner sep=3pt] at (-3,1) {$ A' $};
\node[anchor=south east,text=otGreenDark,inner sep=3pt] at (-5,1) {$ B' $};
\node[anchor=south west,text=otGreenDark,inner sep=3pt] at (-3,3) {$ C' $};
\end{scope}
\end{tikzpicture}

""",
}
