"""Cahier de Moyenne Section : programme « à partir de 4 ans »."""
from outils import *
from gabarits import *

NIVEAU = dict(cle='ms', nom='Moyenne Section', court='MS', age='à partir de 4 ans', accent='otOrange',
              couv=(4, 5), max_quantite=6, max_globale=30)

R = {
 'R1': 'Comprendre qu’une quantité ne dépend ni de la nature des objets ni de leur organisation (jusqu’à six)',
 'R2': 'Ajouter un : la quantité suivante, le nombre suivant',
 'R3': 'Parcourir une collection en passant une et une seule fois par chaque élément',
 'R4': 'Dénombrer une collection (jusqu’à six)',
 'R5': 'Constituer une collection d’un cardinal donné (jusqu’à six)',
 'R6': 'Comparer des quantités : globalement, terme à terme, en dénombrant',
 'R7': 'Composer et décomposer les nombres jusqu’à six',
 'R8': 'Associer une quantité, le nom d’un nombre et son écriture chiffrée',
 'R9': 'Écrire en chiffres les nombres de un à six',
 'R10': 'Connaître la comptine numérique de un à douze',
 'R11': 'Comprendre la notion de rang (jusqu’au sixième)',
 'R12': 'Déterminer l’effet d’un déplacement : avancer ou reculer d’une ou deux cases',
 'R13': 'Se familiariser avec le début de la bande numérique (jusqu’à six)',
 'R14': 'Problèmes : rechercher le tout ou une partie',
 'R15': 'Problèmes : groupements et partage équitable',
 'R16': 'Solides : produire et retrouver des empreintes',
 'R17': 'Formes planes : reconnaître et classer triangles, carrés, disques',
 'R18': 'Reproduire des assemblages de formes (au plus cinq)',
 'R19': 'Longueurs : comparer, classer en trois groupes, ordonner',
 'R20': 'Masses : comparer deux objets, utiliser une balance de Roberval',
 'R21': 'Motifs répétitifs : reconnaître, trouver l’intrus, prolonger, mémoriser',
 'R22': 'Se repérer dans l’espace : situer des objets, suivre et raconter un déplacement',
}

# ------------------------------------------------------------------ partie 1 : quantités
def a_cinq():
    contenus = [(coll('etoile', 5, 'ligne', s=1.25, couleurs=['matJaune']), 5),
                (coll('pomme', 4, 'vrac', s=1.6, couleurs=['matRouge', 'matVert'], graine=51), 4),
                (mixte('ballon', [1.0, 1.6, 1.1, 1.7, 1.2], ['matBleu', 'matRouge', 'matVert', 'matJaune', 'matViolet'], 1.45), 5),
                (coll('jeton', 6, 'de', s=1.0, couleurs=['matViolet']), 6),
                (coll('poisson', 5, 'vrac', s=1.3, couleurs=['matOrange', 'matBleu'], graine=52), 5),
                (coll('jeton', 5, 'de', s=1.0, couleurs=['matRouge']), 5)]
    code, h, bons = boites_rond(contenus, 5)
    return A('Cinq partout', 'Colorie le rond sous chaque boîte où il y a <b>cinq</b> objets.', ['colorier'],
             'Reconnaître des collections de cinq objets de tailles et de dispositions différentes.', 'R1', figure(code, hauteur=h),
             'Faire des tas de cinq objets très différents (cinq perles, cinq livres, cinq ballons de tailles variées) et vérifier en comptant.',
             '« Les ballons sont gros ou petits, mais il y en a cinq. »',
             'Les boîtes des étoiles, des ballons, des poissons et des jetons rouges : quatre boîtes. Les pommes sont quatre, les jetons violets six.',
             quantites=[4, 5, 6], controles=[(bons == 4, 'quatre boîtes à cinq objets')])

def a_bocaux():
    code = ''
    for cx, n in [(4.25, 7), (12.75, 18)]:
        code += P('bocal', cx, 1.0, 4.2, n=0)
        code += tas('perle', n, cx, 1.06, 1.6, ['matRouge', 'matBleu', 'matJaune', 'matVert'])[0]
    fig = figure(code, sol(entoure_sol(12.75, 4.1, 4.6, 3.8)), hauteur=7.6)
    return A('Le plus de billes', 'Sans compter, entoure le bocal où il y a le <b>plus</b> de billes.', ['entourer'],
             'Comparer globalement deux collections dont l’une a au moins deux fois plus d’objets que l’autre.', 'R6', fig,
             'Remplir deux pots transparents, l’un avec beaucoup de perles, l’autre avec peu ; demander sans compter où il y en a le plus.',
             '« Dans ce bocal, il y a plus de billes que dans l’autre. Dans l’autre, il y en a moins. »',
             'Le bocal de droite (dix-huit billes contre sept). On ne demande pas de compter : la différence se voit.',
             globales=[7, 18])

def a_jetons_alignes():
    code = ''
    sols = []
    for r, (nr, nb, er, eb) in enumerate([(5, 5, 3.6, 1.5), (4, 6, 4.4, 1.35)]):
        y = 12.0 - r * 7.0
        code += zone(0.3, y - 3.2, 16.7, y + 2.0)
        xr = [8.5 + (i - (nr - 1) / 2) * er for i in range(nr)]
        xb = [8.5 + (i - (nb - 1) / 2) * eb for i in range(nb)]
        for x in xr:
            code += P('jeton', x, y, 1.6, c='matRouge')
        for x in xb:
            code += P('jeton', x, y - 2.2, 1.6, c='matBleu')
        sols += [trait_sol((xr[i], y - 0.45), (xb[i], y - 1.75)) for i in range(min(nr, nb))]
        if nb > nr:
            sols += [entoure_sol(x, y - 2.2, 0.62, 0.62) for x in xb[nr:]]
    fig = figure(code, sol(*sols), hauteur=14.6)
    return A('Autant de jetons ?', 'Relie chaque jeton rouge à un jeton bleu. Dans chaque cadre, y a-t-il <b>autant</b> de jetons rouges que de bleus ?',
             ['relier', 'dire'], 'Comprendre qu’une quantité ne dépend pas de la place des objets : une rangée plus longue n’a pas forcément plus d’objets.', 'R1', fig,
             'Aligner cinq jetons rouges bien espacés et cinq bleus serrés ; demander où il y en a le plus, puis vérifier en les appariant.',
             '« La rangée rouge est plus longue, mais il y a autant de jetons : cinq et cinq. »',
             'En haut : autant (cinq et cinq). En bas : il y a plus de jetons bleus (six) que de rouges (quatre), même si la rangée bleue est plus courte.',
             quantites=[4, 5, 6])

def a_assiettes_verres():
    code = zone(0.3, 9.4, 16.7, 14.4) + texte(1.0, 13.8, 'la table', 11, 'otMuted', r'\otMedium', 'west')
    xs = [2.6 + i * 2.95 for i in range(5)]
    for x in xs:
        code += P('assiette', x, 11.4, 2.5)
    code += zone(0.3, 0.3, 16.7, 8.2) + texte(1.0, 7.6, 'le placard', 11, 'otMuted', r'\otMedium', 'west')
    verres = [(2.2 + i * 2.6, 5.0) for i in range(6)] + [(3.5 + i * 2.6, 2.1) for i in range(3)]
    sols = []
    for i, (x, y) in enumerate(verres):
        code += P('verre', x, y, 2.0, c='white')
        if i < 5:
            sols.append(P('verre', x, y, 2.0, c='otGreen'))
    fig = figure(code, sol(*sols), hauteur=14.7)
    return A('Un verre par assiette', 'Colorie juste ce qu’il faut de verres pour mettre <b>un verre</b> à côté de chaque assiette.', ['colorier'],
             'Dénombrer une collection pour en constituer une autre de même quantité, sans pouvoir les rapprocher.', 'R4', fig,
             'Mettre des assiettes sur une table et des verres sur une autre, loin : l’enfant doit rapporter juste assez de verres en un seul voyage.',
             '« Il y a cinq assiettes. Je prends cinq verres : un, deux, trois, quatre, cinq. »',
             'Cinq verres coloriés, n’importe lesquels : il y a cinq assiettes.', quantites=[5], globales=[9])

def a_voitures_bateaux():
    code = zone(0.3, 0.3, 8.2, 13.6) + zone(8.8, 0.3, 16.7, 13.6)
    for x, y in [(2.3, 11.0), (6.2, 8.7), (2.6, 5.2), (6.0, 2.2)]:
        code += P('voiture', x, y, 2.6, c='matRouge')
    c, _ = collection('bateau', 6, 'grille', 12.75, 7.0, 4.0, 4.0, s=1.25, couleurs=['matBleu'])
    code += c
    fig = figure(code, sol(entoure_sol(12.75, 7.0, 3.6, 3.4)), hauteur=13.9)
    return A('Voitures ou bateaux ?', 'Compte les voitures, puis les bateaux. Entoure le groupe où il y en a le <b>plus</b>.', ['entourer', 'dire'],
             'Comparer deux collections en dénombrant chacune d’elles.', 'R6', fig,
             'Poser quatre voitures sur une table et six bateaux sur une autre table, loin : comparer en comptant chaque groupe.',
             '« Il y a quatre voitures et six bateaux. Il y a plus de bateaux que de voitures. »',
             'Les bateaux : six bateaux contre quatre voitures, même si les voitures prennent plus de place.', quantites=[4, 6])

# ------------------------------------------------------------------ partie 2 : compter jusqu’à six
def a_constellations():
    gauches = [4, 6, 5, 3]
    droites = [5, 3, 6, 4]
    cols = {3: ['matRouge'], 4: ['matJaune'], 5: ['matVert'], 6: ['matBleu']}
    noms = {3: 'pomme', 4: 'etoile', 5: 'fleur', 6: 'jeton'}
    g = [boite_objets(noms[n], n, s=1.05, couleurs=cols[n], kind='vrac', w=6.4, h=3.0, graine=70 + n) for n in gauches]
    d = [lambda x, y, n=n: P('de', x, y, 2.4, n=n) for n in droites]
    perm = [droites.index(n) for n in gauches]
    code, h = relier(g, d, perm, pas=3.8, x_g=3.4, x_d=14.8, ecart_point=4.0)
    return A('Le dé et les boîtes', 'Compte les objets de chaque boîte. Relie la boîte au dé qui a <b>autant</b> de points.', ['relier'],
             'Dénombrer une collection jusqu’à six et l’associer à la constellation du dé.', 'R8', figure(code, hauteur=h),
             'Lancer un grand dé, compter les points, puis prendre autant d’objets dans une réserve.',
             '« Il y a quatre étoiles : je cherche le dé à quatre points. »',
             'Quatre étoiles avec le dé quatre, six jetons avec le dé six, cinq fleurs avec le dé cinq, trois pommes avec le dé trois.',
             quantites=[3, 4, 5, 6])

def deux_mains(n):
    """Dessin des doigts levés pour n (de 1 à 10) : une main pleine, puis la seconde."""
    def dessin(x, y):
        if n <= 5:
            return P('main', x, y, 2.6, n=n)
        return P('main', x - 1.45, y, 2.6, n=5) + P('main', x + 1.45, y, 2.6, n=n - 5)
    return dessin

def a_doigts_chiffres():
    gauches = [6, 4, 5, 3]
    droites = [3, 5, 6, 4]
    g = [deux_mains(n) for n in gauches]
    d = [lambda x, y, n=n: chiffre(x, y, n, 64) for n in droites]
    perm = [droites.index(n) for n in gauches]
    code, h = relier(g, d, perm, pas=3.9, x_g=3.2, x_d=14.8, ecart_point=3.6)
    return A('Doigts et chiffres', 'Compte les doigts levés. Relie chaque dessin au <b>chiffre</b> qui convient.', ['relier'],
             'Associer une quantité montrée avec les doigts et son écriture chiffrée.', 'R8', figure(code, hauteur=h),
             'Montrer un nombre avec ses doigts ; l’enfant le dit, puis le retrouve parmi des cartes chiffrées.',
             '« Cinq doigts sur une main et un sur l’autre : six. Je relie au 6. »',
             'Six doigts avec 6, quatre avec 4, cinq avec 5, trois avec 3. Toute façon de montrer un nombre avec ses doigts est juste.',
             quantites=[3, 4, 5, 6])

def a_combien_points():
    code = ''
    sols = []
    lignes_ = [(5, [4, 5, 6]), (3, [3, 4, 5]), (6, [4, 5, 6]), (4, [2, 3, 4])]
    for r, (n, choix) in enumerate(lignes_):
        y = 13.2 - r * 3.9
        code += rf'\draw[draw=matTrait,line width=1.2pt,fill=white,rounded corners=5pt] (0.4,{f(y - 1.6)}) rectangle (6.4,{f(y + 1.6)});'
        c, _ = collection('jeton', n, 'vrac', 3.4, y, 5.6, 2.9, s=0.95, couleurs=['matTrait'], graine=80 + r)
        code += c
        for k, v in enumerate(choix):
            x = 9.2 + k * 3.0
            code += chiffre(x, y, v, 52)
            if v == n:
                sols.append(entoure_sol(x, y, 1.0, 1.2))
    fig = figure(code, sol(*sols), hauteur=15.0)
    return A('Combien de points ?', 'Compte les points de chaque carte. Entoure le <b>bon chiffre</b>.', ['entourer'],
             'Dénombrer une collection mal rangée en pointant chaque élément une seule fois.', 'R4', fig,
             'Compter des jetons posés en vrac en les déplaçant un à un d’un côté à l’autre de la table.',
             '« Je touche chaque point une fois : un, deux, trois, quatre, cinq. Il y en a cinq. »',
             'Cinq, puis trois, puis six, puis quatre.', quantites=[3, 4, 5, 6])

def a_dessine_de():
    code = ''
    sols = []
    for r, n in enumerate([4, 6, 5]):
        y = 12.4 - r * 4.6
        code += P('de', 1.9, y, 2.8, n=n) + fleche((3.7, y), (6.0, y), 'otOrange', 3) + cadre_pointille(6.8, y - 1.8, 16.6, y + 1.8)
        c, _ = collection('pomme', n, 'ligne', 11.7, y, 9.4, 3.0, s=1.25, couleurs=['otGreen'])
        sols.append(c)
    fig = figure(code, sol(*sols), hauteur=14.6)
    return A('Autant que le dé', 'Dessine dans chaque boîte <b>autant</b> de pommes qu’il y a de points sur le dé.', ['dessiner'],
             'Constituer une collection de même quantité qu’une constellation donnée.', 'R5', fig,
             'Jeu de marchande : lancer le dé et acheter autant de fruits (jetons) qu’il y a de points.',
             '« Quatre points : je dessine quatre pommes. Je compte pour vérifier. »',
             'Quatre, six et cinq pommes. Des ronds suffisent pour représenter les pommes.', quantites=[4, 5, 6])

def a_un_de_plus_ms():
    code = ''
    sols = []
    for r, k in enumerate([3, 5, 4]):
        y = 12.6 - r * 4.5
        code += zone(0.4, y - 1.8, 16.6, y + 1.8)
        xs = [1.8 + i * 2.0 for i in range(k)]
        for i, x in enumerate(xs):
            code += P('ballon', x, y, 1.6, c=['matRouge', 'matBleu', 'matJaune'][i % 3])
        code += cadre_pointille(1.8 + k * 2.0 - 0.9, y - 1.2, 1.8 + k * 2.0 + 0.9, y + 1.2)
        sols.append(P('ballon', 1.8 + k * 2.0, y, 1.6, c='otGreen'))
        sols.append(texte(15.6, y, f'{k} et 1, {k + 1}', 12, 'otGreenDark', r'\otSemi', 'east'))
    fig = figure(code, sol(*sols), hauteur=14.8)
    return A('Un ballon de plus', 'Dessine <b>un ballon de plus</b> dans la case vide. Dis combien il y en avait et combien il y en a maintenant.', ['dessiner', 'dire'],
             'Réaliser une collection qui a un objet de plus et nommer le nombre avant et après l’ajout.', 'R2', fig,
             'Faire une tour de trois cubes, en ajouter un et dire « trois, et encore un, quatre ».',
             '« Il y avait trois ballons, j’en dessine un de plus : il y en a quatre. »',
             'Trois et un, quatre ; cinq et un, six ; quatre et un, cinq. Quand on ajoute un, on dit le nombre suivant.',
             quantites=[3, 4, 5, 6])

def a_colorie_chiffre():
    code = ''
    sols = []
    for r, n in enumerate([4, 6, 2, 5]):
        y = 13.4 - r * 3.9
        code += chiffre(1.4, y, n, 58)
        for k in range(6):
            x = 4.0 + k * 2.15
            code += rf'\draw[mat contour,fill=white,rounded corners=4pt] ({f(x - 0.85)},{f(y - 0.85)}) rectangle ({f(x + 0.85)},{f(y + 0.85)});'
            if k < n:
                sols.append(rf'\fill[otGreen,rounded corners=3pt] ({f(x - 0.72)},{f(y - 0.72)}) rectangle ({f(x + 0.72)},{f(y + 0.72)});')
    fig = figure(code, sol(*sols), hauteur=15.0)
    return A('Autant que le chiffre', 'Colorie <b>autant</b> de cases que le chiffre écrit au début de la ligne.', ['colorier'],
             'Passer de l’écriture chiffrée d’un nombre à la quantité.', 'R8', fig,
             'Tirer une carte chiffrée, la lire avec l’adulte, puis prendre autant de cubes.',
             '« C’est un quatre : je colorie quatre cases. »',
             'Quatre, six, deux et cinq cases coloriées, à partir de la gauche ou dans n’importe quel ordre.', quantites=[2, 4, 5, 6])

def a_parcours_fleurs():
    rnd = random.Random(91)
    pts = positions(10, 'vrac', 8.5, 6.6, 15.4, 11.2, d=2.4, graine=91)
    code = P('papillon', 1.4, 13.4, 2.2, c='matJaune')
    for i, (x, y) in enumerate(pts):
        code += P('fleur', x, y, 1.9, c=COULEURS[i % len(COULEURS)])
    # Chemin du plus proche voisin, depuis le papillon : une solution possible.
    reste = list(pts)
    cour = (1.4, 13.4)
    chemin = [cour]
    while reste:
        prochain = min(reste, key=lambda p: hypot(p[0] - cour[0], p[1] - cour[1]))
        reste.remove(prochain)
        chemin.append(prochain)
        cour = prochain
    fig = figure(code, sol(chemin_sol(chemin)), hauteur=14.6)
    return A('Le papillon butine', 'Trace le chemin du papillon : il doit passer sur <b>chaque fleur une seule fois</b>, sans en oublier.', ['tracer'],
             'Parcourir une collection en passant une et une seule fois par chaque élément.', 'R3', fig,
             'Poser un jeton dans chaque boîte d’allumettes fermée, sans en oublier ni en mettre deux, en déplaçant les boîtes déjà servies.',
             '« Celle-là, je l’ai déjà visitée. Il me reste celle-ci. »',
             'Il y a dix fleurs. Beaucoup de chemins sont justes : chacun doit toucher toutes les fleurs, une seule fois.',
             controles=[(len(chemin) == 11, 'chemin passant par les dix fleurs')])

# ------------------------------------------------------------------ partie 3 : composer, écrire, réciter
def a_deux_mains_ms():
    code = ''
    sols = []
    lignes_ = [(3, 2, [4, 5, 6]), (4, 2, [5, 6, 4]), (1, 4, [6, 5, 4]), (3, 3, [5, 6, 4])]
    for r, (a, b, choix) in enumerate(lignes_):
        y = 13.3 - r * 3.9
        code += zone(0.3, y - 1.75, 7.6, y + 1.75) + P('main', 2.1, y, 2.6, n=a) + P('main', 5.8, y, 2.6, n=b)
        for k, v in enumerate(choix):
            x = 9.6 + k * 2.7
            code += chiffre(x, y, v, 50)
            if v == a + b:
                sols.append(entoure_sol(x, y, 1.0, 1.2))
    fig = figure(code, sol(*sols), hauteur=15.2)
    return A('Les doigts des deux mains', 'Combien de doigts sont levés en tout ? Entoure le <b>bon chiffre</b>.', ['entourer', 'dire'],
             'Composer des nombres jusqu’à six avec les doigts des deux mains.', 'R7', fig,
             'Montrer trois doigts sur une main et deux sur l’autre : combien en tout ? Recommencer avec d’autres façons.',
             '« Trois et deux, ça fait cinq. Quatre et deux, ça fait six. »',
             'Cinq, six, cinq et six. Remarquer que trois et deux font cinq, comme quatre et un.', quantites=[1, 2, 3, 4, 5, 6])

def a_colliers_cinq():
    code = ''
    sols = []
    choix = [1, 2, 3, 4]
    for r, k in enumerate(choix):
        y = 13.0 - r * 3.7
        code += rf'\draw[matTrait,line width=1.3pt] (1.0,{f(y)}) .. controls (5.0,{f(y - 1.4)}) and (12.0,{f(y - 1.4)}) .. (16.0,{f(y)});'
        for i in range(5):
            t = (i + 1) / 6
            x = (1 - t) ** 3 * 1.0 + 3 * (1 - t) ** 2 * t * 5.0 + 3 * (1 - t) * t ** 2 * 12.0 + t ** 3 * 16.0
            yy = (1 - t) ** 3 * y + 3 * (1 - t) ** 2 * t * (y - 1.4) + 3 * (1 - t) * t ** 2 * (y - 1.4) + t ** 3 * y
            code += P('perle', x, yy, 2.6, c='white')
            sols.append(P('perle', x, yy, 2.6, c='matRouge' if i < k else 'matBleu'))
    fig = figure(code, sol(*sols), hauteur=14.2)
    return A('Cinq perles, deux couleurs', 'Colorie chaque collier en rouge et en bleu. Fais <b>chaque fois</b> un collier différent.', ['colorier', 'dire'],
             'Décomposer cinq de plusieurs façons : un et quatre, deux et trois…', 'R7', fig,
             'Faire des tours de cinq cubes avec deux couleurs et comparer toutes les tours obtenues.',
             '« Mon collier a deux perles rouges et trois bleues : cinq, c’est deux et trois. »',
             'Par exemple : un rouge et quatre bleus, deux et trois, trois et deux, quatre et un. L’ordre des perles peut varier.',
             quantites=[1, 2, 3, 4, 5])

def ligne_trace(y, n):
    code = chiffre_trace(1.6, y, n, 70, modele=True)
    code += rf'\draw[otRule,line width=1pt] (3.2,{f(y - 1.5)}) -- (16.6,{f(y - 1.5)});'
    for k in range(4):
        code += chiffre_trace(4.6 + k * 2.6, y, n, 70)
    code += cadre_pointille(14.6, y - 1.4, 16.6, y + 1.4)
    return code

def a_ecrire(chiffres_, titre):
    def fabrique():
        code = ''
        sols = []
        for r, n in enumerate(chiffres_):
            y = 12.6 - r * 4.6
            code += ligne_trace(y, n)
            sols.append(texte(15.6, y, str(n), 54, 'otGreenDark', r'\otMedium'))
        fig = figure(code, sol(*sols), hauteur=14.4)
        return A(titre, 'Repasse sur les chiffres gris avec ton doigt, puis avec un crayon. Écris le chiffre <b>tout seul</b> dans la dernière case.',
                 ['tracer'], 'Écrire en chiffres les nombres de un à six.', 'R9', fig,
                 'Tracer le chiffre en grand dans l’air, sur le dos de l’enfant, dans le sable ou sur l’ardoise, en partant du haut.',
                 '« Je pars du haut, comme le modèle bleu. »',
                 'Les chiffres sont tracés en partant du haut, sans lever le crayon (sauf pour le 4 et le 5). La forme compte plus que la taille.',
                 quantites=chiffres_)
    return fabrique

def a_ecrire_quantite():
    code = ''
    sols = []
    for r, (nom, n, c) in enumerate([('canard', 2, 'matJaune'), ('etoile', 5, 'matOrange'), ('poisson', 3, 'matBleu'), ('coccinelle', 6, 'matRouge')]):
        y = 13.3 - r * 3.9
        code += zone(0.3, y - 1.6, 11.6, y + 1.6)
        cc, _ = collection(nom, n, 'ligne', 5.95, y, 10.8, 2.8, s=1.5, couleurs=[c])
        code += cc + rf'\draw[mat contour,fill=white,rounded corners=5pt] (13.2,{f(y - 1.5)}) rectangle (16.4,{f(y + 1.5)});'
        sols.append(texte(14.8, y, str(n), 50, 'otGreenDark', r'\otMedium'))
    fig = figure(code, sol(*sols), hauteur=15.2)
    return A('J’écris combien', 'Compte les animaux ou les étoiles. <b>Écris le chiffre</b> dans la case.', ['dessiner'],
             'Représenter une quantité par son écriture chiffrée.', 'R9', fig,
             'Jeu du facteur : compter des jetons et écrire le nombre sur une étiquette pour un camarade qui doit en apporter autant.',
             '« Il y a deux canards : j’écris le chiffre deux. »',
             'Les chiffres 2, 5, 3 et 6.', quantites=[2, 3, 5, 6])

def a_comptine12():
    code = rf'\fill[matCiel!60,rounded corners=12pt] (0.3,0.3) rectangle (16.7,13.4);'
    code += rf'\fill[matVert!35,rounded corners=12pt] (0.3,8.6) rectangle (2.2,13.4) (14.8,0.3) rectangle (16.7,5.2);'
    for y in (12.4, 8.6, 5.0, 1.4):
        code += rf'\draw[matBleu!45,line width=1pt] (4.0,{f(y)}) .. controls (7.0,{f(y + 0.3)}) .. (10.0,{f(y)});'
    # Chemin en zigzag : trois rangées de quatre pierres, sans chevauchement.
    pts = []
    for r, y in enumerate((10.6, 6.8, 3.0)):
        xs = [3.6, 7.0, 10.4, 13.6]
        pts += [(x, y + (0.25 if i % 2 else 0)) for i, x in enumerate(xs if r % 2 == 0 else xs[::-1])]
    for x, y in pts:
        code += P('pierre', x, y, 2.4)
    code += P('lapin', 1.25, 11.0, 2.0, c='matGris') + P('carotte', 15.75, 2.9, 2.2)
    sols = [texte(x, y, str(i + 1), 13, 'otGreenDark', r'\otBold') for i, (x, y) in enumerate(pts)]
    sols.append(rf'\draw[sol entoure] ({f(pts[-1][0])},{f(pts[-1][1])}) ellipse (1.5 and 1.0);')
    fig = figure(code, sol(*sols), hauteur=13.7)
    return A('Les pierres de la rivière', 'Fais sauter le lapin de pierre en pierre avec ton doigt en disant : un, deux, trois… Entoure la dernière pierre : c’est la <b>douzième</b>.',
             ['dire', 'entourer'], 'Réciter la comptine numérique de un à douze, de façon ordonnée, un mot par pierre.', 'R10', fig,
             'Réciter la comptine en sautant de cerceau en cerceau, en tapant dans les mains, en montant un escalier.',
             '« Un, deux, trois… dix, onze, douze ! Le lapin a traversé. »',
             'Douze pierres : un mot-nombre par saut, sans en oublier. La dernière pierre, près de la carotte, est la douzième.',
             controles=[(len(pts) == 12, 'comptine jusqu’à douze')])

# ------------------------------------------------------------------ partie 4 : rang, bande numérique, jeu de l’oie
def a_file_animaux():
    code = rf'\draw[matBrun!30,line width=36pt,line cap=round] (3.2,6.0) -- (14.0,6.0);'
    code += rf'\draw[mat contour,fill=matCiel] (1.3,6.0) ellipse (1.3 and 0.9);' + texte(1.3, 4.3, 'la mare', 11, 'otMuted', r'\otMedium')
    code += P('arbre', 16.0, 7.1, 3.4) + texte(16.0, 4.3, 'l’arbre', 11, 'otMuted', r'\otMedium')
    anim = [('canard', 'matJaune'), ('lapin', 'matGris'), ('chat', 'matOrange'), ('ours', 'matBrun'), ('souris', None), ('escargot', None)]
    xs = [3.5 + i * 1.95 for i in range(6)]
    for (nom, c), x in zip(anim, xs):
        code += P(nom, x, 6.2, 1.9, c=c)
    sols = [entoure_sol(xs[1], 6.2, 1.1, 1.15),
            rf'\draw[sol trait] ({f(xs[4] - 0.8)},5.4) -- ({f(xs[4] + 0.8)},7.0) ({f(xs[4] - 0.8)},7.0) -- ({f(xs[4] + 0.8)},5.4);']
    fig = figure(code, sol(*sols), hauteur=9.4)
    return A('En partant de la mare', 'En partant de la mare, entoure le <b>deuxième</b> animal. Fais une croix sur le <b>cinquième</b>.', ['entourer', 'barrer'],
             'Repérer le rang d’un objet dans une file en comptant, à partir d’un point de départ donné.', 'R11', fig,
             'Faire une file d’enfants ou de peluches : « Qui est le premier ? Le deuxième ? Va te mettre en cinquième place. »',
             '« Je pars de la mare : premier le canard, deuxième le lapin… »',
             'Le lapin est le deuxième ; la souris est la cinquième. En partant de l’arbre, les rangs changent : la souris serait la deuxième.')

def a_wagons_rang():
    code = P('locomotive', 1.7, 8.0, 2.6, c='otNavy!70')
    xs = [4.6 + i * 2.1 for i in range(6)]
    sols = []
    couleurs = {0: 'matRouge', 2: 'matBleu', 5: 'matVert'}
    for i, x in enumerate(xs):
        code += P('wagon', x, 7.88, 2.2, c='white')
        if i in couleurs:
            sols.append(P('wagon', x, 7.88, 2.2, c=couleurs[i]))
    code += texte(8.5, 3.6, '1\\textsuperscript{er} wagon en rouge · 3\\textsuperscript{e} en bleu · 6\\textsuperscript{e} en vert', 13, 'otMuted', r'\otMedium')
    for x, c in [(3.0, 'matRouge'), (8.5, 'matBleu'), (14.0, 'matVert')]:
        code += rf'\fill[{c}] ({f(x)},2.2) circle (0.35);'
    fig = figure(code, sol(*sols), hauteur=10.0)
    return A('Le train des rangs', 'Colorie le <b>premier</b> wagon en rouge, le <b>troisième</b> en bleu et le <b>sixième</b> en vert. On compte à partir de la locomotive.',
             ['colorier'], 'Repérer un rang jusqu’au sixième dans une suite ordonnée.', 'R11', fig,
             'Aligner six chaises derrière une « locomotive » ; demander aux enfants de s’asseoir sur la première, la troisième, la sixième.',
             '« Le premier wagon est collé à la locomotive. Un, deux, trois : voilà le troisième. »',
             'Le wagon juste derrière la locomotive en rouge, le troisième en bleu, le dernier (sixième) en vert.')

def a_perle_rouge():
    code = ''
    sols = []
    positions_ = [4, 3, 1, 5]
    for r, p in enumerate(positions_):
        y = 13.0 - r * 3.7
        code += rf'\draw[matTrait,line width=1.4pt] (1.4,{f(y)}) -- (15.6,{f(y)});'
        code += rf'\fill[matBrun] (1.2,{f(y)}) circle (0.32);' + texte(1.2, y - 0.85, 'nœud', 9, 'otMuted', r'\otMedium')
        for i in range(6):
            code += P('perle', 3.4 + i * 2.15, y, 2.4, c='matRouge' if i + 1 == p else 'matBleu')
        if p == 3:
            sols.append(entoure_sol(8.7, y, 8.0, 1.25))
    fig = figure(code, sol(*sols), hauteur=14.6)
    return A('La perle rouge', 'En partant du nœud, entoure le fil où la perle rouge est la <b>troisième</b>.', ['entourer'],
             'Repérer le rang d’un élément en comptant à partir d’un point de départ.', 'R11', fig,
             'Enfiler cinq perles bleues et une rouge ; un enfant décrit la place de la rouge à un camarade qui doit refaire le même collier.',
             '« Je pars du nœud : un, deux, trois. La perle rouge est la troisième. »',
             'Le deuxième fil. Sur les autres, la perle rouge est la quatrième, la première et la cinquième.')

def a_bande_lacunaire():
    code = ''
    sols = []
    for r, vides in enumerate([(2, 5), (3, 4, 6), (1, 4, 5)]):
        y = 12.6 - r * 4.6
        c, centres = bande(1.3, y, [1, 2, 3, 4, 5, 6], w=2.4, h=2.4, taille=34, vides=vides)
        code += c
        for v in vides:
            sols.append(texte(centres[v - 1][0], y, str(v), 34, 'otGreenDark', r'\otBold'))
    fig = figure(code, sol(*sols), hauteur=14.6)
    return A('La bande des nombres', 'Écris les nombres qui <b>manquent</b> dans chaque bande.', ['dessiner'],
             'Compléter une bande numérique lacunaire jusqu’à six.', 'R13', fig,
             'Construire avec la classe une bande de boîtes : une boîte par nombre, de un à six, avec la quantité et le chiffre.',
             '« Après un, il y a deux. Avant six, il y a cinq. »',
             'Première bande : 2 et 5. Deuxième : 3, 4 et 6. Troisième : 1, 4 et 5.', quantites=[1, 2, 3, 4, 5, 6])

def a_bande_place():
    c, centres = bande(1.3, 12.0, [1, 2, 3, 4, 5, 6], w=2.4, h=2.4, taille=34)
    code = c
    cartes = [('de', 4), ('main', 2), ('points', 6), ('de', 3), ('main', 5), ('points', 1)]
    xs = [1.9 + i * 2.65 for i in range(6)]
    sols = []
    for (kind, n), x in zip(cartes, xs):
        y = 4.0
        if kind == 'de':
            code += P('de', x, y, 2.2, n=n)
        elif kind == 'main':
            code += P('main', x, y, 2.3, n=n)
        else:
            code += carte_points(x, y, n, w=2.2, h=2.2)
        code += point(x, y + 1.75)
        sols.append(trait_sol((x, y + 1.75), (centres[n - 1][0], 10.6)))
    for cx, cy in centres:
        code += point(cx, 10.6)
    fig = figure(code, sol(*sols), hauteur=13.4)
    return A('Chaque carte à sa place', 'Relie chaque carte à la case de la bande qui a le <b>même nombre</b>.', ['relier'],
             'Placer des représentations des nombres (dé, doigts, points) sur la bande numérique.', 'R13', fig,
             'Distribuer des cartes (dés, doigts, chiffres) ; chaque enfant pose la sienne sur la bonne case d’une grande bande au sol.',
             '« Quatre points : je vais à la case du 4. »',
             'Le dé quatre va au 4, les deux doigts au 2, la carte à six points au 6, le dé trois au 3, la main ouverte au 5, le point seul au 1.',
             quantites=[1, 2, 3, 4, 5, 6])

def ligne_oie(y, depart, pas_, recule=False, n=8):
    code, centres = piste(3.6, y, n, w=1.65, h=1.65)
    code += P('de', 1.4, y, 2.0, n=pas_)
    if recule:
        code += rf'\draw[matRouge,line width=2.6pt,-{{Stealth[length=3mm]}}] (2.4,{f(y + 1.35)}) -- (0.4,{f(y + 1.35)});'
    else:
        code += rf'\draw[otGreen,line width=2.6pt,-{{Stealth[length=3mm]}}] (0.4,{f(y + 1.35)}) -- (2.4,{f(y + 1.35)});'
    x, yy = centres[depart - 1]
    code += P('pion', x, yy + 0.1, 1.7, c='matRouge')
    arrivee = depart - pas_ if recule else depart + pas_
    ax, ay = centres[arrivee - 1]
    sol_ = rf'\fill[otGreen,opacity=.55,rounded corners=3pt] ({f(ax - 0.72)},{f(ay - 0.75)}) rectangle ({f(ax + 0.72)},{f(ay + 0.75)});'
    return code, sol_, arrivee

def a_oie_avance():
    code = ''
    sols = []
    for r, (dep, pas_) in enumerate([(2, 2), (4, 1), (3, 2)]):
        y = 11.6 - r * 4.4
        c, s_, _ = ligne_oie(y, dep, pas_)
        code += c
        sols.append(s_)
    fig = figure(code, sol(*sols), hauteur=13.4)
    return A('Le jeu de l’oie', 'Le pion avance d’autant de cases que de points sur le dé. Colorie la case où il <b>arrive</b>.', ['colorier'],
             'Trouver la position d’arrivée après un avancement d’une ou deux cases.', 'R12', fig,
             'Jouer au jeu de l’oie avec un dé à un ou deux points ; avancer le pion en comptant chaque case à voix haute.',
             '« Je suis ici. Le dé fait deux : un, deux. J’arrive là. »',
             'Le pion arrive deux cases plus loin, puis une case plus loin, puis deux cases plus loin. On ne compte pas la case de départ.')

def a_oie_recule():
    code = ''
    sols = []
    for r, (dep, pas_) in enumerate([(5, 1), (6, 2), (4, 2)]):
        y = 11.6 - r * 4.4
        c, s_, _ = ligne_oie(y, dep, pas_, recule=True)
        code += c
        sols.append(s_)
    fig = figure(code, sol(*sols), hauteur=13.4)
    return A('On recule !', 'Attention : la flèche rouge veut dire <b>reculer</b>. Colorie la case où le pion arrive.', ['colorier'],
             'Trouver la position d’arrivée après un recul d’une ou deux cases.', 'R12', fig,
             'Au jeu de l’oie, ajouter des cases « recule d’une case » ou « recule de deux cases ».',
             '« Je recule de deux : un, deux. Je suis revenu là. »',
             'Le pion recule d’une case, puis de deux, puis de deux.')

# ------------------------------------------------------------------ partie 5 : problèmes
def a_fraises():
    code = ''
    xs = [2.6 + i * 3.0 for i in range(5)]
    for x in xs:
        code += P('fraise', x, 10.6, 2.3, c='matRouge')
    for k, v in enumerate([2, 3, 4]):
        code += P('de', 4.0 + k * 4.5, 3.2, 2.6, n=v)
    sols = [rf'\draw[sol trait] ({f(x - 1.0)},9.5) -- ({f(x + 1.0)},11.7) ({f(x - 1.0)},11.7) -- ({f(x + 1.0)},9.5);' for x in xs[3:]]
    sols.append(entoure_sol(8.5, 3.2, 1.7, 1.7))
    fig = figure(code, sol(*sols), hauteur=12.4)
    return A('Les fraises de Lilou', 'Lilou avait cinq fraises. Elle en a mangé deux. <b>Barre</b> les fraises mangées, puis entoure le dé qui montre combien il en reste.',
             ['barrer', 'entourer'], 'Résoudre un problème de retrait en représentant l’action.', 'R14', fig,
             'Jouer la scène avec cinq jetons : en enlever deux, puis compter ce qui reste.',
             '« Il y avait cinq fraises, elle en a mangé deux : il en reste trois. Cinq, c’est deux et trois. »',
             'Deux fraises barrées (n’importe lesquelles) ; il en reste trois : le dé à trois points.', quantites=[5, 2, 3])

def a_chapeau():
    code = carte_points(2.4, 11.2, 6, w=3.2, h=3.2) + texte(2.4, 8.9, 'en tout', 12, 'otMuted', r'\otMedium')
    xs = [6.0, 8.0, 10.0, 12.0]
    for x in xs:
        code += P('lapin', x, 11.0, 2.0, c='matGris')
    code += P('chapeau', 14.9, 11.1, 3.6, c='otNavy')
    code += texte(8.5, 7.0, 'Combien de lapins sont cachés sous le chapeau ?', 13, 'otMuted', r'\otMedium')
    code += cadre_pointille(4.5, 1.0, 12.5, 5.6)
    c, _ = collection('jeton', 2, 'ligne', 8.5, 3.3, 7.0, 3.0, s=1.6, couleurs=['otGreen'])
    fig = figure(code, sol(c), hauteur=13.2)
    return A('Le chapeau du magicien', 'Il y a six lapins en tout. Certains sont cachés sous le chapeau. <b>Dessine</b> dans la boîte autant de ronds que de lapins cachés.',
             ['dessiner'], 'Trouver une partie quand on connaît le tout et l’autre partie.', 'R14', fig,
             'Compter six jetons, puis en cacher sous un gobelet pendant que l’enfant ferme les yeux : combien sont cachés ?',
             '« Il y en a six en tout. J’en vois quatre : cinq, six… il en manque deux. »',
             'Deux lapins sont cachés : six, c’est quatre et deux.', quantites=[6, 4, 2])

def a_billes_boite():
    code = P('boite', 4.0, 9.6, 5.2, c='matVert')
    for x in (2.9, 4.0, 5.1):
        code += P('perle', x, 9.4, 1.8, c='matBleu')
    code += P('perle', 10.6, 12.0, 1.8, c='matRouge') + P('perle', 12.1, 12.0, 1.8, c='matRouge')
    code += fleche((9.6, 11.5), (7.0, 10.4), 'otMuted', 2.5) + texte(11.4, 10.4, 'encore deux', 13, 'otMuted', r'\otMedium')
    sols = []
    for k, v in enumerate([4, 5, 6]):
        x = 4.0 + k * 4.5
        code += chiffre(x, 3.2, v, 60)
        if v == 5:
            sols.append(entoure_sol(x, 3.2, 1.3, 1.5))
    fig = figure(code, sol(*sols), hauteur=13.0)
    return A('Les billes dans la boîte', 'Il y a trois billes dans la boîte. On en met encore deux. Combien y a-t-il de billes dans la boîte ? <b>Entoure</b> le bon chiffre.',
             ['entourer'], 'Résoudre un problème d’ajout : trouver le tout.', 'R14', fig,
             'Mettre trois billes dans une boîte opaque, en ajouter deux devant l’enfant et demander combien il y en a sans ouvrir.',
             '« Trois dans ma tête, et encore deux : quatre, cinq. Il y en a cinq. »',
             'Cinq billes : on peut surcompter à partir de trois (« quatre, cinq ») ou compter sur ses doigts.', quantites=[3, 2, 5])

def a_cache_main():
    code = ''
    sols = []
    for r, (tout, vus) in enumerate([(5, 3), (6, 4), (4, 1)]):
        y = 12.3 - r * 4.6
        code += P('de', 1.5, y, 2.2, n=tout) + texte(1.5, y - 1.55, 'en tout', 10, 'otMuted', r'\otMedium')
        xs = [3.6 + i * 1.3 for i in range(vus)]
        code += ''.join(P('jeton', x, y, 1.15, c='matRouge') for x in xs) + P('main', xs[-1] + 2.0, y, 2.6, n=5, rot=-90)
        code += cadre_pointille(11.2, y - 1.5, 16.6, y + 1.5)
        cs, _ = collection('jeton', tout - vus, 'ligne', 13.9, y, 5.0, 2.4, s=1.2, couleurs=['otGreen'])
        sols.append(cs)
    fig = figure(code, sol(*sols), hauteur=14.2)
    return A('Sous la main', 'Le dé dit combien de jetons il y a en tout. Combien sont cachés sous la main ? <b>Dessine-les</b> dans la boîte.',
             ['dessiner'], 'Rechercher une partie dans un problème de parties-tout.', 'R14', fig,
             'Jeu du cache : poser cinq jetons, en cacher sous sa main, l’enfant trouve combien sont cachés, puis on vérifie.',
             '« Il y en a cinq en tout. J’en vois trois : il en manque deux. »',
             'Deux jetons cachés, puis deux, puis trois.', quantites=[5, 3, 2, 6, 4, 1])

def a_boites_crayons():
    code = ''
    xs = [3.0, 8.5, 14.0]
    for x in xs:
        # Les crayons partent du fond de la boîte : la face avant, dessinée après, cache leur bas.
        for k, c in enumerate(['matRouge', 'matJaune']):
            code += P('crayon', x - 0.5 + k * 1.0, 8.2, 1.0, c=c, l=3.6, rot=90)
        code += P('boite', x, 9.0, 4.0, c='matBleu')
    sols = []
    for k, v in enumerate([4, 5, 6]):
        x = 4.0 + k * 4.5
        code += P('de', x, 3.0, 2.6, n=v)
        if v == 6:
            sols.append(entoure_sol(x, 3.0, 1.7, 1.7))
    fig = figure(code, sol(*sols), hauteur=12.8)
    return A('Les boîtes de crayons', 'Il y a deux crayons dans chaque boîte. Combien de crayons y a-t-il <b>en tout</b> ? Entoure le bon dé.',
             ['entourer'], 'Rechercher le tout dans un problème de groupements.', 'R15', fig,
             'Montrer trois boîtes opaques contenant chacune deux crayons, l’une après l’autre ; demander combien il y a de crayons en tout.',
             '« Deux, et deux, et encore deux : six crayons. »',
             'Six crayons : le dé à six points.', quantites=[2, 6])

def a_partage_gateaux():
    code = ''
    for i in range(6):
        code += P('gateau', 3.2 + i * 2.1, 12.0, 1.8, c=['matRose', 'matJaune', 'matBleu'][i % 3])
    sols = []
    for x, c in [(4.5, 'matBrun'), (12.5, 'matJaune')]:
        code += P('ours', x, 6.8, 2.8, c=c) + P('assiette', x, 3.0, 6.4)
        for k in range(3):
            sols.append(P('gateau', x - 1.6 + k * 1.6, 3.6, 1.3, c='otGreen'))
    fig = figure(code, sol(*sols), hauteur=13.2)
    return A('Le partage des gâteaux', 'Partage les six gâteaux entre les deux ours : chacun doit en avoir <b>autant</b>. Dessine les gâteaux dans les assiettes.',
             ['dessiner'], 'Trouver la valeur d’une part dans un partage équitable, en distribuant un à un.', 'R15', fig,
             'Distribuer six jetons à deux poupées : « un pour toi, un pour toi », jusqu’à ce qu’il n’en reste plus.',
             '« Un pour toi, un pour toi… Chaque ours a trois gâteaux. »',
             'Trois gâteaux dans chaque assiette.', quantites=[6, 3])

def a_partage_carottes():
    code = ''
    for i in range(6):
        code += P('carotte', 2.6 + i * 2.35, 12.0, 2.0)
    sols = []
    for x, c in [(3.0, 'matGris'), (8.5, 'matJaune'), (14.0, 'matRouge')]:
        code += P('lapin', x, 6.6, 2.6, c=c) + cadre_pointille(x - 2.3, 1.0, x + 2.3, 4.2)
        for k in range(2):
            sols.append(P('carotte', x - 0.8 + k * 1.6, 2.6, 1.6))
    fig = figure(code, sol(*sols), hauteur=13.2)
    return A('Une part pour chaque lapin', 'Partage les six carottes entre les trois lapins : chacun doit en avoir <b>autant</b>. Dessine-les dans les cases.',
             ['dessiner'], 'Partager équitablement une collection en distribuant un à un.', 'R15', fig,
             'Distribuer six cubes à trois peluches, un par un, en faisant le tour, jusqu’à ce qu’il n’en reste plus.',
             '« Un pour chacun, puis encore un pour chacun : chaque lapin a deux carottes. »',
             'Deux carottes pour chaque lapin.', quantites=[6, 2])

# ------------------------------------------------------------------ partie 6 : formes et solides
def a_trois_formes():
    rnd = random.Random(101)
    formes_ = ['triangle'] * 4 + ['carre'] * 4 + ['disque'] * 4
    rnd.shuffle(formes_)
    code = ''
    sols = []
    coul = {'triangle': 'matBleu', 'carre': 'matRouge', 'disque': 'matJaune'}
    for i, k in enumerate(formes_):
        r, c = divmod(i, 4)
        x, y = 2.2 + c * 4.2, 12.4 - r * 4.4
        t = [0.95, 1.3, 1.1, 0.8][(i + r) % 4]
        a = rnd.choice([10, 25, 40, 70, 115, 160, 200])
        code += forme(k, x, y, t, angle=a, couleur='white')
        sols.append(forme(k, x, y, t, angle=a, couleur=coul[k]))
    code += rf'\fill[matBleu] (2.2,1.2) circle (0.3);' + texte(2.8, 1.2, 'triangles', 12, 'otMuted', r'\otMedium', 'west')
    code += rf'\fill[matRouge] (7.4,1.2) circle (0.3);' + texte(8.0, 1.2, 'carrés', 12, 'otMuted', r'\otMedium', 'west')
    code += rf'\fill[matJaune] (11.8,1.2) circle (0.3);' + texte(12.4, 1.2, 'disques', 12, 'otMuted', r'\otMedium', 'west')
    fig = figure(code, sol(*sols), hauteur=14.2)
    return A('Triangles, carrés, disques', 'Colorie les triangles en <b>bleu</b>, les carrés en <b>rouge</b> et les disques en <b>jaune</b>.', ['colorier'],
             'Reconnaître et classer triangles, carrés et disques, quelles que soient leur taille et leur orientation.', 'R17', fig,
             'Trier des formes en carton de toutes tailles et tournées dans tous les sens ; les toucher les yeux fermés.',
             '« Ce carré est penché, mais c’est toujours un carré : quatre côtés pareils. »',
             'Quatre triangles en bleu, quatre carrés en rouge, quatre disques en jaune. Les carrés penchés sont bien des carrés.', quantites=[4])

def a_intrus_formes():
    code = ''
    sols = []
    lignes_ = [('carre', 'triangle', 3), ('triangle', 'carre', 1), ('disque', 'carre', 4), ('carre', 'disque', 2)]
    rnd = random.Random(102)
    for r, (base, intrus, pos) in enumerate(lignes_):
        y = 13.2 - r * 3.9
        for i in range(5):
            x = 1.9 + i * 3.3
            k = intrus if i == pos else base
            code += forme(k, x, y, rnd.choice([0.8, 1.0, 1.15]), angle=rnd.choice([0, 20, 35, 50, 75]), couleur=COULEURS[(i + r) % 7])
            if i == pos:
                sols.append(rf'\draw[sol trait] ({f(x - 1.3)},{f(y - 1.3)}) -- ({f(x + 1.3)},{f(y + 1.3)}) ({f(x - 1.3)},{f(y + 1.3)}) -- ({f(x + 1.3)},{f(y - 1.3)});')
    fig = figure(code, sol(*sols), hauteur=14.8)
    return A('L’intrus', 'Dans chaque ligne, une forme n’est pas comme les autres. <b>Barre-la</b>.', ['barrer'],
             'Reconnaître une forme plane malgré sa couleur, sa taille et son orientation.', 'R17', fig,
             'Montrer quatre carrés tournés et un triangle ; demander lequel « n’est pas de la même famille ».',
             '« Ce sont tous des carrés, même tournés. Celui-là est un triangle : c’est l’intrus. »',
             'Le triangle de la première ligne, le carré de la deuxième, le carré de la troisième, le disque de la quatrième.')

def a_empreintes_cube():
    code = ''
    sols = []
    pieces = [('carre', 1.3, 15, True), ('rectangle', 1.1, 0, False), ('disque', 1.3, 0, False),
              ('carre', 1.3, 45, True), ('triangle', 1.4, 20, False), ('carre', 1.3, 0, True)]
    for i, (k, t, a, bon) in enumerate(pieces):
        r, c = divmod(i, 3)
        x, y = 3.0 + c * 5.5, 10.6 - r * 5.6
        code += forme(k, x, y, t, angle=a, couleur='matGris!35')
        if bon:
            sols.append(entoure_sol(x, y, 2.3, 2.3))
    fig = figure(code, sol(*sols), hauteur=13.0)
    return A('Les empreintes du cube', 'Avec un vrai cube et de la pâte à modeler, fais des empreintes. <b>Entoure</b> les empreintes que le cube peut laisser.',
             ['manipuler', 'entourer'], 'Produire les empreintes d’un solide et les reconnaître.', 'R16', fig,
             'Appuyer chaque face d’un cube dans la pâte à modeler ou la peinture : toutes les empreintes sont des carrés pareils.',
             '« Toutes les faces du cube laissent un carré. Le cube ne laisse pas de disque. »',
             'Les trois carrés, même tournés. Le rectangle, le disque et le triangle ne viennent pas d’un cube.')

def a_empreintes_pyramide():
    code = ''
    sols = []
    pieces = [('triangle_equi', 1.5, 10, True), ('disque', 1.2, 0, False), ('carre', 1.2, 0, True),
              ('triangle_equi', 1.5, 200, True), ('rectangle', 1.0, 30, False), ('triangle_equi', 1.5, 95, True)]
    for i, (k, t, a, bon) in enumerate(pieces):
        r, c = divmod(i, 3)
        x, y = 3.0 + c * 5.5, 10.6 - r * 5.6
        code += forme(k, x, y, t, angle=a, couleur='matGris!35')
        if bon:
            sols.append(entoure_sol(x, y, 2.3, 2.3))
    fig = figure(code, sol(*sols), hauteur=13.0)
    return A('Les empreintes de la pyramide', 'Avec une vraie pyramide, fais des empreintes. <b>Entoure</b> les empreintes que la pyramide peut laisser.',
             ['manipuler', 'entourer'], 'Produire les empreintes d’un solide et retrouver le solide à partir d’une empreinte.', 'R16', fig,
             'Faire des empreintes avec une pyramide à base carrée : le dessous laisse un carré, les côtés laissent des triangles.',
             '« La pyramide laisse un carré et des triangles. Le cube aussi laisse un carré : une même empreinte peut venir de deux solides. »',
             'Le carré et les trois triangles. Le disque (empreinte d’un cylindre) et le rectangle ne viennent pas de cette pyramide.')

def poly(pts, couleur, contour=True):
    return rf'\draw[{"mat contour," if contour else ""}fill={couleur}] ' + ' -- '.join(f'({f(x)},{f(y)})' for x, y in pts) + ' -- cycle;'

def fusee(x0, y0, s, couleurs):
    """Fusée en cinq formes : triangle (pointe), deux carrés (corps), deux triangles (ailerons)."""
    P_ = lambda pts: [(x0 + s * a, y0 + s * b) for a, b in pts]
    pieces = [P_([(0, 2), (1, 2), (0.5, 3)]), P_([(0, 1), (1, 1), (1, 2), (0, 2)]), P_([(0, 0), (1, 0), (1, 1), (0, 1)]),
              P_([(0, 0), (0, 1), (-0.6, 0)]), P_([(1, 0), (1, 1), (1.6, 0)])]
    return ''.join(poly(p, c) for p, c in zip(pieces, couleurs))

def a_fusee():
    modele = ['matRouge', 'matBleu', 'matJaune', 'matVert', 'matVert']
    code = texte(3.0, 13.4, 'le modèle', 12, 'otMuted', r'\otMedium') + fusee(1.9, 5.5, 2.2, modele)
    code += fusee(9.6, 1.0, 4.0, ['white'] * 5)
    sols = [fusee(9.6, 1.0, 4.0, modele)]
    fig = figure(code, sol(*sols), hauteur=13.9)
    return A('La fusée', 'Colorie la grande fusée comme le <b>modèle</b>.', ['colorier'],
             'Reproduire un assemblage de cinq formes à partir d’un modèle.', 'R18', fig,
             'Reproduire la fusée avec cinq formes en carton posées sur une feuille, puis la coller.',
             '« En haut, le triangle rouge. Dessous, le carré bleu, puis le carré jaune. Les ailes sont vertes. »',
             'Pointe rouge, carré du haut bleu, carré du bas jaune, ailerons verts.')

def pavage(x0, y0, s, couleurs):
    """Carré de côté 2 découpé en cinq pièces : deux grands triangles, un carré, deux petits triangles."""
    P_ = lambda pts: [(x0 + s * a, y0 + s * b) for a, b in pts]
    pieces = [P_([(0, 0), (2, 0), (1, 1)]), P_([(0, 0), (1, 1), (0, 2)]), P_([(2, 0), (2, 1), (1, 1)]),
              P_([(2, 1), (2, 2), (1, 2), (1, 1)]), P_([(0, 2), (1, 1), (1, 2)])]
    return ''.join(poly(p, c) for p, c in zip(pieces, couleurs))

def aire(pts):
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))) / 2

def a_pavage5():
    modele = ['matBleu', 'matJaune', 'matRouge', 'matVert', 'matOrange']
    code = texte(3.2, 13.4, 'le modèle', 12, 'otMuted', r'\otMedium') + pavage(0.8, 7.6, 2.4, modele)
    code += pavage(8.0, 1.0, 4.3, ['white'] * 5)
    fig = figure(code, sol(pavage(8.0, 1.0, 4.3, modele)), hauteur=13.9)
    return A('Le carré en cinq pièces', 'Colorie le grand carré comme le <b>modèle</b>. Regarde bien la place de chaque pièce.', ['colorier'],
             'Reproduire un pavage de cinq pièces à partir d’un modèle.', 'R18', fig,
             'Découper un carré en cinq pièces de carton ; mélanger les pièces et reconstituer le carré en regardant le modèle.',
             '« Le grand triangle bleu est en bas à gauche. Le carré rouge est en haut à droite. »',
             'Chaque pièce a la couleur de la pièce placée au même endroit sur le modèle.',
             controles=[(abs(sum(aire(p) for p in [[(0, 0), (2, 0), (1, 1)], [(0, 0), (1, 1), (0, 2)], [(2, 0), (2, 1), (1, 1)],
                                                    [(2, 1), (2, 2), (1, 2), (1, 1)], [(0, 2), (1, 1), (1, 2)]]) - 4) < 1e-9,
                         'les cinq pièces recouvrent exactement le carré')])

# ------------------------------------------------------------------ partie 7 : longueurs et masses
def a_trois_groupes():
    rnd = random.Random(111)
    longueurs = [2.0, 2.3, 1.8, 5.2, 5.6, 4.9, 9.8, 10.4, 9.4]
    rnd.shuffle(longueurs)
    code = ''
    sols = []
    for i, L in enumerate(longueurs):
        y = 14.0 - i * 1.55
        x = rnd.uniform(0.6, 16.4 - L)
        code += P('ruban', x, y, 2.0, c='white', l=L / 2.0)
        c = 'matJaune' if L < 3 else ('matVert' if L < 7 else 'matRouge')
        sols.append(P('ruban', x, y, 2.0, c=c, l=L / 2.0))
    code += rf'\fill[matJaune] (1.0,0.3) circle (0.3);' + texte(1.6, 0.3, 'courts', 12, 'otMuted', r'\otMedium', 'west')
    code += rf'\fill[matVert] (6.2,0.3) circle (0.3);' + texte(6.8, 0.3, 'moyens', 12, 'otMuted', r'\otMedium', 'west')
    code += rf'\fill[matRouge] (11.4,0.3) circle (0.3);' + texte(12.0, 0.3, 'longs', 12, 'otMuted', r'\otMedium', 'west')
    fig = figure(code, sol(*sols), hauteur=14.8)
    return A('Courts, moyens, longs', 'Colorie les rubans courts en <b>jaune</b>, les moyens en <b>vert</b> et les longs en <b>rouge</b>.', ['colorier'],
             'Classer des objets selon leur longueur en trois groupes, quand les longueurs sont très différentes.', 'R19', fig,
             'Ranger des bandes de papier ou des bâtons en trois tas : les courts, les moyens, les longs.',
             '« Ce ruban est long, celui-ci est court, celui-là est entre les deux. »',
             'Trois rubans jaunes (courts), trois verts (moyens), trois rouges (longs).',
             controles=[(len(longueurs) == 9, 'trois groupes de trois')])

def a_ordre_crayons():
    longs = [9.0, 12.6, 7.4, 10.8]
    cols = ['matBleu', 'matRouge', 'matVert', 'matJaune']
    code = rf'\draw[otMuted!60,line width=1pt] (1.2,1.0) -- (1.2,14.0);'
    sols = []
    ordre = sorted(range(4), key=lambda i: longs[i])
    for i, (L, c) in enumerate(zip(longs, cols)):
        y = 12.6 - i * 3.5
        code += P('crayon', 1.2, y, 2.0, c=c, l=L / 2.0)
        rang = ordre.index(i) + 1
        for k in range(rang):
            sols.append(rf'\fill[otGreenDark] ({f(1.2 + L + 0.8 + k * 0.6)},{f(y)}) circle (0.2);')
    fig = figure(code, sol(*sols), hauteur=14.4)
    return A('Du plus court au plus long', 'Dessine <b>un</b> point à côté du crayon le plus court, <b>deux</b> points à côté du suivant… et <b>quatre</b> points à côté du plus long.',
             ['dessiner'], 'Ranger des objets rectilignes du plus court au plus long et verbaliser le résultat.', 'R19', fig,
             'Ranger quatre bandes de papier de couleurs différentes du plus court au plus long, en les posant contre une règle.',
             '« Le vert est plus court que le bleu. Le rouge est le plus long. »',
             'Un point pour le vert, deux pour le bleu, trois pour le jaune, quatre pour le rouge.', quantites=[1, 2, 3, 4])

def a_meme_longueur_ms():
    code = ''
    sols = []
    groupes = [[(6.0, 'matRouge'), (8.4, 'matBleu'), (6.0, 'matVert')], [(9.0, 'matJaune'), (7.0, 'matViolet'), (9.0, 'matOrange')]]
    for g, rubans in enumerate(groupes):
        y0 = 13.0 - g * 6.6
        code += zone(0.3, y0 - 5.2, 16.7, y0 + 0.9)
        xs = [1.2, 3.4, 2.2] if g == 0 else [1.0, 1.0, 1.0]
        for i, ((L, c), x) in enumerate(zip(rubans, xs)):
            y = y0 - i * 1.9
            code += P('ruban', x, y, 3.0, c=c, l=L / 3.0)
            if L == rubans[0][0] and (i == 0 or i == 2):
                sols.append(entoure_sol(x + L / 2, y, L / 2 + 0.5, 0.6))
    fig = figure(code, sol(*sols), hauteur=14.2)
    return A('De même longueur', 'Dans chaque cadre, <b>entoure</b> les deux rubans qui ont la même longueur.', ['entourer'],
             'Comparer des longueurs et reconnaître deux objets de même longueur.', 'R19', fig,
             'Comparer deux ficelles en les plaçant côte à côte, bout contre bout, au même point de départ.',
             '« Ce ruban est de même longueur que celui-là. Le bleu est plus long. »',
             'Premier cadre : le rouge et le vert (le bleu est plus long). Deuxième cadre : le jaune et l’orange (le violet est plus court).')

def a_plus_lourd():
    code = ''
    sols = []
    paires = [(('plume', None, 2.2), ('boule', None, 2.0), 1), (('ballon', 'matRouge', 3.2), ('boule', None, 1.8), 1),
              (('pasteque', None, 2.6), ('cerise', None, 1.6), 0)]
    for r, ((n1, c1, s1), (n2, c2, s2), lourd) in enumerate(paires):
        y = 12.4 - r * 4.6
        code += zone(0.3, y - 2.0, 16.7, y + 2.0) + P(n1, 4.5, y, s1, c=c1) + P(n2, 12.5, y, s2, c=c2)
        x = 12.5 if lourd else 4.5
        sols.append(entoure_sol(x, y, 1.9, 1.75))
    fig = figure(code, sol(*sols), hauteur=14.6)
    return A('Le plus lourd', 'Dans chaque cadre, <b>entoure</b> l’objet le plus lourd. Avant, soupèse de vrais objets.', ['manipuler', 'entourer'],
             'Comparer les masses de deux objets très différents ; comprendre qu’un gros objet n’est pas forcément lourd.', 'R20', fig,
             'Soupeser une balle de tennis et une boule de pétanque, un sachet de coton et un sachet de sable de même taille.',
             '« Le ballon est plus gros, mais il est plus léger que la boule. La boule est plus lourde. »',
             'La boule (plus lourde que la plume), la boule (plus lourde que le grand ballon), la pastèque (plus lourde que la cerise).')

def objet_plateau(nom, s, c=None, dy=0.0):
    return lambda x, y: P(nom, x, y + dy, s, c=c)

def a_balances():
    code = ''
    sols = []
    cas = [(-1, ('pasteque', 1.4, None, 0.55), ('pomme', 1.2, 'matRouge', 0.6), 'g'),
           (1, ('plume', 1.3, None, 0.62), ('boule', 1.3, None, 0.55), 'd'),
           (1, ('fraise', 1.2, 'matRouge', 0.6), ('ours', 1.4, 'matBrun', 0.7), 'd'),
           (-1, ('valise', 1.5, 'matOrange', 0.62), ('ballon', 1.4, 'matBleu', 0.7), 'g')]
    for i, (n, (a, sa, ca, da), (b, sb, cb, db), lourd) in enumerate(cas):
        r, c = divmod(i, 2)
        x, y = 4.3 + c * 8.4, 9.0 - r * 7.0
        code += zone(x - 4.0, y - 2.6, x + 4.0, y + 4.2)
        code += sur_balance(x, y, 2.4, n, objet_plateau(a, sa, ca, da), objet_plateau(b, sb, cb, db))
        ang = radians(-8 * n)
        cx = x - 1.05 * 2.4 * cos(ang) if lourd == 'g' else x + 1.05 * 2.4 * cos(ang)
        cy = y + (-1 if lourd == 'g' else 1) * 1.05 * 2.4 * sin(ang) + 0.44 * 2.4 + 0.7
        sols.append(entoure_sol(cx, cy, 1.25, 1.1))
    fig = figure(code, sol(*sols), hauteur=15.4)
    return A('La balance', 'Le plateau le plus lourd descend. Sur chaque balance, <b>entoure</b> l’objet le plus lourd.', ['entourer'],
             'Utiliser une balance de Roberval pour comparer deux masses.', 'R20', fig,
             'Poser deux objets sur une vraie balance de Roberval et observer le plateau qui descend.',
             '« Ce plateau est descendu : la pastèque est plus lourde que la pomme. »',
             'La pastèque, la boule, l’ours et la valise : à chaque fois, l’objet du plateau qui est descendu.')

# ------------------------------------------------------------------ partie 8 : motifs
def symb(k, x, y, t=1.0, c=None):
    if k == 'E':
        return P('etoile', x, y, 1.9 * t, c=c or 'matJaune')
    if k == 'D':
        return forme('disque', x, y, 0.6 * t, couleur=c or 'matBleu')
    if k == 'C':
        return forme('carre', x, y, 0.58 * t, couleur=c or 'matRouge')
    if k == 'T':
        return forme('triangle_equi', x, y, 0.75 * t, couleur=c or 'otGreen')
    raise ValueError(k)

def a_prolonger():
    code = ''
    sols = []
    lignes_ = [list('EDEDED'), list('EDDEDD'), list('CCTCCT'), list('DTEDTE')]
    for r, seq in enumerate(lignes_):
        y = 13.4 - r * 3.9
        periode = {'EDEDED': 2, 'EDDEDD': 3, 'CCTCCT': 3, 'DTEDTE': 3}[''.join(seq)]
        for i, k in enumerate(seq):
            code += symb(k, 1.2 + i * 1.75, y)
        for j in range(3):
            x = 12.0 + j * 1.75
            code += cadre_pointille(x - 0.8, y - 0.8, x + 0.8, y + 0.8)
            sols.append(symb(seq[(6 + j) % periode], x, y, c=None))
    fig = figure(code, sol(*sols), hauteur=15.0)
    return A('Continue la rangée', 'Regarde comment chaque rangée est faite. <b>Dessine</b> les trois formes qui viennent après.', ['dessiner', 'dire'],
             'Prolonger un motif répétitif et dire la règle utilisée.', 'R21', fig,
             'Faire des rangées avec des objets de la classe (crayon, gomme, crayon, gomme…) ; l’enfant continue et explique.',
             '« Étoile, rond, rond, étoile, rond, rond : après, il y a une étoile. »',
             'Étoile, rond, étoile ; étoile, rond, rond ; carré, carré, triangle ; rond, triangle, étoile. D’autres réponses sont possibles si l’enfant explique sa règle.')

def a_intrus_motif():
    code = ''
    sols = []
    # L’intrus remplace un élément : une seule case ne suit pas la règle (pas d’ambiguïté sur la réponse).
    lignes_ = [('EDEDEEEDED', 5, 2), ('CTCTCTCCCT', 7, 2), ('DDEDDDDDED', 5, 3)]
    ecarts = [[i for i, k in enumerate(seq) if k != seq[i % p]] for seq, _, p in lignes_]
    for r, (seq, pos, _) in enumerate(lignes_):
        y = 12.4 - r * 4.4
        for i, k in enumerate(seq):
            code += symb(k, 1.0 + i * 1.66, y, 0.9)
        x = 1.0 + pos * 1.66
        sols.append(rf'\draw[sol trait] ({f(x - 0.8)},{f(y - 0.8)}) -- ({f(x + 0.8)},{f(y + 0.8)}) ({f(x - 0.8)},{f(y + 0.8)}) -- ({f(x + 0.8)},{f(y - 0.8)});')
    fig = figure(code, sol(*sols), hauteur=14.0)
    return A('L’intrus de la rangée', 'Dans chaque rangée, une forme n’est pas à sa place. <b>Barre-la</b>.', ['barrer'],
             'Reconnaître un motif répétitif à ses régularités et trouver l’élément qui ne respecte pas la règle.', 'R21', fig,
             'Faire un collier qui alterne deux couleurs en glissant une erreur ; l’enfant la trouve et la corrige.',
             '« Étoile, rond, étoile, rond… Là, il y a deux ronds de suite : c’est l’intrus. »',
             'Première rangée : la sixième forme (une étoile à la place d’un rond). Deuxième : la huitième (un carré à la place d’un triangle). Troisième : la sixième (un rond à la place d’une étoile).',
             controles=[(e == [pos], 'un seul intrus par rangée') for e, (_, pos, _) in zip(ecarts, lignes_)])

def a_quel_motif():
    code = ''
    sols = []
    lignes_ = [('DCDCDCDC', True), ('DDCDCCCD', False), ('EETEETEE', True), ('TEETTETE', False)]
    for r, (seq, ok) in enumerate(lignes_):
        y = 13.4 - r * 3.9
        code += zone(0.3, y - 1.4, 16.7, y + 1.4)
        for i, k in enumerate(seq):
            code += symb(k, 1.6 + i * 1.98, y, 1.0)
        if ok:
            sols.append(entoure_sol(8.5, y, 8.6, 1.75))
    fig = figure(code, sol(*sols), hauteur=15.0)
    return A('Ça se répète ?', 'Entoure les rangées où les formes <b>se répètent</b> toujours de la même façon.', ['entourer'],
             'Identifier parmi plusieurs rangées celles qui contiennent un motif répétitif.', 'R21', fig,
             'Écouter des rythmes frappés : certains se répètent (tap, tap, pause…), d’autres non.',
             '« Rond, carré, rond, carré : ça se répète. Dans l’autre, il n’y a pas de règle. »',
             'La première rangée (rond, carré) et la troisième (étoile, étoile, triangle).')

def tour(x, y, couleurs, s=1.6):
    code = ''
    for i, c in enumerate(couleurs):
        code += rf'\draw[mat contour,fill={c}] ({f(x - s)},{f(y + i * s * 0.62)}) rectangle ({f(x + s)},{f(y + (i + 1) * s * 0.62)});'
    return code

def a_memoire():
    motif = ['matBleu', 'matJaune', 'matJaune'] * 2
    code = texte(4.0, 9.9, 'le modèle', 12, 'otMuted', r'\otMedium') + texte(13.0, 9.9, 'de mémoire', 12, 'otMuted', r'\otMedium') + tour(4.0, 1.4, motif, 2.0)
    code += rf'\draw[otRule,line width=1pt,dash pattern=on 4pt off 3pt] (8.5,0.6) -- (8.5,10.4);'
    code += tour(13.0, 1.4, ['white'] * 6, 2.0)
    fig = figure(code, sol(tour(13.0, 1.4, motif, 2.0)), hauteur=15.0)
    return A('La tour de mémoire', 'Regarde bien la tour du modèle. <b>Cache-la</b> avec ta main, puis colorie l’autre tour de mémoire.', ['colorier'],
             'Mémoriser un motif répétitif simple pour le reproduire.', 'R21', fig,
             'Montrer une tour de briques (une bleue, deux jaunes…), la cacher, et la faire reconstruire de mémoire.',
             '« Une bleue, deux jaunes, une bleue, deux jaunes. »',
             'De bas en haut : bleu, jaune, jaune, bleu, jaune, jaune. Retenir « une bleue, deux jaunes » aide à mémoriser.')

def a_motif_manquant():
    code = ''
    sols = []
    seqs = [('EDDEDD?DE', 'E', ['E', 'D']), ('CTTCT?CTT', 'T', ['C', 'T']), ('DDE?DEDDE', 'D', ['E', 'D'])]
    for r, (seq, bon, choix) in enumerate(seqs):
        y = 13.0 - r * 4.6
        for i, k in enumerate(seq):
            x = 1.0 + i * 1.7
            if k == '?':
                code += rf'\draw[mat contour,fill=otNavy,rounded corners=4pt] ({f(x - 0.75)},{f(y - 0.75)}) rectangle ({f(x + 0.75)},{f(y + 0.75)});' + texte(x, y, '?', 22, 'white', r'\otBold')
            else:
                code += symb(k, x, y, 0.95)
        code += zone(1.2, y - 3.2, 16.5, y - 1.2, plein=True)
        for j, k in enumerate(choix):
            x = 5.5 + j * 6.0
            code += symb(k, x, y - 2.2, 0.9)
            if k == bon:
                sols.append(entoure_sol(x, y - 2.2, 1.1, 0.9))
    fig = figure(code, sol(*sols), hauteur=14.6)
    return A('Sous la carte', 'Quelle forme est cachée sous la carte bleue ? <b>Entoure-la</b> dans le cadre du dessous.', ['entourer'],
             'Compléter un motif répétitif en trouvant l’élément manquant.', 'R21', fig,
             'Retourner une carte dans une rangée qui se répète et faire deviner ce qu’elle cache.',
             '« Étoile, rond, rond, étoile, rond, rond, étoile : sous la carte, il y a une étoile. »',
             'Une étoile, puis un triangle, puis un rond.')

# ------------------------------------------------------------------ partie 9 : se repérer
def etagere(x0, y0, w, niveaux, h):
    code = rf'\draw[mat contour,fill=matBrun!25] ({f(x0)},{f(y0)}) rectangle ({f(x0 + w)},{f(y0 + niveaux * h)});'
    for k in range(niveaux + 1):
        code += rf'\draw[mat contour,fill=matBrun!70] ({f(x0 - 0.2)},{f(y0 + k * h - 0.18)}) rectangle ({f(x0 + w + 0.2)},{f(y0 + k * h + 0.1)});'
    return code

def a_entre():
    code = etagere(0.8, 1.0, 15.4, 2, 5.6)
    haut = [('chat', 'matOrange', 2.2), ('ballon', 'matRouge', 2.0), ('lapin', 'matGris', 2.2), ('voiture', 'matBleu', 2.4)]
    bas = [('ours', 'matBrun', 2.4), ('bateau', 'matJaune', 2.4), ('canard', 'matJaune', 2.2), ('ballon', 'matVert', 2.0)]
    for i, (nom, c, s) in enumerate(haut):
        code += P(nom, 2.8 + i * 3.8, 7.85, s, c=c)
    for i, (nom, c, s) in enumerate(bas):
        code += P(nom, 2.8 + i * 3.8, 2.25, s, c=c)
    sols = [entoure_sol(2.8 + 3.8, 7.85, 1.5, 1.5), entoure_sol(2.8 + 2 * 3.8, 2.25, 1.5, 1.4)]
    fig = figure(code, sol(*sols), hauteur=12.6)
    return A('Entre les deux', 'En haut, entoure le jouet qui est <b>entre</b> le chat et le lapin. En bas, entoure celui qui est entre le bateau et le ballon.',
             ['entourer'], 'Situer des objets les uns par rapport aux autres : « entre ».', 'R22', fig,
             'Jeu de la file : « Mets-toi entre Léo et Sarah. » Ranger des jouets sur une étagère en suivant des consignes.',
             '« Le ballon est entre le chat et le lapin. »',
             'En haut, le ballon rouge ; en bas, le canard.')

def a_haut_bas():
    code = etagere(4.6, 0.6, 7.8, 3, 4.4)
    # Étagères : dessus des planches en y = 0,7 ; 5,1 ; 9,5.
    jouets = [('ours', 'matBrun', 2.6, 10.8), ('bateau', 'white', 2.8, 6.0), ('voiture', 'matRouge', 2.6, 1.55)]
    for nom, c, s, y in jouets:
        code += P(nom, 8.5, y, s, c=c)
    sols = [entoure_sol(8.5, 10.8, 1.9, 1.7), rf'\draw[sol trait] (7.0,0.8) -- (10.0,2.4) (7.0,2.4) -- (10.0,0.8);',
            P('bateau', 8.5, 6.0, 2.8, c='otGreen')]
    fig = figure(code, sol(*sols), hauteur=14.2)
    return A('En haut, au milieu, en bas', '<b>Entoure</b> le jouet tout en haut, <b>barre</b> celui tout en bas et colorie celui du milieu.',
             ['entourer', 'barrer', 'colorier'], 'Utiliser les mots « en haut », « en bas », « au milieu » pour situer des objets.', 'R22', fig,
             'Ranger des jouets sur une étagère et faire dire où se trouve chacun.',
             '« L’ours est tout en haut. La voiture est en bas. Le bateau est au milieu. »',
             'L’ours est entouré, la voiture barrée, le bateau colorié.')

def a_enclos():
    code = rf'\draw[matBrun,line width=3pt,rounded corners=8pt] (3.2,2.2) rectangle (13.8,11.0);'
    for k in range(12):
        x = 3.2 + k * (10.6 / 11)
        code += rf'\draw[matBrun,line width=2.4pt] ({f(x)},10.6) -- ({f(x)},11.6) ({f(x)},1.8) -- ({f(x)},2.8);'
    dedans = [('lapin', 'matGris', 5.6, 8.4), ('canard', 'matJaune', 10.4, 8.6), ('chat', 'matOrange', 6.4, 4.6), ('lapin', 'matJaune', 11.0, 4.6)]
    dehors = [('canard', 'matJaune', 1.4, 12.6), ('chat', 'matGris', 15.6, 7.0), ('lapin', 'matGris', 1.6, 4.0), ('souris', None, 15.4, 12.6)]
    sols = []
    for nom, c, x, y in dedans + dehors:
        code += P(nom, x, y, 2.2, c='white' if nom != 'souris' else None)
    for nom, c, x, y in dedans:
        sols.append(P(nom, x, y, 2.2, c='otGreen'))
    fig = figure(code, sol(*sols), hauteur=13.6)
    return A('Dans l’enclos', 'Colorie les animaux qui sont <b>à l’intérieur</b> de l’enclos.', ['colorier'],
             'Comprendre et utiliser « à l’intérieur » et « à l’extérieur ».', 'R22', fig,
             'Tracer un grand cercle à la craie dans la cour : « Entre dans le cercle, sors du cercle. »',
             '« Ce lapin est à l’intérieur de l’enclos. Ce canard est à l’extérieur. »',
             'Les quatre animaux à l’intérieur de la barrière. Les quatre autres sont à l’extérieur.', quantites=[4])

def a_labyrinthe():
    murs, chemin = labyrinthe(7, 6, 7, 1.2, 13.2, 2.1)
    code = murs + P('souris', 0.2, 12.15, 1.6) + P('fromage', 16.6, 1.6, 1.8)
    fig = figure(code, sol(chemin_sol([(0.4, 12.15)] + chemin + [(16.0, chemin[-1][1])])), hauteur=13.6)
    return A('Le labyrinthe', 'Trace le chemin de la souris jusqu’au fromage, <b>sans traverser</b> les murs.', ['tracer'],
             'Suivre un déplacement sur une représentation et le tracer.', 'R22', fig,
             'Faire un parcours dans la cour entre des plots, puis le refaire avec le doigt sur un dessin.',
             '« Je vais tout droit, je descends, je tourne… Ce chemin est fermé : je reviens. »',
             'Un seul chemin mène au fromage ; il est tracé en vert sur l’image du guide.',
             controles=[(len(chemin) >= 12, 'chemin assez long')])

def a_trajet():
    code = rf'\fill[matVert!18,rounded corners=10pt] (0.3,0.3) rectangle (16.7,13.6);'
    route = [(2.2, 11.4), (8.0, 11.4), (8.0, 6.6), (3.0, 6.6), (3.0, 2.6), (14.4, 2.6), (14.4, 9.0)]
    pts = ' -- '.join(f'({f(x)},{f(y)})' for x, y in route)
    code += rf'\draw[matGris!45,line width=26pt,line join=round,line cap=round] {pts};'
    code += rf'\fill[matCiel] (8.9,1.0) rectangle (10.6,13.6);'
    code += rf'\draw[mat contour,fill=matBrun!60] (8.6,1.9) rectangle (10.9,3.3);' + texte(9.75, 4.0, 'le pont', 10, 'otMuted', r'\otMedium')
    code += P('chat', 1.2, 12.4, 2.0, c='matOrange') + P('maison', 14.4, 11.0, 3.0, c='matJaune')
    code += P('arbre', 12.2, 8.6, 2.6) + P('sapin', 5.6, 4.6, 2.4) + P('fleur', 12.0, 5.2, 1.6, c='matRose') + P('champignon', 6.0, 9.0, 1.6, c='matRouge')
    fig = figure(code, sol(chemin_sol(route)), hauteur=13.9)
    return A('Le chemin du chat', 'Suis la route avec ton doigt, du chat jusqu’à sa maison. <b>Raconte</b> le trajet, puis trace-le.', ['dire', 'tracer'],
             'Raconter un déplacement à partir d’une représentation, avec des repères et les mots de l’espace.', 'R22', fig,
             'Après un parcours en salle de motricité, le raconter en nommant les repères : « je passe près du banc, je tourne… ».',
             '« Le chat va tout droit, il descend près du champignon, il tourne, il passe à côté du sapin, il traverse le pont et il monte jusqu’à sa maison. »',
             'Le trait suit la route grise. Le récit doit citer les repères dans l’ordre (champignon, sapin, pont).')

PARTIES = [
 ('Plus, moins, autant', 'Comparer des quantités jusqu’à six, et bien plus.',
  'À partir de quatre ans, l’enfant compare des collections globalement, par correspondance terme à terme et en dénombrant chacune. Il comprend qu’une quantité ne change pas quand on déplace les objets.',
  [a_cinq, a_bocaux, a_jetons_alignes, a_assiettes_verres, a_voitures_bateaux], 'pomme'),
 ('Compter jusqu’à six', 'Dénombrer, constituer, associer quantité et chiffre.',
  'L’enfant dénombre des collections jusqu’à six en pointant chaque objet une seule fois, utilise ses doigts et les constellations du dé, et associe chaque quantité à son écriture chiffrée.',
  [a_constellations, a_doigts_chiffres, a_combien_points, a_dessine_de, a_un_de_plus_ms, a_colorie_chiffre, a_parcours_fleurs], 'de'),
 ('Composer et écrire', 'Les nombres jusqu’à six ; la comptine jusqu’à douze.',
  'Les compositions et décompositions (cinq, c’est deux et trois) permettent de dénombrer plus vite. L’enfant s’initie à l’écriture des chiffres de un à six et récite la comptine jusqu’à douze.',
  [a_deux_mains_ms, a_colliers_cinq, a_ecrire((1, 2, 3), 'J’écris 1, 2, 3'), a_ecrire((4, 5, 6), 'J’écris 4, 5, 6'), a_ecrire_quantite, a_comptine12], 'nombre'),
 ('Rangs et cases', 'Le premier, le deuxième… la bande numérique et le jeu de l’oie.',
  'Le nombre sert aussi à repérer une position : un rang dans une file, une case sur une piste. L’enfant compte à partir d’un point de départ, avance ou recule d’une ou deux cases, et découvre le début de la bande numérique.',
  [a_file_animaux, a_wagons_rang, a_perle_rouge, a_bande_lacunaire, a_bande_place, a_oie_avance, a_oie_recule], 'oie'),
 ('Petits problèmes', 'Ajouter, enlever, cacher, regrouper, partager.',
  'Les problèmes se jouent d’abord avec des objets, puis se résolvent sur la fiche. L’enfant peut compter sur ses doigts, surcompter ou utiliser une décomposition (« six, c’est quatre et deux »).',
  [a_fraises, a_chapeau, a_billes_boite, a_cache_main, a_boites_crayons, a_partage_gateaux, a_partage_carottes], 'ours'),
 ('Formes et solides', 'Triangles, carrés, disques ; empreintes et assemblages.',
  'L’enfant reconnaît et classe les formes planes dans toutes les orientations. Les solides (cube, boule, pyramide, cylindre) se manipulent : la fiche travaille leurs empreintes. Aucun solide n’est dessiné en perspective.',
  [a_trois_formes, a_intrus_formes, a_empreintes_cube, a_empreintes_pyramide, a_fusee, a_pavage5], 'formes'),
 ('Longueurs et masses', 'Plus long, plus court ; plus lourd, plus léger.',
  'L’enfant classe et range des objets selon leur longueur, en les mettant à la même origine quand c’est nécessaire. La masse est introduite à partir de quatre ans : on soupèse, puis on utilise une balance de Roberval.',
  [a_trois_groupes, a_ordre_crayons, a_meme_longueur_ms, a_plus_lourd, a_balances], 'balance'),
 ('Les motifs', 'Continuer, trouver l’intrus, mémoriser.',
  'Un motif répétitif suit une règle : l’enfant la repère, la dit avec ses mots, trouve l’intrus et prolonge le motif. Toute proposition cohérente est acceptée si l’enfant explique sa règle.',
  [a_prolonger, a_intrus_motif, a_quel_motif, a_memoire, a_motif_manquant], 'perle'),
 ('Se repérer', 'Entre, au milieu, à l’intérieur ; suivre un chemin.',
  'L’enfant situe les objets les uns par rapport aux autres et utilise un vocabulaire plus riche : entre, au milieu, à l’intérieur, à l’extérieur. Il suit un déplacement sur un dessin et le raconte.',
  [a_entre, a_haut_bas, a_enclos, a_labyrinthe, a_trajet], 'souris'),
]

RESUME = (r'\begin{itemize}[leftmargin=5mm,itemsep=1.2mm,topsep=0pt]'
          r'\item comparer, dénombrer et constituer des collections jusqu’à six ;'
          r'\item composer et décomposer les nombres jusqu’à six, écrire les chiffres de 1 à 6 ;'
          r'\item réciter la comptine numérique jusqu’à douze ;'
          r'\item repérer un rang, avancer et reculer sur une piste, découvrir la bande numérique ;'
          r'\item résoudre des problèmes : ajout, retrait, groupements, partage ;'
          r'\item reconnaître triangles, carrés, disques et les empreintes des solides ;'
          r'\item comparer des longueurs et des masses, prolonger des motifs, se repérer dans l’espace.'
          r'\end{itemize}')

PERIMETRE = (r'\textbf{3. Choix faits dans ce cahier}\par '
             r'Les quantités à dénombrer ne dépassent pas six ; les comparaisons globales portent sur des collections plus grandes, '
             r'dont l’une a au moins deux fois plus d’objets que l’autre. La comptine est récitée jusqu’à douze, mais les chiffres écrits '
             r'ne dépassent pas six. Les solides ne sont pas dessinés en perspective : on travaille leurs empreintes, avec de vrais solides. '
             r'Les assemblages comportent au plus cinq pièces. Les doigts sont montrés en commençant par le pouce, mais toute autre façon '
             r'de montrer un nombre est juste. Chaque fiche commence par une activité avec de vrais objets, décrite dans le guide de l’adulte.')
