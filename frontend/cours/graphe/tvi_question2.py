import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonctions
def f1(x):
    return np.exp(x)

def f2(x):
    return 2*x

# Domaine de définition
x = np.linspace(-20, 20, 1500)

# Courbes
plt.plot(x, f1(x), 'b-', linewidth=2, label=r'$y = e^x$')
plt.plot(x, f2(x), 'r-', linewidth=2, label=r'$y = 2x$')

# Points clés sur [0, 1]
plt.plot(0, np.exp(0), 'go', markersize=6)
ax.annotate('$f(0) = 1 > 0$', (0, np.exp(0)), xytext=(-7, 4), fontsize=10,
            arrowprops=dict(arrowstyle='->', color='green', lw=1))

plt.plot(1, np.exp(1), 'go', markersize=6)
ax.annotate('$f(1) = e - 2 > 0$', (1, np.exp(1)), xytext=(4, 5), fontsize=10,
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
for x_val in xticks_major:
    ax.plot([x_val, x_val], [-0.3, 0.3], color="black", linewidth=0.8)
    ax.text(x_val, -1.0, str(x_val), ha='center', va='top', fontsize=12)

# Axe Y grandes graduations
for y in yticks_major:
    if y < 19:
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=0.8)
        ax.text(-1.0, y, str(y), ha='right', va='center', fontsize=12)

# --- Petites graduations intermédiaires (tous les 1) ---
# Axe X
for x_val in range(1, 20):
    if x_val not in xticks_major:
        ax.plot([x_val, x_val], [-0.15, 0.15], color="black", linewidth=0.5)

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
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/tvi_question2.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'tvi_question2.png' créé avec succès!")
