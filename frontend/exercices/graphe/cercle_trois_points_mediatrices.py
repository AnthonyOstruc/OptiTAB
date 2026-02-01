import numpy as np
import matplotlib.pyplot as plt

# ============================
# Points du triangle
# ============================

A = (1, 3)
B = (5, 1)
C = (3, -1)

# Coordonnées pour tracer le triangle ABC
x_tri = [A[0], B[0], C[0], A[0]]
y_tri = [A[1], B[1], C[1], A[1]]

# ============================
# Médiatrice m1 du segment [AB]
# ============================

# Milieu de [AB]
Mx1 = (A[0] + B[0]) / 2
My1 = (A[1] + B[1]) / 2
M1 = (Mx1, My1)

# Pente de (AB)
m_AB = (B[1] - A[1]) / (B[0] - A[0])   # = -1/2
# Pente de la médiatrice m1 (perpendiculaire)
m_m1 = 2.0                             # inverse négative de -1/2

x_m1 = np.linspace(-1, 7, 400)
y_m1 = m_m1 * (x_m1 - Mx1) + My1

# ============================
# Médiatrice m2 du segment [AC]
# ============================

Mx2 = (A[0] + C[0]) / 2
My2 = (A[1] + C[1]) / 2
M2 = (Mx2, My2)

m_AC = (C[1] - A[1]) / (C[0] - A[0])   # = -2
m_m2 = 0.5                             # inverse négative de -2

x_m2 = np.linspace(-1, 7, 400)
y_m2 = m_m2 * (x_m2 - Mx2) + My2

# ============================
# Centre Ω du cercle circonscrit
# ============================

# Écriture sous forme y = ax + b
b1 = My1 - m_m1 * Mx1
b2 = My2 - m_m2 * Mx2
# 2x + b1 = 0.5x + b2  =>  1.5x = b2 - b1
xO = (b2 - b1) / 1.5
yO = m_m1 * xO + b1
Omega = (xO, yO)          # ≈ (8/3 , 4/3)

# Rayon du cercle circonscrit
radius = np.sqrt((Omega[0] - A[0])**2 + (Omega[1] - A[1])**2)

theta = np.linspace(0, 2 * np.pi, 400)
x_circ = Omega[0] + radius * np.cos(theta)
y_circ = Omega[1] + radius * np.sin(theta)

# ============================
# Tracé
# ============================

plt.figure(figsize=(7, 7))

# Triangle
plt.plot(x_tri, y_tri, label="Triangle ABC")

# Médiatrices
plt.plot(x_m1, y_m1, linestyle='--', label="Médiatrice m1 de [AB]")
plt.plot(x_m2, y_m2, linestyle='-.', label="Médiatrice m2 de [AC]")

# Cercle circonscrit
plt.plot(x_circ, y_circ, label="Cercle circonscrit")

# Points
for P in [A, B, C, M1, M2, Omega]:
    plt.scatter(*P, zorder=5)

# Étiquettes des points (texte plus petit, légèrement décalé)
plt.text(A[0] + 0.15, A[1] - 0, "A(1,3)", zorder=6, fontsize=8)
plt.text(B[0] + 0.1, B[1] - 0.4, "B(5,1)", zorder=6, fontsize=8)
plt.text(C[0] + 0.1, C[1] - 0.4, "C(3,-1)", zorder=6, fontsize=8)
plt.text(M1[0] + 0.15, M1[1] + 0.1, "M1", zorder=6, fontsize=8)
plt.text(M2[0] - 0, M2[1] + 0.2, "M2", zorder=6, fontsize=8)
plt.text(Omega[0] + 0.1, Omega[1] - 0.2,
         f"Ω({Omega[0]:.1f},{Omega[1]:.1f})", zorder=6, fontsize=8)

# Axes et mise en forme
plt.axhline(0, linewidth=0.5)
plt.axvline(0, linewidth=0.5)
plt.xlim(-1, 7)
plt.ylim(-3, 5)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.legend(loc='upper right')


plt.xlabel("x")
plt.ylabel("y")

plt.show()
