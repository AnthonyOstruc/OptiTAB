from modele import C,E

C('Lire et écrire jusqu’à 1 000','Nombres','P1 : la centaine ; P2 : jusqu’à 1 000',
 'Je lis un nombre et je relie ses chiffres aux quantités.','Plaques de cent, barres de dix et cubes unités.',
 'Échange dix barres de dix contre une plaque de cent. Prépare ensuite 2 plaques, 3 barres et 4 cubes. Dis le nombre obtenu.',
 ['Une centaine vaut 10 dizaines ou 100 unités.','234, c’est 2 centaines, 3 dizaines et 4 unités.','Dans 204, le zéro indique qu’il n’y a aucune dizaine isolée.'],
 '234 = 200 + 30 + 4. Je lis « deux-cent-trente-quatre ».',('hundreds',234),
 'Représente 306. Que signifie le zéro ?', '3 centaines et 6 unités. Il n’y a aucune dizaine isolée.',[
 E('Écris le nombre représenté, puis lis-le.','325 : trois-cent-vingt-cinq.',('hundreds',325)),
 E('Écris en chiffres : cent-sept ; quatre-cent-soixante ; neuf-cent-deux.','107 ; 460 ; 902.'),
 E('Lis : 180 ; 508 ; 790 ; 1 000.','cent-quatre-vingts ; cinq-cent-huit ; sept-cent-quatre-vingt-dix ; mille.'),
 E('Écris en lettres : 215 ; 381 ; 600.','deux-cent-quinze ; trois-cent-quatre-vingt-un ; six-cents.'),
 E('Complète : 397 ; 398 ; … ; … ; 401.','399 ; 400.'),
 E('Compte de 100 en 100 : 250 ; 350 ; … ; … ; …','450 ; 550 ; 650.'),
 E('Un stock contient 4 boîtes de 100 cubes, 2 boîtes de 10 et 7 cubes. Combien de cubes ?','400 + 20 + 7 = 427 cubes.',None,'400+20+7==427'),
 E('Combien de centaines faut-il pour obtenir 1 000 unités ?','10 centaines, car 10 × 100 = 1 000.',None,'10*100==1000'),
 E('Lina écrit 45 pour quatre-cent-cinq. Explique et corrige.','405 : le chiffre 4 vaut 400. Le zéro garde la place des dizaines.')],
 'Faire fabriquer la quantité avant de lire et d’écrire le nombre.', 'Aborder la centaine dès P1 et 1 000 au plus tard en P2 ; ne pas installer une longue révision séparée du CP.')

C('Décomposer et échanger','Nombres','P1 et P2',
 'Je représente un même nombre de plusieurs façons.','Matériel de centaines, dizaines et unités.',
 'Construis 243. Échange une plaque de cent contre dix barres de dix. Puis échange une barre contre dix cubes. La quantité change-t-elle ?',
 ['La valeur d’un chiffre dépend de sa place.','Dix unités s’échangent contre une dizaine ; dix dizaines contre une centaine.','Un même nombre peut avoir plusieurs décompositions.'],
 '243 = 200 + 40 + 3. C’est aussi 24 dizaines et 3 unités.',('placevalue',[2,4,3]),
 'Écris 352 avec des centaines, des dizaines et des unités.', '3 centaines, 5 dizaines et 2 unités ; aussi 35 dizaines et 2 unités.',[
 E('Décompose 416 en centaines, dizaines et unités.','416 = 400 + 10 + 6.',('placevalue',[4,1,6]),'400+10+6==416'),
 E('Quel nombre contient 5 centaines, 12 dizaines et 7 unités ?','500 + 120 + 7 = 627.',None,'500+120+7==627'),
 E('Complète : 28 dizaines = … unités ; 6 centaines = … dizaines.','280 unités ; 60 dizaines.',None,'28*10==280 and 6*100==60*10'),
 E('Écris 305 de deux façons différentes avec du matériel.','Par exemple 3 centaines et 5 unités ; 30 dizaines et 5 unités.'),
 E('Recompose : 700 + 80 + 9 ; 400 + 6 ; 90 + 500.','789 ; 406 ; 590.',None,'700+80+9==789 and 400+6==406 and 90+500==590'),
 E('Dans 583, quel est le chiffre des dizaines ? Combien y a-t-il de dizaines entières ?','Le chiffre des dizaines est 8. Il y a 58 dizaines entières et 3 unités.'),
 E('Prépare 236 timbres avec des plaques de 100, des carnets de 10 et des timbres isolés. Trouve trois commandes.','2 plaques, 3 carnets, 6 unités ; ou 1 plaque, 13 carnets, 6 unités ; ou 23 carnets et 6 unités.'),
 E('Une collection a 2 centaines, 8 dizaines et 17 unités. Regroupe-la.','200 + 80 + 17 = 297 : 2 centaines, 9 dizaines et 7 unités.',None,'200+80+17==297'),
 E('Noé dit : « Dans 407, le 4 vaut 4. » Que représente ce 4 ?','Il représente 4 centaines, donc 400 unités.')],
 'Faire réellement les échanges et vérifier qu’aucun cube n’est perdu.', 'Distinguer chiffre des dizaines et nombre de dizaines entières.')

C('Comparer et placer jusqu’à 1 000','Nombres','P1 et P2',
 'Je compare des nombres et je lis le pas d’une graduation.','Cartes de nombres et bandes graduées.',
 'Compare 347 et 372 avec les plaques, les barres et les unités. Place-les ensuite entre 300 et 400 sur une bande.',
 ['Je compare d’abord les centaines, puis les dizaines, puis les unités.','Sur une graduation, je cherche la valeur d’un intervalle.','Encadrer un nombre, c’est le placer entre deux nombres.'],
 '347 < 372 : les centaines sont égales et 4 dizaines sont moins que 7 dizaines.',('scaledline',[300,400,10,[]]),
 'Sur une ligne graduée de dix en dix, quel nombre suit 460 ?', '470 : on ajoute 10 à chaque graduation.',[
 E('Complète les graduations manquantes.','420 ; 450 ; 480.',('scaledline',[400,500,10,[420,450,480]])),
 E('Complète avec <, > ou = : 306 … 360 ; 721 … 719 ; 500 … 500.','306 < 360 ; 721 > 719 ; 500 = 500.'),
 E('Range du plus petit au plus grand : 423 ; 342 ; 432 ; 324 ; 400.','324 < 342 < 400 < 423 < 432.'),
 E('Encadre 568 entre deux centaines consécutives, puis entre deux dizaines consécutives.','500 < 568 < 600 ; 560 < 568 < 570.'),
 E('Écris un nombre entre 799 et 802.','800 ou 801.'),
 E('Lis le point marqué sur cette ligne.','600 : les graduations avancent de 100.',('markedline',[0,1000,100,600])),
 E('Une école a 398 élèves. Une autre en a 403. Laquelle a le plus d’élèves ?','La seconde : 403 > 398.'),
 E('La règle des nombres porte 240, 241, 242… Quel nombre est quatre intervalles après 242 ?','246 : 242 + 4 = 246.',None,'242+4==246'),
 E('Lina range 509 avant 490 parce que 0 est plus petit que 9. Explique son erreur.','Il faut d’abord comparer les centaines : 4 centaines sont moins que 5. Donc 490 < 509.')],
 'Faire annoncer le pas avant de compléter une graduation.', 'Ne pas compter le point de départ comme un intervalle parcouru.')

C('Rangs, suites et motifs','Nombres','P1 puis toute l’année',
 'Je repère un rang et je trouve une règle de suite.','Cartes de lettres et bande des rangs jusqu’à 100.',
 'Aligne des cartes A B C A B C. Marque le départ. Cherche la 8e carte, puis la 30e sans tout recompter.',
 ['Le rang indique une place, à partir d’un départ et dans un sens précis.','Avant le 48e, il y a 47 éléments.','Pour continuer une suite, je cherche le motif répété ou ce qui change.'],
 'A B C se répète. Les rangs 3, 6, 9… portent C ; le 30e porte C.',('pattern','ABCABC'),
 'Tu es 25e dans une file. Combien de personnes sont devant toi ?', '24 personnes.',[
 E('Dans A B A B…, quelle lettre est au 39e rang ?','A : les rangs impairs portent A.',('pattern','ABABAB')),
 E('Un coureur arrive 63e. Combien de coureurs sont arrivés avant lui ?','62 coureurs.'),
 E('Écris le rang qui suit quatre-vingt-dix-neuvième.','Centième : 100e.'),
 E('Dans A B C A B C…, quelle est la 60e lettre ?','C, car 60 = 20 × 3.',None,'20*3==60'),
 E('Continue : 125 ; 135 ; 145 ; … ; …','155 ; 165. On ajoute 10.'),
 E('Continue : 2 ; 4 ; 8 ; 16 ; … ; …','32 ; 64. Chaque nombre est le double du précédent.'),
 E('Dans 1 ; 3 ; 5 ; 7…, quel est le 12e nombre ?','23. On peut poursuivre la suite jusqu’au 12e rang.',None,'1+2*11==23'),
 E('Continue : 1 ; 2 ; 4 ; 7 ; 11 ; … ; …','16 ; 22. On ajoute successivement 1, 2, 3, 4, 5, 6.'),
 E('Tu es 37e dans une file de 100 personnes. Combien sont derrière toi ?','63 personnes : 100 - 37 = 63.',None,'100-37==63')],
 'Utiliser un tableau rang/élément pour repérer le motif sans mélanger rang et valeur.', 'Les ordinaux vont jusqu’à centième. Faire préciser le départ et le sens.')
