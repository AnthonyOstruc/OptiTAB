# -*- coding: utf-8 -*-
"""Figures du chapitre 14 (Thalès, triangles emboîtés) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, finish, _save, right_angle, add_parallel_marks, tableau,
                   BLUE, ORANGE, GREEN, DARK, NEUTRAL, DIR_COURS, DIR_EXOS)
import numpy as np
from math import sqrt
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
P = lambda x, y: np.array([x, y], float)  # noqa: E731
LBLUE, LORANGE, LGREEN = "#d6eafc", "#fdebd0", "#e8f5e9"
STYLE = {"d": (DARK, "normal"), "q": (ORANGE, "bold"), "s": (GREEN, "bold"), "o": (ORANGE, "normal")}


def unit(v):
    v = np.array(v, float)
    return v / np.linalg.norm(v)


def normale_hors(Pa, Qa, R):
    """Normale unitaire à (PQ) du côté opposé au point R."""
    u = unit(Qa - Pa)
    n = np.array([-u[1], u[0]])
    return -n if np.dot(n, R - Pa) > 0 else n


def point(ax, Pt, nom, d, fs=14, s=26):
    d = unit(d)
    ax.scatter([Pt[0]], [Pt[1]], s=s, zorder=6, color=DARK)
    ax.annotate(f"${nom}$", (Pt[0], Pt[1]), textcoords="offset points", xytext=(15 * d[0], 15 * d[1]),
                ha="center", va="center", fontsize=fs, color=DARK, fontweight="bold")


def cote(ax, Pa, Qa, txt, n, style="d", off=0.42, t=0.5, fleche=False, fs=12.5):
    """Longueur écrite le long de [PQ], décalée selon la normale n (flèche de cote en option)."""
    col, wt = STYLE[style]
    if fleche:
        a, b = Pa + off * n, Qa + off * n
        ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="<->", color=col, lw=1.1,
                                                        shrinkA=0, shrinkB=0), annotation_clip=False)
        for E in (Pa, Qa):
            e1, e2 = E + 0.12 * n, E + (off + 0.12) * n
            ax.plot([e1[0], e2[0]], [e1[1], e2[1]], lw=0.8, color=col, ls=":")
        pos = Pa + t * (Qa - Pa) + (off + 0.36) * n
    else:
        pos = Pa + t * (Qa - Pa) + off * n
    ax.text(pos[0], pos[1], txt, color=col, fontsize=fs, ha="center", va="center", fontweight=wt,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))


def tri(ab, ac, bc, base=7.4):
    """Triangle à l'échelle : B = (0, 0), C sur l'axe, [BC] mesurant `base` unités."""
    s = base / bc
    ax_ = (ab ** 2 - ac ** 2 + bc ** 2) / (2 * bc)
    ay = sqrt(ab ** 2 - ax_ ** 2)
    return P(ax_ * s, ay * s), P(0, 0), P(base, 0)


def config(path, k=0.5, ABC=None, noms="ABCMN", cotes=(), fill=True, para=True, droit=(), extra=None,
           bc_ls="-", w=7.2, h=5.4, couleurs=(LBLUE, LORANGE), lw=2.3, marge=1.0, para_mn=(0, 1),
           para_bc=(0, 1)):
    """Triangles emboîtés : M sur [AB], N sur [AC], (MN) // (BC), AM = k AB.
    cotes = [(segment, texte, style, options)] avec segment parmi AM, MB, AB, AN, NC, AC, MN, BC."""
    A, B, Cc = ABC if ABC is not None else (P(0, 5), P(-1, 0), P(7, 0))
    M, N = A + k * (B - A), A + k * (Cc - A)
    pts = {"A": A, "B": B, "C": Cc, "M": M, "N": N}
    fig, ax = new_fig(w, h)
    if fill:
        ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=couleurs[0], edgecolor="none", zorder=0))
        ax.add_patch(Polygon([A, M, N], closed=True, facecolor=couleurs[1], edgecolor="none", zorder=0))
    ax.plot([B[0], A[0], Cc[0]], [B[1], A[1], Cc[1]], lw=lw, color=BLUE)
    ax.plot([B[0], Cc[0]], [B[1], Cc[1]], lw=lw, color=BLUE, ls=bc_ls)
    ax.plot([M[0], N[0]], [M[1], N[1]], lw=lw, color=ORANGE)
    if para:
        a, b = para_mn
        add_parallel_marks(ax, M + a * (N - M), M + b * (N - M), n=2, color=ORANGE, size=0.26)
        a, b = para_bc
        add_parallel_marks(ax, B + a * (Cc - B), B + b * (Cc - B), n=2, color=BLUE, size=0.26)
    for sommet in droit:
        if sommet == "B":
            right_angle(ax, B, A - B, Cc - B, size=0.32)
        elif sommet == "M":
            right_angle(ax, M, A - M, N - M, size=0.28, color=GREEN)
    nAB, nAC = normale_hors(A, B, Cc), normale_hors(A, Cc, B)
    nBC, nMN = normale_hors(B, Cc, A), -normale_hors(M, N, A)
    nrm = {"AB": nAB, "AM": nAB, "MB": nAB, "AC": nAC, "AN": nAC, "NC": nAC, "BC": nBC, "MN": nMN}
    for c in cotes:
        seg, txt, style = c[:3]
        opt = dict(c[3]) if len(c) > 3 else {}
        if seg in ("AB", "AC") and "fleche" not in opt:
            opt.update(fleche=True, off=opt.get("off", 1.05))
        if seg == "MN":
            opt.setdefault("off", 0.32)
        cote(ax, pts[seg[0]], pts[seg[1]], txt, nrm[seg], style, **opt)
    n = dict(zip("ABCMN", noms))
    G = (A + B + Cc) / 3
    point(ax, A, n["A"], A - G)
    point(ax, B, n["B"], B - G)
    point(ax, Cc, n["C"], Cc - G)
    point(ax, M, n["M"], nAB + 0.35 * unit(A - B))
    point(ax, N, n["N"], nAC + 0.35 * unit(A - Cc))
    if extra:
        extra(ax, pts)
    finish(fig, ax, path, [A, B, Cc], margin=marge)


def legende(ax, x, y, txt, col=NEUTRAL, fs=11, **kw):
    ax.text(x, y, txt, fontsize=fs, color=col, **kw)


# ======================================================================= COURS
config(C("thales_4e_configuration.png"), k=0.6, ABC=tri(5, 10, 8),
       extra=lambda ax, p: legende(ax, 3.4, 4.3, "$\\dfrac{AM}{AB} = \\dfrac{AN}{AC} = \\dfrac{MN}{BC}$",
                                   GREEN, 17, fontweight="bold"))


def reduction(path):
    """Les deux triangles séparés : AMN est une réduction de ABC (coefficient 0,6)."""
    fig, ax = new_fig(10.5, 4.6)
    A, B, Cc = tri(5, 10, 8, base=6.0)
    for dx, k, col, fc, lab, L in [
            (0.8, 1.0, BLUE, LBLUE, "ABC", ("5 cm", "10 cm", "8 cm")),
            (10.2, 0.6, ORANGE, LORANGE, "AMN", ("3 cm", "6 cm", "4,8 cm"))]:
        a, b, c = A * k + P(dx, 0), B * k + P(dx, 0), Cc * k + P(dx, 0)
        ax.add_patch(Polygon([a, b, c], closed=True, facecolor=fc, edgecolor=col, lw=2.3))
        G = (a + b + c) / 3
        for Q1, Q2, R, t in [(a, b, c, L[0]), (a, c, b, L[1]), (b, c, a, L[2])]:
            cote(ax, Q1, Q2, t, normale_hors(Q1, Q2, R), off=0.42, fs=13)
        for Pt, nom in zip((a, b, c), lab):
            point(ax, Pt, nom, Pt - G)
    ax.annotate("", xy=(9.3, 1.3), xytext=(7.4, 1.3),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.4, mutation_scale=18))
    ax.text(8.35, 1.65, "$\\times\\, 0{,}6$", fontsize=16, color=GREEN, ha="center", fontweight="bold")
    ax.text(3.8, -1.25, "grand triangle", ha="center", fontsize=12, color=BLUE, fontweight="bold")
    ax.text(12.2, -1.25, "petit triangle (réduction)", ha="center", fontsize=12, color=ORANGE,
            fontweight="bold")
    ax.set_xlim(-1.2, 15.4)
    ax.set_ylim(-1.7, 5.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


reduction(C("thales_4e_reduction.png"))
tableau(C("thales_4e_tableau.png"),
        [["Triangle $AMN$", "$AM$", "$AN$", "$MN$"], ["Triangle $ABC$", "$AB$", "$AC$", "$BC$"]],
        larg_col=[3.0, 1.5, 1.5, 1.5], titre="Les longueurs sont proportionnelles (coefficient $k$)")


# ================================================================== DÉCOUVERTE
def trois_configs(path):
    fig, ax = new_fig(11.0, 4.0)
    for i in range(3):
        x0 = i * 4.1
        A, B, Cc = P(x0 + 1.0, 3), P(x0, 0), P(x0 + 3.2, 0)
        ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=LBLUE, edgecolor="none", zorder=0))
        ax.plot([A[0], B[0], Cc[0], A[0]], [A[1], B[1], Cc[1], A[1]], lw=2, color=BLUE)
        M = A + 0.45 * (B - A)
        if i == 0:
            N = A + 0.45 * (Cc - A)
            add_parallel_marks(ax, M, N, 2, size=0.18, spacing=0.2, color=ORANGE)
            add_parallel_marks(ax, B, Cc, 2, size=0.18, spacing=0.2, color=BLUE)
        elif i == 1:
            N = A + 0.62 * (Cc - A)
        else:
            N = B + 0.62 * (Cc - B)
        ax.plot([M[0], N[0]], [M[1], N[1]], lw=2, color=ORANGE)
        G = (A + B + Cc) / 3
        dN = normale_hors(A, Cc, B) if i < 2 else P(0, -1)
        for Pt, nom, d in [(A, "A", A - G), (B, "B", B - G), (Cc, "C", Cc - G),
                           (M, "M", normale_hors(A, B, Cc)), (N, "N", dN)]:
            point(ax, Pt, nom, d, fs=12.5, s=20)
        ax.text(x0 + 1.6, -0.95, ["figure a", "figure b", "figure c"][i], ha="center", fontsize=12.5,
                color=DARK, fontweight="bold")
    ax.text(5.7, 3.75, "Les codes « // » indiquent des droites parallèles.", ha="center", fontsize=11,
            color=NEUTRAL)
    ax.set_xlim(-0.6, 12.0)
    ax.set_ylim(-1.3, 4.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


trois_configs(X("thales_4e_trois_configs.png"))

# D2 : nommer, puis écrire les rapports
config(X("thales_4e_d2.png"), k=0.4, ABC=tri(5, 7.5, 6.5), noms="RSTUV")

# D3 : AM = 3, AB = 5, AC = 10, BC = 8
T3 = tri(5, 10, 8)
D3 = [("AM", "3 cm", "d"), ("AB", "5 cm", "d"), ("AC", "10 cm", "d"), ("BC", "8 cm", "d")]
config(X("thales_4e_d3.png"), k=0.6, ABC=T3, cotes=D3 + [("AN", "?", "q"), ("MN", "?", "q")])
config(X("thales_4e_d3_solution.png"), k=0.6, ABC=T3,
       cotes=D3 + [("AN", "6 cm", "s"), ("MN", "4,8 cm", "s"), ("NC", "4 cm", "s", dict(t=0.8))])

# D4 : AM = 4, AB = 10, AC = 12, BC = 15
T4 = tri(10, 12, 15)
D4 = [("AM", "4 cm", "d"), ("AB", "10 cm", "d"), ("AC", "12 cm", "d"), ("BC", "15 cm", "d")]
config(X("thales_4e_d4.png"), k=0.4, ABC=T4, cotes=D4)
config(X("thales_4e_d4_solution.png"), k=0.4, ABC=T4,
       cotes=D4 + [("AN", "4,8 cm", "s"), ("MN", "6 cm", "s")])

# D5 : AM = 4, MB = 6, AN = 6, MN = 5
T5 = tri(10, 15, 12.5)
D5 = [("AM", "4 cm", "d"), ("MB", "6 cm", "d"), ("AN", "6 cm", "d"), ("MN", "5 cm", "d")]
config(X("thales_4e_d5.png"), k=0.4, ABC=T5, cotes=D5)
config(X("thales_4e_d5_solution.png"), k=0.4, ABC=T5,
       cotes=D5 + [("NC", "9 cm", "s"), ("BC", "12,5 cm", "s"),
                   ("AC", "15 cm", "s", dict(off=1.15))])

# D6 : AM = 2, AB = 8, AC = 6, BC = 9 + tableau
T6 = tri(8, 6, 9)
config(X("thales_4e_d6.png"), k=0.25, ABC=T6,
       cotes=[("AM", "2 cm", "d", dict(off=0.38)), ("AB", "8 cm", "d", dict(off=1.0)),
              ("AC", "6 cm", "d", dict(off=0.95)), ("BC", "9 cm", "d")])
tableau(X("thales_4e_d6_tableau.png"),
        [["", "côté 1", "côté 2", "côté 3"], ["Triangle $AMN$", "$AM = 2$", "$AN = ?$", "$MN = ?$"],
         ["Triangle $ABC$", "$AB = 8$", "$AC = 6$", "$BC = 9$"]],
        larg_col=[2.9, 1.9, 1.9, 1.9], surligne=[(1, 2), (1, 3)], titre="Longueurs en cm")
tableau(X("thales_4e_d6_tableau_solution.png"),
        [["", "côté 1", "côté 2", "côté 3"], ["Triangle $AMN$", "$AM = 2$", "$AN = 1{,}5$", "$MN = 2{,}25$"],
         ["Triangle $ABC$", "$AB = 8$", "$AC = 6$", "$BC = 9$"]],
        larg_col=[2.9, 1.9, 1.9, 1.9], vert=[(1, 2), (1, 3)], titre="Coefficient : $\\times\\, 0{,}25$")

# D7 : vrai / faux — AM = 2, MB = 3, AN = 3, MN = 4
T7 = tri(5, 7.5, 10)
D7 = [("AM", "2 cm", "d"), ("MB", "3 cm", "d"), ("AN", "3 cm", "d"), ("MN", "4 cm", "d")]
config(X("thales_4e_d7.png"), k=0.4, ABC=T7, cotes=D7)
config(X("thales_4e_d7_solution.png"), k=0.4, ABC=T7,
       cotes=D7 + [("NC", "4,5 cm", "s"), ("BC", "10 cm", "s")])


# ================================================================ ENTRAÎNEMENT
def arbre(ax, x, h, r=1.4, pied=0):
    ax.plot([x, x], [pied, h], lw=6, color="#8d6e63", solid_capstyle="round", zorder=1)
    for dx, dy, rr in [(0, 0.3, r), (-0.8 * r / 1.4, -0.5 * r / 1.4, r * 0.72),
                       (0.8 * r / 1.4, -0.5 * r / 1.4, r * 0.72)]:
        ax.add_patch(Circle((x + dx, h + dy), rr, facecolor="#7cb342", edgecolor="#558b2f", alpha=0.45,
                            zorder=0))


def ombre(path, solution=False):
    fig, ax = new_fig(8.6, 5.0)
    ax.plot([-0.6, 13.6], [0, 0], lw=2, color=NEUTRAL)
    arbre(ax, 12, 9)
    ax.plot([2, 2], [0, 1.5], lw=4, color=ORANGE, solid_capstyle="round")
    ax.plot([0, 12], [0, 9], lw=1.6, color="#f39c12", ls="--")
    ax.text(4.6, 4.3, "rayon de soleil", fontsize=11, color="#d68910", rotation=36.87, ha="center")
    for x1, x2, y, t in [(0, 2, -0.6, "2 m"), (0, 12, -1.7, "12 m")]:
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="<->", color=DARK))
        ax.text((x1 + x2) / 2, y - 0.2, t, ha="center", va="top", fontsize=12)
    ax.text(2.3, 0.8, "bâton : 1,5 m", fontsize=11.5, color=ORANGE, fontweight="bold", va="center")
    ax.text(12.5, 4.2, "9 m" if solution else "?", fontsize=14, color=GREEN if solution else ORANGE,
            fontweight="bold")
    if solution:
        ax.text(9.2, 5.7, "15 m", fontsize=12.5, color=GREEN, fontweight="bold", rotation=36.87, ha="center",
                va="center")
    right_angle(ax, P(12, 0), (-1, 0), (0, 1), size=0.45)
    right_angle(ax, P(2, 0), (-1, 0), (0, 1), size=0.35)
    for Pt, nom, d in [(P(0, 0), "S", (-1, -0.6)), (P(2, 0), "B", (0.7, -1)), (P(2, 1.5), "M", (-0.7, 1)),
                       (P(12, 0), "C", (1, -0.8)), (P(12, 9), "N", (-1, 0.5))]:
        point(ax, Pt, nom, d)
    ax.set_xlim(-1.0, 14.2)
    ax.set_ylim(-2.8, 10.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


ombre(C("thales_4e_ombre.png"), solution=True)
ombre(X("thales_4e_ombre.png"))
ombre(X("thales_4e_ombre_solution.png"), solution=True)

# E2 : décimaux — AM = 2,4 ; AB = 6 ; AN = 3 ; MN = 3,2
TE2 = tri(6, 7.5, 8)
E2 = [("AM", "2,4 cm", "d"), ("AB", "6 cm", "d"), ("AN", "3 cm", "d"), ("MN", "3,2 cm", "d")]


def trapeze(ax, p):
    ax.add_patch(Polygon([p["M"], p["B"], p["C"], p["N"]], closed=True, facecolor=LGREEN, edgecolor=GREEN,
                         lw=0, hatch="//", alpha=0.6, zorder=0))


config(X("thales_4e_e2.png"), k=0.4, ABC=TE2, cotes=E2)
config(X("thales_4e_e2_solution.png"), k=0.4, ABC=TE2, extra=trapeze,
       cotes=E2 + [("MB", "3,6 cm", "s"), ("NC", "4,5 cm", "s"), ("BC", "8 cm", "s"),
                   ("AC", "7,5 cm", "s", dict(off=1.15))])


# E3 : deux parallèles — AM = 2, MP = 3, PB = 3, AN = 3, MN = 2,5
def deux_paralleles(path, solution=False):
    A, B, Cc = tri(8, 12, 10)
    kM, kP = 0.25, 0.625
    M, N = A + kM * (B - A), A + kM * (Cc - A)
    Pp, Q = A + kP * (B - A), A + kP * (Cc - A)
    fig, ax = new_fig(7.4, 5.8)
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=LBLUE, edgecolor="none", zorder=0))
    ax.plot([B[0], A[0], Cc[0], B[0]], [B[1], A[1], Cc[1], B[1]], lw=2.3, color=BLUE)
    for S, T, col in [(M, N, ORANGE), (Pp, Q, ORANGE), (B, Cc, BLUE)]:
        ax.plot([S[0], T[0]], [S[1], T[1]], lw=2.3, color=col)
        add_parallel_marks(ax, S, T, 2, size=0.26, color=col)
    nAB, nAC = normale_hors(A, B, Cc), normale_hors(A, Cc, B)
    cote(ax, A, M, "2 cm", nAB)
    cote(ax, M, Pp, "3 cm", nAB)
    cote(ax, Pp, B, "3 cm", nAB)
    cote(ax, A, N, "3 cm", nAC)
    cote(ax, M, N, "2,5 cm", P(0, 1), off=-0.32)
    if solution:
        cote(ax, N, Q, "4,5 cm", nAC, "s")
        cote(ax, Q, Cc, "4,5 cm", nAC, "s")
        cote(ax, Pp, Q, "6,25 cm", P(0, 1), "s", off=0.32)
        cote(ax, B, Cc, "10 cm", P(0, -1), "s")
        cote(ax, A, Cc, "AC = 12 cm", nAC, "s", off=1.3, fleche=True, t=0.3)
    G = (A + B + Cc) / 3
    for Pt, nom, d in [(A, "A", A - G), (B, "B", B - G), (Cc, "C", Cc - G), (M, "M", nAB + 0.3 * unit(A - B)),
                       (Pp, "P", nAB + 0.3 * unit(A - B)), (N, "N", nAC + 0.3 * unit(A - Cc)),
                       (Q, "Q", nAC + 0.3 * unit(A - Cc))]:
        point(ax, Pt, nom, d)
    finish(fig, ax, path, [A, B, Cc], margin=1.2)


deux_paralleles(X("thales_4e_deux_paralleles.png"))
deux_paralleles(X("thales_4e_deux_paralleles_solution.png"), solution=True)

# E4 : le toit — AB = AC = 6 m, BC = 9 m, AM = 2 m
TT = tri(6, 6, 9, base=7.6)


def mur(ax, p):
    B, Cc = p["B"], p["C"]
    ax.add_patch(Rectangle((B[0] + 0.5, -1.5), Cc[0] - B[0] - 1.0, 1.5, facecolor="#f2f2f2",
                           edgecolor=NEUTRAL, lw=1.2, zorder=0))
    ax.text((B[0] + Cc[0]) / 2, -1.05, "mur", ha="center", fontsize=11, color=NEUTRAL)


def toit_sol(ax, p):
    mur(ax, p)
    A, B, Cc, M = p["A"], p["B"], p["C"], p["M"]
    H = (B + Cc) / 2
    K = P(H[0], M[1])
    ax.plot([A[0], H[0]], [A[1], H[1]], lw=1.6, color=GREEN, ls="--")
    right_angle(ax, H, (1, 0), (0, 1), size=0.25, color=GREEN)
    point(ax, H, "H", (0.6, -1))
    point(ax, K, "K", (0.8, 0.9))
    ax.text(H[0] + 0.15, (H[1] + K[1]) / 2, "≈ 2,65 m", fontsize=11, color=GREEN, fontweight="bold")


ET = [("AB", "6 m", "d"), ("AC", "6 m", "d"), ("BC", "9 m", "d", dict(t=0.25, off=0.35)),
      ("AM", "2 m", "d", dict(off=0.38))]
config(X("thales_4e_toit.png"), k=1 / 3, ABC=TT, cotes=ET, extra=mur, couleurs=("#f6ddcc", "#fdebd0"),
       para_mn=(0.4, 1), para_bc=(0.45, 1))
config(X("thales_4e_toit_solution.png"), k=1 / 3, ABC=TT, extra=toit_sol, couleurs=("#f6ddcc", "#fdebd0"),
       para_mn=(0.4, 1), para_bc=(0.45, 1), cotes=ET + [("MN", "3 m", "s", dict(t=0.25, off=-0.3))])

# E5 : avec une inconnue — AM = x, MB = 4, AN = 3, NC = 6
T5i = tri(6, 9, 7.5)
E5 = [("MB", "4 cm", "d"), ("AN", "3 cm", "d"), ("NC", "6 cm", "d")]
config(X("thales_4e_inconnue.png"), k=1 / 3, ABC=T5i, cotes=E5 + [("AM", "$x$", "q", dict(fs=15))])
config(X("thales_4e_inconnue_solution.png"), k=1 / 3, ABC=T5i,
       cotes=E5 + [("AM", "2 cm", "s"), ("MN", "2,5 cm", "d"), ("BC", "7,5 cm", "s")])

# E6 : erreurs — AM = 3, MB = 2, AN = 4,5, BC = 8
T6e = tri(5, 7.5, 8)
E6 = [("AM", "3 cm", "d"), ("MB", "2 cm", "d"), ("AN", "4,5 cm", "d"), ("BC", "8 cm", "d")]
config(X("thales_4e_e6.png"), k=0.6, ABC=T6e, cotes=E6)
config(X("thales_4e_e6_solution.png"), k=0.6, ABC=T6e,
       cotes=E6 + [("MN", "4,8 cm", "s"), ("NC", "3 cm", "s")])

# E7 : Thalès et Pythagore — ABC rectangle en B, AB = 8, BC = 6, AM = 2
T7r = tri(8, 10, 6, base=5.4)
E7 = [("AB", "8 cm", "d"), ("BC", "6 cm", "d"), ("AM", "2 cm", "d", dict(off=0.4))]
config(X("thales_4e_e7.png"), k=0.25, ABC=T7r, cotes=E7, droit="B", w=5.6, h=6.4)
config(X("thales_4e_e7_solution.png"), k=0.25, ABC=T7r, droit="BM", w=5.6, h=6.4,
       cotes=E7 + [("AC", "10 cm", "s"), ("AN", "2,5 cm", "s", dict(off=0.5)),
                   ("MN", "1,5 cm", "s", dict(off=-0.32))])


# =================================================================== PROBLÈMES
def visee(path, solution=False):
    fig, ax = new_fig(8.8, 4.8)
    ax.plot([-0.6, 21.5], [0, 0], lw=2, color=NEUTRAL)
    arbre(ax, 20, 9, r=1.6)
    ax.plot([4, 4], [0, 1.8], lw=5, color=BLUE, solid_capstyle="round")
    ax.plot([0, 20], [0, 9], lw=1.5, color=ORANGE, ls="--")
    ax.text(9.5, 5.0, "ligne de visée", fontsize=11, color=ORANGE, rotation=24.2, ha="center")
    for x1, x2, y, t in [(0, 4, -0.7, "4 m"), (0, 20, -1.9, "20 m")]:
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="<->", color=DARK))
        ax.text((x1 + x2) / 2, y - 0.2, t, ha="center", va="top", fontsize=12)
    ax.text(4.4, 1.0, "Hugo : 1,8 m", fontsize=11.5, color=BLUE, fontweight="bold", va="center")
    ax.text(20.6, 4.0, "9 m" if solution else "?", fontsize=14, color=GREEN if solution else ORANGE,
            fontweight="bold")
    right_angle(ax, P(4, 0), (-1, 0), (0, 1), size=0.45)
    right_angle(ax, P(20, 0), (-1, 0), (0, 1), size=0.6)
    for Pt, nom, d in [(P(0, 0), "O", (-1, -0.6)), (P(4, 0), "H", (0.8, -1)), (P(4, 1.8), "T", (-0.4, 1)),
                       (P(20, 0), "B", (1, -0.8)), (P(20, 9), "S", (-1, 0.6))]:
        point(ax, Pt, nom, d)
    ax.set_xlim(-1.2, 23.4)
    ax.set_ylim(-3.0, 11.2)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


visee(X("thales_4e_visee.png"))
visee(X("thales_4e_visee_solution.png"), solution=True)


def panneau(path, solution=False):
    A, B, Cc = tri(90, 90, 90, base=7.2)
    fig, ax = new_fig(6.6, 6.2)
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor="white", edgecolor="#c0392b", lw=5,
                         joinstyle="round"))
    pts = {}
    for t, (n1, n2) in [(1 / 3, ("M", "N")), (2 / 3, ("P", "Q"))]:
        M, N = A + t * (B - A), A + t * (Cc - A)
        pts[n1], pts[n2] = M, N
        ax.plot([M[0], N[0]], [M[1], N[1]], lw=3, color=ORANGE)
        add_parallel_marks(ax, M + 0.5 * (N - M), N, 2, size=0.24, color=ORANGE)
        if solution:
            cote(ax, M, N, f"{int(round(90 * t))} cm", P(0, -1), "s", off=0.32, t=0.3)
    add_parallel_marks(ax, B + 0.5 * (Cc - B), Cc, 2, size=0.24, color="#c0392b")
    nAB = normale_hors(A, B, Cc)
    cote(ax, A, pts["M"], "30 cm", nAB, off=0.55)
    cote(ax, A, pts["P"], "AP = 60 cm", nAB, off=1.45, fleche=True, t=0.5)
    cote(ax, B, Cc, "90 cm", P(0, -1), off=0.5, t=0.25)
    if solution:
        H = (B + Cc) / 2
        K = P(H[0], pts["M"][1])
        ax.plot([A[0], H[0]], [A[1], H[1]], lw=1.5, color=GREEN, ls="--")
        right_angle(ax, H, (1, 0), (0, 1), size=0.25, color=GREEN)
        point(ax, H, "H", (0.7, -1))
        point(ax, K, "K", (-0.9, 0.9))
    G = (A + B + Cc) / 3
    for Pt, nom, d in [(A, "A", A - G), (B, "B", B - G), (Cc, "C", Cc - G)]:
        point(ax, Pt, nom, d)
    for nom in "MP":
        point(ax, pts[nom], nom, nAB + 0.3 * unit(A - B))
    for nom in "NQ":
        point(ax, pts[nom], nom, normale_hors(A, Cc, B) + 0.3 * unit(A - Cc))
    finish(fig, ax, path, [A, B, Cc], margin=1.4)


panneau(X("thales_4e_panneau.png"))
panneau(X("thales_4e_panneau_solution.png"), solution=True)

# P3 : l'étang — AM = 12, MB = 36, AN = 13, MN = 15
TE = tri(48, 52, 60)


def etang(ax, p, solution=False):
    B, Cc = p["B"], p["C"]
    mid = (B + Cc) / 2
    ax.add_patch(Ellipse((mid[0], mid[1] - 0.15), (Cc[0] - B[0]) * 0.86, 1.9, facecolor="#b3d9f2",
                         edgecolor="#5dade2", lw=1.2, zorder=0))
    ax.text(mid[0], mid[1] - 0.75, "étang", ha="center", fontsize=12, color="#21618c", fontweight="bold")
    if solution:
        ax.text(mid[0], mid[1] + 0.3, "BC = 60 m", ha="center", fontsize=13, color=GREEN, fontweight="bold")


EE = [("AM", "12 m", "d"), ("MB", "36 m", "d"), ("AN", "13 m", "d"), ("MN", "15 m", "d")]
config(X("thales_4e_etang.png"), k=0.25, ABC=TE, cotes=EE, bc_ls="--", extra=etang, fill=False, marge=1.4)
config(X("thales_4e_etang_solution.png"), k=0.25, ABC=TE, bc_ls="--", fill=False, marge=1.4,
       extra=lambda ax, p: etang(ax, p, True), cotes=EE + [("NC", "39 m", "s")])


def rect_inscrit(path, solution=False):
    B, Cc, A = P(0, 0), P(12, 0), P(5, 8)
    x = 3
    xl = (A[0] - B[0]) * x / 8
    xr = Cc[0] + (A[0] - Cc[0]) * x / 8
    M, N, Pp, Q, H, K = P(xl, x), P(xr, x), P(xr, 0), P(xl, 0), P(A[0], 0), P(A[0], x)
    fig, ax = new_fig(7.6, 5.6)
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.3))
    ax.add_patch(Polygon([M, N, Pp, Q], closed=True, facecolor=LORANGE, edgecolor=ORANGE, lw=2.3))
    ax.plot([A[0], H[0]], [A[1], H[1]], lw=1.4, color=NEUTRAL, ls=":")
    right_angle(ax, H, (1, 0), (0, 1), size=0.3)
    right_angle(ax, Q, (1, 0), (0, 1), size=0.3, color=ORANGE)
    right_angle(ax, Pp, (-1, 0), (0, 1), size=0.3, color=ORANGE)
    ax.text(A[0] + 0.18, 6.0, "8", fontsize=13, color=DARK)
    cote(ax, B, Cc, "12", P(0, -1), off=0.45, t=0.6)
    ax.text(xr + 0.2, x / 2, "$x$", fontsize=15, color=ORANGE, va="center", fontweight="bold")
    if solution:
        ax.text(A[0] + 0.18, 5.4, "AK = 5", fontsize=12, color=GREEN, fontweight="bold")
        ax.text((xl + A[0]) / 2, x + 0.3, "MN = 7,5", fontsize=12, color=GREEN, fontweight="bold", ha="center")
    nAB, nAC = normale_hors(A, B, Cc), normale_hors(A, Cc, B)
    for Pt, nom, d in [(A, "A", (0, 1)), (B, "B", (-1, -0.6)), (Cc, "C", (1, -0.6)), (M, "M", nAB),
                       (N, "N", nAC), (Pp, "P", (0.4, -1)), (Q, "Q", (-0.4, -1)), (H, "H", (0, -1)),
                       (K, "K", (0.7, 0.8))]:
        point(ax, Pt, nom, d)
    finish(fig, ax, path, [A, B, Cc], margin=0.9)


rect_inscrit(X("thales_4e_rectangle_inscrit.png"))
rect_inscrit(X("thales_4e_rectangle_inscrit_solution.png"), solution=True)

# P5 : l'escabeau — AB = AC = 2 m, AM = 0,5 m, MN = 0,4 m
TS = tri(2, 2, 1.6, base=3.2)


def sol_escabeau(ax, p, solution=False):
    B, Cc, A = p["B"], p["C"], p["A"]
    ax.plot([B[0] - 0.8, Cc[0] + 0.8], [0, 0], lw=2, color=NEUTRAL)
    for E in (B, Cc):
        ax.add_patch(Rectangle((E[0] - 0.08, -0.05), 0.16, 0.1, color="#566573"))
    if solution:
        H = (B + Cc) / 2
        ax.plot([A[0], H[0]], [A[1], H[1]], lw=1.5, color=GREEN, ls="--")
        right_angle(ax, H, (1, 0), (0, 1), size=0.16, color=GREEN)
        point(ax, H, "H", (0.6, -1))
        ax.text(H[0] - 0.08, A[1] * 0.25, "≈ 1,83 m", fontsize=11, color=GREEN, fontweight="bold", ha="right")
    N = p["N"]
    ax.text(N[0] + 0.2, N[1], "0,4 m", fontsize=11.5, color=ORANGE, ha="left", va="center", fontweight="bold")


ES = [("AB", "2 m", "d", dict(off=0.55)), ("AM", "0,5 m", "d", dict(off=0.3, fs=11.5))]
config(X("thales_4e_escabeau.png"), k=0.25, ABC=TS, cotes=ES, fill=False, bc_ls=":", w=5.4, h=6.0, lw=4,
       para_bc=(0.5, 1),
       extra=sol_escabeau, marge=0.7)
config(X("thales_4e_escabeau_solution.png"), k=0.25, ABC=TS, fill=False, bc_ls=":", w=5.4, h=6.0, lw=4,
       para_bc=(0.5, 1),
       extra=lambda ax, p: sol_escabeau(ax, p, True), marge=0.7,
       cotes=ES + [("BC", "1,6 m", "s", dict(off=0.35))])


# P6 : la rampe — AC = 12 m, CB = 0,6 m, supports à 3, 6, 9 m (échelle verticale exagérée)
def rampe(path, solution=False):
    sx, sy = 0.75, 3.6
    A, Cc, B = P(0, 0), P(12 * sx, 0), P(12 * sx, 0.6 * sy)
    fig, ax = new_fig(9.0, 3.8)
    ax.plot([-0.6, Cc[0] + 1.6], [0, 0], lw=2, color=NEUTRAL)
    ax.add_patch(Polygon([A, Cc, B], closed=True, facecolor=LBLUE, edgecolor="none", zorder=0))
    ax.plot([A[0], B[0]], [A[1], B[1]], lw=3.2, color=BLUE)
    ax.plot([Cc[0], B[0]], [Cc[1], B[1]], lw=2.6, color=BLUE)
    ax.add_patch(Rectangle((Cc[0], 0), 1.4, B[1], facecolor="#f2f2f2", edgecolor=NEUTRAL, lw=1.2))
    ax.text(Cc[0] + 0.7, B[1] / 2, "porte", ha="center", va="center", fontsize=10.5, color=NEUTRAL,
            rotation=90)
    for d, nd, nr in [(3, "D", "R"), (6, "E", "S"), (9, "F", "T")]:
        G, Rr = P(d * sx, 0), P(d * sx, 0.05 * d * sy)
        ax.plot([G[0], Rr[0]], [G[1], Rr[1]], lw=2.4, color=ORANGE)
        right_angle(ax, G, (1, 0), (0, 1), size=0.16)
        point(ax, G, nd, (0, -1))
        point(ax, Rr, nr, (-0.5, 1))
        if solution:
            ax.text(G[0] + 0.12, Rr[1] / 2, f"{0.05 * d:.2f}".replace(".", ",") + " m", fontsize=10.5,
                    color=GREEN, fontweight="bold", va="center")
    right_angle(ax, Cc, (-1, 0), (0, 1), size=0.16)
    point(ax, A, "A", (-1, -0.4))
    point(ax, Cc, "C", (0.6, -1))
    point(ax, B, "B", (-0.6, 1))
    ax.text(Cc[0] - 0.12, B[1] / 2, "0,6 m", fontsize=11.5, color=DARK, ha="right", va="center")
    for i in range(4):
        x1, x2, y = 3 * i * sx, 3 * (i + 1) * sx, -0.75
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="<->", color=DARK, lw=1))
        ax.text((x1 + x2) / 2, y - 0.12, "3 m", ha="center", va="top", fontsize=11)
    ax.text(Cc[0] / 2, -1.55, "AC = 12 m (échelle verticale exagérée)", ha="center", fontsize=10.5,
            color=NEUTRAL, va="top")
    ax.set_xlim(-1.0, Cc[0] + 2.0)
    ax.set_ylim(-2.1, B[1] + 0.8)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


rampe(X("thales_4e_rampe.png"))
rampe(X("thales_4e_rampe_solution.png"), solution=True)


# P7 : la largeur de la rivière — AM = x, MB = 8, MN = 15, BC = 20
def riviere(path, solution=False):
    s = 0.25
    A, M, B = P(0.5, 24 * s), P(0.5, 0), P(0.5, -8 * s)
    Cc = B + P(20 * s, 0)
    N = A + 0.75 * (Cc - A)
    fig, ax = new_fig(7.4, 6.6)
    ax.add_patch(Rectangle((-1.4, 0), 9.0, 6, facecolor="#cfe8f7", edgecolor="none", zorder=0))
    ax.plot([-1.4, 7.6], [0, 0], lw=2, color="#5dade2")
    ax.plot([-1.4, 7.6], [6, 6], lw=2, color="#5dade2")
    ax.text(5.6, 3.0, "rivière", fontsize=14, color="#21618c", fontweight="bold", ha="center")
    ax.text(5.6, 6.25, "rive d'en face", fontsize=10.5, color=NEUTRAL, ha="center")
    ax.text(6.4, -0.45, "rive où l'on est", fontsize=10.5, color=NEUTRAL, ha="center")
    arbre(ax, A[0], A[1] + 0.75, r=0.45, pied=A[1])
    ax.plot([A[0], B[0]], [A[1], B[1]], lw=1.6, color=BLUE, ls="--")
    ax.plot([A[0], Cc[0]], [A[1], Cc[1]], lw=1.6, color=BLUE, ls="--")
    ax.plot([M[0], N[0]], [M[1], N[1]], lw=2.4, color=ORANGE)
    ax.plot([B[0], Cc[0]], [B[1], Cc[1]], lw=2.4, color=ORANGE)
    add_parallel_marks(ax, M, N, 2, size=0.24, color=ORANGE)
    add_parallel_marks(ax, B, Cc, 2, size=0.24, color=ORANGE)
    right_angle(ax, M, (1, 0), (0, 1), size=0.25)
    cote(ax, M, B, "8 m", P(-1, 0), off=0.45)
    cote(ax, M, N, "15 m", P(0, -1), off=0.3, t=0.62)
    cote(ax, B, Cc, "20 m", P(0, -1), off=0.35)
    cote(ax, A, M, "24 m" if solution else "$x$", P(-1, 0), "s" if solution else "q", off=0.5,
         fs=13 if solution else 15)
    for Pt, nom, d in [(A, "A", (-1, 0.5)), (M, "M", (-0.9, 0.6)), (B, "B", (-1, -0.5)), (N, "N", (0.6, 0.8)),
                       (Cc, "C", (1, -0.5))]:
        point(ax, Pt, nom, d)
    ax.set_xlim(-1.4, 7.6)
    ax.set_ylim(-2.8, 7.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


riviere(X("thales_4e_riviere.png"))
riviere(X("thales_4e_riviere_solution.png"), solution=True)
