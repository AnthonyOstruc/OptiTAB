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
\editionEtape{Retirer le dernier terme}S’arrêter à $-99$ revient à enlever le terme $+100$ de la somme précédente : $50-100=\res{-50}$.
\editionEtape{Contrôle}Avec seulement quatre termes, $-1+2-3+4=2$ : on retrouve deux paires. Le raisonnement repose sur la même structure pour les 50 paires, pas sur une supposition tirée du petit exemple.''',
"assert sum((-1 if k%2 else 1)*k for k in range(1,101))==50 and sum((-1 if k%2 else 1)*k for k in range(1,100))==-50"),
Defi('Retrouver tout le budget',r"On utilise un tiers d’un budget, puis un quart du reste, puis trois cinquièmes du nouveau reste. Il reste alors 18 euros. Retrouver le budget et les trois sommes utilisées.",
['Exprimer chaque reste comme fraction du budget initial.',r'Le reste final représente $\frac23\times\frac34\times\frac25$ du budget.'],
r'''\editionEtape{Suivre les restes}Après la première utilisation, il reste $\frac23$ du budget. Après la deuxième, il reste $\frac34\times\frac23=\frac12$ du budget. La troisième conserve $\frac25$ de ce montant, soit $\frac25\times\frac12=\frac15$ du budget initial.
\editionEtape{Revenir au total}Un cinquième du budget vaut 18 euros, donc le budget est $\res{90}$ euros.
\editionEtape{Calculer les parts}Le tiers initial vaut 30 euros. Il reste 60 euros ; leur quart vaut 15 euros. Il reste 45 euros ; leurs trois cinquièmes valent 27 euros. Contrôle : $30+15+27+18=90$. Les fractions successives ne portaient pas sur le même total.''',
"assert (1-Rational(1,3))*(1-Rational(1,4))*(1-Rational(3,5))==Rational(1,5) and 30+15+27+18==90"),
Defi('Jusqu’où peut-on doubler ?',r"Une mémoire fictive contient au départ un seul élément. À chaque étape, le nombre d’éléments double. Sa capacité maximale est d’un million d’éléments. Quel est le plus grand nombre d’étapes possible ? Donner un encadrement d’un million par deux puissances de 2 consécutives.",
['Après $n$ étapes, combien de facteurs 2 a-t-on introduits ?','Calculer $2^{10}$, puis comparer $2^{19}$ et $2^{20}$ à un million.'],
r'''\editionEtape{Modéliser}Au départ, il y a 1 élément. Après $n$ étapes, il y en a $2^n$ : chaque étape ajoute un facteur 2.
\editionEtape{Encadrer la capacité}$2^{10}=1\,024$, donc $2^{20}=2^{10}\times2^{10}=1\,048\,576$ et $2^{19}=524\,288$. Ainsi $\res{2^{19}<1\,000\,000<2^{20}}$.
\editionEtape{Conclure}On peut effectuer $\res{19}$ étapes complètes ; une vingtième dépasserait la capacité. La valeur de départ ne compte pas comme une étape de doublement.''',
"assert 2**10==1024 and 2**10*2**10==2**20 and 2**19==524288<1000000<2**20==1048576"),
Defi('Racine de deux, un nombre non décimal',r"Le carré construit sur la diagonale d’un carré de côté 1 a une aire égale à 2 : cette diagonale mesure $\sqrt2$. On veut démontrer par l’absurde que $\sqrt2$ n’est pas un nombre décimal."+r"\begin{questions}\item Montrer que $\sqrt2$ n’est pas un nombre entier.\item On suppose que $\sqrt2$ s’écrit avec un nombre fini de chiffres après la virgule, le dernier étant un chiffre $c$ non nul. Quel peut être le dernier chiffre de son carré ?\item Conclure.\end{questions}",
['Encadrer $\\sqrt2$ entre deux entiers consécutifs grâce à $1^2$ et $2^2$.','Écrire les carrés de 1 à 9 et regarder leur chiffre des unités.'],
r'''\editionEtape{1 · Pas un entier}$1^2=1<2<4=2^2$, donc $1<\sqrt2<2$ : aucun entier ne convient.
\editionEtape{2 · Le dernier chiffre}Supposons que $\sqrt2=d$, avec $k\ge1$ chiffres après la virgule, le dernier étant $c$, entre 1 et 9. Alors $d^2$ a $2k$ chiffres après la virgule, et son dernier chiffre est celui de $c^2$. Or les carrés de 1 à 9 se terminent par 1, 4, 9, 6, 5, 6, 9, 4 et 1 : $\res{\text{jamais par 0}}$. Le nombre $d^2$ n’est donc pas entier.
\editionEtape{3 · La contradiction}Pourtant $d^2=2$ est un entier : c’est absurde. L’hypothèse est fausse : $\res{\sqrt2\text{ n’est pas décimal}}$. Par exemple, $1{,}41^2=1{,}9881$ et $1{,}42^2=2{,}0164$ encadrent 2 sans l’atteindre.''',
"assert [c*c%10 for c in range(1,10)]==[1,4,9,6,5,6,9,4,1] and 0 not in [c*c%10 for c in range(1,10)] and Rational('1.41')**2<2<Rational('1.42')**2",'defi-racine'),
Defi('Comparer sans choisir de valeur',r"Pour $x>0$, un rectangle A mesure 3 cm sur $x+4$ cm. Un rectangle B mesure 2 cm sur $x+6$ cm. Quelle aire est la plus grande ? Est-il possible qu’elles soient égales pour une longueur $x$ strictement positive ?",
['Développer les deux expressions d’aire.','Calculer l’aire de A moins celle de B.'],
r'''\editionEtape{Écrire les aires}$A=3(x+4)=3x+12$ et $B=2(x+6)=2x+12$, en cm$^2$.
\editionEtape{Comparer en général}$A-B=(3x+12)-(2x+12)=x$. Puisque $x>0$, cette différence est positive : $\res{A>B}$ pour toutes les longueurs admises.
\editionEtape{Étudier l’égalité}L’égalité des aires imposerait $x=0$, exclu par l’énoncé. Tester plusieurs nombres n’aurait pas prouvé la conclusion pour tous les nombres positifs ; la différence littérale le permet.''',
"assert expand(3*(x+4)-2*(x+6))==x",'defi-litteral'),
Defi('Compter les pièces',r"Une boîte contient 42 pièces, uniquement de 1 euro et de 2 euros. Leur valeur totale est 68 euros. Trouver le nombre de pièces de chaque sorte et vérifier les deux contraintes.",
['Appeler $x$ le nombre de pièces de 2 euros.','Il reste alors $42-x$ pièces de 1 euro.'],
r'''\editionEtape{Choisir une inconnue}Si $x$ est le nombre de pièces de 2 euros, il y a $42-x$ pièces de 1 euro. Leur valeur totale vaut $2x+(42-x)$.
\editionEtape{Résoudre}L’équation $2x+42-x=68$ se réduit en $x+42=68$, donc $\res{x=26}$. Il y a $\res{16}$ pièces de 1 euro.
\editionEtape{Vérifier le contexte}Les nombres sont entiers et positifs. On compte $26+16=42$ pièces et $2\times26+16=68$ euros. Contrôler seulement la somme d’argent n’aurait pas vérifié le nombre de pièces.''',
"assert solve(2*x+(42-x)-68,x)==[26] and 26+16==42 and 2*26+16==68"),
Defi('Partager un bénéfice',r"Trois associés ont investi 12 000 €, 18 000 € et 30 000 €. Le bénéfice de 9 000 € est partagé proportionnellement aux sommes investies."+r"\begin{questions}\item Écrire le ratio des investissements sous forme simplifiée et calculer les trois parts.\item L’année suivante, le troisième associé a retiré 10 000 €. Le bénéfice, de 10 000 €, est partagé de la même manière. Calculer les nouvelles parts.\item Quel associé voit sa part augmenter le plus ?\end{questions}",
['Diviser les trois sommes investies par 6 000.','La première année, le bénéfice se partage en $2+3+5=10$ parts.'],
r'''\editionEtape{1 · Première année}$12\,000:18\,000:30\,000=2:3:5$. Une part vaut $9\,000:10=900$ € : les parts sont $\res{1\,800}$ €, $\res{2\,700}$ € et $\res{4\,500}$ €.
\editionEtape{2 · Deuxième année}$12\,000:18\,000:20\,000=6:9:10$, soit 25 parts. Une part vaut $10\,000:25=400$ € : $\res{2\,400}$ €, $\res{3\,600}$ € et $\res{4\,000}$ €.
\editionEtape{3 · Comparer}Les variations sont $+600$ €, $+900$ € et $-500$ € : le $\res{\text{deuxième associé}}$ gagne le plus. Le troisième reçoit moins malgré un bénéfice total plus grand, car sa part du capital a diminué.''',
"assert Rational(9000,10)==900 and [900*k for k in (2,3,5)]==[1800,2700,4500] and [400*k for k in (6,9,10)]==[2400,3600,4000] and 3600-2700==900"),
Defi('Annuler une remise',r"Un prix baisse de 20\,\%. De quel pourcentage faut-il augmenter le nouveau prix pour retrouver l’ancien ? Prouver que ce pourcentage ne dépend pas du prix initial.",
[r'Une baisse de 20\,\% correspond au coefficient multiplicateur 0,8.',r'Chercher le coefficient $k$ tel que $0{,}8\times k=1$.'],
r'''\editionEtape{Coefficients}Baisser de 20\,\% revient à multiplier par 0,8. Pour revenir au prix $P$, il faut multiplier le nouveau prix par un nombre $k$ tel que $0{,}8\times k=1$, soit $k=\frac1{0{,}8}=1{,}25$ : c’est une hausse de $\res{25\,\%}$.
\editionEtape{Généraliser}Pour tout prix $P>0$ : $P\times0{,}8\times1{,}25=P\times1=P$. Le résultat ne dépend pas de $P$.
\editionEtape{Éviter le piège}Une hausse de 20\,\% donnerait $P\times0{,}8\times1{,}2=0{,}96P$ : il manquerait 4\,\% du prix. Les deux pourcentages ne portent pas sur la même base.''',
"assert 1/Rational('0.8')==Rational('1.25') and Rational('0.8')*Rational('1.2')==Rational('0.96')"),
Defi('Un découpage variable',r"Dans un rectangle de 18 cm sur 10 cm, on retire quatre carrés de côté $x$ cm aux coins, avec $0<x<5$. Donner la formule de l’aire restante $A(x)$. Parmi $x=2$, 3 et 4, lequel laisse 116 cm$^2$ ? Peut-on retrouver ce choix sans tester les trois valeurs ?",
['L’aire retirée est $4x^2$.','Si l’aire restante est 116, chaque carré retiré a une aire de 16.'],
r'''\editionEtape{Établir la formule}L’aire initiale est 180 cm$^2$, donc $\res{A(x)=180-4x^2}$.
\editionEtape{Calculer les trois cas}$A(2)=164$, $A(3)=144$ et $A(4)=\res{116}$ cm$^2$. Le choix est $x=4$ cm.
\editionEtape{Retrouver directement}Retirer $180-116=64$ cm$^2$ en quatre carrés identiques donne 16 cm$^2$ par carré. Le côté positif vaut $\sqrt{16}=4$ cm, et la contrainte $0<x<5$ est respectée.''',
"assert [180-4*a*a for a in [2,3,4]]==[164,144,116] and sqrt(Rational(180-116,4))==4",'coins-retires'),
Defi('Même moyenne, autre médiane',r"Comparer les séries A : 4, 4, 4, 16, 16, 16 et B : 0, 8, 8, 8, 8, 28. Calculer la moyenne, une médiane et l’étendue de chacune. Que peut-on conclure sur l’information fournie par une moyenne seule ?",
['Les deux sommes valent 60.','Avec six valeurs, observer les valeurs de rangs 3 et 4.'],
r'''\editionEtape{Moyennes}Les sommes valent 60 et les effectifs 6 : les deux moyennes valent $\res{10}$.
\editionEtape{Médianes et étendues}Pour A, les valeurs centrales sont 4 et 16 : toute valeur entre 4 et 16 est une médiane, par exemple 10 ; l’étendue vaut 12. Pour B, les valeurs centrales valent 8 : la médiane est $\res8$ et l’étendue vaut 28.
\editionEtape{Interpréter}Une même moyenne n’impose ni la même médiane ni la même dispersion. La valeur 28 compense les petites valeurs de B dans la somme. Pour décrire une série, on précise l’indicateur utilisé sans lui faire dire davantage que ce qu’il mesure.''',
"assert sum([4,4,4,16,16,16])==sum([0,8,8,8,8,28])==60 and Rational(4+16,2)==10 and 16-4==12 and 28-0==28"),
Defi('Un jeu de dés équitable ?',r"On lance un dé rouge et un dé bleu, équilibrés. Léa gagne si le produit des deux nombres est pair ; sinon, c’est Hugo qui gagne."+r"\begin{questions}\item Le jeu est-il équitable ?\item On change la règle : Léa gagne si la somme des deux nombres est paire. Le jeu devient-il équitable ?\end{questions}",
['Construire le tableau des 36 issues et marquer celles qui font gagner Léa.','Un produit est impair seulement si les deux nombres sont impairs : utiliser l’événement contraire.'],
r'''\editionEtape{1 · Produit pair}Les 36 issues sont équiprobables. Le produit est impair seulement si les deux nombres sont impairs : $3\times3=9$ issues. Donc $P(\text{Léa gagne})=1-\frac9{36}=\res{\frac34}$ : le jeu $\res{\text{n’est pas équitable}}$, il avantage Léa.
\editionEtape{2 · Somme paire}La somme est paire si les deux nombres sont pairs ($9$ issues) ou tous deux impairs ($9$ issues) : $P=\frac{18}{36}=\res{\frac12}$. Le jeu devient $\res{\text{équitable}}$.
\editionEtape{Contrôle}Le tableau corrigé colore les issues gagnantes pour Léa avec la première règle : on en compte 27, soit bien $\frac{27}{36}=\frac34$.''',
"I=[(a,b) for a in range(1,7) for b in range(1,7)]; assert len([1 for a,b in I if a*b%2==0])==27 and len([1 for a,b in I if (a+b)%2==0])==18",'defi-des'),
Defi('Six triangles de même aire',r"Dans le triangle ABC, I, J et K sont les milieux de $[BC]$, $[CA]$ et $[AB]$. Les médianes $(AI)$, $(BJ)$ et $(CK)$ se coupent en G. Elles découpent le triangle en six petits triangles. Démontrer que ces six triangles ont la même aire.",
['Noter $a$, $b$ et $c$ les aires de GBI, GCJ et GAK : $[GI]$, $[GJ]$ et $[GK]$ sont des médianes de petits triangles.','La médiane $[AI]$ partage ABC en deux parties de même aire.'],
r'''\editionEtape{Des paires égales}Dans le triangle GBC, $[GI]$ est une médiane : GBI et GIC ont la même aire $a$. De même, GCJ et GJA ont la même aire $b$, et GAK et GKB la même aire $c$.
\editionEtape{Utiliser les grandes médianes}La médiane $[AI]$ partage ABC en ABI et AIC, de même aire : $c+c+a=a+b+b$, donc $c=b$. La médiane $[BJ]$ donne de même $a+a+b=b+c+c$, donc $a=c$.
\editionEtape{Conclure}Ainsi $\res{a=b=c}$ : les six petits triangles ont la même aire, égale au sixième de celle de ABC. Seule la propriété de la médiane, vue en Cinquième, a été utilisée.''',
"a,b,c=S('a'),S('b'),S('c'); assert solve([2*c+a-(a+2*b),2*a+b-(b+2*c)],[a,b],dict=True)==[{a:c,b:c}]",'defi-medianes'),
Defi('Le pont le plus court',r"Une rivière a deux rives parallèles distantes de 1 km. Dans un repère d’unité 1 km, les rives sont les droites d’équations $y=2$ et $y=3$. Le village A est en $(0\,;0)$ et le village B en $(6\,;5)$. On construit un pont MN perpendiculaire aux rives, avec M sur la rive $y=2$. Où placer M pour que le trajet $AM+MN+NB$ soit le plus court ?",
['Faire glisser B vers la rivière, perpendiculairement aux rives, d’une longueur égale à la largeur de la rivière.','Dans le parallélogramme MNBB’, comparer NB et MB’, puis chercher le plus court chemin de A à B’.'],
r'''\editionEtape{Utiliser une translation}La translation qui transforme N en M transforme B en $B'(6\,;4)$. Le quadrilatère MNBB’ est un parallélogramme, donc $NB=MB'$. Le trajet vaut $AM+MB'+1$, car $MN=1$ km.
\editionEtape{Le plus court chemin}$AM+MB'$ est minimal quand M est sur le segment $[AB']$. La droite $(AB')$ passe par les points $(3\,;2)$ et $(6\,;4)$ : M est le point $\res{(3\,;2)}$ de la rive.
\editionEtape{La longueur}$AB'=\sqrt{6^2+4^2}=\sqrt{52}$ km, d’après le théorème de Pythagore. Le trajet minimal vaut $\res{\sqrt{52}+1\approx8{,}21\ \mathrm{km}}$. La translation a transformé le problème en une ligne droite.''',
"assert Rational(4,6)*3==2 and round(float(sqrt(52)+1),2)==8.21",'defi-pont'),
Defi('Varignon et les aires',r"ABCD est un quadrilatère non croisé dont les diagonales se coupent à l’intérieur. I, J, K et L sont les milieux de $[AB]$, $[BC]$, $[CD]$ et $[DA]$. On sait que IJKL est un parallélogramme : c’est le théorème du mathématicien français Pierre Varignon. Démontrer que son aire est la moitié de celle de ABCD.",
['Dans le triangle ABD, comparer les aires de AID et ABD, puis de AIL et AID.','Les quatre triangles des coins représentent ensemble la moitié de l’aire de ABCD.'],
r'''\editionEtape{Un coin}Dans ABD, $[DI]$ est une médiane : $\mathcal A(AID)=\frac12\mathcal A(ABD)$. Dans AID, $[IL]$ est une médiane : $\mathcal A(AIL)=\frac12\mathcal A(AID)=\frac14\mathcal A(ABD)$. De même, $\mathcal A(CKJ)=\frac14\mathcal A(CDB)$.
\editionEtape{Les quatre coins}Les coins A et C totalisent $\frac14\left[\mathcal A(ABD)+\mathcal A(CDB)\right]=\frac14\mathcal A(ABCD)$. De même, les coins B et D totalisent $\frac14\mathcal A(ABCD)$.
\editionEtape{Conclure}Le parallélogramme est ce qui reste : $\mathcal A(IJKL)=\mathcal A(ABCD)-\frac12\mathcal A(ABCD)=\res{\frac12\mathcal A(ABCD)}$. Le résultat ne dépend pas de la forme du quadrilatère.''',
"P=[(0,0),(9,-1),(10,5),(1,6)]; ar=lambda Q:Rational(abs(sum(Q[i][0]*Q[(i+1)%len(Q)][1]-Q[(i+1)%len(Q)][0]*Q[i][1] for i in range(len(Q)))),2); M=[(Rational(P[i][0]+P[(i+1)%4][0],2),Rational(P[i][1]+P[(i+1)%4][1],2)) for i in range(4)]; assert ar(P)==55 and 2*ar(M)==ar(P)",'defi-varignon'),
Defi('Le câble et ses attaches',r"Un câble doit suivre l’hypoténuse d’un triangle rectangle dont les côtés de l’angle droit mesurent 9 m et 12 m. Il faut en plus 0,75 m à chaque extrémité pour les attaches. Le câble coûte 4,80 euros le mètre. Calculer la longueur et le coût exacts.",
['Calculer d’abord la distance entre les points d’attache.','Deux extrémités demandent deux réserves de 0,75 m.'],
r'''\editionEtape{Distance à franchir}D’après le théorème de Pythagore, $d^2=9^2+12^2=225$, donc $d=15$ m.
\editionEtape{Ajouter les réserves}La longueur totale est $15+2\times0{,}75=\res{16{,}5\ \mathrm m}$. La réserve n’est pas un côté du triangle et n’entre pas sous la racine.
\editionEtape{Calculer le coût}$16{,}5\times4{,}80=\res{79{,}20}$ euros. On suppose que le câble peut être acheté au dixième de mètre, sans supplément.''',
"assert sqrt(9**2+12**2)+2*Rational('.75')==Rational('16.5') and Rational('16.5')*Rational('4.8')==Rational('79.2')",'defi-pyth'),
Defi('Le plus grand triangle du demi-cercle',r"$[AB]$ est un diamètre de 10 cm d’un cercle de centre O, et M un point du cercle distinct de A et B."+r"\begin{questions}\item Démontrer que $AM^2+BM^2=100$, quelle que soit la position de M.\item Démontrer que l’aire du triangle AMB est au plus égale à 25 cm$^2$. Pour quelle position de M est-elle égale à 25 cm$^2$ ?\end{questions}",
['Le triangle AMB est rectangle en M.','La hauteur issue de M est au plus égale au rayon OM.'],
r'''\editionEtape{1 · Une somme constante}M est sur le cercle de diamètre $[AB]$ : le triangle AMB est rectangle en M. Le théorème de Pythagore donne $\res{AM^2+BM^2=AB^2=100}$.
\editionEtape{2 · Majorer l’aire}Soit H le pied de la hauteur issue de M. Dans le triangle MHO, rectangle en H, l’hypoténuse $[OM]$ est le plus long côté : $MH\le OM=5$ cm. L’aire vaut $\frac{AB\times MH}2\le\frac{10\times5}2=\res{25\ \mathrm{cm}^2}$.
\editionEtape{Le cas d’égalité}L’aire vaut 25 cm$^2$ lorsque $H=O$, c’est-à-dire lorsque $(OM)\perp(AB)$ : M est alors à égale distance de A et B, et $AM=BM=\sqrt{50}$ cm.''',
"assert 2*50==100 and Rational(10*5,2)==25",'defi-cercle'),
Defi('Une pyramide de verre',r"On modélise la pyramide du Louvre par une pyramide régulière à base carrée de 35 m de côté et de 21 m de hauteur, valeurs arrondies. O est le centre de la base et M le milieu d’un côté de la base."+r"\begin{questions}\item Calculer le volume de cette pyramide.\item Calculer SM, la hauteur d’une face triangulaire, au centième de mètre.\item En déduire l’aire des quatre faces vitrées, au mètre carré près.\end{questions}",
['Le volume d’une pyramide est le tiers du produit de l’aire de la base par la hauteur.','Le triangle SOM est rectangle en O et $OM$ vaut la moitié du côté de la base.'],
r'''\editionEtape{1 · Volume}$V=\frac{35^2\times21}3=\frac{1\,225\times21}3=\res{8\,575\ \mathrm m^3}$.
\editionEtape{2 · Hauteur d’une face}Dans le triangle SOM rectangle en O : $SO=21$ m et $OM=17{,}5$ m. Pythagore donne $SM^2=441+306{,}25=747{,}25$, donc $SM\approx\res{27{,}34\ \mathrm m}$.
\editionEtape{3 · Surface vitrée}Chaque face a pour aire $\frac{35\times SM}2$. Les quatre faces totalisent $70\times SM\approx\res{1\,914\ \mathrm m^2}$, avec la valeur non arrondie de SM. Le modèle ignore l’épaisseur des montants.''',
"assert Rational(35**2*21,3)==8575 and round(float(sqrt(Rational('747.25'))),2)==27.34 and round(float(70*sqrt(Rational('747.25'))))==1914",'defi-pyramide'),
Defi('La suite de Syracuse',r"Le script demande un entier n puis répète 16 fois : si le reste de n divisé par 2 vaut 0, mettre n à n divisé par 2 ; sinon, mettre n à $3\times n+1$ ; dire n."+r"\begin{questions}\item Donner les seize valeurs dites pour l’entrée 7.\item À quel tour obtient-on 1 pour la première fois ? Que se passerait-il si l’on continuait ?\item Le script n’utilise qu’une variable. Expliquer pourquoi c’est suffisant.\end{questions}",
['Écrire n après chaque tour dans un tableau.','Après 1, on obtient 4, puis 2, puis 1.'],
r'''\editionEtape{1 · Les valeurs}Pour 7 : $\res{22,\ 11,\ 34,\ 17,\ 52,\ 26,\ 13,\ 40,\ 20,\ 10,\ 5,\ 16,\ 8,\ 4,\ 2,\ 1}$. Chaque valeur ne dépend que de la précédente.
\editionEtape{2 · Le retour à 1}On obtient 1 au $\res{16^\text{e}}$ tour. Ensuite, on obtiendrait 4, 2, 1, puis de nouveau 4, 2, 1 : la suite devient périodique. Personne n’a encore démontré qu’on atteint 1 pour tout entier de départ.
\editionEtape{3 · Une seule variable}Chaque instruction remplace n par une nouvelle valeur calculée à partir de l’ancienne ; on n’a pas besoin de garder les valeurs précédentes. En Troisième, une boucle « répéter jusqu’à n = 1 » permettra de s’arrêter au bon moment.''',
"from donnees_scripts import SCRIPTS,executer; assert executer(SCRIPTS['defi-syracuse'],[7])[1]==[22,11,34,17,52,26,13,40,20,10,5,16,8,4,2,1]",'defi-script')
]
