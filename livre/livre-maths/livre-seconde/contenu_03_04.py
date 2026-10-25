from modele import *

chapitre(3,'calcul-litteral','Calcul numérique et littéral','1 · Nombres et calculs',
 'Puissances · Racines · Développement · Factorisation',
 ['Calculer exactement avec puissances et racines.','Choisir une forme adaptée à un objectif.','Manipuler une expression fractionnaire avec ses conditions.'],
 ['Priorités opératoires et distributivité.'],[
r'''\essSection{1}{Puissances et racines}
\begin{propriete}Pour $a\ne0$ et $m,n\in\mathbb Z$ : $a^ma^n=a^{m+n}$, $a^m/a^n=a^{m-n}$, $(a^m)^n=a^{mn}$ et $a^{-n}=1/a^n$. L’écriture scientifique d’un nombre positif est $c\times10^p$ avec $1\le c<10$.\end{propriete}
\begin{definition}Pour $a\ge0$, $\sqrt a$ est l’unique réel positif dont le carré vaut $a$. Ainsi $(\sqrt a)^2=a$ et, pour tout réel $u$, $\sqrt{u^2}=|u|$.\end{definition}
\begin{propriete}Pour $a,b\ge0$, $\sqrt{ab}=\sqrt a\sqrt b$. Pour $a\ge0$ et $b>0$, $\sqrt{a/b}=\sqrt a/\sqrt b$.\end{propriete}
\begin{exemple}$\sqrt{72}=\sqrt{36\times2}=6\sqrt2$ ; $\sqrt{(-5)^2}=5$, et non $-5$.\end{exemple}
\begin{savoirfaire}[Éviter les erreurs de signe]Les parenthèses comptent : $(-3)^2=9$, mais $-3^2=-9$. Pour une écriture fractionnaire, simplifier des facteurs, jamais des termes isolés d’une somme.\end{savoirfaire}''',
r'''\essSection{2}{Transformer une expression}
\begin{propriete}
\[(a+b)^2=a^2+2ab+b^2,\qquad(a-b)^2=a^2-2ab+b^2,\]
\[(a-b)(a+b)=a^2-b^2.\]
Développer transforme un produit en somme ; factoriser fait l’inverse.
\end{propriete}
\begin{savoirfaire}[Choisir la forme utile]
Pour calculer une valeur ou lire un coefficient, une forme développée peut être pratique. Pour résoudre un produit nul ou étudier un signe, préférer une forme factorisée. Par exemple $x^2-6x+8=(x-2)(x-4)$.
\end{savoirfaire}
\begin{exemple}[Une expression fractionnaire]
$\dfrac{x^2-9}{x-3}=\dfrac{(x-3)(x+3)}{x-3}=x+3$, seulement pour $x\ne3$. La forme simplifiée ne conserve pas à elle seule l’information sur le domaine initial.
\end{exemple}
\begin{savoirfaire}[Isoler une variable]
Si $V=\pi r^2h$ avec $r>0$, alors $h=V/(\pi r^2)$. Écrire les conditions avant toute division. Les unités peuvent servir à contrôler la formule.
\end{savoirfaire}
\begin{attention}$(a+b)^2$ ne vaut pas $a^2+b^2$ en général. Le terme $2ab$ représente aussi, dans un carré découpé, les deux rectangles de côtés $a$ et $b$.\end{attention}'''
],[
E('Puissances et parenthèses',r"""Calculer $(-2)^4$, $-2^4$, $3^{-2}$ et $5^0$.""",
r"""Les parenthèses font porter la puissance sur le signe : $(-2)^4=\res{16}$ tandis que $-2^4=-(2^4)=\res{-16}$. Un exposant négatif signifie un inverse : $3^{-2}=\res{1/9}$. Enfin $5^0=\res1$, car toute base non nulle à la puissance 0 vaut 1.""",
'Lire la base avant d’appliquer une règle de puissance.','assert (-2)**4==16 and -2**4==-16 and Rational(3)**-2==Rational(1,9) and 5**0==1'),
E('Racines simplifiées',r"""Simplifier $\sqrt{50}$, $\sqrt{108}$ et $\sqrt{16/25}$.""",
r"""On extrait le plus grand carré parfait : $\sqrt{50}=\sqrt{25\times2}=\res{5\sqrt2}$ ; $\sqrt{108}=\sqrt{36\times3}=\res{6\sqrt3}$. Pour le quotient, $\sqrt{16/25}=4/5$, les racines du numérateur et du dénominateur étant positives.""",
'Décomposer le radicande en carré parfait multiplié par un reste.','assert sqrt(50)==5*sqrt(2) and sqrt(108)==6*sqrt(3) and sqrt(Rational(16,25))==Rational(4,5)'),
E('Écriture scientifique',r"""Calculer $A=\dfrac{(3\times10^5)(4\times10^{-2})}{6\times10^2}$ et donner une écriture scientifique.""",
r"""On sépare les coefficients et les puissances : $A=(3\times4/6)\times10^{5-2-2}=2\times10^1$. Cette écriture est scientifique puisque $1\le2<10$. On obtient $\res{A=2\times10^1=20}$.""",
'Regrouper les coefficients puis additionner ou soustraire les exposants.','assert (3*10**5)*Rational(4,100)/(6*10**2)==20'),
E('Développer et réduire',r"""Développer $A=3(x-2)-2(2x+5)$ et $B=(x+4)(2x-1)$.""",
r"""Pour $A$, distribuer le signe négatif à tous les termes : $A=3x-6-4x-10=\res{-x-16}$. Pour $B$, chaque terme du premier facteur multiplie chaque terme du second : $B=2x^2-x+8x-4=\res{2x^2+7x-4}$.""",
'Effectuer toutes les distributions avant de regrouper les termes semblables.','assert expand(3*(x-2)-2*(2*x+5))==-x-16 and expand((x+4)*(2*x-1))==2*x*x+7*x-4'),
E('Reconnaître une identité',r"""Développer $(2x-3)^2$, puis factoriser $x^2-25$ et $x^2+6x+9$.""",
r"""La première expression vaut $\res{4x^2-12x+9}$. La différence de carrés se factorise : $x^2-25=\res{(x-5)(x+5)}$. Enfin $x^2+6x+9=x^2+2\times x\times3+3^2=\res{(x+3)^2}$. Les identités s’utilisent dans les deux sens.""",
'Identifier les deux termes de l’identité remarquable.','assert expand((2*x-3)**2)==4*x*x-12*x+9 and expand((x-5)*(x+5))==x*x-25 and expand((x+3)**2)==x*x+6*x+9'),
E('Un facteur commun',r"""Factoriser $A=5x(x-1)+3(x-1)$ et $B=(x+2)^2-4(x+2)$.""",
r"""Dans $A$, le facteur commun est $x-1$ : $A=\res{(x-1)(5x+3)}$. Dans $B$, extraire $x+2$ donne $(x+2)((x+2)-4)$, donc $B=\res{(x+2)(x-2)}$. Développer les résultats permet de vérifier que rien n’a été perdu.""",
'Repérer un facteur entier commun, même s’il contient plusieurs termes.','assert expand(5*x*(x-1)+3*(x-1)-(x-1)*(5*x+3))==0 and expand((x+2)**2-4*(x+2)-(x+2)*(x-2))==0'),
E('Une simplification conditionnelle',r"""Simplifier $\dfrac{x^2-4}{x+2}$ en précisant le domaine. Calculer la valeur pour $x=3$.""",
r"""Le dénominateur impose $x\ne-2$. Pour ces valeurs, factoriser $x^2-4=(x-2)(x+2)$ puis simplifier le facteur non nul : l’expression vaut $\res{x-2}$. Pour $x=3$, elle vaut 1, ce que confirme $(9-4)/(3+2)=1$. La valeur $-2$ reste interdite.""",
'Déterminer le domaine avant de simplifier.','assert cancel((x*x-4)/(x+2))==x-2 and (3**2-4)/(3+2)==1'),
E('Addition de quotients',r"""Pour $x\ne0$, réduire $\dfrac{2}{x}+\dfrac{x-1}{3x}$ à un seul quotient.""",
r"""Le dénominateur commun est $3x$. Ainsi $2/x=6/(3x)$ et la somme vaut $(6+x-1)/(3x)=\res{(x+5)/(3x)}$. Le domaine reste $x\ne0$. On n’additionne pas les dénominateurs : ils décrivent la même taille d’unité après mise au même dénominateur.""",
'Construire un dénominateur commun, puis additionner les numérateurs.','assert cancel(2/x+(x-1)/(3*x)-(x+5)/(3*x))==0'),
E('Isoler une grandeur',Q(r"""Isoler $t$ dans $d=vt$ pour $v>0$.""",r"""Isoler $r$ dans $S=\pi r^2$ pour $r\ge0$ et $S\ge0$.""",r"""Isoler $y$ dans $3x-2y=7$."""),
r"""La première relation donne $\res{t=d/v}$. Pour la deuxième, $r^2=S/\pi$, puis la condition $r\ge0$ sélectionne $\res{r=\sqrt{S/\pi}}$. Enfin $-2y=7-3x$, donc $\res{y=(3x-7)/2}$. Le signe moins devant $2y$ doit être conservé jusqu’à la division.""",
'Utiliser les opérations inverses et le domaine de la grandeur.','assert solve(3*x-2*y-7,y)==[(3*x-7)/2] and simplify(pi*(sqrt(5/pi))**2)==5'),
E('Comparer par différence ou par quotient',Q(r"""Pour $x\ge0$, comparer $A=(x+1)^2$ et $B=x^2+1$. Quand sont-ils égaux ?""",r"""Comparer $\dfrac79$ et $\dfrac9{11}$ en calculant leur quotient."""),
r"""On calcule $A-B=x^2+2x+1-x^2-1=2x$. Comme $x\ge0$, cette différence est positive ou nulle. Ainsi $\res{A\ge B}$, avec égalité exactement lorsque $2x=0$, soit $\res{x=0}$. Ce raisonnement vaut pour toutes les valeurs autorisées de $x$. Les deux fractions sont strictement positives et $\dfrac79\div\dfrac9{11}=\dfrac{77}{81}<1$ : donc $\res{\dfrac79<\dfrac9{11}}$. Le premier nombre vaut environ 0,95 fois le second.""",
'Ramener une comparaison au signe d’une différence ou à la position d’un quotient par rapport à 1.','assert expand((x+1)**2-x*x-1)==2*x and solve(2*x,x)==[0] and Rational(7,9)/Rational(9,11)==Rational(77,81) and Rational(77,81)<1 and Rational(7,9)<Rational(9,11)'),
E('Un programme de calcul',r"""Choisir un nombre, lui ajouter 3, élever au carré, puis retirer neuf. Exprimer le résultat en fonction de $x$ et montrer qu’il est divisible par 4 lorsque $x$ est un entier pair.""",
r"""Le résultat est $(x+3)^2-9=x^2+6x=x(x+6)$. Si $x=2k$, il devient $2k(2k+6)=4k(k+3)$. Comme $k(k+3)$ est entier, le résultat est multiple de 4. La factorisation $\res{x(x+6)}$ rend cette propriété plus visible que la description du programme.""",
'Transformer le programme en expression, puis exploiter la parité.','assert expand((x+3)**2-9)==x*x+6*x and all(((2*k+3)**2-9)%4==0 for k in range(-20,21))'),
E('Calculer astucieusement',r"""Calculer exactement $1001^2-999^2$ sans développer les deux carrés. Proposer une règle générale pour $(n+1)^2-(n-1)^2$.""",
r"""La différence de carrés donne $(1001-999)(1001+999)=2\times2000=\res{4000}$. En général, $(n+1)^2-(n-1)^2=2\times2n=\res{4n}$. On aurait le même résultat en développant, mais la factorisation réduit ici le nombre d’opérations.""",
'Choisir l’identité qui correspond directement à la forme donnée.','assert 1001**2-999**2==4000 and expand((x+1)**2-(x-1)**2)==4*x'),
E('Un carré encadré',r"""Un carré de côté $x>0$ est entouré d’une bordure de largeur 2. Exprimer l’aire de la bordure et la factoriser. La bordure a une aire de 56 : trouver $x$.""",
r"""Le grand carré a pour côté $x+4$, car la bordure s’ajoute des deux côtés. L’aire cherchée est $(x+4)^2-x^2=8x+16=8(x+2)$. Résoudre $8x+16=56$ donne $\res{x=5}$. On contrôle : $9^2-5^2=81-25=56$.""",
'Soustraire les aires et compter les deux largeurs de bordure.','assert expand((x+4)**2-x*x)==8*x+16 and solve(8*x+16-56,x)==[5]',figure='bordure'),
E('Une identité trompeuse',r"""Un élève écrit $\dfrac{x+4}{x+2}=\dfrac42=2$. Trouver toutes les valeurs de $x$ pour lesquelles son résultat est malgré tout correct.""",
r"""Il faut d’abord $x\ne-2$. L’égalité à 2 équivaut alors à $x+4=2(x+2)$, soit $x+4=2x+4$, donc $\res{x=0}$. Cette valeur est autorisée et donne $4/2=2$. Une égalité vraie pour une seule valeur ne justifie pas la fausse règle de simplification utilisée.""",
'Résoudre l’égalité obtenue sans accepter la transformation erronée.','assert solveset((x+4)/(x+2)-2,x,domain=S.Reals)==FiniteSet(0)'),
E('Deux modèles équivalents',r"""Une aire est décrite par $A(x)=(x+5)^2-(x-1)^2$. Trouver une forme simple, puis déterminer $x\ge1$ pour lequel $A(x)=72$. Expliquer pourquoi l’équation est du premier degré.""",
r"""La différence de carrés se factorise : $A(x)=((x+5)-(x-1))((x+5)+(x-1))=6(2x+4)=12x+24$. Les termes en $x^2$ s’annulent. L’équation devient $12x+24=72$, d’où $\res{x=4}$. La condition $x\ge1$ est respectée et $9^2-3^2=72$.""",
'Transformer l’expression avant de décider du degré de l’équation.','assert expand((x+5)**2-(x-1)**2)==12*x+24 and solve(12*x+24-72,x)==[4]')
],reperes=['Puissances et racines','Identités remarquables','Expressions fractionnaires et domaines','Isolement de variables et comparaison'])

chapitre(4,'equations-inequations','Équations et inéquations','1 · Nombres et calculs',
 'Résoudre · Modéliser · Étudier un signe',
 ['Donner l’ensemble exact des solutions.','Utiliser produit nul et tableaux de signes.','Interpréter les solutions dans une situation concrète.'],
 ['Calcul littéral et intervalles.'],[
r'''\essSection{1}{Équations : transformer sans perdre de solution}
\begin{definition}Résoudre une équation, c’est trouver toutes les valeurs autorisées qui rendent l’égalité vraie. Une transformation équivalente conserve exactement cet ensemble.\end{definition}
\begin{propriete}On peut ajouter un même nombre aux deux membres, ou les multiplier par un même nombre non nul. Un produit est nul si et seulement si au moins l’un de ses facteurs est nul.\end{propriete}
\begin{exemple}$(2x-3)(x+4)=0$ donne $2x-3=0$ ou $x+4=0$, donc $S=\{-4;3/2\}$.\end{exemple}
\begin{propriete}$x^2=a$ n’a pas de solution réelle si $a<0$ ; sa seule solution est 0 si $a=0$ ; pour $a>0$, les solutions sont $-\sqrt a$ et $\sqrt a$.\end{propriete}
\begin{savoirfaire}[Équation quotient]Noter d’abord les valeurs interdites. Pour $(x+1)/(x-2)=3$, imposer $x\ne2$, puis écrire $x+1=3(x-2)$. On trouve $x=7/2$, autorisé.\end{savoirfaire}
\begin{attention}Diviser par une expression contenant $x$ peut faire perdre les valeurs pour lesquelles elle est nulle. Préférer la factorisation.\end{attention}''',
r'''\essSection{2}{Inégalités et signes}
\begin{propriete}Additionner une même quantité conserve l’ordre. Multiplier ou diviser par un nombre strictement négatif renverse le sens de l’inégalité. On peut additionner deux inégalités de même sens.\end{propriete}
\begin{exemple}$-3x+2\ge8$ donne $-3x\ge6$, puis $x\le-2$.\end{exemple}
\begin{propriete}[Comparer deux nombres]Comparaison additive : $a\le b$ équivaut à $a-b\le0$. Comparaison multiplicative, pour $a>0$ et $b>0$ : $a\le b$ équivaut à $a/b\le1$. La différence $b-a$ s’interprète comme une variation additive, le rapport $b/a$ comme un coefficient multiplicateur.\end{propriete}
\begin{savoirfaire}[Produit ou quotient]
Déterminer les zéros de chaque facteur et les valeurs interdites. Les placer dans l’ordre dans un tableau. Sur chaque intervalle, appliquer la règle des signes. Inclure les zéros si l’inégalité est large, mais exclure toujours un dénominateur nul.
\end{savoirfaire}
\begin{exemple}
Pour $(x-1)(x+2)\le0$, les changements de signe se font en $-2$ et 1. Le produit est négatif entre ces valeurs : les solutions sont $[-2;1]$.
\end{exemple}
\begin{savoirfaire}[Modéliser]
Choisir la variable et son domaine ; traduire les contraintes ; résoudre ; revenir à la question. Pour un nombre de billets, ne garder que les entiers autorisés. Une borne réelle n’est pas toujours une réponse concrète.
\end{savoirfaire}'''
],[
E('Une équation linéaire',r"""Résoudre $3x-7=11$ et vérifier la solution.""",
r"""On ajoute 7 aux deux membres : $3x=18$. On divise par 3, qui est non nul : $\res{x=6}$. La substitution donne $3\times6-7=11$. L’ensemble des solutions est $\res{S=\{6\}}$ ; il contient une seule valeur.""",
'Isoler l’inconnue par des opérations réversibles.','assert solve(3*x-7-11,x)==[6]'),
E('L’inconnue des deux côtés',r"""Résoudre $5(x-2)=2x+8$.""",
r"""On développe : $5x-10=2x+8$. En retirant $2x$ puis en ajoutant 10, on obtient $3x=18$, donc $\res{S=\{6\}}$. Contrôle : à gauche $5(6-2)=20$ et à droite $12+8=20$. Les deux membres ont bien la même valeur.""",
'Développer, regrouper les termes en x puis les constantes.','assert solve(5*(x-2)-2*x-8,x)==[6]'),
E('Un signe à renverser',r"""Résoudre $-4x+3>15$ et donner l’intervalle solution.""",
r"""On soustrait 3 : $-4x>12$. En divisant par $-4$, on renverse le signe : $x<-3$. Ainsi $\res{S=]-\infty;-3[}$. La borne $-3$ est exclue puisque l’inégalité est stricte ; elle donnerait l’égalité 15.""",
'Repérer la division par un nombre négatif.','assert solve_univariate_inequality(-4*x+3>15,x,relational=False)==Interval.open(-oo,-3)'),
E('Un carré donné',r"""Résoudre dans $\mathbb R$ les trois équations $x^2=49$, $x^2=0$ et $x^2=-9$.""",
r"""Pour $x^2=49$, il faut les deux signes : $\res{S=\{-7;7\}}$. Pour $x^2=0$, la seule solution est $\res0$. Enfin un carré réel est positif ou nul, donc $x^2=-9$ n’a aucune solution réelle : $\res{S=\varnothing}$.""",
'Distinguer un second membre positif, nul ou négatif.','assert solveset(x*x-49,x,domain=S.Reals)==FiniteSet(-7,7) and solveset(x*x+9,x,domain=S.Reals)==S.EmptySet'),
E('Produit nul',r"""Résoudre $(x-5)(2x+3)=0$.""",
r"""Le produit est nul si $x-5=0$ ou $2x+3=0$. Ces deux équations donnent $x=5$ et $x=-3/2$. On prend leur réunion : $\res{S=\{-3/2;5\}}$. Il ne faut pas imposer que les deux facteurs s’annulent simultanément.""",
'Remplacer le produit nul par une alternative.','assert solveset((x-5)*(2*x+3),x,domain=S.Reals)==FiniteSet(-Rational(3,2),5)'),
E('Une équation quotient',r"""Résoudre $\dfrac{2x+1}{x-3}=5$.""",
r"""Le domaine impose $x\ne3$. Sur ce domaine, on peut multiplier par $x-3$ : $2x+1=5x-15$, donc $3x=16$. La solution $\res{x=16/3}$ est autorisée. Le dénominateur vaut $7/3$ et le numérateur $35/3$, dont le quotient est bien 5.""",
'Fixer le domaine puis supprimer le dénominateur.','assert solveset((2*x+1)/(x-3)-5,x,domain=S.Reals)==FiniteSet(Rational(16,3))'),
E('Tout, rien ou une valeur',r"""Résoudre séparément $2(x+1)=2x+2$ et $2(x+1)=2x+3$.""",
r"""La première devient $2x+2=2x+2$, toujours vraie : $\res{S=\mathbb R}$. La seconde devient $2=3$, impossible : $\res{S=\varnothing}$. L’annulation des termes en $x$ ne permet pas de conclure à $x=0$ : il faut examiner l’égalité restante.""",
'Lire l’égalité finale quand l’inconnue disparaît.','assert expand(2*(x+1)-2*x-2)==0 and expand(2*(x+1)-2*x-3)==-1'),
E('Un produit de deux facteurs',r"""Étudier le signe de $(x-1)(x+3)$ puis résoudre $(x-1)(x+3)\le0$.""",
r"""Les zéros sont $-3$ et 1. Avant $-3$, les deux facteurs sont négatifs, donc le produit est positif. Entre $-3$ et 1, un seul est négatif : le produit est négatif. Après 1, il est positif. Les zéros sont inclus par $\le$ : $\res{S=[-3;1]}$.""",
'Découper la droite aux zéros de chaque facteur.','assert solve_univariate_inequality((x-1)*(x+3)<=0,x,relational=False)==Interval(-3,1)',figure='signes-produit'),
E('Un quotient et sa valeur interdite',r"""Résoudre $\dfrac{x-2}{x+1}>0$.""",
r"""Le quotient est défini pour $x\ne-1$ ; le numérateur s’annule en 2. Il est positif lorsque les deux facteurs ont le même signe : pour $x<-1$ et pour $x>2$. Les bornes sont exclues, $-1$ étant interdit et 2 donnant 0. Ainsi $\res{S=]-\infty;-1[\cup]2;+\infty[}$.""",
'Séparer un zéro autorisé d’un zéro de dénominateur.','assert solve_univariate_inequality((x-2)/(x+1)>0,x,relational=False)==Union(Interval.open(-oo,-1),Interval.open(2,oo))',figure='signes-quotient'),
E('Déplacer une expression',r"""Résoudre $(x-2)^2\le(x-2)(x+4)$.""",
r"""On ramène tout à gauche et on factorise le facteur commun : $(x-2)((x-2)-(x+4))\le0$, soit $-6(x-2)\le0$. La division par $-6$ renverse l’ordre : $x-2\ge0$. La réponse est $\res{S=[2;+\infty[}$. Diviser directement par $x-2$ aurait demandé de distinguer son signe.""",
'Comparer par différence plutôt que diviser par une expression inconnue.','assert expand((x-2)**2-(x-2)*(x+4))==-6*(x-2)'),
E('Un abonnement avantageux',r"""Une salle propose 8 euros par séance, ou un abonnement à 30 euros puis 5 euros par séance. À partir de combien de séances l’abonnement est-il strictement moins cher ?""",
r"""Pour $n\in\mathbb N$, les coûts sont $8n$ et $30+5n$. L’abonnement est moins cher si $30+5n<8n$, donc $n>10$. Le premier entier qui convient est $\res{11}$. À 10 séances les prix sont égaux ; à 11, ils valent 88 euros et 85 euros.""",
'Traduire « strictement moins cher » puis revenir aux entiers.','assert 30+5*10==8*10 and min(n for n in range(100) if 30+5*n<8*n)==11'),
E('Un budget avec remise fixe',r"""Une commande coûte 4,50 euros par carnet et 7 euros de livraison. On dispose de 52 euros. Combien de carnets au maximum peut-on commander ?""",
r"""Si $n$ est le nombre entier de carnets, $4{,}5n+7\le52$. Donc $4{,}5n\le45$, soit $n\le10$. On peut commander $\res{10\text{ carnets}}$. Le coût est alors exactement 52 euros ; onze carnets coûteraient 56,50 euros et dépasseraient le budget.""",
'Écrire une inégalité de budget avec un domaine entier positif.','assert max(n for n in range(30) if Rational(9,2)*n+7<=52)==10'),
E('Des dimensions à retrouver',r"""Un rectangle a pour longueur $x+3$ et largeur $x-1$, en centimètres, avec $x>1$. Son aire vaut 21. Résoudre sans utiliser de discriminant.""",
r"""On écrit $(x+3)(x-1)=21$, soit $x^2+2x-24=0$. On reconnaît $(x+6)(x-4)=0$, donc $x=-6$ ou $x=4$. La condition $x>1$ élimine $-6$. Ainsi $\res{x=4}$ ; les dimensions sont 7 cm et 3 cm, dont le produit vaut 21.""",
'Factoriser une expression simple puis filtrer par le contexte.','assert expand((x+6)*(x-4))==x*x+2*x-24 and solve((x+3)*(x-1)-21,x)==[-6,4]',figure='rectangle-equation'),
E('Un paramètre au premier degré',r"""Pour un réel $m$, discuter le nombre de solutions de $(m-2)x=6$. Donner la solution lorsqu’elle existe.""",
r"""Si $m\ne2$, le coefficient de $x$ est non nul et l’unique solution est $\res{x=6/(m-2)}$. Si $m=2$, l’équation devient $0x=6$, impossible : elle n’a aucune solution. La séparation de ces deux cas est nécessaire avant la division par $m-2$.""",
'Repérer la valeur du paramètre qui annule le coefficient.','assert all(simplify((m-2)*Rational(6,m-2))==6 for m in [-3,0,1,3,8])'),
E('Une équation qui perdrait zéro',r"""Résoudre $x(x-3)=2x$. Expliquer pourquoi diviser immédiatement par $x$ conduit à une réponse incomplète.""",
r"""On ramène tout à gauche : $x(x-3)-2x=x(x-5)=0$. Les solutions sont donc $\res{S=\{0;5\}}$. Diviser par $x$ suppose $x\ne0$ ; on ne trouverait alors que 5 et on aurait éliminé la solution 0. La vérification dans l’équation initiale confirme les deux valeurs.""",
'Factoriser avant toute division par l’inconnue.','assert solveset(x*(x-3)-2*x,x,domain=S.Reals)==FiniteSet(0,5)')
],reperes=['Équations linéaires, produit et quotient','Inéquations et règles de l’ordre','Tableaux de signes','Modélisation et paramètres'])
