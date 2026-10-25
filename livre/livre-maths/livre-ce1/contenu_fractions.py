from modele import C,E

C('Découvrir les fractions','Fractions','Fractions unitaires dès P2',
 'Je partage un tout en parts égales et j’en prends une.','Bandes identiques, disques en papier et ciseaux.',
 'Plie une bande en deux parts égales, puis une autre en quatre. Prends une seule part à chaque fois. Nomme la moitié et le quart.',
 ['Une fraction précise une partie d’un tout partagé en parts égales.','Un quart, c’est une part d’un tout partagé en quatre parts égales.','Dans 1/4, le 4 indique quatre parts égales et le 1 une part prise.'],
 'La bande est partagée en quatre parts égales. Une seule est coloriée : c’est un quart de la bande.',('fracbar',[1,4,True]),
 'Plie une bande en deux parts égales. Comment nommes-tu chaque part ?', 'Une moitié, ou un demi de la bande : 1/2.',[
 E('Quelle fraction de la bande est coloriée ?','Un cinquième : 1/5.',('fracbar',[1,5,False]),'F(1,5)<1'),
 E('Partage cette bande en deux parts égales, puis colorie une moitié.','Deux parts de même aire ; une seule est coloriée.',('plainband',None)),
 E('Colorie un tiers de la bande.','Colorier une des trois parts égales.',('fracbar',[0,3,False])),
 E('Lis : 1/2 ; 1/3 ; 1/4 ; 1/5.','un demi ; un tiers ; un quart ; un cinquième.'),
 E('Lis : 1/6 ; 1/8 ; 1/10.','un sixième ; un huitième ; un dixième.'),
 E('Une bande a six parts égales. Une seule est choisie. Écris la fraction.','1/6.',('fracbar',[1,6,False])),
 E('Lina découpe une bande en quatre parts de tailles différentes. Une part est-elle forcément un quart ?','Non. Il faut quatre parts égales pour que chacune soit un quart du tout.'),
 E('Avec l’adulte, partage équitablement le contenu d’une petite bouteille entre quatre verres identiques. Quelle part reçoit chaque verre ?','Un quart du contenu initial. Vérifier que les quantités sont égales.'),
 E('Colorie un huitième de la bande. Explique le rôle du 8.','Colorier une part. Le 8 indique les huit parts égales du tout.',('fracbar',[0,8,False]))],
 'Toujours désigner le tout et vérifier l’égalité des parts avant d’écrire la fraction.', 'Les fractions sont des fractions d’un tout, au plus égales à 1 ; dénominateurs 2, 3, 4, 5, 6, 8 ou 10.')

C('Lire et comparer des fractions','Fractions','P3, comparaison au plus tard dès P4',
 'Je compte les parts et je compare sur un même tout.','Bandes identiques partagées en parts égales.',
 'Sur deux bandes de même taille, colorie deux cinquièmes puis trois cinquièmes. Compare ensuite un tiers et un sixième sur deux autres bandes identiques.',
 ['Le dénominateur indique le nombre total de parts égales. Le numérateur indique les parts prises.','À dénominateur égal, plus on prend de parts, plus la fraction est grande.','Pour un même tout, un tiers est plus grand qu’un sixième : chaque part est plus grande.'],
 '2/5 < 3/5. Sur le même tout, trois parts d’un cinquième couvrent plus que deux parts.',('fraccompare',[[2,5],[3,5]]),
 'Compare un demi et un quart du même tout.', '1/2 > 1/4 : la moitié du tout est plus grande que son quart.',[
 E('Écris la fraction coloriée et nomme son numérateur et son dénominateur.','3/8. Numérateur : 3 ; dénominateur : 8.',('fracbar',[3,8,False])),
 E('Colorie trois quarts de la bande.','Colorier trois des quatre parts égales.',('fracbar',[0,4,False])),
 E('Complète avec <, > ou = : 2/6 … 5/6 ; 4/8 … 3/8.','2/6 < 5/6 ; 4/8 > 3/8.',None,'F(2,6)<F(5,6) and F(4,8)>F(3,8)'),
 E('Compare un tiers et un sixième du même tout. Explique avec les bandes.','1/3 > 1/6 : le tiers correspond à une plus grande part.',('fraccompare',[[1,3],[1,6]]),'F(1,3)>F(1,6)'),
 E('Compare : 1/5 et 1/10 ; 1/8 et 1/4. Les touts sont identiques.','1/5 > 1/10 ; 1/8 < 1/4.',None,'F(1,5)>F(1,10) and F(1,8)<F(1,4)'),
 E('Quelle fraction correspond au tout entier : 5/5 ou 4/5 ?','5/5 = 1. Les cinq parts sont prises.',None,'F(5,5)==1'),
 E('Lina colorie 7/10 d’une bande et Noé 4/10 d’une bande identique. Qui a colorié la plus grande partie ?','Lina : 7/10 > 4/10.',None,'F(7,10)>F(4,10)'),
 E('Une petite bande et une grande bande sont chacune partagées en deux. Leurs moitiés ont-elles forcément la même longueur ?','Non. Les touts n’ont pas la même longueur. Il faut comparer des parts d’un même tout ou de touts identiques.'),
 E('Avec des bandes identiques, vérifie que deux quarts couvrent une moitié.','2/4 = 1/2. Superposer les deux parts d’un quart à une moitié.',('fraccompare',[[2,4],[1,2]]),'F(2,4)==F(1,2)')],
 'Utiliser des touts identiques et faire superposer les parties.', 'Ne pas comparer seulement les dénominateurs comme des entiers ; préciser le tout de référence.')

C('Réunir et enlever des fractions','Fractions','P4 puis P5',
 'J’ajoute ou je retire des parts de même taille.','Bandes identiques prédécoupées.',
 'Prends deux morceaux d’un cinquième et ajoute un morceau d’un cinquième du même tout. Recompose le tout, puis enlève une part.',
 ['Pour un même tout, j’ajoute des parts de même taille en comptant les parts prises.','Le dénominateur reste le même quand la taille des parts ne change pas.','Je peux chercher la fraction qui manque pour retrouver le tout.'],
 '2/5 + 1/5 = 3/5 : deux cinquièmes et un cinquième font trois cinquièmes.',('fracoperation',[2,1,5,'+']),
 'Il y a trois quarts coloriés. On enlève un quart. Quelle fraction reste ?', '3/4 - 1/4 = 2/4.',[
 E('Ajoute les parts du même tout. Quelle fraction obtiens-tu ?','1/6 + 3/6 = 4/6.',('fracoperation',[1,3,6,'+']),'F(1,6)+F(3,6)==F(4,6)'),
 E('Calcule : 2/8 + 3/8 ; 4/10 + 2/10.','5/8 ; 6/10.',None,'F(2,8)+F(3,8)==F(5,8) and F(4,10)+F(2,10)==F(6,10)'),
 E('Calcule : 5/6 - 2/6 ; 3/5 - 1/5.','3/6 ; 2/5.',None,'F(5,6)-F(2,6)==F(3,6) and F(3,5)-F(1,5)==F(2,5)'),
 E('Complète : 2/5 + … = 1 ; 3/8 + … = 1.','3/5 ; 5/8.',None,'F(2,5)+F(3,5)==1 and F(3,8)+F(5,8)==1'),
 E('Explique pourquoi 3/4 + 1/4 donne le tout entier.','Les quatre quarts sont réunis : 4/4 = 1.',None,'F(3,4)+F(1,4)==1'),
 E('Une bande a dix parts égales. Quatre sont bleues et trois sont vertes. Quelle fraction est coloriée ?','7/10 de la bande.',('fracbar',[0,10,False]),'F(4,10)+F(3,10)==F(7,10)'),
 E('Lina colorie 3/10 d’une figure en bleu et le reste en rouge. Quelle fraction est rouge ?','7/10 : il faut sept dixièmes pour compléter les trois dixièmes.',None,'1-F(3,10)==F(7,10)'),
 E('Noé écrit 1/4 + 2/4 = 3/8. Explique son erreur.','Les parts restent des quarts. On en réunit trois : 3/4.',None,'F(1,4)+F(2,4)==F(3,4)'),
 E('Avec les morceaux d’un même tout, trouve deux façons d’obtenir quatre sixièmes par addition.','Par exemple 1/6 + 3/6 = 4/6 et 2/6 + 2/6 = 4/6.',None,'F(1,6)+F(3,6)==F(4,6) and F(2,6)+F(2,6)==F(4,6)')],
 'Faire réunir les morceaux avant d’écrire ; le nombre de parts change, pas leur taille.', 'Les sommes restent au plus égales à 1. Pas d’opérations sur des fractions de dénominateurs différents.')
