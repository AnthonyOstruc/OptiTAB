import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction h(x) = e^(x^2 - 2x)
def h(x):
    return np.exp(x**2 - 2*x)

# Domaine de tracé sur ℝ
x = np.linspace(-20, 20, 1000)
y = h(x)

# Tracer la courbe
plt.plot(x, y, 'b-', linewidth=2, label=r'$h(x) = e^{x^2-2x}$')

# Point remarquable : minimum en x = 1
x_min = 1
y_min = h(x_min)  # = 1/e
plt.plot(x_min, y_min, 'ro', markersize=8, label=f'Minimum = 1/e')

# Axe x = 0
plt.axhline(y=0, color='black', linestyle='-', linewidth=1.5)

# Asymptote horizontale y = 0 en ±∞
plt.axhline(y=0, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Asymptote horizontale $y = 0$')

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
for x in xticks_major:
    ax.plot([x, x], [-0.3, 0.3], color="black", linewidth=0.8)
    ax.text(x, -1.0, str(x), ha='center', va='top', fontsize=12)

# Axe Y grandes graduations
for y in yticks_major:
    if y < 19:
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=0.8)
        ax.text(-1.0, y, str(y), ha='right', va='center', fontsize=12)

# --- Petites graduations intermédiaires (tous les 1) ---
# Axe X
for x in range(1, 20):
    if x not in xticks_major:
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
plt.legend(fontsize=10, loc='upper left')

# Sauvegarde
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/etude_exponentielle_question3.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'etude_exponentielle_question3.png' créé avec succès!")

