import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
ax = plt.gca()

# Configuration
plt.xlim(-1, 5)
plt.ylim(-1, 4)

# Désactiver axes
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Vecteur de référence u
u_x, u_y = 2, 1

# Vecteur v = k1*u (k1 > 0) - parallèle
v_start_x, v_start_y = 0.5, 2.5
v_x, v_y = v_start_x + 2, v_start_y + 1

# Vecteur w = k2*u (k2 < 0) - parallèle
w_start_x, w_start_y = 2, 1
w_x, w_y = w_start_x - 1.5, w_start_y - 0.75

# Tracé de u (bleu)
ax.annotate("", xy=(u_x, u_y), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#1976d2", linewidth=4))
ax.text(1, 0.2, r'$\vec{u}$', fontsize=18, color="#1976d2", fontweight='bold')

# Tracé de v (vert)
ax.annotate("", xy=(v_x, v_y), xytext=(v_start_x, v_start_y),
            arrowprops=dict(arrowstyle="->", color="#388e3c", linewidth=4))
ax.text((v_start_x + v_x)/2 + 0.1, (v_start_y + v_y)/2 + 0.1, r'$\vec{v} = 1.5\vec{u}$', 
        fontsize=16, color="#388e3c", fontweight='bold')

# Tracé de w (rouge)
ax.annotate("", xy=(w_x, w_y), xytext=(w_start_x, w_start_y),
            arrowprops=dict(arrowstyle="->", color="#d32f2f", linewidth=4))
ax.text((w_start_x + w_x)/2 - 0.3, (w_start_y + w_y)/2 - 0.3, r'$\vec{w} = -0.75\vec{u}$', 
        fontsize=16, color="#d32f2f", fontweight='bold')

# Lignes de direction pour montrer le parallélisme
ax.plot([-0.5, 3], [-0.25, 1.5], 'k--', linewidth=2, alpha=0.5)
ax.plot([0, 3.5], [2.25, 3.75], 'k--', linewidth=2, alpha=0.5)
ax.plot([0.5, 2.5], [1, 0.25], 'k--', linewidth=2, alpha=0.5)

# Point origine
ax.plot(0, 0, 'ko', markersize=10)

# Définition principale
ax.text(3.5, 3.5, r"$\vec{u}$ et $\vec{v}$ sont colinéaires", fontsize=18, ha='center', fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#e3f2fd", edgecolor="#1976d2", linewidth=2))

# Condition
ax.text(3.5, 3, r"$\Leftrightarrow \vec{u} = k\vec{v}$ où $k \in \mathbb{R}$", fontsize=16, ha='center',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#666", linewidth=1))

# Signification
ax.text(3.5, 2.5, r"$\Leftrightarrow \vec{u}$ et $\vec{v}$ sont parallèles", fontsize=14, ha='center', style='italic',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff3e0", edgecolor="#ff9800", linewidth=1))

# Exemples
ax.text(3.5, 2, r"Exemples : $\vec{v} = 1.5\vec{u}$ (même sens)", fontsize=13, ha='center', color="#388e3c",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="#e8f5e8", edgecolor="#388e3c", linewidth=1))

ax.text(3.5, 1.5, r"$\vec{w} = -0.75\vec{u}$ (sens opposé)", fontsize=13, ha='center', color="#d32f2f",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="#ffebee", edgecolor="#d32f2f", linewidth=1))

plt.tight_layout()
plt.show()
