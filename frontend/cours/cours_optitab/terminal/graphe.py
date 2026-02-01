import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_aspect("equal")
ax.axis("off")

# Origine
O = np.array([0, 0])

# Vecteurs
u1 = np.array([2, 1])
u2 = np.array([1, 2])
a1 = 1.0
a2 = 1.0

# Calculs
a1_u1 = a1 * u1
a2_u2 = a2 * u2
v = a1_u1 + a2_u2

# Points
B = O + a1_u1
D = O + v

def draw_arrow(ax, start, end, color="k", linestyle='-'):
    x0, y0 = start
    x1, y1 = end
    dx, dy = x1 - x0, y1 - y0
    
    if linestyle == '-':
        ax.arrow(
            x0, y0, dx, dy,
            length_includes_head=True,
            head_width=0.08,
            head_length=0.15,
            color=color,
            linewidth=2
        )
    else:
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=2, linestyle=linestyle)
        angle = np.arctan2(dy, dx)
        arrow_length = 0.15
        arrow_width = 0.08
        ax.arrow(
            x1 - arrow_length * np.cos(angle),
            y1 - arrow_length * np.sin(angle),
            arrow_length * np.cos(angle),
            arrow_length * np.sin(angle),
            head_width=arrow_width,
            head_length=arrow_length,
            fc=color,
            ec=color,
            linewidth=0
        )

# Vecteur u1 (base) - en pointillés
draw_arrow(ax, O, O + u1, color="tab:blue", linestyle='--')
# Vecteur u2 (base) - en pointillés
draw_arrow(ax, O, O + u2, color="tab:purple", linestyle='--')
# a1*u1
draw_arrow(ax, O, B, color="tab:green")
# a2*u2
draw_arrow(ax, B, D, color="tab:orange")
# Vecteur résultant v
draw_arrow(ax, O, D, color="tab:red")

# Légende
legend_elements = [
    Line2D([0], [0], color='tab:blue', linewidth=1, linestyle='--', label=r'$\vec{u_1}$ (vecteur de base)'),
    Line2D([0], [0], color='tab:purple', linewidth=1, linestyle='--', label=r'$\vec{u_2}$ (vecteur de base)'),
    Line2D([0], [0], color='tab:green', linewidth=1, label=f'${a1}\\vec{{u_1}}$'),
    Line2D([0], [0], color='tab:orange', linewidth=1, label=f'${a2}\\vec{{u_2}}$'),
    Line2D([0], [0], color='tab:red', linewidth=1, label=f'$\\vec{{v}} = {a1}\\vec{{u_1}} + {a2}\\vec{{u_2}}$')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.95, edgecolor='gray')

ax.set_xlim(-0.5, 4)
ax.set_ylim(-0.5, 4)

plt.tight_layout()
plt.savefig("combinaison_lineaire.png", dpi=300, bbox_inches="tight", facecolor='white')
print("Graphique sauvegardé sous 'combinaison_lineaire.png'")
plt.show()
