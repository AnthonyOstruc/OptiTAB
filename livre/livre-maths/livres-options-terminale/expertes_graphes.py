from commun import e,c
CHAPTERS=[]
CHAPTERS.append(c('Graphes et matrices d’adjacence','Graphes et matrices',r'Degrés · Connexité · Chaînes · Puissances',
'Modéliser une situation par un graphe.@@Calculer ordres, degrés et nombres d’arêtes.@@Passer du graphe à sa matrice d’adjacence.@@Compter des parcours de longueur fixée par une puissance.',
'Calcul matriciel et dénombrement élémentaire.',r'''
\essSection{1}{Des sommets reliés}
Un graphe possède des sommets et des arêtes. Deux sommets reliés par une arête sont adjacents.
Dans ce chapitre, les premiers graphes sont simples et non orientés : pas de boucle, ni d'arêtes multiples.
L'ordre est le nombre de sommets ; le degré d'un sommet est le nombre d'arêtes qui lui sont incidentes.
La somme des degrés vaut deux fois le nombre d'arêtes, car chaque arête possède deux extrémités.
Le graphe complet $K_n$ relie toutes les paires de sommets : chacun a degré $n-1$ et il y a $n(n-1)/2$ arêtes.
\figurelivre{e11-graphe.pdf}{Graphe d'ordre $4$, avec les arêtes $AB,AC,BC,CD$. Les degrés sont $2,2,3,1$ ; leur somme $8$ compte deux fois les quatre arêtes.}
\essSection{2}{Chaînes et connexité}
Une chaîne est une succession de sommets dont deux consécutifs sont adjacents. Sa longueur est le nombre d'arêtes parcourues.
Un graphe est connexe si toute paire de sommets peut être reliée par une chaîne.
Dans un graphe orienté, les arêtes deviennent des arcs et un chemin doit respecter leur sens. Un poids peut décrire une distance, un coût ou une probabilité, à préciser selon la situation.
Pour les comptages matriciels, on autorise la répétition des sommets et des arêtes : on compte des parcours, et non uniquement des chemins simples sans répétition.
\essSection{3}{La matrice d'adjacence}
On fixe un ordre des sommets. La matrice $A$ possède un coefficient $a_{ij}=1$ si l'on peut aller directement du sommet $i$ au sommet $j$, et $0$ sinon.
Pour un graphe simple non orienté, elle est symétrique, sa diagonale est nulle et la somme d'une ligne est le degré du sommet.
\begin{exemple}
Pour le graphe de la figure, dans l'ordre $A,B,C,D$,
$A=\begin{pmatrix}0&1&1&0\\1&0&1&0\\1&1&0&1\\0&0&1&0\end{pmatrix}$.
Une permutation de l'ordre des sommets change la présentation de la matrice ; il faut conserver les étiquettes pour interpréter les coefficients.
\end{exemple}
\essSection{4}{Compter avec les puissances}
\begin{theoreme}
Le coefficient $(i,j)$ de $A^n$ compte les parcours de longueur $n$ du sommet $i$ au sommet $j$.
Pour $n=0$, $A^0=I$ correspond au parcours vide, possible seulement si le départ et l'arrivée coïncident.
\end{theoreme}
\begin{demonstration}
Le résultat est la définition pour $n=1$. Supposer le comptage connu à la longueur $n$.
Tout parcours de longueur $n+1$ se décompose en un parcours de longueur $n$ allant de $i$ à un sommet intermédiaire $k$, puis un arc ou une arête de $k$ à $j$.
Pour chaque $k$, le nombre vaut $(A^n)_{ik}a_{kj}$ ; les cas sont disjoints. La somme sur $k$ est précisément $(A^{n+1})_{ij}$.
\end{demonstration}
\figurelivre{e11-parcours.pdf}{Le parcours de longueur $2$ de $A$ à $D$ passe par $C$. Il est compté par $(A^2)_{AD}=1$. Les parcours fermés de longueur $2$ de $A$ à lui-même sont $A,B,A$ et $A,C,A$.}
\essSection{5}{Un prolongement : parcourir chaque arête}
Une chaîne eulérienne utilise chaque arête exactement une fois. Un cycle eulérien revient au départ.
Dans un graphe connexe non orienté avec au moins une arête, il existe une chaîne eulérienne si et seulement si le nombre de sommets de degré impair est $0$ ou $2$ (critère admis ici). Si ce nombre est $0$, un cycle existe.
La nécessité s'explique : dans les sommets intermédiaires, chaque entrée s'associe à une sortie. Seuls le départ et l'arrivée peuvent avoir un degré impair.
Dans le graphe du cours, $D,C,A,B,C$ utilise chaque arête une fois, de $D$ à $C$.
''',[
e('Vocabulaire',1,r'Un graphe possède cinq sommets et sept arêtes.',r'Quel est son ordre ?@@Quelle est la somme de ses degrés ?@@Peut-on déjà dire qu’il est complet ?',r'Ordre $5$.@@$14$ dans un graphe non orienté sans boucle.@@Non ; $K_5$ aurait $5\times4/2=10$ arêtes, donc celui-ci n’est pas complet.'),
e('Graphe du cours',1,'',r'Donner les voisins de $C$.@@Donner le degré de $D$.@@Le graphe est-il connexe ?',r'$A,B,D$.@@$1$, car seule l’arête $CD$ lui est incidente.@@Oui : les sommets du triangle sont reliés entre eux et $D$ rejoint $C$.'),
e('Matrice d’un triangle',1,'',r'Écrire la matrice d’adjacence de $K_3$.@@Donner la somme de chaque ligne.@@Donner le nombre total d’arêtes.',r'$\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix}$.@@$2$, le degré de chaque sommet.@@$3\times2/2=3$.'),
e('Une longueur',1,r'On parcourt $A,C,B,A,C,D$ dans le graphe du cours.',r'Quelle est la longueur ?@@Le sommet $A$ est-il répété ?@@Ce parcours est-il eulérien ?',r'$5$, car il y a cinq déplacements entre six sommets listés.@@Oui. La répétition des sommets est autorisée pour une chaîne.@@Non : l’arête $AC$ est utilisée plusieurs fois et toutes les arêtes ne sont pas parcourues exactement une fois.'),
e('Calculer $A^2$',2,r'$A$ est la matrice du graphe du cours.',r'Calculer $(A^2)_{AD}$.@@Calculer $(A^2)_{AA}$.@@Interpréter ces deux résultats.',r'$1$, par $A,C,D$.@@$2$, via $B$ ou $C$.@@Un parcours de longueur $2$ relie $A$ à $D$ ; deux reviennent en $A$. Les retours immédiats sont comptés.'),
e('Un graphe orienté',2,r'Dans l’ordre $A,B,C$, $M=\begin{pmatrix}0&1&0\\0&0&1\\1&0&0\end{pmatrix}$.',r'Décrire les arcs.@@Calculer $M^3$.@@Donner le nombre de chemins de longueur $4$ de $A$ à $B$.',r'$A\to B$, $B\to C$, $C\to A$.@@$I_3$, car trois transitions reviennent au point de départ.@@$1$, puisque $M^4=M$.'),
e('Complet',2,'',r'Calculer le nombre d’arêtes de $K_6$.@@Donner les degrés.@@Peut-on avoir un cycle eulérien dans $K_6$ ?',r'$6\times5/2=15$.@@Chaque sommet a degré $5$.@@Non : les six degrés sont impairs ; le critère n’est pas satisfait.'),
e('Une chaîne eulérienne',2,r'On utilise le graphe du cours.',r'Repérer les sommets impairs.@@Donner une chaîne eulérienne.@@Peut-elle être fermée ?',r'$C$ de degré $3$ et $D$ de degré $1$.@@$D,C,A,B,C$.@@Non : ses extrémités sont les deux sommets impairs, distincts.'),
e('Interpréter une puissance',3,r'Pour un graphe orienté, $(A^5)_{23}=17$.',r'Que signifie ce nombre ?@@Garantit-il $17$ parcours sans répétition ?@@Que compterait $(A^0)_{23}$ ?',r'Il existe $17$ parcours orientés de longueur $5$ allant du sommet $2$ au sommet $3$.@@Non : les produits matriciels comptent aussi les parcours répétés.@@$0$, car les sommets $2$ et $3$ sont différents et aucun parcours vide ne les relie.'),
e('Connexité et information',3,r'Une matrice non orientée est composée de deux blocs diagonaux, sans coefficient non nul entre les blocs. Chaque bloc contient au moins un sommet.',r'Que révèle l’absence de coefficients croisés ?@@Le graphe est-il connexe ?@@Les puissances peuvent-elles créer un parcours entre les blocs ?',r'Aucune arête ne relie un sommet du premier groupe à un sommet du second.@@Non : ces deux groupes sont séparés.@@Non : tous les produits conservent les blocs ; aucun parcours ne peut franchir une absence totale de liaison.'),
e('Démontrer le comptage',3,'',r'Expliquer le rôle du dernier sommet intermédiaire $k$.@@Pourquoi multiplie-t-on $(A^n)_{ik}$ par $a_{kj}$ ?@@Pourquoi additionne-t-on sur $k$ ?',r'Il sépare un parcours en ses $n$ premières étapes et sa dernière étape.@@Pour chaque parcours arrivant en $k$, la présence d’une dernière arête vers $j$ détermine s’il se prolonge ; dans un graphe simple, le facteur vaut $0$ ou $1$.@@Les parcours classés par leur avant-dernier sommet sont disjoints et couvrent tous les cas. Cette somme est la formule du produit matriciel.'),
e('Poids et comptage',3,r'Une matrice contient des distances sur ses arcs plutôt que des $0$ et des $1$.',r'Les coefficients de ses puissances comptent-ils encore les parcours ?@@Que calcule le produit ordinaire dans ce cas ?@@Quelle précaution prendre avant de choisir une matrice ?',r'Non : l’interprétation de comptage exige la matrice d’adjacence appropriée.@@Il somme des produits de poids le long des parcours, pas des sommes de distances ni un nombre de parcours.@@Préciser ce que chaque coefficient représente et quelle opération correspond au problème. Un même graphe peut nécessiter plusieurs matrices selon la question.')
], 'denombrement'))

CHAPTERS.append(c('Chaînes de Markov à deux ou trois états','Graphes et matrices',r'Transitions · Distributions lignes · Invariance · Limites',
'Construire le graphe et la matrice de transition.@@Calculer une distribution après $n$ étapes.@@Déterminer une distribution invariante.@@Étudier une évolution asymptotique sur des exemples.',
'Probabilités conditionnelles, indépendance conditionnelle et puissances de matrices.',r'''
\essSection{1}{Décrire les transitions}
Une chaîne de Markov modélise un système dont la loi de l'état suivant dépend de l'état actuel et non de toute l'histoire antérieure. Dans les exemples homogènes, les probabilités de transition restent les mêmes à chaque étape.
La matrice $P$ porte en ligne l'état de départ, en colonne l'état d'arrivée ; $p_{ij}$ est la probabilité de passer de $i$ à $j$ en une transition.
Les coefficients sont positifs ou nuls et chaque ligne totalise $1$.
\begin{definition}[Convention du programme]
Une distribution est une \textbf{matrice ligne} $\pi_n$ dont les coefficients sont les probabilités des états à l'instant $n$.
On a $\pi_{n+1}=\pi_nP$ et $\pi_n=\pi_0P^n$.
\end{definition}
\figurelivre{e12-markov2.pdf}{Deux états $A,B$ : $P=\left(\begin{smallmatrix}0{,}8&0{,}2\\0{,}3&0{,}7\end{smallmatrix}\right)$. Les poids sortant de chacun des sommets totalisent $1$, boucles comprises.}
\essSection{2}{Pourquoi les puissances donnent les probabilités}
\begin{demonstration}
Pour passer de $i$ à $j$ en $n+1$ étapes, on partitionne selon l'état $k$ après $n$ étapes.
La propriété de Markov donne une probabilité $(P^n)_{ik}p_{kj}$ pour ce passage via $k$ ; sommer donne $(P^{n+1})_{ij}$.
Ainsi $(P^n)_{ij}$ est la probabilité d'être en $j$ après $n$ transitions, sachant le départ en $i$.
Si le départ est distribué selon $\pi_0$, les probabilités totales donnent pour chaque $j$ la somme $\sum_i(\pi_0)_i(P^n)_{ij}$ : c'est $\pi_0P^n$.
\end{demonstration}
Un coefficient de $P^n$ est une probabilité de transition conditionnelle ; il ne doit pas être confondu avec un coefficient d'une matrice d'adjacence comptant des parcours.
\essSection{3}{Deux états : une récurrence réelle}
Pour la matrice de la figure, si $a_n=P(X_n=A)$, alors $a_{n+1}=0{,}8a_n+0{,}3(1-a_n)=0{,}5a_n+0{,}3$.
L'équilibre vaut $0{,}6$ ; donc $a_n=0{,}6+(a_0-0{,}6)(0{,}5)^n$.
La distribution tend vers $(0{,}6;0{,}4)$, quelle que soit la distribution initiale.
\begin{definition}[Distribution invariante]
Une distribution ligne $\pi$ est invariante si $\pi P=\pi$.
On résout les équations avec la contrainte que les coefficients sont positifs ou nuls et totalisent $1$.
\end{definition}
Une distribution invariante demeure identique à chaque étape si elle est choisie comme distribution initiale. Son existence ne prouve pas que toutes les distributions convergent vers elle.
\essSection{4}{Un exemple à trois états}
\[P=\begin{pmatrix}1/2&1/2&0\\1/4&1/2&1/4\\0&1/2&1/2\end{pmatrix}.
\]
\figurelivre{e12-markov3.pdf}{Trois états, avec les transitions données par la matrice. Les arcs absents correspondent à des probabilités nulles ; les boucles restent indispensables à la somme $1$ de chaque ligne.}
Résoudre $\pi P=\pi$ avec $a+b+c=1$ donne $a=b/2$, $c=b/2$, donc $\pi=(1/4;1/2;1/4)$.
Si $\pi_0=(1;0;0)$, dès $n=1$ on a $b_n=1/2$ ; de plus $a_{n+1}-c_{n+1}=(a_n-c_n)/2$.
Pour $n\geq1$,
$\pi_n=(1/4+2^{-(n+1)};1/2;1/4-2^{-(n+1)})$, qui tend vers $\pi$.
\figurelivre{e12-convergence.pdf}{Depuis l'état $A$, les probabilités à trois états se rapprochent de $(1/4,1/2,1/4)$. La formule simplifiée vaut pour $n\geq1$ ; la distribution initiale est traitée séparément.}
\essSection{5}{Calculer avec une liste Python}
\begin{python}
def distribution(pi, P, n):
    pi = list(pi)
    for k in range(n):
        pi = [sum(pi[i]*P[i][j] for i in range(len(pi)))
              for j in range(len(pi))]
    return pi
\end{python}
On vérifie avant utilisation que $P$ est carrée, que les dimensions correspondent et que les sommes de lignes valent $1$.
Pour $P=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)$, la distribution $(1/2;1/2)$ est invariante, mais un départ certain en $A$ alterne entre les deux états sans converger.
''',[
e('Lire une transition',1,r'$P=\begin{pmatrix}0{,}8&0{,}2\\0{,}3&0{,}7\end{pmatrix}$.',r'Donner la probabilité de $A$ vers $B$.@@Donner celle de rester en $B$.@@Vérifier les sommes de lignes.',r'$0{,}2$, coefficient de la ligne $A$, colonne $B$.@@$0{,}7$.@@$0{,}8+0{,}2=1$ et $0{,}3+0{,}7=1$.'),
e('Une première distribution',1,r'$\pi_0=(1;0)$ et $P$ est la matrice à deux états du cours.',r'Calculer $\pi_1$.@@Calculer $\pi_2$.@@Vérifier les probabilités.',r'$\pi_1=(0{,}8;0{,}2)$.@@$\pi_2=(0{,}8^2+0{,}2\times0{,}3;0{,}8\times0{,}2+0{,}2\times0{,}7)=(0{,}7;0{,}3)$.@@Les coefficients sont positifs et totalisent $1$.'),
e('Invariant',1,r'$P$ est la matrice à deux états du cours.',r'Verifier $(0{,}6;0{,}4)P=(0{,}6;0{,}4)$.@@Que devient cette distribution après dix étapes ?@@Que signifie cette stabilité ?',r'Le premier coefficient vaut $0{,}48+0{,}12=0{,}6$, le second $0{,}12+0{,}28=0{,}4$.@@Elle reste $(0{,}6;0{,}4)$.@@Les proportions probabilistes se conservent, même si un individu peut changer d’état.'),
e('Une matrice admissible ?',1,r'$Q=\begin{pmatrix}0{,}5&0{,}6\\0{,}2&0{,}8\end{pmatrix}$.',r'Peut-elle être une matrice de transition selon la convention du livre ?@@Quelle ligne pose problème ?@@Corriger son second coefficient en gardant le premier.',r'Non : une somme de ligne n’est pas égale à $1$.@@La première somme vaut $1{,}1$.@@Remplacer $0{,}6$ par $0{,}5$ ; la première ligne devient $(0{,}5;0{,}5)$.'),
e('Récurrence à deux états',2,r'Pour $P$ du cours, $a_0=1$.',r'Établir $a_{n+1}=0{,}5a_n+0{,}3$.@@Exprimer $a_n$.@@Donner la limite de la distribution.',r'Probabilités totales : $0{,}8a_n+0{,}3(1-a_n)$.@@$a_n=0{,}6+0{,}4(0{,}5)^n$.@@$(0{,}6;0{,}4)$ car le terme géométrique tend vers zéro.'),
e('Une précision',2,r'On veut $|a_n-0{,}6|\leq0{,}001$ avec $a_0=1$.',r'Traduire en une inégalité géométrique.@@Trouver le premier rang.@@Vérifier les deux rangs voisins.',r'$0{,}4(0{,}5)^n\leq0{,}001$.@@$2^n\geq400$, donc $n=9$.@@Pour $n=8$, l’écart vaut $0{,}0015625$ ; pour $n=9$, $0{,}00078125$.'),
e('Trois états : invariant',2,r'$P$ est la matrice à trois états du cours.',r'Écrire les équations pour $(a;b;c)P=(a;b;c)$.@@Ajouter la normalisation et résoudre.@@Contrôler le résultat par multiplication.',r'$a=a/2+b/4$, $b=a/2+b/2+c/2$, $c=b/4+c/2$.@@$a=b/2,c=b/2$ et $a+b+c=1$ donnent $(a;b;c)=(1/4;1/2;1/4)$.@@Le produit redonne $(1/4;1/2;1/4)$ ; les coefficients sont tous positifs.'),
e('Trois états : deux étapes',2,r'$\pi_0=(1;0;0)$ et $P$ est la matrice à trois états du cours.',r'Calculer $\pi_1$.@@Calculer $\pi_2$.@@Donner la probabilité d’être en $C$ après deux transitions.',r'$\pi_1=(1/2;1/2;0)$.@@$\pi_2=(3/8;1/2;1/8)$.@@$1/8$, coefficient d’arrivée en $C$.'),
e('Périodicité et invariant',3,r'$P=\begin{pmatrix}0&1\\1&0\end{pmatrix}$ et $\pi_0=(1;0)$.',r'Donner les distributions paires et impaires.@@Trouver une distribution invariante.@@Pourquoi l’invariance n’implique-t-elle pas la convergence depuis tout départ ?',r'$\pi_{2k}=(1;0)$, $\pi_{2k+1}=(0;1)$.@@$(1/2;1/2)$.@@Le départ choisi alterne entre deux distributions différentes ; il ne converge pas, malgré l’existence d’un invariant.'),
e('Prouver la formule à trois états',3,r'$\pi_0=(1;0;0)$ pour la matrice à trois états du cours.',r'Montrer que $b_{n+1}=1/2$ pour toute distribution.@@Établir $d_{n+1}=d_n/2$ pour $d_n=a_n-c_n$.@@Retrouver $\pi_n$ pour $n\geq1$.',r'$b_{n+1}=(a_n+b_n+c_n)/2=1/2$.@@$a_{n+1}=a_n/2+b_n/4$ et $c_{n+1}=b_n/4+c_n/2$ ; soustraire donne la formule. Comme $d_0=1$, $d_n=2^{-n}$.@@Pour $n\geq1$, $a_n+c_n=1/2$ ; combiner somme et différence donne $a_n=1/4+2^{-(n+1)}$, $c_n=1/4-2^{-(n+1)}$.'),
e('Sommes de lignes des puissances',3,r'$P$ est une matrice de transition.',r'Pourquoi ses coefficients sont-ils positifs ou nuls ?@@Montrer que la somme d’une ligne de $P^2$ vaut $1$.@@Étendre aux puissances par récurrence.',r'Ils représentent des probabilités. Les produits et sommes qui construisent les puissances restent positifs ou nuls.@@$\sum_j(P^2)_{ij}=\sum_kp_{ik}\sum_jp_{kj}=\sum_kp_{ik}=1$.@@Le même calcul remplace la première matrice par $P^n$ ; si ses lignes totalisent $1$, celles de $P^{n+1}$ aussi.'),
e('Colonnes ou lignes ?',3,r'Un élève utilise $\pi_{n+1}=P\pi_n$ tout en écrivant $\pi_n$ comme ligne.',r'Identifier le problème de dimensions.@@Écrire la relation correcte avec une ligne.@@Si l’on choisit plutôt une colonne $V_n$, quelle matrice doit-on utiliser ?',r'Une matrice $m\times m$ ne peut se multiplier à droite par une ligne $1\times m$ dans cet ordre pour $m>1$.@@$\pi_{n+1}=\pi_nP$.@@$V_{n+1}=P^{\mathsf T}V_n$, avec la transposée. La convention doit être changée de façon cohérente ; le livre suit les lignes du programme.')
], 'conditionnelles'))
