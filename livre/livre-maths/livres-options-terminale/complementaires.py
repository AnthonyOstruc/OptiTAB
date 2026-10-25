from commun import e,c
NOM='complémentaires'
CHAPTERS=[]

DIAGNOSTIC=r'''
Sans calculatrice, sauf à la dernière question. Expliquer chaque réponse.
\begin{questions}
\item Simplifier $\frac23+\frac14$, puis $\frac{3^4\times3^2}{3^3}$.
\item Une quantité augmente de $20\,\%$ puis diminue de $20\,\%$. Revient-elle à sa valeur initiale ?
\item Résoudre $x^2-5x+6=0$ et $2x-3\leq5$.
\item Dériver $x^3-2x+1$, $\mathrm e^x$ et $1/x$ sur leurs domaines.
\item Dans un arbre, $P(A)=0{,}3$, $P_A(B)=0{,}8$, $P_{\bar A}(B)=0{,}2$. Calculer $P(B)$.
\item Écrire les quatre premiers termes de $u_0=10$, $u_{n+1}=0{,}8u_n+2$.
\item Calculer à $10^{-3}$ près $\mathrm e^{0{,}4}$ et expliquer ce que produit \code{range(4)} en Python.
\end{questions}
\begin{savoirfaire}[Repères pour se corriger]
1. $11/12$ et $27$. 2. Le coefficient global vaut $1{,}2\times0{,}8=0{,}96$ : baisse de $4\,\%$.
3. $\{2;3\}$ et $x\leq4$. 4. $3x^2-2$, $\mathrm e^x$, $-1/x^2$.
5. $0{,}3\times0{,}8+0{,}7\times0{,}2=0{,}38$.
6. $10,10,10,10$ : la valeur initiale est un équilibre.
7. $1{,}492$ ; \code{range(4)} fournit les entiers $0,1,2,3$.
\end{savoirfaire}
Si les questions 1 à 3 résistent, reprendre les calculs algébriques avant le chapitre 2.
Les questions 4, 5 et 6 orientent respectivement vers les chapitres 4, 8 et 1.
'''

CHAPTERS.append(c('Suites et modèles discrets','Analyse et évolution',r'Récurrence · Équilibre · Limites · Seuils',
'Construire une suite à partir d’un phénomène.@@Étudier une récurrence arithmético-géométrique.@@Calculer une somme et une limite.@@Lire une construction en escalier et chercher un seuil.',
'Pourcentages, suites arithmétiques et géométriques de Première.',r'''
\essSection{1}{Choisir un modèle et son indice}
Une suite $(u_n)$ décrit une grandeur observée à des instants séparés. L'indice $n$ est un entier ; $u_0$ est la valeur de départ, pas la valeur après une étape. Une formule explicite donne directement $u_n$ ; une relation de récurrence utilise les termes précédents.
\begin{definition}[Deux modèles de référence]
Variation absolue constante : $u_{n+1}=u_n+r$, donc $u_n=u_0+nr$.
Variation relative constante : $u_{n+1}=qu_n$, donc $u_n=u_0q^n$.
Pour un taux d'évolution $t$ écrit sous forme décimale, $q=1+t$.
\end{definition}
\begin{exemple}[Une réserve d'eau]
Une réserve contient $100$ litres. Chaque jour, elle perd $20\,\%$ de son contenu, puis reçoit $30$ litres. Le modèle est $u_0=100$, $u_{n+1}=0{,}8u_n+30$.
Ainsi $u_1=110$ et $u_2=118$. Inverser les deux opérations donnerait un autre modèle.
\end{exemple}
\essSection{2}{Déplacer l'équilibre}
\begin{savoirfaire}[Résoudre $u_{n+1}=au_n+b$]
Si $a\ne1$, chercher $\ell=a\ell+b$, donc $\ell=b/(1-a)$. Poser $v_n=u_n-\ell$.
Alors $v_{n+1}=av_n$ et
\[u_n=\ell+(u_0-\ell)a^n.\]
Si $a=1$, la suite est arithmétique : $u_n=u_0+nb$.
\end{savoirfaire}
Dans l'exemple, $\ell=150$ et $u_n=150-50(0{,}8)^n$.
Le modèle prédit une augmentation vers $150$ litres, sans jamais atteindre exactement cet équilibre en un temps fini.
\figurelivre{c01-suite.pdf}{À gauche : les termes de la réserve. À droite : la construction en escalier de $u_{n+1}=0{,}8u_n+30$, avec la droite $y=x$. Les deux axes portent des volumes en litres.}
\essSection{3}{Comprendre une limite}
Une suite tend vers $\ell$ si ses termes finissent par rester aussi près de $\ell$ qu'on le souhaite. Elle tend vers $+\infty$ si elle finit par dépasser tout niveau fixé. Il s'agit ici d'une approche intuitive.
\begin{propriete}[Raison positive]
Pour $0<q<1$, $q^n\longrightarrow0$. Pour $q=1$, $q^n=1$. Pour $q>1$, $q^n\longrightarrow+\infty$.
Les limites se combinent par somme, produit et quotient lorsque cela ne produit pas une forme indéterminée, et lorsque la limite du dénominateur n'est pas nulle.
\end{propriete}
Si $a_n\leq u_n\leq b_n$ à partir d'un certain rang et si les deux bornes tendent vers le même réel $\ell$, le théorème des gendarmes donne $u_n\to\ell$.
Une inégalité large se conserve à la limite : $u_n\leq v_n$ et des limites finies donnent $\lim u_n\leq\lim v_n$. Une inégalité stricte peut devenir une égalité.
\essSection{4}{Additionner des termes}
\begin{propriete}[Attention au nombre de termes]
\[\sum_{k=0}^{n}u_0q^k=u_0\frac{1-q^{n+1}}{1-q}\quad(q\ne1).
\qquad\sum_{k=0}^{n}(u_0+kr)=(n+1)\frac{u_0+u_n}{2}.\]
Si $0<q<1$, la première somme tend vers $u_0/(1-q)$.
\end{propriete}
\begin{demonstration}[Somme géométrique]
Avec $S=1+q+\cdots+q^n$, la différence $S-qS$ vaut $1-q^{n+1}$. On divise par $1-q$. Lorsque $0<q<1$, $q^{n+1}\to0$, d'où la limite annoncée.
\end{demonstration}
\essSection{5}{Chercher un seuil et critiquer le modèle}
Pour la réserve, dépasser $145$ litres revient à $0{,}8^n<0{,}1$.
Une boucle calcule successivement les termes jusqu'au premier succès ; le logarithme permettra aussi un calcul direct au chapitre 2.
\begin{python}
def seuil_reserve(seuil):
    n, u = 0, 100.0
    while u <= seuil:
        n, u = n + 1, 0.8*u + 30
    return n
\end{python}
Cette fonction est prévue pour $100\leq\text{seuil}<150$. Hors de ce domaine, elle doit être adaptée : un seuil de $150$ ne serait jamais atteint. Une réserve réelle peut déborder ou subir des pertes variables : le modèle a un domaine de validité.
''',[
e('Reconnaître la règle',1,'',r'Donner les quatre premiers termes de $u_n=5+3n$, à partir de $n=0$.@@Donner la raison et $v_4$ si $v_0=16$, $v_{n+1}=v_n/2$.@@Quel modèle convient à une hausse annuelle de $4\,\%$ ?',r'$u_0=5,u_1=8,u_2=11,u_3=14$. La différence vaut $3$.@@La raison vaut $1/2$ et $v_4=16(1/2)^4=1$.@@Une suite géométrique de raison $1{,}04$, si le taux est supposé constant.'),
e('Indices et sommes',1,'',r'Combien de termes contient $u_0+\cdots+u_{12}$ ?@@Calculer $\sum_{k=0}^{4}2^k$.@@Calculer la somme des dix premiers termes de $u_n=3+2n$ à partir de $0$.',r'Il y a $13$ termes, car les deux bornes sont incluses.@@$(1-2^5)/(1-2)=31$.@@Le dernier terme est $u_9=21$ ; la somme vaut $10(3+21)/2=120$.'),
e('Limites de référence',1,'',r'Donner les limites de $3(0{,}6)^n$ et $2(1{,}1)^n$.@@Calculer $\lim(7-4/n)$ puis $\lim(5n+2)/(2n+3)$.@@Pourquoi $u_n<2$ n’entraîne-t-il pas $\lim u_n<2$ ?',r'La première limite vaut $0$ car $0<0{,}6<1$ ; la seconde vaut $+\infty$.@@$7$ ; puis $(5+2/n)/(2+3/n)\to5/2$.@@La suite $2-1/(n+1)$ est toujours inférieure à $2$ et tend vers $2$.'),
e('Un équilibre',1,r'$u_0=4$ et $u_{n+1}=0{,}5u_n+3$.',r'Calculer $u_1,u_2$.@@Déterminer l’équilibre $\ell$.@@Montrer que $u_n=6-2(0{,}5)^n$.',r'$u_1=5$ puis $u_2=5{,}5$.@@$\ell=0{,}5\ell+3$ donne $\ell=6$.@@Avec $v_n=u_n-6$, on obtient $v_{n+1}=0{,}5v_n$, $v_0=-2$ ; donc la formule annoncée.'),
e('Épargne périodique',2,r'Un compte théorique contient $1\,000$ euros ; chaque année il est multiplié par $1{,}02$, puis reçoit $200$ euros. Aucuns frais ni impôts ne sont modélisés.',r'Écrire la récurrence.@@Établir $u_n=11\,000(1{,}02)^n-10\,000$.@@Calculer $u_2$ et interpréter la limite.',r'$u_0=1\,000$, $u_{n+1}=1{,}02u_n+200$.@@L’équilibre est $-10\,000$ ; $u_n+10\,000$ est géométrique de raison $1{,}02$.@@$u_2=1\,444{,}4$ euros. La limite est $+\infty$ dans ce modèle à taux et versements constants.'),
e('Amortissement',2,r'Une dette de $5\,000$ euros porte un intérêt annuel théorique de $5\,\%$, puis un remboursement de $600$ euros a lieu.',r'Écrire le modèle tant que la dette reste positive.@@Exprimer $d_n$.@@Expliquer pourquoi le modèle doit être arrêté, et non poursuivi indéfiniment.',r'$d_0=5\,000$, $d_{n+1}=1{,}05d_n-600$.@@L’équilibre vaut $12\,000$ ; $d_n=12\,000-7\,000(1{,}05)^n$.@@Une dette négative ne représente pas la situation annoncée. À la dernière échéance on ajuste le remboursement au montant effectivement dû.'),
e('Une somme infinie',2,'',r'Calculer $S_n=\sum_{k=0}^{n}6(1/3)^k$.@@Donner sa limite.@@Trouver le premier $n$ tel que $9-S_n<0{,}01$.',r'$S_n=9(1-(1/3)^{n+1})$.@@$9$, puisque $(1/3)^{n+1}\to0$.@@$9-S_n=3^{1-n}$. Pour $n=5$ on a $1/81>0{,}01$ ; pour $n=6$, $1/243<0{,}01$. Le premier rang est $6$.'),
e('Gendarmes',2,r'Pour tout $n\geq1$, $3-2/n\leq u_n\leq3+1/n$.',r'Déterminer $\lim u_n$.@@Donner un rang garantissant $|u_n-3|\leq0{,}01$.@@Peut-on déduire que $(u_n)$ est croissante ?',r'Les deux bornes tendent vers $3$ : le théorème des gendarmes donne $u_n\to3$.@@$|u_n-3|\leq2/n$, donc $n\geq200$ suffit.@@Non. Par exemple $u_n=3+(-1)^n/n$ satisfait ces bornes sans être monotone.'),
e('Construire et conjecturer',3,r'$u_0=0$, $u_{n+1}=\sqrt{2+u_n}$.',r'Calculer $u_1,u_2,u_3$ à $10^{-3}$ près.@@Décrire la construction avec $y=\sqrt{2+x}$ et $y=x$.@@Si une limite positive existe, quelle est-elle ? Cette seule équation prouve-t-elle la convergence ?',r'$1{,}414$, $1{,}848$, $1{,}961$.@@Depuis $u_n$ sur l’axe horizontal, monter à la courbe puis aller horizontalement à la diagonale pour reporter la valeur suivante.@@$\ell=\sqrt{2+\ell}$ implique $\ell^2-\ell-2=0$, donc $\ell=2$ puisque $\ell\geq0$. Cela identifie une limite éventuelle, sans démontrer son existence.'),
e('Changer le pas de temps',3,r'Une population est multipliée par $1{,}21$ tous les deux ans. On suppose une même évolution relative chaque année.',r'Déterminer le coefficient annuel positif.@@Exprimer la population annuelle si $P_0=100$.@@Pourquoi la multiplication par $1{,}105$ chaque année ne convient-elle pas ?',r'$q^2=1{,}21$ donne $q=1{,}1$.@@$P_n=100(1{,}1)^n$.@@Le taux de $21\,\%$ sur deux ans ne se partage pas par addition ; $1{,}105^2=1{,}221025\ne1{,}21$.'),
e('Modèle logistique discret',3,r'On propose $u_{n+1}=u_n+0{,}5u_n(1-u_n/100)$, avec $u_0=20$. Ce modèle guidé est un approfondissement.',r'Calculer les deux termes suivants.@@Déterminer les équilibres.@@Comparer le facteur multiplicatif à celui d’un modèle géométrique et expliquer l’effet de saturation.',r'$u_1=28$ et $u_2=38{,}08$.@@$0{,}5\ell(1-\ell/100)=0$ donne $0$ et $100$.@@Le facteur vaut $1{,}5-0{,}005u_n$ : il diminue lorsque la population augmente. Près de $100$, l’accroissement devient faible ; le modèle géométrique aurait un facteur constant.'),
e('Une preuve plutôt qu’un graphique',3,r'$u_n=150-50(0{,}8)^n$.',r'Prouver que $u_n<150$ et que la suite est croissante.@@Justifier que le programme de seuil du cours s’arrête pour $100\leq s<150$.@@Déterminer le premier rang tel que $u_n>145$.',r'$(0{,}8)^n>0$ donne la borne. $u_{n+1}-u_n=10(0{,}8)^n>0$ donne la croissance.@@La suite tend vers $150$ ; pour tout $s<150$, elle finit par dépasser $s$. La boucle teste chaque rang dans l’ordre.@@$0{,}8^{10}\simeq0{,}107374>0{,}1$, mais $0{,}8^{11}\simeq0{,}085899<0{,}1$ : le premier rang est $11$.')
], 'suites'))

CHAPTERS.append(c('Exponentielle et logarithme','Analyse et calcul',r'Fonctions réciproques · Équations · Échelles',
'Définir le logarithme à partir de l’exponentielle.@@Transformer des expressions et résoudre des équations.@@Calculer un seuil et une durée de demi-vie.@@Relier les propriétés du logarithme aux tables de calcul.',
'Puissances, exponentielle et fonctions croissantes.',r'''
\essSection{1}{Deux fonctions qui se répondent}
La fonction exponentielle est strictement croissante de $\R$ vers $]0,+\infty[$. Chaque réel strictement positif possède un unique antécédent.
\begin{definition}[Logarithme népérien]
Pour $x>0$, $\ln x$ est l'unique réel $y$ tel que $\mathrm e^y=x$.
Ainsi $\ln(\mathrm e^y)=y$ et $\mathrm e^{\ln x}=x$ ; $\ln1=0$ et $\ln\mathrm e=1$.
\end{definition}
Les courbes de deux fonctions réciproques sont symétriques par rapport à $y=x$ lorsque le repère est orthonormé. Le logarithme transforme un facteur multiplicatif en une différence additive.
\figurelivre{c02-reciproques.pdf}{L'exponentielle et le logarithme dans un repère orthonormé. Les points $(0,1)$ et $(1,0)$ se correspondent par symétrie.}
\essSection{2}{Les règles, avec leurs domaines}
\begin{propriete}[Pour $a>0$, $b>0$ et $n\in\Z$]
\[\ln(ab)=\ln a+\ln b,\quad \ln(a/b)=\ln a-\ln b,\quad \ln(a^n)=n\ln a.\]
En particulier $\ln(1/a)=-\ln a$ et $\ln\sqrt a=\tfrac12\ln a$.
\end{propriete}
\begin{demonstration}[Du produit à la somme]
Poser $u=\ln a$ et $v=\ln b$. Alors $ab=\mathrm e^u\mathrm e^v=\mathrm e^{u+v}$ ; prendre le logarithme donne la première identité. Appliquer celle-ci à $a(1/a)=1$ donne la règle de l'inverse.
\end{demonstration}
\begin{attention}
$\ln(a+b)$ ne vaut pas $\ln a+\ln b$. On ne prend pas le logarithme d'un nombre négatif ou nul dans $\R$. L'écriture $\ln(x^2)=2\ln x$ exige $x>0$ ; pour $x\ne0$, la formule générale est $2\ln|x|$.
\end{attention}
\essSection{3}{Résoudre une équation ou une inéquation}
\begin{savoirfaire}[Toujours commencer par le domaine]
Pour $\ln(x-1)+\ln(x+1)=\ln8$, imposer $x>1$.
Puis $\ln(x^2-1)=\ln8$ équivaut à $x^2=9$ ; seule la solution $x=3$ appartient au domaine.
Le logarithme étant strictement croissant, $\ln u\leq\ln v$ équivaut à $u\leq v$ lorsque $u$ et $v$ sont positifs.
\end{savoirfaire}
Pour $q>0$, $q^n=\mathrm e^{n\ln q}$. Si $0<q<1$, alors $\ln q<0$ : diviser une inégalité par $\ln q$ inverse son sens.
La réserve du chapitre 1 dépasse $145$ litres lorsque
$n>\ln(0{,}1)/\ln(0{,}8)\simeq10{,}319$ : le premier entier est $11$.
\essSection{4}{Dérivées et limites de référence}
\begin{propriete}
Sur $]0,+\infty[$, $(\ln x)'=1/x$. Si $u$ est dérivable et strictement positive, $(\ln u)'=u'/u$.
Pour toute fonction dérivable $u$, $(\mathrm e^u)'=u'\mathrm e^u$.
\[\lim_{x\to0^+}\ln x=-\infty,\quad \lim_{x\to+\infty}\ln x=+\infty,
\quad \lim_{x\to-\infty}\mathrm e^x=0,\quad \lim_{x\to+\infty}\mathrm e^x=+\infty.\]
\end{propriete}
En admettant la dérivabilité de $\ln$, dériver $\mathrm e^{\ln x}=x$ donne $\mathrm e^{\ln x}(\ln x)'=1$, soit $(\ln x)'=1/x$.
La règle de composition donne ensuite les dérivées de $\ln u$ et $\mathrm e^u$.
\essSection{5}{Pourquoi des tables de logarithmes ?}
Le programme propose d'étudier l'histoire du logarithme, notamment le passage de progressions géométriques à des progressions arithmétiques. Une table de logarithmes permet de remplacer une multiplication par une addition, puis d'effectuer l'opération inverse par lecture de table.
Pour une même base $a>0$, $a\ne1$, $\log_a x=\ln x/\ln a$. Ainsi $\log_{10}(10^n)=n$.
Les logarithmes décimaux servent à repérer des ordres de grandeur. Les valeurs affichées dans les tables sont approchées : l'erreur de lecture se propage au résultat.
\begin{exemple}[Demi-vie d'un modèle]
Si $N(t)=N_0\mathrm e^{-kt}$ avec $k>0$, la durée $T$ telle que $N(T)=N_0/2$ vérifie $\mathrm e^{-kT}=1/2$, donc $T=\ln2/k$. L'unité de $k$ doit correspondre à celle du temps.
\end{exemple}
''',[
e('Identités immédiates',1,'',r'Calculer $\ln1$, $\ln(\mathrm e^3)$, $\mathrm e^{\ln5}$.@@Simplifier $\ln8-\ln2$.@@Exprimer $\ln(9\sqrt3)$ à l’aide de $\ln3$.',r'$0$, $3$ et $5$, par les identités réciproques.@@$\ln(8/2)=\ln4=2\ln2$.@@$9\sqrt3=3^{5/2}$ donc $\ln(9\sqrt3)=\tfrac52\ln3$.'),
e('Domaine avant calcul',1,'',r'Déterminer le domaine de $\ln(2x-6)$.@@Déterminer celui de $\ln(x^2-1)$.@@Les expressions $2\ln x$ et $\ln(x^2)$ ont-elles le même domaine ?',r'$2x-6>0$, soit $x>3$.@@$x^2>1$, soit $]-\infty,-1[\cup]1,+\infty[$.@@Non : la première exige $x>0$ ; la seconde exige seulement $x\ne0$.'),
e('Équations simples',1,'',r'Résoudre $\mathrm e^{2x}=7$.@@Résoudre $\ln(x+2)=0$.@@Résoudre $\ln x\leq2$.',r'$2x=\ln7$, donc $x=\tfrac12\ln7$.@@Sur $x>-2$, $x+2=1$, donc $x=-1$.@@Sur $x>0$, la croissance de $\ln$ donne $0<x\leq\mathrm e^2$.'),
e('Dériver',1,'',r'Dériver $f(x)=\ln(3x+1)$ sur son domaine.@@Dériver $g(x)=\mathrm e^{-2x}$.@@Dériver $h(x)=\ln(x^2+1)$.',r'$x>-1/3$ et $f\,\!^{\prime}(x)=3/(3x+1)$.@@$g\,\!^{\prime}(x)=-2\mathrm e^{-2x}$.@@$x^2+1>0$ sur $\R$, donc $h\,\!^{\prime}(x)=2x/(x^2+1)$.'),
e('Un seuil de croissance',2,r'$u_n=250(1{,}03)^n$.',r'Résoudre $u_n>400$.@@Donner le premier rang entier et vérifier ses deux voisins.@@Que changerait une condition $u_n\geq400$ ?',r'$n>\ln(1{,}6)/\ln(1{,}03)\simeq15{,}901$.@@Le premier rang est $16$ ; $u_{15}\simeq389{,}49$ et $u_{16}\simeq401{,}18$.@@L’inégalité sur $n$ deviendrait large ; ici le quotient n’étant pas entier, le rang resterait $16$.'),
e('Une décroissance',2,r'$C(t)=80\mathrm e^{-0{,}2t}$, où $t$ est en heures.',r'Calculer la demi-vie.@@Quand $C(t)<10$ ?@@Donner une limite et interpréter le fait que $C(t)$ ne s’annule pas.',r'$T=\ln2/0{,}2\simeq3{,}466$ heures.@@$\mathrm e^{-0{,}2t}<1/8$ équivaut à $t>\ln8/0{,}2\simeq10{,}397$ heures.@@$C(t)\to0$ ; le modèle décrit une approche de zéro, pas une annulation exacte en temps fini.'),
e('Somme de logarithmes',2,'',r'Résoudre $\ln(x-2)+\ln x=\ln3$.@@Pourquoi faut-il écarter une des racines algébriques ?@@Résoudre $\ln(x-2)+\ln x\leq\ln3$.',r'Le domaine est $x>2$. On obtient $x(x-2)=3$, soit $(x-3)(x+1)=0$, donc $x=3$.@@$-1$ annule le polynôme mais n’appartient pas au domaine des logarithmes.@@Sur $x>2$, $x^2-2x-3\leq0$ donne $2<x\leq3$.'),
e('Changer de base',2,'',r'Calculer $\log_{10}(1\,000)$ et $\log_2(32)$.@@Exprimer $\log_2 x$ avec $\ln x$.@@Combien de chiffres possède $2^{20}$ en écriture décimale ?',r'$3$ et $5$, car $1\,000=10^3$ et $32=2^5$.@@$\log_2 x=\ln x/\ln2$ pour $x>0$.@@$\log_{10}(2^{20})=20\log_{10}2\simeq6{,}0206$ ; le nombre est compris entre $10^6$ et $10^7$ et possède donc $7$ chiffres.'),
e('Une propriété à prouver',3,'',r'Prouver $\ln(1/a)=-\ln a$ pour $a>0$.@@En déduire la règle du quotient.@@Un élève écrit $\ln(a-b)=\ln a-\ln b$ : donner un contre-exemple où les deux membres existent.',r'$a(1/a)=1$, donc $\ln a+\ln(1/a)=\ln1=0$.@@$\ln(a/b)=\ln(a\times1/b)=\ln a-\ln b$ pour $a,b>0$.@@Avec $a=3,b=1$, le premier membre vaut $\ln2$ et le second $\ln3$ : ils sont différents.'),
e('Tables de calcul',3,r'Une table donne $\ln2\simeq0{,}693147$ et $\ln3\simeq1{,}098612$.',r'Approcher $\ln6$ puis $\ln(3/2)$.@@Si chaque valeur tabulée a une erreur absolue au plus $5\times10^{-7}$, majorer l’erreur sur la somme et la différence.@@Expliquer l’intérêt historique d’une table et sa limite pratique.',r'$\ln6\simeq1{,}791759$ ; $\ln(3/2)\simeq0{,}405465$.@@L’inégalité triangulaire donne dans les deux cas une erreur au plus $10^{-6}$.@@Les produits et quotients deviennent des sommes et différences ; il faut cependant une lecture inverse de table et maîtriser les arrondis.'),
e('Comparer deux modèles',3,r'$A(t)=100+20t$ et $B(t)=100\mathrm e^{0{,}1t}$ pour $t\geq0$.',r'Comparer leurs taux d’accroissement à $t=0$.@@Montrer que l’égalité des deux modèles équivaut à $\ln(1+0{,}2t)=0{,}1t$.@@Le logarithme donne-t-il directement une formule explicite pour une seconde date de rencontre ?',r'$A\,\!^{\prime}(0)=20$, $B\,\!^{\prime}(0)=10$. Le modèle affine commence plus vite.@@Diviser par $100$ donne $1+0{,}2t=\mathrm e^{0{,}1t}$ ; les deux membres sont positifs et l’application de $\ln$ donne l’équivalence.@@Non : $t$ reste des deux côtés. On utilise une étude de fonction puis une méthode numérique ; $t=0$ est déjà une solution.'),
e('Le piège des inégalités',3,r'$v_n=40(0{,}9)^n$.',r'Déterminer le premier rang tel que $v_n\leq1$.@@Expliquer le changement de sens lors du calcul.@@Écrire une condition équivalente sans logarithme, adaptée à une boucle.',r'$n\geq\ln(1/40)/\ln(0{,}9)\simeq35{,}012$ ; le premier rang est $36$.@@$\ln(0{,}9)<0$ : diviser par ce nombre inverse le sens.@@Initialiser $n=0,v=40$ et répéter tant que $v>1$ : remplacer $v$ par $0{,}9v$ et augmenter $n$ de $1$.')
], 'ln'))

CHAPTERS.append(c('Limites, continuité et équations','Analyse et modèles',r'Asymptotes · Valeurs intermédiaires · Dichotomie',
'Lire et calculer une limite dans un contexte.@@Utiliser la continuité et le théorème des valeurs intermédiaires.@@Justifier l’existence et l’unicité d’une solution.@@Encadrer une solution par balayage ou dichotomie.',
'Fonctions usuelles, variations, exponentielle et logarithme.',r'''
\essSection{1}{Lire le comportement aux bornes}
Une limite décrit les valeurs de $f(x)$ lorsque $x$ se rapproche d'une borne de son domaine, ou devient très grand en valeur absolue. On distingue une limite à gauche et à droite si la fonction n'a pas le même comportement des deux côtés.
\begin{propriete}[Repères usuels]
À $+\infty$, $x^2,x^3,\sqrt x,\mathrm e^x,\ln x$ tendent vers $+\infty$ et $1/x\to0$.
À $-\infty$, $x^2\to+\infty$, $x^3\to-\infty$, $1/x\to0$, $\mathrm e^x\to0$.
À $0^+$, $1/x\to+\infty$, $\sqrt x\to0$, $\ln x\to-\infty$.
\end{propriete}
Si $f(x)\to L$ en $+\infty$ ou $-\infty$, $y=L$ est une asymptote horizontale. Si $f(x)\to\pm\infty$ quand $x\to a$ d'un côté au moins, $x=a$ est une asymptote verticale.
\figurelivre{c03-asymptotes.pdf}{La courbe $y=2+1/(x-1)$ admet les asymptotes $x=1$ et $y=2$. Les branches ne traversent pas la valeur interdite $x=1$.}
\essSection{2}{Calculer sans traiter l'infini comme un nombre}
Pour un quotient de polynômes, factoriser par le terme dominant. Par exemple,
\[\frac{3x^2+x}{2x^2+1}=\frac{3+1/x}{2+1/x^2}\longrightarrow\frac32\quad(x\to+\infty).\]
\begin{attention}[Formes indéterminées]
$\infty-\infty$, $0\times\infty$, $\infty/\infty$ et $0/0$ ne donnent aucune conclusion à eux seuls.
Une factorisation, une simplification ou une comparaison doit lever l'indétermination.
\end{attention}
Pour $x\ne1$, $(x^2-1)/(x-1)=x+1$ ; la limite en $1$ vaut $2$ même si le quotient initial n'y est pas défini.
\essSection{3}{Continuité et solutions}
Intuitivement, une fonction continue sur un intervalle se représente sans rupture. Les fonctions usuelles sont continues sur leur domaine ; une fonction dérivable sur un intervalle y est continue (résultat admis).
\begin{theoreme}[Valeurs intermédiaires, admis]
Si $f$ est continue sur $[a,b]$, toute valeur comprise entre $f(a)$ et $f(b)$ est atteinte au moins une fois sur $[a,b]$.
Si $f$ est de plus strictement monotone, chaque valeur comprise entre ces deux bornes est atteinte exactement une fois.
\end{theoreme}
\begin{savoirfaire}[Existence, puis unicité]
Pour $f(x)=x^3+x-1$ sur $[0,1]$, $f$ est continue, $f(0)=-1$ et $f(1)=1$ : il existe une racine.
Comme $f\,\!^{\prime}(x)=3x^2+1>0$, $f$ est strictement croissante : cette racine est unique.
Une courbe seule ne remplace pas ces deux arguments.
\end{savoirfaire}
Sur un intervalle ouvert, on combine la stricte monotonie avec les limites aux bornes pour déterminer les valeurs atteintes.
Une fonction continue strictement monotone possède une réciproque définie sur son image. Par exemple, le carré sur $[0,+\infty[$ a pour réciproque la racine carrée. Sur tout $\R$, le carré n'est pas injectif et n'a pas de réciproque unique.
\essSection{4}{Encadrer une solution}
Un balayage teste des valeurs espacées d'un pas fixe ; une dichotomie divise par deux un intervalle où la fonction continue change de signe. L'unicité n'est pas nécessaire au maintien d'au moins une racine dans l'intervalle, mais elle permet d'identifier celle que l'on approche.
\begin{python}
def dichotomie(f, a, b, precision):
    assert precision > 0 and a < b
    assert f(a) * f(b) <= 0
    if f(a) == 0: return a, a
    if f(b) == 0: return b, b
    while b - a > precision:
        m = (a + b) / 2
        if f(m) == 0: return m, m
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return a, b
\end{python}
Après $n$ divisions, la largeur vaut $(b_0-a_0)/2^n$ si aucun zéro exact n'a été rencontré.
Pour $x^3+x-1$, les signes en $0{,}682$ et $0{,}683$ donnent un encadrement de largeur $0{,}001$.
\begin{exemple}[Une autre méthode, guidée]
La tangente à la courbe en $x_n$ coupe l'axe des abscisses en $x_{n+1}=x_n-f(x_n)/f\,\!^{\prime}(x_n)$ : c'est la méthode de Newton. Elle peut être rapide, mais exige une dérivée non nulle et des précautions de convergence. La dichotomie, avec ses hypothèses, fournit un encadrement garanti.
\end{exemple}
''',[
e('Limites usuelles',1,'',r'Donner les limites de $1/x$ en $0^+$ et $0^-$.@@Donner la limite de $\sqrt{x+1}$ en $+\infty$.@@Donner la limite de $3+\mathrm e^{-x}$ en $+\infty$.',r'$+\infty$ à droite et $-\infty$ à gauche.@@$+\infty$, car $x+1\to+\infty$ et la racine augmente sans borne.@@$3$ : $\mathrm e^{-x}\to0$.'),
e('Asymptotes',1,r'$f(x)=4+2/(x+3)$.',r'Donner son domaine.@@Déterminer ses asymptotes.@@Peut-on calculer $f(-3)$ ?',r'$\R\setminus\{-3\}$.@@$x=-3$ est verticale ; $y=4$ est horizontale aux deux infinis.@@Non : le dénominateur est nul. Une asymptote verticale n’est pas un point de la courbe.'),
e('Factoriser',1,'',r'Calculer $\lim_{x\to+\infty}(5x+2)/(x+7)$.@@Calculer $\lim_{x\to+\infty}(2x^2-1)/(x^3+1)$.@@Calculer $\lim_{x\to2}(x^2-4)/(x-2)$.',r'$(5+2/x)/(1+7/x)\to5$.@@En divisant par $x^3$, le quotient tend vers $0$.@@Pour $x\ne2$, le quotient vaut $x+2$ ; la limite est $4$.'),
e('Carré et réciproque',1,'',r'Pourquoi $x\mapsto x^2$ n’est-elle pas strictement monotone sur $\R$ ?@@Donner sa réciproque sur $[0,+\infty[$.@@Résoudre $\sqrt x=3$ et préciser le domaine.',r'$(-1)^2=1^2$ : deux antécédents distincts ont la même image.@@$y\mapsto\sqrt y$ sur $[0,+\infty[$ ; les graphes sont symétriques par rapport à $y=x$.@@Le domaine est $x\geq0$ ; élever au carré donne $x=9$, qui convient.'),
e('Une racine unique',2,r'$f(x)=x^3+2x-2$.',r'Justifier une racine dans $[0,1]$.@@Justifier son unicité sur $\R$.@@L’encadrer entre deux centièmes consécutifs.',r'$f$ est continue, $f(0)=-2$ et $f(1)=1$ : le théorème des valeurs intermédiaires s’applique.@@$f\,\!^{\prime}(x)=3x^2+2>0$ sur $\R$.@@$f(0{,}77)=-0{,}003467<0$ et $f(0{,}78)=0{,}034552>0$ : $0{,}77<\alpha<0{,}78$.'),
e('Compter les solutions',2,r'$f$ est continue, strictement croissante sur $[-2,0]$, puis strictement décroissante sur $[0,3]$. On sait $f(-2)=-1$, $f(0)=4$, $f(3)=1$.',r'Combien de solutions possède $f(x)=2$ ?@@Combien pour $f(x)=0$ ?@@Combien pour $f(x)=4$ ?',r'Une sur chacun des deux intervalles monotones, donc deux.@@Une sur $[-2,0]$ ; aucune sur $[0,3]$, où les valeurs sont au moins $1$.@@Une seule : $x=0$. Le point commun aux deux intervalles ne doit pas être compté deux fois.'),
e('Une inéquation avec un zéro',2,r'$g(x)=\mathrm e^x+x$ sur $\R$.',r'Montrer que $g$ est strictement croissante.@@Justifier une unique solution $\alpha$ à $g(x)=0$.@@Résoudre $g(x)\leq0$ à l’aide de $\alpha$.',r'$g\,\!^{\prime}(x)=\mathrm e^x+1>0$.@@$g$ est continue, sa limite en $-\infty$ vaut $-\infty$, et celle en $+\infty$ vaut $+\infty$ : existence et unicité.@@Par croissance stricte, l’ensemble des solutions est $]-\infty,\alpha]$.'),
e('Précision de la dichotomie',2,'',r'Après dix divisions de $[0,1]$, quelle est la largeur ?@@Combien de divisions garantissent une largeur au plus $10^{-4}$ ?@@Si l’on rend le milieu, majorer l’erreur après ces divisions.',r'$2^{-10}=1/1024\simeq0{,}0009766$.@@Il faut $2^n\geq10^4$ : $2^{13}=8192$ et $2^{14}=16384$, donc $14$ divisions.@@La racine est dans l’intervalle : l’erreur sur le milieu est au plus la demi-largeur, soit $1/32768\simeq3{,}052\times10^{-5}$.'),
e('La continuité est nécessaire',3,r'On définit $f(x)=-1$ pour $x<0$ et $f(x)=1$ pour $x\geq0$.',r'Comparer $f(-1)$ et $f(1)$ à zéro.@@Existe-t-il un zéro sur $[-1,1]$ ?@@Quelle hypothèse du théorème manque ?',r'$f(-1)=-1<0<1=f(1)$.@@Non : la fonction ne prend que les valeurs $-1$ et $1$.@@La continuité en $0$ manque. Un changement de signe aux bornes ne suffit pas sans continuité.'),
e('Une limite trompeuse',3,r'$h(x)=\sqrt{x^2+x}-x$ pour $x>0$.',r'Identifier la forme indéterminée en $+\infty$.@@Multiplier par l’expression conjuguée.@@En déduire la limite.',r'Les deux termes tendent vers $+\infty$ : forme $\infty-\infty$.@@$h(x)=x/(\sqrt{x^2+x}+x)=1/(\sqrt{1+1/x}+1)$.@@La limite vaut $1/(1+1)=1/2$.'),
e('Newton sur un exemple',3,r'Pour approcher $\sqrt2$, on applique Newton à $f(x)=x^2-2$, avec $x_0=1{,}5$.',r'Établir $x_{n+1}=(x_n+2/x_n)/2$.@@Calculer $x_1$ puis $x_2$ à $10^{-6}$ près.@@Pourquoi $x_0=0$ serait-il impossible ?',r'$x-f(x)/f\,\!^{\prime}(x)=x-(x^2-2)/(2x)=(x+2/x)/2$ pour $x\ne0$.@@$x_1=17/12\simeq1{,}416667$, $x_2=577/408\simeq1{,}414216$.@@La dérivée $f\,\!^{\prime}(0)=0$ annule le dénominateur de la formule.'),
e('Une recette de résolution',3,r'On cherche $\ln x+x=2$ sur $]0,+\infty[$.',r'Prouver l’existence et l’unicité.@@Encadrer la solution entre $1{,}55$ et $1{,}56$.@@Proposer un algorithme dont le résultat est un intervalle de largeur au plus $10^{-5}$.',r'$f(x)=\ln x+x-2$ est continue, de dérivée $1/x+1>0$ ; ses limites aux bornes sont $-\infty$ et $+\infty$.@@$f(1{,}55)\simeq-0{,}011745$ ; $f(1{,}56)\simeq0{,}004686$. Le changement de signe et la croissance donnent l’encadrement.@@Appliquer la fonction de dichotomie du cours sur $[1{,}55,1{,}56]$ avec précision $10^{-5}$ ; vérifier le changement de signe initial et conserver le sous-intervalle correspondant à chaque étape.')
], 'continuite'))

CHAPTERS.append(c('Dérivation et optimisation','Analyse et modèles',r'Composition · Variations · Coûts · Extremums',
'Calculer les dérivées des fonctions du programme.@@Construire un tableau de variation.@@Optimiser une grandeur sur son domaine.@@Distinguer coût moyen, coût marginal et recette.',
'Dérivées usuelles de Première et règles de calcul.',r'''
\essSection{1}{La dérivée mesure une variation locale}
Pour une fonction dérivable, $f\,\!^{\prime}(a)$ est le coefficient directeur de la tangente en $a$.
L'équation de cette tangente est $y=f(a)+f\,\!^{\prime}(a)(x-a)$.
Localement, $f(a+h)\simeq f(a)+hf\,\!^{\prime}(a)$ : c'est une approximation, dont la précision dépend de $h$ et de la fonction.
\begin{propriete}[Règles de calcul]
$(u+v)'=u'+v'$, $(uv)'=u'v+uv'$ ; pour $v\ne0$,
$(u/v)'=(u'v-uv')/v^2$.
\[(f(ax+b))'=af\,\!^{\prime}(ax+b),\quad (u^2)'=2uu',\quad(\mathrm e^u)'=u'\mathrm e^u,\quad(\ln u)'=u'/u\ (u>0).\]
\end{propriete}
Un domaine de définition et un domaine de dérivabilité peuvent différer : $\sqrt x$ est définie en $0$, mais sa dérivée $1/(2\sqrt x)$ n'y existe pas comme nombre réel fini.
\essSection{2}{Du signe aux variations}
\begin{theoreme}[Admis]
Sur un intervalle, $f\,\!^{\prime}\geq0$ implique que $f$ est croissante ; $f\,\!^{\prime}\leq0$ implique qu'elle est décroissante.
Un changement de signe de $+$ vers $-$ donne un maximum local ; de $-$ vers $+$, un minimum local.
\end{theoreme}
Un tableau de variation doit contenir le domaine, les valeurs critiques, le signe de la dérivée et les valeurs ou limites aux bornes.
\begin{exemple}[Production]
Pour $B(x)=-x^2+12x-20$ sur $[0,10]$, $B\,\!^{\prime}(x)=12-2x$.
La fonction croît sur $[0,6]$ puis décroît sur $[6,10]$ ; son maximum est $B(6)=16$.
\begin{center}\begin{tabular}{c|ccc}$x$&$0$&$6$&$10$\\\hline
$B\,\!^{\prime}(x)$&$+$&$0$&$-$\\$B(x)$&$-20$&$\nearrow16\searrow$&$0$\end{tabular}\end{center}
\end{exemple}
\figurelivre{c04-optimisation.pdf}{À périmètre fixé de $40$ m, l'aire $A(x)=x(20-x)$ est maximale pour $x=10$ m. Le domaine physique $[0,20]$ doit être imposé avant l'étude.}
\essSection{3}{Une méthode d'optimisation complète}
\begin{savoirfaire}
Choisir la variable et son unité ; écrire les contraintes ; exprimer la grandeur à optimiser ; déterminer son domaine ; dériver ; étudier le signe ; comparer les valeurs aux bornes et aux points critiques ; conclure dans le contexte.
\end{savoirfaire}
Une dérivée nulle ne suffit pas à conclure à un extremum : pour $f(x)=x^3$, $f\,\!^{\prime}(0)=0$ mais $f$ reste croissante.
Sur un domaine entier, une solution réelle sert à repérer les entiers voisins qu'il faut comparer.
\essSection{4}{Coût moyen et coût marginal}
Pour une production positive $x$, le coût moyen est $C_m(x)=C(x)/x$.
Le coût marginal est souvent modélisé par $C\,\!^{\prime}(x)$ ; le véritable coût d'une unité supplémentaire est $C(x+1)-C(x)$.
\begin{exemple}[Un minimum de coût moyen]
Si $C(x)=x^2+20x+400$, alors $C_m(x)=x+20+400/x$ pour $x>0$.
Sa dérivée vaut $1-400/x^2$ : négative avant $20$, positive après. Le coût moyen minimal est $C_m(20)=60$.
La recette $R(x)$ et le bénéfice $B(x)=R(x)-C(x)$ sont des grandeurs différentes du coût.
\end{exemple}
\essSection{5}{Contrôler un résultat}
Un graphique permet de détecter un signe inversé ; une valeur numérique teste une formule. Pour conclure, on revient à la dérivée et au domaine.
Le résultat doit conserver son unité. Si $x$ est un temps en secondes et $f$ une distance en mètres, $f\,\!^{\prime}$ s'exprime en mètres par seconde.
''',[
e('Règles usuelles',1,'',r'Dériver $3x^4-2x+7$.@@Dériver $(2x-1)^2$.@@Dériver $\mathrm e^{3x+2}$.',r'$12x^3-2$.@@$2(2x-1)\times2=8x-4$.@@$3\mathrm e^{3x+2}$, par composition.'),
e('Quotient et produit',1,'',r'Dériver $x\mathrm e^x$.@@Dériver $(x+1)/(x+2)$ sur son domaine.@@Dériver $\ln(1+x^2)$.',r'$\mathrm e^x+x\mathrm e^x=(x+1)\mathrm e^x$.@@Pour $x\ne-2$, la dérivée vaut $[(x+2)-(x+1)]/(x+2)^2=1/(x+2)^2$.@@$2x/(1+x^2)$ sur $\R$.'),
e('Tangente',1,r'$f(x)=x^2+1$.',r'Calculer $f(2)$ et $f\,\!^{\prime}(2)$.@@Donner la tangente en $2$.@@Utiliser cette tangente pour approcher $f(2{,}01)$ et comparer à la valeur exacte.',r'$f(2)=5$ et $f\,\!^{\prime}(2)=4$.@@$y=5+4(x-2)=4x-3$.@@$f(2{,}01)\simeq5{,}04$ ; la valeur exacte est $5{,}0401$, soit une erreur de $0{,}0001$.'),
e('Signe et tableau',1,r'$f(x)=x^2-6x+5$ sur $[0,5]$.',r'Calculer la dérivée et son zéro.@@Donner les variations.@@Déterminer le minimum et le maximum sur cet intervalle.',r'$f\,\!^{\prime}(x)=2x-6$, nulle en $3$.@@Décroissance sur $[0,3]$, puis croissance sur $[3,5]$.@@Minimum $f(3)=-4$ ; aux bornes $f(0)=5$, $f(5)=0$, donc maximum $5$.'),
e('Rectangle',2,r'Un rectangle a un périmètre de $60$ m. Une longueur vaut $x$.',r'Exprimer son aire et son domaine physique.@@Maximiser l’aire.@@Conclure avec les dimensions et l’unité de l’aire.',r'L’autre longueur vaut $30-x$, donc $A=x(30-x)$, avec $0<x<30$ pour un rectangle non dégénéré.@@$A\,\!^{\prime}=30-2x$ change de $+$ à $-$ en $15$.@@Le carré de côté $15$ m maximise l’aire, qui vaut $225$ m$^2$.'),
e('Bénéfice',2,r'$R(x)=40x$ et $C(x)=x^2+10x+100$ pour $0\leq x\leq30$.',r'Exprimer $B=R-C$.@@Déterminer la production qui maximise $B$.@@Déterminer les productions à bénéfice positif.',r'$B(x)=-x^2+30x-100$.@@$B\,\!^{\prime}=30-2x$ : maximum en $x=15$, égal à $125$.@@Les racines sont $15\pm5\sqrt5$ ; le bénéfice est positif strictement entre ces deux racines, soit environ $3{,}82<x<26{,}18$.'),
e('Coût moyen',2,r'$C(x)=2x^2+18x+200$ pour $x>0$.',r'Exprimer le coût moyen.@@Trouver son minimum.@@Comparer $C\,\!^{\prime}(10)$ et $C(11)-C(10)$.',r'$C_m(x)=2x+18+200/x$.@@$C_m\,\!^{\prime}=2-200/x^2$ change de signe en $10$ ; minimum $58$.@@$C\,\!^{\prime}(10)=58$ ; la différence exacte vaut $2(121-100)+18=60$. Le coût marginal est ici une approximation.'),
e('Une exponentielle composée',2,r'$f(x)=x\mathrm e^{-x}$ pour $x\geq0$.',r'Calculer la dérivée.@@Dresser les variations.@@Déterminer le maximum et préciser sa valeur exacte.',r'$f\,\!^{\prime}(x)=(1-x)\mathrm e^{-x}$.@@L’exponentielle étant positive, $f$ croît jusqu’à $1$ puis décroît.@@Le maximum vaut $f(1)=\mathrm e^{-1}$, atteint en $x=1$.'),
e('Une boîte sans couvercle',3,r'Dans un carré de $12$ cm de côté, on découpe quatre carrés de côté $x$ aux coins et on replie les bords.',r'Exprimer le volume et son domaine.@@Factoriser sa dérivée.@@Déterminer le volume maximal.',r'$V(x)=x(12-2x)^2$ pour $0<x<6$.@@$V\,\!^{\prime}(x)=(12-2x)(12-6x)$.@@Sur le domaine, le premier facteur est positif ; le signe change en $x=2$. Le maximum vaut $2\times8^2=128$ cm$^3$.'),
e('Dérivée nulle : attention',3,'',r'Comparer le signe de la dérivée de $x^3$ de part et d’autre de zéro.@@Le point $0$ est-il un extremum ?@@Pour $x^4$, quelle différence observe-t-on ?',r'$3x^2\geq0$ des deux côtés ; elle s’annule seulement en zéro.@@Non : les valeurs sont négatives à gauche, positives à droite et la fonction reste croissante.@@La dérivée $4x^3$ change de $-$ à $+$ : zéro est un minimum.'),
e('Production entière',3,r'$B(x)=-2x^2+19x-20$ ; la production doit être un entier de $0$ à $10$.',r'Trouver le maximum sur le domaine réel.@@Comparer les entiers voisins.@@Conclure pour le problème initial.',r'$B\,\!^{\prime}=-4x+19$ s’annule en $19/4=4{,}75$.@@$B(4)=24$, $B(5)=25$.@@La fonction croît avant $4{,}75$ puis décroît : l’entier optimal est $5$ avec un bénéfice de $25$ unités monétaires.'),
e('Deux disciplines, un modèle',3,r'Une distance est modélisée par $s(t)=20t-2t^2$ pour $0\leq t\leq5$, en mètres et secondes.',r'Exprimer la vitesse et son unité.@@À quel instant la distance à l’origine est-elle maximale sur l’intervalle ?@@Pourquoi ne peut-on prolonger automatiquement cette formule à tout $t>5$ ?',r'$v(t)=s\,\!^{\prime}(t)=20-4t$, en m/s.@@La vitesse est positive avant $5$ puis nulle à $5$ ; le maximum sur $[0,5]$ vaut $s(5)=50$ m.@@Le domaine de validité est imposé par le phénomène. Le prolongement prédirait ensuite un mouvement de retour qui doit être justifié physiquement.')
], 'derivation'))

CHAPTERS.append(c('Convexité et inégalités','Analyse et répartition',r'Sécantes · Tangentes · Inflexion · Lorenz',
'Reconnaître convexité et concavité sur un graphique.@@Utiliser le signe de la dérivée seconde.@@Justifier une inégalité par une tangente.@@Lire une courbe de Lorenz et comparer des répartitions.',
'Dérivation, variations et pourcentages cumulés.',r'''
\essSection{1}{La position des cordes}
\begin{definition}
Une fonction est \textbf{convexe} sur un intervalle si sa courbe est située sous chaque segment reliant deux de ses points. Elle est \textbf{concave} si sa courbe est au-dessus de ces segments.
\end{definition}
Une fonction peut être croissante et concave : les valeurs augmentent alors que les pentes diminuent. La convexité décrit la variation des pentes, pas le signe de la fonction ni son sens de variation.
\figurelivre{c05-convexite.pdf}{La parabole est sous la corde et au-dessus de ses tangentes. Pour le logarithme, les positions sont inversées : il est concave sur $]0,+\infty[$.}
\essSection{2}{Deux critères admis}
\begin{propriete}
Pour $f$ dérivable, $f$ est convexe si et seulement si $f\,\!^{\prime}$ est croissante ; sa courbe est alors au-dessus de toutes ses tangentes.
Si $f$ est deux fois dérivable, $f\,\!^{\prime\prime}\geq0$ assure la convexité et $f\,\!^{\prime\prime}\leq0$ la concavité.
\end{propriete}
\begin{definition}[Inflexion]
Un point d'inflexion est un point de la courbe où la convexité change. Dans les cas étudiés ici, un changement de signe de $f\,\!^{\prime\prime}$ permet de le reconnaître.
Une dérivée seconde nulle ne suffit pas : $x^4$ reste convexe de part et d'autre de $0$.
\end{definition}
\begin{exemple}[Une courbe en S]
Pour $f(x)=x^3$, $f\,\!^{\prime\prime}(x)=6x$ : concavité sur $]-\infty,0]$, convexité sur $[0,+\infty[$ et inflexion en $(0,0)$.
\end{exemple}
\essSection{3}{Obtenir une inégalité}
L'exponentielle est convexe et sa tangente en $0$ est $y=1+x$. On obtient, pour tout réel $x$, $\mathrm e^x\geq1+x$.
Le logarithme est concave et sa tangente en $1$ est $y=x-1$. Pour $x>0$, $\ln x\leq x-1$.
\begin{savoirfaire}[Étudier une convexité]
Calculer $f\,\!^{\prime}$ puis $f\,\!^{\prime\prime}$ ; factoriser et étudier le signe sur le domaine ; annoncer les intervalles ; vérifier un changement effectif de signe avant de conclure à une inflexion ; calculer les coordonnées du point.
\end{savoirfaire}
\essSection{4}{Classer une population pour lire une répartition}
On classe les personnes par richesse croissante. Une courbe de Lorenz associe à une proportion cumulée $x$ de population la proportion cumulée $L(x)$ de richesse possédée.
Dans les modèles usuels du thème, $L(0)=0$, $L(1)=1$, $L$ est croissante et convexe sur $[0,1]$, et $L(x)\leq x$.
La diagonale $L(x)=x$ correspond à l'égalité parfaite.
\figurelivre{c05-lorenz.pdf}{Les courbes $L(x)=x^2$ et $L(x)=x^3$ sont des modèles fictifs. À $x=0{,}5$, la première attribue $25\,\%$ de la richesse à la moitié la moins riche ; la seconde, $12{,}5\,\%$.}
\begin{exemple}[Ne pas inverser les axes]
Si $L(0{,}8)=0{,}6$, les $80\,\%$ les moins riches possèdent $60\,\%$ de la richesse. Les $20\,\%$ les plus riches en possèdent donc $40\,\%$. Cela ne signifie pas que $60\,\%$ de la population possède $80\,\%$ de la richesse.
\end{exemple}
\essSection{5}{Quantiles et dispersion}
La médiane partage la série ordonnée en deux groupes. $Q_1$ et $Q_3$ délimitent les quartiles ; $D_1$ et $D_9$ les déciles.
Le rapport interdécile $D_9/D_1$, lorsque $D_1>0$, compare deux seuils ; il ne donne pas le rapport des richesses totales de deux groupes.
Pour une petite série discrète, on annonce la convention de quantile employée. Au chapitre 7, le calcul intégral donnera un autre indicateur, l'indice de Gini.
''',[
e('Signe de la dérivée seconde',1,'',r'Étudier la convexité de $x^2+3x$.@@Étudier celle de $-x^2$.@@Étudier celle de $\mathrm e^x$.',r'La dérivée seconde vaut $2>0$ : convexe sur $\R$.@@Elle vaut $-2<0$ : concave sur $\R$.@@Elle vaut $\mathrm e^x>0$ : convexe sur $\R$.'),
e('Logarithme et racine',1,'',r'Calculer la dérivée seconde de $\ln x$.@@Quelle est sa convexité ?@@Calculer la dérivée seconde de $\sqrt x$ pour $x>0$.',r'$-1/x^2$.@@Elle est strictement concave sur $]0,+\infty[$ car cette dérivée est négative.@@$-1/(4x^{3/2})<0$ : la racine est concave sur cet intervalle.'),
e('Inflexion',1,r'$f(x)=x^3-3x$.',r'Calculer $f\,\!^{\prime\prime}$.@@Donner les intervalles de convexité et concavité.@@Donner le point d’inflexion.',r'$f\,\!^{\prime}=3x^2-3$, donc $f\,\!^{\prime\prime}=6x$.@@Concave avant $0$, convexe après $0$.@@La dérivée seconde change de signe en $0$ ; le point est $(0,0)$.'),
e('Lire Lorenz',1,r'Une courbe fictive vérifie $L(0{,}4)=0{,}1$ et $L(0{,}9)=0{,}7$.',r'Interpréter la première valeur.@@Quelle richesse possèdent les $10\,\%$ les plus riches ?@@Quelle richesse possède le groupe compris entre les proportions $0{,}4$ et $0{,}9$ ?',r'Les $40\,\%$ les moins riches possèdent $10\,\%$ de la richesse.@@$1-0{,}7=0{,}3$, soit $30\,\%$.@@$0{,}7-0{,}1=0{,}6$, soit $60\,\%$, pour ce groupe de $50\,\%$ de la population.'),
e('Une exponentielle amortie',2,r'$f(x)=x\mathrm e^{-x}$ sur $[0,+\infty[$.',r'Calculer $f\,\!^{\prime\prime}$.@@Étudier la convexité.@@Donner le point d’inflexion.',r'$f\,\!^{\prime}=(1-x)\mathrm e^{-x}$, donc $f\,\!^{\prime\prime}=(x-2)\mathrm e^{-x}$.@@Concave sur $[0,2]$, convexe sur $[2,+\infty[$.@@$(2,2\mathrm e^{-2})$, car le signe change en $2$.'),
e('Une tangente utile',2,'',r'Donner la tangente à $\mathrm e^x$ en zéro.@@En déduire une minoration de $\mathrm e^{0{,}2}$.@@Donner une majoration de $\ln(1{,}2)$ par la tangente du logarithme en $1$.',r'$y=1+x$.@@La convexité donne $\mathrm e^{0{,}2}\geq1{,}2$.@@La concavité donne $\ln(1{,}2)\leq0{,}2$.'),
e('Comparer deux répartitions',2,r'$L_A(x)=x^2$ et $L_B(x)=x^3$ sur $[0,1]$.',r'Vérifier les extrémités et la croissance.@@Comparer les deux courbes.@@Quel modèle est le plus éloigné de l’égalité au sens de Lorenz ?',r'Les deux valent $0$ en $0$ et $1$ en $1$ ; leurs dérivées $2x$ et $3x^2$ sont positives ou nulles.@@$L_A-L_B=x^2(1-x)\geq0$.@@$B$ : pour toute proportion intermédiaire, les personnes les moins riches détiennent une part plus faible.'),
e('Déciles',2,r'Dans une série fictive de revenus, $D_1=900$, la médiane vaut $1\,800$ et $D_9=3\,600$ euros.',r'Calculer le rapport interdécile.@@Peut-on affirmer que les $10\,\%$ les plus riches possèdent quatre fois la richesse des $10\,\%$ les moins riches ?@@Quel renseignement manque pour construire une courbe de Lorenz ?',r'$D_9/D_1=3\,600/900=4$.@@Non. Ce rapport compare des seuils de revenus, pas des masses de revenus cumulées.@@Il faut les parts cumulées de revenu associées aux proportions cumulées de population, ou les données individuelles ordonnées.'),
e('Zéro sans inflexion',3,r'$f(x)=x^4$.',r'Calculer la dérivée seconde.@@Que se passe-t-il en zéro ?@@Formuler une règle correcte pour repérer un point d’inflexion dans les exemples deux fois dérivables.',r'$f\,\!^{\prime\prime}=12x^2$.@@Elle s’annule mais ne change pas de signe ; la fonction reste convexe.@@Rechercher un changement de convexité, notamment un changement de signe de la dérivée seconde, plutôt qu’une simple annulation.'),
e('Un modèle admissible ?',3,r'On propose $L(x)=2x-x^2$ pour une courbe de Lorenz.',r'Vérifier les extrémités et la croissance.@@Comparer $L(x)$ à $x$.@@Expliquer pourquoi ce modèle ne convient pas avec un classement par richesse croissante.',r'$L(0)=0,L(1)=1$ et $L\,\!^{\prime}=2-2x\geq0$ sur $[0,1]$.@@$L-x=x(1-x)\geq0$, strictement à l’intérieur.@@La courbe est au-dessus de l’égalité et concave. Les groupes les moins riches ne peuvent cumuler plus que leur part de population selon cette définition.'),
e('Convexité sans croissance',3,r'$f(x)=\mathrm e^{-x}$ sur $\R$.',r'Calculer les deux premières dérivées.@@Donner le sens de variation et la convexité.@@Réfuter « toute fonction convexe est croissante ».',r'$f\,\!^{\prime}=-\mathrm e^{-x}$ et $f\,\!^{\prime\prime}=\mathrm e^{-x}$.@@La fonction est strictement décroissante et convexe sur $\R$.@@Cette fonction constitue un contre-exemple : la convexité porte sur la croissance de la dérivée, pas sur le signe de celle-ci.'),
e('Une courbe logistique',3,r'$f(x)=1/(1+\mathrm e^{-x})$. On donne $f\,\!^{\prime\prime}(x)=\mathrm e^{-x}(\mathrm e^{-x}-1)/(1+\mathrm e^{-x})^3$.',r'Étudier le signe de la dérivée seconde.@@Déterminer l’inflexion.@@Interpréter le changement de convexité pour une croissance avec saturation.',r'Le dénominateur et $\mathrm e^{-x}$ sont positifs ; $\mathrm e^{-x}-1$ est positif si $x<0$, négatif si $x>0$.@@Convexe avant zéro, concave après ; inflexion en $(0,1/2)$.@@Avant l’inflexion la pente augmente ; après, la croissance ralentit vers une valeur de saturation. Cette interprétation concerne le modèle, pas une loi universelle.')
], 'derivation'))

CHAPTERS.append(c('Primitives et équations différentielles','Analyse et évolution',r'Familles de solutions · Condition initiale · Euler',
r'Reconnaître et déterminer des primitives.@@Vérifier une solution d’équation différentielle.@@Résoudre les équations $y\,\!^{\prime}=ay+b$.@@Comparer modèle continu et approximation par Euler.',
'Dérivation, exponentielle et récurrences affines.',r'''
\essSection{1}{Remonter d'une dérivée à une fonction}
\begin{definition}
Une primitive de $f$ sur un intervalle $I$ est une fonction $F$ dérivable telle que $F\,\!^{\prime}=f$ sur $I$.
Si $F$ est une primitive, toutes les primitives sur cet intervalle sont $F+C$, où $C$ est une constante réelle.
\end{definition}
\begin{demonstration}
Si $F$ et $G$ sont deux primitives, $(F-G)'=0$ sur l'intervalle. Une fonction de dérivée nulle sur un intervalle est constante, donc $F-G=C$.
L'hypothèse d'intervalle compte : sur deux morceaux disjoints, les constantes peuvent être différentes.
\end{demonstration}
\begin{center}\begin{tabular}{c|c}Fonction & Une primitive\\\hline
$x^n$ ($n\in\N$)&$x^{n+1}/(n+1)$\\
$1/x$ sur $]0,+\infty[$&$\ln x$\\
$\mathrm e^{ax+b}$ ($a\ne0$)&$\mathrm e^{ax+b}/a$\\
$2uu'$&$u^2$\\
$u'\mathrm e^u$&$\mathrm e^u$\\
$u'/u$ ($u>0$)&$\ln u$\end{tabular}\end{center}
\begin{exemple}[Reconnaître une forme]
Une primitive de $6x(x^2+1)^2$ est $(x^2+1)^3$, car sa dérivée vaut $3(x^2+1)^2\times2x$.
Pour $2x/(x^2+1)$, une primitive est $\ln(x^2+1)$.
Toujours dériver la proposition pour la contrôler.
\end{exemple}
\essSection{2}{Une équation portant sur une fonction}
Une équation différentielle relie une fonction inconnue et ses dérivées. Vérifier une solution consiste à calculer la dérivée puis à substituer les expressions dans l'équation, pour tout point du domaine.
Une condition initiale impose une valeur, par exemple $y(0)=y_0$.
\begin{theoreme}[$y\,\!^{\prime}=ay$]
Les solutions sur $\R$ sont $y(t)=C\mathrm e^{at}$ avec $C\in\R$. Avec $y(0)=y_0$, la solution unique est $y(t)=y_0\mathrm e^{at}$.
\end{theoreme}
\begin{demonstration}
Pour une solution $y$, poser $g(t)=y(t)\mathrm e^{-at}$. Alors $g\,\!^{\prime}(t)=(y\,\!^{\prime}-ay)\mathrm e^{-at}=0$.
Donc $g=C$, d'où $y=C\mathrm e^{at}$. La réciproque se vérifie en dérivant.
\end{demonstration}
\essSection{3}{Ajouter un terme constant}
\begin{savoirfaire}[$y\,\!^{\prime}=ay+b$]
Si $a\ne0$, la solution constante est $\ell=-b/a$. Poser $z=y-\ell$ : $z\,\!^{\prime}=az$.
Ainsi $y(t)=\ell+C\mathrm e^{at}$ ; avec $y(0)=y_0$, $C=y_0-\ell$.
Si $a=0$, l'équation est $y\,\!^{\prime}=b$, donc $y(t)=bt+C$.
\end{savoirfaire}
\begin{exemple}[Refroidissement]
Le modèle $T\,\!^{\prime}=-0{,}2(T-20)$, $T(0)=80$ donne $T(t)=20+60\mathrm e^{-0{,}2t}$.
La température tend vers $20$, celle de l'environnement supposée constante. Le coefficient $0{,}2$ dépend de l'unité de temps.
\end{exemple}
\figurelivre{c06-equadiff.pdf}{La solution exacte du refroidissement et les valeurs d'Euler avec pas $1$. Euler utilise des segments de tangente et donne une approximation, pas une identité.}
\essSection{4}{Du continu au discret : Euler}
Pour $y\,\!^{\prime}=f(t,y)$ et un pas $h>0$, la méthode d'Euler donne
$t_{n+1}=t_n+h$ et $y_{n+1}=y_n+h f(t_n,y_n)$.
Pour le refroidissement, $T_{n+1}=(1-0{,}2h)T_n+4h$ : on retrouve une suite arithmético-géométrique.
\begin{python}
def euler_refroidissement(h, n):
    t, temperature = 0.0, 80.0
    points = [(t, temperature)]
    for k in range(n):
        temperature += h*(-0.2*temperature + 4)
        t += h
        points.append((t, temperature))
    return points
\end{python}
Un pas trop grand peut produire un comportement artificiel. Réduire $h$ et comparer à une solution connue permet de contrôler l'approximation. Les équations non linéaires, comme la logistique, peuvent être explorées sur un exemple guidé sans théorie générale exigée.
''',[
e('Primitives usuelles',1,'',r'Donner toutes les primitives de $3x^2-4$.@@Donner celles de $\mathrm e^{2x}$.@@Donner celles de $1/x$ sur $]0,+\infty[$.',r'$x^3-4x+C$, $C\in\R$.@@$\tfrac12\mathrm e^{2x}+C$.@@$\ln x+C$. Chaque réponse se contrôle par dérivation.'),
e('Reconnaître une composée',1,'',r'Donner une primitive de $2x\mathrm e^{x^2}$.@@Donner une primitive de $2x/(x^2+3)$.@@Donner une primitive de $4x(x^2+1)$.',r'$\mathrm e^{x^2}$.@@$\ln(x^2+3)$, puisque le dénominateur est toujours positif.@@$(x^2+1)^2$, dont la dérivée est $4x(x^2+1)$.'),
e('Condition initiale',1,'',r'Trouver $F$ telle que $F\,\!^{\prime}(x)=2x$ et $F(0)=3$.@@Trouver $G$ telle que $G\,\!^{\prime}(x)=\mathrm e^x$ et $G(1)=0$.@@Pourquoi la constante ne doit-elle pas être oubliée ?',r'$F=x^2+C$ ; $C=3$, donc $F=x^2+3$.@@$G=\mathrm e^x+C$ ; $C=-\mathrm e$, donc $G=\mathrm e^x-\mathrm e$.@@Une même dérivée correspond à toute une famille. La valeur imposée sélectionne un membre précis.'),
e('Vérifier une solution',1,r'$y(t)=4+3\mathrm e^{-2t}$.',r'Calculer $y\,\!^{\prime}$.@@Vérifier $y\,\!^{\prime}=-2y+8$.@@Donner la condition initiale satisfaite.',r'$y\,\!^{\prime}=-6\mathrm e^{-2t}$.@@$-2y+8=-8-6\mathrm e^{-2t}+8=-6\mathrm e^{-2t}$, égal à la dérivée.@@$y(0)=7$.'),
e('Résoudre sans terme constant',2,'',r'Résoudre $y\,\!^{\prime}=3y$, $y(0)=2$.@@Résoudre $z\,\!^{\prime}=-z/2$, $z(0)=10$.@@Donner leurs limites quand $t\to+\infty$.',r'$y(t)=2\mathrm e^{3t}$.@@$z(t)=10\mathrm e^{-t/2}$.@@La première tend vers $+\infty$ ; la seconde vers $0$, car les signes des coefficients exponentiels diffèrent.'),
e('Déplacer un équilibre continu',2,r'$y\,\!^{\prime}=-0{,}5y+6$, $y(0)=2$.',r'Trouver une solution constante.@@Donner la solution du problème.@@Déterminer le temps pour dépasser $11$.',r'$\ell=12$.@@$y(t)=12-10\mathrm e^{-t/2}$.@@$\mathrm e^{-t/2}<0{,}1$ donne $t>2\ln10\simeq4{,}605$ unités de temps.'),
e('Cas $a=0$',2,r'On considère $y\,\!^{\prime}=ay+5$ avec $a=0$ et $y(2)=9$.',r'Pourquoi la formule avec $-b/a$ ne s’applique-t-elle pas ?@@Résoudre directement.@@Vérifier la condition donnée.',r'Elle diviserait par zéro ; l’équation devient simplement $y\,\!^{\prime}=5$.@@$y(t)=5t+C$ ; $9=10+C$, donc $y(t)=5t-1$.@@$y(2)=10-1=9$ et la dérivée est bien $5$.'),
e('Euler à la main',2,r'$y\,\!^{\prime}=-y$, $y(0)=1$. On choisit $h=0{,}5$.',r'Écrire la récurrence d’Euler.@@Calculer les valeurs aux temps $0{,}5$ et $1$.@@Comparer à la solution exacte au temps $1$.',r'$y_{n+1}=y_n-0{,}5y_n=0{,}5y_n$.@@$y_1=0{,}5$, $y_2=0{,}25$.@@La valeur exacte est $\mathrm e^{-1}\simeq0{,}367879$ ; Euler sous-estime d’environ $0{,}117879$.'),
e('Pourquoi une seule constante ?',3,r'$F$ et $G$ sont primitives de la même fonction sur un intervalle $I$.',r'Dériver $F-G$.@@En déduire la forme de $G$.@@Donner un exemple montrant que l’hypothèse d’intervalle est utile.',r'$(F-G)^{\prime}=0$.@@Une dérivée nulle sur un intervalle donne une constante : $G=F+C$.@@Sur $\R\setminus\{0\}$, la fonction égale à $0$ pour $x<0$ et à $1$ pour $x>0$ a une dérivée nulle partout dans son domaine sans être une constante unique.'),
e('Pas trop grand',3,r'Pour $y\,\!^{\prime}=-2y$, $y(0)=1$, Euler donne $y_{n+1}=(1-2h)y_n$.',r'Étudier les valeurs obtenues pour $h=1$.@@Comparer au signe de la solution exacte.@@Que se passe-t-il pour $h=0{,}25$ ?',r'Le facteur vaut $-1$ ; les termes alternent entre $1$ et $-1$.@@La solution exacte $\mathrm e^{-2t}$ reste positive et tend vers $0$. Euler avec ce pas donne un comportement artificiel.@@Le facteur vaut $0{,}5$ ; les termes restent positifs et tendent vers zéro, en cohérence qualitative avec la solution exacte.'),
e('Logistique : vérification guidée',3,r'$y(t)=100/(1+4\mathrm e^{-t})$.',r'Calculer $y(0)$ et sa limite en $+\infty$.@@Vérifier $y\,\!^{\prime}=y(1-y/100)$.@@Pourquoi cette vérification ne constitue-t-elle pas une méthode générale de résolution ?',r'$y(0)=20$ et $y(t)\to100$.@@$y\,\!^{\prime}=400\mathrm e^{-t}/(1+4\mathrm e^{-t})^2$ ; remplacer $y$ dans le second membre donne la même expression.@@On contrôle une fonction déjà fournie. On n’a pas établi comment trouver toutes les solutions de cette équation non linéaire.'),
e('Modèles discret et continu',3,r'Une quantité suit $u_n=50+30(0{,}8)^n$.',r'Trouver $k$ pour que $y(t)=50+30\mathrm e^{-kt}$ coïncide avec $u_n$ aux temps entiers.@@Écrire une équation différentielle satisfaite par $y$.@@Ce modèle continu est-il l’Euler de pas $1$ de cette équation ?',r'$\mathrm e^{-k}=0{,}8$, donc $k=-\ln(0{,}8)$.@@$y\,\!^{\prime}=-k(y-50)$.@@Non : Euler donnerait le coefficient $1-k=1+\ln(0{,}8)\simeq0{,}776856$, différent de $0{,}8$. Coïncidence aux temps entiers et approximation d’Euler sont deux constructions distinctes.')
], 'equadiff'))

CHAPTERS.append(c('Intégrales, aires et valeur moyenne','Analyse et mesure',r'Primitives · Rectangles · Monte-Carlo · Gini',
'Interpréter une intégrale et la calculer avec une primitive.@@Distinguer aire géométrique et aire algébrique.@@Calculer une valeur moyenne et l’interpréter.@@Approcher une aire et déterminer un indice de Gini.',
'Primitives, géométrie plane et convexité.',r'''
\essSection{1}{De l'aire à l'intégrale}
Pour $f$ continue et positive sur $[a,b]$ avec $a<b$, l'intégrale $\int_a^bf(x)\,\mathrm dx$ est l'aire comprise entre la courbe, l'axe horizontal et les droites $x=a,x=b$, exprimée en unités d'aire.
Pour une fonction de signe quelconque, les zones au-dessus de l'axe contribuent positivement et celles au-dessous négativement.
\figurelivre{c07-aires.pdf}{Pour $f(x)=x-1$ sur $[0,3]$, l'intégrale vaut $3/2$, mais l'aire géométrique totale vaut $5/2$. On sépare les deux zones en $x=1$.}
\begin{propriete}[Calcul et relation de Chasles]
Si $F$ est une primitive de $f$, alors $\int_a^bf(x)\,\mathrm dx=F(b)-F(a)$.
La relation de Chasles donne $\int_a^cf=\int_a^bf+\int_b^cf$.
L'intégrale est linéaire : $\int(\lambda f+\mu g)=\lambda\int f+\mu\int g$, avec les mêmes bornes.
\end{propriete}
\essSection{2}{Le lien fondamental avec la dérivée}
\begin{theoreme}[Admis dans le cas général]
Si $f$ est continue sur $[a,b]$, alors $H(x)=\int_a^xf(t)\,\mathrm dt$ est une primitive de $f$ sur l'intervalle. En particulier $H\,\!^{\prime}(x)=f(x)$ et $H(a)=0$.
\end{theoreme}
Pour $f$ croissante et positive, l'aire ajoutée entre $x$ et $x+h$ est comprise entre les rectangles de hauteurs $f(x)$ et $f(x+h)$ lorsque $h>0$.
En divisant par $h$ puis en passant à la limite, la continuité donne $H\,\!^{\prime}(x)=f(x)$. Le même encadrement, avec les inégalités adaptées, vaut à gauche.
Si $f\leq g$ sur $[a,b]$, l'aire entre les courbes vaut $\int_a^b(g-f)$.
\essSection{3}{La valeur moyenne}
\begin{definition}
La valeur moyenne de $f$ sur $[a,b]$ est
$m=\dfrac1{b-a}\int_a^bf(x)\,\mathrm dx$.
Si $m_0\leq f\leq M_0$, alors $m_0\leq m\leq M_0$.
\end{definition}
\begin{exemple}[Débit]
Un débit $d(t)=2t+3$ en litres par minute, pour $0\leq t\leq4$ minutes, fournit
$\int_0^4(2t+3)\,\mathrm dt=[t^2+3t]_0^4=28$ litres.
Le débit moyen vaut $28/4=7$ litres par minute. Ce n'est ni le volume total ni, en général, la moyenne des seules valeurs aux extrémités.
\end{exemple}
\essSection{4}{Approcher une aire}
Avec $n$ intervalles de même largeur $h=(b-a)/n$, la méthode des rectangles à gauche utilise $h\sum_{k=0}^{n-1}f(a+kh)$.
Les rectangles à droite utilisent $k=1,\ldots,n$. Si $f$ est croissante, la première somme minore l'intégrale et la seconde la majore.
La méthode des trapèzes prend la moyenne de ces deux sommes.
\figurelivre{c07-rectangles.pdf}{Rectangles à gauche sous $f(x)=x^2$ sur $[0,1]$, avec $n=6$. Le défaut d'aire diminue quand le pas est réduit.}
\begin{python}
def rectangles(f, a, b, n):
    h = (b-a)/n
    return h*sum(f(a+k*h) for k in range(n))
\end{python}
La méthode de Monte-Carlo tire uniformément des points dans un rectangle contenant la zone. La proportion de points sous la courbe, multipliée par l'aire du rectangle, estime l'aire recherchée. Elle produit une fluctuation aléatoire ; augmenter le nombre de tirages ne garantit pas que chaque nouvelle estimation soit meilleure.
\essSection{5}{Quantifier les inégalités : Gini}
Pour une courbe de Lorenz $L$, l'indice de Gini est le rapport entre l'aire séparant la diagonale de $L$ et l'aire sous la diagonale, égale à $1/2$ :
\[G=1-2\int_0^1L(x)\,\mathrm dx.\]
Pour $L(x)=x^2$, $G=1-2/3=1/3$.
Sur des données groupées, on peut calculer l'aire sous la ligne polygonale par des trapèzes. L'indice décrit la répartition donnée ; il ne mesure pas son niveau moyen, et deux courbes qui se croisent exigent une comparaison prudente.
''',[
e('Calculer avec une primitive',1,'',r'Calculer $\int_0^2 3x^2\,\mathrm dx$.@@Calculer $\int_1^{\mathrm e}1/x\,\mathrm dx$.@@Calculer $\int_0^1\mathrm e^{2x}\,\mathrm dx$.',r'$[x^3]_0^2=8$.@@$[\ln x]_1^{\mathrm e}=1$.@@$[\mathrm e^{2x}/2]_0^1=(\mathrm e^2-1)/2$.'),
e('Chasles et linéarité',1,r'$\int_0^2f=3$ et $\int_2^5f=7$.',r'Calculer $\int_0^5f$.@@Calculer $\int_0^5(2f+1)$.@@Calculer $\int_5^0f$.',r'$3+7=10$.@@$2\times10+(5-0)=25$.@@$-10$, car inverser les bornes change le signe.'),
e('Valeur moyenne',1,'',r'Calculer la moyenne de $x^2$ sur $[0,3]$.@@Comparer à la moyenne des valeurs aux deux bornes.@@La valeur trouvée est-elle comprise entre le minimum et le maximum ?',r'$\frac13[x^3/3]_0^3=3$.@@La moyenne des bornes vaut $(0+9)/2=4{,}5$, différente.@@Oui : $0\leq3\leq9$.'),
e('Une aire signée',1,r'$f(x)=x-2$ sur $[0,4]$.',r'Calculer l’intégrale.@@Calculer l’aire géométrique totale.@@Expliquer l’écart entre les résultats.',r'$[x^2/2-2x]_0^4=0$.@@Deux triangles de base $2$ et hauteur $2$, donc $2+2=4$.@@L’intégrale retranche la zone négative ; les deux zones se compensent. L’aire totale les additionne.'),
e('Entre deux courbes',2,r'$f(x)=x$ et $g(x)=x^2$ sur $[0,1]$.',r'Comparer les deux fonctions.@@Calculer l’aire entre leurs courbes.@@Donner les points d’intersection.',r'$x-x^2=x(1-x)\geq0$, donc $f\geq g$.@@$\int_0^1(x-x^2)\,\mathrm dx=1/2-1/3=1/6$.@@$x=x^2$ donne $x=0$ et $x=1$, soit $(0,0)$ et $(1,1)$.'),
e('Production cumulée',2,r'Un débit vaut $d(t)=6\mathrm e^{-t/2}$ litres par minute pendant les quatre premières minutes.',r'Calculer le volume total.@@Calculer le débit moyen.@@Encadrer cette moyenne par les valeurs minimale et maximale du débit.',r'$[-12\mathrm e^{-t/2}]_0^4=12(1-\mathrm e^{-2})\simeq10{,}376$ litres.@@$3(1-\mathrm e^{-2})\simeq2{,}594$ L/min.@@Le débit décroît de $6$ à $6\mathrm e^{-2}\simeq0{,}812$ ; la moyenne est bien entre ces bornes.'),
e('Rectangles',2,r'On approche $\int_0^1x^2\,\mathrm dx$ avec quatre intervalles.',r'Calculer la somme à gauche.@@Calculer celle à droite et la valeur par trapèzes.@@Comparer à l’intégrale exacte.',r'$\frac14(0+1/16+1/4+9/16)=7/32=0{,}21875$.@@À droite : $15/32=0{,}46875$ ; trapèzes : $11/32=0{,}34375$.@@L’exact vaut $1/3$. Les rectangles l’encadrent ; les trapèzes le surestiment ici de $1/96$.'),
e('Lorenz et Gini',2,r'$L(x)=x^3$ sur $[0,1]$.',r'Calculer la part détenue par les $50\,\%$ les moins riches.@@Calculer l’indice de Gini.@@Comparer au modèle $L(x)=x^2$.',r'$L(1/2)=1/8=12{,}5\,\%$.@@$G=1-2[x^4/4]_0^1=1/2$.@@Pour $x^2$, $G=1/3$. Le modèle $x^3$ présente ici davantage d’inégalités, ce qui concorde avec l’ordre des courbes.'),
e('Une estimation aléatoire',3,r'On tire $N=10\,000$ points uniformes dans $[0,1]^2$ ; $3\,340$ sont sous $y=x^2$.',r'Donner l’estimation de l’aire.@@Comparer à l’aire exacte.@@Le résultat prouve-t-il l’égalité avec $1/3$ ?',r'$3\,340/10\,000=0{,}334$.@@L’exact est $1/3\simeq0{,}333333$ ; l’erreur absolue observée est environ $0{,}000667$.@@Non. Une simulation fournit une estimation fluctuante ; la preuve exacte utilise ici une primitive.'),
e('Données groupées',3,r'Une ligne de Lorenz passe par $(0,0)$, $(0{,}5,0{,}2)$ et $(1,1)$.',r'Calculer l’aire sous la ligne polygonale.@@Calculer son indice de Gini.@@Pourquoi ne peut-on déduire tous les revenus individuels de ces trois points ?',r'Premier trapèze : $0{,}5(0+0{,}2)/2=0{,}05$ ; second : $0{,}5(0{,}2+1)/2=0{,}30$. Total $0{,}35$.@@$G=1-2(0{,}35)=0{,}30$.@@Les parts cumulées de deux groupes ne déterminent pas la répartition interne à chaque groupe ; la ligne polygonale est une représentation groupée.'),
e('Primitive définie par une aire',3,r'$H(x)=\int_1^x(t^2+1)\,\mathrm dt$.',r'Donner $H(1)$ et $H\,\!^{\prime}(x)$.@@Déterminer une expression explicite de $H$.@@Étudier les variations de $H$.',r'$H(1)=0$ et $H\,\!^{\prime}(x)=x^2+1$ par le théorème fondamental.@@$H(x)=x^3/3+x-4/3$.@@La dérivée est strictement positive sur $\R$ ; $H$ est strictement croissante.'),
e('Encadrer sans primitive',3,r'On veut approcher $I=\int_0^1\mathrm e^{-x^2}\,\mathrm dx$, sans chercher de primitive usuelle.',r'Déterminer le sens de variation de l’intégrande.@@Dire quelle somme de rectangles minore et quelle somme majore $I$.@@Majorer la différence entre ces sommes avec $n$ subdivisions égales ; choisir $n$ pour une largeur au plus $0{,}001$.',r'La dérivée $-2x\mathrm e^{-x^2}$ est négative ou nulle sur $[0,1]$ ; la fonction décroît.@@Les rectangles à droite minorent ; ceux à gauche majorent.@@La différence télescopique vaut $(1-\mathrm e^{-1})/n$. Il suffit de $n\geq633$, car $1-\mathrm e^{-1}\simeq0{,}632121$.')
], 'integrale'))

CHAPTERS.append(c('Probabilités conditionnelles et Bayes','Probabilités et décision',r'Arbres · Fréquences · Conditionnement · Prévalence',
'Traduire un énoncé avec un arbre ou un tableau.@@Calculer une probabilité totale.@@Inverser un conditionnement avec la formule de Bayes.@@Interpréter sensibilité, spécificité et valeurs prédictives.',
'Événements, intersection, réunion et probabilités de Première.',r'''
\essSection{1}{Changer l'univers de référence}
\begin{definition}
Si $P(A)>0$, la probabilité de $B$ sachant $A$ est $P_A(B)=P(A\cap B)/P(A)$.
Ainsi $P(A\cap B)=P(A)P_A(B)$.
Les événements $A$ et $B$ sont indépendants si $P(A\cap B)=P(A)P(B)$.
\end{definition}
Conditionner consiste à se restreindre aux cas où l'information est réalisée. Il ne s'agit pas simplement de multiplier deux probabilités quelconques.
Dans un arbre, les poids issus d'un même nœud totalisent $1$. Un chemin se calcule par produit ; des chemins incompatibles se réunissent par addition.
\figurelivre{c08-bayes.pdf}{Arbre d'un test fictif : $M$ désigne la présence d'une caractéristique et $+$ un résultat positif. Les fréquences à droite sont les effectifs théoriques pour $10\,000$ personnes.}
\essSection{2}{La formule des probabilités totales}
\begin{propriete}
Si $A$ et $\bar A$ ont des probabilités non nulles,
\[P(B)=P(A)P_A(B)+P(\bar A)P_{\bar A}(B).\]
Plus généralement, on additionne sur une partition de l'univers : des événements incompatibles dont la réunion est l'univers.
\end{propriete}
Un tableau d'effectifs permet souvent de vérifier les calculs de l'arbre. Les probabilités conditionnelles se lisent en divisant par le total du groupe conditionnant, pas toujours par le total général.
\essSection{3}{Inverser avec Bayes}
\begin{theoreme}[Formule de Bayes]
Pour $P(B)>0$,
\[P_B(A)=\frac{P(A)P_A(B)}{P(B)}.
\]
La probabilité $P(A)$ est dite a priori ; $P_B(A)$ est la probabilité a posteriori après observation de $B$.
\end{theoreme}
Cette formule découle directement des deux expressions de $P(A\cap B)$.
\begin{exemple}[Un test fictif]
On donne $P(M)=0{,}02$, $P_M(+)=0{,}95$ et $P_{\bar M}(+)=0{,}05$.
Alors $P(+)=0{,}02\times0{,}95+0{,}98\times0{,}05=0{,}068$.
Ainsi $P_+(M)=0{,}019/0{,}068=19/68\simeq27{,}94\,\%$.
Sur $10\,000$ personnes, on attend $190$ vrais positifs et $490$ faux positifs. Parmi les $680$ résultats positifs, $190$ concernent $M$.
\end{exemple}
\essSection{4}{Nommer les quatre groupes}
La sensibilité est $s=P_M(+)$ ; la spécificité est $c=P_{\bar M}(-)$.
La valeur prédictive positive est $P_+(M)$ ; la valeur prédictive négative est $P_-(\bar M)$.
Les vrais positifs sont $M\cap+$, les faux positifs $\bar M\cap+$ ; les faux négatifs $M\cap-$ et les vrais négatifs $\bar M\cap-$.
\begin{attention}
Une sensibilité de $95\,\%$ ne signifie pas qu'une personne ayant un test positif a $95\,\%$ de probabilité de posséder la caractéristique.
Les modèles de dépistage du manuel servent uniquement à apprendre le raisonnement probabiliste ; les données sont fictives.
\end{attention}
\essSection{5}{L'effet de la proportion initiale}
Si $p=P(M)$ et si $s,c$ sont fixés, la valeur prédictive positive vaut
\[V(p)=\frac{sp}{sp+(1-c)(1-p)}.\]
Lorsque $s>0$ et $1-c>0$, elle augmente avec $p$. Pour une caractéristique rare, des faux positifs peu fréquents peuvent être nombreux parmi tous les résultats positifs.
Deux tests successifs ne peuvent être traités comme indépendants sans hypothèse. Une indépendance conditionnelle sachant $M$, et une autre sachant $\bar M$, doivent être explicitement annoncées avant de multiplier leurs probabilités.
''',[
e('Lire un conditionnement',1,r'$P(A)=0{,}4$ et $P_A(B)=0{,}7$.',r'Calculer $P(A\cap B)$.@@Calculer $P_A(\bar B)$.@@Peut-on déjà calculer $P(B)$ ?',r'$0{,}4\times0{,}7=0{,}28$.@@$1-0{,}7=0{,}3$.@@Non : il manque la probabilité de $B$ dans le groupe $\bar A$, ou une information équivalente.'),
e('Compléter un arbre',1,r'$P(A)=0{,}3$, $P_A(B)=0{,}8$ et $P_{\bar A}(B)=0{,}2$.',r'Donner les trois poids complémentaires.@@Calculer $P(B)$.@@Calculer $P(B\cap\bar A)$.',r'$P(\bar A)=0{,}7$, $P_A(\bar B)=0{,}2$, $P_{\bar A}(\bar B)=0{,}8$.@@$0{,}3\times0{,}8+0{,}7\times0{,}2=0{,}38$.@@$0{,}7\times0{,}2=0{,}14$.'),
e('Indépendance',1,r'$P(A)=0{,}5$, $P(B)=0{,}4$ et $P(A\cap B)=0{,}2$.',r'Les événements sont-ils indépendants ?@@Calculer $P_A(B)$.@@Sont-ils incompatibles ?',r'Oui : $0{,}2=0{,}5\times0{,}4$.@@$0{,}2/0{,}5=0{,}4=P(B)$.@@Non : leur intersection a une probabilité positive. Indépendance et incompatibilité sont deux notions différentes.'),
e('Deux urnes',1,r'On choisit une urne $U$ avec probabilité $1/3$, sinon $V$. $U$ contient $3$ boules rouges sur $4$ ; $V$ en contient $1$ sur $4$.',r'Calculer $P(R)$.@@Calculer $P_R(U)$.@@Comparer $P_R(U)$ à $P(U)$.',r'$\frac13\frac34+\frac23\frac14=5/12$.@@$P_R(U)=(1/4)/(5/12)=3/5$.@@$3/5>1/3$ : observer une boule rouge rend l’urne $U$ plus probable.'),
e('Production et défauts',2,r'Une machine $A$ produit $60\,\%$ des pièces, avec $2\,\%$ de défauts ; $B$ produit le reste, avec $5\,\%$ de défauts.',r'Calculer le taux global de défaut.@@Une pièce est défectueuse : calculer la probabilité qu’elle vienne de $B$.@@Pourquoi la moyenne simple de $2\,\%$ et $5\,\%$ serait-elle incorrecte ?',r'$0{,}6\times0{,}02+0{,}4\times0{,}05=0{,}032$, soit $3{,}2\,\%$.@@$0{,}4\times0{,}05/0{,}032=5/8=62{,}5\,\%$.@@Les deux machines n’ont pas le même poids dans la production ; il faut une moyenne pondérée.'),
e('Un tableau de test',2,r'Sur $1\,000$ personnes fictives, $50$ possèdent $M$. Parmi elles, $45$ ont un résultat positif. Parmi les autres, $19$ ont un résultat positif.',r'Donner sensibilité et spécificité.@@Calculer la valeur prédictive positive.@@Calculer la valeur prédictive négative.',r'$s=45/50=0{,}9$ ; $c=931/950=0{,}98$.@@$45/(45+19)=45/64\simeq70{,}31\,\%$.@@$931/(931+5)=931/936\simeq99{,}47\,\%$.'),
e('Trois origines',2,r'Trois ateliers ont les parts $0{,}2$, $0{,}3$, $0{,}5$ et les taux de défaut $0{,}01$, $0{,}02$, $0{,}04$.',r'Calculer la probabilité d’un défaut.@@Calculer la part du troisième atelier parmi les pièces défectueuses.@@Vérifier que les trois probabilités a posteriori totalisent $1$.',r'$0{,}002+0{,}006+0{,}020=0{,}028$.@@$0{,}020/0{,}028=5/7$.@@Elles valent $1/14$, $3/14$ et $10/14$ ; leur somme vaut $1$.'),
e('Retrouver une proportion',2,r'$P_A(B)=0{,}8$, $P_{\bar A}(B)=0{,}2$ et $P(B)=0{,}35$.',r'Poser $p=P(A)$ et écrire l’équation.@@Déterminer $p$.@@Calculer $P_B(A)$.',r'$0{,}35=0{,}8p+0{,}2(1-p)$.@@$0{,}15=0{,}6p$, donc $p=1/4$.@@$0{,}8\times0{,}25/0{,}35=4/7\simeq57{,}14\,\%$.'),
e('Prévalence et valeur prédictive',3,r'Un test fictif a $s=0{,}9$ et $c=0{,}95$.',r'Exprimer $V(p)$.@@Déterminer les $p$ pour lesquels $V(p)>1/2$.@@Interpréter sans confondre les deux conditionnements.',r'$V(p)=0{,}9p/(0{,}85p+0{,}05)$.@@Le dénominateur est positif : $1{,}8p>0{,}85p+0{,}05$, donc $p>1/19\simeq5{,}26\,\%$.@@La fiabilité d’un résultat positif dépend de la proportion initiale de $M$, même si la sensibilité du test reste $90\,\%$.'),
e('Deux résultats positifs',3,r'$P(M)=0{,}1$, $P_M(+)=0{,}9$, $P_{\bar M}(+)=0{,}1$. On suppose deux répétitions indépendantes conditionnellement à chacun des deux groupes.',r'Calculer la probabilité de deux positifs sachant chaque groupe.@@Calculer la probabilité de $M$ sachant deux positifs.@@Que faudrait-il revoir si les erreurs des répétitions étaient liées ?',r'$0{,}9^2=0{,}81$ sachant $M$ ; $0{,}1^2=0{,}01$ sachant $\bar M$.@@$0{,}1\times0{,}81/(0{,}081+0{,}009)=0{,}9$.@@Les produits conditionnels $0{,}9^2$ et $0{,}1^2$ ne seraient plus justifiés ; il faudrait les probabilités conjointes des deux résultats.'),
e('L’erreur de l’inversion',3,r'Un élève affirme : « $P_A(B)=0{,}8$, donc $P_B(A)=0{,}8$. »',r'Construire un contre-exemple avec $P(A)=0{,}1$ et $P_{\bar A}(B)=0{,}2$.@@Calculer les deux probabilités.@@Formuler la règle correcte.',r'On peut construire un arbre avec ces trois poids ; tous sont entre $0$ et $1$.@@$P(B)=0{,}08+0{,}18=0{,}26$ ; $P_B(A)=0{,}08/0{,}26=4/13\simeq0{,}3077$, tandis que $P_A(B)=0{,}8$.@@Il faut utiliser Bayes et le taux a priori. Inverser les lettres sans recalcul n’est pas une règle.'),
e('Une preuve de croissance',3,r'$V(p)=sp/(sp+f(1-p))$ avec $s>0,f>0$ et $0\leq p\leq1$.',r'Calculer la dérivée.@@En déduire le sens de variation.@@Donner les valeurs aux bornes et une conclusion.',r'Le dénominateur est $f+(s-f)p$ ; la règle du quotient donne $V\,\!^{\prime}(p)=sf/[f+(s-f)p]^2$.@@Elle est strictement positive, donc $V$ est strictement croissante.@@$V(0)=0$ et $V(1)=1$ : à performances conditionnelles fixées, la valeur prédictive dépend fortement de la proportion initiale.')
], 'conditionnelles'))

CHAPTERS.append(c('Lois discrètes et loi binomiale','Probabilités et répétitions',r'Uniforme · Bernoulli · Pascal · Espérance',
'Identifier une loi uniforme, de Bernoulli ou binomiale.@@Construire et utiliser le triangle de Pascal.@@Calculer des probabilités exactes et cumulées.@@Interpréter espérance, variance et écart type.',
'Probabilités, indépendance et sommes.',r'''
\essSection{1}{Décrire une variable aléatoire discrète}
Une variable aléatoire associe un nombre à chaque issue. Sa loi indique les valeurs possibles et leurs probabilités ; ces dernières sont positives ou nulles et leur somme vaut $1$.
Son espérance est $E(X)=\sum x_iP(X=x_i)$, sa variance $V(X)=\sum(x_i-E(X))^2P(X=x_i)$ et son écart type $\sigma(X)=\sqrt{V(X)}$.
L'espérance est une moyenne théorique ; elle n'est pas nécessairement une valeur possible de $X$.
\begin{definition}[Deux lois élémentaires]
Uniforme sur $\{1,\ldots,n\}$ : chaque valeur a probabilité $1/n$ et $E(X)=(n+1)/2$.
Bernoulli de paramètre $p$ : $P(X=1)=p$, $P(X=0)=1-p$ ;
$E(X)=p$, $V(X)=p(1-p)$ et $\sigma(X)=\sqrt{p(1-p)}$.
\end{definition}
Pour l'uniforme, l'espérance vaut $(1+\cdots+n)/n=(n+1)/2$.
Pour Bernoulli, $E(X)=p$ et $E(X^2)=p$, d'où $V(X)=p-p^2$.
\essSection{2}{Répéter indépendamment}
Un schéma de Bernoulli répète $n$ fois la même épreuve, indépendamment, avec la même probabilité $p$ de succès. Le nombre de succès suit la loi binomiale $\mathcal B(n,p)$.
Un tirage sans remise dans une petite population ne satisfait généralement pas ces hypothèses : le paramètre change au cours des tirages.
\figurelivre{c09-bernoulli.pdf}{Un arbre à trois répétitions. Chaque chemin contenant deux succès et un échec porte la probabilité $p^2(1-p)$ ; il y a trois chemins de ce type.}
\essSection{3}{Compter les chemins : Pascal}
Le coefficient $\binom nk$ compte les façons de placer $k$ succès parmi $n$ répétitions. Il vérifie $\binom n0=\binom nn=1$, $\binom nk=\binom n{n-k}$ et
$\binom{n+1}k=\binom n{k-1}+\binom nk$.
\begin{center}\begin{tabular}{c|rrrrrr}$n$&&&&&&\\\hline
0&1\\1&1&1\\2&1&2&1\\3&1&3&3&1\\4&1&4&6&4&1\\5&1&5&10&10&5&1\end{tabular}\end{center}
Chaque coefficient intérieur s'obtient en additionnant les deux coefficients immédiatement au-dessus. La formule avec les factorielles, $\binom nk=n!/[k!(n-k)!]$, est un outil possible, pas un substitut au sens du coefficient.
\essSection{4}{La formule binomiale}
\begin{propriete}[Résultats d'espérance et d'écart type admis]
Si $X\sim\mathcal B(n,p)$, alors, pour $0\leq k\leq n$,
\[P(X=k)=\binom nkp^k(1-p)^{n-k},\quad E(X)=np,\quad V(X)=np(1-p).\]
\end{propriete}
Pour $n=2$, la loi est $(1-p)^2,2p(1-p),p^2$. Son espérance est $2p(1-p)+2p^2=2p$, ce qui illustre la formule générale.
\begin{exemple}
Pour $X\sim\mathcal B(5,0{,}2)$,
$P(X=2)=10\times0{,}2^2\times0{,}8^3=0{,}2048$.
$P(X\geq1)=1-P(X=0)=1-0{,}8^5=0{,}67232$.
\end{exemple}
\figurelivre{c09-binomiale.pdf}{Diagramme des probabilités pour $\mathcal B(10,0{,}3)$. L'espérance vaut $3$ et l'écart type $\sqrt{2{,}1}$ ; le diagramme représente des masses, pas une densité continue.}
\essSection{5}{Calculatrice, logiciel et notation des événements}
Pour une variable entière, $P(X<k)=P(X\leq k-1)$ et $P(X\geq k)=1-P(X\leq k-1)$.
On peut calculer une probabilité cumulée en additionnant les masses :
\begin{python}
from math import comb
def binom_cumul(n, p, k):
    return sum(comb(n, j)*p**j*(1-p)**(n-j)
               for j in range(k+1))
\end{python}
Cette fonction est utilisée pour $n\in\N$, $0\leq p\leq1$, $0\leq k\leq n$. Au chapitre suivant, les cumuls permettront de construire des intervalles de fluctuation.
''',[
e('Uniforme discrète',1,r'On lance un dé équilibré à six faces numérotées de $1$ à $6$.',r'Donner la loi de $X$, le résultat.@@Calculer $E(X)$.@@Calculer $P(X\geq5)$.',r'$X$ suit la loi uniforme sur $\{1,2,3,4,5,6\}$ ; chaque probabilité vaut $1/6$.@@$(6+1)/2=3{,}5$.@@$2/6=1/3$, car les issues $5$ et $6$ conviennent.'),
e('Bernoulli',1,r'$P(X=1)=0{,}3$ et $P(X=0)=0{,}7$.',r'Identifier la loi.@@Calculer l’espérance et la variance.@@Calculer l’écart type à $10^{-3}$ près.',r'Bernoulli de paramètre $0{,}3$.@@$E(X)=0{,}3$ et $V(X)=0{,}3\times0{,}7=0{,}21$.@@$\sqrt{0{,}21}\simeq0{,}458$.'),
e('Pascal',1,'',r'Écrire la ligne $n=4$.@@En déduire $\binom52$.@@Utiliser la symétrie pour donner $\binom53$.',r'$1,4,6,4,1$.@@$\binom52=4+6=10$.@@$\binom53=\binom52=10$.'),
e('Identifier le modèle',1,'',r'Dix lancers indépendants d’une pièce équilibrée : quelle loi pour le nombre de piles ?@@Trois tirages sans remise dans une urne de cinq boules : pourquoi la binomiale ne s’applique-t-elle pas automatiquement ?@@Quel est le paramètre $n$ si l’on répète vingt fois une expérience ?',r'$\mathcal B(10,1/2)$, car les répétitions sont indépendantes et de même paramètre.@@La composition de l’urne change, donc les probabilités conditionnelles changent et l’indépendance manque.@@$n=20$ : il compte les répétitions, pas la probabilité du succès.'),
e('Une loi complète',2,r'$X\sim\mathcal B(3,1/2)$.',r'Donner toutes les probabilités.@@Calculer $P(X\geq2)$.@@Calculer l’espérance directement à partir de la loi.',r'Pour $k=0,1,2,3$, les probabilités sont $1/8,3/8,3/8,1/8$.@@$3/8+1/8=1/2$.@@$0+3/8+6/8+3/8=12/8=3/2=np$.'),
e('Au moins un défaut',2,r'Les pièces sont supposées indépendantes, chacune défectueuse avec probabilité $0{,}02$. On en prélève $20$.',r'Donner la loi du nombre de défauts.@@Calculer la probabilité d’au moins un défaut.@@Interpréter l’espérance.',r'$X\sim\mathcal B(20,0{,}02)$.@@$1-0{,}98^{20}\simeq0{,}332392$.@@$E(X)=0{,}4$ défaut par lot en moyenne théorique sur de nombreux lots ; ce n’est pas un nombre de défauts réalisable dans un lot.'),
e('Cumuler',2,r'$X\sim\mathcal B(4,0{,}2)$.',r'Calculer $P(X=0)$ et $P(X=1)$.@@Calculer $P(X\leq1)$.@@Calculer $P(X\geq2)$.',r'$0{,}8^4=0{,}4096$ et $4(0{,}2)(0{,}8)^3=0{,}4096$.@@$0{,}8192$.@@$1-0{,}8192=0{,}1808$.'),
e('Choisir une taille',2,r'Chaque tentative indépendante réussit avec probabilité $0{,}1$.',r'Exprimer la probabilité d’au moins un succès en $n$ tentatives.@@Déterminer le plus petit $n$ donnant une probabilité au moins $0{,}95$.@@Expliquer pourquoi on ne peut additionner $n$ fois $0{,}1$.',r'$1-0{,}9^n$.@@$0{,}9^n\leq0{,}05$, donc $n\geq\ln(0{,}05)/\ln(0{,}9)\simeq28{,}433$ ; il faut $29$ tentatives.@@Les succès peuvent se produire ensemble ; les événements ne sont pas incompatibles. L’addition naïve donnerait même des valeurs supérieures à $1$.'),
e('Gagner ou perdre',3,r'Un jeu coûte $2$ euros. Une réussite de probabilité $0{,}3$ rapporte $5$ euros, sinon rien.',r'Exprimer le gain net à l’aide d’une Bernoulli $X$.@@Calculer le gain moyen.@@Sur $100$ parties indépendantes, donner l’espérance du gain net total.',r'$G=5X-2$ : gain $3$ en cas de succès, perte $2$ sinon.@@$E(G)=5(0{,}3)-2=-0{,}5$ euro.@@Le nombre de réussites $S$ suit $\mathcal B(100,0{,}3)$ ; $E(5S-200)=150-200=-50$ euros.'),
e('Prouver la symétrie',3,'',r'Expliquer pourquoi choisir les $k$ places de succès détermine les $n-k$ places d’échec.@@En déduire $\binom nk=\binom n{n-k}$.@@Les probabilités $P(X=k)$ et $P(X=n-k)$ sont-elles toujours égales ?',r'Les places d’échec sont exactement le complément des places de succès. Le choix est bijectif.@@Les deux ensembles de choix ont donc le même nombre d’éléments.@@Non : les facteurs $p^k(1-p)^{n-k}$ et $p^{n-k}(1-p)^k$ diffèrent généralement. La symétrie des masses est assurée pour $p=1/2$.'),
e('Un paramètre inconnu',3,r'$X\sim\mathcal B(12,p)$ et $E(X)=3$.',r'Déterminer $p$.@@Calculer l’écart type.@@Calculer la probabilité de zéro succès.',r'$12p=3$, donc $p=1/4$.@@$\sigma=\sqrt{12(1/4)(3/4)}=3/2$.@@$P(X=0)=(3/4)^{12}\simeq0{,}031676$.'),
e('Détecter un faux modèle',3,r'Une boîte contient exactement deux produits défectueux et huit corrects. On en tire trois sans remise.',r'Pourquoi $\mathcal B(3,0{,}2)$ serait-elle un modèle inexact ?@@Calculer la probabilité que les trois soient corrects par un arbre.@@Comparer à $0{,}8^3$.',r'Les tirages ne sont pas indépendants ; après un tirage correct, la proportion de défauts change.@@$(8/10)(7/9)(6/8)=7/15\simeq0{,}466667$.@@$0{,}8^3=0{,}512$ est différent. Une approximation ne doit pas être présentée comme un calcul exact sans justification.')
], 'binomiale'))

CHAPTERS.append(c('Échantillonnage et décision statistique','Probabilités et inférence',r'Fluctuation · Intervalles · Simulation · Biais',
'Distinguer proportion théorique et fréquence observée.@@Construire un intervalle binomial de probabilité prescrite.@@Conduire une décision sous une hypothèse annoncée.@@Simuler des échantillons et discuter les biais.',
'Loi binomiale, probabilités cumulées et listes Python.',r'''
\essSection{1}{Une fréquence change d'un échantillon à l'autre}
On suppose des observations indépendantes de même probabilité $p$. Si $X$ compte les succès sur $n$ observations, $X\sim\mathcal B(n,p)$ et la fréquence est $F=X/n$.
\[E(F)=p,\qquad \sigma(F)=\sqrt{\frac{p(1-p)}n}.\]
Ces formules décrivent le modèle. La fréquence observée $f$ est une valeur réalisée, et ne devient pas automatiquement égale à $p$.
\figurelivre{c10-fluctuation.pdf}{Distributions théoriques des fréquences pour une pièce équilibrée, à $n=20$ puis $n=100$. Les fréquences se concentrent davantage autour de $1/2$ quand la taille augmente.}
\essSection{2}{Construire un intervalle garanti dans le modèle}
\begin{savoirfaire}[Procédure exacte binomiale]
Sous une hypothèse $p=p_0$, choisir des entiers $a,b$ tels que
$P(a\leq X\leq b)\geq1-\alpha$.
Pour une construction centrale, prendre la plus grande borne basse compatible avec $P(X<a)\leq\alpha/2$, et la plus petite borne haute compatible avec $P(X>b)\leq\alpha/2$.
L'intervalle des fréquences est $[a/n,b/n]$.
\end{savoirfaire}
La loi étant discrète, la probabilité obtenue dépasse souvent le niveau demandé. Les bornes ne sont pas uniques ; annoncer la règle de construction permet de reproduire le résultat.
Pour $X\sim\mathcal B(10,1/2)$, $P(2\leq X\leq8)=1-22/1024=0{,}978515625$.
Le complément a donc une probabilité inférieure à $0{,}05$.
\essSection{3}{Décider sans prétendre prouver une hypothèse}
Sous l'hypothèse d'une pièce équilibrée, observer un résultat dans une zone très peu probable peut conduire à remettre cette hypothèse en cause.
\begin{attention}
Une décision de rejet peut être erronée : un événement rare peut se produire. Une observation dans l'intervalle ne prouve pas que l'hypothèse est vraie ; elle ne la contredit pas selon la règle choisie.
Le risque $\alpha$ concerne la procédure sous l'hypothèse, pas la probabilité que l'hypothèse soit vraie après les données.
\end{attention}
Pour une surréservation, on cherche plutôt une borne unilatérale $k$ telle que $P(X\leq k)\geq1-\alpha$ : le risque de dépasser la capacité $k$ est alors au plus $\alpha$ dans le modèle.
\essSection{4}{Simuler des échantillons}
\begin{python}
from random import Random
def frequences(n, p, repetitions, graine=2026):
    rng = Random(graine)
    resultats = []
    for j in range(repetitions):
        succes = sum(rng.random() < p for k in range(n))
        resultats.append(succes/n)
    return resultats
\end{python}
Le générateur produit des valeurs dans $[0,1[$ ; le test \code{random() < p} simule une Bernoulli de paramètre $p$. Une graine fixe rend l'expérience reproductible.
Pour une variable d'espérance $\mu$ et d'écart type $\sigma$, on peut simuler des moyennes d'échantillons indépendants, puis comparer leur dispersion à $\sigma/\sqrt n$.
Dans une série de $R$ moyennes $m_j$, l'écart type descriptif est $s=\sqrt{\sum(m_j-\bar m)^2/R}$.
Comparer les proportions vérifiant $|m_j-\mu|\leq2\sigma/\sqrt n$ ou $3\sigma/\sqrt n$ explore la concentration. Il ne faut pas annoncer des pourcentages universels à partir de ces seuls seuils.
\essSection{5}{Du modèle à un vrai sondage}
Une grande taille réduit la fluctuation aléatoire dans un modèle pertinent ; elle ne corrige pas un biais de sélection ou de réponse.
Une consultation volontaire en ligne n'est pas automatiquement un échantillon aléatoire représentatif.
Une estimation de proportion peut utiliser $\hat p=f$, mais une « fourchette » doit préciser sa construction et ses hypothèses.
Inverser des tests pour tous les $p$ possibles fournit un ensemble de valeurs compatibles : la construction d'un intervalle de confiance ne se confond pas avec la simple substitution de $f$ dans une formule de fluctuation.
''',[
e('Fréquence et proportion',1,r'$X\sim\mathcal B(100,0{,}4)$ et $F=X/100$.',r'Calculer $E(X)$ puis $E(F)$.@@Calculer $\sigma(F)$.@@Si l’on observe $X=45$, donner la fréquence et dire si elle est égale à $p$.',r'$E(X)=40$ et $E(F)=0{,}4$.@@$\sqrt{0{,}4\times0{,}6/100}\simeq0{,}04899$.@@$f=0{,}45$, différente de $0{,}4$ ; cette différence peut résulter de la fluctuation.'),
e('Effet de la taille',1,'',r'Par quel facteur l’écart type d’une fréquence est-il divisé si la taille est multipliée par $4$ ?@@Et si elle est multipliée par $100$ ?@@Cela supprime-t-il un biais de sélection ?',r'Par $\sqrt4=2$.@@Par $\sqrt{100}=10$.@@Non : la formule traite la fluctuation dans un modèle d’échantillonnage, pas une erreur systématique de recrutement.'),
e('Intervalle exact simple',1,r'$X\sim\mathcal B(4,1/2)$.',r'Calculer $P(1\leq X\leq3)$.@@Cette probabilité atteint-elle $0{,}95$ ?@@Quel intervalle entier atteint au moins $0{,}95$ ?',r'$1-2(1/16)=7/8=0{,}875$.@@Non : $0{,}875<0{,}95$.@@Il faut ici inclure les deux extrêmes pour dépasser $0{,}95$ ; $[0,4]$ a probabilité $1$.'),
e('Complément',1,r'Un intervalle $I$ vérifie $P(X\in I)=0{,}96$.',r'Calculer la probabilité du complément.@@Le complément a-t-il une probabilité inférieure à $0{,}05$ ?@@Une observation hors de $I$ est-elle impossible ?',r'$1-0{,}96=0{,}04$.@@Oui, $0{,}04<0{,}05$.@@Non : rare ne signifie pas impossible.'),
e('Tester une pièce',2,r'Sous l’hypothèse d’une pièce équilibrée, $X\sim\mathcal B(10,1/2)$. On retient $I=[2,8]$.',r'Calculer la probabilité hors de $I$.@@On observe neuf piles : quelle décision suit cette règle ?@@On observe six piles : que peut-on conclure ?',r'$P(X\leq1)+P(X\geq9)=2(1+10)/1024=22/1024\simeq0{,}021484$.@@$9\notin I$ : on rejette l’hypothèse selon cette règle.@@$6\in I$ : on ne rejette pas. Cela ne prouve pas que la pièce est équilibrée.'),
e('Une borne de capacité',2,r'Quatre clients viennent indépendamment avec probabilité $0{,}8$. $X$ est le nombre de présents.',r'Calculer $P(X\leq2)$.@@Calculer $P(X\leq3)$.@@Pour un risque de dépassement au plus $0{,}5$, quelle est la plus petite capacité entière ?',r'$0{,}2^4+4(0{,}8)(0{,}2)^3+6(0{,}8)^2(0{,}2)^2=0{,}1808$.@@$1-0{,}8^4=0{,}5904$.@@Il faut un cumul au moins $0{,}5$ : la plus petite capacité est $3$, puisque le cumul en $2$ est inférieur.'),
e('Simulation reproductible',2,'',r'Expliquer le rôle de la graine dans le programme du cours.@@Pourquoi calcule-t-on \code{succes/n} ?@@Que représente la liste des résultats ?',r'Elle initialise un générateur pseudo-aléatoire ; la même graine reproduit la même suite de tirages avec la même implémentation.@@On convertit le nombre de succès en fréquence observée.@@Une fréquence par échantillon ; sa dispersion illustre la fluctuation d’échantillonnage.'),
e('Sondage biaisé',2,r'Un site propose une question à ses visiteurs ; $50\,000$ répondent volontairement.',r'La grande taille garantit-elle la représentativité ?@@Citer deux biais possibles.@@Quelle différence ferait un tirage aléatoire correctement organisé ?',r'Non : la taille ne suffit pas à assurer la qualité du recrutement.@@Les visiteurs ne représentent pas nécessairement la population visée ; les personnes motivées répondent davantage. Le libellé peut aussi influencer les réponses.@@Un plan de sondage aléatoire maîtrisé permet de modéliser le recrutement ; il faut encore traiter les non-réponses et la qualité de mesure.'),
e('Deux types de risque',3,r'Une procédure rejette une hypothèse lorsque $X$ sort d’une zone contenant au moins $95\,\%$ de probabilité sous cette hypothèse.',r'Quel risque est majoré par $5\,\%$ ?@@Peut-on dire que l’hypothèse a $95\,\%$ de chances d’être vraie si l’observation reste dans la zone ?@@Pourquoi le non-rejet peut-il aussi être trompeur ?',r'Le risque de rejeter l’hypothèse alors qu’elle est vraie, dans le modèle annoncé.@@Non : la probabilité de l’hypothèse après observation n’est pas fournie par cette procédure.@@Une autre valeur du paramètre peut produire une observation compatible avec la zone ; le test peut manquer de puissance pour la distinguer.'),
e('Moyennes d’un dé',3,r'On simule des moyennes de $n=100$ lancers indépendants d’un dé équilibré. On donne $\mu=3{,}5$ et $\sigma=\sqrt{35/12}$.',r'Calculer l’écart type théorique des moyennes.@@Donner le seuil $2\sigma/\sqrt n$.@@Comment mesurer la proportion de moyennes à une distance au plus ce seuil de $\mu$ ?',r'$\sqrt{35/12}/10\simeq0{,}170783$.@@$0{,}341565$ environ.@@Pour chaque moyenne $m$, tester $|m-3{,}5|\leq0{,}341565$ ; compter les succès puis diviser par le nombre de moyennes simulées. On conserve davantage de chiffres dans le calcul effectif.'),
e('Une zone rare',3,r'$X\sim\mathcal B(10,1/2)$.',r'Calculer $P(X\in\{0,1,9,10\})$.@@Cette zone a-t-elle une probabilité inférieure à $0{,}025$ ?@@Expliquer le lien avec l’intervalle $[2,8]$.',r'$(1+10+10+1)/1024=11/512\simeq0{,}021484$.@@Oui : $0{,}021484<0{,}025$.@@C’est son complément sur l’ensemble des valeurs entières possibles. La probabilité de $[2,8]$ dépasse donc $0{,}975$.'),
e('Construire plutôt que deviner',3,r'$X\sim\mathcal B(20,1/2)$. On veut un intervalle centré sur $10$, de probabilité au moins $0{,}95$.',r'Proposer une recherche par rayons entiers $r$.@@Calculer les probabilités pour $[6,14]$ et $[5,15]$.@@Conclure sur le plus petit rayon.',r'Pour $r=0,1,\ldots,10$, calculer $\sum_{k=10-r}^{10+r}\binom{20}k2^{-20}$ et s’arrêter au premier cumul au moins $0{,}95$.@@$P(6\leq X\leq14)=0{,}9586105347$ ; $P(5\leq X\leq15)=0{,}9881820679$.@@Le rayon $4$ convient. Le rayon $3$ donne $P(7\leq X\leq13)\simeq0{,}884682<0{,}95$ : $4$ est minimal.')
], 'grandsnombres'))

CHAPTERS.append(c('Temps d’attente et lois à densité','Probabilités et durée',r'Géométrique · Uniforme · Exponentielle · Mémoire',
'Modéliser le rang d’un premier succès.@@Vérifier une densité et calculer une probabilité par intégration.@@Utiliser les lois uniforme et exponentielle.@@Interpréter la fonction de répartition et l’absence de mémoire.',
'Intégrales, suites géométriques et indépendance.',r'''
\essSection{1}{Attendre un premier succès : le temps discret}
\begin{definition}[Loi géométrique sur $\N^*$]
Des essais indépendants ont une probabilité constante $p\in]0,1]$ de succès. Le rang $X$ du premier succès suit la loi géométrique de paramètre $p$ :
\[P(X=k)=(1-p)^{k-1}p\quad(k\geq1),\qquad P(X>n)=(1-p)^n.\]
Son espérance est $E(X)=1/p$ (admise).
\end{definition}
Le premier succès au rang $k$ impose $k-1$ échecs suivis d'un succès. La probabilité d'au moins un succès avant ou au rang $n$ est $1-(1-p)^n$.
\begin{propriete}[Sans mémoire]
Pour $m,n\in\N$ et $0<p<1$,
$P(X>m+n\mid X>m)=P(X>n)$.
En effet, le quotient des probabilités de survie vaut $(1-p)^{m+n}/(1-p)^m=(1-p)^n$.
\end{propriete}
Réciproquement, une survie discrète sans mémoire vérifie $S(m+n)=S(m)S(n)$, donc $S(n)=S(1)^n$ ; avec $S(1)=1-p$, on retrouve la loi géométrique.
\figurelivre{c11-geometrique.pdf}{Pour $p=0{,}25$, les masses de la loi géométrique décroissent ; la probabilité de continuer à attendre après $n$ essais vaut $0{,}75^n$. Le rang commence à $1$.}
\essSection{2}{Passer d'une masse à une densité}
\begin{definition}
Une densité $f$ est une fonction positive ou nulle dont l'intégrale sur tout le domaine vaut $1$.
Pour une variable de densité $f$,
$P(a\leq X\leq b)=\int_a^bf(x)\,\mathrm dx$.
La fonction de répartition est $F(x)=P(X\leq x)$.
\end{definition}
Une probabilité est une aire, pas la hauteur de la densité. Une densité peut dépasser $1$. Pour une loi à densité, $P(X=x)=0$ ; les inégalités strictes ou larges aux bornes d'un intervalle donnent la même probabilité.
Lorsque les intégrales existent,
$E(X)=\int xf(x)\,\mathrm dx$ et
$V(X)=\int(x-E(X))^2f(x)\,\mathrm dx=\int x^2f(x)\,\mathrm dx-E(X)^2$.
Les intégrales sur un domaine infini sont comprises comme des limites d'intégrales sur des intervalles bornés.
\essSection{3}{Une attente uniforme}
\begin{propriete}[Loi uniforme sur $[a,b]$, $a<b$]
La densité vaut $1/(b-a)$ sur $[a,b]$ et $0$ ailleurs.
Pour $a\leq c\leq d\leq b$, $P(c\leq X\leq d)=(d-c)/(b-a)$.
La répartition vaut $0$ avant $a$, $(x-a)/(b-a)$ entre $a$ et $b$, et $1$ après $b$.
\[E(X)=\frac{a+b}{2},\qquad V(X)=\frac{(b-a)^2}{12}.\]
\end{propriete}
Ces expressions se calculent par intégration. Sur $[0,1]$, $E(X)=\int_0^1x\,\mathrm dx=1/2$ et $V(X)=1/3-1/4=1/12$.
Une arrivée à un arrêt de bus est modélisée par une attente uniforme seulement si les hypothèses concernant les horaires et l'arrivée du voyageur le permettent.
\essSection{4}{Une attente exponentielle}
\begin{propriete}[Paramètre $\lambda>0$]
Sur $[0,+\infty[$, $f(t)=\lambda\mathrm e^{-\lambda t}$ ; ailleurs, $f=0$.
Pour $t\geq0$, $F(t)=1-\mathrm e^{-\lambda t}$ et $P(X>t)=\mathrm e^{-\lambda t}$.
$E(X)=1/\lambda$ ; l'absence de mémoire s'écrit
$P(X>s+t\mid X>s)=\mathrm e^{-\lambda t}$.
\end{propriete}
On vérifie la densité par $\int_0^bf(t)\,\mathrm dt=1-\mathrm e^{-\lambda b}\to1$.
Une primitive de $t\lambda\mathrm e^{-\lambda t}$ est $-(t+1/\lambda)\mathrm e^{-\lambda t}$ ; sa limite donne l'espérance annoncée.
\figurelivre{c11-densites.pdf}{À gauche : l'uniforme sur $[0,10]$. À droite : l'exponentielle de paramètre $0{,}2$. Les zones colorées représentent $P(2\leq X\leq6)$, avec des probabilités différentes malgré le même intervalle.}
La médiane exponentielle vaut $\ln2/\lambda$, différente de l'espérance $1/\lambda$.
L'absence de mémoire suit du quotient $\mathrm e^{-\lambda(s+t)}/\mathrm e^{-\lambda s}$.
Pour simuler cette loi à partir de $U$ uniforme sur $[0,1[$, on utilise $-\ln(1-U)/\lambda$.
En discrétisant par tranches de largeur $h$, le rang de la tranche d'un temps exponentiel suit une géométrique de paramètre $1-\mathrm e^{-\lambda h}$.
''',[
e('Premier succès',1,r'Chaque essai indépendant réussit avec probabilité $0{,}2$. $X$ est le rang du premier succès.',r'Calculer $P(X=3)$.@@Calculer $P(X>4)$.@@Donner l’espérance.',r'$0{,}8^2\times0{,}2=0{,}128$.@@$0{,}8^4=0{,}4096$.@@$E(X)=1/0{,}2=5$ essais.'),
e('Une uniforme',1,r'$X$ suit la loi uniforme sur $[2,8]$.',r'Donner sa densité.@@Calculer $P(3\leq X\leq5)$.@@Donner espérance et variance.',r'$1/6$ sur $[2,8]$, et zéro ailleurs.@@$(5-3)/(8-2)=1/3$.@@$E(X)=5$, $V(X)=6^2/12=3$.'),
e('Une exponentielle',1,r'$T$ suit une loi exponentielle de paramètre $0{,}5$, en minutes.',r'Calculer $P(T>2)$.@@Calculer $P(T\leq2)$.@@Donner la durée moyenne.',r'$\mathrm e^{-1}\simeq0{,}367879$.@@$1-\mathrm e^{-1}\simeq0{,}632121$.@@$1/0{,}5=2$ minutes.'),
e('Hauteur et aire',1,r'$X$ est uniforme sur $[0,0{,}2]$.',r'Donner la hauteur de sa densité.@@Pourquoi peut-elle dépasser $1$ ?@@Calculer $P(X=0{,}1)$.',r'$1/0{,}2=5$.@@C’est l’aire totale qui doit valoir $1$ : ici $5\times0{,}2=1$. Une hauteur n’est pas une probabilité.@@$0$, car une loi à densité attribue une probabilité nulle à un point isolé.'),
e('Vérifier une densité',2,r'$f(x)=kx$ sur $[0,2]$, et $0$ ailleurs.',r'Déterminer $k$ pour obtenir une densité.@@Calculer $P(X\leq1)$.@@Calculer $E(X)$.',r'$\int_0^2kx\,\mathrm dx=2k=1$ donne $k=1/2$ ; la fonction est bien positive.@@$\int_0^1x/2\,\mathrm dx=1/4$.@@$\int_0^2x^2/2\,\mathrm dx=4/3$.'),
e('Fonction de répartition',2,r'$X$ est de densité $2x$ sur $[0,1]$ et zéro ailleurs.',r'Donner $F(x)$ sur les trois intervalles pertinents.@@Calculer $P(1/2<X<3/4)$.@@Calculer la variance.',r'$F(x)=0$ si $x<0$, $x^2$ si $0\leq x\leq1$, et $1$ si $x>1$.@@$(3/4)^2-(1/2)^2=5/16$.@@$E(X)=2/3$, $E(X^2)=1/2$, donc $V(X)=1/2-4/9=1/18$.'),
e('Attendre encore',2,r'$X$ suit une géométrique de paramètre $0{,}3$.',r'Calculer $P(X>7\mid X>4)$.@@Comparer à $P(X>3)$.@@Donner le sens de l’absence de mémoire.',r'$0{,}7^7/0{,}7^4=0{,}7^3=0{,}343$.@@Les deux probabilités sont égales.@@Après quatre échecs, la probabilité d’attendre encore plus de trois essais est identique à celle du départ ; les essais futurs conservent le même modèle indépendant.'),
e('Retrouver le paramètre',2,r'$T$ suit une exponentielle et $P(T>10)=1/2$.',r'Déterminer $\lambda$.@@Calculer l’espérance.@@Calculer $P(T>20\mid T>10)$.',r'$\mathrm e^{-10\lambda}=1/2$, donc $\lambda=\ln2/10$.@@$10/\ln2\simeq14{,}427$ unités de temps.@@Par absence de mémoire, $P(T>10)=1/2$.'),
e('Bus et mémoire',3,r'Un bus passe exactement toutes les $12$ minutes. L’arrivée du voyageur est uniforme dans un cycle, donc l’attente $U$ est uniforme sur $[0,12]$.',r'Calculer $P(U>6)$.@@Calculer $P(U>9\mid U>3)$.@@Cette loi est-elle sans mémoire ?',r'$6/12=1/2$.@@$P(U>9)/P(U>3)=(3/12)/(9/12)=1/3$.@@Non : l’absence de mémoire imposerait ici $P(U>6)=1/2$, différent de $1/3$.'),
e('Simuler une exponentielle',3,r'$U$ est uniforme sur $[0,1[$ et $T=-\ln(1-U)/\lambda$.',r'Pour $t\geq0$, transformer l’événement $T\leq t$.@@Retrouver sa probabilité.@@Pourquoi préfère-t-on $1-U$ à $U$ si le générateur peut rendre zéro ?',r'$T\leq t$ équivaut à $\ln(1-U)\geq-\lambda t$, donc $U\leq1-\mathrm e^{-\lambda t}$.@@L’uniformité donne $P(T\leq t)=1-\mathrm e^{-\lambda t}$ : c’est l’exponentielle.@@$1-U$ est strictement positif si $U\in[0,1[$ ; le logarithme est alors défini, même lorsque $U=0$.'),
e('Discrétiser une attente',3,r'$T$ suit une exponentielle de paramètre $\lambda$. On note $K$ le numéro de la tranche $((k-1)h,kh]$ contenant $T$, avec $h>0$.',r'Calculer $P(K>n)$.@@Identifier la loi de $K$.@@Comparer le paramètre exact à $\lambda h$ lorsque le pas est petit.',r'$P(K>n)=P(T>nh)=\mathrm e^{-\lambda nh}$.@@C’est une géométrique sur $\N^*$ avec $1-p=\mathrm e^{-\lambda h}$, donc $p=1-\mathrm e^{-\lambda h}$.@@L’approximation locale $\mathrm e^{-z}\simeq1-z$ donne $p\simeq\lambda h$ pour $\lambda h$ petit ; ce n’est pas une égalité générale.'),
e('Une densité impossible',3,r'On propose $f(x)=3x-1$ sur $[0,1]$ et $0$ ailleurs.',r'Calculer l’intégrale totale.@@Repérer une zone où $f<0$.@@La multiplier par une constante suffit-il à produire une densité sur ce même intervalle ?',r'$\int_0^1(3x-1)\,\mathrm dx=1/2$.@@$f<0$ pour $0\leq x<1/3$.@@Non : une multiplication positive conserve les valeurs négatives ; une multiplication négative rend négative l’autre partie. L’intégrale égale à $1$ ne suffirait pas.')
], 'sommes'))

CHAPTERS.append(c('Statistiques à deux variables','Statistique et esprit critique',r'Nuage · Régression · Ajustement · Causalité',
'Représenter un nuage et calculer son point moyen.@@Déterminer et utiliser un ajustement affine.@@Linéariser un modèle exponentiel.@@Distinguer corrélation, prévision et causalité.',
'Moyenne, variance et fonction affine.',r'''
\essSection{1}{Deux mesures sur les mêmes individus}
Une série à deux variables est une liste de couples $(x_i,y_i)$ observés sur les mêmes individus ou aux mêmes dates. Le nuage de points conserve l'association entre les deux mesures.
Le point moyen est $G(\bar x,\bar y)$, avec $\bar x=\sum x_i/n$ et $\bar y=\sum y_i/n$.
Un nuage peut suggérer une tendance affine, exponentielle ou autre. Le choix d'un modèle doit être discuté à partir du contexte et des résidus, pas seulement d'un indicateur.
\figurelivre{c12-regression.pdf}{Données fictives $(1,2),(2,3),(3,5),(4,6)$. La droite des moindres carrés est $y=1{,}4x+0{,}5$ et passe par $G(2{,}5,4)$. Les segments verticaux sont les résidus.}
\essSection{2}{La droite des moindres carrés}
\begin{definition}
L'ajustement de $y$ en $x$ cherche la droite $y=ax+b$ minimisant
$S(a,b)=\sum_{i=1}^n(y_i-ax_i-b)^2$.
Les distances mesurées sont verticales. L'ajustement de $x$ en $y$ est un autre problème.
\end{definition}
Avec $V_x=\sum(x_i-\bar x)^2/n>0$ et
$\operatorname{Cov}(x,y)=\sum(x_i-\bar x)(y_i-\bar y)/n$,
\[a=\frac{\operatorname{Cov}(x,y)}{V_x},\qquad b=\bar y-a\bar x.\]
La calculatrice ou un tableur fournit ces coefficients. On doit annoncer la variable expliquée et conserver assez de chiffres dans les calculs.
\begin{demonstration}[Pourquoi ces coefficients ?]
Poser $X_i=x_i-\bar x$ et $Y_i=y_i-\bar y$. Comme $\sum X_i=\sum Y_i=0$,
$S(a,b)=\sum(Y_i-aX_i)^2+n(\bar y-a\bar x-b)^2$.
Pour $a$ fixé, le deuxième terme est minimal si $b=\bar y-a\bar x$.
Le premier vaut $n(V_y-2a\operatorname{Cov}+a^2V_x)$, trinôme minimal en $a=\operatorname{Cov}/V_x$.
\end{demonstration}
\essSection{3}{Le coefficient de corrélation}
Si les deux variances sont non nulles,
$r=\operatorname{Cov}(x,y)/\sqrt{V_xV_y}$, avec $-1\leq r\leq1$.
Une valeur proche de $1$ ou de $-1$ indique une forte liaison affine dans les données. Un $r$ proche de zéro ne signifie pas absence de toute relation : un nuage peut suivre une parabole symétrique.
Une valeur aberrante peut fortement déplacer la droite et $r$.
\essSection{4}{Interpoler, extrapoler et transformer}
Interpoler consiste à prédire entre les valeurs observées de $x$ ; extrapoler, au-delà. Plus l'on s'éloigne du domaine observé, plus la pertinence du modèle doit être examinée.
Si $y>0$ et si un modèle $y=A\mathrm e^{kx}$ est plausible, poser $z=\ln y$ donne $z=\ln A+kx$.
Après une régression de $z$ en $x$, on retrouve $A=\mathrm e^b$, $k=a$.
Cet ajustement minimise les résidus au carré sur l'échelle logarithmique ; ce n'est pas nécessairement le même critère que les résidus sur l'échelle initiale.
\begin{exemple}
Avec $y=2\times3^x$, $\ln y=\ln2+x\ln3$. Des rapports constants entre valeurs successives suggèrent un modèle exponentiel, tandis que des différences constantes suggèrent un modèle affine.
\end{exemple}
\essSection{5}{Corrélation et causalité}
Une corrélation peut venir d'un effet causal, d'un facteur commun, d'une causalité inverse, d'une sélection des observations ou d'une coïncidence.
\figurepetite{c12-causalite.pdf}{Un facteur commun peut influencer deux variables corrélées. La corrélation entre elles ne suffit pas à établir une flèche causale directe. Schéma conceptuel fictif.}
Un protocole, la connaissance du phénomène et le contrôle des facteurs confondants sont nécessaires pour argumenter une causalité.
À l'oral, présenter les axes, le domaine des observations, le modèle, ses résidus et ses limites. Éviter de transformer une association statistique en explication certaine.
''',[
e('Point moyen',1,r'Les couples sont $(1,3),(2,4),(3,8)$.',r'Calculer $\bar x$.@@Calculer $\bar y$.@@Donner le point moyen.',r'$\bar x=(1+2+3)/3=2$.@@$\bar y=(3+4+8)/3=5$.@@$G(2,5)$ ; il se calcule séparément sur les deux coordonnées.'),
e('Utiliser une droite',1,r'Un ajustement donne $y=2{,}5x+7$ pour des valeurs observées de $x$ entre $2$ et $8$.',r'Prédire $y$ pour $x=6$.@@Prédire pour $x=20$.@@Qualifier les deux prédictions.',r'$2{,}5\times6+7=22$.@@$2{,}5\times20+7=57$.@@La première est une interpolation ; la seconde une extrapolation éloignée, plus incertaine et à justifier.'),
e('Résidu',1,r'La droite ajustée est $y=3x+1$. Un point observé est $(2,8)$.',r'Calculer la valeur prédite.@@Calculer le résidu observé moins prédit.@@Donner sa contribution à la somme des carrés.',r'$3(2)+1=7$.@@$8-7=1$.@@$1^2=1$.'),
e('Lire une corrélation',1,'',r'Que suggère $r=-0{,}98$ ?@@Que ne permet-il pas d’affirmer ?@@Pourquoi $r=0$ n’exclut-il pas une relation non affine ?',r'Une forte association affine décroissante dans les données étudiées.@@Il ne prouve ni une causalité ni une validité du modèle hors du domaine observé.@@Par exemple, des points symétriques d’une parabole peuvent avoir une covariance nulle tout en suivant une relation déterministe.'),
e('Calculer une régression',2,r'On observe $(1,2),(2,3),(3,5),(4,6)$.',r'Calculer les moyennes, $V_x$ et la covariance.@@Déterminer $a,b$.@@Calculer $r$, sachant $V_y=2{,}5$.',r'$\bar x=2{,}5$, $\bar y=4$, $V_x=1{,}25$, $\operatorname{Cov}=1{,}75$.@@$a=1{,}75/1{,}25=1{,}4$, $b=4-1{,}4(2{,}5)=0{,}5$.@@$r=1{,}75/\sqrt{1{,}25\times2{,}5}\simeq0{,}989949$.'),
e('Exponentielle par transformation',2,r'Des données suivent exactement $y=5\times2^x$.',r'Exprimer $z=\ln y$.@@Donner la pente et l’ordonnée à l’origine dans le repère $(x,z)$.@@Retrouver $y$ à partir de ces coefficients.',r'$z=\ln5+x\ln2$.@@Pente $\ln2$ ; ordonnée $\ln5$.@@$y=\mathrm e^{\ln5}\mathrm e^{x\ln2}=5\times2^x$.'),
e('Interpolation et seuil',2,r'Un modèle fictif est $y=4\mathrm e^{0{,}3t}$, ajusté pour $0\leq t\leq5$.',r'Prédire la valeur en $t=3$.@@Résoudre $y=20$.@@Discuter le résultat par rapport aux données.',r'$4\mathrm e^{0{,}9}\simeq9{,}838$.@@$\mathrm e^{0{,}3t}=5$, donc $t=\ln5/0{,}3\simeq5{,}365$.@@Cette date dépasse le domaine observé ; c’est une extrapolation, à considérer avec prudence.'),
e('Moindres carrés',2,r'Pour trois points, une droite $D_1$ donne les résidus $1,-1,0$ ; $D_2$ donne $0,0,2$.',r'Calculer les deux sommes de carrés.@@Quelle droite est préférable selon ce critère parmi les deux ?@@Peut-on affirmer qu’il s’agit de la meilleure de toutes les droites ?',r'$S_1=1+1+0=2$ et $S_2=4$.@@$D_1$, car $2<4$.@@Non : on n’a comparé que deux candidates, sans minimiser sur l’ensemble des droites.'),
e('Corrélation nulle et parabole',3,r'On considère $(-1,1),(0,0),(1,1)$.',r'Calculer le point moyen.@@Montrer que la covariance vaut zéro.@@Quelle relation exacte existe pourtant ?',r'$G(0,2/3)$.@@$[(-1)(1-2/3)+0+(1)(1-2/3)]/3=0$.@@$y=x^2$ pour les trois points. Le coefficient de corrélation affine nul n’exclut pas une liaison non linéaire.'),
e('Une variable confondante',3,r'Dans des données fictives, les ventes de boissons fraîches et les baignades augmentent ensemble.',r'Proposer un facteur commun plausible.@@Peut-on conclure que les achats provoquent les baignades ?@@Que faudrait-il examiner pour discuter un lien causal ?',r'La température ou la saison peut influencer les deux.@@Non : la corrélation seule ne suffit pas à attribuer une causalité directe.@@Le protocole, la chronologie, les facteurs communs et les mécanismes possibles ; comparer des situations où ces facteurs sont contrôlés.'),
e('Changer les unités',3,r'Une régression relie $x$ en heures à $y$ en kilomètres : $y=60x+5$.',r'Écrire le modèle avec le temps $u$ en minutes.@@La valeur prédite pour le même instant change-t-elle ?@@Le coefficient de corrélation change-t-il sous ce changement d’unité positif ?',r'$x=u/60$, donc $y=u+5$.@@Non : les nombres de l’abscisse changent avec l’unité, mais la situation et la distance prédite restent les mêmes.@@Non : multiplier une variable par une constante positive laisse $r$ inchangé ; la pente numérique, elle, change.'),
e('Pourquoi la droite passe par $G$',3,'',r'Pour $a$ fixé, écrire $S(a,b)$ en séparant le terme contenant $\bar y-a\bar x-b$.@@En déduire le meilleur $b$.@@Que se passe-t-il si tous les $x_i$ sont égaux ?',r'Avec les variables centrées, $S(a,b)=\sum(Y_i-aX_i)^2+n(\bar y-a\bar x-b)^2$, car les termes croisés se compensent.@@Le carré est minimal en zéro : $b=\bar y-a\bar x$, donc $a\bar x+b=\bar y$.@@$V_x=0$ ; la formule de la pente divise par zéro et une pente unique n’est pas identifiable à partir d’un seul niveau de $x$.')
], 'courbe'))

CHAPTERS.append(c('Algorithmique, logique et raisonnement','Outils transversaux',r'Fonctions Python · Listes · Ensembles · Preuve',
'Décomposer une tâche en fonctions testables.@@Utiliser variables, boucles, conditions et listes.@@Manipuler ensembles et propositions.@@Distinguer implication, réciproque et équivalence.',
'Algorithmique de Seconde et Première ; notions rencontrées dans les chapitres.',r'''
\essSection{1}{Écrire un programme qui répond à une question}
Une fonction informatique possède des paramètres, un traitement et une valeur renvoyée par \code{return}. Définir ce qui entre et ce qui sort aide à vérifier le programme.
L'affectation \code{u = 2*u + 1} remplace la valeur de \code{u} ; ce n'est pas une équation à résoudre.
Une boucle \code{for} convient à un nombre de répétitions connu ; une boucle \code{while} dépend d'une condition dont il faut justifier qu'elle finit par devenir fausse.
\begin{python}
def termes_affines(u0, a, b, n):
    termes = [u0]
    u = u0
    for k in range(n):
        u = a*u + b
        termes.append(u)
    return termes
\end{python}
Cette fonction rend $n+1$ valeurs, de $u_0$ à $u_n$. Les indices d'une liste Python commencent à zéro.
La programmation modulaire évite de réécrire les mêmes calculs : une fonction pour une masse binomiale, une autre pour un cumul, une troisième pour chercher un seuil.
\essSection{2}{Expérimenter, puis vérifier}
Pour un calcul numérique, tester un cas connu, un cas limite et les hypothèses de domaine. Des nombres décimaux sont représentés approximativement : une égalité mathématique n'est pas toujours une égalité machine exacte.
\begin{savoirfaire}[Un compte rendu d'algorithme]
Préciser les entrées ; expliquer chaque variable ; donner la condition d'arrêt ; tester sur un exemple dont on connaît le résultat ; interpréter la sortie et sa précision.
Pour une simulation, préciser le modèle et le nombre de répétitions. Pour un encadrement, vérifier que la racine reste dans l'intervalle.
\end{savoirfaire}
\figurelivre{c13-algorithme.pdf}{La boucle d'un algorithme de seuil : initialisation, test, mise à jour et sortie. Une condition d'arrêt doit être cohérente avec l'inégalité demandée.}
\essSection{3}{Ensembles et événements}
$x\in A$ signifie que $x$ est un élément de $A$ ; $A\subset B$ que chaque élément de $A$ appartient à $B$.
$A\cap B$ signifie « dans $A$ et dans $B$ » ; $A\cup B$, « dans $A$ ou dans $B$, éventuellement les deux ».
Le complémentaire de $A$ dans $E$ est $E\setminus A$, ou $\bar A$ en probabilités.
Un couple $(x,y)$ est ordonné : en général $(x,y)\ne(y,x)$.
\begin{exemple}
Pour $A=[0,3]$ et $B=[2,5]$, $A\cap B=[2,3]$ et $A\cup B=[0,5]$.
La négation de « $x>0$ et $x<3$ » est « $x\leq0$ ou $x\geq3$ ».
\end{exemple}
\essSection{4}{Choisir une forme de raisonnement}
Une proposition est un énoncé auquel on peut attribuer vrai ou faux lorsque ses variables et son domaine sont précisés.
L'implication « si $P$, alors $Q$ » ne dit pas que $Q$ entraîne $P$. Sa réciproque est « si $Q$, alors $P$ ».
L'équivalence nécessite les deux implications.
Un contre-exemple suffit à réfuter une affirmation universelle ; des exemples, même nombreux, ne suffisent pas à la prouver.
\begin{exemple}[Une réciproque fausse]
Si $x=2$, alors $x^2=4$. La réciproque est fausse sur $\R$ : $x=-2$ satisfait $x^2=4$.
En revanche, sur $[0,+\infty[$, $x^2=4$ équivaut à $x=2$.
\end{exemple}
\essSection{5}{Quantifier et communiquer}
« Pour tout $x>0$, $\ln x\leq x-1$ » est universel. « Il existe $x>0$ tel que $\ln x=0$ » est existentiel, vérifié par $x=1$.
Le symbole $\sum$ abrège une addition : $\sum_{k=0}^{n}u_k$ contient $n+1$ termes.
À l'oral, annoncer l'objectif, les hypothèses, la méthode, le résultat et sa limite de validité. Un graphique doit présenter ses axes et une légende ; un nombre doit garder son unité ou son statut de probabilité.
''',[
e('Affectation',1,r'On exécute \code{u = 3}, puis \code{u = 2*u + 1}.',r'Quelle est la valeur finale ?@@Pourquoi ne résout-on pas $u=2u+1$ ?@@Que donnerait une répétition supplémentaire ?',r'$u=7$.@@Le signe d’affectation remplace une ancienne valeur par une nouvelle ; il n’exprime pas une égalité simultanée.@@$2\times7+1=15$.'),
e('Liste',1,r'On appelle \code{termes_affines(0, 2, 1, 3)}.',r'Donner la liste rendue.@@Quelle est sa longueur ?@@Quelle valeur occupe l’indice $2$ ?',r'$[0,1,3,7]$.@@$4$, puisque la valeur initiale est conservée avant les trois mises à jour.@@$3$, qui est $u_2$.'),
e('Ensembles',1,r'$A=\{1,2,3\}$ et $B=\{3,4\}$ dans $E=\{1,2,3,4,5\}$.',r'Donner $A\cap B$ et $A\cup B$.@@Donner $E\setminus A$.@@L’affirmation $A\subset B$ est-elle vraie ?',r'$A\cap B=\{3\}$ ; $A\cup B=\{1,2,3,4\}$.@@$\{4,5\}$.@@Non : $1\in A$ mais $1\notin B$.'),
e('Nier une proposition',1,'',r'Nier « $x>2$ ».@@Nier « $x<0$ ou $x>4$ ».@@Nier « $x\geq1$ et $x\leq3$ ».',r'« $x\leq2$ ».@@« $x\geq0$ et $x\leq4$ ».@@« $x<1$ ou $x>3$ ». La négation échange « et » et « ou » et nie chaque condition.'),
e('Finir une boucle',2,r'On part de $u=1$ et l’on multiplie par $2$ tant que $u<100$.',r'Combien de mises à jour sont faites ?@@Quelle est la valeur finale ?@@Que changerait la condition $u\leq128$ ?',r'$7$ : $2^6=64<100\leq128=2^7$.@@$128$.@@La boucle ferait encore une mise à jour quand $u=128$ ; elle s’arrêterait en $256$, après $8$ mises à jour.'),
e('Une fonction de moyenne',2,'',r'Écrire une fonction Python donnant la moyenne d’une liste non vide.@@Quelle hypothèse faut-il vérifier ?@@Tester sur $[2,4,9]$.',r'\code{def moyenne(valeurs): return sum(valeurs)/len(valeurs)}.@@La liste doit être non vide et ses éléments numériques ; sinon la division ou la somme n’a pas le sens voulu.@@$(2+4+9)/3=5$.'),
e('Implication',2,'',r'La proposition « $x>2$ entraîne $x^2>4$ » est-elle vraie sur $\R$ ?@@Écrire la réciproque et la tester.@@Quel domaine rend les deux propositions équivalentes ?',r'Oui : $x>2$ est positif et le carré est strictement croissant sur $[0,+\infty[$.@@« $x^2>4$ entraîne $x>2$ » est fausse sur $\R$, avec $x=-3$.@@Sur $[0,+\infty[$, $x>2$ équivaut à $x^2>4$.'),
e('Tester un programme de cumul',2,r'Une fonction est censée calculer $P(X\leq k)$ pour une binomiale de taille $n$.',r'Que doit-elle rendre pour $k=n$ ?@@Que doit-elle rendre pour $k=0$ ?@@Pourquoi un résultat légèrement différent de $1$ en machine peut-il apparaître ?',r'$1$ mathématiquement, car toutes les valeurs possibles sont incluses.@@$(1-p)^n$.@@Les arrondis successifs sur des nombres flottants peuvent créer une petite erreur ; on contrôle avec une tolérance adaptée.'),
e('Contre-exemple',3,'',r'Réfuter « toute suite positive est croissante ».@@Réfuter « si $f\,\!^{\prime}(a)=0$, alors $f$ a un extremum en $a$ ».@@Pourquoi un seul exemple suffit-il dans chaque cas ?',r'$u_n=1/(n+1)$ est positive et strictement décroissante.@@$f(x)=x^3$ a $f\,\!^{\prime}(0)=0$ sans extremum en zéro.@@Une affirmation universelle prétend couvrir tous les cas ; un cas contraire contredit cette prétention.'),
e('Raisonner sur un intervalle',3,r'On cherche les solutions de $\ln(x-1)=\ln(3-x)$.',r'Déterminer le domaine commun.@@Résoudre par équivalence.@@Comment présenter une preuve complète ?',r'$x-1>0$ et $3-x>0$, donc $1<x<3$.@@La stricte croissance de $\ln$ donne $x-1=3-x$, donc $x=2$, qui appartient au domaine.@@Annoncer le domaine, justifier l’injectivité du logarithme, résoudre puis vérifier l’appartenance. On conclut par l’ensemble $\{2\}$.'),
e('Somme : une erreur de borne',3,r'Un programme utilise \code{sum(k for k in range(n))}.',r'Quelle somme calcule-t-il ?@@Comment calculer $1+\cdots+n$ ?@@Comparer pour $n=5$.',r'$0+1+\cdots+(n-1)$ pour $n\geq1$.@@Utiliser \code{sum(range(1, n+1))}.@@Le premier rend $10$ ; le second $15$. La borne finale de \code{range} est exclue.'),
e('Un oral argumenté',3,r'Préparer une présentation de trois minutes sur la question « Un test très sensible donne-t-il toujours un résultat positif fiable ? ».',r'Choisir un modèle chiffré.@@Identifier le schéma et le calcul à présenter.@@Formuler une conclusion et une limite.',r'Par exemple le modèle fictif du chapitre 8 : proportion initiale $2\,\%$, sensibilité $95\,\%$, spécificité $95\,\%$.@@Présenter un arbre ou les effectifs sur $10\,000$ personnes : $190$ vrais positifs et $490$ faux positifs ; Bayes donne $19/68\simeq27{,}94\,\%$.@@La sensibilité et la valeur prédictive positive sont deux conditionnements différents. La conclusion dépend des données fictives et des hypothèses du modèle, pas d’un conseil individuel.')
], 'conditions'))

PROJECTS=[
('Une serre à construire','Thème 1 · Modèles définis par une fonction',r'Une serre rectangulaire est adossée à un mur. On dispose de $40$ m de clôture pour les trois autres côtés. La largeur perpendiculaire au mur est $x$.',
r'Exprimer l’aire et préciser le domaine.@@Chercher les dimensions maximisant cette aire.@@On impose une aire d’au moins $150$ m$^2$. Déterminer les largeurs possibles.@@Présenter un schéma coté et une conclusion.',
r'La longueur vaut $40-2x$ ; $A(x)=40x-2x^2$, avec $0<x<20$.@@$A\,\!^{\prime}=40-4x$ : le maximum est en $x=10$, avec une longueur de $20$ m et une aire de $200$ m$^2$.@@$40x-2x^2\geq150$ équivaut à $x^2-20x+75\leq0$, donc $5\leq x\leq15$.@@Le schéma doit montrer le mur, deux largeurs $x$ et le côté $40-2x$. La solution respecte les $40$ m disponibles ; le modèle néglige l’épaisseur des matériaux.'),
('Deux modèles de refroidissement','Thème 2 · Modèles d’évolution',r'Une température initiale vaut $80$ ; l’environnement reste à $20$. Le modèle continu est $T\,\!^{\prime}=-0{,}1(T-20)$. Le temps est en minutes.',
r'Résoudre avec la condition initiale.@@Construire le modèle d’Euler de pas $1$ et sa formule explicite.@@Comparer les températures au temps $10$.@@Quelle approximation peut-on améliorer et comment ?',
r'$T(t)=20+60\mathrm e^{-0{,}1t}$.@@$u_{n+1}=0{,}9u_n+2$, $u_0=80$ ; donc $u_n=20+60(0{,}9)^n$.@@$T(10)\simeq42{,}073$ et $u_{10}\simeq40{,}921$ ; Euler est ici plus bas d’environ $1{,}152$.@@Réduire le pas d’Euler et comparer à la solution exacte. Une précision numérique meilleure ne corrige toutefois pas une hypothèse physique inadaptée.'),
('Du produit à la somme','Thème 3 · Approche historique du logarithme',r'On construit une table associant à $x$ son logarithme décimal $\ell(x)=\ln x/\ln10$.',
r'Prouver $\ell(xy)=\ell(x)+\ell(y)$.@@On lit $\ell(2)\simeq0{,}30103$, $\ell(3)\simeq0{,}47712$. Approcher $\ell(6)$ et $\ell(12)$.@@Montrer que l’aire sous $1/t$ entre $1$ et $x>1$ vaut $\ln x$.@@Expliquer les liens entre table de calcul, progression géométrique et aire sous une courbe.',
r'La propriété du logarithme népérien, divisée par $\ln10$, donne l’identité.@@$\ell(6)\simeq0{,}77815$ et $\ell(12)=2\ell(2)+\ell(3)\simeq1{,}07918$.@@Une primitive de $1/t$ est $\ln t$ : $\int_1^x\mathrm dt/t=\ln x$.@@Les puissances d’une base, en progression géométrique, ont des logarithmes en progression arithmétique. Une autre construction du logarithme utilise l’aire sous l’hyperbole. Les deux approches conduisent à la même fonction après normalisation.'),
('Une aire sans primitive usuelle','Thème 4 · Calculs d’aires',r'On étudie $I=\int_0^1\mathrm e^{-x^2}\,\mathrm dx$.',
r'Encadrer grossièrement $I$ par deux constantes.@@Écrire des sommes de rectangles donnant un encadrement.@@Proposer un programme Monte-Carlo dans le carré unité.@@Comparer les garanties des deux méthodes.',
r'Sur $[0,1]$, $\mathrm e^{-1}\leq\mathrm e^{-x^2}\leq1$, donc $\mathrm e^{-1}\leq I\leq1$.@@La fonction décroît : $D_n=\frac1n\sum_{k=1}^n\mathrm e^{-(k/n)^2}\leq I\leq G_n=\frac1n\sum_{k=0}^{n-1}\mathrm e^{-(k/n)^2}$. La largeur vaut $(1-\mathrm e^{-1})/n$.@@Tirer $N$ couples indépendants $(U,V)$ uniformes dans le carré ; compter les $V\leq\mathrm e^{-U^2}$ et rendre ce nombre divisé par $N$.@@Les rectangles donnent un encadrement déterministe sous les hypothèses de monotonie. Monte-Carlo donne une estimation aléatoire dont la fluctuation doit être étudiée ; il ne donne pas à lui seul une borne certaine.'),
('Mesurer une inégalité','Thème 5 · Répartition des richesses',r'On compare $L_A(x)=x^2$ et $L_B(x)=(x+x^3)/2$ pour $0\leq x\leq1$.',
r'Vérifier que les deux modèles ont les caractéristiques d’une courbe de Lorenz.@@Calculer les deux indices de Gini.@@Comparer directement les courbes.@@Une multiplication de tous les revenus par $2$ change-t-elle ces indicateurs ?',
r'Les deux vont de $0$ à $1$, sont croissantes, convexes et sous la diagonale : pour $B$, $L_B\,\!^{\prime}=(1+3x^2)/2>0$ et $L_B\,\!^{\prime\prime}=3x\geq0$.@@$G_A=1/3$ ; $\int_0^1L_B=\tfrac12(1/2+1/4)=3/8$, donc $G_B=1/4$.@@$L_B-L_A=x(x-1)^2/2\geq0$ : $B$ est plus proche de l’égalité au sens de Lorenz.@@Non : les parts relatives restent identiques. Le niveau des revenus et leur répartition relative sont des informations distinctes.'),
('Une information qui change la décision','Thème 6 · Inférence bayésienne',r'Deux fournisseurs $A,B$ livrent respectivement $80\,\%$ et $20\,\%$ des composants. Les défauts concernent $1\,\%$ des composants de $A$ et $6\,\%$ de ceux de $B$.',
r'Construire un arbre et calculer le taux de défaut.@@Quelle est la probabilité qu’un composant défectueux vienne de $B$ ?@@À quelle part de marché $p$ de $B$ les défauts provenant de $B$ deviennent-ils majoritaires parmi tous les défauts ?@@Expliquer la différence entre probabilité a priori et a posteriori.',
r'Les chemins défectueux ont probabilités $0{,}8(0{,}01)=0{,}008$ et $0{,}2(0{,}06)=0{,}012$ ; total $0{,}02$.@@$0{,}012/0{,}02=0{,}6$.@@$0{,}06p>0{,}01(1-p)$ équivaut à $p>1/7$.@@Avant l’observation, $P(B)=0{,}2$ ; après observation d’un défaut, $P_D(B)=0{,}6$. Le taux plus élevé de défaut chez $B$ explique cette révision.'),
('Contrôler une surréservation','Thème 7 · Répétitions et échantillonnage',r'Une petite navette accepte $12$ réservations pour $10$ places. Chaque client se présente indépendamment avec probabilité $0{,}8$.',
r'Identifier la loi du nombre $X$ de présents.@@Calculer $P(X>10)$.@@La règle « risque de dépassement au plus $0{,}05$ » est-elle respectée ?@@Citer deux hypothèses dont la violation modifierait la conclusion.',
r'$X\sim\mathcal B(12,0{,}8)$.@@$P(X=11)+P(X=12)=12(0{,}8)^{11}(0{,}2)+(0{,}8)^{12}\simeq0{,}274878$.@@Non : le risque vaut environ $27{,}49\,\%$, au-dessus de $5\,\%$. Une espérance de $9{,}6$ présents inférieure à $10$ ne suffit pas.@@Des clients voyageant en groupe créent une dépendance ; des probabilités de présence différentes selon les personnes empêchent l’usage direct de cette binomiale.'),
('Attendre sans vieillir ?','Thème 8 · Temps d’attente',r'Un composant fictif a une durée $T$ exponentielle de moyenne $50$ heures. On le compare à une attente $U$ uniforme sur $[0,100]$.',
r'Donner les deux espérances.@@Calculer $P(T>40\mid T>10)$.@@Calculer $P(U>40\mid U>10)$.@@Comparer avec les probabilités d’attendre encore plus de $30$ heures au départ.',
r'$E(T)=E(U)=50$ heures ; pour l’exponentielle $\lambda=0{,}02$.@@$\mathrm e^{-0{,}02\times30}=\mathrm e^{-0{,}6}\simeq0{,}548812$.@@$(60/100)/(90/100)=2/3$.@@$P(T>30)=\mathrm e^{-0{,}6}$ : égalité sans mémoire. $P(U>30)=0{,}7\ne2/3$ : l’uniforme n’a pas cette propriété. Une même moyenne n’implique pas une même loi.'),
('Une croissance observée','Thème 9 · Corrélation et causalité',r'Les couples fictifs $(t,y)$ sont $(0,2),(1,4),(2,8),(3,16)$.',
r'Construire le nuage et proposer un modèle.@@Linéariser par logarithme et retrouver le modèle.@@Prévoir $y$ pour $t=4$ puis $t=20$ ; comparer la portée des prévisions.@@Cette association exacte prouve-t-elle que le temps est une cause du phénomène ?',
r'Les rapports successifs valent $2$ : $y=2\times2^t$ est un modèle compatible.@@$\ln y=\ln2+t\ln2$ ; l’ajustement logarithmique est exactement affine.@@$y(4)=32$ et $y(20)=2\,097\,152$. Ce sont deux extrapolations ; la seconde est beaucoup plus éloignée des données et peut être dénuée de pertinence.@@Non. Le temps indexe les observations ; le mécanisme doit être expliqué par le contexte. Quatre couples ne démontrent pas une loi universelle ni un lien causal.')
]

ASSESSMENTS=[
('Évaluation 1 · Analyse','60 minutes · 20 points',r'Pour $t\geq0$, $f(t)=20+80\mathrm e^{-0{,}25t}$.',
r'Calculer $f(0)$, la dérivée et la limite en $+\infty$. \hfill(4 points)@@Résoudre $f(t)\leq40$. \hfill(4 points)@@Donner l’équation différentielle et la condition initiale de ce modèle. \hfill(4 points)@@Calculer la moyenne de $f$ sur $[0,4]$. \hfill(4 points)@@Construire Euler avec pas $1$ ; calculer deux étapes et comparer à l’exact. \hfill(4 points)',
r'$f(0)=100$ ; $f\,\!^{\prime}=-20\mathrm e^{-t/4}<0$ ; limite $20$. Barème : 1, 2 et 1 point.@@$\mathrm e^{-t/4}\leq1/4$ donne $t\geq4\ln4\simeq5{,}545$. Domaine et transformation : 2 points ; résolution et conclusion : 2 points.@@$y\,\!^{\prime}=-y/4+5$, $y(0)=100$. Vérifier en substituant ; 2 points pour chaque élément.@@Une primitive est $20t-320\mathrm e^{-t/4}$ ; moyenne $20+80(1-\mathrm e^{-1})\simeq70{,}570$. Primitive : 2 points ; calcul et interprétation : 2 points.@@$u_{n+1}=0{,}75u_n+5$, $u_0=100$ ; $u_1=80,u_2=65$. L’exact donne $f(1)\simeq82{,}304$, $f(2)\simeq68{,}522$. Euler sous-estime ici. Récurrence : 2 points ; valeurs et comparaison : 2 points.'),
('Évaluation 2 · Probabilités','60 minutes · 20 points',r'Un atelier $A$ fabrique $70\,\%$ des pièces, dont $2\,\%$ sont défectueuses. L’atelier $B$ fabrique le reste, dont $5\,\%$ sont défectueuses.',
r'Calculer la probabilité $d$ d’un défaut. \hfill(4 points)@@Une pièce est défectueuse : calculer la probabilité qu’elle vienne de $B$. \hfill(4 points)@@Pour dix pièces indépendantes au même taux $d$, identifier la loi du nombre de défauts et la probabilité d’au moins un défaut. \hfill(4 points)@@On répète des contrôles indépendants jusqu’au premier défaut. Donner la loi du rang, l’espérance et la probabilité de plus de vingt contrôles. \hfill(4 points)@@Une attente continue suit une exponentielle de moyenne $30$ minutes. Calculer $P(T>15)$ et $P(T>25\mid T>10)$. \hfill(4 points)',
r'$d=0{,}7(0{,}02)+0{,}3(0{,}05)=0{,}029$. Arbre ou formule : 2 points ; valeur : 2 points.@@$P_D(B)=0{,}015/0{,}029=15/29\simeq0{,}517241$. Bayes : 2 points ; calcul : 2 points.@@$X\sim\mathcal B(10,0{,}029)$ ; $P(X\geq1)=1-0{,}971^{10}\simeq0{,}254938$. Loi et hypothèses : 2 points ; complément : 2 points.@@Géométrique sur $\N^*$ de paramètre $0{,}029$ ; $E=1/0{,}029\simeq34{,}483$ ; $P(X>20)=0{,}971^{20}\simeq0{,}555117$. Loi : 1 point ; espérance : 1 point ; survie : 2 points.@@$\lambda=1/30$ ; les deux probabilités valent $\mathrm e^{-1/2}\simeq0{,}606531$. Paramètre et première probabilité : 2 points ; absence de mémoire : 2 points.'),
('Évaluation 3 · Statistique et inégalités','60 minutes · 20 points',r'Les observations fictives sont $(1,2),(2,3),(3,5),(4,6)$. On considère aussi la répartition $L(x)=x^2$.',
r'Calculer le point moyen et les quantités nécessaires à une régression affine. \hfill(4 points)@@Déterminer la droite et prédire en $x=3{,}5$, puis en $x=10$. Discuter. \hfill(4 points)@@Calculer le coefficient de corrélation ; commenter sans conclure à une causalité. \hfill(4 points)@@Vérifier que $L$ est une courbe de Lorenz et interpréter $L(0{,}6)$. \hfill(4 points)@@Calculer Gini et expliquer l’effet d’une multiplication de tous les revenus par une même constante positive. \hfill(4 points)',
r'$G(2{,}5,4)$, $V_x=1{,}25$, $V_y=2{,}5$, covariance $1{,}75$. Un point par quantité ou groupe de moyennes.@@$y=1{,}4x+0{,}5$ ; prévisions $5{,}4$ et $14{,}5$. La première interpole, la seconde extrapole au-delà de $[1,4]$. Coefficients : 2 points ; valeurs et critique : 2 points.@@$r=1{,}75/\sqrt{3{,}125}\simeq0{,}989949$ : forte association affine sur ces données, sans preuve causale. Calcul : 2 points ; commentaire : 2 points.@@$L(0)=0,L(1)=1$, $L\,\!^{\prime}=2x\geq0$, $L\,\!^{\prime\prime}=2>0$ et $x^2\leq x$ sur $[0,1]$. $L(0{,}6)=0{,}36$ : les $60\,\%$ les moins riches possèdent $36\,\%$ de la richesse. Vérifications : 3 points ; lecture : 1 point.@@$G=1-2\int_0^1x^2\,\mathrm dx=1/3$. Une multiplication commune conserve les parts relatives, donc Lorenz et Gini. Calcul : 2 points ; explication : 2 points.')
]

def project_pages(projects,prefix,solution=False,solution_par_page=False):
    text=''
    for i,(title,theme,intro,q,a) in enumerate(projects,1):
        if solution:
            if i==1:text+=rf'\fiche{{Solutions des {"dossiers" if prefix=="projet" else "évaluations"}}}{{Méthodes et conclusions}}'
            elif solution_par_page:text+=r'\clearpage'
            text+=rf'\par\addvspace{{6mm}}\Needspace{{9\baselineskip}}\souscours{{{i}. {title}}}'
        else:text+=rf'\fiche{{{title}}}{{{theme}}}'
        text+=rf'\phantomsection\label{{{prefix}{"-cor" if solution else ""}-{i}}}\pdfbookmark[1]{{{title}}}{{bm-{prefix}{"-cor" if solution else ""}-{i}}}'+'\n'
        text+=('\\repere{'+prefix+'-'+str(i)+'}{Énoncé}\n' if solution else intro+'\n\\repere{'+prefix+'-cor-'+str(i)+'}{Solution}\n')
        items=(a if solution else q).split('@@')
        text+='\\begin{questions}\n'+''.join('\\item '+s+'\n' for s in items)+'\\end{questions}\n'
        if not solution:text+=r'\vspace{5mm}\souscours{Pour communiquer}\noindent Présenter les hypothèses, la démarche et une conclusion ; accompagner les résultats numériques de leur précision. Garder une trace de recherche, y compris des essais qui ont permis de choisir la méthode.\par\vfill\noindent{\otMedium\fontsize{8}{10}\selectfont\color{otMuted}Espace de recherche}\par\vspace{2mm}\noindent\begin{tikzpicture}\draw[otRule,line width=.2pt,step=5mm] (0,0) grid (160mm,60mm);\end{tikzpicture}'+'\n'
    return text

DOSSIERS=r'\clearpage\begingroup\renewcommand{\otThumb}{}\renewcommand{\otHeadTag}{D}\phantomsection\label{dossiers}\pdfbookmark[0]{Dossiers et évaluations}{dossiers}'+project_pages(PROJECTS,'projet')+project_pages(ASSESSMENTS,'evaluation')+r'\clearpage\endgroup'
SOLUTIONS_DOSSIERS=project_pages(PROJECTS,'projet',True)+project_pages(ASSESSMENTS,'evaluation',True)

CONCORDANCE=r'''
\fiche{Concordance du programme}{Repérer les contenus et les capacités attendues}
\phantomsection\label{concordance}\pdfbookmark[0]{Programme et sources}{programme}
Référence principale : enseignement optionnel de mathématiques complémentaires de Terminale générale, BO spécial n° 8 du 25 juillet 2019, arrêté du 19 juillet 2019, NOR MENE1921265A. Cette édition vise l'année 2026-2027.
Les intitulés ci-dessous sont des regroupements éditoriaux ; le document officiel reste la référence réglementaire.
\souscours{Analyse}
'''
COVERAGE=[
('A01','Modéliser par suite explicite ou récurrente ; représentation en escalier',1,'5, 9, 11'),
('A02','Limites finies et infinies, opérations, inégalités et gendarmes',1,'3, 8, 12'),
('A03','Suites géométriques positives, sommes et limites de sommes',1,'2, 7'),
('A04','Récurrence affine : équilibre, décalage et expression de toutes les solutions',1,'4, 5, 6'),
('A05','Exponentielle, logarithme réciproque, limites et équation fonctionnelle',2,'1, 3, 7, 9'),
('A06','Logarithme d’une puissance et recherche de seuils',2,'5, 6, 12'),
('A07','Limites des fonctions usuelles ; asymptotes et formes indéterminées',3,'1, 2, 3, 10'),
('A08','Continuité, valeurs intermédiaires, monotonie et nombre de solutions',3,'5, 6, 7, 9'),
('A09','Réciproques : carré/racine et exponentielle/logarithme',3,'4'),
('A10','Valeurs approchées, encadrement et résolution numérique',3,'8, 11, 12'),
('A11','Dérivées : affine composée, carré de fonction, exponentielle et logarithme composés',4,'1, 2, 8'),
('A12','Tableaux de variation, équations, inéquations, optimisation contextualisée',4,'4, 5, 6, 9, 11'),
('A13','Convexité par sécantes et tangentes ; croissance de la dérivée, signe de la dérivée seconde',5,'1, 2, 6, 11'),
('A14','Convexité, concavité, point d’inflexion et lecture de courbes',5,'3, 5, 9, 12'),
('A15','Primitives, constante ; formes reconnues $2uu^{\prime}$, $u^{\prime}\mathrm e^u$, $u^{\prime}/u$',6,'1, 2, 3, 9'),
('A16','Vérifier une solution ; résoudre $y^{\prime}=ay$ et $y^{\prime}=ay+b$',6,'4, 5, 6, 7, 12'),
('A17','Intégrale positive ou signée, Chasles, primitive définie par intégrale',7,'1, 2, 4, 11'),
('A18','Aires sous/entre courbes, encadrement, valeur moyenne et interprétation',7,'3, 5, 6, 12'),
('P01','Conditionnement, probabilité totale, Bayes et répétitions conditionnelles',8,'2, 4, 5, 7, 10'),
('P02','Uniforme discrète : loi, espérance ; Bernoulli : loi, espérance, écart type',9,'1, 2, 9'),
('P03','Schéma de Bernoulli, arbre, coefficients, Pascal et symétrie',9,'3, 4, 5, 10'),
('P04','Binomiale : masses, cumuls, espérance et écart type en résolution de problème',9,'5, 6, 7, 8, 11'),
('P05','Intervalles binomiaux de grande ou faible probabilité ; décision et échantillonnage',10,'3, 5, 6, 11, 12'),
('P06','Géométrique : loi, représentation, espérance, calcul et absence de mémoire',11,'1, 7, 11'),
('P07','Densité, probabilité comme aire, fonction de répartition, intégrales d’espérance et de variance',11,'4, 5, 6, 12'),
('P08','Uniforme continue $[0,1]$ puis $[a,b]$ : densité, répartition, espérance, variance',11,'2, 4, 9'),
('P09','Exponentielle : densité, répartition, espérance et absence de mémoire',11,'3, 8, 10, 11'),
('S01','Nuage et point moyen ; ajustement affine et moindres carrés',12,'1, 3, 5, 8, 12'),
('S02','Corrélation, changement de variable, interpolation et extrapolation',12,'2, 4, 6, 7, 9, 10'),
('T01','Fonctions Python, conditions, boucles, listes et programmation modulaire',13,'1, 2, 5, 6, 8, 11'),
('T02','Ensembles, couples, connecteurs, négation, implication et réciproque',13,'3, 4, 7, 10'),
('T03','Quantification, contre-exemple, raisonnement et communication orale',13,'9, 12')
]
for code,desc,ch,ex in COVERAGE:
    CONCORDANCE+=rf'\noindent\textbf{{{code}}} · {desc}. \hyperref[chap-{ch}]{{Chapitre {ch}}}, exercices {ex}.\par\vspace{{1.6mm}}'+'\n'
CONCORDANCE+=r'''
\fiche{Neuf thèmes, neuf dossiers}{Mettre les connaissances en situation}
'''
for i,p in enumerate(PROJECTS,1):CONCORDANCE+=rf'\repere{{projet-{i}}}{{{p[1]} : {p[0]}}}'+'\n'
CONCORDANCE+=r'''
\souscours{Algorithmes proposés par le programme}
Termes récurrents et seuils : chapitres 1, 2 et 13. Balayage, dichotomie et Newton : chapitre 3.
Euler : chapitre 6. Rectangles, trapèzes et Monte-Carlo : chapitre 7 et dossier 4.
Coefficients binomiaux, cumuls et intervalles : chapitres 9 et 10. Simulation de Bernoulli, dé, géométrique, exponentielle et moyennes : chapitres 10 et 11, exercices associés et atelier ci-dessous.
Les exemples d'algorithmes et les pistes de problèmes du programme ne sont pas tous des exigences autonomes : la couverture des capacités est distinguée des prolongements.
\souscours{Démonstrations et histoire}
Somme géométrique : chapitre 1 ; identités et dérivée du logarithme : chapitre 2 ; primitives et équation différentielle : chapitre 6 ; lien aire/dérivée : chapitre 7 ; espérances uniforme et Bernoulli : chapitre 9 ; absence de mémoire : chapitre 11 ; moindres carrés : chapitre 12.
Les dossiers 3 et 4 relient les tables de logarithmes et les quadratures aux notions actuelles. Les travaux supplémentaires, notamment logistique ou Newton, sont guidés et distingués des connaissances exigibles.
\souscours{Évolution publiée pour septembre 2027}
Le nouveau programme de complémentaires, publié au BO n° 14 du 2 avril 2026, entre en application en 2027-2028. La comparaison des deux annexes retrouve les mêmes neuf thèmes et les mêmes grands blocs de contenus et capacités présentés ici. Le thème de corrélation propose aussi une concentration de médicament parmi les contextes possibles. Le préambule est réorganisé et le vocabulaire logique reste travaillé dans le manuel.
Cette édition est datée 2026-2027 : elle ne transforme pas les exemples possibles en obligations et n'anticipe pas des modalités d'évaluation non vérifiées.
\fiche{Atelier de simulation}{Compléter les algorithmes transversaux}
\begin{python}
from random import Random
from math import log, sqrt
rng = Random(2026)
def de():
    return 1 + int(6*rng.random())
def geometrique(p):
    k = 1
    while rng.random() >= p:
        k += 1
    return k
def exponentielle(taux):
    return -log(1-rng.random())/taux
def moyenne_des(n, repetitions):
    moyennes = [sum(de() for k in range(n))/n
                for j in range(repetitions)]
    m = sum(moyennes)/repetitions
    s = sqrt(sum((x-m)**2 for x in moyennes)/repetitions)
    seuil = 2*sqrt(35/12)/sqrt(n)
    proportion = sum(abs(x-3.5) <= seuil for x in moyennes)
    return m, s, proportion/repetitions
\end{python}
Utiliser $n\geq1$, un nombre de répétitions positif, $0<p\leq1$ et un taux strictement positif.
\code{de()} simule l'uniforme discrète à partir de l'uniforme continue. Pour une géométrique, on compte le premier succès ; pour une exponentielle, on inverse la fonction de répartition.
Comparer l'écart type simulé des moyennes à $\sqrt{35/12}/\sqrt n$ ; modifier le facteur $2$ en $3$ et commenter les proportions observées, sans les transformer en vérités exactes.
\fiche{Sources et repères éditoriaux}{Recherche vérifiée le 23 octobre 2026}
\begin{itemize}
\item Ministère, \href{https://www.education.gouv.fr/bo/19/Special8/MENE1921265A.htm}{arrêté du 19 juillet 2019 et annexe du programme de complémentaires}, BO spécial n° 8 du 25 juillet 2019.
\item Éduscol, \href{https://eduscol.education.gouv.fr/sites/default/files/document/spe265annexe1159134pdf-84162.pdf}{programme officiel en vigueur, 17 pages}.
\item Éduscol, \href{https://eduscol.education.gouv.fr/5817/programmes-et-ressources-en-mathematiques-voie-gt}{programmes et ressources en mathématiques, voie générale et technologique}, mise à jour juillet 2026.
\item Ministère, \href{https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2902920A}{arrêté du 26 février 2026, BO n° 14 du 2 avril 2026}, entrée en application en 2027-2028 et annexe comparée.
\item Mission Villani-Torossian, \href{https://eduscol.education.gouv.fr/sites/default/files/document/grilles-de-positionnement-des-livres-de-mathematiques-70116.pdf}{grilles de positionnement des livres de mathématiques}, mai 2019 : structuration, calcul, compétences, modélisation et démonstrations.
\end{itemize}
Les cours et exercices sont rédigés pour ce manuel à partir des attendus. Les dossiers et les évaluations sont des créations originales : ils ne sont pas des sujets officiels d'examen. Les chiffres contextualisés sont fictifs, sauf identité mathématique explicitement démontrée.
'''
INDEX=r'\fiche{Index des méthodes}{Accéder au bon outil}\phantomsection\label{index-methodes}\pdfbookmark[0]{Index}{index}'
for ch,title in [(1,'Suite affine, somme, limite et seuil'),(2,'Logarithme, domaine et demi-vie'),(3,'Asymptote, existence, unicité et dichotomie'),(4,'Dérivée, tangente, tableau et optimisation'),(5,'Convexité, inflexion et lecture de Lorenz'),(6,'Primitive, condition initiale et Euler'),(7,'Aire, moyenne, rectangles et Gini'),(8,'Arbre, Bayes et valeur prédictive'),(9,'Pascal, Bernoulli et cumul binomial'),(10,'Intervalle, fluctuation et décision'),(11,'Densité, répartition et temps d’attente'),(12,'Régression, résidu et corrélation'),(13,'Python, logique et contre-exemple')]:INDEX+=rf'\repere{{ess-{ch}}}{{{title}}}'+'\n'
