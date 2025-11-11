import matplotlib.pyplot as plt
import numpy as np

# Configuration de la figure
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-0.5, np.pi + 0.5)
ax.set_aspect('equal')

# Fonction arccosinus
x = np.linspace(-1, 1, 1000)
y = np.arccos(x)

# Tracer la fonction arccosinus
ax.plot(x, y, 'b-', linewidth=2, label='arccos(x)')

# Axes
ax.axhline(y=0, color='black', linewidth=1, alpha=0.7)
ax.axvline(x=0, color='black', linewidth=1, alpha=0.7)

# Points clés
points_x = [-1, 0, 1]
points_y = [np.pi, np.pi/2, 0]

for i, (px, py) in enumerate(zip(points_x, points_y)):
    ax.plot(px, py, 'ro', markersize=6)
    if i == 0:
        ax.annotate('(-1, π)', (px, py), xytext=(px-0.3, py+0.1), fontsize=10)
    elif i == 1:
        ax.annotate('(0, π/2)', (px, py), xytext=(px-0.5, py+0.1), fontsize=10)
    elif i == 2:
        ax.annotate('(1, 0)', (px, py), xytext=(px+0.1, py+0.2), fontsize=10)

# Graduations sur l'axe x
x_ticks = [-1, -0.5, 0, 0.5, 1]
x_labels = ['-1', '-0.5', '0', '0.5', '1']
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, fontsize=10)

# Graduations sur l'axe y
y_ticks = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
y_labels = ['0', 'π/4', 'π/2', '3π/4', 'π']
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels, fontsize=10)

# Labels des axes
ax.set_xlabel('x', fontsize=12, fontweight='bold')
ax.set_ylabel('y', fontsize=12, fontweight='bold')

# Légende
ax.legend(loc='upper right')

# Supprimer le titre principal noir
plt.suptitle('', fontsize=0)

# Ajuster la mise en page
plt.tight_layout()

# Sauvegarder
plt.savefig('graphe_arccosinus.png', dpi=300, bbox_inches='tight')
plt.show()
