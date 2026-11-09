# -*- coding: utf-8 -*-
"""Figures du formulaire de trigonométrie (ressources gratuites).

Compilation (style des livres, contrôle des chevauchements texte / trait) :

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/formulaires/trigonometrie --planche

Sortie : images/<nom>.png (240 ppp), affichées à la moitié de leur taille.
"""

PI = r"\pi"

# Repère et cercle communs : axes discrets, cercle bleu marine.
AXES = r"""
  \draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (-#R-0.45,0) -- (#R+0.55,0);
  \draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (0,-#R-0.45) -- (0,#R+0.55);
  \draw[otNavy,line width=1.1pt] (0,0) circle (#R);
  \fill[otInk] (0,0) circle (1.3pt);
"""


def axes(r):
    return AXES.replace("#R", str(r))


# ------------------------------------------------------------------ triangle rectangle
TRIANGLE_RECTANGLE = r"""
\begin{tikzpicture}
  \coordinate (A) at (0,0); \coordinate (B) at (5.4,0); \coordinate (C) at (5.4,3.1);
  \fill[otSky] (A) -- (B) -- (C) -- cycle;
  \draw[otGreenDark,line width=1.6pt] (A) -- (B);
  \draw[otOrange!85!black,line width=1.6pt] (B) -- (C);
  \draw[otNavy,line width=1.6pt] (A) -- (C);
  \angledroit[0.32]{A}{B}{C}
  \draw[otInk,line width=0.7pt] (0.95,0) arc (0:29.86:0.95);
  \node at (16:1.42) {$\alpha$};
  \node[anchor=north east,xshift=-1pt,yshift=-1pt] at (A) {$A$};
  \node[anchor=north west,xshift=1pt,yshift=-1pt] at (B) {$B$};
  \node[anchor=south west,xshift=1pt] at (C) {$C$};
  \node[anchor=north,yshift=-4pt,text=otGreenDark] at (2.7,0) {côté adjacent à $\alpha$};
  \node[anchor=west,xshift=6pt,text=otOrange!75!black,align=left] at (5.4,1.55) {côté\\opposé à $\alpha$};
  \node[anchor=south east,text=otNavy] at (2.05,1.5) {hypoténuse};
\end{tikzpicture}"""

# ------------------------------------------------------------------ premier quadrant
R1 = 4.8
CERCLE_VALEURS = r"""
\begin{tikzpicture}
  \draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (-0.35,0) -- (#R+1.7,0);
  \draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (0,-0.35) -- (0,#R+1.2);
  \draw[otNavy,line width=1.1pt] (#R,0) arc (0:90:#R);
  \foreach \a in {30,45,60} {
    \draw[guide] ({#R*cos(\a)},0) -- ({#R*cos(\a)},{#R*sin(\a)}) -- (0,{#R*sin(\a)});
    \draw[otNavy!45,line width=0.6pt] (0,0) -- (\a:#R);
  }
  \foreach \a in {0,30,45,60,90} \fill[otNavy] (\a:#R) circle (2.3pt);
  \fill[otInk] (0,0) circle (1.3pt);
  \node[anchor=north east,xshift=-1pt,yshift=-1pt] at (0,0) {$O$};
  % angles (en dehors de l'arc)
  \node[anchor=210,text=otNavy] at (30:#R+0.12) {$\frac{\pi}{6}$};
  \node[anchor=225,text=otNavy] at (45:#R+0.12) {$\frac{\pi}{4}$};
  \node[anchor=240,text=otNavy] at (60:#R+0.12) {$\frac{\pi}{3}$};
  \node[anchor=south west,text=otNavy,xshift=3pt,yshift=1pt] at (0,#R) {$\frac{\pi}{2}$};
  \node[anchor=south west,text=otNavy,xshift=3pt,yshift=1pt] at (#R,0) {$0$};
  % abscisses = cosinus
  \node[anchor=north,yshift=-3pt] at ({#R*0.5},0) {$\frac{1}{2}$};
  \node[anchor=north,yshift=-3pt] at ({#R*0.7071},0) {$\frac{\sqrt{2}}{2}$};
  \node[anchor=north,yshift=-3pt] at ({#R*0.8660},0) {$\frac{\sqrt{3}}{2}$};
  \node[anchor=north,yshift=-3pt] at (#R,0) {$1$};
  % ordonnées = sinus
  \node[anchor=east,xshift=-3pt] at (0,{#R*0.5}) {$\frac{1}{2}$};
  \node[anchor=east,xshift=-3pt] at (0,{#R*0.7071}) {$\frac{\sqrt{2}}{2}$};
  \node[anchor=east,xshift=-3pt] at (0,{#R*0.8660}) {$\frac{\sqrt{3}}{2}$};
  \node[anchor=east,xshift=-3pt] at (0,#R) {$1$};
  \node[note,anchor=north east,yshift=-3pt] at (#R+1.7,0) {cosinus};
  \node[note,anchor=north east,xshift=-4pt] at (0,#R+1.2) {sinus};
\end{tikzpicture}""".replace("#R", str(R1))

# ------------------------------------------------------------------ cercle complet
R2 = 3.3
ANGLES = [
    (0, r"0"), (30, r"\frac{\pi}{6}"), (45, r"\frac{\pi}{4}"), (60, r"\frac{\pi}{3}"),
    (90, r"\frac{\pi}{2}"), (120, r"\frac{2\pi}{3}"), (135, r"\frac{3\pi}{4}"), (150, r"\frac{5\pi}{6}"),
    (180, r"\pi"), (210, r"-\frac{5\pi}{6}"), (225, r"-\frac{3\pi}{4}"), (240, r"-\frac{2\pi}{3}"),
    (270, r"-\frac{\pi}{2}"), (300, r"-\frac{\pi}{3}"), (315, r"-\frac{\pi}{4}"), (330, r"-\frac{\pi}{6}"),
]
SPECIAUX = {
    0: r"anchor=south west,xshift=3pt,yshift=1pt",
    90: r"anchor=south west,xshift=3pt,yshift=1pt",
    180: r"anchor=south east,xshift=-3pt,yshift=1pt",
    270: r"anchor=north west,xshift=3pt,yshift=-1pt",
}


def cercle_complet():
    lignes = [r"\begin{tikzpicture}", axes(R2)]
    # cordes (mêmes sinus / mêmes cosinus) en pointillés discrets
    for v in (0.5, 0.7071, 0.8660):
        lignes.append(rf"  \draw[otRule,line width=0.5pt,dash pattern=on 2pt off 1.6pt] ({-R2}*{(1 - v * v) ** 0.5:.4f},{R2 * v:.4f}) -- ({R2}*{(1 - v * v) ** 0.5:.4f},{R2 * v:.4f});")
        lignes.append(rf"  \draw[otRule,line width=0.5pt,dash pattern=on 2pt off 1.6pt] ({-R2}*{(1 - v * v) ** 0.5:.4f},{-R2 * v:.4f}) -- ({R2}*{(1 - v * v) ** 0.5:.4f},{-R2 * v:.4f});")
    for a, tex in ANGLES:
        lignes.append(rf"  \fill[otNavy] ({a}:{R2}) circle (2.2pt);")
        if a in SPECIAUX:
            lignes.append(rf"  \node[{SPECIAUX[a]},text=otNavy] at ({a}:{R2}) {{${tex}$}};")
        else:
            lignes.append(rf"  \node[anchor={a + 180},text=otNavy,inner sep=2pt] at ({a}:{R2 + 0.1}) {{${tex}$}};")
    lignes.append(r"  \node[anchor=north east,xshift=-1pt,yshift=-1pt] at (0,0) {$O$};")
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


# ------------------------------------------------------------------ angles associés
R3 = 3.1
X = 28


def angles_associes():
    pts = [
        (X, r"x", "otNavy", f"anchor={X + 180}"),
        (-X, r"-x", "otGreenDark", f"anchor={180 - X}"),
        (180 - X, r"\pi-x", "otOrange!80!black", f"anchor={-X}"),
        (180 + X, r"\pi+x", "otRed", f"anchor={X}"),
        (90 - X, r"\frac{\pi}{2}-x", "otMuted!70!black", f"anchor={270 - X}"),
    ]
    lignes = [r"\begin{tikzpicture}", axes(R3)]
    lignes.append(rf"  \draw[otRule,line width=0.6pt,dash pattern=on 3pt off 2pt] (225:{R3 + 0.3}) -- (45:{R3 + 0.3});")
    lignes.append(rf"  \node[note,anchor=west] at (45:{R3 + 0.3}) {{$y=x$}};")
    for a, tex, coul, ancre in pts:
        lignes.append(rf"  \draw[{coul},line width=0.8pt] (0,0) -- ({a}:{R3});")
        lignes.append(rf"  \fill[{coul}] ({a}:{R3}) circle (2.4pt);")
        lignes.append(rf"  \node[{ancre},text={coul},inner sep=2.5pt] at ({a}:{R3 + 0.1}) {{${tex}$}};")
    lignes.append(rf"  \draw[otNavy,line width=0.7pt] (0.75,0) arc (0:{X}:0.75);")
    lignes.append(rf"  \node[text=otNavy] at ({X / 2}:1.08) {{$x$}};")
    lignes.append(r"  \node[anchor=north east,xshift=-1pt,yshift=-1pt] at (0,0) {$O$};")
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


# ------------------------------------------------------------------ triangle quelconque
TRIANGLE_QUELCONQUE = r"""
\begin{tikzpicture}
  \coordinate (A) at (0,0); \coordinate (B) at (5.6,0); \coordinate (C) at (1.7,3.2);
  \fill[otSky] (A) -- (B) -- (C) -- cycle;
  \draw[geoTrait,line width=1.2pt] (A) -- (B) -- (C) -- cycle;
  \pic[draw=otNavy,line width=0.7pt,angle radius=0.62cm] {angle=B--A--C};
  \pic[draw=otNavy,line width=0.7pt,angle radius=0.62cm] {angle=C--B--A};
  \pic[draw=otNavy,line width=0.7pt,angle radius=0.5cm] {angle=A--C--B};
  \node[text=otNavy] at ($(A)+(31:0.98)$) {$\widehat{A}$};
  \node[text=otNavy] at ($(B)+(160:1.12)$) {$\widehat{B}$};
  \node[text=otNavy] at ($(C)+(-83:0.92)$) {$\widehat{C}$};
  \node[anchor=north east,xshift=-1pt,yshift=-1pt] at (A) {$A$};
  \node[anchor=north west,xshift=1pt,yshift=-1pt] at (B) {$B$};
  \node[anchor=south,yshift=2pt] at (C) {$C$};
  \node[anchor=north,yshift=-3pt] at ($(A)!0.5!(B)$) {$c$};
  \node[anchor=south west,xshift=2pt,yshift=2pt] at ($(B)!0.5!(C)$) {$a$};
  \node[anchor=south east,xshift=-2pt,yshift=1pt] at ($(A)!0.5!(C)$) {$b$};
\end{tikzpicture}"""

# ------------------------------------------------------------------ courbes
COURBES = r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=8.2cm, height=3.1cm, xmin=-6.9, xmax=7.3, ymin=-1.6, ymax=1.95,
  xtick={-6.2832,-3.1416,3.1416,6.2832}, xticklabels={$-2\pi$,$-\pi$,$\pi$,$2\pi$},
  minor xtick={-4.7124,-1.5708,1.5708,4.7124}, minor grid style={otRule!45,line width=0.3pt}, minor tick length=0pt,
  ytick={-1,1}]
  \addplot[courbe2, domain=-6.9:7.1] {cos(x)};
  \addplot[courbe, domain=-6.9:7.1] {sin(x)};
  \node[etiq,text=otNavy,anchor=south] at (axis cs:1.5708,1.12) {$y=\sin x$};
  \node[etiq,text=otGreenDark,anchor=south] at (axis cs:-3.1416,1.12) {$y=\cos x$};
  \draw[otMuted,line width=0.6pt,{Stealth[length=1.8mm]}-{Stealth[length=1.8mm]}] (axis cs:0,-1.36) -- (axis cs:6.2832,-1.36)
    node[note,midway,below=2pt,fill=none] {période $2\pi$};
\end{axis}
\end{tikzpicture}"""

FIGURES = {
    "triangle_rectangle": TRIANGLE_RECTANGLE,
    "cercle_valeurs": CERCLE_VALEURS,
    "cercle_complet": cercle_complet(),
    "angles_associes": angles_associes(),
    "triangle_quelconque": TRIANGLE_QUELCONQUE,
    "courbes_sin_cos": COURBES,
}

XLAB = {
    "courbes_sin_cos": [(-6.2832, "d", r"-2\pi"), (-3.1416, "g", r"-\pi"), (3.1416, "g", r"\pi"), (6.2832, "d", r"2\pi")],
}
