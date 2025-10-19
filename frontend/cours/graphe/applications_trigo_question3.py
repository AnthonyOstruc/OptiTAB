import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction cos(2x) et ligne y = 1/2
def f(x):
    return np.cos(2*x)

def g(x):
    return 0.5 * np.ones_like(x)

# Domaine de définition - uniquement [0, 2π]
x = np.linspace(0, 2*np.pi, 1500)

# Courbes
plt.plot(x, f(x), 'b-', linewidth=2, label=r'$\cos(2x)$')
plt.plot(x, g(x), 'r--', linewidth=2, label=r'$y = \frac{1}{2}$')

# Zones où cos(2x) >= 1/2 sur [0, 2π]
x_zone1 = np.linspace(0, np.pi/6, 250)
x_zone2 = np.linspace(5*np.pi/6, 7*np.pi/6, 250)
x_zone3 = np.linspace(11*np.pi/6, 2*np.pi, 250)

plt.fill_between(x_zone1, f(x_zone1), g(x_zone1), where=(f(x_zone1) >= g(x_zone1)), 
                 color='green', alpha=0.3, label='$\cos(2x) \geq \\frac{1}{2}$')
plt.fill_between(x_zone2, f(x_zone2), g(x_zone2), where=(f(x_zone2) >= g(x_zone2)), 
                 color='green', alpha=0.3)
plt.fill_between(x_zone3, f(x_zone3), g(x_zone3), where=(f(x_zone3) >= g(x_zone3)), 
                 color='green', alpha=0.3)

# Points d'intersection sur [0, 2π]
intersections = [np.pi/6, 5*np.pi/6, 7*np.pi/6, 11*np.pi/6]
for x_val in intersections:
    plt.plot(x_val, f(x_val), 'go', markersize=6)

# Limites
plt.xlim(-10, 10)
plt.ylim(-10, 10)

# Désactiver ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches
ax.annotate("", xy=(10, 0), xytext=(-10, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))
ax.annotate("", xy=(0, 10), xytext=(0, -10),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))

# Texte "0" 
ax.text(-0.4, -0.6, '0', fontsize=10, ha='right', va='top')

# Label f(x) en haut
ax.text(0, 10.5, 'f(x)', fontsize=12, ha='center', va='bottom')

# Graduations en X (π/2)
xticks_pi_half = [np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
labels = ['π/2', 'π', '3π/2', '2π']
for x_val, label in zip(xticks_pi_half, labels):
    ax.plot([x_val, x_val], [-0.08, 0.08], color="black", linewidth=0.6)
    ax.text(x_val, -0.3, label, ha='center', va='top', fontsize=7)

# Graduations en Y
yticks_major = [-1, 1]
for y in yticks_major:
    ax.plot([-0.05, 0.05], [y, y], color="black", linewidth=0.6)
    ax.text(-0.2, y, str(y), ha='right', va='center', fontsize=8)

# Légende
plt.legend(fontsize=10, loc='upper right')

# Sauvegarde
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/applications_trigo_question3.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'applications_trigo_question3.png' créé avec succès!")
