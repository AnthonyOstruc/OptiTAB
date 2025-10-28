import numpy as np
import matplotlib.pyplot as plt

# Configuration
plt.rcParams['font.size'] = 12
plt.rcParams['mathtext.fontset'] = 'stix'

# Fonctions
def g(x):
    return np.exp(-x**2 + 2*x - 1)

def g_prime(x):
    return (-2*x + 2) * np.exp(-x**2 + 2*x - 1)

def g_double_prime(x):
    return np.exp(-x**2 + 2*x - 1) * (4*x**2 - 8*x + 2)

# Créer la figure
plt.figure(figsize=(16, 10))

# Domaine de définition
x = np.linspace(-2, 4, 20000)

# Tracer la courbe principale
plt.plot(x, g(x), 'b-', linewidth=2, label=r'$g(x) = e^{-x^2 + 2x - 1}$')

# Point critique (maximum)
x_max = 1
y_max = g(x_max)
plt.plot(x_max, y_max, 'ro', markersize=8, label=f'Maximum local (1, {y_max:.0f})')

# Points d'inflexion
x1 = (2 - np.sqrt(2)) / 2  # ≈ 0.293
x2 = (2 + np.sqrt(2)) / 2  # ≈ 1.707
y1 = g(x1)
y2 = g(x2)

plt.plot(x1, y1, 'go', markersize=8, label=f'Point d\'inflexion 1 ({x1:.2f}, {y1:.2f})')
plt.plot(x2, y2, 'go', markersize=8, label=f'Point d\'inflexion 2 ({x2:.2f}, {y2:.2f})')

# Zones de convexité/concavité
x_convexe1 = np.linspace(-2, x1, 1000)
x_concave = np.linspace(x1, x2, 1000)
x_convexe2 = np.linspace(x2, 4, 1000)

# Tracer les zones avec des couleurs différentes
plt.fill_between(x_convexe1, g(x_convexe1), alpha=0.1, color='green', label='Zone convexe 1')
plt.fill_between(x_concave, g(x_concave), alpha=0.1, color='red', label='Zone concave')
plt.fill_between(x_convexe2, g(x_convexe2), alpha=0.1, color='green', label='Zone convexe 2')

# Configuration des axes
ax = plt.gca()
plt.xlim(-20, 20)
plt.ylim(-20, 20)
ax.set_xticks([])
ax.set_yticks([])

# Supprimer les bordures
for spine in ax.spines.values():
    spine.set_visible(False)

# Dessiner les axes avec des flèches
ax.annotate("", xy=(20, 0), xytext=(-20, 0), arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))
ax.annotate("", xy=(0, 20), xytext=(0, -20), arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))

# Origine
ax.text(-0.8, -1.2, '0', fontsize=12)

# Graduations manuelles
xticks_major = [5, 10, 15, 19]
yticks_major = [5, 10, 15, 19]

# Graduations majeures X
for x in xticks_major:
    ax.plot([x, x], [-0.2, 0.2], 'k-', linewidth=0.6)
    ax.text(x, -0.6, str(x), ha='center', va='top', fontsize=9)

# Graduations majeures Y
for y in yticks_major:
    ax.plot([-0.2, 0.2], [y, y], 'k-', linewidth=0.4)
    ax.text(-0.4, y, str(y), ha='right', va='center', fontsize=9)

# Graduations mineures X
xticks_minor = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18]
for x in xticks_minor:
    ax.plot([x, x], [-0.1, 0.1], 'k-', linewidth=0.3)

# Graduations mineures Y
yticks_minor = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18]
for y in yticks_minor:
    ax.plot([-0.1, 0.1], [y, y], 'k-', linewidth=0.2)

# Légende (avant le zoom)
plt.legend(fontsize=10, loc='upper right')

# Zoom sur la partie convexe/concave
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
ax_inset = inset_axes(ax, width="25%", height="30%", loc='lower right', borderpad=1.0)
ax_inset.set_facecolor('white')

# Configuration du zoom
x_zoom = np.linspace(-0.5, 2.5, 2000)
ax_inset.plot(x_zoom, g(x_zoom), 'b-', linewidth=2.5, label='_nolegend_')

# Points dans le zoom
ax_inset.plot(x_max, y_max, 'ro', markersize=6, label='_nolegend_')
ax_inset.plot(x1, y1, 'go', markersize=6, label='_nolegend_')
ax_inset.plot(x2, y2, 'go', markersize=6, label='_nolegend_')

# Zones de convexité/concavité dans le zoom
x_convexe1_zoom = np.linspace(-0.5, x1, 500)
x_concave_zoom = np.linspace(x1, x2, 500)
x_convexe2_zoom = np.linspace(x2, 2.5, 500)

ax_inset.fill_between(x_convexe1_zoom, g(x_convexe1_zoom), alpha=0.2, color='green', label='_nolegend_')
ax_inset.fill_between(x_concave_zoom, g(x_concave_zoom), alpha=0.2, color='red', label='_nolegend_')
ax_inset.fill_between(x_convexe2_zoom, g(x_convexe2_zoom), alpha=0.2, color='green', label='_nolegend_')

# Configuration du zoom
ax_inset.set_xlim(-0.5, 2.5)
ax_inset.set_ylim(0, 1.2)
ax_inset.set_title('Zoom convexité', fontsize=8, pad=5)
ax_inset.tick_params(axis='both', which='both', labelsize=6, length=2, width=0.5)
ax_inset.grid(True, alpha=0.3, linewidth=0.5)

# Sauvegarder
plt.savefig('exercice_derivation_composee.png', dpi=300, bbox_inches='tight')

# Afficher le graphique
plt.show()

print("Graphique 'exercice_derivation_composee.png' créé avec succès!")
