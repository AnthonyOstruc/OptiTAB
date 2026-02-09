import numpy as np
import matplotlib.pyplot as plt

# ---------- helpers ----------
def parallel_marks(ax, P, Q, n=2, size=0.22, spacing=0.30, color="0.25", lw=2):
    """Draw n small parallel marks (//) across segment PQ."""
    P = np.array(P, float); Q = np.array(Q, float)
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
        c = mid + t * u
        a = c - (size / 2) * perp
        b = c + (size / 2) * perp
        ax.plot([a[0], b[0]], [a[1], b[1]], linewidth=lw, color=color)

def tick(ax, P, Q, pos=0.5, size=0.22, color="0.25", lw=2):
    """Small tick mark across segment PQ at relative position pos."""
    P = np.array(P, float); Q = np.array(Q, float)
    v = Q - P
    L = np.linalg.norm(v)
    if L == 0:
        return
    u = v / L
    perp = np.array([-u[1], u[0]])
    c = P + pos * v
    a = c - (size / 2) * perp
    b = c + (size / 2) * perp
    ax.plot([a[0], b[0]], [a[1], b[1]], linewidth=lw, color=color)

def label(ax, txt, p, dx, dy, fs=13, color="0.12"):
    ax.annotate(txt, (p[0], p[1]),
                textcoords="offset points", xytext=(dx, dy),
                fontsize=fs, color=color)

def setup_ax(ax, pts, pad=(1.0, 1.0)):
    pts = np.asarray(pts)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(pts[:, 0].min() - pad[0], pts[:, 0].max() + pad[0])
    ax.set_ylim(pts[:, 1].min() - pad[1], pts[:, 1].max() + pad[1])
    ax.axis('off')

def hollow_points(ax, pts, s=70, edge="0.15", lw=2):
    """White-filled points with outline."""
    pts = np.asarray(pts)
    if np.isscalar(s):
        ax.scatter(pts[:, 0], pts[:, 1], s=s, facecolors="white",
                   edgecolors=edge, linewidths=lw, zorder=3)
    else:
        for (x, y), si in zip(pts, s):
            ax.scatter([x], [y], s=si, facecolors="white",
                       edgecolors=edge, linewidths=lw, zorder=3)

# ---------- colors (bleu/orange, pas trop) ----------
c_main = "tab:blue"
c_aux  = "tab:orange"
c_mark = "0.25"
c_edge = "0.15"

# ---------- figure ----------
fig, axes = plt.subplots(1, 3, figsize=(15, 5.2))

# =========================================================
# 1) Cas général (papillon) : 2 sécantes + 2 parallèles
#    Modèle : points A,B,C,D,E
# =========================================================
ax = axes[0]
A = np.array([0.0, 0.0])

v1 = np.array([1.0, 0.85])     # sécante (B-A-D)
v2 = np.array([1.0, -1.15])    # sécante (E-A-C)

m = -0.22
b_top = 2.2
b_bot = -1.6

def intersect_with_parallel(v, b):
    denom = (v[1] - m * v[0])
    t = b / denom
    return t * v

D = intersect_with_parallel(v1, b_top)
B = intersect_with_parallel(v1, b_bot)
E = intersect_with_parallel(v2, b_top)
C = intersect_with_parallel(v2, b_bot)

# sécantes (bleu)
t_ext = 1.25
p1a, p1b = t_ext * B, t_ext * D
p2a, p2b = t_ext * E, t_ext * C
ax.plot([p1a[0], p1b[0]], [p1a[1], p1b[1]], linewidth=2.4, color=c_main)
ax.plot([p2a[0], p2b[0]], [p2a[1], p2b[1]], linewidth=2.4, color=c_main)

# parallèles (orange)
xs = np.array([B[0], C[0], D[0], E[0]])
x_min, x_max = xs.min() - 1.1, xs.max() + 1.1
y_line = lambda x, b: m * x + b
ax.plot([x_min, x_max], [y_line(x_min, b_top), y_line(x_max, b_top)], linewidth=2.8, color=c_aux)
ax.plot([x_min, x_max], [y_line(x_min, b_bot), y_line(x_max, b_bot)], linewidth=2.8, color=c_aux)

# marques // sur les parallèles
parallel_marks(ax, E, D, n=2, color=c_mark, lw=2.0)
parallel_marks(ax, B, C, n=2, color=c_mark, lw=2.0)

pts1 = np.vstack([A, B, C, D, E])
hollow_points(ax, pts1, s=75, edge=c_edge, lw=2.2)
label(ax, "A", A,  10,  -7)
label(ax, "B", B,  -8, -18)
label(ax, "C", C,  -5, -20)
label(ax, "D", D,  15,   0)
label(ax, "E", E,   0,   6)
setup_ax(ax, pts1, pad=(1.2, 1.2))

# =========================================================
# 2) Triangle + droite parallèle : A,B,C,B',C'
# =========================================================
ax = axes[1]
A = np.array([0.0, 0.0])
B = np.array([6.0, 0.0])
C = A + 5.0 * np.array([np.cos(np.deg2rad(55)), np.sin(np.deg2rad(55))])

k = 0.60
Bp = A + k * (B - A)
Cp = A + k * (C - A)

# grand triangle (bleu)
ax.plot([A[0], B[0], C[0], A[0]],
        [A[1], B[1], C[1], A[1]], linewidth=2.2, color=c_main)

# petit triangle AB'C' (orange)
ax.plot([A[0], Bp[0]], [A[1], Bp[1]], linewidth=3.0, color=c_aux)
ax.plot([A[0], Cp[0]], [A[1], Cp[1]], linewidth=3.0, color=c_aux)
ax.plot([Bp[0], Cp[0]], [Bp[1], Cp[1]], linewidth=3.0, color=c_aux)

parallel_marks(ax, B, C,  n=2, color=c_mark, lw=2.0)
parallel_marks(ax, Bp, Cp, n=2, color=c_mark, lw=2.0)

pts2 = np.vstack([A, B, C, Bp, Cp])
hollow_points(ax, pts2, s=[80, 75, 75, 70, 70], edge=c_edge, lw=2.2)
label(ax, "A",  A,  -18, -18)
label(ax, "B",  B,   10, -18)
label(ax, "C",  C,   10,   0)
label(ax, "B'", Bp,  10, -18)
label(ax, "C'", Cp,  10,   0)
setup_ax(ax, pts2, pad=(1.0, 1.0))

# =========================================================
# 3) Droite des milieux : B' et C' milieux + segment // BC
# =========================================================
ax = axes[2]
A = np.array([0.0, 0.0])
B = np.array([6.0, 0.0])
C = A + 5.0 * np.array([np.cos(np.deg2rad(55)), np.sin(np.deg2rad(55))])

Bp = (A + B) / 2
Cp = (A + C) / 2

# grand triangle (bleu)
ax.plot([A[0], B[0], C[0], A[0]],
        [A[1], B[1], C[1], A[1]], linewidth=2.2, color=c_main)

# segment des milieux (orange)
ax.plot([Bp[0], Cp[0]], [Bp[1], Cp[1]], linewidth=3.0, color=c_aux)

parallel_marks(ax, B, C,  n=2, color=c_mark, lw=2.0)
parallel_marks(ax, Bp, Cp, n=2, color=c_mark, lw=2.0)

# marques d'égalité sur AB et AC
tick(ax, A, Bp, pos=0.65, size=0.22, color=c_mark, lw=2.0)
tick(ax, Bp, B, pos=0.35, size=0.22, color=c_mark, lw=2.0)
tick(ax, A, Cp, pos=0.65, size=0.22, color=c_mark, lw=2.0)
tick(ax, Cp, C, pos=0.35, size=0.22, color=c_mark, lw=2.0)

pts3 = np.vstack([A, B, C, Bp, Cp])
hollow_points(ax, pts3, s=[80, 75, 75, 70, 70], edge=c_edge, lw=2.2)
label(ax, "A",  A,  -18, -18)
label(ax, "B",  B,   10, -18)
label(ax, "C",  C,   10,   0)
label(ax, "B'", Bp,  10, -18)
label(ax, "C'", Cp,  10,   0)
setup_ax(ax, pts3, pad=(1.0, 1.0))

# =========================================================
# Titres AU MÊME NIVEAU (sans savefig) + affichage
# =========================================================
titles = [
    "Cas général (papillon)",
    "Triangle avec droite parallèle",
    "Droite des milieux",
]

plt.tight_layout(w_pad=2.6, rect=[0, 0, 1, 0.90])  # bande en haut pour titres

for ax, title in zip(axes, titles):
    pos = ax.get_position()
    x = (pos.x0 + pos.x1) / 2
    fig.text(x, 0.965, title, ha="center", va="top", fontsize=13, fontweight="bold")

plt.show()
plt.close(fig)
