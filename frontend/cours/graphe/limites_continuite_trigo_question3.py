import matplotlib.pyplot as plt
import numpy as np

# Configuration du style
plt.style.use('default')
plt.rcParams['font.size'] = 12

# Créer la figure
fig, ax = plt.subplots(figsize=(12, 8))

# Fonction tan(x)/(x - π/2)
def f(x):
    return np.tan(x) / (x - np.pi/2)

# Domaine - de -π à 2π, éviter les asymptotes de tan(x) et x = π/2
x1 = np.linspace(-np.pi, -np.pi/2 - 0.05, 500)
x2 = np.linspace(-np.pi/2 + 0.05, np.pi/2 - 0.2, 500)
x3 = np.linspace(np.pi/2 + 0.2, 3*np.pi/2 - 0.05, 500)
x4 = np.linspace(3*np.pi/2 + 0.05, 2*np.pi, 500)

# Tracer tan(x)/(x - π/2)
plt.plot(x1, f(x1), 'b-', linewidth=1.5, label=r'$f(x) = \frac{\tan(x)}{x - \frac{\pi}{2}}$')
plt.plot(x2, f(x2), 'b-', linewidth=1.5)
plt.plot(x3, f(x3), 'b-', linewidth=1.5)
plt.plot(x4, f(x4), 'b-', linewidth=1.5)

# Asymptote verticale x = π/2
plt.axvline(x=np.pi/2, color='red', linestyle='--', linewidth=1.5, label=r'Asymptote $x = \frac{\pi}{2}$')

# Autres asymptotes de tan(x) dans la plage
asymptotes = [-np.pi/2, 3*np.pi/2]
for asym in asymptotes:
    plt.axvline(x=asym, color='red', linestyle='--', linewidth=1.5, alpha=0.7)

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
plt.savefig('limites_continuite_trigo_question3.png', dpi=300, bbox_inches='tight')
print("Graphique 'limites_continuite_trigo_question3.png' créé avec succès!")

plt.show()

