import matplotlib.pyplot as plt
import numpy as np

# Configuration de la figure
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)

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

# Fonctions à comparer
# Pour les fonctions définies sur x > 0
x_pos = np.linspace(0.0001, 20, 2000)
# Pour les fonctions définies sur tout ℝ
x_all = np.linspace(-20, 20, 2000)

# I. Exponentielle népérienne
y_exp = np.exp(x_all)

# II. Logarithme népérien
y_log = np.log(x_pos)

# III. Exponentielles en base a
y_exp2 = 2**x_all  # a > 1
y_exp_half = 0.5**x_all  # 0 < a < 1

# IV. Fonctions puissances
y_pow2 = x_pos**2  # α > 1
y_pow_half = x_pos**0.5  # 0 < α < 1
y_pow_neg = x_pos**(-1)  # α < 0

# Tracer les courbes croissantes uniquement
# Exponentielle népérienne
ax.plot(x_all, y_exp, 'r-', linewidth=2, label=r'$e^x$')

# Logarithme népérien
ax.plot(x_pos, y_log, 'purple', linewidth=2, label=r'$\ln(x)$')

# Exponentielles en base a (a > 1)
ax.plot(x_all, y_exp2, 'b-', linewidth=2, label=r'$2^x$ ($a > 1$)')

# Fonctions puissances (α > 1)
ax.plot(x_pos, y_pow2, 'g-', linewidth=2, label=r'$x^2$ ($\alpha > 1$)')

# Graduation manuelle
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

# Petites graduations intermédiaires
for x_val in range(1, 20):
    if x_val not in xticks_major:
        ax.plot([x_val, x_val], [-0.15, 0.15], color="black", linewidth=0.5)

for y_val in range(1, 20):
    if y_val not in yticks_major and y_val < 19:
        ax.plot([-0.1, 0.1], [y_val, y_val], color="black", linewidth=0.5)

# Labels
ax.set_xlabel(r'$x$', fontsize=14, labelpad=15)
ax.set_ylabel(r'$y$', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
ax.legend(loc='upper right', fontsize=10)

# Supprimer le titre principal
plt.suptitle('', fontsize=0)

# Ajuster la mise en page
plt.tight_layout()

# Sauvegarder
plt.savefig('graphe_croissances_comparees.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'graphe_croissances_comparees.png' créé avec succès!")

