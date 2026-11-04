from commun_redaction import *
def calc(expr,result):return eq(expr.replace('*',chr(92)+'times').replace('/',chr(92)+'div'),result)
def E(title,intro,qs,params=None,figures=None):
 item=ex(title,intro,qs,figures=figures);item['parametres']=params or {};return item
L=[]
L.append(E('Lire deux règles', 'Lis les graduations des deux règles dessinées ; ne mesure pas ton écran.\n\n[IMAGE_1]',[
 q('Quelle unité est utilisée ?','Lis la légende de la règle.','Les nombres correspondent à des millimètres.','L’unité est le millimètre (mm).'),
 q('Quelle est la longueur du segment A ?','Retire la lecture du début de celle de la fin.',calc('63-10',53),'A mesure 53 mm.'),
 q('Quelle est la longueur du segment B ?','Fais la même différence.',calc('82-10',72),'B mesure 72 mm.'),
 q('Quel segment est le plus long et de combien ?','Compare dans la même unité.',calc('72-53',19),'B est plus long de 19 mm.'),
 q('Écris la longueur de A en centimètres et millimètres.','Regroupe les millimètres par dix.','53 mm = 50 mm + 3 mm ; 50 mm font 5 cm.','A mesure 5 cm et 3 mm.')],{'famille':'regles','debuts':[10,10],'fins':[63,82]}, {'1':'deux_regles.png'}))
L.append(E('Échanger les unités', 'On dispose d’un ruban de 6 cm, d’une bande de 3 dm et d’une ficelle de 4 m.',[
 q('Combien de millimètres contient un centimètre ?','Utilise la relation connue.','Dix petits millimètres forment un centimètre.','1 cm = 10 mm.'),
 q('Écris 6 cm en millimètres.','Réunis six groupes de dix.',calc('6*10',60),'6 cm = 60 mm.'),
 q('Écris 3 dm en centimètres.','Un décimètre contient dix centimètres.',calc('3*10',30),'3 dm = 30 cm.'),
 q('Écris 4 m en centimètres.','Un mètre contient cent centimètres.',calc('4*100',400),'4 m = 400 cm.'),
 q('Range les trois objets du plus court au plus long.','Exprime les trois longueurs en centimètres.','Leurs longueurs sont 6 cm, 30 cm et 400 cm.','Ruban, puis bande, puis ficelle.')],{'famille':'conversions','cm':6,'dm':3,'m':4}))
L.append(E('Deux trajets', 'Un trajet A mesure 7 km. Un trajet B mesure 3 km et 250 m.',[
 q('Combien de mètres vaut un kilomètre ?','Rappelle la relation entre les unités.','Le kilomètre contient mille mètres.','1 km = 1 000 m.'),
 q('Écris le trajet A en mètres.','Réunis sept milliers de mètres.',calc('7*1000',7000),'A mesure 7 000 m.'),
 q('Écris le trajet B en mètres.','Convertis les kilomètres puis ajoute les mètres.',calc('3000+250',3250),'B mesure 3 250 m.'),
 q('Quel trajet est le plus court ?','Compare les nombres de mètres.','$3250<7000$.','B est le plus court.'),
 q('Quelle distance sépare les longueurs des deux trajets ?','Retire la plus petite longueur de la plus grande.',calc('7000-3250',3750),'La différence est 3 750 m.')],{'famille':'trajets','a_km':7,'b_km':3,'b_m':250}))
L.append(E('Décomposer 248 cm', 'Une baguette mesure 248 cm. On cherche différentes écritures de cette longueur.',[
 q('Combien de mètres entiers contient-elle ?','Cherche les groupes de cent centimètres.','248 cm contiennent deux groupes de 100 cm.','Elle contient 2 m entiers.'),
 q('Combien de centimètres restent après ces mètres ?','Retire les deux mètres.',calc('248-200',48),'Il reste 48 cm.'),
 q('Écris la longueur en mètres et centimètres.','Réunis les deux informations.','Deux mètres et encore 48 cm représentent toute la baguette.','248 cm = 2 m et 48 cm.'),
 q('Écris-la en mètres, décimètres et centimètres.','Décompose les 48 cm.','48 cm = 40 cm + 8 cm, soit 4 dm et 8 cm.','248 cm = 2 m, 4 dm et 8 cm.'),
 q('Vérifie cette dernière décomposition en centimètres.','Reconvertis chaque partie.',calc('200+40+8',248),'On retrouve 248 cm.')],{'famille':'decomposition','cm':248}))
L.append(E('Comparer avec une unité commune', 'Compare les longueurs suivantes en faisant attention aux unités.',[
 q('Écris 8 cm et 5 mm en millimètres.','Convertis les centimètres avant d’ajouter.',calc('80+5',85),'8 cm et 5 mm = 85 mm.'),
 q('Compare cette longueur à 84 mm.','Compare les nombres de millimètres.','$85>84$.','8 cm et 5 mm > 84 mm.'),
 q('Compare 2 m à 195 cm.','Écris deux mètres en centimètres.','2 m = 200 cm ; $200>195$.','2 m > 195 cm.'),
 q('Compare 4 km à 4 050 m.','Exprime les deux distances en mètres.','4 km = 4 000 m ; $4000<4050$.','4 km < 4 050 m.'),
 q('De combien 2 m dépassent-ils 195 cm ?','Calcule la différence dans la même unité.',calc('200-195',5),'2 m dépassent 195 cm de 5 cm.')],{'famille':'comparaisons'}))
L.append(E('Tracer deux segments', 'Sur ta feuille, prépare une règle graduée pour tracer A de 5 cm et 7 mm et B de 68 mm.',[
 q('Quelle longueur en millimètres faut-il pour A ?','Convertis les centimètres.',calc('50+7',57),'A doit mesurer 57 mm.'),
 q('Où placer le zéro de la règle ?','Pars du début du segment.','Le zéro doit coïncider avec la première extrémité.','Au début du segment.'),
 q('Comment placer l’autre extrémité de B ?','Lis la graduation demandée.','En gardant le début au zéro, marque un point à 68 mm puis relie les deux points.','À la graduation 68 mm.'),
 q('De combien B dépasse-t-il A ?','Compare les deux longueurs en millimètres.',calc('68-57',11),'B dépasse A de 11 mm.'),
 q('Comment contrôler tes deux tracés ?','Reprends la mesure depuis zéro.','Vérifie les deux extrémités, le zéro et les lectures 57 mm et 68 mm ; ne mesure pas depuis le bord non gradué de la règle.','A : 57 mm ; B : 68 mm, lus depuis zéro.')],{'famille':'traces','a_mm':57,'b_mm':68}))
L.append(E('Le ruban découpé', 'Un ruban mesure 1 m. On coupe 35 cm puis 28 cm.',[
 q('Quelle est la longueur initiale en centimètres ?','Utilise la relation mètre-centimètre.','Un mètre vaut cent centimètres.','100 cm.'),
 q('Quelle longueur a été coupée au total ?','Réunis les deux morceaux.',calc('35+28',63),'63 cm ont été coupés.'),
 q('Quelle longueur reste-t-il ?','Retire la longueur utilisée.',calc('100-63',37),'Il reste 37 cm.'),
 q('Le reste est-il plus long que le premier morceau de 35 cm ?','Compare les longueurs.',calc('37-35',2),'Oui, le reste est plus long de 2 cm.'),
 q('Vérifie en réunissant les trois morceaux.','Retrouve la longueur du départ.',calc('35+28+37',100),'On retrouve 100 cm, soit 1 m.')],{'famille':'ruban','total':100,'coupes':[35,28]}))
L.append(E('Choisir des unités plausibles', 'On veut décrire l’épaisseur d’une pièce, la longueur d’un cahier et la distance entre deux villes.',[
 q('Quelle unité convient à l’épaisseur d’une pièce ?','Pense à une très petite longueur.','Une pièce est épaisse de quelques millimètres.','Le millimètre.'),
 q('Quelle unité convient à la longueur d’un cahier ?','Choisis une unité pratique pour un objet tenu en main.','Un cahier mesure quelques dizaines de centimètres.','Le centimètre.'),
 q('Quelle unité convient au trajet entre deux villes ?','Choisis une unité pour une grande distance.','Une distance de plusieurs milliers de mètres se décrit en kilomètres.','Le kilomètre.'),
 q('Un cahier de 24 m est-il plausible ?','Compare avec la taille d’une salle.','24 m représentent une très grande longueur ; un cahier ordinaire tient sur une table.','Non ; 24 cm serait un ordre de grandeur plausible.'),
 q('Une règle mesure 30 cm. Combien cela fait-il de décimètres ?','Regroupe les centimètres par dix.',calc('30/10',3),'30 cm = 3 dm.')],{'famille':'unites'}))
L.append(E('Corriger une confusion d’unités', 'Lina affirme : « 5 cm et 4 mm font 9 mm ».',[
 q('Quelle erreur a-t-elle faite ?','Regarde les unités avant d’additionner.','Elle a ajouté 5 et 4 comme si centimètres et millimètres étaient la même unité.','Elle a mélangé deux unités différentes.'),
 q('Convertis 5 cm en millimètres.','Chaque centimètre contient dix millimètres.',calc('5*10',50),'5 cm = 50 mm.'),
 q('Quelle est la bonne longueur totale ?','Ajoute les quatre millimètres.',calc('50+4',54),'La bonne longueur est 54 mm.'),
 q('Quelle différence y a-t-il avec sa réponse de 9 mm ?','Soustrais les longueurs dans la même unité.',calc('54-9',45),'Sa réponse est trop petite de 45 mm.'),
 q('Quelle phrase peux-tu retenir pour éviter cette erreur ?','Explique la règle de conversion.','Avant d’additionner, choisir une même unité et convertir chaque longueur.','Je convertis dans une unité commune avant de calculer.')],{'famille':'erreur','cm':5,'mm':4}))
write(24,L)

P=[]
def polygon(title,sides,unit='cm',fig=None):
 total=sum(sides);intro='Un polygone a des côtés de '+', '.join(f'{x} {unit}' for x in sides)+'.'
 if fig:intro+='\n\n[IMAGE_1]'
 return E(title,intro,[q('Que mesure son périmètre ?','Suis le bord extérieur.','Le périmètre correspond à un tour complet du polygone.','La longueur de son contour.'),q('Combien de côtés faut-il parcourir ?','Compte chaque côté une fois.',f'La liste contient {len(sides)} côtés.',f'{len(sides)} côtés.'),q('Calcule le périmètre.','Additionne toutes les longueurs.',calc('+'.join(map(str,sides)),total),f'{total} {unit}.'),q('Peut-on oublier le dernier côté pour revenir au départ ?','Imagine un tour complet.','Sans le dernier côté, le parcours s’arrête avant son point de départ.','Non, il faut parcourir tous les côtés.'),q('Quelle longueur de ruban faut-il pour faire deux tours ?','Réunis deux tours identiques.',calc(f'{total}+{total}',2*total),f'{2*total} {unit}.')],{'famille':'polygone','cotes':sides,'unite':unit}, {'1':fig} if fig else {})
P.append(polygon('Le rectangle dessiné',[6,3,6,3],fig='rectangle_6_3.png'))
P.append(polygon('Le triangle de 4, 5 et 6 cm',[4,5,6]))
P.append(polygon('Le carré de côté 7 cm',[7,7,7,7]))
P.append(E('Le triangle coté','Le schéma donne les longueurs des côtés. Ne mesure pas l’écran.\n\n[IMAGE_1]',[
 q('Quelles sont les trois longueurs indiquées ?','Lis les cotes.','Les trois côtés sont repérés par leurs longueurs.','3 cm, 4 cm et 5 cm.'),q('Calcule la somme des deux plus petits côtés.','Réunis 3 cm et 4 cm.',calc('3+4',7),'7 cm.'),q('Calcule le périmètre.','Ajoute aussi le troisième côté.',calc('7+5',12),'12 cm.'),q('Un fil de 10 cm suffit-il pour faire le tour ?','Compare au périmètre.','$10<12$.','Non, il manque 2 cm.'),q('Quel doit être le fil pour faire deux tours ?','Double le périmètre.',calc('12+12',24),'Il faut 24 cm.')],{'famille':'triangle_cote'}, {'1':'triangle_3_4_5.png'}))
P.append(E('Un rectangle avec deux unités','Un rectangle a des côtés de 8 cm et de 25 mm.',[
 q('Pourquoi faut-il convertir ?','Regarde les unités.','Les deux mesures n’utilisent pas la même unité.','Pour additionner des longueurs dans une unité commune.'),q('Exprime 8 cm en millimètres.','Un centimètre vaut dix millimètres.',calc('8*10',80),'80 mm.'),q('Quelles sont les quatre longueurs en millimètres ?','Utilise les côtés opposés égaux.','Les deux grands côtés font 80 mm et les deux petits 25 mm.','80 mm, 25 mm, 80 mm et 25 mm.'),q('Calcule le périmètre en millimètres.','Additionne les quatre côtés.',calc('80+25+80+25',210),'210 mm.'),q('Exprime ce périmètre en centimètres.','Regroupe les millimètres par dix.',calc('210/10',21),'21 cm.')],{'famille':'rectangle_unites','cm':8,'mm':25}))
P.append(E('Même contour, autres côtés','Un rectangle mesure 6 cm sur 4 cm. Un carré a des côtés de 5 cm.',[
 q('Quelles sont les quatre longueurs du rectangle ?','Les côtés opposés sont égaux.','On alterne longueur et largeur.','6 cm, 4 cm, 6 cm et 4 cm.'),q('Calcule son périmètre.','Additionne les quatre longueurs.',calc('6+4+6+4',20),'20 cm.'),q('Calcule le périmètre du carré.','Additionne quatre fois 5 cm.',calc('5+5+5+5',20),'20 cm.'),q('Les périmètres sont-ils égaux ?','Compare les résultats.','Les deux calculs donnent 20 cm.','Oui, les deux périmètres valent 20 cm.'),q('Les deux figures sont-elles pourtant identiques ?','Compare leurs côtés.','Le carré a quatre côtés de 5 cm ; le rectangle a des côtés de 6 cm et de 4 cm.','Non : des figures différentes peuvent avoir le même périmètre.')],{'famille':'meme_contour'}))
P.append(E('La clôture du jardin','Un jardin rectangulaire mesure 12 m sur 8 m. On laisse une ouverture de 2 m sans clôture.',[
 q('Quelles longueurs faut-il parcourir pour un tour complet ?','Utilise les côtés opposés égaux.','Un tour suit les quatre côtés.','12 m, 8 m, 12 m et 8 m.'),q('Calcule le contour entier.','Additionne tous les côtés.',calc('12+8+12+8',40),'40 m.'),q('Faut-il ajouter ou retirer le passage de 2 m ?','Cherche la partie qui reste ouverte.','Cette partie ne reçoit pas de clôture.','Il faut retirer 2 m.'),q('Quelle longueur de clôture faut-il ?','Retire le passage du contour.',calc('40-2',38),'38 m de clôture.'),q('Vérifie en réunissant clôture et passage.','Retrouve le tour complet.',calc('38+2',40),'On retrouve les 40 m du contour.')],{'famille':'jardin','longueur':12,'largeur':8,'passage':2}))
P.append(E('Construire deux contours de 16 cm','Sur ta feuille, dessine un carré et un rectangle qui ont chacun un périmètre de 16 cm.',[
 q('Quel côté peut avoir le carré ?','Partage le tour en quatre côtés égaux.',calc('16/4',4),'Un côté de 4 cm.'),q('Vérifie le périmètre de ce carré.','Additionne les quatre côtés.',calc('4+4+4+4',16),'16 cm.'),q('Un rectangle de 5 cm sur 3 cm convient-il ?','Calcule son contour.',calc('5+3+5+3',16),'Oui, son contour mesure 16 cm.'),q('Comment contrôler les angles droits des deux tracés ?','Utilise l’instrument adapté.','Place l’angle droit de l’équerre sur chaque coin.','Avec une équerre.'),q('Que montre cet exemple sur le périmètre ?','Compare la forme et la mesure du contour.','Les figures ont des côtés différents mais le même tour.','Un même périmètre ne détermine pas une seule figure.')],{'famille':'construire_contour'}))
P.append(E('Les deux côtés oubliés','Noé écrit 6 + 3 = 9 cm pour le périmètre d’un rectangle de 6 cm sur 3 cm.',[
 q('Que représentent les 9 cm qu’il a calculés ?','Compte les côtés pris en compte.','Il a parcouru seulement un grand côté et un petit côté.','Deux côtés du rectangle.'),q('Quelles longueurs a-t-il oubliées ?','Retrouve les côtés opposés.','Les deux autres côtés mesurent aussi 6 cm et 3 cm.','6 cm et 3 cm.'),q('Quelle longueur manque à son calcul ?','Additionne les deux côtés oubliés.',calc('6+3',9),'Il manque 9 cm.'),q('Quel est le bon périmètre ?','Réunis les deux parties du tour.',calc('9+9',18),'18 cm.'),q('Comment éviter cet oubli sur un schéma ?','Marque un départ et suis tout le bord.','Parcourir chaque côté dans l’ordre, puis s’arrêter seulement au retour au point de départ.','Je fais un tour complet et je compte chaque côté une fois.')],{'famille':'erreur_contour'}))
write(25,P)
