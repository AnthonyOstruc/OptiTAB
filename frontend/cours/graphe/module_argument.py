import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import matplotlib.patches as patches

plt.figure(figsize=(12, 10))
ax = plt.gca()

# Configuration du graphique
plt.xlim(-3, 3)
plt.ylim(-3, 3)
ax.set_aspect('equal')

# Désactiver les axes
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Nombres complexes de l'exercice
z1 = 1 + 1j  # z1 = 1 + i
z2 = np.sqrt(3) + 1j  # z2 = √3 + i
z3 = -2 + 2j  # z3 = -2 + 2i
z4 = -np.sqrt(3) + 1j  # z4 = -√3 + i

# Couleurs
colors = ['#1976d2', '#388e3c', '#d32f2f', '#9c27b0']
labels = ['z₁', 'z₂', 'z₃', 'z₄']

# Tracé des nombres complexes
complexes = [z1, z2, z3, z4]
for i, z in enumerate(complexes):
    x, y = z.real, z.imag
    
    # Point
    ax.plot(x, y, 'o', color=colors[i], markersize=12, markeredgecolor='white', markeredgewidth=2)
    
    # Ligne du centre vers le point
    ax.plot([0, x], [0, y], '-', color=colors[i], linewidth=3, alpha=0.8)
    
    # Flèche pour montrer l'argument
    arrow = FancyArrowPatch((0, 0), (x, y), 
                           arrowstyle='->', mutation_scale=20, 
                           color=colors[i], linewidth=2)
    ax.add_patch(arrow)
    
    # Label du point
    ax.text(x + 0.15, y + 0.15, labels[i], fontsize=16, fontweight='bold', color=colors[i])
    
    # Module (distance)
    module = abs(z)
    mid_x, mid_y = x/2, y/2
    ax.text(mid_x - 0.1, mid_y + 0.1, f'r={module:.2f}', fontsize=10, color=colors[i],
            bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

# Calcul des arguments
arg1 = np.angle(z1)
arg2 = np.angle(z2)
arg3 = np.angle(z3)
arg4 = np.angle(z4)

# Arc pour montrer l'argument de z1
theta1 = np.linspace(0, arg1, 50)
r1 = 0.3
x_arc1 = r1 * np.cos(theta1)
y_arc1 = r1 * np.sin(theta1)
ax.plot(x_arc1, y_arc1, '--', color=colors[0], linewidth=2, alpha=0.7)
ax.text(0.2, 0.1, r'$\theta_1 = \frac{\pi}{4}$', fontsize=12, color=colors[0])

# Arc pour montrer l'argument de z2
theta2 = np.linspace(0, arg2, 50)
r2 = 0.4
x_arc2 = r2 * np.cos(theta2)
y_arc2 = r2 * np.sin(theta2)
ax.plot(x_arc2, y_arc2, '--', color=colors[1], linewidth=2, alpha=0.7)
ax.text(0.3, 0.15, r'$\theta_2 = \frac{\pi}{6}$', fontsize=12, color=colors[1])

# Arc pour montrer l'argument de z3
theta3 = np.linspace(0, arg3, 50)
r3 = 0.5
x_arc3 = r3 * np.cos(theta3)
y_arc3 = r3 * np.sin(theta3)
ax.plot(x_arc3, y_arc3, '--', color=colors[2], linewidth=2, alpha=0.7)
ax.text(-0.4, 0.2, r'$\theta_3 = \frac{3\pi}{4}$', fontsize=12, color=colors[2])

# Arc pour montrer l'argument de z4
theta4 = np.linspace(0, arg4, 50)
r4 = 0.6
x_arc4 = r4 * np.cos(theta4)
y_arc4 = r4 * np.sin(theta4)
ax.plot(x_arc4, y_arc4, '--', color=colors[3], linewidth=2, alpha=0.7)
ax.text(-0.5, 0.3, r'$\theta_4 = \frac{5\pi}{6}$', fontsize=12, color=colors[3])

# Axes
ax.axhline(y=0, color='k', linewidth=1, alpha=0.5)
ax.axvline(x=0, color='k', linewidth=1, alpha=0.5)

# Labels des axes
ax.text(2.7, 0.1, 'Axe réel', fontsize=12, color='black')
ax.text(0.1, 2.7, 'Axe imaginaire', fontsize=12, color='black')

# Point origine
ax.plot(0, 0, 'ko', markersize=6)

# Titre
plt.title('Module et Argument des Nombres Complexes', fontsize=16, fontweight='bold', pad=20)

# Légende avec les valeurs exactes
legend_text = f"""Valeurs exactes:
z₁ = 1 + i → |z₁| = √2, arg(z₁) = π/4
z₂ = √3 + i → |z₂| = 2, arg(z₂) = π/6  
z₃ = -2 + 2i → |z₃| = 2√2, arg(z₃) = 3π/4
z₄ = -√3 + i → |z₄| = 2, arg(z₄) = 5π/6"""

ax.text(-2.8, -2.5, legend_text, fontsize=11, 
        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8))

# Formule générale
ax.text(-2.8, 2.2, 'Forme trigonométrique:', fontsize=12, fontweight='bold')
ax.text(-2.8, 2.0, r'$z = |z|(\cos\theta + i\sin\theta)$', fontsize=12,
        bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))

# Grille
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('module_argument.png', dpi=300, bbox_inches='tight')
plt.show()


