from dataclasses import dataclass
from modele import Q,tableau
@dataclass
class Probleme:
    titre:str
    enonce:str
    corrige:str
    controle:str
    figure:str=''
@dataclass
class Bilan:
    lettre:str
    titre:str
    automatismes:list
    problemes:list
BILANS=[
Bilan('A','Nombres, calculs et proportions',[
(r'Écrire en chiffres : « deux-milliards-quarante-millions ».',r'$\res{2\,040\,000\,000}$.','assert 2*10**9+40*10**6==2040000000'),
(r'Écrire $3+\frac5{10}+\frac7{1\,000}$ avec une virgule.',r'$\res{3{,}507}$.','assert 3+Rational(5,10)+Rational(7,1000)==Rational("3.507")'),
(r'Ranger dans l’ordre croissant : $0{,}7$ ; $0{,}65$ ; $0{,}699$.',r'$\res{0{,}65<0{,}699<0{,}7}$.','assert Rational(".65")<Rational(".699")<Rational(".7")'),
(r'Arrondir $14{,}386$ au centième.',r'$\res{14{,}39}$.','assert abs(Rational("14.386")-Rational("14.39"))<Rational(1,200)'),
(r'Calculer $2{,}5\times0{,}4$.',r'$25\times4=100$, deux décimales : $\res1$.','assert Rational("2.5")*Rational(".4")==1'),
(r'Calculer $56\times0{,}01$.',r'$\res{0{,}56}$.','assert 56*Rational(".01")==Rational(".56")'),
(r'Quotient et reste de la division euclidienne de 200 par 15.',r'$200=15\times13+5$ : quotient $\res{13}$, reste $\res5$.','assert divmod(200,15)==(13,5)'),
(r'Compléter : $7\times\square=5$.',r'$\square=\res{\frac57}$.','assert 7*Rational(5,7)==5'),
(r'Calculer $\frac34-\frac14$, puis $\frac12+\frac14$.',r'$\res{\frac12}$ et $\res{\frac34}$.','assert Rational(3,4)-Rational(1,4)==Rational(1,2) and Rational(1,2)+Rational(1,4)==Rational(3,4)'),
(r'Calculer les $\frac23$ de 18.',r'$18:3\times2=\res{12}$.','assert Rational(2,3)*18==12'),
(r'Calculer 25~% de 36.',r'Le quart de 36 : $\res9$.','assert Rational(25,100)*36==9'),
(r'3 stylos coûtent $4{,}50$ €. Combien coûtent 6 stylos ?',r'Deux fois plus : $\res9$ €.','assert 2*Rational("4.5")==9'),
],[
Probleme('La médiathèque',
Q(r'Une médiathèque possède $12\,480$ livres. Elle en achète 350 par an. Combien en aura-t-elle dans 4 ans, sans en retirer ?',r'Elle range ses $12\,480$ livres sur des étagères de 48 livres. Combien d’étagères pleines ? Reste-t-il des livres ?',r'Un livre neuf coûte en moyenne $18{,}50$ €. Combien coûtent les 350 livres achetés en un an ?'),
r'\editionEtape{Dans 4 ans}$12\,480+4\times350=\res{13\,880}$ livres.\editionEtape{Étagères}$12\,480=48\times260$ : $\res{260}$ étagères pleines, aucun livre restant.\editionEtape{Budget}$350\times18{,}50=\res{6\,475}$ €. Ordre de grandeur : $350\times20=7\,000$.',
'assert 12480+4*350==13880 and divmod(12480,48)==(260,0) and 350*Rational("18.5")==6475'),
Probleme('Le marché',
Q(r'Des clémentines sont vendues $2{,}80$ € le kilogramme. Combien coûtent $2{,}5$ kg ?',r'Les cerises coûtent 6 € pour 750 g. Quel est leur prix au kilogramme ?',r'Inès paie avec un billet de 20 € ses $2{,}5$ kg de clémentines et 500 g de cerises. Combien lui rend-on ?'),
r'\editionEtape{Clémentines}$2{,}5\times2{,}80=\res7$ €.\editionEtape{Cerises}250 g coûtent $6:3=2$ € ; 1 kg coûte $4\times2=\res8$ € le kg.\editionEtape{Monnaie}500 g de cerises coûtent 4 €. Total : $7+4=11$ € ; rendu : $\res9$ €.',
'assert Rational("2.5")*Rational("2.8")==7 and 6//3*4==8 and 20-(7+4)==9'),
Probleme('Le gâteau et les parts',
Q(r'Un gâteau est partagé : Léa en prend $\frac14$, Noé $\frac13$. Quelle fraction du gâteau ont-ils prise ensemble ?',r'Quelle fraction reste-t-il ? L’écrire avec le dénominateur 12.',r'Le gâteau pesait 840 g. Quelle masse reste-t-il ? Quel pourcentage du gâteau Léa a-t-elle mangé ?'),
r'\editionEtape{Ensemble}$\frac3{12}+\frac4{12}=\res{\frac7{12}}$.\editionEtape{Reste}$1-\frac7{12}=\res{\frac5{12}}$.\editionEtape{Masse et pourcentage}$840:12\times5=\res{350}$ g. Léa a mangé $\frac14$, soit $\res{25\text{~\%}}$.',
'assert Rational(1,4)+Rational(1,3)==Rational(7,12) and 1-Rational(7,12)==Rational(5,12) and 840//12*5==350 and Rational(1,4)==Rational(25,100)'),
Probleme('Les cartes de collection',
Q(r'Tom a 3 fois plus de cartes que Sarah ; ensemble, ils en ont 96. Représenter la situation par un schéma en barres, puis trouver le nombre de cartes de chacun.',r'Tom donne 12 cartes à Sarah. Combien chacun en a-t-il alors ?',r'Combien Tom aurait-il dû en donner pour qu’ils en aient autant ?'),
r'\editionEtape{Barres}Quatre barres valent 96 : Sarah a $\res{24}$ cartes, Tom $\res{72}$.\editionEtape{Après le don}Tom : $72-12=\res{60}$ ; Sarah : $24+12=\res{36}$.\editionEtape{Égaliser}Au départ, l’écart vaut $72-24=48$ : Tom doit en donner la moitié, $\res{24}$. Chacun aurait alors 48 cartes.',
'assert 96//4==24 and 3*24==72 and 72-12==60 and 24+12==36 and (72-24)//2==24 and 72-24==24+24'),
]),
Bilan('B','Grandeurs, géométrie et données',[
(r'Convertir $3{,}5$ km en mètres.',r'$\res{3\,500}$ m.','assert Rational("3.5")*1000==3500'),
(r'Convertir 450 cm$^2$ en dm$^2$.',r'$\res{4{,}5\ \mathrm{dm}^2}$.','assert Rational(450,100)==Rational("4.5")'),
(r'Aire d’un rectangle de 8 m sur $2{,}5$ m.',r'$\res{20\ \mathrm{m}^2}$.','assert 8*Rational("2.5")==20'),
(r'Périmètre d’un disque de diamètre 20 cm, avec $\pi\approx3{,}14$.',r'Environ $\res{62{,}8\ \mathrm{cm}}$.','assert Rational("3.14")*20==Rational("62.8")'),
(r'Écrire $2{,}25$ h en heures et minutes.',r'$\res{2\text{ h }15\text{ min}}$.','assert Rational(".25")*60==15'),
(r'Un triangle a deux angles de $50^\circ$ et $60^\circ$. Mesure du troisième ?',r'$\res{70^\circ}$.','assert 180-50-60==70'),
(r'Un triangle équilatéral : mesure de chaque angle ?',r'$\res{60^\circ}$.','assert 180//3==60'),
(r'Deux angles supplémentaires : l’un mesure $35^\circ$. L’autre ?',r'$\res{145^\circ}$.','assert 180-35==145'),
(r'Le point M est sur la médiatrice de [AB] et $MA=6$ cm. Que vaut MB ?',r'$\res{MB=6\ \mathrm{cm}}$.','assert 6==6'),
(r'Combien d’axes de symétrie a un carré ?',r'$\res4$.','assert 4==4'),
(r'Volume d’un pavé de 3 cubes sur 2 sur 2, en cubes de 1 cm$^3$.',r'$\res{12\ \mathrm{cm}^3}$.','assert 3*2*2==12'),
(r'On lance un dé équilibré. Probabilité d’obtenir un multiple de 3 ?',r'3 et 6 : $\frac26=\res{\frac13}$.','assert Rational(2,6)==Rational(1,3)'),
],[
Probleme('La cour du collège',
Q(r'La cour est un rectangle de 45 m sur 30 m. Calculer son périmètre et son aire.',r'On y trace une piste circulaire de 20 m de diamètre. Quelle est la longueur d’un tour, au dixième de mètre ?',r'Un élève fait 6 tours de piste en 3 min 30 s. Quelle distance parcourt-il ? Combien de temps met-il en moyenne pour un tour ?'),
r'\editionEtape{Cour}Périmètre : $2\times(45+30)=\res{150\ \mathrm m}$. Aire : $45\times30=\res{1\,350\ \mathrm m^2}$.\editionEtape{Piste}$3{,}14\times20=\res{62{,}8\ \mathrm m}$ environ.\editionEtape{Course}$6\times62{,}8=\res{376{,}8\ \mathrm m}$. 3 min 30 s $=210$ s ; $210:6=\res{35\ \mathrm s}$ par tour.',
'assert 2*(45+30)==150 and 45*30==1350 and Rational("3.14")*20==Rational("62.8") and 6*Rational("62.8")==Rational("376.8") and 210//6==35'),
Probleme('Le triangle et son cercle',
Q(r'Construire le triangle ABC tel que $AB=7$ cm, $\widehat{A}=40^\circ$ et $\widehat{B}=60^\circ$. Calculer $\widehat{C}$.',r'Construire le cercle circonscrit au triangle. Expliquer la construction.',r"Construire le symétrique $A'B'C'$ du triangle par rapport à la droite (BC). Que vaut $A'B'$ ? L’angle de sommet $B'$ ?"),
r"\editionEtape{Triangle}$\widehat{C}=180-40-60=\res{80^\circ}$.\editionEtape{Cercle}On trace deux médiatrices, par exemple celles de [AB] et [AC] ; leur point d’intersection O est à égale distance des trois sommets. Le cercle de centre O de rayon OA passe par A, B et C.\editionEtape{Symétrique}B et C sont sur l’axe : $B'=B$ et $C'=C$. La symétrie conserve les longueurs et les angles : $\res{A'B'=7\ \mathrm{cm}}$ et l’angle de sommet $B'$ mesure $\res{60^\circ}$.",
'assert 180-40-60==80',figure='bilan-triangle'),
Probleme('La sortie au zoo',
Q(r'Le car part du collège à 8 h 40 et arrive au zoo à 10 h 15. Quelle est la durée du trajet ?',r'La visite dure 3,5 h à partir de l’arrivée. À quelle heure se termine-t-elle ?',r'Sur le plan du zoo, 1 cm représente 50 m. L’allée des fauves mesure 9 cm sur le plan. Quelle est sa longueur réelle ? Combien de temps faut-il pour la parcourir à 60 m par minute ?'),
r'\editionEtape{Trajet}$\res{1\text{ h }35\text{ min}}$.\editionEtape{Visite}$3{,}5$ h $=3$ h 30 min : fin à $\res{13\text{ h }45}$.\editionEtape{Allée}$9\times50=\res{450\ \mathrm m}$ ; $450:60=7{,}5$ min, soit $\res{7\text{ min }30\text{ s}}$.',
'assert (10*60+15)-(8*60+40)==95 and divmod(10*60+15+210,60)==(13,45) and 9*50==450 and Rational(450,60)==Rational("7.5")'),
Probleme('Les jeux de la kermesse',
Q(r'Une urne contient 4 boules rouges, 6 boules vertes et 10 boules jaunes. Quelle est la probabilité de tirer une boule verte ? L’écrire aussi en pourcentage.',r'Le tableau donne le nombre de lots gagnés à chaque stand. Quel stand a distribué le plus de lots ? Combien de lots en tout ?'+tableau(['Stand','pêche','chamboule-tout','loterie','quiz'],[['Lots','35','28','42','15']]),r'On retire de l’urne toutes les boules jaunes. Quelle est la nouvelle probabilité de tirer une boule verte ?'),
r'\editionEtape{Urne}20 boules : $\frac6{20}=\frac{30}{100}=\res{30\text{~\%}}$.\editionEtape{Lots}La $\res{\text{loterie}}$, avec 42 lots ; total : $35+28+42+15=\res{120}$ lots.\editionEtape{Sans les jaunes}10 boules restent, dont 6 vertes : $\frac6{10}=\res{0{,}6}$, soit 60~%.',
'assert Rational(6,20)==Rational(30,100) and max([35,28,42,15])==42 and 35+28+42+15==120 and Rational(6,10)==Rational(".6")'),
]),
]
