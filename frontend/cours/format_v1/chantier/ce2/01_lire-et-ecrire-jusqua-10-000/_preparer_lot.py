"""Préparation éditoriale du lot attribué, sans compilation ni accès au site."""
from pathlib import Path
import ast,json,re,operator,datetime
from fractions import Fraction as F
BASE=Path(__file__).resolve().parent.parent
CODES=[1,2,3,15,16,17,18,19,20,21,22,23]
def fmt(n):
 if isinstance(n,F):return str(n.numerator) if n.denominator==1 else f'{n.numerator}/{n.denominator}'
 return f'{n:,}'.replace(',',' ')
def fr(s):return re.sub(r'(?<![\w\\])(\d+)/(\d+)(?!\w)',lambda m:r'$\dfrac{'+m[1]+'}{'+m[2]+'}$',s)
def block(t,s,title=''):return '::: '+t+(' '+title if title else '')+'\n'+s+'\n:::\n'
def item(q,why,a,check=''):return dict(q=q,why=why,a=a,check=check)
def rows(s):
 out=[]
 for line in s.strip().splitlines():
  q,why,a,*ch=line.split('|');out.append(item(q,why,a,ch[0] if ch else ''))
 return out
EX={}
EX[1]=[
'''Quel chiffre indique les milliers ? Quelle est sa valeur ?|Dans le tableau, la colonne des milliers est la première à gauche.|4 ; il vaut 4 000.|4*1000==4000
À quel rang le zéro se trouve-t-il ?|On lit les colonnes dans l’ordre : milliers, centaines, dizaines, unités.|Au rang des dizaines : aucune dizaine isolée.
Décompose ce nombre en somme.|Chaque chiffre donne une quantité de son rang.|4 205 = 4 000 + 200 + 5.|4000+200+5==4205
Écris le nombre obtenu en ajoutant une dizaine.|Une dizaine vaut 10 unités ; on ajoute 10 au nombre du tableau.|4 215.|4205+10==4215''',
'''Quel est le chiffre des centaines de 1 060 ?|Dans 1 060, les rangs sont 1 millier, 0 centaine, 6 dizaines et 0 unité.|0.
Décompose 7 008.|Le zéro conserve les rangs des centaines et des dizaines.|7 008 = 7 000 + 8.|7000+8==7008
Écris en lettres le nombre juste après 9 120.|Le nombre suivant s’obtient en ajoutant une unité.|9 121 : neuf-mille-cent-vingt-et-un.|9120+1==9121
Écris en chiffres « sept-mille-quatre-vingts ».|Sept milliers font 7 000 ; quatre-vingts fait 80.|7 080.|7000+80==7080''',
'''Décompose 2 480 par rangs.|On sépare les milliers, les centaines et les dizaines.|2 480 = 2 000 + 400 + 80.|2000+400+80==2480
Dans 6 003, explique les deux zéros.|Les centaines et les dizaines sont absentes ; les unités restent au bon rang.|0 centaine et 0 dizaine isolées.
Écris en chiffres « six-mille-trente ».|Trente contient 3 dizaines et aucune unité.|6 030.|6000+30==6030
Écris en lettres le nombre formé de 2 milliers, 4 centaines et 8 unités.|On place un zéro aux dizaines.|2 408 : deux-mille-quatre-cent-huit.|2000+400+8==2408''',
'''Quelle est la valeur du chiffre 6 ?|Le dernier chiffre est celui des unités.|6 unités.
Décompose 5 726.|Chaque rang garde sa valeur.|5 726 = 5 000 + 700 + 20 + 6.|5000+700+20+6==5726
Écris le nombre obtenu en échangeant les chiffres des centaines et des dizaines.|Le 2 devient le chiffre des centaines ; le 7 devient celui des dizaines.|5 276.|5000+200+70+6==5276
Quel nombre obtient-on en ajoutant 1 centaine à 5 726 ?|Une centaine vaut 100 unités.|5 826.|5726+100==5826''',
'''Pourquoi faut-il écrire un zéro ?|Les milliers et les dizaines ne doivent pas devenir voisins dans l’écriture : le rang des centaines est vide.|Le zéro garde le rang des centaines.
Écris ce nombre en lettres.|On lit les milliers puis quarante-neuf.|huit-mille-quarante-neuf.
Décompose ce nombre.|8 milliers valent 8 000 et 4 dizaines valent 40.|8 049 = 8 000 + 40 + 9.|8000+40+9==8049
Remplace les 4 dizaines par 4 centaines. Quel nombre obtiens-tu ?|Les dizaines deviennent nulles ; on conserve 8 milliers et 9 unités.|8 409.|8000+400+9==8409''',
'''Quel est le nombre juste avant 3 998 ?|On retire une unité.|3 997.|3998-1==3997
Quel échange permet de passer de 3 999 à 4 000 ?|L’ajout d’une unité déclenche les échanges de dix en dix.|10 unités deviennent 1 dizaine, puis 10 dizaines 1 centaine, puis 10 centaines 1 millier.
Écris 4 002 en lettres.|Les centaines et les dizaines sont nulles.|quatre-mille-deux.
Continue la même suite encore deux nombres.|La suite avance d’une unité à chaque fois.|4 003 ; 4 004.|4002+1==4003 and 4003+1==4004''',
'''Quelle quantité représente le chiffre 2 dans 1 208 ?|Le chiffre 2 est dans le rang des centaines.|200 livres.|2*100==200
À quel rang le zéro se trouve-t-il ?|On sépare 1 millier, 2 centaines, 0 dizaine et 8 unités.|Au rang des dizaines.
L’école reçoit une dizaine de livres. Combien en a-t-elle ?|Une dizaine de livres représente 10 livres.|1 218 livres.|1208+10==1218
Écris ce nouveau total en lettres.|On lit 1 millier, 2 centaines et dix-huit.|mille-deux-cent-dix-huit.''',
'''Pourquoi ne peut-on pas commencer par zéro ?|Un zéro placé devant 258 ne crée pas de millier.|0258 représente 258 : ce n’est pas un nombre à quatre chiffres.
Écris le plus grand nombre possible avec ces quatre chiffres.|On place les chiffres du plus grand au plus petit.|8 520.|8000+500+20==8520
Écris en lettres le plus petit nombre trouvé.|On lit 2 milliers puis cinquante-huit.|deux-mille-cinquante-huit.
Trouve un autre nombre de quatre chiffres qui commence par 2.|On garde le 2 et on permute les trois autres chiffres sans en répéter.|Par exemple 2 085.|2000+80+5==2085''',
'''Décompose le nombre erroné 6 304.|Le chiffre 3 occupe le rang des centaines.|6 304 = 6 000 + 300 + 4.|6000+300+4==6304
Écris en lettres 6 304.|On lit trois-cents et non trente.|six-mille-trois-cent-quatre.
Donne la valeur du 3 dans le nombre corrigé.|Dans 6 034, le 3 occupe le rang des dizaines.|30.|3*10==30
Écris en chiffres « six-mille-trois-cent-quarante ».|On place 6 milliers, 3 centaines, 4 dizaines et 0 unité.|6 340.|6000+300+40==6340''']
EX[2]=[
'''Combien de centaines peut-on échanger contre un millier ?|La numération fonctionne par groupes de dix.|10 centaines.|10*100==1000
Échange les 16 unités ; que reste-t-il au rang des unités ?|16 unités donnent 1 dizaine et 6 unités ; la nouvelle dizaine rejoint les 4 dizaines.|6 unités et 5 dizaines.|16==10+6
Donne la décomposition habituelle du total.|Les 12 centaines deviennent 1 millier et 2 centaines.|4 256 = 4 000 + 200 + 50 + 6.|4000+200+50+6==4256
Combien de dizaines entières contient ce total ?|4 250 unités forment 425 dizaines ; 6 unités restent isolées.|425 dizaines et 6 unités.|425*10+6==4256''',
'''Quel chiffre garde le rang vide ?|6 082 ne contient aucune centaine isolée.|Le zéro des centaines.
Combien de dizaines entières contient 6 082 ?|6 080 unités forment des dizaines ; les 2 dernières unités restent.|608 dizaines et 2 unités.|608*10+2==6082
Combien de centaines entières contient 6 082 ?|6 000 unités se regroupent en centaines ; 82 unités restent.|60 centaines et 82 unités.|60*100+82==6082
Écris une autre décomposition en centaines, dizaines et unités.|On remplace les 6 milliers par 60 centaines.|60 centaines + 8 dizaines + 2 unités.|60*100+8*10+2==6082''',
'''Combien de milliers et de centaines isolées forment 47 centaines ?|40 centaines font 4 milliers ; il reste 7 centaines.|4 milliers et 7 centaines.|4*1000+7*100==4700
Combien de centaines et de dizaines isolées forment 235 dizaines ?|230 dizaines font 23 centaines ; il reste 5 dizaines.|23 centaines et 5 dizaines.|23*100+5*10==2350
Exprime 4 700 en dizaines.|Chaque centaine contient 10 dizaines.|470 dizaines.|470*10==4700
Exprime 2 350 en centaines entières et unités restantes.|On prend les 23 groupes complets de 100.|23 centaines et 50 unités.|23*100+50==2350''',
'''Quelle quantité représente le chiffre des centaines ?|Le 4 est au rang des centaines.|400 unités.|4*100==400
Combien d’unités restent après avoir groupé les centaines entières ?|74 centaines valent 7 400 ; on cherche ce qui manque pour 7 462.|62 unités.|7462-7400==62
Donne le nombre de dizaines entières.|On regroupe 7 460 unités par 10 et on laisse 2 unités.|746 dizaines et 2 unités.|746*10+2==7462
Noé dit « 74 est le chiffre des centaines ». Corrige.|Un chiffre s’écrit avec un seul signe ; 74 est un nombre de groupes.|Le chiffre est 4 ; le nombre de centaines entières est 74.''',
'''Quel rang est absent de 5 018 ?|Entre les milliers et les dizaines, il n’y a pas de centaine isolée.|Le rang des centaines est nul.
Combien de dizaines entières contient ce nombre ?|5 010 unités forment des dizaines ; 8 unités restent.|501 dizaines et 8 unités.|501*10+8==5018
Décompose 5 018 seulement en milliers et unités.|Les 18 dernières unités peuvent rester sans échange.|5 milliers et 18 unités.|5*1000+18==5018
Échange un millier contre des centaines. Donne une décomposition.|On retire 1 des 5 milliers et on ajoute 10 centaines.|4 milliers, 10 centaines, 1 dizaine et 8 unités.|4000+1000+10+8==5018''',
'''Combien d’unités vaut un millier ?|Un millier contient dix centaines de cent unités.|1 000 unités.|10*100==1000
Écris 8 000 comme une somme de deux quantités égales.|On partage les 8 milliers en deux groupes de 4.|4 000 + 4 000.|4000+4000==8000
Combien de centaines manque-t-il à 75 centaines pour faire 8 000 ?|Le total visé contient 80 centaines.|5 centaines.|80-75==5
Retire une dizaine à 8 000. Quel nombre obtiens-tu ?|On échange pour pouvoir retirer 10 unités.|7 990.|8000-10==7990''',
'''Combien de feuilles donnent 12 lots ?|Chaque lot contient 100 feuilles.|1 200 feuilles.|12*100==1200
Combien manque-t-il avec 12 lots ?|On compare les 1 260 feuilles nécessaires aux 1 200 disponibles.|60 feuilles.|1260-1200==60
Combien de feuilles resteront après l’achat de 13 lots et l’utilisation de 1 260 feuilles ?|13 lots donnent 1 300 feuilles ; on retire le besoin.|40 feuilles.|13*100-1260==40
Pour un besoin de 1 300 feuilles, combien de lots faut-il ?|13 lots suffisent exactement ; on n’ajoute pas un lot inutile.|13 lots.|13*100==1300''',
'''Échange 26 centaines en milliers et centaines isolées.|20 centaines font 2 milliers ; il reste 6 centaines.|2 milliers et 6 centaines.|2000+600==2600
Échange les 48 unités en dizaines et unités.|40 unités font 4 dizaines ; 8 unités restent.|4 dizaines et 8 unités.|4*10+8==48
Donne le chiffre des centaines du total.|On lit 2 milliers, 6 centaines, 4 dizaines et 8 unités.|6.
La réserve reçoit 2 centaines. Quelle quantité contient-elle ?|On ajoute 200 unités à 2 648.|2 848 unités.|2648+200==2848''',
'''Quelle quantité représentent les 4 centaines isolées ?|Le chiffre 4 vaut 4 groupes de 100.|400 unités.|4*100==400
Combien d’unités forment 34 centaines ?|Chaque centaine contient 100 unités.|3 400 unités.|34*100==3400
Combien de dizaines entières contient 3 405 ?|3 400 unités forment des dizaines ; 5 unités restent.|340 dizaines et 5 unités.|340*10+5==3405
Donne une décomposition avec 33 centaines.|33 centaines valent 3 300 ; il faut garder encore 105 unités.|33 centaines et 105 unités.|33*100+105==3405''']
EX[3]=[
'''Quel est le pas entre deux graduations voisines ?|De 3 000 à 3 100, on ajoute toujours la même quantité.|100.|3100-3000==100
Combien de pas séparent 3 000 de 3 500 ?|On compte les intervalles, et non les traits.|5 pas.|5*100==3500-3000
Quel nombre est à la graduation juste après 3 700 ?|On ajoute un pas de 100.|3 800.|3700+100==3800
Encadre 3 450 entre deux graduations voisines.|3 450 est entre 3 400 et 3 500.|3 400 < 3 450 < 3 500.|3400<3450<3500''',
'''Quel rang permet de comparer 4 098 et 4 108 ?|Les milliers sont égaux ; on regarde ensuite les centaines.|Les centaines : 0 est inférieur à 1.
Quel rang permet de comparer 7 060 et 7 006 ?|Les milliers et centaines sont égaux ; les dizaines diffèrent.|Les dizaines : 6 est supérieur à 0.
Écris le nombre juste avant 10 000.|On retire une unité et on effectue les échanges.|9 999.|10000-1==9999
Place 4 100 entre les deux nombres 4 098 et 4 108.|On compare successivement les centaines puis les dizaines et unités.|4 098 < 4 100 < 4 108.|4098<4100<4108''',
'''Quel nombre est le plus petit ?|5 milliers sont inférieurs à 6 milliers.|5 999.
Range les mêmes nombres dans l’ordre décroissant.|On reprend le rangement croissant en sens inverse.|6 300 > 6 243 > 6 239 > 6 234 > 5 999.|6300>6243>6239>6234>5999
Quel écart sépare 6 234 et 6 239 ?|On retire le plus petit du plus grand.|5.|6239-6234==5
Ajoute 6 240 au bon endroit entre deux nombres du rangement.|Les milliers et centaines sont égaux ; on compare les dizaines.|6 239 < 6 240 < 6 243.|6239<6240<6243''',
'''Encadre 3 786 entre deux centaines consécutives.|On garde 3 milliers et on cherche les centaines de part et d’autre.|3 700 < 3 786 < 3 800.|3700<3786<3800
Quel écart sépare 3 786 de la dizaine inférieure ?|On enlève les 3 780 unités déjà atteintes.|6.|3786-3780==6
Combien ajouter à 3 786 pour atteindre 3 790 ?|On complète les unités jusqu’à la prochaine dizaine.|4.|3790-3786==4
Encadre 3 790 entre les deux centaines consécutives qui l’entourent.|3 790 reste entre 3 700 et 3 800.|3 700 < 3 790 < 3 800.|3700<3790<3800''',
'''Quel est le pas de la suite ?|On calcule l’écart entre les deux premiers nombres.|10.|4980-4970==10
Quel nombre précède 4 970 dans cette suite ?|Pour reculer d’un pas, on retire 10.|4 960.|4970-10==4960
Quel échange explique le passage de 4 990 à 5 000 ?|La nouvelle dizaine complète les centaines, puis le millier.|10 dizaines forment 1 centaine ; 10 centaines forment 1 millier.
Poursuis de deux pas après 5 010.|On ajoute 10 deux fois.|5 020 ; 5 030.|5010+10==5020 and 5020+10==5030''',
'''Combien d’intervalles séparent 6 000 de 7 000 ?|La différence vaut 1 000 et chaque pas vaut 100.|10 intervalles.|10*100==7000-6000
Quel nombre est juste à gauche du point vert ?|On retire un pas de 100 à 6 500.|6 400.|6500-100==6400
Quel nombre est deux pas à droite du point vert ?|Deux pas valent 200.|6 700.|6500+2*100==6700
Le point vert est-il au milieu entre 6 000 et 7 000 ?|Les deux distances numériques doivent être égales.|Oui : 500 de chaque côté.|6500-6000==7000-6500==500''',
'''Donne tous les entiers strictement entre ces deux bornes.|On avance d’une unité, en excluant les bornes.|2 406 ; 2 407 ; 2 408 ; 2 409.|2405+1==2406 and 2410-1==2409
Combien y en a-t-il ?|On compte les quatre nombres de la liste.|4.
Pourquoi 2 410 ne convient-il pas ?|Strictement compris interdit d’utiliser une borne.|2 410 est la borne supérieure, pas un nombre intérieur.
Trouve un entier compris entre 2 407 et 2 409, bornes exclues.|Un seul entier se trouve au milieu.|2 408.|2407<2408<2409''',
'''Quel est le chiffre des unités avant et après l’avancée ?|Ajouter une dizaine conserve les unités.|5 dans les deux cas.
Combien manque-t-il à 8 995 pour atteindre 9 000 ?|On complète jusqu’au millier suivant.|5 unités.|9000-8995==5
Décris l’avancée en deux petits sauts.|On utilise 5 unités pour atteindre 9 000, puis les 5 restantes.|8 995 + 5 = 9 000 ; 9 000 + 5 = 9 005.|8995+5==9000 and 9000+5==9005
Le compteur avance encore de 10. Que lit-on ?|On ajoute une dizaine au résultat précédent.|9 015.|9005+10==9015''',
'''À quel rang se trouve le 7 de 4 700 ?|On lit 4 milliers puis 7 centaines.|Au rang des centaines ; il vaut 700.|7*100==700
À quel rang se trouve le 8 de 4 087 ?|Le zéro garde le rang des centaines.|Au rang des dizaines ; il vaut 80.|8*10==80
Quel est l’écart entre les deux nombres ?|On retire le plus petit du plus grand.|613.|4700-4087==613
Trouve un nombre strictement entre 4 087 et 4 700.|On peut choisir une centaine située après 4 087.|Par exemple 4 100.|4087<4100<4700''']

# Pour les problèmes, cinq tâches distinctes : comprendre, représenter,
# résoudre le problème-source, contrôler, puis transférer à une variante.
PROB={
15:[
('1 245 cahiers bleus et 876 rouges ; on cherche le total des cahiers.','Deux parties se réunissent : dessine une barre partagée en 1 245 et 876.','Vérifie le résultat en retirant les cahiers rouges du total.','2 121 - 876 = 1 245 cahiers bleus.','2121-876==1245','Il y a 100 cahiers bleus de plus. Quel est le nouveau total ?','2 221 cahiers.','2121+100==2221'),
('2 500 enveloppes au départ ; 675 sont retirées ; on cherche le reste.','Dessine le tout 2 500, une partie retirée 675 et une partie inconnue.','Vérifie en réunissant le reste et les enveloppes retirées.','1 825 + 675 = 2 500 enveloppes.','1825+675==2500','On retire 25 enveloppes de plus. Combien en reste-t-il ?','1 800 enveloppes.','1825-25==1800'),
('3 480 places au total ; 2 756 occupées ; on cherche les places libres.','Le tout se partage en places occupées et places libres : une soustraction convient.','Vérifie en réunissant places occupées et libres.','2 756 + 724 = 3 480 places.','2756+724==3480','100 personnes quittent leur place. Combien de places sont alors libres ?','824 places.','724+100==824'),
('2 130 feuilles après livraison ; 475 reçues ; on cherche le stock avant.','Une barre représente le stock avant, prolongée par 475 : le tout vaut 2 130.','Vérifie en rejouant la livraison.','1 655 + 475 = 2 130 feuilles.','1655+475==2130','Si la livraison avait contenu 100 feuilles de moins, à stock initial identique, quel serait le stock final ?','2 030 feuilles.','2130-100==2030'),
('268 billes données ; 457 restantes ; on cherche le nombre avant le don.','Le stock de départ est le tout : il réunit les billes données et restantes.','Vérifie en retirant le don du stock de départ.','725 - 268 = 457 billes.','725-268==457','Avec le même départ, Lina donne 300 billes. Combien lui en reste-t-il ?','425 billes.','725-300==425'),
('1 435 livres dans une école ; 1 680 dans l’autre ; on cherche leur écart.','Dessine deux barres alignées ; la partie qui dépasse représente l’écart.','Vérifie en ajoutant l’écart à la petite quantité.','1 435 + 245 = 1 680 livres.','1435+245==1680','La première école reçoit 100 livres. Quel devient l’écart ?','145 livres.','1680-(1435+100)==145'),
('Lina a 1 250 images ; elle a 375 images de plus que Noé ; on cherche la quantité de Noé.','La barre de Lina est la barre de Noé prolongée de 375 ; on retire cet écart.','Vérifie en reconstruisant la quantité de Lina.','875 + 375 = 1 250 images.','875+375==1250','Noé reçoit 100 images et Lina garde les siennes. Quel est le nouvel écart ?','275 images.','1250-(875+100)==275'),
('La petite gourde coûte 8,40 € ; l’autre coûte 1,25 € de plus.','La barre du prix le plus élevé prolonge celle de 8,40 € de 1,25 €.','Vérifie en retrouvant l’écart entre les prix.','9,65 € - 8,40 € = 1,25 €, soit 965 - 840 = 125 centimes.','965-840==125','Le prix de l’autre gourde baisse de 0,50 €. Quel est son nouveau prix ?','9,15 €, soit 915 centimes.','965-50==915'),
('On cherche la quantité de Noé, plus petite que celle de Lina : 95 cartes et 18 cartes d’écart.','La barre de Lina contient celle de Noé et un supplément de 18 ; il faut retirer 18.','Vérifie l’histoire proposée en retrouvant la quantité de Lina.','77 + 18 = 95 cartes.','77+18==95','Lina a maintenant 100 cartes, toujours 18 de plus que Noé. Combien Noé en a-t-il ?','82 cartes.','100-18==82')],
16:[
('Lina : 146 images ; Noé : 28 de plus ; on cherche le total des deux enfants.','Calcule d’abord la barre de Noé : 146 + 28 ; réunis ensuite les deux barres.','Pourquoi 174 ne répond-il pas à la question finale ?','174 est seulement la quantité de Noé ; il faut ajouter les 146 images de Lina.','146+28==174','Lina et Noé reçoivent chacun 10 images. Quel est leur nouveau total ?','340 images.','320+10+10==340'),
('Mila : 215 cartes ; elle en a 47 de plus que Sami ; on cherche le total.','Cherche Sami en retirant 47 à 215 ; ajoute ensuite les deux quantités.','Vérifie la quantité de Sami avec l’écart annoncé.','168 + 47 = 215 cartes.','168+47==215','Mila donne 10 cartes à Sami. Leur total change-t-il ?','Non : 383 cartes en tout ; le don déplace les cartes sans en ajouter.','(215-10)+(168+10)==383'),
('Départ : 2 450 feuilles ; livraison : 875 ; utilisation : 1 268.','Un premier saut ajoute 875 au stock ; un deuxième saut retire 1 268.','Vérifie le stock après la livraison à partir du reste.','2 057 + 1 268 = 3 325 feuilles.','2057+1268==3325','On utilise 100 feuilles de moins. Quel est le nouveau reste ?','2 157 feuilles.','2057+100==2157'),
('438 passagers au départ ; 125 descendent ; 87 montent.','Retire les 125 passagers descendus avant d’ajouter les 87 nouveaux.','Vérifie la quantité juste après la descente.','313 + 125 = 438 passagers.','313+125==438','10 passagers de plus montent. Combien sont alors dans le train ?','410 passagers.','400+10==410'),
('Ruban : 850 cm ; morceaux coupés : 175 cm et 248 cm ; on cherche le reste.','Réunis les deux morceaux retirés, puis enlève leur somme à 850 cm.','Vérifie en réunissant les morceaux et le reste.','175 + 248 + 427 = 850 cm.','175+248+427==850','On coupe ensuite 27 cm dans le reste. Quelle longueur reste-t-il ?','400 cm.','427-27==400'),
('Classe A : 178 livres ; classe B : 35 de moins ; on cherche le total.','Cherche B par 178 - 35 ; réunis ensuite A et B.','Vérifie que la classe B a bien 35 livres de moins.','178 - 143 = 35 livres.','178-143==35','Chaque classe reçoit 20 livres. Quel est le nouveau total ?','361 livres.','321+20+20==361'),
('Une boîte : 1 200 g ; l’autre : 250 g de plus ; on cherche la masse totale.','Prolonge une barre de 1 200 g de 250 g ; réunis ensuite les deux masses.','Vérifie l’écart entre les masses.','1 450 - 1 200 = 250 g.','1450-1200==250','On ajoute 100 g dans la petite boîte. Quelle est la nouvelle masse totale ?','2 750 g.','2650+100==2750'),
('Lina : 12,50 € ; Sami : 3,25 € de moins ; on cherche leur somme.','Retire 3,25 € au montant de Lina pour Sami, puis ajoute les deux sommes.','Vérifie la somme de Sami avec l’écart.','9,25 € + 3,25 € = 12,50 €, soit 925 + 325 = 1 250 centimes.','925+325==1250','Chacun dépense 1 €. Combien leur reste-t-il ensemble ?','19,75 €, soit 1 975 centimes.','2175-100-100==1975'),
('Lina a 128 cartes ; Noé en a 35 de plus ; le total doit compter les deux enfants.','La quantité de Noé vient de 128 + 35 ; le total doit encore inclure la barre de Lina.','Vérifie le total en retirant les cartes de Noé.','291 - 163 = 128 cartes de Lina.','291-163==128','Noé donne 5 cartes à Lina. Le total devient-il 296 ? Explique.','Non : il reste 291 cartes, car aucune carte n’est ajoutée.','(163-5)+(128+5)==291')],
17:[
('5 tables de 6 places et 4 tables de 4 places ; on cherche toutes les places.','Fais deux groupes de tables ; calcule chaque nombre de places avant de les réunir.','Vérifie séparément les places de chaque groupe.','5 × 6 = 30 et 4 × 4 = 16 ; 30 + 16 = 46 places.','5*6==30 and 4*4==16 and 30+16==46','On ajoute une table de 4 places. Quelle capacité obtient-on ?','50 places.','46+4==50'),
('6 albums à 8 € ; paiement de 50 € ; on cherche la monnaie.','Calcule le coût des 6 albums ; retire-le ensuite des 50 € donnés.','Vérifie que prix et monnaie recomposent le paiement.','48 € + 2 € = 50 €.','48+2==50','On achète 5 albums au même prix et on donne 50 €. Quelle monnaie reçoit-on ?','10 €.','50-5*8==10'),
('3 boîtes de 12 feutres ; 4 groupes égaux ; on cherche la part de chaque groupe.','Réunis d’abord les boîtes, puis partage le total en 4 parts égales.','Vérifie le partage avec une multiplication.','4 × 9 = 36 feutres.','4*9==36','On partage ces 36 feutres entre 6 groupes. Combien par groupe ?','6 feutres.','36//6==6'),
('7 paquets de 25 cartes ; 18 cartes isolées ; on cherche le total.','Calcule les cartes des paquets, puis ajoute les cartes isolées.','Vérifie en retirant les cartes isolées.','193 - 18 = 175 cartes, soit 7 paquets de 25.','193-18==7*25==175','Il y a 8 paquets au lieu de 7, avec 18 cartes isolées. Quel total ?','218 cartes.','8*25+18==218'),
('4 sacs de 9 pommes ; 12 pommes ajoutées ; 6 paniers égaux.','Cherche les pommes des sacs, ajoute 12, puis partage entre 6 paniers.','Vérifie que tous les paniers réunis redonnent le total.','6 × 8 = 48 pommes.','6*8==4*9+12==48','Si les 48 pommes sont partagées entre 8 paniers, combien par panier ?','6 pommes.','48//8==6'),
('3 tables de 8 places, 2 tables de 6 places et 5 places libres.','Calcule chaque groupe de places, réunis-les, puis retire les places libres.','Vérifie en ajoutant les places libres aux places occupées.','31 + 5 = 36 places.','31+5==36','Il reste seulement 2 places libres. Combien de personnes sont assises ?','34 personnes.','36-2==34'),
('4 carnets à 6 €, 3 stylos à 2 € et paiement de 40 €.','Calcule les deux achats, réunis leurs prix, puis retire la dépense du paiement.','Vérifie le montant payé avec la monnaie.','24 + 6 + 10 = 40 €.','24+6+10==40','On donne 50 € pour les mêmes achats. Quelle monnaie reçoit-on ?','20 €.','50-(4*6+3*2)==20'),
('72 images dans 8 pochettes égales ; 3 images ajoutées dans chaque pochette.','Cherche d’abord la part de 72 pour une pochette, puis ajoute 3 à cette part.','Vérifie le contenu d’une pochette avant l’ajout.','8 × 9 = 72 images.','8*9==72','On ajoute seulement 2 images par pochette au lieu de 3. Combien par pochette ?','11 images.','72//8+2==11'),
('24 crayons rouges et 18 bleus ; 6 abîmés ; 4 enfants se partagent les autres.','Réunis les couleurs, retire les crayons abîmés, puis partage entre 4 enfants.','Vérifie le partage et la prise en compte des crayons abîmés.','4 × 9 + 6 = 42 crayons.','4*9+6==24+18==42','Si les 36 crayons utilisables sont partagés entre 6 enfants, combien chacun reçoit-il ?','6 crayons.','36//6==6')],
18:[
('Lina a 7 billes ; Noé en a 3 de plus ; Sami en a 3 fois autant.','Pour Noé, prolonge la barre de 7 de 3 unités ; pour Sami, juxtapose 3 barres de 7.','Calcule l’écart entre les billes de Sami et de Noé.','11 billes.','21-10==11','Si Lina avait 8 billes, combien Noé et Sami en auraient-ils avec les mêmes relations ?','Noé : 11 billes ; Sami : 24 billes.','8+3==11 and 8*3==24'),
('Album : 12 € ; coffret : 4 fois le prix de l’album.','Le prix du coffret est représenté par 4 barres identiques de 12 €.','Quel serait le prix avec seulement 4 € de plus que l’album ?','16 €, car on ajouterait 4 au lieu de répéter 12 quatre fois.','12+4==16','Quel est l’écart entre le prix du coffret et celui de l’album ?','36 €.','48-12==36'),
('Boîte : 56 cartes ; elle contient 7 fois autant de cartes qu’une pochette.','La barre de 56 se partage en 7 petites barres identiques : une par pochette.','Vérifie la quantité d’une pochette par multiplication.','7 × 8 = 56 cartes.','7*8==56','Combien de cartes contiennent deux de ces pochettes ?','16 cartes.','2*8==16'),
('Ruban rouge : 18 cm ; ruban bleu : 5 fois cette longueur.','Le ruban bleu se dessine avec 5 morceaux de 18 cm alignés.','Quel serait le ruban bleu avec seulement 5 cm de plus ?','23 cm.','18+5==23','Quel est l’écart entre les deux rubans de l’histoire initiale ?','72 cm.','90-18==72'),
('Mila : 36 images ; Sami : une quantité 3 fois plus petite.','Partage la barre de 36 en 3 parts égales ; une part représente Sami.','Vérifie la quantité de Sami.','3 × 12 = 36 images.','3*12==36','Combien Sami aurait-il avec 3 images de moins que Mila ?','33 images.','36-3==33'),
('Petite boîte : 250 g ; grande boîte : 4 fois cette masse.','Représente la grande boîte par 4 barres de 250 g.','Quelle serait la masse avec seulement 4 g de plus ?','254 g.','250+4==254','Quelle est la masse de deux petites boîtes ?','500 g.','2*250==500'),
('Grand trajet : 32 km ; il est 4 fois aussi long que le petit.','Partage le trajet de 32 km en 4 portions identiques ; une portion représente le petit.','Vérifie par multiplication.','4 × 8 = 32 km.','4*8==32','Quelle serait la longueur du petit trajet si le grand était seulement 4 km plus long ?','28 km.','32-4==28'),
('Noé : 15 cartes ; Lina : 30 cartes ; on cherche une relation entre les quantités.','Deux barres de 15 couvrent la barre de 30 : le lien est multiplicatif.','Combien Lina aurait-elle avec seulement 2 cartes de plus ?','17 cartes.','15+2==17','Sami a 3 fois autant de cartes que Noé. Combien en a-t-il ?','45 cartes.','3*15==45'),
('On part de 8 billes ; on compare un ajout de 4 à une répétition 4 fois.','Pour la première histoire, ajoute 4 unités ; pour la seconde, dessine 4 barres de 8.','Quel écart sépare les deux résultats ?','20 billes.','32-12==20','Reprends les deux histoires avec 6 billes et le nombre 4. Quels résultats ?','10 billes avec 4 de plus ; 24 billes avec 4 fois autant.','6+4==10 and 6*4==24')]
}
EX[20]=[
'''Combien de dixièmes couvrent une moitié ?|On coupe la même bande en dix parts ; une moitié couvre cinq parts.|5 dixièmes ; 1/2 = 5/10.|F(1,2)==F(5,10)
Quelle fraction de chaque bande reste blanche ?|L’autre moitié n’a pas été coloriée.|1/2 ; 5/10.|1-F(1,2)==F(5,10)
Écris la même moitié avec des sixièmes.|On partage chacune des deux moitiés en trois.|3/6.|F(1,2)==F(3,6)
Deux gâteaux de tailles différentes sont coloriés à moitié. Peut-on affirmer que les morceaux ont la même taille ?|Une fraction décrit une part du tout choisi ; la taille du tout doit être la même pour comparer les morceaux.|Non : une moitié d’un grand gâteau peut être plus grande qu’une moitié d’un petit.''',
'''Comment obtenir huit parts égales par pliage ?|Plie une bande en deux, encore en deux, puis encore en deux.|On obtient 8 parts égales.|2*2*2==8
Combien de huitièmes restent blancs après le coloriage ?|La bande contient huit parts, dont quatre sont coloriées.|4/8.|F(8,8)-F(4,8)==F(4,8)
Écris cette moitié en quarts.|Deux quarts recouvrent une moitié de la même bande.|2/4.|F(4,8)==F(2,4)
Noé colorie 3 parts sur 8. A-t-il colorié une moitié ?|Une moitié exige quatre des huit parts égales.|Non : il manque 1/8.|F(4,8)-F(3,8)==F(1,8)''',
'''Sur une bande en sixièmes, combien de parts reste-t-il après avoir colorié la moitié ?|Une moitié colore 3 parts et la bande en compte 6.|3 parts.|6-3==3
Combien de douzièmes faut-il pour compléter 1/3 jusqu’au tout ?|Un tiers recouvre 4 douzièmes ; on complète jusqu’à 12.|8/12.|1-F(1,3)==F(8,12)
Pourquoi 3/4 et 9/12 sont-ils égaux ?|Chaque quart est recoupé en trois ; les trois quarts donnent trois groupes de trois parts.|3 quarts deviennent 9 douzièmes, sans changer la zone coloriée.|F(3,4)==F(9,12)
Une bande de 12 cases a 6 cases coloriées. Donne la fraction puis son écriture en moitiés.|Les six cases représentent la moitié des douze cases égales.|6/12 = 1/2.|F(6,12)==F(1,2)''',
'''Pourquoi 2/6 ne convient-il pas dans la liste ?|Une moitié de six parts en exige trois, et non deux.|2/6 est inférieur à 1/2.|F(2,6)<F(1,2)
Pourquoi 5/12 ne convient-il pas ?|Une moitié de douze parts en exige six.|Il manque 1/12 pour atteindre 1/2.|F(1,2)-F(5,12)==F(1,12)
Ajoute une écriture de la moitié qui n’est pas dans la liste.|Dix parts égales se partagent en deux groupes de cinq.|5/10.|F(5,10)==F(1,2)
Avec une bande en huitièmes, combien de parts blanches faut-il laisser pour colorier la moitié ?|La moitié colore quatre parts et laisse les quatre autres.|4 parts blanches.|8-4==4''',
'''Combien de dixièmes restent pour compléter 2/5 jusqu’au tout ?|2/5 représente 4/10 ; le tout contient 10 dixièmes.|6/10.|1-F(2,5)==F(6,10)
Explique 2/3 = 4/6 avec un découpage.|On coupe chaque tiers en deux ; les deux tiers coloriés deviennent quatre parts.|4 sixièmes couvrent les 2 tiers.|F(2,3)==F(4,6)
Quelle fraction en douzièmes représente un demi-tout ?|On colorie la moitié des douze parts égales.|6/12.|F(1,2)==F(6,12)
Noé écrit 3/3 = 3/12. Explique son erreur.|Trois tiers couvrent tout ; trois douzièmes ne couvrent qu’un quart.|Le tout s’écrit 12/12 ; 3/12 n’est pas égal à 3/3.|F(3,3)==F(12,12) and F(3,12)!=1''',
'''Décris précisément les coloriages de tes deux bandes.|Les bandes ont la même longueur et les parts de chaque bande sont égales.|Colorier 2 parts sur 3 sur l’une, et 4 parts sur 6 sur l’autre.
Que reste-t-il blanc sur chaque bande ?|Il reste un tiers sur la première et deux sixièmes sur la seconde.|1/3 = 2/6.|1-F(2,3)==F(1,3)==F(2,6)
Écris la partie coloriée avec des douzièmes.|Chaque tiers est découpé en quatre parts.|8/12.|F(2,3)==F(8,12)
Peut-on décaler une bande pour vérifier l’égalité des longueurs coloriées ?|Pour comparer les extrémités, les bandes doivent commencer au même endroit.|Il faut aligner les débuts et garder des bandes de même longueur.''',
'''Combien de parts du gâteau restent après la prise de Lina ?|Le gâteau avait 12 parts et Lina en prend 6.|6 parts.|12-6==6
Écris la partie restante en douzièmes puis en moitiés.|Six des douze parts restent.|6/12 = 1/2.|F(6,12)==F(1,2)
Si le même gâteau était partagé en 4 parts égales, combien Lina prendrait-elle pour garder la même quantité ?|Une moitié recouvre deux quarts.|2 parts sur 4.|F(6,12)==F(2,4)
Lina dit « j’ai pris 6 parts donc 6 gâteaux ». Corrige.|Une part n’est qu’un morceau du gâteau découpé.|Elle prend la moitié d’un seul gâteau.''',
'''Que signifie 5/5 d’un tout ?|On prend les cinq parts sur les cinq parts égales disponibles.|Le tout entier.|F(5,5)==1
Quel numérateur manque dans …/9 pour représenter le tout ?|Il faut prendre les neuf parts égales.|9.|F(9,9)==1
Combien de douzièmes reste-t-il après avoir pris le tout ?|Toutes les parts ont été prises.|0 douzième.|F(12,12)-1==0
Un gâteau a 8 parts égales. Écris le tout avec cette découpe.|Le numérateur et le dénominateur indiquent tous deux les huit parts.|8/8 = 1.|F(8,8)==1''',
'''Dessine deux bandes de même longueur pour contrôler Noé.|Partage l’une en deux, l’autre en quatre et aligne leurs débuts.|1 moitié et 2 quarts atteignent la même extrémité.|F(1,2)==F(2,4)
Quel est le rôle du dénominateur ?|Il indique le nombre de parts égales qui forment le tout.|Il donne la découpe du tout, donc la taille de chaque part.
Écris 1/2 avec des douzièmes.|La moitié de douze parts en contient six.|6/12.|F(1,2)==F(6,12)
Une bande est coloriée aux 2/4. Quelle fraction faut-il encore colorier pour couvrir le tout ?|Il reste deux parts sur quatre.|2/4 = 1/2.|1-F(2,4)==F(1,2)''']
EX[21]=[
'''Sur deux bandes identiques, quelle part est la plus petite : un huitième ou un quart ?|Le même tout est partagé en plus de parts dans la première bande.|1/8 < 1/4.|F(1,8)<F(1,4)
Écris 3/4 avec des huitièmes.|Chaque quart contient deux huitièmes.|3/4 = 6/8.|F(3,4)==F(6,8)
Combien de huitièmes séparent les deux coloriages ?|On compare 6 huitièmes à 3 huitièmes.|3/8.|F(3,4)-F(3,8)==F(3,8)
Quelle fraction manque à 3/4 pour couvrir le tout ?|Le tout contient quatre quarts.|1/4.|1-F(3,4)==F(1,4)''',
'''Combien de douzièmes séparent 5/12 et 8/12 ?|Les parts ont la même taille ; on compte les parts supplémentaires.|3/12.|F(8,12)-F(5,12)==F(3,12)
Combien de dixièmes séparent 3/10 et 7/10 ?|On retire 3 parts aux 7 parts.|4/10.|F(7,10)-F(3,10)==F(4,10)
Écris une fraction entre 5/12 et 8/12.|On garde les mêmes parts et on choisit 6 ou 7 parts.|Par exemple 6/12.|F(5,12)<F(6,12)<F(8,12)
Un gâteau identique est partagé entre deux enfants : l’un prend 7/10, l’autre 3/10. Peut-on donner ces parts ?|On réunit les dixièmes pris par les enfants.|Oui : 7/10 + 3/10 = 1.|F(7,10)+F(3,10)==1''',
'''Écris 2/3 avec des neuvièmes.|Chaque tiers est partagé en trois.|2/3 = 6/9.|F(2,3)==F(6,9)
Combien de neuvièmes séparent 2/3 et 2/9 ?|On retire 2 neuvièmes aux 6 neuvièmes.|4/9.|F(2,3)-F(2,9)==F(4,9)
Pourquoi ne compare-t-on pas seulement 8 et 12 dans 5/8 et 5/12 ?|Les numérateurs sont égaux ; les huitièmes sont plus grands que les douzièmes.|Cinq huitièmes couvrent davantage que cinq douzièmes.
Compare maintenant 1/3 et 1/9.|Un tiers du même tout est plus grand qu’un neuvième.|1/3 > 1/9.|F(1,3)>F(1,9)''',
'''Combien de dixièmes représente un cinquième ?|On coupe chacun des cinq morceaux en deux.|1/5 = 2/10.|F(1,5)==F(2,10)
Combien de dixièmes manque-t-il à 2/5 pour atteindre 5/10 ?|2/5 vaut 4/10 ; on complète jusqu’à 5/10.|1/10.|F(5,10)-F(2,5)==F(1,10)
Compare 2/5 et 3/10.|On utilise 4/10 pour représenter 2/5.|2/5 > 3/10.|F(2,5)>F(3,10)
Sur des bandes identiques, 5/10 est-il une moitié ?|Cinq est la moitié de dix.|Oui : 5/10 = 1/2.|F(5,10)==F(1,2)''',
'''Combien de huitièmes séparent 3/4 et 5/8 ?|3/4 recouvre 6 huitièmes.|1/8.|F(3,4)-F(5,8)==F(1,8)
Combien de douzièmes séparent 2/3 et 7/12 ?|2/3 recouvre 8 douzièmes.|1/12.|F(2,3)-F(7,12)==F(1,12)
Compare 3/4 et 7/8.|On remplace 3/4 par 6/8.|3/4 < 7/8.|F(3,4)<F(7,8)
Combien de douzièmes faut-il ajouter à 7/12 pour atteindre 1 ?|Le tout compte 12 douzièmes.|5/12.|1-F(7,12)==F(5,12)''',
'''Quelle fraction de la liste représente le tout ?|Prendre quatre parts sur quatre revient à tout prendre.|4/4.|F(4,4)==1
Quelle fraction est égale à une moitié ?|Deux quarts recouvrent une moitié.|2/4.|F(2,4)==F(1,2)
Range les quatre fractions dans l’ordre décroissant.|On prend la liste croissante dans l’autre sens.|4/4 > 3/4 > 2/4 > 1/4.|F(4,4)>F(3,4)>F(2,4)>F(1,4)
Combien de quarts séparent la plus grande et la plus petite ?|On retire un quart aux quatre quarts.|3/4.|F(4,4)-F(1,4)==F(3,4)''',
'''Écris 1/3 avec des sixièmes.|Chaque tiers est partagé en deux.|1/3 = 2/6.|F(1,3)==F(2,6)
Quelle fraction de son gâteau reste à Lina ?|On retire deux sixièmes aux six sixièmes du tout.|4/6.|1-F(2,6)==F(4,6)
Quelle fraction de son gâteau reste à Sami ?|On retire un tiers aux trois tiers du tout.|2/3.|1-F(1,3)==F(2,3)
Compare leurs restes.|4/6 et 2/3 couvrent la même part de gâteaux identiques.|Ils ont autant de gâteau : 4/6 = 2/3.|F(4,6)==F(2,3)''',
'''Écris 3/5 avec des dixièmes.|Chaque cinquième vaut deux dixièmes.|3/5 = 6/10.|F(3,5)==F(6,10)
Quelle fraction sépare les zones coloriées ?|On retire six dixièmes à sept dixièmes.|1/10.|F(7,10)-F(3,5)==F(1,10)
Quelle fraction reste blanche sur la deuxième bande ?|Le tout contient dix dixièmes.|3/10.|1-F(7,10)==F(3,10)
Si on colorie encore 1/10 de la première bande, compare les deux.|La première atteint sept dixièmes, comme la deuxième.|Elles sont aussi coloriées : 3/5 + 1/10 = 7/10.|F(3,5)+F(1,10)==F(7,10)''',
'''Écris 4/6 avec des douzièmes.|Chaque sixième est partagé en deux.|4/6 = 8/12.|F(4,6)==F(8,12)
Combien de douzièmes séparent les deux fractions ?|On retire quatre douzièmes à huit douzièmes.|4/12.|F(4,6)-F(4,12)==F(4,12)
Écris 4/12 avec des tiers.|Quatre douzièmes recouvrent un tiers du tout.|4/12 = 1/3.|F(4,12)==F(1,3)
Compare 2/12 et 2/6 sur le même tout.|Deux sixièmes valent quatre douzièmes.|2/12 < 2/6.|F(2,12)<F(2,6)''']
EX[22]=[
'''Quelle longueur représente une unité u dans ce chapitre ?|La bande-unité de référence est choisie avant toute mesure.|4 cm.
Combien mesure un quart d’unité en centimètres ?|On partage 4 cm en quatre parts égales.|1 cm.|4//4==1
Quelle est la longueur du segment en centimètres ?|Une unité vaut 4 cm ; les trois quarts ajoutent 3 cm.|7 cm.|4+3==7
Complète le segment pour atteindre 2 u. Quelle longueur faut-il ajouter ?|Il manque un des quatre quarts de la deuxième unité.|1/4 u, soit 1 cm.|F(2)-1-F(3,4)==F(1,4)''',
'''Explique comment préparer une règle en quarts.|On choisit u = 4 cm, puis on partage cette longueur en quatre morceaux égaux.|Les traits des quarts sont espacés de 1 cm.|4//4==1
Quelle longueur représente 1/2 u en centimètres ?|Deux des quatre quarts font une moitié.|2 cm.|4*F(1,2)==2
Quel morceau manque à ton segment de 3/4 u pour atteindre u ?|On complète trois quarts jusqu’à quatre quarts.|1/4 u, soit 1 cm.|1-F(3,4)==F(1,4)
Compare les segments de 1/2 u et 3/4 u.|On écrit la moitié en quarts.|1/2 u = 2/4 u < 3/4 u.|F(1,2)==F(2,4)<F(3,4)''',
'''Combien mesure la partie de 2 u en centimètres ?|Chaque unité mesure 4 cm.|8 cm.|2*4==8
Combien mesure la partie de 1/4 u en centimètres ?|On partage les 4 cm de l’unité en quatre.|1 cm.|4*F(1,4)==1
Quel repère faut-il aligner sur le début du segment ?|La mesure doit commencer à l’origine de la règle.|La graduation zéro, puis on marque 9 cm.|8+1==9
Combien ajouter à ce segment pour obtenir 2 u + 3/4 u ?|La partie entière reste la même ; il manque deux quarts.|1/2 u, soit 2 cm.|F(3,4)-F(1,4)==F(1,2)''',
'''Combien de dixièmes forment une unité entière ?|L’unité a été partagée en dix parts égales.|10 dixièmes.|F(10,10)==1
Quelle graduation représente 3/5 u sur la même règle ?|Chaque cinquième contient deux dixièmes.|6/10 u.|F(3,5)==F(6,10)
Quelle longueur est la plus grande : 1/2 u ou 1/5 u ?|Sur la règle en dixièmes, on compare 5 parts à 2 parts.|1/2 u > 1/5 u.|F(1,2)>F(1,5)
Combien de dixièmes séparent ces deux longueurs ?|On retire les deux dixièmes aux cinq dixièmes.|3/10 u.|F(1,2)-F(1,5)==F(3,10)''',
'''Pourquoi 3/5 u se place-t-il à la graduation 6/10 u ?|Chaque cinquième est coupé en deux.|Trois groupes de deux dixièmes donnent six dixièmes.|F(3,5)==F(6,10)
Quelle partie entière faut-il reporter avant les dixièmes ?|La mesure commence par une unité complète.|1 u, soit 4 cm.
Quelle longueur manque pour atteindre 2 u ?|De six dixièmes à une unité entière, il manque quatre dixièmes.|4/10 u, soit 2/5 u.|1-F(3,5)==F(4,10)==F(2,5)
Une autre bande mesure 1 u + 1/2 u. Laquelle est la plus longue ?|Les unités entières sont égales ; on compare 6/10 à 5/10.|La bande de 1 u + 3/5 u est plus longue.|F(3,5)>F(1,2)''',
'''Combien de huitièmes forment un quart d’unité ?|Chaque quart est partagé en deux.|2/8 u.|F(1,4)==F(2,8)
Combien de huitièmes manque-t-il à 3/4 u pour atteindre u ?|3/4 u vaut 6/8 u ; on complète jusqu’à 8/8 u.|2/8 u.|1-F(3,4)==F(2,8)
Quelle graduation en huitièmes correspond à 1/2 u ?|La moitié des huit parts en contient quatre.|4/8 u.|F(1,2)==F(4,8)
Compare les positions 5/8 u et 3/4 u.|3/4 u est placé au sixième huitième.|5/8 u < 3/4 u.|F(5,8)<F(3,4)''',
'''Quelle est la largeur de l’intervalle entre les deux bornes ?|Les parties entières sont égales ; les fractions diffèrent d’un dixième.|1/10 u.|F(8,10)-F(7,10)==F(1,10)
Peut-on dire que la bande mesure exactement 2 u + 7/10 u ?|L’énoncé dit qu’elle dépasse cette mesure.|Non : la borne inférieure est exclue.
Peut-on dire que la bande mesure exactement 2 u + 8/10 u ?|L’énoncé dit qu’elle n’atteint pas cette mesure.|Non : la borne supérieure est exclue.
Une bande mesure 2 u + 6/10 u. Respecte-t-elle l’encadrement ?|Six dixièmes sont inférieurs aux sept dixièmes de la borne inférieure.|Non : elle est trop courte.|F(6,10)<F(7,10)''',
'''Combien de fois reporte-t-on la petite bande ?|Quatre quarts couvrent une unité entière.|4 fois.|4*F(1,4)==1
Si u mesure 4 cm, quelle longueur mesure la petite bande ?|Le quart de 4 cm mesure 1 cm.|1 cm.|4*F(1,4)==1
Quelle longueur obtient-on après trois reports ?|On a assemblé trois quarts, sans trou ni chevauchement.|3/4 u, soit 3 cm.|3*F(1,4)==F(3,4)
Pourquoi faut-il éviter les chevauchements ?|Une partie serait comptée deux fois alors qu’elle n’augmente pas la longueur assemblée.|La longueur obtenue serait trop courte.''',
'''Quel repère doit coïncider avec le début du segment ?|La mesure indique la distance à partir de zéro.|La graduation zéro.
Si le segment commence au trait 1 cm et finit au trait 4 cm, quelle est sa longueur ?|On cherche la distance entre les deux graduations.|3 cm.|4-1==3
Pour u = 4 cm, écris cette longueur en fraction d’unité.|Trois des quatre centimètres de l’unité sont parcourus.|3/4 u.|F(3,4)*4==3
Comment vérifier une mesure sans changer de règle ?|On déplace correctement la règle et on relit la graduation finale.|Aligner le zéro sur le début puis vérifier que la fin indique 3 cm.''']
EX[23]=[
'''Pourquoi garde-t-on le dénominateur 12 dans la première addition ?|Les parts sont toutes des douzièmes ; seules les quantités de parts s’ajoutent.|3 + 5 = 8 parts de même taille, donc 8/12.|F(3,12)+F(5,12)==F(8,12)
Quelle fraction manque à 8/12 pour faire le tout ?|Le tout compte douze douzièmes.|4/12.|1-F(8,12)==F(4,12)
Vérifie la soustraction par une addition.|On réunit le reste et les quatre dixièmes retirés.|5/10 + 4/10 = 9/10.|F(5,10)+F(4,10)==F(9,10)
Un gâteau a 12 parts égales. On mange 3 parts puis 5 parts. Combien de parts restent ?|Huit parts ont été mangées ; on les retire aux douze parts.|4 parts, soit 4/12.|12-3-5==4''',
'''Combien de huitièmes représentent le tout ?|Toutes les huit parts sont prises.|8/8.|F(8,8)==1
Vérifie le complément de 5/8 par une addition.|On réunit la fraction de départ et la fraction manquante.|5/8 + 3/8 = 1.|F(5,8)+F(3,8)==1
Combien de douzièmes représentent le tout ?|Toutes les douze parts sont prises.|12/12.|F(12,12)==1
Un gâteau est mangé aux 7/12. Quelle fraction reste à partager ?|Le reste est le complément jusqu’à douze douzièmes.|5/12.|1-F(7,12)==F(5,12)''',
'''Écris 1/3 avec des sixièmes et explique le découpage.|Chaque tiers est coupé en deux parts égales.|1/3 = 2/6.|F(1,3)==F(2,6)
Pourquoi les deux calculs donnent-ils le même résultat ?|Le premier réunit 2 et 1 sixièmes ; le second retire 2 à 5 sixièmes.|Dans les deux cas, on obtient 3/6.|F(2,6)+F(1,6)==F(5,6)-F(2,6)==F(3,6)
Quelle fraction manque à ce résultat pour faire le tout ?|Trois sixièmes sur six sont déjà pris.|3/6 = 1/2.|1-F(3,6)==F(1,2)
Une bande de 1 u perd 1/3 u puis 1/6 u. Quelle longueur reste ?|Les morceaux retirés totalisent trois sixièmes de l’unité.|1/2 u.|1-F(1,3)-F(1,6)==F(1,2)''',
'''Écris 1/2 et 3/4 avec des huitièmes.|Chaque moitié contient quatre huitièmes et chaque quart deux huitièmes.|1/2 = 4/8 ; 3/4 = 6/8.|F(1,2)==F(4,8) and F(3,4)==F(6,8)
Vérifie la soustraction 3/4 - 1/8 par addition.|On remet la part retirée au résultat.|5/8 + 1/8 = 6/8 = 3/4.|F(5,8)+F(1,8)==F(3,4)
Quelle fraction manque à 5/8 pour faire 1 ?|Le tout vaut huit huitièmes.|3/8.|1-F(5,8)==F(3,8)
Une bande est coloriée à moitié, puis encore d’un huitième. Quelle fraction reste blanche ?|La zone coloriée atteint cinq huitièmes.|3/8.|1-F(1,2)-F(1,8)==F(3,8)''',
'''Écris 2/5 avec des dixièmes et 1/3 avec des douzièmes.|Chaque cinquième devient deux dixièmes ; chaque tiers devient quatre douzièmes.|2/5 = 4/10 ; 1/3 = 4/12.|F(2,5)==F(4,10) and F(1,3)==F(4,12)
Quelle fraction manque à 7/10 pour faire le tout ?|On complète jusqu’à dix dixièmes.|3/10.|1-F(7,10)==F(3,10)
Vérifie le deuxième calcul par une addition.|On remet les quatre douzièmes retirés aux sept douzièmes restants.|7/12 + 4/12 = 11/12.|F(7,12)+F(4,12)==F(11,12)
Un gâteau est mangé aux 2/5 puis aux 3/10. Quelle fraction reste ?|Les deux prises font sept dixièmes du même gâteau.|3/10.|1-F(2,5)-F(3,10)==F(3,10)''',
'''Écris le tout avec des quarts.|Un tout contient ses quatre quarts.|4/4 = 1.|F(4,4)==1
Vérifie le complément par une addition en quarts.|Trois quarts réunis à un quart recouvrent le tout.|3/4 + 1/4 = 1.|F(3,4)+F(1,4)==1
Explique le passage d’un quart à trois douzièmes.|On partage chaque quart en trois parts égales.|1/4 = 3/12.|F(1,4)==F(3,12)
On mange encore 1/12 sur le quart restant. Quelle fraction reste ?|Le quart restant vaut trois douzièmes ; on en retire un.|2/12.|F(1,4)-F(1,12)==F(2,12)''',
'''Écris la part de Lina avec des huitièmes.|Chaque quart contient deux huitièmes.|1/4 = 2/8.|F(1,4)==F(2,8)
Quelle fraction les deux enfants mangent-ils ensemble ?|On réunit deux huitièmes et trois huitièmes.|5/8.|F(1,4)+F(3,8)==F(5,8)
Vérifie le reste en reconstituant le tout.|La partie mangée et la partie restante doivent couvrir huit huitièmes.|5/8 + 3/8 = 1.|F(5,8)+F(3,8)==1
Un troisième enfant mange 1/8 du gâteau initial. Quelle fraction reste ?|On retire un huitième aux trois huitièmes restants.|2/8.|F(3,8)-F(1,8)==F(2,8)''',
'''Écris les deux morceaux retirés en sixièmes.|Un tiers se partage en deux sixièmes.|1/3 u = 2/6 u ; l’autre morceau vaut 1/6 u.|F(1,3)==F(2,6)
Quelle longueur totale est retirée ?|On réunit deux sixièmes et un sixième.|3/6 u = 1/2 u.|F(1,3)+F(1,6)==F(1,2)
Vérifie la longueur restante.|Une moitié retirée et une moitié restante reconstituent l’unité.|1/2 u + 1/2 u = 1 u.|F(1,2)+F(1,2)==1
On coupe encore 1/6 u. Quelle longueur reste alors ?|Il restait trois sixièmes ; on en retire un.|2/6 u, soit 1/3 u.|F(1,2)-F(1,6)==F(1,3)''',
'''Combien de quarts représente 1/2 ?|On coupe la moitié du tout en deux quarts.|2/4.|F(1,2)==F(2,4)
Décris un coloriage qui montre la bonne addition.|Sur une bande en quatre parts égales, colorie deux parts puis une troisième.|Trois quarts sont coloriés ; un quart reste blanc.|F(2,4)+F(1,4)==F(3,4)
Vérifie que le résultat laisse exactement un quart.|On complète trois quarts jusqu’au tout.|3/4 + 1/4 = 1.|F(3,4)+F(1,4)==1
Noé écrit aussi 1/3 + 1/6 = 2/9. Corrige avec des sixièmes.|Un tiers vaut deux sixièmes ; on ajoute encore un sixième.|1/3 + 1/6 = 3/6 = 1/2.|F(1,3)+F(1,6)==F(1,2)''']

def combos(i):
 dims=[[3,2],[4,2],[3,4],[2,5],[2,3,2],[2,2,2],[3,4],[3,3],[3,4]][i]
 names=[['lettres','nombres'],['parfums','fruits'],['tee-shirts','shorts'],['couleurs','symboles'],['entrées','plats','desserts'],['chapeaux','hauts','pantalons'],['pains','garnitures'],['lettres','nombres'],['couleurs','formes']][i]
 from itertools import product
 n=1
 for d in dims:n*=d
 tail=1
 for d in dims[1:]:tail*=d
 q=[item('Énumère les choix possibles quand le premier choix est fixé : utilise les lettres A, B, C… pour la deuxième catégorie et 1, 2… pour la troisième si elle existe.','On garde le premier choix identique et on associe toutes les possibilités restantes.',', '.join(''.join(str(v) for v in z) for z in product(*[[chr(65+j) for j in range(dims[1])]]+([list(range(1,dims[2]+1))] if len(dims)>2 else [])))+f' : {tail} possibilités.',str(tail)+'=='+str(tail))]
 q.append(item(f'Combien de possibilités correspondent à chacun des {dims[0]} choix de la première catégorie ? Comment éviter un oubli ?','On reproduit une ligne identique pour chacun des premiers choix et on parcourt toutes les colonnes.',f'{tail} possibilités pour chaque premier choix ; on vérifie {dims[0]} lignes complètes.',f'{dims[0]}*{tail}=={n}'))
 q.append(item(f'On ajoute un choix de {names[0]}, sans changer les autres catégories. Combien de combinaisons obtient-on ?','Le nouveau premier choix apporte autant de combinaisons qu’une ligne du tableau.',f'{n+tail} combinaisons.',f'{n}+{tail}=={n+tail}'))
 new=1
 for d in dims[:-1]:new*=d
 q.append(item(f'On revient au choix de départ puis on retire un choix de {names[-1]}. Combien de combinaisons reste-t-il ?','Chaque groupe perd un choix de la dernière catégorie ; on recompte les lignes complètes.',f'{n-new} combinaisons.',f'{n}-{new}=={n-new}'))
 if i==8:
  q[0]=item('Énumère les 12 couples pour la première possibilité proposée, avec couleurs A, B, C et formes 1, 2, 3, 4.','Pour chaque couleur, on associe les quatre formes.','A1, A2, A3, A4 ; B1, B2, B3, B4 ; C1, C2, C3, C4.', '3*4==12')
 return q

def trace(check):
 """Explicite les opérations du problème ; aucun eval d'un code externe."""
 if not check:return ''
 out=[]
 def visit(n):
  if isinstance(n,ast.Constant):return n.value
  if isinstance(n,ast.Call):return F(*(visit(x) for x in n.args))
  if isinstance(n,ast.BinOp):
   a,b=visit(n.left),visit(n.right)
   op={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.FloorDiv:operator.floordiv,ast.Div:operator.truediv}[type(n.op)]
   v=op(a,b)
   sym={ast.Add:'+',ast.Sub:'-',ast.Mult:'×',ast.FloorDiv:'÷',ast.Div:'÷'}[type(n.op)]
   if isinstance(a,int) and isinstance(b,int) and type(n.op) in [ast.Add,ast.Sub] and b>=10:
    pieces=[b//1000*1000,b%1000//100*100,b%100//10*10,b%10];cur=a;steps=[]
    for p in pieces:
     if p:nextv=cur+p if isinstance(n.op,ast.Add) else cur-p;steps.append(f'{fmt(cur)} {sym} {fmt(p)} = {fmt(nextv)}');cur=nextv
    out.append('; '.join(steps)+'.')
   elif isinstance(n.op,ast.FloorDiv):out.append(f'{fmt(a)} ÷ {fmt(b)} = {fmt(v)}, car {fmt(b)} × {fmt(v)} = {fmt(a)}.')
   elif isinstance(n.op,ast.Mult) and isinstance(a,int) and isinstance(b,int) and max(a,b)>10 and min(a,b)<=10:
    small,big=sorted([a,b]);t=big//10*10;u=big%10
    out.append(f'{fmt(big)} = {fmt(t)} + {fmt(u)} ; {small} × {fmt(t)} = {fmt(small*t)} ; {small} × {u} = {fmt(small*u)} ; {fmt(small*t)} + {fmt(small*u)} = {fmt(v)}.')
   else:out.append(f'{fmt(a)} {sym} {fmt(b)} = {fmt(v)}.')
   return v
  if isinstance(n,ast.Compare):
   visit(n.left)
   for c in n.comparators:visit(c)
   return True
  if isinstance(n,ast.BoolOp):
   for x in n.values:visit(x)
   return True
  return None
 visit(ast.parse(check,mode='eval').body)
 return '\n\n'.join(dict.fromkeys(out))

def figure(spec):
 kind,data=spec
 s=[r'\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]']
 def node(x,y,t,opt=''):s.append(r'\node['+opt+f'] at ({x},{y}) '+'{'+t+'};')
 def band(n,d,y=0,label=True,col='otGreen!30'):
  for j in range(d):s.append(f'\\fill[{col if j<n else "white"}] ({j*6.4/d:.4f},{y}) rectangle ({(j+1)*6.4/d:.4f},{y+.48});')
  s.append(f'\\draw[otNavy] (0,{y}) rectangle (6.4,{y+.48});')
  for j in range(1,d):s.append(f'\\draw[otNavy] ({j*6.4/d:.4f},{y}) -- ({j*6.4/d:.4f},{y+.48});')
  if label:node(7.05,y+.24,rf'$\dfrac{{{n}}}{{{d}}}$')
 if kind in ['place4','exchanges4']:
  vals=[data] if kind=='place4' else [[2,14,3,17],[3,4,4,7]]
  for j,l in enumerate(['milliers','centaines','dizaines','unités']):
   node(1+j*1.9,1.25,l,'font=\\normalsize,text=otNavy');s.append(f'\\draw[otRule] ({.1+j*1.9},.85)--({1.9+j*1.9},.85);')
   for r,v in enumerate(vals):node(1+j*1.9,.45-r*.8,str(v[j]),'text=otGreenDark' if r else '')
  if kind=='exchanges4':node(3.85,-1.1,'Même quantité après les échanges','font=\\normalsize,text=otGreenDark')
 elif kind in ['scaledline','markedline']:
  a,b,step,missing=data;tot=(b-a)//step
  s.append(r'\draw[otNavy,->] (-.15,0)--(8.2,0);')
  for i in range(tot+1):
   x=8*i/tot;v=a+i*step;s.append(f'\\draw[otNavy] ({x},-.09)--({x},.09);')
   label='?' if kind=='scaledline' and v in missing else fmt(v).replace(' ',r'\,')
   if (tot<=8 or i%2==0) or (kind=='markedline' and v==missing):node(x,-.4,'$'+label+'$','font=\\normalsize')
   if kind=='markedline' and v==missing:s.append(f'\\fill[otGreenDark] ({x},0) circle (3pt);')
  node(4,.6,'Graduations régulièrement espacées','font=\\normalsize,text=otMuted')
 elif kind in ['fraccompare','fracbar','fracjoin']:
  if kind=='fraccompare':
   for j,(n,d) in enumerate(data):band(n,d,(1-j)*1.1)
  elif kind=='fracbar':band(data[0],data[1],label=False)
  else:
   (a,b),(c,d),op=data;common=max(b,d);n=a*(common//b);m=c*(common//d)
   band(n,common,1.1,col='otNavy!18');band(m,common,0,col='otOrange!35');node(3.2,2.15,'Même unité, mêmes parts','font=\\normalsize,text=otNavy')
 elif kind=='unitlength':
  d,whole,n=data;v=whole+n/d;end=max(whole+1,2);width=7.8/end
  s.append(f'\\draw[otNavy,->] (-.1,0)--({7.8+.25},0);')
  for k in range(end*d+1):
   x=k*width/d;s.append(f'\\draw[otNavy] ({x:.4f},-.1)--({x:.4f},.1);')
   if k%d==0:node(x,-.4,f'{k//d} u' if k else '0','font=\\normalsize')
  s.append(f'\\draw[otGreenDark,line width=3pt] (0,.72)--({v*width:.4f},.72);')
  s.append(f'\\draw[otGreenDark,dashed] ({v*width:.4f},.6)--({v*width:.4f},.16);')
  node(3.9,1.3,'Segment à mesurer','text=otGreenDark,font=\\normalsize');node(3.9,-1.05,f'Une unité partagée en {d} parts égales','font=\\normalsize')
 elif kind=='partwhole':
  total,part,*unit=data;cut=7.5*part/total
  s.append(f'\\draw[otNavy,fill=otSky] (0,0) rectangle (7.5,.6);\\draw[otNavy] ({cut:.4f},0)--({cut:.4f},.6);')
  node(cut/2,.3,fmt(part));node((cut+7.5)/2,.3,'?','text=otGreenDark');node(3.75,1.2,f'Tout : {fmt(total)} '+(unit[0] if unit else 'livres'),'text=otNavy')
 elif kind in ['comparetot','timesbars']:
  a,b,*units=data
  if kind=='comparetot':
   s.append(r'\draw[otNavy,fill=otSky] (0,1.3) rectangle (5,1.85);\draw[otNavy,fill=otSky] (0,0) rectangle (5,.55);\draw[otGreenDark,fill=otGreen!20] (5,0) rectangle (7.2,.55);')
   node(2.5,1.575,str(a));node(2.5,.275,str(a));node(6.1,.275,'+'+str(b));node(3.6,-.6,'Ensemble : réunir les deux barres','font=\\normalsize')
  else:
   w=7.5/b;s.append(f'\\draw[otNavy,fill=otSky] (0,1.3) rectangle ({w},1.85);')
   unit=units[0] if units else '€';node(w/2,1.575,str(a)+' '+unit)
   for k in range(b):s.append(f'\\draw[otNavy,fill=otGreen!20] ({k*w},0) rectangle ({(k+1)*w},.55);');node((k+.5)*w,.275,str(a)+' '+unit)
   node(3.75,-.6,f'{b} fois la même quantité','font=\\normalsize,text=otGreenDark')
 elif kind=='mixedgroups':
  pairs=data or [(3,8),(2,6)];wid=7.8/max(n for n,v in pairs)
  for row,(n,v) in enumerate(pairs):
   y=(1-row)*1.4
   for k in range(n):s.append(f'\\draw[otNavy,fill=otSky] ({k*wid},{y}) rectangle ({k*wid+wid-.18},{y+.65});');node(k*wid+(wid-.18)/2,y+.325,str(v))
  node(3.5,-.65,'Chaque cadre représente un groupe','font=\\normalsize')
 elif kind=='choices':
  for j,l in enumerate(['Pantalon 1','Pantalon 2']):node(4.2,1.3-j*1.1,l,'font=\\normalsize,text=otNavy')
  for j in range(3):
   node(0,2.6-j*1.2,chr(65+j),'text=otNavy')
   for k in range(2):s.append(f'\\draw[otRule] (.35,{2.6-j*1.2})--(3.1,{1.3-k*1.1});')
  node(4.5,2.8,'3 tee-shirts, 2 pantalons','font=\\normalsize')
 elif kind=='choicetree':
  # Labels dans un couloir libre, les arêtes s’arrêtent avant les lettres.
  for e in range(2):
   ey=-(e*6+2.5)*.7;node(.3,ey,f'E{e+1}','font=\\normalsize')
   for p in range(3):
    py=-(e*6+p*2+.5)*.7;node(3,py,f'P{p+1}','font=\\normalsize');s.append(f'\\draw[otRule] (.7,{ey})--(2.6,{py});')
    for d in range(2):
     dy=-(e*6+p*2+d)*.7;node(6.3,dy,f'D{d+1}','font=\\normalsize,text=otGreenDark');s.append(f'\\draw[otRule] (3.4,{py})--(5.9,{dy});')
  node(3.3,1,'Entrée puis plat puis dessert','font=\\normalsize,text=otNavy')
 else:raise ValueError(kind)
 s.append(r'\end{tikzpicture}')
 return '\n'.join(s)

VERIFIER=r'''"""Vérification autonome des fichiers livrés et des opérations des situations."""
from pathlib import Path
import ast,json,re,hashlib,operator
from fractions import Fraction as F
P=Path(__file__).resolve().parent
def evaluate(n):
 if isinstance(n,ast.Expression):return evaluate(n.body)
 if isinstance(n,ast.Constant) and isinstance(n.value,(int,bool)):return n.value if isinstance(n.value,bool) else F(n.value)
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='F':return F(*(evaluate(a) for a in n.args))
 if isinstance(n,ast.BinOp):return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.FloorDiv:operator.floordiv,ast.Div:operator.truediv}[type(n.op)](evaluate(n.left),evaluate(n.right))
 if isinstance(n,ast.BoolOp):return all(evaluate(x) for x in n.values)
 if isinstance(n,ast.Compare):
  vals=[evaluate(n.left)]+[evaluate(c) for c in n.comparators]
  ops={ast.Eq:operator.eq,ast.NotEq:operator.ne,ast.Lt:operator.lt,ast.LtE:operator.le,ast.Gt:operator.gt,ast.GtE:operator.ge}
  return all(ops[type(o)](a,b) for o,a,b in zip(n.ops,vals,vals[1:]))
 raise ValueError(ast.dump(n))
def frac(s):return re.sub(r'(?<![\w\\])(\d+)/(\d+)(?!\w)',lambda m:r'$\dfrac{'+m[1]+'}{'+m[2]+'}$',s)
source=json.loads((P/'sources_locales/chapitre.json').read_text(encoding='utf-8'))
plan=json.loads((P/'situations_verifiees.json').read_text(encoding='utf-8'))
txt=(P/'exercices.txt').read_text(encoding='utf-8')
blocks=[x for x in re.split(r'^===[ \t]*$',txt,flags=re.M) if x.strip()]
assert len(blocks)==len(source['exercices'])==len(plan)==9
checks=0
for i,(b,model,original) in enumerate(zip(blocks,plan,source['exercices']),1):
 assert f'Id: nouveau-{i}\n' in b
 enonce=b.split('Énoncé:\n',1)[1].split('\nÉtapes:',1)[0]
 steps=b.split('Étapes:\n',1)[1].split('\nSolution:',1)[0]
 sol=b.split('Solution:\n',1)[1]
 assert len(re.findall(r'^\d+\. ',enonce,re.M))==5
 assert len(re.findall(r'^## Question \d+ :',steps,re.M))==5
 assert frac(original['consigne']) in enonce,(i,'couverture source')
 if original.get('check'):assert evaluate(ast.parse(original['check'],mode='eval')),(i,'source fausse');checks+=1
 for j,q in enumerate(model,1):
  assert f'{j}. '+frac(q['q']) in enonce,(i,j,'énoncé modifié')
  answer=frac(q['a'])
  actual=re.search(rf'^{j}\. (.*)$',sol,re.M)
  assert actual and actual[1]==answer,(i,j,'solution numérique ou verbale différente')
  section=re.search(rf'^## Question {j} :[\s\S]*?(?=^## Question |\Z)',steps,re.M)[0]
  assert answer in section and '::: methode' in section and '::: etape' in section and '::: resultat' in section
  if q['check']:
   assert evaluate(ast.parse(q['check'],mode='eval')),(i,j,q['check'])
   checks+=1
 # Toutes les fractions simples restent dans le domaine CE2.
 for a,d in re.findall(r'\\dfrac\{(\d+)\}\{(\d+)\}',enonce+steps+sol):assert 0<=int(a)<=int(d)<=12
for name in ['cours_nouveau.txt','fiche_nouvelle.txt']:
 t=(P/name).read_text(encoding='utf-8');assert '<!-- optitab:1 -->' in t
 for a,d in re.findall(r'\\dfrac\{(\d+)\}\{(\d+)\}',t):assert 0<=int(a)<=int(d)<=12
numeric_equalities=0
corrections='\n'.join(b.split('Étapes:\n',1)[1] for b in blocks)
corrections=re.sub(r'\\dfrac\{(\d+)\}\{(\d+)\}',r'\1/\2',corrections).replace('$','')
number=r'\d+(?:[ \u00a0]\d{3})*(?:/\d+)?'
expression=rf'{number}(?:[ ]*[+×÷-][ ]*{number})*'
pattern=rf'(?<![\w/,])({expression})[ ]*=[ ]*({expression})(?![\d/,])'
def value(s):return evaluate(ast.parse(s.replace(' ','').replace('\u00a0','').replace('×','*').replace('÷','/'),mode='eval'))
for m in re.finditer(pattern,corrections):
 a,c=m.groups()
 assert value(a)==value(c),(m[0],'égalité fausse dans le fichier réellement livré')
 numeric_equalities+=1
report={'math_OK':True,'exercices':9,'questions':45,'situations_recalculees':checks,'egalites_lues_et_recalculees':numeric_equalities,'fichiers_sha256':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','situations_verifiees.json']}}
(P/'resultats_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
'''

for code in CODES:
 p=next(BASE.glob(f'{code:02}_*'));d=json.loads((p/'sources_locales/chapitre.json').read_text(encoding='utf-8'))
 figdir=p/'figures';figdir.mkdir(exist_ok=True)
 figs={'cours_schema':figure(d['figure'])}
 corr={'cours':{'nouveau':{'1':{'fichier':'cours_schema.png','alt':f'Schéma de référence : {d["titre"]}.'}}},'fiches':{'nouvelle':{}},'exercices':{}}
 if code in [1,2,3,18,20,21,22,23]:corr['fiches']['nouvelle']['1']=corr['cours']['nouveau']['1']
 if code in [15,16,17,19]:
  meth='1. Je raconte l’histoire et je nomme ce qui est cherché.\n2. Je fais un schéma avec des barres ou des groupes.\n3. Je calcule en expliquant ce que donne chaque étape.\n4. Je vérifie puis je réponds avec l’unité.'
 elif code in [20,21,23]:meth='1. Je choisis des bandes ou des gâteaux de même taille.\n2. Je partage en parts égales et je repère les parts prises.\n3. Si nécessaire, je recoupe pour avoir des parts de même taille.\n4. Je calcule ou je compare, puis je contrôle avec le dessin.'
 elif code==22:meth='1. Je choisis la bande-unité : ici, u = 4 cm.\n2. Je partage l’unité en parts égales.\n3. Je place le zéro au début du segment.\n4. Je compte les unités entières puis les parts de la dernière unité.'
 else:meth='1. Je construis la quantité avec des groupes de mille, cent, dix et un.\n2. Je représente les rangs ou les graduations.\n3. Je lis les chiffres en gardant les rangs vides.\n4. Je contrôle par une décomposition ou par les nombres voisins.'
 warning=d['vigilance']
 if code in [20,21,23]:warning+=' Une fraction porte ici sur un même tout ; ses parts doivent être égales.'
 course='Titre: '+d['titre']+'\n\n<!-- optitab:1 -->\n'+block('objectifs',d['objectif'])+'\n## I. Je manipule\n\n'+block('methode',d['manipulation'],'Avec le matériel')+'\n## II. Je comprends le schéma\n\n[IMAGE_1]\n\n'+block('definition','\n\n'.join(d['lecon']))+'\n## III. Je passe au calcul\n\n'+block('methode',meth)+ '\n'+block('exemple',d['exemple'],'Un exemple expliqué')+'\n## IV. Je m’entraîne\n\n'+block('exemple',d['guide']+'\n\n'+d['guide_reponse'],'À faire puis à vérifier')+'\n'+block('attention',warning,'Je fais attention')+'\n'+block('retenir','\n'.join('- '+x for x in d['lecon']))
 sheet='Titre: À retenir — '+d['titre']+'\n\n<!-- optitab:1 -->\n'+block('objectifs',d['objectif'])+'\n## I. Les repères\n\n'+block('retenir','\n'.join('- '+x for x in d['lecon']))+ ('\n[IMAGE_1]\n' if corr['fiches']['nouvelle'] else '')+'\n## II. La méthode\n\n'+block('methode',meth)+'\n'+block('exemple',d['exemple'])+'\n'+block('attention',d['aide'])
 (p/'cours_nouveau.txt').write_text(fr(course),encoding='utf-8');(p/'fiche_nouvelle.txt').write_text(fr(sheet),encoding='utf-8')
 rendered=[];models=[]
 for i,x in enumerate(d['exercices'],1):
  if code in PROB:
   known,scheme,vq,va,vc,tq,ta,tc=PROB[code][i-1]
   questions=[item('Reformule les données utiles et dis ce que l’on cherche.','On distingue les quantités connues et la quantité inconnue avant de choisir une opération.',known),item('Dessine un schéma et annonce les opérations dans l’ordre.','Chaque barre ou groupe doit représenter une quantité nommée.',scheme),item(x['consigne'],'On suit le schéma ; chaque calcul reçoit une unité et un sens.\n\n'+trace(x['check']),x['reponse'],x['check']),item(vq,'Le contrôle doit retrouver une donnée de départ, ou expliquer le sens du résultat.',va,vc),item(tq,'On garde la même histoire et on modifie seulement la donnée annoncée.\n\n'+trace(tc),ta,tc)]
  else:
   extra=combos(i-1) if code==19 else rows(EX[code][i-1])
   why=trace(x['check']) or ('On s’appuie sur les rangs et les groupes de dix.' if code<=3 else 'On fixe un choix de la première catégorie, puis on énumère tous les choix possibles des autres catégories ; on recommence pour chaque premier choix.' if code==19 else 'On partage des bandes de même longueur en parts égales et on suit les graduations.' if code==22 else 'On représente chaque fraction par des parts égales du même tout.')
   questions=[item(x['consigne'],why+'\n\n'+x['reponse'],x['reponse'],x['check'])]+extra
  assert len(questions)==5
  ident=f'nouveau-{i}';corr['exercices'][ident]={};img='';stepimg='';schemaimg=''
  if code in PROB:
   questions[2]['q']='Résous le problème de la situation : écris les calculs puis une phrase de réponse.'
  schemas={15:{1:['partwhole',[2121,1245,'cahiers']],5:['partwhole',[725,268,'billes']],9:['partwhole',[95,18,'cartes']]},16:{1:['comparetot',[146,28]],5:['partwhole',[850,423,'cm']],9:['comparetot',[128,35]]},17:{1:['mixedgroups',[[5,6],[4,4]]],5:['partwhole',[48,36,'pommes']],9:['partwhole',[42,6,'crayons']]},18:{1:['timesbars',[7,3,'billes']],5:['timesbars',[12,3,'images']],9:['timesbars',[8,4,'billes']]}}
  if code in schemas and i in schemas[code]:
   name=f'ex{i}_schema';figs[name]=figure(schemas[code][i]);corr['exercices'][ident]['1']={'fichier':name+'.png','alt':f'Schéma en barres ou groupes du problème {i}, avec les quantités de la situation.'};schemaimg='\n[IMAGE_1]\n'
  if x['figure']:
   name=f'ex{i}_enonce';figs[name]=figure(x['figure']);corr['exercices'][ident]['1']={'fichier':name+'.png','alt':f'Schéma de l’exercice {i} : '+x['consigne']};img='\n\n[IMAGE_1]'
  if code==19 and i==5:
   name='ex5_arbre';figs[name]=figure(['choicetree',None]);corr['exercices'][ident]['1']={'fichier':name+'.png','alt':'Arbre complet des 2 entrées, 3 plats et 2 desserts : 12 menus.'};stepimg='\n[IMAGE_1]\n'
  if code==20 and i==2:
   figs['ex2_correction']=figure(['fracbar',[4,8,True]]);corr['exercices'][ident]['2']={'fichier':'ex2_correction.png','alt':'Quatre huitièmes de la bande coloriés montrent une moitié.'};stepimg='\n[IMAGE_2]\n'
  if code==20 and i in [6,9]:
   spec=['fraccompare',[[2,3],[4,6]]] if i==6 else ['fraccompare',[[2,4],[1,2]]]
   name=f'ex{i}_correction';figs[name]=figure(spec);corr['exercices'][ident]['1']={'fichier':name+'.png','alt':'Bandes de même longueur montrant deux écritures égales de la même fraction.'};stepimg='\n[IMAGE_1]\n'
  title=('Découverte' if i<=2 else 'Entraînement' if i<=6 else 'Problème')+' - '+d['titre']+f' — atelier {i}'
  en=('Situation : '+x['consigne']+'\n\n' if code in PROB else '')+'\n'.join(f'{j}. '+q['q'] for j,q in enumerate(questions,1))+img
  steps=[]
  for j,q in enumerate(questions,1):
   titleq=['Comprendre','Représenter','Résoudre','Contrôler','Transférer'][j-1] if code in PROB else ['Chercher','Observer','Expliquer','Vérifier','Réinvestir'][j-1]
   steps.append(f'## Question {j} : {titleq}\n\n'+block('methode','Je relie la question aux données et au dessin.')+'\n'+block('etape',q['why'],'Je raisonne')+ ('\n'+stepimg if j==1 and stepimg else '')+ ('\n'+schemaimg if j==2 and schemaimg else '')+'\n'+block('resultat',q['a']))
  rendered.append('=== '+title+'\nId: '+ident+'\nDifficulté: '+('easy' if i<=3 else 'medium')+'\n\nÉnoncé:\n<!-- optitab:1 -->\n'+en+'\n\nÉtapes:\n<!-- optitab:1 -->\n'+'\n'.join(steps)+'\nSolution:\n<!-- optitab:1 -->\n'+'\n'.join(f'{j}. '+q['a'] for j,q in enumerate(questions,1))+'\n')
  models.append(questions)
 (p/'exercices.txt').write_text(fr('\n===\n\n'.join(rendered)),encoding='utf-8')
 (p/'situations_verifiees.json').write_text(json.dumps(models,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (p/'verif_math.py').write_text(VERIFIER,encoding='utf-8')
 (figdir/'figures.py').write_text('# -*- coding: utf-8 -*-\n"""Figures TikZ ; compilation uniquement par outils/figures_livre.py --jobs 1."""\nFIGURES = '+repr(figs)+'\n',encoding='utf-8')
 (figdir/'correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (p/'COUVERTURE.md').write_text('# Couverture du livre CE2\n\n9 exercices sources conservés et enrichis ; 45 questions avec 45 corrigés détaillés.\n\n| Exercice source | Bloc final | Question source | Enrichissement |\n|---|---|---|---|\n'+'\n'.join(f'| {i} | nouveau-{i} | {3 if code in PROB else 1} | Compréhension, représentation, contrôle et transfert liés à la situation |' for i in range(1,10))+'\n\nProgramme officiel : [BO 2024, programme cycle 2](https://www.education.gouv.fr/sites/default/files/document/Annexe%204%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20du%20cycle%202-403821.pdf), pages 18–24. Entiers et résultats jusqu’à 10 000 ; fractions au plus égales à 1, dénominateur au plus 12 ; longueurs mixtes avec unités entières explicitement admises ; parts de même taille pour les calculs. Écriture à virgule réservée aux prix.\n',encoding='utf-8')
 (p/'RAPPORT.md').write_text('# Rapport CE2\n\nÉtat : textes, définitions TikZ et vérification mathématique préparés ; validation visuelle en attente de la fenêtre de compilation autorisée par l’orchestrateur.\n\n9 exercices du livre couverts sans retrait : 5 questions réelles et 5 corrigés par bloc. Aucun contexte CE2 en base : identifiants nouveau-1 à nouveau-9. Cours et fiche reconstruits au format OptiTAB v1 ; vocabulaire CE2 et progression manipulation → schéma → calcul.\n\n'+f'Figures : {len(figs)} figures TikZ originales préparées, aucun ancien PNG conservé ; palette et préambule communs des livres.\n\n'+'Contrôle autonome : verif_math.py lit les fichiers finaux et le livre local, vérifie les 45 couples question/corrigé, les expressions numériques, les bornes des fractions et la couverture. Résultats dans resultats_math.json.\n\nAucune écriture en base ni modification de source. Validation navigateur et lecture de chaque PNG à effectuer avant statut prêt.\n',encoding='utf-8')
 (p/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'ce2_nombres_problemes','maj':'2026-11-02','phase':'textes_math_figures_definis'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,len(figs),'figures',len(models)*5,'questions')
