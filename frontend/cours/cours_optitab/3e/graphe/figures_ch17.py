# -*- coding: utf-8 -*-
"""Figures du chapitre 17 (Algorithmique et programmation) — 3ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp

from fig3e import BLUE, ORANGE, GREEN, DARK, DIR_COURS, DIR_EXOS, ROOT
import scratch3e as S
from scripts_ch17 import SCRIPTS


def scripts():
    for nom, (scr, titres) in SCRIPTS.items():
        d = DIR_COURS if nom.startswith("cours_") else DIR_EXOS
        S.render(os.path.join(d, f"algo_3e_{nom}.png"), scr, titres)


def trace(path, nom, xlim, ylim, step=10, labels=(), w=5.6, h=5.0, arrow=True):
    res = S.run(SCRIPTS[nom][0])
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor("white")
    for (x1, y1), (x2, y2) in res["segs"]:
        ax.plot([x1, x2], [y1, y2], color=BLUE, lw=2.6, solid_capstyle="round", zorder=3)
    ax.scatter([0], [0], s=45, color=GREEN, zorder=5)
    ax.annotate("départ", (0, 0), textcoords="offset points", xytext=(-14, -16),
                fontsize=10.5, color=GREEN, fontweight="bold")
    for (x, y), t, off in labels:
        ax.scatter([x], [y], s=22, color=ORANGE, zorder=5)
        ax.annotate(t, (x, y), textcoords="offset points", xytext=off, fontsize=10.5,
                    color=ORANGE, fontweight="bold")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_xticks(range(int(xlim[0] // step * step), int(xlim[1]) + 1, step))
    ax.set_yticks(range(int(ylim[0] // step * step), int(ylim[1]) + 1, step))
    ax.grid(True, color="#e3e8ee", lw=0.8)
    ax.axhline(0, color="#9aa5b1", lw=1.0, zorder=1)
    ax.axvline(0, color="#9aa5b1", lw=1.0, zorder=1)
    ax.tick_params(labelsize=9, colors="#5d6d7e")
    for s in ax.spines.values():
        s.set_visible(False)
    fig.savefig(path, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


def tableur(path, ncols, nrows, cells, sel=None, formule=None, vert=(), widths=None):
    """cells : {'A1': 'x', ...} ; vert : cellules écrites en vert (résultats)."""
    cols = [chr(65 + i) for i in range(ncols)]
    widths = widths or [1.25] * ncols
    rh, hw = 0.34, 0.42
    W = hw + sum(widths)
    H = rh * (nrows + 1) + (0.55 if formule else 0)
    fig, ax = plt.subplots(figsize=(W + 0.1, H + 0.1))
    fig.patch.set_facecolor("white")
    top = H
    if formule:
        ax.add_patch(mp.Rectangle((0, H - 0.42), 0.7, 0.36, facecolor="white",
                                  edgecolor="#b0b7c3", lw=1.0))
        ax.text(0.35, H - 0.24, sel, ha="center", va="center", fontsize=10.5, color=DARK)
        ax.add_patch(mp.Rectangle((0.78, H - 0.42), W - 0.78, 0.36, facecolor="white",
                                  edgecolor="#b0b7c3", lw=1.0))
        ax.text(0.86, H - 0.24, "fx", ha="left", va="center", fontsize=10.5,
                color="#7b8794", style="italic")
        ax.text(1.18, H - 0.24, formule.replace("$", r"\$"), ha="left", va="center",
                fontsize=11, color=DARK, family="DejaVu Sans Mono")
        top = H - 0.55
    xs = [hw]
    for wd in widths:
        xs.append(xs[-1] + wd)
    ax.add_patch(mp.Rectangle((0, top - rh), W, rh, facecolor="#eef1f5", edgecolor="none"))
    ax.add_patch(mp.Rectangle((0, top - rh * (nrows + 1)), hw, rh * nrows,
                              facecolor="#eef1f5", edgecolor="none"))
    for i, c in enumerate(cols):
        ax.text((xs[i] + xs[i + 1]) / 2, top - rh / 2, c, ha="center", va="center",
                fontsize=10.5, color="#5d6d7e", fontweight="bold")
    for r in range(1, nrows + 1):
        ax.text(hw / 2, top - rh * r - rh / 2, str(r), ha="center", va="center",
                fontsize=10, color="#5d6d7e", fontweight="bold")
    for r in range(nrows + 2):
        ax.plot([0, W], [top - rh * r, top - rh * r], color="#c9d1db", lw=0.8)
    for x in [0] + xs:
        ax.plot([x, x], [top, top - rh * (nrows + 1)], color="#c9d1db", lw=0.8)
    for ref, val in cells.items():
        c, r = ord(ref[0]) - 65, int(ref[1:])
        y = top - rh * r - rh / 2
        num = isinstance(val, (int, float)) or (isinstance(val, str) and
                                                val.replace(",", "").replace("-", "").isdigit())
        txt = S.fmt(val) if isinstance(val, (int, float)) else val
        col = GREEN if ref in vert else DARK
        if num:
            ax.text(xs[c + 1] - 0.08, y, txt, ha="right", va="center", fontsize=10.5,
                    color=col, fontweight="bold" if ref in vert else "normal")
        else:
            ax.text(xs[c] + 0.08, y, txt, ha="left", va="center", fontsize=10.5, color=col,
                    fontweight="bold")
    if sel:
        c, r = ord(sel[0]) - 65, int(sel[1:])
        ax.add_patch(mp.Rectangle((xs[c], top - rh * (r + 1)), xs[c + 1] - xs[c], rh,
                                  facecolor="none", edgecolor="#1a7f37", lw=2.2, zorder=5))
    ax.set_xlim(-0.05, W + 0.05)
    ax.set_ylim(top - rh * (nrows + 1) - 0.05, H + 0.05)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    scripts()
    trace(os.path.join(DIR_COURS, "algo_3e_cours_bloc_trace.png"), "cours_bloc",
          (-15, 65), (-15, 65), labels=[((50, 50), "(50 ; 50)", (6, 4))], w=4.2, h=4.2)
    trace(os.path.join(DIR_EXOS, "algo_3e_carre_sol.png"), "carre", (-15, 55), (-15, 55),
          labels=[((40, 0), "(40 ; 0)", (4, -16)), ((40, 40), "(40 ; 40)", (4, 4)),
                  ((0, 40), "(0 ; 40)", (-30, 6))], w=4.4, h=4.4)
    trace(os.path.join(DIR_EXOS, "algo_3e_carres_sol.png"), "carres", (-10, 130), (-15, 45),
          labels=[((40, 0), "40", (-4, -16)), ((80, 0), "80", (-4, -16)),
                  ((120, 0), "120", (-6, -16))], w=7.4, h=3.0)
    trace(os.path.join(DIR_EXOS, "algo_3e_escalier_sol.png"), "escalier", (-15, 115),
          (-15, 115), step=20, labels=[((20, 20), "(20 ; 20)", (6, -12)),
                                       ((100, 100), "(100 ; 100)", (-30, 8))], w=4.8, h=4.8)
    trace(os.path.join(DIR_EXOS, "algo_3e_polygone_sol.png"), "polygone", (-30, 60),
          (-10, 65), labels=[((30, 0), "(30 ; 0)", (4, -16))], w=4.6, h=4.0)
    tableur(os.path.join(DIR_COURS, "algo_3e_cours_tableur.png"), 4, 5,
            {"A1": "Prix HT", "B1": "Prix TTC", "D1": "TVA", "D2": "0,2", "A2": 10, "A3": 25,
             "A4": 40, "A5": 100, "B2": 12, "B3": 30, "B4": 48, "B5": 120},
            sel="B3", formule="=A3*(1+$D$2)", widths=[1.2, 1.2, 0.8, 0.9])
    tableur(os.path.join(DIR_EXOS, "algo_3e_tableur.png"), 4, 6,
            {"A1": "x", "B1": "3x + b", "D1": "b", "D2": 5, "A2": 0, "A3": 1, "A4": 2,
             "A5": 3, "A6": 4, "B2": 5}, sel="B2", formule="=3*A2+$D$2",
            widths=[1.0, 1.2, 0.7, 0.8])
    tableur(os.path.join(DIR_EXOS, "algo_3e_tableur_sol.png"), 4, 6,
            {"A1": "x", "B1": "3x + b", "D1": "b", "D2": 5, "A2": 0, "A3": 1, "A4": 2,
             "A5": 3, "A6": 4, "B2": 5, "B3": 8, "B4": 11, "B5": 14, "B6": 17},
            sel="B6", formule="=3*A6+$D$2", vert=("B3", "B4", "B5", "B6"),
            widths=[1.0, 1.2, 0.7, 0.8])
    cells = {"A1": "Semaine", "B1": "Épargne (€)", "B2": 20, "B3": 35}
    cells.update({f"A{r}": r - 2 for r in range(2, 13)})
    tableur(os.path.join(DIR_EXOS, "algo_3e_epargne.png"), 2, 12, cells, sel="B3",
            formule="=B2+15", widths=[1.2, 1.5])
    print("Figures chapitre 17 : OK")
