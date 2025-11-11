import matplotlib.pyplot as plt
import numpy as np

# Configuration de la figure
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(-2*np.pi, 2*np.pi)
ax.set_ylim(-5, 5)
ax.set_aspect('equal')

# Fonction tangente
x1 = np.linspace(-np.pi/2 + 0.1, np.pi/2 - 0.1, 1000)
x2 = np.linspace(np.pi/2 + 0.1, 3*np.pi/2 - 0.1, 1000)
x3 = np.linspace(-3*np.pi/2 + 0.1, -np.pi/2 - 0.1, 1000)
y1 = np.tan(x1)
y2 = np.tan(x2)
y3 = np.tan(x3)

# Tracer la fonction tangente
ax.plot(x1, y1, 'b-', linewidth=2, label='tan(x)')
ax.plot(x2, y2, 'b-', linewidth=2)
ax.plot(x3, y3, 'b-', linewidth=2)

# Asymptotes verticales
ax.axvline(x=-3*np.pi/2, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
ax.axvline(x=-np.pi/2, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Asymptotes verticales')
ax.axvline(x=np.pi/2, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
ax.axvline(x=3*np.pi/2, color='red', linestyle='--', linewidth=1.5, alpha=0.7)

# Axes
ax.axhline(y=0, color='black', linewidth=1, alpha=0.7)
ax.axvline(x=0, color='black', linewidth=1, alpha=0.7)

# Points clés
points_x = [0]
points_y = [0]

for i, (px, py) in enumerate(zip(points_x, points_y)):
    ax.plot(px, py, 'ro', markersize=6)
    ax.annotate('(0, 0)', (px, py), xytext=(px+0.5, py+0.3), fontsize=10)

# Graduations sur l'axe x
x_ticks = [-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
x_labels = ['-2π', '-3π/2', '-π', '-π/2', '0', 'π/2', 'π', '3π/2', '2π']
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, fontsize=10)

# Graduations sur l'axe y
y_ticks = [-4, -2, -1, 0, 1, 2, 4]
y_labels = ['-4', '-2', '-1', '0', '1', '2', '4']
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
plt.savefig('graphe_tangente.png', dpi=300, bbox_inches='tight')
plt.show()
