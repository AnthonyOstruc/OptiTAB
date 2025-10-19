import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction f(x) = e^x
def f(x):
    return np.exp(x)

# Bornes d'intégration
a = 0
b = 1

# Intervalles - même template que fonction_1_sur_x_moins_3.py
x1 = np.linspace(-20, 4, 1000)  # Même intervalle que le template

# Courbes
plt.plot(x1, f(x1), 'b-', linewidth=2, label=r'$f(x) = e^x$')

# Remplissage de l'aire sous la courbe
x_fill = np.linspace(a, b, 100)
y_fill = np.exp(x_fill)

# Création du polygone pour l'aire
vertices = [(a, 0)] + list(zip(x_fill, y_fill)) + [(b, 0)]
polygon = Polygon(vertices, facecolor='lightgreen', alpha=0.7, edgecolor='green', linewidth=2)
ax.add_patch(polygon)

# Droites verticales aux bornes
plt.axvline(x=a, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='$x = 0$')
plt.axvline(x=b, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='$x = 1$')

# Limites - EXACTEMENT comme le template
plt.xlim(-20, 20)
plt.ylim(-20, 20)

# Désactiver ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches - EXACTEMENT comme le template
ax.annotate("", xy=(20, 0), xytext=(-20, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))
ax.annotate("", xy=(0, 20), xytext=(0, -20),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))

# Texte "0" - EXACTEMENT comme le template
ax.text(-0.8, -1.2, '0', fontsize=12)

# --- Graduation manuelle - EXACTEMENT comme le template ---
xticks_major = [5, 10, 15, 19]
yticks_major = [5, 10, 15, 19]

# Axe X grandes graduations
for x in xticks_major:
    ax.plot([x, x], [-0.3, 0.3], color="black", linewidth=0.8)
    ax.text(x, -1.0, str(x), ha='center', va='top', fontsize=12)

# Axe Y grandes graduations
for y in yticks_major:
    if y < 19:  # évite chevauchement avec la flèche
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=0.8)
        ax.text(-1.0, y, str(y), ha='right', va='center', fontsize=12)

# --- Petites graduations intermédiaires (tous les 1) ---
# Axe X
for x in range(1, 20):
    if x not in xticks_major:  # Pas d'exception pour x=3 ici
        ax.plot([x, x], [-0.15, 0.15], color="black", linewidth=0.5)

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
plt.legend(fontsize=10, loc='upper right')

# Ajout du calcul de l'aire dans la légende
# Calcul de l'intégrale : ∫₀¹ e^x dx = [e^x]₀¹
# En x=1: e^1 = e
# En x=0: e^0 = 1
# Aire = e - 1 ≈ 1.718
aire = np.e - 1  # ≈ 1.718
plt.text(0.02, 0.98, f'$A = e - 1 \\approx {aire:.3f}$', 
         transform=plt.gca().transAxes, fontsize=14, fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
         verticalalignment='top')

# Sauvegarde
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/aire_sous_la_courbe.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'aire_sous_la_courbe.png' créé avec succès!")
