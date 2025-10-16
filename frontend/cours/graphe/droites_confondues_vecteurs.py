import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import os

# Configuration pour un rendu professionnel
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2

# Créer la figure avec quatre sous-graphiques (2 en haut, 2 en bas)
fig = plt.figure(figsize=(16, 12))
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4, projection='3d')

# ===== GRAPHIQUE 1: DROITES PARALLÈLES =====
# Définir les vecteurs directeurs (parallèles, donc colinéaires)
u1 = np.array([2, 1])
u2 = np.array([2, 1])  # Même direction, donc parallèles

# Définir les points de passage pour les deux droites
A = np.array([0, 1])   # Point sur la première droite
B = np.array([1, 4])   # Point sur la deuxième droite

# Générer les points des droites
t = np.linspace(-3, 5, 100)

# Droite 1 : passe par A avec vecteur directeur u1
droite1_x = A[0] + t * u1[0]
droite1_y = A[1] + t * u1[1]

# Droite 2 : passe par B avec vecteur directeur u2
droite2_x = B[0] + t * u2[0]
droite2_y = B[1] + t * u2[1]

# Tracer les droites parallèles
ax1.plot(droite1_x, droite1_y, 'b-', linewidth=2.5, label='Droite $d_1$', alpha=0.8)
ax1.plot(droite2_x, droite2_y, 'r-', linewidth=2.5, label='Droite $d_2$', alpha=0.8)

# Tracer les points A et B
ax1.plot(A[0], A[1], 'bo', markersize=10, zorder=5)
ax1.plot(B[0], B[1], 'ro', markersize=10, zorder=5)
ax1.text(A[0] - 0.3, A[1] - 0.5, '$A$', fontsize=14, fontweight='bold', color='blue')
ax1.text(B[0] - 0.3, B[1] + 0.5, '$B$', fontsize=14, fontweight='bold', color='red')

# Tracer les vecteurs directeurs u1 et u2
arrow1 = FancyArrowPatch(A, A + u1,
                         arrowstyle='->', mutation_scale=25,
                         linewidth=3, color='blue', zorder=10)
ax1.add_patch(arrow1)
ax1.text(A[0] + u1[0]/2 - 0.5, A[1] + u1[1]/2 + 0.3, r'$\vec{u_1}$', 
        fontsize=16, fontweight='bold', color='blue')

arrow2 = FancyArrowPatch(B, B + u2,
                         arrowstyle='->', mutation_scale=25,
                         linewidth=3, color='red', zorder=10)
ax1.add_patch(arrow2)
ax1.text(B[0] + u2[0]/2 - 0.5, B[1] + u2[1]/2 + 0.3, r'$\vec{u_2}$', 
        fontsize=16, fontweight='bold', color='red')

# Annotation pour droites parallèles
ax1.text(1, 8, r'$\vec{u_1} = \vec{u_2}$ (vecteurs colinéaires)', 
        fontsize=9, color='darkgreen', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', edgecolor='darkgreen', linewidth=1.5, alpha=0.8))
ax1.text(1, 7, r'$\Rightarrow$ Droites parallèles $d_1 \parallel d_2$', 
        fontsize=9, color='darkgreen', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', edgecolor='darkgreen', linewidth=1.5, alpha=0.8))

# Configuration du premier graphique
ax1.set_xlim(-2, 8)
ax1.set_ylim(-1, 10)
ax1.set_aspect('equal', adjustable='box')
ax1.axis('off')
ax1.set_title('Droites Parallèles', fontsize=16, fontweight='bold', pad=20, color='#2c3e50')
ax1.legend(loc='upper left', fontsize=12, framealpha=0.9, edgecolor='black', fancybox=True)

# ===== GRAPHIQUE 2: DROITES CONFONDUES =====
# Définir les vecteurs directeurs (colinéaires)
u1_conf = np.array([2, 1])
u2_conf = np.array([4, 2])  # 2 * u1_conf, donc colinéaires

# Définir le même point de passage pour les deux droites (confondues)
A_conf = np.array([0, 1])   # Point commun

# Générer les points des droites confondues
t_conf = np.linspace(-3, 5, 100)

# Les deux droites sont identiques (confondues)
droite1_conf_x = A_conf[0] + t_conf * u1_conf[0]
droite1_conf_y = A_conf[1] + t_conf * u1_conf[1]

droite2_conf_x = A_conf[0] + t_conf * u2_conf[0]
droite2_conf_y = A_conf[1] + t_conf * u2_conf[1]

# Tracer les droites confondues (une seule ligne visible)
ax2.plot(droite1_conf_x, droite1_conf_y, 'purple', linewidth=3, label='Droites confondues $d_1 = d_2$', alpha=0.8)

# Tracer le point commun
ax2.plot(A_conf[0], A_conf[1], 'go', markersize=12, zorder=5)
ax2.text(A_conf[0] - 0.3, A_conf[1] - 0.5, '$A$', fontsize=14, fontweight='bold', color='green')

# Tracer les vecteurs directeurs u1 et u2 (colinéaires)
arrow1_conf = FancyArrowPatch(A_conf, A_conf + u1_conf,
                              arrowstyle='->', mutation_scale=25,
                              linewidth=3, color='blue', zorder=10)
ax2.add_patch(arrow1_conf)
ax2.text(A_conf[0] + u1_conf[0]/2 - 0.5, A_conf[1] + u1_conf[1]/2 + 0.3, r'$\vec{u_1}$', 
        fontsize=16, fontweight='bold', color='blue')

# Décaler u2 vers la droite mais le faire toucher la droite confondue
offset = np.array([4.0, 2.0])  # Décalage vers la droite et descendu pour toucher la droite mauve
arrow2_conf = FancyArrowPatch(A_conf + offset, A_conf + offset + u2_conf,
                              arrowstyle='->', mutation_scale=25,
                              linewidth=3, color='red', zorder=10)
ax2.add_patch(arrow2_conf)
ax2.text(A_conf[0] + offset[0] + u2_conf[0]/2 - 0.5, A_conf[1] + offset[1] + u2_conf[1]/2 + 0.3, r'$\vec{u_2}$', 
        fontsize=16, fontweight='bold', color='red')

# Annotation pour droites confondues
ax2.text(1, 8, r'$\vec{u_1}$ et $\vec{u_2}$ colinéaires', 
        fontsize=9, color='darkgreen', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', edgecolor='darkgreen', linewidth=1.5, alpha=0.8))
ax2.text(1, 7, r'$\Rightarrow$ Droites confondues $d_1 = d_2$', 
        fontsize=9, color='darkgreen', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', edgecolor='darkgreen', linewidth=1.5, alpha=0.8))

# Configuration du deuxième graphique
ax2.set_xlim(-2, 8)
ax2.set_ylim(-1, 10)
ax2.set_aspect('equal', adjustable='box')
ax2.axis('off')
ax2.set_title('Droites Confondues', fontsize=16, fontweight='bold', pad=20, color='#2c3e50')
ax2.legend(loc='upper left', fontsize=12, framealpha=0.9, edgecolor='black', fancybox=True)

# ===== GRAPHIQUE 3: DROITES SÉCANTES =====
# Définir les vecteurs directeurs (non colinéaires)
u1_sec = np.array([2, 1])
u2_sec = np.array([-1, 2])  # Non colinéaire à u1_sec

# Définir le point d'intersection commun
P_sec = np.array([2, 3])

# Générer les points des droites
t_sec = np.linspace(-3, 5, 100)

# Droite 1 : passe par P avec vecteur directeur u1_sec
droite1_x_sec = P_sec[0] + t_sec * u1_sec[0]
droite1_y_sec = P_sec[1] + t_sec * u1_sec[1]

# Droite 2 : passe par P avec vecteur directeur u2_sec
droite2_x_sec = P_sec[0] + t_sec * u2_sec[0]
droite2_y_sec = P_sec[1] + t_sec * u2_sec[1]

# Tracer les droites sécantes
ax3.plot(droite1_x_sec, droite1_y_sec, 'b-', linewidth=2.5, label='Droite $d_1$', alpha=0.8)
ax3.plot(droite2_x_sec, droite2_y_sec, 'r-', linewidth=2.5, label='Droite $d_2$', alpha=0.8)

# Tracer le point d'intersection P
ax3.plot(P_sec[0], P_sec[1], 'go', markersize=10, zorder=5)
ax3.text(P_sec[0] + 0.2, P_sec[1] + 0.2, 'P', fontsize=14, fontweight='bold', color='green')

# Tracer les vecteurs directeurs
arrow1_sec = FancyArrowPatch(P_sec, P_sec + u1_sec,
                             arrowstyle='->', mutation_scale=25,
                             linewidth=3, color='blue', zorder=10)
ax3.add_patch(arrow1_sec)
ax3.text(P_sec[0] + u1_sec[0]/2 - 0.5, P_sec[1] + u1_sec[1]/2 + 0.3, r'$\vec{u_1}$', 
        fontsize=16, fontweight='bold', color='blue')

arrow2_sec = FancyArrowPatch(P_sec, P_sec + u2_sec,
                             arrowstyle='->', mutation_scale=25,
                             linewidth=3, color='red', zorder=10)
ax3.add_patch(arrow2_sec)
ax3.text(P_sec[0] + u2_sec[0]/2 - 1.5, P_sec[1] + u2_sec[1]/2 + 0.3, r'$\vec{u_2}$', 
        fontsize=16, fontweight='bold', color='red')

# Annotation pour droites sécantes
ax3.text(1, 8, r'$\vec{u_1}$ et $\vec{u_2}$ non colinéaires', 
        fontsize=9, color='darkgreen', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', edgecolor='darkgreen', linewidth=1.5, alpha=0.8))
ax3.text(1, 7, r'et un point commun $\Rightarrow$ Droites sécantes', 
        fontsize=9, color='darkgreen', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', edgecolor='darkgreen', linewidth=1.5, alpha=0.8))

# Configuration du troisième graphique
ax3.set_xlim(-2, 8)
ax3.set_ylim(-1, 10)
ax3.set_aspect('equal', adjustable='box')
ax3.axis('off')
ax3.set_title('Droites Sécantes', fontsize=16, fontweight='bold', pad=20, color='#2c3e50')
ax3.legend(loc='upper left', fontsize=12, framealpha=0.9, edgecolor='black', fancybox=True)

# ===== GRAPHIQUE 4: DROITES NON COPLANAIRES (3D) =====
# Créer un cube pour visualiser les droites non coplanaires
# Définir les sommets du cube
cube_size = 2
cube_vertices = np.array([
    [0, 0, 0], [cube_size, 0, 0], [cube_size, cube_size, 0], [0, cube_size, 0],  # Face inférieure
    [0, 0, cube_size], [cube_size, 0, cube_size], [cube_size, cube_size, cube_size], [0, cube_size, cube_size]  # Face supérieure
])

# Tracer le cube (arêtes)
cube_edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],  # Face inférieure
    [4, 5], [5, 6], [6, 7], [7, 4],  # Face supérieure
    [0, 4], [1, 5], [2, 6], [3, 7]   # Arêtes verticales
]

for edge in cube_edges:
    points = cube_vertices[edge]
    ax4.plot3D(*points.T, 'k-', linewidth=1, alpha=0.3)

# Définir les droites non coplanaires dans le cube
# Droite 1 : sur le sol du cube (z=0) - dépasse encore plus des deux côtés
A_3d = np.array([0.1, 0, 0])  # Point sur le sol
u1_3d = np.array([1, 0, 0])   # Vecteur horizontal
t_3d = np.linspace(-0.8, 2.8, 100)  # Encore plus long
droite1_x_3d = A_3d[0] + t_3d * u1_3d[0]
droite1_y_3d = A_3d[1] + t_3d * u1_3d[1]
droite1_z_3d = A_3d[2] + t_3d * u1_3d[2]

# Droite 2 : sur le plafond du cube (z=2) - dépasse encore plus des deux côtés
B_3d = np.array([0, 0.1, 2])  # Point sur le plafond
u2_3d = np.array([0, 1, 0])    # Vecteur horizontal
droite2_x_3d = B_3d[0] + t_3d * u2_3d[0]
droite2_y_3d = B_3d[1] + t_3d * u2_3d[1]
droite2_z_3d = B_3d[2] + t_3d * u2_3d[2]

# Tracer les droites non coplanaires
ax4.plot(droite1_x_3d, droite1_y_3d, droite1_z_3d, 'b-', linewidth=2, label='Droite $d_1$ (sol)', alpha=0.9)
ax4.plot(droite2_x_3d, droite2_y_3d, droite2_z_3d, 'r-', linewidth=2, label='Droite $d_2$ (plafond)', alpha=0.9)

# Tracer les points A et B
ax4.scatter(A_3d[0], A_3d[1], A_3d[2], color='blue', s=100, zorder=5)
ax4.scatter(B_3d[0], B_3d[1], B_3d[2], color='red', s=100, zorder=5)
ax4.text(A_3d[0], A_3d[1], A_3d[2] + 0.3, 'A', fontsize=14, fontweight='bold', color='blue')
ax4.text(B_3d[0] + 0.2, B_3d[1], B_3d[2] + 0.3, 'B', fontsize=14, fontweight='bold', color='red')

# Tracer les vecteurs directeurs (style fin avec pointe plus grande)
# Vecteur u1 (bleu) - style fin avec pointe plus grande
ax4.quiver(A_3d[0], A_3d[1], A_3d[2], u1_3d[0], u1_3d[1], u1_3d[2], 
           color='blue', arrow_length_ratio=0.2, linewidth=2)
ax4.text(A_3d[0] + u1_3d[0]/2 - 0.3, A_3d[1] + u1_3d[1]/2 - 0.3, A_3d[2] + u1_3d[2]/2 + 0.3, 
         r'$\vec{u_1}$', fontsize=14, fontweight='bold', color='blue')

# Vecteur u2 (rouge) - style fin avec pointe plus grande
ax4.quiver(B_3d[0], B_3d[1], B_3d[2], u2_3d[0], u2_3d[1], u2_3d[2], 
           color='red', arrow_length_ratio=0.2, linewidth=2)
ax4.text(B_3d[0] + u2_3d[0]/2 - 0.3, B_3d[1] + u2_3d[1]/2 - 0.3, B_3d[2] + u2_3d[2]/2 + 0.3, 
         r'$\vec{u_2}$', fontsize=14, fontweight='bold', color='red')

# Configuration du quatrième graphique 3D
ax4.set_xlim(-0.8, 2.8)
ax4.set_ylim(-0.8, 2.8)
ax4.set_zlim(-0.5, 2.5)
ax4.set_title('Droites Non Coplanaires', fontsize=16, fontweight='bold', pad=20, color='#2c3e50')
ax4.legend(loc='upper left', fontsize=12, framealpha=0.9, edgecolor='black', fancybox=True)

# Améliorer l'angle de vue pour mieux voir le cube
ax4.view_init(elev=20, azim=45)

# Supprimer complètement les axes 3D
ax4.set_xticks([])
ax4.set_yticks([])
ax4.set_zticks([])
ax4.grid(False)
ax4.set_xlabel('')
ax4.set_ylabel('')
ax4.set_zlabel('')
ax4._axis3don = False

# Ajouter une annotation pour les droites non coplanaires
ax4.text2D(0.75, 0.95, r'$\vec{u_1}$ et $\vec{u_2}$ non colinéaires', 
           transform=ax4.transAxes, fontsize=9, color='darkgreen', fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', edgecolor='darkgreen', linewidth=1.5, alpha=0.8))
ax4.text2D(0.75, 0.88, r'et aucun point commun', 
           transform=ax4.transAxes, fontsize=9, color='darkgreen', fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', edgecolor='darkgreen', linewidth=1.5, alpha=0.8))
ax4.text2D(0.75, 0.81, r'$\Rightarrow$ Droites non coplanaires', 
           transform=ax4.transAxes, fontsize=9, color='darkgreen', fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.2', facecolor='lightgreen', edgecolor='darkgreen', linewidth=1.5, alpha=0.8))
ax4.text2D(0.75, 0.74, r'Les droites sont dans des plans différents', 
           transform=ax4.transAxes, fontsize=8, color='darkblue', fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.2', facecolor='lightblue', edgecolor='darkblue', linewidth=1.5, alpha=0.8))

# Ajuster la mise en page
plt.tight_layout()

# Sauvegarder le graphique
output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'images', 'droites_paralleles_confondues.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"Graphique sauvegardé : {output_path}")

# Afficher le graphique
plt.show()
