# -*- coding: utf-8 -*-
"""Figures de la notion « Arithmétique » (Terminale, Maths expertes), style des livres.

Compilation : python outils/figures_livre.py chantier/terminale/103_arithmetique [nom …] [--planche]
Toutes les valeurs écrites sur les figures sont recalculées dans verif_arithmetique.py.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  residu/.style={circle,draw=otNavy,line width=0.9pt,fill=otSky,minimum size=0.8cm,inner sep=0pt,text=otNavy},
  residuUn/.style={circle,draw=otGreenDark,line width=1pt,fill=otGreen!22,minimum size=0.8cm,inner sep=0pt,text=otGreenDark},
  fleche/.style={otNavy!80,line width=0.8pt,-{Stealth[length=2.1mm]}},
  compose/.style={rectangle,rounded corners=2pt,draw=otNavy!70,line width=0.7pt,fill=otSky,text=otNavy,inner sep=3pt,minimum height=0.6cm},
  premier/.style={circle,draw=otGreenDark,line width=0.9pt,fill=otGreen!20,text=otGreenDark,inner sep=0pt,minimum size=0.6cm},
  branche/.style={otMuted,line width=0.7pt},
}
"""


def cycle(base, mod, rayon, haut_label=None):
    """Cycle des restes de base^k modulo mod (k = 0 … période − 1), parcouru dans le sens horaire."""
    vals = []
    v = 1
    while True:
        vals.append(v)
        v = v * base % mod
        if v == 1:
            break
    p = len(vals)
    r_noeud = 0.4
    d = math.degrees((r_noeud + 0.09) / rayon)  # écart angulaire pour ne pas toucher les disques
    out = [r"\begin{tikzpicture}"]
    for k in range(p):
        a1 = 90 - 360 * k / p
        a2 = 90 - 360 * (k + 1) / p
        out.append(rf"  \draw[fleche] ({a1 - d:.3f}:{rayon}) arc[start angle={a1 - d:.3f}, end angle={a2 + d:.3f}, radius={rayon}cm];")
    for k, val in enumerate(vals):
        a = 90 - 360 * k / p
        style = "residuUn" if k == 0 else "residu"
        out.append(rf"  \node[{style}] at ({a:.3f}:{rayon}) {{${val}$}};")
        lab = haut_label if (k == 0 and haut_label) else rf"{base}^{{{k}}}"
        out.append(rf"  \node[text=otMuted,anchor={(a + 180) % 360:.3f},inner sep=1pt] at ({a:.3f}:{rayon + 0.5}) {{${lab}$}};")
    out.append(rf"  \node[text=otNavy] at (0,0.22) {{$\times\,{base}$}};")
    out.append(rf"  \node[note] at (0,-0.3) {{modulo ${mod}$}};")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def crible(n_max=100, colonnes=10):
    premiers = [k for k in range(2, n_max + 1) if all(k % d for d in range(2, int(k ** 0.5) + 1))]
    lignes = n_max // colonnes
    out = [r"\begin{tikzpicture}[x=0.8cm,y=0.62cm]"]
    for k in range(1, n_max + 1):
        c, l = (k - 1) % colonnes, (k - 1) // colonnes
        if k in premiers:
            out.append(rf"  \fill[otNavy!13] ({c},{-l}) rectangle ({c + 1},{-l - 1});")
    for c in range(1, colonnes):
        out.append(rf"  \draw[otRule,line width=0.6pt] ({c},0) -- ({c},{-lignes});")
    for l in range(1, lignes):
        out.append(rf"  \draw[otRule,line width=0.6pt] (0,{-l}) -- ({colonnes},{-l});")
    out.append(rf"  \draw[otMuted!70,line width=0.8pt] (0,0) rectangle ({colonnes},{-lignes});")
    for k in range(1, n_max + 1):
        c, l = (k - 1) % colonnes, (k - 1) // colonnes
        if k in premiers:
            out.append(rf"  \node[text=otNavy,font=\bfseries] at ({c + 0.5},{-l - 0.5}) {{{k}}};")
        else:
            out.append(rf"  \node[text=otMuted!65] at ({c + 0.5},{-l - 0.5}) {{{k}}};")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


FIGURES = {
# ------------------------------------------------------------------ cours
# Division euclidienne de -17 par 4 lue sur la droite des entiers
"division_droite": r"""
\begin{tikzpicture}[x=0.75cm,y=1cm]
  \draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (-22.3,0) -- (-13.2,0);
  \foreach \k in {-22,-21,-19,-18,-17,-15,-14} \draw[otMuted,line width=0.5pt] (\k,-0.07) -- (\k,0.07);
  \draw[otNavy,line width=0.8pt] (-20,-0.1) -- (-20,0.1);
  \draw[otNavy,line width=0.8pt] (-16,-0.1) -- (-16,0.1);
  \fill[otNavy] (-20,0) circle (2.5pt);
  \fill[otNavy] (-16,0) circle (2.5pt);
  \draw[otGreenDark,line width=0.8pt,decorate,decoration={brace,amplitude=5pt,raise=5pt}] (-20,0) -- (-17,0);
  \node[text=otGreenDark,anchor=south] at (-18.5,0.45) {$r=3$};
  \fill[otGreenDark] (-17,0) circle (2.5pt);
  \node[text=otGreenDark,anchor=south west,inner sep=1pt] at (-16.88,0.14) {$a=-17$};
  \node[text=otNavy,anchor=north] at (-20,-0.2) {$4\times(-5)=-20$};
  \node[text=otNavy,anchor=north] at (-16,-0.2) {$4\times(-4)=-16$};
\end{tikzpicture}""",

# Algorithme d'Euclide pour 252 et 198 : pavage du rectangle par des carrés
"euclide_carres": r"""
\begin{tikzpicture}[x=0.03cm,y=0.03cm]
  \fill[otNavy!7] (0,0) rectangle (198,198);
  \fill[otNavy!22] (198,0) rectangle (252,162);
  \fill[otOrange!35] (198,162) rectangle (234,198);
  \fill[otGreen!38] (234,162) rectangle (252,198);
  \draw[otNavy,line width=0.6pt] (198,0) -- (198,198);
  \draw[otNavy,line width=0.6pt] (198,54) -- (252,54) (198,108) -- (252,108) (198,162) -- (252,162);
  \draw[otNavy,line width=0.6pt] (234,162) -- (234,198) (234,180) -- (252,180);
  \draw[otNavy,line width=1pt] (0,0) rectangle (252,198);
  \node[text=otNavy] at (225,27) {$54$};
  \node[text=otNavy] at (225,81) {$54$};
  \node[text=otNavy] at (225,135) {$54$};
  \node[text=otInk] at (216,180) {$36$};
  \node[text=otGreenDark,font=\small\bfseries,inner sep=0pt] at (243,171) {$18$};
  \node[text=otGreenDark,font=\small\bfseries,inner sep=0pt] at (243,189) {$18$};
  % divisions successives, avec la couleur des carrés correspondants
  \begin{scope}[shift={(24,152)}]
    \fill[otNavy!7] (0,-6) rectangle (12,6); \draw[otNavy,line width=0.5pt] (0,-6) rectangle (12,6);
    \node[anchor=west,text=otInk] at (18,0) {$252=198\times1+54$};
    \fill[otNavy!22] (0,-36) rectangle (12,-24); \draw[otNavy,line width=0.5pt] (0,-36) rectangle (12,-24);
    \node[anchor=west,text=otInk] at (18,-30) {$198=54\times3+36$};
    \fill[otOrange!35] (0,-66) rectangle (12,-54); \draw[otNavy,line width=0.5pt] (0,-66) rectangle (12,-54);
    \node[anchor=west,text=otInk] at (18,-60) {$54=36\times1+18$};
    \fill[otGreen!38] (0,-96) rectangle (12,-84); \draw[otNavy,line width=0.5pt] (0,-96) rectangle (12,-84);
    \node[anchor=west,text=otInk] at (18,-90) {$36=18\times2+0$};
    \node[anchor=west,text=otGreenDark] at (-2,-124) {$\mathrm{PGCD}(252,198)=18$};
  \end{scope}
  % cotes
  \draw[cote] (0,-14) -- (252,-14) node[midway,coteTexte] {$252$};
  \draw[otMuted!70,line width=0.4pt] (0,-2) -- (0,-18) (252,-2) -- (252,-18);
  \draw[cote] (-14,0) -- (-14,198) node[midway,coteTexte] {$198$};
  \draw[otMuted!70,line width=0.4pt] (-2,0) -- (-18,0) (-2,198) -- (-18,198);
\end{tikzpicture}""",

# Restes des puissances de 3 modulo 7 (cours et devoir surveillé)
"cycle_3_mod7": cycle(3, 7, 1.85, haut_label=r"3^0,\ 3^6,\ 3^{12}\dots"),

# Crible d'Ératosthène jusqu'à 100
"crible_100": crible(100),

# Arbre de décomposition de 360
"arbre_360": r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \node[compose] (a) at (0,0) {$360$};
  \node[premier] (p1) at (-0.85,-1) {$2$};
  \node[compose] (b) at (0.85,-1) {$180$};
  \node[premier] (p2) at (0,-2) {$2$};
  \node[compose] (c) at (1.7,-2) {$90$};
  \node[premier] (p3) at (0.85,-3) {$2$};
  \node[compose] (d) at (2.55,-3) {$45$};
  \node[premier] (p4) at (1.7,-4) {$3$};
  \node[compose] (e) at (3.4,-4) {$15$};
  \node[premier] (p5) at (2.55,-5) {$3$};
  \node[premier] (p6) at (4.25,-5) {$5$};
  \draw[branche] (a) -- (p1) (a) -- (b) (b) -- (p2) (b) -- (c) (c) -- (p3) (c) -- (d)
                 (d) -- (p4) (d) -- (e) (e) -- (p5) (e) -- (p6);
  \node[text=otGreenDark] at (1.7,-5.95) {$360=2^3\times3^2\times5$};
\end{tikzpicture}""",

# ------------------------------------------------------------------ exercices
# « Périodicité des puissances » : 3^n modulo 10 et 7^n modulo 11
"cycle_3_mod10": cycle(3, 10, 1.5, haut_label=r"3^0,\ 3^4,\ 3^8\dots"),
"cycle_7_mod11": cycle(7, 11, 2.25, haut_label=r"7^0,\ 7^{10}\dots"),
# « Restes de puissances » : 7^n modulo 10
"cycle_7_mod10": cycle(7, 10, 1.5, haut_label=r"7^0,\ 7^4,\ 7^8\dots"),
}


# =================================================================== FINITION 2026-11-02
def nombre(n):
    """Écriture française d'un entier (espace fine des milliers)."""
    s = str(abs(n))
    g = []
    while len(s) > 3:
        g.insert(0, s[-3:])
        s = s[:-3]
    g.insert(0, s)
    return ("-" if n < 0 else "") + r"\,".join(g)


def euclide_pavage(a, b, u, titre=True):
    """Rectangle a × b pavé par les carrés de l'algorithme d'Euclide, divisions en légende à droite."""
    couleurs = ["otNavy!7", "otNavy!22", "otOrange!35", "otGreen!38", "otNavy!12"]
    carres, divisions = [], []
    x, y, w, h, etape = 0, 0, a, b, 0
    while w > 0 and h > 0:
        if w >= h:
            q, r = divmod(w, h)
            carres += [(x + i * h, y, h, etape) for i in range(q)]
            divisions.append((w, h, q, r))
            x, w = x + q * h, r
        else:
            q, r = divmod(h, w)
            carres += [(x, y + i * w, w, etape) for i in range(q)]
            divisions.append((h, w, q, r))
            y, h = y + q * w, r
        etape += 1
    der = etape - 1
    out = [rf"\begin{{tikzpicture}}[x={u}cm,y={u}cm]"]
    for (cx, cy, c, e) in carres:
        coul = "otGreen!38" if e == der else couleurs[e]
        out.append(rf"  \fill[{coul}] ({cx},{cy}) rectangle ({cx + c},{cy + c});")
        out.append(rf"  \draw[otNavy,line width=0.6pt] ({cx},{cy}) rectangle ({cx + c},{cy + c});")
        if c * u >= 0.62:
            txt = "otGreenDark" if e == der else "otInk"
            out.append(rf"  \node[text={txt},font=\small] at ({cx + c / 2},{cy + c / 2}) {{${c}$}};")
    out.append(rf"  \draw[otNavy,line width=1pt] (0,0) rectangle ({a},{b});")
    # cotes
    out.append(rf"  \draw[cote] (0,{-0.3 / u:.2f}) -- ({a},{-0.3 / u:.2f}) node[midway,coteTexte] {{${a}$}};")
    out.append(rf"  \draw[otMuted!70,line width=0.4pt] (0,{-0.05 / u:.2f}) -- (0,{-0.4 / u:.2f}) ({a},{-0.05 / u:.2f}) -- ({a},{-0.4 / u:.2f});")
    out.append(rf"  \draw[cote] ({-0.3 / u:.2f},0) -- ({-0.3 / u:.2f},{b}) node[midway,coteTexte] {{${b}$}};")
    out.append(rf"  \draw[otMuted!70,line width=0.4pt] ({-0.05 / u:.2f},0) -- ({-0.4 / u:.2f},0) ({-0.05 / u:.2f},{b}) -- ({-0.4 / u:.2f},{b});")
    # légende : une division par ligne, pastille de la couleur des carrés
    x0 = a + 0.55 / u
    pas = 0.62 / u
    y0 = b - 0.25 / u
    for k, (dd, dv, q, r) in enumerate(divisions):
        coul = "otGreen!38" if k == der else couleurs[k]
        yy = y0 - k * pas
        s = 0.11 / u
        out.append(rf"  \fill[{coul}] ({x0},{yy - s}) rectangle ({x0 + 2 * s},{yy + s});")
        out.append(rf"  \draw[otNavy,line width=0.5pt] ({x0},{yy - s}) rectangle ({x0 + 2 * s},{yy + s});")
        out.append(rf"  \node[anchor=west,text=otInk] at ({x0 + 2 * s + 0.12 / u},{yy}) {{${dd} = {dv} \times {q} + {r}$}};")
    pg = divisions[-1][1]
    out.append(rf"  \node[anchor=west,text=otGreenDark] at ({x0 - 0.05 / u},{y0 - len(divisions) * pas - 0.08 / u}) {{$\mathrm{{PGCD}}({a}, {b}) = {pg}$}};")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def euclide_tableau(a, b):
    """Algorithme d'Euclide en tableau : a = b × q + r, le diviseur et le reste descendent d'une ligne."""
    lignes = []
    while b:
        q, r = divmod(a, b)
        lignes.append((a, b, q, r))
        a, b = b, r
    X = [0, 1.7, 3.4, 5.1]
    dy = 0.95
    out = [r"\begin{tikzpicture}[cel/.style={minimum width=1.2cm,minimum height=0.62cm,inner sep=0pt}]"]
    for j, t in enumerate([r"dividende $a$", r"diviseur $b$", r"quotient $q$", r"reste $r$"]):
        out.append(rf"  \node[note,anchor=south] at ({X[j]},0.42) {{{t}}};")
    out.append(rf"  \draw[otMuted,line width=0.6pt] ({X[0] - 0.8},0.36) -- ({X[3] + 0.8},0.36);")
    der = len(lignes) - 2  # ligne du dernier reste non nul
    for i, ligne in enumerate(lignes):
        for j, v in enumerate(ligne):
            style = "cel"
            if j == 3 and i == der:
                style = r"cel,circle,draw=otGreenDark,line width=1.1pt,fill=otGreen!22,text=otGreenDark,minimum width=0.85cm,minimum height=0.85cm"
            out.append(rf"  \node[{style}] (c{i}{j}) at ({X[j]},{-i * dy}) {{${nombre(v)}$}};")
    for i in range(len(lignes) - 1):
        out.append(rf"  \draw[otNavy!45,line width=0.8pt,-{{Stealth[length=2mm]}},shorten <=1pt,shorten >=1pt] (c{i}1.south west) -- (c{i + 1}0.north east);")
        out.append(rf"  \draw[otOrange,line width=0.9pt,-{{Stealth[length=2mm]}},shorten <=3pt,shorten >=2pt] (c{i}3.south west) -- (c{i + 1}1.north east);")
    out.append(rf"  \node[text=otGreenDark,anchor=west] at ({X[3] + 0.62},{-der * dy}) {{PGCD}};")
    out.append(rf"  \node[note,anchor=west] at ({X[3] + 0.62},{-(der + 1) * dy}) {{reste nul : arrêt}};")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def schema_chiffrement(l1, x, y, l2, chif, dechif):
    """Deux lignes : chiffrement l1 → x → y → l2, puis déchiffrement l2 → y → x → l1."""
    out = [r"\begin{tikzpicture}[boite/.style={rectangle,rounded corners=2pt,draw=otNavy!70,line width=0.8pt,fill=otSky,minimum width=1.05cm,minimum height=0.72cm,inner sep=2pt,text=otNavy},"
           r"boiteV/.style={boite,draw=otGreenDark,fill=otGreen!20,text=otGreenDark},"
           r"fl/.style={otNavy!80,line width=0.9pt,-{Stealth[length=2.3mm]},shorten <=2pt,shorten >=2pt},"
           r"flV/.style={otGreenDark,line width=0.9pt,-{Stealth[length=2.3mm]},shorten <=2pt,shorten >=2pt}]"]
    X = [0, 2.0, 4.0, 6.0]
    def rangee(yy, vals, sous, styles, fl, nom):
        for k, v in enumerate(vals):
            out.append(rf"  \node[{styles[k]}] ({nom}{k}) at ({X[k]},{yy}) {{{v}}};")
            out.append(rf"  \node[note,anchor=north] at ({X[k]},{yy - 0.42}) {{{sous[k]}}};")
        for k in range(3):
            out.append(rf"  \draw[{fl}] ({nom}{k}) -- ({nom}{k + 1});")
    out.append(rf"  \node[anchor=south west,text=otNavy,inner sep=1pt] at ({X[0] - 0.55},0.48) {{\textbf{{Chiffrement}} : {chif}}};")
    rangee(0, [rf"${l1}$", f"${x}$", f"${y}$", rf"${l2}$"], ["lettre", "rang $x$", "rang $y$", "lettre codée"],
           ["boite", "boite", "boite", "boiteV"], "fl", "h")
    out.append(rf"  \node[anchor=south west,text=otGreenDark,inner sep=1pt] at ({X[0] - 0.55},-1.72) {{\textbf{{Déchiffrement}} : {dechif}}};")
    rangee(-2.2, [rf"${l2}$", f"${y}$", f"${x}$", rf"${l1}$"], ["lettre codée", "rang $y$", "rang $x$", "lettre"],
           ["boiteV", "boite", "boite", "boite"], "flV", "b")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


FIGURES.update({
# Classes de congruence modulo 5 : « l'horloge » à 5 positions (exercice 1145)
"horloge_mod5": r"""
\begin{tikzpicture}
  \foreach \k/\a in {0/90,1/18,2/-54,3/-126,4/162} {
    \draw[fleche] (\a-21:1.35) arc[start angle=\a-21, end angle=\a-51, radius=1.35cm];
  }
  \node[residu] at (90:1.35) {$0$};
  \node[residu] at (18:1.35) {$1$};
  \node[residuUn] at (-54:1.35) {$2$};
  \node[residu] at (-126:1.35) {$3$};
  \node[residu] at (162:1.35) {$4$};
  \node[text=otMuted,anchor=south,inner sep=1pt] at (90:1.85) {$0,\ 5,\ 10,\ 15,\ 20\dots$};
  \node[text=otMuted,anchor=west,inner sep=1pt] at (18:1.85) {$1,\ 6,\ 11,\ 16\dots$};
  \node[text=otGreenDark,anchor=north west,inner sep=1pt] at (-54:1.8) {$2,\ 7,\ 12,\ 17\dots$};
  \node[text=otMuted,anchor=north east,inner sep=1pt] at (-126:1.8) {$3,\ 8,\ 13,\ 18,\ 23\dots$};
  \node[text=otMuted,anchor=east,inner sep=1pt] at (162:1.85) {$4,\ 9,\ 14,\ 19\dots$};
  \node[text=otNavy] at (0,0.22) {$+1$};
  \node[note] at (0,-0.3) {modulo $5$};
\end{tikzpicture}""",

# Division euclidienne de 84 par 60 (exercice 1143)
"ex1143_division": r"""
\begin{tikzpicture}[x=0.085cm,y=1cm]
  \fill[otNavy!14] (0,0) rectangle (60,0.8);
  \fill[otGreen!32] (60,0) rectangle (84,0.8);
  \draw[otNavy,line width=0.8pt] (0,0) rectangle (84,0.8);
  \draw[otNavy,line width=0.8pt] (60,0) -- (60,0.8);
  \node[text=otNavy] at (30,0.4) {$60$};
  \node[text=otGreenDark] at (72,0.4) {$24$};
  \draw[otInk,line width=0.7pt,decorate,decoration={brace,amplitude=5pt}] (0,0.92) -- (84,0.92);
  \node[anchor=south] at (42,1.12) {$84$};
  \node[note,anchor=north] at (30,-0.1) {$60 \times 1$ (quotient $q = 1$)};
  \node[note,anchor=north,text=otGreenDark] at (72,-0.1) {reste $r = 24$};
  \node[note,anchor=north,text=otGreenDark] at (72,-0.45) {$0 \leqslant 24 < 60$};
\end{tikzpicture}""",

# PGCD(84, 60) : pavage du rectangle par des carrés (exercice 1144, question 1)
"ex1144_euclide": euclide_pavage(84, 60, 0.052),

# Plaque 84 cm × 60 cm découpée en carreaux de 12 cm (exercice 1144, question 3)
"ex1144_plaque": r"""
\begin{tikzpicture}[x=0.068cm,y=0.068cm]
  \fill[otSky] (0,0) rectangle (84,60);
  \fill[otGreen!35] (0,48) rectangle (12,60);
  \foreach \x in {12,24,36,48,60,72} \draw[otNavy!55,line width=0.5pt] (\x,0) -- (\x,60);
  \foreach \y in {12,24,36,48} \draw[otNavy!55,line width=0.5pt] (0,\y) -- (84,\y);
  \draw[otNavy,line width=1pt] (0,0) rectangle (84,60);
  \node[text=otGreenDark,font=\small] at (6,54) {$12$};
  \draw[cote] (0,-4.5) -- (84,-4.5) node[midway,coteTexte] {$84$ cm};
  \draw[otMuted!70,line width=0.4pt] (0,-0.8) -- (0,-6) (84,-0.8) -- (84,-6);
  \draw[cote] (-11,0) -- (-11,60) node[midway,coteTexte] {$60$ cm};
  \draw[otMuted!70,line width=0.4pt] (-0.8,0) -- (-12.5,0) (-0.8,60) -- (-12.5,60);
  \node[text=otGreenDark,anchor=north] at (42,-10.5) {$7 \times 5 = 35$ carreaux carrés de $12$ cm de côté};
\end{tikzpicture}""",

# Restes des puissances de 2 modulo 7 (exercice 1147)
"ex1147_cycle": cycle(2, 7, 1.5, haut_label=r"2^0,\ 2^3,\ 2^6\dots"),

# Algorithme d'Euclide en tableau pour 84 et 30 (exercice 1148)
"ex1148_euclide": euclide_tableau(84, 30),

# Arbre de décomposition de 2 023 (exercice 1149)
"ex1149_arbre": r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \node[compose] (a) at (0,0) {$2\,023$};
  \node[premier] (p1) at (-0.95,-1.1) {$7$};
  \node[compose] (b) at (0.95,-1.1) {$289$};
  \node[premier] (p2) at (0.1,-2.2) {$17$};
  \node[premier] (p3) at (1.8,-2.2) {$17$};
  \draw[branche] (a) -- (p1) (a) -- (b) (b) -- (p2) (b) -- (p3);
  \node[note,anchor=west] at (1.5,-0.55) {$2\,023 = 7 \times 289$};
  \node[note,anchor=west] at (2.4,-1.55) {$289 = 17 \times 17$};
  \node[text=otGreenDark] at (0.45,-3.1) {$2\,023 = 7 \times 17^2$};
\end{tikzpicture}""",

# Équation 6x + 5y = 2 : points à coordonnées entières de la droite (exercice 1146)
"ex1146_droite": r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.6cm, height=6.6cm, xmin=-4.6, xmax=8.6, ymin=-9.6, ymax=5.8,
  xtick={-4,...,8}, ytick={-9,...,5}, xticklabels={}, yticklabels={},
  ticklabel style={fill=none,draw=none}, major tick length=0pt]
  \addplot[courbe,domain=-4.4:8.4] {(2-6*x)/5};
  \draw[guide] (axis cs:-3,0) -- (axis cs:-3,4) -- (axis cs:0,4);
  \draw[guide] (axis cs:2,0) -- (axis cs:2,-2) -- (axis cs:0,-2);
  \draw[guide] (axis cs:7,0) -- (axis cs:7,-8) -- (axis cs:0,-8);
  \pnt[otGreenDark]{-3}{4} \pnt[otGreenDark]{2}{-2} \pnt[otGreenDark]{7}{-8}
  \node[text=otGreenDark,anchor=south west,inner sep=1.5pt] at (axis cs:-2.85,4.15) {$(-3\,;4)$};
  \node[text=otGreenDark,anchor=south west,inner sep=1.5pt] at (axis cs:2.15,-1.85) {$(2\,;-2)$};
  \node[text=otGreenDark,anchor=north east,inner sep=1.5pt] at (axis cs:6.8,-8.2) {$(7\,;-8)$};
  \node[text=otNavy,anchor=south west,inner sep=1.5pt] at (axis cs:0.6,1.0) {$6x + 5y = 2$};
\end{axis}
\end{tikzpicture}""",

# Schémas de chiffrement affine : cours (clé 7, 3) et exercice 1153 (clé 5, 8)
"cours_chiffrement": schema_chiffrement("E", 4, 5, "F", r"$y \equiv 7x + 3 \pmod{26}$", r"$x \equiv 15(y - 3) \pmod{26}$"),
"ex1153_chiffrement": schema_chiffrement("M", 12, 16, "Q", r"$y \equiv 5x + 8 \pmod{26}$", r"$x \equiv 21y + 14 \pmod{26}$"),

# Principe du chiffrement RSA (exercice 1154)
"ex1154_rsa": r"""
\begin{tikzpicture}[boite/.style={rectangle,rounded corners=2pt,draw=otNavy!70,line width=0.8pt,fill=otSky,minimum width=1.5cm,minimum height=0.8cm,inner sep=3pt,text=otNavy,align=center}]
  \node[boite] (m) at (0,0) {message\\$m = 100$};
  \node[boite,draw=otOrange!90!black,fill=otOrange!18,text=otInk] (c) at (3.95,0) {message codé\\$c = 213$};
  \node[boite,draw=otGreenDark,fill=otGreen!20,text=otGreenDark] (m2) at (7.45,0) {message\\$m = 100$};
  \draw[otNavy!80,line width=0.9pt,-{Stealth[length=2.4mm]}] (m) -- (c);
  \draw[otGreenDark,line width=0.9pt,-{Stealth[length=2.4mm]}] (c) -- (m2);
  \node[note,anchor=south] at (1.95,0.66) {$c \equiv m^{3} \pmod{391}$};
  \node[note,anchor=north] at (1.95,-0.66) {clé publique $(391\,;3)$};
  \node[note,anchor=south,text=otGreenDark] at (5.75,0.66) {$c^{235} \equiv m \pmod{391}$};
  \node[note,anchor=north,text=otGreenDark] at (5.75,-0.66) {clé secrète $235$};
\end{tikzpicture}""",
})
