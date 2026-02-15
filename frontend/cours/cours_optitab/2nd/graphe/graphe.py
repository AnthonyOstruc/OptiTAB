import matplotlib.pyplot as plt
import numpy as np

# Création des données
x = np.linspace(-2.2, 2.2, 400)
# Fonction f(x) = x^3 - 3x. Cette fonction est idéale car elle a un max clair et un min clair.
y = x**3 - 3*x

# Configuration du graphique
fig, ax = plt.subplots(figsize=(10, 6))

# Tracer la courbe
ax.plot(x, y, label='Courbe de f', color='#1f77b4', linewidth=3)

# 1. Annotation : La courbe monte (Croissante)
# Flèche et texte pour la première partie montante
ax.annotate('', xy=(-1.2, 0), xytext=(-1.8, -4),
            arrowprops=dict(facecolor='green', shrink=0.05, alpha=0.6))
ax.text(-1.8, -1.5, 'La courbe MONTE\n($f$ croissante)', color='green', fontsize=11, fontweight='bold', ha='center')

# 2. Annotation : Sommet (Maximum)
# Point rouge au sommet (-1, 2)
ax.plot(-1, 2, 'ro', markersize=10)
ax.annotate('SOMMET\n(Maximum)', xy=(-1, 2.2), xytext=(-1, 3.5),
            arrowprops=dict(facecolor='black', arrowstyle='->'),
            fontsize=12, fontweight='bold', ha='center', color='darkred')

# 3. Annotation : La courbe descend (Décroissante)
# Flèche et texte pour la partie descendante
ax.annotate('', xy=(0.8, -1), xytext=(-0.5, 1.5),
            arrowprops=dict(facecolor='red', shrink=0.05, alpha=0.6))
ax.text(0.2, 0.5, 'La courbe DESCEND\n($f$ décroissante)', color='red', fontsize=11, fontweight='bold', ha='center')

# 4. Annotation : Creux (Minimum)
# Point rouge au creux (1, -2)
ax.plot(1, -2, 'ro', markersize=10)
ax.annotate('CREUX\n(Minimum)', xy=(1, -2.2), xytext=(1, -4),
            arrowprops=dict(facecolor='black', arrowstyle='->'),
            fontsize=12, fontweight='bold', ha='center', color='darkred')

# 5. Annotation : La courbe remonte
ax.annotate('', xy=(1.8, 2), xytext=(1.2, -1),
            arrowprops=dict(facecolor='green', shrink=0.05, alpha=0.6))

# Mise en forme du repère
ax.axhline(0, color='black', linewidth=1) # Axe x
ax.axvline(0, color='black', linewidth=1) # Axe y
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_title("Illustration : Variations d'une fonction", fontsize=16, pad=20)
ax.set_xlabel("x (lecture de gauche à droite)", fontsize=12)
ax.set_ylabel("f(x)", fontsize=12)

# Limites pour que tout soit bien visible
ax.set_ylim(-5, 5)

# Sauvegarder et afficher
plt.tight_layout()
plt.show()