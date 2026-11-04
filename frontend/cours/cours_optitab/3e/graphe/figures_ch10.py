# -*- coding: utf-8 -*-
"""Figures du chapitre 10 (Statistiques) — 3ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import (new_fig, barres, BLUE, ORANGE, GREEN, DARK, GRID, NEUTRAL,
                   DIR_COURS, DIR_EXOS, ROOT)
import matplotlib.pyplot as plt


def save(fig, path):
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


# Cours — diagramme en bâtons des notes (6:2, 8:3, 10:6, 12:5, 16:4)
for dossier in (DIR_COURS, DIR_EXOS):
    barres(os.path.join(dossier, "statistiques_3e_batons.png"),
           ["6", "8", "10", "12", "16"], [2, 3, 6, 5, 4],
           ylabel="Effectif", highlight=2)

# E — diagramme circulaire (A:10, B:18, C:12 sur 40)
def disque():
    fig, ax = plt.subplots(figsize=(6.0, 5.2))
    fig.patch.set_facecolor("white")
    vals = [10, 18, 12]
    labels = ["A : 90°", "B : 162°", "C : 108°"]
    cols = [BLUE, ORANGE, GREEN]
    wedges, texts = ax.pie(vals, labels=labels, colors=cols, startangle=90,
                           counterclock=False,
                           wedgeprops=dict(edgecolor="white", linewidth=2.5),
                           textprops=dict(fontsize=13, color=DARK, fontweight="bold"))
    ax.set_aspect("equal")
    save(fig, os.path.join(DIR_EXOS, "statistiques_3e_disque.png"))

disque()

# E — histogramme de classes de même largeur
def histogramme():
    fig, ax = new_fig(8.2, 4.8)
    classes = [(0, 10, 4), (10, 20, 8), (20, 30, 6), (30, 40, 2)]
    for a, b, eff in classes:
        ax.bar(a, eff, width=b - a, align="edge", color=BLUE if a != 10 else ORANGE,
               edgecolor="white", linewidth=2, zorder=3)
        ax.text((a + b) / 2, eff + 0.2, str(eff), ha="center", fontsize=12,
                color=DARK, fontweight="bold")
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.set_xlabel("durée (min)", fontsize=12, color=DARK)
    ax.set_ylabel("effectif", fontsize=12, color=DARK)
    ax.set_ylim(0, 9.5)
    ax.yaxis.grid(True, color=GRID, lw=0.8, zorder=0)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    save(fig, os.path.join(DIR_EXOS, "statistiques_3e_histogramme.png"))

histogramme()

# P — graphique trompeur (axe tronqué à 78) vs axe complet
def axe_tronque():
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.2))
    fig.patch.set_facecolor("white")
    for ax, (lo, titre) in zip(axes, [(78, "Axe commençant à 78"), (0, "Axe commençant à 0")]):
        ax.bar([0, 1], [80, 84], width=0.55, color=[BLUE, ORANGE], zorder=3)
        ax.set_ylim(lo, 86 if lo else 96)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["2025", "2026"], fontsize=11.5)
        ax.set_title(titre, fontsize=12.5, color=DARK, fontweight="bold")
        ax.yaxis.grid(True, color=GRID, lw=0.8, zorder=0)
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)
        for i, v in enumerate([80, 84]):
            ax.text(i, v + 0.3 if lo else v + 1.5, str(v), ha="center",
                    fontsize=11.5, color=DARK, fontweight="bold")
    fig.tight_layout()
    save(fig, os.path.join(DIR_EXOS, "statistiques_3e_axe.png"))

axe_tronque()
print("Figures chapitre 10 : OK")
