import numpy as np
import matplotlib.pyplot as plt

# Configuration
plt.rcParams['font.size'] = 12
plt.rcParams['mathtext.fontset'] = 'stix'

# Fonctions
def f(x):
    return np.log(2*x + 3)

def y_const():
    return 0

# Créer la figure
plt.figure(figsize=(16, 10))

# Domaine de définition
x = np.linspace(-1.5 + 1e-10, 20, 20000)

# Tracer les courbes
plt.plot(x, f(x), 'b-', linewidth=2, label=r'$f(x) = \ln(2x+3)$')
plt.axhline(y=0, color='g', linestyle='-', linewidth=2, label=r'$y = 0$')

# Asymptote verticale
plt.axvline(x=-1.5, color='red', linestyle='--', linewidth=1.5, alpha=0.8, label='Asymptote $x=-\\frac{3}{2}$')

# Point d'intersection
x_intersect = -1
y_intersect = 0
plt.plot(x_intersect, y_intersect, 'ro', markersize=8, label=f'Point d\'intersection (-1, 0)')

# Zone de solution (-3/2 < x ≤ -1)
x_sol = np.linspace(-1.5 + 1e-10, -1, 1000)
plt.fill_between(x_sol, f(x_sol), 0, alpha=0.3, color='lightgreen', label='Solution: $-\\frac{3}{2} < x \\leq -1$')

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
    ax.plot([x, x], [-0.3, 0.3], 'k-', linewidth=1)
    ax.text(x, -0.8, str(x), ha='center', va='top', fontsize=10)

# Graduations majeures Y
for y in yticks_major:
    ax.plot([-0.3, 0.3], [y, y], 'k-', linewidth=0.8)
    ax.text(-0.5, y, str(y), ha='right', va='center', fontsize=10)

# Graduations mineures X
xticks_minor = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18]
for x in xticks_minor:
    ax.plot([x, x], [-0.15, 0.15], 'k-', linewidth=0.5)

# Graduations mineures Y
yticks_minor = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17, 18]
for y in yticks_minor:
    ax.plot([-0.15, 0.15], [y, y], 'k-', linewidth=0.3)

# Légende
plt.legend(fontsize=10, loc='upper right')

# Ajouter un zoom encadré
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
ax_inset = inset_axes(ax, width="25%", height="30%", loc='lower left', borderpad=1.0)
ax_inset.set_facecolor('white')
for spine in ax_inset.spines.values():
    spine.set_edgecolor('#333333')
    spine.set_linewidth(1.0)

# Zone de zoom autour de l'intersection
x_zoom = np.linspace(-1.5 + 1e-10, -1, 1000)
ax_inset.plot(x_zoom, f(x_zoom), 'b-', linewidth=2.5)
ax_inset.axhline(y=0, color='g', linestyle='-', linewidth=2.5)
ax_inset.axvline(x=-1.5, color='red', linestyle='--', linewidth=1.5, alpha=0.8)
ax_inset.plot(-1, 0, 'ro', markersize=6)

# Zone de solution dans le zoom
x_sol_zoom = np.linspace(-1.5 + 1e-10, -1, 500)
ax_inset.fill_between(x_sol_zoom, f(x_sol_zoom), 0, alpha=0.3, color='lightgreen')

# Configuration du zoom
ax_inset.set_xlim(-1.5, -0.5)
ax_inset.set_ylim(-0.8, 0.2)
ax_inset.set_title('Zoom', fontsize=8, pad=5)
ax_inset.tick_params(axis='both', which='both', labelsize=6, length=2, width=0.5)
ax_inset.grid(True, alpha=0.3, linewidth=0.5)

# Sauvegarder
plt.savefig('exercice_logarithme_inequations_question3.png', dpi=300, bbox_inches='tight')

# Afficher le graphique
plt.show()

print("Graphique 'exercice_logarithme_inequations_question3.png' créé avec succès!")
