PREUVES=[
('Pourquoi le produit de deux négatifs est-il positif ?',r'''
\editionEtape{Partir de l’opposé}Soient $a$ et $b$ deux nombres positifs. Comme $b+(-b)=0$, multiplier par $a$ donne $ab+a(-b)=0$ par distributivité. Ainsi $a(-b)$ est l’opposé de $ab$ : $a(-b)=-ab$.
\editionEtape{Changer aussi le premier signe}De même, $a+(-a)=0$. En multipliant par $-b$, on obtient $a(-b)+(-a)(-b)=0$. On sait que $a(-b)=-ab$ ; donc $(-a)(-b)$ est l’opposé de $-ab$, c’est-à-dire $ab$.
\editionEtape{Ce que prouve le raisonnement}La règle des signes est imposée par la distributivité et par la notion d’opposé : ce n’est pas une convention isolée à mémoriser. Le cas d’un facteur nul se traite à part : le produit vaut 0.
\editionRetenir{Deux facteurs négatifs donnent un produit positif, parce que ce produit doit être l’opposé d’un produit négatif pour que la distributivité reste vraie.}'''),
('Pourquoi diviser par une fraction revient-il à multiplier par son inverse ?',r'''
\editionEtape{Utiliser la définition du quotient}Pour $v\ne0$, le quotient $u:v$ est l’unique nombre $q$ tel que $q\times v=u$.
\editionEtape{Tester une expression}L’inverse de $v$ vérifie $v\times\frac1v=1$. Le nombre $u\times\frac1v$, multiplié par $v$, donne $u\times\left(\frac1v\times v\right)=u$. C’est donc le quotient $u:v$.
\editionEtape{Appliquer aux fractions}Si $v=\frac cd$ avec $c$ et $d$ non nuls, son inverse est $\frac dc$, car $\frac cd\times\frac dc=1$. Ainsi $\frac ab:\frac cd=\frac ab\times\frac dc$, tous les dénominateurs étant non nuls.
\editionEtape{Un exemple contrôlé}$\frac34:\frac25=\frac34\times\frac52=\frac{15}{8}$. En sens inverse : $\frac{15}{8}\times\frac25=\frac34$. On inverse uniquement le diviseur.
\editionRetenir{Pour contrôler un quotient, remultiplier le résultat par le diviseur : on doit retrouver le dividende.}'''),
('Le théorème de Pythagore par une comparaison d’aires',r'''
\editionEtape{Construire la figure}On place quatre triangles rectangles identiques, de côtés de l’angle droit $a$ et $b$ et d’hypoténuse $c$, dans un carré de côté $a+b$. Le quadrilatère central a quatre côtés de longueur $c$. Ses angles sont droits, car les deux angles aigus d’un triangle rectangle ont pour somme $90^\circ$ : c’est un carré.
\figureGeo{preuve-pythagore}
\editionEtape{Compter deux fois la même aire}Le grand carré a pour aire $(a+b)\times(a+b)$. La somme des aires des quatre triangles et du carré central vaut $4\times\frac{ab}2+c^2=2ab+c^2$.
\editionEtape{Comparer}En découpant autrement le carré de côté $a+b$, en deux carrés de côtés $a$ et $b$ et deux rectangles de côtés $a$ et $b$, son aire vaut aussi $a^2+b^2+2ab$. Donc $a^2+b^2+2ab=2ab+c^2$, et en retirant $2ab$ : $\res{a^2+b^2=c^2}$.
\editionRetenir{Le théorème compare les aires des carrés construits sur les côtés. La preuve utilise l’hypothèse du triangle rectangle : elle est essentielle.}'''),
('Les trois théorèmes de la droite des milieux',r'''
\editionEtape{Un premier parallélogramme}Dans le triangle ABC, I est le milieu de $[AB]$ et J celui de $[AC]$. Le demi-tour de centre J transforme I en K : J est le milieu de $[IK]$. Les diagonales $[AC]$ et $[IK]$ du quadrilatère AICK ont le même milieu J : AICK est un parallélogramme. Donc $(CK)\parallel(AB)$ et $CK=AI$.
\figureGeo{preuve-milieux}
\editionEtape{Un second parallélogramme}Comme I est le milieu de $[AB]$, $AI=IB$, donc $CK=IB$ ; de plus $(CK)\parallel(IB)$. Le quadrilatère non croisé IBCK a deux côtés opposés parallèles et de même longueur : c’est un parallélogramme. Ainsi $(IK)\parallel(BC)$ et $IK=BC$. Comme J est le milieu de $[IK]$ : $\res{(IJ)\parallel(BC)}$ et $\res{IJ=\frac{BC}2}$. Ce sont les théorèmes 1 et 2.
\editionEtape{Le troisième théorème}La parallèle $(d)$ à $(BC)$ passant par I coupe $(AC)$ en un point M. D’après le théorème 1, la droite $(IJ)$ est elle aussi parallèle à $(BC)$ et passe par I. Par un point, il ne passe qu’une seule parallèle à une droite donnée : $(IJ)=(d)$. Les droites $(d)$ et $(AC)$ n’ayant qu’un point commun, $M=J$ : $(d)$ coupe $[AC]$ en son milieu.
\editionRetenir{Les théorèmes de la droite des milieux reposent sur les propriétés du demi-tour et du parallélogramme vues en Cinquième. Le troisième utilise l’unicité de la parallèle.}''')
]
OUTILS=[
('Calculs et algèbre',r'''
\editionEtape{Relatifs et fractions}Prévoir le signe d’un produit ou d’un quotient avant de calculer. Pour additionner des fractions, utiliser un même dénominateur. Pour multiplier, multiplier les numérateurs entre eux et les dénominateurs entre eux. Pour diviser par un nombre non nul, multiplier par son inverse.
\editionEtape{Puissances et racines}$a^n$ est le produit de $n$ facteurs égaux à $a$. $a^m\times a^n=a^{m+n}$ et $a^n\times b^n=(ab)^n$. Pour $b$ positif, $\sqrt b$ est le nombre positif dont le carré vaut $b$ ; on l’encadre avec deux carrés parfaits.
\editionEtape{Distributivité}$k(a+b)=ka+kb$ et $k(a-b)=ka-kb$. Développer va du produit vers la somme ; factoriser fait le chemin inverse. $-(a-b)=-a+b$. Réduire seulement des termes de même nature.
\editionEtape{Équation}Développer et réduire, effectuer la même opération sur les deux membres, isoler l’inconnue, puis vérifier dans l’équation initiale et dans le contexte.
\editionRetenir{Une égalité exacte s’écrit avec $=$, une valeur arrondie avec $\approx$. Conserver le résultat exact jusqu’au dernier calcul.}'''),
('Proportionnalité et grandeurs',r'''
\editionEtape{Proportionnalité}Coefficient, linéarité, retour à l’unité ou produits en croix : pour $b\ne0$ et $d\ne0$, $\frac ab=\frac cd$ équivaut à $ad=bc$. Une proportionnalité se représente par des points alignés avec l’origine.
\editionEtape{Ratios et partages}Partager selon le ratio $a:b:c$ : compter $a+b+c$ parts, calculer une part, puis multiplier. L’ordre des nombres d’un ratio compte.
\editionEtape{Pourcentages}Hausse de $t\,\%$ : multiplier par $1+\frac t{100}$. Baisse de $t\,\%$ : multiplier par $1-\frac t{100}$. Évolutions successives : multiplier les coefficients.
\editionEtape{Grandeurs quotients}$v=\frac dt$, $q=\frac Vt$, $\rho=\frac mV$. $1$ h $=3\,600$ s ; de km/h à m/s, diviser par 3,6. $1$ m$^3=1\,000$ L et $1$ L $=1$ dm$^3$.
\editionEtape{Aires et volumes}Triangle : $\frac{b\times h}2$. Disque : $\pi r^2$. Prisme et cylindre : $\mathcal B\times h$. Pyramide et cône : $\frac13\mathcal B\times h$.
\editionRetenir{Avant de calculer avec deux mesures, choisir des unités compatibles et écrire l’unité du résultat.}'''),
('Choisir un outil géométrique',r'''
\editionEtape{Droites remarquables}M est sur la médiatrice de $[AB]$ si et seulement si $MA=MB$. Hauteur : perpendiculaire issue d’un sommet. Médiane : sommet et milieu du côté opposé ; elle partage l’aire en deux.
\editionEtape{Translations et parallélogrammes}Une translation conserve longueurs, angles et aires ; si A a pour image A’ et B pour image B’, ABB’A’ est un parallélogramme. Diagonales de même milieu : parallélogramme ; de plus de même longueur : rectangle ; perpendiculaires : losange.
\editionEtape{Des milieux dans un triangle}Deux milieux : parallélisme et moitié du troisième côté. Un milieu et une parallèle : un nouveau milieu.
\editionEtape{Triangle rectangle}Pythagore pour une longueur ; réciproque pour prouver un angle droit ; contraposée pour prouver qu’il n’y en a pas. Le centre du cercle circonscrit est le milieu de l’hypoténuse ; un triangle inscrit dans un demi-cercle est rectangle.
\editionRetenir{Une preuve cite ses données et la propriété utilisée. Un codage de l’énoncé est une donnée ; une mesure sur le dessin n’est qu’un indice.}'''),
('Données, hasard et programmation',r'''
\editionEtape{Statistiques}Moyenne pondérée : somme des produits valeur $\times$ effectif, divisée par l’effectif total. Médiane : ranger, puis partager la série en deux parties de même effectif. Étendue : maximum moins minimum. Tableur : MOYENNE, MEDIANE, MAX, MIN, NB.
\editionEtape{Probabilités}Écrire l’univers, puis l’événement comme ensemble d’issues. $P(\overline A)=1-P(A)$. $A\cap B$ : issues communes ; $A\cup B$ : issues d’au moins un des deux. Deux épreuves : arbre ou tableau à double entrée.
\editionEtape{Fréquences}Une fréquence observée fluctue d’une série à l’autre ; elle donne une approximation de la probabilité, sans la remplacer.
\editionEtape{Scripts}Repérer le déclencheur, initialiser la variable, suivre les blocs dans l’ordre, compter les tours, tester les cas limites d’une condition. Dans un tableur, une référence relative change quand on recopie une formule.
\editionRetenir{Après correction, refaire la question sans aide et expliquer l’idée qui l’a résolue : le but est de retrouver la méthode.}''')
]
