import numpy as np
import matplotlib.pyplot as plt

# Configuration de la figure
fig, ax = plt.subplots(figsize=(10, 8))

# Point A
A = np.array([0, 3])
ax.plot(A[0], A[1], 'kx', markersize=12, markeredgewidth=3)
ax.text(A[0], A[1] + 0.2, 'A', fontsize=16, ha='center', va='bottom', fontweight='bold')

# Droite (d) horizontale
x_line = np.linspace(-3, 3, 100)
y_line = np.zeros_like(x_line)
ax.plot(x_line, y_line, 'b-', linewidth=2, label='Droite (d)')

# Point de projection H (au pied de la perpendiculaire)
H = np.array([0, 0])
ax.plot(H[0], H[1], 'ko', markersize=10, markerfacecolor='green', markeredgecolor='black', markeredgewidth=2)
ax.text(H[0] + 0.1, H[1] - 0.15, 'H', fontsize=14, ha='left', va='top', fontweight='bold', color='green')

# Distance (perpendiculaire) - ligne rouge
ax.plot([A[0], H[0]], [A[1], H[1]], 'r-', linewidth=2, label='Distance')

# Angle droit au point H - dans le coin supérieur droit
angle_size = 0.15
# Ligne horizontale pour l'angle droit (vers la droite, au-dessus de la droite bleue)
ax.plot([H[0], H[0] + angle_size], [H[1] + angle_size, H[1] + angle_size], 'k-', linewidth=1.5)
# Ligne verticale pour l'angle droit (vers le haut, le long de la ligne rouge)
ax.plot([H[0] + angle_size, H[0] + angle_size], [H[1], H[1] + angle_size], 'k-', linewidth=1.5)

# Lignes pointillées pour montrer les autres distances
# Ligne vers la gauche
P1 = np.array([-2, 0])
ax.plot([A[0], P1[0]], [A[1], P1[1]], 'k--', linewidth=2, alpha=0.7)

# Ligne vers la droite
P2 = np.array([2, 0])
ax.plot([A[0], P2[0]], [A[1], P2[1]], 'k--', linewidth=2, alpha=0.7)

# Texte explicatif
ax.text(2.5, 1.5, 'Distance du point A\nà la droite (d)', fontsize=14, 
        ha='center', va='center', color='red',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

# Configuration des axes
ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-0.5, 4)
ax.set_aspect('equal')

# Supprimer les axes et graduations
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Titre supprimé

# Légende
ax.legend(loc='upper right', fontsize=12)

# Grille pour plus de clarté
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("distance_point_droite.png", dpi=200, bbox_inches="tight")

print(f"Graphique sauvegardé sous 'distance_point_droite.png'")
