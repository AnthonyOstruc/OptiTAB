PREUVES=[
('Une identité et une parité',r'''
\begin{demonstration}[Différence de deux carrés]
Par double distributivité, $(a-b)(a+b)=a^2+ab-ab-b^2=a^2-b^2$.
Les deux termes opposés s’annulent. L’égalité permet aussi bien de
développer le produit que de factoriser la différence.
\end{demonstration}
\begin{demonstration}[Le carré d’un entier impair est impair]
Un entier impair s’écrit $2n+1$ avec n entier. Son carré vaut
$(2n+1)^2=4n^2+4n+1=2(2n^2+2n)+1$. Le nombre entre parenthèses est entier :
on obtient bien un multiple de 2 augmenté de 1.
\end{demonstration}
\editionRetenir{Une écriture générale prouve ce que quelques essais ne font que suggérer.}
'''),
('Pythagore par les aires',r'''
Considérons quatre copies d’un triangle rectangle de côtés perpendiculaires
a et b et d’hypoténuse c, disposées dans un carré de côté $a+b$.
\begin{center}\begin{tikzpicture}[scale=.65,font=\small]
\draw[geoTrait](0,0)rectangle(5,5);
\fill[otGreenTint](2,0)--(5,2)--(3,5)--(0,3)--cycle;
\draw[geoTrait](2,0)--(5,2)--(3,5)--(0,3)--cycle;
\node[below]at(1,0){$a$};\node[below]at(3.5,0){$b$};
\node[right]at(5,1){$a$};\node[right]at(5,3.5){$b$};
\node at(2.5,2.5){aire $c^2$};
\end{tikzpicture}\end{center}
Chaque côté du quadrilatère central est une hypoténuse de longueur c.
Ses angles sont droits : les deux angles aigus voisins des triangles
ont une somme de 90 degrés, et complètent un angle plat avec l’angle central.
Le quadrilatère est donc un carré.\par\medskip
L’aire du grand carré vaut $(a+b)^2$. Elle est aussi la somme de l’aire
du carré central et de celles des quatre triangles :
\[
(a+b)^2=c^2+4\times\frac{ab}{2}=c^2+2ab.
\]
En développant puis en soustrayant $2ab$, on obtient
$\res{a^2+b^2=c^2}$.
'''),
('Angles et triangles semblables',r'''
\begin{demonstration}[La somme des angles d’un triangle]
Par le sommet C du triangle ABC, tracer la parallèle à AB.
Les angles alternes-internes y reproduisent les angles A et B,
de part et d’autre de l’angle C. Les trois forment un angle plat :
leur somme vaut $180^\circ$.
\end{demonstration}
\begin{center}\begin{tikzpicture}[scale=.75,font=\small]
\draw[geoTrait](0,0)node[below]{$A$}--(5,0)node[below]{$B$}--(2,3)node[above]{$C$}--cycle;
\draw[geoAide](-1,3)--(6,3);
\node at(1.1,2.7){$\alpha$};\node at(2,2.3){$\gamma$};\node at(3.1,2.7){$\beta$};
\end{tikzpicture}\end{center}
\begin{demonstration}[Deux angles égaux suffisent]
Dans deux triangles, si deux angles sont égaux deux à deux,
le troisième est chaque fois $180^\circ$ moins la même somme.
Il est donc égal aussi : les triangles sont semblables.
\end{demonstration}
'''),
('Facteurs d’aire et de volume',r'''
\begin{demonstration}[Agrandir un rectangle]
Un rectangle de côtés L et $\ell$ devient un rectangle de côtés
$kL$ et $k\ell$ lorsque $k>0$. Son aire devient
$(kL)(k\ell)=k^2L\ell$. Une figure découpée en triangles suit le même
principe, en multipliant base et hauteur par k. Pour une homothétie
de rapport négatif, la longueur est multipliée par $|k|$, et
$|k|^2=k^2$.
\end{demonstration}
\begin{demonstration}[Agrandir un pavé]
Le volume $L\ell h$ devient $(|k|L)(|k|\ell)(|k|h)=|k|^3L\ell h$.
Ce calcul explique pourquoi une maquette au dixième n’a qu’un millième
du volume initial. Les formules des autres solides usuels vérifient
le même facteur lorsque toutes leurs longueurs subissent le même changement.
\end{demonstration}
\editionRetenir{Le nombre de facteurs de longueur explique la puissance : 1 pour une longueur, 2 pour une aire, 3 pour un volume.}
''')
]

OUTILS=[
('Mesures et formules utiles',r'''
\editionEtape{Contours et aires}
\begin{tabularx}{\linewidth}{@{}lYY@{}}\toprule
Figure & Périmètre & Aire\\\midrule
Rectangle & $2(L+\ell)$ & $L\ell$\\[2mm]
Carré & $4c$ & $c^2$\\[2mm]
Triangle & somme des côtés & base $\times$ hauteur associée / 2\\[2mm]
Parallélogramme & somme des côtés & base $\times$ hauteur associée\\[2mm]
Disque / cercle & $2\pi r$ pour le cercle & $\pi r^2$ pour le disque\\\bottomrule
\end{tabularx}
\editionEtape{Unités}
$1$ km = $1000$ m ; $1$ m = $100$ cm ; $1$ m$^2$ = $10000$ cm$^2$ ;
$1$ m$^3$ = $1000$ L ; $1$ L = $1000$ mL ; $1$ mL = $1$ cm$^3$.\par\medskip
Une durée $t$ en heures vaut $60t$ minutes. Une vitesse en km/h se
divise par 3,6 pour obtenir des m/s.
\editionEtape{Angles et triangles}
Angle plat : $180^\circ$ ; tour complet : $360^\circ$.
Dans un triangle, la somme des angles vaut $180^\circ$.
Un triangle isocèle a des angles à la base égaux ; un triangle
équilatéral a trois angles de $60^\circ$.
\editionRetenir{La hauteur d’un triangle est perpendiculaire à la base choisie. Un côté oblique n’est pas automatiquement une hauteur.}
'''),
('Données : ce que montre chaque représentation',r'''
\editionEtape{Exemple exact}
La série de pointures $38;38;39;40;40;40;42;42$ a pour effectifs
2, 1, 3, 2 aux valeurs 38, 39, 40, 42. Un tableau ou des bâtons
à ces abscisses permettent de lire les extrêmes : étendue $42-38=4$.
Un disque dont les secteurs portent ces mêmes valeurs et effectifs
permet aussi ce calcul ; les angles seraient $90^\circ$, $45^\circ$,
$135^\circ$, $90^\circ$.
\editionEtape{Exemple regroupé}
Pour des durées dans $[0;10[$, $[10;20[$, $[20;30[$ et $[30;40[$,
avec effectifs 4, 8, 6, 2, les hauteurs de l’histogramme sont
proportionnelles à ces effectifs. Pour le construire, placer les bornes
sur l’axe horizontal, choisir une graduation verticale et dessiner quatre
rectangles accolés de même largeur.\par\medskip
L’étendue exacte ne peut être retrouvée : le minimum est dans $[0;10[$
et le maximum dans $[30;40[$. On sait seulement que l’étendue est
strictement comprise entre 20 et 40 minutes. Les valeurs exactes ont été
perdues par le regroupement.
\editionEtape{Une estimation annoncée}
En remplaçant chaque classe par son centre (5, 15, 25, 35),
on estime la moyenne par $(4\times5+8\times15+6\times25+2\times35)/20=18$ min.
Cette valeur est une estimation, pas une moyenne exacte des observations inconnues.
'''),
('Décomposer en facteurs premiers avec un algorithme',r'''
\editionEtape{Une procédure en français structuré}
Choisir un entier $N\ge2$. Mettre reste à N et diviseur à 2.
Tant que reste est supérieur à 1 :\par
\begin{itemize}
\item si le reste de la division de reste par diviseur vaut 0, afficher
diviseur et remplacer reste par reste / diviseur ;
\item sinon, augmenter diviseur de 1.
\end{itemize}
La répétition teste donc de nouveau le même diviseur après une division réussie.
En blocs, employer « répéter jusqu’à reste = 1 » et une condition à deux branches.
\editionEtape{Exemple pour 84}
On affiche 2, puis 2, puis 3, puis 7. Les quotients successifs après
division sont 42, 21, 7 et 1. La décomposition vaut
$84=2^2\times3\times7$. Un diviseur composé ne sera pas affiché :
ses facteurs premiers auraient été retirés auparavant.
\editionEtape{Contrôles}
Multiplier les facteurs affichés pour retrouver N.
Tester un nombre premier, par exemple 13 : un seul facteur est affiché.
La procédure doit refuser 0, 1 et les entrées non entières dans ce cadre.
Elle termine, car soit le reste diminue par une division, soit le diviseur
augmente jusqu’à atteindre un diviseur du reste.
'''),
('Rédiger un raisonnement géométrique',r'''
\editionEtape{Une longueur avec Pythagore}
« Le triangle ABC est rectangle en A. D’après le théorème de Pythagore,
$BC^2=AB^2+AC^2$. Donc… Comme BC est une longueur positive, BC = … ».
Ne pas remplacer le carré par la longueur avant la racine.
\editionEtape{Un parallélisme avec Thalès}
« A, M, B sont alignés dans cet ordre, ainsi que A, N, C.
On compare $AM/AB$ et $AN/AC$ : … Les deux rapports sont égaux.
La réciproque de Thalès permet de conclure que $(MN)\parallel(BC)$. »
\editionEtape{Un angle avec trigonométrie}
« Dans ABC rectangle en A, pour l’angle B, le côté AC est opposé et
AB adjacent. Donc $\tan B=AC/AB$. La fonction inverse donne
$B\approx\ldots^\circ$. » Nommer l’angle évite un rapport inversé.
\editionEtape{Une transformation}
Préciser son type, son centre ou son axe, puis son angle, son déplacement
ou son rapport. Pour une homothétie négative, dire explicitement que
le point image se situe de l’autre côté du centre.
\editionRetenir{Une rédaction courte suffit si elle contient les hypothèses utiles, la propriété, le calcul et la conclusion.}
''')
]
