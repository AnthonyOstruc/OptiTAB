# -*- coding: utf-8 -*-
"""Figures : Terminale — Algorithmique (conditions, boucles, listes)."""
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle, Wedge
from matplotlib.ticker import FuncFormatter

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, LBLUE, LGREEN, LORANGE

MONO = dict(family="monospace")
GRID = "#d5dde3"
VIRGULE = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))


def organigramme_qn():
    fig, ax = new_fig(10.4, 4.6)
    tests = [("q > 1 ?", "+∞"), ("q == 1 ?", "1"), ("-1 < q < 1 ?", "0")]
    for i, (t, res) in enumerate(tests):
        x = i * 3.4
        ax.add_patch(Polygon([(x, 2.6), (x + 1.45, 2.0), (x, 1.4), (x - 1.45, 2.0)], closed=True, fc=LORANGE,
                             ec=ORANGE, lw=1.8))
        ax.text(x, 2.0, t, ha="center", va="center", fontsize=11.5, color=DARK, **MONO)
        ax.add_patch(FancyBboxPatch((x - 1.0, -0.15), 2.0, 0.7, boxstyle="round,pad=0.06", fc=LGREEN, ec=GREEN, lw=1.8))
        ax.text(x, 0.2, f"limite {res}", ha="center", va="center", fontsize=12, color=DARK)
        ax.annotate("", xy=(x, 0.62), xytext=(x, 1.4), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.4))
        txt(ax, x + 0.12, 1.0, "oui", GREEN, 11.5, fontweight="bold", va="center")
        x2 = x + 3.4
        ax.annotate("", xy=(x2 - 1.5, 2.0), xytext=(x + 1.45, 2.0), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL,
                                                                                    lw=1.4))
        txt(ax, x + 1.95, 2.12, "non", RED, 11.5, fontweight="bold", ha="center", va="bottom")
    x = 3 * 3.4
    ax.add_patch(FancyBboxPatch((x - 1.2, 1.65), 2.4, 0.7, boxstyle="round,pad=0.06", fc="#fdecea", ec=RED, lw=1.8))
    ax.text(x, 2.0, "pas de limite", ha="center", va="center", fontsize=12, color=DARK)
    txt(ax, x, 1.2, "($q \\leq -1$)", RED, 11.5, ha="center", va="top")
    txt(ax, 5.1, -0.8, "if … elif … elif … else : limite de la suite géométrique $(q^n)$ selon la valeur de $q$",
        DARK, 12, ha="center", va="top")
    ax.set_xlim(-1.8, 11.8)
    ax.set_ylim(-1.4, 2.9)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_algo_qn.png"))


def implication():
    fig, ax = new_fig(8.6, 3.4)
    ent = ["P", "Q", "P ⇒ Q", "non Q ⇒ non P"]
    lignes = [("V", "V"), ("V", "F"), ("F", "V"), ("F", "F")]
    w, h = 2.0, 0.6
    for j, e in enumerate(ent):
        ax.add_patch(Rectangle((j * w, 4 * h), w, h, fc=LBLUE, ec=NEUTRAL, lw=1))
        ax.text(j * w + w / 2, 4.5 * h, e, ha="center", va="center", fontsize=13, color=BLUE, fontweight="bold")
    for i, (a, b) in enumerate(lignes):
        imp = "F" if (a, b) == ("V", "F") else "V"
        for j, v in enumerate((a, b, imp, imp)):
            fc = "white" if j < 2 else (LGREEN if v == "V" else "#fdecea")
            col = DARK if j < 2 else (GREEN if v == "V" else RED)
            ax.add_patch(Rectangle((j * w, (3 - i) * h), w, h, fc=fc, ec=NEUTRAL, lw=1))
            ax.text(j * w + w / 2, (3.5 - i) * h, v, ha="center", va="center", fontsize=13, color=col,
                    fontweight="bold" if j >= 2 else "normal")
    txt(ax, 4 * w + 0.3, 2.5 * h, "une implication et sa\ncontraposée ont toujours\nla même valeur de vérité",
        GREEN, 12, va="center")
    ax.set_xlim(-0.1, 4 * w + 4.2)
    ax.set_ylim(-0.1, 5 * h + 0.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_algo_implication.png"))


def montecarlo():
    rng = np.random.default_rng(42)
    N = 3000
    x, y = rng.random(N), rng.random(N)
    dedans = x * x + y * y <= 1
    fig, ax = new_fig(6.2, 6.4)
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, ec=DARK, lw=1.5))
    ax.add_patch(Wedge((0, 0), 1, 0, 90, fill=False, ec=DARK, lw=1.8))
    ax.scatter(x[dedans], y[dedans], s=3, color=BLUE)
    ax.scatter(x[~dedans], y[~dedans], s=3, color=ORANGE)
    est = 4 * dedans.mean()
    txt(ax, 0.5, -0.08, f"{int(dedans.sum())} points sur {N} dans le quart de disque : $\\pi \\approx 4 \\times$ fréquence $\\approx$ "
        + f"{est:.3f}".replace(".", ","), DARK, 11.5, ha="center", va="top")
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.2, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_algo_montecarlo.png"))
    return est, int(dedans.sum())


def somme_inverse_carres():
    fig, ax = new_fig(8.4, 4.2)
    n = np.arange(1, 201)
    S = np.cumsum(1 / n ** 2)
    ax.plot(n, S, color=BLUE, lw=2.2)
    ax.axhline(np.pi ** 2 / 6, color=RED, lw=1.4, ls="--")
    txt(ax, 198, np.pi ** 2 / 6 + 0.02, "$\\frac{\\pi^2}{6} \\approx 1{,}645$", RED, 13, ha="right", va="bottom")
    txt(ax, 60, 1.25, "$S_n = 1 + \\frac{1}{2^2} + \\cdots + \\frac{1}{n^2}$ calculée par une boucle for", BLUE, 12.5)
    ax.set_xlim(0, 202)
    ax.set_ylim(0.95, 1.75)
    ax.yaxis.set_major_formatter(VIRGULE)
    ax.set_xlabel("$n$", fontsize=13, color=DARK)
    ax.grid(color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _save(fig, I("term_algo_somme.png"))


def pascal_listes():
    fig, ax = new_fig(9.4, 3.4)
    lignes = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    for i, L in enumerate(lignes):
        y = -i * 0.75
        ax.text(-0.4, y, f"ligne {i} :", ha="right", va="center", fontsize=11.5, color=NEUTRAL)
        for k, v in enumerate(L):
            ax.add_patch(Rectangle((k * 0.8, y - 0.28), 0.8, 0.56, fc=LBLUE if i < 4 else LGREEN,
                                   ec=BLUE if i < 4 else GREEN, lw=1.3))
            ax.text(k * 0.8 + 0.4, y, str(v), ha="center", va="center", fontsize=12.5, color=DARK, **MONO)
    ax.text(4.6, -1.6, "ligne suivante = [1] + [L[k] + L[k+1] …] + [1]", ha="left", va="center", fontsize=11.5,
            color=DARK, **MONO)
    ax.text(4.6, -2.3, "(relation de Pascal)", ha="left", va="center", fontsize=11.5, color=GREEN)
    ax.set_xlim(-2.2, 11.4)
    ax.set_ylim(-3.4, 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_algo_pascal.png"))


def simulation_liste():
    rng = np.random.default_rng(8)
    N, n, p = 1000, 100, 0.3
    freqs = rng.binomial(n, p, N) / n
    fig, ax = new_fig(8.4, 4.2)
    bins = np.arange(0.105, 0.51, 0.01)
    ax.hist(freqs, bins=bins, color=BLUE, edgecolor="white", zorder=3)
    ax.axvspan(0.2, 0.4, color="#e8f5e9", zorder=0)
    ax.axvline(0.3, color=RED, lw=1.4, ls="--", zorder=4)
    dans = np.mean(np.abs(freqs - p) <= 0.1 + 1e-12)
    ax.set_title(f"liste de {N} fréquences (échantillons de taille {n}, $p = 0{{,}}3$) : "
                 f"{dans * 100:.1f} % dans $[0{{,}}2\\,;0{{,}}4]$".replace(".", ","), fontsize=12, color=DARK)
    ax.xaxis.set_major_formatter(VIRGULE)
    ax.set_xlabel("fréquence observée", fontsize=12, color=DARK)
    ax.set_ylabel("effectif", fontsize=12, color=DARK)
    ax.grid(axis="y", color=GRID, lw=0.6, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _save(fig, I("term_algo_simulation.png"))
    return dans


organigramme_qn()
implication()
print("monte-carlo", montecarlo())
somme_inverse_carres()
pascal_listes()
print("simulation", simulation_liste())
