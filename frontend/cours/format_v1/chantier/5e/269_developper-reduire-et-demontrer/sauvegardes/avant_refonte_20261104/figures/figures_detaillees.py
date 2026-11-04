# -*- coding: utf-8 -*-
"""Figures TikZ originales, palette et polices communes du chantier."""
FIGURES = {
'cours_modele': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {3 cm};
\node[anchor=east] at (-.2,.85) {4 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_2_2': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {2 cm};
\node[anchor=east] at (-.2,.85) {2 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_2_3': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {3 cm};
\node[anchor=east] at (-.2,.85) {2 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_2_4': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {4 cm};
\node[anchor=east] at (-.2,.85) {2 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_2_5': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {5 cm};
\node[anchor=east] at (-.2,.85) {2 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_2_6': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {6 cm};
\node[anchor=east] at (-.2,.85) {2 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_2_7': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {7 cm};
\node[anchor=east] at (-.2,.85) {2 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_2_8': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {8 cm};
\node[anchor=east] at (-.2,.85) {2 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_3_2': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {2 cm};
\node[anchor=east] at (-.2,.85) {3 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_3_3': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {3 cm};
\node[anchor=east] at (-.2,.85) {3 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_3_4': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {4 cm};
\node[anchor=east] at (-.2,.85) {3 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_3_5': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {5 cm};
\node[anchor=east] at (-.2,.85) {3 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_3_6': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {6 cm};
\node[anchor=east] at (-.2,.85) {3 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_3_7': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {7 cm};
\node[anchor=east] at (-.2,.85) {3 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_3_8': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {8 cm};
\node[anchor=east] at (-.2,.85) {3 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_4_2': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {2 cm};
\node[anchor=east] at (-.2,.85) {4 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_4_3': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {3 cm};
\node[anchor=east] at (-.2,.85) {4 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_4_4': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {4 cm};
\node[anchor=east] at (-.2,.85) {4 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_4_5': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {5 cm};
\node[anchor=east] at (-.2,.85) {4 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_4_6': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {6 cm};
\node[anchor=east] at (-.2,.85) {4 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_4_7': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {7 cm};
\node[anchor=east] at (-.2,.85) {4 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
'rectangle_4_8': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {8 cm};
\node[anchor=east] at (-.2,.85) {4 cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
}
