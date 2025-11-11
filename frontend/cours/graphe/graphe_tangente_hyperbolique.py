import matplotlib.pyplot as plt
import numpy as np

# Configuration de la figure
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(-5, 5)
ax.set_ylim(-1.5, 1.5)

# Fonction tangente hyperbolique
x = np.linspace(-5, 5, 1000)
y = np.tanh(x)

# Tracer la fonction tangente hyperbolique
ax.plot(x, y, 'b-', linewidth=2, label='th(x)')

# Asymptotes horizontales
ax.axhline(y=-1, color='green', linestyle='--', linewidth=1.5, alpha=0.7, label='Asymptote y = -1')
ax.axhline(y=1, color='green', linestyle='--', linewidth=1.5, alpha=0.7, label='Asymptote y = 1')

# Axes
ax.axhline(y=0, color='black', linewidth=1, alpha=0.7)
ax.axvline(x=0, color='black', linewidth=1, alpha=0.7)

# Points clés
points_x = [0]
points_y = [0]

for i, (px, py) in enumerate(zip(points_x, points_y)):
    ax.plot(px, py, 'ro', markersize=6)
    ax.annotate('(0, 0)', (px, py), xytext=(px+0.5, py+0.1), fontsize=10)

# Graduations sur l'axe x
x_ticks = [-4, -2, -1, 0, 1, 2, 4]
x_labels = ['-4', '-2', '-1', '0', '1', '2', '4']
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, fontsize=10)

# Graduations sur l'axe y
y_ticks = [-1, -0.5, 0, 0.5, 1]
y_labels = ['-1', '-0.5', '0', '0.5', '1']
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
plt.savefig('graphe_tangente_hyperbolique.png', dpi=300, bbox_inches='tight')
plt.show()
