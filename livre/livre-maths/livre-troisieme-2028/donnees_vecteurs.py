"""Figures sur quadrillage du chapitre Translations et vecteurs.

Chaque figure est décrite par des coordonnées entières de nœuds du quadrillage.
Les mêmes données servent au dessin (generer_figures.py) et aux contrôles
géométriques (verifier_figures.py) : égalités de vecteurs, parallélogrammes,
symétries et sommes.
"""
QUADRILLAGES = {
 'vect-01': dict(cadre=(0, 14, 0, 8),
     points={'A': (1, 1), 'B': (4, 1), 'C': (1, 3), 'O': (5, 4)},
     polygones=[['A', 'B', 'C']],
     droites=[((7, 0), (7, 8), 'd')],
     solution_points={"A'": (13, 1), "B'": (10, 1), "C'": (13, 3), "A''": (9, 7), "B''": (6, 7), "C''": (9, 5)},
     solution_polygones=[["A'", "B'", "C'"], ["A''", "B''", "C''"]]),
 'vect-02': dict(cadre=(0, 11, 0, 5),
     points={'A': (1, 1), 'B': (5, 4), 'C': (6, 1)},
     fleches=[('A', 'B')],
     solution_points={'D': (10, 4)}, solution_fleches=[('C', 'D')]),
 'vect-03': dict(cadre=(0, 12, 0, 7),
     points={'A': (1, 1), 'B': (3, 2), 'C': (5, 3), 'D': (7, 4), 'E': (9, 2), 'F': (7, 1),
             'G': (1, 4), 'H': (3, 6), 'I': (9, 4), 'J': (11, 5)},
     fleches=[('A', 'B'), ('C', 'D'), ('E', 'F'), ('G', 'H'), ('I', 'J')]),
 'vect-04': dict(cadre=(0, 9, 0, 7),
     points={'A': (1, 1), 'B': (4, 2), 'C': (2, 4)},
     fleches=[('A', 'B')],
     solution_points={'D': (5, 5)}, solution_fleches=[('C', 'D')],
     solution_polygones=[['A', 'B', 'D', 'C']]),
 'vect-05': dict(cadre=(0, 7, 0, 5),
     points={'M': (1, 1), 'N': (5, 3)},
     fleches=[('M', 'N')], solution_fleches=[('N', 'M')]),
 'vect-06': dict(cadre=(0, 9, 0, 5),
     points={'A': (1, 1), 'B': (6, 1), 'C': (8, 4), 'D': (3, 4)},
     polygones=[['A', 'B', 'C', 'D']],
     solution_fleches=[('A', 'B'), ('D', 'C')]),
 'vect-07': dict(cadre=(0, 8, 0, 6),
     points={'E': (1, 1), 'F': (5, 2), 'G': (7, 5), 'H': (3, 4)},
     fleches=[('E', 'F'), ('H', 'G')],
     solution_polygones=[['E', 'F', 'G', 'H']]),
 'vect-08': dict(cadre=(0, 9, 0, 5),
     points={'A': (1, 1), 'B': (4, 4), 'C': (8, 2)},
     fleches=[('A', 'B'), ('B', 'C')], solution_fleches=[('A', 'C')]),
 'vect-09': dict(cadre=(0, 11, 0, 6),
     points={'O': (1, 1)},
     vecteurs_libres=[((6, 4), (9, 5), 'u'), ((9, 1), (10, 3), 'v')],
     solution_points={'P': (4, 2), 'S': (5, 4)},
     solution_fleches=[('O', 'P'), ('P', 'S'), ('O', 'S')]),
 'vect-10': dict(cadre=(0, 9, 0, 8),
     points={'A': (1, 1), 'B': (4, 2), 'C': (5, 4), 'M': (2, 4)},
     fleches=[('A', 'B'), ('B', 'C')],
     solution_points={"M'": (5, 5), "M''": (6, 7)},
     solution_fleches=[('M', "M'"), ("M'", "M''"), ('M', "M''")]),
 'vect-11': dict(cadre=(0, 9, 0, 5),
     points={'A': (1, 1), 'B': (6, 1), 'C': (8, 4), 'D': (3, 4)},
     polygones=[['A', 'B', 'C', 'D']],
     fleches=[('A', 'B'), ('A', 'D')], solution_fleches=[('A', 'C')]),
 'vect-12': dict(cadre=(0, 10, 0, 3),
     points={'A': (1, 1), 'B': (9, 1)},
     segments=[('A', 'B')],
     solution_points={'I': (5, 1)}, solution_fleches=[('A', 'I'), ('I', 'B')]),
 'vect-13': dict(cadre=(0, 6, 0, 6),
     points={'D': (1, 1)},
     unite='1 carreau pour 20 m',
     solution_points={'E': (4, 1), 'F': (4, 5)},
     solution_fleches=[('D', 'E'), ('E', 'F'), ('D', 'F')]),
 'vect-15': dict(cadre=(0, 10, 0, 5),
     points={'A': (1, 1), 'B': (5, 1), 'C': (7, 4), 'D': (3, 4), 'E': (9, 1)},
     polygones=[['A', 'B', 'C', 'D']],
     segments=[('B', 'E')],
     solution_polygones=[['D', 'C', 'E', 'B']]),
}


def vecteur(fig, p, q):
    pts = dict(QUADRILLAGES[fig]['points'])
    pts.update(QUADRILLAGES[fig].get('solution_points', {}))
    return (pts[q][0] - pts[p][0], pts[q][1] - pts[p][1])


def point(fig, p):
    pts = dict(QUADRILLAGES[fig]['points'])
    pts.update(QUADRILLAGES[fig].get('solution_points', {}))
    return pts[p]
