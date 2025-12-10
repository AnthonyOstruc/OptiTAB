import numpy as np
import matplotlib.pyplot as plt

# ============================
# Suite : u_{n+1} = 2 u_n - 1, u0 = 0.5
# ============================

def f(x):
    return 2 * x - 1

u = [0.5]  # u0
for n in range(4):      # calculer jusqu'à u4
    u.append(f(u[-1]))

# Domaine pour tracer f et la droite y = x
x = np.linspace(-8, 2, 400)
y_f = f(x)
y_id = x

# ============================
# Tracé
# ============================

plt.figure(figsize=(7, 7))

# Courbe de f et droite y = x
plt.plot(x, y_f, label="f(x) = 2x - 1")
plt.plot(x, y_id, linestyle='--', label="Droite y = x")

# Toile d'araignée pour u0 -> u4
for n in range(4):
    # segment vertical : (u_n, u_n) -> (u_n, u_{n+1})
    x_vert = [u[n], u[n]]
    y_vert = [u[n], u[n+1]]
    plt.plot(x_vert, y_vert, color="black", linewidth=0.8)
    
    # segment horizontal : (u_n, u_{n+1}) -> (u_{n+1}, u_{n+1})
    x_horiz = [u[n], u[n+1]]
    y_horiz = [u[n+1], u[n+1]]
    plt.plot(x_horiz, y_horiz, color="black", linewidth=0.8)

# Points (u_n, u_n) avec étiquettes
for n, un in enumerate(u):  # u0 à u4
    plt.scatter(un, un, zorder=5)
    plt.text(un -0.25, un + 0.1, f"u{n}", fontsize=8)

# Axes du repère
plt.axhline(0, linewidth=0.5)
plt.axvline(0, linewidth=0.5)
plt.xlim(-8, 2)
plt.ylim(-8, 2)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.legend(loc="lower right", fontsize=8)


plt.xlabel("x")
plt.ylabel("y")

plt.show()
