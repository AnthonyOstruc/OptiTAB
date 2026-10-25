"""Gabarits de figures réutilisés par les trois cahiers (boîtes à colorier, colonnes à relier, rangées)."""
from outils import *

def boites_rond(contenus, cible, largeur=17.0, colonnes=2, h_boite=4.4, w_boite=7.6):
    """contenus : liste de (code_tikz_fonction(cx, cy) -> code, nombre). Rond à colorier sous chaque boîte.
    Les ronds des boîtes dont le nombre vaut cible sont coloriés dans la solution."""
    n = len(contenus)
    lignes = (n + colonnes - 1) // colonnes
    pas_x = (largeur - w_boite) / (colonnes - 1) if colonnes > 1 else 0
    pas_y = h_boite + 1.9
    hauteur = lignes * pas_y + 0.2
    code = ''
    bons = 0
    for i, (dessin, nombre) in enumerate(contenus):
        r, c = divmod(i, colonnes)
        cx = w_boite / 2 + c * pas_x
        cy = hauteur - 0.2 - h_boite / 2 - r * pas_y
        code += zone(cx - w_boite / 2, cy - h_boite / 2, cx + w_boite / 2, cy + h_boite / 2)
        code += dessin(cx, cy, w_boite - 0.6, h_boite - 0.6)
        code += rond_reponse(cx, cy - h_boite / 2 - 0.75)
        if nombre == cible:
            code += sol(rond_colorie_sol(cx, cy - h_boite / 2 - 0.75))
            bons += 1
    return code, hauteur, bons

def coll(nom, n, kind='vrac', s=1.0, couleurs=None, graine=0, **k):
    """Fabrique une fonction de dessin de collection utilisable dans boites_rond."""
    def dessin(cx, cy, w, h):
        code, _ = collection(nom, n, kind, cx, cy, w, h, s=s, couleurs=couleurs or COULEURS, graine=graine, **k)
        return code
    return dessin

def relier(gauche, droite, appariement, largeur=17.0, pas=4.0, x_g=2.8, x_d=14.2, ecart_point=2.2):
    """gauche, droite : listes de fonctions dessin(cx, cy) ; appariement[i] = indice à droite relié au i-ème à gauche."""
    n = max(len(gauche), len(droite))
    hauteur = n * pas
    code = ''
    yg = [hauteur - pas / 2 - i * pas for i in range(len(gauche))]
    yd = [hauteur - pas / 2 - i * pas for i in range(len(droite))]
    pg = [(x_g + ecart_point, y) for y in yg]
    pd = [(x_d - ecart_point, y) for y in yd]
    for i, d in enumerate(gauche):
        code += d(x_g, yg[i]) + point(*pg[i])
    for j, d in enumerate(droite):
        code += d(x_d, yd[j]) + point(*pd[j])
    code += sol(*[trait_sol(pg[i], pd[j]) for i, j in enumerate(appariement) if j is not None])
    return code, hauteur

def melange(n, graine):
    """Permutation déterministe sans point fixe (pour éviter les liens horizontaux trop évidents)."""
    rnd = random.Random(graine)
    while True:
        p = list(range(n))
        rnd.shuffle(p)
        if n == 1 or all(p[i] != i for i in range(n)):
            return p

# ------------------------------------------------------------------ gabarits ajoutés pour la MS et la GS
def mixte(nom, tailles, couleurs, ecart=2.0):
    """Rangée d’objets de tailles différentes (même quantité, tailles variées)."""
    def dessin(cx, cy, w, h):
        n = len(tailles)
        x0 = cx - ecart * (n - 1) / 2
        return ''.join(P(nom, x0 + i * ecart, cy + (0.4 if i % 2 else -0.3), s, c=couleurs[i % len(couleurs)]) for i, s in enumerate(tailles))
    return dessin

def boite_objets(nom, n, s=1.2, couleurs=None, kind='ligne', w=5.4, h=2.6, graine=0):
    """Boîte encadrée contenant n objets ; renvoie une fonction dessin(x, y) pour relier()."""
    def dessin(x, y):
        code = zone(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
        c, _ = collection(nom, n, kind, x, y, w - 0.4, h - 0.4, s=s, couleurs=couleurs or ['matRouge'], graine=graine)
        return code + c
    return dessin

def piste(x0, y, n, w=1.9, h=1.9, depart=True):
    """Piste du jeu de l’oie : n cases alignées ; la première porte un drapeau de départ. Renvoie (code, centres)."""
    code, centres = '', []
    for i in range(n):
        x = x0 + i * w
        code += rf'\draw[mat contour,fill={"matVert!25" if (depart and i == 0) else "white"},rounded corners=3pt] ({f(x + 0.06)},{f(y - h / 2)}) rectangle ({f(x + w - 0.06)},{f(y + h / 2)});'
        centres.append((x + w / 2, y))
    return code, centres

def bande(x0, y, nombres, w=2.4, h=2.4, taille=30, vides=(), couleur='otNavy'):
    """Bande numérique : une case par nombre ; les nombres de « vides » ne sont pas écrits. Renvoie (code, centres)."""
    code, centres = '', []
    for i, n in enumerate(nombres):
        x = x0 + i * w
        code += rf'\draw[mat contour,fill=white] ({f(x)},{f(y - h / 2)}) rectangle ({f(x + w)},{f(y + h / 2)});'
        if n not in vides:
            code += texte(x + w / 2, y, str(n), taille, couleur, r'\otBold')
        centres.append((x + w / 2, y))
    return code, centres

def sur_balance(x, y, s, n, gauche, droite):
    """Balance de Roberval (n : -1 penche à gauche, 0 équilibre, 1 à droite) ; gauche et droite dessinent un objet
    posé sur le plateau : fonction (x, y_du_plateau) -> code."""
    a = radians(-8 * n)
    gx, gy = x - 1.05 * s * cos(a), y - 1.05 * s * sin(a) + 0.44 * s
    dx, dy = x + 1.05 * s * cos(a), y + 1.05 * s * sin(a) + 0.44 * s
    return P('balance', x, y, s, n=n) + gauche(gx, gy) + droite(dx, dy)

def chiffre_trace(x, y, n, taille=66, modele=False):
    """Chiffre modèle (bleu) ou chiffre gris à repasser."""
    return texte(x, y, str(n), taille, 'otNavy' if modele else 'matGris!40', r'\otMedium')

def labyrinthe(cols, lignes, graine, x0, y0, pas):
    """Labyrinthe parfait (un seul chemin) ; entrée en haut à gauche, sortie en bas à droite.
    Renvoie (code des murs, liste des centres du chemin solution)."""
    rnd = random.Random(graine)
    murs = {(c, l, d) for c in range(cols) for l in range(lignes) for d in 'ED'}  # E : mur à droite, D : mur en dessous
    vu = {(0, 0)}
    pile = [(0, 0)]
    while pile:
        c, l = pile[-1]
        voisins = [(c + dc, l + dl) for dc, dl in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if 0 <= c + dc < cols and 0 <= l + dl < lignes and (c + dc, l + dl) not in vu]
        if not voisins:
            pile.pop()
            continue
        nc, nl = rnd.choice(voisins)
        if nc != c:
            murs.discard((min(c, nc), l, 'E'))
        else:
            murs.discard((c, min(l, nl), 'D'))
        vu.add((nc, nl))
        pile.append((nc, nl))
    # Recherche du chemin (largeur d’abord) : vérifie que la sortie est atteignable et donne la solution.
    def ouverts(c, l):
        for dc, dl in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nc, nl = c + dc, l + dl
            if not (0 <= nc < cols and 0 <= nl < lignes):
                continue
            mur = (min(c, nc), l, 'E') if dc else (c, min(l, nl), 'D')
            if mur not in murs:
                yield nc, nl
    prec = {(0, 0): None}
    file = [(0, 0)]
    while file:
        cel = file.pop(0)
        for v in ouverts(*cel):
            if v not in prec:
                prec[v] = cel
                file.append(v)
    assert (cols - 1, lignes - 1) in prec, 'labyrinthe sans issue'
    chemin, cel = [], (cols - 1, lignes - 1)
    while cel is not None:
        chemin.append(cel)
        cel = prec[cel]
    chemin.reverse()
    X = lambda c: x0 + c * pas
    Y = lambda l: y0 - l * pas          # la ligne 0 est en haut
    code = rf'\draw[mat contour,line width=2.6pt] ({f(X(0))},{f(Y(0))}) -- ({f(X(cols))},{f(Y(0))}) -- ({f(X(cols))},{f(Y(lignes - 1))});'
    code += rf'\draw[mat contour,line width=2.6pt] ({f(X(cols))},{f(Y(lignes))}) -- ({f(X(0))},{f(Y(lignes))}) -- ({f(X(0))},{f(Y(1))});'
    for (c, l, d) in sorted(murs):
        if d == 'E' and c < cols - 1:
            code += rf'\draw[mat contour,line width=2.6pt] ({f(X(c + 1))},{f(Y(l))}) -- ({f(X(c + 1))},{f(Y(l + 1))});'
        if d == 'D' and l < lignes - 1:
            code += rf'\draw[mat contour,line width=2.6pt] ({f(X(c))},{f(Y(l + 1))}) -- ({f(X(c + 1))},{f(Y(l + 1))});'
    centres = [(X(c) + pas / 2, Y(l) - pas / 2) for c, l in chemin]
    return code, centres

def tas(nom, n, cx, y_bas, s, couleurs, d=None):
    """n objets ronds empilés en quinconce (rangées de k, k-1, … objets), la première rangée posée en y_bas.
    Renvoie (code, positions)."""
    d = d if d is not None else s * 0.63
    k = 1
    while k * (k + 1) // 2 < n:
        k += 1
    pts, reste, r, j = [], n, k, 0
    while reste > 0:
        m = min(r, reste)
        y = y_bas + d / 2 + j * 0.87 * d
        pts += [(cx + (i - (m - 1) / 2) * d, y) for i in range(m)]
        reste -= m
        r -= 1
        j += 1
    code = ''.join(P(nom, x, y, s, c=couleurs[i % len(couleurs)]) for i, (x, y) in enumerate(pts))
    return code, pts
