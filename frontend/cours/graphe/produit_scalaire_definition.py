import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Arc
import matplotlib.patches as patches

# Configuration du graphique avec une meilleure présentation
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(-1, 8)
ax.set_ylim(-1, 7)
ax.set_aspect('equal')

# Suppression complète des axes
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Définition des vecteurs pour une présentation claire
origin = np.array([1.5, 1.5])
u_end = np.array([5, 2])
v_end = np.array([2.5, 5])

# Calcul des vecteurs
u_vector = u_end - origin
v_vector = v_end - origin

# Calculs mathématiques
dot_product = np.dot(u_vector, v_vector)
norm_u = np.linalg.norm(u_vector)
norm_v = np.linalg.norm(v_vector)
cos_theta = dot_product / (norm_u * norm_v)
angle_rad = np.arccos(np.clip(cos_theta, -1, 1))
angle_deg = np.degrees(angle_rad)

# Tracé des vecteurs avec un style professionnel
arrow_u = FancyArrowPatch(origin, u_end, 
                         arrowstyle='->', mutation_scale=30, 
                         color='#1f77b4', linewidth=5, alpha=0.8)
arrow_v = FancyArrowPatch(origin, v_end, 
                         arrowstyle='->', mutation_scale=30, 
                         color='#ff7f0e', linewidth=5, alpha=0.8)

ax.add_patch(arrow_u)
ax.add_patch(arrow_v)

# Arc d'angle avec un style soigné
arc_radius = 1.0
arc = Arc(origin, 2*arc_radius, 2*arc_radius, angle=0, theta1=0, theta2=angle_deg, 
          color='#2ca02c', linewidth=4, alpha=0.8)
ax.add_patch(arc)

# Labels des vecteurs avec un style professionnel
ax.text(u_end[0] + 0.4, u_end[1] + 0.2, r'$\vec{u}$', fontsize=22, color='#1f77b4', 
        weight='bold', ha='center', va='center')
ax.text(v_end[0] + 0.4, v_end[1] + 0.2, r'$\vec{v}$', fontsize=22, color='#ff7f0e', 
        weight='bold', ha='center', va='center')

# Label de l'angle
angle_text_x = origin[0] + arc_radius * np.cos(angle_rad/2)
angle_text_y = origin[1] + arc_radius * np.sin(angle_rad/2)
ax.text(angle_text_x, angle_text_y, r'$\theta$', fontsize=20, color='#2ca02c', 
        weight='bold', ha='center', va='center')

# Point d'origine
ax.plot(origin[0], origin[1], 'ko', markersize=10, zorder=5)
ax.text(origin[0] - 0.3, origin[1] - 0.4, 'O', fontsize=16, weight='bold', ha='center')

# Titre principal avec un style professionnel
ax.text(4, 6.2, 'Définition géométrique du produit scalaire', 
        fontsize=20, weight='bold', ha='center', color='#2c3e50')

# Formule principale dans un encadré élégant
formula_text = r'$\vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}\| \times \cos(\theta)$'
formula_box = patches.FancyBboxPatch((2.5, 5.4), 3, 0.6, 
                                    boxstyle="round,pad=0.1", 
                                    facecolor='#e8f4fd', 
                                    edgecolor='#3498db', 
                                    linewidth=2)
ax.add_patch(formula_box)
ax.text(4, 5.7, formula_text, fontsize=16, ha='center', va='center', 
        color='#2c3e50', weight='bold')

# Section des calculs avec un design soigné
calc_title = "Calculs :"
ax.text(0.5, 4.5, calc_title, fontsize=16, weight='bold', color='#2c3e50')

calc_text = f'$\|\vec{{u}}\| = {norm_u:.2f}$\n$\|\vec{{v}}\| = {norm_v:.2f}$\n$\\theta = {angle_deg:.1f}°$\n$\\cos(\\theta) = {cos_theta:.3f}$'
calc_box = patches.FancyBboxPatch((0.2, 2.8), 2.2, 1.5, 
                                 boxstyle="round,pad=0.15", 
                                 facecolor='#f8f9fa', 
                                 edgecolor='#6c757d', 
                                 linewidth=1.5)
ax.add_patch(calc_box)
ax.text(1.3, 3.55, calc_text, fontsize=14, ha='center', va='center', 
        color='#2c3e50')

# Résultat du produit scalaire
result_title = "Résultat :"
ax.text(5.5, 4.5, result_title, fontsize=16, weight='bold', color='#2c3e50')

result_text = f'$\\vec{{u}} \\cdot \\vec{{v}} = {dot_product:.2f}$'
result_box = patches.FancyBboxPatch((5.2, 3.8), 2.2, 0.6, 
                                   boxstyle="round,pad=0.15", 
                                   facecolor='#d5f4e6', 
                                   edgecolor='#27ae60', 
                                   linewidth=2)
ax.add_patch(result_box)
ax.text(6.3, 4.1, result_text, fontsize=16, ha='center', va='center', 
        color='#2c3e50', weight='bold')

# Vérification avec la formule
verif_calc = norm_u * norm_v * cos_theta
verif_title = "Vérification :"
ax.text(4, 2.5, verif_title, fontsize=16, weight='bold', ha='center', color='#2c3e50')

verif_text = f'${norm_u:.2f} \\times {norm_v:.2f} \\times {cos_theta:.3f} = {verif_calc:.2f}$'
verif_box = patches.FancyBboxPatch((2.5, 1.5), 3, 0.8, 
                                  boxstyle="round,pad=0.15", 
                                  facecolor='#fff3cd', 
                                  edgecolor='#ffc107', 
                                  linewidth=1.5)
ax.add_patch(verif_box)
ax.text(4, 1.9, verif_text, fontsize=14, ha='center', va='center', 
        color='#2c3e50')

# Légende professionnelle
legend_elements = [
    plt.Line2D([0], [0], color='#1f77b4', linewidth=5, label=r'Vecteur $\vec{u}$'),
    plt.Line2D([0], [0], color='#ff7f0e', linewidth=5, label=r'Vecteur $\vec{v}$'),
    plt.Line2D([0], [0], color='#2ca02c', linewidth=4, label=r'Angle $\theta$')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=14, 
          frameon=True, fancybox=True, shadow=True)

# Ajustement final
plt.tight_layout()
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/produit_scalaire_definition.png', 
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.show()

print("Graphique produit_scalaire_definition.png créé avec succès!")
