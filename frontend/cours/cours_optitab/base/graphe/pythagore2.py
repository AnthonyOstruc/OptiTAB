import numpy as np
import matplotlib.pyplot as plt
from math import atan2, degrees

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

# --- Triangle générique (NON rectangle) ---
A = np.array([0.0, 0.0])
B = np.array([6.0, 0.0])
C = np.array([2.2, 3.8])  # choisi pour ne PAS avoir 90° en A, B ou C

fig, ax = plt.subplots(figsize=(8.5, 5.5))

# Couleurs (pédago, pas trop)
c_ab   = "tab:blue"
c_ac   = "tab:orange"
c_bc   = "0.20"
c_edge = "0.15"
c_txt  = "0.12"

# Côtés du triangle
ax.plot([A[0], B[0]], [A[1], B[1]], linewidth=3.0, color=c_ab)  # AB
ax.plot([A[0], C[0]], [A[1], C[1]], linewidth=3.0, color=c_ac)  # AC
ax.plot([B[0], C[0]], [B[1], C[1]], linewidth=3.0, color=c_bc)  # BC

# Points (cercles blancs)
for name, p, s in [("A", A, 95), ("B", B, 85), ("C", C, 85)]:
    ax.scatter(p[0], p[1], s=s, facecolors="white",
               edgecolors=c_edge, linewidths=2.2, zorder=3)

# Labels des points
ax.annotate("A", A, textcoords="offset points", xytext=(-18, -18), fontsize=14, color=c_txt)
ax.annotate("B", B, textcoords="offset points", xytext=(10, -18),  fontsize=14, color=c_txt)
ax.annotate("C", C, textcoords="offset points", xytext=(10, 8),    fontsize=14, color=c_txt)

# Labels des segments (sans valeurs)
annotate_along_segment(ax, A, B, "AB", offset=-16, fontsize=13, color=c_txt)
annotate_along_segment(ax, A, C, "AC", offset=16,  fontsize=13, color=c_txt)
annotate_along_segment(ax, B, C, "BC", offset=16,  fontsize=13, color=c_txt)

# Mise en forme (sans axes, sans titre)
ax.set_aspect("equal", adjustable="box")
pts = np.vstack([A, B, C])
ax.set_xlim(pts[:, 0].min() - 1.2, pts[:, 0].max() + 1.2)
ax.set_ylim(pts[:, 1].min() - 1.2, pts[:, 1].max() + 1.2)
ax.axis("off")

plt.show()
plt.close(fig)
