import numpy as np
import matplotlib.pyplot as plt

# ============================
# Points du triangle
# ============================

A = (0, 0)
B = (3, 4)
C = (-4, 3)

# Coordonnées pour tracer le triangle ABC
x_tri = [A[0], B[0], C[0], A[0]]
y_tri = [A[1], B[1], C[1], A[1]]

# ============================
# Droite (AB) : y = (4/3)x
# ============================

x_line = np.linspace(-6, 6, 400)
y_line = (4/3) * x_line

# ============================
# Cercle circonscrit au triangle ABC
# (triangle rectangle en A, donc centre = milieu de [BC])
# ============================

center = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
radius = np.sqrt((B[0] - C[0])**2 + (B[1] - C[1])**2) / 2

theta = np.linspace(0, 2 * np.pi, 400)
x_circ = center[0] + radius * np.cos(theta)
y_circ = center[1] + radius * np.sin(theta)

# ============================
# Parabole P passant par A, B et C
# y = ax^2 + bx + c
# (ici : a = 25/84, b = 37/84, c = 0)
# ============================

a = 25 / 84
b = 37 / 84
c_par = 0

x_par = np.linspace(-6, 6, 400)
y_par = a * x_par**2 + b * x_par + c_par

# ============================
# Tracé de la figure
# ============================

plt.figure(figsize=(7, 7))

# Triangle
plt.plot(x_tri, y_tri, label="Triangle ABC")

# Droite (AB)
plt.plot(x_line, y_line, linestyle='--', label="Droite (AB)")

# Cercle circonscrit
plt.plot(x_circ, y_circ, label="Cercle circonscrit à ABC")

# Parabole
plt.plot(x_par, y_par, label="Parabole P")

# Points
plt.scatter(*A, zorder=4)
plt.scatter(*B, zorder=4)
plt.scatter(*C, zorder=4)
plt.scatter(*center, zorder=4)

# Étiquettes des points (légèrement décalées pour ne pas toucher les lignes)
plt.text(A[0] - 0, A[1] - 0.3, "A(0,0)", zorder=5, fontsize=8)
plt.text(B[0] + 0.2, B[1] + 0, "B(3,4)", zorder=5, fontsize=8)
plt.text(C[0] - 0, C[1] + 0.2, "C(-4,3)", zorder=5, fontsize=8)
plt.text(center[0] + 0.15, center[1] + 0.25, "Ω(-0.5,3.5)", zorder=5, fontsize=8)

# Axes, repère et mise en forme
plt.axhline(0, linewidth=0.5)
plt.axvline(0, linewidth=0.5)
plt.xlim(-6, 6)
plt.ylim(-2, 8)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.legend(loc='upper right')


plt.xlabel("x")
plt.ylabel("y")

plt.show()
