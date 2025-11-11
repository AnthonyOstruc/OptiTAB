import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonction pour illustrer le TAF : f(x) = x^3 - 3x + 2
def f(x):
    return x**3 - 3*x + 2

def f_prime(x):
    return 3*x**2 - 3

# Intervalle [a, b]
a = -1.5
b = 2.5

# Calcul des valeurs
f_a = f(a)
f_b = f(b)
coeff_corde = (f_b - f_a) / (b - a)

# On cherche c tel que f'(c) = coeff_corde
# f'(c) = 3c^2 - 3 = coeff_corde
# 3c^2 = coeff_corde + 3
# c^2 = (coeff_corde + 3) / 3
# On prend la solution dans ]a, b[
c_squared = (coeff_corde + 3) / 3
c = np.sqrt(c_squared)  # On prend la solution positive dans l'intervalle
if c < a or c > b:
    c = -np.sqrt(c_squared)  # Si la positive n'est pas dans l'intervalle, prendre la négative

f_c = f(c)

# Intervalle pour la fonction (même template que graphe_exponentielle)
x = np.linspace(-20, 20, 1000)

# Courbe
plt.plot(x, f(x), 'b-', linewidth=2, label=r'$f(x)$')

# Tracer la corde entre (a, f(a)) et (b, f(b))
plt.plot([a, b], [f_a, f_b], 'r--', linewidth=2, label=r'Corde entre $f(a)$ et $f(b)$', alpha=0.8)

# Tracer la tangente en C (parallèle à la corde)
x_tangent = np.linspace(-20, 20, 200)
y_tangent = f_prime(c) * (x_tangent - c) + f_c
plt.plot(x_tangent, y_tangent, 'g--', linewidth=2, label=r'Tangente en $c$', alpha=0.8)

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

plt.savefig('theoreme_accroissements_finis.png', dpi=300, bbox_inches='tight')
print("✓ Graphe généré : theoreme_accroissements_finis.png")
plt.show()
