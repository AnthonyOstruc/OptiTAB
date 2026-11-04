"""Cours et fiches des notions 261 à 265, rédigés pour la Cinquième."""
from pathlib import Path
import json
import runpy

ROOT=Path(__file__).resolve().parent.parent
TEXTES={
261:(r'''
::: objectifs
- Traduire un problème par une expression et choisir les opérations utiles.
- Respecter les priorités et les parenthèses.
- Diviser par un décimal non nul et contrôler le résultat.
:::

## I. Lire une expression

::: definition Termes et facteurs
Une **somme** réunit des termes ; une **différence** soustrait un terme à un autre. Un **produit** multiplie des facteurs. Un **quotient** divise un dividende par un diviseur non nul.
La nature d’une expression est donnée par la dernière opération à effectuer.
:::

::: exemple Les parenthèses changent la lecture
$7+3\times4$ est la somme de $7$ et du produit $3\times4$. Son résultat est $19$.

$(7+3)\times4$ est le produit de la somme $7+3$ par $4$. Son résultat est $40$.
:::

## II. Respecter les priorités

::: methode L’ordre des calculs
1. Calculer les parenthèses, en commençant par les plus intérieures.
2. Effectuer les multiplications et les divisions, de gauche à droite.
3. Effectuer les additions et les soustractions, de gauche à droite.

À chaque ligne, recopier les parties encore inchangées.
:::

::: exemple Sans parenthèses
$$
\begin{aligned}
18-6\div3+2\times4&=18-2+8\\
&=16+8\\
&=24
\end{aligned}
$$
:::

::: attention À priorité égale
Une multiplication n’est pas prioritaire sur une division :
$$24\div3\times2=8\times2=16.$$
De même, $12-5+2=7+2=9$.
:::

::: exemple Avec parenthèses
$$
\begin{aligned}
(18-6)\div(3+2)\times4&=12\div5\times4\\
&=2{,}4\times4\\
&=9{,}6
\end{aligned}
$$
:::

## III. Diviser par un décimal

::: propriete Conserver le quotient
Multiplier le dividende et le diviseur par un même nombre non nul ne change pas le quotient. On choisit $10$, $100$ ou $1\,000$ pour rendre le diviseur entier.
:::

::: exemple Calculer puis vérifier
$$
\begin{aligned}
7{,}56\div0{,}6&=75{,}6\div6\\
&=12{,}6
\end{aligned}
$$
Contrôle : $12{,}6\times0{,}6=7{,}56$.
:::

::: attention Deux réflexes
- La division par zéro est impossible.
- Diviser un nombre positif par un nombre compris entre $0$ et $1$ peut l’augmenter : $3\div0{,}5=6$.
:::

## IV. Résoudre un problème et contrôler

::: methode Du texte au calcul
Repérer les données, la question et les unités. Traduire « pour chaque » par une multiplication ; ajouter une dépense globale une seule fois. Estimer le résultat, calculer, puis rédiger une phrase de réponse.
:::

::: exemple Une commande
Trois ateliers reçoivent chacun deux carnets à $4$ € pièce ; la livraison globale coûte $5$ €.
$$3\times2\times4+5=24+5=29.$$
La commande coûte $29$ €.
:::

::: propriete Distributivité numérique
$$k\times(a+b)=k\times a+k\times b.$$
De même, $k\times(a-b)=k\times a-k\times b$.
Pour calculer $17\times99$, écrire $17\times(100-1)=1\,700-17=1\,683$.
:::

::: retenir
Pour $19{,}8\times5{,}1$, l’estimation $20\times5=100$ permet de contrôler le résultat exact $100{,}98$.
Un nombre de contenants doit être entier : $23\div4=5{,}75$, mais il faut **six** boîtes de quatre places pour emporter 23 objets.
:::
''',r'''
::: objectifs
Priorités, division décimale et problèmes : les réflexes essentiels.
:::

## I. Calculer dans le bon ordre
::: retenir
**Parenthèses**, puis **multiplications et divisions**, puis **additions et soustractions**. À priorité égale : de gauche à droite.
$$18-6\div3=18-2=16.$$
$$24\div3\times2=8\times2=16.$$
:::

## II. Diviser et contrôler
::: methode
Multiplier les deux nombres par $10$, $100$… pour rendre le diviseur entier.
$$7{,}56\div0{,}6=75{,}6\div6=12{,}6.$$
Contrôler : $12{,}6\times0{,}6=7{,}56$.
:::

## III. Choisir l’expression
::: retenir
Regrouper les quantités avec des parenthèses. Ajouter les frais globaux une seule fois. Estimer le résultat et écrire l’unité dans la réponse.
$$k\times(a+b)=k\times a+k\times b.$$
:::

::: attention
Ne jamais diviser par zéro. Pour emporter 23 objets dans des boîtes de quatre, il faut **six boîtes**, même si $23\div4=5{,}75$.
:::
'''),
262:(r'''
::: objectifs
- Effectuer et interpréter une division euclidienne.
- Reconnaître des multiples et des diviseurs.
- Organiser une recherche de partages ou de rendez-vous périodiques.
:::

## I. Quotient entier et reste

::: definition Division euclidienne
Diviser un entier $a\ge0$ par un entier $b>0$, c’est trouver deux entiers $q$ et $r$ tels que :
$$a=b\times q+r\qquad\text{avec }0\le r<b.$$
$q$ est le **quotient entier**, $r$ le **reste**.
:::

::: exemple Ranger 83 objets
$$83=7\times11+6.$$
On remplit 11 boîtes de sept objets et il reste six objets. Comme $0\le6<7$, le reste est autorisé. Il faut **12 boîtes** pour ranger tous les objets.
:::

::: attention Vérifier le reste
L’égalité seule ne suffit pas : $83=7\times10+13$ est vraie, mais ce n’est pas la division euclidienne par 7, car $13\ge7$.
:::

## II. Multiples et diviseurs

::: definition Deux façons de lire un produit
Un entier $a$ est un **multiple** d’un entier $b>0$ si $a=b\times q$ pour un entier $q$. On dit aussi que **$b$ divise $a$**, que $b$ est un **diviseur** de $a$, ou que $a$ est **divisible** par $b$.
Le reste de la division euclidienne de $a$ par $b$ est alors nul.
:::

::: exemple
$36=9\times4$ : 36 est un multiple de 9 et 9 est un diviseur de 36.
Les premiers multiples de 7 sont $0$, $7$, $14$, $21$… Ils sont en nombre infini.
:::

::: methode Trouver tous les diviseurs
Chercher les produits donnant le nombre, par paires :
$$24=1\times24=2\times12=3\times8=4\times6.$$
Les diviseurs positifs de 24 sont $1$, $2$, $3$, $4$, $6$, $8$, $12$ et $24$.
:::

## III. Reconnaître une divisibilité

::: propriete Critères utiles
| Divisible par… | Condition |
|---|---|
| $2$ | Chiffre des unités : $0$, $2$, $4$, $6$ ou $8$ |
| $3$ | Somme des chiffres divisible par $3$ |
| $5$ | Chiffre des unités : $0$ ou $5$ |
| $9$ | Somme des chiffres divisible par $9$ |
| $10$ | Chiffre des unités : $0$ |
:::

::: exemple
Pour 234, $2+3+4=9$ : 234 est divisible par 3 et par 9. Il est aussi divisible par 2 car il est pair. Il n’est divisible ni par 5 ni par 10.
:::

## IV. Choisir une recherche organisée

::: methode Des lots identiques sans reste
Le nombre de lots doit diviser **chaque** effectif. Lister leurs diviseurs et garder ceux qui sont communs.
:::

::: exemple
Avec 12 cartes rouges et 18 cartes bleues, les nombres de lots possibles sont $1$, $2$, $3$ et $6$. Au maximum, on obtient six lots de deux rouges et trois bleues.
:::

::: methode Des rendez-vous périodiques
Écrire les multiples strictement positifs de chaque période. Le premier nombre commun donne la première rencontre après le départ.
:::

::: exemple
Un signal se répète toutes les 4 s, un autre toutes les 6 s.
- Premier : $4$, $8$, $12$…
- Second : $6$, $12$…
Ils se retrouvent à 12 s, puis 24 s, puis 36 s.
:::

::: attention
Additionner les périodes ne suffit pas : $4+6=10$, mais 10 n’est multiple ni de 4 ni de 6.
:::

::: remarque Pour aller plus loin : nombres premiers
Un nombre premier possède exactement deux diviseurs positifs : 1 et lui-même. 2, 3, 5 et 7 sont premiers ; 1 ne l’est pas.
:::
''',r'''
::: objectifs
Distinguer quotient, reste, multiples et diviseurs.
:::

## I. Division entière
::: retenir
$$a=b\times q+r\quad\text{avec }0\le r<b.$$
Exemple : $83=7\times11+6$. Quotient 11, reste 6 ; **12 boîtes** de sept pour tout ranger.
:::

## II. Divisibilité
::: retenir
$36=9\times4$ : 36 est un **multiple** de 9 ; 9 est un **diviseur** de 36.
- Par 2 : chiffre des unités pair.
- Par 3 ou 9 : somme des chiffres divisible par 3 ou 9.
- Par 5 : finit par 0 ou 5 ; par 10 : finit par 0.
:::

## III. Les deux recherches
::: methode
**Lots identiques sans reste** : diviseurs communs à tous les effectifs.

**Rendez-vous périodiques** : multiples communs aux périodes.
:::

::: attention
Le reste doit être inférieur au diviseur. Tester seulement le total oublie les couleurs des lots. Additionner deux périodes ne donne pas forcément une rencontre.
:::
'''),
263:(r'''
::: objectifs
- Lire et placer des nombres relatifs sur une droite graduée.
- Reconnaître des opposés et calculer des distances à zéro.
- Comparer et ranger des nombres relatifs, y compris décimaux.
:::

## I. Donner un sens au signe

::: definition Nombre relatif
Un nombre relatif peut être positif, comme $+3$ ou $2{,}5$, ou négatif, comme $-4$ ou $-0{,}5$. Le signe $+$ peut être omis ; le signe $-$ doit être conservé.
Une température de $-4$ °C se situe quatre degrés sous zéro.
:::

::: remarque Le cas de zéro
Zéro est à la fois positif et négatif. Un nombre **strictement positif** est supérieur à zéro ; un nombre **strictement négatif** est inférieur à zéro.
:::

## II. Se repérer sur une droite

::: definition Abscisse
Une droite graduée possède une origine $O$, un sens positif et une unité de longueur. L’**abscisse** d’un point est le nombre qui repère sa position. Des graduations consécutives représentent toujours le même écart.
:::

[IMAGE_1]

::: methode Placer un nombre
Depuis zéro, se déplacer vers la droite pour un positif et vers la gauche pour un négatif. Pour placer $-1{,}5$, prendre une unité et demie à gauche de zéro.
:::

## III. Distance à zéro et opposé

::: definition Distance à zéro
La distance à zéro d’un nombre est le nombre d’unités entre sa position et l’origine. Elle est positive ou nulle. Ainsi, $-3$ et $3$ ont la même distance à zéro : 3.
:::

::: definition Nombres opposés
Deux nombres opposés ont la même distance à zéro et se situent de part et d’autre de zéro. L’opposé de $-3$ est $3$ ; l’opposé de $3$ est $-3$. L’opposé de zéro est zéro.
:::

::: attention
Le signe et la distance à zéro sont deux informations distinctes. La distance de $-7$ à zéro vaut $7$, jamais $-7$.
:::

## IV. Comparer et ranger

::: propriete Lire de gauche à droite
Sur une droite orientée vers la droite, les abscisses augmentent de gauche à droite.
- Un nombre strictement négatif est inférieur à zéro et à tout nombre positif.
- Entre deux nombres négatifs, le plus éloigné de zéro est le plus petit.
:::

::: exemple Des comparaisons expliquées
$-7<-2$ : le point d’abscisse $-7$ est à gauche de celui d’abscisse $-2$.

$-2{,}8<-2{,}35$ : $-2{,}80$ est plus éloigné de zéro que $-2{,}35$.

Dans l’ordre croissant : $-4<-1{,}5<0<2$.
:::

::: methode Encadrer un décimal
Entre $-1{,}4$ et $-1{,}3$, on peut placer $-1{,}35$ :
$$-1{,}4<-1{,}35<-1{,}3.$$
Ajouter un zéro à droite de la partie décimale ne change pas le nombre : $-1{,}4=-1{,}40$.
:::

::: retenir
Pour comparer des abscisses, lire de gauche à droite. Pour comparer des distances à zéro, oublier le signe et mesurer l’éloignement de l’origine.
:::
''',r'''
::: objectifs
Lire un signe, comparer une position, mesurer une distance.
:::

## I. Signe et position
::: retenir
Sur une droite graduée : les strictement négatifs sont à gauche de zéro, les strictement positifs à droite. L’unité reste constante ; les abscisses augmentent de gauche à droite.
$$-4<-1{,}5<0<2.$$
:::

## II. Opposés et distances
::: definition
$-3$ et $3$ sont opposés : même distance à zéro, 3, de part et d’autre de l’origine.
L’opposé de zéro est zéro. Une distance est toujours positive ou nulle.
:::

## III. Comparer des négatifs
::: methode
Le plus éloigné de zéro est le plus petit :
$$-7<-2\qquad -2{,}8<-2{,}35.$$
Pour comparer des décimaux, compléter si utile avec des zéros : $-2{,}8=-2{,}80$.
:::

::: attention
Distance de $-7$ à zéro : **7**. Ne pas confondre ordre des abscisses et ordre des distances. Zéro n’est ni strictement positif ni strictement négatif.
:::
'''),
264:(r'''
::: objectifs
- Additionner des relatifs de même signe ou de signes contraires.
- Transformer une soustraction en addition.
- Distinguer une valeur, une variation et une distance.
:::

## I. Additionner deux relatifs

::: propriete Même signe
Additionner les distances à zéro et garder le signe commun.
$$(-4)+(-3)=-(4+3)=-7.$$
$$ (+4)+(+3)=+7.$$
:::

::: propriete Signes contraires
Soustraire la plus petite distance à zéro à la plus grande. Garder le signe du nombre le plus éloigné de zéro. Deux opposés ont une somme nulle.
:::

::: exemple
$(-8)+5=-3$, car $8-5=3$ et le nombre le plus éloigné de zéro est négatif.

$(-2)+7=5$, car $7-2=5$ et le nombre le plus éloigné de zéro est positif.

$(-6)+6=0$.
:::

Sur la figure, on part de $-2$ et on ajoute $6$ : on arrive à $4$.

[IMAGE_1]

::: methode Sur une droite graduée
Ajouter un nombre positif déplace vers la droite ; ajouter un négatif déplace vers la gauche. Le point de départ représente le premier nombre et le point d’arrivée la somme.
:::

## II. Soustraire un relatif

::: propriete Ajouter l’opposé
$$a-b=a+(-b).$$
Soustraire $-5$ revient à ajouter $+5$ ; soustraire $+5$ revient à ajouter $-5$.
:::

::: exemple
$$3-(-5)=3+5=8.$$
$$3-(+5)=3+(-5)=-2.$$
:::

::: attention Les deux signes ont des rôles différents
Dans $3-(-5)$, le premier signe $-$ est l’opération de soustraction ; le second appartient au nombre $-5$.
:::

## III. Simplifier une suite de calculs

::: methode Parenthèses et regroupements
Transformer d’abord chaque soustraction en addition de l’opposé. Dans une somme, on peut changer l’ordre des termes et regrouper les opposés.
:::

::: exemple
$$
\begin{aligned}
(-4)+(+6)-(-2)&=-4+6+2\\
&=4
\end{aligned}
$$
$$
\begin{aligned}
-7+4+7-2&=(-7+7)+(4-2)\\
&=0+2=2
\end{aligned}
$$
:::

::: attention Parenthèse soustraite
Dans $8-(3-5)$, calculer d’abord la parenthèse : $3-5=-2$, puis $8-(-2)=10$.
Si on enlève directement la parenthèse, les deux signes changent : $8-3+5=10$.
:::

## IV. Valeur, variation ou distance ?

::: definition Variation
$$\text{variation}=\text{valeur finale}-\text{valeur initiale}.$$
Une variation positive indique une hausse ; une variation négative indique une baisse ; une variation nulle indique un retour à la même valeur.
:::

::: exemple Une température
De $-6$ °C à $2$ °C, la variation vaut $2-(-6)=8$ °C. La température finale est **2 °C** ; la hausse est de **8 °C**. Pour revenir au départ, la variation nécessaire est $-8$ °C.
:::

::: retenir
La différence $-2-5=-7$ peut être négative. La distance entre les abscisses $-2$ et $5$ vaut $5-(-2)=7$ unités : une distance est toujours positive ou nulle.
:::
''',r'''
::: objectifs
Les règles de calcul avec les relatifs et leur interprétation.
:::

## I. Additionner
::: retenir
**Même signe** : additionner les distances à zéro et garder ce signe.
$$(-4)+(-3)=-7.$$
**Signes contraires** : soustraire les distances ; garder le signe du plus éloigné de zéro.
$$(-8)+5=-3\qquad (-2)+7=5.$$
Deux opposés ont une somme nulle.
:::

## II. Soustraire
::: formule
$$a-b=a+(-b).$$
:::
$3-(-5)=3+5=8$ ; $3-5=-2$.

## III. Interpréter
::: methode
Variation = valeur finale − valeur initiale.
De $-6$ °C à $2$ °C : variation $+8$ °C ; retour : variation $-8$ °C.
:::

::: attention
Une différence peut être négative, une distance ne l’est jamais. Ne pas confondre une température finale et sa variation.
:::
'''),
265:(r'''
::: objectifs
- Comprendre une fraction comme quotient et comme partage d’une unité.
- Produire des fractions égales et prendre une fraction d’une quantité.
- Comparer des fractions et les placer sur une droite graduée.
:::

## I. Une fraction est un nombre

::: definition Quotient et fraction
Pour $b\ne0$, le quotient $\frac{a}{b}$ est le nombre qui, multiplié par $b$, donne $a$.
Une **fraction** est le quotient de deux entiers, avec un dénominateur non nul.
Dans $\frac34$, le dénominateur 4 partage l’unité en quatre parts égales ; le numérateur 3 compte trois de ces parts.
:::

[IMAGE_1]

::: attention Choisir la même unité
Trois quarts de deux rubans de longueurs différentes ne donnent pas la même longueur. Pour comparer des portions par leurs fractions, il faut la même unité de référence.
:::

## II. Écrire des fractions égales

::: propriete Conserver le quotient
Multiplier ou diviser le numérateur **et** le dénominateur par le même nombre non nul conserve la valeur.
$$\frac34=\frac68=\frac{15}{20}.$$
Pour simplifier $\frac{18}{24}$, diviser les deux termes par 6 : on obtient $\frac34$.
:::

::: exemple Écriture décimale et valeur exacte
$$1{,}25=\frac{125}{100}=\frac54=1+\frac14.$$
Une fraction peut dépasser 1 : $\frac74=1+\frac34$.
En revanche, $\frac13$ n’a pas d’écriture décimale finie : $0{,}33$ en est une approximation, pas la valeur exacte.
:::

## III. Prendre une fraction d’une quantité

::: methode Partager puis multiplier
Pour prendre $\frac{a}{b}$ d’une quantité, diviser cette quantité par $b$, puis multiplier le résultat par $a$.
:::

::: exemple Trois quarts de 20 L
Une part représente $20\div4=5$ L ; trois parts représentent $5\times3=15$ L.
Il reste $\frac14$ de la réserve initiale, soit 5 L.
:::

## IV. Comparer des fractions

::: propriete Parts de même taille
À dénominateur positif identique, comparer les numérateurs :
$$\frac38<\frac58.$$
À numérateur positif identique, le plus petit dénominateur donne la plus grande fraction :
$$\frac25<\frac23.$$
:::

::: methode Trouver un dénominateur commun
Pour comparer $\frac58$ et $\frac7{12}$, écrire des fractions égales au dénominateur 24 :
$$\frac58=\frac{15}{24}\qquad\frac7{12}=\frac{14}{24}.$$
Comme $15>14$, on a $\frac58>\frac7{12}$.
:::

::: conseil Comparer à un repère
$\frac34>\frac12$ car trois quarts dépassent deux quarts.
$\frac75>1$ car le numérateur dépasse le dénominateur positif.
:::

## V. Placer une fraction sur une droite

::: methode Décomposer en partie entière et fraction
La division euclidienne $11=4\times2+3$ donne :
$$\frac{11}{4}=2+\frac34.$$
Partager l’intervalle de 2 à 3 en quatre parts égales et avancer de trois parts à partir de 2.
:::

::: retenir
Ne pas comparer les dénominateurs seuls. Ne jamais modifier seulement un des deux termes pour fabriquer une fraction égale. Garder une fraction exacte quand l’écriture décimale est infinie.
:::
''',r'''
::: objectifs
Comprendre, transformer et comparer les fractions.
:::

## I. Une fraction : un quotient
::: definition
Dans $\frac34$, 4 partage l’unité en parts égales et 3 compte les parts prises. Le dénominateur n’est jamais nul.
$$\frac34=\frac68=\frac{15}{20}.$$
Multiplier ou diviser **les deux termes** par le même nombre non nul conserve la valeur.
:::

## II. Calculer une portion
::: methode
Diviser la quantité par le dénominateur, puis multiplier par le numérateur.
Trois quarts de 20 L : $20\div4\times3=15$ L.
:::

## III. Comparer et placer
::: retenir
À même dénominateur positif : comparer les numérateurs. Sinon, écrire des fractions égales au même dénominateur.
$$\frac58=\frac{15}{24}>\frac{14}{24}=\frac7{12}.$$
Pour placer $\frac{11}4=2+\frac34$, partager l’unité en quatre et compter trois quarts après 2.
:::

::: attention
Les portions doivent concerner la même unité. $\frac13\ne0{,}33$ : garder la fraction pour une valeur exacte. $\frac25<\frac23$, malgré $5>3$.
:::
''')}

for p in sorted(ROOT.iterdir()):
    if p.name[:3] not in {str(n) for n in TEXTES}: continue
    n=int(p.name[:3]); meta=json.loads((p/'source_en_ligne/meta.json').read_text(encoding='utf8'))
    for group,stem,index in [('cours','cours',0),('fiches','fiche',1)]:
        entry=meta[group][0]
        (p/f'{stem}_{entry["id"]}.txt').write_text('Titre: '+entry['titre']+'\n\n<!-- optitab:1 -->\n'+TEXTES[n][index].strip()+'\n',encoding='utf8')
    fp=p/'figures/figures.py'; figures=runpy.run_path(str(fp))['FIGURES']; corr=json.loads((p/'figures/correspondance.json').read_text(encoding='utf8'))
    if n==263:
        ns=runpy.run_path(str(Path(__file__).with_name('ameliorer_261_265.py')))
        figures['cours_relatifs']=ns['numberline']([('A',-3),('O',0),('B',3)],-4,4)
    if n==264:
        figures['cours_addition']=r'''\begin{tikzpicture}[x=.75cm,y=1cm]
\draw[geoVecteur] (-5,0)--(5,0);
\foreach \x in {-4,...,4}{\draw[otMuted] (\x,-.06)--(\x,.06);\node[below=7pt,text=otMuted] at (\x,0) {$\x$};}
\draw[geoReponse,-{Stealth}] (-2,.6)--(4,.6);
\draw[guide] (-2,.12)--(-2,.6);
\draw[guide] (4,.12)--(4,.6);
\node[text=otGreenDark] at (1,1) {$+6$};
\node[anchor=west,text=otInk] at (-4,-.8) {$(-2)+6=4$};
\end{tikzpicture}'''
    if n==265:
        figures['cours_fraction']=r'''\begin{tikzpicture}[x=1cm,y=1cm]
\fill[otNavy!18] (0,0) rectangle (5.25,.45);
\draw[geoTrait] (0,0) rectangle (7,.45);
\draw[geoTrait] (1.75,0)--(1.75,.45);
\draw[geoTrait] (3.5,0)--(3.5,.45);
\draw[geoTrait] (5.25,0)--(5.25,.45);
\node[anchor=west,text=otInk] at (0,1) {Une unité partagée en quatre parts égales};
\node[text=otNavy] at (3.5,-.45) {Trois parts prises : $\frac34$ de l’unité};
\end{tikzpicture}'''
    if n in (263,264,265):
        name={263:'cours_relatifs',264:'cours_addition',265:'cours_fraction'}[n]
        alt={263:'Droite graduée : les points A et B ont des abscisses opposées -3 et 3.',264:'Sur une droite graduée, partir de -2 et ajouter 6 conduit à 4.',265:'Une unité divisée en quatre parts égales, dont trois sont colorées.'}[n]
        corr['cours'][str(meta['cours'][0]['id'])]={'1':{'fichier':name+'.png','alt':alt}}
    fp.write_text('# -*- coding: utf-8 -*-\n"""Figures TikZ de la notion, palette des livres OptiTAB."""\nFIGURES = '+repr(figures)+'\n',encoding='utf8')
    (p/'figures/correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(n,'cours et fiche rédigés ;',len(figures),'figures')
