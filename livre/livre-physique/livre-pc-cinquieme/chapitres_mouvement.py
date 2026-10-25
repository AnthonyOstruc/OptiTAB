"""Mouvement et interactions : approche descriptive de début de cycle 4."""
from programme_complet import *

C9=Chapitre(9,'Peut-on être immobile et en mouvement à la fois ?',[
    'Préciser l’objet et l’observateur pour décrire un mouvement.',
    'Reconnaître des trajectoires rectilignes, circulaires et curvilignes.',
    'Exploiter des positions relevées à intervalles réguliers.'
],[
Lecon('Le mouvement dépend de l’observateur',
    'Décrire un mouvement demande de choisir l’objet étudié et le repère de l’observateur. Un voyageur assis dans un train est immobile par rapport au siège, mais se déplace par rapport au quai lorsque le train avance. Les deux descriptions sont compatibles. On étudie souvent un point représentatif de l’objet, par exemple le centre d’un ballon ; les autres points peuvent suivre des trajectoires différentes.',
    ('pc_reference',None),'Le voyageur est au repos par rapport au train et en mouvement par rapport au quai.',
    'Il n’existe pas de description complète sans référence à un observateur ou à un repère. Écrire simplement « il bouge » laisse une information essentielle de côté.',
    'Commencer la phrase par « Par rapport à… ». Nommer ensuite l’objet et décrire comment sa position évolue.'),
Lecon('Nommer une trajectoire',
    'La trajectoire est l’ensemble des positions successives du point étudié dans le repère choisi. Elle est rectiligne si ces positions appartiennent à une droite ; circulaire si elles appartiennent à un cercle ; curviligne si elles suivent une courbe. Une trajectoire renseigne sur la forme du chemin, mais pas à elle seule sur la rapidité du déplacement. Une même trajectoire peut être parcourue dans deux sens.',
    ('pc_trajectories',None),'Trois formes de trajectoire ; la flèche précise le sens du parcours représenté.',
    'Rectiligne et uniforme ne sont pas synonymes. Le premier mot décrit la trajectoire ; le second décrit la constance de la valeur de la vitesse.',
    'Repérer plusieurs positions dans le même repère. Décrire séparément la forme de la trajectoire et le sens du déplacement.'),
Lecon('Comparer les positions dans le temps',
    'Une chronophotographie superpose des positions à des dates connues. Pour comparer la valeur de la vitesse, on peut relever les positions à intervalles de temps égaux. Des espacements égaux indiquent alors un mouvement de valeur de vitesse constante. Des espacements croissants correspondent à une augmentation de la valeur de la vitesse sur les intervalles observés ; des espacements décroissants à une diminution.',
    ('pc_chrono',None),'Pour chaque ligne, les dates 0, 1, 2, 3 et 4 sont séparées par la même durée.',
    'L’espacement ne renseigne sur l’évolution de la vitesse que si l’on connaît les durées correspondantes. Un mouvement circulaire peut avoir une valeur de vitesse constante tout en changeant de direction.',
    'Vérifier l’égalité des intervalles de temps avant de comparer les distances entre positions successives.')
],Activite('Photographier un petit mobile',
    'Décrire un déplacement avec une série de positions datées.',[
    'En classe, filmer un mobile sur une piste droite avec un appareil fixe. Garder un repère de longueur dans le plan du mouvement.',
    'Extraire cinq positions à intervalles de temps égaux. Identifier le même point sur chaque image.',
    'Comparer les espacements. Pour un entraînement sans vidéo, analyser les trois lignes du schéma.'
],('pc_chrono',None),'On compare les espacements à l’intérieur d’une même ligne ; l’origine des positions est arbitraire.',[
    'Quelle ligne présente des espacements constants ? Lesquels augmentent ou diminuent ?',
    'Pourquoi l’appareil doit-il rester fixe par rapport à la piste ?',
    'Rédige une description complète d’une ligne avec trajectoire et évolution de la vitesse.'
], 'A montre des espacements constants : mouvement rectiligne de valeur de vitesse constante. En B, les espacements augmentent ; en C, ils diminuent. Un appareil fixe conserve le même repère ; s’il se déplace, les positions apparentes changent aussi à cause de l’observateur. La comparaison suppose des intervalles de temps égaux et une échelle de longueur commune.'),[
    'Décrire un mouvement exige un objet étudié et un repère.',
    'La trajectoire est l’ensemble des positions successives du point choisi.',
    'Rectiligne, circulaire et curviligne décrivent la forme de la trajectoire.',
    'Le sens du parcours est distinct de la forme du chemin.',
    'À durées égales, les espacements renseignent sur l’évolution de la valeur de la vitesse.'
], '« Les points sont plus éloignés, donc le mobile va plus vite. » Vérifier aussi les durées séparant les positions.',[
E(1,'Préciser le repère',['Une élève est assise dans un bus qui roule. Est-elle immobile par rapport à son siège ?','Est-elle immobile par rapport à un arrêt de bus ?'],'Elle est immobile par rapport à son siège si elle reste assise. Elle est en mouvement par rapport à l’arrêt quand le bus roule. Il faut annoncer le repère pour éviter une contradiction apparente.'),
E(2,'Nommer un chemin',['Un point suit une droite. Comment nomme-t-on sa trajectoire ?','Un point suit un cercle. Comment nomme-t-on sa trajectoire ?'],'Les trajectoires sont respectivement rectiligne et circulaire. Ces noms ne précisent pas si la valeur de la vitesse est constante.'),
E(3,'Lire le sens',['Deux cyclistes parcourent la même ligne droite en sens opposés. Leur trajectoire peut-elle avoir la même forme ?','Quelle information faut-il ajouter pour les distinguer ?'],'Oui, la forme peut être rectiligne pour les deux. Il faut préciser le sens du mouvement, par exemple de A vers B et de B vers A.'),
E(4,'Un passager observé',['Nomme deux repères possibles pour le voyageur du schéma.','Décris son mouvement par rapport à chacun.'],'On peut choisir le train ou le quai. Le voyageur assis est au repos par rapport au train et en mouvement par rapport au quai lorsque le train se déplace.',figure=('pc_reference',None)),
E(5,'Des mots différents',['« Rectiligne » décrit-il la rapidité ou la forme de la trajectoire ?','Que décrit « uniforme » lorsqu’on parle de la valeur de la vitesse ?'],'Rectiligne décrit la forme de la trajectoire. Uniforme indique une valeur de vitesse constante. On peut aller en ligne droite en accélérant ou en ralentissant.'),
E(6,'Des positions régulières',['Des positions sont séparées de 2 cm toutes les 0,5 s. Que peux-tu dire de la valeur de la vitesse ?','Quelle condition sur les temps est essentielle ?'],'La même distance est parcourue pendant chaque durée égale : la valeur de la vitesse est constante sur ces intervalles. L’égalité des intervalles de temps est essentielle.'),
E(7,'Trois lignes à comparer',['Classe A, B et C selon l’évolution de la valeur de la vitesse.','Cite les indices utilisés.'],'A : valeur constante ; B : valeur croissante ; C : valeur décroissante. On utilise les espacements successifs, avec les mêmes durées entre positions dans chaque ligne.',figure=('pc_chrono',None)),
E(8,'Un tour de manège',['Dans le repère du sol, quelle est la trajectoire d’un siège de manège tournant autour d’un axe fixe ?','La direction du déplacement reste-t-elle la même tout le tour ?'],'La trajectoire du siège est circulaire dans le modèle. La direction du déplacement change au cours du tour, même si la valeur de la vitesse est constante.'),
E(9,'Le bon point à suivre',['Pourquoi faut-il suivre le même point d’un ballon sur toute une série d’images ?','Quel point simple peut-on choisir pour décrire le déplacement global ?'],'Changer de point peut modifier la trajectoire relevée et fausser la comparaison. Le centre du ballon constitue un choix simple pour décrire son déplacement global, en laissant de côté sa rotation.'),
E(10,'Des durées inégales',['Un point parcourt 1 m en 1 s, puis 2 m en 2 s. Le second intervalle prouve-t-il une accélération ?','Compare les distances parcourues par seconde.'],'Non. Les deux intervalles correspondent à 1 m par seconde en moyenne. La plus grande distance du second intervalle est accompagnée d’une durée deux fois plus longue ; elle ne prouve pas une augmentation de vitesse.',check='1/1==2/2'),
E(11,'Une description complète',['Un mobile suit une ligne droite vers la droite ; les espacements augmentent à durées égales. Rédige une description.'],'Par rapport au repère fixe choisi, le point étudié suit une trajectoire rectiligne vers la droite et la valeur de sa vitesse augmente sur les intervalles observés. Les trois informations sont repère, trajectoire et évolution de vitesse.'),
E(12,'L’appareil se déplace',['Un élève marche en filmant un autre élève immobile au sol. Pourquoi l’image peut-elle montrer un déplacement apparent ?','Quel repère permettrait de dire que le second élève est au repos ?'],'L’appareil change de position par rapport à l’élève filmé. Le mouvement apparent dépend donc du repère de l’appareil. Par rapport au sol ou à un repère fixé au sol, l’élève filmé est au repos dans la situation donnée.'),
E(13,'Une photographie unique',['Peut-on déterminer l’évolution de la vitesse à partir d’une seule photo d’un mobile sans autre information ?','Quelles données supplémentaires demander ?'],'Non. Il faut des positions à plusieurs dates connues ou une mesure de vitesse fournie par un instrument. Une photo seule indique une position ou un aspect à un instant, pas l’évolution temporelle.'),
E(14,'Une hypothèse à tester',['Une balle parcourt des distances égales sur trois images prises à des dates inconnues. Peut-on conclure à un mouvement uniforme ?','Quelle vérification faut-il obtenir ?'],'Pas encore. Il faut vérifier que les durées entre images sont égales. Des espacements égaux parcourus en durées différentes ne correspondent pas à une même vitesse moyenne sur les intervalles.'),
E(15,'Comparer deux observateurs',['Deux amis restent assis face à face dans un train en mouvement. L’un affirme « nous ne bougeons pas » ; un passant affirme le contraire. Qui a raison ?','Formule les deux phrases sans ambiguïté.'],'Les deux descriptions peuvent être correctes. « Nous sommes au repos par rapport au train » et « Les voyageurs sont en mouvement par rapport au quai » précisent chacune le repère. Une description scientifique n’omet pas ce choix.')
],Defi('Le reportage de deux témoins',
    'Une balle est tenue immobile par un voyageur dans un train avançant en ligne droite. Une caméra est fixée dans le train ; une autre est fixée sur le quai. Prépare deux commentaires scientifiques compatibles.',
    ('pc_reference',None),['Choisis le point étudié et le repère de chaque caméra.','Décris ce que chaque caméra peut relever.','Ajoute ce qui changerait si le voyageur lâchait la balle, sans prévoir de calcul.'],
    'Séparer la situation balle tenue de la situation après lâcher ; ne pas mélanger les repères.',
    'Pour la balle tenue, son centre est immobile par rapport au train et se déplace en ligne droite par rapport au quai, dans le modèle donné. Après lâcher, sa position change aussi par rapport au train ; il faut alors relever de nouvelles positions pour décrire les trajectoires dans chaque repère. Les commentaires doivent annoncer le repère au lieu de chercher un mouvement unique absolu.'))

C10=Chapitre(10,'Comment comparer deux trajets de durées différentes ?',[
    'Calculer une vitesse moyenne à partir d’une distance parcourue et d’une durée.',
    'Utiliser des unités cohérentes et convertir les durées.',
    'Distinguer vitesse moyenne et variation de vitesse pendant un trajet.'
],[
Lecon('Distance parcourue, durée et vitesse',
    'La vitesse moyenne compare la distance parcourue à la durée du trajet : vitesse moyenne = distance parcourue ÷ durée. Avec des mètres et des secondes, elle s’exprime en mètres par seconde (m/s). Avec des kilomètres et des heures, elle s’exprime en kilomètres par heure (km/h). Si la valeur de la vitesse reste constante, ce quotient donne aussi cette valeur constante. Sur un trajet varié, il résume le trajet entier.',
    ('pc_speed',None),'Exemple de mouvement uniforme : 3 m sont parcourus chaque seconde ; d désigne la distance depuis le départ.',
    'Une vitesse de 3 m/s signifie 3 m parcourus par seconde dans un mouvement uniforme. La distance parcourue suit le trajet, pas forcément la ligne droite entre départ et arrivée.',
    'Écrire les données, vérifier leurs unités, calculer le quotient puis écrire une phrase avec l’unité : 12 m ÷ 4 s = 3 m/s.'),
Lecon('Rendre les unités cohérentes',
    'Une heure vaut 60 min et 3 600 s. Une minute vaut 60 s. Un kilomètre vaut 1 000 m. Avant un calcul, convertir pour utiliser une même famille d’unités. Pour passer de m/s à km/h, on multiplie par 3,6 : en une heure, 1 m/s correspond à 3 600 m, soit 3,6 km. Dans le sens inverse, on divise par 3,6.',
    ('pc_path',None),'Le trajet mesure 120 m ; la séparation directe des extrémités est différente et ne sert pas à ce calcul.',
    '1 min 30 s vaut 90 s, et non 1,30 min ni 130 s. 0,5 h vaut 30 min ; une écriture décimale d’heure ne se lit pas comme des minutes.',
    'Choisir d’abord l’unité demandée pour la vitesse. Convertir la distance et la durée avant de diviser, puis contrôler l’ordre de grandeur.'),
Lecon('Une moyenne ne raconte pas tout',
    'Deux trajets peuvent avoir la même vitesse moyenne sans se dérouler de la même manière. Un cycliste peut s’arrêter puis repartir, alors qu’un autre avance régulièrement. La moyenne sur le trajet entier inclut les arrêts si leur durée fait partie du temps mesuré. Une valeur donnée par un compteur à un instant ne décrit pas nécessairement la moyenne de tout le trajet.',
    ('pc_chrono',None),'Des mouvements différents peuvent conduire à des distances et durées totales identiques.',
    'Pour un mouvement uniforme, distance = vitesse × durée. Pour un trajet non uniforme, cette relation s’utilise avec la vitesse moyenne sur la même durée totale.',
    'Pour une moyenne sur plusieurs étapes, additionner les distances et les durées, puis diviser les totaux. Ne pas faire automatiquement la moyenne des vitesses des étapes.')
],Activite('Mesurer une vitesse de marche',
    'Prévoir une mesure reproductible sur une distance connue, sans course.',[
    'Choisir une zone sûre et une distance de 10 m mesurée. Définir les lignes de départ et d’arrivée et le moment de déclenchement du chronomètre.',
    'Effectuer trois essais de marche normale. Relever la durée de chaque essai avec son unité ; ne pas modifier la distance.',
    'Calculer les vitesses moyennes. Données d’entraînement possibles : 10 m en 8 s, 10 s et 12 s.'
],('pc_speed',{'t':[0,2,4,6,8],'v':[0,2.5,5,7.5,10],'max':10}),
    'La droite illustre un modèle uniforme de 10 m en 8 s ; une marche réelle présente de petites variations.',[
    'Calcule les trois vitesses moyennes en m/s ; arrondis la dernière au centième.',
    'Quel essai correspond à la plus grande vitesse moyenne ?',
    'Cite deux causes possibles de variation des résultats.'
], 'Les vitesses moyennes sont 10 ÷ 8 = 1,25 m/s ; 10 ÷ 10 = 1 m/s ; 10 ÷ 12 ≈ 0,83 m/s. Le premier essai est le plus rapide en moyenne. Le rythme de marche, le déclenchement du chronomètre, le repérage des lignes et la précision de la distance contribuent aux variations.'),[
    'Vitesse moyenne = distance parcourue ÷ durée du même trajet.',
    'Mètres et secondes conduisent à des m/s ; kilomètres et heures à des km/h.',
    '1 h = 3 600 s ; 1 min = 60 s ; 1 km = 1 000 m.',
    'De m/s à km/h : multiplier par 3,6 ; inversement : diviser par 3,6.',
    'Une moyenne peut inclure des arrêts et masquer des variations de vitesse.'
], '« J’additionne les vitesses puis je divise par deux. » Pour un trajet complet, calculer distance totale ÷ durée totale.',[
E(1,'Choisir une unité',['Quelle unité de vitesse associe-t-on aux mètres et aux secondes ?','Quelle unité associe-t-on aux kilomètres et aux heures ?'],'On obtient respectivement des m/s et des km/h. Le résultat doit inclure à la fois une longueur et une durée dans son unité.'),
E(2,'Une première vitesse',['Un mobile parcourt 20 m en 5 s. Calcule sa vitesse moyenne.','Que signifie le résultat pour un mouvement uniforme ?'],'20 ÷ 5 = 4 m/s. Si le mouvement est uniforme, le mobile parcourt 4 m chaque seconde.',check='20/5==4'),
E(3,'Convertir une durée',['Convertis 2 min en secondes.','Convertis 1 min 30 s en secondes.'],'2 min = 120 s. 1 min 30 s = 60 + 30 = 90 s. Le système des durées utilise 60 secondes par minute.',check='2*60==120 and 60+30==90'),
E(4,'Lire une droite',['Quelle distance est parcourue en 4 s ?','Quelle est la vitesse dans le modèle représenté ?'],'Le graphique donne 12 m en 4 s. La vitesse vaut 12 ÷ 4 = 3 m/s. La droite passant par l’origine indique une distance proportionnelle au temps dans le modèle.',figure=('pc_speed',None)),
E(5,'Le bon trajet',['Pour calculer la vitesse moyenne entre A et B sur ce chemin, faut-il utiliser 120 m ou 80 m ?','Pourquoi ?'],'Il faut utiliser les 120 m réellement parcourus sur le chemin. Les 80 m correspondent à la séparation en ligne droite, qui n’est pas la distance du trajet.',figure=('pc_path',None)),
E(6,'Un trajet à vélo',['Un cycliste parcourt 12 km en 0,5 h. Calcule sa vitesse moyenne.','Exprime la durée en minutes.'],'12 ÷ 0,5 = 24 km/h. La durée 0,5 h correspond à 30 min, et non à 50 min.',check='12/0.5==24 and 0.5*60==30'),
E(7,'Un petit robot',['Un robot parcourt 150 cm en 5 s. Calcule sa vitesse en m/s.','Pourquoi faut-il convertir avant le calcul ?'],'150 cm = 1,50 m. La vitesse moyenne vaut 1,50 ÷ 5 = 0,30 m/s. Sans conversion, on obtiendrait 30 cm/s, pas 30 m/s.',check='1.5/5==0.3'),
E(8,'Changer d’unité de vitesse',['Convertis 5 m/s en km/h.','Convertis 36 km/h en m/s.'],'5 × 3,6 = 18 km/h. 36 ÷ 3,6 = 10 m/s. On contrôle le sens de conversion avec le repère 1 m/s = 3,6 km/h.',check='5*3.6==18 and 36/3.6==10'),
E(9,'Prévoir une distance',['Un mobile garde une vitesse de 2 m/s pendant 15 s. Quelle distance parcourt-il ?','Quelle condition autorise l’utilisation de cette vitesse sur toute la durée ?'],'La distance vaut 2 × 15 = 30 m. On suppose que la valeur de la vitesse reste égale à 2 m/s pendant les 15 s.',check='2*15==30'),
E(10,'Prévoir une durée',['À 4 m/s constants, combien de temps faut-il pour parcourir 100 m ?','Écris la relation utilisée en mots.'],'La durée vaut 100 ÷ 4 = 25 s. On utilise durée = distance ÷ vitesse, avec des unités cohérentes.',check='100/4==25'),
E(11,'Inclure un arrêt',['Une promenade de 3 km dure 1 h, dont 15 min d’arrêt. Quelle vitesse moyenne obtient-on sur la sortie entière ?','Pourquoi n’utilise-t-on pas seulement 45 min ici ?'],'La moyenne de la sortie entière vaut 3 km/h. La durée annoncée inclut l’arrêt ; utiliser 45 min calculerait une moyenne sur le seul temps de déplacement, qui répond à une autre question.'),
E(12,'Deux étapes différentes',['Étape 1 : 2 km en 20 min. Étape 2 : 4 km en 40 min. Calcule la vitesse moyenne totale en km/h.','Que remarques-tu sur les deux étapes ?'],'La distance totale est 6 km et la durée totale 60 min = 1 h : moyenne de 6 km/h. Chaque étape a aussi une moyenne de 6 km/h ; les distances sont proportionnelles aux durées.',check='2+4==6 and 20+40==60'),
E(13,'Une moyenne trompeuse',['Un trajet comprend 1 h à 10 km/h puis 2 h à 4 km/h. Calcule distance et durée totales.','La vitesse moyenne vaut-elle 7 km/h ?'],'Distances : 10 km et 8 km, soit 18 km. Durée : 3 h. La moyenne vaut 18 ÷ 3 = 6 km/h, et non 7 km/h. Les deux vitesses n’ont pas été maintenues pendant des durées égales.',check='(10+2*4)/3==6'),
E(14,'Comparer des performances',['A parcourt 100 m en 20 s ; B parcourt 150 m en 25 s. Qui est le plus rapide en moyenne ?','Pourquoi comparer seulement les durées serait-il incorrect ?'],'A : 5 m/s. B : 6 m/s. B est plus rapide en moyenne. Les distances diffèrent : une durée plus courte ne suffit pas pour classer les vitesses.',check='100/20==5 and 150/25==6'),
E(15,'Contrôler un résultat',['Une élève trouve 500 m/s pour un marcheur ayant parcouru 100 m en 200 s. Repère l’erreur probable.','Calcule et interprète la valeur correcte.'],'Le résultat correct est 100 ÷ 200 = 0,5 m/s. Une confusion entre multiplication, division ou unités a probablement eu lieu. La valeur 500 m/s est incohérente avec une marche ; l’ordre de grandeur aide à détecter l’erreur.',check='100/200==0.5')
],Defi('Le trajet avec une pause',
    'Une élève marche 600 m en 8 min, s’arrête 2 min, puis parcourt encore 400 m en 5 min. Elle affirme : « Ma vitesse moyenne est la moyenne des vitesses des deux parties marchées. »',
    ('pc_path',None),['Calcule la distance et la durée de toute la sortie.','Calcule la vitesse moyenne en m/min puis en km/h.','Explique pourquoi la méthode proposée n’est pas adaptée.'],
    'L’arrêt compte dans la durée totale demandée. 1 000 m correspondent à 1 km.',
    'Distance totale : 1 000 m. Durée totale : 8 + 2 + 5 = 15 min, soit 0,25 h. Moyenne : environ 66,7 m/min, ou 4 km/h. La moyenne arithmétique des deux vitesses ne tient pas compte des durées différentes ni de la pause. Utiliser les totaux du même trajet.'))

C11=Chapitre(11,'Un objet immobile subit-il des actions ?',[
    'Reconnaître des actions qui déforment ou modifient un mouvement.',
    'Distinguer interactions de contact et interactions à distance.',
    'Identifier les objets en interaction avec un système choisi.'
],[
Lecon('Observer les effets d’une action',
    'Une action mécanique peut déformer un objet, le mettre en mouvement ou modifier son mouvement : changer sa direction ou la valeur de sa vitesse. Un objet immobile peut pourtant subir plusieurs actions. Un livre posé sur une table subit notamment l’action de la table et l’attraction de la Terre. L’absence de mouvement visible ne signifie donc pas l’absence d’interactions.',
    ('pc_actions',None),'Quelques effets possibles : déformation, mise en mouvement et modification de trajectoire.',
    'Décrire un effet ne suffit pas toujours à identifier toutes les actions. Une action peut exister sans produire une modification visible dans la situation observée.',
    'Choisir l’objet étudié, décrire son état ou son évolution, puis rechercher quels autres objets peuvent agir sur lui.'),
Lecon('Contact ou action à distance ?',
    'Une action de contact nécessite un contact entre les objets : main et ballon, table et livre, air et voile. Une interaction à distance existe sans contact direct : attraction de la Terre, interaction entre aimants, par exemple. Le mot interaction rappelle que les objets agissent l’un sur l’autre. À ce niveau, on identifie les objets et la nature de l’interaction sans calculer de force.',
    ('pc_magnet',None),'Un aimant peut agir sur un objet ferromagnétique sans le toucher ; tous les métaux ne sont pas attirés de la même façon.',
    'L’air est une matière : son action sur une voile ou un mobile est une action de contact. « Invisible » ne signifie pas « à distance ».',
    'Demander si les surfaces sont en contact. Pour une attraction terrestre ou magnétique, identifier les deux objets même si l’un est loin ou peu visible.'),
Lecon('Construire un diagramme objet-interactions',
    'Un diagramme objet-interactions place l’objet étudié au centre et les objets de son environnement autour. Un lien indique une interaction retenue dans le modèle ; sa légende distingue contact et distance. Le schéma ne représente ni la trajectoire, ni le sens d’une force, ni une valeur mesurée. Il sert à ne pas oublier des interactions dans une situation clairement définie.',
    ('pc_interaction',['Table','Terre','Main']),'Exemple : un livre posé sur une table est poussé par une main. L’interaction avec l’air est négligée dans ce modèle.',
    'La Terre reste à considérer même lorsque l’objet est immobile. On annonce les interactions négligées pour simplifier la situation.',
    'Nommer le système central, dresser la liste des objets extérieurs, classer les liens et ajouter une légende explicite.')
],Activite('Enquêter autour d’un livre',
    'Comparer les interactions dans deux situations proches.',[
    'Situation A : un livre repose sur une table, sans main. Situation B : une main pousse le livre sur la même table.',
    'Choisir le livre comme objet étudié et négliger l’action de l’air pour cette activité.',
    'Tracer un diagramme pour chaque situation, en différenciant contact et distance.'
],('pc_interaction',['Table','Terre','Main']),'Le schéma correspond à la situation B ; il ne représente pas des forces orientées.',[
    'Quel lien doit-on retirer pour représenter la situation A ?',
    'Pourquoi conserve-t-on le lien avec la Terre dans les deux situations ?',
    'Quelles informations ce diagramme ne permet-il pas de calculer ?'
], 'Retirer le lien avec la main dans A ; garder la table et la Terre. L’attraction terrestre existe que le livre soit au repos ou en mouvement. Le diagramme liste les interactions retenues, mais ne donne ni leur valeur, ni leur direction détaillée, ni la vitesse de l’objet. Ces descriptions seront approfondies aux niveaux suivants.'),[
    'Une action peut déformer un objet ou modifier son mouvement.',
    'Un objet immobile peut subir plusieurs actions.',
    'Une interaction de contact exige un contact entre les objets.',
    'L’attraction terrestre et l’interaction magnétique peuvent agir à distance.',
    'Un diagramme objet-interactions est un inventaire avec une légende, pas un calcul de forces.'
], '« Le livre ne bouge pas, donc la Terre n’agit pas sur lui. » Le repos ne prouve pas l’absence d’interaction.',[
E(1,'Un effet visible',['Une main étire un élastique. Quel effet observe-t-on ?','Nomme les deux objets en interaction.'],'On observe une déformation de l’élastique. La main et l’élastique sont en interaction de contact.'),
E(2,'Classer les interactions',['Classe : pied et ballon au moment du tir ; Terre et ballon ; aimant et trombone attiré sans contact.'],'Pied-ballon : contact. Terre-ballon : interaction à distance. Aimant-trombone sans contact : interaction à distance.'),
E(3,'Le livre immobile',['Un livre sur une table subit-il l’attraction de la Terre ?','Quelle autre interaction de contact doit-on retenir ?'],'Oui. Le livre interagit aussi avec la table qui le soutient. Son immobilité n’efface pas ces interactions.'),
E(4,'L’action de l’air',['Le vent déforme une voile. L’interaction air-voile est-elle de contact ou à distance ?','Pourquoi l’air invisible peut-il agir ?'],'C’est une interaction de contact entre l’air et la voile. L’air est une matière ; son invisibilité ne l’empêche pas d’exercer une action.'),
E(5,'Lire un diagramme',['Quel objet est choisi comme système ?','Quel lien représente une interaction à distance ?'],'Le système est l’objet central. Le lien pointillé avec la Terre représente une interaction à distance, conformément à la légende. Les liens pleins indiquent des contacts.',figure=('pc_interaction',['Table','Terre','Main'])),
E(6,'Après le tir',['Après que le pied a quitté le ballon, y a-t-il encore un contact pied-ballon ?','Quelle interaction à distance reste présente ?'],'Il n’y a plus de contact entre le pied et le ballon. L’interaction avec la Terre reste présente. D’autres interactions, comme celle avec l’air, peuvent être retenues selon le modèle.'),
E(7,'Une bille déviée',['Une bille passe près d’un aimant et sa trajectoire change sans contact. Quel type d’interaction est mis en évidence ?','Quel effet de l’action est observé ?'],'Une interaction magnétique à distance est mise en évidence dans la situation donnée. Son effet observé est une modification de trajectoire.'),
E(8,'Préciser les objets',['Pourquoi « la table agit » est-il moins précis que « la table agit sur le livre » ?','Quel élément manque dans la première phrase ?'],'Il manque l’objet qui reçoit l’action. Une description précise identifie les deux objets en interaction ; le seul nom de la table ne suffit pas.'),
E(9,'Changer le système',['On étudie maintenant la table au lieu du livre. Faut-il placer encore le livre au centre du diagramme ?','Quel principe guide la construction ?'],'Non : la table devient le système central. On liste les objets qui interagissent avec elle. Le système central dépend de la question étudiée, et non d’un choix définitif pour toute la scène.'),
E(10,'Main retirée',['Dans le diagramme du livre poussé sur une table, quel lien disparaît lorsque la main est retirée ?','Le lien avec la table disparaît-il aussi si le livre reste posé ?'],'Le lien avec la main disparaît. Le lien avec la table reste puisque le livre est toujours en contact avec elle. Le lien avec la Terre reste également.'),
E(11,'Ne pas tout déduire',['Un diagramme donne un lien table-livre. Permet-il de connaître la valeur de la vitesse du livre ?','Quelle est sa fonction principale ?'],'Non. Le diagramme inventorie les interactions retenues dans la situation. Une valeur de vitesse exige une mesure de distance et de durée ou une autre information adaptée.'),
E(12,'Une chute dans l’air',['Établis la liste de deux objets pouvant interagir avec une balle en chute dans l’air.','Précise la nature de chaque interaction.'],'La Terre interagit à distance avec la balle ; l’air interagit par contact. Ici, on décrit une chute dans l’air ; le modèle simplifié qui néglige l’air doit être annoncé explicitement.'),
E(13,'Choisir un modèle simple',['Pour un livre immobile sur une table, on néglige l’air. Pourquoi cette simplification doit-elle être annoncée ?','Quelles interactions garde-t-on ?'],'Elle indique que le diagramme représente un modèle choisi, pas une liste exhaustive de toutes les influences possibles. On garde l’interaction de contact avec la table et l’interaction à distance avec la Terre.'),
E(14,'Une généralisation à discuter',['« Tous les métaux sont attirés par un aimant. » Pourquoi cette phrase est-elle trop générale ?','Propose un protocole de comparaison.'],'Les matériaux métalliques n’ont pas tous le même comportement magnétique. Comparer plusieurs échantillons identifiés avec le même aimant, à la même distance et sans contact initial, en notant les résultats. Ne pas étendre la propriété d’un trombone en acier à tous les métaux.'),
E(15,'Une action sans mouvement visible',['Un élève pousse très doucement un meuble qui reste immobile. Peut-on conclure qu’il n’exerce aucune action ?','Quelle observation ou information montre le contact ?'],'Non. La main ou le corps peut exercer une action même sans déplacement visible du meuble. Le contact observé et l’effort exercé font partie des informations de la situation. Il faut distinguer existence d’une interaction et effet visible sur le mouvement.')
],Defi('Trois scènes, trois diagrammes',
    'Décris un ballon dans trois situations : tenu dans la main ; lâché dans l’air ; posé sur le sol. Tu retiendras la Terre et les objets en contact nécessaires, en précisant le rôle de l’air.',
    ('pc_actions',None),['Choisis le ballon comme système dans les trois scènes.','Dresse les listes d’interactions et classe-les.','Explique pourquoi une interaction peut rester présente dans les trois scènes.'],
    'L’attraction terrestre ne dépend pas de l’existence d’un contact avec une main ou un support.',
    'Ballon tenu : contact avec la main et interaction à distance avec la Terre. Ballon lâché : Terre à distance et air par contact si on le prend en compte. Ballon posé : contact avec le sol et interaction avec la Terre. L’air entoure aussi les scènes tenues et posées ; il peut être négligé dans un modèle simple annoncé. L’interaction terrestre reste présente dans les trois situations.'))

CHAPITRES_MOUVEMENT=[C9,C10,C11]
