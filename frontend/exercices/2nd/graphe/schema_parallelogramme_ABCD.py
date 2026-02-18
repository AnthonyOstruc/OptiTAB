import matplotlib.pyplot as plt
import numpy as np

A = np.array([2., 1.])
B = np.array([6., 3.])
C = np.array([4., -1.])

drag = None  # "B" ou "C"

fig, ax = plt.subplots(figsize=(7.5, 6))
ax.set_aspect("equal", adjustable="box")
ax.grid(True)

line_poly, = ax.plot([], [], marker="o")
diag1, = ax.plot([], [], linestyle="--")
diag2, = ax.plot([], [], linestyle="--")
midpt, = ax.plot([], [], marker="o")

# --- annotations (texte avec offset pour ne pas coller aux lignes) ---
def make_annot(dx, dy):
    return ax.annotate(
        "", xy=(0, 0),
        xytext=(dx, dy),
        textcoords="offset points",
        ha="left", va="bottom"
    )

annA = make_annot(-40, 0)
annB = make_annot(2, 0)
annC = make_annot(8, -10)
annD = make_annot(-8, -20)
annI = make_annot(8, -5)

def fmt(v):
    # affiche entier si proche d'un entier, sinon 2 décimales
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.2f}"

def redraw():
    global A, B, C
    D = A + C - B
    I = (A + C) / 2
    J = (B + D) / 2  # (= I)

    poly = np.vstack([A, B, C, D, A])
    line_poly.set_data(poly[:, 0], poly[:, 1])

    diag1.set_data([A[0], C[0]], [A[1], C[1]])
    diag2.set_data([B[0], D[0]], [B[1], D[1]])
    midpt.set_data([I[0]], [I[1]])

    # --- TEXTE ICI : tu peux personnaliser le contenu ---
    annA.xy = (A[0], A[1]); annA.set_text(f"A({fmt(A[0])} ; {fmt(A[1])})")
    annB.xy = (B[0], B[1]); annB.set_text(f"B({fmt(B[0])} ; {fmt(B[1])})")
    annC.xy = (C[0], C[1]); annC.set_text(f"C({fmt(C[0])} ; {fmt(C[1])})")
    annD.xy = (D[0], D[1]); annD.set_text(f"D({fmt(D[0])} ; {fmt(D[1])})")
    annI.xy = (I[0], I[1]); annI.set_text(f"I = J ({fmt(I[0])} ; {fmt(I[1])})")

    xs = np.array([A[0], B[0], C[0], D[0], I[0]])
    ys = np.array([A[1], B[1], C[1], D[1], I[1]])
    m = 2
    ax.set_xlim(xs.min() - m, xs.max() + m)
    ax.set_ylim(ys.min() - m, ys.max() + m)

    fig.canvas.draw_idle()

def near(P, x, y, tol=0.25):
    return (P[0] - x)**2 + (P[1] - y)**2 < tol**2

def on_press(event):
    global drag
    if event.inaxes != ax or event.xdata is None or event.ydata is None:
        return
    x, y = event.xdata, event.ydata
    if near(B, x, y): drag = "B"
    elif near(C, x, y): drag = "C"

def on_release(event):
    global drag
    drag = None

def on_move(event):
    global B, C
    if drag is None or event.inaxes != ax or event.xdata is None or event.ydata is None:
        return
    if drag == "B":
        B = np.array([event.xdata, event.ydata])
    elif drag == "C":
        C = np.array([event.xdata, event.ydata])
    redraw()

fig.canvas.mpl_connect("button_press_event", on_press)
fig.canvas.mpl_connect("button_release_event", on_release)
fig.canvas.mpl_connect("motion_notify_event", on_move)

ax.set_xlabel("x")
ax.set_ylabel("y")

redraw()
plt.show()
