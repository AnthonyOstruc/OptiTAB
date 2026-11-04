# -*- coding: utf-8 -*-
"""Figures exactes de la révision du 30 octobre 2026."""
FIGURES={
'cours_repere': r"""


\begin{tikzpicture}
\begin{scope}[x=0.58cm,y=0.58cm]
\draw[otRule,line width=.25pt,step=1] (-3,-3) grid (4,4);
\draw[geoVecteur] (-3,0)--(4.4,0);\draw[geoVecteur] (0,-3)--(0,4.5);
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=south,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=east,font=\small] at (0,4) {$ 4 $};
\node[anchor=north east,text=otInk,inner sep=3pt] at (0,0) {$ O $};
\draw[geoAide] (3,0)--(3,-2)--(0,-2);\fill[otNavy] (3,-2) circle (2pt);\node[anchor=south west,text=otInk,inner sep=3pt] at (3,-2) {$ A $};
\node[anchor=south west,text=otInk,inner sep=3pt] at (-2,3) {$ B $};
\fill[otGreenDark] (-2,3) circle (2pt);
\end{scope}
\end{tikzpicture}


""",
'r30_points_axes_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-4,-3) grid (5,3);\draw[geoVecteur] (-4,0)--(5.35,0);\draw[geoVecteur] (0,-3)--(0,3.35);
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (5,0) {$ 5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ 0 $};
\draw[geoAide] (-3,2)--(4,2);
\draw[geoAide] (4,0)--(4,2);
\fill[otNavy] (-3,2) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-3,2) {$ A $};
\fill[otNavy] (0,-2) circle (2pt);
\node[anchor=east,text=otNavy,inner sep=4pt] at (0,-2) {$ B $};
\fill[otNavy] (4,0) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (4,0) {$ C $};
\fill[otGreenDark] (4,2) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (4,2) {$ D $};

\end{scope}
\end{tikzpicture}
""",
'r30_cuve_enonce': r"""
\begin{tikzpicture}
\begin{scope}[x=0.75cm,y=0.175cm]
\draw[otRule,line width=.3pt] (2,0)--(2,20);\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\draw[otRule,line width=.3pt] (4,0)--(4,20);\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\draw[otRule,line width=.3pt] (6,0)--(6,20);\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\draw[otRule,line width=.3pt] (8,0)--(8,20);\node[coteTexte,anchor=north,font=\small] at (8,0) {$ 8 $};
\draw[otRule,line width=.3pt] (0,5)--(8,5);\node[coteTexte,anchor=east,font=\small] at (0,5) {$ 5 $};
\draw[otRule,line width=.3pt] (0,10)--(8,10);\node[coteTexte,anchor=east,font=\small] at (0,10) {$ 10 $};
\draw[otRule,line width=.3pt] (0,15)--(8,15);\node[coteTexte,anchor=east,font=\small] at (0,15) {$ 15 $};
\draw[otRule,line width=.3pt] (0,20)--(8,20);\node[coteTexte,anchor=east,font=\small] at (0,20) {$ 20 $};
\draw[geoVecteur] (0,0)--(8.48,0);\draw[geoVecteur] (0,0)--(0,21.6);\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ 0 $};
\node[anchor=north,text=otInk,inner sep=4pt] at (4.0,-3.5999999999999996) {$ \text{Temps (min)} $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (0,22.0) {$ \text{Volume (L)} $};
\draw[otNavy,line width=1pt] (0,0)--(8,20);
\fill[otNavy] (0,0) circle (2pt);
\fill[otNavy] (8,20) circle (2pt);

\end{scope}
\end{tikzpicture}
""",
'r30_promenade_enonce': r"""
\begin{tikzpicture}
\begin{scope}[x=0.12cm,y=1.1666666666666667cm]
\draw[otRule,line width=.3pt] (10,0)--(10,3);\node[coteTexte,anchor=north,font=\small] at (10,0) {$ 10 $};
\draw[otRule,line width=.3pt] (20,0)--(20,3);\node[coteTexte,anchor=north,font=\small] at (20,0) {$ 20 $};
\draw[otRule,line width=.3pt] (30,0)--(30,3);\node[coteTexte,anchor=north,font=\small] at (30,0) {$ 30 $};
\draw[otRule,line width=.3pt] (40,0)--(40,3);\node[coteTexte,anchor=north,font=\small] at (40,0) {$ 40 $};
\draw[otRule,line width=.3pt] (50,0)--(50,3);\node[coteTexte,anchor=north,font=\small] at (50,0) {$ 50 $};
\draw[otRule,line width=.3pt] (0,1)--(50,1);\node[coteTexte,anchor=east,font=\small] at (0,1) {$ 1 $};
\draw[otRule,line width=.3pt] (0,2)--(50,2);\node[coteTexte,anchor=east,font=\small] at (0,2) {$ 2 $};
\draw[otRule,line width=.3pt] (0,3)--(50,3);\node[coteTexte,anchor=east,font=\small] at (0,3) {$ 3 $};
\draw[geoVecteur] (0,0)--(53.0,0);\draw[geoVecteur] (0,0)--(0,3.24);\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ 0 $};
\node[anchor=north,text=otInk,inner sep=4pt] at (25.0,-0.54) {$ \text{Temps (min)} $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (0,3.3000000000000003) {$ \text{Distance (km)} $};
\draw[otNavy,line width=1pt] (0,0)--(20,1)--(30,1)--(50,2.5);
\fill[otNavy] (0,0) circle (2pt);
\fill[otNavy] (20,1) circle (2pt);
\fill[otNavy] (30,1) circle (2pt);
\fill[otNavy] (50,2.5) circle (2pt);

\end{scope}
\end{tikzpicture}
""",
'r30_cuve_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=0.75cm,y=0.175cm]
\draw[otRule,line width=.3pt] (2,0)--(2,20);\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\draw[otRule,line width=.3pt] (4,0)--(4,20);\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\draw[otRule,line width=.3pt] (6,0)--(6,20);\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\draw[otRule,line width=.3pt] (8,0)--(8,20);\node[coteTexte,anchor=north,font=\small] at (8,0) {$ 8 $};
\draw[otRule,line width=.3pt] (0,5)--(8,5);\node[coteTexte,anchor=east,font=\small] at (0,5) {$ 5 $};
\draw[otRule,line width=.3pt] (0,10)--(8,10);\node[coteTexte,anchor=east,font=\small] at (0,10) {$ 10 $};
\draw[otRule,line width=.3pt] (0,15)--(8,15);\node[coteTexte,anchor=east,font=\small] at (0,15) {$ 15 $};
\draw[otRule,line width=.3pt] (0,20)--(8,20);\node[coteTexte,anchor=east,font=\small] at (0,20) {$ 20 $};
\draw[geoVecteur] (0,0)--(8.48,0);\draw[geoVecteur] (0,0)--(0,21.6);\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ 0 $};
\node[anchor=north,text=otInk,inner sep=4pt] at (4.0,-3.5999999999999996) {$ \text{Temps (min)} $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (0,22.0) {$ \text{Volume (L)} $};
\draw[otNavy,line width=1pt] (0,0)--(8,20);
\fill[otNavy] (0,0) circle (2pt);
\fill[otNavy] (8,20) circle (2pt);
\draw[geoAide] (4,0)--(4,10)--(0,10);\fill[otGreenDark] (4,10) circle (2.5pt);
\draw[geoAide] (6,0)--(6,15)--(0,15);\fill[otGreenDark] (6,15) circle (2.5pt);

\end{scope}
\end{tikzpicture}
""",
'r30_promenade_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=0.12cm,y=1.1666666666666667cm]
\draw[otRule,line width=.3pt] (10,0)--(10,3);\node[coteTexte,anchor=north,font=\small] at (10,0) {$ 10 $};
\draw[otRule,line width=.3pt] (20,0)--(20,3);\node[coteTexte,anchor=north,font=\small] at (20,0) {$ 20 $};
\draw[otRule,line width=.3pt] (30,0)--(30,3);\node[coteTexte,anchor=north,font=\small] at (30,0) {$ 30 $};
\draw[otRule,line width=.3pt] (40,0)--(40,3);\node[coteTexte,anchor=north,font=\small] at (40,0) {$ 40 $};
\draw[otRule,line width=.3pt] (50,0)--(50,3);\node[coteTexte,anchor=north,font=\small] at (50,0) {$ 50 $};
\draw[otRule,line width=.3pt] (0,1)--(50,1);\node[coteTexte,anchor=east,font=\small] at (0,1) {$ 1 $};
\draw[otRule,line width=.3pt] (0,2)--(50,2);\node[coteTexte,anchor=east,font=\small] at (0,2) {$ 2 $};
\draw[otRule,line width=.3pt] (0,3)--(50,3);\node[coteTexte,anchor=east,font=\small] at (0,3) {$ 3 $};
\draw[geoVecteur] (0,0)--(53.0,0);\draw[geoVecteur] (0,0)--(0,3.24);\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ 0 $};
\node[anchor=north,text=otInk,inner sep=4pt] at (25.0,-0.54) {$ \text{Temps (min)} $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (0,3.3000000000000003) {$ \text{Distance (km)} $};
\draw[otNavy,line width=1pt] (0,0)--(20,1)--(30,1)--(50,2.5);
\fill[otNavy] (0,0) circle (2pt);
\fill[otNavy] (20,1) circle (2pt);
\fill[otNavy] (30,1) circle (2pt);
\fill[otNavy] (50,2.5) circle (2pt);
\draw[geoAide] (20,0)--(20,1)--(0,1);\fill[otGreenDark] (20,1) circle (2.5pt);
\draw[geoAide] (30,0)--(30,1)--(0,1);\fill[otGreenDark] (30,1) circle (2.5pt);
\draw[geoAide] (50,0)--(50,2.5)--(0,2.5);\fill[otGreenDark] (50,2.5) circle (2.5pt);

\end{scope}
\end{tikzpicture}
""",
'r30_aires_carres_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=1.5cm,y=0.21875cm]
\draw[otRule,line width=.3pt] (1,0)--(1,16);\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\draw[otRule,line width=.3pt] (2,0)--(2,16);\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\draw[otRule,line width=.3pt] (3,0)--(3,16);\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\draw[otRule,line width=.3pt] (4,0)--(4,16);\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\draw[otRule,line width=.3pt] (0,4)--(4,4);\node[coteTexte,anchor=east,font=\small] at (0,4) {$ 4 $};
\draw[otRule,line width=.3pt] (0,8)--(4,8);\node[coteTexte,anchor=east,font=\small] at (0,8) {$ 8 $};
\draw[otRule,line width=.3pt] (0,12)--(4,12);\node[coteTexte,anchor=east,font=\small] at (0,12) {$ 12 $};
\draw[otRule,line width=.3pt] (0,16)--(4,16);\node[coteTexte,anchor=east,font=\small] at (0,16) {$ 16 $};
\draw[geoVecteur] (0,0)--(4.24,0);\draw[geoVecteur] (0,0)--(0,17.28);\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ 0 $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.0,-2.88) {$ \text{Côté (cm)} $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (0,17.6) {$ \text{Aire (cm}^2\text{)} $};
\fill[otGreenDark] (1,1) circle (2pt);
\fill[otGreenDark] (2,4) circle (2pt);
\fill[otGreenDark] (3,9) circle (2pt);
\fill[otGreenDark] (4,16) circle (2pt);

\end{scope}
\end{tikzpicture}
""",
'r30_tarifs_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=1.0cm,y=0.19444444444444445cm]
\draw[otRule,line width=.3pt] (1,0)--(1,18);\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\draw[otRule,line width=.3pt] (2,0)--(2,18);\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\draw[otRule,line width=.3pt] (3,0)--(3,18);\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\draw[otRule,line width=.3pt] (4,0)--(4,18);\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\draw[otRule,line width=.3pt] (5,0)--(5,18);\node[coteTexte,anchor=north,font=\small] at (5,0) {$ 5 $};
\draw[otRule,line width=.3pt] (6,0)--(6,18);\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\draw[otRule,line width=.3pt] (0,3)--(6,3);\node[coteTexte,anchor=east,font=\small] at (0,3) {$ 3 $};
\draw[otRule,line width=.3pt] (0,6)--(6,6);\node[coteTexte,anchor=east,font=\small] at (0,6) {$ 6 $};
\draw[otRule,line width=.3pt] (0,9)--(6,9);\node[coteTexte,anchor=east,font=\small] at (0,9) {$ 9 $};
\draw[otRule,line width=.3pt] (0,12)--(6,12);\node[coteTexte,anchor=east,font=\small] at (0,12) {$ 12 $};
\draw[otRule,line width=.3pt] (0,15)--(6,15);\node[coteTexte,anchor=east,font=\small] at (0,15) {$ 15 $};
\draw[otRule,line width=.3pt] (0,18)--(6,18);\node[coteTexte,anchor=east,font=\small] at (0,18) {$ 18 $};
\draw[geoVecteur] (0,0)--(6.36,0);\draw[geoVecteur] (0,0)--(0,19.44);\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ 0 $};
\node[anchor=north,text=otInk,inner sep=4pt] at (3.0,-3.2399999999999998) {$ \text{Nombre d’activités} $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (0,19.8) {$ \text{Prix (€) : A bleu, B orange} $};
\fill[otNavy] (0,0) circle (2pt);
\fill[otNavy] (1,3) circle (2pt);
\fill[otNavy] (2,6) circle (2pt);
\fill[otNavy] (3,9) circle (2pt);
\fill[otNavy] (4,12) circle (2pt);
\fill[otNavy] (5,15) circle (2pt);
\fill[otNavy] (6,18) circle (2pt);
\fill[otOrange] (0,4) circle (2pt);
\fill[otOrange] (1,6) circle (2pt);
\fill[otOrange] (2,8) circle (2pt);
\fill[otOrange] (3,10) circle (2pt);
\fill[otOrange] (4,12) circle (2pt);
\fill[otOrange] (5,14) circle (2pt);
\fill[otOrange] (6,16) circle (2pt);
\draw[geoAide] (4,0)--(4,12)--(0,12);\fill[otGreenDark] (4,12) circle (2.5pt);

\end{scope}
\end{tikzpicture}
""",
'r30_jardin_2_3': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-3,-4) grid (3,4);\draw[geoVecteur] (-3,0)--(3.35,0);\draw[geoVecteur] (0,-4)--(0,4.35);
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\draw[otNavy,line width=1pt] (-2,3)--(2,3)--(2,-3)--(-2,-3)--cycle;
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-2,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-2,3) {$ A $};
\fill[otNavy] (2,3) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (2,3) {$ B $};
\fill[otNavy] (2,-3) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (2,-3) {$ C $};
\fill[otNavy] (-2,-3) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-2,-3) {$ D $};

\end{scope}
\end{tikzpicture}
""",
'r30_jardin_8_3': r"""
\begin{tikzpicture}
\begin{scope}[x=0.3611111111111111cm,y=0.3611111111111111cm]
\draw[otRule,line width=.25pt,step=1] (-9,-4) grid (9,4);\draw[geoVecteur] (-9,0)--(9.35,0);\draw[geoVecteur] (0,-4)--(0,4.35);
\node[coteTexte,anchor=north,font=\small] at (-8,0) {$ -8 $};
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north,font=\small] at (8,0) {$ 8 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\draw[otNavy,line width=1pt] (-8,3)--(8,3)--(8,-3)--(-8,-3)--cycle;
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-8,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-8,3) {$ A $};
\fill[otNavy] (8,3) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (8,3) {$ B $};
\fill[otNavy] (8,-3) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (8,-3) {$ C $};
\fill[otNavy] (-8,-3) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-8,-3) {$ D $};

\end{scope}
\end{tikzpicture}
""",
'r30_jardin_3_4': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-4,-5) grid (4,5);\draw[geoVecteur] (-4,0)--(4.35,0);\draw[geoVecteur] (0,-5)--(0,5.35);
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-5) {$ -5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,5) {$ 5 $};
\draw[otNavy,line width=1pt] (-3,4)--(3,4)--(3,-4)--(-3,-4)--cycle;
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-3,4) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-3,4) {$ A $};
\fill[otNavy] (3,4) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (3,4) {$ B $};
\fill[otNavy] (3,-4) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (3,-4) {$ C $};
\fill[otNavy] (-3,-4) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-3,-4) {$ D $};

\end{scope}
\end{tikzpicture}
""",
'r30_jardin_5_4': r"""
\begin{tikzpicture}
\begin{scope}[x=0.5416666666666666cm,y=0.5416666666666666cm]
\draw[otRule,line width=.25pt,step=1] (-6,-5) grid (6,5);\draw[geoVecteur] (-6,0)--(6.35,0);\draw[geoVecteur] (0,-5)--(0,5.35);
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-5,0) {$ -5 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (5,0) {$ 5 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-5) {$ -5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,5) {$ 5 $};
\draw[otNavy,line width=1pt] (-5,4)--(5,4)--(5,-4)--(-5,-4)--cycle;
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-5,4) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-5,4) {$ A $};
\fill[otNavy] (5,4) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (5,4) {$ B $};
\fill[otNavy] (5,-4) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (5,-4) {$ C $};
\fill[otNavy] (-5,-4) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-5,-4) {$ D $};

\end{scope}
\end{tikzpicture}
""",
'r30_jardin_7_4': r"""
\begin{tikzpicture}
\begin{scope}[x=0.40625cm,y=0.40625cm]
\draw[otRule,line width=.25pt,step=1] (-8,-5) grid (8,5);\draw[geoVecteur] (-8,0)--(8.35,0);\draw[geoVecteur] (0,-5)--(0,5.35);
\node[coteTexte,anchor=north,font=\small] at (-8,0) {$ -8 $};
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north,font=\small] at (8,0) {$ 8 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\draw[otNavy,line width=1pt] (-7,4)--(7,4)--(7,-4)--(-7,-4)--cycle;
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-7,4) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-7,4) {$ A $};
\fill[otNavy] (7,4) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (7,4) {$ B $};
\fill[otNavy] (7,-4) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (7,-4) {$ C $};
\fill[otNavy] (-7,-4) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-7,-4) {$ D $};

\end{scope}
\end{tikzpicture}
""",
'r30_jardin_4_5': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-5,-6) grid (5,6);\draw[geoVecteur] (-5,0)--(5.35,0);\draw[geoVecteur] (0,-6)--(0,6.35);
\node[coteTexte,anchor=north,font=\small] at (-5,0) {$ -5 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (5,0) {$ 5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-6) {$ -6 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-5) {$ -5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,5) {$ 5 $};
\node[coteTexte,anchor=south east,font=\small] at (0,6) {$ 6 $};
\draw[otNavy,line width=1pt] (-4,5)--(4,5)--(4,-5)--(-4,-5)--cycle;
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-4,5) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-4,5) {$ A $};
\fill[otNavy] (4,5) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (4,5) {$ B $};
\fill[otNavy] (4,-5) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (4,-5) {$ C $};
\fill[otNavy] (-4,-5) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-4,-5) {$ D $};

\end{scope}
\end{tikzpicture}
""",
'r30_jardin_6_5': r"""
\begin{tikzpicture}
\begin{scope}[x=0.4642857142857143cm,y=0.4642857142857143cm]
\draw[otRule,line width=.25pt,step=1] (-7,-6) grid (7,6);\draw[geoVecteur] (-7,0)--(7.35,0);\draw[geoVecteur] (0,-6)--(0,6.35);
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-6) {$ -6 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-5) {$ -5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,5) {$ 5 $};
\node[coteTexte,anchor=south east,font=\small] at (0,6) {$ 6 $};
\draw[otNavy,line width=1pt] (-6,5)--(6,5)--(6,-5)--(-6,-5)--cycle;
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-6,5) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-6,5) {$ A $};
\fill[otNavy] (6,5) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (6,5) {$ B $};
\fill[otNavy] (6,-5) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (6,-5) {$ C $};
\fill[otNavy] (-6,-5) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-6,-5) {$ D $};

\end{scope}
\end{tikzpicture}
""",
}

# Dernière correction de lisibilité des graduations.
FIGURES.update({
'r30_jardin_2_3': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-3,-4) grid (3,4);\draw[geoVecteur] (-3,0)--(3.35,0);\draw[geoVecteur] (0,-4)--(0,4.35);
\draw[otNavy,line width=1pt] (-2,3)--(2,3)--(2,-3)--(-2,-3)--cycle;
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-2,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-2,3) {$ A $};
\fill[otNavy] (2,3) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (2,3) {$ B $};
\fill[otNavy] (2,-3) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (2,-3) {$ C $};
\fill[otNavy] (-2,-3) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-2,-3) {$ D $};

\end{scope}
\end{tikzpicture}""",
'r30_jardin_8_3': r"""
\begin{tikzpicture}
\begin{scope}[x=0.3611111111111111cm,y=0.3611111111111111cm]
\draw[otRule,line width=.25pt,step=1] (-9,-4) grid (9,4);\draw[geoVecteur] (-9,0)--(9.35,0);\draw[geoVecteur] (0,-4)--(0,4.35);
\draw[otNavy,line width=1pt] (-8,3)--(8,3)--(8,-3)--(-8,-3)--cycle;
\node[coteTexte,anchor=north,font=\small] at (-8,0) {$ -8 $};
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north,font=\small] at (8,0) {$ 8 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-8,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-8,3) {$ A $};
\fill[otNavy] (8,3) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (8,3) {$ B $};
\fill[otNavy] (8,-3) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (8,-3) {$ C $};
\fill[otNavy] (-8,-3) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-8,-3) {$ D $};

\end{scope}
\end{tikzpicture}""",
'r30_jardin_3_4': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-4,-5) grid (4,5);\draw[geoVecteur] (-4,0)--(4.35,0);\draw[geoVecteur] (0,-5)--(0,5.35);
\draw[otNavy,line width=1pt] (-3,4)--(3,4)--(3,-4)--(-3,-4)--cycle;
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-5) {$ -5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,5) {$ 5 $};
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-3,4) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-3,4) {$ A $};
\fill[otNavy] (3,4) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (3,4) {$ B $};
\fill[otNavy] (3,-4) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (3,-4) {$ C $};
\fill[otNavy] (-3,-4) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-3,-4) {$ D $};

\end{scope}
\end{tikzpicture}""",
'r30_jardin_5_4': r"""
\begin{tikzpicture}
\begin{scope}[x=0.5416666666666666cm,y=0.5416666666666666cm]
\draw[otRule,line width=.25pt,step=1] (-6,-5) grid (6,5);\draw[geoVecteur] (-6,0)--(6.35,0);\draw[geoVecteur] (0,-5)--(0,5.35);
\draw[otNavy,line width=1pt] (-5,4)--(5,4)--(5,-4)--(-5,-4)--cycle;
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-5,0) {$ -5 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (5,0) {$ 5 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-5) {$ -5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,5) {$ 5 $};
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-5,4) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-5,4) {$ A $};
\fill[otNavy] (5,4) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (5,4) {$ B $};
\fill[otNavy] (5,-4) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (5,-4) {$ C $};
\fill[otNavy] (-5,-4) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-5,-4) {$ D $};

\end{scope}
\end{tikzpicture}""",
'r30_jardin_4_5': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-5,-6) grid (5,6);\draw[geoVecteur] (-5,0)--(5.35,0);\draw[geoVecteur] (0,-6)--(0,6.35);
\draw[otNavy,line width=1pt] (-4,5)--(4,5)--(4,-5)--(-4,-5)--cycle;
\node[coteTexte,anchor=north,font=\small] at (-5,0) {$ -5 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (5,0) {$ 5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-6) {$ -6 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-5) {$ -5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,5) {$ 5 $};
\node[coteTexte,anchor=south east,font=\small] at (0,6) {$ 6 $};
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-4,5) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-4,5) {$ A $};
\fill[otNavy] (4,5) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (4,5) {$ B $};
\fill[otNavy] (4,-5) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (4,-5) {$ C $};
\fill[otNavy] (-4,-5) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-4,-5) {$ D $};

\end{scope}
\end{tikzpicture}""",
'r30_jardin_6_5': r"""
\begin{tikzpicture}
\begin{scope}[x=0.4642857142857143cm,y=0.4642857142857143cm]
\draw[otRule,line width=.25pt,step=1] (-7,-6) grid (7,6);\draw[geoVecteur] (-7,0)--(7.35,0);\draw[geoVecteur] (0,-6)--(0,6.35);
\draw[otNavy,line width=1pt] (-6,5)--(6,5)--(6,-5)--(-6,-5)--cycle;
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-6) {$ -6 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-5) {$ -5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,5) {$ 5 $};
\node[coteTexte,anchor=south east,font=\small] at (0,6) {$ 6 $};
\fill[otGreenDark] (0,0) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (-6,5) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-6,5) {$ A $};
\fill[otNavy] (6,5) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (6,5) {$ B $};
\fill[otNavy] (6,-5) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (6,-5) {$ C $};
\fill[otNavy] (-6,-5) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-6,-5) {$ D $};

\end{scope}
\end{tikzpicture}""",
})
