import numpy as np
import matplotlib.pyplot as plt

# Configuration de la figure
plt.figure(figsize=(10, 10))
ax = plt.gca()

# Paramètres du cercle unité
theta = np.pi/4  # Angle θ = 45° (premier quadrant)
radius = 1

# Coordonnées du point M sur le cercle
M_x = radius * np.cos(theta)
M_y = radius * np.sin(theta)

# Coordonnées des projections
B_x = M_x  # Projection sur l'axe des cosinus
B_y = 0
C_x = 0    # Projection sur l'axe des sinus
C_y = M_y

# Tracer le cercle unité
circle = plt.Circle((0, 0), radius, fill=False, color='blue', linewidth=2)
ax.add_patch(circle)

# Tracer les axes
ax.axhline(y=0, color='black', linewidth=1.5)
ax.axvline(x=0, color='black', linewidth=1.5)

# Tracer le rayon OM (vecteur rouge)
ax.plot([0, M_x], [0, M_y], 'r-', linewidth=2)

# Tracer les projections (lignes pointillées)
ax.plot([M_x, B_x], [M_y, B_y], 'k--', linewidth=1.5, alpha=0.7)
ax.plot([M_x, C_x], [M_y, C_y], 'k--', linewidth=1.5, alpha=0.7)

# Marquer les points
ax.plot(M_x, M_y, 'ro', markersize=8, label='M')
ax.plot(B_x, B_y, 'ko', markersize=6, label='B')
ax.plot(C_x, C_y, 'ko', markersize=6, label='C')
ax.plot(0, 0, 'ko', markersize=6, label='O')

# Tracer l'arc d'angle θ
arc_theta = np.linspace(0, theta, 100)
arc_x = 0.3 * np.cos(arc_theta)
arc_y = 0.3 * np.sin(arc_theta)
ax.plot(arc_x, arc_y, 'purple', linewidth=2)

# Ajouter le label θ
theta_label_x = 0.4 * np.cos(theta/2)
theta_label_y = 0.4 * np.sin(theta/2)
ax.text(theta_label_x, theta_label_y, r'$\theta$', fontsize=14, color='purple', 
        ha='center', va='center', fontweight='bold')

# Configuration des axes
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_aspect('equal')

# Supprimer les ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer les spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Ajouter les flèches aux axes
ax.annotate("", xy=(1.3, 0), xytext=(-1.3, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))
ax.annotate("", xy=(0, 1.3), xytext=(0, -1.3),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))

# Labels des axes
ax.text(1.15, -0.1, 'cos', fontsize=14, ha='center', va='center')
ax.text(-0.1, 1.15, 'sin', fontsize=14, ha='center', va='center')

# Marquer l'origine
ax.text(-0.1, -0.1, '0', fontsize=12, ha='center', va='center')

# Marquer le point 1 sur l'axe des cosinus
ax.plot([1, 1], [-0.05, 0.05], 'k-', linewidth=1.5)
ax.text(1.05, -0.12, '1', fontsize=12, ha='center', va='top')

# Marquer le point 1 sur l'axe des sinus
ax.plot([-0.05, 0.05], [1, 1], 'k-', linewidth=1.5)
ax.text(-0.12, 1.05, '1', fontsize=12, ha='right', va='center')

# Labels des points
ax.text(M_x + 0.1, M_y + 0.1, 'M', fontsize=12, ha='left', va='bottom', color='red', fontweight='bold')
ax.text(B_x + 0.1, B_y - 0.1, 'B', fontsize=12, ha='left', va='top', fontweight='bold')
ax.text(C_x - 0.1, C_y + 0.1, 'C', fontsize=12, ha='right', va='bottom', fontweight='bold')

# Pas de titre

# Légende avec les définitions
plt.legend(['Cercle unité', 'Rayon OM', 'Projection cos', 'Projection sin', 
           r'$\cos \theta = \overline{OB}$', r'$\sin \theta = \overline{OC}$'], 
          fontsize=12, loc='upper right', frameon=True, fancybox=True, shadow=True)

# Ajuster l'espacement
plt.tight_layout()

# Afficher le graphique
plt.show()
