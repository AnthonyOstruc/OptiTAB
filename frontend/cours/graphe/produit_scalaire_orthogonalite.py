import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Arc, Rectangle
import matplotlib.patches as patches

# Configuration du graphique
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 12

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Configuration générale
for ax in [ax1, ax2]:
    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 5)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

# === PREMIER GRAPHE : VECTEURS ORTHOGONAUX ===
ax1.set_title('Vecteurs orthogonaux', fontsize=18, weight='bold', color='#2c3e50', pad=20)

# Définition des vecteurs orthogonaux
origin1 = np.array([1, 1])
u1_end = np.array([4, 1])  # Vecteur horizontal
v1_end = np.array([1, 4])  # Vecteur vertical

# Calculs pour les vecteurs orthogonaux
u1_vector = u1_end - origin1
v1_vector = v1_end - origin1
dot_product1 = np.dot(u1_vector, v1_vector)  # = 0 pour vecteurs orthogonaux

# Tracé des vecteurs orthogonaux
arrow_u1 = FancyArrowPatch(origin1, u1_end, 
                          arrowstyle='->', mutation_scale=25, 
                          color='#1f77b4', linewidth=4, alpha=0.8)
arrow_v1 = FancyArrowPatch(origin1, v1_end, 
                          arrowstyle='->', mutation_scale=25, 
                          color='#ff7f0e', linewidth=4, alpha=0.8)

ax1.add_patch(arrow_u1)
ax1.add_patch(arrow_v1)

# Arc d'angle droit
arc_radius = 0.8
arc1 = Arc(origin1, 2*arc_radius, 2*arc_radius, angle=0, theta1=0, theta2=90, 
           color='#2ca02c', linewidth=4, alpha=0.8)
ax1.add_patch(arc1)

# Labels
ax1.text(u1_end[0] + 0.3, u1_end[1], r'$\vec{u}$', fontsize=18, color='#1f77b4', weight='bold')
ax1.text(v1_end[0], v1_end[1] + 0.3, r'$\vec{v}$', fontsize=18, color='#ff7f0e', weight='bold')
ax1.text(origin1[0] + 0.6, origin1[1] + 0.6, r'$90°$', fontsize=16, color='#2ca02c', weight='bold')

# Point d'origine
ax1.plot(origin1[0], origin1[1], 'ko', markersize=8)
ax1.text(origin1[0] - 0.2, origin1[1] - 0.3, 'O', fontsize=14, weight='bold')

# Résultat pour les vecteurs orthogonaux
result1_text = f'$\\vec{{u}} \\cdot \\vec{{v}} = {dot_product1}$'
result1_box = patches.FancyBboxPatch((1.5, 0.2), 2.5, 0.6, 
                                    boxstyle="round,pad=0.1", 
                                    facecolor='#d5f4e6', 
                                    edgecolor='#27ae60', 
                                    linewidth=2)
ax1.add_patch(result1_box)
ax1.text(2.75, 0.5, result1_text, fontsize=14, ha='center', va='center', 
         color='#2c3e50', weight='bold')

# Condition d'orthogonalité
condition1_text = r'$\vec{u} \cdot \vec{v} = 0$'
ax1.text(2.75, 4.5, condition1_text, fontsize=16, ha='center', va='center', 
         bbox=dict(boxstyle="round,pad=0.2", facecolor='#e8f4fd', edgecolor='#3498db'))

# === DEUXIÈME GRAPHE : VECTEURS NON ORTHOGONAUX ===
ax2.set_title('Vecteurs non orthogonaux', fontsize=18, weight='bold', color='#2c3e50', pad=20)

# Définition des vecteurs non orthogonaux
origin2 = np.array([1, 1])
u2_end = np.array([4, 2])
v2_end = np.array([2, 3.5])

# Calculs pour les vecteurs non orthogonaux
u2_vector = u2_end - origin2
v2_vector = v2_end - origin2
dot_product2 = np.dot(u2_vector, v2_vector)

# Calcul de l'angle
norm_u2 = np.linalg.norm(u2_vector)
norm_v2 = np.linalg.norm(v2_vector)
cos_theta = dot_product2 / (norm_u2 * norm_v2)
angle_rad = np.arccos(np.clip(cos_theta, -1, 1))
angle_deg = np.degrees(angle_rad)

# Tracé des vecteurs non orthogonaux
arrow_u2 = FancyArrowPatch(origin2, u2_end, 
                          arrowstyle='->', mutation_scale=25, 
                          color='#1f77b4', linewidth=4, alpha=0.8)
arrow_v2 = FancyArrowPatch(origin2, v2_end, 
                          arrowstyle='->', mutation_scale=25, 
                          color='#ff7f0e', linewidth=4, alpha=0.8)

ax2.add_patch(arrow_u2)
ax2.add_patch(arrow_v2)

# Arc d'angle
arc2 = Arc(origin2, 2*arc_radius, 2*arc_radius, angle=0, theta1=0, theta2=angle_deg, 
           color='#e74c3c', linewidth=4, alpha=0.8)
ax2.add_patch(arc2)

# Labels
ax2.text(u2_end[0] + 0.3, u2_end[1] + 0.1, r'$\vec{u}$', fontsize=18, color='#1f77b4', weight='bold')
ax2.text(v2_end[0] + 0.3, v2_end[1] + 0.1, r'$\vec{v}$', fontsize=18, color='#ff7f0e', weight='bold')

# Label de l'angle
angle_text_x = origin2[0] + arc_radius * np.cos(angle_rad/2)
angle_text_y = origin2[1] + arc_radius * np.sin(angle_rad/2)
ax2.text(angle_text_x, angle_text_y, r'$\theta$', fontsize=16, color='#e74c3c', weight='bold')

# Point d'origine
ax2.plot(origin2[0], origin2[1], 'ko', markersize=8)
ax2.text(origin2[0] - 0.2, origin2[1] - 0.3, 'O', fontsize=14, weight='bold')

# Résultat pour les vecteurs non orthogonaux
result2_text = f'$\\vec{{u}} \\cdot \\vec{{v}} = {dot_product2:.2f} \\neq 0$'
result2_box = patches.FancyBboxPatch((1.5, 0.2), 2.5, 0.6, 
                                    boxstyle="round,pad=0.1", 
                                    facecolor='#f8d7da', 
                                    edgecolor='#dc3545', 
                                    linewidth=2)
ax2.add_patch(result2_box)
ax2.text(2.75, 0.5, result2_text, fontsize=14, ha='center', va='center', 
         color='#2c3e50', weight='bold')

# Condition de non-orthogonalité
condition2_text = r'$\vec{u} \cdot \vec{v} \neq 0$'
ax2.text(2.75, 4.5, condition2_text, fontsize=16, ha='center', va='center', 
         bbox=dict(boxstyle="round,pad=0.2", facecolor='#fdf2f2', edgecolor='#e53e3e'))

# Titre général
fig.suptitle('Orthogonalité et produit scalaire', fontsize=22, weight='bold', color='#2c3e50', y=0.95)

# Légende générale
legend_elements = [
    plt.Line2D([0], [0], color='#1f77b4', linewidth=4, label=r'Vecteur $\vec{u}$'),
    plt.Line2D([0], [0], color='#ff7f0e', linewidth=4, label=r'Vecteur $\vec{v}$'),
    plt.Line2D([0], [0], color='#2ca02c', linewidth=4, label=r'Angle droit $90°$'),
    plt.Line2D([0], [0], color='#e74c3c', linewidth=4, label=r'Angle $\theta \neq 90°$')
]

fig.legend(handles=legend_elements, loc='lower center', fontsize=14, 
           frameon=True, fancybox=True, shadow=True, ncol=4, bbox_to_anchor=(0.5, 0.02))

# Conclusion générale
conclusion_text = r'Deux vecteurs $\vec{u}$ et $\vec{v}$ sont orthogonaux si et seulement si $\vec{u} \cdot \vec{v} = 0$'
fig.text(0.5, 0.08, conclusion_text, fontsize=16, ha='center', va='center', 
         bbox=dict(boxstyle="round,pad=0.3", facecolor='#fff3cd', edgecolor='#ffc107', linewidth=2))

plt.tight_layout()
plt.subplots_adjust(top=0.85, bottom=0.15)
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/produit_scalaire_orthogonalite.png', 
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.show()

print("Graphique produit_scalaire_orthogonalite.png créé avec succès!")
