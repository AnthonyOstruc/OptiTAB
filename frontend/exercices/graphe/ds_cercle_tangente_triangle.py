import numpy as np
import matplotlib.pyplot as plt

# ============================
# Données du problème
# ============================

# Cercle C : x^2 + y^2 - 6x + 4y - 12 = 0
# <=> (x - 3)^2 + (y + 2)^2 = 25
center = (3, -2)
radius = 5

theta = np.linspace(0, 2 * np.pi, 400)
x_c = center[0] + radius * np.cos(theta)
y_c = center[1] + radius * np.sin(theta)

# Points
A = (8, -2)        # point du cercle et sommet du triangle
B = (3, 5)
C = (1, -3)

# Triangle ABC
x_tri = [A[0], B[0], C[0], A[0]]
y_tri = [A[1], B[1], C[1], A[1]]

# Tangente au cercle en A (le rayon est horizontal, donc tangente verticale)
x_tan = np.full(400, A[0])
y_tan = np.linspace(-7, 10, 400)

# Droite (BC) : y = 4x - 7
x_bc = np.linspace(-3, 10, 400)
y_bc = 4 * x_bc - 7

# Hauteur issue de A, perpendiculaire à (BC)
# (BC) : pente 4 -> hauteur : pente -1/4, passant par A(8,-2)
# équation : y = -1/4 x
x_hauteur = np.linspace(-3, 10, 400)
y_hauteur = -0.25 * x_hauteur

# Pied de la hauteur H (intersection hauteur / BC)
# -x/4 = 4x - 7  =>  17x = 28  =>  x = 28/17
xH = 28 / 17
yH = -xH / 4
H = (xH, yH)

# Parabole f(x) = -x^2 + 4x + 5
x_par = np.linspace(-3, 10, 400)
y_par = -x_par**2 + 4 * x_par + 5

# Sommet S de la parabole
xS = 2
yS = -xS**2 + 4 * xS + 5
S = (xS, yS)

# ============================
# Tracé
# ============================

plt.figure(figsize=(7, 7))

# Cercle
plt.plot(x_c, y_c, label="Cercle C")

# Tangente en A
plt.plot(x_tan, y_tan, linestyle='--', label="Tangente en A")

# Triangle ABC
plt.plot(x_tri, y_tri, label="Triangle ABC")

# Droite (BC)
plt.plot(x_bc, y_bc, linestyle='-.', label="Droite (BC)")

# Hauteur issue de A (droite entière + segment AH)
plt.plot(x_hauteur, y_hauteur, linestyle=':', label="Hauteur issue de A")
plt.plot([A[0], H[0]], [A[1], H[1]])  # segment AH

# Parabole
plt.plot(x_par, y_par, label="Parabole f(x) = -x² + 4x + 5")

# Points principaux
for P in [A, B, C, center, H, S]:
    plt.scatter(*P, zorder=5)

# Étiquettes des points (texte plus petit + léger décalage)
plt.text(A[0] + 0.1, A[1] + 0.3, "A(8,-2)", zorder=6, fontsize=8)
plt.text(B[0] -2.2, B[1] -0.2, "B(3,5)", zorder=6, fontsize=8)
plt.text(C[0] + 0.1, C[1] - 0.6, "C(1,-3)", zorder=6, fontsize=8)
plt.text(center[0] + 0, center[1] +0.3, "Ω(3,-2)", zorder=6, fontsize=8)
plt.text(H[0] + 0.1, H[1] - 0.9, "H", zorder=6, fontsize=8)
plt.text(S[0] + 0.1, S[1] + 0.3, "S(2,9)", zorder=6, fontsize=8)

# Axes et mise en forme
plt.axhline(0, linewidth=0.5)
plt.axvline(0, linewidth=0.5)
plt.xlim(-5, 25)
plt.ylim(-10, 12)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.legend(loc='upper right')


plt.xlabel("x")
plt.ylabel("y")

plt.show()
