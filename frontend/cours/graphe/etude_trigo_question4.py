import matplotlib.pyplot as plt
import numpy as np

# Configuration du style
plt.style.use('default')
plt.rcParams['font.size'] = 12

# Créer la figure
fig, ax = plt.subplots(figsize=(12, 8))

# Fonction
def f(x):
    return np.sin(x) * np.cos(x)

# Domaine [0, 2π] seulement
x = np.linspace(0, 2*np.pi, 1500)

# Tracer sin(x)cos(x) sur [0, 2π]
plt.plot(x, f(x), 'b-', linewidth=1.5, label=r'$k(x) = \sin(x)\cos(x)$')

# Points d'extremums
max_x1 = np.pi/4
max_x2 = 5*np.pi/4
min_x1 = 3*np.pi/4
min_x2 = 7*np.pi/4

plt.plot(max_x1, f(max_x1), 'go', markersize=6, markeredgecolor='darkgreen', markeredgewidth=1, label='Max en $\\frac{\\pi}{4}, \\frac{5\\pi}{4}$')
plt.plot(max_x2, f(max_x2), 'go', markersize=6, markeredgecolor='darkgreen', markeredgewidth=1)
plt.plot(min_x1, f(min_x1), 'ro', markersize=6, markeredgecolor='darkred', markeredgewidth=1, label='Min en $\\frac{3\\pi}{4}, \\frac{7\\pi}{4}$')
plt.plot(min_x2, f(min_x2), 'ro', markersize=6, markeredgecolor='darkred', markeredgewidth=1)

# Limites
plt.xlim(-20, 20)
plt.ylim(-20, 20)

# Supprimer les ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer les bordures
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches
ax.annotate("", xy=(20, 0), xytext=(-20, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=2))
ax.annotate("", xy=(0, 20), xytext=(0, -20),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=2))

# Texte "0" à l'origine - déplacé à droite et ajusté verticalement
ax.text(-0.3, -0.8, '0', fontsize=10, ha='center', va='top')

# Graduations en X (multiples de π)
xticks_pi = [
    (-2*np.pi, '$-2\\pi$'),
    (-np.pi, '$-\\pi$'),
    (np.pi, '$\\pi$'),
    (2*np.pi, '$2\\pi$')
]

for x_val, label in xticks_pi:
    ax.plot([x_val, x_val], [-0.3, 0.3], color="black", linewidth=0.8)
    ax.text(x_val, -1.0, label, ha='center', va='top', fontsize=10)

# Petites graduations en X (π/2) - sans texte
xticks_pi_half = [-3*np.pi/2, -np.pi/2, np.pi/2, 3*np.pi/2]
for x_val in xticks_pi_half:
    ax.plot([x_val, x_val], [-0.15, 0.15], color="black", linewidth=0.5)

# Graduations en Y
yticks_major = [-15, -10, -5, 5, 10, 15]
for y in yticks_major:
    ax.plot([-0.3, 0.3], [y, y], color="black", linewidth=0.8)
    ax.text(-1.0, y, str(y), ha='right', va='center', fontsize=10)

# Labels des axes
plt.xlabel('x', fontsize=16, labelpad=20)
plt.ylabel('f(x)', fontsize=16, labelpad=20, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(loc='upper right', fontsize=12, framealpha=0.9)

# Ajuster la mise en page
plt.tight_layout()

# Sauvegarder
plt.savefig('etude_trigo_question4.png', dpi=300, bbox_inches='tight')
print("Graphique 'etude_trigo_question4.png' créé avec succès!")

plt.show()