import numpy as np
import matplotlib.pyplot as plt

# Configuration
plt.rcParams['font.size'] = 12
plt.rcParams['mathtext.fontset'] = 'stix'

# Fonctions
def f1(x):
    return np.log(x + 1)

def f2(x):
    return np.log(2*x)

# Créer la figure
plt.figure(figsize=(16, 10))

# Domaine de définition
x1 = np.linspace(-1 + 1e-10, 0 - 1e-10, 20000)  # Partie gauche de f1
x2 = np.linspace(0 + 1e-10, 20, 20000)  # Partie droite commune

# Tracer les courbes
plt.plot(x1, f1(x1), 'b-', linewidth=2, label=r'$f_1(x) = \ln(x+1)$')
plt.plot(x2, f1(x2), 'b-', linewidth=2)
plt.plot(x2, f2(x2), 'g-', linewidth=2, label=r'$f_2(x) = \ln(2x)$')

# Asymptotes verticales
plt.axvline(x=-1, color='red', linestyle='--', linewidth=1.5, alpha=0.8, label='Asymptote $x=-1$')
plt.axvline(x=0, color='orange', linestyle='--', linewidth=1.5, alpha=0.8, label='Asymptote $x=0$')

# Point d'intersection
x_intersect = 1
y_intersect = f1(x_intersect)
plt.plot(x_intersect, y_intersect, 'ro', markersize=8, label=f'Point d\'intersection (1, {y_intersect:.2f})')

# Zone de solution (x > 1)
x_sol = np.linspace(1.01, 20, 1000)
plt.fill_between(x_sol, f1(x_sol), f2(x_sol), alpha=0.3, color='lightgreen', label='Solution: $x > 1$')

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
plt.savefig('exercice_logarithme_inequations_question1.png', dpi=300, bbox_inches='tight')

# Afficher le graphique
plt.show()

print("Graphique 'exercice_logarithme_inequations_question1.png' créé avec succès!")
