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


# =============================================================== enrichissement 2026-11-02
def conv(d1, d2):
    r = {}
    for a, p in d1.items():
        for b, s in d2.items():
            r[a + b] = r.get(a + b, 0) + p * s
    return r


def fr(x, chiffres=2):
    """Nombre décimal à virgule pour TikZ : 0.25 -> 0{,}25."""
    t = f"{x:.{chiffres}f}" if isinstance(x, float) else str(x)
    return t.replace(".", "{,}")


MARQUE_EX = (r"\draw[otOrange,line width=0.9pt,dash pattern=on 3pt off 2pt] (axis cs:1.1,0) -- (axis cs:1.1,0.43);"
             "\n" r"  \node[note,anchor=south,text=otOrange!70!black] at (axis cs:1.1,0.44) {$E(X)=1{,}1$};")


def n1_forain(corrige):
    """Loi de X (points) ; corrigé : loi de Y = 2X - 1 en vert, mêmes probabilités."""
    loiX = [(0, 0.4), (1, 0.3), (2, 0.2), (4, 0.1)]
    ax = (r"otBarres, clip=false, height=2.7cm, ymin=0, ymax=0.5, bar width=11pt, ytick={0.1,0.2,0.3,0.4}, "
          r"yticklabels={$0{,}1$,$0{,}2$,$0{,}3$,$0{,}4$}, enlarge x limits=false")
    b = [r"\begin{tikzpicture}",
         rf"""\begin{{axis}}[name=gx, {ax}, width=2.8cm, xmin=-0.7, xmax=4.7, xtick={{0,1,2,4}}]
  \addplot[ybar, bar shift=0pt, fill=otNavy!55, draw=otNavy] coordinates {{{coords(loiX)}}};
  {MARQUE_EX if corrige else ""}
  \node[note,anchor=north,text=otNavy] at (rel axis cs:0.5,-0.2) {{loi de $X$ (points)}};
\end{{axis}}"""]
    if corrige:
        loiY = [(2 * x - 1, p) for x, p in loiX]
        b.append(rf"""\begin{{axis}}[at={{(gx.south east)}}, anchor=south west, xshift=0.5cm, {ax}, yticklabels={{}}, width=4.8cm, xmin=-2.2, xmax=8.2, xtick={{-1,1,3,7}}]
  \addplot[ybar, bar shift=0pt, fill=otGreen!70, draw=otGreenDark] coordinates {{{coords(loiY)}}};
  \draw[otGreenDark,line width=0.9pt,dash pattern=on 3pt off 2pt] (axis cs:1.2,0) -- (axis cs:1.2,0.43);
  \node[note,anchor=south,text=otGreenDark] at (axis cs:1.2,0.44) {{$E(Y)=1{{,}}2$}};
  \node[note,anchor=north,text=otGreenDark] at (rel axis cs:0.5,-0.2) {{loi de $Y=2X-1$ (euros)}};
\end{{axis}}""")
    b.append(r"\end{tikzpicture}")
    return "\n".join(b)


def n2_qcm(corrige):
    """Cinq questions = cinq épreuves de Bernoulli ; corrigé : accolade N = X1 + ... + X5."""
    l = [r"\begin{tikzpicture}[x=1.45cm]"]
    for i in range(1, 6):
        l += [rf"\draw[otNavy,fill=otSky,line width=0.8pt,rounded corners=2pt] ({i - 0.42},0) rectangle ({i + 0.42},0.9);",
              rf"\node[text=otNavy] at ({i},0.62) {{$X_{i}$}};",
              rf"\node[note,fill=none] at ({i},0.24) {{Q{i}}};",
              (rf"\node[note,anchor=south,text=otGreenDark] at ({i},0.98) {{$p=\frac{{1}}{{4}}$}};" if corrige
               else rf"\node[note,anchor=south] at ({i},0.98) {{$4$ choix}};")]
    l.append(r"\node[note,anchor=east,align=right] at (0.5,0.45) {juste : $1$\\fausse : $0$};")
    if corrige:
        l += [r"\draw[decorate,decoration={brace,mirror,amplitude=6pt},otGreenDark,line width=0.9pt] (0.58,-0.12) -- (5.42,-0.12);",
              r"\node[anchor=north,text=otGreenDark] at (3,-0.42) {$N=X_1+X_2+X_3+X_4+X_5\sim\mathcal{B}\left(5\,;\frac{1}{4}\right)$};"]
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


LOI_N2 = {0: Fr(0)}
LOI_N2 = {0: Fr(1)}
for _ in range(5):
    LOI_N2 = conv(LOI_N2, {0: Fr(3, 4), 1: Fr(1, 4)})


def n2_loi():
    l = [r"\begin{tikzpicture}",
         r"""\begin{axis}[otBarres, clip=false, width=6.2cm, height=3cm, ymin=0, ymax=0.5, bar width=18pt, enlarge x limits=0.12,
  xtick={0,1,2,3,4,5}, xlabel={nombre $k$ de bonnes réponses}, ytick={0.1,0.2,0.3,0.4}, yticklabels={$0{,}1$,$0{,}2$,$0{,}3$,$0{,}4$}]""",
         rf"  \addplot[ybar, bar shift=0pt, fill=otMuted!35, draw=otMuted] coordinates {{{coords((k, LOI_N2[k]) for k in (0, 1))}}};",
         rf"  \addplot[ybar, bar shift=0pt, fill=otGreen!70, draw=otGreenDark] coordinates {{{coords((k, LOI_N2[k]) for k in range(2, 6))}}};"]
    for k in range(6):
        c = ",text=otGreenDark" if k >= 2 else ""
        l.append(rf"  \node[note,anchor=south{c}] at (axis cs:{k},{float(LOI_N2[k]):.4f}) {{${fr(round(float(LOI_N2[k]), 3), 3)}$}};")
    l += [r"  \node[note,anchor=west,text=otGreenDark,font=\otRegular\fontsize{9.5}{11}\selectfont] at (axis cs:2.6,0.36) {$P(N\geqslant2)=\frac{47}{128}\approx0{,}367$};",
          r"\end{axis}", r"\end{tikzpicture}"]
    return "\n".join(l)


def n3_des():
    """Deux dés indépendants : loi de X + Y ; même dé : X + Z = 7 (une seule valeur)."""
    ax = r"otBarres, clip=false, height=2.8cm, ymin=0, bar width=7pt, xtick={2,4,6,7,8,10,12}, xmin=1.3, xmax=12.7, enlarge x limits=false"
    return rf"""\begin{{tikzpicture}}
\begin{{axis}}[name=g1, {ax}, width=3.9cm, ymax=0.21, ytick={{0.0833333,0.166667}}, yticklabels={{$\frac{{3}}{{36}}$,$\frac{{6}}{{36}}$}}]
  \addplot[ybar, bar shift=0pt, fill=otNavy!55, draw=otNavy] coordinates {{{coords(sorted(DEUX.items()))}}};
  \node[note,anchor=south,text=otNavy] at (rel axis cs:0.5,1.02) {{dés indépendants : $X+Y$}};
  \node[note,anchor=north,text=otNavy] at (rel axis cs:0.5,-0.22) {{$V(X+Y)=\frac{{35}}{{6}}$}};
\end{{axis}}
\begin{{axis}}[at={{(g1.south east)}}, anchor=south west, xshift=0.75cm, {ax}, width=3.9cm, ymax=1.26, ytick={{0.5,1}}, yticklabels={{$0{{,}}5$,$1$}}]
  \addplot[ybar, bar shift=0pt, fill=otGreen!70, draw=otGreenDark] coordinates {{(7,1)}};
  \node[note,anchor=south,text=otGreenDark] at (rel axis cs:0.5,1.02) {{même dé : $X+Z=7$}};
  \node[note,anchor=north,text=otGreenDark] at (rel axis cs:0.5,-0.22) {{$V(X+Z)=0$}};
\end{{axis}}
\end{{tikzpicture}}"""


LOI_T4 = {2: Fr(1, 8), 6: Fr(3, 4), 10: Fr(1, 8)}


def n4_attente():
    return rf"""\begin{{tikzpicture}}
\begin{{axis}}[otBarres, clip=false, width=4.6cm, height=2.6cm, ymin=0, ymax=0.9, bar width=16pt, xmin=0.5, xmax=11.5, enlarge x limits=false,
  xtick={{2,6,10}}, xlabel={{durée $x$ (min)}}, ytick={{0.125,0.75}}, yticklabels={{$\frac{{1}}{{8}}$,$\frac{{3}}{{4}}$}}]
  \addplot[ybar, bar shift=0pt, fill=otNavy!55, draw=otNavy] coordinates {{{coords(sorted(LOI_T4.items()))}}};
\end{{axis}}
\end{{tikzpicture}}"""


def n4_panneau(n, nom, position, barre, bas=False):
    loi = {0: Fr(1)}
    for _ in range(n):
        loi = conv(loi, LOI_T4)
    pmax = float(max(loi.values()))
    sig = {1: "2", 4: "1", 25: r"0{,}4"}[n]
    pos = "" if position is None else f"at={{({position}.south west)}}, anchor=north west, yshift=-0.32cm,"
    ticks = r"xtick={2,4,6,8,10}, xticklabels={$2$,$4$,$6$,$8$,$10$}, xlabel={durée moyenne (min)}," if bas else r"xtick={2,4,6,8,10}, xticklabels={},"
    return rf"""
\begin{{axis}}[name={nom}, {pos} width=7.2cm, height=1.25cm, scale only axis, xmin=1.5, xmax=10.5, ymin=0, ymax={1.25 * pmax:.5f},
  axis y line=none, axis x line*=bottom, axis line style={{otMuted,line width=0.6pt}}, tick style={{otMuted,line width=0.5pt}},
  ticklabel style={{font=\otRegular\fontsize{{9}}{{10}}\selectfont,text=otMuted}}, label style={{font=\otRegular\fontsize{{9}}{{10}}\selectfont,text=otMuted}}, {ticks} ytick=\empty]
  \addplot[ybar, bar width={barre}, fill=otGreen!70, draw=otGreenDark, line width=0.3pt] coordinates {{{coords((s / n, p) for s, p in sorted(loi.items()))}}};
  \node[note,anchor=north west,text=otGreenDark] at (rel axis cs:0,1) {{$n={n}$ : $\sigma(M_{{{n}}})={sig}$}};
\end{{axis}}"""


def n5_arbre(corrige):
    """Arbre d'un contrat : sinistre S (0,03) puis grave G (1/3) ; corrigé : coûts et probabilités des chemins."""
    v = r"text=otGreenDark"
    l = [r"\begin{tikzpicture}[x=2.0cm,y=0.95cm]",
         r"\fill[otNavy] (0,0) circle (1.6pt);",
         r"\draw[otNavy,line width=0.8pt] (0,0) -- (0.86,0.92); \draw[otNavy,line width=0.8pt] (0,0) -- (0.86,-1.42);",
         r"\node[text=otNavy] at (1,1) {$S$}; \node[text=otNavy] at (1,-1.5) {$\overline{S}$};",
         r"\node[note,anchor=south east] at (0.4,0.5) {$0{,}03$}; \node[note,anchor=north east] at (0.4,-0.74) {$0{,}97$};",
         r"\draw[otNavy,line width=0.8pt] (1.14,1.08) -- (1.86,1.92); \draw[otNavy,line width=0.8pt] (1.14,0.92) -- (1.86,0.08);",
         r"\node[text=otNavy] at (2,2) {$G$}; \node[text=otNavy] at (2,0) {$\overline{G}$};",
         r"\node[note,anchor=south east] at (1.48,1.54) {$\frac{1}{3}$}; \node[note,anchor=north east] at (1.48,0.46) {$\frac{2}{3}$};"]
    if corrige:
        l += [rf"\node[anchor=west,{v}] at (2.15,2) {{$X=5\,000$ ; $p=0{{,}}03\times\frac{{1}}{{3}}=0{{,}}01$}};",
              rf"\node[anchor=west,{v}] at (2.15,0) {{$X=1\,000$ ; $p=0{{,}}03\times\frac{{2}}{{3}}=0{{,}}02$}};",
              rf"\node[anchor=west,{v}] at (1.2,-1.5) {{$X=0$ ; $p=0{{,}}97$}};"]
    else:
        l += [r"\node[note,anchor=west] at (2.2,2) {coût $5\,000$ euros};",
              r"\node[note,anchor=west] at (2.2,0) {coût $1\,000$ euros};",
              r"\node[note,anchor=west] at (1.2,-1.5) {coût $0$ euro};"]
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


def n6_defauts():
    p = Fr(4, 100)
    P = {k: comb(50, k) * p ** k * (1 - p) ** (50 - k) for k in range(9)}
    l = [r"\begin{tikzpicture}",
         r"""\begin{axis}[otBarres, clip=false, width=7cm, height=3.2cm, ymin=0, ymax=0.4, bar width=14pt, enlarge x limits=0.07,
  xtick={0,1,2,3,4,5,6,7,8}, xlabel={nombre $k$ de pièces défectueuses}, ytick={0.1,0.2,0.3}, yticklabels={$0{,}1$,$0{,}2$,$0{,}3$}]""",
         rf"  \addplot[ybar, bar shift=0pt, fill=otGreen!70, draw=otGreenDark] coordinates {{{coords((k, P[k]) for k in range(3))}}};",
         rf"  \addplot[ybar, bar shift=0pt, fill=otMuted!35, draw=otMuted] coordinates {{{coords((k, P[k]) for k in range(3, 9))}}};"]
    for k in range(5):
        c = ",text=otGreenDark" if k <= 2 else ""
        l.append(rf"  \node[note,anchor=south{c}] at (axis cs:{k},{float(P[k]):.4f}) {{${fr(round(float(P[k]), 3), 3)}$}};")
    l += [r"  \node[note,anchor=west,text=otGreenDark,font=\otRegular\fontsize{9.5}{11}\selectfont] at (axis cs:4.6,0.3) {$P(D\leqslant2)\approx0{,}677$};",
          r"\end{axis}", r"\end{tikzpicture}"]
    return "\n".join(l)


FIGURES.update({
    "n1_forain": n1_forain(False),
    "n1_forain_corrige": n1_forain(True),
    "n2_qcm": n2_qcm(False),
    "n2_qcm_corrige": n2_qcm(True),
    "n2_loi_corrige": n2_loi(),
    "n3_des_corrige": n3_des(),
    "n4_attente": n4_attente(),
    "n4_moyennes_corrige": r"\begin{tikzpicture}" + n4_panneau(1, "q1", None, "0.5") + n4_panneau(4, "q4", "q1", "0.45")
        + n4_panneau(25, "q25", "q4", "0.1", bas=True) + "\n" + r"\end{tikzpicture}",
    "n5_arbre": n5_arbre(False),
    "n5_arbre_corrige": n5_arbre(True),
    "n6_defauts_corrige": n6_defauts(),
})
