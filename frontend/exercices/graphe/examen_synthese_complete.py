import numpy as np
import matplotlib.pyplot as plt

# ============================
# Données du problème
# ============================

# Cercle C : x^2 + y^2 - 8x - 6y + 24 = 0
# <=> (x - 4)^2 + (y - 3)^2 = 1
center = (4, 3)
radius = 1

theta = np.linspace(0, 2 * np.pi, 400)
x_c = center[0] + radius * np.cos(theta)
y_c = center[1] + radius * np.sin(theta)

# Points
O = (0, 0)
A = (5, 3)
B = (4, 4)

# Droites et courbes
# Tangente en A : x = 5
x_tan = np.full(400, 5)
y_tan = np.linspace(-1, 8, 400)

# Droite D : y = 0
x_D = np.linspace(-2, 10, 400)
y_D = np.zeros_like(x_D)

# Médiatrice de [AB] : y = x - 1
x_med = np.linspace(-2, 10, 400)
y_med = x_med - 1

# Parabole P : y = -1/4 x^2 + 2x
x_par = np.linspace(-2, 10, 400)
y_par = -0.25 * x_par**2 + 2 * x_par

# ============================
# Tracé
# ============================

plt.figure(figsize=(7, 7))

# Courbes (arrière plan)
plt.plot(x_c, y_c, label="Cercle C")
plt.plot(x_tan, y_tan, linestyle='--', label="Tangente en A")
plt.plot(x_D, y_D, linestyle=':', label="Droite D (y = 0)")
plt.plot(x_med, y_med, linestyle='-.', label="Médiatrice de [AB]")
plt.plot(x_par, y_par, label="Parabole P")

# Points (devant les courbes)
plt.scatter(*O, zorder=4)
plt.scatter(*A, zorder=4)
plt.scatter(*B, zorder=4)
plt.scatter(*center, zorder=4)

# Étiquettes des points (encore plus devant, sans toucher les courbes)
plt.text(O[0] + 0, O[1] - 0.3, "O(0,0)", zorder=5, fontsize=8)
plt.text(A[0] + 0.1, A[1] - 0.25, "A(5,3)", zorder=5, fontsize=8)  # déplacé vers le bas
plt.text(B[0] + 0.1, B[1] + 0.1, "B(4,4)", zorder=5, fontsize=8)
plt.text(center[0] - 0.05, center[1] - 0.4, "Ω(4,3)", zorder=5, fontsize=8)

# Axes et mise en forme
plt.axhline(0, linewidth=0.5)
plt.axvline(0, linewidth=0.5)
plt.xlim(-2, 10)
plt.ylim(-2, 8)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.legend(loc='upper right')


plt.xlabel("x")
plt.ylabel("y")

plt.show()
