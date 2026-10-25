from modele import *

chapitre(11,'information-chiffree','Proportions et évolutions','4 · Statistiques et probabilités',
 'Pourcentages · Références · Coefficients multiplicateurs',
 ['Identifier le total de référence d’une proportion.','Calculer évolutions successives et réciproques.','Lire une information chiffrée de manière critique.'],
 ['Fractions et calcul décimal.'],[
r'''\essSection{1}{Proportions et pourcentages}
\begin{definition}Si une partie contient $n$ éléments parmi $N>0$, sa proportion est $p=n/N$. L’écriture $25\,\%$ signifie $25/100=0{,}25$. Ainsi $n=pN$ et, si $p>0$, $N=n/p$.\end{definition}
\begin{propriete}Si $A$ est une partie de $B$, elle-même partie de $E$, la proportion de $A$ dans $E$ est le produit de la proportion de $A$ dans $B$ par celle de $B$ dans $E$.\end{propriete}
\begin{exemple}40\,\% d’une classe fait du sport ; parmi ces élèves, 30\,\% nagent. Les nageurs considérés représentent $0{,}40\times0{,}30=0{,}12$, soit 12\,\% de la classe.\end{exemple}
\begin{attention}Passer de 20\,\% à 25\,\% représente 5 points de pourcentage, mais une hausse relative de $(25-20)/20=25\,\%$. Toujours nommer le total ou la valeur de départ.\end{attention}
\begin{savoirfaire}[Comparer des groupes]On additionne des effectifs avant de calculer une proportion globale. Une moyenne simple de deux pourcentages n’est valable que si leurs populations ont le même effectif.\end{savoirfaire}''',
r'''\essSection{2}{Évolutions multiplicatives}
\begin{definition}De $V_1>0$ à $V_2$, la variation absolue est $V_2-V_1$, le coefficient multiplicateur $C=V_2/V_1$, et le taux d’évolution $t=(V_2-V_1)/V_1=C-1$. Ainsi $V_2=V_1(1+t)$.\end{definition}
\begin{propriete}Pour deux évolutions successives, les coefficients se multiplient : $C=(1+t_1)(1+t_2)$. Le taux global vaut $C-1$. L’évolution réciproque a pour coefficient $1/C$ et pour taux $1/C-1$.\end{propriete}
\begin{exemple}Après une hausse de 20\,\% puis une baisse de 20\,\%, le coefficient vaut $1{,}2\times0{,}8=0{,}96$ : la baisse globale est de 4\,\%. Pour annuler une hausse de 20\,\%, la baisse nécessaire vaut $1-1/1{,}2=1/6$, soit environ 16,67\,\%.\end{exemple}
\begin{savoirfaire}[Tableur]Écrire un taux sous forme de pourcentage ou de décimal, puis une formule du type \code{=B2*(1+C2)} pour la valeur finale. Pour retrouver le départ, diviser par le coefficient ; ne pas soustraire le même pourcentage.\end{savoirfaire}
\otIntertitre{Interpréter}
Vérifier l’unité, les dates, le périmètre et la référence de comparaison. Une évolution d’une commune ne décrit pas automatiquement celle de son agglomération.'''
],[
E('Calculer une proportion',r"""Parmi 240 élèves, 84 viennent à vélo. Donner leur proportion sous forme de fraction irréductible, décimale et de pourcentage.""",
r"""La référence est l’ensemble des 240 élèves : $84/240=\res{7/20}=\res{0{,}35}=\res{35\,\%}$. Les trois écritures décrivent le même rapport. L’effectif 84 reste un nombre d’élèves, tandis que 0,35 est une proportion sans unité.""",
'Diviser la partie par le total et changer d’écriture.','assert Rational(84,240)==Rational(7,20)==Rational(35,100)'),
E('Appliquer un pourcentage',r"""Un prix de 80 euros bénéficie d’une remise de 15\,\%. Calculer la remise puis le prix payé.""",
r"""La remise vaut $80\times0{,}15=12$ euros. Le prix final est $80-12=\res{68\text{ euros}}$, ou directement $80\times0{,}85$. Le coefficient multiplicateur est 0,85 car il reste 85\,\% du prix initial.""",
'Calculer la part retirée ou utiliser directement le coefficient restant.','assert 80*Rational(15,100)==12 and 80*Rational(85,100)==68'),
E('Retrouver le total',r"""54 adhérents représentent 18\,\% d’une association. Combien y a-t-il d’adhérents ?""",
r"""Notons $N$ le total. On a $0{,}18N=54$, donc $N=54/0{,}18=\res{300}$. Contrôle : $18\,\%$ de 300 vaut bien 54. Multiplier 54 par 18\,\% aurait calculé une partie d’une partie et non le total cherché.""",
'Diviser l’effectif connu par sa proportion.','assert Rational(54)/Rational(18,100)==300'),
E('Du départ à l’arrivée',r"""Une quantité passe de 120 à 150. Calculer la variation absolue, le coefficient multiplicateur et le taux d’évolution.""",
r"""La variation absolue vaut $150-120=\res{30}$. Le coefficient est $150/120=\res{1{,}25}$. Le taux est $1{,}25-1=\res{25\,\%}$. Ces trois réponses sont complémentaires : une différence, un rapport et une variation relative.""",
'Utiliser la valeur de départ comme dénominateur du taux.','assert 150-120==30 and Rational(150,120)==Rational(5,4)'),
E('Une baisse',r"""Une consommation passe de 250 à 210 kWh. Calculer son taux d’évolution.""",
r"""La variation vaut $210-250=-40$ kWh. Rapportée à la valeur initiale, elle donne $-40/250=-0{,}16$, soit $\res{-16\,\%}$. Le coefficient multiplicateur est 0,84. Le signe négatif exprime la baisse, et la valeur absolue 16\,\% sa proportion.""",
'Conserver le signe de la variation et la bonne référence.','assert Rational(210-250,250)==-Rational(16,100)'),
E('Un pourcentage de pourcentage',r"""Dans un lycée de 800 élèves, 45\,\% suivent une option. Parmi eux, 40\,\% choisissent le théâtre. Combien d’élèves choisissent le théâtre, et quelle part du lycée représentent-ils ?""",
r"""Les élèves de l’option sont $800\times0{,}45=360$. Ceux de théâtre sont $360\times0{,}40=\res{144}$. La proportion dans tout le lycée vaut $0{,}45\times0{,}40=0{,}18$, soit $\res{18\,\%}$. Les 40\,\% de l’énoncé portaient seulement sur les 360 élèves de l’option.""",
'Identifier les ensembles emboîtés avant de multiplier les proportions.','assert 800*Rational(45,100)*Rational(40,100)==144 and Rational(144,800)==Rational(18,100)',figure='proportions-emboitees'),
E('Deux évolutions successives',r"""Un prix de 200 euros augmente de 10\,\%, puis baisse de 15\,\%. Calculer le prix final et le taux global.""",
r"""Les coefficients sont 1,10 puis 0,85. Leur produit vaut $0{,}935$. Le prix final est $200\times0{,}935=\res{187\text{ euros}}$ ; le taux global est $0{,}935-1=\res{-6{,}5\,\%}$. Additionner les deux taux aurait ignoré que la seconde évolution porte sur un prix déjà modifié.""",
'Multiplier les coefficients plutôt qu’additionner les taux.','assert 200*Rational(110,100)*Rational(85,100)==187'),
E('L’évolution réciproque',r"""Une population augmente de 25\,\%. Quel pourcentage de baisse la ramènerait exactement à son effectif initial ?""",
r"""Le coefficient de hausse est 1,25. Le coefficient réciproque vaut $1/1{,}25=0{,}8$ ; le taux correspondant est donc $\res{-20\,\%}$. Contrôle sur 100 individus : la hausse donne 125, puis une baisse de 20\,\% de 125 retire 25 et ramène à 100.""",
'Inverser le coefficient multiplicateur.','assert 1/Rational(125,100)==Rational(80,100)'),
E('Points et pourcentage',r"""Un taux de réussite passe de 60\,\% à 72\,\%. Donner la hausse en points et la hausse relative.""",
r"""La différence est $72-60=\res{12\text{ points}}$. La hausse relative vaut $(72-60)/60=0{,}20$, soit $\res{20\,\%}$. Les deux formulations sont correctes si leur sens est précisé. Dire seulement « une hausse de 12\,\% » serait ici ambigu et ne correspondrait pas au taux relatif.""",
'Distinguer différence de taux et évolution relative de ce taux.','assert 72-60==12 and Rational(72-60,60)==Rational(20,100)'),
E('Une proportion globale',r"""Une classe de 20 élèves compte 80\,\% de réussites, une autre de 30 élèves en compte 60\,\%. Calculer le taux de réussite de l’ensemble.""",
r"""Les effectifs de réussite sont 16 et 18. Au total, il y a 34 réussites sur 50 élèves : $\res{68\,\%}$. La moyenne simple $(80+60)/2=70\,\%$ serait incorrecte, car les classes n’ont pas le même effectif. On peut aussi utiliser une moyenne pondérée par 20 et 30.""",
'Revenir aux effectifs avant de calculer le pourcentage global.','assert (20*Rational(8,10)+30*Rational(6,10))/50==Rational(68,100)'),
E('Retrouver un prix hors taxe',r"""Un prix TTC est de 144 euros avec une TVA de 20\,\%. Trouver le prix hors taxe et le montant de TVA.""",
r"""Le TTC vaut $1{,}20$ fois le hors taxe. Donc $HT=144/1{,}20=\res{120\text{ euros}}$. La TVA vaut $144-120=\res{24\text{ euros}}$. Retirer 20\,\% de 144 donnerait 115,20 euros et utiliserait la mauvaise référence : la taxe est calculée sur le HT.""",
'Retrouver le départ en divisant par le coefficient.','assert Rational(144)/Rational(12,10)==120 and 144-120==24'),
E('Une baisse suivie d’un retour',r"""Un appareil perd 30\,\% de sa valeur. De quel taux doit ensuite augmenter sa valeur pour retrouver celle du départ ? Donner un résultat exact puis un arrondi au dixième de pourcentage.""",
r"""Après la perte, le coefficient est 0,70. Le retour exige $1/0{,}70=10/7$. Le taux de hausse est donc $10/7-1=\res{3/7}$, soit environ $\res{42{,}9\,\%}$. La hausse est supérieure à 30\,\% parce qu’elle part d’une valeur devenue plus petite.""",
'Calculer un taux réciproque et préciser son écriture en pourcentage.','assert 1/Rational(7,10)-1==Rational(3,7)'),
E('Un seuil après plusieurs hausses',r"""Un capital de 500 euros est multiplié chaque année par 1,1. Après combien d’années dépasse-t-il 700 euros pour la première fois ? On autorise un tableau ou une boucle, sans logarithme.""",
r"""Les valeurs aux années 1 à 4 sont 550 ; 605 ; 665,50 ; 732,05 euros. Le premier dépassement est donc à $\res{4\text{ ans}}$. Le coefficient 1,1 est supérieur à 1 : les valeurs augmentent, ce qui justifie que les années précédentes ne pouvaient pas dépasser 700 après l’échec à l’année 3.""",
'Itérer le coefficient jusqu’au premier franchissement.','assert 500*Rational(11,10)**3<=700<500*Rational(11,10)**4'),
E('Des données de population',r"""L’Insee indique 327734 habitants pour la commune de Nantes et 267991 pour celle de Bordeaux au 1er janvier 2023. Calculer l’écart puis le pourcentage de plus de Nantes par rapport à Bordeaux, arrondi au dixième. \par\smallskip\legende{Source : Insee Focus 374, figure 3b, décembre 2025, \url{https://www.insee.fr/fr/statistiques/8682718}. Il s’agit des communes, pas des métropoles.}""",
r"""L’écart est $327734-267991=\res{59743\text{ habitants}}$. La référence demandée est Bordeaux : le rapport d’écart vaut $59743/267991\approx0{,}22293$. Nantes compte donc environ $\res{22{,}3\,\%}$ d’habitants de plus dans ce périmètre et à cette date. Inverser la comparaison donnerait un autre pourcentage.""",
'Lire le périmètre statistique et choisir explicitement la référence.','assert 327734-267991==59743 and abs(100*59743/267991-22.2929)<0.0001'),
E('Un taux constant à retrouver',r"""Un prix augmente d’un même taux positif lors de deux hausses successives. Au total, il augmente de 21\,\%. Déterminer ce taux sans tâtonnement.""",
r"""Notons $C>1$ le coefficient de chaque hausse. Le coefficient global vaut $C^2=1{,}21$. Comme $C>0$, $C=\sqrt{1{,}21}=1{,}1$. Chaque hausse est donc de $\res{10\,\%}$. La valeur $-1{,}1$, autre solution algébrique du carré, ne représente pas un coefficient de hausse positif.""",
'Traduire la répétition du même coefficient par un carré.','assert Rational(11,10)**2==Rational(121,100)')
],reperes=['Proportion et pourcentages emboîtés','Variations additive et multiplicative','Évolutions successives et réciproques','Lecture critique de données réelles'],deco='statistique')

serie_stats=tableau(['Valeur','$2$','$4$','$6$','$8$'],[['Effectif','$1$','$3$','$4$','$2$']])
classes_stats=tableau(['Classe (min)','$[0;10[$','$[10;20[$','$[20;30[$','$[30;40]$'],[['Effectif','$4$','$8$','$6$','$2$']])

chapitre(12,'statistiques','Statistique descriptive','4 · Statistiques et probabilités',
 'Moyenne · Médiane · Quartiles · Écart type · Classes',
 ['Choisir des indicateurs de position et de dispersion.','Lire barres, boîtes, histogrammes et cumuls.','Distinguer calcul exact et estimation pour des données groupées.'],
 ['Proportions et racines carrées.'],[
r'''\essSection{1}{Résumer sans tout confondre}
\begin{definition}Pour des valeurs $x_i$ d’effectifs $n_i$, avec $N=\sum n_i>0$, la moyenne est $\bar x=\sum n_ix_i/N$. Une médiane partage la série ordonnée en deux groupes contenant chacun au moins la moitié des valeurs. Ici, pour un effectif pair, on utilise la moyenne des deux valeurs centrales.\end{definition}
\begin{definition}Dans la série ordonnée, $Q_1$ est la valeur dont le rang est le plus petit entier supérieur ou égal à $N/4$ ; $Q_3$ est celle dont le rang est le plus petit entier supérieur ou égal à $3N/4$. Pour $N=10$ : rangs 3 et 8. L’écart interquartile est $Q_3-Q_1$ ; l’étendue est maximum moins minimum. Une boîte à moustaches repère minimum, $Q_1$, médiane, $Q_3$ et maximum.\end{definition}
\begin{definition}L’écart type est
\[\sigma=\sqrt{\frac{\sum n_i(x_i-\bar x)^2}{N}}.\]
On divise par l’effectif total $N$, et non par $N-1$. Un grand écart type signale une plus forte dispersion autour de la moyenne ; il a la même unité que les données.
\end{definition}
\begin{propriete}Ajouter $b$ à toutes les données augmente la moyenne de $b$ et laisse l’écart type inchangé. Multiplier toutes les données par $a$ multiplie la moyenne par $a$ et l’écart type par $|a|$.\end{propriete}''',
r'''\essSection{2}{Regrouper et interpréter}
\begin{savoirfaire}[Classes de même amplitude]
L’histogramme représente les effectifs ou fréquences par les aires de rectangles ; pour des classes de même largeur, les hauteurs peuvent être proportionnelles aux effectifs. Le polygone des fréquences cumulées place aux bornes supérieures les proportions accumulées.
\end{savoirfaire}
\begin{propriete}Si les moyennes de classe $m_j$ et les effectifs $n_j$ sont connus, la moyenne totale est exactement $\sum n_jm_j/\sum n_j$. Si seuls les intervalles sont connus, utiliser leurs centres fournit une estimation, exacte dans le modèle de répartition uniforme de chaque classe.\end{propriete}
\begin{savoirfaire}[Médiane groupée]
Localiser la classe qui contient le passage de 50\,\%. Sous l’hypothèse uniforme dans cette classe, interpoler linéairement : on parcourt la fraction de largeur correspondant à l’effectif nécessaire pour atteindre $N/2$.
\end{savoirfaire}
\begin{attention}Une moyenne ne décrit pas toute une distribution. Comparer aussi les dispersions et regarder les graphiques. Une valeur extrême peut beaucoup déplacer la moyenne et laisser la médiane inchangée.\end{attention}
\otIntertitre{Avec un tableur}
Contrôler la convention d’écart type utilisée par le logiciel. Conserver le tableau d’effectifs : la moyenne de moyennes de classe doit être pondérée par leurs effectifs.'''
],[
E('Moyenne simple',r"""Calculer la moyenne de $4,6,7,8,10$.""",
r"""La somme est $4+6+7+8+10=35$ pour 5 valeurs. La moyenne est donc $\res{35/5=7}$. Elle se situe entre le minimum 4 et le maximum 10, ce qui est un premier contrôle de cohérence.""",
'Additionner les valeurs puis diviser par leur nombre.','assert Rational(sum([4,6,7,8,10]),5)==7'),
E('Médiane et quartiles',r"""Pour la série ordonnée $1,2,3,4,5,6,7,8$, déterminer la médiane, $Q_1$, $Q_3$ et l’étendue avec les conventions du cours.""",
r"""Les valeurs centrales sont 4 et 5 : la médiane vaut $\res{4{,}5}$. Les rangs des quartiles sont 2 et 6 : $\res{Q_1=2}$ et $\res{Q_3=6}$. L’étendue vaut $8-1=\res7$. Les conventions de rang doivent être précisées pour éviter les différences entre certains logiciels.""",
'Ordonner puis utiliser les rangs adaptés à l’effectif.','assert Rational(4+5,2)==Rational(9,2) and ceiling(8/4)==2 and ceiling(3*8/4)==6'),
E('Une moyenne pondérée',r"""Calculer la moyenne de cette série."""+serie_stats,
r"""L’effectif total est $1+3+4+2=10$. La somme pondérée vaut $2\times1+4\times3+6\times4+8\times2=54$. Ainsi $\res{\bar x=5{,}4}$. Faire la moyenne simple de 2, 4, 6 et 8 aurait donné 5 et aurait oublié leurs effectifs différents.""",
'Pondérer chaque valeur par son nombre d’occurrences.','assert Rational(2+4*3+6*4+8*2,10)==Rational(54,10)',figure='stats-barres'),
E('Lire un secteur',r"""Un diagramme circulaire représente 60 élèves. Un secteur mesure $120^\circ$. Quelle proportion et quel effectif représente-t-il ? Dans un autre diagramme, un demi-cercle représente les 60 élèves : que représente alors un secteur de $120^\circ$ ?""",
r"""Le cercle entier vaut $360^\circ$, donc la proportion est $120/360=\res{1/3}$ et l’effectif $\res{20\text{ élèves}}$. Dans le demi-cercle, la référence n’est plus 360 mais 180 degrés : $120/180=\res{2/3}$, donc $\res{40\text{ élèves}}$. L’angle seul ne donne pas le pourcentage ; il faut connaître l’angle qui représente toute la population.""",
'Rapporter l’angle du secteur à l’angle qui représente le total.','assert Rational(120,360)==Rational(1,3) and 60*Rational(1,3)==20 and Rational(120,180)==Rational(2,3) and 60*Rational(2,3)==40',figure='stats-secteur'),
E('Un écart type court',r"""Calculer la moyenne et l’écart type de la série $2,2,6,6$.""",
r"""La moyenne vaut $(2+2+6+6)/4=4$. Les écarts à la moyenne sont $-2,-2,2,2$ ; leurs carrés valent tous 4. La moyenne de ces carrés vaut 4, et l’écart type vaut $\res{\sigma=2}$. L’écart type n’est pas la moyenne des écarts signés, qui est ici nulle.""",
'Calculer la moyenne des carrés des écarts avant de prendre la racine.','assert sqrt(Rational(sum((a-4)**2 for a in [2,2,6,6]),4))==2'),
E('Même moyenne, dispersion différente',r"""Comparer les séries $A=(4,4,4,4)$ et $B=(1,3,5,7)$ par la moyenne et l’écart type.""",
r"""Les deux moyennes valent 4. Pour $A$, tous les écarts sont nuls, donc $\sigma_A=0$. Pour $B$, les carrés des écarts sont 9, 1, 1 et 9 : leur moyenne vaut 5, donc $\res{\sigma_B=\sqrt5}$. La série $B$ est plus dispersée autour de la même moyenne.""",
'Comparer un couple position-dispersion plutôt que la seule moyenne.','assert Rational(sum([1,3,5,7]),4)==4 and Rational(sum((a-4)**2 for a in [1,3,5,7]),4)==5',figure='stats-dispersion'),
E('Transformer une série',r"""Une série a pour moyenne 12 et écart type 3. On ajoute 5 à toutes ses valeurs. Quels deviennent ces deux indicateurs ? Justifier pour l’écart type. Dans la série initiale, on remplace maintenant chaque valeur $x_i$ par $-2x_i+1$ : donner les nouveaux indicateurs.""",
r"""Après ajout de 5, la moyenne vaut $\res{17}$. Chaque écart devient $(x_i+5)-(12+5)=x_i-12$ ; l’écart type reste $\res3$. Pour la seconde transformation appliquée à la série initiale, la moyenne vaut $-2\times12+1=\res{-23}$. Les écarts sont multipliés par $-2$, donc leurs carrés par 4 et l’écart type par 2 : il vaut $\res6$. Le signe négatif inverse l’ordre des valeurs sans rendre la dispersion négative.""",
'Comparer les écarts avant et après une transformation affine.','assert expand((x+5)-(12+5))==x-12 and 12+5==17 and -2*12+1==-23 and abs(-2)*3==6'),
E('Réunir deux groupes',r"""Un groupe de 12 mesures a une moyenne de 8 ; un autre de 18 mesures une moyenne de 13. Calculer la moyenne des 30 mesures.""",
r"""Les sommes des deux groupes valent $12\times8=96$ et $18\times13=234$. La somme totale vaut 330 pour 30 mesures : $\res{\bar x=11}$. La moyenne simple 10,5 serait fausse, car le groupe dont la moyenne est 13 est plus nombreux.""",
'Retrouver les sommes de groupe avant de réunir les effectifs.','assert Rational(12*8+18*13,30)==11'),
E('Moyenne par classes',r"""On donne les durées suivantes. Estimer la moyenne avec les centres de classes, en explicitant l’hypothèse."""+classes_stats,
r"""Les centres sont 5, 15, 25 et 35 minutes. La moyenne estimée est $(4\times5+8\times15+6\times25+2\times35)/20=\res{18\text{ min}}$. Cette estimation est exacte dans un modèle uniforme dans chaque classe. Les seuls effectifs ne donnent pas la position exacte des valeurs à l’intérieur des intervalles.""",
'Utiliser les centres et annoncer la nature de l’estimation.','assert Rational(4*5+8*15+6*25+2*35,20)==18',figure='stats-histogramme'),
E('Classe médiane et interpolation',r"""Pour les classes et effectifs ci-dessous, déterminer la classe médiane et estimer la médiane sous l’hypothèse uniforme dans cette classe."""+classes_stats,
r"""L’effectif total est 20. Les cumuls sont 4, 12, 18 et 20 ; le passage de 10 observations se fait dans $[10;20[$. Pour atteindre 10 depuis le cumul 4, il faut 6 des 8 observations de la classe, soit $6/8$ de sa largeur. L’estimation est donc $10+(6/8)\times10=\res{17{,}5\text{ min}}$.""",
'Localiser le seuil de 50 % puis interpoler uniquement sous l’hypothèse annoncée.','assert 10+Rational(10-4,8)*10==Rational(35,2)',figure='stats-cumuls'),
E('Un point extrême',r"""Comparer moyenne et médiane de $2,3,4,5,6$ avant et après remplacement de 6 par 100. Que deviennent-elles si l’on supprime ensuite la valeur 100 ?""",
r"""Avant remplacement, moyenne et médiane valent 4. Après remplacement, la somme vaut 114 et la moyenne $\res{22{,}8}$, tandis que la médiane reste $\res4$. Après suppression de 100, la série $2,3,4,5$ a pour moyenne $14/4=\res{3{,}5}$ et pour médiane $(3+4)/2=\res{3{,}5}$. Une modification d’effectif peut déplacer aussi les rangs centraux : la médiane n’est pas toujours inchangée.""",
'Réordonner et mettre à jour à la fois les effectifs et les rangs.','assert Rational(2+3+4+5+6,5)==4 and Rational(2+3+4+5+100,5)==Rational(114,5) and Rational(2+3+4+5,4)==Rational(3+4,2)==Rational(7,2)'),
E('Deux boîtes à moustaches',r"""Une série $A$ a pour résumé $(0;4;6;8;12)$ et une série $B$ pour résumé $(2;5;6;7;10)$, dans l’ordre minimum, $Q_1$, médiane, $Q_3$, maximum. Comparer leur position centrale et leur dispersion.""",
r"""Les deux médianes valent 6. L’écart interquartile de $A$ vaut $8-4=4$, celui de $B$ vaut $7-5=2$. Les étendues valent respectivement 12 et 8. Selon ces deux mesures, $B$ est moins dispersée. Les boîtes ne suffisent pas à connaître les moyennes ni les écarts types exacts.""",
'Lire uniquement les indicateurs contenus dans une boîte.','assert 8-4==4 and 7-5==2 and 12-0==12 and 10-2==8',figure='stats-boites'),
E('L’effet d’un ajout sur la moyenne',r"""Une série de 10 valeurs a une moyenne de 14. On ajoute la valeur 25. Calculer la nouvelle moyenne et expliquer pourquoi elle augmente.""",
r"""La somme initiale vaut 140. Après ajout, la somme vaut 165 et l’effectif 11. La nouvelle moyenne est $\res{15}$. Comme 25 est au-dessus de l’ancienne moyenne, l’ajout tire la moyenne vers le haut. Il ne faut pas conserver le dénominateur 10 après avoir ajouté une observation.""",
'Mettre à jour à la fois la somme et l’effectif.','assert Rational(10*14+25,11)==15'),
E('Moyennes de classes connues',r"""Deux classes de durées contiennent 8 et 12 mesures. Leurs moyennes réelles sont 7 et 16 minutes. Leurs centres sont 5 et 15 minutes. Calculer la moyenne exacte puis l’estimation par centres ; expliquer l’écart.""",
r"""La moyenne exacte est $(8\times7+12\times16)/20=\res{12{,}4\text{ min}}$. L’estimation par centres donne $(8\times5+12\times15)/20=\res{11\text{ min}}$. Les moyennes réelles de classes diffèrent des centres : l’hypothèse qui rendrait l’estimation exacte n’est pas satisfaite. Lorsqu’elles sont connues, il faut utiliser les moyennes réelles.""",
'Distinguer l’information exacte de l’hypothèse de répartition uniforme.','assert Rational(8*7+12*16,20)==Rational(124,10) and Rational(8*5+12*15,20)==11'),
E('Une série à construire',r"""Construire deux séries de quatre réels ayant la même moyenne 5 et la même médiane 5, mais des écarts types différents. Calculer ces écarts types.""",
r"""On peut choisir $A=(4,4,6,6)$ et $B=(0,0,10,10)$. Chaque somme vaut 20 et chaque paire centrale a pour moyenne 5. Pour $A$, les écarts au carré valent tous 1 : $\sigma_A=\res1$. Pour $B$, ils valent tous 25 : $\sigma_B=\res5$. Même moyenne et même médiane n’imposent donc pas la même dispersion.""",
'Construire des valeurs symétriques autour du centre choisi.','assert sum([4,4,6,6])==sum([0,0,10,10])==20 and sum((a-5)**2 for a in [4,4,6,6])==4 and sum((a-5)**2 for a in [0,0,10,10])==100')
],reperes=['Moyenne, médiane et quartiles','Écart type et transformations de données','Histogrammes et polygones cumulés','Moyenne et médiane pour des classes'],deco='statistique')
