import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

plt.figure(figsize=(12, 10))
ax = plt.gca()

# Configuration du graphique
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
ax.set_aspect('equal')

# Désactiver les axes
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Cercle unité
cercle_unite = Circle((0, 0), 1, fill=False, color='black', linewidth=2)
ax.add_patch(cercle_unite)

# Racines cubiques de l'unité (n=3)
n3 = 3
racines_cubiques = []
for k in range(n3):
    angle = 2 * k * np.pi / n3
    z = np.exp(1j * angle)
    racines_cubiques.append(z)
    x, y = z.real, z.imag
    ax.plot(x, y, 'o', color='#1976d2', markersize=12, markeredgecolor='white', markeredgewidth=2)
    ax.text(x + 0.15, y + 0.15, f'$z_{k}$', fontsize=14, fontweight='bold', color='#1976d2')
    # Ligne du centre vers la racine
    ax.plot([0, x], [0, y], '--', color='#1976d2', alpha=0.6, linewidth=1)

# Racines 4-ièmes de l'unité (n=4)
n4 = 4
racines_quatriemes = []
for k in range(n4):
    angle = 2 * k * np.pi / n4
    z = np.exp(1j * angle)
    racines_quatriemes.append(z)
    x, y = z.real, z.imag
    ax.plot(x, y, 's', color='#388e3c', markersize=10, markeredgecolor='white', markeredgewidth=2)
    ax.text(x + 0.15, y + 0.15, f'$w_{k}$', fontsize=14, fontweight='bold', color='#388e3c')
    # Ligne du centre vers la racine
    ax.plot([0, x], [0, y], '--', color='#388e3c', alpha=0.6, linewidth=1)

# Racines 6-ièmes de l'unité (n=6) - pour montrer la généralisation
n6 = 6
racines_sixiemes = []
for k in range(n6):
    angle = 2 * k * np.pi / n6
    z = np.exp(1j * angle)
    racines_sixiemes.append(z)
    x, y = z.real, z.imag
    ax.plot(x, y, '^', color='#ff9800', markersize=8, markeredgecolor='white', markeredgewidth=1)
    # Ligne du centre vers la racine
    ax.plot([0, x], [0, y], ':', color='#ff9800', alpha=0.4, linewidth=1)

# Point origine
ax.plot(0, 0, 'ko', markersize=6)

# Titre
plt.title('Racines n-ièmes de l\'Unité dans le Plan Complexe', fontsize=16, fontweight='bold', pad=20)

# Légende
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#1976d2', markersize=12, label='Racines cubiques (n=3)'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#388e3c', markersize=10, label='Racines 4-ièmes (n=4)'),
    plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='#ff9800', markersize=8, label='Racines 6-ièmes (n=6)'),
    plt.Line2D([0], [0], color='black', linewidth=2, label='Cercle unité')
]

ax.legend(handles=legend_elements, loc='upper right', fontsize=12)

# Annotations des valeurs exactes
ax.text(1.2, 0.8, 'Racines cubiques:', fontsize=12, fontweight='bold', color='#1976d2')
ax.text(1.2, 0.6, r'$z_0 = 1$', fontsize=10, color='#1976d2')
ax.text(1.2, 0.4, r'$z_1 = -\frac{1}{2} + i\frac{\sqrt{3}}{2}$', fontsize=10, color='#1976d2')
ax.text(1.2, 0.2, r'$z_2 = -\frac{1}{2} - i\frac{\sqrt{3}}{2}$', fontsize=10, color='#1976d2')

ax.text(1.2, -0.2, 'Racines 4-ièmes:', fontsize=12, fontweight='bold', color='#388e3c')
ax.text(1.2, -0.4, r'$w_0 = 1$', fontsize=10, color='#388e3c')
ax.text(1.2, -0.6, r'$w_1 = i$', fontsize=10, color='#388e3c')
ax.text(1.2, -0.8, r'$w_2 = -1$', fontsize=10, color='#388e3c')
ax.text(1.2, -1.0, r'$w_3 = -i$', fontsize=10, color='#388e3c')

# Propriété importante
ax.text(-1.4, 1.2, 'Propriété importante:', fontsize=12, fontweight='bold', color='red')
ax.text(-1.4, 1.0, r'$\sum_{k=0}^{n-1} e^{i\frac{2k\pi}{n}} = 0$', fontsize=12, color='red',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))

# Grille
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('racines_unite.png', dpi=300, bbox_inches='tight')
plt.show()