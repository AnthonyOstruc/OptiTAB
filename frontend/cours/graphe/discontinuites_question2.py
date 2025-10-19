import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction g(x) définie par morceaux
x1 = np.linspace(-20, 0, 1500)
x2 = np.linspace(0, 20, 1500)

# Première partie: x + 1 pour x < 0
y1 = x1 + 1
plt.plot(x1[:-1], y1[:-1], 'b-', linewidth=2, label=r'$g(x)$ (fonction par morceaux)')

# Deuxième partie: x - 1 pour x ≥ 0
y2 = x2 - 1
plt.plot(x2, y2, 'b-', linewidth=2)

# Limite à gauche en x = 0: y = 1
plt.plot(0, 1, 'ro', markersize=8, markerfacecolor='white', markeredgewidth=2, label='Limite à gauche = 1')

# Valeur de la fonction et limite à droite en x = 0: y = -1
plt.plot(0, -1, 'go', markersize=8, label='$g(0) = -1$')

# Annotation du saut
ax.annotate('Saut d\'amplitude 2', (0, 0), xytext=(4, 3), fontsize=10,
            arrowprops=dict(arrowstyle='->', color='orange', lw=1))

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
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/discontinuites_question2.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'discontinuites_question2.png' créé avec succès!")
