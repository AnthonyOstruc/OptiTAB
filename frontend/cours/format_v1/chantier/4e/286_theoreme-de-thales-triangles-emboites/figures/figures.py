# -*- coding: utf-8 -*-
"""Figures de la notion « Théorème de Thalès (triangles emboîtés) » (4e), style des livres.

Compilées par outils/figures_livre.py. Conventions :
- bleu marine : la figure et les données ; petite flèche identique sur deux segments
  = droites parallèles ;
- corrigés : côtés correspondants appariés en couleur (orange : côtés portés par le
  premier côté issu du sommet commun ; bleu : second côté ; violet : côtés parallèles),
  petit triangle teinté en vert, longueurs trouvées écrites en vert ;
- cotes (flèches) : morceaux au premier niveau, côtés entiers au second niveau.

CONTROLES (lu par verif_286.py) : coordonnées des configurations, pour vérifier que
M est sur [AB], N sur [AC], (MN) // (BC) et que les rapports dessinés sont ceux de l'énoncé.
"""
import math

PREAMBULE_EXTRA = r"""
\definecolor{otBleu}{HTML}{2F7FC1}
\definecolor{otViolet}{HTML}{8250B4}
\tikzset{
  lab/.style={text=otInk,inner sep=0pt},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt},
  rayon/.style={otOrange!90!black,line width=.75pt,dash pattern=on 3.5pt off 2pt},
  sol/.style={otMuted,line width=.8pt},
}
"""

V = r"\textcolor{otGreenDark}{%s}"
PA, PB, PC = "otOrange!90!black", "otBleu", "otViolet"
CONTROLES = {}


# ------------------------------------------------------------------ outils
def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


def lerp(a, b, t):
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def pt(p, nom, ang, coul="otNavy", d=.13, texte=None):
    a = math.radians(ang)
    q = (p[0] + d * math.cos(a), p[1] + d * math.sin(a))
    s = [r"\fill[%s] %s circle (2.1pt);" % (coul, P(p))]
    if nom:
        s.append(r"\node[lab,text=%s,anchor=%d] at %s {$%s$};"
                 % (texte or ("otInk" if coul == "otNavy" else coul), (ang + 180) % 360, P(q), nom))
    return s


def lab(p, txt, ang, d=.13, coul="otInk", font=""):
    a = math.radians(ang)
    q = (p[0] + d * math.cos(a), p[1] + d * math.sin(a))
    return [r"\node[lab,%stext=%s,anchor=%d] at %s {%s};" % (font, coul, (ang + 180) % 360, P(q), txt)]


def lseg(p, q, txt, cote=1, t=.5, d=.14, coul="otInk"):
    """Étiquette d'un segment [pq], à gauche (cote=1) ou à droite (cote=-1) de p→q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * cote, dx / L * cote
    m = (p[0] + t * dx + d * nx, p[1] + t * dy + d * ny)
    ang = math.degrees(math.atan2(ny, nx))
    noms = ["east", "north east", "north", "north west", "west", "south west", "south", "south east"]
    anc = noms[int(round(((ang + 180) % 360) / 45)) % 8]
    return [r"\node[lab,text=%s,anchor=%s] at %s {%s};" % (coul, anc, P(m), txt)]


def coord(**pts):
    return [" ".join(r"\coordinate (%s) at %s;" % (k, P(v)) for k, v in pts.items())]


def figure(corps):
    return "\n".join([r"\begin{tikzpicture}[line cap=round]"] + corps + [r"\end{tikzpicture}"])


def cote(p, q, txt, off=.42, coul=None):
    """Flèche de cote parallèle à [pq], décalée à gauche de p→q (coordonnées nommées)."""
    c = coul or "otMuted"
    lw = ",line width=.75pt" if coul else ""
    noeud = (r" node[midway,coteTexte]{%s}" % txt) if txt else ""
    return [r"\draw[cote,%s%s] ($(%s)!%scm!90:(%s)$) -- ($(%s)!%scm!-90:(%s)$)%s;"
            % (c, lw, p, f(off), q, q, f(off), p, noeud),
            r"\draw[%s!70,line width=.4pt] (%s) -- ($(%s)!%scm+2pt!90:(%s)$) (%s) -- ($(%s)!%scm+2pt!-90:(%s)$);"
            % (c, p, p, f(off), q, q, q, f(off), p)]


def chevron(p, q, t=.3, coul="otNavy", n=1):
    """Petite flèche de parallélisme sur [pq] (pointe dans le sens p→q)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    s = []
    for k in range(n):
        x = (p[0] + t * dx + (k - (n - 1) / 2) * .13 * ux, p[1] + t * dy + (k - (n - 1) / 2) * .13 * uy)
        tip = (x[0] + .075 * ux, x[1] + .075 * uy)
        a1 = (x[0] - .055 * ux + .08 * nx, x[1] - .055 * uy + .08 * ny)
        a2 = (x[0] - .055 * ux - .08 * nx, x[1] - .055 * uy - .08 * ny)
        s.append(r"\draw[%s,line width=1pt,line join=round] %s -- %s -- %s;" % (coul, P(a1), P(tip), P(a2)))
    return s


def angle_droit(o, p, q, r=.2, coul="otNavy"):
    """Petit carré d'angle droit en o, entre les directions o→p et o→q."""
    def u(a, b):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        return ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
    u1, u2 = u(o, p), u(o, q)
    a = (o[0] + r * u1[0], o[1] + r * u1[1])
    b = (a[0] + r * u2[0], a[1] + r * u2[1])
    c = (o[0] + r * u2[0], o[1] + r * u2[1])
    return [r"\draw[%s,line width=.6pt] %s -- %s -- %s;" % (coul, P(a), P(b), P(c))]


def tri(ab, ac, bc, U, x0=0.0, y0=0.0):
    """Triangle ABC de base [BC] horizontale (B à gauche), sommet A au-dessus, côtés réels × U."""
    xa = (ab * ab - ac * ac + bc * bc) / (2 * bc)
    ya = math.sqrt(ab * ab - xa * xa)
    return (x0 + xa * U, y0 + ya * U), (x0, y0), (x0 + bc * U, y0)


def V_(txt, vert):
    return (V % txt) if vert else txt


# ------------------------------------------------------------------ configuration emboîtée
CLES_COTE = {  # clé : (origine, extrémité) pour une cote à l'extérieur
    "AM": ("M", "A"), "MB": ("B", "M"), "AB": ("B", "A"),
    "AN": ("A", "N"), "NC": ("N", "C"), "AC": ("A", "C"), "BC": ("C", "B"),
}


def emb(nom_fig, A, B, C, r, L=None, noms="AMBNC", paires=False, vert=(), petit=False, pn=None,
        avant=(), apres=(), fond=(), forme=None, t_mn=.62, t_chev=.3, d_mn=.12, mn_dessus=False, off_bc=.5,
        niv1=.62, niv2=1.38):
    """Configuration emboîtée : M sur [AB] avec AM/AB = r, N sur [AC], (MN) // (BC).

    L : étiquettes par clé (AM, MB, AB, AN, NC, AC, MN, BC) ; vert : clés écrites en vert ;
    paires : côtés correspondants en couleur (AM-AB orange, AN-AC bleu, MN-BC violet).
    """
    L = L or {}
    a, m, b, n, c_ = noms
    M, N = lerp(A, B, r), lerp(A, C, r)
    CONTROLES[nom_fig] = (A, B, C, M, N, {"r": r, **({"forme": forme} if forme else {})})
    s = coord(A=A, B=B, C=C, M=M, N=N)
    s += list(avant)
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;"]
    if petit:
        s += [r"\fill[otGreen!18] (A) -- (M) -- (N) -- cycle;"]
    s += list(fond)
    cpar = PC if paires else "otNavy"
    s += [r"\draw[geoTrait] (B) -- (A) -- (C);"]
    s += [r"\draw[geoTrait%s] (B) -- (C);" % ((",draw=%s,line width=1.3pt" % PC) if paires else "")]
    s += [r"\draw[geoTrait%s] (M) -- (N);" % ((",draw=%s,line width=1.3pt" % PC) if paires else "")]
    s += chevron(M, N, t_chev, cpar) + chevron(B, C, t_chev, cpar)
    couleur = {"AM": PA, "AB": PA, "AN": PB, "AC": PB, "BC": PC} if paires else {}
    deux_g = any(k in L for k in ("AM", "MB")) and "AB" in L
    deux_d = any(k in L for k in ("AN", "NC")) and "AC" in L
    for cle, (p, q) in CLES_COTE.items():
        if cle not in L:
            continue
        off = niv1
        if cle in ("AB", "AC"):  # côté entier : toujours au second niveau, loin des noms M et N
            off = niv2 if (deux_g if cle == "AB" else deux_d) or 0.25 < r < 0.75 else niv1
        if cle == "BC":
            off = off_bc
        if cle == "BC" and cle in vert:  # longueur trouvée : flèche verte, texte vert sous la flèche
            s += cote(p, q, "", off, "otGreenDark")
            s += [r"\node[lab,anchor=north] at %s {%s};" % (P(((B[0] + C[0]) / 2, B[1] - off - .1)), V % L[cle])]
            continue
        s += cote(p, q, V_(L[cle], cle in vert), off, couleur.get(cle))
    if "MN" in L:
        coul_mn = "otGreenDark" if "MN" in vert else (PC if paires else "otInk")
        txt = L["MN"]
        s += lseg(M, N, txt, cote=1 if mn_dessus else -1, t=t_mn, d=d_mn, coul=coul_mn)
    pn = pn or {}
    # M et N : nom placé entre le côté (vers le bas) et la cote (vers l'extérieur)
    ang_g = math.degrees(math.atan2(A[1] - M[1], A[0] - M[0])) + 90 + 45
    ang_d = math.degrees(math.atan2(N[1] - A[1], N[0] - A[0])) + 45
    s += pt(A, a, pn.get("A", 90)) + pt(B, b, pn.get("B", 200)) + pt(C, c_, pn.get("C", 340))
    s += pt(M, m, pn.get("M", ang_g), d=.17) + pt(N, n, pn.get("N", ang_d), d=.17)
    s += list(apres)
    return figure(s)


FIGURES = {}

# ================================================================== COURS
A0, B0, C0 = (1.9, 4.2), (0, 0), (6.0, 0)
FIGURES["cours_config"] = emb("cours_config", A0, B0, C0, .45, petit=True,
                              apres=[r"\node[txt,text=otGreenDark,anchor=west] at (3.55,3.15) {petit triangle $AMN$};",
                                     r"\node[txt,text=otNavy,anchor=north] at (3.0,-.3) {grand triangle $ABC$};"])
FIGURES["cours_paires"] = emb("cours_paires", A0, B0, C0, .45,
                              {"AM": "$AM$", "AB": "$AB$", "AN": "$AN$", "AC": "$AC$", "MN": "$MN$", "BC": "$BC$"},
                              paires=True, petit=True)


def reduction():
    """Le triangle AMN (4 ; 6 ; 5) et le triangle ABC (6 ; 9 ; 7,5), côtés correspondants en couleur."""
    U = .42
    a1, m1, n1 = tri(4, 6, 5, U)
    a2, b2, c2 = tri(6, 9, 7.5, U, x0=3.3)
    s = [r"\fill[otGreen!18] %s -- %s -- %s -- cycle;" % (P(a1), P(m1), P(n1)),
         r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(a2), P(b2), P(c2))]
    # cote = côté extérieur : à droite de A→M (-1), à gauche de A→N (+1), sous [MN] (-1)
    for (p, q, coul, txt, cc) in ((a1, m1, PA, "4", -1), (a1, n1, PB, "6", 1), (m1, n1, PC, "5", -1),
                                  (a2, b2, PA, "6", -1), (a2, c2, PB, "9", 1), (b2, c2, PC, "7,5", -1)):
        s += [r"\draw[%s,line width=1.3pt] %s -- %s;" % (coul, P(p), P(q))]
        s += lseg(p, q, txt, cote=cc, d=.12, coul=coul)
    s += pt(a1, "A", 90) + pt(m1, "M", 225) + pt(n1, "N", 315)
    s += pt(a2, "A", 90) + pt(b2, "B", 225) + pt(c2, "C", 315)
    s += [r"\draw[otGreenDark,line width=.7pt,-{Stealth[length=2mm]}] (.55,2.05) -- (3.05,2.05);",
          r"\node[txt,text=otGreenDark,anchor=south] at (1.6,2.17) {agrandissement $\times\,1{,}5$};",
          r"\draw[otMuted,line width=.7pt,-{Stealth[length=2mm]}] (4.9,-.62) -- (1.0,-.62);",
          r"\node[txt,text=otMuted,anchor=north] at (2.95,-.75) {réduction $\times\,2/3$};"]
    return figure(s)


FIGURES["cours_reduction"] = reduction()


def ombre(sb, bm, sc, cn, U, txt, corrige=False, noms="SBMCN", visee=None):
    """Bâton [BM] et arbre [CN] verticaux, ombres [SB] et [SC] ; S, M, N alignés (rayon de soleil).

    txt : étiquettes (sb, sc, bm, cn, et en option sm, sn) ; corrige : paires en couleur.
    """
    s_, b_, m_, c_, n_ = noms
    S, B, C = (0, 0), (sb * U, 0), (sc * U, 0)
    M, N = (sb * U, bm * U), (sc * U, cn * U)
    CONTROLES["ombre_" + "_".join(map(f, (sb, bm, sc, cn)))] = (S, C, N, B, M, {"r": sb / sc})
    s = coord(S=S, B=B, C=C, M=M, N=N)
    s += [r"\fill[%s] (S) -- (C) -- (N) -- cycle;" % "otSky"]
    if corrige:
        s += [r"\fill[otGreen!18] (S) -- (B) -- (M) -- cycle;"]
    s += [r"\draw[sol] (-.35,0) -- %s;" % P((C[0] + .55, 0))]
    s += [r"\draw[rayon] (S) -- (N);"]
    cb = PB if corrige else "otNavy"
    s += [r"\draw[%s,line width=2pt] (B) -- (M);" % cb,
          r"\draw[%s,line width=2.4pt] (C) -- (N);" % cb]
    s += angle_droit(B, (B[0] - 1, 0), M, .17) + angle_droit(C, (C[0] - 1, 0), N, .2)
    ca = PA if corrige else None
    if sb * U < 1.0:  # cote trop courte pour son texte : texte écrit sous la flèche
        s += cote("B", "S", "", .6, ca)
        s += [r"\node[lab,anchor=east] at %s {%s};" % (P((-.12, -.6)), txt["sb"])]
        s += cote("C", "S", txt["sc"], 1.45, ca)
    else:
        s += cote("B", "S", txt["sb"], .6, ca) + cote("C", "S", txt["sc"], 1.25, ca)
    s += [r"\node[lab,anchor=west] at %s {\textcolor{otMuted}{\otMedium\fontsize{9}{11}\selectfont bâton :} %s};"
          % (P((M[0] + .12, M[1] * .45)), txt["bm"])]
    s += [r"\node[lab,anchor=west] at %s {%s};" % (P((N[0] + .16, N[1] * .5)), txt["cn"])]
    if "sm" in txt:
        s += lseg(S, M, txt["sm"], 1, t=.4, d=.12)
    if "sn" in txt:
        s += lseg(S, N, txt["sn"], 1, t=.62, d=.14)
    else:
        s += [r"\node[txt,text=otOrange!80!black,anchor=south east] at %s {rayon de soleil};"
              % P((N[0] * .55 - .12, N[1] * .55 + .12))]
    s += [r"\node[txt,text=otMuted,anchor=west] at %s {arbre};" % P((N[0] + .2, N[1] - .05))]
    s += pt(S, s_, 120, d=.15) + pt(B, b_, 315, d=.13) + pt(C, c_, 315, d=.13)
    s += pt(M, m_, 125, d=.15) + pt(N, n_, 125, d=.15)
    return figure(s)


FIGURES["cours_ombre"] = ombre(.8, 1, 6, 7.5, .75, {"sb": "0,8 m", "sc": "6 m", "bm": "1 m", "cn": "$h$"})


# ================================================================== EXERCICES
# ---------------------------------------------------------------- 3629 : trois figures
def trois_figures(corrige):
    s = []
    # (a) emboîtée : A M B N C
    A, B, C = (.9, 2.8), (0, 0), (2.3, 0)
    r = .42
    M, N = lerp(A, B, r), lerp(A, C, r)
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C))]
    if corrige:
        s += [r"\fill[otGreen!18] %s -- %s -- %s -- cycle;" % (P(A), P(M), P(N))]
    s += [r"\draw[geoTrait] %s -- %s -- %s -- cycle %s -- %s;" % (P(A), P(B), P(C), P(M), P(N))]
    s += chevron(M, N, .35) + chevron(B, C, .35)
    s += pt(A, "A", 90) + pt(B, "B", 235) + pt(C, "C", 305) + pt(M, "M", 180, d=.15) + pt(N, "N", 0, d=.15)
    s += [r"\node[txt,text=otNavy,anchor=north] at (1.15,-.42) {figure a};"]
    if corrige:
        s += [r"\node[txt,text=otGreenDark,anchor=north] at (1.15,-.85) {oui, sommet $A$};"]
    # (b) aucune information de parallélisme : E P F Q G
    x0 = 3.05
    E, F, G = (x0 + .9, 2.8), (x0, 0), (x0 + 2.3, 0)
    Pp, Q = lerp(E, F, .42), lerp(E, G, .45)
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(E), P(F), P(G)),
          r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(E), P(F), P(G)),
          r"\draw[%s] %s -- %s;" % ("otOrange!90!black,line width=1.1pt" if corrige else "geoTrait", P(Pp), P(Q))]
    s += pt(E, "E", 90) + pt(F, "F", 235) + pt(G, "G", 305) + pt(Pp, "P", 180, d=.15) + pt(Q, "Q", 0, d=.15)
    s += [r"\node[txt,text=otNavy,anchor=north] at (%s,-.42) {figure b};" % f(x0 + 1.15)]
    if corrige:
        s += [r"\node[txt,text=otOrange!80!black,anchor=north] at (%s,-.85) {non, rien n'est codé};" % f(x0 + 1.15)]
    # (c) sommet commun S en bas à gauche : U sur [SR], V sur [ST], (UV) // (RT)
    x1 = 6.05
    R_, S_, T_ = (x1 + 2.0, 2.8), (x1, 0), (x1 + 2.4, 0)
    k = .5
    U_, V_p = lerp(S_, R_, k), lerp(S_, T_, k)
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(R_), P(S_), P(T_))]
    if corrige:
        s += [r"\fill[otGreen!18] %s -- %s -- %s -- cycle;" % (P(S_), P(U_), P(V_p))]
    s += [r"\draw[geoTrait] %s -- %s -- %s -- cycle %s -- %s;" % (P(R_), P(S_), P(T_), P(U_), P(V_p))]
    s += chevron(V_p, U_, .45) + chevron(T_, R_, .45)
    s += pt(R_, "R", 90) + pt(S_, "S", 235) + pt(T_, "T", 305) + pt(U_, "U", 135, d=.15) + pt(V_p, "V", 300, d=.15)
    s += [r"\node[txt,text=otNavy,anchor=north] at (%s,-.42) {figure c};" % f(x1 + 1.2)]
    if corrige:
        s += [r"\node[txt,text=otGreenDark,anchor=north] at (%s,-.85) {oui, sommet $S$};" % f(x1 + 1.2)]
    return figure(s)


FIGURES["ex3629_enonce"] = trois_figures(False)
FIGURES["ex3629_corrige"] = trois_figures(True)

# ---------------------------------------------------------------- 3630 : R U S V T (RU/RS = 2/5)
A, B, C = tri(5, 7.5, 6.5, .62)
FIGURES["ex3630_enonce"] = emb("ex3630_enonce", A, B, C, .4, noms="RUSVT")
FIGURES["ex3630_corrige"] = emb("ex3630_corrige", A, B, C, .4,
                                {"AM": "2 cm", "AB": "5 cm", "AN": "3 cm", "NC": "4,5 cm", "AC": "7,5 cm"},
                                noms="RUSVT", paires=True, vert=("AC", "NC"), petit=True)

# ---------------------------------------------------------------- 3631 : 3 ; 5 ; 10 ; 8
A, B, C = tri(5, 10, 8, .62)
F3631 = (5, 10, 8)
FIGURES["ex3631_enonce"] = emb("ex3631_enonce", A, B, C, .6,
                               {"AM": "3 cm", "AB": "5 cm", "AC": "10 cm", "BC": "8 cm"}, forme=F3631)
FIGURES["ex3631_corrige"] = emb("ex3631_corrige", A, B, C, .6,
                                {"AM": "3 cm", "AB": "5 cm", "AN": "6 cm", "NC": "4 cm", "AC": "10 cm",
                                 "BC": "8 cm", "MN": "4,8 cm"},
                                paires=True, vert=("AN", "NC", "MN"), petit=True, forme=F3631)

# ---------------------------------------------------------------- 3632 : 4 ; 10 ; 12 ; 15
A, B, C = tri(10, 12, 15, .4)
F3632 = (10, 12, 15)
FIGURES["ex3632_enonce"] = emb("ex3632_enonce", A, B, C, .4,
                               {"AM": "4 cm", "AB": "10 cm", "AC": "12 cm", "BC": "15 cm"}, forme=F3632)
FIGURES["ex3632_corrige"] = emb("ex3632_corrige", A, B, C, .4,
                                {"AM": "4 cm", "AB": "10 cm", "AN": "4,8 cm", "AC": "12 cm", "BC": "15 cm",
                                 "MN": "6 cm"},
                                paires=True, vert=("AN", "MN"), petit=True, forme=F3632)

# ---------------------------------------------------------------- 3633 : AM 4, MB 6, AN 6, MN 5
A, B, C = tri(10, 15, 12.5, .4)
F3633 = (10, 15, 12.5)
FIGURES["ex3633_enonce"] = emb("ex3633_enonce", A, B, C, .4,
                               {"AM": "4 cm", "MB": "6 cm", "AN": "6 cm", "MN": "5 cm"}, forme=F3633)
FIGURES["ex3633_corrige"] = emb("ex3633_corrige", A, B, C, .4,
                                {"AM": "4 cm", "MB": "6 cm", "AB": "10 cm", "AN": "6 cm", "NC": "9 cm",
                                 "AC": "15 cm", "MN": "5 cm", "BC": "12,5 cm"},
                                paires=True, vert=("AB", "AC", "NC", "BC"), petit=True, forme=F3633)

# ---------------------------------------------------------------- 3634 : AM 2, AB 8, AC 6, BC 9
A, B, C = tri(8, 6, 9, .72)
F3634 = (8, 6, 9)
FIGURES["ex3634_enonce"] = emb("ex3634_enonce", A, B, C, .25,
                               {"AM": "2 cm", "AB": "8 cm", "AC": "6 cm", "BC": "9 cm"}, forme=F3634)
FIGURES["ex3634_corrige"] = emb("ex3634_corrige", A, B, C, .25,
                                {"AM": "2 cm", "AB": "8 cm", "AN": "1,5 cm", "AC": "6 cm", "BC": "9 cm",
                                 "MN": "2,25 cm"},
                                paires=True, vert=("AN", "MN"), petit=True, forme=F3634, mn_dessus=False)

# ---------------------------------------------------------------- 3635 : E H F K G (EH/EF = 3/5)
A, B, C = tri(5, 7, 6, .7)
F3635 = (5, 7, 6)
FIGURES["ex3635_enonce"] = emb("ex3635_enonce", A, B, C, .6, noms="EHFKG", forme=F3635)
FIGURES["ex3635_corrige"] = emb("ex3635_corrige", A, B, C, .6,
                                {"AM": "3 cm", "AB": "5 cm", "AN": "4,2 cm", "AC": "7 cm", "BC": "6 cm",
                                 "MN": "3,6 cm"},
                                noms="EHFKG", paires=True, vert=("AN", "MN"), petit=True, forme=F3635)

# ---------------------------------------------------------------- 3636 : ombre de l'arbre
FIGURES["ex3636_enonce"] = ombre(2, 1.5, 12, 9, .42, {"sb": "2 m", "sc": "12 m", "bm": "1,5 m", "cn": "?"})
FIGURES["ex3636_corrige"] = ombre(2, 1.5, 12, 9, .42,
                                  {"sb": "2 m", "sc": "12 m", "bm": "1,5 m", "cn": V % "9 m",
                                   "sm": V % "2,5 m", "sn": V % "15 m"}, corrige=True)

# ---------------------------------------------------------------- 3637 : 2,4 ; 6 ; 3 ; 3,2
A, B, C = tri(6, 7.5, 8, .7)
F3637 = (6, 7.5, 8)
FIGURES["ex3637_enonce"] = emb("ex3637_enonce", A, B, C, .4,
                               {"AM": "2,4 cm", "AB": "6 cm", "AN": "3 cm", "MN": "3,2 cm"}, forme=F3637)
FIGURES["ex3637_corrige"] = emb("ex3637_corrige", A, B, C, .4,
                                {"AM": "2,4 cm", "MB": "3,6 cm", "AB": "6 cm", "AN": "3 cm", "NC": "4,5 cm",
                                 "AC": "7,5 cm", "MN": "3,2 cm", "BC": "8 cm"},
                                paires=True, vert=("MB", "NC", "AC", "BC"), forme=F3637,
                                fond=[r"\fill[otGreen!18] (M) -- (B) -- (C) -- (N) -- cycle;"])


# ---------------------------------------------------------------- 3638 : deux parallèles
def deux_paralleles(corrige):
    A, B, C = tri(8, 12, 10, .5)
    M, N = lerp(A, B, .25), lerp(A, C, .25)
    Pp, Q = lerp(A, B, .625), lerp(A, C, .625)
    CONTROLES["ex3638_%s_MN" % corrige] = (A, B, C, M, N, {"r": .25, "forme": (8, 12, 10)})
    CONTROLES["ex3638_%s_PQ" % corrige] = (A, B, C, Pp, Q, {"r": .625})
    s = coord(A=A, B=B, C=C, M=M, N=N, P=Pp, Q=Q)
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;"]
    if corrige:
        s += [r"\fill[otGreen!18] (A) -- (P) -- (Q) -- cycle;"]
    s += [r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle (M) -- (N);"]
    s += [r"\draw[geoTrait%s] (P) -- (Q);" % (",draw=otGreenDark,line width=1.2pt" if corrige else "")]
    s += chevron(M, N, .3) + chevron(Pp, Q, .3) + chevron(B, C, .3)
    s += cote("M", "A", "2 cm", .62) + cote("P", "M", "3 cm", .62) + cote("B", "P", "3 cm", .62)
    s += cote("A", "N", "3 cm", .62)
    s += lseg(M, N, "2,5 cm", -1, t=.62, d=.1)
    if corrige:
        s += cote("B", "A", "8 cm", 1.4) + cote("N", "Q", V % "4,5 cm", .62) + cote("Q", "C", V % "4,5 cm", .62)
        s += cote("A", "C", V % "12 cm", 1.4) + cote("C", "B", "", .5, "otGreenDark")
        s += [r"\node[lab,anchor=north] at %s {%s};" % (P(((B[0] + C[0]) / 2, -.6)), V % "10 cm")]
        s += lseg(Pp, Q, V % "6,25 cm", -1, t=.62, d=.1, coul="otGreenDark")
    ag = math.degrees(math.atan2(A[1] - B[1], A[0] - B[0])) + 135
    ad = math.degrees(math.atan2(C[1] - A[1], C[0] - A[0])) + 45
    s += pt(A, "A", 90) + pt(B, "B", 200) + pt(C, "C", 340)
    s += pt(M, "M", ag, d=.17) + pt(N, "N", ad, d=.17) + pt(Pp, "P", ag, d=.17) + pt(Q, "Q", ad, d=.17)
    return figure(s)


FIGURES["ex3638_enonce"] = deux_paralleles(False)
FIGURES["ex3638_corrige"] = deux_paralleles(True)


# ---------------------------------------------------------------- 3639 : toit
def toit(corrige):
    U = .62
    A, B, C = tri(6, 6, 9, U)
    r = 1 / 3
    M, N = lerp(A, B, r), lerp(A, C, r)
    H = ((B[0] + C[0]) / 2, 0)
    K = ((M[0] + N[0]) / 2, M[1])
    murs = [r"\fill[otMuted!12] %s rectangle %s;" % (P((B[0], -1.3)), P((C[0], 0))),
            r"\draw[otMuted,line width=.8pt] %s -- %s %s -- %s;" % (P(B), P((B[0], -1.3)), P(C), P((C[0], -1.3)))]
    L = {"AM": "2 m", "AB": "6 m", "AC": "6 m", "BC": "9 m"}
    apres = []
    if corrige:
        L.update({"MN": V % "3 m", "AN": V % "2 m"})
        apres = [r"\draw[otGreenDark,line width=.75pt,dash pattern=on 3pt off 2pt] %s -- %s;" % (P(A), P(H))]
        apres += angle_droit(H, C, A, .18, "otGreenDark")
        apres += pt(H, "H", 135, "otGreenDark", d=.15) + pt(K, "K", 305, "otGreenDark", d=.15)
        apres += [r"\node[lab,anchor=west] at %s {%s};" % (P((H[0] + .1, .62)), V % r"$\approx 2{,}65$ m")]
    return emb("ex3639_%s" % corrige, A, B, C, r, L, petit=corrige, paires=corrige,
               vert=("MN", "AN"), avant=murs, apres=apres, forme=(6, 6, 9),
               t_mn=.3 if corrige else .62, t_chev=.75 if corrige else .3, mn_dessus=False)


FIGURES["ex3639_enonce"] = toit(False)
FIGURES["ex3639_corrige"] = toit(True)

# ---------------------------------------------------------------- 3640 : MB 4, AN 3, NC 6, x
A, B, C = tri(6, 9, 7.5, .6)
F3640 = (6, 9, 7.5)
FIGURES["ex3640_enonce"] = emb("ex3640_enonce", A, B, C, 1 / 3,
                               {"AM": "$x$", "MB": "4 cm", "AN": "3 cm", "NC": "6 cm"}, forme=F3640)
FIGURES["ex3640_corrige"] = emb("ex3640_corrige", A, B, C, 1 / 3,
                                {"AM": "$x = 2$ cm", "MB": "4 cm", "AB": "6 cm", "AN": "3 cm", "NC": "6 cm",
                                 "AC": "9 cm", "MN": "2,5 cm", "BC": "7,5 cm"},
                                paires=True, vert=("AM", "AB", "BC"), petit=True, forme=F3640, niv2=1.7)

# ---------------------------------------------------------------- 3641 : AM 3, MB 2, AC 7,5, BC 8
A, B, C = tri(5, 7.5, 8, .7)
F3641 = (5, 7.5, 8)
FIGURES["ex3641_enonce"] = emb("ex3641_enonce", A, B, C, .6,
                               {"AM": "3 cm", "MB": "2 cm", "AC": "7,5 cm", "BC": "8 cm"}, forme=F3641)
FIGURES["ex3641_corrige"] = emb("ex3641_corrige", A, B, C, .6,
                                {"AM": "3 cm", "MB": "2 cm", "AB": "5 cm", "AN": "4,5 cm", "NC": "3 cm",
                                 "AC": "7,5 cm", "MN": "4,8 cm", "BC": "8 cm"},
                                paires=True, vert=("AB", "AN", "NC", "MN"), petit=True, forme=F3641)


# ---------------------------------------------------------------- 3642 : rectangle en B
def rectangle_B(corrige):
    U = .58
    A, B, C = (0, 8 * U), (0, 0), (6 * U, 0)
    r = .25
    L = {"AM": "2 cm", "AB": "8 cm", "BC": "6 cm"}
    if corrige:
        L.update({"AC": V % "10 cm", "AN": V % "2,5 cm", "MN": V % "1,5 cm"})
    M = lerp(A, B, r)
    apres = angle_droit(B, A, C, .2)
    if corrige:
        apres += angle_droit(M, A, lerp(A, C, r), .17, "otGreenDark")
    return emb("ex3642_%s" % corrige, A, B, C, r, L, paires=corrige, petit=corrige, vert=("AC", "AN", "MN"),
               apres=apres, pn={"A": 90, "B": 225, "C": 315}, forme=(8, 10, 6),
               t_mn=.58, t_chev=.62, d_mn=.24)


FIGURES["ex3642_enonce"] = rectangle_B(False)
FIGURES["ex3642_corrige"] = rectangle_B(True)


# ---------------------------------------------------------------- 3643 : visée
def visee(corrige):
    U = .3
    O, H, B = (0, 0), (4 * U, 0), (20 * U, 0)
    T, S = (4 * U, 1.8 * U), (20 * U, 9 * U)
    CONTROLES["ex3643_%s" % corrige] = (O, B, S, H, T, {"r": 4 / 20})
    s = coord(O=O, H=H, B=B, T=T, S=S)
    s += [r"\fill[otSky] (O) -- (B) -- (S) -- cycle;"]
    if corrige:
        s += [r"\fill[otGreen!18] (O) -- (H) -- (T) -- cycle;"]
    s += [r"\draw[sol] (-.4,0) -- %s;" % P((B[0] + .6, 0))]
    s += [r"\draw[rayon] (O) -- (S);"]
    cb = PB if corrige else "otNavy"
    s += [r"\draw[%s,line width=2pt] (H) -- (T);" % cb, r"\draw[%s,line width=2.6pt] (B) -- (S);" % cb]
    s += angle_droit(H, (H[0] - 1, 0), T, .15) + angle_droit(B, (B[0] - 1, 0), S, .2)
    ca = PA if corrige else None
    s += cote("H", "O", "4 m", .6, ca) + cote("B", "O", "20 m", 1.25, ca)
    s += [r"\node[lab,anchor=west] at %s {\textcolor{otMuted}{\otMedium\fontsize{9}{11}\selectfont Hugo :} 1,8 m};"
          % P((T[0] + .12, T[1] * .45))]
    s += lab((S[0], S[1] * .5), V % "9 m" if corrige else "?", 0, d=.18)
    if corrige:
        s += [r"\node[lab,anchor=south east] at (.9,1.0) {%s};" % (V % r"$OT \approx 4{,}39$ m")]
    else:
        s += [r"\node[txt,text=otOrange!80!black,anchor=south east] at %s {ligne de visée};"
              % P((S[0] * .55 - .1, S[1] * .55 + .1))]
    s += [r"\node[txt,text=otMuted,anchor=west] at %s {arbre};" % P((S[0] + .2, S[1] - .05)),
          r"\node[txt,text=otMuted,anchor=north east] at (-.15,-.12) {œil de Lina};"]
    s += pt(O, "O", 120, d=.15) + pt(H, "H", 315, d=.13) + pt(B, "B", 315, d=.13)
    s += pt(T, "T", 125, d=.14) + pt(S, "S", 125, d=.14)
    return figure(s)


FIGURES["ex3643_enonce"] = visee(False)
FIGURES["ex3643_corrige"] = visee(True)

# ---------------------------------------------------------------- 3644 : plan au 1/1 000
A, B, C = tri(7.5, 9, 6, .62)
F3644 = (7.5, 9, 6)
cadre = [r"\draw[otMuted!70,line width=.5pt] %s rectangle %s;" % (P((-1.75, -1.2)), P((5.6, 5.5))),
         r"\node[txt,text=otMuted,anchor=south west] at (-1.75,5.62) {Plan au $\frac{1}{1\,000}$};"]
FIGURES["ex3644_enonce"] = emb("ex3644_enonce", A, B, C, .4,
                               {"AM": "3 cm", "MB": "4,5 cm", "AC": "9 cm", "BC": "6 cm"}, forme=F3644,
                               avant=cadre)
FIGURES["ex3644_corrige"] = emb("ex3644_corrige", A, B, C, .4,
                                {"AM": "3 cm", "MB": "4,5 cm", "AB": "7,5 cm", "AN": "3,6 cm", "AC": "9 cm",
                                 "BC": "6 cm", "MN": "2,4 cm"},
                                paires=True, vert=("AB", "AN", "MN"), petit=True, forme=F3644,
                                avant=cadre)


# ---------------------------------------------------------------- 3645 : étang
def etang(corrige):
    U = .1
    A, B, C = tri(48, 52, 60, U)
    r = .25
    M, N = lerp(A, B, r), lerp(A, C, r)
    cx = (B[0] + C[0]) / 2
    av = [r"\fill[otBleu!22] (%s,0) ellipse (%scm and .62cm);" % (f(cx), f((C[0] - B[0]) / 2))]
    ap = [r"\draw[otBleu!70,line width=.6pt] (%s,0) ellipse (%scm and .62cm);" % (f(cx), f((C[0] - B[0]) / 2)),
          r"\node[txt,text=otBleu!80!black,anchor=north] at (%s,-.18) {étang};" % f(cx)]
    L = {"AM": "12 m", "MB": "36 m", "AN": "13 m", "MN": "15 m"}
    if corrige:
        L.update({"AB": "48 m", "NC": V % "39 m", "AC": V % "52 m"})
        ap += lseg(B, C, V % "60 m", 1, t=.5, d=.12)
    return emb("ex3645_%s" % corrige, A, B, C, r, L, paires=corrige, petit=corrige, vert=("NC", "AC"),
               avant=av, apres=ap, forme=(48, 52, 60))


FIGURES["ex3645_enonce"] = etang(False)
FIGURES["ex3645_corrige"] = etang(True)


# ---------------------------------------------------------------- 3646 : rectangle inscrit (x = 3)
def rect_inscrit(corrige):
    u = .5
    B, C, H, A = (0, 0), (12 * u, 0), (5 * u, 0), (5 * u, 8 * u)
    x = 3
    k = (8 - x) / 8
    M, N = lerp(A, B, k), lerp(A, C, k)
    K = (H[0], x * u)
    Q, Pp = (M[0], 0), (N[0], 0)
    CONTROLES["ex3646_%s" % corrige] = (A, B, C, M, N, {"r": k})
    s = coord(A=A, B=B, C=C, M=M, N=N, H=H, K=K, Q=Q, P=Pp)
    s += [r"\fill[otSky] (A) -- (B) -- (C) -- cycle;",
          r"\fill[%s] (M) -- (N) -- (P) -- (Q) -- cycle;" % ("otGreen!22" if corrige else "otOrange!14")]
    s += [r"\draw[geoTrait] (A) -- (B) -- (C) -- cycle;",
          r"\draw[%s,line width=1.1pt] (M) -- (N) -- (P) -- (Q) -- cycle;" % ("otGreenDark" if corrige else "otOrange!90!black"),
          r"\draw[otMuted,line width=.7pt,dash pattern=on 3pt off 2pt] (A) -- (H);"]
    s += angle_droit(H, C, A, .18) + angle_droit(Q, M, Pp, .16) + angle_droit(Pp, C, N, .16)
    s += cote("C", "B", "12 cm", .62)
    s += [r"\draw[cote] %s -- %s node[midway,coteTexte]{8 cm};" % (P((-.55, A[1])), P((-.55, 0))),
          r"\draw[otMuted!70,line width=.4pt] %s -- %s %s -- %s;" % (P((-.62, A[1])), P((A[0] - .1, A[1])), P((-.62, 0)), P((-.1, 0)))]
    s += lab(((N[0] + Pp[0]) / 2, x * u / 2), V % "$x = 3$" if corrige else "$x$", 0, d=.12,
             coul="otGreenDark" if corrige else "otOrange!80!black")
    if corrige:
        s += [r"\node[lab,anchor=south] at %s {%s};" % (P(((M[0] + N[0]) / 2 + .9, M[1] + .08)), V % "7,5 cm")]
        s += [r"\node[lab,anchor=east] at %s {%s};" % (P((H[0] - .1, (A[1] + K[1]) / 2)), V % "5 cm")]
    s += pt(A, "A", 90) + pt(B, "B", 200) + pt(C, "C", 340) + pt(M, "M", 165, d=.15) + pt(N, "N", 15, d=.15)
    s += pt(H, "H", 270, d=.15) + pt(Q, "Q", 270, d=.15) + pt(Pp, "P", 270, d=.15) + pt(K, "K", 45, d=.14)
    return figure(s)


FIGURES["ex3646_enonce"] = rect_inscrit(False)
FIGURES["ex3646_corrige"] = rect_inscrit(True)


# ---------------------------------------------------------------- 3647 : escabeau
def escabeau(corrige):
    U = 1.9
    A, B, C = tri(2, 2, 1.6, U)
    r = .25
    N = lerp(A, C, r)
    H = ((B[0] + C[0]) / 2, 0)
    xh = C[0] + .75   # cote verticale de la hauteur, à droite
    av = [r"\draw[sol] %s -- %s;" % (P((B[0] - .6, 0)), P((C[0] + 1.0, 0)))]
    ap = [r"\draw[otNavy,line width=2.4pt] (A) -- (B) (A) -- (C);"]
    ap += [r"\node[lab,anchor=west,text=%s] at %s {0,4 m};" % (PC if corrige else "otInk", P((N[0] + .3, N[1] - .12)))]
    L = {"AM": "0,5 m", "AB": "2 m"}
    if corrige:
        L["BC"] = V % "1,6 m"
        ap = [r"\coordinate (H) at %s; \coordinate (h0) at %s; \coordinate (h1) at %s;"
              % (P(H), P((xh, 0)), P((xh, A[1])))] + ap
        ap += [r"\draw[otGreenDark,line width=.75pt,dash pattern=on 3pt off 2pt] (A) -- (H);",
               r"\draw[otMuted!70,line width=.4pt] %s -- %s;" % (P((A[0] + .2, A[1])), P((xh + .1, A[1]))),
               r"\draw[cote,otGreenDark] (h0) -- (h1) node[midway,coteTexte]{%s};" % (V % r"$\approx 1{,}83$ m")]
        ap += angle_droit(H, C, A, .18, "otGreenDark") + pt(H, "H", 150, "otGreenDark", d=.15)
    return emb("ex3647_%s" % corrige, A, B, C, r, L, paires=corrige, petit=corrige, vert=("BC",),
               avant=av, apres=ap, forme=(2, 2, 1.6), t_chev=.3, off_bc=.5,
               pn={"A": 90, "B": 225, "C": 315, "N": 45})


FIGURES["ex3647_enonce"] = escabeau(False)
FIGURES["ex3647_corrige"] = escabeau(True)


# ---------------------------------------------------------------- 3648 : rampe (échelle verticale × 5)
def rampe(corrige):
    ux, uy = .5, 2.5   # 1 m horizontal = 0,5 cm ; 1 m vertical = 2,5 cm (pente exagérée)
    A, C, B = (0, 0), (12 * ux, 0), (12 * ux, .6 * uy)
    s = coord(A=A, C=C, D=(3 * ux, 0), E=(6 * ux, 0), F=(9 * ux, 0))
    # mur et porte (seuil au niveau de B)
    s += [r"\fill[otMuted!12] %s rectangle %s;" % (P((C[0], 0)), P((C[0] + .8, 3.1))),
          r"\draw[otMuted,line width=.8pt] %s -- %s;" % (P(C), P((C[0], 3.1))),
          r"\draw[otMuted,line width=.6pt,fill=white] %s rectangle %s;" % (P((C[0] + .12, B[1])), P((C[0] + .68, 3.0))),
          r"\node[txt,text=otMuted,rotate=90] at %s {porte};" % P((C[0] + .4, (B[1] + 3.0) / 2))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(C), P(B))]
    s += [r"\draw[sol] (-.5,0) -- %s;" % P((C[0] + .8, 0))]
    s += [r"\draw[geoTrait] %s -- %s;" % (P(A), P(B))]
    cb = PB if corrige else "otNavy"
    hauts = []
    for d_, n1, n2, h in ((3, "D", "R", .15), (6, "E", "S", .3), (9, "F", "T", .45)):
        X, Y = (d_ * ux, 0), (d_ * ux, h * uy)
        CONTROLES["ex3648_%s_%s" % (corrige, n2)] = (A, C, B, X, Y, {"r": d_ / 12})
        s += [r"\draw[%s,line width=1.6pt] %s -- %s;" % (cb, P(X), P(Y))]
        s += angle_droit(X, (X[0] - 1, 0), Y, .13)
        s += pt(X, n1, 315, d=.13) + pt(Y, n2, 120, d=.15)
        hauts.append((X, Y, h))
    s += [r"\draw[%s,line width=1.6pt] %s -- %s;" % (cb, P(C), P(B))]
    s += angle_droit(C, (C[0] - 1, 0), B, .15)
    s += pt(A, "A", 135, d=.15) + pt(C, "C", 315, d=.13) + pt(B, "B", 135, d=.15)
    s += [r"\node[lab,anchor=west] at %s {0,6 m};" % P((C[0] + .1, B[1] * .5))]
    ca = PA if corrige else None
    s += cote("D", "A", "3 m", .7, ca) + cote("E", "D", "3 m", .7) + cote("F", "E", "3 m", .7)
    s += cote("C", "F", "3 m", .7) + cote("C", "A", "12 m", 1.35, ca)
    if corrige:
        for X, Y, h in hauts:
            s += [r"\node[lab,anchor=west] at %s {%s};" % (P((X[0] + .1, Y[1] * .5 + .02)),
                                                           V % ("%s m" % f(h).replace(".", "{,}")))]
    s += [r"\node[txt,text=otMuted,anchor=north] at %s {échelle verticale exagérée};" % P((C[0] / 2, -1.75))]
    return figure(s)


FIGURES["ex3648_enonce"] = rampe(False)
FIGURES["ex3648_corrige"] = rampe(True)


# ---------------------------------------------------------------- 3649 : rivière
def riviere(corrige):
    u = .15
    A, M, B = (0, 32 * u), (0, 8 * u), (0, 0)
    N, C = (15 * u, 8 * u), (20 * u, 0)
    CONTROLES["ex3649_%s" % corrige] = (A, B, C, M, N, {"r": 24 / 32})
    xd = C[0] + .9
    s = coord(A=A, M=M, B=B, N=N, C=C)
    s += [r"\fill[otBleu!18] %s rectangle %s;" % (P((-1.5, M[1])), P((xd, A[1])))]
    s += [r"\draw[otBleu!70,line width=.6pt] %s -- %s %s -- %s;" % (P((-1.5, M[1])), P((xd, M[1])),
                                                                 P((-1.5, A[1])), P((xd, A[1])))]
    s += [r"\node[txt,text=otBleu!80!black,anchor=west] at %s {rivière};" % P((1.35, 3.1))]
    s += [r"\node[txt,text=otMuted,anchor=south east] at %s {autre rive};" % P((xd, A[1] + .08)),
          r"\node[txt,text=otMuted,anchor=north west] at %s {rive d'Inès};" % P((C[0] - .2, M[1] - .1)),
          r"\node[txt,text=otMuted,anchor=south east] at %s {arbre};" % P((-.15, A[1] + .08))]
    if corrige:
        s += [r"\fill[otGreen!25] (A) -- (M) -- (N) -- cycle;"]
    cb = PC if corrige else "otNavy"
    s += [r"\draw[geoTrait] (A) -- (B) (A) -- (C);",
          r"\draw[geoTrait%s] (M) -- (N);" % ((",draw=%s,line width=1.3pt" % cb) if corrige else ""),
          r"\draw[geoTrait%s] (B) -- (C);" % ((",draw=%s,line width=1.3pt" % cb) if corrige else "")]
    s += chevron(M, N, .3, cb) + chevron(B, C, .3, cb)
    s += angle_droit(M, A, N, .17) + angle_droit(B, A, C, .17)
    ca = PA if corrige else None
    s += cote("M", "A", V % "$x = 24$ m" if corrige else "$x$", .6, ca)
    s += cote("B", "M", "8 m", .6)
    if corrige:
        s += cote("B", "A", V % "32 m", 1.35, ca)
    s += lseg(M, N, "15 m", -1, t=.6, d=.1, coul=PC if corrige else "otInk")
    s += lseg(B, C, "20 m", -1, t=.6, d=.1, coul=PC if corrige else "otInk")
    s += pt(A, "A", 45, d=.15) + pt(M, "M", 225, d=.13) + pt(B, "B", 225, d=.13)
    s += pt(N, "N", 60, d=.15) + pt(C, "C", 0, d=.15)
    return figure(s)


FIGURES["ex3649_enonce"] = riviere(False)
FIGURES["ex3649_corrige"] = riviere(True)


