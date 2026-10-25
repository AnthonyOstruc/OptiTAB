from dataclasses import dataclass
@dataclass
class Defi:
    titre:str
    enonce:str
    indices:list
    corrige:str
    controle:str
    figure:str=''

DEFIS=[
Defi('Cent termes, sans cent calculs',r"Calculer $S=-1+2-3+4-\cdots-99+100$ sans additionner terme par terme. Expliquer le résultat. Que vaut la somme si l’on s’arrête à $-99$ ?",
['Regrouper les termes par paires consécutives.','Chaque paire $-(2k-1)+2k$ vaut 1.'],
r'''\editionEtape{Regrouper sans changer l’ordre}On écrit $(-1+2)+(-3+4)+\cdots+(-99+100)$. Chaque parenthèse vaut 1. Les 100 termes forment 50 paires, donc $\res{S=50}$.
\editionEtape{Retirer le dernier terme}S’arrêter à $-99$ signifie enlever le terme $+100$ de la somme précédente : $50-100=\res{-50}$.
\editionEtape{Contrôle}Avec seulement quatre termes, $-1+2-3+4=2$ : on retrouve deux paires. Le raisonnement repose sur la même structure pour les 50 paires, pas sur une supposition à partir du petit exemple.''',
"assert sum((-1 if k%2 else 1)*k for k in range(1,101))==50 and sum((-1 if k%2 else 1)*k for k in range(1,100))==-50"),
Defi('Retrouver tout le budget',r"On utilise un tiers d’un budget, puis un quart du reste, puis trois cinquièmes du nouveau reste. Il reste alors 18 euros. Retrouver le budget et les trois sommes utilisées.",
['Exprimer chaque reste comme fraction du budget initial.','Le reste final représente $(2/3)(3/4)(2/5)$ du total.'],
r'''\editionEtape{Suivre les restes}Après la première utilisation, il reste $2/3$ du budget. Après la deuxième, il reste $(3/4)(2/3)=1/2$ du budget. La troisième conserve $2/5$ de ce montant, soit $1/5$ du budget initial.
\editionEtape{Revenir au total}Un cinquième vaut 18 euros, donc le budget est $\res{90}$ euros.
\editionEtape{Calculer les parts}Le tiers initial est 30 euros. Il reste 60 ; son quart est 15. Il reste 45 ; les trois cinquièmes valent 27. Contrôle : $30+15+27+18=90$. Les fractions successives ne portaient pas sur le même total.''',
"assert (1-Rational(1,3))*(1-Rational(1,4))*(1-Rational(3,5))==Rational(1,5) and 30+15+27+18==90"),
Defi('Jusqu’où peut-on doubler ?',r"Une mémoire fictive contient au départ un seul élément. À chaque étape, le nombre d’éléments double. Sa capacité maximale est un million d’éléments. Quel est le plus grand nombre d’étapes possible ? Donner un encadrement avec deux puissances de 2.",
['Après $n$ étapes, combien de facteurs 2 a-t-on introduits ?','Calculer $2^{10}$, puis comparer $2^{19}$ et $2^{20}$ à un million.'],
r'''\editionEtape{Modéliser}Au départ, il y a 1 élément. Après $n$ étapes, il y en a $2^n$ : une étape correspond à un nouveau facteur 2.
\editionEtape{Encadrer la capacité}$2^{19}=524\,288$ et $2^{20}=1\,048\,576$. Ainsi $2^{19}<1\,000\,000<2^{20}$.
\editionEtape{Conclure}On peut effectuer $\res{19}$ étapes complètes. Une vingtième dépasserait la capacité. On ne compte pas la valeur de départ comme une étape de doublement.''',
"assert 2**19==524288<1000000<2**20==1048576"),
Defi('Quatre carreaux pour un grand carré',r"Quatre carreaux carrés identiques, chacun d’aire 18 cm$^2$, sont assemblés en un grand carré, en deux lignes et deux colonnes. Déterminer le côté et le périmètre exacts du grand carré. Comparer le rapport des côtés et celui des aires.",
['Le côté du grand carré contient deux côtés de carreaux.',r'Son aire est la somme des quatre aires ; sa longueur est aussi $\sqrt{72}$.'],
r'''\editionEtape{Du carreau à l’assemblage}Un carreau a pour côté $\sqrt{18}$ cm. Le grand carré a donc pour côté $\res{2\sqrt{18}\ \mathrm{cm}}$ et pour périmètre $\res{8\sqrt{18}\ \mathrm{cm}}$.
\editionEtape{Un second calcul}L’aire totale vaut $4\times18=72$ cm$^2$, donc le côté est aussi $\sqrt{72}$ cm. Ces deux écritures sont égales : $2\sqrt{18}$ est positif et son carré vaut $4\times18=72$.
\editionEtape{Comparer}Le rapport des côtés est 2, celui des aires 4. Doubler toutes les longueurs ne double pas l’aire : il la multiplie par le carré du rapport.''',
"assert simplify(2*sqrt(18)-sqrt(72))==0 and (2*sqrt(18))**2==72",'defi-racine'),
Defi('Comparer sans choisir de valeur',r"Pour $x>0$, un rectangle A mesure 3 cm sur $x+4$ cm. Un rectangle B mesure 2 cm sur $x+6$ cm. Quelle aire est la plus grande ? Est-il possible qu’elles soient égales pour une longueur $x$ strictement positive ?",
['Développer les deux expressions d’aire.','Calculer l’aire de A moins celle de B.'],
r'''\editionEtape{Écrire les aires}$A=3(x+4)=3x+12$ et $B=2(x+6)=2x+12$, en cm$^2$.
\editionEtape{Comparer en général}$A-B=(3x+12)-(2x+12)=x$. Puisque $x>0$, cette différence est positive : $\res{A>B}$ pour toutes les longueurs admises.
\editionEtape{Étudier l’égalité}L’égalité des aires imposerait $x=0$, exclu par l’énoncé. Tester plusieurs nombres n’aurait pas prouvé la conclusion pour tous les nombres positifs ; la différence littérale le permet.''',
"assert expand(3*(x+4)-2*(x+6))==x",'defi-litteral'),
Defi('Compter les pièces',r"Une boîte contient 42 pièces, uniquement de 1 euro et de 2 euros. La somme vaut 68 euros. Trouver le nombre de pièces de chaque sorte. Justifier que les deux contraintes sont satisfaites.",
['Appeler $x$ le nombre de pièces de 2 euros.','Il reste $42-x$ pièces de 1 euro.'],
r'''\editionEtape{Choisir une inconnue}Si $x$ est le nombre de pièces de 2 euros, il y a $42-x$ pièces de 1 euro. Leur valeur totale vaut $2x+(42-x)$.
\editionEtape{Résoudre}L’équation $2x+42-x=68$ se réduit en $x+42=68$, donc $\res{x=26}$. Il reste $\res{16}$ pièces de 1 euro.
\editionEtape{Vérifier le contexte}Les nombres sont entiers et non négatifs. On compte $26+16=42$ pièces et $2\times26+16=68$ euros. Contrôler seulement la somme d’argent n’aurait pas vérifié le nombre total de pièces.''',
"assert solve(2*x+(42-x)-68,x)==[26] and 26+16==42 and 2*26+16==68"),
Defi('Annuler une remise',r"Un prix baisse de 20\,\%. De quel pourcentage faut-il augmenter le nouveau prix pour retrouver l’ancien ? Prouver que le pourcentage obtenu ne dépend pas du prix initial positif.",
[r'Après la baisse, il reste 80\,\% du prix initial.','La somme à rajouter représente 20 parts sur les 80 parts du nouveau prix.'],
r'''\editionEtape{Raisonner sur des parts}Pour 100 euros au départ, le nouveau prix est 80 euros. Il faut rajouter 20 euros, soit $20/80=1/4=\res{25\,\%}$ du nouveau prix.
\editionEtape{Généraliser}Avec un prix initial $P>0$, le nouveau vaut $0{,}8P$. Une hausse de 25\,\% rajoute $0{,}25\times0{,}8P=0{,}2P$. Le prix final est $0{,}8P+0{,}2P=P$.
\editionEtape{Éviter le piège}Une hausse de 20\,\% n’ajouterait que $0{,}16P$ ; elle donnerait $0{,}96P$. Les deux pourcentages successifs ne portent pas sur la même base.''',
"assert Rational(20,80)==Rational(25,100) and Rational('.8')*Rational('1.25')==1"),
Defi('Un remplissage avec fuite',r"Un bassin de 900 L contient 75 L au départ. Un robinet débite 18 L/min ; une fuite retire 3 L/min. Après 20 min, la fuite est réparée et le robinet continue. Combien de temps faut-il au total pour remplir le bassin ?",
['Distinguer les deux périodes.','Après 20 minutes, le volume a augmenté de $20(18-3)$ litres.'],
r'''\editionEtape{Première période}Le débit net est $18-3=15$ L/min. En 20 min, le bassin gagne 300 L. Il contient alors $75+300=375$ L.
\editionEtape{Après réparation}Il manque $900-375=525$ L, fournis à 18 L/min. La durée restante vaut $525/18=175/6$ min, soit 29 min 10 s.
\editionEtape{Durée totale}On ajoute les 20 premières minutes : $\res{49\text{ min }10\text{ s}}$. Utiliser un débit moyen non justifié sur les deux phases masquerait le changement dû à la réparation.''',
"assert 75+20*(18-3)==375 and Rational(900-375,18)+20==Rational(295,6)"),
Defi('Un découpage variable',r"Dans un rectangle de 18 cm sur 10 cm, on retire quatre carrés de côté $x$ cm aux coins, avec $0<x<5$. Donner la formule de l’aire restante. Parmi $x=2,3,4$, lequel laisse 116 cm$^2$ ? Peut-on retrouver ce choix sans tester les trois ?",
['L’aire retirée est $4x^2$.','Si l’aire restante est 116, chaque carré retiré a une aire de 16.'],
r'''\editionEtape{Établir la formule}L’aire initiale est 180 cm$^2$, donc $\res{A=180-4x^2}$.
\editionEtape{Calculer les trois cas}Pour $x=2,3,4$, les aires restantes valent respectivement 164, 144 et $\res{116}$ cm$^2$. Le choix est $x=4$ cm.
\editionEtape{Retrouver directement}Retirer $180-116=64$ cm$^2$ en quatre carrés identiques donne 16 cm$^2$ par carré. Le côté positif vaut $\sqrt{16}=4$ cm. La contrainte $0<x<5$ est respectée.''',
"assert [180-4*a*a for a in [2,3,4]]==[164,144,116] and sqrt(Rational(180-116,4))==4",'coins-retires'),
Defi('Même moyenne, autre médiane',r"Comparer les séries A : 4, 4, 4, 16, 16, 16 et B : 0, 8, 8, 8, 8, 28. Calculer moyenne et médiane. Que peut-on conclure sur l’information fournie par une moyenne seule ?",
['Les deux sommes valent 60.','Avec six valeurs, observer les rangs 3 et 4.'],
r'''\editionEtape{Moyennes}Les sommes valent 60 et les effectifs 6. Les deux moyennes valent donc $\res{10}$.
\editionEtape{Médianes}Pour A, les deux valeurs centrales sont 4 et 16 : la médiane choisie est 10. Pour B, elles sont 8 et 8 : la médiane vaut 8.
\editionEtape{Interpréter}Une même moyenne n’impose pas une même médiane ni une même répartition. La valeur 28 compense les petites valeurs de B dans la somme. Pour décrire une série, il faut préciser l’indicateur utilisé et ne pas lui faire dire davantage que ce qu’il mesure.''',
"assert sum([4,4,4,16,16,16])==sum([0,8,8,8,8,28])==60 and Rational(4+16,2)==10 and Rational(8+8,2)==8"),
Defi('Une cible et une comparaison exacte',r"Un point est choisi uniformément dans un carré de côté 8 cm. On gagne s’il appartient au disque central de rayon 2 cm. Donner la probabilité exacte et montrer qu’elle est inférieure à $1/5$, en utilisant $\pi<3{,}2$.",
['Comparer l’aire du disque à celle du carré.',r'Le quotient se simplifie en $\pi/16$.'],
r'''\editionEtape{Calculer les aires}L’aire totale vaut 64 cm$^2$, l’aire gagnante $4\pi$ cm$^2$. Le modèle uniforme donne $\res{P=4\pi/64=\pi/16}$.
\editionEtape{Comparer sans arrondi}Comme $\pi<3{,}2$, on a $\pi/16<3{,}2/16=0{,}2=1/5$.
\editionEtape{Interpréter}La probabilité est d’environ 19,6\,\%, légèrement inférieure à 20\,\%. Le calcul porte sur des aires, car le point est uniforme sur la surface. Un rapport de rayons et de côtés ne représenterait pas ce modèle.''',
"assert simplify(pi*2**2/8**2)==pi/16 and pi/16<Rational(1,5)",'defi-cible'),
Defi('Une droite, trois rôles',r"ABC est isocèle en A et M est le milieu de BC. En comparant deux triangles, montrer que AM est à la fois une médiane, une hauteur et la bissectrice de l’angle A. Une bissectrice partage un angle en deux angles égaux.",
['Comparer ABM et ACM avec trois côtés.','Les deux angles en M sont égaux et supplémentaires.'],
r'''\editionEtape{Comparer les triangles}$AB=AC$, $BM=CM$ et AM est commun. Les triangles ABM et ACM sont égaux par le cas CCC.
\editionEtape{Au sommet A}Les angles BAM et MAC se correspondent, donc ils sont égaux. AM est la bissectrice de l’angle A.
\editionEtape{Au point M}Les angles AMB et AMC sont égaux et ont pour somme $180^\circ$ ; chacun vaut $90^\circ$. AM est donc une hauteur. Enfin, c’est une médiane par définition puisqu’elle joint A au milieu de BC. Les trois rôles sont prouvés à partir des données.''',
"assert Rational(180,2)==90",'defi-triangles'),
Defi('Le câble et ses attaches',r"Un câble doit suivre l’hypoténuse d’un triangle rectangle de côtés perpendiculaires 9 m et 12 m. Il faut en plus 0,75 m à chaque extrémité pour les attaches. Le câble coûte 4,80 euros par mètre. Calculer la longueur et le coût exacts.",
['Calculer d’abord la distance entre les points d’attache.','Deux extrémités demandent deux réserves de 0,75 m.'],
r'''\editionEtape{Distance à franchir}Par Pythagore, $d^2=9^2+12^2=225$, donc $d=15$ m.
\editionEtape{Ajouter les réserves}La longueur totale est $15+2\times0{,}75=\res{16{,}5\ \mathrm m}$. La réserve n’est pas un côté du triangle et n’entre pas sous la racine.
\editionEtape{Calculer le coût}$16{,}5\times4{,}80=\res{79{,}20}$ euros. On suppose que la longueur peut être achetée au dixième de mètre sans supplément ; aucun arrondi de lot n’est demandé.''',
"assert sqrt(9**2+12**2)+2*Rational('.75')==Rational('16.5') and Rational('16.5')*Rational('4.8')==Rational('79.2')",'defi-pyth'),
Defi('Une bande entre triangles',r"ABC est rectangle en A, $AB=12$ et $AC=16$ cm. M est sur AB, avec $AM=3$ cm. La parallèle à BC par M coupe AC en N. Calculer AN, MN, puis l’aire de la partie de ABC extérieure à AMN.",
['Le rapport petit sur grand vaut $1/4$.','Calculer BC par Pythagore et les deux aires séparément.'],
r'''\editionEtape{Les longueurs}Thalès donne $AN=16/4=\res4$ cm. Par Pythagore, $BC=\sqrt{144+256}=20$ cm. Donc $MN=20/4=\res5$ cm.
\editionEtape{Les aires}ABC a pour aire $12\times16/2=96$ cm$^2$ et AMN $3\times4/2=6$ cm$^2$. La partie extérieure a donc une aire de $\res{90\ \mathrm{cm}^2}$.
\editionEtape{Contrôle}Le rapport des longueurs est $1/4$, mais celui des aires est $6/96=1/16$. L’aire du petit triangle n’est pas le quart de la grande.''',
"assert sqrt(12**2+16**2)==20 and Rational(12*16-3*4,2)==90 and Rational(6,96)==Rational(1,16)",'defi-thales'),
Defi('Choisir la bonne inclinaison',r"Une barre de 10 m forme l’hypoténuse d’un triangle rectangle. Son côté horizontal adjacent à l’angle étudié peut mesurer 5, 6 ou 7 m. Quel choix donne un angle compris entre $50^\circ$ et $55^\circ$ ? Justifier les trois essais.",
['Écrire le cosinus avec chaque longueur horizontale.','Utiliser le cosinus inverse en degrés pour les trois rapports.'],
r'''\editionEtape{Trois rapports}Les cosinus valent $5/10$, $6/10$ et $7/10$.
\editionEtape{Trois angles}Les angles sont respectivement $60^\circ$, environ $53{,}13^\circ$ et environ $45{,}57^\circ$.
\editionEtape{Choisir}Seul le côté horizontal de $\res6$ m convient à l’intervalle demandé. Le schéma rappelle les deux côtés intervenant dans le rapport. Une mesure au rapporteur sur ce dessin de principe ne remplacerait pas les calculs.''',
"assert [50<=math.degrees(math.acos(a/10))<=55 for a in [5,6,7]]==[False,True,False]",'defi-cosinus'),
Defi('Deux glissements, une construction',r"Le triangle a pour sommets A(0;1), B(2;1), C(1;3). On le déplace de 4 carreaux à droite et 2 en bas, puis de 1 à gauche et 5 en haut. Donner les deux triangles images. Le déplacement final conserve-t-il l’aire ?",
['Additionner séparément les déplacements horizontaux et verticaux.','Le déplacement total est de 3 à droite et 3 en haut.'],
r'''\editionEtape{Première image}On ajoute $(4;-2)$ : $A'(4;-1)$, $B'(6;-1)$ et $C'(5;1)$.
\editionEtape{Seconde image}On ajoute ensuite $(-1;5)$ : $\res{A''(3;4),\ B''(5;4),\ C''(4;6)}$. Depuis la figure initiale, le glissement unique ajoute $(3;3)$.
\editionEtape{Aire}Chaque translation conserve l’aire et les longueurs. L’image finale a donc la même aire que le triangle initial, malgré son changement de place. Les deux déplacements sont à reproduire avec leurs sens.''',
"assert [(a+3,b+3) for a,b in [(0,1),(2,1),(1,3)]]==[(3,4),(5,4),(4,6)]",'defi-translation'),
Defi('Un volume sous deux formes',r"Une pyramide de base carrée de côté 6 cm et de hauteur 8 cm est comparée à un prisme droit de même base et de même hauteur. Calculer les deux volumes. Combien de remplissages de la pyramide faut-il verser pour remplir le prisme sans perte ? Puis réduire les deux solides de moitié.",
['Les deux volumes diffèrent par le facteur $1/3$.','Réduire les longueurs de moitié divise le volume par 8.'],
r'''\editionEtape{Volumes initiaux}L’aire de base vaut 36 cm$^2$. Le prisme a pour volume $36\times8=\res{288}$ cm$^3$, la pyramide $288/3=\res{96}$ cm$^3$. Il faut donc trois remplissages pour transférer le même volume de liquide.
\editionEtape{Réduction}Avec un rapport de longueurs $1/2$, le facteur de volume est $1/8$. Les nouveaux volumes sont 36 et 12 cm$^3$.
\editionEtape{Comparer}Le rapport 3 entre les volumes est conservé. Il s’agit de volumes de remplissage : on n’affirme pas que trois objets rigides se rangent nécessairement dans le prisme.''',
"assert Rational(6**2*8,3)==96 and 6**2*8==288 and Rational(288,8)==36 and Rational(96,8)==12",'defi-pyramide'),
Defi('Une somme programmée et prouvée',r"Exécuter mentalement le script pour les entiers de 1 à 10. Donner s et n à la fin. Retrouver la somme en regroupant les entiers par paires. Que se passerait-il si « mettre s à 0 » était déplacé à l’intérieur de la boucle ?",
['n vaut le prochain entier à ajouter.','Regrouper $1+10$, $2+9$, etc.'],
r'''\editionEtape{Suivre les variables}Les dix tours ajoutent les entiers 1 à 10. À la fin, $\res{s=55}$ et $\res{n=11}$ : la dernière augmentation de n a bien lieu après l’ajout de 10.
\editionEtape{Une preuve sans dix additions}Regrouper $1+10$, $2+9$, $3+8$, $4+7$, $5+6$. Les cinq paires valent 11, donc la somme est $5\times11=55$.
\editionEtape{Repérer l’erreur}Si s était remis à 0 à chaque tour, les sommes précédentes seraient perdues. Au dernier tour, on n’aurait plus que l’ajout de 10, donc s vaudrait 10.''',
"assert sum(range(1,11))==55 and 5*11==55",'defi-script')
]
