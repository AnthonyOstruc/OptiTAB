import numpy as np
import matplotlib.pyplot as plt

# Configuration
plt.rcParams['font.size'] = 12
plt.rcParams['mathtext.fontset'] = 'stix'

# Fonction
def f(x):
    return np.log((x**2 + 1) / (x**2 - 4))

# Créer la figure
plt.figure(figsize=(16, 10))

# Domaine de définition (]-∞, -2[ ∪ ]2, +∞[)
x_left = np.linspace(-20, -2 - 1e-10, 20000)
x_right = np.linspace(2 + 1e-10, 20, 20000)

# Tracer la courbe (deux parties)
plt.plot(x_left, f(x_left), 'b-', linewidth=2, label=r'$f(x) = \ln\left(\frac{x^2 + 1}{x^2 - 4}\right)$')
plt.plot(x_right, f(x_right), 'b-', linewidth=2)

# Asymptotes verticales
plt.axvline(x=-2, color='red', linestyle='--', linewidth=1.5, alpha=0.8, label='Asymptote verticale $x=-2$')
plt.axvline(x=2, color='red', linestyle='--', linewidth=1.5, alpha=0.8, label='Asymptote verticale $x=2$')

# Asymptote horizontale
plt.axhline(y=0, color='green', linestyle='--', linewidth=1.5, alpha=0.8, label='Asymptote horizontale $y=0$')

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
plt.savefig('exercice_derivation_composee_complexe.png', dpi=300, bbox_inches='tight')

# Afficher le graphique
plt.show()

print("Graphique 'exercice_derivation_composee_complexe.png' créé avec succès!")
