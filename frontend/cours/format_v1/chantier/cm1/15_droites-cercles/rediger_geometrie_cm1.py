"""Rédaction CM1 : quatre chapitres attribués, sources conservées."""
from pathlib import Path
import json, re, hashlib
BASE=Path(__file__).resolve().parent.parent
DOS={n:next(BASE.glob(f'{n:02}_*')) for n in (15,16,17,18)}
DATA={n:[] for n in DOS};FIG={n:{} for n in DOS};COR={n:{'cours':{'nouveau':{}},'fiches':{'nouvelle':{}},'exercices':{}} for n in DOS}
def ex(n,title,context,rows,images=(),correction=()):
    assert len(rows)>=5
    DATA[n].append(dict(titre=title,contexte=context,questions=[dict(zip(('question','methode','raisonnement','reponse'),row)) for row in rows],images=list(images),correction=list(correction)))
def row(q,a,r,m='Utiliser la définition et les informations données.'):
    return(q,m,r,a)
def fig(n,name,body,alt):FIG[n][name]='\\begin{tikzpicture}[font=\\large,line cap=round,line join=round]'+body+'\\end{tikzpicture}';return name
def label(x,y,t,anchor='center',color='otInk'):
    return rf'\node[anchor={anchor},text={color},inner sep=4pt] at ({x},{y}) {{{t}}};'
def dots(points,color='otNavy',grille=False):
    return ''.join(rf'\fill[{color}] ({x},{y}) circle(1.7pt);'+label(x+(-.275 if grille=='gauche' else .275 if grille else 0),y,'$'+t+'$' if re.fullmatch('[A-Z][′]?',t) else t,a,color) for x,y,t,a in points)
def entry(n,name):return {'fichier':name+'.png','alt':ALT[n][name]}
ALT={n:{} for n in DOS}
def addfig(n,name,body,alt):fig(n,name,body,alt);ALT[n][name]=alt

# Droites et cercles : les énoncés nomment toujours l'objet avant son symbole.
ex(15,'Les bons noms','Sur ton cahier, place six points distincts A, B, C, D, E et F. Les notations ci-dessous sont expliquées dans les questions.',[
 row('Trace le segment [AB] : que représentent A et B ?','A et B sont les deux extrémités du segment.','Le segment est la portion de droite limitée par les deux points ; le trait s’arrête en A et en B.'),
 row('Trace la droite (CD). Doit-elle s’arrêter en C ou en D ?','Non : la droite se prolonge des deux côtés.','C et D donnent sa direction, mais ne sont pas ses extrémités. Sur la feuille, le dessin représente seulement une partie de la droite.'),
 row('Trace la demi-droite [EF), qui part de E et passe par F. Quelle est son origine ?','Son origine est E.','On commence le trait en E, puis on le prolonge au-delà de F, dans cette direction.'),
 row('Avec quel instrument tracer ces trois objets bien droits ?','Avec une règle.','On maintient la règle en place et on trace le long de son bord sans déplacer les points.'),
 row('La longueur du segment [AB] s’écrit AB. Est-ce une droite ou une mesure ?','AB désigne une longueur, donc une mesure.','Les lettres servent ici à nommer la distance entre les points. On accompagne la valeur d’une unité, par exemple 4 cm.')])
ex(15,'Le milieu du segment','Trace un segment [AB] de 7 cm. On veut placer son milieu M.',[
 row('Quelle longueur faut-il partager en deux ?','La longueur AB de 7 cm.','Le milieu partage le segment entier en deux parties de même longueur.'),
 row('Calcule AM.','$AM=3{,}5$ cm.',r'$7\div2=3{,}5$. Cette moitié de la longueur est la distance de A au milieu.'),
 row('Où places-tu M avec la règle graduée ?','Sur le segment, à 3,5 cm de A.','Place le zéro de la règle en A. Marque M à 3,5 cm, sur le trait qui joint A et B.'),
 row('Quelle doit être la longueur MB ?','$MB=3{,}5$ cm.',r'$7-3{,}5=3{,}5$. Les deux parties ont bien la même longueur.'),
 row('Un point placé à 3,5 cm de A mais hors du segment est-il son milieu ?','Non : le milieu doit aussi appartenir au segment.','La distance à A seule ne suffit pas : le point doit être situé entre A et B, sur le segment.')],correction=('milieu',))
ex(15,'Perpendiculaires ou simplement sécantes','Observe les deux paires de droites : un angle droit est codé dans la paire 1. Dans la paire 2, l’ouverture est plus petite que celle de l’équerre.',[
 row('Quelle paire est perpendiculaire ?','La paire 1.','Le petit carré code un angle droit entre les deux droites.'),
 row('Les droites de la paire 2 se coupent-elles ?','Oui, elles se coupent.','Elles ont un point commun : on dit qu’elles sont sécantes.'),
 row('La paire 2 est-elle perpendiculaire ?','Non : son ouverture n’est pas un angle droit.','Se couper ne suffit pas. Il faut que l’angle corresponde exactement à l’angle droit de l’équerre.'),
 row('Quel instrument permet le contrôle ?','L’équerre.','Place son sommet au croisement et un côté sur une droite ; l’autre côté doit suivre la seconde.'),
 row('Une paire inclinée peut-elle être perpendiculaire ?','Oui : l’orientation sur la feuille ne change pas l’angle droit.','Tourne l’équerre pour l’adapter au dessin. Des droites perpendiculaires n’ont pas besoin d’être horizontale et verticale.')],images=('angles_droites',))
ex(15,'Parallèles à vérifier','Sur le dessin, les droites (a) et (b) sont toutes deux perpendiculaires à la même droite (f). La droite (c) coupe (a).',[
 row('Quelles droites sont parallèles ?','Les droites (a) et (b).','On utilise les deux angles droits avec la même droite (f), et non une simple impression visuelle.'),
 row('Les droites (a) et (c) sont-elles parallèles ?','Non : elles se coupent.','Deux droites parallèles distinctes ne se rencontrent pas, même si on les prolonge.'),
 row('Quel instrument contrôle les angles droits du dessin ?','L’équerre.','On la place successivement aux deux croisements avec (f).'),
 row('Les droites (a) et (b) se couperaient-elles en les prolongeant ?','Non : elles restent parallèles.','Le parallélisme concerne les droites entières, pas seulement les portions visibles.'),
 row('Deux traits qui ne se coupent pas sur une petite feuille sont-ils forcément parallèles ?','Non : ils peuvent se couper plus loin.','Il faut contrôler la direction avec les instruments ; l’absence de croisement sur le dessin ne suffit pas.')],images=('paralleles',))
ex(15,'Le vocabulaire du cercle','Observe le cercle de centre O. Les points A, B et C sont sur le cercle ; B, O et C sont alignés.',[
 row('Quel point est le centre ?','O.','Le centre est le point situé à la même distance de tous les points du cercle.'),
 row('Nomme le rayon vertical tracé.','Le segment [OA].','Un rayon relie le centre à un point du cercle.'),
 row('Nomme le diamètre horizontal tracé.','Le segment [BC].','Ses extrémités sont sur le cercle et il passe par le centre O.'),
 row('Si OA mesure 3 cm, combien mesure OB ?','$OB=3$ cm.','Les deux segments sont des rayons du même cercle ; ils ont donc la même longueur.'),
 row('Quelle est alors la longueur BC ?','$BC=6$ cm.',r'$3+3=6$. Le diamètre réunit deux rayons alignés.')],images=('cercle',))
ex(15,'Tracer une perpendiculaire','Trace une droite (d), puis place un point A à l’extérieur de cette droite.',[
 row('Quel instrument faut-il ajouter à la règle ?','Une équerre.','L’équerre fournit l’angle droit ; la règle seule ne garantit pas la perpendicularité.'),
 row('Quel côté de l’équerre poses-tu sur (d) ?','Un des deux côtés de son angle droit.','Le bord opposé à l’angle droit ne permet pas cette construction directement.'),
 row('Comment faire passer l’autre côté par A ?','Faire glisser l’équerre en gardant son premier côté sur (d).','Le mouvement conserve l’angle droit avec (d). On s’arrête quand le second bord passe par A.'),
 row('Trace la droite obtenue et indique sa propriété.','La droite tracée passe par A et est perpendiculaire à (d).','Trace le long du second bord et prolonge si nécessaire. Vérifie le passage par A et l’angle droit.'),
 row('Quel code ajoutes-tu au croisement ?','Un petit carré d’angle droit.','Le code signale la propriété vérifiée, même quand le dessin est reproduit à main levée.')])
ex(15,'Tracer une parallèle','Trace une droite (d), puis place un point B à l’extérieur de (d). Prépare une règle et une équerre.',[
 row('Quelle relation veut-on entre la nouvelle droite et (d) ?','Les deux droites doivent être parallèles.','La nouvelle droite doit garder la direction de (d) tout en passant par B.'),
 row('Comment places-tu les deux instruments ?','Un bord de l’équerre sur (d), et la règle contre un autre bord de l’équerre.','La règle servira de rail pour guider le déplacement sans faire tourner l’équerre.'),
 row('Quel instrument maintiens-tu immobile pendant le glissement ?','La règle.','Tiens fermement la règle et fais coulisser l’équerre le long de ce rail.'),
 row('À quel moment arrêtes-tu le glissement ?','Quand le bord de tracé de l’équerre passe par B.','Le bord a gardé sa direction depuis (d). Trace alors la parallèle le long de ce bord.'),
 row('Que contrôles-tu sur ta construction ?','Le passage par B et le parallélisme avec (d).','Reprends le glissement des instruments dans l’autre sens. La direction doit coïncider avec celle de (d).')])
ex(15,'Rayons et diamètres','Pour chaque cercle, on connaît soit le rayon, soit le diamètre.',[
 row('Le rayon du cercle 1 mesure 4 cm. Calcule son diamètre.','8 cm.',r'$4\times2=8$ : un diamètre mesure deux rayons.'),
 row('Le diamètre du cercle 2 mesure 7 cm. Calcule son rayon.','3,5 cm.',r'$7\div2=3{,}5$ : un rayon est la moitié d’un diamètre.'),
 row('Le rayon du cercle 3 mesure 25 mm. Calcule son diamètre.','50 mm.',r'$25\times2=50$. On conserve ici les millimètres.'),
 row('Le diamètre du cercle 4 mesure 12 cm. À quelle ouverture règles-tu le compas ?','À 6 cm.',r'$12\div2=6$. L’ouverture du compas correspond au rayon, pas au diamètre.'),
 row('Un élève ouvre son compas à 8 cm pour un diamètre demandé de 8 cm. Quel diamètre obtiendra-t-il ?','16 cm.',r'$8\times2=16$. Son rayon serait de 8 cm : il aurait fallu ouvrir à 4 cm.')])
ex(15,'Lire les codes sans inventer','Le triangle ABC porte le même petit trait sur les segments [AB] et [AC], et un carré d’angle droit en A. Aucune longueur n’est indiquée.',[
 row('Quelles longueurs sont égales ?','$AB=AC$.','Les petits traits identiques signalent cette égalité.'),
 row('Quel angle est droit ?','L’angle formé en A par les côtés [AB] et [AC].','Le carré est placé au sommet A, entre ces deux côtés.'),
 row('Quel instrument contrôlerait l’égalité des deux longueurs ?','Le compas, ou la règle graduée.','On reporte l’ouverture AB sur AC, ou on compare les deux mesures.'),
 row('Peut-on affirmer que BC mesure 5 cm ?','Non : aucune mesure ne permet de l’affirmer.','Les codes donnent une égalité et un angle droit, mais aucune longueur numérique.'),
 row('Que doit-on conserver en reproduisant ce triangle ?','L’angle droit en A et l’égalité AB = AC.','Ce sont les deux contraintes annoncées. Choisir une longueur pour AB puis la reporter sur AC suffit à les respecter.')])
ex(15,'À 3 cm du puits','Sur un plan, le puits est représenté par le point O. Les distances indiquées sont celles mesurées sur le plan.',[
 row('Quel instrument permet de placer tous les points à exactement 3 cm de O ?','Le compas ouvert à 3 cm.','La pointe reste en O pendant que la mine décrit les points à cette distance.'),
 row('Quelle figure forme cet ensemble de points ?','Le cercle de centre O et de rayon 3 cm.','Tous les points tracés sont à exactement 3 cm du centre.'),
 row('Un point P à 2 cm de O est-il sur ce cercle ?','Non : il est à l’intérieur.','Sa distance au centre est plus petite que le rayon, donc il n’appartient pas au bord.'),
 row('Un point Q à 4 cm de O est-il dans le disque ?','Non : il est à l’extérieur.','Sa distance au centre dépasse 3 cm. Le disque contient l’intérieur et le cercle.'),
 row('Comment colorier les points situés à 3 cm ou moins de O ?','Colorier tout le disque, y compris son bord.','Le mot « ou moins » ajoute l’intérieur aux points du cercle.')],correction=('disque',))
ex(15,'Un programme à exécuter','Construis un rectangle ABCD tel que AB mesure 5 cm et BC mesure 3 cm. Place ensuite le milieu M du côté [AB], puis le cercle de centre A passant par M.',[
 row('Quels instruments utilises-tu pour le rectangle ?','La règle graduée et l’équerre.','La règle donne les longueurs ; l’équerre permet de construire et de contrôler les quatre angles droits.'),
 row('Quelle longueur dois-tu reporter sur le côté [AD] ?','3 cm.','Les côtés opposés d’un rectangle ont la même longueur : AD et BC sont égaux.'),
 row('Calcule AM.','$AM=2{,}5$ cm.',r'$5\div2=2{,}5$ : M est le milieu du côté de 5 cm.'),
 row('À quelle ouverture règles-tu le compas pour le cercle demandé ?','À 2,5 cm.','Le cercle a pour centre A et passe par M : son rayon est la longueur AM.'),
 row('Calcule le diamètre de ce cercle.','5 cm.',r'$2{,}5\times2=5$. Le diamètre mesure deux fois le rayon.')],correction=('programme',))
ex(15,'Deux cercles croisés','Trace le segment [AB] de 4 cm. Trace deux cercles de rayon 3 cm, l’un de centre A, l’autre de centre B. Appelle C et D leurs deux points de rencontre.',[
 row('Quelle ouverture de compas utilises-tu pour les deux cercles ?','3 cm.','Les rayons demandés sont identiques, donc on conserve la même ouverture.'),
 row('Quelle est la longueur AC ?','3 cm.','C appartient au cercle de centre A et de rayon 3 cm.'),
 row('Quelle est la longueur BC ?','3 cm.','C appartient aussi au cercle de centre B : sa distance à B est donc le même rayon.'),
 row('Quelles sont les longueurs AD et BD ?','$AD=BD=3$ cm.','D est lui aussi situé sur chacun des deux cercles.'),
 row('C est-il le milieu du segment [AB] ?','Non : C n’est pas sur le segment [AB].','Être à égale distance des extrémités ne suffit pas. Le milieu doit aussi être situé sur le segment.')],correction=('croises',))
ex(15,'Reproduire sur quadrillage','Le rectangle ABCD a un côté horizontal de 5 carreaux et un côté vertical de 3 carreaux. Ses sommets sont nommés dans l’ordre ; A est en bas à gauche. Sa diagonale relie A à C.',[
 row('À partir de A, comment places-tu B ?','5 carreaux vers la droite.','A et B sont les deux extrémités du côté horizontal inférieur.'),
 row('À partir de B, comment places-tu C ?','3 carreaux vers le haut.','On suit le côté vertical droit du rectangle.'),
 row('À partir de A, comment places-tu D ?','3 carreaux vers le haut.','Le côté vertical gauche a la même longueur que le côté droit.'),
 row('Quels points relies-tu pour reproduire la diagonale donnée ?','A et C.','Une diagonale relie deux sommets opposés : elle traverse l’intérieur du rectangle.'),
 row('Combien de carreaux-unités mesure le tour du rectangle ?','16 carreaux-unités.',r'$5+3+5+3=16$. On additionne les quatre côtés ; la diagonale n’appartient pas au contour.')],images=('quadrillage_rectangle',))
ex(15,'Perpendiculaires en chaîne','Trace une droite (d1), puis une droite (d2) perpendiculaire à (d1). Place un point P de (d2), différent du croisement, et trace par P la perpendiculaire (d3) à (d2).',[
 row('Quel instrument garantit le premier angle droit ?','L’équerre.','On aligne un côté de l’angle droit sur (d1), puis on trace (d2) le long de l’autre.'),
 row('Par quel point la droite (d3) doit-elle passer ?','Par P.','Le programme impose ce passage ; il faut garder P sur le bord de tracé.'),
 row('Quelle droite est perpendiculaire aux deux autres ?','La droite (d2).','Elle est perpendiculaire à (d1) par construction, puis à (d3) par la seconde construction.'),
 row('Quelle relation observes-tu entre (d1) et (d3) ?','Elles sont parallèles.','Deux droites distinctes perpendiculaires à une même droite ont la même direction.'),
 row('Pourquoi a-t-on choisi P différent du premier croisement ?','Pour obtenir deux droites parallèles distinctes.','Si on utilisait le même point, les deux tracés perpendiculaires à (d2) se superposeraient.')])
ex(15,'Le plan du quartier','Sur le plan, les rues des Lilas et des Érables sont perpendiculaires à l’avenue du Parc. Deux repères F et G, sur cette avenue, sont distants de 6 cm sur le plan. Une fontaine doit être au milieu du segment [FG].',[
 row('Quelles rues sont parallèles ?','La rue des Lilas et la rue des Érables.','Elles sont toutes deux perpendiculaires à l’avenue du Parc.'),
 row('Cite deux voies perpendiculaires.','La rue des Lilas et l’avenue du Parc.','C’est un des deux angles droits indiqués dans les données.'),
 row('À quelle distance de F places-tu la fontaine sur le segment [FG] ?','À 3 cm de F.',r'$6\div2=3$ : le milieu partage les 6 cm en deux parties égales.'),
 row('Quelle est la distance de la fontaine à G sur le plan ?','3 cm.','Le milieu est à la même distance de F et de G.'),
 row('Dire seulement « à égale distance de F et de G » localiserait-il une unique fontaine ?','Non : il faut aussi préciser qu’elle est sur le segment [FG].','Plusieurs points hors du segment peuvent être à égale distance de F et de G. L’appartenance au segment désigne ici son milieu.')])

# Triangles et quadrilatères : construction, vocabulaire, propriétés et vigilance.
ex(16,'Reconnaître les triangles','Observe les trois triangles codés. Le triangle 1 a un angle droit. Le triangle 2 a deux côtés codés égaux. Le triangle 3 a trois côtés codés égaux.',[
 row('Quel triangle est rectangle ?','Le triangle 1.','Le petit carré signale un angle droit.'),
 row('Quelle propriété du triangle 2 montre le codage ?','Il a deux côtés de même longueur : il est isocèle.','Les deux traits identiques affirment l’égalité des côtés.'),
 row('Quel nom plus précis donne-t-on au triangle 3 ?','Un triangle équilatéral.','Ses trois côtés ont la même longueur.'),
 row('Un triangle rectangle peut-il aussi être isocèle ?','Oui, s’il a deux côtés de même longueur.','Les deux conditions sont compatibles ; un angle droit n’interdit pas deux côtés égaux.'),
 row('L’absence de code sur un autre dessin prouve-t-elle que ses côtés sont différents ?','Non : on manque d’information.','Un dessin sans code ne donne pas de preuve d’égalité ni d’inégalité. Il faut des mesures ou des données supplémentaires.')],images=('triangles',))
ex(16,'Coder une figure','Le triangle MNP vérifie MN = MP = 5 cm et NP = 6 cm.',[
 row('Quels côtés portent un même code d’égalité ?','Les côtés [MN] et [MP].','Leurs longueurs sont toutes deux de 5 cm.'),
 row('Comment nomme-t-on ce triangle ?','Un triangle isocèle de sommet principal M.','Les deux côtés égaux se rencontrent au point M.'),
 row('Quel côté constitue sa base ?','Le côté [NP].','C’est le côté opposé au sommet principal M.'),
 row('Peut-on mettre le même code sur [NP] ?','Non : NP mesure 6 cm, pas 5 cm.','Un code identique affirmerait une égalité fausse.'),
 row('Calcule son périmètre.','16 cm.',r'$5+5+6=16$. On additionne les trois longueurs du contour.')])
ex(16,'Le triangle équilatéral','Construis un triangle équilatéral ABC de côté 4 cm.',[
 row('Quel segment traces-tu d’abord ?','Le segment [BC] de 4 cm.','Ce segment constitue un côté connu et sert de base à la construction.'),
 row('À quelle ouverture règles-tu le compas ?','À 4 cm.','Tous les côtés du triangle équilatéral doivent mesurer cette longueur.'),
 row('Comment places-tu A ?','À une intersection des deux arcs de centres B et C, de rayon 4 cm.','Le premier arc impose AB = 4 cm et le second AC = 4 cm.'),
 row('Quelles égalités codes-tu après avoir relié les sommets ?','$AB=BC=CA=4$ cm.','Les trois longueurs sont imposées par le segment et par les arcs du compas.'),
 row('Calcule le périmètre de ce triangle.','12 cm.',r'$4+4+4=12$. Le contour comporte trois côtés égaux.')],correction=('equilateral',))
ex(16,'Reconnaître les quadrilatères','La figure 1 possède quatre angles droits, avec côtés de 4 cm et 2 cm. La figure 2 possède quatre côtés égaux sans angle droit. La figure 3 possède quatre côtés égaux et quatre angles droits.',[
 row('Quel est le nom précis de la figure 1 ?','Un rectangle non carré.','Les quatre angles sont droits, mais les deux longueurs 4 cm et 2 cm sont différentes.'),
 row('Quel est le nom de la figure 2 ?','Un losange non carré.','Ses côtés sont égaux, mais il ne possède pas les angles droits nécessaires au carré.'),
 row('Quel est le nom le plus précis de la figure 3 ?','Un carré.','Le carré réunit les quatre côtés égaux et les quatre angles droits.'),
 row('La figure 3 est-elle aussi un rectangle ?','Oui.','Elle possède les quatre angles droits de la définition du rectangle.'),
 row('La figure 3 est-elle aussi un losange ?','Oui.','Elle possède les quatre côtés de même longueur de la définition du losange.')],images=('quadrilateres',))
ex(16,'Carré ou losange','Un quadrilatère possède quatre côtés de 5 cm. Aucun angle droit n’est donné. Zoé affirme que c’est forcément un carré.',[
 row('Quelle nature peut-on affirmer ?','C’est un losange.','Ses quatre côtés ont la même longueur, ce qui correspond à la définition du losange.'),
 row('L’affirmation de Zoé est-elle justifiée ?','Non.','Il manque une information sur les angles droits pour affirmer que ce losange est un carré.'),
 row('Quel instrument permet de contrôler les angles ?','L’équerre.','Son angle droit doit s’ajuster exactement à l’ouverture des angles du dessin.'),
 row('Si on tourne le dessin, sa nature change-t-elle ?','Non.','Une rotation de la feuille conserve les longueurs et les angles du quadrilatère.'),
 row('Calcule le périmètre connu, même sans connaître les angles.','20 cm.',r'$5+5+5+5=20$. Le calcul ne dépend que des longueurs des côtés.')])
ex(16,'Le triangle rectangle','Construis un triangle ABC rectangle en A avec AB = 4 cm et AC = 3 cm.',[
 row('Quel angle construis-tu d’abord ?','L’angle droit en A.','L’équerre permet de tracer deux directions perpendiculaires issues de A.'),
 row('Où places-tu B ?','Sur le premier côté de l’angle, à 4 cm de A.','Place le zéro de la règle en A, puis B à la graduation 4 cm.'),
 row('Où places-tu C ?','Sur le second côté de l’angle, à 3 cm de A.','Les deux côtés [AB] et [AC] restent perpendiculaires et gardent les longueurs demandées.'),
 row('Quel segment traces-tu pour terminer le triangle ?','Le segment [BC].','Il relie les deux points déjà placés et ferme les trois côtés du triangle.'),
 row('Mesure BC sur ta construction soignée, au millimètre près.','On obtient environ 5 cm.','Place le zéro de la règle en B et lis la position de C. Il s’agit ici d’une vérification par mesure, sans formule nouvelle.')],correction=('rectangle_triangle',))
ex(16,'Le triangle isocèle','Construis un triangle DEF avec EF = 4 cm et DE = DF = 6 cm.',[
 row('Quel côté prends-tu comme base ?','Le côté [EF] de 4 cm.','On commence par le seul côté dont les extrémités serviront de centres aux deux arcs.'),
 row('Quelle ouverture du compas convient aux deux arcs ?','6 cm.','Les distances du sommet D à E et à F doivent chacune valoir 6 cm.'),
 row('Comment trouves-tu D ?','À une intersection des arcs de centres E et F.','Un point commun aux deux arcs respecte simultanément les deux longueurs imposées.'),
 row('Quels côtés codes-tu égaux ?','Les côtés [DE] et [DF].','Ce sont les deux côtés de 6 cm ; la base mesure seulement 4 cm.'),
 row('Calcule le périmètre du triangle.','16 cm.',r'$6+6+4=16$. Les trois côtés sont ajoutés une seule fois.')])
ex(16,'Le rectangle aux instruments','Construis le rectangle ABCD avec AB = 6 cm et BC = 4 cm, en nommant les sommets dans l’ordre.',[
 row('Quel côté traces-tu en premier ?','Le segment [AB] de 6 cm.','Il fixe la position et la longueur du premier côté.'),
 row('Quelles droites traces-tu en A et en B ?','Les perpendiculaires au côté [AB].','L’équerre impose deux angles droits. Les deux droites obtenues sont parallèles entre elles.'),
 row('Comment places-tu C et D ?','À 4 cm de B et de A, du même côté du segment [AB].','On reporte la largeur sur les deux perpendiculaires, puis on joint C à D.'),
 row('Quelle est la longueur CD ?','6 cm.','Dans le rectangle, les côtés opposés [AB] et [CD] ont la même longueur.'),
 row('Calcule le périmètre.','20 cm.',r'$6+4+6+4=20$. Le rectangle a deux côtés de chaque longueur.')])
ex(16,'Le carré penché','Construis un carré ABCD de côté 4 cm en commençant par un segment [AB] incliné sur ta feuille.',[
 row('Comment construis-tu les angles en A et en B ?','Avec l’équerre, perpendiculairement au côté [AB].','On tourne l’équerre pour suivre le segment incliné ; l’inclinaison n’empêche pas de tracer un angle droit.'),
 row('Quelles longueurs reportes-tu pour placer D et C ?','4 cm depuis A et 4 cm depuis B.','Tous les côtés du carré ont la même longueur. On place les deux points du même côté du segment [AB].'),
 row('Quel segment ferme le carré ?','Le segment [CD].','Il relie les deux nouveaux sommets. On vérifie aussi sa longueur et les deux derniers angles droits.'),
 row('Le carré est-il devenu un losange non carré parce qu’il est incliné ?','Non : il reste un carré.','La position du dessin ne modifie ni ses quatre angles droits ni ses quatre côtés égaux.'),
 row('Quel est son périmètre ?','16 cm.',r'$4\times4=16$. On compte les quatre côtés de 4 cm.')])
ex(16,'Le losange au compas','On veut construire un losange ABCD de côté 5 cm. On commence par deux segments [AB] et [AD] de 5 cm formant une ouverture non droite, avec B et D distincts.',[
 row('Quelles longueurs connaît-on déjà ?','$AB=AD=5$ cm.','Les deux premiers côtés du losange partent de A et ont la longueur demandée.'),
 row('Où traces-tu les deux nouveaux arcs ?','Un arc de centre B et un arc de centre D, chacun de rayon 5 cm.','Le futur point C devra être à 5 cm de B et à 5 cm de D.'),
 row('Les arcs se rencontrent en A et en un autre point. Lequel choisis-tu pour C ?','L’autre point de rencontre, différent de A.','Prendre A ne créerait pas un quadrilatère à quatre sommets distincts.'),
 row('Quels segments traces-tu pour terminer ?','Les segments [BC] et [CD].','Avec [AB] et [AD], ils forment les quatre côtés égaux du losange.'),
 row('Quelle vérification suffit pour écarter le nom de carré ici ?','Vérifier que l’angle en A n’est pas droit.','L’ouverture de départ est non droite. Le carré exigerait quatre angles droits.')])
ex(16,'Une figure composée','Construis un carré ABCD de côté 4 cm. À l’extérieur du carré, construis ensuite un triangle équilatéral ABE sur le côté [AB].',[
 row('Quelle figure construis-tu d’abord ?','Le carré ABCD.','Le programme commence par le carré ; le triangle s’appuie sur un de ses côtés.'),
 row('Quelle est la longueur de la base du triangle ?','4 cm.','Le côté commun [AB] est un côté du carré de 4 cm.'),
 row('Comment places-tu E à l’extérieur du carré ?','À l’intersection extérieure des deux arcs de rayon 4 cm, de centres A et B.','Les deux intersections possibles sont de part et d’autre de la base ; on choisit celle située hors du carré.'),
 row('Quelles sont les longueurs AE et BE ?','$AE=BE=4$ cm.','Les arcs garantissent ces deux distances, comme l’exige le triangle équilatéral.'),
 row('Calcule le contour extérieur de l’ensemble, sans compter [AB].','20 cm.',r'Le côté partagé est à l’intérieur. Le contour extérieur a cinq côtés de 4 cm : $5\times4=20$.')],correction=('maison',))
ex(16,'Le programme en désordre','Pour un rectangle de 6 cm sur 2 cm, on propose quatre cartes : A « reporter 2 cm sur les deux perpendiculaires, du même côté » ; B « joindre les deux nouveaux points » ; C « tracer un segment de 6 cm » ; D « tracer les perpendiculaires aux deux extrémités ».',[
 row('Quelle carte vient en premier ?','La carte C.','Il faut d’abord disposer du segment dont les extrémités serviront aux étapes suivantes.'),
 row('Quelle carte vient ensuite ?','La carte D.','Les perpendiculaires se construisent aux extrémités du segment de 6 cm.'),
 row('Quelle est la troisième carte ?','La carte A.','Les perpendiculaires étant tracées, on peut y reporter la largeur de 2 cm.'),
 row('Quelle carte termine la construction ?','La carte B.','Les deux points nouveaux sont maintenant connus ; leur liaison ferme le rectangle.'),
 row('Quelle erreur éviter en exécutant la carte A ?','Placer les deux points de côtés différents du premier segment.','Il faut reporter les 2 cm du même côté ; sinon la figure ne sera pas le rectangle attendu.')])
ex(16,'La figure qui ment','Un croquis de quadrilatère ressemble à un carré. Pourtant ses côtés consécutifs sont indiqués : 7 cm, 4 cm, 7 cm, 4 cm. Quatre angles droits sont codés.',[
 row('Faut-il croire l’apparence ou les données ?','Les données et les codes.','Un croquis peut être volontairement déformé ; les mesures écrites et les codes précisent les propriétés.'),
 row('Quel nom précis convient ?','Un rectangle non carré.','Les quatre angles sont droits, mais 7 cm et 4 cm sont deux longueurs différentes.'),
 row('Pourquoi ne peut-on pas l’appeler carré ?','Ses quatre côtés ne sont pas tous égaux.','Le carré doit posséder quatre côtés de même longueur en plus de ses angles droits.'),
 row('Quelles paires de côtés ont la même longueur ?','Les deux côtés de 7 cm, et les deux côtés de 4 cm.','Ce sont les deux paires de côtés opposés du rectangle.'),
 row('Calcule son périmètre.','22 cm.',r'$7+4+7+4=22$. Les longueurs écrites servent au calcul, même si le dessin semble carré.')])
ex(16,'Le plus grand tour','On compare un carré de côté 5 cm et un rectangle de 7 cm sur 3 cm.',[
 row('Calcule le périmètre du carré.','20 cm.',r'$5\times4=20$. Ses quatre côtés sont égaux.'),
 row('Calcule le périmètre du rectangle.','20 cm.',r'$7+3+7+3=20$. On additionne ses quatre côtés.'),
 row('Lequel a le plus grand tour ?','Aucun : les deux périmètres sont égaux.','Les deux calculs donnent 20 cm, même si les formes sont différentes.'),
 row('Ces deux figures sont-elles superposables ?','Non.','Le carré a quatre côtés de 5 cm ; le rectangle a des côtés de 7 cm et de 3 cm.'),
 row('Un périmètre égal prouve-t-il que deux figures sont identiques ?','Non.','Cet exemple fournit deux figures différentes dont les tours ont pourtant la même longueur.')])
ex(16,'Les diagonales du rectangle','Trace un rectangle ABCD de 6 cm sur 4 cm, avec les sommets nommés dans l’ordre. On appelle diagonale un segment reliant deux sommets opposés.',[
 row('Quelle diagonale part de A ?','Le segment [AC].','Le sommet opposé à A est C ; B et D sont ses voisins.'),
 row('Quelle est l’autre diagonale ?','Le segment [BD].','Elle relie les deux autres sommets opposés.'),
 row('Combien de diagonales as-tu tracées ?','2 diagonales.','Il existe deux paires de sommets opposés dans ce quadrilatère.'),
 row('Mesure et compare leurs longueurs.','Elles ont la même longueur, environ 7,2 cm sur cette construction.','Une mesure soignée donne des valeurs égales au millimètre près. Les diagonales du rectangle sont de même longueur.'),
 row('Leur croisement I est-il le milieu de chacune ?','Oui : IA = IC et IB = ID.','La règle permet de comparer chaque moitié. Les diagonales du rectangle se coupent en leur milieu.')])

# Symétrie : toutes les constructions sont sur quadrillage à axe horizontal/vertical.
ex(17,'Axe ou pas','Un rectangle non carré est dessiné avec deux côtés horizontaux. On propose trois plis : au milieu verticalement, au milieu horizontalement, ou le long d’un bord.',[
 row('Le pli vertical du milieu est-il un axe de symétrie ?','Oui.','Il superpose les deux moitiés gauche et droite du rectangle.'),
 row('Le pli horizontal du milieu est-il un axe de symétrie ?','Oui.','Il superpose les deux moitiés haute et basse.'),
 row('Le bord du rectangle est-il un axe de symétrie de ce rectangle ?','Non.','Un pli sur le bord renvoie le rectangle à l’extérieur de lui-même ; les deux moitiés ne se recouvrent pas.'),
 row('Quel test permet de vérifier un axe sur papier ?','Plier pour vérifier la superposition exacte des deux parties.','Les contours doivent coïncider, pas seulement avoir la même aire.'),
 row('Une droite qui partage une figure en deux aires égales est-elle forcément un axe ?','Non.','L’égalité des aires ne garantit pas la superposition par pliage. Il faut que chaque point trouve son correspondant.')])
ex(17,'Compter les axes','Observe un rectangle non carré, un carré et un triangle isocèle non équilatéral. Les axes se vérifient par pliage.',[
 row('Combien d’axes possède le rectangle non carré ?','2 axes.','Les plis passant par les milieux des côtés opposés superposent la figure.'),
 row('Combien d’axes possède le carré ?','4 axes.','Deux plis passent par les milieux de côtés opposés et deux autres joignent des sommets opposés.'),
 row('Combien d’axes possède le triangle isocèle non équilatéral ?','1 axe.','Le pli passe par son sommet principal et par le milieu de la base.'),
 row('Le carré possède-t-il plus d’axes que le rectangle non carré ?','Oui : 4 au lieu de 2.','Les côtés égaux du carré permettent deux pliages supplémentaires.'),
 row('Un axe peut-il passer par l’intérieur d’une figure sans la partager en parties superposables ?','Oui, une droite peut le faire, mais alors ce n’est pas un axe de symétrie.','Traverser la figure n’est pas suffisant : le test décisif est le recouvrement par pliage.')],images=('axes',))
ex(17,'Le pli décalé','Un rectangle non carré mesure 6 carreaux de large et 4 carreaux de haut. On propose une droite verticale à 2 carreaux du bord gauche.',[
 row('Combien de carreaux séparent cette droite du bord droit ?','4 carreaux.',r'$6-2=4$. On retranche la largeur située à gauche.'),
 row('Les deux largeurs sont-elles égales ?','Non : 2 carreaux et 4 carreaux sont différents.','Les deux parties du rectangle n’ont pas la même largeur.'),
 row('Cette droite est-elle un axe de symétrie ?','Non.','En pliant, les bords gauche et droit ne peuvent pas coïncider.'),
 row('Où faut-il placer un axe vertical ?','Au milieu, à 3 carreaux de chaque bord.','La moitié de 6 carreaux vaut 3 carreaux.'),
 row('Où se place l’axe horizontal ?','Au milieu, à 2 carreaux du haut et du bas.',r'$4\div2=2$. Cet autre pli superpose aussi les bords opposés.')])
ex(17,'Le symétrique de trois points','Sur le quadrillage, l’axe est vertical. A est à 2 carreaux à gauche, B à 3 carreaux à gauche, C à 1 carreau à gauche. Chaque point reste sur sa propre ligne.',[
 row('Où places-tu A′ ?','À 2 carreaux à droite de l’axe, sur la ligne de A.','On compte horizontalement jusqu’à l’axe, puis le même nombre de carreaux de l’autre côté.'),
 row('Où places-tu B′ ?','À 3 carreaux à droite, sur la ligne de B.','La distance à l’axe doit être la même que pour B.'),
 row('Où places-tu C′ ?','À 1 carreau à droite, sur la ligne de C.','Le déplacement se fait sur la ligne horizontale passant par C.'),
 row('Quelle est la distance entre A et A′ en carreaux ?','4 carreaux.',r'$2+2=4$. L’axe est situé entre les deux points.'),
 row('Que devient un point posé exactement sur l’axe ?','Il reste au même endroit.','Sa distance à l’axe est nulle, donc son symétrique se confond avec lui-même.')],images=('points_depart',),correction=('points_corrige',))
ex(17,'Compléter la maison','La moitié gauche d’une maison est dessinée. L’axe vertical passe par le milieu du toit et de la façade. Le coin gauche du toit est à 3 carreaux de l’axe, le coin gauche du mur à 2 carreaux.',[
 row('Où places-tu le coin droit du toit ?','À 3 carreaux à droite, à la même hauteur que le coin gauche.','On reproduit la distance horizontale de l’autre côté de l’axe.'),
 row('Où places-tu le coin droit du mur ?','À 2 carreaux à droite, sur la même ligne que le coin gauche.','Les deux coins du mur doivent se superposer au pliage.'),
 row('Que devient le sommet du toit placé sur l’axe ?','Il reste au même point.','Un point de l’axe est son propre symétrique.'),
 row('Comment relies-tu les nouveaux sommets ?','Dans le même ordre que ceux de la moitié gauche.','On reporte d’abord les points, puis les segments correspondants pour éviter d’inventer un côté.'),
 row('Comment contrôles-tu le dessin terminé ?','Par pliage ou en comparant les distances à l’axe, sommet par sommet.','Les sommets correspondants doivent être sur la même ligne et à égale distance de l’axe.')],images=('maison_depart',),correction=('maison_corrige',))
ex(17,'Axe horizontal','Sur le quadrillage, l’axe est horizontal. A se situe 1 carreau au-dessus et B 3 carreaux au-dessus. Le segment [AB] est tracé.',[
 row('Où places-tu A′ ?','1 carreau au-dessous de l’axe, dans la même colonne que A.','Pour un axe horizontal, on compte verticalement.'),
 row('Où places-tu B′ ?','3 carreaux au-dessous, dans la même colonne que B.','La distance à l’axe est conservée, mais le côté haut ou bas est inversé.'),
 row('Quel segment faut-il tracer ?','Le segment [A′B′].','Les images des deux extrémités déterminent le segment symétrique.'),
 row('Quelle est la distance de B à B′ ?','6 carreaux.',r'$3+3=6$. L’axe partage ce trajet vertical en deux parties égales.'),
 row('Le segment image est-il plus court que [AB] ?','Non : il a la même longueur.','Le pliage superpose les deux segments ; la symétrie conserve les longueurs.')],images=('horizontal_depart',),correction=('horizontal_corrige',))
ex(17,'Le papillon','On construit un motif de papillon par symétrie par rapport à une droite horizontale. Un sommet S de l’aile est sur l’axe ; P est 2 carreaux au-dessus et Q 3 carreaux au-dessus.',[
 row('Où se place S′ ?','Au même point que S.','S appartient à l’axe, donc il ne change pas de place.'),
 row('Où se place P′ ?','2 carreaux au-dessous de l’axe, dans la colonne de P.','On reproduit la même distance verticale de l’autre côté.'),
 row('Où se place Q′ ?','3 carreaux au-dessous, dans la colonne de Q.','La position horizontale ne change pas quand l’axe est horizontal.'),
 row('Comment reconstruis-tu le contour de l’aile image ?','En reliant les points images dans le même ordre.','Chaque côté du modèle possède un côté image entre les sommets correspondants.'),
 row('Si une aile possède une tache à 1 carreau au-dessus de l’axe, où doit être sa tache symétrique ?','À 1 carreau au-dessous, dans la même colonne.','La symétrie concerne aussi les détails intérieurs, pas seulement le contour.')])
ex(17,'Les lettres tracées en bâtons','On dessine des lettres idéales en bâtons : A avec deux jambes identiques et une barre horizontale centrée ; B avec deux lobes identiques ; H avec sa barre au milieu ; F avec une barre haute et une barre médiane plus courte.',[
 row('Quel axe possède le A décrit ?','Un axe vertical.','Les deux jambes s’échangent par pliage gauche-droite et la barre se superpose à elle-même.'),
 row('Quel axe possède le B décrit ?','Un axe horizontal.','Les deux lobes identiques du haut et du bas se superposent.'),
 row('Quels axes possède le H décrit ?','Un axe vertical et un axe horizontal.','Les deux montants et la barre centrale coïncident lors de chacun de ces deux pliages.'),
 row('Le F décrit a-t-il un de ces deux axes ?','Non.','Ni le pli gauche-droite ni le pli haut-bas ne superpose son contour.'),
 row('Peut-on généraliser ces réponses à toutes les polices d’écriture ?','Non : il faut examiner le dessin exact des lettres.','Des épaisseurs, des ornements ou des lobes différents peuvent supprimer une symétrie.')])
ex(17,'Chercher l’erreur','L’axe est vertical. Le point B est à 3 carreaux à gauche. Léa a placé son candidat B′ sur la même ligne, à seulement 2 carreaux à droite.',[
 row('La ligne horizontale choisie convient-elle ?','Oui.','Pour un axe vertical, les deux points doivent être sur la même ligne horizontale.'),
 row('La distance choisie convient-elle ?','Non : 2 carreaux ne valent pas 3 carreaux.','Les distances à l’axe doivent être égales de part et d’autre.'),
 row('Où faut-il placer le vrai B′ ?','À 3 carreaux à droite, sur la ligne de B.','On reporte le nombre de carreaux donné pour B.'),
 row('De combien de carreaux faut-il déplacer le candidat ?','1 carreau vers la droite.',r'$3-2=1$. Le candidat doit s’éloigner de l’axe.'),
 row('Le simple fait d’être de l’autre côté suffit-il ?','Non.','Il faut à la fois le bon côté, la même ligne et la même distance à l’axe.')])
ex(17,'Une extrémité sur l’axe','L’axe est vertical. A est sur cet axe. B est 2 carreaux à gauche de l’axe et 1 carreau au-dessus de A. Le segment [AB] est tracé.',[
 row('Où places-tu A′ ?','Au même point que A.','A est sur l’axe : il ne se déplace pas.'),
 row('Où places-tu B′ ?','2 carreaux à droite et 1 carreau au-dessus de A.','La hauteur de B est conservée ; seule sa position gauche-droite est inversée.'),
 row('Quel segment traces-tu pour obtenir le symétrique ?','Le segment [AB′].','Comme A′ et A sont confondus, le segment image part du même point A.'),
 row('La longueur du segment image est-elle la même ?','Oui : AB′ = AB.','La symétrie conserve les longueurs.'),
 row('A est-il le milieu de [BB′] ?','Non : le milieu est sur la ligne de B, 1 carreau au-dessus de A.','Le milieu est sur le segment reliant B à B′. A est sur l’axe, mais pas sur ce segment horizontal.')])
ex(17,'Le carrelage','À gauche d’un axe vertical, on a colorié six cases : 2 dans la ligne du haut, 1 dans la ligne du milieu et 3 dans la ligne du bas. Aucune ne traverse l’axe.',[
 row('Combien de cases faut-il ajouter à droite pour compléter le motif ?','6 cases.','Chaque case colorée reçoit une unique case symétrique.'),
 row('Combien faut-il ajouter dans la ligne du haut ?','2 cases.','Un axe vertical conserve la ligne de chaque case.'),
 row('Combien faut-il ajouter dans la ligne du milieu ?','1 case.','La case doit se retrouver de l’autre côté à la même distance du pli.'),
 row('Combien faut-il ajouter dans la ligne du bas ?','3 cases.','Les trois cases du bas reçoivent leurs trois correspondantes.'),
 row('Combien de cases colorées le motif final contient-il ?','12 cases.',r'$6+6=12$. Les cases initiales et leurs images sont distinctes.')],images=('carrelage_depart',),correction=('carrelage_corrige',))
ex(17,'Deux axes à la fois','Un motif de 3 cases est placé entièrement dans le quart supérieur gauche d’une grille. Deux axes, l’un vertical et l’autre horizontal, délimitent les quatre quarts. Aucune case colorée ne touche un axe.',[
 row('Combien de cases ajoutes-tu dans le quart supérieur droit ?','3 cases.','On reflète les trois cases à travers l’axe vertical.'),
 row('Combien de cases sont colorées dans toute la moitié du haut ?','6 cases.',r'$3+3=6$ : le motif initial et son premier reflet.'),
 row('Combien de cases ajoutes-tu dans la moitié du bas ?','6 cases.','On reflète toute la moitié du haut à travers l’axe horizontal.'),
 row('Combien de cases sont colorées à la fin ?','12 cases.',r'$3\times4=12$. Chaque quart possède trois cases et aucun reflet ne se superpose à un autre.'),
 row('Pourquoi refléter seulement le motif initial vers le bas ne suffit-il pas ?','Le quart inférieur droit manquerait.','Il faut compléter les quatre quarts pour que les deux pliages fonctionnent.')])
ex(17,'Les longueurs conservées','Le segment horizontal [CD] mesure 4 carreaux. Il est situé 2 carreaux au-dessus d’un axe horizontal.',[
 row('À quelle distance de l’axe places-tu C′ ?','2 carreaux au-dessous.','La distance de chaque point à l’axe est conservée.'),
 row('À quelle distance places-tu D′ ?','2 carreaux au-dessous.','D est à la même hauteur que C ; son image est donc sur la même ligne que C′.'),
 row('Quelle est la longueur C′D′ ?','4 carreaux.','La symétrie conserve les longueurs des segments.'),
 row('Quelle est la distance verticale entre les deux segments ?','4 carreaux.',r'$2+2=4$. Les segments sont de part et d’autre de l’axe.'),
 row('Ces deux segments sont-ils parallèles ?','Oui.','Ils sont tous deux horizontaux, situés sur deux lignes différentes du quadrillage.')])
ex(17,'Le bateau du port','Un demi-bateau est dessiné à gauche d’un axe vertical. Le mât est sur l’axe. Le coin de coque C est 3 carreaux à gauche du mât ; le coin de voile V est 2 carreaux à gauche.',[
 row('Que devient le mât dans le dessin symétrique ?','Il reste sur lui-même.','Tous ses points sont sur l’axe vertical.'),
 row('Où places-tu le coin C′ de la coque ?','3 carreaux à droite, sur la ligne de C.','La coque se reflète à égale distance du mât.'),
 row('Où places-tu le coin V′ de la voile ?','2 carreaux à droite, sur la ligne de V.','La voile se complète point par point, comme le contour.'),
 row('Quelle est la distance horizontale entre C et C′ ?','6 carreaux.',r'$3+3=6$. Le mât se trouve au milieu de cette largeur.'),
 row('Quelle vérification finale fais-tu sur la voile et la coque ?','Vérifier leur superposition par pliage selon le mât.','Les deux contours et leurs détails doivent coïncider, pas seulement les points les plus éloignés.')])
ex(17,'Vrai ou faux : bien justifier','Pour chacune des cinq phrases, réponds vrai ou faux et justifie.',[
 row('« Le symétrique d’un point est toujours un autre point. »','Faux.','Un point situé sur l’axe est son propre symétrique.'),
 row('« Une figure possède au plus un axe de symétrie. »','Faux.','Le rectangle non carré possède déjà deux axes de symétrie.'),
 row('« Deux points symétriques sont à la même distance de l’axe. »','Vrai.','Le pliage fait coïncider les deux points et conserve leurs distances au pli.'),
 row('« Avec un axe vertical, il faut placer le point image dans la même colonne. »','Faux : il faut la même ligne horizontale.','Les colonnes sont conservées pour un axe horizontal, pas pour un axe vertical.'),
 row('« Le symétrique d’un segment mesure autant que ce segment. »','Vrai.','Les deux segments se superposent par pliage ; la symétrie conserve les longueurs.')])

# Solides : pas de formule de volume ; manipulation des modèles et programmes.
ex(18,'Nommer les solides','Observe les sept solides présentés : cube, pavé, cylindre, pyramide, cône, boule et prisme droit à base triangulaire.',[
 row('Quel solide possède six faces carrées ?','Le cube.','Toutes ses faces sont des carrés de même côté.'),
 row('Quel solide possède deux bases circulaires et une surface courbe ?','Le cylindre.','Un tube ou une boîte cylindrique en donne un modèle.'),
 row('Quel solide possède une base circulaire et une pointe ?','Le cône.','Sa surface courbe rejoint le sommet situé au-dessus de sa base.'),
 row('Quel solide n’a aucune face plate ?','La boule.','Sa surface est entièrement courbe, comme celle d’une balle.'),
 row('Quel solide possède deux bases triangulaires et trois faces rectangulaires ?','Le prisme droit à base triangulaire.','Ses deux triangles identiques sont reliés par trois rectangles.')],images=('solides_courbes', 'familles',))
ex(18,'La carte d’identité du cube','Observe un modèle de cube ou sa représentation en perspective. Les arêtes cachées sont en pointillés.',[
 row('Combien de faces possède le cube ?','6 faces.','Compte aussi les faces situées à l’arrière ou au-dessous.'),
 row('Quelle est la forme de chaque face ?','Un carré.','Les faces ont quatre côtés égaux et quatre angles droits, même si la perspective les déforme sur le dessin.'),
 row('Combien d’arêtes possède-t-il ?','12 arêtes.','Il y en a quatre sur le contour supérieur, quatre sur le contour inférieur et quatre pour les relier.'),
 row('Combien de sommets possède-t-il ?','8 sommets.','Quatre sont sur une face et quatre sur la face opposée.'),
 row('Si chaque arête mesure 2 cm, quelle longueur totale de baguettes faut-il pour son squelette ?','24 cm.',r'$12\times2=24$. Chaque arête correspond à une baguette et on la compte une seule fois.')],images=('cube',))
ex(18,'Décrire un pavé','Une boîte est un pavé de longueur 5 cm, de largeur 3 cm et de hauteur 2 cm.',[
 row('Combien de faces possède cette boîte ?','6 faces.','Le dessous et les faces arrière comptent aussi, même s’ils sont invisibles sur un dessin.'),
 row('Quelle est la nature de ses faces ?','Des rectangles.','Un pavé possède six faces rectangulaires ; selon ses dimensions, certaines pourraient être carrées.'),
 row('Combien d’arêtes et de sommets possède-t-elle ?','12 arêtes et 8 sommets.','La structure est la même que celle d’un cube : quatre arêtes sur chaque face opposée et quatre pour les relier.'),
 row('Quelles dimensions ont ses deux plus grandes faces ?','5 cm sur 3 cm.','Les trois types de faces sont 5 sur 3, 5 sur 2 et 3 sur 2 ; chaque type apparaît deux fois.'),
 row('Que dire des faces opposées ?','Elles sont superposables deux à deux.','Les deux faces de chaque paire ont les mêmes dimensions.')],images=('pave',))
ex(18,'Les faces de la pyramide','On étudie une pyramide dont la base est un carré. Ses quatre faces latérales se rejoignent à un sommet au-dessus de la base.',[
 row('Quelle est la forme de la base ?','Un carré.','C’est la face sur laquelle repose la pyramide dans le modèle décrit.'),
 row('Quelle est la forme d’une face latérale ?','Un triangle.','Chaque côté de la base est relié au sommet de la pyramide.'),
 row('Combien y a-t-il de faces latérales ?','4 faces triangulaires.','Le carré de base possède quatre côtés : chacun porte une face latérale.'),
 row('Combien de faces possède la pyramide au total ?','5 faces.',r'$1+4=5$ : une base carrée et quatre triangles.'),
 row('Quels éléments en carton peux-tu préparer pour fabriquer un modèle ?','Un carré et quatre triangles adaptés aux côtés du carré, puis du ruban adhésif.','Les côtés des triangles qui touchent la base doivent correspondre aux côtés du carré. On assemble et on relève les faces pour rejoindre le sommet.')],images=('familles',))
ex(18,'Le prisme droit','On étudie un prisme droit à base triangulaire. Les deux bases sont des triangles identiques, reliés par des rectangles.',[
 row('Combien possède-t-il de bases ?','2 bases.','Les deux faces triangulaires opposées ont la même forme et les mêmes dimensions.'),
 row('Quelle est la nature des autres faces ?','Des rectangles.','Chaque côté d’une base est relié au côté correspondant de l’autre base par une face rectangulaire.'),
 row('Combien y a-t-il de faces rectangulaires ?','3 faces rectangulaires.','Chaque triangle possède trois côtés, donc trois faces latérales.'),
 row('Combien possède-t-il de faces au total ?','5 faces.',r'$2+3=5$ : deux triangles et trois rectangles.'),
 row('Comment réaliser un modèle avec des pièces de carton ?','Assembler deux triangles identiques et trois rectangles adaptés, puis fermer avec du ruban adhésif.','Les largeurs des rectangles correspondent aux trois côtés du triangle ; leurs autres côtés ont une même longueur, celle du prisme.')],images=('familles',))
ex(18,'Patron ou pas','Les trois dispositions de six carrés sont dessinées. A : quatre carrés en ligne, avec un carré au-dessus et un au-dessous du deuxième. B : quatre carrés en ligne, avec un carré au-dessus du deuxième et un au-dessus du troisième. C : trois carrés en ligne, puis trois carrés sous le carré du milieu.',[
 row('Combien de carrés faut-il pour un patron du cube ?','6 carrés identiques.','Ils correspondent aux six faces carrées du cube.'),
 row('La disposition A est-elle un patron ?','Oui.','Les quatre carrés forment une bande autour du cube et les deux autres ferment les deux ouvertures.'),
 row('La disposition B est-elle un patron ?','Non.','Les deux carrés placés du même côté de la bande se superposent au pliage : une face resterait ouverte.'),
 row('La disposition C est-elle un patron ?','Oui.','En relevant les carrés autour du carré central, les six faces se placent sans recouvrement.'),
 row('Comment lever un doute sans se fier au dessin ?','Découper une copie et tester le pliage.','Six carrés ne suffisent pas : leur disposition doit permettre de fermer le cube sans chevauchement.')],images=('patrons',))
ex(18,'Les faces opposées','Observe le patron A–B–C–D en bande, avec E au-dessus de B et F au-dessous. Les six carrés sont identiques.',[
 row('Quelle face devient opposée à A ?','La face C.','En fermant la bande A–B–C–D, les faces A et C se retrouvent de part et d’autre du cube.'),
 row('Quelle face devient opposée à B ?','La face D.','Les faces B et D alternent avec A et C autour du cube.'),
 row('Quelle face devient opposée à E ?','La face F.','Les deux carrés ajoutés au-dessus et au-dessous ferment les deux ouvertures de la bande.'),
 row('Deux faces voisines par un côté sur un patron peuvent-elles être opposées sur le cube ?','Non.','Leur côté commun devient une arête commune ; elles restent donc voisines.'),
 row('Quelle manipulation permet de vérifier les trois paires ?','Plier le patron en gardant les lettres visibles.','On compare alors les faces qui se trouvent de part et d’autre du cube. Une règle du type « sauter une case » ne suffit pas pour tous les patrons.')],images=('patron_lettres',))
ex(18,'Compléter le patron','On dessine quatre carrés A–B–C–D en bande et un carré E au-dessus de B. On cherche une place pour le sixième carré F.',[
 row('Combien de faces sont déjà représentées ?','5 faces.','La bande contient quatre carrés et le carré E en ajoute un.'),
 row('Combien de carrés manque-t-il ?','1 carré.',r'$6-5=1$ : un cube possède six faces.'),
 row('La place juste au-dessous de B convient-elle ?','Oui.','Le carré F fermera l’ouverture opposée à celle fermée par E, sans superposition.'),
 row('La place juste au-dessus de C convient-elle ?','Non.','E et ce carré se rabattraient sur la même ouverture ; deux faces se superposeraient.'),
 row('Quelle caractéristique doit avoir le carré ajouté ?','Le même côté que les cinq autres carrés.','Les faces d’un cube sont six carrés identiques. Le carré doit aussi être relié au reste par un côté entier.')],correction=('patron_lettres',))
ex(18,'Les cubes cachés','Un assemblage comporte trois étages complets décrits ainsi : au sol, 3 rangées de 2 cubes ; au deuxième étage, 3 cubes ; au troisième, 1 cube. Aucun cube ne flotte.',[
 row('Combien de cubes contient l’étage du bas ?','6 cubes.',r'$3\times2=6$. On compte toutes les places de la base, y compris celles masquées.'),
 row('Combien contient l’étage du milieu ?','3 cubes.','Cette quantité est donnée dans la description ; ces cubes sont au-dessus de ceux du bas.'),
 row('Combien contient le dernier étage ?','1 cube.','Un seul cube est posé au sommet.'),
 row('Combien y a-t-il de cubes au total ?','10 cubes.',r'$6+3+1=10$. Chaque étage est compté une seule fois.'),
 row('Pourquoi faut-il compter des cubes invisibles sur une vue en perspective ?','Certains cubes sont cachés derrière les autres ou servent de supports.','Le nombre de cubes dépend de tout l’assemblage, pas seulement des faces que l’on voit.')])
ex(18,'La bonne vue','Un assemblage est décrit par les hauteurs de ses colonnes sur deux rangées. Rangée de devant, de gauche à droite : 1, 2, 1 cubes. Rangée de derrière : 1, 1, 0 cube. Toutes les colonnes reposent au sol.',[
 row('Combien de cubes contient la rangée de devant ?','4 cubes.',r'$1+2+1=4$. On additionne les hauteurs des trois colonnes.'),
 row('Combien de cubes contient la rangée de derrière ?','2 cubes.',r'$1+1+0=2$. La troisième place est vide.'),
 row('Combien contient tout l’assemblage ?','6 cubes.',r'$4+2=6$. On réunit les deux rangées sans les confondre avec des étages.'),
 row('Combien de cases occupées voit-on de dessus ?','5 cases.','Trois colonnes sont occupées devant et deux derrière ; la hauteur ne change pas le nombre de cases occupées au sol.'),
 row('Quelles hauteurs voit-on de face, de gauche à droite ?','1, 2 et 1 cubes.','Pour chaque colonne gauche-droite, on retient la plus grande hauteur entre devant et derrière.')],images=('hauteurs',))
ex(18,'Construire un patron','Tu veux fabriquer un cube de 3 cm d’arête à partir d’un patron.',[
 row('Combien de carrés identiques traces-tu ?','6 carrés.','Chaque carré correspond à une face du cube.'),
 row('Quelle longueur donne-tu à chaque côté de carré ?','3 cm.','Les côtés des faces deviennent les arêtes du cube.'),
 row('Décris une disposition qui convient.','Quatre carrés en bande, un au-dessus et un au-dessous du deuxième.','La bande entoure le cube ; les deux carrés supplémentaires ferment les ouvertures.'),
 row('Quels instruments garantissent des carrés exacts ?','La règle graduée et l’équerre.','La règle impose 3 cm sur chaque côté ; l’équerre impose les angles droits.'),
 row('Comment vérifies-tu ton modèle après découpage ?','Plier sur les côtés communs : les six faces doivent fermer le cube sans se chevaucher.','Les languettes de collage peuvent être ajoutées à l’extérieur du patron, sans devenir des faces supplémentaires.')],correction=('patron_lettres',))
ex(18,'Agrandir l’assemblage','Un petit assemblage de 7 cubes s’inscrit dans un bloc de 2 cubes de long, 2 de large et 2 de haut. On veut compléter ce bloc, puis construire un bloc cubique de 3 cubes de côté contenant les mêmes 7 cubes.',[
 row('Combien de cubes contient un étage du bloc de côté 2 ?','4 cubes.',r'$2\times2=4$. Il y a deux rangées de deux cubes.'),
 row('Combien de cubes contient le bloc complet de côté 2 ?','8 cubes.',r'$4\times2=8$. On superpose deux étages identiques.'),
 row('Combien faut-il ajouter de cubes aux 7 cubes pour compléter ce premier bloc ?','1 cube.',r'$8-7=1$. On calcule la place manquante dans le bloc complet.'),
 row('Combien de cubes contient le bloc de côté 3 ?','27 cubes.',r'Un étage contient $3\times3=9$ cubes. Avec trois étages, $9\times3=27$.'),
 row('Combien faut-il ajouter aux 7 cubes de départ pour obtenir ce bloc de côté 3 ?','20 cubes.',r'$27-7=20$. On repart bien des 7 cubes initiaux, pas des 8 du premier bloc.')])
ex(18,'Coder un chemin','Le pion part vers la droite de la feuille. Le chemin fait 3 cases à droite, 1 case vers le bas, puis 3 cases à gauche.',[
 row('Quelle première instruction écris-tu ?','Avancer de 3 cases.','Le pion est déjà orienté vers la droite ; il avance sans tourner.'),
 row('Quel quart de tour permet ensuite de descendre ?','Un quart de tour à droite.','Quand le pion regarde à droite de la feuille, sa droite est dirigée vers le bas.'),
 row('Après une case vers le bas, quel quart de tour permet d’aller vers la gauche de la feuille ?','Encore un quart de tour à droite.','En regardant vers le bas, tourner à droite oriente vers la gauche de la feuille.'),
 row('Quelle dernière instruction complète le chemin ?','Avancer de 3 cases.','Le pion est maintenant orienté vers la gauche ; il revient sous la colonne de départ.'),
 row('Où finit-il et dans quelle direction regarde-t-il ?','1 case sous le départ, tourné vers la gauche.','Les 3 cases à droite et les 3 cases à gauche se compensent ; la descente d’une case reste.')],images=('chemin',))
ex(18,'Exécuter un programme','Le pion part d’une case et regarde vers la droite. Programme : avancer de 2 cases ; quart de tour à gauche ; avancer de 2 cases ; quart de tour à gauche ; avancer de 1 case.',[
 row('Où arrive le pion après la première avancée ?','2 cases à droite du départ.','Il suit sa direction initiale sans changer de ligne.'),
 row('Dans quelle direction regarde-t-il après le premier quart de tour ?','Vers le haut de la feuille.','Depuis la droite de la feuille, un quart de tour à gauche oriente vers le haut.'),
 row('Où arrive-t-il après la deuxième avancée ?','2 cases à droite et 2 cases au-dessus du départ.','L’avancée verticale s’ajoute au déplacement horizontal déjà effectué.'),
 row('Dans quelle direction regarde-t-il après le deuxième quart de tour ?','Vers la gauche de la feuille.','Depuis le haut, tourner à gauche conduit vers la gauche de la feuille.'),
 row('Quelle est sa position finale ?','1 case à droite et 2 cases au-dessus du départ.','La dernière case vers la gauche retire une des deux cases vers la droite ; la hauteur reste de deux cases.')])
ex(18,'Le dé à compléter','Sur le patron A–B–C–D en bande, E est au-dessus de B et F au-dessous. A porte 1 point, B porte 2 points et E porte 3 points. Deux faces opposées du dé doivent totaliser 7 points.',[
 row('Quelle face est opposée à A ?','C.','Le pliage de la bande place A et C sur deux faces opposées.'),
 row('Combien de points écris-tu sur C ?','6 points.',r'$7-1=6$. La paire A–C totalise alors 7 points.'),
 row('Combien de points écris-tu sur D, opposée à B ?','5 points.',r'$7-2=5$. La paire B–D totalise aussi 7 points.'),
 row('Combien de points écris-tu sur F, opposée à E ?','4 points.',r'$7-3=4$. Les faces E et F ferment les deux ouvertures opposées.'),
 row('Vérifie les trois sommes de faces opposées.','$1+6=7$, $2+5=7$ et $3+4=7$.','Chaque nombre de 1 à 6 apparaît une seule fois et chaque paire opposée respecte la règle du dé.')],images=('patron_lettres',))

# Figures : constructions contrôlables, sans étiquettes sur les traits.
addfig(15,'milieu',r'\draw[geoTrait] (0,0)--(5,0);\draw[geoReponse] (2.5,-.15)--(2.5,.15);'+dots([(0,0,'A','north east'),(5,0,'B','north west'),(2.5,0,'M','south')])+label(1.25,-.65,'3,5 cm')+label(3.75,-.65,'3,5 cm'), 'Segment AB de 7 cm partagé par son milieu M en deux segments de 3,5 cm.')
addfig(15,'angles_droites',r'\draw[geoTrait] (0,0)--(2.5,0) (1,-.7)--(1,1.5);\draw[geoTrait] (1.23,0)--(1.23,.23)--(1,.23);\draw[geoTrait] (3.4,0)--(5.9,0) (3.9,-.6)--(5.3,1.3);'+label(1.1,-1.15,'Paire 1')+label(4.6,-1.15,'Paire 2'), 'Deux paires de droites sécantes ; seule la paire 1 porte le codage d’un angle droit.')
addfig(15,'paralleles',r'\draw[geoTrait] (0,0)--(4.3,0) (0,1.5)--(4.3,1.5) (.7,-.6)--(.7,2.2) (2,-.5)--(3.8,2);\draw[geoTrait] (.7,0)--(.95,0)--(.95,.25)--(.7,.25) (.7,1.5)--(.95,1.5)--(.95,1.75)--(.7,1.75);'+label(4.4,0,'(a)','west')+label(4.4,1.5,'(b)','west')+label(.7,2.2,'(f)','south')+label(3.8,2,'(c)','south west'), 'Les droites a et b sont perpendiculaires à f ; la droite c coupe a et b obliquement.')
addfig(15,'cercle',r'\draw[geoTrait] (0,0) circle(1.7);\draw[geoTrait] (-1.7,0)--(1.7,0) (0,0)--(0,1.7);'+dots([(0,0,'O','north west'),(0,1.7,'A','south'),(-1.7,0,'B','east'),(1.7,0,'C','west')])+label(-.7,.7,'3 cm'), 'Cercle de centre O, rayon OA de 3 cm et diamètre BC passant par O.')
addfig(15,'disque',r'\fill[otSky] (0,0) circle(1.7);\draw[geoReponse] (0,0) circle(1.7);\draw[geoAide] (0,0)--(0,1.7);'+dots([(0,0,'O','south east')])+label(.6,.9,'3 cm')+label(0,-2.2,'disque : intérieur et bord'), 'Disque de centre O et de rayon 3 cm ; le bord circulaire et tout l’intérieur appartiennent au disque.')
addfig(15,'programme',r'\draw[geoTrait] (0,0) rectangle(4,2.4);\draw[geoReponse] (0,0) circle(2);\fill[otNavy] (2,0) circle(1.7pt);'+dots([(0,0,'A','south east'),(4,0,'B','north west'),(4,2.4,'C','south west'),(0,2.4,'D','south east')])+label(2.3,-.55,'$M$','west')+label(2,3,'AB = 5 cm ; BC = 3 cm'), 'Rectangle ABCD de 5 cm sur 3 cm, milieu M de AB et cercle de centre A passant par M.')
addfig(15,'croises',r'\draw[geoTrait] (0,0) circle(1.8) (2.4,0) circle(1.8);\draw[geoTrait] (0,0)--(2.4,0);'+dots([(0,0,'A','east'),(2.4,0,'B','west'),(1.2,1.3416407865,'C','south'),(1.2,-1.3416407865,'D','north')])+label(1.2,2.4,'AB = 4 cm ; rayons = 3 cm'), 'Deux cercles de rayons 3 cm et de centres A et B distants de 4 cm, se coupant en C et D.')
addfig(15,'quadrillage_rectangle',r'\draw[step=.65,otRule] (-.65,-.65) grid(3.9,2.6);\draw[geoTrait] (0,0) rectangle(3.25,1.95);\draw[geoAide] (0,0)--(3.25,1.95);'+dots([(0,0,'A','north east'),(3.25,0,'B','north west'),(3.25,1.95,'C','south west'),(0,1.95,'D','south east')]), 'Rectangle ABCD de cinq carreaux sur trois, avec sa diagonale AC en pointillés.')

addfig(16,'triangles',r'\draw[geoTrait] (0,0)--(1.6,0)--(0,1.4)--cycle;\draw[geoTrait] (.2,0)--(.2,.2)--(0,.2);\draw[geoTrait] (2.5,0)--(4.1,0)--(3.3,1.6)--cycle;\draw[geoTrait] (2.82,.85)--(3,.75) (3.6,.75)--(3.78,.85);\draw[geoTrait] (4.9,0)--(6.5,0)--(5.7,1.38564)--cycle;\draw[geoTrait] (5.6,-.1)--(5.6,.1) (5.25,.77)--(5.43,.67) (5.98,.67)--(6.16,.77);'+label(.7,-.6,'Triangle 1')+label(3.3,-.6,'Triangle 2')+label(5.7,-.6,'Triangle 3'), 'Trois triangles codés : rectangle avec un angle droit, isocèle avec deux côtés égaux, équilatéral avec trois côtés égaux.')
addfig(16,'quadrilateres',r'\draw[geoTrait] (0,0) rectangle(2,1);\draw[geoTrait] (2.6,.6)--(3.6,1.4)--(4.6,.6)--(3.6,-.2)--cycle;\draw[geoTrait] (5.3,0) rectangle(6.7,1.4);'+label(1,-.7,'Figure 1')+label(3.6,-.7,'Figure 2')+label(6,-.7,'Figure 3'), 'Trois quadrilatères distincts : rectangle non carré, losange non carré incliné et carré, repérés par les numéros 1, 2 et 3.')
addfig(16,'equilateral',r'\draw[geoTrait] (0,0)--(3.2,0);\draw[geoAide] (0,0) ++(40:3.2) arc(40:80:3.2);\draw[geoAide] (3.2,0) ++(100:3.2) arc(100:140:3.2);\draw[geoReponse] (0,0)--(1.6,2.771281292)--(3.2,0);'+dots([(0,0,'B','north east'),(3.2,0,'C','north west'),(1.6,2.771281292,'A','south')])+label(1.6,-.75,'trois côtés de 4 cm'), 'Construction du triangle équilatéral ABC de côté 4 cm ; deux arcs identiques de centres B et C se rencontrent en A.')
addfig(16,'rectangle_triangle',r'\draw[geoReponse] (0,0)--(3.2,0)--(0,2.4)--cycle;\draw[geoTrait] (.25,0)--(.25,.25)--(0,.25);'+dots([(0,0,'A','north east'),(3.2,0,'B','north west'),(0,2.4,'C','south')])+label(1.6,-.6,'4 cm')+label(-.55,1.2,'3 cm','east')+label(2,1.5,'environ 5 cm','west'), 'Triangle ABC rectangle en A avec AB de 4 cm et AC de 3 cm ; BC mesure environ 5 cm par lecture à la règle.')
addfig(16,'maison',r'\draw[geoTrait] (0,0) rectangle(2.8,2.8);\draw[geoReponse] (0,0)--(1.4,-2.424871131)--(2.8,0);\draw[geoAide] (0,0)--(2.8,0);'+dots([(0,0,'A','east'),(2.8,0,'B','west'),(2.8,2.8,'C','south west'),(0,2.8,'D','south east'),(1.4,-2.424871131,'E','north')])+label(1.4,3.45,'carré et triangle de côté 4 cm'), 'Carré ABCD et triangle équilatéral ABE à l’extérieur ; le côté partagé AB ne fait pas partie du contour extérieur.')

def grid(axis='v'):
    return r'\draw[step=.55,otRule] (-2.2,-1.65) grid(2.2,1.65);'+(r'\draw[otOrange,line width=1.2pt] (0,-1.9)--(0,1.9);' if axis=='v' else r'\draw[otOrange,line width=1.2pt] (-2.45,0)--(2.45,0);')
addfig(17,'axes',r'\draw[geoTrait] (0,0) rectangle(3,1.8);\draw[otOrange,dashed,line width=1pt] (1.5,-.4)--(1.5,2.2) (-.4,.9)--(3.4,.9);'+label(1.5,-1,'rectangle : deux axes'), 'Rectangle non carré muni de son axe vertical et de son axe horizontal passant par les milieux des côtés.')
for solved in (False,True):
    suffix='corrige' if solved else 'depart'
    body=grid()+dots([(-1.1,.55,'A','south'),(-1.65,-.55,'B','south'),(-.55,1.1,'C','south')],grille=True)
    if solved:body+=dots([(1.1,.55,"A′",'south'),(1.65,-.55,"B′",'south'),(.55,1.1,"C′",'south')],'otGreenDark',grille=True)+r'\draw[geoAide] (-1.1,.55)--(1.1,.55) (-1.65,-.55)--(1.65,-.55) (-.55,1.1)--(.55,1.1);'
    addfig(17,'points_'+suffix,body,'Quadrillage avec axe vertical et points A, B, C à deux, trois et un carreaux à gauche.'+(' Leurs images sont placées en vert à égale distance à droite.' if solved else ''))
    body=grid()+r'\draw[geoTrait] (0,-1.1)--(-1.1,-1.1)--(-1.1,.55)--(-1.65,.55)--(0,1.65);'
    if solved:body+=r'\draw[geoReponse] (0,-1.1)--(1.1,-1.1)--(1.1,.55)--(1.65,.55)--(0,1.65);'
    addfig(17,'maison_'+suffix,body,'Maison sur quadrillage, demi-façade de largeur deux carreaux et demi-toit de trois carreaux autour d’un axe vertical.'+(' La moitié symétrique apparaît en vert.' if solved else ' La moitié droite est à compléter.'))
    body=grid('h')+r'\draw[geoTrait] (-1.1,.55)--(1.1,1.65);'+dots([(-1.1,.55,'A','south'),(1.1,1.65,'B','south')],grille='gauche')
    if solved:body+=r'\draw[geoReponse] (-1.1,-.55)--(1.1,-1.65);'+dots([(-1.1,-.55,"A′",'north'),(1.1,-1.65,"B′",'north')],'otGreenDark',grille='gauche')
    addfig(17,'horizontal_'+suffix,body,'Segment AB sur quadrillage avec A un carreau et B trois carreaux au-dessus d’un axe horizontal.'+(' Le segment image est tracé en vert à distances égales au-dessous.' if solved else ''))
    cells=[(-3,2),(-1,2),(-2,0),(-3,-2),(-2,-2),(-1,-2)]
    body=r'\draw[step=.55,otRule] (-2.2,-1.65) grid(2.2,1.65);'
    for x,y in cells:body+=rf'\fill[otNavy!65] ({x*.55},{y*.55}) rectangle({(x+1)*.55},{(y+1)*.55});'
    if solved:
        for x,y in cells:body+=rf'\fill[otGreen!70] ({(-x-1)*.55},{y*.55}) rectangle({(-x)*.55},{(y+1)*.55});'
    body+=r'\draw[otOrange,line width=1.2pt] (0,-1.9)--(0,1.9);'
    addfig(17,'carrelage_'+suffix,body,'Motif de six cases à gauche d’un axe vertical : deux en haut, une au milieu et trois en bas.'+(' Six cases vertes complètent le motif à droite.' if solved else ''))

def box(w,h,dx,dy):
    return rf'\draw[geoTrait] (0,0)--({w},0)--({w},{h})--(0,{h})--cycle;\draw[geoTrait] (0,{h})--({dx},{h+dy})--({w+dx},{h+dy})--({w},{h}) ({w},0)--({w+dx},{dy})--({w+dx},{h+dy});\draw[geoAide] (0,0)--({dx},{dy})--({dx},{h+dy}) ({dx},{dy})--({w+dx},{dy});'
addfig(18,'cube',box(2,2,.8,.6)+label(1,-.6,'6 faces carrées'),'Cube en perspective, avec les trois arêtes cachées en pointillés ; ses six faces sont carrées dans la réalité.')
addfig(18,'pave',box(3,1.4,.8,.6)+label(1.5,-.6,'5 cm')+label(4.2,1.3,'2 cm','west')+label(3.7,.05,'3 cm','west'),'Pavé en perspective de longueur 5 cm, largeur 3 cm et hauteur 2 cm ; les arêtes cachées sont pointillées.')
addfig(18,'familles',r'\draw[geoTrait] (0,0)--(1.8,0)--(.7,1.5)--cycle;\draw[geoTrait] (2.6,.6)--(1.5,2.1)--(.7,1.5) (1.8,0)--(2.6,.6);\draw[geoAide] (0,0)--(.8,.6)--(2.6,.6) (.8,.6)--(1.5,2.1);\draw[geoTrait] (3.7,0)--(5.5,0)--(6.1,.65)--(4.6,2.3)--(3.7,0) (5.5,0)--(4.6,2.3);\draw[geoAide] (3.7,0)--(4.3,.65)--(6.1,.65) (4.3,.65)--(4.6,2.3);'+label(1.3,-.65,'prisme droit')+label(4.9,-.65,'pyramide'),'Prisme droit à bases triangulaires et pyramide à base carrée, représentés avec les arêtes invisibles en pointillés.')
addfig(18,'solides_courbes',r'\draw[geoTrait] (0,0) ellipse(.6 and .2);\draw[geoTrait] (-.6,0)--(-.6,1.4) (.6,0)--(.6,1.4);\draw[geoTrait] (0,1.4) ellipse(.6 and .2);\draw[geoTrait] (1.7,0) ellipse(.6 and .2);\draw[geoTrait] (1.1,0)--(1.7,1.5)--(2.3,0);\draw[geoTrait] (3.5,.7) circle(.75);\draw[geoAide] (2.75,.7) arc(180:360:.75 and .2);'+label(0,-.6,'cylindre')+label(1.7,-.6,'cône')+label(3.5,-.6,'boule'),'Trois solides à surface courbe : cylindre avec deux bases circulaires, cône avec une base et une pointe, boule sans face plate.')
NETS={'A':[(0,0),(1,0),(2,0),(3,0),(1,1),(1,-1)],'B':[(0,0),(1,0),(2,0),(3,0),(1,1),(2,1)],'C':[(-1,0),(0,0),(1,0),(0,-1),(0,-2),(0,-3)]}
body=''
for title,(ox,oy) in zip('ABC',[(0,0),(0,-3),(4,0)]):
    for x,y in NETS[title]:body+=rf'\draw[geoTrait,fill=otSky] ({ox+x*.65},{oy+y*.65}) rectangle({ox+(x+1)*.65},{oy+(y+1)*.65});'
    body+=label(ox+.9,oy-1.2 if title!='C' else oy-2.65,title)
addfig(18,'patrons',body,'Trois dispositions de six carrés : A et C sont des patrons de cube ; dans B, deux faces se superposent au pliage.')
body=''
for name,(x,y) in zip('ABCDEF',NETS['A']):
    body+=rf'\draw[geoTrait,fill=otSky] ({x*.9},{y*.9}) rectangle({(x+1)*.9},{(y+1)*.9});'+label((x+.5)*.9,(y+.5)*.9,name)
addfig(18,'patron_lettres',body,'Patron de cube : A, B, C et D forment une bande ; E est au-dessus de B et F au-dessous. Les paires opposées sont A–C, B–D et E–F.')
body=''
for y,heights in enumerate(([1,2,1],[1,1,0])):
    for x,height in enumerate(heights):body+=rf'\draw[geoTrait,fill=otSky] ({x*.9},{y*.9}) rectangle({(x+1)*.9},{(y+1)*.9});'+label((x+.5)*.9,(y+.5)*.9,str(height))
body+=label(1.35,-.6,'devant')+label(1.35,2.3,'derrière')+label(1.35,3,'hauteur de chaque colonne')
addfig(18,'hauteurs',body,'Plan de hauteurs d’un assemblage : devant 1, 2 et 1 cubes ; derrière 1, 1 et 0 cube. Zéro indique une case vide.')
addfig(18,'chemin',r'\draw[step=.7,otRule] (-.7,-1.4) grid(2.8,1.4);\draw[geoVecteur] (0,0)--(2.1,0)--(2.1,-.7)--(0,-.7);'+dots([(0,0,'départ','south'),(0,-.7,'but','north')])+label(1.05,.7,'départ vers la droite'), 'Chemin sur quadrillage : trois cases à droite, une case vers le bas, trois cases à gauche ; but une case sous le départ.')

COURS={15:r'''Titre: Droites, cercles et constructions
<!-- optitab:1 -->
::: objectifs
- Décrire points, segments, droites et cercles avec des mots précis.
- Construire et contrôler perpendiculaires et parallèles avec les instruments.
- Lire les codes, placer un milieu et suivre un programme de construction.
:::

## I. Choisir les mots et les instruments
::: definition Droite, segment, demi-droite
Le **segment [AB]** est la portion de droite limitée par ses deux extrémités A et B. Sa longueur s’écrit AB. La **droite (AB)** se prolonge sans fin des deux côtés. La **demi-droite [AB)** commence en A et se prolonge au-delà de B.
:::

Les symboles accompagnent les mots : on dit « le segment [AB] » ou « la droite (AB) ». Un point se marque précisément par une petite croix ou un petit point, puis se nomme par une lettre.

::: methode Le bon outil
La règle trace droit ; la règle graduée mesure des longueurs. L’équerre construit et contrôle les angles droits. Le compas reporte une longueur sans changer son ouverture et trace les cercles.
:::

::: propriete Milieu et codes
Le **milieu** d’un segment appartient à ce segment et partage sa longueur en deux moitiés égales. Des petits traits identiques codent des longueurs égales ; un petit carré code un angle droit.
:::

::: exemple Un segment de 7 cm
Son milieu M est situé entre A et B, à $7\div2=3{,}5$ cm de chacun. Un point hors du segment ne peut pas être son milieu, même s’il est à égale distance des deux extrémités.
:::
[IMAGE_1]

## II. Perpendiculaires et parallèles
::: definition Deux relations différentes
Deux droites **perpendiculaires** se coupent à angle droit. Deux droites **parallèles distinctes** ne se coupent jamais, même prolongées. Elles gardent la même direction.
:::
[IMAGE_2]

::: methode Tracer une perpendiculaire par un point
Pose un côté de l’angle droit de l’équerre sur la droite donnée. Fais glisser l’équerre sans la tourner jusqu’à ce que son autre côté passe par le point. Trace le long de ce bord et contrôle l’angle droit.
:::

::: methode Tracer une parallèle par un point
Pose un bord de l’équerre sur la droite et une règle contre un autre bord. Garde la règle immobile : elle sert de rail. Fais coulisser l’équerre jusqu’au point, puis trace le long du bord qui a gardé la direction initiale.
:::

Deux droites distinctes perpendiculaires à une même droite sont parallèles. Cela permet aussi un contrôle avec l’équerre.

::: attention Le dessin ne prouve pas tout
Deux traits peuvent se couper au-delà de la feuille. Deux droites peuvent se couper sans être perpendiculaires. Utilise les données, les codes et les instruments ; ne conclus pas seulement à l’œil.
:::

## III. Cercle et disque
::: definition À la même distance du centre
Le cercle de centre O et de rayon 3 cm rassemble les points situés **exactement à 3 cm de O**. Le disque contient ces points et tous ceux situés à moins de 3 cm. Le rayon relie le centre à un point du cercle. Un diamètre relie deux points du cercle en passant par le centre : il mesure deux rayons.
:::
[IMAGE_3]

::: exemple Rayon et diamètre
Un rayon de 4 cm donne un diamètre de $4\times2=8$ cm. Pour un diamètre de 7 cm, le rayon vaut $7\div2=3{,}5$ cm. L’ouverture du compas correspond toujours au rayon.
:::

## IV. Suivre puis contrôler un programme
::: methode Une construction étape par étape
Lis tout le programme. Fais un croquis avec les codes utiles. Construis d’abord les objets dont dépendent les suivants. Pour chaque phrase, repère les points déjà placés et choisis l’instrument. Contrôle enfin les longueurs, les angles droits et les passages par les points demandés.
:::

::: retenir
Un milieu est **sur** le segment ; une perpendiculaire forme un angle droit ; une parallèle garde la direction. Le cercle est un bord, le disque inclut l’intérieur. Une figure réussie respecte toutes les contraintes, même si on change son orientation sur la feuille.
:::
''',16:r'''Titre: Triangles et quadrilatères
<!-- optitab:1 -->
::: objectifs
- Reconnaître les figures par leurs propriétés, même lorsqu’elles sont inclinées.
- Construire triangles, carrés et rectangles avec les instruments.
- Utiliser les longueurs, les angles droits et les codes pour justifier.
:::

## I. Les triangles
::: definition Trois côtés et trois sommets
Un **triangle** a trois côtés. Il est **rectangle** s’il possède un angle droit, **isocèle** s’il possède deux côtés de même longueur, **équilatéral** si ses trois côtés ont la même longueur.
:::
[IMAGE_1]

::: propriete Plusieurs propriétés peuvent se combiner
Un triangle rectangle peut aussi être isocèle. Dans un triangle isocèle, les deux angles de la base sont égaux. Dans un triangle équilatéral, les trois angles sont égaux. On compare leurs ouvertures avec un gabarit ; aucun calcul en degrés n’est nécessaire ici.
:::

::: attention Ce qui est prouvé
Un même code sur deux côtés affirme leur égalité. L’absence de code ne prouve pas qu’ils sont différents. Un dessin à main levée prépare la construction, mais ne remplace pas les données ou le contrôle aux instruments.
:::

## II. Construire un triangle
::: methode Un triangle équilatéral de côté 4 cm
Trace le segment [BC] de 4 cm. Ouvre le compas à 4 cm. Trace un arc de centre B, puis un arc de centre C sans modifier l’ouverture. Leur rencontre donne A. Relie A à B et A à C ; garde les arcs visibles pour expliquer ta méthode.
:::
[IMAGE_2]

Pour un triangle isocèle de base 4 cm et de côtés égaux de 6 cm, trace d’abord la base, puis deux arcs de 6 cm depuis ses extrémités. Pour un triangle rectangle, construis d’abord l’angle droit à l’équerre, reporte les deux longueurs depuis son sommet et relie les deux points.

::: methode Contrôler
Mesure les côtés avec la règle graduée ou compare-les au compas. Vérifie l’angle droit avec l’équerre. N’ajoute un code qu’après avoir construit ou vérifié la propriété correspondante.
:::

## III. Carré, rectangle et losange
::: definition Des quadrilatères particuliers
Un **quadrilatère** a quatre côtés. Un **rectangle** a quatre angles droits. Un **losange** a quatre côtés de même longueur. Un **carré** réunit ces deux propriétés : quatre angles droits et quatre côtés égaux.
:::
[IMAGE_3]

::: propriete Côtés opposés
Dans le rectangle, les côtés opposés sont parallèles et de même longueur. Dans le losange et le carré, les côtés opposés sont aussi parallèles. Le carré est donc à la fois un rectangle et un losange.
:::

::: attention Une figure inclinée garde sa nature
Un carré posé sur la pointe reste un carré. Quatre côtés égaux seuls prouvent qu’une figure est un losange, sans garantir qu’elle soit un carré : il faut aussi contrôler les angles droits.
:::

## IV. Construire et expliquer
::: methode Rectangle de 6 cm sur 4 cm
Trace le segment [AB] de 6 cm. Construis les perpendiculaires à ce segment en A et en B. Du même côté, place D à 4 cm de A et C à 4 cm de B. Relie C à D. Contrôle les quatre angles droits et les longueurs opposées. Pour un carré, reporte la même longueur pour les deux dimensions.
:::

::: exemple Un contour à calculer
Le rectangle de 6 cm sur 4 cm a pour périmètre $6+4+6+4=20$ cm. Un carré de côté 5 cm a aussi un périmètre de $5\times4=20$ cm. Un même tour n’impose donc pas une même forme.
:::

Les diagonales d’un rectangle joignent ses sommets opposés : les segments [AC] et [BD]. Elles ont la même longueur et se coupent en leur milieu. On peut le vérifier sur une construction soignée.

::: retenir
Observe les propriétés des côtés et des angles, pas la position du dessin. Pour construire, commence par les données connues, utilise les bons instruments et relis chaque contrainte du programme.
:::
''',17:r'''Titre: Symétrie sur quadrillage
<!-- optitab:1 -->
::: objectifs
- Reconnaître un axe de symétrie par pliage.
- Construire des points et des figures images sur un quadrillage.
- Compléter des motifs avec un axe vertical ou horizontal.
:::

## I. Reconnaître un axe
::: definition Le test du pliage
Une droite est un **axe de symétrie** d’une figure si, en pliant suivant cette droite, les deux parties se superposent exactement. Tous les contours et les détails doivent coïncider.
:::
[IMAGE_1]

Un rectangle non carré possède deux axes : les droites qui passent par les milieux des côtés opposés. Un carré en possède quatre. Une figure peut donc avoir aucun axe, un axe ou plusieurs axes. Les axes se vérifient sur le dessin précis : une lettre décorée peut perdre les symétries d’une lettre simple.

::: attention Partager ne suffit pas
Une droite peut découper une figure en deux parties de même aire sans être un axe. Il faut que les parties se superposent par pliage, pas seulement qu’elles contiennent le même nombre de cases.
:::

## II. Avec un axe vertical
::: methode Construire l’image d’un point
Repère la ligne horizontale du point. Compte les carreaux jusqu’à l’axe. De l’autre côté, reporte exactement le même nombre de carreaux sur cette même ligne. Nomme le nouveau point : A′ se lit « A prime » et désigne l’image de A.
:::
[IMAGE_2]

::: exemple À deux carreaux du pli
Si A est à deux carreaux à gauche de l’axe, A′ est à deux carreaux à droite, sur la même ligne. La distance entre A et A′ vaut $2+2=4$ carreaux. L’axe est au milieu de ce trajet.
:::

## III. Avec un axe horizontal
::: methode Changer de direction de comptage
Repère la colonne du point. Compte verticalement jusqu’à l’axe, puis reporte la même distance de l’autre côté dans cette colonne. Un point au-dessus a son image au-dessous ; un point au-dessous a son image au-dessus.
:::
[IMAGE_3]

::: propriete Les points du pli restent en place
Un point situé sur l’axe est son propre symétrique : il ne se déplace pas. Pour un segment qui commence sur l’axe, son segment image commence donc au même point.
:::

## IV. Compléter une figure
::: methode Des points avant les traits
Repère tous les sommets utiles. Construis l’image de chacun sur la bonne ligne ou dans la bonne colonne. Relie les points images dans le même ordre que les points de départ. Reproduis aussi les détails : une tache, une fenêtre ou une case colorée doit avoir son image.
:::

Pour une case colorée, compte les cases jusqu’au pli et colorie sa correspondante à la même distance. Avec deux axes, complète d’abord par rapport à l’un, puis reflète **tout** le résultat par rapport à l’autre : les quatre quarts sont alors présents.

::: propriete Ce qui est conservé
La symétrie conserve les longueurs et la forme. Le symétrique d’un segment mesure autant que ce segment. Un carré reste un carré ; un angle droit reste droit. C’est le pliage qui permet de comprendre ces conservations.
:::

::: attention Trois contrôles
Être de l’autre côté de l’axe ne suffit pas. Vérifie la bonne ligne pour un axe vertical, la bonne colonne pour un axe horizontal, puis la même distance à l’axe. Ne déplace pas les points qui sont sur le pli.
:::

::: retenir
**Axe vertical : même ligne. Axe horizontal : même colonne.** Dans les deux cas, reporte une distance égale de l’autre côté. Construis les images des sommets avant de relier et contrôle par pliage quand c’est possible.
:::
''',18:r'''Titre: Solides, patrons et espace
<!-- optitab:1 -->
::: objectifs
- Reconnaître et décrire les solides, y compris en perspective.
- Construire des modèles et reconnaître un patron de cube.
- Compter des assemblages et suivre des programmes de déplacement.
:::

## I. Reconnaître les solides
::: definition Des objets de l’espace
Un **solide** occupe une place dans l’espace. Le cube, le pavé, la pyramide et le prisme droit n’ont que des faces plates : ce sont des polyèdres. La boule, le cylindre et le cône possèdent une surface courbe. La boule n’a aucune face plate ; le cylindre a deux bases circulaires et le cône une base circulaire et une pointe.
:::
[IMAGE_1]

Une **face** est une surface plate du solide. Une **arête** est un segment où deux faces se rencontrent. Un **sommet** est un point où des arêtes se rejoignent. On s’entraîne en tenant un modèle et en montrant chaque élément.

## II. Décrire et fabriquer
::: propriete Cube et pavé
Le cube possède **6 faces carrées, 12 arêtes et 8 sommets**. Le pavé possède **6 faces rectangulaires, 12 arêtes et 8 sommets** ; ses faces opposées sont superposables. Un carré étant un rectangle particulier, le cube est aussi un pavé particulier.
:::
[IMAGE_2]

::: definition Pyramide et prisme droit
Une pyramide possède une base et des faces latérales triangulaires qui se rejoignent au même sommet. Une pyramide à base carrée a une base carrée et quatre triangles. Un prisme droit possède deux bases superposables et parallèles, reliées par des rectangles. Avec des bases triangulaires, il a deux triangles et trois rectangles.
:::
[IMAGE_3]

::: methode Construire un modèle
Prépare les faces en carton aux dimensions compatibles. Pour un pavé de 5 cm sur 3 cm sur 2 cm, prépare deux rectangles de 5 cm sur 3 cm, deux de 5 cm sur 2 cm et deux de 3 cm sur 2 cm. Pour une pyramide à base carrée, associe un carré et quatre triangles adaptés. Pour un prisme triangulaire, associe deux triangles identiques et trois rectangles dont les largeurs correspondent aux côtés des triangles. Assemble avec du ruban adhésif et contrôle que le solide se ferme.
:::

::: attention Lire une perspective
Certaines faces et arêtes sont cachées ; les arêtes invisibles peuvent être tracées en pointillés. Un carré peut sembler penché sur le dessin : cela ne transforme pas la face réelle. Compte aussi ce qui est derrière et dessous.
:::

## III. Le patron du cube
::: definition Déplier puis replier
Un **patron** est un dessin d’un seul tenant qui permet de reconstruire un solide en pliant le long des côtés communs. Le patron d’un cube contient six carrés identiques. Leur disposition doit permettre de fermer le cube sans superposition.
:::
[IMAGE_4]

::: methode Tester une disposition
Choisis une face de départ et relève mentalement les carrés voisins. En cas de doute, découpe une copie et plie-la. Quatre carrés en bande avec un carré au-dessus et un au-dessous du deuxième donnent un patron. Six carrés assemblés ne constituent pas toujours un patron : deux peuvent se rabattre au même endroit.
:::

## IV. Assemblages et déplacements
::: methode Compter tous les cubes
Compte étage par étage, ou additionne les hauteurs des colonnes quand elles sont données. Dans une vue de dessus, chaque case occupée indique une colonne, pas forcément un seul cube. Les cubes cachés ou porteurs font partie du total.
:::

::: exemple Trois étages
Un étage de six cubes, puis un de trois cubes, puis un d’un cube donnent $6+3+1=10$ cubes. Une vue montrant moins de dix cubes ne change pas ce total.
:::

::: methode Exécuter un déplacement
Marque le départ **et la direction de regard**. Une instruction « avancer » suit cette direction. Un quart de tour change l’orientation sans changer la case. Mets à jour le regard après chaque tour, puis continue. Pour coder un chemin, sépare les avancées et les changements de direction.
:::

::: attention La droite de qui ?
La droite du pion dépend de son orientation. Quand il regarde à droite de la feuille, tourner à droite le fait regarder vers le bas. Suis son regard plutôt que ta propre droite.
:::

::: retenir
Décris les faces pour identifier un solide. Un patron doit se fermer sans chevauchement. Compte les cubes cachés et garde la direction du pion en mémoire à chaque instruction.
:::
'''}

FICHES={15:r'''Titre: L’essentiel : droites et cercles
<!-- optitab:1 -->
## I. Mots et outils
::: retenir
- Le segment [AB] a deux extrémités ; la droite (AB) se prolonge des deux côtés ; la demi-droite [AB) part de A.
- La règle graduée mesure, l’équerre contrôle les angles droits, le compas reporte une longueur et trace un cercle.
- Le milieu est **sur** le segment et à égale distance des extrémités.
:::
## II. Construire et contrôler
::: methode
Pour une perpendiculaire, garde un côté de l’angle droit de l’équerre sur la droite et fais passer l’autre par le point. Pour une parallèle, fais glisser l’équerre le long d’une règle fixe sans la tourner.
:::
## III. Le cercle
::: retenir
Le cercle rassemble les points à une distance exactement égale au rayon du centre. Le disque ajoute l’intérieur. Un diamètre passe par le centre et mesure deux rayons. Pour tracer au compas, règle l’ouverture sur le rayon.
:::
::: attention
Un trait qui ne croise pas une droite sur le dessin n’est pas forcément parallèle. Lis les codes, utilise les instruments et vérifie chaque contrainte du programme.
:::
''',16:r'''Titre: L’essentiel : triangles et quadrilatères
<!-- optitab:1 -->
## I. Reconnaître
| Figure | Propriété essentielle |
|---|---|
| Triangle rectangle | Un angle droit |
| Triangle isocèle | Deux côtés égaux |
| Triangle équilatéral | Trois côtés égaux |
| Rectangle | Quatre angles droits |
| Losange | Quatre côtés égaux |
| Carré | Quatre côtés égaux et quatre angles droits |

## II. Construire
::: methode
Pour un triangle équilatéral, trace un côté, puis deux arcs de même rayon depuis ses extrémités. Pour un triangle rectangle, commence par l’angle droit. Pour un rectangle ou un carré, trace un côté, puis les perpendiculaires à ses extrémités et reporte les longueurs du même côté.
:::

::: retenir
Dans rectangle, losange et carré, les côtés opposés sont parallèles. Le carré est à la fois rectangle et losange. Un périmètre se calcule en additionnant les côtés du contour.
:::
::: attention
Une figure inclinée garde sa nature. Les codes donnent des propriétés ; l’absence de code ne prouve pas le contraire. Contrôle les longueurs et les angles avec les instruments.
:::
''',17:r'''Titre: L’essentiel : symétrie
<!-- optitab:1 -->
## I. Le pliage
::: definition
Un axe de symétrie permet de superposer exactement les deux parties d’une figure par pliage. Les détails intérieurs comptent aussi.
:::
## II. Sur quadrillage
::: methode
**Axe vertical :** garde la même ligne horizontale et reporte la distance de l’autre côté.

**Axe horizontal :** garde la même colonne et reporte la distance de l’autre côté.

Construis l’image de chaque sommet, puis relie les images dans le même ordre.
:::
## III. À conserver
::: retenir
Un point de l’axe reste au même endroit. La symétrie conserve les longueurs, la forme et les angles droits. Pour deux axes, reflète d’abord le motif selon l’un, puis tout le résultat selon l’autre.
:::
::: attention
Être de l’autre côté ne suffit pas : il faut aussi la bonne ligne ou colonne et la même distance au pli. Deux parties de même aire ne sont pas forcément symétriques.
:::
''',18:r'''Titre: L’essentiel : solides et espace
<!-- optitab:1 -->
## I. Décrire les solides
::: retenir
- Cube : 6 faces carrées, 12 arêtes, 8 sommets.
- Pavé : 6 faces rectangulaires, 12 arêtes, 8 sommets ; faces opposées superposables.
- Pyramide : une base et des triangles réunis au sommet.
- Prisme droit : deux bases superposables et parallèles, reliées par des rectangles.
- Boule : aucune face plate ; cylindre : deux bases circulaires ; cône : une base circulaire et une pointe.
:::
## II. Patron et assemblage
::: methode
Un patron de cube comporte 6 carrés identiques bien disposés. Teste le pliage : aucune face ne manque ou ne se superpose. Pour un assemblage, compte étage par étage ou colonne par colonne, y compris les cubes cachés.
:::
## III. Se déplacer
::: methode
Repère le départ et l’orientation du pion. Avancer suit son regard ; un quart de tour modifie sa direction sans le déplacer. Actualise son orientation après chaque instruction.
:::
::: attention
Une perspective cache des éléments. Une case occupée en vue de dessus peut porter plusieurs cubes. La droite du pion dépend de son orientation.
:::
'''}

COURSEFIG={15:['milieu','paralleles','cercle'],16:['triangles','equilateral','quadrilateres'],17:['axes','points_corrige','horizontal_corrige'],18:['solides_courbes','cube','familles','patron_lettres']}
def methode_precise(q,r):
    t=q.lower();s=r.lower()
    if 'périmètre' in t or 'contour extérieur' in t:return 'Additionner seulement les côtés du contour demandé.'
    if 'diamètre' in t or 'rayon' in t or 'ouverture' in t and 'compas' in t:
        return 'Relier la longueur demandée au rayon et au diamètre.' if 'diamètre' in s or 'rayon' in s else 'Conserver l’ouverture du compas qui impose la longueur donnée.'
    if 'milieu' in t or 'calcule am' in t or 'longueur mb' in t:return 'Partager le segment en deux longueurs égales et rester sur le segment.'
    if 'quel instrument' in t or 'quels instruments' in t:return 'Associer chaque instrument à ce qu’il permet de construire ou de vérifier.'
    if 'patron' in t or 'pliage' in t or 'plie' in t:return 'Imaginer le pliage face par face et contrôler les superpositions.'
    if 'opposée' in t or 'opposées' in t:return 'Repérer les faces qui se font face après le pliage.'
    if 'points écris' in t or 'sommes' in t:return 'Compléter chaque paire pour obtenir un total de sept.'
    if 'regarde' in t or 'quart de tour' in t or 'direction' in t:return 'Se placer dans le sens du regard du pion avant de tourner.'
    if 'arrive' in t or 'position finale' in t or 'finit-il' in t:return 'Suivre les déplacements dans l’ordre en gardant l’orientation à jour.'
    if 'instruction' in t or 'chemin' in t:return 'Séparer les avancées des changements de direction.'
    if 'cubes' in t or 'étage' in t:return 'Dénombrer par étages ou par colonnes sans oublier les éléments cachés.'
    if 'face' in t or 'arête' in t or 'sommet' in t and 'solide' in s:return 'Décrire toutes les parties du solide, visibles et cachées.'
    if 'case' in t or 'cases' in t:
        return 'Associer chaque case à son image, puis compter les cases distinctes.'
    if 'symétr' in t or 'axe' in t or 'places-tu' in t and ('carreau' in s or 'axe' in s):
        if 'colonne' in s:return 'Conserver la colonne et reporter la distance de l’autre côté du pli horizontal.'
        if 'ligne' in s:return 'Conserver la ligne et reporter la distance de l’autre côté du pli vertical.'
        if 'pli' in s or 'superpos' in s:return 'Tester la superposition exacte par pliage.'
        return 'Repérer la position du point par rapport au pli et conserver sa distance.'
    if 'perpendic' in t or 'angle' in t:return 'Construire ou contrôler un angle droit avec l’équerre.'
    if 'parallèl' in t or 'prolonge' in t:return 'Contrôler la direction des droites avec les instruments.'
    if 'carte' in t or 'premier' in t or 'ensuite' in t:return 'Respecter l’ordre des objets nécessaires à chaque étape.'
    if 'code' in t or 'codage' in t:return 'Traduire exactement les égalités ou l’angle droit donnés.'
    if 'nature' in t or 'nom' in t or 'rectangle' in t or 'carré' in t or 'triangle' in t:return 'Comparer les propriétés des côtés et des angles à la définition de la figure.'
    if 'calcule' in t or 'combien' in t:return 'Utiliser les données utiles en conservant leur unité.'
    if 'constru' in t or 'trace' in t or 'relie' in t:return 'Repérer les points déjà placés, puis choisir le tracé qui respecte le programme.'
    if 'vrai' in t or 'faux' in t or 'toujours' in t or 'forcément' in t:return 'Tester la phrase avec la définition et chercher un cas qui la contredit.'
    if 'longueur' in t or 'distance' in t:return 'Identifier la longueur connue et la propriété qui relie les deux mesures.'
    if 'contrôle' in t or 'vérifi' in t:return 'Reprendre chaque contrainte et la contrôler séparément.'
    return 'S’appuyer sur la propriété utile, puis justifier avec les données de la situation.'
def write():
    for n,d in DOS.items():
        assert len(DATA[n])==15
        for e in DATA[n]:
            for q in e['questions']:
                if q['methode']=='Utiliser la définition et les informations données.':q['methode']=methode_precise(q['question'],q['raisonnement'])
        (d/'cours_nouveau.txt').write_text(COURS[n],encoding='utf-8');(d/'fiche_nouvelle.txt').write_text(FICHES[n],encoding='utf-8')
        blocks=[]
        for i,data in enumerate(DATA[n],1):
            level='easy' if i<=5 else 'medium' if i<=10 else 'hard';prefix='Découverte' if i<=5 else 'Entraînement' if i<=10 else 'Problème'
            context=data['contexte'];questions='\n'.join(f'{j}. {q["question"]}' for j,q in enumerate(data['questions'],1))
            imagepart='\n\n'+'\n\n'.join(f'[IMAGE_{j}]' for j,_ in enumerate(data['images'],1)) if data['images'] else ''
            steps=[]
            for j,q in enumerate(data['questions'],1):
                steps.append(f'## Question {j} : {q["question"]}\n\n::: methode\n{q["methode"]}\n:::\n\n::: etape Raisonnement\n{q["raisonnement"]}\n:::\n\n::: resultat\n{q["reponse"]}\n:::')
            for j,name in enumerate(data['correction'],len(data['images'])+1):steps.append(f'[IMAGE_{j}]')
            solutions='\n'.join(f'{j}. {q["reponse"]}' for j,q in enumerate(data['questions'],1))
            blocks.append(f'=== {prefix} - {data["titre"]}\nId: nouveau-{i}\nDifficulté: {level}\nÉnoncé:\n<!-- optitab:1 -->\n{context}{imagepart}\n\n{questions}\n\nÉtapes:\n<!-- optitab:1 -->\n'+ '\n\n'.join(steps)+f'\n\nSolution:\n<!-- optitab:1 -->\n{solutions}\n')
            if data['images'] or data['correction']:COR[n]['exercices'][f'nouveau-{i}']={str(j):entry(n,name) for j,name in enumerate(data['images']+data['correction'],1)}
        (d/'exercices.txt').write_text('\n===\n\n'.join(blocks),encoding='utf-8')
        for j,name in enumerate(COURSEFIG[n],1):COR[n]['cours']['nouveau'][str(j)]=entry(n,name)
        p=d/'figures';p.mkdir(exist_ok=True)
        (p/'figures.py').write_text('# -*- coding: utf-8 -*-\nFIGURES = '+repr(FIG[n])+'\n',encoding='utf-8')
        (p/'correspondance.json').write_text(json.dumps(COR[n],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (d/'donnees_questions.json').write_text(json.dumps(DATA[n],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'cm1_geometrie','maj':'2026-11-01'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(n,len(DATA[n]),sum(len(e['questions']) for e in DATA[n]),len(FIG[n]))
if __name__=='__main__':write()
