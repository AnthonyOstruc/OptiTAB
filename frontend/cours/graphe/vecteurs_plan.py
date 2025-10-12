import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 10))
ax = plt.gca()

# Configuration du graphique - élargi pour avoir deux zones
plt.xlim(-6, 8)
plt.ylim(-1, 6)

# Désactiver ticks automatiques
ax.set_xticks([])
ax.set_yticks([])

# Supprimer spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Axes supprimés

# Ligne de séparation verticale
ax.axvline(x=0, color='gray', linestyle='-', linewidth=2, alpha=0.7)

# --- Vecteur u (en bleu) - déplacé plus à droite et réduit ---
# Origine en (2, 0), extrémité en (5, 1.2) - plus horizontal pour ouvrir le parallélogramme
u_x, u_y = 5, 1.2
ax.annotate("", xy=(u_x, u_y), xytext=(2, 0),
            arrowprops=dict(arrowstyle="->", color="#2e7d32", linewidth=2.2, 
                          mutation_scale=18))
ax.text(u_x + 0.2, u_y + 0.15, r'$\vec{u}$', fontsize=14, color="#2e7d32", 
        fontweight='bold')
ax.text(u_x/2 + 1.6, u_y/2 + 0.2, r'$\vec{u} = \binom{3}{2}$', 
        fontsize=11, color="#2e7d32", bbox=dict(boxstyle="round,pad=0.25", 
        facecolor="white", edgecolor="#2e7d32", linewidth=1.5))

# --- Vecteur v (en rouge) - déplacé plus à droite et réduit ---
# Origine en (2, 0), extrémité en (2.8, 3.2) - plus vertical pour ouvrir le parallélogramme
v_x, v_y = 2.8, 3.2
ax.annotate("", xy=(v_x, v_y), xytext=(2, 0),
            arrowprops=dict(arrowstyle="->", color="#c62828", linewidth=2.2, 
                          mutation_scale=18))
ax.text(v_x - 0.3, v_y + 0.15, r'$\vec{v}$', fontsize=14, color="#c62828", 
        fontweight='bold')
ax.text(v_x/2 + 0.3, v_y/2 - 0.3, r'$\vec{v} = \binom{2}{4}$', 
        fontsize=11, color="#c62828", bbox=dict(boxstyle="round,pad=0.25", 
        facecolor="white", edgecolor="#c62828", linewidth=1.5))

# --- Vecteur w = u + v (en violet) - déplacé plus à droite et réduit ---
# Addition de vecteurs
w_x, w_y = u_x + v_x - 2, u_y + v_y
ax.annotate("", xy=(w_x, w_y), xytext=(2, 0),
            arrowprops=dict(arrowstyle="->", color="#6a1b9a", linewidth=2.2, 
                          mutation_scale=18))
ax.text(w_x + 0.15, w_y + 0.15, r'$\vec{w} = \vec{u} + \vec{v}$', fontsize=14, 
        color="#6a1b9a", fontweight='bold')
ax.text(w_x/2 + 0.3, w_y/2, r'$\vec{w} = \binom{5}{6}$', 
        fontsize=11, color="#6a1b9a", bbox=dict(boxstyle="round,pad=0.25", 
        facecolor="white", edgecolor="#6a1b9a", linewidth=1.5))

# --- Parallélogramme pour montrer l'addition ---
# Ligne en pointillés de u à w
ax.plot([u_x, w_x], [u_y, w_y], 'r--', linewidth=1.0, alpha=0.5)
# Ligne en pointillés de v à w
ax.plot([v_x, w_x], [v_y, w_y], 'g--', linewidth=1.0, alpha=0.5)

# --- Points pour marquer les extrémités ---
ax.plot(2, 0, 'ko', markersize=5)  # Nouvelle origine
ax.plot(u_x, u_y, 'go', markersize=4)
ax.plot(v_x, v_y, 'ro', markersize=4)
ax.plot(w_x, w_y, 'mo', markersize=4)

# Labels des axes supprimés

# Titre supprimé

# Texte explicatif - zone droite
ax.text(4, 5.5, "Addition vectorielle : règle du parallélogramme", 
        fontsize=11, style='italic', color="#34495e",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#e8f4fd", 
                 edgecolor="#3498db", linewidth=1.5))

# Règle de Chasles - zone gauche
ax.text(-3, 5.5, r"Règle de Chasles : $\vec{AB} + \vec{BC} = \vec{AC}$", 
        fontsize=11, style='italic', color="#34495e",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#fef3c7", 
                 edgecolor="#ffa500", linewidth=1.5))

# --- Illustration de la règle de Chasles (zone gauche) ---
# Points A, B, C pour la règle de Chasles - déplacés à gauche
A_x, A_y = -4, 1
B_x, B_y = -1.5, 1.5
C_x, C_y = -0.5, 3.5

# Vecteur AB (en bleu foncé)
ax.annotate("", xy=(B_x, B_y), xytext=(A_x, A_y),
            arrowprops=dict(arrowstyle="->", color="#1565c0", linewidth=2.2, 
                          mutation_scale=18))
ax.text((A_x + B_x)/2, (A_y + B_y)/2 - 0.4, r'$\vec{AB}$', fontsize=13, 
        color="#1565c0", fontweight='bold')

# Vecteur BC (en orange foncé)
ax.annotate("", xy=(C_x, C_y), xytext=(B_x, B_y),
            arrowprops=dict(arrowstyle="->", color="#e65100", linewidth=2.2, 
                          mutation_scale=18))
ax.text((B_x + C_x)/2 + 0.3, (B_y + C_y)/2, r'$\vec{BC}$', fontsize=13, 
        color="#e65100", fontweight='bold')

# Vecteur AC (en violet, pointillé pour montrer la somme)
ax.annotate("", xy=(C_x, C_y), xytext=(A_x, A_y),
            arrowprops=dict(arrowstyle="->", color="#7b1fa2", linewidth=2.2, 
                          mutation_scale=18, linestyle='dashed'))
ax.text((A_x + C_x)/2 - 0.5, (A_y + C_y)/2 + 0.3, r'$\vec{AC}$', fontsize=13, 
        color="#7b1fa2", fontweight='bold')

# Points A, B, C
ax.plot(A_x, A_y, 'ko', markersize=7)
ax.plot(B_x, B_y, 'ko', markersize=7)
ax.plot(C_x, C_y, 'ko', markersize=7)

# Labels des points
ax.text(A_x - 0.3, A_y - 0.3, 'A', fontsize=14, fontweight='bold')
ax.text(B_x, B_y - 0.4, 'B', fontsize=14, fontweight='bold')
ax.text(C_x + 0.2, C_y + 0.2, 'C', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()

