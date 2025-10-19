import matplotlib.pyplot as plt
import numpy as np

# Configuration du style
plt.style.use('default')
plt.rcParams['font.size'] = 12

# Créer la figure
fig, ax = plt.subplots(figsize=(12, 8))

# Fonction
def f(x):
    return np.tan(2*x)

# Domaine [0, π] - éviter les asymptotes en π/4 et 3π/4 (plus proche des asymptotes)
x1 = np.linspace(0, np.pi/4 - 0.01, 1000)
x2 = np.linspace(np.pi/4 + 0.01, 3*np.pi/4 - 0.01, 1000)
x3 = np.linspace(3*np.pi/4 + 0.01, np.pi, 1000)

# Tracer tan(2x) seulement sur [0, π]
plt.plot(x1, f(x1), 'b-', linewidth=1.5, label=r'$f(x) = \tan(2x)$')
plt.plot(x2, f(x2), 'b-', linewidth=1.5)
plt.plot(x3, f(x3), 'b-', linewidth=1.5)

# Tracer y = √3 - en vert
plt.plot([-20, 20], [np.sqrt(3), np.sqrt(3)], color='green', linestyle='--', linewidth=1.5, label=r'$y = \sqrt{3}$')

# Asymptotes verticales x = π/4 et x = 3π/4
plt.axvline(x=np.pi/4, color='red', linestyle='--', linewidth=1.5, label='Asymptotes')
plt.axvline(x=3*np.pi/4, color='red', linestyle='--', linewidth=1.5)

# Points d'intersection
intersections = [np.pi/6, 2*np.pi/3]
for i, x_val in enumerate(intersections):
    if i == 0:
        plt.plot(x_val, f(x_val), 'go', markersize=6, markeredgecolor='darkgreen', markeredgewidth=1, label='Solutions')
    else:
        plt.plot(x_val, f(x_val), 'go', markersize=6, markeredgecolor='darkgreen', markeredgewidth=1)

# Limites
plt.xlim(-10, 10)
plt.ylim(-10, 10)

# Supprimer les ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer les bordures
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches
ax.annotate("", xy=(10, 0), xytext=(-10, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=2))
ax.annotate("", xy=(0, 10), xytext=(0, -10),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=2))

# Texte "0" à l'origine
ax.text(-0.4, -0.6, '0', fontsize=10, ha='right', va='top')

# Label f(x) en haut
ax.text(0, 10.5, 'f(x)', fontsize=12, ha='center', va='bottom')

# Graduations en X (π/4) sur [0, π]
xticks_pi_quarter = [np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
labels = ['π/4', 'π/2', '3π/4', 'π']
for x_val, label in zip(xticks_pi_quarter, labels):
    ax.plot([x_val, x_val], [-0.2, 0.2], color="black", linewidth=0.6)
    ax.text(x_val, -0.7, label, ha='center', va='top', fontsize=7)

# Graduations en Y
yticks_major = [-4, -2, 2, 4]
for y in yticks_major:
    ax.plot([-0.05, 0.05], [y, y], color="black", linewidth=0.6)
    ax.text(-0.25, y, str(y), ha='right', va='center', fontsize=8)

# Pas de titre
# plt.title('Résolution de $\\tan(2x) = \\sqrt{3}$ sur $[0, \\pi]$', fontsize=18, pad=30)

# Légende
plt.legend(loc='upper right', fontsize=12, framealpha=0.9)

# Pas d'annotations des solutions - seulement les points verts

# Ajuster la mise en page
plt.tight_layout()

# Sauvegarder
plt.savefig('applications_trigo_question5.png', dpi=300, bbox_inches='tight')
print("Graphique 'applications_trigo_question5.png' créé avec succès!")

plt.show()