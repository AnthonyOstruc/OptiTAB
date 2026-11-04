# -*- coding: utf-8 -*-
"""Figures TikZ originales, palette et polices communes du chantier."""
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
'facture_2_2_10': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.3000,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (3.9000,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {2\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 10\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_3_2_17': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (1.7333,.8);
\node[text=otNavy] at (0.8667,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (1.7333,0) rectangle (3.4667,.8);
\node[text=otNavy] at (2.6000,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (3.4667,0) rectangle (5.2000,.8);
\node[text=otNavy] at (4.3333,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {2\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 17\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_4_2_26': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (1.3000,.8);
\node[text=otNavy] at (0.6500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (1.3000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.9500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (3.9000,.8);
\node[text=otNavy] at (3.2500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (3.9000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (4.5500,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {2\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 26\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_2_2_16': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.3000,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (3.9000,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {2\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 16\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_4_2_38': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (1.3000,.8);
\node[text=otNavy] at (0.6500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (1.3000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.9500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (3.9000,.8);
\node[text=otNavy] at (3.2500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (3.9000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (4.5500,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {2\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 38\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_2_3_13': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.3000,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (3.9000,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {3\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 13\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_3_3_21': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (1.7333,.8);
\node[text=otNavy] at (0.8667,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (1.7333,0) rectangle (3.4667,.8);
\node[text=otNavy] at (2.6000,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (3.4667,0) rectangle (5.2000,.8);
\node[text=otNavy] at (4.3333,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {3\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 21\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_4_3_31': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (1.3000,.8);
\node[text=otNavy] at (0.6500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (1.3000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.9500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (3.9000,.8);
\node[text=otNavy] at (3.2500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (3.9000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (4.5500,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {3\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 31\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_2_3_19': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.3000,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (3.9000,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {3\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 19\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_4_3_43': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (1.3000,.8);
\node[text=otNavy] at (0.6500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (1.3000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.9500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (3.9000,.8);
\node[text=otNavy] at (3.2500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (3.9000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (4.5500,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {3\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 43\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_2_4_16': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.3000,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (3.9000,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {4\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 16\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_3_4_25': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (1.7333,.8);
\node[text=otNavy] at (0.8667,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (1.7333,0) rectangle (3.4667,.8);
\node[text=otNavy] at (2.6000,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (3.4667,0) rectangle (5.2000,.8);
\node[text=otNavy] at (4.3333,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {4\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 25\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_4_4_36': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (1.3000,.8);
\node[text=otNavy] at (0.6500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (1.3000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.9500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (3.9000,.8);
\node[text=otNavy] at (3.2500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (3.9000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (4.5500,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {4\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 36\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_2_4_22': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.3000,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (3.9000,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {4\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 22\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
'facture_4_4_48': r"""\begin{tikzpicture}
\draw[geoTrait,fill=otNavy!8] (0.0000,0) rectangle (1.3000,.8);
\node[text=otNavy] at (0.6500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (1.3000,0) rectangle (2.6000,.8);
\node[text=otNavy] at (1.9500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (2.6000,0) rectangle (3.9000,.8);
\node[text=otNavy] at (3.2500,.4) {$x$};
\draw[geoTrait,fill=otNavy!8] (3.9000,0) rectangle (5.2000,.8);
\node[text=otNavy] at (4.5500,.4) {$x$};
\draw[geoTrait,fill=otGreen!12] (5.2,0) rectangle (6.3,.8);
\node[text=otGreenDark] at (5.75,.4) {4\,\text{€}};
\node[anchor=south] at (3.15,1.1) {Total : 48\,\text{€}};
\node[anchor=north,text=otMuted] at (2.6,-.2) {Pochettes identiques};
\end{tikzpicture}""",
}
