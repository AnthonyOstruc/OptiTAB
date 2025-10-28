import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(16, 10))
ax = plt.gca()

# Fonctions
f1 = lambda x: 2*np.log(x)
f2 = lambda x: np.log(x**2 + 3)

# Domaine x>0
x = np.linspace(0.00000000001, 20, 20000)

# Courbes
plt.plot(x, f1(x), 'b-', linewidth=2, label=r'$y = 2\ln(x)$')
plt.plot(x, f2(x), 'g-', linewidth=2, label=r'$y = \ln(x^2+3)$')

# Asymptote verticale x=0
plt.axvline(x=0, color='red', linestyle='--', linewidth=1.5, label=r'Asymptote $x=0$')

# Indication: pas d'intersection
plt.text(2.5, 6.0, 'Pas de solution (x>0)', color='crimson', fontsize=11)

# Créer un deuxième graphique zoomé
fig2, ax2 = plt.subplots(figsize=(8, 6))

# Courbes zoomées - domaine x > 0
x_zoom = np.linspace(0.01, 4, 2000)
ax2.plot(x_zoom, f1(x_zoom), 'b-', linewidth=2, label=r'$y = 2\ln(x)$')
ax2.plot(x_zoom, f2(x_zoom), 'g-', linewidth=2, label=r'$y = \ln(x^2+3)$')

# Asymptote verticale x=0
ax2.axvline(x=0, color='red', linestyle='--', linewidth=1.5, label=r'Asymptote $x=0$')

# Limites du zoom
ax2.set_xlim(0, 4)
ax2.set_ylim(-3, 4)

# Style du zoom
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=12, loc='upper right')
ax2.set_xlabel('x', fontsize=14)
ax2.set_ylabel('y', fontsize=14)
ax2.set_title('Zoom - Zone d\'intérêt', fontsize=16, pad=20)

# Sauvegarder le zoom
plt.savefig('exercice_logarithme_equations_question5_zoom.png', dpi=300, bbox_inches='tight')
plt.close(fig2)

# Limites/zoom
plt.xlim(-20, 20)
plt.ylim(-20, 20)

# Désactiver ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Tracer les axes avec flèches
ax.annotate("", xy=(20, 0), xytext=(-20, 0),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))
ax.annotate("", xy=(0, 20), xytext=(0, -20),
            arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5))

# Texte "0"
ax.text(-0.8, -1.2, '0', fontsize=12)

# Graduations template
xticks_major = [5, 10, 15, 19]
yticks_major = [5, 10, 15, 19]
for xv in xticks_major:
    ax.plot([xv, xv], [-0.3, 0.3], color="black", linewidth=0.8)
    ax.text(xv, -1.0, str(xv), ha='center', va='top', fontsize=12)
for yv in yticks_major:
    if yv < 19:
        ax.plot([-0.2, 0.2], [yv, yv], color="black", linewidth=0.8)
        ax.text(-1.0, yv, str(yv), ha='right', va='center', fontsize=12)
for xv in range(1, 20):
    if xv not in xticks_major:
        ax.plot([xv, xv], [-0.15, 0.15], color="black", linewidth=0.5)
for yv in range(1, 20):
    if yv not in yticks_major and yv < 19:
        ax.plot([-0.1, 0.1], [yv, yv], color="black", linewidth=0.5)

# Labels
plt.xlabel('x', fontsize=14, labelpad=15)
plt.ylabel('y', fontsize=14, labelpad=15, rotation=0)
ax.xaxis.set_label_coords(1.02, 0.48)
ax.yaxis.set_label_coords(0.48, 1.02)

plt.legend(fontsize=10, loc='upper right')

plt.savefig('exercice_logarithme_equations_question5.png', dpi=300, bbox_inches='tight')
plt.show()

print("Graphique 'exercice_logarithme_equations_question5.png' créé avec succès!")


