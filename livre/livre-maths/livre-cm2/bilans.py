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
Bilan('A','Nombres, calculs et fractions',[
(r'Écrire en chiffres : « trois-millions-quarante-mille-six ».',r'$\res{3\,040\,006}$.','assert 3*1000000+40*1000+6==3040006'),
(r'Calculer de tête $623-98$.',r'$623-100+2=\res{525}$.','assert 623-98==525'),
(r'Calculer $40\times700$.',r'$4\times7=28$ puis trois zéros : $\res{28\,000}$.','assert 40*700==28000'),
(r'Calculer $(15+25)\times(9-4)$.',r'$40\times5=\res{200}$.','assert (15+25)*(9-4)==200'),
(r'Donner tous les diviseurs de 20.',r'$\res{1, 2, 4, 5, 10, 20}$.','assert divisors(20)==[1,2,4,5,10,20]'),
(r'Calculer le quotient décimal exact de $13:4$.',r'$\res{3{,}25}$.','assert Rational(13,4)==Rational("3.25")'),
(r'Écrire $\frac{17}5$ avec un entier et une fraction.',r'$\res{3+\frac25}$.','assert Rational(17,5)==3+Rational(2,5)'),
(r'Calculer $\frac34+\frac18$.',r'$\frac68+\frac18=\res{\frac78}$.','assert Rational(3,4)+Rational(1,8)==Rational(7,8)'),
(r'Calculer les $\frac23$ de 27.',r'$27:3\times2=\res{18}$.','assert 27//3*2==18'),
(r'Comparer $5{,}09$ et $5{,}1$.',r'$5{,}090<5{,}100$ : $\res{5{,}09<5{,}1}$.','assert Rational("5.09")<Rational("5.1")'),
(r'Calculer $4{,}56\times100$.',r'$\res{456}$.','assert Rational("4.56")*100==456'),
(r'Calculer la moitié de $9{,}4$.',r'$\res{4{,}7}$.','assert Rational("9.4")/2==Rational("4.7")'),
],[
Probleme('Le concert de la région',
Q(r'Un concert a réuni $18\,750$ spectateurs le samedi et $16\,480$ le dimanche. Combien de spectateurs en tout ?',
r'Un billet coûte 24 euros. Calculer la recette du samedi.',
r'La salle peut accueillir $20\,000$ personnes par soir. Combien de places sont restées vides sur les deux soirs ?'),
r'\editionEtape{Total}$18\,750+16\,480=\res{35\,230}$ spectateurs.\editionEtape{Recette}$18\,750\times24=\res{450\,000}$ euros ; estimation : $19\,000\times24\approx456\,000$.\editionEtape{Places vides}Capacité : $40\,000$ places ; vides : $40\,000-35\,230=\res{4\,770}$.',
'assert 18750+16480==35230 and 18750*24==450000 and 40000-35230==4770'),
Probleme('Les sachets de bonbons',
Q(r'Un confiseur répartit $1\,000$ bonbons en sachets de 8. Combien de sachets complets prépare-t-il ? Reste-t-il des bonbons ?',
r'Un sachet est vendu $2{,}50$ euros. Quelle somme rapportent tous les sachets ?',
r'Il partage ensuite 45 euros de pourboire entre 4 vendeurs, au centime près. Combien reçoit chacun ?'),
r'\editionEtape{Sachets}$1\,000=8\times125$ : $\res{125}$ sachets, aucun bonbon restant.\editionEtape{Recette}$125\times2{,}50=\res{312{,}50}$ euros.\editionEtape{Partage}$45:4=\res{11{,}25}$ euros chacun ; contrôle : $11{,}25\times4=45$.',
'assert divmod(1000,8)==(125,0) and 125*Rational("2.50")==Rational("312.50") and Rational(45,4)==Rational("11.25")'),
Probleme('La pizza partagée',
Q(r'Lina mange $\frac38$ d’une pizza et Tom $\frac14$. Quelle fraction ont-ils mangée ensemble ?',
r'Quelle fraction de la pizza reste-t-il ?',
r'La pizza entière pesait 480 g. Quelle masse de pizza reste-t-il ?'),
r'\editionEtape{Ensemble}$\frac38+\frac28=\res{\frac58}$.\editionEtape{Reste}$1-\frac58=\res{\frac38}$.\editionEtape{Masse}$480:8\times3=\res{180}$ g.',
'assert Rational(3,8)+Rational(1,4)==Rational(5,8) and 1-Rational(5,8)==Rational(3,8) and 480//8*3==180'),
Probleme('Le programme mystère',
Q(r'Exécuter le programme « choisir un nombre ; multiplier par 3 ; ajouter 6 ; multiplier par 2 » avec le nombre 4.',
r'Quel nombre faut-il choisir pour obtenir 48 ?',
r'Écrire le résultat du programme pour un nombre $N$ quelconque, avec des parenthèses.'),
r'\editionEtape{Avec 4}$4\times3=12$ ; $12+6=18$ ; $18\times2=\res{36}$.\editionEtape{Remonter}$48:2=24$ ; $24-6=18$ ; $18:3=\res6$.\editionEtape{Pour N}Le résultat s’écrit $\res{((N\times3)+6)\times2}$.',
'assert (4*3+6)*2==36 and (48//2-6)//3==6 and expand((n*3+6)*2)==6*n+12'),
]),
Bilan('B','Grandeurs, géométrie et données',[
(r'Convertir $2{,}5$ km en mètres.',r'$\res{2\,500}$ m.','assert Rational("2.5")*1000==2500'),
(r'Convertir 750 g en kilogrammes.',r'$\res{0{,}75}$ kg.','assert Rational(750,1000)==Rational(".75")'),
(r'Convertir $3\ \mathrm{dm}^2$ en $\mathrm{cm}^2$.',r'$\res{300\ \mathrm{cm}^2}$.','assert 3*100==300'),
(r'Aire d’un rectangle de 9 cm sur 6 cm.',r'$\res{54\ \mathrm{cm}^2}$.','assert 9*6==54'),
(r'Convertir 2 min 30 s en secondes.',r'$\res{150}$ s.','assert 2*60+30==150'),
(r'Combien mesure la moitié d’un angle droit ?',r'$\res{45^\circ}$.','assert 90//2==45'),
(r'Combien de côtés a un hexagone ?',r'$\res6$.','assert 6==6'),
(r'Combien d’arêtes a un pavé ?',r'$\res{12}$.','assert 12==12'),
(r'Quatre cahiers coûtent 6 euros. Combien en coûtent 12 ?',r'Trois fois plus : $\res{18}$ euros.','assert 6*3==18'),
(r'Un dé est lancé. Chances d’obtenir 5 ou 6 ?',r'$\res{2\ \text{chances sur }6}$.','assert len([a for a in range(1,7) if a>=5])==2'),
(r'Un rayon mesure $3{,}5$ cm. Que mesure le diamètre ?',r'$\res7$ cm.','assert Rational("3.5")*2==7'),
(r'Donner le périmètre d’un carré de côté $4{,}5$ cm.',r'$\res{18}$ cm.','assert 4*Rational("4.5")==18'),
],[
Probleme('La rénovation de la chambre',
Q(r'Une chambre rectangulaire mesure $4{,}5$ m sur $3{,}2$ m. Calculer son aire.',
r'Le parquet coûte 25 euros le mètre carré. Quel est le prix du parquet ?',
r'On pose une plinthe sur tout le tour, sauf la porte de $0{,}8$ m. Quelle longueur de plinthe faut-il ?'),
r'\editionEtape{Aire}$4{,}5\times3{,}2=\res{14{,}4\ \mathrm m^2}$.\editionEtape{Prix}$14{,}4\times25=\res{360}$ euros.\editionEtape{Plinthe}Périmètre : $2\times(4{,}5+3{,}2)=15{,}4$ m ; sans la porte : $15{,}4-0{,}8=\res{14{,}6}$ m.',
'assert Rational("4.5")*Rational("3.2")==Rational("14.4") and Rational("14.4")*25==360 and 2*(Rational("4.5")+Rational("3.2"))-Rational(".8")==Rational("14.6")'),
Probleme('Le marathon des enfants',
Q(r'Une course démarre à 9 h 45 min 30 s. Le premier arrive après 38 min 45 s. À quelle heure arrive-t-il ?',
r'Le dernier arrive à 10 h 41. Combien de temps a-t-il couru ?',
r'Quel écart de temps sépare le premier du dernier ?'),
r'\editionEtape{Le premier}$9$ h 45 min 30 s $+38$ min 45 s : 30 s mènent à 9 h 46, puis 38 min 15 s : arrivée à $\res{10\ \text h\ 24\ \text{min}\ 15\ \text s}$.\editionEtape{Le dernier}De 9 h 45 min 30 s à 10 h 41 : $\res{55\ \text{min}\ 30\ \text s}$.\editionEtape{Écart}$55$ min 30 s $-38$ min 45 s $=\res{16\ \text{min}\ 45\ \text s}$.',
'assert (9*3600+45*60+30)+(38*60+45)==10*3600+24*60+15 and (10*3600+41*60)-(9*3600+45*60+30)==55*60+30 and (55*60+30)-(38*60+45)==16*60+45'),
Probleme('Le sondage de la classe',
Q(r'Sur 28 élèves, la moitié vient à pied, le quart en bus, le reste à vélo. Donner les trois effectifs.',
r'Dans un diagramme circulaire, quelle fraction du disque occupe le secteur « vélo » ?',
r'On tire au hasard la fiche d’un élève. Quelles sont les chances de tirer un élève venu en bus ?'),
r'\editionEtape{Effectifs}À pied : $28:2=\res{14}$ ; bus : $28:4=\res7$ ; vélo : $28-14-7=\res7$.\editionEtape{Secteur}$\frac7{28}=\res{\frac14}$ du disque.\editionEtape{Tirage}Les 28 fiches sont équiprobables : $\res{7\ \text{chances sur }28}$, soit une chance sur quatre.',
'assert 28//2==14 and 28//4==7 and 28-14-7==7 and Rational(7,28)==Rational(1,4)'),
Probleme('La figure à construire',
Q(r'Construire un carré ABCD de côté 6 cm. Quel est son périmètre ? son aire ?',
r'Tracer le cercle de centre A et de rayon 3 cm. Coupe-t-il le côté [AB] ? En quel point ?',
r'Le carré a-t-il un axe de symétrie passant par A ? Lequel ?'),
r'\editionEtape{Le carré}Périmètre $4\times6=\res{24}$ cm ; aire $6\times6=\res{36\ \mathrm{cm}^2}$.\editionEtape{Le cercle}Le rayon 3 cm est la moitié de AB : le cercle coupe [AB] en son $\res{\text{milieu}}$.\editionEtape{L’axe}La diagonale $\res{(AC)}$ est un axe de symétrie du carré qui passe par A.',
'assert 4*6==24 and 6*6==36 and 6//2==3'),
]),
]
