import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonctions
f1 = lambda x: np.log(x + 2)
f2 = lambda x: np.log(3*x - 1)

# Domaine de f1: x > -2
# Domaine de f2: x > 1/3
# Domaine commun: x > 1/3

# Créer des domaines séparés pour une meilleure visualisation des asymptotes
x_f1_left = np.linspace(-2 + 1e-11, 1/3 - 1e-11, 20000)  # Partie de f1 avant le domaine commun
x_common = np.linspace(1/3 + 1e-11, 20, 20000)  # Domaine commun

# Courbes
plt.plot(x_f1_left, f1(x_f1_left), 'b-', linewidth=2)  # Courbe f1 sur sa partie gauche
plt.plot(x_common, f1(x_common), 'b-', linewidth=2, label=r'$y = \ln(x+2)$')  # Courbe f1 sur le domaine commun
plt.plot(x_common, f2(x_common), 'g-', linewidth=2, label=r'$y = \ln(3x-1)$')  # Courbe f2 sur le domaine commun

# Asymptotes verticales pertinentes au problème
plt.axvline(x=1/3, color='red', linestyle='--', linewidth=1.5, label=r'Asymptote $x=\frac{1}{3}$')
plt.axvline(x=-2, color='red', linestyle='--', linewidth=1.0, label=r'Asymptote $x=-2$')

# Point solution x = 3/2
x_sol = 1.5
y_sol = np.log(x_sol + 2)
if x_sol > 1/3:
    plt.plot(x_sol, y_sol, 'mo', markersize=6, label=r'Solution $x=\frac{3}{2}$')

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

# --- Graduation manuelle (template) ---
xticks_major = [5, 10, 15, 19]
yticks_major = [5, 10, 15, 19]
for x_val in xticks_major:
    ax.plot([x_val, x_val], [-0.3, 0.3], color="black", linewidth=0.8)
    ax.text(x_val, -1.0, str(x_val), ha='center', va='top', fontsize=12)
for y in yticks_major:
    if y < 19:
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=0.8)
        ax.text(-1.0, y, str(y), ha='right', va='center', fontsize=12)
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

# Légende
plt.legend(fontsize=10, loc='upper right')

# Sauvegarde
plt.savefig('exercice_logarithme_equations_question1.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'exercice_logarithme_equations_question1.png' créé avec succès!")


