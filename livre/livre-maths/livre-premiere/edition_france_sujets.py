"""Deux entraînements originaux, au format de l'épreuve anticipée de la session 2028.

Première partie : 12 automatismes à réponses courtes, choisis dans la rubrique
« Automatismes » du programme de Première et dans celle de Seconde (note de
service du 11 septembre 2026, NOR MENE2622640N). Deuxième partie : deux
exercices indépendants.
"""
SUJETS=[
dict(lettre='A',figures_auto=['fr-sa-auto'],auto=[
(r'Un prix de 60 euros augmente de $15\,\%$. Quel est le nouveau prix ?',r'$60\times1{,}15=\res{69\text{ euros}}$.'),
(r'Après une hausse de $25\,\%$, un article coûte 75 euros. Quel était son prix avant la hausse ?',r'On divise par le coefficient multiplicateur : $75/1{,}25=\res{60\text{ euros}}$.'),
(r'Un prix baisse de $20\,\%$. Quel pourcentage de hausse permet de revenir au prix initial ?',r'Le coefficient réciproque est $1/0{,}8=1{,}25$ : \res{25\,\%}.'),
(r'Calculer $(2-\sqrt3)(2+\sqrt3)$.',r'Par différence de deux carrés : $4-3=\res{1}$.'),
(r'Résoudre dans $\R$ l’équation $(2x-1)(x+3)=0$.',r'Un produit est nul si l’un de ses facteurs est nul : $\res{S=\{-3\,;\,1/2\}}$.'),
(r'Résoudre dans $\R$ l’inéquation $-3x+6>0$.',r'On divise par $-3$ en changeant le sens : \res{x<2}, soit $\mathopen{]}-\infty;2[$.'),
(r'Pour quels réels $x$ a-t-on $(x-1)(x+4)<0$ ?',r'Le coefficient de $x^2$ vaut 1 : le produit est strictement négatif entre ses racines $-4$ et 1, donc $\res{x\in\mathopen{]}-4;1[}$.'),
(r'Déterminer le coefficient directeur de la droite passant par $A(-1;3)$ et $B(3;-5)$.',r'$m=\dfrac{-5-3}{3-(-1)}=\dfrac{-8}{4}=\res{-2}$.'),
(r'On donne $P(A)=0{,}4$ et $P_A(B)=0{,}25$. Calculer $P(A\cap B)$.',r'$P(A\cap B)=P(A)\times P_A(B)=0{,}4\times0{,}25=\res{0{,}1}$.'),
(r'Donner la médiane de la série $1\,;\,2\,;\,2\,;\,5\,;\,10$.',r'La série ordonnée a 5 valeurs ; la troisième est la médiane : \res{2}.'),
(r'La figure 1 représente une fonction $f$ définie sur $[-2;4]$. Résoudre graphiquement $f(x)\leq1$.',r'La courbe est sur ou sous la droite d’équation $y=1$ pour les abscisses de $-1$ à 3 : $\res{S=[-1;3]}$.'),
(r'Lire graphiquement l’équation réduite de la droite $d$ de la figure 2.',r'L’ordonnée à l’origine vaut 3 ; de $(0;3)$ à $(2;2)$, $y$ diminue de 1 quand $x$ augmente de 2 : $\res{y=-\tfrac12x+3}$.')
],problemes=[
dict(titre='Une courbe et sa tangente',enonce=r'''
On définit $f(x)=x^3-6x^2+9x+2$ pour $x\in[0;4]$.
\begin{questions}
\item Calculer $f'(x)$ et le factoriser. \hfill\textit{1 point}
\item Dresser le tableau de variations, avec les valeurs aux bornes et aux points critiques. \hfill\textit{2 points}
\item Donner le minimum et le maximum sur le segment, ainsi que toutes les abscisses où ils sont atteints. \hfill\textit{1 point}
\item Écrire la tangente $T$ au point d'abscisse 2. \hfill\textit{1 point}
\item Vérifier que $f(x)-(-3x+10)=(x-2)^3$, puis déterminer la position de la courbe par rapport à $T$. \hfill\textit{1 point}
\end{questions}
On attend un tableau lisible et une phrase de conclusion pour les extremums et la position relative.
''',corrige=r'''
\editionEtape{1. Dérivée, signes et variations}
On obtient $f'(x)=3x^2-12x+9=3(x-1)(x-3)$.
Sur $[0;4]$, les signes sont successivement $+$, $-$, $+$, avec des zéros en 1 et 3.
\begin{center}\begin{tableau}\otTab[2.1]{$x$/1,$f'(x)$/1,$f$/2}{0,1,3,4}
\tkzTabLine{,+,z,-,z,+,}\tkzTabVar{-/2,+/6,-/2,+/6}\end{tableau}\end{center}
Le minimum est \res{2}, atteint en 0 et 3 ; le maximum est \res{6}, atteint en 1 et 4.
Les bornes du segment sont des candidats aux extremums globaux et doivent être comparées aux points critiques.
\editionEtape{2. Tangente et position relative}
On a $f(2)=4$ et $f'(2)=-3$. Ainsi $T:y=-3(x-2)+4=-3x+10$.
Le développement de $(x-2)^3$ donne $x^3-6x^2+12x-8$, égal à $f(x)-(-3x+10)$.
Ce cube est négatif pour $x<2$, nul en 2, positif pour $x>2$.
La courbe est donc sous la tangente sur $[0;2[$ et au-dessus sur $]2;4]$.
Elle la traverse au point de contact : une tangente ne reste pas forcément du même côté de la courbe.
''',figures_cor=['fr-sa-fonction']),
dict(titre='Ateliers, défauts et gain',enonce=r'''
L'atelier A fournit $60\,\%$ des articles et l'atelier B les autres.
Les taux de défaut sont respectivement $5\,\%$ et $10\,\%$.
On choisit un article au hasard. $D$ désigne l'évènement « l'article présente un défaut ».
\begin{questions}
\item Compléter l'arbre et calculer $P(D)$. \hfill\textit{1 point}
\item Sachant que l'article présente un défaut, calculer la probabilité qu'il provienne de B. \hfill\textit{1 point}
\item Le gain net est 12 unités sans défaut et $-8$ avec défaut. Donner sa loi. \hfill\textit{1 point}
\item Calculer l'espérance du gain. \hfill\textit{1 point}
\item Calculer sa variance. \hfill\textit{1 point}
\item Pour deux articles de défauts indépendants et de même loi, calculer la probabilité d'au moins un défaut. \hfill\textit{1 point}
\end{questions}
''',figures_ex=['fr-sa-arbre'],corrige=r'''
\editionEtape{1. Reconstituer les probabilités}
Les poids manquants sont $19/20$ et $9/10$. Par probabilités totales,
\[P(D)=\frac35\frac1{20}+\frac25\frac1{10}=\frac3{100}+\frac4{100}=\res{\frac7{100}}.\]
Les articles défectueux provenant de B représentent $4/100$ de tous les articles.
En se limitant aux défauts, on obtient
$P_D(B)=(4/100)/(7/100)=\res{4/7}$.
\editionEtape{2. Passer de la loi aux deux moments}
Le gain $G$ prend $-8$ avec probabilité $7/100$ et 12 avec probabilité $93/100$.
Ainsi $E(G)=(-8)(7/100)+12(93/100)=\res{53/5=10{,}6}$.
Le deuxième moment vaut $64(7/100)+144(93/100)=692/5$.
Il vient
\[V(G)=\frac{692}{5}-\left(\frac{53}{5}\right)^2=\res{\frac{651}{25}=26{,}04}.\]
\editionEtape{3. Utiliser l'évènement contraire}
Deux articles sans défaut ont pour probabilité $(93/100)^2$ grâce à l'indépendance.
La probabilité demandée est donc $1-(93/100)^2=\res{1351/10000=0{,}1351}$.
L'évènement « au moins un » comprend un ou deux défauts ; compter seulement un défaut serait incomplet.
''',figures_cor=['fr-sa-arbre'])]),
dict(lettre='B',figures_auto=['fr-sb-auto'],auto=[
(r'Calculer $\dfrac34+\dfrac16$.',r'Au dénominateur 12 : $\dfrac9{12}+\dfrac2{12}=\res{\dfrac{11}{12}}$.'),
(r'Calculer $\dfrac{(2^3)^2}{2^4}$.',r'$(2^3)^2=2^6$, donc le quotient vaut $2^{6-4}=\res{4}$.'),
(r'Factoriser $9x^2-1$.',r'Différence de deux carrés : $(3x)^2-1^2=\res{(3x-1)(3x+1)}$.'),
(r'Une quantité passe de 80 à 92. Calculer son taux d’évolution, en pourcentage.',r'$\dfrac{92-80}{80}=\dfrac{12}{80}=0{,}15$ : hausse de \res{15\,\%}.'),
(r'Deux hausses successives d’un même taux donnent une hausse globale de $21\,\%$. Quel est ce taux ?',r'$(1+t)^2=1{,}21=1{,}1^2$ et $1+t>0$, donc \res{t=10\,\%}.'),
(r'Exprimer $h$ en fonction de $V$ et de $r$, sachant que $V=\pi r^2h$ avec $r>0$.',r'On divise par $\pi r^2\neq0$ : $\res{h=\dfrac{V}{\pi r^2}}$.'),
(r'La droite $d$ passe par $A(0;3)$ et a pour coefficient directeur $-2$. Donner son équation réduite.',r'L’ordonnée à l’origine est l’ordonnée de $A$, soit 3, et la pente vaut $-2$ : $\res{y=-2x+3}$.'),
(r'Calculer la moyenne des notes 8, 12 et 15, de coefficients respectifs 1, 2 et 1.',r'$\dfrac{8+2\times12+15}{1+2+1}=\dfrac{47}4=\res{11{,}75}$.'),
(r'''\begin{minipage}[t]{86mm}Le tableau ci-contre répartit les 200 élèves d’un lycée. On choisit un élève au hasard ; $F$ : « être une fille » et $I$ : « être interne ». Calculer $P_F(I)$.\end{minipage}\hfill
\begin{minipage}[t]{62mm}\vspace{-3.2mm}\small\begin{tabular}[t]{@{}lccc@{}}\toprule
 & Interne & Externe & Total\\\midrule
Fille & 30 & 90 & 120\\
Garçon & 30 & 50 & 80\\
Total & 60 & 140 & 200\\\bottomrule
\end{tabular}\end{minipage}''',r'Parmi les 120 filles, 30 sont internes : $P_F(I)=\dfrac{30}{120}=\res{\dfrac14}$.'),
(r'Avec le même tableau, calculer $P(F\cap I)$, puis $P_I(F)$.',r'$P(F\cap I)=\dfrac{30}{200}=\res{\dfrac3{20}}$ ; parmi les 60 internes, 30 sont des filles : $P_I(F)=\res{\dfrac12}$.'),
(r'La figure 1 représente une fonction $g$ définie sur $[-2;4]$. Donner le signe de $g(x)$ selon $x$.',r'$g$ s’annule en $-1$ et en 3 ; \res{g(x)>0} sur $\mathopen{]}-1;3[$ et \res{g(x)<0} sur $[-2;-1[$ et sur $]3;4]$.'),
(r'La figure 2 résume une série de notes. Donner sa médiane et son écart interquartile.',r'La médiane vaut \res{12} ; l’écart interquartile vaut $Q_3-Q_1=15-9=\res{6}$.')
],problemes=[
dict(titre='Une évolution avec apport',enonce=r'''
On pose $u_0=80$ et $u_{n+1}=\frac34u_n+10$, pour $n\geq0$.
\begin{questions}
\item On pose $v_n=u_n-40$. Montrer que $v$ est géométrique et préciser ses paramètres. \hfill\textit{1,5 point}
\item En déduire l'expression de $u_n$. \hfill\textit{1 point}
\item Justifier que $u_n>40$ pour tout $n$ et que la suite décroît strictement. \hfill\textit{1 point}
\item On donne $3^4=81$, $4^4=256$, $3^5=243$ et $4^5=1024$.
Trouver le premier rang tel que $u_n\leq50$. \hfill\textit{1,5 point}
\item Écrire une boucle Python qui renvoie ce premier rang. \hfill\textit{1 point}
\end{questions}
La recherche du premier rang doit comporter une justification, pas seulement un essai réussi.
''',corrige=r'''
\editionEtape{1. Déplacer la valeur d'équilibre}
On calcule $v_{n+1}=u_{n+1}-40=(3/4)(u_n-40)=(3/4)v_n$ et $v_0=40$.
Ainsi $v_n=40(3/4)^n$ et \res{u_n=40+40(3/4)^n}.
La puissance est positive et strictement décroissante ; on a $u_n>40$ et la suite décroît strictement.
\editionEtape{2. Prouver le premier seuil}
L'inégalité $u_n\leq50$ équivaut à $(3/4)^n\leq1/4$.
Au rang 4, $81/256>64/256=1/4$ ; au rang 5, $243/1024<256/1024=1/4$.
La décroissance établie précédemment prouve donc que le premier rang est \res{5}.
\begin{python}
def premier_rang():
    n, u = 0, 80.0
    while u > 50:
        u = 0.75 * u + 10
        n = n + 1
    return n
\end{python}
Le test \code{u > 50} continue tant que le seuil n'est pas atteint.
À la sortie, $u=u_n\leq50$ ; le compteur correspond au nombre d'actualisations effectuées.
'''),
dict(titre='Cercle, tangente et projection',enonce=r'''
Dans un repère orthonormé, on donne $A(0;0)$, $B(4;0)$, $C(1;3)$ et $M(5;4)$.
\begin{questions}
\item Déterminer les médiatrices de $[AB]$ et $[AC]$, puis leur point d'intersection $\Omega$. \hfill\textit{1,5 point}
\item En déduire l'équation du cercle circonscrit au triangle $ABC$. \hfill\textit{1 point}
\item Vérifier que $C$ appartient à ce cercle. \hfill\textit{0,5 point}
\item Déterminer la tangente au cercle en $C$. \hfill\textit{1,5 point}
\item Projeter orthogonalement $M$ sur cette tangente et calculer la distance correspondante. \hfill\textit{1,5 point}
\end{questions}
''',figures_ex=['fr-sb-geometrie'],corrige=r'''
\editionEtape{1. Construire le centre du cercle}
La médiatrice de $[AB]$ est $x=2$.
Pour un point $(x;y)$, l'égalité des distances à $A$ et à $C$ s'écrit
$x^2+y^2=(x-1)^2+(y-3)^2$, soit $x+3y=5$.
L'intersection des deux médiatrices est \res{\Omega(2;1)}.
Le rayon au carré est $\Omega A^2=5$ : le cercle est
\[\res{(x-2)^2+(y-1)^2=5}.\]
Pour $C(1;3)$, le membre de gauche vaut $1+4=5$ : l'appartenance est vérifiée.
\editionEtape{2. Utiliser la direction normale du rayon}
Le rayon $\vect{\Omega C}=(-1;2)$ est normal à la tangente en $C$.
Son équation est $-(x-1)+2(y-3)=0$, donc \res{-x+2y-5=0}.
\editionEtape{3. Projeter et contrôler}
Le projeté s'écrit $H=M-\lambda(-1;2)=(5+\lambda;4-2\lambda)$.
L'équation de la tangente impose $-(5+\lambda)+2(4-2\lambda)-5=0$,
soit $-2-5\lambda=0$. Ainsi \res{H(23/5;24/5)}.
On vérifie $-23/5+48/5-5=0$. De plus $\vect{MH}=(-2/5;4/5)$ est parallèle au normal.
Les deux conditions du projeté sont donc satisfaites et
\[MH=\sqrt{4/25+16/25}=\res{\frac{2\sqrt5}{5}}.\]
''',figures_cor=['fr-sb-geometrie'])])
]
