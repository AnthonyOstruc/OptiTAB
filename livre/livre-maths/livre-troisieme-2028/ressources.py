PREUVES=[
('Identités remarquables et parité',r'''
\begin{demonstration}[Les trois identités remarquables]
Par double distributivité, $(a+b)^2=(a+b)(a+b)=a^2+ab+ba+b^2=a^2+2ab+b^2$.
De même, $(a-b)^2=a^2-ab-ba+b^2=a^2-2ab+b^2$. Enfin
$(a-b)(a+b)=a^2+ab-ab-b^2=a^2-b^2$ : les deux termes opposés s’annulent.
Lues de droite à gauche, ces égalités permettent de factoriser.
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
('Thalès par les aires',r'''
Dans le triangle ABC, M appartient à [AB], N à [AC] et $(MN)\parallel(BC)$.
On note $\mathcal A$ l’aire d’un triangle.
\begin{center}\begin{tikzpicture}[scale=.5,font=\small]
\draw[geoTrait](0,0)node[below left]{$A$}--(10,0)node[below right]{$B$}--(4,6)node[above]{$C$}--cycle;
\draw[geoTrait](6,0)node[below]{$M$}--(2.4,3.6)node[left]{$N$};
\draw[otMuted,dashed](6,0)--(4,6) (2.4,3.6)--(10,0);
\end{tikzpicture}\end{center}
\begin{demonstration}[Deux triangles de même aire]
B et C sont sur une droite parallèle à (MN) : ils sont à la même distance
de (MN). Les triangles MNB et MNC ont donc la même base [MN] et la même
hauteur : $\mathcal A(MNB)=\mathcal A(MNC)$. En ajoutant l’aire de AMN,
on obtient $\mathcal A(ANB)=\mathcal A(AMC)$.
\end{demonstration}
\begin{demonstration}[L’égalité des rapports]
Les triangles AMN et ABN ont la même hauteur issue de N ; leurs bases
[AM] et [AB] sont sur la même droite. Donc
$\dfrac{\mathcal A(AMN)}{\mathcal A(ABN)}=\dfrac{AM}{AB}$. De même, avec la
hauteur issue de M, $\dfrac{\mathcal A(AMN)}{\mathcal A(AMC)}=\dfrac{AN}{AC}$.
Les dénominateurs sont égaux d’après la première étape :
$\res{\dfrac{AM}{AB}=\dfrac{AN}{AC}}$.
\end{demonstration}
'''),
('Trigonométrie et vecteurs',r'''
\begin{demonstration}[$(\cos\widehat B)^2+(\sin\widehat B)^2=1$]
Dans ABC rectangle en A, $\cos\widehat B=AB/BC$ et $\sin\widehat B=AC/BC$. Donc
$(\cos\widehat B)^2+(\sin\widehat B)^2=\dfrac{AB^2+AC^2}{BC^2}$. D’après le théorème
de Pythagore, $AB^2+AC^2=BC^2$ : la somme vaut 1. Connaissant le cosinus
d’un angle aigu, on en déduit son sinus, qui est positif.
\end{demonstration}
\begin{demonstration}[La règle du parallélogramme]
Si ABCD est un parallélogramme, ses côtés opposés [AD] et [BC] sont
parallèles, de même longueur, et parcourus dans le même sens :
$\vect{AD}=\vect{BC}$. Par la relation de Chasles,
$\vect{AB}+\vect{AD}=\vect{AB}+\vect{BC}=\vect{AC}$.
\end{demonstration}
\editionRetenir{Une égalité de vecteurs traduit à la fois un parallélisme, un sens et une égalité de longueurs.}
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
\editionEtape{Volumes}
Pavé : $L\ell h$ ; prisme droit et cylindre : aire de la base $\times$ hauteur ;
pyramide et cône : aire de la base $\times$ hauteur / 3 ; boule de rayon $r$ : $\frac43\pi r^3$.
\editionEtape{Unités}
$1$ km = $1000$ m ; $1$ m = $100$ cm ; $1$ m$^2$ = $10000$ cm$^2$ ;
$1$ m$^3$ = $1000$ L ; $1$ L = $1000$ mL ; $1$ mL = $1$ cm$^3$.
Une vitesse en km/h se divise par 3,6 pour obtenir des m/s.
\editionRetenir{La hauteur d’un triangle est perpendiculaire à la base choisie. Un côté oblique n’est pas automatiquement une hauteur.}
'''),
('Données : quartiles et boîtes à moustaches',r'''
\editionEtape{Un exemple complet}
La série de pointures $36\,;37\,;37\,;38\,;38\,;38\,;39\,;40\,;40\,;42\,;43\,;44$ compte
$N=12$ valeurs. La moyenne vaut $472/12\approx39{,}3$. La médiane est la moyenne des
6\textsuperscript{e} et 7\textsuperscript{e} valeurs : $(38+39)/2=38{,}5$.
\editionEtape{Quartiles}
$12\times0{,}25=3$ : $Q_1$ est la 3\textsuperscript{e} valeur, soit 37.
$12\times0{,}75=9$ : $Q_3$ est la 9\textsuperscript{e} valeur, soit 40.
Au moins 25 \% des pointures sont inférieures ou égales à 37, au moins 75 \%
inférieures ou égales à 40.
\editionEtape{Boîte à moustaches}
\begin{center}\begin{tikzpicture}[x=.62cm,font=\small]
\draw[otMuted,->](35,0)--(45.5,0);
\foreach\t in{35,...,45}{\draw[otMuted](\t,.07)--(\t,-.07)node[below,font=\tiny]{\t};}
\draw[geoTrait](36,.7)--(37,.7) (40,.7)--(44,.7) (36,.55)--(36,.85) (44,.55)--(44,.85);
\draw[geoTrait](37,.4)rectangle(40,1);\draw[geoTrait,line width=1.4pt](38.5,.4)--(38.5,1);
\end{tikzpicture}\end{center}
Minimum 36, $Q_1=37$, médiane 38,5, $Q_3=40$, maximum 44 ; l’étendue vaut 8.
\editionRetenir{La boîte contient environ la moitié centrale des valeurs ; sa longueur $Q_3-Q_1$ mesure leur dispersion.}
'''),
('Décomposer en facteurs premiers avec un algorithme',r'''
\editionEtape{Une procédure en français structuré}
Choisir un entier $N\ge2$. Mettre reste à N et diviseur à 2.
Répéter jusqu’à ce que reste soit égal à 1 :\par
\begin{itemize}
\item si le reste de la division de reste par diviseur vaut 0, afficher
diviseur et remplacer reste par reste / diviseur ;
\item sinon, augmenter diviseur de 1.
\end{itemize}
La boucle conditionnelle teste donc de nouveau le même diviseur après une division réussie.
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
Pour prouver qu’un triangle n’est pas rectangle, citer la contraposée.
\editionEtape{Un parallélisme avec Thalès}
« A, M, B sont alignés dans cet ordre, ainsi que A, N, C.
On compare $AM/AB$ et $AN/AC$ : … Les deux rapports sont égaux.
D’après la réciproque du théorème de Thalès, $(MN)\parallel(BC)$. »
Si les rapports diffèrent, conclure avec la contraposée.
\editionEtape{Un angle avec la trigonométrie}
« Dans ABC rectangle en A, pour l’angle $\widehat B$, le côté AC est opposé et
AB adjacent. Donc $\tan\widehat B=AC/AB$. La fonction inverse donne
$\widehat B\approx\ldots^\circ$. » Nommer l’angle évite un rapport inversé.
\editionEtape{Une égalité de vecteurs}
« ABCD est un parallélogramme, donc $\vect{AB}=\vect{DC}$. » Pour démontrer
qu’un quadrilatère est un parallélogramme, établir une égalité de vecteurs
en respectant l’ordre des lettres.
\editionRetenir{Une rédaction courte suffit si elle contient les hypothèses utiles, la propriété, le calcul et la conclusion.}
''')
]
