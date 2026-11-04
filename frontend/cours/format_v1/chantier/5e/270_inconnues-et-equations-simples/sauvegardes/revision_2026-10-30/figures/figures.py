# -*- coding: utf-8 -*-
FIGURES = {
'cours_modele': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.3000,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (3.9000,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {2\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 10\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'schema_parametre': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0,0) rectangle (3.8,1.15);
\draw[geoTrait,fill=otGreen!12] (3.8,0) rectangle (5.3,1.15);
\node[text=otNavy,align=center] at (1.9,.575) {$n$ pochettes\\à $x$ euros chacune};
\node[text=otGreenDark] at (4.55,.575) {$b$ euros};
\node[anchor=south] at (2.65,1.4) {Total : $T$ euros};
\node[anchor=north,text=otMuted] at (2.65,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
}
