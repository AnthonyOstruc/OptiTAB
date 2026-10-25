"""Défis originaux : données éditoriales de l'édition française 2026-2027."""
DEFIS=[]
def defi(n,titre,chapitres,niveau,duree,enonce,corrige,indices,figures=None):
    DEFIS.append(dict(numero=n,titre=titre,chapitres=chapitres,niveau=niveau,duree=duree,
                      enonce=enonce.strip(),corrige=[x.strip() for x in corrige],
                      indices=indices,figures=figures or {}))

defi(1,'Deux racines dans un intervalle','1 et 13','Avancé','35 à 50 min',r'''
Pour $m\in\R$, on pose $P_m(x)=x^2-2mx+m$. On cherche les paramètres pour
lesquels $P_m$ possède \textbf{deux racines distinctes, toutes deux dans $]0;2[$}.
\begin{questions}
\item Calculer le discriminant. Pour quels $m$ existe-t-il deux racines distinctes ?
\item Montrer que deux racines dans $]0;2[$ imposent $P_m(0)>0$, $P_m(2)>0$
et que l'abscisse du sommet appartient à $]0;2[$.
\item Réciproquement, expliquer pourquoi ces trois conditions, ajoutées à un
discriminant strictement positif, suffisent. On peut s'aider de la parabole.
\item Déterminer tous les paramètres recherchés. Étudier les deux valeurs frontières.
\item Les seules conditions $P_m(0)>0$ et $P_m(2)>0$ suffisent-elles ? Donner un contre-exemple.
\end{questions}
La figure fournit des exemples pour conjecturer ; la réponse doit être démontrée.
''',[r'''
\editionEtape{1. Traduire la position des racines}
On calcule $\Delta=4m(m-1)$. Il y a deux racines distinctes si et seulement si
$m<0$ ou $m>1$. Le coefficient de $x^2$ est positif : la parabole est tournée vers le haut.
Si les deux racines $r_1<r_2$ sont dans $]0;2[$, les bornes 0 et 2 sont à l'extérieur
de l'intervalle entre les racines. On a donc
\[P_m(0)=m>0,\qquad P_m(2)=4-3m>0.\]
Le sommet a pour abscisse $(r_1+r_2)/2=m$, donc $0<m<2$.
\editionEtape{2. Justifier la réciproque}
Supposons $\Delta>0$, $P_m(0)>0$, $P_m(2)>0$ et $0<m<2$.
L'ordonnée du sommet vaut $m-m^2=-\Delta/4<0$. Sur $[0;m]$, la fonction
décroît d'une valeur positive à une valeur négative ; la première racine se trouve
donc entre 0 et $m$. De même, la seconde se trouve entre $m$ et 2.
On peut aussi utiliser les racines explicites $m\pm\sqrt{m(m-1)}$.
\editionEtape{3. Réunir les conditions}
Les conditions de signe donnent $0<m<4/3$, et $\Delta>0$ impose alors $m>1$.
La condition sur le sommet est automatiquement satisfaite. Ainsi
\[\res{m\in\left]1;\frac43\right[}.\]
Pour $m=1$, la racine 1 est double. Pour $m=4/3$, les racines sont $2/3$ et 2 :
la seconde est exclue du domaine demandé. Aucun des deux paramètres frontières ne convient.
\editionEtape{4. Repérer une condition insuffisante}
Pour $m=1/2$, $P_m(0)=1/2$ et $P_m(2)=5/2$ sont positifs, mais $\Delta=-1<0$ :
il n'existe aucune racine réelle.
\editionRetenir{Une liste de conditions nécessaires n'est pas encore une équivalence.
La réciproque doit être justifiée, puis les bornes du domaine doivent être contrôlées.}
'''],[
"Repérer le sommet et calculer la valeur du polynôme aux deux bornes.",
"Une parabole tournée vers le haut, positive aux bornes et négative à son sommet intérieur, coupe l'axe deux fois entre les bornes."
],{'enonce':['fr-d01']})

defi(2,'Le seuil d’une moyenne','2 et 12','Très exigeant','45 à 65 min',r'''
On définit $u_0=0$ et $u_{n+1}=\frac45u_n+60$ pour $n\geq0$.
Pour $n\geq1$, on note $S_n=\sum_{k=0}^{n-1}u_k$ et $A_n=S_n/n$.
\begin{questions}
\item À l'aide d'une suite auxiliaire géométrique, montrer que
$u_n=300\bigl(1-(4/5)^n\bigr)$. Étudier ses variations.
\item Calculer $S_n$, puis montrer que
$A_n=300-\frac{1500}{n}\bigl(1-(4/5)^n\bigr)$.
\item Expliquer pourquoi $A_n<u_n$, puis établir
$A_{n+1}-A_n=(u_n-A_n)/(n+1)$. En déduire les variations de $A_n$.
\item Écrire une fonction Python qui renvoie le premier $n\geq1$ tel que $A_n\geq240$.
Préciser ce que représentent les variables à chaque passage de la boucle.
\item Le programme conduit à $n=25$. Vérifier le seuil en calculant $A_{24}$ et $A_{25}$.
Pourquoi ces deux seuls contrôles suffisent-ils après la question 3 ?
\end{questions}
La moyenne porte sur les termes $u_0$ à $u_{n-1}$ : elle ne comprend pas $u_n$.
''',[r'''
\editionEtape{1. Déplacer le point fixe}
Le nombre 300 vérifie $300=(4/5)300+60$. En posant $v_n=u_n-300$,
on obtient $v_{n+1}=(4/5)v_n$ et $v_0=-300$.
Ainsi $u_n=300-300(4/5)^n$. La puissance $(4/5)^n$ décroît strictement :
$u_n$ croît strictement, reste inférieur à 300 et commence à 0.
\editionEtape{2. Additionner le bon nombre de termes}
Il y a $n$ termes, des indices 0 à $n-1$. La somme géométrique donne
\[S_n=300n-300\frac{1-(4/5)^n}{1-4/5}
=300n-1500\bigl(1-(4/5)^n\bigr).\]
En divisant par $n>0$, on obtient l'expression demandée de $A_n$.
\editionEtape{3. Comparer une moyenne au terme suivant}
Chacun des $n$ termes $u_0,\ldots,u_{n-1}$ est strictement inférieur à $u_n$.
Leur moyenne vérifie donc $A_n<u_n$.
Comme $S_{n+1}=S_n+u_n=nA_n+u_n$,
\[A_{n+1}-A_n=\frac{nA_n+u_n}{n+1}-A_n
=\frac{u_n-A_n}{n+1}>0.\]
La suite des moyennes est strictement croissante.
\editionRetenir{Pour étudier une moyenne de termes successifs, ajouter le nouveau terme
à la somme est souvent plus simple que soustraire deux formules compliquées.}
''',r'''
\editionEtape{4. Programmer sans décaler les indices}
\begin{python}
def seuil_moyenne():
    n = 1
    u = 60.0
    total = 0.0
    while total / n < 240:
        total = total + u
        u = 0.8 * u + 60
        n = n + 1
    return n
\end{python}
Au test de boucle, \code{total} est $S_n$ et \code{u} est $u_n$.
Au départ, $S_1=u_0=0$ et $u_1=60$. On ajoute $u_n$ à la somme,
puis on prépare $u_{n+1}$ et on augmente $n$ : les trois variables restent cohérentes.
La fonction renvoie \res{25}.
\editionEtape{5. Valider le premier franchissement}
Avec la formule exacte de la première page,
\[A_{24}\approx237{,}795\quad\text{et}\quad A_{25}\approx240{,}227.\]
Ainsi $A_{24}<240\leq A_{25}$. La croissance stricte prouve que tous les rangs
antérieurs à 25 échouent : il ne suffit pas d'obtenir une valeur qui dépasse le seuil,
il faut aussi justifier qu'elle est la première.
\editionRetenir{Le programme repère le rang candidat. La formule et la monotonie
expliquent pourquoi ce candidat répond exactement à la question.}
'''],[
"Chercher le point fixe de la relation affine, puis soustraire ce nombre à chaque terme.",
r"Pour la moyenne, utiliser $S_{n+1}=S_n+u_n$. Au test de boucle, conserver simultanément le rang, la somme $S_n$ et le terme $u_n$."
])

defi(3,'Trois tangentes par un point','3, 4 et 1','Très exigeant','55 à 75 min',r'''
On considère $f(x)=x^3-3x$. Pour $t\in[-1;2]$, on note $T_t$ la tangente
à sa courbe au point d'abscisse $t$. Pour $b\in\R$, on pose $P_b(1;b)$.
\begin{questions}
\item Montrer que $T_t$ a pour équation $y=(3t^2-3)x-2t^3$.
\item Montrer que $T_t$ passe par $P_b$ si et seulement si $g(t)=b$,
où $g(t)=-2t^3+3t^2-3$.
\item Étudier $g$ sur $[-1;2]$ et calculer ses valeurs aux bornes et aux points critiques.
\item Selon $b$, déterminer le nombre de tangentes $T_t$ qui passent par $P_b$.
Soigner les cas où $b$ est une valeur extrême ou une valeur frontière.
\item Pour $b=-5/2$, factoriser $4t^3-6t^2+1$ et déterminer les trois
abscisses de contact, puis les équations des trois tangentes.
\end{questions}
Seules les tangentes dont l'abscisse de contact est dans $[-1;2]$ sont comptées.
''',[r'''
\editionEtape{1. Remplacer une question géométrique par une équation}
Comme $f'(t)=3t^2-3$, la formule de la tangente donne
\[y=f'(t)(x-t)+f(t)=(3t^2-3)x-2t^3.\]
En prenant $x=1$, son ordonnée vaut $g(t)=-2t^3+3t^2-3$.
Chercher les tangentes passant par $P_b$ revient donc à compter les solutions de $g(t)=b$.
\editionEtape{2. Compter les intersections avec une horizontale}
On a $g'(t)=6t(1-t)$. Ainsi $g$ décroît sur $[-1;0]$, croît sur $[0;1]$
et décroît sur $[1;2]$, avec
\[g(-1)=2,\quad g(0)=-3,\quad g(1)=-2,\quad g(2)=-7.\]
\begin{center}\begin{tabular}{@{}lc@{}}\toprule
Valeur de $b$ & Nombre de tangentes\\\midrule
$b<-7$ ou $b>2$ & $0$\\
$-7\leq b<-3$ ou $-2<b\leq2$ & $1$\\
$b=-3$ ou $b=-2$ & $2$\\
$-3<b<-2$ & $3$\\\bottomrule\end{tabular}\end{center}
À une valeur critique, deux branches du tableau aboutissent au \emph{même} point :
ce point ne doit être compté qu'une fois.
Des paramètres distincts donnent ici des droites distinctes : si deux tangentes avaient
le même terme constant $-2t^3$, leurs paramètres seraient égaux.
''',r'''
\editionEtape{3. Trouver exactement les trois tangentes}
Pour $b=-5/2$, l'équation devient $4t^3-6t^2+1=0$.
Le nombre $1/2$ est racine et
\[4t^3-6t^2+1=(2t-1)(2t^2-2t-1).\]
Les trois abscisses de contact sont
\[\res{\frac{1-\sqrt3}{2},\quad\frac12,\quad\frac{1+\sqrt3}{2}}.\]
Elles appartiennent bien à $[-1;2]$. Pour $t=1/2$, la pente vaut $-9/4$.
Pour les deux autres valeurs, $t^2=t+1/2$, donc la pente vaut $3t-3/2=\pm3\sqrt3/2$.
Toutes les droites passent par $(1;-5/2)$ ; leurs équations sont donc
\[\res{y=-\frac94x-\frac14},\qquad
y=\frac{3\sqrt3}{2}(x-1)-\frac52,\qquad
y=-\frac{3\sqrt3}{2}(x-1)-\frac52.\]
\editionRetenir{Le paramètre de la tangente est une abscisse de contact.
Une droite horizontale dans le graphique de $g$ permet de compter les tangentes dans le graphique de $f$.}
'''],[
"Écrire la tangente au point d'abscisse t avant de remplacer x par 1.",
"Pour compter les solutions, utiliser les trois intervalles de monotonie de g et traiter séparément les hauteurs -3 et -2."
],{'enonce':['fr-d03'],'corrige_2':['fr-d03']})

defi(4,'La fenêtre la plus lumineuse','1 et 4','Avancé','35 à 50 min',r'''
Une fenêtre est formée d'un rectangle de largeur $2r$ et de hauteur $h$, surmonté
d'un demi-disque de rayon $r$. La longueur totale de son \textbf{contour extérieur} est de 20 m.
On suppose $r>0$ et $h>0$ et on veut maximiser l'aire vitrée.
\begin{questions}
\item Exprimer le périmètre. Pourquoi le diamètre commun au rectangle et au demi-disque
ne doit-il pas être ajouté au contour extérieur ?
\item Exprimer $h$ en fonction de $r$ et préciser exactement le domaine admissible.
\item Montrer que l'aire est $A(r)=20r-(2+\pi/2)r^2$.
\item Déterminer les dimensions optimales et l'aire maximale, sous forme exacte.
Quelle relation simple lie $h$ et $r$ à l'optimum ?
\item Expliquer pourquoi le maximum calculé correspond à une vraie fenêtre et non à une forme dégénérée.
\end{questions}
''',[r'''
\editionEtape{1. Modéliser le contour avant de calculer}
Le contour comprend la base $2r$, deux côtés $h$ et le demi-cercle $\pi r$.
Le segment séparant les deux parties est intérieur. Ainsi
\[2h+(2+\pi)r=20,\qquad h=10-\frac{2+\pi}{2}r.\]
Les contraintes donnent $0<r<20/(2+\pi)$.
\editionEtape{2. Réduire à une seule variable}
L'aire est celle du rectangle plus celle du demi-disque :
\[A(r)=2rh+\frac{\pi r^2}{2}=20r-\frac{4+\pi}{2}r^2.\]
C'est un trinôme de coefficient dominant négatif. Sa dérivée vaut
$A'(r)=20-(4+\pi)r$ : elle est positive avant $r_*=20/(4+\pi)$ et négative après.
\editionEtape{3. Contrôler et interpréter l'optimum}
Le rayon $r_*$ appartient au domaine, puisque $4+\pi>2+\pi$.
En remplaçant dans la formule de $h$,
\[\res{r_*=h_*=\frac{20}{4+\pi}\ \mathrm{m}},\qquad
\res{A_{\max}=\frac{200}{4+\pi}\ \mathrm{m}^2}.\]
La largeur vaut $40/(4+\pi)$ m. Les deux dimensions sont strictement positives :
le maximum est atteint à l'intérieur du domaine géométrique.
\editionRetenir{Un bon modèle distingue le contour extérieur des segments intérieurs.
Après l'optimisation, revenir aux dimensions et aux unités donne son sens au résultat.}
'''],[
"Tracer au crayon uniquement le contour extérieur ; sa longueur est la somme de quatre morceaux.",
"Éliminer h avec le périmètre, puis optimiser le trinôme en r."
],{'enonce':['fr-d04'],'corrige_1':['fr-d04']})

defi(5,'Encadrer sans logarithme','5, 2 et 12','Très exigeant','45 à 60 min',r'''
On veut encadrer $e^{1/2}$ avec des puissances de nombres rationnels.
\begin{questions}
\item Étudier $F(x)=e^x-1-x$ sur $\R$ et montrer que $e^x\geq1+x$,
avec égalité seulement pour $x=0$.
\item Pour $0<t<1$, appliquer ce résultat à $-t$, puis justifier
$1+t<e^t<1/(1-t)$.
\item Pour tout entier $n\geq1$, en déduire
\[L_n=\left(1+\frac1{2n}\right)^n<e^{1/2}<
U_n=\left(1-\frac1{2n}\right)^{-n}.\]
\item Programmer le calcul de $L_n$ et $U_n$, puis donner des encadrements
pour $n=10$, $100$ et $1000$. Arrondir la borne inférieure vers le bas et la borne supérieure vers le haut.
\item Que prouve l'encadrement théorique ? Que ne suffit pas à prouver la seule observation des décimales calculées ?
\end{questions}
On utilise uniquement les propriétés de l'exponentielle ; le logarithme n'est pas nécessaire.
''',[r'''
\editionEtape{1. Établir une inégalité valable sur tout le domaine}
La dérivée $F'(x)=e^x-1$ est négative pour $x<0$, nulle en 0 et positive pour $x>0$.
Ainsi $F$ admet son minimum $F(0)=0$. Il vient $e^x\geq1+x$, et l'égalité
n'est possible qu'en 0.
\editionEtape{2. Inverser sans changer le sens à tort}
Pour $0<t<1$, l'inégalité stricte donne $e^t>1+t$ et $e^{-t}>1-t>0$.
Sur les nombres strictement positifs, prendre les inverses renverse l'ordre :
$e^t<1/(1-t)$. La positivité de $1-t$ est indispensable.
\editionEtape{3. Passer aux puissances entières}
On prend $t=1/(2n)$, qui est dans $]0;1[$. Les trois quantités sont positives ;
la puissance entière $n$ conserve donc les inégalités. Comme $(e^{1/(2n)})^n=e^{1/2}$,
on obtient $L_n<e^{1/2}<U_n$.
\editionRetenir{Pour produire un encadrement, combiner une inégalité générale
avec des opérations dont le sens et le domaine sont explicitement contrôlés.}
''',r'''
\editionEtape{4. Calculer et arrondir dans le bon sens}
\begin{python}
def bornes_exponentielle(n):
    bas = (1 + 1 / (2 * n)) ** n
    haut = (1 - 1 / (2 * n)) ** (-n)
    return bas, haut
\end{python}
Des arrondis extérieurs à cinq décimales donnent :
\begin{center}\begin{tabular}{@{}ccc@{}}\toprule
$n$ & Borne inférieure & Borne supérieure\\\midrule
10 & $1{,}62889$ & $1{,}67019$\\
100 & $1{,}64666$ & $1{,}65080$\\
1000 & $1{,}64851$ & $1{,}64893$\\\bottomrule\end{tabular}\end{center}
Chaque ligne enferme $e^{1/2}$. Un arrondi usuel au plus proche pourrait
déplacer une borne vers l'intérieur ; c'est pourquoi on arrondit ici volontairement vers l'extérieur.
\editionEtape{5. Distinguer preuve et observation}
La preuve garantit l'encadrement \emph{pour chaque entier} $n\geq1$.
Les calculs suggèrent qu'il se resserre. À eux seuls, quelques essais ne démontrent
ni une propriété pour tous les rangs, ni une convergence.
La fonction Python travaille en nombres approchés : pour certifier une précision arbitraire,
on utiliserait des calculs rationnels ou des bornes d'erreur adaptées.
\editionRetenir{Le calcul numérique illustre une preuve ; il ne remplace pas
le contrôle du sens des inégalités et des arrondis.}
'''],[
r"Étudier le signe de la dérivée de $e^x-1-x$.",
r"Pour la majoration, remplacer $x$ par $-t$ et inverser deux nombres positifs. Puis prendre $t=1/(2n)$."
])

defi(6,'Additionner sinus et cosinus','6, 1 et 8','Très exigeant','45 à 65 min',r'''
Pour $t\in[0;2\pi[$, on pose $x=\cos t$, $y=\sin t$. On cherche à résoudre
$\cos t+\sin t=k$, où $k$ est un paramètre réel.
\begin{questions}
\item Traduire le problème comme une intersection entre un cercle et une droite.
\item En utilisant $(x-y)^2\geq0$, montrer que $-\sqrt2\leq x+y\leq\sqrt2$.
\item Lorsque $x+y=k$, montrer que $xy=(k^2-1)/2$, puis que $x$ et $y$
sont les racines de $X^2-kX+(k^2-1)/2=0$.
\item Classer le nombre de solutions $t$ selon $k$. Donner les coordonnées des points correspondants.
\item Résoudre explicitement pour $k=0$, $k=1$ et $k=\sqrt2$.
\end{questions}
L'intervalle est ouvert en $2\pi$ pour ne pas compter deux fois le même point du cercle.
''',[r'''
\editionEtape{1. Changer de représentation}
Les coordonnées vérifient $x^2+y^2=1$ ; l'autre condition est la droite $x+y=k$.
De $(x-y)^2\geq0$, on déduit $2xy\leq1$, puis
$(x+y)^2=1+2xy\leq2$. Il faut donc $|k|\leq\sqrt2$.
\editionEtape{2. Reconstruire les coordonnées}
En développant $k^2=(x+y)^2$, on trouve $xy=(k^2-1)/2$.
Le trinôme dont les racines sont $x$ et $y$ a pour discriminant $2-k^2$.
Pour $|k|\leq\sqrt2$, les points cherchés ont pour coordonnées
\[\left(\frac{k+\sqrt{2-k^2}}2;\frac{k-\sqrt{2-k^2}}2\right)
\quad\text{et}\quad
\left(\frac{k-\sqrt{2-k^2}}2;\frac{k+\sqrt{2-k^2}}2\right).\]
Ces couples vérifient bien les deux équations ; la condition est donc suffisante.
Si $|k|<\sqrt2$, les deux points sont distincts : il existe deux solutions $t$.
Si $k=\pm\sqrt2$, les deux couples coïncident : une solution.
Si $|k|>\sqrt2$, aucune solution.
\editionRetenir{Une condition nécessaire devient une caractérisation seulement
après avoir vérifié que les coordonnées construites satisfont les équations de départ.}
''',r'''
\editionEtape{3. Revenir aux angles remarquables}
Pour $k=0$, on a $y=-x$ et les points
$(-\sqrt2/2;\sqrt2/2)$ et $(\sqrt2/2;-\sqrt2/2)$ :
\[\res{t\in\{3\pi/4;7\pi/4\}}.\]
Pour $k=1$, les coordonnées sont $(1;0)$ et $(0;1)$, donc
\[\res{t\in\{0;\pi/2\}}.\]
Pour $k=\sqrt2$, il n'y a qu'un point, $(\sqrt2/2;\sqrt2/2)$, donc
\[\res{t=\pi/4}.\]
Pour une valeur générale de $k$, les coordonnées exactes suffisent à décrire les points :
on ne suppose pas que leurs angles soient des angles remarquables.
\editionRetenir{Les points du cercle et les angles ne sont pas des réponses interchangeables :
préciser le domaine de l'angle permet de compter correctement les solutions.}
'''],[
r"Dans le repère, écrire $x^2+y^2=1$ et $x+y=k$.",
r"Calculer le produit $xy$ grâce au carré de la somme, puis utiliser un trinôme de somme $k$ et de produit $(k^2-1)/2$."
],{'enonce':['fr-d06'],'corrige_2':['fr-d06']})

defi(7,'Un triangle sous deux contraintes','7 et 8','Très exigeant','40 à 60 min',r'''
Dans un repère orthonormé, $A(-2;0)$, $B(2;0)$ et $M(x;y)$ vérifient
\[\vect{MA}\cdot\vect{MB}=0,\qquad MA^2+2MB^2=k.\]
Le paramètre $k$ est réel.
\begin{questions}
\item Montrer que la première condition équivaut à $x^2+y^2=4$.
\item Sous cette condition, établir $MA^2=8+4x$ et $MB^2=8-4x$.
\item En déduire les coordonnées possibles de $M$ en fonction de $k$ et discuter leur nombre.
\item Pour quels $k$ obtient-on un \textbf{vrai triangle} $AMB$ rectangle en $M$ ?
Pourquoi les valeurs frontières doivent-elles être exclues ?
\item Pour quel $k$ le triangle est-il aussi isocèle en $M$ ? Donner ses deux sommets possibles.
\end{questions}
''',[r'''
\editionEtape{1. Reconnaître le lieu d'orthogonalité}
Les vecteurs sont $(-2-x;-y)$ et $(2-x;-y)$ ; leur produit scalaire vaut
$x^2+y^2-4$. Le lieu est le cercle de centre $O$ et de rayon 2, de diamètre $[AB]$.
Sur ce cercle, $MA^2=(x+2)^2+y^2=8+4x$ et $MB^2=8-4x$.
\editionEtape{2. Réduire le second lieu à une droite}
La seconde condition devient $24-4x=k$, donc $x=6-k/4$.
Il reste
\[y^2=4-\left(6-\frac k4\right)^2.\]
Cette quantité est positive si $16<k<32$, nulle si $k=16$ ou $32$, négative sinon.
Il existe donc deux points pour $16<k<32$ :
\[\res{M\left(6-\frac k4;\ \pm\sqrt{4-(6-k/4)^2}\right)}.\]
Aux bornes, un seul point subsiste : $B$ pour $k=16$, $A$ pour $k=32$.
Hors de $[16;32]$, aucun point ne convient.
\editionEtape{3. Séparer orthogonalité et angle d'un triangle}
En $A$ ou en $B$, l'un des vecteurs est nul. Son produit scalaire avec l'autre est nul,
mais le triangle est dégénéré : l'angle demandé n'existe pas.
Les vrais triangles correspondent exactement à \res{16<k<32}.
Enfin $MA=MB$ équivaut à $x=0$, d'où \res{k=24} et \res{M(0;2)\text{ ou }M(0;-2)}.
\editionRetenir{Un produit scalaire nul autorise un vecteur nul. Pour conclure sur
un angle droit, vérifier que les trois sommets forment effectivement un triangle.}
'''],[
"Développer le produit scalaire en coordonnées avant de reconnaître un cercle.",
r"Sur ce cercle, remplacer $x^2+y^2$ par 4 dans les carrés des distances. Le second lieu devient une droite verticale."
],{'enonce':['fr-d07'],'corrige_1':['fr-d07']})

defi(8,'Une famille de cercles tangents','8, 7 et 1','Très exigeant','55 à 75 min',r'''
Pour $m\in\R$, on considère $\mathcal C_m$ d'équation
$x^2+y^2-4x-2my=0$ et la droite $d:x+y=6$.
\begin{questions}
\item Déterminer le centre et le rayon de $\mathcal C_m$. Montrer que tous
ces cercles passent par $A(0;0)$ et $B(4;0)$.
\item Substituer $y=6-x$ dans l'équation du cercle. Montrer que le discriminant
de l'équation obtenue est $4(m^2+8m-8)$.
\item Classer, selon $m$, le nombre de points communs à $d$ et $\mathcal C_m$.
Pour quels paramètres y a-t-il tangence ?
\item On note $\Omega_m(2;m)$. Calculer son projeté orthogonal $H_m$ sur $d$.
Vérifier, pour chacun des paramètres de tangence, que $H_m$ appartient au cercle.
\item Expliquer pourquoi la droite $d$ est alors perpendiculaire au rayon au point de contact.
\end{questions}
La figure de l'énoncé représente seulement les points fixes et la droite ; les cercles restent à déterminer.
''',[r'''
\editionEtape{1. Identifier les cercles sans oublier le rayon}
On complète les carrés :
\[(x-2)^2+(y-m)^2=4+m^2.\]
Le centre est $\Omega_m(2;m)$ et le rayon $\sqrt{4+m^2}$, strictement positif pour tout $m$.
Les points $(0;0)$ et $(4;0)$ vérifient l'équation initiale, quel que soit $m$.
\editionEtape{2. Compter les intersections par le discriminant}
Après substitution,
\[2x^2+(2m-16)x+36-12m=0.\]
Son discriminant vaut
\[(2m-16)^2-8(36-12m)=4\bigl((m+4)^2-24\bigr).\]
Posons $m_-=-4-2\sqrt6$ et $m_+=-4+2\sqrt6$.
Il existe deux intersections si $m<m_-$ ou $m>m_+$, aucune si $m_-<m<m_+$,
et une seule si $m=m_-$ ou $m=m_+$.
Les deux paramètres de tangence sont donc \res{m=-4\pm2\sqrt6}.
\editionEtape{3. Trouver le point de contact par projection}
Un vecteur normal à $d$ est $(1;1)$. Le projeté est de la forme
$H_m=(2-\lambda;m-\lambda)$. La condition $x_H+y_H=6$ donne
$\lambda=(m-4)/2$, donc
\[\res{H_m\left(4-\frac m2;2+\frac m2\right)}.\]
''',r'''
\editionEtape{4. Vérifier les deux constructions}
La distance au carré entre le centre et son projeté est
\[\Omega_mH_m^2=\frac{(m-4)^2}{2}.\]
Pour $m=m_-$ ou $m=m_+$, l'identité $m^2+8m-8=0$ entraîne
$(m-4)^2/2=m^2+4$. La distance au centre est donc égale au rayon : le projeté
appartient bien au cercle. Ses coordonnées explicites sont
\[H_-\bigl(6+\sqrt6;-\sqrt6\bigr),\qquad
H_+\bigl(6-\sqrt6;\sqrt6\bigr).\]
Le vecteur $\vect{\Omega_mH_m}$ est un multiple de $(1;1)$ : il est normal à $d$.
C'est donc le rayon perpendiculaire à la tangente au point de contact.
\editionRetenir{Le discriminant compte les intersections ; la projection construit
le point de contact. Faire concorder les deux démarches fournit une vérification indépendante.}
'''],[
r"Compléter deux carrés, puis remplacer $y$ par $6-x$ pour obtenir un trinôme en $x$.",
r"Pour projeter le centre, se déplacer dans la direction du vecteur normal $(1;1)$ jusqu'à satisfaire $x+y=6$."
],{'enonce':['fr-d08-ex'],'corrige_2':['fr-d08-cor']})

defi(9,'Choisir une règle de contrôle','9 et 10','Très exigeant','55 à 75 min',r'''
Dans un modèle fictif, $10\,\%$ des articles présentent un défaut $D$.
On applique deux tests $T_1$ et $T_2$, de résultat positif $+$ ou négatif $-$.
Sur les articles défectueux, chaque test est positif avec probabilité $0{,}9$ ;
sur les autres, avec probabilité $0{,}2$.
\textbf{Dans chacun de ces deux groupes}, le résultat du second test a les mêmes
probabilités quel que soit le résultat du premier.
\begin{questions}
\item Compléter l'arbre à trois niveaux. Les deux tests sont-ils pour autant
indépendants dans la population entière ? Comparer $P(T_1^+\cap T_2^+)$ à $P(T_1^+)P(T_2^+)$.
\item Calculer la probabilité du défaut sachant qu'un test est positif,
puis sachant que les deux sont positifs.
\item La règle U écarte un article dès qu'au moins un test est positif.
La règle B ne l'écarte que si les deux sont positifs. Pour un article choisi dans toute la production,
calculer, pour chaque règle, $P(\overline D\text{ et rejet})$ et $P(D\text{ et acceptation})$.
\item Le premier type d'erreur coûte 1 unité, le second $\lambda$ unités, avec $\lambda\geq0$.
Comparer les coûts moyens des deux règles selon $\lambda$.
\end{questions}
''',[r'''
\editionEtape{1. Respecter la population conditionnante}
Dans le groupe $D$, le chemin $++$ a pour poids $0{,}9^2=0{,}81$ ; dans le groupe
$\overline D$, son poids est $0{,}2^2=0{,}04$.
En ajoutant les deux origines, $P(T_1^+\cap T_2^+)=0{,}1(0{,}81)+0{,}9(0{,}04)=0{,}117$.
Chaque test a une probabilité marginale $0{,}1(0{,}9)+0{,}9(0{,}2)=0{,}27$ d'être positif.
Or $0{,}27^2=0{,}0729\ne0{,}117$ : les tests ne sont pas indépendants dans la population entière.
\editionEtape{2. Inverser le conditionnement}
Pour un seul test positif, la part de défauts est
\[\frac{P(D\cap T_1^+)}{P(T_1^+)}=\frac{0{,}09}{0{,}27}=\res{\frac13}.\]
Pour deux tests positifs, elle devient
\[\frac{P(D\cap T_1^+\cap T_2^+)}{P(T_1^+\cap T_2^+)}
=\frac{0{,}081}{0{,}117}=\res{\frac9{13}}.\]
\editionRetenir{Des poids identiques au second test dans chaque groupe ne donnent
pas automatiquement l'indépendance dans le mélange des groupes.}
''',r'''
\editionEtape{3. Compter les deux erreurs séparément}
Pour U, on rejette un article sans défaut sauf si les deux tests sont négatifs :
$P(\overline D\text{ et rejet})=0{,}9(1-0{,}8^2)=0{,}324$.
Un défaut passe seulement par le chemin $D--$, de poids $0{,}1(0{,}1^2)=0{,}001$.
Pour B, les erreurs ont les probabilités $0{,}9(0{,}2^2)=0{,}036$ et
$0{,}1(1-0{,}9^2)=0{,}019$.
\editionEtape{4. Comparer des espérances, pas seulement des pourcentages}
Les coûts moyens valent
\[C_U=0{,}324+0{,}001\lambda,\qquad C_B=0{,}036+0{,}019\lambda.\]
Leur différence est $C_U-C_B=0{,}288-0{,}018\lambda$.
Pour $0\leq\lambda<16$, B coûte moins ; pour $\lambda>16$, U coûte moins ;
pour $\lambda=16$, les coûts sont égaux.
Par exemple, pour $\lambda=5$, on obtient $C_U=0{,}329$ et $C_B=0{,}131$.
\editionRetenir{La règle qui détecte le plus de défauts n'est pas nécessairement
celle qui minimise un coût donné. Le choix dépend du modèle et des conséquences des deux erreurs.}
'''],[
"Commencer par séparer les groupes D et son complément ; multiplier ensuite les poids des deux tests à l'intérieur de chaque groupe.",
"Pour U, le seul chemin accepté réunit deux tests négatifs. Pour comparer les règles, calculer une différence de deux fonctions affines du coût d'erreur."
],{'enonce':['fr-d09'],'corrige_1':['fr-d09']})

defi(10,'Même moyenne, objectifs différents','10 et 1','Très exigeant','40 à 60 min',r'''
Un jeu présente trois issues $I_1,I_2,I_3$ de probabilités $1/4,1/2,1/4$.
Pour un paramètre $a\in[0;2]$, le lot brut $L_a$ vaut respectivement
$2a$, $2-a$ et $6$ unités. Le prix d'entrée est $5/2$ ; le gain net est $G_a=L_a-5/2$.
\begin{questions}
\item Donner la loi issue par issue de $L_a$ et calculer son espérance.
À quelle valeur de $a$ deux lots coïncident-ils ? Comment regrouper alors les probabilités ?
\item Calculer $E(G_a)$ et montrer que
$V(G_a)=\frac32a^2-2a+\frac{19}{4}$.
\item Déterminer le paramètre qui minimise cette variance et la valeur minimale.
\item Calculer la probabilité $P(G_a>0)$ selon $a$, en traitant le seuil d'égalité.
Le choix de variance minimale maximise-t-il la probabilité de gagner strictement ?
\item Pour une prévision réelle $r$, développer $E((L_a-r)^2)$.
Déterminer simultanément les valeurs de $a$ et $r$ qui minimisent cette erreur quadratique moyenne.
\end{questions}
''',[r'''
\editionEtape{1. Séparer les issues et les valeurs}
Les trois issues ont pour lots $2a$, $2-a$ et 6. Les deux premiers coïncident
pour $a=2/3$ ; on regroupe alors leurs probabilités en $3/4$.
Dans tous les cas,
\[E(L_a)=\frac14(2a)+\frac12(2-a)+\frac14(6)=\frac52,\qquad \res{E(G_a)=0}.\]
\editionEtape{2. Optimiser la dispersion}
On calcule $E(L_a^2)=a^2+(2-a)^2/2+9=3a^2/2-2a+11$.
Soustraire le carré $25/4$ de la moyenne donne
\[V(G_a)=V(L_a)=\frac32\left(a-\frac23\right)^2+\frac{49}{12}.\]
Le minimum est donc \res{49/12}, atteint uniquement en \res{a=2/3}.
\editionEtape{3. Changer d'objectif peut changer la réponse}
Le deuxième gain net vaut $-a-1/2<0$ ; le troisième vaut $7/2>0$.
Le premier, $2a-5/2$, est strictement positif seulement si $a>5/4$.
Ainsi $P(G_a>0)=1/4$ sur $[0;5/4]$ et $1/2$ sur $]5/4;2]$.
Le choix $a=2/3$ ne maximise donc pas cette probabilité.
\editionEtape{4. Choisir aussi la prévision}
En développant et en utilisant $E(L_a)=5/2$,
\[E((L_a-r)^2)=V(L_a)+(r-5/2)^2.
\]
Les deux carrés sont minimaux pour \res{a=2/3\text{ et }r=5/2}.
\editionRetenir{Espérance, variance, chance de gain et erreur de prévision répondent
à des questions différentes. Une moyenne identique ne suffit pas à départager deux choix.}
'''],[
"Calculer d'abord l'espérance et le deuxième moment avec les probabilités des issues, même si deux lots coïncident.",
"Mettre la variance sous forme canonique ; pour le gain strictement positif, traiter les trois issues une à une."
],{'enonce':['fr-d10'],'corrige_1':['fr-d10']})

defi(11,'La dispersion d’un groupe réuni','11 et 1','Très exigeant','45 à 65 min',r'''
Le groupe A contient les valeurs 0 et 2 ; le groupe B contient 8 et 10.
La variance d'une série est la moyenne des carrés des écarts à sa moyenne.
\begin{questions}
\item Calculer les moyennes et variances des deux groupes, puis de leur réunion.
Pourquoi la variance de la réunion n'est-elle pas la moyenne des deux variances ?
\item Plus généralement, deux groupes ont des tailles $n_A,n_B>0$, des moyennes
$\mu_A,\mu_B$ et des variances $V_A,V_B$. Poser $p=n_A/(n_A+n_B)$ et exprimer
la moyenne $\mu$ de leur réunion.
\item Dans le groupe A, développer
$(x-\mu)^2=((x-\mu_A)+(\mu_A-\mu))^2$ puis moyenner.
Que devient le terme croisé ? Faire de même dans B.
\item En déduire la formule
\[V=pV_A+(1-p)V_B+p(1-p)(\mu_A-\mu_B)^2.\]
\item Deux groupes ont chacun une variance égale à 1. La variance de leur réunion
peut-elle être aussi grande que l'on veut ? Construire un exemple avec deux groupes de même taille.
\end{questions}
''',[r'''
\editionEtape{1. Calculer un exemple qui oblige à changer d'idée}
Dans A, $\mu_A=1$ et $V_A=1$ ; dans B, $\mu_B=9$ et $V_B=1$.
La réunion est $0,2,8,10$, de moyenne 5. Sa variance vaut
\[V=\frac{25+9+9+25}{4}=\res{17}.\]
La moyenne des variances internes vaut seulement 1. Elle ignore l'écart entre les centres des deux groupes.
\editionEtape{2. Décomposer les écarts à la moyenne totale}
La moyenne totale est $\mu=p\mu_A+(1-p)\mu_B$.
Dans A, la moyenne de $x-\mu_A$ est nulle. Le terme croisé du développement
s'annule donc après la moyenne :
\[\text{moyenne dans A de }(x-\mu)^2=V_A+(\mu_A-\mu)^2.\]
Dans B, on obtient $V_B+(\mu_B-\mu)^2$.
Les écarts des moyennes au centre total sont
\[\mu_A-\mu=(1-p)(\mu_A-\mu_B),\qquad
\mu_B-\mu=-p(\mu_A-\mu_B).\]
''',r'''
\editionEtape{3. Réunir en pondérant par les effectifs}
Une proportion $p$ des observations vient de A ; l'autre vient de B. Ainsi
\begin{align*}
V&=pV_A+(1-p)V_B+p(\mu_A-\mu)^2+(1-p)(\mu_B-\mu)^2\\
 &=pV_A+(1-p)V_B+p(1-p)\bigl((1-p)+p\bigr)(\mu_A-\mu_B)^2.
\end{align*}
On retrouve la formule demandée. Le dernier terme est positif ou nul et s'annule
quand les deux moyennes sont égales.
Pour l'exemple, $p=1/2$ et l'écart des moyennes vaut 8 : $V=1+8^2/4=17$.
\editionEtape{4. Construire une famille de contre-exemples}
Prenons A $=\{-1;1\}$ et B $=\{M-1;M+1\}$, avec $M>0$.
Chaque groupe a une variance égale à 1 ; leurs moyennes sont 0 et $M$.
La réunion a donc pour variance
\[\res{V=1+\frac{M^2}{4}}.\]
En choisissant $M$ suffisamment grand, cette variance dépasse n'importe quelle borne fixée.
\editionRetenir{Une dispersion totale associe la dispersion à l'intérieur des groupes
et la séparation de leurs moyennes. Les effectifs déterminent les pondérations.}
'''],[
"Dans le calcul de la variance réunie, tous les écarts doivent être mesurés à la même moyenne totale.",
"La moyenne des écarts à la moyenne d'un groupe est nulle ; c'est ce qui annule le terme croisé du développement."
],{'enonce':['fr-d11'],'corrige_2':['fr-d11']})

defi(12,'Un algorithme qui encadre une racine','12, 3 et 4','Très exigeant','45 à 60 min',r'''
On pose $f(x)=x^3+x-1$. \textbf{On admet l'existence} d'une solution $\alpha$ de
$f(x)=0$ dans $[0;1]$ ; il ne s'agit pas ici de démontrer un théorème de continuité.
\begin{questions}
\item Justifier que cette solution est unique.
\item On part de $a=0$, $b=1$, puis on calcule $m=(a+b)/2$.
Si $f(m)<0$, on remplace $a$ par $m$ ; sinon, on remplace $b$ par $m$.
Expliquer pourquoi $a\leq\alpha\leq b$ reste vrai après cette étape.
\item Écrire une fonction qui réalise exactement $N$ étapes et renvoie les deux bornes.
Préciser les entrées autorisées.
\item Montrer que la largeur finale vaut $2^{-N}$.
Quel est le plus petit $N$ qui garantit une largeur au plus $10^{-3}$ ?
\item Pour $N=10$, vérifier l'encadrement exact
$698/1024\leq\alpha\leq699/1024$ en étudiant les signes aux deux bornes.
Quelle erreur maximale garantit le milieu de cet intervalle ?
\end{questions}
''',[r'''
\editionEtape{1. Dire précisément ce qui est admis et ce qui est démontré}
On a $f'(x)=3x^2+1>0$ : $f$ est strictement croissante, donc elle s'annule au plus une fois.
L'existence est donnée dans l'énoncé ; on en déduit l'unicité.
\editionEtape{2. Conserver un invariant}
Si $f(m)<0=f(\alpha)$, la croissance donne $m<\alpha$ : on peut avancer la borne gauche.
Si $f(m)\geq0$, on a $m\geq\alpha$ : on peut reculer la borne droite.
Dans les deux cas, le nouvel intervalle contient toujours $\alpha$.
\begin{python}
def encadrer_racine(N):
    a, b = 0.0, 1.0
    for k in range(N):
        m = (a + b) / 2
        if m ** 3 + m - 1 < 0:
            a = m
        else:
            b = m
    return a, b
\end{python}
L'entrée $N$ est un entier naturel, y compris 0. À chaque passage,
$a\leq\alpha\leq b$ est conservé et la largeur est divisée par 2.
''',r'''
\editionEtape{3. Garantir une précision avant de lancer le calcul}
La largeur initiale vaut 1. Après $N$ divisions par 2, elle vaut $2^{-N}$.
Comme $2^9=512<1000$ et $2^{10}=1024\geq1000$, le premier nombre d'étapes
garantissant une largeur au plus $10^{-3}$ est \res{N=10}.
\editionEtape{4. Vérifier en arithmétique exacte}
On trouve
\[f\left(\frac{698}{1024}\right)=\frac{-1767384}{1073741824}<0,
\qquad f\left(\frac{699}{1024}\right)=\frac{744899}{1073741824}>0.\]
La croissance confirme que $\alpha$ est dans cet intervalle.
Son milieu est $1397/2048$. La distance d'un point de l'intervalle au milieu
ne dépasse pas la demi-largeur, d'où
\[\res{\left|\alpha-\frac{1397}{2048}\right|\leq\frac1{2048}<5\times10^{-4}}.\]
\editionRetenir{Un algorithme d'encadrement associe un invariant, une règle de réduction
et une précision garantie. L'affichage de nombreuses décimales ne suffit pas à garantir leur justesse.}
'''],[
r"Utiliser la stricte croissance pour relier le signe de $f(m)$ à la position de $m$ par rapport à la racine.",
r"La largeur est une suite géométrique de raison $1/2$ ; distinguer la largeur de l'intervalle et l'erreur du milieu."
],{'corrige_2':['fr-d12']})

defi(13,'Une garantie pour tous les x','13, 1 et 4','Très exigeant','45 à 65 min',r'''
Pour $m\in\R$, on définit $P_m(x)=x^2-2mx+m$, et l'on s'intéresse à $x\in[0;1]$.
\begin{questions}
\item Formuler la négation de : « Pour tout $x\in[0;1]$, $P_m(x)\geq0$. »
\item Montrer que cette propriété impose $0\leq m\leq1$ en regardant les bornes.
Prouver la réciproque avec la forme canonique.
\item On note $q(m)$ le minimum de $P_m$ sur $[0;1]$. Déterminer $q(m)$
pour $m<0$, $0\leq m\leq1$ et $m>1$.
\item Quel paramètre fournit la plus grande garantie $q(m)$ ?
Donner une seconde preuve en utilisant la valeur commune $P_m(1/2)$.
\item Comparer les deux affirmations : « Il existe un $m$ tel que, pour tout $x$,
$P_m(x)\geq1/4$ » et « Pour tout $m$, il existe un $x$ tel que $P_m(x)\geq1/4$ ».
Préciser les domaines et justifier chacune des réponses.
\end{questions}
''',[r'''
\editionEtape{1. Respecter la portée des quantificateurs}
La négation est : « Il existe $x\in[0;1]$ tel que $P_m(x)<0$. »
La positivité partout impose $P_m(0)=m\geq0$ et $P_m(1)=1-m\geq0$.
Réciproquement, pour $m\in[0;1]$,
$P_m(x)=(x-m)^2+m(1-m)\geq0$. Les paramètres sont donc exactement \res{m\in[0;1]}.
\editionEtape{2. Trouver le minimum avec la position du sommet}
Pour $m<0$, $P'_m(x)=2(x-m)>0$ sur $[0;1]$, donc $q(m)=P_m(0)=m$.
Pour $0\leq m\leq1$, le sommet est dans le segment : $q(m)=m(1-m)$.
Pour $m>1$, la fonction décroît sur le segment : $q(m)=P_m(1)=1-m$.
Sur $[0;1]$, $m(1-m)=1/4-(m-1/2)^2$ ; à l'extérieur, $q(m)<0$.
La meilleure garantie est donc \res{q(1/2)=1/4}, atteinte uniquement pour \res{m=1/2}.
\editionEtape{3. Vérifier la garantie et distinguer deux énoncés}
Pour chaque $m\in\R$, $P_m(1/2)=1/4$, donc le minimum ne peut dépasser $1/4$.
Le choix $m=1/2$ donne $P_{1/2}(x)=(x-1/2)^2+1/4\geq1/4$ pour tout $x\in[0;1]$ :
la première affirmation est vraie.
La seconde est vraie aussi : pour \emph{tout} $m\in\R$, choisir $x=1/2$ suffit.
Mais elle autorise une seule valeur de $x$, et ne garantit aucune borne sur les autres valeurs.
Par exemple, pour $m=2$, $P_2(1)=-1<1/4$.
\editionRetenir{« Une borne valable partout » et « un point où la borne est dépassée »
expriment deux exigences différentes, même lorsque les deux affirmations sont vraies.}
'''],[
"Le minimum peut être au sommet ou à une borne : commencer par situer le sommet selon m.",
r"Comparer le minimum à la valeur $P_m(1/2)$, puis chercher un paramètre qui atteint cette borne pour tous les $x$."
])

defi(14,'Qualité, coût et risque','5, 9, 10 et 12','Très exigeant','60 à 80 min',r'''
Dans un atelier fictif, une intensité de contrôle $x\in[0;4]$ entraîne un coût
de $2x$ unités par article et une probabilité de défaut $p(x)=\frac15e^{-x}$.
Avant ce coût, un article rapporte 12 unités s'il est sans défaut et $-8$ sinon.
Le gain net après contrôle est noté $G_x$.
\begin{questions}
\item Donner les deux valeurs de $G_x$, leurs probabilités, puis montrer que
$E(G_x)=g(x)=12-2x-4e^{-x}$.
\item Montrer que le maximum est atteint pour l'unique $\alpha\in]0;1[$ tel que $e^\alpha=2$.
On admet l'existence de ce réel. Aucun logarithme n'est demandé.
\item Écrire un algorithme de dichotomie sur $[0;1]$ pour encadrer $\alpha$ à $10^{-3}$ près.
En déduire une approximation du gain moyen maximal.
\item Montrer que $V(G_x)=80e^{-x}-16e^{-2x}$ et étudier ses variations sur $[0;4]$.
Au point optimal pour l'espérance, calculer la probabilité de défaut et la variance exacte.
\item Deux articles sont contrôlés avec la même intensité $\alpha$ ; leurs défauts sont indépendants.
Dessiner l'arbre, puis calculer la probabilité d'au moins un défaut.
La plus grande intensité maximise-t-elle aussi le gain moyen ?
\end{questions}
''',[r'''
\editionEtape{1. Passer de la loi au gain moyen}
Les deux gains sont $12-2x$, de probabilité $1-p$, et $-8-2x$, de probabilité $p$.
Ainsi $E(G_x)=(12-2x)(1-p)+(-8-2x)p=12-2x-20p=12-2x-4e^{-x}$.
\editionEtape{2. Étudier le signe sans logarithme}
On a $g'(x)=-2+4e^{-x}$ ; son signe est positif si $e^x<2$ et négatif si $e^x>2$.
La stricte croissance de l'exponentielle donne l'unicité de $\alpha$.
Comme $e^0=1<2<e^1$, on a $0<\alpha<1$, et $g$ croît jusqu'à $\alpha$, puis décroît.
\[\res{g(\alpha)=10-2\alpha}\qquad\text{car }e^{-\alpha}=1/2.\]
\editionEtape{3. Encadrer le paramètre de réglage}
\begin{python}
from math import exp
def encadrer_reglage(N=10):
    a, b = 0.0, 1.0
    for k in range(N):
        m = (a + b) / 2
        if exp(m) < 2:
            a = m
        else:
            b = m
    return a, b
\end{python}
Pour $N=10$, la largeur est $1/1024<10^{-3}$ ; on obtient
$709/1024<\alpha<710/1024$. En poursuivant les calculs, $\alpha\approx0{,}693147$
et le gain moyen maximal vaut environ $8{,}614$ unités.
''',r'''
\editionEtape{4. Distinguer gain moyen et dispersion}
Les deux gains diffèrent de 20. En calculant les deux écarts à la moyenne,
ou en développant le deuxième moment,
\[V(G_x)=400p(1-p)=80e^{-x}-16e^{-2x}.\]
La dépense $2x$, constante pour un réglage fixé, ne change pas la variance.
La dérivée vaut
\[V'(x)=16e^{-x}(2e^{-x}-5)<0\quad\text{sur }[0;4],\]
car $e^{-x}\leq1$. La dispersion décroît donc sur tout le segment.
Pour $x=\alpha$, on a \res{p(\alpha)=1/10} et \res{V(G_\alpha)=36}.
\editionEtape{5. Répéter deux contrôles indépendants}
L'arbre donne la probabilité de deux articles sans défaut : $(9/10)^2=81/100$.
Par complément,
\[\res{P(\text{au moins un défaut})=1-81/100=19/100}.\]
L'intensité 4 minimise ici la variance et le défaut, mais elle ne maximise pas l'espérance,
puisque $4>\alpha$ et $g$ décroît strictement sur $[\alpha;4]$.
\editionRetenir{Le meilleur réglage dépend du critère choisi. Un modèle doit
préciser les coûts, les probabilités et l'indépendance avant que l'on optimise quoi que ce soit.}
'''],[
"Calculer l'espérance avant de dériver ; la différence entre les deux gains est constante.",
r"Le signe de $g'$ se lit avec la croissance de $e^x$. À l'optimum, remplacer $e^{-\alpha}$ par $1/2$ simplifie les probabilités et la variance."
],{'corrige_2':['fr-d14']})

# Deux discussions longues sont réparties à une articulation mathématique.
for numero,marqueur in [(7,r"\editionEtape{3. Séparer orthogonalité et angle d'un triangle}"),
                         (10,r"\editionEtape{3. Changer d'objectif peut changer la réponse}")]:
    d=DEFIS[numero-1]
    debut,fin=d['corrige'][0].split(marqueur,1)
    d['corrige']=[debut,marqueur+fin]
    if 'corrige_1' in d['figures']:
        d['figures']['corrige_2']=d['figures'].pop('corrige_1')
