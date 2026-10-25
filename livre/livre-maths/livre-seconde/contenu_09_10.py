from modele import *

chapitre(9,'configurations','Repérage et configurations','3 · Géométrie',
 'Milieux · Distances · Triangles · Aires et volumes',
 ['Calculer distances et milieux dans un repère orthonormé.','Choisir entre outils repérés et théorèmes géométriques.','Justifier une construction à partir de ses propriétés.'],
 ['Pythagore, Thalès et trigonométrie du triangle rectangle.'],[
r'''\essSection{1}{Distances et milieux}
\begin{propriete}Dans un repère orthonormé, pour $A(x_A;y_A)$ et $B(x_B;y_B)$ :
\[AB=\sqrt{(x_B-x_A)^2+(y_B-y_A)^2}.\]
Le milieu $I$ de $[AB]$ a pour coordonnées
\[I\left(\frac{x_A+x_B}{2}\,;\,\frac{y_A+y_B}{2}\right).\]
\end{propriete}
\begin{savoirfaire}[Reconnaître une figure]
Comparer des carrés de longueurs : égalité de deux côtés pour un triangle isocèle, relation de Pythagore pour un angle droit. Pour un parallélogramme, on peut aussi montrer que les diagonales ont le même milieu ou que deux côtés opposés ont des vecteurs égaux.
\end{savoirfaire}
\begin{definition}La médiatrice de $[AB]$ est la droite perpendiculaire à $(AB)$ passant par son milieu. Ses points sont exactement les points équidistants de $A$ et de $B$.\end{definition}
\begin{attention}La formule de distance suppose des axes perpendiculaires et une même unité sur les deux axes. Un dessin déformé n’autorise pas à mesurer directement une longueur.\end{attention}''',
r'''\essSection{2}{Réinvestir les configurations du collège}
\begin{propriete}Dans un triangle rectangle, le carré de l’hypoténuse est la somme des carrés des deux autres côtés. Réciproquement, cette égalité caractérise le triangle rectangle si l’hypoténuse présumée est le plus grand côté.\end{propriete}
\begin{savoirfaire}[Thalès]Identifier deux triangles en configuration de Thalès et établir le parallélisme requis avant d’écrire des rapports de côtés correspondants. La réciproque permet de démontrer un parallélisme si les points sont dans le même ordre.\end{savoirfaire}
\begin{propriete}Pour un angle aigu $\alpha$ d’un triangle rectangle :
\[\cos\alpha=\frac{\text{adjacent}}{\text{hypoténuse}},\quad
\sin\alpha=\frac{\text{opposé}}{\text{hypoténuse}},\quad
\tan\alpha=\frac{\text{opposé}}{\text{adjacent}}.\]
\end{propriete}
\begin{propriete}Cercle de rayon $r$ : périmètre $2\pi r$, aire du disque $\pi r^2$. Aire d’un triangle : base fois hauteur divisée par 2. Volume d’un prisme ou cylindre : aire de base fois hauteur ; pavé droit : $abc$. Pour une pyramide ou un cône, diviser aire de base fois hauteur par 3. Volume d’une boule : $4\pi r^3/3$.\end{propriete}
\otIntertitre{Choisir sa preuve}
Un repère est utile pour calculer ; une propriété géométrique peut être plus courte. Dans les corrigés, repérer ce qui relève des données, ce qui est construit et ce qui est démontré.'''
],[
E('Distance entre deux points',r"""On donne $A(-1;2)$ et $B(3;5)$. Calculer $AB$.""",
r"""Les différences de coordonnées sont 4 et 3. Dans le repère orthonormé, $AB^2=4^2+3^2=25$, donc $\res{AB=5}$. La racine positive est retenue puisqu’une longueur est positive. Le triangle auxiliaire du dessin relie ces différences au théorème de Pythagore.""",
'Calculer le carré de la distance, puis prendre la racine positive.','assert (3+1)**2+(5-2)**2==25',figure='conf-01'),
E('Coordonnées d’un milieu',r"""Déterminer le milieu de $[AB]$ pour $A(-2;5)$ et $B(6;-1)$. Vérifier par une égalité vectorielle.""",
r"""On fait la moyenne des coordonnées : $I((-2+6)/2;(5-1)/2)=\res{I(2;2)}$. Puis $\vect{AI}=(4;-3)$ et $\vect{IB}=(4;-3)$. Cette égalité confirme que $I$ est bien le milieu, et pas seulement un point équidistant des deux extrémités.""",
'Faire deux moyennes et contrôler le placement sur le segment.','assert ((-2+6)/2,(5-1)/2)==(2,2)',figure='conf-02'),
E('Retrouver une extrémité',r"""$I(2;1)$ est le milieu de $[AB]$ et $A(-1;4)$. Déterminer $B$.""",
r"""Les formules de milieu donnent $(-1+x_B)/2=2$ et $(4+y_B)/2=1$. Donc $x_B=5$ et $y_B=-2$ : $\res{B(5;-2)}$. Vérification : la moyenne des abscisses vaut 2 et celle des ordonnées 1. Le point $B$ est le symétrique de $A$ par rapport à $I$.""",
'Résoudre les deux formules du milieu pour l’extrémité inconnue.','assert (2*2-(-1),2*1-4)==(5,-2)',figure='conf-03'),
E('Un triangle rectangle',r"""$A(0;0)$, $B(4;0)$ et $C(4;3)$. Montrer que le triangle est rectangle et calculer son aire.""",
r"""$AB^2=16$, $BC^2=9$ et $AC^2=25$. Puisque $AB^2+BC^2=AC^2$, la réciproque de Pythagore montre que le triangle est rectangle en $B$. L’aire vaut $AB\times BC/2=4\times3/2=\res6$. Le côté $AC$, opposé à l’angle droit, est bien le plus long.""",
'Vérifier Pythagore puis utiliser les deux côtés perpendiculaires.','assert 4**2+3**2==5**2 and Rational(4*3,2)==6',figure='conf-04'),
E('Une médiatrice facile',r"""$A(-2;0)$ et $B(4;0)$. Donner le milieu de $[AB]$, puis une équation de sa médiatrice. Le point $M(1;3)$ lui appartient-il ?""",
r"""Le milieu est $(1;0)$. Le segment étant horizontal, sa médiatrice est verticale : $\res{x=1}$. Le point $M(1;3)$ lui appartient. On contrôle l’équidistance : $MA^2=3^2+3^2=18$ et $MB^2=(-3)^2+3^2=18$.""",
'Associer une médiatrice à un milieu et à une perpendicularité.','assert Rational(-2+4,2)==1 and (1+2)**2+3**2==(1-4)**2+3**2',figure='conf-05'),
E('Un triangle isocèle',r"""On donne $A(0;0)$, $B(4;0)$ et $C(2;3)$. Démontrer que le triangle est isocèle, puis calculer son périmètre et son aire.""",
r"""$CA^2=2^2+3^2=13$ et $CB^2=(-2)^2+3^2=13$. Ainsi $CA=CB=\sqrt{13}$ : le triangle est isocèle en $C$. Son périmètre est $\res{4+2\sqrt{13}}$. La hauteur sur la base horizontale vaut 3, donc l’aire est $4\times3/2=\res6$.""",
'Comparer les carrés des côtés et lire une hauteur perpendiculaire.','assert 2**2+3**2==(-2)**2+3**2==13 and Rational(4*3,2)==6',figure='conf-06'),
E('Thalès dans un triangle',r"""Dans $ABC$, $AB=9$, $AC=12$. Les points $M\in[AB]$ et $N\in[AC]$ vérifient $AM=6$ et $(MN)\parallel(BC)$. Calculer $AN$ et le rapport des aires $AMN$ et $ABC$.""",
r"""Le parallélisme autorise Thalès : $AM/AB=AN/AC=2/3$. Ainsi $AN=12\times2/3=\res8$. Les longueurs sont multipliées par $2/3$, donc les aires par son carré : $\res{\mathcal A(AMN)/\mathcal A(ABC)=4/9}$. Le facteur d’aire n’est pas le facteur de longueur.""",
'Identifier le coefficient de réduction et le mettre au carré pour les aires.','assert Rational(6,9)*12==8 and Rational(6,9)**2==Rational(4,9)',figure='conf-07'),
E('Une hauteur par trigonométrie',r"""Un point $P$ au sol est à 20 m du pied $B$ d’une tour verticale $BS$. L’angle $\widehat{BPS}$ vaut $35^\circ$. Exprimer la hauteur, puis l’arrondir au dixième de mètre.""",
r"""Le triangle est rectangle en $B$. Pour l’angle en $P$, la hauteur est le côté opposé et 20 le côté adjacent : $\tan35^\circ=BS/20$. Donc $\res{BS=20\tan35^\circ\approx14{,}0\text{ m}}$. La calculatrice doit être réglée en degrés ; il faut ensuite arrondir, sans modifier les données en cours de calcul.""",
'Choisir le rapport trigonométrique correspondant aux côtés connus.','assert abs(float(20*tan(35*pi/180))-14.004150764)<1e-7',figure='conf-08'),
E('Une réduction de cône',r"""Un cône de rayon 3 cm et hauteur 8 cm est coupé parallèlement à sa base à mi-hauteur depuis son sommet. Calculer le volume du petit cône et la fraction du volume total qu’il représente. Calculer aussi le volume d’une boule de rayon 3 cm et celui d’une pyramide de base d’aire 27 cm$^2$ et de hauteur 8 cm.""",
r"""Le petit cône est une réduction de coefficient $1/2$ : son rayon vaut 1,5 cm et sa hauteur 4 cm. Son volume est $\pi\times1{,}5^2\times4/3=\res{3\pi\text{ cm}^3}$. Le grand volume vaut $24\pi$ cm$^3$. Le rapport est $\res{1/8}$, soit le cube du coefficient de réduction. Pour la boule, $4\pi\times3^3/3=\res{36\pi\text{ cm}^3}$. Pour la pyramide, $27\times8/3=\res{72\text{ cm}^3}$. Les trois formules concernent des solides différents ; l’aire de base seule ne détermine pas le volume.""",
'Utiliser la similitude puis la formule adaptée à chaque solide.','assert pi*Rational(3,2)**2*4/3==3*pi and Rational(3,24)==Rational(1,8) and 4*pi*3**3/3==36*pi and Rational(27*8,3)==72',figure='conf-09'),
E('Le centre d’un parallélogramme',r"""$A(0;0)$, $B(4;1)$, $C(5;4)$ et $D(1;3)$. Démontrer que $ABCD$ est un parallélogramme en utilisant les milieux.""",
r"""Le milieu de $[AC]$ est $(5/2;2)$. Celui de $[BD]$ est $((4+1)/2;(1+3)/2)=(5/2;2)$. Les diagonales ont le même milieu : le quadrilatère $ABCD$ est donc un parallélogramme. Le critère concerne les diagonales $AC$ et $BD$, pas deux côtés quelconques.""",
'Calculer les milieux des deux diagonales et appliquer la réciproque.','assert (Rational(0+5,2),Rational(0+4,2))==(Rational(4+1,2),Rational(1+3,2))',figure='conf-10'),
E('Un rectangle incliné',r"""$A(0;0)$, $B(4;2)$, $C(3;4)$ et $D(-1;2)$. Montrer que $ABCD$ est un rectangle sans utiliser le produit scalaire.""",
r"""On a $\vect{AB}=(4;2)=\vect{DC}$, donc c’est un parallélogramme. Puis $AB^2=20$, $BC^2=5$ et $AC^2=25$. L’égalité $AB^2+BC^2=AC^2$ prouve que l’angle en $B$ est droit. Un parallélogramme avec un angle droit est un rectangle. L’orientation des côtés sur la page n’intervient pas.""",
'Combiner un critère de parallélogramme et la réciproque de Pythagore.','assert (4,2)==(3-(-1),4-2) and (4**2+2**2)+((-1)**2+2**2)==3**2+4**2',figure='conf-11'),
E('Un triangle avec un paramètre',r"""$A(-1;0)$, $B(3;0)$ et $C(t;2)$. Déterminer $t$ pour que $CA=CB$. Calculer alors l’aire.""",
r"""On compare les carrés : $(t+1)^2+4=(t-3)^2+4$. Après développement, $2t+1=-6t+9$, soit $t=1$. Le point $C(1;2)$ se trouve sur la médiatrice verticale de $[AB]$. La base vaut 4 et la hauteur 2, donc l’aire est $\res4$.""",
'Traduire l’équidistance par une égalité de distances au carré.','assert solve((x+1)**2-(x-3)**2,x)==[1] and Rational(4*2,2)==4',figure='conf-12'),
E('Un point équidistant',r"""$A(0;0)$, $B(4;0)$ et $C(0;6)$. Trouver le point $O$ équidistant de ces trois points, puis le rayon du cercle qui les contient.""",
r"""La médiatrice de $[AB]$ est $x=2$ et celle de $[AC]$ est $y=3$. Leur intersection est $\res{O(2;3)}$. On calcule $OA^2=13$, $OB^2=13$ et $OC^2=13$. Le cercle de centre $O$ et de rayon $\res{\sqrt{13}}$ passe donc par les trois points. Les égalités de distance vérifient directement la construction.""",
'Intersecter deux médiatrices simples puis contrôler la troisième distance.','assert [(a-2)**2+(b-3)**2 for a,b in [(0,0),(4,0),(0,6)]]==[13,13,13]',figure='conf-13'),
E('Un lieu de points sur une horizontale',r"""Les points $M(t;4)$ sont à distance 5 de l’origine $O$. Déterminer tous ces points. Donner aussi le périmètre du cercle de centre $O$ et rayon 5, puis l’aire de son disque.""",
r"""On écrit $OM^2=t^2+16=25$, donc $t^2=9$ et $t=-3$ ou 3. Les points sont $\res{(-3;4)\text{ et }(3;4)}$. Ils sont symétriques par rapport à l’axe des ordonnées. Garder seulement la racine positive aurait oublié une intersection. Le cercle a pour périmètre $2\pi\times5=\res{10\pi}$ ; le disque a pour aire $\pi\times5^2=\res{25\pi}$. Une unité de longueur devient une unité d’aire dans le dernier résultat.""",
'Résoudre la distance au carré puis distinguer longueur du cercle et aire du disque.','assert solveset(x*x+16-25,x,domain=S.Reals)==FiniteSet(-3,3) and 2*pi*5==10*pi and pi*5**2==25*pi',figure='conf-14'),
E('Un raccourci dans un pavé',r"""Un pavé droit mesure 6 cm sur 8 cm, pour une hauteur de 5 cm. Calculer la diagonale de sa base, puis sa diagonale intérieure. Comparer cette dernière au trajet suivant trois arêtes.""",
r"""La diagonale de base vaut $\sqrt{6^2+8^2}=10$ cm. Elle forme avec la hauteur un triangle rectangle, donc la diagonale intérieure vaut $\sqrt{10^2+5^2}=\res{5\sqrt5\text{ cm}}$, environ 11,18 cm. Le trajet de trois arêtes vaut $6+8+5=19$ cm ; il est plus long. Les deux applications de Pythagore sont faites dans deux plans perpendiculaires appropriés.""",
'Ramener une question spatiale à deux triangles rectangles successifs.','assert sqrt(6**2+8**2)==10 and sqrt(100+25)==5*sqrt(5) and 5*sqrt(5)<19',figure='conf-15')
],reperes=['Distances et coordonnées du milieu','Configurations planes et médiatrices','Réactivation de Pythagore, Thalès et trigonométrie','Aires, volumes et réductions'],deco='cercleplan')

chapitre(10,'droites','Droites du plan','3 · Géométrie',
 'Équations · Pentes · Parallélisme · Intersections',
 ['Passer d’une droite à ses équations et réciproquement.','Construire une droite à partir de données variées.','Résoudre une intersection et interpréter un système.'],
 ['Vecteurs, déterminants et fonctions affines.'],[
r'''\essSection{1}{Deux écritures pour une droite}
\begin{definition}Une équation cartésienne de droite est $ax+by+c=0$, avec $(a;b)\ne(0;0)$. Un vecteur directeur non nul est $(-b;a)$. Il décrit une direction parallèle à la droite.\end{definition}
\begin{propriete}Si $b\ne0$, l’équation devient $y=mx+p$, avec $m=-a/b$ et $p=-c/b$. Si $b=0$, la droite est verticale : $x=-c/a$. Elle n’a pas de pente et ne représente pas une fonction de $x$.\end{propriete}
\begin{savoirfaire}[À partir de deux points]
Pour $A$ et $B$ distincts avec $x_A\ne x_B$, calculer $m=(y_B-y_A)/(x_B-x_A)$ puis $p=y_A-mx_A$. Si leurs abscisses sont égales, écrire directement $x=x_A$.
\end{savoirfaire}
\begin{savoirfaire}[À partir d’un directeur]
Si $d$ passe par $A$ et a pour directeur $\vec u=(u;v)\ne\vec0$, un point $M(x;y)$ est sur $d$ si $\det(\vec u,\vect{AM})=0$, soit $u(y-y_A)-v(x-x_A)=0$.
\end{savoirfaire}''',
r'''\essSection{2}{Positions relatives et systèmes}
\begin{propriete}Deux droites non verticales de même pente sont parallèles : confondues si leurs ordonnées à l’origine sont aussi égales, distinctes sinon. Avec des directeurs, le déterminant nul caractérise le parallélisme.\end{propriete}
\begin{savoirfaire}[Intersection]
Pour $y=m_1x+p_1$ et $y=m_2x+p_2$, résoudre $(m_1-m_2)x=p_2-p_1$, puis calculer $y$ dans l’une des équations. Vérifier le point dans les deux équations initiales.
\end{savoirfaire}
\begin{exemple}$y=2x+1$ et $y=-x+7$ se coupent pour $3x=6$, donc au point $(2;5)$. Deux pentes distinctes donnent exactement une intersection.\end{exemple}
\begin{attention}Une équation peut être multipliée par un réel non nul sans changer la droite. Les écritures $x-2y+3=0$ et $2x-4y+6=0$ représentent ainsi la même droite.\end{attention}
\otIntertitre{Avec un logiciel de géométrie}
Créer deux points, tracer leur droite et afficher son équation. Déplacer un point jusqu’à obtenir une droite verticale : observer ce qui change dans l’équation réduite. Expliquer ensuite ce changement avec les coordonnées.'''
],[
E('Tester des points',r"""La droite $d$ a pour équation $2x-y+3=0$. Les points $A(1;5)$ et $B(2;6)$ lui appartiennent-ils ?""",
r"""Pour $A$, $2\times1-5+3=0$ : il appartient à $d$. Pour $B$, $4-6+3=1\ne0$ : il n’y appartient pas. Une équation de droite est un test exact d’appartenance ; il ne suffit pas qu’un point soit proche du tracé.""",
'Substituer les coordonnées dans l’équation cartésienne.','assert 2*1-5+3==0 and 2*2-6+3!=0',figure='droite-01'),
E('De l’équation au tracé',r"""Écrire $3x-2y+6=0$ sous forme réduite. Donner deux points de la droite.""",
r"""On isole $y$ : $-2y=-3x-6$, puis $\res{y=\tfrac32x+3}$. Avec $x=0$, on obtient $(0;3)$ ; avec $y=0$, on obtient $(-2;0)$. Ces deux points distincts suffisent à tracer la droite et sont faciles à contrôler dans l’équation initiale.""",
'Isoler y et choisir des coordonnées simples.','assert solve(3*x-2*y+6,y)==[Rational(3,2)*x+3] and 3*(-2)+6==0',figure='droite-02'),
E('Une droite verticale',r"""Quelle droite représente $x=2$ ? Donner un vecteur directeur non nul et expliquer pourquoi on ne peut pas l’écrire $y=mx+p$.""",
r"""Elle contient tous les points d’abscisse 2 : c’est une verticale. Un directeur est $\res{(0;1)}$. Pour la même abscisse 2, elle contient une infinité d’ordonnées ; elle ne peut donc représenter une fonction de $x$. Une équation réduite de la forme demandée n’existe pas.""",
'Reconnaître la coordonnée fixe et le déplacement parallèle possible.','assert Matrix([0,1])!=Matrix([0,0]) and 2==2',figure='droite-03'),
E('Lire une pente',r"""Une droite passe par $A(0;-1)$ et $B(3;5)$. Calculer sa pente et son équation réduite.""",
r"""La pente vaut $(5-(-1))/(3-0)=6/3=\res2$. Le point $A$ est sur l’axe des ordonnées, donc l’ordonnée à l’origine vaut $-1$. L’équation est $\res{y=2x-1}$. Le point $B$ vérifie bien $5=2\times3-1$.""",
'Calculer variation d’ordonnée divisée par variation d’abscisse.','assert Rational(5+1,3)==2 and 2*3-1==5',figure='droite-04'),
E('Un point et une pente',r"""Donner une équation de la droite de pente $-2$ passant par $A(1;3)$.""",
r"""Elle s’écrit $y=-2x+p$. En remplaçant par les coordonnées de $A$, $3=-2+p$, donc $p=5$. L’équation cherchée est $\res{y=-2x+5}$. Le point $(2;1)$ permet un second repère pour le tracé : avancer de 1 fait descendre de 2.""",
'Utiliser le point pour déterminer l’ordonnée à l’origine.','assert solve(3-(-2+p),p)==[5]',figure='droite-05'),
E('Un point et un directeur',r"""Déterminer une équation de la droite passant par $A(2;1)$ et de directeur $(3;-2)$.""",
r"""Un point $M(x;y)$ est sur la droite si $\det((3;-2);(x-2;y-1))=0$. Cela donne $3(y-1)+2(x-2)=0$, soit $\res{2x+3y-7=0}$. On vérifie $A$ : $4+3-7=0$. Le point $A+(3;-2)=(5;-1)$ vérifie aussi l’équation.""",
'Annuler le déterminant entre un directeur et le déplacement depuis le point.','assert expand(3*(y-1)+2*(x-2))==2*x+3*y-7 and 2*5+3*(-1)-7==0',figure='droite-06'),
E('Deux points quelconques',r"""Déterminer l’équation réduite de $(AB)$ pour $A(-1;4)$ et $B(3;-2)$.""",
r"""La pente est $(-2-4)/(3-(-1))=-6/4=-3/2$. Dans $4=(-3/2)(-1)+p$, on obtient $p=5/2$. Donc $\res{y=-\tfrac32x+\tfrac52}$. Une équation cartésienne équivalente est $3x+2y-5=0$. Les deux points vérifient les deux écritures.""",
'Calculer la pente puis utiliser un des points pour trouver p.','assert Rational(-2-4,3+1)==-Rational(3,2) and 3*(-1)+2*4-5==0 and 3*3+2*(-2)-5==0',figure='droite-07'),
E('Parallèles ou confondues ?',r"""Comparer les droites $d_1:y=2x-1$, $d_2:4x-2y-2=0$ et $d_3:y=2x+3$.""",
r"""La deuxième équation se réduit à $y=2x-1$ : $d_1$ et $d_2$ sont confondues. $d_3$ a la même pente 2 mais une ordonnée à l’origine différente ; elle est parallèle et distincte des deux premières. Il faut comparer les deux coefficients pour distinguer ces deux situations.""",
'Mettre les équations sous la même forme avant de comparer.','assert solve(4*x-2*y-2,y)==[2*x-1] and -1!=3',figure='droite-08'),
E('Une intersection',r"""Déterminer l’intersection de $d:y=2x+1$ et $e:y=-x+7$.""",
r"""À l’intersection, les ordonnées sont égales : $2x+1=-x+7$. Donc $3x=6$, soit $x=2$. Puis $y=5$. Le point est $\res{I(2;5)}$. Contrôle dans les deux équations : $2\times2+1=5$ et $-2+7=5$. Les pentes sont distinctes, donc cette intersection est unique.""",
'Égaliser les ordonnées puis vérifier le couple trouvé.','assert solve([y-2*x-1,y+x-7],[x,y])=={x:2,y:5}',figure='droite-09'),
E('Intersection avec une verticale',r"""Trouver le point commun à $x=-2$ et $3x+2y=8$.""",
r"""On remplace $x$ par $-2$ dans la seconde équation : $-6+2y=8$, donc $2y=14$ et $y=7$. L’intersection est $\res{(-2;7)}$. Aucune pente de la verticale n’est nécessaire : la substitution suffit.""",
'Utiliser directement la coordonnée imposée par la verticale.','assert 3*(-2)+2*7==8',figure='droite-10'),
E('Des tarifs et des droites',r"""Deux livreurs facturent respectivement $A(d)=5+2d$ et $B(d)=11+d$, pour une distance $d\ge0$ en kilomètres. Comparer leurs tarifs selon la distance.""",
r"""L’égalité donne $5+2d=11+d$, soit $d=6$ ; le prix commun est 17 euros. La différence $A(d)-B(d)=d-6$ est négative avant 6 et positive après. Donc $A$ est moins cher pour $0\le d<6$, les tarifs sont égaux à 6 km, puis $B$ est moins cher pour $d>6$.""",
'Interpréter une intersection puis étudier le signe de la différence.','assert solve(5+2*x-11-x,x)==[6] and 5+2*6==17',figure='droite-11'),
E('Une famille de droites',r"""Pour $m\in\mathbb R$, on considère $d_m:y=mx+2-m$. Montrer qu’elles passent toutes par un même point. Laquelle est parallèle à $y=3x-5$ ?""",
r"""On réécrit $y=m(x-1)+2$. Pour $x=1$, le terme contenant $m$ s’annule et $y=2$. Toutes les droites passent par $\res{P(1;2)}$. Pour être parallèle à la droite donnée, il faut la pente $m=3$. On obtient $\res{d_3:y=3x-1}$, distincte de $y=3x-5$.""",
'Faire apparaître une abscisse qui élimine le paramètre.','assert (p*x+2-p).subs(x,1)==2 and (3*x+2-3)==3*x-1',figure='droite-12'),
E('Un alignement à deux méthodes',r"""$A(-2;1)$, $B(2;3)$ et $C(6;5)$. Montrer leur alignement par une équation de droite, puis par un déterminant.""",
r"""La pente de $(AB)$ vaut $2/4=1/2$, et son équation est $y=x/2+2$. Pour $C$, $6/2+2=5$ : il appartient donc à $(AB)$. Avec les vecteurs, $\vect{AB}=(4;2)$ et $\vect{AC}=(8;4)$ ont un déterminant $4\times4-2\times8=0$. Les deux preuves établissent le même alignement.""",
'Changer de registre pour contrôler le résultat.','assert Rational(6,2)+2==5 and 4*4-2*8==0',figure='droite-13'),
E('Un système à interpréter',r"""Discuter les solutions des systèmes formés de $x+2y=4$ avec, d’une part, $2x+4y=8$, et d’autre part $2x+4y=10$.""",
r"""Dans le premier cas, la seconde équation est le double de la première : les deux droites sont confondues et le système a une infinité de solutions, tous les points de $x+2y=4$. Dans le second, la première imposerait $2x+4y=8$, incompatible avec 10 : le système n’a aucune solution. Les droites sont alors parallèles distinctes.""",
'Détecter les équations proportionnelles et vérifier les constantes.','assert expand(2*(x+2*y-4))==2*x+4*y-8 and 8!=10',figure='droite-14'),
E('Une médiane à déterminer',r"""$A(0;4)$, $B(-2;0)$ et $C(4;0)$. Déterminer une équation de la médiane issue de $A$, puis son intersection avec la droite $y=2$.""",
r"""Le milieu de $[BC]$ est $I(1;0)$. La droite $(AI)$ a une pente $(0-4)/(1-0)=-4$, donc $\res{y=-4x+4}$. Pour $y=2$, $2=-4x+4$, d’où $x=1/2$. L’intersection est $\res{(1/2;2)}$, qui est aussi le milieu de $[AI]$ ; cela fournit un contrôle supplémentaire.""",
'Construire le point géométrique nécessaire avant l’équation.','assert Rational(-2+4,2)==1 and solve(2-(-4*x+4),x)==[Rational(1,2)]',figure='droite-15')
],reperes=['Équations réduite et cartésienne','Vecteur directeur et pente','Alignement et parallélisme','Systèmes et intersections'],deco='vecteursplan')
