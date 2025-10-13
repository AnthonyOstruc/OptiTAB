# Shift both vectors (u and v) downward by more for better spacing, keeping symmetry
import numpy as np
import matplotlib.pyplot as plt

# Define symmetric vectors about x-axis for perfect centered θ
angle = np.deg2rad(30)  # each vector 30° from x-axis (angle plus grand)
length = 1.8
shift_y = -0.4  # déplacement vers le bas
u = np.array([length * np.cos(angle), length * np.sin(angle) + shift_y])
v = np.array([length * np.cos(-angle), length * np.sin(-angle) + shift_y])

# Compute θ (should be 2*angle)
theta = 2 * angle

# Figure setup
fig, ax = plt.subplots(figsize=(7,7))
ax.set_aspect("equal")
ax.set_xlim(-0.5, 3)
ax.set_ylim(-1.5, 1.5)
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

# Axes supprimés

# Vectors u (blue) and v (orange)
ax.arrow(0, 0, u[0], u[1], head_width=0.08, head_length=0.12, linewidth=2.2, color="#1f77b4")
ax.arrow(0, 0, v[0], v[1], head_width=0.08, head_length=0.12, linewidth=2.2, color="#ff7f0e")

# Labels positionnés au milieu des vecteurs
ax.text(u[0]/2 + 0.05, u[1]/2 + 0.05, r"$\vec{u}$", fontsize=14, color="#1f77b4")
ax.text(v[0]/2 + 0.05, v[1]/2 - 0.05, r"$\vec{v}$", fontsize=14, color="#ff7f0e")

# Arc pour montrer l'angle θ entre les vecteurs
from matplotlib.patches import Arc
arc = Arc((0, shift_y), 0.8, 0.8, angle=0, theta1=-np.rad2deg(angle), theta2=np.rad2deg(angle), 
          color='black', linewidth=1.5)
ax.add_patch(arc)

# θ label positionné au milieu de l'arc (plus haut)
theta_mid_radius = 0.5  # rayon plus grand pour positionner θ
theta_x = theta_mid_radius * np.cos(0)  # au milieu (angle = 0)
theta_y = theta_mid_radius * np.sin(0) + shift_y + 0.2  # plus haut
ax.text(theta_x + 0.05, theta_y, r"$\theta$", fontsize=14)


plt.tight_layout()
plt.savefig("produit_scalaire_simple_aigu_v4.png", dpi=200, bbox_inches="tight")
plt.show()

print("Graphique sauvegardé sous 'produit_scalaire_simple_aigu_v4.png'")
