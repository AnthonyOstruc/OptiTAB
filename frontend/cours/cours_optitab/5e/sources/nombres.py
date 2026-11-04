"""Problèmes originaux : opérations, divisibilité et nombres relatifs."""
from fractions import Fraction as F
from modele_5e import ex, q, n, m


def operations(i, niveau):
    a, b, groupes = 3+i, 2+niveau, 4+niveau
    prix = F(25+5*i+3*niveau, 10)
    budget = groupes*(a+b)*prix + 20 + i
    total = groupes*(a+b)*prix
    return ex(['Les fournitures des ateliers', 'Une commande de carnets', 'Le budget du club'][i%3],
        f'Un club prépare {groupes} ateliers. Chaque atelier reçoit {a} carnets bleus et {b} carnets verts. Chaque carnet coûte {m(n(prix))} €. Le club dispose de {m(n(budget))} €. Les frais de livraison pour toute la commande sont de 6 €.', [
        q('Combien de carnets faut-il pour un atelier ?', 'Les deux couleurs se complètent : on additionne leurs effectifs.', f'{a+b} carnets.', m(f'{a}+{b}={a+b}'), f'{a}+{b} == {a+b}'),
        q('Combien de carnets faut-il pour tous les ateliers ?', 'Chaque atelier reçoit le même nombre : on multiplie le nombre d’ateliers par les besoins d’un atelier.', f'{groupes*(a+b)} carnets.', m(f'{groupes}\\times({a}+{b})={groupes*(a+b)}')),
        q('Écrire une seule expression pour le prix des carnets, puis la calculer.', 'Les parenthèses regroupent les carnets d’un atelier ; le prix unitaire multiplie le nombre total.', m(n(total))+' €.', m(f'{groupes}\\times({a}+{b})\\times {n(prix)}={n(total)}'), f'{groupes}*({a}+{b})*F("{prix}") == F("{total}")'),
        q('Calculer le coût de la commande, livraison comprise.', 'Les frais concernent toute la commande ; on les ajoute une seule fois après le prix des carnets.', m(n(total+6))+' €.', m(f'{n(total)}+6={n(total+6)}')),
        q('Quelle somme restera-t-il au club ?', 'On soustrait la dépense totale au budget disponible et on vérifie que le reste est positif.', m(n(budget-total-6))+' €.', m(f'{n(budget)}-({n(total)}+6)={n(budget-total-6)}')),
        q('Un élève multiplie aussi les 6 € de livraison par le nombre d’ateliers. De combien surestime-t-il la dépense ?', 'Comparer la livraison facturée une fois à la livraison comptée une fois par atelier : seules les copies supplémentaires sont en trop.', f'{6*(groupes-1)} € de trop.', m(f'6\\times {groupes}-6={6*(groupes-1)}'), f'6*{groupes}-6 == {6*(groupes-1)}')],
        'Lire « pour chaque » et « pour toute la commande » avant de poser un calcul ; une parenthèse indique une quantité regroupée.',
        dict(type='table', headers=['Pour un atelier', 'Carnets bleus', 'Carnets verts'], rows=[['Quantités', a, b], ['Prix par carnet', n(prix)+' €', n(prix)+' €']]))


def divisibilite(i, niveau):
    capacite = 4+i
    quotient = 5+2*niveau+i
    reste = 1+i%3
    total = capacite*quotient+reste
    return ex(['Des places pour une sortie', 'Ranger la collection', 'Préparer les colis'][i%3],
        f'Une association doit ranger {total} objets dans des boîtes qui contiennent chacune au maximum {capacite} objets. Les objets ne peuvent pas être découpés.', [
        q(f'Encadrer {total} par deux multiples consécutifs de {capacite}.', 'Chercher deux produits consécutifs entre lesquels se trouve le nombre d’objets.', m(f'{capacite*quotient}\\le {total}<{capacite*(quotient+1)}'), m(f'{capacite}\\times {quotient}={capacite*quotient} \\ ;\\ {capacite}\\times {quotient+1}={capacite*(quotient+1)}')),
        q('Effectuer la division euclidienne : donner quotient et reste.', 'Le quotient compte les boîtes pleines ; le reste compte les objets qui ne remplissent pas une boîte.', f'Quotient {quotient} ; reste {reste}.', m(f'{total}={capacite}\\times {quotient}+{reste}'), f'divmod({total},{capacite}) == ({quotient},{reste})'),
        q('Vérifier que le reste est autorisé.', 'Dans une division euclidienne, le reste est positif ou nul et strictement inférieur au diviseur.', m(f'0\\le {reste}<{capacite}')+' : le reste convient.'),
        q('Combien de boîtes faut-il pour ranger tous les objets ?', 'Le reste est non nul : une boîte supplémentaire est nécessaire pour les derniers objets.', f'{quotient+1} boîtes.', m(f'{quotient}+1={quotient+1}')),
        q('Combien de places resteront vides dans la dernière boîte ?', 'La dernière boîte reçoit le reste ; on soustrait ce reste à sa capacité.', f'{capacite-reste} places.', m(f'{capacite}-{reste}={capacite-reste}'), f'{capacite}*({quotient}+1)-{total} == {capacite-reste}'),
        q(f'{capacite} est-il un diviseur de {total} ? Quel nombre minimal d’objets faudrait-il ajouter pour obtenir des boîtes toutes pleines ?', 'Un diviseur donne un reste nul. Compléter la dernière boîte supprime le reste.', f'Non ; il faut ajouter {capacite-reste} objets pour obtenir {capacite*(quotient+1)} objets.')],
        'Le quotient entier, le reste et le nombre de boîtes nécessaires sont trois informations différentes. Toujours interpréter le résultat.',
        dict(type='boxes', total=total, capacity=capacite, quotient=quotient, remainder=reste))


def relatifs(i, niveau):
    a, b, c = -(2+i+niveau), 3+i, -1-niveau
    vals = sorted([a,b,c,0])
    distances = {p:abs(v) for p,v in [('A',a),('B',b),('C',c),('O',0)]}
    groupes = [' et '.join(p for p in distances if distances[p]==d) for d in sorted(set(distances.values()),reverse=True)]
    return ex(['Les étages du bâtiment', 'Un relevé de températures', 'Les balises de la grotte'][i%3],
        f'Sur une droite graduée d’unité 1, les points A, B et C ont respectivement pour abscisses {a}, {b} et {c}. Le point O a pour abscisse 0. La droite aide à comparer les positions.', [
        q('Quels points ont une abscisse négative ?', 'Sur une droite orientée vers la droite, les nombres négatifs sont situés à gauche de l’origine.', 'A et C, car leurs abscisses sont strictement inférieures à 0.'),
        q('Ranger les quatre abscisses dans l’ordre croissant.', 'Lire les points de gauche à droite ; parmi les nombres négatifs, celui qui est le plus éloigné de zéro est le plus petit.', m('<'.join(map(str,vals)))),
        q('Quelle est la distance de A à zéro ?', 'Une distance n’est jamais négative ; elle correspond au nombre d’unités séparant le point de l’origine.', f'{-a} unités.', controle=f'abs({a}) == {-a}'),
        q('Donner l’abscisse du point D opposé à A.', 'Deux nombres opposés ont la même distance à zéro et des signes contraires.', m(f'{-a}')+'.', m(f'{a}+{-a}=0')),
        q('Quelle est la distance entre A et B ?', 'Les points sont de part et d’autre de zéro : additionner les deux distances à l’origine.', f'{b-a} unités.', m(f'{-a}+{b}={b-a}'), f'{b}-({a}) == {b-a}'),
        q('Ranger A, B, C et O du plus éloigné au plus proche de zéro. Y a-t-il une égalité ?', 'Comparer les distances à zéro au lieu de comparer les abscisses : un point négatif peut être très éloigné.', 'Du plus éloigné au plus proche : '+' ; puis '.join(groupes)+'. Distances : '+', '.join(f'{p} : {abs(v)}' for p,v in [('A',a),('B',b),('C',c),('O',0)])+'. '+('A et B sont à égalité.' if abs(a)==b else 'Aucune égalité.'))],
        'Comparer des nombres et comparer leurs distances à zéro sont deux questions différentes ; zéro n’est ni strictement positif ni strictement négatif.',
        dict(type='numberline', points={'A':a,'B':b,'C':c,'O':0}), True)


def sommes_relatifs(i, niveau):
    depart = -4-i
    hausse = 7+niveau+i
    baisse = 5+2*niveau
    t1, t2 = depart+hausse, depart+hausse-baisse
    return ex(['La station météo', 'La sonde de montagne', 'Le journal de températures'][i%3],
        f'À 6 h, la température est de {depart} °C. Elle augmente de {hausse} °C avant midi, puis baisse de {baisse} °C avant 18 h. On étudie les variations de cette même journée.', [
        q('Traduire la hausse du matin par un nombre relatif.', 'Une augmentation se représente par une variation positive.', m(f'+{hausse}')+' °C.'),
        q('Quelle est la température à midi ?', 'Ajouter la variation du matin à la température initiale ; on ne change pas arbitrairement le signe de la température.', f'{t1} °C.', m(f'({depart})+(+{hausse})={t1}'), f'{depart}+{hausse} == {t1}'),
        q('Traduire la baisse de l’après-midi par un nombre relatif.', 'Une diminution se représente par un nombre négatif, même si la température de départ était positive.', m(f'-{baisse}')+' °C.'),
        q('Quelle est la température à 18 h ?', 'Soustraire la baisse à la température de midi, ou ajouter la variation négative.', f'{t2} °C.', m(f'{t1}-{baisse}={t1}+(-{baisse})={t2}'), f'{t1}-{baisse} == {t2}'),
        q('Calculer la variation entre 6 h et 18 h.', 'La variation totale est finale moins initiale ; elle doit aussi être égale à la somme des variations successives.', f'{hausse-baisse:+d} °C.', m(f'{t2}-({depart})={hausse-baisse} \\ ;\\ {hausse}-{baisse}={hausse-baisse}')),
        q('Quelle variation faut-il ensuite pour revenir à la température de 6 h ?', 'La variation du retour est l’opposée de la variation totale : sa somme avec la variation aller est nulle.', f'{baisse-hausse:+d} °C.', m(f'{t2}+({baisse-hausse})={depart}'), f'{t2}+({baisse-hausse}) == {depart}')],
        'Température et variation sont deux grandeurs différentes. Pour contrôler une variation, additionner départ et variation : on doit retrouver l’arrivée.',
        dict(type='steps', labels=['6 h','Midi','18 h'], values=[depart,t1,t2]), True)


def fractions(i, niveau):
    d = [4,5,6,8,10,12,20][i]
    a = 1+niveau
    quantite = d*(4+i+niveau)
    part = F(a,d)
    return ex(['La réserve de jus', 'Les rubans de l’atelier', 'Une collection à partager'][i%3],
        f'Un atelier possède {quantite} L de jus. Il en réserve {m(rf"\frac{{{a}}}{{{d}}}")} pour le matin. Toutes les fractions de cet exercice concernent cette réserve initiale, sauf indication contraire.', [
        q('Que représentent le numérateur et le dénominateur de la fraction réservée ?', 'Le dénominateur donne le nombre de parts égales de l’unité ; le numérateur indique combien de ces parts sont prises.', f'{d} parts égales, dont {a} sont réservées.'),
        q('Écrire une fraction égale en doublant numérateur et dénominateur.', 'Multiplier les deux termes d’une fraction par un même nombre non nul conserve le quotient.', m(rf'\frac{{{2*a}}}{{{2*d}}}='+n(part)), controle=f'F({2*a},{2*d}) == F({a},{d})'),
        q('Quelle quantité représente une seule part ?', 'Partager d’abord la quantité initiale par le dénominateur.', f'{quantite//d} L.', m(f'{quantite}\\div {d}={quantite//d}')),
        q('Quelle quantité est réservée pour le matin ?', 'Multiplier la valeur d’une part par le numérateur. C’est prendre une fraction d’une quantité.', f'{quantite*a//d} L.', m(f'{quantite}\\div {d}\\times {a}={quantite*a//d}'), f'F({a},{d})*{quantite} == {quantite*a//d}'),
        q('Quelle fraction de la réserve initiale reste-t-il ?', 'Une unité entière vaut dénominateur sur lui-même ; on enlève les parts réservées.', m(n(1-part))+'.', m(rf'\frac{{{d}}}{{{d}}}-\frac{{{a}}}{{{d}}}=\frac{{{d-a}}}{{{d}}}')),
        q('La quantité réservée dépasse-t-elle la moitié ? Justifier sans approximation.', 'Mettre la fraction et un demi au même dénominateur, ou comparer le double du numérateur au dénominateur.', ('Oui' if 2*a>d else 'Non')+f' : le double du numérateur vaut {2*a}, '+('supérieur à' if 2*a>d else 'inférieur ou égal à')+f' {d}.')],
        'Une fraction se réfère toujours à une unité précise. Pour calculer une part, diviser par le dénominateur puis multiplier par le numérateur.',
        dict(type='fraction', denominator=d, numerator=a, total=quantite), True)


def additions_fractions(i, niveau):
    d = [6,8,10,12,14,16,18][i]
    a, b = 1+niveau, 1
    matin, apres = F(a,d), F(b,d//2)
    total = matin+apres
    quantite = d*10
    return ex(['Le réservoir du jardin', 'L’eau des serres', 'Le suivi de l’arrosage'][i%3],
        f'Un réservoir contient {quantite} L. On utilise {m(rf"\frac{{{a}}}{{{d}}}")} du volume initial le matin et {m(rf"\frac{{{b}}}{{{d//2}}}")} du volume initial l’après-midi. On ne remplit pas le réservoir entre les deux.', [
        q('Pourquoi peut-on additionner les deux fractions ?', 'On additionne des parts comparables parce que les deux fractions portent explicitement sur le même volume initial.', 'Les deux fractions ont la même unité de référence : le réservoir initial.'),
        q('Écrire la fraction de l’après-midi avec le même dénominateur que celle du matin.', 'Multiplier le numérateur et le dénominateur par 2 pour obtenir des parts de même taille.', m(rf'\frac{{1}}{{{d//2}}}=\frac{{2}}{{{d}}}'), controle=f'F(1,{d//2}) == F(2,{d})'),
        q('Quelle fraction du volume initial a été utilisée en tout ?', 'Additionner les nombres de parts en conservant leur taille : le dénominateur reste inchangé.', m(n(total))+'.', m(rf'\frac{{{a}}}{{{d}}}+\frac{{2}}{{{d}}}=\frac{{{a+2}}}{{{d}}}='+n(total)), f'F({a},{d})+F(1,{d//2}) == F("{total}")'),
        q('Quelle fraction du volume initial reste-t-il ?', 'Écrire le réservoir entier sous la forme d/d puis soustraire la fraction utilisée.', m(n(1-total))+'.', m(rf'1-\frac{{{a+2}}}{{{d}}}=\frac{{{d-a-2}}}{{{d}}}')),
        q('Calculer le nombre de litres utilisés et le nombre de litres restants.', 'Appliquer chaque fraction au volume initial. Leur somme doit redonner la capacité initiale.', f'{n(total*quantite)} L utilisés ; {n((1-total)*quantite)} L restants.', m(f'{quantite}\\times {n(total)}={n(total*quantite)}')),
        q('L’après-midi a-t-on utilisé plus d’eau que le matin ? Donner l’écart en litres.', 'Les fractions sont au même dénominateur : comparer les numérateurs, puis calculer la différence entre les volumes.', ('Plus' if apres>matin else 'Autant' if apres==matin else 'Moins')+f' d’eau l’après-midi ; écart de {n(abs(apres-matin)*quantite)} L.', controle=f'F("{total*quantite}")+F("{(1-total)*quantite}") == {quantite}')],
        'On n’additionne pas les dénominateurs. Si la seconde fraction concernait seulement le reste, il faudrait changer le modèle.',
        dict(type='fraction', denominator=d, numerator=a+2, total=quantite), True)


def carres_cubes(i, niveau):
    cote = 2+i+niveau
    return ex(['Une mosaïque et des cubes', 'L’atelier de construction', 'Du carré au cube'][i%3],
        f'On fabrique une mosaïque carrée de {cote} carreaux de côté, puis un grand cube ayant {cote} petits cubes sur chaque arête. Chaque carreau a un côté de 1 cm et chaque petit cube une arête de 1 cm.', [
        q('Écrire le nombre de carreaux comme un produit puis comme un carré.', 'Un carré contient autant de lignes que de colonnes : on multiplie le nombre de lignes par le nombre de carreaux d’une ligne.', m(f'{cote}\\times {cote}={cote}^2')+'.'),
        q('Calculer l’aire de la mosaïque.', 'Chaque carreau a une aire de 1 cm² : le nombre de carreaux et l’aire ont la même valeur numérique, mais pas la même unité.', f'{cote*cote} cm².', m(f'{cote}^2={cote*cote}'), f'{cote}**2 == {cote*cote}'),
        q('Combien de couches de petits cubes comporte le grand cube ?', 'La hauteur du cube est le nombre de cubes le long d’une arête verticale.', f'{cote} couches.'),
        q('Écrire puis calculer le nombre total de petits cubes.', 'Chaque couche compte le carré du côté ; on multiplie encore par le nombre de couches.', f'{cote**3} petits cubes.', m(f'{cote}^3={cote}\\times {cote}\\times {cote}={cote**3}'), f'{cote}**3 == {cote**3}'),
        q('Si on double le côté de la mosaïque, par combien son aire est-elle multipliée ?', 'Le doublement concerne les lignes et les colonnes. Il y a donc deux facteurs 2.', f'Par 4 : la nouvelle aire est {4*cote*cote} cm².', m(rf'(2\times {cote})^2=4\times {cote}^2')),
        q('Si on double l’arête du grand cube, par combien son volume est-il multiplié ?', 'Longueur, largeur et hauteur doublent : il y a trois facteurs 2.', f'Par 8 : le nouveau volume est {8*cote**3} cm³.', m(rf'(2\times {cote})^3=8\times {cote}^3'), f'(2*{cote})**3 == 8*{cote**3}')],
        'Un exposant compte les facteurs identiques : un carré a deux facteurs et un cube trois. Doubler une longueur ne double pas son aire.',
        dict(type='grid', side=cote), True)


BUILDERS = {'operations':operations, 'divisibilite':divisibilite, 'relatifs':relatifs,
    'sommes-relatifs':sommes_relatifs, 'fractions':fractions,
    'additions-fractions':additions_fractions, 'carres-cubes':carres_cubes}
