# -*- coding: utf-8 -*-
"""Figures de la notion « Variables aléatoires réelles » (Première spécialité).

Compilation (style des livres OptiTAB, contrôle des chevauchements) :

    python ../../../outils/figures_livre.py <dossier_notion> [nom …] [--planche]

- Arbres pondérés : coordonnées calculées en Python (repris de la notion
  Terminale 179), probabilités posées à côté des branches, jamais sur un trait.
  Version « énoncé » : squelette sans probabilités ; version « corrigé » :
  probabilités et valeurs de la variable en vert.
- Diagrammes en bâtons : pgfplots, sans quadrillage (aucune étiquette sur un
  trait) ; bâtons bleus dans le cours, verts dans les corrigés.
- Simulations : graines fixes ; les mêmes fonctions servent au script
  ../verif_variables_aleatoires.py, qui contrôle les nombres cités dans le texte.
"""
import math
import random
from fractions import Fraction
from itertools import product

PREAMBULE_EXTRA = r"""
\tikzset{
  evt/.style={font=\normalsize, text=otNavy, inner sep=2.4pt},
  branche/.style={otNavy!65, line width=0.8pt, line cap=round},
  poids/.style={font=\small, text=otInk, inner sep=1.7pt},
  poidsV/.style={poids, text=otGreenDark},
  issue/.style={font=\small, text=otMuted, anchor=west, inner sep=1.5pt},
  issueV/.style={issue, text=otGreenDark},
  racine/.style={fill=otNavy},
  legende/.style={font=\otRegular\fontsize{9}{10}\selectfont, text=otMuted, inner sep=1.5pt},
  legendeV/.style={font=\otMedium\fontsize{9}{10}\selectfont, text=otGreenDark, inner sep=1.5pt},
}
\pgfplotsset{otLoi/.style={
  axis lines=left,
  axis line style={otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}},
  tick style={otMuted,line width=0.5pt}, major tick length=3pt, tick align=outside,
  ticklabel style={font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted},
  xticklabel style={yshift=-1pt},
  every axis x label/.style={at={(current axis.right of origin)},anchor=west,font=\normalsize,text=otMuted,xshift=2pt},
  every axis y label/.style={at={(current axis.north west)},anchor=south,font=\normalsize,text=otMuted,yshift=4pt},
  scale only axis, clip=false, ymin=0,
  /pgf/number format/use comma, /pgf/number format/1000 sep={\,},
}}
\pgfplotsset{otBas/.style={axis x line=bottom, axis y line=left,
  every axis x label/.style={at={(current axis.south east)},anchor=west,font=\normalsize,text=otMuted,xshift=4pt}}}
"""

FIGURES = {}


# ================================================================ données des simulations
def _gain(r):
    d = r.randint(1, 6)
    return 5 if d == 6 else (1 if d % 2 == 0 else -2)


def moyennes_cumulees():
    """Jeu de dé du cours : moyenne après n parties, n = 1 … 2000 (graine 6)."""
    r = random.Random(6)
    s, out = 0, []
    for n in range(1, 2001):
        s += _gain(r)
        out.append(s / n)
    return out


def moyennes_echantillons_cours():
    """100 échantillons de taille 100 du gain du jeu de dé (graine 2)."""
    r = random.Random(2)
    return [sum(_gain(r) for _ in range(100)) / 100 for _ in range(100)]


def moyennes_echantillons_de():
    """200 échantillons de taille 100 du numéro d'un dé (graine 2)."""
    r = random.Random(2)
    return [sum(r.randint(1, 6) for _ in range(100)) / 100 for _ in range(200)]


# ================================================================ arbres
def N(nom, poids, *enfants, droite=None):
    return {"nom": nom, "poids": poids, "enfants": list(enfants), "droite": droite}


def _placer(n, prof, y, dy, L):
    n["x"] = prof * L
    if not n["enfants"]:
        n["y"] = y
        return y - dy
    ys = []
    for c in n["enfants"]:
        y = _placer(c, prof + 1, y, dy, L)
        ys.append(c["y"])
    n["y"] = (ys[0] + ys[-1]) / 2
    return y


def arbre(enfants, L=2.3, dy=1.0, squelette=False, ecart_droite="4pt"):
    """Arbre pondéré horizontal. squelette=True : sans probabilités ni textes
    de droite (énoncé) ; sinon probabilités et textes de droite en vert (corrigé)."""
    racine = {"nom": None, "poids": None, "enfants": enfants, "droite": None}
    _placer(racine, 0, 0.0, dy, L)
    noeuds, aretes, poids, droites = [], [], [], []
    k = [0]

    def visiter(n, parent_ref, parent_y):
        for c in n["enfants"]:
            k[0] += 1
            nom = f"n{k[0]}"
            noeuds.append(rf"\node[evt] ({nom}) at ({c['x']:.3f},{c['y']:.3f}) {{${c['nom']}$}};")
            aretes.append(rf"\draw[branche] {parent_ref} -- ({nom}.west);")
            if c["poids"] is not None and not squelette:
                ecart = c["y"] - parent_y
                anc = "south east" if ecart > 1e-6 else ("north east" if ecart < -1e-6 else "south")
                poids.append(rf"\path {parent_ref} -- ({nom}.west) node[poidsV,pos=0.5,anchor={anc}] {{${c['poids']}$}};")
            if not c["enfants"] and c["droite"] and not squelette:
                droites.append(rf"\node[issueV] at ([xshift={ecart_droite}]{nom}.east) {{{c['droite']}}};")
            visiter(c, f"({nom}.east)", c["y"])

    lignes = [r"\begin{tikzpicture}[x=1cm,y=1cm]", rf"\coordinate (r) at (0,{racine['y']:.3f});"]
    visiter(racine, "(r)", racine["y"])
    lignes += noeuds + aretes + [r"\fill[racine] (r) circle (1.9pt);"] + poids + droites
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


def F(p, q):
    return rf"\dfrac{{{p}}}{{{q}}}"


def fr_tex(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else F(x.numerator, x.denominator)


def urne2(n1, n2, nom1, nom2, valeur, droite_fmt, squelette=False, **kw):
    """Deux tirages sans remise ; nom1(k), nom2(k) : noms LaTeX des événements ;
    valeur(issue) : valeur de la variable ; droite_fmt(issue, v, p) : texte de droite."""
    eff = {1: n1, 2: n2}
    noms = {1: nom1, 2: nom2}

    def sous(reste, issue, k):
        tot = sum(reste.values())
        out = []
        for c in (1, 2):
            if reste[c] == 0:
                continue
            r2 = dict(reste)
            r2[c] -= 1
            iss = issue + (c,)
            if k == 2:
                p = Fraction(1)
                rr = dict(eff)
                for l in iss:
                    p *= Fraction(rr[l], sum(rr.values()))
                    rr[l] -= 1
                out.append(N(noms[c](k), F(reste[c], tot), droite=droite_fmt(iss, valeur(iss), p)))
            else:
                out.append(N(noms[c](k), F(reste[c], tot), *sous(r2, iss, k + 1)))
        return out

    return arbre(sous(dict(eff), (), 1), squelette=squelette, **kw)


# ---------------------------------------------------------------- cours : urne 3R 2B
FIGURES["cours_arbre"] = urne2(
    3, 2, lambda k: f"R_{k}", lambda k: f"B_{k}",
    valeur=lambda iss: iss.count(1),
    droite_fmt=lambda iss, v, p: rf"$X = {v}$ \quad ${fr_tex(p)}$",
    L=2.5, dy=1.05)
# le cours n'est pas un corrigé : probabilités en noir, textes de droite en gris
FIGURES["cours_arbre"] = FIGURES["cours_arbre"].replace("poidsV", "poids").replace("issueV", "issue")


# ---------------------------------------------------------------- 1331 : trois lancers
def _pieces(squelette):
    def sous(issue, k):
        out = []
        for e in ("P", "F"):
            iss = issue + e
            if k == 3:
                out.append(N(e, F(1, 2), droite=rf"{iss} : $Z = {iss.count('P')}$"))
            else:
                out.append(N(e, F(1, 2), *sous(iss, k + 1)))
        return out
    return arbre(sous("", 1), L=1.85, dy=1.0, squelette=squelette)


FIGURES["ex1331_arbre_enonce"] = _pieces(True)
FIGURES["ex1331_arbre"] = _pieces(False)

# ---------------------------------------------------------------- 1333 : 4 blanches, 6 noires
for suf, sq in (("_enonce", True), ("", False)):
    FIGURES["ex1333_arbre" + suf] = urne2(
        4, 6, lambda k: f"B_{k}", lambda k: f"N_{k}",
        valeur=lambda iss: iss.count(1),
        droite_fmt=lambda iss, v, p: rf"$Y = {v}$ \quad ${fr_tex(p)}$",
        squelette=sq, L=2.5, dy=1.05)

# ---------------------------------------------------------------- 1336 : 2 gagnants, 4 perdants
for suf, sq in (("_enonce", True), ("", False)):
    FIGURES["ex1336_arbre" + suf] = urne2(
        2, 4, lambda k: f"W_{k}", lambda k: f"L_{k}",
        valeur=lambda iss: iss.count(1),
        droite_fmt=lambda iss, v, p: rf"$X = {v}$ \quad ${fr_tex(p)}$",
        squelette=sq, L=2.5, dy=1.05)

# ---------------------------------------------------------------- 1338 : 5 rouges, 5 non rouges
for suf, sq in (("_enonce", True), ("", False)):
    FIGURES["ex1338_arbre" + suf] = urne2(
        5, 5, lambda k: f"R_{k}", lambda k: rf"\overline{{R_{k}}}",
        valeur=lambda iss: iss.count(1),
        droite_fmt=lambda iss, v, p: rf"$Z = {v}$ \quad ${fr_tex(p)}$",
        squelette=sq, L=2.5, dy=1.05)


# ================================================================ diagrammes en bâtons
def batons(points, xmin, xmax, ymax, xticks, yticks, couleur="otNavy!60", etiquettes=None,
           largeur=7.6, hauteur=4.2, xlabel="x_i", ylabel="P(X = x_i)", vide=False, extra="",
           epaisseur="8pt"):
    """points : [(x, p)] ; yticks : [(valeur, texte LaTeX)] ; etiquettes : {x: texte au-dessus}."""
    yt = ",".join(f"{v:.6f}" for v, _ in yticks)
    ytl = ",".join("{$" + t + "$}" for _, t in yticks)
    xt = ",".join(str(x) for x in xticks)
    lignes = [r"\begin{tikzpicture}",
              rf"\begin{{axis}}[otLoi, width={largeur}cm, height={hauteur}cm, xmin={xmin}, xmax={xmax}, ymax={ymax},",
              rf"  xtick={{{xt}}}, ytick={{{yt}}}, yticklabels={{{ytl}}},",
              rf"  xlabel={{${xlabel}$}}, ylabel={{${ylabel}$}}]"]
    if not vide:
        coords = " ".join(f"({x},{float(p):.6f})" for x, p in points)
        lignes.append(rf"\addplot[ycomb, line width={epaisseur}, {couleur}] coordinates {{{coords}}};")
        for x, t in (etiquettes or {}).items():
            p = dict(points)[x]
            lignes.append(rf"\node[anchor=south, font=\normalsize, inner sep=1.5pt, yshift=1pt] at (axis cs:{x},{float(p):.6f}) {{${t}$}};")
    lignes.append(extra)
    lignes += [r"\end{axis}", r"\end{tikzpicture}"]
    return "\n".join(lignes)


# ---------------------------------------------------------------- cours : loi du gain
FIGURES["cours_loi"] = batons(
    [(-2, Fraction(1, 2)), (1, Fraction(1, 3)), (5, Fraction(1, 6))],
    xmin=-3, xmax=6, ymax=0.72, largeur=7.2, xticks=list(range(-2, 6)),
    yticks=[(0.1, "0{,}1"), (0.2, "0{,}2"), (0.3, "0{,}3"), (0.4, "0{,}4"), (0.5, "0{,}5"), (0.6, "0{,}6")],
    etiquettes={-2: r"\dfrac{1}{2}", 1: r"\dfrac{1}{3}", 5: r"\dfrac{1}{6}"},
    extra=r"""\draw[otGreenDark, line width=0.9pt, dash pattern=on 4pt off 2.5pt] (axis cs:0.1667,0) -- (axis cs:0.1667,0.58);
\node[anchor=south, legendeV] at (axis cs:0.1667,0.58) {$E(X) = \dfrac{1}{6} \approx 0{,}17$};""")


# ---------------------------------------------------------------- cours : même espérance, dispersions différentes
def _dispersion(nom, valeur, sigma, decal):
    return rf"""\begin{{axis}}[otLoi, at={{({decal}cm,0)}}, width=2.9cm, height=3.4cm, xmin=-4.2, xmax=4.4, ymax=0.82,
  xtick={{-3,-1,1,3}}, ytick={{0.25,0.5}}, yticklabels={{{{$0{{,}}25$}},{{$0{{,}}5$}}}},
  xlabel={{${nom.lower()}_i$}}, ylabel={{$P({nom} = {nom.lower()}_i)$}}]
\addplot[ycomb, line width=8pt, otNavy!60] coordinates {{(-{valeur},0.5) ({valeur},0.5)}};
\draw[otGreenDark, line width=0.9pt, {{Stealth[length=2mm]}}-{{Stealth[length=2mm]}}] (axis cs:-{sigma},0.66) -- (axis cs:{sigma},0.66);
\node[anchor=south, legendeV, yshift=1pt] at (axis cs:0,0.66) {{$\sigma({nom}) = {sigma}$}};
\node[anchor=north, legende, yshift=-18pt] at (axis cs:0,0) {{Jeu ${nom}$ : $E({nom}) = 0$}};
\end{{axis}}"""


FIGURES["cours_dispersion"] = ("\\begin{tikzpicture}\n" + _dispersion("A", 1, 1, 0) + "\n"
                               + _dispersion("B", 3, 3, 4.6) + "\n\\end{tikzpicture}")


# ---------------------------------------------------------------- cours : moyenne cumulée
def _simulation():
    moy = moyennes_cumulees()
    pts = [(n, moy[n - 1]) for n in list(range(1, 200)) + list(range(200, 2001, 5))]
    coords = " ".join(f"({n},{m:.4f})" for n, m in pts)
    return rf"""\begin{{tikzpicture}}
\begin{{axis}}[otLoi, otBas, width=5.6cm, height=4.6cm, xmin=0, xmax=2100, ymin=-2.2, ymax=1.1,
  xtick={{500,1000,1500,2000}}, ytick={{-2,-1,0,1}}, yticklabels={{{{$-2$}},{{$-1$}},{{$0$}},{{$1$}}}},
  xticklabels={{{{$500$}},{{$1\,000$}},{{$1\,500$}},{{$2\,000$}}}},
  xlabel={{$n$}}, ylabel={{moyenne observée (€)}}]
\draw[otMuted!60, line width=0.5pt] (axis cs:0,0) -- (axis cs:2100,0);
\draw[otGreenDark, line width=0.9pt, dash pattern=on 4pt off 2.5pt] (axis cs:0,0.16667) -- (axis cs:2100,0.16667);
\addplot[courbe, line width=1pt] coordinates {{{coords}}};
\node[anchor=west, legendeV] at (axis cs:2120,0.16667) {{$E(X) \approx 0{{,}}17$}};
\end{{axis}}
\end{{tikzpicture}}"""


FIGURES["cours_simulation"] = _simulation()


# ---------------------------------------------------------------- nuages de moyennes d'échantillons
def _nuage(ms, mu, h, ymin, ymax, yticks, mu_tex, haut_tex, bas_tex, largeur=7.0, entourer=False):
    hors = [(k + 1, m) for k, m in enumerate(ms) if abs(m - mu) > h]
    dans = [(k + 1, m) for k, m in enumerate(ms) if abs(m - mu) <= h]
    n = len(ms)
    yt = ",".join(f"{v}" for v, _ in yticks)
    ytl = ",".join("{$" + t + "$}" for _, t in yticks)
    c_dans = " ".join(f"({k},{m:.4f})" for k, m in dans)
    c_hors = " ".join(f"({k},{m:.4f})" for k, m in hors)
    marques_hors = "otOrange" if not entourer else "otGreenDark"
    entour = ""
    if entourer:
        entour = "\n".join(rf"\draw[otGreenDark, line width=0.8pt] (axis cs:{k},{m:.4f}) circle (4pt);" for k, m in hors)
    xt = ",".join(str(v) for v in range(n // 4, n + 1, n // 4))
    return rf"""\begin{{tikzpicture}}
\begin{{axis}}[otLoi, otBas, width={largeur}cm, height=4.6cm, xmin=0, xmax={n + 4}, ymin={ymin}, ymax={ymax},
  xtick={{{xt}}}, ytick={{{yt}}}, yticklabels={{{ytl}}},
  xlabel={{n° de l’échantillon}}, ylabel={{moyenne $m$}},
  every axis x label/.style={{at={{(current axis.south east)}},anchor=north east,font=\otRegular\fontsize{{9}}{{10}}\selectfont,text=otMuted,yshift=-16pt}}]
\fill[otGreen!16] (axis cs:0,{mu - h:.4f}) rectangle (axis cs:{n + 4},{mu + h:.4f});
\draw[otGreenDark, line width=0.7pt, dash pattern=on 3pt off 2pt] (axis cs:0,{mu - h:.4f}) -- (axis cs:{n + 4},{mu - h:.4f});
\draw[otGreenDark, line width=0.7pt, dash pattern=on 3pt off 2pt] (axis cs:0,{mu + h:.4f}) -- (axis cs:{n + 4},{mu + h:.4f});
\draw[otGreenDark, line width=0.9pt] (axis cs:0,{mu:.4f}) -- (axis cs:{n + 4},{mu:.4f});
\addplot[only marks, mark=*, mark size=1.5pt, otNavy] coordinates {{{c_dans}}};
\addplot[only marks, mark=*, mark size=1.9pt, {marques_hors}] coordinates {{{c_hors}}};
{entour}
\node[anchor=west, legendeV] at (axis cs:{n + 6},{mu + h:.4f}) {{{haut_tex}}};
\node[anchor=west, legendeV] at (axis cs:{n + 6},{mu:.4f}) {{{mu_tex}}};
\node[anchor=west, legendeV] at (axis cs:{n + 6},{mu - h:.4f}) {{{bas_tex}}};
\end{{axis}}
\end{{tikzpicture}}"""


_mu, _s = 1 / 6, math.sqrt(233) / 6
FIGURES["cours_echantillons"] = _nuage(
    moyennes_echantillons_cours(), _mu, 2 * _s / 10, -1.0, 1.3,
    [(-1, "-1"), (-0.5, "-0{,}5"), (0, "0"), (0.5, "0{,}5"), (1, "1")],
    r"$\mu \approx 0{,}17$", r"$\mu + 2\sigma/\sqrt{n}$", r"$\mu - 2\sigma/\sqrt{n}$", largeur=6.2)

_sd = math.sqrt(35 / 12)
for suf, ent in (("", False), ("_corrige", True)):
    FIGURES["n4_echantillons" + suf] = _nuage(
        moyennes_echantillons_de(), 3.5, 2 * _sd / 10, 2.9, 4.15,
        [(3, "3"), (3.25, "3{,}25"), (3.5, "3{,}5"), (3.75, "3{,}75"), (4, "4")],
        r"$3{,}5$", r"$3{,}842$", r"$3{,}158$", largeur=7.0, entourer=ent)
# énoncé : tous les points en bleu (l'élève les compte lui-même)
FIGURES["n4_echantillons"] = FIGURES["n4_echantillons"].replace(
    "mark size=1.9pt, otOrange", "mark size=1.5pt, otNavy")


# ---------------------------------------------------------------- 1335 : somme de deux dés
_SOMME = [(s, s - 1 if s <= 7 else 13 - s) for s in range(2, 13)]
_Y36 = [(k, str(k)) for k in range(1, 7)]
for suf, vide, coul in (("_enonce", True, ""), ("", False, "otGreen!80!black")):
    FIGURES["ex1335_somme" + suf] = batons(
        _SOMME, xmin=1, xmax=13, ymax=7, xticks=list(range(2, 13)), yticks=_Y36,
        couleur=coul, vide=vide, largeur=7.4, hauteur=4.0, epaisseur="7pt", ylabel=r"36 \times P(X = x_i)")

# ---------------------------------------------------------------- 1332 : écart entre deux dés
_ECART = [(k, c) for k, c in zip(range(6), (6, 10, 8, 6, 4, 2))]
_Y36b = [(k, str(k)) for k in (2, 4, 6, 8, 10)]
for suf, vide, coul in (("_enonce", True, ""), ("", False, "otGreen!80!black")):
    FIGURES["ex1332_ecart" + suf] = batons(
        _ECART, xmin=-0.8, xmax=5.8, ymax=11.5, xticks=list(range(6)), yticks=_Y36b,
        couleur=coul, vide=vide, largeur=6.4, hauteur=4.0, xlabel="z_i", ylabel=r"36 \times P(Z = z_i)")


# ---------------------------------------------------------------- nouveau-5 : deux jeux
def _jeu(nom, pts, decal, corrige, e, sigma_tex, s_val, ymax=1.5):
    coords = " ".join(f"({x},{float(p):.6f})" for x, p in pts)
    lab = {x: fr_tex(p) for x, p in pts}
    noeuds = "\n".join(rf"\node[anchor=south, font=\normalsize, inner sep=1.5pt, yshift=1pt] at (axis cs:{x},{float(p):.6f}) {{${lab[x]}$}};"
                       for x, p in pts)
    sup = ""
    if corrige:
        sup = rf"""\draw[otGreenDark, line width=0.9pt, dash pattern=on 4pt off 2.5pt] (axis cs:{e},0) -- (axis cs:{e},1.2);
\draw[otGreenDark, line width=0.9pt, {{Stealth[length=2mm]}}-{{Stealth[length=2mm]}}] (axis cs:{e - s_val:.4f},1.27) -- (axis cs:{e + s_val:.4f},1.27);
\node[anchor=south, legendeV, yshift=1pt] at (axis cs:{e},1.27) {{{sigma_tex}}};"""
    return rf"""\begin{{axis}}[otLoi, at={{({decal}cm,0)}}, width=3.0cm, height=3.9cm, xmin=-3.6, xmax=9, ymax={ymax},
  xtick={{{",".join(str(x) for x, _ in pts)}}}, ytick={{0.5}}, yticklabels={{{{$0{{,}}5$}}}},
  xlabel={{${nom.lower()}_i$}}, ylabel={{$P({nom} = {nom.lower()}_i)$}}]
\addplot[ycomb, line width=8pt, otNavy!60] coordinates {{{coords}}};
{noeuds}
{sup}
\node[anchor=north, legende, yshift=-18pt] at (axis cs:2.7,0) {{Jeu ${nom}$}};
\end{{axis}}"""


_A = [(-1, Fraction(1, 2)), (2, Fraction(1, 2))]
_B = [(-1, Fraction(5, 6)), (8, Fraction(1, 6))]
for suf, corr in (("", False), ("_corrige", True)):
    FIGURES["n5_jeux" + suf] = ("\\begin{tikzpicture}\n"
                                + _jeu("A", _A, 0, corr, 0.5, r"$\sigma(A) = 1{,}5$", 1.5) + "\n"
                                + _jeu("B", _B, 4.75, corr, 0.5, r"$\sigma(B) \approx 3{,}35$", 3.354)
                                + "\n\\end{tikzpicture}")


# ---------------------------------------------------------------- moyennes observées et intervalles 2σ/√n
def _entonnoir(mu, sigma, resultats, ymin, ymax, yticks, mu_tex):
    """resultats : [(n, m)] ; en abscisse log10(n)."""
    yt = ",".join(f"{v}" for v, _ in yticks)
    ytl = ",".join("{$" + t + "$}" for _, t in yticks)
    xs = [math.log10(n) for n, _ in resultats]
    xt = ",".join(f"{x:.4f}" for x in xs)
    xtl = ",".join("{$" + f"{n:,}".replace(",", r"\,") + "$}" for n, _ in resultats)
    barres = []
    for (n, m), x in zip(resultats, xs):
        h = 2 * sigma / math.sqrt(n)
        lo, hi = max(mu - h, ymin), min(mu + h, ymax)
        barres.append(rf"\draw[otGreenDark, line width=2.2pt, opacity=0.55] (axis cs:{x:.4f},{lo:.4f}) -- (axis cs:{x:.4f},{hi:.4f});")
        barres.append(rf"\fill[otNavy] (axis cs:{x:.4f},{m:.4f}) circle (2.4pt);")
    x0, x1 = xs[0] - 0.5, xs[-1] + 0.5
    return rf"""\begin{{tikzpicture}}
\begin{{axis}}[otLoi, otBas, width=6.0cm, height=4.4cm, xmin={x0:.3f}, xmax={x1:.3f}, ymin={ymin}, ymax={ymax},
  xtick={{{xt}}}, xticklabels={{{xtl}}}, ytick={{{yt}}}, yticklabels={{{ytl}}},
  xlabel={{$n$}}, ylabel={{moyenne observée}}]
\draw[otGreenDark, line width=0.9pt, dash pattern=on 4pt off 2.5pt] (axis cs:{x0:.3f},{mu}) -- (axis cs:{x1:.3f},{mu});
{chr(10).join(barres)}
\node[anchor=west, legendeV] at (axis cs:{x1 + 0.05:.3f},{mu}) {{{mu_tex}}};
\end{{axis}}
\end{{tikzpicture}}"""


FIGURES["n3_entonnoir"] = _entonnoir(
    0.6, math.sqrt(3.64), [(10, 1.6), (100, 0.72), (1000, 0.609), (10000, 0.5948)], -0.7, 2.0,
    [(-0.5, "-0{,}5"), (0, "0"), (0.5, "0{,}5"), (1, "1"), (1.5, "1{,}5")], r"$E(X) = 0{,}6$")
FIGURES["ex1340_simulation"] = _entonnoir(
    0.5, math.sqrt(7.75), [(10, 1.6), (100, 0.64), (10000, 0.5036)], -1.5, 2.4,
    [(-1, "-1"), (0, "0"), (0.5, "0{,}5"), (1, "1"), (2, "2")], r"$E(G) = 0{,}5$")
