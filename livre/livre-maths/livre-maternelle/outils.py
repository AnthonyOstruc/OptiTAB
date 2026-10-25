"""Boîte à outils des figures maternelle : chaque fonction renvoie du code TikZ (unités : cm)."""
from dataclasses import dataclass, field
from math import cos, sin, radians, hypot, pi
import random

COULEURS = ['matRouge', 'matBleu', 'matVert', 'matJaune', 'matOrange', 'matViolet', 'matRose']

def f(v):
    return f'{v:.3f}'.rstrip('0').rstrip('.') if isinstance(v, float) else str(v)

def P(nom, x, y, s=1.0, c=None, c2=None, n=None, l=None, rot=0, miroir=False):
    """Place une illustration de la bibliothèque (échelle explicite, rotation éventuelle, retournement gauche-droite).
    Les transformations doivent être données au \\pic lui-même : celles d’un scope englobant ne s’appliquent pas."""
    o = [f'scale={f(s)}']
    if miroir: o.append('xscale=-1')
    if rot: o.append(f'rotate={f(rot)}')
    if c: o.append(f'mat/c={c}')
    if c2: o.append(f'mat/c2={c2}')
    if n is not None: o.append(f'mat/n={n}')
    if l is not None: o.append(f'mat/l={f(l)}')
    return rf'\pic[{",".join(o)}] at ({f(x)},{f(y)}) {{{nom}}};'

def zone(x0, y0, x1, y1, plein=False):
    return rf'\draw[{"zone pleine" if plein else "zone"}] ({f(x0)},{f(y0)}) rectangle ({f(x1)},{f(y1)});'

def point(x, y):
    return rf'\fill[point relier] ({f(x)},{f(y)}) circle (0.17);'

def rond_reponse(x, y, r=0.36):
    """Petit rond vide à colorier sous une boîte."""
    return rf'\draw[draw=matTrait,line width=1.2pt,fill=white] ({f(x)},{f(y)}) circle ({f(r)});'

def sol(*morceaux):
    return r'\sol{' + ''.join(morceaux) + '}'

def enonce(*morceaux):
    return r'\enonce{' + ''.join(morceaux) + '}'

def trait_sol(p, q):
    return rf'\draw[sol trait] ({f(p[0])},{f(p[1])}) -- ({f(q[0])},{f(q[1])});'

def chemin_sol(pts):
    return r'\draw[sol trait] ' + ' -- '.join(f'({f(x)},{f(y)})' for x, y in pts) + ';'

def entoure_sol(x, y, rx, ry):
    return rf'\draw[sol entoure] ({f(x)},{f(y)}) ellipse ({f(rx)} and {f(ry)});'

def rond_colorie_sol(x, y, r=0.36):
    return rf'\fill[otGreen] ({f(x)},{f(y)}) circle ({f(r - 0.06)});'

def texte(x, y, t, taille=14, couleur='otInk', police=r'\otSemi', ancre='center'):
    return rf'\node[anchor={ancre},font={police}\fontsize{{{taille}}}{{{int(taille * 1.2)}}}\selectfont,text={couleur}] at ({f(x)},{f(y)}) {{{t}}};'

def chiffre(x, y, n, taille=60, couleur='otNavy'):
    return texte(x, y, str(n), taille, couleur, r'\otBold')

def fleche(p, q, couleur='otMuted', epaisseur=2.0):
    return rf'\draw[{couleur},line width={f(epaisseur)}pt,-{{Stealth[length=4mm]}}] ({f(p[0])},{f(p[1])}) -- ({f(q[0])},{f(q[1])});'

def cadre_pointille(x0, y0, x1, y1):
    return rf'\draw[pointille,rounded corners=6pt] ({f(x0)},{f(y0)}) rectangle ({f(x1)},{f(y1)});'

def constellation(x, y, n, r=0.17, pas=0.55, couleur='matTrait'):
    """Points disposés comme sur un dé (n de 1 à 6)."""
    motifs = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)],
              4: [(-1, 1), (1, 1), (-1, -1), (1, -1)], 5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
              6: [(-1, 1.1), (1, 1.1), (-1, 0), (1, 0), (-1, -1.1), (1, -1.1)]}
    return ''.join(rf'\fill[{couleur}] ({f(x + a * pas)},{f(y + b * pas)}) circle ({f(r)});' for a, b in motifs[n])

def carte_points(x, y, n, w=2.6, h=2.6):
    return (rf'\draw[draw=matTrait,line width=1.2pt,fill=white,rounded corners=5pt] ({f(x - w / 2)},{f(y - h / 2)}) rectangle ({f(x + w / 2)},{f(y + h / 2)});'
            + constellation(x, y, n, r=0.2, pas=min(w, h) * 0.24))

def forme(kind, x, y, taille=1.0, angle=0, couleur='matBleu', contour=True, plein=True):
    """Forme plane géométrique : disque, carre, triangle, rectangle (taille = demi-largeur)."""
    style = (('mat contour' if contour else '') + (f',fill={couleur}' if plein else ',fill=white')).strip(',')
    t = taille
    if kind == 'disque':
        return rf'\draw[{style}] ({f(x)},{f(y)}) circle ({f(t)});'
    if kind == 'carre':
        pts = [(-t, -t), (t, -t), (t, t), (-t, t)]
    elif kind == 'rectangle':
        pts = [(-1.5 * t, -0.8 * t), (1.5 * t, -0.8 * t), (1.5 * t, 0.8 * t), (-1.5 * t, 0.8 * t)]
    elif kind == 'triangle':
        pts = [(-1.05 * t, -0.8 * t), (1.1 * t, -0.62 * t), (-0.2 * t, 1.0 * t)]
    elif kind == 'triangle_equi':
        pts = [(t * cos(radians(a)), t * sin(radians(a))) for a in (90, 210, 330)]
    else:
        raise ValueError(kind)
    a = radians(angle)
    pts = [(x + px * cos(a) - py * sin(a), y + px * sin(a) + py * cos(a)) for px, py in pts]
    return rf'\draw[{style}] ' + ' -- '.join(f'({f(px)},{f(py)})' for px, py in pts) + ' -- cycle;'

def positions(n, kind, cx, cy, w, h, d=1.0, graine=0):
    """Positions de n objets d'encombrement d dans un rectangle (centre cx, cy ; taille w x h)."""
    if kind == 'ligne':
        if n == 1:
            return [(cx, cy)]
        pas = min(d * 1.25, (w - d) / (n - 1))
        x0 = cx - pas * (n - 1) / 2
        return [(x0 + i * pas, cy) for i in range(n)]
    if kind == 'colonne':
        if n == 1:
            return [(cx, cy)]
        pas = min(d * 1.25, (h - d) / (n - 1))
        y0 = cy + pas * (n - 1) / 2
        return [(cx, y0 - i * pas) for i in range(n)]
    if kind == 'de':
        assert 1 <= n <= 6
        motifs = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)],
                  4: [(-1, 1), (1, 1), (-1, -1), (1, -1)], 5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
                  6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}
        pas = min(d * 1.1, (min(w, h) - d) / 2)
        return [(cx + a * pas, cy + b * pas) for a, b in motifs[n]]
    if kind == 'grille':
        cols = min(n, max(1, int((w + 0.01) // (d * 1.15))))
        rows = (n + cols - 1) // cols
        pas = d * 1.15
        pts = []
        for i in range(n):
            r, c = divmod(i, cols)
            nb = cols if r < rows - 1 else n - cols * (rows - 1)
            x0 = cx - pas * (nb - 1) / 2
            pts.append((x0 + c * pas, cy + pas * (rows - 1) / 2 - r * pas))
        return pts
    if kind == 'vrac':
        if n == 1:
            return [(cx, cy)]
        rnd = random.Random(graine)
        for _ in range(4000):
            pts = []
            essais = 0
            while len(pts) < n and essais < 3000:
                essais += 1
                x = rnd.uniform(cx - w / 2 + d / 2, cx + w / 2 - d / 2)
                y = rnd.uniform(cy - h / 2 + d / 2, cy + h / 2 - d / 2)
                if all(hypot(x - a, y - b) >= d * 1.05 for a, b in pts):
                    pts.append((x, y))
            if len(pts) == n:
                return pts
        raise RuntimeError(f'impossible de placer {n} objets')
    raise ValueError(kind)

def verifier_sans_chevauchement(pts, d):
    for i, (a, b) in enumerate(pts):
        for (c, e) in pts[i + 1:]:
            assert hypot(a - c, b - e) >= d * 0.99, (pts, d)

def collection(nom, n, kind, cx, cy, w, h, s=1.0, couleurs=None, graine=0, d=None, **k):
    """Collection de n illustrations ; renvoie (code, positions)."""
    d = d if d is not None else s * 1.05
    pts = positions(n, kind, cx, cy, w, h, d, graine)
    verifier_sans_chevauchement(pts, d * 0.95)
    code = ''
    for i, (x, y) in enumerate(pts):
        c = couleurs[i % len(couleurs)] if isinstance(couleurs, list) else couleurs
        code += P(nom, x, y, s, c=c, **k)
    return code, pts

@dataclass
class Activite:
    titre: str
    consigne: str
    pictos: list
    objectif: str
    rubrique: str
    figure: str
    avant: str
    dire: str
    reponse: str
    corrige: bool = True
    quantites: list = field(default_factory=list)   # quantités à dénombrer ou nommées
    globales: list = field(default_factory=list)     # quantités comparées sans dénombrer
    controles: list = field(default_factory=list)    # couples (condition, message)
    hauteur: float = 0.0                              # hauteur de la figure en cm
    largeur: float = 0.0

def figure(*morceaux, largeur=17.0, hauteur=16.0, cadre=False):
    corps = ''.join(morceaux)
    # Pas de boîte englobante imposée : la page d’activité agrandit la figure d’après son contenu réel.
    debut = r'\begin{tikzpicture}[line cap=round,line join=round]'
    return debut + corps + r'\end{tikzpicture}', largeur, hauteur

def A(titre, consigne, pictos, objectif, rubrique, fig, avant, dire, reponse, corrige=True, quantites=(), globales=(), controles=()):
    code, w, h = fig
    return Activite(titre, consigne, list(pictos), objectif, rubrique, code, avant, dire, reponse, corrige,
                    list(quantites), list(globales), list(controles), h, w)
