import numpy as np
import matplotlib.pyplot as plt
from math import atan2, degrees

def annotate_along_segment(ax, P, Q, text, offset=12, fontsize=12, color="0.12", rotation=None):
    """
    Place un label près du milieu du segment PQ, avec décalage perpendiculaire.
    - rotation=None : rotation automatique selon la pente du segment (et texte toujours "à l'endroit")
    - rotation=...  : force un angle (en degrés)
    """
    P = np.array(P, float); Q = np.array(Q, float)
    mid = (P + Q) / 2
    v = Q - P

    ang = degrees(atan2(v[1], v[0])) if rotation is None else rotation

    # Garder le texte lisible (jamais à l'envers)
    if ang > 90:
        ang -= 180
    if ang < -90:
        ang += 180

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

def right_angle_marker(ax, A, B, C, size=0.55, color="0.12", lw=2.2):
    """Petit carré d'angle droit en A, en utilisant les directions AB et AC."""
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

# --- Triangle rectangle (vocabulaire + hypothénuse) ---
A = np.array([0.0, 0.0])
B = np.array([6.0, 0.0])   # AB horizontal
C = np.array([0.0, 4.0])   # AC vertical (angle droit en A)

fig, ax = plt.subplots(figsize=(8.5, 5.5))

# Couleurs pédagogiques (AB bleu, AC orange, BC noir/gris)
c_ab   = "tab:blue"
c_ac   = "tab:orange"   # demandé : AC autre que bleu
c_bc   = "0.15"         # hypothénuse (sobre)
c_edge = "0.15"
c_txt  = "0.12"

# Côtés
ax.plot([A[0], B[0]], [A[1], B[1]], linewidth=3.0, color=c_ab)  # AB
ax.plot([A[0], C[0]], [A[1], C[1]], linewidth=3.0, color=c_ac)  # AC
ax.plot([B[0], C[0]], [B[1], C[1]], linewidth=3.2, color=c_bc)  # BC (hypoténuse)

# Marque d'angle droit
right_angle_marker(ax, A, B, C, size=0.55, color=c_txt, lw=2.2)

# Points (cercles blancs)
for name, p, s in [("A", A, 95), ("B", B, 85), ("C", C, 85)]:
    ax.scatter(p[0], p[1], s=s, facecolors="white",
               edgecolors=c_edge, linewidths=2.2, zorder=3)

# Labels des points
ax.annotate("A", A, textcoords="offset points", xytext=(-18, -18), fontsize=14, color=c_txt)
ax.annotate("B", B, textcoords="offset points", xytext=(10, -18),  fontsize=14, color=c_txt)
ax.annotate("C", C, textcoords="offset points", xytext=(-18, 10),  fontsize=14, color=c_txt)

# Labels des segments (sans valeurs)
annotate_along_segment(ax, A, B, "AB", offset=-16, fontsize=13, color=c_txt)
annotate_along_segment(ax, A, C, "AC", offset=16,  fontsize=13, color=c_txt)

# ✅ BC : rotation forcée (choisis 0 si tu veux horizontal, sinon laisse rotation=None)
annotate_along_segment(ax, B, C, "BC", offset=16, fontsize=13, color=c_txt, rotation=None)

# Texte "hypoténuse" (optionnel utile pour vocabulaire)
ax.annotate("hypoténuse", ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2),
            textcoords="offset points", xytext=(18, 18),
            fontsize=12, color=c_txt)

# Mise en forme
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-1.2, 7.2)
ax.set_ylim(-1.2, 5.4)
ax.axis("off")

plt.show()
plt.close(fig)
