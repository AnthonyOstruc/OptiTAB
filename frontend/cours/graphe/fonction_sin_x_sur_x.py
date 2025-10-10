import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction sin(x)/x
def f(x):
    # Éviter la division par zéro en x = 0
    # La limite de sin(x)/x quand x -> 0 est 1 (théorème de l'Hôpital)
    return np.where(x == 0, 1, np.sin(x) / x)

# Intervalles - on évite x = 0 (point de discontinuité apparente)
x1 = np.linspace(-20, -0.01, 1000)  # Avant x = 0
x2 = np.linspace(0.01, 20, 1000)    # Après x = 0

# Courbes
plt.plot(x1, f(x1), 'b-', linewidth=2, label=r'$f(x) = \frac{\sin(x)}{x}$')
plt.plot(x2, f(x2), 'b-', linewidth=2)

# Point spécial en x = 0 (limite)
plt.plot(0, 1, 'ro', markersize=8, markeredgewidth=2, markerfacecolor='white', 
         label='f(0) = 1 (limite)')

# Asymptote horizontale en y = 0 (limite quand x tend vers ±∞)
plt.axhline(y=0, color='green', linestyle='--', linewidth=1.5, alpha=0.7, label='Asymptote y = 0')

# Limites
plt.xlim(-20, 20)
plt.ylim(-1, 1.5)

# Désactiver ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches
ax.annotate("", xy=(20, 0), xytext=(-20, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))
ax.annotate("", xy=(0, 1.5), xytext=(0, -1),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))

# Texte "0"
ax.text(-0.8, -0.15, '0', fontsize=12)

# --- Graduation manuelle ---
# Graduations en multiples de π
xticks_major = [-6*np.pi, -4*np.pi, -2*np.pi, 2*np.pi, 4*np.pi, 6*np.pi]
xticks_labels = ['-6π', '-4π', '-2π', '2π', '4π', '6π']
yticks_major = [0.5, 1, 1.5]

# Axe X grandes graduations (plus petites)
for i, x in enumerate(xticks_major):
    ax.plot([x, x], [-0.03, 0.03], color="black", linewidth=0.6)
    ax.text(x, -0.1, xticks_labels[i], ha='center', va='top', fontsize=10)

# Axe Y grandes graduations (plus petites)
for y in yticks_major:
    if y < 1.4:  # évite chevauchement avec la flèche
        ax.plot([-0.2, 0.2], [y, y], color="black", linewidth=0.6)
        ax.text(-0.6, y, str(y), ha='right', va='center', fontsize=10)

# --- Petites graduations intermédiaires ---
# Axe X (en π/2)
for k in range(-12, 13):
    x = k * np.pi / 2
    if x not in xticks_major and x != 0:
        ax.plot([x, x], [-0.015, 0.015], color="black", linewidth=0.4)

# Axe Y (tous les 0.1)
for y in np.arange(-0.9, 1.6, 0.1):
    if y not in yticks_major and y < 1.4:
        ax.plot([-0.1, 0.1], [y, y], color="black", linewidth=0.4)

# Labels
plt.xlabel('x', fontsize=14, labelpad=15)
plt.ylabel('f(x)', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.415)
ax.yaxis.set_label_coords(0.48, 1.02)

# Légende
plt.legend(fontsize=10, loc='upper right')

# Titre supprimé

plt.show()
