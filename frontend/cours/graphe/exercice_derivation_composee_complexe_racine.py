import numpy as np
import matplotlib.pyplot as plt

# Configuration de la figure
plt.figure(figsize=(16, 10))

# Définition de la fonction
def f(x):
    return np.sqrt(x**2 + 4*x + 3)

# Domaine de définition Df = ]-∞, -3] U [-1, +∞[
x_left = np.linspace(-20, -3, 20000)
x_right = np.linspace(-1, 20, 20000)

# Tracé de la fonction
plt.plot(x_left, f(x_left), 'b-', linewidth=2, label=r'$f(x) = \sqrt{x^2 + 4x + 3}$')
plt.plot(x_right, f(x_right), 'b-', linewidth=2)

# Points importants
plt.plot(-3, 0, 'ro', markersize=8, label='Point (-3, 0)')
plt.plot(-1, 0, 'ro', markersize=8, label='Point (-1, 0)')

# Configuration des axes
plt.xlim(-20, 20)
plt.ylim(-20, 20)

# Suppression des graduations automatiques
ax = plt.gca()
ax.set_xticks([])
ax.set_yticks([])

# Suppression des bordures
for spine in ax.spines.values():
    spine.set_visible(False)

# Ajout des axes avec flèches
ax.annotate("", xy=(20, 0), xytext=(-20, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))
ax.annotate("", xy=(0, 20), xytext=(0, -20),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))

# Texte "0"
ax.text(-0.8, -1.2, '0', fontsize=12)

# --- Graduation manuelle ---
xticks_major = [5, 10, 15, 19]
yticks_major = [5, 10, 15, 19]

# Axe X grandes graduations
for x_val in xticks_major:
    ax.plot([x_val, x_val], [-0.3, 0.3], color="black", linewidth=0.8)
    ax.text(x_val, -1.0, str(x_val), ha='center', va='top', fontsize=12)

# Axe Y grandes graduations
for y in yticks_major:
    if y < 19:
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=0.8)
        ax.text(-1.0, y, str(y), ha='right', va='center', fontsize=12)

# --- Petites graduations intermédiaires (tous les 1) ---
# Axe X
for x_val in range(1, 20):
    if x_val not in xticks_major:
        ax.plot([x_val, x_val], [-0.15, 0.15], color="black", linewidth=0.5)

# Axe Y
for y in range(1, 20):
    if y not in yticks_major and y < 19:
        ax.plot([-0.1, 0.1], [y, y], color="black", linewidth=0.5)

# Labels
plt.xlabel('x', fontsize=14, labelpad=15)
plt.ylabel('f(x)', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(loc='upper right', fontsize=12)

# Sauvegarde
plt.savefig('exercice_derivation_composee_complexe_racine.png', dpi=300, bbox_inches='tight')

# Affichage
plt.show()
