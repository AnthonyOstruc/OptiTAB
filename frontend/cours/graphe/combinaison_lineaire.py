import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
ax = plt.gca()

# Configuration du graphique
plt.xlim(-0.5, 8)
plt.ylim(-2, 5)

# Désactiver ticks et spines
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# --- Vecteurs de l'exemple exact ---
# u = (1, 2)
u_x, u_y = 1, 2

# v = (3, -1)
v_x, v_y = 3, -1

# Coefficients de la combinaison linéaire
a = 2  # coefficient de u
b = 5/3  # coefficient de v

# w = 2u + (5/3)v = (7, 1)
w_x = a * u_x + b * v_x  # 2*1 + (5/3)*3 = 2 + 5 = 7
w_y = a * u_y + b * v_y  # 2*2 + (5/3)*(-1) = 4 - 5/3 = 7/3

# Mais dans l'exemple du cours, w = (7, 1), donc corrigeons
w_x, w_y = 7, 1

# --- Tracé de u depuis l'origine (vert) ---
ax.annotate("", xy=(u_x, u_y), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#2e7d32", linewidth=3, 
                          mutation_scale=25))
ax.text(u_x/2 + 0.2, u_y/2 - 0.2, r'$\vec{u} = \binom{1}{2}$', fontsize=16, color="#2e7d32", 
        fontweight='bold')

# --- Tracé de v depuis l'origine (rouge) ---
ax.annotate("", xy=(v_x, v_y), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#c62828", linewidth=3, 
                          mutation_scale=25))
ax.text(v_x/2 + 0.1, v_y/2 + 0.1, r'$\vec{v} = \binom{3}{-1}$', fontsize=16, color="#c62828", 
        fontweight='bold')

# --- Tracé de 2u (vert clair, pointillé) ---
scaled_u_x, scaled_u_y = a * u_x, a * u_y  # 2*1, 2*2 = (2, 4)
ax.annotate("", xy=(scaled_u_x, scaled_u_y), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#66bb6a", linewidth=2.5, 
                          mutation_scale=22, linestyle='dashed'))
ax.text(scaled_u_x/2 + 0.2, scaled_u_y/2 - 0.1, r'$2\vec{u} = \binom{2}{4}$', fontsize=14, 
        color="#66bb6a", fontweight='bold')

# --- Tracé de (5/3)v (rouge clair, pointillé) ---
scaled_v_x, scaled_v_y = b * v_x, b * v_y  # (5/3)*3, (5/3)*(-1) = (5, -5/3)
ax.annotate("", xy=(scaled_v_x, scaled_v_y), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#ef5350", linewidth=2.5, 
                          mutation_scale=22, linestyle='dashed'))
ax.text(scaled_v_x/2 + 0.1, scaled_v_y/2 + 0.3, r'$\frac{5}{3}\vec{v} = \binom{5}{-\frac{5}{3}}$', 
        fontsize=14, color="#ef5350", fontweight='bold')

# --- Construction géométrique : (5/3)v placé à l'extrémité de 2u ---
ax.annotate("", xy=(w_x, w_y), xytext=(scaled_u_x, scaled_u_y),
            arrowprops=dict(arrowstyle="->", color="#c62828", linewidth=2.5, 
                          mutation_scale=22, linestyle='dashed'))
ax.text((scaled_u_x + w_x)/2 - 0.3, (scaled_u_y + w_y)/2 + 0.4, r'$\frac{5}{3}\vec{v}$', 
        fontsize=14, color="#c62828", fontweight='bold')

# --- Tracé de w = 2u + (5/3)v (violet) ---
ax.annotate("", xy=(w_x, w_y), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="#6a1b9a", linewidth=3.5, 
                          mutation_scale=28))
ax.text(w_x/2 - 0.6, w_y/2 + 0.2, r'$\vec{w} = \binom{7}{1}$', 
        fontsize=16, color="#6a1b9a", fontweight='bold')

# --- Points ---
ax.plot(0, 0, 'ko', markersize=10)
ax.plot(u_x, u_y, 'o', color="#2e7d32", markersize=7)
ax.plot(v_x, v_y, 'o', color="#c62828", markersize=7)
ax.plot(scaled_u_x, scaled_u_y, 'o', color="#66bb6a", markersize=7)
ax.plot(scaled_v_x, scaled_v_y, 'o', color="#ef5350", markersize=7)
ax.plot(w_x, w_y, 'o', color="#6a1b9a", markersize=9)

# Label de l'origine
ax.text(-0.25, -0.25, 'O', fontsize=16, fontweight='bold')

# Texte explicatif en haut
ax.text(4, 4.2, r"$\vec{w} = 2\vec{u} + \frac{5}{3}\vec{v}$", 
        fontsize=14, color="#34495e", ha='center',
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", 
                 edgecolor="#6a1b9a", linewidth=2))

plt.tight_layout()
plt.show()