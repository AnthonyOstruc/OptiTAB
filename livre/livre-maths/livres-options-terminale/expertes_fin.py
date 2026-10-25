from complementaires import project_pages

PROJECTS=[
('Une spirale et son centre','Synthèse · Complexes et suites',r'$z_0=0$, $z_{n+1}=az_n+1$ avec $a=(1+\mathrm i)/2$.',
r'Trouver le point fixe $\ell$.@@Exprimer $z_n-\ell$ et sa distance à zéro.@@Décrire l’évolution géométrique autour de $\ell$.@@Trouver un rang garantissant $|z_n-\ell|<0{,}01$.',
r'$\ell=1/(1-a)=1+\mathrm i$.@@$z_n-\ell=-\ell a^n$ ; sa norme vaut $\sqrt2(1/\sqrt2)^n=2^{(1-n)/2}$.@@À chaque étape, la distance au centre est multipliée par $1/\sqrt2$ et la direction tourne de $\pi/4$. Les points tendent vers $\ell$.@@$2^{(1-n)/2}<1/100$ donne $n>1+2\ln100/\ln2\simeq14{,}288$ ; le premier rang est $15$.'),
('Le pentagone régulier','Synthèse · Racines de l’unité',r'On pose $\omega=\mathrm e^{2\mathrm i\pi/5}$ et $c=\cos(2\pi/5)$.',
r'Justifier $1+\omega+\cdots+\omega^4=0$.@@Prendre les parties réelles et obtenir $1+2c+2\cos(4\pi/5)=0$.@@En déduire la valeur exacte de $c$.@@Calculer la longueur d’un côté du pentagone inscrit dans le cercle unité.',
r'$\omega^5=1$ et $\omega\ne1$ ; la somme géométrique vaut zéro.@@Les termes d’angles opposés ont le même cosinus ; les cinq parties réelles se regroupent comme indiqué.@@$\cos(4\pi/5)=2c^2-1$ donne $4c^2+2c-1=0$. Comme $2\pi/5<\pi/2$, $c>0$ ; donc $c=(\sqrt5-1)/4$.@@Le côté vaut $|\omega-1|=\sqrt{2-2c}=\sqrt{(5-\sqrt5)/2}$.'),
('Un message affine','Synthèse · Congruences et chiffrement',r'Les lettres sont numérotées de $0$ à $25$. On chiffre par $y\equiv7x+3\pmod{26}$.',
r'Pourquoi le déchiffrement est-il possible ?@@Trouver la formule inverse.@@Chiffrer MAT.@@Déchiffrer le résultat et discuter l’intérêt pédagogique du modèle.',
r'$\operatorname{PGCD}(7,26)=1$ : $7$ est inversible modulo $26$.@@$7\times15\equiv1$, donc $x\equiv15(y-3)\pmod{26}$.@@M vaut $12$, A vaut $0$, T vaut $19$. Les images sont $9,3,6$, soit JDG.@@$15(9-3)\equiv12$, $15(3-3)=0$, $15(6-3)\equiv19$. On retrouve MAT. Le système illustre l’inverse modulaire mais reste facile à attaquer et ne représente pas une sécurité moderne.'),
('Pourquoi un RSA miniature fonctionne','Synthèse · Fermat, Gauss et puissances',r'On prend $p=7$, $q=11$, $n=77$, $e=7$ et $d=43$. On considère des messages entiers premiers avec $77$.',
r'Verifier $ed\equiv1\pmod{60}$.@@Chiffrer le message $m=2$ par $c\equiv m^e\pmod{77}$.@@Montrer $m^{ed}\equiv m$ modulo $7$ puis modulo $11$.@@Conclure modulo $77$ et contrôler le déchiffrement avec Python.',
r'$7\times43=301=5\times60+1$.@@$2^7=128\equiv51\pmod{77}$.@@Fermat donne $m^6\equiv1\pmod7$ et $m^{10}\equiv1\pmod{11}$. Comme $ed-1=300$ est divisible par $6$ et $10$, on obtient dans les deux cas $m^{ed}\equiv m$.@@La différence est divisible par $7$ et $11$, premiers entre eux ; Gauss donne la divisibilité par $77$. \code{pow(51, 43, 77)} rend $2$. La preuve a utilisé l’hypothèse de coprimalité annoncée ; ces petits paramètres servent uniquement à l’étude.'),
('Deux calendriers','Synthèse · Équations entières',r'Un événement se produit aux jours $x\equiv4\pmod7$, un autre aux jours $x\equiv3\pmod5$.',
r'Poser $x=4+7k$ et trouver $k$ modulo $5$.@@Donner tous les jours communs.@@Lesquels appartiennent à $[1,100]$ ?@@Justifier la période et l’unicité de la classe obtenue.',
r'$4+7k\equiv3\pmod5$ donne $2k\equiv4$, donc $k\equiv2\pmod5$.@@$k=2+5t$, donc $x=18+35t$, $t\in\Z$.@@$18,53,88$.@@La différence de deux solutions est divisible par $7$ et $5$, donc par $35$. Réciproquement ajouter $35$ conserve les deux restes.'),
('Visiter toutes les liaisons','Synthèse · Graphe complet et Euler',r'Cinq lieux sont reliés deux à deux. On note les sommets $0,1,2,3,4$.',
r'Identifier le graphe, ses degrés et son nombre d’arêtes.@@Un cycle eulérien existe-t-il ?@@Vérifier le parcours $0,1,2,0,3,1,4,2,3,4,0$.@@La puissance $A^{10}$ permet-elle de compter seulement les cycles eulériens ?',
r'C’est $K_5$, d’ordre $5$ ; chaque sommet a degré $4$ et il y a $10$ arêtes.@@Oui, par le critère admis : le graphe est connexe et tous ses degrés sont pairs.@@Les dix arêtes parcourues sont $01,12,02,03,13,14,24,23,34,04$, toutes différentes ; elles épuisent les dix arêtes. Le départ et l’arrivée coïncident.@@Non : les puissances de la matrice d’adjacence comptent tous les parcours, y compris avec répétition d’arêtes. Un critère supplémentaire serait nécessaire.'),
('Une parabole par trois mesures','Synthèse · Matrices et interpolation',r'On cherche $f(x)=ax^2+bx+c$ passant par $(0,1),(1,3),(2,9)$.',
r'Écrire le système sur $(c,b,a)$.@@Donner sa matrice et expliquer l’unicité.@@Résoudre et vérifier.@@Un quatrième point non compatible pourrait-il être imposé sans changer le degré ?',
r'$c=1$, $c+b+a=3$, $c+2b+4a=9$.@@$V=\begin{pmatrix}1&0&0\\1&1&1\\1&2&4\end{pmatrix}$ ; éliminer $c$ donne $b+a=2$, $2b+4a=8$, système de solution unique. Donc $V$ est inversible.@@$a=2,b=0,c=1$, soit $f(x)=2x^2+1$ ; les trois valeurs sont bien $1,3,9$.@@Non en général. Trois points d’abscisses distinctes fixent au plus une parabole de degré au plus $2$ ; une quatrième contrainte peut la contredire.'),
('Diffusion d’Ehrenfest à deux particules','Synthèse · Chaîne à trois états',r'Deux particules sont réparties entre deux boîtes. À chaque étape, on choisit uniformément une particule et on la change de boîte. L’état est le nombre de particules dans la première boîte.',
r'Construire la matrice $R$ dans l’ordre $0,1,2$.@@Déterminer une distribution invariante.@@Partant de $0$, montrer l’absence de convergence.@@On reste maintenant immobile avec probabilité $1/2$, sinon on applique une transition de $R$. Construire $P$ et comparer au cours.',
r'$R=\begin{pmatrix}0&1&0\\1/2&0&1/2\\0&1&0\end{pmatrix}$. Depuis $1$, chaque particule a une chance sur deux d’être choisie.@@$\pi=(1/4;1/2;1/4)$ vérifie $\pi R=\pi$.@@Aux temps impairs l’état est certainement $1$ ; aux temps pairs à partir de $2$, la distribution vaut $(1/2;0;1/2)$. Deux sous-suites différentes empêchent la convergence.@@$P=(I_3+R)/2=\left(\begin{smallmatrix}1/2&1/2&0\\1/4&1/2&1/4\\0&1/2&1/2\end{smallmatrix}\right)$ : c’est le modèle du chapitre 12, qui converge pour le départ étudié. La possibilité de rester modifie ici la périodicité.'),
('Un modèle de classement de pages','Synthèse · Marche aléatoire et redémarrage',r'Dans un réseau fictif, $A$ pointe vers $B,C$ à parts égales ; $B,C$ pointent vers $A$. À chaque étape, on suit un lien avec probabilité $0{,}85$, sinon on choisit une page parmi les trois uniformément.',
r'Construire la matrice $P$.@@Justifier que les probabilités d’arrivée en $B,C$ sont égales après une étape.@@Trouver une distribution invariante et classer les pages.@@Établir une récurrence pour la probabilité $a_n$ d’être en $A$ et discuter la convergence.',
r'$P=\begin{pmatrix}0{,}05&0{,}475&0{,}475\\0{,}9&0{,}05&0{,}05\\0{,}9&0{,}05&0{,}05\end{pmatrix}$. Chaque coefficient comprend le redémarrage uniforme $0{,}15/3=0{,}05$.@@Les colonnes d’arrivée en $B,C$ sont identiques, donc les deux produits donnent la même probabilité.@@$a=0{,}05a+0{,}9(1-a)$ donne $a=18/37$ ; $b=c=(1-a)/2=19/74$. $A$ a le score le plus élevé, $B,C$ sont ex æquo.@@$a_{n+1}=0{,}9-0{,}85a_n$, donc $a_n=18/37+(a_0-18/37)(-0{,}85)^n$. Le terme d’écart tend vers zéro ; les trois probabilités convergent vers la distribution calculée. C’est un modèle pédagogique de classement par marche aléatoire, pas la description exhaustive d’un moteur de recherche.')
]

ASSESSMENTS=[
('Évaluation 1 · Nombres complexes','60 minutes · 20 points',r'On considère $P(z)=z^3-z^2+4z-4$ et les points d’affixes $a=0,b=2,c=2\mathrm i$.',
r'Factoriser $P$ à partir de la racine $1$ et résoudre $P(z)=0$. \hfill(4 points)@@Donner module, argument et forme exponentielle de $1+\mathrm i$ ; calculer sa puissance $12$. \hfill(4 points)@@Interpréter $(c-a)/(b-a)$ et décrire le triangle. \hfill(4 points)@@Déterminer et placer les racines sixièmes de l’unité. \hfill(4 points)@@Retrouver $\cos3x=4\cos^3x-3\cos x$ et calculer $\int_0^{\pi/2}\cos^3x\,\mathrm dx$. \hfill(4 points)',
r'$P=(z-1)(z^2+4)$ ; solutions $1,2\mathrm i,-2\mathrm i$. Vérification de racine et factorisation : 2 points ; solutions : 2 points.@@$|1+\mathrm i|=\sqrt2$, argument $\pi/4$ ; forme $\sqrt2\mathrm e^{\mathrm i\pi/4}$. Puissance $12$ : $64\mathrm e^{3\mathrm i\pi}=-64$. Forme : 2 points ; puissance : 2 points.@@Le quotient vaut $\mathrm i$, de module $1$ et d’argument $\pi/2$ : triangle rectangle isocèle en $A$. Calcul : 2 points ; interprétation : 2 points.@@$\mathrm e^{\mathrm ik\pi/3}$, $k=0,\ldots,5$, formant un hexagone régulier sur le cercle unité. Expressions : 2 points ; placement et distinction : 2 points.@@Moivre au cube puis identification réelle donne la formule ; $\cos^3x=(\cos3x+3\cos x)/4$. L’intégrale vaut $[\sin3x/12+3\sin x/4]_0^{\pi/2}=-1/12+3/4=2/3$. Démonstration : 2 points ; intégrale : 2 points.'),
('Évaluation 2 · Arithmétique','60 minutes · 20 points',r'Tous les inconnus sont entiers, sauf indication contraire.',
r'Calculer le PGCD de $252,198$ et donner un couple de Bézout. \hfill(4 points)@@Résoudre $7x\equiv5\pmod{26}$. \hfill(4 points)@@Résoudre $15x+21y=6$ dans $\Z^2$. \hfill(4 points)@@Étudier la primalité de $223$, puis calculer $2^{100}$ modulo $13$. \hfill(4 points)@@Prouver l’infinitude des nombres premiers sans supposer que le produit d’une liste de premiers augmenté de $1$ est premier. \hfill(4 points)',
r'Euclide donne les restes $54,36,18,0$ ; PGCD $18$. En remontant : $18=4\times252-5\times198$. Algorithme : 2 points ; identité : 2 points.@@Inverse de $7$ : $15$ ; donc $x\equiv15\times5\equiv23\pmod{26}$. Inverse justifié : 2 points ; classe et vérification : 2 points.@@Réduire à $5x+7y=2$ ; une solution est $(-1,1)$ ; toutes sont $x=-1+7k$, $y=1-5k$, $k\in\Z$. Réduction et solution particulière : 2 points ; famille complète : 2 points.@@Tester les premiers $2,3,5,7,11,13$ suffit pour $223$ ; aucun ne divise. Fermat donne $2^{12}\equiv1\pmod{13}$ ; donc $2^{100}\equiv2^4\equiv3$. Deux points par partie.@@Supposer la liste finie $p_1,\ldots,p_r$ exhaustive. $N=p_1\cdots p_r+1>1$ possède un diviseur premier ; aucun $p_i$ ne peut le diviser. Contradiction. Hypothèse et construction : 2 points ; diviseur premier et contradiction : 2 points.'),
('Évaluation 3 · Matrices et graphes','75 minutes · 20 points',r'$A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$. Une chaîne indépendante de cette première matrice a pour transition $P=\begin{pmatrix}0{,}8&0{,}2\\0{,}3&0{,}7\end{pmatrix}$.',
r'Donner et prouver $A^n$ par récurrence. \hfill(4 points)@@Résoudre $AX=\binom53$ puis calculer $A^{10}\binom01$. \hfill(4 points)@@Construire le graphe de transition de $P$ et calculer $P^2$. \hfill(4 points)@@Depuis $\pi_0=(1;0)$, déterminer la distribution après $n$ transitions et sa limite. \hfill(4 points)@@Expliquer la différence entre le coefficient d’une puissance de matrice d’adjacence et celui d’une puissance de matrice de transition. \hfill(4 points)',
r'$A^n=\left(\begin{smallmatrix}1&n\\0&1\end{smallmatrix}\right)$ ; vérifier $n=0$ et multiplier par $A$ pour l’hérédité. Formule : 1 point ; initialisation et hérédité : 3 points.@@$x+y=5,y=3$, donc $X=\binom23$ ; $A^{10}\binom01=\binom{10}1$. Deux points par calcul.@@Le graphe porte quatre arcs, boucles comprises, de poids $0{,}8,0{,}2,0{,}3,0{,}7$. $P^2=\left(\begin{smallmatrix}0{,}7&0{,}3\\0{,}45&0{,}55\end{smallmatrix}\right)$. Graphe : 2 points ; produit : 2 points.@@$\pi_n=(0{,}6+0{,}4(0{,}5)^n;0{,}4-0{,}4(0{,}5)^n)$ ; limite $(0{,}6;0{,}4)$. Récurrence et formule : 3 points ; limite : 1 point.@@L’adjacence compte des parcours de longueur fixée, répétitions comprises ; la transition somme des produits de probabilités et donne une probabilité conditionnelle après plusieurs étapes. Deux points par interprétation, avec départ et arrivée identifiés.')
]

DOSSIERS=r'\clearpage\begingroup\renewcommand{\otThumb}{}\renewcommand{\otHeadTag}{D}\phantomsection\label{dossiers}\pdfbookmark[0]{Dossiers et évaluations}{dossiers}'+project_pages(PROJECTS,'projet')+project_pages(ASSESSMENTS,'evaluation')+r'\clearpage\endgroup'
SOLUTIONS_DOSSIERS=project_pages(PROJECTS,'projet',True)+project_pages(ASSESSMENTS,'evaluation',True,True)

COVERAGE=[
('C01','Ensemble complexe, parties réelle et imaginaire, opérations et équation $az=b$',1,'1, 2, 5'),
('C02','Conjugaison, inverse, équations simples avec $z$ et son conjugué',1,'3, 4, 6, 7, 9, 11'),
('C03','Conjugué du produit, de l’inverse et des puissances ; formule du binôme et sa preuve',1,'8, 10, 12'),
('C04','Affixes de points/vecteurs, image du conjugué et représentation',2,'1, 5'),
('C05',r'Module, distance, $|z|^2=z\bar z$, produit, inverse et puissance',2,'2, 6, 9'),
('C06','Cercle unité et stabilité ; arguments et forme trigonométrique',2,'3, 4, 6, 8'),
('C07','Addition et duplication trigonométriques ; démonstration par produit scalaire',3,'4, 5, 11'),
('C08','Exponentielle imaginaire, relation fonctionnelle, changement des trois formes',3,'1, 2, 3, 8'),
('C09','Euler et Moivre : transformations, intégrales, suites et puissances',3,'6, 7, 9, 10, 12'),
('C10','Second degré réel dans $\C$, racine connue d’un troisième degré',4,'1, 2, 4, 5, 6'),
('C11','Factorisations $z^n-a^n$ et $P(z)$ par $z-a$ ; borne du nombre de racines et preuves',4,'3, 7, 8, 9, 10, 12'),
('C12','Module et argument d’un quotient de vecteurs, alignement, orthogonalité et lieux',5,'1, 2, 5, 6, 8'),
('C13','Racines de l’unité, preuve, cas $2,3,4$, polygones réguliers',5,'3, 4, 7, 12'),
('A01','Divisibilité dans $\Z$, combinaisons et diviseurs',6,'1, 5, 10, 12'),
('A02','Division euclidienne d’un relatif par un entier strictement positif',6,'2, 3'),
('A03','Congruences et compatibilité avec opérations ; tests de divisibilité',6,'4, 6, 7, 8, 9, 11'),
('A04','PGCD, Euclide, couples premiers entre eux et Bézout constructif',7,'1, 2, 4, 5'),
('A05','Gauss : démonstration et applications',7,'6, 12'),
('A06','Inverse modulaire et résolution de $ax\equiv b$ modulo $n$',7,'3, 7, 10'),
('A07','Équations diophantiennes et contraintes sur les solutions',7,'4, 8, 9, 11'),
('A08','Nombres premiers, infinitude, décomposition unique et étude de primalité',8,'1, 2, 5, 10'),
('A09','Petit théorème de Fermat ; limites d’un test de primalité',8,'3, 8, 9'),
('A10','Crible, décomposition algorithmique et chiffrement',8,'4, 6, 7, 11'),
('M01','Matrices carrées, lignes/colonnes, opérations et dimensions',9,'1, 2, 3, 5'),
('M02','Inverse en ordres $2$ et $3$, résolution de systèmes',9,'4, 6, 7, 9, 11'),
('M03','Transformations géométriques représentées par matrices',9,'8, 10, 12'),
('M04','Puissances en ordres $2$ et $3$, récurrences et preuve de formules',10,'1, 2, 5, 6, 7, 9, 12'),
('M05','Colonnes récurrentes $U_{n+1}=AU_n+C$ et problèmes d’évolution',10,'3, 4, 8, 10, 11'),
('G01','Graphes, sommets, arêtes, adjacence, ordre, degrés et graphe complet',11,'1, 2, 3, 7'),
('G02','Chaînes, longueurs, connexité et modèle par graphe',11,'4, 8, 10'),
('G03','Adjacence, parcours de longueur fixée, comptage par puissances et preuve',11,'5, 6, 9, 11, 12'),
('P01','Markov à deux/trois états : graphe pondéré, transition et distribution initiale',12,'1, 2, 4, 8'),
('P02','Interprétation de $P^n$ et distribution ligne $\pi_0P^n$ ; preuves',12,'2, 5, 8, 11, 12'),
('P03','Distributions invariantes à deux/trois états et étude de probabilités',12,'3, 6, 7, 9, 10')
]

CONCORDANCE=r'''\fiche{Concordance du programme}{Des attendus aux chapitres et aux exercices}
\phantomsection\label{concordance}\pdfbookmark[0]{Programme et sources}{programme}
Référence : programme de l'enseignement optionnel de mathématiques expertes de Terminale générale, BO spécial n° 8 du 25 juillet 2019, arrêté du 19 juillet 2019, NOR MENE1921264A.
La page Éduscol consultée le 23 octobre 2026 conserve ce programme pour l'option. Les nouveaux programmes publiés en avril 2026 pour d'autres enseignements ne doivent pas lui être substitués.
Les regroupements ci-dessous sont éditoriaux ; les exemples de problèmes possibles du programme permettent un choix pédagogique et ne sont pas tous des obligations.
\par\vspace{3mm}
'''
for code,desc,ch,ex in COVERAGE:
    CONCORDANCE+=rf'\noindent\textbf{{{code}}} · {desc}. \hyperref[chap-{ch}]{{Chapitre {ch}}}, exercices {ex}.\par\vspace{{1.7mm}}'+'\n'
CONCORDANCE+=r'''\fiche{Démontrer et approfondir}{Une progression vers des problèmes plus ouverts}
\souscours{Démonstrations mentionnées par le programme}
Conjugués de produits, inverses, puissances et binôme : chapitre 1.
Identité du module, produit et puissance : chapitre 2.
Formule d'addition : chapitre 3.
Factorisation des différences de puissances, factorisation par une racine et majoration du nombre de racines : chapitre 4.
Détermination des racines de l'unité : chapitre 5.
Écriture du PGCD comme combinaison de Bézout et Gauss : chapitre 7.
Infinitude des premiers : chapitre 8.
Comptage des parcours par les puissances d'adjacence : chapitre 11.
Probabilités de transition à plusieurs étapes et distributions lignes : chapitre 12.
\souscours{Algorithmes et outils}
Euclide et Bézout : chapitre 7, avec fonction Python.
Crible et décomposition en premiers : chapitre 8, avec fonctions Python.
Puissances, systèmes et contrôles de produits : chapitres 9 et 10.
Calcul des distributions : chapitre 12.
La fonction native \code{pow(a, n, m)} donne une exponentiation modulaire efficace ; une calculatrice ou un logiciel de calcul matriciel peut soutenir l'expérimentation, puis la preuve justifie les formules.
\souscours{Repères historiques}
Le programme propose de relier les complexes aux équations algébriques de la Renaissance, puis à leur représentation géométrique. Les chapitres 1 à 5 suivent ce passage du calcul au plan.
L'arithmétique relie division d'Euclide, identités de Bézout et applications au chiffrement.
Les graphes, matrices et chaînes de Markov éclairent l'unité entre problèmes de réseaux, calcul et probabilités. Les dossiers fournissent des contextes de recherche et de communication orale.
\souscours{Prolongements guidés}
Les carrées de complexes, suites complexes, inégalité triangulaire, interpolation, Euler, RSA, diffusion et classement par marche aléatoire sont présentés comme des problèmes guidés. Aucune théorie générale de diagonalisation, de cryptographie ou de convergence des chaînes n'est supposée.
'''
for i,p in enumerate(PROJECTS,1):CONCORDANCE+=rf'\repere{{projet-{i}}}{{{p[0]}}}'+'\n'
CONCORDANCE+=r'''\fiche{Sources et démarche éditoriale}{Recherche vérifiée le 23 octobre 2026}
\begin{itemize}
\item Ministère, \href{https://www.education.gouv.fr/bo/19/Special8/MENE1921264A.htm}{arrêté du 19 juillet 2019, BO spécial n° 8 du 25 juillet 2019}, programme de mathématiques expertes.
\item Éduscol, \href{https://eduscol.education.gouv.fr/sites/default/files/document/spe264annexe1158825pdf-84165.pdf}{annexe officielle en vigueur, 11 pages}.
\item Éduscol, \href{https://eduscol.education.gouv.fr/5817/programmes-et-ressources-en-mathematiques-voie-gt}{programmes et ressources en mathématiques, voie générale et technologique}, mise à jour juillet 2026.
\item Mission Villani-Torossian, \href{https://eduscol.education.gouv.fr/sites/default/files/document/grilles-de-positionnement-des-livres-de-mathematiques-70116.pdf}{grilles de positionnement des livres de mathématiques}, mai 2019.
\end{itemize}
Les anciens cours OptiTAB sur les complexes, l'arithmétique et les matrices ont servi de repères internes ; le texte de cette édition est restructuré pour l'option et complété selon l'annexe officielle.
Les exercices, dossiers et évaluations sont des créations originales avec leurs solutions. Ils ne sont pas présentés comme des sujets officiels de baccalauréat.
Les données et réseaux sont fictifs. Les schémas sont construits à partir des coordonnées, des arêtes et des matrices du texte ; les algorithmes et les calculs clés ont fait l'objet de contrôles indépendants.
'''
INDEX=r'\fiche{Index des méthodes}{Choisir une représentation et un raisonnement}\phantomsection\label{index-methodes}\pdfbookmark[0]{Index}{index}'
for ch,title in [(1,'Conjugaison, quotient, équation et binôme'),(2,'Module, argument, affixe et lieu'),(3,'Exponentielle imaginaire, Euler et Moivre'),(4,'Discriminant, racine connue et factorisation'),(5,'Quotient géométrique, racines de l’unité et polygone'),(6,'Division, congruence, cycle et test de divisibilité'),(7,'Euclide, Bézout, Gauss et équation entière'),(8,'Primalité, décomposition, Fermat et chiffrement'),(9,'Produit, inverse, système et transformation'),(10,'Puissance, point fixe et colonne récurrente'),(11,'Adjacence, degré, connexité et parcours'),(12,'Distribution ligne, transition, invariant et limite')]:INDEX+=rf'\repere{{ess-{ch}}}{{{title}}}'+'\n'
