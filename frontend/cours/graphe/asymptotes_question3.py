import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction h(x) = (x³ + 1)/(x² - 1)
def h(x):
    return (x**3 + 1) / (x**2 - 1)

# Asymptote oblique y = x
def asymptote_oblique(x):
    return x

# Domaine de définition (éviter x = -1 et x = 1)
# x = -1 est un trou (discontinuité amovible), pas une asymptote
x1 = np.linspace(-20, -1.1, 1500)
x2 = np.linspace(-0.9, 0.95, 1500)
x3 = np.linspace(1.05, 20, 1500)

# Courbes
plt.plot(x1, h(x1), 'b-', linewidth=2, label=r'$h(x) = \frac{x^3 + 1}{x^2 - 1}$')
plt.plot(x2, h(x2), 'b-', linewidth=2)
plt.plot(x3, h(x3), 'b-', linewidth=2)

# Asymptote verticale x = 1 uniquement
plt.axvline(x=1, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Asymptote verticale $x = 1$')

# Trou en x = -1, y = -3/2
plt.plot(-1, -3/2, 'ro', markersize=8, markerfacecolor='white', markeredgewidth=2, label='Trou en $(-1, -\\frac{3}{2})$')

# Asymptote oblique y = x
x_asymptote = np.linspace(-20, 20, 1000)
plt.plot(x_asymptote, asymptote_oblique(x_asymptote), 'green', linestyle='--', linewidth=1.5, alpha=0.7, label='Asymptote oblique $y = x$')

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
    if y < 19:
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=0.8)
        ax.text(-1.0, y, str(y), ha='right', va='center', fontsize=12)

# --- Petites graduations intermédiaires (tous les 1) ---
# Axe X
for x in range(1, 20):
    if x not in xticks_major:
        ax.plot([x, x], [-0.15, 0.15], color="black", linewidth=0.5)

# Axe Y
for y in range(1, 20):
    if y not in yticks_major and y < 19:
        ax.plot([-0.1, 0.1], [y, y], color="black", linewidth=0.5)

# Labels
plt.xlabel('x', fontsize=14, labelpad=15)
plt.ylabel('f(x)', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(fontsize=10, loc='upper left')

# Sauvegarde
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/asymptotes_question3.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'asymptotes_question3.png' créé avec succès!")
