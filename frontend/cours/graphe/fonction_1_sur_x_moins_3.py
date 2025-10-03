import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction rationnelle f(x) = 1/(x-3)
def f(x):
    return 1 / (x - 3)

# Intervalles (en évitant x = 3)
x1 = np.linspace(-20, 2.99, 1000)  # Branche gauche - plus proche de 3
x2 = np.linspace(3.01, 20, 1000)   # Branche droite - plus proche de 3

# Courbes
plt.plot(x1, f(x1), 'r-', linewidth=2, label=r'$f(x) = \frac{1}{x-3}$')
plt.plot(x2, f(x2), 'r-', linewidth=2)

# Asymptote verticale x = 3
plt.axvline(x=3, color='black', linestyle='--', linewidth=2, alpha=0.7, label='Asymptote verticale x = 3')

# Asymptote horizontale y = 0 (axe des x)
plt.axhline(y=0, color='black', linestyle='--', linewidth=2, alpha=0.7, label='Asymptote horizontale y = 0')

# Limites
plt.xlim(-20, 20)
plt.ylim(-30, 30)

# Désactiver ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches
ax.annotate("", xy=(20, 0), xytext=(-20, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))
ax.annotate("", xy=(0, 30), xytext=(0, -30),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))

# Texte "0"
ax.text(-0.8, -1.2, '0', fontsize=12)

# --- Graduation manuelle ---
xticks_major = [5, 10, 15, 19]
yticks_major = [5, 10, 15, 20, 25]

# Axe X grandes graduations
for x in xticks_major:
    ax.plot([x, x], [-0.3, 0.3], color="black", linewidth=1.5)
    ax.text(x, -1.0, str(x), ha='center', va='top', fontsize=12)

# Axe Y grandes graduations
for y in yticks_major:
    if y < 29:  # évite chevauchement avec la flèche
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=1.5)
        ax.text(-1.0, y, str(y), ha='right', va='center', fontsize=12)

# --- Petites graduations intermédiaires ---
# Axe X
for x in range(1, 20):
    if x not in xticks_major:
        ax.plot([x, x], [-0.15, 0.15], color="black", linewidth=1)

# Axe Y
for y in range(1, 30):
    if y not in yticks_major and y < 29:
        ax.plot([-0.1, 0.1], [y, y], color="black", linewidth=1)

# Labels
plt.xlabel('x', fontsize=14, labelpad=15)
plt.ylabel('f(x)', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(fontsize=10, loc='upper right')

plt.show()
