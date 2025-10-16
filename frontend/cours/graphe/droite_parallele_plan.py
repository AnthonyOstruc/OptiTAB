import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os

# Configuration pour un rendu professionnel
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

# Créer la figure 3D
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# ============= DÉFINIR LE CUBE =============
# Sommets du cube (coin à l'origine, arête = 3)
cube_size = 3
vertices = np.array([
    [0, 0, 0], [cube_size, 0, 0], [cube_size, cube_size, 0], [0, cube_size, 0],  # Base
    [0, 0, cube_size], [cube_size, 0, cube_size], [cube_size, cube_size, cube_size], [0, cube_size, cube_size]  # Sommet
])

# Définir les faces du cube
faces = [
    [vertices[0], vertices[1], vertices[5], vertices[4]],  # Face avant
    [vertices[2], vertices[3], vertices[7], vertices[6]],  # Face arrière
    [vertices[0], vertices[3], vertices[7], vertices[4]],  # Face gauche
    [vertices[1], vertices[2], vertices[6], vertices[5]],  # Face droite
    [vertices[0], vertices[1], vertices[2], vertices[3]],  # Face bas
    [vertices[4], vertices[5], vertices[6], vertices[7]]   # Face haut
]

# Créer une collection de polygones pour le cube
cube_collection = Poly3DCollection(faces, alpha=0.15, facecolor='lightblue', 
                                   edgecolor='darkblue', linewidth=1.5)
ax.add_collection3d(cube_collection)

# Tracer les arêtes du cube pour meilleure visibilité
edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],  # Base
    [4, 5], [5, 6], [6, 7], [7, 4],  # Sommet
    [0, 4], [1, 5], [2, 6], [3, 7]   # Verticales
]
for edge in edges:
    points = vertices[edge]
    ax.plot3D(*points.T, 'b-', linewidth=2, alpha=0.6)

# ============= DÉFINIR LE PLAN =============
# Équation du plan : x + y + z = 6
# Vecteur normal : n = (1, 1, 1)
vecteur_normal = np.array([1, 1, 1])

# Créer une grille pour le plan
x_plan = np.linspace(-1, 7, 20)
y_plan = np.linspace(-1, 7, 20)
X_plan, Y_plan = np.meshgrid(x_plan, y_plan)

# Équation du plan : x + y + z = 6 => z = 6 - x - y
Z_plan = 6 - X_plan - Y_plan

# Tracer le plan avec transparence
ax.plot_surface(X_plan, Y_plan, Z_plan, alpha=0.3, color='yellow', 
                edgecolor='orange', linewidth=0.5)

# Point sur le plan pour dessiner le vecteur normal
point_plan = np.array([2, 2, 2])  # Ce point est sur le plan car 2+2+2=6

# Tracer le vecteur normal n
scale_n = 1.5
ax.quiver(point_plan[0], point_plan[1], point_plan[2],
          vecteur_normal[0], vecteur_normal[1], vecteur_normal[2],
          color='red', arrow_length_ratio=0.3, linewidth=4, 
          label=r'Vecteur normal $\vec{n}$')

# Ajouter le label pour le vecteur normal
ax.text(point_plan[0] + scale_n*vecteur_normal[0]*0.7, 
        point_plan[1] + scale_n*vecteur_normal[1]*0.7,
        point_plan[2] + scale_n*vecteur_normal[2]*0.7 + 0.3,
        r'$\vec{n}(1,1,1)$', fontsize=14, fontweight='bold', color='red',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                  edgecolor='red', linewidth=2))

# ============= DÉFINIR LA DROITE PARALLÈLE AU PLAN =============
# Pour qu'une droite soit parallèle au plan, son vecteur directeur u
# doit être orthogonal au vecteur normal n, donc u·n = 0

# Choisir un vecteur directeur u orthogonal à n = (1,1,1)
# Par exemple u = (1, -1, 0) car (1,1,1)·(1,-1,0) = 1-1+0 = 0
vecteur_directeur = np.array([1, -1, 0])

# Point de passage de la droite (pas sur le plan)
point_droite = np.array([1, 4, 3])

# Paramètre t pour la droite
t = np.linspace(-2, 4, 100)

# Équation paramétrique de la droite : P = point_droite + t*vecteur_directeur
droite_x = point_droite[0] + t * vecteur_directeur[0]
droite_y = point_droite[1] + t * vecteur_directeur[1]
droite_z = point_droite[2] + t * vecteur_directeur[2]

# Tracer la droite
ax.plot3D(droite_x, droite_y, droite_z, 'g-', linewidth=3.5, 
          label='Droite $d$ parallèle au plan', alpha=0.9)

# Tracer le point sur la droite
ax.scatter(*point_droite, color='green', s=100, marker='o', 
           edgecolor='darkgreen', linewidth=2, zorder=10)
ax.text(point_droite[0]-0.3, point_droite[1]+0.3, point_droite[2]+0.3,
        '$A$', fontsize=14, fontweight='bold', color='green')

# Tracer le vecteur directeur u à partir du point A
scale_u = 2
ax.quiver(point_droite[0], point_droite[1], point_droite[2],
          vecteur_directeur[0], vecteur_directeur[1], vecteur_directeur[2],
          color='darkgreen', arrow_length_ratio=0.2, linewidth=4,
          length=scale_u, label=r'Vecteur directeur $\vec{u}$')

# Ajouter le label pour le vecteur directeur
ax.text(point_droite[0] + scale_u*vecteur_directeur[0]*0.6,
        point_droite[1] + scale_u*vecteur_directeur[1]*0.6,
        point_droite[2] + scale_u*vecteur_directeur[2]*0.6 + 0.5,
        r'$\vec{u}(1,-1,0)$', fontsize=14, fontweight='bold', color='darkgreen',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                  edgecolor='darkgreen', linewidth=2))

# ============= AJOUTER DES ANNOTATIONS =============
# Annotation du plan
ax.text(5, 1, 5, 'Plan $\mathcal{P}$:\n$x + y + z = 6$', 
        fontsize=13, fontweight='bold', color='darkorange',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', 
                  edgecolor='orange', linewidth=2))

# Annotation sur la condition de parallélisme
condition_text = (r'$\vec{u} \perp \vec{n}$ (orthogonaux)' + '\n' +
                  r'$\vec{u} \cdot \vec{n} = 1(1) + (-1)(1) + 0(1) = 0$' + '\n' +
                  r'$\Rightarrow$ Droite $d \parallel$ Plan $\mathcal{P}$')

ax.text2D(0.02, 0.98, condition_text,
          transform=ax.transAxes, fontsize=12, fontweight='bold',
          verticalalignment='top', color='darkblue',
          bbox=dict(boxstyle='round,pad=0.8', facecolor='lightcyan',
                    edgecolor='darkblue', linewidth=2.5, alpha=0.95))

# ============= CONFIGURATION DES AXES =============
ax.set_xlabel('X', fontsize=12, fontweight='bold', labelpad=10)
ax.set_ylabel('Y', fontsize=12, fontweight='bold', labelpad=10)
ax.set_zlabel('Z', fontsize=12, fontweight='bold', labelpad=10)

# Limites des axes
ax.set_xlim(-1, 7)
ax.set_ylim(-1, 7)
ax.set_zlim(-1, 7)

# Titre
ax.set_title('Droite Parallèle au Plan\nCondition : $\\vec{u} \\cdot \\vec{n} = 0$',
             fontsize=16, fontweight='bold', pad=20, color='#2c3e50')

# Vue optimale
ax.view_init(elev=25, azim=45)

# Grille
ax.grid(True, alpha=0.3)

# Légende
ax.legend(loc='upper right', fontsize=11, framealpha=0.95, 
          edgecolor='black', fancybox=True)

# ============= SAUVEGARDER =============
output_path = os.path.join(os.path.dirname(__file__), '..', '..', 
                           'public', 'images', 'droite_parallele_plan.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print(f"✓ Graphique sauvegardé : {output_path}")

# Afficher
plt.tight_layout()
plt.show()

