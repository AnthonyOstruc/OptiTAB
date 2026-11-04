# -*- coding: utf-8 -*-
"""Rendu de scripts de blocs (style Scratch 3) et tortue de dessin — 4ème OptiTAB.

Un script est une liste de blocs :
  ("hat", texte, cat)                         bloc chapeau (événement, définition)
  ("cmd", texte, cat)                         bloc commande
  ("c", texte, cat, [enfants])                boucle ou « si … alors »
  ("ce", texte, cat, [enfants], [sinon])      « si … alors … sinon »
Dans le texte : (…) champ blanc, […] menu, {…} variable, «…» opérateur, ⟨…⟩ condition.
"""
import re
from math import sin, cos, radians

import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, Polygon
from matplotlib.textpath import TextPath

CAT = {"mvt": ("#4C97FF", "#3373CC"), "app": ("#9966FF", "#774DCB"), "evt": ("#FFBF00", "#CC9900"),
       "ctrl": ("#FFAB19", "#CF8B17"), "cap": ("#5CB1D6", "#2E8EB8"), "ope": ("#59C059", "#389438"),
       "var": ("#FF8C1A", "#DB6E00"), "sty": ("#0FBD8C", "#0B8E69"), "mes": ("#FF6680", "#FF3355")}
U = 0.40          # pouces par unité
FS = 11.5
H_ROW, H_HAT, ARM, FOOT = 0.98, 1.2, 0.55, 0.5
FP = FontProperties(family="DejaVu Sans", weight="bold")
TOKEN = re.compile(r"(\([^()]*\)|\[[^\]]*\]|\{[^}]*\}|«[^»]*»|⟨[^⟩]*⟩)")


def largeur(s, fs=FS):
    if not s:
        return 0.0
    return TextPath((0, 0), s, size=fs, prop=FP).get_extents().width / 72 / U


def jetons(texte):
    out = []
    for part in TOKEN.split(texte):
        if not part:
            continue
        if part[0] in "([{«⟨":
            out.append((part[0], part[1:-1]))
        else:
            out.append(("t", part.strip()))
    return [j for j in out if j[1] != "" or j[0] != "t"]


def largeur_jeton(j):
    k, s = j
    if k == "t":
        return largeur(s) + 0.18
    return largeur(s, FS - 0.5) + 0.62 + 0.14


def largeur_ligne(texte):
    return 0.32 + sum(largeur_jeton(j) for j in jetons(texte)) + 0.2


def dessiner_ligne(ax, texte, x, yc, cat):
    fond, bord = CAT[cat]
    xx = x + 0.32
    for k, s in jetons(texte):
        if k == "t":
            ax.text(xx, yc, s, color="white", fontsize=FS, fontproperties=FP, va="center", ha="left", zorder=5)
            xx += largeur(s) + 0.18
            continue
        w = largeur(s, FS - 0.5) + 0.62
        if k == "(":
            fc, ec, tc, style = "white", bord, "#575E75", "round,pad=0,rounding_size=0.3"
        elif k == "[":
            fc, ec, tc, style = bord, bord, "white", "round,pad=0,rounding_size=0.12"
        elif k == "{":
            col = CAT["cap"] if s == "réponse" else CAT["var"]
            fc, ec, tc, style = col[0], col[1], "white", "round,pad=0,rounding_size=0.3"
        elif k == "«":
            fc, ec, tc, style = CAT["ope"][0], CAT["ope"][1], "white", "round,pad=0,rounding_size=0.3"
        else:
            fc, ec, tc, style = CAT["ope"][0], CAT["ope"][1], "white", "round,pad=0,rounding_size=0.08"
        ax.add_patch(FancyBboxPatch((xx, yc - 0.31), w, 0.62, boxstyle=style, facecolor=fc, edgecolor=ec, lw=1.1,
                                    zorder=4))
        ax.text(xx + w / 2, yc, s, color=tc, fontsize=FS - 0.5, fontproperties=FP, va="center", ha="center",
                zorder=5)
        xx += w + 0.14


def mesurer(blocs):
    """Largeur maximale (en unités) occupée par une pile de blocs."""
    m = 0.0
    for b in blocs:
        m = max(m, largeur_ligne(b[1]))
        if b[0] in ("c", "ce"):
            m = max(m, ARM + mesurer(b[3]))
            if b[0] == "ce":
                m = max(m, ARM + mesurer(b[4]), largeur_ligne("sinon"))
    return m


def pile(ax, blocs, x, y):
    """Dessine une pile de blocs à partir du coin haut gauche (x, y) ; renvoie le y du bas."""
    for b in blocs:
        kind, texte, cat = b[0], b[1], b[2]
        fond, bord = CAT[cat]
        w = largeur_ligne(texte)
        if kind == "hat":
            ax.add_patch(FancyBboxPatch((x, y - H_HAT), max(w, 3.0), H_HAT - 0.2,
                                        boxstyle="round,pad=0,rounding_size=0.2", facecolor=fond, edgecolor=bord,
                                        lw=1.3, zorder=2))
            t = np.linspace(0, np.pi, 40)
            ax.fill(x + 0.95 + 0.95 * np.cos(t), y - 0.2 + 0.32 * np.sin(t), color=fond, zorder=2)
            ax.plot(x + 0.95 + 0.95 * np.cos(t), y - 0.2 + 0.32 * np.sin(t), color=bord, lw=1.3, zorder=2)
            dessiner_ligne(ax, texte, x, y - 0.2 - (H_HAT - 0.2) / 2, cat)
            y -= H_HAT
        elif kind == "cmd":
            ax.add_patch(FancyBboxPatch((x, y - H_ROW), w, H_ROW, boxstyle="round,pad=0,rounding_size=0.12",
                                        facecolor=fond, edgecolor=bord, lw=1.3, zorder=2))
            dessiner_ligne(ax, texte, x, y - H_ROW / 2, cat)
            y -= H_ROW
        else:
            haut = y
            y_in = y - H_ROW
            y_bas1 = pile(ax, b[3], x + ARM, y_in) if b[3] else y_in - 0.5
            if kind == "ce":
                y_sinon = y_bas1 - H_ROW
                y_bas2 = pile(ax, b[4], x + ARM, y_sinon) if b[4] else y_sinon - 0.5
            else:
                y_sinon, y_bas2 = None, y_bas1
            y_fin = y_bas2 - FOOT
            wf = max(2.6, w * 0.45)
            pts = [(x, haut), (x + w, haut), (x + w, y_in), (x + ARM, y_in)]
            if kind == "ce":
                pts += [(x + ARM, y_bas1), (x + max(w, 2.6), y_bas1), (x + max(w, 2.6), y_sinon), (x + ARM, y_sinon)]
            pts += [(x + ARM, y_bas2), (x + wf, y_bas2), (x + wf, y_fin), (x, y_fin)]
            ax.add_patch(Polygon(pts, closed=True, facecolor=fond, edgecolor=bord, lw=1.3, zorder=1,
                                 joinstyle="round"))
            dessiner_ligne(ax, texte, x, haut - H_ROW / 2, cat)
            if kind == "ce":
                dessiner_ligne(ax, "sinon", x, y_bas1 - H_ROW / 2, cat)
            y = y_fin
    return y


def hauteur(blocs):
    h = 0.0
    for b in blocs:
        if b[0] == "hat":
            h += H_HAT
        elif b[0] == "cmd":
            h += H_ROW
        else:
            h += H_ROW + (hauteur(b[3]) if b[3] else 0.5) + FOOT
            if b[0] == "ce":
                h += H_ROW + (hauteur(b[4]) if b[4] else 0.5)
    return h


def figure_scripts(path, scripts, titres=None, ecart=1.2, sauver=None, vertical=False):
    """Plusieurs piles côte à côte, ou les unes sous les autres (titres optionnels au-dessus)."""
    import matplotlib.pyplot as plt
    ws = [mesurer(s) for s in scripts]
    hs = [hauteur(s) for s in scripts]
    if vertical:
        W = max(ws) + 0.6
        H = sum(hs) + len(scripts) * (0.9 if titres else 0.3) + ecart * (len(scripts) - 1) + 0.3
        fig = plt.figure(figsize=(W * U, H * U))
        ax = fig.add_axes([0, 0, 1, 1])
        y = H - 0.1
        for i, s in enumerate(scripts):
            if titres:
                ax.text(0.3, y - 0.4, titres[i], fontsize=FS + 1, color="#2c3e50", fontweight="bold", va="center")
                y -= 0.9
            y = pile(ax, s, 0.3, y) - ecart
        ax.set_xlim(0, W)
        ax.set_ylim(0, H)
        ax.set_aspect("equal")
        ax.axis("off")
        (sauver or _save_default)(fig, path)
        return
    W = sum(ws) + ecart * (len(scripts) - 1) + 0.6
    H = max(hs) + (0.9 if titres else 0.3) + 0.4
    fig = plt.figure(figsize=(W * U, H * U))
    ax = fig.add_axes([0, 0, 1, 1])
    fig.patch.set_facecolor("white")
    x = 0.3
    for i, s in enumerate(scripts):
        top = H - (0.9 if titres else 0.35)
        if titres:
            ax.text(x, H - 0.45, titres[i], fontsize=FS + 1, color="#2c3e50", fontweight="bold", va="center")
        pile(ax, s, x, top)
        x += ws[i] + ecart
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")
    (sauver or _save_default)(fig, path)


def _save_default(fig, path):
    import matplotlib.pyplot as plt
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)


class Tortue:
    """Lutin Scratch : orientation 90 = vers la droite, rotation ↻ = sens horaire."""

    def __init__(self, x=0.0, y=0.0, o=90.0):
        self.x, self.y, self.o, self.stylo = x, y, o, False
        self.traits = []

    def aller(self, x, y):
        if self.stylo:
            self.traits.append(((self.x, self.y), (x, y)))
        self.x, self.y = x, y

    def avancer(self, d):
        self.aller(self.x + d * sin(radians(self.o)), self.y + d * cos(radians(self.o)))

    def horaire(self, a):
        self.o += a

    def antihoraire(self, a):
        self.o -= a
