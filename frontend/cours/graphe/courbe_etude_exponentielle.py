import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction f(x) = (2x - 1)e^x
def f(x):
    return (2*x - 1) * np.exp(x)

# Intervalle pour la fonction
x = np.linspace(-20, 20, 1000)

# Courbe
plt.plot(x, f(x), 'b-', linewidth=2, label=r'$f(x) = (2x - 1)e^x$')

# Asymptote horizontale en y = 0 (limite quand x tend vers -∞)
plt.axhline(y=0, color='green', linestyle='--', linewidth=1.5, alpha=0.7, label='Asymptote y = 0')

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
    if y < 19:  # évite chevauchement avec la flèche
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=0.8)
        ax.text(-1.0, y, str(y), ha='right', va='center', fontsize=12)

# --- Petites graduations intermédiaires (tous les 1) ---
# Axe X
for x in range(1, 20):
    ax.plot([x, x], [-0.15, 0.15], color="black", linewidth=0.5)

# Axe Y
for y in range(1, 20):
    if y not in yticks_major and y < 19:
        ax.plot([-0.1, 0.1], [y, y], color="black", linewidth=0.5)

# Point clé - zéro de la fonction
# f(x) = 0 ⟺ (2x - 1)e^x = 0 ⟺ 2x - 1 = 0 ⟺ x = 1/2
zero_x = 0.5
zero_y = f(zero_x)
ax.plot(zero_x, zero_y, 'ro', markersize=6)
ax.annotate(r'$(\frac{1}{2}, 0)$', (zero_x, zero_y), xytext=(zero_x+0.5, zero_y+1), fontsize=10)

# Point clé - minimum
# f'(x) = 2e^x + (2x-1)e^x = e^x(2 + 2x - 1) = e^x(2x + 1)
# f'(x) = 0 ⟺ 2x + 1 = 0 ⟺ x = -0.5
min_x = -0.5
min_y = f(min_x)
ax.plot(min_x, min_y, 'ro', markersize=6)
ax.annotate(r'$(-\frac{1}{2}, -2e^{-\frac{1}{2}})$', (min_x, min_y), xytext=(min_x+0.5, min_y-1), fontsize=10)

# Labels
plt.xlabel('x', fontsize=14, labelpad=15)
plt.ylabel('f(x)', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(fontsize=10, loc='upper right')

plt.show()
