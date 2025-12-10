import numpy as np
import matplotlib.pyplot as plt

# ============================
# Données
# ============================

# Cercle C : centre Ω(1,2), rayon R = 3
center = (1, 2)
radius = 3

theta = np.linspace(0, 2 * np.pi, 400)
x_c = center[0] + radius * np.cos(theta)
y_c = center[1] + radius * np.sin(theta)

# Droite Δ : x + y - 4 = 0  <=>  y = 4 - x
x_line = np.linspace(-3, 7, 400)
y_line = 4 - x_line

# ============================
# Points d'intersection C ∩ Δ
# ============================

# Résolution analytique :
# (x - 1)^2 + (y - 2)^2 = 9 et y = 4 - x
# => x = (3 ± sqrt(17)) / 2, y = 4 - x
sqrt17 = np.sqrt(17)
x1 = (3 + sqrt17) / 2
y1 = 4 - x1
x2 = (3 - sqrt17) / 2
y2 = 4 - x2
P = (x1, y1)
Q = (x2, y2)

# ============================
# Pied H de la perpendiculaire du centre Ω à Δ
# ============================

# Droite Δ : x + y - 4 = 0  => a = 1, b = 1, c = -4
a = 1
b = 1
c = -4
x0, y0 = center
val = a * x0 + b * y0 + c
den = a**2 + b**2

xH = x0 - a * val / den
yH = y0 - b * val / den
H = (xH, yH)

# ============================
# Tracé
# ============================

plt.figure(figsize=(7, 7))

# Cercle C
plt.plot(x_c, y_c, label="Cercle C")

# Droite Δ
plt.plot(x_line, y_line, linestyle='--', label="Droite Δ : x + y - 4 = 0")

# Segment perpendiculaire ΩH
plt.plot([center[0], H[0]], [center[1], H[1]], linestyle=':', label="Distance d (Ω, Δ)")

# Points importants
for Pnt in [center, H, P, Q]:
    plt.scatter(*Pnt, zorder=5)

# Étiquettes (petite taille, légèrement décalées pour ne pas toucher les lignes)
plt.text(center[0] + 0.1, center[1] - 0.1, "Ω(1,2)", zorder=6, fontsize=8)
plt.text(H[0] + 0.1, H[1] - 0, "H", zorder=6, fontsize=8)
plt.text(P[0] + 0.15, P[1] + 0, "P", zorder=6, fontsize=8)
plt.text(Q[0] - 0.1, Q[1] - 0.3, "Q", zorder=6, fontsize=8)

# Axes et mise en forme
plt.axhline(0, linewidth=0.5)
plt.axvline(0, linewidth=0.5)
plt.xlim(-3, 7)
plt.ylim(-3, 7)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.legend(loc='upper right')


plt.xlabel("x")
plt.ylabel("y")

plt.show()
