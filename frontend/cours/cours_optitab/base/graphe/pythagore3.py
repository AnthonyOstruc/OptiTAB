import numpy as np
import matplotlib.pyplot as plt
from math import atan2, degrees
from matplotlib.patches import Arc

def annotate_along_segment(ax, P, Q, text, offset=12, fontsize=12, color="0.12", rotation=None):
    """Label au milieu de PQ, décalé + rotation (auto si rotation=None), texte toujours lisible."""
    P = np.array(P, float); Q = np.array(Q, float)
    mid = (P + Q) / 2
    v = Q - P

    ang = degrees(atan2(v[1], v[0])) if rotation is None else rotation
    if ang > 90:  ang -= 180
    if ang < -90: ang += 180

    L = np.linalg.norm(v)
    if L == 0:
        return
    u = v / L
    perp = np.array([-u[1], u[0]])

    ax.annotate(
        text, mid,
        textcoords="offset points",
        xytext=(perp[0] * offset, perp[1] * offset),
        ha="center", va="center",
        fontsize=fontsize, color=color,
        rotation=ang, rotation_mode="anchor"
    )

def angle_arc(ax, A, B, C, r=0.9, color="0.12", lw=2.0):
    """Petit arc pour marquer l'angle en A (entre AB et AC)."""
    A = np.array(A, float); B = np.array(B, float); C = np.array(C, float)
    u = B - A
    v = C - A
    if np.linalg.norm(u) == 0 or np.linalg.norm(v) == 0:
        return

    a1 = degrees(atan2(u[1], u[0]))
    a2 = degrees(atan2(v[1], v[0]))

    # normaliser pour prendre le petit angle
    d = (a2 - a1 + 360) % 360
    if d > 180:
        a1, a2 = a2, a1
        d = 360 - d

    arc = Arc((A[0], A[1]), 2*r, 2*r, angle=0, theta1=a1, theta2=a1+d, lw=lw, color=color)
    ax.add_patch(arc)

# ----------------------------
# Triangle ABC : BC plus long, triangle NON rectangle
# ----------------------------
B = np.array([-3.0, 0.0])
C = np.array([ 3.0, 0.0])

# Choisis A assez "haut" pour que AB et AC soient < BC (BC reste le plus long)
# (triangle acutangle, et non rectangle)
A = np.array([0.0, 3.6])

fig, ax = plt.subplots(figsize=(8.5, 5.5))

# Couleurs pédagogiques
c_sides = "tab:blue"     # AB, AC
c_long  = "tab:orange"   # BC (le plus long)
c_edge  = "0.15"
c_txt   = "0.12"

# Côtés
ax.plot([A[0], B[0]], [A[1], B[1]], linewidth=3.0, color=c_sides)  # AB
ax.plot([A[0], C[0]], [A[1], C[1]], linewidth=3.0, color=c_sides)  # AC
ax.plot([B[0], C[0]], [B[1], C[1]], linewidth=3.4, color=c_long)   # BC (plus long)

# Marque d'angle en A (pour montrer que ce n'est pas un angle droit)
angle_arc(ax, A, B, C, r=0.9, color=c_txt, lw=2.2)

# Points (cercles blancs)
for name, p, s in [("A", A, 95), ("B", B, 85), ("C", C, 85)]:
    ax.scatter(p[0], p[1], s=s, facecolors="white",
               edgecolors=c_edge, linewidths=2.2, zorder=3)

# Labels points
ax.annotate("A", A, textcoords="offset points", xytext=(10, 10),   fontsize=14, color=c_txt)
ax.annotate("B", B, textcoords="offset points", xytext=(-18, -18), fontsize=14, color=c_txt)
ax.annotate("C", C, textcoords="offset points", xytext=(10, -18),  fontsize=14, color=c_txt)

# Labels côtés (sans valeurs)
annotate_along_segment(ax, A, B, "AB", offset=14,  fontsize=13, color=c_txt)
annotate_along_segment(ax, A, C, "AC", offset=14,  fontsize=13, color=c_txt)
annotate_along_segment(ax, B, C, "BC", offset=-16, fontsize=13, color=c_txt, rotation=0)  # BC horizontal

# Mise en forme
ax.set_aspect("equal", adjustable="box")
pts = np.vstack([A, B, C])
ax.set_xlim(pts[:, 0].min() - 1.5, pts[:, 0].max() + 1.5)
ax.set_ylim(pts[:, 1].min() - 1.2, pts[:, 1].max() + 1.5)
ax.axis("off")

plt.show()
plt.close(fig)
