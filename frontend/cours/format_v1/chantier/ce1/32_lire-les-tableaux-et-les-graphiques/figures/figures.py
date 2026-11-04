# -*- coding: utf-8 -*-
"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otRule] (0,0.0) -- (6.5,0.0);
\node[text=otMuted,font=\normalsize] at (-0.35,0.0) {0};
\draw[otRule] (0,0.43) -- (6.5,0.43);
\node[text=otMuted,font=\normalsize] at (-0.35,0.43) {1};
\draw[otRule] (0,0.86) -- (6.5,0.86);
\node[text=otMuted,font=\normalsize] at (-0.35,0.86) {2};
\draw[otRule] (0,1.29) -- (6.5,1.29);
\node[text=otMuted,font=\normalsize] at (-0.35,1.29) {3};
\draw[otRule] (0,1.72) -- (6.5,1.72);
\node[text=otMuted,font=\normalsize] at (-0.35,1.72) {4};
\draw[otRule] (0,2.15) -- (6.5,2.15);
\node[text=otMuted,font=\normalsize] at (-0.35,2.15) {5};
\draw[otRule] (0,2.58) -- (6.5,2.58);
\node[text=otMuted,font=\normalsize] at (-0.35,2.58) {6};
\draw[otRule] (0,3.01) -- (6.5,3.01);
\node[text=otMuted,font=\normalsize] at (-0.35,3.01) {7};
\draw[otMuted] (0,0) -- (0,3.1599999999999997);
\draw[otMuted] (0,0) -- (6.5,0);
\draw[draw=otNavy,fill=otNavy!25] (0.7,0) rectangle (1.7,1.72);
\node[text=otInk,font=\normalsize] at (1.2,-0.48) {Lecture};
\draw[draw=otNavy,fill=otNavy!25] (2.7,0) rectangle (3.7,1.29);
\node[text=otInk,font=\normalsize] at (3.2,-0.48) {Dessin};
\draw[draw=otNavy,fill=otNavy!25] (4.7,0) rectangle (5.7,2.58);
\node[text=otInk,font=\normalsize] at (5.2,-0.48) {Ballon};
\node[text=otMuted,font=\normalsize] at (3.25,3.61) {Une graduation = une réponse};
\end{tikzpicture}
""",
    'ex4_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otRule] (0,0.0) -- (6.5,0.0);
\node[text=otMuted,font=\normalsize] at (-0.35,0.0) {0};
\draw[otRule] (0,0.43) -- (6.5,0.43);
\node[text=otMuted,font=\normalsize] at (-0.35,0.43) {1};
\draw[otRule] (0,0.86) -- (6.5,0.86);
\node[text=otMuted,font=\normalsize] at (-0.35,0.86) {2};
\draw[otRule] (0,1.29) -- (6.5,1.29);
\node[text=otMuted,font=\normalsize] at (-0.35,1.29) {3};
\draw[otRule] (0,1.72) -- (6.5,1.72);
\node[text=otMuted,font=\normalsize] at (-0.35,1.72) {4};
\draw[otRule] (0,2.15) -- (6.5,2.15);
\node[text=otMuted,font=\normalsize] at (-0.35,2.15) {5};
\draw[otRule] (0,2.58) -- (6.5,2.58);
\node[text=otMuted,font=\normalsize] at (-0.35,2.58) {6};
\draw[otRule] (0,3.01) -- (6.5,3.01);
\node[text=otMuted,font=\normalsize] at (-0.35,3.01) {7};
\draw[otMuted] (0,0) -- (0,3.1599999999999997);
\draw[otMuted] (0,0) -- (6.5,0);
\draw[draw=otNavy,fill=otNavy!25] (0.7,0) rectangle (1.7,1.72);
\node[text=otInk,font=\normalsize] at (1.2,-0.48) {Lecture};
\draw[draw=otNavy,fill=otNavy!25] (2.7,0) rectangle (3.7,1.29);
\node[text=otInk,font=\normalsize] at (3.2,-0.48) {Dessin};
\draw[draw=otNavy,fill=otNavy!25] (4.7,0) rectangle (5.7,2.58);
\node[text=otInk,font=\normalsize] at (5.2,-0.48) {Ballon};
\node[text=otMuted,font=\normalsize] at (3.25,3.61) {Une graduation = une réponse};
\end{tikzpicture}
""",
    'ex5_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otRule] (0,0.0) -- (6.5,0.0);
\node[text=otMuted,font=\normalsize] at (-0.35,0.0) {0};
\draw[otRule] (0,0.43) -- (6.5,0.43);
\node[text=otMuted,font=\normalsize] at (-0.35,0.43) {1};
\draw[otRule] (0,0.86) -- (6.5,0.86);
\node[text=otMuted,font=\normalsize] at (-0.35,0.86) {2};
\draw[otRule] (0,1.29) -- (6.5,1.29);
\node[text=otMuted,font=\normalsize] at (-0.35,1.29) {3};
\draw[otRule] (0,1.72) -- (6.5,1.72);
\node[text=otMuted,font=\normalsize] at (-0.35,1.72) {4};
\draw[otRule] (0,2.15) -- (6.5,2.15);
\node[text=otMuted,font=\normalsize] at (-0.35,2.15) {5};
\draw[otRule] (0,2.58) -- (6.5,2.58);
\node[text=otMuted,font=\normalsize] at (-0.35,2.58) {6};
\draw[otRule] (0,3.01) -- (6.5,3.01);
\node[text=otMuted,font=\normalsize] at (-0.35,3.01) {7};
\draw[otMuted] (0,0) -- (0,3.1599999999999997);
\draw[otMuted] (0,0) -- (6.5,0);
\draw[draw=otNavy,fill=otNavy!25] (0.7,0) rectangle (1.7,1.72);
\node[text=otInk,font=\normalsize] at (1.2,-0.48) {Lecture};
\draw[draw=otNavy,fill=otNavy!25] (2.7,0) rectangle (3.7,1.29);
\node[text=otInk,font=\normalsize] at (3.2,-0.48) {Dessin};
\draw[draw=otNavy,fill=otNavy!25] (4.7,0) rectangle (5.7,2.58);
\node[text=otInk,font=\normalsize] at (5.2,-0.48) {Ballon};
\node[text=otMuted,font=\normalsize] at (3.25,3.61) {Une graduation = une réponse};
\end{tikzpicture}
""",
    'ex6_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otRule] (0,0.0) -- (6.5,0.0);
\node[text=otMuted,font=\normalsize] at (-0.35,0.0) {0};
\draw[otRule] (0,0.43) -- (6.5,0.43);
\node[text=otMuted,font=\normalsize] at (-0.35,0.43) {1};
\draw[otRule] (0,0.86) -- (6.5,0.86);
\node[text=otMuted,font=\normalsize] at (-0.35,0.86) {2};
\draw[otRule] (0,1.29) -- (6.5,1.29);
\node[text=otMuted,font=\normalsize] at (-0.35,1.29) {3};
\draw[otRule] (0,1.72) -- (6.5,1.72);
\node[text=otMuted,font=\normalsize] at (-0.35,1.72) {4};
\draw[otRule] (0,2.15) -- (6.5,2.15);
\node[text=otMuted,font=\normalsize] at (-0.35,2.15) {5};
\draw[otRule] (0,2.58) -- (6.5,2.58);
\node[text=otMuted,font=\normalsize] at (-0.35,2.58) {6};
\draw[otRule] (0,3.01) -- (6.5,3.01);
\node[text=otMuted,font=\normalsize] at (-0.35,3.01) {7};
\draw[otMuted] (0,0) -- (0,3.1599999999999997);
\draw[otMuted] (0,0) -- (6.5,0);
\draw[draw=otNavy,fill=otNavy!25] (0.7,0) rectangle (1.7,1.72);
\node[text=otInk,font=\normalsize] at (1.2,-0.48) {Lecture};
\draw[draw=otNavy,fill=otNavy!25] (2.7,0) rectangle (3.7,1.29);
\node[text=otInk,font=\normalsize] at (3.2,-0.48) {Dessin};
\draw[draw=otNavy,fill=otNavy!25] (4.7,0) rectangle (5.7,2.58);
\node[text=otInk,font=\normalsize] at (5.2,-0.48) {Ballon};
\node[text=otMuted,font=\normalsize] at (3.25,3.61) {Une graduation = une réponse};
\end{tikzpicture}
""",
    'ex8_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otRule] (0,0.0) -- (6.5,0.0);
\node[text=otMuted,font=\normalsize] at (-0.35,0.0) {0};
\draw[otRule] (0,0.43) -- (6.5,0.43);
\node[text=otMuted,font=\normalsize] at (-0.35,0.43) {1};
\draw[otRule] (0,0.86) -- (6.5,0.86);
\node[text=otMuted,font=\normalsize] at (-0.35,0.86) {2};
\draw[otRule] (0,1.29) -- (6.5,1.29);
\node[text=otMuted,font=\normalsize] at (-0.35,1.29) {3};
\draw[otRule] (0,1.72) -- (6.5,1.72);
\node[text=otMuted,font=\normalsize] at (-0.35,1.72) {4};
\draw[otRule] (0,2.15) -- (6.5,2.15);
\node[text=otMuted,font=\normalsize] at (-0.35,2.15) {5};
\draw[otRule] (0,2.58) -- (6.5,2.58);
\node[text=otMuted,font=\normalsize] at (-0.35,2.58) {6};
\draw[otRule] (0,3.01) -- (6.5,3.01);
\node[text=otMuted,font=\normalsize] at (-0.35,3.01) {7};
\draw[otMuted] (0,0) -- (0,3.1599999999999997);
\draw[otMuted] (0,0) -- (6.5,0);
\draw[draw=otNavy,fill=otNavy!25] (0.7,0) rectangle (1.7,1.72);
\node[text=otInk,font=\normalsize] at (1.2,-0.48) {Lecture};
\draw[draw=otNavy,fill=otNavy!25] (2.7,0) rectangle (3.7,1.29);
\node[text=otInk,font=\normalsize] at (3.2,-0.48) {Dessin};
\draw[draw=otNavy,fill=otNavy!25] (4.7,0) rectangle (5.7,2.58);
\node[text=otInk,font=\normalsize] at (5.2,-0.48) {Ballon};
\node[text=otMuted,font=\normalsize] at (3.25,3.61) {Une graduation = une réponse};
\end{tikzpicture}
""",
}
