# -*- coding: utf-8 -*-
"""Figures : Seconde — Algorithmique (variables, instructions, fonctions)."""
import numpy as np
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, LBLUE, LGREEN, LORANGE

CODE_BG = "#2c3e50"
MONO = dict(family="monospace")


def ligne_code(ax, x, y, w, s, h=0.62, fs=13):
    ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h, boxstyle="round,pad=0.05", fc=CODE_BG, ec="none"))
    ax.text(x + 0.18, y, s, color="#ecf0f1", fontsize=fs, va="center", ha="left", **MONO)


def case(ax, x, y, nom, val, neuf=False, w=1.3, h=0.9):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.04",
                                fc=LGREEN if neuf else LBLUE, ec=GREEN if neuf else BLUE, lw=2))
    txt(ax, x, y, val, DARK, 16, ha="center", va="center", fontweight="bold")
    ax.text(x, y + h / 2 + 0.12, nom, color=DARK, fontsize=13, ha="center", va="bottom", **MONO)


def variables():
    fig, ax = new_fig(10.6, 3.6)
    etapes = [("a = 5", [("a", "5", True)]),
              ("b = 2 * a", [("a", "5", False), ("b", "10", True)]),
              ("a = a + 3", [("a", "8", True), ("b", "10", False)])]
    for k, (code, cases) in enumerate(etapes):
        x0 = k * 3.9
        ligne_code(ax, x0, 2.2, 3.1, code)
        for j, (nom, val, neuf) in enumerate(cases):
            case(ax, x0 + 0.85 + 1.5 * j, 0.6, nom, val, neuf)
        if k < 2:
            ax.annotate("", xy=(x0 + 3.65, 1.0), xytext=(x0 + 3.25, 1.0),
                        arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.6, mutation_scale=16))
    txt(ax, 5.4, -0.5, "« a = a + 3 » : on calcule a + 3 avec l’ancienne valeur, puis on range le résultat dans a",
        DARK, 12, ha="center", va="top")
    ax.set_xlim(-0.3, 11.2)
    ax.set_ylim(-1.2, 2.8)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("2nd_algo_variables.png"))


def organigramme():
    fig, ax = new_fig(8.4, 5.4)
    ax.add_patch(FancyBboxPatch((-1.6, 3.6), 3.2, 0.8, boxstyle="round,pad=0.1", fc=LBLUE, ec=BLUE, lw=2))
    ax.text(0, 4.0, "age = 15", ha="center", va="center", fontsize=13, color=DARK, **MONO)
    ax.annotate("", xy=(0, 2.95), xytext=(0, 3.5), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.6))
    ax.add_patch(Polygon([(0, 2.9), (2.2, 2.0), (0, 1.1), (-2.2, 2.0)], closed=True, fc=LORANGE, ec=ORANGE, lw=2))
    ax.text(0, 2.0, "age >= 18 ?", ha="center", va="center", fontsize=13, color=DARK, **MONO)
    for s, lab, col, texte in ((-1, "Vrai", GREEN, 'print("majeur")'), (1, "Faux", RED, 'print("mineur")')):
        ax.plot([s * 2.2, s * 3.6], [2.0, 2.0], color=NEUTRAL, lw=1.6)
        ax.annotate("", xy=(s * 3.6, 0.75), xytext=(s * 3.6, 2.0), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL,
                                                                                 lw=1.6))
        txt(ax, s * 2.9, 2.15, lab, col, 13, ha="center", va="bottom", fontweight="bold")
        ax.add_patch(FancyBboxPatch((s * 3.6 - 1.75, -0.05), 3.5, 0.75, boxstyle="round,pad=0.08",
                                    fc=LGREEN if s < 0 else "#fdecea", ec=col, lw=2))
        ax.text(s * 3.6, 0.32, texte, ha="center", va="center", fontsize=12.5, color=DARK, **MONO)
    txt(ax, 0, -0.9, "ici la condition est fausse : le programme affiche « mineur »", DARK, 12.5, ha="center",
        va="top")
    ax.set_xlim(-5.6, 5.6)
    ax.set_ylim(-1.5, 4.7)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("2nd_algo_organigramme.png"))


def trace():
    fig, ax = new_fig(9.6, 3.4)
    lignes = ["s = 0", "for i in range(1, 5):", "    s = s + i", "print(s)"]
    for k, l in enumerate(lignes):
        ligne_code(ax, 0, 2.4 - 0.72 * k, 3.6, l, fs=12)
    cols = ["", "début", "i = 1", "i = 2", "i = 3", "i = 4"]
    vals_i = ["i", "", "1", "2", "3", "4"]
    vals_s = ["s", "0", "1", "3", "6", "10"]
    x0, w, h = 4.4, 0.95, 0.72
    for j in range(6):
        for r, (vals, fc) in enumerate(((vals_i, "white"), (vals_s, "white"))):
            y = 1.9 - r * h
            fcj = "#ecf0f1" if j == 0 else (LGREEN if (r == 1 and j == 5) else fc)
            ax.add_patch(Rectangle((x0 + j * w, y - h / 2), w, h, fc=fcj, ec=NEUTRAL, lw=1))
            ax.text(x0 + j * w + w / 2, y, vals[j], ha="center", va="center", fontsize=14,
                    color=GREEN if (r == 1 and j == 5) else DARK, fontweight="bold" if j == 0 or j == 5 else "normal",
                    **MONO)
        if j > 0:
            txt(ax, x0 + j * w + w / 2, 1.9 + h / 2 + 0.12, cols[j], NEUTRAL, 10.5, ha="center", va="bottom")
    txt(ax, x0 + 3 * w, 0.4, "affichage : 10", GREEN, 13, ha="center", va="top", fontweight="bold")
    txt(ax, x0 + 3 * w, 2.75, "tableau de suivi", DARK, 12.5, ha="center", va="bottom", fontweight="bold")
    ax.set_xlim(-0.3, 10.3)
    ax.set_ylim(-0.4, 3.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("2nd_algo_trace.png"))


def machine():
    fig, ax = new_fig(9.6, 3.2)
    ax.add_patch(FancyBboxPatch((-0.8, 0.45), 1.6, 0.9, boxstyle="round,pad=0.06", fc=LBLUE, ec=BLUE, lw=2))
    txt(ax, 0, 0.9, "$4$", BLUE, 18, ha="center", va="center", fontweight="bold")
    txt(ax, 0, 1.6, "argument", BLUE, 12, ha="center", va="bottom")
    ax.annotate("", xy=(1.75, 0.9), xytext=(0.95, 0.9), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.8,
                                                                      mutation_scale=18))
    ax.add_patch(FancyBboxPatch((1.9, -0.1), 4.6, 2.0, boxstyle="round,pad=0.1", fc=CODE_BG, ec="none"))
    for k, l in enumerate(["def f(x):", "    y = 3 * x + 2", "    return y"]):
        ax.text(2.1, 1.5 - 0.55 * k, l, color="#ecf0f1", fontsize=13, va="center", **MONO)
    ax.annotate("", xy=(7.45, 0.9), xytext=(6.65, 0.9), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.8,
                                                                      mutation_scale=18))
    ax.add_patch(FancyBboxPatch((7.6, 0.45), 1.6, 0.9, boxstyle="round,pad=0.06", fc=LGREEN, ec=GREEN, lw=2))
    txt(ax, 8.4, 0.9, "$14$", GREEN, 18, ha="center", va="center", fontweight="bold")
    txt(ax, 8.4, 1.6, "valeur renvoyée", GREEN, 12, ha="center", va="bottom")
    ax.text(4.2, -0.65, "f(4) renvoie 3 * 4 + 2 = 14", ha="center", va="top", fontsize=13, color=DARK, **MONO)
    ax.set_xlim(-1.1, 9.5)
    ax.set_ylim(-1.3, 2.3)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("2nd_algofct_machine.png"))


def simulation():
    rng = np.random.default_rng(11)
    n = 1200
    d = rng.integers(1, 7, n)
    freq = np.array([(d == k).mean() for k in range(1, 7)])
    fig, ax = new_fig(7.6, 4.2)
    ax.bar(range(1, 7), freq, color=BLUE, width=0.6, zorder=3)
    ax.axhline(1 / 6, color=RED, lw=1.6, ls="--", zorder=4)
    for k, f in zip(range(1, 7), freq):
        txt(ax, k, 0.08, f"{f:.3f}".replace(".", ","), "white", 12, ha="center", va="center", fontweight="bold",
            zorder=5)
    txt(ax, 6.45, 0.222, "en pointillés : $p = \\frac{1}{6} \\approx 0{,}167$", RED, 12.5, ha="right", va="center")
    ax.set_xticks(range(1, 7))
    ax.set_ylim(0, 0.25)
    ax.set_yticks([0, 0.05, 0.1, 0.15, 0.2, 0.25])
    ax.set_yticklabels(["0", "0,05", "0,1", "0,15", "0,2", "0,25"])
    ax.set_xlabel("face obtenue", fontsize=12, color=DARK)
    ax.set_ylabel("fréquence", fontsize=12, color=DARK)
    ax.grid(axis="y", color="#d5dde3", lw=0.7, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title(f"{n} lancers simulés avec randint(1, 6)", fontsize=12.5, color=DARK)
    _save(fig, I("2nd_algofct_simulation.png"))


variables()
organigramme()
trace()
machine()
simulation()
