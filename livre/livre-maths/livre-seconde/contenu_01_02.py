from modele import *

chapitre(1,'arithmetique','Arithmétique et nombres entiers','1 · Nombres et calculs',
         'Divisibilité · Parité · Fractions · Raisonnement',
         ['Traduire une divisibilité par une égalité.','Reconnaître les nombres pairs et impairs.','Simplifier une fraction et organiser une preuve.'],
         ['Tables de multiplication et division euclidienne.'],[
r'''\essSection{1}{Multiples, diviseurs et parité}
\begin{definition}
Pour des entiers $a$ et $b$, dire que $a$ est un multiple de $b$ signifie qu'il existe un entier $k$ tel que $a=bk$. On dit aussi que $b$ divise $a$. Un entier pair s'écrit $2k$ ; un entier impair s'écrit $2k+1$, avec $k\in\mathbb Z$.
\end{definition}
\begin{exemple}Les multiples de 6 sont $\ldots,-12,-6,0,6,12,\ldots$. Le nombre 0 est multiple de tout entier. On ne divise jamais par 0.\end{exemple}
\begin{propriete}Si $a$ et $b$ sont multiples de 7, $a+b$ et $a-b$ le sont aussi : écrire $a=7m$ et $b=7n$, puis factoriser 7.\end{propriete}
\begin{savoirfaire}[Prouver une propriété de parité]
Remplacer les entiers par leur écriture générale. Par exemple,
\[(2k+1)^2=4k^2+4k+1=2(2k^2+2k)+1.\]
Le nombre entre parenthèses est entier : le carré d'un impair est impair.
\end{savoirfaire}
\begin{attention}Tester dix exemples peut suggérer une règle. Cela ne démontre pas une affirmation portant sur tous les entiers.\end{attention}''',
r'''\essSection{2}{Fractions et résolution de problèmes}
\begin{definition}Une fraction $a/b$, avec $b\ne0$, est irréductible lorsque le seul diviseur positif commun à $a$ et $b$ est 1.\end{definition}
\begin{savoirfaire}[Simplifier sans changer le nombre]
Diviser numérateur et dénominateur par un même entier non nul. Pour $84/126$, les divisions successives par 2 puis 3 puis 7 donnent $2/3$. Le PGCD permet de le faire en une seule étape.
\end{savoirfaire}
\begin{exemple}[Un multiple dans une plage donnée]
Pour chercher les multiples de 12 entre 90 et 130, écrire $90\le12k\le130$. Les entiers possibles sont $k=8,9,10$ : on obtient 96, 108 et 120.
\end{exemple}
\begin{propriete}Pour $a>0$ et $b\ge0$ entiers, la division euclidienne s’écrit $b=aq+r$ avec $0\le r<a$. Le plus grand multiple de $a$ inférieur ou égal à $b$ est alors $aq$, car $aq\le b<a(q+1)$. En Python, le quotient $q$ s’obtient par \code{b // a} et le multiple par \code{a * (b // a)}.\end{propriete}
\begin{attention}Dans un problème, préciser si l'on cherche des entiers positifs, des entiers relatifs ou des nombres réels. Cette information change l'ensemble des réponses.\end{attention}
\otIntertitre{À expliquer à l'oral}
Pourquoi une fraction peut-elle changer d'écriture sans changer de valeur ? Donner une explication par partage d'une même unité.'''
],[
E('Reconnaître un multiple',Q(r"""Parmi $-36,0,14,42,55$, relever les multiples de 6.""",r"""Écrire chacun d’eux sous la forme $6k$."""),
r"""On cherche un quotient entier par 6. On a $-36=6\times(-6)$, $0=6\times0$ et $42=6\times7$. Les quotients $14/6$ et $55/6$ ne sont pas entiers. Les trois nombres cherchés sont donc $\res{-36,0,42}$.""",
'Tester la définition, y compris pour zéro et les nombres négatifs.','assert [n for n in [-36,0,14,42,55] if n%6==0]==[-36,0,42]'),
E('Diviseurs positifs',r"""Lister tous les diviseurs positifs de 36, puis ceux de 24. Relever leurs diviseurs communs.""",
r"""On regroupe les facteurs par paires. Pour 36 : $1\times36$, $2\times18$, $3\times12$, $4\times9$, $6\times6$. Pour 24 : $1\times24$, $2\times12$, $3\times8$, $4\times6$. Les diviseurs communs sont $\res{1,2,3,4,6,12}$ ; le plus grand est 12.""",
'Former des paires de facteurs sans oublier les petits diviseurs.','assert sorted(set(divisors(36))&set(divisors(24)))==[1,2,3,4,6,12]'),
E('Parité sans calcul lourd',r"""Dire si $2\times137$, $2\times137+1$ et $137^2$ sont pairs ou impairs. Justifier.""",
r"""Le premier nombre est de la forme $2k$ : il est pair. Le deuxième est de la forme $2k+1$ : il est impair. Comme $137=2\times68+1$, son carré est impair d’après la propriété démontrée dans le cours. On peut contrôler : $137^2=18769$.""",
'Reconnaître les écritures générales de la parité.','assert [274%2,275%2,137**2%2]==[0,1,1]'),
E('Rendre irréductible',r"""Simplifier $\dfrac{90}{126}$ et $\dfrac{-132}{84}$ sous forme irréductible.""",
r"""Le PGCD de 90 et 126 est 18 : $90/126=5/7$. Celui de 132 et 84 est 12 : $-132/84=-11/7$. Les couples $(5,7)$ et $(11,7)$ n’ont plus de diviseur commun autre que 1. Les résultats sont $\res{5/7}$ et $\res{-11/7}$.""",
'Diviser les deux termes par leur PGCD.','assert Rational(90,126)==Rational(5,7) and Rational(-132,84)==Rational(-11,7)'),
E('Additionner des fractions',r"""Calculer exactement $A=\dfrac56-\dfrac7{15}+\dfrac1{10}$.""",
r"""Un dénominateur commun est 30 : $A=25/30-14/30+3/30=14/30$. On simplifie par 2. Ainsi $\res{A=7/15}$. L’ordre de grandeur est cohérent : $0{,}83-0{,}47+0{,}10$ vaut environ $0{,}46$.""",
'Choisir un dénominateur commun avant de sommer.','assert Rational(5,6)-Rational(7,15)+Rational(1,10)==Rational(7,15)'),
E('Somme de multiples',r"""Les entiers $a$ et $b$ sont des multiples de 9. Démontrer que $a+b$ et $2a-3b$ sont multiples de 9.""",
r"""Il existe des entiers $m,n$ tels que $a=9m$ et $b=9n$. Alors $a+b=9(m+n)$ et $2a-3b=9(2m-3n)$. Les deux expressions entre parenthèses sont entières. Elles donnent exactement les écritures exigées par la définition de multiple de 9.""",
'Introduire deux entiers, puis factoriser le diviseur commun.','assert all((2*9*m-3*9*n)%9==0 for m in range(-12,13) for n in range(-12,13))'),
E('Deux entiers consécutifs',r"""Démontrer que la somme de deux entiers consécutifs est impaire et que leur produit est pair.""",
r"""Écrire les entiers $n$ et $n+1$. Leur somme est $2n+1$, donc impaire. Pour le produit, distinguer deux cas : si $n$ est pair, il fournit le facteur 2 ; si $n$ est impair, $n+1$ est pair. Dans chaque cas, $n(n+1)$ est multiple de 2.""",
'Utiliser une expression générale, puis une disjonction de cas.','assert all((n+n+1)%2==1 and (n*(n+1))%2==0 for n in range(-100,101))'),
E('Tester une divisibilité en Python',r"""Expliquer les résultats de \code{35 \% 7 == 0} et \code{35 \% 6 == 0}. Écrire une fonction \code{multiple(a,b)} pour $b\ne0$.""",
r"""Le symbole \code{\%} donne le reste de la division. Les deux tests valent respectivement \code{True} et \code{False}, car les restes sont 0 et 5. Une fonction possible est :
\begin{python}
def multiple(a, b):
    return a % b == 0
\end{python}
Le domaine $b\ne0$ doit être respecté lors de l’appel. Cette fonction renvoie un booléen, pas un reste.""",
'Traduire « le reste est nul » en test logique.','assert 35%7==0 and 35%6!=0'),
E('Le dernier multiple',r"""Déterminer le plus grand multiple de 17 inférieur ou égal à 1000. Expliquer le rôle de la division entière.""",
r"""La division euclidienne donne $1000=17\times58+14$. Le multiple cherché est donc $\res{986}$. Le suivant vaut $17\times59=1003>1000$. En Python, \code{1000 // 17} renvoie 58, puis \code{17 * 58} renvoie 986. Les deux comparaisons prouvent que l’on a bien le dernier multiple admissible.""",
'Encadrer le nombre entre deux multiples consécutifs.','assert 17*58<=1000<17*59'),
E('Une affirmation à réfuter',r"""« La somme de deux nombres impairs est toujours un multiple de 4. » Cette affirmation est-elle vraie ? Donner ensuite une propriété correcte.""",
r"""Elle est fausse : $1+5=6$ n’est pas multiple de 4. En revanche, la somme de deux impairs est toujours paire : $(2m+1)+(2n+1)=2(m+n+1)$. Un contre-exemple suffit à réfuter la première phrase ; une écriture générale démontre la seconde.""",
'Séparer réfutation par exemple et preuve générale.','assert (1+5)%4!=0 and all(((2*m+1)+(2*n+1))%2==0 for m in range(8) for n in range(8))'),
E('Des colis identiques',r"""Une association possède 84 cahiers et 126 stylos. Elle veut préparer le plus grand nombre de colis identiques sans reste. Chaque colis doit contenir les deux objets. Combien de colis et quel contenu ?""",
r"""Le nombre de colis doit diviser 84 et 126. Leur PGCD est 42 : il est donc impossible de dépasser 42 colis, et cette valeur convient. Chaque colis contient $84/42=2$ cahiers et $126/42=3$ stylos. La réponse est $\res{42\text{ colis de 2 cahiers et 3 stylos}}$.""",
'Interpréter le nombre de groupes comme un diviseur commun.','assert gcd(84,126)==42 and 84//42==2 and 126//42==3'),
E('Un départ simultané',r"""Deux navettes passent à 8 h au même arrêt, puis toutes les 12 minutes pour l’une et toutes les 18 minutes pour l’autre. À quelle heure se retrouvent-elles pour la première fois après 8 h ?""",
r"""Le temps écoulé doit être un multiple positif de 12 et de 18. Les premiers multiples de 12 sont 12, 24, 36 ; ceux de 18 sont 18, 36. Le plus petit commun est 36. Les navettes se retrouvent donc à $\res{8\text{ h }36}$. On vérifie $36=3\times12=2\times18$.""",
'Chercher le premier multiple commun strictement positif.','assert ilcm(12,18)==36'),
E('Un carré et sa parité',r"""Démontrer que si $n^2$ est pair, alors $n$ est pair. Peut-on conclure de même avec « multiple de 4 » à la place de « pair » dans les deux occurrences ?""",
r"""On raisonne par contraposée : si $n$ était impair, son carré serait impair. Cela prouve la première implication. La seconde formulation est fausse : $n=2$ donne $n^2=4$, multiple de 4, alors que 2 n’est pas multiple de 4. La bonne conclusion reste « $n$ est pair ».""",
'Utiliser une contraposée, puis éprouver une généralisation.','assert all(n%2==0 for n in range(-100,101) if n*n%2==0) and 2**2%4==0 and 2%4!=0'),
E('Un entier mystérieux',r"""Un entier naturel est compris entre 200 et 250. Il est multiple de 6 et de 8. La somme de ses chiffres vaut 9. Le déterminer et justifier l’unicité.""",
r"""Un multiple commun de 6 et de 8 est multiple de 24. Dans l’intervalle demandé, les seuls candidats sont 216 et 240, puisque $24\times8=192$ et $24\times11=264$. Les sommes de chiffres valent 9 et 6. Ainsi $\res{216}$ est l’unique solution.""",
'Réduire d’abord la liste des candidats, puis utiliser la dernière contrainte.','assert [n for n in range(200,251) if n%6==0 and n%8==0 and sum(map(int,str(n)))==9]==[216]'),
E('Une fraction qui se simplifie toujours',r"""Pour un entier $n\ge1$, montrer que $\dfrac{3n+3}{6n+6}$ a une valeur indépendante de $n$. Pourquoi la même écriture ne convient-elle pas pour $n=-1$ ?""",
r"""On factorise : $3n+3=3(n+1)$ et $6n+6=6(n+1)$. Pour $n\ge1$, le facteur $n+1$ est non nul ; il peut être simplifié. On obtient $\res{1/2}$. Pour $n=-1$, le dénominateur est nul : la fraction initiale n’a pas de sens. Une simplification ne rétablit pas une valeur exclue.""",
'Factoriser et contrôler la condition de simplification.','assert simplify((3*x+3)/(6*x+6))==Rational(1,2) and (6*x+6).subs(x,-1)==0')
],reperes=['Multiples, diviseurs et parité','Fractions irréductibles','Somme de multiples et carré impair','Algorithmes de divisibilité'],deco='algorithmique')

chapitre(2,'reels-intervalles','Réels et intervalles','1 · Nombres et calculs',
         'Ensembles de nombres · Encadrements · Distances',
         ['Distinguer valeur exacte et valeur approchée.','Lire et représenter les intervalles.','Traduire une distance sur la droite numérique.'],
         ['Fractions, nombres relatifs et ordre.'],[
r'''\essSection{1}{Les nombres et leurs écritures}
\begin{definition}
$\mathbb N$ contient les entiers naturels, dont 0 ; $\mathbb Z$ les entiers relatifs ; $\mathbb D$ les nombres ayant une écriture décimale finie ; $\mathbb Q$ les quotients d’entiers de dénominateur non nul. Tous appartiennent à $\mathbb R$.
\[\mathbb N\subset\mathbb Z\subset\mathbb D\subset\mathbb Q\subset\mathbb R.\]
Un irrationnel est un réel qui n’appartient pas à $\mathbb Q$, par exemple $\sqrt2$ ou $\pi$.
\end{definition}
\begin{exemple}$3/8=0{,}375$ est décimal ; $1/3$ est rationnel mais non décimal. $\sqrt{25}=5$ est entier : une racine carrée n’est pas toujours irrationnelle.\end{exemple}
\begin{savoirfaire}[Encadrer et arrondir]
Un encadrement $a\le x\le b$ a pour amplitude $b-a$. Pour arrondir au centième, repérer les deux centièmes consécutifs qui encadrent le nombre puis choisir le plus proche. Préciser l’unité et la précision dans un problème de mesure.
\end{savoirfaire}
\begin{attention}Un affichage de calculatrice est souvent approché. $1{,}414$ n’est pas égal à $\sqrt2$ ; écrire $\sqrt2\approx1{,}414$.\end{attention}''',
r'''\essSection{2}{Intervalles et distance}
\begin{definition}
$[a;b]$ contient les réels tels que $a\le x\le b$ ; $]a;b[$ impose $a<x<b$. Un crochet tourné vers le nombre signifie que la borne est incluse. Aux infinis, le crochet est toujours ouvert. Le programme officiel écrit aussi $[a,b]$ ou $[a,+\infty[$ avec une virgule ; ce livre utilise le point-virgule pour éviter toute confusion avec la virgule décimale, comme dans $[1{,}5;2]$.
\end{definition}
\begin{exemple}$x>-2$ s’écrit $x\in]-2;+\infty[$. La réunion $I\cup J$ signifie « dans $I$ ou dans $J$ » ; l’intersection $I\cap J$, « dans les deux ».\end{exemple}
\begin{definition}La valeur absolue $|a|$ est la distance entre $a$ et 0. La distance entre $a$ et $b$ est $|a-b|$. Pour $r\ge0$ :
\[|x-a|\le r\iff a-r\le x\le a+r.\]
\end{definition}
\begin{savoirfaire}[Lire un intervalle centré]
$|x-3|\le2$ signifie que $x$ est à distance au plus 2 de 3, donc $x\in[1;5]$. Le centre est 3 et le rayon est 2.
\end{savoirfaire}
\begin{attention}Une longueur est positive ; une abscisse peut être négative. Pour une borne exclue, ne pas remplacer une inégalité stricte par une inégalité large.\end{attention}'''
],[
E('Le plus petit ensemble',r"""Pour chacun des nombres $-4$, $7/8$, $2/3$, $\sqrt{49}$ et $\sqrt3$, donner le plus petit ensemble parmi $\mathbb N,\mathbb Z,\mathbb D,\mathbb Q,\mathbb R$ qui le contient.""",
r"""$-4$ est entier relatif mais non naturel : $\mathbb Z$. $7/8=0{,}875$ est décimal non entier : $\mathbb D$. $2/3$ est rationnel non décimal : $\mathbb Q$. $\sqrt{49}=7$ appartient à $\mathbb N$. Enfin $\sqrt3$ est irrationnel : parmi les ensembles proposés, seul $\mathbb R$ le contient.""",
'Simplifier le nombre avant de classer son écriture.','assert sqrt(49)==7 and Rational(7,8)==Rational(875,1000) and not sqrt(3).is_rational'),
E('Comparer exactement',r"""Ranger $-3/2$, $-1{,}4$, $7/5$ et $\sqrt2$ dans l’ordre croissant sans remplacer la racine par un arrondi grossier.""",
r"""$-3/2=-1{,}5<-1{,}4$. Les deux autres nombres sont positifs. Comme $(7/5)^2=49/25=1{,}96<2$, on a $7/5<\sqrt2$. Ainsi $\res{-3/2<-1{,}4<7/5<\sqrt2}$. Comparer les carrés était légitime pour ces deux nombres positifs.""",
'Utiliser les carrés pour comparer deux nombres positifs.','assert -Rational(3,2)<-Rational(14,10)<Rational(7,5)<sqrt(2)'),
E('Du texte à l’intervalle',Q(r"""Écrire sous forme d’intervalle : $-2\le x<5$ ; $x\ge3$ ; $x<-1$.""",r"""Dire si 5 appartient au premier intervalle."""),
r"""Les ensembles sont respectivement $\res{[-2;5[}$, $\res{[3;+\infty[}$ et $\res{]-\infty;-1[}$. Le nombre 5 n’appartient pas au premier : le crochet de droite est ouvert. En revanche, $-2$ lui appartient. Le symbole $+\infty$ n’est pas un nombre réel que l’on pourrait inclure.""",
'Faire correspondre chaque inégalité à son crochet.','assert Interval.Ropen(-2,5).contains(-2) and not Interval.Ropen(-2,5).contains(5)'),
E('Union et intersection',r"""Pour $I=[-3;2]$ et $J=]0;5]$, déterminer $I\cap J$ et $I\cup J$. Représenter les deux intervalles sur une droite.""",
r"""Les nombres présents dans les deux intervalles vérifient $0<x\le2$ : $\res{I\cap J=]0;2]}$. Les deux intervalles se chevauchent, leur réunion couvre sans trou de $-3$ à 5 : $\res{I\cup J=[-3;5]}$. En particulier 0 reste dans la réunion grâce à $I$, même s’il est exclu de $J$.""",
'Repérer la zone commune, puis la zone couverte par au moins un intervalle.','assert Intersection(Interval(-3,2),Interval.Lopen(0,5))==Interval.Lopen(0,2) and Union(Interval(-3,2),Interval.Lopen(0,5))==Interval(-3,5)',figure='intervalles'),
E('Distances sur une droite',r"""Calculer la distance entre les abscisses $-4$ et 3, puis entre $2{,}5$ et $-1{,}5$. Écrire chaque calcul avec une valeur absolue.""",
r"""La distance est la valeur absolue de la différence : $|-4-3|=|-7|=\res7$ ; $|2{,}5-(-1{,}5)|=|4|=\res4$. Échanger les deux points change le signe de la différence mais pas sa valeur absolue. C’est pourquoi une distance reste la même dans les deux sens.""",
'Transformer la différence signée en distance positive.','assert abs(-4-3)==7 and abs(Rational(5,2)+Rational(3,2))==4'),
E('Un intervalle centré',r"""Résoudre $|x-2|\le3$ et représenter l’ensemble obtenu.""",
r"""La condition demande les points situés à distance au plus 3 de l’abscisse 2. Les extrémités sont $2-3=-1$ et $2+3=5$. Elles sont autorisées par « au plus ». L’ensemble des solutions est $\res{[-1;5]}$. Le centre vaut bien $(-1+5)/2=2$.""",
'Lire une inégalité de valeur absolue comme une distance.','assert solve_univariate_inequality(Abs(x-2)<=3,x,relational=False)==Interval(-1,5)',figure='intervalle-centre'),
E('Un encadrement de racine',r"""Démontrer $2{,}23<\sqrt5<2{,}24$. En déduire l’arrondi de $\sqrt5$ au dixième.""",
r"""Les nombres sont positifs. On calcule $2{,}23^2=4{,}9729<5$ et $2{,}24^2=5{,}0176>5$. La fonction carré conserve l’ordre sur les positifs ; l’encadrement est donc établi. Tous les nombres de cet intervalle s’arrondissent à $\res{2{,}2}$ au dixième, car ils sont inférieurs à 2,25.""",
'Contrôler un encadrement par des carrés exacts.','assert Rational(223,100)**2<5<Rational(224,100)**2'),
E('Une erreur absolue',r"""Un capteur annonce $12{,}4$ cm avec une erreur absolue d’au plus $0{,}15$ cm. Donner l’intervalle des longueurs possibles et sa largeur.""",
r"""Notons $L$ la longueur réelle. L’énoncé se traduit par $|L-12{,}4|\le0{,}15$. Donc $\res{L\in[12{,}25;12{,}55]}$ en centimètres. La largeur de l’intervalle est $12{,}55-12{,}25=\res{0{,}30\text{ cm}}$. L’erreur maximale est le rayon, pas la largeur totale.""",
'Distinguer rayon d’incertitude et amplitude de l’intervalle.','assert Rational(124,10)-Rational(15,100)==Rational(1225,100) and Rational(1255,100)-Rational(1225,100)==Rational(3,10)'),
E('Complémentaire d’un intervalle',r"""Dans $\mathbb R$, décrire les nombres qui n’appartiennent pas à $]-2;4]$. Donner une écriture par réunion.""",
r"""Ne pas vérifier $-2<x\le4$ signifie être à gauche, en incluant $-2$, ou strictement à droite de 4. Le complémentaire est donc $\res{]-\infty;-2]\cup]4;+\infty[}$. Le nombre 4 reste exclu du complémentaire puisqu’il appartient à l’intervalle initial.""",
'Examiner les deux côtés et traiter chaque borne séparément.','assert Complement(S.Reals,Interval.Lopen(-2,4))==Union(Interval(-oo,-2),Interval.open(4,oo))'),
E('Mesures et chiffres significatifs',r"""Un rectangle mesure $12{,}3$ cm sur $4{,}56$ cm. Calculer son aire, puis l’arrondir à trois chiffres significatifs. Convertir la valeur non arrondie en mètres carrés. Effectuer aussi ces conversions : 750 mL en L ; $2{,}5$ h en heures et minutes ; 72 km/h en m/s ; $1{,}4$ kg en g ; 3 dm$^3$ en L.""",
r"""Le produit exact des données est $12{,}3\times4{,}56=56{,}088$ cm$^2$. À trois chiffres significatifs, il devient $\res{56{,}1\text{ cm}^2}$. Comme $1\text{ m}^2=10000\text{ cm}^2$, la valeur non arrondie est $\res{0{,}0056088\text{ m}^2}$. Pour les autres conversions : $\res{750\text{ mL}=0{,}75\text{ L}}$ ; $\res{2{,}5\text{ h}=2\text{ h }30\text{ min}}$ ; $72\times1000/3600=\res{20\text{ m/s}}$ ; $\res{1{,}4\text{ kg}=1400\text{ g}}$ ; $\res{3\text{ dm}^3=3\text{ L}}$. Le facteur dépend de la grandeur : une aire se convertit avec le carré du facteur de longueur.""",
'Calculer avant d’arrondir et adapter la conversion à la grandeur.','assert Rational(123,10)*Rational(456,100)==Rational(56088,1000) and Rational(750,1000)==Rational(3,4) and Rational(1,2)*60==30 and Rational(72*1000,3600)==20 and Rational(14,10)*1000==1400'),
E('Deux contraintes de mesure',r"""Une longueur $x$ en centimètres vérifie $|x-10|\le2$ et $9<x\le13$. Quel est l’ensemble exact des valeurs possibles ?""",
r"""La première condition donne $8\le x\le12$, soit $[8;12]$. La seconde donne $]9;13]$. Les deux conditions doivent être satisfaites simultanément : on prend leur intersection. La réponse est $\res{x\in]9;12]}$. La borne 9 est exclue, tandis que 12 respecte bien les deux contraintes.""",
'Transformer chaque contrainte puis prendre une intersection.','assert Intersection(Interval(8,12),Interval.Lopen(9,13))==Interval.Lopen(9,12)'),
E('Un décimal caché',r"""Parmi $13/40$, $7/12$ et $21/28$, quels nombres sont décimaux ? On pourra chercher une écriture de dénominateur puissance de 10.""",
r"""$13/40=325/1000=0{,}325$ est décimal. $21/28=3/4=75/100=0{,}75$ l’est aussi. La fraction $7/12$ est irréductible et son dénominateur contient un facteur 3 ; elle ne peut avoir un dénominateur puissance de 10 après réduction. Elle n’est donc pas décimale. Ce dernier critère est démontré dans le parcours d’approfondissement.""",
'Réduire la fraction avant d’examiner son dénominateur.','assert Rational(13,40)==Rational(325,1000) and Rational(21,28)==Rational(75,100) and factorint(12)=={2:2,3:1}'),
E('Un faux calcul sur les racines',r"""Une élève affirme $\sqrt{a+b}=\sqrt a+\sqrt b$ pour tous $a,b\ge0$. Réfuter l’affirmation, puis comparer les deux membres pour $a=b=4$.""",
r"""Prendre $a=b=4$ donne $\sqrt8=2\sqrt2$ à gauche et $2+2=4$ à droite. Ces nombres sont distincts puisque leurs carrés valent 8 et 16. De plus $\res{\sqrt8<4}$. La racine d’une somme ne se distribue pas ; cette erreur ne doit pas être confondue avec la propriété du produit de deux réels positifs.""",
'Construire un contre-exemple exact et comparer ses carrés.','assert sqrt(8)!=sqrt(4)+sqrt(4) and sqrt(8)<4'),
E('Une amplitude imposée',r"""On sait $1{,}732<\sqrt3<1{,}733$. Encadrer $2+3\sqrt3$ avec une amplitude de $0{,}003$. Donner aussi son arrondi au centième.""",
r"""Multiplier par 3 conserve le sens : $5{,}196<3\sqrt3<5{,}199$. Ajouter 2 donne $\res{7{,}196<2+3\sqrt3<7{,}199}$. L’amplitude est $0{,}003$. Tout cet intervalle est entre 7,195 et 7,205 : l’arrondi au centième est donc $\res{7{,}20}$. L’encadrement permet de garantir l’arrondi.""",
'Propager un encadrement par des opérations qui conservent l’ordre.','assert Rational(7196,1000)<2+3*sqrt(3)<Rational(7199,1000)'),
E('Balayer pour encadrer',r"""Pour encadrer $\sqrt2$ au centième, on teste les entiers $k$ et on compare $k^2$ à 20000. Expliquer pourquoi, puis trouver les deux centièmes consécutifs convenables.""",
r"""Le nombre $k/100$ est positif et $(k/100)^2=k^2/10000$. Comparer son carré à 2 revient donc à comparer $k^2$ à 20000. Or $141^2=19881<20000<20164=142^2$. Ainsi $\res{1{,}41<\sqrt2<1{,}42}$. Le recours aux entiers évite ici les erreurs d’arrondi lors du balayage.""",
'Remplacer des comparaisons décimales par des calculs entiers exacts.','assert 141**2<20000<142**2')
],reperes=['Ensembles de nombres','Intervalles, union et intersection','Valeur absolue et distance','Encadrement et chiffres significatifs'],deco='ensembles')
