# -*- coding: utf-8 -*-
"""Figures TikZ au style des livres ; compiler avec outils/figures_livre.py."""
FIGURES = {
}


# Figures pédagogiques ajoutées lors de la révision du 30 octobre 2026.
FIGURES.update({
'roue_aabb': r"""\begin{tikzpicture}[line cap=round,line join=round]
\fill[otNavy!20] (0,0)--(1.40000,0.00000) arc[start angle=0,end angle=90,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(1.4,0.0);
\node[anchor=center,text=otInk] at (0.5868986283848344,0.5868986283848344) {A};
\fill[otNavy!20] (0,0)--(0.00000,1.40000) arc[start angle=90,end angle=180,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(8.572527594031472e-17,1.4);
\node[anchor=center,text=otInk] at (-0.5868986283848344,0.5868986283848344) {A};
\fill[otOrange!30] (0,0)--(-1.40000,0.00000) arc[start angle=180,end angle=270,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(-1.4,1.7145055188062944e-16);
\node[anchor=center,text=otInk] at (-0.5868986283848345,-0.5868986283848344) {B};
\fill[otOrange!30] (0,0)--(-0.00000,-1.40000) arc[start angle=270,end angle=360,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(-2.5717582782094415e-16,-1.4);
\node[anchor=center,text=otInk] at (0.5868986283848343,-0.5868986283848345) {B};

\end{tikzpicture}""",
'roue_aabb_corrige': r"""\begin{tikzpicture}[line cap=round,line join=round]
\fill[otGreen!40] (0,0)--(1.40000,0.00000) arc[start angle=0,end angle=90,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(1.4,0.0);
\node[anchor=center,text=otInk] at (0.5868986283848344,0.5868986283848344) {A};
\fill[otGreen!40] (0,0)--(0.00000,1.40000) arc[start angle=90,end angle=180,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(8.572527594031472e-17,1.4);
\node[anchor=center,text=otInk] at (-0.5868986283848344,0.5868986283848344) {A};
\fill[otRule] (0,0)--(-1.40000,0.00000) arc[start angle=180,end angle=270,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(-1.4,1.7145055188062944e-16);
\node[anchor=center,text=otInk] at (-0.5868986283848345,-0.5868986283848344) {B};
\fill[otRule] (0,0)--(-0.00000,-1.40000) arc[start angle=270,end angle=360,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(-2.5717582782094415e-16,-1.4);
\node[anchor=center,text=otInk] at (0.5868986283848343,-0.5868986283848345) {B};

\end{tikzpicture}""",
'roue_inegale': r"""\begin{tikzpicture}[line cap=round,line join=round]
\fill[otRed!65] (0,0)--(1.40000,0.00000) arc[start angle=0,end angle=180,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(1.4,0.0);
\node[anchor=west,text=otInk] at (1.85,0.8) {Rouge : $180^\circ$};
\fill[otNavy!50] (0,0)--(-1.40000,0.00000) arc[start angle=180,end angle=270,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(-1.4,1.7145055188062944e-16);
\node[anchor=west,text=otInk] at (1.85,0.0) {Bleu : $90^\circ$};
\fill[otGreen!65] (0,0)--(-0.00000,-1.40000) arc[start angle=270,end angle=360,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(-2.5717582782094415e-16,-1.4);
\node[anchor=west,text=otInk] at (1.85,-0.8) {Vert : $90^\circ$};

\end{tikzpicture}""",
'roue_egale': r"""\begin{tikzpicture}[line cap=round,line join=round]
\fill[otRed!65] (0,0)--(1.40000,0.00000) arc[start angle=0,end angle=120,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(1.4,0.0);
\node[anchor=west,text=otInk] at (1.85,0.8) {Rouge : $120^\circ$};
\fill[otNavy!50] (0,0)--(-0.70000,1.21244) arc[start angle=120,end angle=240,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(-0.6999999999999996,1.2124355652982142);
\node[anchor=west,text=otInk] at (1.85,0.0) {Bleu : $120^\circ$};
\fill[otGreen!65] (0,0)--(-0.70000,-1.21244) arc[start angle=240,end angle=360,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(-0.7000000000000006,-1.2124355652982137);
\node[anchor=west,text=otInk] at (1.85,-0.8) {Vert : $120^\circ$};

\end{tikzpicture}""",
})
