"""Constructions, propriétés et dénombrement : niveau Sixième."""
from fractions import Fraction as F
from modele_6e import ex,q,n,m


def distances_cercles(i,l):
    rayon=3+l+i%3
    return ex('Placer les balises autour d’un point',f'On trace le cercle de centre O et de rayon {rayon} cm. Trois balises A, B et C sont placées à des distances de O respectivement égales à {rayon-1} cm, {rayon} cm et {rayon+2} cm.',[
        q('Décrire avec des mots tous les points du cercle.', 'Le centre et le rayon définissent le cercle : les points du cercle ont tous exactement la même distance au centre.', f'Les points situés à exactement {rayon} cm de O.'),
        q('Quelle balise appartient au cercle ? Justifier.', 'Comparer chaque distance au rayon. L’appartenance au cercle exige l’égalité.', f'B, car OB = {rayon} cm.'),
        q('Où se trouve A par rapport au disque délimité par le cercle ?', 'Une distance au centre inférieure au rayon place le point à l’intérieur du disque, sans le placer sur le cercle.', f'À l’intérieur, car OA = {rayon-1} cm < {rayon} cm.'),
        q('Où se trouve C par rapport au disque ?', 'Une distance au centre supérieure au rayon place le point à l’extérieur.', f'À l’extérieur, car OC = {rayon+2} cm > {rayon} cm.'),
        q('Un diamètre passant par B rencontre le cercle en D, de l’autre côté de O. Calculer BD.', 'O est entre B et D et les deux rayons ont même longueur ; additionner les deux rayons.', f'{2*rayon} cm.', m(f'{rayon}+{rayon}={2*rayon}'), f'2*{rayon} == {2*rayon}'),
        q('Distinguer le segment OB, sa longueur OB et la droite OB. Lequel est un rayon ?', 'Un segment est un objet borné, une longueur est un nombre avec une unité et une droite se prolonge sans limite.', f'[OB] est un segment rayon ; OB = {rayon} cm est sa longueur ; (OB) est une droite.')],
        'Le cercle est la frontière ; le disque contient aussi l’intérieur. Pour un cercle, la distance au centre est exactement égale au rayon.',
        dict(type='circle_points',radius=rayon),True)


def mediatrice(i,l):
    ab=4+2*i
    pa=ab//2+2+l
    return ex('Trouver un lieu à égale distance',f'Deux lieux A et B sont séparés de {ab} cm sur un plan. M est le milieu du segment AB. On trace la droite perpendiculaire à AB passant par M. Un point P de cette droite vérifie PA = {pa} cm.',[
        q('Calculer AM et MB.', 'Un milieu partage un segment en deux segments de même longueur.', f'AM = MB = {ab//2} cm.'),
        q('Quel est le nom de la droite construite ?', 'La médiatrice d’un segment est la droite perpendiculaire au segment qui passe par son milieu.', 'La médiatrice du segment AB.'),
        q('Calculer PB sans mesurer le dessin.', 'Tout point de la médiatrice d’un segment est à égale distance de ses extrémités ; P appartient à cette droite.', f'PB = PA = {pa} cm.'),
        q('Décrire une construction de la médiatrice au compas.', 'Tracer deux arcs de même rayon centrés en A puis en B ; leur rayon doit être supérieur à la moitié de AB pour qu’ils se coupent en deux points.', f'Choisir un rayon supérieur à {ab//2} cm, tracer les deux paires d’arcs, puis relier leurs deux intersections.'),
        q('Un point Q vérifie QA = QB. Que peut-on affirmer sur sa position ?', 'La propriété fonctionne dans l’autre sens : les points équidistants de A et B appartiennent à la médiatrice.', 'Q appartient à la médiatrice de AB.'),
        q('Le fait d’être à égale distance de A et B impose-t-il d’être leur milieu ?', 'M est un point particulier de la médiatrice, mais celle-ci contient une infinité d’autres points. Distinguer la droite et un de ses points.', 'Non. P, situé en dehors de AB sur la figure, peut être équidistant de A et B sans être leur milieu.')],
        'Une médiatrice permet de justifier des distances égales. Une apparence de milieu ou d’angle droit sur un schéma ne suffit pas.',
        dict(type='bisector',length=ab,distance=pa),True)


def angles(i,l):
    angle=30+10*i+5*l
    demi=F(angle,2)
    return ex('Mesurer puis partager un angle',f'L’angle AOB mesure {angle}°. On veut le reproduire avec un rapporteur puis tracer sa bissectrice OC. Les demi-droites OA et OB partent toutes deux de O.',[
        q('Nommer le sommet de l’angle et ses côtés.', 'Dans un nom d’angle à trois lettres, la lettre centrale est le sommet ; les côtés sont deux demi-droites issues de ce sommet.', 'Sommet O ; côtés [OA) et [OB).'),
        q('Classer l’angle : aigu, droit ou obtus.', 'Comparer sa mesure à 90° ; aigu signifie moins de 90°, obtus signifie entre 90° et 180°.', 'Aigu.' if angle<90 else 'Droit.' if angle==90 else 'Obtus.'),
        q('Comment placer le rapporteur pour reproduire cet angle ?', 'L’origine du rapporteur va sur le sommet, et le zéro de la bonne graduation doit coïncider avec un côté déjà tracé.', f'Placer son centre sur O, aligner le zéro avec OA, puis marquer {angle}° dans le sens choisi.'),
        q('Quelle propriété définit la bissectrice OC ?', 'La bissectrice est une demi-droite intérieure à l’angle qui le partage en deux angles de même mesure.', 'Les angles AOC et COB sont égaux et leur somme vaut l’angle AOB.'),
        q('Calculer les deux angles obtenus.', 'Partager la mesure initiale en deux parts égales.', m(n(demi))+'° chacun.', m(f'{angle}\\div2={n(demi)}'), f'2*F("{demi}") == {angle}'),
        q('Vérifier le partage puis décrire une erreur fréquente avec le rapporteur.', 'Additionner les deux demi-angles pour retrouver l’angle initial. Pour mesurer, le sens de lecture doit commencer au zéro du côté de départ.', m(n(demi)+'+'+n(demi)+f'={angle}')+'°. Lire l’autre graduation sans vérifier le zéro peut donner le mauvais angle.')],
        'Une mesure au rapporteur se lit depuis le zéro choisi, et non depuis n’importe quel bord. La bissectrice partage la mesure, pas la longueur des côtés.',
        dict(type='angle_bisector',angle=angle),True)


def triangles(i,l):
    if i%2:
        a,b=35+5*i,40+5*l
        c=180-a-b
        return ex('Préparer une construction avec deux angles',f'On veut construire le triangle ABC avec AB = {5+l} cm, l’angle BAC = {a}° et l’angle ABC = {b}°. On utilise la propriété de la somme des angles du triangle, rencontrée en classe.',[
            q('Calculer la somme des deux angles connus.', 'Les deux mesures connues concernent deux sommets distincts du même triangle ; les additionner.', f'{a+b}°.'),
            q('Calculer l’angle ACB.', 'La somme des trois angles d’un triangle vaut 180° ; soustraire la somme des deux angles connus.', f'{c}°.', m(f'180-({a}+{b})={c}'), f'{a}+{b}+{c} == 180'),
            q('Par quel segment commencer la construction ?', 'Tracer d’abord le côté dont la longueur est fixée ; ses extrémités serviront à placer les deux angles.', f'Le segment AB de {5+l} cm.'),
            q('Comment placer C ?', 'Tracer les demi-droites à l’aide du rapporteur, depuis A et B et dans le même demi-plan par rapport à AB.', f'Tracer {a}° en A et {b}° en B ; C est l’intersection des deux demi-droites.'),
            q('Comment vérifier la construction obtenue ?', 'Les mesures demandées doivent être contrôlées sur la construction en vraie grandeur, pas sur une figure de travail.', f'Vérifier AB = {5+l} cm, les angles en A et B, puis l’angle en C de {c}°.'),
            q('Deux positions symétriques de C sont possibles. Est-ce une erreur ?', 'Les demi-droites peuvent être construites au-dessus ou au-dessous de AB ; les deux figures sont images l’une de l’autre par symétrie axiale.', 'Non. Les deux triangles respectent les mêmes données et sont symétriques par rapport à la droite AB.')],
            'Les calculs préparent la construction ; le rapporteur permet de la réaliser. Un schéma n’est pas à mesurer.',
            dict(type='triangle_angles',a=a,b=b,base=5+l),True)
    base=4+i
    cote=base+1+l
    return ex('Construire un triangle et son cercle',f'On veut construire un triangle ABC avec AB = {base} cm, AC = BC = {cote} cm. On dispose d’une règle, d’un compas et d’une équerre.',[
        q('Quelle est la nature de ce triangle ? Préciser son sommet principal.', 'Deux côtés de même longueur définissent un triangle isocèle ; ils se rencontrent au sommet principal.', 'Triangle isocèle en C, car CA = CB.'),
        q('Quel côté peut-on tracer en premier ?', 'Commencer par un côté connu permet de fixer les deux centres des arcs de construction.', f'Tracer AB de {base} cm à la règle.'),
        q('Comment placer le sommet C avec le compas ?', 'C doit être à la distance donnée de A et de B simultanément : il est à une intersection de deux cercles.', f'Tracer deux arcs de rayon {cote} cm, l’un de centre A et l’autre de centre B ; choisir une intersection pour C.'),
        q('Calculer le périmètre du triangle.', 'Le périmètre est la somme des longueurs des trois côtés ; la construction n’est pas nécessaire pour ce calcul.', f'{base+2*cote} cm.', m(f'{base}+{cote}+{cote}={base+2*cote}'), f'{base}+2*{cote} == {base+2*cote}'),
        q('Où se trouve C par rapport à la médiatrice de AB ?', 'Un point à égale distance de A et de B appartient à la médiatrice de AB ; les deux côtés égaux donnent ces distances.', 'C appartient à la médiatrice de AB.'),
        q('Décrire la construction du cercle passant par A, B et C.', 'Le centre du cercle circonscrit est à égale distance des trois sommets. L’intersection de deux médiatrices permet de l’obtenir.', 'Tracer les médiatrices de deux côtés ; leur intersection O est le centre. Tracer le cercle de centre O passant par A, puis vérifier qu’il passe aussi par B et C.')],
        'Préparer une figure de travail, construire avec les instruments, puis justifier avec les données et les propriétés d’équidistance.',
        dict(type='triangle_sides',base=base,side=cote),True)


def symetrie_axiale(i,l):
    distance=2+i%3
    largeur=2+l
    hauteur=3+i%2
    perimetre=2*(largeur+hauteur)
    return ex('Compléter un motif par pliage',f'Un rectangle ABCD est dessiné sur un quadrillage. Son côté AD est vertical, à {distance} carreaux à droite d’un axe vertical ; le rectangle s’étend encore de {largeur} carreaux vers la droite et de {hauteur} carreaux vers le haut. On cherche son image par symétrie d’axe la droite verticale.',[
        q('De quel côté de l’axe se trouve le rectangle image ?', 'Un pliage selon l’axe transporte les points de l’autre côté en conservant leur distance perpendiculaire à l’axe.', 'À gauche de l’axe.'),
        q('À quelle distance de l’axe placer A′ et D′ ?', 'A et D ont la même distance à l’axe ; leurs images sont à cette même distance de l’autre côté.', f'{distance} carreaux à gauche.'),
        q('À quelle distance de l’axe placer B′ et C′ ?', 'Les sommets les plus éloignés de l’axe sont à la distance du premier côté augmentée de la largeur du rectangle.', f'{distance+largeur} carreaux à gauche.'),
        q('Quelle est la nature et quelles sont les dimensions de la figure image ?', 'La symétrie conserve les angles droits et les longueurs des côtés.', f'Un rectangle de {largeur} carreaux sur {hauteur} carreaux.'),
        q('Calculer le périmètre de la figure image en unités du quadrillage.', 'Les longueurs sont conservées ; le périmètre est donc le même que celui du rectangle initial.', f'{perimetre} unités de longueur.', m(f'2({largeur}+{hauteur})={perimetre}')),
        q('Que peut-on affirmer du segment qui joint un sommet à son image ?', 'L’axe de symétrie est la médiatrice du segment joignant chaque point à son image.', 'Ce segment est perpendiculaire à l’axe et son milieu est sur l’axe.')],
        'Compter les carreaux perpendiculairement à l’axe. Une symétrie conserve la forme ; elle ne décale pas simplement le dessin.',
        dict(type='reflection_rectangle',distance=distance,width=largeur,height=hauteur),True)


def solides_volumes(i,l):
    a,b,c=3+i,2+l,2+i%3
    cubes=a*b*c
    return ex('Construire un pavé avec des cubes',f'On construit un bloc avec des petits cubes de 1 cm d’arête. Chaque couche rectangulaire contient {a} cubes dans le sens de la longueur et {b} dans le sens de la largeur. On empile {c} couches identiques, sans vide.',[
        q('Quel est le volume d’un petit cube ?', 'Un cube de 1 cm d’arête définit l’unité de volume appelée centimètre cube.', '1 cm³.'),
        q('Combien de petits cubes contient une rangée ?', 'La longueur de la couche indique le nombre de cubes alignés dans une rangée.', f'{a} cubes.'),
        q('Combien de cubes contient une couche complète ?', 'Il y a autant de rangées que de cubes dans le sens de la largeur ; multiplier les deux effectifs.', f'{a*b} cubes.', m(f'{a}\\times{b}={a*b}')),
        q('Combien de cubes contient le bloc complet ?', 'Chaque couche est identique et pleine ; multiplier le nombre de cubes d’une couche par le nombre de couches.', f'{cubes} cubes.', m(f'{a*b}\\times{c}={cubes}'), f'{a}*{b}*{c} == {cubes}'),
        q('Quel est le volume du bloc en cm³ ?', 'Le volume se mesure en comptant les cubes unités qui remplissent le solide, y compris ceux cachés dans la représentation.', f'{cubes} cm³.'),
        q('Si on retire une couche complète, combien de cubes et quel volume reste-t-il ?', 'Enlever les cubes d’une couche du total ; on peut aussi compter les couches restantes.', f'{a*b*(c-1)} cubes, soit {a*b*(c-1)} cm³.')],
        'La perspective cache certains cubes ; compter par rangées et par couches pour ne pas oublier les cubes invisibles. En 6e, on construit le sens du cm³ par dénombrement.',
        dict(type='cube_layers',length=a,width=b,height=c),True)


BUILDERS={'distances-cercles':distances_cercles,'mediatrice':mediatrice,'angles':angles,
    'triangles':triangles,'symetrie-axiale':symetrie_axiale,'solides-volumes':solides_volumes}
