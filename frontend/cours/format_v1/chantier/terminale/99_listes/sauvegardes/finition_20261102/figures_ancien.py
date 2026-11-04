# -*- coding: utf-8 -*-
"""Figures de la notion « Listes » (Terminale), style des livres OptiTAB.

Compilation : python ../../../outils/figures_livre.py <dossier_notion> --planche
Schémas de listes repris du livre de Terminale (chapitre 22, « Listes ») :
cases bleu marine, indices en Fira Mono, éléments de réponse en vert.
"""

PREAMBULE_EXTRA = r"""
\newfontfamily\otMono{FiraMono}[Extension=.otf, UprightFont=*-Regular, BoldFont=*-Medium]
\colorlet{otNavyTint}{otNavy!7}
\colorlet{otGreenTint}{otGreen!18}
\tikzset{
  caseL/.style={draw=otNavy,fill=otNavyTint,line width=0.7pt},
  caseV/.style={draw=otGreenDark,fill=otGreenTint,line width=1pt},
  val/.style={font=\otMono\fontsize{10}{12}\selectfont,text=otInk},
  idx/.style={font=\otMono\fontsize{9}{10}\selectfont,text=otNavy},
  idxn/.style={font=\otMono\fontsize{9}{10}\selectfont,text=otMuted},
  idxV/.style={font=\otMono\bfseries\fontsize{9}{10}\selectfont,text=otGreenDark},
  lib/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,text=otMuted},
  nomvar/.style={font=\otMono\fontsize{10}{12}\selectfont,text=otInk},
  fleche/.style={otMuted,line width=0.7pt,-{Stealth[length=2mm]}},
  boiteNom/.style={draw=otMuted,fill=white,rounded corners=0.8mm,minimum width=7mm,
    minimum height=5.5mm,inner sep=0pt,font=\otMono\fontsize{10}{12}\selectfont},
}
"""

# ------------------------------------------------------------------ cours, fiche
# notes = [12, 15, 18, 10, 14] : indices positifs (au-dessus) et négatifs (dessous)
LISTE_INDICES = r"""
\begin{tikzpicture}[x=10mm,y=10mm]
  \foreach \v [count=\i from 0] in {12,15,18,10,14} {
    \draw[caseL] (\i,0) rectangle ++(1,0.8);
    \node[val] at (\i+0.5,0.4) {\v};
    \node[idx] at (\i+0.5,1.12) {\i};
    \pgfmathtruncatemacro\kneg{\i-5}
    \node[idxn] at (\i+0.5,-0.33) {\kneg};
  }
  \node[nomvar,anchor=east] at (-0.12,0.4) {notes =};
  \node[lib,anchor=east] at (-0.12,1.12) {indice};
  \node[lib,anchor=east] at (-0.12,-0.33) {indice négatif};
\end{tikzpicture}
"""

# nombres = [5, 10, 15] puis nombres.insert(1, 8) -> [5, 8, 10, 15]
LISTE_INSERTION = r"""
\begin{tikzpicture}[x=10mm,y=10mm]
  % avant
  \foreach \v [count=\i from 0] in {5,10,15} {
    \draw[caseL] (\i,2.3) rectangle ++(1,0.8);
    \node[val] at (\i+0.5,2.7) {\v};
    \node[idx] at (\i+0.5,3.42) {\i};
  }
  % après
  \draw[caseL] (0,0) rectangle ++(1,0.8);  \node[val] at (0.5,0.4) {5};
  \draw[caseV] (1,0) rectangle ++(1,0.8);  \node[val,text=otGreenDark] at (1.5,0.4) {8};
  \draw[caseL] (2,0) rectangle ++(1,0.8);  \node[val] at (2.5,0.4) {10};
  \draw[caseL] (3,0) rectangle ++(1,0.8);  \node[val] at (3.5,0.4) {15};
  \node[idx] at (0.5,-0.33) {0};
  \node[idxV] at (1.5,-0.33) {1};
  \node[idx] at (2.5,-0.33) {2};
  \node[idx] at (3.5,-0.33) {3};
  % déplacements
  \draw[fleche,dash pattern=on 2pt off 1.6pt] (0.5,2.22) -- (0.5,0.88);
  \draw[fleche] (1.5,2.22) -- (2.5,0.88);
  \draw[fleche] (2.5,2.22) -- (3.5,0.88);
  % libellés
  \node[lib,anchor=east] at (-0.15,2.7) {avant};
  \node[lib,anchor=east] at (-0.15,0.4) {après};
  \node[nomvar,text=otNavy,anchor=west] at (3.25,2.7) {nombres.insert(1, 8)};
\end{tikzpicture}
"""

# M = L : un seul objet liste ; N = L.copy() : une copie indépendante
LISTE_COPIE = r"""
\begin{tikzpicture}[x=9mm,y=9mm]
  \foreach \v [count=\i from 0] in {1,2,3,4} {
    \draw[caseL] (\i,0) rectangle ++(1,1);
    \node[val] at (\i+0.5,0.5) {\v};
  }
  \foreach \v [count=\i from 0] in {1,2,3,4,5} {
    \draw[caseV] (\i,-2.1) rectangle ++(1,1);
    \node[val] at (\i+0.5,-1.6) {\v};
  }
  \node[boiteNom] (l) at (-2.3,1.05) {L};
  \node[boiteNom] (m) at (-2.3,-0.05) {M};
  \node[boiteNom] (n) at (-2.3,-1.6) {N};
  \draw[fleche] (l.east) -- (-0.1,0.68);
  \draw[fleche] (m.east) -- (-0.1,0.32);
  \draw[fleche] (n.east) -- (-0.1,-1.6);
  \node[lib,anchor=west] at (4.2,0.5) {une seule liste};
  \node[lib,anchor=west] at (5.2,-1.6) {copie};
\end{tikzpicture}
"""

# ------------------------------------------------------------------ exercice 836
# fruits = ["pomme", "banane", "orange", "kiwi"] : fruits[2] et fruits[-2] désignent "orange"
FRUITS_INDICES = r"""
\begin{tikzpicture}[x=16.5mm,y=10mm]
  \tikzset{val/.append style={font=\otMono\fontsize{9}{11}\selectfont}}
  \foreach \v [count=\i from 0] in {pomme,banane,orange,kiwi} {
    \pgfmathtruncatemacro\kneg{\i-4}
    \ifnum\i=2
      \draw[caseV] (\i,0) rectangle ++(1,0.8);
      \node[val,text=otGreenDark] at (\i+0.5,0.4) {"\v"};
      \node[idxV] at (\i+0.5,1.12) {\i};
      \node[idxV] at (\i+0.5,-0.33) {\kneg};
    \else
      \draw[caseL] (\i,0) rectangle ++(1,0.8);
      \node[val] at (\i+0.5,0.4) {"\v"};
      \node[idx] at (\i+0.5,1.12) {\i};
      \node[idxn] at (\i+0.5,-0.33) {\kneg};
    \fi
  }
  \node[lib,anchor=east] at (-0.07,1.12) {indice};
  \node[lib,anchor=east] at (-0.07,-0.33) {indice négatif};
  \node[nomvar,anchor=east] at (-0.07,0.4) {fruits =};
\end{tikzpicture}
"""

FIGURES = {
    "liste_indices": LISTE_INDICES,
    "liste_insertion": LISTE_INSERTION,
    "liste_copie": LISTE_COPIE,
    "fruits_indices": FRUITS_INDICES,
}
