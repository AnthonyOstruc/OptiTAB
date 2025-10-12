import numpy as np
import matplotlib.pyplot as plt

# Configuration de la figure avec deux sous-graphes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# ============= GRAPHE 1 : FONCTION CONVEXE =============
def f_convexe(x):
    """Fonction convexe : x^2"""
    return x**2

# Intervalle
x = np.linspace(-3, 3, 500)
y_convexe = f_convexe(x)

# Tracer la courbe convexe
ax1.plot(x, y_convexe, color='#3498db', linewidth=3, label=r'$f(x) = x^2$ (convexe)')

# Points pour les tangentes
points = [-2, 0, 2]
colors_tangent = ['#e74c3c', '#27ae60', '#9b59b6']

for i, x0 in enumerate(points):
    y0 = f_convexe(x0)
    # Point sur la courbe
    ax1.plot(x0, y0, 'o', color=colors_tangent[i], markersize=8, zorder=5)
    
    # Dérivée : f'(x) = 2x
    m = 2 * x0
    
    # Tangente
    x_tangent = np.linspace(x0-1.5, x0+1.5, 100)
    y_tangent = m * (x_tangent - x0) + y0
    ax1.plot(x_tangent, y_tangent, '--', color=colors_tangent[i], 
             linewidth=2, alpha=0.8, label=f'Tangente en x={x0}')


# Axes
ax1.axhline(y=0, color='black', linewidth=1.2, alpha=0.7)
ax1.axvline(x=0, color='black', linewidth=1.2, alpha=0.7)

# Configuration des axes
ax1.set_xlim(-3, 3)
ax1.set_ylim(-1, 10)
ax1.set_xlabel('x', fontsize=14, fontweight='bold')
ax1.set_ylabel('f(x)', fontsize=14, fontweight='bold')
ax1.set_title('FONCTION CONVEXE\n' + r"$f''(x) > 0$ : courbe au-dessus des tangentes", 
              fontsize=14, fontweight='bold', pad=15, color='#3498db')
ax1.legend(fontsize=10, loc='center')

# ============= GRAPHE 2 : FONCTION CONCAVE =============
def f_concave(x):
    """Fonction concave : -x^2 + 8"""
    return -x**2 + 8

y_concave = f_concave(x)

# Tracer la courbe concave
ax2.plot(x, y_concave, color='#e67e22', linewidth=3, label=r'$f(x) = -x^2 + 8$ (concave)')

# Points pour les tangentes
for i, x0 in enumerate(points):
    y0 = f_concave(x0)
    # Point sur la courbe
    ax2.plot(x0, y0, 'o', color=colors_tangent[i], markersize=8, zorder=5)
    
    # Dérivée : f'(x) = -2x
    m = -2 * x0
    
    # Tangente
    x_tangent = np.linspace(x0-1.5, x0+1.5, 100)
    y_tangent = m * (x_tangent - x0) + y0
    ax2.plot(x_tangent, y_tangent, '--', color=colors_tangent[i], 
             linewidth=2, alpha=0.8, label=f'Tangente en x={x0}')


# Axes
ax2.axhline(y=0, color='black', linewidth=1.2, alpha=0.7)
ax2.axvline(x=0, color='black', linewidth=1.2, alpha=0.7)

# Configuration des axes
ax2.set_xlim(-3, 3)
ax2.set_ylim(-1, 10)
ax2.set_xlabel('x', fontsize=14, fontweight='bold')
ax2.set_ylabel('f(x)', fontsize=14, fontweight='bold')
ax2.set_title('FONCTION CONCAVE\n' + r"$f''(x) < 0$ : courbe en-dessous des tangentes", 
              fontsize=14, fontweight='bold', pad=15, color='#e67e22')
ax2.legend(fontsize=10, loc='center')

# Titre général
fig.suptitle('COMPARAISON : CONVEXITÉ vs CONCAVITÉ', 
             fontsize=18, fontweight='bold', y=0.98)

# Ajuster la mise en page
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Sauvegarder
plt.savefig('convexite_concavite.png', dpi=300, bbox_inches='tight')
print("✓ Graphe généré : convexite_concavite.png")
plt.show()

