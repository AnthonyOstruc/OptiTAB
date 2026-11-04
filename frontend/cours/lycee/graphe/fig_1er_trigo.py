# -*- coding: utf-8 -*-
"""Figures : Première — Trigonométrie."""
import numpy as np
from matplotlib.patches import Arc, Circle

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

BOITE = dict(fc="white", ec="none", pad=1.2)


def axes_cercle(ax, r=1.0, ext=1.35):
    ax.annotate("", xy=(ext, 0), xytext=(-ext, 0), arrowprops=dict(arrowstyle="->", lw=1.3, color=NEUTRAL))
    ax.annotate("", xy=(0, ext), xytext=(0, -ext), arrowprops=dict(arrowstyle="->", lw=1.3, color=NEUTRAL))
    ax.add_patch(Circle((0, 0), r, fill=False, ec=BLUE, lw=2.2))
    txt(ax, 1.03, -0.1, "$I$", DARK, 13, va="top")
    txt(ax, -0.08, 1.04, "$J$", DARK, 13, ha="right")
    txt(ax, -0.06, -0.06, "$O$", DARK, 12, ha="right", va="top")


def fin(ax, lim=1.6):
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.axis("off")


def cercle():
    fig, ax = new_fig(6.4, 6.4)
    axes_cercle(ax)
    t = 0.95
    M = np.array([np.cos(t), np.sin(t)])
    ax.add_patch(Arc((0, 0), 2, 2, theta1=0, theta2=np.degrees(t), color=ORANGE, lw=5, alpha=0.8))
    ax.plot([0, M[0]], [0, M[1]], color=DARK, lw=1.4)
    ax.plot([M[0], M[0]], [0, M[1]], color=GREEN, lw=1.6, ls="--")
    ax.plot([0, M[0]], [M[1], M[1]], color=RED, lw=1.6, ls="--")
    ax.plot([0, M[0]], [0, 0], color=GREEN, lw=4)
    ax.plot([0, 0], [0, M[1]], color=RED, lw=4)
    ax.scatter([M[0]], [M[1]], s=40, color=DARK, zorder=6)
    txt(ax, M[0] + 0.06, M[1] + 0.06, "$M(t)$", DARK, 14, fontweight="bold")
    txt(ax, M[0] / 2, -0.08, "$\\cos t$", GREEN, 14, ha="center", va="top", fontweight="bold")
    txt(ax, -0.06, M[1] / 2, "$\\sin t$", RED, 14, ha="right", va="center", fontweight="bold")
    txt(ax, 1.05, 0.45, "arc de\nlongueur $t$", ORANGE, 12.5, va="center")
    txt(ax, 0.0, -1.5, "rayon $1$ ; sens direct : inverse des aiguilles d’une montre", DARK, 11.5, ha="center")
    fin(ax)
    _save(fig, I("1er_trigo_cercle.png"))


def remarquables():
    fig, ax = new_fig(6.8, 6.8)
    ax.annotate("", xy=(1.3, 0), xytext=(-0.15, 0), arrowprops=dict(arrowstyle="->", lw=1.3, color=NEUTRAL))
    ax.annotate("", xy=(0, 1.3), xytext=(0, -0.15), arrowprops=dict(arrowstyle="->", lw=1.3, color=NEUTRAL))
    ax.add_patch(Arc((0, 0), 2, 2, theta1=-5, theta2=95, color=BLUE, lw=2.2))
    pts = [(np.pi / 6, "\\frac{\\pi}{6}", "\\left(\\frac{\\sqrt{3}}{2}\\,;\\frac{1}{2}\\right)", ORANGE),
           (np.pi / 4, "\\frac{\\pi}{4}", "\\left(\\frac{\\sqrt{2}}{2}\\,;\\frac{\\sqrt{2}}{2}\\right)", GREEN),
           (np.pi / 3, "\\frac{\\pi}{3}", "\\left(\\frac{1}{2}\\,;\\frac{\\sqrt{3}}{2}\\right)", RED)]
    for a, nom, coord, col in pts:
        c, s = np.cos(a), np.sin(a)
        ax.plot([0, c], [0, s], color=col, lw=1.3)
        ax.plot([c, c], [0, s], color=col, lw=1, ls=":")
        ax.plot([0, c], [s, s], color=col, lw=1, ls=":")
        ax.scatter([c], [s], s=36, color=col, zorder=6)
        txt(ax, 1.08 * c + 0.03, 1.08 * s + 0.02, f"${coord}$", col, 13, va="center")
        r = {6: 0.6, 4: 0.47, 3: 0.36}[round(np.pi / a)]
        txt(ax, r * np.cos(a), r * np.sin(a), f"${nom}$", col, 13, ha="center", va="center", bbox=BOITE)
    for x, lab in ((0.5, "\\frac{1}{2}"), (np.sqrt(2) / 2, "\\frac{\\sqrt{2}}{2}"), (np.sqrt(3) / 2, "\\frac{\\sqrt{3}}{2}")):
        txt(ax, x, -0.05, f"${lab}$", DARK, 11.5, ha="center", va="top")
        txt(ax, -0.05, x, f"${lab}$", DARK, 11.5, ha="right", va="center")
    ax.scatter([1, 0], [0, 1], s=30, color=DARK, zorder=6)
    txt(ax, 1.03, 0.04, "$0$ : $(1\\,;0)$", DARK, 12.5, va="bottom")
    txt(ax, 0.04, 1.04, "$\\frac{\\pi}{2}$ : $(0\\,;1)$", DARK, 12.5, va="bottom")
    ax.set_xlim(-0.35, 1.95)
    ax.set_ylim(-0.3, 1.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_trigo_remarquables.png"))


def associes():
    fig, ax = new_fig(6.6, 6.6)
    axes_cercle(ax)
    x = 0.6
    P = {"M(x)": (x, BLUE, (0.07, 0.07), "left"), "M(-x)": (-x, GREEN, (0.07, -0.1), "left"),
         "M(\\pi - x)": (np.pi - x, ORANGE, (-0.07, 0.07), "right"),
         "M(\\pi + x)": (np.pi + x, RED, (-0.07, -0.1), "right")}
    c, s = np.cos(x), np.sin(x)
    ax.plot([c, c], [-s, s], color=NEUTRAL, lw=1, ls=":")
    ax.plot([-c, -c], [-s, s], color=NEUTRAL, lw=1, ls=":")
    ax.plot([-c, c], [s, s], color=NEUTRAL, lw=1, ls=":")
    ax.plot([-c, c], [-s, -s], color=NEUTRAL, lw=1, ls=":")
    ax.plot([-c, c], [-s, s], color=NEUTRAL, lw=1, ls="--")
    for nom, (a, col, d, ha) in P.items():
        px, py = np.cos(a), np.sin(a)
        ax.scatter([px], [py], s=40, color=col, zorder=6)
        txt(ax, px + d[0], py + d[1], f"${nom}$", col, 13.5, ha=ha, fontweight="bold")
    txt(ax, 0, -1.55, "symétries : $(Ox)$ pour $-x$, $(Oy)$ pour $\\pi - x$, centre $O$ pour $\\pi + x$", DARK, 11.5,
        ha="center")
    fin(ax, 1.65)
    _save(fig, I("1er_trigo_associes.png"))


def courbes():
    fig, ax = new_fig(10.4, 4.0)
    x = np.linspace(-2 * np.pi, 2 * np.pi, 600)
    ax.axhline(0, color=NEUTRAL, lw=1.2)
    ax.axvline(0, color=NEUTRAL, lw=1.2)
    for k in range(-4, 5):
        ax.axvline(k * np.pi / 2, color="#e5e8eb", lw=0.8, zorder=0)
    for yv in (-1, 1):
        ax.axhline(yv, color="#e5e8eb", lw=0.8, zorder=0)
        txt(ax, -0.12, yv, f"${yv}$", DARK, 11, ha="right", va="center")
    ax.plot(x, np.cos(x), color=BLUE, lw=2.6, label="cos")
    ax.plot(x, np.sin(x), color=ORANGE, lw=2.6, label="sin")
    labs = {-2: "-2\\pi", -1: "-\\pi", 1: "\\pi", 2: "2\\pi"}
    for k, l in labs.items():
        txt(ax, k * np.pi, -0.12, f"${l}$", DARK, 12, ha="center", va="top")
    txt(ax, np.pi / 2, -0.12, "$\\frac{\\pi}{2}$", DARK, 12, ha="center", va="top")
    txt(ax, -6.1, 1.25, "$y = \\cos x$ (paire)", BLUE, 13, fontweight="bold")
    txt(ax, 3.4, 1.25, "$y = \\sin x$ (impaire)", ORANGE, 13, fontweight="bold")
    ax.annotate("", xy=(2 * np.pi, -1.45), xytext=(0, -1.45), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.4))
    txt(ax, np.pi, -1.5, "période $2\\pi$", GREEN, 12.5, ha="center", va="top")
    ax.set_xlim(-2 * np.pi - 0.3, 2 * np.pi + 0.3)
    ax.set_ylim(-1.95, 1.6)
    ax.axis("off")
    _save(fig, I("1er_trigo_courbes.png"))


cercle()
remarquables()
associes()
courbes()
