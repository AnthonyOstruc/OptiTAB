# -*- coding: utf-8 -*-
"""Module de figures partagé pour la classe de 4ème du site OptiTAB.

Style maison (cf. Thales2.py et figures de la 3ème) : pas d'axes superflus,
bleu #3498db pour les éléments principaux, orange #e67e22 pour les éléments mis
en évidence ou les inconnues, vert #2e7d32 pour les réponses des corrections.
"""
import os
from math import radians, cos, sin, ceil, floor

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Polygon

BLUE = "#3498db"
ORANGE = "#e67e22"
GREEN = "#2e7d32"
RED = "#c0392b"
DARK = "#2c3e50"
NEUTRAL = "0.25"
GRID = "#d5dde3"

ROOT = r"c:/Users/SWEELCO-AT/Desktop/SWINDER/OptiTABV2/frontend"
DIR_COURS = os.path.join(ROOT, "cours/cours_optitab/4e/images")
DIR_EXOS = os.path.join(ROOT, "exercices/4e/images")
os.makedirs(DIR_COURS, exist_ok=True)
os.makedirs(DIR_EXOS, exist_ok=True)


# ---------------------------------------------------------------- base

def new_fig(w=8.2, h=5.2):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    return fig, ax


def finish(fig, ax, path, pts=None, margin=1.1, equal=True, axis_off=True):
    if pts is not None:
        pts = np.vstack([np.atleast_2d(p) for p in pts])
        ax.set_xlim(pts[:, 0].min() - margin, pts[:, 0].max() + margin)
        ax.set_ylim(pts[:, 1].min() - margin, pts[:, 1].max() + margin)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    if axis_off:
        ax.axis("off")
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


def dot_label(ax, P, name, dx, dy, color="0.1", s=70, fs=13):
    ax.scatter([P[0]], [P[1]], s=s, zorder=5, color=color)
    ax.annotate(name, (P[0], P[1]), textcoords="offset points", xytext=(dx, dy),
                fontsize=fs, color=DARK, fontweight="bold")


def seg_label(ax, P, Q, text, side=1, offset=0.42, t=0.5, color=DARK, fs=12.5,
              weight="normal"):
    P, Q = np.array(P, float), np.array(Q, float)
    u = Q - P
    L = np.linalg.norm(u)
    u = u / L
    nrm = np.array([-u[1], u[0]]) * side
    pos = P + t * (Q - P) + offset * nrm
    ax.text(pos[0], pos[1], text, color=color, fontsize=fs, ha="center",
            va="center", fontweight=weight)


def add_parallel_marks(ax, P, Q, n=2, size=0.24, spacing=0.3, color=NEUTRAL, lw=2.2):
    P, Q = np.array(P, float), np.array(Q, float)
    v = Q - P
    L = np.linalg.norm(v)
    if L == 0:
        return
    u = v / L
    ang = np.deg2rad(60)
    d = np.array([u[0] * cos(ang) - u[1] * sin(ang), u[0] * sin(ang) + u[1] * cos(ang)])
    mid = (P + Q) / 2
    ts = [0.0] if n == 1 else np.linspace(-spacing * (n - 1) / 2, spacing * (n - 1) / 2, n)
    for t in ts:
        c = mid + t * u
        a, b = c - (size / 2) * d, c + (size / 2) * d
        ax.plot([a[0], b[0]], [a[1], b[1]], lw=lw, color=color, solid_capstyle="round")


def tick_marks(ax, P, Q, n=1, size=0.2, spacing=0.14, color=NEUTRAL, lw=2.0):
    """Marques d'égalité de longueurs (petits traits perpendiculaires)."""
    P, Q = np.array(P, float), np.array(Q, float)
    u = (Q - P) / np.linalg.norm(Q - P)
    nrm = np.array([-u[1], u[0]])
    mid = (P + Q) / 2
    ts = [0.0] if n == 1 else np.linspace(-spacing * (n - 1) / 2, spacing * (n - 1) / 2, n)
    for t in ts:
        c = mid + t * u
        a, b = c - (size / 2) * nrm, c + (size / 2) * nrm
        ax.plot([a[0], b[0]], [a[1], b[1]], lw=lw, color=color, solid_capstyle="round")


def right_angle(ax, corner, d1, d2, size=0.32, color=NEUTRAL, lw=1.5):
    corner = np.array(corner, float)
    d1 = np.array(d1, float) / np.linalg.norm(d1)
    d2 = np.array(d2, float) / np.linalg.norm(d2)
    p1, p2, p3 = corner + size * d1, corner + size * (d1 + d2), corner + size * d2
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], lw=lw, color=color)


def angle_arc(ax, P, v1, v2, r=0.55, color=ORANGE, lw=1.8, n=1, dr=0.12,
              label=None, label_r=None, fs=12):
    """Arc(s) d'angle au sommet P entre les directions v1 et v2 (+ étiquette)."""
    P = np.array(P, float)
    a1 = np.degrees(np.arctan2(v1[1], v1[0])) % 360
    a2 = np.degrees(np.arctan2(v2[1], v2[0])) % 360
    if (a2 - a1) % 360 > 180:
        a1, a2 = a2, a1
    if a2 < a1:
        a2 += 360
    for i in range(n):
        rr = r + i * dr
        ax.add_patch(Arc(P, 2 * rr, 2 * rr, angle=0, theta1=a1, theta2=a2,
                         lw=lw, color=color))
    if label:
        am = radians((a1 + a2) / 2)
        lr = label_r if label_r is not None else r + 0.45
        ax.text(P[0] + lr * cos(am), P[1] + lr * sin(am), label, color=color,
                fontsize=fs, ha="center", va="center")


# ---------------------------------------------------------------- schémas de géométrie

def draw_schema(path, points, segments, labels=(), droits=(), measures=(),
                dots=None, w=8.2, h=5.2, extra=None, hidden=(), margin=1.1):
    """Schéma générique : points {nom: (x,y)}, segments [(P,Q)] ou [(P,Q,dict)],
    droits = angles droits [('A','B','C')] (sommet au milieu) ou ['A'] si ambigu,
    measures = [(P,Q,texte,kwargs)] pour seg_label, labels = [(nom,dx,dy)] sinon auto.
    """
    pts = {k: np.array(v, float) for k, v in points.items()}
    fig, ax = new_fig(w, h)
    for seg in segments:
        P, Q = pts[seg[0]], pts[seg[1]]
        kw = seg[2] if len(seg) > 2 else {}
        style = dict(lw=kw.get("lw", 2.2), color=kw.get("color", BLUE),
                     linestyle=kw.get("ls", "--" if (seg[0], seg[1]) in hidden else "-"),
                     zorder=kw.get("zorder", 2))
        ax.plot([P[0], Q[0]], [P[1], Q[1]], **style)
    for d in droits:
        if isinstance(d, (tuple, list)) and len(d) == 3:
            A, S, B = pts[d[0]], pts[d[1]], pts[d[2]]
            right_angle(ax, S, A - S, B - S)
    centroid = np.mean(np.vstack(list(pts.values())), axis=0)
    placed = {lbl[0]: (lbl[1], lbl[2]) for lbl in labels}
    for name, P in pts.items():
        if name.startswith("_"):
            continue
        if name in placed:
            dx, dy = placed[name]
        else:
            v = P - centroid
            nv = np.linalg.norm(v)
            v = v / nv if nv > 1e-9 else np.array([0.0, -1.0])
            dx, dy = 14 * v[0] - 5, 14 * v[1] - 4
        dot_label(ax, P, f"${name}$", dx, dy,
                  color="0.1" if name == "A" else BLUE, s=60)
    for m in measures:
        P, Q, text = pts[m[0]], pts[m[1]], m[2]
        kw = m[3] if len(m) > 3 else {}
        seg_label(ax, P, Q, text, **kw)
    if extra:
        extra(ax, pts)
    finish(fig, ax, path, list(pts.values()), margin=margin)


def triangle_rect(path, ab, ac, la="A", lb="B", lc="C", measures=(), extra=None,
                  droit=True, scale=None, w=7.5, h=5.0, labels=()):
    """Triangle rectangle en A : AB horizontal (longueur dessinée ab), AC vertical (ac)."""
    if scale:
        ab, ac = ab * scale, ac * scale
    points = {la: (0, 0), lb: (ab, 0), lc: (0, ac)}
    segs = [(la, lb), (lb, lc), (lc, la)]
    droits = [(lb, la, lc)] if droit else []
    draw_schema(path, points, segs, droits=droits, measures=measures,
                extra=extra, w=w, h=h, labels=labels)


# ---------------------------------------------------------------- repères et graphiques

def setup_repere(ax, xb, yb, xt=1, yt=1, xlabel="$x$", ylabel="$y$", grid=True,
                 unit_labels=True):
    xmin, xmax = xb
    ymin, ymax = yb
    if grid:
        for j in range(ceil(xmin / xt), floor(xmax / xt) + 1):
            ax.axvline(j * xt, color=GRID, lw=0.7, zorder=0)
        for j in range(ceil(ymin / yt), floor(ymax / yt) + 1):
            ax.axhline(j * yt, color=GRID, lw=0.7, zorder=0)
    ax.annotate("", xy=(xmax, 0), xytext=(xmin, 0),
                arrowprops=dict(arrowstyle="->", lw=1.4, color=NEUTRAL))
    ax.annotate("", xy=(0, ymax), xytext=(0, ymin),
                arrowprops=dict(arrowstyle="->", lw=1.4, color=NEUTRAL))
    ax.text(xmax - 0.02 * (xmax - xmin), 0.025 * (ymax - ymin), xlabel,
            fontsize=12, color=DARK, ha="right", va="bottom")
    ax.text(0.015 * (xmax - xmin), ymax - 0.07 * (ymax - ymin), ylabel,
            fontsize=12, color=DARK)
    if unit_labels:
        for j in range(ceil(xmin / xt), floor(xmax / xt) + 1):
            a = j * xt
            if a != 0 and xmin < a < xmax:
                lab = f"{a:g}".replace(".", ",")
                ax.text(a, -0.035 * (ymax - ymin), lab, fontsize=8.5, ha="center",
                        va="top", color=DARK,
                        bbox=dict(fc="white", ec="none", pad=0.4))
        for j in range(ceil(ymin / yt), floor(ymax / yt) + 1):
            a = j * yt
            if a != 0 and ymin < a < ymax:
                lab = f"{a:g}".replace(".", ",")
                ax.text(-0.012 * (xmax - xmin), a, lab, fontsize=8.5, ha="right",
                        va="center", color=DARK,
                        bbox=dict(fc="white", ec="none", pad=0.4))
    ax.text(-0.015 * (xmax - xmin), -0.035 * (ymax - ymin), "0", fontsize=9,
            ha="right", va="top", color=DARK)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)


def graphe(path, curves=(), points=(), segments=(), xb=(-5, 5), yb=(-4, 4),
           xt=1, yt=1, w=8.2, h=5.4, equal=False, extra=None, xlabel="$x$",
           ylabel="$y$", point_labels=True):
    """curves = [(fonction, lo, hi, couleur, label)], points = [(nom, x, y[, couleur])]."""
    fig, ax = new_fig(w, h)
    setup_repere(ax, xb, yb, xt, yt, xlabel, ylabel)
    for c in curves:
        fn, lo, hi = c[0], c[1], c[2]
        col = c[3] if len(c) > 3 else BLUE
        lab = c[4] if len(c) > 4 else None
        xs = np.linspace(lo, hi, 300)
        ys = np.array([fn(x) for x in xs])
        mask = (ys >= yb[0] - 0.5) & (ys <= yb[1] + 0.5)
        ax.plot(xs[mask], ys[mask], lw=2.2, color=col, zorder=3)
        if lab:
            xl = lab[1] if isinstance(lab, tuple) else (lo + hi) / 2
            txt = lab[0] if isinstance(lab, tuple) else lab
            yl = fn(xl)
            ax.annotate(txt, (xl, yl), textcoords="offset points", xytext=(8, 8),
                        fontsize=12.5, color=col, fontweight="bold")
    for s in segments:
        (x1, y1), (x2, y2) = s[0], s[1]
        kw = s[2] if len(s) > 2 else {}
        ax.plot([x1, x2], [y1, y2], lw=kw.get("lw", 1.6),
                color=kw.get("color", ORANGE), linestyle=kw.get("ls", "--"), zorder=2)
    for p in points:
        nom, x, y = p[0], p[1], p[2]
        col = p[3] if len(p) > 3 else ORANGE
        ax.scatter([x], [y], s=55, zorder=5, color=col)
        if point_labels and nom:
            ax.annotate(nom, (x, y), textcoords="offset points", xytext=(7, 7),
                        fontsize=12, color=col, fontweight="bold")
    if equal:
        ax.set_aspect("equal", adjustable="box")
    if extra:
        extra(ax)
    ax.axis("off")
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


# ---------------------------------------------------------------- statistiques

def barres(path, categories, valeurs, ylabel="Effectif", w=8.2, h=4.8,
           color=BLUE, highlight=None, ymax=None, annot=True):
    fig, ax = new_fig(w, h)
    cols = [ORANGE if highlight is not None and i == highlight else color
            for i in range(len(categories))]
    bars = ax.bar(range(len(categories)), valeurs, width=0.62, color=cols, zorder=3)
    if annot:
        for b, v in zip(bars, valeurs):
            ax.annotate(f"{v:g}".replace(".", ","), (b.get_x() + b.get_width() / 2, v),
                        textcoords="offset points", xytext=(0, 4), ha="center",
                        fontsize=11.5, color=DARK, fontweight="bold")
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories, fontsize=11.5, color=DARK)
    ax.set_ylabel(ylabel, fontsize=12, color=DARK)
    top = ymax if ymax else max(valeurs) * 1.18
    ax.set_ylim(0, top)
    ax.yaxis.grid(True, color=GRID, lw=0.8, zorder=0)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(NEUTRAL)
    ax.tick_params(colors=DARK)
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


# ---------------------------------------------------------------- arbres de probabilités

def arbre2(path, racines, feuilles=None, w=8.6, h=5.0):
    """Arbre à 1 ou 2 niveaux.
    racines  = [(etiquette, proba_texte)], feuilles = liste par racine de [(etiquette, proba_texte)].
    """
    fig, ax = new_fig(w, h)
    n = len(racines)
    y1 = np.linspace(0.78, 0.22, n) if n > 1 else [0.5]
    x0, x1, x2 = 0.04, 0.42, 0.86
    ax.scatter([x0], [0.5], s=50, color=DARK, zorder=5)
    for i, (lab, p) in enumerate(racines):
        ax.plot([x0, x1], [0.5, y1[i]], lw=2.0, color=BLUE, zorder=2)
        ax.text((x0 + x1) / 2 - 0.02, (0.5 + y1[i]) / 2 + 0.035, p, fontsize=12,
                color=BLUE, ha="center", fontweight="bold")
        ax.text(x1 + 0.015, y1[i], lab, fontsize=13, color=DARK, va="center",
                fontweight="bold")
        if feuilles:
            m = len(feuilles[i])
            spread = (0.30 if n > 1 else 0.5) * (m - 1) / max(m - 1, 1)
            ys = np.linspace(y1[i] + spread / 2, y1[i] - spread / 2, m) if m > 1 else [y1[i]]
            for j, (lab2, p2) in enumerate(feuilles[i]):
                ax.plot([x1 + 0.09, x2], [y1[i], ys[j]], lw=2.0, color=ORANGE, zorder=2)
                dy = 0.035 if ys[j] >= y1[i] else -0.06
                ax.text((x1 + 0.09 + x2) / 2, (y1[i] + ys[j]) / 2 + dy, p2,
                        fontsize=11.5, color=ORANGE, ha="center", fontweight="bold")
                ax.text(x2 + 0.012, ys[j], lab2, fontsize=12.5, color=DARK, va="center")
    ax.set_xlim(0, 1.04)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


# ---------------------------------------------------------------- solides (perspective cavalière)

def _proj(x, y, z, k=0.45, ang=35):
    """Perspective cavalière : y = profondeur."""
    return (x + k * y * cos(radians(ang)), z + k * y * sin(radians(ang)))


def _edges(ax, verts, edges, hidden_edges=(), color=BLUE, lw=2.0):
    for e in edges:
        (x1, y1), (x2, y2) = verts[e[0]], verts[e[1]]
        ls = "--" if e in hidden_edges or (e[1], e[0]) in hidden_edges else "-"
        ax.plot([x1, x2], [y1, y2], lw=lw if ls == "-" else 1.4, color=color,
                linestyle=ls, zorder=2)


def pave(path, L=5, P=3, H=2.6, noms="ABCDEFGH", measures=(), w=7.6, h=5.0,
         extra=None, diagonales=()):
    """Pavé droit ABCDEFGH : ABCD face avant (A bas gauche), EFGH face arrière.
    measures = [(arete, texte)] avec arete parmi 'AB','AD','AE'... ;
    diagonales = [('A','G', couleur)] tracées en pointillés épais.
    """
    V = {}
    coords = {
        noms[0]: (0, 0, 0), noms[1]: (L, 0, 0), noms[2]: (L, 0, H), noms[3]: (0, 0, H),
        noms[4]: (0, P, 0), noms[5]: (L, P, 0), noms[6]: (L, P, H), noms[7]: (0, P, H),
    }
    for k3, (x, y, z) in coords.items():
        V[k3] = _proj(x, y, z)
    A, B, C, D, E, F, G, Hh = noms
    edges = [(A, B), (B, C), (C, D), (D, A), (E, F), (F, G), (G, Hh), (Hh, E),
             (A, E), (B, F), (C, G), (D, Hh)]
    hidden = [(E, F), (Hh, E), (A, E)]
    fig, ax = new_fig(w, h)
    _edges(ax, V, edges, hidden)
    for d in diagonales:
        P1, P2 = V[d[0]], V[d[1]]
        col = d[2] if len(d) > 2 else ORANGE
        ax.plot([P1[0], P2[0]], [P1[1], P2[1]], lw=2.4, color=col, linestyle="--",
                zorder=3)
    for name, (x, y) in V.items():
        off = {A: (-16, -14), B: (8, -14), C: (8, 4), D: (-16, 4),
               E: (-16, -12), F: (10, -12), G: (10, 4), Hh: (-16, 6)}[name]
        dot_label(ax, (x, y), f"${name}$", off[0], off[1], color=BLUE, s=38)
    for m in measures:
        a, txt = m[0], m[1]
        kw = m[2] if len(m) > 2 else {}
        seg_label(ax, V[a[0]], V[a[1]], txt, **({"side": -1, "offset": 0.38} | kw))
    if extra:
        extra(ax, V)
    finish(fig, ax, path, list(V.values()), margin=0.9)


def pyramide(path, base=4.2, prof=3.2, haut=4.0, noms="ABCDS", measures=(),
             w=7.2, h=5.2, extra=None, hauteur=True):
    """Pyramide à base rectangulaire ABCD de sommet S, hauteur tracée en pointillés."""
    A3 = (0, 0, 0)
    B3 = (base, 0, 0)
    C3 = (base, prof, 0)
    D3 = (0, prof, 0)
    S3 = (base / 2, prof / 2, haut)
    O3 = (base / 2, prof / 2, 0)
    V = {n: _proj(*c) for n, c in zip(noms, [A3, B3, C3, D3, S3])}
    O = _proj(*O3)
    A, B, C, D, S = noms
    fig, ax = new_fig(w, h)
    _edges(ax, V, [(A, B), (B, C), (C, D), (D, A)], hidden_edges=[(C, D), (D, A)])
    for X in (A, B, C, D):
        ax.plot([V[X][0], V[S][0]], [V[X][1], V[S][1]], lw=2.0, color=BLUE,
                linestyle="--" if X == D else "-")
    if hauteur:
        ax.plot([O[0], V[S][0]], [O[1], V[S][1]], lw=1.6, color=ORANGE, linestyle="--")
        ax.scatter([O[0]], [O[1]], s=28, color=ORANGE, zorder=5)
        ax.annotate("$O$", O, textcoords="offset points", xytext=(6, -12),
                    fontsize=12, color=ORANGE, fontweight="bold")
    offs = {A: (-16, -14), B: (8, -14), C: (10, -4), D: (-16, 2), S: (-4, 10)}
    for n in noms:
        dot_label(ax, V[n], f"${n}$", *offs[n], color=BLUE, s=38)
    for m in measures:
        a, txt = m[0], m[1]
        kw = m[2] if len(m) > 2 else {}
        P1 = V[a[0]] if a[0] in V else O
        P2 = V[a[1]] if a[1] in V else O
        seg_label(ax, P1, P2, txt, **({"side": -1, "offset": 0.38} | kw))
    if extra:
        extra(ax, V | {"O": O})
    finish(fig, ax, path, list(V.values()) + [O], margin=0.9)


def cylindre(path, r=1.6, h=3.4, mesures=("r", "h"), w=5.8, hh=5.0, color=BLUE):
    fig, ax = new_fig(w, hh)
    t = np.linspace(0, 2 * np.pi, 120)
    ax.plot(r * np.cos(t), 0.32 * r * np.sin(t) + h, lw=2.0, color=color)
    ax.plot(r * np.cos(t[t > np.pi]), 0.32 * r * np.sin(t[t > np.pi]), lw=2.0, color=color)
    ax.plot(r * np.cos(t[t <= np.pi]), 0.32 * r * np.sin(t[t <= np.pi]), lw=1.3,
            color=color, linestyle="--")
    ax.plot([-r, -r], [0, h], lw=2.0, color=color)
    ax.plot([r, r], [0, h], lw=2.0, color=color)
    if mesures[0]:
        ax.plot([0, r], [h, h], lw=1.6, color=ORANGE)
        ax.scatter([0], [h], s=25, color=ORANGE, zorder=5)
        ax.text(r / 2, h + 0.28, f"${mesures[0]}$", color=ORANGE, fontsize=13,
                ha="center", fontweight="bold")
    if mesures[1]:
        ax.text(r + 0.3, h / 2, f"${mesures[1]}$", color=ORANGE, fontsize=13,
                va="center", fontweight="bold")
    finish(fig, ax, path, [(-r - 1, -r), (r + 1.2, h + r)])


def cone(path, r=1.8, h=3.6, mesures=("r", "h"), w=5.8, hh=5.2):
    fig, ax = new_fig(w, hh)
    t = np.linspace(0, 2 * np.pi, 120)
    ax.plot(r * np.cos(t[t > np.pi]), 0.3 * r * np.sin(t[t > np.pi]), lw=2.0, color=BLUE)
    ax.plot(r * np.cos(t[t <= np.pi]), 0.3 * r * np.sin(t[t <= np.pi]), lw=1.3,
            color=BLUE, linestyle="--")
    ax.plot([-r, 0], [0, h], lw=2.0, color=BLUE)
    ax.plot([r, 0], [0, h], lw=2.0, color=BLUE)
    ax.plot([0, 0], [0, h], lw=1.6, color=ORANGE, linestyle="--")
    right_angle(ax, (0, 0), (1, 0), (0, 1), size=0.22, color=ORANGE)
    if mesures[0]:
        ax.plot([0, r], [0, 0], lw=1.6, color=ORANGE)
        ax.text(r / 2, -0.42, f"${mesures[0]}$", color=ORANGE, fontsize=13,
                ha="center", fontweight="bold")
    if mesures[1]:
        ax.text(-0.35, h / 2, f"${mesures[1]}$", color=ORANGE, fontsize=13,
                ha="right", fontweight="bold")
    ax.scatter([0], [h], s=35, color=BLUE, zorder=5)
    ax.annotate("$S$", (0, h), textcoords="offset points", xytext=(6, 6),
                fontsize=13, color=DARK, fontweight="bold")
    finish(fig, ax, path, [(-r - 1, -r), (r + 1, h + 0.8)])


def sphere_section(path, R=2.6, d=1.4, w=6.4, hh=6.0):
    """Sphère de rayon R coupée par un plan à distance d du centre."""
    r = (R * R - d * d) ** 0.5
    fig, ax = new_fig(w, hh)
    t = np.linspace(0, 2 * np.pi, 160)
    ax.plot(R * np.cos(t), R * np.sin(t), lw=2.0, color=BLUE)
    ax.plot(r * np.cos(t), 0.26 * r * np.sin(t) + d, lw=1.8, color=ORANGE)
    O = (0, 0)
    Hc = (0, d)
    M = (r, d)
    for P, nom, off, col in [(O, "O", (-14, -12), DARK), (Hc, "H", (-14, 4), ORANGE),
                             (M, "M", (8, 2), ORANGE)]:
        ax.scatter([P[0]], [P[1]], s=38, color=col, zorder=5)
        ax.annotate(f"${nom}$", P, textcoords="offset points", xytext=off,
                    fontsize=13, color=col, fontweight="bold")
    ax.plot([0, 0], [0, d], lw=1.7, color=DARK)
    ax.plot([0, r], [d, d], lw=1.7, color=ORANGE)
    ax.plot([0, r], [0, d], lw=1.7, color=BLUE, linestyle="--")
    right_angle(ax, (0, d), (0, -1), (1, 0), size=0.22, color=DARK)
    finish(fig, ax, path, [(-R - 0.6, -R - 0.6), (R + 0.6, R + 0.6)])


# ---------------------------------------------------------------- ajouts 4ème

def _save(fig, path):
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


def tableau(path, lignes, entete_col=True, entete_lig=True, larg_col=None,
            haut=0.62, fs=13, surligne=(), vert=(), titre=None):
    """Tableau de données dessiné (lisible sur mobile, pas de HTML).
    lignes = liste de listes de textes (mathtext autorisé : '$-3$').
    surligne = cellules (i, j) en orange ; vert = cellules (i, j) en vert (corrections).
    """
    nl, nc = len(lignes), max(len(r) for r in lignes)
    if larg_col is None:
        larg_col = [max(1.25, 0.16 * max(len(str(r[j])) for r in lignes if j < len(r)))
                    for j in range(nc)]
    W = sum(larg_col)
    fig, ax = new_fig(min(11.5, 0.95 * W + 0.6), 0.62 * nl * haut / 0.62 + (0.5 if titre else 0.2))
    y0 = 0
    for i, r in enumerate(lignes):
        x = 0
        for j in range(nc):
            txt = r[j] if j < len(r) else ""
            head = (entete_col and i == 0) or (entete_lig and j == 0)
            fc = "#e8f4fd" if head else "white"
            col = DARK
            if (i, j) in surligne:
                fc, col = "#fdebd0", ORANGE
            if (i, j) in vert:
                fc, col = "#e8f5e9", GREEN
            ax.add_patch(Polygon([(x, y0 - i * haut), (x + larg_col[j], y0 - i * haut),
                                  (x + larg_col[j], y0 - (i + 1) * haut),
                                  (x, y0 - (i + 1) * haut)], closed=True, facecolor=fc,
                                 edgecolor=BLUE, lw=1.3))
            ax.text(x + larg_col[j] / 2, y0 - (i + 0.5) * haut, txt, ha="center",
                    va="center", fontsize=fs, color=col,
                    fontweight="bold" if head or (i, j) in vert else "normal")
            x += larg_col[j]
    if titre:
        ax.text(W / 2, 0.32, titre, ha="center", va="bottom", fontsize=fs, color=DARK,
                fontweight="bold")
    ax.set_xlim(-0.05, W + 0.05)
    ax.set_ylim(-nl * haut - 0.05, 0.75 if titre else 0.05)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


def droite_graduee(path, lo, hi, pas=1, points=(), fleches=(), w=9.0, h=1.9,
                   etiquettes_tous=True, sous=None):
    """Droite graduée de lo à hi. points = [(nom, x, couleur)] ;
    fleches = [(x1, x2, texte, couleur, hauteur)] (bonds au-dessus de la droite)."""
    fig, ax = new_fig(w, h)
    ax.annotate("", xy=(hi + 0.6 * pas, 0), xytext=(lo - 0.4 * pas, 0),
                arrowprops=dict(arrowstyle="->", lw=1.6, color=NEUTRAL))
    k = 0
    x = lo
    while x <= hi + 1e-9:
        ax.plot([x, x], [-0.12, 0.12], lw=1.3, color=NEUTRAL)
        if etiquettes_tous or abs(x) < 1e-9:
            ax.text(x, -0.32, f"{x:g}".replace(".", ",").replace("-", "−"), ha="center",
                    va="top", fontsize=11.5, color=DARK)
        k += 1
        x = lo + k * pas
    for p in points:
        nom, xx = p[0], p[1]
        col = p[2] if len(p) > 2 else ORANGE
        ax.scatter([xx], [0], s=70, color=col, zorder=5)
        if fleches:
            ax.text(xx, -0.62, nom, ha="center", va="top", fontsize=12.5, color=col,
                    fontweight="bold")
        else:
            ax.text(xx, 0.32, nom, ha="center", va="bottom", fontsize=13, color=col,
                    fontweight="bold")
    for f in fleches:
        x1, x2, txt = f[0], f[1], f[2]
        col = f[3] if len(f) > 3 else BLUE
        hh = f[4] if len(f) > 4 else 0.9
        ax.add_patch(FancyArrowPatch((x1, 0.18), (x2, 0.18), connectionstyle=f"arc3,rad={-0.45 if x2 > x1 else 0.45}",
                                     arrowstyle="-|>", mutation_scale=14, lw=1.8, color=col))
        ax.text((x1 + x2) / 2, 0.18 + hh * 0.75, txt, ha="center", va="bottom",
                fontsize=12, color=col, fontweight="bold")
    if sous:
        ax.text((lo + hi) / 2, -1.05 if fleches else -0.95, sous, ha="center", va="top", fontsize=12, color=DARK)
    ax.set_xlim(lo - 0.7 * pas, hi + 0.8 * pas)
    ax.set_ylim((-1.45 if fleches else -1.3) if sous else (-1.0 if fleches else -0.8),
                max([0.9] + [0.18 + (f[4] if len(f) > 4 else 0.9) * 0.75 + 0.45 for f in fleches]))
    ax.axis("off")
    _save(fig, path)


def thermometre(path, valeurs, lo=-10, hi=10, pas=2, w=3.2, h=6.0, titre=None):
    """Thermomètre vertical ; valeurs = [(texte, temperature, couleur)]."""
    fig, ax = new_fig(w, h)
    ax.add_patch(Polygon([(-0.25, lo - 0.5), (0.25, lo - 0.5), (0.25, hi + 0.5),
                          (-0.25, hi + 0.5)], closed=True, facecolor="#f4f6f7",
                         edgecolor=NEUTRAL, lw=1.4))
    for t in range(lo, hi + 1, pas):
        ax.plot([0.25, 0.5], [t, t], lw=1.2, color=NEUTRAL)
        ax.text(0.62, t, f"{t}".replace("-", "−"), va="center", fontsize=10.5, color=DARK)
    ax.plot([-0.25, 0.25], [0, 0], lw=1.6, color=DARK)
    for txt, t, col in valeurs:
        ax.plot([-0.45, 0.25], [t, t], lw=2.4, color=col)
        ax.text(-0.55, t, txt, ha="right", va="center", fontsize=11.5, color=col,
                fontweight="bold")
    if titre:
        ax.text(0, hi + 1.3, titre, ha="center", fontsize=12, color=DARK, fontweight="bold")
    ax.set_xlim(-3.2, 1.6)
    ax.set_ylim(lo - 1.2, hi + 2.2)
    ax.axis("off")
    _save(fig, path)
