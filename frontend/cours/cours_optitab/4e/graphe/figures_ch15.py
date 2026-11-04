# -*- coding: utf-8 -*-
"""Figures du chapitre 15 (cosinus dans le triangle rectangle) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, finish, _save, right_angle, angle_arc, tableau,
                   BLUE, ORANGE, GREEN, DARK, NEUTRAL, DIR_COURS, DIR_EXOS)
import numpy as np
from math import cos, sin, radians, sqrt, degrees, acos
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
P = lambda x, y: np.array([x, y], float)  # noqa: E731
LBLUE, LORANGE, LGREEN, GRIS = "#d6eafc", "#fdebd0", "#e8f5e9", "#7f8c8d"
STYLE = {"d": (DARK, "normal"), "q": (ORANGE, "bold"), "s": (GREEN, "bold"), "b": (BLUE, "bold")}


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


def cote(ax, Pa, Qa, txt, n, style="d", off=0.42, t=0.5, fs=12.5):
    col, wt = STYLE[style]
    pos = Pa + t * (Qa - Pa) + off * n
    ax.text(pos[0], pos[1], txt, color=col, fontsize=fs, ha="center", va="center", fontweight=wt,
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))


def angle(ax, V, P1, P2, txt=None, col=ORANGE, r=0.7, fs=13, lr=None):
    angle_arc(ax, V, P1 - V, P2 - V, r=r, color=col, lw=2, label=txt, fs=fs,
              label_r=lr if lr is not None else r + 0.5)


def pts_rect(hyp, a, rot=0.0, sens=1, s=1.0):
    """Triangle rectangle : sommet V de l'angle a (en degrés) en (0, 0), angle droit en R, T troisième sommet."""
    u = P(cos(radians(rot)), sin(radians(rot)))
    n = P(-u[1], u[0]) * sens
    V = P(0, 0)
    R = V + s * hyp * cos(radians(a)) * u
    T = R + s * hyp * sin(radians(a)) * n
    return R, V, T


def rect(path, R, V, T, noms="ABC", ang=None, ang_col=ORANGE, cotes=(), couleurs=False, extra=None,
         w=6.8, h=5.0, marge=1.0, fill=LBLUE, legende=False, ang_r=0.75):
    """Triangle rectangle en R ; angle marqué en V. cotes = [(côté parmi RV, VT, RT, texte, style, opts)]."""
    fig, ax = new_fig(w, h)
    ax.add_patch(Polygon([R, V, T], closed=True, facecolor=fill, edgecolor="none", zorder=0))
    if couleurs:
        ax.plot([R[0], V[0]], [R[1], V[1]], lw=4, color=ORANGE, solid_capstyle="round")
        ax.plot([V[0], T[0]], [V[1], T[1]], lw=4, color=BLUE, solid_capstyle="round")
        ax.plot([R[0], T[0]], [R[1], T[1]], lw=2.4, color=GRIS, solid_capstyle="round")
    else:
        ax.plot([R[0], V[0], T[0], R[0]], [R[1], V[1], T[1], R[1]], lw=2.3, color=BLUE)
    right_angle(ax, R, V - R, T - R, size=0.32)
    if ang:
        angle(ax, V, R, T, ang, ang_col, r=ang_r)
    S = {"R": R, "V": V, "T": T}
    third = {"RV": "T", "VT": "R", "RT": "V"}
    for c in cotes:
        seg, txt, style = c[:3]
        opt = dict(c[3]) if len(c) > 3 else {}
        Pa, Qa = S[seg[0]], S[seg[1]]
        cote(ax, Pa, Qa, txt, normale_hors(Pa, Qa, S[third[seg]]), style, **opt)
    G = (R + V + T) / 3
    for Pt, nom in zip((R, V, T), noms):
        point(ax, Pt, nom, Pt - G)
    if legende:
        nV, nR, nT = noms
        y0 = min(R[1], V[1], T[1]) - 1.0
        x0 = min(R[0], V[0], T[0])
        for i, (col, txt) in enumerate([(BLUE, f"hypoténuse $[{nV}{nT}]$"),
                                        (ORANGE, f"côté adjacent à l'angle ${nV}$ : $[{nV}{nR}]$")]):
            ax.plot([x0, x0 + 0.6], [y0 - 0.55 * i] * 2, lw=4, color=col)
            ax.text(x0 + 0.8, y0 - 0.55 * i, txt, va="center", fontsize=12, color=col, fontweight="bold")
    if extra:
        extra(ax, S)
    pts = [R, V, T] + ([P(min(R[0], V[0], T[0]), min(R[1], V[1], T[1]) - 1.6)] if legende else [])
    finish(fig, ax, path, pts, margin=marge)


# ======================================================================= COURS
def vocabulaire(path):
    R, V, T = P(6.4, 0), P(0, 0), P(6.4, 4.2)
    fig, ax = new_fig(7.6, 5.0)
    ax.add_patch(Polygon([R, V, T], closed=True, facecolor=LBLUE, edgecolor="none", zorder=0))
    ax.plot([R[0], V[0]], [R[1], V[1]], lw=4.5, color=ORANGE, solid_capstyle="round")
    ax.plot([V[0], T[0]], [V[1], T[1]], lw=4.5, color=BLUE, solid_capstyle="round")
    ax.plot([R[0], T[0]], [R[1], T[1]], lw=3, color=GRIS, solid_capstyle="round")
    right_angle(ax, R, V - R, T - R, size=0.36)
    angle(ax, V, R, T, None, ORANGE, r=1.0)
    ax.text(1.75, 0.42, "angle $\\widehat{B}$", fontsize=12, color=ORANGE, fontweight="bold")
    ax.text(2.6, 2.55, "hypoténuse", fontsize=14, color=BLUE, fontweight="bold", rotation=33.3, ha="center")
    ax.text(3.2, -0.55, "côté adjacent à l'angle $\\widehat{B}$", fontsize=13, color=ORANGE, fontweight="bold",
            ha="center", va="top")
    ax.text(6.75, 2.1, "côté opposé\nà l'angle $\\widehat{B}$", fontsize=12.5, color=GRIS, fontweight="bold",
            va="center")
    for Pt, nom, d in [(R, "A", (1, -0.6)), (V, "B", (-1, -0.4)), (T, "C", (0.3, 1))]:
        point(ax, Pt, nom, d)
    ax.text(3.2, 5.0, "$\\cos \\widehat{B} = \\dfrac{\\mathrm{côté\\ adjacent}}{\\mathrm{hypoténuse}}"
            " = \\dfrac{BA}{BC}$", fontsize=17, color=DARK, ha="center")
    ax.set_xlim(-0.8, 9.2)
    ax.set_ylim(-1.4, 5.8)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


vocabulaire(C("cosinus_4e_vocabulaire.png"))


def independance(path):
    a = 35
    fig, ax = new_fig(8.6, 4.6)
    u, v = P(1, 0), P(cos(radians(a)), sin(radians(a)))
    B = P(0, 0)
    ax.plot([0, 10.2], [0, 0], lw=2.2, color=DARK)
    ax.plot([0, 10.2 / cos(radians(a)) * v[0]], [0, 10.2 / cos(radians(a)) * v[1]], lw=2.2, color=DARK)
    for i, (d, col) in enumerate([(3.2, ORANGE), (6.0, GREEN), (9.2, BLUE)], 1):
        A = d * u
        Cc = d / cos(radians(a)) * v
        ax.plot([A[0], Cc[0]], [A[1], Cc[1]], lw=2.2, color=col)
        right_angle(ax, A, -u, Cc - A, size=0.25)
        point(ax, A, f"A_{i}", (0.2, -1), fs=13)
        point(ax, Cc, f"C_{i}", (-0.5, 1), fs=13)
    angle(ax, B, P(1, 0), v, "35°", ORANGE, r=1.0)
    point(ax, B, "B", (-1, -0.3))
    ax.text(5.2, -1.25, "$\\dfrac{BA_1}{BC_1} = \\dfrac{BA_2}{BC_2} = \\dfrac{BA_3}{BC_3} = \\cos 35° \\approx 0{,}82$",
            fontsize=15, color=DARK, ha="center", va="top")
    ax.set_xlim(-0.9, 11.0)
    ax.set_ylim(-2.6, 7.0)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


independance(C("cosinus_4e_independance.png"))


def ecran(ax, x, y, saisie, resultat, titre):
    ax.add_patch(FancyBboxPatch((x, y), 5.2, 2.3, boxstyle="round,pad=0.12,rounding_size=0.3",
                                facecolor="#34495e", edgecolor=DARK, lw=2))
    ax.add_patch(Rectangle((x + 0.3, y + 0.35), 4.6, 1.55, facecolor="#dfe9d8", edgecolor="#95a5a6", lw=1.2))
    ax.text(x + 0.45, y + 1.55, saisie, fontsize=14, color=DARK, va="center", family="monospace")
    ax.text(x + 4.75, y + 0.72, resultat, fontsize=15, color=DARK, va="center", ha="right", family="monospace",
            fontweight="bold")
    ax.text(x + 4.75, y + 1.62, "D", fontsize=10, color=DARK, ha="right", va="center", fontweight="bold")
    ax.text(x + 2.6, y - 0.35, titre, fontsize=12, color=DARK, ha="center", va="top", fontweight="bold")


def calculatrice(path):
    fig, ax = new_fig(9.2, 3.4)
    ecran(ax, 0, 0, "cos(35)", "0,8191520443", "Calculer un cosinus")
    ecran(ax, 6.2, 0, "cos⁻¹(0,6)", "53,13010235", "Retrouver un angle")
    ax.text(5.7, 2.9, "Calculatrice en mode degrés (D ou DEG) — touche cos⁻¹ (ou Arccos)", fontsize=11.5,
            color=ORANGE, ha="center", fontweight="bold")
    ax.set_xlim(-0.3, 11.7)
    ax.set_ylim(-1.1, 3.3)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


calculatrice(C("cosinus_4e_calculatrice.png"))


# ================================================================== DÉCOUVERTE
def trois_triangles(path, solution=False):
    fig, ax = new_fig(11.0, 4.6)
    cas = [((P(4.2, 0), P(0, 0), P(4.2, 3.0)), ("A", "B", "C"), P(0, 0)),
           (pts_rect(4.6, 40, rot=90, sens=-1), ("F", "E", "D"), P(6.0, -0.2)),
           (pts_rect(4.8, 32, rot=180, sens=1), ("H", "K", "G"), P(15.0, 2.6))]
    for k, ((R, V, T), noms, dec) in enumerate(cas):
        R, V, T = R + dec, V + dec, T + dec
        ax.add_patch(Polygon([R, V, T], closed=True, facecolor=LBLUE, edgecolor="none", zorder=0))
        if solution:
            ax.plot([R[0], V[0]], [R[1], V[1]], lw=4, color=ORANGE, solid_capstyle="round")
            ax.plot([V[0], T[0]], [V[1], T[1]], lw=4, color=BLUE, solid_capstyle="round")
            ax.plot([R[0], T[0]], [R[1], T[1]], lw=2, color=GRIS)
        else:
            ax.plot([R[0], V[0], T[0], R[0]], [R[1], V[1], T[1], R[1]], lw=2.2, color=BLUE)
        right_angle(ax, R, V - R, T - R, size=0.28)
        angle(ax, V, R, T, None, ORANGE, r=0.6)
        G = (R + V + T) / 3
        for Pt, nom in zip((R, V, T), noms):
            point(ax, Pt, nom, Pt - G, fs=13)
        ax.text(G[0], -1.2, "①②③"[k], fontsize=17, ha="center", color=DARK)
    if solution:
        ax.plot([2.2, 2.8], [-2.1, -2.1], lw=4, color=BLUE)
        ax.text(2.95, -2.1, "hypoténuse", va="center", fontsize=12.5, color=BLUE, fontweight="bold")
        ax.plot([7.0, 7.6], [-2.1, -2.1], lw=4, color=ORANGE)
        ax.text(7.75, -2.1, "côté adjacent à l'angle marqué", va="center", fontsize=12.5, color=ORANGE,
                fontweight="bold")
    ax.set_xlim(-0.8, 15.8)
    ax.set_ylim(-2.6 if solution else -1.7, 4.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


trois_triangles(X("cosinus_4e_trois_triangles.png"))
trois_triangles(X("cosinus_4e_trois_triangles_solution.png"), solution=True)

# D2 : DEF rectangle en E, DE = 4, EF = 3, DF = 5
s2 = 1.2
E2_, D2_, F2_ = P(4 * s2, 0), P(0, 0), P(4 * s2, 3 * s2)
rect(X("cosinus_4e_d2.png"), E2_, D2_, F2_, noms="EDF",
     cotes=[("RV", "4 cm", "d"), ("RT", "3 cm", "d"), ("VT", "5 cm", "d")],
     extra=lambda ax, S: (angle(ax, S["V"], S["R"], S["T"], None, ORANGE, r=0.7),
                          angle(ax, S["T"], S["V"], S["R"], None, GREEN, r=0.6)))

# D3 : ABC rectangle en A, BC = 10, angle B = 35°
R3, V3, T3 = pts_rect(10, 35, s=0.68)
D3 = [("VT", "10 cm", "d")]
rect(X("cosinus_4e_d3.png"), R3, V3, T3, noms="ABC", ang="35°", cotes=D3 + [("RV", "?", "q")])
rect(X("cosinus_4e_d3_solution.png"), R3, V3, T3, noms="ABC", ang="35°", couleurs=True,
     cotes=D3 + [("RV", "≈ 8,2 cm", "s"), ("RT", "≈ 5,7 cm", "s")],
     extra=lambda ax, S: angle(ax, S["T"], S["V"], S["R"], "55°", GREEN, r=0.6))

# D4 : ABC rectangle en A, AB = 6, angle B = 50°
R4, V4, T4 = pts_rect(6 / cos(radians(50)), 50, s=0.62)
rect(X("cosinus_4e_d4.png"), R4, V4, T4, noms="ABC", ang="50°", cotes=[("RV", "6 cm", "d"), ("VT", "?", "q")])
rect(X("cosinus_4e_d4_solution.png"), R4, V4, T4, noms="ABC", ang="50°", couleurs=True,
     cotes=[("RV", "6 cm", "d"), ("VT", "≈ 9,3 cm", "s", dict(off=0.75)), ("RT", "≈ 7,2 cm", "s")])

# D5 : ABC rectangle en A, AB = 4, BC = 7
R5, V5, T5 = pts_rect(7, degrees(acos(4 / 7)), s=0.85)
rect(X("cosinus_4e_d5.png"), R5, V5, T5, noms="ABC", ang="?", cotes=[("RV", "4 cm", "d"), ("VT", "7 cm", "d")])
rect(X("cosinus_4e_d5_solution.png"), R5, V5, T5, noms="ABC", ang="≈ 55°", couleurs=True,
     cotes=[("RV", "4 cm", "d"), ("VT", "7 cm", "d")],
     extra=lambda ax, S: angle(ax, S["T"], S["V"], S["R"], "≈ 35°", GREEN, r=0.6, lr=1.35))

# D6 : tableau de valeurs
ANG = ["20°", "30°", "45°", "60°", "70°", "89°"]
tableau(X("cosinus_4e_tableau.png"),
        [["angle $x$"] + ANG, ["$\\cos x$"] + ["?", "?", "?", "?", "?", "?"]],
        larg_col=[2.0] + [1.45] * 6, surligne=[(1, j) for j in range(1, 7)],
        titre="Valeurs arrondies au millième")
tableau(X("cosinus_4e_tableau_solution.png"),
        [["angle $x$"] + ANG, ["$\\cos x$", "0,940", "0,866", "0,707", "0,5", "0,342", "0,017"]],
        larg_col=[2.0] + [1.45] * 6, vert=[(1, j) for j in range(1, 7)],
        titre="Quand l'angle augmente, le cosinus diminue")


# D7 : agrandissement
def agrandissement(path):
    fig, ax = new_fig(9.0, 4.4)
    for dx, k, col, noms, L in [(0, 1, ORANGE, "RVT", ("4", "3", "5")), (5.2, 2, BLUE, "EDF", ("8", "6", "10"))]:
        s = 0.7
        R, V, T = P(dx + 4 * k * s, 0), P(dx, 0), P(dx + 4 * k * s, 3 * k * s)
        ax.add_patch(Polygon([R, V, T], closed=True, facecolor=LORANGE if k == 1 else LBLUE, edgecolor=col,
                             lw=2.3))
        right_angle(ax, R, V - R, T - R, size=0.25)
        angle(ax, V, R, T, None, GREEN, r=0.6)
        for (Pa, Qa, Rr), t in zip([(R, V, T), (R, T, V), (V, T, R)], L):
            cote(ax, Pa, Qa, t, normale_hors(Pa, Qa, Rr), off=0.35)
    ax.text(1.4, 3.6, "$\\cos \\widehat{B} = \\dfrac{4}{5} = 0{,}8$", fontsize=14, color=ORANGE, ha="center")
    ax.text(8.0, 5.0, "$\\cos \\widehat{E} = \\dfrac{8}{10} = 0{,}8$", fontsize=14, color=BLUE, ha="center")
    point(ax, P(0, 0), "B", (-1, -0.4), fs=13)
    point(ax, P(5.2, 0), "E", (-1, -0.4), fs=13)
    ax.set_xlim(-0.8, 11.6)
    ax.set_ylim(-0.9, 5.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


agrandissement(X("cosinus_4e_agrandissement.png"))


# ================================================================ ENTRAÎNEMENT
def echelle(path, solution=False, cours=False):
    a, L = 70, 5
    s = 0.85
    A = P(0, 0)
    Cc = P(L * cos(radians(a)) * s, 0)
    B = P(Cc[0], L * sin(radians(a)) * s)
    fig, ax = new_fig(5.6, 5.6)
    ax.add_patch(Rectangle((Cc[0], -0.25), 0.7, B[1] + 0.9, facecolor="#e5e7e9", edgecolor=NEUTRAL, lw=1.2))
    ax.text(Cc[0] + 0.35, B[1] + 0.25, "mur", rotation=90, ha="center", fontsize=10.5, color=NEUTRAL)
    ax.plot([-1.0, Cc[0]], [0, 0], lw=2, color=NEUTRAL)
    for t in np.linspace(0.08, 0.92, 9):
        Q = A + t * (B - A)
        n = P(-sin(radians(a)), cos(radians(a))) * 0.18
        ax.plot([Q[0] - n[0], Q[0] + n[0]], [Q[1] - n[1], Q[1] + n[1]], lw=2, color="#a0522d")
    ax.plot([A[0], B[0]], [A[1], B[1]], lw=3.5, color="#a0522d")
    right_angle(ax, Cc, A - Cc, B - Cc, size=0.25)
    angle(ax, A, Cc, B, "70°", ORANGE, r=0.55, lr=1.0)
    cote(ax, A, B, "5 m", normale_hors(A, B, Cc), off=0.45)
    if solution:
        cote(ax, A, Cc, "≈ 1,71 m", P(0, -1), "s", off=0.4)
        cote(ax, Cc, B, "≈ 4,70 m", P(1, 0), "s", off=1.55, t=0.45)
    elif not cours:
        cote(ax, A, Cc, "?", P(0, -1), "q", off=0.4)
    for Pt, nom, d in [(A, "A", (-1, -0.5)), (Cc, "C", (0.4, -1)), (B, "B", (-1, 0.3))]:
        point(ax, Pt, nom, d)
    ax.set_xlim(-1.2, Cc[0] + 2.4)
    ax.set_ylim(-1.0, B[1] + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


echelle(C("cosinus_4e_echelle.png"), solution=True)
echelle(X("cosinus_4e_echelle.png"))
echelle(X("cosinus_4e_echelle_solution.png"), solution=True)


def cerf_volant(path, solution=False):
    a, L, s = 40, 50, 0.16
    M = P(0, 1 * s)
    H = M + P(L * cos(radians(a)) * s, 0)
    K = P(H[0], M[1] + L * sin(radians(a)) * s)
    fig, ax = new_fig(7.4, 5.4)
    ax.plot([-1.2, H[0] + 1.5], [0, 0], lw=2, color="#58a55c")
    ax.plot([-0.25, -0.25], [0, M[1] + 0.3], lw=0)
    ax.add_patch(Polygon([K + P(0, 0.55), K + P(0.4, 0), K + P(0, -0.7), K + P(-0.4, 0)], closed=True,
                         facecolor="#e74c3c", edgecolor="#922b21", lw=1.5, zorder=1))
    ax.plot([K[0], K[0] + 0.3, K[0] - 0.1, K[0] + 0.2], [K[1] - 0.7, K[1] - 1.1, K[1] - 1.4, K[1] - 1.8],
            lw=1.2, color="#922b21")
    ax.plot([M[0], K[0]], [M[1], K[1]], lw=1.6, color=DARK)
    ax.plot([M[0], H[0]], [M[1], H[1]], lw=1.4, color=NEUTRAL, ls="--")
    ax.plot([H[0], K[0]], [H[1], K[1]], lw=1.4, color=NEUTRAL, ls="--")
    ax.plot([H[0], H[0]], [0, H[1]], lw=1.0, color=NEUTRAL, ls=":")
    right_angle(ax, H, M - H, K - H, size=0.3)
    angle(ax, M, H, K, "40°", ORANGE, r=0.9)
    cote(ax, M, K, "ficelle : 50 m", normale_hors(M, K, H), off=0.45)
    if solution:
        cote(ax, M, H, "≈ 38,3 m", P(0, -1), "s", off=0.38)
        cote(ax, H, K, "≈ 32,1 m", P(1, 0), "s", off=0.95)
    for Pt, nom, d in [(M, "M", (-1, 0.6)), (H, "H", (1, -0.7)), (K, "K", (1.3, 0.9))]:
        point(ax, Pt, nom, d)
    ax.set_xlim(-1.4, H[0] + 2.0)
    ax.set_ylim(-0.6, K[1] + 1.0)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


cerf_volant(X("cosinus_4e_cerf_volant.png"))
cerf_volant(X("cosinus_4e_cerf_volant_solution.png"), solution=True)


def isocele(path, solution=False):
    s = 0.6
    B, Cc, A = P(0, 0), P(12 * s, 0), P(6 * s, 8 * s)
    H = (B + Cc) / 2
    fig, ax = new_fig(6.8, 4.8)
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.3))
    ax.plot([A[0], H[0]], [A[1], H[1]], lw=1.6, color=NEUTRAL, ls="--")
    right_angle(ax, H, Cc - H, A - H, size=0.28)
    G = (A + B + Cc) / 3
    cote(ax, A, B, "10 cm", normale_hors(A, B, Cc))
    cote(ax, A, Cc, "10 cm", normale_hors(A, Cc, B))
    cote(ax, B, Cc, "12 cm", P(0, -1), t=0.75)
    if solution:
        angle(ax, B, Cc, A, "≈ 53,1°", GREEN, r=0.75, lr=1.55)
        angle(ax, Cc, B, A, "≈ 53,1°", GREEN, r=0.75, lr=1.55)
        angle(ax, A, B, Cc, None, GREEN, r=0.65)
        ax.text(A[0] + 0.2, A[1] - 1.15, "≈ 73,7°", fontsize=13, color=GREEN, ha="left")
        cote(ax, B, H, "6 cm", P(0, 1), "s", off=0.3)
    else:
        angle(ax, B, Cc, A, "?", ORANGE, r=0.75)
    for Pt, nom in [(A, "A"), (B, "B"), (Cc, "C")]:
        point(ax, Pt, nom, Pt - G)
    point(ax, H, "H", (0, -1))
    finish(fig, ax, path, [A, B, Cc], margin=0.9)


isocele(X("cosinus_4e_isocele.png"))
isocele(X("cosinus_4e_isocele_solution.png"), solution=True)


def rectangle(path, solution=False):
    s = 0.75
    A, B, Cc, Dd = P(0, 0), P(8 * s, 0), P(8 * s, 6 * s), P(0, 6 * s)
    O = (A + Cc) / 2
    fig, ax = new_fig(6.6, 5.0)
    ax.add_patch(Polygon([A, B, Cc, Dd], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.3))
    ax.plot([A[0], Cc[0]], [A[1], Cc[1]], lw=2, color=ORANGE)
    ax.plot([B[0], Dd[0]], [B[1], Dd[1]], lw=1.6, color=NEUTRAL, ls="--")
    for Q, u, v in [(A, B - A, Dd - A), (B, A - B, Cc - B), (Cc, B - Cc, Dd - Cc), (Dd, Cc - Dd, A - Dd)]:
        right_angle(ax, Q, u, v, size=0.25)
    cote(ax, A, B, "8 cm", P(0, -1))
    cote(ax, B, Cc, "6 cm", P(1, 0), off=0.55)
    if solution:
        angle(ax, A, B, Cc, "≈ 36,9°", GREEN, r=1.0, lr=1.75)
        angle(ax, Cc, A, B, "≈ 53,1°", GREEN, r=0.7, lr=1.3)
        angle(ax, O, A, B, "≈ 106,3°", GREEN, r=0.45, lr=0.95)
        cote(ax, A, Cc, "10 cm", P(-0.6, 0.8), "s", off=0.35, t=0.3)
    else:
        angle(ax, A, B, Cc, "?", ORANGE, r=1.0)
    for Pt, nom, d in [(A, "A", (-1, -1)), (B, "B", (1, -1)), (Cc, "C", (1, 1)), (Dd, "D", (-1, 1)),
                       (O, "O", (0, 1))]:
        point(ax, Pt, nom, d)
    finish(fig, ax, path, [A, Cc], margin=1.0)


rectangle(X("cosinus_4e_rectangle.png"))
rectangle(X("cosinus_4e_rectangle_solution.png"), solution=True)


def deux_triangles(path, solution=False):
    s = 0.55
    B = P(0, 0)
    H = P(10 * cos(radians(40)) * s, 0)
    A = P(H[0], 10 * sin(radians(40)) * s)
    hc = sqrt(64 - (10 * sin(radians(40))) ** 2)
    Cc = P(H[0] + hc * s, 0)
    fig, ax = new_fig(7.0, 4.6)
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.3))
    ax.plot([A[0], H[0]], [A[1], H[1]], lw=2, color=ORANGE)
    right_angle(ax, H, Cc - H, A - H, size=0.25)
    right_angle(ax, H, B - H, A - H, size=0.25)
    angle(ax, B, H, A, "40°", ORANGE, r=0.8)
    cote(ax, A, B, "10 cm", normale_hors(A, B, Cc))
    cote(ax, A, Cc, "8 cm", normale_hors(A, Cc, B))
    if solution:
        cote(ax, B, H, "≈ 7,66 cm", P(0, -1), "s", off=0.38)
        cote(ax, H, Cc, "≈ 4,76", P(0, -1), "s", off=0.38)
        cote(ax, A, H, "≈ 6,43", P(-1, 0), "s", off=0.62, t=0.55)
        angle(ax, Cc, B, A, "≈ 53,5°", GREEN, r=0.7, lr=1.45)
    G = (A + B + Cc) / 3
    for Pt, nom in [(A, "A"), (B, "B"), (Cc, "C")]:
        point(ax, Pt, nom, Pt - G)
    point(ax, H, "H", (0.2, -1))
    finish(fig, ax, path, [A, B, Cc], margin=1.0)


deux_triangles(X("cosinus_4e_deux_triangles.png"))
deux_triangles(X("cosinus_4e_deux_triangles_solution.png"), solution=True)

# E6 : RST rectangle en S, RS = 5, RT = 13
s6 = 0.5
rect(X("cosinus_4e_rst.png"), P(0, 0), P(0, 5 * s6 * 1.0), P(12 * s6, 0), noms="SRT",
     cotes=[("RV", "5 cm", "d"), ("VT", "13 cm", "d"), ("RT", "12 cm", "d")], w=6.6, h=3.8,
     extra=lambda ax, S: (angle(ax, S["V"], S["R"], S["T"], None, ORANGE, r=0.5),
                          angle(ax, S["T"], S["V"], S["R"], None, GREEN, r=0.9)))


def hauteur(path, solution=False):
    s = 0.62
    B = P(0, 0)
    A = P(7 * cos(radians(60)) * s, 7 * sin(radians(60)) * s)
    Cc = P(9 * s, 0)
    H = P(A[0], 0)
    fig, ax = new_fig(6.6, 4.8)
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.3))
    ax.plot([A[0], H[0]], [A[1], H[1]], lw=1.8, color=ORANGE, ls="--")
    right_angle(ax, H, Cc - H, A - H, size=0.25)
    angle(ax, B, Cc, A, "60°", ORANGE, r=0.7)
    cote(ax, A, B, "7 cm", normale_hors(A, B, Cc))
    cote(ax, B, Cc, "9 cm", P(0, -1), t=0.72, off=0.45)
    if solution:
        cote(ax, B, H, "3,5", P(0, 1), "s", off=0.28, t=0.62)
        cote(ax, A, H, "≈ 6,06", P(1, 0), "s", off=0.55, t=0.45)
        cote(ax, A, Cc, "≈ 8,19 cm", normale_hors(A, Cc, B), "s")
        angle(ax, Cc, B, A, "≈ 47,8°", GREEN, r=0.7, lr=1.45)
    G = (A + B + Cc) / 3
    for Pt, nom in [(A, "A"), (B, "B"), (Cc, "C")]:
        point(ax, Pt, nom, Pt - G)
    point(ax, H, "H", (0, -1))
    finish(fig, ax, path, [A, B, Cc], margin=1.0)


hauteur(X("cosinus_4e_hauteur.png"))
hauteur(X("cosinus_4e_hauteur_solution.png"), solution=True)


# =================================================================== PROBLÈMES
def telepherique(path, solution=False):
    s = 1 / 150
    D = P(0, 0)
    H = P(1200 * cos(radians(25)) * s, 0)
    A = P(H[0], 1200 * sin(radians(25)) * s)
    fig, ax = new_fig(7.8, 4.4)
    xs = np.linspace(-0.8, H[0] + 1.0, 120)
    prof = np.interp(xs, [-0.8, 0.0, 2.0, 4.5, H[0], H[0] + 1.0], [-0.3, -0.2, 0.2, 1.4, A[1] - 0.15, A[1] - 0.6])
    ax.fill_between(xs, -0.9, prof, color="#d5dbdb", zorder=0)
    ax.plot([D[0], A[0]], [D[1], A[1]], lw=2, color=DARK)
    ax.add_patch(Rectangle((A[0] * 0.55 - 0.25, A[1] * 0.55 - 0.55), 0.5, 0.4, facecolor="#e74c3c",
                           edgecolor="#922b21", zorder=5))
    ax.plot([A[0] * 0.55, A[0] * 0.55], [A[1] * 0.55, A[1] * 0.55 - 0.15], lw=1.2, color=DARK)
    ax.plot([D[0], H[0]], [D[1], H[1]], lw=1.4, color=NEUTRAL, ls="--")
    ax.plot([H[0], A[0]], [H[1], A[1]], lw=1.4, color=NEUTRAL, ls="--")
    right_angle(ax, H, D - H, A - H, size=0.22)
    angle(ax, D, H, A, "25°", ORANGE, r=1.0, lr=1.55)
    cote(ax, D, A, "câble : 1 200 m", normale_hors(D, A, H), off=0.5, t=0.28)
    ax.text(D[0] - 0.1, D[1] - 0.45, "départ : 1 350 m", fontsize=10.5, color=DARK, ha="left", va="top")
    if solution:
        cote(ax, D, H, "≈ 1 088 m", P(0, 1), "s", off=0.3, t=0.62)
        cote(ax, H, A, "≈ 507 m", P(1, 0), "s", off=0.75)
        ax.text(A[0], A[1] + 0.45, "arrivée ≈ 1 857 m", fontsize=11, color=GREEN, ha="center", fontweight="bold")
    for Pt, nom, d in [(D, "D", (-1, 0.4)), (H, "H", (1, -0.6)), (A, "A", (-0.6, 1))]:
        point(ax, Pt, nom, d)
    ax.set_xlim(-1.0, H[0] + 1.6)
    ax.set_ylim(-1.0, A[1] + 1.0)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


telepherique(X("cosinus_4e_telepherique.png"))
telepherique(X("cosinus_4e_telepherique_solution.png"), solution=True)


def avion(path, solution=False):
    s = 1 / 330
    O = P(0, 0)
    a = radians(15)
    Pp = P(3000 * cos(a) * s, 3000 * sin(a) * s)
    Hh = P(Pp[0], 0)
    Kx = 2000 * s
    K = P(Kx, 2000 * np.tan(a) * s)
    fig, ax = new_fig(8.6, 3.8)
    ax.plot([-1.0, Pp[0] + 1.0], [0, 0], lw=2.5, color=NEUTRAL)
    ax.plot([-1.0, 1.4], [0, 0], lw=5, color="#566573")
    ax.text(0.2, -0.3, "piste", fontsize=10, color=NEUTRAL, ha="center", va="top")
    ax.plot([O[0], Pp[0] + 0.5 * cos(a)], [O[1], Pp[1] + 0.5 * sin(a)], lw=1.6, color=BLUE, ls="--")
    xs = np.linspace(Kx - 1.6, Kx + 1.6, 60)
    ax.fill_between(xs, 0, 300 * s * np.exp(-((xs - Kx) / 0.7) ** 2), color="#a9cce3", zorder=0)
    ax.text(Kx + 0.9, 0.25, "colline\n300 m", fontsize=10, color="#21618c", va="bottom")
    ax.text(Pp[0] + 0.25, Pp[1] + 0.05, "✈", fontsize=22, color=BLUE, va="center", rotation=15)
    ax.plot([Pp[0], Hh[0]], [Pp[1], Hh[1]], lw=1.4, color=NEUTRAL, ls="--")
    right_angle(ax, Hh, O - Hh, Pp - Hh, size=0.2)
    angle(ax, O, P(1, 0), Pp, "15°", ORANGE, r=1.4, lr=2.0)
    cote(ax, O, Pp, "3 km", normale_hors(O, Pp, Hh), off=0.35, t=0.4)
    if solution:
        cote(ax, Hh, Pp, "≈ 776 m", P(1, 0), "s", off=0.8)
        ax.plot([Kx, Kx], [0, K[1]], lw=1.4, color=GREEN, ls=":")
        ax.text(Kx - 0.1, K[1] + 0.35, "≈ 536 m", fontsize=11, color=GREEN, ha="right", fontweight="bold")
    for Pt, nom, d in [(O, "O", (-0.6, 1)), (Hh, "H", (0.6, -1)), (Pp, "P", (-0.7, 1))]:
        point(ax, Pt, nom, d)
    ax.set_xlim(-1.2, Pp[0] + 1.8)
    ax.set_ylim(-0.9, Pp[1] + 0.9)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


avion(X("cosinus_4e_avion.png"))
avion(X("cosinus_4e_avion_solution.png"), solution=True)


def toit(path, solution=False):
    s = 0.6
    B, Cc = P(0, 0), P(9 * s, 0)
    I = (B + Cc) / 2
    A = P(I[0], sqrt(10) * s)
    fig, ax = new_fig(6.4, 5.0)
    ax.add_patch(Rectangle((B[0], -3.0), Cc[0] - B[0], 3.0, facecolor="#fdf2e9", edgecolor=NEUTRAL, lw=1.5))
    ax.add_patch(Rectangle((I[0] - 0.45, -3.0), 0.9, 1.6, facecolor="#a04000", edgecolor=NEUTRAL))
    for xw in (B[0] + 0.6, Cc[0] - 1.4):
        ax.add_patch(Rectangle((xw, -1.6), 0.8, 0.8, facecolor="#aed6f1", edgecolor=NEUTRAL))
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor="#e59866", edgecolor="#a04000", lw=2.5))
    ax.plot([A[0], I[0]], [A[1], I[1]], lw=1.5, color=DARK, ls="--")
    right_angle(ax, I, Cc - I, A - I, size=0.25)
    angle(ax, B, Cc, A, "≈ 35,1°" if solution else "?", GREEN if solution else ORANGE, r=0.8, lr=1.55)
    cote(ax, A, B, "5,5 m", normale_hors(A, B, Cc))
    cote(ax, A, Cc, "5,5 m", normale_hors(A, Cc, B))
    ax.annotate("", xy=(Cc[0], -3.35), xytext=(B[0], -3.35), arrowprops=dict(arrowstyle="<->", color=DARK))
    ax.text(I[0], -3.5, "largeur : 9 m", ha="center", va="top", fontsize=12, color=DARK)
    if solution:
        cote(ax, A, I, "≈ 3,16 m", P(1, 0), "s", off=0.85, t=0.78)
    for Pt, nom, d in [(A, "A", (0, 1)), (B, "B", (-1, 0.2)), (Cc, "C", (1, 0.2)), (I, "I", (-0.5, -1))]:
        point(ax, Pt, nom, d)
    finish(fig, ax, path, [A, B, Cc, P(0, -3.9)], margin=0.8)


toit(X("cosinus_4e_toit.png"))
toit(X("cosinus_4e_toit_solution.png"), solution=True)


def bateau(path, solution=False):
    s = 0.42
    O = P(0, 0)
    a = radians(40)
    Pp = P(12 * sin(a) * s, 12 * cos(a) * s)
    Hh = P(0, Pp[1])
    Q = Pp + P(5 * s, 0)
    fig, ax = new_fig(6.6, 5.6)
    ax.add_patch(Rectangle((-1.6, -1.2), 9.4, 7.4, facecolor="#ebf5fb", edgecolor="none", zorder=0))
    ax.annotate("", xy=(0, Pp[1] + 1.4), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=DARK, lw=1.4))
    ax.text(0.15, Pp[1] + 1.2, "Nord", fontsize=11, color=DARK, fontweight="bold")
    ax.annotate("", xy=(Q[0] + 0.9, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.2))
    ax.text(Q[0] + 0.8, -0.35, "Est", fontsize=11, color=NEUTRAL, ha="right", va="top")
    ax.plot([O[0], Pp[0]], [O[1], Pp[1]], lw=2.4, color=BLUE)
    ax.plot([Pp[0], Q[0]], [Pp[1], Q[1]], lw=2.4, color=BLUE)
    ax.plot([Hh[0], Pp[0]], [Hh[1], Pp[1]], lw=1.4, color=NEUTRAL, ls="--")
    right_angle(ax, Hh, P(0, -1), P(1, 0), size=0.25)
    angle(ax, O, P(0, 1), Pp, "40°", ORANGE, r=0.9, lr=1.4)
    cote(ax, O, Pp, "12 km", -normale_hors(O, Pp, Hh), off=0.45, t=0.62)
    cote(ax, Pp, Q, "5 km", P(0, 1), off=0.3)
    if solution:
        ax.plot([O[0], Q[0]], [O[1], Q[1]], lw=2, color=GREEN, ls="--")
        cote(ax, O, Hh, "≈ 9,19 km", P(-1, 0), "s", off=0.95)
        cote(ax, Hh, Pp, "≈ 7,71 km", P(0, 1), "s", off=0.3)
        cote(ax, O, Q, "≈ 15,7 km", normale_hors(O, Q, Pp), "s", off=0.45, t=0.55)
    ax.add_patch(Circle(O, 0.18, color="#a04000", zorder=6))
    ax.text(0.25, -0.35, "port", fontsize=10.5, color="#a04000", va="top")
    for Pt, nom, d in [(O, "O", (-1, -0.5)), (Hh, "H", (-1, 0)), (Pp, "P", (-0.3, 1)), (Q, "Q", (1, 0.3))]:
        point(ax, Pt, nom, d)
    ax.set_xlim(-1.6, Q[0] + 1.4)
    ax.set_ylim(-1.2, Pp[1] + 1.8)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


bateau(X("cosinus_4e_bateau.png"))
bateau(X("cosinus_4e_bateau_solution.png"), solution=True)


def pendule(path, solution=False):
    s = 3.6
    O = P(0, 0)
    a = radians(30)
    B0 = P(0, -1.2 * s)
    B = P(1.2 * sin(a) * s, -1.2 * cos(a) * s)
    Hh = P(0, B[1])
    fig, ax = new_fig(5.2, 5.6)
    ax.add_patch(Rectangle((-1.2, 0), 2.4, 0.25, facecolor="#7f8c8d", edgecolor=DARK))
    ax.plot([O[0], B0[0]], [O[1], B0[1]], lw=1.2, color=NEUTRAL, ls=":")
    ax.add_patch(Circle(B0, 0.2, facecolor="white", edgecolor=NEUTRAL, ls=":", lw=1.2))
    ax.plot([O[0], B[0]], [O[1], B[1]], lw=2, color=DARK)
    ax.add_patch(Circle(B, 0.15, facecolor=ORANGE, edgecolor="#a04000", zorder=5))
    ax.plot([Hh[0], B[0]], [Hh[1], B[1]], lw=1.4, color=NEUTRAL, ls="--")
    right_angle(ax, Hh, P(0, 1), P(1, 0), size=0.22)
    angle(ax, O, P(0, -1), B - O, "30°", ORANGE, r=0.9, lr=1.35)
    cote(ax, O, B, "1,2 m", normale_hors(O, B, Hh), off=0.4)
    if solution:
        cote(ax, O, Hh, "≈ 1,04 m", P(-1, 0), "s", off=0.75)
        cote(ax, Hh, B0, "≈ 16 cm", P(-1, 0), "s", off=0.75)
        cote(ax, Hh, B, "0,6 m", P(0, 1), "s", off=0.28)
    for Pt, nom, d in [(O, "O", (-1, -0.4)), (Hh, "H", (-1, 0.3)), (B, "B", (1, -0.6)), (B0, "B_0", (0.8, -1))]:
        point(ax, Pt, nom, d)
    ax.set_xlim(-1.8, 2.6)
    ax.set_ylim(B0[1] - 0.8, 0.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


pendule(X("cosinus_4e_pendule.png"))
pendule(X("cosinus_4e_pendule_solution.png"), solution=True)


def losange(path, solution=False):
    s = 0.7
    a = radians(35)
    A = P(0, 0)
    Cc = P(2 * 6 * cos(a) * s, 0)
    O = (A + Cc) / 2
    B = P(O[0], -6 * sin(a) * s)
    Dd = P(O[0], 6 * sin(a) * s)
    fig, ax = new_fig(6.8, 4.4)
    ax.add_patch(Polygon([A, B, Cc, Dd], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.3))
    ax.plot([A[0], Cc[0]], [A[1], Cc[1]], lw=1.6, color=NEUTRAL, ls="--")
    ax.plot([B[0], Dd[0]], [B[1], Dd[1]], lw=1.6, color=NEUTRAL, ls="--")
    right_angle(ax, O, Cc - O, Dd - O, size=0.22)
    angle(ax, A, B, Dd, None, ORANGE, r=0.8)
    ax.text(A[0] + 1.0, A[1] - 0.5, "70°", fontsize=13, color=ORANGE, va="center")
    cote(ax, A, Dd, "6 cm", normale_hors(A, Dd, Cc))
    if solution:
        angle(ax, A, O + P(0, 0), Dd, None, GREEN, r=1.3)
        ax.text(A[0] + 1.45, A[1] + 0.3, "35°", fontsize=12, color=GREEN, fontweight="bold", va="center")
        cote(ax, A, O, "≈ 4,91", P(0, -1), "s", off=0.32, t=0.72)
        cote(ax, O, Dd, "≈ 3,44", P(1, 0), "s", off=0.62)
    for Pt, nom, d in [(A, "A", (-1, 0)), (B, "B", (0, -1)), (Cc, "C", (1, 0)), (Dd, "D", (0, 1)),
                       (O, "O", (0.7, -0.7))]:
        point(ax, Pt, nom, d)
    finish(fig, ax, path, [A, B, Cc, Dd], margin=0.8)


losange(X("cosinus_4e_losange.png"))
losange(X("cosinus_4e_losange_solution.png"), solution=True)


def escalator(path, solution=False):
    s = 0.42
    A = P(0, 0)
    Hh = P(sqrt(189) * s, 0)
    B = P(Hh[0], 6 * s)
    fig, ax = new_fig(7.0, 4.0)
    ax.add_patch(Rectangle((-1.2, -0.35), Hh[0] + 1.2, 0.35, facecolor="#d5dbdb", edgecolor=NEUTRAL))
    ax.add_patch(Rectangle((Hh[0], B[1] - 0.35), 2.0, 0.35, facecolor="#d5dbdb", edgecolor=NEUTRAL))
    ax.text(-0.9, -0.7, "rez-de-chaussée", fontsize=10, color=NEUTRAL, va="top")
    ax.text(Hh[0] + 1.0, B[1] + 0.2, "1er étage", fontsize=10, color=NEUTRAL, ha="center")
    n = 14
    for i in range(n):
        x0 = A[0] + (B[0] - A[0]) * i / n
        y0 = A[1] + (B[1] - A[1]) * i / n
        ax.plot([x0, x0, x0 + (B[0] - A[0]) / n], [y0, y0 + (B[1] - A[1]) / n, y0 + (B[1] - A[1]) / n],
                lw=1.2, color="#5d6d7e")
    ax.plot([A[0], B[0]], [A[1], B[1]], lw=2.4, color=BLUE)
    ax.plot([A[0], Hh[0]], [A[1], Hh[1]], lw=1.4, color=NEUTRAL, ls="--")
    ax.plot([Hh[0], B[0]], [Hh[1], B[1]], lw=1.4, color=NEUTRAL, ls="--")
    right_angle(ax, Hh, A - Hh, B - Hh, size=0.2)
    cote(ax, A, B, "15 m", normale_hors(A, B, Hh), off=0.45)
    cote(ax, Hh, B, "6 m", P(1, 0), off=0.4)
    if solution:
        cote(ax, A, Hh, "≈ 13,75 m", P(0, 1), "s", off=0.3, t=0.62)
        angle(ax, A, Hh, B, "≈ 23,6°", GREEN, r=1.2, lr=1.9)
    else:
        angle(ax, A, Hh, B, "?", ORANGE, r=1.2, lr=1.7)
    for Pt, nom, d in [(A, "A", (-1, 0.5)), (Hh, "H", (0.5, -1)), (B, "B", (-0.6, 1))]:
        point(ax, Pt, nom, d)
    ax.set_xlim(-1.3, Hh[0] + 2.2)
    ax.set_ylim(-1.2, B[1] + 0.9)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


escalator(X("cosinus_4e_escalator.png"))
escalator(X("cosinus_4e_escalator_solution.png"), solution=True)
