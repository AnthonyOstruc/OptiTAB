from modele import *

table_clubs=tableau(['','$C$',r"$\overline C$",'Total'],[['$A$','36','24','60'],['$B$','24','36','60'],['Total','60','60','120']])
table_test=tableau(['','Signal $+$','Signal $-$','Total'],[['Défectueux','18','2','20'],['Conformes','49','931','980'],['Total','67','933','1000']])

chapitre(13,'tableaux-croises','Tableaux croisés et fréquences','4 · Statistiques et probabilités',
 'Variables qualitatives · Marges · Conditions · Filtres',
 ['Lire et compléter des tableaux d’effectifs.','Distinguer fréquences marginale et conditionnelle.','Choisir le bon dénominateur selon la question.'],
 ['Proportions et pourcentages.'],[
r'''\essSection{1}{Deux variables qualitatives}
\begin{definition}Une variable qualitative décrit une catégorie. Elle est nominale si les catégories ne sont pas ordonnées (transport, couleur), ordinale si un ordre a un sens (degré de satisfaction). Un tableau croisé compte les individus pour chaque couple de catégories.\end{definition}
\begin{savoirfaire}[Contrôler un tableau]
Chaque case compte une intersection de deux catégories. La somme d’une ligne donne son total marginal ; celle d’une colonne donne l’autre total marginal. Les deux façons de sommer doivent retrouver le même effectif total.
\end{savoirfaire}
\begin{definition}La fréquence marginale de $A$ est $n_A/N$. La fréquence de $C$ parmi les individus de $A$ est $n_{A\cap C}/n_A$, si $n_A>0$. Elle est conditionnelle : le groupe de référence est restreint à $A$.\end{definition}
\begin{exemple}Si 36 personnes de $A$ sont inscrites à $C$ parmi 60 personnes de $A$, la fréquence est $36/60=60\,\%$. Si $C$ compte 90 personnes au total, la fréquence de $A$ parmi $C$ serait $36/90=40\,\%$.\end{exemple}
\begin{attention}« Parmi les inscrits » et « parmi le groupe A » n’annoncent pas le même dénominateur. Commencer par entourer le groupe de référence.\end{attention}''',
r'''\essSection{2}{Filtrer et comparer}
\begin{savoirfaire}[ET, OU, NON]
Le filtre « $A$ ET $C$ » conserve l’intersection. « $A$ OU $C$ » conserve les individus d’au moins une catégorie, sans compter deux fois ceux des deux. « NON $C$ » conserve le complémentaire dans la population étudiée.
\end{savoirfaire}
\begin{propriete}L’effectif de l’union vérifie $n_{A\cup C}=n_A+n_C-n_{A\cap C}$. Une fréquence globale peut être obtenue en additionnant les effectifs des groupes puis en divisant par le total.\end{propriete}
\begin{savoirfaire}[Tableur ou fichier]
Une ligne représente un individu, une colonne une variable. Filtrer, puis compter les individus retenus. Les fonctions de comptage conditionnel ou un tableau croisé dynamique permettent d’organiser les calculs. Vérifier les modalités manquantes et éviter de mélanger des populations de dates différentes.
\end{savoirfaire}
\begin{attention}Un écart de fréquences décrit une association dans les données. Il ne démontre pas une relation de cause à effet. Des groupes de tailles différentes peuvent aussi rendre une comparaison globale trompeuse.\end{attention}
\otIntertitre{À l’oral}
Dire une fréquence en une phrase complète : catégorie comptée, groupe de référence, valeur. Faire ensuite inverser la question à un camarade et expliquer pourquoi la réponse peut changer.'''
],[
E('Lire les marges',r"""Le tableau décrit deux groupes $A,B$ et l’inscription à un club $C$. Donner le total, l’effectif de $A$, celui de $C$ et celui de $A\cap C$."""+table_clubs,
r"""Le total général est 120. La marge de la ligne donne $n_A=60$ ; la marge de la colonne donne $n_C=60$. La case à leur croisement donne $n_{A\cap C}=36$. Ce dernier nombre ne représente ni tous les membres de $A$, ni tous les inscrits du club, mais ceux qui vérifient les deux conditions.""",
'Distinguer case intérieure et totaux marginaux.','assert 36+24+24+36==120 and 36+24==60'),
E('Une fréquence conditionnelle',r"""À partir du tableau, donner la fréquence de $C$ parmi $A$, puis celle de $C$ parmi $B$."""+table_clubs,
r"""Parmi les 60 individus de $A$, 36 sont dans $C$ : la fréquence est $36/60=\res{60\,\%}$. Parmi les 60 de $B$, 24 sont dans $C$ : $24/60=\res{40\,\%}$. Chaque dénominateur est le total du groupe introduit par « parmi ».""",
'Restreindre le total à la ligne demandée.','assert Rational(36,60)==Rational(6,10) and Rational(24,60)==Rational(4,10)'),
E('Inverser la référence',r"""Dans une enquête, 30 cyclistes sont des élèves de seconde. Il y a 50 cyclistes et 120 élèves de seconde. Calculer la fréquence des secondes parmi les cyclistes et celle des cyclistes parmi les secondes.""",
r"""La première fréquence vaut $30/50=\res{60\,\%}$ ; la seconde vaut $30/120=\res{25\,\%}$. Le numérateur reste identique parce qu’il décrit les mêmes 30 individus. Le dénominateur change avec la population conditionnée. Les deux résultats ne sont donc pas contradictoires.""",
'Conserver l’intersection et changer le dénominateur avec la question.','assert Rational(30,50)==Rational(6,10) and Rational(30,120)==Rational(1,4)'),
E('Compléter avec des pourcentages',r"""Une population compte 200 individus : 80 dans $A$ et 120 dans $B$. Dans $A$, 75\,\% sont satisfaits ; dans $B$, 40\,\% le sont. Construire le tableau croisé satisfait / non satisfait.""",
r"""Dans $A$, les satisfaits sont $0{,}75\times80=60$ et les autres 20. Dans $B$, ils sont $0{,}40\times120=48$ et les autres 72. Les totaux de colonnes sont $\res{108\text{ satisfaits et }92\text{ non satisfaits}}$. Le contrôle $60+20+48+72=200$ retrouve l’effectif général.""",
'Calculer les cases à partir des fréquences de leur groupe.','assert Rational(75,100)*80==60 and Rational(40,100)*120==48 and 60+20+48+72==200'),
E('Nominal ou ordinal ?',r"""Classer les variables « moyen de transport », « avis : mauvais, moyen, bon », « couleur des yeux » et « niveau : débutant, intermédiaire, avancé ».""",
r"""Le moyen de transport et la couleur des yeux sont des variables nominales : aucun ordre naturel unique n’est imposé. L’avis et le niveau sont ordinaux : les catégories ont un ordre explicite. Cela ne les transforme pas en nombres : attribuer des codes 1, 2, 3 ne prouve pas que les écarts entre catégories sont identiques.""",
'Chercher si un ordre des catégories a un sens.','assert len(["transport","couleur"])==2 and len(["avis","niveau"])==2'),
E('Marge et condition',r"""Avec le tableau ci-dessous, calculer la fréquence globale du club, puis la fréquence du groupe $A$ parmi les non-inscrits."""+table_clubs,
r"""La fréquence globale du club est $60/120=\res{50\,\%}$. Parmi les 60 non-inscrits, 24 viennent du groupe $A$ : la seconde fréquence est $24/60=\res{40\,\%}$. Le premier calcul utilise le total général ; le deuxième utilise la marge de la colonne des non-inscrits.""",
'Nommer le dénominateur avant d’effectuer le quotient.','assert Rational(60,120)==Rational(1,2) and Rational(24,60)==Rational(2,5)'),
E('ET, OU et complémentaire',r"""À l’aide du tableau, calculer les effectifs qui vérifient : $A$ et $C$ ; $A$ ou $C$ ; non $C$."""+table_clubs,
r"""« $A$ et $C$ » donne directement 36. Pour « $A$ ou $C$ », on additionne les totaux puis on retire l’intersection comptée deux fois : $60+60-36=\res{84}$. Enfin non $C$ contient $120-60=\res{60}$ personnes. Le « ou » mathématique inclut les personnes qui vérifient les deux conditions.""",
'Utiliser l’inclusion-exclusion pour ne pas doubler l’intersection.','assert 60+60-36==84 and 120-60==60',figure='croise-venn'),
E('Du fichier au tableau',r"""Un fichier de huit individus contient les couples : $(A;O)$, $(B;N)$, $(A;N)$, $(A;O)$, $(B;O)$, $(B;N)$, $(A;N)$, $(B;O)$. Dresser le tableau des effectifs, avec les modalités $O,N$.""",
r"""On compte séparément chaque couple. Dans $A$, il y a 2 $O$ et 2 $N$ ; dans $B$, également 2 $O$ et 2 $N$. Chaque ligne et chaque colonne totalise 4 ; le total général est 8. Pour vérifier, barrer ou cocher chaque ligne du fichier après son comptage évite les oublis et les doubles comptes.""",
'Compter les couples, pas seulement les deux variables séparées.','from collections import Counter\nassert Counter([("A","O"),("B","N"),("A","N"),("A","O"),("B","O"),("B","N"),("A","N"),("B","O")])=={("A","O"):2,("A","N"):2,("B","O"):2,("B","N"):2}'),
E('Comparer des taux avec des effectifs',r"""Une formation $A$ réussit à 18 personnes sur 20 ; une formation $B$ à 72 sur 90. Comparer les fréquences de réussite puis calculer la fréquence globale.""",
r"""$A$ a un taux de $18/20=90\,\%$ ; $B$, $72/90=80\,\%$. Le taux de $A$ est plus élevé, même si $B$ compte plus de réussites en nombre. Globalement, il y a 90 réussites sur 110 personnes, soit $\res{9/11\approx81{,}8\,\%}$. Il faut distinguer effectifs et fréquences.""",
'Comparer les rapports puis réunir les numérateurs et les effectifs.','assert Rational(18,20)>Rational(72,90) and Rational(18+72,20+90)==Rational(9,11)'),
E('Des données réelles de l’Insee',r"""Pour la France hors Mayotte, le RP2023 donne 32987021 hommes et 35107259 femmes, dont respectivement 5934049 et 5674817 ont moins de 15 ans. Calculer la part des moins de 15 ans parmi les hommes, parmi les femmes, puis la part des femmes parmi les moins de 15 ans. Arrondir au dixième de pourcentage.\par\smallskip\legende{Source : Insee, dossier France, POP T4, géographie au 01/01/2026, \url{https://www.insee.fr/fr/statistiques/2011101?geo=FRANCE-1}.}""",
r"""Les trois dénominateurs sont différents. On calcule $5934049/32987021\approx\res{18{,}0\,\%}$, $5674817/35107259\approx\res{16{,}2\,\%}$ et $5674817/(5934049+5674817)\approx\res{48{,}9\,\%}$. La dernière référence est l’ensemble des moins de 15 ans, pas l’ensemble des femmes. Le champ, le millésime et le découpage géographique font partie de l’information.""",
'Lire une donnée réelle en conservant son champ et sa référence.','assert round(100*5934049/32987021,1)==18.0 and round(100*5674817/35107259,1)==16.2 and round(100*5674817/(5934049+5674817),1)==48.9'),
E('Un total à retrouver',r"""Dans le groupe $A$, 24 personnes pratiquent une activité ; elles représentent 60\,\% du groupe. Le groupe $B$ compte 50 personnes, dont 15 pratiquent l’activité. Déterminer l’effectif de $A$ puis la fréquence globale.""",
r"""Le groupe $A$ compte $24/0{,}60=\res{40}$ personnes. Dans l’ensemble, 39 personnes pratiquent l’activité parmi 90 : $39/90=\res{13/30\approx43{,}3\,\%}$. Il faut retrouver le total manquant avant de réunir les groupes ; les deux pourcentages ne se moyennent pas à poids égaux.""",
'Reconstituer le dénominateur manquant puis agréger les effectifs.','assert Rational(24)/Rational(6,10)==40 and Rational(24+15,40+50)==Rational(13,30)'),
E('Une annonce impossible',r"""Une enquête portant sur 35 personnes affirme que « exactement 30\,\% ont répondu oui ». Cette annonce peut-elle correspondre à un effectif entier ? Comment peut-elle devenir cohérente ?""",
r"""Exactement 30\,\% de 35 donnerait $35\times0{,}30=10{,}5$ personnes, impossible pour un effectif. L’annonce peut être cohérente comme pourcentage approximatif : 10 sur 35 font environ 28,6\,\%, et 11 sur 35 environ 31,4\,\%, tous deux proches de 30\,\% à une précision grossière. Il faut annoncer l’arrondi utilisé plutôt que le mot « exactement ».""",
'Vérifier la compatibilité d’une proportion avec un effectif entier.','assert Rational(35)*Rational(3,10)==Rational(21,2) and not Rational(21,2).is_integer'),
E('Des fréquences identiques',r"""Une catégorie $C$ concerne 40\,\% du groupe $A$ et 40\,\% du groupe $B$. Montrer que sa fréquence globale vaut aussi 40\,\%, quels que soient les effectifs positifs des deux groupes.""",
r"""Si les effectifs sont $a$ et $b$, le nombre d’individus de $C$ est $0{,}4a+0{,}4b=0{,}4(a+b)$. En divisant par le total $a+b>0$, on obtient $\res{0{,}4=40\,\%}$. La taille relative des groupes n’a ici aucun effet parce que les deux fréquences conditionnelles sont égales.""",
'Factoriser une proportion commune avant la division.','assert cancel((Rational(2,5)*x+Rational(2,5)*y)/(x+y))==Rational(2,5)'),
E('L’effet d’un recrutement',r"""Un club compte 30 débutants sur 80 membres. On recrute uniquement des débutants. Combien faut-il en recruter au minimum pour que leur part atteigne au moins 50\,\% ?""",
r"""Après $n$ recrutements, leur part est $(30+n)/(80+n)$ avec $n\ge0$. Le dénominateur est positif : l’inégalité à $1/2$ équivaut à $60+2n\ge80+n$, soit $n\ge20$. Il faut $\res{20\text{ personnes}}$. Au seuil, la proportion vaut $50/100=1/2$. Le total augmente lui aussi lors du recrutement.""",
'Faire évoluer simultanément le numérateur et le dénominateur.','assert min(n for n in range(100) if Rational(30+n,80+n)>=Rational(1,2))==20'),
E('Des groupes à pondérer',r"""Une offre $X$ compte 9 satisfaits sur 10 dans le groupe 1 et 24 sur 40 dans le groupe 2. Une offre $Y$ compte 32 sur 40 dans le groupe 1 et 5 sur 10 dans le groupe 2. Comparer les offres dans chaque groupe puis globalement.""",
r"""Dans le premier groupe, $X$ a 90\,\% contre 80\,\% pour $Y$ ; dans le second, 60\,\% contre 50\,\%. Pourtant globalement, $X$ a $33/50=66\,\%$ et $Y$ $37/50=74\,\%$. Les répartitions des effectifs entre groupes sont différentes. Une comparaison globale ne conserve donc pas nécessairement l’ordre observé dans chaque groupe.""",
'Calculer tous les effectifs globaux et interpréter l’effet des pondérations.','assert Rational(9,10)>Rational(32,40) and Rational(24,40)>Rational(5,10) and Rational(33,50)<Rational(37,50)')
],reperes=['Variables nominales et ordinales','Tableaux croisés et marges','Fréquences conditionnelles','Filtres et lecture de données réelles'],deco='statistique')

chapitre(14,'probabilites','Probabilités et arbres','4 · Statistiques et probabilités',
 'Modèles · Événements · Conditions · Simulation',
 ['Expliciter le modèle probabiliste choisi.','Calculer sur un tableau ou un chemin d’arbre.','Distinguer un conditionnement et son inversion.'],
 ['Fréquences, fractions et vocabulaire des ensembles.'],[
r'''\essSection{1}{Un modèle pour le hasard}
\begin{definition}L’univers $\Omega$ est l’ensemble des issues. Un événement est un sous-ensemble de $\Omega$. Une loi de probabilité sur un univers fini attribue à chaque issue un nombre positif ou nul, de somme totale 1. La probabilité d’un événement est la somme de celles de ses issues.\end{definition}
\begin{propriete}Pour tout événement $A$, $0\le P(A)\le1$ et $P(\overline A)=1-P(A)$. En équiprobabilité, $P(A)=\operatorname{Card}(A)/\operatorname{Card}(\Omega)$. Pour deux événements : $P(A\cup B)=P(A)+P(B)-P(A\cap B)$.\end{propriete}
\begin{attention}L’équiprobabilité est une hypothèse du modèle, par exemple un dé équilibré. Le fait qu’un objet ait six faces ne démontre pas à lui seul que ses six résultats ont la même probabilité.\end{attention}
\begin{savoirfaire}[Deux épreuves]Décrire les issues par des couples ordonnés. Pour deux dés équilibrés indépendants, les 36 couples sont équiprobables ; les sommes de 2 à 12 ne le sont pas.\end{savoirfaire}''',
r'''\essSection{2}{Conditionner et lire un arbre}
\begin{definition}Pour $P(A)>0$, la probabilité de $B$ sachant $A$ est
\[P_A(B)=\frac{P(A\cap B)}{P(A)}.\]
Lors d’un tirage au sort avec équiprobabilité dans une population $\Omega$, $P_A(B)=\dfrac{\operatorname{Card}(A\cap B)}{\operatorname{Card}(A)}$ : c’est la fréquence conditionnelle de $B$ parmi $A$.
\end{definition}
\begin{propriete}Les probabilités sur les branches issues d’un même nœud somment à 1. Sur un chemin $A$ puis $B$, la multiplication donne $P(A\cap B)=P(A)P_A(B)$. Ne pas confondre $P_A(B)$ et $P_B(A)$.\end{propriete}
\begin{savoirfaire}[Inverser à partir d’effectifs]Construire une population de référence, compléter ses cases, puis diviser par l’effectif du groupe conditionnant. Un arbre ou un tableau explicite rend visibles les faux positifs et faux négatifs d’un contrôle.\end{savoirfaire}
\begin{propriete}[Observation de la loi des grands nombres]Lors de nombreuses répétitions indépendantes d’une même expérience, sauf exception, la fréquence observée est proche de la probabilité du modèle. Elle peut fluctuer et ne se rapproche pas forcément à chaque nouvelle répétition.\end{propriete}
\begin{attention}Le calcul général à partir des probabilités conditionnelles d’une partition n’est pas un attendu du programme de Seconde 2026. Les prolongements de ce type sont signalés dans les défis ; le cours utilise les chemins, les tableaux et les informations données.\end{attention}'''
],[
E('Un dé équilibré',r"""On lance un dé équilibré à six faces. Décrire l’univers, puis calculer la probabilité d’obtenir un nombre pair et celle d’obtenir un nombre supérieur ou égal à 5.""",
r"""L’univers est $\{1,2,3,4,5,6\}$ et chaque issue a une probabilité $1/6$. Les pairs sont 2, 4 et 6 : $P(\text{pair})=3/6=\res{1/2}$. Les issues au moins égales à 5 sont 5 et 6 : la probabilité vaut $2/6=\res{1/3}$. L’équiprobabilité vient de l’hypothèse du dé équilibré.""",
'Décrire les issues favorables dans le modèle équiprobable.','assert len([a for a in range(1,7) if a%2==0])==3 and len([a for a in range(1,7) if a>=5])==2'),
E('L’événement contraire',r"""La probabilité qu’une pièce soit conforme est $0{,}96$. Quelle est la probabilité qu’elle ne soit pas conforme ?""",
r"""Les deux événements sont contraires, donc leurs probabilités somment à 1. La réponse est $1-0{,}96=\res{0{,}04=4\,\%}$. Cette opération ne demande pas de supposer deux expériences indépendantes : elle concerne les deux possibilités d’une même pièce.""",
'Utiliser le complémentaire dans le même univers.','assert 1-Rational(96,100)==Rational(4,100)'),
E('Une loi non uniforme',r"""Une roue donne les nombres 1, 2, 3, 4 avec probabilités $0{,}1$, $0{,}2$, $0{,}3$, $0{,}4$. Vérifier la loi et calculer $P(X\ge3)$.""",
r"""Les probabilités sont positives et leur somme vaut $0{,}1+0{,}2+0{,}3+0{,}4=1$ : la loi est valide. L’événement $X\ge3$ contient les issues 3 et 4, donc sa probabilité vaut $0{,}3+0{,}4=\res{0{,}7}$. Le rapport $2/4$ serait faux car les quatre issues ne sont pas équiprobables.""",
'Additionner les probabilités des issues plutôt que les compter sans hypothèse.','assert sum([Rational(i,10) for i in range(1,5)])==1 and Rational(3,10)+Rational(4,10)==Rational(7,10)'),
E('Une union',r"""Pour un dé équilibré, $A$ est « pair » et $B$ est « au moins 4 ». Décrire $A\cap B$ et calculer $P(A\cup B)$.""",
r"""$A=\{2,4,6\}$ et $B=\{4,5,6\}$. Leur intersection est $\{4,6\}$ et leur union $\{2,4,5,6\}$. Ainsi $P(A\cup B)=\res{4/6=2/3}$. La formule donne aussi $3/6+3/6-2/6=4/6$, en retirant les issues comptées deux fois.""",
'Lister les ensembles ou appliquer l’inclusion-exclusion.','assert set([2,4,6])&set([4,5,6])=={4,6} and len(set([2,4,6])|set([4,5,6]))==4'),
E('Conditionner dans un tableau',r"""On choisit uniformément un individu du tableau. Calculer $P_A(C)$ et $P(A\cap C)$."""+table_clubs,
r"""Le conditionnement à $A$ restreint le choix aux 60 personnes de la ligne : $P_A(C)=36/60=\res{3/5}$. Pour l’intersection sans conditionnement, la référence reste les 120 personnes : $P(A\cap C)=36/120=\res{3/10}$. Les deux numérateurs sont les mêmes, mais pas les univers de référence.""",
'Identifier si le tirage est restreint ou non à un groupe.','assert Rational(36,60)==Rational(3,5) and Rational(36,120)==Rational(3,10)'),
E('Deux conditionnements différents',r"""Une population compte 200 personnes, dont 80 dans $A$, 50 dans $B$ et 30 dans les deux. Calculer $P_A(B)$ et $P_B(A)$.""",
r"""$P_A(B)=30/80=\res{3/8}$ tandis que $P_B(A)=30/50=\res{3/5}$. L’intersection est identique, mais on choisit respectivement parmi 80 et 50 personnes. Leur différence montre que l’ordre des lettres dans un conditionnement a un sens et ne peut être permuté librement.""",
'Garder l’intersection et choisir le bon groupe conditionnant.','assert Rational(30,80)==Rational(3,8) and Rational(30,50)==Rational(3,5)'),
E('Lire un chemin d’arbre',r"""Un arbre indique $P(A)=0{,}4$, $P_A(B)=0{,}7$ et $P_{\overline A}(B)=0{,}2$. Calculer $P(A\cap B)$ et $P(A\cap\overline B)$.""",
r"""Le chemin $A$ puis $B$ a une probabilité $0{,}4\times0{,}7=\res{0{,}28}$. Au nœud $A$, la branche contraire pèse $1-0{,}7=0{,}3$, donc le chemin $A$ puis non $B$ vaut $0{,}4\times0{,}3=\res{0{,}12}$. Leur somme vaut 0,4, cohérente avec la probabilité du premier événement $A$.""",
'Multiplier les branches du même chemin.','assert Rational(4,10)*Rational(7,10)==Rational(28,100) and Rational(4,10)*Rational(3,10)==Rational(12,100)',figure='proba-arbre-01'),
E('Compléter des branches',r"""On connaît $P(A)=0{,}3$, $P_A(B)=0{,}8$ et $P_{\overline A}(B)=0{,}4$. Donner les trois branches contraires et la probabilité du chemin non $A$ puis non $B$.""",
r"""Les branches contraires sont $P(\overline A)=0{,}7$, $P_A(\overline B)=0{,}2$ et $P_{\overline A}(\overline B)=0{,}6$. Le chemin demandé vaut $0{,}7\times0{,}6=\res{0{,}42}$. Chaque complément est calculé au bon nœud ; les six branches ne doivent pas être additionnées toutes ensemble.""",
'Compléter chaque embranchement séparément.','assert (1-Rational(3,10))*(1-Rational(4,10))==Rational(42,100)',figure='proba-arbre-02'),
E('Deux tirages avec remise',r"""Une urne contient 3 boules rouges et 2 bleues. On tire deux fois, avec remise et mélange entre les tirages. Calculer la probabilité d’obtenir deux rouges puis celle d’obtenir rouge puis bleu.""",
r"""La remise conserve les proportions et le modèle suppose les tirages indépendants. Les branches du second tirage restent $3/5$ et $2/5$. Deux rouges ont pour probabilité $(3/5)^2=\res{9/25}$. Le chemin rouge puis bleu vaut $(3/5)(2/5)=\res{6/25}$. L’ordre est imposé dans la deuxième question.""",
'Représenter deux épreuves et conserver la composition après remise.','assert Rational(3,5)**2==Rational(9,25) and Rational(3,5)*Rational(2,5)==Rational(6,25)',figure='proba-remise'),
E('Deux tirages sans remise',r"""La même urne contient 3 rouges et 2 bleues. On tire deux fois sans remise. Calculer la probabilité de deux rouges et celle de rouge puis bleu.""",
r"""Après une rouge, il reste 2 rouges et 2 bleues parmi 4 boules. La probabilité de deux rouges vaut $(3/5)(2/4)=\res{3/10}$. Celle de rouge puis bleu vaut aussi $(3/5)(2/4)=\res{3/10}$. Les secondes branches dépendent du premier résultat : on ne reprend pas les proportions de l’urne initiale.""",
'Actualiser les effectifs après le premier tirage.','assert Rational(3,5)*Rational(2,4)==Rational(3,10)',figure='proba-sans-remise'),
E('Un contrôle et ses erreurs',r"""Un contrôle de fabrication produit le tableau ci-dessous. On choisit une pièce au hasard. Calculer la sensibilité (signal positif parmi les défectueuses), la spécificité (signal négatif parmi les conformes), puis la probabilité qu’une pièce à signal positif soit défectueuse."""+table_test,
r"""La sensibilité vaut $18/20=\res{90\,\%}$ ; la spécificité vaut $931/980=\res{95\,\%}$. Parmi les 67 signaux positifs, 18 correspondent à des défauts : la probabilité inversée est $\res{18/67\approx26{,}9\,\%}$. Les 49 faux positifs expliquent pourquoi cette probabilité n’est pas 90\,\%. Ces données sont construites pour l’exercice.""",
'Interpréter chaque terme du contrôle par son dénominateur.','assert Rational(18,20)==Rational(9,10) and Rational(931,980)==Rational(19,20) and round(100*18/67,1)==26.9'),
E('Deux dés et une somme',r"""On lance deux dés équilibrés indépendants. Calculer la probabilité d’une somme égale à 8 en listant les couples possibles.""",
r"""Les 36 couples ordonnés sont équiprobables. La somme 8 est obtenue avec $(2;6),(3;5),(4;4),(5;3),(6;2)$, soit cinq couples. La probabilité vaut $\res{5/36}$. Les couples $(2;6)$ et $(6;2)$ sont distincts car les deux dés occupent des positions différentes dans l’expérience.""",
'Compter les couples élémentaires, pas les valeurs de somme.','assert [(a,b) for a in range(1,7) for b in range(1,7) if a+b==8]==[(2,6),(3,5),(4,4),(5,3),(6,2)]',figure='proba-des'),
E('Un conditionnement reconstitué',r"""On sait $P(A)=0{,}6$, $P(A\cap B)=0{,}24$ et $P(B)=0{,}3$. Calculer $P_A(B)$ et $P_B(A)$. Les données sont-elles cohérentes ?""",
r"""La définition donne $P_A(B)=0{,}24/0{,}6=\res{0{,}4}$ et $P_B(A)=0{,}24/0{,}3=\res{0{,}8}$. Les quatre cases d’un tableau de probabilités sont 0,24 ; 0,36 ; 0,06 ; 0,34. Elles sont positives et somment à 1 : les données sont cohérentes. Ce contrôle évite d’accepter des probabilités incompatibles.""",
'Appliquer la définition puis vérifier les quatre intersections.','assert Rational(24,100)/Rational(6,10)==Rational(4,10) and Rational(24,100)/Rational(3,10)==Rational(8,10) and sum([Rational(24,100),Rational(36,100),Rational(6,100),Rational(34,100)])==1'),
E('Fréquence et probabilité',r"""Une pièce équilibrée donne 62 piles en 100 lancers. Cela prouve-t-il qu’elle est truquée ? La fréquence doit-elle se rapprocher de $1/2$ à chacun des lancers suivants ?""",
r"""La fréquence observée est $\res{0{,}62}$. Une fluctuation reste possible pour une pièce équilibrée : ce seul constat ne prouve pas un trucage. La loi des grands nombres décrit une proximité fréquente pour de grands effectifs, pas une convergence monotone. Un lancer supplémentaire peut rapprocher ou éloigner la fréquence de $1/2$. Une décision statistique demanderait un protocole dépassant cette simple observation.""",
'Distinguer modèle, observation et conclusion statistique.','assert Rational(62,100)==Rational(31,50) and abs(Rational(63,101)-Rational(1,2))>abs(Rational(62,100)-Rational(1,2))'),
E('Choisir le bon arbre',r"""Une usine produit 40\,\% de ses pièces sur $A$. La probabilité d’un défaut sachant $A$ vaut 2\,\%. On sait aussi que 3\,\% de toutes les pièces sont défectueuses. Calculer la probabilité « $A$ et défaut », puis la part de $A$ parmi les pièces défectueuses.""",
r"""Le chemin $A$ puis défaut vaut $0{,}4\times0{,}02=\res{0{,}008}$. Pour inverser, on utilise la probabilité globale du défaut qui est donnée : $0{,}008/0{,}03=\res{4/15\approx26{,}7\,\%}$. La donnée $P(D)=3\,\%$ est nécessaire à ce calcul ; elle n’est pas remplacée par le 2\,\% conditionnel.""",
'Multiplier un chemin puis diviser par la probabilité donnée du nouvel événement conditionnant.','assert Rational(4,10)*Rational(2,100)==Rational(8,1000) and Rational(8,1000)/Rational(3,100)==Rational(4,15)',figure='proba-usine')
],reperes=['Univers, équiprobabilité et événements','Conditionnement et inversion','Arbres et probabilités de chemin','Simulation et fluctuation'],deco='probabilites')
