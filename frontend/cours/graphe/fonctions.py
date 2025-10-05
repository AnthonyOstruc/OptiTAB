import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction rationnelle simplifiée : (x² + 4x + 3)/(x² - 1) = (x + 3)/(x - 1)
def f(x):
    return (x + 3) / (x - 1)

# Intervalles (éviter les discontinuités en x = 1 et x = -1)
x1 = np.linspace(-10, 0.9, 1000)  # x < 1
x2 = np.linspace(1.1, 10, 1000)   # x > 1

# Courbes
plt.plot(x1, f(x1), 'b-', linewidth=2, label=r'$f(x) = \frac{x^2 + 4x + 3}{x^2 - 1} = \frac{x + 3}{x - 1}$')
plt.plot(x2, f(x2), 'b-', linewidth=2)

# Asymptotes
plt.axvline(x=1, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Asymptote verticale x = 1')
plt.axhline(y=1, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Asymptote horizontale y = 1')

# Limites du graphique
plt.xlim(-8, 8)
plt.ylim(-5, 15)

# Désactiver ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches
ax.annotate("", xy=(8, 0), xytext=(-8, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))
ax.annotate("", xy=(0, 15), xytext=(0, -5),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))

# Texte "0"
ax.text(-0.8, -1.2, '0', fontsize=12)

# --- Graduation manuelle ---
xticks_major = [-5, -10, 5, 10]
yticks_major = [5, 10]

# Axe X grandes graduations
for x in xticks_major:
    if x >= -5 and x <= 5:  # éviter les zones problématiques
        ax.plot([x, x], [-0.3, 0.3], color="black", linewidth=1.5)
        ax.text(x, -1.0, str(x), ha='center', va='top', fontsize=12)

# Axe Y grandes graduations
for y in yticks_major:
    if y <= 10:
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=1.5)
        ax.text(-1.0, y, str(y), ha='right', va='center', fontsize=12)

# --- Petites graduations intermédiaires ---
# Axe X
for x in range(-7, 8):
    if x not in xticks_major and x != 1 and x != -1:
        ax.plot([x, x], [-0.15, 0.15], color="black", linewidth=1)

# Axe Y
for y in range(1, 12):
    if y not in yticks_major:
        ax.plot([-0.1, 0.1], [y, y], color="black", linewidth=1)

# Labels
plt.xlabel('x', fontsize=14, labelpad=15)
plt.ylabel('f(x)', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(fontsize=10, loc='upper right')

# Titre
plt.title('Graphe de la fonction rationnelle avec ses asymptotes', fontsize=16, pad=20)

plt.show()
