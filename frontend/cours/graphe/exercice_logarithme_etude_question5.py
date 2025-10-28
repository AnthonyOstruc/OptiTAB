import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonctions
def m(x):
    return np.log((x + 1) / (x - 1))

# Domaine de définition : ]-∞, -1[ ∪ ]1, +∞[
# Créer deux domaines séparés
x1 = np.linspace(-20, -1.00000000001, 20000)  # Premier intervalle - ultra proche de -1
x2 = np.linspace(1.00000000001, 20, 20000)    # Deuxième intervalle - ultra proche de 1

# Courbes
plt.plot(x1, m(x1), 'b-', linewidth=2, label=r'$m(x) = \ln\left(\frac{x+1}{x-1}\right)$')
plt.plot(x2, m(x2), 'b-', linewidth=2)

# Asymptotes verticales
plt.axvline(x=-1, color='red', linestyle='--', linewidth=1.5, label='Asymptote $x = -1$')
plt.axvline(x=1, color='red', linestyle='--', linewidth=1.5, label='Asymptote $x = 1$')

# Asymptote horizontale y = 0
plt.axhline(y=0, color='orange', linestyle='--', linewidth=1.5, label='Asymptote $y = 0$')

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
plt.ylabel('m(x)', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(fontsize=10, loc='upper right')

# Sauvegarde
plt.savefig('exercice_logarithme_etude_question5.png', 
            dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'exercice_logarithme_etude_question5.png' créé avec succès!")