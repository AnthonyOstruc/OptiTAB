"""
Template pour graphiques avec axes centrés
Style standardisé pour les graphiques mathématiques
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================
# CONFIGURATION DE BASE
# ============================================
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(-20, 20)  # Ajuster selon les besoins
ax.set_ylim(-20, 20)  # Ajuster selon les besoins

# ============================================
# CONFIGURATION DES AXES CENTRÉS
# ============================================
# Désactiver ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches
ax.annotate("", xy=(20, 0), xytext=(-20, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))
ax.annotate("", xy=(0, 20), xytext=(0, -20),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))

# Texte "0" à l'origine
ax.text(-0.8, -1.2, '0', fontsize=12)

# ============================================
# TRACÉ DES COURBES
# ============================================
# Exemple avec labels LaTeX
# ax.plot(x, y, 'b-', linewidth=2, label=r'$f(x) = x^2$')
# ax.plot(x2, y2, 'r-', linewidth=2, label=r'$g(x) = 2x$')

# ============================================
# POINTS PARTICULIERS
# ============================================
# Exemple : point avec couleur différente des courbes
# points_x = [0]
# points_y = [1]
# for i, (px, py) in enumerate(zip(points_x, points_y)):
#     ax.plot(px, py, 'go', markersize=6, label=r'$(0, 1)$')
#     # Pas d'annotation textuelle si déjà dans la légende

# ============================================
# GRADUATIONS MANUELLES
# ============================================
xticks_major = [5, 10, 15, 19]  # Ajuster selon les besoins
yticks_major = [5, 10, 15, 19]  # Ajuster selon les besoins

# Axe X grandes graduations
for x in xticks_major:
    ax.plot([x, x], [-0.3, 0.3], color="black", linewidth=0.8)
    ax.text(x, -1.0, str(x), ha='center', va='top', fontsize=12)

# Axe Y grandes graduations
for y in yticks_major:
    if y < 19:  # Éviter chevauchement avec la flèche
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=0.8)
        ax.text(-1.0, y, str(y), ha='right', va='center', fontsize=12)

# Petites graduations intermédiaires
for x in range(1, 20):
    if x not in xticks_major:
        ax.plot([x, x], [-0.15, 0.15], color="black", linewidth=0.5)

for y in range(1, 20):
    if y not in yticks_major and y < 19:
        ax.plot([-0.1, 0.1], [y, y], color="black", linewidth=0.5)

# ============================================
# LABELS DES AXES
# ============================================
ax.set_xlabel(r'$x$', fontsize=14, labelpad=15)
ax.set_ylabel(r'$y$', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# ============================================
# LÉGENDE
# ============================================
ax.legend(loc='upper right')

# ============================================
# FINALISATION
# ============================================
# Supprimer le titre principal
plt.suptitle('', fontsize=0)

# Ajuster la mise en page
plt.tight_layout()

# Sauvegarder
# plt.savefig('nom_du_fichier.png', dpi=300, bbox_inches='tight')
# plt.show()

