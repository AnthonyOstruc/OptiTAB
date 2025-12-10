import numpy as np
import matplotlib.pyplot as plt

# ============================
# Points du quadrilatère
# ============================

A = (1, 1)
B = (5, 2)
C = (4, 6)
D = (0, 5)

# Quadrilatère ABCD fermé
x_quad = [A[0], B[0], C[0], D[0], A[0]]
y_quad = [A[1], B[1], C[1], D[1], A[1]]

# Diagonales AC et BD
x_AC = [A[0], C[0]]
y_AC = [A[1], C[1]]

x_BD = [B[0], D[0]]
y_BD = [B[1], D[1]]

# ============================
# Milieux I de [AC] et J de [BD]
# ============================

Ix = (A[0] + C[0]) / 2
Iy = (A[1] + C[1]) / 2
I = (Ix, Iy)

Jx = (B[0] + D[0]) / 2
Jy = (B[1] + D[1]) / 2
J = (Jx, Jy)

# ============================
# Droite (AC) (prolongement)
# ============================

x_line_AC = np.linspace(-1, 7, 200)
m_AC = (C[1] - A[1]) / (C[0] - A[0])    # pente de AC
b_AC = A[1] - m_AC * A[0]
y_line_AC = m_AC * x_line_AC + b_AC

# ============================
# Tracé
# ============================

plt.figure(figsize=(7, 7))

# Quadrilatère
plt.plot(x_quad, y_quad, label="Quadrilatère ABCD")

# Diagonales
plt.plot(x_AC, y_AC, linestyle='--', label="Diagonale AC")
plt.plot(x_BD, y_BD, linestyle='--', label="Diagonale BD")

# Droite (AC) prolongée
plt.plot(x_line_AC, y_line_AC, linestyle=':', label="Droite (AC)")

# Points A, B, C, D, I, J
for P in [A, B, C, D, I, J]:
    plt.scatter(*P, zorder=5)

# Étiquettes (petite taille, légèrement décalées)
plt.text(A[0] - 0, A[1] - 0.2, "A(1,1)", fontsize=8)
plt.text(B[0] + 0.1, B[1] - 0.1, "B(5,2)", fontsize=8)
plt.text(C[0] + 0.1, C[1] + 0, "C(4,6)", fontsize=8)
plt.text(D[0] - 0, D[1] + 0.15, "D(0,5)", fontsize=8)
plt.text(I[0] + 0, I[1] - 0.3, "I", fontsize=8)
plt.text(J[0] - 0.05, J[1] + 0.2, "J", fontsize=8)

# Axes et repère
plt.axhline(0, linewidth=0.5)
plt.axvline(0, linewidth=0.5)
plt.xlim(-1, 7)
plt.ylim(0, 8)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.legend(loc="upper right", fontsize=8)


plt.xlabel("x")
plt.ylabel("y")

plt.show()
