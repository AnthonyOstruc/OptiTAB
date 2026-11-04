"""Géométrie : données explicites, propriétés et figures codées."""
from fractions import Fraction as F
from modele_5e import ex,q,n,m


def angles(i,niveau):
    angle=30+5*i+5*niveau
    if i%2:
        return ex('Deux parallèles et une sécante',
            f'Les droites d et e sont parallèles et une sécante les coupe en A et B. En A, l’angle situé au-dessus de d et à droite de la sécante mesure {angle}°. Les positions des autres angles sont indiquées sur la figure.', [
            q('Cet angle est-il aigu, droit ou obtus ?', 'Comparer la mesure à 90° ; un angle aigu est strictement compris entre 0° et 90°.', 'Aigu, car '+m(f'0<{angle}<90')+'.'),
            q('Calculer l’angle opposé par le sommet à l’angle donné.', 'Deux angles opposés par le sommet ont la même mesure, même sans hypothèse de parallélisme.', f'{angle}°.'),
            q('Calculer l’angle adjacent à l’angle donné et situé sur la même demi-droite de d.', 'Ces deux angles forment ensemble un angle plat : leur somme vaut 180°.', f'{180-angle}°.', m(f'180-{angle}={180-angle}'), f'180-{angle} == {180-angle}'),
            q('Calculer en B l’angle correspondant à l’angle donné en A.', 'La sécante coupe deux parallèles : les angles situés dans la même position aux deux intersections sont égaux.', f'{angle}°.'),
            q('Calculer en B l’angle alterne-interne à l’angle intérieur situé en bas à gauche de A.', 'Les angles sont à l’intérieur des deux parallèles, de part et d’autre de la sécante : ils sont égaux.', f'{angle}°.'),
            q('Si le parallélisme de d et e n’était plus donné, pourrait-on conserver les réponses des deux dernières questions ?', 'Distinguer les propriétés vraies à une seule intersection de celles qui utilisent deux droites parallèles.', 'Non. Il faudrait prouver le parallélisme, ou disposer d’autres mesures. L’apparence du dessin ne suffit pas.')],
            'Pour invoquer des angles correspondants ou alternes-internes égaux, citer explicitement le parallélisme et repérer les positions.',
            dict(type='parallel',angle=angle),True)
    return ex('Une rosace d’angles',
        f'Deux droites AB et CD se coupent en O. Les points A, O, B sont alignés dans cet ordre, et C, O, D également. L’angle AOC mesure {angle}°. La demi-droite OE est la bissectrice de AOC.', [
        q('Quelle est la mesure de l’angle AOB ?', 'A, O et B sont alignés avec O entre A et B : l’angle est plat.', '180°.'),
        q('Calculer l’angle BOC.', 'AOC et BOC sont adjacents et forment un angle plat : soustraire l’angle connu à 180°.', f'{180-angle}°.', m(f'180-{angle}={180-angle}')),
        q('Calculer l’angle BOD.', 'Les demi-droites OA et OB sont opposées, tout comme OC et OD : AOC et BOD sont opposés par le sommet.', f'{angle}°.'),
        q('Calculer l’angle AOD.', 'AOD est opposé par le sommet à BOC ; il a donc la même mesure.', f'{180-angle}°.'),
        q('Calculer les angles AOE et EOC.', 'Une bissectrice partage un angle en deux angles de même mesure.', m(n(F(angle,2)))+'° chacun.', m(rf'{angle}\div2={n(F(angle,2))}'), f'2*F("{F(angle,2)}") == {angle}'),
        q('Vérifier que les quatre angles autour de O forment un tour complet.', 'Un tour complet mesure 360° : additionner les quatre angles adjacents, sans ajouter à nouveau les demi-angles de la bissectrice.', m(f'{angle}+{180-angle}+{angle}+{180-angle}=360')+'°.')],
        'Dans le nom d’un angle à trois lettres, la lettre du milieu est le sommet. Distinguer angles opposés, adjacents et supplémentaires.',
        dict(type='intersect',angle=angle),True)


def triangles(i,niveau):
    if i%3==1:
        base=6+2*i
        hauteur=3+niveau
        aire=F(base*hauteur,2)
        return ex('La médiane du jardin triangulaire',
            f'Le triangle ABC a une base BC de {base} m. La hauteur AH relative à BC mesure {hauteur} m. M est le milieu de BC. On trace AM. Le dessin est un schéma ; seules les longueurs indiquées font foi.', [
            q('Que signifie « AH est la hauteur relative à BC » ?', 'Une hauteur passe par un sommet et est perpendiculaire à la droite portant le côté opposé.', 'A appartient à AH, H appartient à (BC), et (AH) est perpendiculaire à (BC).'),
            q('Calculer l’aire du triangle ABC.', 'Prendre la base et la hauteur associée, dans la même unité ; diviser le produit par 2.', m(n(aire))+' m².', m(rf'\frac{{{base}\times {hauteur}}}{{2}}={n(aire)}'), f'F({base}*{hauteur},2) == F("{aire}")'),
            q('Calculer BM et MC.', 'M est le milieu : les deux demi-bases sont égales à la moitié de BC.', f'BM = MC = {base//2} m.'),
            q('Quel nom donne-t-on à la droite AM ?', 'Une droite passant par un sommet et par le milieu du côté opposé est une médiane.', 'La médiane issue de A.'),
            q('Démontrer que ABM et ACM ont la même aire et calculer cette aire.', 'Ils ont des bases BM et MC égales et la même hauteur issue de A. Leurs aires sont donc égales et se partagent l’aire totale.', m(n(aire/2))+' m² chacun.', m(rf'\frac{{{base//2}\times {hauteur}}}{{2}}={n(aire/2)}')),
            q('AM est-elle nécessairement perpendiculaire à BC ? Justifier.', 'Une médiane est définie par un milieu, une hauteur par une perpendicularité. Ces deux conditions ne sont pas équivalentes dans un triangle quelconque.', 'Non. Le fait que M soit le milieu n’impose pas que AM soit une hauteur.')],
            'La hauteur doit correspondre à la base choisie. Une médiane partage l’aire en deux parts égales, mais ne mesure pas nécessairement une hauteur.',
            dict(type='triangle_area',base=base,height=hauteur),True)
    a,b=35+5*i,45+5*niveau
    c=180-a-b
    return ex('Construire un triangle en vraie grandeur',
        f'On veut construire le triangle ABC avec AB = {5+niveau} cm, l’angle BAC = {a}° et l’angle ABC = {b}°. Une figure de travail à main levée est fournie ; elle n’est pas à mesurer.', [
        q('Calculer l’angle ACB.', 'La somme des angles d’un triangle vaut 180°. Enlever la somme des deux angles connus.', f'{c}°.', m(f'180-({a}+{b})={c}'), f'{a}+{b}+{c} == 180'),
        q('Le triangle a-t-il un angle obtus ?', 'Comparer chacune des trois mesures à 90° ; un angle obtus est strictement supérieur à 90°.', ('Oui.' if max(a,b,c)>90 else 'Non, aucun angle ne dépasse 90°.')),
        q('Quelle est la première étape de construction ?', 'Commencer par le côté dont la longueur est connue ; ses extrémités serviront à placer les deux angles.', f'Tracer le segment AB de {5+niveau} cm avec une règle graduée.'),
        q('Comment placer le sommet C ?', 'Au rapporteur, tracer en A et en B les demi-droites faisant les angles donnés avec AB et BA, dans le même demi-plan.', f'C est leur point d’intersection ; utiliser {a}° en A et {b}° en B.'),
        q('Comment construire le centre du cercle circonscrit ?', 'Les points d’une médiatrice sont équidistants des deux extrémités du segment. L’intersection de deux médiatrices est à égale distance des trois sommets.', 'Tracer les médiatrices de deux côtés ; leur intersection O est le centre du cercle passant par A, B et C.'),
        q('Le dessin de travail peut-il servir à vérifier les longueurs en vraie grandeur ? Comment contrôler la construction ?', 'Un schéma indique des relations et des données, pas une échelle fiable. Contrôler la construction obtenue avec les instruments.', f'Non : vérifier AB = {5+niveau} cm et les angles {a}°, {b}° puis {c}° sur la construction en vraie grandeur.')],
        'Un calcul d’angle permet de préparer une construction ; une propriété permet de justifier. Une mesure sur un schéma ne constitue pas une preuve.',
        dict(type='triangle_angles',a=a,b=b,base=5+niveau),True)


def symetries(i,niveau):
    x,y=2+i,1+niveau
    axial=i%2==1
    xp,yp=(-x,y) if axial else (-x,-y)
    return ex('Un motif et son image',
        f'Dans un repère orthogonal, A({x} ; {y}), B({x+2} ; {y}) et C({x} ; {y+2}) forment un triangle. On considère '+('la symétrie d’axe vertical passant par l’origine.' if axial else 'la symétrie centrale de centre O(0 ; 0).'), [
        q('Décrire la construction de l’image A′ du point A.', 'Symétrie axiale : l’axe est la médiatrice de AA′. Symétrie centrale : O est le milieu de AA′. Appliquer la définition correspondant à la transformation donnée.', ('Tracer la perpendiculaire à l’axe par A puis reporter la distance de l’autre côté de l’axe.' if axial else 'Tracer AO puis placer A′ de l’autre côté de O, avec OA′ = OA.')),
        q('Donner les coordonnées de A′.', 'Pour l’axe vertical, changer seulement le signe de l’abscisse. Pour le centre O, les deux coordonnées changent de signe.', f'A′({xp} ; {yp}).'),
        q('Donner les coordonnées de B′ et C′.', 'Appliquer à chacun des sommets la même règle de transformation ; conserver l’ordre abscisse puis ordonnée.', f'B′({-x-2} ; {y if axial else -y}) ; C′({-x} ; {y+2 if axial else -y-2}).'),
        q('Calculer A′B′ et A′C′.', 'La symétrie conserve les longueurs ; AB et AC sont ici des segments horizontaux ou verticaux de longueur 2.', 'A′B′ = A′C′ = 2 unités.'),
        q('Quelle est l’aire du triangle image ?', 'Le triangle de départ est rectangle en A, de côtés perpendiculaires 2 et 2. Une symétrie conserve les aires.', '2 unités d’aire.', m(r'\frac{2\times2}{2}=2'), 'F(2*2,2) == 2'),
        q('Que devient le motif si on applique encore une fois la même symétrie ?', 'Le second report ramène chaque point à sa position initiale : on vérifie la définition avec le même axe ou le même centre.', 'On retrouve exactement le triangle ABC.')],
        'Un demi-tour est une symétrie centrale ; un pliage selon une droite est une symétrie axiale. Les deux conservent les longueurs, les angles et les aires.',
        dict(type='symmetry',x=x,y=y,axial=axial),True)


def parallelogrammes(i,niveau):
    base,cote,h=6+i,4+niveau,2+niveau
    aire=base*h
    return ex('Un terrain en parallélogramme',
        f'ABCD est un parallélogramme. AB = {base} m, AD = {cote} m et la hauteur issue de D relative à AB mesure {h} m. Les diagonales se coupent en O. On veut clôturer le terrain et calculer sa surface.', [
        q('Donner BC et CD en justifiant.', 'Les côtés opposés d’un parallélogramme ont la même longueur.', f'BC = AD = {cote} m ; CD = AB = {base} m.'),
        q('Calculer le périmètre du terrain.', 'Additionner les quatre côtés, ou doubler la somme de deux côtés consécutifs.', f'{2*(base+cote)} m.', m(f'2({base}+{cote})={2*(base+cote)}'), f'2*({base}+{cote}) == {2*(base+cote)}'),
        q('Calculer l’aire du terrain.', 'Multiplier la base par la hauteur perpendiculaire associée, et non par le côté oblique AD.', f'{aire} m².', m(f'{base}\\times {h}={aire}'), f'{base}*{h} == {aire}'),
        q('Pourquoi AB × AD ne donne-t-il pas nécessairement l’aire ?', 'Dans un parallélogramme quelconque, AD est oblique. La hauteur mesure l’écartement perpendiculaire entre les côtés parallèles.', f'Il faudrait que AD soit une hauteur ; ici la hauteur donnée est {h} m et AD vaut {cote} m.'),
        q('Que peut-on affirmer sur AO et OC, puis sur BO et OD ?', 'Les diagonales d’un parallélogramme se coupent en leur milieu.', 'AO = OC et BO = OD ; O est le milieu des deux diagonales.'),
        q('La diagonale AC partage-t-elle le terrain en deux parties de même aire ? Calculer chacune.', 'Les triangles ABC et ACD ont une base commune AC ; on peut aussi utiliser la symétrie centrale de centre O qui échange ces deux triangles.', 'Oui : '+m(n(F(aire,2)))+' m² chacun.', m(rf'{aire}\div2={n(F(aire,2))}'))],
        'Ne pas confondre périmètre (longueur de clôture, en m) et aire (surface, en m²). Dans une aire, la hauteur est perpendiculaire à la base.',
        dict(type='parallelogram',base=base,side=cote,height=h),True)


def espace(i,niveau):
    if i%2:
        rayon,h=2+niveau,5+i
        base=rayon*rayon
        volume=base*h
        return ex('La boîte cylindrique',
            f'Une boîte cylindrique a un rayon intérieur de {rayon} cm et une hauteur intérieure de {h} cm. On néglige l’épaisseur du matériau. Donner d’abord les valeurs exactes avec π ; pour les approximations, prendre π ≈ 3,14.', [
            q('Calculer le diamètre de la base.', 'Le diamètre est le double du rayon.', f'{2*rayon} cm.'),
            q('Calculer le périmètre du disque de base.', 'Le contour d’un disque est un cercle : utiliser 2πr, à distinguer de la formule de l’aire.', m(f'{2*rayon}\\pi')+' cm, soit environ '+m(n(F(314,100)*2*rayon))+' cm.'),
            q('Calculer l’aire d’un disque de base.', 'L’aire du disque est π multiplié par le carré du rayon, et non par le carré du diamètre.', m(f'{base}\\pi')+' cm².', m(f'\\pi\\times {rayon}^2={base}\\pi')),
            q('Calculer le volume de la boîte.', 'Le volume d’un cylindre est l’aire de sa base multipliée par sa hauteur.', m(f'{volume}\\pi')+' cm³, soit environ '+m(n(F(314,100)*volume))+' cm³.', m(f'{base}\\pi\\times {h}={volume}\\pi'), f'{rayon}**2*{h} == {volume}'),
            q('Exprimer sa capacité en mL puis en L.', 'Un cm³ vaut 1 mL et 1 000 mL valent 1 L. Convertir le volume approché sans changer de forme de solide.', 'Environ '+m(n(F(314,100)*volume))+' mL, soit '+m(n(F(314,100)*volume/1000))+' L.'),
            q('Décrire les pièces d’un patron de ce cylindre fermé.', 'En déroulant la surface latérale, on obtient un rectangle dont la longueur est le tour de la base ; les deux bases restent des disques.', f'Deux disques de rayon {rayon} cm et un rectangle de hauteur {h} cm et de longueur '+m(f'{2*rayon}\\pi')+' cm.')],
            'Ne pas confondre contour (cm), aire (cm²) et volume (cm³). Une valeur exacte avec π se conserve jusqu’à la dernière étape.',
            dict(type='cylinder',radius=rayon,height=h),True)
    l,w,h=5+i,3+niveau,2+niveau
    volume=l*w*h
    return ex('Un aquarium en pavé droit',
        f'Un aquarium a des dimensions intérieures de {l} dm de longueur, {w} dm de largeur et {h} dm de hauteur. Il a la forme d’un pavé droit. On néglige l’épaisseur du verre.', [
        q('Combien le pavé droit a-t-il de faces, d’arêtes et de sommets ?', 'Compter de façon organisée : deux bases et quatre faces latérales ; quatre sommets par base et les arêtes entre les bases.', '6 faces, 12 arêtes, 8 sommets.'),
        q('Calculer l’aire de la base.', 'La base est un rectangle : multiplier longueur et largeur, dans la même unité.', f'{l*w} dm².', m(f'{l}\\times {w}={l*w}')),
        q('Calculer le volume intérieur total.', 'Un pavé droit est un prisme droit : multiplier l’aire de la base par la hauteur.', f'{volume} dm³.', m(f'{l}\\times {w}\\times {h}={volume}'), f'{l}*{w}*{h} == {volume}'),
        q('Exprimer la capacité de l’aquarium en litres.', 'Une capacité de 1 L correspond à un volume de 1 dm³ : les valeurs numériques sont ici les mêmes.', f'{volume} L.'),
        q('On remplit l’aquarium aux trois quarts de sa hauteur. Quelle quantité d’eau contient-il ?', 'La base reste la même ; le volume est proportionnel à la hauteur. Prendre les trois quarts du volume total.', m(n(F(3*volume,4)))+' L.', m(rf'{volume}\times\frac34={n(F(3*volume,4))}')),
        q('Exprimer le volume total en cm³ et expliquer le facteur de conversion.', '1 dm vaut 10 cm ; une unité de volume comporte trois dimensions : 10 × 10 × 10 = 1 000.', f'{volume*1000} cm³.', m(f'{volume}\\times 1000={volume*1000}'), f'{l}*10*{w}*10*{h}*10 == {volume*1000}')],
        'Un volume multiplie trois dimensions : chaque changement d’unité comporte un facteur 1 000. Retenir 1 dm³ = 1 L et 1 cm³ = 1 mL.',
        dict(type='cuboid',length=l,width=w,height=h),True)


BUILDERS={'angles':angles,'triangles':triangles,'symetries':symetries,
    'parallelogrammes':parallelogrammes,'espace':espace}
