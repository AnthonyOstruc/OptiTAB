import numpy as np
import matplotlib.pyplot as plt

def add_parallel_marks(ax, P, Q, n=2, size=0.22, spacing=0.28, color=None, lw=2):
    """Dessine n marques // sur le segment PQ."""
    P = np.array(P, dtype=float)
    Q = np.array(Q, dtype=float)
    v = Q - P
    L = np.linalg.norm(v)
    if L == 0:
        return
    u = v / L
    perp = np.array([-u[1], u[0]])

    mid = (P + Q) / 2
    total = spacing * (n - 1)
    ts = [0.0] if n == 1 else np.linspace(-total / 2, total / 2, n)

    for t in ts:
        center = mid + t * u
        a = center - (size / 2) * perp
        b = center + (size / 2) * perp
        ax.plot([a[0], b[0]], [a[1], b[1]], linewidth=lw, color=color)

# --- Thalès dans un triangle : version pédagogique (couleur légère) ---
A = np.array([0.0, 0.0])
B = np.array([6.0, 0.0])

# C placé "comme avant" : sur une demi-droite inclinée (55°)
theta = np.deg2rad(55)
AC_len = 5.0
C = A + AC_len * np.array([np.cos(theta), np.sin(theta)])

# B' sur [AB] et C' sur [AC] avec le même rapport => B'C' // BC
k = 0.60
Bp = A + k * (B - A)
Cp = A + k * (C - A)

fig, ax = plt.subplots(figsize=(9, 5.5))

# Couleurs "pas trop" (2 couleurs max)
big_col = "tab:blue"     # grand triangle
small_col = "tab:orange" # petit triangle (A, B', C')

# Grand triangle ABC
ax.plot([A[0], B[0], C[0], A[0]],
        [A[1], B[1], C[1], A[1]],
        linewidth=2.2, color=big_col)

# Petit triangle AB'C' (mise en évidence)
ax.plot([A[0], Bp[0]], [A[1], Bp[1]], linewidth=3.0, color=small_col)
ax.plot([A[0], Cp[0]], [A[1], Cp[1]], linewidth=3.0, color=small_col)
ax.plot([Bp[0], Cp[0]], [Bp[1], Cp[1]], linewidth=3.0, color=small_col)

# Marques // pour indiquer le parallélisme
neutral = "0.25"
add_parallel_marks(ax, B, C, n=2, color=neutral, lw=2.2)
add_parallel_marks(ax, Bp, Cp, n=2, color=neutral, lw=2.2)

# Points
ax.scatter([A[0]], [A[1]], s=95, zorder=3, color="0.1")
ax.scatter([B[0], C[0]], [B[1], C[1]], s=80, zorder=3, color=big_col)
ax.scatter([Bp[0], Cp[0]], [Bp[1], Cp[1]], s=70, zorder=3, color=small_col)

# Labels (décalés)
labels = [(A, r"$A$", (-18, -18)),
          (B, r"$B$", (10, -18)),
          (C, r"$C$", (10, 1)),
          (Bp, r"$B'$", (10, -18)),
          (Cp, r"$C'$", (10, 1))]
for p, lab, (dx, dy) in labels:
    ax.annotate(lab, (p[0], p[1]),
                textcoords="offset points", xytext=(dx, dy),
                fontsize=13)

# Sans axes, sans titre
pts = np.vstack([A, B, C, Bp, Cp])
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(pts[:, 0].min() - 1, pts[:, 0].max() + 1.2)
ax.set_ylim(pts[:, 1].min() - 1, pts[:, 1].max() + 1.2)
ax.axis('off')

plt.show()
