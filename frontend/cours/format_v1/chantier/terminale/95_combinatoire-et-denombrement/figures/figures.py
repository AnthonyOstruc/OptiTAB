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
  % cases à remplir (principe multiplicatif)
  grandeCase/.style={draw=otGreenDark,fill=otGreen!12,line width=0.8pt,rounded corners=2pt,
    minimum width=1.45cm,minimum height=0.95cm,inner sep=0pt,font=\Large,text=otGreenDark},
  caseVide/.style={draw=otNavy,fill=white,line width=0.8pt,rounded corners=2pt,
    minimum width=1.45cm,minimum height=0.95cm,inner sep=0pt},
  fois/.style={font=\large,text=otInk,inner sep=1pt},
  % positions (mots, rangements)
  posN/.style={draw=otRule,line width=0.6pt,fill=white,minimum width=0.72cm,minimum height=0.72cm,
    inner sep=0pt,font=\normalsize,text=otInk},
  posR/.style={posN,draw=otRed!80!black,fill=otRed!18},
  posB/.style={posN,draw=otNavy,fill=otSky},
  posV/.style={posN,draw=otGreenDark,fill=otGreen!22},
  posL/.style={posN,draw=otNavy,fill=otSky},
  posC/.style={posN,draw=otGreenDark,fill=otGreen!22},
  numPos/.style={font=\otRegular\fontsize{8}{9}\selectfont,text=otMuted,inner sep=1pt},
  % boules
  bouleR/.style={circle,draw=otRed!80!black,fill=otRed!22,line width=0.7pt,minimum size=0.6cm,inner sep=0pt,font=\normalsize,text=otInk},
  bouleB/.style={circle,draw=otNavy,fill=otSky,line width=0.7pt,minimum size=0.6cm,inner sep=0pt,font=\normalsize,text=otInk},
  choisie/.style={line width=1.6pt,draw=otGreenDark},
}
"""

from math import comb as _comb


def _pascal(n_max, ligne_vide=None, ligne_verte=None, somme=None):
    """Triangle de Pascal des lignes 0 à n_max.
    ligne_vide : ligne dessinée en cases vides (énoncé) ; ligne_verte : ligne en vert (corrigé) ;
    somme = (n, k) : relation C(n-1,k-1) + C(n-1,k) = C(n,k) mise en évidence."""
    w, h = 0.86, 0.74
    lignes = [r"\begin{tikzpicture}[x=1cm,y=1cm]",
              r"  \node[font=\normalsize,text=otMuted,inner sep=1pt] at (%.2f,%.2f) {$n$};" % (-(n_max / 2) * w - 0.95, h * 0.85)]
    for n in range(n_max + 1):
        lignes.append(r"  \node[font=\otMedium\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1pt] at (%.2f,%.2f) {%d};"
                      % (-(n_max / 2) * w - 0.95, -n * h, n))
        for k in range(n + 1):
            x = (k - n / 2) * w
            if n == ligne_vide:
                lignes.append(r"  \node[case,minimum width=0.74cm,draw=otNavy,line width=0.7pt] (c%d-%d) at (%.3f,%.3f) {};" % (n, k, x, -n * h))
            else:
                style = "caseB" if n == ligne_verte else "case"
                if somme and ((n == somme[0] - 1 and k in (somme[1] - 1, somme[1]))):
                    style = "caseA"
                if somme and n == somme[0] and k == somme[1]:
                    style = "caseB,line width=1.3pt"
                lignes.append(r"  \node[%s,minimum width=0.74cm] (c%d-%d) at (%.3f,%.3f) {$%d$};" % (style, n, k, x, -n * h, _comb(n, k)))
    if somme:
        n, k = somme
        lignes.append(r"  \draw[otOrange!85!black,line width=0.8pt,-{Stealth[length=1.6mm]}] ([xshift=1.5pt]c%d-%d.south) -- ([xshift=-3.5pt]c%d-%d.north);" % (n - 1, k - 1, n, k))
        lignes.append(r"  \draw[otOrange!85!black,line width=0.8pt,-{Stealth[length=1.6mm]}] ([xshift=-1.5pt]c%d-%d.south) -- ([xshift=3.5pt]c%d-%d.north);" % (n - 1, k, n, k))
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


def _positions(rangees, pas=0.82, bilan=None, titre=None):
    """Rangées de cases de positions. rangees = [(liste de (style, texte)), étiquette à droite] ;
    bilan : ligne verte sous les rangées."""
    out = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    n = len(rangees[0][0])
    c = min(0.72, pas - 0.08)
    if titre:
        out.append(r"  \node[numPos,anchor=east] at (-0.5,0.66) {%s};" % titre)
    for i in range(n):
        out.append(r"  \node[numPos] at (%.2f,0.66) {%d};" % (i * pas, i + 1))
    for r, (cases, etiq) in enumerate(rangees):
        y = -r * 1.0
        for i, (st, tx) in enumerate(cases):
            out.append(r"  \node[%s,minimum width=%.2fcm,minimum height=%.2fcm] at (%.2f,%.2f) {%s};" % (st, c, c, i * pas, y, tx))
        out.append(r"  \node[anchor=west,font=\normalsize,text=otInk,inner sep=1pt] at (%.2f,%.2f) {%s};" % ((n - 1) * pas + c / 2 + 0.25, y, etiq))
    if bilan:
        out.append(r"  \node[bilan,anchor=north west] at (-0.36,%.2f) {%s};" % (-(len(rangees) - 1) * 1.0 - 0.62, bilan))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)

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
  % pas du quadrillage = unité du repère (sinon le chemin ne suit pas les lignes)
  \draw[otRule,line width=0.6pt,xstep=1.05cm,ystep=1.05cm] (0,0) grid (4,3);
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

# ---------------------------------------------------------------- finition 2026-11-02


def _cases(titres, valeurs, notes=None, bilan="", pas=2.3):
    """Cases à remplir : un choix par case, on multiplie."""
    out = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    n = len(valeurs)
    for i, (t, v) in enumerate(zip(titres, valeurs)):
        x = i * pas
        out.append(r"  \node[titreCol] at (%.2f,0.86) {%s};" % (x, t))
        out.append(r"  \node[grandeCase] at (%.2f,0) {$%s$};" % (x, v))
        if notes:
            out.append(r"  \node[exemple,align=center] at (%.2f,-0.86) {%s};" % (x, notes[i]))
        if i < n - 1:
            out.append(r"  \node[fois] at (%.2f,0) {$\times$};" % ((i + 0.5) * pas))
    out.append(r"  \node[bilan,anchor=west,font=\large] at (%.2f,0) {%s};" % ((n - 1) * pas + 0.95, bilan))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


FIGURES.update({
# III (cours) et 1265 Q1 : podium, cases à remplir
"cases_podium": _cases(["or", "argent", "bronze"], ["10", "9", "8"],
                       [r"$10$ coureurs", r"il en reste $9$", r"il en reste $8$"], r"$=720$ podiums"),

# 1263 Q1 : menus
"cases_menu": _cases(["entrée", "plat", "dessert"], ["3", "5", "4"], None, r"$=60$ menus"),

# 1267 Q3 : nombres de 3 chiffres distincts (premier chiffre non nul)
"cases_nombre": _cases(["centaines", "dizaines", "unités"], ["9", "9", "8"],
                       [r"de $1$ à $9$\\(pas de $0$)", r"$0$ à $9$, sauf le\\chiffre des centaines", r"il reste $8$\\chiffres"],
                       r"$=648$"),

# IV (cours) et 1266 Q1 : les k! ordres d'une même partie
"combinaison_ordres": r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \foreach \y/\t in {1.25/{(A\,;B\,;C)}, 0.75/{(A\,;C\,;B)}, 0.25/{(B\,;A\,;C)}, -0.25/{(B\,;C\,;A)}, -0.75/{(C\,;A\,;B)}, -1.25/{(C\,;B\,;A)}}
    \node[anchor=east,text=otNavy,inner sep=1pt] at (0,\y) {$\t$};
  \draw[otMuted,line width=0.7pt,decorate,decoration={brace,amplitude=5pt}] (0.18,1.45) -- (0.18,-1.45);
  \node[titreCol] at (-0.85,2.05) {$3$-uplets d’éléments\\distincts : l’ordre compte};
  \draw[fleche] (0.6,0) -- (2.5,0);
  \node[exemple,anchor=south,align=center] at (1.55,0.1) {on oublie\\l’ordre};
  \node[draw=otGreenDark,fill=otGreen!12,line width=0.8pt,rounded corners=2pt,inner sep=2.4mm,text=otGreenDark] at (3.75,0) {$\{A\,;B\,;C\}$};
  \node[titreCol] at (3.75,1.0) {une seule partie\\(une équipe)};
  \node[bilan,align=center,anchor=north] at (1.4,-1.75) {$3!=6$ triplets donnent la même partie :\\on divise le nombre de triplets par $3!$};
\end{tikzpicture}""",

# 1266 Q2 : symétrie, 3 pris = 7 laissés
"symetrie_10_3": r"""
\begin{tikzpicture}[x=1cm,y=1cm,
  pris/.style={circle,draw=otGreenDark,fill=otGreen!25,line width=0.9pt,minimum size=0.64cm,inner sep=0pt,font=\normalsize,text=otInk},
  laisse/.style={circle,draw=otMuted,fill=white,line width=0.6pt,minimum size=0.64cm,inner sep=0pt,font=\normalsize,text=otMuted}]
""" + "\n".join(r"  \node[%s] at (%.2f,0) {%d};" % ("pris" if i in (2, 5, 9) else "laisse", (i - 1) * 0.86, i) for i in range(1, 11)) + r"""
  \node[pris,minimum size=0.42cm] at (0.3,-0.95) {};
  \node[anchor=west,font=\normalsize,text=otGreenDark,inner sep=1pt] at (0.6,-0.95) {$3$ éléments pris};
  \node[laisse,minimum size=0.42cm] at (4.3,-0.95) {};
  \node[anchor=west,font=\normalsize,text=otMuted,inner sep=1pt] at (4.6,-0.95) {$7$ éléments laissés};
  \node[bilan,anchor=north] at (3.87,-1.45) {choisir les $3$ pris $=$ choisir les $7$ laissés : $\dbinom{10}{3}=\dbinom{10}{7}$};
\end{tikzpicture}""",

# 1263 Q2 : les 36 couples de deux dés distingués
"tableau_des": r"""
\begin{tikzpicture}[x=0.74cm,y=0.74cm]
  \fill[otGreen!40] (4,-1) rectangle (5,-2);
  \fill[otOrange!40] (1,-4) rectangle (2,-5);
  \foreach \k in {0,...,6}{
    \draw[otRule,line width=0.6pt] (\k,0) -- (\k,-6);
    \draw[otRule,line width=0.6pt] (0,-\k) -- (6,-\k);
  }
  \foreach \i in {1,...,6}{
    \node[font=\otMedium\fontsize{9}{10}\selectfont,text=otNavy,inner sep=1pt] at (\i-0.5,0.38) {\i};
    \node[font=\otMedium\fontsize{9}{10}\selectfont,text=otRed!80!black,inner sep=1pt] at (-0.38,-\i+0.5) {\i};
    \foreach \j in {1,...,6}
      \fill[otMuted!70] (\j-0.5,-\i+0.5) circle (1.5pt);
  }
  \node[titreCol,text=otNavy] at (3,1.05) {dé bleu};
  \node[titreCol,text=otRed!80!black,rotate=90] at (-1.05,-3) {dé rouge};
  \fill[otGreen!40] (0,-6.75) rectangle (0.5,-7.25);
  \node[anchor=west,font=\normalsize,inner sep=1pt] at (0.7,-7) {$(2\,;5)$ : rouge $2$, bleu $5$};
  \fill[otOrange!40] (0,-7.65) rectangle (0.5,-8.15);
  \node[anchor=west,font=\normalsize,inner sep=1pt] at (0.7,-7.9) {$(5\,;2)$ : rouge $5$, bleu $2$};
  \node[bilan,anchor=west] at (-0.1,-8.95) {$6\times6=36$ résultats};
\end{tikzpicture}""",

# 1268 Q1 : 2 rouges parmi 5 et 2 bleues parmi 3
"urne_tirage": r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \draw[otNavy,line width=1pt,rounded corners=9pt] (0,2.15) -- (0,0) -- (3.5,0) -- (3.5,2.15);
  \foreach \x/\y in {0.55/0.45, 1.25/0.45, 1.95/0.45, 0.9/1.12, 1.6/1.12}
    \node[bouleR] at (\x,\y) {R};
  \foreach \x/\y in {2.65/0.45, 2.3/1.12, 3.0/1.12}
    \node[bouleB] at (\x,\y) {B};
  \foreach \x/\y in {0.55/0.45, 1.6/1.12, 2.65/0.45, 3.0/1.12}
    \draw[choisie] (\x,\y) circle (0.38);
  \node[exemple] at (1.75,-0.38) {$5$ rouges et $3$ bleues};
  \node[anchor=west,inner sep=1pt] at (4.0,1.6) {$\dbinom{5}{2}=10$ choix des $2$ rouges};
  \node[anchor=west,inner sep=1pt] at (4.0,0.55) {$\dbinom{3}{2}=3$ choix des $2$ bleues};
  \node[bilan,anchor=west] at (4.0,-0.38) {$10\times3=30$ tirages};
\end{tikzpicture}""",

# 1270 Q1 : passage au complémentaire (schéma non à l'échelle)
"complementaire_comites": r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \fill[otGreen!22] (0,0) rectangle (4.9,1.75);
  \fill[otOrange!22] (4.9,0) rectangle (8.6,1.75);
  \draw[otNavy,line width=0.6pt] (4.9,0) -- (4.9,1.75);
  \draw[otNavy,line width=0.6pt] (6.75,0) -- (6.75,1.75);
  \draw[otNavy,line width=0.8pt] (0,0) rectangle (8.6,1.75);
  \node[align=center,text=otGreenDark] at (2.45,0.875) {comités mixtes\\$53\,130-3\,003-252$\\$=49\,875$};
  \node[align=center] at (5.825,0.875) {que des\\hommes\\$3\,003$};
  \node[align=center] at (7.675,0.875) {que des\\femmes\\$252$};
  \draw[otMuted,line width=0.7pt,decorate,decoration={brace,amplitude=6pt}] (0,1.9) -- (8.6,1.9);
  \node[anchor=south,inner sep=1pt] at (4.3,2.18) {tous les comités : $\dbinom{25}{5}=53\,130$};
  \node[exemple] at (4.3,-0.4) {(schéma non à l’échelle)};
\end{tikzpicture}""",

# 1272 C2 : ranger 4 R, 3 B, 2 V en choisissant les positions
"positions_boules": _positions([
    ([("posN", "")] + [("posR", "R")] * 2 + [("posN", "")] * 2 + [("posR", "R"), ("posN", ""), ("posN", ""), ("posR", "R")],
     r"rouges : $\dbinom{9}{4}=126$"),
    ([("posB", "B"), ("posR", "R"), ("posR", "R"), ("posN", ""), ("posB", "B"), ("posR", "R"), ("posB", "B"), ("posN", ""), ("posR", "R")],
     r"bleues : $\dbinom{5}{3}=10$"),
    ([("posB", "B"), ("posR", "R"), ("posR", "R"), ("posV", "V"), ("posB", "B"), ("posR", "R"), ("posB", "B"), ("posV", "V"), ("posR", "R")],
     r"vertes : $1$"),
], pas=0.66, bilan=r"$126\times10\times1=1\,260$ rangements"),

# 1268 Q5 : positions des lettres puis remplissage
"positions_mdp": _positions([
    ([("posL", "L"), ("posC", "C"), ("posL", "L"), ("posL", "L"), ("posC", "C"), ("posC", "C")],
     r"positions : $\dbinom{6}{3}=20$"),
    ([("posL", "26"), ("posC", "10"), ("posL", "26"), ("posL", "26"), ("posC", "10"), ("posC", "10")],
     r"remplissage : $26^3\times10^3$"),
], pas=0.82, bilan=r"$20\times26^3\times10^3=351\,520\,000$"),

# 1269 Q4 : anagrammes de BANANE
"positions_banane": _positions([
    ([("posN", ""), ("posB", "A"), ("posN", ""), ("posB", "A"), ("posN", ""), ("posN", "")],
     r"les A : $\dbinom{6}{2}=15$"),
    ([("posN", ""), ("posB", "A"), ("posV", "N"), ("posB", "A"), ("posV", "N"), ("posN", "")],
     r"les N : $\dbinom{4}{2}=6$"),
    ([("posR", "B"), ("posB", "A"), ("posV", "N"), ("posB", "A"), ("posV", "N"), ("posR", "E")],
     r"B et E : $2!=2$"),
], pas=0.82, bilan=r"$15\times6\times2=180$ anagrammes"),

# 1271 Q1 : chemins de O(0 ; 0) à B(5 ; 4) passant par C(2 ; 2) — énoncé et corrigé
"chemins_enonce": r"""
\begin{tikzpicture}[x=0.95cm,y=0.95cm]
  \foreach \k in {0,...,5} \draw[otRule,line width=0.6pt] (\k,0) -- (\k,4);
  \foreach \k in {0,...,4} \draw[otRule,line width=0.6pt] (0,\k) -- (5,\k);
  \foreach \p in {(0,0),(2,2),(5,4)} \fill[otNavy] \p circle (2.6pt);
  \node[anchor=north east,inner sep=1pt] at (-0.06,-0.06) {$O$};
  \node[anchor=south east,inner sep=1pt] at (1.94,2.06) {$C$};
  \node[anchor=south west,inner sep=1pt] at (5.06,4.06) {$B$};
  \draw[otGreenDark,line width=0.9pt,-{Stealth[length=2mm]}] (-0.9,1.3) -- (-0.2,1.3);
  \node[anchor=south,font=\otMedium\fontsize{9}{10}\selectfont,text=otGreenDark] at (-0.55,1.42) {D};
  \draw[otGreenDark,line width=0.9pt,-{Stealth[length=2mm]}] (-0.55,2.2) -- (-0.55,2.9);
  \node[anchor=east,font=\otMedium\fontsize{9}{10}\selectfont,text=otGreenDark] at (-0.68,2.55) {H};
\end{tikzpicture}""",

"chemins_corrige": r"""
\begin{tikzpicture}[x=0.95cm,y=0.95cm]
  \fill[otGreen!16] (0,0) rectangle (2,2);
  \fill[otOrange!20] (2,2) rectangle (5,4);
  \foreach \k in {0,...,5} \draw[otRule,line width=0.6pt] (\k,0) -- (\k,4);
  \foreach \k in {0,...,4} \draw[otRule,line width=0.6pt] (0,\k) -- (5,\k);
  \draw[otGreenDark,line width=2.2pt,line cap=round,line join=round] (0,0) -- (1,0) -- (1,1) -- (2,1) -- (2,2) -- (3,2) -- (3,3) -- (5,3) -- (5,4);
  \foreach \p in {(0,0),(2,2),(5,4)} \fill[otNavy] \p circle (2.6pt);
  \node[anchor=north east,inner sep=1pt] at (-0.06,-0.06) {$O$};
  \node[anchor=south east,inner sep=1pt] at (1.94,2.06) {$C$};
  \node[anchor=south west,inner sep=1pt] at (5.06,4.06) {$B$};
  \fill[otGreen!16] (0,-0.81) rectangle (0.42,-1.19);
  \node[anchor=west,inner sep=1pt] at (0.55,-1.0) {de $O$ à $C$ : $\dbinom{4}{2}=6$ chemins};
  \fill[otOrange!20] (0,-1.86) rectangle (0.42,-2.24);
  \node[anchor=west,inner sep=1pt] at (0.55,-2.05) {de $C$ à $B$ : $\dbinom{5}{2}=10$ chemins};
  \node[bilan,anchor=west] at (-0.05,-2.95) {par $C$ : $6\times10=60$ chemins};
\end{tikzpicture}""",

# nouveau-1, Partie A : 1 défectueux parmi 4 et 2 bons parmi 16
"lot_composants": r"""
\begin{tikzpicture}[x=1cm,y=1cm,
  def/.style={draw=otOrange!85!black,fill=otOrange!22,line width=0.7pt,minimum size=0.5cm,inner sep=0pt,font=\otMedium\fontsize{8}{9}\selectfont,text=otInk},
  bon/.style={draw=otNavy,fill=otSky,line width=0.6pt,minimum size=0.5cm,inner sep=0pt,font=\otMedium\fontsize{8}{9}\selectfont,text=otInk},
  pris/.style={draw=otGreenDark,fill=otGreen!35,line width=1.5pt}]
""" + "\n".join(r"  \node[def%s] at (%.2f,%.2f) {D};" % (",pris" if i == 1 else "", (i % 2) * 0.66, 0.66 - (i // 2) * 0.66) for i in range(4))
    + "\n" + "\n".join(r"  \node[bon%s] at (%.2f,%.2f) {B};" % (",pris" if i in (5, 14) else "", 2.6 + (i % 4) * 0.66, 0.99 - (i // 4) * 0.66) for i in range(16)) + r"""
  \node[anchor=north,align=center,inner sep=1pt] at (0.33,-1.45) {$4$ défectueux\\[2pt]$\dbinom{4}{1}=4$};
  \node[anchor=north,align=center,inner sep=1pt] at (3.59,-1.45) {$16$ bons\\[2pt]$\dbinom{16}{2}=120$};
  \node[bilan,anchor=north] at (2.0,-3.05) {$4\times120=480$ prélèvements};
  \node[exemple,anchor=north,align=center] at (2.0,-3.7) {en vert : un prélèvement possible\\(1 défectueux, 2 bons)};
\end{tikzpicture}""",

# nouveau-1, Partie B : place du composant défectueux dans le triplet
"prelevement_positions": _positions([
    ([("posR", "D"), ("posB", "B"), ("posB", "B")], r"$4\times16\times16=1\,024$"),
    ([("posB", "B"), ("posR", "D"), ("posB", "B")], r"$16\times4\times16=1\,024$"),
    ([("posB", "B"), ("posB", "B"), ("posR", "D")], r"$16\times16\times4=1\,024$"),
], pas=0.82, bilan=r"$3\times1\,024=3\,072$ résultats", titre="tirage"),

# nouveau-2 : triangle de Pascal, ligne 7 à compléter (énoncé) puis complétée (corrigé)
"pascal_a_completer": _pascal(7, ligne_vide=7),
"pascal_complete": _pascal(7, ligne_verte=7, somme=(7, 3)),
})
