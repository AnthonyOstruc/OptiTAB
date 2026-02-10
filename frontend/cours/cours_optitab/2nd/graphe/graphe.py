import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- Configuration des données ---
# Coordonnées du point M (départ)
Mx, My = 2, 3
# Coordonnées du point M' (arrivée)
Mpx, Mpy = 7, 6

# Calcul des composantes du vecteur (pour les pointillés)
dx = Mpx - Mx
dy = Mpy - My

# --- Création de la figure et des axes ---
fig, ax = plt.subplots(figsize=(10, 7))

# --- Configuration du repère (style mathématique) ---
# Activer la grille
ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')

# Configurer les axes pour qu'ils passent par (0,0)
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# Ajouter des flèches au bout des axes (un peu une astuce en matplotlib)
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

# Labels des axes
ax.set_xlabel('$x$', loc='right', fontsize=14)
ax.set_ylabel('$y$', loc='top', fontsize=14, rotation=0)
ax.text(-0.5, -0.5, '$O$', fontsize=14) # Origine

# Définir les limites du graphique
ax.set_xlim(-1, 10)
ax.set_ylim(-1, 9)
ax.set_aspect('equal') # Important pour que le vecteur ne soit pas déformé

# --- Dessin des éléments mathématiques ---

# 1. Les pointillés (triangle rectangle pour les composantes)
plt.plot([Mx, Mpx], [My, My], 'k--', linewidth=1) # Ligne horizontale
plt.plot([Mpx, Mpx], [My, Mpy], 'k--', linewidth=1) # Ligne verticale
# Petit carré pour l'angle droit
rect = patches.Rectangle((Mpx, My), -0.4, 0.4, linewidth=1, edgecolor='k', facecolor='none')
ax.add_patch(rect)

# 2. Les points M et M'
ax.scatter([Mx, Mpx], [My, Mpy], color='black', s=50, zorder=5)

# 3. Le Vecteur MM' (Grosse flèche rouge)
# On utilise annotate pour une belle flèche
ax.annotate('', xy=(Mpx, Mpy), xytext=(Mx, My),
            arrowprops=dict(arrowstyle='->', color='red', linewidth=3, mutation_scale=25))

# --- Ajout des textes et labels ---

# Labels des points
ax.text(Mx - 0.5, My + 0.3, '$M(x, y)$', fontsize=14, ha='right')
ax.text(Mpx + 0.3, Mpy + 0.3, "$M'(x', y')$", fontsize=14)

# Nom du vecteur au-dessus de la flèche
mid_x = (Mx + Mpx) / 2
mid_y = (My + Mpy) / 2
ax.text(mid_x - 0.5, mid_y + 0.8, r'$\vec{MM}$ ou $\vec{u}$', fontsize=16, color='red')

# Labels des composantes sur les pointillés
ax.text(mid_x, My - 0.5, r"$x' - x$", fontsize=12, ha='center')
ax.text(Mpx + 0.3, mid_y, r"$y' - y$", fontsize=12, va='center')

# --- Ajout de la boîte de définition en haut ---
definition_text = (
    "Définition mathématique :\n"
    r"Le vecteur $\vec{u} = \vec{MM'}$ est associé à la translation"
    "\nqui transforme le point M en M'."
)

# Création d'une boîte de texte stylisée
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.5, 8.5, definition_text, fontsize=14,
        verticalalignment='top', bbox=props)

# --- (Optionnel) Un deuxième vecteur équivalent pour montrer le concept ---
Mx2, My2 = 4, 0.5
Mpx2, Mpy2 = Mx2 + dx, My2 + dy
ax.annotate('', xy=(Mpx2, Mpy2), xytext=(Mx2, My2),
            arrowprops=dict(arrowstyle='->', color='red', linewidth=2, mutation_scale=20, alpha=0.6))
ax.text((Mx2+Mpx2)/2, (My2+Mpy2)/2 + 0.3, r'$\vec{v}$', fontsize=14, color='red', alpha=0.6)


plt.title("Schéma Mathématique de la Définition d'un Vecteur", pad=20)
plt.show()