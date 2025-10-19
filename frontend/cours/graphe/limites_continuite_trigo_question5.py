import matplotlib.pyplot as plt
import numpy as np

# Configuration du style
plt.style.use('default')
plt.rcParams['font.size'] = 12

# Créer la figure
fig, ax = plt.subplots(figsize=(12, 8))

# Fonction sin(x)/x
def f(x):
    return np.sin(x) / x

# Domaine - éviter x = 0
x1 = np.linspace(-20, -0.01, 1000)
x2 = np.linspace(0.01, 20, 1000)

# Tracer sin(x)/x
plt.plot(x1, f(x1), 'b-', linewidth=1.5, label=r'$f(x) = \frac{\sin(x)}{x}$')
plt.plot(x2, f(x2), 'b-', linewidth=1.5)

# Encadrement: -1/x et 1/x
x_pos = np.linspace(0.2, 20, 500)
x_neg = np.linspace(-20, -0.2, 500)
plt.plot(x_pos, 1/x_pos, 'r--', linewidth=2.5, label=r'$y = \frac{1}{x}$', alpha=0.9)
plt.plot(x_pos, -1/x_pos, 'r--', linewidth=2.5, label=r'$y = -\frac{1}{x}$', alpha=0.9)
plt.plot(x_neg, 1/x_neg, 'r--', linewidth=2.5, alpha=0.9)
plt.plot(x_neg, -1/x_neg, 'r--', linewidth=2.5, alpha=0.9)

# Ligne y = 0 pour visualiser la limite à l'infini
plt.axhline(y=0, color='green', linestyle='--', linewidth=2, alpha=0.8, label=r'$\lim_{x \to +\infty} \frac{\sin(x)}{x} = 0$')

# Limites - zoom plus approprié
plt.xlim(-20, 20)
plt.ylim(-5, 5)

# Supprimer les ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer les bordures
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches
ax.annotate("", xy=(20, 0), xytext=(-20, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=2))
ax.annotate("", xy=(0, 5), xytext=(0, -5),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=2))

# Pas de graduations ni de textes

# Labels des axes
plt.xlabel('x', fontsize=16, labelpad=20)
plt.ylabel('f(x)', fontsize=16, labelpad=20, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(loc='upper right', fontsize=11, framealpha=0.9)

# Ajuster la mise en page
plt.tight_layout()

# Sauvegarder
plt.savefig('limites_continuite_trigo_question5.png', dpi=300, bbox_inches='tight')
print("Graphique 'limites_continuite_trigo_question5.png' créé avec succès!")

plt.show()

