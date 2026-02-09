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

def right_angle_marker(ax, A, B, C, size=0.7, color="0.12", lw=2.2):
    """Petit carré d'angle droit en A (directions AB et AC)."""
    A = np.array(A, float); B = np.array(B, float); C = np.array(C, float)
    u = B - A
    v = C - A
    nu = np.linalg.norm(u); nv = np.linalg.norm(v)
    if nu == 0 or nv == 0:
        return
    u = u / nu
    v = v / nv

    P = A + size * u
    Q = A + size * v
    R = P + size * v

    ax.plot([P[0], R[0]], [P[1], R[1]], color=color, linewidth=lw)
    ax.plot([Q[0], R[0]], [Q[1], R[1]], color=color, linewidth=lw)

# ----------------------------
# Exemple (réciproque) : MN=6, NP=8, MP=10 => triangle rectangle en N
# ----------------------------
MN, NP, MP = 6.0, 8.0, 10.0

N = np.array([0.0, 0.0])
M = np.array([MN, 0.0])   # MN horizontal
P = np.array([0.0, NP])   # NP vertical

fig, ax = plt.subplots(figsize=(8.8, 5.6))

# Couleurs pédagogiques
c_legs = "tab:blue"     # cathètes
c_hyp  = "tab:orange"   # hypothénuse MP
c_edge = "0.15"
c_txt  = "0.12"

# Côtés
ax.plot([M[0], N[0]], [M[1], N[1]], linewidth=3.0, color=c_legs)  # MN
ax.plot([N[0], P[0]], [N[1], P[1]], linewidth=3.0, color=c_legs)  # NP
ax.plot([M[0], P[0]], [M[1], P[1]], linewidth=3.4, color=c_hyp)   # MP

# Marque d'angle droit en N
right_angle_marker(ax, N, M, P, size=0.75, color=c_txt, lw=2.2)

# Points (cercles blancs)
for name, p, s in [("M", M, 90), ("N", N, 95), ("P", P, 90)]:
    ax.scatter(p[0], p[1], s=s, facecolors="white",
               edgecolors=c_edge, linewidths=2.2, zorder=3)

# Labels points
ax.annotate("M", M, textcoords="offset points", xytext=(10, -18),  fontsize=14, color=c_txt)
ax.annotate("N", N, textcoords="offset points", xytext=(-18, -18), fontsize=14, color=c_txt)
ax.annotate("P", P, textcoords="offset points", xytext=(-18, 10),  fontsize=14, color=c_txt)

# Labels côtés (avec valeurs)
annotate_along_segment(ax, M, N, "MN = 6", offset=-18, fontsize=12, color=c_txt, rotation=0)
annotate_along_segment(ax, N, P, "NP = 8", offset=18,  fontsize=12, color=c_txt, rotation=90)
annotate_along_segment(ax, M, P, "MP = 10", offset=18, fontsize=12, color=c_txt)  # rotation auto

# Mise en forme
ax.set_aspect("equal", adjustable="box")
pts = np.vstack([M, N, P])
ax.set_xlim(pts[:, 0].min() - 1.6, pts[:, 0].max() + 1.6)
ax.set_ylim(pts[:, 1].min() - 1.4, pts[:, 1].max() + 1.6)
ax.axis("off")

plt.show()
plt.close(fig)
