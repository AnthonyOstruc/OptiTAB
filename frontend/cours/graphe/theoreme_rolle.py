import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction pour illustrer le théorème de Rolle : f(x) = -x^2 + 4
# Sur [-2, 2], on a f(-2) = f(2) = 0 et f'(0) = 0
def f(x):
    return -x**2 + 4

def f_prime(x):
    return -2*x

# Intervalle [a, b] où f(a) = f(b)
a = -2
b = 2

# Calcul des valeurs
f_a = f(a)
f_b = f(b)

# Point c où f'(c) = 0 (dans le théorème de Rolle)
# f'(c) = -2c = 0 donc c = 0
c = 0
f_c = f(c)

# Intervalle pour la fonction
x = np.linspace(-20, 20, 1000)

# Courbe
plt.plot(x, f(x), 'b-', linewidth=2, label=r'$f(x)$')

# Tracer la corde horizontale entre (a, f(a)) et (b, f(b))
# Comme f(a) = f(b), c'est une ligne horizontale
plt.plot([a, b], [f_a, f_b], 'r--', linewidth=2, label=r'Corde entre $f(a)$ et $f(b)$', alpha=0.8)

# Tracer la tangente horizontale en C (f'(c) = 0)
x_tangent = np.linspace(-20, 20, 200)
y_tangent = f_prime(c) * (x_tangent - c) + f_c  # f'(c) = 0, donc y_tangent = f_c (constante)
plt.plot(x_tangent, y_tangent, 'g--', linewidth=2, label=r'Tangente en $c$ ($f\'(c) = 0$)', alpha=0.8)

# Points (a, f(a)), (b, f(b)) et (c, f(c)) avec labels pour la légende
ax.plot(a, f_a, 'ro', markersize=6, zorder=5, label=r'$(a, f(a))$')
ax.plot(b, f_b, 'go', markersize=6, zorder=5, label=r'$(b, f(b))$')
ax.plot(c, f_c, 'mo', markersize=6, zorder=5, label=r'$(c, f(c))$')

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

# Légende
plt.legend(fontsize=10, loc='upper right')

plt.savefig('theoreme_rolle.png', dpi=300, bbox_inches='tight')
print("✓ Graphe généré : theoreme_rolle.png")
plt.show()

