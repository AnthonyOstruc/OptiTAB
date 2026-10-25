from modele import *

chapitre(15,'algorithmique','Algorithmique et programmation','5 · Méthodes transversales',
 'Variables · Conditions · Boucles · Fonctions · Simulations',
 ['Lire, écrire, modifier et tester un programme Python.','Relier un algorithme à sa signification mathématique.','Interpréter les résultats d’une simulation.'],
 ['Calcul numérique ; les notions sont à utiliser toute l’année.'],[
r'''\essSection{1}{Variables et instructions}
\begin{definition}Une variable associe un nom à une valeur. Les types rencontrés sont notamment entier (\code{int}), décimal approché (\code{float}), booléen (\code{bool}) et chaîne de caractères (\code{str}). L’affectation \code{x = x + 1} calcule d’abord le membre de droite, puis remplace la valeur de \code{x}.\end{definition}
\begin{propriete}Le test d’égalité s’écrit \code{==}, la différence \code{!=}, le reste de division \code{\%}, la puissance \code{**}. Une condition utilise \code{if}, puis éventuellement \code{elif} et \code{else}. L’indentation délimite les blocs.\end{propriete}
\begin{savoirfaire}[Choisir une boucle]
Une boucle \code{for} convient si le nombre de répétitions est fixé. \code{range(n)} produit les entiers de 0 à $n-1$. Une boucle \code{while} répète tant qu’une condition est vraie : expliquer pourquoi elle finit et ce que signifie sa condition de sortie.
\end{savoirfaire}
\begin{savoirfaire}[Du langage naturel à Python]
En langage naturel, l’affectation se note avec une flèche : $n\leftarrow n+1$ se lit « $n$ prend la valeur $n+1$ ». Les deux écritures ci-dessous décrivent le même algorithme ; il affiche 10.
\begin{codecote}[0.42]
\renewcommand{\arraystretch}{1.18}\begin{tabular}{@{}l@{}}
$n\leftarrow0$\\
$v\leftarrow1$\\
Tant que $v\le1000$\\
\quad $v\leftarrow2\times v$\\
\quad $n\leftarrow n+1$\\
Fin Tant que\\
Afficher $n$
\end{tabular}
\cote
\begin{pythoncol}
n = 0
v = 1
while v <= 1000:
    v = 2 * v
    n = n + 1
print(n)
\end{pythoncol}
\end{codecote}
\end{savoirfaire}
\begin{attention}Les flottants sont approchés : $0{,}1+0{,}2$ peut ne pas être exactement égal à $0{,}3$ en machine. Pour un encadrement garanti, préférer quand c’est possible une comparaison sur des entiers.\end{attention}''',
r'''\essSection{2}{Fonctions, hasard et contrôle}
\begin{definition}Une fonction est définie avec \code{def}, reçoit des arguments et peut renvoyer une valeur avec \code{return}. Définir la fonction ne l’exécute pas : il faut l’appeler.\end{definition}
\begin{savoirfaire}[Tester une fonction]
Choisir un exemple simple dont on connaît la réponse, un cas limite et un cas non trivial. Comparer le résultat numérique au raisonnement. Un programme qui s’exécute sans erreur peut encore calculer la mauvaise grandeur.
\end{savoirfaire}
\begin{propriete}Dans le module \code{random}, \code{randint(a,b)} tire uniformément un entier entre $a$ et $b$, bornes incluses. \code{random()} produit un flottant dans $[0;1[$. Répéter une expérience permet d’obtenir une série statistique et d’observer les fluctuations de fréquences.\end{propriete}
\begin{attention}Une simulation ne démontre pas une probabilité exacte. Pour refaire un même essai sur une installation donnée, on peut fixer une graine avec \code{seed}. La proximité observée ne doit pas être présentée comme une garantie à chaque exécution.\end{attention}
\otIntertitre{Parcours transversal}
Reprendre les algorithmes de divisibilité, de seuil, d’alignement et de balayage des chapitres précédents. Les listes ne sont pas un prérequis du programme ; lorsqu’un fichier ou une collection apparaît, son format est expliqué.'''
],[
E('Suivre les affectations',r"""Donner les valeurs finales de \code{a} et \code{b}, en détaillant les étapes. Réécrire ensuite ces quatre lignes en langage naturel, avec le symbole $\leftarrow$.
\begin{python}
a = 3
b = a + 2
a = 2 * b
b = a - b
\end{python}""",
r"""Après les deux premières lignes, $a=3$ et $b=5$. La troisième remplace $a$ par 10. La quatrième utilise les valeurs alors présentes : $b=10-5=5$. Les valeurs finales sont donc $\res{a=10}$ et $\res{b=5}$. Une affectation n’est pas une égalité algébrique à conserver simultanément avec les anciennes lignes. En langage naturel : $a\leftarrow3$ ; $b\leftarrow a+2$ ; $a\leftarrow2\times b$ ; $b\leftarrow a-b$.""",
'Mettre à jour les valeurs ligne après ligne.','assert 2*(3+2)==10 and 10-(3+2)==5'),
E('Reconnaître les types',r"""Identifier les types des valeurs \code{7}, \code{7.0}, \code{7 > 3} et \code{"7"}. Quel est le résultat de \code{7 / 2} et de \code{7 // 2} ?""",
r"""Les types sont respectivement entier, flottant, booléen et chaîne. Le test \code{7 > 3} vaut \code{True}. La division \code{7 / 2} renvoie le flottant 3,5 ; la division entière \code{7 // 2} renvoie 3. La chaîne \code{"7"} n’est pas directement un nombre : le rôle des guillemets est essentiel.""",
'Distinguer la valeur affichée de son type informatique.','assert type(7) is int and type(7.0) is float and type(7>3) is bool and type("7") is str and 7/2==3.5 and 7//2==3'),
E('Une fonction à appeler',r"""Que renvoie \code{f(4)} ? Et \code{f(-1)} ?
\begin{python}
def f(x):
    return 2 * x * x - 3
\end{python}""",
r"""La fonction calcule $2x^2-3$. Elle renvoie $2\times16-3=\res{29}$ pour 4 et $2\times1-3=\res{-1}$ pour $-1$. Les parenthèses de l’appel attribuent une valeur à l’argument local \code{x} ; la ligne \code{def} seule n’affiche pas les images.""",
'Traduire la ligne return en formule mathématique.','assert 2*4*4-3==29 and 2*(-1)*(-1)-3==-1'),
E('Une condition',r"""Que renvoie la fonction pour $x=-5$, $x=0$ et $x=2$ ? Quelle fonction mathématique reconnaît-on ?
\begin{python}
def distancezero(x):
    if x < 0:
        return -x
    return x
\end{python}""",
r"""Pour $-5$, la condition est vraie et la fonction renvoie 5. Pour 0 et 2, elle atteint la dernière ligne et renvoie 0 et 2. Elle calcule $\res{|x|}$, la distance à 0. Le cas 0 ne nécessite pas un traitement supplémentaire, car les deux écritures donnent la même valeur.""",
'Examiner la branche exécutée, y compris au seuil.','assert [abs(a) for a in [-5,0,2]]==[5,0,2]'),
E('Une somme avec for',r"""Que vaut \code{s} à la fin ? Pourquoi la valeur 5 est-elle incluse ?
\begin{python}
s = 0
for k in range(1, 6):
    s = s + k
\end{python}""",
r"""Les valeurs de \code{k} sont 1, 2, 3, 4 et 5, car la borne finale 6 est exclue. Les sommes successives sont 1, 3, 6, 10 et 15. Ainsi $\res{s=15}$. La variable \code{s} est un accumulateur ; l’initialiser à 0 correspond à la somme avant toute addition.""",
'Lister les valeurs réellement parcourues par range.','assert sum(range(1,6))==15 and list(range(1,6))==[1,2,3,4,5]'),
E('La première puissance au-dessus du seuil',r"""Compléter mentalement l’exécution et expliquer le résultat renvoyé.
\begin{python}
def seuil():
    n = 0
    v = 1
    while v <= 1000:
        v = 2 * v
        n = n + 1
    return n, v
\end{python}""",
r"""Après $n$ passages, $v=2^n$. Or $2^9=512\le1000$ et $2^{10}=1024>1000$. La fonction renvoie $\res{(10;1024)}$. La condition utilise $\le$ pour chercher un dépassement strict. La boucle finit parce que les puissances de 2 dépassent tout seuil fixé ; ici les deux valeurs voisines suffisent à contrôler la sortie. Pour la première puissance de $0{,}5$ strictement inférieure à $0{,}01$, on garde la même structure :
\begin{python}
def seuilbas():
    n = 0
    v = 1
    while v >= 0.01:
        v = 0.5 * v
        n = n + 1
    return n, v
\end{python}
Comme $0{,}5^6=0{,}015625\ge0{,}01$ et $0{,}5^7=0{,}0078125<0{,}01$, elle renvoie $\res{(7;0{,}0078125)}$.""",
'Relier les variables à une puissance et interpréter le test de sortie.','assert 2**9<=1000<2**10 and Rational(1,2)**6>=Rational(1,100)>Rational(1,2)**7 and Rational(1,2)**7==Rational(78125,10**7)'),
E('Un encadrement garanti',r"""Pour $n\ge0$ entier, expliquer ce que renvoie la fonction, puis donner sa sortie pour $n=2$.
\begin{python}
def encadrement(n):
    q = 10 ** n
    k = 0
    while (k + 1) ** 2 <= 2 * q ** 2:
        k = k + 1
    return k / q, (k + 1) / q
\end{python}""",
r"""La boucle trouve le dernier entier $k$ tel que $k^2\le2q^2$ ; le suivant a un carré plus grand. Les bornes mathématiques sont donc $k/q\le\sqrt2<(k+1)/q$, d’amplitude $1/q=10^{-n}$. Pour $n=2$, $k=141$ et la sortie est $\res{(1{,}41;1{,}42)}$. Les tests sont entiers ; les flottants retournés ne doivent pas être confondus avec une écriture rationnelle exacte en machine.""",
'Établir ce qui est vrai avant et après le dernier test.','assert 141**2<=2*100**2<142**2'),
E('Tester un alignement',r"""Expliquer la fonction et calculer son résultat pour $A(0;0)$, $B(2;3)$, $C(4;6)$, puis pour $C(4;7)$.
\begin{python}
def alignes(xa, ya, xb, yb, xc, yc):
    d = (xb-xa)*(yc-ya) - (yb-ya)*(xc-xa)
    return d == 0
\end{python}""",
r"""La valeur \code{d} est le déterminant de $\vect{AB}$ et $\vect{AC}$. Pour $C(4;6)$, elle vaut $2\times6-3\times4=0$ : \code{True}. Pour $C(4;7)$, elle vaut $14-12=2$ : \code{False}. Le test exact est adapté à ces coordonnées entières ; avec des données approchées, il faudrait réfléchir à une tolérance.""",
'Reconnaître un critère géométrique dans le calcul du programme.','assert 2*6-3*4==0 and 2*7-3*4!=0'),
E('Programmer une droite',r"""Écrire une fonction qui, pour deux points d’abscisses distinctes, renvoie la pente et l’ordonnée à l’origine de leur droite. Tester avec $(0;1)$ et $(2;5)$.""",
r"""Le domaine impose \code{xb != xa}. Les formules du cours se traduisent directement :
\begin{python}
def droite(xa, ya, xb, yb):
    m = (yb - ya) / (xb - xa)
    p = ya - m * xa
    return m, p
\end{python}
L’appel donne $\res{(2;1)}$. Une verticale doit être traitée séparément : elle n’a pas de pente réelle et provoquerait ici une division par zéro.""",
'Transformer les formules en fonction et expliciter son domaine.','assert Rational(5-1,2-0)==2 and 1-2*0==1'),
E('Une expérience simulée',r"""Quelle expérience la fonction simule-t-elle ? Donner sa probabilité exacte de renvoyer 1. Écrire ensuite une fonction \code{somme2()} qui renvoie la somme des résultats de deux dés équilibrés lancés indépendamment.
\begin{python}
from random import randint
def succes():
    d = randint(1, 6)
    if d >= 5:
        return 1
    return 0
\end{python}""",
r"""Elle simule un dé équilibré et code le succès « 5 ou 6 » par 1, les autres issues par 0. La probabilité exacte de renvoyer 1 est donc $\res{2/6=1/3}$. Le résultat d’un seul appel ne donne pas cette probabilité ; il représente une réalisation aléatoire de l’expérience. Chaque appel de \code{randint} simule un lancer indépendant :
\begin{python}
from random import randint
def somme2():
    return randint(1, 6) + randint(1, 6)
\end{python}
La fonction renvoie un entier de 2 à 12 ; ces sommes ne sont pas équiprobables.""",
'Lire les issues favorables de la condition, puis traduire deux lancers par deux appels.','assert Rational(len([d for d in range(1,7) if d>=5]),6)==Rational(1,3) and sorted(set(a+b for a in range(1,7) for b in range(1,7)))==list(range(2,13))'),
E('Fréquence simulée',r"""Expliquer la sortie de la fonction ci-dessous pour $n>0$. Comparer son rôle à la probabilité théorique.
\begin{python}
from random import randint
def frequence(n):
    s = 0
    for k in range(n):
        if randint(1, 6) >= 5:
            s = s + 1
    return s / n
\end{python}""",
r"""\code{s} compte les succès parmi $n$ lancers et la fonction renvoie leur fréquence. Elle est entre 0 et 1 et fluctue autour de $1/3$ lorsque $n$ est grand. Elle ne vaut pas nécessairement $1/3$, même pour un grand nombre de lancers. Le cas $n=0$ est exclu à cause de la division finale.""",
'Interpréter l’accumulateur et le dénominateur de la fréquence.','assert Rational(2,6)==Rational(1,3) and all(0<=Rational(s,10)<=1 for s in range(11))'),
E('Moyenne et écart type sans liste',r"""La fonction simule $n>0$ dés. Expliquer les accumulateurs et la formule renvoyée pour l’écart type.
\begin{python}
from random import randint
from math import sqrt
def resume(n):
    s = 0
    q = 0
    for k in range(n):
        d = randint(1, 6)
        s = s + d
        q = q + d*d
    m = s / n
    variance = max(0, q / n - m*m)
    return m, sqrt(variance)
\end{python}""",
r"""\code{s} additionne les valeurs et \code{q} leurs carrés. La moyenne est \code{s / n}. En développant les écarts au carré, leur moyenne vaut $\overline{x^2}-\bar x^2$, d’où la formule. Le \code{max(0,...)} évite une très petite valeur négative due aux arrondis. La fonction renvoie des indicateurs de l’échantillon simulé, pas exactement ceux de la loi uniforme.""",
'Relier chaque accumulateur à une somme statistique.','assert Rational(sum(a*a for a in [2,2,6,6]),4)-Rational(sum([2,2,6,6]),4)**2==4'),
E('Corriger une boucle',r"""Le programme suivant prétend chercher le premier rang où $3^n>100$, mais ne finit pas. Expliquer et corriger.
\begin{python}
n = 0
v = 1
while v <= 100:
    n = n + 1
\end{python}""",
r"""La variable \code{v} reste égale à 1 : le test est toujours vrai. Ajouter dans la boucle \code{v = 3 * v}, à la même indentation que la mise à jour de \code{n}, rétablit le lien $v=3^n$. Le programme corrigé s’arrête avec $\res{n=5}$ et $\res{v=243}$, puisque $3^4=81\le100<243$.""",
'Identifier la variable du test et vérifier qu’elle évolue vers la sortie.','assert 3**4<=100<3**5'),
E('Approcher une longueur de courbe',r"""Pour $f(x)=x^2$ sur $[0;1]$, expliquer la somme calculée. Donner le résultat exact pour $n=2$.
\begin{python}
from math import sqrt
def longueur(n):
    total = 0
    for k in range(n):
        a = k / n
        b = (k + 1) / n
        total += sqrt((b-a)**2 + (b*b-a*a)**2)
    return total
\end{python}""",
r"""Chaque terme est la distance entre deux points successifs de la parabole, d’abscisses $k/n$ et $(k+1)/n$. La somme est la longueur de la ligne polygonale, une approximation de la longueur courbe. Pour $n=2$, elle vaut $\res{(\sqrt5+\sqrt{13})/4\approx1{,}4604}$. Le domaine est $n\ge1$ entier. Augmenter $n$ affine la subdivision, sans transformer la valeur calculée en preuve exacte de la longueur.""",
'Reconnaître une formule de distance dans la boucle.','assert simplify(sqrt(Rational(1,4)+Rational(1,16))+sqrt(Rational(1,4)+Rational(9,16))-(sqrt(5)+sqrt(13))/4)==0',figure='courbe-longueur'),
E('Une dichotomie pour un maximum',r"""On sait que $f(x)=4-(x-0{,}7)^2$ atteint son maximum en $c=0{,}7\in[0;2]$. Expliquer pourquoi comparer $f(a)$ et $f(b)$ localise $c$ de part et d’autre du milieu, puis interpréter le programme.
\begin{python}
def encadremaximum(n):
    a, b = 0.0, 2.0
    for k in range(n):
        m = (a + b) / 2
        if 4-(a-0.7)**2 < 4-(b-0.7)**2:
            a = m
        else:
            b = m
    return a, b
\end{python}""",
r"""$f(b)-f(a)=(b-a)(1{,}4-a-b)$. Comme $b-a>0$, si $f(a)<f(b)$ alors $c>(a+b)/2$ ; sinon $c\le(a+b)/2$. On conserve donc la moitié qui contient le maximum. Après $n$ étapes, l’intervalle contient $c$ et a une largeur mathématique $\res{2/2^n}$. Cette règle est justifiée pour cette parabole symétrique ; elle ne s’applique pas automatiquement à toute fonction qui monte puis descend.""",
'Démontrer la règle de réduction avant d’interpréter la précision.','assert expand((4-(y-Rational(7,10))**2)-(4-(x-Rational(7,10))**2)-(y-x)*(Rational(14,10)-x-y))==0')
],reperes=['Types, affectations, conditions et boucles','Fonctions et tests','Simulation, moyenne et écart type','Algorithmes géométriques, balayage et dichotomie'],deco='algorithmique')

chapitre(16,'raisonnement-syntheses','Raisonner et faire la synthèse','5 · Méthodes transversales',
 'Ensembles · Logique · Démonstrations · Problèmes mixtes',
 ['Lire et écrire une proposition avec ses hypothèses.','Choisir un contre-exemple ou une méthode de preuve.','Mobiliser plusieurs chapitres dans un même problème.'],
 ['Ces ressources se travaillent progressivement toute l’année.'],[
r'''\essSection{1}{Ensembles et propositions}
\begin{definition}$x\in E$ signifie que $x$ est un élément de $E$ ; $A\subset E$ signifie que tout élément de $A$ appartient à $E$ : $A$ est un sous-ensemble de $E$. L’ensemble vide est $\varnothing$. Pour $A,B\subset E$ : l’intersection $A\cap B$ contient les éléments communs à $A$ et $B$ ; la réunion $A\cup B$ ceux qui sont dans $A$ ou dans $B$ ; le complémentaire de $A$ dans $E$, noté $\overline A$ ou $E\setminus A$, ceux de $E$ qui ne sont pas dans $A$. Le cardinal $\operatorname{Card}(A)$ d’un ensemble fini est son nombre d’éléments. Le produit cartésien $A\times B$ est l’ensemble des couples $(a;b)$ avec $a\in A$ et $b\in B$.\end{definition}
\begin{definition}Une proposition est un énoncé mathématique qui est soit vrai, soit faux. Elle peut contenir une variable : « $n$ est pair » est vraie pour $n=4$ et fausse pour $n=7$.\end{definition}
\begin{propriete}« Et » exige les deux conditions ; « ou » signifie au moins l’une des deux, y compris les deux. Nier $x<3$ donne $x\ge3$. Nier « $x$ est pair et positif » donne « $x$ n’est pas pair ou n’est pas positif ».\end{propriete}
\begin{definition}Une implication « si $P$, alors $Q$ » affirme que l’hypothèse $P$ entraîne $Q$. Sa réciproque échange $P$ et $Q$. Sa contraposée est « si non $Q$, alors non $P$ » ; elle a la même valeur de vérité que l’implication. Une équivalence $P\iff Q$, lue « $P$ si et seulement si $Q$ », exige les deux implications. Par exemple, pour un réel $x$, $x^2=4\iff x=-2\text{ ou }x=2$.\end{definition}
\begin{attention}Une implication n’autorise pas automatiquement sa réciproque. « Multiple de 4 entraîne pair » est vraie, mais « pair entraîne multiple de 4 » est fausse.\end{attention}''',
r'''\essSection{2}{Chercher, démontrer et communiquer}
\begin{savoirfaire}[Une preuve adaptée]
Pour une affirmation universelle, raisonner sur un objet quelconque avec les hypothèses. Pour une existence, fournir un exemple qui convient. Pour réfuter une affirmation universelle, un seul contre-exemple suffit. Les formulations quantifiées sont écrites en mots ; les symboles de quantification ne sont pas requis en Seconde.
\end{savoirfaire}
\begin{savoirfaire}[Trois démarches]
Disjonction : étudier tous les cas possibles. Contraposée : démontrer non $Q$ entraîne non $P$. Absurde : supposer la conclusion fausse puis obtenir une contradiction avec les hypothèses ou une propriété établie.
\end{savoirfaire}
\begin{exemple}Pour montrer qu’un entier dont le carré est pair est pair, on peut utiliser la contraposée : le carré d’un impair est impair. La preuve générale se trouve au chapitre 1 ; un simple test numérique ne suffirait pas.\end{exemple}
\otIntertitre{Une rédaction complète}
Nommer les objets ; annoncer les conditions ; présenter les étapes dans l’ordre ; conclure dans le contexte et avec les unités. Un schéma sert à chercher et expliquer, mais une propriété lue à l’œil doit être justifiée.
\par\medskip Les exercices 11 à 15 mélangent les domaines. Rechercher d’abord les liens utiles entre leurs données plutôt que tenter d’appliquer le dernier cours appris.'''
],[
E('Appartenance et inclusion',Q(r"""Pour $A=\{1;2;4\}$, dire si $2\in A$, $\{2\}\subset A$, $3\in A$ et $\varnothing\subset A$ sont vraies.""",r"""Dans $E=\{1;2;3;4;5\}$, on donne aussi $B=\{2;3;5\}$. Déterminer $A\cap B$, $A\cup B$, $\overline A=E\setminus A$ et $\operatorname{Card}(A\cup B)$."""),
r"""Les deux premières phrases sont vraies : 2 est un élément de $A$, et le seul élément de $\{2\}$ est dans $A$. La troisième est fausse car 3 n’est pas listé. La dernière est vraie : aucun élément de l’ensemble vide ne peut contredire l’inclusion. Les symboles $\in$ et $\subset$ ne décrivent pas la même relation. Ensuite $\res{A\cap B=\{2\}}$, $\res{A\cup B=E}$ et $\res{\overline A=\{3;5\}}$. Donc $\res{\operatorname{Card}(A\cup B)=5}$, ce que confirme $3+3-1=5$.""",
'Distinguer un élément de l’ensemble qui le contient, puis appliquer chaque opération sur les ensembles.','assert 2 in {1,2,4} and {2}<={1,2,4} and 3 not in {1,2,4} and set()<={1,2,4} and {1,2,4}&{2,3,5}=={2} and {1,2,4}|{2,3,5}=={1,2,3,4,5} and {1,2,3,4,5}-{1,2,4}=={3,5} and len({1,2,4}|{2,3,5})==3+3-1==5'),
E('Un produit cartésien',r"""Pour $A=\{0;1\}$ et $B=\{a;b;c\}$, lister $A\times B$ et donner son cardinal.""",
r"""On obtient $(0;a),(0;b),(0;c),(1;a),(1;b),(1;c)$. Il y a $\res6$ couples, soit $2\times3$. L’ordre des composantes compte : les premières appartiennent à $A$ et les secondes à $B$. Le produit cartésien est un outil naturel pour décrire deux épreuves successives.""",
'Associer chaque élément du premier ensemble à tous ceux du second.','assert len([(a,b) for a in [0,1] for b in ["a","b","c"]])==6'),
E('Nier une condition',r"""Formuler la négation de « $x<5$ », puis de « $x\ge2$ et $x\le7$ ».""",
r"""La négation de $x<5$ est $\res{x\ge5}$, en incluant le cas d’égalité. La négation des deux conditions réunies est « $\res{x<2\text{ ou }x>7}$ ». Il suffit que l’une des deux contraintes échoue pour sortir de l’intervalle $[2;7]$.""",
'Compléter toutes les possibilités sans laisser de borne oubliée.','assert all((not (2<=a<=7))==(a<2 or a>7) for a in range(-10,20))'),
E('Implication et réciproque',r"""Écrire la réciproque de « si un entier est multiple de 6, il est pair ». Donner la valeur de vérité de chacune des deux phrases.""",
r"""L’implication est vraie : $n=6k=2(3k)$ est pair. La réciproque est « si un entier est pair, il est multiple de 6 ». Elle est fausse, par exemple pour 2. Une hypothèse plus forte peut entraîner une propriété sans que cette propriété suffise à retrouver l’hypothèse.""",
'Prouver la phrase initiale puis tester sa réciproque indépendamment.','assert all((6*k)%2==0 for k in range(-10,11)) and 2%6!=0'),
E('Prouver une existence',r"""Existe-t-il un réel $x$ tel que $x^2=2x$ ? Donner toutes les solutions. Quelle différence y a-t-il entre « il existe » et « pour tout » ?""",
r"""On résout $x(x-2)=0$ : les solutions sont $\res{0\text{ et }2}$. La phrase d’existence est donc vraie. La phrase « pour tout réel $x$, $x^2=2x$ » est fausse, par exemple en $x=1$. Un seul exemple suffit pour établir une existence, mais il ne démontre pas une propriété universelle.""",
'Identifier ce que demande la formulation avant de choisir une preuve.','assert solveset(x*x-2*x,x,domain=S.Reals)==FiniteSet(0,2) and 1**2!=2*1'),
E('Un contre-exemple décisif',r"""Réfuter : « Pour tout réel $x$, si $x^2>4$, alors $x>2$. » Proposer une conclusion correcte.""",
r"""Prendre $x=-3$ : son carré vaut 9, supérieur à 4, mais $-3$ n’est pas supérieur à 2. La conclusion correcte est $\res{x<-2\text{ ou }x>2}$. Elle tient compte des deux branches de la fonction carré. On peut aussi formuler la conclusion comme une distance à 0 supérieure à 2.""",
'Chercher un oubli de signe dans une affirmation sur les carrés.','assert (-3)**2>4 and not -3>2 and solve_univariate_inequality(x*x>4,x,relational=False)==Union(Interval.open(-oo,-2),Interval.open(2,oo))'),
E('Une disjonction de cas',r"""Démontrer que le produit de deux entiers consécutifs est pair en distinguant les deux parités possibles du premier.""",
r"""Si $n=2k$, alors $n(n+1)=2k(n+1)$ est pair. Si $n=2k+1$, alors $n+1=2(k+1)$ et $n(n+1)=2n(k+1)$ est pair. Les deux cas couvrent tous les entiers, donc la propriété est établie pour tout $n\in\mathbb Z$. Il faut montrer que la liste des cas est exhaustive.""",
'Faire deux preuves partielles qui couvrent toutes les possibilités.','assert all(n*(n+1)%2==0 for n in range(-100,101))'),
E('Une preuve par l’absurde',r"""Démontrer qu’il n’existe pas de plus grand entier naturel.""",
r"""Supposons qu’un plus grand entier naturel $N$ existe. Le nombre $N+1$ est encore un entier naturel, et il est strictement supérieur à $N$. Cela contredit le choix de $N$. L’hypothèse de départ est donc impossible. Le raisonnement ne dépend d’aucune valeur particulière de $N$.""",
'Supposer l’existence de l’objet impossible puis construire une contradiction.','assert all(n+1>n for n in range(100))'),
E('Une contraposée',r"""Pour un entier $n$, démontrer : « si $n^2$ est impair, alors $n$ est impair », en utilisant la contraposée.""",
r"""La contraposée est « si $n$ est pair, alors $n^2$ est pair ». Écrire $n=2k$ donne $n^2=4k^2=2(2k^2)$, donc un entier pair. La contraposée étant démontrée, l’implication initiale est vraie. Cette méthode évite de supposer directement l’écriture recherchée de $n$.""",
'Écrire correctement la contraposée avant le calcul.','assert all(n%2==1 for n in range(-100,101) if n*n%2==1)'),
E('Le statut d’un dessin',r"""Un logiciel affiche trois points presque alignés. Quelles données permettent de démontrer l’alignement ? Proposer un exemple de trois points très proches d’une même droite mais non alignés.""",
r"""Il faut par exemple des coordonnées exactes et un déterminant nul, ou une propriété géométrique démontrée. Les points $(0;0),(1;1),(2;2{,}001)$ paraissent presque alignés à petite échelle, mais le déterminant vaut $1\times2{,}001-1\times2=0{,}001\ne0$. Ils ne sont donc pas alignés. La précision d’affichage ne remplace pas l’égalité exacte.""",
'Distinguer une observation numérique d’une condition mathématique exacte.','assert Rational(2001,1000)-2==Rational(1,1000)'),
E('Synthèse : une aire maximale',r"""Un rectangle a un périmètre de 28 cm. Exprimer son aire en fonction d’un côté $x$, déterminer son maximum et les dimensions correspondantes.""",
r"""La somme des deux côtés vaut 14 ; l’autre côté est $14-x$ avec $0<x<14$. L’aire est $A(x)=x(14-x)=49-(x-7)^2\le49$. Le maximum $\res{49\text{ cm}^2}$ est atteint pour $\res{7\text{ cm}\times7\text{ cm}}$. Le rectangle optimal est un carré ; les dimensions respectent le périmètre annoncé.""",
'Relier une contrainte géométrique à une optimisation algébrique.','assert expand(49-(x-7)**2)==expand(x*(14-x))',figure='synthese-rectangle'),
E('Synthèse : contrôler une pièce',r"""Une fabrication de 500 pièces compte 40 défectueuses. Un contrôle donne 36 signaux positifs parmi les défectueuses et 23 parmi les conformes. Calculer la sensibilité et la part de défauts parmi les signaux positifs.""",
r"""La sensibilité vaut $36/40=\res{90\,\%}$. Il y a $36+23=59$ signaux positifs, dont 36 vrais défauts ; la probabilité inversée est $\res{36/59\approx61{,}0\,\%}$. La fréquence initiale des défauts est $40/500=8\,\%$, distincte des deux autres valeurs. Chaque pourcentage répond à une question de référence différente.""",
'Construire les effectifs avant d’inverser le conditionnement.','assert Rational(36,40)==Rational(9,10) and round(100*36/59,1)==61.0'),
E('Synthèse : coûts et seuil',r"""Une sortie coûte 180 euros de transport et 12 euros par participant. Chaque participant paie 18 euros. Exprimer le résultat financier pour $n$ participants et déterminer le seuil de rentabilité.""",
r"""Les recettes sont $18n$, les dépenses $180+12n$ ; le résultat est $B(n)=6n-180$. Il est positif ou nul pour $n\ge30$. Le seuil est donc $\res{30\text{ participants}}$, avec résultat nul au seuil ; un bénéfice strict demande au moins 31 participants. Le domaine est l’ensemble des entiers naturels.""",
'Comparer recettes et dépenses puis interpréter une inégalité entière.','assert 18*30-(180+12*30)==0 and 18*31-(180+12*31)>0'),
E('Synthèse : un lieu et une droite',r"""$A(0;0)$ et $B(4;0)$. Trouver le point de la droite $y=x+1$ qui est équidistant de $A$ et de $B$.""",
r"""Les points équidistants de $A$ et $B$ sont sur la médiatrice $x=2$. L’intersection avec $y=x+1$ est donc $\res{M(2;3)}$. Contrôle : $MA^2=4+9=13$ et $MB^2=4+9=13$. Le problème se résout plus vite en utilisant la médiatrice qu’en développant d’emblée toutes les distances.""",
'Choisir d’abord la propriété géométrique qui simplifie le système.','assert 2+1==3 and (2-0)**2+3**2==(2-4)**2+3**2',figure='synthese-mediatrice'),
E('Synthèse : juger une conclusion',r"""Une série de 20 mesures a une moyenne de 10. Un élève affirme que 10 de ces mesures sont forcément inférieures ou égales à 10. Réfuter sa conclusion avec une série explicite, puis préciser l’indicateur qui parle de partage en deux.""",
r"""Prendre une mesure égale à $-9$ et 19 mesures égales à 11. La somme vaut $-9+19\times11=200$, donc la moyenne vaut bien 10. Pourtant une seule mesure est inférieure ou égale à 10. L’affirmation est fausse. C’est la médiane, et non la moyenne, qui décrit un partage de la série ordonnée en deux parties.""",
'Construire un exemple qui respecte l’hypothèse mais contredit la conclusion.','assert Rational(-9+19*11,20)==10 and sum(v<=10 for v in [-9]+[11]*19)==1')
],reperes=['Ensembles, couples et cardinal','Connecteurs, implication et réciproque','Disjonction, contraposée et absurde','Problèmes de synthèse'],deco='ensembles')
