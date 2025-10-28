import numpy as np
import matplotlib.pyplot as plt

# Configuration
plt.rcParams['font.size'] = 12
plt.rcParams['mathtext.fontset'] = 'stix'

# Fonctions
def f1(x):
    return np.log(x)

def f2_neg(x):
    return -0.5 * x  # a < 0

def f2_zero(x):
    return 0 * x     # a = 0

def f2_pos(x):
    return (1/np.e) * x  # a = 1/e

def f2_large(x):
    return 2 * x     # a > 1/e

# Créer la figure
plt.figure(figsize=(16, 10))

# Domaine de définition
x = np.linspace(0.00000000001, 8, 20000)

# Tracer la courbe logarithmique
plt.plot(x, f1(x), 'b-', linewidth=2, label=r'$f_1(x) = \ln(x)$')

# Tracer les différentes droites y = ax
plt.plot(x, f2_neg(x), 'g-', linewidth=2, label=r'$y = -0.5x$ (cas $a < 0$)')
plt.plot(x, f2_zero(x), 'orange', linewidth=2, label=r'$y = 0$ (cas $a = 0$)')
plt.plot(x, f2_pos(x), 'red', linewidth=2, label=r'$y = \frac{1}{e}x$ (cas $a = \frac{1}{e}$)')
plt.plot(x, f2_large(x), 'purple', linewidth=2, label=r'$y = 2x$ (cas $a > \frac{1}{e}$)')

# Asymptote verticale
plt.axvline(x=0, color='red', linestyle='--', linewidth=1.5, alpha=0.8, label='Asymptote $x=0$')

# Points d'intersection pour a = 1/e
x_intersect = np.e
y_intersect = f2_pos(x_intersect)
plt.plot(x_intersect, y_intersect, 'ro', markersize=8, label=f'Point de tangence ($e$, 1)')

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

# Sauvegarder
plt.savefig('exercice_logarithme_synthese1_question5.png', dpi=300, bbox_inches='tight')

# Afficher le graphique
plt.show()

print("Graphique 'exercice_logarithme_synthese1_question5.png' créé avec succès!")
