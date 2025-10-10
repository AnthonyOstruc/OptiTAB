import matplotlib.pyplot as plt
import numpy as np

# Configuration de la figure
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(-2*np.pi, 2*np.pi)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')

# Fonction sin(x) + cos(x)
x = np.linspace(-2*np.pi, 2*np.pi, 1000)
y = np.sin(x) + np.cos(x)

# Tracer la fonction sin(x) + cos(x)
ax.plot(x, y, 'purple', linewidth=2, label='sin(x) + cos(x)')

# Axes
ax.axhline(y=0, color='black', linewidth=1, alpha=0.7)
ax.axvline(x=0, color='black', linewidth=1, alpha=0.7)

# Extremums seulement
# Pour sin(x) + cos(x) = √2 * sin(x + π/4)
# Maximums: √2 en x = π/4 + 2kπ  
# Minimums: -√2 en x = 5π/4 + 2kπ

# Maximums (calculés exactement) - seulement les vrais maximums
max_x = [np.pi/4]
max_y = [np.sin(np.pi/4) + np.cos(np.pi/4)]

# Minimums (calculés exactement) - seulement les vrais minimums
min_x = [5*np.pi/4]
min_y = [np.sin(5*np.pi/4) + np.cos(5*np.pi/4)]

# Afficher les maximums
for i, (px, py) in enumerate(zip(max_x, max_y)):
    ax.plot(px, py, 'ro', markersize=6)
    if i == 0:
        ax.annotate('(π/4, √2)', (px, py), xytext=(px+0.1, py+0.2), fontsize=10)

# Afficher les minimums
for i, (px, py) in enumerate(zip(min_x, min_y)):
    ax.plot(px, py, 'ro', markersize=6)
    if i == 0:
        ax.annotate('(5π/4, -√2)', (px, py), xytext=(px+0.1, py-0.3), fontsize=10)

# Graduations sur l'axe x
x_ticks = [-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
x_labels = ['-2π', '-3π/2', '-π', '-π/2', '0', 'π/2', 'π', '3π/2', '2π']
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, fontsize=10)

# Graduations sur l'axe y
y_ticks = [-2, -np.sqrt(2), -1, 0, 1, np.sqrt(2), 2]
y_labels = ['-2', '-√2', '-1', '0', '1', '√2', '2']
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
plt.savefig('graphe_sin_plus_cos.png', dpi=300, bbox_inches='tight')
plt.show()
