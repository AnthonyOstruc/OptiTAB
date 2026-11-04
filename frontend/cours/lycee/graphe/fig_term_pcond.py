# -*- coding: utf-8 -*-
"""Figures : Terminale — Probabilités conditionnelles et indépendance."""
from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED

BOITE = dict(fc="white", ec="none", pad=1.2)
v = lambda x: f"{x:g}".replace(".", "{,}")  # noqa: E731


def depistage():
    fig, ax = new_fig(9.8, 5.0)
    branches = [("M", 0.02, 1.7, RED, [("T", 0.95), ("\\overline{T}", 0.05)]),
                ("\\overline{M}", 0.98, -1.7, BLUE, [("T", 0.10), ("\\overline{T}", 0.90)])]
    ax.scatter([0], [0], s=30, color=DARK)
    for n1, p, y1, col, feuilles in branches:
        ax.plot([0.12, 2.1], [0, y1], color=col, lw=2)
        txt(ax, 1.05, y1 / 2 + (0.3 if y1 > 0 else -0.3), f"${v(p)}$", col, 13, ha="center", va="center",
            fontweight="bold", bbox=BOITE)
        txt(ax, 2.4, y1, f"${n1}$", col, 17, ha="center", va="center", fontweight="bold")
        for k, (n2, q) in enumerate(feuilles):
            y2 = y1 + (0.85 if k == 0 else -0.85)
            ax.plot([2.7, 4.7], [y1, y2], color=NEUTRAL, lw=1.6)
            txt(ax, 3.7, (y1 + y2) / 2 + (0.25 if k == 0 else -0.25), f"${v(q)}$", DARK, 12.5, ha="center",
                va="center", bbox=BOITE)
            txt(ax, 5.0, y2, f"${n2}$", GREEN if n2 == "T" else DARK, 16, ha="center", va="center",
                fontweight="bold")
            txt(ax, 5.6, y2, f"$P({n1} \\cap {n2}) = {v(round(p * q, 4))}$", GREEN if n2 == "T" else DARK, 12.5,
                va="center")
    txt(ax, 0.2, 3.1, "$M$ : malade ; $T$ : test positif", DARK, 12.5)
    txt(ax, 4.6, -3.35, "$P(T) = 0{,}019 + 0{,}098 = 0{,}117$  et  $P_T(M) = \\frac{0{,}019}{0{,}117} \\approx 0{,}16$",
        GREEN, 13, ha="center", va="center", fontweight="bold")
    ax.set_xlim(-0.3, 10.2)
    ax.set_ylim(-3.8, 3.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_pcond_depistage.png"))


def epreuves():
    fig, ax = new_fig(10.4, 5.6)
    p = 0.6
    xs = [0, 2.2, 4.4, 6.6]
    def noeud(x, y, niv, chemin):
        if niv == 3:
            nbS = chemin.count("S")
            col = GREEN if nbS == 2 else DARK
            proba = 1.0
            for c in chemin:
                proba *= p if c == "S" else 1 - p
            txt(ax, x + 0.35, y, f"${''.join(chemin)}$ : ${v(round(proba, 3))}$", col, 11.5, va="center",
                fontweight="bold" if nbS == 2 else "normal")
            return
        dy = [2.4, 1.2, 0.6][niv]
        for k, c in enumerate(("S", "E")):
            y2 = y + (dy if k == 0 else -dy)
            x2 = xs[niv + 1]
            ax.plot([x + 0.15, x2 - 0.2], [y, y2], color=BLUE if c == "S" else ORANGE, lw=1.5)
            txt(ax, x2, y2, f"${c}$", BLUE if c == "S" else ORANGE, 13, ha="center", va="center", fontweight="bold")
            txt(ax, (x + x2) / 2, (y + y2) / 2 + (0.18 if k == 0 else -0.18), f"${v(p if c == 'S' else 1 - p)}$",
                DARK, 10, ha="center", va="center", bbox=BOITE)
            noeud(x2, y2, niv + 1, chemin + [c])
    ax.scatter([0], [0], s=30, color=DARK)
    noeud(0, 0, 0, [])
    txt(ax, 4.6, -4.7, "en vert : exactement 2 succès, $3 \\times 0{,}6^2 \\times 0{,}4 = 0{,}432$", GREEN, 13,
        ha="center", va="center", fontweight="bold")
    ax.set_xlim(-0.3, 9.8)
    ax.set_ylim(-5.1, 4.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_pcond_epreuves.png"))


depistage()
epreuves()
