# -*- coding: utf-8 -*-
r"""Figures de la notion 253 « Sujets type brevet » (3e), style des livres.

Compilation : python outils/figures_livre.py <dossier_notion>

Conventions (partie A : cours, fiche, sujets 01 à 05) :
  - noms : cours_…, fiche_…, brevet_3e_sNN_<objet> (énoncé : données seules)
    et brevet_3e_sNN_<objet>_corrige (corrigé : éléments de réponse en vert) ;
  - bleu marine = données, vert foncé (otGreenDark) = réponses, orange = repère
    d'alerte ou niveau (budget, seuil) ;
  - scripts Scratch : module scratch.py, COPIE (instantané du 03/11/2026) du module
    de la notion 248 (chantier/3e/248_*/figures/scratch.py) — ne pas modifier
    l'original ; les scripts sont décrits une fois (listes SCRIPT_…) et
    exécutés par verif_253.py (scratch.executer) ;
  - toutes les valeurs écrites ici sont recontrôlées par ../verif_253.py.

Aides (réutilisables par la partie B) : pt, lab, lseg, cote_seg, angle_droit, arc,
tri_rect (triangle rectangle avec côtés nommés), arbre / deux_etapes (arbres
pondérés, repris de la notion 243), cylindre (repris de 247), barres, camembert
(repris de 242), graphe (pgfplots, style otWeb).
"""
import math
from fractions import Fraction as Fr

from scratch import *  # noqa: F401,F403  (blocs Scratch : Drapeau, Mettre, Op, V…)
from scratch import PREAMBULE_SCRATCH, figure_scripts, figure_trace, executer

PREAMBULE_EXTRA = PREAMBULE_SCRATCH + r"""
\tikzset{
  lab/.style={text=otInk,inner sep=0pt,align=center},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=1pt,text=otInk},
  petit/.style={font=\otRegular\fontsize{8.5}{10}\selectfont,inner sep=1pt,text=otMuted},
  aide/.style={otMuted,line width=.7pt,dash pattern=on 3.5pt off 2pt},
  % arbres (notion 243)
  evt/.style={font=\normalsize, text=otNavy, inner sep=2.4pt},
  branche/.style={otNavy!65, line width=0.8pt, line cap=round},
  brancheV/.style={otGreenDark, line width=1.6pt, line cap=round},
  poids/.style={font=\small, text=otInk, inner sep=1.7pt},
  poidsV/.style={poids, text=otGreenDark},
  issue/.style={font=\small, text=otMuted, anchor=west, inner sep=1.5pt},
  issueV/.style={issue, text=otGreenDark},
  racine/.style={fill=otNavy},
  titreCol/.style={font=\otRegular\fontsize{8.5}{10}\selectfont, text=otMuted, anchor=south},
  % solides (notion 247)
  solide/.style={otNavy,line width=.9pt,line join=round},
  cache/.style={otNavy,line width=.6pt,dash pattern=on 2.5pt off 2pt},
  face/.style={fill=otSky},
  rayon/.style={otOrange!85!black,line width=.75pt,dash pattern=on 3pt off 2pt},
  hauteur/.style={otOrange!85!black,line width=.75pt,dash pattern=on 3pt off 2pt},
  rep/.style={otGreenDark,line width=1.2pt,line join=round},
  repc/.style={otGreenDark,line width=1pt,dash pattern=on 3pt off 2pt},
  % statistiques (notion 242)
  barre/.style={fill=otNavy!55,draw=otNavy,line width=.6pt},
  barreV/.style={fill=otGreen!60,draw=otGreenDark,line width=.6pt},
  grille/.style={otRule,line width=.35pt},
  axeS/.style={otMuted,line width=.7pt},
  % graphiques
  lecture/.style={otGreenDark,line width=0.8pt,dash pattern=on 2.5pt off 1.8pt},
  niveau/.style={otOrange,line width=0.9pt,dash pattern=on 4pt off 2.5pt},
  courbeB/.style={otOrange!90!black,line width=1.35pt},
  courbeC/.style={otGreen,line width=1.35pt},
}
\pgfplotsset{gm/.style={grid=both, minor grid style={otRule!75,line width=0.35pt}, minor tick length=0pt}}
% premier quadrant : graduations de l'axe des ordonnées centrées sur les traits
\pgfplotsset{Q1/.style={yticklabel style={anchor=east,yshift=0pt,xshift=-1.5pt}}}
\newcommand{\rl}{\otMedium\fontsize{8.5}{10}\selectfont\color{otGreenDark}}
"""

VERT = r"\textcolor{otGreenDark}{%s}"
FIGURES = {}
XLAB = {}
TOLERE = {}


# ============================================================ aides géométriques
def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


def figure(corps, opt="line cap=round"):
    return "\n".join([r"\begin{tikzpicture}[%s]" % opt] + corps + [r"\end{tikzpicture}"])


def pt(p, nom, ang, coul="otNavy", d=.14, txt_coul="otInk"):
    """Point marqué + nom placé dans la direction ang (degrés)."""
    a = math.radians(ang)
    q = (p[0] + d * math.cos(a), p[1] + d * math.sin(a))
    s = [r"\fill[%s] %s circle (2.1pt);" % (coul, P(p))]
    if nom:
        s.append(r"\node[lab,text=%s,anchor=%d] at %s {$%s$};" % (txt_coul, (ang + 180) % 360, P(q), nom))
    return s


def lab(p, txt, ang, d=.13, coul="otInk"):
    a = math.radians(ang)
    q = (p[0] + d * math.cos(a), p[1] + d * math.sin(a))
    return [r"\node[lab,text=%s,anchor=%d] at %s {%s};" % (coul, (ang + 180) % 360, P(q), txt)]


def _ancre(ang):
    noms = ["east", "north east", "north", "north west", "west", "south west", "south", "south east"]
    return noms[int(round(((ang + 180) % 360) / 45)) % 8]


def lseg(p, q, txt, cote=1, t=.5, d=.14, coul="otInk"):
    """Étiquette d'un segment, à côté de son milieu (cote = 1 : à gauche de p→q)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * cote, dx / L * cote
    m = (p[0] + t * dx + d * nx, p[1] + t * dy + d * ny)
    ang = math.degrees(math.atan2(ny, nx))
    return [r"\node[lab,text=%s,anchor=%s] at %s {%s};" % (coul, _ancre(ang), P(m), txt)]


def ext(p, q, r):
    """cote (1 ou -1) qui place une étiquette de [pq] du côté opposé au point r."""
    cr = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return -1 if cr > 0 else 1


def cote_seg(p, q, txt, d=.55, coul="otMuted", txt_coul="otInk", cote_a_cote=False):
    """Flèche de cote parallèle à [pq], décalée de d (d > 0 : à gauche de p→q), avec
    traits de rappel ; texte sur fond blanc au milieu (cote : fond blanc permis), ou
    écrit à côté de la flèche, à l'extérieur (cote_a_cote=True)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    a = (p[0] + d * nx, p[1] + d * ny)
    b = (q[0] + d * nx, q[1] + d * ny)
    e = .1 if d > 0 else -.1
    return [r"\draw[%s!70,line width=.4pt] %s -- %s %s -- %s;"
            % (coul, P((p[0] + .08 * nx * (1 if d > 0 else -1), p[1] + .08 * ny * (1 if d > 0 else -1))),
               P((a[0] + e * nx, a[1] + e * ny)),
               P((q[0] + .08 * nx * (1 if d > 0 else -1), q[1] + .08 * ny * (1 if d > 0 else -1))),
               P((b[0] + e * nx, b[1] + e * ny))),
            r"\draw[cote] %s -- %s node[midway,coteTexte,text=%s] {%s};" % (P(a), P(b), txt_coul, txt)
            if not cote_a_cote else
            r"\draw[cote] %s -- %s node[midway,lab,text=%s,anchor=%s] {%s};"
            % (P(a), P(b), txt_coul, _ancre(math.degrees(math.atan2(ny, nx)) + (0 if d > 0 else 180)), txt)]


def angle_droit(p, sommet, q, coul="otNavy", r=.22):
    def u(a, b):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        return ((b[0] - a[0]) / L * r, (b[1] - a[1]) / L * r)
    a, b = u(sommet, p), u(sommet, q)
    p1 = (sommet[0] + a[0], sommet[1] + a[1])
    p2 = (sommet[0] + a[0] + b[0], sommet[1] + a[1] + b[1])
    p3 = (sommet[0] + b[0], sommet[1] + b[1])
    return [r"\draw[%s,line width=.6pt] %s -- %s -- %s;" % (coul, P(p1), P(p2), P(p3))]


def arc(S, p, q, txt=None, coul="otNavy", r=.55, dl=None, txt_coul=None):
    """Arc de l'angle de sommet S entre S→p et S→q ; mesure écrite dans l'angle."""
    a1 = math.degrees(math.atan2(p[1] - S[1], p[0] - S[0]))
    a2 = math.degrees(math.atan2(q[1] - S[1], q[0] - S[0]))
    dlt = (a2 - a1) % 360
    if dlt > 180:
        a1, dlt = a2, 360 - dlt
    d0 = (S[0] + r * math.cos(math.radians(a1)), S[1] + r * math.sin(math.radians(a1)))
    s = [r"\draw[%s,line width=.85pt] %s arc[start angle=%s, delta angle=%s, radius=%s];"
         % (coul, P(d0), f(a1), f(dlt), f(r))]
    if txt:
        mid = math.radians(a1 + dlt / 2)
        half = math.radians(dlt / 2)
        d = dl or max(r + .34, .36 / math.sin(half))
        m = (S[0] + d * math.cos(mid), S[1] + d * math.sin(mid))
        s.append(r"\node[lab,text=%s] at %s {%s};" % (txt_coul or ("otInk" if coul == "otNavy" else coul), P(m), txt))
    return s


# ============================================================ arbres (notion 243)
def frac(x):
    x = Fr(x)
    return str(x.numerator) if x.denominator == 1 else rf"\dfrac{{{x.numerator}}}{{{x.denominator}}}"


def N(nom, p=None, *enfants, donne=True, vert=False, droite=None):
    return {"nom": nom, "p": p, "enfants": list(enfants), "donne": donne, "vert": vert, "droite": droite}


def _vert(n):
    if not n["enfants"]:
        return n["vert"]
    n["vert"] = n["vert"] or any([_vert(c) for c in n["enfants"]])
    return n["vert"]


def _placer(n, prof, y, dy, ecarts, L):
    n["x"] = prof * L
    if not n["enfants"]:
        n["y"] = y
        return y - dy
    ys = []
    for k, c in enumerate(n["enfants"]):
        if k and c["enfants"]:
            y -= ecarts.get(prof + 1, 0)
        y = _placer(c, prof + 1, y, dy, ecarts, L)
        ys.append(c["y"])
    n["y"] = (ys[0] + ys[-1]) / 2
    return y


def _tous_y(n):
    ys = [n["y"]]
    for c in n["enfants"]:
        ys += _tous_y(c)
    return ys


def arbre(enfants, mode="corrige", L=2.2, dy=0.95, ecarts=None, titres=None, produits=True):
    """mode « enonce » : poids inconnus « … » ; « corrige » : poids trouvés en vert,
    chemins demandés en vert épais, issues et probabilités à droite."""
    racine = {"nom": None, "p": None, "enfants": enfants, "droite": None, "vert": False, "donne": True}
    if mode == "corrige":
        _vert(racine)
    _placer(racine, 0, 0.0, dy, ecarts or {}, L)
    noeuds, aretes, poids, droites = [], [], [], []
    k = [0]

    def visiter(n, parent_ref, parent_y, prod):
        for c in n["enfants"]:
            k[0] += 1
            nom = f"n{k[0]}"
            v = mode == "corrige" and c["vert"]
            noeuds.append(rf"\node[{'evt,text=otGreenDark' if v else 'evt'}] ({nom}) at ({c['x']:.3f},{c['y']:.3f}) {{{c['nom']}}};")
            st = "brancheV" if v else "branche"
            aretes.append((st, rf"\draw[{st}] {parent_ref} -- ({nom}.west);"))
            pr = None
            if c["p"] is not None:
                ecart = c["y"] - parent_y
                anc = "south east" if ecart > 1e-6 else ("north east" if ecart < -1e-6 else "south")
                if mode == "enonce" and not c["donne"]:
                    t, sp = r"\ldots", "poids"
                else:
                    t = frac(c["p"])
                    sp = "poidsV" if (mode == "corrige" and not c["donne"]) else "poids"
                poids.append(rf"\path {parent_ref} -- ({nom}.west) node[{sp},pos=0.5,anchor={anc}] {{${t}$}};")
                pr = prod * c["p"] if prod is not None else None
            if not c["enfants"] and mode == "corrige":
                txt = c["droite"] or ""
                if produits and pr is not None:
                    txt = (txt + r"\quad " if txt else "") + "$" + frac(pr) + "$"
                if txt:
                    si = "issueV" if c["vert"] else "issue"
                    droites.append(rf"\node[{si}] at ([xshift=4pt]{nom}.east) {{{txt}}};")
            visiter(c, f"({nom}.east)", c["y"], pr)

    lignes = [r"\begin{tikzpicture}[x=1cm,y=1cm]", rf"\coordinate (r) at (0,{racine['y']:.3f});"]
    visiter(racine, "(r)", racine["y"], Fr(1))
    lignes += noeuds
    lignes += [a for s, a in aretes if s == "branche"] + [a for s, a in aretes if s == "brancheV"]
    lignes.append(r"\fill[racine] (r) circle (1.9pt);")
    lignes += poids + droites
    if titres:
        haut = max(_tous_y(racine)) + 0.45
        for i, t in enumerate(titres, start=1):
            lignes.append(rf"\node[titreCol] at ({i * L:.3f},{haut:.3f}) {{{t}}};")
    lignes.append(r"\end{tikzpicture}")
    return "\n".join(lignes)


def deux_etapes(e1, e2, p1, p2, donnes, verts, noms=None, issue=None):
    """e1, e2 : issues de chaque étape ; p1[a] ; p2[a][b] (Fractions) ; donnes : poids
    donnés (('1', a) ou ('2', a, b)) ; verts : chemins (a, b) en vert au corrigé ;
    noms : texte LaTeX affiché pour chaque issue ; issue(a, b) : texte de l'issue."""
    noms = noms or {}
    res = []
    for a in e1:
        enf = []
        for b in e2:
            enf.append(N(noms.get(b, "$%s$" % b), p2[a][b], donne=("2", a, b) in donnes, vert=(a, b) in verts,
                         droite=(issue(a, b) if issue else "$%s%s$" % (a, b))))
        res.append(N(noms.get(a, "$%s$" % a), p1[a], *enf, donne=("1", a) in donnes))
    return res


T2 = [r"1\textsuperscript{er} tirage", r"2\textsuperscript{e} tirage"]


# ============================================================ triangle rectangle (notion 245)
ROLE = {"hyp": "hypoténuse", "adj": "côté adjacent", "opp": "côté opposé"}


def tri_rect(noms, adj, opp, U, cotes=None, vert=(), roles=False, traits=(), miroir=False,
             marque=True, ang_txt=None, ang_vert=False, arc_r=.55):
    """Triangle rectangle : noms = (sommet de l'angle marqué, sommet de l'angle droit, troisième) ;
    côté adjacent horizontal, côté opposé vertical. cotes : {"adj"|"opp"|"hyp": texte} ;
    vert : clés écrites en vert ; roles : nom du côté (en vert) ; traits : côtés en vert."""
    sg = -1 if miroir else 1
    pts = [(0, 0), (sg * adj * U, 0), (sg * adj * U, opp * U)]
    idx = {"adj": (0, 1), "opp": (1, 2), "hyp": (0, 2)}
    cotes = cotes or {}
    G = (sum(p[0] for p in pts) / 3, sum(p[1] for p in pts) / 3)
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(pts[0]), P(pts[1]), P(pts[2])),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(pts[0]), P(pts[1]), P(pts[2]))]
    for k in traits:
        i, j = idx[k]
        s.append(r"\draw[geoReponse,line width=1.5pt] %s -- %s;" % (P(pts[i]), P(pts[j])))
    s += angle_droit(pts[0], pts[1], pts[2])
    if marque:
        s += arc(pts[0], pts[1], pts[2], (VERT % ang_txt) if (ang_txt and ang_vert) else ang_txt,
                 "otGreenDark" if ang_vert else "otNavy", r=arc_r)
    for k in ("adj", "opp", "hyp"):
        txt = cotes.get(k)
        if txt is not None and k in vert:
            txt = VERT % txt
        if roles and k in roles:
            rl = r"{\rl %s}" % ROLE[k]
            txt = (txt + r"\\" + rl) if txt else rl
        if txt:
            i, j = idx[k]
            c = ext(pts[i], pts[j], pts[3 - i - j])
            s += lseg(pts[i], pts[j], txt, c)
    for k in range(3):
        a = math.degrees(math.atan2(pts[k][1] - G[1], pts[k][0] - G[0]))
        s += pt(pts[k], noms[k], a)
    return s


# ============================================================ cylindre (notion 247)
def cylindre(xc, r, h, lr, lh, y0=0.0, cote=True, eau=None, eau_txt=None):
    ry = 0.32 * r
    a, b = y0, y0 + h
    L = [rf"\fill[face] ({f(xc-r)},{f(a)}) -- ({f(xc-r)},{f(b)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- ({f(xc+r)},{f(a)}) arc[start angle=0,end angle=-180,x radius={f(r)},y radius={f(ry)}] -- cycle;"]
    if eau is not None:   # hauteur d'eau (corrigé)
        e = a + eau
        L += [rf"\fill[otGreen!35] ({f(xc-r)},{f(a)}) -- ({f(xc-r)},{f(e)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- ({f(xc+r)},{f(a)}) arc[start angle=0,end angle=-180,x radius={f(r)},y radius={f(ry)}] -- cycle;",
              rf"\fill[otGreen!20] ({f(xc)},{f(e)}) ellipse[x radius={f(r)},y radius={f(ry)}];",
              rf"\draw[otGreenDark,line width=.8pt] ({f(xc)},{f(e)}) ellipse[x radius={f(r)},y radius={f(ry)}];"]
    L += [rf"\fill[otSky!60!white] ({f(xc)},{f(b)}) ellipse[x radius={f(r)},y radius={f(ry)}];",
          rf"\draw[solide] ({f(xc)},{f(b)}) ellipse[x radius={f(r)},y radius={f(ry)}];",
          rf"\draw[solide] ({f(xc-r)},{f(b)}) -- ({f(xc-r)},{f(a)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- ({f(xc+r)},{f(b)});",
          rf"\draw[cache] ({f(xc+r)},{f(a)}) arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(ry)}];"]
    if lr:
        L += [rf"\draw[rayon] ({f(xc)},{f(b)}) -- ({f(xc+r)},{f(b)});",
              rf"\fill[otNavy] ({f(xc)},{f(b)}) circle (1.6pt);",
              rf"\node[anchor=south,text=otInk] at ({f(xc+r/2)},{f(b+ry+0.05)}) {{{lr}}};"]
    if lh and cote:
        L += [rf"\draw[cote] ({f(xc+r+0.32)},{f(a)}) -- ({f(xc+r+0.32)},{f(b)});",
              rf"\node[anchor=west,text=otInk] at ({f(xc+r+0.4)},{f((a+b)/2)}) {{{lh}}};"]
    if eau is not None and eau_txt:
        L += [rf"\draw[cote,otGreenDark] ({f(xc-r-0.32)},{f(a)}) -- ({f(xc-r-0.32)},{f(a+eau)});",
              rf"\node[anchor=east,text=otGreenDark] at ({f(xc-r-0.4)},{f(a+eau/2)}) {{{eau_txt}}};"]
    return L


# ============================================================ graphiques (pgfplots)
def graphe(opts, corps):
    return (r"\begin{tikzpicture}" + "\n" + r"\begin{axis}[otWeb, " + opts + "]\n" + corps
            + "\n\\end{axis}\n\\end{tikzpicture}")


# ============================================================ statistiques (notion 242)
def barres(etiq, hauteurs, ymax, pas, unite=.32, dx=1.1, larg=.22, titre_y="", valeurs=False, vert=(),
           pas_lab=None):
    s = []
    n = len(etiq)
    W = (n + .2) * dx
    H = ymax * unite
    pas_lab = pas_lab or pas
    k = 0
    while k <= ymax:
        y = k * unite
        if k > 0:
            s.append(r"\draw[grille] (0,%.3f) -- (%.3f,%.3f);" % (y, W, y))
        s.append(r"\draw[axeS] (-.08,%.3f) -- (0,%.3f);" % (y, y))
        if k % pas_lab == 0:
            s.append(r"\node[petit,anchor=east] at (-.12,%.3f) {%s};" % (y, nombre_tex(k)))
        k += pas
    for i, (e, h) in enumerate(zip(etiq, hauteurs)):
        x = (i + .7) * dx
        st = "barreV" if i in vert else "barre"
        s.append(r"\draw[%s] (%.3f,0) rectangle (%.3f,%.3f);" % (st, x - larg, x + larg, h * unite))
        s.append(r"\node[txt,anchor=north] at (%.3f,-.12) {%s};" % (x, e))
        if valeurs:
            c = "otGreenDark" if i in vert else "otInk"
            s.append(r"\node[txt,anchor=south,text=%s] at (%.3f,%.3f) {%s};" % (c, x, h * unite + .06, nombre_tex(h)))
    s.append(r"\draw[axeS] (0,0) -- (%.3f,0);" % W)
    s.append(r"\draw[axeS,-{Stealth[length=2mm]}] (0,0) -- (0,%.3f);" % (H + .35))
    if titre_y:
        s.append(r"\node[petit,anchor=south west] at (.1,%.3f) {%s};" % (H + .3, titre_y))
    return s, W


def nombre_tex(v):
    r"""6800 -> 6\,800 ; 2.5 -> 2{,}5 (texte de figure)."""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    if isinstance(v, int):
        s = str(abs(v))
        g = []
        while s:
            g.insert(0, s[-3:])
            s = s[:-3]
        return ("-" if v < 0 else "") + r"\,".join(g)
    return str(v).replace(".", "{,}")


def camembert(parts, r=1.7, vert=()):
    """parts : liste (étiquette, angle en degrés, texte de l'angle) ; vert : indices en vert."""
    cols = ["otNavy!45", "otOrange!55", "otSky!70!otNavy!30", "otMuted!35"]
    s = []
    a = 90
    for i, (lab_, ang, txt) in enumerate(parts):
        b = a - ang
        c = "otGreen!60" if i in vert else cols[i % 4]
        s.append(r"\fill[%s] (0,0) -- (%.3f:%.2f) arc[start angle=%.3f,end angle=%.3f,radius=%.2f] -- cycle;"
                 % (c, a, r, a, b, r))
        a = b
    a = 90
    for i, (lab_, ang, txt) in enumerate(parts):
        s.append(r"\draw[white,line width=1.2pt] (0,0) -- (%.3f:%.2f);" % (a, r))
        a -= ang
    s.append(r"\draw[otNavy,line width=.8pt] (0,0) circle (%.2f);" % r)
    a = 90
    for i, (lab_, ang, txt) in enumerate(parts):
        m = a - ang / 2
        c = "otGreenDark" if i in vert else "otInk"
        lab2 = r"\textcolor{%s}{%s}" % (c, lab_) + (r" : \textcolor{%s}{%s}" % (c, txt) if txt else "")
        s.append(r"\node[txt,anchor=%s] at (%.3f:%.2f) {%s};" % (_ancre_cam(m), m, r + .15, lab2))
        a -= ang
    return s


def _ancre_cam(m):
    m = m % 360
    if 80 <= m < 100:
        return "south"
    if 260 <= m < 280:
        return "north"
    if m < 10 or m >= 350:
        return "west"
    if 170 <= m < 190:
        return "east"
    if m < 90:
        return "south west"
    if m < 180:
        return "south east"
    if m < 270:
        return "north east"
    return "north west"


# ######################################################################
#                              SUJET 01
# ######################################################################
# ---- Partie 1, question 9 : triangle RST rectangle en S, angle en R
FIGURES["brevet_3e_s01_cos"] = figure(tri_rect("RST", 3.4, 2.3, 1.0))
FIGURES["brevet_3e_s01_cos_corrige"] = figure(
    tri_rect("RST", 3.4, 2.3, 1.0, cotes={"adj": "", "hyp": "", "opp": ""}, roles=("adj", "hyp"),
             traits=("adj", "hyp")))

# ---- Exercice 2 : la voile (unité : 1 m = 0,4 cm)
U1 = .4
VA, VB, VC = (0, 0), (12 * U1, 0), (0, 9 * U1)
VM, VN = (4 * U1, 0), (0, 3 * U1)


def voile(corrige):
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(VA), P(VB), P(VC))]
    if corrige:
        s.append(r"\fill[otGreen!18] %s -- %s -- %s -- %s -- cycle;" % (P(VM), P(VB), P(VC), P(VN)))
    s += [r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(VA), P(VB), P(VC)),
          r"\draw[%s] %s -- %s;" % ("geoReponse,line width=1.4pt" if corrige else "geoTrait", P(VM), P(VN))]
    s += angle_droit(VB, VA, VC)
    s += pt(VA, "A", 225) + pt(VB, "B", -30) + pt(VC, "C", 90) + pt(VM, "M", 60, d=.12) + pt(VN, "N", 30, d=.12)
    s += lseg(VA, VM, "$4$ m", -1, d=.12)
    s += cote_seg(VA, VB, "$12$ m", d=-.8)
    if corrige:
        s += lseg(VA, VN, VERT % "$3$ m", 1, d=.12)
        s += cote_seg(VA, VC, "$9$ m", d=.95)
        s += lseg(VM, VN, VERT % "$5$ m", -1, d=.12)
        s += lseg(VB, VC, VERT % "$15$ m", -1, d=.14)
    else:
        s += cote_seg(VA, VC, "$9$ m", d=.6)
    return figure(s)


FIGURES["brevet_3e_s01_voile"] = voile(False)
FIGURES["brevet_3e_s01_voile_corrige"] = voile(True)

# ---- Exercice 3 : deux loueurs (A : 18 + 7n ; B : 10n)
LOUEURS = (r"width=6.4cm, height=5.6cm, xmin=0, xmax=15.8, ymin=0, ymax=172, gm, Q1, "
           r"xtick={0,1,...,15}, minor ytick={10,30,...,150}, ytick={20,40,...,160}, "
           r"yticklabels={20,40,60,80,100,120,140,160}, "
           r"xticklabels={,,2,,4,,6,,8,,10,,12,,14,}, "
           r"xlabel={jours}, ylabel={prix (\texteuro)}, "
           r"every axis y label/.style={at={(current axis.above origin)},anchor=south west,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}, "
           r"every axis x label/.style={at={(current axis.right of origin)},anchor=north east,yshift=-14pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}")


def loueurs(corrige):
    c = [r"\addplot[courbe, domain=0:15] {18+7*x};",
         r"\addplot[courbeB, domain=0:15] {10*x};",
         r"\node[etiq,text=otNavy,anchor=north west] at (axis cs:14.1,113) {A};",
         r"\node[etiq,text=otOrange!90!black,anchor=south east] at (axis cs:13.9,141) {B};"]
    if corrige:
        c += [r"\draw[niveau] (axis cs:0,90) -- (axis cs:15.4,90);",
              r"\node[note,text=otOrange!90!black,anchor=south west] at (axis cs:0.25,92) {budget 90 €};",
              r"\draw[lecture] (axis cs:6,0) -- (axis cs:6,60) -- (axis cs:0,60);",
              r"\draw[lecture] (axis cs:9,0) -- (axis cs:9,90);",
              r"\draw[lecture] (axis cs:%.4f,0) -- (axis cs:%.4f,90);" % (72 / 7, 72 / 7),
              r"\pnt[otGreenDark]{6}{60} \pnt[otGreenDark]{9}{90} \pnt[otGreenDark]{%.4f}{90}" % (72 / 7),
              r"\node[note,text=otGreenDark,anchor=north west] at (axis cs:6.25,57) {$(6\ ;\ 60)$};"]
    return graphe(LOUEURS, "\n".join(c))


FIGURES["brevet_3e_s01_loueurs"] = loueurs(False)
FIGURES["brevet_3e_s01_loueurs_corrige"] = loueurs(True)

# ---- Exercice 4 : tirage avec remise, 3 R et 1 B
P1_S01 = {"R": Fr(3, 4), "B": Fr(1, 4)}
P2_S01 = {a: dict(P1_S01) for a in "RB"}
FIGURES["brevet_3e_s01_arbre"] = arbre(deux_etapes("RB", "RB", P1_S01, P2_S01, set(), set()), "enonce",
                                       ecarts={1: 0.3}, titres=T2)
FIGURES["brevet_3e_s01_arbre_corrige"] = arbre(deux_etapes("RB", "RB", P1_S01, P2_S01, set(), {("R", "B"), ("B", "R")}),
                                               "corrige", ecarts={1: 0.3}, titres=T2)


# ######################################################################
#                              SUJET 02
# ######################################################################
# ---- Exercice 1 : l'abri (triangle ABC rectangle en A, angle marqué en B)
def abri(corrige):
    s = tri_rect("BAC", 4, 2.5, 1.15, miroir=True,
                 cotes={"adj": "$4$ m", "opp": "$2{,}5$ m", "hyp": r"$\approx 4{,}72$ m" if corrige else None},
                 vert=("hyp",), ang_txt=r"$\approx 32^\circ$" if corrige else None, ang_vert=corrige, arc_r=.7)
    return figure(s)


FIGURES["brevet_3e_s02_abri"] = abri(False)
FIGURES["brevet_3e_s02_abri_corrige"] = abri(True)

# ---- Exercice 2 : la bouteille (r = 4 cm, h = 20 cm) et sa version « mini » (× 0,75)
FIGURES["brevet_3e_s02_bouteille"] = figure(cylindre(0, .8, 4.0, "$4$ cm", "$20$ cm"))
FIGURES["brevet_3e_s02_bouteille_corrige"] = figure(
    cylindre(0, .8, 4.0, "$4$ cm", "$20$ cm")
    + cylindre(3.3, .6, 3.0, VERT % "$3$ cm", VERT % "$15$ cm")
    + [r"\node[txt,text=otNavy,anchor=north] at (0,-.42) {bouteille};",
       r"\node[txt,text=otGreenDark,anchor=north] at (3.3,-.42) {version « mini »};"])

# ---- Exercice 3 : script de carrés (Scratch) et tracé du lutin
DEF_S02 = [Definir("carré", ["côté"]), Repeter(4, [Avancer(Param("côté")), TournerG(90)])]
MAIN_S02 = [Drapeau(), EffacerTout(), AllerA(0, 0), Orienter(90), StyloBas(), Mettre("c", 10),
            Repeter(4, [Appel("carré", [V("c")]), StyloHaut(), Avancer(Op(V("c"), "+", 5)), StyloBas(),
                        Ajouter("c", 5)])]
TEXTE_BLOC = ("textes blancs écrits sur le fond coloré des blocs Scratch : aucun trait sous le texte "
              "(contrôlé par controle_scratch.py sur une version à fonds blancs, comme dans la notion 248)")


def scripts_fig(nom, scripts, corrige=False, **kw):
    FIGURES[nom] = figure_scripts(scripts, corrige=corrige, **kw)
    TOLERE[nom] = TEXTE_BLOC


scripts_fig("brevet_3e_s02_script", [("Bloc personnalisé", DEF_S02), ("Script principal", MAIN_S02)])
R_S02 = executer({"Lutin": [DEF_S02, MAIN_S02]})
_l = R_S02.lutins["lutin"]
FIGURES["brevet_3e_s02_trace"] = figure_trace(
    _l.segments, (-5, 95, -5, 30), 5, .06, depart=(0, 0), fleche=(_l.x, _l.y, _l.direction), pas_lab=20,
    points=[(_l.x, _l.y, r"$(90\ ;\ 0)$", "north west")])

# ---- Exercice 4 : roue (3 secteurs A, 1 secteur B) et arbre
def roue_lettres(lettres, R=1.2):
    n = len(lettres)
    L = []
    for k, let in enumerate(lettres):
        a = 90 - k * 360 / n
        b = a - 360 / n
        fond = "otSky" if let == "A" else "otOrange!25"
        L.append(r"\fill[%s] (0,0) -- (%.2f:%.2f) arc[start angle=%.2f,end angle=%.2f,radius=%.2f] -- cycle;" % (fond, a, R, a, b, R))
        L.append(r"\draw[otNavy,line width=.8pt] (0,0) -- (%.2f:%.2f);" % (a, R))
        L.append(r"\node[text=otNavy,font=\otMedium\fontsize{12}{14}\selectfont] at (%.2f:%.2f) {%s};" % ((a + b) / 2, .6 * R, let))
    L.append(r"\draw[otNavy,line width=1pt] (0,0) circle (%.2f);" % R)
    L.append(r"\fill[otNavy] (0,0) circle (1.6pt);")
    L.append(r"\fill[otOrange] (%.2f,%.2f) -- (%.2f,%.2f) -- (%.2f,%.2f) -- cycle;" % (R + .05, 0, R + .38, .17, R + .38, -.17))
    return figure(L)


FIGURES["brevet_3e_s02_roue"] = roue_lettres("AABA")
P1_S02 = {"A": Fr(3, 4), "B": Fr(1, 4)}
P2_S02 = {a: {"r": Fr(1, 2), "b": Fr(1, 2)} for a in "AB"}
NOMS_S02 = {"A": "A", "B": "B", "r": "rouge", "b": "bleue"}
TITRES_S02 = ["roue", "boule"]


def _issue_s02(a, b):
    return "%s et %s" % (a, NOMS_S02[b])


FIGURES["brevet_3e_s02_arbre"] = arbre(deux_etapes("AB", "rb", P1_S02, P2_S02, set(), set(), NOMS_S02, _issue_s02),
                                       "enonce", L=2.0, ecarts={1: 0.3}, titres=TITRES_S02)
FIGURES["brevet_3e_s02_arbre_corrige"] = arbre(
    deux_etapes("AB", "rb", P1_S02, P2_S02, set(), {("A", "r"), ("B", "b")}, NOMS_S02, _issue_s02),
    "corrige", L=2.0, ecarts={1: 0.3}, titres=TITRES_S02)


# ######################################################################
#                              SUJET 03
# ######################################################################
# ---- Partie 1, question 10 : symétrie centrale (triangle 1 -> triangle 2)
T1_S03 = [(-4, 1), (-1, 1), (-1, 3)]
T2_S03 = [(-x, -y) for x, y in T1_S03]


def symetrie(corrige, u=.45):
    s = []
    for x in range(-5, 6):
        s.append(r"\draw[otRule,line width=.35pt] (%s,%s) -- (%s,%s);" % (f(x * u), f(-4 * u), f(x * u), f(4 * u)))
    for y in range(-4, 5):
        s.append(r"\draw[otRule,line width=.35pt] (%s,%s) -- (%s,%s);" % (f(-5 * u), f(y * u), f(5 * u), f(y * u)))

    def poly(T, style):
        return r"\draw[%s] %s -- cycle;" % (style, " -- ".join(P((x * u, y * u)) for x, y in T))
    s.append(r"\draw[otOrange!85!black,line width=.9pt,dash pattern=on 4pt off 2.5pt] (%s,%s) -- (%s,%s);"
             % (f(2 * u), f(-4 * u), f(2 * u), f(4 * u)))
    s.append(r"\node[lab,text=otOrange!85!black,anchor=south west] at (%s,%s) {$(d)$};" % (f(2.1 * u), f(3.05 * u)))
    s.append(r"\fill[otSky] %s -- cycle;" % " -- ".join(P((x * u, y * u)) for x, y in T1_S03))
    s.append(poly(T1_S03, "geoTrait"))
    s.append(r"\fill[%s] %s -- cycle;" % ("otGreen!25" if corrige else "otSky", " -- ".join(P((x * u, y * u)) for x, y in T2_S03)))
    s.append(poly(T2_S03, "geoReponse,line width=1.2pt" if corrige else "geoTrait"))
    if corrige:
        for (x, y), (x2, y2) in zip(T1_S03, T2_S03):
            s.append(r"\draw[lecture] (%s,%s) -- (%s,%s);" % (f(x * u), f(y * u), f(x2 * u), f(y2 * u)))
    s.append(r"\fill[otNavy] (0,0) circle (2.1pt);")
    s.append(r"\node[lab,anchor=north west,fill=white,inner sep=1pt] at (.06,-.06) {$O$};")
    rond = r"\node[circle,draw=%s,line width=.7pt,inner sep=1.2pt,fill=white,text=%s,font=\otMedium\fontsize{9}{10}\selectfont] at (%s,%s) {%s};"
    s.append(rond % ("otNavy", "otNavy", f(-2.85 * u), f(2.55 * u), "1"))
    c2 = "otGreenDark" if corrige else "otNavy"
    s.append(rond % (c2, c2, f(2.85 * u), f(-2.55 * u), "2"))
    return figure(s)


FIGURES["brevet_3e_s03_symetrie"] = symetrie(False)
FIGURES["brevet_3e_s03_symetrie_corrige"] = symetrie(True)
TOLERE["brevet_3e_s03_symetrie"] = "pastilles 1 et 2 et nom de O sur fond blanc posés sur le quadrillage clair (pas sur un trait de la figure)"
TOLERE["brevet_3e_s03_symetrie_corrige"] = TOLERE["brevet_3e_s03_symetrie"]

# ---- Exercice 2 : le trajet en car
TRAJET = (r"width=6.4cm, height=5.6cm, xmin=0, xmax=4.7, ymin=0, ymax=335, gm, Q1, "
          r"xtick={0.5,1,...,4.5}, xticklabels={0{,}5,1,1{,}5,2,2{,}5,3,3{,}5,4,4{,}5}, "
          r"ytick={40,80,...,320}, yticklabels={40,80,120,160,200,240,280,320}, minor ytick={20,60,...,300}, "
          r"xlabel={durée (h)}, ylabel={distance (km)}, "
          r"every axis y label/.style={at={(current axis.above origin)},anchor=south west,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}, "
          r"every axis x label/.style={at={(current axis.right of origin)},anchor=north east,yshift=-14pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}")


def trajet(corrige):
    c = [r"\addplot[courbe] coordinates {(0,0) (2,180) (2.5,180) (4,300)};"]
    if corrige:
        c += [r"\draw[lecture] (axis cs:2,0) -- (axis cs:2,180) -- (axis cs:0,180);",
              r"\draw[lecture] (axis cs:4,0) -- (axis cs:4,300) -- (axis cs:0,300);",
              r"\draw[otGreenDark,line width=3pt,opacity=.85] (axis cs:2,180) -- (axis cs:2.5,180);",
              r"\node[note,text=otGreenDark,anchor=south] at (axis cs:2.25,186) {pause};",
              r"\pnt[otGreenDark]{2}{180} \pnt[otGreenDark]{4}{300}",
              r"\node[note,text=otGreenDark,anchor=south west] at (axis cs:0.08,184) {$180$ km};",
              r"\node[note,text=otGreenDark,anchor=south west] at (axis cs:1.1,303) {$300$ km};"]
    return graphe(TRAJET, "\n".join(c))


FIGURES["brevet_3e_s03_trajet"] = trajet(False)
FIGURES["brevet_3e_s03_trajet_corrige"] = trajet(True)

# ---- Exercice 3 : la statue (Thalès) ; figure « pas à l'échelle » : la zone du bâton est
#      élargie pour laisser la place aux étiquettes (H reste sur le rayon [OT]).
SS, SO_, ST_ = (0, 0), (6.2, 0), (0, 4.0)
SB = (3.6, 0)
SH = (3.6, 4.0 * (6.2 - 3.6) / 6.2)


def statue(corrige):
    s = [r"\draw[otMuted,line width=.7pt] (%s,0) -- (%s,0);" % (f(-.5), f(SO_[0] + .5))]
    # rayon de soleil prolongé au-delà de T
    d = (ST_[0] - SO_[0], ST_[1] - SO_[1])
    k = 1.1
    s.append(r"\draw[otOrange!85!black,line width=.8pt,dash pattern=on 4pt off 2.5pt] %s -- %s;"
             % (P(SO_), P((SO_[0] + k * d[0], SO_[1] + k * d[1]))))
    s.append(r"\draw[otNavy,line width=2.2pt] %s -- %s;" % (P(SS), P(ST_)))
    s.append(r"\draw[otNavy,line width=1.5pt] %s -- %s;" % (P(SB), P(SH)))
    s += angle_droit(SO_, SS, ST_) + angle_droit(SO_, SB, SH, r=.18)
    s += pt(SS, "S", 225) + pt(ST_, "T", 165) + pt(SB, "B", -140, d=.14) + pt(SO_, "O", -40) + pt(SH, "H", 60, d=.12)
    s += lseg(SB, SH, "$1{,}5$ m", 1, d=.1)
    s += cote_seg(SB, SO_, "$2$ m", d=-.55)
    s += cote_seg(SS, SO_, "$9{,}6$ m", d=-1.1)
    if corrige:
        s += lseg(SS, ST_, VERT % "$7{,}2$ m", 1, d=.14)
        s += lseg(SO_, ST_, VERT % "$12$ m", -1, t=.6, d=.16)
        s += arc(SO_, SS, ST_, VERT % r"$\approx 37^\circ$", "otGreenDark", r=.6, dl=1.3)
    return figure(s)


FIGURES["brevet_3e_s03_statue"] = statue(False)
FIGURES["brevet_3e_s03_statue_corrige"] = statue(True)

# ---- Exercice 4 : diagramme circulaire (corrigé)
ACT_S03 = [("Musée", 18), ("Parc", 12), ("Spectacle", 10), ("Plage", 8)]
FIGURES["brevet_3e_s03_activites_corrige"] = figure(camembert(
    [(n, e * 360 / 48, "%d°" % (e * 360 // 48)) for n, e in ACT_S03], r=1.5, vert=(0,)))


# ######################################################################
#                              SUJET 04
# ######################################################################
# ---- Exercice 1 : le jardin, unité 1 m = 0,42 cm
U4 = .42
JA, JB, JC, JD = (0, 0), (12 * U4, 0), (12 * U4, 9 * U4), (0, 9 * U4)
JE = (6 * U4, 9 * U4)


def jardin(corrige):
    s = [r"\fill[otGreen!14] %s rectangle %s;" % (P(JA), P(JC)),
         r"\fill[otOrange!30] %s -- %s -- %s -- cycle;" % (P(JA), P(JD), P(JE)),
         r"\draw[geoTrait] %s rectangle %s;" % (P(JA), P(JC)),
         r"\draw[geoTrait] %s -- %s;" % (P(JA), P(JE)),
         r"\draw[%s] %s -- %s;" % ("otGreenDark,line width=1.3pt,dash pattern=on 4pt off 2.5pt" if corrige
                                   else "otMuted,line width=1pt,dash pattern=on 4pt off 2.5pt", P(JA), P(JC))]
    s += angle_droit(JB, JA, JD) + angle_droit(JA, JB, JC) + angle_droit(JB, JC, JD) + angle_droit(JC, JD, JA)
    s.append(r"\path[postaction={decorate,decoration={markings,mark=at position 0.5 with {\draw[otNavy,line width=.7pt] (0,-3.2pt) -- (0,3.2pt);}}}] %s -- %s;" % (P(JD), P(JE)))
    s.append(r"\path[postaction={decorate,decoration={markings,mark=at position 0.5 with {\draw[otNavy,line width=.7pt] (0,-3.2pt) -- (0,3.2pt);}}}] %s -- %s;" % (P(JE), P(JC)))
    s += pt(JA, "A", 225) + pt(JB, "B", -45) + pt(JC, "C", 45) + pt(JD, "D", 135) + pt(JE, "E", 90)
    s.append(r"\node[txt,text=otOrange!70!black] at (%s,%s) {massif};" % (f(1.75 * U4), f(6.3 * U4)))
    s.append(r"\node[txt,text=otGreenDark] at (%s,%s) {pelouse};" % (f(9.4 * U4), f(2.2 * U4)))
    s += cote_seg(JA, JB, "$12$ m", d=-.55)
    s += cote_seg(JB, JC, "$9$ m", d=-.55)
    if corrige:
        s += lseg(JA, JC, VERT % "$15$ m", -1, t=.52, d=.13)
        s += lseg(JD, JE, VERT % "$6$ m", 1, d=.36)
        s.append(r"\node[txt,text=otGreenDark] at (%s,%s) {$27$ m²};" % (f(1.75 * U4), f(5.2 * U4)))
        s.append(r"\node[txt,text=otGreenDark] at (%s,%s) {$81$ m²};" % (f(9.4 * U4), f(1.35 * U4)))
    else:
        s.append(r"\node[txt,text=otMuted,anchor=south east] at (%s,%s) {allée};" % (f(8.0 * U4), f(6.15 * U4)))
    return figure(s)


FIGURES["brevet_3e_s04_jardin"] = jardin(False)
FIGURES["brevet_3e_s04_jardin_corrige"] = jardin(True)

# ---- Exercice 2 : la citerne (r = 0,8 m ; h = 1,5 m), 1 m = 1,5 cm
H_EAU = 0.72 / (0.64 * math.pi)
FIGURES["brevet_3e_s04_citerne"] = figure(cylindre(0, 1.2, 2.25, "$0{,}8$ m", "$1{,}5$ m"))
FIGURES["brevet_3e_s04_citerne_corrige"] = figure(cylindre(0, 1.2, 2.25, "$0{,}8$ m", "$1{,}5$ m",
                                                           eau=H_EAU * 1.5, eau_txt=r"$\approx 36$ cm"))

# ---- Exercice 3 : la charpente (GSD isocèle en S, GS = 5,2 m, angle G = 35°), 1 m = 0,6 cm
U5 = .6
_gf = 5.2 * math.cos(math.radians(35))
_sf = 5.2 * math.sin(math.radians(35))
KG, KD, KS, KF = (0, 0), (2 * _gf * U5, 0), (_gf * U5, _sf * U5), (_gf * U5, 0)


def toit(corrige):
    s = [r"\fill[otOrange!18] %s -- %s -- %s -- cycle;" % (P(KG), P(KD), P(KS)),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(KG), P(KD), P(KS)),
         r"\draw[%s] %s -- %s;" % ("otGreenDark,line width=1.3pt" if corrige else "aide", P(KS), P(KF))]
    for a, b in ((KG, KF), (KF, KD)):
        s.append(r"\path[postaction={decorate,decoration={markings,mark=at position 0.5 with {\draw[otNavy,line width=.7pt] (-1.2pt,-3.2pt) -- (-1.2pt,3.2pt) (1.2pt,-3.2pt) -- (1.2pt,3.2pt);}}}] %s -- %s;" % (P(a), P(b)))
    if corrige:
        s += angle_droit(KG, KF, KS, "otGreenDark")
    s += pt(KG, "G", 200) + pt(KD, "D", -20) + pt(KS, "S", 90) + pt(KF, "F", -90)
    s += lseg(KG, KS, "$5{,}2$ m", 1, d=.13)
    s += arc(KG, KD, KS, r"$35^\circ$", r=.75, dl=1.15)
    if corrige:
        s += lseg(KF, KS, VERT % r"$\approx 2{,}98$ m", -1, t=.32, d=.12)
        s += arc(KS, KG, KD, None, "otGreenDark", r=.42)
        s.append(r"\node[lab,text=otGreenDark,anchor=north east] at (%s,%s) {$110^\circ$};"
                 % (f(KS[0] - .08), f(KS[1] - .5)))
        s += cote_seg(KG, KF, VERT % r"$\approx 4{,}26$ m", d=-.5, coul="otGreenDark", txt_coul="otGreenDark",
                      cote_a_cote=True)
        s += cote_seg(KG, KD, VERT % r"$\approx 8{,}52$ m", d=-1.3, coul="otGreenDark", txt_coul="otGreenDark",
                      cote_a_cote=True)
    return figure(s)


FIGURES["brevet_3e_s04_toit"] = toit(False)
FIGURES["brevet_3e_s04_toit_corrige"] = toit(True)

# ---- Exercice 4 : programme de calcul (Scratch)
SCRIPT_S04 = [Drapeau(), Demander("Choisis un nombre"), Mettre("x", Reponse()),
              Mettre("a", Op(V("x"), "-", 3)), Mettre("b", Op(V("x"), "+", 3)),
              Mettre("r", Op(V("a"), "*", V("b"))), Dire(V("r"))]
scripts_fig("brevet_3e_s04_script", [("", SCRIPT_S04)])


# ######################################################################
#                              SUJET 05
# ######################################################################
# ---- Exercice 1 : trois formules (A : 15n ; B : 20 + 10n ; C : 60)
TARIFS = (r"width=6.4cm, height=5.6cm, xmin=0, xmax=10.6, ymin=0, ymax=172, gm, Q1, "
          r"xtick={0,1,...,10}, xticklabels={,1,2,3,4,5,6,7,8,9,10}, "
          r"ytick={20,40,...,160}, yticklabels={20,40,60,80,100,120,140,160}, minor ytick={10,30,...,150}, "
          r"xlabel={concerts}, ylabel={prix (\texteuro)}, "
          r"every axis y label/.style={at={(current axis.above origin)},anchor=south west,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}, "
          r"every axis x label/.style={at={(current axis.right of origin)},anchor=north east,yshift=-14pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}")


def tarifs(corrige):
    c = [r"\addplot[courbe, domain=0:10] {15*x};",
         r"\addplot[courbeB, domain=0:10] {20+10*x};",
         r"\addplot[courbeC, domain=0:10] {60};",
         r"\node[etiq,text=otNavy,anchor=east] at (axis cs:9.1,145) {A};",
         r"\node[etiq,text=otOrange!90!black,anchor=north west] at (axis cs:9.1,108) {B};",
         r"\node[etiq,text=otGreenDark,anchor=south] at (axis cs:9.5,62) {C};"]
    if corrige:
        c += [r"\draw[lecture] (axis cs:4,0) -- (axis cs:4,60);",
              r"\draw[lecture] (axis cs:7,0) -- (axis cs:7,105);",
              r"\pnt[otGreenDark]{4}{60} \pnt[otGreenDark]{7}{105} \pnt[otGreenDark]{7}{90} \pnt[otGreenDark]{7}{60}",
              r"\node[note,text=otGreenDark,anchor=south east] at (axis cs:3.85,64) {$(4\ ;\ 60)$};",
              r"\node[note,text=otGreenDark,anchor=east] at (axis cs:6.85,108) {$105$};",
              r"\node[note,text=otGreenDark,anchor=west] at (axis cs:7.15,86) {$90$};",
              r"\node[note,text=otGreenDark,anchor=north west] at (axis cs:7.1,57) {$60$};"]
    return graphe(TARIFS, "\n".join(c))


FIGURES["brevet_3e_s05_tarifs"] = tarifs(False)
FIGURES["brevet_3e_s05_tarifs_corrige"] = tarifs(True)

# ---- Exercice 1, question 6 : script à compléter (case A)
SCRIPT_S05 = [Drapeau(), Demander("Nombre de concerts ?"), Mettre("n", Reponse()),
              Mettre("prix", Trou("A", Op(20, "+", Op(10, "*", V("n"))))), Dire(V("prix"))]
scripts_fig("brevet_3e_s05_script", [("", SCRIPT_S05)])
scripts_fig("brevet_3e_s05_script_corrige", [("", SCRIPT_S05)], corrige=True)

# ---- Exercice 2 : le projecteur (PH = 6 m, HE = 8 m), 1 m = 0,5 cm
U6 = .5
PP, PH, PE = (0, 6 * U6), (0, 0), (8 * U6, 0)


def projecteur(corrige):
    s = [r"\draw[otMuted,line width=.7pt] (-.6,0) -- (%s,0);" % f(8 * U6 + .6),
         r"\fill[otOrange!22] %s -- %s -- %s -- cycle;" % (P(PP), P(PH), P(PE)),
         r"\draw[otNavy,line width=2pt] %s -- %s;" % (P(PH), P(PP)),
         r"\draw[%s] %s -- %s;" % ("otGreenDark,line width=1.4pt" if corrige else
                                   "otOrange!85!black,line width=1pt,dash pattern=on 4pt off 2.5pt", P(PP), P(PE))]
    s += angle_droit(PP, PH, PE)
    s += pt(PP, "P", 135) + pt(PH, "H", 225) + pt(PE, "E", -45)
    s += lseg(PH, PP, "$6$ m", 1, d=.14)
    s += lseg(PH, PE, "$8$ m", -1, d=.14)
    if corrige:
        s += lseg(PP, PE, VERT % "$10$ m", -1, d=.14)
        s += arc(PP, PH, PE, VERT % r"$\approx 53^\circ$", "otGreenDark", r=.65, dl=1.25)
    else:
        s += lseg(PP, PE, r"\textcolor{otOrange!85!black}{faisceau}", -1, d=.14)
    return figure(s)


FIGURES["brevet_3e_s05_projecteur"] = projecteur(False)
FIGURES["brevet_3e_s05_projecteur_corrige"] = projecteur(True)

# ---- Exercice 3 : la fréquentation
JOURS = ["Vendredi", "Samedi", "Dimanche"]
SPECT = [4200, 6800, 5400]


def frequentation(corrige):
    s, W = barres(JOURS, SPECT, 8000, 1000, unite=.0005, dx=1.75, larg=.42, titre_y="spectateurs",
                  valeurs=True, pas_lab=2000)
    if corrige:
        m = sum(SPECT) / 3
        s.append(r"\draw[otGreenDark,line width=1pt,dash pattern=on 4pt off 2.5pt] (0,%.3f) -- (%.3f,%.3f);" % (m * .0005, W, m * .0005))
        s.append(r"\node[txt,text=otGreenDark,anchor=west,align=left] at (%.3f,%.3f) {moyenne\\$\approx 5\,467$};"
                 % (W + .08, m * .0005))
    return figure(s)


FIGURES["brevet_3e_s05_frequentation"] = frequentation(False)
FIGURES["brevet_3e_s05_frequentation_corrige"] = frequentation(True)


# ######################################################################
#                           COURS ET FICHE
# ######################################################################
# ---- Déroulé des 2 heures (1 min = 0,075 cm)
def deroule():
    k = .055
    x1, x2 = 20 * k, 120 * k
    s = [r"\fill[otOrange!28] (0,1.0) rectangle (%s,1.62);" % f(x1),
         r"\draw[otOrange!80!black,line width=.8pt] (0,1.0) rectangle (%s,1.62);" % f(x1),
         r"\node[txt,anchor=west,align=left] at (%s,1.31) {\textbf{Partie 1} : 6 points, sans calculatrice};" % f(x1 + .1),
         r"\fill[otSky] (%s,.12) rectangle (%s,.74);" % (f(x1), f(x2)),
         r"\draw[otNavy,line width=.8pt] (%s,.12) rectangle (%s,.74);" % (f(x1), f(x2)),
         r"\node[txt] at (%s,.43) {\textbf{Partie 2} : 14 points, calculatrice};" % f((x1 + x2) / 2),
         r"\draw[axeS] (0,0) -- (%s,0);" % f(x2)]
    for m in range(0, 121, 10):
        h = .12 if m % 30 == 0 or m == 20 else .06
        s.append(r"\draw[axeS] (%s,0) -- (%s,-%s);" % (f(m * k), f(m * k), f(h)))
    for m, t in ((0, "0"), (20, "20 min"), (60, "1 h"), (90, "1 h 30"), (120, "2 h")):
        s.append(r"\node[petit,anchor=north] at (%s,-.16) {%s};" % (f(m * k), t))
    return figure(s)


FIGURES["cours_deroule"] = deroule()


# ---- Données → propriété → conclusion
def demarche():
    """Trois boîtes empilées (lisible sur téléphone) : titre, puis exemple dessous."""
    w, g, h = 6.3, .42, 1.2
    boites = [("otSky", "otNavy", "1. Données",
               r"Dans le triangle $ABC$, $BC^2 = AB^2 + AC^2$."),
              ("otOrange!18", "otOrange!80!black", "2. Propriété",
               r"D'après la réciproque de Pythagore,"),
              ("otGreen!18", "otGreenDark", "3. Conclusion",
               r"le triangle $ABC$ est rectangle en $A$.")]
    s = []
    for i, (fond, bord, titre, txt) in enumerate(boites):
        y = -i * (h + g)
        s.append(r"\fill[%s] (0,%s) rectangle (%s,%s);" % (fond, f(y), f(w), f(y + h)))
        s.append(r"\draw[%s,line width=.9pt,rounded corners=2pt] (0,%s) rectangle (%s,%s);" % (bord, f(y), f(w), f(y + h)))
        s.append(r"\node[txt,text=%s,anchor=north west] at (.15,%s) {\textbf{%s}};" % (bord, f(y + h - .1), titre))
        s.append(r"\node[font=\otRegular\fontsize{8.5}{11}\selectfont,text=otInk,anchor=south west] at (.15,%s) {%s};"
                 % (f(y + .12), txt))
        if i < 2:
            s.append(r"\draw[otMuted,line width=1pt,-{Stealth[length=2mm]}] (%s,%s) -- (%s,%s);"
                     % (f(w / 2), f(y - .05), f(w / 2), f(y - g + .05)))
    return figure(s)


FIGURES["cours_demarche"] = demarche()

# ---- Fiche : trigonométrie (rôle des côtés pour l'angle en A)
FIGURES["fiche_trigo"] = figure(tri_rect("ABC", 3.6, 2.4, 1.0, cotes={"adj": "", "hyp": "", "opp": ""},
                                         roles=("adj", "hyp", "opp"), ang_txt=None))


# ---- Fiche : les deux configurations de Thalès
def thales():
    s = []
    # triangles emboîtés
    A, B, C = (1.35, 2.4), (0, 0), (2.9, 0)
    t = .45
    M = (A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1]))
    N = (A[0] + t * (C[0] - A[0]), A[1] + t * (C[1] - A[1]))
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
          r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
          r"\draw[geoReponse,line width=1.3pt] %s -- %s;" % (P(M), P(N)),
          r"\draw[otNavy,line width=1.3pt] %s -- %s;" % (P(B), P(C))]
    s += pt(A, "A", 90) + pt(B, "B", 225) + pt(C, "C", -45) + pt(M, "M", 180) + pt(N, "N", 0)
    s.append(r"\node[txt,text=otMuted,anchor=north] at (1.45,-.42) {emboîtés};")
    # papillon
    A2, B2, C2 = (5.25, 1.1), (4.0, 0), (6.6, 0)
    t2 = -.6
    M2 = (A2[0] + t2 * (B2[0] - A2[0]), A2[1] + t2 * (B2[1] - A2[1]))
    N2 = (A2[0] + t2 * (C2[0] - A2[0]), A2[1] + t2 * (C2[1] - A2[1]))
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A2), P(B2), P(C2)),
          r"\fill[otGreen!18] %s -- %s -- %s -- cycle;" % (P(A2), P(M2), P(N2)),
          r"\draw[geoTrait] %s -- %s %s -- %s;" % (P(B2), P(M2), P(C2), P(N2)),
          r"\draw[otNavy,line width=1.3pt] %s -- %s;" % (P(B2), P(C2)),
          r"\draw[geoReponse,line width=1.3pt] %s -- %s;" % (P(M2), P(N2))]
    s += pt(A2, "A", 180, d=.2) + pt(B2, "B", 225) + pt(C2, "C", -45) + pt(M2, "M", 45) + pt(N2, "N", 135)
    s.append(r"\node[txt,text=otMuted,anchor=north] at (5.3,-.42) {papillon};")
    return figure(s)


FIGURES["fiche_thales"] = thales()


# ######################################################################
#             PARTIE B (sujets 06 à 10) : aides supplémentaires
# ######################################################################
# Solides en perspective cavalière (repris de la notion 247 : angle 40°, coefficient 0,6)
K3, AL3 = 0.6, math.radians(40)
CX3, CY3 = K3 * math.cos(AL3), K3 * math.sin(AL3)


def P3(x, y, z, s=1.0):
    """Projection cavalière d'un point de l'espace (x : largeur, y : profondeur, z : hauteur)."""
    return (s * (x + CX3 * y), s * (z + CY3 * y))


def pave_cav(Lx, W, H, s, eau=None):
    """Pavé droit (repris de 247) ; eau : hauteur d'eau dessinée en vert (corrigé)."""
    S = {"A": (0, 0, 0), "B": (Lx, 0, 0), "C": (Lx, 0, H), "D": (0, 0, H),
         "E": (0, W, 0), "F": (Lx, W, 0), "G": (Lx, W, H), "H": (0, W, H)}
    p = {k: P(P3(*v, s=s)) for k, v in S.items()}
    out = [r"\fill[face] %s -- %s -- %s -- %s -- %s -- %s -- cycle;" % tuple(p[k] for k in "ABFGHD")]
    if eau is not None:
        q = [P(P3(*v, s=s)) for v in ((0, 0, 0), (Lx, 0, 0), (Lx, W, 0), (Lx, W, eau), (0, W, eau), (0, 0, eau))]
        out.append(r"\fill[otGreen!22] %s -- %s -- %s -- %s -- %s -- %s -- cycle;" % tuple(q))
        out.append(r"\draw[otGreenDark,line width=.7pt] %s -- %s -- %s;" % (q[5], P(P3(Lx, 0, eau, s)), q[3]))
        out.append(r"\draw[otGreenDark,line width=.5pt,dash pattern=on 2pt off 1.5pt] %s -- %s -- %s;" % (q[3], q[4], q[5]))
    out += [r"\draw[cache] %s -- %s -- %s %s -- %s;" % (p["A"], p["E"], p["F"], p["E"], p["H"]),
            r"\draw[solide] %s -- %s -- %s -- %s -- cycle;" % (p["A"], p["B"], p["C"], p["D"]),
            r"\draw[solide] %s -- %s -- %s -- %s -- %s %s -- %s;" % (p["B"], p["F"], p["G"], p["H"], p["D"], p["C"], p["G"])]
    return out


def cornet_glace(xc, r, h, lr, lh, vert=False):
    """Cornet : cône pointe en bas (rayon r, hauteur h) surmonté d'une demi-boule de rayon r (repris de 247)."""
    ry = 0.32 * r
    trait = "rep" if vert else "solide"
    cach = "repc" if vert else "cache"
    tc = "otGreenDark" if vert else "otInk"
    L = [rf"\fill[{'otGreen!22' if vert else 'otOrange!25'}] ({f(xc)},0) -- ({f(xc-r)},{f(h)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}] -- cycle;",
         rf"\fill[{'otGreen!12' if vert else 'face'}] ({f(xc-r)},{f(h)}) arc[start angle=180,end angle=0,radius={f(r)}] arc[start angle=0,end angle=-180,x radius={f(r)},y radius={f(ry)}] -- cycle;",
         rf"\draw[{cach}] ({f(xc+r)},{f(h)}) arc[start angle=0,end angle=180,x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[{trait}] ({f(xc-r)},{f(h)}) arc[start angle=180,end angle=0,radius={f(r)}];",
         rf"\draw[{trait}] ({f(xc-r)},{f(h)}) arc[start angle=180,end angle=360,x radius={f(r)},y radius={f(ry)}];",
         rf"\draw[{trait}] ({f(xc-r)},{f(h)}) -- ({f(xc)},0) -- ({f(xc+r)},{f(h)});",
         rf"\draw[hauteur] ({f(xc)},{f(h)}) -- ({f(xc+r)},{f(h)});",
         rf"\fill[otNavy] ({f(xc)},{f(h)}) circle (1.4pt);",
         rf"\node[anchor=west,text={tc}] at ({f(xc+r)},{f(h)}) [xshift=2pt] {{{lr}}};",
         rf"\draw[cote] ({f(xc-r-0.32)},0) -- ({f(xc-r-0.32)},{f(h)});",
         rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] ({f(xc-0.1)},0) -- ({f(xc-r-0.42)},0);",
         rf"\draw[otMuted,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] ({f(xc-r-0.1)},{f(h)}) -- ({f(xc-r-0.42)},{f(h)});",
         rf"\node[anchor=east,text={tc}] at ({f(xc-r-0.4)},{f(h/2)}) {{{lh}}};"]
    return L


# Sphère terrestre (repris de 247 : projection orthogonale, parties cachées en pointillés)
EL_T = 22.0


def sp_t(lat, lon, R, lon0):
    la, lo = math.radians(lat), math.radians(lon - lon0)
    x, y, z = math.cos(la) * math.sin(lo), math.sin(la), math.cos(la) * math.cos(lo)
    e = math.radians(EL_T)
    return R * x, R * (y * math.cos(e) - z * math.sin(e)), y * math.sin(e) + z * math.cos(e)


def courbe_sph(points, epais, cache):
    out, seg, vis = [], [], None
    for (x, y, d) in points:
        v = d >= 0
        if vis is None or v == vis:
            seg.append((x, y))
        else:
            seg.append((x, y))
            out.append((vis, seg))
            seg = [(x, y)]
        vis = v
    out.append((vis, seg))
    return [rf"\draw[{epais if v else cache}] " + " -- ".join(P(p) for p in sg) + ";" for v, sg in out if len(sg) > 1]


def globe_t(R, lon0, points=(), arc_=None):
    L = [rf"\fill[face] (0,0) circle ({f(R)});"]
    L += courbe_sph([sp_t(0, lo, R, lon0) for lo in range(-180, 181, 2)],
                    "otNavy,line width=1pt", "otNavy,line width=.6pt,dash pattern=on 2.5pt off 2pt")
    L += courbe_sph([sp_t(la, 0, R, lon0) for la in range(-90, 91, 2)],
                    "otOrange!85!black,line width=1pt", "otOrange!85!black,line width=.6pt,dash pattern=on 2.5pt off 2pt")
    if arc_:
        la, a, b = arc_
        L += courbe_sph([sp_t(la, lo, R, lon0) for lo in range(a, b + 1)], "otGreenDark,line width=2.2pt",
                        "otGreenDark,line width=1.2pt")
    L.append(rf"\draw[solide] (0,0) circle ({f(R)});")
    N_ = sp_t(90, 0, R, lon0)
    L += [rf"\fill[otNavy] {P(N_[:2])} circle (1.5pt);",
          rf"\node[anchor=south,text=otNavy,font=\small] at ({f(N_[0])},{f(R)}) [yshift=1pt] {{pôle Nord}};",
          rf"\fill[otNavy] (0,0) circle (1.3pt);"]
    e = sp_t(0, lon0 - 62, R, lon0)
    L += [rf"\node[anchor=north east,text=otNavy,font=\small] at ({f(-0.72*R)},{f(-0.8*R)}) {{équateur}};",
          rf"\draw[otNavy,line width=.4pt] ({f(-0.74*R)},{f(-0.82*R)}) -- {P(e[:2])};"]
    g = sp_t(58, 0, R, lon0)
    L += [rf"\node[anchor=south west,text=otOrange!75!black,font=\small,align=left] at ({f(0.62*R)},{f(0.86*R)}) {{méridien de\\Greenwich}};",
          rf"\draw[otOrange!75!black,line width=.4pt] ({f(0.64*R)},{f(0.88*R)}) -- {P(g[:2])};"]
    for (la, lo, nom, sgx, sgy, coul) in points:
        x, y, _ = sp_t(la, lo, R, lon0)
        L += [rf"\fill[{coul}] {P((x, y))} circle (1.9pt);",
              rf"\node[text={coul},inner sep=1pt,anchor={'south west' if sgx > 0 else 'south east'}] at {P((x + .06 * sgx, y + .1 * sgy))} {{{nom}}};"]
    return L


def quadrillage(x0, x1, y0, y1, u):
    s = []
    for x in range(x0, x1 + 1):
        s.append(r"\draw[otRule,line width=.35pt] (%s,%s) -- (%s,%s);" % (f(x * u), f(y0 * u), f(x * u), f(y1 * u)))
    for y in range(y0, y1 + 1):
        s.append(r"\draw[otRule,line width=.35pt] (%s,%s) -- (%s,%s);" % (f(x0 * u), f(y * u), f(x1 * u), f(y * u)))
    return s


def pastille(x, y, txt, coul="otNavy"):
    """Numéro de figure dans un cercle, centré dans une case (ne touche aucun trait)."""
    return [r"\node[circle,draw=%s,line width=.7pt,inner sep=.9pt,fill=white,text=%s,font=\otMedium\fontsize{8}{9}\selectfont] at (%s,%s) {%s};"
            % (coul, coul, f(x), f(y), txt)]


def triangle_grille(T, u, fond, trait):
    pts = " -- ".join(P((x * u, y * u)) for x, y in T)
    return [r"\fill[%s] %s -- cycle;" % (fond, pts), r"\draw[%s] %s -- cycle;" % (trait, pts)]


AXES_Q1 = (r"every axis y label/.style={at={(current axis.above origin)},anchor=south west,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}, "
           r"every axis x label/.style={at={(current axis.right of origin)},anchor=north east,yshift=-14pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted}")


# ######################################################################
#                              SUJET 06
# ######################################################################
# ---- Exercice 1 : l'aquarium 80 × 35 × 40 (cm), eau à 36 cm au corrigé ; 1 cm = 0,065 cm
S6 = .065


def aquarium(corrige):
    L = pave_cav(80, 35, 40, S6, eau=36 if corrige else None)
    a = P3(40, 0, 0, S6)
    b = P3(80, 17.5, 0, S6)
    c = P3(80, 35, 20, S6)
    L += [r"\node[lab,anchor=north] at %s {$80$ cm};" % P((a[0], a[1] - .1)),
          r"\node[lab,anchor=north west] at %s {$35$ cm};" % P((b[0] + .06, b[1] - .02)),
          r"\node[lab,anchor=west] at %s {$40$ cm};" % P((c[0] + .1, c[1]))]
    if corrige:
        d0, d1 = P3(-7, 0, 0, S6), P3(-7, 0, 36, S6)
        L += [r"\draw[cote,otGreenDark] %s -- %s;" % (P(d0), P(d1)),
              r"\node[lab,text=otGreenDark,anchor=east] at %s {$36$ cm};" % P((d0[0] - .08, (d0[1] + d1[1]) / 2))]
    return figure(L)


FIGURES["brevet_3e_s06_aquarium"] = aquarium(False)
FIGURES["brevet_3e_s06_aquarium_corrige"] = aquarium(True)


# ---- Exercice 3 : effet d'un agrandissement sur les aires (exemple k = 3)
def aires_k2(u=.42):
    x0 = 2.3
    s = [r"\fill[otSky] (0,0) rectangle (%s,%s);" % (f(u), f(u)),
         r"\draw[geoTrait] (0,0) rectangle (%s,%s);" % (f(u), f(u)),
         r"\fill[otGreen!22] (%s,0) rectangle (%s,%s);" % (f(x0), f(x0 + 3 * u), f(3 * u))]
    for k in (1, 2):
        s.append(r"\draw[otGreenDark!55,line width=.45pt] (%s,0) -- (%s,%s);" % (f(x0 + k * u), f(x0 + k * u), f(3 * u)))
        s.append(r"\draw[otGreenDark!55,line width=.45pt] (%s,%s) -- (%s,%s);" % (f(x0), f(k * u), f(x0 + 3 * u), f(k * u)))
    s.append(r"\draw[geoReponse,line width=1.1pt] (%s,0) rectangle (%s,%s);" % (f(x0), f(x0 + 3 * u), f(3 * u)))
    s.append(r"\draw[otMuted,line width=.9pt,-{Stealth[length=2mm]}] (%s,%s) -- (%s,%s);" % (f(u + .2), f(u / 2), f(x0 - .2), f(u / 2)))
    s.append(r"\node[txt,text=otMuted,anchor=south] at (%s,%s) {$\times 3$};" % (f((u + x0) / 2), f(u / 2 + .1)))
    s.append(r"\node[txt,anchor=north,align=center] at (%s,-.12) {côté $1$\\aire $1$};" % f(u / 2))
    s.append(r"\node[txt,text=otGreenDark,anchor=north,align=center] at (%s,-.12) {côté $3$\\aire $9 = 3^2$};" % f(x0 + 1.5 * u))
    return figure(s)


FIGURES["brevet_3e_s06_aires_corrige"] = aires_k2()

# ---- Exercice 4 : simulation de la croissance (Scratch, « répéter jusqu'à »)
SCRIPT_S06 = [Drapeau(), Mettre("n", 5000), Mettre("t", 0),
              JusquA(Cmp(V("n"), ">", 1000000), [Mettre("n", Op(V("n"), "*", 2)), Ajouter("t", 20)]),
              Dire(V("t"))]
SCRIPT_S06_TRIPLE = [Drapeau(), Mettre("n", 5000), Mettre("t", 0),
                     JusquA(Cmp(V("n"), ">", 1000000), [Mettre("n", Op(V("n"), "*", 3), hl=True), Ajouter("t", 30, hl=True)]),
                     Dire(V("t"))]
scripts_fig("brevet_3e_s06_script", [("", SCRIPT_S06)])
scripts_fig("brevet_3e_s06_script_corrige", [("", SCRIPT_S06_TRIPLE)], corrige=True)


# ######################################################################
#                              SUJET 07
# ######################################################################
# ---- Partie 1, question 10 : rotation de centre O et d'angle 90° (sens inverse des aiguilles)
T1_S07 = [(1, 1), (4, 1), (1, 3)]
T2_S07 = [(-y, x) for x, y in T1_S07]
U7G = .46


def rotation_q10(corrige):
    u = U7G
    s = quadrillage(-5, 5, -1, 5, u)
    s += triangle_grille(T1_S07, u, "otSky", "geoTrait")
    s += triangle_grille(T2_S07, u, "otGreen!25" if corrige else "otSky",
                         "geoReponse,line width=1.2pt" if corrige else "geoTrait")
    if corrige:
        A1, A2 = T1_S07[1], T2_S07[1]
        s += [r"\draw[lecture] (0,0) -- %s;" % P((A1[0] * u, A1[1] * u)),
              r"\draw[lecture] (0,0) -- %s;" % P((A2[0] * u, A2[1] * u))]
        r = math.hypot(*A1) * u
        a1 = math.degrees(math.atan2(A1[1], A1[0]))
        s.append(r"\draw[otGreenDark,line width=.9pt,-{Stealth[length=2mm]}] %s arc[start angle=%s,delta angle=86,radius=%s];"
                 % (P((A1[0] * u, A1[1] * u)), f(a1), f(r)))
        s += angle_droit((A1[0], A1[1]), (0, 0), (A2[0], A2[1]), "otGreenDark", r=.22)
    s.append(r"\fill[otNavy] (0,0) circle (2.1pt);")
    s.append(r"\node[lab,anchor=north west] at (.07,-.07) {$O$};")
    s += pastille(1.5 * u, 1.5 * u, "1")
    s += pastille(-1.5 * u, 1.5 * u, "2", "otGreenDark" if corrige else "otNavy")
    return figure(s)


FIGURES["brevet_3e_s07_rotation"] = rotation_q10(False)
FIGURES["brevet_3e_s07_rotation_corrige"] = rotation_q10(True)

# ---- Exercice 1 : la grande roue (rayon 25 m, centre à 27 m du sol) ; 1 m = 0,062 cm
U7 = .062
RO = (0.0, 27 * U7)
RP = (0.0, 2 * U7)
RM = (RO[0] + 25 * U7 * math.cos(math.radians(-30)), RO[1] + 25 * U7 * math.sin(math.radians(-30)))
RH = (0.0, RO[1] - 25 * U7 * math.cos(math.radians(60)))


def grande_roue(corrige):
    R = 25 * U7
    s = [r"\fill[otSky!70] (%s,%s) circle (%s);" % (f(RO[0]), f(RO[1]), f(R)),
         r"\draw[otNavy,line width=1.1pt] (%s,%s) circle (%s);" % (f(RO[0]), f(RO[1]), f(R)),
         r"\draw[otMuted,line width=.8pt] (-2.3,0) -- (2.3,0);",
         r"\draw[geoTrait] %s -- %s;" % (P(RO), P(RP)),
         r"\draw[geoTrait] %s -- %s;" % (P(RO), P(RM))]
    s += arc(RO, RP, RM, r"$60^\circ$", r=.32, dl=.7)
    s += lseg(RO, RM, "$25$ m", 1, t=.42, d=.1)
    # hauteur du centre
    s += [r"\draw[otMuted!70,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] (-.1,%s) -- (-2.08,%s);" % (f(RO[1]), f(RO[1])),
          r"\draw[cote] (-1.98,0) -- (-1.98,%s);" % f(RO[1]),
          r"\node[lab,anchor=east] at (-2.06,%s) {$27$ m};" % f(RO[1] / 2)]
    if corrige:
        s += [r"\draw[repc] %s -- %s;" % (P(RM), P(RH)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(RO), P(RH))]
        s += angle_droit(RO, RH, RM, "otGreenDark", r=.16)
        s += lseg(RO, RH, VERT % "$12{,}5$ m", -1, d=.12)
        xc = RM[0] + .42
        s += [r"\draw[otMuted!70,line width=.4pt,dash pattern=on 1.5pt off 1.5pt] (%s,%s) -- (%s,%s);" % (f(RM[0] + .1), f(RM[1]), f(xc + .1), f(RM[1])),
              r"\draw[cote,otGreenDark] (%s,0) -- (%s,%s);" % (f(xc), f(xc), f(RM[1])),
              r"\node[lab,text=otGreenDark,anchor=west] at (%s,%s) {$14{,}5$ m};" % (f(xc + .08), f(RM[1] / 2))]
        s += pt(RH, "H", 180, coul="otGreenDark", txt_coul="otGreenDark")
    s += pt(RO, "O", 135) + pt(RP, "P", 150, d=.17) + pt(RM, "M", 30)
    return figure(s)


FIGURES["brevet_3e_s07_roue"] = grande_roue(False)
FIGURES["brevet_3e_s07_roue_corrige"] = grande_roue(True)

# ---- Exercice 2 : le grand huit, h(t) = -0,5 t² + 6 t + 2
GRAND_HUIT = (r"width=6.4cm, height=5.2cm, xmin=0, xmax=12.8, ymin=0, ymax=23.5, gm, Q1, "
              r"xtick={0,1,...,12}, xticklabels={,,2,,4,,6,,8,,10,,12}, "
              r"ytick={2,4,...,22}, yticklabels={2,4,6,8,10,12,14,16,18,20,22}, minor ytick={1,3,...,21}, "
              r"xlabel={temps (s)}, ylabel={hauteur (m)}, " + AXES_Q1)


def grand_huit(corrige):
    c = [r"\addplot[courbe, domain=0:12] {-0.5*x^2+6*x+2};"]
    if corrige:
        c += [r"\draw[niveau] (axis cs:0,18) -- (axis cs:12.4,18);",
              r"\draw[lecture] (axis cs:6,0) -- (axis cs:6,20) -- (axis cs:0,20);",
              r"\draw[lecture] (axis cs:4,0) -- (axis cs:4,18);",
              r"\draw[lecture] (axis cs:8,0) -- (axis cs:8,18);",
              r"\draw[lecture] (axis cs:10,0) -- (axis cs:10,12) -- (axis cs:0,12);",
              r"\sol{4}{8}",
              r"\pnt[otGreenDark]{6}{20} \pnt[otGreenDark]{4}{18} \pnt[otGreenDark]{8}{18} \pnt[otGreenDark]{10}{12} \pnt[otGreenDark]{0}{2}",
              r"\node[note,text=otGreenDark,anchor=south] at (axis cs:6,20.6) {$(6\ ;\ 20)$};"]
    return graphe(GRAND_HUIT, "\n".join(c))


FIGURES["brevet_3e_s07_grand_huit"] = grand_huit(False)
FIGURES["brevet_3e_s07_grand_huit_corrige"] = grand_huit(True)

# ---- Exercice 3 : le cornet (cône r = 3 cm, h = 12 cm + demi-boule r = 3 cm) ; 1 cm = 0,3 cm
FIGURES["brevet_3e_s07_cornet"] = figure(cornet_glace(0, .9, 3.6, "$3$ cm", "$12$ cm"))
FIGURES["brevet_3e_s07_cornet_corrige"] = figure(
    cornet_glace(0, .9, 3.6, "$3$ cm", "$12$ cm")
    + cornet_glace(3.5, .6, 2.4, VERT % "$2$ cm", VERT % "$8$ cm", vert=True)
    + [r"\node[txt,text=otNavy,anchor=north] at (0,-.12) {cornet};",
       r"\node[txt,text=otGreenDark,anchor=north] at (3.5,-.12) {mini-cornet};"])


# ######################################################################
#                              SUJET 08
# ######################################################################
# ---- Exercice 1 : le parcours ABC (AB = 1,2 km ; BC = 0,9 km ; CA = 1,5 km) ; 1 km = 2,6 cm
U8 = 2.6
PA, PB, PC = (0, 0), (1.2 * U8, 0), (1.2 * U8, .9 * U8)


def parcours(corrige):
    fl = r"\draw[geoTrait,postaction={decorate,decoration={markings,mark=at position 0.24 with {\arrow{Stealth[length=2.4mm]}}}}] %s -- %s;"
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(PA), P(PB), P(PC)),
         fl % (P(PA), P(PB)), fl % (P(PB), P(PC)), fl % (P(PC), P(PA))]
    s += lseg(PA, PB, "$1{,}2$ km", -1, t=.6, d=.14)
    s += lseg(PB, PC, "$0{,}9$ km", -1, t=.62, d=.14)
    s += lseg(PA, PC, "$1{,}5$ km", 1, t=.45, d=.14)
    if corrige:
        s += angle_droit(PA, PB, PC, "otGreenDark", r=.26)
        s += arc(PA, PB, PC, VERT % r"$\approx 37^\circ$", "otGreenDark", r=.75, dl=1.45)
    s += pt(PA, "A", 200) + pt(PB, "B", -30) + pt(PC, "C", 60)
    return figure(s)


FIGURES["brevet_3e_s08_parcours"] = parcours(False)
FIGURES["brevet_3e_s08_parcours_corrige"] = parcours(True)

# ---- Exercice 2 : la somme rapportée D(x) = 1,5 x + 8 (corrigé)
DONS = (r"width=6.4cm, height=5cm, xmin=0, xmax=12.8, ymin=0, ymax=29, gm, Q1, "
        r"xtick={0,1,...,12}, xticklabels={,,2,,4,,6,,8,,10,,12}, "
        r"ytick={4,8,...,28}, yticklabels={4,8,12,16,20,24,28}, minor ytick={2,6,...,26}, "
        r"xlabel={distance (km)}, ylabel={somme (\texteuro)}, " + AXES_Q1)
FIGURES["brevet_3e_s08_dons_corrige"] = graphe(DONS, "\n".join([
    r"\addplot[courbe, domain=0:12] {1.5*x+8};",
    r"\node[etiq,text=otNavy,anchor=south east] at (axis cs:11.6,26.4) {$D$};",
    r"\draw[lecture] (axis cs:8,0) -- (axis cs:8,20) -- (axis cs:0,20);",
    r"\pnt[otGreenDark]{0}{8} \pnt[otGreenDark]{8}{20}",
    r"\node[note,text=otGreenDark,anchor=north west] at (axis cs:0.35,7.6) {$(0\ ;\ 8)$ : pas l'origine};",
    r"\node[note,text=otGreenDark,anchor=north west] at (axis cs:8.25,19.5) {$(8\ ;\ 20)$};"]))

# ---- Exercice 4 : script de chronométrage (Scratch, « si … alors … sinon »)
SCRIPT_S08 = [Drapeau(), Demander("Durée en min ?"), Mettre("t", Reponse()), Mettre("v", Op(648, "/", V("t"))),
              Si(Cmp(V("v"), ">", 12), [Dire("Objectif atteint !")], [Dire("Objectif manqué")])]
SCRIPT_S08_CORR = [Drapeau(), Demander("Durée en min ?"), Mettre("t", Reponse()), Mettre("v", Op(648, "/", V("t"))),
                   Si(Trou("", Non(Cmp(V("v"), "<", 12))),
                      [Dire("Objectif atteint !")], [Dire("Objectif manqué")])]
scripts_fig("brevet_3e_s08_script", [("", SCRIPT_S08)])
scripts_fig("brevet_3e_s08_script_corrige", [("", SCRIPT_S08_CORR)], corrige=True)


# ######################################################################
#                              SUJET 09
# ######################################################################
# ---- Exercice 1 : le pan de toit, triangle PHR rectangle en H, PR = 4,5 m, angle P = 30°
_ph9 = 4.5 * math.cos(math.radians(30))
FIGURES["brevet_3e_s09_toit"] = figure(tri_rect("PHR", _ph9, 2.25, .8, cotes={"hyp": "$4{,}5$ m"},
                                                ang_txt=r"$30^\circ$", arc_r=.7))
FIGURES["brevet_3e_s09_toit_corrige"] = figure(tri_rect("PHR", _ph9, 2.25, .8,
                                                        cotes={"hyp": "$4{,}5$ m", "opp": "$2{,}25$ m",
                                                               "adj": r"$\approx 3{,}90$ m"},
                                                        vert=("opp", "adj"), ang_txt=r"$30^\circ$", arc_r=.7))

# ---- Exercice 2 : deux offres, A(x) = 0,22 x + 12 et B(x) = 0,19 x + 18
OFFRES = (r"width=6.4cm, height=5.2cm, xmin=0, xmax=520, ymin=0, ymax=135, gm, Q1, "
          r"xtick={0,50,...,500}, xticklabels={,,100,,200,,300,,400,,500}, "
          r"ytick={20,40,...,120}, yticklabels={20,40,60,80,100,120}, minor ytick={10,30,...,130}, "
          r"xlabel={kWh}, ylabel={prix (\texteuro)}, " + AXES_Q1)


def offres(corrige):
    c = [r"\addplot[courbe, domain=0:500] {0.22*x+12};",
         r"\addplot[courbeB, domain=0:500] {0.19*x+18};",
         r"\node[etiq,text=otNavy,anchor=south east] at (axis cs:470,118) {A};",
         r"\node[etiq,text=otOrange!90!black,anchor=north west] at (axis cs:470,101) {B};"]
    if corrige:
        c += [r"\draw[lecture] (axis cs:200,0) -- (axis cs:200,56) -- (axis cs:0,56);",
              r"\pnt[otGreenDark]{200}{56}",
              r"\node[note,text=otGreenDark,anchor=south east] at (axis cs:190,62) {$(200\ ;\ 56)$};"]
    return graphe(OFFRES, "\n".join(c))


FIGURES["brevet_3e_s09_offres"] = offres(False)
FIGURES["brevet_3e_s09_offres_corrige"] = offres(True)

# ---- Exercice 3 : la maison (pavé 8 × 8 × 2,5) et ses combles (pyramide régulière, SO = 3 m)
S9 = .42


def maison(corrige):
    c, hm, hp = 8, 2.5, 3
    q = lambda x, y, z: P(P3(x, y, z, S9))  # noqa: E731
    A0, B0, C0, D0 = (0, 0, 0), (c, 0, 0), (c, c, 0), (0, c, 0)
    A, B, C, D = (0, 0, hm), (c, 0, hm), (c, c, hm), (0, c, hm)
    O, S, M = (c / 2, c / 2, hm), (c / 2, c / 2, hm + hp), (c / 2, 0, hm)
    s = [r"\fill[face] %s -- %s -- %s -- %s -- %s -- %s -- cycle;" % (q(*A0), q(*B0), q(*C0), q(*C), q(*S), q(*A)),
         r"\fill[otOrange!22] %s -- %s -- %s -- cycle;" % (q(*A), q(*B), q(*S)),
         r"\fill[otOrange!30] %s -- %s -- %s -- cycle;" % (q(*B), q(*C), q(*S)),
         r"\fill[otOrange!14] %s -- %s -- %s -- cycle;" % (q(*A), q(*D), q(*S)),
         # arêtes cachées
         r"\draw[cache] %s -- %s -- %s %s -- %s %s -- %s;" % (q(*A0), q(*D0), q(*C0), q(*D0), q(*D), q(*D), q(*C)),
         r"\draw[hauteur] %s -- %s;" % (q(*S), q(*O))]
    if corrige:
        s += [r"\draw[repc] %s -- %s;" % (q(*O), q(*M)),
              r"\draw[otGreenDark,line width=1.6pt] %s -- %s;" % (q(*S), q(*M))]
    s += [r"\draw[solide] %s -- %s -- %s -- %s -- cycle;" % (q(*A0), q(*B0), q(*B), q(*A)),
          r"\draw[solide] %s -- %s -- %s -- %s;" % (q(*B0), q(*C0), q(*C), q(*B)),
          r"\draw[solide] %s -- %s -- %s %s -- %s %s -- %s -- %s;" % (q(*A), q(*S), q(*B), q(*S), q(*C), q(*A), q(*D), q(*S)),
          r"\fill[otOrange!85!black] %s circle (1.5pt);" % q(*O),
          r"\fill[otNavy] %s circle (1.4pt);" % q(*M)]
    if corrige:
        po, pm = P3(*O, S9), P3(*M, S9)
        u = (pm[0] - po[0], pm[1] - po[1])
        n = math.hypot(*u)
        u = (u[0] / n * .2, u[1] / n * .2)
        s.append(r"\draw[otGreenDark,line width=.6pt] (%s,%s) -- (%s,%s) -- (%s,%s);"
                 % (f(po[0]), f(po[1] + .2), f(po[0] + u[0]), f(po[1] + .2 + u[1]), f(po[0] + u[0]), f(po[1] + u[1])))
    lb = lambda pnt, txt, anc, col="otInk": r"\node[lab,text=%s,anchor=%s] at %s {%s};" % (col, anc, P(pnt), txt)  # noqa: E731
    pa, pb, pc, pd, ps, po, pm = (P3(*v, S9) for v in (A, B, C, D, S, O, M))
    s += [lb((pa[0] - .08, pa[1] + .02), "$A$", "south east"), lb((pb[0] + .1, pb[1] - .02), "$B$", "north west"),
          lb((pc[0] + .08, pc[1]), "$C$", "west"), lb((pd[0] - .08, pd[1]), "$D$", "east"),
          lb((ps[0], ps[1] + .08), "$S$", "south"), lb((po[0] + .05, po[1] - .06), "$O$", "north west"),
          lb((pm[0], pm[1] - .1), "$M$", "north")]
    a0, b0 = P3(*A0, S9), P3(*B0, S9)
    s += [lb(((a0[0] + b0[0]) / 2, a0[1] - .08), "$8$ m", "north"),
          lb(P3(c + .25, c / 2, 0, S9), "$8$ m", "north west"),
          lb((a0[0] - .1, P3(0, 0, hm / 2, S9)[1]), "$2{,}5$ m", "east"),
          r"\node[lab,text=otOrange!75!black,anchor=south east] at %s {$SO = 3$ m};" % P((ps[0] - .22, ps[1] - .02))]
    if corrige:
        # triangle SOM en vraie grandeur (rectangle en O), à droite du dessin
        x0, y0, k = P3(c, c, 0, S9)[0] + .75, .25, .36
        o_, m_, s_ = (x0, y0), (x0 + 4 * k, y0), (x0, y0 + 3 * k)
        s += [r"\fill[otGreen!18] %s -- %s -- %s -- cycle;" % (P(o_), P(m_), P(s_)),
              r"\draw[otGreenDark,line width=.9pt] %s -- %s -- %s -- cycle;" % (P(o_), P(m_), P(s_))]
        s += angle_droit(m_, o_, s_, "otGreenDark", r=.15)
        s += lseg(o_, m_, VERT % "$4$ m", -1, d=.1) + lseg(o_, s_, VERT % "$3$ m", 1, d=.1)
        s += lseg(m_, s_, VERT % "$5$ m", -1, d=.1)
        s += [lb((o_[0] - .06, o_[1] - .06), VERT % "$O$", "north east", "otGreenDark"),
              lb((m_[0] + .08, m_[1] - .04), VERT % "$M$", "north west", "otGreenDark"),
              lb((s_[0], s_[1] + .08), VERT % "$S$", "south", "otGreenDark")]
    return figure(s)


FIGURES["brevet_3e_s09_maison"] = maison(False)
FIGURES["brevet_3e_s09_maison_corrige"] = maison(True)

# ---- Exercice 4 : consommation mensuelle (corrigé : diagramme, hiver en vert, moyenne)
MOIS = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre",
        "Novembre", "Décembre"]
CONSO = [420, 380, 320, 260, 210, 180, 170, 160, 200, 270, 340, 410]


def conso_corrige():
    k = .0078
    s, W = barres([m[0] for m in MOIS], CONSO, 450, 50, unite=k, dx=.43, larg=.14, titre_y="kWh",
                  vert=(0, 1, 11), pas_lab=100)
    m = sum(CONSO) / 12
    s.append(r"\draw[otGreenDark,line width=1pt,dash pattern=on 4pt off 2.5pt] (0,%s) -- (%s,%s);" % (f(m * k), f(W), f(m * k)))
    s.append(r"\node[txt,text=otGreenDark,anchor=west,align=left] at (%s,%s) {moyenne\\$\approx 277$};" % (f(W + .08), f(m * k)))
    return figure(s)


FIGURES["brevet_3e_s09_conso_corrige"] = conso_corrige()


# ######################################################################
#                              SUJET 10
# ######################################################################
# ---- Partie 1, question 10 : homothétie de centre O et de rapport -2
T1_S10 = [(1, 1), (3, 1), (1, 2)]
T2_S10 = [(-2 * x, -2 * y) for x, y in T1_S10]
U10G = .4


def homothetie_q10(corrige):
    u = U10G
    s = quadrillage(-7, 4, -5, 3, u)
    s += triangle_grille(T1_S10, u, "otSky", "geoTrait")
    s += triangle_grille(T2_S10, u, "otGreen!25" if corrige else "otSky",
                         "geoReponse,line width=1.2pt" if corrige else "geoTrait")
    if corrige:
        for a, b in zip(T1_S10, T2_S10):
            s.append(r"\draw[lecture] %s -- %s;" % (P((a[0] * u, a[1] * u)), P((b[0] * u, b[1] * u))))
    s.append(r"\fill[otNavy] (0,0) circle (2.1pt);")
    s.append(r"\node[lab,anchor=north west] at (.07,-.07) {$O$};")
    s += pastille(3.5 * u, 2.5 * u, "1")
    s += pastille(-5.5 * u, -4.5 * u, "2", "otGreenDark" if corrige else "otNavy")
    return figure(s)


FIGURES["brevet_3e_s10_homothetie"] = homothetie_q10(False)
FIGURES["brevet_3e_s10_homothetie_corrige"] = homothetie_q10(True)

# ---- Exercice 1 : le phare (PS = 45 m, angles 8° en A et 15° en B) ; figure pas à l'échelle
#      (angles dessinés : 22° et 40°, pour la lisibilité)
HPH = 2.2
FP = (5.45, 0.0)
FS = (FP[0], HPH)
FB = (FP[0] - HPH / math.tan(math.radians(40)), 0.0)
FA = (FP[0] - HPH / math.tan(math.radians(22)), 0.0)


def phare(corrige):
    s = [r"\fill[otSky!80] (-.35,-.02) rectangle (%s,-.3);" % f(FP[0] + .6),
         r"\draw[otNavy!60,line width=.8pt] (-.35,0) -- (%s,0);" % f(FP[0] + .6),
         r"\draw[otOrange!85!black,line width=.8pt,dash pattern=on 4pt off 2.5pt] %s -- %s;" % (P(FA), P(FS)),
         r"\draw[otOrange!85!black,line width=.8pt,dash pattern=on 4pt off 2.5pt] %s -- %s;" % (P(FB), P(FS)),
         r"\draw[otNavy,line width=2.4pt] %s -- %s;" % (P(FP), P(FS))]
    s += angle_droit(FA, FP, FS, r=.2)
    s += arc(FA, FP, FS, r"$8^\circ$", r=.95)
    s += arc(FB, FP, FS, r"$15^\circ$", r=.6)
    s += lseg(FP, FS, "$45$ m", -1, d=.16)
    s += pt(FA, "A", 135) + pt(FB, "B", 135) + pt(FS, "S", 90)
    s += [r"\fill[otNavy] %s circle (2.1pt);" % P(FP),
          r"\node[lab,anchor=north west] at %s {$P$};" % P((FP[0] + .08, -.08))]
    if corrige:
        s += cote_seg(FA, FB, VERT % r"$\approx 152$ m", d=-.55, coul="otGreenDark", txt_coul="otGreenDark", cote_a_cote=True)
        s += cote_seg(FB, FP, VERT % r"$\approx 168$ m", d=-.55, coul="otGreenDark", txt_coul="otGreenDark", cote_a_cote=True)
        s += cote_seg(FA, FP, VERT % r"$\approx 320$ m", d=-1.35, coul="otGreenDark", txt_coul="otGreenDark", cote_a_cote=True)
    return figure(s)


FIGURES["brevet_3e_s10_phare"] = phare(False)
FIGURES["brevet_3e_s10_phare_corrige"] = phare(True)

# ---- Exercice 2 : la traversée de l'Atlantique sur l'équateur, de 40° O (départ D) à 10° O (arrivée F)
LON0_T = -22.0
LON_D, LON_F = -40, -10
FIGURES["brevet_3e_s10_terre"] = figure(globe_t(2.3, LON0_T, points=[(0, LON_D, "$D$", -1, 1, "otNavy"),
                                                                     (0, LON_F, "$F$", 1, 1, "otNavy")]))
FIGURES["brevet_3e_s10_terre_corrige"] = figure(globe_t(2.3, LON0_T, points=[(0, LON_D, "$D$", -1, 1, "otGreenDark"),
                                                                             (0, LON_F, "$F$", 1, 1, "otGreenDark")],
                                                        arc_=(0, LON_D, LON_F)))

# ---- Exercice 3 : la voile MTB rectangle en M (MT = 6 m, MB = 4,5 m), renfort [RS] ; 1 m = 0,55 cm
U10 = .55
VM10, VT10, VB10 = (0, 0), (0, 6 * U10), (4.5 * U10, 0)
VR10 = (0, 2 * U10)                  # TR = 4 m
VS10 = (3 * U10, 2 * U10)            # TS = 5 m (sur [TB], TB = 7,5 m)


def voile10(corrige):
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(VM10), P(VT10), P(VB10))]
    if corrige:
        s.append(r"\fill[otGreen!22] %s -- %s -- %s -- cycle;" % (P(VT10), P(VR10), P(VS10)))
    s += [r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(VM10), P(VT10), P(VB10)),
          r"\draw[%s] %s -- %s;" % ("geoReponse,line width=1.5pt" if corrige else "geoTrait", P(VR10), P(VS10))]
    s += angle_droit(VT10, VM10, VB10)
    s += cote_seg(VM10, VT10, "$6$ m", d=1.0)
    s += lseg(VT10, VR10, "$4$ m", -1, d=.13)
    s += lseg(VT10, VS10, "$5$ m", 1, d=.13)
    s += lseg(VM10, VB10, "$4{,}5$ m", -1, d=.13)
    if corrige:
        s += angle_droit(VT10, VR10, VS10, "otGreenDark", r=.18)
        s += lseg(VR10, VS10, VERT % "$3$ m", -1, d=.13)
        s += lseg(VS10, VB10, VERT % "$2{,}5$ m", 1, d=.13)
    s += pt(VM10, "M", 225) + pt(VT10, "T", 90) + pt(VB10, "B", -30) + pt(VR10, "R", 180) + pt(VS10, "S", 30)
    return figure(s)


FIGURES["brevet_3e_s10_voile"] = voile10(False)
FIGURES["brevet_3e_s10_voile_corrige"] = voile10(True)

# ---- Exercice 4 : la marée, hauteur d'eau h(t) = 3,5 + 2,5 cos(30 t °) pour t de 0 à 12 h
MAREES = (r"width=6.4cm, height=4.8cm, xmin=0, xmax=12.8, ymin=0, ymax=7.4, gm, Q1, "
          r"xtick={0,1,...,12}, xticklabels={,,2,,4,,6,,8,,10,,12}, "
          r"ytick={1,2,...,7}, yticklabels={1,2,3,4,5,6,7}, minor ytick={0.5,1.5,...,6.5}, "
          r"xlabel={heure (h)}, ylabel={hauteur d'eau (m)}, " + AXES_Q1)


def marees(corrige):
    c = [r"\addplot[courbe, domain=0:12] {3.5+2.5*cos(30*x)};"]
    if corrige:
        c += [r"\draw[niveau] (axis cs:0,2.25) -- (axis cs:12.4,2.25);",
              r"\node[note,text=otOrange!90!black,anchor=south west] at (axis cs:8.6,2.35) {$2{,}25$ m};",
              r"\draw[lecture] (axis cs:4,0) -- (axis cs:4,2.25);",
              r"\draw[lecture] (axis cs:8,0) -- (axis cs:8,2.25);",
              r"\draw[lecture] (axis cs:3,0) -- (axis cs:3,3.5) -- (axis cs:0,3.5);",
              r"\sol{4}{8}",
              r"\pnt[otGreenDark]{0}{6} \pnt[otGreenDark]{6}{1} \pnt[otGreenDark]{3}{3.5} \pnt[otGreenDark]{4}{2.25} \pnt[otGreenDark]{8}{2.25}",
              r"\node[note,text=otGreenDark,anchor=south west] at (axis cs:0.3,6.05) {pleine mer};",
              r"\node[note,text=otGreenDark,anchor=north] at (axis cs:6,0.85) {basse mer};"]
    return graphe(MAREES, "\n".join(c))


FIGURES["brevet_3e_s10_marees"] = marees(False)
FIGURES["brevet_3e_s10_marees_corrige"] = marees(True)
