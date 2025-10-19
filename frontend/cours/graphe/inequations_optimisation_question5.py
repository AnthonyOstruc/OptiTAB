import matplotlib.pyplot as plt
import numpy as np

# Configuration du style
plt.style.use('default')
plt.rcParams['font.size'] = 12

# Créer la figure
fig, ax = plt.subplots(figsize=(12, 8))

# Fonction f(x) = sin(x) + cos(x)
x = np.linspace(0, 2*np.pi, 1000)
y = np.sin(x) + np.cos(x)

# Tracer f(x)
plt.plot(x, y, 'b-', linewidth=2, label=r'$f(x) = \sin(x) + \cos(x)$')

# Ligne horizontale y = 1
y_target = 1
plt.axhline(y=y_target, color='green', linestyle='--', linewidth=1.5, label=r'$y = 1$')

# Solutions : x = 0 et x = π/2
x1 = 0
x2 = np.pi/2
plt.axvline(x=x2, color='red', linestyle=':', linewidth=1.5, alpha=0.7)

# Marquer les points de solution
plt.plot(x1, y_target, 'ro', markersize=8, markeredgecolor='darkred', markeredgewidth=2, label=r'Solutions : $x = 0, \frac{\pi}{2}$')
plt.plot(x2, y_target, 'ro', markersize=8, markeredgecolor='darkred', markeredgewidth=2)

# Zone solution : [0, π/2]
x_solution = np.linspace(x1, x2, 100)
y_solution = np.sin(x_solution) + np.cos(x_solution)
plt.fill_between(x_solution, y_solution, y_target, where=(y_solution >= y_target), alpha=0.3, color='green', interpolate=True, label=r'Solution : $\sin(x) + \cos(x) \geq 1$')

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
ax.text(-0.1, -0.15, '0', fontsize=10, ha='right', va='top')

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
plt.savefig('inequations_optimisation_question5.png', dpi=300, bbox_inches='tight')
print("Graphique 'inequations_optimisation_question5.png' créé avec succès!")

plt.show()

