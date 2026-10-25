from modele import C,E

C('Lire l’heure à la minute','Temps','P1-P4',
 'Je lis et je place les heures et les minutes sur un cadran.','Horloge à aiguilles manipulables.',
 'Fais avancer la grande aiguille de cinq petites graduations, puis de dix-huit. Observe la petite aiguille : elle avance aussi entre deux heures.',
 ['Un tour de la grande aiguille dure 60 minutes. Entre deux nombres du cadran, il y a 5 minutes.','La petite aiguille indique les heures et avance progressivement vers l’heure suivante.','Je distingue matin et après-midi : 3 h 42 l’après-midi s’écrit 15 h 42.'],
 'À 10 h 35, la grande aiguille est sur 7. La petite est entre 10 et 11. Je peux dire « onze heures moins vingt-cinq ».',('minuteclocks',[[10,35],[15,42]]),
 'Où placer les aiguilles pour 6 h 18 ?','Grande aiguille à la 18e graduation de minute ; petite aiguille un peu après 6.',[
 E('Lis les deux horloges pour le matin.','8 h 20 ; 10 h 35.',('minuteclocks',[[8,20],[10,35]])),
 E('Lis cette heure pour l’après-midi.','15 h 42.',('minuteclocks',[[15,42]])),
 E('Sur une horloge des outils, dessine les aiguilles de 13 h 25.','Grande aiguille sur le 5 ; petite aiguille entre 1 et 2, avant la moitié.'),
 E('Sur une horloge des outils, dessine 6 h 18.','Grande aiguille trois petites graduations après le 3 ; petite aiguille un peu après 6.'),
 E('Écris en heures et minutes : neuf heures moins le quart ; quatre heures moins vingt.','8 h 45 ; 3 h 40.'),
 E('Écris pour l’après-midi ou le soir : deux heures et dix ; sept heures et cinquante.','14 h 10 ; 19 h 50.'),
 E('À 11 h 55, la petite aiguille est-elle sur 11, entre 11 et 12, ou sur 12 ? Explique.','Entre 11 et 12, très près de 12. Elle avance pendant que les minutes passent.'),
 E('Écris en langage courant : 7 h 15 ; 9 h 30 ; 11 h 45.','Sept heures et quart ; neuf heures et demie ; midi moins le quart.'),
 E('Lina place la petite aiguille exactement sur 4 pour 4 h 50. Corrige sa position.','La petite aiguille doit être entre 4 et 5, très près de 5.')],
 'Faire tourner une vraie horloge d’apprentissage pour relier les deux mouvements.',
 'Le cadran seul ne distingue pas matin et après-midi ; le contexte doit le préciser. Midi correspond à 12 h et minuit à 0 h.')

C('Calculer et comparer des durées','Temps','P2-P5',
 'Je trouve une durée, une heure de départ ou une heure d’arrivée.','Frise horaire et ardoise.',
 'Place 8 h 45 et 10 h 10 sur une frise. Passe d’abord par 9 h, puis par 10 h. Réunis les durées sans confondre une heure et 100 minutes.',
 ['Une heure vaut 60 minutes ; 2 h 20 min valent 140 minutes.','Pour chercher une durée, je peux faire des bonds jusqu’à une heure entière puis jusqu’à l’arrivée.','Pour trouver un départ ou une arrivée, j’enlève ou j’ajoute la durée sur une frise.'],
 'De 8 h 45 à 10 h 10 : 15 min, puis 1 h, puis 10 min. Durée totale : 1 h 25 min.',('duration',[525,610]),
 'Une activité commence à 14 h 35 et dure 50 min. À quelle heure se termine-t-elle ?','25 min pour arriver à 15 h, puis 25 min : 15 h 25.',[
 E('Convertis : 2 h 15 min en minutes ; 95 min en heures et minutes.','135 min ; 1 h 35 min.',None,'2*60+15==135 and 95==60+35'),
 E('Compare : 2 h … 130 min ; 1 h 45 min … 100 min.','< ; >. 2 h = 120 min et 1 h 45 min = 105 min.'),
 E('Combien de temps s’écoule entre 9 h 20 et 10 h 05 ?','40 min puis 5 min : 45 min.',None,'605-560==45'),
 E('Une séance va de 13 h 48 à 15 h 12. Quelle est sa durée ?','12 min + 1 h + 12 min = 1 h 24 min.',None,'912-828==84'),
 E('Un film commence à 14 h 35 et dure 1 h 40 min. Quand se termine-t-il ?','16 h 15.',None,'14*60+35+100==16*60+15'),
 E('Une sortie dure 1 h 25 min et se termine à 11 h 10. À quelle heure a-t-elle commencé ?','9 h 45.',None,'11*60+10-85==9*60+45'),
 E('Un train part à 7 h 18. Il roule 1 h 30 min puis encore 42 min. À quelle heure arrive-t-il ?','8 h 48 après la première partie ; 9 h 30 à l’arrivée.',None,'7*60+18+90+42==9*60+30'),
 E('Une visite dure 45 min, puis on marche 25 min. Départ à 10 h 20. Quand les deux activités se terminent-elles ?','Durée totale : 70 min ; fin : 11 h 30.',None,'10*60+20+45+25==11*60+30'),
 E('Noé écrit que de 8 h 50 à 9 h 10 il s’écoule 60 min. Corrige avec une frise.','10 min jusqu’à 9 h, puis 10 min : 20 min.',None,'9*60+10-(8*60+50)==20')],
 'Construire des bonds sur une frise et utiliser 60 jetons pour représenter une heure.',
 'Les situations restent dans une même journée. Les durées se calculent en base 60 et non comme des prix à virgule.')
