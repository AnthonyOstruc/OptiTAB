import matplotlib.pyplot as plt
import numpy as np

# Configuration de la figure
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(-2*np.pi, 2*np.pi)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')

# Fonction sinus
x = np.linspace(-2*np.pi, 2*np.pi, 1000)
y = np.sin(x)

# Tracer la fonction sinus
ax.plot(x, y, 'b-', linewidth=2, label='sin(x)')

# Axes
ax.axhline(y=0, color='black', linewidth=1, alpha=0.7)
ax.axvline(x=0, color='black', linewidth=1, alpha=0.7)

# Points clés
points_x = [-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
points_y = [0, 1, 0, -1, 0, 1, 0, -1, 0]

for i, (px, py) in enumerate(zip(points_x, points_y)):
    ax.plot(px, py, 'ro', markersize=6)
    if i == 0:
        ax.annotate('(-2π, 0)', (px, py), xytext=(px+0.2, py-0.3), fontsize=10)
    elif i == 1:
        ax.annotate('(-3π/2, 1)', (px, py), xytext=(px-0.5, py+0.2), fontsize=10)
    elif i == 2:
        ax.annotate('(-π, 0)', (px, py), xytext=(px-0.3, py-0.3), fontsize=10)
    elif i == 3:
        ax.annotate('(-π/2, -1)', (px, py), xytext=(px-0.5, py-0.3), fontsize=10)
    elif i == 4:
        ax.annotate('(0, 0)', (px, py), xytext=(px+0.1, py-0.3), fontsize=10)
    elif i == 5:
        ax.annotate('(π/2, 1)', (px, py), xytext=(px+0.1, py+0.2), fontsize=10)
    elif i == 6:
        ax.annotate('(π, 0)', (px, py), xytext=(px+0.4, py-0.3), fontsize=10)
    elif i == 7:
        ax.annotate('(3π/2, -1)', (px, py), xytext=(px+0.1, py-0.3), fontsize=10)
    elif i == 8:
        ax.annotate('(2π, 0)', (px, py), xytext=(px-0.9, py-0.3), fontsize=10)

# Graduations sur l'axe x
x_ticks = [-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
x_labels = ['-2π', '-3π/2', '-π', '-π/2', '0', 'π/2', 'π', '3π/2', '2π']
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, fontsize=10)

# Graduations sur l'axe y
y_ticks = [-1, 0, 1]
y_labels = ['-1', '0', '1']
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
plt.savefig('graphe_sinus.png', dpi=300, bbox_inches='tight')
plt.show()
