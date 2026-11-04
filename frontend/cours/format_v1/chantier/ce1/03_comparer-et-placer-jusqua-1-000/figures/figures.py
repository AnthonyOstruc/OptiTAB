# -*- coding: utf-8 -*-
"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,-{Stealth}] (-.15,0) -- (7.9,0);
\draw[otNavy] (0.0,-.08) -- (0.0,.08);
\node[text=otInk,font=\normalsize] at (0.0,-0.43) {300};
\draw[otNavy] (0.75,-.08) -- (0.75,.08);
\node[text=otInk,font=\normalsize] at (0.75,-0.43) {310};
\draw[otNavy] (1.5,-.08) -- (1.5,.08);
\node[text=otInk,font=\normalsize] at (1.5,-0.43) {320};
\draw[otNavy] (2.25,-.08) -- (2.25,.08);
\node[text=otInk,font=\normalsize] at (2.25,-0.43) {330};
\draw[otNavy] (3.0,-.08) -- (3.0,.08);
\node[text=otInk,font=\normalsize] at (3.0,-0.43) {340};
\draw[otNavy] (3.75,-.08) -- (3.75,.08);
\node[text=otInk,font=\normalsize] at (3.75,-0.43) {350};
\draw[otNavy] (4.5,-.08) -- (4.5,.08);
\node[text=otInk,font=\normalsize] at (4.5,-0.43) {360};
\draw[otNavy] (5.25,-.08) -- (5.25,.08);
\node[text=otInk,font=\normalsize] at (5.25,-0.43) {370};
\draw[otNavy] (6.0,-.08) -- (6.0,.08);
\node[text=otInk,font=\normalsize] at (6.0,-0.43) {380};
\draw[otNavy] (6.75,-.08) -- (6.75,.08);
\node[text=otInk,font=\normalsize] at (6.75,-0.43) {390};
\draw[otNavy] (7.5,-.08) -- (7.5,.08);
\node[text=otInk,font=\normalsize] at (7.5,-0.43) {400};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,-{Stealth}] (-.15,0) -- (7.9,0);
\draw[otNavy] (0.0,-.08) -- (0.0,.08);
\node[text=otInk,font=\normalsize] at (0.0,-0.43) {400};
\draw[otNavy] (0.75,-.08) -- (0.75,.08);
\node[text=otInk,font=\normalsize] at (0.75,-0.43) {410};
\draw[otNavy] (1.5,-.08) -- (1.5,.08);
\node[text=otInk,font=\normalsize] at (1.5,-0.43) {?};
\draw[otNavy] (2.25,-.08) -- (2.25,.08);
\node[text=otInk,font=\normalsize] at (2.25,-0.43) {430};
\draw[otNavy] (3.0,-.08) -- (3.0,.08);
\node[text=otInk,font=\normalsize] at (3.0,-0.43) {440};
\draw[otNavy] (3.75,-.08) -- (3.75,.08);
\node[text=otInk,font=\normalsize] at (3.75,-0.43) {?};
\draw[otNavy] (4.5,-.08) -- (4.5,.08);
\node[text=otInk,font=\normalsize] at (4.5,-0.43) {460};
\draw[otNavy] (5.25,-.08) -- (5.25,.08);
\node[text=otInk,font=\normalsize] at (5.25,-0.43) {470};
\draw[otNavy] (6.0,-.08) -- (6.0,.08);
\node[text=otInk,font=\normalsize] at (6.0,-0.43) {?};
\draw[otNavy] (6.75,-.08) -- (6.75,.08);
\node[text=otInk,font=\normalsize] at (6.75,-0.43) {490};
\draw[otNavy] (7.5,-.08) -- (7.5,.08);
\node[text=otInk,font=\normalsize] at (7.5,-0.43) {500};
\end{tikzpicture}
""",
    'ex6_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,-{Stealth}] (-.15,0) -- (7.9,0);
\draw[otNavy] (0.0,-.08) -- (0.0,.08);
\node[text=otInk,font=\normalsize] at (0.0,-0.43) {0};
\draw[otNavy] (0.75,-.08) -- (0.75,.08);
\node[text=otInk,font=\normalsize] at (0.75,-0.43) {100};
\draw[otNavy] (1.5,-.08) -- (1.5,.08);
\node[text=otInk,font=\normalsize] at (1.5,-0.43) {200};
\draw[otNavy] (2.25,-.08) -- (2.25,.08);
\node[text=otInk,font=\normalsize] at (2.25,-0.43) {300};
\draw[otNavy] (3.0,-.08) -- (3.0,.08);
\node[text=otInk,font=\normalsize] at (3.0,-0.43) {400};
\draw[otNavy] (3.75,-.08) -- (3.75,.08);
\node[text=otInk,font=\normalsize] at (3.75,-0.43) {500};
\draw[otNavy] (4.5,-.08) -- (4.5,.08);
\node[text=otInk,font=\normalsize] at (4.5,-0.43) {600};
\fill[otNavy] (4.5,0) circle (2pt);
\node[text=otInk] at (4.5,0.45) {$A$};
\draw[otNavy] (5.25,-.08) -- (5.25,.08);
\node[text=otInk,font=\normalsize] at (5.25,-0.43) {700};
\draw[otNavy] (6.0,-.08) -- (6.0,.08);
\node[text=otInk,font=\normalsize] at (6.0,-0.43) {800};
\draw[otNavy] (6.75,-.08) -- (6.75,.08);
\node[text=otInk,font=\normalsize] at (6.75,-0.43) {900};
\draw[otNavy] (7.5,-.08) -- (7.5,.08);
\node[text=otInk,font=\normalsize] at (7.5,-0.43) {1000};
\end{tikzpicture}
""",
}
