import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonctions
def f1(x):
    return np.exp(x**2)

def f2(x):
    return np.exp(3*x - 2)

# Domaine de définition
x = np.linspace(-20, 20, 1500)

# Courbes
plt.plot(x, f1(x), 'b-', linewidth=2, label=r'$y = e^{x^2}$')
plt.plot(x, f2(x), 'r-', linewidth=2, label=r'$y = e^{3x-2}$')

# Solutions
plt.plot(1, np.exp(1), 'go', markersize=8, label='Solution $x = 1$')
plt.plot(2, np.exp(4), 'go', markersize=8, label='Solution $x = 2$')

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

# Ajouter un sous-graphique avec zoom sur les solutions
ax_zoom = plt.axes([0.15, 0.15, 0.25, 0.25])  # Position et taille du sous-graphique

# Zone de zoom autour des solutions
x_zoom = np.linspace(0, 3, 200)
ax_zoom.plot(x_zoom, f1(x_zoom), 'b-', linewidth=2, label=r'$e^{x^2}$')
ax_zoom.plot(x_zoom, f2(x_zoom), 'r-', linewidth=2, label=r'$e^{3x-2}$')
ax_zoom.plot(1, np.exp(1), 'go', markersize=6, label='$x = 1$')
ax_zoom.plot(2, np.exp(4), 'go', markersize=6, label='$x = 2$')

# Configuration du zoom
ax_zoom.set_xlim(0, 3)
ax_zoom.set_ylim(0, 20)
ax_zoom.grid(True, alpha=0.3)
ax_zoom.set_title('Zoom sur les solutions', fontsize=8)
ax_zoom.tick_params(labelsize=6)

# Sauvegarde
plt.savefig('exercice_exponentielle_avancees_question2.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'exercice_exponentielle_avancees_question2.png' créé avec succès!")
