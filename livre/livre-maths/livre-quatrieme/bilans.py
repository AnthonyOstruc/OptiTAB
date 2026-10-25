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
(r"Calculer $\frac34+\frac18$.",r"$6/8+1/8=\res{7/8}$.","assert Rational(3,4)+Rational(1,8)==Rational(7,8)"),
(r"Donner l’inverse de $-2/5$.",r"L’inverse est $\res{-5/2}$ ; le produit des deux vaut 1.","assert Rational(-2,5)*Rational(-5,2)==1"),
(r"Écrire $0{,}00046$ en notation scientifique.",r"$\res{4{,}6\times10^{-4}}$.","assert Rational('4.6')/10**4==Rational('.00046')"),
(r"Donner $\sqrt{121}$.",r"$11^2=121$ et $11\ge0$, donc $\res{11}$.","assert sqrt(121)==11"),
(r"Développer $3(2x-5)$.",r"Distribuer 3 : $\res{6x-15}$.","assert expand(3*(2*x-5))==6*x-15"),
(r"Résoudre $4x+3=19$.",r"$4x=16$, donc $\res{x=4}$.","assert solve(4*x+3-19,x)==[4]"),
(r"Calculer 15\,\% de 80.",r"$15\times80/100=\res{12}$.","assert Rational(15,100)*80==12"),
(r"Convertir 54 km/h en m/s.",r"$54/3{,}6=\res{15\ \mathrm{m/s}}$.","assert 54/Rational('3.6')==15"),
(r"Donner la médiane de 2, 5, 8, 9, 12.",r"La troisième valeur est centrale : $\res8$.","assert [2,5,8,9,12][2]==8"),
(r"Une probabilité vaut 0,7. Donner celle de l’événement contraire.",r"$1-0{,}7=\res{0{,}3}$.","assert 1-Rational('.7')==Rational('.3')")
],[
Probleme('Un atelier et ses achats',r"Un atelier demande 12 euros d’inscription puis 4 euros par séance. Un autre atelier demande 7 euros par séance sans inscription."+Q(
r"Exprimer les deux dépenses pour $n$ séances.",
r"Pour combien de séances sont-elles égales ? Donner le prix commun.",
r"Pour huit séances, on réduit de 10\,\% le prix total du premier atelier. Comparer les deux coûts."),
r'''\editionEtape{1 · Modéliser}Les prix sont $A=12+4n$ et $B=7n$ euros. Le premier tarif n’est pas proportionnel au nombre de séances à cause de la partie fixe.
\editionEtape{2 · Résoudre}$12+4n=7n$ donne $12=3n$, donc $\res{n=4}$. Les deux dépenses valent $\res{28}$ euros.
\editionEtape{3 · Appliquer la remise}Pour huit séances, A vaut $12+32=44$ euros. La remise est 4,40 euros, donc A coûte $\res{39{,}60}$ euros. B coûte $7\times8=56$ euros. A est moins cher de $\res{16{,}40}$ euros.''',
"assert solve(12+4*x-7*x,x)==[4] and 44*Rational(9,10)==Rational('39.6') and 56-Rational('39.6')==Rational('16.4')"),
Probleme('Un terrain et un câble',r"ABC est rectangle en A avec $AB=6$ m et $AC=8$ m."+Q(
r"Calculer la longueur BC en justifiant.",
r"Calculer l’angle ABC au degré près.",
r"Un câble suit BC et nécessite 0,5 m de réserve à chaque bout. Il coûte 3,20 euros par mètre. Calculer le prix."),
r'''\editionEtape{1 · Pythagore}$BC^2=6^2+8^2=100$, donc $\res{BC=10\ \mathrm m}$. L’hypoténuse dépasse les deux côtés de l’angle droit.
\editionEtape{2 · Cosinus}$\cos\widehat{ABC}=AB/BC=6/10=0{,}6$. En degrés, $\widehat{ABC}=\arccos(0{,}6)\approx\res{53^\circ}$.
\editionEtape{3 · Les réserves}La longueur achetée est $10+2\times0{,}5=11$ m. Le coût vaut $11\times3{,}20=\res{35{,}20}$ euros. Les réserves s’ajoutent après le calcul de la distance.''',
"assert sqrt(6**2+8**2)==10 and round(math.degrees(math.acos(.6)))==53 and 11*Rational('3.2')==Rational('35.2')",'bilan-a-geometrie'),
Probleme('Une petite enquête',r"Douze élèves indiquent leur temps de lecture quotidien en minutes : 5, 10, 10, 10, 15, 15, 20, 20, 20, 25, 25, 30."+Q(
r"Calculer la moyenne et la médiane choisie dans le livre.",
r"Calculer la fréquence des durées d’au moins 20 min et l’angle correspondant dans un diagramme circulaire.",
r"On choisit au hasard un des douze élèves. Calculer la probabilité d’une durée strictement inférieure à 20 min, puis vérifier avec l’événement contraire."),
r'''\editionEtape{1 · Deux indicateurs}La somme est 205 min. La moyenne vaut $\res{205/12\ \mathrm{min}}\approx17{,}08$ min. Les rangs 6 et 7 sont 15 et 20 ; la médiane choisie vaut $\res{17{,}5}$ min.
\editionEtape{2 · Une part du total}Six élèves lisent au moins 20 min : fréquence $6/12=\res{1/2}$, soit 50\,\%. Le secteur correspondant mesure $\res{180^\circ}$.
\editionEtape{3 · Le hasard}Les six autres ont une durée inférieure à 20 min. Comme chaque élève a la même chance d’être choisi, la probabilité vaut $\res{1/2}$. On retrouve $1-1/2=1/2$ avec le contraire.''',
"assert sum([5,10,10,10,15,15,20,20,20,25,25,30])==205 and Rational(15+20,2)==Rational('17.5') and len([a for a in [5,10,10,10,15,15,20,20,20,25,25,30] if a>=20])==6"),
Probleme('Un cône et sa réduction',r"Un cône a pour rayon 3 cm et pour hauteur 12 cm."+Q(
r"Calculer son volume exact et son volume approché au dixième de cm$^3$.",
r"On réduit toutes les longueurs de moitié. Donner le volume exact du petit cône.",
r"Exprimer en mL la capacité du grand cône et dire si 110 mL peuvent y tenir."),
r'''\editionEtape{1 · Volume}$V=\pi\times3^2\times12/3=\res{36\pi\ \mathrm{cm}^3}\approx\res{113{,}1\ \mathrm{cm}^3}$.
\editionEtape{2 · Réduction}Le facteur de volume vaut $(1/2)^3=1/8$. Le petit cône a pour volume $36\pi/8=\res{4{,}5\pi\ \mathrm{cm}^3}$.
\editionEtape{3 · Contenance}Un cm$^3$ vaut un mL, donc la capacité est d’environ 113,1 mL. $\res{110\ \mathrm{mL}}$ peuvent y tenir dans ce modèle. Les dimensions intérieures sont supposées être celles données.''',
"assert Rational(3**2*12,3)==36 and round(float(36*pi),1)==113.1 and Rational(36,8)==Rational('4.5') and 110<36*pi",'bilan-a-cone')
]),
Bilan('B','Choisir une méthode et contrôler',[
(r"Calculer $(-45):9$.",r"Signes opposés : $\res{-5}$.","assert Rational(-45,9)==-5"),
(r"Calculer $\frac25\times\frac{15}{4}$.",r"Simplifier les facteurs : $\res{3/2}$.","assert Rational(2,5)*Rational(15,4)==Rational(3,2)"),
(r"Décomposer 84 en facteurs premiers.",r"$\res{84=2^2\times3\times7}$.","assert factorint(84)=={2:2,3:1,7:1}"),
(r"Écrire $6{,}2\times10^4$ en écriture décimale.",r"$\res{62\,000}$.","assert Rational('6.2')*10**4==62000"),
(r"Encadrer $\sqrt{90}$ entre deux entiers consécutifs.",r"$81<90<100$, donc $\res{9<\sqrt{90}<10}$.","assert 9<sqrt(90)<10"),
(r"Réduire $7x-4-2x+9$.",r"$\res{5x+5}$.","assert expand(7*x-4-2*x+9)==5*x+5"),
(r"Factoriser $12x+18$.",r"Facteur commun 6 : $\res{6(2x+3)}$.","assert expand(6*(2*x+3))==12*x+18"),
(r"Résoudre $5x=2x+12$.",r"$3x=12$, donc $\res{x=4}$.","assert solve(5*x-(2*x+12),x)==[4]"),
(r"Convertir 0,025 m$^3$ en litres.",r"$0{,}025\times1000=\res{25\ \mathrm L}$.","assert Rational('.025')*1000==25"),
(r"Une longueur passe de 8 à 12 cm par agrandissement. Donner le rapport.",r"$12/8=\res{1{,}5}$.","assert Rational(12,8)==Rational('1.5')"),
(r"Une roue a dix secteurs équiprobables ; trois sont verts. Donner la probabilité de vert.",r"$\res{3/10=0{,}3}$.","assert Rational(3,10)==Rational('.3')"),
(r"Une translation déplace de 2 carreaux à gauche et 3 vers le haut. Donner l’image de (4;1).",r"$(4-2;1+3)=\res{(2;4)}$.","assert (4-2,1+3)==(2,4)")
],[
Probleme('Un bassin et deux unités',r"Un bassin contient 720 L. Une pompe le vide à débit constant de $0{,}004$ m$^3$/s."+Q(
r"Convertir le débit en L/s puis en L/min.",
r"Calculer la durée de vidange en minutes.",
r"Après 1 min 30 s de fonctionnement, calculer le volume restant et sa fraction de la capacité initiale."),
r'''\editionEtape{1 · Convertir}$0{,}004$ m$^3$/s $=\res4$ L/s, soit $\res{240}$ L/min.
\editionEtape{2 · Durée}$t=V/q=720/240=\res3$ min. On suppose le débit constant jusqu’à la fin.
\editionEtape{3 · Volume restant}En 90 s, la pompe retire $4\times90=360$ L. Il reste $\res{360\ \mathrm L}$, soit $360/720=\res{1/2}$ de la capacité initiale. La durée choisie est bien antérieure à l’épuisement.''',
"assert Rational('.004')*1000*60==240 and Rational(720,240)==3 and 720-4*90==360"),
Probleme('Un parallélisme à prouver',r"$M\in[AB]$ et $N\in[AC]$. $AB=10$, $AC=15$, $AM=4$, $AN=6$ et $BC=12$ cm."+Q(
r"Démontrer que MN et BC sont parallèles.",
r"Calculer MN et NC.",
r"Quelle est la proportion de l’aire de ABC représentée par AMN ?"),
r'''\editionEtape{1 · Réciproque}$AM/AB=4/10=2/5$ et $AN/AC=6/15=2/5$. Les points sont dans l’ordre sur les segments. La réciproque de Thalès donne $\res{(MN)\parallel(BC)}$.
\editionEtape{2 · Longueurs}Thalès donne $MN=(2/5)\times12=\res{4{,}8}$ cm. Puis $NC=AC-AN=15-6=\res9$ cm.
\editionEtape{3 · Aire}Les longueurs sont réduites au rapport $2/5$. Le rapport des aires est donc $(2/5)^2=\res{4/25}$, soit 16\,\%. Une aire n’est pas multipliée par le simple rapport des longueurs.''',
"assert Rational(4,10)==Rational(6,15) and 12*Rational(2,5)==Rational('4.8') and Rational(2,5)**2==Rational(4,25)",'bilan-b-thales'),
Probleme('Une série et un tirage',r"Une boîte contient 20 cartes portant des nombres : six cartes portent 1, huit portent 2 et six portent 4. Les cartes sont indiscernables au toucher et l’on tire au hasard."+Q(
r"Calculer la moyenne et la médiane des nombres inscrits.",
r"Calculer la probabilité d’obtenir un nombre pair et celle de son contraire.",
r"On ajoute uniquement des cartes portant 1 pour que la probabilité d’un nombre pair devienne $1/2$. Combien faut-il en ajouter ?"),
r'''\editionEtape{1 · Statistiques}La moyenne vaut $(6+16+24)/20=\res{2{,}3}$. Dans la série ordonnée, les rangs 10 et 11 portent tous deux 2 : médiane $\res2$.
\editionEtape{2 · Probabilités}Il y a $8+6=14$ cartes paires sur 20 : $P(\text{pair})=\res{7/10}$. Le contraire vaut $\res{3/10}$.
\editionEtape{3 · Modifier le total}Les 14 cartes paires ne changent pas. Pour représenter la moitié, elles doivent être dans un total de 28 cartes. On ajoute donc $28-20=\res8$ cartes portant 1. Vérification : $14/28=1/2$.''',
"assert Rational(6+2*8+4*6,20)==Rational('2.3') and Rational(14,20)==Rational(7,10) and Rational(14,20+8)==Rational(1,2)"),
Probleme('Tripler une variable',r"Le script affiché utilise une variable x."+Q(
r"Donner les valeurs de x après chacun des quatre tours.",
r"Exprimer l’affichage avec une puissance et le calculer.",
r"On remplace la valeur initiale 2 par une entrée $a$. Quelle entrée donne un résultat de 405 ?"),
r'''\editionEtape{1 · Suivi}À partir de 2, les tours donnent $\res{6,\ 18,\ 54,\ 162}$. Le premier 2 est une initialisation, pas un tour.
\editionEtape{2 · Puissance}Quatre multiplications par 3 donnent $2\times3^4=2\times81=\res{162}$.
\editionEtape{3 · Remonter le calcul}Avec une entrée $a$, le résultat vaut $81a$. L’équation $81a=405$ donne $\res{a=5}$. Contrôle : $5\times3^4=405$.''',
"assert [2*3**k for k in range(1,5)]==[6,18,54,162] and Rational(405,81)==5",'bilan-b-script')
])
]
