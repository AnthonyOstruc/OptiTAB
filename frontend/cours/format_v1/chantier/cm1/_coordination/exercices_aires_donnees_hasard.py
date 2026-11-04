from commun_redaction import *
def aires(t,k):
 if k==0:
  whole=6+2*t;halves=4+2*t;a=whole+halves//2;b=a-1
  return ex(f'Paver et comparer — mosaïque {t+1}',f'Une surface A contient {whole} carreaux entiers et {halves} demi-carreaux. Une surface B couvre {b} carreaux entiers du même quadrillage.',[
   q('Combien de carreaux entiers peut-on former avec les demi-carreaux de A ?','Associer les demi-carreaux deux par deux.',eq(f'{halves}\\div2',halves//2),f'{halves//2} carreaux entiers.'),
   q('Quelle est l’aire de A en carreaux ?','Ajouter les parties sans trou ni superposition.',eq(f'{whole}+{halves//2}',a),f'{a} carreaux.'),
   q('Quelle surface a la plus grande aire ?','Comparer avec la même unité.',f'{a}>{b} : la surface A couvre davantage de carreaux.','La surface A a la plus grande aire.'),
   q('De combien de carreaux les aires diffèrent-elles ?','Soustraire les deux mesures.',eq(f'{a}-{b}',1),'Les aires diffèrent de 1 carreau.'),
   q('Si chaque carreau est un carré de 1 cm de côté, comment exprimer l’aire de A ?','Nommer l’unité carrée.','Un carré de 1 cm de côté a une aire de 1 centimètre carré, noté cm².',f'L’aire de A est {a} cm².')])
 if k==1:
  L=4+t;w=3;cut=2;outer=L*w;area=outer-cut
  return ex(f'Une surface en L — découpage {t+1}',f'Un rectangle quadrillé contient {w} rangées de {L} carreaux. On enlève deux carreaux voisins dans son coin supérieur droit.\n\n[IMAGE_1]',[
   q('Combien de carreaux contient chaque rangée avant la découpe ?','Lire le nombre de colonnes.',f'Chaque rangée traverse les {L} colonnes du rectangle.',f'{L} carreaux.'),
   q('Quelle est l’aire du rectangle avant la découpe ?','Compter les rangées identiques.',eq(f'3\\times{L}',outer),f'{outer} carreaux.'),
   q('Quelle est l’aire de la surface en L restante ?','Enlever les carreaux découpés.',eq(f'{outer}-2',area),f'{area} carreaux.'),
   q('On déplace les deux carreaux découpés et on les recolle ailleurs sans chevauchement. Quelle est l’aire totale reconstituée ?','Le déplacement ne change pas la surface des morceaux.',eq(f'{area}+2',outer),f'{outer} carreaux.'),
   q('Le contour peut-il changer quand l’aire est conservée ?','Distinguer bord et surface.','Les mêmes carreaux peuvent être disposés en bloc compact ou en longue bande. Le nombre de carreaux reste identique, mais le bord extérieur peut changer.','Oui : conserver l’aire n’impose pas de conserver le périmètre.')],figures={'1':f'surface_l_{t}.png'})
 if k==2:
  a=2+t;big=2*a;small=a*a;large=big*big;strips=2*small
  return ex(f'Doubler un côté — pavage {t+1}',f'Un petit carré a {a} carreaux de côté. Un grand carré a un côté deux fois plus long. On compte les carreaux, sans formule à apprendre.',[
   q('Combien de carreaux y a-t-il sur un côté du grand carré ?','Doubler la longueur.',eq(f'2\\times{a}',big),f'{big} carreaux de côté.'),
   q('Quelle est l’aire du petit carré ?','Compter les rangées de carreaux.',eq(f'{a}\\times{a}',small),f'{small} carreaux.'),
   q('Quelle est l’aire du grand carré ?','Compter ses rangées.',eq(f'{big}\\times{big}',large),f'{large} carreaux.'),
   q('L’aire du grand carré est-elle seulement le double de la petite ?','Comparer avec le double de la petite aire.',f'Le double serait {2*small} carreaux ; le grand carré en couvre {large}. Il contient quatre petits carrés.',f'Non : l’aire est multipliée par 4, pas par 2.'),
   q(f'Une frise contient {2*small} triangles, chacun valant un demi-carreau. Quelle est son aire ?','Assembler les triangles par paires.',eq(f'{2*small}\\div2',small),f'La frise couvre {small} carreaux, comme le petit carré.')])
 if k==3:
  # The same comparison diagram is a reference; angle labels explicitly match it.
  name=['ABC','MNP','RST'][t];center=name[1];A=name[0];C=name[2]
  return ex(f'Nommer et comparer les ouvertures — calque {t+1}',f'On observe trois angles A, B et C sur le schéma : A est plus fermé que l’angle droit ; B est droit ; C est plus ouvert. On dessine séparément un angle nommé ${chr(92)}widehat{{{name}}}$.\n\n[IMAGE_1]',[
   q(f'Quel est le sommet de l’angle ${chr(92)}widehat{{{name}}}$ ?','Lire la lettre du milieu.',f'Le nom de l’angle place son sommet entre les deux autres lettres.',f'Le sommet est {center}.'),
   q('Ranger les angles A, B et C du plus petit au plus grand.','Comparer les ouvertures avec un calque.','A est moins ouvert que l’angle droit B ; C est plus ouvert que B.','A, puis B, puis C.'),
   q('Quel instrument permet de vérifier que B est droit ?','Utiliser le coin droit de l’outil.','On place le sommet de l’équerre sur celui de B et on aligne un côté : l’autre côté doit coïncider.','Une équerre.'),
   q('Si on prolonge les côtés de A, son angle devient-il plus grand ?','Distinguer longueur des côtés et ouverture.','Le sommet et les directions restent les mêmes ; seule la longueur du dessin augmente.','Non : l’ouverture de A ne change pas.'),
   q('Comment transporter un angle pour le comparer à un autre ?','Superposer le sommet et un côté.','Décalquer le sommet et les deux côtés ; placer ensuite le sommet du calque sur le nouveau sommet et aligner un premier côté. Comparer alors les seconds côtés.','On utilise un calque en superposant les sommets et un côté.')],figures={'1':'angles_comparaison.png'})
 L=8+2*t;w=1;side=3+t;p=2*(L+w);squarep=4*side;area=L;sa=side*side
 return ex(f'Le tour ne mesure pas l’aire — débat {t+1}',f'Une bande rectangulaire mesure {L} cm sur 1 cm. Un carré mesure {side} cm de côté. Chaque centimètre carré peut être pavé par un carré de 1 cm de côté.',[
  q('Calculer le périmètre de la bande en additionnant les côtés.','Faire le tour de la bande.',eq(f'{L}+1+{L}+1',p),f'{p} cm.'),
  q('Calculer le périmètre du carré.','Additionner quatre côtés égaux.',eq(f'{side}+{side}+{side}+{side}',squarep),f'{squarep} cm.'),
  q('Déterminer les deux aires en comptant les carrés unités.','Compter les rangées.',[f'La bande a une rangée de {L} carrés.',eq(f'{side}\\times{side}',sa)],f'Bande : {area} cm² ; carré : {sa} cm².'),
  q('La figure de plus grand périmètre a-t-elle ici la plus grande aire ?','Comparer séparément les deux grandeurs.',f'{p}>{squarep}, mais {area}<{sa}. La bande a un plus long contour et une plus petite aire.','Non : le contour et la surface peuvent varier différemment.'),
  q('Comment vérifier cette comparaison sans formule d’aire ?','Utiliser un pavage ou un découpage.','Dessiner les deux figures sur un quadrillage de 1 cm de côté et compter les carrés recouverts ; pour le contour, compter les côtés de carreaux extérieurs.','En comptant les carrés à l’intérieur et les segments du contour séparément.')])

def donnees(t,k):
 if k==0:
  v=[7+2*t,9+2*t,5+2*t,4+2*t];total=sum(v)
  intro=table(['Fruit','Élèves'],zip(['Pomme','Fraise','Cerise','Banane'],v))+'\n\nDans cette enquête fictive, chaque élève choisit un seul fruit.'
  return ex(f'Lire une enquête — classe {t+1}',intro,[
   q('Combien d’élèves choisissent la fraise ?','Croiser la ligne du fruit et la colonne de l’effectif.',f'La ligne Fraise indique {v[1]}.',f'{v[1]} élèves.'),
   q('Combien d’élèves ont répondu ?','Additionner les effectifs.',eq('+'.join(map(str,v)),total),f'{total} élèves.'),
   q('Quel fruit est le plus choisi ?','Chercher le plus grand effectif.',f'{v[1]} est supérieur aux trois autres effectifs.','La fraise.'),
   q('Combien d’élèves de plus choisissent la fraise plutôt que la pomme ?','Soustraire les effectifs.',eq(f'{v[1]}-{v[0]}',2),'2 élèves de plus.'),
   q('La fraise est-elle choisie par plus de la moitié des élèves ?','Comparer le double de son effectif au total.',f'Deux groupes de {v[1]} donnent {2*v[1]}, moins que le total {total}. La fraise ne représente donc pas plus de la moitié.','Non : le choix le plus fréquent n’est pas forcément majoritaire.')])
 if k==1:
  a,b,c,e=17+t,8+t,14+t,12+t;tot=a+b+c+e
  return ex(f'Le tableau des menus — service {t+1}',table(['Classe','Menu A','Menu B'],[['CM1',a,b],['CM2',c,e]]),[
   q('Combien de CM2 choisissent le menu A ?','Croiser la ligne CM2 et la colonne Menu A.',f'À leur intersection, on lit {c}.',f'{c} élèves.'),
   q('Combien d’élèves choisissent le menu B au total ?','Additionner une colonne.',eq(f'{b}+{e}',b+e),f'{b+e} élèves.'),
   q('Combien d’élèves de CM1 ont répondu ?','Additionner la ligne CM1.',eq(f'{a}+{b}',a+b),f'{a+b} élèves.'),
   q('Combien d’élèves ont répondu dans les deux classes ?','Additionner les quatre cases une seule fois.',eq(f'{a}+{b}+{c}+{e}',tot),f'{tot} élèves.'),
   q('Le menu A est-il plus choisi que le menu B ?','Calculer puis comparer les totaux des colonnes.',[eq(f'{a}+{c}',a+c),f'{a+c}>{b+e}.'],'Oui, le menu A est plus choisi.')])
 if k==2:
  v=[4+2*t,8+2*t,6+2*t];wrong=v[1]+2
  return ex(f'Lire et corriger des barres — bibliothèque {t+1}',f'Le diagramme présente des prêts fictifs le lundi, mardi et mercredi.\n\n[IMAGE_1]',[
   q('Quelle grandeur est représentée et quelle est la valeur d’un intervalle vertical ?','Lire le titre et les graduations.','L’axe vertical compte les livres prêtés ; deux graduations successives diffèrent de 2.','Le nombre de prêts ; 2 prêts par intervalle.'),
   q('Combien de livres ont été prêtés le mardi ?','Lire la hauteur de la barre de mardi.',f'La barre de mardi atteint {v[1]}.',f'{v[1]} livres.'),
   q('Combien de livres ont été prêtés sur les trois jours ?','Additionner les hauteurs.',eq('+'.join(map(str,v)),sum(v)),f'{sum(v)} livres.'),
   q('Quel est l’écart entre mardi et lundi ?','Soustraire leurs effectifs.',eq(f'{v[1]}-{v[0]}',4),'4 livres.'),
   q(f'Une copie du diagramme place mardi à {wrong}. Comment la corriger ?','Comparer avec la valeur du diagramme de référence.',f'La copie montre {wrong} au lieu de {v[1]} : elle ajoute 2 prêts de trop.',f'Il faut abaisser la barre de mardi à {v[1]}.')],figures={'1':f'barres_{t}.png'})
 if k==3:
  v=[6+2*t,10+2*t,12+2*t,18+2*t]
  return ex(f'Une plante suivie chaque semaine — culture {t+1}',f'La courbe décrit la plante {chr(65+t)}. Ses hauteurs fictives, en centimètres, sont mesurées une fois par semaine.\n\n[IMAGE_1]',[
   q('Que représentent les deux axes ?','Lire les libellés du repère.','L’axe horizontal repère les semaines ; l’axe vertical indique la hauteur en centimètres.','Horizontal : semaine ; vertical : hauteur en cm.'),
   q('Quelle est la hauteur à la semaine 3 ?','Partir de 3 et rejoindre le point.',f'Le point de la semaine 3 est à la hauteur {v[2]}.',f'{v[2]} cm.'),
   q('De combien la plante a-t-elle grandi entre les semaines 1 et 4 ?','Soustraire la hauteur initiale de la finale.',eq(f'{v[3]}-{v[0]}',12),'Elle a grandi de 12 cm.'),
   q('Entre quelles semaines la croissance est-elle la plus forte ?','Comparer les écarts entre mesures successives.',[eq(f'{v[1]}-{v[0]}',4),eq(f'{v[2]}-{v[1]}',2),eq(f'{v[3]}-{v[2]}',6)],'Entre les semaines 3 et 4 : 6 cm.'),
   q('Peut-on lire avec certitude la hauteur exacte de chaque jour ?','Distinguer mesures et ligne reliant les points.','Les données ont été recueillies une fois par semaine. Les valeurs des jours intermédiaires ne sont pas mesurées.','Non : seules les hauteurs des semaines mesurées sont connues.')],figures={'1':f'courbe_{t}.png'})
 replies=['pied','vélo','pied','bus','vélo','pied','bus','pied','vélo','pied']+['bus']*t
 counts=[replies.count(x) for x in ['pied','vélo','bus']];total=len(replies);rain=[45+5*t,78+5*t,96+5*t,60+5*t]
 return ex(f'Organiser puis interpréter — collecte {t+1}',f'Réponses fictives sur le trajet vers l’école : '+', '.join(replies)+'.\n\n'+table(['Mois','Pluie fictive (mm)'],zip(['Septembre','Octobre','Novembre','Décembre'],rain)),[
  q('Donner les effectifs des trois moyens de transport.','Compter chaque réponse une seule fois.',f'On regroupe les réponses identiques : pied {counts[0]}, vélo {counts[1]}, bus {counts[2]}.',f'À pied : {counts[0]} ; vélo : {counts[1]} ; bus : {counts[2]}.'),
  q('Vérifier le nombre total de réponses.','Additionner les effectifs et comparer avec la liste.',eq('+'.join(map(str,counts)),total),f'{total} réponses.'),
  q('Quel mois est le plus pluvieux ?','Chercher la valeur maximale dans le tableau.',f'{rain[2]} mm est la plus grande valeur.','Novembre.'),
  q('Quel est le total de pluie des quatre mois ?','Additionner des mesures de même unité.',eq('+'.join(map(str,rain)),sum(rain)),f'{sum(rain)} mm.'),
  q('Novembre reçoit-il davantage de pluie que septembre et décembre réunis ?','Comparer avec la somme des deux mois.',[eq(f'{rain[0]}+{rain[3]}',rain[0]+rain[3]),f'{rain[2]}<{rain[0]+rain[3]}.'],'Non, septembre et décembre réunis reçoivent davantage.')])

def hasard(t,k):
 if k==0:
  value=[2,3,6][t];fav=[2,4,6]
  return ex(f'Le dé équilibré — observation {t+1}',f'On lance un dé équilibré dont les faces portent les numéros 1 à 6. On compare « obtenir {value} » et « obtenir un nombre pair ».',[
   q('Pourquoi cette expérience est-elle aléatoire ?','Chercher si le résultat peut être prévu avec certitude.','Avant le lancer, on ne sait pas quelle face apparaîtra, même si on connaît tous les résultats possibles.','Le résultat exact ne peut pas être prévu avec certitude.'),
   q('Lister tous les résultats possibles.','Recenser les faces sans oubli.','Les six faces sont numérotées de 1 à 6.','1, 2, 3, 4, 5 et 6.'),
   q('Obtenir 7 est-il impossible, possible ou certain ?','Vérifier si 7 figure parmi les faces.','Aucune face ne porte 7.','C’est impossible.'),
   q('Obtenir un nombre pair a-t-il une chance sur deux de se réaliser ?','Comparer les résultats pairs et impairs.','Pairs : 2, 4, 6 ; impairs : 1, 3, 5. Les deux groupes comptent trois faces également possibles.','Oui, il y a autant de faces paires que de faces impaires.'),
   q(f'Quel évènement est le plus probable : obtenir {value} ou un nombre pair ?','Comparer les nombres de faces favorables.','Une seule face donne le nombre demandé ; trois faces donnent un nombre pair. Toutes les faces ont la même chance.','Obtenir un nombre pair est plus probable.')])
 if k==1:
  red=1+t;blue=3+t;total=red+blue
  red_text=f'{red} jeton rouge' if red==1 else f'{red} jetons rouges'
  return ex(f'Le sac aux deux couleurs — tirage {t+1}',f'Un sac contient {red_text} et {blue} jetons bleus, identiques au toucher. On tire un seul jeton sans regarder.',[
   q('Quelles couleurs peut-on obtenir ?','Recenser les couleurs présentes.','Le sac contient seulement des jetons rouges et bleus.','Rouge ou bleu.'),
   q('Combien de jetons contient le sac ?','Additionner les deux collections.',eq(f'{red}+{blue}',total),f'{total} jetons.'),
   q('Le rouge et le bleu ont-ils la même chance de sortir ?','Compter les jetons de chaque couleur.',f'Il y a {blue} jetons bleus contre {red} rouges. Les jetons sont également susceptibles d’être tirés.','Non : le bleu est plus probable.'),
   q('Tirer un rouge est-il peu probable ou probable ?','Comparer le nombre de rouges au nombre des autres jetons.',f'{red}<{blue} : il est plus facile de ne pas tirer rouge que de tirer rouge.','Tirer un rouge est peu probable.'),
   q('Comment modifier le sac pour que les deux couleurs aient la même chance ?','Égaliser les effectifs.',eq(f'{blue}-{red}',2),'Ajouter 2 jetons rouges pour égaliser les deux couleurs.')])
 if k==2:
  # Equal-likelihood classic cards and coin, no numerical probability notation.
  suit=['cœur','carreau','trèfle'][t];black=suit=='trèfle'
  return ex(f'Pièce et jeu de cartes — comparaison {t+1}',f'On utilise une pièce équilibrée et un jeu de 32 cartes bien mélangé. Le jeu contient 8 cœurs, 8 carreaux, 8 trèfles et 8 piques. On tire une carte au hasard.',[
   q('Quels sont les deux résultats possibles du lancer de pièce ?','Nommer les deux faces.','La pièce peut retomber sur pile ou sur face.','Pile et face.'),
   q('Obtenir pile a-t-il une chance sur deux de se réaliser ?','Utiliser le caractère équilibré de la pièce.','Les deux faces ont la même chance ; il n’y a pas de troisième résultat dans ce modèle.','Oui, pile a une chance sur deux.'),
   q('Combien de cartes rouges contient le jeu ?','Regrouper cœurs et carreaux.',eq('8+8',16),'16 cartes rouges.'),
   q('Tirer une carte rouge a-t-il une chance sur deux de se réaliser ?','Comparer cartes rouges et noires.','Il y a 16 rouges et 16 noires, également susceptibles d’être tirées.','Oui, les deux groupes sont de même taille.'),
   q(f'Est-il plus probable de tirer un {suit} ou une carte rouge ?','Comparer les effectifs des groupes de cartes.',f'Le groupe {suit} contient 8 cartes ; le groupe rouge en contient 16.','Tirer une carte rouge est plus probable.')])
 if k==3:
  lost=4-t;bonbon=3;toy=1+t
  return ex(f'La roue de la fête — jeu {t+1}',f'Une roue équilibrée comporte 8 secteurs de même taille : {lost} « perdu », {bonbon} « bonbon » et {toy} « peluche ». Le schéma représente exactement cette roue.\n\n[IMAGE_1]',[
   q('Pourquoi les huit secteurs ont-ils la même chance d’être désignés ?','Utiliser la forme de la roue et son équilibre.','Les secteurs ont la même ouverture et le mécanisme est équilibré. Aucun secteur n’est favorisé.','Ils ont la même taille et la roue est équilibrée.'),
   q('Quels sont les trois résultats annoncés au joueur ?','Regrouper les secteurs par inscription.','Plusieurs secteurs peuvent porter la même inscription.','Perdu, bonbon ou peluche.'),
   q('Combien de secteurs permettent de gagner un lot ?','Regrouper bonbons et peluches.',eq(f'{bonbon}+{toy}',bonbon+toy),f'{bonbon+toy} secteurs.'),
   q('Gagner un lot a-t-il moins, autant ou plus d’une chance sur deux ?','Comparer secteurs gagnants et perdants.',f'Il y a {bonbon+toy} secteurs gagnants et {lost} perdants.',('Autant : une chance sur deux.' if lost==4 else 'Plus d’une chance sur deux.')),
   q('Une roue aux secteurs inégaux donnerait-elle automatiquement la même chance à chaque inscription ?','Distinguer nombre de résultats et taille des secteurs.','Un grand secteur occupe plus de place qu’un petit : compter seulement les inscriptions ne suffit pas pour comparer les chances.','Non : il faut aussi tenir compte de la taille des secteurs.')],figures={'1':f'roue_{t}.png'})
 winners=10+5*t;tickets=500;non=tickets-winners
 return ex(f'Gagner n’est pas une garantie — tombola {t+1}',f'Une tombola comporte {tickets} billets, dont {winners} gagnants. Les billets sont mélangés et un billet est tiré au hasard.',[
  q('Quels sont les deux résultats possibles pour le billet tiré ?','Décrire le résultat utile au joueur.','Le billet peut appartenir au groupe des gagnants ou à celui des perdants.','Gagner ou perdre.'),
  q('Combien de billets sont perdants ?','Retirer les gagnants du total.',eq(f'{tickets}-{winners}',non),f'{non} billets.'),
  q('A-t-on une chance sur deux de gagner parce qu’on peut gagner ou perdre ?','Comparer les effectifs des deux groupes.',f'Il y a {winners} billets gagnants et {non} perdants : les deux groupes n’ont pas la même taille.','Non : deux résultats possibles ne signifient pas deux chances égales.'),
  q('Gagner est-il impossible, peu probable, probable ou certain ?','Vérifier s’il existe des gagnants et les comparer aux perdants.',f'Des billets gagnants existent, mais ils sont bien moins nombreux que les perdants.','Gagner est possible et peu probable.'),
  q('Après plusieurs résultats identiques avec un dé, peut-on affirmer avec certitude le prochain résultat ?','Distinguer observation et garantie.','Un dé équilibré peut encore donner n’importe laquelle de ses faces. Une série observée ne rend pas un résultat obligatoire ou impossible.','Non : le prochain résultat reste incertain.')])

if __name__=='__main__':
 for code,fun in [(13,aires),(20,donnees),(21,hasard)]:write(code,[fun(t,k) for t in range(3) for k in range(5)])
