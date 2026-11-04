# -*- coding: utf-8 -*-
"""Figures TikZ ; pr?ambule officiel fourni par outils/figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\node[font=\normalsize,text=otNavy] at (4.2,1.3) {Pantalon 1};
\node[font=\normalsize,text=otNavy] at (4.2,0.19999999999999996) {Pantalon 2};
\node[text=otNavy] at (0,2.6) {A};
\draw[otRule] (.35,2.6)--(3.1,1.3);
\draw[otRule] (.35,2.6)--(3.1,0.19999999999999996);
\node[text=otNavy] at (0,1.4000000000000001) {B};
\draw[otRule] (.35,1.4000000000000001)--(3.1,1.3);
\draw[otRule] (.35,1.4000000000000001)--(3.1,0.19999999999999996);
\node[text=otNavy] at (0,0.20000000000000018) {C};
\draw[otRule] (.35,0.20000000000000018)--(3.1,1.3);
\draw[otRule] (.35,0.20000000000000018)--(3.1,0.19999999999999996);
\node[font=\normalsize] at (4.5,2.8) {3 tee-shirts, 2 pantalons};
\end{tikzpicture}
""",
    'ex5_arbre': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\node[font=\normalsize] at (0.3,-1.75) {E1};
\node[font=\normalsize] at (3,-0.35) {P1};
\draw[otRule] (.7,-1.75)--(2.6,-0.35);
\node[font=\normalsize,text=otGreenDark] at (6.3,0.0) {D1};
\draw[otRule] (3.4,-0.35)--(5.9,0.0);
\node[font=\normalsize,text=otGreenDark] at (6.3,-0.7) {D2};
\draw[otRule] (3.4,-0.35)--(5.9,-0.7);
\node[font=\normalsize] at (3,-1.75) {P2};
\draw[otRule] (.7,-1.75)--(2.6,-1.75);
\node[font=\normalsize,text=otGreenDark] at (6.3,-1.4) {D1};
\draw[otRule] (3.4,-1.75)--(5.9,-1.4);
\node[font=\normalsize,text=otGreenDark] at (6.3,-2.0999999999999996) {D2};
\draw[otRule] (3.4,-1.75)--(5.9,-2.0999999999999996);
\node[font=\normalsize] at (3,-3.15) {P3};
\draw[otRule] (.7,-1.75)--(2.6,-3.15);
\node[font=\normalsize,text=otGreenDark] at (6.3,-2.8) {D1};
\draw[otRule] (3.4,-3.15)--(5.9,-2.8);
\node[font=\normalsize,text=otGreenDark] at (6.3,-3.5) {D2};
\draw[otRule] (3.4,-3.15)--(5.9,-3.5);
\node[font=\normalsize] at (0.3,-5.949999999999999) {E2};
\node[font=\normalsize] at (3,-4.55) {P1};
\draw[otRule] (.7,-5.949999999999999)--(2.6,-4.55);
\node[font=\normalsize,text=otGreenDark] at (6.3,-4.199999999999999) {D1};
\draw[otRule] (3.4,-4.55)--(5.9,-4.199999999999999);
\node[font=\normalsize,text=otGreenDark] at (6.3,-4.8999999999999995) {D2};
\draw[otRule] (3.4,-4.55)--(5.9,-4.8999999999999995);
\node[font=\normalsize] at (3,-5.949999999999999) {P2};
\draw[otRule] (.7,-5.949999999999999)--(2.6,-5.949999999999999);
\node[font=\normalsize,text=otGreenDark] at (6.3,-5.6) {D1};
\draw[otRule] (3.4,-5.949999999999999)--(5.9,-5.6);
\node[font=\normalsize,text=otGreenDark] at (6.3,-6.3) {D2};
\draw[otRule] (3.4,-5.949999999999999)--(5.9,-6.3);
\node[font=\normalsize] at (3,-7.35) {P3};
\draw[otRule] (.7,-5.949999999999999)--(2.6,-7.35);
\node[font=\normalsize,text=otGreenDark] at (6.3,-7.0) {D1};
\draw[otRule] (3.4,-7.35)--(5.9,-7.0);
\node[font=\normalsize,text=otGreenDark] at (6.3,-7.699999999999999) {D2};
\draw[otRule] (3.4,-7.35)--(5.9,-7.699999999999999);
\node[font=\normalsize,text=otNavy] at (3.3,1) {Entrée puis plat puis dessert};
\end{tikzpicture}
""",
}
