"""Rédaction des six chapitres attribués ; sources conservées séparément."""
from pathlib import Path
from fractions import Fraction
import json, re

BASE=Path(__file__).resolve().parent.parent
CODES=[2,3,4,5,10,19]
DATA={c:[] for c in CODES}

def fr(v):
    v=Fraction(str(v))
    if v.denominator==1:return f'{v.numerator:,}'.replace(',',r'\,')
    s=f'{float(v):.2f}'.rstrip('0').rstrip('.')
    return s.replace('.',r'{,}')

def tex(expr):
    return re.sub(r'\d+(?:\.\d+)?',lambda m:fr(m[0]),expr).replace('*',r'\times ').replace('/',r'\div ')

def calc(expr):
    # Expressions écrites exclusivement dans ce script, sans entrée externe.
    return eval(re.sub(r'\d+(?:\.\d+)?',lambda m:'Fraction('+repr(m[0])+')',expr),{'Fraction':Fraction})

def Q(question,reason,chain,answer,method='Choisir les informations utiles et procéder dans l’ordre.'):
    return {'question':question,'methode':method,'raison':reason,'calcul':chain,'reponse':answer}

def C(expr,reason,question=None,unit=''):
    val=calc(expr); form=tex(expr)+'='+fr(val)
    return Q(question or ('Calculer $'+tex(expr)+'$.'),reason,form,'$'+fr(val)+'$'+(' '+unit if unit else ''),'Décomposer le calcul ou utiliser les rangs de numération.')

def E(c,title,context,qs,figure=None):
    assert len(qs)>=5,(c,title)
    DATA[c].append({'titre':title,'contexte':context,'questions':qs,'figure':figure})

COURSES={
2:r'''::: objectifs
- Comprendre une somme, une différence, un ajout, un retrait et une comparaison.
- Choisir entre calcul mental et opération posée, puis contrôler le résultat.
- Résoudre un problème en deux ou trois étapes avec un schéma en barres.
:::

## I. Comprendre ce que l’on cherche
::: definition Deux opérations
Une **addition** réunit des quantités ou traduit un ajout. Son résultat est une **somme**. Une **soustraction** cherche un reste, un écart ou une partie manquante. Son résultat est une **différence**.
:::
::: exemple Le tout et les parties
Une école accueille 258 élèves, dont 136 filles. Les filles et les garçons forment ensemble le tout. Pour trouver la partie manquante, on calcule $258-136=122$ : il y a 122 garçons.
:::
[IMAGE_1]
::: attention Le sens avant les mots
« Nina a 68 cartes de plus que Marco » ne demande pas toujours une addition. Si Nina en a 325, Marco en a moins : $325-68=257$. Reformuler l’histoire avant de choisir l’opération.
:::

## II. Poser une addition
::: methode Calculer rang par rang
1. Écrire les unités sous les unités, puis aligner les autres rangs.
2. Commencer par les unités.
3. Chaque fois que l’on atteint dix unités d’un rang, les échanger contre une unité du rang suivant : c’est la retenue.
4. Continuer vers les dizaines, les centaines et les milliers.
:::
::: exemple Une retenue qui se propage
Pour $6\,478+525$, les unités donnent $8+5=13$ : écrire 3 et retenir une dizaine. Les dizaines donnent $7+2+1=10$ : écrire 0 et retenir une centaine. Les centaines donnent $4+5+1=10$. Les milliers donnent $6+1=7$. Ainsi $6\,478+525=7\,003$.
:::

## III. Poser une soustraction et vérifier
::: methode Effectuer les échanges
Aligner les rangs et commencer par les unités. Si un rang ne contient pas assez d’unités, échanger une unité du rang supérieur contre dix unités du rang courant. Écrire les échanges pour ne pas les oublier.
:::
::: exemple Franchir un zéro
Pour $5\,204-1\,368$, on échange une centaine contre dix dizaines, puis une dizaine contre dix unités. Les rangs du premier nombre deviennent 5 milliers, 1 centaine, 9 dizaines et 14 unités. Après un nouvel échange entre milliers et centaines, on obtient $3\,836$. Contrôle : $3\,836+1\,368=5\,204$.
:::
::: attention
On ne soustrait pas systématiquement le petit chiffre du grand : l’ordre des deux nombres doit être respecté.
:::

## IV. Calculer de tête, estimer et résoudre
::: methode Chercher des nombres ronds
Pour ajouter 19, ajouter 20 puis retirer 1 : $457+19=457+20-1=476$. Pour retirer 398, retirer 400 puis ajouter 2 : $757-398=757-400+2=359$. On peut aussi regrouper les termes d’une somme : $254+378+46=300+378=678$.
:::
::: methode Du problème à la réponse
Comprendre l’histoire ; représenter le tout et les parties ; calculer une étape à la fois ; répondre avec l’unité. Un théâtre possède 850 places et vend 512 puis 218 billets. Les ventes font $512+218=730$ billets ; il reste $850-730=120$ places. Le contrôle $730+120=850$ retrouve le tout.
:::
::: retenir
Estimer avant de calculer : $6\,478+525$ est proche de $6\,500+500=7\,000$. Vérifier une différence en additionnant la partie retirée et le reste. Une estimation contrôle l’ordre de grandeur ; elle ne remplace pas le résultat exact.
:::
''',
3:r'''::: objectifs
- Comprendre la multiplication comme le comptage de groupes égaux.
- Utiliser les tables, les doubles et la décomposition d’un facteur.
- Poser un produit d’entiers et résoudre des problèmes de dénombrement.
:::

## I. Compter des groupes égaux
::: definition Produit et facteurs
Le **produit** est le résultat d’une multiplication. Les nombres multipliés sont les **facteurs**. Quatre groupes de 45 objets contiennent $4\times45=180$ objets. L’addition $45+45+45+45$ traduit la même situation.
:::
[IMAGE_1]
::: propriete Changer l’ordre ou regrouper
Changer l’ordre des facteurs ne change pas le produit : $7\times8=8\times7=56$. On peut aussi regrouper : $4\times25\times6=100\times6=600$. Cela aide à calculer de tête.
:::
::: attention Comparer deux quantités
« Trois fois autant » signifie trois groupes de la quantité de départ. Avec 8 250 spectateurs le samedi, trois fois autant le dimanche donne $8\,250\times3=24\,750$, et non $8\,250+3$.
:::

## II. Des chemins de calcul mental
::: methode Utiliser la numération
Pour multiplier un entier par 10, 100 ou 1 000, chaque chiffre prend une valeur 10, 100 ou 1 000 fois plus grande. Il monte d’un, deux ou trois rangs. Ainsi $358\times100=35\,800$. Cette explication concerne ici les nombres entiers.
:::
::: methode Doubler ou prendre une moitié
Multiplier par 4 revient à doubler deux fois : $35\times2=70$, puis $70\times2=140$. Multiplier par 8 revient à doubler trois fois. Pour multiplier par 5, multiplier par 10 puis prendre la moitié : $68\times10=680$, puis $680\div2=340$.
:::
::: propriete Décomposer un facteur
On peut distribuer une multiplication sur une somme :
$$\begin{aligned}
23\times12&=23\times(10+2)\\
&=230+46\\
&=276.
\end{aligned}$$
Chaque produit partiel compte une partie des groupes ; il faut ensuite les additionner.
:::

## III. Poser une multiplication
::: methode Un multiplicateur à un chiffre
Multiplier successivement les unités, les dizaines, les centaines. Reporter les retenues. Pour $486\times7$, les unités donnent $6\times7=42$, les dizaines $8\times7+4=60$, les centaines $4\times7+6=34$. Le résultat est $3\,402$.
:::
::: methode Un multiplicateur à deux chiffres
Pour $347\times26$, séparer $26=20+6$. Calculer $347\times6=2\,082$, puis $347\times20=6\,940$. Additionner : $2\,082+6\,940=9\,022$. La ligne des dizaines représente vingt groupes, pas deux groupes.
:::
::: attention
Écrire clairement la retenue et la valeur de chaque ligne. Dans $40\times70$, il y a $4\times7=28$ centaines, donc $2\,800$.
:::

## IV. Choisir un calcul et contrôler
::: exemple Fauteuils d’une salle
Une salle de 32 rangées de 28 fauteuils possède $32\times28=896$ places. Si 850 billets sont vendus, il reste $896-850=46$ places. On calcule d’abord la capacité, puis la différence.
:::
::: exemple Des choix à combiner
Avec 3 entrées et 4 plats, chaque entrée peut accompagner chacun des 4 plats : $3\times4=12$ menus. Si chaque menu accepte 2 desserts, il y a $12\times2=24$ menus complets. Une liste organisée évite les oublis et les doublons.
:::
::: retenir
Avant de poser, estimer : $486\times7$ est proche de $500\times7=3\,500$. Un produit de groupes égaux peut se contrôler par addition ou par décomposition. Terminer un problème avec une phrase et une unité.
:::
''',
4:r'''::: objectifs
- Distinguer partager équitablement et former des groupes de taille donnée.
- Trouver un quotient entier et un reste avec un diviseur à un chiffre.
- Utiliser les multiples et interpréter le reste selon la question.
:::

## I. Donner du sens à une division
::: definition Deux questions de partage
Partager 24 objets entre 4 enfants consiste à chercher la taille de chaque part. Former des paquets de 4 avec 24 objets consiste à chercher le nombre de paquets. Dans les deux cas, $24\div4=6$, mais le nombre 6 ne désigne pas la même chose.
:::
[IMAGE_1]
::: definition Division euclidienne
Diviser un nombre entier par un entier non nul, c’est chercher un **quotient entier** et un **reste**. Le reste est positif ou nul et strictement inférieur au diviseur. Par exemple :
$$87=4\times21+3\qquad\text{avec }3<4.$$
Le quotient est 21 et le reste est 3. Il reste trop peu d’objets pour constituer un nouveau groupe complet.
:::

## II. Utiliser les multiples et les diviseurs
::: definition Un partage qui tombe juste
Un multiple de 8 s’obtient en multipliant 8 par un entier : 0, 8, 16, 24, etc. Si le reste de la division de 91 par 7 est nul, 7 est un **diviseur** de 91 : $7\times13=91$.
:::
::: methode Des reconnaissances rapides
- Un entier est multiple de 2 si son chiffre des unités est 0, 2, 4, 6 ou 8 : il est pair.
- Un entier est multiple de 5 s’il se termine par 0 ou 5.
- Un entier est multiple de 10 s’il se termine par 0.
Pour un autre petit diviseur, utiliser les tables, une multiplication ou une division.
:::
::: exemple Encadrer par deux multiples consécutifs
Comme $7\times7=49$ et $7\times8=56$, on a $49<50<56$. Sept groupes de 7 sont possibles ; huit groupes demanderaient trop d’objets. Ainsi $50=7\times7+1$.
:::

## III. Poser la division
::: methode De gauche à droite
1. Prendre les premiers chiffres qui permettent de partager.
2. Chercher combien de fois le diviseur entre dans cette quantité.
3. Multiplier, soustraire, puis abaisser le chiffre suivant.
4. Écrire un chiffre du quotient à chaque nouveau rang, même si c’est zéro.
5. Contrôler l’égalité et la taille du reste.
:::
::: exemple Le zéro dans le quotient
Pour diviser 1 258 par 6 : dans 12 centaines, on place 2 centaines au quotient et il ne reste rien ; après avoir abaissé 5 dizaines, on place 0 dizaine ; on abaisse 8 unités et on partage 58 unités en 9 groupes avec 4 unités restantes. Donc $1\,258=6\times209+4$, et $4<6$.
:::
::: attention Deux conditions à vérifier
$74=8\times8+10$ est une égalité exacte, mais le reste 10 est trop grand. On forme encore un paquet de 8 : $74=8\times9+2$, avec $2<8$.
:::

## IV. Répondre à la question du problème
::: exemple Des boîtes d’œufs
Avec 230 œufs et des boîtes de 6, $230=6\times38+2$. On remplit 38 boîtes complètes. Pour emporter tous les œufs, il faut une boîte supplémentaire, donc 39 boîtes. Les deux réponses correspondent à deux questions différentes.
:::
::: retenir
Nommer ce que représente le quotient ; exprimer le reste dans la bonne unité. Ne pas écrire une égalité de division ordinaire quand il reste des objets : utiliser « quotient…, reste… » ou l’égalité de contrôle. Une moitié partage en 2, un quart partage en 4.
:::
''',
5:r'''::: objectifs
- Comprendre le signe égal et chercher un nombre inconnu.
- Exécuter un programme dans l’ordre et remonter ses instructions.
- Reconnaître une régularité dans une suite de nombres ou de motifs.
:::

## I. Une égalité compare deux valeurs
::: definition Même valeur des deux côtés
Le signe $=$ signifie « a la même valeur que ». Il peut relier deux calculs : $8+6=9+5$, car chaque côté vaut 14. Il ne signifie pas simplement « écrire la réponse ».
:::
::: methode Tester une égalité
Calculer séparément les deux côtés, puis comparer. Pour $7\times4=30-3$, on obtient 28 à gauche et 27 à droite : l’égalité est fausse. On peut la corriger en écrivant $7\times4=30-2$.
:::
::: attention
Une chaîne d’égalités doit garder la même valeur à chaque signe égal. Pour un programme en deux étapes, écrire les deux calculs séparément si les valeurs intermédiaires changent.
:::

## II. Trouver un nombre caché
::: methode Défaire une opération
Dans $47+\square=92$, chercher la partie manquante : $92-47=45$. Dans $\square-28=35$, retrouver le nombre initial : $35+28=63$. Dans $7\times\square=84$, chercher le nombre de groupes de 7 : $84\div7=12$. Toujours remplacer le symbole par la réponse pour contrôler.
:::
::: exemple Un même symbole, une même valeur
Si $\triangle+\triangle+5=19$, les deux triangles valent ensemble $19-5=14$, donc chaque triangle vaut $14\div2=7$. Si l’on sait aussi que $\triangle+\bullet=12$, alors le disque vaut $12-7=5$.
:::
::: notation Une lettre peut représenter un nombre
Un tee-shirt coûte 12 euros, et la livraison de toute la commande coûte 5 euros. Pour $N$ tee-shirts, le prix en euros s’écrit $(N\times12)+5$. La lettre $N$ représente le nombre de tee-shirts. Avec 4 tee-shirts : $(4\times12)+5=53$. La livraison n’est ajoutée qu’une fois.
:::

## III. Suivre et remonter un programme
::: methode Respecter l’ordre
Choisir un nombre, ajouter 2, puis multiplier le résultat par 4. Avec 6 : $6+2=8$, puis $8\times4=32$. Avec 10 : $10+2=12$, puis $12\times4=48$. Le second calcul utilise le résultat du premier.
:::
::: methode Retrouver le départ
Un programme multiplie par 3 puis retire 4. Pour obtenir 20, on remonte les instructions en sens inverse : $20+4=24$, puis $24\div3=8$. Vérifier en repartant de 8 : $8\times3=24$, puis $24-4=20$.
:::

## IV. Des suites et des motifs qui évoluent
::: methode Formuler une règle
Observer plusieurs passages, annoncer une règle, puis l’appliquer sans changer. Avec la règle « ajouter 7 », la suite 3 ; 10 ; 17 ; 24 continue par 31 puis 38. Une règle peut alterner deux instructions : ajouter 5, retirer 2, puis recommencer.
:::
::: exemple Une rangée de carrés
Le premier carré utilise 4 allumettes. Chaque nouveau carré partage un côté avec le précédent et ajoute 3 allumettes. Pour 5 carrés : $4+4\times3=16$ allumettes. Il y a quatre ajouts après le premier carré.
:::
[IMAGE_1]
::: attention Une règle doit être précisée
Quelques termes ne suffisent pas toujours à déterminer une règle unique. Dire « on poursuit avec la règle annoncée » permet de savoir quelle régularité on étudie.
:::
::: retenir
Contrôler une valeur inconnue en la remplaçant dans l’égalité. Pour remonter un programme, inverser à la fois les opérations et leur ordre. Dans un motif, compter les ajouts après l’étape initiale.
:::
''',
10:r'''::: objectifs
- Calculer avec des décimaux jusqu’aux centièmes en respectant les rangs.
- Poser additions, soustractions et produits par un entier inférieur à 10.
- Calculer mentalement avec 10 et résoudre des problèmes de monnaie ou de longueur.
:::

## I. Les mêmes rangs doivent se rencontrer
::: rappel Unités, dixièmes, centièmes
Une unité vaut 10 dixièmes ou 100 centièmes. On peut écrire $4{,}7=4{,}70$ : ajouter un zéro à droite de la partie décimale ne change pas le nombre. Ce zéro rend visible le rang des centièmes.
:::
::: methode Poser une addition ou une soustraction
Aligner les virgules, donc les unités sous les unités, les dixièmes sous les dixièmes et les centièmes sous les centièmes. Ajouter des zéros utiles, puis calculer à partir de la droite avec les retenues ou les échanges habituels. Placer la virgule du résultat sous les autres virgules.
:::
::: exemple
$4{,}70+2{,}85=7{,}55$. Pour $10-3{,}48$, écrire $10{,}00-3{,}48=6{,}52$. Contrôle : $6{,}52+3{,}48=10$.
:::
::: attention
Aligner seulement le dernier chiffre est incorrect si les nombres n’ont pas le même nombre de chiffres après la virgule. Dans $5{,}6+2{,}14$, écrire $5{,}60+2{,}14=7{,}74$.
:::

## II. Calculer de tête avec la numération
::: methode Ajouter des unités du même rang
Pour $5{,}34+2$, seules les unités changent : $7{,}34$. Pour $5{,}34+0{,}2$, on ajoute deux dixièmes : $5{,}54$. Pour $5{,}34+0{,}04$, on ajoute quatre centièmes : $5{,}38$.
:::
::: methode Multiplier ou diviser par 10
Multiplier par 10 rend chaque chiffre dix fois plus important : $3{,}7\times10=37$ et $0{,}85\times10=8{,}5$. Diviser par 10 rend chaque chiffre dix fois moins important : $45{,}2\div10=4{,}52$. Les chiffres changent de rang ; on complète avec un zéro si nécessaire.
:::
::: exemple Un complément à une unité
35 centièmes et 65 centièmes font 100 centièmes : $0{,}35+0{,}65=1$. Pour atteindre 10 à partir de $7{,}2$, il manque $10-7{,}2=2{,}8$.
:::

## III. Multiplier un décimal par un petit entier
::: methode Raisonner en dixièmes ou en centièmes
Pour $2{,}4\times3$, compter les dixièmes : $24\times3=72$ dixièmes, donc $7{,}2$. Pour $3{,}45\times6$, compter les centièmes : $345\times6=2\,070$ centièmes, donc $20{,}70$.
:::
::: methode Poser le produit
Effectuer le produit comme avec des entiers, puis conserver la valeur des rangs : si le nombre de départ est exprimé en centièmes, le produit obtenu compte encore des centièmes. Ici, on multiplie toujours par un entier de 1 à 9.
:::
::: attention
Un produit de nombres positifs par 6 ne peut pas être plus petit que le nombre de départ. Estimer permet de détecter une virgule mal placée : $3{,}45\times6$ est proche de $3{,}5\times6=21$.
:::

## IV. Résoudre et contrôler
::: exemple Une monnaie à rendre
Un achat coûte $7{,}45$ euros et on paie 10 euros. Aller d’abord à $7{,}50$, puis à 8, puis à 10 : $0{,}05+0{,}50+2=2{,}55$ euros. Contrôle : $7{,}45+2{,}55=10$.
:::
[IMAGE_1]
::: retenir
Lire l’histoire et conserver les unités. Estimer avant le calcul, puis contrôler une différence par une addition. Une somme de longueurs reste une longueur ; une somme de prix reste un prix.
:::
''',
19:r'''::: objectifs
- Reconnaître une situation de proportionnalité dans des grandeurs.
- Expliquer le lien « autant de fois plus » ou « autant de fois moins ».
- Calculer en langage naturel et repérer une situation qui ne suit pas cette règle.
:::

## I. Comprendre ce qui varie ensemble
::: definition Même multiplication des deux grandeurs
Une situation relève de la **proportionnalité** lorsque multiplier une quantité par un nombre multiplie l’autre quantité par le même nombre. Pour des cahiers identiques vendus au même prix, sans réduction ni frais fixes, trois fois autant de cahiers coûtent trois fois autant.
:::
::: exemple Une recette
Une recette pour 4 personnes utilise 250 g de riz. Pour 8 personnes, il y a deux fois autant de personnes : il faut deux fois autant de riz, soit $250\times2=500$ g. Pour 12 personnes, il y a trois fois autant de personnes : $250\times3=750$ g.
:::
[IMAGE_1]
::: attention Des conditions à lire
Le prix dépend aussi des conditions de vente. Un tarif avec abonnement, une réduction ou des frais fixes ne suit pas nécessairement la même règle. La taille d’un enfant n’est pas proportionnelle à son âge : deux fois plus âgé ne signifie pas deux fois plus grand.
:::

## II. Chercher « combien de fois »
::: methode Multiplier une quantité connue
1. Identifier les deux grandeurs et leurs unités.
2. Comparer la quantité demandée à la quantité connue.
3. Dire en une phrase combien de fois elle est plus grande ou plus petite.
4. Effectuer la même multiplication ou division sur l’autre grandeur.
5. Répondre avec l’unité et vérifier le sens de la variation.
:::
::: exemple Un lot suffit
Quatre pains aux raisins coûtent 7 euros. Douze pains, c’est trois lots de quatre : il y a trois fois autant de pains. Le prix est donc trois fois plus grand : $7\times3=21$ euros. Il est inutile de chercher le prix d’un seul pain.
:::
::: exemple Partager la quantité connue
Six litres de peinture couvrent 30 mètres carrés de mur dans les mêmes conditions. Trois litres, c’est deux fois moins de peinture : on couvre deux fois moins de surface, soit $30\div2=15$ mètres carrés. Dix-huit litres, c’est trois fois plus : $30\times3=90$ mètres carrés.
:::

## III. Vérifier si la règle s’applique
::: methode Tester un double
Si une quantité double dans une situation de proportionnalité, l’autre doit doubler aussi. Un contre-exemple suffit à montrer qu’une situation n’est pas proportionnelle. Un exemple isolé, sans information sur la règle suivie, ne suffit pas à garantir tous les cas.
:::
::: exemple Une part fixe
La piscine demande 10 euros d’abonnement puis 2 euros par entrée. Pour 5 entrées : $10+5\times2=20$ euros. Pour 10 entrées : $10+10\times2=30$ euros. Le nombre d’entrées double, mais le prix ne double pas : $20\times2=40$, et non 30. Le tarif n’est pas proportionnel au nombre d’entrées.
:::
::: attention Expliquer la relation, pas seulement le calcul
Dire « je multiplie par 3 » ne suffit pas. Préciser : « le nombre de cahiers est trois fois plus grand, donc le prix est trois fois plus grand ». Au CM1, les raisonnements sont exprimés par des phrases, sans tableau de proportionnalité ni produit en croix.
:::

## IV. Comparer et contrôler
::: exemple Deux magasins
Quatre croissants coûtent 5 euros chez Bleuet. Huit croissants y coûtent deux fois plus, soit 10 euros. S’ils coûtent $9{,}60$ euros chez Coquelicot, ce second magasin est moins cher pour huit croissants, avec $10-9{,}60=0{,}40$ euro d’écart.
:::
::: retenir
Garder les mêmes conditions, relier les deux grandeurs par une phrase, puis effectuer la même multiplication ou division. Si l’on achète moins d’objets au même tarif, le prix doit diminuer. Choisir une quantité intermédiaire simple lorsque cela aide, puis expliquer chaque passage.
:::
'''}

SHEETS={
2:r'''::: retenir
Addition : réunir ou ajouter ; résultat = somme. Soustraction : retirer, comparer ou chercher une partie ; résultat = différence.
:::
## I. Poser et contrôler
::: methode
Aligner les rangs. Calculer à partir des unités, en écrivant les retenues ou les échanges. Vérifier une soustraction par une addition : $5\,204-1\,368=3\,836$, car $3\,836+1\,368=5\,204$.
:::
## II. Choisir un chemin
::: exemple
Ajouter 19 : ajouter 20, puis retirer 1. $457+19=477-1=476$. Regrouper : $254+378+46=300+378=678$.
:::
::: methode Un problème
Comprendre, dessiner le tout et les parties si besoin, calculer les étapes, répondre avec l’unité. Estimer avant de poser : $6\,478+525$ est proche de 7 000.
:::
::: attention
Le mot « plus » ne choisit pas l’opération. Celui qui possède 68 cartes de moins que 325 en possède $325-68=257$.
:::
''',
3:r'''::: retenir
Multiplier compte des groupes égaux. $4\times45=180$ signifie quatre groupes de 45. L’ordre des facteurs ne change pas le produit.
:::
## I. Calculer de tête
::: methode
Multiplier par 4 : doubler deux fois. Par 8 : doubler trois fois. Par 5 : multiplier par 10, puis prendre la moitié. Par 10, 100, 1 000 : chaque chiffre monte de un, deux, trois rangs.
:::
::: exemple Décomposer
$$\begin{aligned}
23\times12&=23\times10+23\times2\\
&=230+46\\
&=276.
\end{aligned}$$
:::
## II. Poser et vérifier
::: methode
Calculer les produits partiels puis les ajouter : $347\times6=2\,082$ ; $347\times20=6\,940$ ; $2\,082+6\,940=9\,022$. Estimer : $486\times7$ est proche de $500\times7=3\,500$.
:::
::: attention
La deuxième ligne représente des dizaines. « Trois fois autant » signifie multiplier par 3. Dans un problème à plusieurs étapes, calculer d’abord chaque groupe, puis le total ou le reste.
:::
''',
4:r'''::: retenir
Une division euclidienne fournit un quotient entier et un reste : $87=4\times21+3$, avec $0\leq3<4$. Le reste est toujours plus petit que le diviseur.
:::
## I. Partager et contrôler
::: methode
Chercher un multiple proche sans dépasser. Poser de gauche à droite : partager, multiplier, soustraire, abaisser. Écrire les zéros utiles au quotient. Contrôler : $1\,258=6\times209+4$, avec $4<6$.
:::
## II. Multiples et diviseurs
::: rappel
Terminaison 0, 2, 4, 6, 8 : multiple de 2, donc pair. Terminaison 0 ou 5 : multiple de 5. Terminaison 0 : multiple de 10. Si le reste est nul, le diviseur partage exactement le nombre.
:::
::: attention Interpréter le reste
Pour 230 œufs en boîtes de 6 : 38 boîtes complètes et 2 œufs restants. Pour tout emporter : 39 boîtes. Lire la question avant de répondre.
:::
''',
5:r'''::: retenir
$=$ signifie « même valeur ». Un symbole garde la même valeur dans une situation. Une lettre peut désigner un nombre variable.
:::
## I. Nombre caché
::: methode
Défaire l’opération, puis contrôler : $47+\square=92$ donne $\square=45$, car $47+45=92$. Avec deux instructions, les défaire dans l’ordre inverse.
:::
## II. Programme et suite
::: exemple
Ajouter 2 puis multiplier par 4, en partant de 6 : $6+2=8$, puis $8\times4=32$. L’ordre compte.
:::
::: methode
Comparer plusieurs passages et formuler la règle. Avec « ajouter 7 » : 3 ; 10 ; 17 ; 24 ; 31. Avec un motif, compter les ajouts après la première étape.
:::
::: attention
Quelques termes ne déterminent pas toujours une règle unique. Respecter la règle annoncée. Pour une rangée de 5 carrés partageant un côté, il y a 4 ajouts de 3 allumettes : $4+4\times3=16$.
:::
''',
10:r'''::: retenir
Unités sous unités, dixièmes sous dixièmes, centièmes sous centièmes : aligner les virgules. $4{,}7=4{,}70$.
:::
## I. Additionner et soustraire
::: methode
Compléter par des zéros utiles, calculer de droite à gauche avec retenues ou échanges, placer la virgule sous les autres : $4{,}70+2{,}85=7{,}55$. Contrôler une différence par addition : $10-3{,}48=6{,}52$ et $6{,}52+3{,}48=10$.
:::
## II. Multiplier
::: methode
Par un entier de 1 à 9 : compter les dixièmes ou centièmes, puis retrouver l’écriture décimale. $345\times6=2\,070$ centièmes, donc $3{,}45\times6=20{,}70$. Par 10, chaque chiffre monte d’un rang ; diviser par 10 le fait descendre d’un rang.
:::
::: attention
Ne pas aligner simplement les derniers chiffres. Estimer : $5{,}6+2{,}14$ est proche de 8 ; son résultat exact est $7{,}74$. Dans un problème, garder l’unité et vérifier la vraisemblance.
:::
''',
19:r'''::: retenir
Dans une situation de proportionnalité, trois fois autant d’une grandeur donne trois fois autant de l’autre. Les conditions doivent rester identiques.
:::
## I. Raisonner par une phrase
::: methode
Comparer la quantité demandée à la quantité connue. Dire « deux fois plus », « trois fois moins », etc. Appliquer la même multiplication ou division à l’autre grandeur. Répondre avec l’unité.
:::
::: exemple
4 pains coûtent 7 euros. 12 pains, c’est trois fois autant : $7\times3=21$ euros. 6 L couvrent 30 mètres carrés ; 3 L, c’est deux fois moins : $30\div2=15$ mètres carrés.
:::
## II. Tester la règle
::: attention
Un abonnement fixe peut empêcher la proportionnalité. Si 5 entrées coûtent 20 euros et 10 entrées 30 euros, doubler les entrées ne double pas le prix. La taille d’un enfant n’est pas proportionnelle à son âge.
:::
::: conseil
Écrire le raisonnement en langage naturel. Un tableau ou un produit en croix n’est pas nécessaire. Un calcul exact doit toujours être accompagné de son sens.
:::
'''}

# Chaque exercice source est conservé dans le même ordre et enrichi en cinq questions.
E(2,'Deux sommes posées','Écrire les opérations en alignant les rangs.',[
C('6478+525','Échanger dix unités contre une dizaine, puis traiter les retenues successives.'),
C('38467+4850','Aligner les unités et ne pas oublier la retenue des centaines.'),
C('6500+500','Arrondir les deux termes permet de contrôler la première somme.','Estimer la première somme à partir de 6 500 et 500.'),
C('43317-4850','Retirer un terme de la somme doit retrouver l’autre.','Contrôler la deuxième somme par une soustraction.'),
Q('Mila trouve 7003 pour la première somme, mais 43317 pour la deuxième. Est-ce cohérent avec les estimations ?','Les résultats exacts sont proches des estimations, respectivement 7 000 et 43 000.','38000+5000=43000','Oui : les deux résultats ont un ordre de grandeur cohérent.')])
E(2,'Deux différences posées','Écrire les échanges nécessaires avant de soustraire.',[
C('5204-1368','Transformer une centaine en dix dizaines puis une dizaine en dix unités ; échanger aussi un millier si nécessaire.'),
C('70000-2460','Les échanges traversent les rangs contenant zéro : les noter sans modifier la valeur du nombre.'),
C('3836+1368','Le reste et la quantité retirée reconstituent le nombre de départ.','Vérifier la première différence.'),
C('67540+2460','Additionner les deux parties pour retrouver le tout.','Vérifier la seconde différence.'),
Q('Pourquoi ne peut-on pas écrire 5 204 − 1 368 = 4 164 en soustrayant toujours le petit chiffre du grand ?','Une soustraction respecte l’ordre des nombres. Si un rang manque d’unités, on effectue un échange. Le contrôle de la réponse proposée ne retrouve pas le départ.','4164+1368=5532','Cette règle est fausse : le résultat correct est $3\\,836$.')])
E(2,'Compléments utiles','Chercher la quantité manquante pour atteindre un repère.',[
C('100-64','La partie cherchée est la différence entre le tout et la partie connue.','Compléter $64+\\square=100$.'),
C('1000-380','Passer de 380 à 400, puis de 400 à 1 000.','Compléter $380+\\square=1\\,000$.'),
C('1000-725','Atteindre 800 puis 1 000, ou soustraire directement.','Compléter $725+\\square=1\\,000$.'),
C('10000-8640','Chercher ce qui manque pour atteindre dix milliers.','Compléter $8\\,640+\\square=10\\,000$.'),
C('8640+1360','Les deux parties doivent reconstituer le repère.','Contrôler le dernier complément par une addition.')])
E(2,'Ajouter 9, 19 ou 29','Calculer de tête en utilisant une dizaine entière.',[
C('457+9','Ajouter 10 donne 467, puis retirer 1.'),
C('457+19','Ajouter 20 donne 477, puis retirer 1.'),
C('262+29','Ajouter 30 donne 292, puis retirer 1.'),
C('638+39','Ajouter 40 donne 678, puis retirer 1.'),
Q('Léa calcule 262 + 29 en faisant 262 + 30 + 1. Quelle erreur commet-elle ?','Ajouter 30 ajoute déjà une unité de trop : il faut la retirer, pas l’ajouter.','262+30+1=293','Elle doit retirer 1 : $262+29=291$.')])
E(2,'Estimer avant de calculer','Pour 4 980 + 3 120, on propose 810 ; 8 100 ; 81 000.',[
C('5000+3000','Arrondir au millier suffit pour distinguer les propositions.','Donner une estimation de la somme.'),
Q('Quelle proposition est vraisemblable ?','Seule la proposition située autour de huit milliers convient.','','$8\\,100$.'),
C('4980+3120','Calculer maintenant le résultat exact pour confirmer le choix.','Vérifier par le calcul exact.'),
C('8100-8000','L’écart mesure la différence entre estimation et résultat exact.','Quel est l’écart entre la somme exacte et l’estimation ?'),
Q('Une estimation peut-elle servir de réponse exacte à toutes les questions ?','Arrondir modifie les données ; l’estimation contrôle seulement l’ordre de grandeur.','','Non : on calcule exactement quand la question demande un résultat exact.')])
E(2,'Regrouper pour aller vite','Dans une addition, on peut changer l’ordre des termes et les regrouper.',[
C('254+46','Ces deux termes atteignent une centaine entière.','Quels termes de $254+378+46$ peut-on réunir facilement ?'),
C('300+378','Remplacer les deux termes regroupés par leur somme.','Terminer le calcul $254+378+46$.'),
C('125+289+75','Réunir 125 et 75 pour obtenir 200.'),
C('650+487+350','Réunir 650 et 350 pour obtenir 1 000.'),
Q('Peut-on changer de même l’ordre de 650 − 350 sans modifier le résultat ?','Une différence dépend de l’ordre : retirer 650 à 350 ne donne pas le même résultat et sort ici du champ des entiers positifs.','650-350=300','Non : la propriété de changement d’ordre concerne l’addition, pas la soustraction.')])
E(2,'Une soustraction à trous','Remplacer chaque carré par un nombre qui rend l’égalité vraie.',[
C('385+247','Le nombre initial réunit ce qui a été retiré et ce qui reste.','Compléter $\\square-247=385$.'),
C('902-345','Le nombre retiré est la différence entre le départ et le reste.','Compléter $902-\\square=345$.'),
C('632-247','Replacer le nombre trouvé dans l’égalité initiale.','Contrôler la première réponse.'),
C('902-557','Replacer le nombre trouvé dans l’égalité initiale.','Contrôler la seconde réponse.'),
C('1200-468','Chercher la partie retirée pour laisser 468.','Compléter $1\\,200-\\square=468$.')])
E(2,'Le bon panneau','Une automobiliste lit « Beaupré 68 km », puis « Beaupré 29 km ». Elle suit la même route vers Beaupré.',[
Q('Quelle distance indique le premier panneau ?','Le panneau indique la distance encore à parcourir jusqu’à Beaupré.','','Il reste 68 km à parcourir.'),
Q('Pourquoi faut-il chercher une différence entre les indications ?','La distance restante diminue au fur et à mesure du trajet. L’écart entre les deux restes est la distance parcourue.','','Il faut retirer 29 de 68.'),
C('68-29','Soustraire les deux distances restantes.','Quelle distance a-t-elle parcourue entre les panneaux ?','km'),
C('39+29','La portion parcourue et la portion restante reconstituent la distance du premier panneau.','Vérifier la distance du premier panneau.','km'),
C('29-12','Le nouveau reste est plus petit de 12 km.','Elle roule encore 12 km après le deuxième panneau. Quelle distance reste-t-il ?','km')])
E(2,'Avec un schéma en barres','Un théâtre propose 850 places pour un même spectacle. Il vend 512 billets le samedi puis 218 le dimanche. Le schéma montre le tout et les parties.',[
Q('Que représente la barre complète ?','Les places vendues et les places libres forment toute la capacité du théâtre.','','La barre représente les 850 places.'),
C('512+218','Réunir les deux ventes avant de chercher le reste.','Combien de billets sont vendus en tout ?','billets'),
C('850-730','Retirer les places déjà vendues de la capacité totale.','Combien de places sont encore libres ?','places'),
C('730+120','Les places vendues et libres doivent retrouver la capacité.','Contrôler le résultat.','places'),
C('120-95','La nouvelle vente prélève des places dans la partie libre.','On vend ensuite 95 billets. Combien de places restent libres ?','places')], 'theatre')
E(2,'Le compte est-il bon ?','Issa affirme : « 4 003 − 1 587 = 3 584 ».',[
C('3584+1587','Une différence se contrôle en ajoutant ce qui a été retiré.','Calculer la somme qui permet de tester sa réponse.'),
Q('Sa réponse est-elle correcte ?','Le contrôle donne 5 171, alors que le départ était 4 003.','','Non : l’addition de contrôle ne retrouve pas 4 003.'),
C('4003-1587','Écrire les échanges à travers les zéros avant de soustraire.','Calculer la bonne différence.'),
C('2416+1587','Reconstituer le nombre initial.','Contrôler la correction.'),
C('4000-1600','Arrondir au millier et à la centaine donne un contrôle rapide.','Donner une estimation simple de la différence.')])
E(2,'La bibliothèque','Une bibliothèque possède 12 540 livres. Elle en prête 3 275, puis reçoit 1 860 livres. Les livres prêtés ne sont pas encore revenus.',[
C('12540-3275','Les livres prêtés quittent les étagères.','Combien de livres restent après les prêts ?','livres'),
C('9265+1860','Le don ajoute des livres présents sur place.','Combien de livres sont maintenant sur les étagères ?','livres'),
C('3275-1860','Comparer les sorties aux entrées.','De combien le nombre de livres présents a-t-il diminué ?','livres'),
C('12540-1415','Retirer la diminution totale retrouve la quantité présente.','Vérifier le résultat à partir de la diminution.','livres'),
C('11125+500','Ces retours ajoutent des livres sur les étagères.','Ensuite 500 livres prêtés reviennent. Combien sont présents ?','livres')])
E(2,'Qui a le plus ?','Nina a 325 cartes. Elle en a 68 de plus que Marco.',[
Q('Qui possède le plus de cartes ?','L’expression « Nina a 68 cartes de plus » compare sa collection à celle de Marco.','','Nina possède le plus de cartes.'),
C('325-68','Marco a moins de cartes : retirer l’écart de la collection de Nina.','Combien Marco a-t-il de cartes ?','cartes'),
C('257+68','Ajouter l’écart à la petite collection doit retrouver la grande.','Contrôler la comparaison.','cartes'),
C('325+257','Réunir les deux collections.','Combien ont-ils de cartes ensemble ?','cartes'),
C('257+68','Nina ne change pas sa collection ; Marco doit atteindre 325.','Marco reçoit 68 nouvelles cartes. A-t-il maintenant autant que Nina ?','cartes : oui, leurs collections sont égales.')], 'cartes')
E(2,'La cagnotte de la classe','La classe doit réunir 1 500 euros. La vente de gâteaux rapporte 480 euros et la tombola 655 euros.',[
C('480+655','Additionner les deux recettes de la classe.','Combien la classe a-t-elle déjà réuni ?','euros'),
C('1500-1135','Chercher la partie encore manquante du budget.','Combien manque-t-il ?','euros'),
C('1135+365','Le montant réuni et le manque doivent reconstituer l’objectif.','Vérifier le budget.','euros'),
C('365-200','Un nouveau don réduit le manque.','Un don de 200 euros arrive. Combien manque-t-il encore ?','euros'),
C('1135+200+165','Additionner toutes les recettes après une dernière collecte de 165 euros.','Une dernière collecte rapporte 165 euros. L’objectif est-il atteint ?','euros : oui, exactement.')])
E(2,'Trois étapes de course','Un rallye de 2 000 km comporte trois étapes. La première mesure 712 km. La deuxième mesure 56 km de moins.',[
C('712-56','La deuxième étape est plus courte que la première.','Quelle est la longueur de la deuxième étape ?','km'),
C('712+656','Réunir les deux premières étapes.','Combien mesure leur total ?','km'),
C('2000-1368','La troisième étape est la partie manquante du trajet.','Quelle est la longueur de la troisième étape ?','km'),
C('712+656+632','Toutes les étapes doivent reconstituer le parcours.','Vérifier la distance totale.','km'),
C('712-632','Comparer la plus longue à la plus courte.','De combien la première étape dépasse-t-elle la troisième ?','km')])
E(2,'Le vrai du faux','Chloé propose de remplacer 757 − 398 par 759 − 400.',[
Q('De combien a-t-elle augmenté chaque nombre ?','Les deux nombres ont été déplacés ensemble du même nombre d’unités.','759-757=2','Elle a ajouté 2 à chacun des deux nombres.'),
C('759-400','Retirer quatre centaines devient immédiat.','Calculer la nouvelle différence.'),
C('757-398','Retirer 400 puis remettre 2 donne le même écart.','Calculer la différence initiale.'),
Q('Pourquoi les deux différences sont-elles égales ?','Déplacer les deux extrémités d’un même écart de la même quantité conserve leur distance.','','Ajouter le même nombre aux deux termes conserve leur différence.'),
C('1246-799','Ajouter 1 aux deux nombres permet de calculer 1 247 − 800.','Utiliser la même idée pour calculer $1\\,246-799$.')])

E(3,'Des tables bien connues','Utiliser les tables de multiplication et contrôler les facteurs manquants.',[
C('7*8','Retrouver la table de 7 ou celle de 8.'),C('9*6','Utiliser neuf groupes de six.'),
C('48/6','Chercher combien de groupes de 6 font 48.','Compléter $\\square\\times6=48$.'),
C('8*6','Replacer le facteur trouvé.','Contrôler le facteur manquant.'),
C('7*8+9*6','Utiliser les deux premiers résultats et additionner.','Calculer $(7\\times8)+(9\\times6)$.')])
E(3,'Une addition qui se répète','On additionne quatre fois 45 : 45 + 45 + 45 + 45.',[
Q('Écrire cette addition sous forme d’un produit.','Le nombre de termes est quatre et chaque terme vaut 45.','','$4\\times45$.'),
C('45*2','Le double de 45 regroupe les deux premiers termes.','Calculer deux fois 45.'),
C('90*2','Doubler encore compte les quatre termes.','Calculer le total des quatre termes.'),
C('180+45','Ajouter un groupe augmente le nombre de groupes de un.','Quel serait le total avec cinq termes égaux à 45 ?'),
C('45*4','Le nombre d’objets reste identique si l’on change l’ordre des facteurs.','Contrôler le premier total en calculant $45\\times4$.')])
E(3,'Multiplier par 10, 100 ou 1 000','Observer la valeur de chaque chiffre après multiplication.',[
C('47*10','Chaque chiffre monte d’un rang.'),C('358*100','Chaque chiffre monte de deux rangs.'),
C('6*1000','Le chiffre des unités devient un chiffre des milliers.'),C('205*10','Le zéro des dizaines reste nécessaire pour conserver les rangs.'),
Q('Pourquoi 358 × 100 ne donne-t-il pas 3 580 ?','3 580 est seulement dix fois 358. Multiplier par 100 rend chaque chiffre cent fois plus grand.','358*10=3580'.replace('*',r'\times '),'Le bon résultat est $35\\,800$.')])
E(3,'Un produit posé','Étudier le calcul 486 × 7 rang par rang.',[
C('500*7','Arrondir 486 à 500 donne une estimation.','Estimer le produit en remplaçant 486 par 500.'),
C('6*7','42 unités donnent 2 unités écrites et 4 dizaines retenues.','Calculer le produit des unités.'),
C('8*7+4','Ajouter aux dizaines la retenue de quatre dizaines.','Calculer les dizaines avec la retenue.'),
C('4*7+6','La retenue précédente contient six centaines.','Calculer les centaines avec la retenue.'),
C('486*7','Réunir les rangs calculés : 3 milliers, 4 centaines, 0 dizaine et 2 unités.','Donner le produit exact et le comparer à l’estimation.')])
E(3,'Multiplier par 5','Multiplier par 10 puis prendre la moitié.',[
C('68*10','Dix groupes contiennent deux fois autant que cinq groupes.','Première étape pour calculer $68\\times5$.'),
C('680/2','Prendre la moitié du produit par dix.','Terminer le calcul de $68\\times5$.'),
C('240*5','La moitié de 2 400 vaut 1 200.'),C('86*5','La moitié de 860 vaut 430.'),
Q('Pourquoi cette méthode fonctionne-t-elle ?','Dix groupes se partagent en deux ensembles égaux de cinq groupes.','','La moitié de dix groupes est exactement cinq groupes.')])
E(3,'Deux chiffres au multiplicateur','Poser 347 × 26 en donnant le sens des deux lignes.',[
Q('Décomposer 26 pour préparer le produit.','Le chiffre 2 représente deux dizaines et le chiffre 6 représente six unités.','','$26=20+6$.'),
C('347*6','Cette ligne compte six groupes de 347.','Calculer la ligne des unités.'),
C('347*20','Cette ligne compte vingt groupes de 347.','Calculer la ligne des dizaines.'),
C('2082+6940','Réunir les six groupes et les vingt groupes.','Terminer le produit.'),
Q('Paul écrit 694 sur la seconde ligne et additionne sans décalage. Pourquoi est-ce faux ?','694 compte seulement deux groupes de 347. Le multiplicateur est vingt, donc cette ligne doit être dix fois plus grande.','347\\times2=694','La seconde ligne vaut $6\\,940$, car elle représente des dizaines.')])
E(3,'Décomposer un facteur','Calculer sans poser, en montrant la décomposition.',[
C('23*10','Préparer la partie dix du multiplicateur 12.','Calculer le premier produit de $23\\times(10+2)$.'),
C('23*2','Préparer la partie deux du multiplicateur 12.','Calculer le second produit.'),
C('230+46','Réunir les deux parties pour obtenir douze groupes de 23.','Donner $23\\times12$.'),
C('34*11','Décomposer 11 en 10 + 1 : dix groupes puis un groupe.'),
C('42*15','Décomposer 15 en 10 + 5 : 420 puis 210, à additionner.')])
E(3,'Des dizaines entre elles','Raisonner avec les groupes de dizaines ou de centaines.',[
C('40*70','Quatre dizaines multipliées par sept dizaines font vingt-huit centaines.'),
C('300*6','Trois centaines multipliées par six font dix-huit centaines.'),
C('50*80','Cinq dizaines multipliées par huit dizaines font quarante centaines.'),
C('60*90','Six dizaines multipliées par neuf dizaines font cinquante-quatre centaines.'),
Q('Pourquoi 50 × 80 possède-t-il trois zéros à la fin ?','Le produit de 5 par 8 vaut déjà 40 ; le passage des dizaines apporte encore un facteur 100.','40\\times100=4000','Le produit vaut $4\\,000$, pas 400.')])
E(3,'Le facteur caché','Trouver la valeur du carré puis vérifier.',[
C('200/25','Huit groupes de 25 forment deux centaines.','Compléter $25\\times\\square=200$.'),
C('270/30','Neuf groupes de 30 forment 270.','Compléter $\\square\\times30=270$.'),
C('25*8','Replacer le facteur trouvé dans le premier produit.','Contrôler la première réponse.'),
C('9*30','Replacer le facteur trouvé dans le second produit.','Contrôler la seconde réponse.'),
C('360/40','Utiliser la table de 4 : neuf groupes de quatre dizaines font 36 dizaines.','Compléter $40\\times\\square=360$.')])
E(3,'Trois fois autant','Un stade accueille 8 250 spectateurs le samedi et trois fois autant le dimanche.',[
Q('Que signifie « trois fois autant » ?','Le dimanche correspond à trois groupes ayant chacun l’effectif du samedi.','','Il faut multiplier $8\\,250$ par 3.'),
C('8250*3','Multiplier chaque partie : 8 000 fois 3 et 250 fois 3.','Combien viennent le dimanche ?','spectateurs'),
C('8250+24750','Réunir les deux journées sans compter trois fois le samedi en plus du dimanche.','Combien viennent sur les deux jours ?','spectateurs'),
C('24750-8250','Comparer les deux effectifs.','Combien de spectateurs supplémentaires viennent le dimanche ?','spectateurs'),
Q('Est-ce la même chose que « 8 250 spectateurs de plus » ?','Ajouter 8 250 au samedi donne seulement deux groupes de 8 250.','8250+8250=16500','Non : « trois fois autant » donne $24\\,750$ spectateurs.')])
E(3,'La commande de la cantine','La cantine reçoit 26 cagettes de 145 pommes et 18 cagettes de 230 poires.',[
C('145*26','Décomposer 26 en 20 + 6 : 2 900 et 870.','Combien de pommes reçoit-elle ?','pommes'),
C('230*18','Décomposer 18 en 10 + 8 : 2 300 et 1 840.','Combien de poires reçoit-elle ?','poires'),
C('3770+4140','Réunir les deux sortes de fruits.','Combien reçoit-elle de fruits au total ?','fruits'),
C('4140-3770','Comparer les deux quantités avant de répondre.','Combien reçoit-elle de poires de plus que de pommes ?','poires'),
C('7910-145','Retirer le contenu d’une cagette de pommes, pas une seule pomme.','Une cagette de pommes est réservée à une autre école. Combien reste-t-il de fruits ?','fruits')])
E(3,'La salle de spectacle','Une salle contient 32 rangées de 28 fauteuils. Pour un concert, 850 billets sont vendus.',[
C('32*20','Décomposer les 28 fauteuils de chaque rangée.','Combien de places représentent 20 fauteuils dans chacune des 32 rangées ?','places'),
C('32*8','Compter la partie restante de chaque rangée.','Combien représentent les 8 autres fauteuils par rangée ?','places'),
C('640+256','Réunir les deux parties pour compter toute la salle.','Quelle est la capacité de la salle ?','places'),
C('896-850','Comparer la capacité et les billets vendus.','Combien de places restent libres ?','places'),
C('46-28','Une nouvelle vente utilise une rangée entière.','On vend 28 billets supplémentaires. Combien de places restent libres ?','places')])
E(3,'Des menus à composer','On peut choisir 3 entrées, 4 plats et 2 desserts. Un menu prend un choix dans chaque catégorie.',[
C('1*4','Fixer une entrée : elle peut accompagner chacun des quatre plats.','Combien de couples entrée-plat avec une entrée fixée ?','couples'),
C('3*4','Chacune des trois entrées ouvre quatre choix de plat.','Combien de menus entrée-plat ?','menus'),
C('12*2','Chaque couple peut recevoir l’un ou l’autre des deux desserts.','Combien de menus complets ?','menus'),
C('4*2','Fixer l’entrée, puis combiner plats et desserts.','Combien de menus complets avec une entrée imposée ?','menus'),
C('3*5*2','Avec un cinquième plat, chaque entrée possède cinq choix, chacun avec deux desserts.','Un cinquième plat est ajouté. Combien de menus complets devient-il possible de composer ?','menus')])
E(3,'L’économie de Salomé','Salomé économise 35 euros par mois pendant 12 mois. Son frère économise 3 euros par semaine pendant 52 semaines.',[
C('35*12','Douze mois donnent douze versements identiques.','Combien Salomé économise-t-elle ?','euros'),
C('3*52','Compter les 52 versements hebdomadaires du frère.','Combien son frère économise-t-il ?','euros'),
Q('Qui économise le plus ?','Comparer 420 et 156 : 420 est plus grand.','','Salomé économise le plus.'),
C('420-156','Chercher l’écart entre les deux économies.','Combien Salomé a-t-elle d’avance ?','euros'),
C('35*6','Six mois correspondent à la moitié de l’année.','Combien Salomé économise-t-elle en six mois ?','euros')])
E(3,'Le piège du double','Maël affirme que 25 × 16 et 50 × 8 donnent le même résultat.',[
C('25*16','Décomposer 16 en 10 + 6 ou doubler quatre fois.'),C('50*8','Cinq dizaines multipliées par huit font quarante dizaines.'),
Q('Maël a-t-il raison ?','Les deux calculs donnent le même produit ; un facteur double et l’autre est partagé en deux.','','Oui : les deux produits valent 400.'),
C('100*4','Doubler encore le premier facteur et prendre la moitié du second.','Continuer la transformation : calculer $100\\times4$.'),
Q('Peut-on remplacer 25 × 16 par 50 × 16 en gardant le même produit ?','Un seul facteur a doublé : le nombre de groupes ne diminue pas. Le produit double donc aussi.','50\\times16=800','Non : il faut aussi prendre la moitié de l’autre facteur.')])

E(4,'Les premiers multiples','On cherche les multiples de 8 strictement positifs.',[
C('8*1','Un groupe de huit donne le premier multiple non nul.','Donner le premier multiple non nul de 8.'),
C('8*2','Deux groupes de huit donnent le deuxième multiple non nul.','Donner le deuxième multiple non nul de 8.'),
Q('Donner les trois multiples suivants.','Ajouter 8 à chaque fois : après 16, on obtient 24, puis 32, puis 40.','8\\times5=40','$24$ ; $32$ ; $40$.'),
C('8*6','Le sixième multiple non nul compte six groupes de huit.','Donner le sixième multiple non nul de 8.'),
Q('42 est-il un multiple de 8 ?','Les deux multiples qui entourent 42 sont 40 et 48 ; aucun ne vaut 42.','40<42<48','Non : 42 ne forme pas un nombre entier de groupes de 8.')])
E(4,'Pair ou impair','Étudier 346 ; 1 275 ; 90 ; 83 en observant le chiffre des unités.',[
Q('346 est-il pair ou impair ?','Son chiffre des unités est 6, donc il se partage en deux parts entières égales.','346\\div2=173','346 est pair.'),
Q('1 275 est-il pair ou impair ?','Son chiffre des unités est 5 : un partage en paquets de deux laisse une unité.','1275=2\\times637+1','1 275 est impair.'),
Q('90 est-il pair ou impair ?','Le chiffre des unités est zéro : c’est une terminaison paire.','90\\div2=45','90 est pair.'),
Q('83 est-il pair ou impair ?','Un partage en deux laisse une unité.','83=2\\times41+1','83 est impair.'),
Q('Donner un entier pair compris entre 83 et 90, puis justifier.','84 est dans l’intervalle et son chiffre des unités est 4.','84=2\\times42','84 convient ; 86 et 88 conviennent aussi.')])
E(4,'Multiples de 5 et de 10','Étudier 85 ; 120 ; 905 ; 1 004.',[
Q('85 est-il un multiple de 5 ?','Un entier terminé par 5 est multiple de 5.','85=5\\times17','Oui.'),
Q('120 est-il un multiple de 5 et de 10 ?','La terminaison zéro vérifie les deux critères.','120=10\\times12','Oui : 120 est multiple de 5 et de 10.'),
Q('905 est-il un multiple de 5 ? de 10 ?','Il se termine par 5, mais pas par zéro.','905=5\\times181','Multiple de 5 : oui. Multiple de 10 : non.'),
Q('1 004 est-il un multiple de 5 ou de 10 ?','Le chiffre des unités est 4, et ne vérifie aucun des deux critères.','','Non, ni de 5 ni de 10.'),
Q('Tout multiple de 10 est-il aussi multiple de 5 ?','Un multiple de 10 se termine par zéro, ce qui est aussi une terminaison de multiple de 5.','','Oui : deux groupes de 5 forment un groupe de 10.')])
E(4,'Une division posée','Partager 87 objets en paquets de 4.',[
Q('Quel multiple de 4 ne dépasse pas 8 dizaines et permet de commencer la division ?','Deux dizaines de paquets utilisent les huit dizaines.','4\\times20=80','80 : on commence par 2 dizaines au quotient.'),
C('87-80','Retirer les objets utilisés dans les vingt premiers paquets.','Combien reste-t-il après vingt paquets ?','objets'),
Q('Combien de paquets supplémentaires peut-on former avec ces 7 objets ?','Un paquet utilise 4 objets ; deux paquets en demanderaient 8.','7=4\\times1+3','Un paquet supplémentaire, puis 3 objets restants.'),
Q('Donner le quotient et le reste de la division de 87 par 4.','Les vingt premiers paquets et le paquet supplémentaire font vingt et un paquets.','87=4\\times21+3','Quotient : 21 ; reste : 3.'),
Q('Pourquoi ne peut-on pas constituer un paquet complet supplémentaire ?','Il reste trois objets, alors qu’un paquet en demande quatre.','3<4','Le reste est inférieur au diviseur.')])
E(4,'Diviseur ou pas ?','Utiliser un produit exact ou une égalité avec un reste.',[
C('7*13','Un produit qui retrouve exactement 91 prouve le partage sans reste.','Calculer $7\\times13$.'),
Q('7 est-il un diviseur de 91 ?','91 forme treize groupes de sept sans reste.','','Oui : $91=7\\times13$.'),
Q('Donner le quotient et le reste de 75 divisé par 6.','Douze groupes de six utilisent 72 objets ; il en reste trois.','75=6\\times12+3','Quotient : 12 ; reste : 3.'),
Q('6 est-il un diviseur de 75 ?','Le reste de la division n’est pas nul.','','Non : il reste 3.'),
Q('6 est-il un diviseur de 78 ?','Un groupe de six ajouté aux douze groupes précédents permet d’atteindre 78.','78=6\\times13','Oui : le reste est nul.')])
E(4,'Partager équitablement','On partage 345 billes entre 5 enfants, avec autant de billes pour chacun.',[
Q('Quelle opération permet de chercher la part d’un enfant ?','Le tout est connu et le nombre de parts égales aussi ; on cherche la taille d’une part.','','Il faut diviser 345 par 5.'),
C('345/5','On peut partager 300 en cinq, puis 45 en cinq : 60 et 9.','Combien chaque enfant reçoit-il ?','billes'),
C('69*5','Les cinq parts doivent reconstituer toutes les billes.','Contrôler le partage.','billes'),
Q('Le partage tombe-t-il juste ?','Le produit de la part par le nombre d’enfants retrouve exactement le tout.','','Oui : le reste est nul.'),
Q('On ajoute 2 billes au stock. Quel est alors le quotient et le reste du partage entre cinq ?','Les cinq parts de 69 utilisent encore 345 billes ; il en reste deux, insuffisantes pour donner une bille à chacun.','347=5\\times69+2','Quotient : 69 ; reste : 2.')])
E(4,'Quotient et contrôle','Effectuer la division de 1 258 par 6.',[
Q('Combien de centaines peut-on placer au quotient ?','On partage les 12 centaines en groupes de 6.','12\\div6=2','2 centaines.'),
Q('Pourquoi écrit-on zéro au rang des dizaines du quotient ?','Après avoir partagé les centaines, on abaisse 5 dizaines : elles ne permettent pas de donner une dizaine à chacun des six groupes.','','Il faut écrire 0 dizaine pour conserver les rangs.'),
Q('Après avoir abaissé le 8, comment partager les 58 unités ?','Neuf groupes de six utilisent 54 unités et il reste quatre.','58=6\\times9+4','9 unités au quotient et un reste de 4.'),
Q('Donner le quotient et le reste de la division complète.','Réunir les chiffres des centaines, dizaines et unités.','1258=6\\times209+4','Quotient : 209 ; reste : 4.'),
Q('La réponse 29 au quotient peut-elle convenir ?','Le zéro ne peut pas être supprimé : le contrôle ne retrouve pas 1 258.','6\\times29+4=178','Non : il faut conserver le zéro de 209.')])
E(4,'Encadrer par des multiples','Chercher les deux multiples consécutifs de 7 qui entourent 50.',[
C('7*7','La table de 7 permet d’approcher 50 sans le dépasser.'),
C('7*8','Le multiple suivant dépasse 50.'),
Q('Écrire l’encadrement de 50 avec ces multiples.','49 est juste en dessous de 50 et 56 juste au-dessus.','49<50<56','$49<50<56$.'),
Q('En déduire le quotient et le reste de 50 divisé par 7.','Sept groupes utilisent 49 unités ; une unité reste.','50=7\\times7+1','Quotient : 7 ; reste : 1.'),
Q('Donner le quotient et le reste de 55 divisé par 7.','55 reste inférieur à 56 : le quotient ne change pas, seul le reste augmente.','55=7\\times7+6','Quotient : 7 ; reste : 6.')])
E(4,'Un reste trop grand','Lina écrit : 74 = 8 × 8 + 10.',[
C('8*8+10','Il faut d’abord distinguer une égalité exacte d’une division correctement terminée.','L’égalité de Lina est-elle numériquement exacte ?'),
Q('Pourquoi ce n’est pas une division euclidienne terminée ?','Le reste annoncé dépasse le diviseur ; il contient encore un paquet complet.','10>8','Le reste 10 est trop grand.'),
C('10-8','Constituer un paquet de huit avec le reste augmente le quotient de un.','Quel reste obtient-on après un paquet supplémentaire ?'),
Q('Écrire la bonne égalité de division.','Le quotient devient neuf et le reste deux est inférieur à huit.','74=8\\times9+2','$74=8\\times9+2$ ; quotient 9, reste 2.'),
Q('Combien manque-t-il à 74 pour atteindre le multiple de 8 suivant ?','Le multiple suivant est 80 ; il manque six unités.','80-74=6','Il manque 6.')])
E(4,'Moitiés et quarts','Une moitié partage en deux ; un quart partage en quatre parts égales.',[
C('470/2','Partager 400 puis 70 en deux : 200 et 35.','Calculer la moitié de 470.'),
C('232/2','Préparer le quart en prenant une première moitié.','Calculer la moitié de 232.'),
C('116/2','Prendre la moitié de la moitié revient à partager en quatre.','Calculer le quart de 232.'),
C('58*4','Les quatre quarts doivent reconstituer le tout.','Contrôler le quart trouvé.'),
C('360/4','Prendre la moitié de 360, puis la moitié de 180.','Calculer le quart de 360.')])
E(4,'Les œufs en boîtes','Une ferme veut ranger 230 œufs dans des boîtes contenant 6 œufs chacune.',[
Q('Quelle opération faut-il effectuer ?','On connaît la taille d’un groupe et on cherche le nombre de groupes complets.','','Diviser 230 par 6.'),
Q('Combien de boîtes complètes peut-elle remplir ?','Trente-huit boîtes utilisent 228 œufs ; une boîte complète de plus demanderait 234 œufs.','230=6\\times38+2','38 boîtes complètes.'),
Q('Combien d’œufs restent hors des boîtes complètes ?','Le reste de la division compte les œufs qui ne remplissent pas une boîte.','','2 œufs.'),
Q('Combien faut-il de boîtes pour emporter tous les œufs ?','Les deux œufs restants demandent une boîte supplémentaire, même si elle n’est pas pleine.','38+1=39','39 boîtes.'),
C('6-2','La dernière boîte contient deux œufs et dispose de six emplacements.','Combien d’emplacements restent vides dans la dernière boîte ?','emplacements')], 'oeufs')
E(4,'Le vide-grenier','On répartit 91 livres en 7 lots identiques.',[
Q('Que cherche la division : un nombre de lots ou une taille de lot ?','Le nombre de lots est déjà donné : sept.','','On cherche le nombre de livres par lot.'),
C('91/7','La table de 7 peut être prolongée : dix groupes donnent 70 et trois groupes donnent 21.','Combien de livres contient chaque lot ?','livres'),
C('13*7','Reconstituer les livres en réunissant les sept lots.','Contrôler la répartition.','livres'),
Q('Le partage tombe-t-il juste ?','Le produit de 13 par 7 retrouve exactement les 91 livres.','','Oui : le reste est nul, donc 7 est un diviseur de 91.'),
C('13+2','Quatorze livres supplémentaires partagés en sept donnent deux livres de plus à chaque lot.','On reçoit 14 livres de plus. Combien contient maintenant chaque lot ?','livres')])
E(4,'Des équipes de huit','134 élèves souhaitent former des équipes de 8.',[
Q('Combien d’équipes complètes peut-on former ?','Seize équipes utilisent 128 élèves, sans dépasser 134.','134=8\\times16+6','16 équipes complètes.'),
Q('Combien d’élèves restent hors des équipes complètes ?','Le reste compte les élèves qui ne constituent pas une nouvelle équipe entière.','','6 élèves.'),
C('8-6','Compléter le groupe incomplet jusqu’à huit.','Combien faut-il d’élèves de plus pour compléter une équipe supplémentaire ?','élèves'),
C('8*17','Dix-sept équipes doivent contenir chacune huit élèves.','Combien faut-il d’élèves pour 17 équipes ?','élèves'),
C('134+2','L’effectif initial augmenté du manque doit retrouver l’effectif nécessaire.','Vérifier la dernière réponse.','élèves')])
E(4,'Le nombre mystère','Un entier est compris strictement entre 82 et 94. C’est un multiple de 5 et il est pair.',[
Q('Quels multiples de 5 peuvent convenir dans cet intervalle ?','Chercher les terminaisons 0 ou 5 parmi les entiers autorisés.','','85 et 90.'),
Q('Pourquoi 85 est-il éliminé ?','Le chiffre des unités est 5 : ce nombre est impair.','','85 n’est pas pair.'),
Q('Quel est le nombre mystère ?','90 est dans l’intervalle, se termine par zéro et vérifie les deux critères.','','90.'),
Q('Pourquoi la réponse est-elle unique ?','Les seuls multiples de 5 possibles étaient 85 et 90 ; l’un des deux a été éliminé.','','Il reste une seule possibilité : 90.'),
Q('Si l’on retire la condition « pair », la réponse reste-t-elle unique ?','Les deux multiples de 5 sont alors autorisés.','','Non : 85 et 90 conviennent.')])
E(4,'Toujours vrai ?','Zoé affirme : « La somme de deux nombres pairs est toujours paire. »',[
C('26+58','Calculer le premier exemple avant d’examiner sa parité.'),
Q('Le premier résultat est-il pair ?','84 est constitué de paquets de deux.','84=2\\times42','Oui : 84 est pair.'),
C('134+72','Calculer un deuxième exemple différent.'),
Q('Deux exemples suffisent-ils à prouver que l’affirmation est toujours vraie ?','Les exemples vérifient seulement les cas testés ; une explication générale est nécessaire.','','Non : il faut expliquer ce qui se passe pour tous les nombres pairs.'),
Q('Expliquer avec des paquets de deux.','Chaque nombre pair est un ensemble de paquets de deux. Réunir les deux ensembles ne laisse aucun objet seul.','','La somme reste faite de paquets de deux : elle est toujours paire.')])

E(5,'Vrai ou faux ?','Une égalité est vraie si les deux côtés ont la même valeur.',[
C('8+6','Évaluer le côté gauche de la première égalité.','Calculer le côté gauche de $8+6=9+5$.'),
C('9+5','Comparer avec la première valeur obtenue : les deux côtés valent quatorze.','Calculer le côté droit et conclure sur la première égalité.',': l’égalité est vraie.'),
C('7*4','Évaluer le côté gauche de la seconde égalité.','Calculer le côté gauche de $7\\times4=30-3$.'),
C('30-3','La valeur 27 n’est pas égale à la valeur 28 trouvée à gauche.','Calculer le côté droit et conclure sur la seconde égalité.',': l’égalité est fausse.'),
Q('Remplacer le 3 de la seconde égalité par le bon nombre pour la rendre vraie.','Chercher ce qu’il faut retirer à 30 pour obtenir 28.','30-28=2','Il faut écrire $7\\times4=30-2$.')])
E(5,'Trous additifs','Chaque carré cache le nombre qui rend l’égalité vraie.',[
C('92-47','Retirer la partie connue du total.','Compléter $47+\\square=92$.'),
C('35+28','Le départ réunit ce qui a été retiré et ce qui reste.','Compléter $\\square-28=35$.'),
C('47+45','Remplacer le carré par le nombre trouvé.','Contrôler la première égalité.'),
C('63-28','Remplacer le carré par le nombre trouvé.','Contrôler la seconde égalité.'),
C('108-64','Chercher la partie retirée pour laisser 64.','Compléter $108-\\square=64$.')])
E(5,'Trous multiplicatifs','Trouver les nombres manquants en traitant chaque côté de l’égalité.',[
C('84/7','Chercher le nombre de groupes de sept dans 84.','Compléter $7\\times\\square=84$.'),
C('7*12','Remplacer le carré et retrouver le produit demandé.','Contrôler la première réponse.'),
C('6*8','Calculer d’abord le côté entièrement connu.','Dans $178-\\square=6\\times8$, calculer le côté droit.'),
C('178-48','Chercher la quantité retirée pour laisser 48.','Trouver le second nombre caché.'),
C('178-130','Replacer la valeur et comparer au côté droit.','Contrôler la seconde réponse.')])
E(5,'La machine à nombres','Le programme ajoute 2 au nombre choisi, puis multiplie le résultat par 4.',[
C('6+2','Exécuter seulement la première instruction.','Quelle est la valeur intermédiaire en partant de 6 ?'),
C('8*4','La seconde instruction utilise la valeur intermédiaire 8.','Quel est le résultat final en partant de 6 ?'),
C('10+2','Recommencer le programme avec un autre départ.','Quelle est la valeur intermédiaire en partant de 10 ?'),
C('12*4','Multiplier la nouvelle valeur intermédiaire par 4.','Quel est le résultat final en partant de 10 ?'),
C('(3+2)*4','Les parenthèses montrent que l’addition est faite en premier.','Exécuter tout le programme en partant de 3.')])
E(5,'Poursuivre une suite','On poursuit la suite 3 ; 10 ; 17 ; 24 en ajoutant toujours le même nombre.',[
C('10-3','L’écart entre les deux premiers termes donne une règle possible.','Quel nombre ajoute-t-on entre les deux premiers termes ?'),
C('17-10','Vérifier la même différence sur le passage suivant.','Vérifier la règle entre 10 et 17.'),
C('24+7','Appliquer la règle annoncée, ajouter 7.','Donner le terme qui suit 24.'),
C('31+7','Recommencer la même instruction.','Donner encore le terme suivant.'),
Q('45 est-il le terme qui suit 38 avec cette règle ?','Le passage doit encore ajouter sept.','38+7=45','Oui : le terme suivant est 45.')])
E(5,'Deux règles différentes','La suite A commence par 5 ; 10 ; 20 ; 40 et double à chaque fois. La suite B commence par 5 ; 10 ; 15 ; 20 et ajoute 5 à chaque fois.',[
C('40*2','Appliquer le double annoncé pour la suite A.','Donner le cinquième terme de A.'),
C('20+5','Appliquer l’ajout annoncé pour la suite B.','Donner le cinquième terme de B.'),
C('80*2','La règle de A reste le double.','Donner le sixième terme de A.'),
C('25+5','La règle de B reste ajouter cinq.','Donner le sixième terme de B.'),
Q('Les deux premiers termes 5 et 10 suffisent-ils à distinguer ces deux règles ?','Ajouter cinq et doubler transforment tous deux 5 en 10, mais divergent ensuite.','','Non : les mêmes premiers termes peuvent appartenir à des suites différentes.')])
E(5,'Remonter la machine','Un programme multiplie le nombre choisi par 3, puis retire 4. Il affiche 20.',[
C('20+4','Défaire la dernière instruction : retirer quatre se défait en ajoutant quatre.','Quelle était la valeur juste avant le retrait ?'),
C('24/3','Défaire ensuite la multiplication par trois.','Quel était le nombre de départ ?'),
C('8*3','Contrôler dans le sens direct à partir du départ trouvé.','Quelle valeur obtient-on après la première instruction ?'),
C('24-4','Terminer le contrôle du programme.','Vérifier le résultat affiché.'),
C('(32+4)/3','Pour obtenir 32, ajouter quatre puis partager en trois.','Quel départ donnerait un résultat final de 32 ?')])
E(5,'La suite qui zigzague','On part de 80 et on alterne « ajouter 5 », puis « retirer 2 ». Les premiers termes sont 80 ; 85 ; 83 ; 88 ; 86 ; 91 ; 89.',[
Q('Quelle instruction suit le dernier terme 89 ?','Le passage de 91 à 89 a retiré deux ; on revient ensuite à l’ajout de cinq.','','Ajouter 5.'),
C('89+5','Appliquer la prochaine instruction.','Donner le terme suivant.'),
C('94-2','Alterner : après l’ajout de cinq vient le retrait de deux.','Donner encore le terme suivant.'),
C('92+5','Le nouvel ajout de cinq relance le même cycle.','Donner le terme suivant 92.'),
C('5-2','Sur deux passages, l’ajout et le retrait se combinent.','De combien la valeur augmente-t-elle après deux passages successifs ?')])
E(5,'Deux symboles','Un triangle garde la même valeur : $\\triangle+\\triangle+5=19$ et $\\triangle+\\bullet=12$.',[
C('19-5','Retirer la partie connue pour isoler les deux triangles.','Quelle est la valeur des deux triangles réunis ?'),
C('14/2','Les deux triangles ont la même valeur.','Quelle est la valeur d’un triangle ?'),
C('12-7','Retirer la valeur du triangle pour trouver celle du disque.','Quelle est la valeur du disque ?'),
C('7+7+5','Remplacer chaque triangle par sa valeur.','Contrôler la première égalité.'),
C('7+5','Remplacer le triangle et le disque par leurs valeurs.','Contrôler la seconde égalité.')])
E(5,'Le nombre caché','Le carré vérifie $\\square\\times4+3=31$. La multiplication se fait avant l’ajout de 3.',[
C('31-3','Défaire la dernière étape : l’ajout de trois.','Quelle est la valeur du produit avant l’ajout de 3 ?'),
C('28/4','Défaire la multiplication par quatre.','Trouver la valeur du carré.'),
C('7*4','Repartir du nombre trouvé et exécuter la première opération.','Contrôler le produit.'),
C('28+3','Terminer le contrôle dans le sens direct.','Vérifier l’égalité complète.'),
C('(35-3)/4','Défaire les mêmes opérations en partant cette fois de 35.','Quel nombre remplacerait le carré si le résultat final était 35 ?')])
E(5,'Les tee-shirts','Un tee-shirt coûte 12 euros. La livraison de la commande coûte 5 euros, quel que soit le nombre de tee-shirts.',[
C('4*12','Quatre tee-shirts représentent quatre groupes de douze euros.','Quel est le prix de 4 tee-shirts sans livraison ?','euros'),
C('48+5','La livraison est ajoutée une seule fois à toute la commande.','Quel est le prix de 4 tee-shirts livrés ?','euros'),
C('6*12+5','Calculer d’abord les six tee-shirts, puis une seule livraison.','Quel est le prix de 6 tee-shirts livrés ?','euros'),
Q('Que représente N dans l’expression $(N\\times12)+5$ ?','La même règle peut être utilisée pour diverses quantités commandées.','','N représente le nombre de tee-shirts de la commande.'),
Q('L’expression $N\\times(12+5)$ décrit-elle le même tarif ?','Elle ajouterait cinq euros pour chaque tee-shirt au lieu d’une seule fois.','4\\times17=68','Non : la bonne expression est $(N\\times12)+5$.')])
E(5,'Ciseaux et stylos','Deux paires de ciseaux identiques et trois stylos à 2 euros coûtent ensemble 20 euros.',[
C('3*2','Le prix des trois stylos est entièrement connu.','Combien coûtent les stylos ?','euros'),
C('20-6','Retirer les stylos du prix total pour isoler les deux paires de ciseaux.','Combien coûtent les deux paires de ciseaux ?','euros'),
C('14/2','Les deux paires ont le même prix.','Combien coûte une paire de ciseaux ?','euros'),
C('2*7+3*2','Reconstituer le prix des deux types d’objets.','Vérifier le ticket.','euros'),
C('3*7+2*2','Réutiliser les prix trouvés pour une autre commande.','Combien coûtent trois paires de ciseaux et deux stylos ?','euros')])
E(5,'Des carrés d’allumettes','Le premier carré utilise 4 allumettes. Chaque carré suivant partage un côté avec le précédent et ajoute 3 allumettes.',[
Q('Pourquoi ajoute-t-on seulement trois allumettes par nouveau carré ?','Un côté appartient déjà au carré précédent ; les trois autres côtés sont nouveaux.','','Un côté est partagé, donc on ajoute 3 allumettes.'),
C('4+3','Après le premier carré, il y a un ajout.','Combien faut-il d’allumettes pour deux carrés ?','allumettes'),
C('4+4*3','Cinq carrés comprennent le premier puis quatre ajouts.','Combien pour cinq carrés ?','allumettes'),
C('4+9*3','Dix carrés comprennent le premier puis neuf ajouts.','Combien pour dix carrés ?','allumettes'),
Q('Avec 22 allumettes, combien de carrés forme une telle rangée ?','Après les quatre premières allumettes, il reste dix-huit allumettes, soit six ajouts de trois ; ajouter le premier carré.','(22-4)\\div3+1=7','7 carrés.')], 'allumettes')
E(5,'Le motif en croix','Une croix a 5 carreaux à l’étape 1. À chaque étape, on ajoute un carreau à chacun de ses quatre bras.',[
C('5+4','La deuxième étape ajoute un carreau sur chaque bras.','Combien de carreaux à l’étape 2 ?','carreaux'),
C('5+3*4','De l’étape 1 à l’étape 4, il y a trois ajouts de quatre.','Combien à l’étape 4 ?','carreaux'),
C('29-5','Retirer les carreaux de l’étape initiale.','Pour une croix de 29 carreaux, combien ont été ajoutés ?','carreaux'),
C('24/4','Chaque passage ajoute quatre carreaux.','Combien de passages séparent l’étape 1 de la croix de 29 carreaux ?'),
C('1+6','Six passages après l’étape 1 mènent à l’étape 7.','À quelle étape trouve-t-on 29 carreaux ?')], 'croix')
E(5,'Inventer et suivre un programme','On compare les programmes A : « multiplier par 5, puis ajouter 1 » et B : « ajouter 1, puis multiplier par 5 ». Le plan quadrillé sert à une dernière activité de codage.',[
C('5*5','Le programme A commence par une multiplication.','Avec le départ 5, quelle est la valeur intermédiaire de A ?'),
C('25+1','Ajouter un après la multiplication.','Quel résultat final donne A avec le départ 5 ?'),
C('(5+1)*5','Les parenthèses respectent l’ordre annoncé du programme B.','Quel résultat final donne B avec le même départ ?'),
Q('L’ordre des deux instructions change-t-il le résultat ici ?','Les deux valeurs finales sont différentes, 26 et 30.','','Oui : A donne 26 et B donne 30.'),
Q('Inventer un autre programme en deux instructions qui transforme 5 en 26.','On peut multiplier d’abord par quatre, puis ajouter six. D’autres réponses contrôlées peuvent convenir.','5\\times4+6=26','Par exemple : multiplier par 4, puis ajouter 6.'),
Q('Sur le plan, partir de A1, aller de deux cases vers la droite puis de deux cases vers le haut. Quelle case atteint-on ?','Les colonnes suivent les lettres A, B, C ; les lignes augmentent en montant. Après la première instruction, on est en C1 ; après la seconde, en C3.','','On atteint la case C3.')], 'deplacement')

E(10,'Une somme posée','Étudier 4,7 + 2,85 avec des rangs bien alignés.',[
Q('Écrire 4,7 avec deux chiffres après la virgule.','Un zéro ajouté à droite de la partie décimale ne change pas la valeur.','4{,}7=4{,}70','$4{,}70$.'),
Q('Quels chiffres doivent être alignés ?','On additionne des unités de même taille : unités avec unités, dixièmes avec dixièmes, centièmes avec centièmes.','','Les virgules, donc les mêmes rangs, doivent être alignés.'),
C('4.7+2.85','Les centièmes donnent cinq ; les dixièmes donnent quinze dixièmes, donc une unité retenue.','Poser et calculer la somme.'),
C('5+3','Arrondir chacun des deux nombres à l’entier le plus proche.','Donner une estimation simple de la somme.'),
C('7.55-2.85','Retirer un terme doit retrouver l’autre terme.','Contrôler le résultat exact.')])
E(10,'Une différence posée','Calculer 10 − 3,48 en utilisant les centièmes.',[
Q('Comment écrire 10 pour faire apparaître les centièmes ?','Dix unités valent dix unités et zéro centième.','10=10{,}00','$10{,}00$.'),
Q('Pourquoi faut-il des échanges pour soustraire les centièmes ?','Le premier nombre n’a aucun centième disponible. On échange une unité contre dix dixièmes, puis un dixième contre dix centièmes.','','Pour disposer d’assez de dixièmes et de centièmes à retirer.'),
C('10-3.48','Après les échanges, effectuer la soustraction rang par rang.','Calculer la différence.'),
C('6.52+3.48','Le reste et la quantité retirée doivent reconstituer le départ.','Contrôler le résultat.'),
C('20-3.48','On retire la même quantité à un nombre supérieur de dix : la différence augmente de dix.','Calculer ensuite $20-3{,}48$.')])
E(10,'De tête sans retenue','Modifier seulement les rangs utiles.',[
C('5.34+2','Ajouter deux unités ne modifie pas les chiffres des dixièmes et centièmes.'),
C('5.34+0.2','Ajouter deux dixièmes au chiffre des dixièmes.'),
C('7.89-4','Retirer quatre unités en conservant la partie décimale.'),
C('5.34+0.04','Ajouter quatre centièmes au chiffre des centièmes.'),
C('7.89-0.3','Retirer trois dixièmes sans changer les centièmes.')])
E(10,'Par 10 dans les deux sens','Expliquer les résultats par le changement de rang des chiffres.',[
C('3.7*10','Le chiffre 3 devient trois dizaines et le chiffre 7 devient sept unités.'),
C('0.85*10','Huit dixièmes deviennent huit unités ; cinq centièmes deviennent cinq dixièmes.'),
C('45.2/10','Chaque chiffre prend une valeur dix fois plus petite ; les deux dixièmes deviennent deux centièmes.'),
C('0.6/10','Six dixièmes partagés par dix deviennent six centièmes.'),
C('4.52*10','Multiplier par dix défait la division par dix.','Contrôler le résultat de $45{,}2\\div10$.')])
E(10,'Un produit en dixièmes','Calculer 2,4 × 3 en comptant les dixièmes.',[
Q('Combien de dixièmes contient 2,4 ?','Deux unités font vingt dixièmes, auxquels on ajoute quatre dixièmes.','2{,}4=24\\div10','24 dixièmes.'),
C('24*3','On triple le nombre de dixièmes sans changer l’unité de comptage.','Combien de dixièmes obtient-on après multiplication par 3 ?','dixièmes'),
Q('Écrire 72 dixièmes sous forme décimale.','Dix dixièmes font une unité : 72 dixièmes font sept unités et deux dixièmes.','72\\div10=7{,}2','$7{,}2$.'),
C('2.4+2.4+2.4','Trois groupes de 2,4 peuvent aussi se compter par addition.','Contrôler par une addition répétée.'),
C('2.4*4','Quatre groupes contiennent un groupe de plus que trois groupes.','Calculer $2{,}4\\times4$.')])
E(10,'Compléments utiles','Chercher une partie manquante, puis vérifier par addition.',[
C('1-0.35','100 centièmes moins 35 centièmes laissent 65 centièmes.','Compléter $0{,}35+\\square=1$.'),
C('10-7.2','Chercher l’écart entre le nombre et la dizaine suivante.','Compléter $7{,}2+\\square=10$.'),
C('0.35+0.65','Les deux parties reconstituent une unité.','Contrôler la première réponse.'),
C('7.2+2.8','Les deux parties reconstituent dix unités.','Contrôler la seconde réponse.'),
C('5-4.76','Écrire cinq sous la forme 5,00 pour raisonner en centièmes.','Compléter $4{,}76+\\square=5$.')])
E(10,'Un produit posé','Calculer 3,45 × 6 avec les centièmes.',[
Q('Combien de centièmes contient 3,45 ?','Trois unités font 300 centièmes, quatre dixièmes font 40 centièmes et il reste cinq centièmes.','','345 centièmes.'),
C('345*6','Poser le produit entier : unités, dizaines, centaines avec les retenues.','Calculer le produit du nombre de centièmes.','centièmes'),
Q('Écrire 2 070 centièmes sous forme décimale.','Cent centièmes font une unité : il y a vingt unités et soixante-dix centièmes.','2070\\div100=20{,}70','$20{,}70$, soit $20{,}7$.'),
C('3.5*6','Arrondir à 3,5 permet un contrôle proche.','Estimer le produit avec $3{,}5\\times6$.'),
Q('Le résultat 2,07 pourrait-il convenir pour 3,45 × 6 ?','Multiplier un nombre positif par six l’agrandit ; 2,07 est plus petit que 3,45 et loin de l’estimation 21.','','Non : le produit correct est $20{,}70$.')])
E(10,'Regrouper pour simplifier','Choisir les termes qui forment une somme facile.',[
C('2.6+0.4','Six dixièmes et quatre dixièmes font une unité.','Quels termes de $2{,}6+4{,}85+0{,}4$ donnent une somme entière ?'),
C('3+4.85','Remplacer les deux termes regroupés par leur somme.','Terminer le calcul de la somme.'),
C('1.75+3.6+0.25','Réunir 1,75 et 0,25 pour former deux unités.'),
C('4.2+2.85+0.8','Réunir 4,2 et 0,8 pour former cinq unités.'),
Q('Peut-on supprimer la virgule dans 2,6 pour faciliter le calcul ?','2,6 et 26 n’ont pas la même valeur : le rang de chaque chiffre serait modifié.','','Non : on peut regrouper les termes, mais pas changer leur valeur.')])
E(10,'Contrôler une soustraction','Noé annonce : « 8 − 2,35 = 6,35 ».',[
C('6.35+2.35','La différence proposée et le nombre retiré doivent retrouver huit.','Calculer la somme de contrôle.'),
Q('La proposition de Noé est-elle juste ?','La somme de contrôle vaut 8,70 et non 8.','','Non : son résultat est trop grand.'),
C('8-2.35','Écrire 8,00 et effectuer les échanges nécessaires.','Calculer la différence correcte.'),
C('5.65+2.35','Contrôler la nouvelle réponse par l’opération inverse.','Vérifier la correction.'),
C('6.35-5.65','Comparer le résultat annoncé au résultat exact.','De combien Noé s’est-il trompé ?')])
E(10,'Rendre la monnaie','Un achat coûte 7,45 euros. On paie avec un billet de 10 euros.',[
C('7.5-7.45','Atteindre le demi-euro suivant.','Combien faut-il pour passer de 7,45 euros à 7,50 euros ?','euro'),
C('8-7.5','Atteindre ensuite l’euro entier.','Combien faut-il pour passer de 7,50 euros à 8 euros ?','euro'),
C('10-8','Terminer le trajet jusqu’à dix euros.','Combien faut-il pour passer de 8 à 10 euros ?','euros'),
C('0.05+0.5+2','Additionner les trois compléments successifs.','Quelle monnaie doit-on rendre ?','euros'),
C('7.45+2.55','Le prix et la monnaie doivent reconstituer le billet donné.','Contrôler la monnaie.','euros')])
E(10,'Le panier de courses','Une baguette coûte 1,20 euro, le beurre 2,85 euros et le lait 1,15 euro. On paie ces trois achats avec 10 euros.',[
C('2.85+1.15','Ces deux prix forment exactement quatre euros.','Quel regroupement facilite le calcul du beurre et du lait ?','euros'),
C('1.2+4','Ajouter la baguette au total des deux autres achats.','Quelle est la dépense totale ?','euros'),
C('10-5.2','Chercher la différence entre le paiement et la dépense.','Quelle monnaie reçoit-on ?','euros'),
C('5.2+4.8','Le prix et la monnaie reconstituent le paiement.','Contrôler le ticket.','euros'),
C('5.2-1.15','Retirer le prix du lait du panier initial.','Si l’on renonce au lait, combien dépense-t-on ?','euros')])
E(10,'Les sorties du coureur','Un coureur parcourt 4,5 km lundi. Mardi, il parcourt 1,8 km de moins que lundi.',[
Q('Mardi, la distance est-elle plus grande ou plus petite ?','L’expression « de moins » compare le mardi au lundi.','','Elle est plus petite.'),
C('4.5-1.8','Retirer l’écart à la distance de lundi.','Quelle distance court-il mardi ?','km'),
C('4.5+2.7','Réunir les distances des deux journées.','Quelle distance parcourt-il en tout ?','km'),
C('2.7+1.8','Ajouter l’écart à la petite distance doit retrouver celle de lundi.','Contrôler la comparaison.','km'),
C('10-7.2','Comparer la distance déjà courue à l’objectif.','Il vise 10 km sur trois jours. Quelle distance lui manque-t-il ?','km')])
E(10,'Trois carnets identiques','Un carnet coûte 2,45 euros. Lina en achète trois et paie avec 10 euros.',[
C('245*3','Compter les prix en centimes pour effectuer un produit entier.','Quel est le prix de trois carnets en centimes ?','centimes'),
Q('Écrire ce prix en euros.','Cent centimes font un euro : 735 centimes font sept euros et trente-cinq centimes.','735\\div100=7{,}35','$7{,}35$ euros.'),
C('10-7.35','Le paiement est supérieur au prix : chercher ce qui doit être rendu.','Quelle monnaie reçoit Lina ?','euros'),
C('7.35+2.65','Le prix et la monnaie doivent faire dix euros.','Contrôler la réponse.','euros'),
C('2.45*4','Un quatrième carnet ajoute encore 2,45 euros.','Quatre carnets pourraient-ils être payés avec 10 euros ?','euros : oui, car ce prix est inférieur à 10 euros.')])
E(10,'Le ruban coupé','Un ruban mesure 2,75 m. On y coupe deux morceaux de 0,9 m chacun. Le dessin est un schéma de la situation.',[
C('0.9+0.9','Réunir les longueurs des deux morceaux identiques.','Quelle longueur a été coupée au total ?','m'),
C('2.75-1.8','Retirer la longueur utilisée de la longueur initiale.','Quelle longueur reste-t-il ?','m'),
C('1.8+0.95','La partie coupée et le reste reconstituent le ruban.','Contrôler le résultat.','m'),
C('0.95-0.9','Comparer le reste à la longueur d’un morceau demandé.','Peut-on couper encore un morceau de 0,9 m ? Quelle longueur restera-t-il ?','m : oui, il reste cette longueur.'),
C('0.9*3+0.05','Les trois morceaux et la chute doivent reconstituer le ruban initial.','Vérifier après les trois coupes.','m')], 'ruban')
E(10,'L’alignement fautif','Tom calcule 5,6 + 2,14 en alignant les derniers chiffres plutôt que les virgules. Il annonce 2,70.',[
Q('Quel rang doit être placé sous le chiffre 6 de 5,6 ?','Le chiffre 6 représente six dixièmes. Il faut le placer au-dessus des dixièmes de l’autre nombre.','','Le chiffre 1 de 2,14, qui représente un dixième.'),
Q('Écrire le premier nombre pour faire apparaître les centièmes.','Ajouter un zéro à droite de la partie décimale conserve la valeur.','5{,}6=5{,}60','$5{,}60$.'),
C('5.6+2.14','Additionner les centièmes puis les dixièmes puis les unités, avec les virgules alignées.','Calculer la bonne somme.'),
C('6+2','Une estimation à l’entier donne une somme proche de huit.','Donner une estimation simple.'),
Q('Pourquoi 2,70 est-il impossible même sans poser le calcul ?','On ajoute un nombre positif à 5,6 : la somme doit être supérieure à 5,6. Or 2,70 est plus petit.','','Ce résultat est inférieur au premier terme ; il ne peut donc pas être la somme.')])

E(19,'Proportionnel ou pas ?','On suppose les cahiers identiques vendus au même tarif, sans frais supplémentaires ni réduction.',[
Q('Le prix de ces cahiers est-il proportionnel à leur nombre ?','Deux fois autant de cahiers coûtent deux fois autant, et la même relation vaut pour toute multiplication de la quantité.','','Oui, avec les conditions annoncées.'),
Q('La taille d’un enfant est-elle proportionnelle à son âge ?','Un enfant deux fois plus âgé n’est pas nécessairement deux fois plus grand.','','Non.'),
Q('Si trois cahiers coûtent 6 euros, combien coûtent six cahiers au même tarif ?','Six cahiers, c’est deux fois autant que trois ; le prix est donc doublé.','6\\times2=12','12 euros.'),
Q('Si une personne de 5 ans mesure 110 cm, peut-on déduire qu’elle mesurera 220 cm à 10 ans ?','Le doublement de l’âge ne commande pas un doublement de la taille.','','Non : la taille ne suit pas cette règle de proportionnalité.'),
Q('Pourquoi faut-il préciser « sans frais supplémentaires ni réduction » ?','Un coût fixe ou une réduction peut changer la relation entre quantité et prix.','','Pour garantir que la même multiplication s’applique aux deux grandeurs.')])
E(19,'Deux fois plus','Un kilogramme de pommes coûte 2,40 euros. Les pommes sont vendues au même tarif quelle que soit la quantité.',[
Q('Quel lien y a-t-il entre 2 kg et 1 kg ?','Deux kilogrammes représentent deux fois un kilogramme.','','2 kg, c’est deux fois autant que 1 kg.'),
C('2.4*2','Deux fois autant de pommes coûtent deux fois autant.','Quel est le prix de 2 kg ?','euros'),
C('4.8*2','Quatre kilogrammes, c’est deux fois autant que deux ; doubler encore le prix.','Quel est le prix de 4 kg ?','euros'),
C('2.4*3','Trois kilogrammes, c’est trois fois autant qu’un ; tripler le prix.','Quel est le prix de 3 kg ?','euros'),
Q('Pourquoi ne faut-il pas seulement ajouter 1 euro quand on passe de 1 à 2 kg ?','La relation porte sur les quantités : doubler les kilogrammes impose de doubler le prix, pas d’ajouter un euro.','','Le prix doit suivre la même multiplication que la masse.')])
E(19,'La recette multipliée','Pour 4 personnes, une recette demande 250 g de riz. Les portions restent identiques.',[
C('8/4','Chercher combien de groupes de quatre personnes composent huit personnes.','Combien de fois 8 personnes représentent-elles 4 personnes ?'),
C('250*2','Deux fois autant de personnes demandent deux fois autant de riz.','Quelle masse faut-il pour 8 personnes ?','g'),
C('250*3','Douze personnes, c’est trois fois autant que quatre.','Quelle masse faut-il pour 12 personnes ?','g'),
C('250*4','Seize personnes, c’est quatre fois autant que quatre.','Quelle masse faut-il pour 16 personnes ?','g'),
Q('Pourquoi la masse pour 12 personnes ne vaut-elle pas 250 + 8 ?','L’augmentation de huit personnes ne se traduit pas par huit grammes ; il faut respecter la taille des portions.','','On doit tripler 250 g, car 12 personnes représentent trois fois 4 personnes.')])
E(19,'Les pains aux raisins','Quatre pains aux raisins identiques coûtent 7 euros, sans réduction ni frais fixes.',[
C('12/4','Déterminer le nombre de lots identiques à celui qui est connu.','Combien de lots de quatre pains y a-t-il dans douze pains ?'),
C('7*3','Trois fois autant de pains coûtent trois fois autant.','Combien coûtent douze pains ?','euros'),
C('7*2','Huit pains, c’est deux fois autant que quatre.','Combien coûtent huit pains ?','euros'),
C('7*5','Vingt pains correspondent à cinq lots de quatre.','Combien coûtent vingt pains ?','euros'),
Q('Faut-il obligatoirement connaître le prix d’un seul pain pour répondre ?','Toutes les quantités demandées sont des multiples entiers du lot connu.','','Non : on raisonne directement sur les lots de quatre.')])
E(19,'Les cahiers du bureau','Cinq cahiers identiques coûtent 8 euros. Le tarif ne change pas.',[
C('15/5','Quinze cahiers forment trois lots de cinq.','Combien de fois quinze cahiers représentent-ils cinq cahiers ?'),
C('8*3','Le prix doit être trois fois plus grand pour trois fois autant de cahiers.','Combien coûtent quinze cahiers ?','euros'),
C('8*2','Dix cahiers, c’est deux fois autant que cinq.','Combien coûtent dix cahiers ?','euros'),
C('8*4','Vingt cahiers, c’est quatre fois autant que cinq.','Combien coûtent vingt cahiers ?','euros'),
Q('Un lot de vingt cahiers annoncé à 24 euros respecterait-il ce tarif ?','Quatre fois cinq cahiers devraient coûter quatre fois huit euros, soit trente-deux euros.','','Non : vingt cahiers coûtent 32 euros au tarif annoncé.')])
E(19,'Fois moins','Dix photocopies coûtent 3 euros au même tarif, sans frais fixes.',[
C('30/10','Chercher combien de lots de dix copies composent trente copies.','Trente copies, c’est combien de fois dix copies ?'),
C('3*3','Trois fois plus de copies coûtent trois fois plus.','Combien coûtent trente copies ?','euros'),
Q('Cinq copies représentent quelle part de dix copies ?','On partage les dix copies en deux groupes égaux.','','Cinq copies, c’est deux fois moins que dix copies.'),
Q('Combien coûtent cinq copies ?','Trois euros font 300 centimes ; la moitié de 300 centimes vaut 150 centimes, soit 1,50 euro.','300\\div2=150','$1{,}50$ euro.'),
C('1.5*2','Doubler la petite quantité doit retrouver la grande et son prix.','Contrôler le prix de dix copies à partir de celui de cinq copies.','euros')])
E(19,'Le pot de peinture','Six litres de peinture couvrent 30 mètres carrés. Le mur et l’épaisseur de peinture restent comparables.',[
Q('Pourquoi peut-on utiliser la proportionnalité ?','Dans les conditions annoncées, deux fois autant de peinture couvre deux fois autant de surface.','','Dans les mêmes conditions, multiplier le volume de peinture multiplie la surface couverte par le même nombre.'),
C('30/2','Trois litres, c’est deux fois moins que six ; la surface est deux fois plus petite.','Quelle surface couvre-t-on avec 3 L ?','mètres carrés'),
C('30*3','Dix-huit litres, c’est trois fois autant que six.','Quelle surface couvre-t-on avec 18 L ?','mètres carrés'),
C('30*2','Douze litres, c’est deux fois autant que six.','Quelle surface couvre-t-on avec 12 L ?','mètres carrés'),
Q('Pour couvrir 90 mètres carrés, combien de litres faut-il ?','90 mètres carrés, c’est trois fois 30 ; il faut donc trois fois 6 litres.','6\\times3=18','18 L.')])
E(19,'À allure régulière','Un train parcourt 320 km en 2 heures. Il garde exactement la même allure, sans arrêt.',[
Q('Quelle condition rend la distance proportionnelle au temps ici ?','La même durée produit toujours la même distance tant que l’allure reste constante et qu’il n’y a pas d’arrêt.','','L’allure reste constante, sans arrêt.'),
C('320/2','Une heure, c’est deux fois moins de temps que deux heures.','Quelle distance parcourt-il en 1 heure ?','km'),
C('320*3','Six heures, c’est trois fois autant que deux heures.','Quelle distance parcourt-il en 6 heures ?','km'),
C('320*2','Quatre heures, c’est deux fois autant que deux heures.','Quelle distance parcourt-il en 4 heures ?','km'),
Q('Peut-on appliquer directement la même règle si le train s’arrête pendant une heure ?','Une durée incluant un arrêt ne correspond plus à la même distance parcourue par heure.','','Non : il faut connaître et prendre en compte l’arrêt.')])
E(19,'Les crêpes du goûter','Avec 250 g de farine, on prépare 12 crêpes de même taille, en gardant les proportions de la recette.',[
C('500/250','La masse de farine est multipliée par deux.','Combien de fois 500 g représentent-ils 250 g ?'),
C('12*2','Deux fois autant de farine permet deux fois autant de crêpes.','Combien de crêpes avec 500 g ?','crêpes'),
C('36/12','Chercher combien de groupes de douze font trente-six.','Combien de fois 36 crêpes représentent-elles 12 crêpes ?'),
C('250*3','Trois fois autant de crêpes demandent trois fois autant de farine.','Quelle masse pour 36 crêpes ?','g'),
C('12*4','Un kilogramme vaut mille grammes, soit quatre fois la quantité connue.','Combien de crêpes avec 1 kg de farine ?','crêpes')])
E(19,'L’abonnement piégé','La piscine demande 10 euros d’abonnement, puis 2 euros par entrée. L’abonnement n’est payé qu’une fois.',[
C('5*2','Compter d’abord les entrées seules.','Quel est le prix de cinq entrées sans l’abonnement ?','euros'),
C('10+5*2','Ajouter la part fixe une seule fois.','Quel est le prix total pour cinq entrées ?','euros'),
C('10+10*2','Le nombre d’entrées double, mais l’abonnement reste le même.','Quel est le prix total pour dix entrées ?','euros'),
C('20*2','Dans une situation proportionnelle, doubler les entrées devrait doubler ce total.','Quel serait le double du total pour cinq entrées ?','euros'),
Q('Paul affirme que dix entrées coûtent deux fois le total de cinq entrées. A-t-il raison ?','Le vrai total vaut 30 euros, tandis que le double de 20 vaut 40 euros.','','Non : le tarif total n’est pas proportionnel au nombre d’entrées.')])
E(19,'La fontaine du square','Une fontaine à débit régulier remplit un grand récipient de 40 L en 5 minutes, sans interruption.',[
C('20/5','Vingt minutes représentent quatre fois la durée connue.','Combien de fois 20 minutes représentent-elles 5 minutes ?'),
C('40*4','Quatre fois plus de temps donne quatre fois plus de volume.','Quel volume remplit-elle en 20 minutes ?','L'),
C('120/40','120 litres représentent trois fois le volume connu.','Combien de fois 120 L représentent-ils 40 L ?'),
C('5*3','Trois fois plus de volume nécessite trois fois plus de temps à débit constant.','Combien de temps faut-il pour remplir 120 L ?','minutes'),
C('40*2','Dix minutes représentent deux fois cinq minutes.','Quel volume remplit-elle en 10 minutes ?','L')])
E(19,'Le marché','Trois kilogrammes de poires coûtent 7,50 euros. Le tarif reste le même.',[
C('9/3','Neuf kilogrammes forment trois fois la masse connue.','Combien de fois 9 kg représentent-ils 3 kg ?'),
C('7.5*3','Trois fois plus de masse entraîne trois fois plus de prix.','Combien coûtent 9 kg ?','euros'),
C('7.5*2','Six kilogrammes représentent deux fois trois kilogrammes.','Combien coûtent 6 kg ?','euros'),
C('7.5*4','Douze kilogrammes représentent quatre fois trois kilogrammes.','Combien coûtent 12 kg ?','euros'),
Q('Pourquoi n’ajoute-t-on pas seulement 6 euros quand on passe de 3 kg à 9 kg ?','Les six kilogrammes supplémentaires ne coûtent pas un euro chacun ; il faut utiliser le tarif de la situation.','','On triple le prix de 3 kg, car on achète trois fois cette masse.')])
E(19,'Deux boulangeries','Chez Bleuet, 4 croissants coûtent 5 euros. Chez Coquelicot, 8 croissants coûtent 9,60 euros. Dans chaque boulangerie, le tarif est proportionnel à la quantité.',[
C('5*2','Huit croissants, c’est deux fois quatre.','Combien coûtent 8 croissants chez Bleuet ?','euros'),
Q('Où les huit croissants sont-ils les moins chers ?','Comparer les prix pour une même quantité : 9,60 euros est inférieur à 10 euros.','','Chez Coquelicot.'),
C('10-9.6','Comparer les prix pour huit croissants, sans changer la quantité.','Quelle est l’économie réalisée ?','euro'),
C('5*4','Seize croissants, c’est quatre fois quatre.','Combien coûtent 16 croissants chez Bleuet ?','euros'),
C('9.6*2','Seize croissants, c’est deux fois huit.','Combien coûtent 16 croissants chez Coquelicot ?','euros')])
E(19,'Le ruban au mètre','Quatre mètres de ruban coûtent 6 euros. Le tarif est proportionnel à la longueur. Lisa veut connaître le prix de 10 m.',[
Q('Pourquoi Lisa choisit-elle d’abord 2 m ?','Deux mètres sont la moitié de quatre mètres, et dix mètres sont cinq fois deux mètres.','','Cette longueur intermédiaire se relie simplement aux deux longueurs.'),
C('6/2','Deux fois moins de ruban coûte deux fois moins.','Quel est le prix de 2 m ?','euros'),
C('3*5','Dix mètres sont cinq fois deux mètres : multiplier le prix par cinq.','Quel est le prix de 10 m ?','euros'),
C('6*3','Douze mètres sont trois fois quatre mètres.','Quel est le prix de 12 m ?','euros'),
Q('Un prix de 5 euros pour 10 m serait-il vraisemblable ?','Dix mètres dépassent quatre mètres ; au même tarif, le prix doit dépasser six euros.','','Non : la quantité augmente, donc son prix doit augmenter.')])
E(19,'Le carré qui grandit','Un carré a d’abord 3 carreaux de côté. On double ce côté : le nouveau carré a 6 carreaux de côté. On compte le contour en côtés de carreaux et l’aire en carreaux.',[
C('3+3+3+3','Le contour comporte quatre côtés de trois unités.','Quelle est la longueur du premier contour ?','unités de longueur'),
C('6+6+6+6','Le nouveau contour comporte quatre côtés de six unités.','Quelle est la longueur du nouveau contour ?','unités de longueur'),
Q('Le contour a-t-il doublé ?','Le premier contour vaut 12 et le nouveau 24.','12\\times2=24','Oui : doubler chaque côté double le contour.'),
Q('Compter les carreaux des deux surfaces.','Le premier carré possède trois rangées de trois carreaux ; le second six rangées de six carreaux.','3\\times3=9\n6\\times6=36','Ancienne aire : 9 carreaux ; nouvelle aire : 36 carreaux.'),
Q('L’aire est-elle proportionnelle à la longueur du côté ?','Le côté double, mais la surface compte quatre fois plus de carreaux.','9\\times4=36','Non : l’aire est multipliée par 4 et ne double pas.')], 'carres')

FIGURES={c:{} for c in CODES}
FIGURES[2]['ecole']=r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[text=otNavy] at (3.8,1.25) {258 élèves au total};
\fill[otNavy!12] (0,0) rectangle (4,.7);
\fill[otGreen!18] (4,0) rectangle (7.6,.7);
\draw[geoTrait] (0,0) rectangle (7.6,.7);
\draw[geoTrait] (4,0)--(4,.7);
\node[text=otNavy] at (2,.35) {136 filles};
\node[text=otGreenDark] at (5.8,.35) {122 garçons};
\end{tikzpicture}'''
FIGURES[2]['theatre']=r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[text=otNavy] at (4,1.25) {850 places au total};
\fill[otNavy!12] (0,0) rectangle (4.82,.7);
\fill[otOrange!18] (4.82,0) rectangle (6.87,.7);
\fill[otGreen!15] (6.87,0) rectangle (8,.7);
\draw[geoTrait] (0,0) rectangle (8,.7);
\draw[geoTrait] (4.82,0)--(4.82,.7) (6.87,0)--(6.87,.7);
\node at (2.41,.35) {512}; \node at (5.845,.35) {218};
\node[text=otGreenDark] at (7.435,.35) {?};
\node[text=otMuted] at (2.41,-.42) {samedi};
\node[text=otMuted] at (5.845,-.42) {dimanche};
\node[text=otGreenDark] at (7.435,-.42) {libres};
\end{tikzpicture}'''
FIGURES[2]['cartes']=r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[anchor=east,text=otNavy] at (-.2,1.35) {Nina};
\node[anchor=east,text=otNavy] at (-.2,.15) {Marco};
\draw[geoTrait,fill=otNavy!12] (0,1) rectangle (6.5,1.7);
\draw[geoTrait,fill=otNavy!12] (0,-.2) rectangle (5.14,.5);
\node at (3.25,1.35) {325 cartes};
\node at (2.57,.15) {?};
\draw[guide] (5.14,.55)--(5.14,.85) (6.5,-.2)--(6.5,.85);
\draw[cote] (5.14,.7)--(6.5,.7) node[coteTexte,midway] {68};
\end{tikzpicture}'''
FIGURES[3]['groupes']=r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[text=otNavy] at (3.5,1.6) {Quatre groupes égaux};
\foreach \x in {0,1.8,3.6,5.4}{
\draw[geoTrait,fill=otSky] (\x,0) rectangle +(1.5,.9);
\node at (\x+.75,.45) {45};}
\node[text=otGreenDark] at (3.45,-.55) {$4\times45=180$};
\end{tikzpicture}'''
FIGURES[4]['partage']=r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[text=otNavy] at (3.5,1.85) {24 objets répartis en 4 groupes égaux};
\foreach \x in {0,1.8,3.6,5.4}{
\draw[geoTrait,fill=otSky] (\x,0) rectangle +(1.5,1.15);
\foreach \u in {.35,.75,1.15}{\foreach \v in {.35,.8}{
\fill[otNavy] (\x+\u,\v) circle (2.5pt);}}}
\node[text=otGreenDark] at (3.45,-.55) {6 objets dans chaque groupe};
\end{tikzpicture}'''
FIGURES[4]['oeufs']=r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[text=otNavy] at (3.5,2.05) {230 œufs : des boîtes de 6 et un reste};
\foreach \x in {0,1.65}{
\draw[geoTrait,fill=otSky] (\x,0) rectangle +(1.3,1.1);
\foreach \u in {.25,.65,1.05}{\foreach \v in {.3,.8}{
\fill[otNavy] (\x+\u,\v) ellipse (.065 and .09);}}}
\node at (3.4,.55) {$\cdots$};
\draw[geoTrait,fill=otSky] (4,0) rectangle +(1.3,1.1);
\foreach \u in {.25,.65,1.05}{\foreach \v in {.3,.8}{\fill[otNavy] (4+\u,\v) ellipse (.065 and .09);}}
\draw[otGreenDark,line width=.8pt] (5.9,0) rectangle +(1.3,1.1);
\foreach \u in {.25,.65}{\fill[otGreenDark] (5.9+\u,.3) ellipse (.065 and .09);}
\node[text=otNavy] at (2.6,-.55) {38 boîtes complètes};
\node[text=otGreenDark] at (6.55,-.55) {2 œufs};
\end{tikzpicture}'''
FIGURES[5]['allumettes']=r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[text=otNavy] at (3.25,1.75) {Chaque nouveau carré partage un côté};
\foreach \x in {0,1.3,2.6,3.9,5.2}{
\draw[geoTrait] (\x,0)--(\x,1.3)--(\x+1.3,1.3);
\draw[geoTrait] (\x,0)--(\x+1.3,0);}
\draw[geoTrait] (6.5,0)--(6.5,1.3);
\node[text=otGreenDark] at (3.25,-.55) {5 carrés : 16 allumettes};
\end{tikzpicture}'''
FIGURES[5]['croix']=r'''
\begin{tikzpicture}[x=.43cm,y=.43cm]
\foreach \x/\n in {0/1,6/2,14/3}{
\foreach \a in {-\n,...,\n}{
\draw[geoTrait,fill=otSky] (\x+\a,0) rectangle +(1,1);}
\foreach \a in {-\n,...,\n}{
\draw[geoTrait,fill=otSky] (\x,\a) rectangle +(1,1);}}
\node[text=otMuted] at (.5,-2.1) {étape 1};
\node[text=otMuted] at (6.5,-3.1) {étape 2};
\node[text=otMuted] at (14.5,-4.1) {étape 3};
\end{tikzpicture}'''
FIGURES[5]['deplacement']=r'''
\begin{tikzpicture}[x=1.05cm,y=1.05cm]
\draw[otRule,step=1] (0,0) grid (4,4);
\foreach \x/\l in {.5/A,1.5/B,2.5/C,3.5/D}{\node[text=otNavy] at (\x,-.35) {\l};}
\foreach \y/\l in {.5/1,1.5/2,2.5/3,3.5/4}{\node[text=otNavy] at (-.35,\y) {\l};}
\fill[otNavy] (.5,.5) circle (3pt);
\node[text=otNavy,anchor=west] at (4.4,2.6) {Départ : A1};
\node[text=otMuted,anchor=west] at (4.4,1.85) {Droite : colonnes};
\node[text=otMuted,anchor=west] at (4.4,1.1) {Haut : lignes};
\end{tikzpicture}'''
FIGURES[10]['monnaie']=r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \x/\l in {.65/7{,}45,2.65/7{,}50,4.65/8,6.65/10}{
\draw[geoTrait,fill=otSky] (\x-.65,0) rectangle +(1.3,.75);
\node[text=otNavy] at (\x,.375) {$\l$};}
\foreach \x in {1.3,3.3,5.3}{\draw[otGreenDark,-{Stealth},line width=.8pt] (\x+.08,.375)--(\x+.62,.375);}
\node[text=otGreenDark] at (1.65,1.2) {$+0{,}05$};
\node[text=otGreenDark] at (3.65,1.2) {$+0{,}50$};
\node[text=otGreenDark] at (5.65,1.2) {$+2$};
\node[text=otMuted] at (3.65,-.55) {Étapes du complément en euros};
\end{tikzpicture}'''
FIGURES[10]['ruban']=r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[text=otNavy] at (3.85,1.25) {Ruban initial : $2{,}75$ m};
\fill[otSky] (0,0) rectangle (2.52,.7);
\fill[otNavy!18] (2.52,0) rectangle (5.04,.7);
\fill[otGreen!15] (5.04,0) rectangle (7.7,.7);
\draw[geoTrait] (0,0) rectangle (7.7,.7);
\draw[geoTrait] (2.52,0)--(2.52,.7) (5.04,0)--(5.04,.7);
\node at (1.26,.35) {$0{,}9$ m};
\node at (3.78,.35) {$0{,}9$ m};
\node[text=otGreenDark] at (6.37,.35) {reste ?};
\end{tikzpicture}'''
FIGURES[19]['recette']=r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[text=otNavy] at (1.3,1.8) {4 personnes};
\node[text=otNavy] at (5.5,1.8) {8 personnes};
\draw[geoTrait,fill=otSky] (.3,0) rectangle (2.3,1);
\node at (1.3,.5) {250 g};
\draw[geoTrait,fill=otSky] (3.4,0) rectangle (5.4,1);
\draw[geoTrait,fill=otSky] (5.7,0) rectangle (7.7,1);
\node at (4.4,.5) {250 g}; \node at (6.7,.5) {250 g};
\draw[otGreenDark,-{Stealth},line width=.9pt] (2.6,.5)--(3.1,.5);
\node[text=otGreenDark] at (5.5,-.55) {Deux fois autant de riz};
\end{tikzpicture}'''
FIGURES[19]['carres']=r'''
\begin{tikzpicture}[x=.65cm,y=.65cm]
\fill[otNavy!12] (0,0) rectangle (3,3);
\fill[otGreen!12] (5,0) rectangle (11,6);
\draw[otNavy,step=1] (0,0) grid (3,3);
\draw[otGreenDark,step=1] (5,0) grid (11,6);
\node[text=otNavy] at (1.5,-.65) {côté : 3};
\node[text=otGreenDark] at (8,-.65) {côté : 6};
\end{tikzpicture}'''

ALTS={
'ecole':'Barre de 258 élèves partagée en 136 filles et 122 garçons.',
'theatre':'Barre de 850 places partagée entre 512 billets du samedi, 218 du dimanche et les places libres à trouver.',
'cartes':'Comparaison des 325 cartes de Nina avec la collection plus petite de Marco, avec un écart de 68 cartes.',
'groupes':'Quatre rectangles contenant chacun 45 objets représentent quatre groupes égaux et un total de 180.',
'partage':'Vingt-quatre points répartis en quatre rectangles contenant six points chacun.',
'oeufs':'Boîtes contenant chacune six œufs, avec trente-huit boîtes complètes et deux œufs dans une dernière boîte.',
'allumettes':'Rangée de cinq carrés partageant leurs côtés, constituée de seize segments représentant des allumettes.',
'croix':'Trois croix successives sur un quadrillage : un centre et quatre bras qui grandissent d’un carreau à chaque étape.',
'deplacement':'Plan de quatre colonnes A à D et quatre lignes 1 à 4, avec le point de départ dans la case A1.',
'monnaie':'Schéma des compléments successifs de 7,45 à 7,50 puis 8 et 10 euros, avec ajouts de 0,05, 0,50 et 2 euros.',
'ruban':'Ruban de 2,75 mètres partagé en deux morceaux de 0,9 mètre et une longueur restante à calculer.',
'recette':'Un paquet de 250 grammes pour quatre personnes et deux paquets identiques pour huit personnes.',
'carres':'Deux carrés quadrillés de trois puis six carreaux de côté, pour comparer leurs contours et leurs surfaces.'}

COURSE_FIG={2:'ecole',3:'groupes',4:'partage',5:'allumettes',10:'monnaie',19:'recette'}

def rediger():
    for c in CODES:
        d=next(BASE.glob(f'{c:02}_*'))
        source=json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf-8'))
        assert len(DATA[c])==len(source['exercices'])==15
        title=source['titre']
        (d/'cours_nouveau.txt').write_text('Titre: '+title+'\n<!-- optitab:1 -->\n'+COURSES[c].strip()+'\n',encoding='utf-8')
        (d/'fiche_nouvelle.txt').write_text('Titre: '+title+' — l’essentiel\n<!-- optitab:1 -->\n'+SHEETS[c].strip()+'\n',encoding='utf-8')
        figures=d/'figures';figures.mkdir(exist_ok=True)
        (figures/'figures.py').write_text('# -*- coding: utf-8 -*-\nFIGURES = '+repr(FIGURES[c])+'\n',encoding='utf-8')
        corr={'cours':{'nouveau':{'1':{'fichier':COURSE_FIG[c]+'.png','alt':ALTS[COURSE_FIG[c]]}}},'fiches':{},'exercices':{}}
        output=[]; attendu=[]
        for i,e in enumerate(DATA[c],1):
            ident=f'nouveau-{i}'
            diff=source['exercices'][i-1]['difficulte']
            kind={1:'Découverte',2:'Entraînement',3:'Problème'}[diff]
            out=[f'=== {kind} - {e["titre"]}',f'Id: {ident}',f'Difficulté: { {1:"easy",2:"medium",3:"hard"}[diff]}','', 'Énoncé:','<!-- optitab:1 -->',e['contexte'],'']
            if e['figure'] and e['figure']!='oeufs':out.extend(['[IMAGE_1]',''])
            for n,q in enumerate(e['questions'],1):out.append(f'{n}. {q["question"]}')
            out.extend(['','Étapes:','<!-- optitab:1 -->'])
            for n,q in enumerate(e['questions'],1):
                out.extend([f'## Question {n} : {q["question"]}','','::: methode',q['methode'],':::','','::: etape Raisonner et calculer',q['raison']])
                if q['calcul']:
                    for chain in q['calcul'].splitlines():out.extend(['','$$'+chain+'$$'])
                out.extend([':::','','::: resultat',q['reponse'],':::',''])
                if n==2 and e['figure']=='oeufs':out.extend(['[IMAGE_1]',''])
            out.extend(['Solution:','<!-- optitab:1 -->'])
            for n,q in enumerate(e['questions'],1):out.append(f'{n}. {q["reponse"]}')
            output.append('\n'.join(out)+'\n')
            attendu.append({'id':ident,'titre_source':source['exercices'][i-1]['titre'],'questions':e['questions']})
            if e['figure']:corr['exercices'][ident]={'1':{'fichier':e['figure']+'.png','alt':ALTS[e['figure']]}}
        (d/'exercices.txt').write_text('\n===\n\n'.join(output),encoding='utf-8')
        (figures/'correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (d/'verification_attendus.json').write_text(json.dumps(attendu,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'cm1_calculs','maj':'2026-11-01'},ensure_ascii=False)+'\n',encoding='utf-8')
        report=f'''# {title} — CM1

État : textes rédigés ; compilation et relecture visuelle encore à effectuer.

Les 15 exercices sources sont repris dans leur ordre et enrichis, avec au moins cinq questions chacun, un corrigé détaillé par question et une solution courte cohérente. Aucun fichier source n’a été modifié. Il n’existait pas d’ID de base à conserver ; les blocs sont préparés avec les identifiants nouveau-1 à nouveau-15.

Programme vérifié dans l’annexe officielle du cycle 3 : https://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf. Les nombres entiers restent limités à six chiffres, les décimaux aux centièmes et les diviseurs posés à un chiffre. La multiplication décimale par un entier inférieur à dix figure explicitement au programme CM1 (section Les quatre opérations). Les lettres et les programmes à deux instructions sont explicitement prévus. La proportionnalité est traitée par des phrases et des multiplications ou divisions de grandeurs ; aucun tableau, coefficient ou produit en croix n’est utilisé.

Figures : {len(FIGURES[c])} schémas TikZ nouveaux, aucune image source altérée. Les appels et alternatives descriptives sont définis dans figures/correspondance.json. Les documents utilisent le même format OptiTAB v1 que le pilote.

Contrôles : verif_math.py vérifie les calculs réellement présents, la présence des cinq questions et l’accord résultats/solutions. Les preuves visuelles seront ajoutées après compilation et contrôle mobile autorisés par l’orchestrateur.
'''
        (d/'RAPPORT.md').write_text(report,encoding='utf-8')
        coverage=['# Couverture des sources et du programme','',f'{len(DATA[c])} exercices, {sum(len(e["questions"]) for e in DATA[c])} questions.','']
        for i,e in enumerate(DATA[c],1):coverage.append(f'- Source {i} « {source["exercices"][i-1]["titre"]} » → nouveau-{i} « {e["titre"]} », {len(e["questions"])} questions : {source["exercices"][i-1]["methode"]}')
        if c==5:coverage.append('\nLe codage de déplacements est ajouté comme sixième question du dernier exercice, avec un plan quadrillé. Les programmes gardent deux instructions.')
        (d/'COUVERTURE.md').write_text('\n'.join(coverage)+'\n',encoding='utf-8')
        print(d.name,len(DATA[c]),sum(len(e['questions']) for e in DATA[c]),'questions',len(FIGURES[c]),'figures')

if __name__=='__main__':rediger()







