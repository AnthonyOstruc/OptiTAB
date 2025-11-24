import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# Configuration
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(-0.5, 6)
ax.set_ylim(-0.5, 5)
ax.set_aspect('equal')
ax.axis('off')

# Origine
O = np.array([0, 0])

# Vecteurs
u1 = np.array([2, 1])
u2 = np.array([1, 2])
a1 = 1.5
a2 = 1.0

# Calculs
a1_u1 = a1 * u1
a2_u2 = a2 * u2
v = a1_u1 + a2_u2

# Points
B = O + a1_u1
D = O + v

# Créer les flèches avec labels pour la légende
arrow_u1 = FancyArrowPatch(O, O + u1, arrowstyle='->', mutation_scale=15,
                           linewidth=1, color='#3498db', linestyle='--', alpha=0.6,
                           label='$\\vec{u_1}$ (vecteur de base)')
arrow_u2 = FancyArrowPatch(O, O + u2, arrowstyle='->', mutation_scale=15,
                           linewidth=1, color='#9c27b0', linestyle='--', alpha=0.6,
                           label='$\\vec{u_2}$ (vecteur de base)')
arrow_a1u1 = FancyArrowPatch(O, B, arrowstyle='->', mutation_scale=18,
                            linewidth=1.5, color='#2ecc71',
                            label=f'${a1}\\vec{{u_1}}$')
arrow_a2u2 = FancyArrowPatch(B, D, arrowstyle='->', mutation_scale=18,
                            linewidth=1.5, color='#e74c3c',
                            label=f'${a2}\\vec{{u_2}}$')
arrow_v = FancyArrowPatch(O, D, arrowstyle='->', mutation_scale=20,
                         linewidth=2, color='#f39c12',
                         label=f'$\\vec{{v}} = {a1}\\vec{{u_1}} + {a2}\\vec{{u_2}}$')

# Ajouter au graphique
ax.add_patch(arrow_u1)
ax.add_patch(arrow_u2)
ax.add_patch(arrow_a1u1)
ax.add_patch(arrow_a2u2)
ax.add_patch(arrow_v)

# Légende
ax.legend(loc='upper left', fontsize=11, framealpha=0.95, edgecolor='gray')

plt.tight_layout()
plt.savefig('combinaison_lineaire.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Graphique sauvegardé sous 'combinaison_lineaire.png'")
plt.show()
