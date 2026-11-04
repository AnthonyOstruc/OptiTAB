"""Mesures et constructions adaptées au primaire, avec critères de vérification."""
from fractions import Fraction as F
from config import GRADE
from modele_site import ex, m
from nombres import a,c,f,frac,NOMS

def mesures(i,l,kind='length'):
    factor,large,small,objet={
        'length':(100,'m','cm','ruban'),
        'mass':(1000,'kg','g','sac'),
        'capacity':(100,'L','cL','réservoir')}[kind]
    whole=2+i%3; extra=15+i*5+l*10;total=whole*factor+extra;used=factor+5+i
    if GRADE=='ce1' and kind=='mass':whole=1;extra=0;total=1000;used=100+i*25
    qty=f'{whole} {large} et {extra} {small}' if extra else f'{whole} {large}'
    return ex('Une mesure à suivre',f'Un {objet} contient une quantité de {qty}. Pour travailler, on utilise {used} {small}. Les données sont à interpréter dans une même unité.',[
        a(f'Quelle relation relie {large} et {small} ?','Je m’appuie sur une relation connue entre les deux unités.',f'1 {large} = {factor} {small}.',f'{factor}=={factor}'),
        c(f'Exprime la quantité initiale en {small}.','Je transforme les grandes unités, puis j’ajoute les petites unités.',f'{whole}*{factor}+{extra}',total,small),
        c(f'Combien de {small} reste-t-il après l’utilisation ?','Les mesures étant dans la même unité, je peux soustraire.',f'{total}-{used}',total-used,small),
        c(f'On ajoute encore {factor} {small}. Quelle est la quantité maintenant ?','J’ajoute la quantité reçue à celle qui restait.',f'{total-used}+{factor}',total-used+factor,small),
        a(f'Exprime cette dernière quantité avec des {large} entiers et le reste en {small}.','Je forme le plus de grandes unités complètes possible, puis je garde le reste.',f'{(total-used+factor)//factor} {large} et {(total-used+factor)%factor} {small}.',f'{(total-used+factor)//factor}*{factor}+{(total-used+factor)%factor}=={total-used+factor}'),
        c('Vérifie la quantité initiale à partir du reste après utilisation et de la quantité utilisée.','J’ajoute ce qui reste et ce qui a été utilisé.',f'{total-used}+{used}',total,small)],
        'Pour réunir, retirer ou comparer des mesures, je choisis d’abord une même unité.',dict(type='measure',kind=kind,initial=qty,used=f'{used} {small}',answer=f'{total-used} {small}'),True)

def perimetre(i,l,area=False):
    L=6+i+l*2;w=3+i%3+l
    perimeter=2*(L+w)
    qs=[a('Quelles sont les longueurs des quatre côtés ?','Dans un rectangle, les côtés opposés ont la même longueur.',f'{L} cm ; {w} cm ; {L} cm ; {w} cm.'),
        a('Écris une addition pour trouver la longueur du contour.','Je parcours le contour sans oublier de côté.',m(f'{L}+{w}+{L}+{w}')+' cm.'),
        c('Calcule ce périmètre.','J’additionne toutes les longueurs du contour.',f'{L}+{w}+{L}+{w}',perimeter,'cm')]
    if area:
        qs += [c('Combien de carrés de 1 cm² recouvrent une rangée ?','Une rangée contient un carré par centimètre de longueur.',str(L),L,'carrés'),
            c('Quelle est l’aire du rectangle ?','Je compte les carrés par rangée puis le nombre de rangées.',f'{L}*{w}',L*w,'cm²'),
            c('On ajoute une bande de 1 cm à la largeur, sans changer la longueur. Quelle est la nouvelle aire ?','Il y a une rangée complète de plus.',f'{L}*({w}+1)',L*(w+1),'cm²')]
    else:
        qs += [c('On laisse une ouverture de 2 cm dans le contour. Quelle longueur faut-il border ?','Je retire uniquement la longueur de l’ouverture.',f'{perimeter}-2',perimeter-2,'cm'),
            c('Deux rectangles identiques doivent être entièrement bordés. Quelle longueur faut-il ?','Chaque rectangle demande un contour complet.',f'{perimeter}*2',perimeter*2,'cm'),
            a('Peut-on trouver le contour en additionnant seulement la longueur et la largeur ?','Je vérifie que chaque côté a été compté une fois.','Non : cela ne compte que deux côtés. Il reste les deux côtés opposés, de mêmes longueurs.')]
    return ex('Le cadre rectangulaire',f'Un rectangle mesure {L} cm de longueur et {w} cm de largeur. Le dessin représente la forme ; utilise les longueurs indiquées.',qs,
        'Le périmètre mesure le contour en cm. L’aire mesure la surface en cm².' if area else 'Le périmètre est la longueur de tout le contour ; chaque côté est compté une fois.',dict(type='rectangle',length=L,width=w,grid=area),True)

def aires_angles(i,l):
    cols=3+i%4;rows=2+l;other=cols*rows-1
    return ex('Recouvrir deux surfaces',f'Chaque petit carré du quadrillage est la même unité d’aire. La figure A est un rectangle de {cols} colonnes et {rows} rangées ; la figure B est ce rectangle auquel on a retiré un seul carré dans un coin.',[
        c('Combien de carrés contient une rangée de A ?','Je compte les carrés dans une seule ligne du quadrillage.',str(cols),cols,'carrés'),
        c('Combien de rangées contient A ?','Je compte les lignes de carrés.',str(rows),rows,'rangées'),
        c('Combien d’unités d’aire couvre A ?','Je compte tous les carrés, rangée après rangée.',f'{cols}*{rows}',cols*rows,'unités d’aire'),
        c('Combien d’unités d’aire couvre B ?','Un seul carré a été retiré de la surface de A.',f'{cols*rows}-1',other,'unités d’aire'),
        a('Quelle figure possède la plus grande aire ? De combien ?','Je compare les nombres de carrés de même taille.',f'A possède une unité d’aire de plus que B.',f'{cols*rows}-{other}==1'),
        a('Les angles aux coins du rectangle A sont-ils aigus, droits ou obtus ?','Je peux superposer le coin d’une équerre à chaque coin du rectangle.','Les quatre angles sont droits. La longueur des côtés ne change pas cette propriété.')],
        'Pour comparer des aires par comptage, les carreaux doivent avoir la même taille.',dict(type='area',cols=cols,rows=rows),True)

def angles(i,l):
    return ex('Contrôler les coins d’un dessin','Observe les trois angles A, B et C. Pour vérifier, reproduis leur forme sur une feuille et utilise une équerre ou un gabarit d’angle droit.',[
        a('Quel instrument permet de repérer un angle droit ?','Je cherche un instrument possédant un coin de référence.','Une équerre ou un gabarit d’angle droit obtenu par pliage.'),
        a('Quel angle est plus petit qu’un angle droit ?','Je compare son ouverture au coin de l’équerre.','A est plus petit : c’est un angle aigu.'),
        a('Quel angle est droit ?','Les deux côtés doivent suivre les deux bords perpendiculaires du gabarit.','B est un angle droit.'),
        a('Quel angle est plus grand qu’un angle droit ?','Je compare l’ouverture, sans me laisser tromper par la longueur des côtés.','C est plus grand : c’est un angle obtus.'),
        a('Si on prolonge les côtés de A, devient-il plus grand ?','Un angle décrit une ouverture, pas la longueur de ses côtés.','Non. L’ouverture reste la même : A reste aigu.'),
        a('Au CM2, quelle mesure en degrés connaît-on pour un angle droit ?','Je relie le gabarit d’angle droit à la mesure de référence.','Un angle droit mesure 90°.')],
        'Je compare l’ouverture des angles. La longueur et l’orientation des côtés ne donnent pas leur nature.',dict(type='angles',variant=i+l),True)

def durees(i,l,clock=False):
    if GRADE=='ce1':h=8+i;m0=[0,15,30,45,0,15,30][i];duration=[30,45,60][l]
    else:h=8+i;m0=12+i*3;duration=35+l*27+i
    start=h*60+m0;end=start+duration;eh,em=divmod(end,60)
    pause=10+l*5
    def heure(t):hh,mm=divmod(t,60);return f'{hh} h {mm:02}'
    qs=[a('Quelle est l’heure de départ ?','Je lis les heures puis les minutes ; sur l’horloge, la grande aiguille indique les minutes.',heure(start)+'.'),
        c('Combien de minutes séparent le départ de l’heure pleine suivante ?','Je complète les minutes jusqu’à 60.',f'60-{m0}',60-m0,'min'),
        a(f'À quelle heure finit l’activité de {duration} minutes ?','J’avance sur la ligne du temps ; 60 minutes forment une heure.',heure(end)+'.',f'{start}+{duration}=={end}'),
        a(f'Après une pause de {pause} minutes, à quelle heure reprend-on ?','Je pars de la fin de l’activité et j’ajoute la durée de la pause.',heure(end+pause)+'.',f'{end}+{pause}=={end+pause}'),
        c('Quelle durée s’est écoulée du départ jusqu’à la reprise ?','J’additionne la durée de l’activité et celle de la pause.',f'{duration}+{pause}',duration+pause,'min'),
        c('Exprime la durée de l’activité en secondes.','Une minute contient 60 secondes.',f'{duration}*60',duration*60,'s') if GRADE=='cm2' else a('Pourquoi 1 h 30 ne signifie-t-il pas 130 minutes ?','Je remplace une heure par sa durée en minutes.','1 h 30 min = 60 min + 30 min = 90 min.', '60+30==90')]
    return ex('Le programme de la matinée',f'Une activité commence à {heure(start)} et dure {duration} minutes. Toutes les activités ont lieu le même jour.',qs,
        'Une heure contient 60 minutes ; je passe par les heures pleines quand cela simplifie le calcul.',dict(type='clock' if clock else 'timeline',hour=h,minute=m0,duration=duration,answer=heure(end)),True)

def construction(i,l):
    r=2+i%4;diam=2*r
    return ex('Construire une roue',f'Sur une feuille, trace un segment [AB] de {diam} cm. Marque son milieu O. Le dessin est un schéma : réalise les mesures avec tes instruments.',[
        a('Comment placer le milieu O ?','Je cherche la moitié de la longueur totale en partant d’une extrémité.',f'Placer O sur [AB] à {r} cm de A et à {r} cm de B.',f'{diam}//2=={r}'),
        a('Que valent AO et OB ?','Le milieu partage le segment en deux segments de même longueur.',f'AO = OB = {r} cm.'),
        a('Comment tracer le cercle de centre O passant par A ?','Je garde fixe le centre et je conserve la même ouverture du compas.',f'Piquer le compas en O, ouvrir jusqu’à A ({r} cm), puis tracer le cercle.'),
        a('Le point B appartient-il à ce cercle ? Justifie.','Je compare OB au rayon OA.',f'Oui : OB = OA = {r} cm. B est à la distance voulue du centre.'),
        a('Quel rôle joue [AB] dans ce cercle ?','Le segment relie deux points du cercle et passe par son centre.',f'[AB] est un diamètre, de longueur {diam} cm.'),
        a('Un point C se trouve à 1 cm de O. Est-il sur ce cercle ?','Je compare la distance OC au rayon, sans juger seulement à l’œil.',f'Non : le rayon mesure {r} cm. Comme 1 < {r}, C se trouve à l’intérieur.',f'1<{r}')],
        'Tous les points d’un cercle sont à la même distance de son centre. Un diamètre vaut deux rayons.',dict(type='circle',radius=r),True)

def polygones(i,l):
    cm2=GRADE=='cm2';names=['triangle','quadrilatère','pentagone','hexagone'] if cm2 else ['triangle','rectangle','carré','losange']
    return ex('L’atelier des figures', 'Observe les quatre figures A, B, C et D. Les petits carrés codent les angles droits ; les mêmes traits sur les côtés codent des longueurs égales.',[
        a('Combien de côtés et de sommets possède A ?','Je suis le contour et je compte chaque segment et chaque coin une fois.','A possède 3 côtés et 3 sommets : c’est un triangle.'),
        a('Quel est le nom de B ? Qu’observes-tu ?','Je compte d’abord les côtés ; je lis ensuite les codes.', 'B est un quadrilatère : 4 côtés et 4 sommets.' if cm2 else 'B est un rectangle : 4 angles droits et des côtés opposés de même longueur.'),
        a('Quel est le nom de C ? Justifie.','Je relie le nombre de côtés ou les propriétés codées au nom de la figure.','C est un pentagone : 5 côtés.' if cm2 else 'C est un carré : 4 côtés de même longueur et 4 angles droits.'),
        a('Quel est le nom de D ? Justifie.','Je compte les côtés et je regarde leurs codes.','D est un hexagone : 6 côtés.' if cm2 else 'D est un losange : ses 4 côtés sont de même longueur.'),
        a('Si on tourne la feuille, les noms des figures changent-ils ?','Je vérifie ce qui reste pareil quand on change l’orientation.','Non : le nombre de côtés, les longueurs et les angles restent les mêmes.'),
        a('Peut-on appeler un cercle un polygone ?','Un polygone doit être fermé et composé uniquement de segments.','Non : le contour d’un cercle est courbe ; il n’est pas composé de côtés droits.')],
        'Je décris les propriétés et les codes avant de nommer une figure ; son orientation ne change pas sa nature.',dict(type='polygons',cm2=cm2,rotation=(i+l)%3),True)

def symetrie(i,l):
    distance=1+i%3; horizontal=l==1;diagonal=GRADE=='cm2' and l==2
    axis='oblique' if diagonal else 'horizontal' if horizontal else 'vertical'
    return ex('Un dessin à compléter par pliage',f'Le dessin présente un triangle et un axe {axis}. Reproduis le quadrillage sur une feuille. Chaque carreau a la même taille.',[
        a('Que doit-il se passer si on plie sur l’axe ?','Le pliage donne le sens du mot symétrique.','La figure et son image doivent se superposer exactement.'),
        a('Où placer l’image A′ du point A ?','Je compte les carreaux jusqu’à l’axe, puis je reporte de l’autre côté ; pour un axe oblique, je suis la direction perpendiculaire à l’axe.','Voir A′ sur le corrigé : il est de l’autre côté, à la même distance de l’axe que A.'),
        a('Place de la même façon les images B′ et C′.','Je reporte chaque sommet séparément avant de tracer les côtés.','Les points B′ et C′ sont indiqués en vert dans le corrigé.'),
        a('Dans quel ordre relier les points images ?','Je conserve les voisinages des sommets du triangle de départ.','Relier A′ à B′, B′ à C′ puis C′ à A′.'),
        a('Que devient un point situé exactement sur l’axe ?','Lors du pliage, un point du pli ne se déplace pas.','Son image est le point lui-même : il reste sur l’axe.'),
        a('Les longueurs des côtés sont-elles conservées ? Comment le vérifier ?','Je superpose par pliage ou je compare les longueurs sur le quadrillage.','Oui. Le triangle et son image ont les mêmes longueurs et les mêmes angles.')],
        'Je reporte les sommets de part et d’autre de l’axe avant de relier leurs images.',dict(type='symmetry',axis=axis,offset=distance),True)

def solides(i,l):
    edge=2+i%4
    return ex('Fabriquer une boîte cubique',f'On veut fabriquer un cube dont chaque arête mesure {edge} cm. Le dessin montre une boîte et un patron possible.',[
        a('Quelle est la forme d’une face du cube ?','Toutes les faces d’un cube ont la même forme et les mêmes dimensions.',f'Un carré de côté {edge} cm.'),
        a('Combien de faces possède le cube ?','Je compte le dessus, le dessous et les quatre faces autour.','6 faces.', '2+4==6'),
        a('Combien d’arêtes possède-t-il ?','Je compte 4 arêtes en haut, 4 en bas et 4 qui les relient.','12 arêtes.', '4+4+4==12'),
        a('Combien de sommets possède-t-il ?','Je compte les 4 coins de la face du haut et les 4 du bas.','8 sommets.', '4+4==8'),
        c('Quelle longueur totale de baguette faut-il pour construire toutes ses arêtes ?','Chaque arête doit être fabriquée une fois.',f'12*{edge}',12*edge,'cm'),
        a('Pourquoi six carrés alignés ne forment-ils pas un patron de cube ?','Je dois pouvoir fermer le cube par pliage sans trou ni superposition.','Une bande de six carrés ne peut pas former les six faces autour de la boîte. Les carrés doivent être disposés pour se replier dans toutes les directions.')],
        'Une face est une surface, une arête est un segment, un sommet est un coin.',dict(type='solid',edge=edge),True)

def plan(i,l):
    x=1+i%3;y=1;right=2+l;up=2;endx=x+right;endy=y+up
    return ex('Guider le petit robot',f'Le robot part de D sur le quadrillage, tourné vers la droite de la feuille. Une instruction « avancer » fait parcourir un seul carreau. On lui demande : avancer {right} fois, tourner à gauche d’un quart de tour, avancer {up} fois.',[
        a('Dans quelle direction se déplace-t-il au début ?','Je lis l’orientation annoncée au départ.','Vers la droite de la feuille.'),
        c('Combien de carreaux parcourt-il avant de tourner ?','Je compte les premières instructions « avancer ».',str(right),right,'carreaux'),
        a('Vers quel côté de la feuille regarde-t-il après le quart de tour à gauche ?','Je me place mentalement à la place du robot orienté vers la droite.','Vers le haut de la feuille.'),
        c('Combien de carreaux parcourt-il en tout ?','Je réunis les déplacements horizontaux et verticaux.',f'{right}+{up}',right+up,'carreaux'),
        a('Indique sa case d’arrivée sur ton dessin.','Je suis chaque instruction dans l’ordre sans déplacer le point de départ.',f'Il arrive {right} carreaux à droite et {up} carreaux au-dessus de D. La case est indiquée dans le corrigé.'),
        a('Comment revenir au départ en suivant le même chemin en sens inverse ?','Je retourne le sens et l’ordre des déplacements.','Faire demi-tour, avancer 2 carreaux, tourner à droite d’un quart de tour, puis avancer '+str(right)+' carreaux.')],
        'Un trajet doit préciser le départ, l’orientation et la longueur d’un pas.',dict(type='path',start=[x,y],right=right,up=up),True)
