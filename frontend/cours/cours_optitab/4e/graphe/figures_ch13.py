# -*- coding: utf-8 -*-
"""Figures du chapitre 13 (théorème de Pythagore) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, finish, _save, dot_label, seg_label, right_angle, tick_marks, pave, graphe,
                   setup_repere, BLUE, ORANGE, GREEN, DARK, NEUTRAL, DIR_COURS, DIR_EXOS, _proj)
import numpy as np
from math import sqrt, radians, cos, sin, atan2
from matplotlib.patches import Polygon, Rectangle

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
P = lambda x, y: np.array([x, y], float)  # noqa: E731
LBLUE, LORANGE, LGREEN = "#d6eafc", "#fdebd0", "#e8f5e9"
inc = dict(color=ORANGE, fs=13, weight="bold")
lab_ = dict(color=DARK, fs=12.5)


def tri(ax, A, B, Cc, col=BLUE, fc=LBLUE):
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=fc, edgecolor=col, lw=2.2))


def lab(ax, pts):
    for Pt, n, off in pts:
        dot_label(ax, Pt, f"${n}$", *off, color=DARK, s=28)


def carres(path):
    fig, ax = new_fig(7.2, 7.0)
    A, B, Cc = P(0, 0), P(4, 0), P(0, 3)
    ax.add_patch(Polygon([A, B, B + P(0, -4), A + P(0, -4)], closed=True, facecolor=LBLUE,
                         edgecolor=BLUE, lw=1.8))
    ax.text(2, -2, "$AB^2 = 16$", ha="center", va="center", fontsize=13, color=BLUE, fontweight="bold")
    ax.add_patch(Polygon([A, Cc, Cc + P(-3, 0), A + P(-3, 0)], closed=True, facecolor=LBLUE,
                         edgecolor=BLUE, lw=1.8))
    ax.text(-1.5, 1.5, "$AC^2 = 9$", ha="center", va="center", fontsize=13, color=BLUE,
            fontweight="bold")
    n = P(3, 4) / 5
    P3, P4 = Cc + 5 * n, B + 5 * n
    ax.add_patch(Polygon([B, Cc, P3, P4], closed=True, facecolor=LORANGE, edgecolor=ORANGE, lw=1.8))
    ctr = (B + Cc + P3 + P4) / 4
    ax.text(ctr[0], ctr[1], "$BC^2 = 25$", ha="center", va="center", fontsize=14, color=ORANGE,
            fontweight="bold")
    ax.plot([A[0], B[0], Cc[0], A[0]], [A[1], B[1], Cc[1], A[1]], lw=2.6, color=DARK)
    right_angle(ax, A, (1, 0), (0, 1), size=0.32)
    lab(ax, [(A, "A", (-16, -16)), (B, "B", (6, -16)), (Cc, "C", (-16, 6))])
    ax.text(1.2, -5.0, "$9 + 16 = 25$  :  $AB^2 + AC^2 = BC^2$", fontsize=13, ha="center", color=GREEN,
            fontweight="bold")
    finish(fig, ax, path, [P(-3.3, -5.5), P(7.3, 7.2)], margin=0.2)


carres(C("pythagore_4e_carres.png"))


def triangle_rect(path, a_txt, b_txt, c_txt, names=("A", "B", "C"), wa=4.6, hb=3.4, hl=None):
    """Triangle rectangle en names[0] : [AB] horizontal (longueur wa), [AC] vertical (hb)."""
    fig, ax = new_fig(6.8, 4.8)
    A, B, Cc = P(0, 0), P(wa, 0), P(0, hb)
    tri(ax, A, B, Cc)
    right_angle(ax, A, (1, 0), (0, 1), size=0.3)
    if a_txt:
        seg_label(ax, A, B, a_txt[0], side=-1, offset=0.38, **a_txt[1])
    if b_txt:
        seg_label(ax, A, Cc, b_txt[0], side=1, offset=1.35, **b_txt[1])
    if c_txt:
        seg_label(ax, B, Cc, c_txt[0], side=-1, offset=0.85, **c_txt[1])
    lab(ax, [(A, names[0], (-16, -16)), (B, names[1], (6, -16)), (Cc, names[2], (-16, 6))])
    finish(fig, ax, path, [A, B, Cc], margin=1.0)


triangle_rect(C("pythagore_4e_vocabulaire.png"), ("côté de l'angle droit", lab_),
              ("côté de l'angle droit", lab_), ("hypoténuse", inc))
triangle_rect(X("pythagore_4e_9_12.png"), ("$AB = 9$ cm", lab_), ("$AC = 12$ cm", lab_),
              ("$BC = $ ?", inc), wa=4.5, hb=6.0)
triangle_rect(X("pythagore_4e_17_8.png"), ("$EF = $ ?", inc), ("$DE = 8$ cm", lab_),
              ("$DF = 17$ cm", lab_), names=("E", "F", "D"), wa=7.5, hb=4.0)
triangle_rect(X("pythagore_4e_5_7.png"), ("$GH = 7$ cm", lab_), ("$GK = 5$ cm", lab_),
              ("$HK = $ ?", inc), names=("G", "H", "K"), wa=5.6, hb=4.0)


def trois_triangles(path):
    fig, ax = new_fig(10.5, 3.8)
    # triangle 1 : rectangle en A
    A, B, Cc = P(0, 0), P(3, 0), P(0, 2.2)
    tri(ax, A, B, Cc)
    right_angle(ax, A, (1, 0), (0, 1), size=0.25)
    lab(ax, [(A, "A", (-16, -14)), (B, "B", (6, -14)), (Cc, "C", (-14, 4))])
    # triangle 2 : rectangle en F
    D_, E_, F_ = P(4.2, 0.2), P(7.0, 0.2), P(5.0, 1.9)
    v1, v2 = D_ - F_, E_ - F_
    # rendre F exactement droit : F sur le cercle de diamètre [DE]
    M = (D_ + E_) / 2
    rr = np.linalg.norm(E_ - D_) / 2
    F_ = M + rr * P(cos(radians(115)), sin(radians(115)))
    tri(ax, D_, E_, F_)
    right_angle(ax, F_, D_ - F_, E_ - F_, size=0.25)
    lab(ax, [(D_, "D", (-16, -14)), (E_, "E", (6, -14)), (F_, "F", (-4, 8))])
    # triangle 3 : rectangle en H, côtés 5 et 12 (échelle 0,2)
    H, G, K = P(8.4, 0), P(8.4, 1.0 * 2.2), P(8.4 + 2.4 * 1.1, 0)
    tri(ax, H, G, K)
    right_angle(ax, H, (1, 0), (0, 1), size=0.25)
    seg_label(ax, H, G, "5", side=1, offset=0.3, fs=12)
    seg_label(ax, H, K, "12", side=-1, offset=0.3, fs=12)
    lab(ax, [(H, "H", (-16, -14)), (G, "G", (-14, 4)), (K, "K", (6, -14))])
    ax.text(1.5, -0.7, "triangle ①", ha="center", fontsize=12, color=DARK, fontweight="bold")
    ax.text(5.6, -0.7, "triangle ②", ha="center", fontsize=12, color=DARK, fontweight="bold")
    ax.text(9.7, -0.7, "triangle ③", ha="center", fontsize=12, color=DARK, fontweight="bold")
    ax.set_xlim(-0.6, 11.6)
    ax.set_ylim(-1.1, 3.0)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


trois_triangles(X("pythagore_4e_trois_triangles.png"))


def echelle(path):
    fig, ax = new_fig(6.0, 6.0)
    ax.plot([-0.3, 2.6], [0, 0], lw=2.4, color=NEUTRAL)
    ax.add_patch(Rectangle((-0.5, 0), 0.5, 5.2, facecolor="#e0e0e0", edgecolor=NEUTRAL, lw=1.4))
    A, B, Cc = P(0, 0), P(1.2, 0), P(0, 4.34)
    ax.plot([B[0], Cc[0]], [B[1], Cc[1]], lw=4, color=ORANGE, solid_capstyle="round")
    for t in np.linspace(0.1, 0.9, 8):
        Q = B + t * (Cc - B)
        ax.plot([Q[0] - 0.12, Q[0] + 0.12], [Q[1] - 0.04, Q[1] + 0.04], lw=1.5, color="#a04000")
    right_angle(ax, A, (1, 0), (0, 1), size=0.25)
    lab(ax, [(A, "A", (-18, -16)), (B, "B", (6, -16)), (Cc, "C", (8, 2))])
    seg_label(ax, A, B, "1,2 m", side=-1, offset=0.35, fs=12)
    seg_label(ax, B, Cc, "échelle :\n4,5 m", side=-1, offset=1.0, fs=12, color=ORANGE)
    ax.text(-0.25, 2.2, "mur", rotation=90, ha="center", va="center", fontsize=11, color=DARK)
    finish(fig, ax, path, [P(-0.6, -0.4), P(2.8, 5.3)], margin=0.3)


echelle(X("pythagore_4e_echelle.png"))


def terrain(path, L=40, l=20, txt=("40 m", "20 m"), titre=None):
    fig, ax = new_fig(7.6, 4.4)
    ax.add_patch(Rectangle((0, 0), L, l, facecolor="#e8f5e9", edgecolor=GREEN, lw=2.2))
    ax.plot([0, L], [0, l], lw=2.2, color=ORANGE, ls="--")
    ax.plot([L / 2, L / 2], [0, l], lw=1.2, color=GREEN)
    right_angle(ax, (L, 0), (-1, 0), (0, 1), size=l * 0.08)
    ax.text(L / 2, -l * 0.08, txt[0], ha="center", va="top", fontsize=12.5, color=DARK)
    ax.text(L + L * 0.02, l / 2, txt[1], ha="left", va="center", fontsize=12.5, color=DARK)
    for Pt, n, off in [((0, 0), "A", (-16, -14)), ((L, 0), "B", (6, -14)), ((L, l), "C", (6, 4)),
                       ((0, l), "D", (-16, 4))]:
        dot_label(ax, Pt, f"${n}$", *off, color=DARK, s=28)
    ax.set_xlim(-L * 0.08, L * 1.14)
    ax.set_ylim(-l * 0.25, l * 1.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


terrain(X("pythagore_4e_terrain_hand.png"))
terrain(X("pythagore_4e_terrain_foot.png"), 105, 68, ("105 m", "68 m"))


def isocele(path, solution=False):
    fig, ax = new_fig(6.0, 5.2)
    B, Cc, A = P(0, 0), P(6, 0), P(3, 4)
    H = P(3, 0)
    tri(ax, A, B, Cc)
    ax.plot([A[0], H[0]], [A[1], H[1]], lw=2, color=ORANGE, ls="--" if not solution else "-")
    right_angle(ax, H, (1, 0), (0, 1), size=0.25)
    tick_marks(ax, A, B, 2)
    tick_marks(ax, A, Cc, 2)
    seg_label(ax, A, B, "10 cm", side=-1, offset=0.5, fs=12)
    seg_label(ax, B, Cc, "12 cm", side=-1, offset=0.75, fs=12)
    if solution:
        seg_label(ax, A, H, "8 cm", side=-1, offset=0.45, fs=12, color=GREEN, weight="bold")
        seg_label(ax, B, H, "6", side=1, offset=0.3, fs=11, color=GREEN)
    lab(ax, [(A, "A", (-4, 8)), (B, "B", (-16, -14)), (Cc, "C", (6, -14)), (H, "H", (-4, -18))])
    finish(fig, ax, path, [A, B, Cc], margin=0.9)


isocele(X("pythagore_4e_isocele.png"))
isocele(X("pythagore_4e_isocele_solution.png"), solution=True)


def quadrillage(path, solution=False):
    def extra(ax):
        pts = {"A": (1, 1), "B": (7, 1), "C": (7, 9), "D": (-2, 5)}
        ax.plot([1, 7, 7, 1], [1, 1, 9, 1], lw=2.2, color=BLUE)
        ax.plot([1, -2], [1, 5], lw=2.2, color=ORANGE)
        if solution:
            ax.plot([-2, 1, 1], [5, 5, 1], lw=1.6, color=GREEN, ls="--")
            ax.text(-0.5, 5.3, "3", color=GREEN, fontsize=12, fontweight="bold", ha="center")
            ax.text(1.3, 3.0, "4", color=GREEN, fontsize=12, fontweight="bold")
            ax.text(4.0, 0.4, "6", color=GREEN, fontsize=12, fontweight="bold", ha="center")
            ax.text(7.3, 5.0, "8", color=GREEN, fontsize=12, fontweight="bold")
        for n, (x, y) in pts.items():
            ax.scatter([x], [y], s=45, color=DARK, zorder=5)
            ax.annotate(f"${n}$", (x, y), textcoords="offset points", xytext=(6, 6), fontsize=13,
                        color=DARK, fontweight="bold")
    graphe(path, curves=[], extra=extra, xb=(-3.5, 9.5), yb=(-1, 10.5), xt=1, yt=1, w=7.4, h=6.4,
           equal=True)


quadrillage(X("pythagore_4e_quadrillage.png"))
quadrillage(X("pythagore_4e_quadrillage_solution.png"), solution=True)


def losange(path):
    fig, ax = new_fig(6.4, 5.0)
    A, B, Cc, D_ = P(-8, 0), P(0, -6), P(8, 0), P(0, 6)
    O = P(0, 0)
    ax.add_patch(Polygon([A, B, Cc, D_], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.2))
    ax.plot([A[0], Cc[0]], [0, 0], lw=1.8, color=ORANGE)
    ax.plot([0, 0], [B[1], D_[1]], lw=1.8, color=ORANGE)
    right_angle(ax, O, (1, 0), (0, 1), size=0.8)
    seg_label(ax, A, O, "8", side=1, offset=0.7, fs=12, color=ORANGE)
    seg_label(ax, O, D_, "6", side=-1, offset=0.7, fs=12, color=ORANGE)
    lab(ax, [(A, "A", (-16, -4)), (B, "B", (-4, -18)), (Cc, "C", (8, -4)), (D_, "D", (-4, 8)),
             (O, "O", (6, -16))])
    finish(fig, ax, path, [A, B, Cc, D_], margin=1.5)


losange(X("pythagore_4e_losange.png"))


def corde(path):
    fig, ax = new_fig(6.4, 5.4)
    A, B, Cc = P(0, 0), P(4, 0), P(0, 3)
    pts = [A + (B - A) * k / 4 for k in range(4)] + [B + (Cc - B) * k / 5 for k in range(5)] + \
          [Cc + (A - Cc) * k / 3 for k in range(3)]
    ax.plot([A[0], B[0], Cc[0], A[0]], [A[1], B[1], Cc[1], A[1]], lw=3, color="#a0522d")
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=70, color=DARK, zorder=5)
    right_angle(ax, A, (1, 0), (0, 1), size=0.3, color=GREEN, lw=2)
    ax.text(2, -0.45, "4 intervalles", ha="center", va="top", fontsize=12, color=DARK)
    ax.text(-0.35, 1.5, "3", ha="right", va="center", fontsize=12, color=DARK)
    ax.text(2.3, 1.85, "5 intervalles", ha="left", fontsize=12, color=DARK)
    ax.text(2, 3.5, "corde à 13 nœuds (12 intervalles égaux)", ha="center", fontsize=12, color=DARK,
            fontweight="bold")
    ax.set_xlim(-1.0, 5.0)
    ax.set_ylim(-1.0, 3.9)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


corde(X("pythagore_4e_corde.png"))


def toboggan(path):
    fig, ax = new_fig(8.6, 4.6)
    ax.plot([-0.5, 8.4], [0, 0], lw=2.4, color=NEUTRAL)
    T = P(0, 2.4)
    ax.add_patch(Rectangle((-0.6, 0), 0.6, 2.4, facecolor="#e0e0e0", edgecolor=NEUTRAL, lw=1.4))
    ax.plot([0, 3.2], [2.4, 0], lw=4, color=ORANGE, solid_capstyle="round")
    ax.plot([0, 4.5], [2.4, 0], lw=3, color=BLUE, ls="--")
    right_angle(ax, P(0, 0), (1, 0), (0, 1), size=0.22)
    ax.text(-0.75, 1.2, "2,4 m", ha="right", va="center", fontsize=12, color=DARK)
    ax.text(1.6, -0.25, "3,2 m", ha="center", va="top", fontsize=12, color=ORANGE, fontweight="bold")
    ax.text(3.2, -0.75, "4,5 m", ha="center", va="top", fontsize=12, color=BLUE, fontweight="bold")
    ax.annotate("", xy=(4.5, -0.55), xytext=(0, -0.55), arrowprops=dict(arrowstyle="<->", color=BLUE))
    ax.text(1.9, 1.6, "toboggan A", fontsize=12, color=ORANGE, fontweight="bold", rotation=-37)
    ax.text(3.0, 0.95, "toboggan B", fontsize=12, color=BLUE, fontweight="bold", rotation=-28)
    ax.set_xlim(-1.6, 5.3)
    ax.set_ylim(-1.2, 2.9)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


toboggan(X("pythagore_4e_toboggan.png"))


def tente(path):
    fig, ax = new_fig(6.4, 4.4)
    A, B, S = P(0, 0), P(1.8, 0), P(0.9, 1.2)
    H = P(0.9, 0)
    tri(ax, A, B, S, ORANGE, LORANGE)
    ax.plot([S[0], H[0]], [S[1], H[1]], lw=1.8, color=BLUE, ls="--")
    right_angle(ax, H, (1, 0), (0, 1), size=0.08)
    seg_label(ax, A, S, "1,5 m", side=1, offset=0.15, fs=12)
    seg_label(ax, S, B, "1,5 m", side=1, offset=0.15, fs=12)
    seg_label(ax, A, B, "1,8 m", side=-1, offset=0.24, fs=12)
    ax.text(0.95, 0.5, "hauteur ?", fontsize=12, color=BLUE, fontweight="bold")
    lab(ax, [(A, "A", (-16, -14)), (B, "B", (6, -14)), (S, "S", (-4, 8)), (H, "H", (6, -16))])
    finish(fig, ax, path, [A, B, S], margin=0.35)


tente(X("pythagore_4e_tente.png"))


def boite(path, solution=False):
    def extra(ax, V):
        if solution:
            ax.plot([V["A"][0], V["C"][0]], [V["A"][1], V["C"][1]], lw=2, color=GREEN, ls="--")
    pave(path, L=6.0, P=4.0, H=2.4, noms="ABCDEFGH",
         measures=[("AB", "30 cm"), ("BF", "20 cm", dict(side=-1, offset=0.5)),
                   ("BC", "12 cm", dict(side=-1, offset=0.5))],
         diagonales=[("A", "G", ORANGE)] + ([("A", "F", GREEN)] if solution else []), w=7.6, h=5.0)


boite(X("pythagore_4e_boite.png"))
boite(X("pythagore_4e_boite_solution.png"), solution=True)


def spirale(path):
    fig, ax = new_fig(7.0, 7.0)
    O = P(0, 0)
    Pk = P(1, 0)
    pts = [Pk]
    ax.plot([0, 1], [0, 0], lw=2, color=BLUE)
    for n in range(1, 16):
        u = Pk / np.linalg.norm(Pk)
        nrm = P(-u[1], u[0])
        Q = Pk + nrm
        ax.add_patch(Polygon([O, Pk, Q], closed=True, facecolor=LBLUE if n % 2 else "#eaf3fb",
                             edgecolor=BLUE, lw=1.4))
        right_angle(ax, Pk, -u, nrm, size=0.12, lw=1)
        if n <= 4 or n == 15:
            mid = Q * 0.78
            txt = f"$\\sqrt{{{n + 1}}}$" if n + 1 not in (4, 9, 16) else f"${int(sqrt(n + 1))}$"
            ax.text(mid[0], mid[1], txt, fontsize=12, color=ORANGE, fontweight="bold", ha="center",
                    va="center", bbox=dict(fc="white", ec="none", pad=0.5))
        Pk = Q
        pts.append(Q)
    ax.scatter([0], [0], s=40, color=DARK, zorder=5)
    ax.annotate("$O$", (0, 0), textcoords="offset points", xytext=(-14, -12), fontsize=13, color=DARK)
    ax.text(0.5, -0.25, "1", ha="center", va="top", fontsize=12, color=DARK)
    allp = np.vstack(pts + [O])
    ax.set_xlim(allp[:, 0].min() - 0.5, allp[:, 0].max() + 0.5)
    ax.set_ylim(allp[:, 1].min() - 0.5, allp[:, 1].max() + 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


spirale(X("pythagore_4e_spirale.png"))


def voilier(path, solution=False):
    fig, ax = new_fig(6.6, 6.6)
    Pp, N, E2, F_ = P(0, 0), P(0, 15), P(8, 15), P(8, 6)
    ax.plot([0, 0, 8, 8], [0, 15, 15, 6], lw=2.4, color=BLUE)
    for a, b in [(Pp, N), (N, E2), (E2, F_)]:
        m = (a + b) / 2
        d = (b - a) / np.linalg.norm(b - a)
        ax.annotate("", xy=m + 0.6 * d, xytext=m - 0.6 * d, arrowprops=dict(arrowstyle="-|>", color=BLUE,
                                                                              lw=2))
    seg_label(ax, Pp, N, "15 km", side=1, offset=0.9, fs=12)
    seg_label(ax, N, E2, "8 km", side=1, offset=0.7, fs=12)
    seg_label(ax, E2, F_, "9 km", side=-1, offset=0.9, fs=12)
    right_angle(ax, N, (0, -1), (1, 0), size=0.6)
    right_angle(ax, E2, (-1, 0), (0, -1), size=0.6)
    if solution:
        ax.plot([0, 8], [0, 15], lw=1.8, color=ORANGE, ls="--")
        ax.plot([0, 8], [0, 6], lw=2.2, color=GREEN)
        ax.plot([0, 8], [6, 6], lw=1.2, color=GREEN, ls=":")
        seg_label(ax, Pp, E2, "17 km", side=-1, offset=0.9, fs=12, color=ORANGE, weight="bold")
        seg_label(ax, Pp, F_, "10 km", side=-1, offset=0.8, fs=12, color=GREEN, weight="bold")
    ax.annotate("", xy=(-3, 13.5), xytext=(-3, 11), arrowprops=dict(arrowstyle="-|>", color=DARK, lw=1.6))
    ax.text(-3, 13.9, "N", ha="center", fontsize=13, color=DARK, fontweight="bold")
    lab_pts = [(Pp, "P", (-16, -10)), (N, "N", (-16, 4)), (E2, "E", (6, 4)), (F_, "F", (8, -6))]
    lab(ax, lab_pts)
    ax.text(0.5, -1.4, "port", fontsize=11, color=DARK)
    finish(fig, ax, path, [P(-3.6, -1.8), P(10, 16)], margin=0.3)


voilier(X("pythagore_4e_voilier.png"))
voilier(X("pythagore_4e_voilier_solution.png"), solution=True)


def ecran(path):
    fig, ax = new_fig(7.6, 4.8)
    W, H = 12.18, 6.85
    ax.add_patch(Rectangle((0, 0), W, H, facecolor="#2c3e50", edgecolor=DARK, lw=3))
    ax.add_patch(Rectangle((0.15, 0.15), W - 0.3, H - 0.3, facecolor="#5d8fb8", edgecolor="none"))
    ax.plot([0, W], [0, H], lw=2.2, color=ORANGE, ls="--")
    ax.text(W / 2 + 0.3, H / 2 + 0.2, "diagonale : 55 pouces", color="white", fontsize=12,
            fontweight="bold", rotation=29, ha="center")
    ax.text(W / 2, -0.4, "largeur $= 16k$", ha="center", va="top", fontsize=12.5, color=DARK)
    ax.text(W + 0.3, H / 2, "hauteur $= 9k$", ha="left", va="center", fontsize=12.5, color=DARK)
    ax.set_xlim(-0.4, W + 3.6)
    ax.set_ylim(-1.3, H + 0.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


ecran(X("pythagore_4e_ecran.png"))
