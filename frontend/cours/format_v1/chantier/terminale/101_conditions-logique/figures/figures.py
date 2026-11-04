# -*- coding: utf-8 -*-
"""Figures de la notion « Conditions / Logique » (Terminale), style des livres OptiTAB.

Compilation : python ../../../outils/figures_livre.py <dossier_notion> --planche
Organigramme repris du livre de Terminale (chapitre 20) ; libellés « oui » / « non »
posés à côté des flèches, jamais dessus ; éléments de réponse en vert.
"""

PREAMBULE_EXTRA = r"""
\newfontfamily\otMono{FiraMono}[Extension=.otf, UprightFont=*-Regular, BoldFont=*-Medium]
\colorlet{otNavyTint}{otNavy!7}
\colorlet{otGreenTint}{otGreen!18}
\colorlet{otOrangeTint}{otOrange!16}
\tikzset{
  test/.style={draw=otNavy,fill=otNavyTint,line width=0.7pt,rounded corners=1.2mm,
    inner xsep=2.2mm,inner ysep=1.6mm,font=\otMono\fontsize{9.5}{11}\selectfont,text=otInk},
  bloc/.style={draw=otGreenDark,fill=otGreenTint,line width=0.7pt,rounded corners=1.2mm,
    inner xsep=2.4mm,inner ysep=1.6mm,font=\otMono\fontsize{9.5}{11}\selectfont,text=otInk},
  blocGris/.style={draw=otMuted,fill=white,line width=0.6pt,rounded corners=1.2mm,
    inner xsep=2.4mm,inner ysep=1.6mm,font=\otRegular\fontsize{9}{11}\selectfont,text=otInk},
  borne/.style={draw=otMuted,fill=white,line width=0.6pt,rounded corners=2.6mm,
    inner xsep=2.6mm,inner ysep=1.5mm,font=\otRegular\fontsize{9}{11}\selectfont,text=otInk},
  fleche/.style={otMuted,line width=0.7pt,-{Stealth[length=2mm]}},
  flecheV/.style={otGreenDark,line width=1.2pt,-{Stealth[length=2.3mm]}},
  ouinon/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},
  ouinonV/.style={font=\otMedium\fontsize{8.5}{10}\selectfont,text=otGreenDark},
  lib/.style={font=\otMono\fontsize{9.5}{11}\selectfont},
}
"""

# ------------------------------------------------------------------ cours, fiche
# if condition1: bloc1 / elif condition2: bloc2 / else: bloc3 / suite
ORGANIGRAMME = r"""
\begin{tikzpicture}[x=10mm,y=10mm]
  \node[test] (t1) at (0,0) {condition1 ?};
  \node[bloc] (b1) at (3.9,0) {bloc1};
  \node[test] (t2) at (0,-1.5) {condition2 ?};
  \node[bloc] (b2) at (3.9,-1.5) {bloc2};
  \node[bloc] (b3) at (0,-3.0) {bloc3};
  \node[borne] (s) at (0,-4.4) {suite du programme};
  \draw[fleche] (t1.east) -- (b1.west) node[ouinon,midway,above=1.2mm] {oui};
  \draw[fleche] (t2.east) -- (b2.west) node[ouinon,midway,above=1.2mm] {oui};
  \draw[fleche] (t1.south) -- (t2.north) node[ouinon,midway,right=1.2mm] {non};
  \draw[fleche] (t2.south) -- (b3.north) node[ouinon,midway,right=1.2mm] {non};
  \draw[fleche] (b3.south) -- (s.north);
  \draw[otMuted,line width=0.7pt] (b1.east) -- ++(0.5,0) |- (b2.east);
  \draw[fleche] (b2.east) ++(0.5,0) |- (s.east);
\end{tikzpicture}
"""

# négation de 18 <= age <= 65 : age < 18 or age > 65
NEGATION = r"""
\begin{tikzpicture}[x=0.86mm,y=10mm]
  \draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (-4,0) -- (92,0);
  \node[font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=north west] at (88,-0.12) {âge};
  \draw[otOrange,line width=3.2pt,line cap=butt] (0,0) -- (18,0);
  \draw[otOrange,line width=3.2pt,line cap=butt] (65,0) -- (86,0);
  \draw[otGreen,line width=3.2pt,line cap=butt] (18,0) -- (65,0);
  \foreach \x in {0,18,65} {
    \draw[otMuted,line width=0.5pt] (\x,-0.12) -- (\x,0.12);
    \node[font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,anchor=north] at (\x,-0.2) {\x};
  }
  \fill[otGreenDark] (18,0) circle (0.75mm);
  \fill[otGreenDark] (65,0) circle (0.75mm);
  \node[lib,text=otGreenDark,anchor=south] at (41.5,0.28) {18 <= age <= 65};
  \node[lib,text=otOrange!85!black,anchor=south] at (9,0.28) {age < 18};
  \node[lib,text=otOrange!85!black,anchor=south] at (77,0.28) {age > 65};
\end{tikzpicture}
"""

# ------------------------------------------------------------------ exercice 829
# tarif du cinéma pour age = 25 et jour = "Lundi" : chemin en vert
ARBRE_CINEMA = r"""
\begin{tikzpicture}[x=10mm,y=10mm]
  \node[test] (t1) at (0,0) {age < 18 ?};
  \node[blocGris] (r7) at (3.6,0) {7 €};
  \node[test,draw=otGreenDark,line width=1.1pt] (t2) at (0,-1.5) {age < 65 ?};
  \node[blocGris] (r8) at (3.6,-1.5) {8 €};
  \node[test,draw=otGreenDark,line width=1.1pt] (t3) at (0,-3.0) {jour == "Lundi" ?};
  \node[bloc,line width=1.1pt,font=\otMedium\fontsize{9.5}{11}\selectfont] (r9) at (0,-4.5) {9 €};
  \node[blocGris] (r12) at (3.6,-3.0) {12 €};
  \draw[fleche] (t1.east) -- (r7.west) node[ouinon,midway,above=1.2mm] {oui};
  \draw[flecheV] (t1.south) -- (t2.north) node[ouinonV,midway,right=1.2mm] {non};
  \draw[fleche] (t2.east) -- (r8.west) node[ouinon,midway,above=1.2mm] {non};
  \draw[flecheV] (t2.south) -- (t3.north) node[ouinonV,midway,right=1.2mm] {oui};
  \draw[fleche] (t3.east) -- (r12.west) node[ouinon,midway,above=1.2mm] {non};
  \draw[flecheV] (t3.south) -- (r9.north) node[ouinonV,midway,right=1.2mm] {oui};
  \node[font=\otRegular\fontsize{8.5}{10}\selectfont,text=otGreenDark,anchor=west] at (0.65,-4.5) {age = 25, jour = "Lundi"};
\end{tikzpicture}
"""

FIGURES = {
    "organigramme_elif": ORGANIGRAMME,
    "negation_intervalle": NEGATION,
    "arbre_cinema": ARBRE_CINEMA,
}
