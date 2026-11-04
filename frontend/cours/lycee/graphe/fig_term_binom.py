# -*- coding: utf-8 -*-
"""Figures : Terminale — Loi binomiale."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from scipy.stats import binom

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED

GRID = "#d5dde3"
VIRGULE = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))


def style(ax):
    ax.grid(axis="y", color=GRID, lw=0.7, zorder=0)
    ax.yaxis.set_major_formatter(VIRGULE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def diagramme():
    fig, ax = new_fig(8.4, 4.4)
    k = np.arange(0, 11)
    p = binom.pmf(k, 10, 0.3)
    cols = [GREEN if v == 3 else BLUE for v in k]
    ax.bar(k, p, width=0.55, color=cols, zorder=3)
    ax.axvline(3, color=RED, lw=1.4, ls="--", zorder=4)
    txt(ax, 3.25, 0.285, "$E(X) = np = 3$", RED, 12.5, va="bottom")
    txt(ax, 6.5, 0.2, "$P(X = 3) = \\binom{10}{3}\\,0{,}3^3\\,0{,}7^7 \\approx 0{,}267$", GREEN, 13, ha="center")
    ax.set_xticks(k)
    ax.set_ylim(0, 0.32)
    ax.set_xlabel("$k$", fontsize=13, color=DARK)
    ax.set_ylabel("$P(X = k)$", fontsize=12, color=DARK)
    ax.set_title("loi binomiale $\\mathcal{B}(10\\,;0{,}3)$", fontsize=13, color=DARK)
    style(ax)
    _save(fig, I("term_binom_diagramme.png"))


def formes():
    fig, axs = plt.subplots(1, 3, figsize=(12.0, 3.6), sharey=True)
    fig.patch.set_facecolor("white")
    k = np.arange(0, 21)
    for ax, p, col in zip(axs, (0.2, 0.5, 0.8), (ORANGE, BLUE, GREEN)):
        ax.bar(k, binom.pmf(k, 20, p), width=0.6, color=col, zorder=3)
        ax.axvline(20 * p, color=RED, lw=1.2, ls="--", zorder=4)
        ax.set_title(f"$\\mathcal{{B}}(20\\,;{p:g})$ : $E = {20 * p:g}$".replace(".", "{,}"), fontsize=12.5, color=col)
        ax.set_xticks([0, 5, 10, 15, 20])
        style(ax)
    fig.tight_layout()
    _save(fig, I("term_binom_formes.png"))


def cumul():
    fig, ax = new_fig(8.4, 4.4)
    k = np.arange(0, 11)
    F = binom.cdf(k, 10, 0.3)
    cols = [GREEN if v == 5 else BLUE for v in k]
    ax.bar(k, F, width=0.55, color=cols, zorder=3)
    ax.axhline(0.95, color=RED, lw=1.5, ls="--", zorder=4)
    txt(ax, -0.45, 0.965, "$0{,}95$", RED, 12.5, ha="left", va="bottom")
    txt(ax, 5, F[5] + 0.03, "$0{,}953$", GREEN, 12, ha="center", va="bottom", fontweight="bold")
    txt(ax, 1.2, 0.62, "plus petit $k$ tel que\n$P(X \\leq k) \\geq 0{,}95$ : $k = 5$", GREEN, 12.5, ha="center")
    ax.set_xticks(k)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel("$k$", fontsize=13, color=DARK)
    ax.set_ylabel("$P(X \\leq k)$", fontsize=12, color=DARK)
    ax.set_title("probabilités cumulées de $\\mathcal{B}(10\\,;0{,}3)$", fontsize=13, color=DARK)
    style(ax)
    _save(fig, I("term_binom_cumul.png"))


diagramme()
formes()
cumul()
