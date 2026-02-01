import numpy as np
import matplotlib.pyplot as plt

# ============================
# Points du triangle
# ============================

A = (-1, 2)
B = (3, 4)
C = (1, -2)

# Coordonnées pour tracer le triangle ABC
x_tri = [A[0], B[0], C[0], A[0]]
y_tri = [A[1], B[1], C[1], A[1]]

# ============================
# Médiatrice du segment [AB]
# ============================

# Milieu de [AB]
Mx = (A[0] + B[0]) / 2   # = 1
My = (A[1] + B[1]) / 2   # = 3
M = (Mx, My)

# Pente de (AB)
m_AB = (B[1] - A[1]) / (B[0] - A[0])   # (4-2)/(3+1) = 0.5
# Pente de la médiatrice (perpendiculaire)
m_med = -2.0

x_med = np.linspace(-3, 5, 400)
y_med = m_med * (x_med - Mx) + My      # équation de la médiatrice

# ============================
# Cercle circonscrit (triangle rectangle en A)
# ============================

# Pour un triangle rectangle, centre du cercle circonscrit = milieu de l'hypoténuse [BC]
Ox = (B[0] + C[0]) / 2   # = 2
Oy = (B[1] + C[1]) / 2   # = 1
Omega = (Ox, Oy)

# Rayon (distance ΩB ou ΩC)
radius = np.sqrt((Ox - B[0])**2 + (Oy - B[1])**2)

theta = np.linspace(0, 2 * np.pi, 400)
x_circ = Ox + radius * np.cos(theta)
y_circ = Oy + radius * np.sin(theta)

# ============================
# Tracé
# ============================

plt.figure(figsize=(7, 7))

# Triangle
plt.plot(x_tri, y_tri, label="Triangle ABC")

# Médiatrice de [AB]
plt.plot(x_med, y_med, linestyle='--', label="Médiatrice de [AB]")

# Cercle circonscrit
plt.plot(x_circ, y_circ, label="Cercle circonscrit à ABC")

# Points
for P in [A, B, C, M, Omega]:
    plt.scatter(*P, zorder=5)

# Étiquettes (fontsize=8, légèrement décalées pour ne pas toucher les segments)
plt.text(A[0] - 0.65, A[1] + 0.2, "A(-1,2)", zorder=6, fontsize=8)
plt.text(B[0] + 0.1, B[1] + 0.1, "B(3,4)", zorder=6, fontsize=8)
plt.text(C[0] - 0.1, C[1] - 0.4, "C(1,-2)", zorder=6, fontsize=8)
plt.text(M[0] + 0.05, M[1] + 0.15, "M", zorder=6, fontsize=8)
plt.text(Omega[0] + 0.1, Omega[1] + 0.1,
         f"Ω({Omega[0]:.1f},{Omega[1]:.1f})", zorder=6, fontsize=8)

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
