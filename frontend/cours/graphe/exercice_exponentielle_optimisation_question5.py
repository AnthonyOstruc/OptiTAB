import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction
def k(x):
    return x**2 * np.exp(-x)

# Domaine de définition [0, +∞[
x = np.linspace(0, 20, 1500)

# Courbe principale
plt.plot(x, k(x), 'b-', linewidth=2, label=r'$k(x) = x^2e^{-x}$')

# Point maximum en x = 2
x_max = 2
y_max = k(x_max)
plt.plot(x_max, y_max, 'ro', markersize=8, label=f'Maximum en $x = 2$ : $k(2) = \\frac{{4}}{{e^2}}$')

# Asymptote horizontale y = 0 (limite en +∞)
plt.axhline(y=0, color='red', linestyle='--', linewidth=2, label='Asymptote $y = 0$ en $+\\infty$')

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
plt.ylabel('k(x)', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(fontsize=10, loc='upper right')

# Ajouter un sous-graphique avec zoom sur le maximum
ax_zoom = plt.axes([0.15, 0.15, 0.25, 0.25])  # Position et taille du sous-graphique

# Zone de zoom autour de x = 2
x_zoom = np.linspace(0, 4, 200)
ax_zoom.plot(x_zoom, k(x_zoom), 'b-', linewidth=2, label=r'$k(x) = x^2e^{-x}$')
ax_zoom.plot(2, k(2), 'ro', markersize=6, label='Maximum')

# Configuration du zoom
ax_zoom.set_xlim(0, 4)
ax_zoom.set_ylim(0, 1)
ax_zoom.grid(True, alpha=0.3)
ax_zoom.set_title('Zoom sur le maximum', fontsize=8)
ax_zoom.tick_params(labelsize=6)

# Sauvegarde
plt.savefig('exercice_exponentielle_optimisation_question5.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'exercice_exponentielle_optimisation_question5.png' créé avec succès!")
