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

bareme=r"\par\medskip{\small\color{otMuted}Barème : question 1 : 1 pt ; question 2 : 1 pt ; question 3 : 1 pt ; maîtrise de la langue et clarté de la rédaction : 0,5 pt.}"

schema('brevet-A-geo',{'A':(0,0),'B':(6,0),'C':(0,4.5),'M':(2,0),'N':(0,1.5)},
[('A','B'),('B','C'),('C','A'),('M','N')],droits=['A'],
solution=r'\draw[geoReponse](2,0)--(6,0)--(4,1.5)--(0,1.5)--cycle;\fill[otGreenDark](4,1.5)circle(1.6pt)node[above right]{$D$};')
schema('brevet-B-geo',{'A':(0,0),'B':(6,0),'C':(0,4)},
[('A','B'),('B','C'),('C','A')],droits=['A'])

BILANS=[
Bilan('A','Relier calculs, modèles et figures',[
(r"Calculer $-7+3\times5$.",r"$\res8$ : la multiplication est prioritaire.","assert -7+3*5==8"),
(r"Calculer $\dfrac23+\dfrac16$.",r"$4/6+1/6=\res{5/6}$.","assert Rational(2,3)+Rational(1,6)==Rational(5,6)"),
(r"Donner la notation scientifique de 450000.",r"$\res{4{,}5\times10^5}$.","assert Rational('4.5')*10**5==450000"),
(r"Résoudre $x^2=81$.",r"$\res{x=-9\text{ ou }x=9}$ : deux solutions opposées.","assert set(solve(x*x-81,x))=={-9,9}"),
(r"Développer $(x+3)^2$.",r"$\res{x^2+6x+9}$.","assert expand((x+3)**2)==x*x+6*x+9"),
(r"Résoudre l’inéquation $-2x\ge8$.",r"$\res{x\le-4}$ : diviser par $-2$ change le sens.","assert solve_univariate_inequality(-2*x>=8,x,relational=False)==Interval(-oo,-4)"),
(r"Calculer 15 \% de 80.",r"$0{,}15\times80=\res{12}$.","assert Rational(15,100)*80==12"),
(r"Pour $f(x)=2x+1$, calculer $f(-2)$.",r"$-4+1=\res{-3}$.","assert 2*(-2)+1==-3"),
(r"Partager 35 € selon le ratio $2:5$.",r"7 parts de 5 € : $\res{10\text{ € et }25\text{ €}}$.","assert 35*Rational(2,7)==10 and 35*Rational(5,7)==25"),
(r"Donner la médiane de $2\,;4\,;5\,;8\,;11$.",r"La troisième valeur est $\res5$.","assert sorted([2,4,5,8,11])[2]==5"),
(r"$P(A)=0{,}5$, $P(B)=0{,}4$ et $P(A\cap B)=0{,}2$. Calculer $P(A\cup B)$.",r"$0{,}5+0{,}4-0{,}2=\res{0{,}7}$.","assert Rational(1,2)+Rational(2,5)-Rational(1,5)==Rational(7,10)"),
(r"ABCD est un parallélogramme. Compléter : $\vect{AB}=\vect{D\ldots}$.",r"$\res{\vect{AB}=\vect{DC}}$ : côtés opposés de même sens.","A,B,C,D=(0,0),(5,0),(7,3),(2,3); assert (B[0]-A[0],B[1]-A[1])==(C[0]-D[0],C[1]-D[1])")
],[
Probleme('Un atelier de carnets',
r"Un atelier possède 168 feuilles bleues et 126 feuilles blanches. Il prépare le plus grand nombre possible de carnets identiques, sans reste. Chaque carnet contient le même nombre de feuilles de chaque couleur."
+Q("Déterminer le nombre maximal de carnets et leur composition.","L’atelier vend chaque carnet 4,50 €. Les fournitures ont coûté 78 €. Calculer le solde si tous les carnets sont vendus.","Un autre atelier vend le carnet 5 €, puis applique 10 \\% de réduction. Comparer son prix unitaire au précédent.")+bareme,
r"\editionEtape{1 · Partager sans reste}Le nombre de carnets divise 168 et 126. $168=2^3\times3\times7$ et $126=2\times3^2\times7$. Le plus grand diviseur commun est $2\times3\times7=42$. On prépare $\res{42\text{ carnets}}$, chacun contenant $\res4$ feuilles bleues et $\res3$ blanches."
r"\editionEtape{2 · Recettes et solde}Les recettes sont $42\times4{,}50=189$ €. Le solde, hors autres frais, est $189-78=\res{111\text{ €}}$."
r"\editionEtape{3 · Une comparaison de prix}Diminuer de 10 \% revient à multiplier par 0,9 : $5\times0{,}9=\res{4{,}50\text{ €}}$. Les prix unitaires sont égaux."
r"\editionRetenir{Le maximum de lots identiques correspond au plus grand diviseur commun, pas au plus petit multiple commun.}",
"assert gcd(168,126)==42 and (168//42,126//42)==(4,3) and 42*Rational('4.5')-78==111 and 5*Rational('.9')==Rational('4.5')"),
Probleme('Une voile divisée',
r"ABC est rectangle en A, AB = 12 m, AC = 9 m. M appartient à [AB] avec AM = 4 m. N appartient à [AC] et (MN) est parallèle à (BC)."
+Q("Calculer BC.","Calculer AN et MN.","On construit le point D, image de N par la translation de vecteur $\\vect{MB}$. Quelle est la nature du quadrilatère MBDN ? Démontrer que D appartient à la droite (BC).")+bareme,
r"\editionEtape{1 · Le triangle rectangle}Le théorème de Pythagore donne $BC^2=12^2+9^2=225$, donc $\res{BC=15\text{ m}}$."
r"\editionEtape{2 · La réduction}Les alignements et le parallélisme permettent d’appliquer le théorème de Thalès : $AM/AB=AN/AC=MN/BC=4/12=1/3$. Ainsi $\res{AN=3\text{ m}}$ et $\res{MN=5\text{ m}}$."
r"\editionEtape{3 · Une translation}Par définition de la translation de vecteur $\vect{MB}$, $\vect{ND}=\vect{MB}$ : $\res{MBDN\text{ est un parallélogramme}}$. Donc $(BD)\parallel(MN)$. Comme $(MN)\parallel(BC)$, les droites (BD) et (BC) sont parallèles et ont le point B en commun : elles sont confondues, et $\res{D\in(BC)}$."
r"\editionRetenir{Deux droites parallèles ayant un point commun sont confondues : c’est un argument classique pour prouver un alignement.}",
"assert 12**2+9**2==15**2 and 9*Rational(1,3)==3 and 15*Rational(1,3)==5 and Rational(8,12)+Rational(3,9)==1",'brevet-A-geo'),
Probleme('Deux locations de matériel',
r"Pour $n$ journées entières de location, A facture $18+7n$ euros et B facture $10n$ euros, pour $1\le n\le15$."
+Q("Calculer les deux prix pour 4 jours. Quelle offre choisir ?","Pour combien de jours les prix sont-ils égaux ? Résoudre l’inéquation $18+7n<10n$ et interpréter le résultat.","Avec un budget de 90 €, déterminer la durée maximale possible chez chaque loueur, en résolvant une inéquation.")+bareme,
r"\editionEtape{1 · Quatre journées}A coûte $18+28=\res{46\text{ €}}$ ; B coûte $\res{40\text{ €}}$. B est moins chère de 6 €."
r"\editionEtape{2 · Le seuil}$18+7n=10n$ donne $3n=18$, donc $\res{n=6}$ ; les deux prix valent 60 €. L’inéquation $18+7n<10n$ équivaut à $18<3n$, soit $n>6$ : $\res{A\text{ est moins chère à partir de 7 jours}}$, B l’est pour moins de 6 jours."
r"\editionEtape{3 · Un budget}Chez A, $18+7n\le90$ équivaut à $n\le72/7\approx10{,}3$ : maximum $\res{10\text{ jours}}$. Chez B, $10n\le90$ équivaut à $n\le9$ : maximum $\res{9\text{ jours}}$. On ne garde que des nombres entiers de jours.",
"assert 18+7*4==46 and solve(18+7*x-10*x,x)==[6] and solve_univariate_inequality(18+7*x<10*x,x,relational=False)==Interval.open(6,oo) and 18+7*10<=90<18+7*11 and 10*9<=90<10*10",'brevet-A-tarifs'),
Probleme('Des scores et un tirage',
r"Une série de 20 essais donne les scores du tableau. On tire ensuite deux boules avec remise dans un sac de 3 boules rouges et 1 bleue, numérotées $R_1$, $R_2$, $R_3$ et $B$ ; les tirages sont faits au hasard."
+tableau(['Score','$0$','$1$','$2$','$3$'],[['Effectif','$2$','$5$','$8$','$5$']])
+Q("Calculer la moyenne, la médiane et les quartiles des scores.","À l’aide du tableau des couples, calculer la probabilité d’obtenir deux boules rouges.","Calculer la probabilité d’obtenir exactement une boule bleue, puis celle d’obtenir au moins une boule rouge.")+bareme,
r"\editionEtape{1 · La série}La somme pondérée vaut $0+5+16+15=36$, donc la moyenne vaut $\res{1{,}8}$. Les effectifs cumulés sont 2, 7, 15, 20. Les rangs 10 et 11 valent 2 : médiane $\res2$. $Q_1$ est la 5\textsuperscript{e} valeur : $\res{Q_1=1}$ ; $Q_3$ est la 15\textsuperscript{e} : $\res{Q_3=2}$."
r"\editionEtape{2 · Deux rouges}Le tableau compte $4\times4=16$ couples équiprobables, dont $3\times3=9$ formés de deux rouges : $\res{9/16}$."
r"\editionEtape{3 · Une bleue, au moins une rouge}Exactement une bleue : $3+3=6$ couples, soit $\res{6/16=3/8}$. Au moins une rouge est le contraire de « deux bleues », qui ne contient que le couple $(B\,;B)$ : $\res{1-1/16=15/16}$.",
"v=[0]*2+[1]*5+[2]*8+[3]*5; assert Rational(sum(v),20)==Rational('1.8') and v[9]==v[10]==2 and v[4]==1 and v[14]==2 and Rational(9,16)==Rational(3,4)**2 and Rational(6,16)==Rational(3,8) and 1-Rational(1,16)==Rational(15,16)",'brevet-A-tableau')
]),
Bilan('B','Choisir une méthode et contrôler',[
(r"Calculer $18-4\times3$.",r"$\res6$.","assert 18-4*3==6"),
(r"Calculer $\dfrac35\div\dfrac9{10}$.",r"$3/5\times10/9=\res{2/3}$.","assert Rational(3,5)/Rational(9,10)==Rational(2,3)"),
(r"Écrire $10^3\times10^{-5}$ comme une puissance de 10.",r"$\res{10^{-2}}$.","assert 3+(-5)==-2"),
(r"Décomposer 60 en produit de facteurs premiers.",r"$\res{2^2\times3\times5}$.","assert factorint(60)=={2:2,3:1,5:1}"),
(r"Factoriser $x^2-49$.",r"$\res{(x-7)(x+7)}$.","assert expand((x-7)*(x+7))==x*x-49"),
(r"Résoudre $(x-3)(2x+1)=0$.",r"$\res{x=3\text{ ou }x=-1/2}$.","assert set(solve((x-3)*(2*x+1),x))=={3,Rational(-1,2)}"),
(r"Augmenter 50 de 12 \%.",r"$50\times1{,}12=\res{56}$.","assert 50*Rational('1.12')==56"),
(r"Pour $g(x)=-3x$, donner l’antécédent de 12.",r"$-3x=12$, donc $\res{-4}$.","assert solve(-3*x-12,x)==[-4]"),
(r"Donner le volume exact d’une boule de rayon 3 cm.",r"$\frac43\pi\times27=\res{36\pi\text{ cm}^3}$.","assert Rational(4,3)*27==36"),
(r"Donner le premier quartile de $1\,;3\,;4\,;6\,;8\,;9\,;12\,;15$.",r"$8\times0{,}25=2$ : la 2\textsuperscript{e} valeur, $\res3$.","assert sorted([1,3,4,6,8,9,12,15])[ceil(8*Rational(1,4))-1]==3"),
(r"Un évènement a une probabilité de 0,3. Donner celle de son contraire.",r"$1-0{,}3=\res{0{,}7}$.","assert 1-Rational('.3')==Rational('.7')"),
(r"Simplifier $\vect{AB}+\vect{BC}$.",r"$\res{\vect{AC}}$, d’après la relation de Chasles.","A,B,C=(0,0),(3,1),(5,4); assert (B[0]-A[0]+C[0]-B[0],B[1]-A[1]+C[1]-B[1])==(C[0]-A[0],C[1]-A[1])")
],[
Probleme('Un abri et sa pente',
r"Un toit est représenté par ABC rectangle en A. AB = 4 m horizontalement, AC = 2,5 m verticalement et BC est le versant. L’abri a une longueur de 6 m perpendiculaire au dessin."
+Q("Calculer BC au centimètre.","Calculer l’angle $\\widehat B$ au degré.","Le versant rectangulaire doit être couvert. Ajouter 8 \\% à son aire pour les découpes ; chaque plaque couvre 2 m$^2$. Combien de plaques au minimum ? Utiliser la longueur BC non arrondie.")+bareme,
r"\editionEtape{1 · Longueur du versant}$BC^2=4^2+2{,}5^2=22{,}25$, donc $BC=\sqrt{22{,}25}\approx\res{4{,}72\text{ m}}$."
r"\editionEtape{2 · Angle de pente}$\tan\widehat B=2{,}5/4=0{,}625$. La fonction inverse donne $\widehat B\approx32{,}005^\circ$, soit $\res{32^\circ}$."
r"\editionEtape{3 · Achat entier}L’aire utile vaut $6\sqrt{22{,}25}\approx28{,}3019$ m$^2$. Avec les découpes, on multiplie par 1,08 : environ 30,5660 m$^2$. Le nombre de plaques doit être au moins $30{,}5660/2\approx15{,}283$. Il faut $\res{16\text{ plaques}}$. Quinze ne couvriraient que 30 m$^2$.",
"assert round(math.sqrt(22.25),2)==4.72 and round(math.degrees(math.atan(2.5/4)))==32 and ceil(6*math.sqrt(22.25)*1.08/2)==16",'brevet-B-geo'),
Probleme('Une bouteille et une boule',
r"Une bouteille est modélisée par un cylindre de rayon intérieur 4 cm et de hauteur utile 20 cm. Une machine la remplit à 50 mL/s, à débit constant."
+Q("Calculer la capacité exacte en cm$^3$, puis l’arrondir au mL.","Calculer la durée nécessaire pour remplir 90 \\% de la capacité, au dixième de seconde.","On verse le contenu d’une bouteille pleine dans un récipient en forme de boule de rayon intérieur 7 cm. Le récipient est-il assez grand ? Quel pourcentage de son volume est rempli, à l’unité près ?")+bareme,
r"\editionEtape{1 · Capacité}Le volume vaut $\pi\times4^2\times20=\res{320\pi\text{ cm}^3}$. Un cm$^3$ vaut un mL : capacité $\res{1005\text{ mL}}$ au mL."
r"\editionEtape{2 · Remplissage}Le volume visé vaut $0{,}9\times320\pi=288\pi$ mL. La durée vaut $288\pi/50\approx\res{18{,}1\text{ s}}$."
r"\editionEtape{3 · Une boule}Le récipient a un volume de $\frac43\pi\times7^3=\frac{1372\pi}3\approx1436{,}8$ cm$^3$, supérieur à $1005$ cm$^3$ : $\res{\text{il est assez grand}}$. La part remplie vaut $\dfrac{320\pi}{1372\pi/3}=\dfrac{240}{343}\approx\res{70\,\%}$.",
"assert round(320*math.pi)==1005 and round(288*math.pi/50,1)==18.1 and Rational(4,3)*7**3==Rational(1372,3) and Rational(320)/(Rational(1372,3))==Rational(240,343) and round(240/343*100)==70",'brevet-B-cylindre'),
Probleme('Un script de figures',
r"Le projet démarre stylo baissé, orienté vers la droite. Le bloc carré(c) trace un carré de côté c et revient au départ avec l’orientation initiale. Le programme principal est donné ci-dessous."
+Q("Donner les côtés successifs des carrés tracés et le nombre de passages dans la boucle.","Calculer la somme des périmètres tracés.","Donner la valeur affichée à la fin et la distance totale parcourue stylo relevé. Expliquer pourquoi cette valeur finale de c n’est pas le côté d’un carré tracé.")+bareme,
r"\editionEtape{1 · Une variable à chaque tour}Les carrés ont pour côtés $\res{10,15,20,25}$ unités : l’ajout de 5 vient après le tracé. Après le quatrième tour, c vaut 30 et la condition $c>25$ devient vraie : $\res{4\text{ passages}}$."
r"\editionEtape{2 · Longueur dessinée}La somme des côtés vaut 70. Les périmètres totalisent $4\times70=\res{280}$ unités."
r"\editionEtape{3 · État final}Le script affiche $\res{30}$. Les déplacements sans tracer valent $c+5$ à chaque tour, soit 15, 20, 25, 30 : leur somme vaut $\res{90}$ unités. La boucle s’arrête dès que $c>25$ ; aucun appel carré(30) n’est exécuté.",
"assert sum([10,15,20,25])*4==280 and sum([15,20,25,30])==90 and 10+4*5==30",'brevet-B-script'),
Probleme('Un jeu à deux étapes',
r"Une roue possède quatre secteurs égaux : trois portent la lettre A, un porte la lettre B. Un sac contient une boule rouge et une bleue. On tourne la roue, puis on tire une boule au hasard, indépendamment de la roue. Le joueur gagne s’il obtient A et rouge, ou B et bleue. Les secteurs A sont numérotés A1, A2, A3 dans le tableau."
+Q("Combien d’issues équiprobables compte l’expérience ? Calculer la probabilité de gagner.","Sur 100 parties, peut-on garantir exactement 50 gains ? Expliquer.","On note E : « la roue donne A » et F : « la boule est rouge ». Calculer $P(E)$, $P(F)$, $P(E\\cap F)$, puis $P(E\\cup F)$.")+bareme,
r"\editionEtape{1 · Dénombrer}Le tableau donne $4\times2=\res{8\text{ issues équiprobables}}$. Les issues gagnantes sont A1-rouge, A2-rouge, A3-rouge et B-bleue : $P(G)=4/8=\res{1/2}$."
r"\editionEtape{2 · Fréquence et probabilité}$\res{\text{Non}}$ : sur une série de 100 parties, le nombre de gains varie d’une série à l’autre. La probabilité $1/2$ indique que la fréquence des gains se stabilise autour de 0,5 quand le nombre de parties devient très grand."
r"\editionEtape{3 · Réunion}$P(E)=6/8=3/4$, $P(F)=4/8=1/2$ et $E\cap F$ contient 3 issues : $P(E\cap F)=3/8$. La relation du cours donne $P(E\cup F)=3/4+1/2-3/8=\res{7/8}$. Contrôle : seule l’issue B-bleue n’est ni dans E ni dans F.",
"assert Rational(4,8)==Rational(1,2) and Rational(3,4)+Rational(1,2)-Rational(3,8)==Rational(7,8) and 1-Rational(1,8)==Rational(7,8)",'brevet-B-tableau')
])
]
