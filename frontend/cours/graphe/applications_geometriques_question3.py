import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonctions
def f1(x):
    return np.sin(x)

def f2(x):
    return np.cos(x)

# Bornes d'intégration
a = 0
b = 2*np.pi
intersection1 = np.pi/4
intersection2 = 5*np.pi/4

# Intervalles
x1 = np.linspace(-20, 4, 1000)

# Courbes
plt.plot(x1, f1(x1), 'b-', linewidth=2, label=r'$y = \sin(x)$')
plt.plot(x1, f2(x1), 'r-', linewidth=2, label=r'$y = \cos(x)$')

# Remplissage de l'aire entre les courbes - Partie 1 (0 à π/4)
x_fill1 = np.linspace(a, intersection1, 50)
y1_fill1 = f1(x_fill1)
y2_fill1 = f2(x_fill1)

# Création du polygone pour la première partie
vertices1 = list(zip(x_fill1, y2_fill1)) + list(zip(x_fill1[::-1], y1_fill1[::-1]))
polygon1 = Polygon(vertices1, facecolor='lightgreen', alpha=0.7, edgecolor='green', linewidth=2)
ax.add_patch(polygon1)

# Remplissage de l'aire entre les courbes - Partie 2 (π/4 à 5π/4)
x_fill2 = np.linspace(intersection1, intersection2, 50)
y1_fill2 = f1(x_fill2)
y2_fill2 = f2(x_fill2)

# Création du polygone pour la deuxième partie
vertices2 = list(zip(x_fill2, y1_fill2)) + list(zip(x_fill2[::-1], y2_fill2[::-1]))
polygon2 = Polygon(vertices2, facecolor='lightgreen', alpha=0.7, edgecolor='green', linewidth=2)
ax.add_patch(polygon2)

# Remplissage de l'aire entre les courbes - Partie 3 (5π/4 à 2π)
x_fill3 = np.linspace(intersection2, b, 50)
y1_fill3 = f1(x_fill3)
y2_fill3 = f2(x_fill3)

# Création du polygone pour la troisième partie
vertices3 = list(zip(x_fill3, y2_fill3)) + list(zip(x_fill3[::-1], y1_fill3[::-1]))
polygon3 = Polygon(vertices3, facecolor='lightgreen', alpha=0.7, edgecolor='green', linewidth=2)
ax.add_patch(polygon3)

# Droites verticales aux bornes
plt.axvline(x=a, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='$x = 0$')
plt.axvline(x=b, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='$x = 2\pi$')
plt.axvline(x=intersection1, color='orange', linestyle=':', linewidth=1.5, alpha=0.7, label='$x = \pi/4$')
plt.axvline(x=intersection2, color='orange', linestyle=':', linewidth=1.5, alpha=0.7, label='$x = 5\pi/4$')

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
aire = 4*np.sqrt(2)
plt.text(0.02, 0.98, f'$A = 4\\sqrt{{2}} \\approx {aire:.3f}$', 
         transform=plt.gca().transAxes, fontsize=14, fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
         verticalalignment='top')

# Sauvegarde
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/applications_geometriques_question3.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'applications_geometriques_question3.png' créé avec succès!")
