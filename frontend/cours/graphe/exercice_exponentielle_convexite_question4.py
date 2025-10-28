import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction
def f(x: np.ndarray) -> np.ndarray:
    return np.exp(-x**2)

# Domaine de définition
x = np.linspace(-20, 20, 1500)

# Courbe principale
plt.plot(x, f(x), 'b-', linewidth=2, label=r'$f(x) = e^{-x^2}$')

# Points d'inflexion pour guider convexité/concavité
a = np.sqrt(2) / 2
plt.plot([-a, a], [f(-a), f(a)], 'go', markersize=6, label=r"Points d'inflexion $x=\pm\frac{\sqrt{2}}{2}$")

# Bandes de convexité/concavité (indicatives)
x_left = x[x <= -a]
x_mid = x[(x >= -a) & (x <= a)]
x_right = x[x >= a]
ax.fill_between(x_left, f(x_left), -20, color='green', alpha=0.05, label='Convexe')
ax.fill_between(x_mid, f(x_mid), -20, color='red', alpha=0.05, label='Concave')
ax.fill_between(x_right, f(x_right), -20, color='green', alpha=0.05)

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
plt.legend(fontsize=10, loc='upper right')

# Ajouter un sous-graphique avec zoom sur la zone de convexité/concavité
ax_zoom = plt.axes([0.15, 0.15, 0.25, 0.25])  # Position et taille du sous-graphique

# Zone de zoom autour des points d'inflexion
x_zoom = np.linspace(-2, 2, 200)
ax_zoom.plot(x_zoom, f(x_zoom), 'b-', linewidth=2, label=r'$f(x)$')
ax_zoom.plot([-a, a], [f(-a), f(a)], 'go', markersize=6, label=r"Points d'inflexion")

# Bandes de convexité/concavité dans le zoom
x_left_zoom = x_zoom[x_zoom <= -a]
x_mid_zoom = x_zoom[(x_zoom >= -a) & (x_zoom <= a)]
x_right_zoom = x_zoom[x_zoom >= a]
ax_zoom.fill_between(x_left_zoom, f(x_left_zoom), 0, color='green', alpha=0.1, label='Convexe')
ax_zoom.fill_between(x_mid_zoom, f(x_mid_zoom), 0, color='red', alpha=0.1, label='Concave')
ax_zoom.fill_between(x_right_zoom, f(x_right_zoom), 0, color='green', alpha=0.1)

# Configuration du zoom
ax_zoom.set_xlim(-2, 2)
ax_zoom.set_ylim(0, 1.2)
ax_zoom.grid(True, alpha=0.3)
ax_zoom.set_title('Zoom sur convexité/concavité', fontsize=8)
ax_zoom.tick_params(labelsize=6)

# Sauvegarde
plt.savefig('exercice_exponentielle_convexite_question4.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'exercice_exponentielle_convexite_question4.png' créé avec succès!")


