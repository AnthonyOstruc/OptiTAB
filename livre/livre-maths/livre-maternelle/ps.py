"""Cahier de Petite Section : 40 activités, programme « à aborder avant 4 ans »."""
from outils import *
from gabarits import *

NIVEAU = dict(cle='ps', nom='Petite Section', court='PS', age='avant 4 ans', accent='otGreen',
              couv=(3, 3), max_quantite=4, max_globale=12)

R = {
 'R1': 'Comprendre qu’une quantité ne dépend ni de la nature des objets ni de leur organisation',
 'R2': 'Ajouter un : la quantité suivante, le nombre suivant',
 'R3': 'Dénombrer une collection (jusqu’à trois, voire quatre)',
 'R4': 'Constituer une collection d’un cardinal donné',
 'R5': 'Comparer des quantités (globalement, terme à terme)',
 'R6': 'Composer et décomposer deux, trois, voire quatre',
 'R7': 'Associer une quantité, le nom d’un nombre et son écriture chiffrée',
 'R8': 'Connaître la comptine numérique de un à six',
 'R9': 'Problèmes : rechercher le tout ou une partie',
 'R10': 'Formes : reconnaître, trier, classer, encastrer, reproduire',
 'R11': 'Longueurs : reconnaître et comparer',
 'R12': 'Motifs : mémoriser, reproduire, compléter',
 'R13': 'Se repérer dans l’espace : vocabulaire et parcours',
}

def boite_simple(nom, n, kind='vrac', s=1.95, graine=1, couleurs=None):
    return coll(nom, n, kind, s=s, couleurs=couleurs, graine=graine)

# ------------------------------------------------------------------ partie 1
def panier_tas(cx, y0, n, s, couleurs, W=6.9, H=2.6):
    """Grand panier en osier (fond en y0) avec n pommes en tas : rangées de k, k-1, … pommes."""
    d = s * 1.05
    k = 1
    while k * (k + 1) // 2 < n:
        k += 1
    rangs, reste = [], n
    while reste > 0:
        rangs.append(min(k, reste))
        reste -= rangs[-1]
        k -= 1
    haut = y0 + H
    code = (rf'\draw[matBrun!70!black,line width=3.2pt] ({f(cx - 0.36 * W)},{f(haut)}) .. controls ({f(cx - 0.36 * W)},{f(haut + 5.0)}) '
            rf'and ({f(cx + 0.36 * W)},{f(haut + 5.0)}) .. ({f(cx + 0.36 * W)},{f(haut)});')
    i = 0
    for j, r in enumerate(rangs):
        y = haut + 0.3 + j * 0.86 * d
        for m in range(r):
            code += P('pomme', cx + (m - (r - 1) / 2) * d, y, s, c=couleurs[i % len(couleurs)])
            i += 1
    code += (rf'\draw[mat contour,fill=matBrun!70] ({f(cx - W / 2)},{f(haut)}) -- ({f(cx + W / 2)},{f(haut)}) -- '
             rf'({f(cx + 0.4 * W)},{f(y0)}) -- ({f(cx - 0.4 * W)},{f(y0)}) -- cycle;')
    for t in (0.36, 0.68):
        y = y0 + t * H
        demi = 0.4 * W + t * 0.1 * W
        code += rf'\draw[mat fin] ({f(cx - demi)},{f(y)}) -- ({f(cx + demi)},{f(y)});'
    for u in (-0.25, 0, 0.25):
        code += rf'\draw[mat fin] ({f(cx + u * 0.8 * W)},{f(y0)}) -- ({f(cx + u * W)},{f(haut)});'
    code += rf'\draw[mat contour,fill=matBrun!85,rounded corners=3pt] ({f(cx - W / 2 - 0.2)},{f(haut - 0.3)}) rectangle ({f(cx + W / 2 + 0.2)},{f(haut + 0.12)});'
    return code, sum(rangs)

def a_beaucoup():
    g, ng = panier_tas(4.25, 1.0, 2, 1.5, ['matRouge', 'matVert'])
    d, nd = panier_tas(12.75, 1.0, 8, 1.5, ['matRouge', 'matRouge', 'matVert'])
    fig = figure(zone(0.3, 0.4, 8.2, 9.4), zone(8.8, 0.4, 16.7, 9.4), g, d,
                 sol(entoure_sol(12.75, 4.9, 4.5, 5.2)), hauteur=9.8)
    return A('Beaucoup ou peu ?', 'Entoure le panier où il y a <b>beaucoup</b> de pommes.', ['entourer'],
             'Comparer globalement deux quantités très différentes et dire « plus que », « moins que ».', 'R5', fig,
             'Mettre huit jetons dans un pot transparent et deux dans un autre ; demander, sans compter, où il y en a le plus.',
             '« Ici, il y a beaucoup de pommes. Là, il y en a peu : il y en a moins. »',
             'Le panier de droite : il contient huit pommes, celui de gauche deux seulement. On ne demande pas de compter.',
             globales=[ng, nd], controles=[((ng, nd) == (2, 8), 'deux et huit pommes dessinées')])

def a_oiseaux():
    code = zone(0.3, 0.4, 8.2, 13.2) + zone(8.8, 0.4, 16.7, 13.2)
    code += P('arbre', 4.25, 6.2, 8.0) + P('arbre', 12.75, 6.2, 8.0)
    g, _ = collection('oiseau', 7, 'vrac', 4.25, 8.6, 6.0, 4.4, s=1.05, couleurs=['matBleu', 'matJaune', 'matRouge'], graine=11)
    d, _ = collection('oiseau', 3, 'vrac', 12.75, 8.6, 6.0, 4.4, s=1.05, couleurs=['matBleu', 'matJaune', 'matRouge'], graine=12)
    fig = figure(code, g, d, sol(entoure_sol(12.75, 6.8, 4.5, 6.9)), hauteur=13.8)
    return A('Le moins d’oiseaux', 'Entoure l’arbre où il y a le <b>moins</b> d’oiseaux.', ['entourer'],
             'Comparer globalement deux quantités très différentes et dire « moins que ».', 'R5', fig,
             'Poser beaucoup de cubes sur une assiette et seulement quelques-uns sur une autre ; demander où il y en a moins.',
             '« Sur cet arbre, il y a moins d’oiseaux. Sur l’autre, il y en a plus. »',
             'L’arbre de droite (trois oiseaux contre sept). La comparaison se fait d’un coup d’œil, sans compter.',
             globales=[7, 3])

def a_lapins():
    perm = melange(3, 5)
    cols = ['matRouge', 'matGris', 'matJaune']
    gauche = [lambda x, y, c=c: P('lapin', x, y, 2.2, c=c) for c in cols]
    droite = [lambda x, y: P('carotte', x, y, 2.4)] * 3
    code, h = relier(gauche, droite, perm, pas=4.4)
    return A('Une carotte pour chaque lapin', 'Relie chaque lapin à une carotte. Y a-t-il une carotte pour chaque lapin ?',
             ['relier', 'dire'], 'Comparer deux collections par correspondance terme à terme.', 'R5', figure(code, hauteur=h),
             'Mettre la table pour des peluches : une assiette devant chaque peluche, puis vérifier qu’aucune n’est oubliée.',
             '« Chaque lapin a sa carotte. Il y a autant de lapins que de carottes. »',
             'Oui : chaque lapin reçoit une carotte et aucune carotte ne reste seule. N’importe quel appariement convient.')

def a_gateaux():
    code = ''
    xs_a = [1.9 + i * 3.3 for i in range(5)]
    xs_g = [2.4, 5.9, 9.9, 13.6]
    for x in xs_a:
        code += P('assiette', x, 10.4, 2.4) + point(x, 8.9)
    for i, x in enumerate(xs_g):
        code += P('gateau', x, 3.0 + (0.5 if i % 2 else 0), 2.0, c=COULEURS[i]) + point(x, 5.2 + (0.5 if i % 2 else 0))
    sols = [trait_sol((xs_g[i], 5.2 + (0.5 if i % 2 else 0)), (xs_a[i], 8.9)) for i in range(4)]
    sols.append(P('gateau', xs_a[4], 12.6, 1.6, c='otGreen'))
    fig = figure(code, sol(*sols), hauteur=14.0)
    return A('Il manque un gâteau', 'Relie chaque gâteau à une assiette. Dessine le gâteau qui manque.', ['relier', 'dessiner'],
             'Comparer par correspondance terme à terme, même avec des collections plus grandes que les nombres connus.', 'R5', fig,
             'Distribuer un gâteau (un jeton) par assiette et constater qu’une assiette reste vide.',
             '« Il y a une assiette sans gâteau. Il manque un gâteau. »',
             'Il y a cinq assiettes et quatre gâteaux : une assiette reste vide, l’enfant dessine un gâteau pour elle.')

def a_ours():
    code = ''
    xs_o = [2.1 + i * 4.25 for i in range(4)]
    xs_c = [3.6, 8.5, 13.4]
    for i, x in enumerate(xs_o):
        code += P('ours', x, 10.6, 2.2, c=['matBrun', 'matOrange', 'matBrun', 'matJaune'][i]) + point(x, 8.7)
    for x in xs_c:
        code += P('chaise', x, 3.3, 3.0, c='matBleu') + point(x, 5.4)
    sols = [trait_sol((xs_o[i], 8.7), (xs_c[i], 5.4)) for i in range(3)] + [entoure_sol(xs_o[3], 10.6, 1.5, 1.5)]
    fig = figure(code, sol(*sols), hauteur=12.5)
    return A('Une chaise pour chaque ours', 'Relie chaque ours à une chaise. Entoure l’ours qui n’a pas de chaise.', ['relier', 'entourer'],
             'Comparer deux collections par correspondance terme à terme.', 'R5', fig,
             'Jeu des chaises avec des peluches : un ours par chaise, puis repérer celui qui reste debout.',
             '« Il y a plus d’ours que de chaises. Un ours n’a pas de chaise. »',
             'Quatre ours et trois chaises : un ours reste sans chaise. Celui que l’on entoure dépend des liens tracés.')

def a_elephants():
    code = ''
    xs_e = [2.4, 8.5, 14.6]
    xs_f = [6.3, 8.5, 10.7]
    for x in xs_e:
        code += P('elephant', x, 9.6, 3.6) + point(x, 7.4)
    for x in xs_f:
        code += P('fourmi', x, 2.6, 1.7) + point(x, 4.0)
    sols = [trait_sol((xs_f[i], 4.0), (xs_e[i], 7.4)) for i in range(3)]
    fig = figure(code, sol(*sols), hauteur=12.0)
    return A('Éléphants et fourmis', 'Relie chaque éléphant à une fourmi. Y a-t-il autant d’éléphants que de fourmis ?', ['relier', 'dire'],
             'Comprendre qu’une quantité ne dépend ni de la taille ni de la place des objets.', 'R1', fig,
             'Aligner trois gros objets et trois petits objets serrés ; demander s’il y en a autant, puis vérifier en les appariant.',
             '« Les éléphants sont gros, les fourmis sont petites, mais il y en a autant : trois et trois. »',
             'Oui, il y en a autant : trois éléphants et trois fourmis. La taille des animaux ne change pas la quantité.',
             quantites=[3])

# ------------------------------------------------------------------ partie 2
def a_un_seul():
    contenus = [(boite_simple('ballon', 1), 1), (boite_simple('poisson', 2, 'ligne', graine=2), 2), (boite_simple('voiture', 1), 1),
                (boite_simple('fleur', 2, graine=4), 2), (boite_simple('etoile', 1), 1), (boite_simple('pomme', 2, graine=6, couleurs=['matRouge', 'matVert']), 2)]
    code, h, bons = boites_rond(contenus, 1)
    return A('Un seul', 'Colorie le rond sous chaque boîte où il y a <b>un seul</b> objet.', ['colorier'],
             'Percevoir globalement une petite quantité : un, deux.', 'R3', figure(code, hauteur=h),
             'Montrer des boîtes contenant un ou deux objets ; demander de montrer celles où il y a « un seul » objet.',
             '« Là, il y a un ballon : un seul. Là, il y a deux poissons. »',
             f'Les {bons} boîtes du ballon, de la voiture et de l’étoile.', quantites=[1, 2],
             controles=[(bons == 3, 'trois boîtes à un objet')])

def mixte(nom, tailles, couleurs, ecart=2.0):
    def dessin(cx, cy, w, h):
        n = len(tailles)
        x0 = cx - ecart * (n - 1) / 2
        return ''.join(P(nom, x0 + i * ecart, cy + (0.4 if i % 2 else -0.3), s, c=couleurs[i % len(couleurs)]) for i, s in enumerate(tailles))
    return dessin

def a_deux():
    contenus = [(boite_simple('canard', 2, 'ligne', couleurs=['matJaune']), 2), (boite_simple('bonbon', 3, graine=8), 3),
                (mixte('coccinelle', [2.5, 1.3], ['matRouge'], 2.8), 2), (boite_simple('ours', 1, couleurs=['matBrun']), 1),
                (boite_simple('cle', 2, graine=9, couleurs=['matJaune', 'matBleu']), 2), (boite_simple('etoile', 3, 'ligne'), 3)]
    code, h, bons = boites_rond(contenus, 2)
    return A('Deux', 'Colorie le rond sous chaque boîte où il y a <b>deux</b> objets.', ['colorier'],
             'Reconnaître des collections de deux objets de tailles et de dispositions différentes.', 'R1', figure(code, hauteur=h),
             'Faire des paires d’objets très différents (deux cuillères, deux voitures, une grosse et une petite balle).',
             '« Il y a deux coccinelles : une grosse et une petite. Deux, c’est un et encore un. »',
             'Les boîtes des canards, des coccinelles et des clés : trois boîtes. La grosse et la petite coccinelle font bien deux.',
             quantites=[1, 2, 3], controles=[(bons == 3, 'trois boîtes à deux objets')])

def a_trois():
    contenus = [(boite_simple('poisson', 3, 'ligne', couleurs=['matOrange', 'matBleu']), 3), (boite_simple('fleur', 2, graine=21), 2),
                (boite_simple('champignon', 3, graine=23, couleurs=['matRouge']), 3), (boite_simple('voiture', 1), 1),
                (mixte('ballon', [1.3, 2.4, 1.7], ['matBleu', 'matRouge', 'matVert'], 2.3), 3), (boite_simple('lapin', 2, 'ligne', couleurs=['matGris']), 2)]
    code, h, bons = boites_rond(contenus, 3)
    return A('Trois', 'Colorie le rond sous chaque boîte où il y a <b>trois</b> objets.', ['colorier'],
             'Reconnaître des collections de trois objets, quelle que soit leur disposition.', 'R3', figure(code, hauteur=h),
             'Montrer trois jetons alignés, puis en triangle, puis en vrac : c’est toujours trois.',
             '« Un, et encore un, et encore un : trois. »',
             'Les boîtes des poissons, des champignons et des ballons. Les ballons ont des tailles différentes mais sont bien trois.',
             quantites=[1, 2, 3], controles=[(bons == 3, 'trois boîtes à trois objets')])

def a_un_de_plus():
    code = ''
    sols = []
    for r, k in enumerate([1, 2, 3]):
        y = 12.6 - r * 4.4
        code += zone(0.6, y - 1.6, 6.6, y + 1.6) + cadre_pointille(10.4, y - 1.6, 16.4, y + 1.6)
        c, _ = collection('jeton', k, 'ligne', 3.6, y, 5.6, 2.8, s=1.5, couleurs=['matBleu'])
        code += c + fleche((7.3, y), (9.7, y), 'matAccent' if False else 'otGreen', 3)
        c2, _ = collection('jeton', k + 1, 'ligne', 13.4, y, 5.6, 2.8, s=1.25, couleurs=['otGreen'])
        sols.append(c2)
    fig = figure(code, sol(*sols), hauteur=14.4)
    return A('Un de plus', 'Dans chaque boîte de droite, dessine <b>un rond de plus</b> que dans la boîte de gauche.', ['dessiner'],
             'Réaliser une collection contenant un objet de plus qu’une collection donnée.', 'R2', fig,
             'Donner une voiture, puis dire : « Je me suis trompé, j’en voulais deux » ; l’enfant en ajoute une.',
             '« Un, et encore un, ça fait deux. Deux, et encore un, ça fait trois. »',
             'Deux ronds, puis trois ronds, puis quatre ronds.', quantites=[1, 2, 3, 4])

def boite_objets(nom, n, s=1.2, couleurs=None, kind='ligne', w=5.4, h=2.6):
    def dessin(x, y):
        code = zone(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
        c, _ = collection(nom, n, kind, x, y, w - 0.4, h - 0.4, s=s, couleurs=couleurs or ['matRouge'])
        return code + c
    return dessin

def a_mains():
    gauches = [2, 3, 1]
    droites = [3, 1, 2]
    g = [lambda x, y, n=n: P('main', x, y, 2.9, n=n) for n in gauches]
    d = [boite_objets('pomme', n, couleurs=['matRouge', 'matVert']) for n in droites]
    perm = [droites.index(n) for n in gauches]
    code, h = relier(g, d, perm, pas=4.6, x_g=2.6, x_d=14.0, ecart_point=3.3)
    return A('Mes doigts', 'Relie chaque main à la boîte qui a <b>autant</b> de pommes que de doigts levés.', ['relier'],
             'Associer une quantité à sa représentation avec les doigts.', 'R7', figure(code, hauteur=h),
             'Montrer deux, puis trois doigts ; l’enfant prend autant de jetons, puis montre lui-même ses doigts.',
             '« Deux doigts, deux pommes. Trois doigts, trois pommes. »',
             'Deux doigts avec la boîte de deux pommes, trois doigts avec celle de trois, un doigt avec celle d’une pomme.',
             quantites=[1, 2, 3])

def a_des():
    gauches = [3, 1, 2]
    droites = [1, 2, 3]
    g = [lambda x, y, n=n: P('de', x, y, 2.3, n=n) for n in gauches]
    d = [boite_objets('bonbon', n, couleurs=['matRose', 'matBleu', 'matJaune'], s=1.5) for n in droites]
    perm = [droites.index(n) for n in gauches]
    code, h = relier(g, d, perm, pas=4.4, x_d=14.0, ecart_point=3.3)
    return A('Le dé et les bonbons', 'Relie chaque dé à la boîte qui a <b>autant</b> de bonbons que de points.', ['relier'],
             'Associer une constellation de points à la quantité correspondante.', 'R7', figure(code, hauteur=h),
             'Lancer un grand dé et prendre autant de jetons qu’il y a de points.',
             '« Trois points sur le dé, trois bonbons dans la boîte. »',
             'Le dé à trois points avec la boîte de trois bonbons, celui à un point avec la boîte d’un bonbon, celui à deux points avec celle de deux.',
             quantites=[1, 2, 3])

def a_autant_points():
    code = ''
    sols = []
    for r, k in enumerate([2, 1, 3]):
        y = 12.4 - r * 4.4
        code += carte_points(2.6, y, k, w=3.0, h=3.0) + fleche((4.6, y), (7.4, y), 'otGreen', 3) + cadre_pointille(8.2, y - 1.7, 16.4, y + 1.7)
        c, _ = collection('jeton', k, 'ligne', 12.3, y, 7.0, 2.8, s=1.3, couleurs=['otGreen'])
        sols.append(c)
    fig = figure(code, sol(*sols), hauteur=14.2)
    return A('Autant que sur la carte', 'Dessine dans chaque boîte <b>autant</b> de ronds qu’il y a de points sur la carte.', ['dessiner'],
             'Constituer une collection de même quantité qu’une représentation de points.', 'R4', fig,
             'Situation des boîtes : poser dans chaque boîte autant de jetons que de points sur son étiquette.',
             '« Sur la carte, il y a deux points ; je dessine deux ronds. »',
             'Deux ronds, puis un rond, puis trois ronds.', quantites=[1, 2, 3])

def a_deux_mains():
    code = ''
    sols = []
    lignes_ = [(1, 1), (2, 1), (1, 2)]
    for r, (a, b) in enumerate(lignes_):
        y = 12.6 - r * 4.5
        code += zone(0.3, y - 1.9, 6.9, y + 1.9) + P('main', 1.95, y, 2.6, n=a) + P('main', 5.25, y, 2.6, n=b)
        for k, v in enumerate([1, 2, 3]):
            code += P('de', 9.3 + k * 2.9, y, 2.0, n=v)
        sols.append(entoure_sol(9.3 + (a + b - 1) * 2.9, y, 1.35, 1.35))
    fig = figure(code, sol(*sols), hauteur=14.6)
    return A('Les doigts des deux mains', 'Combien de doigts sont levés en tout ? Entoure le dé qui montre <b>autant</b> de points.', ['entourer', 'dire'],
             'Composer deux et trois avec les doigts des deux mains.', 'R6', fig,
             'Lever un doigt sur chaque main et demander combien cela fait ; recommencer avec deux et un.',
             '« Un et un, ça fait deux. Deux et un, ça fait trois. Un et deux, ça fait trois aussi. »',
             'Deux, puis trois, puis trois : l’ordre des mains ne change pas le total.', quantites=[1, 2, 3])

def a_trains():
    code = ''
    sols = []
    trains = [2, 3, 3]
    choix = [['matRouge', 'matBleu'], ['matRouge', 'matBleu', 'matBleu'], ['matRouge', 'matRouge', 'matBleu']]
    for r, n in enumerate(trains):
        y = 12.2 - r * 4.4
        code += P('locomotive', 2.0, y, 2.6, c='otNavy!70')
        for k in range(n):
            code += P('wagon', 5.0 + k * 2.9, y - 0.12, 2.6, c='white')
            sols.append(P('wagon', 5.0 + k * 2.9, y - 0.12, 2.6, c=choix[r][k]))
    fig = figure(code, sol(*sols), hauteur=14.0)
    return A('Des trains de deux couleurs', 'Colorie les wagons de chaque train en rouge et en bleu. Utilise les deux couleurs dans chaque train.', ['colorier'],
             'Décomposer deux et trois : deux, c’est un et un ; trois, c’est un et deux.', 'R6', fig,
             'Faire des tours de deux ou trois cubes de deux couleurs et comparer les différentes tours obtenues.',
             '« Mon train a un wagon rouge et deux wagons bleus : trois, c’est un et deux. »',
             'Deux wagons : un rouge et un bleu. Trois wagons : un et deux, ou deux et un. Toutes les solutions qui utilisent les deux couleurs conviennent.',
             quantites=[2, 3])

def a_quatre():
    contenus = [(boite_simple('fraise', 4, graine=31, couleurs=['matRouge']), 4), (boite_simple('poire', 3, 'ligne', couleurs=['matJaune']), 3),
                (boite_simple('jeton', 4, 'de', s=1.6, couleurs=['matViolet']), 4), (boite_simple('papillon', 2, graine=33, couleurs=['matBleu', 'matRose']), 2),
                (boite_simple('etoile', 4, 'ligne', s=1.5, couleurs=['matJaune', 'matOrange']), 4), (boite_simple('poisson', 3, graine=35, couleurs=['matOrange']), 3)]
    code, h, bons = boites_rond(contenus, 4)
    return A('Quatre', 'Colorie le rond sous chaque boîte où il y a <b>quatre</b> objets.', ['colorier'],
             'Dénombrer une collection jusqu’à quatre, en déplaçant ou en pointant les objets.', 'R3', figure(code, hauteur=h),
             'À aborder seulement quand deux et trois sont bien compris : compter des jetons en les déplaçant un à un.',
             '« Un, deux, trois, quatre : il y en a quatre. »',
             'Les boîtes des fraises, des jetons violets et des étoiles.', quantites=[2, 3, 4],
             controles=[(bons == 3, 'trois boîtes à quatre objets')])

def a_chiffres():
    gauches = [2, 1, 3]
    droites = [1, 3, 2]
    g = [lambda x, y, n=n: chiffre(x, y, n, 72) for n in gauches]
    d = [boite_objets('etoile', n, couleurs=['matJaune', 'matOrange'], s=1.1) for n in droites]
    perm = [droites.index(n) for n in gauches]
    code, h = relier(g, d, perm, pas=4.4, x_d=14.0, ecart_point=3.3)
    return A('Les chiffres 1, 2, 3', 'Relie chaque chiffre à la boîte qui a <b>autant</b> d’étoiles.', ['relier'],
             'Associer une écriture chiffrée à une quantité (jusqu’à trois).', 'R7', figure(code, hauteur=h),
             'Montrer le chiffre écrit sur une carte, le nommer, et le faire correspondre à des collections de jetons.',
             '« Ça, c’est le chiffre deux : il faut deux étoiles. »',
             '2 avec la boîte de deux étoiles, 1 avec celle d’une étoile, 3 avec celle de trois étoiles.', quantites=[1, 2, 3])

def a_chenille():
    code = ''
    xs = [2.0 + i * 2.25 for i in range(6)]
    ys = [6.0 + (0.7 if i % 2 else 0) for i in range(6)]
    for i, (x, y) in enumerate(zip(xs, ys)):
        code += rf'\draw[mat contour,fill=white] ({f(x)},{f(y)}) circle (1.15);'
        code += rf'\draw[mat contour] ({f(x - 0.3)},{f(y - 1.12)}) -- ({f(x - 0.4)},{f(y - 1.6)}) ({f(x + 0.3)},{f(y - 1.12)}) -- ({f(x + 0.4)},{f(y - 1.6)});'
    hx, hy = 15.6, 7.6
    code += rf'\draw[mat contour,fill=matVert] ({f(hx)},{f(hy)}) circle (1.35);'
    code += rf'\fill[white] ({f(hx - 0.4)},{f(hy + 0.35)}) circle (0.28) ({f(hx + 0.4)},{f(hy + 0.35)}) circle (0.28);'
    code += rf'\fill[matTrait] ({f(hx - 0.35)},{f(hy + 0.35)}) circle (0.13) ({f(hx + 0.45)},{f(hy + 0.35)}) circle (0.13);'
    code += rf'\draw[mat contour] ({f(hx - 0.5)},{f(hy - 0.4)}) .. controls ({f(hx)},{f(hy - 0.8)}) .. ({f(hx + 0.5)},{f(hy - 0.4)});'
    code += rf'\draw[mat contour] ({f(hx - 0.5)},{f(hy + 1.2)}) -- ({f(hx - 0.8)},{f(hy + 2.0)}) ({f(hx + 0.5)},{f(hy + 1.2)}) -- ({f(hx + 0.8)},{f(hy + 2.0)});'
    code += rf'\fill[matRouge] ({f(hx - 0.8)},{f(hy + 2.0)}) circle (0.16) ({f(hx + 0.8)},{f(hy + 2.0)}) circle (0.16);'
    code += P('opti', 2.4, 11.4, 2.4)
    sols = [texte(x, y, str(i + 1), 26, 'otGreenDark', r'\otBold') for i, (x, y) in enumerate(zip(xs, ys))]
    fig = figure(code, sol(*sols), hauteur=13.5)
    return A('La chenille qui compte', 'Touche chaque rond de la chenille en disant : un, deux, trois… jusqu’à six. Puis colorie-la.', ['dire', 'colorier'],
             'Réciter la comptine numérique de un à six, de façon ordonnée, en partant de un.', 'R8', fig,
             'Réciter la comptine en montant un escalier, une marche par mot-nombre, puis en tapant dans les mains.',
             '« Un, deux, trois, quatre, cinq, six. » Un mot pour chaque rond, sans en sauter.',
             'Six ronds : l’enfant dit un mot-nombre par rond, de un à six. La récitation est orale ; on ne fait pas écrire les nombres.',
             controles=[(len(xs) == 6, 'comptine récitée jusqu’à six, limite du programme')])

# ------------------------------------------------------------------ partie 3
def a_valise():
    code = P('boite', 5.2, 9.6, 5.0, c='matOrange') + P('ours', 4.2, 9.2, 1.45, c='matBrun') + P('ours', 6.2, 9.2, 1.45, c='matJaune')
    code += P('ours', 12.6, 11.4, 1.7, c='matRose') + fleche((11.2, 11.0), (8.4, 10.4), 'otMuted', 2.5)
    code += texte(12.6, 9.4, 'encore un', 13, 'otMuted', r'\otMedium')
    for k in range(4):
        code += P('de', 3.0 + k * 3.7, 3.0, 2.3, n=k + 1)
    fig = figure(code, sol(entoure_sol(3.0 + 2 * 3.7, 3.0, 1.55, 1.55)), hauteur=13.3)
    return A('Les ours dans la boîte', 'Il y a deux ours dans la boîte. On en met encore un. Combien y a-t-il d’ours dans la boîte ? Entoure le bon dé.',
             ['entourer'], 'Résoudre un petit problème d’ajout en se représentant l’action.', 'R9', fig,
             'Jouer la scène avec une vraie boîte et des peluches : en mettre deux, en ajouter une, fermer la boîte et demander combien il y en a.',
             '« Il y avait deux ours, j’en mets encore un : il y en a trois. »',
             'Trois ours : le dé à trois points.', quantites=[1, 2, 3])

def a_crayons():
    code = zone(0.4, 4.8, 8.2, 13.6) + zone(8.8, 4.8, 16.6, 13.6)
    code += texte(4.3, 13.0, 'avant', 13, 'otMuted', r'\otMedium') + texte(12.7, 13.0, 'après', 13, 'otMuted', r'\otMedium')
    for k, c in enumerate(['matRouge', 'matJaune', 'matVert', 'matViolet']):
        code += P('crayon', 2.7 + k * 1.05, 6.6, 1.0, c=c, l=4.4, rot=90)
    code += P('boite', 4.3, 7.2, 3.6, c='matBleu')
    code += P('boite', 12.7, 7.2, 3.6, c='matBleu') + rf'\draw[mat contour,fill=matBleu!60] (10.5,8.5) rectangle (14.9,9.0);' + texte(12.7, 7.0, '?', 34, 'otNavy', r'\otBold')
    code += P('crayon', 9.8, 11.4, 1.0, c='matRouge', l=4.4) + P('crayon', 9.8, 10.6, 1.0, c='matJaune', l=4.4)
    for k in range(3):
        code += P('main', 4.0 + k * 4.5, 2.0, 2.4, n=k + 1)
    fig = figure(code, sol(entoure_sol(4.0 + 4.5, 2.0, 1.5, 1.6)), hauteur=14.0)
    return A('La boîte de crayons', 'Il y avait quatre crayons dans la boîte. On en a sorti deux. Combien en reste-t-il dans la boîte ? Entoure la bonne main.',
             ['entourer'], 'Résoudre un petit problème de retrait en se représentant l’action.', 'R9', fig,
             'Mettre quatre crayons dans une boîte opaque, en retirer deux devant l’enfant, fermer et demander combien il en reste ; ouvrir pour vérifier.',
             '« Il y en avait quatre, j’en ai enlevé deux : il en reste deux. »',
             'Il reste deux crayons : la main qui lève deux doigts.', quantites=[4, 2])

def a_envol():
    code = rf'\draw[line width=9pt,matBrun,line cap=round] (1.0,7.0) .. controls (6,7.6) and (10,6.6) .. (13.4,7.2);'
    code += rf'\draw[mat contour,fill=matVert] (13.0,7.2) .. controls (13.8,8.2) and (15.2,7.8) .. (15.4,7.0) .. controls (14.6,6.4) and (13.6,6.6) .. (13.0,7.2) -- cycle;'
    code += P('oiseau', 3.6, 8.1, 1.8, c='matBleu') + P('oiseau', 7.4, 8.15, 1.8, c='matJaune')
    code += P('oiseau', 12.6, 12.0, 1.8, c='matRouge')
    code += rf'\draw[otMuted,line width=1.4pt,dash pattern=on 3pt off 3pt] (9.5,8.6) .. controls (10.4,10.2) .. (11.4,11.5);'
    for k in range(3):
        code += carte_points(4.0 + k * 4.5, 2.6, k + 1, w=2.8, h=2.8)
    fig = figure(code, sol(entoure_sol(8.5, 2.6, 1.85, 1.85)), hauteur=13.2)
    return A('Les oiseaux s’envolent', 'Il y avait trois oiseaux sur la branche. Un oiseau s’est envolé. Combien en reste-t-il sur la branche ? Entoure la bonne carte.',
             ['entourer'], 'Résoudre un petit problème de retrait en percevant la solution.', 'R9', fig,
             'Jouer la scène avec trois peluches sur un banc : l’une s’en va, combien en reste-t-il ?',
             '« Il y avait trois oiseaux. Un est parti. Il en reste deux. »',
             'Il reste deux oiseaux : la carte à deux points.', quantites=[3, 1, 2])

def a_coccinelles():
    code = rf'\draw[mat contour,fill=matVert] (2.0,7.0) .. controls (4.0,11.0) and (10.0,11.0) .. (12.0,7.0) .. controls (10.0,3.6) and (4.0,3.6) .. (2.0,7.0) -- cycle;'
    code += rf'\draw[mat contour,draw=matVertFonce] (2.0,7.0) -- (12.0,7.0);'
    code += P('coccinelle', 5.0, 7.6, 2.2, c='matRouge') + P('coccinelle', 14.4, 11.6, 2.0, c='matRouge')
    code += rf'\draw[otMuted,line width=1.4pt,dash pattern=on 3pt off 3pt] (13.2,10.6) .. controls (11.4,9.8) .. (9.4,8.4);'
    for k in range(3):
        code += P('main', 4.0 + k * 4.5, 1.9, 2.4, n=k + 1)
    fig = figure(code, sol(entoure_sol(8.5, 1.9, 1.5, 1.6)), hauteur=13.0)
    return A('Une coccinelle arrive', 'Une coccinelle est sur la feuille. Une autre arrive. Combien y aura-t-il de coccinelles sur la feuille ? Entoure la bonne main.',
             ['entourer'], 'Résoudre un petit problème d’ajout : un et encore un.', 'R9', fig,
             'Poser un jeton sur une feuille de papier, en ajouter un autre et demander combien il y en a.',
             '« Une coccinelle, et encore une : deux coccinelles. »',
             'Deux coccinelles : la main qui lève deux doigts.', quantites=[1, 2])

# ------------------------------------------------------------------ partie 4
def a_meme_forme():
    rnd = random.Random(41)
    formes_ = ['disque'] * 4 + ['carre'] * 4 + ['triangle'] * 4
    rnd.shuffle(formes_)
    code = zone(6.0, 11.0, 11.0, 15.0, plein=True) + texte(8.5, 14.45, 'le modèle', 11, 'otMuted', r'\otMedium') + forme('disque', 8.5, 12.6, 1.2, couleur='matBleu')
    sols = []
    for i, k in enumerate(formes_):
        r, c = divmod(i, 4)
        x, y = 2.2 + c * 4.2, 8.6 - r * 3.4
        t = [0.75, 1.05, 0.9][i % 3]
        code += forme(k, x, y, t, angle=rnd.choice([0, 15, 30, 45, 60, 100]), couleur=COULEURS[i % len(COULEURS)])
        if k == 'disque':
            sols.append(entoure_sol(x, y, 1.45, 1.45))
    fig = figure(code, sol(*sols), hauteur=15.2)
    return A('Pareil que le modèle', 'Entoure toutes les formes qui ont la <b>même forme</b> que le modèle.', ['entourer'],
             'Reconnaître des objets de même forme, quelles que soient leur couleur et leur taille.', 'R10', fig,
             'Toucher et regarder des formes en bois ; chercher dans la classe des objets qui ont la même forme qu’un disque.',
             '« Celui-là est rond comme le modèle, même s’il est rouge et petit. » L’adulte dit « disque ».',
             'Les quatre disques, quelle que soit leur couleur ou leur taille.', quantites=[4])

def a_trier():
    rnd = random.Random(42)
    pieces = [('disque', 'matRouge', 0.9, 0), ('carre', 'matBleu', 0.85, 20), ('triangle', 'matJaune', 1.0, 15),
              ('carre', 'matVert', 0.6, 45), ('triangle', 'matViolet', 0.75, 200), ('disque', 'matOrange', 0.6, 0)]
    xs = [1.8 + i * 2.7 for i in range(6)]
    code = ''
    boites = ['disque', 'carre', 'triangle']
    xb = [3.2, 8.5, 13.8]
    for x, b in zip(xb, boites):
        code += P('boite', x, 2.5, 3.2, c='matGris') + forme(b, x, 2.5, 0.6, angle=10 if b == 'carre' else 0, couleur='white') + point(x, 4.6)
    sols = []
    for (k, c, t, a), x in zip(pieces, xs):
        y = 11.0 + (0.8 if xs.index(x) % 2 else 0)
        code += forme(k, x, y, t, a, c) + point(x, 9.0)
        sols.append(trait_sol((x, 9.0), (xb[boites.index(k)], 4.6)))
    fig = figure(code, sol(*sols), hauteur=13.2)
    return A('Ranger les formes', 'Relie chaque forme à la boîte qui a la <b>même forme</b>.', ['relier'],
             'Trier et classer des formes planes selon leur forme, malgré la couleur, la taille et l’orientation.', 'R10', fig,
             'Ranger des formes en bois ou en carton dans trois boîtes marquées d’un disque, d’un carré et d’un triangle.',
             '« Ce carré va avec les carrés, même s’il est tourné. »',
             'Les deux disques dans la boîte du disque, les deux carrés dans celle du carré, les deux triangles dans celle du triangle.')

def a_encastrer():
    code = rf'\draw[mat contour,fill=matBrun!35,rounded corners=10pt] (9.0,0.6) rectangle (16.6,13.0);'
    trous = [('etoile', 12.8, 10.6, 0), ('coeur', 11.0, 6.8, 0), ('tri', 14.6, 3.0, 0)]
    pieces = [('coeur', 3.0, 11.0, 35, 'matRouge'), ('tri', 3.0, 6.8, 75, 'matBleu'), ('etoile', 3.0, 2.6, 22, 'matJaune')]
    for nom, x, y, a in trous:
        code += (forme('triangle', x, y, 1.3, 0, 'matTrait!70') if nom == 'tri' else P(nom, x, y, 2.6, c='matTrait!70'))
    pts_t = {'etoile': (12.8, 12.2), 'coeur': (11.0, 8.4), 'tri': (14.6, 4.6)}
    sols = []
    for nom, x, y, a, c in pieces:
        code += (forme('triangle', x, y, 1.3, a, c) if nom == 'tri' else P(nom, x, y, 2.6, c=c, rot=a)) + point(x + 2.3, y)
        sols.append(trait_sol((x + 2.3, y), pts_t[nom]))
    for nom, (x, y) in pts_t.items():
        code += point(x, y)
    fig = figure(code, sol(*sols), hauteur=13.4)
    return A('Chaque pièce dans son trou', 'Relie chaque pièce au trou où elle peut entrer.', ['relier'],
             'Percevoir qu’une forme reste la même quand on la tourne ; encastrer des objets.', 'R10', fig,
             'Jouer avec un vrai jeu d’encastrement : tourner la pièce jusqu’à ce qu’elle entre.',
             '« Si je tourne le cœur, il entre dans le trou du cœur. »',
             'Le cœur va dans le trou en forme de cœur, le triangle dans le trou triangulaire, l’étoile dans le trou en étoile, même si les pièces sont tournées.')

def moitie(nom, x, y, s, cote, decal, c=None):
    """Moitié gauche ou droite d’une illustration, la coupe étant décalée de decal."""
    e = 0.6 * s     # le rectangle de découpe compte dans la taille de la figure : il reste au plus près du dessin
    clip = rf'({f(x - e)},{f(y - e)}) rectangle ({f(x)},{f(y + e)})' if cote == 'g' else rf'({f(x)},{f(y - e)}) rectangle ({f(x + e)},{f(y + e)})'
    dx = -decal if cote == 'g' else decal
    return (rf'\begin{{scope}}[shift={{({f(dx)},0)}}]\begin{{scope}}\clip {clip};' + P(nom, x, y, s, c=c) + r'\end{scope}'
            + rf'\draw[otMuted,line width=1pt,dash pattern=on 2pt off 2pt] ({f(x)},{f(y - 0.55 * s)}) -- ({f(x)},{f(y + 0.55 * s)});\end{{scope}}')

def a_moities():
    objets_ = [('pomme', 'matRouge'), ('poisson', 'matBleu'), ('maison', 'matJaune')]
    perm = melange(3, 7)
    code = ''
    yg = [11.6, 7.4, 3.2]
    sols = []
    for i, (nom, c) in enumerate(objets_):
        code += moitie(nom, 3.6, yg[i], 3.4, 'g', 0.0, c) + point(5.4, yg[i])
    for j in range(3):
        nom, c = objets_[perm.index(j)]
        code += moitie(nom, 13.4, yg[j], 3.4, 'd', 0.0, c) + point(11.6, yg[j])
    for i in range(3):
        sols.append(trait_sol((5.4, yg[i]), (11.6, yg[perm[i]])))
    fig = figure(code, sol(*sols), hauteur=13.8)
    return A('Les deux moitiés', 'Relie chaque moitié d’image à l’autre moitié.', ['relier'],
             'Reconstituer une image coupée en deux (assemblage de deux pièces).', 'R10', fig,
             'Couper en deux des images de catalogue et les faire réassembler.',
             '« Cette moitié de pomme va avec l’autre moitié de pomme. »',
             'La pomme avec la pomme, le poisson avec le poisson, la maison avec la maison.')

def quart(nom, cx, cy, s, q, dx, dy, c=None):
    """Quart d’illustration (q parmi hg, hd, bg, bd) déplacé de (dx, dy)."""
    x0 = cx - 0.6 * s if q[1] == 'g' else cx
    x1 = cx if q[1] == 'g' else cx + 0.6 * s
    y0 = cy if q[0] == 'h' else cy - 0.6 * s
    y1 = cy + 0.6 * s if q[0] == 'h' else cy
    return (rf'\begin{{scope}}[shift={{({f(dx)},{f(dy)})}}]\begin{{scope}}\clip ({f(x0)},{f(y0)}) rectangle ({f(x1)},{f(y1)});'
            + P(nom, cx, cy, s, c=c) + r'\end{scope}'
            + rf'\draw[otRule,line width=1pt] ({f(max(x0, cx - 0.55 * s))},{f(max(y0, cy - 0.55 * s))}) rectangle ({f(min(x1, cx + 0.55 * s))},{f(min(y1, cy + 0.55 * s))});\end{{scope}}')

def a_puzzle4():
    s = 7.0
    cx, cy = 8.5, 10.4
    code = rf'\draw[draw=otRule,line width=1pt,fill=white] ({f(cx - 0.55 * s)},{f(cy - 0.55 * s)}) rectangle ({f(cx + 0.55 * s)},{f(cy + 0.55 * s)});'
    for q in ['hg', 'hd', 'bg']:
        code += quart('ours', cx, cy, s, q, 0, 0, 'matBrun!80')
    code += rf'\draw[pointille] ({f(cx)},{f(cy - 0.55 * s)}) rectangle ({f(cx + 0.55 * s)},{f(cy)});'
    code += sol(quart('ours', cx, cy, s, 'bd', 0, 0, 'matBrun!80'))
    ty = 2.0
    cand = [('ours', 'hg', 'matBrun!80', 2.6), ('ours', 'bd', 'matBrun!80', 8.5), ('lapin', 'bd', 'matGris', 14.4)]
    for nom, q, c, x in cand:
        sc = s
        # La pièce candidate est un quart dessiné à plus petite échelle, centré en (x, ty).
        ox = sc * 0.275 if q[1] == 'g' else -sc * 0.275
        oy = -sc * 0.275 if q[0] == 'h' else sc * 0.275
        code += quart(nom, x + ox, ty + oy, sc, q, 0, 0, c)
    code += sol(entoure_sol(8.5, 2.0, 2.9, 2.9))
    fig = figure(code, hauteur=14.6)
    return A('La pièce qui manque', 'Il manque une pièce au puzzle de l’ours. Entoure la pièce qui manque.', ['entourer'],
             'Compléter un assemblage de quatre pièces à partir d’un modèle.', 'R10', fig,
             'Faire un puzzle de quatre grosses pièces ; en cacher une et la chercher parmi d’autres.',
             '« Il manque le bas à droite : c’est la pièce avec la bouche de l’ours. »',
             'La pièce du milieu : le bas à droite de l’ours. La première est le haut de l’ours, la troisième vient du lapin.')

def a_pavage():
    couleurs = [['matRouge', 'matBleu'], ['matJaune', 'matVert']]
    code = texte(4.0, 13.6, 'le modèle', 12, 'otMuted', r'\otMedium')
    sols = []
    for r in range(2):
        for c in range(2):
            code += rf'\draw[mat contour,fill={couleurs[r][c]}] ({f(1.6 + c * 2.4)},{f(10.6 - r * 2.4)}) rectangle ({f(4.0 + c * 2.4)},{f(13.0 - r * 2.4)});'
            code += rf'\draw[mat contour,fill=white] ({f(8.6 + c * 3.4)},{f(7.2 - r * 3.4)}) rectangle ({f(12.0 + c * 3.4)},{f(10.6 - r * 3.4)});'
            sols.append(rf'\draw[mat contour,fill={couleurs[r][c]}] ({f(8.6 + c * 3.4)},{f(7.2 - r * 3.4)}) rectangle ({f(12.0 + c * 3.4)},{f(10.6 - r * 3.4)});')
    code += P('opti', 3.6, 3.8, 3.0)
    fig = figure(code, sol(*sols), hauteur=14.2)
    return A('Le carrelage', 'Colorie le grand carrelage comme le modèle.', ['colorier'],
             'Reproduire un assemblage de quatre formes à partir d’un modèle (à une autre taille).', 'R10', fig,
             'Reproduire avec quatre carrés de couleur un petit modèle posé sur la table.',
             '« En haut, rouge puis bleu. En bas, jaune puis vert. »',
             'Rouge en haut à gauche, bleu en haut à droite, jaune en bas à gauche, vert en bas à droite.')

# ------------------------------------------------------------------ partie 5
def a_serpents():
    code = P('serpent', 1.0, 9.6, 1.2, c='matVert', c2='matJaune', l=11.5) + P('serpent', 4.0, 4.0, 1.2, c='matOrange', c2='matRouge', l=4.0)
    fig = figure(code, sol(entoure_sol(7.9, 9.6, 7.6, 1.5)), hauteur=13.0)
    return A('Le serpent le plus long', 'Entoure le serpent le plus <b>long</b>.', ['entourer'],
             'Comparer visuellement deux longueurs très différentes.', 'R11', fig,
             'Comparer deux cordes ou deux bandes de papier très différentes, puis deux bâtons.',
             '« Ce serpent est plus long. L’autre est plus court. »',
             'Le serpent vert, en haut.', controles=[(11.5 > 2 * 4.0, 'longueurs très différentes')])

def a_crayons_long():
    longs = [7.0, 12.0, 9.5]
    code = rf'\draw[otRule,line width=1.5pt] (1.4,1.0) -- (1.4,13.0);'
    sols = []
    for i, L in enumerate(longs):
        y = 11.4 - i * 4.4
        code += P('crayon', 1.6, y, 2.2, c='white', l=L / 2.2)
        if L == max(longs):
            sols.append(P('crayon', 1.6, y, 2.2, c='otGreen', l=L / 2.2))
    fig = figure(code, sol(*sols), hauteur=13.6)
    return A('Le crayon le plus long', 'Colorie le crayon le plus <b>long</b>.', ['colorier'],
             'Comparer des longueurs quand les objets partent du même point.', 'R11', fig,
             'Poser trois crayons contre un bord de table pour qu’ils partent du même endroit, et comparer leurs bouts.',
             '« Ils partent tous du même trait. Celui-ci va le plus loin : c’est le plus long. »',
             'Le crayon du milieu.')

def a_rubans():
    gl = [3.0, 6.0, 4.5]
    dl = [6.0, 4.5, 3.0]
    perm = [dl.index(L) for L in gl]
    cg = ['matRouge', 'matBleu', 'matJaune']
    cd = ['matViolet', 'matVert', 'matOrange']
    g = [lambda x, y, L=L, c=c: P('ruban', 0.6, y, 1.0, c=c, l=L) for L, c in zip(gl, cg)]
    d = [lambda x, y, L=L, c=c: P('ruban', 10.6, y, 1.0, c=c, l=L) for L, c in zip(dl, cd)]
    code, h = relier(g, d, perm, pas=4.2, x_g=5.8, x_d=11.4, ecart_point=1.6)
    code += rf'\draw[otRule,line width=1.5pt] (0.6,0.3) -- (0.6,{f(h - 0.3)}) (10.6,0.3) -- (10.6,{f(h - 0.3)});'
    return A('Même longueur', 'Relie chaque ruban de gauche au ruban de droite qui a la <b>même longueur</b>.', ['relier'],
             'Reconnaître un objet de même longueur qu’un objet donné.', 'R11', figure(code, hauteur=h),
             'Chercher, parmi des bandes de papier, celle qui a la même longueur qu’une bande donnée, en les mettant côte à côte.',
             '« Ce ruban est aussi long que celui-là : ils ont la même longueur. »',
             'Le petit rouge avec le petit orange, le grand bleu avec le grand violet, le moyen jaune avec le moyen vert.')

def a_briques():
    longs = [(2.5, 3.0, 10.4), (6.0, 8.6, 6.2), (4.2, 1.8, 2.4)]
    code = ''
    sols = []
    mx, mn = max(L for L, _, _ in longs), min(L for L, _, _ in longs)
    for L, x, y in longs:
        code += P('brique', x, y, 2.6, c='white', l=L / 2.6)
        if L == mx:
            sols.append(P('brique', x, y, 2.6, c='matRouge', l=L / 2.6))
        if L == mn:
            sols.append(P('brique', x, y, 2.6, c='matBleu', l=L / 2.6))
    fig = figure(code, sol(*sols), hauteur=13.4)
    return A('La plus longue, la plus courte', 'Colorie la brique la plus longue en rouge et la plus courte en bleu.', ['colorier'],
             'Comparer des longueurs ; préparer le rangement du plus long au plus court.', 'R11', fig,
             'Construire un escalier avec trois briques de longueurs différentes, de la plus longue à la plus courte.',
             '« Celle-ci est la plus longue. Celle-là est la plus courte. »',
             'La brique du milieu de la page est la plus longue (rouge) ; celle du haut est la plus courte (bleue).')

# ------------------------------------------------------------------ partie 6
def a_collier():
    code = rf'\draw[matTrait,line width=1.4pt] (0.8,9.0) .. controls (4.0,4.5) and (13.0,4.5) .. (16.2,9.0);'
    pts = []
    for i in range(10):
        t = i / 9
        x = (1 - t) ** 3 * 0.8 + 3 * (1 - t) ** 2 * t * 4.0 + 3 * (1 - t) * t ** 2 * 13.0 + t ** 3 * 16.2
        y = (1 - t) ** 3 * 9.0 + 3 * (1 - t) ** 2 * t * 4.5 + 3 * (1 - t) * t ** 2 * 4.5 + t ** 3 * 9.0
        pts.append((x, y))
    motif = ['matRouge', 'matBleu'] * 5
    trous = [3, 6, 8]
    sols = []
    for i, (x, y) in enumerate(pts):
        code += P('perle', x, y, 2.4, c='white' if i in trous else motif[i])
        if i in trous:
            sols.append(P('perle', x, y, 2.4, c=motif[i]))
    code += rf'\draw[matTrait,line width=1.4pt] (0.8,9.0) .. controls (0.2,10.6) and (3.0,12.2) .. (8.5,12.4) .. controls (14.0,12.2) and (16.8,10.6) .. (16.2,9.0);'
    code += rf'\draw[mat contour,fill=matJaune] (8.2,12.4) circle (0.32) (8.8,12.4) circle (0.32);'
    fig = figure(code, sol(*sols), hauteur=13.0, largeur=17.0)
    return A('Le collier', 'Colorie les perles qui manquent : le collier fait rouge, bleu, rouge, bleu…', ['colorier'],
             'Compléter un motif répétitif très simple (alternance de deux couleurs).', 'R12', fig,
             'Enfiler des perles en alternant deux couleurs, puis retirer une perle et demander laquelle il faut remettre.',
             '« Rouge, bleu, rouge, bleu… Ici, il manque une bleue. »',
             'Dans l’ordre : la quatrième perle est bleue, la septième rouge, la neuvième rouge.',
             controles=[(all(motif[i] == ('matRouge' if i % 2 == 0 else 'matBleu') for i in range(10)), 'alternance')])

def a_carres():
    modele = ['matRouge', 'matJaune'] * 3
    code = texte(1.0, 12.6, 'le modèle', 12, 'otMuted', r'\otMedium', 'west')
    sols = []
    for i, c in enumerate(modele):
        code += rf'\draw[mat contour,fill={c}] ({f(1.0 + i * 2.6)},{f(9.6)}) rectangle ({f(3.2 + i * 2.6)},{f(11.8)});'
        code += rf'\draw[mat contour,fill=white] ({f(1.0 + i * 2.6)},{f(3.6)}) rectangle ({f(3.2 + i * 2.6)},{f(5.8)});'
        sols.append(rf'\draw[mat contour,fill={c}] ({f(1.0 + i * 2.6)},{f(3.6)}) rectangle ({f(3.2 + i * 2.6)},{f(5.8)});')
    code += fleche((8.4, 8.8), (8.4, 6.6), 'otGreen', 3)
    fig = figure(code, sol(*sols), hauteur=13.2)
    return A('La même rangée', 'Colorie la rangée du bas comme celle du haut.', ['colorier'],
             'Reproduire à l’identique un motif répétitif.', 'R12', fig,
             'Recopier une rangée de cubes de deux couleurs posée sur la table, cube par cube.',
             '« Rouge, jaune, rouge, jaune… C’est toujours pareil. »',
             'Rouge, jaune, rouge, jaune, rouge, jaune.')

def symbole(k, x, y, t=0.8, c=None):
    if k == 'E':
        return P('etoile', x, y, 2.0 * t, c=c or 'matJaune')
    return forme('disque', x, y, 0.62 * t, couleur=c or 'matBleu')

def a_cache():
    seq = ['E', 'D', 'E', 'D', None, 'D', 'E', 'D']
    code = ''
    xs = [1.1 + i * 2.15 for i in range(8)]
    for x, k in zip(xs, seq):
        if k is None:
            # Carte retournée, plus grande que les formes qu’elle peut cacher.
            code += (rf'\draw[mat contour,fill=otNavy,rounded corners=5pt] ({f(x - 1.0)},9.0) rectangle ({f(x + 1.0)},11.0);'
                     + texte(x, 10.0, '?', 30, 'white', r'\otBold'))
        else:
            code += symbol_ok(k, x)
    code += texte(8.5, 6.0, 'Qu’y a-t-il sous la carte ?', 13, 'otMuted', r'\otMedium')
    code += zone(3.0, 1.0, 7.4, 4.6) + zone(9.6, 1.0, 14.0, 4.6) + symbole('E', 5.2, 2.8, 1.1) + symbole('D', 11.8, 2.8, 1.1)
    fig = figure(code, sol(entoure_sol(5.2, 2.8, 2.6, 2.2)), hauteur=12.0)
    return A('Ce qui est caché', 'Quelle forme est cachée sous la carte bleue ? Entoure-la en bas.', ['entourer'],
             'Compléter un motif répétitif : anticiper l’élément caché.', 'R12', fig,
             'Aligner étoile, disque, étoile, disque avec des cartes ; en retourner une et la faire deviner.',
             '« Étoile, rond, étoile, rond… Sous la carte, il y a une étoile. »',
             'Une étoile : après le rond vient toujours une étoile.', controles=[(seq[3] == 'D' and seq[5] == 'D', 'motif cohérent')])

def symbol_ok(k, x):
    return symbole(k, x, 10.0, 1.0)

def a_train_copie():
    modele = ['matVert', 'matJaune', 'matVert', 'matJaune', 'matVert']
    code = texte(0.6, 13.4, 'le modèle', 12, 'otMuted', r'\otMedium', 'west')
    sols = []
    code += P('locomotive', 1.8, 10.8, 2.3, c='otNavy!70') + P('locomotive', 1.8, 4.2, 2.3, c='otNavy!70')
    for i, c in enumerate(modele):
        code += P('wagon', 4.4 + i * 2.5, 10.7, 2.3, c=c) + P('wagon', 4.4 + i * 2.5, 4.1, 2.3, c='white')
        sols.append(P('wagon', 4.4 + i * 2.5, 4.1, 2.3, c=c))
    fig = figure(code, sol(*sols), hauteur=14.0)
    return A('Le train à copier', 'Colorie le train du bas comme celui du haut.', ['colorier'],
             'Reproduire à l’identique un motif répétitif.', 'R12', fig,
             'Copier un train de cubes de deux couleurs, d’abord en le regardant, puis de mémoire.',
             '« Vert, jaune, vert, jaune, vert. »',
             'Vert, jaune, vert, jaune, vert, derrière la locomotive.')

# ------------------------------------------------------------------ partie 7
def a_bocal():
    # Table basse dessinée ici (plateau large, pieds courts) avec le bocal posé dessus.
    code = (r'\draw[mat contour,draw=matBrun!70!black,line width=2.4pt] (1.8,3.2) -- (1.8,0.2) (15.2,3.2) -- (15.2,0.2);'
            r'\draw[mat contour,fill=matBrun!70] (0.6,3.2) rectangle (16.4,4.0);')
    code += P('bocal', 6.0, 4.0, 3.8, n=0)
    dedans = [(4.6, 4.46), (7.4, 4.46), (6.0, 5.4)]
    dehors = [(11.6, 4.46), (14.2, 4.46)]
    sols = []
    for x, y in dedans + dehors:
        code += P('bonbon', x, y, 2.2, c='white', c2='white')
    for x, y in dedans:
        sols.append(P('bonbon', x, y, 2.2, c='otGreen', c2='otGreen!60'))
    fig = figure(code, sol(*sols), hauteur=12.6)
    return A('Dans le bocal', 'Colorie les bonbons qui sont <b>dans</b> le bocal.', ['colorier'],
             'Comprendre et utiliser les mots « dans » et « dehors ».', 'R13', fig,
             'Jouer à mettre des objets dans une boîte ou dehors, en le disant à voix haute.',
             '« Ce bonbon est dans le bocal. Celui-là est dehors, sur la table. »',
             'Les trois bonbons du bocal. Les deux autres sont dehors, sur la table.')

def a_table():
    code = ''
    for k, (dessus, dessous) in enumerate([('chat', 'ballon'), ('ballon', 'chat')]):
        x = 4.3 + k * 8.4
        code += zone(x - 4.0, 0.4, x + 4.0, 12.4) + rf'\draw[otRule,line width=1.5pt] ({f(x - 3.8)},3.5) -- ({f(x + 3.8)},3.5);' + P('table', x, 7.4, 3.4)
        code += (P('chat', x, 8.5, 2.6, c='matOrange') if dessus == 'chat' else P('ballon', x, 8.5, 2.4, c='matRouge', c2='matJaune'))
        code += (P('chat', x, 4.6, 2.6, c='matOrange') if dessous == 'chat' else P('ballon', x, 4.65, 2.4, c='matRouge', c2='matJaune'))
    fig = figure(code, sol(entoure_sol(12.7, 4.6, 1.8, 1.7)), hauteur=12.8)
    return A('Sur ou sous la table', 'Entoure le chat qui est <b>sous</b> la table.', ['entourer'],
             'Comprendre et utiliser les mots « sur » et « sous ».', 'R13', fig,
             'Poser une peluche sur la table, puis sous la table, et le dire chaque fois.',
             '« Ici, le chat est sur la table. Là, il est sous la table. »',
             'Le chat de droite, sous la table.')

def a_derriere():
    code = ''
    for k in range(2):
        x = 4.3 + k * 8.4
        code += zone(x - 4.0, 0.4, x + 4.0, 13.0)
        code += rf'\draw[otRule,line width=1.5pt] ({f(x - 3.8)},2.1) -- ({f(x + 3.8)},2.1);'
        if k == 0:
            code += P('lapin', x + 0.75, 3.3, 2.6, c='matGris') + P('arbre', x, 6.6, 8.6)
        else:
            code += P('arbre', x, 6.6, 8.6) + P('lapin', x + 1.1, 3.3, 2.6, c='matGris')
    fig = figure(code, sol(entoure_sol(5.05, 3.3, 1.6, 1.7)), hauteur=13.4)
    return A('Devant ou derrière', 'Entoure le lapin qui est <b>derrière</b> l’arbre.', ['entourer'],
             'Comprendre et utiliser les mots « devant » et « derrière ».', 'R13', fig,
             'Se cacher derrière une chaise, puis se mettre devant ; faire dire où l’on est.',
             '« Ce lapin est derrière l’arbre : on ne le voit pas en entier. L’autre est devant. »',
             'Le lapin de gauche, à moitié caché par l’arbre.')

def a_chemin():
    route = [(2.0, 11.6), (8.0, 11.6), (8.0, 8.0), (3.0, 8.0), (3.0, 4.2), (10.0, 4.2), (10.0, 9.6), (14.6, 9.6), (14.6, 3.0)]
    pts = ' -- '.join(f'({f(x)},{f(y)})' for x, y in route)
    code = rf'\draw[matGris!40,line width=34pt,line join=round,line cap=round] {pts};'
    code += rf'\draw[white,line width=1.6pt,dash pattern=on 5pt off 5pt] {pts};'
    code += P('souris', 1.4, 12.6, 2.2) + P('fromage', 14.8, 1.6, 2.4)
    code += P('arbre', 12.4, 12.4, 2.4) + P('fleur', 6.0, 6.0, 1.6, c='matRose') + P('champignon', 12.8, 6.2, 1.8, c='matRouge')
    fig = figure(code, sol(chemin_sol(route)), hauteur=13.6)
    return A('Le chemin de la souris', 'Suis le chemin avec ton doigt, puis trace-le avec un crayon, de la souris jusqu’au fromage.', ['tracer'],
             'Suivre et reproduire un parcours simple.', 'R13', fig,
             'Faire un parcours dans la cour ou dans la salle de jeux, puis le refaire avec une petite voiture sur une feuille.',
             '« Je vais tout droit, je tourne, je descends… »',
             'Le trait suit la route grise sans en sortir, de la souris jusqu’au fromage.')

PARTIES = [
 ('Plus, moins, autant', 'Comparer des quantités sans compter.',
  'Avant quatre ans, l’enfant compare globalement des collections très différentes et utilise les mots « plus que », « moins que ». Il apprend aussi à comparer par correspondance terme à terme, même pour des collections plus grandes que les nombres qu’il connaît.',
  [a_beaucoup, a_oiseaux, a_lapins, a_gateaux, a_ours, a_elephants], 'pomme'),
 ('Un, deux, trois', 'Découvrir les premiers nombres.',
  'Les petits nombres s’apprennent dans l’ordre : deux, puis trois, voire quatre. L’enfant les rencontre avec ses doigts, des constellations de points et des collections variées, avant de découvrir les chiffres. On ne parle pas encore de zéro.',
  [a_un_seul, a_deux, a_trois, a_un_de_plus, a_mains, a_des, a_autant_points, a_deux_mains, a_trains, a_quatre, a_chiffres, a_chenille], 'de'),
 ('Petits problèmes', 'Ajouter, enlever : se représenter l’action.',
  'Les problèmes sont d’abord joués avec du matériel : on ajoute, on enlève, on cache. La fiche vient après, quand la situation est comprise. L’enfant peut s’aider de ses doigts.',
  [a_valise, a_crayons, a_envol, a_coccinelles], 'ours'),
 ('Les formes', 'Reconnaître, trier, encastrer, assembler.',
  'L’enfant reconnaît et trie des objets selon leur forme, comprend qu’une forme ne change pas quand on la tourne et reproduit de petits assemblages (au plus quatre pièces). L’adulte emploie les bons mots — disque, carré, triangle — sans les exiger.',
  [a_meme_forme, a_trier, a_encastrer, a_moities, a_puzzle4, a_pavage], 'formes'),
 ('Long et court', 'Comparer des longueurs.',
  'Avant quatre ans, on compare des longueurs très différentes d’un coup d’œil, puis des longueurs proches en mettant les objets à la même origine.',
  [a_serpents, a_crayons_long, a_rubans, a_briques], 'serpent'),
 ('Les motifs', 'Copier, compléter, deviner ce qui est caché.',
  'L’enfant mémorise et reproduit des motifs répétitifs très simples, souvent une alternance de deux éléments, et complète un motif dont une partie est cachée.',
  [a_collier, a_carres, a_cache, a_train_copie], 'perle'),
 ('Se repérer', 'Dans, dehors, sur, sous, devant, derrière.',
  'Ces mots de l’espace s’apprennent d’abord avec le corps et les objets de la classe. La fiche permet ensuite de les retrouver sur une image et de suivre un parcours.',
  [a_bocal, a_table, a_derriere, a_chemin], 'souris'),
]

RESUME = (r'\begin{itemize}[leftmargin=5mm,itemsep=1.2mm,topsep=0pt]'
          r'\item comparer des collections sans compter, puis en faisant correspondre un à un ;'
          r'\item découvrir un, deux, trois, voire quatre, avec ses doigts, des points, des dés et les premiers chiffres ;'
          r'\item réciter la comptine numérique jusqu’à six ;'
          r'\item résoudre de petits problèmes en ajoutant ou en enlevant des objets ;'
          r'\item reconnaître, trier, encastrer et assembler des formes ;'
          r'\item comparer des longueurs, reproduire des motifs et se repérer dans l’espace.'
          r'\end{itemize}')

PERIMETRE = (r'\textbf{3. Choix faits dans ce cahier}\par '
             r'Les quantités travaillées ne dépassent pas quatre ; les collections comparées globalement sont très différentes '
             r'(au moins du simple au double), comme le demande le programme pour les enfants de moins de quatre ans. '
             r'Le nombre zéro n’est pas introduit. Les doigts sont montrés en commençant par le pouce, mais toute autre façon de '
             r'montrer un nombre avec ses doigts est juste. Les solides ne sont pas dessinés : ils se manipulent en classe. '
             r'Les assemblages de formes comportent au plus quatre pièces. Chaque fiche commence par une activité avec de vrais objets, '
             r'décrite dans le guide de l’adulte.')
