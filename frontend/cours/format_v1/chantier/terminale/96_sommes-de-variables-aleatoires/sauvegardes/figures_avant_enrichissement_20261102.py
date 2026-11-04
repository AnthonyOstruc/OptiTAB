# -*- coding: utf-8 -*-
"""Figures de la notion « Sommes de variables aléatoires » (Terminale), style des livres.

    python ../../../outils/figures_livre.py <dossier_notion> [nom …] [--planche]

Les lois (dés, binomiale) sont calculées exactement ici, puis injectées dans le TikZ.
"""
from fractions import Fraction as Fr
from math import comb


def loi_somme_des(n):
    """Loi exacte de la somme de n dés équilibrés : {somme: probabilité}."""
    loi = {0: Fr(1)}
    for _ in range(n):
        nouv = {}
        for s, p in loi.items():
            for f in range(1, 7):
                nouv[s + f] = nouv.get(s + f, 0) + p / 6
        loi = nouv
    return loi


def coords(paires):
    return " ".join(f"({x:.6g},{float(p):.6g})" for x, p in paires)


DEUX = loi_somme_des(2)
CINQ = loi_somme_des(5)


def panneau_moyenne(n, nom, position, largeur_barre, bas=False):
    loi = loi_somme_des(n)
    pmax = float(max(loi.values()))
    sigma = {1: r"1{,}71", 4: r"0{,}85", 16: r"0{,}43"}[n]
    pos = "" if position is None else f"at={{({position}.south west)}}, anchor=north west, yshift=-0.32cm,"
    ticks = r"xtick={1,2,3,3.5,4,5,6}, xticklabels={$1$,$2$,$3$,$3{,}5$,$4$,$5$,$6$}," if bas else r"xtick={1,2,3,4,5,6}, xticklabels={},"
    return rf"""
\begin{{axis}}[name={nom}, {pos} width=7.2cm, height=1.25cm, scale only axis, xmin=0.75, xmax=6.25, ymin=0, ymax={1.62 * pmax:.5f},
  axis y line=none, axis x line*=bottom, axis line style={{otMuted,line width=0.6pt}}, tick style={{otMuted,line width=0.5pt}},
  ticklabel style={{font=\otRegular\fontsize{{9}}{{10}}\selectfont,text=otMuted}}, {ticks} ytick=\empty]
  \addplot[ybar, bar width={largeur_barre}, fill=otNavy!55, draw=otNavy, line width=0.3pt] coordinates {{{coords((s / n, p) for s, p in sorted(loi.items()))}}};
  \draw[otOrange,line width=0.9pt,dash pattern=on 3pt off 2pt] (axis cs:3.5,0) -- (axis cs:3.5,{1.25 * pmax:.5f});
  \node[note,anchor=north west] at (rel axis cs:0,1) {{$n={n}$ : $\sigma(M_{{{n}}})\approx{sigma}$}};
\end{{axis}}"""


def schema_lineaire(corrige):
    """Valeurs de X (dé) et de 3X + 2 alignées : la moyenne suit la même transformation."""
    haut, bas = 1.7, 0.0
    lignes = [r"\begin{tikzpicture}[x=1.05cm]",
              rf"\draw[otMuted,line width=0.6pt] (0.55,{haut}) -- (6.45,{haut});",
              rf"\draw[otMuted,line width=0.6pt] (0.55,{bas}) -- (6.45,{bas});",
              rf"\node[anchor=east,text=otNavy] at (0.35,{haut}) {{$X$}};",
              rf"\node[anchor=east,text=otNavy] at (0.35,{bas}) {{$3X+2$}};"]
    for k in range(1, 7):
        lignes += [rf"\draw[-{{Stealth[length=4pt]}},otNavy!40,line width=0.6pt] ({k},{haut - 0.16}) -- ({k},{bas + 0.16});",
                   rf"\fill[otNavy] ({k},{haut}) circle (2pt); \fill[otNavy] ({k},{bas}) circle (2pt);",
                   rf"\node[anchor=south,font=\otRegular\fontsize{{9}}{{10}}\selectfont,text=otMuted] at ({k},{haut + 0.08}) {{${k}$}};",
                   rf"\node[anchor=north,font=\otRegular\fontsize{{9}}{{10}}\selectfont,text=otMuted] at ({k},{bas - 0.08}) {{${3 * k + 2}$}};"]
    lignes += [rf"\node[note,anchor=west,align=left] at (6.55,{(haut + bas) / 2}) {{× 3\\puis\\+ 2}};",
               rf"\draw[otOrange,line width=0.9pt,dash pattern=on 3pt off 2pt] (3.5,{haut}) -- (3.5,{haut + 0.62});",
               rf"\node[note,anchor=south,text=otOrange!70!black] at (3.5,{haut + 0.64}) {{$E(X)=3{{,}}5$}};"]
    if corrige:
        lignes += [rf"\draw[-{{Stealth[length=5pt]}},otGreenDark,line width=1.1pt] (3.5,{haut - 0.1}) -- (3.5,{bas + 0.1});",
                   rf"\draw[otGreenDark,line width=0.9pt,dash pattern=on 3pt off 2pt] (3.5,{bas}) -- (3.5,{bas - 0.62});",
                   rf"\node[note,anchor=north,text=otGreenDark] at (3.5,{bas - 0.64}) {{$E(3X+2)=3\times3{{,}}5+2=12{{,}}5$}};"]
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


def pieces(corrige):
    """Lois de X1 et X2 (Bernoulli 1/2) ; dans le corrigé, loi de S = X1 + X2."""
    axe = (r"otBarres, clip=false, width={w}, height=2.6cm, ymin=0, ymax=0.68, bar width=16pt, enlarge x limits={e}, "
           r"ytick={{0.25,0.5}}, yticklabels={yl}")
    blocs = [r"\begin{tikzpicture}"]
    for i, (nom, pos) in enumerate((("X_1", None), ("X_2", "a1"))):
        place = "" if pos is None else f"at={{({pos}.south east)}}, anchor=south west, xshift=0.45cm,"
        yl = r"{$\frac{1}{4}$,$\frac{1}{2}$}" if pos is None else "{}"
        blocs.append(rf"""\begin{{axis}}[name=a{i + 1}, {place} {axe.format(w="1.7cm", e="0.5", yl=yl)}, xtick={{0,1}}]
  \addplot[ybar, fill=otNavy!55, draw=otNavy] coordinates {{(0,0.5) (1,0.5)}};
  \node[note,anchor=south,text=otNavy] at (rel axis cs:0.5,1.0) {{loi de ${nom}$}};
\end{{axis}}""")
    if corrige:
        blocs.append(rf"""\begin{{axis}}[name=a3, at={{(a2.south east)}}, anchor=south west, xshift=0.75cm, {axe.format(w="2.6cm", e="0.25", yl="{}")}, xtick={{0,1,2}}]
  \addplot[ybar, fill=otGreen!70, draw=otGreenDark] coordinates {{(0,0.25) (1,0.5) (2,0.25)}};
  \node[note,anchor=south,text=otGreenDark] at (rel axis cs:0.5,1.0) {{loi de $S=X_1+X_2$}};
\end{{axis}}""")
    blocs.append(r"\end{tikzpicture}")
    return "\n".join(blocs)


def urne(corrige):
    """Urne de 8 boules : 3 rouges, 4 bleues, 1 verte ; corrigé : 7 sur 8 sont rouges ou bleues."""
    styles = [("otRed", "R")] * 3 + [("otNavy", "B")] * 4 + [("otGreenDark", "V")]
    lignes = [r"\begin{tikzpicture}[x=0.8cm]"]
    for i, (c, lettre) in enumerate(styles):
        x = i + (0.25 if i >= 3 else 0) + (0.25 if i >= 7 else 0)
        lignes.append(rf"\draw[{c},fill={c}!18,line width=0.8pt] ({x},0) circle (0.3cm); \node[text={c},font=\otMedium\fontsize{{9}}{{10}}\selectfont] at ({x},0) {{{lettre}}};")
    lignes += [r"\node[note,anchor=north,text=otRed!85!black] at (1,-0.42) {3 rouges};",
               r"\node[note,anchor=north,text=otNavy] at (4.75,-0.42) {4 bleues};",
               r"\node[note,anchor=north,text=otGreenDark] at (7.5,-0.42) {1 verte};"]
    if corrige:
        lignes += [r"\draw[decorate,decoration={brace,amplitude=5pt},otGreenDark,line width=0.9pt] (-0.3,0.45) -- (6.55,0.45);",
                   r"\node[note,anchor=south,text=otGreenDark,font=\otRegular\fontsize{9.5}{11}\selectfont] at (3.125,0.7) {rouge ou bleue : $7$ boules sur $8$, $P=\frac{7}{8}$};"]
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


FIGURES = {
# ---------------------------------------------------------------- cours
# loi d'un dé et loi de la somme de deux dés (même échelle)
"cours_deux_des": r"""
\begin{tikzpicture}
\begin{axis}[otBarres, clip=false, name=g, width=2.3cm, height=3cm, ymin=0, ymax=0.235, bar width=8pt,
  enlarge x limits=0.13, xtick={1,2,3,4,5,6},
  ytick={0.0555556,0.111111,0.166667}, yticklabels={$\frac{2}{36}$,$\frac{4}{36}$,$\frac{6}{36}$}]
  \addplot[ybar, fill=otNavy!55, draw=otNavy] coordinates {(1,0.166667) (2,0.166667) (3,0.166667) (4,0.166667) (5,0.166667) (6,0.166667)};
  \draw[otOrange,line width=0.9pt,dash pattern=on 3pt off 2pt] (axis cs:3.5,0) -- (axis cs:3.5,0.188);
  \node[note,anchor=south,text=otOrange!70!black] at (axis cs:3.5,0.19) {$E(X)=3{,}5$};
  \node[note,anchor=south,text=otNavy] at (rel axis cs:0.5,1.02) {un dé : $X$};
\end{axis}
\begin{axis}[otBarres, clip=false, at={(g.south east)}, anchor=south west, xshift=0.55cm, width=4.6cm, height=3cm,
  ymin=0, ymax=0.235, bar width=8pt, enlarge x limits=0.06, xtick={2,3,4,5,6,7,8,9,10,11,12},
  ytick={0.0555556,0.111111,0.166667}, yticklabels={}]
  \addplot[ybar, fill=otGreen!70, draw=otGreenDark] coordinates {""" + coords(sorted(DEUX.items())) + r"""};
  \draw[otOrange,line width=0.9pt,dash pattern=on 3pt off 2pt] (axis cs:7,0.172) -- (axis cs:7,0.188);
  \node[note,anchor=south,text=otOrange!70!black] at (axis cs:7,0.19) {$E(S)=7$};
  \node[note,anchor=south,text=otGreenDark] at (rel axis cs:0.5,1.02) {deux dés : $S=X+Y$};
\end{axis}
\end{tikzpicture}""",

# loi de la moyenne M_n de n dés, n = 1, 4, 16 : concentration autour de 3,5
"cours_moyennes": r"""
\begin{tikzpicture}""" + panneau_moyenne(1, "m1", None, "0.42") + panneau_moyenne(4, "m4", "m1", "0.15")
    + panneau_moyenne(16, "m16", "m4", "0.042", bas=True) + r"""
\end{tikzpicture}""",

# ------------------------------------------------- exercice 1287, question 2 (cinq dés)
"ex_cinq_des": r"""
\begin{tikzpicture}
\begin{axis}[otBarres, width=7.2cm, height=3.2cm, ymin=0, ymax=0.142, bar width=5.2pt, enlarge x limits=0.03,
  xtick={5,10,15,20,25,30}, xticklabels={$5$,$10$,$15$,$20$,$25$,$30$},
  ytick={0.05,0.1}, yticklabels={$0{,}05$,$0{,}1$}]
  \addplot[ybar, bar shift=0pt, fill=otMuted!35, draw=otMuted] coordinates {""" + coords((s, p) for s, p in sorted(CINQ.items()) if s < 20) + r"""};
  \addplot[ybar, bar shift=0pt, fill=otGreen!70, draw=otGreenDark] coordinates {""" + coords((s, p) for s, p in sorted(CINQ.items()) if 20 <= s <= 24) + r"""};
  \addplot[ybar, bar shift=0pt, fill=otOrange!80, draw=otOrange!80!black] coordinates {""" + coords((s, p) for s, p in sorted(CINQ.items()) if s >= 25) + r"""};
  \node[note,anchor=south] at (axis cs:11,0.112) {gain $0$ : $\approx0{,}6948$};
  \node[note,anchor=south,text=otGreenDark] at (axis cs:22,0.112) {gain $10$ : $\approx0{,}2728$};
  \node[note,anchor=south,text=otOrange!70!black] at (axis cs:28.2,0.045) {gain $20$};
  \node[note,anchor=north,text=otOrange!70!black] at (axis cs:28.2,0.045) {$\approx0{,}0324$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------- exercice 1287, question 4 (intervalle)
"ex_fluctuation": r"""
\begin{tikzpicture}
\begin{axis}[otBarres, width=7.2cm, height=3.2cm, ymin=0, ymax=0.083, bar width=2.2pt, enlarge x limits=0.02,
  xmin=0.47, xmax=0.73, scaled y ticks=false, xtick={0.5,0.55,0.6,0.65,0.7}, xticklabels={$0{,}50$,$0{,}55$,$0{,}60$,$0{,}65$,$0{,}70$},
  ytick={0.02,0.04}, yticklabels={$0{,}02$,$0{,}04$}, xlabel={fréquence $F$}]
  \addplot[ybar, bar shift=0pt, fill=otMuted!35, draw=otMuted, line width=0.2pt] coordinates {""" + coords((k / 200, comb(200, k) * 0.6 ** k * 0.4 ** (200 - k)) for k in range(94, 107)) + " " + coords((k / 200, comb(200, k) * 0.6 ** k * 0.4 ** (200 - k)) for k in range(134, 147)) + r"""};
  \addplot[ybar, bar shift=0pt, fill=otGreen!70, draw=otGreenDark, line width=0.2pt] coordinates {""" + coords((k / 200, comb(200, k) * 0.6 ** k * 0.4 ** (200 - k)) for k in range(107, 134)) + r"""};
  \draw[cote] (axis cs:0.5307,0.066) -- (axis cs:0.6693,0.066) node[midway,coteTexte,font=\otRegular\fontsize{8.5}{10}\selectfont] {$I$ : $\approx 95$ \%};
  \draw[otMuted!70,line width=0.4pt] (axis cs:0.5307,0.003) -- (axis cs:0.5307,0.07);
  \draw[otMuted!70,line width=0.4pt] (axis cs:0.6693,0.003) -- (axis cs:0.6693,0.07);
  \node[note,anchor=south east] at (axis cs:0.528,0.012) {$0{,}531$};
  \node[note,anchor=south west] at (axis cs:0.672,0.012) {$0{,}669$};
\end{axis}
\end{tikzpicture}""",

# ------------------------------------------------- exercice 1284, question 4 (linéarité)
"ex1284_lineaire": schema_lineaire(False),
"ex1284_lineaire_corrige": schema_lineaire(True),

# ------------------------------------------------- exercice 1285, question 2 (deux pièces)
"ex1285_pieces": pieces(False),
"ex1285_pieces_corrige": pieces(True),

# ------------------------------------------------- exercice 1286, question 2 (urne)
"ex1286_urne": urne(False),
"ex1286_urne_corrige": urne(True),

# ------------------------------------------------- exercice 1288, question E1 (composants)
"ex1288_composants_corrige": r"""
\begin{tikzpicture}
\begin{axis}[otBarres, width=6.4cm, height=3.4cm, ymin=0, ymax=0.68, bar width=20pt, enlarge x limits=0.14,
  xtick={0,1,2,3,4}, xlabel={nombre $k$ de composants qui fonctionnent},
  ytick={0.2,0.4}, yticklabels={$0{,}2$,$0{,}4$}]
  \addplot[ybar, bar shift=0pt, fill=otMuted!35, draw=otMuted] coordinates {""" + coords((k, comb(4, k) * Fr(85, 100) ** k * Fr(15, 100) ** (4 - k)) for k in range(3)) + r"""};
  \addplot[ybar, bar shift=0pt, fill=otGreen!70, draw=otGreenDark] coordinates {""" + coords((k, comb(4, k) * Fr(85, 100) ** k * Fr(15, 100) ** (4 - k)) for k in (3, 4)) + r"""};
  \node[note,anchor=south] at (axis cs:0,0.0005) {$0{,}0005$};
  \node[note,anchor=south] at (axis cs:1,0.0115) {$0{,}0115$};
  \node[note,anchor=south] at (axis cs:2,0.0975) {$0{,}0975$};
  \node[note,anchor=south,text=otGreenDark] at (axis cs:3,0.3685) {$0{,}3685$};
  \node[note,anchor=south,text=otGreenDark] at (axis cs:4,0.5220) {$0{,}5220$};
  \node[note,anchor=west,text=otGreenDark,font=\otRegular\fontsize{9.5}{11}\selectfont] at (axis cs:-0.45,0.5) {$P(N\geqslant3)\approx0{,}890$};
\end{axis}
\end{tikzpicture}""",
}
