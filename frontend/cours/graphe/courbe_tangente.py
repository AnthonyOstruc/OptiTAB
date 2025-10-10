import matplotlib.pyplot as plt
import numpy as np

# Configuration de la figure
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(-2*np.pi, 2*np.pi)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')

# Fonction tangente
x = np.linspace(-2*np.pi, 2*np.pi, 1000)
# Éviter les asymptotes verticales
x1 = np.linspace(-2*np.pi, -3*np.pi/2-0.1, 200)
x2 = np.linspace(-3*np.pi/2+0.1, -np.pi/2-0.1, 200)
x3 = np.linspace(-np.pi/2+0.1, np.pi/2-0.1, 200)
x4 = np.linspace(np.pi/2+0.1, 3*np.pi/2-0.1, 200)
x5 = np.linspace(3*np.pi/2+0.1, 2*np.pi, 200)

y1 = np.tan(x1)
y2 = np.tan(x2)
y3 = np.tan(x3)
y4 = np.tan(x4)
y5 = np.tan(x5)

# Tracer la fonction tangente par segments
ax.plot(x1, y1, 'g-', linewidth=2, label='tan(x)')
ax.plot(x2, y2, 'g-', linewidth=2)
ax.plot(x3, y3, 'g-', linewidth=2)
ax.plot(x4, y4, 'g-', linewidth=2)
ax.plot(x5, y5, 'g-', linewidth=2)

# Axes
ax.axhline(y=0, color='black', linewidth=1, alpha=0.7)
ax.axvline(x=0, color='black', linewidth=1, alpha=0.7)

# Asymptotes verticales
ax.axvline(x=-3*np.pi/2, color='red', linestyle='--', alpha=0.7, linewidth=1)
ax.axvline(x=-np.pi/2, color='red', linestyle='--', alpha=0.7, linewidth=1)
ax.axvline(x=np.pi/2, color='red', linestyle='--', alpha=0.7, linewidth=1)
ax.axvline(x=3*np.pi/2, color='red', linestyle='--', alpha=0.7, linewidth=1)

# Points clés
points_x = [-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
points_y = [0, np.nan, 0, np.nan, 0, np.nan, 0, np.nan, 0]  # np.nan pour les asymptotes

for i, (px, py) in enumerate(zip(points_x, points_y)):
    if not np.isnan(py):  # Seulement pour les points définis
        ax.plot(px, py, 'ro', markersize=6)
        if i == 0:
            ax.annotate('(-2π, 0)', (px, py), xytext=(px+0.2, py-0.3), fontsize=10)
        elif i == 2:
            ax.annotate('(-π, 0)', (px, py), xytext=(px-0.3, py-0.3), fontsize=10)
        elif i == 4:
            ax.annotate('(0, 0)', (px, py), xytext=(px+0.1, py-0.3), fontsize=10)
        elif i == 6:
            ax.annotate('(π, 0)', (px, py), xytext=(px+0.4, py-0.3), fontsize=10)
        elif i == 8:
            ax.annotate('(2π, 0)', (px, py), xytext=(px-0.9, py-0.3), fontsize=10)

# Graduations sur l'axe x
x_ticks = [-2*np.pi, -3*np.pi/2, -np.pi, -np.pi/2, 0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
x_labels = ['-2π', '-3π/2', '-π', '-π/2', '0', 'π/2', 'π', '3π/2', '2π']
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, fontsize=10)

# Graduations sur l'axe y
y_ticks = [-2, -1, 0, 1, 2]
y_labels = ['-2', '-1', '0', '1', '2']
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
plt.savefig('courbe_tangente.png', dpi=300, bbox_inches='tight')
plt.show()
