# -*- coding: utf-8 -*-
"""Figures de la page « Quantité de matière, concentration et dilution ».

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/physique-chimie/quantite-de-matiere-concentration --planche --jobs 1

Valeurs des exemples de la page (calculées et vérifiées dans le texte) :
combustion du méthane avec 0,50 mol de CH4 et 0,80 mol de O2 (x_max = 0,40 mol,
O2 limitant) ; gamme d'étalonnage A = 1,2 × C (C en mmol/L), mesure A = 0,54
donc C = 0,45 mmol/L.
"""

NOTE = r"\otMedium\fontsize{9.5}{11.5}\selectfont"
PETIT = r"\otRegular\fontsize{8.5}{10}\selectfont"

PREAMBULE_EXTRA = r"""
\definecolor{cRouge}{HTML}{E53935}
\definecolor{cJaune}{HTML}{FBC02D}
\definecolor{cVert}{HTML}{43A047}
\definecolor{cCyan}{HTML}{00ACC1}
\definecolor{cBleu}{HTML}{1E40C8}
\definecolor{cMagenta}{HTML}{C2185B}
\colorlet{solMere}{otOrange!70}
\colorlet{solFille}{otOrange!28}
\colorlet{solTitrante}{otNavy!32}
\colorlet{solTitree}{otGreen!28}
"""


# ---------------------------------------------------------------- 1. tout passe par la mole
# Cadres dessinés à part (chemins), texte dans des nœuds sans fond ni bord.
DEMI_L, DEMI_H = 1.85, 1.05
SAUT = chr(92) * 2 + "[4pt]"   # retour à la ligne LaTeX « \\[4pt] »
DEBUT, FIN = chr(92) + "begin{tikzpicture}", chr(92) + "end{tikzpicture}"


def boite(x, y, titre, formule, aide):
    return (rf"  \draw[otNavy!40,fill=otSky,line width=0.8pt,rounded corners=5pt] ({x - DEMI_L},{y - DEMI_H}) rectangle ({x + DEMI_L},{y + DEMI_H});" + "\n"
            + rf"  \node[align=center,inner sep=0pt] at ({x},{y}) {{{{\color{{otNavy}}{NOTE} {titre}}}{SAUT}"
            rf"{{\large ${formule}$}}{SAUT}{{\color{{otMuted}}{PETIT} {aide}}}}};" + "\n")


def lien(x1, y1, x2, y2):
    return rf"  \draw[otNavy!55,line width=1.1pt] ({x1},{y1}) -- ({x2},{y2});" + "\n"


CARTE_MOLE = ("\n" + DEBUT + "\n"
    + r"  \draw[otNavy,fill=otNavy!10,line width=1.4pt,rounded corners=6pt] (-1.85,-0.65) rectangle (1.85,0.65);" + "\n"
    + r"  \node[align=center,text=otNavy,inner sep=0pt] at (0,0) {{\otMedium\fontsize{9.5}{11.5}\selectfont quantité de matière}" + SAUT + r"{\large $n$ en mol}};" + "\n"
    + boite(-2.05, 2.75, "Une masse", r"n = \dfrac{m}{M}", r"$m$ en g, $M$ en g/mol")
    + boite(2.05, 2.75, "Un nombre d’entités", r"n = \dfrac{N}{N_{\mathrm{A}}}", r"$N_{\mathrm{A}} = 6{,}02 \times 10^{23}$ mol$^{-1}$")
    + boite(-2.05, -2.75, "Un volume de gaz", r"n = \dfrac{V}{V_{\mathrm{m}}}", r"$V_{\mathrm{m}} \approx 24$ L/mol à 20 °C")
    + boite(2.05, -2.75, "Un soluté dissous", r"n = C \times V", r"$C$ en mol/L, $V$ en L")
    + lien(-0.95, 0.65, -1.5, 1.7) + lien(0.95, 0.65, 1.5, 1.7)
    + lien(-0.95, -0.65, -1.5, -1.7) + lien(0.95, -0.65, 1.5, -1.7)
    + FIN)


# ---------------------------------------------------------------- 2. la dilution en trois étapes
def forme_fiole(x):
    return (f"({x - 0.12},3.3) -- ({x - 0.12},1.72) .. controls ({x - 0.92},1.5) and ({x - 0.92},0) .. ({x - 0.42},0) "
            f"-- ({x + 0.42},0) .. controls ({x + 0.92},0) and ({x + 0.92},1.5) .. ({x + 0.12},1.72) -- ({x + 0.12},3.3)")


def fiole(x, niveau, couleur, bouchon=False):
    forme = forme_fiole(x)
    s = ""
    if niveau > 0:
        s += rf"  \begin{{scope}}\clip {forme} -- cycle; \fill[{couleur}] ({x - 1},0) rectangle ({x + 1},{niveau}); \end{{scope}}" + "\n"
    s += rf"  \draw[otInk,line width=0.9pt,line join=round] {forme};" + "\n"
    s += rf"  \draw[otInk,line width=0.8pt] ({x - 0.26},2.85) -- ({x + 0.26},2.85);" + "\n"
    if bouchon:
        s += rf"  \fill[otInk!70,rounded corners=1pt] ({x - 0.18},3.3) rectangle ({x + 0.18},3.56);" + "\n"
    return s


def becher(x, niveau, couleur, haut=1.45, demi=0.7):
    return (rf"  \fill[{couleur}] ({x - demi},0) rectangle ({x + demi},{niveau});" + "\n"
            + rf"  \draw[otInk,line width=0.9pt,line join=round] ({x - demi - 0.12},{haut + 0.1}) -- ({x - demi},{haut}) -- ({x - demi},0) -- ({x + demi},0) -- ({x + demi},{haut});" + "\n")


def pipette(x, bas, haut, jauge, couleur):
    ampoule = (bas + jauge) / 2 + 0.15
    return (rf"  \draw[otInk,line width=3.6pt] ({x},{bas}) -- ({x},{haut});" + "\n"
            + rf"  \draw[white,line width=2.0pt] ({x},{bas + 0.03}) -- ({x},{haut + 0.01});" + "\n"
            + rf"  \draw[{couleur},line width=2.0pt] ({x},{bas + 0.03}) -- ({x},{jauge});" + "\n"
            + rf"  \draw[otInk,line width=0.9pt,fill={couleur}] ({x},{ampoule}) ellipse (0.2 and 0.48);" + "\n"
            + rf"  \draw[otInk,line width=0.8pt] ({x - 0.2},{jauge}) -- ({x + 0.2},{jauge});" + "\n")



def numero(x, n):
    """Numéro d'étape sous un récipient (les étapes sont détaillées dans le texte)."""
    return (rf"  \draw[otNavy,line width=0.9pt,fill=white] ({x},-0.5) circle (0.25);" + "\n"
            + rf"  \node[text=otNavy,font=\otMedium\fontsize{{11}}{{12}}\selectfont,inner sep=0pt] at ({x},-0.5) {{{n}}};" + "\n")


def fleche(x1, x2, y=1.3):
    return rf"  \draw[otMuted,line width=1.1pt,-{{Stealth[length=2.6mm]}}] ({x1},{y}) -- ({x2},{y});" + "\n"


DILUTION = ("\n\\begin{tikzpicture}\n"
            + becher(0, 1.0, "solMere")
            + pipette(0.12, 0.3, 4.15, 3.6, "solMere")
            + fiole(3.0, 0.32, "solMere")
            + fiole(6.0, 2.85, "solFille", bouchon=True)
            + fleche(0.95, 1.95) + fleche(3.95, 4.95)
            + numero(0, 1) + numero(3.0, 2) + numero(6.0, 3)
            + "\\end{tikzpicture}")


# ---------------------------------------------------------------- 3. tableau d'avancement
# Colonnes : état | avancement | CH4 | O2 | CO2 | H2O
BORDS_X = [0, 1.4, 3.4, 4.85, 6.3, 7.75, 9.2]
BORDS_Y = [0, -0.72, -1.78, -2.5, -3.22, -3.94]


def centre(i):
    return (BORDS_X[i] + BORDS_X[i + 1]) / 2


def ligne_tableau(rang, cellules, couleurs=None):
    y = (BORDS_Y[rang] + BORDS_Y[rang + 1]) / 2
    s = ""
    for i, texte in enumerate(cellules):
        couleur = (couleurs or {}).get(i, "otInk")
        s += rf"  \node[text={couleur}] at ({centre(i)},{y}) {{{texte}}};" + "\n"
    return s


def tableau():
    x0, x1 = BORDS_X[0], BORDS_X[-1]
    s = "\n\\begin{tikzpicture}\n"
    # fonds : en-têtes et état final
    s += rf"  \fill[otSky] ({x0},{BORDS_Y[0]}) rectangle ({x1},{BORDS_Y[2]});" + "\n"
    s += rf"  \fill[otGreen!14] ({x0},{BORDS_Y[4]}) rectangle ({x1},{BORDS_Y[5]});" + "\n"
    # traits
    s += rf"  \draw[otMuted,line width=0.7pt] ({x0},{BORDS_Y[0]}) rectangle ({x1},{BORDS_Y[5]});" + "\n"
    for y in BORDS_Y[1:-1]:
        s += rf"  \draw[otMuted!80,line width=0.5pt] ({x0},{y}) -- ({x1},{y});" + "\n"
    # « Équation » occupe les deux premières colonnes : pas de trait entre elles sur la ligne 1.
    s += rf"  \draw[otMuted!80,line width=0.5pt] ({BORDS_X[1]},{BORDS_Y[1]}) -- ({BORDS_X[1]},{BORDS_Y[5]});" + "\n"
    s += rf"  \draw[otMuted!80,line width=0.5pt] ({BORDS_X[2]},{BORDS_Y[0]}) -- ({BORDS_X[2]},{BORDS_Y[5]});" + "\n"
    for x in BORDS_X[3:6]:
        s += rf"  \draw[otMuted!55,line width=0.45pt] ({x},{BORDS_Y[2]}) -- ({x},{BORDS_Y[5]});" + "\n"
    # ligne 1 : l'équation, chaque espèce au-dessus de sa colonne
    y = (BORDS_Y[0] + BORDS_Y[1]) / 2
    s += rf"  \node[text=otNavy,font=\otMedium\fontsize{{9.5}}{{11}}\selectfont] at ({(BORDS_X[0] + BORDS_X[2]) / 2},{y}) {{Équation}};" + "\n"
    for i, espece in zip(range(2, 6), [r"$\mathrm{CH_4}$", r"$2\,\mathrm{O_2}$", r"$\mathrm{CO_2}$", r"$2\,\mathrm{H_2O}$"]):
        s += rf"  \node[text=otInk] at ({centre(i)},{y}) {{{espece}}};" + "\n"
    for x, signe in zip(BORDS_X[3:6], [r"$+$", r"$\longrightarrow$", r"$+$"]):
        s += rf"  \node[text=otInk,inner sep=0pt] at ({x},{y}) {{{signe}}};" + "\n"
    # ligne 2 : intitulés
    y = (BORDS_Y[1] + BORDS_Y[2]) / 2
    entete = r"\otMedium\fontsize{8.5}{10.5}\selectfont"
    s += rf"  \node[text=otNavy,font={entete}] at ({centre(0)},{y}) {{État}};" + "\n"
    s += rf"  \node[text=otNavy,font={entete},align=center] at ({centre(1)},{y}) {{Avancement" + SAUT.replace("[4pt]", "[1pt]") + "(mol)};" + "\n"
    s += rf"  \node[text=otNavy,font={entete}] at ({(BORDS_X[2] + BORDS_X[6]) / 2},{y}) {{Quantités de matière (mol)}};" + "\n"
    # lignes 3 à 5
    s += ligne_tableau(2, ["initial", "$x = 0$", "0,50", "0,80", "0", "0"])
    s += ligne_tableau(3, ["en cours", "$x$", r"$0{,}50 - x$", r"$0{,}80 - 2x$", "$x$", "$2x$"])
    s += ligne_tableau(4, ["final", r"$x_{\max} = 0{,}40$", "0,10", r"\textbf{0}", "0,40", "0,80"],
                       {3: "otOrange!80!black"})
    return s + "\\end{tikzpicture}"


TABLEAU_AVANCEMENT = tableau()


# ---------------------------------------------------------------- 4. droite d'étalonnage (Beer-Lambert)
ETALONNAGE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.4cm, xmin=0, xmax=1.12, ymin=0, ymax=1.36,
  xlabel={$C$ (mmol/L)}, ylabel={$A$}, grid=major,
  xtick={0.2,0.4,0.6,0.8,1.0}, ytick={0.3,0.6,0.9,1.2},
  xticklabel style={/pgf/number format/fixed, /pgf/number format/fixed zerofill, /pgf/number format/precision=1},
  yticklabel style={/pgf/number format/fixed, /pgf/number format/fixed zerofill, /pgf/number format/precision=1}]
  \addplot[courbe, domain=0:1.08] {1.2*x};
  \addplot[only marks, mark=*, mark size=2.3pt, mark options={fill=otNavy, draw=white, line width=0.6pt}]
    coordinates {(0.2,0.24) (0.4,0.48) (0.6,0.72) (0.8,0.96) (1.0,1.2)};
  \draw[seuil] (axis cs:0,0.54) -- (axis cs:0.45,0.54) -- (axis cs:0.45,0);
  \fill[otOrange!85!black] (axis cs:0.45,0.54) circle (2.6pt);
  \node[etiq, text=otOrange!80!black, anchor=north west] at (axis cs:0.49,0.47) {mesure : $A = 0{,}54$};
  \node[etiq, text=otNavy, anchor=north west] at (axis cs:0.86,0.92) {$A = k \times C$};
\end{axis}
\end{tikzpicture}"""


# ---------------------------------------------------------------- 5. cercle chromatique
SECTEURS = [(90, "cRouge", "rouge", "south"), (30, "cJaune", "jaune", "south west"),
            (-30, "cVert", "vert", "north west"), (-90, "cCyan", "cyan", "north"),
            (-150, "cBleu", "bleu", "north east"), (150, "cMagenta", "magenta", "south east")]


def cercle():
    s = "\n\\begin{tikzpicture}\n"
    for a, couleur, nom, ancre in SECTEURS:
        s += rf"  \fill[{couleur}] (0,0) -- ({a - 30}:1.45) arc[start angle={a - 30}, end angle={a + 30}, radius=1.45] -- cycle;" + "\n"
    for a, *_ in SECTEURS:
        s += rf"  \draw[white,line width=1.6pt] (0,0) -- ({a + 30}:1.47);" + "\n"
    s += r"  \fill[white] (0,0) circle (0.42);" + "\n"
    for a, couleur, nom, ancre in SECTEURS:
        s += rf"  \node[anchor={ancre},font=\otMedium\fontsize{{10}}{{12}}\selectfont,text=otInk,inner sep=2pt] at ({a}:1.55) {{{nom}}};" + "\n"
    return s + "\\end{tikzpicture}"


CERCLE_CHROMATIQUE = cercle()


# ---------------------------------------------------------------- 6. montage de titrage
def montage_titrage():
    s = "\n\\begin{tikzpicture}\n"
    # burette : tube gradué, robinet, pointe
    s += r"  \fill[solTitrante] (-0.14,2.35) rectangle (0.14,5.75);" + "\n"
    s += r"  \draw[otInk,line width=0.9pt,line join=round] (-0.14,6.25) -- (-0.14,2.35) -- (-0.05,2.12) -- (-0.05,1.62);" + "\n"
    s += r"  \draw[otInk,line width=0.9pt,line join=round] (0.14,6.25) -- (0.14,2.35) -- (0.05,2.12) -- (0.05,1.62);" + "\n"
    for k in range(12):
        y = round(2.6 + 0.3 * k, 2)
        long = 0.11 if k % 2 == 0 else 0.06
        s += rf"  \draw[otInk!70,line width=0.45pt] (-0.14,{y}) -- ({-0.14 + long},{y});" + "\n"
    s += r"  \fill[otInk!75,rounded corners=1pt] (-0.12,1.86) rectangle (0.12,2.02);" + "\n"
    s += r"  \draw[otInk!75,line width=1.4pt,line cap=round] (0.12,1.94) -- (0.42,1.94);" + "\n"
    # bécher, solution titrée, barreau aimanté, agitateur
    s += becher(0, 0.95, "solTitree", haut=1.45, demi=0.8).replace("(0.8,0)", "(0.8,0.34)").replace("(-0.8,0)", "(-0.8,0.34)")
    s += r"  \fill[otInk!75,rounded corners=1.5pt] (-0.24,0.4) rectangle (0.24,0.5);" + "\n"
    s += r"  \draw[otMuted,line width=0.8pt,fill=otRule!70,rounded corners=3pt] (-1.15,-0.32) rectangle (1.15,0.34);" + "\n"
    s += r"  \fill[otMuted] (0.78,0.01) circle (0.09);" + "\n"
    # légendes à droite (traits de rappel qui s'arrêtent avant le texte)
    rappel = r"otMuted,line width=0.55pt"
    s += rf"  \draw[{rappel}] (0.22,4.4) -- (1.0,4.4);" + "\n"
    s += rf"  \node[anchor=west,align=left,font={NOTE},text=otInk] at (1.05,4.4) {{burette graduée :\\solution titrante,\\$C_{{\mathrm{{B}}}}$ connue}};" + "\n"
    s += rf"  \draw[{rappel}] (0.88,1.05) -- (1.35,1.05);" + "\n"
    s += rf"  \node[anchor=west,align=left,font={NOTE},text=otInk] at (1.4,1.05) {{bécher : solution\\titrée, $V_{{\mathrm{{A}}}}$ connu}};" + "\n"
    s += rf"  \draw[{rappel}] (1.15,-0.05) -- (1.35,-0.05);" + "\n"
    s += rf"  \node[anchor=west,font={NOTE},text=otInk] at (1.4,-0.05) {{agitateur magnétique}};" + "\n"
    return s + "\\end{tikzpicture}"


MONTAGE_TITRAGE = montage_titrage()


FIGURES = {
    "carte_mole": CARTE_MOLE,
    "dilution": DILUTION,
    "tableau_avancement": TABLEAU_AVANCEMENT,
    "etalonnage_beer_lambert": ETALONNAGE,
    "cercle_chromatique": CERCLE_CHROMATIQUE,
    "montage_titrage": MONTAGE_TITRAGE,
}
