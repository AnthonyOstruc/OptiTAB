# -*- coding: utf-8 -*-
"""Rédaction locale des cinq chapitres attribués. Aucun accès à une base."""
from pathlib import Path
from decimal import Decimal as D
import json, re

BASE = Path(__file__).resolve().parent.parent
NAMES = ['07_operations-entiers','08_division','09_calculs-decimaux','10_proportionnalite','21_regularites']
def write(n, name, s):
    (BASE/n/name).write_text(s.strip()+'\n',encoding='utf-8')

COURSES = [r'''
Titre: Additionner, soustraire et multiplier des entiers
<!-- optitab:1 -->
::: objectifs
- Choisir une opération pour résoudre un problème.
- Calculer de tête ou poser une addition, une soustraction et une multiplication.
- Estimer, utiliser des parenthèses et contrôler un résultat.
:::

## I. Donner du sens aux opérations
::: definition Somme, différence et produit
Une addition réunit des quantités ou traduit un ajout. Son résultat est une **somme**. Une soustraction permet de chercher ce qui reste, un écart ou une quantité manquante. Son résultat est une **différence**. Une multiplication permet de compter des groupes de même taille. Son résultat est un **produit**.
:::
::: exemple Le stock de livres
La bibliothèque possède 1 246 livres et en reçoit 378 : $1\,246+378=1\,624$. Si elle en prête 195, il reste $1\,624-195=1\,429$ livres. Quatre cartons de 125 livres contiennent $4\times125=500$ livres.
:::
[IMAGE_1]
::: attention Lire la question
Le mot « plus » ne demande pas toujours une addition. Lila a 37 cartes, soit 12 de plus que Noé. Noé a donc $37-12=25$ cartes.
:::

## II. Calculer de tête en choisissant un chemin
::: methode Décomposer ou compenser
Chercher un nombre rond, regrouper ce qui se calcule facilement, puis terminer. Pour ajouter 99, on peut ajouter 100 puis retirer 1. Pour retirer 99, on peut retirer 100 puis ajouter 1.
:::
::: exemple
$$\begin{aligned}
648+99&=648+100-1\\
&=748-1\\
&=747
\end{aligned}$$
Pour multiplier par 25, on peut multiplier par 100 puis prendre deux fois la moitié : $36\times25=900$.
:::
::: propriete Décomposer un produit
On peut décomposer un facteur : $24\times13=(24\times10)+(24\times3)=240+72=312$. On peut aussi changer l'ordre des facteurs et les regrouper : $4\times17\times25=17\times100=1\,700$.
:::

## III. Poser les opérations
::: methode Addition et soustraction
1. Aligner les unités sous les unités, les dizaines sous les dizaines, etc.
2. Calculer en commençant par les unités.
3. Dans l'addition, échanger 10 unités d'un rang contre 1 unité du rang suivant. Dans la soustraction, effectuer les échanges nécessaires.
4. Contrôler par estimation ou par l'opération inverse.
:::
::: exemple Soustraction avec des zéros
Pour $4\,002-785$, on échange 1 millier en 10 centaines, puis 1 centaine en 10 dizaines et 1 dizaine en 10 unités. On dispose de 3 milliers, 9 centaines, 9 dizaines et 12 unités. On obtient $3\,217$. Contrôle : $3\,217+785=4\,002$.
:::
::: methode Multiplier par un nombre à deux chiffres
Pour $326\times24$, calculer d'abord $326\times4=1\,304$, puis $326\times20=6\,520$. Additionner les deux produits : $1\,304+6\,520=7\,824$. La seconde ligne représente des dizaines : elle ne vaut pas $326\times2$.
:::

## IV. Parenthèses et contrôle
::: methode Respecter les groupements
Calculer d'abord ce qui se trouve dans chaque paire de parenthèses, puis terminer. Avec deux paires, traiter chacune avant de les combiner.
:::
::: exemple
$$\begin{aligned}
(36+14)\times(20-8)&=50\times12\\
&=600
\end{aligned}$$
:::
::: retenir Résoudre un problème
Comprendre ce que l'on cherche ; choisir les opérations ; calculer ; répondre avec l'unité et vérifier que le résultat est plausible. Une estimation donne un ordre de grandeur : $398\times21$ est proche de $400\times20=8\,000$ ; le résultat exact est $8\,358$.
:::
''',r'''
Titre: Diviser et interpréter le quotient
<!-- optitab:1 -->
::: objectifs
- Résoudre des problèmes de partage et de groupement.
- Effectuer une division par un entier de 1 à 9.
- Distinguer quotient entier avec reste et quotient décimal exact.
- Contrôler et interpréter la réponse selon la situation.
:::

## I. Deux questions de division
::: definition Partager ou grouper
Partager 37 jetons entre 5 enfants, c'est chercher le nombre de jetons de chacun. Ranger 37 jetons en paquets de 5, c'est chercher le nombre de paquets. Dans les deux cas, $37=5\times7+2$ : le quotient entier est 7 et le reste est 2.
:::
[IMAGE_1]
::: propriete Division euclidienne
Le dividende est égal au diviseur multiplié par le quotient entier, plus le reste. Le diviseur est non nul ; le reste est positif ou nul et **strictement inférieur au diviseur**.
:::
::: exemple Le sens du reste
Avec 230 œufs, on remplit 38 boîtes de 6 et il reste 2 œufs : $230=6\times38+2$. Pour transporter tous les œufs dans ces boîtes, il en faut 39, dont la dernière n'est pas pleine.
:::

## II. Diviser chiffre après chiffre
::: methode Poser une division
Pour diviser $1\,258$ par 6, commencer à gauche. Les 12 centaines donnent 2 centaines au quotient, reste 0. Les 5 dizaines ne permettent aucune dizaine : écrire **0** au quotient. Les 58 unités donnent 9 unités, reste 4. Le quotient est 209.
$$1\,258=6\times209+4$$
Contrôler à la fois cette égalité et $4<6$.
:::
::: attention Le zéro du quotient
Omettre le zéro transformerait 209 en 29. Le quotient possède une place pour chaque rang traité, même si l'on obtient zéro à ce rang.
:::

## III. Poursuivre un partage dans les décimaux
::: methode Échanger le reste contre des dixièmes
Pour partager 27 m en 4 longueurs égales, le quotient entier est 6 et le reste est 3 m. Échanger ces 3 unités contre 30 dixièmes. Chaque part reçoit 7 dixièmes et il reste 2 dixièmes. Les échanger contre 20 centièmes : chaque part reçoit 5 centièmes. Le reste est nul.
$$27\div4=6{,}75$$
Contrôle : $6{,}75\times4=27$. Chaque longueur mesure donc $6{,}75$ m.
:::
::: methode Dividende décimal
Pour $8{,}7\div6$, 8 unités donnent 1 unité, reste 2 unités. Avec les 7 dixièmes, cela fait 27 dixièmes : chaque part reçoit 4 dixièmes, reste 3 dixièmes. Ces 30 centièmes donnent 5 centièmes par part.
$$8{,}7\div6=1{,}45$$
On place la virgule du quotient lorsqu'on commence à partager les dixièmes. Contrôle : $1{,}45\times6=8{,}7$.
:::

## IV. Choisir la réponse et vérifier
::: attention Objets indivisibles ou grandeurs partageables
On ne découpe pas un élève pour compléter un groupe. En revanche, une longueur ou une masse peut se partager en parts décimales. Lire la question permet de choisir entre quotient entier, nombre de récipients nécessaires et mesure exacte d'une part.
:::
::: retenir
Avant de diviser, estimer. Pendant le calcul, conserver tous les rangs. Après le calcul, multiplier pour vérifier, contrôler le reste éventuel et rédiger une réponse adaptée. Les divisions étudiées ici ont un diviseur entier à un chiffre ; pour les quotients décimaux demandés, le calcul se termine.
:::
''',r'''
Titre: Calculer avec les nombres décimaux
<!-- optitab:1 -->
::: objectifs
- Additionner et soustraire des décimaux en respectant les rangs.
- Multiplier un décimal par un entier.
- Multiplier et diviser par 10, 100 et 1 000.
- Calculer mentalement, utiliser des parenthèses et contrôler.
:::

## I. Additionner et soustraire
::: methode Aligner les rangs
Aligner les unités, les dixièmes, les centièmes et les millièmes : les virgules se trouvent alors dans la même colonne. On peut compléter la partie décimale par des zéros sans changer la valeur. Calculer de droite à gauche, en effectuant les échanges nécessaires.
:::
::: exemple
Pour $12{,}7+3{,}85$, écrire $12{,}70+3{,}85=16{,}55$. Pour $20-4{,}35$, écrire $20{,}00-4{,}35=15{,}65$. Le contrôle $15{,}65+4{,}35=20$ vérifie la différence.
:::
[IMAGE_1]
::: attention
Aligner les derniers chiffres ne suffit pas : $3{,}5+0{,}27=3{,}77$, car 5 dixièmes sont 50 centièmes.
:::

## II. Multiplier par un entier
::: methode Utiliser les unités de numération
Pour $6{,}38\times7$, penser à 638 centièmes. $638\times7=4\,466$ : le produit est 4 466 centièmes, soit $44{,}66$. On peut poser la multiplication comme avec des entiers puis donner au résultat la bonne unité de numération.
:::
::: exemple Un entier à deux chiffres
$$\begin{aligned}
2{,}35\times12&=(2{,}35\times10)+(2{,}35\times2)\\
&=23{,}5+4{,}7\\
&=28{,}2
\end{aligned}$$
Douze carnets à $2{,}35$ € coûtent $28{,}20$ €.
:::

## III. Multiplier ou diviser par 10, 100, 1 000
::: propriete La valeur des chiffres change
Multiplier par 10 donne à chaque chiffre une valeur dix fois plus grande : un centième devient un dixième. Multiplier par 100 ou 1 000 donne une valeur cent ou mille fois plus grande. Diviser produit le changement inverse.
$$3{,}456\times100=345{,}6$$
$$47{,}2\div100=0{,}472$$
:::
::: attention Les zéros ont un rôle
Multiplier un décimal par 10 ne consiste pas à ajouter un zéro à droite : $2{,}4\times10=24$, tandis que $2{,}40=2{,}4$. Pour $4{,}5\div1\,000=0{,}0045$, les zéros conservent la place des rangs.
:::

## IV. Choisir une procédure mentale
::: methode Décomposer
Pour additionner, on peut réunir les unités puis les dixièmes : $4{,}7+2{,}8=6+1{,}5=7{,}5$. Pour multiplier par 5, multiplier par 10 puis prendre la moitié : $3{,}6\times5=36\div2=18$.
:::
::: exemple Doubles et moitiés
Le double de $3{,}45$ est $6{,}9$. La moitié de $7{,}3$ est $3{,}65$ : $3{,}65+3{,}65=7{,}3$. Pour diviser par 4, prendre deux fois la moitié : $18\div4=9\div2=4{,}5$.
:::
::: methode Parenthèses et estimation
Calculer d'abord chaque parenthèse : $(4{,}5+1{,}5)\times(9-6)=6\times3=18$. Estimer avant un long calcul : $19{,}8\times6$ est proche de $20\times6=120$ ; le produit exact $118{,}8$ est plausible.
:::
::: retenir
Dans une somme ou une différence, aligner les rangs. Dans un produit par un entier, compter dans la bonne unité de numération. Toujours vérifier l'ordre de grandeur et écrire l'unité dans un problème. La division par un entier à un chiffre est détaillée dans le chapitre « Diviser ».
:::
''',r'''
Titre: Raisonner en situation de proportionnalité
<!-- optitab:1 -->
::: objectifs
- Reconnaître une situation de proportionnalité entre deux grandeurs.
- Expliquer un raisonnement par le double, la moitié ou un autre partage.
- Additionner des situations et résoudre des problèmes en plusieurs étapes.
:::

## I. Reconnaître la relation entre les grandeurs
::: definition Proportionnalité
Dans une situation de proportionnalité, lorsqu'une grandeur est multipliée par un nombre, l'autre est multipliée par le même nombre. Par exemple, pour des cahiers identiques vendus au même prix à l'unité, acheter deux fois plus de cahiers revient à payer deux fois plus.
:::
::: exemple
Si 4 cahiers coûtent 6 €, alors 8 cahiers coûtent 12 € : on achète le double et on paie le double. La règle du prix à l'unité reste la même pour tous les achats.
:::
[IMAGE_1]
::: attention Une augmentation ne suffit pas
La taille d'un enfant augmente avec son âge, mais elle ne double pas forcément quand son âge double. Un taxi qui facture une prise en charge en plus du trajet ne fait pas payer le double pour une distance double. Ces situations ne sont pas proportionnelles.
:::

## II. Multiplier ou partager une situation
::: methode Dire ce que l'on fait aux deux grandeurs
Repérer combien de fois la quantité demandée est plus grande ou plus petite que celle connue. Faire la même transformation sur la grandeur associée et l'expliquer dans une phrase.
:::
::: exemple Recette pour 4 puis 12 personnes
Pour 4 personnes, une recette utilise 150 g de riz. Pour 12 personnes, il y a trois fois plus de personnes ; il faut donc trois fois plus de riz : $150\times3=450$ g. Pour 2 personnes, il faut deux fois moins de riz : $150\div2=75$ g.
:::

## III. Assembler des situations
::: propriete Additionner les quantités correspondantes
Dans une même situation de proportionnalité, on peut réunir deux quantités connues et additionner les grandeurs qui leur correspondent.
:::
::: exemple Du ruban
4 m de ruban coûtent 6 €. La moitié, 2 m, coûte 3 €. Pour obtenir 10 m, on réunit 4 m, 4 m et 2 m. Le prix est donc $6+6+3=15$ €. On a d'abord partagé une quantité puis additionné des achats.
:::

## IV. Passer par une unité quand cela aide
::: methode Revenir à un objet
Trois carnets identiques coûtent 9 €. Un carnet coûte trois fois moins : $9\div3=3$ €. Cinq carnets coûtent cinq fois ce prix : $3\times5=15$ €. Chaque calcul est accompagné de son sens.
:::
::: exemple Plusieurs étapes
Pour 6 crêpes, il faut 150 g de farine. Trois crêpes demandent la moitié, soit 75 g. Pour 15 crêpes, on prépare 6 crêpes, encore 6 crêpes puis 3 crêpes : $150+150+75=375$ g de farine. Un paquet de 500 g suffit et il restera $500-375=125$ g.
:::
::: retenir
Nommer les deux grandeurs ; vérifier la règle de la situation ; choisir un double, une moitié, un retour à une unité ou un assemblage ; expliquer chaque transformation en phrases ; donner le résultat avec son unité. À prix unitaire constant, davantage d'objets doivent coûter davantage.
:::
''',r'''
Titre: Égalités, régularités et programmes
<!-- optitab:1 -->
::: objectifs
- Compléter des égalités et trouver des nombres représentés par des symboles.
- Poursuivre des suites de nombres et de motifs en expliquant une règle.
- Exécuter et produire un programme de calcul de trois instructions.
- Coder un chemin et tenir compte du point de vue d'un personnage.
:::

## I. Comprendre une égalité
::: definition Deux écritures d'un même nombre
Le signe $=$ signifie que les deux côtés représentent le même nombre. Pour compléter $178-\square=6\times8$, calculer d'abord $6\times8=48$, puis chercher ce qu'il faut retirer à 178 pour obtenir 48 : $178-48=130$. On vérifie $178-130=48$.
:::
::: methode Un symbole garde la même valeur
Dans une énigme, deux symboles identiques représentent le même nombre. Si $\triangle+\triangle=18$, chaque triangle vaut 9. Si $\triangle+\square=14$, le carré vaut $14-9=5$. Vérifier dans les deux égalités.
:::

## II. Suivre une règle de suite
::: methode Repérer et vérifier la règle
Comparer plusieurs termes, formuler une règle, puis vérifier qu'elle fonctionne à chaque passage. Une règle indiquée dans l'énoncé doit être respectée.
:::
::: exemple
Avec la règle « doubler puis ajouter 1 », $7;15;31;63$ se poursuit par 127 puis 255. Avec « ajouter 5 puis retirer 2, en alternance », $80;85;83;88;86$ se poursuit par 91 puis 89.
:::
::: attention
Les seuls nombres 2 et 4 ne fixent pas une règle unique : on peut ajouter 2 ou doubler. On propose une règle possible et on précise son choix.
:::

## III. Compter les motifs
[IMAGE_1]
::: exemple Des croix qui grandissent
La première croix contient 5 carreaux. À chaque nouvelle étape, on ajoute un carreau au bout de chacune des quatre branches, donc 4 carreaux. L'étape 2 en contient 9 ; l'étape 3 en contient 13. Pour l'étape 10, il y a neuf ajouts après la première : $5+(9\times4)=41$ carreaux.
:::

## IV. Exécuter un programme de calcul
::: methode Conserver les résultats intermédiaires
Choisir un entier ; ajouter 2 ; multiplier le résultat par 4 ; retirer 3. Ces trois instructions transforment le nombre de départ. Avec 6 : $6+2=8$, puis $8\times4=32$, puis $32-3=29$.
:::
::: attention L'ordre compte
Ajouter 2 puis multiplier par 4 ne donne pas le même résultat que multiplier par 4 puis ajouter 2. Il faut appliquer chaque instruction au résultat de la précédente.
:::
::: exemple Produire un programme
Pour passer de 5 à 26 en trois instructions, on peut écrire : ajouter 2 ; multiplier par 4 ; retirer 2. Test : $5+2=7$, $7\times4=28$, $28-2=26$. D'autres programmes sont possibles.
:::

## V. Coder des déplacements
[IMAGE_2]
::: definition Avancer et tourner
« Avancer » déplace le personnage dans la direction qu'il regarde. « Tourner à droite » ou « tourner à gauche » lui fait effectuer un quart de tour sur place. Sa droite dépend de sa direction, et non de celle du lecteur.
:::
::: exemple
Le personnage part de B2 en regardant vers la droite de la page. Il avance de 2 cases, tourne à gauche puis avance d'une case : il arrive en D3 et regarde vers le haut. S'il regardait d'abord vers le haut, tourner à droite le ferait regarder vers la droite de la page. S'il regardait vers le bas, tourner à droite le ferait regarder vers la gauche de la page.
:::
::: retenir
Noter la position **et** l'orientation après chaque instruction. Tester un programme, repérer une erreur et la corriger font partie du raisonnement. Dans un programme de calcul comme dans un chemin, l'ordre des instructions est essentiel.
:::
''']

SHEETS = [r'''
Titre: Additionner, soustraire et multiplier — l'essentiel
<!-- optitab:1 -->
::: retenir Choisir puis contrôler
Addition : réunir ou ajouter. Soustraction : reste, écart ou quantité manquante. Multiplication : groupes de même taille. Répondre avec l'unité.
:::
::: methode Calculer
- De tête : décomposer, regrouper, compenser. $648+99=648+100-1=747$.
- Poser : aligner les rangs ; traiter les échanges.
- Multiplier : $326\times24=(326\times4)+(326\times20)=7\,824$.
- Parenthèses : calculer chaque groupe d'abord. $(36+14)\times(20-8)=600$.
:::
::: attention
La ligne « fois 20 » est dix fois la ligne « fois 2 ». Estimer avant et vérifier après : une différence se contrôle par une addition.
:::
''',r'''
Titre: Diviser — l'essentiel
<!-- optitab:1 -->
::: retenir Quotient et reste
Dividende = diviseur × quotient entier + reste. Le reste est positif ou nul et plus petit que le diviseur. $37=5\times7+2$.
:::
::: methode Trois contrôles
1. Estimer le quotient.
2. Conserver les zéros de chaque rang : $1\,258=6\times209+4$.
3. Vérifier par multiplication et interpréter le reste.
:::
::: methode Partage décimal
Échanger les unités restantes contre des dixièmes, puis les dixièmes contre des centièmes si nécessaire. $27\div4=6{,}75$ ; contrôle : $6{,}75\times4=27$.
:::
::: attention
230 œufs donnent 38 boîtes pleines de 6 et 2 œufs restants ; il faut 39 boîtes pour tout transporter. Une mesure partageable peut donner un quotient décimal.
:::
''',r'''
Titre: Calculer avec les décimaux — l'essentiel
<!-- optitab:1 -->
::: methode Les bons rangs
Somme ou différence : aligner les virgules et les rangs. $12{,}70+3{,}85=16{,}55$ ; $20{,}00-4{,}35=15{,}65$.
:::
::: methode Produit par un entier
$6{,}38$ vaut 638 centièmes. $638\times7=4\,466$, donc $6{,}38\times7=44{,}66$.
:::
::: retenir Changer de rang
Multiplier par 10, 100, 1 000 donne aux chiffres une valeur 10, 100, 1 000 fois plus grande. Diviser produit l'effet inverse. $3{,}456\times100=345{,}6$ ; $47{,}2\div100=0{,}472$.
:::
::: attention
$2{,}40=2{,}4$ : ajouter un zéro à droite ne multiplie pas par 10. Calculer d'abord les parenthèses ; estimer puis vérifier. Pour multiplier par 5, on peut multiplier par 10 puis prendre la moitié.
:::
''',r'''
Titre: Proportionnalité — l'essentiel
<!-- optitab:1 -->
::: retenir Reconnaître
Quand une grandeur est doublée, triplée ou partagée, l'autre subit la même transformation. Un prix fixe par objet convient ; une taille selon l'âge ne convient pas en général.
:::
::: methode Expliquer en phrases
- Double : 4 cahiers coûtent 6 €, donc 8 cahiers coûtent 12 €.
- Moitié : 2 cahiers coûtent 3 €.
- Assembler : 10 cahiers, c'est 4 cahiers, encore 4 puis 2 ; le prix est $6+6+3=15$ €.
- Une unité : 3 carnets coûtent 9 €, donc 1 carnet coûte 3 €, puis 5 carnets coûtent 15 €.
:::
::: attention
Lire les conditions : un forfait de départ ou une réduction peut changer la relation. Nommer les grandeurs, expliquer chaque étape et donner l'unité.
:::
''',r'''
Titre: Égalités, régularités et programmes — l'essentiel
<!-- optitab:1 -->
::: retenir Égalités et motifs
Les deux côtés de $=$ ont la même valeur. Un même symbole représente le même nombre. Vérifier les valeurs trouvées. Dans une suite, énoncer une règle et la tester à chaque passage.
:::
::: methode Programme de trois instructions
Ajouter 2, multiplier par 4, retirer 3. Avec 6 : $6+2=8$, $8\times4=32$, $32-3=29$. Chaque instruction agit sur le résultat précédent.
:::
::: methode Motifs et chemins
- Une croix de 5 carreaux qui gagne 4 carreaux par étape en a $5+(9\times4)=41$ à l'étape 10.
- « Avancer » dépend du regard du personnage ; tourner d'un quart de tour change son orientation sans le déplacer.
:::
::: attention
La droite du personnage n'est pas toujours celle de la page. Noter sa position et son orientation après chaque instruction. Pour une suite, deux termes ne suffisent pas toujours à déterminer une règle unique.
:::
''']

def q(enonce, methode, etape, resultat):
    return dict(enonce=enonce,methode=methode,etape=etape,resultat=resultat)
def calc(expr,result,method='Décomposer le calcul en gardant les rangs.',detail=None, prompt='Calculer'):
    formula=f'${expr}={result}$'
    return q(f'{prompt} ${expr}$.',method,detail or f'On effectue les calculs dans les rangs correspondants : {formula}.',formula+'.')
def fmt(x):
    x=D(str(x)); s=format(x,'f').rstrip('0').rstrip('.') if '.' in format(x,'f') else str(x)
    return s.replace('.',r'{,}')
def partage_detail(a,d):
    a=D(str(a)); whole=int(a); quo,rem=divmod(whole,d)
    chunks=[f'Les ${whole}$ unités donnent ${quo}$ unités par part ; le reste vaut ${rem}$ unité(s).']
    digits=format(a,'f').partition('.')[2]
    remainder=D(rem)+(a-whole)
    # À chaque rang, le reste antérieur et le chiffre du dividende sont regroupés.
    r=rem; exact=quo; ranknames=['dixièmes','centièmes','millièmes','dix-millièmes']
    for k in range(4):
        digit=int(digits[k]) if k<len(digits) else 0
        if not r and not any(c!='0' for c in digits[k:]):break
        amount=r*10+digit; part,r=divmod(amount,d)
        chunks.append(f'Au rang des {ranknames[k]}, on partage ${amount}$ : ${amount}={d}\\times{part}+{r}$. Chaque part reçoit ${part}$ {ranknames[k]}.')
    chunks.append(f'Le reste est nul. Contrôle : ${fmt(a/D(d))}\\times{d}={fmt(a)}$.')
    return ' '.join(chunks)
def addition_detail(a,b):
    a,b=D(str(a)),D(str(b));places=max(0,-a.as_tuple().exponent,-b.as_tuple().exponent)
    power=10**places;x,y=int(a*power),int(b*power)
    unit={0:'unités',1:'dixièmes',2:'centièmes',3:'millièmes'}.get(places,'parts décimales')
    chunks=[f'On compte dans la même unité : ${x}$ et ${y}$ {unit}.']
    carry=0
    for j in range(max(len(str(x)),len(str(y)))):
        dx,dy=(x//10**j)%10,(y//10**j)%10
        total=dx+dy+carry;digit=total%10;nextcarry=total//10
        line=f'${dx}+{dy}'+(f'+{carry}' if carry else '')+f'={total}$ : on écrit {digit}'
        line+=f' et on retient {nextcarry} au rang suivant.' if nextcarry else '.'
        chunks.append(line);carry=nextcarry
    if carry:chunks.append(f'La dernière retenue donne {carry} au rang suivant.')
    chunks.append(f'La somme vaut ${x+y}$ {unit}, soit ${fmt(a+b)}$.')
    return ' '.join(chunks)
def block(i,title,level,context,qs):
    typ=['Découverte','Entraînement','Problème'][level]
    # Le contexte est du texte courant ; la virgule LaTeX reste réservée aux maths.
    context=context.replace('{,}',',')
    s=f'=== {typ} - {title}\nId: nouveau-{i}\nDifficulté: '+['easy','medium','hard'][level]+'\n\nÉnoncé:\n<!-- optitab:1 -->\n'+context+'\n\n'
    s+='\n'.join(f'{k}. {a["enonce"]}' for k,a in enumerate(qs,1))
    s+='\n\nÉtapes:\n<!-- optitab:1 -->\n'
    for k,a in enumerate(qs,1):
        s+=f'\n## Question {k} : '+a['enonce'].rstrip('.')+'\n\n'
        for tag,key in [('methode','methode'),('etape Raisonnement','etape'),('resultat','resultat')]:
            s+=f'::: {tag}\n{a[key]}\n:::\n\n'
    s+='Solution:\n<!-- optitab:1 -->\n'+'\n'.join(f'{k}. {a["resultat"]}' for k,a in enumerate(qs,1))+'\n\n'
    return s

def operations(level):
    a=[348,2748,28475][level]; b=[275,1687,39786][level]; m=[24,126,326][level]; n=[13,24,47][level]
    out=[]
    out.append(('Sommes et échanges', 'Calculer en posant si nécessaire ; expliquer les échanges.',[
        calc(rf'{a}+{b}',a+b,'Aligner unités, dizaines et centaines.',addition_detail(a,b)),
        calc(rf'{a}+{b}+125',a+b+125,'Regrouper les sommes.',f'Les deux premiers nombres donnent ${a+b}$ ; ajouter 125 donne ${a+b+125}$.'),
        q(f'Vérifier la somme précédente par un retrait de 125.','Utiliser une opération inverse.',f'${a+b+125}-125={a+b}$. On retrouve la somme des deux premiers nombres.',f'Le contrôle donne ${a+b}$ : la somme est cohérente.')]))
    out.append(('Différences et contrôle','Effectuer les différences et contrôler.',[
        calc(rf'{a+b}-{b}',a,'Soustraire en alignant les rangs.',f'On cherche ce qui manque à ${b}$ pour obtenir ${a+b}$. Comme ${b}+{a}={a+b}$, la différence vaut ${a}$.'),
        calc(rf'{10**(level+3)+2}-785',10**(level+3)-783,'Échanger à travers les zéros.',f'On effectue les échanges depuis le premier rang disponible ; le retrait de 785 donne ${10**(level+3)-783}$.'),
        q('Comment vérifier la deuxième réponse ?','Ajouter ce qui a été retiré.',f'${10**(level+3)-783}+785={10**(level+3)+2}$. Le nombre de départ est retrouvé.','Le contrôle par addition confirme la différence.')]))
    out.append(('Produits et décomposition','Décomposer le second facteur en dizaines et unités.',[
        calc(rf'{m}\times{n}',m*n,'Séparer dizaines et unités.',f'${m}\\times{n//10*10}={m*(n//10*10)}$ et ${m}\\times{n%10}={m*(n%10)}$. On additionne ces deux produits : ${m*(n//10*10)}+{m*(n%10)}={m*n}$.'),
        calc(rf'{m}\times{n+10}',m*(n+10),'Ajouter dix groupes.',f'${m}\\times{n}={m*n}$. Dix groupes supplémentaires valent ${m*10}$ ; le total est ${m*n}+{m*10}={m*(n+10)}$.'),
        q(f'Un élève écrit ${m}\\times{n}={m*(n//10)+m*(n%10)}$. Expliquer son erreur.','Donner leur valeur aux dizaines.',f'Il a utilisé ${n//10}$ au lieu de ${n//10*10}$. La ligne des dizaines représente ${n//10*10}$ groupes.',f'Le produit correct est ${m*n}$ ; la valeur des dizaines a été oubliée.')]))
    x=[275,487,1236][level]
    out.append(('Calcul mental astucieux','Choisir un chemin court et l’expliquer.',[
        calc(rf'{x}+99',x+99,'Ajouter 100 puis retirer 1.',f'${x}+100={x+100}$ puis ${x+100}-1={x+99}$.'),
        calc(rf'{x}-99',x-99,'Retirer 100 puis ajouter 1.',f'${x}-100={x-100}$ puis ${x-100}+1={x-99}$.'),
        calc(rf'{4*(level+3)}\times25',100*(level+3),'Multiplier par 100 puis diviser par 4.',f'${4*(level+3)}\\times100={400*(level+3)}$. La moitié est ${200*(level+3)}$, puis la moitié est ${100*(level+3)}$.')]))
    p=12+6*level
    out.append(('Parenthèses à respecter','Calculer les groupes avant de les combiner.',[
        calc(rf'({p}+8)\times3',(p+8)*3,'Commencer par la parenthèse.',f'${p}+8={p+8}$ puis ${p+8}\\times3={(p+8)*3}$.'),
        calc(rf'({p}+8)\times(20-7)',(p+8)*13,'Calculer les deux parenthèses.',f'${p}+8={p+8}$ et $20-7=13$ ; le produit vaut ${(p+8)*13}$.'),
        q(f'${p}+(8\\times3)$ donne-t-il le même résultat que la question 1 ?','Comparer les groupements.',f'$8\\times3=24$, puis ${p}+24={p+24}$. À la question 1, le résultat est ${(p+8)*3}$.',f'Non : ${p+24}$ et ${(p+8)*3}$ sont différents.')]))
    out.append(('Choisir et estimer','Une association reçoit '+str(a)+' livres lundi et '+str(b)+' mardi. Elle en distribue 186.',[
        q('Combien de livres a-t-elle reçus ?','Réunir les deux livraisons.',f'${a}+{b}={a+b}$. On additionne car on cherche le total reçu.',f'Elle a reçu ${a+b}$ livres.'),
        q('Combien de livres reste-t-il ?','Retirer les livres distribués.',f'${a+b}-186={a+b-186}$. On soustrait 186 au stock reçu.',f'Il reste ${a+b-186}$ livres.'),
        q(f'Un bénévole annonce seulement {a+b-1186} livres restants. Pourquoi peut-on rejeter ce résultat ?','Comparer avec le contrôle inverse.',f'${a+b-1186}+186={a+b-1000}$, ce qui ne redonne pas ${a+b}$. Il manque 1 000 livres au contrôle.',f'Le contrôle échoue ; le stock correct est ${a+b-186}$ livres.')]))
    c=12+level*6; cost=35+level*7; cash=1000+level*1000
    out.append(('Organiser une sortie','Une classe achète '+str(c)+' billets à '+str(cost)+' € et paie 85 € de transport. Elle dispose de '+str(cash)+' €.',[
        q('Calculer le prix des billets.','Compter des groupes de même prix.',f'${c}\\times{cost}={c*cost}$.',f'Les billets coûtent ${c*cost}$ €.'),
        q('Calculer la dépense totale.','Ajouter le transport.',f'${c*cost}+85={c*cost+85}$.',f'La dépense totale est de ${c*cost+85}$ €.'),
        q('Le budget suffit-il et quelle somme reste-t-il ?','Comparer budget et dépense.',f'${cash}-{c*cost+85}={cash-c*cost-85}$. La différence est positive.',f'Oui ; il reste ${cash-c*cost-85}$ €.')]))
    return out

def divisions(level):
    out=[]; d=[3,6,8][level]; total=[77,1258,3247][level]; quo,rem=divmod(total,d)
    out.append(('Quotient et reste','Effectuer la division euclidienne de '+str(total)+' par '+str(d)+'.',[
        q('Donner le quotient entier et le reste.','Chercher les multiples qui encadrent le dividende.',f'${d}\\times{quo}={d*quo}$ et ${d}\\times{quo+1}={d*(quo+1)}$. Le reste vaut ${total}-{d*quo}={rem}$.',f'Quotient : ${quo}$ ; reste : ${rem}$.'),
        q('Écrire le contrôle complet.','Reconstituer le dividende.',f'${d}\\times{quo}+{rem}={total}$ et ${rem}<{d}$.','Le dividende est retrouvé et le reste est inférieur au diviseur.'),
        q(f'Que deviendrait le quotient si on ajoutait {d} au dividende ?','Un groupe supplémentaire de la taille du diviseur.',f'${total+d}={d}\\times{quo+1}+{rem}$. Ajouter ${d}$ permet de former exactement un groupe de plus.',f'Le quotient serait ${quo+1}$ et le reste resterait ${rem}$.')]))
    a=[612,2418,3609][level]; d=[3,6,9][level]; z=a//d
    out.append(('Ne pas perdre un zéro','Une division peut contenir un zéro au quotient.',[
        calc(rf'{a}\div{d}',z,'Traiter chaque rang.',f'On partage de gauche à droite. Quand un rang ne donne aucun groupe, on écrit 0. On obtient ${z}$ ; le contrôle est ${z}\\times{d}={a}$.'),
        calc(rf'{a+d}\div{d}',z+1,'Comparer au calcul précédent.',f'Le dividende augmente de ${d}$ : une part supplémentaire est possible ; ${z}+1={z+1}$.'),
        q(f'Pourquoi le quotient {int(str(z).replace("0",""))} est-il impossible pour la première division ?','Contrôler par multiplication.',f'${int(str(z).replace("0",""))}\\times{d}={int(str(z).replace("0",""))*d}$, ce qui ne vaut pas ${a}$.','Il manque le zéro qui conserve la place des dizaines.')]))
    eggs=[98,230,421][level]; d=[6,6,8][level]; v,r=divmod(eggs,d)
    out.append(('Boîtes pleines ou boîtes nécessaires',f'On range {eggs} objets indivisibles dans des boîtes de {d}.',[
        q('Combien de boîtes peut-on remplir complètement ?','Chercher le quotient entier.',f'${eggs}={d}\\times{v}+{r}$.',f'On remplit ${v}$ boîtes.'),
        q('Combien d’objets restent hors des boîtes pleines ?','Lire le reste.',f'Les boîtes pleines contiennent ${d*v}$ objets. ${eggs}-{d*v}={r}$.',f'Il reste ${r}$ objets.'),
        q('Combien de boîtes faut-il pour tout ranger ?','Prévoir une boîte pour le reste.',f'Le reste ${r}$ est non nul ; on ajoute une boîte : ${v}+1={v+1}$.',f'Il faut ${v+1}$ boîtes, dont une incomplète.')]))
    nums=[[15,27,43],[37,59,73],[81,101,137]][level]; d=[2,4,8][level]
    out.append(('Partager une longueur exactement',f'Chaque longueur est partagée en {d} morceaux égaux. Donner la mesure d’un morceau.',[
        calc(rf'{a}\div{d}',fmt(D(a)/d),'Échanger le reste contre des dixièmes puis des centièmes.',partage_detail(a,d),prompt='Calculer, en mètres, le partage de') for a in nums]))
    nums=[['8.4','12.6','15.3'],['8.7','14.1','25.5'],['12.84','37.2','60.6']][level]; d=[3,6,4][level]
    out.append(('Dividende décimal','Calculer puis vérifier chaque quotient exact.',[
        calc(rf'{fmt(a)}\div{d}',fmt(D(a)/d),'Partager en conservant les rangs.',partage_detail(a,d)) for a in nums]))
    d=[4,5,8][level]; a=[36,65,104][level]
    out.append(('Vérifier une proposition',f'On étudie {a} ÷ {d}.',[
        q(f'Le quotient {a//d+1} est-il exact ?','Multiplier le quotient proposé.',f'${a//d+1}\\times{d}={a+d}$, ce qui dépasse ${a}$.',f'Non ; le quotient exact est ${a//d}$.'),
        q(f'Une division de {a+2} par {d} peut-elle avoir pour reste {d+2} ?','Comparer reste et diviseur.',f'${d+2}>{d}$. On peut encore retirer un groupe de ${d}$ ; la division ne serait pas terminée.','Non ; un reste doit être strictement inférieur au diviseur.'),
        q(f'Corriger la division euclidienne de {a+2} par {d}.','Reconstituer avec le bon reste.',f'${a+2}={d}\\times{a//d}+2$ et $2<{d}$.',f'Quotient : ${a//d}$ ; reste : 2.')]))
    bottles=[5,6,8][level]; liters=[D('12.5'),D('16.5'),D('22')][level]; used=D('0.75')
    out.append(('Jus pour un atelier',f'On répartit {fmt(liters)} L de jus également dans {bottles} récipients. On utilise ensuite 0,75 L de chaque récipient.',[
        q('Quel volume contient chaque récipient au départ ?','Partager le volume total.',f'${fmt(liters)}\\div{bottles}={fmt(liters/bottles)}$.',f'Chaque récipient contient ${fmt(liters/bottles)}$ L.'),
        q('Quel volume reste dans chaque récipient ?','Retirer le volume utilisé.',f'${fmt(liters/bottles)}-0{{,}}75={fmt(liters/bottles-used)}$.',f'Il reste ${fmt(liters/bottles-used)}$ L par récipient.'),
        q('Quel volume reste en tout ?','Réunir les volumes restants.',f'${fmt(liters/bottles-used)}\\times{bottles}={fmt(liters-used*bottles)}$.',f'Il reste en tout ${fmt(liters-used*bottles)}$ L.')]))
    return out

def decimals(level):
    out=[]; a=D(['12.7','23.405','104.875'][level]); b=D(['3.85','6.79','38.056'][level]); n=[4,12,24][level]
    out.append(('Aligner les rangs','Calculer en détaillant les unités de numération.',[
        calc(rf'{fmt(a)}+{fmt(b)}',fmt(a+b),'Aligner unités et rangs décimaux.',addition_detail(a,b)),
        calc(rf'{fmt(a)}-{fmt(b)}',fmt(a-b),'Aligner les virgules et effectuer les échanges.',f'Le retrait rang par rang donne ${fmt(a-b)}$. Contrôle : ${fmt(a-b)}+{fmt(b)}={fmt(a)}$.'),
        q('Comment contrôler la première somme ?','Retirer un des termes.',f'${fmt(a+b)}-{fmt(b)}={fmt(a)}$.','On retrouve le premier terme : la somme est confirmée.')]))
    b=D(['3.85','6.79','8.65'][level])
    out.append(('Multiplier par un entier',f'Un mètre de ruban coûte {fmt(b)} €. Le prix au mètre ne change pas.',[
        calc(rf'{fmt(b)}\times{n}',fmt(b*n),'Compter dans l’unité décimale du nombre.',f'On multiplie le nombre de millièmes ou de centièmes par ${n}$, puis on réécrit en euros : ${fmt(b*n)}$.'),
        calc(rf'{fmt(b)}\times{n+1}',fmt(b*(n+1)),'Ajouter le prix d’un mètre.',f'${fmt(b*n)}+{fmt(b)}={fmt(b*(n+1))}$.'),
        q(f'Pourquoi ${fmt(b*n*10)}$ € ne convient-il pas pour {n} m ?','Vérifier la place de la virgule.',f'Ce nombre est dix fois le produit attendu. Le calcul exact donne ${fmt(b)}\\times{n}={fmt(b*n)}$.',f'La virgule a été mal placée ; le prix correct est ${fmt(b*n)}$ €.')] ))
    x=D(['3.456','0.728','12.305'][level])
    out.append(('Donner une valeur plus grande aux chiffres','Expliquer les changements de rang.',[
        calc(rf'{fmt(x)}\times{k}',fmt(x*k),f'Chaque chiffre prend une valeur {k} fois plus grande.',f'Les chiffres se placent {len(str(k))-1} rang(s) vers les unités plus grandes. On obtient ${fmt(x*k)}$.') for k in [10,100,1000]]))
    x=D(['47.2','6.4','305.8'][level])
    out.append(('Partager par dix, cent, mille','Compléter par des zéros si nécessaire.',[
        calc(rf'{fmt(x)}\div{k}',fmt(x/k),f'Chaque chiffre prend une valeur {k} fois plus petite.',f'Les chiffres se placent {len(str(k))-1} rang(s) vers les unités plus petites ; les zéros gardent les places. Le quotient est ${fmt(x/k)}$.') for k in [10,100,1000]]))
    x=D(['3.6','7.35','12.46'][level])
    out.append(('Doubles, moitiés et calcul mental','Choisir une procédure mentale.',[
        calc(rf'{fmt(x)}\times2',fmt(x*2),'Additionner deux nombres identiques.',f'${fmt(x)}+{fmt(x)}={fmt(x*2)}$.'),
        calc(rf'{fmt(x)}\div2',fmt(x/2),'Partager chaque rang et échanger si nécessaire.',f'La moitié est ${fmt(x/2)}$, car ${fmt(x/2)}+{fmt(x/2)}={fmt(x)}$.'),
        calc(rf'{fmt(x)}\times5',fmt(x*5),'Multiplier par 10 puis prendre la moitié.',f'${fmt(x)}\\times10={fmt(x*10)}$ puis ${fmt(x*10)}\\div2={fmt(x*5)}$.')]))
    x=D(['4.5','7.25','12.375'][level]); y=D(['1.5','2.75','3.625'][level])
    out.append(('Groupements et erreurs','Respecter les parenthèses ; contrôler le résultat.',[
        calc(rf'({fmt(x)}+{fmt(y)})\times3',fmt((x+y)*3),'Commencer par la parenthèse.',f'${fmt(x)}+{fmt(y)}={fmt(x+y)}$ puis ${fmt(x+y)}\\times3={fmt((x+y)*3)}$.'),
        calc(rf'({fmt(x)}+{fmt(y)})\times(8-5)',fmt((x+y)*3),'Calculer les deux parenthèses.',f'La première vaut ${fmt(x+y)}$ et la seconde vaut 3 ; leur produit vaut ${fmt((x+y)*3)}$.'),
        q(f'Un élève affirme ${fmt(x)}+0{{,}}25={fmt(x+D("2.5"))}$. Corriger.','Distinguer dixièmes et centièmes.',f'0,25 représente 25 centièmes, et non 25 dixièmes. La somme correcte est ${fmt(x)}+0{{,}}25={fmt(x+D(".25"))}$.',f'La somme vaut ${fmt(x+D(".25"))}$.')]))
    unit=D(['2.35','4.75','6.85'][level]); count=[4,12,24][level]; budget=[20,100,200][level]; extra=D('3.8')
    out.append(('Un achat à plusieurs étapes',f'On achète {count} carnets à {fmt(unit)} € et une boîte à 3,80 €. On paie avec {budget} €.',[
        q('Calculer le prix des carnets.','Multiplier le prix d’un carnet par leur nombre.',f'${fmt(unit)}\\times{count}={fmt(unit*count)}$.',f'Les carnets coûtent ${fmt(unit*count)}$ €.'),
        q('Calculer le montant de l’achat.','Ajouter le prix de la boîte.',f'${fmt(unit*count)}+3{{,}}8={fmt(unit*count+extra)}$.',f'Le montant est de ${fmt(unit*count+extra)}$ €.'),
        q('Quelle monnaie doit-on rendre ?','Retirer le montant payé de la somme donnée.',f'${budget}-{fmt(unit*count+extra)}={fmt(D(budget)-unit*count-extra)}$.',f'La monnaie est de ${fmt(D(budget)-unit*count-extra)}$ €.')] ))
    return out

def proportions(level):
    out=[]; p=[6,9,15][level]
    out.append(('Reconnaître une situation','Justifier chacune des réponses en phrases.',[
        q(f'Des carnets identiques coûtent toujours {p} € les trois. Le prix est-il proportionnel au nombre de carnets ?','Examiner le double d’une quantité.',f'Deux lots de trois coûtent ${p}+{p}={2*p}$ €. Quand on double le nombre de carnets, le prix double ; chaque carnet garde le même prix.','Oui : le prix à l’unité reste constant.'),
        q('Un enfant mesure 1 m à 5 ans et 1,40 m à 10 ans. La taille est-elle proportionnelle à l’âge ?','Comparer les effets d’un doublement.','L’âge a doublé. Si la situation était proportionnelle, la taille aurait doublé jusqu’à 2 m. Or elle vaut 1,40 m.','Non : le doublement de l’âge ne double pas la taille.'),
        q('Une livraison coûte 4 € fixes puis 2 € par colis. Le prix total est-il proportionnel au nombre de colis ?','Tester un puis deux colis.','$4+2=6$ € pour un colis ; $4+(2\\times2)=8$ € pour deux. Le double de 6 € serait 12 €.','Non : deux fois plus de colis ne coûtent pas deux fois plus.')]))
    flour=[150,225,375][level]
    out.append(('Doubler puis tripler une recette',f'Une recette pour 4 personnes utilise {flour} g de farine. On conserve les mêmes portions.',[
        q('Quelle masse faut-il pour 8 personnes ?','Il y a deux fois plus de personnes.',f'Il faut donc deux fois plus de farine : ${flour}\\times2={2*flour}$.',f'Il faut ${2*flour}$ g.'),
        q('Quelle masse faut-il pour 12 personnes ?','Il y a trois fois plus de personnes.',f'Il faut trois fois plus de farine : ${flour}\\times3={3*flour}$.',f'Il faut ${3*flour}$ g.'),
        q('Quelle masse faut-il pour 2 personnes ?','Il y a deux fois moins de personnes.',f'Il faut la moitié de la farine : ${flour}\\div2={fmt(D(flour)/2)}$.',f'Il faut ${fmt(D(flour)/2)}$ g.')]))
    price=[6,10,14][level]
    out.append(('Partager un achat',f'Quatre mètres de ruban coûtent {price} €. Chaque mètre a le même prix.',[
        q('Combien coûtent 2 m ?','La longueur est divisée par deux.',f'Le prix est lui aussi divisé par deux : ${price}\\div2={price//2}$.',f'2 m coûtent ${price//2}$ €.'),
        q('Combien coûtent 1 m ?','Prendre encore la moitié.',f'1 m est la moitié de 2 m ; le prix est ${price//2}\\div2={fmt(D(price)/4)}$.',f'1 m coûte ${fmt(D(price)/4)}$ €.'),
        q('Combien coûtent 3 m ?','Réunir 2 m et 1 m.',f'Les deux prix s’additionnent : ${price//2}+{fmt(D(price)/4)}={fmt(D(price)*3/4)}$.',f'3 m coûtent ${fmt(D(price)*3/4)}$ €.')]))
    out.append(('Assembler des longueurs',f'Quatre mètres de tissu coûtent {price} €, toujours au même prix au mètre.',[
        q('Trouver le prix de 6 m en assemblant deux longueurs.','Réunir 4 m et leur moitié.',f'2 m coûtent ${fmt(D(price)/2)}$ €. Donc 6 m coûtent ${price}+{fmt(D(price)/2)}={fmt(D(price)*D("1.5"))}$.',f'6 m coûtent ${fmt(D(price)*D("1.5"))}$ €.'),
        q('Trouver le prix de 10 m.','Réunir 4 m, encore 4 m puis 2 m.',f'Les trois morceaux coûtent ${price}+{price}+{fmt(D(price)/2)}={fmt(D(price)*D("2.5"))}$ €.',f'10 m coûtent ${fmt(D(price)*D("2.5"))}$ €.'),
        q('Trouver le prix de 14 m.','Ajouter un morceau de 4 m aux 10 m.',f'Le prix est ${fmt(D(price)*D("2.5"))}+{price}={fmt(D(price)*D("3.5"))}$ €.',f'14 m coûtent ${fmt(D(price)*D("3.5"))}$ €.')] ))
    cartons=[3,4,6][level]; mass=[12,18,27][level]; unit=D(mass)/cartons
    out.append(('Revenir à une unité',f'{cartons} bouteilles identiques pleines contiennent {mass} L en tout.',[
        q('Quel volume contient une bouteille ?','Partager le volume entre les bouteilles.',f'Une bouteille contient ${cartons}$ fois moins que le lot : ${mass}\\div{cartons}={fmt(unit)}$.',f'Une bouteille contient ${fmt(unit)}$ L.'),
        q('Quel volume contiennent 5 bouteilles ?','Prendre cinq fois le contenu d’une bouteille.',f'Cinq bouteilles contiennent cinq fois plus qu’une seule : ${fmt(unit)}\\times5={fmt(unit*5)}$.',f'5 bouteilles contiennent ${fmt(unit*5)}$ L.'),
        q('Combien de bouteilles faut-il pour contenir le double du volume de 5 bouteilles ?','Doubler le nombre de bouteilles.',f'Le double du volume de cinq bouteilles demande le double de bouteilles : $5\\times2=10$.',f'Il faut 10 bouteilles, contenant ${fmt(unit*10)}$ L.')]))
    flow=[12,18,30][level]
    out.append(('Un débit régulier',f'Un robinet fournit {flow} L en 3 minutes. Son débit reste régulier.',[
        q('Quel volume fournit-il en 6 minutes ?','La durée double.',f'Le volume double aussi : ${flow}\\times2={flow*2}$.',f'Il fournit ${flow*2}$ L.'),
        q('Quel volume fournit-il en 9 minutes ?','Réunir les durées 6 min et 3 min.',f'Le volume est ${flow*2}+{flow}={flow*3}$.',f'Il fournit ${flow*3}$ L.'),
        q('Combien de minutes faut-il pour obtenir cinq fois le volume de départ ?','Multiplier la durée par cinq.',f'Pour obtenir cinq fois plus d’eau, il faut cinq fois plus de temps : $3\\times5=15$.',f'Il faut 15 minutes pour ${flow*5}$ L.')]))
    rice=[150,250,350][level]; stock=rice*4
    out.append(('Préparer un repas',f'Pour 4 personnes, il faut {rice} g de riz. On garde les mêmes portions. On possède {stock} g de riz.',[
        q('Quelle masse prévoir pour 10 personnes ?','Réunir deux groupes de 4 et un groupe de 2.',f'2 personnes demandent ${fmt(D(rice)/2)}$ g. Pour 10 personnes : ${rice}+{rice}+{fmt(D(rice)/2)}={fmt(D(rice)*D("2.5"))}$ g.',f'Il faut ${fmt(D(rice)*D("2.5"))}$ g.'),
        q('Quelle masse restera-t-il ?','Retirer la masse utilisée du stock.',f'${stock}-{fmt(D(rice)*D("2.5"))}={fmt(D(rice)*D("1.5"))}$.',f'Il restera ${fmt(D(rice)*D("1.5"))}$ g.'),
        q('Pour combien de personnes le riz restant suffit-il ?','Assembler 4 personnes et la moitié de ce groupe.',f'Le reste représente ${rice}$ g et ${fmt(D(rice)/2)}$ g ; cela nourrit $4+2=6$ personnes.',f'Le reste suffit pour 6 personnes.')]))
    return out

def regularities(level):
    out=[]; a=[48,137,237][level]; b=[19,54,126][level]
    out.append(('Compléter des égalités','Trouver le nombre manquant et vérifier.',[
        q(f'Compléter ${a}+\\square={a+b}$.','Chercher le complément.',f'${a+b}-{a}={b}$. Vérification : ${a}+{b}={a+b}$.',f'$\\square={b}$.'),
        q(f'Compléter ${a+b}-\\square={a}$.','Retrouver la quantité retirée.',f'${a+b}-{a}={b}$. Retirer ${b}$ redonne bien ${a}$.',f'$\\square={b}$.'),
        q(f'Compléter $({2+level}\\times\\square)-5={a*(2+level)-5}$.','Défaire le retrait puis le produit.',f'On ajoute 5 : ${a*(2+level)-5}+5={a*(2+level)}$. On partage par ${2+level}$ : ${a*(2+level)}\\div{2+level}={a}$.',f'$\\square={a}$.')] ))
    t=[7,12,18][level]; s=[4,8,11][level]
    out.append(('Les pictogrammes inconnus',f'On sait que $\\triangle+\\triangle={2*t}$ et $\\triangle+\\square={t+s}$. Un symbole garde toujours la même valeur.',[
        q('Trouver la valeur du triangle.','Partager la somme de deux valeurs identiques.',f'${2*t}\\div2={t}$.',f'$\\triangle={t}$.'),
        q('Trouver la valeur du carré.','Remplacer le triangle par sa valeur.',f'${t+s}-{t}={s}$.',f'$\\square={s}$.'),
        q('Calculer la valeur de deux carrés et un triangle.','Réunir les trois valeurs.',f'${s}+{s}+{t}={2*s+t}$.',f'La valeur totale est ${2*s+t}$.')] ))
    start=[7,12,21][level]; step=[4,7,13][level]
    out.append(('Des suites à expliquer',f'Première suite : partir de {start} et ajouter {step} à chaque passage.',[
        q('Écrire les quatre premiers termes.','Appliquer trois fois la même règle.',f'On part de ${start}$, puis on ajoute ${step}$ : ${start+step}$, ${start+2*step}$ et ${start+3*step}$.',f'${start};{start+step};{start+2*step};{start+3*step}$.'),
        q('Trouver le dixième terme.','Compter les ajouts depuis le premier terme.',f'Il y a neuf ajouts : ${start}+(9\\times{step})={start+9*step}$.',f'Le dixième terme est ${start+9*step}$.'),
        q('Avec la règle « doubler puis ajouter 1 », poursuivre 7 ; 15 ; 31 par deux termes.','Appliquer les deux actions à chaque passage.','$31\\times2=62$, puis $62+1=63$. Ensuite $63\\times2=126$, puis $126+1=127$.','Les deux termes suivants sont 63 et 127.')] ))
    inc=[4,6,8][level]; first=[5,7,9][level]; far=[10,15,20][level]
    out.append(('Des motifs qui grandissent',f'Un motif contient {first} carreaux à l’étape 1. Chaque nouvelle étape ajoute {inc} carreaux. La règle est conservée.',[
        q('Combien de carreaux contient l’étape 3 ?','Effectuer deux ajouts après l’étape 1.',f'${first}+(2\\times{inc})={first+2*inc}$.',f'L’étape 3 contient ${first+2*inc}$ carreaux.'),
        q(f'Combien de carreaux contient l’étape {far} ?','Compter un ajout de moins que le numéro de l’étape.',f'Il y a ${far-1}$ ajouts : ${first}+({far-1}\\times{inc})={first+(far-1)*inc}$.',f'L’étape {far} contient ${first+(far-1)*inc}$ carreaux.'),
        q(f'À quelle étape y a-t-il {first+7*inc} carreaux ?','Compter les ajouts puis revenir au numéro de l’étape.',f'${first+7*inc}-{first}={7*inc}$, soit 7 ajouts de ${inc}$. Après sept ajouts à partir de l’étape 1, on est à l’étape 8.',f'Il s’agit de l’étape 8.')] ))
    start=[4,7,12][level]; add=[2,3,5][level]; mul=[3,4,5][level]; sub=[1,2,3][level]
    out.append(('Exécuter trois instructions',f'Programme : ajouter {add} ; multiplier le résultat par {mul} ; retirer {sub}.',[
        q(f'Exécuter le programme avec {start}.','Noter chaque résultat intermédiaire.',f'${start}+{add}={start+add}$ ; ${start+add}\\times{mul}={(start+add)*mul}$ ; ${(start+add)*mul}-{sub}={(start+add)*mul-sub}$.',f'Le résultat est ${(start+add)*mul-sub}$.'),
        q(f'Exécuter le programme avec {start+2}.','Répéter les trois instructions dans l’ordre.',f'${start+2}+{add}={start+2+add}$ ; ${start+2+add}\\times{mul}={(start+2+add)*mul}$ ; ${(start+2+add)*mul}-{sub}={(start+2+add)*mul-sub}$.',f'Le résultat est ${(start+2+add)*mul-sub}$.'),
        q(f'Quel nombre de départ donne {(start+add)*mul-sub} ?','Défaire les trois instructions dans l’ordre inverse.',f'On ajoute ${sub}$ : on obtient ${(start+add)*mul}$ ; on divise par ${mul}$ : on obtient ${start+add}$ ; on retire ${add}$ : on retrouve ${start}$.',f'Le nombre de départ est ${start}$.')] ))
    out.append(('Tester et produire un programme','Le programme A ajoute 2, multiplie par 4 puis retire 3. Le programme B multiplie par 4, ajoute 2 puis retire 3.',[
        q(f'Calculer le résultat de A pour {start}.','Respecter l’ordre des instructions.',f'${start}+2={start+2}$ ; ${start+2}\\times4={(start+2)*4}$ ; ${(start+2)*4}-3={(start+2)*4-3}$.',f'A donne ${(start+2)*4-3}$.'),
        q(f'Calculer le résultat de B pour {start} et comparer.','Calculer le programme B indépendamment.',f'${start}\\times4={start*4}$ ; ${start*4}+2={start*4+2}$ ; ${start*4+2}-3={start*4-1}$. Les résultats diffèrent de 6.',f'B donne ${start*4-1}$, soit 6 de moins que A.'),
        q(f'Proposer trois instructions qui transforment {start} en {start*3+5}, puis tester.','Choisir des actions et vérifier chaque étape.',f'Une possibilité est : multiplier par 3 ; ajouter 7 ; retirer 2. Test : ${start}\\times3={start*3}$ ; ${start*3}+7={start*3+7}$ ; ${start*3+7}-2={start*3+5}$.','Une réponse possible : multiplier par 3, ajouter 7, retirer 2.')] ))
    # Trois problèmes de point de vue distincts ; la figure du cours fournit les repères.
    if level==0:
        context='Sur un quadrillage, les colonnes A à F vont de gauche à droite et les lignes 1 à 6 de bas en haut. Un robot part de B2 et regarde vers la droite de la page.'
        qs=[q('Il avance de 2 cases. Quelle est sa position ?','Avancer dans la direction du regard.','De B2, il passe par C2 puis atteint D2.','Il est en D2 et regarde vers la droite.'),q('Il tourne à gauche puis avance d’une case. Où arrive-t-il ?','Tourner sur place puis avancer.','Depuis la droite de la page, un quart de tour à gauche oriente vers le haut ; de D2 il atteint D3.','Il arrive en D3 et regarde vers le haut.'),q('Écrire un programme de retour en B2.','Décrire un chemin et vérifier chaque changement d’orientation.','Depuis D3, tourner à gauche (vers la gauche de la page), avancer de 2 cases en B3, tourner à gauche (vers le bas), avancer d’une case en B2.','Tourner à gauche ; avancer de 2 ; tourner à gauche ; avancer de 1.')]
    elif level==1:
        context='Sur un quadrillage, A à F vont de gauche à droite et 1 à 6 de bas en haut. Le robot part de D4 en regardant vers le bas de la page.'
        qs=[q('Il tourne à droite : vers où regarde-t-il ?','Adopter le point de vue du robot.','En regardant vers le bas, sa droite se trouve à gauche de la page. Le quart de tour ne change pas sa case.','Il reste en D4 et regarde vers la gauche de la page.'),q('Il avance de 2 cases, tourne à gauche puis avance de 1. Où arrive-t-il ?','Noter position et orientation après chaque instruction.','Il atteint B4 en regardant à gauche. Un quart de tour à gauche l’oriente vers le bas. Il avance en B3.','Il arrive en B3 et regarde vers le bas.'),q('Un camarade le place en F4 après le premier déplacement. Quelle erreur a-t-il faite ?','Distinguer la droite de la page de celle du robot.','F4 est à droite de D4 sur la page. Le robot orienté vers le bas avait tourné vers la gauche de la page.','Il a confondu la droite du robot et celle du lecteur ; la bonne case était B4.')]
    else:
        context='Sur un quadrillage, A à F vont de gauche à droite et 1 à 6 de bas en haut. Un robot part de C3 en regardant vers le haut de la page.'
        qs=[q('Exécuter : avancer de 2 ; tourner à droite ; avancer de 2 ; tourner à droite ; avancer de 1.','Tenir une trace après chaque instruction.','C3 devient C5 ; le robot regarde ensuite à droite et atteint E5 ; il tourne vers le bas et atteint E4.','Il arrive en E4 et regarde vers le bas.'),q('Écrire un programme qui le ramène en C3.','Choisir un chemin horizontal puis vertical.','Depuis E4 et le regard vers le bas : tourner à droite, avancer de 2 en C4, tourner à gauche, avancer de 1 en C3.','Tourner à droite ; avancer de 2 ; tourner à gauche ; avancer de 1.'),q('Le programme « tourner à gauche, avancer de 2 » le ramène-t-il de E4 à C4 ?','Tester sa droite et sa gauche en regardant vers le bas.','Depuis E4 orienté vers le bas, tourner à gauche fait regarder vers la droite de la page. Deux pas mèneraient en G4, hors du quadrillage.','Non ; il faut tourner à droite pour aller vers C4.')]
    out.append(('Coder un chemin et changer de point de vue',context,qs))
    return out

GENERATORS=[operations,divisions,decimals,proportions,regularities]
for idx,n in enumerate(NAMES):
    write(n,'etat.json',json.dumps({'statut':'en_cours','agent':'cm2_calculs','maj':'2026-11-01'},ensure_ascii=False,indent=2))
    write(n,'cours_nouveau.txt',COURSES[idx]);write(n,'fiche_nouvelle.txt',SHEETS[idx])
    blocks=[];cover=[]
    for level in range(3):
        for family,(title,context,qs) in enumerate(GENERATORS[idx](level),1):
            i=level*7+family
            blocks.append(block(i,title+[' — premiers pas',' — consolider',' — chercher'][level],level,context,qs))
            cover.append({'id':f'nouveau-{i}','famille':title,'niveau':['easy','medium','hard'][level],'questions':len(qs)})
    # Les séparateurs seuls sont indispensables au parseur de l'aperçu.
    write(n,'exercices.txt','\n===\n\n'.join(blocks))
    write(n,'couverture.json',json.dumps(cover,ensure_ascii=False,indent=2))
    write(n,'COUVERTURE.md','# Couverture CM2\n\n21 exercices, 7 familles déclinées sur 3 niveaux, 3 questions par exercice.\n\n'+ '\n'.join(f'- {c["id"]} : {c["famille"]} ({c["niveau"]}) ; 3 questions avec méthode, raisonnement et résultat.' for c in cover)+'\n\nRéférence : BO cycle 3, annexe 2 (programme applicable au CM2 à la rentrée 2026). Exemples Eduscol CM2 2025. Les choix ont été contrôlés dans les deux PDF officiels.\n\nhttps://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf\nhttps://eduscol.education.gouv.fr/sites/default/files/document/exemplesmiseenoeuvrecm2-mathpdf-111537.pdf')
print('5 chapitres rédigés, 105 exercices et 315 questions.')
