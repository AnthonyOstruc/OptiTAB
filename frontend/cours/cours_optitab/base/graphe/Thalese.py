import numpy as np
import matplotlib.pyplot as plt

# --- Géométrie : configuration de Thalès ---
A = np.array([0.0, 0.0])

# Deux demi-droites sécantes issues de A
ray1_dir = np.array([1.0, 0.0])              # horizontale
ray2_dir = np.array([np.cos(np.deg2rad(55)),  # 55°
                     np.sin(np.deg2rad(55))])

# Points B et C sur chaque demi-droite
AB = 4.0
AC = 3.2
B = A + AB * ray1_dir
C = A + AC * ray2_dir

# On "agrandit" depuis A pour créer B' et C' (assure BC ∥ B'C')
k = 1.7
Bp = A + k * (B - A)
Cp = A + k * (C - A)

# Pour tracer les droites sécantes un peu plus loin
t_max = 1.1
P1_end = A + t_max * (Bp - A)
P2_end = A + t_max * (Cp - A)

# --- Tracé ---
fig, ax = plt.subplots(figsize=(9, 5.5))

# Droites sécantes (d1) et (d2) -> légende
ax.plot([A[0], P1_end[0]], [A[1], P1_end[1]], linewidth=2, label=r'$(d_1)$')
ax.plot([A[0], P2_end[0]], [A[1], P2_end[1]], linewidth=2, label=r'$(d_2)$')

# Segments parallèles BC et B'C'
ax.plot([B[0], C[0]],   [B[1], C[1]],   linewidth=2)
ax.plot([Bp[0], Cp[0]], [Bp[1], Cp[1]], linewidth=2)

# Points
points = {"A": A, "B": B, "C": C, "B'": Bp, "C'": Cp}
for name, p in points.items():
    ax.scatter(p[0], p[1], s=60, zorder=3)

# Décalages des labels pour qu’ils ne touchent pas les lignes
offsets = {
    "A": (-18, -18),
    "B": (10, -14),
    "C": (8, 0),
    "B'": (10, -14),
    "C'": (10, 1),
}
for name, p in points.items():
    dx, dy = offsets[name]
    ax.annotate(name, (p[0], p[1]),
                textcoords="offset points", xytext=(dx, dy),
                fontsize=13)

# Annotation "parallèle" (si tu veux la garder)
ax.annotate("BC ∥ B'C'", ( (Bp[0]+Cp[0])/2, (Bp[1]+Cp[1])/2 ),
            textcoords="offset points", xytext=(14, 12),
            fontsize=12)

# Légende (sans cadre, propre)
ax.legend(
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),  # à droite, centré verticalement
    frameon=False,
    fontsize=12,
    handlelength=2.5
)
plt.tight_layout(rect=[0, 0, 0.85, 1])


# Mise en forme
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(-1, max(P1_end[0], P2_end[0]) + 1.5)
ax.set_ylim(-1, max(P2_end[1], Cp[1]) + 1.5)
ax.axis('off')

plt.show()
