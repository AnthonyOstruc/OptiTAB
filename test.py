#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OptiTAB – Config Bâtiment (v2)
- Vues: Gauche / Droite / Avant / Arrière / Plan
- Déplacer les vues (cadres) + zoom/pan par vue

✅ FIX: Ajout des "pentes" visuelles (mono-pente et 2 pans) avec logique de vues cohérente.

Hypothèses géométriques (simples et cohérentes) :
- Plan: L (axe x), B (axe y)
- Vue Avant / Arrière : largeur = L (x)
- Vue Gauche / Droite : largeur = B (y)
- Direction de pente:
    * Sur L (gauche↔droite) : la hauteur varie avec x
        - Différence de hauteur entre Vue Gauche et Vue Droite
        - La pente (ligne inclinée / pignon) est visible sur Vue Avant & Vue Arrière
    * Sur B (avant↔arrière) : la hauteur varie avec y
        - Différence de hauteur entre Vue Avant et Vue Arrière
        - La pente (ligne inclinée / pignon) est visible sur Vue Gauche & Vue Droite

#Versant:
- 1 = mono-pente
- 2 = 2 pans (pignon visible sur les vues "pente visible", faces opposées identiques)

Hs:
- Pour l’instant, Hs est dessiné comme une petite "surélévation" symbolique (placeholder).
"""

import tkinter as tk
from tkinter import ttk


def _f(v, default=0.0) -> float:
    if v is None:
        return default
    s = str(v).strip().replace(",", ".")
    if s == "":
        return default
    try:
        return float(s)
    except ValueError:
        return default


def _clamp(a, lo, hi):
    return max(lo, min(hi, a))


class BuildingSketchApp(ttk.Frame):
    PAD = 10

    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.master.title("OptiTAB – Config Bâtiment (v2)")
        self.master.minsize(1280, 780)

        self._make_style()
        self.pack(fill="both", expand=True)

        # per-view state
        self.views = ["rear", "left", "plan", "right", "front"]
        self.view_box_offset = {k: (0.0, 0.0) for k in self.views}   # move the view box
        self.view_zoom = {k: 1.0 for k in self.views}               # zoom content inside view
        self.view_pan = {k: (0.0, 0.0) for k in self.views}          # pan content inside view (px)

        self.active_view = None

        # drag state
        self._drag_mode = None      # "box" or "pan"
        self._drag_view = None
        self._drag_start = (0, 0)
        self._drag_base = (0.0, 0.0)

        self._build_ui()
        self._bind_events()
        self.load_example()

    # ---------------- Style/UI ----------------

    def _make_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("Hint.TLabel", font=("Segoe UI", 9))
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TCombobox", font=("Segoe UI", 10))

    def _build_ui(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        left = ttk.Frame(self, padding=self.PAD)
        left.grid(row=0, column=0, sticky="nsw")

        right = ttk.Frame(self, padding=(self.PAD, self.PAD, self.PAD, self.PAD))
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)

        ttk.Label(left, text="Config. Bâtiment", style="Title.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.var_L = tk.StringVar()
        self.var_B = tk.StringVar()
        self.var_Hmin = tk.StringVar()
        self.var_Hmax = tk.StringVar()
        self.var_nvers = tk.StringVar()
        self.var_Hs = tk.StringVar()

        self.var_slope_dir = tk.StringVar()   # "L" or "B" via label
        self.var_high_end = tk.StringVar()    # depends on slope dir + mono
        self.var_move_boxes = tk.BooleanVar(value=True)

        def row(label, var, unit="m", r=0, widget="entry", values=None, width=18):
            ttk.Label(left, text=label).grid(row=r, column=0, sticky="w", pady=4)
            if widget == "combo":
                cb = ttk.Combobox(left, textvariable=var, values=values or (), width=width, state="readonly")
                cb.grid(row=r, column=1, sticky="w", pady=4)
                w = cb
            else:
                ent = ttk.Entry(left, textvariable=var, width=12)
                ent.grid(row=r, column=1, sticky="w", pady=4)
                w = ent
            ttk.Label(left, text=unit).grid(row=r, column=1, sticky="e", pady=4, padx=(0, 2))
            return w

        self.w_L = row("L", self.var_L, "m", r=1)
        self.w_B = row("B", self.var_B, "m", r=2)
        self.w_Hmin = row("H_min", self.var_Hmin, "m", r=3)
        self.w_Hmax = row("H_max", self.var_Hmax, "m", r=4)
        self.w_nvers = row("# Versant", self.var_nvers, "-", r=5, widget="combo", values=("1", "2"), width=10)
        self.w_Hs = row("Hs (surélévation)", self.var_Hs, "m", r=6)

        ttk.Separator(left).grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)

        ttk.Label(left, text="Toiture (vues)", style="Title.TLabel").grid(row=8, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.w_dir = row(
            "Direction de pente",
            self.var_slope_dir,
            "",
            r=9,
            widget="combo",
            values=("Sur L (gauche↔droite)", "Sur B (avant↔arrière)"),
            width=22
        )
        self.w_high = row(
            "Côté haut (mono)",
            self.var_high_end,
            "",
            r=10,
            widget="combo",
            values=("Droite", "Gauche"),
            width=22
        )

        ttk.Separator(left).grid(row=11, column=0, columnspan=2, sticky="ew", pady=10)

        ttk.Label(left, text="Vues (mise en page)", style="Title.TLabel").grid(row=12, column=0, columnspan=2, sticky="w", pady=(0, 6))
        ttk.Checkbutton(left, text="Déplacer les vues (cadres)", variable=self.var_move_boxes).grid(row=13, column=0, columnspan=2, sticky="w")

        self.lbl_active = ttk.Label(left, text="Vue active: (clique une vue)", style="Hint.TLabel")
        self.lbl_active.grid(row=14, column=0, columnspan=2, sticky="w", pady=(6, 0))

        zoom_row = ttk.Frame(left)
        zoom_row.grid(row=15, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        zoom_row.columnconfigure(0, weight=1)
        zoom_row.columnconfigure(1, weight=1)
        zoom_row.columnconfigure(2, weight=1)
        ttk.Button(zoom_row, text="Zoom +", command=lambda: self.zoom_active(1.15)).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(zoom_row, text="Zoom -", command=lambda: self.zoom_active(1/1.15)).grid(row=0, column=1, sticky="ew", padx=(0, 6))
        ttk.Button(zoom_row, text="Reset vue", command=self.reset_active_view).grid(row=0, column=2, sticky="ew")

        reset_row = ttk.Frame(left)
        reset_row.grid(row=16, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        reset_row.columnconfigure(0, weight=1)
        reset_row.columnconfigure(1, weight=1)
        ttk.Button(reset_row, text="Reset positions", command=self.reset_positions).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(reset_row, text="Reset tout (zoom/pan)", command=self.reset_all_view_transforms).grid(row=0, column=1, sticky="ew")

        ttk.Separator(left).grid(row=17, column=0, columnspan=2, sticky="ew", pady=10)

        btns = ttk.Frame(left)
        btns.grid(row=18, column=0, columnspan=2, sticky="ew")
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)
        ttk.Button(btns, text="Charger exemple", command=self.load_example).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(btns, text="Dessiner", style="Primary.TButton", command=self.redraw).grid(row=0, column=1, sticky="ew")

        ttk.Label(
            left,
            text=("Souris:\n"
                  "• Clic = sélectionner une vue\n"
                  "• Molette = zoomer la vue sous la souris\n"
                  "• Clic droit + glisser = pan (contenu)\n"
                  "• Clic gauche + glisser = déplacer cadre (si activé) sinon pan\n"
                  "• Double-clic = reset zoom/pan de la vue"),
            style="Hint.TLabel"
        ).grid(row=19, column=0, columnspan=2, sticky="w", pady=(10, 0))

        self.canvas = tk.Canvas(right, bg="white", highlightthickness=1, highlightbackground="#d0d0d0")
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def _bind_events(self):
        for w in (self.w_L, self.w_B, self.w_Hmin, self.w_Hmax, self.w_Hs):
            w.bind("<Return>", lambda _e: self.redraw())
            w.bind("<FocusOut>", lambda _e: self.redraw())
        self.w_nvers.bind("<<ComboboxSelected>>", lambda _e: self.redraw())
        self.w_dir.bind("<<ComboboxSelected>>", lambda _e: self._on_dir_change())
        self.w_high.bind("<<ComboboxSelected>>", lambda _e: self.redraw())

        self._resize_job = None
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        self.canvas.bind("<ButtonPress-1>", self._on_left_down)
        self.canvas.bind("<B1-Motion>", self._on_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_left_up)

        self.canvas.bind("<ButtonPress-3>", self._on_right_down)
        self.canvas.bind("<B3-Motion>", self._on_right_drag)
        self.canvas.bind("<ButtonRelease-3>", self._on_right_up)

        self.canvas.bind("<Double-Button-1>", self._on_double_click)

        self.canvas.bind("<MouseWheel>", self._on_wheel)        # Windows/macOS
        self.canvas.bind("<Button-4>", self._on_wheel_linux)    # Linux up
        self.canvas.bind("<Button-5>", self._on_wheel_linux)    # Linux down

    def _on_canvas_resize(self, _evt):
        if self._resize_job:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(120, self.redraw)

    # ---------------------- UI commands ----------------------

    def load_example(self):
        self.var_L.set("18")
        self.var_B.set("17")
        self.var_Hmin.set("12")
        self.var_Hmax.set("12,6")
        self.var_nvers.set("2")
        self.var_Hs.set("0")
        self.var_slope_dir.set("Sur L (gauche↔droite)")
        self.var_high_end.set("Droite")
        self.active_view = None
        self._update_active_label()
        self.redraw()

    def _on_dir_change(self):
        # Update "côté haut" choices to match slope direction
        d = self._slope_dir()
        if d == "L":
            vals = ("Gauche", "Droite")
            if self.var_high_end.get() not in vals:
                self.var_high_end.set("Droite")
        else:
            vals = ("Avant", "Arrière")
            if self.var_high_end.get() not in vals:
                self.var_high_end.set("Arrière")
        self.w_high.config(values=vals)
        self.redraw()

    def reset_positions(self):
        for k in self.views:
            self.view_box_offset[k] = (0.0, 0.0)
        self.redraw()

    def reset_all_view_transforms(self):
        for k in self.views:
            self.view_zoom[k] = 1.0
            self.view_pan[k] = (0.0, 0.0)
        self.redraw()

    def zoom_active(self, factor):
        if not self.active_view:
            return
        z = self.view_zoom[self.active_view] * factor
        self.view_zoom[self.active_view] = _clamp(z, 0.2, 10.0)
        self.redraw()

    def reset_active_view(self):
        if not self.active_view:
            return
        self.view_zoom[self.active_view] = 1.0
        self.view_pan[self.active_view] = (0.0, 0.0)
        self.redraw()

    def _update_active_label(self):
        names = {"rear": "Vue Arrière", "left": "Vue Gauche", "plan": "Vue en Plan", "right": "Vue Droite", "front": "Vue Avant", None: "(clique une vue)"}
        self.lbl_active.config(text=f"Vue active: {names.get(self.active_view, '(clique une vue)')}")

    # ---------------------- Mouse helpers ----------------------

    def _hit_test_view(self, x, y, boxes):
        for key, (x0, y0, x1, y1) in boxes.items():
            if x0 <= x <= x1 and y0 <= y <= y1:
                return key
        return None

    def _set_active_view_from_mouse(self, evt):
        boxes = self._get_view_boxes_with_offsets()
        key = self._hit_test_view(evt.x, evt.y, boxes)
        if key:
            self.active_view = key
            self._update_active_label()
        return key

    def _on_left_down(self, evt):
        key = self._set_active_view_from_mouse(evt)
        if not key:
            return
        self._drag_start = (evt.x, evt.y)
        if self.var_move_boxes.get():
            self._drag_mode = "box"
            self._drag_base = self.view_box_offset[key]
            self.canvas.configure(cursor="fleur")
        else:
            self._drag_mode = "pan"
            self._drag_base = self.view_pan[key]
            self.canvas.configure(cursor="hand2")
        self._drag_view = key

    def _on_left_drag(self, evt):
        if not self._drag_view:
            return
        dx = evt.x - self._drag_start[0]
        dy = evt.y - self._drag_start[1]
        if self._drag_mode == "box":
            ox0, oy0 = self._drag_base
            W = max(10, self.canvas.winfo_width())
            H = max(10, self.canvas.winfo_height())
            self.view_box_offset[self._drag_view] = (_clamp(ox0 + dx, -W * 0.6, W * 0.6), _clamp(oy0 + dy, -H * 0.6, H * 0.6))
        elif self._drag_mode == "pan":
            px0, py0 = self._drag_base
            self.view_pan[self._drag_view] = (px0 + dx, py0 + dy)
        self.redraw()

    def _on_left_up(self, _evt):
        self._drag_view = None
        self._drag_mode = None
        self.canvas.configure(cursor="")

    def _on_right_down(self, evt):
        key = self._set_active_view_from_mouse(evt)
        if not key:
            return
        self._drag_view = key
        self._drag_mode = "pan"
        self._drag_start = (evt.x, evt.y)
        self._drag_base = self.view_pan[key]
        self.canvas.configure(cursor="hand2")

    def _on_right_drag(self, evt):
        if not self._drag_view or self._drag_mode != "pan":
            return
        dx = evt.x - self._drag_start[0]
        dy = evt.y - self._drag_start[1]
        px0, py0 = self._drag_base
        self.view_pan[self._drag_view] = (px0 + dx, py0 + dy)
        self.redraw()

    def _on_right_up(self, _evt):
        if self._drag_mode == "pan":
            self._drag_view = None
            self._drag_mode = None
        self.canvas.configure(cursor="")

    def _on_double_click(self, evt):
        key = self._set_active_view_from_mouse(evt)
        if not key:
            return
        self.view_zoom[key] = 1.0
        self.view_pan[key] = (0.0, 0.0)
        self.redraw()

    def _on_wheel(self, evt):
        boxes = self._get_view_boxes_with_offsets()
        key = self._hit_test_view(evt.x, evt.y, boxes)
        if not key:
            return
        self.active_view = key
        self._update_active_label()
        factor = 1.12 if evt.delta > 0 else 1 / 1.12
        self._zoom_view_at_point(key, factor, evt.x, evt.y)

    def _on_wheel_linux(self, evt):
        boxes = self._get_view_boxes_with_offsets()
        key = self._hit_test_view(evt.x, evt.y, boxes)
        if not key:
            return
        self.active_view = key
        self._update_active_label()
        factor = 1.12 if evt.num == 4 else 1 / 1.12
        self._zoom_view_at_point(key, factor, evt.x, evt.y)

    def _zoom_view_at_point(self, key, factor, mx, my):
        old_z = self.view_zoom[key]
        new_z = _clamp(old_z * factor, 0.2, 10.0)
        if abs(new_z - old_z) < 1e-9:
            return
        boxes = self._get_view_boxes_with_offsets()
        x0, y0, x1, y1 = boxes[key]
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        px, py = self.view_pan[key]
        vx = (mx - (cx + px))
        vy = (my - (cy + py))
        ratio = new_z / old_z
        new_px = px + vx * (1 - ratio)
        new_py = py + vy * (1 - ratio)
        self.view_zoom[key] = new_z
        self.view_pan[key] = (new_px, new_py)
        self.redraw()

    # ---------------------- Drawing helpers ----------------------

    def _clear(self):
        self.canvas.delete("all")

    def _text(self, x, y, s, **kw):
        return self.canvas.create_text(x, y, text=s, **kw)

    def _line(self, x1, y1, x2, y2, **kw):
        return self.canvas.create_line(x1, y1, x2, y2, **kw)

    def _rect(self, x1, y1, x2, y2, **kw):
        return self.canvas.create_rectangle(x1, y1, x2, y2, **kw)

    def _poly(self, pts, **kw):
        return self.canvas.create_polygon(*pts, **kw)

    def _fmt_m(self, v: float) -> str:
        return f"{v:,.2f} m".replace(",", " ").replace(".", ",")

    def _draw_dim_h(self, x1, y, x2, text, offset=16, color="#111"):
        y_dim = y + offset
        self._line(x1, y_dim, x2, y_dim, fill=color, width=1, arrow=tk.BOTH)
        self._line(x1, y, x1, y_dim, fill=color, width=1)
        self._line(x2, y, x2, y_dim, fill=color, width=1)
        self._text((x1 + x2) / 2, y_dim - 12, text, fill=color, font=("Segoe UI", 9))

    def _draw_dim_v(self, x, y1, y2, text, offset=16, color="#111"):
        x_dim = x - offset
        self._line(x_dim, y1, x_dim, y2, fill=color, width=1, arrow=tk.BOTH)
        self._line(x, y1, x_dim, y1, fill=color, width=1)
        self._line(x, y2, x_dim, y2, fill=color, width=1)
        self._text(x_dim + 44, (y1 + y2) / 2, text, fill=color, font=("Segoe UI", 9), angle=90)

    def _fit_scale(self, phys_w, phys_h, box_w, box_h, pad=18):
        if phys_w <= 0 or phys_h <= 0:
            return 1.0
        sx = (box_w - 2 * pad) / phys_w
        sy = (box_h - 2 * pad) / phys_h
        return max(0.01, min(sx, sy))

    # ---------------------- Layout ----------------------

    def _default_view_boxes(self, W, H):
        margin = 24
        gap = 24
        top_h = int(H * 0.30)
        mid_h = int(H * 0.34)
        bot_h = max(160, H - margin * 2 - top_h - mid_h - gap * 2)
        mid_w = W - margin * 2
        box_w = (mid_w - 2 * gap) / 3
        rear_box = (margin + box_w + gap, margin, margin + 2 * box_w + gap, margin + top_h)
        left_box = (margin, margin + top_h + gap, margin + box_w, margin + top_h + gap + mid_h)
        plan_box = (margin + box_w + gap, margin + top_h + gap, margin + 2 * box_w + gap, margin + top_h + gap + mid_h)
        right_box = (margin + 2 * box_w + 2 * gap, margin + top_h + gap, margin + 3 * box_w + 2 * gap, margin + top_h + gap + mid_h)
        front_box = (margin + box_w + gap, margin + top_h + gap + mid_h + gap, margin + 2 * box_w + gap, margin + top_h + gap + mid_h + gap + bot_h)
        return {"rear": rear_box, "left": left_box, "plan": plan_box, "right": right_box, "front": front_box}

    def _get_view_boxes_with_offsets(self):
        W = max(10, self.canvas.winfo_width())
        H = max(10, self.canvas.winfo_height())
        base = self._default_view_boxes(W, H)
        out = {}
        for k, (x0, y0, x1, y1) in base.items():
            ox, oy = self.view_box_offset.get(k, (0.0, 0.0))
            out[k] = (x0 + ox, y0 + oy, x1 + ox, y1 + oy)
        return out

    # ---------------------- Roof logic ----------------------

    def _slope_dir(self):
        return "L" if str(self.var_slope_dir.get()).startswith("Sur L") else "B"

    def _mono_high_end(self):
        # returns one of: "left","right","front","rear"
        d = self._slope_dir()
        v = self.var_high_end.get().strip()
        if d == "L":
            return "left" if v == "Gauche" else "right"
        return "front" if v == "Avant" else "rear"

    def _heights_for_view(self, view_key, Hmin, Hmax, nvers):
        """
        Returns (h_left_edge, h_right_edge, h_peak) for the elevation:
        - For constant top: h_left_edge == h_right_edge == h_peak
        - For mono slope profile: h_left_edge != h_right_edge, h_peak = max
        - For gable: h_left_edge == h_right_edge == Hmin, h_peak = Hmax
        """
        d = self._slope_dir()
        high = self._mono_high_end()
        dh = max(0.0, Hmax - Hmin)

        # which elevations have "profile" (show slope/pignon)?
        # If slope varies with x (dir=L), profile visible on front/rear (width=L)
        # If slope varies with y (dir=B), profile visible on left/right (width=B)
        profile = (view_key in ("front", "rear")) if d == "L" else (view_key in ("left", "right"))

        if nvers == 2:
            if profile:
                return (Hmin, Hmin, Hmax)
            return (Hmin, Hmin, Hmin)

        # nvers == 1 mono-pente
        if profile:
            # slope across the view width
            # Determine which edge (left vs right) is higher depending on direction/high end
            if d == "L":
                # slope varies with x -> left/right elevations at x=0/x=L; high is one of them
                left_h = Hmax if high == "left" else Hmin
                right_h = Hmax if high == "right" else Hmin
            else:
                # slope varies with y -> front/rear elevations at y=0/y=B; within side view, left edge ~ front, right edge ~ rear
                # We map the left edge of a side view to "front" and right edge to "rear" (visual convention)
                left_h = Hmax if high == "front" else Hmin
                right_h = Hmax if high == "rear" else Hmin
            return (left_h, right_h, max(left_h, right_h))

        # non-profile elevations are at a fixed coordinate => constant height depending on which end they are
        if d == "L":
            if view_key == "left":
                h = Hmax if high == "left" else Hmin
            elif view_key == "right":
                h = Hmax if high == "right" else Hmin
            else:
                h = Hmin  # front/rear not profile? (shouldn't happen)
        else:
            if view_key == "front":
                h = Hmax if high == "front" else Hmin
            elif view_key == "rear":
                h = Hmax if high == "rear" else Hmin
            else:
                h = Hmin
        return (h, h, h)

    # ---------------------- Transform per view ----------------------

    def _view_transform(self, key, box, phys_w, phys_h, pad=18, label_space=34):
        x0, y0, x1, y1 = box
        cx0 = x0 + 6
        cy0 = y0 + 8
        cx1 = x1 - 6
        cy1 = y1 - label_space
        box_w = max(10, cx1 - cx0)
        box_h = max(10, cy1 - cy0)
        base_scale = self._fit_scale(phys_w, phys_h, box_w, box_h, pad=pad)
        scale = base_scale * self.view_zoom.get(key, 1.0)
        panx, pany = self.view_pan.get(key, (0.0, 0.0))
        cx = (cx0 + cx1) / 2 + panx
        cy = (cy0 + cy1) / 2 + pany
        return scale, cx, cy

    # ---------------------- Drawing ----------------------

    def redraw(self):
        self._clear()
        L = max(0.01, _f(self.var_L.get(), 18.0))
        B = max(0.01, _f(self.var_B.get(), 17.0))
        Hmin = max(0.01, _f(self.var_Hmin.get(), 12.0))
        Hmax = max(Hmin, _f(self.var_Hmax.get(), 12.6))
        nvers = 1 if int(_f(self.var_nvers.get(), 2)) == 1 else 2
        Hs = max(0.0, _f(self.var_Hs.get(), 0.0))

        boxes = self._get_view_boxes_with_offsets()

        for k, (x0, y0, x1, y1) in boxes.items():
            is_active = (k == self.active_view)
            outline = "#8aa7ff" if is_active else "#e1e1e1"
            width = 2 if is_active else 1
            dash = (3, 3) if self.var_move_boxes.get() else None
            self._rect(x0, y0, x1, y1, outline=outline, width=width, dash=dash)

        self._draw_elevation("Vue Arrière", "rear", boxes["rear"], L, Hmin, Hmax, nvers, Hs)
        self._draw_elevation("Vue Gauche", "left", boxes["left"], B, Hmin, Hmax, nvers, Hs)
        self._draw_plan("Vue en Plan", "plan", boxes["plan"], L, B)
        self._draw_elevation("Vue Droite", "right", boxes["right"], B, Hmin, Hmax, nvers, Hs)
        self._draw_elevation("Vue Avant", "front", boxes["front"], L, Hmin, Hmax, nvers, Hs)

        d = self._slope_dir()
        he = self._mono_high_end()
        self._text(
            10, 10,
            f"L={self._fmt_m(L)} | B={self._fmt_m(B)} | H_min={self._fmt_m(Hmin)} | H_max={self._fmt_m(Hmax)} | Versant={nvers} | Hs={self._fmt_m(Hs)} | Pente={d} | Haut={he}",
            anchor="nw", fill="#333", font=("Segoe UI", 9)
        )

    def _draw_box_label(self, title, box):
        x0, y0, x1, y1 = box
        self._text((x0 + x1) / 2, y1 - 14, title, fill="#000", font=("Segoe UI", 13, "bold"))

    def _draw_plan(self, title, key, box, L, B):
        self._draw_box_label(title, box)
        scale, cx, cy = self._view_transform(key, box, L, B)
        left = cx - (L * scale) / 2
        right = cx + (L * scale) / 2
        top = cy - (B * scale) / 2
        bot = cy + (B * scale) / 2
        self._rect(left, top, right, bot, outline="#0b3de1", width=3)
        self._draw_dim_h(left, bot, right, self._fmt_m(L), offset=18)
        self._draw_dim_v(left, top, bot, self._fmt_m(B), offset=18)

    def _draw_elevation(self, title, key, box, width_phys, Hmin, Hmax, nvers, Hs):
        self._draw_box_label(title, box)

        hL, hR, hPeak = self._heights_for_view(key, Hmin, Hmax, nvers)
        phys_h = max(hPeak, hL, hR, Hmin)

        scale, cx, cy = self._view_transform(key, box, width_phys, phys_h)

        left = cx - (width_phys * scale) / 2
        right = cx + (width_phys * scale) / 2
        bottom = cy + (phys_h * scale) / 2

        # Convert heights to canvas Y
        def y_of(h):
            return bottom - h * scale

        yL = y_of(hL)
        yR = y_of(hR)
        yMin = y_of(min(hL, hR))
        yMax = y_of(max(hL, hR, hPeak))

        # Outline:
        if nvers == 2 and hPeak > max(hL, hR):
            # gable: (left,Hmin) -> (mid,Hmax) -> (right,Hmin)
            mid = (left + right) / 2
            yE = y_of(Hmin)
            yP = y_of(hPeak)
            pts = [left, bottom, left, yE, mid, yP, right, yE, right, bottom]
            self._poly(pts, outline="#0b3de1", width=3, fill="")
            # half spans (optional, like Excel)
            self._draw_dim_h(left, yE - 2, mid, self._fmt_m(width_phys / 2), offset=-22)
            self._draw_dim_h(mid, yE - 2, right, self._fmt_m(width_phys / 2), offset=-22)
        elif abs(hL - hR) > 1e-6:
            # mono-pente profile: trapezoid top
            pts = [left, bottom, left, yL, right, yR, right, bottom]
            self._poly(pts, outline="#0b3de1", width=3, fill="")
            # draw slope line thicker for clarity
            self._line(left, yL, right, yR, fill="#0b3de1", width=3)
        else:
            # constant height rectangle
            yT = y_of(hL)
            self._rect(left, yT, right, bottom, outline="#0b3de1", width=3)

        # Dimensions
        self._draw_dim_h(left, bottom, right, self._fmt_m(width_phys), offset=18)

        h_low = min(hL, hR)
        h_high = max(hL, hR, hPeak)

        # show low height
        self._draw_dim_v(left, y_of(h_low), bottom, self._fmt_m(h_low), offset=18)

        # show high height if different (avoid overlapping)
        if abs(h_high - h_low) > 1e-6:
            self._draw_dim_v(left, y_of(h_high), bottom, self._fmt_m(h_high), offset=90)

        # Hs placeholder: small cap at the highest zone
        if Hs > 1e-6:
            cap_h = min(Hs * scale, 0.18 * (Hmin * scale))
            cap_w = 0.16 * (width_phys * scale)
            # put cap near the highest point
            if nvers == 2 and hPeak > max(hL, hR):
                cap_x0 = (left + right) / 2 - cap_w / 2
                cap_y1 = y_of(h_high)
            else:
                cap_x0 = right - cap_w if hR >= hL else left
                cap_y1 = y_of(h_high)
            cap_x1 = cap_x0 + cap_w
            cap_y0 = cap_y1 - cap_h
            self._rect(cap_x0, cap_y0, cap_x1, cap_y1, outline="#0b3de1", width=2)

    # ---------------------- end class ----------------------


def main():
    root = tk.Tk()
    BuildingSketchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
