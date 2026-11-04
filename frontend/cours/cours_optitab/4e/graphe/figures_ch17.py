# -*- coding: utf-8 -*-
"""Figures du chapitre 17 (pyramides, cônes et volumes) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, _proj, right_angle, tableau,
                   BLUE, ORANGE, GREEN, DARK, NEUTRAL, DIR_COURS, DIR_EXOS)
import numpy as np
from math import sqrt
from matplotlib.patches import Polygon, Rectangle

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
P = lambda x, y: np.array([x, y], float)  # noqa: E731
LBLUE, LORANGE, LGREEN = "#d6eafc", "#fdebd0", "#e8f5e9"


def unit(v):
    v = np.array(v, float)
    return v / np.linalg.norm(v)


def point(ax, Pt, nom, d, fs=14, s=24, col=DARK):
    d = unit(d)
    ax.scatter([Pt[0]], [Pt[1]], s=s, zorder=6, color=col)
    ax.annotate(f"${nom}$", (Pt[0], Pt[1]), textcoords="offset points", xytext=(15 * d[0], 15 * d[1]),
                ha="center", va="center", fontsize=fs, color=col, fontweight="bold")


def txt(ax, x, y, s, col=DARK, fs=12, **kw):
    ax.text(x, y, s, color=col, fontsize=fs, **kw)


def lab(ax, A, B, s, d, col=DARK, fs=12, t=0.5, bold=False):
    m = np.array(A) + t * (np.array(B) - np.array(A)) + np.array(d)
    ax.text(m[0], m[1], s, color=col, fontsize=fs, ha="center", va="center", fontweight="bold" if bold else "normal",
            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))


def cadre(ax, pts, marge=0.8):
    pts = np.array(pts, float)
    ax.set_xlim(pts[:, 0].min() - marge, pts[:, 0].max() + marge)
    ax.set_ylim(pts[:, 1].min() - marge, pts[:, 1].max() + marge)
    ax.set_aspect("equal")
    ax.axis("off")


def seg(ax, A, B, col=BLUE, lw=2.2, cache=False):
    ax.plot([A[0], B[0]], [A[1], B[1]], lw=1.4 if cache else lw, color=col, ls="--" if cache else "-", zorder=2)


def pyramide_rect(ax, L, Pf, H, noms="ABCDS", col=BLUE, face=None, hauteur=True, dec=(0, 0), k=0.45):
    """Pyramide de base rectangle L x Pf (profondeur) et de hauteur H ; sommet au-dessus du centre."""
    pr = lambda x, y, z: P(*_proj(x, y, z, k=k)) + P(*dec)  # noqa: E731
    V = {noms[0]: pr(0, 0, 0), noms[1]: pr(L, 0, 0), noms[2]: pr(L, Pf, 0), noms[3]: pr(0, Pf, 0),
         noms[4]: pr(L / 2, Pf / 2, H)}
    O = pr(L / 2, Pf / 2, 0)
    A, B, Cc, D, S = noms
    if face:
        ax.add_patch(Polygon([V[n] for n in face], closed=True, facecolor=LORANGE, edgecolor="none", zorder=0))
    for a, b, h in [(A, B, 0), (B, Cc, 0), (Cc, D, 1), (D, A, 1), (A, S, 0), (B, S, 0), (Cc, S, 0), (D, S, 1)]:
        seg(ax, V[a], V[b], col, cache=bool(h))
    if hauteur:
        ax.plot([O[0], V[S][0]], [O[1], V[S][1]], lw=1.6, color=ORANGE, ls="--")
    V["O"] = O
    return V


def cone_dessin(ax, r, h, centre=(0, 0), col=BLUE, e=0.3, axe=True, pointe_bas=False, lw=2.2):
    cx, cy = centre
    t = np.linspace(0, 2 * np.pi, 160)
    sgn = -1 if pointe_bas else 1
    x, y = cx + r * np.cos(t), cy + e * r * np.sin(t)
    if pointe_bas:
        ax.plot(x, y, lw=lw, color=col)
    else:
        ax.plot(x[t > np.pi], y[t > np.pi], lw=lw, color=col)
        ax.plot(x[t <= np.pi], y[t <= np.pi], lw=1.3, color=col, ls="--")
    S = P(cx, cy + sgn * h)
    ax.plot([cx - r, S[0]], [cy, S[1]], lw=lw, color=col)
    ax.plot([cx + r, S[0]], [cy, S[1]], lw=lw, color=col)
    if axe:
        ax.plot([cx, cx], [cy, S[1]], lw=1.5, color=ORANGE, ls="--")
    return S, P(cx, cy)


def cylindre_dessin(ax, r, h, base=(0, 0), col=BLUE, e=0.3, lw=2.2, fc=None):
    cx, cy = base
    t = np.linspace(0, 2 * np.pi, 160)
    if fc:
        xs = np.concatenate([cx + r * np.cos(t[t > np.pi]), (cx + r * np.cos(t[t <= np.pi]))[::-1]])
        ax.fill_between([cx - r, cx + r], cy, cy + h, color=fc, zorder=0)
    ax.plot(cx + r * np.cos(t), cy + h + e * r * np.sin(t), lw=lw, color=col)
    ax.plot(cx + r * np.cos(t[t > np.pi]), cy + e * r * np.sin(t[t > np.pi]), lw=lw, color=col)
    ax.plot(cx + r * np.cos(t[t <= np.pi]), cy + e * r * np.sin(t[t <= np.pi]), lw=1.3, color=col, ls="--")
    ax.plot([cx - r, cx - r], [cy, cy + h], lw=lw, color=col)
    ax.plot([cx + r, cx + r], [cy, cy + h], lw=lw, color=col)


# ======================================================================= COURS
def vocab_pyramide(path):
    fig, ax = new_fig(7.0, 5.4)
    V = pyramide_rect(ax, 4.4, 3.4, 4.2, face="ABS")
    for n, d in [("A", (-1, -0.6)), ("B", (1, -0.6)), ("C", (1, 0)), ("D", (-1, 0.3)), ("S", (0, 1)), ("O", (0.8, -0.8))]:
        point(ax, V[n], n, d, col=ORANGE if n == "O" else DARK)
    txt(ax, V["S"][0] + 0.3, V["S"][1] + 0.35, "sommet", DARK, 12, fontweight="bold")
    g = (V["A"] + V["B"] + V["S"]) / 3
    txt(ax, g[0] - 0.55, g[1] + 0.2, "face latérale", ORANGE, 12, ha="center", fontweight="bold")
    txt(ax, 5.6, 1.2, "base\n(rectangle ABCD)", BLUE, 11.5, fontweight="bold")
    txt(ax, V["O"][0] + 0.12, (V["O"][1] + V["S"][1]) / 2 + 0.5, "hauteur [SO]", ORANGE, 11.5, fontweight="bold")
    m = (V["B"] + V["S"]) / 2
    txt(ax, m[0] + 0.45, m[1] + 0.1, "arête latérale", BLUE, 11.5, fontweight="bold")
    right_angle(ax, V["O"], V["A"] - V["O"], V["S"] - V["O"], size=0.22, color=ORANGE)
    cadre(ax, list(V.values()) + [P(7.6, 1.0)], 0.9)
    _save(fig, path)


vocab_pyramide(C("espace_4e_pyramide.png"))


def vocab_cone(path):
    fig, ax = new_fig(6.2, 5.4)
    r, h = 2.0, 4.0
    S, O = cone_dessin(ax, r, h)
    A = P(r, 0)
    ax.plot([0, r], [0, 0], lw=1.6, color=GREEN)
    right_angle(ax, O, (1, 0), (0, 1), size=0.22, color=ORANGE)
    point(ax, S, "S", (0, 1))
    point(ax, O, "O", (-0.6, -1), col=ORANGE)
    point(ax, A, "A", (1, -0.3))
    txt(ax, 0.25, 0.25 + 0.0, "rayon", GREEN, 11, fontweight="bold")
    txt(ax, -0.15, 2.2, "hauteur", ORANGE, 11.5, ha="right", fontweight="bold")
    txt(ax, 1.25, 2.35, "génératrice [SA]", BLUE, 11.5, fontweight="bold")
    txt(ax, 0, -1.0, "base : disque de centre O", BLUE, 11.5, ha="center", fontweight="bold")
    cadre(ax, [S, P(-r, -1.2), P(r + 2.6, 0)], 0.6)
    _save(fig, path)


vocab_cone(C("espace_4e_cone.png"))


def tiers(path):
    fig, ax = new_fig(8.4, 4.6)
    pr = lambda x, y, z, dx=0: P(*_proj(x, y, z)) + P(dx, 0)  # noqa: E731
    a = 3.2
    cube = {"A": pr(0, 0, 0), "B": pr(a, 0, 0), "C": pr(a, a, 0), "D": pr(0, a, 0),
            "E": pr(0, 0, a), "F": pr(a, 0, a), "G": pr(a, a, a), "H": pr(0, a, a)}
    for u, v_, h in [("A", "B", 0), ("B", "C", 0), ("C", "D", 1), ("D", "A", 1), ("E", "F", 0), ("F", "G", 0),
                     ("G", "H", 0), ("H", "E", 0), ("A", "E", 0), ("B", "F", 0), ("C", "G", 0), ("D", "H", 1)]:
        seg(ax, cube[u], cube[v_], NEUTRAL, lw=1.8, cache=bool(h))
    S = pr(a / 2, a / 2, a)
    ax.add_patch(Polygon([cube["A"], cube["B"], S], closed=True, facecolor=LORANGE, edgecolor="none", zorder=0))
    for n, h in [("A", 0), ("B", 0), ("C", 0), ("D", 1)]:
        seg(ax, cube[n], S, ORANGE, cache=bool(h))
    txt(ax, 2.6, -0.75, "même base, même hauteur", DARK, 12, ha="center", va="top")
    txt(ax, 7.6, 2.4, "$V_{\\mathrm{pyramide}} = \\dfrac{1}{3}\\, V_{\\mathrm{prisme}}$", GREEN, 18, ha="center",
        va="center", fontweight="bold")
    txt(ax, 7.6, 1.0, "il faut 3 pyramides pleines\npour remplir le prisme", DARK, 11.5, ha="center", va="center")
    cadre(ax, list(cube.values()) + [P(9.6, 0), P(0, -1.0)], 0.4)
    _save(fig, path)


tiers(C("espace_4e_tiers.png"))
tiers(X("espace_4e_tiers.png"))
tableau(C("espace_4e_conversions.png"),
        [["unité", "m³", "dm³", "cm³", "mm³"], ["contenance", "1 000 L", "1 L", "1 mL", ""]],
        larg_col=[2.4, 1.8, 1.8, 1.8, 1.6], titre="Chaque unité de volume vaut 1 000 fois la suivante")


# ================================================================== DÉCOUVERTE
def d1(path):
    fig, ax = new_fig(6.8, 5.4)
    V = pyramide_rect(ax, 4.4, 3.4, 4.2)
    for n, d in [("A", (-1, -0.6)), ("B", (1, -0.6)), ("C", (1, 0)), ("D", (-1, 0.3)), ("S", (0, 1)), ("O", (0.8, -0.8))]:
        point(ax, V[n], n, d, col=ORANGE if n == "O" else DARK)
    right_angle(ax, V["O"], V["A"] - V["O"], V["S"] - V["O"], size=0.22, color=ORANGE)
    txt(ax, 3.4, -0.9, "$ABCD$ est un carré", NEUTRAL, 11.5, ha="center")
    cadre(ax, list(V.values()) + [P(2, -1.1)], 0.8)
    _save(fig, path)


d1(X("espace_4e_d1_pyramide.png"))


def d2(path, solution=False):
    fig, ax = new_fig(5.6, 5.2)
    S, O = cone_dessin(ax, 3 * 0.75, 4 * 0.75)
    A = P(3 * 0.75, 0)
    ax.plot([0, A[0]], [0, 0], lw=1.6, color=GREEN)
    right_angle(ax, O, (1, 0), (0, 1), size=0.2, color=ORANGE)
    point(ax, S, "S", (0, 1))
    point(ax, O, "O", (-0.6, -1), col=ORANGE)
    point(ax, A, "A", (1, -0.3))
    if solution:
        lab(ax, O, A, "3 cm", (0, -0.3), GREEN, 11.5, bold=True)
        lab(ax, O, S, "4 cm", (-0.45, 0), ORANGE, 11.5, bold=True)
        lab(ax, S, A, "5 cm", (0.55, 0.15), GREEN, 12, bold=True)
    cadre(ax, [S, P(-2.4, -0.9), P(3.2, 0)], 0.5)
    _save(fig, path)


d2(X("espace_4e_d2_cone.png"))
d2(X("espace_4e_d2_cone_solution.png"), solution=True)


def d3(path):
    fig, ax = new_fig(6.8, 5.4)
    V = pyramide_rect(ax, 4.0, 4.0, 4.0)
    for n, d in [("A", (-1, -0.6)), ("B", (1, -0.6)), ("C", (1, 0)), ("D", (-1, 0.3)), ("S", (0, 1)), ("O", (0.8, -0.8))]:
        point(ax, V[n], n, d, col=ORANGE if n == "O" else DARK)
    lab(ax, V["A"], V["B"], "6 cm", (0, -0.35))
    lab(ax, V["B"], V["C"], "6 cm", (0.55, -0.1))
    lab(ax, V["O"], V["S"], "5 cm", (0.45, 0), ORANGE, bold=True)
    right_angle(ax, V["O"], V["A"] - V["O"], V["S"] - V["O"], size=0.22, color=ORANGE)
    txt(ax, 3.0, -1.0, "base carrée", NEUTRAL, 11.5, ha="center")
    cadre(ax, list(V.values()) + [P(2, -1.1)], 0.8)
    _save(fig, path)


d3(X("espace_4e_d3.png"))


def d4(path):
    fig, ax = new_fig(4.8, 5.6)
    S, O = cone_dessin(ax, 1.5, 5.0)
    ax.plot([0, 1.5], [0, 0], lw=1.6, color=GREEN)
    right_angle(ax, O, (1, 0), (0, 1), size=0.2, color=ORANGE)
    lab(ax, O, P(1.5, 0), "3 cm", (0, -0.3), GREEN, bold=True)
    lab(ax, O, S, "10 cm", (-0.5, 0), ORANGE, bold=True)
    point(ax, S, "S", (0, 1))
    point(ax, O, "O", (-0.6, -1), col=ORANGE)
    cadre(ax, [S, P(-1.9, -0.8), P(1.9, 0)], 0.5)
    _save(fig, path)


d4(X("espace_4e_d4.png"))


def d5(path):
    fig, ax = new_fig(6.0, 5.6)
    pr = lambda x, y, z: P(*_proj(x, y, z, k=0.6))  # noqa: E731
    A, B, Cc, S = pr(0, 0, 0), pr(4, 0, 0), pr(0, 3, 0), pr(0, 0, 6)
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=LBLUE, edgecolor="none", zorder=0))
    for u, v_, h in [(A, B, 0), (B, Cc, 0), (A, Cc, 1), (S, A, 0), (S, B, 0), (S, Cc, 0)]:
        seg(ax, u, v_, BLUE, cache=bool(h))
    right_angle(ax, A, B - A, S - A, size=0.25, color=ORANGE)
    lab(ax, A, B, "4 cm", (0, -0.35))
    lab(ax, A, Cc, "3 cm", (-0.4, 0.15))
    lab(ax, A, S, "6 cm", (-0.5, 0), ORANGE, bold=True)
    for Q, n, d in [(A, "A", (-1, -0.6)), (B, "B", (1, -0.6)), (Cc, "C", (1, 0.3)), (S, "S", (0, 1))]:
        point(ax, Q, n, d)
    cadre(ax, [A, B, Cc, S], 0.9)
    _save(fig, path)


d5(X("espace_4e_d5.png"))
tableau(X("espace_4e_conversions_d6.png"),
        [["m³", "dm³", "cm³"], ["kL", "L", "mL"]], larg_col=[2.2, 2.2, 2.2],
        titre="1 m³ = 1 000 dm³ ; 1 dm³ = 1 000 cm³")
tableau(X("espace_4e_conversions_d6_solution.png"),
        [["volume", "en litres (L)"], ["$2{,}5$ dm³", "$2{,}5$ L"], ["$750$ cm³", "$0{,}75$ L"],
         ["$0{,}3$ m³", "$300$ L"], ["$60$ cm³", "$0{,}06$ L"]],
        larg_col=[2.6, 2.6], vert=[(i, 1) for i in range(1, 5)], titre="Conversions", entete_lig=False)


def patron(path, solution=False):
    fig, ax = new_fig(6.0, 6.0)
    a = 4.0
    hap = sqrt(25 - 4)
    sq = [P(0, 0), P(a, 0), P(a, a), P(0, a)]
    ax.add_patch(Polygon(sq, closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.2))
    tri = [(sq[0], sq[1], P(a / 2, -hap)), (sq[1], sq[2], P(a + hap, a / 2)), (sq[2], sq[3], P(a / 2, a + hap)),
           (sq[3], sq[0], P(-hap, a / 2))]
    for U, V_, W in tri:
        ax.add_patch(Polygon([U, V_, W], closed=True, facecolor=LORANGE, edgecolor=ORANGE, lw=2.2))
    lab(ax, sq[0], sq[1], "4 cm", (0, 0.32), BLUE)
    lab(ax, tri[1][0], tri[1][2], "5 cm", (0.2, -0.45), ORANGE)
    if solution:
        Hm = (sq[0] + sq[1]) / 2
        ax.plot([Hm[0], a / 2], [Hm[1], -hap], lw=1.6, color=GREEN, ls="--")
        right_angle(ax, Hm, (1, 0), (0, -1), size=0.22, color=GREEN)
        txt(ax, a / 2 + 0.12, -hap / 2, "≈ 4,58 cm", GREEN, 11.5, fontweight="bold")
        for (U, V_, W) in tri:
            ax.scatter([W[0]], [W[1]], s=30, color=GREEN, zorder=6)
        txt(ax, a / 2, a / 2, "ces 4 sommets\nforment S", GREEN, 10.5, ha="center", va="center")
    cadre(ax, [P(-hap, -hap), P(a + hap, a + hap)], 0.4)
    _save(fig, path)


patron(X("espace_4e_patron.png"))
patron(X("espace_4e_patron_solution.png"), solution=True)


# ================================================================ ENTRAÎNEMENT
def louvre(path, solution=False):
    fig, ax = new_fig(7.2, 5.0)
    s = 0.12
    V = pyramide_rect(ax, 35 * s, 35 * s, 21.6 * s, k=0.42, face="ABS" if solution else None)
    ax.plot([-0.8, 6.8], [-0.02, -0.02], lw=1.5, color=NEUTRAL)
    for n, d in [("A", (-1, -0.6)), ("B", (1, -0.6)), ("C", (1, 0)), ("D", (-1, 0.3)), ("S", (0, 1)), ("O", (0.8, -0.8))]:
        point(ax, V[n], n, d, col=ORANGE if n == "O" else DARK)
    lab(ax, V["A"], V["B"], "35 m", (0, -0.35))
    lab(ax, V["O"], V["S"], "21,6 m", (-0.6, 0), ORANGE, bold=True)
    if solution:
        Hm = (V["B"] + V["C"]) / 2
        seg(ax, V["O"], Hm, GREEN, lw=1.6)
        seg(ax, V["S"], Hm, GREEN, lw=2.0)
        point(ax, Hm, "H", (1, -0.3), col=GREEN)
        lab(ax, V["S"], Hm, "≈ 27,8 m", (0.75, 0.1), GREEN, bold=True)
    cadre(ax, list(V.values()) + [P(-0.8, 0), P(6.8, 0)], 0.6)
    _save(fig, path)


louvre(X("espace_4e_louvre.png"))
louvre(X("espace_4e_louvre_solution.png"), solution=True)


def cornet(path):
    fig, ax = new_fig(4.8, 5.8)
    s = 0.38
    S, O = cone_dessin(ax, 2.5 * s, 12 * s, centre=(0, 0), pointe_bas=True, col="#b9770e")
    t = np.linspace(0, np.pi, 80)
    ax.fill_between(2.5 * s * np.cos(t), 0, 2.5 * s * 0.9 * np.sin(t) + 0.0, color="#f5b7b1", zorder=0)
    for i in range(1, 6):
        y = -12 * s * i / 6
        w_ = 2.5 * s * (1 - i / 6)
        ax.plot([-w_, w_], [y, y], lw=0.8, color="#d4ac0d")
    ax.plot([0, 2.5 * s], [0, 0], lw=1.6, color=GREEN)
    lab(ax, O, P(2.5 * s, 0), "2,5 cm", (0.15, 0.3), GREEN, 11, bold=True)
    lab(ax, O, S, "12 cm", (-0.55, 0), ORANGE, 11.5, bold=True)
    point(ax, S, "S", (0, -1))
    point(ax, O, "O", (-1, 0.4), col=ORANGE)
    cadre(ax, [S, P(-1.6, 1.0), P(1.8, 0)], 0.4)
    _save(fig, path)


cornet(X("espace_4e_cornet.png"))


def tas_sable(path, solution=False):
    fig, ax = new_fig(6.6, 4.0)
    r, h = 2.0, 1.5
    t = np.linspace(-np.pi, 0, 80)
    ax.add_patch(Polygon([(-r, 0), (0, h), (r, 0)] + [(r * np.cos(a), 0.3 * r * np.sin(a)) for a in t[::-1]],
                         closed=True, facecolor="#f8e5b9", edgecolor="none", zorder=0))
    S, O = cone_dessin(ax, r, h, col="#b9770e")
    ax.plot([0, r], [0, 0], lw=1.6, color=GREEN)
    right_angle(ax, O, (1, 0), (0, 1), size=0.18, color=ORANGE)
    lab(ax, P(-r, -0.75), P(r, -0.75), "diamètre : 4 m", (0, 0), DARK, 11.5)
    ax.annotate("", xy=(r, -0.75 + 0.2), xytext=(-r, -0.75 + 0.2), arrowprops=dict(arrowstyle="<->", color=DARK))
    lab(ax, O, S, "1,5 m", (-0.45, 0), ORANGE, 11.5, bold=True)
    A = P(r, 0)
    point(ax, S, "S", (0, 1))
    point(ax, O, "O", (-0.4, -1), col=ORANGE, fs=12)
    point(ax, A, "A", (1, 0), fs=12)
    if solution:
        lab(ax, S, A, "2,5 m", (0.45, 0.25), GREEN, 12, bold=True)
        from fig4e import angle_arc
        angle_arc(ax, A, S - A, P(-1, 0), r=0.55, color=GREEN, lw=2, label="≈ 36,9°", label_r=1.2, fs=11)
    cadre(ax, [S, P(-r, -1.1), P(r + 0.6, 0)], 0.5)
    _save(fig, path)


tas_sable(X("espace_4e_tas_sable.png"))
tas_sable(X("espace_4e_tas_sable_solution.png"), solution=True)


def e4(path):
    fig, ax = new_fig(8.4, 4.6)
    V = pyramide_rect(ax, 3.0, 3.0, 4.2, k=0.45)
    for n, d in [("A", (-1, -0.6)), ("B", (1, -0.6)), ("S", (0, 1)), ("O", (0.8, -0.8))]:
        point(ax, V[n], n, d, col=ORANGE if n == "O" else DARK, fs=12)
    lab(ax, V["A"], V["B"], "5 cm", (0, -0.35))
    lab(ax, V["O"], V["S"], "h = ?", (0.6, 0), ORANGE, bold=True)
    txt(ax, 2.0, -1.0, "$V = 75$ cm³", DARK, 13, ha="center")
    S, O = cone_dessin(ax, 1.8, 3.4, centre=(7.5, 0))
    ax.plot([7.5, 9.3], [0, 0], lw=1.6, color=GREEN)
    lab(ax, O, P(9.3, 0), "4 cm", (0, -0.3), GREEN)
    lab(ax, O, S, "h = ?", (-0.6, 0), ORANGE, bold=True)
    txt(ax, 7.5, -1.0, "$V = 100$ cm³", DARK, 13, ha="center")
    cadre(ax, list(V.values()) + [S, P(9.6, -1.2)], 0.4)
    _save(fig, path)


e4(X("espace_4e_e4.png"))


def cube_solides(path):
    fig, ax = new_fig(9.4, 4.6)
    pr = lambda x, y, z, dx=0: P(*_proj(x, y, z)) + P(dx, 0)  # noqa: E731
    a = 3.6
    cube = {"A": pr(0, 0, 0), "B": pr(a, 0, 0), "C": pr(a, a, 0), "D": pr(0, a, 0),
            "E": pr(0, 0, a), "F": pr(a, 0, a), "G": pr(a, a, a), "H": pr(0, a, a)}
    for u, v_, h in [("A", "B", 0), ("B", "C", 0), ("C", "D", 1), ("D", "A", 1), ("E", "F", 0), ("F", "G", 0),
                     ("G", "H", 0), ("H", "E", 0), ("A", "E", 0), ("B", "F", 0), ("C", "G", 0), ("D", "H", 1)]:
        seg(ax, cube[u], cube[v_], NEUTRAL, lw=1.8, cache=bool(h))
    S = pr(a / 2, a / 2, a)
    for n, h in [("A", 0), ("B", 0), ("C", 0), ("D", 1)]:
        seg(ax, cube[n], S, ORANGE, cache=bool(h))
    lab(ax, cube["A"], cube["B"], "6 cm", (0, -0.35))
    txt(ax, 2.4, -1.0, "cube et pyramide", DARK, 12, ha="center")
    cylindre_dessin(ax, 1.8, 3.6, base=(8.2, 0), col=NEUTRAL, lw=1.8)
    cone_dessin(ax, 1.8, 3.6, centre=(8.2, 0), col=ORANGE)
    lab(ax, P(8.2, 0), P(10.0, 0), "r = 3 cm", (0, -0.3), DARK, 11)
    txt(ax, 8.2, -1.0, "cylindre et cône", DARK, 12, ha="center")
    txt(ax, 10.6, 1.8, "h = 6 cm", ORANGE, 11.5, va="center")
    cadre(ax, list(cube.values()) + [P(11.8, -1.2), P(8.2, 4.2)], 0.3)
    _save(fig, path)


cube_solides(X("espace_4e_cube_solides.png"))


def e6(path):
    fig, ax = new_fig(8.6, 4.8)
    V = pyramide_rect(ax, 4.6, 3.0, 4.0)
    for n, d in [("A", (-1, -0.6)), ("B", (1, -0.6)), ("C", (1, 0)), ("D", (-1, 0.3)), ("S", (0, 1)), ("O", (0.8, -0.8))]:
        point(ax, V[n], n, d, col=ORANGE if n == "O" else DARK, fs=12)
    lab(ax, V["A"], V["B"], "6 cm", (0, -0.35))
    lab(ax, V["B"], V["C"], "4 cm", (0.5, -0.15))
    lab(ax, V["O"], V["S"], "5 cm", (0.45, -0.2), ORANGE, bold=True)
    lab(ax, V["B"], V["S"], "7 cm", (0.45, 0.1), BLUE)
    S, O = cone_dessin(ax, 1.8, 2.4, centre=(8.8, 0.4))
    ax.plot([8.8, 10.6], [0.4, 0.4], lw=1.6, color=GREEN)
    lab(ax, O, P(10.6, 0.4), "3 cm", (0, -0.3), GREEN)
    lab(ax, O, S, "4 cm", (-0.45, 0.2), ORANGE, bold=True)
    cadre(ax, list(V.values()) + [S, P(10.8, -0.3)], 0.6)
    _save(fig, path)


e6(X("espace_4e_e6.png"))


def tente(path, solution=False):
    fig, ax = new_fig(6.6, 5.0)
    V = pyramide_rect(ax, 4.0, 4.0, 3.6, k=0.45, face="BCS")
    ax.plot([-0.8, 6.6], [-0.02, -0.02], lw=1.5, color="#58a55c")
    for n, d in [("A", (-1, -0.6)), ("B", (1, -0.6)), ("C", (1, 0)), ("D", (-1, 0.3)), ("S", (0, 1)), ("O", (0.8, -0.8))]:
        point(ax, V[n], n, d, col=ORANGE if n == "O" else DARK, fs=12)
    lab(ax, V["A"], V["B"], "2 m", (0, -0.35))
    lab(ax, V["O"], V["S"], "1,8 m", (-0.55, 0), ORANGE, bold=True)
    if solution:
        Hm = (V["B"] + V["C"]) / 2
        seg(ax, V["O"], Hm, GREEN, lw=1.6)
        seg(ax, V["S"], Hm, GREEN, lw=2.0)
        point(ax, Hm, "H", (1, -0.3), col=GREEN, fs=12)
        lab(ax, V["S"], Hm, "≈ 2,06 m", (0.8, 0.15), GREEN, bold=True)
        lab(ax, V["O"], Hm, "1 m", (0, -0.28), GREEN, 11)
    cadre(ax, list(V.values()) + [P(6.6, 0)], 0.6)
    _save(fig, path)


tente(X("espace_4e_tente.png"))
tente(X("espace_4e_tente_solution.png"), solution=True)


# =================================================================== PROBLÈMES
def sablier(path):
    fig, ax = new_fig(4.8, 6.4)
    r, h = 1.8, 2.4
    ax.add_patch(Rectangle((-2.4, 2 * h + 0.65), 4.8, 0.3, facecolor="#a04000", edgecolor=DARK))
    ax.add_patch(Rectangle((-2.4, -0.95), 4.8, 0.3, facecolor="#a04000", edgecolor=DARK))
    ys = 2 * h - 0.25 * h
    w_ = r * (ys - h) / h
    ax.add_patch(Polygon([(-w_, ys), (w_, ys), (0, h)], closed=True, facecolor="#f8c471", edgecolor="none", zorder=0))
    ax.add_patch(Polygon([(-0.7, 0), (0.7, 0), (0, 0.45)], closed=True, facecolor="#f8c471", edgecolor="none",
                         zorder=0))
    cone_dessin(ax, r, h, centre=(0, 2 * h), pointe_bas=True, axe=False, col=BLUE)
    cone_dessin(ax, r, h, centre=(0, 0), axe=False, col=BLUE)
    ax.plot([0, 0], [0, 2 * h], lw=1.2, color=ORANGE, ls="--")
    ax.plot([0, r], [2 * h, 2 * h], lw=1.6, color=GREEN)
    lab(ax, P(0, 2 * h), P(r, 2 * h), "3 cm", (0, 0.3), GREEN, 11.5, bold=True)
    lab(ax, P(0, h), P(0, 2 * h), "4 cm", (0.5, -0.2), ORANGE, 11.5, bold=True)
    lab(ax, P(0, 0), P(0, h), "4 cm", (0.5, 0.2), ORANGE, 11.5, bold=True)
    txt(ax, -1.9, 2 * h - 0.9, "sable", "#b9770e", 11, ha="right")
    cadre(ax, [P(-2.4, -1.0), P(2.4, 2 * h + 1.0)], 0.3)
    _save(fig, path)


sablier(X("espace_4e_sablier.png"))


def maison(path):
    fig, ax = new_fig(7.4, 5.4)
    s = 0.42
    L, Pf, H, Hc = 10 * s, 8 * s, 2.5 * s, 3 * s
    pr = lambda x, y, z: P(*_proj(x, y, z, k=0.5))  # noqa: E731
    bas = [pr(0, 0, 0), pr(L, 0, 0), pr(L, Pf, 0), pr(0, Pf, 0)]
    haut = [pr(0, 0, H), pr(L, 0, H), pr(L, Pf, H), pr(0, Pf, H)]
    S = pr(L / 2, Pf / 2, H + Hc)
    ax.add_patch(Polygon([bas[0], bas[1], haut[1], haut[0]], closed=True, facecolor="#fdf2e9", edgecolor="none"))
    ax.add_patch(Polygon([haut[0], haut[1], S], closed=True, facecolor="#e59866", edgecolor="none"))
    ax.add_patch(Polygon([haut[1], haut[2], S], closed=True, facecolor="#dc7633", edgecolor="none"))
    for i in range(4):
        seg(ax, bas[i], bas[(i + 1) % 4], BLUE, cache=i in (2, 3))
        seg(ax, haut[i], haut[(i + 1) % 4], BLUE, cache=i in (2, 3))
        seg(ax, bas[i], haut[i], BLUE, cache=i == 3)
        seg(ax, haut[i], S, "#a04000", cache=i == 3)
    O = pr(L / 2, Pf / 2, H)
    ax.plot([O[0], S[0]], [O[1], S[1]], lw=1.5, color=ORANGE, ls="--")
    lab(ax, bas[0], bas[1], "10 m", (0, -0.35))
    lab(ax, bas[1], bas[2], "8 m", (0.5, -0.15))
    lab(ax, bas[1], haut[1], "2,5 m", (0.5, 0))
    lab(ax, O, S, "3 m", (0.35, 0), ORANGE, bold=True)
    cadre(ax, bas + haut + [S], 0.7)
    _save(fig, path)


maison(X("espace_4e_maison.png"))


def verre(path, solution=False):
    fig, ax = new_fig(5.0, 6.2)
    s = 0.5
    r, h = 4 * s, 9 * s
    top = P(0, h)
    if solution:
        ax.add_patch(Polygon([(0, 0), (-r / 2, h / 2), (r / 2, h / 2)], closed=True, facecolor="#aed6f1",
                             edgecolor="none", zorder=0))
        t = np.linspace(0, 2 * np.pi, 120)
        ax.plot(r / 2 * np.cos(t), h / 2 + 0.3 * r / 2 * np.sin(t), lw=1.4, color="#2874a6")
    t = np.linspace(0, 2 * np.pi, 160)
    ax.plot(r * np.cos(t), h + 0.3 * r * np.sin(t), lw=2.2, color=BLUE)
    ax.plot([-r, 0], [h, 0], lw=2.2, color=BLUE)
    ax.plot([r, 0], [h, 0], lw=2.2, color=BLUE)
    ax.plot([0, 0], [0, -1.6], lw=3, color=BLUE)
    ax.plot([-1.0, 1.0], [-1.6, -1.6], lw=3, color=BLUE)
    ax.plot([0, 0], [0, h], lw=1.4, color=ORANGE, ls="--")
    ax.plot([0, r], [h, h], lw=1.6, color=GREEN)
    lab(ax, top, top + P(r, 0), "4 cm", (0, 0.35), GREEN, 11.5, bold=True)
    lab(ax, P(0, 0), top, "9 cm", (0.5, 0), ORANGE, 11.5, bold=True, t=0.78)
    if solution:
        ax.plot([0, r / 2], [h / 2, h / 2], lw=1.6, color=GREEN)
        lab(ax, P(0, h / 2), P(r / 2, h / 2), "2 cm", (0.95, 0), GREEN, 11, bold=True)
        lab(ax, P(0, 0), P(0, h / 2), "4,5 cm", (-0.6, 0), ORANGE, 11)
    point(ax, P(0, 0), "S", (1, -0.2), fs=12)
    cadre(ax, [P(-r, -1.7), P(r, h + 0.8)], 0.4)
    _save(fig, path)


verre(X("espace_4e_verre.png"))
verre(X("espace_4e_verre_solution.png"), solution=True)


def kheops(path, solution=False):
    fig, ax = new_fig(7.4, 4.8)
    s = 0.024
    V = pyramide_rect(ax, 230 * s, 230 * s, 146 * s, k=0.4, face="BCS" if solution else None)
    ax.plot([-0.8, 8.4], [-0.02, -0.02], lw=1.5, color="#d4ac0d")
    for n, d in [("A", (-1, -0.6)), ("B", (1, -0.6)), ("C", (1, 0)), ("S", (0, 1)), ("O", (0.8, -0.8))]:
        point(ax, V[n], n, d, col=ORANGE if n == "O" else DARK, fs=12)
    lab(ax, V["A"], V["B"], "230 m", (0, -0.35))
    lab(ax, V["O"], V["S"], "146 m", (-0.6, 0), ORANGE, bold=True)
    if solution:
        Hm = (V["B"] + V["C"]) / 2
        seg(ax, V["O"], Hm, GREEN, lw=1.6)
        seg(ax, V["S"], Hm, GREEN, lw=2.0)
        point(ax, Hm, "H", (1, -0.3), col=GREEN, fs=12)
        lab(ax, V["O"], Hm, "115 m", (0, -0.3), GREEN, 11)
        lab(ax, V["S"], Hm, "≈ 185,9 m", (0.95, 0.2), GREEN, bold=True)
    cadre(ax, list(V.values()) + [P(-0.8, 0), P(8.4, 0)], 0.6)
    _save(fig, path)


kheops(X("espace_4e_kheops.png"))
kheops(X("espace_4e_kheops_solution.png"), solution=True)


def silo(path):
    fig, ax = new_fig(4.8, 6.4)
    s = 0.6
    r, hc, hk = 2 * s, 6 * s, 1.5 * s
    cylindre_dessin(ax, r, hc, base=(0, 0), col=BLUE)
    cone_dessin(ax, r, hk, centre=(0, 0), pointe_bas=True, axe=False, col=BLUE)
    t = np.linspace(0, 2 * np.pi, 160)
    ax.plot(r * np.cos(t[t > np.pi]), 0.3 * r * np.sin(t[t > np.pi]), lw=1.3, color=BLUE, ls="--")
    ax.plot([-0.4, -0.4], [-hk - 1.2, -hk - 0.05], lw=2, color=NEUTRAL)
    ax.plot([0.4, 0.4], [-hk - 1.2, -hk - 0.05], lw=2, color=NEUTRAL)
    ax.plot([0, r], [hc, hc], lw=1.6, color=GREEN)
    lab(ax, P(0, hc), P(r, hc), "2 m", (0, 0.4), GREEN, 13, bold=True)
    lab(ax, P(r, 0), P(r, hc), "6 m", (0.6, 0), ORANGE, 13, bold=True)
    lab(ax, P(0, 0), P(0, -hk), "1,5 m", (-0.95, -0.1), ORANGE, 13, bold=True)
    ax.plot([0, 0], [0, -hk], lw=1.4, color=ORANGE, ls="--")
    cadre(ax, [P(-r, -hk - 1.2), P(r + 1.2, hc + 0.8)], 0.3)
    _save(fig, path)


silo(X("espace_4e_silo.png"))


def bougies(path):
    fig, ax = new_fig(8.0, 4.6)
    V = pyramide_rect(ax, 3.0, 3.0, 4.5, k=0.45, hauteur=True)
    lab(ax, V["A"], V["B"], "6 cm", (0, -0.35))
    lab(ax, V["O"], V["S"], "9 cm", (0.5, 0), ORANGE, bold=True)
    ax.plot([V["S"][0], V["S"][0]], [V["S"][1], V["S"][1] + 0.5], lw=2, color=DARK)
    S, O = cone_dessin(ax, 1.5, 4.5, centre=(7.0, 0.3))
    ax.plot([S[0], S[0]], [S[1], S[1] + 0.5], lw=2, color=DARK)
    ax.plot([7.0, 8.5], [0.3, 0.3], lw=1.6, color=GREEN)
    lab(ax, O, P(8.5, 0.3), "3 cm", (0, -0.3), GREEN)
    lab(ax, O, S, "9 cm", (-0.45, 0), ORANGE, bold=True)
    txt(ax, 2.2, -1.0, "bougie pyramide", DARK, 12, ha="center")
    txt(ax, 7.0, -1.0, "bougie cône", DARK, 12, ha="center")
    cadre(ax, list(V.values()) + [S + P(0, 0.6), P(8.8, -1.2)], 0.4)
    _save(fig, path)


bougies(X("espace_4e_bougies.png"))


def gobelet(path, solution=False):
    fig, ax = new_fig(4.8, 5.8)
    s = 0.42
    r, h = 3.5 * s, sqrt(68.75) * s
    S, O = cone_dessin(ax, r, h, centre=(0, 0), pointe_bas=True, col=BLUE)
    A = P(r, 0)
    ax.plot([0, r], [0, 0], lw=1.6, color=GREEN)
    right_angle(ax, O, (1, 0), (0, -1), size=0.18, color=ORANGE)
    lab(ax, O, A, "3,5 cm", (0, 0.3), GREEN, 11, bold=True)
    lab(ax, S, A, "9 cm", (0.55, -0.1), BLUE, 11.5)
    if solution:
        lab(ax, O, S, "≈ 8,29 cm", (-0.85, 0), ORANGE, 11, bold=True)
        from fig4e import angle_arc
        angle_arc(ax, S, P(0, 1), A - S, r=0.7, color=GREEN, lw=2, label="≈ 22,9°", label_r=1.4, fs=10.5)
    else:
        lab(ax, O, S, "?", (-0.4, 0), ORANGE, 13, bold=True)
    point(ax, S, "S", (0, -1))
    point(ax, O, "O", (-1, 0.4), col=ORANGE)
    point(ax, A, "A", (1, 0.3))
    cadre(ax, [S, P(-r - 0.6, 0.8), P(r + 0.8, 0)], 0.4)
    _save(fig, path)


gobelet(X("espace_4e_gobelet.png"))
gobelet(X("espace_4e_gobelet_solution.png"), solution=True)
