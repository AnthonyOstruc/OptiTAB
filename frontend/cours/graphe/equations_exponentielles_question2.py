import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Inéquation e^(2x) - 3e^x + 2 ≤ 0
# Solutions: x ∈ [0, ln(2)]

# Fonction f(x) = e^(2x) - 3e^x + 2
def f(x):
    return np.exp(2*x) - 3*np.exp(x) + 2

# Domaine de tracé sur ℝ
x = np.linspace(-20, 20, 1000)
y = f(x)

# Tracer la courbe
plt.plot(x, y, 'b-', linewidth=2, label=r'$f(x) = e^{2x} - 3e^x + 2$')

# Solutions f(x) = 0
plt.plot(0, f(0), 'go', markersize=8, label='Solution x = 0')
plt.plot(np.log(2), f(np.log(2)), 'go', markersize=8, label='Solution x = ln(2)')

# Zone solution f(x) ≤ 0 (entre 0 et ln(2))
x_solution = np.linspace(0, np.log(2), 100)
y_solution = f(x_solution)
plt.fill_between(x_solution, y_solution, 0, alpha=0.3, color='red', label='Solution f(x) ≤ 0')

# Axe x = 0
plt.axhline(y=0, color='black', linestyle='-', linewidth=1.5)

# Asymptote horizontale y = 2 en -∞
plt.axhline(y=2, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Asymptote horizontale $y = 2$')

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
for y_val in yticks_major:
    if y_val < 19:
        ax.plot([-0.2, 0.2], [y_val, y_val], color="black", linewidth=0.8)
        ax.text(-1.0, y_val, str(y_val), ha='right', va='center', fontsize=12)

# --- Petites graduations intermédiaires (tous les 1) ---
# Axe X
for x_val in range(1, 20):
    if x_val not in xticks_major:
        ax.plot([x_val, x_val], [-0.15, 0.15], color="black", linewidth=0.5)

# Axe Y
for y_val in range(1, 20):
    if y_val not in yticks_major and y_val < 19:
        ax.plot([-0.1, 0.1], [y_val, y_val], color="black", linewidth=0.5)

# Labels
plt.xlabel('x', fontsize=14, labelpad=15)
plt.ylabel('f(x)', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(fontsize=10, loc='upper left')

# Sauvegarde
plt.savefig('/Users/anthonytabet/Desktop/OptiTABV2/OptiTAB/frontend/cours/graphe/equations_exponentielles_question2.png', 
            dpi=300, bbox_inches='tight')
plt.close()

print("Graphique 'equations_exponentielles_question2.png' créé avec succès!")


