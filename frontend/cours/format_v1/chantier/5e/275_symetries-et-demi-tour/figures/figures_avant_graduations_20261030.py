# -*- coding: utf-8 -*-
"""Figures exactes de la révision du 30 octobre 2026."""
FIGURES={
'r30_centre_decale_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-3,-5) grid (5,3);\draw[geoVecteur] (-3,0)--(5.35,0);\draw[geoVecteur] (0,-5)--(0,3.35);
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (5,0) {$ 5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-5) {$ -5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\draw[geoAide] (3,2)--(-1,-4);
\draw[geoAide] (-2,0)--(4,-2);
\fill[otNavy] (3,2) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (3,2) {$ A $};
\fill[otNavy] (-2,0) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-2,0) {$ B $};
\fill[otOrange] (1,-1) circle (2pt);
\node[anchor=north west,text=otOrange,inner sep=4pt] at (1.2,-1.4) {$ S $};
\fill[otGreenDark] (-1,-4) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (-1,-4) {$ A' $};
\fill[otGreenDark] (4,-2) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (4,-2) {$ B' $};
\fill[otInk] (0,0) circle (2pt);
\node[anchor=south west,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otGreenDark] (2,-2) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (2,-2) {$ O' $};

\end{scope}
\end{tikzpicture}
""",
'r30_axe_oblique_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-2,-2) grid (6,6);\draw[geoVecteur] (-2,0)--(6.35,0);\draw[geoVecteur] (0,-2)--(0,6.35);
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (5,0) {$ 5 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,5) {$ 5 $};
\node[coteTexte,anchor=south east,font=\small] at (0,6) {$ 6 $};
\draw[geoTrait] (-1,-1)--(5,5);
\draw[geoAide] (1,3)--(3,1);
\draw[geoAide] (4,2)--(2,4);
\fill[otInk] (0,0) circle (2pt);
\node[anchor=south east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otOrange] (1,1) circle (2pt);
\node[anchor=south east,text=otOrange,inner sep=4pt] at (1,1) {$ I $};
\fill[otNavy] (1,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (1,3) {$ A $};
\fill[otNavy] (4,2) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (4,2) {$ B $};
\fill[otGreenDark] (3,1) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (3,1) {$ A' $};
\fill[otGreenDark] (2,4) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (2,4) {$ B' $};

\node[anchor=west,text=otInk,inner sep=4pt] at (5,5) {$ (d) $};
\end{scope}
\end{tikzpicture}
""",
'r30_cercle_image_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=0.5416666666666666cm,y=0.5416666666666666cm]
\draw[otRule,line width=.25pt,step=1] (-6,-4) grid (6,4);\draw[geoVecteur] (-6,0)--(6.35,0);\draw[geoVecteur] (0,-4)--(0,4.35);
\node[coteTexte,anchor=south,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=south,font=\small] at (-5,0) {$ -5 $};
\node[coteTexte,anchor=south,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=south,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=south,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=south,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=south,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=south,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=south,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=south,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=south,font=\small] at (5,0) {$ 5 $};
\node[coteTexte,anchor=south,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\draw[otNavy,line width=1pt] (3,1) circle (2);
\draw[otGreenDark,line width=1pt] (-3,-1) circle (2);
\fill[otInk] (0,0) circle (2pt);
\node[anchor=south west,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (3,1) circle (2pt);
\node[anchor=south,text=otNavy,inner sep=4pt] at (3,1) {$ C $};
\fill[otGreenDark] (-3,-1) circle (2pt);
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (-3,-1) {$ C' $};
\fill[otNavy] (5,1) circle (2pt);
\node[anchor=west,text=otNavy,inner sep=4pt] at (5,1) {$ P $};
\fill[otGreenDark] (-5,-1) circle (2pt);
\node[anchor=east,text=otGreenDark,inner sep=4pt] at (-5,-1) {$ P' $};

\end{scope}
\end{tikzpicture}
""",
'r30_centre_inconnu_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-3,-1) grid (5,5);\draw[geoVecteur] (-3,0)--(5.35,0);\draw[geoVecteur] (0,-1)--(0,5.35);
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (5,0) {$ 5 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,5) {$ 5 $};
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ 0 $};
\draw[geoAide] (-2,1)--(4,3);
\draw[geoAide] (0,4)--(2,0);
\fill[otNavy] (-2,1) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-2,1) {$ A $};
\fill[otNavy] (4,3) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (4,3) {$ A' $};
\fill[otNavy] (0,4) circle (2pt);
\node[anchor=east,text=otNavy,inner sep=4pt] at (0,4) {$ B $};
\fill[otGreenDark] (2,0) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (2,0) {$ B' $};
\fill[otGreenDark] (1,2) circle (2pt);
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (1.4,2.5) {$ S $};

\end{scope}
\end{tikzpicture}
""",
'r30_deux_symetries_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-4,-3) grid (4,3);\draw[geoVecteur] (-4,0)--(4.35,0);\draw[geoVecteur] (0,-3)--(0,3.35);
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\draw[geoAide] (3,-2)--(-3,2);
\draw[geoAide] (3,-2)--(-3,-2);
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (3,-2) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (3,-2) {$ A $};
\fill[otGreenDark] (-3,2) circle (2pt);
\node[anchor=south east,text=otGreenDark,inner sep=4pt] at (-3,2) {$ A_c $};
\fill[otGreenDark] (-3,-2) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (-3,-2) {$ A_a $};

\end{scope}
\end{tikzpicture}
""",
'r30_rectangle_centre_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-4,-3) grid (6,3);\draw[geoVecteur] (-4,0)--(6.35,0);\draw[geoVecteur] (0,-3)--(0,3.35);
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (5,0) {$ 5 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ 0 $};
\draw[otNavy,line width=1pt] (-3,2)--(5,2)--(5,-2)--(-3,-2)--cycle;
\draw[geoAide] (-3,2)--(5,-2);
\draw[geoAide] (5,2)--(-3,-2);
\fill[otNavy] (-3,2) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (-3,2) {$ A $};
\fill[otNavy] (5,2) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (5,2) {$ B $};
\fill[otNavy] (5,-2) circle (2pt);
\node[anchor=north west,text=otNavy,inner sep=4pt] at (5,-2) {$ C $};
\fill[otNavy] (-3,-2) circle (2pt);
\node[anchor=north east,text=otNavy,inner sep=4pt] at (-3,-2) {$ D $};
\fill[otGreenDark] (1,0) circle (2pt);
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (1,0.5) {$ S $};

\end{scope}
\end{tikzpicture}
""",
'r30_successives_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-3,-2) grid (3,2);\draw[geoVecteur] (-3,0)--(3.35,0);\draw[geoVecteur] (0,-2)--(0,2.35);
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\draw[geoAide] (2,1)--(-2,-1);
\draw[geoAide] (-2,-1)--(2,-1);
\fill[otInk] (0,0) circle (2pt);
\node[anchor=south east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (2,1) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (2,1) {$ A $};
\fill[otOrange] (-2,-1) circle (2pt);
\node[anchor=north east,text=otOrange,inner sep=4pt] at (-2,-1) {$ B $};
\fill[otGreenDark] (2,-1) circle (2pt);
\node[anchor=north west,text=otGreenDark,inner sep=4pt] at (2,-1) {$ C $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_2_1': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-5,-4) grid (5,4);\draw[geoVecteur] (-5,0)--(5.35,0);\draw[geoVecteur] (0,-4)--(0,4.35);
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
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\draw[otNavy,line width=1pt] (2,1)--(4,1)--(2,3)--cycle;
\draw[otGreenDark,line width=1pt] (-2,-1)--(-4,-1)--(-2,-3)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (2,1) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (2,1) {$ A $};
\fill[otNavy] (4,1) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (4,1) {$ B $};
\fill[otNavy] (2,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (2,3) {$ C $};
\fill[otGreenDark] (-2,-1) circle (2pt);
\node[anchor=north west,text=otGreenDark,inner sep=4pt] at (-2,-1) {$ A' $};
\fill[otGreenDark] (-4,-1) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (-4,-1) {$ B' $};
\fill[otGreenDark] (-2,-3) circle (2pt);
\node[anchor=north west,text=otGreenDark,inner sep=4pt] at (-2,-3) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_3_1': r"""
\begin{tikzpicture}
\begin{scope}[x=0.5416666666666666cm,y=0.5416666666666666cm]
\draw[otRule,line width=.25pt,step=1] (-6,-1) grid (6,4);\draw[geoVecteur] (-6,0)--(6.35,0);\draw[geoVecteur] (0,-1)--(0,4.35);
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
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\draw[otNavy,line width=1pt] (3,1)--(5,1)--(3,3)--cycle;
\draw[otGreenDark,line width=1pt] (-3,1)--(-5,1)--(-3,3)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (3,1) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (3,1) {$ A $};
\fill[otNavy] (5,1) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (5,1) {$ B $};
\fill[otNavy] (3,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (3,3) {$ C $};
\fill[otGreenDark] (-3,1) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-3,1) {$ A' $};
\fill[otGreenDark] (-5,1) circle (2pt);
\node[anchor=south east,text=otGreenDark,inner sep=4pt] at (-5,1) {$ B' $};
\fill[otGreenDark] (-3,3) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-3,3) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_5_1': r"""
\begin{tikzpicture}
\begin{scope}[x=0.40625cm,y=0.40625cm]
\draw[otRule,line width=.25pt,step=1] (-8,-1) grid (8,4);\draw[geoVecteur] (-8,0)--(8.35,0);\draw[geoVecteur] (0,-1)--(0,4.35);
\node[coteTexte,anchor=north,font=\small] at (-8,0) {$ -8 $};
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north,font=\small] at (8,0) {$ 8 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\draw[otNavy,line width=1pt] (5,1)--(7,1)--(5,3)--cycle;
\draw[otGreenDark,line width=1pt] (-5,1)--(-7,1)--(-5,3)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (5,1) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (5,1) {$ A $};
\fill[otNavy] (7,1) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (7,1) {$ B $};
\fill[otNavy] (5,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (5,3) {$ C $};
\fill[otGreenDark] (-5,1) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-5,1) {$ A' $};
\fill[otGreenDark] (-7,1) circle (2pt);
\node[anchor=south east,text=otGreenDark,inner sep=4pt] at (-7,1) {$ B' $};
\fill[otGreenDark] (-5,3) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-5,3) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_7_1': r"""
\begin{tikzpicture}
\begin{scope}[x=0.325cm,y=0.325cm]
\draw[otRule,line width=.25pt,step=1] (-10,-1) grid (10,4);\draw[geoVecteur] (-10,0)--(10.35,0);\draw[geoVecteur] (0,-1)--(0,4.35);
\node[coteTexte,anchor=north,font=\small] at (-10,0) {$ -10 $};
\node[coteTexte,anchor=north,font=\small] at (-8,0) {$ -8 $};
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north,font=\small] at (8,0) {$ 8 $};
\node[coteTexte,anchor=north,font=\small] at (10,0) {$ 10 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\draw[otNavy,line width=1pt] (7,1)--(9,1)--(7,3)--cycle;
\draw[otGreenDark,line width=1pt] (-7,1)--(-9,1)--(-7,3)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (7,1) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (7,1) {$ A $};
\fill[otNavy] (9,1) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (9,1) {$ B $};
\fill[otNavy] (7,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (7,3) {$ C $};
\fill[otGreenDark] (-7,1) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-7,1) {$ A' $};
\fill[otGreenDark] (-9,1) circle (2pt);
\node[anchor=south east,text=otGreenDark,inner sep=4pt] at (-9,1) {$ B' $};
\fill[otGreenDark] (-7,3) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-7,3) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_2_2': r"""
\begin{tikzpicture}
\begin{scope}[x=0.62cm,y=0.62cm]
\draw[otRule,line width=.25pt,step=1] (-5,-5) grid (5,5);\draw[geoVecteur] (-5,0)--(5.35,0);\draw[geoVecteur] (0,-5)--(0,5.35);
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
\draw[otNavy,line width=1pt] (2,2)--(4,2)--(2,4)--cycle;
\draw[otGreenDark,line width=1pt] (-2,-2)--(-4,-2)--(-2,-4)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (2,2) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (2,2) {$ A $};
\fill[otNavy] (4,2) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (4,2) {$ B $};
\fill[otNavy] (2,4) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (2,4) {$ C $};
\fill[otGreenDark] (-2,-2) circle (2pt);
\node[anchor=north west,text=otGreenDark,inner sep=4pt] at (-2,-2) {$ A' $};
\fill[otGreenDark] (-4,-2) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (-4,-2) {$ B' $};
\fill[otGreenDark] (-2,-4) circle (2pt);
\node[anchor=north west,text=otGreenDark,inner sep=4pt] at (-2,-4) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_3_2': r"""
\begin{tikzpicture}
\begin{scope}[x=0.5416666666666666cm,y=0.5416666666666666cm]
\draw[otRule,line width=.25pt,step=1] (-6,-1) grid (6,5);\draw[geoVecteur] (-6,0)--(6.35,0);\draw[geoVecteur] (0,-1)--(0,5.35);
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
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,5) {$ 5 $};
\draw[otNavy,line width=1pt] (3,2)--(5,2)--(3,4)--cycle;
\draw[otGreenDark,line width=1pt] (-3,2)--(-5,2)--(-3,4)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (3,2) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (3,2) {$ A $};
\fill[otNavy] (5,2) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (5,2) {$ B $};
\fill[otNavy] (3,4) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (3,4) {$ C $};
\fill[otGreenDark] (-3,2) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-3,2) {$ A' $};
\fill[otGreenDark] (-5,2) circle (2pt);
\node[anchor=south east,text=otGreenDark,inner sep=4pt] at (-5,2) {$ B' $};
\fill[otGreenDark] (-3,4) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-3,4) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_5_2': r"""
\begin{tikzpicture}
\begin{scope}[x=0.40625cm,y=0.40625cm]
\draw[otRule,line width=.25pt,step=1] (-8,-1) grid (8,5);\draw[geoVecteur] (-8,0)--(8.35,0);\draw[geoVecteur] (0,-1)--(0,5.35);
\node[coteTexte,anchor=north,font=\small] at (-8,0) {$ -8 $};
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north,font=\small] at (8,0) {$ 8 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\draw[otNavy,line width=1pt] (5,2)--(7,2)--(5,4)--cycle;
\draw[otGreenDark,line width=1pt] (-5,2)--(-7,2)--(-5,4)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (5,2) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (5,2) {$ A $};
\fill[otNavy] (7,2) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (7,2) {$ B $};
\fill[otNavy] (5,4) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (5,4) {$ C $};
\fill[otGreenDark] (-5,2) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-5,2) {$ A' $};
\fill[otGreenDark] (-7,2) circle (2pt);
\node[anchor=south east,text=otGreenDark,inner sep=4pt] at (-7,2) {$ B' $};
\fill[otGreenDark] (-5,4) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-5,4) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_6_2': r"""
\begin{tikzpicture}
\begin{scope}[x=0.3611111111111111cm,y=0.3611111111111111cm]
\draw[otRule,line width=.25pt,step=1] (-9,-5) grid (9,5);\draw[geoVecteur] (-9,0)--(9.35,0);\draw[geoVecteur] (0,-5)--(0,5.35);
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
\draw[otNavy,line width=1pt] (6,2)--(8,2)--(6,4)--cycle;
\draw[otGreenDark,line width=1pt] (-6,-2)--(-8,-2)--(-6,-4)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (6,2) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (6,2) {$ A $};
\fill[otNavy] (8,2) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (8,2) {$ B $};
\fill[otNavy] (6,4) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (6,4) {$ C $};
\fill[otGreenDark] (-6,-2) circle (2pt);
\node[anchor=north west,text=otGreenDark,inner sep=4pt] at (-6,-2) {$ A' $};
\fill[otGreenDark] (-8,-2) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (-8,-2) {$ B' $};
\fill[otGreenDark] (-6,-4) circle (2pt);
\node[anchor=north west,text=otGreenDark,inner sep=4pt] at (-6,-4) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_7_2': r"""
\begin{tikzpicture}
\begin{scope}[x=0.325cm,y=0.325cm]
\draw[otRule,line width=.25pt,step=1] (-10,-1) grid (10,5);\draw[geoVecteur] (-10,0)--(10.35,0);\draw[geoVecteur] (0,-1)--(0,5.35);
\node[coteTexte,anchor=north,font=\small] at (-10,0) {$ -10 $};
\node[coteTexte,anchor=north,font=\small] at (-8,0) {$ -8 $};
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north,font=\small] at (8,0) {$ 8 $};
\node[coteTexte,anchor=north,font=\small] at (10,0) {$ 10 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\draw[otNavy,line width=1pt] (7,2)--(9,2)--(7,4)--cycle;
\draw[otGreenDark,line width=1pt] (-7,2)--(-9,2)--(-7,4)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (7,2) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (7,2) {$ A $};
\fill[otNavy] (9,2) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (9,2) {$ B $};
\fill[otNavy] (7,4) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (7,4) {$ C $};
\fill[otGreenDark] (-7,2) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-7,2) {$ A' $};
\fill[otGreenDark] (-9,2) circle (2pt);
\node[anchor=south east,text=otGreenDark,inner sep=4pt] at (-9,2) {$ B' $};
\fill[otGreenDark] (-7,4) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-7,4) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_2_3': r"""
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
\draw[otNavy,line width=1pt] (2,3)--(4,3)--(2,5)--cycle;
\draw[otGreenDark,line width=1pt] (-2,-3)--(-4,-3)--(-2,-5)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (2,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (2,3) {$ A $};
\fill[otNavy] (4,3) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (4,3) {$ B $};
\fill[otNavy] (2,5) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (2,5) {$ C $};
\fill[otGreenDark] (-2,-3) circle (2pt);
\node[anchor=north west,text=otGreenDark,inner sep=4pt] at (-2,-3) {$ A' $};
\fill[otGreenDark] (-4,-3) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (-4,-3) {$ B' $};
\fill[otGreenDark] (-2,-5) circle (2pt);
\node[anchor=north west,text=otGreenDark,inner sep=4pt] at (-2,-5) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_3_3': r"""
\begin{tikzpicture}
\begin{scope}[x=0.5416666666666666cm,y=0.5416666666666666cm]
\draw[otRule,line width=.25pt,step=1] (-6,-1) grid (6,6);\draw[geoVecteur] (-6,0)--(6.35,0);\draw[geoVecteur] (0,-1)--(0,6.35);
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
\node[coteTexte,anchor=north east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,5) {$ 5 $};
\node[coteTexte,anchor=south east,font=\small] at (0,6) {$ 6 $};
\draw[otNavy,line width=1pt] (3,3)--(5,3)--(3,5)--cycle;
\draw[otGreenDark,line width=1pt] (-3,3)--(-5,3)--(-3,5)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (3,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (3,3) {$ A $};
\fill[otNavy] (5,3) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (5,3) {$ B $};
\fill[otNavy] (3,5) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (3,5) {$ C $};
\fill[otGreenDark] (-3,3) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-3,3) {$ A' $};
\fill[otGreenDark] (-5,3) circle (2pt);
\node[anchor=south east,text=otGreenDark,inner sep=4pt] at (-5,3) {$ B' $};
\fill[otGreenDark] (-3,5) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-3,5) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_5_3': r"""
\begin{tikzpicture}
\begin{scope}[x=0.40625cm,y=0.40625cm]
\draw[otRule,line width=.25pt,step=1] (-8,-1) grid (8,6);\draw[geoVecteur] (-8,0)--(8.35,0);\draw[geoVecteur] (0,-1)--(0,6.35);
\node[coteTexte,anchor=north,font=\small] at (-8,0) {$ -8 $};
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north,font=\small] at (8,0) {$ 8 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,6) {$ 6 $};
\draw[otNavy,line width=1pt] (5,3)--(7,3)--(5,5)--cycle;
\draw[otGreenDark,line width=1pt] (-5,3)--(-7,3)--(-5,5)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (5,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (5,3) {$ A $};
\fill[otNavy] (7,3) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (7,3) {$ B $};
\fill[otNavy] (5,5) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (5,5) {$ C $};
\fill[otGreenDark] (-5,3) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-5,3) {$ A' $};
\fill[otGreenDark] (-7,3) circle (2pt);
\node[anchor=south east,text=otGreenDark,inner sep=4pt] at (-7,3) {$ B' $};
\fill[otGreenDark] (-5,5) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-5,5) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_6_3': r"""
\begin{tikzpicture}
\begin{scope}[x=0.3611111111111111cm,y=0.3611111111111111cm]
\draw[otRule,line width=.25pt,step=1] (-9,-6) grid (9,6);\draw[geoVecteur] (-9,0)--(9.35,0);\draw[geoVecteur] (0,-6)--(0,6.35);
\node[coteTexte,anchor=north,font=\small] at (-8,0) {$ -8 $};
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north,font=\small] at (8,0) {$ 8 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-6) {$ -6 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-4) {$ -4 $};
\node[coteTexte,anchor=north east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,6) {$ 6 $};
\draw[otNavy,line width=1pt] (6,3)--(8,3)--(6,5)--cycle;
\draw[otGreenDark,line width=1pt] (-6,-3)--(-8,-3)--(-6,-5)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (6,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (6,3) {$ A $};
\fill[otNavy] (8,3) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (8,3) {$ B $};
\fill[otNavy] (6,5) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (6,5) {$ C $};
\fill[otGreenDark] (-6,-3) circle (2pt);
\node[anchor=north west,text=otGreenDark,inner sep=4pt] at (-6,-3) {$ A' $};
\fill[otGreenDark] (-8,-3) circle (2pt);
\node[anchor=north east,text=otGreenDark,inner sep=4pt] at (-8,-3) {$ B' $};
\fill[otGreenDark] (-6,-5) circle (2pt);
\node[anchor=north west,text=otGreenDark,inner sep=4pt] at (-6,-5) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
'r30_motif_7_3': r"""
\begin{tikzpicture}
\begin{scope}[x=0.325cm,y=0.325cm]
\draw[otRule,line width=.25pt,step=1] (-10,-1) grid (10,6);\draw[geoVecteur] (-10,0)--(10.35,0);\draw[geoVecteur] (0,-1)--(0,6.35);
\node[coteTexte,anchor=north,font=\small] at (-10,0) {$ -10 $};
\node[coteTexte,anchor=north,font=\small] at (-8,0) {$ -8 $};
\node[coteTexte,anchor=north,font=\small] at (-6,0) {$ -6 $};
\node[coteTexte,anchor=north,font=\small] at (-4,0) {$ -4 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=north,font=\small] at (6,0) {$ 6 $};
\node[coteTexte,anchor=north,font=\small] at (8,0) {$ 8 $};
\node[coteTexte,anchor=north,font=\small] at (10,0) {$ 10 $};
\node[coteTexte,anchor=south east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=south east,font=\small] at (0,4) {$ 4 $};
\node[coteTexte,anchor=south east,font=\small] at (0,6) {$ 6 $};
\draw[otNavy,line width=1pt] (7,3)--(9,3)--(7,5)--cycle;
\draw[otGreenDark,line width=1pt] (-7,3)--(-9,3)--(-7,5)--cycle;
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\fill[otNavy] (7,3) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (7,3) {$ A $};
\fill[otNavy] (9,3) circle (2pt);
\node[anchor=south west,text=otNavy,inner sep=4pt] at (9,3) {$ B $};
\fill[otNavy] (7,5) circle (2pt);
\node[anchor=south east,text=otNavy,inner sep=4pt] at (7,5) {$ C $};
\fill[otGreenDark] (-7,3) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-7,3) {$ A' $};
\fill[otGreenDark] (-9,3) circle (2pt);
\node[anchor=south east,text=otGreenDark,inner sep=4pt] at (-9,3) {$ B' $};
\fill[otGreenDark] (-7,5) circle (2pt);
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (-7,5) {$ C' $};

\end{scope}
\end{tikzpicture}
""",
}
