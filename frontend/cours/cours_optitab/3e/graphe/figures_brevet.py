# -*- coding: utf-8 -*-
"""Figures des sujets type brevet — 3ème OptiTAB."""
import os
import sys
from math import cos, sin, radians, pi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp

from fig3e import (new_fig, seg_label, right_angle, dot_label, graphe, barres, arbre2,
                   _proj, BLUE, ORANGE, GREEN, DARK, NEUTRAL, DIR_EXOS, ROOT)
import figures_ch16 as f16
import figures_ch17 as f17
import scratch3e as S
from scripts_brevet import SCRIPTS, TITRES

LIGHT = "#d6eafc"


def out(nom):
    return os.path.join(DIR_EXOS, f"brevet_3e_{nom}.png")


def save(fig, ax, path, xlim=None, ylim=None):
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


def Pt(ax, name, xy, dx, dy, color=DARK):
    dot_label(ax, xy, f"${name}$", dx, dy, color=color, s=34)


def poly(ax, pts, color=BLUE, face=LIGHT, lw=2.2, z=2):
    ax.add_patch(mp.Polygon(pts, closed=True, facecolor=face, edgecolor=color, lw=lw, zorder=z))


def table_fig(path, rows, w0=1.7, w=0.95, h=0.5, fs=12.5):
    """rows : liste de lignes ; la première colonne est l'en-tête (style commun fig3e.tableau)."""
    from fig3e import tableau
    return tableau(path, rows, w0=w0, w=w, h=h, fs=fs)


def _ancien_table_fig(path, rows, w0=1.7, w=0.95, h=0.5, fs=12.5):
    nr, nc = len(rows), len(rows[0])
    W = w0 + w * (nc - 1)
    fig, ax = plt.subplots(figsize=(W * 0.9 + 0.2, nr * h * 0.9 + 0.2))
    fig.patch.set_facecolor("white")
    xs = [0, w0] + [w0 + w * k for k in range(1, nc)]
    for r, row in enumerate(rows):
        y = -(r + 1) * h
        for c, val in enumerate(row):
            x0 = xs[c]
            x1 = xs[c + 1] if c + 1 < len(xs) else W
            ax.add_patch(mp.Rectangle((x0, y), x1 - x0, h, facecolor="#e8f4fd" if c == 0 else "white",
                                      edgecolor=BLUE, lw=1.3))
            ax.text((x0 + x1) / 2, y + h / 2, val, ha="center", va="center", fontsize=fs,
                    color=DARK, fontweight="bold" if c == 0 else "normal")
    ax.set_xlim(-0.05, W + 0.05)
    ax.set_ylim(-nr * h - 0.05, 0.05)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


def frac(a, b):
    return f"{a}/{b}"


# ---------------------------------------------------------------- sujet 01

def s01():
    fig, ax = new_fig(6.4, 5.0)
    A, B, C, M, N = (0, 0), (6, 0), (0, 4.5), (2, 0), (0, 1.5)
    poly(ax, [A, B, C])
    ax.plot([M[0], N[0]], [M[1], N[1]], lw=2.2, color=ORANGE, zorder=3)
    right_angle(ax, A, (1, 0), (0, 1), size=0.3)
    for n, p, off in [("A", A, (-16, -14)), ("B", B, (8, -12)), ("C", C, (-16, 4)),
                      ("M", M, (-4, -18)), ("N", N, (-18, 2))]:
        Pt(ax, n, p, *off, color=ORANGE if n in "MN" else DARK)
    seg_label(ax, M, B, "8 m", side=-1, offset=0.35)
    seg_label(ax, A, M, "4 m", side=-1, offset=0.35)
    seg_label(ax, A, C, "9 m", side=1, offset=0.45)
    save(fig, ax, out("s01_voile"), (-1.2, 7.0), (-1.0, 5.2))
    graphe(out("s01_tarifs"),
           curves=[(lambda n: 18 + 7 * n, 0, 15, BLUE, ("A", 13)),
                   (lambda n: 10 * n, 0, 15, ORANGE, ("B", 14))],
           xb=(-0.8, 15.8), yb=(-6, 168), xt=1, yt=10, w=8.4, h=6.0,
           xlabel="nombre de jours", ylabel="prix (€)")
    table_fig(out("s01_scores"), [["Score", "0", "1", "2", "3"],
                                  ["Effectif", "2", "5", "8", "5"]])
    arbre2(out("s01_arbre"), [("R", frac(3, 4)), ("B", frac(1, 4))],
           [[("R", frac(3, 4)), ("B", frac(1, 4))], [("R", frac(3, 4)), ("B", frac(1, 4))]])


# ---------------------------------------------------------------- sujet 02

def s02():
    fig, ax = new_fig(6.4, 4.4)
    k = 1.1
    A, B, C = (0, 0), (4 * k, 0), (0, 2.5 * k)
    poly(ax, [A, B, C])
    right_angle(ax, A, (1, 0), (0, 1), size=0.25)
    Pt(ax, "A", A, -16, -14)
    Pt(ax, "B", B, 8, -12)
    Pt(ax, "C", C, -16, 4)
    seg_label(ax, A, B, "4 m", side=-1, offset=0.3)
    seg_label(ax, A, C, "2,5 m", side=1, offset=0.5)
    seg_label(ax, B, C, "versant", side=-1, offset=-0.35, color=ORANGE)
    save(fig, ax, out("s02_abri"), (-1.2, 5.4), (-0.8, 3.3))
    fig, ax = new_fig(4.2, 5.4)
    f16.cylinder(ax, 0, 1.0, 4.0)
    ax.plot([0, 1.0], [4.0, 4.0], lw=1.6, color=ORANGE)
    ax.scatter([0], [4.0], s=20, color=ORANGE, zorder=5)
    f16.txt(ax, 0.5, 4.62, "4 cm", fs=12)
    f16.txt(ax, 1.35, 2.0, "20 cm", fs=12, ha="left")
    save(fig, ax, out("s02_bouteille"), (-1.5, 2.6), (-0.6, 5.0))
    S.render(out("s02_script"), SCRIPTS["s02"], TITRES["s02"])
    arbre2(out("s02_arbre"), [("A", frac(3, 4)), ("B", frac(1, 4))],
           [[("rouge", frac(1, 2)), ("bleue", frac(1, 2))],
            [("rouge", frac(1, 2)), ("bleue", frac(1, 2))]])


# ---------------------------------------------------------------- sujet 03

def s03():
    def trajet(t):
        if t <= 2:
            return 90 * t
        if t <= 2.5:
            return 180
        return 180 + 80 * (t - 2.5)
    graphe(out("s03_trajet"), curves=[(trajet, 0, 4, BLUE)],
           xb=(-0.25, 4.6), yb=(-18, 340), xt=0.5, yt=20, w=8.4, h=6.2,
           xlabel="durée (h)", ylabel="distance (km)")
    fig, ax = new_fig(8.0, 4.6)
    s = 0.62
    Sb, St, Bb, Bt, O = (0, 0), (0, 7.2 * s), (7.6 * s, 0), (7.6 * s, 1.5 * s), (9.6 * s, 0)
    ax.plot([-0.6, 10.4 * s], [0, 0], lw=1.6, color=NEUTRAL)
    ax.plot([Sb[0], St[0]], [Sb[1], St[1]], lw=4, color=BLUE)
    ax.plot([Bb[0], Bt[0]], [Bb[1], Bt[1]], lw=3, color=GREEN)
    ax.plot([St[0] - 0.8, O[0]], [St[1] + 0.8 * 0.75, O[1]], lw=1.6, color=ORANGE, ls="--")
    f16.txt(ax, St[0] - 0.2, St[1] + 1.0, "rayon de soleil", color=ORANGE, fs=11, ha="left")
    Pt(ax, "S", Sb, -16, -14)
    Pt(ax, "T", St, -18, -12)
    Pt(ax, "B", Bb, -6, -18, GREEN)
    Pt(ax, "H", Bt, -4, 8, GREEN)
    Pt(ax, "O", O, 6, -14, ORANGE)
    f16.txt(ax, Bt[0] - 0.15, 0.75 * s, "1,5 m", color=GREEN, fs=11, ha="right")
    ax.annotate("", xy=(O[0], -0.55), xytext=(Bb[0], -0.55),
                arrowprops=dict(arrowstyle="<->", lw=1.2, color=DARK))
    f16.txt(ax, (Bb[0] + O[0]) / 2, -0.82, "2 m", color=DARK, fs=11)
    ax.annotate("", xy=(O[0], -1.25), xytext=(Sb[0], -1.25),
                arrowprops=dict(arrowstyle="<->", lw=1.2, color=DARK))
    f16.txt(ax, O[0] / 2, -1.52, "9,6 m", color=DARK, fs=11)
    f16.txt(ax, -0.25, St[1] / 2, "statue", color=BLUE, fs=11.5, ha="right")
    save(fig, ax, out("s03_statue"), (-1.6, 6.8), (-1.9, 5.6))
    cells = {"A1": "Activité", "B1": "Élèves", "A2": "Musée", "B2": 18, "A3": "Parc",
             "B3": 12, "A4": "Spectacle", "B4": 10, "A5": "Plage", "B5": 8, "A6": "Total"}
    f17.tableur(out("s03_tableur"), 2, 6, cells, sel="B6", widths=[1.5, 1.1])


# ---------------------------------------------------------------- sujet 04

def s04():
    fig, ax = new_fig(6.6, 5.2)
    s = 0.45
    A, B, C, D = (0, 0), (12 * s, 0), (12 * s, 9 * s), (0, 9 * s)
    E = (6 * s, 9 * s)
    poly(ax, [A, B, C, D], face="#e8f5e9", color=BLUE)
    poly(ax, [A, D, E], face="#f8c9a0", color=ORANGE, z=3)
    ax.plot([A[0], C[0]], [A[1], C[1]], lw=2.0, color=NEUTRAL, ls="--", zorder=4)
    for n, p, off in [("A", A, (-16, -14)), ("B", B, (8, -12)), ("C", C, (8, 4)),
                      ("D", D, (-16, 4)), ("E", E, (-4, 8))]:
        Pt(ax, n, p, *off)
    seg_label(ax, A, B, "12 m", side=-1, offset=0.32)
    seg_label(ax, B, C, "9 m", side=-1, offset=0.42)
    f16.txt(ax, 0.95, 3.0, "massif", color="#a04000", fs=11)
    f16.txt(ax, 3.9, 1.3, "allée", color=NEUTRAL, fs=11)
    save(fig, ax, out("s04_jardin"), (-0.9, 6.3), (-0.8, 4.8))
    fig, ax = new_fig(4.4, 4.8)
    f16.cylinder(ax, 0, 1.3, 2.4)
    ax.plot([0, 1.3], [2.4, 2.4], lw=1.6, color=ORANGE)
    ax.scatter([0], [2.4], s=20, color=ORANGE, zorder=5)
    f16.txt(ax, 0.65, 3.0, "0,8 m", fs=12)
    f16.txt(ax, 1.6, 1.2, "1,5 m", fs=12, ha="left")
    save(fig, ax, out("s04_citerne"), (-1.8, 2.8), (-0.7, 3.4))
    fig, ax = new_fig(7.4, 3.8)
    k = 0.75
    L, H = 5.2 * cos(radians(35)) * k, 5.2 * sin(radians(35)) * k
    G, Dr, Hs, Ft = (-L, 0), (L, 0), (0, H), (0, 0)
    poly(ax, [G, Dr, Hs], face="#fdebd0", color=ORANGE)
    ax.plot([Hs[0], Ft[0]], [Hs[1], Ft[1]], lw=1.6, color=BLUE, ls="--")
    right_angle(ax, Ft, (1, 0), (0, 1), size=0.2, color=BLUE)
    ax.add_patch(mp.Arc(G, 1.4, 1.4, theta1=0, theta2=35, color=DARK, lw=1.6))
    f16.txt(ax, G[0] + 0.95, 0.24, "35°", color=DARK, fs=11.5)
    seg_label(ax, G, Hs, "5,2 m", side=1, offset=0.35)
    Pt(ax, "G", G, -16, -12)
    Pt(ax, "D", Dr, 6, -12)
    Pt(ax, "S", Hs, -4, 8)
    Pt(ax, "F", Ft, 4, -16, BLUE)
    save(fig, ax, out("s04_toit"), (-L - 0.8, L + 0.8), (-0.7, H + 0.7))
    S.render(out("s04_script"), SCRIPTS["s04"])


# ---------------------------------------------------------------- sujet 05

def s05():
    graphe(out("s05_tarifs"),
           curves=[(lambda n: 15 * n, 0, 10, BLUE, ("A", 7.6)),
                   (lambda n: 20 + 10 * n, 0, 10, ORANGE, ("B", 9)),
                   (lambda n: 60, 0, 10, GREEN, ("C", 1.0))],
           xb=(-0.5, 10.6), yb=(-8, 165), xt=1, yt=10, w=8.4, h=6.0,
           xlabel="nombre de concerts", ylabel="prix (€)")
    barres(out("s05_frequentation"), ["Vendredi", "Samedi", "Dimanche"], [4200, 6800, 5400],
           ylabel="Nombre de spectateurs", w=7.2, h=4.6)


# ---------------------------------------------------------------- sujet 06

def s06():
    fig, ax = new_fig(6.8, 4.6)
    s = 0.06
    L, Pp, H = 80 * s, 35 * s, 40 * s
    V = f16.box(ax, L, Pp, H, names="ABCDEFGH", face="#cfe8fb")
    seg_label(ax, V["A"], V["B"], "80 cm", side=-1, offset=0.35)
    seg_label(ax, V["B"], V["F"], "35 cm", side=-1, offset=0.75)
    seg_label(ax, V["F"], V["G"], "40 cm", side=-1, offset=0.62)
    save(fig, ax, out("s06_aquarium"), (-0.8, 6.8), (-0.8, 3.7))
    S.render(out("s06_script"), SCRIPTS["s06"])


# ---------------------------------------------------------------- sujet 07

def s07():
    fig, ax = new_fig(6.6, 6.6)
    k = 0.1
    O = (0, 27 * k)
    R = 25 * k
    ax.plot([-3.4, 3.4], [0, 0], lw=1.8, color=NEUTRAL)
    ax.add_patch(mp.Circle(O, R, facecolor="none", edgecolor=BLUE, lw=2.4))
    Pb = (0, O[1] - R)
    M = (O[0] + R * sin(radians(60)), O[1] - R * cos(radians(60)))
    Hm = (0, M[1])
    ax.plot([O[0], Pb[0]], [O[1], Pb[1]], lw=1.8, color=DARK)
    ax.plot([O[0], M[0]], [O[1], M[1]], lw=1.8, color=DARK)
    ax.plot([M[0], Hm[0]], [M[1], Hm[1]], lw=1.4, color=ORANGE, ls="--")
    right_angle(ax, Hm, (1, 0), (0, 1), size=0.14, color=ORANGE)
    ax.add_patch(mp.Arc(O, 1.0, 1.0, theta1=-90, theta2=-30, color=ORANGE, lw=1.8))
    f16.txt(ax, O[0] + 0.32, O[1] - 0.72, "60°", color=ORANGE, fs=11.5)
    Pt(ax, "O", O, -16, 4)
    Pt(ax, "P", Pb, -16, -14)
    Pt(ax, "M", M, 8, -6, ORANGE)
    Pt(ax, "H", Hm, -18, -2, ORANGE)
    ax.annotate("", xy=(-3.0, O[1]), xytext=(-3.0, 0),
                arrowprops=dict(arrowstyle="<->", lw=1.2, color=DARK))
    ax.plot([-3.1, O[0]], [O[1], O[1]], lw=0.8, color=NEUTRAL, ls=":")
    f16.txt(ax, -3.15, O[1] / 2, "27 m", color=DARK, fs=11.5, ha="right")
    seg_label(ax, O, Pb, "25 m", side=-1, offset=0.38, t=0.25)
    f16.txt(ax, 2.6, 0.25, "sol", color=NEUTRAL, fs=11)
    save(fig, ax, out("s07_roue"), (-4.3, 3.4), (-0.4, 5.6))
    graphe(out("s07_grand_huit"), curves=[(lambda t: -0.5 * t * t + 6 * t + 2, 0, 12, BLUE)],
           xb=(-0.5, 12.8), yb=(-1.2, 23), xt=1, yt=2, w=8.4, h=5.8,
           xlabel="temps (s)", ylabel="hauteur (m)")
    table_fig(out("s07_attente"), [["Attente (min)", "5", "10", "15", "20", "30"],
                                   ["Effectif", "3", "6", "8", "5", "3"]], w0=2.1)


# ---------------------------------------------------------------- sujet 08

def s08():
    fig, ax = new_fig(5.0, 5.2)
    k = 3
    A, B, C = (0, 1.2 * k), (0, 0), (0.9 * k, 0)
    poly(ax, [A, B, C])
    right_angle(ax, B, (1, 0), (0, 1), size=0.22)
    Pt(ax, "A", A, -16, 4)
    Pt(ax, "B", B, -16, -14)
    Pt(ax, "C", C, 6, -14)
    seg_label(ax, A, B, "1,2 km", side=1, offset=0.55)
    seg_label(ax, B, C, "0,9 km", side=-1, offset=0.3)
    ax.annotate("", xy=(1.9, 0.9), xytext=(1.2, 1.85),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=ORANGE))
    f16.txt(ax, 1.75, 1.55, "sens\nde course", color=ORANGE, fs=10, ha="left")
    save(fig, ax, out("s08_parcours"), (-1.4, 3.6), (-0.8, 4.2))
    S.render(out("s08_script"), SCRIPTS["s08"])


# ---------------------------------------------------------------- sujet 09

def s09():
    fig, ax = new_fig(6.4, 3.8)
    k = 1.0
    Pg = (0, 0)
    Rf = (4.5 * cos(radians(30)) * k, 4.5 * sin(radians(30)) * k)
    Hf = (Rf[0], 0)
    poly(ax, [Pg, Hf, Rf], face="#fff4e6", color=NEUTRAL, lw=1.6)
    ax.plot([Pg[0], Rf[0]], [Pg[1], Rf[1]], lw=5, color="#1f4e79", solid_capstyle="butt")
    right_angle(ax, Hf, (-1, 0), (0, 1), size=0.2)
    ax.add_patch(mp.Arc(Pg, 1.3, 1.3, theta1=0, theta2=30, color=ORANGE, lw=1.8))
    f16.txt(ax, 0.9, 0.2, "30°", color=ORANGE, fs=11.5)
    seg_label(ax, Pg, Rf, "panneaux : 4,5 m", side=1, offset=0.62, color="#1f4e79")
    Pt(ax, "P", Pg, -16, -12)
    Pt(ax, "R", Rf, 6, 4)
    Pt(ax, "H", Hf, 6, -14)
    save(fig, ax, out("s09_toit"), (-0.8, 4.8), (-0.6, 2.9))
    graphe(out("s09_offres"),
           curves=[(lambda x: 12 + 0.22 * x, 0, 400, BLUE, ("A", 330)),
                   (lambda x: 18 + 0.19 * x, 0, 400, ORANGE, ("B", 360))],
           xb=(-15, 420), yb=(-5, 110), xt=50, yt=10, w=8.4, h=5.8,
           xlabel="consommation (kWh)", ylabel="facture (€)")
    fig, ax = new_fig(3.8, 5.6)
    f16.cylinder(ax, 0, 0.75, 3.6)
    ax.plot([0, 0.75], [3.6, 3.6], lw=1.6, color=ORANGE)
    ax.scatter([0], [3.6], s=20, color=ORANGE, zorder=5)
    f16.txt(ax, 0.4, 4.15, "0,25 m", fs=11.5)
    f16.txt(ax, 1.0, 1.8, "1,2 m", fs=12, ha="left")
    save(fig, ax, out("s09_ballon"), (-1.2, 2.0), (-0.5, 4.5))
    mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov",
            "Déc"]
    barres(out("s09_conso"), mois, [420, 380, 330, 260, 200, 150, 140, 130, 180, 270, 350, 410],
           ylabel="Consommation (kWh)", w=10.0, h=4.8)


# ---------------------------------------------------------------- sujet 10

def s10():
    fig, ax = new_fig(8.4, 4.2)
    Pp, Sm = (0, 0), (0, 3.0)
    B1, B2 = (-9.0, 0), (-5.0, 0)
    ax.plot([-10, 0.8], [0, 0], lw=1.6, color="#5dade2")
    ax.add_patch(mp.Rectangle((-0.25, 0), 0.5, 3.0, facecolor="#f2f3f4", edgecolor=DARK, lw=1.6))
    for i in range(3):
        ax.add_patch(mp.Rectangle((-0.25, 0.5 + i * 0.9), 0.5, 0.35, facecolor="#e74c3c",
                                  edgecolor="none"))
    for B, a in [(B1, "8°"), (B2, "15°")]:
        ax.plot([B[0], Sm[0]], [B[1], Sm[1]], lw=1.6, color=ORANGE, ls="--")
        ang = np.degrees(np.arctan2(Sm[1], -B[0]))
        ax.add_patch(mp.Arc(B, 2.2, 2.2, theta1=0, theta2=ang, color=ORANGE, lw=1.6))
        f16.txt(ax, B[0] + 1.45, 0.17, a, color=ORANGE, fs=11)
    Pt(ax, "A", B1, -6, -18)
    Pt(ax, "B", B2, -6, -18)
    Pt(ax, "P", Pp, 8, -14)
    Pt(ax, "S", Sm, 8, 2)
    f16.txt(ax, 0.45, 1.5, "45 m", color=DARK, fs=11.5, ha="left")
    f16.txt(ax, -5.0, 2.6, "(figure non à l'échelle)", color=NEUTRAL, fs=10, weight="normal")
    save(fig, ax, out("s10_phare"), (-10.2, 1.8), (-0.9, 3.6))
    fig, ax = new_fig(4.6, 5.6)
    k = 0.6
    Mp, T, Bm = (0, 0), (0, 6 * k), (4 * k, 0)
    poly(ax, [Mp, T, Bm], face="#fdfefe", color=BLUE)
    ax.plot([0, 0], [-0.3, 6 * k + 0.3], lw=3.2, color=DARK)
    right_angle(ax, Mp, (1, 0), (0, 1), size=0.2)
    Pt(ax, "M", Mp, -18, -12)
    Pt(ax, "T", T, -16, 4)
    Pt(ax, "B", Bm, 6, -12)
    seg_label(ax, Mp, T, "6 m", side=1, offset=0.5)
    seg_label(ax, Mp, Bm, "4 m", side=-1, offset=0.3)
    save(fig, ax, out("s10_voile"), (-1.2, 3.4), (-0.8, 4.3))
    graphe(out("s10_marees"), curves=[(lambda t: 3.5 + 2.5 * cos(pi * t / 6), 0, 12, BLUE)],
           xb=(-0.5, 12.8), yb=(-0.4, 6.9), xt=1, yt=0.5, w=8.4, h=5.6,
           xlabel="heure (h)", ylabel="hauteur d'eau (m)")


if __name__ == "__main__":
    for f in (s01, s02, s03, s04, s05, s06, s07, s08, s09, s10):
        f()
    print("Figures brevet : OK")
