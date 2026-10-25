from commun import e,c
CHAPTERS=[]
CHAPTERS.append(c('Matrices et systèmes linéaires','Graphes et matrices',r'Dimensions · Produit · Inverse · Transformations',
'Lire et calculer avec des matrices de tailles compatibles.@@Déterminer un inverse en ordre $2$ ou $3$.@@Résoudre un système sous forme matricielle.@@Représenter une transformation du plan par une matrice.',
'Systèmes linéaires, coordonnées et calcul algébrique.',r'''
\essSection{1}{Un tableau dont les dimensions comptent}
Une matrice de taille $m\times n$ comporte $m$ lignes et $n$ colonnes. Le coefficient $a_{ij}$ est situé à la ligne $i$, colonne $j$.
Une matrice ligne a une seule ligne ; une matrice colonne, une seule colonne. Une matrice carrée d'ordre $n$ a $n$ lignes et $n$ colonnes.
L'addition et la multiplication par un réel se font coefficient par coefficient ; l'addition exige des dimensions identiques.
\begin{definition}[Produit]
Si $A$ est de taille $m\times n$ et $B$ de taille $n\times p$, $AB$ est de taille $m\times p$ et
$(AB)_{ij}=\sum_{k=1}^na_{ik}b_{kj}$.
Chaque coefficient est le produit d'une ligne par une colonne.
\end{definition}
\figurelivre{e09-produit.pdf}{Le coefficient $(1,2)$ de $AB$ se calcule avec la première ligne de $A$ et la deuxième colonne de $B$. La somme des produits croisés vaut ici $1\times1+2\times0=1$.}
\begin{exemple}
Avec $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$ et $B=\begin{pmatrix}0&1\\1&0\end{pmatrix}$,
$AB=\begin{pmatrix}2&1\\4&3\end{pmatrix}$ mais $BA=\begin{pmatrix}3&4\\1&2\end{pmatrix}$.
En général $AB\ne BA$, même lorsque les deux produits sont définis.
\end{exemple}
\essSection{2}{L'identité et l'inverse}
La matrice identité $I_n$ a des $1$ sur la diagonale et des $0$ ailleurs. Pour une matrice carrée $A$, $AI_n=I_nA=A$ et $A^0=I_n$.
Une matrice $A$ est inversible s'il existe $A^{-1}$ tel que $AA^{-1}=A^{-1}A=I_n$.
\begin{propriete}[Ordre $2$]
Pour $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$, si $ad-bc\ne0$,
$A^{-1}=\dfrac1{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}$.
Si $ad-bc=0$, $A$ n'est pas inversible. La formule se contrôle en multipliant les matrices.
\end{propriete}
On ne « divise » pas par une matrice ; on multiplie par son inverse, du bon côté, lorsqu'il existe.
\essSection{3}{Systèmes et inverse en ordre $3$}
Le système $2x+y=5$, $x+y=3$ devient
$AX=Y$, avec $A=\begin{pmatrix}2&1\\1&1\end{pmatrix}$, $X=\binom xy$, $Y=\binom53$.
Comme $A^{-1}=\begin{pmatrix}1&-1\\-1&2\end{pmatrix}$, on obtient $X=A^{-1}Y=\binom21$.
En ordre $3$, on peut résoudre successivement les systèmes $AX=e_j$ pour construire les colonnes de l'inverse, ou employer un outil en contrôlant le produit.
\begin{exemple}
$T=\begin{pmatrix}1&1&0\\0&1&1\\0&0&1\end{pmatrix}$ a pour inverse
$\begin{pmatrix}1&-1&1\\0&1&-1\\0&0&1\end{pmatrix}$.
En effet $TX=Y$ donne successivement $x_3=y_3$, $x_2=y_2-y_3$, $x_1=y_1-y_2+y_3$.
\end{exemple}
\essSection{4}{Transformations du plan}
La matrice $R_\theta=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$ agit sur la colonne des coordonnées et représente une rotation de centre $O$.
$\begin{pmatrix}1&0\\0&-1\end{pmatrix}$ représente la symétrie par rapport à l'axe horizontal ; $kI_2$ représente l'homothétie de centre $O$ et de rapport $k$.
\figurelivre{e09-transformation.pdf}{La rotation d'angle $\pi/2$ envoie le point $(2,1)$ sur $(-1,2)$. Les vecteurs colonnes et le calcul complexe par multiplication par $\mathrm i$ décrivent la même transformation.}
Une translation non nulle ne se représente pas par une matrice $2\times2$ appliquée seule à la colonne $(x,y)$, car une telle matrice envoie toujours l'origine sur l'origine. Elle s'écrit sous forme affine $X\mapsto AX+C$.
''',[
e('Dimensions',1,r'$A$ est $2\times3$ et $B$ est $3\times4$.',r'Quelle est la taille de $AB$ ?@@Le produit $BA$ est-il défini ?@@Peut-on additionner $A$ et $B$ ?',r'$2\times4$, car les dimensions intérieures $3$ coïncident.@@Non : les dimensions intérieures seraient $4$ et $2$.@@Non : les tailles sont différentes.'),
e('Addition et scalaire',1,r'$A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$.',r'Calculer $2A$.@@Calculer $A+I_2$.@@Donner $A^0$.',r'$\begin{pmatrix}2&4\\6&8\end{pmatrix}$.@@$\begin{pmatrix}2&2\\3&5\end{pmatrix}$.@@$I_2$, par convention sur les puissances.'),
e('Produit ligne-colonne',1,r'$A=\begin{pmatrix}2&1\\0&3\end{pmatrix}$ et $X=\binom45$.',r'Calculer $AX$.@@Quelle taille a le résultat ?@@Que représente le premier coefficient ?',r'$AX=\binom{13}{15}$.@@Une colonne de taille $2\times1$.@@$2\times4+1\times5=13$, combinaison des coordonnées avec les coefficients de la première ligne.'),
e('Inverser en ordre $2$',1,r'$A=\begin{pmatrix}2&1\\1&1\end{pmatrix}$.',r'Calculer $ad-bc$.@@Donner $A^{-1}$.@@Vérifier le produit.',r'$2-1=1$.@@$\begin{pmatrix}1&-1\\-1&2\end{pmatrix}$.@@$AA^{-1}=\begin{pmatrix}1&0\\0&1\end{pmatrix}$ par multiplication ligne-colonne.'),
e('Non-commutativité',2,r'$A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$ et $B=\begin{pmatrix}0&1\\1&0\end{pmatrix}$.',r'Calculer $AB$.@@Calculer $BA$.@@Peut-on utiliser $(A+B)^2=A^2+2AB+B^2$ sans condition ?',r'$\begin{pmatrix}2&1\\4&3\end{pmatrix}$.@@$\begin{pmatrix}3&4\\1&2\end{pmatrix}$.@@Non : le développement général est $A^2+AB+BA+B^2$ ; il faut $AB=BA$ pour regrouper les termes croisés.'),
e('Résoudre un système',2,r'$2x+y=5$, $x+y=3$.',r'Écrire $AX=Y$.@@Résoudre à l’aide de l’inverse.@@Vérifier dans les deux équations.',r'$A=\begin{pmatrix}2&1\\1&1\end{pmatrix}$, $X=\binom xy$, $Y=\binom53$.@@$X=\begin{pmatrix}1&-1\\-1&2\end{pmatrix}\binom53=\binom21$.@@$2(2)+1=5$ et $2+1=3$.'),
e('Un ordre $3$',2,r'$T=\begin{pmatrix}1&1&0\\0&1&1\\0&0&1\end{pmatrix}$.',r'Résoudre $TX=\begin{pmatrix}3\\5\\2\end{pmatrix}$.@@Donner $T^{-1}$.@@Contrôler un coefficient hors diagonale de $TT^{-1}$.',r'En remontant : $x_3=2$, $x_2=3$, $x_1=0$.@@$\begin{pmatrix}1&-1&1\\0&1&-1\\0&0&1\end{pmatrix}$.@@Le coefficient $(1,3)$ vaut $1\times1+1\times(-1)+0\times1=0$, comme dans $I_3$.'),
e('Rotation',2,r'$R=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$.',r'Calculer l’image de $(2,1)$.@@Calculer $R^2$.@@Interpréter les deux transformations.',r'$R\binom21=\binom{-1}2$.@@$R^2=-I_2$.@@$R$ est la rotation d’angle $\pi/2$ ; $R^2$ est la symétrie centrale, ou rotation d’angle $\pi$.'),
e('Matrice singulière',3,r'$A=\begin{pmatrix}1&2\\2&4\end{pmatrix}$.',r'Pourquoi n’est-elle pas inversible ?@@Étudier $AX=\binom36$.@@Étudier $AX=\binom37$.',r'$ad-bc=4-4=0$ ; la seconde ligne est le double de la première.@@Les deux équations sont équivalentes à $x+2y=3$ : une infinité de solutions réelles.@@Les équations se contredisent : la seconde devrait avoir second membre $6$, donc aucune solution.'),
e('Ordre d’une composition',3,r'$S=\begin{pmatrix}1&0\\0&-1\end{pmatrix}$ et $R=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$.',r'Calculer $RS$ et $SR$.@@Quelle matrice correspond à « appliquer $S$, puis $R$ » sur une colonne ?@@Comparer les images de $(1,1)$.',r'$RS=\begin{pmatrix}0&1\\1&0\end{pmatrix}$ ; $SR=\begin{pmatrix}0&-1\\-1&0\end{pmatrix}$.@@$R(SX)=(RS)X$ : la transformation appliquée en premier est à droite.@@$RS$ donne $(1,1)$ ; $SR$ donne $(-1,-1)$, montrant la différence.'),
e('Un inverse de produit',3,r'$A,B$ sont inversibles de même ordre.',r'Verifier $(AB)(B^{-1}A^{-1})=I$.@@Vérifier le produit dans l’autre sens.@@Conclure et signaler le piège d’ordre.',r'Par associativité, $A(BB^{-1})A^{-1}=AA^{-1}=I$.@@$B^{-1}(A^{-1}A)B=B^{-1}B=I$.@@$(AB)^{-1}=B^{-1}A^{-1}$. L’ordre des facteurs est inversé ; $A^{-1}B^{-1}$ ne convient pas en général.'),
e('Translation et matrice',3,'',r'Montrer que toute matrice $2\times2$ envoie la colonne nulle sur zéro.@@Pourquoi une translation non nulle ne peut-elle être représentée ainsi ?@@Écrire la translation de vecteur $(3,-1)$ sous forme affine.',r'Chaque coefficient du produit est une somme de produits par zéro, donc nul.@@Elle déplace l’origine, contrairement à toute application $X\mapsto AX$.@@$X\mapsto I_2X+\binom3{-1}$.')
], 'courbe'))

CHAPTERS.append(c('Puissances et suites matricielles','Graphes et matrices',r'Récurrence · Point fixe · Ordres 2 et 3',
'Calculer des puissances de matrices en ordres $2$ et $3$.@@Démontrer une formule par récurrence.@@Modéliser une évolution couplée par colonnes.@@Résoudre une récurrence affine avec un point fixe.',
'Calcul matriciel, suites et récurrence.',r'''
\essSection{1}{Répéter une transformation}
Pour une matrice carrée, $A^{n+1}=A^nA$ et $A^0=I$. Pour une matrice colonne $U_{n+1}=AU_n$, une récurrence donne $U_n=A^nU_0$.
On ne calcule pas $A^n$ en élevant chaque coefficient à la puissance $n$.
Pour $D=\operatorname{diag}(a,b)$, en revanche $D^n=\operatorname{diag}(a^n,b^n)$.
\begin{exemple}[Une matrice de cisaillement]
Pour $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$,
$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$.
Au rang zéro, on retrouve $I$ ; multiplier la formule au rang $n$ par $A$ remplace le coefficient $n$ par $n+1$.
\end{exemple}
\essSection{2}{Conjecturer puis prouver en ordre $2$}
Pour $B=\begin{pmatrix}3&1\\0&2\end{pmatrix}$, calculer $B^2,B^3$ suggère
$B^n=\begin{pmatrix}3^n&3^n-2^n\\0&2^n\end{pmatrix}$.
Le coefficient supérieur droit du produit au rang suivant vaut $3^n+2(3^n-2^n)=3^{n+1}-2^{n+1}$, ce qui établit l'hérédité.
Une autre méthode guidée consiste à fournir $B=PDP^{-1}$. Alors $(PDP^{-1})^n=PD^nP^{-1}$, puisque les facteurs intermédiaires $P^{-1}P$ se simplifient. Le manuel ne suppose pas une théorie générale de diagonalisation.
\essSection{3}{Un exemple en ordre $3$}
Pour $T=\begin{pmatrix}1&1&0\\0&1&1\\0&0&1\end{pmatrix}$, on a
\[T^n=\begin{pmatrix}1&n&n(n-1)/2\\0&1&n\\0&0&1\end{pmatrix}.
\]
Pour vérifier l'hérédité, le coefficient $(1,3)$ devient $n(n-1)/2+n=n(n+1)/2$. Les autres coefficients se contrôlent directement.
Cette formule illustre la présence naturelle de suites arithmétiques et de coefficients binomiaux dans les puissances de matrices.
\essSection{4}{Évolutions affines couplées}
\begin{savoirfaire}
Pour $U_{n+1}=AU_n+C$, chercher une colonne constante $L$ vérifiant $(I-A)L=C$.
Si une telle colonne existe, $V_n=U_n-L$ satisfait $V_{n+1}=AV_n$, donc
$U_n=L+A^n(U_0-L)$.
Si $I-A$ est inversible, $L=(I-A)^{-1}C$ est unique.
\end{savoirfaire}
\begin{exemple}
Pour $A=\begin{pmatrix}1/2&0\\0&1/4\end{pmatrix}$, $C=\binom13$ et $U_0=\binom00$, on trouve $L=\binom24$.
Ainsi $U_n=\binom{2(1-2^{-n})}{4(1-4^{-n})}$, qui tend vers $L$ coordonnée par coordonnée.
\end{exemple}
\figurelivre{e10-evolution.pdf}{Les deux composantes de l'exemple tendent vers leurs valeurs d'équilibre, $2$ et $4$. Le modèle matriciel regroupe les deux récurrences et conserve leur interprétation.}
\essSection{5}{La matrice ne garantit pas une limite}
Une suite matricielle peut diverger ou être périodique. Pour $A=\begin{pmatrix}0&1\\1&0\end{pmatrix}$, $A^2=I$ : certaines colonnes alternent indéfiniment.
Des modèles de populations peuvent coupler plusieurs effectifs. Il faut vérifier la pertinence des coefficients et le maintien de valeurs admissibles ; une formule algébrique n'assure pas qu'une approximation physique reste valable sur une longue durée.
Le programme distingue ces colonnes d'évolution des distributions lignes des chaînes de Markov, étudiées au chapitre 12.
''',[
e('Puissances diagonales',1,r'$D=\begin{pmatrix}2&0\\0&3\end{pmatrix}$.',r'Calculer $D^2$.@@Donner $D^n$.@@Donner $D^{-1}$.',r'$\begin{pmatrix}4&0\\0&9\end{pmatrix}$.@@$\begin{pmatrix}2^n&0\\0&3^n\end{pmatrix}$ pour $n\in\N$.@@$\begin{pmatrix}1/2&0\\0&1/3\end{pmatrix}$.'),
e('Matrice périodique',1,r'$A=\begin{pmatrix}0&1\\1&0\end{pmatrix}$.',r'Calculer $A^2$.@@Donner $A^{2026}$.@@Donner $A^{2027}$.',r'$I_2$.@@$I_2$, car $2026$ est pair.@@$A$, car $2027$ est impair.'),
e('Premières colonnes',1,r'$A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ et $U_0=\binom01$.',r'Calculer $U_1=AU_0$.@@Calculer $U_2$.@@Conjecturer $U_n$.',r'$\binom11$.@@$\binom21$.@@$U_n=\binom n1$, confirmé par la formule de $A^n$.'),
e('Équilibre',1,r'$U_{n+1}=\frac12I_2U_n+\binom12$.',r'Chercher la colonne fixe $L$.@@Exprimer $U_n-L$.@@Si $U_0=0$, donner la limite.',r'$L=\tfrac12L+\binom12$, donc $L=\binom24$.@@$U_n-L=2^{-n}(U_0-L)$.@@La limite est $L$, car $2^{-n}\to0$.'),
e('Prouver une puissance',2,r'$A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$.',r'Verifier la formule du cours pour $n=0$.@@Établir l’hérédité par multiplication.@@Donner $A^{100}$.',r'La formule donne $I_2$.@@$\begin{pmatrix}1&n\\0&1\end{pmatrix}A=\begin{pmatrix}1&n+1\\0&1\end{pmatrix}$.@@$\begin{pmatrix}1&100\\0&1\end{pmatrix}$.'),
e('Une puissance triangulaire',2,r'$B=\begin{pmatrix}3&1\\0&2\end{pmatrix}$.',r'Calculer $B^2$.@@Donner $B^n$ et vérifier au rang $1$.@@Calculer $B^5$.',r'$\begin{pmatrix}9&5\\0&4\end{pmatrix}$.@@$\begin{pmatrix}3^n&3^n-2^n\\0&2^n\end{pmatrix}$ ; pour $n=1$, le coefficient supérieur droit vaut $1$.@@$\begin{pmatrix}243&211\\0&32\end{pmatrix}$.'),
e('Ordre $3$',2,r'$T=\begin{pmatrix}1&1&0\\0&1&1\\0&0&1\end{pmatrix}$.',r'Calculer $T^2$.@@Utiliser la formule du cours pour $T^4$.@@Calculer $T^4\begin{pmatrix}0\\0\\1\end{pmatrix}$.',r'$\begin{pmatrix}1&2&1\\0&1&2\\0&0&1\end{pmatrix}$.@@$\begin{pmatrix}1&4&6\\0&1&4\\0&0&1\end{pmatrix}$.@@$\begin{pmatrix}6\\4\\1\end{pmatrix}$, la troisième colonne de $T^4$.'),
e('Deux récurrences',2,r'$u_{n+1}=u_n/2+1$, $v_{n+1}=v_n/4+3$, $u_0=v_0=0$.',r'Écrire $U_{n+1}=AU_n+C$.@@Trouver $L$.@@Exprimer les deux composantes et leurs limites.',r'$U_n=\binom{u_n}{v_n}$, $A=\operatorname{diag}(1/2,1/4)$, $C=\binom13$.@@$L=\binom24$.@@$u_n=2(1-2^{-n})\to2$ et $v_n=4(1-4^{-n})\to4$.'),
e('Une méthode avec $PDP^{-1}$',3,r'$P=\begin{pmatrix}1&-1\\0&1\end{pmatrix}$ et $D=\operatorname{diag}(3,2)$.',r'Calculer $P^{-1}$ et $PDP^{-1}$.@@Justifier $(PDP^{-1})^n=PD^nP^{-1}$.@@Retrouver les puissances de $B$.',r'$P^{-1}=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ ; le produit vaut $B=\begin{pmatrix}3&1\\0&2\end{pmatrix}$.@@Les facteurs $P^{-1}P$ se simplifient dans les produits successifs ; une récurrence formalise l’identité.@@$B^n=\begin{pmatrix}3^n&3^n-2^n\\0&2^n\end{pmatrix}$.'),
e('Un couplage périodique',3,r'$A=\begin{pmatrix}0&2\\1/2&0\end{pmatrix}$, $U_0=\binom10$.',r'Calculer $A^2$.@@Donner les colonnes paires et impaires.@@La suite converge-t-elle ?',r'$I_2$.@@$U_{2k}=\binom10$, $U_{2k+1}=\binom0{1/2}$.@@Non : les deux sous-suites constantes ont des valeurs différentes.'),
e('Point fixe non unique',3,r'$A=I_2$ et $C=0$.',r'Quelles colonnes sont fixes ?@@Que vaut $U_n$ ?@@Pourquoi ne peut-on utiliser $(I-A)^{-1}C$ ?',r'Toutes les colonnes $L$ satisfont $L=AL+C$.@@$U_n=U_0$ pour tout $n$.@@$I-A$ est la matrice nulle, non inversible. L’existence d’un point fixe ne garantit pas son unicité.'),
e('Contrôler une formule en ordre $3$',3,r'On propose la formule de $T^n$ du cours.',r'Verifier les coefficients pour $n=0,1$.@@Calculer le coefficient $(1,3)$ de $T^nT$.@@Expliquer l’apparition de $\binom n2$.',r'Pour $n=0$, les hors-diagonales sont nulles ; pour $n=1$, $(1,3)=0$ : on retrouve $I$ puis $T$.@@$n+n(n-1)/2=n(n+1)/2$.@@Le coefficient satisfait la récurrence $c_{n+1}=c_n+n$, avec $c_0=0$ ; c’est la somme $0+1+\cdots+(n-1)=\binom n2$.')
], 'suites'))
