# -*- coding: utf-8 -*-
"""Figures de la notion « Cosinus dans le triangle rectangle » (4e), style des livres.

Compilées par outils/figures_livre.py. Bleu marine = données ; vert foncé = éléments
de réponse (corrigés) : hypoténuse et côté adjacent repérés (trait vert épais + nom),
résultats. Les étiquettes de côtés sont placées à l'extérieur du triangle ; l'angle
marqué est un arc avec sa mesure dans l'angle. Les données numériques des figures sont
celles des énoncés (contrôlées par verif_287.py).
"""
import math

PREAMBULE_EXTRA = r"""
\tikzset{
  lab/.style={text=otInk,inner sep=0pt,align=center},
  txt/.style={font=\otMedium\fontsize{9}{11}\selectfont,inner sep=0pt,align=center},
  aide/.style={otMuted,line width=.7pt,dash pattern=on 3.5pt off 2pt},
}
\newcommand{\rl}{\otMedium\fontsize{8.5}{10}\selectfont\color{otGreenDark}}
\newcommand{\rmu}{\otMedium\fontsize{8.5}{10}\selectfont\color{otMuted}}
"""

V = r"\textcolor{otGreenDark}{%s}"
ROLE = {"hyp": "hypoténuse", "adj": "côté adjacent", "opp": "côté opposé"}
DEG = math.pi / 180


def f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def P(p):
    return "(%s,%s)" % (f(p[0]), f(p[1]))


def add(p, q, k=1):
    return (p[0] + k * q[0], p[1] + k * q[1])


def mil(p, q, t=.5):
    return (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))


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
    """Étiquette de [pq] posée à côté du segment (cote = 1 : à gauche de p→q)."""
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


def arc(S, p, q, txt=None, coul="otNavy", r=.55, dl=None, double=False):
    """Arc de l'angle de sommet S entre les directions S->p et S->q, mesure dans l'angle."""
    a1 = math.degrees(math.atan2(p[1] - S[1], p[0] - S[0]))
    a2 = math.degrees(math.atan2(q[1] - S[1], q[0] - S[0]))
    dlt = (a2 - a1) % 360
    if dlt > 180:
        a1, dlt = a2, 360 - dlt
    s = []
    for rr in ((r, r + .09) if double else (r,)):
        d0 = (S[0] + rr * math.cos(math.radians(a1)), S[1] + rr * math.sin(math.radians(a1)))
        s.append(r"\draw[%s,line width=.85pt] %s arc[start angle=%s, delta angle=%s, radius=%s];"
                 % (coul, P(d0), f(a1), f(dlt), f(rr)))
    if txt:
        mid = math.radians(a1 + dlt / 2)
        half = math.radians(dlt / 2)
        d = dl or max(r + .34, .36 / math.sin(half)) + (.3 if "approx" in txt else 0)
        m = (S[0] + d * math.cos(mid), S[1] + d * math.sin(mid))
        s.append(r"\node[lab,text=%s] at %s {%s};" % ("otInk" if coul == "otNavy" else coul, P(m), txt))
    return s


def tri_pts(adj, opp, U, theta=0, sens=1, O=(0, 0)):
    """Sommets (S, R, T) : S angle marqué, R angle droit, T troisième sommet.

    [SR] (côté adjacent) part de S dans la direction theta (degrés) ; [RT] tourne
    vers la gauche (sens = 1) ou vers la droite (sens = -1)."""
    u = (math.cos(math.radians(theta)), math.sin(math.radians(theta)))
    n = (-u[1] * sens, u[0] * sens)
    S = O
    R = add(S, u, adj * U)
    T = add(R, n, opp * U)
    return S, R, T


def TRI(S, R, T, noms, ang=None, ang_vert=False, cotes=None, vert=(), roles=(), traits=(), arc_r=.55,
        dl=None, droit_vert=False, angT=None, angT_vert=False, arcT_r=.5, dlT=None, noms_ang=None,
        roles_muets=(), fond=True, d_cote=.14):
    """Triangle rectangle en R. cotes : {"adj"|"opp"|"hyp": texte} ; vert : cotes écrites en vert ;
    roles : nom du côté écrit en vert sous la cote ; roles_muets : nom écrit en gris ;
    traits : côtés tracés en vert ; angT : mesure de l'angle en T."""
    pts = {"S": S, "R": R, "T": T}
    idx = {"adj": ("S", "R"), "opp": ("R", "T"), "hyp": ("S", "T")}
    tiers = {"adj": "T", "opp": "S", "hyp": "R"}
    cotes = cotes or {}
    G = ((S[0] + R[0] + T[0]) / 3, (S[1] + R[1] + T[1]) / 3)
    s = []
    if fond:
        s.append(r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(S), P(R), P(T)))
    s.append(r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(S), P(R), P(T)))
    for k in traits:
        i, j = idx[k]
        s.append(r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(pts[i]), P(pts[j])))
    s += angle_droit(S, R, T, "otGreenDark" if droit_vert else "otNavy")
    if ang is not None:
        s += arc(S, R, T, (V % ang) if (ang_vert and ang) else ang, "otGreenDark" if ang_vert else "otNavy",
                 r=arc_r, dl=dl)
    if angT is not None:
        s += arc(T, R, S, (V % angT) if (angT_vert and angT) else angT, "otGreenDark" if angT_vert else "otNavy",
                 r=arcT_r, dl=dlT, double=True)
    for k in ("adj", "opp", "hyp"):
        txt = cotes.get(k)
        if txt is not None and k in vert:
            txt = V % txt
        if k in roles:
            rl = r"{\rl %s}" % ROLE[k]
            txt = (txt + r"\\" + rl) if txt else rl
        elif k in roles_muets:
            rl = r"{\rmu %s}" % ROLE[k]
            txt = (txt + r"\\" + rl) if txt else rl
        if txt:
            i, j = idx[k]
            c = ext(pts[i], pts[j], pts[tiers[k]])
            s += lseg(pts[i], pts[j], txt, c, d=d_cote)
    for k, p in enumerate((S, R, T)):
        a = noms_ang[k] if noms_ang else math.degrees(math.atan2(p[1] - G[1], p[0] - G[0]))
        s += pt(p, noms[k], a)
    return s


def sol(x0, x1, y=0):
    return [r"\fill[otRule!60] %s rectangle %s;" % (P((x0, y - .16)), P((x1, y))),
            r"\draw[otMuted,line width=.8pt] %s -- %s;" % (P((x0, y)), P((x1, y)))]


def mot(p, txt, anchor="center"):
    return [r"\node[txt,text=otMuted,anchor=%s] at %s {%s};" % (anchor, P(p), txt)]


FIGURES = {}
TOLERE = {}

# ================================================================== COURS
UA = .62
A0, B0, C0 = (0, 0), (7 * UA, 0), (0, 4.4 * UA)


def vocab(angle):
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A0), P(B0), P(C0)),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A0), P(B0), P(C0))]
    s += angle_droit(B0, A0, C0)
    if angle == "B":
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(A0), P(B0)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(B0), P(C0))]
        s += arc(B0, A0, C0)
        s += lseg(A0, B0, r"{\rl côté adjacent à $\widehat{ABC}$}", -1)
        s += lseg(A0, C0, r"{\rmu côté opposé}\\{\rmu à $\widehat{ABC}$}", 1)
    else:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(A0), P(C0)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(B0), P(C0))]
        s += arc(C0, A0, B0)
        s += lseg(A0, B0, r"{\rmu côté opposé à $\widehat{ACB}$}", -1)
        s += lseg(A0, C0, r"{\rl côté adjacent}\\{\rl à $\widehat{ACB}$}", 1)
    s += lseg(B0, C0, r"{\rl hypoténuse}", ext(B0, C0, A0))
    s += pt(A0, "A", 225, d=.16) + pt(B0, "B", 315) + pt(C0, "C", 135)
    return figure(s)


FIGURES["cours_vocab_b"] = vocab("B")
FIGURES["cours_vocab_c"] = vocab("C")


# triangles emboîtés : le cosinus ne dépend que de l'angle (40°)
def emboites():
    U = .95
    t = math.tan(math.radians(40))
    B = (0, 0)
    xs = (2.4, 4.2, 6.2)
    s = [r"\draw[geoTrait] %s -- %s;" % (P(B), P((6.9 * U, 0))),
         r"\draw[geoTrait] %s -- %s;" % (P(B), P((6.9 * U, 6.9 * U * t)))]
    cols = ("otNavy", "otNavy", "otNavy")
    for k, x in enumerate(xs, start=1):
        A, C = (x * U, 0), (x * U, x * U * t)
        s += [r"\draw[otNavy,line width=.9pt] %s -- %s;" % (P(A), P(C))]
        s += angle_droit(B, A, C, cols[k - 1], r=.18)
        s += pt(A, "A_%d" % k, 270, d=.16) + pt(C, "C_%d" % k, 120, d=.16)
    s += arc(B, (1, 0), (1, t), r"$40^\circ$", r=.75)
    s += pt(B, "B", 180, d=.16)
    return figure(s)


FIGURES["cours_emboites"] = emboites()


# exemples du cours (données en bleu, résultat en vert)
c40 = 8 * math.cos(40 * DEG)
S, R, T = tri_pts(c40, 8 * math.sin(40 * DEG), .55)
FIGURES["cours_ex_adj"] = figure(TRI(S, R, T, "BAC", ang=r"$40^\circ$", cotes={"hyp": "8 cm", "adj": r"$\approx 6{,}1$ cm"},
                                     vert=("adj",), roles=("hyp", "adj"), traits=("hyp", "adj")))
o55 = 5 * math.tan(55 * DEG)
S, R, T = tri_pts(5, o55, .55)
FIGURES["cours_ex_hyp"] = figure(TRI(S, R, T, "BAC", ang=r"$55^\circ$", cotes={"adj": "5 cm", "hyp": r"$\approx 8{,}7$ cm"},
                                     vert=("hyp",), roles=("hyp", "adj"), traits=("hyp", "adj")))
o38 = math.sqrt(64 - 9)
S, R, T = tri_pts(3, o38, .55)
FIGURES["cours_ex_angle"] = figure(TRI(S, R, T, "BAC", ang=r"$\approx 68^\circ$", ang_vert=True,
                                       cotes={"adj": "3 cm", "hyp": "8 cm"}, roles=("hyp", "adj"),
                                       traits=("hyp", "adj"), dl=.95))


# échelle contre un mur (cours : 4 m, 75° ; exercice 3657 : 5 m, 70°)
def echelle(L, ang, corrige, U, adj_txt=None, opp_txt=None, noms=None, angle_txt=None, arc_r=.5, arc_dl=None):
    a = math.radians(ang)
    A, C = (L * math.cos(a) * U, 0), (0, 0)
    B = (0, L * math.sin(a) * U)
    s = [r"\fill[otMuted!22] %s rectangle %s;" % (P((-.45, 0)), P((0, B[1] + .55))),
         r"\draw[otMuted,line width=.8pt] (0,0) -- %s;" % P((0, B[1] + .55))]
    s += sol(-.45, A[0] + 1.7)
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(C), P(A), P(B))]
    s += [r"\draw[otOrange!90!black,line width=2.4pt] %s -- %s;" % (P(A), P(B))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(C), P(A))]
    s += angle_droit(A, C, B)
    s += arc(A, C, B, angle_txt or (r"$%d^\circ$" % ang), r=arc_r, dl=arc_dl)
    txt = "%s m" % f(L).replace(".", ",") + (r"\\{\rl hypoténuse}" if corrige else "")
    s += lseg(A, B, txt, -1, d=.2)
    if corrige:
        s += [r"\node[lab,anchor=east] at %s {%s};" % (P((-.6, B[1] / 2)), V % opp_txt),
              r"\node[lab,anchor=north] at %s {%s\\{\rl côté adjacent}};" % (P((A[0] / 2, -.48 if noms else -.3)), V % adj_txt)]
    else:
        s += mot((-.6, B[1] / 2), "mur", "east") + mot((A[0] + 1.0, -.32), "sol", "north")
    if noms:
        s += pt(A, noms[0], 330, d=.2) + pt(B, noms[1], 20, d=.16) + pt(C, noms[2], 200, d=.2)
    return figure(s)


FIGURES["cours_echelle"] = echelle(4, 75, True, .78, r"$d \approx 1{,}04$ m", r"$h \approx 3{,}86$ m", arc_r=.32, arc_dl=.66)
FIGURES["ex3657_enonce"] = echelle(5, 70, False, .66, noms="ABC")
FIGURES["ex3657_corrige"] = echelle(5, 70, True, .66, r"$AC \approx 1{,}71$ m", r"$BC \approx 4{,}70$ m", noms="ABC")


# plus l'angle est grand, plus le côté adjacent est court (hypoténuse 10 cm)
def variation():
    U = .42
    s = []
    y0 = 0
    for a, val in ((20, "9{,}4"), (45, "7{,}1"), (70, "3{,}4")):   # de haut en bas
        h = 10 * math.sin(a * DEG) * U
        y0 -= h
        S, R, T = tri_pts(10 * math.cos(a * DEG), 10 * math.sin(a * DEG), U, O=(0, y0))
        s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(S), P(R), P(T)),
              r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(S), P(R), P(T)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(S), P(R))]
        s += angle_droit(S, R, T, r=.16)
        s += arc(S, R, T, r"$%d^\circ$" % a, r=.5, dl=(1.15 if a == 20 else None))
        s += lseg(S, T, "10 cm", 1, d=.2 if a == 20 else .12)
        s += [r"\node[lab,anchor=north] at %s {%s};" % (P(((S[0] + R[0]) / 2, y0 - .12)), V % (r"$\approx %s$ cm" % val))]
        s += [r"\node[lab,anchor=west] at %s {%s};" % (P((4.6, y0 + h / 2)),
                                                        V % (r"$\cos %d^\circ \approx 0{,}%s$" % (a, {20: "94", 45: "71", 70: "34"}[a])))]
        y0 -= 1.0
    return figure(s)


FIGURES["cos_variation"] = variation()

# ================================================================== EXERCICES
# 3650 : trois triangles
T1 = tri_pts(3.0, 2.0, .62, O=(0, 0))                 # B (angle), A (droit), C
T2 = tri_pts(3.0, 2.0, .62, theta=90, sens=-1, O=(3.0, 0))   # E, F, D
T3 = tri_pts(3.0, 2.0, .62, theta=180, sens=1, O=(8.3, 1.24))  # K, H, G


def ex3650_enonce():
    s = []
    s += TRI(*T1, "BAC", ang="", noms_ang=(200, 315, 45))
    s += TRI(*T2, "EFD", ang="", noms_ang=(270, 135, 45))
    s += TRI(*T3, "KHG", ang="", noms_ang=(20, 135, 225))
    s += mot((T1[0][0] + .93, -.55), "triangle 1", "north")
    s += mot((T2[0][0] + .62, -.55), "triangle 2", "north")
    s += mot((T3[1][0] + .93, -.55), "triangle 3", "north")
    return figure(s)


FIGURES["ex3650_enonce"] = ex3650_enonce()
S, R, T = tri_pts(3.0, 2.0, 1.15)
FIGURES["ex3650_c1"] = figure(TRI(S, R, T, "BAC", ang="", roles=("hyp", "adj"), traits=("hyp", "adj"),
                                  noms_ang=(200, 315, 45)))
S, R, T = tri_pts(3.0, 2.0, 1.15, theta=90, sens=-1)
FIGURES["ex3650_c2"] = figure(TRI(S, R, T, "EFD", ang="", roles=("hyp", "adj"), traits=("hyp", "adj"),
                                  noms_ang=(270, 135, 45)))
S, R, T = tri_pts(3.0, 2.0, 1.15, theta=180, sens=1)
FIGURES["ex3650_c3"] = figure(TRI(S, R, T, "KHG", ang="", roles=("hyp", "adj"), traits=("hyp", "adj"),
                                  noms_ang=(20, 135, 225)))
# angle C du triangle 1 : C devient le sommet de l'angle marqué
S, R, T = tri_pts(3.0, 2.0, 1.15)
FIGURES["ex3650_c5"] = figure(TRI(T, R, S, "CAB", ang="", roles=("hyp", "adj"), traits=("hyp", "adj"),
                                  noms_ang=(45, 315, 200)))

# 3651 : DEF rectangle en E, DE = 4, EF = 3, DF = 5
S, R, T = tri_pts(4, 3, .95)
FIGURES["ex3651_enonce"] = figure(TRI(S, R, T, "DEF", ang="", angT="", cotes={"adj": "4 cm", "opp": "3 cm", "hyp": "5 cm"}))
FIGURES["ex3651_cd"] = figure(TRI(S, R, T, "DEF", ang=r"$\approx 37^\circ$", ang_vert=True,
                                  cotes={"adj": "4 cm", "opp": "3 cm", "hyp": "5 cm"}, roles=("hyp", "adj"),
                                  traits=("hyp", "adj"), dl=1.25))
FIGURES["ex3651_cf"] = figure(TRI(T, R, S, "FED", ang=r"$\approx 53^\circ$", ang_vert=True,
                                  cotes={"adj": "3 cm", "opp": "4 cm", "hyp": "5 cm"}, roles=("hyp", "adj"),
                                  traits=("hyp", "adj"), dl=1.0))

# 3652 : ABC rectangle en A, BC = 10, B = 35°
a, o = 10 * math.cos(35 * DEG), 10 * math.sin(35 * DEG)
S, R, T = tri_pts(a, o, .6)
FIGURES["ex3652_enonce"] = figure(TRI(S, R, T, "BAC", ang=r"$35^\circ$", cotes={"hyp": "10 cm"}))
FIGURES["ex3652_corrige"] = figure(TRI(S, R, T, "BAC", ang=r"$35^\circ$", angT=r"$55^\circ$", angT_vert=True, dlT=.95,
                                       cotes={"hyp": "10 cm", "adj": r"$\approx 8{,}2$ cm", "opp": r"$\approx 5{,}7$ cm"},
                                       vert=("adj", "opp"), roles=("hyp", "adj"), traits=("hyp", "adj")))

# 3653 : ABC rectangle en A, AB = 6, B = 52°
o = 6 * math.tan(52 * DEG)
S, R, T = tri_pts(6, o, .55)
FIGURES["ex3653_enonce"] = figure(TRI(S, R, T, "BAC", ang=r"$52^\circ$", cotes={"adj": "6 cm"}))
FIGURES["ex3653_corrige"] = figure(TRI(S, R, T, "BAC", ang=r"$52^\circ$",
                                       cotes={"adj": "6 cm", "hyp": r"$\approx 9{,}7$ cm", "opp": r"$\approx 7{,}7$ cm"},
                                       vert=("hyp", "opp"), roles=("hyp", "adj"), traits=("hyp", "adj")))

# 3654 : ABC rectangle en A, AB = 4, BC = 7
o = math.sqrt(33)
S, R, T = tri_pts(4, o, .62)
FIGURES["ex3654_enonce"] = figure(TRI(S, R, T, "BAC", ang="", cotes={"adj": "4 cm", "hyp": "7 cm"}))
FIGURES["ex3654_corrige"] = figure(TRI(S, R, T, "BAC", ang=r"$\approx 55^\circ$", ang_vert=True, dl=1.0,
                                       angT=r"$\approx 35^\circ$", angT_vert=True, dlT=1.55,
                                       cotes={"adj": "4 cm", "hyp": "7 cm", "opp": r"$\approx 5{,}74$ cm"},
                                       vert=("opp",), roles=("hyp", "adj"), traits=("hyp", "adj")))

# 3655 : la figure « cos_variation » du cours sert aussi au corrigé


# 3656 : agrandissement (4 ; 5) -> (8 ; 10)
def ex3656(corrige):
    s = []
    S, R, T = tri_pts(4, 3, .42)
    s += TRI(S, R, T, "BAC", ang="", cotes={"adj": "4 cm", "hyp": "5 cm"},
             traits=("hyp", "adj") if corrige else (), noms_ang=(200, 315, 90))
    S2, R2, T2 = tri_pts(8, 6, .42, O=(2.6, 0))
    s += TRI(S2, R2, T2, "EDF", ang="", cotes={"adj": "8 cm", "hyp": "10 cm"},
             traits=("hyp", "adj") if corrige else (), noms_ang=(200, 315, 90))
    if corrige:
        s += [r"\node[lab,anchor=north] at %s {%s};" % (P((R[0] / 2, -.75)), V % r"$\cos \widehat{B} = \dfrac{4}{5} = 0{,}8$"),
              r"\node[lab,anchor=north] at %s {%s};" % (P(((S2[0] + R2[0]) / 2, -.75)), V % r"$\cos \widehat{E} = \dfrac{8}{10} = 0{,}8$")]
    return figure(s)


FIGURES["ex3656_enonce"] = ex3656(False)
FIGURES["ex3656_corrige"] = ex3656(True)


# 3658 : cerf-volant, ficelle 50 m à 40°, main à 1 m
def cerf_volant(corrige):
    U, e = .1, .95
    a = math.radians(40)
    M = (0, e)
    H = (50 * math.cos(a) * U, e)
    K = (H[0], e + 50 * math.sin(a) * U)
    s = sol(-1.0, H[0] + 1.4)
    s += [r"\draw[otMuted,line width=2.2pt] (0,0) -- %s;" % P((0, e - .08))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(M), P(H), P(K))]
    s += [r"\draw[aide] %s -- %s;" % (P(M), P(H)), r"\draw[aide] %s -- %s;" % (P(H), P(K)),
          r"\draw[aide] %s -- %s;" % (P(H), P((H[0], 0)))]
    s += [r"\draw[otNavy,line width=1pt] %s -- %s;" % (P(M), P(K))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(M), P(H)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(M), P(K))]
    kx, ky = K
    s += [r"\fill[otOrange!80] %s -- %s -- %s -- %s -- cycle;" % (P((kx, ky + .34)), P((kx + .21, ky + .05)),
                                                                 P((kx, ky - .22)), P((kx - .21, ky + .05)))]
    s += angle_droit(M, H, K)
    s += arc(M, H, K, r"$40^\circ$", r=.65)
    s += lseg(M, K, "50 m" + (r"\\{\rl hypoténuse}" if corrige else ""), 1, d=.18)
    s += [r"\node[lab,anchor=east] at %s {1 m};" % P((-.22, e / 2))]
    if corrige:
        s += [r"\node[lab,anchor=west] at %s {%s};" % (P((H[0] + .2, (e + ky) / 2)), V % r"$HK \approx 32{,}1$ m"),
              r"\node[lab,anchor=north] at %s {%s\\{\rl côté adjacent}};" % (P((H[0] / 2 + .2, e - .14)), V % r"$MH \approx 38{,}3$ m")]
    s += pt(M, "M", 135, d=.16) + pt(H, "H", 315, d=.16) + pt(K, "K", 160, d=.3)
    return figure(s)


FIGURES["ex3658_enonce"] = cerf_volant(False)
FIGURES["ex3658_corrige"] = cerf_volant(True)


# 3659 : triangle isocèle ABC, AB = AC = 10, BC = 12, H milieu de [BC]
def isocele(corrige):
    U = .52
    B, C = (0, 0), (12 * U, 0)
    H = (6 * U, 0)
    A = (6 * U, 8 * U)
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C))]
    if corrige:
        s += [r"\fill[otGreen!14] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(H)),
              r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(B), P(H)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(B), P(A)),
              r"\draw[otNavy,line width=.9pt] %s -- %s;" % (P(A), P(H))]
        s += angle_droit(B, H, A, "otGreenDark")
        s += arc(B, C, A, V % r"$\approx 53{,}1^\circ$", "otGreenDark", r=.6, dl=1.45)
        s += arc(C, B, A, V % r"$\approx 53{,}1^\circ$", "otGreenDark", r=.6, dl=1.45)
        s += arc(A, B, C, None, "otGreenDark", r=.55)
        s += [r"\node[lab,anchor=south west] at %s {%s};" % (P((A[0] + .3, A[1] + .12)), V % r"$\widehat{BAC} \approx 73{,}7^\circ$")]
        s += [r"\node[lab,anchor=north] at %s {%s\\{\rl côté adjacent}};" % (P((H[0] / 2, -.14)), V % "$6$ cm"),
              r"\node[lab,anchor=north] at %s {6 cm};" % P(((H[0] + C[0]) / 2, -.14))]
        s += lseg(B, A, r"10 cm\\{\rl hypoténuse}", 1, d=.16)
    else:
        s += [r"\draw[aide] %s -- %s;" % (P(A), P(H))]
        s += [r"\node[lab,anchor=north] at %s {12 cm};" % P((H[0], -.42))]
        s += lseg(B, A, "10 cm", 1, d=.16)
    s += [r"\codage{%s}{%s}" % (P(B)[1:-1], P(H)[1:-1]), r"\codage{%s}{%s}" % (P(H)[1:-1], P(C)[1:-1])]
    s += [r"\codage[2]{%s}{%s}" % (P(B)[1:-1], P(A)[1:-1]), r"\codage[2]{%s}{%s}" % (P(A)[1:-1], P(C)[1:-1])]
    s += lseg(A, C, "10 cm", 1, d=.16)
    s += pt(A, "A", 90 if not corrige else 150) + pt(B, "B", 200, d=.16) + pt(C, "C", 340, d=.16)
    s += pt(H, "H", 270, d=.16 if not corrige else .75)
    return figure(s)


FIGURES["ex3659_enonce"] = isocele(False)
FIGURES["ex3659_corrige"] = isocele(True)


# 3660 : rectangle ABCD, AB = 8, BC = 6, diagonales en O
def rectangle(corrige):
    U = .7
    A, B, C, D = (0, 0), (8 * U, 0), (8 * U, 6 * U), (0, 6 * U)
    O = (4 * U, 3 * U)
    s = [r"\fill[otSky] %s -- %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C), P(D)),
         r"\draw[geoTrait] %s -- %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C), P(D)),
         r"\draw[otNavy,line width=.8pt] %s -- %s;" % (P(A), P(C)),
         r"\draw[otNavy,line width=.8pt] %s -- %s;" % (P(B), P(D))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(A), P(C)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(A), P(B))]
    for p, q, r in ((B, A, D), (A, B, C), (B, C, D), (C, D, A)):
        s += angle_droit(p, q, r)
    s += [r"\node[lab,anchor=north] at %s {%s};" % (P((B[0] / 2, -.14)), "8 cm" + (r"\\{\rl côté adjacent}" if corrige else "")),
          r"\node[lab,anchor=west] at %s {6 cm};" % P((B[0] + .14, C[1] / 2))]
    if corrige:
        s += arc(A, B, C, V % r"$\approx 36{,}9^\circ$", "otGreenDark", r=.75, dl=1.75)
        s += arc(C, A, B, V % r"$\approx 53{,}1^\circ$", "otGreenDark", r=.55, dl=1.3)
        s += arc(O, A, B, V % r"$\approx 106{,}3^\circ$", "otGreenDark", r=.4, dl=.95)
        s += [r"\node[lab] at %s {%s};" % (P((1.15, 2.2)), V % r"$AC = 10$ cm" + r"\\{\rl hypoténuse}")]
    s += pt(A, "A", 225, d=.16) + pt(B, "B", 315, d=.16) + pt(C, "C", 45) + pt(D, "D", 135) + pt(O, "O", 90, d=.2)
    return figure(s)


FIGURES["ex3660_enonce"] = rectangle(False)
FIGURES["ex3660_corrige"] = rectangle(True)


# 3661 : AB = 10, AC = 8, B = 40°, H pied de la hauteur issue de A
def hauteur(corrige):
    U = .5
    bh = 10 * math.cos(40 * DEG)
    ah = 10 * math.sin(40 * DEG)
    hc = math.sqrt(64 - ah ** 2)
    B, H, A, C = (0, 0), (bh * U, 0), (bh * U, ah * U), ((bh + hc) * U, 0)
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
         r"\draw[otNavy,line width=.9pt] %s -- %s;" % (P(A), P(H))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(B), P(H)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(H), P(C))]
    s += angle_droit(B, H, A) + angle_droit(A, H, C)
    s += arc(B, H, A, r"$40^\circ$", r=.7)
    s += lseg(B, A, "10 cm", 1, d=.16) + lseg(A, C, "8 cm", 1, d=.16)
    if corrige:
        s += arc(C, A, H, V % r"$\approx 53{,}5^\circ$", "otGreenDark", r=.55, dl=1.35, double=True)
        s += [r"\node[lab,anchor=north] at %s {%s};" % (P((H[0] / 2, -.14)), V % r"$BH \approx 7{,}66$ cm"),
              r"\node[lab,anchor=north] at %s {%s};" % (P(((H[0] + C[0]) / 2 + .1, -.14)), V % r"$HC \approx 4{,}76$ cm"),
              r"\node[lab,anchor=east] at %s {%s};" % (P((H[0] - .14, A[1] * .4)), V % r"$\approx 6{,}43$ cm")]
    s += pt(A, "A", 90) + pt(B, "B", 200, d=.16) + pt(C, "C", 20 if corrige else 340, d=.16)
    s += pt(H, "H", 270, d=.16 if not corrige else .62)
    return figure(s)


FIGURES["ex3661_enonce"] = hauteur(False)
FIGURES["ex3661_corrige"] = hauteur(True)

# 3662 : RST rectangle en S, RS = 5, ST = 12, RT = 13 (S en bas à gauche)
S_, R_, T_ = (0, 0), (0, 5 * .52), (12 * .52, 0)


def rst(corrige):
    s = TRI(T_, S_, R_, "TSR", ang="" if not corrige else r"$\approx 22{,}6^\circ$", ang_vert=corrige, arc_r=1.0,
            dl=2.35 if corrige else None,
            angT="" if not corrige else r"$\approx 67{,}4^\circ$", angT_vert=corrige, arcT_r=.45, dlT=1.15,
            cotes={"adj": "12 cm", "opp": "5 cm", "hyp": "13 cm"},
            roles=("hyp",) if corrige else (), traits=("hyp",) if corrige else (), noms_ang=(340, 225, 110))
    return figure(s)


FIGURES["ex3662_enonce"] = rst(False)
FIGURES["ex3662_corrige"] = rst(True)

# 3663 : trois triangles, trois calculs
# a) MNP rectangle en N, M = 28°, MP = 9
a = 9 * math.cos(28 * DEG)
Sa = tri_pts(a, 9 * math.sin(28 * DEG), .6)
FIGURES["ex3663_ea"] = figure(TRI(*Sa, "MNP", ang=r"$28^\circ$", cotes={"hyp": "9 cm"}, dl=1.35, arc_r=.8))
FIGURES["ex3663_ca"] = figure(TRI(*Sa, "MNP", ang=r"$28^\circ$", dl=1.35, arc_r=.8,
                                  cotes={"hyp": "9 cm", "adj": r"$MN \approx 7{,}9$ cm"}, vert=("adj",),
                                  roles=("hyp", "adj"), traits=("hyp", "adj")))
# b) RST rectangle en S, R = 62°, RS = 4,5 (côté adjacent vertical)
o = 4.5 * math.tan(62 * DEG)
Sb = tri_pts(4.5, o, .5, theta=90, sens=-1)
FIGURES["ex3663_eb"] = figure(TRI(*Sb, "RST", ang=r"$62^\circ$", cotes={"adj": "4,5 cm"}, noms_ang=(270, 135, 0)))
FIGURES["ex3663_cb"] = figure(TRI(*Sb, "RST", ang=r"$62^\circ$", noms_ang=(270, 135, 0),
                                  cotes={"adj": "4,5 cm", "hyp": r"$RT \approx 9{,}6$ cm", "opp": r"$ST \approx 8{,}5$ cm"},
                                  vert=("hyp", "opp"), roles=("hyp", "adj"), traits=("hyp", "adj")))
# c) UVW rectangle en V, UV = 6,3, UW = 9 (U à droite)
o = math.sqrt(81 - 6.3 ** 2)
Sc = tri_pts(6.3, o, .6, theta=180, sens=-1)
FIGURES["ex3663_ec"] = figure(TRI(*Sc, "UVW", ang="", cotes={"adj": "6,3 cm", "hyp": "9 cm"}, noms_ang=(0, 225, 135)))
FIGURES["ex3663_cc"] = figure(TRI(*Sc, "UVW", ang=r"$\approx 45{,}6^\circ$", ang_vert=True, dl=1.3,
                                  angT=r"$\approx 44{,}4^\circ$", angT_vert=True, dlT=2.0,
                                  cotes={"adj": "6,3 cm", "hyp": "9 cm"}, roles=("hyp", "adj"), traits=("hyp", "adj"),
                                  noms_ang=(0, 225, 135)))


# 3664 : téléphérique, DH = 1 500 m, 25°, départ à 1 350 m
def telepherique(corrige):
    U = .0042
    W = 1500 * U
    Hh = 1500 * math.tan(25 * DEG) * U
    D, H, A = (0, 0), (W, 0), (W, Hh)
    mont = [(-.7, -.55), (-.7, -.25), (W * .35, Hh * .2), (W * .7, Hh * .55), (W, Hh - .15), (W + .9, Hh - .45), (W + .9, -.55)]
    s = [r"\fill[otRule!70] %s -- cycle;" % " -- ".join(P(p) for p in mont)]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(D), P(H), P(A))]
    s += [r"\draw[aide] %s -- %s;" % (P(D), P(H)), r"\draw[aide] %s -- %s;" % (P(H), P(A))]
    s += [r"\draw[otNavy,line width=1.1pt] %s -- %s;" % (P(D), P(A))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(D), P(A)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(D), P(H))]
    c = mil(D, A, .5)
    s += [r"\draw[otMuted,line width=.7pt] %s -- %s;" % (P(c), P((c[0], c[1] - .22))),
          r"\fill[otOrange!85] %s rectangle %s;" % (P((c[0] - .2, c[1] - .55)), P((c[0] + .2, c[1] - .22)))]
    s += angle_droit(D, H, A)
    s += arc(D, H, A, r"$25^\circ$", r=.8)
    s += [r"\node[lab,anchor=north] at %s {%s};" % (P((W / 2 + .3, -.12)),
                                                     "1 500 m" + (r"\\{\rl côté adjacent}" if corrige else ""))]
    if corrige:
        s += lseg(D, A, V % r"$DA \approx 1\,655$ m" + r"\\{\rl hypoténuse}", 1, t=.42, d=.2)
        s += [r"\node[lab,anchor=east] at %s {%s};" % (P((W - .14, Hh * .55)), V % r"$HA \approx 699$ m"),
              r"\node[lab,anchor=south] at %s {%s};" % (P((W, Hh + .55)), V % r"altitude $\approx 2\,049$ m")]
    else:
        s += lseg(D, A, "câble", 1, t=.42, d=.2)
    s += mot((-.6, -1.4 if corrige else -.85), r"départ : 1~350 m d'altitude", "north west")
    s += pt(D, "D", 135, d=.16) + pt(H, "H", 315, d=.16) + pt(A, "A", 135 if corrige else 90, d=.18)
    return figure(s)


FIGURES["ex3664_enonce"] = telepherique(False)
FIGURES["ex3664_corrige"] = telepherique(True)


# 3665 : rampe de chargement d'un camion
def rampe(L, h, corrige, adj_txt=None, ang_txt=None, U=1.35):
    d = math.sqrt(L ** 2 - h ** 2)
    A, H, Pp = (0, 0), (d * U, 0), (d * U, h * U)
    s = sol(-.5, H[0] + 2.9)
    s += [r"\fill[otMuted!25] %s rectangle %s;" % (P((H[0], .45)), P((H[0] + 2.7, Pp[1] + 1.6))),
          r"\draw[otMuted,line width=.8pt] %s rectangle %s;" % (P((H[0], .45)), P((H[0] + 2.7, Pp[1] + 1.6))),
          r"\fill[otMuted!45] %s rectangle %s;" % (P((H[0], Pp[1] - .08)), P((H[0] + 2.7, Pp[1]))),
          r"\fill[otMuted!70] %s circle (.36);" % P((H[0] + 2.0, .36)),
          r"\fill[white] %s circle (.13);" % P((H[0] + 2.0, .36))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(H), P(Pp)),
          r"\draw[aide] %s -- %s;" % (P(H), P(Pp))]
    s += [r"\draw[otOrange!90!black,line width=2.4pt] %s -- %s;" % (P(A), P(Pp))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(A), P(H))]
    s += angle_droit(A, H, Pp)
    s += arc(A, H, Pp, (V % ang_txt) if corrige else r"$\alpha$", "otGreenDark" if corrige else "otNavy",
             r=1.0, dl=2.05 if corrige else 1.45)
    s += lseg(A, Pp, ("%s m" % f(L).replace(".", ",")) + (r"\\{\rl hypoténuse}" if corrige else ""), 1, t=.45, d=.36)
    s += [r"\node[lab,anchor=west] at %s {%s m};" % (P((H[0] + .14, Pp[1] / 2)), f(h).replace(".", ","))]
    if corrige:
        s += [r"\node[lab,anchor=north] at %s {%s\\{\rl côté adjacent}};" % (P((H[0] / 2, -.3)), V % adj_txt)]
    s += mot((H[0] + 1.35, Pp[1] + .8), "camion")
    s += pt(A, "A", 225, d=.16) + pt(H, "H", 290, d=.2) + pt(Pp, "P", 120, d=.16)
    return figure(s)


FIGURES["ex3665_enonce"] = rampe(3, 1, False)
FIGURES["ex3665_c1"] = rampe(3, 1, True, r"$AH \approx 2{,}83$ m", r"$\alpha \approx 19{,}5^\circ$")
FIGURES["ex3665_c2"] = rampe(4, 1.2, True, r"$AH \approx 3{,}82$ m", r"$\alpha \approx 17{,}5^\circ$", U=1.15)


# 3666 : toit symétrique
def toit(larg, cote_txt, corrige, chev_txt=None, ang_txt=None, ang_vert=False, h_txt=None, demi_txt=None):
    U = .62 * 9 / larg
    B, C = (0, 0), (larg * U, 0)
    I = (larg / 2 * U, 0)
    if ang_txt and not ang_vert:      # angle donné (30°)
        hA = larg / 2 * math.tan(30 * DEG)
    else:
        hA = math.sqrt(5.5 ** 2 - 4.5 ** 2)
    A = (I[0], hA * U)
    s = [r"\fill[otMuted!18] %s rectangle %s;" % (P((0, -2.2)), P(C)),
         r"\draw[otMuted,line width=.8pt] %s rectangle %s;" % (P((0, -2.2)), P(C)),
         r"\fill[white] %s rectangle %s;" % (P((.6, -1.6)), P((1.5, -.7))),
         r"\fill[white] %s rectangle %s;" % (P((C[0] - 1.5, -1.6)), P((C[0] - .6, -.7))),
         r"\fill[white] %s rectangle %s;" % (P((I[0] - .42, -2.2)), P((I[0] + .42, -.95)))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
          r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C))]
    s += [r"\draw[%s] %s -- %s;" % ("otNavy,line width=.9pt" if corrige else "aide", P(A), P(I))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(B), P(I)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(B), P(A))]
        s += angle_droit(B, I, A, "otGreenDark")
    if ang_txt:
        s += arc(B, C, A, (V % ang_txt) if ang_vert else ang_txt, "otGreenDark" if ang_vert else "otNavy", r=.8,
                 dl=1.75 if ang_vert else 1.35)
    s += lseg(B, A, (V % chev_txt if (corrige and ang_txt and not ang_vert) else chev_txt)
              + (r"\\{\rl hypoténuse}" if corrige else ""), 1, d=.16)
    if not (ang_txt and not ang_vert):
        s += lseg(A, C, chev_txt, 1, d=.16)
    if corrige:
        s += [r"\node[lab,anchor=west] at %s {%s};" % (P((I[0] + .14, A[1] * .32)), V % h_txt),
              r"\node[lab,anchor=north] at %s {%s\\{\rl côté adjacent}};" % (P((I[0] / 2, -.1)), V % demi_txt)]
    s += [r"\draw[cote] %s -- %s;" % (P((0, -2.55)), P((C[0], -2.55))),
          r"\node[coteTexte] at %s {%s};" % (P((C[0] / 2, -2.55)), cote_txt)]
    s += pt(A, "A", 90) + pt(B, "B", 180, d=.16) + pt(C, "C", 0, d=.16) + pt(I, "", 0)
    s += [r"\node[lab,anchor=north west] at %s {$I$};" % P((I[0] + .08, -.08))]
    return figure(s)


FIGURES["ex3666_enonce"] = toit(9, "9 m", False, "5,5 m")
FIGURES["ex3666_c1"] = toit(9, "9 m", True, "5,5 m", r"$\approx 35{,}1^\circ$", True, r"$\approx 3{,}16$ m", r"$BI = 4{,}5$ m")
FIGURES["ex3666_c2"] = toit(10, "10 m", True, r"$\ell \approx 5{,}77$ m", r"$30^\circ$", False, r"$h \approx 2{,}89$ m", r"$5$ m")


# 3667 : bateau, OP = 12 km à 40° du nord, puis 5 km vers l'est
def bateau(corrige):
    U = .42
    a = 40 * DEG
    O = (0, 0)
    H = (0, 12 * math.cos(a) * U)
    Pp = (12 * math.sin(a) * U, H[1])
    Q = (Pp[0] + 5 * U, H[1])
    s = [r"\draw[otMuted,line width=.7pt,-{Stealth[length=2.4mm]}] %s -- %s;" % (P(O), P((0, H[1] + 1.1))),
         r"\draw[otMuted,line width=.7pt,-{Stealth[length=2.4mm]}] %s -- %s;" % (P(O), P((Q[0] + .7, 0)))]
    s += mot((0, H[1] + 1.2), "nord", "south") + mot((Q[0] + .8, 0), "est", "west")
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(O), P(H), P(Pp))]
    if corrige:
        s += [r"\fill[otGreen!12] %s -- %s -- %s -- cycle;" % (P(O), P(Pp), P(Q)),
              r"\draw[otGreenDark,line width=1pt,dash pattern=on 4pt off 2.5pt] %s -- %s;" % (P(O), P(Q))]
    s += [r"\draw[aide] %s -- %s;" % (P(H), P(Pp))]
    s += [r"\draw[otNavy,line width=1.1pt,-{Stealth[length=2.6mm]}] %s -- %s;" % (P(O), P(Pp)),
          r"\draw[otNavy,line width=1.1pt,-{Stealth[length=2.6mm]}] %s -- %s;" % (P(Pp), P(Q))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(O), P(H))]
    s += angle_droit(O, H, Pp)
    s += arc(O, H, Pp, r"$40^\circ$", r=.9, dl=1.3)
    s += lseg(O, Pp, "12 km" + (r"\\{\rl hypoténuse}" if corrige else ""), 1 if corrige else -1,
              t=.62 if corrige else .55, d=.18)
    s += [r"\node[lab,anchor=south] at %s {5 km};" % P(mil(Pp, Q, .5)[0:1] + (H[1] + .14,))]
    if corrige:
        s += arc(O, H, Q, V % r"$\approx 54{,}1^\circ$", "otGreenDark", r=1.55, dl=2.25)
        s += [r"\node[lab,anchor=east] at %s {%s\\{\rl côté adjacent}};" % (P((-.18, H[1] / 2)), V % r"$OH \approx 9{,}19$ km"),
              r"\node[lab,anchor=south] at %s {%s};" % (P((Pp[0] / 2, H[1] + .14)), V % r"$HP \approx 7{,}71$ km"),
              r"\node[lab,anchor=north west] at %s {%s};" % (P(mil(O, Q, .78)), V % r"$OQ \approx 15{,}7$ km")]
    s += pt(O, "O", 225, d=.16) + pt(H, "H", 135 if not corrige else 200, d=.16) + pt(Pp, "P", 90 if not corrige else 300, d=.2) + pt(Q, "Q", 0, d=.16)
    return figure(s)


FIGURES["ex3667_enonce"] = bateau(False)
FIGURES["ex3667_corrige"] = bateau(True)


# 3668 : pendule, fil de 1,2 m écarté de 30°
def pendule(corrige):
    U = 4.4
    a = 30 * DEG
    O = (0, 0)
    B0 = (0, -1.2 * U)
    B = (1.2 * math.sin(a) * U, -1.2 * math.cos(a) * U)
    H = (0, B[1])
    s = [r"\fill[otMuted!35] %s rectangle %s;" % (P((-1.1, 0)), P((1.1, .22))),
         r"\draw[otMuted,line width=.8pt] %s -- %s;" % (P((-1.1, 0)), P((1.1, 0)))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(O), P(H), P(B))]
    s += [r"\draw[aide] %s -- %s;" % (P(O), P(B0)), r"\draw[aide] %s -- %s;" % (P(H), P(B))]
    s += [r"\draw[otMuted,line width=.7pt,dash pattern=on 2pt off 2pt] %s arc[start angle=-90, delta angle=36, radius=%s];"
          % (P(B0), f(1.2 * U))]
    s += [r"\draw[otNavy,line width=1.1pt] %s -- %s;" % (P(O), P(B))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(O), P(H)),
              r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(O), P(B)),
              r"\draw[otGreenDark,line width=1.6pt] %s -- %s;" % (P(H), P(B0))]
    s += [r"\draw[otNavy,fill=white,line width=.8pt] %s circle (.13);" % P(B0)]
    s += [r"\fill[otOrange!85] %s circle (.16);" % P(B)]
    s += angle_droit(O, H, B)
    s += arc(O, H, B, r"$30^\circ$", r=.9, dl=1.35)
    s += lseg(O, B, "1,2 m" + (r"\\{\rl hypoténuse}" if corrige else ""), 1, t=.5, d=.2)
    if corrige:
        s += [r"\node[lab,anchor=east] at %s {%s\\{\rl côté adjacent}};" % (P((-.18, H[1] * .5)), V % r"$OH \approx 1{,}04$ m"),
              r"\node[lab,anchor=east] at %s {%s};" % (P((-.25, H[1] - .42)), V % r"$HB_0 \approx 16$ cm"),
              r"\node[lab,anchor=south] at %s {%s};" % (P((B[0] / 2 + .2, H[1] + .1)), V % r"$HB = 0{,}6$ m")]
    s += pt(O, "O", 160, d=.18) + pt(H, "H", 160, d=.2) + pt(B0, "B_0", 270, d=.2)
    s += [r"\node[lab,anchor=west] at %s {$B$};" % P((B[0] + .24, B[1]))]
    return figure(s)


FIGURES["ex3668_enonce"] = pendule(False)
FIGURES["ex3668_corrige"] = pendule(True)


# 3669 : toboggan (type brevet)
def toboggan(L, ang, corrige, h=None, zone=True, adj_txt=None, h_txt=None, L_txt=None, ang_txt=None, d_txt=None):
    U = 1.05
    if h is None:
        d = L * math.cos(ang * DEG)
        hh = math.sqrt(L ** 2 - d ** 2)
    else:
        d, hh = L, h
    A, H, Sx = (0, 0), (d * U, 0), (d * U, hh * U)
    s = sol(-2.4 if zone else -.6, H[0] + 1.2)
    if zone:
        s += [r"\fill[otGreen!18] %s rectangle %s;" % (P((-2.1, .0)), P((0, .28)))]
        s += [r"\draw[cote] %s -- %s;" % (P((-2.1, -.55)), P((0, -.55))),
              r"\node[coteTexte] at %s {2 m};" % P((-1.05, -.55))]
        s += mot((-1.05, .42), "zone libre", "south")
    # échelle verticale et plateforme
    s += [r"\draw[otMuted,line width=1.4pt] %s -- %s;" % (P((H[0] + .45, 0)), P((H[0] + .45, Sx[1])))]
    for k in range(1, int(Sx[1] / .38)):
        s += [r"\draw[otMuted,line width=.9pt] %s -- %s;" % (P((H[0], k * .38)), P((H[0] + .45, k * .38)))]
    s += [r"\fill[otMuted!55] %s rectangle %s;" % (P((H[0], Sx[1])), P((H[0] + .45, Sx[1] + .1)))]
    s += [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(H), P(Sx))]
    s += [r"\draw[otNavy,line width=1pt] %s -- %s;" % (P(H), P(Sx))]
    s += [r"\draw[otOrange!90!black,line width=2.6pt] %s -- %s;" % (P(A), P(Sx))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(A), P(H))]
    s += angle_droit(A, H, Sx)
    if h is None:
        s += arc(A, H, Sx, r"$%d^\circ$" % ang, r=.75)
        s += lseg(A, Sx, ("%s m" % f(L).replace(".", ",")) + (r"\\{\rl hypoténuse}" if corrige else ""), 1, t=.45, d=.2)
    else:
        s += arc(A, H, Sx, V % ang_txt, "otGreenDark", r=.75, dl=1.6)
        s += lseg(A, Sx, V % L_txt + r"\\{\rl hypoténuse}", 1, t=.45, d=.2)
    if corrige:
        s += [r"\node[lab,anchor=north] at %s {%s\\{\rl côté adjacent}};" % (P((H[0] / 2, -.3)), V % adj_txt if h is None else adj_txt)]
        s += [r"\node[lab,anchor=west] at %s {%s};" % (P((H[0] + .6, Sx[1] / 2)), V % h_txt if h is None else h_txt)]
    s += pt(A, "A", 250, d=.18) + pt(H, "H", 290, d=.2) + pt(Sx, "S", 135, d=.16)
    return figure(s)


FIGURES["ex3669_enonce"] = toboggan(4.5, 32, False)
FIGURES["ex3669_ca"] = toboggan(4.5, 32, True, zone=False, adj_txt=r"$AH \approx 3{,}82$ m", h_txt=r"$HS \approx 2{,}38$ m")
FIGURES["ex3669_cc"] = toboggan(3.5, None, True, h=2.1, zone=False, adj_txt="3,5 m", h_txt="2,1 m",
                                L_txt=r"$AS \approx 4{,}08$ m", ang_txt=r"$\approx 31{,}0^\circ$")


# 3670 : ABC, AB = 9, AC = 12, BC = 15 ; H pied de la hauteur issue de A
def brevet(corrige):
    U = .45
    B, C = (0, 0), (15 * U, 0)
    H = (5.4 * U, 0)
    A = (5.4 * U, 7.2 * U)
    s = [r"\fill[otSky] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
         r"\draw[geoTrait] %s -- %s -- %s -- cycle;" % (P(A), P(B), P(C)),
         r"\draw[otNavy,line width=.9pt] %s -- %s;" % (P(A), P(H))]
    if corrige:
        s += [r"\draw[geoReponse,line width=1.6pt] %s -- %s;" % (P(B), P(H))]
        s += angle_droit(B, A, C, "otGreenDark")
        s += arc(B, C, A, V % r"$\approx 53^\circ$", "otGreenDark", r=.6, dl=1.25)
        s += arc(C, B, A, V % r"$\approx 37^\circ$", "otGreenDark", r=.8, dl=1.65, double=True)
        s += [r"\node[lab,anchor=north] at %s {%s};" % (P((H[0] / 2, -.14)), V % r"$BH = 5{,}4$ cm"),
              r"\node[lab,anchor=west] at %s {%s};" % (P((H[0] + .12, A[1] * .4)), V % r"$AH = 7{,}2$ cm")]
    s += angle_droit(B, H, A)
    s += lseg(B, A, "9 cm", 1, d=.16) + lseg(A, C, "12 cm", 1, d=.16)
    s += [r"\draw[cote] %s -- %s;" % (P((0, -.95 if corrige else -.55)), P((C[0], -.95 if corrige else -.55))),
          r"\node[coteTexte] at %s {15 cm};" % P((C[0] / 2, -.95 if corrige else -.55))]
    s += pt(A, "A", 90) + pt(B, "B", 180, d=.16) + pt(C, "C", 0, d=.16) + pt(H, "", 0)
    s += [r"\node[lab,anchor=north west] at %s {$H$};" % P((H[0] + .06, -.06))]
    return figure(s)


FIGURES["ex3670_enonce"] = brevet(False)
FIGURES["ex3670_corrige"] = brevet(True)
