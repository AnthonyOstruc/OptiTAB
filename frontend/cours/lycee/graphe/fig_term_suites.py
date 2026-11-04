# -*- coding: utf-8 -*-
"""Figures : Terminale — Suites (récurrence, limites)."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import Affine2D

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE, LBLUE, LGREEN

GRID = "#d5dde3"
VIRGULE = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))


def recurrence():
    fig, ax = new_fig(11.0, 3.6)
    ax.plot([-0.5, 12.2], [0, 0], color=NEUTRAL, lw=1.5)
    for k in range(8):
        x0 = 0.4 + 1.5 * k
        ang = -28 if k < 3 else 0
        col = GREEN if k == 0 else (BLUE if k < 3 else "#aab7c4")
        r = Rectangle((x0, 0), 0.35, 2.0, fc=col, ec=DARK, lw=1.2)
        r.set_transform(Affine2D().rotate_deg_around(x0 + 0.35, 0, ang) + ax.transData)
        ax.add_patch(r)
        lab = ["$P(n_0)$", "$P(n_0+1)$", "$P(n_0+2)$", "", "", "$P(n)$", "$P(n+1)$", "…"][k]
        txt(ax, x0 + 0.18, -0.3, lab, DARK, 11.5, ha="center", va="top")
    txt(ax, 0.6, 2.75, "initialisation :\n$P(n_0)$ est vraie", GREEN, 12, ha="left", va="center", fontweight="bold")
    ax.annotate("", xy=(9.4 + 0.18, 2.35), xytext=(7.9 + 0.18, 2.35),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2, mutation_scale=18))
    txt(ax, 8.7, 2.75, "hérédité : si $P(n)$ est vraie,\nalors $P(n+1)$ est vraie", BLUE, 12, ha="center",
        va="bottom", fontweight="bold")
    ax.set_xlim(-0.6, 12.4)
    ax.set_ylim(-1.0, 3.7)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_suites_recurrence.png"))


def convergence():
    fig, ax = new_fig(8.4, 4.4)
    n = np.arange(0, 31)
    u = 2 + 2 * (-0.82) ** n
    eps = 0.3
    ax.axhspan(2 - eps, 2 + eps, color="#e8f5e9", zorder=0)
    ax.axhline(2, color=RED, lw=1.6, ls="--")
    ax.axhline(2 + eps, color=GREEN, lw=1)
    ax.axhline(2 - eps, color=GREEN, lw=1)
    rang = next(k for k in n if all(abs(u[j] - 2) < eps for j in range(k, 31)))
    ax.scatter(n[n < rang], u[n < rang], s=26, color=ORANGE, zorder=5)
    ax.scatter(n[n >= rang], u[n >= rang], s=26, color=BLUE, zorder=5)
    ax.axvline(rang - 0.5, color=NEUTRAL, lw=1, ls=":")
    txt(ax, rang - 0.3, 3.75, f"à partir du rang {rang}, tous les termes\nsont dans l’intervalle autour de $\\ell$",
        DARK, 11.5, va="top")
    txt(ax, 30.5, 2 + eps + 0.05, "$\\ell + \\varepsilon$", GREEN, 12, ha="right", va="bottom")
    txt(ax, 30.5, 2 - eps - 0.05, "$\\ell - \\varepsilon$", GREEN, 12, ha="right", va="top")
    txt(ax, -0.8, 2, "$\\ell = 2$", RED, 13, ha="right", va="center", fontweight="bold")
    ax.set_xlim(-0.5, 31)
    ax.set_ylim(0, 4.2)
    ax.set_xlabel("$n$", fontsize=13, color=DARK)
    ax.set_yticks([0, 1, 3, 4])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _save(fig, I("term_suites_convergence.png"))


def gendarmes():
    fig, ax = new_fig(8.4, 4.4)
    n = np.arange(1, 41)
    v, w = 1 - 1 / n, 1 + 1 / n
    u = 1 + np.sin(n) / n
    ax.plot(n, w, color=ORANGE, lw=1.6, marker="o", ms=3.5, label="w")
    ax.plot(n, v, color=GREEN, lw=1.6, marker="o", ms=3.5)
    ax.scatter(n, u, s=26, color=BLUE, zorder=5)
    ax.axhline(1, color=RED, lw=1.4, ls="--")
    txt(ax, 40.5, 1.06, "$w_n = 1 + \\frac{1}{n}$", ORANGE, 12.5, va="bottom")
    txt(ax, 40.5, 0.94, "$v_n = 1 - \\frac{1}{n}$", GREEN, 12.5, va="top")
    txt(ax, 12, 1.45, "$v_n \\leq u_n = 1 + \\frac{\\sin n}{n} \\leq w_n$", BLUE, 13, ha="left")
    txt(ax, 25, 0.62, "$v_n$ et $w_n$ tendent vers $1$, donc $u_n$ aussi", DARK, 12.5, ha="center")
    ax.yaxis.set_major_formatter(VIRGULE)
    ax.set_xlim(0, 47)
    ax.set_ylim(0.4, 2.1)
    ax.set_xlabel("$n$", fontsize=13, color=DARK)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _save(fig, I("term_suites_gendarmes.png"))


def qn():
    fig, axs = plt.subplots(1, 4, figsize=(12.4, 3.8))
    fig.patch.set_facecolor("white")
    cas = [(1.2, "$q > 1$ : $+\\infty$", BLUE), (0.8, "$0 < q < 1$ : $0$", GREEN), (-0.8, "$-1 < q < 0$ : $0$", ORANGE),
           (-1.2, "$q \\leq -1$ : pas de limite", RED)]
    n = np.arange(0, 16)
    for ax, (q, titre, col) in zip(axs, cas):
        y = q ** n
        ax.axhline(0, color=NEUTRAL, lw=1)
        ax.scatter(n, y, s=18, color=col, zorder=5)
        ax.set_title(titre, fontsize=12.5, color=col)
        ax.set_ylim(-16, 16) if abs(q) > 1 else ax.set_ylim(-1.1, 1.1)
        ax.set_xticks([0, 5, 10, 15])
        ax.tick_params(labelsize=10)
        ax.yaxis.set_major_formatter(VIRGULE)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.text(0.97, 0.05, f"$q = {q:g}$".replace(".", "{,}"), transform=ax.transAxes, ha="right", fontsize=11,
                color=DARK)
    fig.tight_layout()
    _save(fig, I("term_suites_qn.png"))


recurrence()
convergence()
gendarmes()
qn()
