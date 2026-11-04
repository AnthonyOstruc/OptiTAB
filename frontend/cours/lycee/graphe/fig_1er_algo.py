# -*- coding: utf-8 -*-
"""Figures : Première — Algorithmique (conditions, boucles, listes)."""
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, LBLUE, LGREEN, LORANGE

CODE_BG = "#2c3e50"
MONO = dict(family="monospace")


def cellule(ax, x, y, w, h, s, fc="white", col=DARK, fs=13, bold=False, mono=True):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=NEUTRAL, lw=1))
    kw = MONO if mono else {}
    ax.text(x + w / 2, y + h / 2, s, ha="center", va="center", fontsize=fs, color=col,
            fontweight="bold" if bold else "normal", **kw)


def logique():
    fig, ax = new_fig(8.6, 3.4)
    ent = ["A", "B", "A and B", "A or B", "not A"]
    lignes = [("True", "True"), ("True", "False"), ("False", "True"), ("False", "False")]
    w, h = 1.7, 0.6
    for j, e in enumerate(ent):
        cellule(ax, j * w, 4 * h, w, h, e, fc=LBLUE, col=BLUE, bold=True)
    for i, (a, b) in enumerate(lignes):
        A, B = a == "True", b == "True"
        vals = [a, b, str(A and B), str(A or B), str(not A)]
        for j, v in enumerate(vals):
            fc = "white" if j < 2 else (LGREEN if v == "True" else "#fdecea")
            col = DARK if j < 2 else (GREEN if v == "True" else RED)
            cellule(ax, j * w, (3 - i) * h, w, h, v, fc=fc, col=col)
    ax.set_xlim(-0.1, 5 * w + 0.1)
    ax.set_ylim(-0.1, 5 * h + 0.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_algo_logique.png"))


def organigramme():
    fig, ax = new_fig(9.4, 5.6)
    ax.add_patch(FancyBboxPatch((-2.2, 4.3), 4.4, 0.8, boxstyle="round,pad=0.1", fc=LBLUE, ec=BLUE, lw=2))
    ax.text(0, 4.7, "delta = b*b - 4*a*c", ha="center", va="center", fontsize=12.5, color=DARK, **MONO)
    ax.annotate("", xy=(0, 3.75), xytext=(0, 4.2), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.6))
    losanges = [(0, 3.0, "delta > 0 ?"), (3.6, 1.2, "delta == 0 ?")]
    for x, y, s in losanges:
        ax.add_patch(Polygon([(x, y + 0.75), (x + 1.9, y), (x, y - 0.75), (x - 1.9, y)], closed=True, fc=LORANGE,
                             ec=ORANGE, lw=2))
        ax.text(x, y, s, ha="center", va="center", fontsize=12, color=DARK, **MONO)
    boites = [(-3.4, 1.2, "return 2", "Vrai"), (1.0, -0.8, "return 1", "Vrai"), (6.2, -0.8, "return 0", "Faux")]
    for x, y, s, _ in boites:
        ax.add_patch(FancyBboxPatch((x - 1.2, y - 0.35), 2.4, 0.7, boxstyle="round,pad=0.08", fc=LGREEN, ec=GREEN,
                                    lw=2))
        ax.text(x, y, s, ha="center", va="center", fontsize=12.5, color=DARK, **MONO)
    # liaisons
    ax.plot([-1.9, -3.4], [3.0, 3.0], color=NEUTRAL, lw=1.5)
    ax.annotate("", xy=(-3.4, 1.62), xytext=(-3.4, 3.0), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.5))
    txt(ax, -2.65, 3.12, "Vrai", GREEN, 12, ha="center", va="bottom", fontweight="bold")
    ax.plot([1.9, 3.6], [3.0, 3.0], color=NEUTRAL, lw=1.5)
    ax.annotate("", xy=(3.6, 1.98), xytext=(3.6, 3.0), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.5))
    txt(ax, 2.75, 3.12, "Faux", RED, 12, ha="center", va="bottom", fontweight="bold")
    ax.plot([1.7, 1.0], [1.2, 1.2], color=NEUTRAL, lw=1.5)
    ax.annotate("", xy=(1.0, -0.38), xytext=(1.0, 1.2), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.5))
    txt(ax, 1.35, 1.32, "Vrai", GREEN, 12, ha="center", va="bottom", fontweight="bold")
    ax.plot([5.5, 6.2], [1.2, 1.2], color=NEUTRAL, lw=1.5)
    ax.annotate("", xy=(6.2, -0.38), xytext=(6.2, 1.2), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.5))
    txt(ax, 5.85, 1.32, "Faux", RED, 12, ha="center", va="bottom", fontweight="bold")
    txt(ax, 1.4, -1.7, "if … elif … else : un seul bloc est exécuté, le premier dont la condition est vraie", DARK,
        12, ha="center", va="top")
    ax.set_xlim(-5.0, 7.8)
    ax.set_ylim(-2.3, 5.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_algo_organigramme.png"))


def ranges():
    fig, ax = new_fig(9.6, 3.8)
    cas = [("range(6)", range(6)), ("range(2, 7)", range(2, 7)), ("range(1, 10, 3)", range(1, 10, 3))]
    for r, (nom, vals) in enumerate(cas):
        y = 2.2 - r * 1.1
        ax.text(-0.3, y, nom, ha="right", va="center", fontsize=13, color=BLUE, **MONO)
        for k in range(11):
            on = k in vals
            ax.add_patch(Rectangle((k * 0.75, y - 0.3), 0.7, 0.6, fc=LGREEN if on else "white",
                                   ec=GREEN if on else "#d5dde3", lw=1.4 if on else 1))
            ax.text(k * 0.75 + 0.35, y, str(k), ha="center", va="center", fontsize=12,
                    color=GREEN if on else "#b0b8bf", fontweight="bold" if on else "normal", **MONO)
    txt(ax, 3.8, -1.05, "la borne de fin est toujours exclue", RED, 12.5, ha="center", va="center")
    ax.set_xlim(-3.6, 8.4)
    ax.set_ylim(-1.5, 2.8)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_algo_range.png"))


def trace_while():
    fig, ax = new_fig(10.0, 3.4)
    code = ["n = 0", "u = 2", "while u <= 20:", "    u = 1.5 * u", "    n = n + 1", "print(n)"]
    for k, l in enumerate(code):
        ax.add_patch(FancyBboxPatch((0, 2.6 - 0.52 * k - 0.23), 3.4, 0.46, boxstyle="round,pad=0.03", fc=CODE_BG,
                                    ec="none"))
        ax.text(0.15, 2.6 - 0.52 * k, l, color="#ecf0f1", fontsize=11.5, va="center", **MONO)
    ns = ["n", "0", "1", "2", "3", "4", "5", "6"]
    us = ["u", "2", "3", "4.5", "6.75", "10.125", "15.1875", "22.78…"]
    tests = ["u <= 20 ?", "oui", "oui", "oui", "oui", "oui", "oui", "non"]
    x0, w, h = 4.0, 0.92, 0.55
    for j in range(8):
        for r, vals in enumerate((ns, us, tests)):
            fc = "#ecf0f1" if j == 0 else "white"
            col = DARK
            if r == 2 and j > 0:
                col = GREEN if vals[j] == "oui" else RED
            if j == 7 and r == 0:
                fc, col = LGREEN, GREEN
            wj = 1.75 if j == 0 else w
            xj = x0 if j == 0 else x0 + 1.75 + (j - 1) * w
            ax.add_patch(Rectangle((xj, 2.3 - r * h), wj, h, fc=fc, ec=NEUTRAL, lw=1))
            ax.text(xj + wj / 2, 2.3 - r * h + h / 2, vals[j], ha="center", va="center",
                    fontsize=10 if (r == 1 and j >= 5) else 11.5, color=col,
                    fontweight="bold" if j == 0 or (j == 7 and r == 0) else "normal", **MONO)
    txt(ax, x0 + 4.3, 0.75, "la boucle s’arrête dès que u > 20 : le programme affiche 6", GREEN, 12, ha="center",
        va="center", fontweight="bold")
    ax.set_xlim(-0.2, 12.4)
    ax.set_ylim(-0.45, 3.0)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_algo_trace_while.png"))


def liste():
    fig, ax = new_fig(8.4, 3.0)
    L = [3, 7, 1, 9, 4]
    w = 1.2
    ax.text(-0.4, 1.0, "L =", ha="right", va="center", fontsize=15, color=DARK, **MONO)
    for k, v in enumerate(L):
        ax.add_patch(Rectangle((k * w, 0.6), w, 0.8, fc=LBLUE, ec=BLUE, lw=1.8))
        ax.text(k * w + w / 2, 1.0, str(v), ha="center", va="center", fontsize=17, color=DARK, fontweight="bold",
                **MONO)
        ax.text(k * w + w / 2, 1.65, str(k), ha="center", va="center", fontsize=13, color=GREEN, **MONO)
        ax.text(k * w + w / 2, 0.3, str(k - 5), ha="center", va="center", fontsize=13, color=ORANGE, **MONO)
    ax.text(6.3, 1.65, "indices positifs : L[0] vaut 3", ha="left", va="center", fontsize=12, color=GREEN)
    ax.text(6.3, 0.3, "indices négatifs : L[-1] vaut 4", ha="left", va="center", fontsize=12, color=ORANGE)
    ax.text(6.3, 1.0, "len(L) vaut 5", ha="left", va="center", fontsize=12, color=DARK)
    ax.set_xlim(-1.4, 11.2)
    ax.set_ylim(-0.1, 2.0)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_algo_liste.png"))


def append():
    fig, ax = new_fig(8.6, 3.4)
    etapes = [("u = [2]", [2]), ("u.append(3)", [2, 3]), ("u.append(3.5)", [2, 3, 3.5])]
    w = 1.0
    for r, (code, vals) in enumerate(etapes):
        y = 2.0 - r * 0.9
        ax.text(-0.3, y, code, ha="right", va="center", fontsize=13, color=BLUE, **MONO)
        for k, v in enumerate(vals):
            neuf = k == len(vals) - 1
            ax.add_patch(Rectangle((k * w, y - 0.32), w, 0.64, fc=LGREEN if neuf else LBLUE,
                                   ec=GREEN if neuf else BLUE, lw=1.6))
            ax.text(k * w + w / 2, y, f"{v:g}", ha="center", va="center", fontsize=13, color=DARK, **MONO)
    txt(ax, 1.5, -0.5, "termes de $u_{n+1} = 0{,}5\\,u_n + 2$ ajoutés un par un à la fin de la liste", DARK, 12,
        ha="center", va="center")
    ax.set_xlim(-3.6, 4.4)
    ax.set_ylim(-0.85, 2.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_algo_append.png"))


logique()
organigramme()
ranges()
trace_while()
liste()
append()
