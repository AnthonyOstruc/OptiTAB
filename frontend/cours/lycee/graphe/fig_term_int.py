# -*- coding: utf-8 -*-
"""Figures : Terminale — Calcul intégral."""
import numpy as np
from matplotlib.patches import Rectangle

from figlycee import new_fig, _save, setup_repere, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

BOITE = dict(fc="white", ec="none", pad=1.5)


def aire():
    fig, ax = new_fig(6.8, 5.6)
    setup_repere(ax, (-0.6, 2.8), (-0.5, 5.0), 0.5, 1)
    x = np.linspace(0, 2.2, 300)
    ax.plot(x, x ** 2, color=BLUE, lw=2.6)
    xs = np.linspace(0, 2, 200)
    ax.fill_between(xs, xs ** 2, color="#d6eafc")
    ax.plot([2, 2], [0, 4], color=BLUE, lw=1.2, ls=":")
    txt(ax, 1.38, 0.45, "$\\int_0^2 x^2\\,dx = \\frac{8}{3}$ u.a.", DARK, 13, ha="center", fontweight="bold")
    txt(ax, 2.25, 4.7, "$y = x^2$", BLUE, 13.5, ha="left", va="center", fontweight="bold")
    ax.set_aspect(0.55)
    ax.axis("off")
    _save(fig, I("term_int_aire.png"))


def rectangles():
    fig, ax = new_fig(7.4, 5.4)
    setup_repere(ax, (-0.4, 2.6), (-0.4, 4.6), 0.5, 1)
    n, a, b = 8, 0.0, 2.0
    h = (b - a) / n
    for k in range(n):
        x0 = a + k * h
        ax.add_patch(Rectangle((x0, 0), h, (x0 + h) ** 2, fc="#fdebd0", ec=ORANGE, lw=1))
        ax.add_patch(Rectangle((x0, 0), h, x0 ** 2, fc="#d6eafc", ec=BLUE, lw=1))
    x = np.linspace(0, 2.15, 200)
    ax.plot(x, x ** 2, color=DARK, lw=2.4)
    s_inf = sum((a + k * h) ** 2 * h for k in range(n))
    s_sup = sum((a + (k + 1) * h) ** 2 * h for k in range(n))
    txt(ax, 1.1, -0.65, f"bleu : {s_inf:.4f}".replace(".", ",") + "  ≤  $\\int_0^2 x^2\\,dx$  ≤  " +
        f"{s_sup:.4f}".replace(".", ",") + " : orange", DARK, 12, ha="center", va="top")
    ax.set_aspect(0.5)
    ax.axis("off")
    _save(fig, I("term_int_rectangles.png"))
    return s_inf, s_sup


def entre():
    fig, ax = new_fig(6.4, 5.6)
    setup_repere(ax, (-0.3, 1.4), (-0.25, 1.35), 0.5, 0.5)
    x = np.linspace(0, 1.25, 200)
    ax.plot(x, x, color=ORANGE, lw=2.4)
    ax.plot(x, x ** 2, color=BLUE, lw=2.4)
    xs = np.linspace(0, 1, 200)
    ax.fill_between(xs, xs ** 2, xs, color="#e8f5e9")
    ax.annotate("$\\mathcal{A} = \\frac{1}{6}$", xy=(0.5, 0.37), xytext=(0.88, 0.18), fontsize=15, color=GREEN,
                fontweight="bold", ha="center", arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.4))
    txt(ax, 1.27, 1.25, "$y = x$", ORANGE, 13, va="center")
    txt(ax, 1.15, 1.38, "$y = x^2$", BLUE, 13, ha="right", va="bottom")
    txt(ax, 0.55, -0.32, "$\\mathcal{A} = \\int_0^1 (x - x^2)\\,dx$ car $x^2 \\leq x$ sur $[0\\,;1]$", DARK, 12.5,
        ha="center", va="top")
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_int_entre.png"))


def moyenne():
    fig, ax = new_fig(7.0, 5.4)
    setup_repere(ax, (-0.5, 3.6), (-0.7, 9.8), 1, 1)
    x = np.linspace(0, 3.15, 300)
    ax.plot(x, x ** 2, color=BLUE, lw=2.6)
    xs = np.linspace(0, 3, 200)
    ax.fill_between(xs, xs ** 2, color="#d6eafc")
    ax.add_patch(Rectangle((0, 0), 3, 3, fill=False, ec=ORANGE, lw=2.4, ls="--"))
    txt(ax, 3.1, 3.0, "$\\mu = 3$", ORANGE, 14, va="center", fontweight="bold")
    txt(ax, 0.15, 8.2, "même aire : $\\int_0^3 x^2\\,dx = 9 = 3 \\times \\mu$", DARK, 12.5, ha="left")
    ax.set_aspect(0.3)
    ax.axis("off")
    _save(fig, I("term_int_moyenne.png"))


aire()
print(rectangles())
entre()
moyenne()
