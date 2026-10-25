PREUVES=[
('Pourquoi le produit de deux négatifs est-il positif ?',r'''
\editionEtape{Partir de l’opposé}Soient $a$ et $b$ positifs. Comme $b+(-b)=0$, multiplier par $a$ donne $ab+a(-b)=0$ par distributivité. Ainsi $a(-b)$ est l’opposé de $ab$ : $a(-b)=-ab$.
\editionEtape{Changer aussi le premier signe}De même, $a+(-a)=0$. En multipliant par $-b$, on obtient $a(-b)+(-a)(-b)=0$. On sait que $a(-b)=-ab$ ; donc $(-a)(-b)$ est l’opposé de $-ab$, soit $ab$.
\editionEtape{Ce que prouve le raisonnement}La règle des signes est cohérente avec la distributivité et la notion d’opposé. Elle ne repose pas seulement sur une convention isolée à mémoriser. Le cas d’un facteur nul se traite à part : son produit vaut 0.
\editionRetenir{Deux facteurs négatifs donnent un produit positif parce que ce produit doit être l’opposé d’un produit négatif pour que la distributivité reste vraie.}'''),
('Pourquoi diviser par une fraction revient-il à inverser ?',r'''
\editionEtape{Utiliser la définition du quotient}Pour $v\ne0$, le quotient $u/v$ est l’unique nombre $q$ tel que $qv=u$.
\editionEtape{Tester une expression}L’inverse de $v$ vérifie $v\times(1/v)=1$. Le nombre $u\times(1/v)$, multiplié par $v$, donne $u\times[(1/v)\times v]=u$. C’est donc le quotient $u/v$.
\editionEtape{Appliquer aux fractions}Si $v=c/d$ avec $c,d\ne0$, son inverse est $d/c$ car $(c/d)(d/c)=1$. Ainsi $\frac ab:\frac cd=\frac ab\times\frac dc$, avec tous les dénominateurs non nuls.
\editionEtape{Un exemple contrôlé}$\frac34:\frac25=\frac34\times\frac52=\frac{15}{8}$. Vérifier en sens inverse : $\frac{15}{8}\times\frac25=\frac34$. On inverse uniquement le diviseur.
\editionRetenir{Pour justifier un quotient, remultiplier la réponse par le diviseur : on doit retrouver le dividende.}'''),
('Pythagore par une comparaison d’aires',r'''
\editionEtape{Construire la figure}On place quatre triangles rectangles identiques, de côtés perpendiculaires $a,b$ et d’hypoténuse $c$, dans un carré de côté $a+b$. Le quadrilatère central a quatre côtés de longueur $c$. Ses angles sont droits car les deux angles aigus d’un triangle rectangle ont pour somme $90^\circ$ : c’est un carré.
\figureGeo{preuve-pythagore}
\editionEtape{Compter deux fois la même aire}Le grand carré a pour aire $(a+b)^2$. La somme des aires des quatre triangles et du carré central est $4(ab/2)+c^2=2ab+c^2$.
\editionEtape{Comparer}En partageant un carré de côté $a+b$ en deux carrés et deux rectangles, on obtient aussi son aire $a^2+2ab+b^2$. Les deux calculs donnent $a^2+2ab+b^2=2ab+c^2$. En soustrayant $2ab$, il reste $\res{a^2+b^2=c^2}$.
\editionRetenir{Le théorème compare les aires des carrés construits sur les côtés. Cette preuve concerne le triangle rectangle, hypothèse essentielle.}'''),
('Pourquoi le cosinus dépend-il de l’angle ?',r'''
\editionEtape{Deux triangles rectangles emboîtés}On considère un triangle ABC rectangle en B et un point M sur AB. La parallèle à BC par M coupe AC en N. Le triangle AMN est rectangle en M ; il a le même angle aigu en A que le grand triangle.
\figureGeo{cours-thales}
\editionEtape{Appliquer Thalès}On a $AM/AB=AN/AC$. Les longueurs étant non nulles, les produits en croix donnent $AM\times AC=AN\times AB$, puis $AM/AN=AB/AC$.
\editionEtape{Interpréter}Le rapport côté adjacent à A sur hypoténuse est donc le même dans les deux triangles. On peut agrandir ou réduire le triangle sans le changer tant que l’angle est conservé : c’est ce rapport qui définit le cosinus de l’angle.
\editionRetenir{Un cosinus est un rapport de longueurs, donc un nombre sans unité. Le choix de l’angle fixe le côté adjacent ; l’hypoténuse reste opposée à l’angle droit.}''')
]
OUTILS=[
('Calculs et algèbre',r'''
\editionEtape{Fractions et relatifs}Pour additionner des fractions, utiliser un même dénominateur. Pour multiplier, multiplier les numérateurs entre eux et les dénominateurs entre eux. Pour diviser par une fraction non nulle, multiplier par son inverse. Avant un produit de relatifs, contrôler le signe.
\editionEtape{Puissances et racines}Une puissance positive est un produit répété. $10^{-n}=1/10^n$ ; l’écriture scientifique positive est $a\times10^n$ avec $1\le a<10$. Pour $b\ge0$, $\sqrt b$ est non négatif et son carré vaut $b$.
\editionEtape{Distributivité}$k(a+b)=ka+kb$. Développer va du produit vers la somme ; factoriser fait le chemin inverse. Réduire uniquement des termes de même nature.
\editionEtape{Équation}Développer et réduire, appliquer les mêmes opérations aux deux membres, isoler l’inconnue. Vérifier ensuite dans l’équation initiale et dans le contexte.
\editionRetenir{Une égalité exacte utilise $=$. Une valeur arrondie utilise $\approx$. Conserver le résultat exact ou la valeur complète de la calculatrice jusqu’au dernier calcul.}'''),
('Conversions et formules',r'''
\editionEtape{Temps et vitesses}$1$ h $=60$ min $=3600$ s. $v=d/t$, $d=vt$, $t=d/v$. De km/h à m/s : diviser par 3,6. Dans l’autre sens : multiplier par 3,6.
\editionEtape{Volumes et débits}$1$ m$^3=1000$ L ; $1$ L $=1$ dm$^3$ ; $1$ mL $=1$ cm$^3$. $q=V/t$. Pour convertir un débit, traiter séparément le volume et l’unité de temps.
\editionEtape{Aires}Rectangle : $L\ell$. Triangle : base $\times$ hauteur associée divisée par 2. Disque : $\pi r^2$. Circonférence : $2\pi r$. Une hauteur de triangle est perpendiculaire à la droite de sa base.
\editionEtape{Volumes}Pavé : $L\ell h$. Prisme et cylindre : aire de base $\times h$. Pyramide et cône : aire de base $\times h/3$. Pour le cône : $\pi r^2h/3$.
\editionEtape{Agrandir ou réduire}Un rapport positif $k$ agit sur les longueurs par $k$, sur les aires par $k^2$ et sur les volumes par $k^3$. Les angles sont conservés.
\editionRetenir{Avant de multiplier deux mesures, choisir des unités compatibles. Une longueur en cm et une aire en cm$^2$ donnent un volume en cm$^3$.}'''),
('Choisir un outil géométrique',r'''
\editionEtape{Une longueur dans un triangle rectangle}Deux côtés connus : Pythagore. Un angle aigu et un côté connu : cosinus si l’on dispose de l’adjacent ou de l’hypoténuse. Écrire le rapport avant de choisir une opération.
\editionEtape{Démontrer un angle droit}Comparer le carré du plus long côté à la somme des deux autres carrés. Si les deux calculs sont égaux, utiliser la réciproque de Pythagore et nommer le sommet opposé au plus long côté.
\editionEtape{Des parallèles et des triangles emboîtés}Thalès pour calculer à partir d’un parallélisme connu. Sa réciproque pour prouver un parallélisme à partir de rapports égaux. Vérifier alignements, ordre des points et correspondance.
\editionEtape{Comparer deux triangles}Chercher CCC, CAC ou ACA. Respecter les sommets correspondants, puis transférer une longueur ou un angle. Une translation conserve les mesures et fournit des parallélogrammes.
\editionRetenir{Une preuve cite ses données et sa propriété. Un codage issu de l’énoncé est une donnée ; une mesure approximative du dessin est seulement un indice pour chercher.}'''),
('Données, hasard et programmation',r'''
\editionEtape{Données}Fréquence = effectif de la catégorie / effectif total. Moyenne = somme des valeurs répétées / effectif total. Pour une médiane, ranger les valeurs et trouver les rangs centraux. Angle d’un secteur = fréquence $\times360^\circ$.
\editionEtape{Hasard}Définir l’expérience et les issues. Vérifier l’équiprobabilité avant de compter favorable / total. Pour le contraire : $1-P(A)$. Dans un modèle uniforme sur une cible, comparer les aires. Ne pas confondre modèle de probabilité et fréquence observée.
\editionEtape{Graphiques}Lire titre, axes, unités et graduations. Pour une lecture inverse, parcourir toutes les intersections de l’horizontale avec le tracé. Une droite doit passer par l’origine pour représenter une proportionnalité.
\editionEtape{Scripts}Repérer le déclencheur ; initialiser ; suivre l’ordre des blocs ; noter les variables ; compter les tours ; tester les cas limites. Pour un dessin, préciser départ, orientation et stylo. Dans un tableur, une référence relative change quand on recopie une formule.
\editionRetenir{Après correction, refaire une question sans aide et expliquer l’idée qui l’a résolue. Le but est de retrouver la méthode, pas de reconnaître le résultat.}''')
]
