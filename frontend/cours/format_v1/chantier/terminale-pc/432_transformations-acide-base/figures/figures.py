# -*- coding: utf-8 -*-
"""Figures de la notion « Transformations acide-base » (Terminale, physique-chimie), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion> [nom …] [--planche]

Repris et adapté du livre OptiTAB de physique-chimie de Terminale
(livre/livre-physique/livre-pc-terminale : figures/01-transfert.tex, 01-lewis.tex,
01-echelle-ph.tex, corriges/01-acide-base.tex, réglages chemfig de pc-livre.sty).
Seules les figures indispensables sont faites (consigne du pilote) : transfert d'ion
hydrogène, schémas de Lewis, échelle de pH. Polices agrandies pour le téléphone
(figure affichée à la moitié de ses pixels : 10 pt dans la figure = texte du site).
Corrigés : ce que l'élève devait ajouter (doublets non liants, charges) en vert.
"""

PREAMBULE_EXTRA = r"""
\usepackage{graphicx}
\usepackage[version=4]{mhchem}
\usepackage{chemfig}
\usetikzlibrary{fit}
% formules chimiques en mode mathématique (Libertinus, comme MathJax sur le site)
\newcommand{\cm}[1]{\ensuremath{\ce{#1}}}
\newfontfamily\otSemi{Montserrat}[Extension=.otf, UprightFont=*-SemiBold, BoldFont=*-Bold]
\newcommand{\titreF}{\otSemi\fontsize{8}{10}\selectfont}
\newcommand{\otCaps}[2][8]{{\addfontfeature{LetterSpace=#1}\MakeUppercase{#2}}}
\definecolor{otNavyDark}{HTML}{122A66}
\colorlet{otGreenTint}{otGreen!13}
\colorlet{otNavyTint}{otNavy!6}
% ------------------------------------------------------------ schémas de Lewis
\setchemfig{atom sep=2.1em,bond offset=1.5pt,double bond sep=2.8pt,
  bond style={line width=0.75pt,otInk},atom style={text=otInk}}
\setcharge{extra sep=1.2pt,"length=1.5ex,|style={otInk,line width=0.85pt}}
\newcommand{\dnlVert}{\setcharge{extra sep=1.2pt,"length=1.5ex,|style={otGreenDark,line width=1.1pt}}}
\newcommand{\G}[1]{\textcolor{otGreenDark}{#1}}
\newcommand{\cplus}{\scalebox{0.85}{$\oplus$}}
\newcommand{\cmoins}{\scalebox{0.85}{$\ominus$}}
\newcommand{\cplusV}{\textcolor{otGreenDark}{\scalebox{0.9}{$\oplus$}}}
\newcommand{\cmoinsV}{\textcolor{otGreenDark}{\scalebox{0.9}{$\ominus$}}}
\tikzset{pcGroupe/.style={draw=otGreenDark,line width=0.8pt,rounded corners=1.8mm,
  dash pattern=on 2.6pt off 1.6pt}}
% ------------------------------------------------------------ légendes
\tikzset{
  leg/.style={font=\otRegular\fontsize{8.5}{10.5}\selectfont,text=otInk,inner sep=1.4pt,align=left},
  fil/.style={draw=otMuted,line width=0.45pt},
  flN/.style={draw=otNavy,line width=0.9pt,-{Stealth[length=2.3mm]}},
  flV/.style={draw=otGreenDark,line width=1pt,-{Stealth[length=2.4mm]}},
  boite/.style={rounded corners=1.6mm,align=center,inner sep=1.3mm,fill=otNavyTint,draw=otNavy!45,line width=0.6pt},
}
"""


# ====================================================================== outils
def lewis_ligne(gauche, droite, nom_g, nom_d, groupe_g="", groupe_d=""):
    """Deux schémas de Lewis conjugués reliés par une double flèche (perte / gain d'un ion H+)."""
    def leg(nom, grp):
        g = f"\\\\[0.4mm]{{\\otRegular\\fontsize{{8.5}}{{10}}\\selectfont\\color{{otGreenDark}}{grp}}}" if grp else ""
        return (f"\\begin{{tabular}}[t]{{@{{}}c@{{}}}}{{\\otMedium\\fontsize{{9}}{{11}}\\selectfont\\color{{otInk}}{nom}}}"
                f"{g}\\end{{tabular}}")
    # disposition verticale (lecture sur téléphone) : acide en haut, base en bas
    fleche = (r"\begin{tikzpicture}"
              r"\draw[otNavy,line width=0.8pt,-{Stealth[length=2mm]}] (-1mm,4mm) -- (-1mm,-4mm);"
              r"\draw[otNavy,line width=0.8pt,-{Stealth[length=2mm]}] (1mm,-4mm) -- (1mm,4mm);"
              r"\node[left,font=\fontsize{9}{10}\selectfont] at (-1.8mm,0) {$-\,$\cm{H+}};"
              r"\node[right,font=\fontsize{9}{10}\selectfont] at (1.8mm,0) {$+\,$\cm{H+}};"
              r"\end{tikzpicture}")
    return (r"{\renewcommand{\arraystretch}{1}\begin{tabular}{@{}c@{}}" "\n"
            f"{gauche}\\\\[2.5mm]\n{leg(nom_g, groupe_g)}\\\\[2mm]\n"
            f"{fleche}\\\\[2mm]\n"
            f"{droite}\\\\[2.5mm]\n{leg(nom_d, groupe_d)}\n"
            r"\end{tabular}}")


FIGURES = {}

# ====================================================================== cours (et fiche)
FIGURES["c_transfert"] = r"""
\begin{tikzpicture}[x=1mm,y=1mm,esp/.style={boite,minimum width=27mm,minimum height=13mm}]
\node[esp] (a1) at (0,32) {{\titreF\color{otNavy}\otCaps[6]{acide 1}}\\[0.8mm]\cm{CH3COOH}};
\node[esp] (b1) at (58,32) {{\titreF\color{otNavy}\otCaps[6]{base 1}}\\[0.8mm]\cm{CH3COO-}};
\node[esp,fill=otGreenTint,draw=otGreen] (b2) at (0,0) {{\titreF\color{otGreenDark}\otCaps[6]{base 2}}\\[0.8mm]\cm{NH3}};
\node[esp,fill=otGreenTint,draw=otGreen] (a2) at (58,0) {{\titreF\color{otGreenDark}\otCaps[6]{acide 2}}\\[0.8mm]\cm{NH4+}};
\draw[flN] (a1) -- (b1);
\node[leg,anchor=north,text=otNavy] at (29,30.2) {cède un ion \cm{H+}};
\draw[flV] (b2) -- (a2);
\node[leg,anchor=south,text=otGreenDark] at (29,1.8) {capte un ion \cm{H+}};
\draw[otOrange!85!black,line width=1.3pt,-{Stealth[length=2.6mm]}] (a1.south) -- (b2.north);
\node[anchor=west,font=\fontsize{10}{11}\selectfont,text=otOrange!80!black] at (1.5,16) {\cm{H+}};
\node[leg,text=otMuted,anchor=south] at (29,40.5) {couple 1 : \cm{CH3COOH}/\cm{CH3COO-}};
\node[leg,text=otMuted,anchor=north] at (29,-8.5) {couple 2 : \cm{NH4+}/\cm{NH3}};
\end{tikzpicture}"""

# Groupe caractéristique en vert (atomes et liaisons). Les cadres \chemmove de chemfig
# demandent deux compilations : ils ne sont pas utilisés ici.
VB = ",,,,draw=otGreenDark"   # liaison verte
LEWIS_ACIDE_ETH = (r"\chemfig{H-C(-[2]H)(-[6]H)-\G{C}(=[1" + VB + r"]\charge{0=\|,90=\|}{\G{O}})"
                   r"-[7" + VB + r"]\charge{180=\|,270=\|}{\G{O}}-[" + VB + r"]\G{H}}")
LEWIS_ETHANOATE = (r"\chemfig{H-C(-[2]H)(-[6]H)-\G{C}(=[1" + VB + r"]\charge{0=\|,90=\|}{\G{O}})"
                   r"-[7" + VB + r"]\charge{0=\|,180=\|,270=\|,60:4.4pt=\cmoins}{\G{O}}}")
LEWIS_METHYLAMMONIUM = (r"\chemfig{H-C(-[2]H)(-[6]H)-\charge{45:4.8pt=\cplus}{\G{N}}(-[2" + VB + r"]\G{H})"
                        r"(-[6" + VB + r"]\G{H})-[" + VB + r"]\G{H}}")
LEWIS_METHYLAMINE = (r"\chemfig{H-C(-[2]H)(-[6]H)-\charge{90=\|}{\G{N}}(-[6" + VB + r"]\G{H})-[" + VB + r"]\G{H}}")

FIGURES["c_lewis_acide"] = lewis_ligne(LEWIS_ACIDE_ETH, LEWIS_ETHANOATE,
                                       "acide éthanoïque", "ion éthanoate", "groupe carboxyle", "groupe carboxylate")
FIGURES["c_lewis_amine"] = lewis_ligne(LEWIS_METHYLAMMONIUM, LEWIS_METHYLAMINE,
                                       "ion méthylammonium", "méthylamine", "groupe ammonium", "groupe amino")


def echelle_ph(exemples, u=4.6, L=6):
    """Échelle de pH verticale (pH 0 en bas), exemples à droite reliés par des filets coudés.

    exemples : [(pH, texte, hauteur de l'étiquette en unités de pH)].
    """
    # une ombre pgf de 100 bp est étirée pour que sa partie centrale (25 à 75 bp) couvre le rectangle
    out = [r"\pgfdeclareverticalshading{echPH}{100bp}{color(0bp)=(otRed!85);color(25bp)=(otRed!85);"
           r"color(37.5bp)=(otOrange!90);color(50bp)=(otGreen!75);color(62.5bp)=(cyan!45!otNavy!75);"
           r"color(75bp)=(otNavyDark);color(100bp)=(otNavyDark)}",
           r"\begin{tikzpicture}[x=1mm,y=1mm]",
           f"\\shade[shading=echPH] (0,0) rectangle ({L},{14 * u});",
           f"\\draw[otInk!45,line width=0.4pt] (0,0) rectangle ({L},{14 * u});"]
    for k in range(15):
        out.append(f"\\draw[otInk!60,line width=0.45pt] (0,{k * u}) -- (-1.4,{k * u});")
        out.append(f"\\node[anchor=east,font=\\otMedium\\fontsize{{8.5}}{{10}}\\selectfont,text=otInk,inner sep=1pt] "
                   f"at (-1.7,{k * u}) {{{k}}};")
    for ph, txt, ylab in exemples:
        y, yl = ph * u, ylab * u
        out.append(f"\\fill[otInk] ({L},{y}) circle (0.55mm);")
        out.append(f"\\draw[fil] ({L},{y}) -- ({L + 3},{y}) -- ({L + 7},{yl}) -- ({L + 9},{yl});")
        out.append(f"\\node[leg,anchor=west] at ({L + 9.2},{yl}) {{{txt}}};")
    x = -9
    out += [f"\\draw[otRed!80!black,line width=0.9pt] ({x},{0.15 * u}) -- ({x},{6.75 * u});",
            f"\\draw[otNavy,line width=0.9pt] ({x},{7.25 * u}) -- ({x},{13.85 * u});",
            f"\\fill[otGreenDark] ({x},{7 * u}) circle (0.7mm);",
            f"\\node[leg,anchor=east,align=right,text=otRed!80!black] at ({x - 1.2},{3.5 * u}) {{solution\\\\acide}};",
            f"\\node[leg,anchor=east,align=right,text=otGreenDark] at ({x - 1.2},{7 * u}) {{neutre}};",
            f"\\node[leg,anchor=east,align=right,text=otNavy] at ({x - 1.2},{10.5 * u}) {{solution\\\\basique}};",
            f"\\node[anchor=south,font=\\otSemi\\fontsize{{8.5}}{{10}}\\selectfont] at ({L / 2},{14 * u + 1.2}) {{pH}};",
            r"\end{tikzpicture}"]
    return "\n".join(out)


FIGURES["c_echelle_ph"] = echelle_ph([
    (1.5, r"suc gastrique (≈ 1,5)", 1.2),
    (2.4, r"jus de citron (≈ 2,4)", 2.6),
    (5.0, r"café (≈ 5)", 5.0),
    (7.0, r"eau pure à 25 °C (7,0)", 6.6),
    (7.4, r"sang (≈ 7,4)", 7.9),
    (8.1, r"eau de mer (≈ 8,1)", 9.2),
    (12.0, r"eau de Javel (≈ 12)", 11.9),
    (13.5, r"déboucheur (≈ 13,5)", 13.3),
])

# ====================================================================== corrigés (en vert : ce que l'élève ajoute)
# Exercice : éthylamine et ion éthylammonium
FIGURES["ex_lewis_ethylamine"] = lewis_ligne(
    r"{\setchemfig{atom sep=1.8em}\dnlVert"
    r"\chemfig{H-C(-[2]H)(-[6]H)-C(-[2]H)(-[6]H)-\charge{45:4.8pt=\cplusV}{N}(-[2]H)(-[6]H)-H}}",
    r"{\setchemfig{atom sep=1.8em}\dnlVert"
    r"\chemfig{H-C(-[2]H)(-[6]H)-C(-[2]H)(-[6]H)-\charge{90=\|}{N}(-[6]H)-H}}",
    "ion éthylammonium", "éthylamine", "charge $+1$ sur l’azote", "doublet non liant de N")
