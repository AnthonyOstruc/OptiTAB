from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent.parent
CH={}
def q(question,raison,reponse):return [question,raison,reponse]
def ex(titre,contexte,items,image=None):return dict(titre=titre,contexte=contexte,questions=items,image=image)
CH[32]=[
ex('Trois quadrilatères','Observe les figures. Contrôle les angles avec le coin d’une feuille et les côtés en reportant une même longueur sur une bande de papier.',[
q('Nomme la figure A.','Les quatre côtés ont la même longueur. Les quatre coins coïncident avec le coin droit du papier, même si la figure est tournée.','A est un carré.'),
q('Nomme la figure B.','Les quatre angles sont droits. Deux côtés voisins ont des longueurs différentes.','B est un rectangle qui n’est pas un carré.'),
q('Nomme la figure C.','Les quatre côtés ont la même longueur ; aucun angle ne coïncide avec le coin droit.','C est un losange qui n’est pas un carré.'),
q('Combien A a-t-il de sommets ?','Pars d’un coin et suis le contour. Compte chaque coin une seule fois.','A a 4 sommets.'),
q('Quelle propriété A et C partagent-ils ?','Reporte la longueur d’un côté sur les trois autres côtés de chaque figure.','A et C ont chacun 4 côtés de même longueur.')],'quadrilateres'),
ex('Compter autour des polygones','Observe les deux polygones P et H.',[
q('Combien P a-t-il de côtés ?','Suis le contour de P et compte chacun de ses segments une seule fois.','P a 5 côtés.'),
q('Combien P a-t-il de sommets ?','Chaque changement de direction forme un sommet. Compte les cinq coins.','P a 5 sommets.'),
q('Comment appelle-t-on P ?','Un polygone à cinq côtés porte le nom de pentagone.','P est un pentagone.'),
q('Combien H a-t-il de côtés et de sommets ?','Fais le tour de H. Tu rencontres six segments et six coins.','H a 6 côtés et 6 sommets.'),
q('Comment appelle-t-on H ?','Un polygone à six côtés porte le nom d’hexagone.','H est un hexagone.')],'polygones'),
ex('Comparer des angles','Compare chaque angle au coin droit d’une feuille. Les lettres désignent les trois angles, pas des points.',[
q('L’angle A est-il aigu, droit ou obtus ?','Le coin droit est plus ouvert que A. Les deux bords de A sont plus rapprochés.','A est un angle aigu.'),
q('Nomme l’angle B.','Les deux bords du coin droit se posent exactement sur les deux côtés de B.','B est un angle droit.'),
q('Nomme l’angle C.','C est plus ouvert que le coin droit.','C est un angle obtus.'),
q('Quel instrument permet de contrôler B sur une copie ?','Pose le sommet de l’angle droit de l’équerre sur le sommet de B ; aligne un bord et regarde l’autre.','On utilise une équerre.'),
q('Quel angle est le plus ouvert ?','Compare les ouvertures, sans comparer la longueur des traits. C est plus ouvert que B et A.','C est le plus ouvert.')],'angles'),
ex('Tracer un triangle rectangle','Sur une feuille, trace un triangle ABC rectangle en A. Les côtés AB et AC mesurent 4 cm et 3 cm.',[
q('Trace AB. Quelle longueur doit-il avoir ?','Place A devant le zéro de la règle. Place B devant 4 cm puis relie les deux points.','AB mesure 4 cm.'),
q('Comment placer AC ?','Place le coin droit de l’équerre en A, un bord sur AB. Trace AC le long de l’autre bord et place C à 3 cm de A.','AC mesure 3 cm et l’angle en A est droit.'),
q('Termine le triangle. Quel segment manque ?','A et B sont déjà reliés, A et C aussi. La règle permet de fermer le contour en reliant B à C.','Il faut tracer BC.'),
q('Où places-tu le petit carré ?','Contrôle le coin en A avec l’équerre, puis dessine le code à l’intérieur du triangle contre AB et AC.','Le petit carré se place en A.'),
q('Combien la figure a-t-elle de côtés et de sommets ?','Le contour est formé de AB, BC et CA. Les coins sont A, B et C.','Le triangle a 3 côtés et 3 sommets.')]),
ex('Le carré dans deux familles','On découpe un carré puis on le tourne. Utilise ses propriétés.',[
q('Combien le carré a-t-il d’angles droits ?','Le coin de l’équerre coïncide avec chacun des quatre coins.','Le carré a 4 angles droits.'),
q('Pourquoi est-il aussi un rectangle ?','Un rectangle est un quadrilatère à quatre angles droits ; le carré respecte cette règle.','Le carré est un rectangle car il a 4 angles droits.'),
q('Combien ses côtés de même longueur sont-ils ?','Reporte un côté sur chacun des autres : la longueur reste la même.','Ses 4 côtés ont la même longueur.'),
q('Pourquoi est-il aussi un losange ?','Un losange est un quadrilatère à quatre côtés de même longueur ; le carré respecte cette règle.','Le carré est un losange car ses 4 côtés ont la même longueur.'),
q('Le nom du carré change-t-il si on le tourne ?','Tourner le morceau de papier ne coupe aucun côté et ne déforme aucun angle.','Non, il reste un carré.')]),
ex('Relier des sommets opposés','Le rectangle ABCD a ses sommets nommés dans l’ordre du contour.',[
q('Quels sommets sont voisins de A ?','Le contour part de A vers B dans un sens et vers D dans l’autre sens.','B et D sont voisins de A.'),
q('Quel sommet est opposé à A ?','C n’est relié à A par aucun côté du rectangle.','C est opposé à A.'),
q('Trace une diagonale issue de A.','Une diagonale relie deux sommets opposés. Pose la règle sur A et C puis trace.','La diagonale issue de A est AC.'),
q('Trace l’autre diagonale.','Les deux sommets restants sont B et D. Ils sont eux aussi opposés.','L’autre diagonale est BD.'),
q('Combien de diagonales as-tu tracées ?','Les seules paires de sommets opposés sont A avec C, et B avec D.','Le rectangle possède 2 diagonales.')],'diagonales'),
ex('Les longueurs ne disent pas tout','Un quadrilatère a des côtés successifs de 4 cm, 6 cm, 4 cm et 6 cm.',[
q('Combien a-t-il de côtés ?','Le mot quadrilatère désigne un polygone à quatre côtés.','Il a 4 côtés.'),
q('Ses côtés opposés ont-ils la même longueur ?','Le premier et le troisième mesurent 4 cm ; le deuxième et le quatrième mesurent 6 cm.','Oui, les côtés opposés ont la même longueur.'),
q('Peut-on déjà affirmer que c’est un rectangle ?','Les longueurs n’indiquent pas si les coins sont droits. Un quadrilatère penché peut avoir ces mêmes longueurs.','Non, les longueurs seules ne suffisent pas.'),
q('Quel contrôle manque-t-il ?','Pose l’équerre dans chacun des quatre coins. Pour un rectangle, les deux bords doivent coïncider à chaque coin.','Il faut vérifier les 4 angles droits.'),
q('Peut-il être un carré ?','Un carré exige quatre côtés de même longueur. Ici 4 cm et 6 cm sont différents.','Non, ce quadrilatère n’est pas un carré.')]),
ex('Contour ou surface','Observe les deux dessins : à gauche un contour rond ; à droite une surface ronde colorée.',[
q('Comment appelle-t-on le contour seul ?','Le trait délimite la forme mais ne remplit pas son intérieur.','Le contour seul est un cercle.'),
q('Comment appelle-t-on le contour avec son intérieur ?','La forme comprend tous les points du milieu jusqu’au bord.','Le contour et son intérieur forment un disque.'),
q('Un point au milieu du disque appartient-il au cercle ?','Le cercle ne contient que les points du bord ; le milieu n’est pas sur le bord.','Non, ce point intérieur n’appartient pas au cercle.'),
q('Un point du bord appartient-il aussi au disque ?','Le disque comprend la surface intérieure et le contour.','Oui, un point du bord appartient au disque.'),
q('Le cercle est-il un polygone ?','Un polygone est formé de segments. Le cercle est courbe, sans côtés droits.','Non, le cercle n’est pas un polygone.')],'cercle_disque'),
ex('Le carré tourné de Noé','Noé tourne son carré sans le déformer et dit : « Il n’a plus d’angle droit ! »',[
q('Que deviennent les longueurs des côtés ?','Le papier n’a été ni coupé ni étiré ; chaque côté garde sa longueur.','Les 4 côtés gardent la même longueur.'),
q('Que deviennent les angles droits ?','Pose l’équerre en tournant aussi l’instrument. Le coin droit coïncide encore avec chaque coin.','Les 4 angles restent droits.'),
q('Quel est toujours le nom précis de la figure ?','Elle possède encore quatre côtés égaux et quatre angles droits.','La figure reste un carré.'),
q('Est-elle encore aussi un losange ?','Un losange a quatre côtés de même longueur. Cette propriété est conservée.','Oui, elle reste aussi un losange.'),
q('Corrige la phrase de Noé.','L’orientation change, mais les propriétés ne changent pas. On contrôle les coins plutôt que de se fier à leur direction.','Le carré tourné a toujours 4 angles droits.')])]

CH[33]=[
ex('Un segment et son milieu','Sur une feuille unie, utilise une règle graduée.',[
q('Trace AB de 8 cm.','Place A au zéro, marque B à la graduation 8 cm puis trace le segment.','AB mesure 8 cm.'),
q('À quelle distance de A places-tu le milieu M ?','Cherche deux longueurs égales dont la somme est 8 cm : 4 cm et 4 cm.','AM mesure 4 cm.'),
q('Quelle est la longueur MB ?','Le milieu partage le segment en deux parties égales. De la graduation 4 à la graduation 8, il y a 4 cm.','MB mesure 4 cm.'),
q('Comment coder les deux parties ?','Trace un même petit trait à travers AM et MB pour signaler qu’elles ont la même longueur.','AM et MB portent le même code.'),
q('Une droite a-t-elle les mêmes limites que AB ?','Le segment s’arrête en A et B ; une droite se prolonge des deux côtés.','Non, le segment a deux extrémités ; la droite se prolonge.')]),
ex('Un cercle au compas','Trace sur ta feuille un cercle de centre O et de rayon 3 cm.',[
q('Comment règles-tu le compas ?','Pose les deux pointes sur les graduations 0 et 3 de la règle. Garde cette ouverture.','L’ouverture du compas est 3 cm.'),
q('Où places-tu la pointe fixe ?','Le centre doit rester le même pendant tout le tour. Pique la pointe sèche exactement sur O.','La pointe fixe se place en O.'),
q('Trace le cercle puis marque A sur son bord. Combien mesure OA ?','Le crayon reste à 3 cm de O durant tout le tracé. Chaque point du bord est à cette distance.','OA mesure 3 cm.'),
q('Marque un autre point B sur le cercle. Combien mesure OB ?','A et B sont tous les deux sur le même cercle de centre O. L’ouverture n’a pas changé.','OB mesure 3 cm.'),
q('Peut-on déplacer la pointe fixe pendant le tracé ?','Si la pointe se déplace, les points ne restent plus à la même distance d’un seul centre.','Non, la pointe doit rester en O.')]),
ex('Passer par le centre','Trace un cercle de centre O et de rayon 3 cm. Place A sur le cercle.',[
q('Trace une droite qui passe par A et O. Que fait-elle après O ?','Pose la règle sur A et O. Prolonge le trait de l’autre côté de O jusqu’au cercle, au point B.','La droite rencontre encore le cercle en B.'),
q('Comment appelle-t-on AB ?','A et B sont sur le cercle et le segment passe par son centre O.','AB est un diamètre.'),
q('Combien mesure AO ?','AO relie le centre à un point du cercle : c’est un rayon.','AO mesure 3 cm.'),
q('Combien mesure OB ?','B est lui aussi sur le cercle de centre O et de rayon 3 cm.','OB mesure 3 cm.'),
q('Combien mesure le diamètre AB ?','Les deux rayons sont bout à bout : 3 cm + 3 cm = 6 cm.','AB mesure 6 cm.')]),
ex('Construire un rectangle','Construis ABCD, dans l’ordre du contour, de longueur 7 cm et de largeur 3 cm. Dessine sur une feuille, sans mesurer l’image.',[
q('Trace le premier côté AB.','Aligne le zéro de la règle avec A et place B à 7 cm.','AB mesure 7 cm.'),
q('Construis AD.','Place le coin droit de l’équerre en A et un bord sur AB. Trace sur l’autre bord et place D à 3 cm de A.','AD mesure 3 cm et l’angle en A est droit.'),
q('Construis BC du même côté de AB que D.','Place le coin droit en B et un bord sur AB. Sur l’autre bord, place C à 3 cm de B, vers le même côté que D.','BC mesure 3 cm et l’angle en B est droit.'),
q('Ferme le rectangle et contrôle CD.','Relie C à D avec la règle. Mesure le segment obtenu, puis vérifie les coins C et D avec l’équerre.','CD mesure 7 cm et les 4 angles sont droits.'),
q('Code les angles et les côtés égaux.','Place un petit carré dans chaque coin. Utilise un code pour AB et CD, un autre pour AD et BC.','AB et CD ont le même code ; AD et BC ont un autre code.')]),
ex('Construire un carré','Construis le carré ABCD de côté 5 cm sur une feuille.',[
q('Trace AB.','Place A au zéro et B à 5 cm. Relie-les sans dépasser.','AB mesure 5 cm.'),
q('Trace AD avec un angle droit en A.','Place l’équerre sur AB avec son coin en A. Trace le second bord et place D à 5 cm.','AD mesure 5 cm et l’angle en A est droit.'),
q('Place C.','En B, trace un angle droit avec AB, du même côté que D. Mesure 5 cm sur ce nouveau côté pour placer C.','BC mesure 5 cm et l’angle en B est droit.'),
q('Termine puis contrôle.','Trace CD. Vérifie sa longueur avec la règle puis les quatre coins avec l’équerre.','Les 4 côtés mesurent 5 cm ; les 4 angles sont droits.'),
q('Quels codes ajoutes-tu ?','Le même trait sur les quatre côtés indique la même longueur. Un petit carré indique chaque angle droit.','On ajoute le même code sur les 4 côtés et un code à chaque angle droit.')]),
ex('Un triangle avec un coin droit','Construis ABC rectangle en A, avec AB de 6 cm et AC de 4 cm.',[
q('Trace AB.','Pose le zéro de la règle en A puis place B à 6 cm.','AB mesure 6 cm.'),
q('Prépare le côté AC.','Pose un bord de l’équerre sur AB et son angle droit en A. Trace le long de l’autre bord.','Les directions AB et AC forment un angle droit en A.'),
q('Place C à la bonne distance.','Pose le zéro en A sur le nouveau trait. Place C à 4 cm, puis arrête le segment en C.','AC mesure 4 cm.'),
q('Ferme la figure.','Relie B et C à la règle. Tu obtiens un contour fermé à trois côtés.','On trace BC pour obtenir le triangle ABC.'),
q('Quel angle codes-tu ?','Contrôle le coin A à l’équerre ; il est formé par les deux côtés de 6 cm et 4 cm.','On code l’angle droit en A.')]),
ex('Assembler carré et cercle','Sur une grande feuille, construis un carré ABCD de côté 4 cm puis un cercle de centre A et de rayon 3 cm.',[
q('Quelle longueur donnes-tu aux côtés du carré ?','Trace AB, AD et BC de 4 cm en construisant des coins droits, puis ferme par CD et contrôle.','Chaque côté du carré mesure 4 cm.'),
q('Quels angles contrôles-tu ?','Le nom carré impose un coin droit à chacun des quatre sommets. Pose successivement l’équerre en A, B, C et D.','On contrôle les 4 angles droits.'),
q('Où piques-tu le compas ?','Le centre demandé est A, qui est aussi un sommet du carré.','La pointe fixe se place en A.'),
q('Quelle ouverture choisis-tu ?','Le rayon annoncé est 3 cm. Règle l’écartement sur la règle avant de tracer.','L’ouverture du compas est 3 cm.'),
q('B est-il sur le cercle ?','AB mesure 4 cm alors que tout point du cercle est à 3 cm de A. B est donc plus loin que le bord.','Non, B est à l’extérieur du cercle.')]),
ex('Reproduire sur quadrillage','Reproduis le modèle dans le quadrillage vide. Pars de son point A. Un carreau est l’intervalle entre deux lignes voisines.',[
q('Comment passer de A à B ?','Compte les intervalles horizontalement puis verticalement sur le modèle. Le déplacement ne suit pas un trait du quadrillage.','Depuis A : 3 carreaux à droite et 1 vers le haut.'),
q('Comment passer de B à C ?','Sur le modèle, C se trouve une colonne après B et deux lignes plus haut.','Depuis B : 1 carreau à droite et 2 vers le haut.'),
q('Comment passer de C à D ?','D est trois colonnes avant C et une ligne plus bas.','Depuis C : 3 carreaux à gauche et 1 vers le bas.'),
q('Comment fermer la figure ?','D se trouve une colonne à droite et deux lignes au-dessus de A. Reviens en A puis relie les points dans l’ordre.','Depuis D : 1 carreau à gauche et 2 vers le bas, jusqu’à A.'),
q('Comment vérifier ta copie ?','Compare chaque déplacement du modèle et de la copie. Avec une bande de papier, compare les côtés ; avec un calque, compare les coins.','La copie doit garder les mêmes déplacements, longueurs et angles.')],'quadrillage'),
ex('Le compas de Lina','Lina veut tracer un cercle de centre O et de rayon 2 cm, mais sa pointe fixe glisse.',[
q('Quel point devait rester fixe ?','Le centre du cercle est le point autour duquel tourne le crayon.','Le point O devait rester fixe.'),
q('Quelle ouverture devait-elle garder ?','La distance entre la pointe sèche et le crayon est le rayon demandé.','Elle devait garder une ouverture de 2 cm.'),
q('Pourquoi son premier tracé ne convient-il pas ?','En glissant, la pointe change de place ; le crayon ne reste pas à 2 cm du même point O.','Le tracé n’est pas un cercle de centre O et de rayon 2 cm.'),
q('Comment recommencer ?','Marque bien O, règle 2 cm, pique en O puis tourne doucement sans déplacer la pointe sèche.','Il faut garder le centre fixe et l’ouverture constante.'),
q('Comment contrôler le tracé obtenu ?','Choisis plusieurs points du contour et mesure depuis O. Tu dois retrouver la même longueur à chaque fois.','Chaque point choisi sur le cercle doit être à 2 cm de O.')])]

CH[34]=[
ex('Six solides à reconnaître','Les six dessins représentent des solides A à F. Tu peux aussi chercher des objets qui leur ressemblent.',[
q('Nomme A et B.','A a six faces carrées. B a la forme d’une boîte allongée à faces rectangulaires.','A est un cube ; B est un pavé.'),
q('Nomme C.','Sa surface est toute ronde ; elle n’a ni coin ni face plate, comme une balle pleine.','C est une boule.'),
q('Nomme D.','Ses deux bases sont des disques de même taille ; son bord latéral est arrondi, comme une boîte de conserve.','D est un cylindre.'),
q('Nomme E.','Il possède une base en disque et une pointe, comme un chapeau de fête.','E est un cône.'),
q('Nomme F et décris sa base.','Quatre faces triangulaires rejoignent une pointe au-dessus d’une base à quatre côtés égaux et quatre angles droits.','F est une pyramide à base carrée.')],'solides'),
ex('Explorer un cube','Prends un cube réel. Marque les éléments déjà comptés avec de petits papiers.',[
q('Combien le cube a-t-il de faces ?','Compte une face dessous, une dessus et les quatre faces autour. 1 + 1 + 4 = 6.','Le cube a 6 faces.'),
q('Quelle est la forme de ses faces ?','Pose une face sur le papier : son contour a quatre côtés égaux et quatre angles droits. Toutes les faces ont cette forme.','Toutes les faces du cube sont des carrés.'),
q('Combien a-t-il d’arêtes ?','Compte quatre arêtes en haut, quatre en bas et quatre qui les relient. 4 + 4 + 4 = 12.','Le cube a 12 arêtes.'),
q('Combien a-t-il de sommets ?','Compte les quatre coins du dessus puis les quatre du dessous. 4 + 4 = 8.','Le cube a 8 sommets.'),
q('Combien faut-il de tiges et de boules de pâte pour son squelette ?','Chaque tige représente une arête et chaque boule de pâte un sommet. Utilise les deux comptages précédents.','Il faut 12 tiges et 8 boules de pâte.')]),
ex('Comparer cube et pavé','Observe un cube et une boîte rectangulaire allongée, appelée pavé.',[
q('Combien le pavé a-t-il de faces ?','Compte le dessus, le dessous et les quatre faces autour, comme pour le cube.','Le pavé a 6 faces.'),
q('Quelle est la forme de ses faces ?','Le contour de chaque face a quatre angles droits ; des faces peuvent être carrées.','Les faces du pavé sont des rectangles.'),
q('Combien le pavé a-t-il d’arêtes ?','Compte quatre arêtes sur le dessus, quatre dessous et les quatre qui les relient.','Le pavé a 12 arêtes.'),
q('Combien le pavé a-t-il de sommets ?','Compte quatre coins au-dessus et quatre au-dessous.','Le pavé a 8 sommets.'),
q('Qu’est-ce qui est pareil dans les deux solides ?','Compare les comptages : les formes des faces peuvent différer, mais les trois nombres sont identiques.','Cube et pavé ont chacun 6 faces, 12 arêtes et 8 sommets.')]),
ex('Une pyramide triangulaire','Observe la pyramide à base triangulaire. Le sommet du haut est relié aux trois sommets de la base.',[
q('Quelle est la forme de la base ?','La base a trois côtés et trois sommets.','La base est un triangle.'),
q('Combien de faces se dressent au-dessus de la base ?','Chaque côté de la base forme le bas d’une face qui rejoint le sommet du haut. La base a trois côtés.','Il y a 3 faces au-dessus de la base.'),
q('Combien de faces triangulaires le solide a-t-il en tout ?','Ajoute la base triangulaire aux trois faces qui la rejoignent : 1 + 3 = 4.','La pyramide a 4 faces triangulaires.'),
q('Combien a-t-elle d’arêtes ?','Il y a trois arêtes autour de la base et trois qui montent au sommet : 3 + 3 = 6.','Elle a 6 arêtes.'),
q('Combien a-t-elle de sommets ?','Aux trois sommets de la base, ajoute le sommet du haut : 3 + 1 = 4.','Elle a 4 sommets.')],'pyramides'),
ex('Voir ce qui est caché','Observe le cube dessiné. Les sommets visibles et cachés sont tous indiqués par des petits points.',[
q('Que représentent les segments en pointillés ?','Dans cette vue, des faces cachent une partie des bords. On utilise des pointillés pour montrer ces bords sans les confondre avec les bords visibles.','Les pointillés représentent des arêtes cachées.'),
q('Les arêtes cachées existent-elles sur le cube réel ?','Tourne le cube : un bord caché devient visible. Le dessin ne supprime aucun bord.','Oui, les arêtes cachées existent.'),
q('Combien d’arêtes sont ici en pointillés ?','Repère les trois segments qui partent du sommet caché, à l’arrière et en bas.','Il y a 3 arêtes cachées en pointillés.'),
q('Combien d’arêtes sont ici en trait plein ?','Le cube a douze arêtes. Trois sont cachées dans cette vue : 12 − 3 = 9.','Il y a 9 arêtes en trait plein.'),
q('Combien le cube a-t-il de sommets en tout ?','Compte les points des deux carrés décalés : quatre devant et quatre derrière.','Le cube a 8 sommets.')],'cube_cache'),
ex('Deux assemblages à plier','Sur du papier quadrillé, recopie les deux assemblages, avec des carrés de 3 cm de côté. Découpe le contour extérieur avec un adulte. Les segments entre carrés sont des plis.',[
q('Combien de carrés A contient-il ?','Compte la colonne de quatre carrés, puis le carré à gauche et celui à droite : 4 + 1 + 1 = 6.','A contient 6 carrés.'),
q('Combien de carrés B contient-il ?','Compte un à un les carrés de la bande.','B contient 6 carrés.'),
q('Prévois quel assemblage peut former un cube.','Dans A, les carrés peuvent couvrir le dessous, les quatre côtés et le dessus. Dans B, tous les carrés se suivent dans une seule bande.','On prévoit que A forme un cube.'),
q('Plie A pour vérifier. Que constates-tu ?','Choisis le carré central comme dessous ; relève les quatre côtés puis ferme avec le carré restant. Les faces ne se superposent pas.','A se ferme en un cube à 6 faces.'),
q('Plie B. Peut-il fermer un cube ?','En pliant la bande autour du cube, elle revient sur des faces déjà couvertes ; elle ne couvre pas le dessus et le dessous.','Non, B ne ferme pas un cube.')],'patrons'),
ex('Le squelette d’une pyramide','Construis une pyramide à base carrée avec des tiges et des boules de pâte. Observe aussi le modèle de pyramide carrée.',[
q('Combien de tiges faut-il pour la base ?','Un carré a quatre côtés ; chaque côté reçoit une tige.','Il faut 4 tiges pour la base.'),
q('Combien de tiges montent au sommet ?','Chacun des quatre sommets de la base est relié au sommet du haut.','Il faut 4 tiges qui montent au sommet.'),
q('Combien de tiges faut-il en tout ?','Ajoute les quatre tiges de base et les quatre autres : 4 + 4 = 8.','Il faut 8 tiges en tout.'),
q('Combien de boules de pâte faut-il ?','Place quatre boules aux coins de la base et une au sommet du haut : 4 + 1 = 5.','Il faut 5 boules de pâte.'),
q('Combien de faces le squelette délimite-t-il ?','Il délimite la base carrée et quatre triangles qui se rejoignent en haut : 1 + 4 = 5.','Il délimite 5 faces : 1 carré et 4 triangles.')],'pyramides'),
ex('Il manque un carré','Mila a un assemblage de cinq carrés de même taille pour fabriquer un cube.',[
q('Combien de faces doit avoir un cube ?','Un cube a un dessus, un dessous et quatre faces autour.','Un cube doit avoir 6 faces.'),
q('Combien de faces ses cinq carrés peuvent-ils fournir ?','Chaque carré peut devenir une face. Cinq carrés donnent au maximum cinq faces.','Ils peuvent fournir 5 faces.'),
q('Combien de carrés manque-t-il au minimum ?','Compare les six faces nécessaires et les cinq carrés disponibles : 6 − 5 = 1.','Il manque au moins 1 carré.'),
q('L’assemblage est-il déjà un patron complet ?','Une face manquerait pour fermer le solide.','Non, cinq carrés ne forment pas un patron complet de cube.'),
q('Ajouter un carré n’importe où suffit-il ?','Même avec six carrés, leur place compte. Il faut prévoir le pliage puis vérifier sans faces superposées.','Non, il faut placer le sixième carré puis vérifier par pliage.')]),
ex('Vérifier l’idée de Noé','Noé dit : « Avec six carrés, je fabrique toujours un cube. » Utilise à nouveau les deux assemblages manipulables.',[
q('Quelle condition sur le nombre de faces est correcte ?','Chaque face carrée du cube doit être couverte par un carré de l’assemblage.','Il faut 6 carrés pour les 6 faces.'),
q('Les carrés doivent-ils avoir la même taille ?','Les faces du cube sont des carrés de même taille ; des tailles différentes empêcheraient leurs bords de se joindre.','Oui, les 6 carrés doivent avoir la même taille.'),
q('Quel assemblage contredit la phrase de Noé ?','La bande contient bien six carrés égaux, mais elle ne ferme pas un cube.','La bande B contredit la phrase de Noé.'),
q('Quelle autre condition manque dans sa phrase ?','Les carrés doivent se rejoindre après pliage pour couvrir chaque face une fois.','La disposition doit permettre de fermer le cube sans superposition.'),
q('Comment vérifier sa prévision ?','Recopie, découpe le contour, marque les plis puis plie réellement l’assemblage.','On vérifie par un pliage effectif.')],'patrons')]

CH[35]=[
ex('Plier un rectangle','Dessine et découpe un rectangle de 6 cm sur 4 cm. Il n’est pas carré.',[
q('Teste un pli vertical passant au milieu. Les parties se superposent-elles ?','Ramène le côté gauche sur le côté droit, en faisant coïncider les coins. Le pli passe au milieu du haut et du bas.','Oui, le pli vertical du milieu est un axe de symétrie.'),
q('Teste un pli horizontal passant au milieu.','Ramène le bas sur le haut. Les bords et les coins coïncident.','Le pli horizontal du milieu est aussi un axe de symétrie.'),
q('Teste une diagonale comme pli.','Ramène un côté de 6 cm contre un côté de 4 cm. Leurs extrémités ne coïncident pas.','Une diagonale n’est pas un axe de ce rectangle.'),
q('Combien d’axes as-tu trouvés ?','Les deux plis du milieu fonctionnent ; les diagonales ne fonctionnent pas.','Le rectangle non carré possède 2 axes de symétrie.'),
q('Que faut-il regarder pour reconnaître un axe ?','Après pliage, tous les bords doivent se poser les uns sur les autres, pas seulement deux coins.','Les deux parties doivent se superposer entièrement.')]),
ex('Les plis du carré','Dessine et découpe un carré de 4 cm de côté.',[
q('Teste le pli vertical du milieu.','Plie le bord gauche sur le bord droit. Les quatre coins se superposent deux à deux.','Le pli vertical du milieu est un axe.'),
q('Teste le pli horizontal du milieu.','Plie le bas sur le haut. Les bords coïncident sur toute leur longueur.','Le pli horizontal du milieu est un axe.'),
q('Teste une première diagonale.','Plie selon un trait qui relie deux coins opposés. Les deux triangles obtenus se superposent.','La première diagonale est un axe.'),
q('Teste l’autre diagonale.','Recommence avec les deux autres coins opposés. Les deux morceaux se superposent encore.','La deuxième diagonale est un axe.'),
q('Combien d’axes le carré possède-t-il ?','Compte les deux plis du milieu et les deux diagonales : 2 + 2 = 4.','Le carré possède 4 axes de symétrie.')]),
ex('Compléter autour d’un axe vertical','Recopie le quadrillage et sa ligne brisée ABCD. Le trait orange est l’axe. Place les points de l’autre côté puis relie-les dans le même ordre.',[
q('Où placer le point qui correspond à A ?','A est sur l’axe. Au pliage, le pli reste à sa place.','Le point correspondant à A reste en A.'),
q('Où placer le point qui correspond à B ?','B est trois carreaux à gauche de l’axe. Compte trois carreaux à droite, sur la même ligne.','B se reporte à 3 carreaux à droite, sur la même ligne.'),
q('Où placer le point qui correspond à C ?','C est à un carreau à gauche de l’axe. Garde sa ligne et compte un carreau à droite.','C se reporte à 1 carreau à droite, sur la même ligne.'),
q('Où placer le point qui correspond à D ?','D est sur l’axe comme A. Il ne change pas de place au pliage.','Le point correspondant à D reste en D.'),
q('Comment terminer et contrôler ?','Relie A, le point de B, le point de C et D dans cet ordre. Plie sur l’axe ou utilise du calque pour comparer les deux tracés.','Les deux lignes brisées doivent se superposer par pliage.')],'sym_v'),
ex('De part et d’autre d’un pli horizontal','Dessine un axe horizontal sur un quadrillage. Place A à 2 carreaux au-dessus, B à 1 carreau au-dessus et C à 3 carreaux au-dessous.',[
q('Où se place le point correspondant à A ?','Garde la même colonne ; reporte deux intervalles de l’autre côté du trait horizontal.','À 2 carreaux au-dessous de l’axe, dans la même colonne que A.'),
q('Où se place le point correspondant à B ?','Garde la colonne de B et reporte un intervalle sous le trait.','À 1 carreau au-dessous de l’axe, dans la même colonne que B.'),
q('Où se place le point correspondant à C ?','C est sous l’axe ; son point correspondant est donc au-dessus, à la même distance.','À 3 carreaux au-dessus de l’axe, dans la même colonne que C.'),
q('Où se place le point correspondant à un point sur l’axe ?','Le point est dans le pli : il ne bouge pas quand on replie.','Il reste au même endroit sur l’axe.'),
q('Faut-il compter les lignes ou les intervalles ?','Un carreau est l’espace entre deux lignes voisines ; compter la ligne de départ ajouterait un carreau à tort.','Il faut compter les intervalles entre les lignes.')]),
ex('Un point dans le pli','Trace un axe vertical. Place A et B sur cet axe à 3 carreaux l’un de l’autre, puis C à 2 carreaux à gauche de A, sur sa ligne.',[
q('Où va A quand on plie sur l’axe ?','A est exactement dans le pli. Aucun déplacement n’est nécessaire.','A reste en A.'),
q('Où va B quand on plie ?','B appartient lui aussi au pli ; il garde la même place.','B reste en B.'),
q('Où va le segment AB ?','Ses deux extrémités et tous ses points sont sur l’axe.','Le segment AB reste au même endroit.'),
q('Où se place le point correspondant à C ?','C est deux carreaux à gauche ; garde la ligne de A et compte deux carreaux à droite.','À 2 carreaux à droite de l’axe, sur la ligne de A.'),
q('Pourquoi ne faut-il pas déplacer A d’un carreau ?','Un point dans le pli se superpose à lui-même. Le déplacer le ferait sortir du pli.','A est sur l’axe : son point correspondant est A lui-même.')]),
ex('Compléter autour d’un axe horizontal','Recopie la ligne brisée ABCD et le quadrillage. Le trait orange est l’axe horizontal.',[
q('Où se reporte A ?','A est dans le pli horizontal ; il reste à sa place.','A reste sur l’axe en A.'),
q('Où se reporte B ?','B est trois carreaux au-dessus de l’axe. Garde la même colonne et descends de trois carreaux sous l’axe.','B se reporte à 3 carreaux au-dessous, dans la même colonne.'),
q('Où se reporte C ?','C est un carreau au-dessus de l’axe. Garde la colonne et compte un carreau sous l’axe.','C se reporte à 1 carreau au-dessous, dans la même colonne.'),
q('Où se reporte D ?','D est sur le trait orange : il ne bouge pas au pliage.','D reste sur l’axe en D.'),
q('Comment terminer ?','Relie les points reportés dans l’ordre A, B, C, D, puis contrôle par pliage ou calque.','Les deux tracés doivent se superposer en pliant sur l’axe.')],'sym_h'),
ex('Deux côtés égaux suffisent-ils ?','Observe le quadrilatère. Il possède deux côtés de même longueur mais sa forme est décalée. Recopie-le et utilise du calque.',[
q('Deux côtés de même longueur prouvent-ils la symétrie ?','Ils renseignent sur deux longueurs seulement. Ils ne garantissent pas que tous les autres points se correspondent par pliage.','Non, deux côtés égaux ne suffisent pas.'),
q('Que faut-il chercher ?','Essaie plusieurs plis sur la copie. Un bon pli doit faire coïncider toute une moitié avec l’autre.','Il faut chercher un axe qui fait superposer les deux parties.'),
q('Le pli vertical du milieu convient-il ici ?','Le bord du haut est décalé vers la droite : ses coins ne rejoignent pas ceux du bas après ce pli. Vérifie au calque.','Non, le pli vertical ne convient pas.'),
q('Le pli horizontal du milieu convient-il ?','Le haut reste décalé par rapport au bas ; les coins ne se posent pas l’un sur l’autre.','Non, le pli horizontal ne convient pas.'),
q('Quel contrôle donne une preuve concrète ?','Retourne le calque autour du pli essayé et compare l’ensemble des contours. Une seule portion mal superposée suffit à refuser cet axe.','Il faut contrôler la superposition de toute la figure.')],'sans_axe'),
ex('Une forme avec un seul axe','Sur un quadrillage, place A puis B 6 carreaux à droite sur la même ligne. Place C 3 carreaux à droite et 4 au-dessus de A. Relie A, B et C.',[
q('Quelle figure obtiens-tu ?','Les trois segments AB, BC et CA ferment un contour à trois côtés.','On obtient un triangle.'),
q('Où passe le pli vertical à essayer ?','Le milieu de AB est à trois carreaux de A et B. C est sur cette même colonne.','Le pli vertical passe par C et le milieu de AB.'),
q('Que deviennent A et B avec ce pli ?','A est trois carreaux à gauche du pli et B trois carreaux à droite, sur la même ligne.','A et B se superposent.'),
q('Ce pli est-il un axe ?','C reste dans le pli ; A rejoint B et les deux côtés obliques se superposent. Vérifie avec du calque.','Oui, le pli vertical est un axe de symétrie.'),
q('Un pli horizontal est-il aussi un axe ?','La pointe du haut ne peut pas rejoindre une pointe identique en bas : il n’y en a pas.','Non, ce triangle n’a pas d’axe horizontal.')]),
ex('Corriger le point de Lina','Un axe est vertical. P est 3 carreaux à gauche de l’axe. Lina place Q sur la même ligne, mais seulement 2 carreaux à droite.',[
q('Lina a-t-elle choisi le bon côté ?','Pour un point qui n’est pas sur l’axe, le point correspondant se place de l’autre côté.','Oui, il faut aller à droite de l’axe.'),
q('A-t-elle choisi la bonne ligne ?','Avec un axe vertical, on conserve la même ligne horizontale.','Oui, il faut garder la même ligne que P.'),
q('Sa distance à l’axe est-elle correcte ?','P est à trois carreaux de l’axe, Q seulement à deux. Les distances sont différentes.','Non, Q est trop près de l’axe.'),
q('De combien de carreaux faut-il déplacer Q ?','Pour passer de deux carreaux à trois, on ajoute un carreau en s’éloignant de l’axe.','Il faut déplacer Q de 1 carreau vers la droite.'),
q('Comment vérifier la correction ?','Après le déplacement, plie sur l’axe ou retourne le calque : P doit tomber exactement sur Q.','P et Q doivent se superposer au pliage.')])]

REPONSES='0 ; 1 ; 2 ; 1 ; 0 ; 3 ; 2 ; 1 ; 1 ; 0 ; 2 ; 1'
TABLE='| Activité | Lundi | Mardi |\n|---|---|---|\n| Dessin | 12 | 18 |\n| Musique | 8 | 7 |'
CH[36]=[
ex('Compter les réponses',f'On demande le nombre de frères et sœurs à 12 élèves. Voici les réponses : {REPONSES}.',[
q('Combien d’élèves ont répondu 0 ?','Barre chaque 0 une seule fois : ils apparaissent aux places 1, 5 et 10.','3 élèves ont répondu 0.'),
q('Combien ont répondu 1 ?','Repère les 1 aux places 2, 4, 8, 9 et 12. Compte cinq réponses.','5 élèves ont répondu 1.'),
q('Combien ont répondu 2 ?','Les 2 apparaissent aux places 3, 7 et 11.','3 élèves ont répondu 2.'),
q('Combien ont répondu 3 ?','Seule la réponse à la place 6 vaut 3. Ne confonds pas la réponse 3 avec le nombre d’élèves.','1 élève a répondu 3.'),
q('Contrôle le nombre total de réponses.','Additionne les quatre groupes : 3 + 5 + 3 + 1 = 12. On retrouve le nombre d’élèves interrogés.','Le total est 12 réponses.')]),
ex('Organiser dans un tableau',f'Voici à nouveau toutes les réponses : {REPONSES}. Présente un tableau à deux colonnes : « Frères et sœurs » et « Nombre d’élèves ».',[
q('Quelles valeurs écris-tu dans la première colonne ?','Cherche les réponses différentes et classe-les du plus petit au plus grand, sans les répéter.','On écrit 0, 1, 2 et 3.'),
q('Complète la ligne 0.','Compte les trois réponses égales à 0 ; ce sont trois élèves différents.','Pour 0 frère ou sœur : 3 élèves.'),
q('Complète la ligne 1.','Compte les cinq réponses égales à 1.','Pour 1 frère ou sœur : 5 élèves.'),
q('Complète les lignes 2 et 3.','Il y a trois réponses 2 et une réponse 3. Écris le comptage en face de chaque valeur.','Pour 2 : 3 élèves ; pour 3 : 1 élève.'),
q('Quel total écris-tu sous le tableau ?','Additionne uniquement les nombres d’élèves : 3 + 5 + 3 + 1 = 12. Les valeurs 0, 1, 2, 3 ne sont pas des effectifs.','Le total du tableau est 12 élèves.')]),
ex('Tracer quatre barres','On a compté : 0 frère ou sœur pour 3 élèves ; 1 pour 5 élèves ; 2 pour 3 élèves ; 3 pour 1 élève. Trace le graphique sur une feuille quadrillée.',[
q('Quel titre peux-tu écrire ?','Le titre indique le sujet de l’enquête et les personnes concernées.','Titre possible : « Les frères et sœurs de 12 élèves ».'),
q('Qu’écris-tu sous les quatre barres ?','Les catégories sont les nombres de frères et sœurs, pas les effectifs. Place-les dans l’ordre.','On écrit 0, 1, 2 et 3 sous les barres.'),
q('Quelle échelle simple choisis-tu ?','Le plus grand effectif est 5. Une graduation pour un élève permet de tout représenter en cinq intervalles.','On peut choisir 1 élève par graduation.'),
q('Quelles hauteurs donnes-tu aux quatre barres ?','Pars de zéro pour chaque barre. Monte respectivement de trois, cinq, trois et un intervalles.','Les hauteurs sont 3, 5, 3 et 1 élèves.'),
q('Que nommes-tu sur les deux axes ?','L’axe du bas donne la réponse à l’enquête ; l’axe vertical compte les élèves.','Axe du bas : « Frères et sœurs » ; axe vertical : « Élèves ».')]),
ex('Lire une échelle de cinq','Le graphique présente les déplacements de 50 élèves. Une graduation verticale vaut 5 élèves.',[
q('Combien viennent à vélo ?','La barre Vélo atteint la graduation 15, soit trois intervalles de cinq : 5 + 5 + 5 = 15.','15 élèves viennent à vélo.'),
q('Combien viennent à pied ?','La barre À pied atteint la cinquième graduation après zéro : 5 × 5 = 25.','25 élèves viennent à pied.'),
q('Combien viennent en bus ?','La barre Bus atteint la deuxième graduation après zéro : 2 × 5 = 10.','10 élèves viennent en bus.'),
q('Combien viennent à pied ou en bus en tout ?','Ces deux groupes sont distincts. Additionne leurs effectifs : 25 + 10 = 35.','35 élèves viennent à pied ou en bus.'),
q('Combien d’élèves le graphique compte-t-il ?','Additionne les trois groupes : 25 + 15 + 10 = 50.','Le graphique compte 50 élèves.')],'trajets'),
ex('Croiser ligne et colonne','Chaque élève s’inscrit à une seule activité par jour. Lis le tableau.\n\n'+TABLE,[
q('Combien sont inscrits en dessin le mardi ?','Pars de la ligne Dessin puis rejoins la colonne Mardi. Leur case commune contient 18.','18 élèves sont inscrits en dessin le mardi.'),
q('Combien sont inscrits en musique le lundi ?','Croise la ligne Musique avec la colonne Lundi ; lis 8.','8 élèves sont inscrits en musique le lundi.'),
q('Combien sont inscrits en dessin le lundi ?','La ligne Dessin et la colonne Lundi se croisent dans la case 12.','12 élèves sont inscrits en dessin le lundi.'),
q('Combien sont inscrits le lundi en tout ?','Dans la colonne Lundi, additionne les deux activités : 12 + 8 = 20.','20 élèves sont inscrits le lundi.'),
q('Combien sont inscrits le mardi en tout ?','Dans la colonne Mardi, additionne 18 en dessin et 7 en musique : 18 + 7 = 25.','25 élèves sont inscrits le mardi.')]),
ex('Comparer deux journées','Chaque élève choisit une activité par jour. Utilise ce tableau autonome.\n\n'+TABLE,[
q('Calcule le total du lundi.','Additionne les inscriptions des deux activités dans la colonne Lundi : 12 + 8 = 20.','Le lundi compte 20 inscriptions.'),
q('Calcule le total du mardi.','Additionne les deux cases de Mardi : 18 + 7 = 25.','Le mardi compte 25 inscriptions.'),
q('Quel jour compte le plus d’inscriptions ?','Compare les totaux : 25 est plus grand que 20.','Le mardi compte le plus d’inscriptions.'),
q('Quel est l’écart entre les deux totaux ?','Soustrais le petit total du grand : 25 − 20 = 5.','L’écart est de 5 inscriptions.'),
q('Combien d’inscriptions au dessin y a-t-il en plus mardi que lundi ?','Compare la même ligne : 18 − 12 = 6. Ne soustrais pas les totaux des journées.','Il y a 6 inscriptions au dessin en plus le mardi.')]),
ex('Le groupe des voitures','Une école compte 100 élèves. Chaque élève a un seul mode de déplacement : 25 viennent à pied, 15 à vélo, 10 en bus et tous les autres en voiture.',[
q('Combien viennent à pied ou à vélo ?','Réunis les deux groupes distincts : 25 + 15 = 40.','40 élèves viennent à pied ou à vélo.'),
q('Combien viennent à pied, à vélo ou en bus ?','Ajoute les dix élèves du bus aux quarante déjà comptés : 40 + 10 = 50.','50 élèves viennent à pied, à vélo ou en bus.'),
q('Combien viennent en voiture ?','Les cent élèves sont répartis entre tous les groupes. Retire ceux des trois groupes connus : 100 − 50 = 50.','50 élèves viennent en voiture.'),
q('Vérifie le total avec les voitures.','Additionne les quatre groupes : 25 + 15 + 10 + 50 = 100.','Le total est bien 100 élèves.'),
q('Quel groupe est le plus nombreux ?','Compare 25, 15, 10 et 50. Le plus grand nombre est 50.','Le groupe des voitures est le plus nombreux.')]),
ex('Choisir une échelle régulière','Trois groupes A, B et C comptent 20, 40 et 60 personnes. Ton graphique dispose de six grands intervalles verticaux à partir de zéro.',[
q('Une personne par grand intervalle suffit-elle ?','Six intervalles permettraient de représenter seulement six personnes, moins que vingt.','Non, 1 personne par intervalle ne suffit pas.'),
q('Quelle échelle simple permet de placer 60 en haut ?','Partage soixante en six groupes égaux : six groupes de dix font soixante.','On choisit 10 personnes par grand intervalle.'),
q('À quelle graduation places-tu la barre de A ?','Deux groupes de dix font vingt : 2 × 10 = 20.','A atteint la deuxième graduation après zéro.'),
q('À quelle graduation places-tu la barre de B ?','Quatre groupes de dix font quarante : 4 × 10 = 40.','B atteint la quatrième graduation après zéro.'),
q('À quelle graduation places-tu la barre de C ?','Six groupes de dix font soixante : 6 × 10 = 60. Garde le même écart entre toutes les graduations.','C atteint la sixième graduation après zéro.')]),
ex('Mener sa propre enquête','Interroge un petit groupe sur son fruit préféré parmi pomme, poire et banane. Chaque personne donne une seule réponse. Les nombres de ta réponse dépendent de ton enquête.',[
q('Comment formuler la question ?','Propose les trois mêmes choix à chaque personne et demande une seule préférence.','Question possible : « Préfères-tu la pomme, la poire ou la banane ? »'),
q('Comment recueillir les réponses sans doublon ?','Prépare une ligne par personne et coche un fruit sur sa ligne dès qu’elle répond.','On note une seule réponse par personne.'),
q('Comment présenter le tableau ?','Crée une ligne par fruit et compte ses coches. Écris chaque nombre en face du bon fruit.','Le tableau donne les trois fruits et leur nombre de réponses.'),
q('Comment vérifier les comptages ?','Additionne les trois nombres du tableau et compare avec le nombre de personnes interrogées. Recompte si les deux nombres diffèrent.','Le total doit être égal au nombre de personnes interrogées.'),
q('Construis le graphique puis écris une question.','Trace une barre par fruit avec une même échelle ; ajoute un titre et les noms des axes. Demande ensuite quel fruit a le plus de réponses et lis la barre la plus haute ; en cas d’égalité, cite les fruits à égalité.','Le graphique garde les nombres du tableau ; la réponse dépend de l’enquête.')])]

def picture(s):return '\\begin{tikzpicture}[x=1cm,y=1cm]\n'+s+'\n\\end{tikzpicture}'
def path(points,style='geoTrait',close=True):return '\\draw['+style+'] '+' -- '.join(f'({x},{y})' for x,y in points)+(' -- cycle;' if close else ';')
def label(x,y,s,anchor='center'):return f'\\node[anchor={anchor},text=otInk] at ({x},{y}) {{{s}}};'
def points(poly,names):
 s=''
 cx=sum(x for x,y in poly)/len(poly);cy=sum(y for x,y in poly)/len(poly)
 for (x,y),name in zip(poly,names):
  s+=f'\\fill[otNavy] ({x},{y}) circle (1.7pt);'
  dx=x-cx;dy=y-cy
  anchor=('east' if dx<0 else 'west') if abs(dx)>abs(dy) else ('north' if dy<0 else 'south')
  ox=x+(-.12 if anchor=='east' else .12 if anchor=='west' else 0);oy=y+(-.12 if anchor=='north' else .12 if anchor=='south' else 0)
  s+=label(ox,oy,'$'+name+'$',anchor)
 return s
FIG={n:{} for n in CH};GEO={n:{} for n in CH}
def add(n,name,s,data=None):
 FIG[n][name]=picture(s)
 if data is not None:GEO[n][name]=data
polys=[[(.3,1.3),(1.3,2.3),(2.3,1.3),(1.3,.3)],[(3,.6),(5,.6),(5,2),(3,2)],[(5.4,1.3),(6.6,2),(7.8,1.3),(6.6,.6)]]
add(32,'quadrilateres','\n'.join(path(p)+label(x,-.1,t) for p,x,t in zip(polys,[1.3,4,6.6],['A','B','C'])),polys)
pent=[(.4,.3),(1.8,.3),(2.2,1.6),(1.1,2.4),(0,1.6)];hexa=[(3.3,.4),(4.6,.4),(5.3,1.5),(4.6,2.6),(3.3,2.6),(2.6,1.5)]
add(32,'polygones',path(pent)+path(hexa)+label(1.1,-.1,'P')+label(3.95,-.1,'H'),[pent,hexa])
import math
ang=''
for x,a,t in [(0,45,'A'),(2.8,90,'B'),(5.6,120,'C')]:
 p=[(x+1.4,0),(x,0),(x+1.4*math.cos(math.radians(a)),1.4*math.sin(math.radians(a)))]
 ang+=path(p,close=False)+label(x+.35,-.45,t)
add(32,'angles',ang,[45,90,120])
rect=[(0,0),(5,0),(5,2.6),(0,2.6)]
add(32,'diagonales',path(rect)+points(rect,'ABCD'),rect)
add(32,'cercle_disque',r'\draw[geoTrait] (1.3,1.4) circle (1.1);\draw[geoTrait,fill=otSky] (4.5,1.4) circle (1.1);'+label(1.3,-.15,'Contour seul')+label(4.5,-.15,'Surface colorée'))
tri32=[(0,0),(4,0),(0,3)]
add(32,'triangle_corrige',path(tri32,'geoReponse')+points(tri32,'ABC')+path([(.2,0),(.2,.2),(0,.2)],'geoReponse',False)+label(2,-.6,'4 cm')+label(-.65,1.5,'3 cm'),tri32)
add(32,'diagonales_corrige',path(rect)+points(rect,'ABCD')+path([rect[0],rect[2]],'geoReponse',False)+path([rect[1],rect[3]],'geoReponse',False),rect)

def construction(name,poly,names,cm,angles):
 s=path(poly,'geoReponse')+points(poly,names)
 for i in angles:
  a=poly[i-1];b=poly[i];c=poly[(i+1)%len(poly)]
  u=(a[0]-b[0],a[1]-b[1]);v=(c[0]-b[0],c[1]-b[1]);lu=math.hypot(*u);lv=math.hypot(*v)
  p=(b[0]+u[0]/lu*.18,b[1]+u[1]/lu*.18);r=(b[0]+v[0]/lv*.18,b[1]+v[1]/lv*.18);mid=(p[0]+r[0]-b[0],p[1]+r[1]-b[1])
  s+=path([p,mid,r],'geoReponse',False)
 for x,y,text in cm:s+=label(x,y,text)
 add(33,name,s,poly)
construction('rectangle',[(0,0),(5.6,0),(5.6,2.4),(0,2.4)],'ABCD',[(2.8,-.65,'7 cm'),(-.65,1.2,'3 cm')],[0,1,2,3])
construction('carre',[(0,0),(3.5,0),(3.5,3.5),(0,3.5)],'ABCD',[(1.75,-.65,'5 cm')],[0,1,2,3])
construction('triangle',[(0,0),(4.2,0),(0,2.8)],'ABC',[(2.1,-.65,'6 cm'),(-.65,1.4,'4 cm')],[0])
add(33,'milieu',r'\draw[geoReponse] (0,0)--(5.6,0);\draw[geoTrait] (1.35,-.08)--(1.45,.08);\draw[geoTrait] (4.15,-.08)--(4.25,.08);'+points([(0,0),(2.8,0),(5.6,0)],'AMB')+label(1.4,.55,'4 cm')+label(4.2,.55,'4 cm'),[[0,0],[4,0],[8,0]])
circle=r'\draw[geoReponse] (0,0) circle (2.1);\fill[otNavy] (0,0) circle (1.7pt);\draw[geoTrait] (0,0)--(2.1,0);'+label(-.13,-.15,'$O$','north east')+label(2.25,0,'$A$','west')+label(1,.35,'3 cm')
add(33,'cercle',circle+r'\fill[otNavy] (0,2.1) circle (1.7pt);'+label(0,2.3,'$B$','south'),{'centre':[0,0],'rayon':3,'A':[3,0],'B':[0,3]})
add(33,'diametre',r'\draw[geoReponse] (0,0) circle (2.1);\draw[geoTrait] (-2.1,0)--(2.1,0);\fill[otNavy] (0,0) circle (1.7pt);'+label(-2.25,0,'$A$','east')+label(2.25,0,'$B$','west')+label(0,-.15,'$O$','north')+label(-1,.35,'3 cm')+label(1,.35,'3 cm')+label(0,-2.55,'Diamètre : 6 cm'),{'centre':[0,0],'rayon':3,'A':[-3,0],'B':[3,0]})
p=[(0,0),(2.4,0),(2.4,2.4),(0,2.4)]
add(33,'assemblage',path(p,'geoReponse')+r'\draw[geoReponse] (0,0) circle (1.8);'+points(p,'ABCD')+label(1.2,2.95,'Côté du carré : 4 cm')+label(1,-2.3,'Rayon du cercle : 3 cm'),{'carre':[[0,0],[4,0],[4,4],[0,4]],'rayon':3})
grid=r'\draw[otRule,step=.55] (0,0) grid (3.3,2.75);\draw[otRule,step=.55] (4.4,0) grid (7.7,2.75);'
pg=[(.55,.55),(2.2,1.1),(2.75,2.2),(1.1,1.65)]
# Noms à l'extérieur du contour ; le quadrillage est un fond de repérage.
grid+=path(pg)+points(pg,'ABCD')+r'\fill[otNavy] (4.95,.55) circle (1.7pt);'+label(4.8,.4,'$A$','north east')+label(1.65,-.4,'Modèle')+label(6.05,-.4,'À reproduire')
add(33,'quadrillage',grid,[[1,1],[4,2],[5,4],[2,3]])

def cube(x,y,w=1.4,h=1.4,d=.55):
 p=[(x,y),(x+w,y),(x+w,y+h),(x,y+h)];q=[(a+d,b+d) for a,b in p]
 s=path(p)
 for i in [1,2,3]:s+=path([p[i],q[i]],close=False)
 s+=path([q[1],q[2],q[3]],close=False)
 s+=path([p[0],q[0],q[1]],'geoAide',False)+path([q[0],q[3]],'geoAide',False)
 for a,b in p+q:s+=f'\\fill[otNavy] ({a},{b}) circle (1.6pt);'
 return s
def pyramid(x,y,tri=False):
 base=[(x,y),(x+1.8,y),(x+2.4,y+.65),(x+.6,y+.65)] if not tri else [(x,y),(x+2,y),(x+.7,y+.7)]
 top=(x+1.1,y+2.1);s=''
 for i,p in enumerate(base):s+=path([p,base[(i+1)%len(base)]],'geoAide' if i>=2 else 'geoTrait',False)
 for i,p in enumerate(base):s+=path([p,top],'geoAide' if i==len(base)-1 else 'geoTrait',False)
 for a,b in base+[top]:s+=f'\\fill[otNavy] ({a},{b}) circle (1.6pt);'
 return s
sol=cube(0,6.8)+label(.9,6.35,'A')+cube(3.6,6.8,2.0,1.1,.5)+label(4.8,6.35,'B')
sol+=r'\draw[geoTrait,fill=otSky] (.9,4.7) circle (.85);\draw[geoAide] (.05,4.7) arc[start angle=180,end angle=0,x radius=.85,y radius=.23];\draw[geoTrait] (.05,4.7) arc[start angle=180,end angle=360,x radius=.85,y radius=.23];'+label(.9,3.35,'C')
sol+=r'\draw[geoTrait] (3.9,4) -- (3.9,5.4);\draw[geoTrait] (5.7,4) -- (5.7,5.4);\draw[geoTrait] (4.8,5.4) ellipse (.9 and .25);\draw[geoTrait] (3.9,4) arc[start angle=180,end angle=360,x radius=.9,y radius=.25];\draw[geoAide] (3.9,4) arc[start angle=180,end angle=0,x radius=.9,y radius=.25];'+label(4.8,3.35,'D')
sol+=r'\draw[geoTrait] (0,0)--(.9,2)--(1.8,0);\draw[geoTrait] (0,0) arc[start angle=180,end angle=360,x radius=.9,y radius=.28];\draw[geoAide] (0,0) arc[start angle=180,end angle=0,x radius=.9,y radius=.28];'+label(.9,-.65,'E')+pyramid(3.7,0)+label(4.9,-.65,'F')
add(34,'solides',sol,{'lettres':['cube','pave','boule','cylindre','cone','pyramide_carree']})
add(34,'cube_cache',cube(0,0,3,3,.9),{'sommets':8,'aretes_visibles':9,'aretes_cachees':3})
add(34,'pyramides',pyramid(0,0,True)+pyramid(3.8,0)+label(1.1,-.55,'Base triangulaire')+label(4.95,-.55,'Base carrée'),{'triangulaire':{'faces':4,'aretes':6,'sommets':4},'carree':{'faces':5,'aretes':8,'sommets':5}})
netA=[(1,0),(0,1),(1,1),(2,1),(1,2),(1,3)];netB=[(i,0) for i in range(6)]
ns=''
for p in netA:
 x,y=p;ns+=path([(x*.8,y*.8),((x+1)*.8,y*.8),((x+1)*.8,(y+1)*.8),(x*.8,(y+1)*.8)])
ns+=label(1.2,-.4,'A')
for x,y in netB:ns+=path([(x*.8,4.4),((x+1)*.8,4.4),((x+1)*.8,5.2),(x*.8,5.2)])
ns+=label(2.4,5.7,'B')
add(34,'patrons',ns,{'A':netA,'B':netB,'cote_cm':3})

def symfigure(horizontal=False,sol=False):
 # Coordonnées en carreaux. Les deux points extrêmes sont sur l’axe.
 p=[(4,1),(1,2),(3,4),(4,5)]
 if horizontal:p=[(y,x) for x,y in p]
 axis=4;pp=[(x,2*axis-y) if horizontal else (2*axis-x,y) for x,y in p]
 s=r'\draw[otRule,step=.6] (0,0) grid (4.8,4.8);'
 s+=path([(0,2.4),(4.8,2.4)] if horizontal else [(2.4,0),(2.4,4.8)],'otOrange,line width=1.2pt',False)
 sp=[(x*.6,y*.6) for x,y in p];s+=path(sp,'geoTrait',False)
 # Les noms hors des traits du quadrillage seront sur fond blanc : faux positif documenté.
 for (x,y),name in zip(sp,'ABCD'):
  s+=f'\\fill[otNavy] ({x},{y}) circle (1.7pt);'+f'\\node[geoLabel,anchor=south east,xshift=-3pt,yshift=3pt] at ({x},{y}) {{${name}$}};'
 if sol:s+=path([(x*.6,y*.6) for x,y in pp],'geoReponse',False)
 s+=label(2.4,5.2,'Axe horizontal' if horizontal else 'Axe vertical')
 return s,{'points':p,'reportes':pp,'axe':'h' if horizontal else 'v','position':axis}
for h,name in [(False,'sym_v'),(True,'sym_h')]:
 for done in [False,True]:
  s,data=symfigure(h,done);add(35,name+('_corrige' if done else ''),s,data)
add(35,'sans_axe',path([(0,0),(4,0),(5,2),(1,2)])+label(2.5,-.5,'Quadrilatère à reproduire'),[[0,0],[4,0],[5,2],[1,2]])
axes=r'\draw[geoTrait] (0,0) rectangle (3,2);\draw[otGreenDark,dashed,line width=.8pt] (1.5,-.3)--(1.5,2.3);\draw[otGreenDark,dashed,line width=.8pt] (-.3,1)--(3.3,1);\draw[geoTrait] (4.5,0) rectangle (6.5,2);\draw[otGreenDark,dashed,line width=.8pt] (5.5,-.3)--(5.5,2.3);\draw[otGreenDark,dashed,line width=.8pt] (4.2,1)--(6.8,1);\draw[otGreenDark,dashed,line width=.8pt] (4.3,-.2)--(6.7,2.2);\draw[otGreenDark,dashed,line width=.8pt] (4.3,2.2)--(6.7,-.2);'
add(35,'axes',axes+label(1.5,-.75,'Rectangle : 2 axes')+label(5.5,-.75,'Carré : 4 axes'))

def barres(n,name,categories,values,step,title,xname):
 # Axes manuels : graduations régulières, labels extérieurs, aucun nombre dans les barres.
 maxv=max(values);height=3.6;width=5.4;stepy=height/(maxv/step)
 s=label(width/2,height+.9,title)+label(0,height+.35,'Élèves' if name!='echelle' else 'Personnes','west')
 for v in range(0,maxv+1,step):
  y=v/maxv*height;s+=path([(0,y),(width,y)],'otRule,line width=.35pt',False)+label(-.2,y,str(v),'east')
 s+=path([(0,height+.1),(0,0),(width+.1,0)],'otMuted,line width=.7pt',False)
 for k,(c,v) in enumerate(zip(categories,values)):
  x=.65+k*(width-.8)/len(values);bw=.65
  s+=f'\\draw[otNavy,fill=otNavy!45] ({x},0) rectangle ({x+bw},{v/maxv*height});'+label(x+bw/2,-.4,c)
 s+=label(width/2,-.9,xname)
 add(n,name,s,{'categories':categories,'valeurs':values,'pas':step,'max':maxv})
barres(36,'trajets',['À pied','Vélo','Bus'],[25,15,10],5,'Venir à l’école','Déplacement')
barres(36,'fratrie',['0','1','2','3'],[3,5,3,1],1,'Les frères et sœurs de 12 élèves','Frères et sœurs')
barres(36,'echelle',['A','B','C'],[20,40,60],10,'Les trois groupes','Groupe')

COURS={32:'''::: objectifs
Nommer les figures, compter leurs côtés et leurs sommets. Contrôler les longueurs avec la règle et les angles avec l’équerre.
:::

## I. Suivre le contour
::: definition Polygone
Un polygone est une figure fermée formée de segments. Un segment du contour est un **côté** ; un coin est un **sommet**.
:::

| Nom | Côtés | Sommets |
|---|---|---|
| Triangle | 3 | 3 |
| Quadrilatère | 4 | 4 |
| Pentagone | 5 | 5 |
| Hexagone | 6 | 6 |

::: methode Compter
Pars d’un sommet. Fais le tour du contour en comptant chaque côté une seule fois. Recommence pour les sommets.
:::

## II. Reconnaître les quadrilatères
::: propriete
- Un rectangle a **4 angles droits** ; ses côtés opposés ont la même longueur.
- Un losange a **4 côtés de même longueur**.
- Un carré a **4 côtés de même longueur et 4 angles droits** : c’est aussi un rectangle et un losange.
:::

[IMAGE_1]

Dans ce dessin, A est un carré tourné, B un rectangle non carré et C un losange non carré.

::: methode Contrôler
Pose le coin droit de l’équerre sur chaque sommet et un bord contre un côté. L’autre bord doit aussi coïncider pour avoir un angle droit. Compare les côtés à la règle, sur une copie à taille réelle.
:::

::: attention
Tourner une figure ne change ni ses longueurs ni ses angles. Des côtés opposés égaux ne suffisent pas à prouver qu’une figure est un rectangle : il faut vérifier ses angles.
:::

## III. Comparer les angles
::: definition
Un angle **aigu** est moins ouvert qu’un angle droit. Un angle **obtus** est plus ouvert qu’un angle droit. On peut comparer avec le coin droit d’une feuille ou une équerre.

Un **triangle rectangle** est un triangle qui possède un angle droit.
:::

[IMAGE_2]

A est aigu ; B est droit ; C est obtus. On compare l’ouverture, pas la longueur des traits. Un petit carré sert à **coder** un angle droit après l’avoir vérifié.

## IV. Diagonale, cercle et disque
::: definition
Une **diagonale** d’un quadrilatère relie deux sommets opposés. Un quadrilatère a deux diagonales.

Le **cercle** est le contour rond. Le **disque** comprend ce contour et tout son intérieur. Ce ne sont pas des polygones.
:::

::: exemple
Dans un rectangle ABCD nommé dans l’ordre du contour, les diagonales sont AC et BD.
:::

::: retenir
Je nomme une figure grâce à ses propriétés. Je compte, je compare et je vérifie avec mes instruments.
:::
''',33:'''::: objectifs
Tracer des segments, trouver un milieu, utiliser l’équerre et le compas. Construire puis contrôler des figures sur une feuille.
:::

## I. Règle : segment et milieu
::: definition
Un **segment** s’arrête à ses deux extrémités. Une **droite** se prolonge des deux côtés. Le **milieu** partage un segment en deux parties de même longueur.
:::

::: methode Tracer 8 cm
Place le premier point devant le **zéro** de la règle, pas devant son bord. Marque le second point devant 8 cm puis relie-les. Le milieu est à 4 cm de chaque extrémité. Vérifie : 4 cm + 4 cm = 8 cm.
:::

[IMAGE_1]

## II. Compas : cercle, rayon et diamètre
::: definition
Le **centre** reste fixe. Le **rayon** est la distance du centre au cercle. Un **diamètre** relie deux points du cercle en passant par le centre ; il mesure deux rayons mis bout à bout.
:::

::: methode Tracer un cercle
Règle l’ouverture sur la règle. Pique la pointe sèche au centre. Tourne le crayon sans changer l’ouverture et sans déplacer la pointe sèche. Pour passer par un point donné, règle l’ouverture du centre jusqu’à ce point.
:::

[IMAGE_2]

::: exemple
Un cercle de rayon 3 cm a un diamètre de 6 cm : 3 cm + 3 cm = 6 cm. Tous les points de ce cercle sont à 3 cm de son centre.
:::

## III. Équerre : construire un rectangle
::: methode Rectangle de 7 cm sur 3 cm
1. Trace AB de 7 cm.
2. En A, place le coin droit de l’équerre contre AB. Trace AD de 3 cm le long de l’autre bord.
3. En B, trace BC de 3 cm avec un angle droit, du même côté de AB que D.
4. Relie C à D. Vérifie les quatre angles et les quatre longueurs.
5. Ajoute les petits carrés des angles droits et les codes des côtés égaux.
:::

[IMAGE_3]

Pour un carré, les quatre côtés ont la même longueur. Pour un triangle rectangle, construis deux côtés de l’angle droit puis relie leurs extrémités.

## IV. Reproduire et contrôler
::: methode Sur quadrillage
Place un premier sommet. Compte les carreaux vers la droite ou la gauche puis vers le haut ou le bas pour chaque sommet suivant. Relie dans le même ordre. Compte les intervalles, pas les lignes.
:::

::: attention
Les images sont des modèles réduits : construis les longueurs annoncées sur ta feuille. La pointe du compas reste fixe ; l’équerre contrôle les angles ; la règle contrôle les longueurs.
:::

::: retenir
Je prépare mes instruments, je construis un élément à la fois et je contrôle avant d’ajouter les codes.
:::
''',34:'''::: objectifs
Reconnaître six solides. Décrire les faces, les arêtes et les sommets. Prévoir un patron du cube puis le vérifier par un vrai pliage.
:::

## I. Reconnaître les solides
[IMAGE_1]

::: definition
A : cube. B : pavé. C : boule. D : cylindre. E : cône. F : pyramide à base carrée.

Une **face** est une surface plane du solide. Une **arête** est le bord commun à deux faces planes. Un **sommet** est un coin où se rejoignent des arêtes.
:::

::: exemple
Une balle pleine ressemble à une boule ; une boîte de conserve à un cylindre ; un chapeau de fête à un cône.
:::

## II. Décrire et compter
::: propriete
| Solide | Faces | Arêtes | Sommets |
|---|---|---|---|
| Cube | 6 carrés de même taille | 12 | 8 |
| Pavé | 6 rectangles | 12 | 8 |
| Pyramide à base triangulaire | 4 triangles | 6 | 4 |
| Pyramide à base carrée | 1 carré et 4 triangles | 8 | 5 |

Les faces d’un pavé peuvent être carrées. Dans une pyramide, les faces qui montent au sommet sont des triangles ; la base est un polygone.
:::

::: methode Manipuler
Compte sur un objet réel. Marque chaque face, arête ou sommet déjà compté. Pour un cube, compte 4 arêtes en haut, 4 en bas et 4 qui les relient : 12 arêtes.
:::

::: attention Lire une vue
Un dessin cache des bords. Les pointillés peuvent représenter les **arêtes cachées**. Elles existent et doivent être comptées. Sur une vue de cube, des faces carrées paraissent penchées.
:::

## III. Construire un squelette
::: methode
Utilise une tige pour chaque arête et une boule de pâte pour chaque sommet. Pour une pyramide à base carrée, prépare 4 tiges de base puis 4 qui montent : 8 tiges ; il faut 5 boules de pâte.
:::

## IV. Vérifier un patron du cube
::: definition
Un **patron** du cube est un assemblage de six carrés de même taille qui se ferme par pliage, sans superposer les faces.
:::

[IMAGE_2]

::: methode Prévoir, puis plier
Recopie chaque assemblage avec des carrés de 3 cm sur du papier. Avec un adulte, découpe le contour extérieur sans séparer les carrés. Marque les plis entre carrés. Prévois ce qui se ferme, puis plie réellement : A forme un cube, B ne le ferme pas.
:::

::: retenir
Six carrés sont nécessaires, mais leur disposition compte aussi. Cinq carrés ne suffisent pas. Je vérifie toujours un patron en manipulant.
:::
''',35:'''::: objectifs
Trouver un axe par pliage ou avec du calque. Compléter une figure sur quadrillage autour d’un axe vertical ou horizontal.
:::

## I. Essayer un pli
::: definition Axe de symétrie
Une droite est un **axe de symétrie** si les deux parties de la figure se superposent entièrement quand on plie sur cette droite.
:::

::: methode Vérifier
Dessine et découpe la figure. Plie sur la droite essayée, ou recopie sur du calque et retourne-le autour de cette droite. Compare tous les bords et tous les coins. Deux côtés égaux ne suffisent pas à prouver la symétrie.
:::

[IMAGE_1]

::: exemple
Un rectangle non carré a 2 axes : les deux plis qui passent par les milieux de côtés opposés. Ses diagonales ne sont pas des axes. Un carré a 4 axes : ces deux plis et les deux diagonales. Vérifie-les sur des figures découpées.
:::

## II. Un axe vertical
::: methode Compter les carreaux
1. Repère un sommet.
2. Compte les carreaux jusqu’à l’axe.
3. Garde la même ligne horizontale.
4. Reporte le même nombre de carreaux de l’autre côté.
5. Recommence pour les autres sommets et relie-les dans le même ordre.
:::

[IMAGE_2]

::: exemple
Un point à 3 carreaux à gauche de l’axe se reporte à 3 carreaux à droite, sur la même ligne. Un point situé **sur l’axe reste au même endroit**.
:::

## III. Un axe horizontal
::: methode
Garde la même colonne. Un point à 2 carreaux au-dessus du pli se reporte à 2 carreaux au-dessous. Reporte tous les sommets, puis relie-les dans le même ordre.
:::

::: attention
Compte les intervalles entre les lignes du quadrillage. Les deux distances au pli doivent être égales : 3 carreaux d’un côté demandent 3 carreaux de l’autre, pas 2. Vérifie ton dessin par pliage ou calque.
:::

::: retenir
Je change de côté, je garde la même distance au pli. Sur l’axe, je reste à la même place.
:::
''',36:'''::: objectifs
Recueillir des réponses, les compter et les organiser. Lire un tableau, lire et construire un diagramme en barres avec une échelle régulière.
:::

## I. Faire une enquête
::: methode Une réponse par personne
Pose la même question à chaque personne. Note chaque réponse une seule fois. Trie les réponses, puis compte combien de personnes ont donné chaque réponse : ce nombre est l’**effectif**.
:::

::: exemple
Douze élèves indiquent leur nombre de frères et sœurs. Après comptage :

| Frères et sœurs | Nombre d’élèves |
|---|---|
| 0 | 3 |
| 1 | 5 |
| 2 | 3 |
| 3 | 1 |

Vérification : 3 + 5 + 3 + 1 = 12. On ne somme pas les réponses 0, 1, 2, 3 pour compter les personnes.
:::

## II. Lire un diagramme en barres
[IMAGE_1]

::: methode
Lis le titre, les catégories et l’échelle. Ici, les graduations montent de **5 élèves en 5 élèves**. Suis le haut d’une barre jusqu’à la graduation correspondante : la barre Vélo représente 15 élèves.
:::

::: exemple
À pied ou en bus : 25 + 10 = 35 élèves. Le graphique compte 25 + 15 + 10 = 50 élèves en tout.
:::

## III. Construire un graphique
::: methode
1. Trace deux axes et place le zéro.
2. Nomme les catégories sous les barres.
3. Choisis une échelle régulière qui permet de placer le plus grand effectif.
4. Trace les barres depuis zéro avec la même largeur et la même échelle.
5. Ajoute un titre, le nom des axes et vérifie les hauteurs avec le tableau.
:::

::: exemple
Pour 20, 40 et 60 personnes sur six grands intervalles, choisis 10 personnes par intervalle. Les barres atteignent les deuxième, quatrième et sixième graduations après zéro.
:::

## IV. Lire un tableau à double entrée
'''+TABLE+'''

::: methode
Croise la ligne et la colonne demandées. La ligne Dessin et la colonne Mardi se croisent dans la case 18. Pour le total du lundi, additionne les deux cases de la colonne : 12 + 8 = 20.
:::

::: attention
Une barre trois fois plus haute que le premier intervalle ne signifie pas forcément trois personnes : commence par lire l’échelle. Garde le même écart entre les graduations.
:::

::: retenir
Je compte une fois chaque personne. Je vérifie les totaux et l’échelle avant de comparer les résultats.
:::
'''}
FICHES={32:'''::: objectifs
Reconnaître et décrire les figures.
:::

## I. Les repères
- Polygone : contour fermé formé de segments.
- Triangle : 3 côtés ; quadrilatère : 4 ; pentagone : 5 ; hexagone : 6. Il y a autant de sommets que de côtés.
- Rectangle : 4 angles droits, côtés opposés de même longueur.
- Losange : 4 côtés de même longueur.
- Carré : 4 côtés de même longueur et 4 angles droits.

## II. Les gestes
::: methode
Je compte en suivant le contour. Je compare les côtés avec la règle et les coins avec l’équerre. Un angle aigu est moins ouvert qu’un angle droit ; un angle obtus est plus ouvert.
:::

::: retenir
Une diagonale relie deux sommets opposés ; un quadrilatère a 2 diagonales. Cercle : contour ; disque : contour et intérieur.
:::

::: attention
Un carré tourné reste un carré, donc aussi un rectangle et un losange. Je vérifie les propriétés, pas seulement l’allure.
:::
''',33:'''::: objectifs
Construire avec les bons instruments.
:::

## I. Les outils
- Règle : tracer droit et mesurer depuis le zéro.
- Équerre : vérifier ou tracer un angle droit.
- Compas : tracer un cercle, centre fixe et ouverture constante.

## II. Les repères
- Segment : deux extrémités ; droite : elle se prolonge.
- Milieu : deux longueurs égales. Pour 8 cm : 4 cm de chaque côté.
- Rayon : du centre au cercle. Diamètre : traverse le centre, deux rayons bout à bout. Rayon de 3 cm : diamètre de 6 cm.

::: methode Construire
Trace un premier côté, construis les angles droits, reporte les longueurs, puis ferme la figure. Pour un rectangle : quatre angles droits et côtés opposés égaux. Pour un carré : quatre angles droits et quatre côtés égaux.
:::

::: attention
Je contrôle avant de coder. Les images sont réduites : je trace les mesures demandées sur ma feuille. Sur quadrillage, je compte les intervalles.
:::
''',34:'''::: objectifs
Décrire les solides et vérifier un patron.
:::

## I. Les repères
- Cube : 6 faces carrées de même taille, 12 arêtes, 8 sommets.
- Pavé : 6 faces rectangulaires, 12 arêtes, 8 sommets.
- Pyramide carrée : 1 face carrée, 4 triangles, 8 arêtes, 5 sommets.
- Pyramide triangulaire : 4 triangles, 6 arêtes, 4 sommets.
- Boule : toute ronde ; cylindre : deux bases en disques ; cône : une base en disque et une pointe.

## II. Les gestes
::: methode
Je compte sur un objet en marquant ce qui est déjà compté. Pour un squelette : une tige par arête, une boule de pâte par sommet.
:::

::: retenir
Un patron du cube a 6 carrés de même taille, bien disposés. Je prévois, je découpe le contour, je plie et je vérifie que le cube se ferme sans faces superposées.
:::

::: attention
Les pointillés peuvent montrer des arêtes cachées : elles existent. Six carrés ne suffisent pas si leur disposition ne convient pas.
:::
''',35:'''::: objectifs
Vérifier et compléter une symétrie.
:::

## I. Un pli qui fonctionne
::: definition
Un axe de symétrie permet de superposer toute la figure en pliant sur lui. Je vérifie par pliage ou calque.
:::

- Rectangle non carré : 2 axes.
- Carré : 4 axes.

## II. Compléter sur quadrillage
::: methode
Avec un axe vertical : même ligne, même nombre de carreaux de l’autre côté.

Avec un axe horizontal : même colonne, même nombre de carreaux de l’autre côté.

Je reporte chaque sommet puis je relie dans le même ordre.
:::

::: attention
Je compte les intervalles. Un point sur l’axe reste à sa place. Deux côtés égaux ne prouvent pas qu’un axe existe : je contrôle toute la figure.
:::
''',36:'''::: objectifs
Organiser et lire des données.
:::

## I. Enquêter
::: methode
Une question identique et une seule réponse par personne. Je compte les réponses par catégorie, je remplis un tableau et je vérifie le total.
:::

## II. Lire ou construire
- Tableau : je croise la bonne ligne et la bonne colonne.
- Graphique : je lis le titre, les catégories et les graduations avant les barres.
- Pour construire : zéro, axes nommés, barres de même largeur et une échelle régulière.

::: exemple
Une graduation vaut 5 élèves : la troisième graduation après zéro vaut 15 élèves. Pour 20, 40 et 60 personnes, on peut prendre 10 personnes par graduation.
:::

::: attention
Le nombre de frères et sœurs est une réponse ; le nombre d’élèves qui donnent cette réponse est un effectif. Je garde la même échelle pour toutes les barres.
:::
'''}

VERIF=r'''"""Relit les documents livrés et les coordonnées TikZ ; aucune donnée en base."""
from pathlib import Path
import importlib.util,json,re,math,collections
P=Path(__file__).resolve().parent
D=json.loads((P/'donnees_pedagogiques.json').read_text(encoding='utf-8'))
spec=importlib.util.spec_from_file_location('figures_locales',P/'figures/figures.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
G=f.GEOMETRIE;code=D['chapitre'];checks=[]
def check(b,label):
 assert b,label
 checks.append(label)
text=(P/'exercices.txt').read_text(encoding='utf-8');blocks=[b.strip() for b in re.split(r'^===[ \t]*$',text,flags=re.M) if b.strip()]
check(len(blocks)==9,'9 exercices conservant les 9 compétences sources')
for i,(b,e) in enumerate(zip(blocks,D['exercices']),1):
 check(f'Id: nouveau-{i}\n' in b,f'ex{i} identifiant')
 enonce=b.split('Énoncé:\n',1)[1].split('Étapes:\n',1)[0];etapes=b.split('Étapes:\n',1)[1].split('Solution:\n',1)[0];solution=b.split('Solution:\n',1)[1]
 check(len(re.findall(r'^\d+\. ',enonce,re.M))==5,f'ex{i} cinq questions réelles')
 check(len(re.findall(r'^## Question ',etapes,re.M))==5,f'ex{i} cinq corrections')
 for j,(question,raison,reponse) in enumerate(e['questions'],1):
  check(f'{j}. {question}' in enonce,f'ex{i} Q{j} énoncé actuel')
  sec=re.search(rf'^## Question {j} :.*?(?=^## Question |\Z)',etapes,re.M|re.S)[0]
  check(all(f'::: {k}' in sec for k in ('methode','etape','resultat')),f'ex{i} Q{j} méthode étape résultat')
  check(raison in sec and reponse in sec,f'ex{i} Q{j} résultat développé actuel')
  check(f'{j}. {reponse}' in solution,f'ex{i} Q{j} solution actuelle')
 # Recalcul indépendant de TOUTES les égalités entières réellement présentes.
 for expression,result in re.findall(r'(?<![\w])([0-9]+(?:\s*[+−×]\s*[0-9]+)+)\s*=\s*([0-9]+)',b):
  check(eval(expression.replace('−','-').replace('×','*'),{'__builtins__':{}},{})==int(result),f'ex{i} calcul {expression}={result}')
for name in ('cours_nouveau.txt','fiche_nouvelle.txt'):
 s=(P/name).read_text(encoding='utf-8');check(s.startswith('Titre: ') and '<!-- optitab:1 -->' in s,name+' format')
 for expression,result in re.findall(r'(?<![\w])([0-9]+(?:\s*[+−×]\s*[0-9]+)+)\s*=\s*([0-9]+)',s):
  check(eval(expression.replace('−','-').replace('×','*'),{'__builtins__':{}},{})==int(result),name+' '+expression)
def lengths(p):return [math.dist(a,b) for a,b in zip(p,p[1:]+p[:1])]
def rights(p):
 return [abs((p[i-1][0]-b[0])*(p[(i+1)%len(p)][0]-b[0])+(p[i-1][1]-b[1])*(p[(i+1)%len(p)][1]-b[1]))<1e-8 for i,b in enumerate(p)]
def eq(a,b):return math.isclose(a,b,abs_tol=1e-8)
def drawpaths(name,style):
 bodies=re.findall(r'\\draw\['+re.escape(style)+r'\]\s*([^;]+);',f.FIGURES[name])
 return [[tuple(map(float,p)) for p in re.findall(r'\((-?[\d.]+),(-?[\d.]+)\)',s)] for s in bodies]
def samecoords(a,b):return len(a)==len(b) and all(eq(x,u) and eq(y,v) for (x,y),(u,v) in zip(a,b))
if code==32:
 for actual,expected in zip(drawpaths('quadrilateres','geoTrait'),G['quadrilateres']):check(samecoords(actual,expected),'TikZ quadrilatère correspondant aux coordonnées testées')
 a,b,c=G['quadrilateres'];check(all(rights(a)) and max(lengths(a))-min(lengths(a))<1e-8,'A carré tourné exact')
 check(all(rights(b)) and not eq(lengths(b)[0],lengths(b)[1]),'B rectangle non carré exact')
 check(not any(rights(c)) and max(lengths(c))-min(lengths(c))<1e-8,'C losange non carré exact')
 check([len(p) for p in G['polygones']]==[5,6],'pentagone hexagone exacts')
 check(G['angles']==[45,90,120],'angles aigu droit obtus sans codes révélateurs')
 for actual,angle in zip(drawpaths('angles','geoTrait'),G['angles']):
  a,b,c=actual;u=(a[0]-b[0],a[1]-b[1]);v=(c[0]-b[0],c[1]-b[1]);value=math.degrees(math.acos(sum(x*y for x,y in zip(u,v))/(math.hypot(*u)*math.hypot(*v))))
  check(eq(value,angle),'ouverture tracée TikZ '+str(angle))
 check('A est un carré.' in text and 'B est un rectangle' in text and 'C est un losange' in text,'classement actuel des figures')
if code==33:
 check([math.dist(G['milieu'][i],G['milieu'][i+1]) for i in [0,1]]==[4,4],'milieu 8 cm réel')
 for name,scale,w,h in [('rectangle',.8,7,3),('carre',.7,5,5)]:
  p=G[name];check(all(rights(p)) and eq(lengths(p)[0]/scale,w) and eq(lengths(p)[1]/scale,h),name+' angles et longueurs exacts')
  check(samecoords(drawpaths(name,'geoReponse')[0],p),name+' tracé TikZ conforme aux coordonnées')
 p=G['triangle'];check(rights(p)[0] and eq(math.dist(p[0],p[1])/.7,6) and eq(math.dist(p[0],p[2])/.7,4),'triangle rectangle 6 sur 4 exact')
 for name in ['cercle','diametre']:
  c=G[name];check(eq(math.dist(c['centre'],c['A']),c['rayon']) and eq(math.dist(c['centre'],c['B']),c['rayon']),name+' rayons exacts')
 check(eq(math.dist(G['diametre']['A'],G['diametre']['B']),6),'diamètre 6 cm exact')
 p=G['quadrillage'];moves=[(b[0]-a[0],b[1]-a[1]) for a,b in zip(p,p[1:]+p[:1])]
 check(moves==[(3,1),(1,2),(-3,-1),(-1,-2)],'déplacements de reproduction exacts')
 check('Depuis A : 3 carreaux à droite et 1 vers le haut.' in text,'déplacement A B actuel')
if code==34:
 # Comptage combinatoire des solides, indépendant des phrases de solution.
 for k in [3,4]:
  expected={'faces':k+1,'aretes':2*k,'sommets':k+1};name='triangulaire' if k==3 else 'carree'
  check(G['pyramides'][name]==expected,name+' faces arêtes sommets')
 check(G['cube_cache']['aretes_visibles']+G['cube_cache']['aretes_cachees']==12,'cube 12 arêtes visibles cachées')
 check(len(G['solides']['lettres'])==6,'six solides dessinés pour six annoncés')
 # Propagation exacte de repères 3D sur le réseau de carrés. Deux normales
 # identiques impliquent deux faces superposées, donc un faux patron.
 def neg(v):return tuple(-a for a in v)
 def faces(net):
  cells={tuple(c) for c in net};start=min(cells);seen={start:((1,0,0),(0,1,0),(0,0,1))};todo=[start];coherent=True
  while todo:
   x,y=todo.pop();u,v,n=seen[x,y]
   for dx,dy,frame in [(1,0,(neg(n),v,u)),(-1,0,(n,v,neg(u))),(0,1,(u,neg(n),v)),(0,-1,(u,n,neg(v)))]:
    other=(x+dx,y+dy)
    if other not in cells:continue
    if other in seen:coherent &= seen[other]==frame
    else:seen[other]=frame;todo.append(other)
  return coherent and len(seen)==6 and len({frame[2] for frame in seen.values()})==6
 check(faces(G['patrons']['A']),'patron A six normales 3D distinctes')
 check(not faces(G['patrons']['B']),'bande B se superpose après pliage')
 drawn=drawpaths('patrons','geoTrait')
 expectedA=[[(x*.8,y*.8),((x+1)*.8,y*.8),((x+1)*.8,(y+1)*.8),(x*.8,(y+1)*.8)] for x,y in G['patrons']['A']]
 expectedB=[[(x*.8,4.4),((x+1)*.8,4.4),((x+1)*.8,5.2),(x*.8,5.2)] for x,y in G['patrons']['B']]
 check(len(drawn)==12 and all(samecoords(a,b) for a,b in zip(drawn,expectedA+expectedB)),'douze carrés TikZ égaux et dispositions des patrons vérifiées')
 check('A se ferme en un cube à 6 faces.' in text and 'B ne ferme pas un cube.' in text,'prévisions actuelles cohérentes avec pliage 3D')
if code==35:
 for name in ['sym_v','sym_v_corrige','sym_h','sym_h_corrige']:
  g=G[name];axis=g['position'];expected=[(x,2*axis-y) if g['axe']=='h' else (2*axis-x,y) for x,y in g['points']]
  check([list(p) for p in expected]==g['reportes'],name+' report exact de tous sommets')
  check(samecoords(drawpaths(name,'geoTrait')[0],[(x*.6,y*.6) for x,y in g['points']]),name+' points réellement tracés')
  if name.endswith('_corrige'):check(samecoords(drawpaths(name,'geoReponse')[0],[(x*.6,y*.6) for x,y in g['reportes']]),name+' correction réellement tracée')
  check(eq(sum(lengths(g['points'])),sum(lengths(g['reportes']))),name+' longueurs conservées')
 p=G['sans_axe'];check(eq(lengths(p)[0],lengths(p)[2]) and not any(rights(p)) and not eq(lengths(p)[0],lengths(p)[1]),'parallélogramme non rectangle non losange')
 check('B se reporte à 3 carreaux à droite' in text and 'B se reporte à 3 carreaux au-dessous' in text,'reports énoncés actuels verticaux et horizontaux')
 check('Le carré possède 4 axes' in text and 'possède 2 axes de symétrie' in text,'nombres d’axes actuels')
if code==36:
 values=[0,1,2,1,0,3,2,1,1,0,2,1];counts=collections.Counter(values)
 check([counts[i] for i in range(4)]==G['fratrie']['valeurs']==[3,5,3,1],'dépouillement réel des 12 réponses')
 check(sum(G['fratrie']['valeurs'])==12,'total enquête')
 check(G['trajets']['valeurs']==[25,15,10] and G['trajets']['pas']==5,'hauteurs et échelle trajets')
 check(G['echelle']['valeurs']==[20,40,60] and G['echelle']['pas']==10,'hauteurs et échelle groupes')
 for name,g in G.items():
  check(all(v%g['pas']==0 for v in g['valeurs']) and g['max']==max(g['valeurs']),name+' graduations régulières')
  rectangles=re.findall(r'\\draw\[otNavy,fill=otNavy!45\]\s*\([\d.]+,0\) rectangle \([\d.]+,([\d.]+)\)',f.FIGURES[name])
  check(len(rectangles)==len(g['valeurs']) and all(eq(float(h),v/g['max']*3.6) for h,v in zip(rectangles,g['valeurs'])),name+' hauteurs réellement tracées TikZ')
  labels=re.findall(r'\\node\[anchor=east,text=otInk\] at \(-0.2,([\d.]+)\) \{(\d+)\}',f.FIGURES[name])
  check([int(v) for _,v in labels]==list(range(0,g['max']+1,g['pas'])),name+' graduations réellement dessinées')
 check('15 élèves viennent à vélo.' in text and '35 élèves viennent à pied ou en bus.' in text,'lectures graphique actuelles')
 check('50 élèves viennent en voiture.' in text and 100-sum(G['trajets']['valeurs'])==50,'complément voitures actuel')
 check('Le mardi compte 25 inscriptions.' in text and 'L’écart est de 5 inscriptions.' in text and (18+7)-(12+8)==5,'tableau double entrée actuel')
mapping=json.loads((P/'figures/correspondance.json').read_text(encoding='utf-8'));used=[]
for family,docs in mapping.items():
 for ident,positions in docs.items():
  for position,meta in positions.items():
   check(meta['fichier'].removesuffix('.png') in f.FIGURES,'figure référencée '+meta['fichier']);used.append(meta['fichier'])
report={'math_OK':True,'chapitre':code,'exercices':9,'questions':45,'controles':len(checks),'details':checks,'figures_referencees':sorted(set(used))}
(P/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False))
'''

def writeall():
 course_figs={32:['quadrilateres','angles'],33:['milieu','diametre','rectangle'],34:['solides','patrons'],35:['axes','sym_v_corrige'],36:['trajets']}
 corrections={32:{4:'triangle_corrige',6:'diagonales_corrige'},33:{1:'milieu',2:'cercle',3:'diametre',4:'rectangle',5:'carre',6:'triangle',7:'assemblage'},34:{},35:{3:'sym_v_corrige',6:'sym_h_corrige'},36:{3:'fratrie',8:'echelle'}}
 for n,exs in CH.items():
  folder=next(ROOT.glob(f'{n:02}_*'));source=json.loads((folder/'sources_locales/chapitre.json').read_text(encoding='utf-8'));title=source['titre']
  (folder/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'ce2_geometrie_donnees','maj':'2026-11-02'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  (folder/'cours_nouveau.txt').write_text('Titre: '+title+'\n\n<!-- optitab:1 -->\n'+COURS[n],encoding='utf-8')
  (folder/'fiche_nouvelle.txt').write_text('Titre: Résumé : '+title+'\n\n<!-- optitab:1 -->\n'+FICHES[n],encoding='utf-8')
  m={'cours':{'nouveau':{}},'fiches':{'nouvelle':{}},'exercices':{}}
  def mapping(group,key,pos,name):m[group].setdefault(key,{})[str(pos)]={'fichier':name+'.png','alt':ALT[name]}
  for j,name in enumerate(course_figs[n],1):mapping('cours','nouveau',j,name)
  blocks=[]
  for i,e in enumerate(exs,1):
   key=f'nouveau-{i}';prefix='Découverte' if i<=3 else 'Entraînement' if i<=7 else 'Problème'
   enonce=e['contexte']+'\n\n'
   if e['image']:enonce+='[IMAGE_1]\n\n';mapping('exercices',key,1,e['image'])
   enonce+='\n'.join(f'{j}. {row[0]}' for j,row in enumerate(e['questions'],1))
   etapes=[]
   for j,(question,raison,reponse) in enumerate(e['questions'],1):
    method=method_for(n,question)
    # Le titre reprend la tâche précise ; aucune question n’est laissée sans démarche.
    step=f'## Question {j} : {question}\n\n::: methode\n{method}\n:::\n\n::: etape Observer et vérifier\n{raison}\n:::\n\n::: resultat\n{reponse}\n:::\n'
    if j==5 and i in corrections[n]:
     pos=2 if e['image'] else 1;name=corrections[n][i];mapping('exercices',key,pos,name);step+=f'\nModèle de contrôle du tracé :\n\n[IMAGE_{pos}]\n'
    etapes.append(step)
   sol='\n'.join(f'{j}. {row[2]}' for j,row in enumerate(e['questions'],1))
   blocks.append(f'=== {prefix} - {e["titre"]}\nId: {key}\nDifficulté: '+('easy' if i<=3 else 'medium')+'\n\nÉnoncé:\n<!-- optitab:1 -->\n'+enonce+'\n\nÉtapes:\n<!-- optitab:1 -->\n'+'\n'.join(etapes)+'\nSolution:\n<!-- optitab:1 -->\n'+sol+'\n')
  (folder/'exercices.txt').write_text('\n===\n\n'.join(blocks),encoding='utf-8')
  (folder/'donnees_pedagogiques.json').write_text(json.dumps({'chapitre':n,'exercices':exs},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  figdir=folder/'figures';figdir.mkdir(exist_ok=True)
  tol={}
  # Les noms sur quadrillage sont posés dans des cases sans toucher le contour.
  (figdir/'figures.py').write_text('# -*- coding: utf-8 -*-\n"""Figures TikZ locales ; préambule officiel fourni par figures_livre.py."""\nFIGURES = '+repr(FIG[n])+'\nGEOMETRIE = '+repr(json.loads(json.dumps(GEO[n])))+'\nTOLERE = '+repr(tol)+'\n',encoding='utf-8')
  (figdir/'correspondance.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  (folder/'verif_math.py').write_text(VERIF,encoding='utf-8')
  rows=['# Couverture pédagogique CE2 — chapitre '+str(n),'','Source locale : `sources_locales/chapitre.json` (lecture seule). Les 9 compétences des 9 exercices du livre sont conservées, chacune déclinée en cinq questions guidées. Aucun exercice supplémentaire nécessaire.','', '| Exercice | Compétence source conservée | Questions finales |','|---|---|---|']
  for i,(s,e) in enumerate(zip(source['exercices'],exs),1):rows.append(f'| nouveau-{i} | '+s['consigne'].replace('|','/')+' | 5 |')
  rows+=['','Cadre : programme officiel du cycle 2, CE2, pages 35–38 (solides, géométrie plane, données). Pliages réellement demandés pour les patrons et les axes ; constructions sur feuille avec instruments. Aucune mesure d’angle en degrés demandée à l’élève, aucune formule d’aire/volume, aucun axe oblique à compléter.','', '[Programme officiel](https://www.education.gouv.fr/sites/default/files/document/Annexe%204%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20du%20cycle%202-403821.pdf)']
  (folder/'COUVERTURE.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')
  (folder/'RAPPORT.md').write_text(f'# Chapitre {n} — {title}\n\nÉtat : rédaction terminée, compilation et relecture visuelle à réaliser avant passage prêt.\n\nCréation CE2, niveau 11 : aucune ancienne ressource en ligne et aucun identifiant numérique. Cours et fiche structurés au format commun. Neuf exercices, cinq questions par exercice, méthode, démarche détaillée et résultat pour chaque question, solutions courtes concordantes. Toutes les compétences sources sont conservées.\n\nFigures : {len(FIG[n])} nouvelles figures TikZ avec préambule officiel ; aucune image ancienne conservée. Les figures de reconnaissance ne portent pas les codes qui révéleraient la réponse.\n\nContrôle mathématique : `verif_math.py` relit les textes actuels, toutes les réponses, les égalités entières et les coordonnées des figures ; géométrie vérifiée indépendamment (longueurs, angles, reports, pliage 3D des patrons ou données selon la notion).\n\nContrôles visuels et navigateur à compléter. Aucune écriture en base.\n',encoding='utf-8')
  print(n,len(exs),'exercices',sum(len(e['questions']) for e in exs),'questions',len(FIG[n]),'figures')

METHODES={32:'Compter les éléments et vérifier les propriétés avec les instruments.',33:'Suivre les mesures et contrôler chaque geste avec le bon instrument.',34:'Manipuler le solide ou l’assemblage et compter chaque élément une seule fois.',35:'Utiliser le pliage, le calque ou le report du même nombre de carreaux.',36:'Repérer les bonnes données puis compter, calculer ou construire en gardant la même échelle.'}
def method_for(n,question):
 low=question.lower()
 if n==32:
  if 'combien' in low:return 'Faire le tour de la figure en comptant chaque élément une seule fois.'
  if 'angle' in low or 'ouvert' in low:return 'Comparer l’ouverture avec le coin droit de l’équerre.'
  if 'diagonale' in low or 'opposé' in low:return 'Repérer les sommets qui ne sont pas voisins sur le contour.'
  if 'cercle' in low or 'disque' in low:return 'Distinguer les points du contour et les points de la surface intérieure.'
 if n==33:
  if 'compas' in low or 'ouverture' in low or 'pointe' in low:return 'Repérer le centre puis régler le compas à la longueur du rayon.'
  if 'de a à b' in low or 'de b à c' in low or 'de c à d' in low:return 'Compter séparément le déplacement horizontal puis vertical.'
  if 'code' in low:return 'Vérifier les mesures et les angles avant de placer les codes.'
  if 'trace' in low or 'construis' in low:return 'Placer les points avec la règle et contrôler les coins avec l’équerre.'
 if n==34:
  if 'combien' in low:return 'Séparer les éléments du bas, du haut et du tour pour éviter de compter deux fois.'
  if 'plie' in low or 'pliage' in low or 'assemblage' in low:return 'Prévoir la place des faces puis vérifier en découpant et en pliant.'
  if 'nomme' in low:return 'Observer la forme des surfaces, les bords et les pointes du solide.'
 if n==35:
  if 'reporte' in low or 'place' in low:return 'Garder la ligne ou la colonne et reporter la même distance de l’autre côté du pli.'
  if 'pli' in low or 'axe' in low:return 'Essayer le pli et vérifier la superposition de tous les bords.'
 if n==36:
  if 'combien ont répondu' in low or 'combien d’élèves ont répondu' in low:return 'Repérer la réponse demandée et compter chacune de ses apparitions une seule fois.'
  if 'barre' in low or 'graduation' in low or 'échelle' in low:return 'Lire la valeur d’un intervalle avant de placer ou de lire une hauteur.'
  if 'total' in low or 'en tout' in low:return 'Additionner les effectifs des groupes sans compter une personne deux fois.'
  if 'écart' in low or 'en plus' in low:return 'Comparer les deux nombres puis soustraire le plus petit du plus grand.'
 return METHODES[n]
ALT={
'quadrilateres':'Trois quadrilatères A, B et C sans codage de reconnaissance.',
'polygones':'Un pentagone P et un hexagone H dont les sommets sont visibles.',
'angles':'Trois ouvertures d’angles nommées A, B et C sans code révélateur.',
'diagonales':'Rectangle ABCD dont les sommets sont nommés dans l’ordre du contour.',
'cercle_disque':'À gauche un contour circulaire et à droite une surface ronde colorée.',
'triangle_corrige':'Triangle ABC rectangle en A avec AB de 4 cm et AC de 3 cm.',
'diagonales_corrige':'Rectangle ABCD avec ses deux diagonales AC et BD tracées en vert.',
'rectangle':'Modèle du rectangle ABCD de longueur 7 cm et de largeur 3 cm.',
'carre':'Modèle du carré ABCD de côté 5 cm avec ses quatre angles droits.',
'triangle':'Modèle d’un triangle ABC rectangle en A, avec AB de 6 cm et AC de 4 cm.',
'milieu':'Segment AB de 8 cm partagé par son milieu M en deux parties de 4 cm.',
'cercle':'Cercle de centre O avec un rayon OA de longueur 3 cm.',
'diametre':'Cercle de centre O traversé par un diamètre AB de 6 cm.',
'assemblage':'Carré de côté 4 cm et cercle de rayon 3 cm centré sur son sommet A.',
'quadrillage':'Modèle oblique ABCD sur quadrillage et quadrillage vide avec point de départ A.',
'solides':'Six solides A à F disposés en trois rangées de deux objets.',
'cube_cache':'Cube à huit sommets marqués et trois arêtes cachées en pointillés.',
'pyramides':'Pyramide à base triangulaire et pyramide à base carrée avec leurs sommets.',
'patrons':'Deux assemblages manipulables de six carrés : une croix A et une bande B.',
'sym_v':'Ligne brisée ABCD à gauche d’un axe vertical sur quadrillage.',
'sym_v_corrige':'Ligne brisée et son report en vert autour d’un axe vertical sur quadrillage.',
'sym_h':'Ligne brisée ABCD au-dessus d’un axe horizontal sur quadrillage.',
'sym_h_corrige':'Ligne brisée et son report en vert autour d’un axe horizontal sur quadrillage.',
'sans_axe':'Quadrilatère penché à reproduire pour essayer des plis avec du calque.',
'axes':'Rectangle avec deux axes et carré avec quatre axes de symétrie.',
'trajets':'Diagramme des trajets à pied, à vélo et en bus gradué de cinq élèves en cinq élèves.',
'fratrie':'Diagramme des effectifs 3, 5, 3 et 1 pour les nombres de frères et sœurs 0, 1, 2 et 3.',
'echelle':'Diagramme de trois groupes de 20, 40 et 60 personnes gradué de dix en dix.'}
if __name__=='__main__':writeall()
