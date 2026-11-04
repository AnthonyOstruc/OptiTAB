# -*- coding: utf-8 -*-
"""Figures exactes de la révision du 30 octobre 2026."""
FIGURES={
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
'r30_trois_cotes_corrige': r"""
\begin{tikzpicture}
\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at (1.8,2.4);\draw[geoReponse] (A)--(B)--(C)--cycle;\draw[geoAide] (0,0)--(1.8,-2.4)--(5,0);\node[anchor=east,text=otInk,inner sep=4pt] at (0,0) {$ A $};
\node[anchor=west,text=otInk,inner sep=4pt] at (5,0) {$ B $};
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (1.8,2.4) {$ C $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (1.8,-2.4) {$ C' $};
\draw[otOrange!85] (1.2616776233582279,-2.7217952852331) arc[start angle=-65.13010235415598,end angle=-41.13010235415598,radius=3];\draw[otOrange!85] (2.2596537392834724,1.9733131982891667) arc[start angle=41.13010235415598,end angle=65.13010235415598,radius=3];\draw[otOrange!85] (1.3709396196891999,-1.6822368311443041) arc[start angle=-155.13010235415598,end angle=-131.13010235415598,radius=4];\draw[otOrange!85] (2.368915735614444,3.012871652377963) arc[start angle=131.13010235415598,end angle=155.13010235415598,radius=4];\node[anchor=south,text=otInk,inner sep=4pt] at (2.5,0.25) {$ 5\text{ cm} $};
\node[anchor=east,text=otInk,inner sep=4pt] at (0.4,1.3) {$ 3\text{ cm} $};
\node[anchor=west,text=otInk,inner sep=4pt] at (3.8,1.3) {$ 4\text{ cm} $};

\end{tikzpicture}
""",
'r30_deux_cotes_angle_corrige': r"""
\begin{tikzpicture}
\draw[geoReponse] (0,0)--(5,0)--(2,3.4641016151377544)--cycle;\draw[otOrange] (.65,0) arc[start angle=0,end angle=60,radius=.65];\draw[geoAide] (45:4) arc[start angle=45,end angle=75,radius=4];\node[anchor=east,text=otInk,inner sep=4pt] at (0,0) {$ A $};
\node[anchor=west,text=otInk,inner sep=4pt] at (5,0) {$ B $};
\node[anchor=south,text=otInk,inner sep=4pt] at (2,3.4641016151377544) {$ C $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.5,-0.4) {$ 5\text{ cm} $};
\node[anchor=east,text=otInk,inner sep=4pt] at (0.4,2) {$ 4\text{ cm} $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (1,0.28) {$ 60^\circ $};

\end{tikzpicture}
""",
'r30_isocele_corrige': r"""
\begin{tikzpicture}
\coordinate(A) at (0,3.9601389654660744);\coordinate(B) at (-1.6,0);\coordinate(C) at (1.6,0);\coordinate(M) at (0,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoReponse] (A)--(M);\codage{A}{B}\codage{A}{C}\angledroit{A}{M}{C}\node[anchor=south,text=otInk,inner sep=4pt] at (0,3.9601389654660744) {$ A $};
\node[anchor=north east,text=otInk,inner sep=4pt] at (-1.6,0) {$ B $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (1.6,0) {$ C $};
\node[anchor=north,text=otInk,inner sep=4pt] at (0,0) {$ M $};
\node[anchor=south west,text=otOrange,inner sep=4pt] at (0.5,4.460138965466074) {$ \widehat{BAC}=44^\circ $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (0,-0.85) {$ \widehat{BAM}=22^\circ $};

\end{tikzpicture}
""",
'r30_mediatrices_corrige': r"""
\begin{tikzpicture}
\coordinate(A) at (0,0);\coordinate(B) at (6,0);\coordinate(C) at (2,4);\coordinate(O) at (3,1);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoReponse] (O) circle (3.16227766);\draw[geoAide] (3,-2.3)--(3,4.7) (-.5,2.75)--(6.5,-.75);\fill[otGreenDark] (O) circle (2pt);\node[anchor=east,text=otInk,inner sep=4pt] at (0,0) {$ A $};
\node[anchor=west,text=otInk,inner sep=4pt] at (6,0) {$ B $};
\node[anchor=south,text=otInk,inner sep=4pt] at (2,4) {$ C $};
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (3.4,1.4) {$ O $};

\end{tikzpicture}
""",
'r30_hauteur_exterieure_corrige': r"""
\begin{tikzpicture}
\coordinate(A) at (-2,3);\coordinate(B) at (0,0);\coordinate(C) at (6,0);\coordinate(H) at (-2,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoAide] (H)--(B);\draw[geoReponse] (A)--(H);\angledroit{A}{H}{C}\node[anchor=south,text=otInk,inner sep=4pt] at (-2,3) {$ A $};
\node[anchor=north,text=otInk,inner sep=4pt] at (0,0) {$ B $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (6,0) {$ C $};
\node[anchor=north,text=otInk,inner sep=4pt] at (-2,0) {$ H $};
\node[anchor=east,text=otGreenDark,inner sep=4pt] at (-2.3,1.5) {$ 3\text{ cm} $};
\node[anchor=north,text=otInk,inner sep=4pt] at (3,-0.6) {$ 6\text{ cm} $};
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (3,2.2) {$ \mathcal A=9\text{ cm}^2 $};

\end{tikzpicture}
""",
'r30_angle_exterieur_enonce': r"""
\begin{tikzpicture}
\coordinate(A) at (0,2.6686097433229325);\coordinate(B) at (-1.8,0);\coordinate(C) at (1.8,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoTrait] (1.8,0)--(3.6,0);\codage{A}{B}\codage{A}{C}\node[anchor=south,text=otInk,inner sep=4pt] at (0,2.6686097433229325) {$ A $};
\node[anchor=north east,text=otInk,inner sep=4pt] at (-1.8,0) {$ B $};
\node[anchor=north,text=otInk,inner sep=4pt] at (1.8,0) {$ C $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (3.6,0) {$ D $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (2.35,1) {$ 124^\circ $};

\end{tikzpicture}
""",
'r30_angle_exterieur_corrige': r"""
\begin{tikzpicture}
\coordinate(A) at (0,2.6686097433229325);\coordinate(B) at (-1.8,0);\coordinate(C) at (1.8,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoTrait] (1.8,0)--(3.6,0);\codage{A}{B}\codage{A}{C}\node[anchor=south,text=otInk,inner sep=4pt] at (0,2.6686097433229325) {$ A $};
\node[anchor=north east,text=otInk,inner sep=4pt] at (-1.8,0) {$ B $};
\node[anchor=north,text=otInk,inner sep=4pt] at (1.8,0) {$ C $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (3.6,0) {$ D $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (2.35,1) {$ 124^\circ $};
\node[anchor=center,text=otGreenDark,inner sep=4pt] at (0,1.8186097433229325) {$ 68^\circ $};
\node[anchor=center,text=otGreenDark,inner sep=4pt] at (-1.05,0.4) {$ 56^\circ $};
\node[anchor=center,text=otGreenDark,inner sep=4pt] at (1.05,0.4) {$ 56^\circ $};

\end{tikzpicture}
""",
'r30_construction_5_35_45': r"""
\begin{tikzpicture}
\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at (2.9408174517711623,2.0591825482288373);\coordinate(O) at (2.5,-0.4408174517711628);\draw[otGreenDark!70,line width=.7pt] (O) circle (2.5385665297143625);\draw[geoTrait] (A)--(B)--(C)--cycle;\fill[otGreenDark] (O) circle (2pt);\node[anchor=east,text=otInk,inner sep=4pt] at (0,0) {$ A $};
\node[anchor=west,text=otInk,inner sep=4pt] at (5,0) {$ B $};
\node[anchor=south,text=otInk,inner sep=4pt] at (2.9408174517711623,2.0591825482288373) {$ C $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (2.5,-0.4408174517711628) {$ O $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.5,-3.379383981485525) {$ AB=5\text{ cm} $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (1.0490886458230497,0.33077637945470045) {$ 35^\circ $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (3.983732514237585,0.4209517756015989) {$ 45^\circ $};
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (2.9408174517711623,2.6591825482288374) {$ 100^\circ $};

\end{tikzpicture}
""",
'r30_mediane_8_3': r"""
\begin{tikzpicture}
\begin{scope}[x=0.65cm,y=0.65cm]\coordinate(B) at (0,0);\coordinate(C) at (8,0);\coordinate(A) at (2.6666666666666665,3);\coordinate(H) at (2.6666666666666665,0);\coordinate(M) at (4.0,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoAide] (A)--(H);\draw[geoReponse] (A)--(M);\angledroit{A}{H}{C}\codage{B}{M}\codage{M}{C}\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ B $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (8,0) {$ C $};
\node[anchor=south,text=otInk,inner sep=4pt] at (2.6666666666666665,3) {$ A $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.6666666666666665,0) {$ H $};
\node[anchor=north,text=otInk,inner sep=4pt] at (4.0,0) {$ M $};
\end{scope}
\end{tikzpicture}
""",
'r30_mediane_14_3': r"""
\begin{tikzpicture}
\begin{scope}[x=0.42857142857142855cm,y=0.42857142857142855cm]\coordinate(B) at (0,0);\coordinate(C) at (14,0);\coordinate(A) at (4.666666666666667,3);\coordinate(H) at (4.666666666666667,0);\coordinate(M) at (7.0,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoAide] (A)--(H);\draw[geoReponse] (A)--(M);\angledroit{A}{H}{C}\codage{B}{M}\codage{M}{C}\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ B $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (14,0) {$ C $};
\node[anchor=south,text=otInk,inner sep=4pt] at (4.666666666666667,3) {$ A $};
\node[anchor=north,text=otInk,inner sep=4pt] at (4.666666666666667,0) {$ H $};
\node[anchor=north,text=otInk,inner sep=4pt] at (7.0,0) {$ M $};
\end{scope}
\end{tikzpicture}
""",
'r30_construction_5_60_45': r"""
\begin{tikzpicture}
\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at (1.8301270189221932,3.169872981077806);\coordinate(O) at (2.5,0.6698729810778062);\draw[otGreenDark!70,line width=.7pt] (O) circle (2.5881904510252074);\draw[geoTrait] (A)--(B)--(C)--cycle;\fill[otGreenDark] (O) circle (2pt);\node[anchor=east,text=otInk,inner sep=4pt] at (0,0) {$ A $};
\node[anchor=west,text=otInk,inner sep=4pt] at (5,0) {$ B $};
\node[anchor=south,text=otInk,inner sep=4pt] at (1.8301270189221932,3.169872981077806) {$ C $};
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (2.5,0.6698729810778062) {$ O $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.5,-2.318317469947401) {$ AB=5\text{ cm} $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (0.9526279441628827,0.5499999999999999) {$ 60^\circ $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (3.983732514237585,0.4209517756015989) {$ 45^\circ $};
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (1.8301270189221932,3.769872981077806) {$ 75^\circ $};

\end{tikzpicture}
""",
'r30_construction_6_35_50': r"""
\begin{tikzpicture}
\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at (3.149519229519842,2.2053171062462305);\coordinate(O) at (2.5,-0.2187216588148097);\draw[otGreenDark!70,line width=.7pt] (O) circle (2.5095495938583685);\draw[geoTrait] (A)--(B)--(C)--cycle;\fill[otGreenDark] (O) circle (2pt);\node[anchor=east,text=otInk,inner sep=4pt] at (0,0) {$ A $};
\node[anchor=west,text=otInk,inner sep=4pt] at (5,0) {$ B $};
\node[anchor=south,text=otInk,inner sep=4pt] at (3.149519229519842,2.2053171062462305) {$ C $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (2.5,-0.2187216588148097) {$ O $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.5,-3.128271252673178) {$ AB=6\text{ cm} $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (1.0490886458230497,0.33077637945470045) {$ 35^\circ $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (4.003061434259685,0.4648800879147695) {$ 50^\circ $};
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (3.149519229519842,2.8053171062462305) {$ 95^\circ $};

\end{tikzpicture}
""",
'r30_mediane_8_4': r"""
\begin{tikzpicture}
\begin{scope}[x=0.65cm,y=0.65cm]\coordinate(B) at (0,0);\coordinate(C) at (8,0);\coordinate(A) at (2.6666666666666665,4);\coordinate(H) at (2.6666666666666665,0);\coordinate(M) at (4.0,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoAide] (A)--(H);\draw[geoReponse] (A)--(M);\angledroit{A}{H}{C}\codage{B}{M}\codage{M}{C}\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ B $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (8,0) {$ C $};
\node[anchor=south,text=otInk,inner sep=4pt] at (2.6666666666666665,4) {$ A $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.6666666666666665,0) {$ H $};
\node[anchor=north,text=otInk,inner sep=4pt] at (4.0,0) {$ M $};
\end{scope}
\end{tikzpicture}
""",
'r30_construction_6_50_50': r"""
\begin{tikzpicture}
\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at (2.5,2.979383981485525);\coordinate(O) at (2.5,0.4408174517711626);\draw[otGreenDark!70,line width=.7pt] (O) circle (2.5385665297143625);\draw[geoTrait] (A)--(B)--(C)--cycle;\fill[otGreenDark] (O) circle (2pt);\node[anchor=east,text=otInk,inner sep=4pt] at (0,0) {$ A $};
\node[anchor=west,text=otInk,inner sep=4pt] at (5,0) {$ B $};
\node[anchor=south,text=otInk,inner sep=4pt] at (2.5,2.979383981485525) {$ C $};
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (2.5,0.4408174517711626) {$ O $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.5,-2.4977490779431997) {$ AB=6\text{ cm} $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (0.996938565740315,0.4648800879147694) {$ 50^\circ $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (4.003061434259685,0.4648800879147695) {$ 50^\circ $};
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (2.5,3.5793839814855253) {$ 80^\circ $};

\end{tikzpicture}
""",
'r30_mediane_14_4': r"""
\begin{tikzpicture}
\begin{scope}[x=0.42857142857142855cm,y=0.42857142857142855cm]\coordinate(B) at (0,0);\coordinate(C) at (14,0);\coordinate(A) at (4.666666666666667,4);\coordinate(H) at (4.666666666666667,0);\coordinate(M) at (7.0,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoAide] (A)--(H);\draw[geoReponse] (A)--(M);\angledroit{A}{H}{C}\codage{B}{M}\codage{M}{C}\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ B $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (14,0) {$ C $};
\node[anchor=south,text=otInk,inner sep=4pt] at (4.666666666666667,4) {$ A $};
\node[anchor=north,text=otInk,inner sep=4pt] at (4.666666666666667,0) {$ H $};
\node[anchor=north,text=otInk,inner sep=4pt] at (7.0,0) {$ M $};
\end{scope}
\end{tikzpicture}
""",
'r30_construction_6_60_50': r"""
\begin{tikzpicture}
\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at (2.0380186727397622,3.5299518879593554);\coordinate(O) at (2.5,0.9099255856655057);\draw[otGreenDark!70,line width=.7pt] (O) circle (2.6604444311897804);\draw[geoTrait] (A)--(B)--(C)--cycle;\fill[otGreenDark] (O) circle (2pt);\node[anchor=east,text=otInk,inner sep=4pt] at (0,0) {$ A $};
\node[anchor=west,text=otInk,inner sep=4pt] at (5,0) {$ B $};
\node[anchor=south,text=otInk,inner sep=4pt] at (2.0380186727397622,3.5299518879593554) {$ C $};
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (2.5,0.9099255856655057) {$ O $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.5,-2.1505188455242745) {$ AB=6\text{ cm} $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (0.9526279441628827,0.5499999999999999) {$ 60^\circ $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (4.003061434259685,0.4648800879147695) {$ 50^\circ $};
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (2.0380186727397622,4.129951887959355) {$ 70^\circ $};

\end{tikzpicture}
""",
'r30_construction_7_35_55': r"""
\begin{tikzpicture}
\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at (3.355050358314172,2.349231551964771);\coordinate(O) at (2.5,0.0);\draw[otGreenDark!70,line width=.7pt] (O) circle (2.5);\draw[geoTrait] (A)--(B)--(C)--cycle;\fill[otGreenDark] (O) circle (2pt);\node[anchor=east,text=otInk,inner sep=4pt] at (0,0) {$ A $};
\node[anchor=west,text=otInk,inner sep=4pt] at (5,0) {$ B $};
\node[anchor=south,text=otInk,inner sep=4pt] at (3.355050358314172,2.349231551964771) {$ C $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (2.5,0.0) {$ O $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.5,-2.9) {$ AB=7\text{ cm} $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (1.0490886458230497,0.33077637945470045) {$ 35^\circ $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (4.024288083503956,0.5079234745585374) {$ 55^\circ $};
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (3.355050358314172,2.949231551964771) {$ 90^\circ $};

\end{tikzpicture}
""",
'r30_mediane_8_5': r"""
\begin{tikzpicture}
\begin{scope}[x=0.65cm,y=0.65cm]\coordinate(B) at (0,0);\coordinate(C) at (8,0);\coordinate(A) at (2.6666666666666665,5);\coordinate(H) at (2.6666666666666665,0);\coordinate(M) at (4.0,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoAide] (A)--(H);\draw[geoReponse] (A)--(M);\angledroit{A}{H}{C}\codage{B}{M}\codage{M}{C}\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ B $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (8,0) {$ C $};
\node[anchor=south,text=otInk,inner sep=4pt] at (2.6666666666666665,5) {$ A $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.6666666666666665,0) {$ H $};
\node[anchor=north,text=otInk,inner sep=4pt] at (4.0,0) {$ M $};
\end{scope}
\end{tikzpicture}
""",
'r30_construction_7_50_55': r"""
\begin{tikzpicture}
\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at (2.7255756611314985,3.2482145860408025);\coordinate(O) at (2.5,0.669872981077807);\draw[otGreenDark!70,line width=.7pt] (O) circle (2.588190451025208);\draw[geoTrait] (A)--(B)--(C)--cycle;\fill[otGreenDark] (O) circle (2pt);\node[anchor=east,text=otInk,inner sep=4pt] at (0,0) {$ A $};
\node[anchor=west,text=otInk,inner sep=4pt] at (5,0) {$ B $};
\node[anchor=south,text=otInk,inner sep=4pt] at (2.7255756611314985,3.2482145860408025) {$ C $};
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (2.5,0.669872981077807) {$ O $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.5,-2.318317469947401) {$ AB=7\text{ cm} $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (0.996938565740315,0.4648800879147694) {$ 50^\circ $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (4.024288083503956,0.5079234745585374) {$ 55^\circ $};
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (2.7255756611314985,3.8482145860408026) {$ 75^\circ $};

\end{tikzpicture}
""",
'r30_mediane_14_5': r"""
\begin{tikzpicture}
\begin{scope}[x=0.42857142857142855cm,y=0.42857142857142855cm]\coordinate(B) at (0,0);\coordinate(C) at (14,0);\coordinate(A) at (4.666666666666667,5);\coordinate(H) at (4.666666666666667,0);\coordinate(M) at (7.0,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoAide] (A)--(H);\draw[geoReponse] (A)--(M);\angledroit{A}{H}{C}\codage{B}{M}\codage{M}{C}\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ B $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (14,0) {$ C $};
\node[anchor=south,text=otInk,inner sep=4pt] at (4.666666666666667,5) {$ A $};
\node[anchor=north,text=otInk,inner sep=4pt] at (4.666666666666667,0) {$ H $};
\node[anchor=north,text=otInk,inner sep=4pt] at (7.0,0) {$ M $};
\end{scope}
\end{tikzpicture}
""",
'r30_construction_7_60_55': r"""
\begin{tikzpicture}
\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at (2.259585694853647,3.9137172275423406);\coordinate(O) at (2.5,1.165769145387496);\draw[otGreenDark!70,line width=.7pt] (O) circle (2.7584447974062294);\draw[geoTrait] (A)--(B)--(C)--cycle;\fill[otGreenDark] (O) circle (2pt);\node[anchor=east,text=otInk,inner sep=4pt] at (0,0) {$ A $};
\node[anchor=west,text=otInk,inner sep=4pt] at (5,0) {$ B $};
\node[anchor=south,text=otInk,inner sep=4pt] at (2.259585694853647,3.9137172275423406) {$ C $};
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (2.5,1.165769145387496) {$ O $};
\node[anchor=north,text=otInk,inner sep=4pt] at (2.5,-1.9926756520187334) {$ AB=7\text{ cm} $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (0.9526279441628827,0.5499999999999999) {$ 60^\circ $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (4.024288083503956,0.5079234745585374) {$ 55^\circ $};
\node[anchor=south,text=otGreenDark,inner sep=4pt] at (2.259585694853647,4.51371722754234) {$ 65^\circ $};

\end{tikzpicture}
""",
}
