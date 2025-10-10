import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction avec saut fini
def f(x):
    return np.where(x < 1, x, x + 1)

# Intervalles - on évite x = 1 (point de discontinuité)
x1 = np.linspace(-10, 0.99, 1000)  # Avant x = 1
x2 = np.linspace(1.01, 10, 1000)   # Après x = 1

# Courbes
plt.plot(x1, f(x1), 'b-', linewidth=3, label=r'$f(x) = x$ si $x < 1$')
plt.plot(x2, f(x2), 'b-', linewidth=3, label=r'$f(x) = x + 1$ si $x \geq 1$')

# Point de discontinuité en x = 1
# Limite à gauche : f(1-) = 1
# Limite à droite : f(1+) = 2
plt.plot(1, 1, 'ro', markersize=10, markeredgewidth=3, markerfacecolor='white', 
         label='f(1⁻) = 1', zorder=5)
plt.plot(1, 2, 'ro', markersize=10, markeredgewidth=3, markerfacecolor='red', 
         label='f(1⁺) = 2', zorder=5)

# Ligne verticale pour marquer la discontinuité
plt.axvline(x=1, color='red', linestyle='--', linewidth=2, alpha=0.7, 
            label='Discontinuité en x = 1')

# Limites
plt.xlim(-10, 10)
plt.ylim(-5, 8)

# Désactiver ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches
ax.annotate("", xy=(10, 0), xytext=(-10, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))
ax.annotate("", xy=(0, 8), xytext=(0, -5),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))

# Texte "0"
ax.text(-0.8, -0.4, '0', fontsize=12)

# --- Graduation manuelle ---
xticks_major = [-8, -6, -4, -2, 2, 4, 6, 8]
yticks_major = [-4, -2, 2, 4, 6, 8]

# Axe X grandes graduations
for x in xticks_major:
    ax.plot([x, x], [-0.2, 0.2], color="black", linewidth=0.8)
    ax.text(x, -0.4, str(x), ha='center', va='top', fontsize=12)

# Axe Y grandes graduations
for y in yticks_major:
    if y < 7.5:  # évite chevauchement avec la flèche
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=0.8)
        ax.text(-0.6, y, str(y), ha='right', va='center', fontsize=12)

# --- Petites graduations intermédiaires ---
# Axe X (tous les 1)
for x in range(-9, 10):
    if x not in xticks_major and x != 1:
        ax.plot([x, x], [-0.1, 0.1], color="black", linewidth=0.5)

# Axe Y (tous les 1)
for y in range(-4, 9):
    if y not in yticks_major and y < 7.5:
        ax.plot([-0.1, 0.1], [y, y], color="black", linewidth=0.5)

# Labels
plt.xlabel('x', fontsize=14, labelpad=15)
plt.ylabel('f(x)', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(fontsize=11, loc='upper left')

# Annotations pour le saut
ax.annotate('Saut fini = 1', xy=(1, 1.5), xytext=(2, 4),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=12, ha='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#FFE6E6', alpha=0.9))

plt.show()
