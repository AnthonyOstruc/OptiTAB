from commun_redaction import *
def longueurs(t,k):
 if k==0:
  cm=18+2*t;m=2+t;mm=45+5*t
  return ex(f'Unités et repères — atelier {t+1}',f'Une élève mesure un crayon de {cm} cm, un ruban de {m} m et une vis de {mm} mm.',[
   q('Quelle unité choisir pour l’épaisseur d’une pièce et la distance entre deux villes ?','Choisir une unité à l’échelle de l’objet.','Une pièce est très fine : quelques millimètres. Les villes peuvent être séparées de nombreux kilomètres.','Millimètres pour l’épaisseur ; kilomètres pour la distance.'),
   q('Exprimer la longueur du crayon en millimètres.','Un centimètre contient dix millimètres.',eq(f'{cm}\\times10',cm*10),f'{cm*10} mm.'),
   q('Exprimer la longueur du ruban en centimètres.','Un mètre contient cent centimètres.',eq(f'{m}\\times100',m*100),f'{m*100} cm.'),
   q('Exprimer la longueur de la vis en centimètres.','Regrouper les millimètres par dix.',eq(f'{mm}\\div10',F(mm,10)),f'${n(F(mm,10))}$ cm.'),
   q('Une gomme de 4 cm, une chaise de 90 cm et un terrain de 100 m sont-ils des repères raisonnables ?','Comparer avec des objets connus.','Une gomme tient dans la main, une chaise arrive environ à la taille d’un enfant et un terrain s’étend sur une grande distance.','Oui, ces trois ordres de grandeur sont raisonnables.')])
 if k==1:
  start=10+5*t;end=65+10*t;length=end-start;shift=20
  return ex(f'La règle décalée — mesure {t+1}',f'Sur une règle graduée en millimètres, un segment commence à {start} mm et finit à {end} mm.\n\n[IMAGE_1]',[
   q('La graduation de fin suffit-elle pour connaître la longueur ?','Vérifier si le segment commence à zéro.',f'Le segment commence à {start} mm et non à zéro. La lecture finale inclut donc une partie qui n’appartient pas au segment.','Non : il faut enlever la lecture de départ.'),
   q('Calculer sa longueur en millimètres.','Soustraire le départ de l’arrivée.',eq(f'{end}-{start}',length),f'{length} mm.'),
   q('Donner la longueur en centimètres.','Utiliser 10 mm = 1 cm.',eq(f'{length}\\div10',F(length,10)),f'${n(F(length,10))}$ cm.'),
   q(f'On déplace le segment sans le déformer : son début est à {start+shift} mm. Où est sa fin ?','Conserver la longueur.',eq(f'{start+shift}+{length}',end+shift),f'À la graduation {end+shift} mm.'),
   q(f'Un autre segment mesure {length+5} mm. De combien est-il plus long ?','Comparer dans la même unité.',eq(f'{length+5}-{length}',5),'Il est plus long de 5 mm, soit 0,5 cm.')],figures={'1':f'regle_{t}.png'})
 if k==2:
  m=2+t;cut=50+25*t;total=100*m;rest=total-cut;piece=F(rest,5)
  return ex(f'Le ruban de décoration — projet {t+1}',f'Un ruban de {m} m sert à décorer une affiche. On coupe {cut} cm, puis on partage le reste en cinq morceaux égaux.',[
   q('Pourquoi faut-il convertir avant de soustraire ?','Mettre les mesures dans une unité commune.','Les mètres et les centimètres sont des unités différentes : soustraire leurs nombres sans conversion donnerait une longueur fausse.','Il faut exprimer les deux longueurs en centimètres.'),
   q('Exprimer la longueur initiale en centimètres.','Un mètre vaut cent centimètres.',eq(f'{m}\\times100',total),f'{total} cm.'),
   q('Quelle longueur reste après la coupe ?','Retirer ce qui est utilisé.',eq(f'{total}-{cut}',rest),f'Il reste {rest} cm.'),
   q('Quelle est la longueur d’un morceau ?','Partager en cinq parts égales.',eq(f'{rest}\\div5',piece),f'Chaque morceau mesure ${n(piece)}$ cm.'),
   q('Vérifier que les cinq morceaux et la coupe reconstituent le ruban.','Additionner toutes les parties.',eq(f'5\\times{n(piece)}+{cut}',total),f'On retrouve {total} cm : le partage est correct.')])
 if k==3:
  L=8+2*t;w=3+t;p=2*(L+w);side=5+t;otherL=side+2;otherw=side-2
  return ex(f'Contours et figures différentes — plan {t+1}',f'Un rectangle mesure {L} cm sur {w} cm. Un carré a des côtés de {side} cm. On compare aussi ce carré à un rectangle de {otherL} cm sur {otherw} cm.',[
   q('Que mesure le périmètre ?','Suivre le bord de la figure.','Faire le tour signifie parcourir tous les côtés, sans mesurer la surface intérieure.','Le périmètre mesure la longueur du contour.'),
   q('Calculer le périmètre du premier rectangle en additionnant ses côtés.','Les côtés opposés ont la même longueur.',eq(f'{L}+{w}+{L}+{w}',p),f'{p} cm.'),
   q('Calculer le périmètre du carré.','Additionner quatre côtés égaux.',eq(f'{side}+{side}+{side}+{side}',4*side),f'{4*side} cm.'),
   q('Calculer le périmètre du second rectangle.','Additionner ses quatre côtés.',eq(f'{otherL}+{otherw}+{otherL}+{otherw}',4*side),f'{4*side} cm.'),
   q('Deux figures de même périmètre sont-elles forcément identiques ?','Utiliser le carré et le second rectangle comme contre-exemple.',f'Le carré et le rectangle ont tous deux un périmètre de {4*side} cm, mais leurs côtés ne sont pas les mêmes.','Non : un même périmètre peut correspondre à des figures différentes.')])
 L=12+2*t;w=8+t;gate=2;p=2*(L+w);fence=p-gate;roll=10;rolls=(fence+9)//10
 return ex(f'Clôture et achat de grillage — jardin {t+1}',f'Un jardin rectangulaire mesure {L} m sur {w} m. Un portail de {gate} m ne reçoit pas de grillage. Le grillage se vend en rouleaux de 10 m.',[
  q('Calculer la longueur du contour du jardin.','Additionner les quatre côtés.',eq(f'{L}+{w}+{L}+{w}',p),f'{p} m.'),
  q('Combien de mètres de grillage sont nécessaires ?','Retirer la largeur du portail.',eq(f'{p}-{gate}',fence),f'{fence} m de grillage.'),
  q('Combien de rouleaux entiers faut-il acheter au minimum ?','Chercher le premier multiple de 10 suffisant.',f'{rolls-1} rouleaux donnent {(rolls-1)*10} m, ce qui est insuffisant. {rolls} rouleaux donnent {rolls*10} m.',f'Il faut {rolls} rouleaux.'),
  q('Quelle longueur restera après la pose ?','Retirer le besoin de la longueur achetée.',eq(f'{rolls*10}-{fence}',rolls*10-fence),f'Il restera {rolls*10-fence} m.'),
  q('Quelle longueur de grillage faudrait-il pour deux jardins identiques, chacun avec son portail ?','Doubler le besoin d’un jardin, sans ajouter de grillage au portail.',eq(f'2\\times{fence}',2*fence),f'Il faudrait {2*fence} m de grillage.')])

def masses(t,k):
 if k==0:
  kg=2+t;g=250+50*t
  return ex(f'Choisir, convertir et comparer — balance {t+1}',f'Un sac pèse {kg} kg et un paquet pèse {g} g.',[
   q('Quelles unités choisir pour une gomme et un camion chargé ?','Adapter l’unité à la masse.','Une gomme pèse quelques grammes ; un camion chargé pèse plusieurs tonnes.','Grammes pour la gomme ; tonnes pour le camion.'),
   q('Convertir la masse du sac en grammes.','Un kilogramme contient mille grammes.',eq(f'{kg}\\times1000',kg*1000),f'{kg*1000} g.'),
   q('Quelle est la masse totale en grammes ?','Additionner dans la même unité.',eq(f'{kg*1000}+{g}',kg*1000+g),f'{kg*1000+g} g.'),
   q('Donner cette masse en kilogrammes.','Regrouper les grammes par mille.',f'{g} g = ${n(F(g,1000))}$ kg. On ajoute {kg} kg.',f'${n(F(kg*1000+g,1000))}$ kg.'),
   q('Un kilogramme de plumes est-il plus lourd qu’un kilogramme de plomb ?','Comparer les masses et non le volume occupé.','Les deux lots ont une masse de 1 kg. Les plumes prennent davantage de place, mais la masse annoncée est identique.','Non, les deux masses sont égales.')])
 if k==1:
  hL=3+t;used=120+30*t;total=100*hL;rest=total-used
  return ex(f'La citerne et les unités de contenance — école {t+1}',f'Une citerne contient {hL} hL d’eau. On utilise {used} L pour arroser.',[
   q('Quelle grandeur mesure-t-on et quelle unité choisir pour une cuillère ?','Distinguer contenance et masse.','La quantité qu’un récipient peut contenir est sa contenance. Une cuillère contient quelques millilitres.','On mesure une contenance ; on choisit les millilitres pour la cuillère.'),
   q('Convertir la contenance initiale en litres.','Un hectolitre contient cent litres.',eq(f'{hL}\\times100',total),f'{total} L.'),
   q('Combien de litres restent ?','Retirer l’eau utilisée.',eq(f'{total}-{used}',rest),f'{rest} L.'),
   q('Exprimer le reste en centilitres.','Un litre contient cent centilitres.',eq(f'{rest}\\times100',rest*100),f'{rest*100} cL.'),
   q('Un élève écrit « 1 L = 10 mL ». Corriger et expliquer.','Passer du litre au centilitre puis au millilitre.','1 L = 100 cL et 1 cL = 10 mL : 100 groupes de 10 mL font 1 000 mL.','1 L = 1 000 mL.')])
 if k==2:
  large=500+100*t;medium=200;small=50;mass=large+medium+small;pack=1000
  return ex(f'La balance et la recette — préparation {t+1}',f'Une balance est en équilibre : un sac à gauche et des masses de {large} g, {medium} g et {small} g à droite. Une recette utilise 250 g de farine ; on veut en préparer le double avec un paquet de 1 kg.',[
   q('Calculer la masse du sac.','À l’équilibre, les masses des deux plateaux sont égales.',eq(f'{large}+{medium}+{small}',mass),f'Le sac pèse {mass} g.'),
   q('Combien manque-t-il au sac pour atteindre 1 kg ?','Convertir un kilogramme puis chercher le complément.',eq(f'1000-{mass}',1000-mass),f'Il manque {1000-mass} g.'),
   q('Combien de farine faut-il pour doubler la recette ?','Deux recettes demandent deux fois la même masse.',eq(r'2\times250',500),'Il faut 500 g.'),
   q('Quelle masse restera dans le paquet ?','Retirer la masse utilisée du kilogramme.',eq('1000-500',500),'Il restera 500 g.'),
   q('Pourquoi 500 mg ne remplacent-ils pas 500 g dans la recette ?','Utiliser la relation entre gramme et milligramme.','1 g = 1 000 mg. Ainsi 500 mg représentent seulement un demi-gramme, bien moins que 500 g.','500 mg et 500 g représentent des masses différentes.')])
 if k==3:
  bottles=6+2*t;cl=25;total=bottles*cl;used=bottles-2
  return ex(f'Le goûter et les verres — groupe {t+1}',f'Une carafe contient {n(F(total,100))} L de jus. Chaque verre reçoit {cl} cL. Après le service, {used} verres ont été remplis.',[
   q('Convertir la contenance initiale en centilitres.','Un litre contient cent centilitres.',eq(f'{n(F(total,100))}\\times100',total),f'{total} cL.'),
   q('Combien de verres peut-on remplir au total ?','Chercher combien de groupes de 25 cL sont possibles.',eq(f'{total}\\div25',bottles),f'{bottles} verres.'),
   q('Quelle contenance a été servie ?','Multiplier la contenance d’un verre par le nombre servi.',eq(f'{used}\\times25',used*25),f'{used*25} cL.'),
   q('Combien de jus reste-t-il, en litres ?','Soustraire en centilitres puis convertir.',[eq(f'{total}-{used*25}',50),'50 cL = 0,5 L.'],'Il reste 0,5 L.'),
   q('La cantine reçoit 3 packs de 6 briques de 1 L puis utilise 15 L. Combien reste-t-il ?','Calculer le stock avant de retirer la consommation.',[eq(r'3\times6',18),eq('18-15',3)],'Il reste 3 L de lait.')])
 limit=300+50*t;people=4;each=72+5*t;parcel=15;mass=people*each+parcel;jam=2400+300*t;pots=mass//1
 return ex(f'Charge maximale et partage — contrôle {t+1}',f'Un ascenseur accepte {limit} kg au maximum. Quatre personnes de {each} kg montent avec un colis de {parcel} kg. À la cuisine, on dispose aussi de {n(F(jam,1000))} kg de confiture pour des pots de 300 g.',[
  q('Calculer la masse des quatre personnes.','Additionner quatre masses égales.',eq(f'4\\times{each}',4*each),f'{4*each} kg.'),
  q('Calculer la masse totale dans l’ascenseur.','Ajouter le colis.',eq(f'{4*each}+15',mass),f'{mass} kg.'),
  q('La charge est-elle autorisée ?','Comparer avec la limite.',f'{mass} kg '+('dépasse' if mass>limit else 'ne dépasse pas')+f' {limit} kg.',('Non, la charge dépasse la limite.' if mass>limit else 'Oui, la charge respecte la limite.')),
  q('Convertir la confiture en grammes.','Un kilogramme vaut mille grammes.',eq(f'{n(F(jam,1000))}\\times1000',jam),f'{jam} g.'),
  q('Combien de pots pleins peut-on préparer ?','Partager la masse en groupes de 300 g.',eq(f'{jam}\\div300',F(jam,300)),f'{jam//300} pots de 300 g.')])

def time(m):return f'{m//60} h {m%60:02} min'
def durees(t,k):
 if k==0:
  h=8+t;m=20+10*t;instant=60*h+m
  return ex(f'Lire et placer les aiguilles — cadran {t+1}',f'L’horloge dessinée indique une heure du matin. La petite aiguille est entre {h} et {h+1} ; la grande indique {m} minutes.\n\n[IMAGE_1]',[
   q('Quelle aiguille indique les heures ?','Comparer la longueur des aiguilles.','La petite aiguille montre les heures ; la grande parcourt les graduations des minutes.','La petite aiguille indique les heures.'),
   q('Quelle heure est-il le matin ?','Lire l’heure dépassée puis les minutes.',f'La petite aiguille a dépassé {h}, et la grande indique {m} minutes.',f'Il est {time(instant)}.'),
   q('Quelle heure du soir aurait la même position des aiguilles ?','Ajouter douze heures à l’heure du matin.',eq(f'{h}+12',h+12),f'{time(instant+720)}.'),
   q('Combien de minutes reste-t-il avant l’heure suivante ?','Chercher le complément à soixante.',eq(f'60-{m}',60-m),f'Il reste {60-m} min.'),
   q('Où placer les aiguilles quinze minutes plus tard ?','Avancer la grande aiguille de trois nombres du cadran.',f'{m}+15={m+15} minutes. La petite aiguille avance aussi progressivement.',f'Elles indiquent {time(instant+15)}.')],figures={'1':f'horloge_{t}.png'})
 if k==1:
  minutes=95+25*t;h,r=divmod(minutes,60);other=120+5*t
  return ex(f'Convertir et comparer des durées — séance {t+1}',f'Ana travaille pendant {minutes} min. Bob travaille pendant {time(other)}.',[
   q('Combien de minutes contient une heure ?','Retenir la relation de base.','La grande aiguille fait un tour en 60 minutes, soit une heure.','1 h = 60 min.'),
   q('Exprimer la durée d’Ana en heures et minutes.','Former des groupes de soixante.',eq(f'{h}\\times60+{r}',minutes),f'{h} h {r} min.'),
   q('Exprimer la durée de Bob en minutes.','Convertir les heures puis ajouter les minutes.',eq(f'{other//60}\\times60+{other%60}',other),f'{other} min.'),
   q('Qui travaille le plus longtemps et de combien ?','Comparer les durées dans la même unité.',eq(f'{max(minutes,other)}-{min(minutes,other)}',abs(minutes-other)),f'{"Ana" if minutes>other else "Bob"} travaille {abs(minutes-other)} min de plus.'),
   q('Pourquoi 1 h 30 min ne s’écrit-il pas 1,30 h ?','Une heure se partage en soixante minutes.','30 minutes représentent la moitié de 60 minutes : une heure et demie vaut 1,5 h. L’écriture 1,30 h ne code pas 30 minutes.','1 h 30 min = 1,5 h.')])
 if k==2:
  start=9*60+40+5*t;end=11*60+15+10*t;first=60-start%60;dur=end-start
  return ex(f'Le trajet et l’heure d’arrivée — voyage {t+1}',f'Un train part à {time(start)} et arrive à {time(end)}.',[
   q('Combien de minutes séparent le départ de 10 h ?','Avancer jusqu’à l’heure ronde.',eq(f'60-{start%60}',first),f'{first} min.'),
   q('Quelle durée sépare 10 h de l’arrivée ?','Compter l’heure entière puis les minutes.',f'De 10 h à 11 h : 60 min ; puis {end%60} min.',f'{60+end%60} min.'),
   q('Quelle est la durée totale du trajet ?','Additionner les étapes.',eq(f'{first}+{60+end%60}',dur),f'{dur//60} h {dur%60} min.'),
   q('Le même trajet commence à 14 h. Quand finit-il ?','Ajouter la durée à l’horaire de départ.',f'14 h + {dur//60} h {dur%60} min = {time(14*60+dur)}.',f'Il finit à {time(14*60+dur)}.'),
   q('Pour arriver à 18 h par ce train, à quelle heure faudrait-il partir ?','Reculer de la durée du trajet.',f'On retire {dur//60} h puis {dur%60} min à 18 h.',f'Il faudrait partir à {time(18*60-dur)}.')])
 if k==3:
  start=14*60+50+5*t;dur=105+10*t;end=start+dur;early=15
  return ex(f'Le cinéma et le rendez-vous — sortie {t+1}',f'Un film commence à {time(start)} et dure {dur} min. La classe doit être sur place 15 min avant le début ; son trajet dure 30 min.',[
   q('Exprimer la durée du film en heures et minutes.','Regrouper les minutes par soixante.',eq(f'{dur//60}\\times60+{dur%60}',dur),f'{dur//60} h {dur%60:02} min.'),
   q('À quelle heure le film se termine-t-il ?','Avancer d’une heure puis du reste des minutes.',f'Après une heure, il est {time(start+60)} ; en ajoutant {dur-60} min, on atteint {time(end)}.',f'À {time(end)}.'),
   q('À quelle heure faut-il être sur place ?','Retirer la marge avant le début.',f'{time(start)} moins 15 min donne {time(start-15)}.',f'À {time(start-15)}.'),
   q('À quelle heure la classe doit-elle partir ?','Reculer encore de la durée du trajet.',f'{time(start-15)} moins 30 min donne {time(start-45)}.',f'À {time(start-45)}.'),
   q('Pourquoi ne faut-il pas retirer la marge à la durée du film ?','Identifier ce que concerne chaque durée.','La marge sert à arriver avant la séance ; elle ne raccourcit pas la projection. Le trajet et la marge se placent avant l’heure de début.','La durée du film reste identique ; la marge agit sur l’heure de départ.')])
 interval=20+5*t;first=7*60;end=first+3*interval;departures=[first+i*interval for i in range(4)];cooking=55+t*5;oven=17*60+40;removed=oven+cooking-5
 return ex(f'Horaires réguliers et cuisson — planning {t+1}',f'Un bus part toutes les {interval} min à partir de 7 h. On observe les départs jusqu’à {time(end)}, inclus. Un gâteau enfourné à 17 h 40 doit cuire {cooking} min ; il est sorti à {time(removed)}.',[
  q('Écrire les quatre horaires de bus.','Ajouter toujours le même intervalle.',f'On ajoute {interval} min après chaque départ.',', '.join(time(x) for x in departures)+'.'),
  q('Combien d’intervalles séparent le premier et le quatrième départ ?','Distinguer les horaires et les écarts.','Entre quatre horaires successifs, on trouve trois espaces.','Il y a 3 intervalles.'),
  q('Quelle durée sépare ces deux départs ?','Additionner trois intervalles égaux.',eq(f'3\\times{interval}',3*interval),f'{3*interval} min.'),
  q('Combien de temps le gâteau est-il resté dans le four ?','Avancer de l’enfournement à la sortie.',f'De 17 h 40 à {time(removed)}, il s’écoule {cooking-5} min.',f'{cooking-5} min.'),
  q('Le temps de cuisson a-t-il été respecté ?','Comparer avec le temps demandé.',eq(f'{cooking}-{cooking-5}',5),'Non : il manque 5 min de cuisson.')])

if __name__=='__main__':
 for code,fun in [(11,longueurs),(12,masses),(14,durees)]:write(code,[fun(t,k) for t in range(3) for k in range(5)])
