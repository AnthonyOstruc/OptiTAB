import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction m(x) = (√(x+1) - 1)/x
def m(x):
    return (np.sqrt(x + 1) - 1) / x

# Domaine de définition (éviter x = 0 et x > -1)
x1 = np.linspace(-0.95, -0.05, 1500)
x2 = np.linspace(0.05, 20, 1500)

# Courbes
plt.plot(x1, m(x1), 'b-', linewidth=2, label=r'$m(x) = \frac{\sqrt{x + 1} - 1}{x}$')
plt.plot(x2, m(x2), 'b-', linewidth=2)

# Trou en x = 0, y = 1/2 (discontinuité évitable)
plt.plot(0, 0.5, 'ro', markersize=8, markerfacecolor='white', markeredgewidth=2, label='Trou en $(0, \\frac{1}{2})$')

# Point de prolongement
plt.plot(0, 0.5, 'go', markersize=6, label='Prolongement : $m(0) = \\frac{1}{2}$')

# Annotation
ax.annotate('$m(0) = \\frac{1}{2}$', (0, 0.5), xytext=(-6, 3), fontsize=10,
            arrowprops=dict(arrowstyle='->', color='green', lw=1))

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
plt.legend(fontsize=10, loc='upper right')

# Sauvegarde
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/prolongement_question5.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'prolongement_question5.png' créé avec succès!")
