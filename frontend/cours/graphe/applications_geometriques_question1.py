import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction f(x) = x³
def f(x):
    return x**3

# Bornes d'intégration
a = -1
b = 2
zero = 0

# Intervalles
x1 = np.linspace(-20, 4, 1000)

# Courbes
plt.plot(x1, f(x1), 'b-', linewidth=2, label=r'$y = x^3$')
plt.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.7, label='$y = 0$')

# Remplissage de l'aire sous la courbe - Partie 1 (négative)
x_fill1 = np.linspace(a, zero, 50)
y_fill1 = f(x_fill1)

# Création du polygone pour la première partie (négative)
vertices1 = [(a, 0)] + list(zip(x_fill1, y_fill1)) + [(zero, 0)]
polygon1 = Polygon(vertices1, facecolor='lightcoral', alpha=0.7, edgecolor='red', linewidth=2)
ax.add_patch(polygon1)

# Remplissage de l'aire sous la courbe - Partie 2 (positive)
x_fill2 = np.linspace(zero, b, 50)
y_fill2 = f(x_fill2)

# Création du polygone pour la deuxième partie (positive)
vertices2 = [(zero, 0)] + list(zip(x_fill2, y_fill2)) + [(b, 0)]
polygon2 = Polygon(vertices2, facecolor='lightgreen', alpha=0.7, edgecolor='green', linewidth=2)
ax.add_patch(polygon2)

# Droites verticales aux bornes
plt.axvline(x=a, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='$x = -1$')
plt.axvline(x=b, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='$x = 2$')
plt.axvline(x=zero, color='orange', linestyle=':', linewidth=1.5, alpha=0.7, label='$x = 0$')

# Limites
plt.xlim(-20, 20)
plt.ylim(-20, 20)

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

# Texte "0"
ax.text(-0.8, -1.2, '0', fontsize=12)

# Graduation manuelle
xticks_major = [5, 10, 15, 19]
yticks_major = [5, 10, 15, 19]

# Axe X grandes graduations
for x in xticks_major:
    ax.plot([x, x], [-0.3, 0.3], color="black", linewidth=0.8)
    ax.text(x, -1.0, str(x), ha='center', va='top', fontsize=12)

# Axe Y grandes graduations
for y in yticks_major:
    if y < 19:
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=0.8)
        ax.text(-1.0, y, str(y), ha='right', va='center', fontsize=12)

# Petites graduations intermédiaires
for x in range(1, 20):
    if x not in xticks_major:
        ax.plot([x, x], [-0.15, 0.15], color="black", linewidth=0.5)

for y in range(1, 20):
    if y not in yticks_major and y < 19:
        ax.plot([-0.1, 0.1], [y, y], color="black", linewidth=0.5)

# Labels
plt.xlabel('x', fontsize=14, labelpad=15)
plt.ylabel('y', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(fontsize=10, loc='upper right')

# Ajout du calcul de l'aire
aire = 17/4
plt.text(0.02, 0.98, f'$A = \\frac{{17}}{{4}} = {aire}$', 
         transform=plt.gca().transAxes, fontsize=14, fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
         verticalalignment='top')

# Sauvegarde
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/applications_geometriques_question1.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'applications_geometriques_question1.png' créé avec succès!")
