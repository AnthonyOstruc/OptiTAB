import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patches as patches

plt.figure(figsize=(12, 10))
ax = plt.gca()

# Configuration du graphique
plt.xlim(-6, 6)
plt.ylim(-2, 8)

# Désactiver les axes
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Points donnés dans l'exercice
z_A = 1 + 2j  # A(1, 2)
z_B = 3 - 1j  # B(3, -1)
z_C = -2 + 3j  # C(-2, 3)
z_I = (z_A + z_B) / 2  # Milieu I de [AB]
z_D = z_A - z_B + z_C  # Point D pour le parallélogramme

# Coordonnées des points
A = (z_A.real, z_A.imag)
B = (z_B.real, z_B.imag)
C = (z_C.real, z_C.imag)
I = (z_I.real, z_I.imag)
D = (z_D.real, z_D.imag)

# Tracé des points
ax.plot(A[0], A[1], 'o', color='#1976d2', markersize=10, markeredgecolor='white', markeredgewidth=2)
ax.plot(B[0], B[1], 'o', color='#388e3c', markersize=10, markeredgecolor='white', markeredgewidth=2)
ax.plot(C[0], C[1], 'o', color='#d32f2f', markersize=10, markeredgecolor='white', markeredgewidth=2)
ax.plot(I[0], I[1], 'o', color='#ff9800', markersize=8, markeredgecolor='white', markeredgewidth=2)
ax.plot(D[0], D[1], 'o', color='#9c27b0', markersize=10, markeredgecolor='white', markeredgewidth=2)

# Labels des points
ax.text(A[0] + 0.2, A[1] + 0.2, 'A', fontsize=16, fontweight='bold', color='#1976d2')
ax.text(B[0] + 0.2, B[1] - 0.3, 'B', fontsize=16, fontweight='bold', color='#388e3c')
ax.text(C[0] - 0.3, C[1] + 0.2, 'C', fontsize=16, fontweight='bold', color='#d32f2f')
ax.text(I[0] + 0.2, I[1] + 0.2, 'I', fontsize=14, fontweight='bold', color='#ff9800')
ax.text(D[0] - 0.3, D[1] + 0.2, 'D', fontsize=16, fontweight='bold', color='#9c27b0')

# Affixes des points
ax.text(A[0] + 0.2, A[1] - 0.4, r'$z_A = 1 + 2i$', fontsize=12, color='#1976d2', 
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
ax.text(B[0] + 0.2, B[1] - 0.6, r'$z_B = 3 - i$', fontsize=12, color='#388e3c',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
ax.text(C[0] - 1.2, C[1] + 0.2, r'$z_C = -2 + 3i$', fontsize=12, color='#d32f2f',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
ax.text(D[0] - 1.2, D[1] - 0.4, r'$z_D = -4 + 6i$', fontsize=12, color='#9c27b0',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

# Question 1: Milieu I
ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', linewidth=2, alpha=0.7)
ax.plot([A[0], I[0]], [A[1], I[1]], 'k--', linewidth=1, alpha=0.5)
ax.plot([I[0], B[0]], [I[1], B[1]], 'k--', linewidth=1, alpha=0.5)

# Question 2: Distance AB
distance_AB = abs(z_B - z_A)
ax.text(2, 0.5, f'AB = {distance_AB:.2f}', fontsize=12, 
        bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.8))

# Question 3: Cercle |z - z_A| = 3
cercle = Circle(A, 3, fill=False, color='#1976d2', linewidth=3, linestyle='--')
ax.add_patch(cercle)
ax.text(A[0] + 3.5, A[1] + 0.5, r'$|z - z_A| = 3$', fontsize=12, color='#1976d2',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

# Question 4: Médiatrice |z - z_A| = |z - z_B|
# Calcul de la médiatrice
mid_x = (A[0] + B[0]) / 2
mid_y = (A[1] + B[1]) / 2
# Vecteur directeur de AB
dir_x = B[0] - A[0]
dir_y = B[1] - A[1]
# Vecteur perpendiculaire
perp_x = -dir_y
perp_y = dir_x
# Normalisation
norm = np.sqrt(perp_x**2 + perp_y**2)
perp_x /= norm
perp_y /= norm

# Tracé de la médiatrice
x_med = np.linspace(-6, 6, 100)
y_med = mid_y + perp_y * (x_med - mid_x) / perp_x
ax.plot(x_med, y_med, '--', color='#ff5722', linewidth=2, alpha=0.8)
ax.text(0, 4, r'$|z - z_A| = |z - z_B|$', fontsize=12, color='#ff5722',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

# Question 5: Parallélogramme ABCD
# Côtés du parallélogramme
ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', linewidth=2, alpha=0.7)
ax.plot([B[0], C[0]], [B[1], C[1]], 'k-', linewidth=2, alpha=0.7)
ax.plot([C[0], D[0]], [C[1], D[1]], 'k-', linewidth=2, alpha=0.7)
ax.plot([D[0], A[0]], [D[1], A[1]], 'k-', linewidth=2, alpha=0.7)

# Diagonales du parallélogramme
ax.plot([A[0], C[0]], [A[1], C[1]], 'k:', linewidth=1, alpha=0.5)
ax.plot([B[0], D[0]], [B[1], D[1]], 'k:', linewidth=1, alpha=0.5)

# Titre et légende
plt.title('Nombres Complexes - Transformations Géométriques', fontsize=16, fontweight='bold', pad=20)

# Légende
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#1976d2', markersize=10, label='Point A'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#388e3c', markersize=10, label='Point B'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#d32f2f', markersize=10, label='Point C'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#ff9800', markersize=8, label='Milieu I'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#9c27b0', markersize=10, label='Point D'),
    plt.Line2D([0], [0], color='#1976d2', linestyle='--', linewidth=3, label='Cercle |z-z_A|=3'),
    plt.Line2D([0], [0], color='#ff5722', linestyle='--', linewidth=2, label='Médiatrice |z-z_A|=|z-z_B|'),
    plt.Line2D([0], [0], color='k', linewidth=2, label='Parallélogramme ABCD')
]

ax.legend(handles=legend_elements, loc='upper right', fontsize=10)

# Grille
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('transformations_geometriques_complexes.png', dpi=300, bbox_inches='tight')
plt.show()
