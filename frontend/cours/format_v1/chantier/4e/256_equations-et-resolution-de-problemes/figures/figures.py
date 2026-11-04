# -*- coding: utf-8 -*-
"""Figures de la notion 256 (4e : équations et résolution de problèmes), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>
Balances de Roberval (chaque étape de résolution = une opération sur les deux
plateaux), schémas en barres des partages, frises du temps, figures de géométrie
des problèmes, droite des forfaits, route de la poursuite, frise de Diophante.
Bleu marine = données, vert foncé = éléments de réponse (corrigés), orange = repères.
"""
from math import sqrt, cos, sin, radians, atan2, degrees

PREAMBULE_EXTRA = r"""
\tikzset{
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt,text=otInk},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,inner sep=0pt,text=otMuted},
  boite/.style={draw=otNavy,fill=otSky,line width=.8pt,rounded corners=1pt},
  masse/.style={draw=otOrange!80!black,fill=otOrange!25,line width=.8pt},
  accol/.style={decorate,decoration={brace,amplitude=5pt},otMuted,line width=.7pt},
  barre/.style={draw=otNavy,line width=.8pt},
  fleche/.style={otOrange!90!black,line width=1pt,-{Stealth[length=2.4mm]}},
  axe/.style={otMuted,line width=.7pt,-{Stealth[length=2.3mm]}},
}
% \coteSous[décalage]{A}{B}{texte} : cote horizontale (A à droite de B), texte vert écrit sous la flèche
\newcommand{\coteSous}[4][0.35]{\draw[cote] ($(#2)!#1cm!90:(#3)$) -- ($(#3)!#1cm!-90:(#2)$) node[midway,below=3pt,inner sep=1pt,text=otGreenDark]{#4};
  \draw[otMuted!70,line width=.4pt] (#2) -- ($(#2)!#1cm+2pt!90:(#3)$) (#3) -- ($(#3)!#1cm+2pt!-90:(#2)$);}
"""

FIGURES = {}
TOLERE = {}   # aucune tolérance : aucun texte n'est posé sur un trait
V = "otGreenDark"


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def figure(corps, opt="line cap=round"):
    return "\n".join([r"\begin{tikzpicture}[%s]" % opt] + corps + [r"\end{tikzpicture}"])


def vert(s):
    return r"\textcolor{otGreenDark}{%s}" % s


# ================================================================== BALANCES DE ROBERVAL
E, PW = 1.9, 1.6           # demi-fléau, demi-largeur d'un plateau
LB, GAP, LM, HM = .44, .07, .66, .42


def plateau(cx, y0, n, m, final=False):
    """n boîtes x puis une masse m (texte) posées sur un plateau centré en cx."""
    s = []
    larg = n * LB + max(n - 1, 0) * GAP + ((GAP if n else 0) + LM if m else 0)
    x = cx - larg / 2
    bord, fond, enc = ("otGreenDark", "otGreen!18", "otGreenDark") if final else ("otNavy", "otSky", "otInk")
    for _ in range(n):
        s.append(r"\draw[boite,draw=%s,fill=%s] (%s,%s) rectangle (%s,%s);" % (bord, fond, f(x), f(y0), f(x + LB), f(y0 + LB)))
        s.append(r"\node[text=%s] at (%s,%s) {$x$};" % (enc, f(x + LB / 2), f(y0 + LB / 2)))
        x += LB + GAP
    if m:
        s.append(r"\draw[masse] (%s,%s) -- (%s,%s) -- (%s,%s) -- (%s,%s) -- cycle;"
                 % (f(x), f(y0), f(x + LM), f(y0), f(x + LM - .1), f(y0 + HM), f(x + .1), f(y0 + HM)))
        s.append(r"\node[text=otInk] at (%s,%s) {$%s$};" % (f(x + LM / 2), f(y0 + HM / 2), m))
    return s


def balance(g, d, oy=0.0, eg=None, ed=None, final=False):
    """g, d : (nombre de boîtes, masse ou None) ; eg, ed : membres écrits sous les plateaux."""
    s = [
        r"\fill[otMuted!25] (-1,%s) -- (1,%s) -- (.6,%s) -- (-.6,%s) -- cycle;" % (f(oy), f(oy), f(oy + .25), f(oy + .25)),
        r"\draw[otMuted,line width=.8pt] (-1,%s) -- (1,%s) -- (.6,%s) -- (-.6,%s) -- cycle;" % (f(oy), f(oy), f(oy + .25), f(oy + .25)),
        r"\draw[otMuted,line width=2.2pt] (0,%s) -- (0,%s);" % (f(oy + .25), f(oy + 1.1)),
        r"\draw[otNavy,line width=1.6pt] (%s,%s) -- (%s,%s);" % (f(-E), f(oy + 1.1), f(E), f(oy + 1.1)),
        r"\fill[otMuted] (0,%s) circle (2.4pt);" % f(oy + 1.1),
    ]
    for cx in (-E, E):
        s += [r"\draw[otNavy,line width=1.6pt] (%s,%s) -- (%s,%s);" % (f(cx), f(oy + 1.1), f(cx), f(oy + 1.45)),
              r"\draw[otNavy,line width=1.8pt] (%s,%s) -- (%s,%s);" % (f(cx - PW), f(oy + 1.5), f(cx + PW), f(oy + 1.5))]
    s += plateau(-E, oy + 1.6, *g, final=final)
    s += plateau(E, oy + 1.6, *d, final=final)
    c = V if final else "otInk"
    if eg:
        s.append(r"\node[text=%s] at (%s,%s) {$%s$};" % (c, f(-E), f(oy + .62), eg))
    if ed:
        s.append(r"\node[text=%s] at (%s,%s) {$%s$};" % (c, f(E), f(oy + .62), ed))
    return s


PAS = 3.05   # écart vertical entre deux étapes


def operation(oy, texte):
    """Flèches orange et texte de l'opération, sous la balance dont le socle est en oy."""
    return [r"\draw[fleche] (%s,%s) -- (%s,%s);" % (f(xx), f(oy - .12), f(xx), f(oy - .8)) for xx in (-3.35, 3.35)] \
        + [r"\node[txt] at (0,%s) {%s};" % (f(oy - .46), texte)]


def etapes(liste, ops, conclusion=None):
    """liste : [(g, d, eg, ed)] ; ops : textes entre les étapes ; la dernière étape est en vert."""
    s = []
    for k, (g, d, eg, ed) in enumerate(liste):
        oy = -k * PAS
        s += balance(g, d, oy, eg, ed, final=(k == len(liste) - 1))
        if k < len(liste) - 1:
            s += operation(oy, ops[k])
    if conclusion:
        oy = -(len(liste) - 1) * PAS
        s.append(r"\node[txt,text=otGreenDark] at (0,%s) {%s};" % (f(oy - .5), conclusion))
    return figure(s)


# cours et fiche : 3x + 2 = x + 10
FIGURES["cours_balance"] = etapes(
    [((3, "2"), (1, "10"), "3x + 2", "x + 10"),
     ((2, None), (0, "8"), "2x", "8"),
     ((1, None), (0, "4"), "x", "4")],
    ["on enlève $x$ et $2$ g sur chaque plateau", "on garde la moitié de chaque plateau"])

# exercice 2601
FIGURES["ex2601_balance1"] = figure(balance((3, "4"), (0, "19")))
FIGURES["ex2601_balance2"] = figure(balance((2, "7"), (5, "1")))
FIGURES["ex2601_balance1_corrige"] = etapes(
    [((3, "4"), (0, "19"), "3x + 4", "19"),
     ((3, None), (0, "15"), "3x", "15"),
     ((1, None), (0, "5"), "x", "5")],
    ["on enlève $4$ g sur chaque plateau", "on garde le tiers de chaque plateau"])
FIGURES["ex2601_balance2_corrige"] = etapes(
    [((2, "7"), (5, "1"), "2x + 7", "5x + 1"),
     ((0, "7"), (3, "1"), "7", "3x + 1"),
     ((0, "6"), (3, None), "6", "3x")],
    ["on enlève $2$ boîtes sur chaque plateau", "on enlève $1$ g sur chaque plateau"],
    conclusion=r"donc $3x = 6$ et $x = 6 \div 3 = 2$")


# ================================================================== SCHÉMAS EN BARRES
def barres(lignes, u, H=.56, pas=.82, xlab=-.25, droite=None, total=None, bas=None):
    """lignes : [(nom, [(largeur, texte, style)])] ; style ∈ {'x','n','moins'}.
    droite : textes écrits à droite de chaque ligne ; total : accolade à droite des barres ; bas : texte sous la figure."""
    s, xmax = [], 0.0
    for i, (nom, blocs) in enumerate(lignes):
        y = -i * pas
        s.append(r"\node[txt,anchor=east] at (%s,%s) {%s};" % (f(xlab), f(y + H / 2), nom))
        x = 0.0
        for (w, t, st) in blocs:
            w *= u
            if st == "moins":
                s.append(r"\draw[otOrange!80!black,line width=.8pt,dash pattern=on 2pt off 1.5pt,pattern=north east lines,pattern color=otOrange!70] (%s,%s) rectangle (%s,%s);"
                         % (f(x - w), f(y), f(x), f(y + H)))
                continue
            fond = "otSky" if st == "x" else "otOrange!18"
            s.append(r"\draw[barre,fill=%s] (%s,%s) rectangle (%s,%s);" % (fond, f(x), f(y), f(x + w), f(y + H)))
            s.append(r"\node[text=otInk] at (%s,%s) {%s};" % (f(x + w / 2), f(y + H / 2), t))
            x += w
        xmax = max(xmax, x)
    n = len(lignes)
    if droite:
        for i, t in enumerate(droite):
            s.append(r"\node[anchor=west] at (%s,%s) {%s};" % (f(xmax + .35), f(-i * pas + H / 2), t))
    if total:
        haut, bas_ = H + .05, -(n - 1) * pas - .05
        s.append(r"\draw[accol] (%s,%s) -- (%s,%s);" % (f(xmax + .25), f(haut), f(xmax + .25), f(bas_)))
        s.append(r"\node[anchor=west] at (%s,%s) {%s};" % (f(xmax + .55), f((haut + bas_) / 2), total))
    if bas:
        for j, ligne in enumerate([bas] if isinstance(bas, str) else bas):
            s.append(r"\node[anchor=north] at (%s,%s) {%s};" % (f(xmax / 2), f(-(n - 1) * pas - .3 - .5 * j), ligne))
    return figure(s)


# cours : trois frères, 260 €
U_FR = 1.45
FIGURES["cours_partage"] = barres(
    [("premier", [(1, "$x$", "x")]),
     ("deuxième", [(1, "$x$", "x"), (1 / 3, "$20$", "n")]),
     ("troisième", [(1, "$x$", "x"), (1, "$x$", "x")])],
    U_FR, total=r"$260$ €")

# 2610 : quatre amis, 380 €
U_AM = 1.5
LIGNES_2610 = [("Alice", [(1, "$x$", "x")]),
               ("Bastien", [(1, "$x$", "x"), (.5, "$30$", "n")]),
               ("Chloé", [(1, "$x$", "x"), (1, "$x$", "x")]),
               ("David", [(1, "$x$", "x"), (1, "$x$", "x"), (1 / 6, "", "moins")])]
FIGURES["ex2610_schema"] = barres(
    LIGNES_2610, U_AM,
    droite=["$x$", "$x + 30$", "$2x$", "$2x - 10$"],
    bas=[r"\textcolor{otOrange!80!black}{hachures : les $10$ € en moins de David}",
         r"en tout : $380$ €"])
FIGURES["ex2610_corrige"] = barres(
    LIGNES_2610, U_AM,
    droite=[vert("$60$ €"), vert("$90$ €"), vert("$120$ €"), vert("$110$ €")],
    bas=vert(r"$60 + 90 + 120 + 110 = 380$ €"))


# ================================================================== FRISE DES ÂGES (2607)
def frise_ages(cols, corrige):
    """cols : [(abscisse, quand, âge Léa, âge père)]."""
    xmin, xmax = cols[0][0] - .9, cols[-1][0] + .75
    s = [r"\draw[axe] (%s,0) -- (%s,0);" % (f(xmin), f(xmax)),
         r"\node[petit,anchor=west] at (%s,0) {temps};" % f(xmax + .1),
         r"\node[txt,anchor=east] at (%s,-.75) {Léa};" % f(xmin - .1),
         r"\node[txt,anchor=east] at (%s,-1.45) {père};" % f(xmin - .1)]
    for (x, q, a, b) in cols:
        s += [r"\draw[otNavy,line width=1pt] (%s,-.12) -- (%s,.12);" % (f(x), f(x)),
              r"\fill[otNavy] (%s,0) circle (2.2pt);" % f(x),
              r"\node[petit,anchor=south] at (%s,.3) {%s};" % (f(x), q),
              r"\node at (%s,-.75) {%s};" % (f(x), a),
              r"\node at (%s,-1.45) {%s};" % (f(x), b)]
    return s


FIGURES["ex2607_enonce"] = figure(frise_ages(
    [(0, "aujourd'hui", "$12$ ans", "$40$ ans"),
     (3.6, "dans $x$ années", "?", "?")], False))

_c = [(0, "il y a $5$ ans", vert("$7$ ans"), vert("$35$ ans")),
      (2.1, "aujourd'hui", "$12$ ans", "$40$ ans"),
      (4.6, "dans $16$ ans", vert("$28$ ans"), vert("$56$ ans"))]
FIGURES["ex2607_corrige"] = figure(
    frise_ages(_c, True)
    + [r"\draw[accol] (0,.85) -- (2.1,.85) node[midway,above=6pt,petit] {$5$ ans};",
       r"\draw[accol] (2.1,.85) -- (4.6,.85) node[midway,above=6pt,petit] {$16$ ans};",
       r"\node[txt,text=otGreenDark] at (0,-2.15) {$35 = 5 \times 7$};",
       r"\node[txt,text=otGreenDark] at (4.6,-2.15) {$56 = 2 \times 28$};"])


# ================================================================== TRIANGLE ET RECTANGLE (2608)
def fig2608(corr):
    k = .2
    b, c = 14 * k, 11 * k
    h = sqrt(c * c - (b / 2) ** 2)
    ox = b + 1.3
    lw, LL = 7 * .155, 21 * .155
    s = [r"\coordinate (B) at (0,0); \coordinate (C) at (%s,0); \coordinate (A) at (%s,%s);" % (f(b), f(b / 2), f(h)),
         r"\fill[otSky] (A) -- (B) -- (C) -- cycle;",
         r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;",
         r"\codage{A}{B} \codage{A}{C}",
         r"\node[anchor=south,yshift=2pt] at (A) {$A$};",
         r"\node[anchor=north east] at (B) {$B$};",
         r"\node[anchor=north west] at (C) {$C$};",
         r"\coordinate (E) at (%s,0); \coordinate (F) at (%s,0); \coordinate (G) at (%s,%s); \coordinate (H) at (%s,%s);"
         % (f(ox), f(ox + LL), f(ox + LL), f(lw), f(ox), f(lw)),
         r"\fill[otOrange!15] (E) rectangle (G);",
         r"\draw[geoTrait] (E) rectangle (G);",
         r"\angledroit{F}{E}{H} \angledroit{E}{F}{G} \angledroit{F}{G}{H} \angledroit{G}{H}{E}",
         r"\node[anchor=north east] at (E) {$E$};", r"\node[anchor=north west] at (F) {$F$};",
         r"\node[anchor=south west] at (G) {$G$};", r"\node[anchor=south east] at (H) {$H$};"]
    # milieux des côtés obliques, étiquettes décalées vers l'extérieur
    mx1, my1 = b / 4, h / 2
    mx2 = 3 * b / 4
    if corr:
        s += [r"\node[text=otGreenDark,anchor=south east] at (%s,%s) {$11$ cm};" % (f(mx1 - .12), f(my1 + .05)),
              r"\node[text=otGreenDark,anchor=south west] at (%s,%s) {$11$ cm};" % (f(mx2 + .12), f(my1 + .05)),
              r"\node[text=otGreenDark,anchor=north] at (%s,-.35) {$14$ cm};" % f(b / 2),
              r"\node[text=otGreenDark,anchor=east] at (%s,%s) {$7$ cm};" % (f(ox - .45), f(lw / 2)),
              r"\node[text=otGreenDark,anchor=north] at (%s,-.35) {$21$ cm};" % f(ox + LL / 2),
              r"\node[txt,text=otGreenDark] at (%s,%s) {aire $147$ cm²};" % (f(ox + LL / 2), f(lw / 2)),
              r"\node[txt,text=otGreenDark,anchor=north] at (%s,-.95) {$11 + 11 + 14 = 36$};" % f(b / 2),
              r"\node[txt,text=otGreenDark,anchor=north] at (%s,-.95) {$2 \times (7 + 21) = 56$};" % f(ox + LL / 2)]
    else:
        s += [r"\node[anchor=south east] at (%s,%s) {$x$};" % (f(mx1 - .12), f(my1 + .05)),
              r"\node[anchor=south west] at (%s,%s) {$x$};" % (f(mx2 + .12), f(my1 + .05)),
              r"\node[anchor=north] at (%s,-.35) {$x + 3$};" % f(b / 2),
              r"\node[anchor=east] at (%s,%s) {$\ell$};" % (f(ox - .45), f(lw / 2)),
              r"\node[txt,anchor=north] at (%s,-.95) {périmètre : $36$ cm};" % f(b / 2),
              r"\node[txt,anchor=north] at (%s,-.95) {périmètre : $56$ cm};" % f(ox + LL / 2)]
    return figure(s)


FIGURES["ex2608_enonce"] = fig2608(False)
FIGURES["ex2608_corrige"] = fig2608(True)


# ================================================================== ANGLES D'UN TRIANGLE (2611)
def fig2611(corr):
    k = .92
    AB = 5 * k
    AC = AB / sin(radians(60)) * sin(radians(40))
    Cx, Cy = AC * cos(radians(80)), AC * sin(radians(80))
    s = [r"\coordinate (A) at (0,0); \coordinate (B) at (%s,0); \coordinate (C) at (%s,%s);" % (f(AB), f(Cx), f(Cy)),
         r"\fill[otSky] (A) -- (B) -- (C) -- cycle;",
         r"\draw[otOrange!85!black,line width=.8pt] (A) ++(0:.55) arc (0:80:.55);",
         r"\draw[otOrange!85!black,line width=.8pt] (B) ++(180:.8) arc (180:140:.8);",
         r"\draw[otOrange!85!black,line width=.8pt] (C) ++(260:.55) arc (260:320:.55);",
         r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;",
         r"\node[anchor=north east] at (A) {$A$};",
         r"\node[anchor=north west] at (B) {$B$};",
         r"\node[anchor=south,yshift=2pt] at (C) {$C$};"]
    # étiquettes sur les bissectrices, à l'intérieur du triangle
    def lab(px, py, ang, r, t):
        return r"\node[text=%s] at (%s,%s) {%s};" % (V if corr else "otInk", f(px + r * cos(radians(ang))), f(py + r * sin(radians(ang))), t)
    if corr:
        s += [lab(0, 0, 40, 1.05, "$80°$"), lab(AB, 0, 160, 1.45, "$40°$"), lab(Cx, Cy, 290, 1.15, "$60°$")]
    else:
        s += [lab(0, 0, 40, .95, "$2x$"), lab(AB, 0, 160, 1.35, "$x$"), lab(Cx, Cy, 290, 1.3, "$x + 20$")]
    return figure(s)


FIGURES["ex2611_enonce"] = fig2611(False)
FIGURES["ex2611_corrige"] = fig2611(True)


# ================================================================== CARRÉ ET RECTANGLE (2612)
def fig2612(corr):
    if corr:
        k, c, L, l = .4, 4, 8, 2
    else:
        k, c, L, l = .36, 5, 9, 3
    cc, LL, ll = c * k, L * k, l * k
    ox = cc + 1.75
    s = [r"\coordinate (A) at (0,0); \coordinate (B) at (%s,0); \coordinate (C) at (%s,%s); \coordinate (D) at (0,%s);" % (f(cc), f(cc), f(cc), f(cc)),
         r"\coordinate (E) at (%s,0); \coordinate (F) at (%s,0); \coordinate (G) at (%s,%s); \coordinate (H) at (%s,%s);" % (f(ox), f(ox + LL), f(ox + LL), f(ll), f(ox), f(ll)),
         r"\fill[otSky] (A) rectangle (C);", r"\draw[geoTrait] (A) rectangle (C);",
         r"\fill[otOrange!15] (E) rectangle (G);", r"\draw[geoTrait] (E) rectangle (G);",
         r"\angledroit{B}{A}{D} \angledroit{F}{E}{H}"]
    if corr:
        s += [r"\coteSous[.4]{B}{A}{$4$ cm}", r"\cote[.4]{A}{D}{\textcolor{otGreenDark}{$4$}}",
              r"\coteSous[.4]{F}{E}{$8$ cm}", r"\cote[.4]{E}{H}{\textcolor{otGreenDark}{$2$}}",
              r"\node[txt,text=otGreenDark] at (%s,%s) {$16$ cm²};" % (f(cc / 2), f(cc / 2)),
              r"\node[txt,text=otGreenDark] at (%s,%s) {$16$ cm²};" % (f(ox + LL / 2), f(ll / 2))]
    else:
        s += [r"\cote[.4]{B}{A}{$x$}", r"\cote[.4]{A}{D}{$x$}",
              r"\cote[.4]{F}{E}{$x + 4$}", r"\cote[.4]{E}{H}{$x - 2$}",
              r"\node[txt] at (%s,%s) {carré};" % (f(cc / 2), f(cc / 2)),
              r"\node[txt] at (%s,%s) {rectangle};" % (f(ox + LL / 2), f(ll / 2))]
    return figure(s)


FIGURES["ex2612_enonce"] = fig2612(False)
FIGURES["ex2612_corrige"] = fig2612(True)


# ================================================================== FORFAITS (2614)
def fig2614():
    k = .011
    X = lambda m: m * k
    fin = 560
    H0, H1 = .12, .58
    s = [r"\fill[otSky] (%s,%s) rectangle (%s,%s);" % (f(X(0)), f(H0), f(X(60)), f(H1)),
         r"\fill[otGreen!20] (%s,%s) rectangle (%s,%s);" % (f(X(60)), f(H0), f(X(360)), f(H1)),
         r"\fill[otOrange!20] (%s,%s) rectangle (%s,%s);" % (f(X(360)), f(H0), f(X(fin - 20)), f(H1)),
         r"\draw[otNavy,line width=.8pt] (%s,%s) rectangle (%s,%s);" % (f(X(0)), f(H0), f(X(60)), f(H1)),
         r"\draw[otGreenDark,line width=.8pt] (%s,%s) rectangle (%s,%s);" % (f(X(60)), f(H0), f(X(360)), f(H1)),
         r"\draw[otOrange!80!black,line width=.8pt] (%s,%s) -- (%s,%s) -- (%s,%s) -- (%s,%s);" % (f(X(fin - 20)), f(H1), f(X(360)), f(H1), f(X(360)), f(H0), f(X(fin - 20)), f(H0)),
         r"\node[text=otNavy] at (%s,%s) {A};" % (f(X(30)), f((H0 + H1) / 2)),
         r"\node[text=otGreenDark] at (%s,%s) {B};" % (f(X(210)), f((H0 + H1) / 2)),
         r"\node[text=otOrange!80!black] at (%s,%s) {C};" % (f(X(450)), f((H0 + H1) / 2)),
         r"\node[txt] at (%s,%s) {forfait le moins cher};" % (f(X(280)), f(H1 + .38)),
         r"\draw[axe] (0,0) -- (%s,0);" % f(X(fin)),
         r"\node[petit,anchor=west] at (%s,0) {min};" % f(X(fin) + .1)]
    for m in (0, 60, 360):
        s += [r"\draw[otMuted,line width=.6pt] (%s,-.1) -- (%s,0);" % (f(X(m)), f(X(m))),
              r"\node[petit,anchor=north] at (%s,-.17) {$%d$};" % (f(X(m)), m)]
    s += [r"\node[txt,text=otGreenDark,anchor=north] at (%s,-.68) {A et B : $15$ €};" % f(X(60) + .35),
          r"\node[txt,text=otGreenDark,anchor=north] at (%s,-.68) {B et C : $30$ €};" % f(X(360))]
    return figure(s)


FIGURES["ex2614_corrige"] = fig2614()


# ================================================================== POURSUITE (2615)
def fig2615(corr):
    k = .215
    X = lambda d: d * k
    fin = 26.5
    yL, yM = 1.25, .45
    s = [r"\draw[axe,otNavy] (0,%s) -- (%s,%s);" % (f(yL), f(X(fin)), f(yL)),
         r"\draw[axe,otOrange!85!black] (0,%s) -- (%s,%s);" % (f(yM), f(X(fin)), f(yM)),
         r"\node[txt,anchor=east] at (-.25,%s) {Léo};" % f(yL),
         r"\node[txt,anchor=east] at (-.25,%s) {Mia};" % f(yM),
         r"\node[petit,anchor=west] at (%s,%s) {$15$ km/h};" % (f(X(fin) + .1), f(yL)),
         r"\node[petit,anchor=west] at (%s,%s) {$25$ km/h};" % (f(X(fin) + .1), f(yM))]
    if corr:
        s.append(r"\draw[otMuted,line width=.6pt] (0,-.25) -- (%s,-.25);" % f(X(fin)))
        for d in range(0, 26, 5):
            s += [r"\draw[otMuted,line width=.6pt] (%s,-.35) -- (%s,-.15);" % (f(X(d)), f(X(d))),
                  r"\node[petit,anchor=north] at (%s,-.42) {$%d$};" % (f(X(d)), d)]
        s += [r"\node[petit,anchor=west] at (%s,-.25) {km};" % f(X(fin) + .1),
              r"\draw[otNavy,fill=white,line width=.9pt] (%s,%s) circle (2.4pt);" % (f(X(7.5)), f(yL)),
              r"\node[petit,anchor=south] at (%s,%s) {$14$ h $30$};" % (f(X(7.5)), f(yL + .18)),
              r"\draw[otOrange!85!black,fill=white,line width=.9pt] (0,%s) circle (2.4pt);" % f(yM),
              r"\node[petit,anchor=north west] at (.1,%s) {$14$ h $30$};" % f(yM - .14),
              r"\draw[guide] (%s,%s) -- (%s,-.25);" % (f(X(18.75)), f(yL), f(X(18.75))),
              r"\fill[otGreenDark] (%s,%s) circle (2.8pt);" % (f(X(18.75)), f(yL)),
              r"\fill[otGreenDark] (%s,%s) circle (2.8pt);" % (f(X(18.75)), f(yM)),
              r"\node[txt,text=otGreenDark,anchor=south] at (%s,%s) {$15$ h $15$};" % (f(X(18.75)), f(yL + .18)),
              r"\node[txt,text=otGreenDark,anchor=north] at (%s,-.95) {rattrapage à $18{,}75$ km du départ};" % f(X(13))]
    else:
        s += [r"\draw[guide] (0,%s) -- (0,%s);" % (f(yL), f(yM)),
              r"\node[petit,anchor=north] at (0,%s) {départ};" % f(yM - .32),
              r"\fill[otNavy] (%s,%s) circle (2.6pt);" % (f(X(7.5)), f(yL)),
              r"\fill[otOrange!85!black] (0,%s) circle (2.6pt);" % f(yM),
              r"\draw[accol] (0,%s) -- (%s,%s);" % (f(yL + .2), f(X(7.5)), f(yL + .2)),
              r"\node[petit,anchor=south] at (%s,%s) {avance de Léo : ?};" % (f(X(3.75)), f(yL + .5)),
              r"\node[txt,anchor=south] at (%s,%s) {à $14$ h $30$};" % (f(X(15)), f(yL + .45))]
    return figure(s)


FIGURES["ex2615_enonce"] = fig2615(False)
FIGURES["ex2615_corrige"] = fig2615(True)


# ================================================================== TERRAIN (2616)
def fig2616(xc, corr):
    k = .045
    L, l, c = 120 * k, 80 * k, xc * k
    s = [r"\coordinate (A) at (0,0); \coordinate (B) at (%s,0); \coordinate (C) at (%s,%s); \coordinate (D) at (0,%s);" % (f(L), f(L), f(l), f(l)),
         r"\coordinate (K) at (%s,0); \coordinate (Kh) at (%s,%s);" % (f(c), f(c), f(l)),
         r"\fill[otSky] (A) rectangle (Kh);", r"\fill[otGreen!15] (K) rectangle (C);",
         r"\draw[geoTrait] (A) rectangle (C);",
         r"\draw[otOrange!85!black,line width=1.6pt] (K) -- (Kh);",
         r"\cote[.4]{D}{C}{$120$ m}", r"\cote[.4]{A}{D}{$80$ m}"]
    if corr:
        s += [r"\coteSous[.4]{K}{A}{$80$ m}", r"\coteSous[.4]{B}{K}{$40$ m}",
              r"\node[txt] at (%s,%s) {parcelle 1};" % (f(c / 2), f(l * .6)),
              r"\node[txt,text=otGreenDark] at (%s,%s) {$6\,400$ m²};" % (f(c / 2), f(l * .4)),
              r"\node[txt] at (%s,%s) {parcelle 2};" % (f((c + L) / 2), f(l * .6)),
              r"\node[txt,text=otGreenDark] at (%s,%s) {$3\,200$ m²};" % (f((c + L) / 2), f(l * .4))]
    else:
        s += [r"\cote[.4]{K}{A}{$x$}",
              r"\node[txt] at (%s,%s) {parcelle 1};" % (f(c / 2), f(l / 2)),
              r"\node[txt] at (%s,%s) {parcelle 2};" % (f((c + L) / 2), f(l / 2)),
              r"\node[petit,anchor=north west,text=otOrange!85!black] at (%s,%s) {clôture};" % (f(c + .12), f(l - .12))]
    return figure(s)


FIGURES["ex2616_enonce"] = fig2616(75, False)
FIGURES["ex2616_corrige"] = fig2616(80, True)


# ================================================================== CARRÉ ET TRIANGLE SUR UN SEGMENT (2619)
def fig2619(xv, corr):
    k = .52
    AB, s_ = 12 * k, xv * k
    t = AB - s_
    Qx, Qy = s_ + t / 2, t * sqrt(3) / 2
    s = [r"\coordinate (A) at (0,0); \coordinate (M) at (%s,0); \coordinate (B) at (%s,0);" % (f(s_), f(AB)),
         r"\coordinate (N) at (%s,%s); \coordinate (P) at (0,%s); \coordinate (Q) at (%s,%s);" % (f(s_), f(s_), f(s_), f(Qx), f(Qy)),
         r"\fill[otSky] (A) rectangle (N);", r"\fill[otGreen!15] (M) -- (B) -- (Q) -- cycle;",
         r"\draw[geoTrait] (A) -- (M) -- (N) -- (P) -- cycle;",
         r"\draw[geoTrait] (M) -- (B) -- (Q) -- cycle;",
         r"\angledroit{M}{A}{P} \angledroit{A}{M}{N} \angledroit{M}{N}{P} \angledroit{N}{P}{A}",
         r"\codage[2]{M}{Q} \codage[2]{Q}{B} \codage[2]{M}{B}",
         r"\node[anchor=north east] at (A) {$A$};", r"\node[anchor=north west] at (B) {$B$};",
         r"\node[anchor=south east] at (P) {$P$};", r"\node[anchor=south,yshift=2pt] at (Q) {$Q$};",
         r"\node[anchor=south,yshift=1pt] at (N) {$N$};",
         r"\fill[otNavy] (M) circle (1.8pt);"]
    if corr:
        s += [r"\node[anchor=north west,xshift=1pt,yshift=-1pt] at (M) {$M$};",
              r"\coteSous[.75]{M}{A}{$\frac{36}{7}$ cm}",
              r"\coteSous[.75]{B}{M}{$\frac{48}{7}$ cm}",
              r"\node[txt,text=otGreenDark,anchor=north] at (%s,-1.85) {$4 \times \frac{36}{7} = 3 \times \frac{48}{7} = \frac{144}{7}$ cm};" % f(AB / 2)]
    else:
        s += [r"\node[anchor=north west,xshift=1pt,yshift=-1pt] at (M) {$M$};",
              r"\cote[.75]{M}{A}{$x$}",
              r"\cote[1.5]{B}{A}{$12$ cm}"]
    return figure(s)


FIGURES["ex2619_enonce"] = fig2619(4, False)
FIGURES["ex2619_corrige"] = fig2619(36 / 7, True)


# ================================================================== DIOPHANTE (2620)
def fig2620():
    k = .09
    X = lambda a: a * k
    H = .62
    etapes_ = [(0, 14, r"\frac{x}{6}", "otSky"), (14, 21, r"\frac{x}{12}", "otGreen!18"),
               (21, 33, r"\frac{x}{7}", "otSky"), (33, 38, "5", "otOrange!20"),
               (38, 80, r"\frac{x}{2}", "otGreen!18"), (80, 84, "4", "otOrange!20")]
    s = []
    for (a, b, e, c) in etapes_:
        s += [r"\fill[%s] (%s,0) rectangle (%s,%s);" % (c, f(X(a)), f(X(b)), f(H)),
              r"\node[text=otInk,anchor=south] at (%s,%s) {$%s$};" % (f(X((a + b) / 2)), f(H + .12), e),
              r"\node[text=otGreenDark] at (%s,%s) {$%d$};" % (f(X((a + b) / 2)), f(H / 2), b - a)]
    s.append(r"\draw[barre] (0,0) rectangle (%s,%s);" % (f(X(84)), f(H)))
    for a in (14, 21, 33, 38, 80):
        s.append(r"\draw[barre] (%s,0) -- (%s,%s);" % (f(X(a)), f(X(a)), f(H)))
    for a in (0, 14, 21, 33, 38, 84):
        s.append(r"\node[petit,anchor=north] at (%s,-.1) {$%d$};" % (f(X(a)), a))
    s += [r"\draw[accol] (%s,-.55) -- (0,-.55);" % f(X(84)),
          r"\node[txt,text=otGreenDark,anchor=north] at (%s,-.85) {Diophante a vécu $x = 84$ ans};" % f(X(42)),
          r"\node[petit,anchor=north] at (%s,-1.35) {mariage à $33$ ans ; fils né à $38$ ans};" % f(X(42)),
          r"\node[petit,anchor=north] at (%s,-1.8) {mort du fils à $80$ ans};" % f(X(42))]
    return figure(s)


FIGURES["ex2620_corrige"] = fig2620()
