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
Bilan('A','Calculer, lire et démontrer',[
(r"Calculer $(-8)\times(-3)$.",r"Mêmes signes, produit positif : $\res{24}$.","assert (-8)*(-3)==24"),
(r"Calculer $7-2\times5$.",r"Le produit est prioritaire : $7-10=\res{-3}$.","assert 7-2*5==-3"),
(r"Calculer $\frac34+\frac18$.",r"$\frac68+\frac18=\res{\frac78}$.","assert Rational(3,4)+Rational(1,8)==Rational(7,8)"),
(r"Donner l’inverse de $-\frac25$.",r"L’inverse est $\res{-\frac52}$ : le produit des deux nombres vaut 1.","assert Rational(-2,5)*Rational(-5,2)==1"),
(r"Écrire $2^3\times2^4$ sous la forme d’une seule puissance.",r"$3+4=7$ facteurs 2 : $\res{2^7}$.","assert 2**3*2**4==2**7"),
(r"Donner $\sqrt{121}$.",r"$11^2=121$ et $11$ est positif, donc $\res{11}$.","assert sqrt(121)==11"),
(r"Développer $3(2x-5)$.",r"On distribue 3 : $\res{6x-15}$.","assert expand(3*(2*x-5))==6*x-15"),
(r"Résoudre $4x+3=19$.",r"$4x=16$, donc $\res{x=4}$.","assert solve(4*x+3-19,x)==[4]"),
(r"Calculer 15\,\% de 80.",r"$\frac{15}{100}\times80=\res{12}$.","assert Rational(15,100)*80==12"),
(r"Par quel nombre multiplie-t-on un prix pour l’augmenter de 8\,\% ?",r"Le coefficient multiplicateur vaut $1+\frac8{100}=\res{1{,}08}$.","assert 1+Rational(8,100)==Rational('1.08')"),
(r"Donner la médiane de la série 2, 5, 8, 9, 12.",r"La troisième valeur est centrale : $\res8$.","assert sorted([2,5,8,9,12])[2]==8"),
(r"Une probabilité vaut 0,7. Donner celle de l’événement contraire.",r"$1-0{,}7=\res{0{,}3}$.","assert 1-Rational('.7')==Rational('.3')")
],[
Probleme('Deux ateliers',r"Un atelier demande 12 euros d’inscription puis 4 euros par séance. Un autre atelier demande 7 euros par séance, sans inscription."+Q(
r"Exprimer les deux dépenses $A(n)$ et $B(n)$ pour $n$ séances.",
r"Pour combien de séances sont-elles égales ? Donner le prix commun.",
r"Pour huit séances, on réduit de 10\,\% le prix total du premier atelier. Comparer les deux coûts."),
r'''\editionEtape{1 · Modéliser}$A(n)=12+4n$ et $B(n)=7n$, en euros. Le premier tarif n’est pas proportionnel au nombre de séances, à cause de la partie fixe.
\editionEtape{2 · Résoudre}$12+4n=7n$ donne $12=3n$, donc $\res{n=4}$. Les deux dépenses valent alors $\res{28}$ euros.
\editionEtape{3 · Appliquer la remise}$A(8)=12+32=44$ euros ; avec le coefficient 0,9, on paie $44\times0{,}9=\res{39{,}60}$ euros. $B(8)=56$ euros. Le premier atelier est moins cher de $\res{16{,}40}$ euros.''',
"assert solve(12+4*x-7*x,x)==[4] and 44*Rational(9,10)==Rational('39.6') and 56-Rational('39.6')==Rational('16.4')"),
Probleme('Un terrain et un arroseur',r"Le terrain ABC est un triangle rectangle en A, avec $AB=6$ m et $AC=8$ m."+Q(
r"Calculer la longueur BC en justifiant.",
r"On veut placer un arroseur à égale distance des trois coins A, B et C. Où le placer ? Quelle portée lui donner pour qu’il atteigne exactement les trois coins ?",
r"Un câble suit $[BC]$ et nécessite 0,5 m de réserve à chaque extrémité. Il coûte 3,20 euros le mètre. Calculer le prix du câble."),
r'''\editionEtape{1 · Pythagore}ABC est rectangle en A : $BC^2=6^2+8^2=100$, donc $\res{BC=10\ \mathrm m}$.
\editionEtape{2 · Le cercle circonscrit}Le point équidistant des trois sommets est le centre du cercle circonscrit. Comme ABC est rectangle en A, c’est le $\res{\text{milieu de }[BC]}$, et la portée vaut $\frac{10}2=\res{5\ \mathrm m}$.
\editionEtape{3 · Les réserves}La longueur achetée est $10+2\times0{,}5=11$ m. Le coût vaut $11\times3{,}20=\res{35{,}20}$ euros. Les réserves s’ajoutent après le calcul de la distance.''',
"assert sqrt(6**2+8**2)==10 and sqrt(6**2+8**2)/2==5 and 11*Rational('3.2')==Rational('35.2')",'bilan-a-geometrie'),
Probleme('Une petite enquête',r"Douze élèves indiquent leur temps de lecture quotidien, en minutes : 5, 10, 10, 10, 15, 15, 20, 20, 20, 25, 25, 30."+Q(
r"Calculer la moyenne au dixième, puis une médiane de la série.",
r"Calculer l’étendue, puis la fréquence des durées d’au moins 20 minutes.",
r"On choisit au hasard un de ces douze élèves. Calculer la probabilité que sa durée soit strictement inférieure à 20 minutes, puis vérifier avec l’événement contraire."),
r'''\editionEtape{1 · Deux indicateurs}La somme vaut 205 min. La moyenne vaut $\frac{205}{12}\approx\res{17{,}1\ \mathrm{min}}$. Les 6e et 7e valeurs sont 15 et 20 : toute valeur entre 15 et 20 est une médiane, par exemple $\res{17{,}5\ \mathrm{min}}$.
\editionEtape{2 · Dispersion et fréquence}L’étendue vaut $30-5=\res{25\ \mathrm{min}}$. Six élèves lisent au moins 20 min : fréquence $\frac6{12}=\res{\frac12}$, soit 50\,\%.
\editionEtape{3 · Le hasard}Les six autres élèves lisent moins de 20 min. Chaque élève ayant la même chance d’être choisi, la probabilité vaut $\res{\frac12}$. L’événement contraire, « au moins 20 min », a pour probabilité $\frac12$ et $1-\frac12=\frac12$.''',
"d=[5,10,10,10,15,15,20,20,20,25,25,30]; assert sum(d)==205 and round(205/12,1)==17.1 and max(d)-min(d)==25 and len([a for a in d if a>=20])==6"),
Probleme('Un cône et un cylindre',r"Un cône a pour rayon 3 cm et pour hauteur 12 cm."+Q(
r"Calculer son volume exact, puis arrondi au dixième de cm$^3$.",
r"Un cylindre a la même base et la même hauteur. Combien de cônes remplis faut-il verser pour remplir ce cylindre ?",
r"Exprimer en mL la capacité du cône et dire si 110 mL de liquide peuvent y tenir."),
r'''\editionEtape{1 · Volume}$V=\frac{\pi\times3^2\times12}3=\res{36\pi\ \mathrm{cm}^3}\approx\res{113{,}1\ \mathrm{cm}^3}$.
\editionEtape{2 · Comparaison}Le cylindre a pour volume $\pi\times9\times12=108\pi$ cm$^3$, soit trois fois le volume du cône : il faut $\res3$ cônes remplis.
\editionEtape{3 · Contenance}Un cm$^3$ vaut un mL : la capacité est d’environ 113,1 mL. Donc $\res{110\ \mathrm{mL}}$ peuvent y tenir, si les dimensions intérieures sont celles données.''',
"assert Rational(3**2*12,3)==36 and round(float(36*pi),1)==113.1 and 9*12==3*36 and 110<36*pi",'bilan-a-cone')
]),
Bilan('B','Choisir une méthode et contrôler',[
(r"Calculer $(-45):9$.",r"Signes contraires : $\res{-5}$.","assert Rational(-45,9)==-5"),
(r"Calculer $\frac25\times\frac{15}{4}$.",r"On simplifie les facteurs : $\res{\frac32}$.","assert Rational(2,5)*Rational(15,4)==Rational(3,2)"),
(r"Simplifier $\frac{36}{48}$.",r"On divise par 12 : $\res{\frac34}$.","assert Rational(36,48)==Rational(3,4)"),
(r"Écrire $5^3\times2^3$ sous la forme d’une puissance de 10.",r"$(5\times2)^3=\res{10^3}$.","assert 5**3*2**3==10**3"),
(r"Encadrer $\sqrt{90}$ entre deux entiers consécutifs.",r"$81<90<100$, donc $\res{9<\sqrt{90}<10}$.","assert 9<sqrt(90)<10"),
(r"Réduire $7x-4-2x+9$.",r"$\res{5x+5}$.","assert expand(7*x-4-2*x+9)==5*x+5"),
(r"Factoriser $12x+18$.",r"Le facteur commun est 6 : $\res{6(2x+3)}$.","assert expand(6*(2*x+3))==12*x+18"),
(r"Résoudre $5x=2x+12$.",r"$3x=12$, donc $\res{x=4}$.","assert solve(5*x-(2*x+12),x)==[4]"),
(r"Convertir 0,025 m$^3$ en litres.",r"$0{,}025\times1\,000=\res{25\ \mathrm L}$.","assert Rational('.025')*1000==25"),
(r"Partager 35 dans le ratio $2:5$.",r"7 parts de 5 : $\res{10\text{ et }25}$.","assert 35//7*2==10 and 35//7*5==25"),
(r"On lance deux pièces équilibrées. Quelle est la probabilité d’obtenir deux faces ?",r"Une issue sur quatre : $\res{\frac14}$.","assert Rational(1,4)==Rational(1,len([(a,b) for a in 'PF' for b in 'PF']))"),
(r"Une translation déplace de 2 carreaux vers la gauche et de 3 vers le haut. Donner l’image du point $(4\,;1)$.",r"$(4-2\,;1+3)=\res{(2\,;4)}$.","assert (4-2,1+3)==(2,4)")
],[
Probleme('Un bassin et deux unités',r"Un bassin contient 720 L. Une pompe le vide à débit constant de $0{,}004$ m$^3$/s."+Q(
r"Convertir le débit en L/s, puis en L/min.",
r"Calculer la durée de vidange en minutes.",
r"Après 1 min 30 s de fonctionnement, calculer le volume restant et la fraction de la capacité initiale qu’il représente."),
r'''\editionEtape{1 · Convertir}$0{,}004$ m$^3$/s $=\res4$ L/s, soit $\res{240}$ L/min.
\editionEtape{2 · Durée}$t=\frac Vq=\frac{720}{240}=\res3$ min. On suppose le débit constant jusqu’à la fin.
\editionEtape{3 · Volume restant}En 90 s, la pompe retire $4\times90=360$ L. Il reste $\res{360\ \mathrm L}$, soit $\frac{360}{720}=\res{\frac12}$ de la capacité initiale.''',
"assert Rational('.004')*1000*60==240 and Rational(720,240)==3 and 720-4*90==360"),
Probleme('Des milieux et un parallélogramme',r"Le triangle ABC a pour côtés $AB=7$ cm, $AC=9$ cm et $BC=12$ cm. I, J et K sont les milieux de $[AB]$, $[AC]$ et $[BC]$."+Q(
r"Démontrer que $(IJ)$ et $(BC)$ sont parallèles, puis calculer IJ.",
r"Démontrer que le quadrilatère IBKJ est un parallélogramme.",
r"Calculer le périmètre de IBKJ."),
r'''\editionEtape{1 · Droite des milieux}Dans ABC, I et J sont les milieux de $[AB]$ et $[AC]$ : $\res{(IJ)\parallel(BC)}$ et $IJ=\frac{12}2=\res{6\ \mathrm{cm}}$.
\editionEtape{2 · Parallélogramme}$(IJ)\parallel(BK)$ car K est sur $[BC]$, et $IJ=6=BK$ car K est le milieu de $[BC]$. Le quadrilatère non croisé IBKJ a deux côtés opposés parallèles et de même longueur : c’est un $\res{\text{parallélogramme}}$.
\editionEtape{3 · Périmètre}$IB=3{,}5$ cm et $BK=6$ cm : le périmètre vaut $2\times(3{,}5+6)=\res{19\ \mathrm{cm}}$.''',
"assert Rational(12,2)==6 and 2*(Rational(7,2)+6)==19",'bilan-b-milieux'),
Probleme('Une série et un tirage',r"Une boîte contient 20 cartes : six cartes portent le nombre 1, huit le nombre 2 et six le nombre 4. Les cartes sont indiscernables au toucher et l’on en tire une au hasard."+Q(
r"Calculer la moyenne et la médiane des nombres inscrits.",
r"Calculer la probabilité d’obtenir un nombre pair, puis celle de l’événement contraire.",
r"On ajoute uniquement des cartes portant 1 pour que la probabilité d’un nombre pair devienne $\frac12$. Combien faut-il en ajouter ?"),
r'''\editionEtape{1 · Statistiques}La moyenne vaut $\frac{6+16+24}{20}=\res{2{,}3}$. Dans la série ordonnée, les 10e et 11e valeurs valent toutes deux 2 : la médiane est $\res2$.
\editionEtape{2 · Probabilités}Il y a $8+6=14$ cartes paires sur 20 : $P(\text{pair})=\res{\frac7{10}}$. L’événement contraire a pour probabilité $\res{\frac3{10}}$.
\editionEtape{3 · Modifier le total}Les 14 cartes paires ne changent pas. Pour représenter la moitié, elles doivent être dans un total de 28 cartes : on ajoute $28-20=\res8$ cartes portant 1. Vérification : $\frac{14}{28}=\frac12$.''',
"assert Rational(6+2*8+4*6,20)==Rational('2.3') and sorted([1]*6+[2]*8+[4]*6)[9:11]==[2,2] and Rational(14,20)==Rational(7,10) and Rational(14,20+8)==Rational(1,2)"),
Probleme('Tripler une variable',r"Le script affiché utilise une seule variable x."+Q(
r"Donner les valeurs de x après chacun des quatre tours.",
r"Exprimer l’affichage avec une puissance, puis le calculer.",
r"On remplace la valeur initiale 2 par une entrée $a$. Quelle entrée donne un affichage de 405 ?"),
r'''\editionEtape{1 · Suivi}À partir de 2, les tours donnent $\res{6,\ 18,\ 54,\ 162}$. La valeur initiale 2 n’est pas un tour.
\editionEtape{2 · Puissance}Quatre multiplications par 3 donnent $2\times3^4=2\times81=\res{162}$.
\editionEtape{3 · Remonter le calcul}Avec une entrée $a$, l’affichage vaut $81a$. L’équation $81a=405$ donne $\res{a=5}$. Contrôle : $5\times3^4=405$.''',
"assert [2*3**k for k in range(1,5)]==[6,18,54,162] and Rational(405,81)==5",'bilan-b-script')
])
]
