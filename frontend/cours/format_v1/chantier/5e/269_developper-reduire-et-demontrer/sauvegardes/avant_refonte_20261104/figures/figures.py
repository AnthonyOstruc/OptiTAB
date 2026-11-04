# -*- coding: utf-8 -*-
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
'schema_parametre': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (3,1.7);
\fill[otGreen!12] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south,text=otNavy] at (1.5,1.9) {$x$ cm};
\node[anchor=south,text=otGreenDark] at (3.8,1.9) {$b$ cm};
\node[anchor=east] at (-.2,.85) {$k$ cm};
\node[anchor=north,text=otMuted] at (2.3,-.25) {Schéma non à l'échelle};
\end{tikzpicture}""",
}


# Figures de la révision pédagogique du 30 octobre 2026.
FIGURES.update({
'rectangle_aires_corrige': r"""\begin{tikzpicture}
\fill[otGreen!12] (0,0) rectangle (3,1.7);
\fill[otGreen!20] (3,0) rectangle (4.6,1.7);
\draw[geoTrait] (0,0) rectangle (4.6,1.7);
\draw[geoTrait] (3,0)--(3,1.7);
\node[anchor=south] at (1.5,1.9) {$x$ cm};
\node[anchor=south] at (3.8,1.9) {$b$ cm};
\node[anchor=east] at (-.2,.85) {$k$ cm};
\node[text=otGreenDark] at (1.5,.85) {$kx$};
\node[text=otGreenDark] at (3.8,.85) {$kb$};
\node[anchor=north,text=otGreenDark] at (2.3,-.25) {$k(x+b)=kx+kb$};
\end{tikzpicture}""",
})
