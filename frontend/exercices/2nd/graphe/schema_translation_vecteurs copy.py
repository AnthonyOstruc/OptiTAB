import matplotlib.pyplot as plt
import numpy as np

# Points donnés
A = np.array([1, -2])
B = np.array([4, 1])
C = np.array([-2, 3])

# Construction : CD = AB  =>  D = C + (B - A)
AB = B - A
D = C + AB

# AE = 0  =>  E = A
E = A.copy()

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_aspect("equal", adjustable="box")
ax.grid(True)

# Points
ax.scatter([A[0], B[0], C[0], D[0]], [A[1], B[1], C[1], D[1]])
ax.scatter([E[0]], [E[1]])  # E = A (superposé)

# Fonction pour écrire un texte décalé
def label_point(P, text, dx=8, dy=8):
    ax.annotate(
        text,
        xy=(P[0], P[1]),
        xytext=(dx, dy),
        textcoords="offset points",
        ha="left",
        va="bottom",
    )

# Labels (tu peux changer dx,dy si ça chevauche)
label_point(A, "A(1 ; -2)", dx=8, dy=-18)
label_point(B, "B(4 ; 1)", dx=8, dy=8)
label_point(C, "C(-2 ; 3)", dx=8, dy=8)
label_point(D, "D(1 ; 6)", dx=8, dy=8)
label_point(E, "E = A", dx=-45, dy=-18)

# Flèches (vecteurs)
def arrow(P, Q):
    v = Q - P
    ax.arrow(
        P[0], P[1], v[0], v[1],
        length_includes_head=True,
        head_width=0.20,
        head_length=0.30,
        linewidth=1.5,
    )

# Vecteurs demandés
arrow(A, B)  # AB
arrow(C, D)  # CD
arrow(B, A)  # BA

# Texte des vecteurs (près du milieu)
def label_vec(P, Q, text, dx=6, dy=6):
    M = (P + Q) / 2
    ax.annotate(
        text,
        xy=(M[0], M[1]),
        xytext=(dx, dy),
        textcoords="offset points",
        ha="left",
        va="bottom",
    )

label_vec(A, B, r"$\overrightarrow{AB}$", dx=8, dy=8)
label_vec(C, D, r"$\overrightarrow{CD}$", dx=8, dy=8)
label_vec(B, A, r"$\overrightarrow{BA}$", dx=8, dy=-16)

# Axes passant par l'origine
ax.axhline(0, linewidth=1)
ax.axvline(0, linewidth=1)

# Limites + graduations
xs = np.array([A[0], B[0], C[0], D[0]])
ys = np.array([A[1], B[1], C[1], D[1]])
m = 2
ax.set_xlim(xs.min() - m, xs.max() + m)
ax.set_ylim(ys.min() - m, ys.max() + m)

ax.set_xticks(np.arange(np.floor(ax.get_xlim()[0]), np.ceil(ax.get_xlim()[1]) + 1, 1))
ax.set_yticks(np.arange(np.floor(ax.get_ylim()[0]), np.ceil(ax.get_ylim()[1]) + 1, 1))

ax.set_xlabel("x")
ax.set_ylabel("y")

plt.tight_layout()
plt.show()
