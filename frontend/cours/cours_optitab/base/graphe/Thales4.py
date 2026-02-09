import numpy as np
import matplotlib.pyplot as plt

# --- Configuration "contraposée" : B'C' n'est PAS parallèle à BC (aucune valeur affichée) ---

A = np.array([0.0, 0.0])

# Deux demi-droites sécantes issues de A
ray1_dir = np.array([1.0, 0.0])  # d1
ray2_dir = np.array([np.cos(np.deg2rad(55)), np.sin(np.deg2rad(55))])  # d2

# Points B,C sur les demi-droites
B = A + 4.0 * ray1_dir
C = A + 3.6 * ray2_dir

# Points B',C' sur les mêmes demi-droites mais avec des rapports différents => B'C' non // BC
Bp = A + 6.2 * ray1_dir
Cp = A + 4.6 * ray2_dir  # pas le même facteur que pour C

# Pour tracer les deux droites sécantes un peu plus loin
P1_end = A + 1.12 * (Bp - A)
P2_end = A + 1.12 * (Cp - A)

fig, ax = plt.subplots(figsize=(9, 5.5))

# Couleurs sobres (bleu/orange)
c_sec = "tab:blue"
c_seg = "tab:orange"
c_edge = "0.15"

# Droites sécantes
ax.plot([A[0], P1_end[0]], [A[1], P1_end[1]], linewidth=2.4, color=c_sec)
ax.plot([A[0], P2_end[0]], [A[1], P2_end[1]], linewidth=2.4, color=c_sec)

# Segments BC et B'C' (non parallèles)
ax.plot([B[0], C[0]],   [B[1], C[1]],   linewidth=2.8, color=c_seg)
ax.plot([Bp[0], Cp[0]], [Bp[1], Cp[1]], linewidth=2.8, color=c_seg, linestyle="--")

# Points (cercles blancs)
points = {"A": A, "B": B, "C": C, "B'": Bp, "C'": Cp}
sizes  = {"A": 90, "B": 75, "C": 75, "B'": 70, "C'": 70}
for name, p in points.items():
    ax.scatter(p[0], p[1], s=sizes[name], facecolors="white",
               edgecolors=c_edge, linewidths=2.2, zorder=3)

# Labels (décalés pour ne pas toucher les lignes)
offsets = {
    "A": (7, -15),
    "B": (7, -18),
    "C": (10, -3),
    "B'": (7, -18),
    "C'": (10, 0),
}
for name, p in points.items():
    dx, dy = offsets[name]
    ax.annotate(name, (p[0], p[1]),
                textcoords="offset points", xytext=(dx, dy),
                fontsize=13, color="0.12")

# Mise en forme : sans axes, sans titre
ax.set_aspect('equal', adjustable='box')
pts = np.vstack([A, B, C, Bp, Cp, P1_end, P2_end])
ax.set_xlim(pts[:, 0].min() - 1.0, pts[:, 0].max() + 1.2)
ax.set_ylim(pts[:, 1].min() - 1.0, pts[:, 1].max() + 1.2)
ax.axis('off')

plt.show()
