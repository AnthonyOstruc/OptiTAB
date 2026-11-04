# -*- coding: utf-8 -*-
"""Figures : Première — Équations, fonctions polynômes du second degré."""
import numpy as np

from figlycee import new_fig, _save, setup_repere, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED

f = lambda x: 2 * x ** 2 + 4 * x - 6  # noqa: E731  (= 2(x+1)^2 - 8 = 2(x-1)(x+3))


def repere_parabole(ax, xb, yb, xt=1, yt=2):
    setup_repere(ax, xb, yb, xt, yt)


def formes():
    fig, ax = new_fig(7.6, 6.2)
    repere_parabole(ax, (-4.6, 2.6), (-9.5, 8.5), 1, 2)
    x = np.linspace(-4.2, 2.2, 300)
    ax.plot(x, f(x), color=BLUE, lw=2.6)
    ax.axvline(-1, color=NEUTRAL, lw=1.1, ls="--")
    for (px, py, nom, col, dx, dy, ha) in [(-1, -8, "sommet $S(-1\\,;-8)$\n(forme canonique)", ORANGE, -0.3, -0.9, "right"),
                                          (-3, 0, "racine $-3$", GREEN, -0.15, 0.7, "right"),
                                          (1, 0, "racine $1$\n(forme factorisée)", GREEN, 0.3, -2.6, "left"),
                                          (0, -6, "$f(0)=c=-6$\n(forme développée)", RED, 0.3, -1.4, "left")]:
        ax.scatter([px], [py], s=55, color=col, zorder=6)
        txt(ax, px + dx, py + dy, nom, col, 11.5, ha=ha, fontweight="bold")
    txt(ax, -1.1, 7.6, "axe $x=-1$", NEUTRAL, 11, ha="right")
    txt(ax, -4.4, -11.2, "$f(x)=2x^2+4x-6=2(x+1)^2-8=2(x-1)(x+3)$", DARK, 13)
    ax.set_ylim(-11.8, 8.5)
    ax.axis("off")
    _save(fig, I("1er_second_degre_formes.png"))


def discriminant():
    fig, axs = __import__("matplotlib.pyplot", fromlist=["subplots"]).subplots(2, 3, figsize=(10.2, 6.4))
    cas = [("$\\Delta>0$ : deux racines", lambda x: (x - 1) * (x - 3), [1, 3]),
           ("$\\Delta=0$ : une racine double", lambda x: (x - 2) ** 2, [2]),
           ("$\\Delta<0$ : aucune racine", lambda x: (x - 2) ** 2 + 1, [])]
    for ligne, a in enumerate((1, -1)):
        for col, (titre, g, rac) in enumerate(cas):
            ax = axs[ligne][col]
            x = np.linspace(-0.4, 4.4, 200)
            ax.axhline(0, color=NEUTRAL, lw=1.2)
            ax.axvline(0, color=NEUTRAL, lw=0.8)
            ax.plot(x, a * g(x), color=BLUE if a > 0 else ORANGE, lw=2.6)
            for r in rac:
                ax.scatter([r], [0], s=50, color=GREEN, zorder=5)
            ax.set_xlim(-0.5, 4.5)
            ax.set_ylim(-3.2, 3.2)
            ax.set_xticks([])
            ax.set_yticks([])
            for s in ax.spines.values():
                s.set_color("#d5d8dc")
            if ligne == 0:
                ax.set_title(titre, fontsize=12.5, color=DARK)
        axs[ligne][0].set_ylabel("$a>0$" if a > 0 else "$a<0$", fontsize=14, color=BLUE if a > 0 else ORANGE,
                                 rotation=0, labelpad=26)
    fig.suptitle("Position de la parabole par rapport à l'axe des abscisses", fontsize=13, color=DARK,
                 fontweight="bold")
    _save(fig, I("1er_second_degre_discriminant.png"))


def signe():
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(7.6, 6.6))
    ax = fig.add_axes([0.08, 0.36, 0.86, 0.6])
    setup_repere(ax, (-4.6, 2.6), (-9.5, 8.5), 1, 2)
    x = np.linspace(-4.2, 2.2, 300)
    y = f(x)
    ax.fill_between(x, 0, y, where=y > 0, color="#d6eafc", alpha=0.9)
    ax.fill_between(x, 0, y, where=y < 0, color="#fdebd0", alpha=0.9)
    ax.plot(x, y, color=BLUE, lw=2.6)
    for r in (-3, 1):
        ax.scatter([r], [0], s=55, color=GREEN, zorder=6)
    txt(ax, -4.3, 4.0, "$f(x)>0$", BLUE, 13, fontweight="bold")
    txt(ax, 1.55, 4.0, "$f(x)>0$", BLUE, 13, fontweight="bold")
    txt(ax, -1.0, -3.2, "$f(x)<0$", ORANGE, 13, ha="center", fontweight="bold")
    ax.axis("off")
    tb = fig.add_axes([0.08, 0.04, 0.86, 0.26])
    tb.set_xlim(0, 10)
    tb.set_ylim(0, 2)
    tb.axis("off")
    for yy in (0, 1, 2):
        tb.plot([0, 10], [yy, yy], color=BLUE, lw=1.2)
    for xx in (0, 2, 10):
        tb.plot([xx, xx], [0, 2], color=BLUE, lw=1.2)
    tb.text(1, 1.5, "$x$", ha="center", va="center", fontsize=14)
    tb.text(1, 0.5, "signe de $f(x)$", ha="center", va="center", fontsize=12)
    for xx, s in [(2.3, "$-\\infty$"), (4.6, "$-3$"), (7.4, "$1$"), (9.6, "$+\\infty$")]:
        tb.text(xx, 1.5, s, ha="center", va="center", fontsize=14)
    for xx, s, c in [(3.45, "$+$", BLUE), (4.6, "$0$", GREEN), (6.0, "$-$", ORANGE), (7.4, "$0$", GREEN),
                     (8.5, "$+$", BLUE)]:
        tb.text(xx, 0.5, s, ha="center", va="center", fontsize=17, color=c, fontweight="bold")
    for xx in (4.6, 7.4):
        tb.plot([xx, xx], [0, 1], color=NEUTRAL, lw=1, ls=":")
    _save(fig, I("1er_second_degre_signe.png"))


def projectile():
    fig, ax = new_fig(7.6, 5.0)
    setup_repere(ax, (-0.4, 4.9), (-2, 34), 1, 5, xlabel="$t$ (s)", ylabel="$h$ (m)")
    t = np.linspace(0, 4.45, 200)
    h = -5 * t ** 2 + 20 * t + 10
    ax.plot(t, h, color=BLUE, lw=2.6)
    ax.plot([2, 2], [0, 30], color=ORANGE, lw=1.3, ls="--")
    ax.plot([0, 2], [30, 30], color=ORANGE, lw=1.3, ls="--")
    ax.scatter([2], [30], s=60, color=ORANGE, zorder=6)
    txt(ax, 2.15, 31.0, "maximum : $h(2)=30$ m", ORANGE, 12.5, fontweight="bold")
    ax.scatter([0], [10], s=40, color=DARK, zorder=6)
    txt(ax, 0.12, 8.2, "départ : 10 m", DARK, 11)
    txt(ax, 2.15, 4, "$h(t)=-5(t-2)^2+30$", BLUE, 13)
    ax.axis("off")
    _save(fig, I("1er_second_degre_projectile.png"))


def variations():
    from figlycee import tableau_variations
    tableau_variations(I("1er_second_degre_variations.png"), ["$-\\infty$", "$-1$", "$+\\infty$"],
                       [("", "h"), ("$-8$", "b"), ("", "h")], col_w=1.8, nom="f(x)",
                       titre="$f(x) = 2x^2 + 4x - 6$ : $a = 2 > 0$, minimum $f(-1) = -8$")


formes()
discriminant()
signe()
projectile()
variations()
