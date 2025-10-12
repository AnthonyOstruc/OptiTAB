import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Configuration
ax.set_xlim(-2, 4)
ax.set_ylim(-1, 3)
ax.set_zlim(-1, 3)

# Désactiver les axes
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# Vecteurs coplanaires - bien séparés
# Vecteur u
u_start = np.array([0, 0, 0])
u_end = np.array([2, 0, 0])
u_vec = u_end - u_start

# Vecteur v
v_start = np.array([0, 0, 0])
v_end = np.array([0, 2, 0])
v_vec = v_end - v_start

# Vecteur w (combinaison linéaire de u et v)
w_start = np.array([0, 0, 0])
w_end = np.array([1.5, 1.5, 0])
w_vec = w_end - w_start

# Tracé des vecteurs
ax.quiver(u_start[0], u_start[1], u_start[2], u_vec[0], u_vec[1], u_vec[2], 
          color='#1976d2', arrow_length_ratio=0.1, linewidth=3)
ax.text(u_end[0]/2 + 0.1, u_end[1]/2 + 0.1, u_end[2], r'$\vec{u}$', fontsize=16, color='#1976d2', fontweight='bold')

ax.quiver(v_start[0], v_start[1], v_start[2], v_vec[0], v_vec[1], v_vec[2], 
          color='#388e3c', arrow_length_ratio=0.1, linewidth=3)
ax.text(v_end[0]/2 + 0.1, v_end[1]/2 + 0.1, v_end[2], r'$\vec{v}$', fontsize=16, color='#388e3c', fontweight='bold')

ax.quiver(w_start[0], w_start[1], w_start[2], w_vec[0], w_vec[1], w_vec[2], 
          color='#d32f2f', arrow_length_ratio=0.1, linewidth=3)
ax.text(w_end[0]/2 + 0.1, w_end[1]/2 + 0.1, w_end[2], r'$\vec{w}$', fontsize=16, color='#d32f2f', fontweight='bold')

# Plan contenant les vecteurs (surface translucide)
xx, yy = np.meshgrid(np.linspace(-1, 3, 10), np.linspace(-0.5, 2.5, 10))
zz = np.zeros_like(xx)
ax.plot_surface(xx, yy, zz, alpha=0.3, color='lightblue', edgecolor='none')

# Vecteur non-coplanaire (pour comparaison)
n_start = np.array([1, 1, 0])
n_end = np.array([1, 1, 2])
n_vec = n_end - n_start

ax.quiver(n_start[0], n_start[1], n_start[2], n_vec[0], n_vec[1], n_vec[2], 
          color='#ff9800', arrow_length_ratio=0.1, linewidth=3, linestyle='--')
ax.text(n_end[0] + 0.1, n_end[1] + 0.1, n_end[2] + 0.1, r'$\vec{n}$ (non-coplanaire)', 
        fontsize=14, color='#ff9800', fontweight='bold')

# Point origine
ax.scatter([0], [0], [0], color='black', s=50)

# Titre et définition
ax.text2D(0.05, 0.95, "Coplanarité", transform=ax.transAxes, fontsize=20, fontweight='bold',
          bbox=dict(boxstyle="round,pad=0.4", facecolor="#e3f2fd", edgecolor="#1976d2", linewidth=2))

ax.text2D(0.05, 0.85, r"$\vec{u}$, $\vec{v}$, $\vec{w}$ sont coplanaires", transform=ax.transAxes, fontsize=16,
          bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#666", linewidth=1))

ax.text2D(0.05, 0.75, r"$\Leftrightarrow \vec{w} = a\vec{u} + b\vec{v}$ où $a,b \in \mathbb{R}$", transform=ax.transAxes, fontsize=14,
          bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff3e0", edgecolor="#ff9800", linewidth=1))

ax.text2D(0.05, 0.65, r"$\Leftrightarrow$ ils appartiennent au même plan", transform=ax.transAxes, fontsize=14, style='italic',
          bbox=dict(boxstyle="round,pad=0.3", facecolor="#e8f5e8", edgecolor="#388e3c", linewidth=1))

# Exemple concret
ax.text2D(0.05, 0.55, r"Exemple : $\vec{w} = 0.75\vec{u} + 0.75\vec{v}$", transform=ax.transAxes, fontsize=13,
          bbox=dict(boxstyle="round,pad=0.2", facecolor="#ffebee", edgecolor="#d32f2f", linewidth=1))

plt.tight_layout()
plt.show()
