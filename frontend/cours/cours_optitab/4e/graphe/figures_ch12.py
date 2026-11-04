# -*- coding: utf-8 -*-
"""Figures du chapitre 12 (construire et comparer des triangles) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, finish, _save, dot_label, seg_label, tick_marks, right_angle, angle_arc,
                   BLUE, ORANGE, GREEN, DARK, NEUTRAL, DIR_COURS, DIR_EXOS)
import numpy as np
from math import radians, cos, sin, sqrt
from matplotlib.patches import Arc, Polygon

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
P = lambda x, y: np.array([x, y], float)  # noqa: E731
LBLUE, LORANGE, LGREEN = "#d6eafc", "#fdebd0", "#e8f5e9"
PURP = "#8e44ad"


def tri(ax, A, B, Cc, col=BLUE, fc=None, lw=2.2):
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=fc or "none", edgecolor=col, lw=lw))


def lab(ax, pts, col=DARK):
    for Pt, n, off in pts:
        dot_label(ax, Pt, f"${n}$", *off, color=col, s=28)


def third_point(A, B, ra, rb, up=True):
    """Point à distance ra de A et rb de B (au-dessus de (AB) si up)."""
    d = np.linalg.norm(B - A)
    a = (ra ** 2 - rb ** 2 + d ** 2) / (2 * d)
    h = sqrt(max(ra ** 2 - a ** 2, 0))
    u = (B - A) / d
    n = np.array([-u[1], u[0]])
    return A + a * u + (h if up else -h) * n


# ------------------------------------------------------------------ construction CCC
def construction_ccc(path, AB=6, AC=5, BC=4, deux=False):
    fig, ax = new_fig(7.4, 5.6)
    A, B = P(0, 0), P(AB, 0)
    Cc = third_point(A, B, AC, BC)
    ax.plot([A[0], B[0]], [A[1], B[1]], lw=2.4, color=BLUE)
    angA = np.degrees(np.arctan2(Cc[1] - A[1], Cc[0] - A[0]))
    angB = np.degrees(np.arctan2(Cc[1] - B[1], Cc[0] - B[0]))
    span = 25
    for ctr, rr, ang in [(A, AC, angA), (B, BC, angB)]:
        ax.add_patch(Arc(ctr, 2 * rr, 2 * rr, theta1=ang - span, theta2=ang + span, color=ORANGE, lw=1.6))
        if deux:
            ax.add_patch(Arc(ctr, 2 * rr, 2 * rr, theta1=-ang - span, theta2=-ang + span, color=ORANGE,
                             lw=1.6))
    tri(ax, A, B, Cc, GREEN, LGREEN)
    pts = [(A, "A", (-16, -14)), (B, "B", (6, -14)), (Cc, "C", (-4, 8))]
    if deux:
        C2 = np.array([Cc[0], -Cc[1]])
        tri(ax, A, B, C2, GREEN)
        ax.plot([A[0], C2[0], B[0]], [A[1], C2[1], B[1]], lw=1.6, color=GREEN, ls="--")
        pts.append((C2, "C'", (-6, -18)))
    seg_label(ax, A, B, "6 cm", side=-1, offset=0.38, fs=12)
    seg_label(ax, A, Cc, "5 cm", side=1, offset=0.38, fs=12, color=ORANGE)
    seg_label(ax, B, Cc, "4 cm", side=-1, offset=0.38, fs=12, color=ORANGE)
    lab(ax, pts)
    allp = [A, B, Cc] + ([np.array([Cc[0], -Cc[1]])] if deux else [P(0, -0.5)])
    finish(fig, ax, path, allp, margin=0.9)


construction_ccc(C("triangles_4e_construction.png"))
construction_ccc(X("triangles_4e_ccc_solution.png"), deux=True)


# ------------------------------------------------------------------ inégalité triangulaire
def inegalite(path, cas):
    fig, ax = new_fig(10.0, 3.6)
    x0 = 0
    for a, b, c, titre, col in cas:
        A, B = P(x0, 0), P(x0 + c * 0.55, 0)
        ax.plot([A[0], B[0]], [0, 0], lw=2.4, color=DARK)
        if a + b > c:
            Cc = third_point(A, B, a * 0.55, b * 0.55)
            ax.plot([A[0], Cc[0], B[0]], [A[1], Cc[1], B[1]], lw=2.4, color=col)
        else:
            ang = 25
            ax.plot([A[0], A[0] + a * 0.55 * cos(radians(ang))], [0, a * 0.55 * sin(radians(ang))], lw=2.4,
                    color=col)
            ax.plot([B[0], B[0] - b * 0.55 * cos(radians(ang))], [0, b * 0.55 * sin(radians(ang))], lw=2.4,
                    color=col)
        ax.text((A[0] + B[0]) / 2, -0.45, titre, ha="center", va="top", fontsize=11.5, color=col,
                fontweight="bold")
        x0 += c * 0.55 + 1.3
    ax.set_xlim(-0.4, x0 - 0.9)
    ax.set_ylim(-1.5, 2.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


inegalite(C("triangles_4e_inegalite.png"),
          [(4, 5, 6, "4 ; 5 ; 6 : 4 + 5 > 6\ntriangle possible", GREEN),
           (3, 4, 8, "3 ; 4 ; 8 : 3 + 4 < 8\nimpossible", "#c0392b")])
inegalite(X("triangles_4e_inegalite_solution.png"),
          [(3, 4, 8, "3 ; 4 ; 8\nimpossible", "#c0392b"), (4, 5, 6, "4 ; 5 ; 6\npossible", GREEN),
           (5, 7, 12, "5 ; 7 ; 12\naplati", ORANGE)])


# ------------------------------------------------------------------ les trois cas d'égalité
def code_angle(ax, S, U, V, n=1, col=ORANGE, r=0.42):
    angle_arc(ax, S, U - S, V - S, r=r, color=col, n=n, dr=0.1)


def paire(ax, x0, y0, cas, titre, s=1.6, k=1.0):
    A, B, Cc = P(x0, y0), P(x0 + 2.6 * s, y0), P(x0 + 0.9 * s, y0 + 1.9 * s)
    A2 = P(x0 + 3.6 * s, y0 + 1.9 * s)
    B2 = A2 + k * P(2.6 * s, 0)
    C2 = A2 + k * P(0.9 * s, -1.9 * s)
    for (a, b, c) in [(A, B, Cc), (A2, B2, C2)]:
        tri(ax, a, b, c, BLUE, LBLUE)
        if cas == "CCC":
            tick_marks(ax, a, b, 1, size=0.25)
            tick_marks(ax, b, c, 2, size=0.25)
            tick_marks(ax, a, c, 3, size=0.25)
        if cas == "CAC":
            tick_marks(ax, a, b, 1, size=0.25)
            tick_marks(ax, a, c, 2, size=0.25)
            code_angle(ax, a, b, c, 1, r=0.55)
        if cas == "ACA":
            tick_marks(ax, a, b, 1, size=0.25)
            code_angle(ax, a, b, c, 1, r=0.55)
            code_angle(ax, b, a, c, 2, col=GREEN, r=0.55)
        if cas == "AAA":
            code_angle(ax, a, b, c, 1, r=0.55)
            code_angle(ax, b, a, c, 2, col=GREEN, r=0.55)
            code_angle(ax, c, a, b, 3, col=PURP, r=0.4)
    ax.text(x0 + 3.1 * s * (1 + 0.15 * (k - 1)), y0 - 0.35, titre, ha="center", va="top", fontsize=13,
            color=DARK, fontweight="bold")


def trois_cas(path):
    fig, ax = new_fig(7.6, 10.0)
    for i, (cas, t) in enumerate([("CCC", "CCC : trois côtés respectivement égaux"),
                                  ("CAC", "CAC : deux côtés et l'angle compris"),
                                  ("ACA", "ACA : un côté et les deux angles adjacents")]):
        paire(ax, 0, -i * 4.6, cas, t)
    ax.set_xlim(-0.4, 10.6)
    ax.set_ylim(-10.4, 3.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


trois_cas(C("triangles_4e_cas_egalite.png"))


def quatre_paires(path):
    fig, ax = new_fig(8.2, 10.6)
    for i, (cas, t, k) in enumerate([("CCC", "paire ①", 1.0), ("CAC", "paire ②", 1.0),
                                     ("ACA", "paire ③", 1.0), ("AAA", "paire ④", 1.3)]):
        paire(ax, 0, -i * 4.4, cas, t, s=1.45, k=k)
    ax.set_xlim(-0.4, 11.2)
    ax.set_ylim(-14.2, 3.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


quatre_paires(X("triangles_4e_paires.png"))


# ------------------------------------------------------------------ CAC et ACA construits
def construction_cac(path):
    fig, ax = new_fig(7.0, 5.0)
    A, B = P(0, 0), P(5, 0)
    Cc = A + 4 * P(cos(radians(50)), sin(radians(50)))
    ax.plot([A[0], A[0] + 5.6 * cos(radians(50))], [A[1], 5.6 * sin(radians(50))], lw=1.2, color=NEUTRAL,
            ls="--")
    tri(ax, A, B, Cc, GREEN, LGREEN)
    angle_arc(ax, A, B - A, Cc - A, r=0.8, color=ORANGE, label="50°", label_r=1.25, fs=12)
    seg_label(ax, A, B, "5 cm", side=-1, offset=0.38, fs=12)
    seg_label(ax, A, Cc, "4 cm", side=1, offset=0.4, fs=12)
    seg_label(ax, B, Cc, "≈ 3,9 cm", side=-1, offset=0.55, fs=12, color=GREEN, weight="bold")
    lab(ax, [(A, "A", (-16, -14)), (B, "B", (6, -14)), (Cc, "C", (-4, 8))])
    finish(fig, ax, path, [A, B, Cc, P(0, -0.6), P(3.6, 4.3)], margin=0.8)


construction_cac(X("triangles_4e_cac_solution.png"))


def construction_aca(path):
    fig, ax = new_fig(7.0, 5.0)
    B, Cc = P(0, 0), P(6, 0)
    AB = 6 * sin(radians(60)) / sin(radians(80))
    A = B + AB * P(cos(radians(40)), sin(radians(40)))
    tri(ax, A, B, Cc, GREEN, LGREEN)
    angle_arc(ax, B, Cc - B, A - B, r=0.9, color=ORANGE, label="40°", label_r=1.35, fs=12)
    angle_arc(ax, Cc, B - Cc, A - Cc, r=0.8, color=ORANGE, label="60°", label_r=1.25, fs=12)
    angle_arc(ax, A, B - A, Cc - A, r=0.5, color=GREEN, label="80°", label_r=0.95, fs=12)
    seg_label(ax, B, Cc, "6 cm", side=-1, offset=0.38, fs=12)
    lab(ax, [(A, "A", (-4, 8)), (B, "B", (-16, -14)), (Cc, "C", (6, -14))])
    finish(fig, ax, path, [A, B, Cc, P(0, -0.6)], margin=0.8)


construction_aca(X("triangles_4e_aca_solution.png"))


# ------------------------------------------------------------------ correspondance des sommets
def correspondance(path):
    fig, ax = new_fig(9.0, 4.0)
    A, B = P(0, 0), P(5, 0)
    Cc = third_point(A, B, 6, 7)
    Cc = P(Cc[0], abs(Cc[1]))
    tri(ax, A, B, Cc, BLUE, LBLUE)
    seg_label(ax, A, B, "5", side=-1, offset=0.35, fs=12)
    seg_label(ax, A, Cc, "6", side=1, offset=0.35, fs=12)
    seg_label(ax, B, Cc, "7", side=-1, offset=0.35, fs=12)
    lab(ax, [(A, "A", (-16, -14)), (B, "B", (6, -14)), (Cc, "C", (-4, 8))])
    # triangle DEF retourné (symétrique) et déplacé
    off = P(9.5, 0)
    D_, E_ = off + P(5, 0), off + P(0, 0)
    F_ = off + P(5 - Cc[0], Cc[1])
    tri(ax, D_, E_, F_, ORANGE, LORANGE)
    seg_label(ax, E_, D_, "5", side=1, offset=-0.35, fs=12)
    seg_label(ax, D_, F_, "6", side=-1, offset=0.35, fs=12)
    seg_label(ax, E_, F_, "7", side=1, offset=0.35, fs=12)
    lab(ax, [(D_, "D", (6, -14)), (E_, "E", (-16, -14)), (F_, "F", (-4, 8))])
    finish(fig, ax, path, [A, B, Cc, D_, E_, F_], margin=0.8)


correspondance(X("triangles_4e_correspondance.png"))


# ------------------------------------------------------------------ parallélogramme, isocèle, cerf-volant
def parallelogramme(path):
    fig, ax = new_fig(7.6, 4.0)
    A, B = P(0, 0), P(7, 0)
    D_ = P(-1.37, 3.76)  # AD = 4, angle A = 110°
    Cc = B + D_ - A
    ax.add_patch(Polygon([A, B, Cc, D_], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.2))
    ax.plot([A[0], Cc[0]], [A[1], Cc[1]], lw=2, color=ORANGE)
    tick_marks(ax, A, B, 1)
    tick_marks(ax, D_, Cc, 1)
    tick_marks(ax, A, D_, 2)
    tick_marks(ax, B, Cc, 2)
    lab(ax, [(A, "A", (-16, -14)), (B, "B", (6, -14)), (Cc, "C", (6, 4)), (D_, "D", (-16, 4))])
    finish(fig, ax, path, [A, B, Cc, D_], margin=0.8)


parallelogramme(X("triangles_4e_parallelogramme.png"))


def isocele(path):
    fig, ax = new_fig(6.0, 5.2)
    B, Cc = P(0, 0), P(4, 0)
    A = P(2, 4.2)
    H = P(2, 0)
    tri(ax, A, B, Cc, BLUE, LBLUE)
    ax.plot([A[0], H[0]], [A[1], H[1]], lw=2, color=ORANGE)
    tick_marks(ax, A, B, 2)
    tick_marks(ax, A, Cc, 2)
    tick_marks(ax, B, H, 1)
    tick_marks(ax, H, Cc, 1)
    lab(ax, [(A, "A", (-4, 8)), (B, "B", (-16, -14)), (Cc, "C", (6, -14)), (H, "H", (-4, -18))])
    finish(fig, ax, path, [A, B, Cc, H], margin=0.8)


isocele(X("triangles_4e_isocele.png"))


def cerf_volant(path, mesures=False):
    fig, ax = new_fig(6.0, 6.0)
    A, Cc = P(0, 3.2), P(0, -4.6)
    B, D_ = P(-2.5, 1.2), P(2.5, 1.2)
    ax.add_patch(Polygon([A, B, Cc, D_], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.2))
    ax.plot([A[0], Cc[0]], [A[1], Cc[1]], lw=1.8, color=ORANGE)
    if mesures:
        H = P(0, 1.2)
        ax.plot([B[0], D_[0]], [B[1], D_[1]], lw=1.8, color=ORANGE)
        right_angle(ax, H, (1, 0), (0, 1), size=0.25)
        lab(ax, [(H, "H", (10, 8))])
        seg_label(ax, A, H, "20", side=1, offset=0.35, fs=11)
        seg_label(ax, H, Cc, "60", side=1, offset=0.35, fs=11)
        seg_label(ax, B, H, "25", side=-1, offset=0.3, fs=11)
        seg_label(ax, H, D_, "25", side=-1, offset=0.3, fs=11)
    else:
        tick_marks(ax, A, B, 1)
        tick_marks(ax, A, D_, 1)
        tick_marks(ax, B, Cc, 2)
        tick_marks(ax, D_, Cc, 2)
    lab(ax, [(A, "A", (-4, 8)), (B, "B", (-18, -4)), (Cc, "C", (-4, -18)), (D_, "D", (8, -4))])
    finish(fig, ax, path, [A, B, Cc, D_], margin=0.9)


cerf_volant(X("triangles_4e_cerf_volant.png"))
cerf_volant(X("triangles_4e_cerf_volant_baguettes.png"), mesures=True)


def milieu_commun(path):
    fig, ax = new_fig(7.0, 4.6)
    O = P(0, 0)
    A, B = P(-3, -0.8), P(3, 0.8)
    Cc, D_ = P(-1.2, 2.2), P(1.2, -2.2)
    ax.plot([A[0], B[0]], [A[1], B[1]], lw=2.2, color=BLUE)
    ax.plot([Cc[0], D_[0]], [Cc[1], D_[1]], lw=2.2, color=BLUE)
    ax.plot([A[0], Cc[0]], [A[1], Cc[1]], lw=2, color=ORANGE)
    ax.plot([B[0], D_[0]], [B[1], D_[1]], lw=2, color=ORANGE)
    tick_marks(ax, A, O, 1)
    tick_marks(ax, O, B, 1)
    tick_marks(ax, Cc, O, 2)
    tick_marks(ax, O, D_, 2)
    lab(ax, [(A, "A", (-16, -10)), (B, "B", (8, -4)), (Cc, "C", (-4, 8)), (D_, "D", (6, -14)),
             (O, "O", (8, 2))])
    finish(fig, ax, path, [A, B, Cc, D_], margin=0.9)


milieu_commun(X("triangles_4e_milieu_commun.png"))


def ssa(path):
    fig, ax = new_fig(8.4, 4.6)
    B, A = P(0, 0), P(6, 0)
    u = P(cos(radians(40)), sin(radians(40)))
    c1, c2 = 6.915 * u, 2.278 * u
    ax.plot([B[0], 8 * u[0]], [B[1], 8 * u[1]], lw=1.2, color=NEUTRAL, ls="--")
    tri(ax, A, B, c1, BLUE, LBLUE)
    tri(ax, A, B, c2, ORANGE, LORANGE)
    ax.add_patch(Arc(A, 9, 9, theta1=100, theta2=175, color=GREEN, lw=1.4, ls=":"))
    angle_arc(ax, B, A - B, u, r=0.8, color=DARK, label="40°", label_r=1.2, fs=12)
    seg_label(ax, B, A, "6 cm", side=-1, offset=0.38, fs=12)
    seg_label(ax, A, c1, "4,5", side=-1, offset=0.35, fs=11.5, color=BLUE)
    seg_label(ax, A, c2, "4,5", side=1, offset=0.35, fs=11.5, color=ORANGE)
    lab(ax, [(B, "B", (-16, -14)), (A, "A", (6, -14)), (c1, "C_1", (-6, 8)), (c2, "C_2", (-22, 4))])
    finish(fig, ax, path, [A, B, c1, P(0, -0.6)], margin=0.8)


ssa(X("triangles_4e_ssa.png"))


def riviere(path, solution=False):
    fig, ax = new_fig(8.6, 5.2)
    ax.fill_between([-1.5, 9.5], [0, 0], [-3.0, -3.0], color="#d6eafc", zorder=0)
    ax.text(8.8, -1.5, "rivière", fontsize=12, color=BLUE, ha="right", fontweight="bold")
    A, B = P(0, -3.0), P(0, 0)
    Cc, D_ = P(4, 0), P(8, 0)
    E_ = P(8, 3.0)
    ax.scatter([A[0]], [A[1]], s=160, marker="^", color=GREEN, zorder=6)
    ax.plot([B[0], D_[0]], [0, 0], lw=2, color=DARK)
    ax.plot([A[0], B[0]], [A[1], B[1]], lw=2, color=ORANGE, ls="--" if not solution else "-")
    ax.plot([A[0], E_[0]], [A[1], E_[1]], lw=1.6, color=BLUE)
    ax.plot([D_[0], E_[0]], [D_[1], E_[1]], lw=2, color=ORANGE)
    right_angle(ax, B, (1, 0), (0, -1), size=0.3)
    right_angle(ax, D_, (-1, 0), (0, 1), size=0.3)
    seg_label(ax, B, Cc, "40 m", side=1, offset=0.35, fs=11.5)
    seg_label(ax, Cc, D_, "40 m", side=1, offset=0.35, fs=11.5)
    seg_label(ax, D_, E_, "28 m" if solution else "?", side=1, offset=-0.5, fs=12, color=ORANGE,
              weight="bold")
    if solution:
        seg_label(ax, A, B, "28 m", side=-1, offset=0.5, fs=12, color=GREEN, weight="bold")
        tick_marks(ax, B, Cc, 1)
        tick_marks(ax, Cc, D_, 1)
    lab(ax, [(A, "A", (8, -6)), (B, "B", (-16, 6)), (Cc, "C", (-4, -18)), (D_, "D", (6, -16)),
             (E_, "E", (8, 2))])
    ax.text(0.2, -3.6, "arbre sur l'autre rive", fontsize=10.5, color=GREEN)
    finish(fig, ax, path, [A, B, D_, E_, P(-1, -3.8)], margin=0.7)


riviere(X("triangles_4e_riviere.png"))
riviere(X("triangles_4e_riviere_solution.png"), solution=True)


def equi_interieur(path):
    fig, ax = new_fig(6.4, 5.8)
    A, B = P(0, 0), P(6, 0)
    Cc = P(3, 3 * sqrt(3))
    D_ = A + (B - A) * 2 / 6
    E_ = B + (Cc - B) * 2 / 6
    F_ = Cc + (A - Cc) * 2 / 6
    tri(ax, A, B, Cc, BLUE, LBLUE)
    tri(ax, D_, E_, F_, ORANGE, LORANGE)
    for (S, T) in [(A, D_), (B, E_), (Cc, F_)]:
        tick_marks(ax, S, T, 1)
    for (S, T) in [(D_, B), (E_, Cc), (F_, A)]:
        tick_marks(ax, S, T, 2)
    lab(ax, [(A, "A", (-16, -14)), (B, "B", (6, -14)), (Cc, "C", (-4, 8)), (D_, "D", (-4, -18)),
             (E_, "E", (8, -2)), (F_, "F", (-18, 0))])
    finish(fig, ax, path, [A, B, Cc], margin=0.8)


equi_interieur(X("triangles_4e_equilateral.png"))


def rectangle_milieu(path):
    fig, ax = new_fig(7.6, 4.0)
    A, B, Cc, D_ = P(0, 0), P(8, 0), P(8, 3), P(0, 3)
    M = P(4, 0)
    ax.add_patch(Polygon([A, B, Cc, D_], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.2))
    ax.plot([D_[0], M[0], Cc[0]], [D_[1], M[1], Cc[1]], lw=2, color=ORANGE)
    right_angle(ax, A, (1, 0), (0, 1))
    right_angle(ax, B, (-1, 0), (0, 1))
    tick_marks(ax, A, M, 1)
    tick_marks(ax, M, B, 1)
    lab(ax, [(A, "A", (-16, -14)), (B, "B", (6, -14)), (Cc, "C", (6, 4)), (D_, "D", (-16, 4)),
             (M, "M", (-4, -18))])
    finish(fig, ax, path, [A, B, Cc, D_], margin=0.8)


rectangle_milieu(X("triangles_4e_rectangle.png"))


def losange(path):
    fig, ax = new_fig(6.4, 5.0)
    a = radians(35)
    A = P(0, 0)
    Cc = P(2 * 5 * cos(a), 0)
    B = P(5 * cos(a), -5 * sin(a))
    D_ = P(5 * cos(a), 5 * sin(a))
    O = (A + Cc) / 2
    ax.add_patch(Polygon([A, B, Cc, D_], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.2))
    ax.plot([A[0], Cc[0]], [A[1], Cc[1]], lw=1.8, color=ORANGE)
    ax.plot([B[0], D_[0]], [B[1], D_[1]], lw=1.8, color=ORANGE)
    for S, T in [(A, B), (B, Cc), (Cc, D_), (D_, A)]:
        tick_marks(ax, S, T, 1)
    lab(ax, [(A, "A", (-16, -4)), (B, "B", (-4, -18)), (Cc, "C", (8, -4)), (D_, "D", (-4, 8)),
             (O, "O", (6, 4))])
    finish(fig, ax, path, [A, B, Cc, D_], margin=0.8)


losange(X("triangles_4e_losange.png"))
