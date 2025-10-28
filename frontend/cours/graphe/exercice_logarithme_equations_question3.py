import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Domaine de validité final: x > 2
f = lambda x: np.log(x + 2)

x = np.linspace(2.00001, 20, 3000)

plt.plot(x, f(x), 'b-', linewidth=2, label=r'$y = \ln(x+2)$ (domaine $x>2$)')
plt.axhline(y=1, color='orange', linestyle='--', linewidth=1.5, label=r'$y=1$')

# Indication visuelle: pas de solution dans x>2
plt.text(3, 1.2, 'Pas de solution (x>2)', color='crimson', fontsize=11)

# Limites/zoom
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

# Graduations template
xticks_major = [5, 10, 15, 19]
yticks_major = [5, 10, 15, 19]
for xv in xticks_major:
    ax.plot([xv, xv], [-0.3, 0.3], color="black", linewidth=0.8)
    ax.text(xv, -1.0, str(xv), ha='center', va='top', fontsize=12)
for yv in yticks_major:
    if yv < 19:
        ax.plot([-0.2, 0.2], [yv, yv], color="black", linewidth=0.8)
        ax.text(-1.0, yv, str(yv), ha='right', va='center', fontsize=12)
for xv in range(1, 20):
    if xv not in xticks_major:
        ax.plot([xv, xv], [-0.15, 0.15], color="black", linewidth=0.5)
for yv in range(1, 20):
    if yv not in yticks_major and yv < 19:
        ax.plot([-0.1, 0.1], [yv, yv], color="black", linewidth=0.5)

# Labels
plt.xlabel('x', fontsize=14, labelpad=15)
plt.ylabel('y', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

plt.legend(fontsize=10, loc='upper right')

plt.savefig('exercice_logarithme_equations_question3.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'exercice_logarithme_equations_question3.png' créé avec succès!")


