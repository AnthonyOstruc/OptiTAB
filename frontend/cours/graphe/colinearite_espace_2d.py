import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 8))
ax = plt.gca()

# Configuration
plt.xlim(-1, 8)
plt.ylim(-2, 5)

# Désactiver axes par défaut
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# ========== PARTIE GAUCHE : Vecteurs colinéaires (même sens) ==========
# Vecteur de base u
u_x, u_y = 2, 1.5

# Vecteur v = 2*u (colinéaire, même sens)
v_x, v_y = 2*u_x, 2*u_y

# Tracé de u (bleu)
ax.annotate("", xy=(u_x, u_y), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#1976d2", linewidth=5))

# Tracé de v (vert)
ax.annotate("", xy=(v_x, v_y), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#388e3c", linewidth=5))
ax.text(v_x/2 - 0.3, v_y/2 + 0.4, r'$\vec{v} = 2\vec{u}$', fontsize=18, color="#388e3c", fontweight='bold', ha='center', va='center')

# Ligne de direction pour montrer le parallélisme
t = np.linspace(-0.3, 1.2, 100)
line_x = t * v_x
line_y = t * v_y
ax.plot(line_x, line_y, 'k--', linewidth=2, alpha=0.4, label='Même direction')

# Point origine gauche
ax.plot(0, 0, 'ko', markersize=12)
ax.text(-0.3, -0.3, 'O', fontsize=14, fontweight='bold')

# Encadré explicatif gauche
ax.text(2, 4.3, r"Même sens", fontsize=16, ha='center', fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#e8f5e8", edgecolor="#388e3c", linewidth=2))
ax.text(2, 3.8, r"$\vec{v} = k\vec{u}$ avec $k > 0$", fontsize=14, ha='center',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#666", linewidth=1))

# ========== PARTIE DROITE : Vecteurs colinéaires (sens opposés) ==========
# Décalage pour la partie droite
offset_x = 5

# Vecteur w = -1.5*u (colinéaire, sens opposé)
w_origin_x, w_origin_y = offset_x + 1, 3.5
w_x, w_y = w_origin_x - 1.5*u_x, w_origin_y - 1.5*u_y

# Tracé de u2 (bleu)
ax.annotate("", xy=(offset_x + u_x, u_y), xytext=(offset_x, 0),
            arrowprops=dict(arrowstyle="->", color="#1976d2", linewidth=5))
ax.text(offset_x + u_x/2 - 0.3, u_y/2 + 0.3, r'$\vec{u}$', fontsize=20, color="#1976d2", fontweight='bold', ha='center', va='center')

# Tracé de w (rouge)
ax.annotate("", xy=(w_x, w_y), xytext=(w_origin_x, w_origin_y),
            arrowprops=dict(arrowstyle="->", color="#d32f2f", linewidth=5))
ax.text((w_origin_x + w_x)/2 + 0.5, (w_origin_y + w_y)/2 - 0.5, r'$\vec{w} = -1.5\vec{u}$', fontsize=18, color="#d32f2f", fontweight='bold', ha='center', va='center')

# Ligne de direction pour montrer le parallélisme (sens opposé)
t2 = np.linspace(-0.5, 1.5, 100)
line2_x = w_origin_x - t2 * u_x
line2_y = w_origin_y - t2 * u_y
ax.plot(line2_x, line2_y, 'k--', linewidth=2, alpha=0.4)

# Points origines droite
ax.plot(offset_x, 0, 'ko', markersize=12)
ax.text(offset_x - 0.3, -0.3, 'O', fontsize=14, fontweight='bold')
ax.plot(w_origin_x, w_origin_y, 'ko', markersize=12)
ax.text(w_origin_x - 0.3, w_origin_y + 0.3, 'A', fontsize=14, fontweight='bold')

# Encadré explicatif droite
ax.text(w_origin_x, 4.6, r"Sens opposés", fontsize=16, ha='center', fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#ffebee", edgecolor="#d32f2f", linewidth=2))
ax.text(w_origin_x, 4.1, r"$\vec{w} = k\vec{u}$ avec $k < 0$", fontsize=14, ha='center',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#666", linewidth=1))

# ========== DÉFINITION PRINCIPALE EN BAS ==========
# Titre principal
plt.text(3.8, -1.2, r"Colinéarité de vecteurs", fontsize=22, ha='center', fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#e3f2fd", edgecolor="#1976d2", linewidth=3))

# Définition
definition_text = r"$\vec{u}$ et $\vec{v}$ sont colinéaires $\Leftrightarrow \exists k \in \mathbb{R}$ tel que $\vec{u} = k\vec{v}$"
plt.text(3.8, -1.7, definition_text, fontsize=15, ha='center',
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff3e0", edgecolor="#ff9800", linewidth=2))

plt.tight_layout()
plt.savefig('colinearite_espace_2d.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("✅ Graphe de colinéarité 2D généré : colinearite_espace_2d.png")

