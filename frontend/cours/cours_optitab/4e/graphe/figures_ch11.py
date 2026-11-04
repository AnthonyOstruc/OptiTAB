# -*- coding: utf-8 -*-
"""Figures du chapitre 11 (probabilités) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, tableau, barres, graphe, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                   DIR_COURS, DIR_EXOS)
import numpy as np
from matplotlib.patches import Wedge, Circle, Rectangle, Polygon, FancyArrowPatch

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
RED, YEL, PURP = "#e74c3c", "#f1c40f", "#8e44ad"


def echelle(path, events=(), titre=None):
    fig, ax = new_fig(10.5, 3.2 if events else 2.4)
    ax.add_patch(Rectangle((0, -0.12), 10, 0.24, facecolor="#e8f4fd", edgecolor=BLUE, lw=1.5))
    for v, t in [(0, "0\nimpossible"), (2.5, "0,25\npeu probable"), (5, "0,5\nune chance sur deux"),
                 (7.5, "0,75\ntrès probable"), (10, "1\ncertain")]:
        ax.plot([v, v], [-0.2, 0.2], lw=2, color=DARK)
        ax.text(v, -0.32, t, ha="center", va="top", fontsize=12.5, color=DARK)
    for i, (lab, p, col) in enumerate(events):
        y = 0.45 + (i % 2) * 0.55
        ax.plot([10 * p, 10 * p], [0.15, y - 0.05], lw=1.2, color=col)
        ax.scatter([10 * p], [0], s=70, color=col, zorder=5)
        ax.text(10 * p, y, lab, ha="center", va="bottom", fontsize=14, color=col, fontweight="bold")
    if titre:
        ax.text(5, 1.0, titre, ha="center", fontsize=12.5, color=DARK, fontweight="bold")
    ax.set_xlim(-0.8, 10.8)
    ax.set_ylim(-1.3, 1.7 if events else 1.3)
    ax.axis("off")
    _save(fig, path)


echelle(C("probabilites_4e_echelle.png"), titre="L'échelle des probabilités")
echelle(X("probabilites_4e_echelle_solution.png"),
        [("A", 0, RED), ("C", 1 / 6, ORANGE), ("F", 1 / 3, PURP), ("B", 0.5, BLUE),
         ("E", 5 / 6, GREEN), ("D", 1, DARK)])


def urne(path, boules, titre=None):
    """boules = [(couleur, nombre, nom)]"""
    fig, ax = new_fig(6.0, 5.2)
    ax.add_patch(Polygon([(0, 4.2), (0.3, 0), (4.7, 0), (5, 4.2)], closed=True, facecolor="#f4f6f7",
                         edgecolor=DARK, lw=2.2))
    pts = []
    for row in range(5):
        for k in range(5):
            pts.append((0.8 + k * 0.8 + (0.2 if row % 2 else 0), 0.55 + row * 0.72))
    i = 0
    for col, n, _ in boules:
        for _ in range(n):
            x, y = pts[i]
            ax.add_patch(Circle((x, y), 0.32, facecolor=col, edgecolor=DARK, lw=1.2))
            i += 1
    leg = " ; ".join(f"{n} {nom}" for _, n, nom in boules)
    ax.text(2.5, -0.5, leg, ha="center", va="top", fontsize=12, color=DARK, fontweight="bold")
    if titre:
        ax.text(2.5, 4.55, titre, ha="center", fontsize=12.5, color=DARK, fontweight="bold")
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-1.2, 5.0)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


urne(C("probabilites_4e_urne.png"), [(RED, 5, "rouges"), (BLUE, 3, "bleues"), (GREEN, 2, "vertes")])
urne(X("probabilites_4e_urne_ex.png"), [(RED, 5, "rouges"), (BLUE, 3, "bleues"), (GREEN, 2, "vertes")])

# simulation : fréquence d'apparition du 6
rng = np.random.default_rng(4)
lancers = rng.integers(1, 7, 2000)
freq = np.cumsum(lancers == 6) / np.arange(1, 2001)


def sim(ax):
    ax.plot(np.arange(1, 2001), freq, lw=1.8, color=BLUE)
    ax.axhline(1 / 6, color=ORANGE, lw=1.6, ls="--")
    ax.text(1990, 1 / 6 + 0.012, "probabilité $\\frac{1}{6} \\approx 0{,}167$", color=ORANGE,
            fontsize=12, ha="right", fontweight="bold")


graphe(C("probabilites_4e_frequences.png"), curves=[], extra=sim, xb=(-40, 2080), yb=(-0.02, 0.42),
       xt=250, yt=0.05, xlabel="nombre de lancers", ylabel="fréquence du 6", w=8.6, h=4.8)


def deux_des(path, cible=None, titre=None):
    lignes = [["+", "1", "2", "3", "4", "5", "6"]]
    for a in range(1, 7):
        lignes.append([str(a)] + [str(a + b) for b in range(1, 7)])
    vert = []
    if cible is not None:
        vert = [(a, b) for a in range(1, 7) for b in range(1, 7) if cible(a + b, a, b)]
    tableau(path, lignes, larg_col=[1.0] * 7, haut=0.62, vert=vert, titre=titre)


deux_des(C("probabilites_4e_deux_des.png"), titre="Somme de deux dés : 36 issues équiprobables")
deux_des(X("probabilites_4e_deux_des_solution.png"), cible=lambda s, a, b: s == 7,
         titre="Somme égale à 7 : 6 cases sur 36")


def roue(path, secteurs, numeros=True, titre=None):
    """secteurs = [(angle, couleur, étiquette)]"""
    fig, ax = new_fig(5.8, 5.6)
    a = 90.0
    for i, (ang, col, lab) in enumerate(secteurs):
        ax.add_patch(Wedge((0, 0), 2, a - ang, a, facecolor=col, edgecolor="white", lw=2.5))
        am = np.radians(a - ang / 2)
        if lab:
            ax.text(1.3 * np.cos(am), 1.3 * np.sin(am), lab, ha="center", va="center", fontsize=14,
                    color="white" if col not in (YEL,) else DARK, fontweight="bold")
        a -= ang
    ax.add_patch(Circle((0, 0), 0.12, facecolor=DARK))
    ax.add_patch(Polygon([(-0.15, 2.35), (0.15, 2.35), (0, 1.95)], closed=True, facecolor=DARK))
    if titre:
        ax.text(0, -2.5, titre, ha="center", va="top", fontsize=12, color=DARK)
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.9 if titre else -2.3, 2.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


cols8 = [RED, BLUE, RED, YEL, GREEN, RED, BLUE, YEL]
roue(X("probabilites_4e_roue8.png"), [(45, c, str(i + 1)) for i, c in enumerate(cols8)])
roue(X("probabilites_4e_roue_angles.png"),
     [(180, RED, "180°"), (90, BLUE, "90°"), (60, GREEN, "60°"), (30, YEL, "30°")])


def simulation_piece(ax):
    xs = [10, 100, 1000, 10000]
    fs = [0.7, 0.56, 0.512, 0.4985]
    ax.scatter(np.log10(xs), fs, s=70, color=BLUE, zorder=5)
    ax.plot(np.log10(xs), fs, lw=1.6, color=BLUE)
    ax.axhline(0.5, color=ORANGE, lw=1.6, ls="--")
    for x, f in zip(xs, fs):
        ax.annotate(f"{f:g}".replace(".", ","), (np.log10(x), f), textcoords="offset points",
                    xytext=(-30, 12) if x == 10000 else (8, 6), fontsize=11.5, color=BLUE,
                    fontweight="bold")


def piece(path):
    import matplotlib.pyplot as plt
    fig, ax = new_fig(8.0, 4.4)
    simulation_piece(ax)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(["10", "100", "1 000", "10 000"], fontsize=11.5)
    ax.set_xlabel("nombre de lancers (échelle des puissances de 10)", fontsize=11.5, color=DARK)
    ax.set_ylabel("fréquence de « pile »", fontsize=11.5, color=DARK)
    ax.set_ylim(0.4, 0.75)
    ax.set_xlim(0.7, 4.4)
    ax.grid(True, color="#d5dde3", lw=0.7)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.text(0.75, 0.488, "probabilité 0,5", color=ORANGE, fontsize=11.5, va="top", ha="left")
    _save(fig, path)


piece(X("probabilites_4e_piece.png"))

tableau(X("probabilites_4e_deux_pieces_solution.png"),
        [["2e pièce →\n1re pièce ↓", "Pile", "Face"], ["Pile", "PP", "PF"], ["Face", "FP", "FF"]],
        larg_col=[2.6, 1.6, 1.6], haut=0.75, vert=[(1, 2), (2, 1)],
        titre="4 issues équiprobables ; « exactement un pile » : PF et FP")
tableau(X("probabilites_4e_lancers.png"),
        [["Face", "1", "2", "3", "4", "5", "6", "Total"],
         ["Effectif", "95", "103", "98", "107", "96", "101", "600"]],
        larg_col=[1.8] + [1.05] * 6 + [1.4])


def urnes3(path):
    fig, ax = new_fig(10.0, 3.8)
    data = [("urne A", 3, 2), ("urne B", 5, 4), ("urne C", 8, 7)]
    for k, (nom, r, n) in enumerate(data):
        x0 = k * 3.6
        ax.add_patch(Polygon([(x0, 3.0), (x0 + 0.2, 0), (x0 + 2.8, 0), (x0 + 3.0, 3.0)], closed=True,
                             facecolor="#f4f6f7", edgecolor=DARK, lw=2))
        cols = [RED] * r + [DARK] * n
        for i, c in enumerate(cols):
            row, kk = divmod(i, 5)
            ax.add_patch(Circle((x0 + 0.55 + kk * 0.48, 0.38 + row * 0.5), 0.2, facecolor=c,
                                edgecolor=DARK, lw=1))
        ax.text(x0 + 1.5, -0.3, f"{nom}\n{r} rouges, {n} noires", ha="center", va="top",
                fontsize=12, color=DARK, fontweight="bold")
    ax.set_xlim(-0.3, 10.5)
    ax.set_ylim(-1.4, 3.3)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


urnes3(X("probabilites_4e_urnes.png"))
barres(X("probabilites_4e_de_truque.png"), ["1", "2", "3", "4", "5", "6"], [60, 65, 70, 75, 80, 150],
       ylabel="Effectif (sur 500 lancers)", w=8.0, h=4.4, highlight=5)
tableau(X("probabilites_4e_college.png"),
        [["", "Demi-pensionnaires", "Externes", "Total"], ["Filles", "40", "24", "64"],
         ["Garçons", "35", "21", "56"], ["Total", "75", "45", "120"]],
        larg_col=[1.8, 3.2, 1.8, 1.4], haut=0.66)
tableau(X("probabilites_4e_pfc_solution.png"),
        [["Ana ↓  Ben →", "pierre", "feuille", "ciseaux"],
         ["pierre", "égalité", "Ben", "Ana"], ["feuille", "Ana", "égalité", "Ben"],
         ["ciseaux", "Ben", "Ana", "égalité"]], larg_col=[2.4, 1.7, 1.7, 1.7], haut=0.66,
        vert=[(1, 3), (2, 1), (3, 2)], titre="9 issues : Ana gagne dans 3 cases (en vert)")


def cible(path):
    fig, ax = new_fig(5.6, 5.6)
    ax.add_patch(Rectangle((-20, -20), 40, 40, facecolor="#fdebd0", edgecolor=DARK, lw=2))
    ax.add_patch(Circle((0, 0), 20, facecolor="#d6eafc", edgecolor=BLUE, lw=2))
    ax.add_patch(Circle((0, 0), 10, facecolor=RED, edgecolor=DARK, lw=2, alpha=0.85))
    ax.plot([0, 10], [0, 0], lw=1.6, color="white")
    ax.text(5, 1.2, "10 cm", ha="center", fontsize=11, color="white", fontweight="bold")
    ax.plot([0, 0], [0, -20], lw=1.4, color=BLUE, ls="--")
    ax.text(1.0, -15, "20 cm", fontsize=11, color=BLUE, fontweight="bold")
    ax.text(0, -22.5, "carré de 40 cm de côté", ha="center", va="top", fontsize=12, color=DARK)
    ax.set_xlim(-21, 21)
    ax.set_ylim(-26, 21)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


cible(X("probabilites_4e_cible.png"))
deux_des(X("probabilites_4e_somme10_solution.png"), cible=lambda s, a, b: s >= 10,
         titre="Somme au moins égale à 10 : 6 cases sur 36")
