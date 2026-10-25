from dataclasses import dataclass
from modele import Q
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
Bilan('A','Relier calculs, données et géométrie',[
(r'Calculer $7+4\times3$.',r'Le produit est prioritaire : $7+12=\res{19}$.','assert 7+4*3==19'),
(r'Calculer $8{,}4:0{,}7$.',r'$84:7=\res{12}$.','assert Rational("8.4")/Rational(".7")==12'),
(r'Donner quotient et reste de 74 par 9.',r'$74=9\times8+2$ : quotient $\res8$, reste $\res2$.','assert divmod(74,9)==(8,2)'),
(r'Comparer $-3{,}4$ et $-3{,}04$.',r'$\res{-3{,}4<-3{,}04}$ ; le premier est plus éloigné de zéro du côté négatif.','assert Rational("-3.4")<Rational("-3.04")'),
(r'Calculer $-7-(-12)$.',r'$-7+12=\res5$.','assert -7-(-12)==5'),
(r'Calculer $2/3+1/4$.',r'$8/12+3/12=\res{11/12}$.','assert Rational(2,3)+Rational(1,4)==Rational(11,12)'),
(r'Calculer $11^2$.',r'$11\times11=\res{121}$.','assert 11**2==121'),
(r'Développer $4(x+2)$.',r'$\res{4x+8}$ par distributivité.','assert expand(4*(x+2))==4*x+8'),
(r'Résoudre $5x=18$.',r'$x=18/5=\res{3{,}6}$.','assert solve(5*x-18,x)==[Rational("3.6")]'),
(r'Calculer 25 % de 60.',r'Un quart de 60 vaut $\res{15}$.','assert Rational(25,100)*60==15'),
(r'Deux angles d’un triangle valent 55 et 65 degrés. Trouver le troisième.',r'$180-55-65=\res{60^\circ}$.','assert 180-55-65==60'),
(r'Quelle est la probabilité d’obtenir un nombre impair sur un dé équilibré à six faces ?',r'Trois faces sur six : $\res{1/2}$.','assert len([a for a in range(1,7) if a%2==1])==3'),
],[
Probleme('Une sortie et son budget',
Q(r'28 élèves paient chacun 8,50 euros. Le transport coûte 98 euros et les entrées 4,50 euros par élève. Calculer la dépense totale.',
r'Quelle somme reste-t-il ? Quel pourcentage des sommes reçues cela représente-t-il ?',
r'Le reste est partagé également entre sept ateliers. Combien reçoit chacun ?'),
r'\editionEtape{Dépenses}Les entrées coûtent $28\times4{,}50=126$ euros. Le total vaut $98+126=\res{224}$ euros.\editionEtape{Reste}Les sommes reçues valent $28\times8{,}50=238$ euros. Il reste $\res{14}$ euros, soit $14/238=1/17\approx\res{5{,}88\,\%}$ du total reçu.\editionEtape{Partage}Chaque atelier reçoit $14:7=\res2$ euros. Le pourcentage prend pour référence les sommes reçues, pas les dépenses.',
'assert 98+28*Rational("4.5")==224 and 28*Rational("8.5")==238 and 238-224==14 and Rational(14,238)==Rational(1,17) and 14//7==2'),
Probleme('Un triangle et sa médiane',
Q(r'ABC a $AB=10$ cm et une hauteur issue de C de 6 cm. Calculer son aire.',
r'M est le milieu de [AB]. Calculer l’aire de ACM et justifier.',
r'N est le milieu de [AM]. Calculer l’aire de ACN, puis celle de NCM.'),
r'\editionEtape{Aire entière}$10\times6:2=\res{30\ \mathrm{cm}^2}$.\editionEtape{Première médiane}CM partage le triangle en deux triangles de bases égales et de même hauteur : ACM a une aire de $\res{15\ \mathrm{cm}^2}$.\editionEtape{Second partage}Dans ACM, N est le milieu de [AM]. CN partage donc cette aire en deux : ACN et NCM ont chacun $\res{7{,}5\ \mathrm{cm}^2}$. On n’a pas besoin de connaître la longueur des médianes.',
'assert Rational(10*6,2)==30 and Rational(5*6,2)==15 and Rational(15,2)==Rational("7.5")','bilan-triangle'),
Probleme('Une enquête et un tirage',
Q(r'Une enquête auprès de 20 élèves donne 8 vélos, 6 bus et 6 déplacements à pied. Donner les trois fréquences.',
r'Donner les angles d’un diagramme circulaire représentant cette enquête.',
r'On tire au hasard une fiche parmi les 20 fiches individuelles, toutes de même taille. Donner la probabilité que la fiche corresponde à un élève venu en bus, puis expliquer le modèle.'),
r'\editionEtape{Fréquences}Elles valent $\res{40\,\%,30\,\%,30\,\%}$.\editionEtape{Diagramme}Les angles valent $\res{144^\circ,108^\circ,108^\circ}$ ; leur somme est 360 degrés.\editionEtape{Tirage}Les fiches sont supposées mélangées et équiprobables. Six fiches sur vingt correspondent au bus : $\res{3/10}$. Cela décrit un tirage dans les fiches recueillies, pas nécessairement les habitudes de tout le collège.',
'assert [Rational(a,20)*100 for a in [8,6,6]]==[40,30,30] and [Rational(a,20)*360 for a in [8,6,6]]==[144,108,108] and Rational(6,20)==Rational(3,10)','bilan-enquete'),
Probleme('Un bac et des récipients',
Q(r'Un bac intérieur mesure 40 cm sur 25 cm sur 30 cm. Calculer son volume en cm$^3$ puis en litres.',
r'On remplit seulement les $3/5$ du bac. Quel volume d’eau cela représente-t-il ?',
r'On dispose de bouteilles de 1,5 L. Combien de bouteilles pleines faut-il pour ce remplissage ?'),
r'\editionEtape{Capacité totale}$40\times25\times30=30000$ cm$^3$, soit $\res{30\ \mathrm L}$.\editionEtape{Niveau choisi}Les $3/5$ de 30 L valent $(30:5)\times3=\res{18\ \mathrm L}$.\editionEtape{Bouteilles}$18:1{,}5=\res{12}$ bouteilles. Le quotient est entier : aucun reste de bouteille n’est nécessaire.',
'assert 40*25*30==30000 and Rational(3,5)*30==18 and Rational(18)/Rational("1.5")==12','bilan-bac'),
]),
Bilan('B','Chercher, modéliser et expliquer',[
(r'Calculer $24:3\times2$.',r'De gauche à droite : $8\times2=\res{16}$.','assert Rational(24,3)*2==16'),
(r'315 est-il divisible par 9 ?',r'La somme des chiffres vaut 9 : $\res{oui}$.','assert 315%9==0'),
(r'Donner l’opposé de $-2{,}5$ et sa distance à zéro.',r'Les deux valent $\res{2{,}5}$ ; la distance à zéro est la valeur absolue.','assert -Rational("-2.5")==Abs(Rational("-2.5"))==Rational("2.5")'),
(r'Calculer $-3+8-6$.',r'$5-6=\res{-1}$.','assert -3+8-6==-1'),
(r'Comparer $3/4$ et $5/8$.',r'$3/4=6/8>5/8$.','assert Rational(3,4)>Rational(5,8)'),
(r'Calculer $5/6-1/4$.',r'$10/12-3/12=\res{7/12}$.','assert Rational(5,6)-Rational(1,4)==Rational(7,12)'),
(r'Calculer $3^3+2^2$.',r'$27+4=\res{31}$.','assert 3**3+2**2==31'),
(r'Réduire $2x+5+3x+1$.',r'$\res{5x+6}$.','assert simplify(2*x+5+3*x+1)==5*x+6'),
(r'Résoudre $x+7=3$.',r'$x=3-7=\res{-4}$.','assert solve(x+7-3,x)==[-4]'),
(r'Convertir 4500 cm$^3$ en litres.',r'$4500:1000=\res{4{,}5\ \mathrm L}$.','assert Rational(4500,1000)==Rational("4.5")'),
(r'Calculer la moyenne de 6, 9 et 12.',r'$27:3=\res9$.','assert Rational(6+9+12,3)==9'),
(r'Un demi-tour conserve-t-il les aires ?',r'$\res{Oui}$, comme les longueurs et les angles.','assert 12==12'),
],[
Probleme('Deux tarifs de location',
Q(r'A coûte 4 euros par heure. B coûte 6 euros fixes puis 2 euros par heure. Construire un tableau pour 0, 1, 2, 3 et 4 h.',
r'Lire quand les deux tarifs sont égaux. Comparer pour 2 h puis 4 h.',
r'Quel tarif est proportionnel à la durée ? Justifier par le tableau et le graphique.'),
r'\editionEtape{Tableau}A donne $0,4,8,12,16$ ; B donne $6,8,10,12,14$ euros.\editionEtape{Comparer}Les tarifs sont égaux à $\res3$ h pour 12 euros. A est moins cher à 2 h ; B à 4 h.\editionEtape{Proportionnalité}Seul $\res A$ est proportionnel : coefficient 4 et droite passant par l’origine. B a un supplément fixe ; son prix à 0 h vaut 6 euros.',
'assert [t for t in range(5) if 4*t==6+2*t]==[3] and 4*2<6+2*2 and 4*4>6+2*4','bilan-tarifs'),
Probleme('Un parallélogramme et ses diagonales',
Q(r'Dans ABCD, O est le milieu de [AC] et de [BD]. Quelle nature peut-on prouver ?',
r'On sait en plus que $AC=BD$. Que peut-on préciser ? Et si les diagonales sont aussi perpendiculaires ?',
r'Pour $AB=8$ cm et $BC=5$ cm dans le cas du rectangle, calculer aire et périmètre.'),
r'\editionEtape{Milieu commun}Les diagonales ont le même milieu : ABCD est un parallélogramme.\editionEtape{Nature plus précise}Des diagonales égales en font un rectangle. Si elles sont aussi perpendiculaires, il est en plus losange : c’est un carré.\editionEtape{Mesures du rectangle}Avec les seules dimensions 8 cm et 5 cm, $A=8\times5=\res{40\ \mathrm{cm}^2}$ et $P=2(8+5)=\res{26\ \mathrm{cm}}$. Ce rectangle précis n’a pas de diagonales perpendiculaires, car ses côtés sont différents : les cas de la question précédente étaient conditionnels.',
'assert 8*5==40 and 2*(8+5)==26 and 8!=5','bilan-rectangle'),
Probleme('Un cylindre à remplir',
Q(r'Un cylindre a un rayon intérieur de 3 cm et une hauteur de 12 cm. Calculer son volume exact.',
r'Arrondir sa capacité au mL. Expliquer la conversion.',
r'Un second cylindre a le même rayon mais une hauteur de 8 cm. Donner le rapport de sa capacité à celle du premier et l’exprimer en pourcentage, au dixième près.'),
r'\editionEtape{Volume}$V=\pi\times3^2\times12=\res{108\pi\ \mathrm{cm}^3}$.\editionEtape{Capacité}Un cm$^3$ vaut un mL, donc environ $\res{339\ \mathrm{mL}}$.\editionEtape{Comparaison}La base est la même, les volumes sont proportionnels aux hauteurs. Le rapport vaut $8/12=2/3$, soit environ $\res{66{,}7\,\%}$. Utiliser les valeurs exactes évite les écarts dus aux arrondis.',
'assert pi*3**2*12==108*pi and round(float(108*pi))==339 and Rational(8,12)==Rational(2,3)','bilan-cylindre'),
Probleme('Un script à lire et à réparer',
Q(r'Le script donné répète trois fois : avancer de 40 pas, tourner à gauche de 90 degrés. Décrire la figure obtenue.',
r'Corriger un seul paramètre pour obtenir un carré et donner son périmètre.',
r'On veut ensuite un carré de périmètre 240 pas. Quel paramètre modifier ? Pourquoi un virage de 60 degrés ne convient-il pas pour un carré ?'),
r'\editionEtape{Lecture}Trois côtés d’un carré sont tracés ; le chemin n’est pas fermé.\editionEtape{Réparation}Mettre quatre répétitions. Le périmètre est $4\times40=\res{160}$ pas.\editionEtape{Autre taille}Pour un périmètre de 240, chaque côté doit mesurer $240:4=\res{60}$ pas. On garde quatre répétitions et des virages de 90 degrés. Des virages de 60 degrés ne donnent pas les angles droits du carré.',
'assert 4*40==160 and 240//4==60 and 4*90==360 and 4*60!=360','bilan-script'),
])
]
