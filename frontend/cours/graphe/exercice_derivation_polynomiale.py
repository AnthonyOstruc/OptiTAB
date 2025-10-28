import numpy as np
import matplotlib.pyplot as plt

# Configuration
plt.rcParams['font.size'] = 12
plt.rcParams['mathtext.fontset'] = 'stix'

# Fonctions
def f(x):
    return 2*x**3 - 3*x**2 - 12*x + 5

def f_prime(x):
    return 6*x**2 - 6*x - 12

def tangente(x):
    return np.full_like(x, 12)  # Tangente horizontale en x = -1

# Créer la figure
plt.figure(figsize=(16, 10))

# Domaine de définition
x = np.linspace(-4, 5, 20000)

# Tracer la courbe principale
plt.plot(x, f(x), 'b-', linewidth=2, label=r'$f(x) = 2x^3 - 3x^2 - 12x + 5$')

# Points critiques
x_max = -1
y_max = f(x_max)
x_min = 2
y_min = f(x_min)

# Marquer les extremums
plt.plot(x_max, y_max, 'ro', markersize=8, label=f'Maximum local (-1, {y_max})')
plt.plot(x_min, y_min, 'go', markersize=8, label=f'Minimum local (2, {y_min})')

# Tangente horizontale en x = -1
x_tangente = np.linspace(-3, 1, 1000)
plt.plot(x_tangente, tangente(x_tangente), 'r--', linewidth=2, alpha=0.8, label='Tangente en $x=-1$ : $y=12$')

# Points d'intersection avec les axes
# Zéros de la fonction (approximatifs)
x_zeros = []
for x_test in np.linspace(-3, 4, 1000):
    if abs(f(x_test)) < 0.1:
        x_zeros.append(x_test)

if x_zeros:
    for x_zero in x_zeros[:3]:  # Limiter à 3 zéros
        plt.plot(x_zero, 0, 'ko', markersize=6, alpha=0.7)

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
plt.savefig('exercice_derivation_polynomiale.png', dpi=300, bbox_inches='tight')

# Afficher le graphique
plt.show()

print("Graphique 'exercice_derivation_polynomiale.png' créé avec succès!")
