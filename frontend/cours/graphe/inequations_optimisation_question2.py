import matplotlib.pyplot as plt
import numpy as np

# Configuration du style
plt.style.use('default')
plt.rcParams['font.size'] = 12

# Créer la figure
fig, ax = plt.subplots(figsize=(12, 8))

# Fonction cos(2x)
x = np.linspace(0, np.pi, 1000)
y = np.cos(2*x)

# Tracer cos(2x)
plt.plot(x, y, 'b-', linewidth=2, label=r'$y = \cos(2x)$')

# Ligne horizontale y = 1/2
y_target = 0.5
plt.axhline(y=y_target, color='green', linestyle='--', linewidth=1.5, label=r'$y = \frac{1}{2}$')

# Solutions : x = π/6 et x = 5π/6
x1 = np.pi/6
x2 = 5*np.pi/6
plt.axvline(x=x1, color='red', linestyle=':', linewidth=1.5, alpha=0.7)
plt.axvline(x=x2, color='red', linestyle=':', linewidth=1.5, alpha=0.7)

# Marquer les points de solution
plt.plot(x1, y_target, 'ro', markersize=8, markeredgecolor='darkred', markeredgewidth=2, label=r'Solutions : $x = \frac{\pi}{6}, \frac{5\pi}{6}$')
plt.plot(x2, y_target, 'ro', markersize=8, markeredgecolor='darkred', markeredgewidth=2)

# Zone solution : ]π/6, 5π/6[
x_solution = np.linspace(x1, x2, 100)
y_solution = np.cos(2*x_solution)
plt.fill_between(x_solution, y_solution, y_target, where=(y_solution < y_target), alpha=0.3, color='green', interpolate=True, label=r'Solution : $\cos(2x) < \frac{1}{2}$')

# Limites
plt.xlim(-5, 5)
plt.ylim(-5, 5)

# Supprimer les ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer les bordures
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches
ax.annotate("", xy=(5, 0), xytext=(-5, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=2))
ax.annotate("", xy=(0, 5), xytext=(0, -5),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=2))

# Texte "0" à l'origine
ax.text(-0.05, -0.15, '0', fontsize=10, ha='right', va='top')

# Graduations tous les π/2 (sans 0π)
xticks_pi_half = [-3*np.pi/2, -np.pi/2, np.pi/2, 3*np.pi/2]
for x_val in xticks_pi_half:
    if -5 <= x_val <= 5:  # Seulement si dans la plage visible
        ax.plot([x_val, x_val], [-0.15, 0.15], color="black", linewidth=0.6)
        n = int(x_val/(np.pi/2))
        if abs(n) == 1:
            label = 'π/2' if n > 0 else '-π/2'
        else:
            label = f'{n}π/2'
        ax.text(x_val, -0.5, label, ha='center', va='top', fontsize=7)

# Labels des axes
ax.text(0, 5.3, 'f(x)', fontsize=12, ha='center', va='bottom')

# Légende
plt.legend(loc='upper right', fontsize=11, framealpha=0.9)

# Ajuster la mise en page
plt.tight_layout()

# Sauvegarder
plt.savefig('inequations_optimisation_question2.png', dpi=300, bbox_inches='tight')
print("Graphique 'inequations_optimisation_question2.png' créé avec succès!")

plt.show()

