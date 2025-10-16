import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import os

# Configuration pour un rendu professionnel
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2

# Créer la figure
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

# Définir les vecteurs directeurs (parallèles, donc colinéaires)
u1 = np.array([2, 1])
u2 = np.array([2, 1])  # Même direction, donc parallèles

# Définir les points de passage pour les deux droites
A = np.array([0, 1])   # Point sur la première droite
B = np.array([1, 4])   # Point sur la deuxième droite

# Générer les points des droites
t = np.linspace(-3, 5, 100)

# Droite 1 : passe par A avec vecteur directeur u1
# Équation paramétrique : (x, y) = A + t * u1
droite1_x = A[0] + t * u1[0]
droite1_y = A[1] + t * u1[1]

# Droite 2 : passe par B avec vecteur directeur u2
# Équation paramétrique : (x, y) = B + t * u2
droite2_x = B[0] + t * u2[0]
droite2_y = B[1] + t * u2[1]

# Tracer les droites
ax.plot(droite1_x, droite1_y, 'b-', linewidth=2.5, label='Droite $d_1$', alpha=0.8)
ax.plot(droite2_x, droite2_y, 'r-', linewidth=2.5, label='Droite $d_2$', alpha=0.8)

# Tracer les points A et B
ax.plot(A[0], A[1], 'bo', markersize=10, zorder=5)
ax.plot(B[0], B[1], 'ro', markersize=10, zorder=5)
ax.text(A[0] - 0.3, A[1] - 0.5, '$A$', fontsize=14, fontweight='bold', color='blue')
ax.text(B[0] - 0.3, B[1] + 0.5, '$B$', fontsize=14, fontweight='bold', color='red')

# Tracer les vecteurs directeurs u1 et u2
# Vecteur u1 à partir du point A
arrow1 = FancyArrowPatch(A, A + u1,
                         arrowstyle='->', mutation_scale=25,
                         linewidth=3, color='blue', zorder=10)
ax.add_patch(arrow1)
ax.text(A[0] + u1[0]/2 - 0.5, A[1] + u1[1]/2 + 0.3, r'$\vec{u_1}$', 
        fontsize=16, fontweight='bold', color='blue',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='blue', linewidth=2))

# Vecteur u2 à partir du point B
arrow2 = FancyArrowPatch(B, B + u2,
                         arrowstyle='->', mutation_scale=25,
                         linewidth=3, color='red', zorder=10)
ax.add_patch(arrow2)
ax.text(B[0] + u2[0]/2 - 0.5, B[1] + u2[1]/2 + 0.3, r'$\vec{u_2}$', 
        fontsize=16, fontweight='bold', color='red',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='red', linewidth=2))

# Ajouter une annotation pour expliquer le parallélisme
ax.text(1, 8, r'$\vec{u_1} = \vec{u_2}$ (vecteurs colinéaires)', 
        fontsize=13, color='darkgreen', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', edgecolor='darkgreen', linewidth=2, alpha=0.8))
ax.text(1, 7, r'$\Rightarrow$ Droites parallèles $d_1 \parallel d_2$', 
        fontsize=13, color='darkgreen', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', edgecolor='darkgreen', linewidth=2, alpha=0.8))

# Configuration des axes
ax.set_xlim(-2, 8)
ax.set_ylim(-1, 10)
ax.set_aspect('equal', adjustable='box')

# Supprimer les axes, graduations et quadrillage
ax.axis('off')

# Titre
ax.set_title('Droites Parallèles avec Vecteurs Directeurs', 
             fontsize=16, fontweight='bold', pad=20, color='#2c3e50')

# Légende
ax.legend(loc='upper left', fontsize=12, framealpha=0.9, edgecolor='black', fancybox=True)

# Ajuster la mise en page
plt.tight_layout()

# Sauvegarder le graphique
output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'images', 'droites_paralleles_vecteurs.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"Graphique sauvegardé : {output_path}")

# Afficher le graphique
plt.show()

