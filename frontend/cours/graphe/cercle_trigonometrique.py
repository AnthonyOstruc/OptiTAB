import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Arc
import matplotlib.patches as patches

# Configuration de la figure
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')

# Cercle trigonométrique (rayon 1)
cercle = Circle((0, 0), 1, fill=False, color='black', linewidth=2)
ax.add_patch(cercle)

# Annotation pour spécifier que c'est un cercle unitaire
ax.text(0, -1.3, 'Cercle unitaire (rayon = 1)', fontsize=12, ha='center', 
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))

# Axes
ax.axhline(y=0, color='black', linewidth=1, alpha=0.7)
ax.axvline(x=0, color='black', linewidth=1, alpha=0.7)

# Angle θ (en radians)
theta = np.pi/4  # 45 degrés
x_point = np.cos(theta)
y_point = np.sin(theta)

# Point M sur le cercle
ax.plot(x_point, y_point, 'ro', markersize=8, label=f'Point M(cos(θ), sin(θ))')

# Rayon OM
ax.plot([0, x_point], [0, y_point], 'r-', linewidth=2, alpha=0.7)

# Arc pour l'angle θ
arc = Arc((0, 0), 0.3, 0.3, angle=0, theta1=0, theta2=np.degrees(theta), 
          color='blue', linewidth=2)
ax.add_patch(arc)

# Projections sur les axes
# Projection sur l'axe des abscisses (cos)
ax.plot([x_point, x_point], [0, y_point], 'g--', linewidth=1, alpha=0.7)
ax.plot([0, x_point], [0, 0], 'g-', linewidth=2, label='cos(θ)')

# Projection sur l'axe des ordonnées (sin)
ax.plot([0, x_point], [y_point, y_point], 'b--', linewidth=1, alpha=0.7)
ax.plot([0, 0], [0, y_point], 'b-', linewidth=2, label='sin(θ)')


# Marques sur les axes
ax.plot(1, 0, 'ko', markersize=4)
ax.plot(0, 1, 'ko', markersize=4)
ax.plot(-1, 0, 'ko', markersize=4)
ax.plot(0, -1, 'ko', markersize=4)

# Annotations
ax.annotate('O', (0, 0), xytext=(-0.1, -0.1), fontsize=12, fontweight='bold')
ax.annotate('M', (x_point, y_point), xytext=(x_point+0.1, y_point+0.1), 
           fontsize=12, fontweight='bold', color='red')
ax.annotate('θ', (0.25, 0.1), fontsize=14, fontweight='bold', color='blue')

# Labels des axes
ax.text(1.3, 0, 'x', fontsize=12, fontweight='bold')
ax.text(0, 1.3, 'y', fontsize=12, fontweight='bold')

# Valeurs trigonométriques
cos_val = np.cos(theta)
sin_val = np.sin(theta)


# Quadrants
ax.text(0.6, 0.5, 'I', fontsize=16, fontweight='bold', alpha=0.5, ha='center', va='center')
ax.text(-0.5, 0.5, 'II', fontsize=16, fontweight='bold', alpha=0.5, ha='center', va='center')
ax.text(-0.5, -0.5, 'III', fontsize=16, fontweight='bold', alpha=0.5, ha='center', va='center')
ax.text(0.5, -0.5, 'IV', fontsize=16, fontweight='bold', alpha=0.5, ha='center', va='center')

# Configuration de l'affichage
ax.grid(True, alpha=0.3)
ax.set_xlabel('Axe des abscisses', fontsize=12)
ax.set_ylabel('Axe des ordonnées', fontsize=12)

# Légende
ax.legend(loc='upper right', bbox_to_anchor=(0.95, 0.95))

# Supprimer les graduations des axes
ax.set_xticks([])
ax.set_yticks([])

# Supprimer le titre principal noir
plt.suptitle('', fontsize=0)

# Ajuster la mise en page
plt.tight_layout()

# Sauvegarder
plt.savefig('cercle_trigonometrique.png', dpi=300, bbox_inches='tight')
plt.show()
