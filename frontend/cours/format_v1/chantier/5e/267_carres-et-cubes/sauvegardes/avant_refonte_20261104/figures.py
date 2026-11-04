# -*- coding: utf-8 -*-
"""Figures TikZ originales, palette et polices communes du chantier."""
FIGURES = {
'cours_modele': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (2.2,2.2);
\draw[otNavy!55,line width=.4pt] (0.00000,0)--(0.00000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.00000)--(2.2,0.00000);
\draw[otNavy!55,line width=.4pt] (0.73333,0)--(0.73333,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.73333)--(2.2,0.73333);
\draw[otNavy!55,line width=.4pt] (1.46667,0)--(1.46667,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.46667)--(2.2,1.46667);
\draw[otNavy!55,line width=.4pt] (2.20000,0)--(2.20000,2.2);
\draw[otNavy!55,line width=.4pt] (0,2.20000)--(2.2,2.20000);
\node[anchor=south] at (1.1,2.45) {3 carreaux de côté};
\draw[geoTrait] (3.4,0) rectangle (5.6,2.2);
\draw[geoTrait] (3.4,2.2)--(4.15,2.95)--(6.35,2.95)--(6.35,.75)--(5.6,0);
\draw[geoTrait] (5.6,2.2)--(6.35,2.95);
\draw[geoAide] (3.4,0)--(4.15,.75)--(6.35,.75);
\draw[geoAide] (4.15,.75)--(4.15,2.95);
\node[anchor=north] at (4.5,-.2) {3 cubes par arête};
\node[anchor=north,text=otMuted] at (1.1,-.2) {Une couche du cube};
\end{tikzpicture}""",
'carre_cube_2': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (2.2,2.2);
\draw[otNavy!55,line width=.4pt] (0.00000,0)--(0.00000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.00000)--(2.2,0.00000);
\draw[otNavy!55,line width=.4pt] (1.10000,0)--(1.10000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.10000)--(2.2,1.10000);
\draw[otNavy!55,line width=.4pt] (2.20000,0)--(2.20000,2.2);
\draw[otNavy!55,line width=.4pt] (0,2.20000)--(2.2,2.20000);
\node[anchor=south] at (1.1,2.45) {2 carreaux de côté};
\draw[geoTrait] (3.4,0) rectangle (5.6,2.2);
\draw[geoTrait] (3.4,2.2)--(4.15,2.95)--(6.35,2.95)--(6.35,.75)--(5.6,0);
\draw[geoTrait] (5.6,2.2)--(6.35,2.95);
\draw[geoAide] (3.4,0)--(4.15,.75)--(6.35,.75);
\draw[geoAide] (4.15,.75)--(4.15,2.95);
\node[anchor=north] at (4.5,-.2) {2 cubes par arête};
\node[anchor=north,text=otMuted] at (1.1,-.2) {Une couche du cube};
\end{tikzpicture}""",
'carre_cube_3': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (2.2,2.2);
\draw[otNavy!55,line width=.4pt] (0.00000,0)--(0.00000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.00000)--(2.2,0.00000);
\draw[otNavy!55,line width=.4pt] (0.73333,0)--(0.73333,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.73333)--(2.2,0.73333);
\draw[otNavy!55,line width=.4pt] (1.46667,0)--(1.46667,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.46667)--(2.2,1.46667);
\draw[otNavy!55,line width=.4pt] (2.20000,0)--(2.20000,2.2);
\draw[otNavy!55,line width=.4pt] (0,2.20000)--(2.2,2.20000);
\node[anchor=south] at (1.1,2.45) {3 carreaux de côté};
\draw[geoTrait] (3.4,0) rectangle (5.6,2.2);
\draw[geoTrait] (3.4,2.2)--(4.15,2.95)--(6.35,2.95)--(6.35,.75)--(5.6,0);
\draw[geoTrait] (5.6,2.2)--(6.35,2.95);
\draw[geoAide] (3.4,0)--(4.15,.75)--(6.35,.75);
\draw[geoAide] (4.15,.75)--(4.15,2.95);
\node[anchor=north] at (4.5,-.2) {3 cubes par arête};
\node[anchor=north,text=otMuted] at (1.1,-.2) {Une couche du cube};
\end{tikzpicture}""",
'carre_cube_4': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (2.2,2.2);
\draw[otNavy!55,line width=.4pt] (0.00000,0)--(0.00000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.00000)--(2.2,0.00000);
\draw[otNavy!55,line width=.4pt] (0.55000,0)--(0.55000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.55000)--(2.2,0.55000);
\draw[otNavy!55,line width=.4pt] (1.10000,0)--(1.10000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.10000)--(2.2,1.10000);
\draw[otNavy!55,line width=.4pt] (1.65000,0)--(1.65000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.65000)--(2.2,1.65000);
\draw[otNavy!55,line width=.4pt] (2.20000,0)--(2.20000,2.2);
\draw[otNavy!55,line width=.4pt] (0,2.20000)--(2.2,2.20000);
\node[anchor=south] at (1.1,2.45) {4 carreaux de côté};
\draw[geoTrait] (3.4,0) rectangle (5.6,2.2);
\draw[geoTrait] (3.4,2.2)--(4.15,2.95)--(6.35,2.95)--(6.35,.75)--(5.6,0);
\draw[geoTrait] (5.6,2.2)--(6.35,2.95);
\draw[geoAide] (3.4,0)--(4.15,.75)--(6.35,.75);
\draw[geoAide] (4.15,.75)--(4.15,2.95);
\node[anchor=north] at (4.5,-.2) {4 cubes par arête};
\node[anchor=north,text=otMuted] at (1.1,-.2) {Une couche du cube};
\end{tikzpicture}""",
'carre_cube_5': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (2.2,2.2);
\draw[otNavy!55,line width=.4pt] (0.00000,0)--(0.00000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.00000)--(2.2,0.00000);
\draw[otNavy!55,line width=.4pt] (0.44000,0)--(0.44000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.44000)--(2.2,0.44000);
\draw[otNavy!55,line width=.4pt] (0.88000,0)--(0.88000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.88000)--(2.2,0.88000);
\draw[otNavy!55,line width=.4pt] (1.32000,0)--(1.32000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.32000)--(2.2,1.32000);
\draw[otNavy!55,line width=.4pt] (1.76000,0)--(1.76000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.76000)--(2.2,1.76000);
\draw[otNavy!55,line width=.4pt] (2.20000,0)--(2.20000,2.2);
\draw[otNavy!55,line width=.4pt] (0,2.20000)--(2.2,2.20000);
\node[anchor=south] at (1.1,2.45) {5 carreaux de côté};
\draw[geoTrait] (3.4,0) rectangle (5.6,2.2);
\draw[geoTrait] (3.4,2.2)--(4.15,2.95)--(6.35,2.95)--(6.35,.75)--(5.6,0);
\draw[geoTrait] (5.6,2.2)--(6.35,2.95);
\draw[geoAide] (3.4,0)--(4.15,.75)--(6.35,.75);
\draw[geoAide] (4.15,.75)--(4.15,2.95);
\node[anchor=north] at (4.5,-.2) {5 cubes par arête};
\node[anchor=north,text=otMuted] at (1.1,-.2) {Une couche du cube};
\end{tikzpicture}""",
'carre_cube_6': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (2.2,2.2);
\draw[otNavy!55,line width=.4pt] (0.00000,0)--(0.00000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.00000)--(2.2,0.00000);
\draw[otNavy!55,line width=.4pt] (0.36667,0)--(0.36667,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.36667)--(2.2,0.36667);
\draw[otNavy!55,line width=.4pt] (0.73333,0)--(0.73333,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.73333)--(2.2,0.73333);
\draw[otNavy!55,line width=.4pt] (1.10000,0)--(1.10000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.10000)--(2.2,1.10000);
\draw[otNavy!55,line width=.4pt] (1.46667,0)--(1.46667,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.46667)--(2.2,1.46667);
\draw[otNavy!55,line width=.4pt] (1.83333,0)--(1.83333,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.83333)--(2.2,1.83333);
\draw[otNavy!55,line width=.4pt] (2.20000,0)--(2.20000,2.2);
\draw[otNavy!55,line width=.4pt] (0,2.20000)--(2.2,2.20000);
\node[anchor=south] at (1.1,2.45) {6 carreaux de côté};
\draw[geoTrait] (3.4,0) rectangle (5.6,2.2);
\draw[geoTrait] (3.4,2.2)--(4.15,2.95)--(6.35,2.95)--(6.35,.75)--(5.6,0);
\draw[geoTrait] (5.6,2.2)--(6.35,2.95);
\draw[geoAide] (3.4,0)--(4.15,.75)--(6.35,.75);
\draw[geoAide] (4.15,.75)--(4.15,2.95);
\node[anchor=north] at (4.5,-.2) {6 cubes par arête};
\node[anchor=north,text=otMuted] at (1.1,-.2) {Une couche du cube};
\end{tikzpicture}""",
'carre_cube_7': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (2.2,2.2);
\draw[otNavy!55,line width=.4pt] (0.00000,0)--(0.00000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.00000)--(2.2,0.00000);
\draw[otNavy!55,line width=.4pt] (0.31429,0)--(0.31429,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.31429)--(2.2,0.31429);
\draw[otNavy!55,line width=.4pt] (0.62857,0)--(0.62857,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.62857)--(2.2,0.62857);
\draw[otNavy!55,line width=.4pt] (0.94286,0)--(0.94286,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.94286)--(2.2,0.94286);
\draw[otNavy!55,line width=.4pt] (1.25714,0)--(1.25714,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.25714)--(2.2,1.25714);
\draw[otNavy!55,line width=.4pt] (1.57143,0)--(1.57143,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.57143)--(2.2,1.57143);
\draw[otNavy!55,line width=.4pt] (1.88571,0)--(1.88571,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.88571)--(2.2,1.88571);
\draw[otNavy!55,line width=.4pt] (2.20000,0)--(2.20000,2.2);
\draw[otNavy!55,line width=.4pt] (0,2.20000)--(2.2,2.20000);
\node[anchor=south] at (1.1,2.45) {7 carreaux de côté};
\draw[geoTrait] (3.4,0) rectangle (5.6,2.2);
\draw[geoTrait] (3.4,2.2)--(4.15,2.95)--(6.35,2.95)--(6.35,.75)--(5.6,0);
\draw[geoTrait] (5.6,2.2)--(6.35,2.95);
\draw[geoAide] (3.4,0)--(4.15,.75)--(6.35,.75);
\draw[geoAide] (4.15,.75)--(4.15,2.95);
\node[anchor=north] at (4.5,-.2) {7 cubes par arête};
\node[anchor=north,text=otMuted] at (1.1,-.2) {Une couche du cube};
\end{tikzpicture}""",
'carre_cube_8': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (2.2,2.2);
\draw[otNavy!55,line width=.4pt] (0.00000,0)--(0.00000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.00000)--(2.2,0.00000);
\draw[otNavy!55,line width=.4pt] (0.27500,0)--(0.27500,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.27500)--(2.2,0.27500);
\draw[otNavy!55,line width=.4pt] (0.55000,0)--(0.55000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.55000)--(2.2,0.55000);
\draw[otNavy!55,line width=.4pt] (0.82500,0)--(0.82500,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.82500)--(2.2,0.82500);
\draw[otNavy!55,line width=.4pt] (1.10000,0)--(1.10000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.10000)--(2.2,1.10000);
\draw[otNavy!55,line width=.4pt] (1.37500,0)--(1.37500,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.37500)--(2.2,1.37500);
\draw[otNavy!55,line width=.4pt] (1.65000,0)--(1.65000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.65000)--(2.2,1.65000);
\draw[otNavy!55,line width=.4pt] (1.92500,0)--(1.92500,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.92500)--(2.2,1.92500);
\draw[otNavy!55,line width=.4pt] (2.20000,0)--(2.20000,2.2);
\draw[otNavy!55,line width=.4pt] (0,2.20000)--(2.2,2.20000);
\node[anchor=south] at (1.1,2.45) {8 carreaux de côté};
\draw[geoTrait] (3.4,0) rectangle (5.6,2.2);
\draw[geoTrait] (3.4,2.2)--(4.15,2.95)--(6.35,2.95)--(6.35,.75)--(5.6,0);
\draw[geoTrait] (5.6,2.2)--(6.35,2.95);
\draw[geoAide] (3.4,0)--(4.15,.75)--(6.35,.75);
\draw[geoAide] (4.15,.75)--(4.15,2.95);
\node[anchor=north] at (4.5,-.2) {8 cubes par arête};
\node[anchor=north,text=otMuted] at (1.1,-.2) {Une couche du cube};
\end{tikzpicture}""",
'carre_cube_9': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (2.2,2.2);
\draw[otNavy!55,line width=.4pt] (0.00000,0)--(0.00000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.00000)--(2.2,0.00000);
\draw[otNavy!55,line width=.4pt] (0.24444,0)--(0.24444,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.24444)--(2.2,0.24444);
\draw[otNavy!55,line width=.4pt] (0.48889,0)--(0.48889,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.48889)--(2.2,0.48889);
\draw[otNavy!55,line width=.4pt] (0.73333,0)--(0.73333,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.73333)--(2.2,0.73333);
\draw[otNavy!55,line width=.4pt] (0.97778,0)--(0.97778,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.97778)--(2.2,0.97778);
\draw[otNavy!55,line width=.4pt] (1.22222,0)--(1.22222,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.22222)--(2.2,1.22222);
\draw[otNavy!55,line width=.4pt] (1.46667,0)--(1.46667,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.46667)--(2.2,1.46667);
\draw[otNavy!55,line width=.4pt] (1.71111,0)--(1.71111,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.71111)--(2.2,1.71111);
\draw[otNavy!55,line width=.4pt] (1.95556,0)--(1.95556,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.95556)--(2.2,1.95556);
\draw[otNavy!55,line width=.4pt] (2.20000,0)--(2.20000,2.2);
\draw[otNavy!55,line width=.4pt] (0,2.20000)--(2.2,2.20000);
\node[anchor=south] at (1.1,2.45) {9 carreaux de côté};
\draw[geoTrait] (3.4,0) rectangle (5.6,2.2);
\draw[geoTrait] (3.4,2.2)--(4.15,2.95)--(6.35,2.95)--(6.35,.75)--(5.6,0);
\draw[geoTrait] (5.6,2.2)--(6.35,2.95);
\draw[geoAide] (3.4,0)--(4.15,.75)--(6.35,.75);
\draw[geoAide] (4.15,.75)--(4.15,2.95);
\node[anchor=north] at (4.5,-.2) {9 cubes par arête};
\node[anchor=north,text=otMuted] at (1.1,-.2) {Une couche du cube};
\end{tikzpicture}""",
'carre_cube_10': r"""\begin{tikzpicture}
\fill[otNavy!8] (0,0) rectangle (2.2,2.2);
\draw[otNavy!55,line width=.4pt] (0.00000,0)--(0.00000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.00000)--(2.2,0.00000);
\draw[otNavy!55,line width=.4pt] (0.22000,0)--(0.22000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.22000)--(2.2,0.22000);
\draw[otNavy!55,line width=.4pt] (0.44000,0)--(0.44000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.44000)--(2.2,0.44000);
\draw[otNavy!55,line width=.4pt] (0.66000,0)--(0.66000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.66000)--(2.2,0.66000);
\draw[otNavy!55,line width=.4pt] (0.88000,0)--(0.88000,2.2);
\draw[otNavy!55,line width=.4pt] (0,0.88000)--(2.2,0.88000);
\draw[otNavy!55,line width=.4pt] (1.10000,0)--(1.10000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.10000)--(2.2,1.10000);
\draw[otNavy!55,line width=.4pt] (1.32000,0)--(1.32000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.32000)--(2.2,1.32000);
\draw[otNavy!55,line width=.4pt] (1.54000,0)--(1.54000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.54000)--(2.2,1.54000);
\draw[otNavy!55,line width=.4pt] (1.76000,0)--(1.76000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.76000)--(2.2,1.76000);
\draw[otNavy!55,line width=.4pt] (1.98000,0)--(1.98000,2.2);
\draw[otNavy!55,line width=.4pt] (0,1.98000)--(2.2,1.98000);
\draw[otNavy!55,line width=.4pt] (2.20000,0)--(2.20000,2.2);
\draw[otNavy!55,line width=.4pt] (0,2.20000)--(2.2,2.20000);
\node[anchor=south] at (1.1,2.45) {10 carreaux de côté};
\draw[geoTrait] (3.4,0) rectangle (5.6,2.2);
\draw[geoTrait] (3.4,2.2)--(4.15,2.95)--(6.35,2.95)--(6.35,.75)--(5.6,0);
\draw[geoTrait] (5.6,2.2)--(6.35,2.95);
\draw[geoAide] (3.4,0)--(4.15,.75)--(6.35,.75);
\draw[geoAide] (4.15,.75)--(4.15,2.95);
\node[anchor=north] at (4.5,-.2) {10 cubes par arête};
\node[anchor=north,text=otMuted] at (1.1,-.2) {Une couche du cube};
\end{tikzpicture}""",
}


# Figures de la révision pédagogique du 30 octobre 2026.
FIGURES.update({
'terrasse_81': r"""\begin{tikzpicture}
\fill[otGreen!10] (0,0) rectangle (3.6,3.6);
\draw[otNavy!60,line width=.45pt] (0.00,0)--(0.00,3.6) (0,0.00)--(3.6,0.00);
\draw[otNavy!60,line width=.45pt] (0.40,0)--(0.40,3.6) (0,0.40)--(3.6,0.40);
\draw[otNavy!60,line width=.45pt] (0.80,0)--(0.80,3.6) (0,0.80)--(3.6,0.80);
\draw[otNavy!60,line width=.45pt] (1.20,0)--(1.20,3.6) (0,1.20)--(3.6,1.20);
\draw[otNavy!60,line width=.45pt] (1.60,0)--(1.60,3.6) (0,1.60)--(3.6,1.60);
\draw[otNavy!60,line width=.45pt] (2.00,0)--(2.00,3.6) (0,2.00)--(3.6,2.00);
\draw[otNavy!60,line width=.45pt] (2.40,0)--(2.40,3.6) (0,2.40)--(3.6,2.40);
\draw[otNavy!60,line width=.45pt] (2.80,0)--(2.80,3.6) (0,2.80)--(3.6,2.80);
\draw[otNavy!60,line width=.45pt] (3.20,0)--(3.20,3.6) (0,3.20)--(3.6,3.20);
\draw[otNavy!60,line width=.45pt] (3.60,0)--(3.60,3.6) (0,3.60)--(3.6,3.60);
\draw[geoTrait] (0,0) rectangle (3.6,3.6);
\node[anchor=south] at (1.8,3.9) {Terrasse : $4{,}5$ m de côté};
\node[anchor=north,text=otGreenDark] at (1.8,-.25) {$9\times9=81$ dalles};
\node[anchor=west,align=left] at (4,1.8) {Une dalle :\\$0{,}5$ m de côté};
\end{tikzpicture}""",
'cube_216': r"""\begin{tikzpicture}
\fill[otGreen!10] (0,0) rectangle (2.4,2.4);
\draw[otNavy!55,line width=.4pt] (0.00,0)--(0.00,2.4) (0,0.00)--(2.4,0.00);
\draw[otNavy!55,line width=.4pt] (0.40,0)--(0.40,2.4) (0,0.40)--(2.4,0.40);
\draw[otNavy!55,line width=.4pt] (0.80,0)--(0.80,2.4) (0,0.80)--(2.4,0.80);
\draw[otNavy!55,line width=.4pt] (1.20,0)--(1.20,2.4) (0,1.20)--(2.4,1.20);
\draw[otNavy!55,line width=.4pt] (1.60,0)--(1.60,2.4) (0,1.60)--(2.4,1.60);
\draw[otNavy!55,line width=.4pt] (2.00,0)--(2.00,2.4) (0,2.00)--(2.4,2.00);
\draw[otNavy!55,line width=.4pt] (2.40,0)--(2.40,2.4) (0,2.40)--(2.4,2.40);
\draw[geoTrait] (0,0) rectangle (2.4,2.4);
\draw[geoTrait] (0,2.4)--(.8,3.2)--(3.2,3.2)--(3.2,.8)--(2.4,0);
\draw[geoTrait] (2.4,2.4)--(3.2,3.2);
\draw[geoAide] (0,0)--(.8,.8)--(3.2,.8) (.8,.8)--(.8,3.2);
\node[anchor=north] at (1.2,-.25) {$30$ cm};
\node[anchor=west,align=left] at (3.6,1.8) {Petits cubes :\\arête $5$ cm};
\node[anchor=south,text=otGreenDark] at (1.6,3.5) {$6$ cubes par arête : $6^3=216$ cubes};
\end{tikzpicture}""",
})
