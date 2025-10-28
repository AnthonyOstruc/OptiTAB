import numpy as np
import matplotlib.pyplot as plt

# Configuration
plt.rcParams['font.size'] = 12
plt.rcParams['mathtext.fontset'] = 'stix'

# Fonctions
def h(x):
    return (x**2 + 3*x) * (2*x - 1)

def k(x):
    return (x**2 + 2) / (x - 3)

# Créer la figure
plt.figure(figsize=(16, 10))

# Domaine pour h(x) (défini sur R) – prolongé sur toute la fenêtre
x_h = np.linspace(-20, 20, 40000)

# (Supprimé) Domaine pour k(x) – on ne trace plus k(x)

# Tracer h(x)
plt.plot(x_h, h(x_h), 'b-', linewidth=2, label=r'$h(x) = (x^2 + 3x)(2x - 1)$')

# (Supprimé) Tracé de k(x) et son asymptote verticale

# Points critiques pour h(x)
# Racines de h'(x) = 6x² + 10x - 3 = 0
# x = (-5 ± √43)/6
sqrt_43 = np.sqrt(43)
x1 = (-5 - sqrt_43) / 6  # ≈ -1.926
x2 = (-5 + sqrt_43) / 6  # ≈ 0.26

y1 = h(x1)
y2 = h(x2)

plt.plot(x1, y1, 'ro', markersize=8, label=f'Maximum local ({x1:.2f}, {y1:.1f})')
plt.plot(x2, y2, 'go', markersize=8, label=f'Minimum local ({x2:.2f}, {y2:.1f})')

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

# Légende
plt.legend(fontsize=10, loc='upper right')

# Sauvegarder
plt.savefig('exercice_derivation_produit_quotient.png', dpi=300, bbox_inches='tight')

# Afficher le graphique
plt.show()

print("Graphique 'exercice_derivation_produit_quotient.png' créé avec succès!")
