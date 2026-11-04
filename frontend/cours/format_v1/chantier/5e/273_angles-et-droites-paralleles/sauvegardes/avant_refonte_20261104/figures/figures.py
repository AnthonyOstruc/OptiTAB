# -*- coding: utf-8 -*-
"""Figures exactes de la révision du 30 octobre 2026."""
FIGURES={
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
'r30_angle_droit_corrige': r"""
\begin{tikzpicture}
\draw[geoTrait] (0,3)--(0,0)--(3,0);\draw[geoTrait] (0,0)--(34:3);\draw[geoReponse] (0,0)--(62:3.2);\draw[otNavy] (.22,0)--(.22,.22)--(0,.22);\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (3,0) {$ A $};
\node[anchor=south,text=otInk,inner sep=4pt] at (0,3) {$ B $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (2.4871127176651253,1.6775787104122406) {$ C $};
\node[anchor=south,text=otInk,inner sep=4pt] at (1.5023090009148508,2.8254322971485664) {$ D $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (1.3388266583482495,0.40932038661183145) {$ 34^\circ $};
\node[anchor=center,text=otGreenDark,inner sep=4pt] at (1.4720873339894882,1.6349186160502676) {$ 28^\circ $};

\end{tikzpicture}
""",
'r30_bissectrices_supplementaires_corrige': r"""
\begin{tikzpicture}
\draw[geoTrait] (-3,0)--(3,0) (0,0)--(64:3);\draw[geoReponse] (0,0)--(32:2.9) (0,0)--(122:2.9);\node[anchor=north,text=otInk,inner sep=4pt] at (3.2,0.0) {$ B $};
\node[anchor=north,text=otInk,inner sep=4pt] at (-3.2,3.9188697572715305e-16) {$ A $};
\node[anchor=south,text=otInk,inner sep=4pt] at (1.4027876697250479,2.876140948157335) {$ C $};
\node[anchor=south,text=otInk,inner sep=4pt] at (2.7137539077005632,1.6957416455462557) {$ P $};
\node[anchor=south,text=otInk,inner sep=4pt] at (-1.6957416455462555,2.7137539077005637) {$ Q $};
\node[anchor=north,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (0,-0.65) {$ \widehat{POQ}=32^\circ+58^\circ=90^\circ $};

\end{tikzpicture}
""",
'r30_reciproque_enonce': r"""
\begin{tikzpicture}
\coordinate(A) at (0.6248693519093274,1);\coordinate(B) at (-0.6248693519093274,-1);\draw[geoTrait] (-3.1,1)--(3.1,1) (-3.1,-1)--(3.1,-1) (-0.9685474954594574,-1.55)--(1.03103443065039,1.65);\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (0.6248693519093274,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (-0.6248693519093274,-1) {$ B $};
\draw[otOrange] (-0.0751306480906726,1.0) arc[start angle=180,end angle=238,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (-0.3547047200867961,0.4570132253241026) {$ 58^\circ $};
\draw[otOrange] (0.0751306480906726,-1.0) arc[start angle=0,end angle=58,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (0.354704720086796,-0.4570132253241025) {$ 58^\circ $};

\end{tikzpicture}
""",
'r30_reciproque_corrige': r"""
\begin{tikzpicture}
\coordinate(A) at (0.6248693519093274,1);\coordinate(B) at (-0.6248693519093274,-1);\draw[geoTrait] (-3.1,1)--(3.1,1) (-3.1,-1)--(3.1,-1) (-0.9685474954594574,-1.55)--(1.03103443065039,1.65);\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (0.6248693519093274,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (-0.6248693519093274,-1) {$ B $};
\draw[otOrange] (-0.0751306480906726,1.0) arc[start angle=180,end angle=238,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (-0.3547047200867961,0.4570132253241026) {$ 58^\circ $};
\draw[otOrange] (0.0751306480906726,-1.0) arc[start angle=0,end angle=58,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (0.354704720086796,-0.4570132253241025) {$ 58^\circ $};
\draw[otGreenDark] (0.2539258669460839,0.4063663326905018) arc[start angle=238,end angle=360,radius=.7];\node[anchor=center,text=otGreenDark,inner sep=4pt] at (1.1678561265852252,0.02042592800387677) {$ 122^\circ $};

\end{tikzpicture}
""",
'r30_perpendiculaires_enonce': r"""
\begin{tikzpicture}
\coordinate(A) at (1.32704482162041,1);\coordinate(B) at (-1.32704482162041,-1);\draw[geoTrait] (-3.1,1)--(3.1,1) (-3.1,-1)--(3.1,-1) (-2.056919473511636,-1.55)--(2.1896239556736763,1.65);\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (1.32704482162041,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (-1.32704482162041,-1) {$ B $};
\draw[geoTrait] (-2.4,-1.5)--(-2.4,1.6);\draw[otNavy] (-2.4,.78)--(-2.18,.78)--(-2.18,1) (-2.4,-.78)--(-2.18,-.78)--(-2.18,-1);\node[anchor=south,text=otInk,inner sep=4pt] at (-2.4,1.65) {$ (s) $};
\draw[otOrange] (2.02704482162041,1.0) arc[start angle=0,end angle=37,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (2.3891673154513535,1.3553812151737032) {$ 37^\circ $};

\end{tikzpicture}
""",
'r30_perpendiculaires_corrige': r"""
\begin{tikzpicture}
\coordinate(A) at (1.32704482162041,1);\coordinate(B) at (-1.32704482162041,-1);\draw[geoTrait] (-3.1,1)--(3.1,1) (-3.1,-1)--(3.1,-1) (-2.056919473511636,-1.55)--(2.1896239556736763,1.65);\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (1.32704482162041,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (-1.32704482162041,-1) {$ B $};
\draw[geoTrait] (-2.4,-1.5)--(-2.4,1.6);\draw[otNavy] (-2.4,.78)--(-2.18,.78)--(-2.18,1) (-2.4,-.78)--(-2.18,-.78)--(-2.18,-1);\node[anchor=south,text=otInk,inner sep=4pt] at (-2.4,1.65) {$ (s) $};
\draw[otOrange] (2.02704482162041,1.0) arc[start angle=0,end angle=37,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (2.3891673154513535,1.3553812151737032) {$ 37^\circ $};
\draw[otGreenDark] (-0.6270448216204101,-1.0) arc[start angle=0,end angle=37,radius=.7];\node[anchor=center,text=otGreenDark,inner sep=4pt] at (-0.2649223277894668,-0.6446187848262968) {$ 37^\circ $};

\end{tikzpicture}
""",
'r30_somme_paralleles_enonce': r"""
\begin{tikzpicture}
\coordinate(A) at (0.40402622583515674,1);\coordinate(B) at (-0.40402622583515674,-1);\draw[geoTrait] (-3.1,1)--(3.1,1) (-3.1,-1)--(3.1,-1) (-0.6262406500444929,-1.55)--(0.6666432726280086,1.65);\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (0.40402622583515674,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (-0.40402622583515674,-1) {$ B $};
\draw[otOrange] (0.14180161044401812,0.35097130180324887) arc[start angle=248,end angle=360,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (1.0303222777223935,0.0714779187383533) {$ 112^\circ $};
\draw[otOrange] (0.2959737741648432,-1.0) arc[start angle=0,end angle=68,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (0.52449585542649,-0.3737039481127634) {$ 68^\circ $};

\end{tikzpicture}
""",
'r30_somme_paralleles_corrige': r"""
\begin{tikzpicture}
\coordinate(A) at (0.40402622583515674,1);\coordinate(B) at (-0.40402622583515674,-1);\draw[geoTrait] (-3.1,1)--(3.1,1) (-3.1,-1)--(3.1,-1) (-0.6262406500444929,-1.55)--(0.6666432726280086,1.65);\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (0.40402622583515674,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (-0.40402622583515674,-1) {$ B $};
\draw[otOrange] (0.14180161044401812,0.35097130180324887) arc[start angle=248,end angle=360,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (1.0303222777223935,0.0714779187383533) {$ 112^\circ $};
\draw[otOrange] (0.2959737741648432,-1.0) arc[start angle=0,end angle=68,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (0.52449585542649,-0.3737039481127634) {$ 68^\circ $};
\draw[otGreenDark] (-0.2959737741648432,1.0) arc[start angle=180,end angle=248,radius=.7];\node[anchor=center,text=otGreenDark,inner sep=4pt] at (-0.52449585542649,0.37370394811276364) {$ 68^\circ $};

\end{tikzpicture}
""",
'r30_triangle_parallele_enonce': r"""
\begin{tikzpicture}
\draw[geoTrait] (0,0)--(5,0)--(3.3980617818634915,3.773929941100381)--cycle;\draw[geoTrait] (-.8,3.773929941100381)--(5.8,3.773929941100381);\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ B $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (5,0) {$ C $};
\node[anchor=south,text=otInk,inner sep=4pt] at (3.3980617818634915,3.773929941100381) {$ A $};
\node[anchor=south,text=otInk,inner sep=4pt] at (-0.8,3.773929941100381) {$ D $};
\node[anchor=south,text=otInk,inner sep=4pt] at (5.8,3.773929941100381) {$ E $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (0.8221909118783408,0.3660629787682202) {$ 48^\circ $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (4.249502760139548,0.49674328678085244) {$ 67^\circ $};

\end{tikzpicture}
""",
'r30_triangle_parallele_corrige': r"""
\begin{tikzpicture}
\draw[geoTrait] (0,0)--(5,0)--(3.3980617818634915,3.773929941100381)--cycle;\draw[geoTrait] (-.8,3.773929941100381)--(5.8,3.773929941100381);\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ B $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (5,0) {$ C $};
\node[anchor=south,text=otInk,inner sep=4pt] at (3.3980617818634915,3.773929941100381) {$ A $};
\node[anchor=south,text=otInk,inner sep=4pt] at (-0.8,3.773929941100381) {$ D $};
\node[anchor=south,text=otInk,inner sep=4pt] at (5.8,3.773929941100381) {$ E $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (0.8221909118783408,0.3660629787682202) {$ 48^\circ $};
\node[anchor=center,text=otOrange,inner sep=4pt] at (4.249502760139548,0.49674328678085244) {$ 67^\circ $};
\node[anchor=center,text=otGreenDark,inner sep=4pt] at (3.3980617818634915,2.923929941100381) {$ 65^\circ $};
\node[anchor=center,text=otGreenDark,inner sep=4pt] at (2.3931617784566304,3.326519633717001) {$ 48^\circ $};
\node[anchor=center,text=otGreenDark,inner sep=4pt] at (4.315336186137377,3.166799257257117) {$ 67^\circ $};

\end{tikzpicture}
""",
'r30_bissectrice_corrige': r"""
\begin{tikzpicture}
\draw[geoTrait] (0,0)--(3.1,0) (0,0)--(70:3.1);\draw[otOrange] (1.7,0) arc[start angle=0,end angle=70,radius=1.7];\draw[geoReponse] (0,0)--(1.884049701864681,1.3192258036074058);\draw[otGreenDark!65] (2.28270486101322,1.197783811299705) arc[start angle=64.0577345615529,end angle=100.0577345615529,radius=1.3320026327526848];\draw[otGreenDark!65] (1.7343106743149992,0.9303140950669114) arc[start angle=-30.057734561552888,end angle=5.942265438447112,radius=1.3320026327526848];\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ O $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (3.1,0) {$ A $};
\node[anchor=south,text=otInk,inner sep=4pt] at (1.0602624443095734,2.913047124436316) {$ B $};
\node[anchor=north,text=otInk,inner sep=4pt] at (1.7,0) {$ M $};
\node[anchor=south east,text=otInk,inner sep=4pt] at (0.5814342436536369,1.597477455336044) {$ N $};
\node[anchor=south west,text=otGreenDark,inner sep=4pt] at (1.884049701864681,1.3192258036074058) {$ P $};

\end{tikzpicture}
""",
'r30_rosace_30': r"""
\begin{tikzpicture}
\coordinate(O) at (0,0);\coordinate(A) at (-3,0);\coordinate(B) at (3,0);\coordinate(C) at (210:2.6);\coordinate(D) at (30:2.6);\coordinate(E) at (195.0:2.8);\draw[geoTrait] (A)--(B) (C)--(D);\draw[geoAide] (O)--(E);\draw[otOrange] (-.7,0) arc[start angle=180,end angle=210,radius=.7];\draw[geoReponse] (.7,0) arc[start angle=0,end angle=30,radius=.7];\node[anchor=south east,inner sep=4pt] at (A) {$ A $};\node[anchor=south west,inner sep=4pt] at (B) {$ B $};\node[anchor=south east,inner sep=4pt] at (O) {$ O $};\node[anchor=north east,inner sep=4pt] at (C) {$ C $};\node[anchor=south west,inner sep=4pt] at (D) {$ D $};\node[anchor=north west,inner sep=4pt] at (E) {$ E $};\node[anchor=north,text=otOrange,inner sep=4pt] at (0,-1.7999999999999998) {$ \widehat{AOC}=30^\circ $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (0,-2.4) {$ \widehat{BOD}=30^\circ $};

\end{tikzpicture}
""",
'r30_paralleles_35': r"""
\begin{tikzpicture}
\coordinate(A) at (1.4281480067421146,1);\coordinate(B) at (-1.4281480067421146,-1);\draw[geoTrait] (-3.1,1)--(3.1,1) (-3.1,-1)--(3.1,-1) (-2.213629410450278,-1.55)--(2.356444211124489,1.65);\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (1.4281480067421146,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (-1.4281480067421146,-1) {$ B $};
\draw[otOrange] (2.128148006742115,1.0) arc[start angle=0,end angle=35,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (2.496310991580129,1.3367904954447858) {$ 35^\circ $};
\draw[otGreenDark] (-0.7281480067421147,-1.0) arc[start angle=0,end angle=35,radius=.7];\node[anchor=center,text=otGreenDark,inner sep=4pt] at (-0.3599850219041003,-0.6632095045552141) {$ 35^\circ $};

\end{tikzpicture}
""",
'r30_paralleles_45': r"""
\begin{tikzpicture}
\coordinate(A) at (1.0000000000000002,1);\coordinate(B) at (-1.0000000000000002,-1);\draw[geoTrait] (-3.1,1)--(3.1,1) (-3.1,-1)--(3.1,-1) (-1.5500000000000005,-1.55)--(1.6500000000000004,1.65);\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (1.0000000000000002,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (-1.0000000000000002,-1) {$ B $};
\draw[otOrange] (1.7000000000000002,1.0) arc[start angle=0,end angle=45,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (2.0347450764126416,1.4286054442489005) {$ 45^\circ $};
\draw[otGreenDark] (-0.30000000000000027,-1.0) arc[start angle=0,end angle=45,radius=.7];\node[anchor=center,text=otGreenDark,inner sep=4pt] at (0.03474507641264113,-0.5713945557510994) {$ 45^\circ $};

\end{tikzpicture}
""",
'r30_paralleles_55': r"""
\begin{tikzpicture}
\coordinate(A) at (0.7002075382097098,1);\coordinate(B) at (-0.7002075382097098,-1);\draw[geoTrait] (-3.1,1)--(3.1,1) (-3.1,-1)--(3.1,-1) (-1.0853216842250502,-1.55)--(1.155342438046021,1.65);\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (0.7002075382097098,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (-0.7002075382097098,-1) {$ B $};
\draw[otOrange] (1.4002075382097097,1.0) arc[start angle=0,end angle=55,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (1.6936596713693182,1.5171584468232382) {$ 55^\circ $};
\draw[otGreenDark] (-0.0002075382097098677,-1.0) arc[start angle=0,end angle=55,radius=.7];\node[anchor=center,text=otGreenDark,inner sep=4pt] at (0.29324459494989863,-0.4828415531767619) {$ 55^\circ $};

\end{tikzpicture}
""",
'r30_rosace_60': r"""
\begin{tikzpicture}
\coordinate(O) at (0,0);\coordinate(A) at (-3,0);\coordinate(B) at (3,0);\coordinate(C) at (240:2.6);\coordinate(D) at (60:2.6);\coordinate(E) at (210.0:2.8);\draw[geoTrait] (A)--(B) (C)--(D);\draw[geoAide] (O)--(E);\draw[otOrange] (-.7,0) arc[start angle=180,end angle=240,radius=.7];\draw[geoReponse] (.7,0) arc[start angle=0,end angle=60,radius=.7];\node[anchor=south east,inner sep=4pt] at (A) {$ A $};\node[anchor=south west,inner sep=4pt] at (B) {$ B $};\node[anchor=south east,inner sep=4pt] at (O) {$ O $};\node[anchor=north east,inner sep=4pt] at (C) {$ C $};\node[anchor=south west,inner sep=4pt] at (D) {$ D $};\node[anchor=north west,inner sep=4pt] at (E) {$ E $};\node[anchor=north,text=otOrange,inner sep=4pt] at (0,-2.75166604983954) {$ \widehat{AOC}=60^\circ $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (0,-3.3516660498395403) {$ \widehat{BOD}=60^\circ $};

\end{tikzpicture}
""",
'r30_rosace_35': r"""
\begin{tikzpicture}
\coordinate(O) at (0,0);\coordinate(A) at (-3,0);\coordinate(B) at (3,0);\coordinate(C) at (215:2.6);\coordinate(D) at (35:2.6);\coordinate(E) at (197.5:2.8);\draw[geoTrait] (A)--(B) (C)--(D);\draw[geoAide] (O)--(E);\draw[otOrange] (-.7,0) arc[start angle=180,end angle=215,radius=.7];\draw[geoReponse] (.7,0) arc[start angle=0,end angle=35,radius=.7];\node[anchor=south east,inner sep=4pt] at (A) {$ A $};\node[anchor=south west,inner sep=4pt] at (B) {$ B $};\node[anchor=south east,inner sep=4pt] at (O) {$ O $};\node[anchor=north east,inner sep=4pt] at (C) {$ C $};\node[anchor=south west,inner sep=4pt] at (D) {$ D $};\node[anchor=north west,inner sep=4pt] at (E) {$ E $};\node[anchor=north,text=otOrange,inner sep=4pt] at (0,-1.9912987345127198) {$ \widehat{AOC}=35^\circ $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (0,-2.59129873451272) {$ \widehat{BOD}=35^\circ $};

\end{tikzpicture}
""",
'r30_rosace_45': r"""
\begin{tikzpicture}
\coordinate(O) at (0,0);\coordinate(A) at (-3,0);\coordinate(B) at (3,0);\coordinate(C) at (225:2.6);\coordinate(D) at (45:2.6);\coordinate(E) at (202.5:2.8);\draw[geoTrait] (A)--(B) (C)--(D);\draw[geoAide] (O)--(E);\draw[otOrange] (-.7,0) arc[start angle=180,end angle=225,radius=.7];\draw[geoReponse] (.7,0) arc[start angle=0,end angle=45,radius=.7];\node[anchor=south east,inner sep=4pt] at (A) {$ A $};\node[anchor=south west,inner sep=4pt] at (B) {$ B $};\node[anchor=south east,inner sep=4pt] at (O) {$ O $};\node[anchor=north east,inner sep=4pt] at (C) {$ C $};\node[anchor=south west,inner sep=4pt] at (D) {$ D $};\node[anchor=north west,inner sep=4pt] at (E) {$ E $};\node[anchor=north,text=otOrange,inner sep=4pt] at (0,-2.3384776310850235) {$ \widehat{AOC}=45^\circ $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (0,-2.938477631085024) {$ \widehat{BOD}=45^\circ $};

\end{tikzpicture}
""",
'r30_rosace_55': r"""
\begin{tikzpicture}
\coordinate(O) at (0,0);\coordinate(A) at (-3,0);\coordinate(B) at (3,0);\coordinate(C) at (235:2.6);\coordinate(D) at (55:2.6);\coordinate(E) at (207.5:2.8);\draw[geoTrait] (A)--(B) (C)--(D);\draw[geoAide] (O)--(E);\draw[otOrange] (-.7,0) arc[start angle=180,end angle=235,radius=.7];\draw[geoReponse] (.7,0) arc[start angle=0,end angle=55,radius=.7];\node[anchor=south east,inner sep=4pt] at (A) {$ A $};\node[anchor=south west,inner sep=4pt] at (B) {$ B $};\node[anchor=south east,inner sep=4pt] at (O) {$ O $};\node[anchor=north east,inner sep=4pt] at (C) {$ C $};\node[anchor=south west,inner sep=4pt] at (D) {$ D $};\node[anchor=north west,inner sep=4pt] at (E) {$ E $};\node[anchor=north,text=otOrange,inner sep=4pt] at (0,-2.629795315151379) {$ \widehat{AOC}=55^\circ $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (0,-3.229795315151379) {$ \widehat{BOD}=55^\circ $};

\end{tikzpicture}
""",
'r30_paralleles_60': r"""
\begin{tikzpicture}
\coordinate(A) at (0.577350269189626,1);\coordinate(B) at (-0.577350269189626,-1);\draw[geoTrait] (-3.1,1)--(3.1,1) (-3.1,-1)--(3.1,-1) (-0.8948929172439203,-1.55)--(0.9526279441628828,1.65);\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (0.577350269189626,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (-0.577350269189626,-1) {$ B $};
\draw[otOrange] (1.277350269189626,1.0) arc[start angle=0,end angle=60,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (1.5472987214281972,1.56) {$ 60^\circ $};
\draw[otGreenDark] (0.122649730810374,-1.0) arc[start angle=0,end angle=60,radius=.7];\node[anchor=center,text=otGreenDark,inner sep=4pt] at (0.39259818304894545,-0.44000000000000006) {$ 60^\circ $};

\end{tikzpicture}
""",
'r30_rosace_65': r"""
\begin{tikzpicture}
\coordinate(O) at (0,0);\coordinate(A) at (-3,0);\coordinate(B) at (3,0);\coordinate(C) at (245:2.6);\coordinate(D) at (65:2.6);\coordinate(E) at (212.5:2.8);\draw[geoTrait] (A)--(B) (C)--(D);\draw[geoAide] (O)--(E);\draw[otOrange] (-.7,0) arc[start angle=180,end angle=245,radius=.7];\draw[geoReponse] (.7,0) arc[start angle=0,end angle=65,radius=.7];\node[anchor=south east,inner sep=4pt] at (A) {$ A $};\node[anchor=south west,inner sep=4pt] at (B) {$ B $};\node[anchor=south east,inner sep=4pt] at (O) {$ O $};\node[anchor=north east,inner sep=4pt] at (C) {$ C $};\node[anchor=south west,inner sep=4pt] at (D) {$ D $};\node[anchor=north west,inner sep=4pt] at (E) {$ E $};\node[anchor=north,text=otOrange,inner sep=4pt] at (0,-2.8564002462952898) {$ \widehat{AOC}=65^\circ $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (0,-3.45640024629529) {$ \widehat{BOD}=65^\circ $};

\end{tikzpicture}
""",
'r30_rosace_50': r"""
\begin{tikzpicture}
\coordinate(O) at (0,0);\coordinate(A) at (-3,0);\coordinate(B) at (3,0);\coordinate(C) at (230:2.6);\coordinate(D) at (50:2.6);\coordinate(E) at (205.0:2.8);\draw[geoTrait] (A)--(B) (C)--(D);\draw[geoAide] (O)--(E);\draw[otOrange] (-.7,0) arc[start angle=180,end angle=230,radius=.7];\draw[geoReponse] (.7,0) arc[start angle=0,end angle=50,radius=.7];\node[anchor=south east,inner sep=4pt] at (A) {$ A $};\node[anchor=south west,inner sep=4pt] at (B) {$ B $};\node[anchor=south east,inner sep=4pt] at (O) {$ O $};\node[anchor=north east,inner sep=4pt] at (C) {$ C $};\node[anchor=south west,inner sep=4pt] at (D) {$ D $};\node[anchor=north west,inner sep=4pt] at (E) {$ E $};\node[anchor=north,text=otOrange,inner sep=4pt] at (0,-2.491715552109343) {$ \widehat{AOC}=50^\circ $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (0,-3.091715552109343) {$ \widehat{BOD}=50^\circ $};

\end{tikzpicture}
""",
'r30_rosace_75': r"""
\begin{tikzpicture}
\coordinate(O) at (0,0);\coordinate(A) at (-3,0);\coordinate(B) at (3,0);\coordinate(C) at (255:2.6);\coordinate(D) at (75:2.6);\coordinate(E) at (217.5:2.8);\draw[geoTrait] (A)--(B) (C)--(D);\draw[geoAide] (O)--(E);\draw[otOrange] (-.7,0) arc[start angle=180,end angle=255,radius=.7];\draw[geoReponse] (.7,0) arc[start angle=0,end angle=75,radius=.7];\node[anchor=south east,inner sep=4pt] at (A) {$ A $};\node[anchor=south west,inner sep=4pt] at (B) {$ B $};\node[anchor=south east,inner sep=4pt] at (O) {$ O $};\node[anchor=north east,inner sep=4pt] at (C) {$ C $};\node[anchor=south west,inner sep=4pt] at (D) {$ D $};\node[anchor=north west,inner sep=4pt] at (E) {$ E $};\node[anchor=north,text=otOrange,inner sep=4pt] at (0,-3.011407148351578) {$ \widehat{AOC}=75^\circ $};
\node[anchor=north,text=otGreenDark,inner sep=4pt] at (0,-3.611407148351578) {$ \widehat{BOD}=75^\circ $};

\end{tikzpicture}
""",
'r30_paralleles_65': r"""
\begin{tikzpicture}
\coordinate(A) at (0.4663076581549986,1);\coordinate(B) at (-0.4663076581549986,-1);\draw[geoTrait] (-3.1,1)--(3.1,1) (-3.1,-1)--(3.1,-1) (-0.7227768701402478,-1.55)--(0.7694076359557476,1.65);\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,1) {$ (d) $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (-3.1,-1) {$ (e) $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (0.4663076581549986,1) {$ A $};
\node[anchor=north west,text=otInk,inner sep=4pt] at (-0.4663076581549986,-1) {$ B $};
\draw[otOrange] (1.1663076581549985,1.0) arc[start angle=0,end angle=65,radius=.7];\node[anchor=center,text=otOrange,inner sep=4pt] at (1.4109060774654307,1.6017755613484428) {$ 65^\circ $};
\draw[otGreenDark] (0.23369234184500137,-1.0) arc[start angle=0,end angle=65,radius=.7];\node[anchor=center,text=otGreenDark,inner sep=4pt] at (0.4782907611554335,-0.3982244386515573) {$ 65^\circ $};

\end{tikzpicture}
""",
}
