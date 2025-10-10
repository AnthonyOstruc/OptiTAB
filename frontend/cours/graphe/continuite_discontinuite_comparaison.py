import matplotlib.pyplot as plt
import numpy as np

# Configuration du style
plt.style.use('default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# === FONCTION CONTINUE (gauche) ===
def fonction_continue(x):
    return x**2 - 2*x + 1

# Création des données pour la fonction continue
x1 = np.linspace(-2, 4, 1000)
y1 = fonction_continue(x1)

# Tracé de la fonction continue
ax1.plot(x1, y1, color='#2E8B57', linewidth=4, label='f(x) = x² - 2x + 1')

# Configuration du graphique gauche
ax1.set_xlim(-2, 4)
ax1.set_ylim(-1, 8)
ax1.grid(False)
ax1.set_xlabel('')
ax1.set_ylabel('')
ax1.set_title('Fonction Continue', fontsize=18, fontweight='bold', color='#2E8B57', pad=20)
ax1.set_xticks([])
ax1.set_yticks([])

# Ajout d'annotations pour la continuité
ax1.annotate('Courbe continue\n(peut être tracée\nsans lever le stylo)', 
            xy=(1, 0), xytext=(0.5, 3),
            arrowprops=dict(arrowstyle='->', color='#2E8B57', lw=2),
            fontsize=12, ha='center',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#E8F5E8', alpha=0.9))

# Mise en forme du graphique gauche
ax1.legend(fontsize=14)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_visible(False)

# === FONCTION DISCONTINUE (droite) ===
def fonction_discontinue(x):
    y = np.zeros_like(x)
    # Première partie : parabole pour x < 1
    mask1 = x < 1
    y[mask1] = x[mask1]**2 - 2*x[mask1] + 1
    
    # Deuxième partie : parabole décalée pour x >= 1 (avec saut)
    mask2 = x >= 1
    y[mask2] = x[mask2]**2 - 2*x[mask2] + 1 + 2  # +2 pour créer le saut
    
    return y

# Création des données pour la fonction discontinue
x2 = np.linspace(-2, 4, 1000)
y2 = fonction_discontinue(x2)

# Tracé de la fonction discontinue
ax2.plot(x2, y2, color='#8B4513', linewidth=4, label='f(x) avec discontinuité')

# Ajout du point de discontinuité (cercle vide)
ax2.plot(1, 1, 'o', color='#8B4513', markersize=10, markeredgewidth=3, 
        markerfacecolor='white', label='Point de discontinuité')

# Configuration du graphique droite
ax2.set_xlim(-2, 4)
ax2.set_ylim(-1, 8)
ax2.grid(False)
ax2.set_xlabel('')
ax2.set_ylabel('')
ax2.set_title('Fonction Discontinue', fontsize=18, fontweight='bold', color='#8B4513', pad=20)
ax2.set_xticks([])
ax2.set_yticks([])

# Ajout d'annotations pour la discontinuité
ax2.annotate('Saut de discontinuité\n(impossible de tracer\nsans lever le stylo)', 
            xy=(1, 3), xytext=(2.5, 5),
            arrowprops=dict(arrowstyle='->', color='#8B4513', lw=2),
            fontsize=12, ha='center',
            bbox=dict(boxstyle="round,pad=0.4", facecolor='#FDF2E9', alpha=0.9))

# Ligne verticale pour marquer la discontinuité
ax2.axvline(x=1, color='red', linestyle='--', alpha=0.8, linewidth=3)

# Mise en forme du graphique droite
ax2.legend(fontsize=14)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['bottom'].set_visible(False)

# Ligne de séparation verticale entre les deux graphiques
ax2.axvline(x=-2, color='black', linewidth=2, alpha=0.8)

# Titre principal supprimé

# Ajustement de la mise en page
plt.tight_layout()

# Sauvegarde
plt.savefig('continuite_discontinuite_comparaison.png', dpi=300, bbox_inches='tight')
plt.show()
