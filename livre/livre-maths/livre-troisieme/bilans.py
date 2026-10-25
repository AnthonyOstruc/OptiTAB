from dataclasses import dataclass
from modele import Q,tableau
from donnees_figures import schema
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

bareme=r"\par\medskip{\small\color{otMuted}Barème : question 1 : 1 pt ; question 2 : 1 pt ; question 3 : 1 pt ; clarté de la rédaction : 0,5 pt.}"

schema('brevet-A-geo',{'A':(0,0),'B':(6,0),'C':(0,4.5),'M':(2,0),'N':(0,1.5)},
[('A','B'),('B','C'),('C','A'),('M','N')],droits=['A'])
schema('brevet-B-geo',{'A':(0,0),'B':(6,0),'C':(0,4)},
[('A','B'),('B','C'),('C','A')],droits=['A'])

BILANS=[
Bilan('A','Relier calculs, modèles et figures',[
(r"Calculer $-7+3\times5$.",r"$\res8$ : la multiplication est prioritaire.","assert -7+3*5==8"),
(r"Calculer $2/3+1/6$.",r"$4/6+1/6=\res{5/6}$.","assert Rational(2,3)+Rational(1,6)==Rational(5,6)"),
(r"Donner l’écriture scientifique de 450000.",r"$\res{4{,}5\times10^5}$.","assert Rational('4.5')*10**5==450000"),
(r"Donner $\sqrt{81}$.",r"$\res9$, la racine carrée est positive.","assert sqrt(81)==9"),
(r"Développer $3(x-4)$.",r"$\res{3x-12}$.","assert expand(3*(x-4))==3*x-12"),
(r"Résoudre $5x=35$.",r"$\res{x=7}$.","assert solve(5*x-35,x)==[7]"),
(r"Calculer 15 \% de 80.",r"$0{,}15\times80=\res{12}$.","assert Rational(15,100)*80==12"),
(r"Pour $f(x)=2x+1$, calculer $f(-2)$.",r"$-4+1=\res{-3}$.","assert 2*(-2)+1==-3"),
(r"Convertir 0,25 h en minutes.",r"$0{,}25\times60=\res{15\text{ min}}$.","assert Rational(1,4)*60==15"),
(r"Donner la médiane de $2;4;5;8;11$.",r"La troisième valeur est $\res5$.","assert sorted([2,4,5,8,11])[2]==5"),
(r"On tire au hasard dans un sac de 2 rouges et 3 bleues. Donner la probabilité de bleu.",r"$\res{3/5}$, car il y a cinq boules équiprobables.","assert Rational(3,5)==Rational('.6')"),
(r"Un carré a un côté de 3 cm. Donner son aire.",r"$3^2=\res{9\text{ cm}^2}$.","assert 3**2==9")
],[
Probleme('Un atelier de carnets',
r"Un atelier possède 168 feuilles bleues et 126 feuilles blanches. Il prépare le plus grand nombre possible de carnets identiques, sans reste. Chaque carnet contient le même nombre de feuilles de chaque couleur."
+Q("Déterminer le nombre maximal de carnets et leur composition.","L’atelier vend chaque carnet 4,50 €. Les fournitures ont coûté 78 €. Calculer le solde si tous les carnets sont vendus.","Un autre atelier vend le carnet 5 €, puis applique 10 \\% de réduction. Comparer son prix unitaire au précédent.")+bareme,
r"\editionEtape{1 · Partager sans reste}Le nombre de carnets divise 168 et 126. $168=2^3\times3\times7$ et $126=2\times3^2\times7$. Le plus grand diviseur commun est $2\times3\times7=42$. On prépare $\res{42\text{ carnets}}$, chacun contenant $\res4$ feuilles bleues et $\res3$ blanches."
r"\editionEtape{2 · Recettes et solde}Les recettes sont $42\times4{,}50=189$ €. Le solde, hors autres frais, est $189-78=\res{111\text{ €}}$."
r"\editionEtape{3 · Une comparaison de prix}$5\times0{,}9=\res{4{,}50\text{ €}}$ : les prix unitaires sont égaux. La réduction s’applique au prix de 5 €."
r"\editionRetenir{Le maximum de lots identiques correspond au plus grand diviseur commun, pas au plus petit multiple commun.}",
"assert gcd(168,126)==42 and (168//42,126//42)==(4,3) and 42*Rational('4.5')-78==111 and 5*Rational('.9')==Rational('4.5')"),
Probleme('Une voile divisée',
r"ABC est rectangle en A, AB = 12 m, AC = 9 m. M appartient à [AB] avec AM = 4 m. N appartient à [AC] et MN est parallèle à BC."
+Q("Calculer BC.","Calculer AN et MN.","Calculer l’aire de ABC puis celle du quadrilatère MBCN.")+bareme,
r"\editionEtape{1 · Le triangle rectangle}Pythagore donne $BC^2=12^2+9^2=225$, donc $\res{BC=15\text{ m}}$."
r"\editionEtape{2 · La réduction}Les alignements et le parallélisme permettent Thalès : $AM/AB=AN/AC=MN/BC=4/12=1/3$. Ainsi $\res{AN=3\text{ m}}$ et $\res{MN=5\text{ m}}$."
r"\editionEtape{3 · Les aires}ABC a pour aire $12\times9/2=54$ m$^2$. AMN a pour aire $4\times3/2=6$ m$^2$. Le quadrilatère a donc pour aire $\res{48\text{ m}^2}$."
r"\editionRetenir{Le rapport des aires est $1/9$, carré du rapport des longueurs $1/3$.}",
"assert 12**2+9**2==15**2 and 9*Rational(1,3)==3 and 15*Rational(1,3)==5 and 12*9/2-4*3/2==48",'brevet-A-geo'),
Probleme('Deux locations de matériel',
r"Pour n journées entières de location, A facture $18+7n$ euros et B facture $10n$ euros, pour $1\le n\le15$."
+Q("Calculer les deux prix pour 4 jours. Quelle offre choisir ?","Pour combien de jours les prix sont-ils égaux ? Préciser l’offre la moins chère avant et après ce nombre.","Avec 90 €, déterminer la durée maximale possible chez chaque loueur. Justifier les deux maximums.")+bareme,
r"\editionEtape{1 · Quatre journées}A coûte $18+28=\res{46\text{ €}}$ ; B coûte $\res{40\text{ €}}$. B est moins chère de 6 €."
r"\editionEtape{2 · Le seuil}$18+7n=10n$ donne $3n=18$, donc $\res{n=6}$ ; les deux prix valent 60 €. La différence A moins B est $18-3n$. Elle est positive avant 6 : B est moins chère. Elle est négative après 6 : A est moins chère."
r"\editionEtape{3 · Un budget}Chez A, 10 jours coûtent 88 € et 11 jours 95 € : maximum $\res{10\text{ jours}}$. Chez B, 9 jours coûtent 90 € et 10 jours 100 € : maximum $\res{9\text{ jours}}$. Les deux tarifs augmentent avec n, ce qui justifie les maximums.",
"assert 18+7*4==46 and solve(18+7*x-10*x,x)==[6] and 18+7*10<=90<18+7*11 and 10*9<=90<10*10",'brevet-A-tarifs'),
Probleme('Des essais et un tirage',
r"Une série de 20 essais donne les scores du tableau. On tire ensuite deux boules avec remise dans un sac de 3 rouges et 1 bleue. Les tirages sont réalisés au hasard, avec mélange à chaque étape."
+tableau(['Score','$0$','$1$','$2$','$3$'],[['Effectif','$2$','$5$','$8$','$5$']])
+Q("Calculer la moyenne et la médiane des scores.","Calculer la probabilité d’obtenir deux rouges.","Calculer la probabilité d’obtenir exactement une bleue. Comparer à la probabilité de deux rouges.")+bareme,
r"\editionEtape{1 · La série}La somme pondérée vaut $0+5+16+15=36$, donc la moyenne vaut $\res{1{,}8}$. Les effectifs cumulés sont 2, 7, 15, 20 ; les rangs 10 et 11 valent 2 : médiane $\res2$."
r"\editionEtape{2 · Deux rouges}La remise maintient la composition du sac. Le chemin RR a pour poids $(3/4)^2=\res{9/16}$."
r"\editionEtape{3 · Exactement une bleue}Les chemins RB et BR valent chacun $3/4\times1/4=3/16$. Leur somme est $\res{6/16=3/8}$. Elle est inférieure à $9/16$, de $3/16$. Le chemin BB est exclu par « exactement une ». ",
"assert Rational(0*2+1*5+2*8+3*5,20)==Rational('1.8') and Rational(3,4)**2==Rational(9,16) and 2*Rational(3,4)*Rational(1,4)==Rational(3,8)",'brevet-A-arbre')
]),
Bilan('B','Choisir une méthode et contrôler',[
(r"Calculer $18-4\times3$.",r"$\res6$.","assert 18-4*3==6"),
(r"Calculer $(3/5)\div(9/10)$.",r"$3/5\times10/9=\res{2/3}$.","assert Rational(3,5)/Rational(9,10)==Rational(2,3)"),
(r"Écrire $10^3\times10^{-5}$ comme une puissance de 10.",r"$\res{10^{-2}}$.","assert 3+(-5)==-2"),
(r"Décomposer 60 en facteurs premiers.",r"$\res{2^2\times3\times5}$.","assert factorint(60)=={2:2,3:1,5:1}"),
(r"Factoriser $x^2-49$.",r"$\res{(x-7)(x+7)}$.","assert expand((x-7)*(x+7))==x*x-49"),
(r"Résoudre $x+8=3$.",r"$\res{x=-5}$.","assert solve(x+8-3,x)==[-5]"),
(r"Augmenter 50 de 12 \%.",r"$50\times1{,}12=\res{56}$.","assert 50*Rational('1.12')==56"),
(r"Pour $g(x)=-3x$, donner l’antécédent de 12.",r"$-3x=12$, donc $\res{-4}$.","assert solve(-3*x-12,x)==[-4]"),
(r"Convertir 2,4 m$^3$ en litres.",r"$\res{2400\text{ L}}$.","assert Rational('2.4')*1000==2400"),
(r"Donner l’étendue de $-2;1;4;9$.",r"$9-(-2)=\res{11}$.","assert 9-(-2)==11"),
(r"Un événement a une probabilité de 0,3. Donner celle de son contraire.",r"$1-0{,}3=\res{0{,}7}$.","assert 1-Rational('.3')==Rational('.7')"),
(r"Une longueur de 8 cm est réduite avec un rapport de $-0{,}5$. Donner la longueur de son image.",r"$8\times0{,}5=\res{4\text{ cm}}$.","assert 8*abs(Rational(-1,2))==4")
],[
Probleme('Un abri et sa pente',
r"Un toit est représenté par ABC rectangle en A. AB = 4 m horizontalement, AC = 2,5 m verticalement et BC est le versant. L’abri a une longueur de 6 m perpendiculaire au dessin."
+Q("Calculer BC au centimètre.","Calculer l’angle B au degré.","Le versant rectangulaire doit être couvert. Ajouter 8 \\% à son aire pour les découpes ; chaque plaque couvre 2 m$^2$. Combien de plaques au minimum ? Utiliser la longueur BC non arrondie.")+bareme,
r"\editionEtape{1 · Longueur du versant}$BC^2=4^2+2{,}5^2=22{,}25$, donc $BC=\sqrt{22{,}25}\approx\res{4{,}72\text{ m}}$."
r"\editionEtape{2 · Angle de pente}$\tan B=2{,}5/4=0{,}625$. La fonction inverse donne $B\approx32{,}005^\circ$, soit $\res{32^\circ}$."
r"\editionEtape{3 · Achat entier}L’aire utile vaut $6\sqrt{22{,}25}\approx28{,}3019$ m$^2$. Avec les découpes : environ 30,5660 m$^2$. Le nombre de plaques doit être au moins $30{,}5660/2\approx15{,}283$. Il faut $\res{16\text{ plaques}}$. Quinze ne couvriraient que 30 m$^2$.",
"assert round(math.sqrt(22.25),2)==4.72 and round(math.degrees(math.atan(2.5/4)))==32 and ceil(6*math.sqrt(22.25)*1.08/2)==16",'brevet-B-geo'),
Probleme('Une bouteille et un débit',
r"Une bouteille est modélisée par un cylindre de rayon intérieur 4 cm et de hauteur utile 20 cm. Une machine la remplit à 50 mL/s, à débit constant."
+Q("Calculer la capacité exacte en cm$^3$, puis l’arrondir au mL.","Calculer la durée nécessaire pour remplir 90 \\% de la capacité, au dixième de seconde.","Une version réduite a toutes ses longueurs multipliées par 0,75. Calculer sa capacité au mL et expliquer pourquoi elle ne vaut pas 75 \\% de l’ancienne.")+bareme,
r"\editionEtape{1 · Capacité}Le volume vaut $\pi\times4^2\times20=\res{320\pi\text{ cm}^3}$. Un cm$^3$ vaut un mL : capacité $\res{1005\text{ mL}}$ au mL."
r"\editionEtape{2 · Remplissage}Le volume visé vaut $0{,}9\times320\pi=288\pi$ mL. La durée vaut $288\pi/50\approx\res{18{,}1\text{ s}}$."
r"\editionEtape{3 · Réduction}Le facteur de volume est $0{,}75^3=0{,}421875$. La nouvelle capacité vaut $135\pi$ mL, soit $\res{424\text{ mL}}$. Elle représente 42,1875 \% de la première ; 75 \% est le facteur des seules longueurs.",
"assert round(320*math.pi)==1005 and round(288*math.pi/50,1)==18.1 and 320*Rational(3,4)**3==135 and round(135*math.pi)==424",'brevet-B-cylindre'),
Probleme('Un script de figures',
r"Le projet démarre stylo baissé, orienté vers la droite. Le bloc carré(c) trace un carré de côté c et revient au départ avec l’orientation initiale. Le programme met c à 10, puis répète quatre fois : carré(c) ; relever le stylo ; avancer de c + 5 ; baisser le stylo ; ajouter 5 à c."
+Q("Donner les côtés successifs des quatre carrés.","Calculer la somme des périmètres tracés.","Donner la valeur finale de c et la distance totale avancée stylo relevé. Expliquer pourquoi la valeur finale de c n’est pas le côté d’un cinquième carré tracé.")+bareme,
r"\editionEtape{1 · Une variable à chaque tour}Les carrés utilisent successivement $\res{10,15,20,25}$ unités : l’ajout de 5 vient après le tracé."
r"\editionEtape{2 · Longueur dessinée}La somme des côtés vaut 70. Les périmètres totalisent $4\times70=\res{280}$ unités."
r"\editionEtape{3 · État final}Après le quatrième ajout, c vaut $\res{30}$. Les déplacements sans tracer valent 15, 20, 25, 30, donc leur somme vaut $\res{90}$ unités. La boucle s’arrête après quatre tours ; aucun appel carré(30) n’est exécuté.",
"assert sum([10,15,20,25])*4==280 and sum([15,20,25,30])==90 and 10+4*5==30",'brevet-B-script'),
Probleme('Un jeu à deux étapes',
r"Une roue possède quatre secteurs égaux : trois portent A, un porte B. Un sac contient une boule rouge et une bleue. On tourne la roue, puis on tire une boule au hasard, indépendamment de la roue. Le joueur gagne sur A-rouge ou B-bleue."
+Q("Calculer la probabilité de chacun des deux chemins gagnants.","En déduire la probabilité de gagner. Sur 100 parties, peut-on garantir exactement 50 gains ?","Un gain rapporte 6 points, la participation coûte 2 points. Selon la règle « moyenne théorique = somme des bilans multipliés par leurs probabilités », calculer le bilan net moyen par partie.")+bareme,
r"\editionEtape{1 · Chemins}A-rouge a pour poids $3/4\times1/2=\res{3/8}$. B-bleue a pour poids $1/4\times1/2=\res{1/8}$."
r"\editionEtape{2 · Événement gagnant}Les chemins sont incompatibles : $P(G)=3/8+1/8=\res{1/2}$. Une série finie peut avoir un nombre différent de 50 gains ; 50 est une valeur moyenne théorique sur 100, pas une garantie."
r"\editionEtape{3 · Bilan net}En cas de gain, le bilan net est $6-2=4$ points ; sinon il est $-2$. Le bilan moyen vaut $4\times1/2+(-2)\times1/2=\res{1\text{ point}}$. Il ne correspond pas à un résultat certain d’une partie.",
"assert Rational(3,4)*Rational(1,2)+Rational(1,4)*Rational(1,2)==Rational(1,2) and 4*Rational(1,2)-2*Rational(1,2)==1",'brevet-B-arbre')
])
]
