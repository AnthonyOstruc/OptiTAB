# -*- coding: utf-8 -*-
"""Figures du chapitre 'Théorème de Thalès et triangles semblables' (3ème) pour le site OptiTAB.

Style aligné sur les figures matplotlib existantes du site (cf. frontend/cours/cours_optitab/base/graphe/Thales2.py) :
- pas d'axes, pas de titre, aspect égal, 2 couleurs principales max ;
- grand triangle bleu, petit triangle / éléments mis en évidence en orange ;
- marques // neutres pour le parallélisme, réponses en vert dans les figures de correction.
"""
import os
from math import radians, cos, sin

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc

BLUE = "#3498db"
ORANGE = "#e67e22"
GREEN = "#2e7d32"
RED = "#c0392b"
DARK = "#2c3e50"
NEUTRAL = "0.25"

ROOT = r"c:/Users/SWEELCO-AT/Desktop/SWINDER/OptiTABV2/frontend"
DIR_COURS = os.path.join(ROOT, "cours/cours_optitab/3e/images")
DIR_EXOS = os.path.join(ROOT, "exercices/3e/images")
os.makedirs(DIR_COURS, exist_ok=True)
os.makedirs(DIR_EXOS, exist_ok=True)


def new_fig(w=8.2, h=5.2):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    return fig, ax


def finish(fig, ax, path, pts, margin=1.15):
    pts = np.vstack(pts)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(pts[:, 0].min() - margin, pts[:, 0].max() + margin)
    ax.set_ylim(pts[:, 1].min() - margin, pts[:, 1].max() + margin)
    ax.axis("off")
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


def add_parallel_marks(ax, P, Q, n=2, size=0.24, spacing=0.3, color=NEUTRAL, lw=2.2):
    """n marques // (petits traits obliques) au milieu du segment PQ."""
    P = np.array(P, float)
    Q = np.array(Q, float)
    v = Q - P
    L = np.linalg.norm(v)
    if L == 0:
        return
    u = v / L
    # Trait incliné à ~60° par rapport au segment pour un rendu « chevron »
    ang = np.deg2rad(60)
    d = np.array([u[0] * cos(ang) - u[1] * sin(ang), u[0] * sin(ang) + u[1] * cos(ang)])
    mid = (P + Q) / 2
    total = spacing * (n - 1)
    ts = [0.0] if n == 1 else np.linspace(-total / 2, total / 2, n)
    for t in ts:
        c = mid + t * u
        a = c - (size / 2) * d
        b = c + (size / 2) * d
        ax.plot([a[0], b[0]], [a[1], b[1]], lw=lw, color=color, solid_capstyle="round")


def seg_label(ax, P, Q, text, side=1, offset=0.42, t=0.5, color=DARK, fs=12.5, weight="normal"):
    """Étiquette au point P + t*(Q-P), décalée perpendiculairement (side = +1 / -1)."""
    P = np.array(P, float)
    Q = np.array(Q, float)
    u = Q - P
    L = np.linalg.norm(u)
    u = u / L
    nrm = np.array([-u[1], u[0]]) * side
    pos = P + t * (Q - P) + offset * nrm
    ax.text(pos[0], pos[1], text, color=color, fontsize=fs, ha="center", va="center",
            fontweight=weight)


def dot_label(ax, P, name, dx, dy, color="0.1", s=70, fs=13):
    ax.scatter([P[0]], [P[1]], s=s, zorder=5, color=color)
    ax.annotate(name, (P[0], P[1]), textcoords="offset points", xytext=(dx, dy),
                fontsize=fs, color=DARK, fontweight="bold")


def right_angle(ax, corner, d1, d2, size=0.35, color=NEUTRAL):
    """Petit carré d'angle droit au point corner, directions unitaires d1 et d2."""
    corner = np.array(corner, float)
    d1 = np.array(d1, float) / np.linalg.norm(d1)
    d2 = np.array(d2, float) / np.linalg.norm(d2)
    p1 = corner + size * d1
    p2 = corner + size * (d1 + d2)
    p3 = corner + size * d2
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], lw=1.4, color=color)


# ---------------------------------------------------------------- configurations Thalès

def thales_points(AB=6.0, AC=5.0, theta=55.0, kM=0.6, kN=None, papillon=False):
    """Renvoie A, B, C, M, N. kM = AM/AB, kN = AN/AC (kN = kM si None => (MN)//(BC))."""
    A = np.array([0.0, 0.0])
    B = np.array([AB, 0.0])
    C = A + AC * np.array([cos(radians(theta)), sin(radians(theta))])
    if kN is None:
        kN = kM
    sgn = -1.0 if papillon else 1.0
    M = A + sgn * kM * (B - A)
    N = A + sgn * kN * (C - A)
    return A, B, C, M, N


def draw_thales(path, kM=0.6, kN=None, papillon=False, AB=6.0, AC=5.0, theta=55.0,
                labels=None, marks=True, mn_style="-", small_highlight=True,
                extra=None, w=8.2, h=5.2, label_MN_names=("M", "N")):
    """Figure générique de configuration de Thalès.

    labels : liste de tuples (seg, texte, kwargs) avec seg parmi
             'AM','MB','AB','AN','NC','AC','MN','BC'.
    extra  : fonction(ax, pts) pour annotations supplémentaires.
    """
    A, B, C, M, N = thales_points(AB, AC, theta, kM, kN, papillon)
    fig, ax = new_fig(w, h)

    # Grand triangle ABC (bleu)
    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], lw=2.2, color=BLUE, zorder=2)
    # Droites (AM) et (AN) prolongées côté papillon
    if papillon:
        ax.plot([M[0], B[0]], [M[1], B[1]], lw=1.6, color=BLUE, zorder=1)
        ax.plot([N[0], C[0]], [N[1], C[1]], lw=1.6, color=BLUE, zorder=1)
    # Petit triangle AMN (orange)
    if small_highlight:
        lw_s = 3.0
        ax.plot([A[0], M[0]], [A[1], M[1]], lw=lw_s, color=ORANGE, zorder=3)
        ax.plot([A[0], N[0]], [A[1], N[1]], lw=lw_s, color=ORANGE, zorder=3)
        ax.plot([M[0], N[0]], [M[1], N[1]], lw=lw_s, color=ORANGE, zorder=3,
                linestyle=mn_style)
    else:
        ax.plot([M[0], N[0]], [M[1], N[1]], lw=2.4, color=ORANGE, zorder=3, linestyle=mn_style)

    if marks:
        add_parallel_marks(ax, B, C)
        add_parallel_marks(ax, M, N)

    # Points et noms
    dot_label(ax, A, "$A$", -20, -6 if papillon else -18, color="0.1", s=90)
    dot_label(ax, B, "$B$", 10, -18, color=BLUE)
    dot_label(ax, C, "$C$", 8, 4, color=BLUE)
    nm, nn = label_MN_names
    if papillon:
        dot_label(ax, M, f"${nm}$", -16, -18, color=ORANGE)
        dot_label(ax, N, f"${nn}$", -18, 4, color=ORANGE)
    else:
        dot_label(ax, M, f"${nm}$", 2, -20, color=ORANGE)
        dot_label(ax, N, f"${nn}$", -20, 6, color=ORANGE)

    seg_points = {"A": A, "B": B, "C": C, "M": M, "N": N}
    if labels:
        for seg, text, kw in labels:
            P, Q = seg_points[seg[0]], seg_points[seg[1]]
            seg_label(ax, P, Q, text, **kw)

    pts = [A, B, C, M, N]
    if extra:
        extra(ax, {"A": A, "B": B, "C": C, "M": M, "N": N, "pts": pts})
    finish(fig, ax, path, pts)


# ============================================================ FIGURES DU COURS

# 1. Configuration emboîtée (générique)
draw_thales(
    os.path.join(DIR_COURS, "thales_3e_config_emboitee.png"),
    kM=0.58,
    labels=[
        ("AB", "$M$ est sur $[AB]$,  $N$ est sur $[AC]$", dict(side=-1, offset=0.72, t=0.5, color=DARK, fs=11.5)),
        ("MN", "$(MN)\\,/\\!/\\,(BC)$", dict(side=-1, offset=0.95, t=0.62, color=ORANGE, fs=12.5, weight="bold")),
    ],
)

# 2. Configuration papillon (générique)
draw_thales(
    os.path.join(DIR_COURS, "thales_3e_config_papillon.png"),
    kM=0.58, papillon=True, AB=5.4, AC=4.6,
    labels=[
        ("MN", "$(MN)\\,/\\!/\\,(BC)$", dict(side=-1, offset=1.0, t=0.4, color=ORANGE, fs=12.5, weight="bold")),
    ],
)

# 3. Réciproque : rapports égaux -> parallèles (conclusion en vert)
def extra_reciproque(ax, p):
    M, N, B, C = p["M"], p["N"], p["B"], p["C"]
    add_parallel_marks(ax, M, N, color=GREEN)
    add_parallel_marks(ax, B, C, color=GREEN)
    mid = (M + N) / 2
    ax.text(mid[0] + 1.7, mid[1] + 1.15, "$(MN)\\,/\\!/\\,(BC)$", color=GREEN,
            fontsize=13.5, ha="center", fontweight="bold")

draw_thales(
    os.path.join(DIR_COURS, "thales_3e_reciproque.png"),
    kM=0.4, AB=7.0, AC=5.6, marks=False,
    labels=[
        ("AM", "$AM = 4$", dict(side=-1, offset=0.4, color=DARK, fs=12)),
        ("AB", "$AB = 10$", dict(side=-1, offset=1.0, t=0.62, color=DARK, fs=12)),
        ("AN", "$AN = 6$", dict(side=1, offset=0.42, color=DARK, fs=12)),
        ("AC", "$AC = 15$", dict(side=1, offset=1.05, t=0.62, color=DARK, fs=12)),
    ],
    extra=extra_reciproque,
)

# 4. Triangles semblables (angles marqués)
def fig_semblables():
    fig, ax = new_fig(9.0, 4.8)
    A = np.array([0.0, 0.0]); B = np.array([3.0, 0.0]); C = np.array([2.1, 1.9])
    k = 1.6
    D = np.array([4.6, 0.0]); E = D + k * (B - A); F = D + k * (C - A)

    for (P, Q, R), col, lw in [((A, B, C), ORANGE, 2.6), ((D, E, F), BLUE, 2.4)]:
        ax.plot([P[0], Q[0], R[0], P[0]], [P[1], Q[1], R[1], P[1]], lw=lw, color=col)

    def angle_arc(P, v1, v2, radii, color):
        a1 = np.degrees(np.arctan2(v1[1], v1[0]))
        a2 = np.degrees(np.arctan2(v2[1], v2[0]))
        if a2 < a1:
            a1, a2 = a2, a1
        if a2 - a1 > 180:
            a1, a2 = a2, a1 + 360
        for r in radii:
            ax.add_patch(Arc(P, 2 * r, 2 * r, angle=0, theta1=a1, theta2=a2, lw=1.8, color=color))

    for (P, Q, R), scale in [((A, B, C), 1.0), ((D, E, F), 1.0)]:
        angle_arc(P, Q - P, R - P, [0.45 * scale], RED)                       # angle en A / D
        angle_arc(Q, P - Q, R - Q, [0.4 * scale, 0.52 * scale], GREEN)        # angle en B / E
        angle_arc(R, P - R, Q - R, [0.38 * scale, 0.5 * scale, 0.62 * scale], BLUE)  # angle en C / F

    for P, s, dx, dy, col in [(A, "$A$", -16, -16, ORANGE), (B, "$B$", 8, -16, ORANGE),
                              (C, "$C$", 2, 10, ORANGE), (D, "$D$", -16, -16, BLUE),
                              (E, "$E$", 8, -16, BLUE), (F, "$F$", 2, 10, BLUE)]:
        dot_label(ax, P, s, dx, dy, color=col, s=60)

    ax.annotate("", xy=(4.35, 1.45), xytext=(3.15, 1.45),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=NEUTRAL))
    ax.text(3.75, 1.72, "$\\times\\,k$", color=DARK, fontsize=14, ha="center", fontweight="bold")
    finish(fig, ax, os.path.join(DIR_COURS, "thales_3e_triangles_semblables.png"),
           [A, B, C, D, E, F])

fig_semblables()

# 5. Ombres (bâton / arbre, rayons parallèles) — sert au cours ET à l'exercice 8
def fig_ombre(path, solution=False, bh=1.5, bs=2.0, th=9.0, ts=12.0,
              lab_bh="1,5 m", lab_bs="2 m", lab_ts="12 m", lab_sol="$h = 9$ m"):
    fig, ax = new_fig(9.6, 5.0)
    # Sol
    ax.plot([-0.8, 20.2], [0, 0], lw=2.2, color=NEUTRAL)
    # Bâton : base x=4, ombre vers la gauche
    bx = 4.0
    ax.plot([bx, bx], [0, bh], lw=4.5, color=ORANGE, solid_capstyle="round")
    ax.plot([bx - bs, bx], [0.02, 0.02], lw=5.5, color="0.6", solid_capstyle="butt")
    ax.plot([bx - bs, bx], [bh * 0, bh * 0], lw=0, color="0.6")
    # Rayon du soleil : du sommet du bâton au bout de l'ombre
    ax.plot([bx, bx - bs], [bh, 0], lw=1.6, color="#f1c40f", linestyle="--")
    # Arbre : base x=18, ombre vers la gauche
    tx = 18.0
    ax.plot([tx, tx], [0, th * 0.82], lw=7, color="#8d6e63", solid_capstyle="round")
    foliage = plt.Circle((tx, th * 0.86), th * 0.16, color="#66bb6a", zorder=3)
    ax.add_patch(foliage)
    ax.plot([tx - ts, tx], [0.02, 0.02], lw=5.5, color="0.6", solid_capstyle="butt")
    ax.plot([tx, tx - ts], [th, 0], lw=1.6, color="#f1c40f", linestyle="--")
    # Soleil
    sun = plt.Circle((19.6, 10.6), 0.55, color="#f1c40f", zorder=3)
    ax.add_patch(sun)
    # Angles droits au sol
    right_angle(ax, (bx, 0), (-1, 0), (0, 1), size=0.3)
    right_angle(ax, (tx, 0), (-1, 0), (0, 1), size=0.45)
    # Mesures
    ax.text(bx + 0.35, bh / 2, lab_bh, color=DARK, fontsize=12.5, va="center")
    ax.text(bx - bs / 2, -0.75, lab_bs, color=DARK, fontsize=12.5, ha="center")
    ax.text(tx - ts / 2, -0.75, lab_ts, color=DARK, fontsize=12.5, ha="center")
    if solution:
        ax.text(tx + 0.5, th / 2, lab_sol, color=GREEN, fontsize=14, va="center",
                fontweight="bold")
    else:
        ax.text(tx + 0.5, th / 2, "$h = $ ?", color=ORANGE, fontsize=14, va="center",
                fontweight="bold")
    ax.text(10.5, th * 0.62, "rayons du soleil\nparallèles", color="#b7950b", fontsize=11,
            ha="center", style="italic")
    pts = [np.array([-0.8, -1.2]), np.array([20.2, max(th + 2.2, 11.2)])]
    finish(fig, ax, path, pts, margin=0.4)

# Version du cours : bâton 1 m / ombre 1,5 m ; arbre ombre 9 m (h = 6 m)
fig_ombre(os.path.join(DIR_COURS, "thales_3e_ombre.png"),
          bh=1.0, bs=1.5, th=6.0, ts=9.0, lab_bh="1 m", lab_bs="1,5 m", lab_ts="9 m")

# ============================================================ FIGURES DES EXERCICES

EX = DIR_EXOS

# Ex 1 — écrire les rapports (générique, parallélisme donné)
draw_thales(os.path.join(EX, "thales_3e_ex01.png"), kM=0.55)

# Ex 2 — AM=3, AB=5, AC=10 -> AN ?
draw_thales(
    os.path.join(EX, "thales_3e_ex02.png"), kM=0.6, AB=6.0, AC=5.2,
    labels=[
        ("AM", "$AM = 3$ cm", dict(side=-1, offset=0.42, color=DARK, fs=12)),
        ("AB", "$AB = 5$ cm", dict(side=-1, offset=1.05, t=0.6, color=DARK, fs=12)),
        ("AC", "$AC = 10$ cm", dict(side=1, offset=1.2, t=0.8, color=DARK, fs=12)),
        ("AN", "$AN = $ ?", dict(side=1, offset=0.55, color=ORANGE, fs=13, weight="bold")),
    ],
)

# Ex 3 — AM=4, AB=10, BC=15 -> MN ?
draw_thales(
    os.path.join(EX, "thales_3e_ex03.png"), kM=0.4, AB=7.0, AC=5.6,
    labels=[
        ("AM", "$AM = 4$ cm", dict(side=-1, offset=0.42, color=DARK, fs=12)),
        ("AB", "$AB = 10$ cm", dict(side=-1, offset=1.05, t=0.62, color=DARK, fs=12)),
        ("BC", "$BC = 15$ cm", dict(side=-1, offset=0.5, color=DARK, fs=12)),
        ("MN", "$MN = $ ?", dict(side=1, offset=0.48, color=ORANGE, fs=13, weight="bold")),
    ],
)

# Ex 4 — AM=3, MB=2, AC=12 -> AN ?  (+ correction : AB=5, AN=7,2)
def labels_ex4(solution):
    lab = [
        ("AM", "$AM = 3$ cm", dict(side=-1, offset=0.42, color=DARK, fs=12)),
        ("MB", "$MB = 2$ cm", dict(side=-1, offset=0.42, color=DARK, fs=12)),
        ("AC", "$AC = 12$ cm", dict(side=1, offset=1.2, t=0.8, color=DARK, fs=12)),
    ]
    if solution:
        lab += [
            ("AB", "$AB = 3 + 2 = 5$ cm", dict(side=-1, offset=1.15, t=0.55, color=GREEN, fs=12.5, weight="bold")),
            ("AN", "$AN = 7{,}2$ cm", dict(side=1, offset=0.6, color=GREEN, fs=13, weight="bold")),
        ]
    else:
        lab += [("AN", "$AN = $ ?", dict(side=1, offset=0.55, color=ORANGE, fs=13, weight="bold"))]
    return lab

for sol, name in [(False, "thales_3e_ex04.png"), (True, "thales_3e_ex04_solution.png")]:
    draw_thales(os.path.join(EX, name), kM=0.6, AB=6.0, AC=5.2, labels=labels_ex4(sol))

# Ex 5 — réciproque : AM=4, AB=10, AN=6, AC=15 -> parallèles ? (+ correction verte)
def labels_ex5():
    return [
        ("AM", "$AM = 4$", dict(side=-1, offset=0.42, color=DARK, fs=12)),
        ("AB", "$AB = 10$", dict(side=-1, offset=1.05, t=0.62, color=DARK, fs=12)),
        ("AN", "$AN = 6$", dict(side=1, offset=0.42, color=DARK, fs=12)),
        ("AC", "$AC = 15$", dict(side=1, offset=1.05, t=0.62, color=DARK, fs=12)),
    ]

draw_thales(
    os.path.join(EX, "thales_3e_ex05.png"), kM=0.4, AB=7.0, AC=5.6, marks=False,
    mn_style="--",
    labels=labels_ex5() + [("MN", "parallèles ?", dict(side=1, offset=0.5, color=ORANGE, fs=12.5, weight="bold"))],
)
draw_thales(
    os.path.join(EX, "thales_3e_ex05_solution.png"), kM=0.4, AB=7.0, AC=5.6, marks=False,
    labels=labels_ex5(),
    extra=extra_reciproque,
)

# Ex 6 — non parallèles : AM=3, AB=8, AN=5, AC=12
def labels_ex6():
    return [
        ("AM", "$AM = 3$", dict(side=-1, offset=0.42, color=DARK, fs=12)),
        ("AB", "$AB = 8$", dict(side=-1, offset=1.05, t=0.65, color=DARK, fs=12)),
        ("AN", "$AN = 5$", dict(side=1, offset=0.42, t=0.45, color=DARK, fs=12)),
        ("AC", "$AC = 12$", dict(side=1, offset=1.05, t=0.68, color=DARK, fs=12)),
    ]

def extra_ex6_sol(ax, p):
    M, N = p["M"], p["N"]
    mid = (M + N) / 2
    ax.text(mid[0] - 0.25, mid[1] + 0.8,
            "$3\\times12 = 36 \\neq 40 = 5\\times8$",
            color=RED, fontsize=12.5, ha="center", fontweight="bold")
    ax.text(mid[0] - 0.25, mid[1] + 1.45, "$(MN)$ et $(BC)$ non parallèles",
            color=RED, fontsize=12.5, ha="center", fontweight="bold")

draw_thales(
    os.path.join(EX, "thales_3e_ex06.png"), kM=0.375, kN=5 / 12, AB=7.2, AC=5.8,
    marks=False, mn_style="--",
    labels=labels_ex6() + [("MN", "parallèles ?", dict(side=1, offset=0.5, t=0.45, color=ORANGE, fs=12.5, weight="bold"))],
)
draw_thales(
    os.path.join(EX, "thales_3e_ex06_solution.png"), kM=0.375, kN=5 / 12, AB=7.2, AC=5.8,
    marks=False, mn_style="--", labels=labels_ex6(), extra=extra_ex6_sol,
)

# Ex 7 — papillon : AM=3, AB=5, AC=8 -> AN ? (+ correction AN=4,8)
def labels_ex7(solution):
    lab = [
        ("AM", "$AM = 3$ cm", dict(side=-1, offset=0.5, color=DARK, fs=12)),
        ("AB", "$AB = 5$ cm", dict(side=1, offset=0.5, t=0.55, color=DARK, fs=12)),
        ("AC", "$AC = 8$ cm", dict(side=-1, offset=0.55, t=0.6, color=DARK, fs=12)),
    ]
    if solution:
        lab += [("AN", "$AN = 4{,}8$ cm", dict(side=-1, offset=1.0, t=0.6, color=GREEN, fs=13, weight="bold"))]
    else:
        lab += [("AN", "$AN = $ ?", dict(side=-1, offset=0.9, t=0.6, color=ORANGE, fs=13, weight="bold"))]
    return lab

for sol, name in [(False, "thales_3e_ex07.png"), (True, "thales_3e_ex07_solution.png")]:
    draw_thales(os.path.join(EX, name), kM=0.6, papillon=True, AB=5.4, AC=4.6,
                labels=labels_ex7(sol))

# Ex 8 — ombre de l'arbre (énoncé + correction)
fig_ombre(os.path.join(EX, "thales_3e_ex08.png"))
fig_ombre(os.path.join(EX, "thales_3e_ex08_solution.png"), solution=True)

# Ex 9 — équation : AM=4, MB=x, AN=6, NC=3 (+ correction x=2)
def labels_ex9(solution):
    lab = [
        ("AM", "$AM = 4$ cm", dict(side=-1, offset=0.42, color=DARK, fs=12)),
        ("AN", "$AN = 6$ cm", dict(side=1, offset=0.42, color=DARK, fs=12)),
        ("NC", "$NC = 3$ cm", dict(side=1, offset=0.42, color=DARK, fs=12)),
    ]
    if solution:
        lab += [("MB", "$x = 2$ cm", dict(side=-1, offset=0.42, color=GREEN, fs=13, weight="bold"))]
    else:
        lab += [("MB", "$MB = x$", dict(side=-1, offset=0.42, color=ORANGE, fs=13, weight="bold"))]
    return lab

for sol, name in [(False, "thales_3e_ex09.png"), (True, "thales_3e_ex09_solution.png")]:
    draw_thales(os.path.join(EX, name), kM=2 / 3, AB=6.6, AC=5.4, labels=labels_ex9(sol))

# Ex 10 — contrôle critique : AM=3, AB=8, AC=16 -> NC ? (+ correction AN=6, NC=10)
def labels_ex10(solution):
    lab = [
        ("AM", "$AM = 3$ cm", dict(side=-1, offset=0.42, color=DARK, fs=12)),
        ("AB", "$AB = 8$ cm", dict(side=-1, offset=1.05, t=0.62, color=DARK, fs=12)),
        ("AC", "$AC = 16$ cm", dict(side=1, offset=1.05, t=0.62, color=DARK, fs=12)),
    ]
    if solution:
        lab += [
            ("AN", "$AN = 6$ cm", dict(side=1, offset=0.42, color=GREEN, fs=12.5, weight="bold")),
            ("NC", "$NC = 10$ cm", dict(side=1, offset=0.42, color=GREEN, fs=12.5, weight="bold")),
        ]
    else:
        lab += [("NC", "$NC = $ ?", dict(side=1, offset=0.42, color=ORANGE, fs=13, weight="bold"))]
    return lab

for sol, name in [(False, "thales_3e_ex10.png"), (True, "thales_3e_ex10_solution.png")]:
    draw_thales(os.path.join(EX, name), kM=0.375, AB=7.2, AC=5.8, labels=labels_ex10(sol))

print("Toutes les figures ont été générées.")
