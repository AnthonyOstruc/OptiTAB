import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonctions sin(3x) et sin(x)
def f1(x):
    return np.sin(3*x)

def f2(x):
    return np.sin(x)

# Domaine de définition - uniquement [0, 2π]
x = np.linspace(0, 2*np.pi, 1500)

# Courbes
plt.plot(x, f1(x), 'b-', linewidth=2, label=r'$\sin(3x)$')
plt.plot(x, f2(x), 'r-', linewidth=2, label=r'$\sin(x)$')

# Points d'intersection sur [0, 2π] - solutions correctes de sin(3x) = sin(x)
# sin(3x) = sin(x) ⟺ 3x = x + 2kπ ou 3x = π - x + 2kπ
# ⟺ 2x = 2kπ ou 4x = π + 2kπ
# ⟺ x = kπ ou x = π/4 + kπ/2
# Solutions sur [0, 2π] : 0, π/4, 3π/4, π, 5π/4, 7π/4, 2π
intersections = [0, np.pi/4, 3*np.pi/4, np.pi, 5*np.pi/4, 7*np.pi/4, 2*np.pi]
for i, x_val in enumerate(intersections):
    if i == 0:
        plt.plot(x_val, f1(x_val), 'go', markersize=6, label='Solutions')
    else:
        plt.plot(x_val, f1(x_val), 'go', markersize=6)

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
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/applications_trigo_question1.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'applications_trigo_question1.png' créé avec succès!")
