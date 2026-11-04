# -*- coding: utf-8 -*-
"""Figures : Terminale — Équations différentielles."""
import numpy as np

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

GRID = "#d5dde3"


def champ():
    fig, ax = new_fig(8.4, 5.4)
    X, Y = np.meshgrid(np.linspace(0, 8, 17), np.linspace(-1, 8, 19))
    P = -0.5 * Y + 2
    N = np.sqrt(1 + P ** 2)
    ax.quiver(X, Y, 1 / N, P / N, color="#aab7c4", angles="xy", scale=38, width=0.0025, headwidth=0)
    x = np.linspace(0, 8, 300)
    for C in (-4, -2, 2, 4):
        ax.plot(x, 4 + C * np.exp(-0.5 * x), color=NEUTRAL, lw=1.3)
    ax.plot(x, 4 - 4 * np.exp(-0.5 * x), color=BLUE, lw=2.8)
    ax.axhline(4, color=RED, lw=1.6, ls="--")
    ax.scatter([0], [0], s=40, color=BLUE, zorder=6)
    txt(ax, 7.9, 3.5, "solution constante $y = 4$", RED, 12, ha="right", va="top", bbox=dict(fc="white", ec="none", pad=1.5))
    txt(ax, 2.6, 1.0, "$y(0) = 0$ : $y = 4 - 4e^{-0{,}5x}$", BLUE, 13, fontweight="bold", bbox=dict(fc="white", ec="none", pad=1.5))
    ax.set_xlim(-0.2, 8.2)
    ax.set_ylim(-1.2, 8.2)
    ax.set_xlabel("$x$", fontsize=13, color=DARK)
    ax.set_ylabel("$y$", fontsize=13, color=DARK)
    ax.set_title("$y' = -0{,}5y + 2$ : en chaque point, la pente vaut $-0{,}5y + 2$", fontsize=12.5, color=DARK)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _save(fig, I("term_ed_champ.png"))


def refroidissement():
    fig, ax = new_fig(8.4, 4.4)
    t = np.linspace(0, 50, 300)
    ax.plot(t, 20 + 70 * np.exp(-0.1 * t), color=ORANGE, lw=2.8)
    ax.axhline(20, color=BLUE, lw=1.5, ls="--")
    t40 = 10 * np.log(3.5)
    ax.plot([0, t40], [40, 40], color=GREEN, lw=1.2, ls=":")
    ax.plot([t40, t40], [0, 40], color=GREEN, lw=1.2, ls=":")
    ax.scatter([t40], [40], s=36, color=GREEN, zorder=6)
    txt(ax, t40 + 0.8, 42, "$40$ °C au bout de $10\\ln 3{,}5 \\approx 12{,}5$ min", GREEN, 12, va="bottom")
    txt(ax, 49, 17, "température de la pièce : $20$ °C", BLUE, 12, ha="right", va="top")
    txt(ax, 22, 70, "$T(t) = 20 + 70e^{-0{,}1t}$", ORANGE, 14, fontweight="bold")
    ax.set_xlim(0, 51)
    ax.set_ylim(0, 95)
    ax.set_xlabel("temps $t$ (min)", fontsize=12, color=DARK)
    ax.set_ylabel("température (°C)", fontsize=12, color=DARK)
    ax.grid(color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _save(fig, I("term_ed_refroidissement.png"))


champ()
refroidissement()
