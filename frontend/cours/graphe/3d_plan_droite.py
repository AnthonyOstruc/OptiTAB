import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Création de la figure 3D
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Définir les paramètres du plan
# Plan: z = 2x + 3y + 1
x = np.linspace(-5, 5, 20)
y = np.linspace(-5, 5, 20)
X, Y = np.meshgrid(x, y)
Z = 2*X + 3*Y + 1

# Tracer le plan
ax.plot_surface(X, Y, Z, alpha=0.6, color='lightblue', label='Plan: z = 2x + 3y + 1')

# Définir la droite qui coupe le plan
# Droite paramétrique: x = t, y = 2t, z = 3t + 2
t = np.linspace(-3, 3, 100)
x_droite = t
y_droite = 2*t
z_droite = 3*t + 2

# Tracer la droite
ax.plot(x_droite, y_droite, z_droite, 'r-', linewidth=3, label='Droite: x=t, y=2t, z=3t+2')

# Calculer le point d'intersection
# Substituer dans l'équation du plan: 3t + 2 = 2t + 3(2t) + 1
# 3t + 2 = 2t + 6t + 1
# 3t + 2 = 8t + 1
# 1 = 5t
# t = 1/5 = 0.2
t_intersect = 0.2
x_intersect = t_intersect
y_intersect = 2*t_intersect
z_intersect = 3*t_intersect + 2

# Marquer le point d'intersection
ax.scatter([x_intersect], [y_intersect], [z_intersect], 
          color='black', s=100, label=f'Intersection: ({x_intersect:.1f}, {y_intersect:.1f}, {z_intersect:.1f})')

# Configuration des axes
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_zlabel('Z', fontsize=12)

# Limites des axes
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 15)

# Titre
plt.title('Plan et droite en 3D', fontsize=16, fontweight='bold')

# Légende
ax.legend()

# Afficher le graphique
plt.show()
