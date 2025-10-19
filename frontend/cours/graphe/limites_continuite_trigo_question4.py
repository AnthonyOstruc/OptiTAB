import matplotlib.pyplot as plt
import numpy as np

# Configuration du style
plt.style.use('default')
plt.rcParams['font.size'] = 12

# Créer la figure
fig, ax = plt.subplots(figsize=(12, 8))

# Fonction sin(x)/x
def f(x):
    return np.sin(x) / x

# Domaine - éviter x = 0
x1 = np.linspace(-20, -0.01, 1000)
x2 = np.linspace(0.01, 20, 1000)

# Tracer sin(x)/x
plt.plot(x1, f(x1), 'b-', linewidth=1.5, label=r'$f(x) = \frac{\sin(x)}{x}$ pour $x \neq 0$')
plt.plot(x2, f(x2), 'b-', linewidth=1.5)

# Trou en x = 0 (fonction non définie)
plt.plot(0, 1, 'ro', markersize=8, markerfacecolor='white', markeredgecolor='red', markeredgewidth=2, label='Trou en $x = 0$', zorder=5)

# Prolongement par continuité en (0, 1)
plt.plot(0, 1, 'go', markersize=8, markeredgecolor='darkgreen', markeredgewidth=2, label=r'Prolongement: $\tilde{f}(0) = 1$', zorder=6)

# Ligne horizontale y = 1 pour visualiser la limite
plt.axhline(y=1, color='green', linestyle='--', linewidth=1, alpha=0.5)

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

# Texte "0" à l'origine
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

# Graduation spéciale pour y = 1
ax.plot([-0.3, 0.3], [1, 1], color="green", linewidth=0.8)
ax.text(-1.0, 1.5, '1', ha='right', va='center', fontsize=10, color='green')

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
plt.savefig('limites_continuite_trigo_question4.png', dpi=300, bbox_inches='tight')
print("Graphique 'limites_continuite_trigo_question4.png' créé avec succès!")

plt.show()

