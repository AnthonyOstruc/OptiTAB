# -*- coding: utf-8 -*-
"""Réécriture pédagogique du lot 6e ; sources exportées jamais modifiées."""
from pathlib import Path
import json,re,shutil
ROOT=Path(__file__).resolve().parent.parent
NUMS=(138,139,146,147,148,149,152)
DATA={n:[] for n in NUMS}
def Q(question,methode,titre,raisonnement,resultat):
    return dict(question=question,methode=methode,titre=titre,raisonnement=raisonnement,resultat=resultat)
def E(n,titre,contexte,questions,retenir,calculs=(),images=()):
    DATA[n].append(dict(titre=titre,contexte=contexte,questions=questions,retenir=retenir,calculs=calculs,images=images))

# Volume = dénombrement de cubes unités : ne pas anticiper les formules du cycle 4.
E(138,'Le cube unité','Un petit cube a une arête de 1 cm. Un assemblage plein est formé de 9 de ces cubes.',[
Q('Quelle unité de volume ce cube représente-t-il ?','Relier la longueur de l’arête à la définition de l’unité.','Définir le centimètre cube','Un cube de 1 cm de côté occupe exactement un centimètre cube.','1 cm³.'),
Q('Quel volume occupe l’assemblage ?','Compter les unités de volume, sans compter les faces.','Additionner les volumes','Les 9 cubes ne se recouvrent pas : chacun apporte 1 cm³.','9 cm³.')], 'Une face se mesure en cm² ; un solide occupe un volume en cm³.', [('9*1',9)])
E(138,'Une couche rectangulaire','Une couche de cubes unités contient 4 rangées de 3 cubes.',[
Q('Combien de cubes contient la couche ?','Compter les mêmes groupes une seule fois.','Passer des rangées au total',r'$$4\times3=12$$','12 cubes.'),
Q('Quel est son volume si chaque cube occupe 1 cm³ ?','Associer un centimètre cube à chaque cube unité.','Interpréter le dénombrement','La couche contient 12 unités de volume.','12 cm³.')], 'Une couche peut être organisée en rangées régulières.', [('4*3',12)])
E(138,'Deux couches identiques','Un bloc plein comporte 2 couches de 6 cubes unités chacune.',[
Q('Combien de cubes contient le bloc ?','Multiplier le contenu d’une couche par le nombre de couches.','Compter les couches',r'$$2\times6=12$$','12 cubes.'),
Q('Quel volume reste-t-il si on retire une couche ?','Retirer une couche entière.','Dénombrer ce qui reste',r'$$12-6=6$$','6 cm³.')], 'Un cube caché compte autant qu’un cube visible.', [('2*6',12),('12-6',6)])
E(138,'Comparer sans se laisser tromper','A contient 14 cubes unités. B contient 12 cubes unités, mais ses cubes sont disposés en une tour plus haute.',[
Q('Quel assemblage a le plus grand volume ?','Comparer les nombres de cubes, pas seulement les hauteurs.','Comparer les dénombrements',r'$14>12$ : la forme ne modifie pas le volume de chaque cube.','A.'),
Q('Quelle est la différence des volumes ?','Soustraire dans la même unité.','Calculer l’écart',r'$$14-12=2$$','2 cm³.')], 'Le plus haut assemblage n’a pas toujours le plus grand volume.', [('14-12',2)])
E(138,'Lire un plan de hauteurs','Les colonnes d’un assemblage sans vide ont les hauteurs suivantes, en cubes. Chaque case est occupée par une pile verticale.\n\n| Position | Gauche | Droite |\n|---|---|---|\n| Rangée arrière | 1 | 2 |\n| Rangée avant | 3 | 1 |',[
Q('Combien y a-t-il de piles ?','Compter les cases du plan, sans additionner encore les hauteurs.','Repérer les emplacements','Deux rangées contiennent chacune deux emplacements.','4 piles.'),
Q('Combien de cubes contient l’assemblage ?','Additionner les hauteurs des piles.','Compter tous les étages',r'$$1+2+3+1=7$$','7 cubes.')], 'Le nombre écrit dans une case est une hauteur, pas un numéro de cube.', [('2*2',4),('1+2+3+1',7)])
E(138,'Voir de face','Le même assemblage a pour hauteurs arrière (1 ; 2) et avant (3 ; 1), de gauche à droite. On regarde de face depuis la rangée avant.',[
Q('Quelle hauteur voit-on dans chaque colonne ?','Dans une même direction de regard, retenir la pile la plus haute.','Comparer les piles alignées','À gauche : le maximum de 1 et 3 vaut 3. À droite : le maximum de 2 et 1 vaut 2.','Hauteurs 3 et 2.'),
Q('Combien de carrés unités comporte cette silhouette ?','Additionner les hauteurs visibles de face.','Compter les carrés de la vue',r'$$3+2=5$$','5 carrés.')], 'Une vue de face ne révèle pas toujours tous les cubes.', [('max(1,3)',3),('max(2,1)',2),('3+2',5)],images=('vues','vues_corrige'))
E(138,'Réorganiser les cubes','On démonte un assemblage de 18 cubes unités pour fabriquer un autre solide avec exactement les mêmes cubes, sans recouvrement.',[
Q('Le volume change-t-il ?','Conserver les unités de volume lors d’un déplacement.','Suivre les mêmes cubes','Aucun cube n’est ajouté ni retiré : le nombre de cm³ ne change pas.','Non : 18 cm³.'),
Q('Peut-on fabriquer deux assemblages de 10 cubes chacun ?','Comparer la quantité nécessaire à la quantité disponible.','Vérifier la réserve',r'$2\times10=20$ cubes seraient nécessaires ; $20>18$.','Non : il manque 2 cubes.')], 'Changer une disposition ne change pas le nombre de cubes.', [('2*10',20),('20-18',2)])
E(138,'Un bloc à trois étages','Chaque couche d’un bloc plein contient 5 rangées de 4 cubes ; il y a 3 couches.',[
Q('Combien de cubes contient une couche ?','Dénombrer les rangées.','Former un étage',r'$$5\times4=20$$','20 cubes.'),
Q('Déterminer le volume du bloc en cm³.','Dénombrer les trois couches identiques.','Empiler les étages',r'$$3\times20=60$$','60 cm³.')], 'Le calcul par couches doit correspondre à un bloc plein, sans trou.', [('5*4',20),('3*20',60)])
E(138,'Retirer une colonne','Un bloc contient 24 cubes unités. On enlève une pile de 3 cubes depuis le dessus, sans déplacer les autres cubes.',[
Q('Quel volume a été retiré ?','Identifier le nombre de cubes enlevés.','Mesurer le retrait','La pile retirée contient trois cubes de 1 cm³.','3 cm³.'),
Q('Quel est le volume restant ?','Soustraire le retrait du volume initial.','Effectuer le bilan',r'$$24-3=21$$','21 cm³.')], 'Le volume retiré se compte dans la même unité que le volume initial.', [('24-3',21)])
E(138,'Compléter un pavé','Un pavé plein aurait 4 rangées de 3 cubes par couche et 2 couches. L’assemblage actuel contient 17 cubes unités.',[
Q('Combien de cubes contiendrait le pavé plein ?','Compter une couche puis les deux couches.','Dénombrer le modèle complet',r'$$\begin{aligned}4\times3&=12\\2\times12&=24\end{aligned}$$','24 cubes.'),
Q('Combien faut-il ajouter de cubes ?','Calculer la différence entre modèle et assemblage.','Compléter les places vides',r'$$24-17=7$$','7 cubes.')], 'Pour compléter, comparer le plein et l’existant ; ne pas additionner leurs volumes.', [('4*3',12),('2*12',24),('24-17',7)])
E(138,'Des couches différentes','Une construction sans chevauchement a trois couches contenant respectivement 12, 8 et 4 cubes unités.',[
Q('Pourquoi ne peut-on pas multiplier 12 par 3 ?','Vérifier que les groupes sont identiques avant de multiplier.','Examiner les couches','La deuxième et la troisième couche ne contiennent pas 12 cubes.','Les couches ont des contenus différents.'),
Q('Quel est le volume total ?','Additionner les contenus des trois couches.','Dénombrer couche par couche',r'$$12+8+4=24$$','24 cm³.')], 'La multiplication par le nombre de couches exige des couches identiques.', [('12+8+4',24)])
E(138,'Deux volumes égaux','A a 3 couches de 8 cubes unités. B a 4 couches de 6 cubes unités.',[
Q('Déterminer le volume de chacun.','Dénombrer les cubes de chaque bloc.','Calculer les deux totaux',r'$$\begin{aligned}3\times8&=24\\4\times6&=24\end{aligned}$$','A et B occupent chacun 24 cm³.'),
Q('Peut-on affirmer qu’ils ont la même forme ?','Distinguer une mesure d’une forme.','Interpréter l’égalité','Le même nombre de cubes peut être organisé de plusieurs façons.','Non.')], 'Deux solides de même volume ne sont pas nécessairement identiques.', [('3*8',24),('4*6',24)])
E(138,'Des cubes invisibles','Un assemblage sans vide a trois piles alignées de hauteurs 3, 1 et 2 cubes. De dessus, on ne voit que le carré supérieur de chaque pile.',[
Q('Combien de cubes y a-t-il ?','Compter les hauteurs, et non les seuls carrés du dessus.','Additionner les piles',r'$$3+1+2=6$$','6 cubes.'),
Q('Combien de cubes n’ont pas leur face supérieure visible ?','Retirer les trois cubes qui sont au sommet des piles.','Séparer sommets et cubes cachés',r'$$6-3=3$$','3 cubes.')], 'Une vue du dessus donne les emplacements occupés, sans indiquer leurs hauteurs.', [('3+1+2',6),('6-3',3)])
E(138,'La vue ne suffit pas','Une vue du dessus montre 4 emplacements occupés. Toutes les piles sont verticales, sans vide, et leur hauteur vaut au plus 3 cubes.',[
Q('Quel est le plus petit nombre possible de cubes ?','Placer au moins un cube par emplacement occupé.','Construire le minimum',r'$$4\times1=4$$','4 cubes.'),
Q('Quel est le plus grand nombre possible ?','Remplir chaque pile jusqu’à la hauteur autorisée.','Construire le maximum',r'$$4\times3=12$$','12 cubes.')], 'Une même empreinte au sol peut correspondre à plusieurs volumes.', [('4*1',4),('4*3',12)])
E(138,'Une réserve pour construire','Une boîte contient 50 cubes unités. On construit deux blocs de 3 couches de 6 cubes chacun.',[
Q('Combien de cubes utilise-t-on ?','Calculer un bloc, puis deux blocs.','Dénombrer les constructions',r'$$\begin{aligned}3\times6&=18\\2\times18&=36\end{aligned}$$','36 cubes.'),
Q('Peut-on encore construire un bloc identique ?','Comparer la réserve au contenu d’un bloc.','Examiner le reste',r'$50-36=14$ et $14<18$.','Non : il manque 4 cubes.')], 'Un problème de réserve nécessite le bilan après toutes les constructions.', [('3*6',18),('2*18',36),('50-36',14),('18-14',4)])
E(138,'Un escalier de cubes','Une rangée d’escalier est formée de piles de hauteurs 1, 2, 3 et 4 cubes. Deux rangées identiques sont juxtaposées, sans chevauchement.',[
Q('Combien de cubes contient une rangée ?','Additionner les hauteurs successives.','Dénombrer les marches',r'$$1+2+3+4=10$$','10 cubes.'),
Q('Quel volume occupent les deux rangées ?','Doubler le contenu de la rangée.','Assembler les deux rangées',r'$$2\times10=20$$','20 cm³.')], 'La marche la plus haute ne résume pas tout l’escalier.', [('1+2+3+4',10),('2*10',20)])
E(138,'Un trou traversant','Un bloc plein comporte 3 couches de 4 rangées de 3 cubes unités. On enlève une pile verticale de 3 cubes pour faire un trou du haut jusqu’en bas.',[
Q('Quel était le volume initial ?','Dénombrer le plein avant le retrait.','Compter les couches',r'$$\begin{aligned}4\times3&=12\\3\times12&=36\end{aligned}$$','36 cm³.'),
Q('Quel volume reste-t-il ?','Retirer les cubes du trou une seule fois.','Mesurer le solide troué',r'$$36-3=33$$','33 cm³.')], 'Un vide n’apporte aucun volume de matière.', [('4*3',12),('3*12',36),('36-3',33)])
E(138,'Reconstruire d’après deux vues','Trois piles sans vide sont alignées côte à côte. De face, on lit les hauteurs 2, 4 et 1. De dessus, les trois emplacements sont occupés et aucune autre pile n’existe.',[
Q('Déterminer le nombre exact de cubes.','Exploiter l’information qui donne les hauteurs.','Reconstituer les trois piles',r'$$2+4+1=7$$','7 cubes.'),
Q('Combien en ajouter pour obtenir trois piles de hauteur 4 ?','Calculer les manques de chaque pile.','Compléter la silhouette',r'$$\begin{aligned}(4-2)+(4-4)+(4-1)&=2+0+3\\&=5\end{aligned}$$','5 cubes.')], 'Une reconstruction doit satisfaire simultanément toutes les vues.', [('2+4+1',7),('(4-2)+(4-4)+(4-1)',5)])
E(138,'Changer d’unité de cube','Un grand cube de 2 cm d’arête est rempli de petits cubes de 1 cm d’arête, sans vide.',[
Q('Combien de petits cubes contient une couche ?','Placer deux rangées de deux cubes.','Paver une couche',r'$$2\times2=4$$','4 cubes.'),
Q('Quel volume occupe le grand cube ?','Empiler les deux couches de petits cubes.','Compter les unités de 1 cm³',r'$$2\times4=8$$','8 cm³, et non 2 cm³.')], 'L’arête de 2 cm ne signifie pas un volume de 2 cm³.', [('2*2',4),('2*4',8)])
E(138,'Ajouter un cube sans changer la face','Les hauteurs de l’assemblage sont arrière (1 ; 2), avant (3 ; 1), de gauche à droite. On ajoute un cube sur la pile arrière gauche.',[
Q('Quel devient le volume ?','Actualiser la somme des hauteurs.','Compter après ajout',r'$$2+2+3+1=8$$','8 cm³.'),
Q('La vue de face depuis l’avant change-t-elle ?','Comparer les maxima dans chaque colonne.','Tester les hauteurs visibles','À gauche, la pile avant de hauteur 3 masque encore celle de hauteur 2. À droite, rien ne change.','Non : les hauteurs visibles restent 3 et 2.')], 'Le volume peut augmenter sans modifier une vue donnée.', [('2+2+3+1',8),('max(2,3)',3),('max(2,1)',2)])
E(138,'Le défi des 24 cubes','On dispose de 24 cubes unités. Une couche doit être un rectangle de 4 rangées de 3 cubes.',[
Q('Combien de couches complètes peut-on fabriquer ?','Calculer le contenu d’une couche puis partager la réserve.','Organiser les cubes',r'$$\begin{aligned}4\times3&=12\\24\div12&=2\end{aligned}$$','2 couches.'),
Q('Peut-on faire 3 couches identiques en gardant cette base ?','Comparer le besoin à la réserve.','Vérifier une proposition',r'$3\times12=36$ ; il manque $36-24=12$ cubes.','Non.')], 'La quantité de cubes limite les dimensions possibles de l’assemblage.', [('4*3',12),('24/12',2),('3*12',36),('36-24',12)])

# Horaires : lecture, base 60, calculs inverses, calendrier et contraintes.
E(139,'Instant ou durée','Une affiche indique « départ à 8 h 20 ; trajet de 45 min ; arrivée à 9 h 05 ».',[
Q('Quels renseignements sont des horaires ?','Un horaire repère un instant.','Distinguer les rôles','Le départ et l’arrivée désignent des moments précis de la journée.','8 h 20 et 9 h 05.'),
Q('Quel renseignement est une durée ?','Une durée mesure le temps écoulé.','Identifier l’intervalle','Le trajet sépare les deux instants.','45 min.')], 'Un horaire répond à « quand ? » ; une durée à « combien de temps ? ».')
E(139,'Minutes et secondes','On chronomètre une course de 2 min 15 s.',[
Q('Exprimer la durée en secondes.','Remplacer chaque minute par 60 secondes.','Convertir puis additionner',r'$$\begin{aligned}2\times60&=120\\120+15&=135\end{aligned}$$','135 s.'),
Q('Exprimer 150 s en minutes et secondes.','Séparer des groupes de 60 secondes et le reste.','Décomposer la durée',r'$150=2\times60+30$.','2 min 30 s.')], 'Une minute vaut 60 secondes, pas 100.', [('2*60+15',135),('2*60+30',150)])
E(139,'De l’après-midi au soir','Une horloge à aiguilles indique 3 h 25 après midi.',[
Q('Donner l’horaire sur un affichage de 24 heures.','Ajouter 12 heures pour l’après-midi.','Changer la convention',r'$$3+12=15$$','15 h 25.'),
Q('Où se trouvent les aiguilles ?','La grande aiguille compte les minutes ; la petite avance entre deux heures.','Situer les deux aiguilles','La grande aiguille pointe le 5, car chaque intervalle représente 5 min. La petite se trouve entre 3 et 4, un peu avant le milieu.','Grande : sur 5 ; petite : entre 3 et 4.')], 'La petite aiguille ne reste pas immobile sur 3 pendant toute l’heure.', [('3+12',15),('5*5',25)],images=('horloge_1525',))
E(139,'Passer l’heure suivante','Une séance commence à 10 h 45 et dure 35 min.',[
Q('Combien de temps reste-t-il jusqu’à 11 h ?','Compléter jusqu’à 60 minutes.','Atteindre l’heure ronde',r'$$60-45=15$$','15 min.'),
Q('À quelle heure la séance finit-elle ?','Utiliser le complément puis le temps restant.','Finir le déplacement dans le temps',r'$35-15=20$ min restent après 11 h.','11 h 20.')], 'Décomposer au passage d’une heure évite de traiter les minutes en base 100.', [('60-45',15),('35-15',20)])
E(139,'Mesurer un intervalle','Un atelier a lieu de 14 h 15 à 15 h 05 le même jour.',[
Q('Calculer sa durée en minutes.','Passer par l’heure ronde.','Additionner deux intervalles',r'$$\begin{aligned}60-15&=45\\45+5&=50\end{aligned}$$','50 min.'),
Q('Peut-on écrire 0 h 90 min pour cette durée ?','Comparer les durées dans une même unité.','Contrôler l’écriture','90 min dépassent une heure, alors que l’atelier dure moins d’une heure.','Non.')], 'Une durée doit être cohérente avec les horaires de départ et d’arrivée.', [('60-15+5',50)])
E(139,'Les fractions d’heure','On travaille avec une demi-heure, un quart d’heure et trois quarts d’heure.',[
Q('Exprimer ces trois durées en minutes.','Partager 60 minutes en parts égales.','Utiliser les fractions usuelles',r'$$\begin{aligned}60\div2&=30\\60\div4&=15\\3\times15&=45\end{aligned}$$','30 min ; 15 min ; 45 min.'),
Q('Combien dure une demi-heure suivie d’un quart d’heure ?','Additionner les minutes.','Réunir les intervalles',r'$$30+15=45$$','45 min.')], 'Un quart d’heure vaut 15 minutes.', [('60/2',30),('60/4',15),('3*15',45),('30+15',45)])
E(139,'Lire une horloge à secondes','L’horloge indique 10 h 10 min 30 s.',[
Q('Où pointent la grande aiguille et la trotteuse ?','Compter 5 minutes ou 5 secondes entre deux nombres successifs.','Lire les graduations','10 minutes correspondent au nombre 2 ; 30 secondes correspondent au nombre 6.','Grande aiguille : 2 ; trotteuse : 6.'),
Q('Quel horaire indique-t-elle 30 secondes plus tard ?','Compléter la minute en cours.','Passer à la minute suivante',r'$30+30=60$ secondes forment une minute.','10 h 11 min 00 s.')], 'La grande aiguille et la trotteuse n’indiquent pas la même unité.', [('2*5',10),('6*5',30),('30+30',60)])
E(139,'Une heure et demie en décimal','Une activité dure 1 h 30 min.',[
Q('Exprimer cette durée en heures décimales.','Diviser les minutes par 60 avant de les ajouter aux heures.','Convertir la partie en minutes',r'$$\begin{aligned}30\div60&=0{,}5\\1+0{,}5&=1{,}5\end{aligned}$$','1,5 h.'),
Q('Pourquoi 1,30 h est-il une écriture incorrecte de cette durée ?','Convertir les dixièmes et centièmes d’heure en minutes.','Tester l’autre écriture',r'$0{,}30\times60=18$ min ; 1,30 h vaut 1 h 18 min.','1,30 h ne vaut pas 1 h 30 min.')], 'La virgule décimale ne sépare pas des heures et des minutes.', [('30/60',0.5),('1+0.5',1.5),('0.30*60',18)])
E(139,'Trois quarts d’heure en décimal','Un fichier de suivi indique une durée de 2,75 h.',[
Q('Convertir la partie décimale en minutes.','Multiplier la fraction d’heure par 60.','Mesurer les 0,75 heure',r'$$0{,}75\times60=45$$','45 min.'),
Q('Donner la durée en heures et minutes, puis en minutes seules.','Conserver les deux heures entières.','Assembler puis convertir',r'$$2\times60+45=165$$','2 h 45 min, soit 165 min.')], '2,75 h ne se lit pas « 2 heures 75 minutes ».', [('0.75*60',45),('2*60+45',165)])
E(139,'Retrouver le départ','Un train arrive à 17 h 10 après 1 h 45 de trajet.',[
Q('À quelle heure est-il parti ?','Remonter le temps en retirant d’abord une heure puis 45 minutes.','Calculer à rebours','17 h 10 moins 1 h donne 16 h 10 ; retirer 10 min mène à 16 h, puis 35 min mène à 15 h 25.','15 h 25.'),
Q('Vérifier avec une addition.','Repartir de l’horaire trouvé.','Revenir vers l’arrivée','15 h 25 + 1 h donne 16 h 25 ; + 45 min donne 17 h 10.','L’horaire de départ est vérifié.')], 'Une vérification dans le sens direct permet de contrôler un calcul inverse.', [('17*60+10-(60+45)',15*60+25)])
E(139,'Ajouter des durées','Un trajet dure 1 h 48 min à l’aller et 1 h 37 min au retour.',[
Q('Calculer la durée totale.','Regrouper les heures et les minutes, puis convertir 60 minutes.','Normaliser la somme',r'$48+37=85$ min, soit 1 h 25 min. Les deux heures initiales donnent donc 3 h 25 min.','3 h 25 min.'),
Q('Exprimer ce total en minutes.','Remplacer chaque heure par 60 minutes.','Changer d’unité',r'$$3\times60+25=205$$','205 min.')], 'Après une addition, ramener le nombre de minutes sous 60.', [('48+37',85),('(60+48)+(60+37)',205),('3*60+25',205)])
E(139,'Franchir minuit','Un film commence à 23 h 35 et finit à 0 h 20 le lendemain.',[
Q('Combien de temps s’écoule avant minuit ?','Compléter jusqu’à 24 h.','Atteindre le changement de jour',r'$$60-35=25$$','25 min.'),
Q('Quelle est la durée du film ?','Ajouter les minutes avant et après minuit.','Additionner les deux parties',r'$$25+20=45$$','45 min.')], 'Après minuit, l’horaire repart à 0 h mais le temps continue de s’écouler.', [('60-35',25),('25+20',45)],images=('minuit','minuit_corrige'))
E(139,'Comparer des chronos','Deux coureurs réalisent 3 min 08 s et 192 s.',[
Q('Convertir le premier temps en secondes.','Utiliser la même unité pour comparer.','Calculer le temps de référence',r'$$3\times60+8=188$$','188 s.'),
Q('Qui est le plus rapide et de combien ?','La plus petite durée correspond au plus rapide.','Mesurer l’écart',r'$188<192$ et $192-188=4$.','Le premier coureur, de 4 s.')], 'En course, une durée plus petite signifie une arrivée plus rapide.', [('3*60+8',188),('192-188',4)])
E(139,'Un calendrier','L’année 2024 compte 366 jours ; l’année 2025 en compte 365. Une semaine dure 7 jours.',[
Q('Quel est l’écart entre les deux années ?','Soustraire les nombres de jours.','Comparer les durées',r'$$366-365=1$$','1 jour.'),
Q('Décomposer 365 jours en semaines entières et jours restants.','Chercher des groupes de 7.','Effectuer une division avec reste',r'$$365=52\times7+1$$','52 semaines et 1 jour.')], 'Un siècle contient 100 ans ; un millénaire en contient 1 000.', [('366-365',1),('52*7+1',365)])
E(139,'Une correspondance possible ?','Un train arrive à 10 h 48. Le second part à 11 h 02. Il faut 12 min pour changer de quai.',[
Q('Combien de minutes séparent les trains ?','Passer par 11 h.','Calculer le temps disponible',r'$$12+2=14$$','14 min.'),
Q('La correspondance est-elle possible si le premier train a 4 min de retard ?','Retirer le retard puis comparer au temps de changement.','Tester la marge',r'$14-4=10$ et $10<12$.','Non : il manque 2 min.')], 'Un retard réduit le temps disponible pour la correspondance.', [('12+2',14),('14-4',10),('12-10',2)])
E(139,'Un enregistrement complet','Une émission dure 48 min 35 s. La mémoire disponible permet 50 min d’enregistrement.',[
Q('Combien de secondes de mémoire restent après l’émission ?','Convertir les deux durées en secondes.','Calculer la différence',r'$$\begin{aligned}50\times60&=3000\\48\times60+35&=2915\\3000-2915&=85\end{aligned}$$','85 s.'),
Q('Peut-on enregistrer en plus un message de 1 min 30 s ?','Comparer les secondes nécessaires et disponibles.','Vérifier la capacité',r'$1\times60+30=90$ s et $90>85$.','Non : il manque 5 s.')], 'Pour comparer des durées avec secondes, une conversion commune simplifie le contrôle.', [('50*60',3000),('48*60+35',2915),('3000-2915',85),('60+30',90),('90-85',5)])
E(139,'Finir avant la fermeture','La bibliothèque ferme à 18 h. Lina y arrive à 16 h 25 et veut travailler 1,5 h.',[
Q('À quelle heure termine-t-elle ?','Convertir la durée décimale puis l’ajouter à l’arrivée.','Calculer la fin','1,5 h vaut 1 h 30 min. 16 h 25 + 1 h 30 min donne 17 h 55.','17 h 55.'),
Q('Quelle marge lui reste-t-il avant la fermeture ?','Comparer la fin à l’heure limite.','Mesurer le temps restant',r'$$60-55=5$$','5 min.')], 'Toujours convertir une durée décimale avant de l’ajouter à un horaire.', [('0.5*60',30),('16*60+25+90',17*60+55),('60-55',5)])
E(139,'Une journée organisée','Un groupe part à 8 h 35. Le trajet dure 50 min, puis une pause de 20 min précède une visite de 1 h 30 min.',[
Q('À quelle heure commence la visite ?','Enchaîner les deux premières durées.','Suivre le planning','L’arrivée a lieu à 9 h 25 ; après 20 min de pause, la visite commence à 9 h 45.','9 h 45.'),
Q('À quelle heure finit-elle et combien de temps s’est écoulé depuis le départ ?','Ajouter la visite puis totaliser toutes les durées.','Contrôler le programme',r'La fin est à 11 h 15. $50+20+90=160$ min, soit 2 h 40 min.','11 h 15 ; 2 h 40 min.')], 'Les pauses font partie du temps écoulé même si elles ne sont pas du transport.', [('8*60+35+50+20',9*60+45),('50+20+90',160)])
E(139,'Répartir une répétition','Une répétition dure 2 h. Elle comporte 15 min d’installation, trois passages de 25 min et une pause de 10 min.',[
Q('Quelle durée est déjà utilisée ?','Additionner l’installation, les passages et la pause.','Établir le bilan',r'$$15+3\times25+10=100$$','100 min.'),
Q('Quelle durée reste pour le rangement ?','Convertir deux heures puis retirer le temps utilisé.','Calculer le temps disponible',r'$$120-100=20$$','20 min.')], 'Une répétition d’activités identiques se calcule par multiplication.', [('15+3*25+10',100),('120-100',20)])
E(139,'Des temps exprimés autrement','A dure 1,2 h ; B dure 1 h 15 min ; C dure 4 500 s.',[
Q('Exprimer les trois durées en minutes.','Choisir une même unité.','Convertir séparément',r'$$\begin{aligned}1{,}2\times60&=72\\60+15&=75\\4500\div60&=75\end{aligned}$$','A : 72 min ; B : 75 min ; C : 75 min.'),
Q('Classer les trois durées.','Comparer les mesures converties.','Ordonner les résultats',r'$72<75$ ; B et C sont égales.','A < B = C.')], 'Des écritures différentes peuvent désigner exactement la même durée.', [('1.2*60',72),('60+15',75),('4500/60',75)])
E(139,'Choisir le bon départ','Une sortie doit arriver avant 14 h 30. Le trajet prend 1 h 20, mais on prévoit 15 min de marge. Les départs possibles sont 12 h 40 ou 13 h.',[
Q('Quel est l’horaire de départ le plus tardif avec la marge ?','Retirer le trajet et la marge de l’heure limite.','Reculer depuis l’échéance','14 h 30 moins 1 h 20 donne 13 h 10 ; moins 15 min donne 12 h 55.','12 h 55.'),
Q('Quel départ faut-il choisir ?','Retenir un départ qui précède l’horaire maximal.','Appliquer la contrainte','12 h 40 précède 12 h 55 ; 13 h dépasse cette limite.','12 h 40.')], 'Prévoir une marge revient à partir plus tôt, pas plus tard.', [('14*60+30-80-15',12*60+55)])

def finaliser():
    for n in NUMS:
        d=next(ROOT.glob(f'{n}_*')); sauvegarde=d/'sauvegardes'/'avant_refonte_2026-10-30'
        if not sauvegarde.exists():
            sauvegarde.mkdir(parents=True)
            for f in d.iterdir():
                if f.is_file():shutil.copy2(f,sauvegarde/f.name)
        meta=json.loads((d/'source_en_ligne'/'meta.json').read_text(encoding='utf8'))
        ids=[str(e['id']) for e in meta['exercices']]
        assert len(DATA[n])==21,(n,len(DATA[n]))
        if not ids:ids=[f'nouveau-{i+1}' for i in range(21)]
        assert len(ids)==21
        blocs=[];cor={'cours':{},'fiches':{},'exercices':{}}
        for i,(ident,e) in enumerate(zip(ids,DATA[n])):
            level=i//7;prefix=('Découverte','Entraînement','Problème')[level]
            en=e['contexte']+'\n\n'+('\n\n'.join(f'[IMAGE_{j+1}]' for j,_ in enumerate(e['images'][:1])))
            en+='\n\n'+'\n'.join(f'{k}. '+q['question'] for k,q in enumerate(e['questions'],1))
            steps=[]
            for k,q in enumerate(e['questions'],1):
                steps.append(f"## Question {k} : {q['question']}\n\n::: methode\n{q['methode']}\n:::\n\n::: etape {q['titre']}\n{q['raisonnement']}\n:::\n\n::: resultat\n{q['resultat']}\n:::")
            if len(e['images'])>1:steps.append('[IMAGE_2]')
            steps.append('::: retenir\n'+e['retenir']+'\n:::')
            sol='\n'.join(f"{k}. {q['resultat']}" for k,q in enumerate(e['questions'],1))
            blocs.append(f"=== {prefix} - {i+1}. {e['titre']}\nId: {ident}\nDifficulté: {('easy','medium','hard')[level]}\n\nÉnoncé:\n<!-- optitab:1 -->\n{en.strip()}\n\nÉtapes:\n<!-- optitab:1 -->\n"+'\n\n'.join(steps)+'\n\nSolution:\n<!-- optitab:1 -->\n'+sol+'\n')
            if e['images']:cor['exercices'][ident]={str(j+1):{'fichier':nom+'.png','alt':e['titre']+' : '+nom.replace('_',' ')} for j,nom in enumerate(e['images'])}
        (d/'exercices.txt').write_text('\n\n'.join(blocs),encoding='utf8')
        (d/'manifest_pedagogique.json').write_text(json.dumps(DATA[n],ensure_ascii=False,indent=2),encoding='utf8')
        (d/'figures').mkdir(exist_ok=True)
        (d/'figures'/'correspondance.json').write_text(json.dumps(cor,ensure_ascii=False,indent=2),encoding='utf8')
        (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'donnees_espace','maj':'2026-10-30'},indent=2),encoding='utf8')

if __name__=='__main__':
    exec((Path(__file__).parent/'donnees_suite.py').read_text(encoding='utf8'))
    finaliser()
