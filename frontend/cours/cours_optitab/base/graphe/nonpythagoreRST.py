import numpy as np
import matplotlib.pyplot as plt
from math import atan2, degrees, sqrt
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

def angle_arc(ax, V, P1, P2, r=0.9, color="0.12", lw=2.0):
    """Petit arc pour marquer l'angle en V entre (V->P1) et (V->P2)."""
    V = np.array(V, float); P1 = np.array(P1, float); P2 = np.array(P2, float)
    u = P1 - V
    v = P2 - V
    if np.linalg.norm(u) == 0 or np.linalg.norm(v) == 0:
        return

    a1 = degrees(atan2(u[1], u[0]))
    a2 = degrees(atan2(v[1], v[0]))

    # choisir le petit angle
    d = (a2 - a1 + 360) % 360
    if d > 180:
        a1, a2 = a2, a1
        d = 360 - d

    ax.add_patch(Arc((V[0], V[1]), 2*r, 2*r, angle=0,
                     theta1=a1, theta2=a1+d, lw=lw, color=color))

# ----------------------------
# Exemple : triangle RST avec RS=5, ST=7, RT=9
# ----------------------------
RS, ST, RT = 5.0, 7.0, 9.0

R = np.array([0.0, 0.0])
T = np.array([RT, 0.0])

# S = intersection des cercles (centre R, rayon RS) et (centre T, rayon ST)
d = RT
x = (d*d + RS*RS - ST*ST) / (2*d)
y = sqrt(max(0.0, RS*RS - x*x))
S = np.array([x, y])

fig, ax = plt.subplots(figsize=(8.8, 5.6))

# Couleurs pédagogiques
c_main = "tab:blue"
c_long = "tab:orange"
c_edge = "0.15"
c_txt  = "0.12"

# Côtés
ax.plot([R[0], S[0]], [R[1], S[1]], linewidth=3.0, color=c_main)  # RS
ax.plot([S[0], T[0]], [S[1], T[1]], linewidth=3.0, color=c_main)  # ST
ax.plot([R[0], T[0]], [R[1], T[1]], linewidth=3.4, color=c_long)  # RT (plus long)

# Arc en S (angle opposé au plus grand côté RT)
angle_arc(ax, S, R, T, r=0.9, color=c_txt, lw=2.2)

# Points
for name, p, s in [("R", R, 90), ("S", S, 90), ("T", T, 90)]:
    ax.scatter(p[0], p[1], s=s, facecolors="white",
               edgecolors=c_edge, linewidths=2.2, zorder=3)

# Labels points
ax.annotate("R", R, textcoords="offset points", xytext=(-18, -18), fontsize=14, color=c_txt)
ax.annotate("T", T, textcoords="offset points", xytext=(10, -18),  fontsize=14, color=c_txt)
ax.annotate("S", S, textcoords="offset points", xytext=(10, 10),    fontsize=14, color=c_txt)

# Labels côtés
annotate_along_segment(ax, R, S, "RS = 5", offset=16,  fontsize=12, color=c_txt)
annotate_along_segment(ax, S, T, "ST = 7", offset=16,  fontsize=12, color=c_txt)
annotate_along_segment(ax, R, T, "RT = 9", offset=-18, fontsize=12, color=c_txt, rotation=0)

# Mise en forme
ax.set_aspect("equal", adjustable="box")
pts = np.vstack([R, S, T])
ax.set_xlim(pts[:, 0].min() - 1.4, pts[:, 0].max() + 1.4)
ax.set_ylim(pts[:, 1].min() - 1.2, pts[:, 1].max() + 1.6)
ax.axis("off")

plt.show()
plt.close(fig)
