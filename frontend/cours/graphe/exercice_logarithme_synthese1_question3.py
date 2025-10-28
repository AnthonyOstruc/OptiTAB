import numpy as np
import matplotlib.pyplot as plt

# Configuration
plt.rcParams['font.size'] = 12
plt.rcParams['mathtext.fontset'] = 'stix'

# Fonctions
def f1(x):
    return np.log(1 + x)

def f2(x):
    return x

def g(x):
    return x - np.log(1 + x)

# Créer la figure
plt.figure(figsize=(16, 10))

# Domaine de définition
x = np.linspace(-0.99, 8, 20000)

# Tracer les courbes
plt.plot(x, f1(x), 'b-', linewidth=2, label=r'$f_1(x) = \ln(1+x)$')
plt.plot(x, f2(x), 'g-', linewidth=2, label=r'$f_2(x) = x$')

# Asymptote verticale
plt.axvline(x=-1, color='red', linestyle='--', linewidth=1.5, alpha=0.8, label='Asymptote $x=-1$')

# Point d'intersection (x = 0)
plt.plot(0, 0, 'ro', markersize=8, label='Point d\'intersection (0, 0)')

# Zone où ln(1+x) ≤ x (g(x) ≥ 0)
x_sol = np.linspace(-0.99, 8, 1000)
plt.fill_between(x_sol, f2(x_sol), f1(x_sol), alpha=0.3, color='lightgreen', label='Zone où $\\ln(1+x) \\leq x$')

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
plt.savefig('exercice_logarithme_synthese1_question3.png', dpi=300, bbox_inches='tight')

# Afficher le graphique
plt.show()

print("Graphique 'exercice_logarithme_synthese1_question3.png' créé avec succès!")
