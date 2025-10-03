import numpy as np
import matplotlib.pyplot as plt

# Définir les vecteurs u et v
u = np.array([3, 2])
v = np.array([1, 4])

# Calcul de la projection de u sur v
proj_u_on_v = (np.dot(u, v) / np.dot(v, v)) * v

# Création de la figure
plt.figure(figsize=(6,6))

# Tracer les vecteurs
plt.quiver(0, 0, u[0], u[1], angles='xy', scale_units='xy', scale=1, color='blue')
plt.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1, color='green')
plt.quiver(0, 0, proj_u_on_v[0], proj_u_on_v[1], angles='xy', scale_units='xy', scale=1, color='red')

# Ajouter les étiquettes en mode mathématique
plt.text(u[0]+0.1, u[1]+0.1, r'$\vec{u}$', color='blue', fontsize=14)
plt.text(v[0]+0.1, v[1]+0.1, r'$\vec{v}$', color='green', fontsize=14)
plt.text(proj_u_on_v[0]+0.1, proj_u_on_v[1]+0.1, r'$\mathrm{proj}_{\vec{v}}\vec{u}$', color='red', fontsize=14)

# Tracer une ligne pour montrer la projection (en pointillés)
plt.plot([u[0], proj_u_on_v[0]], [u[1], proj_u_on_v[1]], color='red', linestyle='--', linewidth=1)

# Ajouter un angle droit (petit carré) à l'intersection
angle_size = 0.15

# Calculer les vecteurs unitaires
v_unit = v / np.linalg.norm(v)  # Direction de v (normalisée)
u_to_proj = u - proj_u_on_v  # Vecteur de proj vers u
u_to_proj_unit = u_to_proj / np.linalg.norm(u_to_proj)  # Direction perpendiculaire (normalisée)

# Points pour former un carré (angle droit)
# Point 1: sur le vecteur v (direction de la projection)
p1 = proj_u_on_v - angle_size * v_unit
# Point 2: coin de l'angle droit
p2 = proj_u_on_v
# Point 3: sur la direction perpendiculaire
p3 = proj_u_on_v + angle_size * u_to_proj_unit
# Point 4: pour fermer le carré
p4 = p1 + angle_size * u_to_proj_unit

# Tracer le carré (angle droit) - 4 côtés
plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='red', linewidth=2)  # Côté 1
plt.plot([p2[0], p3[0]], [p2[1], p3[1]], color='red', linewidth=2)  # Côté 2
plt.plot([p3[0], p4[0]], [p3[1], p4[1]], color='red', linewidth=2)  # Côté 3
plt.plot([p4[0], p1[0]], [p4[1], p1[1]], color='red', linewidth=2)  # Côté 4

# Limites du graphique
plt.xlim(-1, max(u[0], v[0], proj_u_on_v[0]) + 1)
plt.ylim(-1, max(u[1], v[1], proj_u_on_v[1]) + 1)

# Masquer les axes
plt.axis('off')

# Afficher le graphique
plt.show()
