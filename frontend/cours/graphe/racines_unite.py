import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuration du style
plt.style.use('default')
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'serif'

# Création de la figure
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.set_aspect('equal')

# Configuration des axes
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)

# Grille
ax.grid(True, alpha=0.3, linestyle='--')

# Axes principaux
ax.axhline(y=0, color='black', linewidth=1.5)
ax.axvline(x=0, color='black', linewidth=1.5)

# Flèches des axes
ax.annotate('', xy=(1.4, 0), xytext=(1.2, 0),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
ax.annotate('', xy=(0, 1.4), xytext=(0, 1.2),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# Labels des axes
ax.text(1.3, -0.1, 'Re', fontsize=14, ha='center')
ax.text(-0.1, 1.3, 'Im', fontsize=14, ha='center')

# Cercle unité
circle = plt.Circle((0, 0), 1, fill=False, color='black', linewidth=2)
ax.add_patch(circle)

# Racines de l'unité pour n = 6
n = 6
angles = np.linspace(0, 2*np.pi, n+1)[:-1]  # 0 à 2π exclu
roots_x = np.cos(angles)
roots_y = np.sin(angles)

# Couleurs pour les racines
colors = ['red', 'orange', 'cyan', 'green', 'blue', 'purple']

# Tracer les racines
for i, (x, y) in enumerate(zip(roots_x, roots_y)):
    # Point
    ax.plot(x, y, 'o', color=colors[i], markersize=10)
    
    # Ligne du centre vers la racine
    ax.plot([0, x], [0, y], color=colors[i], linewidth=2)
    
    # Label de la racine avec positionnement adaptatif
    if i == 0:  # z_0 sur l'axe réel positif
        ax.text(x*1.3, -0.2, f'z_{i}', fontsize=12, fontweight='bold', 
                color=colors[i], ha='center', va='top')
    elif i == 3:  # z_3 sur l'axe réel négatif
        ax.text(x*1.3, 0.2, f'z_{i}', fontsize=12, fontweight='bold', 
                color=colors[i], ha='center', va='bottom')
    elif i == 1 or i == 2:  # z_1 et z_2 dans les quadrants supérieurs
        ax.text(x*1.3, y*1.3, f'z_{i}', fontsize=12, fontweight='bold', 
                color=colors[i], ha='center', va='center')
    else:  # z_4 et z_5 dans les quadrants inférieurs
        ax.text(x*1.3, y*1.3, f'z_{i}', fontsize=12, fontweight='bold', 
                color=colors[i], ha='center', va='center')

# Racine principale z_0 = 1 (déjà tracée dans la boucle)

# Marques sur les axes
ax.text(1, -0.1, '1', ha='center', va='top', fontsize=10)
ax.text(-1, -0.1, '-1', ha='center', va='top', fontsize=10)
ax.text(-0.1, 1, 'i', ha='right', va='center', fontsize=10)
ax.text(-0.1, -1, '-i', ha='right', va='center', fontsize=10)

# Annotation de l'unité imaginaire
ax.text(0.05, 1.05, 'i', fontsize=14, fontweight='bold', color='red')

# Titre simple
ax.text(0, 1.4, 'Racines n-ièmes de l\'unité (n=6)', 
        fontsize=16, fontweight='bold', ha='center')

# Suppression des ticks par défaut
ax.set_xticks([])
ax.set_yticks([])

# Ajustement des marges
plt.tight_layout()

# Sauvegarde
plt.savefig('racines_unite.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')

# Affichage
plt.show()

print("Graphique sauvegardé sous 'racines_unite.png'")
