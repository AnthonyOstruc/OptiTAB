import matplotlib.pyplot as plt
import numpy as np

# Configuration du style
plt.style.use('default')
plt.rcParams['font.size'] = 12

# Créer la figure
fig, ax = plt.subplots(figsize=(12, 8))

# Fonction tan(x) - éviter les asymptotes
x1 = np.linspace(0, np.pi/2 - 0.1, 300)
x2 = np.linspace(np.pi/2 + 0.1, np.pi - 0.01, 300)
x3 = np.linspace(np.pi + 0.01, 3*np.pi/2 - 0.1, 300)
x4 = np.linspace(3*np.pi/2 + 0.1, 2*np.pi - 0.01, 300)

y1 = np.tan(x1)
y2 = np.tan(x2)
y3 = np.tan(x3)
y4 = np.tan(x4)

# Tracer tan(x) - limiter l'axe Y
y1_clipped = np.clip(y1, -5, 5)
y2_clipped = np.clip(y2, -5, 5)
y3_clipped = np.clip(y3, -5, 5)
y4_clipped = np.clip(y4, -5, 5)

plt.plot(x1, y1_clipped, 'b-', linewidth=2, label=r'$y = \tan(x)$')
plt.plot(x2, y2_clipped, 'b-', linewidth=2)
plt.plot(x3, y3_clipped, 'b-', linewidth=2)
plt.plot(x4, y4_clipped, 'b-', linewidth=2)

# Ligne horizontale y = 1
y_target = 1
plt.axhline(y=y_target, color='green', linestyle='--', linewidth=1.5, label=r'$y = 1$')

# Asymptotes verticales
plt.axvline(x=np.pi/2, color='red', linestyle='--', linewidth=1, alpha=0.5)
plt.axvline(x=3*np.pi/2, color='red', linestyle='--', linewidth=1, alpha=0.5)

# Solutions : x = π/4 et x = 5π/4
x_sol1 = np.pi/4
x_sol2 = 5*np.pi/4
plt.axvline(x=x_sol1, color='orange', linestyle=':', linewidth=1.5, alpha=0.7)
plt.axvline(x=x_sol2, color='orange', linestyle=':', linewidth=1.5, alpha=0.7)

# Marquer les points de solution
plt.plot(x_sol1, y_target, 'ro', markersize=8, markeredgecolor='darkred', markeredgewidth=2, label=r'Solutions : $x = \frac{\pi}{4}, \frac{5\pi}{4}$')
plt.plot(x_sol2, y_target, 'ro', markersize=8, markeredgecolor='darkred', markeredgewidth=2)

# Zones solution (simplifiées pour la visualisation)
# [0, π/4]
x_zone1 = np.linspace(0, x_sol1, 100)
y_zone1 = np.tan(x_zone1)
plt.fill_between(x_zone1, -5, y_zone1, alpha=0.2, color='green')

# ]π/2, 5π/4]
x_zone2 = np.linspace(np.pi/2 + 0.15, x_sol2, 100)
y_zone2 = np.tan(x_zone2)
y_zone2_clipped = np.clip(y_zone2, -5, 5)
plt.fill_between(x_zone2, -5, y_zone2_clipped, alpha=0.2, color='green')

# ]3π/2, 2π[
x_zone3 = np.linspace(3*np.pi/2 + 0.15, 2*np.pi - 0.01, 100)
y_zone3 = np.tan(x_zone3)
y_zone3_clipped = np.clip(y_zone3, -5, 5)
plt.fill_between(x_zone3, -5, y_zone3_clipped, alpha=0.2, color='green', label=r'Solution : $\tan(x) \leq 1$')

# Limites
plt.xlim(-10, 10)
plt.ylim(-10, 10)

# Supprimer les ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer les bordures
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches
ax.annotate("", xy=(10, 0), xytext=(-10, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=2))
ax.annotate("", xy=(0, 10), xytext=(0, -10),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=2))

# Texte "0" à l'origine
ax.text(-0.1, -0.3, '0', fontsize=10, ha='right', va='top')

# Graduations tous les π/2 (sans 0π)
xticks_pi_half = [-9*np.pi/2, -7*np.pi/2, -5*np.pi/2, -3*np.pi/2, -np.pi/2, np.pi/2, 3*np.pi/2, 5*np.pi/2, 7*np.pi/2, 9*np.pi/2]
for x_val in xticks_pi_half:
    if -10 <= x_val <= 10:  # Seulement si dans la plage visible
        ax.plot([x_val, x_val], [-0.15, 0.15], color="black", linewidth=0.6)
        n = int(x_val/(np.pi/2))
        if abs(n) == 1:
            label = 'π/2' if n > 0 else '-π/2'
        else:
            label = f'{n}π/2'
        ax.text(x_val, -0.6, label, ha='center', va='top', fontsize=7)

# Labels des axes
ax.text(0, 10.5, 'f(x)', fontsize=12, ha='center', va='bottom')

# Légende
plt.legend(loc='upper right', fontsize=11, framealpha=0.9)

# Ajuster la mise en page
plt.tight_layout()

# Sauvegarder
plt.savefig('inequations_optimisation_question4.png', dpi=300, bbox_inches='tight')
print("Graphique 'inequations_optimisation_question4.png' créé avec succès!")

plt.show()

