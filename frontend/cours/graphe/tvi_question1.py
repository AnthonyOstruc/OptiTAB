import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction f(x) = x³ - 3x + 1
def f(x):
    return x**3 - 3*x + 1

# Domaine de définition
x = np.linspace(-20, 20, 1500)

# Courbe
plt.plot(x, f(x), 'b-', linewidth=2, label=r'$f(x) = x^3 - 3x + 1$')

# Axe y = 0
plt.axhline(y=0, color='green', linestyle='--', linewidth=1.5, alpha=0.7, label='$y = 0$')

# Points clés
plt.plot(0, f(0), 'ro', markersize=6)
ax.annotate('$f(0) = 1$', (0, f(0)), xytext=(-5, 3), fontsize=10,
            arrowprops=dict(arrowstyle='->', color='red', lw=1))

plt.plot(1, f(1), 'ro', markersize=6)
ax.annotate('$f(1) = -1$', (1, f(1)), xytext=(4, -4), fontsize=10,
            arrowprops=dict(arrowstyle='->', color='red', lw=1))

plt.plot(2, f(2), 'ro', markersize=6)
ax.annotate('$f(2) = 3$', (2, f(2)), xytext=(5, 5), fontsize=10,
            arrowprops=dict(arrowstyle='->', color='red', lw=1))

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
plt.legend(fontsize=10, loc='upper left')

# Sauvegarde
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/tvi_question1.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'tvi_question1.png' créé avec succès!")
