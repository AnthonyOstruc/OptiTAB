# -*- coding: utf-8 -*-
"""Figures de la notion « Combinatoire et dénombrement » (Terminale), style des livres.

Compilation : python ../../../outils/figures_livre.py <ce dossier de notion> [--planche]

Cours : arbre des parties de {a ; b ; c}, arbre des couples d'éléments distincts,
triangle de Pascal, chemin sur un quadrillage, organigramme « quel modèle ? ».
Exercices : table ronde (rotations), hexagone et ses diagonales.
"""

# Styles communs aux arbres et schémas (ajoutés au préambule des livres)
PREAMBULE_EXTRA = r"""
\newcommand{\notefig}{\otRegular\fontsize{8}{9.5}\selectfont\color{otMuted}}
\tikzset{
  arbreB/.style={otNavy,line width=0.75pt},
  arbreV/.style={otGreenDark,line width=0.75pt},
  noeudA/.style={inner sep=2.6pt,font=\normalsize},
  titreCol/.style={font=\otMedium\fontsize{8.5}{10.5}\selectfont,text=otMuted,align=center,inner sep=1pt},
  bilan/.style={font=\normalsize,text=otGreenDark,inner sep=1pt},
  question/.style={draw=otNavy,fill=otSky,line width=0.7pt,rounded corners=2mm,inner sep=2.2mm,
    align=center,text=otInk,font=\normalsize,minimum width=2.55cm,minimum height=0.85cm},
  modele/.style={draw=otGreenDark,fill=otGreen!13,line width=0.7pt,rounded corners=2mm,inner sep=1.6mm,
    align=center,text=otInk,font=\normalsize,minimum width=2.8cm},
  fleche/.style={otMuted,line width=0.7pt,-{Stealth[length=2.1mm]}},
  reponse/.style={font=\otMedium\fontsize{8.5}{10}\selectfont,inner sep=1.2pt},
  exemple/.style={font=\otRegular\fontsize{8}{9.5}\selectfont,text=otMuted},
  case/.style={draw=otRule,line width=0.55pt,fill=white,rounded corners=1.3pt,minimum width=0.66cm,
    minimum height=0.5cm,inner sep=0pt,font=\normalsize,text=otInk},
  caseA/.style={case,draw=otOrange,fill=otOrange!16,line width=0.8pt},
  caseB/.style={case,draw=otGreenDark,fill=otGreen!22,line width=0.8pt},
}
"""

FIGURES = {
# ------------------------------------------------------------------ cours
# II. Un ensemble à n éléments a 2^n parties : arbre des choix oui / non pour E = {a ; b ; c}
"arbre_parties": r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \def\ya{1.86}\def\yb{0.62}
  % racine
  \fill[otInk] (0,0) circle (2pt);
  % niveau 1 : a ?
  \node[noeudA,text=otGreenDark] (o) at (1.7,1.24) {oui};
  \node[noeudA,text=otMuted] (n) at (1.7,-1.24) {non};
  % niveau 2 : b ?
  \node[noeudA,text=otGreenDark] (oo) at (3.4,1.86) {oui};
  \node[noeudA,text=otMuted] (on) at (3.4,0.62) {non};
  \node[noeudA,text=otGreenDark] (no) at (3.4,-0.62) {oui};
  \node[noeudA,text=otMuted] (nn) at (3.4,-1.86) {non};
  % niveau 3 : c ?
  \node[noeudA,text=otGreenDark] (ooo) at (5.1,2.17) {oui};
  \node[noeudA,text=otMuted] (oon) at (5.1,1.55) {non};
  \node[noeudA,text=otGreenDark] (ono) at (5.1,0.93) {oui};
  \node[noeudA,text=otMuted] (onn) at (5.1,0.31) {non};
  \node[noeudA,text=otGreenDark] (noo) at (5.1,-0.31) {oui};
  \node[noeudA,text=otMuted] (non) at (5.1,-0.93) {non};
  \node[noeudA,text=otGreenDark] (nno) at (5.1,-1.55) {oui};
  \node[noeudA,text=otMuted] (nnn) at (5.1,-2.17) {non};
  \draw[arbreB] (0,0) -- (o); \draw[arbreB] (0,0) -- (n);
  \draw[arbreB] (o) -- (oo); \draw[arbreB] (o) -- (on);
  \draw[arbreB] (n) -- (no); \draw[arbreB] (n) -- (nn);
  \draw[arbreB] (oo) -- (ooo); \draw[arbreB] (oo) -- (oon);
  \draw[arbreB] (on) -- (ono); \draw[arbreB] (on) -- (onn);
  \draw[arbreB] (no) -- (noo); \draw[arbreB] (no) -- (non);
  \draw[arbreB] (nn) -- (nno); \draw[arbreB] (nn) -- (nnn);
  % parties obtenues
  \foreach \y/\p in {2.17/{\{a\,;b\,;c\}}, 1.55/{\{a\,;b\}}, 0.93/{\{a\,;c\}}, 0.31/{\{a\}},
                     -0.31/{\{b\,;c\}}, -0.93/{\{b\}}, -1.55/{\{c\}}, -2.17/{\varnothing}}
    \node[anchor=west,text=otInk,inner sep=1pt] at (5.85,\y) {$\p$};
  % en-têtes de colonnes
  \node[titreCol] at (1.7,2.95) {prend-on\\$a$ ?};
  \node[titreCol] at (3.4,2.95) {prend-on\\$b$ ?};
  \node[titreCol] at (5.1,2.95) {prend-on\\$c$ ?};
  \node[titreCol] at (6.55,2.95) {partie\\obtenue};
  \node[bilan] at (3.6,-2.85) {$2\times2\times2=2^3=8$ parties};
\end{tikzpicture}""",

# III. k-uplets d'éléments distincts : couples d'éléments distincts de {A ; B ; C}
"arbre_arrangements": r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \fill[otInk] (0,0) circle (2pt);
  \node[noeudA,text=otNavy] (A) at (2,1.7) {$A$};
  \node[noeudA,text=otNavy] (B) at (2,0) {$B$};
  \node[noeudA,text=otNavy] (C) at (2,-1.7) {$C$};
  \draw[arbreB] (0,0) -- (A); \draw[arbreB] (0,0) -- (B); \draw[arbreB] (0,0) -- (C);
  \node[noeudA,text=otGreenDark] (AB) at (4.3,2.125) {$B$};
  \node[noeudA,text=otGreenDark] (AC) at (4.3,1.275) {$C$};
  \node[noeudA,text=otGreenDark] (BA) at (4.3,0.425) {$A$};
  \node[noeudA,text=otGreenDark] (BC) at (4.3,-0.425) {$C$};
  \node[noeudA,text=otGreenDark] (CA) at (4.3,-1.275) {$A$};
  \node[noeudA,text=otGreenDark] (CB) at (4.3,-2.125) {$B$};
  \draw[arbreV] (A) -- (AB); \draw[arbreV] (A) -- (AC);
  \draw[arbreV] (B) -- (BA); \draw[arbreV] (B) -- (BC);
  \draw[arbreV] (C) -- (CA); \draw[arbreV] (C) -- (CB);
  \foreach \y/\c in {2.125/{(A\,;B)}, 1.275/{(A\,;C)}, 0.425/{(B\,;A)}, -0.425/{(B\,;C)}, -1.275/{(C\,;A)}, -2.125/{(C\,;B)}}
    \node[anchor=west,text=otInk,inner sep=1pt] at (5.45,\y) {$\c$};
  \node[titreCol] at (2,2.95) {1\textsuperscript{er} élément\\3 choix};
  \node[titreCol] at (4.3,2.95) {2\textsuperscript{e} élément\\2 choix};
  \node[titreCol] at (6.0,2.95) {couple\\obtenu};
  \node[bilan] at (3.2,-2.85) {$3\times2=6$ couples d'éléments distincts};
\end{tikzpicture}""",

# IV. Triangle de Pascal (lignes 0 à 6) et relation de Pascal 4 + 6 = 10
"triangle_pascal": r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \def\w{0.8}\def\h{0.78}
  \node[font=\normalsize,text=otMuted,inner sep=1pt] at (-3.2,0.62) {$n$};
  \foreach \n/\ligne in {0/{1}, 1/{1,1}, 2/{1,2,1}, 3/{1,3,3,1}, 4/{1,4,6,4,1}, 5/{1,5,10,10,5,1}, 6/{1,6,15,20,15,6,1}}{
    \node[font=\otMedium\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt] at (-3.2,-\n*\h) {\n};
    \foreach \v [count=\k from 0] in \ligne {
      \pgfmathsetmacro{\xx}{(\k-\n/2)*\w}
      \node[case] (c\n-\k) at (\xx,-\n*\h) {$\v$};
    }
  }
  % relation de Pascal mise en évidence : C(4,1) + C(4,2) = C(5,2)
  \node[caseA] at (c4-1) {$4$};
  \node[caseA] at (c4-2) {$6$};
  \node[caseB] at (c5-2) {$10$};
  \draw[otOrange!85!black,line width=0.8pt,-{Stealth[length=1.6mm]}] ([xshift=1.5pt]c4-1.south) -- ([xshift=-3.5pt]c5-2.north);
  \draw[otOrange!85!black,line width=0.8pt,-{Stealth[length=1.6mm]}] ([xshift=-1.5pt]c4-2.south) -- ([xshift=3.5pt]c5-2.north);
  \node[anchor=north,align=center,inner sep=1pt,font=\normalsize,text=otInk] at (-0.2,-5.22)
    {\textcolor{otMuted}{\otMedium\fontsize{8.5}{10}\selectfont Relation de Pascal}\\[3pt]
     $\dbinom{4}{1}+\dbinom{4}{2}=\dbinom{5}{2}$, soit $4+6=10$};
\end{tikzpicture}""",

# IV. Mots et chemins : le chemin DDHDHHD de O(0 ; 0) à A(4 ; 3)
"chemin_quadrillage": r"""
\begin{tikzpicture}[x=1.05cm,y=1.05cm]
  \draw[otRule,line width=0.6pt] (0,0) grid (4,3);
  \draw[otGreen,line width=2.2pt,line cap=round,line join=round] (0,0) -- (2,0) -- (2,1) -- (3,1) -- (3,3) -- (4,3);
  \fill[otNavy] (0,0) circle (2.6pt);
  \fill[otNavy] (4,3) circle (2.6pt);
  \node[anchor=north east,inner sep=1pt,text=otInk] at (-0.06,-0.06) {$O(0\,;0)$};
  \node[anchor=south west,inner sep=1pt,text=otInk] at (4.06,3.06) {$A(4\,;3)$};
  \foreach \x/\y/\l in {0.5/0.3/D, 1.5/0.3/D, 2.25/0.5/H, 2.5/1.3/D, 3.25/1.5/H, 3.25/2.5/H, 3.5/3.3/D}
    \node[font=\otMedium\fontsize{9}{10}\selectfont,text=otGreenDark,inner sep=0.5pt] at (\x,\y) {\l};
  \node[anchor=north,exemple,align=center] at (2,-0.45) {chemin DDHDHHD : 7 pas, dont 3 vers le haut};
\end{tikzpicture}""",

# V. Choisir le bon modèle
"organigramme_modele": r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \node[question] (Q1) at (0,0) {L’ordre\\compte-t-il ?};
  \node[question] (Q2) at (0,-2.6) {Répétitions\\possibles ?};
  \node[modele] (C) at (3.7,0) {\textbf{Combinaisons}\\[1pt] $\dbinom{n}{k}$\\[1pt] {\notefig tirage simultané}};
  \node[modele] (A) at (3.7,-2.6) {\textbf{Arrangements}\\[1pt] $\dfrac{n!}{(n-k)!}$\\[1pt] {\notefig tirages successifs}\\{\notefig sans remise}};
  \node[modele] (K) at (0,-5.25) {\textbf{$k$-uplets}\\[1pt] $n^{k}$\\[1pt] {\notefig tirages successifs}\\{\notefig avec remise}};
  \node[modele] (P) at (3.7,-5.25) {\textbf{Permutations}\\[1pt] $n!$\\[1pt] {\notefig on range les}\\{\notefig $n$ éléments}};
  \draw[fleche] (Q1.east) -- node[reponse,above=1.5pt,text=otOrange!85!black] {non} (C.west);
  \draw[fleche] (Q2.east) -- node[reponse,above=1.5pt,text=otOrange!85!black] {non} (A.west);
  \draw[fleche] (Q1.south) -- node[reponse,right=2pt,text=otGreenDark] {oui} (Q2.north);
  \draw[fleche] (Q2.south) -- node[reponse,right=2pt,text=otGreenDark] {oui} (K.north);
  \draw[fleche] (A.south) -- node[reponse,right=2pt,text=otMuted] {si $k=n$} (P.north);
\end{tikzpicture}""",

# ------------------------------------------------------------------ exercices
# 1264, question 5 : deux placements qui se déduisent l'un de l'autre par une rotation
"table_ronde": r"""
\begin{tikzpicture}[x=1cm,y=1cm,
  table/.style={draw=otNavy,fill=otSky,line width=0.8pt},
  pers/.style={circle,draw=otNavy,fill=white,line width=0.7pt,minimum size=0.62cm,inner sep=0pt,font=\normalsize,text=otInk}]
  \begin{scope}
    \draw[table] (0,0) circle (0.72);
    \node[pers] at (90:1.12) {$A$};
    \node[pers] at (0:1.12) {$B$};
    \node[pers] at (-90:1.12) {$C$};
    \node[pers] at (180:1.12) {$D$};
    \node[exemple] at (0,-1.85) {placement 1};
  \end{scope}
  \begin{scope}[xshift=5.2cm]
    \draw[table] (0,0) circle (0.72);
    \node[pers] at (90:1.12) {$D$};
    \node[pers] at (0:1.12) {$A$};
    \node[pers] at (-90:1.12) {$B$};
    \node[pers] at (180:1.12) {$C$};
    \node[exemple] at (0,-1.85) {placement 2};
  \end{scope}
  \draw[otMuted,line width=0.7pt,-{Stealth[length=2.1mm]}] (1.75,0) -- (3.45,0);
  \node[exemple,anchor=south,align=center] at (2.6,0.12) {rotation d’un\\quart de tour};
  \node[anchor=north,font=\normalsize,text=otGreenDark,align=center] at (2.6,-2.25)
    {même placement : chacun garde ses deux voisins};
\end{tikzpicture}""",

# 1267, question 5 : hexagone, 6 côtés et 9 diagonales
"hexagone_diagonales": r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \foreach \i/\l in {0/A,1/B,2/C,3/D,4/E,5/F}
    \coordinate (\l) at (90+60*\i:1.65);
  \foreach \p/\q in {A/C,A/D,A/E,B/D,B/E,B/F,C/E,C/F,D/F}
    \draw[otGreenDark,line width=0.75pt,dash pattern=on 3.5pt off 2pt] (\p) -- (\q);
  \draw[otNavy,line width=1.2pt,line join=round] (A) -- (B) -- (C) -- (D) -- (E) -- (F) -- cycle;
  \foreach \i/\l in {0/A,1/B,2/C,3/D,4/E,5/F}{
    \fill[otNavy] (\l) circle (1.9pt);
    \node[text=otInk,inner sep=1pt] at (90+60*\i:2.02) {$\l$};
  }
  \begin{scope}[xshift=2.75cm,yshift=0.55cm]
    \draw[otNavy,line width=1.2pt] (0,0) -- (0.55,0);
    \node[anchor=west,font=\normalsize,text=otInk,inner sep=1pt] at (0.68,0) {$6$ côtés};
    \draw[otGreenDark,line width=0.75pt,dash pattern=on 3.5pt off 2pt] (0,-0.62) -- (0.55,-0.62);
    \node[anchor=west,font=\normalsize,text=otInk,inner sep=1pt] at (0.68,-0.62) {$9$ diagonales};
    \node[anchor=west,font=\normalsize,text=otGreenDark,inner sep=1pt] at (-0.05,-1.4) {$\dbinom{6}{2}=15$ segments};
  \end{scope}
\end{tikzpicture}""",
}
