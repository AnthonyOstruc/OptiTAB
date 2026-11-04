# -*- coding: utf-8 -*-
"""Rédaction locale du lot CM2 nombres. Ne contacte aucune base de données."""
from pathlib import Path
from fractions import Fraction
import json, re, shutil

ROOT=Path(__file__).resolve().parent.parent
SLUGS=['01_grands-nombres','02_multiples-diviseurs','03_fractions','04_comparer-fractions','05_fraction-quantite','06_decimaux']
MARK='<!-- optitab:1 -->'
def write(p,s): p.write_text(s.rstrip()+'\n',encoding='utf-8')
def jwrite(p,v): write(p,json.dumps(v,ensure_ascii=False,indent=2))
def N(n): return f'{n:,}'.replace(',',r'\,')
def F(a,b): return rf'\frac{{{a}}}{{{b}}}'
def D(v): return str(v).replace('.',r'{,}')
def box(kind,text,title=''): return f'::: {kind} {title}\n{text}\n:::\n'
def q(s,m,e,r,check=None): return dict(s=s,m=m,e=e,r=r,check=check or [])
def test(expr,expected): return [expr,expected]
def calc(expr): return eval(expr,{'__builtins__':{}},{'Fraction':Fraction,'range':range,'sorted':sorted,'set':set,'list':list,'min':min,'max':max,'len':len,'sum':sum,'int':int,'str':str})
def dump_value(v):
    if isinstance(v,Fraction): return v.numerator if v.denominator==1 else [v.numerator,v.denominator]
    if isinstance(v,(list,tuple)): return [dump_value(x) for x in v]
    return v

COURSES={
0:('Les grands nombres entiers',r'''::: objectifs
- Lire et écrire les entiers jusqu’à $999\,999\,999$.
- Expliquer la valeur d’un chiffre et changer d’unité de numération.
- Comparer, ranger, encadrer et repérer ces nombres.
:::

## I. Lire et écrire par classes

::: definition Chiffre, rang et classe
Un chiffre est l’un des symboles 0 à 9. Les nombres sont écrits avec ces chiffres. Leur valeur dépend de leur position. Une classe réunit trois rangs : centaines, dizaines, unités. Au CM2, on utilise les classes des unités, des milliers et des millions.
:::

| Millions | Milliers | Unités |
|---|---|---|
| 206 | 045 | 018 |

$206\,045\,018$ se lit « deux-cent-six-millions-quarante-cinq-mille-dix-huit ». Une classe nulle ne se prononce pas. Dans une classe intérieure, on garde les zéros : $45\,018$ et $450\,018$ sont différents.

::: methode Écrire un nombre dicté
Préparer trois groupes de trois cases. Placer chaque classe à son rang ; compléter ses places vides par des zéros. Retirer seulement les zéros inutiles à gauche du nombre.
:::

::: exemple
« Sept-millions-huit-mille-trente » donne les classes $7\mid008\mid030$, donc $7\,008\,030$.
:::

## II. Comprendre la position

::: propriete Regrouper
Dix unités d’un rang forment une unité du rang situé juste à gauche. Mille milliers forment un million.
$$1\,000\,000=1\,000\times1\,000$$
:::

Dans $206\,045\,018$, le chiffre des dizaines de milliers est 4. Sa valeur est $40\,000$. Le nombre de milliers entiers est $206\,045$ : il faut aussi compter ceux contenus dans les millions.

::: exemple Décomposer
$$\begin{aligned}
206\,045\,018&=206\,000\,000+45\,000+18\\
&=200\,000\,000+6\,000\,000\\
&\quad+40\,000+5\,000+10+8
\end{aligned}$$
On peut aussi écrire $206\,045$ milliers et 18 unités.
:::

::: attention Chiffre et nombre de groupes
Le chiffre des milliers de $52\,406$ est 2 ; ce nombre contient 52 milliers entiers. Le chiffre et le nombre de milliers ne répondent pas à la même question.
:::

## III. Comparer, ranger et encadrer

::: methode Comparer deux entiers
Un entier qui a davantage de chiffres est plus grand. À nombre de chiffres égal, lire de gauche à droite : le premier chiffre différent décide de l’ordre.
:::

::: exemple
$42\,907\,105<42\,970\,015$ : les classes des millions sont égales, mais $907<970$ dans celle des milliers. Ranger dans l’ordre croissant signifie aller du plus petit au plus grand.
:::

Encadrer $6\,472\,850$ au million donne $6\,000\,000<6\,472\,850<7\,000\,000$. Intercaler, c’est choisir un nombre entre deux bornes ; par exemple $6\,500\,000$ entre $6\,472\,850$ et $7\,000\,000$.

## IV. Lire une graduation

::: methode Trouver la valeur d’un pas
Calculer l’écart entre deux graduations connues, puis le partager par le nombre d’intervalles qui les séparent. Compter les intervalles, et non les traits.
:::

[IMAGE_1]

::: exemple
De $3\,000\,000$ à $4\,000\,000$, il y a cinq intervalles : un pas vaut $200\,000$. Le point $A$, placé au troisième pas après $3\,000\,000$, repère $3\,600\,000$.
:::

::: retenir
Je garde les zéros de position, je distingue chiffre et nombre de groupes, puis je justifie comparaison et placement à partir des rangs ou du pas.
:::
'''),
1:('Multiples et diviseurs',r'''::: objectifs
- Relier une multiplication aux mots multiple et diviseur.
- Utiliser les critères de divisibilité par 2, 5 et 10.
- Organiser une recherche de diviseurs ou de multiples communs.
:::

## I. Une multiplication, deux lectures

::: definition
Si $24=6\times4$, 24 est un **multiple de 6** et 6 est un **diviseur de 24**. On dit aussi que 24 est divisible par 6 : le partage en groupes de 6 ne laisse aucun reste. Ici, 4 est également un diviseur de 24.
:::

[IMAGE_1]

::: exemple
$35=5\times7$ : 35 est multiple de 5 et de 7. En revanche $37=5\times7+2$ : 37 n’est pas un multiple de 5.
:::

::: attention Le sens des mots
« 6 est un diviseur de 24 » n’est pas « 6 est un multiple de 24 ». Le nombre 0 est un multiple de tout entier positif ; on ne divise jamais par 0.
:::

## II. Reconnaître certains multiples

::: propriete Trois critères
Un entier est divisible par :
- 2 si son chiffre des unités est 0, 2, 4, 6 ou 8 ;
- 5 si son chiffre des unités est 0 ou 5 ;
- 10 si son chiffre des unités est 0.
:::

::: exemple
270 est divisible par 2, 5 et 10. 275 est divisible par 5, mais pas par 2 ni par 10. Pour 3, 4, 6, 7, 8 ou 9, on utilise les tables ou un calcul de multiplication ou de division : aucun autre critère n’est nécessaire ici.
:::

## III. Trouver des diviseurs

::: methode Chercher par paires
Tester les nombres dans l’ordre et écrire les produits qui donnent le nombre cherché. Pour trouver tous les diviseurs d’un entier jusqu’à 30, poursuivre jusqu’à ce que les paires se répètent.
:::

::: exemple Tous les diviseurs de 24
$$24=1\times24=2\times12=3\times8=4\times6$$
Le test de 5 ne convient pas. En arrivant à 6, on retrouve la paire $4\times6$. Les diviseurs sont donc 1, 2, 3, 4, 6, 8, 12 et 24. Un nombre a toujours 1 et lui-même comme diviseurs.
:::

Pour un nombre jusqu’à 100, on peut aussi demander seulement **quelques** diviseurs : $72=8\times9$ donne déjà 1, 8, 9 et 72.

## IV. Chercher ce qui est commun

::: definition Diviseurs communs
Un diviseur commun à deux entiers divise chacun d’eux sans reste. Les diviseurs de 12 sont 1, 2, 3, 4, 6, 12 ; ceux de 18 sont 1, 2, 3, 6, 9, 18. Leurs diviseurs communs sont 1, 2, 3 et 6.
:::

::: methode Multiples communs
Écrire les multiples de chacun des deux nombres dans la zone demandée. Retenir les nombres présents dans les deux listes. Pour 4 et 6, les multiples positifs communs jusqu’à 30 sont 12 et 24.
:::

::: exemple Donner du sens
Pour disposer 24 cartes en lignes complètes de même longueur, les nombres de cartes par ligne sont les diviseurs de 24. Pour trouver une longueur réalisable avec des baguettes de 4 cm ou avec des baguettes de 6 cm, on cherche un multiple commun de 4 et de 6.
:::

::: retenir
Une réponse se justifie par une multiplication ou une division sans reste. Pour affirmer « tous », il faut expliquer comment la recherche est complète.
:::
'''),
2:('Les fractions, du tout au nombre',r'''::: objectifs
- Lire et représenter une fraction à partir d’une unité.
- Passer entre fraction et entier plus fraction.
- Encadrer une fraction et la repérer sur une demi-droite.
:::

## I. Une unité partagée en parts égales

::: definition Numérateur et dénominateur
Dans $\frac58$, le dénominateur 8 indique qu’une unité est partagée en huit parts égales ; le numérateur 5 compte cinq de ces parts. On lit « cinq huitièmes ». Le dénominateur n’est jamais nul.
:::

[IMAGE_1]

::: attention Choisir la même unité
Des parts doivent être égales **dans la même unité**. Cinq morceaux de tailles différentes ne représentent pas forcément cinq huitièmes. Une fraction peut désigner une longueur, une aire ou un nombre.
:::

::: propriete Compter des fractions de l’unité
$$\frac58=5\times\frac18\qquad\frac88=1\qquad\frac{16}8=2$$
Une fraction est inférieure à 1 si son numérateur est inférieur à son dénominateur ; elle vaut 1 s’ils sont égaux ; elle dépasse 1 si le numérateur est plus grand.
:::

## II. Dépasser une unité

::: methode Regrouper les parts
Pour écrire $\frac{19}6$ comme entier plus fraction, chercher combien de groupes de 6 tiennent dans 19. $19=3\times6+1$ : il y a trois unités et un sixième restant.
$$\frac{19}6=3+\frac16$$
La fraction restante doit être inférieure à 1.
:::

::: exemple Revenir à une fraction
$$2+\frac56=\frac{12}6+\frac56=\frac{17}6$$
Les deux unités apportent douze sixièmes, auxquels on ajoute cinq sixièmes.
:::

::: attention Conserver la valeur
$2+\frac56$ ne vaut pas $\frac76$ : l’entier 2 représente douze sixièmes, pas deux sixièmes.
:::

## III. Encadrer entre deux entiers

::: methode Utiliser les multiples
Pour encadrer $\frac{23}5$, repérer $20=4\times5$ et $25=5\times5$. Comme $20<23<25$, on obtient :
$$4<\frac{23}5<5$$
:::

Si la fraction est un entier, on le dit directement : $\frac{24}6=4$. Un encadrement qui l’inclut peut s’écrire $4\le\frac{24}6<5$.

## IV. Un nombre sur une demi-droite

::: methode Placer et lire
Repérer l’intervalle de 0 à 1. Compter ses parts égales pour connaître le dénominateur. Partir de 0 et compter les petits pas pour connaître le numérateur. Le même pas est conservé après 1.
:::

[IMAGE_2]

::: exemple
Chaque unité est divisée en 6. Le point $A$ est au dix-neuvième pas depuis 0 : son abscisse est $\frac{19}6=3+\frac16$. Pour placer $2+\frac56$, on avance de cinq pas après l’entier 2.
:::

::: retenir
Le dénominateur indique la taille d’un pas, le numérateur le nombre de pas. Une fraction est un nombre ; elle peut être plus grande qu’une unité.
:::
'''),
3:('Comparer et calculer avec des fractions',r'''::: objectifs
- Reconnaître des fractions égales et justifier une comparaison.
- Choisir un même dénominateur dans les cas simples.
- Additionner et soustraire des fractions compatibles avec le programme du CM2.
:::

## I. Plusieurs écritures d’un même nombre

::: propriete Agrandir le partage
Partager chaque part en un même nombre de parts plus petites ne change pas la quantité représentée. On multiplie donc le numérateur **et** le dénominateur par le même entier positif.
$$\frac34=\frac68=\frac9{12}$$
:::

[IMAGE_1]

::: exemple
Chaque quart est partagé en deux huitièmes. Trois quarts représentent six huitièmes. Réciproquement, regrouper les huitièmes deux par deux permet de retrouver les quarts.
:::

## II. Choisir une comparaison simple

::: methode Même dénominateur
Les parts ont la même taille : comparer leur nombre. Ainsi $\frac58<\frac78$ puisque $5<7$.
:::

::: methode Même numérateur
À nombre de parts égal, les plus petites parts donnent la plus petite quantité. Ainsi $\frac35>\frac38$ : un cinquième est plus grand qu’un huitième, pour une même unité.
:::

::: methode Comparer à une unité
$\frac78<1$ et $\frac98>1$, donc $\frac78<\frac98$. Il est inutile de transformer ces fractions.
:::

## III. Mettre au même dénominateur

::: methode Un partage commun
Chercher un multiple commun des dénominateurs, au plus égal à 60 dans les comparaisons du CM2. Transformer chaque fraction en expliquant le nouveau partage, puis comparer les numérateurs.
:::

::: exemple
Pour comparer $\frac34$ et $\frac7{10}$, on choisit les vingtièmes.
$$\frac34=\frac{15}{20}\qquad\frac7{10}=\frac{14}{20}$$
Donc $\frac34>\frac7{10}$.
:::

::: attention Une erreur fréquente
Un dénominateur plus grand ne donne pas toujours une fraction plus grande. Il faut tenir compte du numérateur et de la taille des parts. On n’ajoute pas le même entier en haut et en bas pour obtenir une fraction égale.
:::

## IV. Ajouter et retirer des parts

::: propriete Même taille de parts
Pour additionner ou soustraire des fractions de même dénominateur, on additionne ou soustrait les numérateurs et on garde le dénominateur.
$$\frac38+\frac28=\frac58\qquad\frac78-\frac38=\frac48=\frac12$$
:::

::: methode Un dénominateur multiple de l’autre
Avant le calcul, écrire les deux fractions avec le plus grand des deux dénominateurs. Au CM2, ces changements utilisent les tables de multiplication.
:::

::: exemple
Un demi vaut quatre huitièmes, donc :
$$\frac12+\frac38=\frac48+\frac38=\frac78$$
De même $\frac56-\frac1{12}=\frac{10}{12}-\frac1{12}=\frac9{12}$.
:::

::: retenir
Je cherche d’abord le moyen le plus simple de comparer. Pour calculer une somme ou une différence, je compte des parts de même taille et je vérifie si le résultat est plausible.
:::
'''),
4:('Prendre une fraction d’une quantité',r'''::: objectifs
- Identifier le tout auquel une fraction se rapporte.
- Déterminer une fraction d’une quantité ou d’une grandeur.
- Relier le produit d’un entier et d’une fraction à une addition répétée.
:::

## I. Le tout et les parts

::: definition Une fraction d’une quantité
Prendre $\frac35$ de 40 jetons, c’est partager les **40 jetons** en 5 groupes égaux, puis prendre 3 de ces groupes. La fraction se rapporte au total de départ.
:::

[IMAGE_1]

::: methode Partager puis multiplier
1. Identifier la quantité totale et son unité.
2. Diviser cette quantité par le dénominateur : on obtient une part.
3. Multiplier une part par le numérateur : on obtient la quantité cherchée.
:::

::: exemple
$$\begin{aligned}
40\div5&=8\\
8\times3&=24
\end{aligned}$$
Trois cinquièmes de 40 jetons font 24 jetons.
:::

## II. Mesurer une fraction de grandeur

::: exemple Une longueur
Pour parcourir $\frac34$ d’un trajet de 100 m : $100\div4=25$, puis $25\times3=75$. La distance parcourue est 75 m.
:::

::: exemple Une masse
Pour utiliser $\frac3{10}$ de 500 g : $500\div10=50$, puis $50\times3=150$. On utilise 150 g.
:::

::: attention Garder le sens et l’unité
$\frac34$ est un nombre ; les 75 m sont une longueur. On ne répond pas « 75 quarts ». Si l’on prend une fraction inférieure à 1 d’une quantité positive, on obtient une quantité plus petite que le tout.
:::

## III. Ce qui reste ou ce qui manque

::: methode Relier les parties au tout
Après avoir calculé la partie utilisée, la soustraire au total. On peut aussi calculer directement la fraction complémentaire quand les parts sont les mêmes.
:::

::: exemple
On utilise $\frac35$ de 40 jetons, soit 24 jetons. Il reste $40-24=16$ jetons. Cela représente les $\frac25$ du total, car cinq cinquièmes moins trois cinquièmes donnent deux cinquièmes.
:::

::: attention Deux touts différents
La moitié de 20 vaut 10 et le tiers de 36 vaut 12. Une fraction plus grande peut donner une quantité plus petite si les quantités de départ diffèrent.
:::

## IV. Répéter une fraction

::: propriete Produit d’un entier et d’une fraction
Multiplier une fraction par un entier revient à additionner cette fraction autant de fois.
$$3\times\frac54=\frac54+\frac54+\frac54=\frac{15}4$$
Le dénominateur est conservé : on compte toujours des quarts.
:::

::: exemple Une longueur répétée
Trois bandes mesurent chacune $\frac54$ m. Mises bout à bout, elles mesurent $\frac{15}4$ m, soit $3+\frac34$ m.
:::

## V. Retrouver le tout dans un cas simple

::: methode Remonter des parts à la quantité entière
Si les $\frac35$ d’un stock représentent 24 objets, trois parts valent 24 objets. Une part vaut $24\div3=8$ objets. Le tout contient cinq parts, soit $8\times5=40$ objets. Vérifier ensuite les trois cinquièmes du total retrouvé.
:::

::: retenir
« Une fraction de » demande de préciser le tout. « Trois fois une fraction » demande de répéter cette fraction. Dans les deux cas, j’explique le sens du calcul avant de calculer.
:::
'''),
5:('Les nombres décimaux jusqu’aux millièmes',r'''::: objectifs
- Relier fractions décimales, décompositions et écriture à virgule.
- Lire la valeur des chiffres jusqu’aux millièmes.
- Comparer, ranger, intercaler et repérer ; arrondir à l’entier.
:::

## I. Des parts de plus en plus petites

::: definition Fractions décimales
Une fraction décimale a pour dénominateur 10, 100, 1 000, etc. Au CM2, on travaille jusqu’aux millièmes. Une unité vaut 10 dixièmes, 100 centièmes ou 1 000 millièmes.
$$1=\frac{10}{10}=\frac{100}{100}=\frac{1\,000}{1\,000}$$
$$\frac1{10}=\frac{10}{100}=\frac{100}{1\,000}\qquad\frac1{100}=\frac{10}{1\,000}$$
:::

## II. Coder par une virgule

::: definition Écriture décimale
La virgule sépare la partie entière des chiffres des dixièmes, centièmes et millièmes. Chaque rang vaut dix fois le rang situé juste à sa droite.
:::

Dans le nombre $4{,}207$ :

| Rang | Chiffre | Contribution |
|---|---|---|
| Unités | 4 | $4$ |
| Dixièmes | 2 | $\frac2{10}$ |
| Centièmes | 0 | $0$ |
| Millièmes | 7 | $\frac7{1\,000}$ |

::: exemple Trois écritures
$$\begin{aligned}
4{,}207&=\frac{4\,207}{1\,000}\\
&=4+\frac{207}{1\,000}\\
&=4+\frac2{10}+\frac7{1\,000}
\end{aligned}$$
On peut lire « quatre unités et deux-cent-sept millièmes ». Le zéro des centièmes garde la place : $4{,}207$ est différent de $4{,}27$.
:::

::: propriete Zéros finaux
Ajouter ou retirer un zéro **à la fin de la partie décimale** ne change pas le nombre : $3{,}5=3{,}50=3{,}500$. On ne peut pas retirer un zéro situé entre deux chiffres.
:::

## III. Comparer et intercaler

::: methode Comparer rang par rang
Comparer les parties entières, puis les dixièmes, les centièmes et les millièmes si nécessaire. Des zéros finaux peuvent aider à aligner les rangs.
:::

::: exemple
$5{,}8=5{,}800>5{,}79=5{,}790$. Le nombre qui a le plus de chiffres après la virgule n’est pas forcément le plus grand. On peut intercaler $5{,}795$ entre $5{,}79$ et $5{,}8$.
:::

Encadrer $4{,}207$ entre deux entiers donne $4<4{,}207<5$. Entre deux dixièmes consécutifs : $4{,}2<4{,}207<4{,}3$.

## IV. Lire une graduation

[IMAGE_1]

::: methode Déterminer le pas
Entre $4{,}20$ et $4{,}30$, dix intervalles représentent dix centièmes : un pas vaut $0{,}01$. Le point $A$ au troisième pas après $4{,}20$ repère $4{,}23$, soit $\frac{423}{100}$.
:::

## V. Partie entière et arrondi

::: definition
La partie entière de $7{,}682$ est 7. Son arrondi à l’entier est l’entier le plus proche, ici 8. Quand le nombre est exactement à mi-chemin, on choisit l’entier supérieur : $7{,}5$ s’arrondit à 8.
:::

::: methode Observer les dixièmes
Si le chiffre des dixièmes est inférieur à 5, garder la partie entière. S’il est au moins égal à 5, choisir l’entier suivant. Ainsi $12{,}499$ s’arrondit à 12 et $12{,}501$ à 13.
:::

::: retenir
Un nombre décimal est un seul nombre. Je compare les rangs et je conserve les zéros de position ; je distingue sa partie entière et son arrondi.
:::
''')}

FICHES={
0:r'''::: retenir
Trois classes au CM2 : **millions | milliers | unités**, trois chiffres dans chaque classe intérieure. Maximum étudié : $999\,999\,999$.
:::
## I. Lire et décomposer
$7\,008\,030$ : sept-millions-huit-mille-trente.
$$7\,008\,030=7\,000\,000+8\,000+30$$
::: methode
Un rang vers la gauche vaut 10 fois plus. Mille milliers font un million. Dans $52\,406$, chiffre des milliers : 2 ; nombre de milliers entiers : 52.
:::
## II. Comparer et repérer
Comparer le nombre de chiffres, puis le premier rang différent depuis la gauche. Croissant : du plus petit au plus grand.
$$6\,000\,000<6\,472\,850<7\,000\,000$$
Sur une droite : **pas = écart connu ÷ nombre d’intervalles**.
::: attention
Garder les zéros entre les chiffres et dans les classes intérieures. Compter les intervalles, pas les traits.
:::
''',
1:r'''::: retenir
$24=6\times4$ : 24 est multiple de 6 ; 6 est diviseur de 24. Le partage ne laisse aucun reste.
:::
## I. Reconnaître
| Divisible par | Chiffre des unités |
|---|---|
| 2 | 0, 2, 4, 6, 8 |
| 5 | 0 ou 5 |
| 10 | 0 |
Pour les autres diviseurs, utiliser les tables ou calculer.
## II. Chercher
::: methode
Écrire les paires de facteurs : $24=1\times24=2\times12=3\times8=4\times6$. Rechercher dans l’ordre pour ne pas oublier de diviseur.
:::
**Diviseurs communs** : diviseurs présents dans les deux listes. **Multiples communs** : nombres présents dans les deux suites de multiples.
::: attention
« Tous » exige une recherche complète. 1 divise tout entier positif. On ne divise pas par 0. Préciser « positif » si 0 est exclu des multiples cherchés.
:::
''',
2:r'''::: retenir
Dans $\frac58$, 8 partage l’unité en parts égales et 5 compte les parts. Une fraction est un nombre.
:::
## I. Une unité ou davantage
$$\frac88=1\qquad\frac{19}6=3+\frac16$$
::: methode
Regrouper les parts par paquets du dénominateur. Inversement, transformer chaque entier en fractions de ce dénominateur : $2+\frac56=\frac{17}6$.
:::
## II. Encadrer et placer
$20<23<25$ donne $4<\frac{23}5<5$.
::: methode
Sur une droite, compter les intervalles entre 0 et 1 pour connaître le dénominateur. Compter ensuite les petits pas depuis 0 pour connaître le numérateur.
:::
::: attention
Les parts doivent être égales. La fraction restante dans « entier plus fraction » est inférieure à 1. Le pas ne change pas après 1.
:::
''',
3:r'''::: retenir
Multiplier le numérateur et le dénominateur par le **même entier positif** conserve la valeur : $\frac34=\frac68$.
:::
## I. Comparer
- Même dénominateur : comparer les numérateurs.
- Même numérateur positif : le plus petit dénominateur donne la plus grande fraction.
- Sinon : comparer à 1 ou chercher un dénominateur commun simple, au plus 60.
$$\frac34=\frac{15}{20}>\frac{14}{20}=\frac7{10}$$
## II. Ajouter ou soustraire
::: methode
Compter des parts de même taille. Si l’un des dénominateurs est multiple de l’autre, transformer d’abord une fraction avec les tables.
$$\frac12+\frac38=\frac48+\frac38=\frac78$$
:::
::: attention
On garde le dénominateur dans une somme de parts de même taille. On ne l’additionne pas aux autres dénominateurs.
:::
''',
4:r'''::: retenir
Pour prendre $\frac35$ de 40 jetons, le tout est **40 jetons**.
:::
## I. Fraction d’une quantité
::: methode
Partager par le dénominateur, puis multiplier par le numérateur.
$$40\div5=8\qquad8\times3=24$$
Les $\frac35$ de 40 jetons font 24 jetons. Il reste $40-24=16$ jetons.
:::
## II. Répéter une fraction
$$3\times\frac54=\frac54+\frac54+\frac54=\frac{15}4$$
::: attention
Identifier le tout et garder l’unité dans la réponse. Une fraction inférieure à 1 d’une quantité positive est plus petite que le tout. Avec deux touts différents, comparer les quantités obtenues, pas seulement les fractions.
:::
''',
5:r'''::: retenir
$1=\frac{10}{10}=\frac{100}{100}=\frac{1\,000}{1\,000}$.
Un dixième vaut 10 centièmes ; un centième vaut 10 millièmes.
:::
## I. Lire et écrire
$$4{,}207=4+\frac2{10}+\frac7{1\,000}=\frac{4\,207}{1\,000}$$
Les rangs après la virgule sont : dixièmes, centièmes, millièmes.
## II. Comparer et repérer
::: methode
Comparer les parties entières puis les rangs décimaux. $5{,}8=5{,}800>5{,}790=5{,}79$. Sur une droite, calculer la valeur d’un intervalle avant de compter les pas.
:::
## III. Arrondir à l’entier
Partie entière de $7{,}682$ : 7. Arrondi à l’entier : 8. Observer les dixièmes : de 0 à 4, garder la partie entière ; de 5 à 9, prendre l’entier suivant.
::: attention
$3{,}5=3{,}50$, mais $3{,}05\ne3{,}5$. Un zéro final se retire ; un zéro de position se conserve.
:::
'''}

def exercise(i,family,qs,level,title,context=''):
    prefix=['Découverte','Entraînement','Problème'][level]
    out=f'=== {prefix} - {title}\nId: nouveau-{i}\nDifficulté: '+['easy','medium','hard'][level]+'\n\nÉnoncé:\n'+MARK+'\n'
    if context: out+=context+'\n\n'
    out+='\n'.join(f'{k}. {v["s"]}' for k,v in enumerate(qs,1))+'\n\nÉtapes:\n'+MARK+'\n'
    for k,v in enumerate(qs,1):
        out+=f'\n## Question {k} : '+['Comprendre et répondre','Expliquer le raisonnement','Vérifier et conclure','Chercher et justifier'][k-1]+'\n\n'
        out+=box('methode',v['m'])+'\n'+box('etape',v['e'],'Raisonner avec les données')+'\n'+box('resultat',v['r'])
    out+='\nSolution:\n'+MARK+'\n'+'\n'.join(f'{k}. {v["r"]}' for k,v in enumerate(qs,1))+'\n'
    return out,{'id':f'nouveau-{i}','famille':family,'niveau':level+1,'titre':title,'questions':qs}

def grands(level,fam):
    if fam==0:
        n=[7008030,206045018,890006040][level]
        names=['sept-millions-huit-mille-trente','deux-cent-six-millions-quarante-cinq-mille-dix-huit','huit-cent-quatre-vingt-dix-millions-six-mille-quarante'][level]
        classes=[n//1000000,(n//1000)%1000,n%1000]
        return ['La dictée des trois classes','Les classes avec des zéros','Retrouver une écriture effacée'][level], [
            q(f'Écrire en chiffres « {names} ».','Séparer les classes et garder trois chiffres dans les classes intérieures.',f'Les classes millions, milliers, unités sont {classes[0]}, {classes[1]:03d}, {classes[2]:03d}. Les zéros occupent les rangs non prononcés.',f'${N(n)}$.',[test(f'{classes[0]}*1000000+{classes[1]}*1000+{classes[2]}',n)]),
            q(f'Lire ${N(n)}$ en nommant les classes.','Lire de gauche à droite et omettre les classes nulles.',f'La classe de gauche compte {classes[0]} millions. On lit ensuite {classes[1]} milliers puis {classes[2]} unités, sans prononcer les zéros de position.',f'« {names} ».'),
            q(f'Peut-on supprimer les zéros de la classe des milliers ? Expliquer.','Comparer la valeur des rangs avant toute suppression.',f'Cette classe s’écrit {classes[1]:03d} sur trois rangs. Enlever un zéro intérieur déplacerait les chiffres ; les espaces de classes ne sont pas des chiffres.', 'Non : ces zéros gardent les positions des chiffres.')]
    if fam==1:
        n=[52406,406072018,808080808][level]; rank=[1000,10000,1000000][level]; digit=n//rank%10; groups=n//rank
        label=['milliers','dizaines de milliers','millions'][level]
        return ['Trois questions sur le chiffre 2','Le rang qui change tout','Les huit n’ont pas la même valeur'][level],[
            q(f'Dans ${N(n)}$, quel est le chiffre des {label} ?','Partir des unités et compter les rangs.',f'Un groupe du rang demandé vaut ${N(rank)}$. Le chiffre qui occupe cette position est {digit}.',f'Le chiffre est {digit}.',[test(f'{n}//{rank}%10',digit)]),
            q('Quelle est sa contribution au nombre ?','Multiplier le chiffre par la valeur de son rang.',f'${digit}\\times {N(rank)}={N(digit*rank)}$.',f'${N(digit*rank)}$.',[test(f'{digit}*{rank}',digit*rank)]),
            q(f'Combien de {label} entiers ce nombre contient-il ?','Compter tous les groupes complets, y compris ceux des rangs supérieurs.',f'Le partage de ${N(n)}$ par ${N(rank)}$ donne ${N(groups)}$ groupes complets et un reste de ${N(n%rank)}$. Ce reste est plus petit que ${N(rank)}$.',f'{N(groups)} groupes complets.'.replace(r'\,',' '),[test(f'[{n}//{rank},{n}%{rank}]',[groups,n%rank])])]
    if fam==2:
        a,b,c=[(12,345,6),(206,45,18),(490,1008,75)][level]; n=a*1000000+b*1000+c
        return ['Assembler trois classes','Deux décompositions du même nombre','Une classe à regrouper'][level],[
            q(f'Écrire le nombre formé de {a} millions, {b} milliers et {c} unités.','Additionner les contributions, avec échange si une classe dépasse 999.',f'${N(a*1000000)}+{N(b*1000)}+{c}={N(n)}$.',f'${N(n)}$.',[test(f'{a}*1000000+{b}*1000+{c}',n)]),
            q('Écrire ce nombre en milliers entiers et unités restantes.','Un million contient mille milliers.',f'${a}\\times1\\,000+{b}={N(n//1000)}$ milliers, puis {c} unités.',f'{n//1000:,} milliers et {c} unités.'.replace(',',' '),[test(f'{a}*1000+{b}',n//1000)]),
            q(f'L’écriture « {n//1000-1} milliers et {c+1000} unités » convient-elle ?','Échanger un millier contre mille unités.',f'On a retiré un millier et ajouté 1 000 unités. Le calcul donne encore ${N((n//1000-1)*1000+c+1000)}$.','Oui, les deux écritures ont la même valeur.',[test(f'({n//1000}-1)*1000+{c+1000}',n)])]
    if fam==3:
        vals=[[3405200,3450200,3405020,3400520,3450020],[42907105,42970015,42907051,42970150,42971005],[908090800,908098000,908008900,908080900,980008900]][level]; s=sorted(vals)
        return ['Des étiquettes à ranger','Le premier rang différent','Classer sans confondre les zéros'][level],[
            q('Ranger les cinq nombres dans l’ordre croissant.','Comparer les classes, puis le premier chiffre différent.', 'Les classes les plus à gauche départagent d’abord les nombres. À égalité, on poursuit vers la droite sans ignorer les zéros.', 'Ordre croissant : '+', '.join('$'+N(x)+'$' for x in s)+'.',[test(f'sorted({vals})',s)]),
            q('Donner le plus grand et le plus petit.','Lire les deux extrémités du rangement.',f'Le premier est le plus petit, ${N(s[0])}$ ; le dernier est le plus grand, ${N(s[-1])}$.',f'Minimum : ${N(s[0])}$ ; maximum : ${N(s[-1])}$.',[test(f'[min({vals}),max({vals})]',[s[0],s[-1]])]),
            q('Proposer un entier strictement entre les deux plus petits.','Ajouter 1 au plus petit et vérifier la seconde borne.',f'${N(s[0])}<{N(s[0]+1)}<{N(s[1])}$.',f'Par exemple ${N(s[0]+1)}$.',[test(f'{s[0]}<{s[0]+1}<{s[1]}',True)])], 'Les étiquettes portent : '+', '.join('$'+N(x)+'$' for x in vals)+'.'
    if fam==4:
        n,step=[(6472850,1000000),(203047018,10000),(899999999,1000000)][level]; lo=n//step*step; hi=lo+step
        return ['Entre deux millions','Encadrer au bon rang','À la frontière d’une classe'][level],[
            q(f'Encadrer ${N(n)}$ entre deux multiples consécutifs de ${N(step)}$.','Trouver le multiple juste avant et celui juste après.',f'${N(lo)}$ précède le nombre et le multiple suivant est ${N(lo)}+{N(step)}={N(hi)}$.',f'${N(lo)}<{N(n)}<{N(hi)}$.',[test(f'{lo}<{n}<{hi} and {hi}-{lo}=={step}',True)]),
            q('Quel entier vient immédiatement avant le nombre étudié ?','Soustraire une unité, avec les échanges nécessaires.',f'${N(n)}-1={N(n-1)}$.',f'${N(n-1)}$.',[test(f'{n}-1',n-1)]),
            q('Quel entier vient immédiatement après ?','Ajouter une unité et contrôler la retenue.',f'${N(n)}+1={N(n+1)}$.',f'${N(n+1)}$.',[test(f'{n}+1',n+1)])]
    if fam==5:
        start,step=[(3000000,200000),(42000000,50000),(208000000,250000)][level]; point=start+3*step
        return ['Cinq intervalles pour un million','Une fenêtre sur les millions','Retrouver une graduation intermédiaire'][level],[
            q('Calculer la valeur d’un petit intervalle.','Partager l’écart connu par cinq intervalles.',f'$({N(start+5*step)}-{N(start)})\\div5={N(step)}$.',f'Un pas vaut ${N(step)}$.',[test(f'({start+5*step}-{start})//5',step)]),
            q('Quelle abscisse porte le troisième trait après la première borne ?','Ajouter trois pas à la borne de départ.',f'${N(start)}+3\\times {N(step)}={N(point)}$.',f'${N(point)}$.',[test(f'{start}+3*{step}',point)]),
            q(f'Combien de pas séparent ${N(start+step)}$ de ${N(start+4*step)}$ ?','Calculer la différence puis la diviser par le pas.',f'$({N(start+4*step)}-{N(start+step)})\\div {N(step)}=3$.','3 pas.',[test(f'({start+4*step}-{start+step})//{step}',3)])],f'Une portion de droite va de ${N(start)}$ à ${N(start+5*step)}$ en cinq intervalles égaux.'
    total,size=[(123450,1000),(12342320,10000),(98765432,100000)][level]; count=total//size; rest=total%size
    return ['Les boîtes de boutons','Le stock de l’imprimerie','Le comptable corrige son tableau'][level],[
        q('Combien de paquets complets peut-on former ?','Compter les groupes entiers de la taille demandée.',f'${N(total)}={N(count)}\\times {N(size)}+{N(rest)}$.',f'{N(count)} paquets complets.'.replace(r'\,',' '),[test(f'{total}//{size}',count)]),
        q('Combien d’objets ne sont pas rangés dans un paquet complet ?','Retirer le contenu des paquets complets.',f'${N(total)}-{N(count*size)}={N(rest)}$.',f'{N(rest)} objets.'.replace(r'\,',' '),[test(f'{total}-{count}*{size}',rest)]),
        q('Un élève annonce un paquet de plus. Pourquoi est-ce impossible ?','Comparer le stock au nombre nécessaire.',f'${N(count+1)}$ paquets de ${N(size)}$ demanderaient ${N((count+1)*size)}$ objets. Ce total dépasse le stock de ${N(total)}$ objets.',f'Il manquerait {size-rest:,} objets.'.replace(',',' '),[test(f'({count}+1)*{size}-{total}',size-rest)])],f'On dispose de ${N(total)}$ objets à ranger par paquets de ${N(size)}$.'

def divs(n): return [d for d in range(1,n+1) if n%d==0]
def multiples(level,fam):
    if fam==0:
        n,d=[(24,6),(56,7),(72,8)][level]; k=n//d
        return ['Les mots de la multiplication','Le rangement sans reste','Une affirmation à retourner'][level],[
            q(f'Compléter ${n}={d}\\times\\ldots$.','Chercher dans la table ou partager sans reste.',f'La table de {d} donne ${d}\\times{k}={n}$.',f'Le nombre manquant est {k}.',[test(f'{d}*{k}',n)]),
            q(f'Écrire une phrase avec « multiple » puis « diviseur ».','Lire l’égalité dans les deux sens.',f'Le produit prouve que {n} est constitué de {k} groupes de {d}. Le partage est exact.',f'{n} est multiple de {d} ; {d} est diviseur de {n}.'),
            q(f'{n+1} est-il aussi un multiple de {d} ?','Chercher si un reste apparaît.',f'${n+1}={d}\\times{k}+1$. Le reste 1 est non nul et inférieur à {d}.','Non, le partage laisse un reste de 1.',[test(f'({n}+1)%{d}',1)])]
    if fam==1:
        nums=[[120,132,145],[275,270,282],[1340,1347,1355]][level]
        qs=[]
        for n,d in zip(nums,[10,5,2]):
            yes=n%d==0
            qs.append(q(f'{n} est-il divisible par {d} ? Justifier.','Observer le chiffre des unités avec le critère adapté.',f'Le chiffre des unités de {n} est {n%10}. Pour {d}, il doit être '+({10:'0',5:'0 ou 5',2:'0, 2, 4, 6 ou 8'}[d])+'.',f'Oui : ${n}={d}\\times{n//d}$.' if yes else 'Non.',[test(f'{n}%{d}==0',yes)]))
        return ['Trois chiffres des unités','Des critères à choisir','Des nombres longs, des tests courts'][level],qs
    if fam==2:
        n=[18,24,28][level]; ds=divs(n); pairs=[(a,n//a) for a in ds if a<=n//a]
        return ['Les rectangles de 18 carrés','Toutes les paires pour 24','La recherche complète pour 28'][level],[
            q(f'Trouver les paires de facteurs de {n}, sans répéter une paire inversée.','Tester les petits facteurs dans l’ordre.', 'Les produits possibles sont '+', '.join(f'${a}\\times{b}={n}$' for a,b in pairs)+'. On arrête quand les paires s’inversent.', '; '.join(f'{a} et {b}' for a,b in pairs)+'.',[test(f'[[d,{n}//d] for d in range(1,{n}+1) if {n}%d==0 and d<={n}//d]',[list(p) for p in pairs])]),
            q(f'En déduire tous les diviseurs de {n}.','Prendre les deux nombres de chaque paire, puis ranger.', 'Chaque facteur d’une paire divise le nombre. La recherche ordonnée ne laisse aucun petit facteur non testé.',', '.join(map(str,ds))+'.',[test(f'[d for d in range(1,{n}+1) if {n}%d==0]',ds)]),
            q('Combien de rectangles différents peut-on former, en confondant deux rectangles tournés ?','Une paire de dimensions donne un rectangle.',f'Il y a {len(pairs)} paires sans inversion, donc autant de rectangles.',f'{len(pairs)} rectangles.',[test(f'len([d for d in range(1,{n}+1) if {n}%d==0 and d<={n}//d])',len(pairs))])]
    if fam==3:
        a,b=[(12,18),(20,30),(24,30)][level]; common=sorted(set(divs(a))&set(divs(b)))
        return ['Des équipes de même taille','Deux collections à partager','Le plus grand groupe commun'][level],[
            q(f'Lister les diviseurs de {a}.','Chercher les produits par paires.',f'Les facteurs de {a} donnent : '+', '.join(map(str,divs(a)))+'.',', '.join(map(str,divs(a)))+'.',[test(f'[d for d in range(1,{a}+1) if {a}%d==0]',divs(a))]),
            q(f'Quels sont les diviseurs communs de {a} et {b} ?','Comparer avec la liste des diviseurs du second nombre.',f'Les diviseurs de {b} sont '+', '.join(map(str,divs(b)))+'. Les nombres présents dans les deux listes conviennent.',', '.join(map(str,common))+'.',[test(f'[d for d in range(1,31) if {a}%d==0 and {b}%d==0]',common)]),
            q('Quelle est la plus grande taille de groupe qui partage exactement les deux collections ?','Choisir le plus grand diviseur commun.',f'Le plus grand nombre retenu est {common[-1]}. On obtient {a//common[-1]} groupes pour la première collection et {b//common[-1]} pour la seconde.',f'{common[-1]} objets par groupe.',[test(f'max([d for d in range(1,31) if {a}%d==0 and {b}%d==0])',common[-1])])]
    if fam==4:
        a,b,limit=[(4,6,30),(6,8,60),(8,12,100)][level]; cs=[x for x in range(1,limit+1) if x%a==0 and x%b==0]
        return ['Deux tables se rencontrent','Les chemins de baguettes','Toutes les longueurs communes'][level],[
            q(f'Lister les multiples positifs de {a} jusqu’à {limit}.','Multiplier successivement par 1, 2, 3… sans dépasser la borne.',f'On avance de {a} à chaque fois.',', '.join(map(str,range(a,limit+1,a)))+'.',[test(f'list(range({a},{limit}+1,{a}))',list(range(a,limit+1,a)))]),
            q(f'Quels sont les multiples positifs communs à {a} et {b}, jusqu’à {limit} ?','Garder les nombres qui figurent dans les deux tables.',f'On teste aussi chaque multiple de {a} dans la table de {b}. Les valeurs communes sont '+', '.join(map(str,cs))+'.',', '.join(map(str,cs))+'.',[test(f'[x for x in range(1,{limit}+1) if x%{a}==0 and x%{b}==0]',cs)]),
            q('Pour la plus petite longueur commune, combien faut-il de baguettes de chaque sorte ?','Diviser cette longueur par celle d’une baguette.',f'La longueur {cs[0]} cm nécessite ${cs[0]}\\div{a}={cs[0]//a}$ baguettes ou ${cs[0]}\\div{b}={cs[0]//b}$ baguettes.',f'{cs[0]//a} baguettes de {a} cm ou {cs[0]//b} baguettes de {b} cm.',[test(f'[{cs[0]}//{a},{cs[0]}//{b}]',[cs[0]//a,cs[0]//b])])]
    if fam==5:
        n=[60,72,96][level]; ds=divs(n); selected=ds[:3]+ds[-3:]
        return ['Six diviseurs dans un stock de 60','Les boîtes de 72 perles','Choisir des conditionnements pour 96'][level],[
            q(f'Donner six diviseurs différents de {n}.','Utiliser trois paires de facteurs.',f'On peut utiliser les paires $1\\times{n}$, $2\\times{n//2}$ et $3\\times{n//3}$.',', '.join(map(str,selected))+'.',[test(f'[{n}%d for d in {selected}]',[0]*6)]),
            q(f'Peut-on ranger {n} objets en boîtes de 8 sans reste ?','Contrôler par une multiplication.',f'${n}=8\\times{n//8}+{n%8}$.',f'Oui : {n//8} boîtes.' if n%8==0 else f'Non : reste {n%8}.',[test(f'[{n}//8,{n}%8]',[n//8,n%8])]),
            q(f'Après l’ajout d’un objet, les boîtes de 2 conviennent-elles encore ?','Étudier la parité ou le reste.',f'{n+1} se termine par {(n+1)%10}, chiffre impair. Il reste un objet dans le partage par 2.','Non, il reste un objet.',[test(f'({n}+1)%2',1)])]
    lo,hi,d,e=[(20,40,5,2),(40,70,8,5),(60,100,9,2)][level]; poss=[x for x in range(lo,hi+1) if x%d==0 and x%e==0]
    return ['Le nombre caché des équipes','Un code entre 40 et 70','Un nombre sous trois contraintes'][level],[
        q(f'Lister les multiples de {d} compris entre {lo} et {hi}, bornes comprises.','Débuter au premier multiple dans l’intervalle.',f'On ajoute {d} à chaque étape sans sortir de l’intervalle.',', '.join(str(x) for x in range(lo,hi+1) if x%d==0)+'.',[test(f'[x for x in range({lo},{hi}+1) if x%{d}==0]',[x for x in range(lo,hi+1) if x%d==0])]),
        q(f'Garder ceux qui sont aussi multiples de {e}.','Tester le second partage sur chaque candidat.', 'Les candidats restants satisfont les deux conditions.',', '.join(map(str,poss))+'.',[test(f'[x for x in range({lo},{hi}+1) if x%{d}==0 and x%{e}==0]',poss)]),
        q(f'Le nombre caché est le plus grand candidat. Combien de groupes de {d} contient-il ?','Choisir le maximum puis effectuer le partage exact.',f'Le nombre est {max(poss)} et ${max(poss)}\\div{d}={max(poss)//d}$.',f'{max(poss)} ; {max(poss)//d} groupes.',[test(f'max({poss})//{d}',max(poss)//d)])]

def fractions(level,fam):
    if fam==0:
        a,b=[(5,8),(7,12),(17,24)][level]
        return ['La bande de huit parts','Des douzièmes à expliquer','Un dessin peut-il représenter dix-sept vingt-quatrièmes ?'][level],[
            q(f'Une unité est partagée en {b} parts égales, dont {a} sont colorées. Quelle fraction est colorée ?','Le dénominateur compte les parts de l’unité ; le numérateur compte celles choisies.',f'Il y a {b} parts dans le tout et {a} parts colorées.',f'${F(a,b)}$.',[test(f'Fraction({a},{b})',[a,b])]),
            q('Quelle fraction n’est pas colorée ?','Retirer les parts colorées du nombre total de parts.',f'${b}-{a}={b-a}$ parts restent sans couleur. Elles ont toujours la taille d’un {b}-ième.',f'${F(b-a,b)}$.',[test(f'{b}-{a}',b-a)]),
            q('La même réponse reste-t-elle valable si les morceaux ont des aires différentes ?','Vérifier la condition de parts égales.',f'Compter {a} morceaux sur {b} ne suffit pas quand leurs tailles diffèrent. Une fraction d’aire compte des parts de même aire.','Non : il faut des parts de même aire.')]
    if fam==1:
        a,b=[(11,4),(29,6),(58,7)][level]; whole,rest=a//b,a%b
        return ['Onze quarts à regrouper','Le rouleau de vingt-neuf sixièmes','Cinquante-huit septièmes sans dessin géant'][level],[
            q(f'Combien d’unités complètes contient ${F(a,b)}$ ?','Former des paquets du dénominateur.',f'${a}={whole}\\times{b}+{rest}$. Chaque paquet de {b} parts forme une unité.',f'{whole} unités complètes.',[test(f'{a}//{b}',whole)]),
            q('Écrire la fraction comme un entier plus une fraction inférieure à 1.','Garder les parts qui restent après les regroupements.',f'Les {whole} unités utilisent {whole*b} parts. Il reste ${a}-{whole*b}={rest}$ parts de taille ${F(1,b)}$.',f'${F(a,b)}={whole}+{F(rest,b)}$.',[test(f'Fraction({a},{b})=={whole}+Fraction({rest},{b})',True)]),
            q('Quelle distance manque-t-il pour atteindre l’entier suivant, en unité ?','Compléter le dernier groupe de parts.',f'Il faut ${b}-{rest}={b-rest}$ parts supplémentaires pour former l’unité suivante.',f'${F(b-rest,b)}$ unité.',[test(f'{whole+1}-Fraction({a},{b})',[b-rest,b])])]
    if fam==2:
        whole,a,b=[(2,3,5),(4,7,8),(8,11,12)][level]; n=whole*b+a
        return ['Une bande de deux unités et trois cinquièmes','L’étiquette en huitièmes','Reconstruire une grande fraction'][level],[
            q(f'Combien de {b}-ièmes représentent {whole} unités ?','Chaque unité contient le dénominateur en parts.',f'${whole}\\times{b}={whole*b}$.',f'{whole*b} parts.',[test(f'{whole}*{b}',whole*b)]),
            q(f'Écrire ${whole}+{F(a,b)}$ comme une seule fraction.','Ajouter aux parts des unités les parts restantes.',f'${whole*b}+{a}={n}$ parts ; le dénominateur reste {b}.',f'${F(n,b)}$.',[test(f'{whole}+Fraction({a},{b})',[n,b])]),
            q(f'L’écriture ${F(whole+a,b)}$ conviendrait-elle ? Expliquer.','Comparer le nombre de parts réellement apportées par les unités.',f'Elle ne compterait que ${whole}+{a}={whole+a}$ parts. Les {whole} unités en apportent déjà {whole*b}.', 'Non : il faut convertir les unités en parts avant d’ajouter.',[test(f'Fraction({whole+a},{b})!=Fraction({n},{b})',True)])]
    if fam==3:
        a,b=[(17,5),(43,8),(119,12)][level]; w=a//b; rest=a%b
        return ['Entre trois et quatre','Un encadrement en huitièmes','Les multiples voisins de 119'][level],[
            q(f'Donner les deux multiples de {b} qui encadrent {a} au plus près.','Chercher les produits voisins dans la table prolongée.',f'${w}\\times{b}={w*b}$ et ${w+1}\\times{b}={(w+1)*b}$.',f'${w*b}<{a}<{(w+1)*b}$.',[test(f'{w*b}<{a}<{(w+1)*b}',True)]),
            q(f'Encadrer ${F(a,b)}$ entre deux entiers consécutifs.','Chaque groupe du dénominateur représente une unité.',f'${F(w*b,b)}={w}$ et ${F((w+1)*b,b)}={w+1}$. La fraction est entre ces deux nombres.',f'${w}<{F(a,b)}<{w+1}$.',[test(f'{w}<Fraction({a},{b})<{w+1}',True)]),
            q('La fraction est-elle plus proche de la borne basse ou de la borne haute ?','Comparer les nombres de petits pas qui la séparent des bornes.',f'Elle est à {rest} parts de la borne basse et à {b-rest} parts de la borne haute.', 'Plus proche de la borne basse.' if rest<b-rest else ('À égale distance.' if rest==b-rest else 'Plus proche de la borne haute.'),[test(f'[{a}-{w*b},{(w+1)*b}-{a}]',[rest,b-rest])])]
    if fam==4:
        b,start,k=[(4,0,7),(6,1,11),(8,2,13)][level]; n=start*b+k; w=n//b;r=n%b
        return ['Lire le point sur les quarts','Une droite qui commence à un','La fenêtre en huitièmes'][level],[
            q('Quelle est la valeur d’un petit pas, en unité ?','Compter les intervalles dans une unité.',f'Chaque unité est partagée en {b} intervalles égaux.',f'${F(1,b)}$ unité.',[test(f'Fraction(1,{b})',[1,b])]),
            q(f'Le point est au {k}e petit pas après {start}. Donner son abscisse sous forme d’une fraction.','Compter aussi les parts avant le début de la fenêtre.',f'Avant {start}, il y a ${start}\\times{b}={start*b}$ petits pas depuis 0. Le point est donc au pas ${start*b}+{k}={n}$.',f'${F(n,b)}$.',[test(f'{start}+Fraction({k},{b})',[Fraction(n,b).numerator,Fraction(n,b).denominator])]),
            q('Donner une écriture entier plus fraction, puis encadrer l’abscisse.','Regrouper les petits pas en unités.',f'${n}={w}\\times{b}+{r}$, avec $0<{r}<{b}$.',f'${F(n,b)}={w}+{F(r,b)}$ et ${w}<{F(n,b)}<{w+1}$.',[test(f'Fraction({n},{b})=={w}+Fraction({r},{b})',True)])],f'La droite garde partout le même pas : {b} intervalles dans une unité. La fenêtre commence à {start}.'
    if fam==5:
        a,b=[(8,4),(18,6),(45,15)][level]; v=a//b
        return ['La fraction qui est un entier','Une unité ne suffit pas','Le dénominateur ne compte pas les unités'][level],[
            q(f'Calculer ${F(a,b)}$ en regroupant les parts.','Compter les groupes complets du dénominateur.',f'${a}={v}\\times{b}$. Il n’y a aucune part restante.',f'${F(a,b)}={v}$.',[test(f'Fraction({a},{b})',v)]),
            q(f'Un élève dit « Toute fraction est inférieure à 1 ». Donner ici un contre-exemple.','Comparer numérateur et dénominateur.',f'${a}>{b}$, donc les {a} parts occupent plusieurs unités. Le nombre trouvé est {v}.',f'${F(a,b)}={v}>1$.',[test(f'Fraction({a},{b})>1',True)]),
            q(f'Que vaut ${F(a+1,b)}$ ? Donner une écriture avec un entier.','Ajouter une seule part à l’entier déjà obtenu.',f'${a+1}={v}\\times{b}+1$. Le partage reste en {b}-ièmes.',f'${v}+{F(1,b)}$.',[test(f'Fraction({a+1},{b})=={v}+Fraction(1,{b})',True)])]
    b,a,c=[(6,5,9),(8,7,19),(12,11,35)][level]; total=a+c; w=total//b;r=total%b
    return ['Deux rubans mesurés en sixièmes','La mesure par reports successifs','Composer puis raccourcir une longueur'][level],[
        q(f'Une bande mesure ${F(a,b)}$ unité. Combien manque-t-il pour faire une unité ?','Compléter le nombre de parts du tout.',f'Une unité contient {b} parts et la bande en contient {a} ; il manque ${b}-{a}={b-a}$ part.',f'${F(b-a,b)}$ unité.',[test(f'1-Fraction({a},{b})',[1,b])]),
        q(f'On ajoute une bande de ${F(c,b)}$ unité. Quelle est la longueur totale ?','Compter des parts de même taille.',f'Les {a} parts et les {c} parts font ${a}+{c}={total}$ parts de même taille.',f'${F(total,b)}$ unités.',[test(f'Fraction({a},{b})+Fraction({c},{b})',[Fraction(total,b).numerator,Fraction(total,b).denominator])]),
        q('Combien d’unités complètes peut-on reporter dans cette longueur ? Que reste-t-il ?','Regrouper les parts en unités complètes.',f'${total}={w}\\times{b}+{r}$.',f'{w} unités et ${F(r,b)}$ unité.',[test(f'[{total}//{b},{total}%{b}]',[w,r])])]

def comparer(level,fam):
    if fam==0:
        a,c,b=[(3,5,8),(11,9,12),(47,49,60)][level];sign='<' if a<c else '>'
        return ['Des huitièmes de même taille','Des douzièmes au-delà du regard','Comparer des soixantièmes'][level],[
            q(f'Comparer ${F(a,b)}$ et ${F(c,b)}$.','À même dénominateur, comparer les numérateurs.',f'Les parts ont la même taille et ${a}{sign}{c}$.',f'${F(a,b)}{sign}{F(c,b)}$.',[test(f'Fraction({a},{b})'+sign+f'Fraction({c},{b})',True)]),
            q('Quelle est la différence entre la plus grande et la plus petite ?','Retirer le petit nombre de parts au grand.',f'${max(a,c)}-{min(a,c)}={abs(a-c)}$ parts de taille ${F(1,b)}$.',f'${F(abs(a-c),b)}$.',[test(f'Fraction({max(a,c)},{b})-Fraction({min(a,c)},{b})',[Fraction(abs(a-c),b).numerator,Fraction(abs(a-c),b).denominator])]),
            q('Ces deux fractions sont-elles inférieures à 1 ?','Comparer chaque numérateur au dénominateur.',f'${a}<{b}$ et ${c}<{b}$, donc les deux fractions sont inférieures à une unité.','Oui, toutes deux sont inférieures à 1.',[test(f'{a}<{b} and {c}<{b}',True)])]
    if fam==1:
        a,b,d=[(3,5,8),(7,6,12),(17,8,12)][level]
        return ['Trois parts de tailles différentes','Sept sixièmes ou sept douzièmes','Dix-sept parts ne suffisent pas pour comparer'][level],[
            q(f'Comparer une part ${F(1,b)}$ et une part ${F(1,d)}$.','Un partage en moins de parts donne des parts plus grandes.',f'Une même unité partagée en {b} donne de plus grandes parts qu’un partage en {d}.',f'${F(1,b)}>{F(1,d)}$.',[test(f'Fraction(1,{b})>Fraction(1,{d})',True)]),
            q(f'En déduire la comparaison de ${F(a,b)}$ et ${F(a,d)}$.','Prendre le même nombre de parts des deux tailles.',f'On prend {a} parts de chaque sorte. Les {b}-ièmes sont plus grands, donc leur somme est plus grande.',f'${F(a,b)}>{F(a,d)}$.',[test(f'Fraction({a},{b})>Fraction({a},{d})',True)]),
            q('Peut-on dire « le plus grand dénominateur donne la plus grande fraction » ?','Confronter l’affirmation aux deux nombres étudiés.',f'Ici le dénominateur {d} est plus grand que {b}, mais la fraction correspondante est plus petite.','Non ; à numérateur positif égal, c’est l’inverse.')]
    if fam==2:
        a,b,c,d=[(7,8,9,8),(11,12,7,6),(59,60,21,20)][level]
        return ['Une unité pour séparer deux fractions','Comparer sans changer le partage','Le repère 1 évite des calculs'][level],[
            q(f'Comparer ${F(a,b)}$ à 1.','Comparer numérateur et dénominateur.',f'${a}<{b}$. La fraction n’atteint pas une unité.',f'${F(a,b)}<1$.',[test(f'Fraction({a},{b})<1',True)]),
            q(f'Comparer ${F(c,d)}$ à 1, puis comparer les deux fractions.','Utiliser 1 comme nombre intermédiaire.',f'${c}>{d}$, donc la seconde fraction dépasse 1. La première est en dessous de 1.',f'${F(a,b)}<1<{F(c,d)}$.',[test(f'Fraction({a},{b})<1<Fraction({c},{d})',True)]),
            q(f'Combien manque-t-il à ${F(a,b)}$ pour atteindre 1 ?','Compléter l’unité en parts du même dénominateur.',f'${b}-{a}={b-a}$ part reste à ajouter.',f'${F(b-a,b)}$.',[test(f'1-Fraction({a},{b})',[b-a,b])])]
    if fam==3:
        a,b,k=[(3,4,2),(5,6,5),(7,12,5)][level]; top=a*k;bottom=b*k
        return ['Changer des quarts en huitièmes','Des sixièmes aux trentièmes','La case manquante des soixantièmes'][level],[
            q(f'Compléter ${F(a,b)}={F("?",bottom)}$.','Découper chaque part en autant de petites parts.',f'${bottom}={b}\\times{k}$. On multiplie aussi le numérateur : ${a}\\times{k}={top}$.',f'${F(a,b)}={F(top,bottom)}$.',[test(f'Fraction({a},{b})==Fraction({top},{bottom})',True)]),
            q(f'Compléter ${F(top,"?")}={F(a,b)}$.','Retrouver le même facteur entre les numérateurs.',f'Le numérateur {top} est {k} fois {a}. Le dénominateur doit être ${b}\\times{k}={bottom}$.',f'Le dénominateur manquant est {bottom}.',[test(f'{b}*{k}',bottom)]),
            q(f'Multiplier seulement le numérateur par {k} donnerait-il la même fraction ?','Comparer des nombres de parts de même taille.',f'La fraction obtenue serait ${F(a*k,b)}$. On compterait {a*k} parts au lieu de {a}, alors que leur taille resterait identique.', 'Non, il faut multiplier les deux termes par le même facteur.',[test(f'Fraction({a*k},{b})!=Fraction({a},{b})',True)])]
    if fam==4:
        a,b,c,d,den=[(3,4,7,10,20),(7,6,9,8,24),(17,12,7,5,60)][level]; na=a*(den//b); nc=c*(den//d); sign='>' if na>nc else '<'
        return ['Les vingtièmes départagent les longueurs','Un partage commun en vingt-quatrièmes','Soixante parts suffisent'][level],[
            q(f'Choisir un dénominateur commun à ${F(a,b)}$ et ${F(c,d)}$, au plus égal à 60.','Chercher un multiple commun des deux dénominateurs.',f'${den}={b}\\times{den//b}={d}\\times{den//d}$.',f'On choisit {den}.',[test(f'{den}%{b}==0 and {den}%{d}==0 and {den}<=60',True)]),
            q('Écrire les deux fractions avec ce dénominateur.','Multiplier les deux termes par le facteur de changement de partage.',f'Le premier numérateur devient ${a}\\times{den//b}={na}$ ; le second devient ${c}\\times{den//d}={nc}$.',f'${F(a,b)}={F(na,den)}$ et ${F(c,d)}={F(nc,den)}$.',[test(f'Fraction({a},{b})==Fraction({na},{den}) and Fraction({c},{d})==Fraction({nc},{den})',True)]),
            q('Comparer les fractions de départ.','Comparer les nombres de parts de même taille.',f'${na}{sign}{nc}$, donc le même ordre vaut pour les fractions.',f'${F(a,b)}{sign}{F(c,d)}$.',[test(f'Fraction({a},{b})'+sign+f'Fraction({c},{d})',True)])]
    if fam==5:
        vals=[[(1,2),(3,4),(5,8)],[(7,6),(9,8),(5,4)],[(7,10),(11,15),(17,20)]][level];den=[8,24,60][level]; ss=sorted(vals,key=lambda z:Fraction(*z)); nums=[a*(den//b) for a,b in vals]
        return ['Les trois marques d’un ruban','Un classement au-delà de 1','Trois dénominateurs à organiser'][level],[
            q('Écrire les trois fractions avec un même dénominateur au plus égal à 60.','Choisir un multiple commun aux trois dénominateurs.',f'Le dénominateur {den} convient. En respectant l’ordre donné, les numérateurs deviennent '+', '.join(map(str,nums))+'.',', '.join('$'+F(n,den)+'$' for n in nums)+'.',[test(f'[Fraction(a,b) for a,b in {vals}]',[dump_value(Fraction(*x)) for x in vals])]),
            q('Ranger les trois fractions dans l’ordre croissant.','Comparer les numérateurs après le changement de partage.', 'Toutes les parts ont maintenant la même taille ; on range leur nombre dans l’ordre croissant.', '$'+'<'.join(F(a,b) for a,b in ss)+'$.',[test(f'sorted([Fraction(a,b) for a,b in {vals}])',[dump_value(Fraction(*x)) for x in ss])]),
            q('Donner l’écart entre la plus grande et la plus petite.','Soustraire les numérateurs des deux extrêmes.',f'Les numérateurs extrêmes sont {min(nums)} et {max(nums)} ; leur différence est {max(nums)-min(nums)}.',f'${F(max(nums)-min(nums),den)}$.',[test(f'Fraction({max(nums)},{den})-Fraction({min(nums)},{den})',dump_value(Fraction(max(nums)-min(nums),den)))])], 'Les marques sont : '+', '.join('$'+F(a,b)+'$' for a,b in vals)+'.'
    a,b,c,d=[(1,2,3,8),(5,6,1,12),(11,40,1,8)][level]; den=max(b,d);na=a*(den//b);nc=c*(den//d)
    return ['Additionner puis retirer des huitièmes','La différence en douzièmes','Un calcul avec des quarantièmes'][level],[
        q(f'Écrire ${F(a,b)}$ et ${F(c,d)}$ avec le plus grand des deux dénominateurs.','L’un des dénominateurs est un multiple de l’autre.',f'On utilise {den}. Le premier numérateur est {na}, le second {nc}.',f'${F(na,den)}$ et ${F(nc,den)}$.',[test(f'Fraction({a},{b})==Fraction({na},{den}) and Fraction({c},{d})==Fraction({nc},{den})',True)]),
        q('Calculer leur somme.','Additionner les nombres de parts de même taille.',f'${na}+{nc}={na+nc}$ ; le dénominateur reste {den}.',f'${F(na+nc,den)}$.',[test(f'Fraction({a},{b})+Fraction({c},{d})',dump_value(Fraction(na+nc,den)))]),
        q('Calculer la première fraction moins la seconde.','Retirer le second nombre de parts au premier.',f'${na}-{nc}={na-nc}$. On compte toujours des {den}-ièmes.',f'${F(na-nc,den)}$.',[test(f'Fraction({a},{b})-Fraction({c},{d})',dump_value(Fraction(na-nc,den)))])]

def quantite(level,fam):
    if fam==0:
        total,a,b=[(24,2,3),(56,3,7),(96,5,8)][level]; unit=total//b; value=unit*a
        return ['Deux tiers des jetons','Trois septièmes des cartes','Cinq huitièmes d’une collection'][level],[
            q(f'Que représente une part quand on cherche les ${F(a,b)}$ de {total} jetons ?','Partager le tout en autant de groupes que le dénominateur.',f'${total}\\div{b}={unit}$. Une part contient {unit} jetons.',f'{unit} jetons.',[test(f'{total}//{b}',unit)]),
            q('Combien de jetons prend-on ?','Prendre le nombre de parts indiqué par le numérateur.',f'${unit}\\times{a}={value}$.',f'{value} jetons.',[test(f'{total}*Fraction({a},{b})',value)]),
            q('Combien de jetons reste-t-il ?','Soustraire la partie prise au total.',f'${total}-{value}={total-value}$.',f'{total-value} jetons.',[test(f'{total}-{value}',total-value)])]
    if fam==1:
        total,a,b,unit=[(100,3,4,'m'),(500,3,10,'g'),(1200,7,12,'mL')][level]; part=total//b;v=part*a
        return ['La marche des trois quarts','La farine de la recette','Le réservoir gradué en douzièmes'][level],[
            q('Quelle grandeur est le tout de référence ?','Relire la quantité avant de fractionner.',f'La fraction porte sur la totalité des {total} {unit}.',f'Le tout est {total} {unit}.'),
            q(f'Calculer ${F(a,b)}$ de cette grandeur.','Partager puis multiplier en conservant l’unité.',f'${total}\\div{b}={part}$, puis ${part}\\times{a}={v}$.',f'{v} {unit}.',[test(f'{total}*Fraction({a},{b})',v)]),
            q('La réponse est-elle cohérente avec une fraction inférieure à 1 ?','Comparer la partie au tout positif.',f'${a}<{b}$ et ${v}<{total}$. La partie obtenue est bien plus petite que le tout.','Oui : la partie est plus petite que le tout.',[test(f'{a}<{b} and {v}<{total}',True)])],f'On prend ${F(a,b)}$ d’une quantité de {total} {unit}.'
    if fam==2:
        total,a,b=[(40,3,5),(72,5,8),(180,7,12)][level];used=total*a//b;left=total-used
        return ['Les livres encore en rayon','Les places libres du spectacle','Préparer la seconde livraison'][level],[
            q(f'On utilise les ${F(a,b)}$ de {total} objets. Combien sont utilisés ?','Déterminer une part, puis le nombre de parts utilisées.',f'${total}\\div{b}={total//b}$ puis ${total//b}\\times{a}={used}$.',f'{used} objets.',[test(f'{total}*Fraction({a},{b})',used)]),
            q('Quelle fraction du total reste disponible ?','Retirer les parts utilisées aux parts du tout.',f'Le tout correspond à ${F(b,b)}$. Il reste ${b}-{a}={b-a}$ parts.',f'${F(b-a,b)}$ du total.',[test(f'1-Fraction({a},{b})',dump_value(Fraction(b-a,b)))]),
            q('Calculer le reste par deux méthodes.','Soustraire ou calculer directement la fraction complémentaire.',f'${total}-{used}={left}$. Autre méthode : ${total}\\div{b}={total//b}$ puis ${total//b}\\times{b-a}={left}$.',f'{left} objets restent.',[test(f'{total}-{used}',left),test(f'{total}*Fraction({b-a},{b})',left)])]
    if fam==3:
        t1,a,b,t2,c,d=[(20,1,2,36,1,3),(48,3,4,70,1,2),(96,5,8,84,3,4)][level];v1=t1*a//b;v2=t2*c//d
        return ['Une moitié peut être plus petite qu’un tiers','Deux lots, deux touts différents','Comparer deux prélèvements'][level],[
            q('Calculer le prélèvement sur le premier lot.','Utiliser uniquement le total du premier lot.',f'${t1}\\div{b}={t1//b}$ puis ${t1//b}\\times{a}={v1}$.',f'{v1} objets.',[test(f'{t1}*Fraction({a},{b})',v1)]),
            q('Calculer le prélèvement sur le second lot.','Repartir du second total, qui est différent.',f'${t2}\\div{d}={t2//d}$ puis ${t2//d}\\times{c}={v2}$.',f'{v2} objets.',[test(f'{t2}*Fraction({c},{d})',v2)]),
            q('Quel lot donne le plus d’objets ? Quel est l’écart ?','Comparer les quantités calculées et non les seules fractions.',f'${max(v1,v2)}-{min(v1,v2)}={abs(v1-v2)}$.',f'Le '+('premier' if v1>v2 else 'second')+f' lot donne {abs(v1-v2)} objets de plus.',[test(f'{max(v1,v2)}-{min(v1,v2)}',abs(v1-v2))])],f'Premier lot : ${F(a,b)}$ de {t1} objets. Second lot : ${F(c,d)}$ de {t2} objets.'
    if fam==4:
        k,a,b=[(3,5,4),(4,7,6),(7,11,8)][level];n=k*a;w=n//b;r=n%b
        return ['Trois bandes de cinq quarts','Quatre reports de sept sixièmes','Sept rubans identiques'][level],[
            q(f'Écrire ${k}\\times{F(a,b)}$ comme une addition répétée.','Le facteur entier indique le nombre de répétitions.',f'Il faut additionner {k} fois la même longueur ${F(a,b)}$.', '$'+'+'.join(F(a,b) for _ in range(k))+'$.'),
            q('Calculer le produit sous la forme d’une fraction.','Multiplier le nombre de parts, conserver leur taille.',f'${k}\\times{a}={n}$ parts de taille ${F(1,b)}$.',f'${F(n,b)}$.',[test(f'{k}*Fraction({a},{b})',dump_value(Fraction(n,b)))]),
            q('Donner la longueur totale sous la forme entier plus fraction, en mètres.','Former les unités complètes avec les parts.',f'${n}={w}\\times{b}+{r}$.',f'${w}+{F(r,b)}$ m.',[test(f'Fraction({n},{b})=={w}+Fraction({r},{b})',True)])],f'Chaque bande mesure ${F(a,b)}$ m. On en aligne {k}, sans les superposer.'
    if fam==5:
        a,b,part=[(1,4,9),(3,5,24),(5,8,35)][level];u=part//a;total=u*b
        return ['Retrouver le sac à partir d’un quart','Reconstruire le total avec trois cinquièmes','Cinq huitièmes sont connus'][level],[
            q(f'On sait que ${F(a,b)}$ du stock représentent {part} objets. Combien vaut une seule part ?','Les objets connus correspondent au numérateur en parts.',f'${part}\\div{a}={u}$ objets par part.',f'{u} objets.',[test(f'{part}//{a}',u)]),
            q('Retrouver le stock entier.','Le tout contient le dénominateur en parts.',f'${u}\\times{b}={total}$.',f'{total} objets.',[test(f'{u}*{b}',total)]),
            q('Vérifier en recalculant la fraction du total retrouvé.','Partager le total, puis prendre les parts annoncées.',f'${total}\\div{b}={u}$ puis ${u}\\times{a}={part}$. On retrouve la donnée de départ.',f'La vérification redonne {part} objets.',[test(f'{total}*Fraction({a},{b})',part)])]
    total,a,b,need=[(60,2,3,35),(96,5,8,64),(180,7,12,100)][level];v=total*a//b;dif=abs(v-need)
    return ['Assez de matériel pour l’atelier ?','Le stock réservé suffit-il ?','Choisir et justifier une préparation'][level],[
        q(f'On réserve ${F(a,b)}$ de {total} feuilles. Combien de feuilles sont réservées ?','Calculer la part du stock disponible pour l’atelier.',f'${total}\\div{b}={total//b}$, puis ${total//b}\\times{a}={v}$.',f'{v} feuilles.',[test(f'{total}*Fraction({a},{b})',v)]),
        q(f'Il faut {need} feuilles pour l’atelier. La réserve suffit-elle ?','Comparer besoin et quantité réservée.',f'La réserve contient {v} feuilles pour un besoin de {need}. L’écart vaut ${max(v,need)}-{min(v,need)}={dif}$.',f'Oui, {dif} feuilles en plus.' if v>=need else f'Non, il manque {dif} feuilles.',[test(f'{v}>={need}',v>=need)]),
        q('Combien de feuilles du stock total resteront après l’atelier, si on utilise exactement le besoin ?','Le total de départ reste le tout ; retirer le besoin réel.',f'${total}-{need}={total-need}$. Réserver des feuilles ne les consomme pas encore.',f'{total-need} feuilles.',[test(f'{total}-{need}',total-need)])]

def decimal_str(n,den=1000):
    digits={10:1,100:2,1000:3}[den]
    return f'{n//den},{n%den:0{digits}d}'
def dec(n,den=1000): return decimal_str(n,den).replace(',',r'{,}')
def decimaux(level,fam):
    if fam==0:
        n=[3205,14070,208007][level];w=n//1000;ds=[n//100%10,n//10%10,n%10]
        return ['Lire trois unités et des millièmes','Un zéro au bon rang','Les deux zéros de 208,007'][level],[
            q(f'Donner la partie entière de ${dec(n)}$ et nommer les trois rangs après la virgule.','Séparer les unités entières des parts d’unité.',f'Avant la virgule, on lit {w}. Après viennent les dixièmes, centièmes et millièmes.',f'Partie entière : {w} ; dixièmes, centièmes, millièmes.',[test(f'{n}//1000',w)]),
            q('Donner le chiffre de chaque rang décimal et sa contribution.','Un chiffre indique combien de parts de son rang sont présentes.',f'Les chiffres sont {ds[0]}, {ds[1]}, {ds[2]}. Leurs contributions sont ${F(ds[0],10)}$, ${F(ds[1],100)}$ et ${F(ds[2],1000)}$.',f'{ds[0]} dixièmes, {ds[1]} centièmes et {ds[2]} millièmes.',[test(f'{w}+Fraction({ds[0]},10)+Fraction({ds[1]},100)+Fraction({ds[2]},1000)',dump_value(Fraction(n,1000)))]),
            q('Lire le nombre en unités et millièmes.','Tout exprimer dans le rang des millièmes.',f'La partie décimale compte {n%1000} millièmes, en plus des {w} unités entières.',f'{w} unités et {n%1000} millièmes.',[test(f'{w}*1000+{n%1000}',n)])]
    if fam==1:
        n,den=[(237,100),(4207,1000),(12508,1000)][level];w=n//den;r=n%den
        return ['Des centièmes à la virgule','Les trois écritures de 4,207','Une décomposition avec un zéro intérieur'][level],[
            q(f'Écrire ${F(N(n),N(den))}$ avec une virgule.','Le dénominateur fixe le rang du dernier chiffre.',f'Le dénominateur {den} impose '+('deux' if den==100 else 'trois')+f' chiffres décimaux. On place {w} unités avant la virgule.',f'${dec(n,den)}$.',[test(f'Fraction({n},{den})',dump_value(Fraction(n,den)))]),
            q('Écrire le nombre comme entier plus une fraction décimale inférieure à 1.','Séparer les groupes complets et le reste.',f'${N(n)}={w}\\times{N(den)}+{r}$.',f'${w}+{F(r,N(den))}$.',[test(f'{w}+Fraction({r},{den})',dump_value(Fraction(n,den)))]),
            q('Décomposer avec des dixièmes, centièmes et, si besoin, millièmes de numérateurs inférieurs à 10.','Lire chaque rang et omettre les contributions nulles.',f'Chaque chiffre occupe son rang : {decimal_str(n,den)}. Les zéros intérieurs ne changent pas la place des autres chiffres.', '$'+str(w)+''.join('+'+F(int(x),10**(i+1)) for i,x in enumerate(decimal_str(n,den).split(',')[1]) if int(x))+'$.',[test(f'{w}+'+'+'.join(f'Fraction({int(x)},{10**(i+1)})' for i,x in enumerate(decimal_str(n,den).split(',')[1])),dump_value(Fraction(n,den)))])]
    if fam==2:
        a,b,c=[(35,350,305),(407,4070,4007),(1205,12050,12005)][level];den=[10,100,1000][level];den2=den*10
        # À la difficulté 3, éviter les dix-millièmes : comparer à des écritures à virgule uniquement.
        x=Fraction(a,den)
        if level==2:
            return 'Les zéros que l’on peut retirer',[
                q('Les écritures $12{,}05$ et $12{,}050$ désignent-elles le même nombre ?','Un zéro ajouté après le dernier chiffre décimal ne change aucun rang existant.','Les 1 205 centièmes valent 12 050 millièmes. Le zéro final n’ajoute aucune quantité.','Oui : $12{,}05=12{,}050$.',[test('Fraction(1205,100)==Fraction(12050,1000)',True)]),
                q('Peut-on écrire $12{,}005=12{,}05$ ?','Un zéro intérieur garde la place du rang.',r'$12{,}005$ a 0 centième ; $12{,}05$ a 5 centièmes. En millièmes : $12\,005\ne12\,050$.','Non : $12{,}005<12{,}05$.',[test('Fraction(12005,1000)<Fraction(1205,100)',True)]),
                q('Donner le nombre de centièmes entiers contenus dans $12{,}005$.','Regrouper les millièmes par paquets de dix.',r'$12\,005=1\,200\times10+5$ millièmes. Il y a 1 200 centièmes entiers et encore 5 millièmes.','1 200 centièmes entiers.',[test('12005//10',1200)])]
        return ['Le zéro final ou le zéro intérieur','Des écritures qui semblent différentes'][level],[
            q(f'Comparer ${F(a,den)}$ et ${F(b,den2)}$.','Exprimer les deux nombres dans le même rang.',f'${a}\\times10={b}$ et ${den}\\times10={den2}$. Les fractions ont la même valeur.',f'${F(a,den)}={F(b,den2)}$.',[test(f'Fraction({a},{den})==Fraction({b},{den2})',True)]),
            q('Écrire leur valeur commune avec une virgule.','Placer les chiffres selon les rangs du dénominateur.',f'${a}$ parts de taille ${F(1,den)}$ donnent ${dec(a,den)}$.',f'${dec(a,den)}$.',[test(f'Fraction({a},{den})',dump_value(x))]),
            q(f'Comparer cette valeur à ${dec(c,den2)}$.','Aligner les rangs avec un zéro final.',f'La valeur commune est ${dec(b,den2)}$. Au même rang, ${b}>{c}$.',f'${dec(a,den)}>{dec(c,den2)}$.',[test(f'Fraction({a},{den})>Fraction({c},{den2})',True)])]
    if fam==3:
        vals=[[5800,5790,5080,5780,5805],[7205,7250,7025,7520,7200],[12005,12050,12500,12009,12090]][level];s=sorted(vals)
        return ['Cinq étiquettes décimales','Des millièmes pour ranger','Les zéros du classement'][level],[
            q('Ranger les cinq nombres dans l’ordre croissant.','Comparer rang par rang, avec trois décimales pour s’aider.', 'Les parties entières sont d’abord comparées. À égalité, on compare les dixièmes, puis les centièmes, puis les millièmes.', '$'+'<'.join(dec(n) for n in s)+'$.',[test(f'sorted({vals})',s)]),
            q('Donner le plus grand nombre et sa partie entière.','Lire la dernière valeur du rangement et ses unités entières.',f'Le plus grand est ${dec(s[-1])}$. Les chiffres avant la virgule donnent {s[-1]//1000}.',f'${dec(s[-1])}$ ; partie entière {s[-1]//1000}.',[test(f'max({vals})//1000',s[-1]//1000)]),
            q('Un élève compare seulement les nombres formés après la virgule, sans aligner les rangs. Cette méthode est-elle fiable ?','Les chiffres n’ont pas la même valeur selon leur rang.','Par exemple $5{,}8=5{,}800$ dépasse $5{,}79=5{,}790$, bien que $8<79$. Il faut comparer des rangs identiques.','Non : il faut aligner les rangs décimaux.',[test('Fraction(58,10)>Fraction(579,100)',True)])], 'Nombres à comparer : '+', '.join('$'+dec(n)+'$' for n in vals)+'.'
    if fam==4:
        n=[4207,9995,17009][level];w=n//1000;lo=n//100*100;hi=lo+100; lower=n//10*10;upper=lower+10
        return ['Entre deux entiers et deux dixièmes','Au voisinage de 10','Intercaler sous trois contraintes'][level],[
            q(f'Encadrer ${dec(n)}$ entre deux entiers consécutifs.','Repérer la partie entière et l’entier suivant.',f'La partie entière est {w} et la partie décimale est non nulle.',f'${w}<{dec(n)}<{w+1}$.',[test(f'{w}<Fraction({n},1000)<{w+1}',True)]),
            q('Encadrer le même nombre entre deux dixièmes consécutifs.','Garder le rang des dixièmes puis avancer d’un dixième.',f'Les dixièmes voisins sont ${dec(lo)}$ et ${dec(hi)}$.',f'${dec(lo)}<{dec(n)}<{dec(hi)}$.',[test(f'{lo}<{n}<{hi} and {hi}-{lo}==100',True)]),
            q(f'Donner un nombre avec au plus trois décimales, strictement entre ${dec(lower)}$ et ${dec(upper)}$, différent du nombre étudié.','Choisir un autre millième à l’intérieur des deux bornes.',f'Le nombre ${dec(lower+1)}$ est un millième après la borne basse et reste avant la borne haute.',f'Par exemple ${dec(lower+1)}$.',[test(f'{lower}<{lower+1}<{upper} and {lower+1}!={n}',True)])]
    if fam==5:
        start,step,count=[(4200,10,3),(7200,5,7),(12000,1,13)][level];n=start+step*count;right=start+step*20
        return ['Le troisième centième','Une graduation de cinq millièmes','Une loupe sur les millièmes'][level],[
            q('Calculer la valeur d’un petit intervalle.','Partager l’écart des bornes par les vingt intervalles.',f'La différence des bornes vaut ${dec(right-start)}$. En partageant par 20, un pas vaut ${dec(step)}$.',f'${dec(step)}$.',[test(f'Fraction({right-start},1000)/20',dump_value(Fraction(step,1000)))]),
            q(f'Un point est au {count}e petit pas après la première borne. Donner son abscisse.','Ajouter le nombre de pas au départ.',f'En millièmes : ${start}+{count}\\times{step}={n}$.',f'${dec(n)}$.',[test(f'{start}+{count}*{step}',n)]),
            q('Écrire cette abscisse sous forme d’une fraction décimale.','Compter les millièmes depuis zéro, même si la fenêtre commence plus loin.',f'Le point est repéré par {n} millièmes, et non seulement par les pas visibles dans la fenêtre.',f'${F(N(n),"1\\,000")}$.',[test(f'Fraction({n},1000)',dump_value(Fraction(n,1000)))])],f'Une fenêtre de droite va de ${dec(start)}$ à ${dec(right)}$ en vingt intervalles égaux.'
    nums=[[7499,7500,7501],[12499,12500,12501],[99499,99500,99501]][level]
    qs=[]
    for n in nums:
        w=n//1000;v=(n+500)//1000;digit=n//100%10
        qs.append(q(f'Donner la partie entière et l’arrondi à l’entier de ${dec(n)}$.','Distinguer la partie entière de l’entier le plus proche.',f'La partie entière est {w}. Le chiffre des dixièmes est {digit} : '+('il est inférieur à 5, on garde la partie entière.' if digit<5 else 'il est au moins égal à 5, on choisit l’entier suivant. À mi-chemin, on choisit aussi le supérieur.'),f'Partie entière : {w} ; arrondi : {v}.',[test(f'[{n}//1000,({n}+500)//1000]',[w,v])]))
    return ['Juste avant, au milieu, juste après','La frontière des douze unités','Un arrondi peut changer de dizaine'][level],qs

BUILDERS=[grands,multiples,fractions,comparer,quantite,decimaux]
FAMILIES=[
 ['lecture-écriture','rangs et groupes','décompositions et échanges','comparaison et rangement','encadrement et succession','graduations','conditionnement'],
 ['sens multiple-diviseur','critères 2 5 10','recherche exhaustive par paires','diviseurs communs','multiples communs','diviseurs jusqu’à 100','recherche sous contraintes'],
 ['partie-tout et représentation','regroupement au-delà de 1','écriture mixte vers fraction','encadrement','repérage','analyse d’erreur et entier','mesure et complément'],
 ['même dénominateur','même numérateur','comparaison à 1','fractions équivalentes','dénominateur commun','rangement et écart','addition et soustraction'],
 ['fraction de collection','fraction de grandeur','complément au tout','comparaison de touts différents','produit entier-fraction','recherche du tout','décision et besoin'],
 ['numération de position','passages entre écritures','équivalences et zéros','comparaison et rangement','encadrement et intercalation','graduations','partie entière et arrondi']]

HARD=[
 [q('Un nombre a les classes 890, 006 et 040. Un élève écrit 890 640. Identifier son erreur.','Contrôler trois rangs dans chaque classe intérieure.',r'Les classes 006 et 040 doivent chacune conserver leurs trois chiffres. On obtient $890\,006\,040$, et non $890\,640$.',r'Il a supprimé des zéros de position : le bon nombre est $890\,006\,040$.',[test('890*1000000+6*1000+40',890006040)]),
  q('Dans 808 080 808, échanger le chiffre des unités avec celui des dizaines change-t-il le nombre ? De combien ?','Recalculer seulement les contributions modifiées.','Les 8 unités et 0 dizaine deviennent 0 unité et 8 dizaines. La valeur augmente de $80-8=72$.',r'Oui : le nouveau nombre est $808\,080\,880$, soit 72 de plus.',[test('808080880-808080808',72)]),
  q('Peut-on écrire le nombre obtenu avec 489 millions, 2 008 milliers et 75 unités ?','Échanger un million contre mille milliers.',r'$489\,000\,000+2\,008\,000+75=491\,008\,075$. Cette somme est la même que $490\,000\,000+1\,008\,000+75$.','Oui, car un million échangé donne mille milliers.',[test('489*1000000+2008*1000+75==490*1000000+1008*1000+75',True)]),
  q('Combien d’entiers sont strictement entre les deux plus petits nombres de la liste ?','Retirer les deux bornes après avoir calculé leur écart.',r'Les deux plus petits sont $908\,008\,900$ et $908\,080\,900$. Leur écart vaut $72\,000$. Il y a un entier de moins que cet écart entre les bornes.',r'$71\,999$ entiers.',[test('908080900-908008900-1',71999)]),
  q(r'Trouver le plus petit entier dont l’encadrement au million est $899\,000\,000<n<900\,000\,000$ et dont les trois derniers chiffres sont 500.','Commencer juste après la borne basse et respecter les unités imposées.',r'$899\,000\,500$ convient. Un nombre plus petit de même terminaison serait au plus $898\,999\,500$, hors de l’intervalle.',r'$899\,000\,500$.',[test('899000000<899000500<900000000 and 899000500%1000==500',True)]),
  q('Un point situé à mi-chemin du deuxième et du troisième trait après la borne de départ représente-t-il un entier ? Lequel ?','Ajouter deux pas et la moitié d’un pas.',r'$208\,000\,000+2\times250\,000+125\,000=208\,625\,000$. La moitié de 250 000 est entière.',r'Oui : $208\,625\,000$.',[test('208000000+2*250000+125000',208625000)]),
  q('Un collègue compte 987 paquets et 65 432 objets isolés. Un autre annonce 986 paquets et 165 432 objets isolés. Qui a le bon total ? Qui a le maximum de paquets complets ?','Distinguer une décomposition juste d’un rangement terminé.',r'Les deux totaux valent $98\,765\,432$. Mais 165 432 objets isolés permettent encore un paquet de 100 000.',r'Les deux totaux sont justes ; 987 est le maximum de paquets complets.',[test('987*100000+65432==986*100000+165432==98765432',True)])],
 [q('Un élève affirme : « Si 8 divise 72, alors 16 divise aussi 72. » Est-ce vrai ?','Un facteur doublé ne conserve pas toujours le partage exact.',r'$72=16\times4+8$. Il reste 8, donc le partage par 16 n’est pas exact.','Non : 16 n’est pas un diviseur de 72.',[test('72%16',8)]),
  q(r'Donner les chiffres qui peuvent remplacer la case dans $13\,4\square$ pour que le nombre soit divisible par 2 et par 5.','Croiser les deux critères du chiffre des unités.','Un multiple de 5 se termine par 0 ou 5. Parmi eux, seul 0 est pair. Le nombre est donc 1 340.','Seulement 0.',[test('[d for d in range(10) if (1340+d)%2==0 and (1340+d)%5==0]',[0])]),
  q('Pourquoi la liste des diviseurs de 28 est-elle complète ?','Poursuivre les tests jusqu’au croisement des facteurs.',r'Les tests de 1, 2, 3, 4 et 5 donnent les paires $1\times28$, $2\times14$ et $4\times7$. Les autres tests utiles ne donnent aucune nouvelle paire avant de retrouver 7 avec 4.','Tout diviseur est dans l’une des paires 1 et 28 ; 2 et 14 ; 4 et 7.',[test('[d for d in range(1,29) if 28%d==0]',[1,2,4,7,14,28])]),
  q('Avec 24 cartes rouges et 30 bleues, former le maximum de lots identiques sans reste. Quel est le contenu de chaque lot ?','Le nombre de lots est un diviseur commun ; choisir le plus grand.',r'Les diviseurs communs sont 1, 2, 3 et 6. Avec 6 lots, chaque lot reçoit $24\div6=4$ rouges et $30\div6=5$ bleues.','6 lots, chacun avec 4 cartes rouges et 5 bleues.',[test('[24//6,30//6]',[4,5])]),
  q('Pour une longueur commune strictement supérieure à 50 cm et au plus 100 cm, quelles possibilités restent avec les baguettes de 8 cm et de 12 cm ?','Filtrer la liste commune avec les deux bornes.','Les multiples communs positifs jusqu’à 100 sont 24, 48, 72 et 96. Après la condition supérieure à 50, il reste 72 et 96.','72 cm et 96 cm.',[test('[x for x in range(51,101) if x%8==0 and x%12==0]',[72,96])]),
  q('Trouver deux tailles de boîtes, différentes de 1 et 96, donnant chacune au moins 10 boîtes complètes pour les 96 perles.','Une taille doit diviser 96 et son quotient doit être au moins 10.',r'Les tailles 6 et 8 donnent respectivement $96\div6=16$ et $96\div8=12$ boîtes.','Par exemple 6 perles ou 8 perles par boîte.',[test('96%6==0 and 96%8==0 and 96//6>=10 and 96//8>=10',True)]),
  q('Le nombre caché pourrait-il être à la fois multiple de 9, multiple de 2 et se terminer par 5 ?','Utiliser la parité pour déceler une contradiction.','Tout nombre terminé par 5 est impair. Il ne peut donc pas être divisible par 2, quelle que soit sa divisibilité par 9.','Non : les conditions « pair » et « se termine par 5 » sont incompatibles.')],
 [q('Deux bandes identiques représentent chacune une unité. On colorie 17 parts sur 24 dans chacune. Quelle fraction d’une unité est colorée au total ?','Additionner les parts en gardant l’unité de référence.',r'Il y a $17+17=34$ vingt-quatrièmes colorés. Les deux unités sont identiques. La fraction d’une seule unité est $\frac{34}{24}$, même si 34 parts dépassent une unité.',r'$\frac{34}{24}$ unité.',[test('2*Fraction(17,24)',dump_value(Fraction(34,24)))]),
  q('Quel est le plus petit numérateur à ajouter à 58 pour obtenir une fraction entière de dénominateur 7 ?','Compléter jusqu’au prochain multiple de 7.',r'Le multiple suivant est $9\times7=63$. Il faut $63-58=5$ parts de plus.',r'Ajouter 5 au numérateur ; on obtient $\frac{63}7=9$.',[test('63-58',5)]),
  q(r'Trouver l’entier manquant dans $\frac{107}{12}=\square+\frac{11}{12}$.','Retirer les parts de la fraction restante puis regrouper.',r'$107-11=96$ parts correspondent à l’entier. Or $96=8\times12$.','L’entier manquant est 8.',[test('(107-11)//12',8)]),
  q('Trouver toutes les fractions de dénominateur 12 strictement entre 9 et 10 et dont le numérateur se termine par 5.','Traduire les bornes en nombre de douzièmes.','$108<n<120$ ; dans cet intervalle, seul 115 se termine par 5.',r'Seulement $\frac{115}{12}$.',[test('[n for n in range(109,120) if n%10==5]',[115])]),
  q('Un autre point est trois petits pas avant le point étudié. Donner son abscisse comme entier plus fraction.','Reculer en gardant le même pas.',r'Le point étudié est $\frac{29}8$. Trois pas avant donnent $\frac{26}8=3+\frac28$.',r'$3+\frac28$.',[test('Fraction(29,8)-Fraction(3,8)==3+Fraction(2,8)',True)]),
  q('Pour obtenir 4 avec un dénominateur 15, faut-il ajouter 1 au numérateur 45 ou changer davantage de parts ?','Une unité supplémentaire contient quinze quinzièmes.',r'$4=\frac{60}{15}$. Il faut $60-45=15$ parts supplémentaires.','Ajouter 15 au numérateur, et non 1.',[test('60-45',15)]),
  q('Après l’assemblage, on retire une unité. Quelle longueur reste-t-il ?','Une unité correspond à douze douzièmes.',r'La longueur assemblée est $\frac{46}{12}$. Après retrait d’une unité : $\frac{46}{12}-\frac{12}{12}=\frac{34}{12}=2+\frac{10}{12}$.',r'$2+\frac{10}{12}$ unités.',[test('Fraction(46,12)-1==2+Fraction(10,12)',True)])],
 [q(r'Intercaler une fraction de dénominateur 60 strictement entre $\frac{47}{60}$ et $\frac{49}{60}$. Est-elle unique avec ce dénominateur ?','Chercher un numérateur entier entre les deux numérateurs.','Seul 48 est strictement entre 47 et 49.',r'$\frac{48}{60}$ ; oui, avec ce dénominateur elle est unique.',[test('[n for n in range(48,49)]',[48])]),
  q(r'Une bande de $\frac{17}8$ unité est-elle plus longue que deux bandes de $\frac{17}{12}$ unité mises bout à bout ?','Calculer la longueur répétée puis utiliser les vingt-quatrièmes.',r'Deux bandes font $\frac{34}{12}=\frac{68}{24}$ unité. L’autre fait $\frac{17}8=\frac{51}{24}$. Comme $51<68$, elle est plus courte.',r'Non : $\frac{17}8<2\times\frac{17}{12}$.',[test('Fraction(17,8)<2*Fraction(17,12)',True)]),
  q('Trouver une fraction de dénominateur 60 entre les deux fractions étudiées, qui ne soit pas égale à 1.','Réécrire les bornes en soixantièmes puis choisir un numérateur.',r'$\frac{59}{60}<\frac{61}{60}<\frac{63}{60}=\frac{21}{20}$. Le numérateur 61 n’est pas 60.',r'Par exemple $\frac{61}{60}$.',[test('Fraction(59,60)<Fraction(61,60)<Fraction(21,20) and Fraction(61,60)!=1',True)]),
  q(r'Compléter $\frac{7}{12}=\frac{\square}{60}=\frac{14}{\square}$.','Appliquer séparément les facteurs 5 et 2.','Le passage de 12 à 60 multiplie par 5, donc le premier numérateur est 35. Le passage de 7 à 14 multiplie par 2, donc le dernier dénominateur est 24.','35 et 24.',[test('Fraction(7,12)==Fraction(35,60)==Fraction(14,24)',True)]),
  q(r'Sans nouveau dessin, quelle fraction faut-il ajouter à $\frac75$ pour obtenir $\frac{17}{12}$ ?','Utiliser les soixantièmes déjà calculés.',r'$\frac{17}{12}=\frac{85}{60}$ et $\frac75=\frac{84}{60}$. Il manque un soixantième.',r'$\frac1{60}$.',[test('Fraction(17,12)-Fraction(7,5)',[1,60])]),
  q('Peut-on intercaler une fraction de dénominateur 60 entre chacune des trois fractions rangées ?','Observer les numérateurs après mise au même dénominateur.',r'Les trois fractions valent $\frac{42}{60}$, $\frac{44}{60}$ et $\frac{51}{60}$. On peut choisir $\frac{43}{60}$ puis $\frac{45}{60}$.',r'Oui : $\frac{43}{60}$ et $\frac{45}{60}$ conviennent.',[test('Fraction(7,10)<Fraction(43,60)<Fraction(11,15)<Fraction(45,60)<Fraction(17,20)',True)]),
  q('Quel nombre faut-il ajouter à la somme calculée pour obtenir une unité ?','Compléter les quarantièmes jusqu’à 40.',r'La somme vaut $\frac{16}{40}$. Il manque $40-16=24$ quarantièmes.',r'$\frac{24}{40}$.',[test('1-(Fraction(11,40)+Fraction(1,8))',dump_value(Fraction(24,40)))])],
 [q('On prend ensuite la moitié des jetons restants. Combien de jetons a-t-on pris au total ?','La seconde fraction porte sur le reste, pas sur le stock initial.','La première prise vaut 60 et il reste 36 jetons. La moitié de 36 vaut 18. Au total, $60+18=78$.','78 jetons.',[test('96*Fraction(5,8)+(96-60)*Fraction(1,2)',78)]),
  q('On partage la quantité prélevée en cinq verres égaux. Quel volume reçoit chaque verre ?','Utiliser la quantité calculée, et non la capacité totale.',r'Les sept douzièmes de 1 200 mL valent 700 mL. Puis $700\div5=140$.','140 mL par verre.',[test('(1200*Fraction(7,12))/5',140)]),
  q('On livre ensuite un tiers des objets encore disponibles. Combien reste-t-il après les deux livraisons ?','Recalculer le nouveau tout pour le second prélèvement.','Après la première livraison, il reste $180-105=75$. Un tiers de 75 vaut 25. Il reste donc $75-25=50$.','50 objets.',[test('(180-180*Fraction(7,12))*(1-Fraction(1,3))',50)]),
  q('Combien faudrait-il ajouter au premier lot avant le prélèvement pour obtenir exactement 65 objets en prenant ses cinq huitièmes ?','Chercher la quantité d’une part puis le tout.',r'65 objets correspondent à cinq parts, donc une part vaut $65\div5=13$. Le tout doit être $13\times8=104$. Il faut ajouter $104-96=8$.','8 objets à ajouter.',[test('(65//5)*8-96',8)]),
  q('On raccourcit chaque ruban d’un huitième de mètre avant l’assemblage. Quelle est la nouvelle longueur totale ?','Modifier une longueur puis la répéter sept fois.',r'Chaque ruban mesure maintenant $\frac{10}8$ m. Sept rubans font $7\times\frac{10}8=\frac{70}8=8+\frac68$ m.',r'$8+\frac68$ m.',[test('7*(Fraction(11,8)-Fraction(1,8))==8+Fraction(6,8)',True)]),
  q('Un autre élève multiplie directement 35 par 8 et annonce le tout. Expliquer précisément son erreur.','Les 35 objets représentent cinq parts et non une seule.','Il doit d’abord partager 35 par 5 pour obtenir 7 objets par part, puis multiplier par 8. Multiplier 35 par 8 compte cinq fois trop.','Le tout vaut 56, pas 280.',[test('35//5*8',56),test('35*8',280)]),
  q('Si l’on réserve seulement les deux tiers du stock, peut-on encore couvrir le même besoin de 100 feuilles ? Comparer les deux réserves.','Calculer le nouveau prélèvement et garder le même stock de départ.',r'Deux tiers de 180 font $180\div3\times2=120$, contre 105 pour sept douzièmes. Le nouveau prélèvement couvre 100 feuilles avec 20 feuilles de marge.','Oui : 120 feuilles réservées, soit 15 de plus et une marge de 20.',[test('180*Fraction(2,3)',120),test('120-105',15),test('120-100',20)])],
 [q('Dans $208{,}007$, combien de millièmes sont contenus au total, unités comprises ?','Transformer aussi les unités en millièmes.','208 unités donnent 208 000 millièmes, auxquels on ajoute 7 millièmes.','208 007 millièmes.',[test('208*1000+7',208007)]),
  q(r'Un élève propose $12{,}508=12+\frac5{100}+\frac8{1\,000}$. Corriger sans changer le nombre de départ.','Le 5 est au rang des dixièmes.',r'Il faut écrire $12+\frac5{10}+\frac8{1\,000}$. L’écriture proposée vaut seulement $12{,}058$.',r'$12{,}508=12+\frac5{10}+\frac8{1\,000}$.',[test('12+Fraction(5,10)+Fraction(8,1000)',dump_value(Fraction(12508,1000)))]),
  q('Trouver un nombre de trois décimales compris entre $12{,}005$ et $12{,}05$, dont le zéro final peut être retiré.','Choisir un centième entier strictement entre les bornes.','$12{,}020=12{,}02$ est plus grand que $12{,}005$ et plus petit que $12{,}050$.','Par exemple $12{,}020$.',[test('Fraction(12005,1000)<Fraction(12020,1000)<Fraction(1205,100)',True)]),
  q('Combien de nombres ayant exactement trois chiffres après la virgule sont strictement entre les deux plus petits nombres de la liste ?','Compter les millièmes intermédiaires.','Les deux plus petits sont $12{,}005$ et $12{,}009$. Les millièmes intermédiaires sont $12{,}006$, $12{,}007$ et $12{,}008$.','3 écritures à trois décimales.',[test('12009-12005-1',3)]),
  q('Trouver un nombre strictement entre $17{,}009$ et $17{,}01$, avec au plus trois décimales, ou expliquer pourquoi c’est impossible.','Traduire les deux bornes en millièmes.','Les bornes sont deux millièmes consécutifs : 17 009 et 17 010 millièmes. Aucun entier de millièmes ne s’intercale.','Impossible avec au plus trois décimales.',[test('17010-17009',1)]),
  q('La fenêtre est-elle suffisante pour placer $12{,}025$ ? Justifier.','Comparer le nombre à la borne droite.','Vingt pas de $0{,}001$ après 12 conduisent à $12{,}020$. Le point $12{,}025$ est au-delà de cette borne.','Non : il est 5 millièmes après la borne droite.',[test('12025-(12000+20)',5)]),
  q('Quel est le plus petit nombre de partie entière 99, écrit au millième, dont l’arrondi à l’entier vaut 100 ?','La frontière de l’arrondi est à mi-chemin de 99 et 100.','La frontière est $99{,}500$. Tout millième inférieur a un chiffre des dixièmes inférieur à 5 ; à la frontière, on arrondit à 100.','$99{,}500$.',[test('(99500+500)//1000',100),test('(99499+500)//1000',99)])]
]

def main():
    for index,slug in enumerate(SLUGS):
        p=ROOT/slug
        jwrite(p/'etat.json',{'statut':'en_cours','agent':'cm2_nombres','maj':'2026-11-01'})
        title,body=COURSES[index]
        write(p/'cours_nouveau.txt','Titre: '+title+'\n\n'+MARK+'\n'+body)
        write(p/'fiche_nouvelle.txt','Titre: '+title+' — Synthèse\n\n'+MARK+'\n'+FICHES[index])
        docs=[];manifest=[]
        for level in range(3):
            for fam in range(7):
                i=level*7+fam+1
                result=BUILDERS[index](level,fam)
                if level==2: result[1].append(HARD[index][fam])
                ex,info=exercise(i,FAMILIES[index][fam],result[1],level,result[0],result[2] if len(result)>2 else '')
                docs.append(ex);manifest.append(info)
        write(p/'exercices.txt','\n===\n\n'.join(docs))
        jwrite(p/'verification_questions.json',manifest)
        for ex in manifest:
            for k,question in enumerate(ex['questions'],1):
                for expr,expected in question['check']:
                    actual=dump_value(calc(expr))
                    assert actual==expected,(slug,ex['id'],k,expr,actual,expected)
        jwrite(p/'figures'/'correspondance.json',{'cours':{'nouveau':{}},'fiches':{'nouvelle':{}},'exercices':{}})
        print(slug,len(manifest),'exercices rédigés, calculs contrôlés')

if __name__=='__main__': main()

