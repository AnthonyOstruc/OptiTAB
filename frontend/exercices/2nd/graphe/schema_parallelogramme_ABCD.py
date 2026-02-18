import numpy as np
import matplotlib.pyplot as plt

# Données
A = np.array([2.0,  1.0])
B = np.array([6.0,  3.0])
C = np.array([4.0, -1.0])

# Parallélogramme ABCD (dans cet ordre) : D = A + C - B
D = A + C - B

# Milieux
I = (A + C) / 2          # milieu de [AC]
J = (B + D) / 2          # milieu de [BD]

fig, ax = plt.subplots(figsize=(7.2, 5.6))

# Repère + grille
ax.axhline(0, linewidth=1)
ax.axvline(0, linewidth=1)
ax.grid(True, linewidth=0.6)

# Parallélogramme
poly = np.vstack([A, B, C, D, A])
ax.plot(poly[:, 0], poly[:, 1], linewidth=2)

# Diagonales
ax.plot([A[0], C[0]], [A[1], C[1]], linestyle="--", linewidth=2)
ax.plot([B[0], D[0]], [B[1], D[1]], linestyle="--", linewidth=2)

# Points
def pt(P, s=70, z=5):
    ax.scatter(P[0], P[1], s=s, zorder=z)

pt(A); pt(B); pt(C); pt(D)
pt(I, s=85, z=7)
pt(J, s=55, z=8)

# Labels
def lab(P, name, dx=8, dy=8):
    ax.annotate(
        name, P,
        xytext=(dx, dy),
        textcoords="offset points",
        fontsize=12,
        weight="bold"
    )

lab(A, "A", dx=-16, dy=10)
lab(B, "B", dx=10, dy=10)
lab(C, "C", dx=10, dy=-16)
lab(D, "D", dx=-16, dy=-16)

# ✅ Texte "I = J" déplacé vers la droite
lab(I, "I = J", dx=20, dy=2)

# Fenêtre d'affichage
all_pts = np.vstack([A, B, C, D, I])
xmin, ymin = all_pts.min(axis=0) - 1.5
xmax, ymax = all_pts.max(axis=0) + 1.5
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("x")
ax.set_ylabel("y")

plt.show()
