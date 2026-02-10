import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(9, 4.6), dpi=160)
ax = fig.add_subplot(111)

# Points (exemple générique)
M  = np.array([1.2, 1.1])
Mp = np.array([6.2, 3.2])
u  = Mp - M

# Un autre point pour montrer que la même translation s'applique à tout point P -> P'
P  = np.array([2.0, 4.1])
Pp = P + u

# Points
ax.scatter([M[0], Mp[0], P[0], Pp[0]],
           [M[1], Mp[1], P[1], Pp[1]], s=40)

# Flèches (même vecteur)
arrow_kw = dict(arrowstyle="->", lw=2)
ax.annotate("", xy=Mp, xytext=M,  arrowprops=arrow_kw)
ax.annotate("", xy=Pp, xytext=P,  arrowprops=arrow_kw)

# Labels (décalés pour ne pas toucher les traits)
def label_point(Pt, text, dx=0.12, dy=0.15, ha="left", va="bottom"):
    ax.text(Pt[0] + dx, Pt[1] + dy, text, fontsize=13, ha=ha, va=va)

label_point(M,  r"$M$",  dx=-0.15, dy=-0.22, ha="right", va="top")
label_point(Mp, r"$M'$", dx= 0.15, dy=-0.22, ha="left",  va="top")
label_point(P,  r"$P$",  dx=-0.15, dy= 0.18, ha="right", va="bottom")
label_point(Pp, r"$P'$", dx= 0.15, dy= 0.18, ha="left",  va="bottom")

# Label du vecteur u (décalé perpendiculairement à la flèche)
mid  = (M + Mp) / 2
perp = np.array([-u[1], u[0]])
perp = perp / (np.linalg.norm(perp) + 1e-9) * 0.35
ax.text(mid[0] + perp[0], mid[1] + perp[1],
        r"$\vec{u}=\overrightarrow{MM'}$", fontsize=13,
        ha="center", va="center")

# Mise en forme
ax.set_xlim(0, 7.5)
ax.set_ylim(0, 5.5)
ax.set_aspect("equal", adjustable="box")
ax.set_xticks(np.arange(0, 7.6, 1))
ax.set_yticks(np.arange(0, 5.6, 1))
ax.grid(True, linewidth=0.6, alpha=0.25)

for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

ax.text(0.0, 5.65, "Translation associée au vecteur", fontsize=13,
        ha="left", va="bottom")

# Exports
fig.savefig("graphe_definition_vecteur.png", bbox_inches="tight")
fig.savefig("graphe_definition_vecteur.svg", bbox_inches="tight")
plt.show()
