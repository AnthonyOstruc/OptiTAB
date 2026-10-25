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
Bilan('A','Nombres, calculs et premiers outils',[
(r'Écrire le nombre $8\times1\,000+3\times100+7$.',r'$\res{8\,307}$ : chaque valeur rejoint son rang.','assert 8*1000+3*100+7==8307'),
(r'Calculer de tête $457+19$.',r'$457+20-1=\res{476}$.','assert 457+19==476'),
(r'Poser et calculer $702-458$.',r'$\res{244}$ ; contrôle : $244+458=702$.','assert 702-458==244'),
(r'Calculer $36:4$.',r'$\res9$, car $9\times4=36$.','assert 36//4==9'),
(r'Calculer $7\times60$.',r'$7\times6=42$ puis un zéro : $\res{420}$.','assert 7*60==420'),
(r'Encadrer $3\,456$ entre deux centaines consécutives.',r'$\res{3\,400<3\,456<3\,500}$.','assert 3400<3456<3500'),
(r'Calculer $\frac38+\frac28$.',r'$\res{\frac58}$ : les huitièmes s’ajoutent.','assert Rational(3,8)+Rational(2,8)==Rational(5,8)'),
(r'Écrire avec une virgule : $2+\frac3{10}+\frac5{100}$.',r'$\res{2{,}35}$.','assert 2+Rational(3,10)+Rational(5,100)==Rational("2.35")'),
(r'Comparer $4{,}5$ et $4{,}45$.',r'$4{,}50>4{,}45$ : $\res{4{,}5>4{,}45}$.','assert Rational("4.5")>Rational("4.45")'),
(r'Calculer $3{,}6\times10$.',r'$\res{36}$ : chaque chiffre monte d’un rang.','assert Rational("3.6")*10==36'),
(r'Compléter : $25\times\square=100$.',r'$\square=\res4$.','assert 25*4==100'),
(r'Donner l’arrondi à l’entier de $6{,}78$.',r'$\res7$, car $6{,}78$ est plus proche de 7.','assert abs(Rational("6.78")-7)<abs(Rational("6.78")-6)'),
],[
Probleme('La fête de l’école',
Q(r'La fête de l’école a rapporté 875 euros aux stands de jeux et 468 euros à la buvette. Calculer la recette totale.',
r'Les dépenses s’élèvent à 390 euros. Quelle somme reste-t-il ?',
r'Le reste est partagé également entre 7 classes. Combien reçoit chaque classe ?'),
r'\editionEtape{Recette}$875+468=\res{1\,343}$ euros.\editionEtape{Reste}$1\,343-390=\res{953}$ euros.\editionEtape{Partage}$953=7\times136+1$ : chaque classe reçoit $\res{136}$ euros et il reste 1 euro. Contrôle : $7\times136+1=953$.',
'assert 875+468==1343 and 1343-390==953 and divmod(953,7)==(136,1)'),
Probleme('Les cartons de la médiathèque',
Q(r'La médiathèque reçoit $1\,350$ livres neufs. Elle les range dans des cartons de 8 livres. Combien de cartons complets remplit-elle ?',
r'Combien de livres restent hors carton ?',
r'Combien de cartons faut-il au total pour transporter tous les livres ?'),
r'\editionEtape{Division}$1\,350=8\times168+6$ : $\res{168}$ cartons complets.\editionEtape{Le reste}Il reste $\res6$ livres.\editionEtape{Interpréter}Pour tout transporter, un carton entamé s’ajoute : $\res{169}$ cartons. Le même reste se lit selon la question.',
'assert divmod(1350,8)==(168,6) and 168+1==169'),
Probleme('Le gâteau du dimanche',
Q(r'Un gâteau est coupé en 8 parts égales. La famille en mange 5 parts le midi. Quelle fraction du gâteau reste-t-il ?',
r'Le soir, chacun des 3 convives mange une part. Quelle fraction du gâteau a été mangée sur la journée ?',
r'Un second gâteau identique est partagé entre 4 enfants. Quelle est la part de chacun ? La donner en fraction de gâteau.'),
r'\editionEtape{Après le midi}$\frac88-\frac58=\res{\frac38}$ du gâteau.\editionEtape{Sur la journée}$5+3=8$ parts : $\res{\frac88=1}$, tout le gâteau.\editionEtape{Le second gâteau}Chaque enfant reçoit $\res{\frac14}$ de gâteau, soit 2 parts sur 8 : $\frac28=\frac14$.',
'assert 1-Rational(5,8)==Rational(3,8) and Rational(5,8)+Rational(3,8)==1 and Rational(2,8)==Rational(1,4)'),
Probleme('Les courses du mercredi',
Q(r'Lou achète un livre à $8{,}70$ euros et un jeu de cartes à $4{,}55$ euros. Calculer la dépense.',
r'Elle paie avec un billet de 20 euros. Combien lui rend-on ?',
r'Avec la monnaie rendue, peut-elle acheter trois carnets à $2{,}20$ euros l’un ?'),
r'\editionEtape{Dépense}$8{,}70+4{,}55=\res{13{,}25}$ euros.\editionEtape{Monnaie}$20-13{,}25=\res{6{,}75}$ euros.\editionEtape{Comparer}Trois carnets coûtent $2{,}20\times3=6{,}60$ euros et $6{,}60<6{,}75$ : $\res{\text{oui}}$, il resterait 15 centimes.',
'assert Rational("8.70")+Rational("4.55")==Rational("13.25") and 20-Rational("13.25")==Rational("6.75") and Rational("2.20")*3==Rational("6.60") and Rational("6.75")-Rational("6.60")==Rational(".15")'),
]),
Bilan('B','Toute l’année en quatre problèmes',[
(r'Donner le chiffre des dizaines de mille de $582\,741$.',r'$\res8$.','assert (582741//10000)%10==8'),
(r'Calculer de tête $68\times5$.',r'$680:2=\res{340}$.','assert 68*5==340'),
(r'Calculer de tête $801-599$.',r'$801-600+1=\res{202}$.','assert 801-599==202'),
(r'Donner le quotient et le reste de $75:8$.',r'$75=8\times9+3$ : quotient $\res9$, reste $\res3$.','assert divmod(75,8)==(9,3)'),
(r'Écrire $\frac74$ avec un entier et une fraction.',r'$\res{1+\frac34}$.','assert Rational(7,4)==1+Rational(3,4)'),
(r'Écrire $0{,}75$ sous forme de fraction.',r'$\frac{75}{100}=\res{\frac34}$.','assert Rational(".75")==Rational(3,4)'),
(r'Comparer $5{,}08$ et $5{,}8$.',r'$\res{5{,}08<5{,}8}$.','assert Rational("5.08")<Rational("5.8")'),
(r'Calculer $10-3{,}45$.',r'$\res{6{,}55}$ par compléments.','assert 10-Rational("3.45")==Rational("6.55")'),
(r'Convertir 2 h 15 min en minutes.',r'$120+15=\res{135}$ min.','assert 2*60+15==135'),
(r'Donner le périmètre d’un carré de côté 9 cm.',r'$4\times9=\res{36}$ cm.','assert 4*9==36'),
(r'Comparer 3 kg et $2\,900$ g.',r'$3\,000>2\,900$ : $\res{3\ \mathrm{kg}>2\,900\ \mathrm g}$.','assert 3000>2900'),
(r'Quatre pains coûtent 6 euros. Combien coûtent 8 pains ?',r'Deux fois plus : $\res{12}$ euros.','assert 6*2==12'),
],[
Probleme('Le train de Lucie',
Q(r'Lucie prend un train qui part à 9 h 47 et arrive à 12 h 15. Combien dure le voyage ?',
r'Son retour dure 2 h 40 et se termine à 19 h 05. À quelle heure est-elle partie ?',
r'Quel trajet est le plus long, et de combien de minutes ?'),
r'\editionEtape{L’aller}De 9 h 47 à 10 h : 13 min ; puis 2 h ; puis 15 min : $\res{2\ \text h\ 28}$.\editionEtape{Le retour}Reculer de 2 h 40 depuis 19 h 05 : $19\ \text h\ 05\to17\ \text h\ 05\to16\ \text h\ 25$ : départ à $\res{16\ \text h\ 25}$.\editionEtape{Comparer}$2$ h $40=160$ min et $2$ h $28=148$ min : le retour dépasse l’aller de $\res{12}$ min.',
'assert (12*60+15)-(9*60+47)==148 and (19*60+5)-160==16*60+25 and 160-148==12'),
Probleme('Le potager de l’école',
Q(r'Le potager est un rectangle de $7{,}5$ m sur 4 m. Calculer son périmètre.',
r'On le clôture avec un grillage vendu $2{,}50$ euros le mètre. Calculer le prix du grillage.',
r'La classe dispose de 60 euros. Quelle somme restera-t-il après l’achat ?'),
r'\editionEtape{Périmètre}$2\times(7{,}5+4)=2\times11{,}5=\res{23}$ m.\editionEtape{Prix}Un mètre coûte $2{,}50$ euros : 23 m coûtent $2{,}50\times23=\res{57{,}50}$ euros, car $2{,}5\times23=57{,}5$.\editionEtape{Reste}$60-57{,}50=\res{2{,}50}$ euros. Contrôle : le prix est proportionnel à la longueur achetée.',
'assert 2*(Rational("7.5")+4)==23 and Rational("2.50")*23==Rational("57.50") and 60-Rational("57.50")==Rational("2.50")'),
Probleme('L’enquête des déplacements',
Q(r'Une enquête interroge les 55 élèves de deux classes.'+tableau(['','À pied','En bus','À vélo'],[['CM1','12','9','5'],['CM2','10','13','6']])+r'Combien d’élèves viennent en bus ?',
r'Dans quelle classe la marche à pied est-elle la plus fréquente ?',
r'Vérifier que le tableau recense bien les 55 élèves.'),
r'\editionEtape{Colonne bus}$9+13=\res{22}$ élèves.\editionEtape{Comparer}12 marcheurs en CM1 contre 10 en CM2 : la marche domine en $\res{\text{CM1}}$.\editionEtape{Contrôle global}$12+9+5=26$ en CM1 et $10+13+6=29$ en CM2 : $26+29=\res{55}$ élèves, le compte est bon.',
'assert 9+13==22 and 12>10 and 12+9+5==26 and 10+13+6==29 and 26+29==55'),
Probleme('La kermesse du hasard',
Q(r'Au stand de la kermesse, une roue porte 10 secteurs identiques : 6 marqués « perdu », 3 « sucette », 1 « cadeau ». Quel résultat est le plus probable ?',
r'A-t-on une chance sur deux d’obtenir une sucette ? Justifier.',
r'Le stand propose aussi 2 tailles de ballons et 5 couleurs. Combien de ballons différents peut-on composer ?'),
r'\editionEtape{Le plus probable}Les secteurs sont équiprobables : « perdu », avec $\res6$ secteurs sur 10, domine.\editionEtape{La sucette}Trois secteurs sur dix, moins de la moitié : $\res{\text{non}}$, c’est peu probable, pas une chance sur deux.\editionEtape{Les ballons}Chaque taille accepte 5 couleurs : $2\times5=\res{10}$ ballons différents.',
'assert 6>3>1 and 6+3+1==10 and Rational(3,10)<Rational(1,2) and 2*5==10'),
]),
]
