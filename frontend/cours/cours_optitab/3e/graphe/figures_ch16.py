# -*- coding: utf-8 -*-
"""Figures du chapitre 16 (Géométrie dans l'espace) — 3ème OptiTAB."""
import os
import sys
from math import cos, sin, radians

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import (new_fig, seg_label, right_angle, _proj, BLUE, ORANGE, GREEN, DARK,
                   NEUTRAL, DIR_COURS, DIR_EXOS, ROOT)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mp

LIGHT = "#d6eafc"
LORANGE = "#fdebd0"
WATER = "#cfe8fb"


def save(fig, ax, path, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


def lab(ax, P, txt, dx, dy, color=DARK, fs=12.5, dot=True):
    if dot:
        ax.scatter([P[0]], [P[1]], s=30, color=color, zorder=6)
    ax.annotate(txt, P, textcoords="offset points", xytext=(dx, dy), fontsize=fs,
                color=color, fontweight="bold")


def txt(ax, x, y, s, color=ORANGE, fs=12.5, ha="center", va="center", weight="bold"):
    ax.text(x, y, s, color=color, fontsize=fs, ha=ha, va=va, fontweight=weight)


# ---------------------------------------------------------------- briques 3D

def box(ax, L, P, H, o=(0, 0, 0), color=BLUE, lw=2.0, names=None, face=None):
    x0, y0, z0 = o
    c3 = {"A": (0, 0, 0), "B": (L, 0, 0), "C": (L, 0, H), "D": (0, 0, H),
          "E": (0, P, 0), "F": (L, P, 0), "G": (L, P, H), "H": (0, P, H)}
    V = {k: _proj(x0 + x, y0 + y, z0 + z) for k, (x, y, z) in c3.items()}
    if face:
        ax.add_patch(mp.Polygon([V[k] for k in "ABCD"], closed=True, facecolor=face,
                                edgecolor="none", alpha=0.5, zorder=1))
    edges = ["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"]
    for e in edges:
        hidden = e in ("EF", "HE", "AE")
        (a, b), (c, d) = V[e[0]], V[e[1]]
        ax.plot([a, c], [b, d], lw=1.3 if hidden else lw, color=color,
                linestyle="--" if hidden else "-", zorder=2)
    if names:
        offs = {"A": (-16, -14), "B": (8, -14), "C": (8, 4), "D": (-16, 4),
                "E": (-16, -12), "F": (10, -12), "G": (10, 4), "H": (-16, 6)}
        for k in names:
            lab(ax, V[k], f"${k}$", *offs[k], color=BLUE)
    return V


def ellipse(ax, cx, cy, rx, ry, color=BLUE, lw=2.0, back_hidden=True, full=False):
    t = np.linspace(0, 2 * np.pi, 200)
    front = t[t >= np.pi]
    back = t[t <= np.pi]
    ax.plot(cx + rx * np.cos(front), cy + ry * np.sin(front), lw=lw, color=color, zorder=3)
    if full or not back_hidden:
        ax.plot(cx + rx * np.cos(back), cy + ry * np.sin(back), lw=lw, color=color, zorder=3)
    else:
        ax.plot(cx + rx * np.cos(back), cy + ry * np.sin(back), lw=1.2, color=color,
                linestyle="--", zorder=3)


def cylinder(ax, cx, r, h, y0=0, color=BLUE, top=True, k=0.32):
    ellipse(ax, cx, y0, r, k * r, color)
    if top:
        ellipse(ax, cx, y0 + h, r, k * r, color, full=True)
    ax.plot([cx - r, cx - r], [y0, y0 + h], lw=2.0, color=color)
    ax.plot([cx + r, cx + r], [y0, y0 + h], lw=2.0, color=color)


def cone_up(ax, cx, r, h, y0=0, color=BLUE, k=0.3, axis=True):
    ellipse(ax, cx, y0, r, k * r, color)
    ax.plot([cx - r, cx], [y0, y0 + h], lw=2.0, color=color)
    ax.plot([cx + r, cx], [y0, y0 + h], lw=2.0, color=color)
    if axis:
        ax.plot([cx, cx], [y0, y0 + h], lw=1.4, color=ORANGE, linestyle="--")
        right_angle(ax, (cx, y0), (1, 0), (0, 1), size=0.16 * max(r, 1), color=ORANGE)


def cone_down(ax, cx, r, h, y0=0, color=BLUE, k=0.3):
    """Cône pointe en bas : sommet en (cx, y0), base (visible) à y0 + h."""
    ellipse(ax, cx, y0 + h, r, k * r, color, full=True)
    ax.plot([cx - r, cx], [y0 + h, y0], lw=2.0, color=color)
    ax.plot([cx + r, cx], [y0 + h, y0], lw=2.0, color=color)


def dome(ax, cx, r, y0, color=BLUE):
    t = np.linspace(0, np.pi, 120)
    ax.plot(cx + r * np.cos(t), y0 + r * np.sin(t), lw=2.0, color=color)


def ball(ax, cx, cy, R, color=BLUE, equator=True, face=None):
    ax.add_patch(mp.Circle((cx, cy), R, facecolor=face or "none", edgecolor=color,
                           lw=2.0, zorder=2))
    if equator:
        ellipse(ax, cx, cy, R, 0.28 * R, color, lw=1.6)


def pyramid(ax, b, p, h, o=(0, 0, 0), color=BLUE, height=True):
    x0, y0, z0 = o
    pts3 = {"A": (0, 0, 0), "B": (b, 0, 0), "C": (b, p, 0), "D": (0, p, 0),
            "S": (b / 2, p / 2, h), "O": (b / 2, p / 2, 0)}
    V = {k: _proj(x0 + x, y0 + y, z0 + z) for k, (x, y, z) in pts3.items()}
    for e, hid in [("AB", 0), ("BC", 0), ("CD", 1), ("DA", 1), ("AS", 0), ("BS", 0),
                   ("CS", 0), ("DS", 1)]:
        (a, bb), (c, d) = V[e[0]], V[e[1]]
        ax.plot([a, c], [bb, d], lw=1.3 if hid else 2.0, color=color,
                linestyle="--" if hid else "-")
    if height:
        ax.plot([V["O"][0], V["S"][0]], [V["O"][1], V["S"][1]], lw=1.5, color=ORANGE,
                linestyle="--")
    return V


# ---------------------------------------------------------------- cours

def cours_solides():
    fig, axes = plt.subplots(2, 3, figsize=(11, 7.2))
    fig.patch.set_facecolor("white")
    titres = ["Pavé droit\n$V = L \\times \\ell \\times h$",
              "Prisme droit\n$V = \\mathcal{B} \\times h$",
              "Cylindre\n$V = \\pi r^2 h$",
              "Pyramide\n$V = \\dfrac{\\mathcal{B} \\times h}{3}$",
              "Cône\n$V = \\dfrac{\\pi r^2 h}{3}$",
              "Boule\n$V = \\dfrac{4}{3}\\pi r^3$"]
    for ax, t in zip(axes.flat, titres):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-2.4, 4.4)
        ax.set_ylim(-1.6, 3.9)
        ax.text(1.0, -1.45, t, ha="center", va="top", fontsize=12.5, color=DARK,
                fontweight="bold", linespacing=1.6)
    a = axes[0, 0]
    V = box(a, 3.0, 2.2, 2.0, o=(-0.6, 0, 0))
    seg_label(a, V["A"], V["B"], "$L$", side=-1, offset=0.3, color=ORANGE, fs=13)
    seg_label(a, V["B"], V["F"], "$\\ell$", side=-1, offset=0.3, color=ORANGE, fs=13)
    seg_label(a, V["B"], V["C"], "$h$", side=1, offset=-0.3, color=ORANGE, fs=13)
    a = axes[0, 1]
    tri = [(0, 0), (2.4, 0), (0, 1.6)]
    dep = 2.2
    F0 = [_proj(x - 0.6, 0, z) for x, z in tri]
    F1 = [_proj(x - 0.6, dep, z) for x, z in tri]
    a.add_patch(mp.Polygon(F0, closed=True, facecolor=LIGHT, edgecolor=BLUE, lw=2.0))
    a.plot([F1[0][0], F1[1][0]], [F1[0][1], F1[1][1]], lw=1.3, color=BLUE, ls="--")
    a.plot([F1[1][0], F1[2][0]], [F1[1][1], F1[2][1]], lw=2.0, color=BLUE)
    a.plot([F1[2][0], F1[0][0]], [F1[2][1], F1[0][1]], lw=2.0, color=BLUE)
    for i, ls in [(0, "--"), (1, "-"), (2, "-")]:
        a.plot([F0[i][0], F1[i][0]], [F0[i][1], F1[i][1]], lw=2.0 if ls == "-" else 1.3,
               color=BLUE, ls=ls)
    txt(a, -0.22, 0.98, "$\\mathcal{B}$", fs=13)
    seg_label(a, F0[1], F1[1], "$h$", side=-1, offset=0.3, color=ORANGE, fs=13)
    a = axes[0, 2]
    cylinder(a, 1.0, 1.2, 2.6, y0=0.2)
    a.plot([1.0, 2.2], [2.8, 2.8], lw=1.6, color=ORANGE)
    txt(a, 1.6, 3.5, "$r$", fs=13)
    txt(a, 2.55, 1.5, "$h$", fs=13)
    a = axes[1, 0]
    V = pyramid(a, 2.8, 2.4, 2.6, o=(-0.6, 0, 0))
    txt(a, 1.0, 1.6, "$h$", fs=13)
    txt(a, 0.45, 0.3, "$\\mathcal{B}$", fs=12)
    a = axes[1, 1]
    cone_up(a, 1.0, 1.3, 2.9, y0=0.2)
    a.plot([1.0, 2.3], [0.2, 0.2], lw=1.6, color=ORANGE)
    txt(a, 1.65, 0.03, "$r$", fs=12)
    txt(a, 0.75, 1.6, "$h$", fs=13)
    a = axes[1, 2]
    ball(a, 1.0, 1.3, 1.45, face=LIGHT)
    a.scatter([1.0], [1.3], s=25, color=DARK, zorder=5)
    ang = radians(40)
    a.plot([1.0, 1.0 + 1.45 * cos(ang)], [1.3, 1.3 + 1.45 * sin(ang)], lw=1.6, color=ORANGE,
           zorder=4)
    txt(a, 1.38, 1.98, "$r$", fs=13)
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_COURS, "espace_3e_solides.png"), dpi=175,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK espace_3e_solides.png")


def cours_sections():
    fig, axes = plt.subplots(1, 4, figsize=(13, 4.2))
    fig.patch.set_facecolor("white")
    titres = ["Pavé : un rectangle", "Cylindre : un disque", "Pyramide : une réduction",
              "Sphère : un cercle"]
    for ax, t in zip(axes, titres):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-2.0, 3.6)
        ax.set_ylim(-1.3, 3.8)
        ax.text(0.8, -1.2, t, ha="center", va="top", fontsize=12.5, color=DARK,
                fontweight="bold")
    a = axes[0]
    box(a, 2.6, 2.2, 3.0, o=(-0.6, 0, 0))
    z = 1.3
    S = [_proj(-0.6 + x, y, z) for x, y in [(0, 0), (2.6, 0), (2.6, 2.2), (0, 2.2)]]
    a.add_patch(mp.Polygon(S, closed=True, facecolor=ORANGE, alpha=0.35, edgecolor=ORANGE,
                           lw=2.0, zorder=4))
    a = axes[1]
    cylinder(a, 0.8, 1.2, 3.0)
    t = np.linspace(0, 2 * np.pi, 120)
    a.fill(0.8 + 1.2 * np.cos(t), 1.4 + 0.38 * np.sin(t), color=ORANGE, alpha=0.35, zorder=4)
    a.plot(0.8 + 1.2 * np.cos(t), 1.4 + 0.38 * np.sin(t), color=ORANGE, lw=2.0, zorder=4)
    a = axes[2]
    b, p, h = 3.0, 2.6, 3.4
    pyramid(a, b, p, h, o=(-0.8, 0, 0), height=False)
    kk = 0.5
    S3 = [(b / 2 + (x - b / 2) * kk, p / 2 + (y - p / 2) * kk, h * (1 - kk))
          for x, y in [(0, 0), (b, 0), (b, p), (0, p)]]
    S = [_proj(-0.8 + x, y, z) for x, y, z in S3]
    a.add_patch(mp.Polygon(S, closed=True, facecolor=ORANGE, alpha=0.35, edgecolor=ORANGE,
                           lw=2.0, zorder=4))
    a = axes[3]
    R = 1.6
    ball(a, 0.8, 1.3, R, equator=False)
    d = 0.8
    r = (R * R - d * d) ** 0.5
    a.fill(0.8 + r * np.cos(t), 1.3 + d + 0.3 * r * np.sin(t), color=ORANGE, alpha=0.35,
           zorder=4)
    a.plot(0.8 + r * np.cos(t), 1.3 + d + 0.3 * r * np.sin(t), color=ORANGE, lw=2.0, zorder=4)
    a.scatter([0.8], [1.3], s=25, color=DARK, zorder=5)
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_COURS, "espace_3e_sections.png"), dpi=175,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK espace_3e_sections.png")


# ---------------------------------------------------------------- globe

class Globe:
    def __init__(self, ax, R=2.6, lam0=-10, elev=22):
        self.ax, self.R, self.lam0, self.e = ax, R, lam0, radians(elev)

    def p(self, lat, lon, r=None):
        r = self.R if r is None else r
        ph, la = radians(lat), radians(lon - self.lam0)
        X, Y, Z = r * cos(ph) * cos(la), r * cos(ph) * sin(la), r * sin(ph)
        return (Y, Z * cos(self.e) - X * sin(self.e), X * cos(self.e) + Z * sin(self.e))

    def curve(self, pts, color, lw=1.8, hidden_ls="--"):
        pts = np.array(pts)
        vis = pts[:, 2] >= -1e-9
        start = 0
        for i in range(1, len(pts) + 1):
            if i == len(pts) or vis[i] != vis[start]:
                seg = pts[start:min(i + 1, len(pts))]
                if vis[start]:
                    self.ax.plot(seg[:, 0], seg[:, 1], lw=lw, color=color, zorder=3)
                else:
                    self.ax.plot(seg[:, 0], seg[:, 1], lw=1.0, color=color,
                                 linestyle=hidden_ls, zorder=2)
                start = i
        return pts

    def parallel(self, lat, color, lw=1.8):
        return self.curve([self.p(lat, l) for l in np.linspace(-180, 180, 361)], color, lw)

    def meridian(self, lon, color, lw=1.8):
        return self.curve([self.p(lt, lon) for lt in np.linspace(-90, 90, 181)], color, lw)

    def outline(self):
        self.ax.add_patch(mp.Circle((0, 0), self.R, facecolor="#f4f9fe", edgecolor=BLUE,
                                    lw=2.2, zorder=1))


def cours_globe():
    fig, ax = new_fig(7.2, 6.4)
    g = Globe(ax, lam0=15)
    g.outline()
    g.parallel(0, BLUE, 2.0)
    g.meridian(0, GREEN, 2.0)
    latM, lonM = 40, 50
    g.parallel(latM, NEUTRAL, 1.2)
    g.meridian(lonM, NEUTRAL, 1.2)
    O = (0, 0)
    M = g.p(latM, lonM)
    E0 = g.p(0, 0)
    EM = g.p(0, lonM)
    for Q, col in [(M, DARK), (E0, GREEN), (EM, DARK)]:
        ax.plot([0, Q[0]], [0, Q[1]], lw=1.4, color=col, zorder=4)
    arc_lat = np.array([g.p(t, lonM, 0.95) for t in np.linspace(0, latM, 40)])
    ax.plot(arc_lat[:, 0], arc_lat[:, 1], lw=2.6, color=ORANGE, zorder=5)
    arc_lon = np.array([g.p(0, t, 1.15) for t in np.linspace(0, lonM, 40)])
    ax.plot(arc_lon[:, 0], arc_lon[:, 1], lw=2.6, color="#8e44ad", zorder=5)
    lab(ax, O, "O", -18, 2, color=DARK)
    lab(ax, M[:2], "M", 6, 6, color=ORANGE)
    N = g.p(90, 0)
    lab(ax, N[:2], "N", -5, 8, color=DARK)
    txt(ax, 2.85, -0.95, "équateur", color=BLUE, fs=11.5, ha="left")
    txt(ax, -2.2, 2.75, "méridien de\nGreenwich", color=GREEN, fs=11.5, ha="right")
    txt(ax, 2.6, 2.1, "parallèle\nde M", color=NEUTRAL, fs=11, ha="left")
    txt(ax, 0, -3.0, "arc orange : latitude de M = 40° N", color=ORANGE, fs=11.5)
    txt(ax, 0, -3.45, "arc violet : longitude de M = 50° E", color="#8e44ad", fs=11.5)
    save(fig, ax, os.path.join(DIR_COURS, "espace_3e_globe.png"), (-4.6, 4.6), (-3.7, 3.4))


def repere_pave(path, L=6, P=4, H=3, s=0.8, point=None, pname="P", graduer=True):
    fig, ax = new_fig(7.6, 5.6)
    V = box(ax, L * s, P * s, H * s)
    O = V["A"]
    ends = {"x": _proj((L + 1.3) * s, 0, 0), "y": _proj(0, (P + 1.6) * s, 0),
            "z": _proj(0, 0, (H + 1.1) * s)}
    for k, Q in ends.items():
        ax.annotate("", xy=Q, xytext=O, arrowprops=dict(arrowstyle="-|>", lw=1.8,
                                                         color=DARK), zorder=5)
        txt(ax, Q[0] + (0.15 if k != "z" else -0.25), Q[1] + (0.2 if k != "x" else -0.25),
            f"${k}$", color=DARK, fs=13)
    if graduer:
        for i in range(1, L + 1):
            Q = _proj(i * s, 0, 0)
            ax.plot([Q[0], Q[0]], [Q[1] - 0.07, Q[1] + 0.07], lw=1.2, color=DARK)
            txt(ax, Q[0], Q[1] - 0.3, str(i), color=DARK, fs=10, weight="normal")
        for i in range(1, H + 1):
            Q = _proj(0, 0, i * s)
            ax.plot([Q[0] - 0.07, Q[0] + 0.07], [Q[1], Q[1]], lw=1.2, color=DARK)
            txt(ax, Q[0] - 0.25, Q[1], str(i), color=DARK, fs=10, weight="normal")
        for i in range(1, P + 1):
            Q = _proj(0, i * s, 0)
            ax.plot([Q[0] - 0.07, Q[0] + 0.07], [Q[1], Q[1]], lw=1.2, color=DARK)
            txt(ax, Q[0] - 0.22, Q[1] + 0.12, str(i), color=DARK, fs=10, weight="normal")
    lab(ax, O, "O", -18, -14, color=DARK)
    if point:
        x, y, z = point
        Pp = _proj(x * s, y * s, z * s)
        Pb = _proj(x * s, y * s, 0)
        Px = _proj(x * s, 0, 0)
        Py = _proj(0, y * s, 0)
        for A, B in [(Pp, Pb), (Pb, Px), (Pb, Py)]:
            ax.plot([A[0], B[0]], [A[1], B[1]], lw=1.4, color=ORANGE, ls=":", zorder=4)
        lab(ax, Pp, pname, 7, 4, color=ORANGE)
        ax.scatter([Pb[0]], [Pb[1]], s=18, color=ORANGE, zorder=6)
    xs = [v[0] for v in V.values()] + [q[0] for q in ends.values()]
    ys = [v[1] for v in V.values()] + [q[1] for q in ends.values()]
    save(fig, ax, path, (min(xs) - 0.8, max(xs) + 0.8), (min(ys) - 0.7, max(ys) + 0.5))


# ---------------------------------------------------------------- exercices

def ex_pave():
    fig, ax = new_fig(7.2, 4.6)
    V = box(ax, 8 * 0.6, 5 * 0.6, 3 * 0.6, names="ABCDEFGH")
    seg_label(ax, V["A"], V["B"], "8 cm", side=-1, offset=0.38)
    seg_label(ax, V["B"], V["F"], "5 cm", side=-1, offset=0.42)
    seg_label(ax, V["F"], V["G"], "3 cm", side=-1, offset=0.55)
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_pave.png"), (-0.8, 6.8), (-0.8, 3.4))


def ex_cylindre():
    fig, ax = new_fig(4.6, 5.4)
    cylinder(ax, 0, 1.2, 4.0)
    ax.plot([0, 1.2], [4.0, 4.0], lw=1.6, color=ORANGE)
    ax.scatter([0], [4.0], s=22, color=ORANGE, zorder=5)
    txt(ax, 0.6, 4.65, "3 cm", fs=12)
    txt(ax, 1.55, 2.0, "10 cm", fs=12, ha="left")
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_cylindre.png"), (-1.8, 3.0), (-0.7, 5.0))


def ex_pyramide():
    fig, ax = new_fig(5.6, 5.4)
    V = pyramid(ax, 3.0, 3.0, 4.0)
    for k, off in [("A", (-14, -14)), ("B", (8, -14)), ("C", (8, -4)), ("D", (-16, 2)),
                   ("S", (-4, 10))]:
        lab(ax, V[k], f"${k}$", *off, color=BLUE)
    lab(ax, V["O"], "$O$", 6, -12, color=ORANGE)
    seg_label(ax, V["A"], V["B"], "6 cm", side=-1, offset=0.35)
    txt(ax, V["O"][0] + 0.25, (V["O"][1] + V["S"][1]) / 2, "9 cm", fs=12, ha="left")
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_pyramide.png"), (-0.8, 4.8), (-0.8, 4.8))


def ex_cone():
    fig, ax = new_fig(4.8, 5.2)
    cone_up(ax, 0, 1.6, 3.6, axis=True)
    ax.annotate("", xy=(1.6, -0.75), xytext=(-1.6, -0.75),
                arrowprops=dict(arrowstyle="<->", lw=1.5, color=ORANGE))
    txt(ax, 0, -1.02, "diamètre 8 cm", fs=12)
    txt(ax, 0.12, 1.15, "9 cm", fs=12, ha="left")
    lab(ax, (0, 3.6), "$S$", 6, 6, color=DARK)
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_cone.png"), (-2.2, 2.2), (-1.4, 4.2))


def ex_boule():
    fig, ax = new_fig(4.6, 4.6)
    ball(ax, 0, 0, 1.8, face="#f4f9fe")
    ax.scatter([0], [0], s=25, color=DARK, zorder=5)
    ang = radians(38)
    ax.plot([0, 1.8 * cos(ang)], [0, 1.8 * sin(ang)], lw=1.6, color=ORANGE, zorder=4)
    txt(ax, 0.42, 0.98, "3 cm", fs=12)
    lab(ax, (0, 0), "O", -16, -4, color=DARK, dot=False)
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_boule.png"), (-2.2, 2.2), (-2.2, 2.2))


def ex_patron():
    fig, ax = new_fig(6.4, 4.8)
    cases = {"B": (0, 1), "C": (1, 1), "D": (2, 1), "E": (3, 1), "A": (1, 2), "F": (1, 0)}
    for n, (x, y) in cases.items():
        ax.add_patch(mp.Rectangle((x, y), 1, 1, facecolor=LIGHT, edgecolor=BLUE, lw=2.0))
        txt(ax, x + 0.5, y + 0.5, n, color=DARK, fs=16)
    ax.annotate("", xy=(4, 0.82), xytext=(3, 0.82),
                arrowprops=dict(arrowstyle="<->", lw=1.4, color=ORANGE))
    txt(ax, 3.5, 0.62, "2 cm", fs=12)
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_patron.png"), (-0.3, 4.3), (-0.3, 3.3))


def ex_vues_sol():
    fig, ax = new_fig(9.6, 3.8)
    s = 0.42
    vues = [("Face (8 × 3)", 8, 3, 0), ("Dessus (8 × 5)", 8, 5, 4.2), ("Côté droit (5 × 3)",
                                                                       5, 3, 8.4)]
    for nom, w, h, x0 in vues:
        ax.add_patch(mp.Rectangle((x0, 0), w * s, h * s, facecolor="#c8e6c9", edgecolor=GREEN,
                                  lw=2.0))
        txt(ax, x0 + w * s / 2, -0.35, nom, color=GREEN, fs=12)
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_vues_sol.png"), (-0.3, 10.9), (-0.8, 2.4))


def ex_section_pave():
    fig, ax = new_fig(6.4, 5.4)
    s = 0.5
    V = box(ax, 8 * s, 5 * s, 6 * s, names="ABCDEFGH")
    z = 2 * s
    S = [_proj(x, y, z) for x, y in [(0, 0), (8 * s, 0), (8 * s, 5 * s), (0, 5 * s)]]
    ax.add_patch(mp.Polygon(S, closed=True, facecolor=ORANGE, alpha=0.35, edgecolor=ORANGE,
                            lw=2.0, zorder=4))
    for Q, n in zip(S, "IJKL"):
        lab(ax, Q, f"${n}$", -16 if n in "IL" else 8, 2, color=ORANGE)
    seg_label(ax, V["A"], V["B"], "8 cm", side=-1, offset=0.38)
    seg_label(ax, V["B"], V["F"], "5 cm", side=-1, offset=0.42)
    seg_label(ax, V["F"], V["G"], "6 cm", side=-1, offset=0.55)
    seg_label(ax, V["A"], S[0], "2 cm", side=1, offset=0.62, color=ORANGE)
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_section_pave.png"), (-0.9, 6.1),
         (-0.8, 4.4))


def ex_globe():
    fig, ax = new_fig(7.2, 6.4)
    g = Globe(ax, lam0=-15)
    g.outline()
    g.parallel(0, BLUE, 2.0)
    g.meridian(0, GREEN, 2.0)
    g.parallel(35, NEUTRAL, 1.2)
    g.parallel(-35, NEUTRAL, 1.2)
    g.meridian(20, NEUTRAL, 1.2)
    g.meridian(-50, NEUTRAL, 1.2)
    for nom, (la, lo), off in [("A", (35, 20), (6, 6)), ("B", (35, -50), (-18, 6)),
                               ("C", (-35, 20), (6, -16))]:
        Q = g.p(la, lo)
        lab(ax, Q[:2], nom, *off, color=ORANGE)
    N = g.p(90, 0)
    lab(ax, N[:2], "N", -5, 8, color=DARK)
    txt(ax, 2.95, -0.7, "équateur", color=BLUE, fs=11.5, ha="left")
    txt(ax, 0.75, -2.85, "méridien de Greenwich", color=GREEN, fs=11.5, ha="left")
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_globe.png"), (-3.4, 4.6), (-3.2, 3.2))


def ex_section_sphere():
    fig, ax = new_fig(5.6, 5.6)
    R, d = 2.5, 1.5
    r = (R * R - d * d) ** 0.5
    t = np.linspace(0, 2 * np.pi, 200)
    ax.add_patch(mp.Circle((0, 0), R, facecolor="#f4f9fe", edgecolor=BLUE, lw=2.0))
    ax.fill(r * np.cos(t), d + 0.26 * r * np.sin(t), color=ORANGE, alpha=0.3)
    ax.plot(r * np.cos(t), d + 0.26 * r * np.sin(t), color=ORANGE, lw=1.8)
    ax.plot([0, 0], [0, d], lw=1.7, color=DARK)
    ax.plot([0, r], [d, d], lw=1.7, color=ORANGE)
    ax.plot([0, r], [0, d], lw=1.7, color=BLUE, ls="--")
    right_angle(ax, (0, d), (0, -1), (1, 0), size=0.2, color=DARK)
    lab(ax, (0, 0), "O", -16, -12, color=DARK)
    lab(ax, (0, d), "H", -16, 4, color=ORANGE)
    lab(ax, (r, d), "M", 8, 2, color=ORANGE)
    txt(ax, -0.32, d / 2, "3 cm", color=DARK, fs=11.5, ha="right")
    txt(ax, r / 2 + 0.25, d / 2 - 0.15, "5 cm", color=BLUE, fs=11.5, ha="left")
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_section_sphere.png"), (-2.8, 2.8),
         (-2.8, 2.8))


def ex_reservoir():
    fig, ax = new_fig(4.8, 6.0)
    r, h = 1.5, 3.0
    ellipse(ax, 0, 0, r, 0.32 * r)
    ellipse(ax, 0, h, r, 0.32 * r)
    ax.plot([-r, -r], [0, h], lw=2.0, color=BLUE)
    ax.plot([r, r], [0, h], lw=2.0, color=BLUE)
    dome(ax, 0, r, h)
    ax.plot([0, r], [0, 0], lw=1.6, color=ORANGE)
    ax.scatter([0], [0], s=22, color=ORANGE, zorder=5)
    txt(ax, 0.75, -0.21, "1 m", fs=12)
    txt(ax, r + 0.3, h / 2, "2 m", fs=12, ha="left")
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_reservoir.png"), (-2.0, 2.6), (-0.8, 4.8))


def ex_cavite():
    fig, ax = new_fig(5.0, 5.0)
    ax.add_patch(mp.Circle((0, 0), 2.5, facecolor=LIGHT, edgecolor=BLUE, lw=2.0))
    ax.add_patch(mp.Circle((0, 0), 1.0, facecolor="white", edgecolor=ORANGE, lw=1.8, ls="--"))
    ax.scatter([0], [0], s=25, color=DARK, zorder=5)
    ax.plot([0, 2.5 * cos(radians(35))], [0, 2.5 * sin(radians(35))], lw=1.6, color=BLUE)
    ax.plot([0, -1.0], [0, 0], lw=1.6, color=ORANGE)
    txt(ax, 1.25, 1.2, "5 cm", color=BLUE, fs=12)
    txt(ax, -0.5, 0.25, "2 cm", fs=11)
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_cavite.png"), (-2.8, 2.8), (-2.8, 2.8))


def ex_cone_coupe():
    fig, ax = new_fig(5.2, 5.6)
    r, h = 1.8, 3.6
    cone_up(ax, 0, r, h)
    t = np.linspace(0, 2 * np.pi, 160)
    ax.fill(r / 2 * np.cos(t), h / 2 + 0.3 * r / 2 * np.sin(t), color=ORANGE, alpha=0.3)
    ax.plot(r / 2 * np.cos(t), h / 2 + 0.3 * r / 2 * np.sin(t), color=ORANGE, lw=1.8)
    ax.plot([0, r], [0, 0], lw=1.6, color=ORANGE)
    txt(ax, r / 2 + 0.2, 0.2, "6 cm", fs=12)
    txt(ax, -0.25, h / 4, "12 cm", fs=12, ha="right")
    lab(ax, (0, h), "$S$", 6, 6, color=DARK)
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_cone_coupe.png"), (-2.4, 2.4), (-0.9, 4.2))


def ex_silo():
    fig, ax = new_fig(4.8, 6.2)
    r, hc, hk = 1.2, 3.2, 0.8
    cylinder(ax, 0, r, hc, y0=hk)
    ax.plot([-r, 0, r], [hk, 0, hk], lw=2.0, color=BLUE)
    ax.plot([0, r], [hk + hc, hk + hc], lw=1.6, color=ORANGE)
    ax.scatter([0], [hk + hc], s=22, color=ORANGE, zorder=5)
    txt(ax, r / 2, hk + hc + 0.62, "3 m", fs=12)
    ax.plot([0, 0], [0, hk], lw=1.3, color=ORANGE, ls="--")
    for y1, y2, t in [(hk, hk + hc, "8 m"), (0, hk, "2 m")]:
        ax.annotate("", xy=(r + 0.35, y2), xytext=(r + 0.35, y1),
                    arrowprops=dict(arrowstyle="<->", lw=1.3, color=ORANGE))
        txt(ax, r + 0.5, (y1 + y2) / 2, t, fs=12, ha="left")
    for yy in (0, hk):
        ax.plot([0.05, r + 0.45], [yy, yy], lw=0.7, color=ORANGE, ls=":")
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_silo.png"), (-1.8, 2.8), (-0.4, 5.0))


def ex_cube():
    fig, ax = new_fig(5.6, 5.0)
    V = box(ax, 3, 3, 3, names="ABCDEFGH")
    ax.plot([V["A"][0], V["F"][0]], [V["A"][1], V["F"][1]], lw=2.2, color=ORANGE, ls="--",
            zorder=4)
    ax.plot([V["A"][0], V["G"][0]], [V["A"][1], V["G"][1]], lw=2.4, color=GREEN, ls="--",
            zorder=4)
    seg_label(ax, V["A"], V["B"], "6 cm", side=-1, offset=0.38)
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_cube.png"), (-0.8, 5.2), (-0.8, 4.6))


def ex_glace():
    fig, ax = new_fig(4.4, 5.6)
    r, h = 1.0, 3.2
    ellipse(ax, 0, h, r, 0.3 * r)
    ax.plot([-r, 0, r], [h, 0, h], lw=2.0, color=BLUE)
    dome(ax, 0, r, h)
    ax.plot([0, r], [h, h], lw=1.6, color=ORANGE)
    ax.scatter([0], [h], s=22, color=ORANGE, zorder=5)
    txt(ax, r / 2, h + 0.52, "3 cm", fs=11.5)
    ax.plot([0, 0], [0, h], lw=1.3, color=ORANGE, ls="--")
    ax.annotate("", xy=(-r - 0.3, h), xytext=(-r - 0.3, 0),
                arrowprops=dict(arrowstyle="<->", lw=1.3, color=ORANGE))
    for yy in (0, h):
        ax.plot([-r - 0.4, -0.05 if yy == 0 else -r], [yy, yy], lw=0.7, color=ORANGE, ls=":")
    txt(ax, -r - 0.45, h / 2, "10 cm", fs=12, ha="right")
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_glace.png"), (-2.6, 1.6), (-0.4, 4.4))


def ex_pyramide_louvre():
    fig, ax = new_fig(6.4, 5.2)
    b, h = 4.2, 2.6
    V = pyramid(ax, b, b, h)
    for k, off in [("A", (-14, -14)), ("B", (8, -14)), ("C", (8, -4)), ("D", (-16, 2)),
                   ("S", (-4, 10))]:
        lab(ax, V[k], f"${k}$", *off, color=BLUE)
    Ib = _proj(b / 2, 0, 0)
    O = V["O"]
    ax.plot([O[0], Ib[0]], [O[1], Ib[1]], lw=1.6, color=ORANGE, ls="--")
    ax.plot([V["S"][0], Ib[0]], [V["S"][1], Ib[1]], lw=2.0, color=GREEN)
    lab(ax, O, "$O$", 7, -2, color=ORANGE)
    lab(ax, Ib, "$I$", -4, -18, color=GREEN)
    txt(ax, 2.9, -0.75, "AB = 35 m      SO = 21,6 m", color=DARK, fs=12)
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_pyramide_louvre.png"), (-0.8, 6.4),
         (-1.1, 3.6))


def ex_verre():
    fig, ax = new_fig(4.6, 5.8)
    r, h = 1.2, 3.6
    hl = 3.0
    rl = r * hl / h
    ax.fill([-rl, 0, rl], [hl, 0, hl], color=WATER, zorder=1)
    t = np.linspace(0, 2 * np.pi, 160)
    ax.fill(rl * np.cos(t), hl + 0.3 * rl * np.sin(t), color="#9fd0f5", zorder=1)
    ax.plot(rl * np.cos(t), hl + 0.3 * rl * np.sin(t), color=BLUE, lw=1.2, zorder=2)
    cone_down(ax, 0, r, h)
    ax.plot([0, r], [h, h], lw=1.6, color=ORANGE)
    txt(ax, r / 2, h + 0.62, "4 cm", fs=11.5)
    ax.annotate("", xy=(-r - 0.35, h), xytext=(-r - 0.35, 0),
                arrowprops=dict(arrowstyle="<->", lw=1.3, color=ORANGE))
    txt(ax, -r - 0.5, h / 2, "12 cm", fs=11.5, ha="right")
    ax.annotate("", xy=(r + 0.35, hl), xytext=(r + 0.35, 0),
                arrowprops=dict(arrowstyle="<->", lw=1.3, color=BLUE))
    txt(ax, r + 0.5, hl / 2, "10 cm", color=BLUE, fs=11.5, ha="left")
    for yy in (0, hl):
        ax.plot([0, r + 0.42], [yy, yy], lw=0.7, color=BLUE, ls=":")
    ax.plot([-r - 0.42, 0], [0, 0], lw=0.7, color=ORANGE, ls=":")
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_verre.png"), (-2.9, 2.9), (-0.4, 4.5))


def ex_aquarium():
    fig, ax = new_fig(7.0, 5.0)
    s = 0.05
    L, P, H, eau = 80 * s, 40 * s, 50 * s, 45 * s
    W = [_proj(x, y, z) for x, y, z in [(0, 0, 0), (L, 0, 0), (L, 0, eau), (0, 0, eau)]]
    ax.add_patch(mp.Polygon(W, closed=True, facecolor=WATER, edgecolor="none", zorder=1))
    T = [_proj(x, y, eau) for x, y in [(0, 0), (L, 0), (L, P), (0, P)]]
    ax.add_patch(mp.Polygon(T, closed=True, facecolor="#9fd0f5", edgecolor=BLUE, lw=1.0,
                            alpha=0.8, zorder=1))
    Rt = [_proj(L, y, z) for y, z in [(0, 0), (P, 0), (P, eau), (0, eau)]]
    ax.add_patch(mp.Polygon(Rt, closed=True, facecolor="#b8dcf8", edgecolor="none", zorder=1))
    V = box(ax, L, P, H)
    bc = _proj(L * 0.35, P * 0.5, 0.3)
    ax.add_patch(mp.Circle(bc, 0.3, facecolor=ORANGE, edgecolor="#a04000", lw=1.2, zorder=3))
    seg_label(ax, V["A"], V["B"], "80 cm", side=-1, offset=0.35)
    seg_label(ax, V["B"], V["F"], "40 cm", side=-1, offset=0.45)
    seg_label(ax, V["F"], V["G"], "50 cm", side=-1, offset=0.6)
    ax.annotate("", xy=W[3], xytext=W[0], arrowprops=dict(arrowstyle="<->", lw=1.3,
                                                          color=BLUE))
    txt(ax, W[0][0] - 0.15, eau / 2, "45 cm", color=BLUE, fs=11.5, ha="right")
    save(fig, ax, os.path.join(DIR_EXOS, "espace_3e_aquarium.png"), (-1.4, 6.4), (-0.7, 3.6))


if __name__ == "__main__":
    cours_solides()
    cours_sections()
    cours_globe()
    repere_pave(os.path.join(DIR_COURS, "espace_3e_repere.png"), point=(4, 2, 3), pname="M")
    ex_pave()
    ex_cylindre()
    ex_pyramide()
    ex_cone()
    ex_boule()
    ex_patron()
    ex_vues_sol()
    ex_section_pave()
    repere_pave(os.path.join(DIR_EXOS, "espace_3e_repere_pave.png"), point=(2, 3, 1))
    ex_globe()
    ex_section_sphere()
    ex_reservoir()
    ex_cavite()
    ex_cone_coupe()
    ex_silo()
    ex_cube()
    ex_glace()
    ex_pyramide_louvre()
    ex_verre()
    ex_aquarium()
    print("Figures chapitre 16 : OK")
