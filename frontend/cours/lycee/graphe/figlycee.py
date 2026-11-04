# -*- coding: utf-8 -*-
"""Style commun des figures de lycée (mêmes couleurs et tracés que les figures de 4ème)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "cours_optitab", "4e", "graphe"))
from fig4e import (new_fig, _save, right_angle, setup_repere, BLUE, ORANGE, GREEN, DARK, NEUTRAL,  # noqa: E402,F401
                   tableau)
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Polygon  # noqa: E402,F401

IMAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
LBLUE, LORANGE, LGREEN, RED, PURPLE = "#d6eafc", "#fdebd0", "#e8f5e9", "#c0392b", "#8e44ad"
I = lambda f: os.path.join(IMAGES, f)  # noqa: E731


def txt(ax, x, y, s, col=DARK, fs=12, **kw):
    ax.text(x, y, s, color=col, fontsize=fs, **kw)


def cadre(ax, xl, yl):
    ax.set_xlim(*xl)
    ax.set_ylim(*yl)
    ax.set_aspect("equal")
    ax.axis("off")


def droite(ax, y, lo, hi, graduations=(), etiquettes=True, fs=11, couleur=NEUTRAL, fleche=True):
    """Droite graduée horizontale à l'ordonnée y."""
    ax.annotate("", xy=(hi, y), xytext=(lo, y),
                arrowprops=dict(arrowstyle="-|>" if fleche else "-", color=couleur, lw=1.6, mutation_scale=14))
    for g in graduations:
        ax.plot([g, g], [y - 0.09, y + 0.09], color=couleur, lw=1.3)
        if etiquettes:
            s = f"{g:g}".replace(".", ",").replace("-", "−")
            ax.text(g, y - 0.18, s, ha="center", va="top", fontsize=fs, color=DARK)


def crochet(ax, x, y, sens, couleur=BLUE, h=0.22, lw=3):
    """Crochet à la française : sens=+1 « [ » (ouvert vers la droite), sens=-1 « ] »."""
    d = 0.09 * sens
    ax.plot([x + d, x, x, x + d], [y - h, y - h, y + h, y + h], color=couleur, lw=lw, solid_capstyle="butt")


def _grille_tableau(ax, nl, W, hauts, lab_w):
    y = 0
    ax.plot([0, W], [0, 0], color=BLUE, lw=1.4)
    for h in hauts:
        y -= h
        ax.plot([0, W], [y, y], color=BLUE, lw=1.4)
    ax.plot([0, 0], [0, y], color=BLUE, lw=1.4)
    ax.plot([W, W], [0, y], color=BLUE, lw=1.4)
    ax.plot([lab_w, lab_w], [0, y], color=BLUE, lw=1.4)
    return y


def tableau_signes(path, xs, lignes, lab_w=2.6, col_w=1.5, fs=14, titre=None, w=None):
    """Tableau de signes. xs : valeurs remarquables (textes) ; lignes : [(nom, cellules)] avec
    2n+1 cellules (intervalle, point, intervalle, …) : '+', '-', '0', '||' (valeur interdite) ou ''."""
    import matplotlib.pyplot as plt
    n = len(xs)
    x0 = lab_w + 0.3
    W = x0 + 2 * col_w * (n + 1) + 0.3
    hauts = [0.8] + [0.8] * len(lignes)
    H = sum(hauts)
    fig = plt.figure(figsize=(w or W * 0.62, (H + (0.6 if titre else 0.1)) * 0.62))
    ax = fig.add_axes([0, 0, 1, 1])
    ybas = _grille_tableau(ax, len(lignes) + 1, W, hauts, lab_w)
    pos = [x0 + 2 * col_w * (k + 1) for k in range(n)]
    txt(ax, lab_w / 2, -0.4, "$x$", DARK, fs, ha="center", va="center")
    txt(ax, lab_w + 0.35, -0.4, "$-\\infty$", DARK, fs - 1, ha="left", va="center")
    txt(ax, W - 0.15, -0.4, "$+\\infty$", DARK, fs - 1, ha="right", va="center")
    for p, s in zip(pos, xs):
        txt(ax, p, -0.4, s, DARK, fs, ha="center", va="center")
    for i, (nom, cells) in enumerate(lignes):
        yc = -0.8 * (i + 1) - 0.4
        txt(ax, lab_w / 2, yc, nom, DARK, fs - 1.5, ha="center", va="center")
        for j, c in enumerate(cells):
            if j % 2 == 0:
                xc = (x0 if j == 0 else pos[j // 2 - 1]) + ((pos[j // 2] if j // 2 < n else W - 0.3) -
                                                             (x0 if j == 0 else pos[j // 2 - 1])) / 2
                col = BLUE if c == "+" else ORANGE if c == "-" else DARK
                sym = {"+": "$+$", "-": "$-$"}.get(c, c)
                txt(ax, xc, yc, sym, col, fs + 3, ha="center", va="center", fontweight="bold")
            else:
                p = pos[j // 2]
                if c == "||":
                    for dx in (-0.05, 0.05):
                        ax.plot([p + dx, p + dx], [yc - 0.4, yc + 0.4], color=DARK, lw=1.4)
                else:
                    ax.plot([p, p], [yc - 0.4, yc + 0.4], color=NEUTRAL, lw=0.9, ls=":")
                    if c:
                        txt(ax, p, yc, c, GREEN, fs, ha="center", va="center",
                            bbox=dict(fc="white", ec="none", pad=0.5))
    if titre:
        txt(ax, W / 2, 0.35, titre, DARK, fs - 1, ha="center", va="bottom", fontweight="bold")
    ax.set_xlim(-0.05, W + 0.05)
    ax.set_ylim(ybas - 0.05, 0.7 if titre else 0.05)
    ax.axis("off")
    _save(fig, path)


def tableau_variations(path, xs, valeurs, lab_w=2.4, col_w=1.7, fs=14, signe=None, nom="f(x)", w=None,
                       titre=None):
    """Tableau de variations. xs : textes des bornes et valeurs remarquables (bornes incluses) ;
    valeurs : [(texte, 'h' ou 'b')] une par abscisse (texte '' pour ne rien écrire) ;
    signe : cellules de la ligne « f'(x) » (2n-1 cellules entre la 1re et la dernière abscisse) ou None."""
    import matplotlib.pyplot as plt
    n = len(xs)
    W = lab_w + col_w * (n - 1) * 2 + 1.0
    hauts = [0.8] + ([0.8] if signe else []) + [1.9]
    H = sum(hauts)
    fig = plt.figure(figsize=(w or W * 0.62, (H + (0.6 if titre else 0.1)) * 0.62))
    ax = fig.add_axes([0, 0, 1, 1])
    ybas = _grille_tableau(ax, len(hauts), W, hauts, lab_w)
    pos = [lab_w + 0.5 + 2 * col_w * k for k in range(n)]
    txt(ax, lab_w / 2, -0.4, "$x$", DARK, fs, ha="center", va="center")
    for p, s in zip(pos, xs):
        txt(ax, p, -0.4, s, DARK, fs, ha="center", va="center")
    y = -0.8
    if signe:
        yc = y - 0.4
        txt(ax, lab_w / 2, yc, "$f'(x)$", DARK, fs - 1, ha="center", va="center")
        for j, c in enumerate(signe):
            if j % 2 == 0:
                xc = (pos[j // 2] + pos[j // 2 + 1]) / 2
                col = BLUE if c == "+" else ORANGE if c == "-" else DARK
                txt(ax, xc, yc, {"+": "$+$", "-": "$-$"}.get(c, c), col, fs + 3, ha="center", va="center",
                    fontweight="bold")
            else:
                p = pos[j // 2 + 1]
                ax.plot([p, p], [yc - 0.4, yc + 0.4], color=NEUTRAL, lw=0.9, ls=":")
                if c:
                    txt(ax, p, yc, c, GREEN, fs, ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.5))
        y -= 0.8
    yh, yb = y - 0.35, y - 1.55
    txt(ax, lab_w / 2, (yh + yb) / 2, f"${nom}$", DARK, fs - 1, ha="center", va="center")
    pts = []
    for p, (t, hb) in zip(pos, valeurs):
        yy = yh if hb == "h" else yb
        if t:
            txt(ax, p, yy, t, DARK, fs, ha="center", va="center")
        pts.append((p, yy))
    for (p1, y1), (p2, y2) in zip(pts, pts[1:]):
        dy = 0.22 if y1 > y2 else -0.22
        ax.annotate("", xy=(p2 - 0.45, y2 - dy), xytext=(p1 + 0.45, y1 + dy),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.8, mutation_scale=16))
    if titre:
        txt(ax, W / 2, 0.35, titre, DARK, fs - 1, ha="center", va="bottom", fontweight="bold")
    ax.set_xlim(-0.05, W + 0.05)
    ax.set_ylim(ybas - 0.05, 0.7 if titre else 0.05)
    ax.axis("off")
    _save(fig, path)


def intervalle(ax, y, a, b, ferme_a, ferme_b, couleur=BLUE, lo=None, hi=None):
    """Trait épais de a à b ; crochets tournés vers l'intérieur si l'extrémité est incluse."""
    xa = a if a is not None else lo
    xb = b if b is not None else hi
    ax.plot([xa, xb], [y, y], color=couleur, lw=6, alpha=0.55, solid_capstyle="butt")
    if a is not None:
        crochet(ax, a, y, +1 if ferme_a else -1, couleur)
    if b is not None:
        crochet(ax, b, y, -1 if ferme_b else +1, couleur)
