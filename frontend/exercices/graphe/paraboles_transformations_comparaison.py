import numpy as np
import matplotlib.pyplot as plt

# 1) Domaine de x
x = np.linspace(-4, 4, 400)

# 2) Définition des fonctions
def fA(x):
    return x**2              # Parabole A : référence

def fB(x):
    return x**2 + 2          # Parabole B : translation verticale

def fC(x):
    return (x - 2)**2        # Parabole C : translation horizontale

def fD(x):
    return (x - 2)**2 - 2    # Parabole D : translation horizontale + verticale

# 3) Création de la figure avec 4 sous-graphes (2 lignes × 2 colonnes)
fig, axes = plt.subplots(2, 2, figsize=(8, 8))

fonctions = [fA, fB, fC, fD]
titres = [
    "Parabole A",
    "Parabole B",
    "Parabole C",
    "Parabole D"
]
couleurs = ["red", "blue", "green", "purple"]

# 4) Tracé de chaque parabole dans son cadre
for ax, f, titre, couleur in zip(axes.flatten(), fonctions, titres, couleurs):
    ax.axhline(0, linewidth=0.8)        # axe horizontal
    ax.axvline(0, linewidth=0.8)        # axe vertical
    ax.plot(x, f(x), couleur)
    ax.set_title(titre, pad=10)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 6)
    ax.grid(True, linewidth=0.4, alpha=0.4)

# 5) Titre global + ajustement des marges

fig.tight_layout(rect=[0, 0, 1, 0.94])

# 6) Affichage
plt.show()

# 7) (Optionnel) Sauvegarde dans un fichier
# fig.savefig("paraboles_grille_2x2.png", dpi=200, bbox_inches="tight")
