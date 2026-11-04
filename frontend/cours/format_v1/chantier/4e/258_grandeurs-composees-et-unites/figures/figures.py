# -*- coding: utf-8 -*-
"""Figures de la notion 258 (4e : grandeurs composées et unités), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Frises des durées (base 60), schémas de trajets (distance, durée, vitesse),
conversion km/h et m/s, robinets et réservoirs (débit), tableau de conversion
des volumes et contenances, cubes (masse volumique), graphique distance-durée,
aquarium et piscine, compteurs, orage, ligne de bus, iceberg.
Bleu marine = données, vert foncé = éléments de réponse (corrigés), orange = repères.
"""

PREAMBULE_EXTRA = r"""
\tikzset{
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt,text=otInk},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,inner sep=0pt,text=otMuted},
  route/.style={otNavy,line width=1.6pt},
  fleche/.style={otOrange!90!black,line width=1pt,-{Stealth[length=2.4mm]}},
  flecheV/.style={otGreenDark,line width=1pt,-{Stealth[length=2.4mm]}},
  axe/.style={otMuted,line width=.7pt,-{Stealth[length=2.3mm]}},
  solide/.style={otNavy,line width=.9pt,line join=round},
  cache/.style={otNavy,line width=.6pt,dash pattern=on 2.5pt off 2pt},
  eau/.style={fill=otSky},
  ligne/.style={otNavy,line width=1.35pt,line join=round},
  accol/.style={decorate,decoration={brace,amplitude=5pt},otMuted,line width=.7pt},
}
\pgfplotsset{gm/.style={grid=both, minor grid style={otRule!75,line width=0.35pt}, minor tick length=0pt}}
"""

FIGURES = {}
TOLERE = {}
V = "otGreenDark"


def f(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


def P(x, y):
    return f"({f(x)},{f(y)})"


def tikz(L, opts="line cap=round"):
    return "\\begin{tikzpicture}[" + opts + "]\n" + "\n".join(L) + "\n\\end{tikzpicture}"


def vert(s):
    return r"\textcolor{otGreenDark}{" + s + "}"


# ================================================================== FRISES DES DURÉES
def frise(hmax, cm_h, pas_min, majeurs, haut, bas, marque=None):
    """Droite graduée des durées. majeurs : heures décimales des grands traits ;
    haut / bas : étiquettes (heures décimales / minutes) aux grands traits ;
    marque : (heure, texte vert au-dessus, accolade (début, texte) ou None)."""
    L = []
    W = hmax * cm_h
    L.append(rf"\draw[axe] (-0.15,0) -- ({f(W + 0.45)},0);")
    n = int(round(hmax * 60 / pas_min))
    for k in range(n + 1):
        x = k * pas_min / 60 * cm_h
        L.append(rf"\draw[otMuted,line width=.5pt] {P(x, -0.07)} -- {P(x, 0.07)};")
    for h, th, tb in zip(majeurs, haut, bas):
        x = h * cm_h
        L.append(rf"\draw[otNavy,line width=.9pt] {P(x, -0.16)} -- {P(x, 0.16)};")
        L.append(rf"\node[anchor=south,text=otNavy] at {P(x, 0.24)} {{{th}}};")
        L.append(rf"\node[anchor=north,text=otInk] at {P(x, -0.24)} {{{tb}}};")
    if marque:
        h, texte, acc = marque
        x = h * cm_h
        L.append(rf"\fill[otGreenDark] {P(x, 0)} circle (2.4pt);")
        L.append(rf"\node[anchor=south,text=otGreenDark] at {P(x, 0.95)} {{{texte}}};")
        L.append(rf"\draw[otGreenDark,line width=.5pt,dash pattern=on 1.5pt off 1.5pt] {P(x, 0.12)} -- {P(x, 0.9)};")
        if acc:
            x0 = acc[0] * cm_h
            L.append(rf"\draw[accol,otGreenDark] {P(x, -0.95)} -- {P(x0, -0.95)};")
            L.append(rf"\node[anchor=north,text=otGreenDark] at {P((x + x0) / 2, -1.12)} {{{acc[1]}}};")
    return tikz(L)


FIGURES["cours_durees"] = frise(
    1, 5.6, 5, [0, 0.25, 0.5, 0.75, 1],
    [r"$0$ h", r"$0{,}25$ h", r"$0{,}5$ h", r"$0{,}75$ h", r"$1$ h"],
    [r"$0$ min", r"$15$ min", r"$30$ min", r"$45$ min", r"$60$ min"])

FIGURES["ex2642_frise"] = frise(
    2, 2.9, 15, [0, 1, 2], [r"$0$ h", r"$1$ h", r"$2$ h"], [r"$0$ min", r"$60$ min", r"$120$ min"],
    marque=(1.75, r"$1{,}75$ h $= 1$ h $45$ min", (1, r"$0{,}75 \times 60 = 45$ min")))


# ================================================================== SCHÉMA DE TRAJET
def trajet(duree, distance, vitesse, reponse=None, L_cm=5.0, noms=("A", "B")):
    """Route de A à B : durée au-dessus, cote de la distance, vitesse sous la route.
    reponse : texte vert écrit sous le schéma (corrigé)."""
    L = [
        rf"\draw[route] (0,0) -- ({f(L_cm)},0);",
        rf"\node[geoPoint] at (0,0) {{}};",
        rf"\node[geoPoint] at ({f(L_cm)},0) {{}};",
        rf"\node[anchor=east,text=otInk] at (-0.15,0) {{${noms[0]}$}};",
        rf"\node[anchor=west,text=otInk] at ({f(L_cm + 0.15)},0) {{${noms[1]}$}};",
        rf"\draw[cote] (0,0.5) -- ({f(L_cm)},0.5);",
        rf"\draw[otMuted!70,line width=.4pt] (0,0.12) -- (0,0.62) ({f(L_cm)},0.12) -- ({f(L_cm)},0.62);",
        rf"\node[anchor=south,text=otInk] at ({f(L_cm / 2)},0.64) {{distance : {distance}}};",
        rf"\draw[fleche] ({f(L_cm / 2 - 1.1)},-0.32) -- ({f(L_cm / 2 + 1.1)},-0.32);",
        rf"\node[anchor=north,text=otInk] at ({f(L_cm / 2)},-0.48) {{durée : {duree}}};",
        rf"\node[anchor=north,text=otInk] at ({f(L_cm / 2)},-1.06) {{vitesse : {vitesse}}};",
    ]
    if reponse:
        L.append(rf"\node[anchor=north,text=otGreenDark] at ({f(L_cm / 2)},-1.85) {{{reponse}}};")
    return tikz(L)


FIGURES["cours_trajet"] = trajet(r"$t = 3$ h", r"$d = 210$ km", r"$v = \dfrac{d}{t} = \dfrac{210}{3} = 70$ km/h")
FIGURES["ex2644_trajet"] = trajet(r"$2$ h $30$ min", r"$d = $ ? km", r"$80$ km/h")
FIGURES["ex2644_trajet_corrige"] = trajet(r"$2$ h $30$ min $= 2{,}5$ h", vert(r"$d = 200$ km"), r"$80$ km/h",
                                          reponse=r"$d = v \times t = 80 \times 2{,}5 = 200$ km")
FIGURES["ex2662_trajet_corrige"] = trajet(
    r"$4$ h $30$ min (pause : $30$ min)", vert(r"$378$ km"), vert(r"$\dfrac{378}{4{,}5} = 84$ km/h"),
    reponse=r"conduite : $4$ h, soit $\dfrac{378}{4} = 94{,}5$ km/h", noms=(r"\text{Départ}", r"\text{Arrivée}"), L_cm=4.2)


# ================================================================== CONVERSION km/h ⇄ m/s
def conversion():
    L = [
        r"\node[draw=otNavy,fill=otSky,line width=.9pt,rounded corners=3pt,minimum width=2.6cm,minimum height=1.05cm,align=center] (a) at (0,0) {vitesse\\en m/s};",
        r"\node[draw=otNavy,fill=otSky,line width=.9pt,rounded corners=3pt,minimum width=2.6cm,minimum height=1.05cm,align=center] (b) at (4.4,0) {vitesse\\en km/h};",
        r"\draw[fleche] (a.north east) to[bend left=28] node[midway,above=2pt,text=otOrange!80!black] {$\times\, 3{,}6$} (b.north west);",
        r"\draw[fleche] (b.south west) to[bend left=28] node[midway,below=2pt,text=otOrange!80!black] {$\div\, 3{,}6$} (a.south east);",
        r"\node[anchor=north,text=otMuted,align=center] at (2.2,-1.55) {$20$ m/s $= 72$ km/h\\$54$ km/h $= 15$ m/s};",
    ]
    return tikz(L)


FIGURES["cours_conversion"] = conversion()


# ================================================================== ROBINETS ET RÉSERVOIRS
def reservoir(W, H, niveau, debit, volume, lignes=(), bonde=None, nom=None):
    """Réservoir ouvert W × H (cm) rempli jusqu'à `niveau` (fraction), robinet à gauche.
    debit : texte du robinet ; volume : texte écrit dans l'eau ; lignes : textes sous le réservoir ;
    bonde : texte de la bonde (écoulement en bas à droite)."""
    h = H * niveau
    L = [
        rf"\fill[otSky] (0,0) rectangle ({f(W)},{f(h)});",
        rf"\draw[otNavy!45,line width=.5pt] (0,{f(h)}) -- ({f(W)},{f(h)});",
        rf"\draw[solide,line width=1.2pt] (0,{f(H)}) -- (0,0) -- ({f(W)},0) -- ({f(W)},{f(H)});",
        # robinet : tuyau horizontal puis bec vers le bas
        rf"\draw[otMuted,line width=4pt] (-1.1,{f(H + 0.75)}) -- (0.55,{f(H + 0.75)}) -- (0.55,{f(H + 0.45)});",
        rf"\fill[otMuted] (-0.55,{f(H + 0.75)}) circle (3.2pt);",
        rf"\draw[otMuted,line width=1.4pt] (-0.55,{f(H + 0.75)}) -- (-0.55,{f(H + 1.05)}) (-0.75,{f(H + 1.05)}) -- (-0.35,{f(H + 1.05)});",
        # filet d'eau
        rf"\draw[otNavy!45,line width=2.2pt] (0.55,{f(H + 0.38)}) -- (0.55,{f(h + 0.02)});",
        rf"\node[anchor=west,text=otInk] at (0.95,{f(H + 0.75)}) {{débit : {debit}}};",
        rf"\node[text=otNavy] at ({f(W / 2 + 0.3)},{f(h / 2)}) {{{volume}}};",
    ]
    if nom:
        L.append(rf"\node[anchor=north,petit] at ({f(W / 2)},-0.12) {{{nom}}};")
    if bonde:
        L += [rf"\draw[otMuted,line width=3pt] ({f(W - 0.5)},0) -- ({f(W - 0.5)},-0.45) -- ({f(W + 0.3)},-0.45);",
              rf"\draw[otNavy!45,line width=2pt] ({f(W + 0.38)},-0.45) -- ({f(W + 0.38)},-0.95);",
              rf"\node[anchor=west,text=otInk] at ({f(W + 0.6)},-0.6) {{bonde : {bonde}}};"]
    y = -0.5 if not bonde else -1.25
    for t in lignes:
        L.append(rf"\node[anchor=north,text=otGreenDark] at ({f(W / 2 + 0.6)},{f(y)}) {{{t}}};")
        y -= 0.62
    return tikz(L)


FIGURES["cours_robinet"] = reservoir(4.2, 2.0, 0.55, r"$15$ L/min", r"cuve de $240$ L",
                                     [r"durée $= \dfrac{240}{15} = 16$ min"])
FIGURES["ex2647_robinet"] = reservoir(5.0, 1.6, 0.6, r"$12$ L/min", r"baignoire de $150$ L")
FIGURES["ex2647_robinet_corrige"] = reservoir(5.0, 1.6, 0.6, r"$12$ L/min", r"baignoire de $150$ L",
                                              [r"$150 \div 12 = 12{,}5$ min $= 12$ min $30$ s"])
FIGURES["ex2659_baignoire"] = reservoir(3.8, 1.6, 0.6, r"$15$ L/min", r"pleine : $180$ L", bonde=r"$6$ L/min")
FIGURES["ex2659_baignoire_corrige"] = reservoir(3.8, 1.6, 0.6, r"$15$ L/min", r"pleine : $180$ L", bonde=r"$6$ L/min",
                                                lignes=[r"débit réel : $15 - 6 = 9$ L/min", r"$180 \div 9 = 20$ min"])


# ================================================================== TABLEAU DE CONVERSION DES VOLUMES
def tableau_volumes(lignes, legende=None, nb_lignes=None):
    """9 colonnes : m³ (3), dm³ (3), cm³ (3). lignes : [[(colonne, texte, couleur)]]."""
    cw, hh = 0.8, 0.6
    n = nb_lignes or max(len(lignes), 1)
    W = 9 * cw
    L = [rf"\fill[otSky] (0,0) rectangle ({f(W)},{f(2 * hh)});"]
    # filets
    L.append(rf"\draw[otNavy,line width=.8pt] (0,{f(-n * hh)}) rectangle ({f(W)},{f(2 * hh)});")
    L.append(rf"\draw[otNavy,line width=.6pt] (0,{f(hh)}) -- ({f(W)},{f(hh)}) (0,0) -- ({f(W)},0);")
    for k in range(1, n):
        L.append(rf"\draw[otRule,line width=.5pt] (0,{f(-k * hh)}) -- ({f(W)},{f(-k * hh)});")
    for j in range(1, 9):
        x = j * cw
        if j % 3 == 0:
            L.append(rf"\draw[otNavy,line width=.6pt] ({f(x)},{f(-n * hh)}) -- ({f(x)},{f(2 * hh)});")
        else:
            L.append(rf"\draw[otRule,line width=.5pt] ({f(x)},{f(-n * hh)}) -- ({f(x)},{f(hh)});")
    for i, u in enumerate(["m³", "dm³", "cm³"]):
        L.append(rf"\node[text=otNavy,font=\otMedium\small] at ({f((3 * i + 1.5) * cw)},{f(1.5 * hh)}) {{{u}}};")
    for j, u in zip(range(3, 9), ["hL", "daL", "L", "dL", "cL", "mL"]):
        L.append(rf"\node[text=otNavy,font=\otRegular\small] at ({f((j + 0.5) * cw)},{f(0.5 * hh)}) {{{u}}};")
    for i, ligne in enumerate(lignes):
        for col, t, c in ligne:
            L.append(rf"\node[text={c}] at ({f((col + 0.5) * cw)},{f(-(i + 0.5) * hh)}) {{${t}$}};")
    if legende:
        L.append(rf"\node[anchor=north,align=center,text=otInk] at ({f(W / 2)},{f(-n * hh - 0.15)}) {{{legende}}};")
    return tikz(L)


I_ = "otInk"
FIGURES["cours_tableau_volumes"] = tableau_volumes(
    [[(2, "1{,}", I_), (3, "2", I_), (4, "0", V), (5, "0", V)]],
    r"$1{,}2$ m³ $= 1\,200$ dm³ $= 1\,200$ L\\{\small trois colonnes par unité de volume}")
FIGURES["ex2646_tableau"] = tableau_volumes([], nb_lignes=2)
FIGURES["ex2646_tableau_corrige"] = tableau_volumes(
    [[(2, "2{,}", I_), (3, "5", I_), (4, "0", V), (5, "0", V)],
     [(5, "0{,}", V), (6, "7", I_), (7, "5", I_), (8, "0", I_)]],
    vert(r"$2{,}5$ m³ $= 2\,500$ L") + r"\quad " + vert(r"$750$ mL $= 0{,}75$ L"))


# ================================================================== CUBES (MASSE VOLUMIQUE)
def cube(x0, a, fond, haut, cote_, masse, nom, rho=None, cote=False):
    dx, dy = 0.45 * a, 0.32 * a
    L = [
        rf"\fill[{fond}] {P(x0, 0)} rectangle {P(x0 + a, a)};",
        rf"\fill[{haut}] {P(x0, a)} -- {P(x0 + dx, a + dy)} -- {P(x0 + a + dx, a + dy)} -- {P(x0 + a, a)} -- cycle;",
        rf"\fill[{cote_}] {P(x0 + a, 0)} -- {P(x0 + a + dx, dy)} -- {P(x0 + a + dx, a + dy)} -- {P(x0 + a, a)} -- cycle;",
        rf"\draw[solide] {P(x0, 0)} rectangle {P(x0 + a, a)};",
        rf"\draw[solide] {P(x0, a)} -- {P(x0 + dx, a + dy)} -- {P(x0 + a + dx, a + dy)} -- {P(x0 + a + dx, dy)} -- {P(x0 + a, 0)};",
        rf"\draw[solide] {P(x0 + a, a)} -- {P(x0 + a + dx, a + dy)};",
        rf"\node[anchor=north,text=otNavy] at {P(x0 + (a + dx) / 2, -0.15)} {{{nom}}};",
        rf"\node[anchor=north,text=otInk] at {P(x0 + (a + dx) / 2, -0.7)} {{{masse}}};",
    ]
    if rho:
        L.append(rf"\node[anchor=north,text=otGreenDark] at {P(x0 + (a + dx) / 2, -1.25)} {{{rho}}};")
    if cote:
        L += [rf"\draw[cote] {P(x0 - 0.3, 0)} -- {P(x0 - 0.3, a)};",
              rf"\node[anchor=east,text=otInk] at {P(x0 - 0.38, a / 2)} {{$10$ cm}};"]
    return L


def cubes(corrige):
    a = 1.45
    mats = [("otMuted!40", "otMuted!25", "otMuted!32", r"masse : $7{,}8$ kg", "fer", r"$\rho = 7{,}8$ g/cm³"),
            ("otMuted!14", "otMuted!6", "otMuted!10", r"masse : $2{,}7$ kg", "aluminium", r"$\rho = 2{,}7$ g/cm³"),
            ("otOrange!35", "otOrange!18", "otOrange!26", r"masse : $600$ g", "bois", r"$\rho = 0{,}6$ g/cm³")]
    L = []
    for k, (fo, ha, co, m, nom, rho) in enumerate(mats):
        L += cube(k * 2.55, a, fo, ha, co, m, nom, rho if corrige else None, cote=(k == 0))
    return tikz(L)


FIGURES["ex2648_cubes"] = cubes(False)
FIGURES["ex2648_cubes_corrige"] = cubes(True)


# ================================================================== GRAPHIQUE DISTANCE-DURÉE (2649)
P49 = (r"width=6.2cm, height=5cm, xmin=0, xmax=3.3, ymin=0, ymax=195, "
       r"xtick={0.5,1,1.5,2,2.5,3}, xticklabels={$0{,}5$,$1$,$1{,}5$,$2$,$2{,}5$,$3$}, "
       r"ytick={20,40,60,80,100,120,140,160,180}, yticklabels={,$40$,,$80$,,$120$,,$160$,}, "
       r"minor ytick={10,30,50,70,90,110,130,150,170,190}, "
       r"xlabel={durée (h)}, ylabel={distance (km)}, "
       r"every axis x label/.style={at={(current axis.right of origin)},anchor=north east,yshift=-14pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}, "
       r"every axis y label/.style={at={(current axis.above origin)},anchor=south west,xshift=2pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}")
B49 = r"""
  \draw[ligne] (axis cs:0,0) -- (axis cs:1,60) -- (axis cs:1.5,60) -- (axis cs:3,165);
  \fill[otNavy] (axis cs:0,0) circle (2.1pt); \fill[otNavy] (axis cs:1,60) circle (2.1pt);
  \fill[otNavy] (axis cs:1.5,60) circle (2.1pt); \fill[otNavy] (axis cs:3,165) circle (2.1pt);
"""


def graphe(corrige):
    s = r"\begin{tikzpicture}" + "\n" + r"\begin{axis}[otWeb, gm, " + P49 + "]\n" + B49
    if corrige:
        s += r"""
  \node[note,text=otGreenDark,anchor=north west] at (axis cs:0.62,30) {$60$ km/h};
  \node[note,text=otGreenDark,anchor=south] at (axis cs:1.25,66) {arrêt};
  \node[note,text=otGreenDark,anchor=north west] at (axis cs:2.2,96) {$70$ km/h};
"""
    return s + "\\end{axis}\n\\end{tikzpicture}"


FIGURES["ex2649_trajet"] = graphe(False)
FIGURES["ex2649_trajet_corrige"] = graphe(True)


# ================================================================== ALLER-RETOUR (2650)
def aller_retour(corrige):
    W = 5.6
    L = [
        r"\node[geoPoint] at (0,0) {};",
        rf"\node[geoPoint] at ({f(W)},0) {{}};",
        r"\node[anchor=east,text=otInk] at (-0.15,0) {$A$};",
        rf"\node[anchor=west,text=otInk] at ({f(W + 0.15)},0) {{$B$}};",
        rf"\draw[otNavy,line width=1.1pt,-{{Stealth[length=2.6mm]}}] (0.25,0.38) -- ({f(W - 0.25)},0.38);",
        rf"\draw[otOrange!90!black,line width=1.1pt,-{{Stealth[length=2.6mm]}}] ({f(W - 0.25)},-0.38) -- (0.25,-0.38);",
        rf"\node[anchor=south,text=otNavy] at ({f(W / 2)},0.55) {{aller : $30$ km à $20$ km/h}};",
        rf"\node[anchor=north,text=otOrange!80!black] at ({f(W / 2)},-0.55) {{retour : $30$ km à $30$ km/h}};",
    ]
    if corrige:
        L += [rf"\node[anchor=south,text=otGreenDark] at ({f(W / 2)},1.05) {{durée : $\dfrac{{30}}{{20}} = 1{{,}}5$ h}};",
              rf"\node[anchor=north,text=otGreenDark] at ({f(W / 2)},-1.05) {{durée : $\dfrac{{30}}{{30}} = 1$ h}};",
              rf"\node[anchor=north,text=otGreenDark,font=\bfseries] at ({f(W / 2)},-2.0) {{total : $60$ km en $2{{,}}5$ h}};"]
    return tikz(L)


FIGURES["ex2650_aller_retour"] = aller_retour(False)
FIGURES["ex2650_aller_retour_corrige"] = aller_retour(True)


# ================================================================== PAVÉ AVEC EAU (aquarium, piscine)
def bassin(w, h, d, niveau, la, lb, lc, ln, reponse=None):
    """Pavé w × h (face avant), profondeur d (oblique), eau jusqu'à la fraction `niveau`.
    la : longueur (bas), lb : largeur (oblique), lc : hauteur (gauche), ln : hauteur d'eau (droite)."""
    dx, dy = 0.55 * d, 0.4 * d
    he = h * niveau
    A, B, C, D = (0, 0), (w, 0), (w, h), (0, h)
    E, F, G, H = (dx, dy), (w + dx, dy), (w + dx, h + dy), (dx, h + dy)
    Q = lambda p: P(*p)
    L = [
        # eau : face avant, face droite, surface
        rf"\fill[otSky] {Q(A)} -- {Q(B)} -- {Q(F)} -- {P(w + dx, he + dy)} -- {P(dx, he + dy)} -- {P(0, he)} -- cycle;",
        rf"\fill[otNavy!12] {P(0, he)} -- {P(w, he)} -- {P(w + dx, he + dy)} -- {P(dx, he + dy)} -- cycle;",
        rf"\draw[otNavy!50,line width=.5pt] {P(0, he)} -- {P(w, he)} -- {P(w + dx, he + dy)};",
        rf"\draw[cache] {Q(A)} -- {Q(E)} -- {Q(F)} {Q(E)} -- {Q(H)};",
        rf"\draw[solide] {Q(A)} -- {Q(B)} -- {Q(C)} -- {Q(D)} -- cycle;",
        rf"\draw[solide] {Q(B)} -- {Q(F)} -- {Q(G)} -- {Q(H)} -- {Q(D)} {Q(C)} -- {Q(G)};",
        # cotes
        rf"\draw[cote] (0,-0.3) -- ({f(w)},-0.3);",
        rf"\node[anchor=north,text=otInk] at ({f(w / 2)},-0.36) {{{la}}};",
        rf"\draw[cote] ({f(w + 0.3)},-0.12) -- ({f(w + dx + 0.3)},{f(dy - 0.12)});",
        rf"\node[anchor=north west,text=otInk] at ({f(w + dx / 2 + 0.38)},{f(dy / 2 - 0.12)}) {{{lb}}};",
        rf"\draw[cote] (-0.3,0) -- (-0.3,{f(h)});",
        rf"\node[anchor=east,text=otInk] at (-0.38,{f(h / 2)}) {{{lc}}};",
        rf"\draw[cote,otOrange!90!black] ({f(w + dx + 0.35)},{f(dy)}) -- ({f(w + dx + 0.35)},{f(he + dy)});",
        rf"\node[anchor=west,text=otOrange!80!black] at ({f(w + dx + 0.45)},{f((he) / 2 + dy)}) {{{ln}}};",
    ]
    if reponse:
        L.append(rf"\node[anchor=north,text=otGreenDark] at ({f(w / 2)},-0.95) {{{reponse}}};")
    return tikz(L)


FIGURES["ex2652_aquarium"] = bassin(3.4, 1.9, 1.5, 40 / 45, r"$80$ cm", r"$35$ cm", r"$45$ cm", r"eau : $40$ cm")
FIGURES["ex2652_aquarium_corrige"] = bassin(3.4, 1.9, 1.5, 40 / 45, r"$80$ cm", r"$35$ cm", r"$45$ cm", r"eau : $40$ cm",
                                            reponse=r"$112\,000$ cm³ $= 112$ L")
FIGURES["ex2660_piscine"] = bassin(3.7, 1.1, 1.8, 1.25 / 1.5, r"$10$ m", r"$4$ m", r"$1{,}5$ m", r"eau : $1{,}25$ m")
FIGURES["ex2660_piscine_corrige"] = bassin(3.7, 1.1, 1.8, 1.25 / 1.5, r"$10$ m", r"$4$ m", r"$1{,}5$ m", r"eau : $1{,}25$ m",
                                           reponse=r"$10 \times 4 \times 1{,}25 = 50$ m³")


# ================================================================== COMPTEURS
def compteur(x0, y0, chiffres, decimales, unite, titre, sous_titre=None, couleur="otInk"):
    """Afficheur à tambours : chiffres entiers (chaîne) + décimales (chaîne, sur fond orange)."""
    c, hgt = 0.42, 0.6
    n = len(chiffres) + len(decimales)
    W = n * c + 0.3 + (0.18 if decimales else 0)
    L = [rf"\draw[otNavy,fill=otSky!60,line width=.9pt,rounded corners=4pt] {P(x0, y0)} rectangle {P(x0 + W + 1.0, y0 + hgt + 0.36)};"]
    x = x0 + 0.15
    for k, ch in enumerate(chiffres + decimales):
        if k == len(chiffres):
            L.append(rf"\fill[otInk] {P(x + 0.04, y0 + 0.22)} circle (1.3pt);")
            x += 0.18
        fond = "otOrange!25" if k >= len(chiffres) else "white"
        L.append(rf"\draw[otNavy,fill={fond},line width=.6pt] {P(x, y0 + 0.18)} rectangle {P(x + c - 0.05, y0 + 0.18 + hgt)};")
        L.append(rf"\node[text={couleur},font=\otMedium\large] at {P(x + (c - 0.05) / 2, y0 + 0.18 + hgt / 2)} {{{ch}}};")
        x += c
    L.append(rf"\node[anchor=west,text=otNavy,font=\otMedium] at {P(x + 0.12, y0 + 0.18 + hgt / 2)} {{{unite}}};")
    L.append(rf"\node[anchor=south,text=otNavy] at {P(x0 + (W + 1.0) / 2, y0 + hgt + 0.48)} {{{titre}}};")
    if sous_titre:
        L.append(rf"\node[anchor=north,text=otInk] at {P(x0 + (W + 1.0) / 2, y0 - 0.12)} {{{sous_titre}}};")
    return L


FIGURES["ex2653_compteur"] = tikz(compteur(0, 0, "12458", "0", "kWh", "compteur au début du mois"))
FIGURES["ex2653_compteur_corrige"] = tikz(
    compteur(0, 1.9, "12458", "0", "kWh", "début du mois")
    + compteur(0, 0, "12498", "2", "kWh", "fin du mois", r"$12\,458{,}0 + 40{,}2 = 12\,498{,}2$ kWh", couleur="otGreenDark"))
FIGURES["ex2662_compteurs"] = tikz(
    compteur(0, 0, "45872", "", "km", r"départ à $7$ h $50$ min")
    + compteur(4.0, 0, "46250", "", "km", r"arrivée à $12$ h $20$ min"))


# ================================================================== ORAGE (2657)
def orage(corrige):
    L = [r"\draw[otGreenDark!70,line width=1pt] (-0.6,0) -- (7.0,0);"]
    # observateur (silhouette)
    L += [r"\fill[otNavy] (0,1.12) circle (0.14);",
          r"\draw[otNavy,line width=1.6pt] (0,0.97) -- (0,0.5) (0,0.5) -- (-0.17,0.02) (0,0.5) -- (0.17,0.02) (-0.25,0.8) -- (0.25,0.8);",
          r"\node[anchor=north,petit] at (0,-0.12) {Lucas};"]

    def nuage(xc, yc, pale=False):
        col = "otMuted!20" if pale else "otMuted!40"
        return [rf"\fill[{col}] {P(xc - 0.5, yc)} circle (0.38) {P(xc, yc + 0.22)} circle (0.48) {P(xc + 0.55, yc + 0.02)} circle (0.4) {P(xc + 0.05, yc - 0.12)} circle (0.36);"]

    def eclair(xc, pale=False):
        col = "otOrange!45" if pale else "otOrange"
        return [rf"\draw[{col},line width=1.6pt,line join=bevel] {P(xc + 0.1, 2.05)} -- {P(xc - 0.15, 1.2)} -- {P(xc + 0.12, 1.25)} -- {P(xc - 0.05, 0.1)};"]

    if not corrige:
        x = 6.0
        L += nuage(x, 2.45) + eclair(x)
        L += [rf"\draw[fleche] {P(x - 0.45, 0.7)} -- (0.55,0.7);",
              rf"\node[anchor=south,text=otOrange!80!black] at {P(x / 2, 0.82)} {{son : $340$ m/s}};",
              rf"\draw[cote] (0,-0.75) -- {P(x - 0.05, -0.75)};",
              rf"\node[anchor=north,text=otInk] at {P(x / 2, -0.85)} {{distance ?}};"]
    else:
        x1, x2 = 6.2, 3.2
        L += nuage(x1, 2.45, pale=True) + eclair(x1, pale=True) + nuage(x2, 2.45) + eclair(x2)
        L += [rf"\node[anchor=south,petit] at {P(x1, 3.3)} {{il y a $5$ min}};",
              rf"\node[anchor=south,petit] at {P(x2, 3.3)} {{maintenant}};",
              rf"\draw[cote] (0,-0.75) -- {P(x2 - 0.05, -0.75)};",
              rf"\node[anchor=north,text=otGreenDark] at {P(x2 / 2, -0.85)} {{$340 \times 3 = 1\,020$ m}};",
              rf"\draw[cote] (0,-1.75) -- {P(x1 - 0.05, -1.75)};",
              rf"\node[anchor=north,text=otGreenDark] at {P(x1 / 2, -1.85)} {{$340 \times 6 = 2\,040$ m}};",
              rf"\draw[flecheV] {P(x1 - 0.4, 1.35)} -- {P(x2 + 0.55, 1.35)};",
              rf"\node[anchor=south,text=otGreenDark] at {P((x1 + x2) / 2 + 0.1, 1.45)} {{$1\,020$ m}};"]
    return tikz(L)


FIGURES["ex2657_orage"] = orage(False)
FIGURES["ex2657_orage_corrige"] = orage(True)


# ================================================================== LIGNE DE BUS (2658)
def ligne_bus(corrige):
    xs = [0, 2.5, 5.4, 7.3]
    km = ["$8$ km", "$12$ km", "$5$ km"]
    pas = ["$30$", "$45$", "$20$"]
    pk = ["$240$", "$540$", "$100$"]
    L = [rf"\draw[otNavy,line width=2.4pt] (0,0) -- ({f(xs[-1])},0);"]
    for x, nom in zip(xs, "ABCD"):
        L += [rf"\draw[otNavy,fill=white,line width=1.4pt] {P(x, 0)} circle (0.13);",
              rf"\node[anchor=south,text=otNavy,font=\bfseries] at {P(x, 0.2)} {{${nom}$}};"]
    for k in range(3):
        m = (xs[k] + xs[k + 1]) / 2
        L += [rf"\node[anchor=south,text=otInk] at {P(m, 0.12)} {{{km[k]}}};",
              rf"\node[anchor=north,text=otOrange!80!black,align=center] at {P(m, -0.22)} {{{pas[k]}\\[-1pt]{{\small passagers}}}};"]
        if corrige:
            L.append(rf"\node[anchor=north,text=otGreenDark,align=center] at {P(m, -1.35)} {{{pas[k]} $\times$ {km[k].replace(' km', '')}\\$=$ {pk[k]}}};")
    if corrige:
        L += [rf"\node[anchor=north,text=otGreenDark,font=\bfseries] at {P(xs[-1] / 2, -2.55)} {{total : $880$ passagers-kilomètres}};"]
    return tikz(L)


FIGURES["ex2658_ligne"] = ligne_bus(False)
FIGURES["ex2658_ligne_corrige"] = ligne_bus(True)


# ================================================================== ICEBERG (2661)
def iceberg(corrige):
    haut = [(-0.7, 0), (-0.45, 0.55), (-0.1, 0.85), (0.3, 0.7), (0.6, 0.3), (0.75, 0)]
    bas = [(0.75, 0), (1.5, -0.6), (1.85, -1.6), (1.4, -2.6), (0.4, -3.1), (-0.8, -2.9), (-1.7, -2.0), (-1.75, -0.9), (-1.2, -0.3), (-0.7, 0)]
    L = [r"\fill[otNavy!14] (-2.6,0) rectangle (4.3,-3.4);",
         r"\fill[white] " + " -- ".join(P(*p) for p in haut) + " -- cycle;",
         r"\fill[white] " + " -- ".join(P(*p) for p in bas) + " -- cycle;",
         r"\draw[solide] " + " -- ".join(P(*p) for p in haut[:-1] + bas) + ";",
         r"\draw[otNavy!60,line width=1pt] (-2.6,0) -- (-0.7,0) (0.75,0) -- (4.3,0);",
         r"\node[anchor=north east,petit,text=otNavy] at (4.2,-0.12) {surface de la mer};"]
    if not corrige:
        L += [r"\node[anchor=west,text=otInk] at (1.0,0.55) {partie visible};",
              r"\node[text=otNavy] at (0.05,-1.6) {partie immergée};"]
    else:
        L += [r"\node[anchor=west,text=otGreenDark] at (1.0,0.55) {partie visible : environ $10{,}2$ \%};",
              r"\node[text=otNavy,align=center] at (0.05,-1.6) {partie immergée\\\textcolor{otGreenDark}{environ $89{,}8$ \%}};"]
    return tikz(L)


FIGURES["ex2661_iceberg"] = iceberg(False)
FIGURES["ex2661_iceberg_corrige"] = iceberg(True)
