import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction f(x) = sin(x)/(1 + sin(x))
def f(x):
    return np.sin(x) / (1 + np.sin(x))

# Domaine de définition (éviter x = 3π/2) - uniquement [0, 2π]
x1 = np.linspace(0, 3*np.pi/2 - 0.05, 750)
x2 = np.linspace(3*np.pi/2 + 0.05, 2*np.pi, 750)

# Courbes
plt.plot(x1, f(x1), 'b-', linewidth=2, label=r'$f(x) = \frac{\sin(x)}{1 + \sin(x)}$')
plt.plot(x2, f(x2), 'b-', linewidth=2)

# Asymptote verticale x = 3π/2
plt.axvline(x=3*np.pi/2, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Asymptote verticale')

# Points clés
plt.plot(0, f(0), 'go', markersize=6)
plt.plot(np.pi/2, f(np.pi/2), 'ro', markersize=6, label='Maximum = 1/2')
plt.plot(2*np.pi, f(2*np.pi), 'go', markersize=6)

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
    ax.plot([x_val, x_val], [-0.2, 0.2], color="black", linewidth=0.6)
    ax.text(x_val, -0.6, label, ha='center', va='top', fontsize=7)

# Graduations en Y
yticks_major = [-4, -2, 2, 4]
for y in yticks_major:
    ax.plot([-0.08, 0.08], [y, y], color="black", linewidth=0.6)
    ax.text(-0.3, y, str(y), ha='right', va='center', fontsize=8)

# Légende
plt.legend(fontsize=10, loc='upper right')

# Sauvegarde
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/applications_trigo_question2.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'applications_trigo_question2.png' créé avec succès!")
