import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(20, 12))

# ========== PREMIER GRAPHE : VECTEURS COPLANAIRES ==========
ax1 = fig.add_subplot(121, projection='3d')

# Désactiver les axes
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_zticks([])
ax1._axis3don = False

# Configuration
ax1.set_xlim([-2, 5])
ax1.set_ylim([-2, 5])
ax1.set_zlim([-2, 5])

# Trois vecteurs coplanaires
u1 = np.array([3, 0, 0])    # Vecteur bleu horizontal
v1 = np.array([0, 3, 0])    # Vecteur vert vertical  
w1 = np.array([2, 2, 0])    # Vecteur rouge diagonal (dans le même plan)

# Tracer le plan
xx, yy = np.meshgrid(np.linspace(-1.5, 4.5, 20), np.linspace(-1.5, 4.5, 20))
zz = np.zeros_like(xx)
ax1.plot_surface(xx, yy, zz, alpha=0.3, color='lightblue')

# Tracer les vecteurs
ax1.quiver(0, 0, 0, u1[0], u1[1], u1[2],
           color='#1976d2', arrow_length_ratio=0.1, linewidth=2)
ax1.text(u1[0]/2 + 0.2, u1[1]/2, u1[2]/2 + 0.2, r'$\vec{u}$',
         fontsize=16, color='#1976d2', fontweight='bold')

ax1.quiver(0, 0, 0, v1[0], v1[1], v1[2],
           color='#388e3c', arrow_length_ratio=0.1, linewidth=2)
ax1.text(v1[0]/2, v1[1]/2 + 0.2, v1[2]/2 + 0.2, r'$\vec{v}$',
         fontsize=16, color='#388e3c', fontweight='bold')

ax1.quiver(0, 0, 0, w1[0], w1[1], w1[2],
           color='#d32f2f', arrow_length_ratio=0.1, linewidth=2)
ax1.text(w1[0]/2 - 0.3, w1[1]/2 - 0.2, w1[2]/2 + 0.2, r'$\vec{w}$',
         fontsize=16, color='#d32f2f', fontweight='bold')

ax1.set_title('Vecteurs coplanaires', fontsize=18, fontweight='bold', pad=20)

# Texte explicatif sous le titre
ax1.text2D(0.5, -0.1, r'$\vec{w}$ est une combinaison linéaire de $\vec{u}$ et $\vec{v}$', 
           transform=ax1.transAxes, fontsize=14, ha='center', va='top',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='#e8f5e8', edgecolor='#388e3c', linewidth=1))
ax1.text2D(0.5, -0.15, r'Tous les vecteurs appartiennent au même plan', 
           transform=ax1.transAxes, fontsize=12, ha='center', va='top',
           bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='#666', linewidth=1))

# ========== DEUXIÈME GRAPHE : VECTEURS NON-COPLANAIRES ==========
ax2 = fig.add_subplot(122, projection='3d')

# Désactiver les axes
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_zticks([])
ax2._axis3don = False

# Configuration
ax2.set_xlim([-2, 5])
ax2.set_ylim([-2, 5])
ax2.set_zlim([-2, 5])

# Trois vecteurs avec w non-coplanaire
u2 = np.array([3, 0, 0])    # Vecteur bleu horizontal
v2 = np.array([0, 3, 0])    # Vecteur vert vertical  
w2 = np.array([1, 1, 4])    # Vecteur rouge (sort du plan, plus prononcé)

# Tracer le plan défini par u et v
xx2, yy2 = np.meshgrid(np.linspace(-1.5, 4.5, 20), np.linspace(-1.5, 4.5, 20))
zz2 = np.zeros_like(xx2)
ax2.plot_surface(xx2, yy2, zz2, alpha=0.3, color='lightblue')

# Tracer les vecteurs
ax2.quiver(0, 0, 0, u2[0], u2[1], u2[2],
           color='#1976d2', arrow_length_ratio=0.1, linewidth=2)
ax2.text(u2[0]/2 + 0.2, u2[1]/2, u2[2]/2 + 0.2, r'$\vec{u}$',
         fontsize=16, color='#1976d2', fontweight='bold')

ax2.quiver(0, 0, 0, v2[0], v2[1], v2[2],
           color='#388e3c', arrow_length_ratio=0.1, linewidth=2)
ax2.text(v2[0]/2, v2[1]/2 + 0.2, v2[2]/2 + 0.2, r'$\vec{v}$',
         fontsize=16, color='#388e3c', fontweight='bold')

ax2.quiver(0, 0, 0, w2[0], w2[1], w2[2],
           color='#d32f2f', arrow_length_ratio=0.1, linewidth=2)
ax2.text(w2[0]/2 - 0.4, w2[1]/2, w2[2]/2 + 0.3, r'$\vec{w}$',
         fontsize=16, color='#d32f2f', fontweight='bold')

ax2.set_title('Vecteur non-coplanaire', fontsize=18, fontweight='bold', pad=20)

# Texte explicatif sous le titre
ax2.text2D(0.5, -0.1, '$\\vec{w}$ n\'est pas une combinaison linéaire de $\\vec{u}$ et $\\vec{v}$', 
           transform=ax2.transAxes, fontsize=14, ha='center', va='top',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='#ffebee', edgecolor='#d32f2f', linewidth=1))
ax2.text2D(0.5, -0.15, r'$\vec{w}$ sort du plan défini par $\vec{u}$ et $\vec{v}$', 
           transform=ax2.transAxes, fontsize=12, ha='center', va='top',
           bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='#666', linewidth=1))

# Pas de titre général

# Ajouter une barre verticale de séparation
fig.add_artist(plt.Line2D([0.5, 0.5], [0.1, 0.9], color='black', linewidth=2, transform=fig.transFigure))

plt.tight_layout()
plt.savefig('coplanarite_3d.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("✅ Graphe de coplanarité 3D simple généré : coplanarite_3d.png")
