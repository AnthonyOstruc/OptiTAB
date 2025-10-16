import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Configuration générale
plt.rcParams['font.size'] = 12
plt.rcParams['figure.facecolor'] = 'white'

# Créer la figure avec 4 sous-graphiques
fig = plt.figure(figsize=(16, 12))

# ===== GRAPHIQUE 1: DROITE DANS LE PLAN =====
ax1 = fig.add_subplot(2, 2, 1)

# Définir la droite dans le plan
A_2d = np.array([3, -2])  # Point de passage
u_2d = np.array([1, 2])    # Vecteur directeur

# Générer les points de la droite
t_2d = np.linspace(-2, 3, 100)
droite_x_2d = A_2d[0] + t_2d * u_2d[0]
droite_y_2d = A_2d[1] + t_2d * u_2d[1]

# Tracer la droite
ax1.plot(droite_x_2d, droite_y_2d, 'b-', linewidth=3, label='Droite $(d)$', alpha=0.8)

# Tracer le point A
ax1.scatter(A_2d[0], A_2d[1], color='blue', s=100, zorder=5)
ax1.text(A_2d[0] + 0.2, A_2d[1] + 0.2, 'A(3, -2)', fontsize=12, fontweight='bold', color='blue')

# Tracer le vecteur directeur
ax1.quiver(A_2d[0], A_2d[1], u_2d[0], u_2d[1], 
           color='red', linewidth=3, scale=10)
ax1.text(A_2d[0] + u_2d[0]/2 - 0.3, A_2d[1] + u_2d[1]/2 + 0.3, r'$\vec{u}$', 
         fontsize=14, fontweight='bold', color='red')

# Configuration du premier graphique
ax1.set_xlim(0, 8)
ax1.set_ylim(-6, 4)
ax1.set_aspect('equal', adjustable='box')
ax1.grid(True, alpha=0.3)
ax1.set_title('Droite dans le plan', fontsize=16, fontweight='bold', pad=20, color='#2c3e50')
ax1.legend(loc='upper left', fontsize=12, framealpha=0.9, edgecolor='black', fancybox=True)

# ===== GRAPHIQUE 2: DROITE DANS L'ESPACE (3D) =====
ax2 = fig.add_subplot(2, 2, 2, projection='3d')

# Définir la droite dans l'espace
A_3d = np.array([1, 2, -3])  # Point de passage
u_3d = np.array([2, -1, 4])  # Vecteur directeur

# Générer les points de la droite
t_3d = np.linspace(-1, 2, 100)
droite_x_3d = A_3d[0] + t_3d * u_3d[0]
droite_y_3d = A_3d[1] + t_3d * u_3d[1]
droite_z_3d = A_3d[2] + t_3d * u_3d[2]

# Tracer la droite
ax2.plot(droite_x_3d, droite_y_3d, droite_z_3d, 'b-', linewidth=3, label='Droite $(d)$', alpha=0.8)

# Tracer le point A
ax2.scatter(A_3d[0], A_3d[1], A_3d[2], color='blue', s=100, zorder=5)
ax2.text(A_3d[0], A_3d[1], A_3d[2] + 0.5, 'A(1, 2, -3)', fontsize=12, fontweight='bold', color='blue')

# Tracer le vecteur directeur
ax2.quiver(A_3d[0], A_3d[1], A_3d[2], u_3d[0], u_3d[1], u_3d[2], 
           color='red', arrow_length_ratio=0.1, linewidth=3)
ax2.text(A_3d[0] + u_3d[0]/2 - 0.3, A_3d[1] + u_3d[1]/2 - 0.3, A_3d[2] + u_3d[2]/2 + 0.5, 
         r'$\vec{u}$', fontsize=14, fontweight='bold', color='red')

# Configuration du deuxième graphique 3D
ax2.set_xlim(-2, 6)
ax2.set_ylim(-2, 4)
ax2.set_zlim(-6, 4)
ax2.set_title('Droite dans l\'espace', fontsize=16, fontweight='bold', pad=20, color='#2c3e50')
ax2.legend(loc='upper left', fontsize=12, framealpha=0.9, edgecolor='black', fancybox=True)

# Améliorer l'angle de vue
ax2.view_init(elev=20, azim=45)

# ===== GRAPHIQUE 3: REPRÉSENTATION PARAMÉTRIQUE =====
ax3 = fig.add_subplot(2, 2, 3)

# Créer un graphique pour montrer la représentation paramétrique
ax3.text(0.5, 0.9, 'Représentation paramétrique :', 
         transform=ax3.transAxes, fontsize=16, fontweight='bold', color='#2c3e50', ha='center')

# Formule pour le plan
ax3.text(0.5, 0.7, 'Dans le plan :', 
         transform=ax3.transAxes, fontsize=14, ha='center', fontweight='bold')
ax3.text(0.5, 0.6, 'x = x₀ + at', 
         transform=ax3.transAxes, fontsize=12, ha='center', 
         bbox=dict(boxstyle='round,pad=0.2', facecolor='lightblue', edgecolor='blue', alpha=0.8))
ax3.text(0.5, 0.5, 'y = y₀ + bt', 
         transform=ax3.transAxes, fontsize=12, ha='center',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='lightblue', edgecolor='blue', alpha=0.8))

# Formule pour l'espace
ax3.text(0.5, 0.35, 'Dans l\'espace :', 
         transform=ax3.transAxes, fontsize=14, ha='center', fontweight='bold')
ax3.text(0.5, 0.25, 'x = x₀ + at', 
         transform=ax3.transAxes, fontsize=12, ha='center',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', edgecolor='green', alpha=0.8))
ax3.text(0.5, 0.15, 'y = y₀ + bt', 
         transform=ax3.transAxes, fontsize=12, ha='center',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', edgecolor='green', alpha=0.8))
ax3.text(0.5, 0.05, 'z = z₀ + ct', 
         transform=ax3.transAxes, fontsize=12, ha='center',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', edgecolor='green', alpha=0.8))

ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')
ax3.set_title('Formules paramétriques', fontsize=16, fontweight='bold', pad=20, color='#2c3e50')

# ===== GRAPHIQUE 4: EXEMPLE NUMÉRIQUE =====
ax4 = fig.add_subplot(2, 2, 4)

# Créer un graphique pour montrer l'exemple numérique
ax4.text(0.5, 0.9, 'Exemple numérique :', 
         transform=ax4.transAxes, fontsize=16, fontweight='bold', color='#2c3e50', ha='center')

# Données de l'exemple
ax4.text(0.5, 0.8, 'Point : A(1, 2, -3)', 
         transform=ax4.transAxes, fontsize=12, ha='center', color='blue')

ax4.text(0.5, 0.7, 'Vecteur : u⃗ = (2, -1, 4)', 
         transform=ax4.transAxes, fontsize=12, ha='center', color='red')

# Représentation paramétrique de l'exemple
ax4.text(0.5, 0.55, 'x = 1 + 2t', 
         transform=ax4.transAxes, fontsize=12, ha='center',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow', edgecolor='orange', alpha=0.8))
ax4.text(0.5, 0.45, 'y = 2 - t', 
         transform=ax4.transAxes, fontsize=12, ha='center',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow', edgecolor='orange', alpha=0.8))
ax4.text(0.5, 0.35, 'z = -3 + 4t', 
         transform=ax4.transAxes, fontsize=12, ha='center',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow', edgecolor='orange', alpha=0.8))

ax4.text(0.5, 0.2, 't ∈ ℝ', 
         transform=ax4.transAxes, fontsize=12, ha='center', fontweight='bold', color='red')

ax4.text(0.5, 0.1, 'Pour t = 0 : point A', 
         transform=ax4.transAxes, fontsize=10, ha='center', color='gray')

ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
ax4.axis('off')
ax4.set_title('Exemple concret', fontsize=16, fontweight='bold', pad=20, color='#2c3e50')

# Ajuster la mise en page
plt.tight_layout()

# Sauvegarder le graphique
output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'images', 'representation_parametrique_droite.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"Graphique sauvegardé : {output_path}")

# Afficher le graphique
plt.show()
