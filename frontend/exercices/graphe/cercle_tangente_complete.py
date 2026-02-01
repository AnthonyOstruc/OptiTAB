import numpy as np
import matplotlib.pyplot as plt

# ============================
# Données
# ============================

# Cercle C : x^2 + y^2 - 4x + 2y - 20 = 0
# <=> (x - 2)^2 + (y + 1)^2 = 25
center = (2, -1)
radius = 5

theta = np.linspace(0, 2 * np.pi, 400)
x_c = center[0] + radius * np.cos(theta)
y_c = center[1] + radius * np.sin(theta)

# Point A(7,-1) sur le cercle
A = (7, -1)

# Point M(7,4) extérieur
M = (7, 4)

# Tangente T au cercle en A
# Rayon ΩA horizontal => tangente verticale : x = 7
x_tan = np.full(400, A[0])
y_tan = np.linspace(-7, 9, 400)

# Segment ΩA (rayon)
x_OA = [center[0], A[0]]
y_OA = [center[1], A[1]]

# Segment ΩM (distance du centre au point M)
x_OM = [center[0], M[0]]
y_OM = [center[1], M[1]]

# ============================
# Tracé
# ============================

plt.figure(figsize=(7, 7))

# Cercle C
plt.plot(x_c, y_c, label="Cercle C")

# Tangente T
plt.plot(x_tan, y_tan, linestyle='--', label="Tangente T en A")

# Segments ΩA et ΩM
plt.plot(x_OA, y_OA, linestyle=':', label="Rayon ΩA")
plt.plot(x_OM, y_OM, linestyle='-.', label="Distance ΩM")

# Points importants
for P in [center, A, M]:
    plt.scatter(*P, zorder=5)

# Étiquettes (texte plus petit, légèrement décalé pour ne pas toucher les lignes)
plt.text(center[0] + 0.1, center[1] - 0.5, "Ω(2,-1)", zorder=6, fontsize=8)
plt.text(A[0] + 0.2, A[1] - 0.5, "A(7,-1)", zorder=6, fontsize=8)
plt.text(M[0] + 0.2, M[1] + 0.2, "M(7,4)", zorder=6, fontsize=8)

# Axes et mise en forme
plt.axhline(0, linewidth=0.5)
plt.axvline(0, linewidth=0.5)
plt.xlim(-4, 12)
plt.ylim(-7, 9)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.legend(loc='upper right')


plt.xlabel("x")
plt.ylabel("y")

plt.show()
