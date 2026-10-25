"""Cahier de Grande Section : programme « à partir de 5 ans »."""
from outils import *
from gabarits import *
from ms import deux_mains, symb, poly, tour, ligne_trace, aire, fusee

NIVEAU = dict(cle='gs', nom='Grande Section', court='GS', age='à partir de 5 ans', accent='matViolet',
              couv=(5, 6), max_quantite=10, max_globale=40)

R = {
 'R1': 'Comprendre qu’une quantité ne dépend ni de la nature des objets ni de leur organisation (jusqu’à dix)',
 'R2': 'Un de plus, un de moins : le nombre suivant, le nombre précédent',
 'R3': 'Parcourir une collection en passant une et une seule fois par chaque élément',
 'R4': 'Dénombrer une collection jusqu’à dix en utilisant des compositions',
 'R5': 'Constituer une collection d’un cardinal donné, y compris par son écriture chiffrée',
 'R6': 'Comparer des quantités et des nombres écrits en chiffres',
 'R7': 'Composer et décomposer les nombres jusqu’à dix ; les doubles',
 'R8': 'Surcompter à partir d’un nombre donné',
 'R9': 'Associer une quantité, le nom d’un nombre et son écriture chiffrée (jusqu’à dix)',
 'R10': 'Écrire en chiffres les nombres de un à dix',
 'R11': 'Comptine numérique : jusqu’à trente, à rebours de dix, de deux en deux, à partir d’un nombre donné',
 'R12': 'Rang : premier, dernier, deuxième, avant-dernier ; changer de point de départ',
 'R13': 'Déterminer l’effet d’un déplacement : avancer, reculer',
 'R14': 'Construire la bande numérique jusqu’à dix',
 'R15': 'Problèmes de parties-tout, d’ajout et de retrait',
 'R16': 'Problèmes d’écart : « de plus », « de moins »',
 'R17': 'Problèmes de position : retrouver la case de départ',
 'R18': 'Problèmes de groupements et de partage (avec un reste)',
 'R19': 'Solides : décrire le cube et la pyramide par leurs faces',
 'R20': 'Formes planes : carré, rectangle, triangle, disque, dans toutes les orientations',
 'R21': 'Reproduire des assemblages de formes (au plus huit)',
 'R22': 'Utiliser la règle pour tracer',
 'R23': 'Longueurs : bande témoin, ranger jusqu’à cinq objets, reproduire une longueur',
 'R24': 'Masses : ordonner trois objets, réaliser l’équilibre',
 'R25': 'Motifs : motifs évolutifs, transcription, structure commune, création',
 'R26': 'Se repérer : gauche et droite, codage de déplacements, quadrillage',
}

def miroir(nom, x, y, s, c=None):
    """Illustration retournée (elle regarde de l’autre côté)."""
    return P(nom, x, y, s, c=c, miroir=True)

def case_ecrire(x, y, w=2.6, h=2.6):
    return rf'\draw[mat contour,fill=white,rounded corners=5pt] ({f(x - w / 2)},{f(y - h / 2)}) rectangle ({f(x + w / 2)},{f(y + h / 2)});'

def ecrit_sol(x, y, n, taille=44):
    return texte(x, y, str(n), taille, 'otGreenDark', r'\otMedium')

def croix_sol(x, y, r=0.8):
    return rf'\draw[sol trait] ({f(x - r)},{f(y - r)}) -- ({f(x + r)},{f(y + r)}) ({f(x - r)},{f(y + r)}) -- ({f(x + r)},{f(y - r)});'

def deux_constellations(x, y, a, b, ecart=1.6, r=0.19, pas=0.42):
    return constellation(x - ecart, y, a, r=r, pas=pas) + constellation(x + ecart, y, b, r=r, pas=pas)

# ------------------------------------------------------------------ partie 1 : les nombres jusqu’à dix
def a_sept_partout():
    contenus = [(coll('etoile', 7, 'ligne', s=0.95, couleurs=['matJaune']), 7),
                (coll('pomme', 6, 'vrac', s=1.2, couleurs=['matRouge', 'matVert'], graine=201), 6),
                (mixte('ballon', [0.8, 1.2, 0.85, 1.25, 0.8, 1.15, 0.9], ['matBleu', 'matRouge', 'matVert', 'matJaune', 'matViolet'], 1.0), 7),
                (coll('jeton', 7, 'grille', s=1.0, couleurs=['matViolet']), 7),
                (coll('poisson', 8, 'vrac', s=1.1, couleurs=['matOrange', 'matBleu'], graine=202), 8),
                (coll('fleur', 7, 'vrac', s=1.15, couleurs=['matRouge', 'matRose', 'matJaune'], graine=203), 7)]
    code, h, bons = boites_rond(contenus, 7)
    return A('Sept partout', 'Colorie le rond sous chaque boîte où il y a <b>sept</b> objets.', ['colorier'],
             'Reconnaître des collections de sept objets de tailles, de natures et de dispositions différentes.', 'R1', figure(code, hauteur=h),
             'Faire des collections de sept objets très différents (sept perles, sept livres) et les comparer en les alignant.',
             '« Les ballons sont petits ou gros, rangés ou en vrac, mais il y en a toujours sept. »',
             'Les boîtes des étoiles, des ballons, des jetons et des fleurs. Il y a six pommes et huit poissons.',
             quantites=[6, 7, 8], controles=[(bons == 4, 'quatre boîtes à sept objets')])

def a_combien_gs():
    gauches = [8, 10, 6, 9]
    droites = [9, 6, 10, 8]
    noms = {8: ('fraise', ['matRouge']), 10: ('etoile', ['matJaune']), 6: ('poisson', ['matBleu']), 9: ('bonbon', ['matRose', 'matVert'])}
    g = [boite_objets(noms[n][0], n, s=0.9, couleurs=noms[n][1], kind='grille', w=6.6, h=3.0) for n in gauches]
    d = [lambda x, y, n=n: chiffre(x, y, n, 60) for n in droites]
    perm = [droites.index(n) for n in gauches]
    code, h = relier(g, d, perm, pas=3.8, x_g=3.5, x_d=14.9, ecart_point=4.1)
    return A('Le bon nombre', 'Compte les objets de chaque boîte. Relie la boîte au <b>nombre</b> qui convient.', ['relier'],
             'Dénombrer une collection jusqu’à dix et l’associer à son écriture chiffrée.', 'R9', figure(code, hauteur=h),
             'Jeu du marchand : l’enfant compte des objets et pose la carte chiffrée qui convient.',
             '« Il y a dix étoiles : cinq et cinq. Je relie au 10. »',
             'Huit fraises avec 8, dix étoiles avec 10, six poissons avec 6, neuf bonbons avec 9.', quantites=[6, 8, 9, 10])

def a_cartes_doubles():
    code = ''
    sols = []
    for r, (a, b) in enumerate([(4, 4), (5, 3), (5, 5), (6, 3)]):
        y = 13.2 - r * 3.9
        code += rf'\draw[draw=matTrait,line width=1.2pt,fill=white,rounded corners=6pt] (0.6,{f(y - 1.4)}) rectangle (8.6,{f(y + 1.4)});'
        code += rf'\draw[otRule,line width=1pt] (4.6,{f(y - 1.2)}) -- (4.6,{f(y + 1.2)});'
        code += deux_constellations(4.6, y, a, b, ecart=2.0, r=0.22, pas=0.5)
        code += fleche((9.4, y), (11.8, y), 'matViolet', 3) + case_ecrire(14.0, y)
        sols.append(ecrit_sol(14.0, y, a + b))
    fig = figure(code, sol(*sols), hauteur=15.0)
    return A('Deux groupes de points', 'Combien de points sur chaque carte ? <b>Écris</b> le nombre dans la case.', ['dessiner'],
             'Dénombrer en utilisant des compositions : « quatre et quatre, huit ».', 'R4', fig,
             'Montrer rapidement deux constellations de dé ; l’enfant dit le total sans compter un à un, puis vérifie.',
             '« Je vois quatre et encore quatre : ça fait huit. Je sais que quatre et quatre font huit. »',
             'Huit, huit, dix et neuf. Pour la dernière carte, on peut garder six dans sa tête et surcompter : sept, huit, neuf.',
             quantites=[4, 5, 6, 8, 9, 10])

def a_parcours_bonbons():
    pts = positions(14, 'vrac', 8.5, 7.0, 15.6, 12.4, d=2.2, graine=204)
    code = ''
    sols = []
    for i, (x, y) in enumerate(pts):
        code += P('bonbon', x, y, 1.8, c=COULEURS[i % 7], c2=COULEURS[(i + 3) % 7])
        sols.append(croix_sol(x, y, 0.5))
    sols.append(texte(8.5, 0.0, 'quatorze bonbons', 14, 'otGreenDark', r'\otSemi'))
    fig = figure(code, sol(*sols), hauteur=13.6)
    return A('Tous les bonbons', 'Compte les bonbons : fais une petite croix sur chacun quand tu le comptes, pour n’en oublier aucun. Dis combien il y en a.',
             ['barrer', 'dire'], 'Parcourir une grande collection en marquant les éléments déjà comptés.', 'R3', fig,
             'Compter des jetons posés en vrac en les poussant d’un côté de la table au fur et à mesure.',
             '« Celui-là, je l’ai déjà compté : il a sa croix. Un, deux, trois… quatorze. »',
             'Quatorze bonbons. Chaque bonbon porte une seule croix ; aucun n’est oublié.',
             controles=[(len(pts) == 14, 'quatorze bonbons')])

def a_dessine_chiffre():
    code = ''
    sols = []
    for r, n in enumerate([7, 9, 6]):
        y = 12.4 - r * 4.6
        code += chiffre(1.5, y, n, 66) + cadre_pointille(3.6, y - 1.8, 16.6, y + 1.8)
        c, _ = collection('jeton', n, 'ligne', 10.1, y, 12.4, 3.0, s=1.1, couleurs=['otGreen'])
        sols.append(c)
    fig = figure(code, sol(*sols), hauteur=14.6)
    return A('Autant que le nombre', 'Lis le nombre. Dessine <b>autant</b> de ronds dans la boîte.', ['dessiner'],
             'Constituer une collection dont la quantité est donnée par son écriture chiffrée.', 'R5', fig,
             'Tirer une carte chiffrée et aller chercher exactement autant d’objets, en un seul voyage.',
             '« C’est un sept : je dessine sept ronds. Cinq et encore deux. »',
             'Sept, neuf et six ronds.', quantites=[6, 7, 9])

def a_plus_grand():
    c, _ = bande(0.5, 13.6, list(range(1, 11)), w=1.6, h=1.6, taille=20)
    code = c
    sols = []
    for r, (a, b) in enumerate([(7, 9), (10, 6), (5, 8), (6, 4)]):
        y = 10.0 - r * 3.0
        code += zone(2.2, y - 1.3, 14.8, y + 1.3) + chiffre(5.6, y, a, 50) + chiffre(11.4, y, b, 50)
        sols.append(entoure_sol(5.6 if a > b else 11.4, y, 1.4, 1.2))
    fig = figure(code, sol(*sols), hauteur=14.6)
    return A('Le plus grand nombre', 'Dans chaque cadre, <b>entoure</b> le nombre le plus grand. Tu peux t’aider de la bande des nombres.', ['entourer'],
             'Comparer des quantités données par leur écriture chiffrée.', 'R6', fig,
             'Jeu de la bataille avec des cartes de un à dix : on dit qui a le plus grand nombre et pourquoi.',
             '« Neuf est plus grand que sept : sur la bande, il est plus loin. »',
             '9, 10, 8 et 6.', quantites=[4, 5, 6, 7, 8, 9, 10])

def a_autant_panier():
    code = zone(5.0, 10.0, 12.0, 14.6, plein=True) + texte(8.5, 14.1, 'le modèle', 11, 'otMuted', r'\otMedium')
    c, _ = collection('pomme', 8, 'grille', 8.5, 11.9, 6.0, 3.0, s=1.1, couleurs=['matRouge'])
    code += c
    sols = []
    for k, (n, graine) in enumerate([(7, 205), (8, 206), (9, 207)]):
        x = 2.9 + k * 5.6
        code += zone(x - 2.6, 1.0, x + 2.6, 8.0)
        cc, _ = collection('pomme', n, 'vrac', x, 4.5, 4.8, 6.6, s=1.25, couleurs=['matRouge', 'matVert'], graine=graine)
        code += cc
        if n == 8:
            sols.append(entoure_sol(x, 4.5, 3.1, 4.0))
    fig = figure(code, sol(*sols), hauteur=14.8)
    return A('Autant que le modèle', 'Entoure la boîte qui a <b>autant</b> de pommes que le modèle.', ['entourer'],
             'Comparer des collections en les dénombrant, quand elles sont organisées différemment.', 'R6', fig,
             'Deux enfants ont des collections rangées différemment : ont-ils autant d’objets ? On compte pour le savoir.',
             '« Le modèle a huit pommes. Cette boîte aussi : huit. Il y en a autant. »',
             'La boîte du milieu (huit pommes). Les autres en ont sept et neuf.', quantites=[7, 8, 9])

# ------------------------------------------------------------------ partie 2 : un de plus, un de moins, composer
def a_un_de_moins():
    code = ''
    sols = []
    for r, (nom, n, c) in enumerate([('etoile', 7, 'matJaune'), ('pomme', 10, 'matRouge'), ('ballon', 9, 'matBleu')]):
        y = 12.4 - r * 4.6
        code += zone(0.3, y - 1.6, 12.6, y + 1.6)
        cc, pts = collection(nom, n, 'ligne', 6.45, y, 11.8, 2.8, s=1.05, couleurs=[c])
        code += cc + case_ecrire(14.6, y)
        sols += [croix_sol(*pts[-1], 0.55), ecrit_sol(14.6, y, n - 1)]
    fig = figure(code, sol(*sols), hauteur=14.4)
    return A('Un de moins', 'Barre <b>un</b> objet dans chaque rangée. Combien en reste-t-il ? Écris le nombre.', ['barrer', 'dessiner'],
             'Réaliser une collection qui a un objet de moins et nommer le nombre avant et après le retrait.', 'R2', fig,
             'Faire une tour de sept cubes, en retirer un : « sept, j’en enlève un, six ».',
             '« Il y avait sept étoiles, j’en enlève une : il en reste six. Six vient juste avant sept. »',
             '6, 9 et 8 : quand on enlève un, on obtient le nombre qui vient juste avant.', quantites=[6, 7, 8, 9, 10])

def a_avant_apres():
    code = ''
    sols = []
    for r, n in enumerate([6, 9, 3, 2]):
        y = 13.2 - r * 3.8
        code += case_ecrire(4.0, y) + case_ecrire(8.5, y, 2.8, 2.8) + case_ecrire(13.0, y)
        code += rf'\fill[matViolet!15,rounded corners=5pt] (7.1,{f(y - 1.4)}) rectangle (9.9,{f(y + 1.4)});' + chiffre(8.5, y, n, 50)
        sols += [ecrit_sol(4.0, y, n - 1), ecrit_sol(13.0, y, n + 1)]
    code += texte(4.0, 15.4, 'juste avant', 12, 'otMuted', r'\otMedium') + texte(13.0, 15.4, 'juste après', 12, 'otMuted', r'\otMedium')
    fig = figure(code, sol(*sols), hauteur=15.8)
    return A('Juste avant, juste après', 'Écris le nombre qui vient <b>juste avant</b> et celui qui vient <b>juste après</b>.', ['dessiner'],
             'Comprendre que chaque nombre s’obtient en ajoutant un au précédent.', 'R2', fig,
             'Réciter la comptine et s’arrêter : « Quel nombre vient juste après six ? Juste avant ? »',
             '« Avant six, il y a cinq. Après six, il y a sept : six et un, sept. »',
             '5 et 7 ; 8 et 10 ; 2 et 4 ; 1 et 3.', quantites=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

def a_surcompter():
    code = ''
    sols = []
    for r, (a, b) in enumerate([(5, 3), (6, 3), (4, 2)]):
        y = 12.4 - r * 4.6
        code += P('de', 1.7, y, 2.6, n=a) + texte(4.6, y, 'et encore', 13, 'otMuted', r'\otMedium')
        code += ''.join(P('jeton', 6.9 + k * 1.3, y, 1.4, c='matRouge') for k in range(b))
        code += fleche((10.9, y), (12.6, y), 'matViolet', 3) + case_ecrire(14.8, y)
        sols.append(ecrit_sol(14.8, y, a + b))
    fig = figure(code, sol(*sols), hauteur=14.4)
    return A('Je garde dans ma tête', 'Garde le nombre du dé dans ta tête, puis compte les jetons en continuant. <b>Écris</b> combien il y a en tout.',
             ['dessiner', 'dire'], 'Surcompter à partir d’un nombre donné.', 'R8', fig,
             'Cacher cinq jetons sous un gobelet, en ajouter trois à côté : « Cinq sont cachés. Combien en tout ? »',
             '« Je mets cinq dans ma tête : six, sept, huit. Il y en a huit. »',
             '8, 9 et 6. On part du nombre du dé et on continue la comptine, un mot par jeton.', quantites=[2, 3, 4, 5, 6, 8, 9])

def papillon_points(x, y, n):
    code = rf'\draw[mat contour,fill=matJaune!45] ({f(x - 1.25)},{f(y)}) circle (1.15) ({f(x + 1.25)},{f(y)}) circle (1.15);'
    code += rf'\draw[mat contour,fill=matBrun] ({f(x)},{f(y)}) ellipse (0.22 and 1.25);'
    code += rf'\draw[mat contour] ({f(x - 0.1)},{f(y + 1.2)}) -- ({f(x - 0.45)},{f(y + 1.8)}) ({f(x + 0.1)},{f(y + 1.2)}) -- ({f(x + 0.45)},{f(y + 1.8)});'
    code += constellation(x - 1.25, y, n, r=0.16, pas=0.36) + constellation(x + 1.25, y, n, r=0.16, pas=0.36)
    return code

def a_doubles():
    code = ''
    sols = []
    for i, n in enumerate([2, 3, 4, 5]):
        r, c = divmod(i, 2)
        x, y = 4.25 + c * 8.5, 11.6 - r * 6.6
        code += papillon_points(x, y, n) + case_ecrire(x, y - 2.8, 2.4, 2.0)
        sols.append(ecrit_sol(x, y - 2.8, 2 * n, 36))
    fig = figure(code, sol(*sols), hauteur=14.4)
    return A('Les doubles des papillons', 'Les deux ailes ont autant de points. Combien de points en tout ? <b>Écris</b> le nombre.', ['dessiner', 'dire'],
             'Connaître les doubles : deux et deux, trois et trois, quatre et quatre, cinq et cinq.', 'R7', fig,
             'Plier une feuille peinte pour faire des papillons symétriques ; compter les taches d’une aile, puis des deux.',
             '« Trois et trois font six. Deux fois trois, six. Cinq et cinq font dix. »',
             '4, 6, 8 et 10.', quantites=[2, 3, 4, 5, 6, 8, 10])

def a_deux_mains_gs():
    code = ''
    sols = []
    for r, (a, b) in enumerate([(5, 3), (4, 2), (5, 5), (5, 4)]):
        y = 13.3 - r * 3.9
        code += zone(0.3, y - 1.75, 9.0, y + 1.75) + P('main', 2.5, y, 2.7, n=a) + P('main', 6.8, y, 2.7, n=b)
        code += fleche((9.8, y), (11.8, y), 'matViolet', 3) + case_ecrire(14.0, y)
        sols.append(ecrit_sol(14.0, y, a + b))
    fig = figure(code, sol(*sols), hauteur=15.2)
    return A('Les doigts des deux mains', 'Combien de doigts sont levés en tout ? <b>Écris</b> le nombre.', ['dessiner'],
             'Composer les nombres jusqu’à dix avec les doigts des deux mains.', 'R7', fig,
             'Montrer huit avec ses doigts de plusieurs façons : cinq et trois, quatre et quatre…',
             '« Une main pleine, c’est cinq ; et encore trois : six, sept, huit. »',
             '8, 6, 10 et 9.', quantites=[2, 3, 4, 5, 6, 8, 9, 10])

def a_maison_8():
    code = poly([(3.0, 10.6), (14.0, 10.6), (8.5, 14.4)], 'matRouge!55') + texte(8.5, 11.9, '8', 40, 'white', r'\otBold')
    sols = []
    for r, n in enumerate([5, 3, 6, 4]):
        y = 9.2 - r * 2.5
        code += rf'\draw[mat contour,fill=matJaune!30] (3.6,{f(y - 1.25)}) rectangle (13.4,{f(y + 1.25)});'
        code += case_ecrire(6.0, y, 4.0, 2.0) + case_ecrire(11.0, y, 4.0, 2.0)
        code += constellation(6.0, y, n, r=0.15, pas=0.32)
        reste = 8 - n
        sols.append(constellation(11.0, y, reste, r=0.15, pas=0.32, couleur='otGreen') if reste <= 6 else '')
    fig = figure(code, sol(*sols), hauteur=14.6)
    return A('La maison du huit', 'Dans la maison du huit, chaque étage a huit points en tout. <b>Dessine</b> les points qui manquent dans la fenêtre de droite.',
             ['dessiner'], 'Décomposer huit de plusieurs façons.', 'R7', fig,
             'Cacher une partie de huit jetons sous sa main : combien sont cachés ?',
             '« Huit, c’est cinq et trois. Huit, c’est six et deux. »',
             'Trois, cinq, deux et quatre points.', quantites=[2, 3, 4, 5, 6, 8],
             controles=[(all(0 < 8 - n <= 6 for n in [5, 3, 6, 4]), 'compléments de un à six')])

def domino(x, y, a, b, w=5.4, h=2.5):
    return (rf'\draw[draw=matTrait,line width=1.3pt,fill=white,rounded corners=6pt] ({f(x - w / 2)},{f(y - h / 2)}) rectangle ({f(x + w / 2)},{f(y + h / 2)});'
            + rf'\draw[matTrait,line width=1.1pt] ({f(x)},{f(y - h / 2 + 0.2)}) -- ({f(x)},{f(y + h / 2 - 0.2)});'
            + deux_constellations(x, y, a, b, ecart=w / 4, r=0.18, pas=0.38))

def a_dominos():
    code = ''
    sols = []
    doms = [(4, 3), (5, 1), (6, 1), (3, 3), (5, 2), (4, 4)]
    for i, (a, b) in enumerate(doms):
        r, c = divmod(i, 2)
        x, y = 4.25 + c * 8.5, 12.0 - r * 4.4
        code += domino(x, y, a, b)
        if a + b == 7:
            sols.append(rf'\draw[sol entoure,rounded corners=10pt] ({f(x - 3.1)},{f(y - 1.65)}) rectangle ({f(x + 3.1)},{f(y + 1.65)});')
    fig = figure(code, sol(*sols), hauteur=14.0)
    return A('Les dominos du sept', 'Entoure les dominos qui ont <b>sept</b> points en tout.', ['entourer'],
             'Reconnaître différentes décompositions de sept.', 'R7', fig,
             'Trier un jeu de dominos : chercher tous ceux qui font sept.',
             '« Quatre et trois, sept. Six et un, sept aussi. Cinq et un, ça fait six. »',
             'Les dominos quatre-trois, six-un et cinq-deux.', quantites=[1, 2, 3, 4, 5, 6, 7, 8],
             controles=[(sum(a + b == 7 for a, b in doms) == 3, 'trois dominos de sept')])

# ------------------------------------------------------------------ partie 3 : écrire et réciter
def a_ecrire_789():
    code = ''
    sols = []
    for r, n in enumerate([7, 8, 9]):
        y = 12.6 - r * 4.6
        code += ligne_trace(y, n)
        sols.append(texte(15.6, y, str(n), 54, 'otGreenDark', r'\otMedium'))
    fig = figure(code, sol(*sols), hauteur=14.4)
    return A('J’écris 7, 8, 9', 'Repasse sur les chiffres gris avec ton doigt, puis avec un crayon. Écris le chiffre <b>tout seul</b> dans la dernière case.',
             ['tracer'], 'Écrire en chiffres les nombres de un à dix.', 'R10', fig,
             'Tracer le chiffre en grand dans l’air, puis sur une ardoise, en partant toujours du haut.',
             '« Le huit : je pars en haut, je fais un S, et je remonte. »',
             'Les chiffres sont tracés en partant du haut. Le sept peut s’écrire avec ou sans barre.', quantites=[7, 8, 9])

def a_ecrire_10():
    code = chiffre_trace(1.9, 13.2, 10, 70, modele=True) + rf'\draw[otRule,line width=1pt] (4.0,11.7) -- (16.6,11.7);'
    code += ''.join(chiffre_trace(5.6 + k * 3.4, 13.2, 10, 70) for k in range(3)) + cadre_pointille(14.0, 11.8, 16.6, 14.6)
    sols = [texte(15.3, 13.2, '10', 44, 'otGreenDark', r'\otMedium')]
    for r, (nom, n, c) in enumerate([('etoile', 10, 'matOrange'), ('poisson', 7, 'matBleu'), ('fleur', 8, 'matRose')]):
        y = 8.6 - r * 3.6
        code += zone(0.3, y - 1.5, 12.6, y + 1.5)
        cc, _ = collection(nom, n, 'ligne', 6.45, y, 11.8, 2.6, s=1.05, couleurs=[c])
        code += cc + case_ecrire(14.6, y)
        sols.append(ecrit_sol(14.6, y, n))
    fig = figure(code, sol(*sols), hauteur=15.0)
    return A('J’écris jusqu’à 10', 'Repasse sur les nombres gris. Puis compte et <b>écris</b> le nombre d’objets dans chaque case.', ['tracer', 'dessiner'],
             'Écrire en chiffres les nombres de un à dix pour dire une quantité.', 'R10', fig,
             'Écrire le nombre d’élèves présents, de jours de la semaine, dans des situations réelles de la classe.',
             '« Dix, ça s’écrit avec un 1 et un rond à côté. »',
             'Dix, sept et huit.', quantites=[7, 8, 10])

def a_points20():
    # Contour d’un poisson : dos (angles 0 à 144 °), queue, ventre (216 à 342 °), centre (7.6, 7.2).
    cx, cy, rx, ry = 8.4, 7.2, 5.6, 3.6
    pts = [(cx + rx * cos(radians(a)), cy + ry * sin(radians(a))) for a in range(0, 145, 18)]
    pts += [(1.0, 10.6), (2.2, 7.2), (1.0, 3.8)]
    pts += [(cx + rx * cos(radians(a)), cy + ry * sin(radians(a))) for a in range(216, 343, 18)]
    code = ''
    for i, (x, y) in enumerate(pts):
        if i in (9, 10, 11):
            dx, dy = (-0.55, 0.3) if i != 10 else (0.6, 0.0)
        else:
            nx, ny = x - cx, y - cy
            n = hypot(nx, ny)
            dx, dy = 0.62 * nx / n, 0.62 * ny / n
        code += point(x, y) + texte(x + dx, y + dy, str(i + 1), 12, 'otNavy', r'\otSemi')
    code += rf'\draw[mat contour,fill=white] (11.9,8.3) circle (0.5);\fill[matTrait] (12.05,8.3) circle (0.2);'
    fig = figure(code, sol(chemin_sol(pts + [pts[0]])), hauteur=12.8)
    return A('Relie de 1 à 20', 'Dis la comptine et relie les points dans l’ordre, de 1 à 20. Termine en reliant 20 à 1. Qu’apparaît-il ?', ['relier', 'dire'],
             'Connaître la comptine numérique au-delà de dix et suivre la suite des nombres.', 'R11', fig,
             'Réciter la comptine jusqu’à trente en se déplaçant sur une piste numérotée dans la cour.',
             '« …dix-huit, dix-neuf, vingt. C’est un poisson ! »',
             'Un poisson. L’adulte aide à lire les nombres au-delà de dix si besoin : la comptine orale est l’objectif.',
             controles=[(len(pts) == 20, 'vingt points')])

def a_rebours():
    nombres = list(range(10, 0, -1))
    vides = (8, 6, 3, 1)
    c, centres = bande(0.3, 3.0, nombres, w=1.64, h=2.2, taille=28, vides=vides)
    code = c
    sols = [texte(centres[nombres.index(v)][0], 3.0, str(v), 28, 'otGreenDark', r'\otBold') for v in vides]
    code += fusee(13.6, 5.6, 1.9, ['matRouge', 'matBleu', 'white', 'matJaune', 'matJaune'])
    code += texte(5.0, 9.4, 'Dix, neuf, huit…', 20, 'matViolet', r'\otSemi') + texte(5.0, 7.8, '… décollage !', 20, 'matViolet', r'\otSemi')
    fig = figure(code, sol(*sols), hauteur=11.6)
    return A('Le compte à rebours', 'La fusée va décoller ! Dis les nombres de dix à un et <b>écris</b> ceux qui manquent.', ['dessiner', 'dire'],
             'Réciter la comptine numérique à rebours de dix à un.', 'R11', fig,
             'Faire décoller une fusée en carton : toute la classe compte à rebours, de dix jusqu’à un.',
             '« Dix, neuf, huit, sept, six, cinq, quatre, trois, deux, un… décollage ! »',
             'Il manque 8, 6, 3 et 1.', quantites=[1, 3, 6, 8])

def a_deux_en_deux():
    code = ''
    sols = []
    k = 0
    for r in range(2):
        y = 11.0 - r * 6.0
        code += rf'\draw[matBrun,line width=1.5pt] (0.4,{f(y + 1.6)}) .. controls (8.5,{f(y + 1.0)}) .. (16.6,{f(y + 1.6)});'
        for i in range(5):
            x = 1.9 + i * 3.3
            couleur = COULEURS[(r * 5 + i) % 7]
            code += P('chaussette', x - 0.55, y, 1.9, c=couleur) + P('chaussette', x + 0.55, y, 1.9, c=couleur)
            code += rf'\fill[matBrun] ({f(x - 0.55)},{f(y + 1.25)}) rectangle ({f(x - 0.45)},{f(y + 1.55)}) ({f(x + 0.45)},{f(y + 1.25)}) rectangle ({f(x + 0.55)},{f(y + 1.55)});'
            k += 1
            sols.append(texte(x, y - 1.6, str(2 * k), 13, 'otGreenDark', r'\otBold'))
            if 2 * k == 10:
                sols.append(entoure_sol(x, y, 1.6, 1.45))
    fig = figure(code, sol(*sols), hauteur=13.6)
    return A('De deux en deux', 'Les chaussettes vont par deux. Compte de deux en deux en touchant chaque paire : deux, quatre, six… <b>Entoure</b> la paire où tu dis « dix ».',
             ['entourer', 'dire'], 'Réciter la comptine de deux en deux, en partant de deux.', 'R11', fig,
             'Compter les élèves rangés par deux, les chaussures, les mains : « deux, quatre, six… ».',
             '« Deux, quatre, six, huit, dix ! » Puis jusqu’à vingt.',
             'La cinquième paire (dans la première rangée, la dernière). Il y a vingt chaussettes en tout.', quantites=[10])

def a_depart():
    code = P('locomotive', 1.5, 8.1, 3.0, c='otNavy!70')
    sols = []
    xs = [4.9 + i * 2.45 for i in range(6)]
    for i, x in enumerate(xs):
        code += P('wagon', x, 7.9, 2.4, c='white')
        if i == 0:
            code += texte(x, 8.1, '12', 22, 'otNavy', r'\otBold')
        else:
            sols.append(texte(x, 8.1, str(12 + i), 20, 'otGreenDark', r'\otBold'))
        if 12 + i == 16:
            sols.append(P('wagon', x, 7.9, 2.4, c='otGreen') + texte(x, 8.1, '16', 20, 'white', r'\otBold'))
    fig = figure(code, sol(*sols), hauteur=10.0)
    return A('Le train part de douze', 'Le premier wagon porte le nombre douze. Continue la comptine en touchant chaque wagon. Colorie le wagon où tu dis « <b>seize</b> ».',
             ['colorier', 'dire'], 'Réciter la comptine en partant d’un nombre autre que un.', 'R11', fig,
             'Jeu du furet : un enfant dit un nombre, le suivant continue la comptine à partir de là.',
             '« Douze, treize, quatorze, quinze, seize. »',
             'Le cinquième wagon : douze, treize, quatorze, quinze, seize.')

# ------------------------------------------------------------------ partie 4 : rangs et bande numérique
def a_rang_dix():
    code = rf'\fill[matBleu] (0.7,6.0) circle (0.55);' + rf'\fill[matRouge] (16.3,6.0) circle (0.55);'
    xs = [2.1 + i * 1.42 for i in range(10)]
    for x in xs:
        code += rf'\draw[mat contour,fill=matViolet!12,rounded corners=4pt] ({f(x - 0.6)},5.0) rectangle ({f(x + 0.6)},7.0);'
    code += texte(0.7, 4.4, 'départ bleu', 10, 'otMuted', r'\otMedium') + texte(16.3, 4.4, 'départ rouge', 10, 'otMuted', r'\otMedium')
    sols = [rf'\fill[otGreen,opacity=.6,rounded corners=4pt] ({f(xs[6] - 0.6)},5.0) rectangle ({f(xs[6] + 0.6)},7.0);',
            entoure_sol(xs[7], 6.0, 0.95, 1.4)]
    fig = figure(code, sol(*sols), hauteur=8.0)
    return A('Dix cartes', 'En partant du disque <b>bleu</b>, colorie la septième carte. En partant du disque <b>rouge</b>, entoure la troisième carte.',
             ['colorier', 'entourer'], 'Déterminer un rang dans une suite de dix objets quand on change le point de départ.', 'R12', fig,
             'Aligner dix cartes entre un disque bleu et un disque rouge ; cacher un dessin sous une carte et faire décrire sa place.',
             '« Je pars du bleu : un, deux… sept. Je pars du rouge : un, deux, trois. »',
             'La septième carte en partant du bleu est coloriée ; la troisième en partant du rouge (la huitième en partant du bleu) est entourée.')

def a_canards_rang():
    code = rf'\draw[mat contour,fill=matCiel] (15.6,5.6) ellipse (1.3 and 0.8);' + texte(15.6, 4.2, 'la mare', 10, 'otMuted', r'\otMedium')
    xs = [1.0 + i * 1.6 for i in range(9)]
    for x in xs:
        code += P('canard', x, 5.8, 1.5, c='white')
    couleurs = {8: 'matRouge', 7: 'matJaune', 1: 'otGreen', 0: 'matBleu'}
    sols = [P('canard', xs[i], 5.8, 1.5, c=c) for i, c in couleurs.items()]
    for x, c, t in [(1.4, 'matRouge', 'premier'), (5.0, 'matJaune', 'deuxième'), (8.8, 'otGreen', 'avant-dernier'), (13.4, 'matBleu', 'dernier')]:
        code += rf'\fill[{c}] ({f(x)},1.6) circle (0.32);' + texte(x + 0.5, 1.6, t, 12, 'otMuted', r'\otMedium', 'west')
    fig = figure(code, sol(*sols), hauteur=7.4)
    return A('Les canards vont à la mare', 'Les canards marchent vers la mare. Colorie le <b>premier</b> en rouge, le <b>deuxième</b> en jaune, l’<b>avant-dernier</b> en vert et le <b>dernier</b> en bleu.',
             ['colorier'], 'Repérer le premier, le deuxième, l’avant-dernier et le dernier d’une file.', 'R12', fig,
             'Faire une file : qui est le premier, le dernier ? Et si la file se retourne ?',
             '« Le premier est le plus près de la mare. Le dernier est tout au bout. »',
             'Le canard le plus proche de la mare en rouge, le suivant en jaune ; le dernier (le plus loin) en bleu et celui juste devant lui en vert.')

def train_symboles(y, symboles, s=1.6):
    code = P('locomotive', 1.0, y + 0.1, s * 1.15, c='otNavy!70')
    xs = [2.9 + i * 1.72 for i in range(8)]
    for i, x in enumerate(xs):
        code += P('wagon', x, y, s, c='white')
        if i + 1 in symboles:
            code += symb(symboles[i + 1], x, y + 0.13, 0.55)
    return code, xs

def a_meme_place():
    modele = {2: 'E', 5: 'D', 7: 'T'}
    c1, xs = train_symboles(10.6, modele)
    c2, _ = train_symboles(4.0, {})
    code = texte(0.4, 12.6, 'le modèle', 11, 'otMuted', r'\otMedium', 'west') + c1 + c2
    sols = [symb(k, xs[i - 1], 4.13, 0.55) for i, k in modele.items()]
    fig = figure(code, sol(*sols), hauteur=13.2)
    return A('À la même place', 'Dessine dans le train du bas l’étoile, le rond et le triangle, <b>dans les mêmes wagons</b> que sur le modèle.', ['dessiner'],
             'Repérer la position d’un objet dans une suite ordonnée pour la reproduire.', 'R12', fig,
             'Un enfant regarde un train modèle et dicte à un camarade où placer chaque symbole.',
             '« L’étoile est dans le deuxième wagon après la locomotive. Le rond dans le cinquième. »',
             'L’étoile dans le deuxième wagon, le rond dans le cinquième, le triangle dans le septième.')

def a_bande10():
    code = ''
    sols = []
    for r, vides in enumerate([(3, 6, 9), (2, 5, 7, 10), (1, 4, 8)]):
        y = 12.4 - r * 4.4
        c, centres = bande(0.4, y, list(range(1, 11)), w=1.62, h=2.0, taille=26, vides=vides)
        code += c
        sols += [texte(centres[v - 1][0], y, str(v), 26, 'otGreenDark', r'\otBold') for v in vides]
    fig = figure(code, sol(*sols), hauteur=14.0)
    return A('La bande jusqu’à dix', 'Écris les nombres qui <b>manquent</b> dans chaque bande.', ['dessiner'],
             'Compléter une bande numérique lacunaire jusqu’à dix.', 'R14', fig,
             'Fabriquer la bande numérique de la classe : une case par nombre, avec la quantité et le chiffre.',
             '« Après deux, il y a trois. Avant sept, il y a six. »',
             '3, 6, 9 ; 2, 5, 7, 10 ; 1, 4, 8.', quantites=list(range(1, 11)))

def a_bande_rep():
    c, centres = bande(0.4, 12.6, list(range(1, 11)), w=1.62, h=1.8, taille=24)
    code = c
    sols = []
    cartes = []
    def carte_tour(x, y):
        return ''.join(rf'\draw[mat contour,fill=matViolet!60] ({f(x - 0.3)},{f(y - 1.7 + k * 0.48)}) rectangle ({f(x + 0.3)},{f(y - 1.7 + (k + 1) * 0.48)});' for k in range(7))
    cartes = [(6, lambda x, y: P('de', x, y, 2.2, n=6)), (8, lambda x, y: P('main', x - 0.75, y, 1.8, n=5) + P('main', x + 0.75, y, 1.8, n=3)),
              (7, carte_tour), (10, lambda x, y: carte_points(x - 0.95, y, 5, 1.8, 1.8) + carte_points(x + 0.95, y, 5, 1.8, 1.8)),
              (4, lambda x, y: P('de', x, y, 2.2, n=4))]
    xs = [1.8, 5.2, 8.4, 11.6, 15.2]
    for (n, dessin), x in zip(cartes, xs):
        code += dessin(x, 4.0) + point(x, 6.2)
        sols.append(trait_sol((x, 6.2), (centres[n - 1][0], 11.4)))
    for cx, cy in centres:
        code += point(cx, 11.4)
    fig = figure(code, sol(*sols), hauteur=13.6)
    return A('Sur la bande', 'Relie chaque carte à la case de la bande qui a le <b>même nombre</b>.', ['relier'],
             'Placer différentes représentations des nombres jusqu’à dix sur la bande numérique.', 'R14', fig,
             'Accrocher sous la bande de la classe des cartes : dés, doigts, tours de cubes, collections.',
             '« La tour a sept cubes : je vais au 7. »',
             'Le dé six au 6, les huit doigts au 8, la tour de sept cubes au 7, les dix points au 10, le dé quatre au 4.',
             quantites=[4, 6, 7, 8, 10])

def ligne_bande_pion(y, depart, deplacement, colorie_depart=False):
    c, centres = bande(1.6, y, list(range(1, 11)), w=1.5, h=1.7, taille=20)
    code = c
    arrivee = depart + deplacement
    pion = arrivee if colorie_depart else depart
    x, yy = centres[pion - 1]
    code += P('pion', x, yy + 1.45, 1.35, c='matRouge')
    n = abs(deplacement)
    code += P('de', 0.55, y, 1.4, n=n) if n <= 6 else ''
    couleur = 'otGreen' if deplacement > 0 else 'matRouge'
    if deplacement > 0:
        code += rf'\draw[{couleur},line width=2.4pt,-{{Stealth[length=3mm]}}] (0.0,{f(y + 1.15)}) -- (1.2,{f(y + 1.15)});'
    else:
        code += rf'\draw[{couleur},line width=2.4pt,-{{Stealth[length=3mm]}}] (1.2,{f(y + 1.15)}) -- (0.0,{f(y + 1.15)});'
    cible = depart if colorie_depart else arrivee
    cx, _ = centres[cible - 1]
    sol_ = rf'\fill[otGreen,opacity=.45] ({f(cx - 0.7)},{f(y - 0.82)}) rectangle ({f(cx + 0.7)},{f(y + 0.82)});'
    return code, sol_

def a_oie_gs():
    code = ''
    sols = []
    for r, (dep, dpl) in enumerate([(4, 3), (8, -2), (2, 6)]):
        y = 11.4 - r * 4.4
        c, s_ = ligne_bande_pion(y, dep, dpl)
        code += c
        sols.append(s_)
    fig = figure(code, sol(*sols), hauteur=13.6)
    return A('Avancer, reculer', 'Le pion avance (flèche verte) ou recule (flèche rouge) d’autant de cases que le dé. Colorie la case où il <b>arrive</b>.', ['colorier'],
             'Déterminer la position d’arrivée après un déplacement sur la bande numérique.', 'R13', fig,
             'Jeu de piste sur une grande bande au sol : avancer ou reculer en comptant les cases.',
             '« Je suis sur le quatre, j’avance de trois : cinq, six, sept. J’arrive sur le sept. »',
             'Le 7, le 6 et le 8. Avancer de trois revient à ajouter trois.', quantites=[2, 3, 4, 6, 7, 8])

# ------------------------------------------------------------------ partie 5 : problèmes
def a_trois_parties():
    code = P('boite', 8.5, 3.6, 5.6, c='matViolet')
    groupes = [(['matRouge'] * 3, 3.0), (['matBleu'], 8.5), (['matVert'] * 2, 14.0)]
    for couleurs, x in groupes:
        n = len(couleurs)
        for k, c in enumerate(couleurs):
            code += P('cube', x + (k - (n - 1) / 2) * 1.2, 11.6, 1.2, c=c)
        code += fleche((x, 10.4), (8.5 + (x - 8.5) * 0.25, 6.6), 'otMuted', 2.2)
    code += case_ecrire(15.0, 3.4)
    fig = figure(code, sol(ecrit_sol(15.0, 3.4, 6)), hauteur=12.6)
    return A('Les cubes dans la boîte', 'On met dans la boîte trois cubes rouges, un cube bleu et deux cubes verts. Combien y a-t-il de cubes dans la boîte ? <b>Écris</b> le nombre.',
             ['dessiner'], 'Déterminer le tout dans un problème à trois parties.', 'R15', fig,
             'Mettre successivement des cubes dans une boîte opaque devant l’enfant, puis demander combien elle en contient.',
             '« Trois, et un, quatre ; et deux, cinq, six. Il y a six cubes. »',
             'Six cubes.', quantites=[1, 2, 3, 6])

def a_oiseaux7():
    code = rf'\draw[line width=9pt,matBrun,line cap=round] (0.6,6.0) .. controls (6,6.6) and (11,5.6) .. (16.4,6.2);'
    xs = [1.6 + i * 2.2 for i in range(7)]
    sols = []
    for i, x in enumerate(xs):
        code += P('oiseau', x, 7.05, 1.6, c=['matBleu', 'matJaune', 'matRouge'][i % 3])
        if i >= 4:
            sols.append(croix_sol(x, 7.05, 0.7))
    code += texte(5.0, 2.6, 'Il en reste :', 15, 'otMuted', r'\otMedium') + case_ecrire(9.4, 2.6)
    sols.append(ecrit_sol(9.4, 2.6, 4))
    fig = figure(code, sol(*sols), hauteur=9.2)
    return A('Les oiseaux s’envolent', 'Sept oiseaux sont sur la branche. Trois s’envolent. <b>Barre</b> les oiseaux qui s’envolent, puis écris combien il en reste.',
             ['barrer', 'dessiner'], 'Résoudre un problème de retrait en s’aidant d’une représentation.', 'R15', fig,
             'Accrocher sept pinces à linge sur une ficelle, en retirer trois et compter celles qui restent.',
             '« Sept, j’en enlève trois : il en reste quatre. Je le sais aussi : sept, c’est quatre et trois. »',
             'Trois oiseaux barrés (n’importe lesquels) ; il en reste quatre.', quantites=[3, 4, 7])

def a_carottes_manquantes():
    code = ''
    xs = [1.1 + i * 2.1 for i in range(8)]
    sols = []
    for i, x in enumerate(xs):
        code += P('lapin', x, 9.0, 1.8, c=['matGris', 'matJaune'][i % 2]) + cadre_pointille(x - 0.9, 4.6, x + 0.9, 7.2)
        if i < 2:
            code += P('carotte', x, 5.9, 1.9)
        else:
            sols.append(P('carotte', x, 5.9, 1.9))
    code += texte(7.0, 2.2, 'Il faut encore', 15, 'otMuted', r'\otMedium') + case_ecrire(11.2, 2.2) + texte(13.2, 2.2, 'carottes', 15, 'otMuted', r'\otMedium', 'west')
    sols.append(ecrit_sol(11.2, 2.2, 6))
    fig = figure(code, sol(*sols), hauteur=10.4)
    return A('Une carotte pour chacun', 'Chaque lapin veut une carotte, mais il n’y en a que deux. <b>Dessine</b> les carottes qui manquent, puis écris combien il en faut encore.',
             ['dessiner'], 'Trouver la quantité à ajouter pour passer d’une collection à une autre.', 'R15', fig,
             'Huit enfants veulent un vélo, deux sont sortis : combien faut-il en sortir encore ?',
             '« Il y a huit lapins et deux carottes : il manque six carottes. Deux et six, huit. »',
             'Six carottes.', quantites=[2, 6, 8])

def sac_billes(x, y, n, couleur, graine):
    code = rf'\draw[mat contour,fill=matBrun!25] ({f(x - 2.4)},{f(y - 1.6)}) rectangle ({f(x + 2.4)},{f(y + 1.6)});'
    c, _ = collection('perle', n, 'vrac', x, y, 4.4, 2.8, s=1.3, couleurs=[couleur], graine=graine)
    return code + c

def a_billes_plus():
    code = P('ours', 3.0, 11.4, 2.6, c='matBrun') + sac_billes(10.0, 11.4, 4, 'matBleu', 208)
    code += P('lapin', 3.0, 5.2, 2.6, c='matGris') + cadre_pointille(6.6, 2.8, 16.6, 7.6)
    c, _ = collection('perle', 7, 'ligne', 11.6, 5.2, 9.6, 3.0, s=1.25, couleurs=['otGreen'])
    fig = figure(code, sol(c), hauteur=13.4)
    return A('Trois billes de plus', 'L’ours a quatre billes. Le lapin a <b>trois billes de plus</b> que l’ours. Dessine les billes du lapin.', ['dessiner'],
             'Trouver une quantité à partir d’une autre et de l’écart entre les deux.', 'R16', fig,
             'Donner quatre jetons à un enfant ; un autre doit en avoir trois de plus : combien lui en donner ?',
             '« Le lapin a autant de billes que l’ours, et encore trois : quatre, cinq, six, sept. »',
             'Sept billes.', quantites=[3, 4, 7])

def a_billes_moins():
    code = P('chat', 3.0, 11.4, 2.6, c='matOrange') + sac_billes(10.0, 11.4, 5, 'matRouge', 209)
    code += P('souris', 3.0, 5.2, 2.8) + cadre_pointille(6.6, 2.8, 16.6, 7.6)
    c, _ = collection('perle', 8, 'ligne', 11.6, 5.2, 9.6, 3.0, s=1.2, couleurs=['otGreen'])
    fig = figure(code, sol(c), hauteur=13.4)
    return A('Trois billes de moins', 'Le chat a cinq billes. Il a <b>trois billes de moins</b> que la souris. Dessine les billes de la souris.', ['dessiner'],
             'Résoudre un problème d’écart dont l’énoncé dit « de moins » alors qu’il faut ajouter.', 'R16', fig,
             'Jouer la scène avec des jetons : si le chat en a trois de moins, c’est que la souris en a trois de plus.',
             '« Le chat en a moins. Donc la souris en a plus : cinq, et encore trois, huit. »',
             'Huit billes. Attention : le mot « moins » ne veut pas dire qu’il faut enlever.', quantites=[3, 5, 8])

def a_position_depart():
    code = ''
    sols = []
    for r, (dep, dpl) in enumerate([(6, 3), (7, -2)]):
        y = 10.4 - r * 5.4
        c, s_ = ligne_bande_pion(y, dep, dpl, colorie_depart=True)
        code += c
        sols.append(s_)
    fig = figure(code, sol(*sols), hauteur=12.4)
    return A('D’où est parti le pion ?', 'Le pion est arrivé sur la case où il est. Il a avancé (flèche verte) ou reculé (flèche rouge) comme le dé. Colorie la case d’où il est <b>parti</b>.',
             ['colorier'], 'Trouver la position de départ à partir de la position d’arrivée et du déplacement.', 'R17', fig,
             'Sur une piste au sol : « Je suis arrivé ici en avançant de trois. D’où suis-je parti ? »',
             '« Il a avancé de trois pour arriver sur neuf. Je recule de trois : huit, sept, six. Il était sur six. »',
             'Il est parti de 6 (il a avancé de trois jusqu’à 9), puis de 7 (il a reculé de deux jusqu’à 5).', quantites=[2, 3, 5, 6, 7, 9])

def a_assiettes2():
    code = ''
    sols = []
    for i in range(4):
        x = 2.4 + i * 4.1
        code += P('assiette', x, 9.6, 3.6)
        sols += [P('gateau', x - 0.6, 10.0, 1.1, c='otGreen'), P('gateau', x + 0.6, 10.0, 1.1, c='otGreen')]
    code += texte(1.0, 12.4, 'Deux gâteaux dans chaque assiette.', 14, 'otMuted', r'\otMedium', 'west')
    code += zone(0.4, 1.0, 9.4, 6.6) + texte(4.9, 6.0, 'la réserve', 11, 'otMuted', r'\otMedium')
    c, _ = collection('gateau', 14, 'grille', 4.9, 3.4, 8.4, 4.2, s=1.0, couleurs=['matRose', 'matJaune', 'matBleu'])
    code += c + texte(12.8, 4.6, 'J’en prends :', 14, 'otMuted', r'\otMedium') + case_ecrire(12.8, 2.6)
    sols.append(ecrit_sol(12.8, 2.6, 8))
    fig = figure(code, sol(*sols), hauteur=13.0)
    return A('Le goûter', 'On veut mettre <b>deux</b> gâteaux dans chaque assiette. Combien faut-il prendre de gâteaux dans la réserve ? Écris le nombre.',
             ['dessiner'], 'Déterminer le tout dans un problème de groupements.', 'R18', fig,
             'Quatre assiettes sur une table, des jetons sur une autre : aller chercher en un seul voyage de quoi mettre deux gâteaux par assiette.',
             '« Deux, quatre, six, huit. Il faut huit gâteaux. »',
             'Huit gâteaux : deux, quatre, six, huit.', quantites=[2, 4, 8], globales=[14])

def a_partage_reste():
    code = ''
    for i in range(7):
        code += P('gateau', 2.6 + i * 1.95, 12.4, 1.7, c=['matRose', 'matJaune', 'matBleu'][i % 3])
    sols = []
    for x, c in [(3.4, 'matBrun'), (10.4, 'matJaune')]:
        code += P('ours', x, 8.0, 2.4, c=c) + P('assiette', x, 4.8, 5.4)
        sols += [P('gateau', x - 1.3 + k * 1.3, 5.3, 1.1, c='otGreen') for k in range(3)]
    code += cadre_pointille(14.2, 3.4, 16.6, 6.4) + texte(15.4, 7.0, 'le reste', 11, 'otMuted', r'\otMedium')
    sols.append(P('gateau', 15.4, 4.9, 1.2, c='otGreen'))
    fig = figure(code, sol(*sols), hauteur=13.4)
    return A('Partager sept gâteaux', 'Partage les sept gâteaux entre les deux ours pour qu’ils en aient <b>autant</b>. Dessine-les dans les assiettes. S’il en reste un, dessine-le dans la case « le reste ».',
             ['dessiner'], 'Partager équitablement avec un reste.', 'R18', fig,
             'Distribuer sept jetons à deux poupées, un à un : il en reste un qu’on ne peut pas donner sans faire de jaloux.',
             '« Un pour toi, un pour toi… Chacun en a trois, et il en reste un. »',
             'Trois gâteaux pour chaque ours et un gâteau qui reste.', quantites=[1, 3, 7])

def a_enveloppes():
    code = ''
    images = ['pomme', 'etoile', 'poisson', 'fleur', 'ballon', 'coeur', 'voiture', 'bateau', 'soleil', 'papillon']
    for i, nom in enumerate(images):
        r, c = divmod(i, 5)
        x, y = 1.9 + c * 3.3, 11.4 - r * 3.4
        code += rf'\draw[mat contour,fill=white,rounded corners=4pt] ({f(x - 1.1)},{f(y - 1.3)}) rectangle ({f(x + 1.1)},{f(y + 1.3)});'
        code += P(nom, x, y, 1.5, c=COULEURS[i % 7])
    code += rf'\draw[mat contour,fill=matJaune!40] (1.4,1.4) rectangle (5.0,3.8) (1.4,3.8) -- (3.2,2.4) -- (5.0,3.8);'
    code += texte(9.6, 2.6, 'Il faut', 15, 'otMuted', r'\otMedium') + case_ecrire(12.0, 2.6) + texte(13.6, 2.6, 'enveloppes', 14, 'otMuted', r'\otMedium', 'west')
    sols = [rf'\draw[sol entoure,rounded corners=8pt] ({f(1.9 + c * 3.3 - 1.3)},{f(8.0 - 1.5)}) rectangle ({f(1.9 + c * 3.3 + 1.3)},{f(11.4 + 1.5)});' for c in range(5)]
    sols.append(ecrit_sol(12.0, 2.6, 5))
    fig = figure(code, sol(*sols), hauteur=13.0)
    return A('Les enveloppes', 'On range <b>deux</b> images dans chaque enveloppe. Entoure les images deux par deux, puis écris combien il faut d’enveloppes.',
             ['entourer', 'dessiner'], 'Trouver le nombre de parts dans un problème de groupements.', 'R18', fig,
             'Ranger dix images dans des enveloppes, deux par enveloppe, et compter les enveloppes utilisées.',
             '« Deux, quatre, six, huit, dix : cinq enveloppes. »',
             'Cinq enveloppes. On peut regrouper les images de bien des façons, par paires.', quantites=[2, 5, 10])

# ------------------------------------------------------------------ partie 6 : formes, solides, règle
def a_quatre_formes():
    rnd = random.Random(301)
    formes_ = ['carre'] * 4 + ['rectangle'] * 4 + ['triangle'] * 4 + ['disque'] * 4
    rnd.shuffle(formes_)
    coul = {'carre': 'matRouge', 'rectangle': 'matBleu', 'triangle': 'matJaune', 'disque': 'otGreen'}
    code = ''
    sols = []
    for i, k in enumerate(formes_):
        r, c = divmod(i, 4)
        x, y = 2.2 + c * 4.2, 13.4 - r * 3.6
        t = [0.8, 1.05, 0.9, 1.15][(i + r) % 4] * (0.85 if k == 'rectangle' else 1)
        a = rnd.choice([0, 15, 30, 50, 75, 105, 140])
        code += forme(k, x, y, t, a, 'white')
        sols.append(forme(k, x, y, t, a, coul[k]))
    for x, k, t in [(0.8, 'carre', 'carrés'), (5.0, 'rectangle', 'rectangles'), (9.4, 'triangle', 'triangles'), (13.4, 'disque', 'disques')]:
        code += rf'\fill[{coul[k]}] ({f(x)},1.0) circle (0.3);' + texte(x + 0.5, 1.0, t, 12, 'otMuted', r'\otMedium', 'west')
    fig = figure(code, sol(*sols), hauteur=15.2)
    return A('Quatre familles de formes', 'Colorie les carrés en <b>rouge</b>, les rectangles en <b>bleu</b>, les triangles en <b>jaune</b> et les disques en <b>vert</b>.', ['colorier'],
             'Reconnaître et classer carrés, rectangles, triangles et disques, quelles que soient leur taille et leur orientation.', 'R20', fig,
             'Trier des formes en carton dans quatre boîtes ; les décrire : nombre de côtés, côtés pareils ou non.',
             '« Le carré a quatre côtés tous pareils. Le rectangle a quatre côtés : deux longs et deux courts. »',
             'Quatre formes de chaque famille. Les formes penchées gardent leur nom.', quantites=[4])

def a_combien_cotes():
    pieces = [('triangle', 1.3, 25), ('carre', 1.1, 40), ('rectangle', 0.95, 15), ('triangle', 1.2, 200), ('rectangle', 0.9, 70), ('carre', 1.0, 10)]
    cotes = {'triangle': 3, 'carre': 4, 'rectangle': 4}
    code = ''
    sols = []
    for i, (k, t, a) in enumerate(pieces):
        r, c = divmod(i, 3)
        x, y = 3.0 + c * 5.5, 11.2 - r * 6.4
        code += forme(k, x, y, t, a, COULEURS[i % 7]) + case_ecrire(x, y - 2.9, 2.0, 1.8)
        sols.append(ecrit_sol(x, y - 2.9, cotes[k], 32))
    fig = figure(code, sol(*sols), hauteur=13.4)
    return A('Combien de côtés ?', 'Compte les côtés de chaque forme. <b>Écris</b> le nombre dans la case.', ['dessiner'],
             'Décrire des formes planes : compter leurs côtés.', 'R20', fig,
             'Faire le tour d’une forme en bois avec le doigt en comptant les côtés.',
             '« Le triangle a trois côtés. Le carré et le rectangle en ont quatre. »',
             '3, 4, 4 ; 3, 4, 4.', quantites=[3, 4])

def a_faces_cube():
    rnd = random.Random(302)
    pieces = [('carre', 1.0, True)] * 6 + [('carre', 1.45, False), ('rectangle', 0.9, False), ('triangle', 1.2, False), ('rectangle', 0.75, False), ('disque', 1.0, False), ('triangle_equi', 1.3, False)]
    rnd.shuffle(pieces)
    code = ''
    sols = []
    for i, (k, t, bon) in enumerate(pieces):
        r, c = divmod(i, 4)
        x, y = 2.2 + c * 4.2, 11.6 - r * 4.4
        a = rnd.choice([0, 20, 35, 60])
        code += forme(k, x, y, t, a, 'white')
        if bon:
            sols.append(forme(k, x, y, t, a, 'otGreen'))
    fig = figure(code, sol(*sols), hauteur=14.0)
    return A('Les faces du cube', 'On veut fabriquer un cube en collant des faces. <b>Colorie</b> toutes les faces qu’il faut. Combien en faut-il ?',
             ['colorier', 'manipuler'], 'Décrire un cube : six faces carrées, toutes pareilles.', 'R19', fig,
             'Observer un vrai cube : poser une gommette sur chaque face en comptant. Comparer avec un pavé.',
             '« Le cube a six faces. Ce sont des carrés, tous de la même taille. »',
             'Les six petits carrés pareils. Le grand carré est trop grand ; les autres formes ne sont pas des carrés.',
             quantites=[6], controles=[(sum(b for _, _, b in pieces) == 6, 'six faces')])

def a_faces_pyramide():
    rnd = random.Random(303)
    tri = lambda x, y, a, c: poly([(x + 1.3 * cos(radians(a + d)) * (1 if d != 90 else 1.25), y + 1.3 * sin(radians(a + d)) * (1 if d != 90 else 1.25)) for d in (210, 330, 90)], c)
    pieces = [('carre', True), ('tri', True), ('tri', True), ('tri', True), ('tri', True), ('disque', False), ('rectangle', False), ('carre2', False), ('triangle', False)]
    rnd.shuffle(pieces)
    code = ''
    sols = []
    for i, (k, bon) in enumerate(pieces):
        r, c = divmod(i, 3)
        x, y = 3.0 + c * 5.5, 11.4 - r * 4.6
        a = rnd.choice([0, 25, 50, 80])
        if k == 'tri':
            code += tri(x, y, a, 'white')
            if bon:
                sols.append(tri(x, y, a, 'otGreen'))
        else:
            kind, t = {'carre': ('carre', 1.13), 'carre2': ('carre', 0.7), 'disque': ('disque', 1.1), 'rectangle': ('rectangle', 0.9), 'triangle': ('triangle_equi', 0.8)}[k]
            code += forme(kind, x, y, t, a, 'white')
            if bon:
                sols.append(forme(kind, x, y, t, a, 'otGreen'))
    fig = figure(code, sol(*sols), hauteur=14.2)
    return A('Les faces de la pyramide', 'On veut fabriquer une pyramide comme celle de la classe : un carré en dessous et des triangles tout autour. <b>Colorie</b> les faces qu’il faut.',
             ['colorier', 'manipuler'], 'Décrire une pyramide à base carrée : un carré et quatre triangles.', 'R19', fig,
             'Observer une vraie pyramide à base carrée, compter ses faces, les faire « tamponner » dans la peinture.',
             '« La pyramide a une face carrée et quatre faces triangulaires toutes pareilles. »',
             'Le grand carré et les quatre triangles pareils. Le petit carré, le petit triangle, le disque et le rectangle ne conviennent pas.',
             quantites=[1, 4], controles=[(sum(b for _, b in pieces) == 5, 'cinq faces')])

TANGRAM = [[(0, 0), (2, 2), (0, 4)], [(0, 0), (4, 0), (2, 2)], [(4, 4), (2, 4), (4, 2)], [(4, 0), (4, 2), (3, 1)],
           [(2, 2), (3, 1), (4, 2), (3, 3)], [(2, 2), (3, 3), (1, 3)], [(0, 4), (1, 3), (3, 3), (2, 4)]]

def tangram(x0, y0, s, couleurs):
    return ''.join(poly([(x0 + s * a, y0 + s * b) for a, b in p], c) for p, c in zip(TANGRAM, couleurs))

def a_tangram():
    modele = ['matRouge', 'matBleu', 'matJaune', 'otGreen', 'matOrange', 'matViolet', 'matRose']
    code = texte(2.8, 9.8, 'le modèle', 12, 'otMuted', r'\otMedium') + tangram(0.6, 4.6, 1.1, modele)
    code += tangram(7.6, 0.8, 2.25, ['white'] * 7)
    fig = figure(code, sol(tangram(7.6, 0.8, 2.25, modele)), hauteur=10.4)
    return A('Le tangram', 'Le grand carré est fait des mêmes sept pièces que le modèle. <b>Colorie</b> chaque pièce de la même couleur que sur le modèle.',
             ['colorier', 'manipuler'], 'Reproduire un assemblage de sept formes, même s’il n’est pas à la même taille.', 'R21', fig,
             'Reconstituer un vrai tangram sur son modèle, puis sur un modèle plus grand ou plus petit.',
             '« Les deux grands triangles sont à gauche et en bas. Le carré est penché, au milieu. »',
             'Chaque pièce garde sa place et sa couleur ; seule la taille change.',
             controles=[(abs(sum(aire(p) for p in TANGRAM) - 16) < 1e-9, 'les sept pièces recouvrent le carré')])

def a_regle():
    maison = [(1.6, 1.2), (7.0, 1.2), (7.0, 5.8), (4.3, 8.5), (1.6, 5.8)]
    code = zone(0.3, 0.2, 8.3, 10.6) + zone(8.7, 0.2, 16.7, 10.6)
    code += texte(4.3, 10.0, 'la maison', 11, 'otMuted', r'\otMedium') + texte(12.7, 10.0, 'l’étoile', 11, 'otMuted', r'\otMedium')
    for i, (x, y) in enumerate(maison):
        code += point(x, y) + texte(x + (-0.55 if x < 4 else 0.55) * (0 if i == 3 else 1), y + (0.6 if i == 3 else -0.1), str(i + 1), 14, 'otNavy', r'\otBold')
    etoile = [(12.7 + 3.1 * cos(radians(90 + 144 * k)), 4.9 + 3.1 * sin(radians(90 + 144 * k))) for k in range(5)]
    for i, (x, y) in enumerate(etoile):
        nx, ny = x - 12.7, y - 4.9
        code += point(x, y) + texte(x + 0.2 * nx, y + 0.2 * ny, str(i + 1), 14, 'matViolet', r'\otBold')
    code += rf'\draw[mat contour,fill=matJaune!50] (4.5,11.6) rectangle (12.5,12.6);'
    for k in range(9):
        code += rf'\draw[matTrait,line width=0.8pt] ({f(4.9 + k * 0.9)},12.6) -- ({f(4.9 + k * 0.9)},{f(12.2 if k % 2 else 11.95)});'
    sols = [chemin_sol(maison + [maison[0]]), chemin_sol(etoile + [etoile[0]])]
    fig = figure(code, sol(*sols), hauteur=12.9)
    return A('Avec la règle', 'Avec ta <b>règle</b>, relie les points dans l’ordre : 1 avec 2, 2 avec 3… et le dernier avec 1. Fais la maison, puis l’étoile.',
             ['tracer'], 'Utiliser la règle pour tracer des traits droits.', 'R22', fig,
             'Apprendre à tenir la règle : la main à plat au milieu, le crayon qui glisse le long du bord.',
             '« Je pose la règle sur les deux points, je la tiens bien et je trace. »',
             'Une maison à cinq côtés et une étoile à cinq branches.')

# ------------------------------------------------------------------ partie 7 : longueurs et masses
def a_bande_temoin():
    crayons = [(1.0, 2.4, 35, 7.2, 'matBleu'), (9.6, 12.2, -62, 8.0, 'matRouge'), (1.4, 12.6, -8, 6.4, 'otGreen')]
    code = ''
    for x, y, a, L, c in crayons:
        code += P('crayon', x, y, 1.6, c=c, l=L / 1.6, rot=a)
    code += rf'\draw[mat contour,fill=matJaune!40] (8.6,1.0) rectangle (16.6,1.8);' + texte(12.6, 2.4, 'une bande de papier', 11, 'otMuted', r'\otMedium')
    x, y, a, L, c = crayons[1]
    cx, cy = x + L / 2 * cos(radians(a)), y + L / 2 * sin(radians(a))
    sols = [rf'\draw[sol entoure,rotate around={{{a}:({f(cx)},{f(cy)})}}] ({f(cx)},{f(cy)}) ellipse ({f(L / 2 + 0.6)} and 0.8);']
    fig = figure(code, sol(*sols), hauteur=13.6)
    return A('La bande témoin', 'Quel crayon est le plus long ? Marque la longueur de chaque crayon sur une bande de papier pour comparer, puis <b>entoure</b> le plus long.',
             ['manipuler', 'entourer'], 'Comparer des longueurs avec une bande témoin quand on ne peut pas rapprocher les objets.', 'R23', fig,
             'Comparer la largeur de la porte et celle de la fenêtre avec une ficelle ou une bande de papier.',
             '« Je reporte la longueur du crayon bleu sur ma bande. Le rouge dépasse : il est plus long. »',
             'Le crayon rouge. Les écarts sont petits : il faut reporter les longueurs pour en être sûr.')

def a_ordonner5():
    longs = [6.0, 3.6, 8.6, 4.8, 7.3]
    rnd = random.Random(304)
    rang = {L: i + 1 for i, L in enumerate(sorted(longs))}
    code = ''
    sols = []
    for i, L in enumerate(longs):
        y = 13.2 - i * 2.9
        x = rnd.uniform(3.0, 16.6 - L)
        code += case_ecrire(1.2, y, 1.8, 1.8) + P('ruban', x, y, 2.4, c=COULEURS[i], l=L / 2.4)
        sols.append(ecrit_sol(1.2, y, rang[L], 30))
    fig = figure(code, sol(*sols), hauteur=14.4)
    return A('Du plus court au plus long', 'Range les rubans du plus court au plus long : écris <b>1</b> à côté du plus court, puis 2, 3, 4 et <b>5</b> à côté du plus long.',
             ['dessiner'], 'Ranger cinq objets selon leur longueur.', 'R23', fig,
             'Ranger cinq bandes de papier en escalier, en les mettant à la même origine.',
             '« Le vert est le plus court : un. Le jaune est le plus long : cinq. »',
             'Dans l’ordre des rubans : 3, 1, 5, 2, 4.', quantites=[1, 2, 3, 4, 5])

def a_meme_trait():
    code = ''
    sols = []
    for r, (nom, L, c) in enumerate([('crayon', 6.0, 'matRouge'), ('ruban', 9.6, 'matBleu')]):
        y = 12.0 - r * 6.4
        code += P(nom, 1.4, y, 2.0, c=c, l=L / 2.0) + point(1.4, y - 2.0)
        sols.append(rf'\draw[sol trait] (1.4,{f(y - 2.0)}) -- ({f(1.4 + L)},{f(y - 2.0)});')
    fig = figure(code, sol(*sols), hauteur=13.0)
    return A('Aussi long', 'À partir du point, trace avec ta règle un trait <b>aussi long</b> que l’objet du dessus.', ['tracer'],
             'Produire un trait de même longueur qu’un objet donné.', 'R23', fig,
             'Couper une ficelle aussi longue qu’un crayon, puis aussi longue que la table.',
             '« Je mets ma règle sous le crayon, je repère où il s’arrête, puis je trace jusque-là. »',
             'Deux traits qui commencent au point et finissent juste sous la fin du crayon et du ruban.')

def paquet(c):
    return lambda x, y: P('cube', x, y + 0.55, 1.35, c=c)

def a_ordre_masses():
    code = zone(0.3, 6.4, 8.2, 13.6) + zone(8.8, 6.4, 16.7, 13.6)
    code += sur_balance(4.25, 8.4, 2.4, -1, paquet('matRouge'), paquet('matBleu'))
    code += sur_balance(12.75, 8.4, 2.4, -1, paquet('matBleu'), paquet('matJaune'))
    xs = [3.0, 8.5, 14.0]
    for x, c in zip(xs, ['matBleu', 'matJaune', 'matRouge']):
        code += P('cube', x, 3.0, 2.6, c=c)
    sols = [entoure_sol(14.0, 3.0, 1.8, 1.8), croix_sol(8.5, 3.0, 1.2)]
    fig = figure(code, sol(*sols), hauteur=13.9)
    return A('Le plus lourd des trois', 'Regarde les deux balances. En bas, <b>entoure</b> le paquet le plus lourd et <b>barre</b> le plus léger.', ['entourer', 'barrer'],
             'Ordonner les masses de trois objets à partir de deux comparaisons.', 'R24', fig,
             'Comparer trois boîtes de même taille sur une balance de Roberval, deux par deux.',
             '« Le rouge est plus lourd que le bleu. Le bleu est plus lourd que le jaune. Donc le rouge est le plus lourd. »',
             'Le paquet rouge est le plus lourd, le jaune le plus léger.')

def pile_cubes(n, c='matViolet', s=0.95):
    def dessin(x, y):
        code = ''
        rangs = [min(2, n - 2 * k) for k in range((n + 1) // 2)]
        for j, m in enumerate(rangs):
            for i in range(m):
                code += P('cube', x + (i - (m - 1) / 2) * s * 0.85, y + s * 0.42 + j * s * 0.82, s, c=c)
        return code
    return dessin

def a_equilibre():
    code = ''
    sols = []
    for r, (g, d) in enumerate([(4, 2), (5, 2)]):
        y = 9.6 - r * 6.4
        code += zone(0.3, y - 2.6, 16.7, y + 3.4)
        code += sur_balance(4.8, y, 2.6, -1, pile_cubes(g), pile_cubes(d))
        for k, v in enumerate([1, 2, 3]):
            x = 10.6 + k * 2.4
            code += chiffre(x, y + 0.4, v, 44)
            if v == g - d:
                sols.append(entoure_sol(x, y + 0.4, 0.9, 1.0))
    fig = figure(code, sol(*sols), hauteur=13.4)
    return A('L’équilibre', 'Tous les cubes ont la même masse. Combien de cubes faut-il <b>ajouter</b> sur le plateau de droite pour que la balance soit droite ? Entoure le nombre.',
             ['entourer', 'manipuler'], 'Réaliser l’équilibre sur une balance de Roberval.', 'R24', fig,
             'Avec une vraie balance et des cubes identiques, chercher à rendre la balance droite.',
             '« À gauche, il y a quatre cubes ; à droite, deux. Il faut en ajouter deux pour avoir autant. »',
             '2, puis 3.', quantites=[1, 2, 3, 4, 5])

# ------------------------------------------------------------------ partie 8 : motifs
def a_evolutif():
    code = ''
    sols = []
    seq1 = list('CDCCDDCCCDDD')
    for i, k in enumerate(seq1):
        code += symb(k, 0.8 + i * 1.32, 12.8, 0.85)
    for j in range(4):
        x = 2.0 + j * 1.6
        code += cadre_pointille(x - 0.7, 9.4, x + 0.7, 10.8)
        sols.append(symb('C', x, 10.1, 0.85))
    seq2 = list('EDEDDEDDD')
    for i, k in enumerate(seq2):
        code += symb(k, 0.8 + i * 1.6, 6.2, 0.9)
    for j in range(5):
        x = 2.0 + j * 1.6
        code += cadre_pointille(x - 0.75, 2.4, x + 0.75, 3.9)
        sols.append(symb('E' if j == 0 else 'D', x, 3.15, 0.9))
    code += texte(14.6, 10.1, 'à toi !', 13, 'otMuted', r'\otMedium') + texte(14.6, 3.15, 'à toi !', 13, 'otMuted', r'\otMedium')
    fig = figure(code, sol(*sols), hauteur=13.8)
    return A('Ça grandit', 'Dans ces rangées, il y en a <b>un de plus à chaque fois</b>. Dessine dans les cases ce qui vient après.', ['dessiner', 'dire'],
             'Repérer et prolonger un motif évolutif.', 'R25', fig,
             'Faire des rythmes qui grandissent : un tape, un claque ; deux tapes, deux claques…',
             '« Un carré, un rond ; deux carrés, deux ronds ; trois carrés, trois ronds… puis quatre carrés. »',
             'Première rangée : quatre carrés. Deuxième rangée : une étoile, puis quatre ronds.')

def a_tours_croissantes():
    code = ''
    sols = []
    for k, n in enumerate([1, 2, 3, 4]):
        code += tour(1.6 + k * 3.2, 7.6, ['matViolet'] * n, 1.0)
    code += cadre_pointille(13.6, 7.4, 16.6, 11.2)
    sols.append(tour(15.1, 7.6, ['otGreen'] * 5, 1.0))
    for k, n in enumerate([6, 5, 4, 3]):
        code += ''.join(P('etoile', 1.6 + k * 3.2, 1.0 + j * 0.9, 1.0, c='matJaune') for j in range(n))
    code += cadre_pointille(13.6, 0.4, 16.6, 6.4)
    sols += [P('etoile', 15.1, 1.0 + j * 0.9, 1.0, c='otGreen') for j in range(2)]
    code += rf'\draw[otRule,line width=1pt] (0.4,6.9) -- (16.6,6.9);'
    fig = figure(code, sol(*sols), hauteur=11.6)
    return A('Plus grand, plus petit', 'Regarde comment les tours changent. <b>Dessine</b> la tour qui vient après dans chaque cadre en pointillés.', ['dessiner', 'dire'],
             'Prolonger un motif évolutif et dire sa règle.', 'R25', fig,
             'Construire des tours de cubes de plus en plus hautes, puis de plus en plus basses.',
             '« Un cube de plus à chaque fois : la suivante a cinq cubes. En bas, une étoile de moins : il en reste deux. »',
             'Une tour de cinq cubes ; une pile de deux étoiles.', quantites=[1, 2, 3, 4, 5, 6])

def a_transcrire():
    code = ''
    sols = []
    lignes_ = [('CTCTCT', {'C': 'E', 'T': 'D'}), ('CCDCCDCCD', {'C': 'T', 'D': 'E'})]
    for r, (seq, trad) in enumerate(lignes_):
        y0 = 13.0 - r * 6.8
        for i, k in enumerate(seq):
            code += symb(k, 1.0 + i * 1.75, y0, 0.9)
        code += texte(0.3, y0 - 1.6, 'avec', 11, 'otMuted', r'\otMedium', 'west')
        legende = ''.join(sorted(set(trad.values()), key=list(trad.values()).index))
        for j, k in enumerate(legende):
            code += symb(k, 2.4 + j * 1.5, y0 - 1.6, 0.6)
        for i, k in enumerate(seq):
            x = 1.0 + i * 1.75
            code += cadre_pointille(x - 0.75, y0 - 4.0, x + 0.75, y0 - 2.5)
            sols.append(symb(trad[k], x, y0 - 3.25, 0.85))
    fig = figure(code, sol(*sols), hauteur=14.2)
    return A('Le même motif, autrement', 'Refais chaque rangée dans les cases, mais <b>avec les formes proposées</b> : la règle doit rester la même.', ['dessiner'],
             'Transcrire un motif avec d’autres symboles en gardant sa structure.', 'R25', fig,
             'Traduire un collier rouge-bleu en sons (tape, claque) ou en gestes (debout, assis).',
             '« Carré, triangle, carré, triangle… devient étoile, rond, étoile, rond. »',
             'Première rangée : étoile, rond, étoile, rond, étoile, rond. Deuxième : triangle, triangle, étoile, trois fois.')

def a_meme_structure():
    code = ''
    sols = []
    lignes_ = [('EDDEDDEDD', True), ('CCTCCTCCT', False), ('TCCTCCTCC', True), ('DEDEDEDED', False)]
    for r, (seq, bon) in enumerate(lignes_):
        y = 13.4 - r * 3.9
        code += zone(0.3, y - 1.35, 16.7, y + 1.35)
        for i, k in enumerate(seq):
            code += symb(k, 1.4 + i * 1.78, y, 0.9)
        if bon:
            sols.append(entoure_sol(8.5, y, 8.6, 1.7))
    fig = figure(code, sol(*sols), hauteur=15.0)
    return A('La même règle', 'Deux rangées sont faites avec la <b>même règle</b>, même si les formes changent. Entoure-les.', ['entourer', 'dire'],
             'Reconnaître des motifs qui ont la même structure avec des éléments différents.', 'R25', fig,
             'Comparer « tape, cuisse, cuisse » et un collier « rouge, bleu, bleu » : c’est la même règle.',
             '« Un, puis deux pareils ; un, puis deux pareils. »',
             'La première (étoile, rond, rond) et la troisième (triangle, carré, carré) : une forme, puis deux formes pareilles.')

def a_creer():
    code = rf'\draw[matTrait,line width=1.3pt] (0.6,10.0) .. controls (5,7.6) and (12,7.6) .. (16.4,10.0);'
    pts = []
    for i in range(10):
        t = (i + 1) / 11
        x = (1 - t) ** 3 * 0.6 + 3 * (1 - t) ** 2 * t * 5 + 3 * (1 - t) * t ** 2 * 12 + t ** 3 * 16.4
        y = (1 - t) ** 3 * 10 + 3 * (1 - t) ** 2 * t * 7.6 + 3 * (1 - t) * t ** 2 * 7.6 + t ** 3 * 10
        pts.append((x, y))
        code += P('perle', x, y, 2.0, c='white')
    code += texte(8.5, 4.6, 'Ma règle :', 14, 'otMuted', r'\otMedium')
    code += rf'\draw[otRule,line width=1pt] (2.0,3.2) -- (15.0,3.2) (2.0,1.6) -- (15.0,1.6);'
    motif = ['matRouge', 'matRouge', 'matBleu']
    sols = [P('perle', x, y, 2.0, c=motif[i % 3]) for i, (x, y) in enumerate(pts)]
    sols.append(texte(8.5, 3.6, 'deux rouges, une bleue, et on recommence', 12, 'otGreenDark', r'\otSemi'))
    fig = figure(code, sol(*sols), hauteur=11.2)
    return A('J’invente mon collier', 'Invente un collier avec une <b>règle</b> : choisis tes couleurs et colorie les perles. Puis explique ta règle à un adulte, qui l’écrit.',
             ['colorier', 'dire'], 'Créer un motif et le décrire pour qu’un autre puisse le reproduire.', 'R25', fig,
             'Un enfant invente un collier et le décrit à un camarade qui le fabrique sans le voir.',
             '« Ma règle : deux rouges, une bleue, et on recommence. »',
             'Toutes les réponses sont justes si les couleurs suivent la règle annoncée. L’image montre un exemple.')

# ------------------------------------------------------------------ partie 9 : se repérer
def a_sens_animaux():
    animaux = [('canard', 'matJaune', False), ('poisson', 'matBleu', False), ('escargot', 'matRose', True), ('oiseau', 'matRouge', True),
               ('elephant', None, False), ('souris', None, True), ('canard', 'matJaune', True), ('poisson', 'matOrange', True)]
    # Sens naturel du dessin : canard, escargot, éléphant regardent à droite ; poisson, oiseau, souris à gauche.
    naturel_droite = {'canard': True, 'escargot': True, 'elephant': True, 'poisson': False, 'oiseau': False, 'souris': False}
    code = rf'\draw[matViolet,line width=4pt,-{{Stealth[length=6mm]}}] (6.0,13.6) -- (11.0,13.6);' + texte(8.5, 12.6, 'vers la droite', 13, 'matViolet', r'\otSemi')
    sols = []
    for i, (nom, c, retourne) in enumerate(animaux):
        r, col = divmod(i, 4)
        x, y = 2.2 + col * 4.2, 9.2 - r * 5.0
        code += zone(x - 1.9, y - 2.0, x + 1.9, y + 2.0)
        code += miroir(nom, x, y, 2.6, c) if retourne else P(nom, x, y, 2.6, c=c)
        if naturel_droite[nom] != retourne:
            sols.append(entoure_sol(x, y, 1.7, 1.7))
    fig = figure(code, sol(*sols), hauteur=14.2)
    return A('Vers la droite', 'Entoure les animaux qui regardent <b>vers la droite</b>, comme la flèche.', ['entourer'],
             'Distinguer la droite et la gauche.', 'R26', fig,
             'Jeu de Jacques a dit : « Lève la main droite, tourne vers la gauche… »',
             '« Ce canard regarde vers la droite, comme la flèche. Ce poisson regarde vers la gauche. »',
             'Le premier canard, l’oiseau, l’éléphant, la souris et le poisson orange regardent vers la droite.',
             controles=[(sum(naturel_droite[n] != r for n, _, r in animaux) == 5, 'cinq animaux vers la droite')])

def a_gauche_droite():
    code = rf'\draw[mat contour,fill=matBrun!70] (0.4,5.2) rectangle (16.6,5.8);'
    objets_ = [('ballon', 'matRouge', 2.0), ('chat', 'matOrange', 2.4), ('pomme', 'matVert', 2.0), ('ours', 'matBrun', 2.4), ('voiture', 'matBleu', 2.4), ('lapin', 'matGris', 2.4)]
    xs = [1.8 + i * 2.7 for i in range(6)]
    for (nom, c, s), x in zip(objets_, xs):
        code += P(nom, x, 6.9, s, c=c)
    sols = [entoure_sol(xs[2], 6.9, 1.3, 1.3), croix_sol(xs[4], 6.9, 0.9)]
    code += texte(0.6, 3.6, 'gauche', 12, 'otMuted', r'\otMedium', 'west') + texte(16.4, 3.6, 'droite', 12, 'otMuted', r'\otMedium', 'east')
    code += rf'\draw[otMuted,line width=1.4pt,{{Stealth[length=3mm]}}-{{Stealth[length=3mm]}}] (2.6,3.6) -- (14.4,3.6);'
    fig = figure(code, sol(*sols), hauteur=8.6)
    return A('À gauche, à droite', 'Entoure l’objet qui est juste <b>à droite</b> du chat. Fais une croix sur l’objet qui est juste <b>à gauche</b> du lapin.',
             ['entourer', 'barrer'], 'Situer un objet par rapport à un autre avec « à gauche de », « à droite de ».', 'R26', fig,
             'Ranger des jouets sur une étagère en suivant des consignes : « Mets la voiture à gauche de l’ours. »',
             '« La pomme est à droite du chat. La voiture est à gauche du lapin. »',
             'La pomme est entourée, la voiture barrée.')

def fleche_case(x, y, d, taille=0.55, couleur='otNavy'):
    v = {'D': (1, 0), 'G': (-1, 0), 'H': (0, 1), 'B': (0, -1)}[d]
    return rf'\draw[{couleur},line width=2.6pt,-{{Stealth[length=3mm]}}] ({f(x - v[0] * taille)},{f(y - v[1] * taille)}) -- ({f(x + v[0] * taille)},{f(y + v[1] * taille)});'

def grille(x0, y0, cols, lignes, pas):
    code = ''
    for c in range(cols + 1):
        code += rf'\draw[matTrait,line width=1pt] ({f(x0 + c * pas)},{f(y0)}) -- ({f(x0 + c * pas)},{f(y0 + lignes * pas)});'
    for l in range(lignes + 1):
        code += rf'\draw[matTrait,line width=1pt] ({f(x0)},{f(y0 + l * pas)}) -- ({f(x0 + cols * pas)},{f(y0 + l * pas)});'
    return code

def a_codage():
    x0, y0, pas = 1.2, 4.0, 2.1
    centre = lambda c, l: (x0 + (c + 0.5) * pas, y0 + (l + 0.5) * pas)
    code = grille(x0, y0, 7, 5, pas)
    code += P('etoile', *centre(0, 0), 1.6, c='matJaune')
    for (c, l, nom, coul) in [(3, 4, 'arbre', None), (1, 3, 'fleur', 'matRose'), (6, 1, 'champignon', 'matRouge'), (4, 0, 'pomme', 'matRouge')]:
        code += P(nom, *centre(c, l), 1.5, c=coul)
    moves = 'DDHHDDHG'
    for i, m in enumerate(moves):
        x = 1.6 + i * 1.95
        code += rf'\draw[mat contour,fill=white,rounded corners=3pt] ({f(x - 0.75)},0.6) rectangle ({f(x + 0.75)},2.1);' + fleche_case(x, 1.35, m)
    pos = [(0, 0)]
    for m in moves:
        c, l = pos[-1]
        dc, dl = {'D': (1, 0), 'G': (-1, 0), 'H': (0, 1), 'B': (0, -1)}[m]
        pos.append((c + dc, l + dl))
    ac, al = pos[-1]
    sols = [chemin_sol([centre(*p) for p in pos]),
            rf'\fill[otGreen,opacity=.5] ({f(x0 + ac * pas)},{f(y0 + al * pas)}) rectangle ({f(x0 + (ac + 1) * pas)},{f(y0 + (al + 1) * pas)});']
    fig = figure(code, sol(*sols), hauteur=14.6)
    return A('Le code secret', 'Pars de l’étoile et suis les flèches du code, une case par flèche. <b>Colorie</b> la case où tu arrives.', ['colorier'],
             'Réaliser un déplacement à partir de son codage par des flèches.', 'R26', fig,
             'Dans la cour, sur un quadrillage tracé à la craie, avancer d’une case par flèche lue par un camarade.',
             '« Droite, droite, haut, haut, droite, droite, haut, gauche. »',
             'On arrive dans la case juste sous l’arbre.',
             controles=[(all(0 <= c < 7 and 0 <= l < 5 for c, l in pos), 'le chemin reste dans la grille'), (pos[-1] == (3, 3), 'arrivée prévue')])

def a_coder_chemin():
    x0, y0, pas = 1.6, 4.0, 2.0
    centre = lambda c, l: (x0 + (c + 0.5) * pas, y0 + (l + 0.5) * pas)
    code = grille(x0, y0, 7, 5, pas)
    moves = 'DDBDBBDDDB'
    pos = [(0, 4)]
    for m in moves:
        c, l = pos[-1]
        dc, dl = {'D': (1, 0), 'G': (-1, 0), 'H': (0, 1), 'B': (0, -1)}[m]
        pos.append((c + dc, l + dl))
    code += rf'\draw[matViolet,line width=3pt,dash pattern=on 6pt off 4pt] ' + ' -- '.join(f'({f(x)},{f(y)})' for x, y in (centre(*p) for p in pos)) + ';'
    code += P('souris', *centre(*pos[0]), 1.5) + P('fromage', *centre(*pos[-1]), 1.5)
    for (c, l) in [(0, 0), (1, 1), (5, 4), (4, 3), (6, 3), (2, 0)]:
        if (c, l) not in pos:
            code += P('sapin', *centre(c, l), 1.6)
    sols = []
    for i, m in enumerate(moves):
        x = 1.0 + i * 1.66
        code += rf'\draw[mat contour,fill=white,rounded corners=3pt] ({f(x - 0.72)},0.6) rectangle ({f(x + 0.72)},2.1);'
        sols.append(fleche_case(x, 1.35, m, couleur='otGreenDark'))
    fig = figure(code, sol(*sols), hauteur=14.4)
    return A('J’écris le chemin', 'Le chemin de la souris est en pointillés. <b>Dessine</b> une flèche par case dans les cadres du bas pour coder son chemin jusqu’au fromage.',
             ['dessiner'], 'Coder un déplacement à l’aide de flèches.', 'R26', fig,
             'Un enfant se déplace sur un quadrillage au sol ; un autre code son trajet avec des cartes-flèches.',
             '« La souris va à droite, à droite, puis elle descend… »',
             'Droite, droite, bas, droite, bas, bas, droite, droite, droite, bas.',
             controles=[(len(moves) == 10 and pos[-1] == (6, 0), 'dix flèches jusqu’au fromage')])

QUADRI = {(2, 4): 'matRouge', (1, 3): 'matRouge', (2, 3): 'matRouge', (3, 3): 'matRouge', (1, 2): 'matJaune', (2, 2): 'matJaune',
          (3, 2): 'matJaune', (1, 1): 'matJaune', (2, 1): 'matBrun', (3, 1): 'matJaune', (0, 0): 'otGreen', (1, 0): 'otGreen',
          (2, 0): 'otGreen', (3, 0): 'otGreen', (4, 0): 'otGreen'}

def quadri(x0, y0, pas, cases):
    code = ''.join(rf'\fill[{c}] ({f(x0 + col * pas)},{f(y0 + l * pas)}) rectangle ({f(x0 + (col + 1) * pas)},{f(y0 + (l + 1) * pas)});' for (col, l), c in cases.items())
    return code + grille(x0, y0, 5, 5, pas)

def a_quadrillage():
    code = texte(3.0, 7.8, 'le modèle', 12, 'otMuted', r'\otMedium') + quadri(0.6, 2.2, 0.95, QUADRI) + quadri(7.0, 0.6, 1.9, {})
    fig = figure(code, sol(quadri(7.0, 0.6, 1.9, QUADRI)), hauteur=10.4)
    return A('Sur le quadrillage', 'Reproduis le dessin du modèle sur le grand quadrillage : <b>colorie</b> les mêmes cases, de la même couleur.', ['colorier'],
             'Repérer des cases sur un quadrillage pour reproduire un dessin.', 'R26', fig,
             'Reproduire un dessin fait de gommettes sur une grille, en comptant les cases depuis un coin.',
             '« Le toit rouge est en haut, au milieu. La porte marron est sur la deuxième ligne. »',
             'Une maison : un toit rouge, des murs jaunes, une porte marron, et une bande d’herbe verte en bas.',
             controles=[(len(QUADRI) == 15, 'quinze cases coloriées')])

PARTIES = [
 ('Compter jusqu’à dix', 'Dénombrer, constituer, comparer.',
  'À partir de cinq ans, l’enfant dénombre des collections jusqu’à dix, voire au-delà, en utilisant des compositions (« cinq et deux, sept »). Il constitue des collections à partir de l’écriture chiffrée et compare des nombres.',
  [a_sept_partout, a_combien_gs, a_cartes_doubles, a_parcours_bonbons, a_dessine_chiffre, a_plus_grand, a_autant_panier], 'pomme'),
 ('Composer les nombres', 'Un de plus, un de moins, surcompter, les doubles.',
  'L’enfant comprend que chaque nombre s’obtient en ajoutant un au précédent. Il surcompte à partir d’un nombre gardé « dans sa tête » et mémorise des compositions, dont les doubles, qui lui permettent de calculer sans tout recompter.',
  [a_un_de_moins, a_avant_apres, a_surcompter, a_doubles, a_deux_mains_gs, a_maison_8, a_dominos], 'de'),
 ('Écrire et réciter', 'Les chiffres jusqu’à dix ; la comptine jusqu’à trente.',
  'L’enfant écrit les nombres de un à dix. Il récite la comptine jusqu’à trente, à partir d’un nombre donné, de deux en deux et à rebours de dix à un, ce qui prépare le surcomptage et le décomptage.',
  [a_ecrire_789, a_ecrire_10, a_points20, a_rebours, a_deux_en_deux, a_depart], 'etoile'),
 ('Rangs et bande', 'Premier, dernier, avant-dernier ; la bande numérique.',
  'L’enfant repère le rang d’un objet dans une suite de dix, même quand on change le point de départ. Il construit la bande numérique jusqu’à dix et relie l’ajout à un avancement, le retrait à un recul.',
  [a_rang_dix, a_canards_rang, a_meme_place, a_bande10, a_bande_rep, a_oie_gs], 'oie'),
 ('Petits problèmes', 'Réunir, enlever, comparer, regrouper, partager.',
  'En fin de maternelle, l’enfant résout des problèmes en une étape en s’aidant d’un dessin, de ses doigts ou d’une décomposition. Certains énoncés sont « discordants » : « de moins » peut demander d’ajouter. On vérifie toujours la réponse.',
  [a_trois_parties, a_oiseaux7, a_carottes_manquantes, a_billes_plus, a_billes_moins, a_position_depart, a_assiettes2, a_partage_reste, a_enveloppes], 'ours'),
 ('Formes et solides', 'Nommer, décrire, assembler, tracer à la règle.',
  'L’enfant nomme carré, rectangle, triangle et disque dans toutes les orientations, décrit le cube et la pyramide par leurs faces, reproduit des assemblages (jusqu’à huit pièces) et apprend à tracer à la règle. Aucun solide n’est dessiné en perspective.',
  [a_quatre_formes, a_combien_cotes, a_faces_cube, a_faces_pyramide, a_tangram, a_regle], 'formes'),
 ('Longueurs et masses', 'Bande témoin, rangement, balance.',
  'L’enfant compare des longueurs indirectement avec une bande témoin, range jusqu’à cinq objets et reproduit une longueur. Avec la balance de Roberval, il ordonne trois masses et réalise l’équilibre.',
  [a_bande_temoin, a_ordonner5, a_meme_trait, a_ordre_masses, a_equilibre], 'balance'),
 ('Les motifs', 'Motifs qui grandissent, même règle, invention.',
  'À cinq ans, l’enfant découvre les motifs évolutifs, transcrit un motif avec d’autres symboles, reconnaît des motifs de même structure et en invente. On n’attend pas d’écriture formelle (AABB).',
  [a_evolutif, a_tours_croissantes, a_transcrire, a_meme_structure, a_creer], 'perle'),
 ('Se repérer', 'Gauche et droite, flèches, quadrillages.',
  'L’enfant distingue sa gauche et sa droite, situe les objets les uns par rapport aux autres, code et décode des déplacements avec des flèches et reproduit un dessin sur un quadrillage.',
  [a_sens_animaux, a_gauche_droite, a_codage, a_coder_chemin, a_quadrillage], 'souris'),
]

RESUME = (r'\begin{itemize}[leftmargin=5mm,itemsep=1.2mm,topsep=0pt]'
          r'\item dénombrer, comparer et constituer des collections jusqu’à dix, voire au-delà ;'
          r'\item surcompter, connaître les doubles et les décompositions jusqu’à dix, écrire les chiffres de 1 à 10 ;'
          r'\item réciter la comptine jusqu’à trente, à rebours et de deux en deux ;'
          r'\item repérer un rang, construire la bande numérique jusqu’à dix ;'
          r'\item résoudre des problèmes : parties-tout, écarts, positions, groupements, partages ;'
          r'\item nommer les formes, décrire le cube et la pyramide, tracer à la règle ;'
          r'\item comparer longueurs et masses, prolonger et inventer des motifs, coder des déplacements.'
          r'\end{itemize}')

PERIMETRE = (r'\textbf{3. Choix faits dans ce cahier}\par '
             r'Les quantités à dénombrer vont jusqu’à dix ; une activité de parcours en compte quatorze, et la comptine va jusqu’à trente. '
             r'Les nombres écrits ne dépassent pas dix, sauf dans les activités de comptine, où l’adulte aide à lire. '
             r'Les problèmes comportent des énoncés « discordants » (« de moins » quand il faut ajouter), comme le demande le programme. '
             r'Les solides ne sont jamais dessinés en perspective : on les décrit par leurs faces, dessinées à plat. '
             r'Les assemblages comportent au plus huit pièces. Le nombre zéro n’est pas étudié. Chaque fiche commence par une activité '
             r'avec de vrais objets, décrite dans le guide de l’adulte.')
