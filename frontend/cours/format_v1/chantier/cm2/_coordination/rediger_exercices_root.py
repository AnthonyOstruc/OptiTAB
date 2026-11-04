"""Sept familles progressives par chapitre ; génération locale explicite, sans import."""
from pathlib import Path
from fractions import Fraction
import math,json,re
ROOT=Path(__file__).resolve().parent.parent
def num(x):
 x=Fraction(x)
 if x.denominator==1:return str(x.numerator)
 return str(float(x)).rstrip('0').rstrip('.').replace('.',r'{,}')
def f(x):return '$'+num(x)+'$'
def calc(left,right):return '$'+left+'='+num(right)+'$'
def q(question,method,steps,result):return {'question':question,'methode':method,'etapes':steps if isinstance(steps,list) else [steps],'resultat':result}
def heure(seconds):
 h,s=divmod(seconds%86400,3600);m,s=divmod(s,60)
 return f'{h} h {m:02} min'+(f' {s:02} s' if s else '')
def duree(seconds):
 h,s=divmod(seconds,3600);m,s=divmod(s,60)
 return (f'{h} h ' if h else '')+(f'{m} min ' if m or not h else '')+(f'{s} s' if s else '') or '0 s'
def table(headers,rows):return '\n'.join(['| '+' | '.join(map(str,headers))+' |','|'+'---|'*len(headers)]+['| '+' | '.join(map(str,row))+' |' for row in rows])
def ex(title,intro,questions,params=None,figure=None):return {'titre':title,'enonce':intro,'questions':questions,'parametres':params or {},'figure':figure}

def mesures(t,k):
 if k==0:
  cm=18+3*t;mass=125+25*t;cl=25+5*t
  return ex('Choisir une unité et contrôler une mesure',f'Un crayon mesure {cm} cm, une pomme pèse {mass} g et un verre contient {cl} cL.',[
   q('Quelle grandeur mesure-t-on pour chacun des trois objets ?','Relier chaque unité à la grandeur correspondante.','Le centimètre mesure une longueur, le gramme une masse et le centilitre une contenance.','Crayon : longueur ; pomme : masse ; verre : contenance.'),
   q('Exprimer la longueur du crayon en millimètres.','Chaque centimètre contient dix millimètres.',calc(f'{cm}\\times10',cm*10),f'Le crayon mesure {f(cm*10)} mm.'),
   q('Exprimer la contenance du verre en millilitres.','Chaque centilitre contient dix millilitres.',calc(f'{cl}\\times10',cl*10),f'Le verre contient {f(cl*10)} mL.')],{'famille':'unites','cm':cm,'g':mass,'cl':cl})
 if k==1:
  a=15+5*t;b=68+11*t;l=b-a
  return ex('Lire une règle dont le zéro est décalé',f'Sur une règle graduée en millimètres, un segment commence à la graduation {a} et finit à la graduation {b}.',[
   q('Quelle est sa longueur en millimètres ?','Soustraire la lecture de départ à la lecture de fin.',calc(f'{b}-{a}',l),f'La longueur est {f(l)} mm.'),
   q('Exprimer cette longueur en centimètres.','Dix millimètres représentent un centimètre.',calc(f'{l}\\div10',Fraction(l,10)),f'Le segment mesure {f(Fraction(l,10))} cm.'),
   q(f'Noé répond « {b} mm ». Pourquoi sa réponse est-elle fausse ?','Vérifier où commence le segment.',f'La lecture {b} mesure la distance depuis zéro, mais le segment commence à {a} mm. Il faut retirer cette partie.',f'Il faut soustraire {a} mm ; la bonne longueur est {l} mm.')],{'famille':'regle','debut':a,'fin':b})
 if k==2:
  m=2+t;cm=75+5*t;total=m*100;remaining=total-cm
  return ex('Découper un ruban puis partager le reste',f'Un ruban de {m} m est coupé de {cm} cm. Le reste est partagé en cinq morceaux de même longueur.',[
   q('Exprimer la longueur initiale en centimètres.','Mettre toutes les longueurs dans la même unité.',calc(f'{m}\\times100',total),f'La longueur initiale est {total} cm.'),
   q('Quelle longueur reste-t-il après la découpe ?','Retirer la longueur coupée.',calc(f'{total}-{cm}',remaining),f'Il reste {remaining} cm.'),
   q('Quelle est la longueur de chaque morceau ?','Diviser le reste en cinq parts égales.',calc(f'{remaining}\\div5',Fraction(remaining,5)),f'Chaque morceau mesure {f(Fraction(remaining,5))} cm.')],{'famille':'ruban','m':m,'coupe_cm':cm})
 if k==3:
  total=2300+350*t;tare=300+50*t;net=total-tare;n=(4,5,8)[t]
  return ex('La balance et la masse de l’emballage',f'Une caisse pleine pèse {num(Fraction(total,1000)).replace("{,}",",")} kg. La caisse vide pèse {tare} g. Elle contient {n} sachets identiques.',[
   q('Exprimer la masse totale en grammes.','Un kilogramme contient mille grammes.',calc(num(Fraction(total,1000))+r'\times1\,000',total),f'La caisse pleine pèse {total} g.'),
   q('Quelle est la masse de tous les sachets sans la caisse ?','Retirer la masse de l’emballage.',calc(f'{total}-{tare}',net),f'Les sachets pèsent ensemble {net} g.'),
   q('Quelle est la masse d’un sachet ?','Partager la masse du contenu en parts égales.',calc(f'{net}\\div{n}',Fraction(net,n)),f'Un sachet pèse {f(Fraction(net,n))} g.')],{'famille':'masse','total_g':total,'tare_g':tare,'sachets':n})
 if k==4:
  l=2+t;glass=25;ml=l*1000;portion=glass*10;n=ml//portion
  return ex('Remplir des verres sans se tromper d’unité',f'Une carafe contient {l} L de jus. Chaque verre contient 25 cL.',[
   q('Exprimer le contenu de la carafe en millilitres.','Chaque litre contient mille millilitres.',calc(f'{l}\\times1\\,000',ml),f'La carafe contient {ml} mL.'),
   q('Exprimer le contenu d’un verre en millilitres.','Chaque centilitre contient dix millilitres.',calc('25\\times10',portion),f'Un verre contient {portion} mL.'),
   q('Combien de verres peut-on remplir complètement ?','Diviser deux mesures exprimées dans la même unité.',calc(f'{ml}\\div{portion}',n),f'On remplit {n} verres sans reste.')],{'famille':'contenance','litres':l,'verre_cl':glass})
 if k==5:
  sides=[5+t,7+t,8+t];p=sum(sides)
  return ex('Le contour d’un triangle',f'Un jardin triangulaire a trois côtés de {sides[0]} m, {sides[1]} m et {sides[2]} m. On en fait le tour.',[
   q('Quelle distance parcourt-on en un tour ?','Additionner les trois côtés extérieurs.',calc('+'.join(map(str,sides)),p),f'Un tour mesure {p} m.'),
   q('Quelle distance parcourt-on en trois tours ?','Répéter trois fois le même parcours.',calc(f'3\\times{p}',3*p),f'Trois tours mesurent {3*p} m.'),
   q('Un sentier intérieur est ajouté. Le contour extérieur change-t-il ?','Distinguer le bord extérieur des traits intérieurs.','Le sentier ne déplace aucun côté extérieur. Il ne s’ajoute pas au périmètre.',f'Non. Le périmètre reste {p} m.')],{'famille':'contour','cotes':sides})
 a=12+2*t;b=7+t;gate=2+t;p=2*(a+b);need=p-gate;roll=10;rolls=math.ceil(need/roll)
 return ex('Acheter une clôture en tenant compte du portail',f'Un potager rectangulaire mesure {a} m sur {b} m. Un portail de {gate} m reste sans clôture. La clôture est vendue en rouleaux entiers de 10 m.',[
  q('Calculer la longueur du contour entier.','Additionner les deux longueurs et les deux largeurs.',calc(f'{a}+{b}+{a}+{b}',p),f'Le contour mesure {p} m.'),
  q('Quelle longueur de clôture faut-il poser ?','Retirer l’ouverture du portail.',calc(f'{p}-{gate}',need),f'Il faut poser {need} m de clôture.'),
  q('Combien de rouleaux faut-il acheter ?','Chercher le premier multiple de dix suffisant.',f'{rolls-1} rouleaux donnent {(rolls-1)*10} m, ce qui est insuffisant ; {rolls} rouleaux donnent {rolls*10} m.',f'Il faut {rolls} rouleaux entiers.')],{'famille':'cloture','longueur':a,'largeur':b,'portail':gate})

def aires(t,k):
 if k==0:
  whole=8+3*t;halves=4+2*t;total=whole+halves//2
  return ex('Réunir des demi-carreaux',f'Une surface recouvre {whole} carreaux entiers et {halves} demi-carreaux. Un carreau entier vaut 1 cm².',[
   q('À combien de carreaux entiers les demi-carreaux correspondent-ils ?','Réunir les demi-carreaux deux par deux.',calc(f'{halves}\\div2',halves//2),f'Ils correspondent à {halves//2} carreaux entiers.'),
   q('Quelle est l’aire totale de la surface ?','Ajouter les carreaux entiers et ceux reconstitués.',calc(f'{whole}+{halves//2}',total),f'L’aire est {total} cm².'),
   q('Peut-on connaître son périmètre avec ces seules informations ?','Se demander si la disposition des carreaux est connue.','Le comptage indique une surface, mais ne décrit pas son contour. Des dispositions différentes peuvent avoir la même aire.','Non : il manque la forme et la disposition des carreaux.')],{'famille':'carreaux','entiers':whole,'demis':halves})
 if k==1:
  l=2+t;w=50+25*t;cm=l*100;area=cm*w
  return ex('Un rectangle avec deux unités de longueur',f'Une affiche rectangulaire mesure {l} m de longueur et {w} cm de largeur.',[
   q('Exprimer sa longueur en centimètres.','Convertir avant de multiplier les dimensions.',calc(f'{l}\\times100',cm),f'La longueur vaut {cm} cm.'),
   q('Calculer son aire en centimètres carrés.','Compter les rangées de centimètres carrés.',calc(f'{cm}\\times{w}',area),f'L’aire est {area} cm².'),
   q('Exprimer cette aire en mètres carrés.','Un mètre carré contient dix mille centimètres carrés.',calc(f'{area}\\div10\\,000',Fraction(area,10000)),f'L’aire est {f(Fraction(area,10000))} m².')],{'famille':'rectangle','longueur_m':l,'largeur_cm':w})
 if k==2:
  dm=Fraction(25+5*t,10);cm=350+100*t;m=3+t
  return ex('Expliquer trois conversions d’aires',f'Convertir {f(dm)} dm² en cm², {cm} cm² en dm² et {m} m² en cm².',[
   q('Effectuer la première conversion.','Chaque décimètre carré contient cent centimètres carrés.',calc(num(dm)+r'\times100',dm*100),f'Cela donne {f(dm*100)} cm².'),
   q('Effectuer la deuxième conversion.','Regrouper les centimètres carrés par paquets de cent.',calc(f'{cm}\\div100',Fraction(cm,100)),f'Cela donne {f(Fraction(cm,100))} dm².'),
   q('Effectuer la troisième conversion.','Un mètre carré contient dix mille centimètres carrés.',calc(f'{m}\\times10\\,000',m*10000),f'Cela donne {m*10000} cm².')],{'famille':'conversions','dm2':str(dm),'cm2':cm,'m2':m})
 if k==3:
  l=8+t;w=6+t;a=3+t;b=2;outer=l*w;cut=a*b
  return ex('Une pièce avec un coin rectangulaire retiré',f'Une pièce est obtenue en retirant un coin de {a} m sur {b} m à un rectangle de {l} m sur {w} m. Le dessin indique le contour obtenu.\n\n[IMAGE_1]',[
   q('Quelle serait l’aire du grand rectangle complet ?','Calculer d’abord l’aire avant le retrait.',calc(f'{l}\\times{w}',outer),f'Le grand rectangle mesure {outer} m².'),
   q('Quelle aire a été retirée ?','Calculer l’aire du coin rectangulaire.',calc(f'{a}\\times{b}',cut),f'Le coin retiré mesure {cut} m².'),
   q('Quelle est l’aire de la pièce restante ?','Soustraire la surface retirée à la surface initiale.',calc(f'{outer}-{cut}',outer-cut),f'La pièce mesure {outer-cut} m².')],{'famille':'decomposition','L':l,'l':w,'coinL':a,'coinl':b},f'piece_l_{t}')
 if k==4:
  a=8+4*t;w=2+t;area=a*w;b=a//2;h=w*2;pa=2*(a+w);pb=2*(b+h)
  return ex('Même surface, contours différents',f'Le rectangle A mesure {a} cm sur {w} cm. Le rectangle B mesure {b} cm sur {h} cm.',[
   q('Comparer leurs aires.','Multiplier les dimensions de chaque rectangle.',[calc(f'{a}\\times{w}',area),calc(f'{b}\\times{h}',b*h)],f'Les deux aires valent {area} cm².'),
   q('Calculer le périmètre de chaque rectangle.','Additionner les quatre côtés de chaque contour.',[calc(f'{a}+{w}+{a}+{w}',pa),calc(f'{b}+{h}+{b}+{h}',pb)],f'Périmètres : A = {pa} cm ; B = {pb} cm.'),
   q('Une même aire impose-t-elle un même périmètre ?','Utiliser la comparaison précédente.',f'Les aires sont égales, mais {pa} et {pb} sont différents.','Non : ces deux rectangles constituent un contre-exemple.')],{'famille':'aire_perimetre','A':[a,w],'B':[b,h]})
 if k==5:
  l=5+t;w=3+t;area=l*w;tiles=area*4;box=8;nb=math.ceil(tiles/box)
  return ex('Prévoir des boîtes de dalles',f'Une terrasse rectangulaire mesure {l} m sur {w} m. Il faut 4 dalles pour recouvrir 1 m², sans perte. Une boîte contient 8 dalles.',[
   q('Quelle est l’aire de la terrasse ?','Calculer la surface du rectangle.',calc(f'{l}\\times{w}',area),f'La terrasse mesure {area} m².'),
   q('Combien de dalles faut-il ?','Chaque mètre carré demande quatre dalles.',calc(f'{area}\\times4',tiles),f'Il faut {tiles} dalles.'),
   q('Combien de boîtes entières faut-il acheter ?','Choisir le premier nombre de boîtes suffisant.',f'{nb-1} boîtes donnent {(nb-1)*8} dalles ; {nb} boîtes donnent {nb*8} dalles.',f'Il faut {nb} boîtes entières.')],{'famille':'pavage','longueur':l,'largeur':w,'dalles_m2':4,'boite':8})
 l=6+2*t;w=4+t;area=l*w;p=2*(l+w)
 return ex('Retrouver une dimension d’une surface',f'Un rectangle a une aire de {area} cm² et une longueur de {l} cm.',[
  q('Quelle est sa largeur ?','Trouver le nombre qui, multiplié par la longueur, donne l’aire.',calc(f'{area}\\div{l}',w),f'La largeur est {w} cm.'),
  q('Vérifier cette largeur en recalculant l’aire.','Multiplier les deux dimensions.',calc(f'{l}\\times{w}',area),f'On retrouve bien {area} cm².'),
  q('Calculer le périmètre du rectangle.','Additionner ses quatre côtés.',calc(f'{l}+{w}+{l}+{w}',p),f'Le périmètre est {p} cm.')],{'famille':'dimension','longueur':l,'aire':area})

def temps(t,k):
 if k==0:
  minutes=125+17*t;seconds=185+38*t;h,m=divmod(minutes,60);mm,ss=divmod(seconds,60)
  return ex('Regrouper les minutes et les secondes',f'Une randonnée dure {minutes} min. Une courte course dure {seconds} s.',[
   q('Exprimer la randonnée en heures et minutes.','Regrouper les minutes par paquets de soixante.',f'${minutes}={h}\\times60+{m}$.',f'Elle dure {h} h {m} min.'),
   q('Exprimer la course en minutes et secondes.','Regrouper les secondes par paquets de soixante.',f'${seconds}={mm}\\times60+{ss}$.',f'Elle dure {mm} min {ss} s.'),
   q('Exprimer la durée de la randonnée en secondes.','Chaque minute contient soixante secondes.',calc(f'{minutes}\\times60',minutes*60),f'Elle dure {minutes*60} s.')],{'famille':'conversions','minutes':minutes,'secondes':seconds})
 if k==1:
  h,m,s=[(8,20,15),(11,45,30),(16,10,45)][t];total=h*3600+m*60+s
  return ex('Lire les trois aiguilles d’une horloge',f'Observer le cadran {"ABC"[t]}. Il s’agit de l’{["heure du matin","heure du matin","heure de l’après-midi"][t]}. La trotteuse orange indique les secondes.\n\n[IMAGE_1]',[
   q('Quelle heure indique l’horloge, à la seconde près ?','Lire successivement les heures, les minutes et les secondes.',f'La petite aiguille a dépassé {h%12 or 12} ; la grande indique {m} min ; la trotteuse indique {s} s.',f'Il est {heure(total)}.'),
   q('Quelle heure sera-t-il 45 secondes plus tard ?','Ajouter les secondes et regrouper soixante secondes en une minute.',calc(f'{s}+45',s+45)+'. '+f'{s+45} s = {duree(s+45)}.',f'Il sera {heure(total+45)}.'),
   q('Combien de secondes reste-t-il avant la minute suivante ?','Compléter les secondes pour atteindre soixante.',calc(f'60-{s}',60-s),f'Il reste {60-s} s.')],{'famille':'horloge','h':h,'m':m,'s':s},f'horloge_{t}')
 if k==2:
  start=(13+t)*3600+45*60;end=(15+t)*3600+(20+5*t)*60;gap=end-start
  return ex('Calculer une durée en passant par les heures entières',f'Une activité commence à {heure(start)} et finit à {heure(end)} le même jour.',[
   q('Combien de temps sépare le départ de l’heure entière suivante ?','Compléter les minutes jusqu’à soixante.',calc('60-45',15),f'Il faut 15 min.'),
   q('Quelle est la durée complète de l’activité ?','Additionner les étapes jusqu’à l’arrivée.',f'15 min + 1 h + {20+5*t} min = {duree(gap)}.',f'La durée est {duree(gap)}.'),
   q('Exprimer cette durée en minutes.','Convertir l’heure puis ajouter les minutes restantes.',calc(f'60+{gap//60-60}',gap//60),f'La durée est {gap//60} min.')],{'famille':'ecoulee','debut_s':start,'fin_s':end})
 if k==3:
  start=23*3600+(40+3*t)*60;end=(15+7*t)*60;gap=86400-start+end
  return ex('Un trajet qui passe minuit',f'Un train part à {heure(start)} et arrive à {heure(end)} le lendemain.',[
   q('Quelle durée sépare le départ de minuit ?','Avancer jusqu’à vingt-quatre heures.',calc(f'60-{40+3*t}',20-3*t),f'Il reste {20-3*t} min avant minuit.'),
   q('Quelle est la durée du trajet ?','Ajouter le temps avant minuit et le temps après minuit.',calc(f'{20-3*t}+{15+7*t}',gap//60),f'Le trajet dure {gap//60} min.'),
   q('Pourquoi ne faut-il pas soustraire directement les deux nombres d’heures ?','Tenir compte du changement de jour.','L’arrivée appartient au lendemain. On passe par minuit pour conserver l’ordre des instants.','Le passage au jour suivant doit être pris en compte.')],{'famille':'minuit','depart_s':start,'arrivee_s':end})
 if k==4:
  start=9*3600+58*60+45;duration=150+35*t;end=start+duration
  return ex('Trouver la fin d’une activité avec secondes',f'Un exercice commence à {heure(start)} et dure {duree(duration)}.',[
   q('Exprimer la durée en secondes.','Convertir chaque minute en soixante secondes.',calc(f'{duration//60}\\times60+{duration%60}',duration),f'La durée vaut {duration} s.'),
   q('Combien de secondes manque-t-il pour atteindre 10 h ?','Compter 15 s jusqu’à 9 h 59, puis une minute.',calc('15+60',75),f'Il manque 75 s.'),
   q('À quelle heure finit l’exercice ?','Retirer les secondes qui mènent à 10 h, puis avancer du reste.',calc(f'{duration}-75',duration-75)+'. '+f'Après 10 h, il reste {duree(duration-75)}.',f'L’exercice finit à {heure(end)}.')],{'famille':'arrivee','depart_s':start,'duree_s':duration})
 if k==5:
  arrival=(10+t)*3600+15*60;travel=(48+7*t)*60;margin=10*60;depart=arrival-margin-travel
  return ex('Prévoir un départ avec une marge',f'Un rendez-vous est fixé à {heure(arrival)}. Le trajet dure {duree(travel)}. On veut être sur place 10 min avant le rendez-vous.',[
   q('À quelle heure faut-il être sur place ?','Reculer de dix minutes depuis l’horaire du rendez-vous.',f'À partir de {heure(arrival)}, on recule de 10 min.',f'Il faut être sur place à {heure(arrival-margin)}.'),
   q('À quelle heure faut-il partir au plus tard ?','Reculer encore de la durée du trajet.',f'De {heure(arrival-margin)}, reculer de {duree(travel)} mène à {heure(depart)}.',f'Il faut partir à {heure(depart)} au plus tard.'),
   q('Vérifier en avançant depuis l’heure de départ.','Refaire le trajet dans l’autre sens.',f'{heure(depart)} + {duree(travel)} = {heure(arrival-margin)}. Il reste bien 10 min avant {heure(arrival)}.',f'L’horaire de départ respecte la marge de 10 min.')],{'famille':'depart','rdv_s':arrival,'trajet_s':travel,'marge_s':margin})
 hours=Fraction(15+5*t,10);minutes=int(hours*60);claimed=int(hours)*60+int((hours-int(hours))*100)
 return ex('Distinguer l’écriture décimale et les minutes',f'Une affiche annonce une séance de {num(hours).replace("{,}",",")} h. Sam pense que cette écriture signifie {duree(claimed*60)}.',[
  q('Convertir la durée annoncée en minutes.','Multiplier le nombre d’heures par soixante.',calc(num(hours)+r'\times60',minutes),f'La séance dure {minutes} min.'),
  q('Écrire la bonne durée en heures et minutes.','Regrouper les minutes par soixante.',f'${minutes}={minutes//60}\\times60+{minutes%60}$.',f'La durée est {duree(minutes*60)}.'),
  q('La proposition de Sam est-elle correcte ?','Comparer sa durée avec la conversion précédente.',f'Sam annonce {claimed} min, alors que la durée vaut {minutes} min.',('Oui, dans ce cas le nombre d’heures est entier.' if claimed==minutes else 'Non : les minutes utilisent des paquets de 60, pas de 100.'))],{'famille':'decimal','heures':str(hours)})

def donnees(t,k):
 if k==0:
  values=[6+2*t,4+t,8+3*t];total=sum(values)
  return ex('Lire un tableau de préférences',table(['Fruit','Effectif'],zip(['Pomme','Poire','Banane'],values))+'\n\nChaque élève a donné une seule réponse.',[
   q('Combien d’élèves ont répondu ?','Additionner tous les effectifs.',calc('+'.join(map(str,values)),total),f'{total} élèves ont répondu.'),
   q('Quel fruit est le plus choisi et de combien dépasse-t-il la pomme ?','Comparer les effectifs puis calculer l’écart.',calc(f'{values[2]}-{values[0]}',values[2]-values[0]),f'La banane est la plus choisie, avec {values[2]-values[0]} réponses de plus que la pomme.'),
   q('La banane a-t-elle obtenu plus de la moitié des réponses ?','Comparer son effectif à la moitié du total.',calc(f'{total}\\div2',Fraction(total,2))+f'. Son effectif est {values[2]}.','Non : la catégorie la plus fréquente ne dépasse pas la moitié du total.')],{'famille':'tableau','valeurs':values})
 if k==1:
  v=[7+t,3+t,5+2*t,5+t];total=sum(v)
  return ex('Croiser deux informations dans un tableau',table(['Classe','À pied','À vélo'],[['CM1',v[0],v[1]],['CM2',v[2],v[3]]]),[
   q('Combien d’élèves de CM2 viennent à vélo ?','Lire à l’intersection de la ligne CM2 et de la colonne À vélo.',f'La cellule CM2 / À vélo contient {v[3]}.',f'{v[3]} élèves de CM2 viennent à vélo.'),
   q('Combien d’élèves viennent à vélo dans les deux classes réunies ?','Additionner les deux cases de la colonne concernée.',calc(f'{v[1]}+{v[3]}',v[1]+v[3]),f'{v[1]+v[3]} élèves viennent à vélo.'),
   q('Combien d’élèves figurent au total dans le tableau ?','Additionner toutes les cases sans les compter deux fois.',calc('+'.join(map(str,v)),total),f'Le tableau décrit {total} élèves.')],{'famille':'double_entree','valeurs':v})
 if k==2:
  v=[4+2*t,8+2*t,6+2*t]
  return ex('Lire des barres à l’aide de leur graduation',f'Le diagramme donne les prêts de livres de la classe CM2{"ABC"[t]} pendant trois jours.\n\n[IMAGE_1]',[
   q('Combien de livres ont été prêtés le mardi ?','Lire la hauteur de la barre au-dessus de Mar.',f'La barre de mardi atteint la graduation {v[1]}.',f'{v[1]} livres ont été prêtés mardi.'),
   q('Combien de prêts y a-t-il eu sur les trois jours ?','Additionner les trois hauteurs lues.',calc('+'.join(map(str,v)),sum(v)),f'Il y a eu {sum(v)} prêts.'),
   q('Combien de livres de plus ont été prêtés mardi que lundi ?','Calculer la différence entre les deux barres.',calc(f'{v[1]}-{v[0]}',v[1]-v[0]),f'Mardi compte {v[1]-v[0]} prêts de plus.')],{'famille':'barres','valeurs':v},f'barres_{t}')
 if k==3:
  v=[6+2*t,10+2*t,12+2*t,18+2*t];gap=v[-1]-v[0]
  return ex('Lire une croissance sur une courbe',f'La plante {"ABC"[t]} a été mesurée une fois par semaine. Les données sont fictives et exprimées en centimètres.\n\n[IMAGE_1]',[
   q('Quelle est sa hauteur en semaine 3 ?','Repérer la semaine 3 puis lire le point correspondant.',f'Le point au-dessus de 3 correspond à {v[2]} cm.',f'La plante mesure {v[2]} cm.'),
   q('De combien a-t-elle grandi entre les semaines 1 et 4 ?','Soustraire la première hauteur à la dernière.',calc(f'{v[-1]}-{v[0]}',gap),f'Elle a grandi de {gap} cm.'),
   q('Pendant quel intervalle d’une semaine la croissance a-t-elle été la plus forte ?','Comparer les écarts entre mesures successives.',[calc(f'{v[1]}-{v[0]}',4),calc(f'{v[2]}-{v[1]}',2),calc(f'{v[3]}-{v[2]}',6)],'La croissance la plus forte est entre les semaines 3 et 4 : 6 cm.')],{'famille':'courbe','valeurs':v},f'courbe_{t}')
 if k==4:
  total=24+8*t
  return ex('Lire les parts d’un disque','Le diagramme représente les choix de '+str(total)+' élèves : A occupe la moitié du disque, B et C occupent chacun un quart.\n\n[IMAGE_1]',[
   q('Combien d’élèves ont choisi A ?','Partager le total en deux parts égales.',calc(f'{total}\\div2',total//2),f'{total//2} élèves ont choisi A.'),
   q('Combien d’élèves ont choisi B ?','Partager le total en quatre parts égales.',calc(f'{total}\\div4',total//4),f'{total//4} élèves ont choisi B.'),
   q('Vérifier que les trois secteurs représentent tous les élèves.','Additionner les trois effectifs.',calc(f'{total//2}+{total//4}+{total//4}',total),f'On retrouve les {total} élèves : aucun choix ne manque.')],{'famille':'disque','total':total},'disque_parts')
 if k==5:
  raw=['A','B','A','C','B','A','B','A','C','A']+['C','B']*t;counts=[raw.count(x) for x in 'ABC']
  return ex('Passer d’une liste de réponses à une représentation',f'Une enquête recueille ces réponses, dans l’ordre : {", ".join(raw)}. Chaque lettre représente une activité différente.',[
   q('Compter le nombre de réponses A, B et C.','Cocher chaque réponse une seule fois en la regroupant par lettre.',table(['Réponse','Effectif'],zip('ABC',counts)),f'A : {counts[0]} ; B : {counts[1]} ; C : {counts[2]}.'),
   q('Vérifier le nombre total de réponses.','Comparer la somme des effectifs à la longueur de la liste.',calc('+'.join(map(str,counts)),len(raw)),f'Il y a bien {len(raw)} réponses.'),
   q('Décrire comment représenter ces données en barres.','Choisir une graduation régulière qui permet de lire tous les effectifs.',f'Sur l’axe vertical, une graduation représente une réponse. Tracer les catégories A, B, C puis des barres de hauteurs {counts[0]}, {counts[1]} et {counts[2]}.','Titre et axes nommés ; graduation de 1 en 1 ; trois barres de même largeur.')],{'famille':'enquete','reponses':raw})
 a,b,c=12+2*t,18+2*t,24+2*t
 return ex('Vérifier une affirmation à partir de données',f'Les effectifs de trois ateliers sont :\n\n'+table(['Atelier','Effectif'],[['A',a],['B',b],['C',c]])+f'\n\nUn graphique proposé affiche une barre à {a} pour A, {b+2} pour B et {c} pour C.',[
  q('Quelle barre contredit le tableau ?','Comparer chaque hauteur annoncée à la valeur du tableau.',f'A et C correspondent au tableau. Pour B, le tableau indique {b}, mais le dessin montre {b+2}.',f'La barre B doit descendre à {b}.'),
  q('Quel est le véritable effectif total ?','Utiliser le tableau de référence.',calc(f'{a}+{b}+{c}',a+b+c),f'Le total exact est {a+b+c}.'),
  q('Combien d’élèves ont choisi B ou C ?','Additionner seulement les deux catégories demandées.',calc(f'{b}+{c}',b+c),f'{b+c} élèves ont choisi B ou C.')],{'famille':'critique','valeurs':[a,b,c]})

def probabilites(t,k):
 if k==0:
  targets=[[2,4,6],[3,6],[1,2]][t];label=['un nombre pair','un multiple de 3','un nombre inférieur à 3'][t]
  return ex('Lister les résultats favorables d’un dé',f'On lance un dé équilibré à six faces numérotées de 1 à 6. On s’intéresse à l’évènement « obtenir {label} ».',[
   q('Lister toutes les issues possibles.','Recenser les six faces une fois chacune.','Les numéros possibles sont 1, 2, 3, 4, 5 et 6.','Il y a 6 issues équiprobables.'),
   q('Lister les issues favorables puis exprimer les chances.','Garder les numéros qui satisfont la condition.',f'Les numéros favorables sont {", ".join(map(str,targets))} : il y en a {len(targets)}.',f'Il y a {len(targets)} chances sur 6.'),
   q('L’évènement a-t-il moins, autant ou plus d’une chance sur deux ?','Comparer le nombre favorable à la moitié de six.',calc(r'6\div2',3)+f'. On compare {len(targets)} à 3.',('Autant : une chance sur deux.' if len(targets)==3 else 'Moins d’une chance sur deux.'))],{'famille':'de','favorables':targets})
 if k==1:
  green=3+t;orange=5+2*t;total=green+orange
  return ex('Ne pas confondre couleurs et jetons',f'Un sac contient {green} jetons verts et {orange} jetons orange. Les jetons sont identiques au toucher. On tire au hasard sans regarder.',[
   q('Combien de jetons peuvent être tirés ?','Compter tous les jetons, et pas seulement les couleurs.',calc(f'{green}+{orange}',total),f'Il y a {total} jetons équiprobables.'),
   q('Exprimer les chances d’obtenir vert.','Compter les jetons verts parmi tous les jetons.',f'{green} jetons favorables sur {total} jetons au total.',f'Il y a {green} chances sur {total} d’obtenir vert.'),
   q('La couleur verte a-t-elle une chance sur deux ?','Comparer le nombre de verts à la moitié du total.',calc(f'{total}\\div2',Fraction(total,2))+f'. Il n’y a que {green} verts.','Non, vert est moins probable qu’orange. Deux couleurs ne suffisent pas à rendre les chances égales.')],{'famille':'sac','verts':green,'orange':orange})
 if k==2:
  previous=['pile, pile, pile','face, pile, face, pile','face, face, face, face, face'][t]
  return ex('Une pièce ne garde pas le souvenir des lancers',f'On lance plusieurs fois une pièce équilibrée dans les mêmes conditions. Les résultats précédents sont : {previous}.',[
   q('Quelles sont les issues possibles du prochain lancer ?','Décrire l’expérience qui va se produire.','Le prochain lancer peut donner pile ou face.','Les deux issues possibles sont pile et face.'),
   q('Quelle chance a-t-on d’obtenir face au prochain lancer ?','Utiliser l’équilibre de la pièce et l’indépendance des lancers.','Les anciens résultats ne modifient pas la pièce. Pile et face restent équiprobables.','Face a 1 chance sur 2.'),
   q('Doit-on obtenir le résultat le moins fréquent pour compenser ?','Distinguer une chance et une obligation.','Chaque nouveau lancer conserve les mêmes chances ; aucune compensation n’est imposée.','Non : la pièce ne doit pas compenser les lancers précédents.')],{'famille':'independance','historique':previous})
 if k==3:
  wanted=['exactement une fois face','deux fois le même résultat','au moins une fois face'][t];fav=[['PF','FP'],['PP','FF'],['PF','FP','FF']][t]
  return ex('Deux lancers : l’ordre des résultats compte',f'On lance deux fois de suite une pièce équilibrée. P signifie pile et F signifie face. On cherche « {wanted} ».\n\n[IMAGE_1]',[
   q('Lister les quatre issues dans l’ordre des lancers.','Suivre chaque chemin de l’arbre.','Après P, on peut obtenir P ou F ; après F, on peut obtenir P ou F.','PP, PF, FP et FF : quatre issues équiprobables.'),
   q('Quelles issues réalisent l’évènement demandé ?','Vérifier la condition pour chacun des quatre couples.',f'On retient : {", ".join(fav)}.',f'{len(fav)} issues favorables : {", ".join(fav)}.'),
   q('Exprimer les chances de l’évènement.','Rapporter les issues favorables aux quatre issues équiprobables.',f'Il y a {len(fav)} chemins favorables parmi 4 chemins.',f'Il y a {len(fav)} chances sur 4.')],{'famille':'deux_pieces','evenement':t},'arbre_pieces' if t==0 else f'arbre_pieces_{t}')
 if k==4:
  cutoff=2+t;fav=list(range(1,cutoff+1))
  return ex('Justifier les chances sur une roue',f'Une roue équilibrée a quatre secteurs superposables numérotés de 1 à 4. On cherche à obtenir un numéro inférieur ou égal à {cutoff}.\n\n[IMAGE_1]',[
   q('Pourquoi les quatre numéros sont-ils équiprobables ?','Relier les chances à la construction de la roue.','La roue est équilibrée et les quatre secteurs sont superposables.','Chaque numéro a 1 chance sur 4.'),
   q('Lister les numéros favorables.','Tester les numéros de 1 à 4 avec la condition donnée.',f'Les numéros inférieurs ou égaux à {cutoff} sont {", ".join(map(str,fav))}.',f'Il y a {len(fav)} numéros favorables.'),
   q('Exprimer les chances puis dire si l’évènement est certain.','Comparer les issues favorables avec toutes les issues.',f'{len(fav)} numéros sont favorables parmi 4.',f'{len(fav)} chances sur 4 ; '+('l’évènement est certain.' if cutoff==4 else 'l’évènement n’est pas certain.'))],{'famille':'roue','borne':cutoff},'roue_quatre')
 if k==5:
  sums=3+t;pairs=[(a,b) for a in range(1,4) for b in range(1,4)];fav=[(a,b) for a,b in pairs if a+b==sums]
  rows=[[a]+[f'({a} ; {b})' for b in range(1,4)] for a in range(1,4)]
  return ex('Deux tirages et un tableau de couples',f'On tire au hasard une carte parmi 1, 2 et 3, on la remet puis on mélange avant un second tirage. Les trois cartes sont identiques au toucher. On cherche une somme égale à {sums}.',[
   q('Construire le tableau de tous les couples possibles.','Mettre le premier tirage en ligne et le second en colonne.',table(['Premier / second',1,2,3],rows),'Il y a 9 couples équiprobables.'),
   q('Quels couples donnent la somme demandée ?','Additionner les deux numéros de chaque couple.',f'Les couples retenus sont '+', '.join(f'({a} ; {b})' for a,b in fav)+'.',f'{len(fav)} couples donnent la somme {sums}.'),
   q('Exprimer les chances d’obtenir cette somme.','Compter les couples favorables parmi les neuf couples.',f'Il y a {len(fav)} couples favorables parmi 9.',f'Il y a {len(fav)} chances sur 9.')],{'famille':'couples','somme':sums})
 # Comparer deux sacs dont les totaux sont différents, par regroupement simple.
 red=2+t;total=2*red;redb=red;totalb=3*red
 return ex('Comparer deux sacs sans comparer seulement les quantités rouges',f'Le sac A contient {red} jetons rouges et {red} bleus. Le sac B contient {redb} rouges et {totalb-redb} bleus. Tous les jetons sont identiques au toucher et chaque tirage se fait au hasard.',[
  q('Exprimer les chances d’obtenir rouge dans A.','Compter les rouges puis tous les jetons de A.',calc(f'{red}+{red}',total),f'Il y a {red} chances sur {total}, soit une chance sur deux.'),
  q('Exprimer les chances d’obtenir rouge dans B.','Compter les rouges puis tous les jetons de B.',calc(f'{redb}+{totalb-redb}',totalb),f'Il y a {redb} chances sur {totalb}, soit une chance sur trois.'),
  q('Quel sac donne le plus de chances d’obtenir rouge ?','Comparer les parts rouges de chaque sac.','Dans A, la moitié des jetons sont rouges. Dans B, les rouges représentent seulement un des trois groupes égaux.',f'Le sac A est préférable, même si les deux sacs ont {red} jetons rouges.')],{'famille':'comparer','rouges':red})

GENERATORS={11:mesures,12:aires,18:temps,19:donnees,20:probabilites}
def render(item,i,tier):
 title=['Découverte','Entraînement','Problème'][tier]+' - '+item['titre']+f' - Parcours {tier+1}'
 questions=item['questions'];en=item['enonce']+'\n\n'+'\n'.join(f'{k}. {v["question"]}' for k,v in enumerate(questions,1))
 et=[];sol=[]
 for k,v in enumerate(questions,1):
  et.append(f'## Question {k} : {v["question"]}\n\n::: methode\n{v["methode"]}\n:::')
  for j,step in enumerate(v['etapes'],1):et.append(f'::: etape '+('Raisonner' if j==1 else 'Vérifier')+f'\n{step}\n:::')
  et.append('::: resultat\n'+v['resultat']+'\n:::');sol.append(f'{k}. '+v['resultat'])
 return f'=== {title}\nId: nouveau-{i}\nDifficulté: '+['easy','medium','hard'][tier]+'\n\nÉnoncé:\n<!-- optitab:1 -->\n'+en+'\n\nÉtapes:\n<!-- optitab:1 -->\n'+'\n\n'.join(et)+'\n\nSolution:\n<!-- optitab:1 -->\n'+'\n'.join(sol)+'\n'
if __name__=='__main__':
 for code,generator in GENERATORS.items():
  d=next(ROOT.glob(f'{code:02}_*'));bank=[]
  for tier in range(3):
   for family in range(7):
    item=generator(tier,family);item.update(id=f'nouveau-{len(bank)+1}',niveau=tier+1);bank.append(item)
  assert len({x['enonce'] for x in bank})==21
  (d/'exercices.txt').write_text('\n===\n\n'.join(render(x,i,x['niveau']-1) for i,x in enumerate(bank,1))+'\n===\n',encoding='utf-8')
  (d/'donnees_exercices_root.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print(code,len(bank),'exercices',sum(len(x['questions']) for x in bank),'questions')
