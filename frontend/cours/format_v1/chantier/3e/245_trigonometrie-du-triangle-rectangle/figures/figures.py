# -*- coding: utf-8 -*-
"""Figures de la notion « Trigonométrie du triangle rectangle » (3e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données ; vert foncé = éléments
de réponse (corrigés) : nom du côté (hypoténuse, adjacent, opposé), résultats, côtés
utilisés. Les étiquettes de côtés sont placées automatiquement à l'extérieur du triangle ;
l'angle marqué est un arc avec sa mesure dans l'angle.
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  lab/.style={text=otInk,inner sep=0pt,align=center},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt},
  aide/.style={otMuted,line width=.7pt,dash pattern=on 3.5pt off 2pt},
}
\newcommand{\rl}{\otMedium\fontsize{8.5}{10}\selectfont\color{otGreenDark}}
"""

V = r"\textcolor{otGreenDark}{%s}"
ROLE = {"hyp": "hypoténuse", "adj": "côté adjacent", "opp": "côté opposé"}


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


def pt(p, nom, ang, coul="otNavy", d=.14):
    a = math.radians(ang)
    q = (p[0] + d * math.cos(a), p[1] + d * math.sin(a))
    s = [r"\fill[%s] %s circle (2.1pt);" % (coul, P(p))]
    if nom:
        s.append(r"\node[lab,anchor=%d] at %s {$%s$};" % ((ang + 180) % 360, P(q), nom))
    return s


def lab(p, txt, ang, d=.13):
    a = math.radians(ang)
    q = (p[0] + d * math.cos(a), p[1] + d * math.sin(a))
    return [r"\node[lab,anchor=%d] at %s {%s};" % ((ang + 180) % 360, P(q), txt)]


def lseg(p, q, txt, cote=1, t=.5, d=.14):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * cote, dx / L * cote
    m = (p[0] + t * dx + d * nx, p[1] + t * dy + d * ny)
    ang = math.degrees(math.atan2(ny, nx))
    noms = ["east", "north east", "north", "north west", "west", "south west", "south", "south east"]
    anc = noms[int(round(((ang + 180) % 360) / 45)) % 8]
    return [r"\node[lab,anchor=%s] at %s {%s};" % (anc, P(m), txt)]


def ext(p, q, r):
    """cote (1 ou -1) qui place une étiquette de [pq] du côté opposé à r."""
    cr = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return -1 if cr > 0 else 1


def figure(corps):
    return "\n".join([r"\begin{tikzpicture}[line cap=round]"] + corps + [r"\end{tikzpicture}"])


def angle_droit(p, sommet, q, coul="otNavy", r=.22):
    def u(a, b):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        return ((b[0] - a[0]) / L * r, (b[1] - a[1]) / L * r)
    a, b = u(sommet, p), u(sommet, q)
    p1 = (sommet[0] + a[0], sommet[1] + a[1])
    p2 = (sommet[0] + a[0] + b[0], sommet[1] + a[1] + b[1])
    p3 = (sommet[0] + b[0], sommet[1] + b[1])
    return [r"\draw[%s,line width=.6pt] %s -- %s -- %s;" % (coul, P(p1), P(p2), P(p3))]


def arc(S, p, q, txt=None, coul="otNavy", r=.55, dl=None):
    """Arc de l'angle de sommet S entre les directions S->p et S->q, mesure dans l'angle."""
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
        d = dl or max(r + .34, .36 / math.sin(half)) + (.3 if "approx" in txt else 0)
        m = (S[0] + d * math.cos(mid), S[1] + d * math.sin(mid))
        s.append(r"\node[lab,text=%s] at %s {%s};" % ("otInk" if coul == "otNavy" else coul, P(m), txt))
    return s


def tri(noms, adj, opp, U, ang=None, cotes=None, vert=(), roles=False, traits=(), miroir=False,
        ang_vert=False, noms_ang=None, arc_r=.55, dl=None, droit_vert=False):
    """Triangle rectangle : noms = (sommet de l'angle marqué, sommet de l'angle droit, troisième).

    Le côté adjacent est horizontal, le côté opposé vertical. cotes : {"adj"|"opp"|"hyp": texte} ;
    vert : clés écrites en vert ; roles : nom du côté (en vert) sous chaque cote ;
    traits : côtés tracés en vert.
    """
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
    s += angle_droit(pts[0], pts[1], pts[2], "otGreenDark" if droit_vert else "otNavy")
    if ang is not None:
        s += arc(pts[0], pts[1], pts[2], (V % ang) if ang_vert else ang, "otGreenDark" if ang_vert else "otNavy",
                 r=arc_r, dl=dl)
    for k in ("adj", "opp", "hyp"):
        txt = cotes.get(k)
        if txt is not None and k in vert:
            txt = V % txt
        if roles:
            rl = r"{\rl %s}" % ROLE[k]
            txt = (txt + r"\\" + rl) if txt else rl
        if txt:
            i, j = idx[k]
            c = ext(pts[i], pts[j], pts[3 - i - j])
            s += lseg(pts[i], pts[j], txt, c)
    for k in range(3):
        a = noms_ang[k] if noms_ang else math.degrees(math.atan2(pts[k][1] - G[1], pts[k][0] - G[0]))
        s += pt(pts[k], noms[k], a)
    return s


FIGURES = {}
TOLERE = {}

# ================================================================== COURS
# ABC rectangle en A : A en bas à gauche, B en bas à droite, C en haut à gauche
UA = .62
A0, B0, C0 = (0, 0), (7 * UA, 0), (0, 4.4 * UA)


def vocab(angle, roles=True):
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A0), P(B0), P(C0)),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A0), P(B0), P(C0))]
    s += angle_droit(B0, A0, C0)
    if angle == "B":
        s += arc(B0, A0, C0, None if not roles else None)
        if roles:
            s += [r"\draw[geoReponse,line width=1.5pt] %s -- %s;" % (P(A0), P(B0))]
            s += lseg(A0, B0, r"{\rl côté adjacent à $\widehat{ABC}$}", -1)
            s += lseg(A0, C0, r"{\rl côté opposé}\\{\rl à $\widehat{ABC}$}", 1)
            s += lseg(B0, C0, r"{\rl hypoténuse}", ext(B0, C0, A0))
    elif angle == "C":
        s += arc(C0, A0, B0)
        if roles:
            s += [r"\draw[geoReponse,line width=1.5pt] %s -- %s;" % (P(A0), P(C0))]
            s += lseg(A0, B0, r"{\rl côté opposé à $\widehat{ACB}$}", -1)
            s += lseg(A0, C0, r"{\rl côté adjacent}\\{\rl à $\widehat{ACB}$}", 1)
            s += lseg(B0, C0, r"{\rl hypoténuse}", ext(B0, C0, A0))
    s += pt(A0, "A", 225, d=.16) + pt(B0, "B", 315) + pt(C0, "C", 135)
    return figure(s)


FIGURES["cours_vocab_b"] = vocab("B")
FIGURES["cours_vocab_c"] = vocab("C")
FIGURES["ex2380_enonce"] = vocab(None, roles=False)


def sol(x0, x1, y=0):
    return [r"\fill[otRule!60] %s rectangle %s;" % (P((x0, y - .16)), P((x1, y))),
            r"\draw[otMuted,line width=.8pt] %s -- %s;" % (P((x0, y)), P((x1, y)))]


# observateur et arbre (cours) : yeux à 1,5 m, 20 m, 40°
def arbre():
    e, W, h = .85, 4.6, 4.6 * math.tan(math.radians(40))
    O, H, T = (0, e), (W, e), (W, e + h)
    s = sol(-1.1, W + 1.1)
    s += [r"\fill[otMuted!55] %s rectangle %s;" % (P((W - .09, 0)), P((W + .09, T[1] - 1.0))),
          r"\fill[otGreen!28] %s circle (.62);" % P((W, T[1] - .62))]
    s += [r"\draw[otMuted,line width=2.2pt] (0,0) -- %s;" % P((0, e - .1))]
    s += [r"\fill[otSky,opacity=.7] %s -- %s -- %s -- cycle;" % (P(O), P(H), P(T))]
    s += [r"\draw[aide] %s -- %s;" % (P(O), P(H)), r"\draw[aide] %s -- %s;" % (P(H), P(T)),
          r"\draw[geoTrait] %s -- %s;" % (P(O), P(T))]
    s += angle_droit(O, H, T)
    s += arc(O, H, T, r"$40^\circ$", r=.7)
    s += [r"\node[lab,anchor=north] at %s {20 m};" % P((W / 2, -.28)),
          r"\node[lab,anchor=east] at %s {1,5 m};" % P((-.2, e / 2)),
          r"\node[lab,anchor=east] at %s {%s};" % (P((W - .18, e + h * .55)), V % "$h$")]
    s += [r"\fill[otNavy] %s circle (2.1pt);" % P(O), r"\fill[otNavy] %s circle (2.1pt);" % P(T)]
    s += [r"\node[txt,text=otMuted,anchor=south] at %s {regard};" % P((W * .32 - .25, e + h * .32 + .25))]
    return figure(s)


FIGURES["cours_arbre"] = arbre()

# ================================================================== EXERCICES
# 2381 : DEF rectangle en E, DE = 8, EF = 6, DF = 10
FIGURES["ex2381_enonce"] = figure(tri("DEF", 8, 6, .6, ang="", cotes={"adj": "8 cm", "opp": "6 cm", "hyp": "10 cm"}))
FIGURES["ex2381_corrige"] = figure(tri("DEF", 8, 6, .6, ang=r"$\approx 37^\circ$", ang_vert=True,
                                       cotes={"adj": "8 cm", "opp": "6 cm", "hyp": "10 cm"}, roles=True))

# 2382 : ABC rectangle en A, B = 40°, BC = 8
c40, s40 = 8 * math.cos(math.radians(40)), 8 * math.sin(math.radians(40))
FIGURES["ex2382_enonce"] = figure(tri("BAC", c40, s40, .72, ang=r"$40^\circ$", cotes={"hyp": "8 cm"}, miroir=True))
FIGURES["ex2382_corrige"] = figure(tri("BAC", c40, s40, .72, ang=r"$40^\circ$", miroir=True, roles=True,
                                       cotes={"hyp": "8 cm", "opp": r"$\approx 5{,}1$ cm", "adj": r"$\approx 6{,}1$ cm"},
                                       vert=("opp", "adj"), traits=("opp", "adj")))

# 2383 : EFG rectangle en F, E = 52°, EG = 7,5
c52, s52 = 7.5 * math.cos(math.radians(52)), 7.5 * math.sin(math.radians(52))
FIGURES["ex2383_enonce"] = figure(tri("EFG", c52, s52, .7, ang=r"$52^\circ$", cotes={"hyp": "7,5 cm"}))
FIGURES["ex2383_corrige"] = figure(tri("EFG", c52, s52, .7, ang=r"$52^\circ$", roles=True,
                                       cotes={"hyp": "7,5 cm", "adj": r"$\approx 4{,}6$ cm", "opp": r"$\approx 5{,}9$ cm"},
                                       vert=("adj", "opp"), traits=("adj", "opp")))

# 2384 : KLM rectangle en K, L = 34°, KL = 6
t34 = 6 * math.tan(math.radians(34))
FIGURES["ex2384_enonce"] = figure(tri("LKM", 6, t34, .72, ang=r"$34^\circ$", cotes={"adj": "6 cm"}, miroir=True))
FIGURES["ex2384_corrige"] = figure(tri("LKM", 6, t34, .72, ang=r"$34^\circ$", miroir=True, roles=True,
                                       cotes={"adj": "6 cm", "hyp": r"$\approx 7{,}2$ cm", "opp": r"$\approx 4{,}0$ cm"},
                                       vert=("hyp", "opp"), traits=("hyp", "opp")))

# 2385 : IJK rectangle en J, IJ = 5, IK = 8
o85 = math.sqrt(64 - 25)
FIGURES["ex2385_enonce"] = figure(tri("IJK", 5, o85, .6, ang="", cotes={"adj": "5 cm", "hyp": "8 cm"}))
FIGURES["ex2385_corrige"] = figure(tri("IJK", 5, o85, .6, ang=r"$\approx 51^\circ$", ang_vert=True, roles=True,
                                       cotes={"adj": "5 cm", "hyp": "8 cm"}, traits=("adj", "hyp")))

# 2386 : RST rectangle en S, R = 28°
t28 = 7 * math.tan(math.radians(28))
FIGURES["ex2386_enonce"] = figure(tri("RST", 7, t28, .8, ang=r"$28^\circ$"))
FIGURES["ex2386_corrige"] = figure(tri("RST", 7, t28, .8, ang=r"$28^\circ$", roles=True))

# 2387 : ABC rectangle en A, AB = 7, AC = 4,5
FIGURES["ex2387_enonce"] = figure(tri("BAC", 7, 4.5, .7, ang="", cotes={"adj": "7 cm", "opp": "4,5 cm"}, miroir=True))
FIGURES["ex2387_corrige"] = figure(tri("BAC", 7, 4.5, .7, ang=r"$\approx 32{,}7^\circ$", ang_vert=True, miroir=True,
                                       roles=True, cotes={"adj": "7 cm", "opp": "4,5 cm", "hyp": r"$\approx 8{,}3$ cm"},
                                       vert=("hyp",), traits=("adj", "opp")))

# 2388 : ABC rectangle en A, AB = 5, C = 25°
a25 = 5 / math.tan(math.radians(25))
FIGURES["ex2388_enonce"] = figure(tri("CAB", a25, 5, .52, ang=r"$25^\circ$", cotes={"opp": "5 cm"}))
FIGURES["ex2388_corrige"] = figure(tri("CAB", a25, 5, .52, ang=r"$25^\circ$", roles=True,
                                       cotes={"opp": "5 cm", "hyp": r"$\approx 11{,}8$ cm", "adj": r"$\approx 10{,}7$ cm"},
                                       vert=("hyp", "adj"), traits=("hyp", "adj")))

# 2390 : ABC rectangle en A, AB = 6, B = 40°
o40 = 6 * math.tan(math.radians(40))
FIGURES["ex2390_enonce"] = figure(tri("BAC", 6, o40, .7, ang=r"$40^\circ$", cotes={"adj": "6 cm", "hyp": "?"}, miroir=True))
FIGURES["ex2390_corrige"] = figure(tri("BAC", 6, o40, .7, ang=r"$40^\circ$", miroir=True, roles=True,
                                       cotes={"adj": "6 cm", "hyp": r"$\approx 7{,}8$ cm"}, vert=("hyp",),
                                       traits=("adj", "hyp")))


# 2389 : échelle de 6 m contre un mur, 70°
def echelle(corrige, pied=None):
    U = .72
    a = math.radians(70)
    Fp, T, A = (6 * math.cos(a) * U, 0), (0, 6 * math.sin(a) * U), (0, 0)
    s = [r"\fill[otMuted!22] %s rectangle %s;" % (P((-.45, 0)), P((0, T[1] + .55))),
         r"\draw[otMuted,line width=.8pt] (0,0) -- %s;" % P((0, T[1] + .55))]
    s += sol(-.45, Fp[0] + 1.6)
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(Fp), P(T))]
    s += [r"\draw[otOrange!90!black,line width=2.4pt] %s -- %s;" % (P(Fp), P(T))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(A), P(T)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(A), Fp and P(Fp))]
    s += angle_droit(Fp, A, T)
    s += arc(Fp, A, T, r"$70^\circ$", r=.5)
    txt = "6 m" + (r"\\{\rl hypoténuse}" if corrige else "")
    s += lseg(Fp, T, txt, -1, d=.2)
    if corrige:
        s += [r"\node[lab,anchor=east] at %s {%s\\{\rl côté opposé}};" % (P((-.6, T[1] / 2)), V % r"$h \approx 5{,}64$ m"),
              r"\node[lab,anchor=north] at %s {%s\\{\rl côté adjacent}};" % (P((Fp[0] / 2 + .25, -.3)), V % r"$d \approx 2{,}05$ m")]
    else:
        s += [r"\node[txt,text=otMuted,anchor=east] at %s {mur};" % P((-.6, T[1] / 2)),
              r"\node[txt,text=otMuted,anchor=north] at %s {sol};" % P((Fp[0] + .9, -.3))]
    return figure(s)


FIGURES["ex2389_enonce"] = echelle(False)
FIGURES["ex2389_corrige"] = echelle(True)


# 2391 : rampe, 4 m à l'horizontale, 3° (schéma sans échelle)
def rampe(corrige):
    W, H = 5.6, 1.25
    O, R, Q = (0, 0), (W, 0), (W, H)
    s = sol(-.6, W, 0)
    s += [r"\fill[otMuted!22] %s rectangle %s;" % (P(R), P((W + 1.9, H))),
          r"\draw[otMuted,line width=.8pt] %s -- %s -- %s;" % (P(R), P(Q), P((W + 1.9, H))),
          r"\draw[otMuted,line width=.8pt] %s -- %s;" % (P(R), P((W + 1.9, 0)))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(O), P(R), P(Q))]
    s += [r"\draw[otOrange!90!black,line width=2.4pt] %s -- %s;" % (P(O), P(Q))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(R), P(Q))]
    s += angle_droit(O, R, Q)
    s += arc(O, R, Q, r"$3^\circ$", r=1.3, dl=2.3)
    s += [r"\node[lab,anchor=north] at %s {%s};" % (P((W / 2, -.3)),
                                                     "4 m" + (r"\\{\rl côté adjacent}" if corrige else ""))]
    if corrige:
        s += [r"\node[lab,anchor=west] at %s {%s\\{\rl côté opposé}};" % (P((W + .15, H / 2)), V % r"$h \approx 0{,}21$ m"),
              r"\node[lab,anchor=south east] at %s {%s\\{\rl hypoténuse}};" % (P((W * .5, H * .5 + .2)), V % r"$L \approx 4{,}01$ m")]
    else:
        s += [r"\node[lab,anchor=west] at %s {$h$};" % P((W + .15, H / 2)),
              r"\node[lab,anchor=south east] at %s {$L$};" % P((W * .5, H * .5 + .15)),
              r"\node[txt,text=otMuted,anchor=south] at %s {entrée};" % P((W + .95, H + .12))]
    return figure(s)


FIGURES["ex2391_enonce"] = rampe(False)
FIGURES["ex2391_corrige"] = rampe(True)


# 2392 : cerf-volant, fil de 35 m à 48°, main à 1,2 m (hauteur de la main exagérée)
def cerf_volant(corrige):
    U, e = .125, .95
    a = math.radians(48)
    M = (0, e)
    H = (35 * math.cos(a) * U, e)
    K = (H[0], e + 35 * math.sin(a) * U)
    s = sol(-.9, H[0] + 1.3)
    s += [r"\draw[otMuted,line width=2.2pt] (0,0) -- %s;" % P((0, e - .08))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(M), P(H), P(K))]
    s += [r"\draw[aide] %s -- %s;" % (P(M), P(H)), r"\draw[aide] %s -- %s;" % (P(H), P(K)),
          r"\draw[aide] %s -- %s;" % (P(H), P((H[0], 0)))]
    s += [r"\draw[otNavy,line width=1pt] %s -- %s;" % (P(M), P(K))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.5pt] %s -- %s;" % (P(H), P(K))]
    kx, ky = K
    s += [r"\fill[otOrange!80] %s -- %s -- %s -- %s -- cycle;" % (P((kx, ky + .32)), P((kx + .2, ky + .05)),
                                                                 P((kx, ky - .22)), P((kx - .2, ky + .05)))]
    s += angle_droit(M, H, K)
    s += arc(M, H, K, r"$48^\circ$", r=.6)
    s += lseg(M, K, "35 m" + (r"\\{\rl hypoténuse}" if corrige else ""), 1, d=.18)
    s += [r"\node[lab,anchor=east] at %s {1,2 m};" % P((-.22, e / 2))]
    if corrige:
        s += [r"\node[lab,anchor=west] at %s {%s\\{\rl côté opposé}};" % (P((H[0] + .2, (e + ky) / 2)), V % r"$h \approx 26{,}01$ m"),
              r"\node[lab,anchor=north] at %s {%s\\{\rl côté adjacent}};" % (P((H[0] / 2, -.3)), V % r"$d \approx 23{,}4$ m")]
    s += pt(M, "", 0)
    return figure(s)


FIGURES["ex2392_enonce"] = cerf_volant(False)
FIGURES["ex2392_corrige"] = cerf_volant(True)


# 2393 : toboggan, piste 4,2 m, hauteur 2,1 m
def toboggan(corrige):
    U = 1.1
    d = 4.2 * math.cos(math.radians(30))
    B, Pp, T = (0, 0), (d * U, 0), (d * U, 2.1 * U)
    s = sol(-.6, Pp[0] + 1.4)
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(B), P(Pp), P(T))]
    s += [r"\draw[otMuted,line width=1.6pt] %s -- %s;" % (P(Pp), P(T)),
          r"\draw[otMuted,line width=1.6pt] %s -- %s;" % (P(T), P((T[0] + .55, T[1])))]
    s += [r"\draw[otOrange!90!black,line width=2.4pt] %s -- %s;" % (P(B), P(T))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(B), P(Pp))]
    s += angle_droit(B, Pp, T)
    s += arc(B, Pp, T, (V % r"$\alpha = 30^\circ$") if corrige else r"$\alpha$", "otGreenDark" if corrige else "otNavy",
             r=.65, dl=1.75 if corrige else None)
    s += lseg(B, T, "4,2 m" + (r"\\{\rl hypoténuse}" if corrige else ""), 1, d=.2)
    s += [r"\node[lab,anchor=west] at %s {%s};" % (P((Pp[0] + .2, T[1] / 2)),
                                                    "2,1 m" + (r"\\{\rl côté opposé}" if corrige else ""))]
    s += [r"\node[lab,anchor=north] at %s {%s};" % (P((Pp[0] / 2, -.3)),
                                                     (V % r"$d \approx 3{,}64$ m" + r"\\{\rl côté adjacent}") if corrige else "$d$")]
    return figure(s)


FIGURES["ex2393_enonce"] = toboggan(False)
FIGURES["ex2393_corrige"] = toboggan(True)


# 2394 : immeuble, 30 m, 38°, yeux à 1,6 m (hauteur des yeux exagérée)
def immeuble(corrige):
    U, e = .13, .8
    W = 30 * U
    hs = 30 * math.tan(math.radians(38)) * U
    O, H, S = (0, e), (W, e), (W, e + hs)
    s = sol(-1.0, W + 1.7)
    s += [r"\fill[otMuted!22] %s rectangle %s;" % (P((W, 0)), P((W + 1.4, S[1]))),
          r"\draw[otMuted,line width=.8pt] %s rectangle %s;" % (P((W, 0)), P((W + 1.4, S[1])))]
    for k in range(int((S[1] - .75) // .95)):
        for j in range(2):
            x0, y0 = W + .25 + j * .55, .55 + k * .95
            s.append(r"\fill[white] %s rectangle %s;" % (P((x0, y0)), P((x0 + .35, y0 + .5))))
    s += [r"\draw[otMuted,line width=2.2pt] (0,0) -- %s;" % P((0, e - .08))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(O), P(H), P(S))]
    s += [r"\draw[aide] %s -- %s;" % (P(O), P(H)), r"\draw[geoTrait] %s -- %s;" % (P(O), P(S))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(H), P(S))]
    s += angle_droit(O, H, S)
    s += arc(O, H, S, r"$38^\circ$", r=.65)
    s += [r"\node[lab,anchor=north] at %s {%s};" % (P((W / 2, -.28)), "30 m" + (r"\\{\rl côté adjacent}" if corrige else "")),
          r"\node[lab,anchor=east] at %s {1,6 m};" % P((-.22, e / 2))]
    if corrige:
        s += [r"\node[lab,anchor=west] at %s {%s\\{\rl côté opposé}};" % (P((W + 1.55, e + hs * .5)), V % r"$HS \approx 23{,}44$ m")]
    s += pt(O, "O", 135) + pt(H, "H", 300, d=.16) + pt(S, "S", 135)
    return figure(s)


FIGURES["ex2394_enonce"] = immeuble(False)
FIGURES["ex2394_corrige"] = immeuble(True)


# 2395 : toit symétrique, AC = 10 m, 35°
def toit(corrige):
    U = .66
    A, C = (0, 0), (10 * U, 0)
    Hh = (5 * U, 0)
    B = (5 * U, 5 * U * math.tan(math.radians(35)))
    s = [r"\fill[otMuted!18] %s rectangle %s;" % (P((0, -2.2)), P(C)),
         r"\draw[otMuted,line width=.8pt] %s rectangle %s;" % (P((0, -2.2)), P(C))]
    s += [r"\fill[white] %s rectangle %s;" % (P((.6, -1.6)), P((1.6, -.6))),
          r"\fill[white] %s rectangle %s;" % (P((C[0] - 1.6, -1.6)), P((C[0] - .6, -.6))),
          r"\fill[white] %s rectangle %s;" % (P((Hh[0] - .45, -2.2)), P((Hh[0] + .45, -.9)))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
          r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C))]
    s += [r"\draw[%s] %s -- %s;" % ("geoReponse,line width=1.5pt" if corrige else "aide", P(B), P(Hh))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.5pt] %s -- %s;" % (P(A), P(B))]
    s += angle_droit(A, Hh, B, "otGreenDark" if corrige else "otNavy")
    s += arc(A, C, B, r"$35^\circ$", r=.7)
    s += arc(C, A, B, r"$35^\circ$", r=.7)
    if corrige:
        s += lseg(A, B, V % r"$AB \approx 6{,}10$ m", ext(A, B, C), d=.16)
        s += [r"\node[lab,anchor=west] at %s {%s};" % (P((Hh[0] + .14, B[1] * .3)), V % r"$\approx 3{,}50$ m"),
              r"\node[lab,anchor=north] at %s {%s};" % (P((Hh[0] / 2 + .2, -.12)), V % "5 m")]
    s += [r"\draw[cote] %s -- %s;" % (P((0, -2.55)), P((C[0], -2.55))),
          r"\node[coteTexte] at %s {10 m};" % P((C[0] / 2, -2.55))]
    s += pt(A, "A", 180, d=.16) + pt(C, "C", 0, d=.16) + pt(B, "B", 90) + pt(Hh, "", 0)
    s += [r"\node[lab,anchor=north west] at %s {$H$};" % P((Hh[0] + .08, -.08))]
    return figure(s)


FIGURES["ex2395_enonce"] = toit(False)
FIGURES["ex2395_corrige"] = toit(True)


# 2396 : rivière, AC = 25 m, angle C = 58°
def riviere(corrige):
    U = .1
    A, C = (0, 0), (25 * U, 0)
    B = (0, 25 * math.tan(math.radians(58)) * U)
    s = [r"\fill[otSky!60!white] %s rectangle %s;" % (P((-1.6, 0)), P((C[0] + 2.2, B[1]))),
         r"\draw[otMuted,line width=.8pt] %s -- %s;" % (P((-1.6, 0)), P((C[0] + 2.2, 0))),
         r"\draw[otMuted,line width=.8pt] %s -- %s;" % (P((-1.6, B[1])), P((C[0] + 2.2, B[1])))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(C), P(B)),
          r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(C), P(B))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(A), P(B)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(B), P(C))]
    s += [r"\fill[otGreen!45] %s circle (.2);" % P((B[0] - .05, B[1] + .45)),
          r"\draw[otMuted,line width=1.2pt] %s -- %s;" % (P((B[0] - .05, B[1] + .08)), P((B[0] - .05, B[1] + .25)))]
    s += angle_droit(C, A, B)
    s += arc(C, A, B, r"$58^\circ$", r=.55)
    s += [r"\node[lab,anchor=north] at %s {%s};" % (P((C[0] / 2, -.15)),
                                                     "25 m" + (r"\\{\rl côté adjacent}" if corrige else ""))]
    s += [r"\node[txt,text=otMuted,anchor=west] at %s {rivière};" % P((C[0] + .7, B[1] * .82))]
    if corrige:
        s += [r"\node[lab,anchor=east] at %s {%s\\{\rl côté opposé}};" % (P((-.2, B[1] * .5)), V % r"$\approx 40{,}0$ m"),
              r"\node[lab,anchor=south west] at %s {%s\\{\rl hypoténuse}};" % (P((C[0] * .5 + .18, B[1] * .5 + .1)), V % r"$\approx 47{,}2$ m")]
    s += pt(A, "A", 225, d=.16) + pt(C, "C", 315, d=.16) + pt(B, "B", 150, d=.18)
    return figure(s)


FIGURES["ex2396_enonce"] = riviere(False)
FIGURES["ex2396_corrige"] = riviere(True)


# 2397 : avion, 12°, 3 km à l'horizontale (angle exagéré)
def avion(corrige):
    W, Hh = 6.2, 2.2
    O, H, A = (0, 0), (W, 0), (W, Hh)
    s = sol(-.6, W + 1.2)
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(O), P(H), P(A)),
          r"\draw[aide] %s -- %s;" % (P(H), P(A)), r"\draw[otNavy,line width=1.1pt] %s -- %s;" % (P(O), P(A))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(H), P(A))]
    s += [r"\draw[otNavy,line width=1pt,-{Stealth[length=2.6mm]}] %s -- %s;" % (P(A), P((W + .75, Hh + .27)))]
    s += angle_droit(O, H, A)
    s += arc(O, H, A, r"$12^\circ$", r=1.1, dl=2.6)
    s += [r"\node[lab,anchor=north] at %s {%s};" % (P((W / 2, -.3)), "3 km" + (r"\\{\rl côté adjacent}" if corrige else ""))]
    if corrige:
        s += [r"\node[lab,anchor=west] at %s {%s\\{\rl côté opposé}};" % (P((W + .15, Hh * .45)), V % r"$h \approx 638$ m"),
              r"\node[lab,anchor=south east] at %s {%s\\{\rl hypoténuse}};" % (P((W * .5 - .05, Hh * .5 + .2)), V % r"$t \approx 3\,067$ m")]
    else:
        s += [r"\node[lab,anchor=west] at %s {$h$};" % P((W + .15, Hh * .45)),
              r"\node[lab,anchor=south east] at %s {$t$};" % P((W * .5 - .05, Hh * .5 + .15))]
    s += pt(A, "", 0)
    s += [r"\node[txt,text=otMuted,anchor=south] at %s {avion};" % P((W - .2, Hh + .32))]
    return figure(s)


FIGURES["ex2397_enonce"] = avion(False)
FIGURES["ex2397_corrige"] = avion(True)


# 2398 : phare de 45 m, angle de dépression 8° (angle exagéré)
def phare(corrige):
    W, Hh = 5.5, 2.3
    Pp, S, B = (0, 0), (0, Hh), (W, 0)
    s = [r"\fill[otSky!70!white] %s rectangle %s;" % (P((-1.3, -.4)), P((W + 1.0, 0))),
         r"\draw[otMuted,line width=.8pt] %s -- %s;" % (P((-1.3, 0)), P((W + 1.0, 0)))]
    s += [r"\fill[otMuted!22] %s -- %s -- %s -- %s -- cycle;" % (P((-.42, 0)), P((0, 0)), P((0, Hh)), P((-.3, Hh))),
          r"\fill[otOrange!70] %s rectangle %s;" % (P((-.36, Hh)), P((0, Hh + .32)))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(Pp), P(B), P(S)),
          r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(Pp), P(B), P(S))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(Pp), P(B))]
    s += [r"\draw[aide] %s -- %s;" % (P(S), P((W + .6, Hh)))]
    s += [r"\fill[otNavy!70] %s -- %s -- %s -- %s -- cycle;" % (P((W - .35, .02)), P((W + .35, .02)),
                                                                P((W + .22, -.2)), P((W - .22, -.2)))]
    s += angle_droit(B, Pp, S)
    s += arc(S, (W + .6, Hh), B, r"$8^\circ$", r=1.3, dl=2.5)
    if corrige:
        s += arc(B, Pp, S, V % r"$8^\circ$", "otGreenDark", r=1.3, dl=2.5)
    s += [r"\node[lab,anchor=east] at %s {%s};" % (P((-.55, Hh / 2)), "45 m" + (r"\\{\rl côté opposé}" if corrige else ""))]
    if corrige:
        s += [r"\node[lab,anchor=north] at %s {%s\\{\rl côté adjacent}};" % (P((W / 2, -.48)), V % r"$PB \approx 320$ m")]
        s += [r"\node[txt,text=otMuted,anchor=south] at %s {horizontale};" % P((W - .2, Hh + .1))]
    else:
        s += [r"\node[txt,text=otMuted,anchor=south] at %s {horizontale};" % P((W - .2, Hh + .1))]
    s += pt(Pp, "P", 315, d=.16) + pt(S, "S", 120, d=.42) + pt(B, "B", 60, d=.2)
    return figure(s)


FIGURES["ex2398_enonce"] = phare(False)
FIGURES["ex2398_corrige"] = phare(True)


# 2399 : route à 10 %, 2,5 km à l'horizontale (pente exagérée)
def route(corrige):
    W, Hh = 6.4, 1.75
    O, R, Q = (0, 0), (W, 0), (W, Hh)
    s = sol(-.5, W + .9)
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(O), P(R), P(Q)),
          r"\draw[aide] %s -- %s;" % (P(R), P(Q)),
          r"\draw[otNavy,line width=2.6pt] %s -- %s;" % (P(O), P(Q))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(R), P(Q))]
    s += angle_droit(O, R, Q)
    s += arc(O, R, Q, (V % r"$\alpha \approx 5{,}7^\circ$") if corrige else r"$\alpha$",
             "otGreenDark" if corrige else "otNavy", r=1.2, dl=2.9 if corrige else 2.3)
    s += [r"\node[lab,anchor=north] at %s {%s};" % (P((W / 2, -.3)), "2,5 km" + (r"\\{\rl côté adjacent}" if corrige else ""))]
    if corrige:
        s += [r"\node[lab,anchor=west] at %s {%s\\{\rl côté opposé}};" % (P((W + .15, Hh / 2)), V % r"$h = 250$ m"),
              r"\node[lab,anchor=south east] at %s {%s\\{\rl hypoténuse}};" % (P((W * .48, Hh * .48 + .22)), V % r"$L \approx 2\,512$ m")]
    else:
        s += [r"\node[lab,anchor=west] at %s {$h$};" % P((W + .15, Hh / 2)),
              r"\node[lab,anchor=south east] at %s {$L$};" % P((W * .48, Hh * .48 + .18))]
    return figure(s)


FIGURES["ex2399_enonce"] = route(False)
FIGURES["ex2399_corrige"] = route(True)


# 2400 : ABC rectangle en B, AB = 8, BC = 6, AE = 5, (EF) perpendiculaire à (AB)
def thales(corrige):
    U = .72
    A, B, C = (0, 0), (8 * U, 0), (8 * U, 6 * U)
    E, F = (5 * U, 0), (5 * U, 3.75 * U)
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C))]
    if corrige:
        s += [r"\fill[otGreen!14] %s -- %s -- %s -- cycle;" % (P(A), P(E), P(F))]
    s += [r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
          r"\draw[geoTrait] %s -- %s;" % (P(E), P(F))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(E), P(F))]
    s += angle_droit(A, B, C) + angle_droit(A, E, F)
    s += [r"\draw[cote] %s -- %s;" % (P((0, -.72)), P((E[0], -.72))),
          r"\node[coteTexte] at %s {5 cm};" % P((E[0] / 2, -.72)),
          r"\draw[cote] %s -- %s;" % (P((0, -1.25)), P((B[0], -1.25))),
          r"\node[coteTexte] at %s {8 cm};" % P((B[0] / 2, -1.25))]
    s += lseg(B, C, "6 cm", -1)
    if corrige:
        s += arc(A, B, C, V % r"$\approx 36{,}9^\circ$", "otGreenDark", r=.6, dl=1.45)
        s += lseg(A, C, V % r"$AC = 10$ cm", 1, t=.78, d=.16)
        s += lseg(A, F, V % r"$AF = 6{,}25$ cm", 1, t=.4, d=.16)
        s += [r"\node[lab,anchor=east] at %s {%s};" % (P((E[0] - .12, F[1] * .38)), V % r"$3{,}75$ cm")]
    s += pt(A, "A", 200, d=.16) + pt(B, "B", 315, d=.16) + pt(C, "C", 45) + pt(E, "E", 270, d=.2) + pt(F, "F", 115, d=.18)
    return figure(s)


FIGURES["ex2400_enonce"] = thales(False)
FIGURES["ex2400_corrige"] = thales(True)
