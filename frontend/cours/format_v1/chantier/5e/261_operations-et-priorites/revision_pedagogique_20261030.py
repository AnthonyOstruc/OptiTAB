"""Exercices diversifiés, rédigés question par question ; identifiants conservés."""
from pathlib import Path
import json
import re
import runpy

BASE=Path(__file__).resolve().parent.parent
MARK='<!-- optitab:1 -->'
EX={}

def Q(question,method,steps,answer):
    return {'question':question,'methode':method,'etapes':steps,'reponse':answer}

def add(eid,title,difficulty,intro,qs,note,checks):
    EX[eid]={'titre':title,'difficulte':difficulty,'introduction':intro,'questions':qs,'note':note,'calculs_controles':checks}

def math(s):
    if s.count('=')>=2 and not any(t in s for t in (r'\begin',r'\quad',r'\qquad','<','>')):
        left,*right=s.split('=')
        s=r'\begin{aligned}'+left+'&='+r'\\&='.join(right)+r'\end{aligned}'
    return '$$'+s+'$$'

# 261 — vocabulaire, priorités, parenthèses, calcul mental, décision et critique.
add(2709,'Découverte - Opérations et priorités - Calculer dans le bon ordre','easy','Calculer sans calculatrice et expliquer la priorité utilisée.',[
 Q(r'Calculer $20-12\div3\times2$.','Effectuer divisions et multiplications avant la soustraction.', [('Diviser puis multiplier',math(r'12\div3\times2=4\times2=8')),('Terminer la différence',math('20-8=12'))],r'$12$.'),
 Q(r'Calculer $30\div5\times2$.','Avancer de gauche à droite entre opérations de même priorité.', [('Suivre l’ordre de lecture',math(r'\begin{aligned}30\div5\times2&=6\times2\\&=12\end{aligned}'))],r'$12$.'),
 Q(r'Un élève trouve $3$ à la question 2 en calculant $30\div(5\times2)$. Expliquer son erreur.','Comparer les regroupements imposés par les deux écritures.', [('Identifier la modification',r'Les parenthèses ont été ajoutées : dans l’expression initiale, on doit d’abord diviser 30 par 5.'),('Contrôler le calcul différent',math(r'30\div(5\times2)=30\div10=3'))],r'Les parenthèses ajoutées changent le calcul : le résultat demandé est $12$, pas $3$.')
],r'À priorité égale, on calcule de gauche à droite : une multiplication ne passe pas devant une division.', [('20-12/3*2','12'),('30/5*2','12'),('30/(5*2)','3')])
add(2710,'Découverte - Opérations et priorités - Choisir les parenthèses','easy','Les mêmes nombres peuvent donner des résultats différents selon les regroupements.',[
 Q(r'Calculer $A=18-6\div3$ et $B=(18-6)\div3$.','Calculer d’abord ce que les priorités ou les parenthèses imposent.', [('Sans parenthèses',math(r'A=18-2=16')),('Avec parenthèses',math(r'B=12\div3=4'))],r'$A=16$ et $B=4$.'),
 Q(r'Calculer $C=24\div(3\times2)$.','Calculer tout le diviseur avant la division.', [('Former le diviseur',math(r'3\times2=6')),('Diviser',math(r'C=24\div6=4'))],r'$C=4$.'),
 Q(r'Ajouter une paire de parenthèses à $8+4\times3$ pour obtenir $36$.','Faire effectuer l’addition avant la multiplication.', [('Regrouper la somme',math(r'(8+4)\times3=12\times3=36'))],r'$(8+4)\times3=36$.')
],r'Une parenthèse regroupe une quantité : on ne l’ajoute pas au hasard.', [('18-6/3','16'),('(18-6)/3','4'),('24/(3*2)','4'),('(8+4)*3','36')])
add(2716,'Entraînement - Opérations et priorités - Du vocabulaire à l’expression','medium','Écrire une seule expression pour chaque description, puis calculer.',[
 Q('Calculer le produit de 4 par la somme de 7 et de 5.','Regrouper la somme qui constitue un facteur.', [('Traduire les mots',r'Les facteurs sont 4 et la somme $7+5$, donc l’expression est $4\times(7+5)$.'),('Respecter le regroupement',math(r'\begin{aligned}4\times(7+5)&=4\times12\\&=48\end{aligned}'))],r'$4\times(7+5)=48$.'),
 Q('Calculer la différence entre 50 et le quotient de 18 par 3.','Identifier les deux termes de la différence.', [('Identifier le second terme',r'Le quotient à soustraire est $18\div3$.'),('Calculer le quotient puis la différence',math(r'\begin{aligned}50-18\div3&=50-6\\&=44\end{aligned}'))],r'$50-18\div3=44$.'),
 Q('Quelle est la dernière opération de chacune des deux expressions ? Que permet-elle de nommer ?','Lire la structure extérieure de l’expression.', [('Repérer les opérations finales',r'À la question 1, on termine par multiplier 4 par 12. À la question 2, on termine par soustraire 6 à 50.')],r'Question 1 : multiplication, donc produit ; question 2 : soustraction, donc différence.')
],r'La nature d’une expression dépend de la dernière opération effectuée.', [('4*(7+5)','48'),('50-18/3','44')])
add(2717,'Entraînement - Opérations et priorités - Calculer mentalement avec la distributivité','medium','Choisir une écriture qui simplifie le calcul ; détailler la transformation.',[
 Q(r'Calculer $37\times99$.','Remplacer 99 par une différence proche de 100.', [('Décomposer un facteur',math(r'37\times99=37\times(100-1)')),('Distribuer puis calculer',math(r'\begin{aligned}37\times(100-1)&=3\,700-37\\&=3\,663\end{aligned}'))],r'$3\,663$.'),
 Q(r'Calculer $24\times17+24\times3$.','Regrouper le facteur commun aux deux produits.', [('Reconnaître 24 dans les deux produits',math(r'24\times17+24\times3=24\times(17+3)')),('Calculer le produit simplifié',math(r'24\times20=480'))],r'$480$.'),
 Q(r'Calculer $3{,}5\times18$, puis vérifier l’ordre de grandeur.','Remplacer 18 par 20 moins 2.', [('Distribuer',math(r'3{,}5\times18=3{,}5\times20-3{,}5\times2')),('Calculer et contrôler',math(r'70-7=63')+r'\n\nLe résultat est inférieur à $3{,}5\times20=70$, comme prévu.')],r'$63$.')
],r'Développer ou regrouper sert à simplifier le calcul, tout en conservant exactement sa valeur.', [('37*99','3663'),('24*17+24*3','480'),('3.5*18','63')])
add(2723,'Problème - Opérations et priorités - Comparer deux tarifs de sortie','hard',r'Pour une sortie, le tarif A comprend 28 € de forfait et $3{,}5$ € par personne. Le tarif B comprend 15 € de forfait et $4{,}2$ € par personne.',[
 Q('Quel tarif est le moins cher pour 18 personnes ? De combien ?','Comparer les coûts totaux pour le même effectif.', [('Calculer chaque coût',math(r'\begin{aligned}A&=28+18\times3{,}5=91\\B&=15+18\times4{,}2=90{,}6\end{aligned}')),('Comparer',math(r'91-90{,}6=0{,}4'))],r'Le tarif B coûte $0{,}40$ € de moins.'),
 Q('Le choix est-il le même pour 20 personnes ?','Recalculer les deux expressions avec le nouvel effectif.', [('Adapter les deux coûts',math(r'\begin{aligned}A&=28+20\times3{,}5=98\\B&=15+20\times4{,}2=99\end{aligned}')),('Décider',r'Cette fois, $98<99$ : le tarif A devient le moins cher.')],r'Non : le tarif A est moins cher de 1 €.'),
 Q('Avec 95 €, combien de personnes au maximum peut-on financer avec le tarif A ? Justifier le maximum.','Retirer le forfait puis encadrer le nombre entier de personnes.', [('Calculer la somme disponible',math('95-28=67')),('Tester deux effectifs consécutifs',math(r'19\times3{,}5=66{,}5\le67<70=20\times3{,}5'))],r'19 personnes au maximum ; coût $94{,}50$ €. La 20e ferait dépasser le budget.')
],r'Le tarif le plus avantageux peut changer avec l’effectif. Un maximum entier se justifie en montrant que l’entier suivant ne convient plus.', [('28+18*3.5','91'),('15+18*4.2','90.6'),('28+20*3.5','98'),('15+20*4.2','99'),('28+19*3.5','94.5')])
add(2724,'Problème - Opérations et priorités - Vérifier une facture avec remise','hard',r'Une association commande 4 boîtes contenant chacune 6 cahiers. Un cahier coûte $1{,}75$ €. Une remise globale de 3 € est accordée ; la livraison globale coûte 5 €. Le budget est de 50 €.',[
 Q('Écrire une seule expression du montant à payer, puis calculer.','Distinguer le prix répété et les montants appliqués une seule fois.', [('Calculer le prix des cahiers',math(r'4\times6\times1{,}75=24\times1{,}75=42')),('Appliquer remise et livraison',math('42-3+5=44'))],r'$4\times6\times1{,}75-3+5=44$ €.'),
 Q(r'Un élève calcule $4\times(6\times1{,}75-3)+5$. Pourquoi sa facture est-elle fausse ? Quel est l’écart ?','Repérer la remise appliquée à tort à chaque boîte.', [('Calculer la facture erronée',math(r'4\times(10{,}5-3)+5=4\times7{,}5+5=35')),('Expliquer l’écart',math(r'4\times3-3=9')+r'\n\nLa remise a été comptée quatre fois au lieu d’une.')],r'La facture est sous-estimée de 9 € : 35 € au lieu de 44 €.'),
 Q('Peut-on acheter une cinquième boîte en gardant la même remise et la même livraison ?','Ajouter uniquement le prix d’une boîte supplémentaire.', [('Calculer le nouveau montant',math(r'44+6\times1{,}75=44+10{,}5=54{,}5')),('Comparer au budget',math(r'54{,}5-50=4{,}5'))],r'Non : il manquerait $4{,}50$ €.')
],r'Une remise ou un forfait global ne doit pas être placé dans une parenthèse répétée pour chaque boîte.', [('4*6*1.75-3+5','44'),('4*(6*1.75-3)+5','35'),('44+6*1.75','54.5')])

# 262 — critères, preuve du reste, chiffre inconnu, énumération et contraintes.
add(2730,'Découverte - Multiples, diviseurs et partages - Utiliser les critères de divisibilité','easy','On étudie les nombres 126, 245, 270 et 301.',[
 Q('Lesquels sont divisibles par 2, par 5 et par 10 ?','Examiner uniquement le chiffre des unités.', [('Lire les unités',r'126 finit par 6 ; 245 par 5 ; 270 par 0 ; 301 par 1.'),('Appliquer les trois critères',r'Les unités paires donnent la divisibilité par 2 ; 0 ou 5 par 5 ; 0 par 10.')],r'Par 2 : 126 et 270 ; par 5 : 245 et 270 ; par 10 : 270.'),
 Q('Lesquels sont divisibles par 3 ? Par 9 ?','Additionner les chiffres avant de tester la divisibilité.', [('Calculer les sommes des chiffres',math(r'\begin{aligned}1+2+6&=9\\2+4+5&=11\\2+7+0&=9\\3+0+1&=4\end{aligned}')),('Conclure',r'Seules les sommes associées à 126 et 270 sont multiples de 3 et de 9.')],r'126 et 270 sont divisibles par 3 et par 9.'),
 Q('301 est-il divisible par 7 ? Vérifier par un produit.','Un critère non satisfait pour 2, 3 ou 5 n’interdit pas un autre diviseur.', [('Chercher puis vérifier',math(r'7\times43=301'))],r'Oui : $301=7\times43$.')
],r'Chaque critère porte sur un diviseur précis : ne pas être divisible par 3 ne signifie pas n’avoir aucun autre diviseur.', [('126/9','14'),('270/9','30'),('7*43','301')])
add(2731,'Découverte - Multiples, diviseurs et partages - Reconnaître une division euclidienne','easy',r'Pour diviser 93 par 7, on propose $93=7\times13+2$ ou $93=7\times12+9$.',[
 Q('Les deux égalités sont-elles exactes ?','Vérifier le produit et le reste par un calcul.', [('Calculer les deux seconds membres',math(r'\begin{aligned}7\times13+2&=91+2=93\\7\times12+9&=84+9=93\end{aligned}'))],r'Oui, les deux égalités sont exactes.'),
 Q('Laquelle décrit la division euclidienne de 93 par 7 ?','Ajouter à l’égalité la condition sur le reste.', [('Vérifier les restes',r'Le reste 2 satisfait $0\le2<7$. Le reste 9 ne convient pas, car $9\\ge7$.')],r'$93=7\times13+2$ : quotient 13, reste 2.'),
 Q('Effectuer la division euclidienne de 61 par 8 et la contrôler.','Encadrer 61 par deux multiples consécutifs de 8.', [('Encadrer',math(r'8\times7=56\le61<64=8\times8')),('Calculer et vérifier le reste',math('61-56=5')+r'\n\nOn a bien $0\le5<8$.')],r'$61=8\times7+5$ : quotient 7, reste 5.')
],r'Une égalité correcte ne suffit pas : le reste doit être positif ou nul et strictement inférieur au diviseur.', [('7*13+2','93'),('7*12+9','93'),('61-8*7','5')])
add(2737,'Entraînement - Multiples, diviseurs et partages - Trouver un chiffre inconnu','medium',r'On note $4\square2$ un entier à trois chiffres dont le chiffre des dizaines est inconnu.',[
 Q('Quels chiffres peut-on placer pour que le nombre soit divisible par 2 et par 3 ?','Combiner le critère des unités avec la somme des chiffres.', [('Traiter la divisibilité par 2',r'Le chiffre des unités est 2 : le nombre sera pair quel que soit le chiffre choisi.'),('Tester la somme des chiffres',r'La somme vaut $4+\square+2=6+\square$. Elle est multiple de 3 pour $\square=0$, $3$, $6$ ou $9$.')],r'Les chiffres possibles sont 0, 3, 6 et 9 : 402, 432, 462 et 492.'),
 Q('Lequel de ces nombres est divisible par 9 ?','Chercher une somme des chiffres multiple de 9.', [('Examiner les sommes',r'Les sommes des chiffres sont respectivement 6, 9, 12 et 15. Seul 9 convient.'),('Contrôler',math(r'432=9\times48'))],r'$432$.'),
 Q('Peut-on obtenir un nombre divisible par 5 ?','Vérifier le chiffre des unités, qui est imposé.', [('Confronter les unités possibles',r'Un multiple de 5 finit par 0 ou par 5. Ici, tous les nombres finissent par 2.')],r'Non, quel que soit le chiffre des dizaines.')
],r'Plusieurs contraintes doivent être satisfaites simultanément. Une condition sur les unités peut rendre toute recherche impossible.', [('432/9','48')])
add(2738,'Entraînement - Multiples, diviseurs et partages - Des rectangles d’aire imposée','medium',r'Un rectangle a une aire de $36\ \mathrm{cm}^2$. Ses côtés mesurent des nombres entiers de centimètres. Deux rectangles obtenus en échangeant longueur et largeur ne comptent qu’une fois.',[
 Q('Trouver toutes les dimensions possibles.','Énumérer les paires de diviseurs dont le produit vaut 36.', [('Chercher les produits par paires',math(r'36=1\times36=2\times18=3\times12=4\times9=6\times6')),('Justifier l’arrêt',r'Après $6\times6$, on retrouve les mêmes paires dans l’ordre inverse.')],r'$1\times36$, $2\times18$, $3\times12$, $4\times9$ et $6\times6$ cm.'),
 Q('Calculer les périmètres et trouver le plus petit.','Utiliser deux fois la somme des deux côtés pour chaque paire.', [('Comparer dans un tableau',r'| Côtés (cm) | Périmètre (cm) |\n|---|---|\n| 1 et 36 | 74 |\n| 2 et 18 | 40 |\n| 3 et 12 | 30 |\n| 4 et 9 | 26 |\n| 6 et 6 | 24 |'),('Choisir le minimum',r'Les cinq possibilités ont été testées : le plus petit périmètre est 24 cm.')],r'Le carré de côté 6 cm a le périmètre minimal : 24 cm.'),
 Q('Même aire signifie-t-il même périmètre ? Donner un contre-exemple.','Comparer deux lignes du tableau.', [('Exhiber deux cas',r'Les rectangles de côtés 1 et 36, et de côtés 6 et 6, ont tous deux une aire de 36 cm². Leurs périmètres sont 74 cm et 24 cm.')],r'Non : les périmètres 74 cm et 24 cm sont différents malgré la même aire.')
],r'Une recherche par paires évite les doublons et permet de prouver que tous les cas ont été examinés.', [('2*(1+36)','74'),('2*(2+18)','40'),('2*(3+12)','30'),('2*(4+9)','26'),('2*(6+6)','24')])
add(2744,'Problème - Multiples, diviseurs et partages - Des lots sous plusieurs contraintes','hard','On dispose de 84 cartes rouges et de 126 cartes bleues. Tous les lots doivent avoir la même composition et utiliser toutes les cartes.',[
 Q('Trouver tous les nombres de lots possibles.','Chercher les diviseurs communs aux deux effectifs.', [('Lister les diviseurs de chaque effectif',r'84 : 1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84.\n\n126 : 1, 2, 3, 6, 7, 9, 14, 18, 21, 42, 63, 126.'),('Garder l’intersection des listes',r'Les nombres qui figurent dans les deux listes sont 1, 2, 3, 6, 7, 14, 21 et 42.')],r'1, 2, 3, 6, 7, 14, 21 ou 42 lots.'),
 Q('On ne peut préparer que 20 lots au maximum. Quel est alors le plus grand nombre de lots, et leur composition ?','Filtrer les diviseurs communs avec la contrainte supplémentaire.', [('Écarter les effectifs trop grands',r'21 et 42 dépassent 20. Le plus grand effectif restant est 14.'),('Calculer la composition',math(r'84\div14=6\qquad126\div14=9'))],r'14 lots de 6 cartes rouges et 9 cartes bleues.'),
 Q('On abandonne la limite de 20 lots, mais chaque lot doit contenir au moins quatre cartes de chaque couleur. Quel maximum obtient-on ?','Rechercher la plus grande possibilité qui respecte les deux minima.', [('Tester les plus grands effectifs',r'Avec 42 lots, chaque lot contient 2 rouges et 3 bleues : cela ne convient pas.'),('Vérifier l’effectif suivant',math(r'84\div21=4\qquad126\div21=6')+r'\n\n21 est le plus grand diviseur commun restant.')],r'21 lots de 4 rouges et 6 bleues.')
],r'Le plus grand diviseur commun ne suffit pas toujours : il faut encore vérifier toutes les contraintes de l’énoncé.', [('84/14','6'),('126/14','9'),('84/21','4'),('126/21','6')])
add(2745,'Problème - Multiples, diviseurs et partages - Deux navettes aux départs décalés','hard','La navette A part à 9 h 10 puis toutes les 8 minutes. La navette B part à 9 h 14 puis toutes les 12 minutes. Elles poursuivent leurs rotations toute la matinée.',[
 Q('Écrire les départs de chaque navette jusqu’à 9 h 50 inclus.','Ajouter chaque période à son propre premier départ.', [('Établir les deux listes',r'| Navette | Départs |\n|---|---|\n| A | 9 h 10 ; 9 h 18 ; 9 h 26 ; 9 h 34 ; 9 h 42 ; 9 h 50 |\n| B | 9 h 14 ; 9 h 26 ; 9 h 38 ; 9 h 50 |')],r'A : 9 h 10, 18, 26, 34, 42 et 50 ; B : 9 h 14, 26, 38 et 50.'),
 Q('Quel est leur premier départ simultané ? Combien de rotations se sont écoulées depuis chaque départ initial ?','Chercher la première heure commune, en tenant compte du décalage initial.', [('Lire la première heure commune',r'La première heure présente dans les deux listes est 9 h 26.'),('Compter séparément les périodes écoulées',math(r'26-10=16=2\times8')+r'\n\n'+math(r'26-14=12=1\times12'))],r'À 9 h 26 : deux périodes pour A et une pour B.'),
 Q('Après ce rendez-vous, combien de minutes séparent deux départs simultanés ? Donner les deux rendez-vous suivants.','Une fois réunies, chercher le premier multiple positif commun aux périodes.', [('Chercher une durée commune',r'Multiples de 8 : 8, 16, 24. Multiples de 12 : 12, 24. La première durée commune vaut 24 min.'),('Ajouter cette durée aux heures',r'9 h 26 + 24 min = 9 h 50 ; puis 9 h 50 + 24 min = 10 h 14.')],r'Toutes les 24 min : 9 h 50 puis 10 h 14.')
],r'Lorsque les premiers départs sont décalés, chercher d’abord une heure commune ; les multiples de la seule période ne donnent pas directement cette heure.', [('26-10','16'),('26-14','12'),('50-26','24'),('74-50','24')])

# 263 — décimaux, lecture fine, encadrement, ordres distincts et contraintes.
add(2751,'Découverte - Découvrir les nombres relatifs - Comparer des températures décimales','easy',r'On relève les températures suivantes : $-2{,}8$ °C ; $-2{,}35$ °C ; $0$ °C ; $1{,}2$ °C ; $-0{,}5$ °C.',[
 Q('Quelles températures sont strictement négatives ? Et strictement positives ?','Comparer chacune des valeurs à zéro.', [('Séparer les signes',r'Trois nombres portent un signe moins et sont différents de zéro. $1{,}2$ est supérieur à zéro. Zéro n’est ni strictement positif ni strictement négatif.')],r'Négatives : $-2{,}8$, $-2{,}35$, $-0{,}5$ °C ; positive : $1{,}2$ °C.'),
 Q('Ranger les cinq températures dans l’ordre croissant.','Entre deux négatifs, le plus éloigné de zéro est le plus petit.', [('Comparer les décimaux négatifs',r'$-2{,}8=-2{,}80$ est plus éloigné de zéro que $-2{,}35$.'),('Rassembler tous les nombres',math(r'-2{,}8<-2{,}35<-0{,}5<0<1{,}2'))],r'$-2{,}8<-2{,}35<-0{,}5<0<1{,}2$.'),
 Q(r'Un élève affirme que $-2{,}35<-2{,}8$ car $35<80$. Pourquoi cela ne convient-il pas ?','Comparer les nombres entiers ou décimaux complets, puis tenir compte du signe.', [('Identifier l’inversion chez les négatifs',r'$2{,}35<2{,}80$ ; mais les nombres négatifs correspondants se rangent dans l’autre sens.')],r'La comparaison correcte est $-2{,}8<-2{,}35$.')
],r'Ajouter des zéros à droite d’un décimal conserve sa valeur. Entre deux négatifs, la comparaison des distances à zéro est inversée.', [('-2.8 < -2.35','True'),('-2.35 < -0.5','True')])
add(2752,'Découverte - Découvrir les nombres relatifs - Lire une graduation au quart','easy',r'Sur cette droite, les graduations sont régulières. Les abscisses 0 et 1 sont indiquées.\n\n[IMAGE_1]',[
 Q('Quel écart représente une graduation ?','Compter les intervalles entre 0 et 1.', [('Compter les intervalles égaux',r'Entre les graduations 0 et 1, on compte quatre intervalles.'),('Partager l’unité',math(r'1\div4=0{,}25'))],r'Une graduation représente $0{,}25$.'),
 Q(r'Lire les abscisses de $A$, $B$ et $C$.','Compter les graduations à partir de zéro et choisir le signe.', [('Lire les points à gauche de zéro',r'$A$ est à trois graduations à gauche de 0 : son abscisse vaut $-0{,}75$. $C$ est à une graduation à gauche de 0 : $-0{,}25$.'),('Lire le point à droite de zéro',r'$B$ est à deux graduations à droite de 0 : son abscisse vaut $0{,}5$.')],r'$A(-0{,}75)$, $B(0{,}5)$, $C(-0{,}25)$.'),
 Q(r'Placer le point $D$ dont l’abscisse est l’opposée de celle de $A$.','Reporter la même distance à zéro de l’autre côté de l’origine.', [('Déterminer l’abscisse',r'L’opposé de $-0{,}75$ est $0{,}75$.'),('Placer sur la graduation',r'$D$ se place à trois graduations à droite de 0.\n\n[IMAGE_2]')],r'$D(0{,}75)$.')
],r'Pour lire une graduation, compter les intervalles, pas les traits. Un opposé conserve la distance à zéro.', [('1/4','0.25'),('-3/4','-0.75'),('2/4','0.5')])
add(2758,'Entraînement - Découvrir les nombres relatifs - Encadrer et intercaler un décimal','medium',r'On travaille avec le nombre $-3{,}47$.',[
 Q('L’encadrer par deux entiers consécutifs.','Repérer les deux graduations entières voisines.', [('Comparer les distances à zéro',r'Le nombre est plus éloigné de zéro que $-3$, mais moins éloigné de zéro que $-4$.')],r'$-4<-3{,}47<-3$.'),
 Q('L’encadrer par deux nombres consécutifs au dixième.','Compléter les dixièmes avec un zéro pour comparer.', [('Écrire les bornes au centième',r'$-3{,}5=-3{,}50$ et $-3{,}4=-3{,}40$.'),('Placer le nombre entre les bornes',math(r'-3{,}50<-3{,}47<-3{,}40'))],r'$-3{,}5<-3{,}47<-3{,}4$.'),
 Q(r'Donner un décimal strictement compris entre $-3{,}47$ et $-3{,}46$, puis vérifier.','Passer au millième pour disposer de graduations intermédiaires.', [('Proposer un nombre',r'On écrit les bornes $-3{,}470$ et $-3{,}460$. On peut choisir $-3{,}465$.'),('Vérifier les deux comparaisons',math(r'-3{,}470<-3{,}465<-3{,}460'))],r'Par exemple $-3{,}465$.')
],r'Deux décimaux consécutifs au centième ne sont pas deux nombres consécutifs : on peut encore intercaler des millièmes.', [('-4 < -3.47','True'),('-3.47 < -3','True'),('-3.47 < -3.465','True'),('-3.465 < -3.46','True')])
add(2759,'Entraînement - Découvrir les nombres relatifs - Comparer les positions et les distances','medium',r'Les abscisses des points sont : $A(-4{,}5)$, $B(3{,}2)$, $C(-3{,}2)$ et $D(0{,}7)$.',[
 Q('Ranger les points de gauche à droite.','Comparer les abscisses dans l’ordre croissant.', [('Comparer les négatifs puis les positifs',math(r'-4{,}5<-3{,}2<0{,}7<3{,}2'))],r'$A$, $C$, $D$, $B$.'),
 Q('Les ranger du plus éloigné au plus proche de zéro. Signaler les égalités.','Comparer cette fois les distances à zéro.', [('Former le tableau des distances',r'| Point | $A$ | $B$ | $C$ | $D$ |\n|---|---|---|---|---|\n| Distance à zéro | $4{,}5$ | $3{,}2$ | $3{,}2$ | $0{,}7$ |'),('Trier les distances',r'$4{,}5>3{,}2>0{,}7$ ; les points $B$ et $C$ sont à égalité.')],r'$A$, puis $B$ et $C$ à égalité, puis $D$.'),
 Q('Quels points ont des abscisses opposées ? Justifier les deux conditions.','Vérifier à la fois la distance à zéro et le côté de l’origine.', [('Vérifier la distance',r'$B$ et $C$ ont tous deux une distance à zéro de $3{,}2$.'),('Vérifier les signes',r'Leurs abscisses $3{,}2$ et $-3{,}2$ ont des signes contraires.')],r'$B$ et $C$.')
],r'Le classement des positions et celui des distances à zéro sont deux classements différents.', [('-4.5 < -3.2','True'),('abs(-3.2)','3.2')])
add(2765,'Problème - Découvrir les nombres relatifs - Retrouver un nombre sous contraintes','hard',r'Un nombre $x$ est strictement négatif. Sa distance à zéro est strictement comprise entre $2{,}4$ et $2{,}6$. On sait aussi que $x>-2{,}5$.',[
 Q('Traduire la contrainte de distance en un encadrement de x.','Sur le côté négatif, renverser l’ordre des distances à zéro.', [('Situer les deux bornes',r'À distance $2{,}6$ du côté négatif, on trouve $-2{,}6$ ; à distance $2{,}4$, on trouve $-2{,}4$.'),('Choisir les nombres entre les bornes',math(r'-2{,}6<x<-2{,}4'))],r'$-2{,}6<x<-2{,}4$.'),
 Q('Combiner toutes les informations pour obtenir un encadrement plus précis.','Ne garder que les nombres satisfaisant les deux contraintes.', [('Comparer les bornes inférieures',r'La condition $x>-2{,}5$ est plus restrictive que $x>-2{,}6$.'),('Conserver la borne supérieure',r'Il reste toujours nécessaire que $x<-2{,}4$.')],r'$-2{,}5<x<-2{,}4$.'),
 Q('Donner deux solutions différentes et vérifier chacune. Le nombre est-il unique ?','Choisir des centièmes situés strictement entre les deux bornes.', [('Choisir deux candidats',r'$-2{,}45$ et $-2{,}48$ sont tous deux supérieurs à $-2{,}5$ et inférieurs à $-2{,}4$.'),('Vérifier les distances',r'Leurs distances à zéro sont $2{,}45$ et $2{,}48$, toutes deux comprises entre $2{,}4$ et $2{,}6$.')],r'$-2{,}45$ et $-2{,}48$ conviennent ; il n’y a pas unicité.')
],r'Trouver un nombre compatible ne prouve pas qu’il est unique. Chaque contrainte doit être vérifiée.', [('-2.5 < -2.45 < -2.4','True'),('-2.5 < -2.48 < -2.4','True')])
add(2766,'Problème - Découvrir les nombres relatifs - Distinguer trois critères de classement','hard',r'On donne les points $P(-6{,}2)$, $Q(-6{,}02)$, $R(6{,}2)$ et $S(0)$.',[
 Q('Quel point a la plus grande abscisse ? Quels points sont les plus éloignés de zéro ?','Traiter séparément l’ordre des abscisses et celui des distances.', [('Chercher la plus grande abscisse',r'$-6{,}2<-6{,}02<0<6{,}2$ : $R$ a la plus grande abscisse.'),('Chercher le plus grand éloignement',r'Les distances de $P$ et de $R$ à zéro sont égales à $6{,}2$, supérieures à $6{,}02$ et à 0.')],r'Plus grande abscisse : $R$ ; plus grande distance : $P$ et $R$ à égalité.'),
 Q(r'Un élève dit : « Deux points distincts de même distance à zéro ont forcément des abscisses opposées. » A-t-il raison sur une droite graduée ?','Étudier les deux positions possibles à une distance fixée de l’origine.', [('Décrire les positions possibles',r'À une distance non nulle fixée, il existe une position à gauche de zéro et une à droite.'),('Utiliser le fait que les points sont distincts',r'Deux points distincts ne peuvent occuper la même position : ils sont donc de part et d’autre de zéro, à la même distance.')],r'Oui : leurs abscisses sont opposées.'),
 Q(r'Donner un nombre négatif situé entre $-6{,}2$ et $-6{,}02$, dont la distance à zéro dépasse $6{,}1$. Justifier.','Combiner une comparaison d’abscisses avec une comparaison de distances.', [('Proposer une valeur',r'On peut prendre $-6{,}15$.'),('Vérifier les deux exigences',math(r'-6{,}2<-6{,}15<-6{,}02')+r'\n\nSa distance à zéro est $6{,}15>6{,}1$.')],r'Par exemple $-6{,}15$.')
],r'Une propriété « forcément » demande un raisonnement ; un seul exemple ne suffit pas à la prouver.', [('-6.2 < -6.15 < -6.02','True'),('abs(-6.15) > 6.1','True')])

# 264 — signes, soustraction, regroupements, parenthèses et problèmes à étapes.
add(2772,'Découverte - Additionner et soustraire des relatifs - Reconnaître la règle d’addition','easy','Calculer les sommes suivantes en indiquant la règle utilisée.',[
 Q(r'Calculer $(-3{,}5)+(-2{,}4)$.','Même signe : additionner les distances et garder le signe commun.', [('Additionner les distances',math(r'3{,}5+2{,}4=5{,}9')),('Conserver le signe négatif',r'Les deux nombres sont négatifs : leur somme est négative.')],r'$-5{,}9$.'),
 Q(r'Calculer $(+4{,}8)+(+1{,}7)$.','Même signe positif : additionner les distances.', [('Effectuer la somme',math(r'4{,}8+1{,}7=6{,}5'))],r'$6{,}5$.'),
 Q(r'Calculer $(-2{,}75)+(+2{,}75)$ et $0+(-4)$.','Reconnaître les opposés et le rôle de zéro dans une addition.', [('Annuler deux opposés',math(r'(-2{,}75)+(+2{,}75)=0')),('Ajouter zéro',math('0+(-4)=-4'))],r'$0$ et $-4$.')
],r'Zéro ne change pas un nombre lorsqu’on l’ajoute. Deux opposés se compensent exactement.', [('-3.5-2.4','-5.9'),('4.8+1.7','6.5'),('-2.75+2.75','0')])
add(2773,'Découverte - Additionner et soustraire des relatifs - Soustraire revient à ajouter l’opposé','easy','Dans chaque cas, transformer la soustraction en addition avant de calculer.',[
 Q(r'Calculer $7-(-4)$.','Prendre l’opposé du nombre soustrait.', [('Transformer',math('7-(-4)=7+(+4)')),('Calculer',math('7+4=11'))],r'$11$.'),
 Q(r'Calculer $-6-(+2)$.','Soustraire un positif revient à ajouter un négatif.', [('Transformer',math('-6-(+2)=-6+(-2)')),('Additionner deux négatifs',math('-6+(-2)=-8'))],r'$-8$.'),
 Q(r'Calculer $-3-(-8)$ et expliquer pourquoi le résultat est positif.','Comparer les distances à zéro après transformation.', [('Ajouter l’opposé',math('-3-(-8)=-3+8')),('Comparer les distances',r'La distance 8 dépasse la distance 3. Le nombre le plus éloigné de zéro est positif et $8-3=5$.')],r'$5$.')
],r'Le signe de soustraction et le signe du nombre soustrait ont des rôles distincts.', [('7-(-4)','11'),('-6-2','-8'),('-3-(-8)','5')])
add(2779,'Entraînement - Additionner et soustraire des relatifs - Regrouper sans perdre les signes','medium','Choisir des regroupements utiles, puis calculer.',[
 Q(r'Calculer $-7{,}5+4+7{,}5-9$.','Regrouper d’abord les deux opposés.', [('Faire apparaître l’annulation',math(r'\begin{aligned}-7{,}5+4+7{,}5-9&=(-7{,}5+7{,}5)+(4-9)\\&=0-5\end{aligned}')),('Conclure',math('0-5=-5'))],r'$-5$.'),
 Q(r'Calculer $(-2{,}6)+(-5{,}4)+3+8$.','Regrouper les termes négatifs puis les positifs.', [('Calculer les deux groupes',math(r'(-2{,}6)+(-5{,}4)=-8\qquad3+8=11')),('Comparer les distances restantes',math('-8+11=3'))],r'$3$.'),
 Q(r'Peut-on remplacer $12-7-3$ par $12-(7-3)$ ? Vérifier.','Une modification de parenthèses doit conserver le sens des opérations.', [('Calculer de gauche à droite',math('12-7-3=5-3=2')),('Calculer l’autre regroupement',math('12-(7-3)=12-4=8'))],r'Non : les résultats sont 2 et 8.')
],r'On peut réordonner les termes d’une somme en gardant leur signe ; on ne peut pas déplacer librement les termes d’une soustraction.', [('-7.5+4+7.5-9','-5'),('-2.6-5.4+3+8','3'),('12-7-3','2'),('12-(7-3)','8')])
add(2780,'Entraînement - Additionner et soustraire des relatifs - Calculer avec des parenthèses','medium','Les parenthèses doivent être traitées avant le calcul extérieur.',[
 Q(r'Calculer $8-(3-5)+(-2)$.','Calculer la parenthèse puis ajouter l’opposé de son résultat.', [('Traiter la parenthèse',math('3-5=-2')),('Reprendre le calcul extérieur',math(r'\begin{aligned}8-(-2)+(-2)&=8+2-2\\&=8\end{aligned}'))],r'$8$.'),
 Q(r'Calculer $-4-(-3+7)$.','Ne pas confondre le premier signe du groupe avec le signe de tout son résultat.', [('Calculer la somme intérieure',math('-3+7=4')),('Soustraire le résultat obtenu',math('-4-4=-8'))],r'$-8$.'),
 Q(r'Un élève transforme $-4-(-3+7)$ en $-4+3+7$. Corriger cette transformation sans calculer d’abord la parenthèse.','Le signe moins extérieur change le signe de chaque terme du groupe.', [('Transformer le groupe entier',math('-4-(-3+7)=-4+3-7')),('Vérifier le résultat',math('-4+3-7=-1-7=-8'))],r'Il faut écrire $-4+3-7$, qui vaut $-8$.')
],r'Devant une parenthèse soustraite, changer le signe d’un seul terme est une erreur : tout le groupe est soustrait.', [('8-(3-5)-2','8'),('-4-(-3+7)','-8'),('-4+3-7','-8')])
add(2786,'Problème - Additionner et soustraire des relatifs - Rééquilibrer un compte','hard',r'Un compte présente un solde de $-12{,}50$ €. On reçoit un versement de $18{,}75$ €, puis un paiement de $9{,}40$ € est prélevé.',[
 Q('Calculer le solde après les deux opérations.','Traduire une entrée par un positif et une sortie par un négatif.', [('Calculer après le versement',math(r'-12{,}50+18{,}75=6{,}25')),('Soustraire le prélèvement',math(r'6{,}25-9{,}40=-3{,}15'))],r'$-3{,}15$ €.'),
 Q('Quel versement minimal permettrait de retrouver un solde positif ou nul ?','Compenser exactement la dette pour atteindre zéro.', [('Chercher l’opposé du solde',math(r'-3{,}15+3{,}15=0')),('Justifier le minimum',r'Un versement inférieur à $3{,}15$ € ne compenserait pas toute la dette.')],r'$3{,}15$ €.'),
 Q(r'Au lieu du versement minimal, on verse 10 €, puis on paie $2{,}50$ €. Quel est le solde final ?','Repartir du solde calculé à la question 1 et respecter l’ordre annoncé.', [('Appliquer le versement de 10 €',math(r'-3{,}15+10=6{,}85')),('Déduire le nouveau paiement',math(r'6{,}85-2{,}50=4{,}35'))],r'$4{,}35$ €.')
],r'Le signe d’un montant dépend de l’opération : un versement augmente le solde, un paiement le diminue, même si le solde était déjà négatif.', [('-12.5+18.75-9.4','-3.15'),('-3.15+3.15','0'),('-3.15+10-2.5','4.35')])
add(2787,'Problème - Additionner et soustraire des relatifs - Altitude et dénivelé parcouru','hard',r'Un explorateur part à l’altitude $-15$ m. Il monte de 12 m, descend de 7 m, puis monte de 18 m. Les déplacements sont verticaux.',[
 Q('Calculer l’altitude après chaque déplacement.','Ajouter chaque variation à l’altitude précédente.', [('Traiter les deux premiers déplacements',math('-15+12=-3')+r'\n\n'+math('-3-7=-10')),('Traiter la dernière montée',math('-10+18=8'))],r'Après les déplacements : $-3$ m, $-10$ m, puis $8$ m.'),
 Q('Calculer la variation totale d’altitude et la distance verticale totale parcourue.','Distinguer le bilan signé et la somme des longueurs parcourues.', [('Calculer le bilan',math('8-(-15)=8+15=23')),('Additionner toutes les longueurs',math('12+7+18=37'))],r'Variation totale : $+23$ m ; distance verticale : 37 m.'),
 Q('Quelle variation directe ramènerait au point de départ ? Quelle distance verticale cela représenterait-il ?','Prendre l’opposé de la variation totale pour le retour direct.', [('Calculer la variation de retour',math('-15-8=-23')),('Interpréter la longueur',r'Une descente de 23 m ramène de 8 m à $-15$ m. Sa longueur est positive.')],r'Variation : $-23$ m ; distance du retour direct : 23 m.')
],r'Un déplacement vers le bas est une variation négative mais sa longueur reste positive. Une distance parcourue ne se calcule pas en compensant montées et descentes.', [('-15+12','-3'),('-3-7','-10'),('-10+18','8'),('8-(-15)','23'),('12+7+18','37'),('-15-8','-23')])

# 265 — écritures exactes, équivalence, comparaison, placement et unités.
add(2793,'Découverte - Fractions, quotients et comparaisons - Passer d’une écriture à l’autre','easy','Donner des valeurs exactes ; distinguer une égalité d’une approximation.',[
 Q(r'Écrire $\frac74$ sous forme décimale et comme somme d’un entier et d’une fraction inférieure à 1.','Partager le numérateur par le dénominateur.', [('Décomposer le numérateur',math(r'7=4\times1+3')),('Traduire les deux écritures',math(r'\frac74=1+\frac34=1{,}75'))],r'$\frac74=1+\frac34=1{,}75$.'),
 Q(r'Écrire $0{,}45$ sous forme de fraction, puis simplifier.','Lire les centièmes puis diviser les deux termes par un même entier.', [('Traduire les centièmes',math(r'0{,}45=\frac{45}{100}')),('Simplifier par 5',math(r'\frac{45}{100}=\frac9{20}'))],r'$\frac9{20}$.'),
 Q(r'A-t-on $\frac13=0{,}333$ ? Justifier en multipliant par 3.','Un quotient exact, multiplié par son dénominateur, doit redonner le numérateur.', [('Tester le décimal proposé',math(r'0{,}333\times3=0{,}999')),('Comparer à la définition du quotient',r'$0{,}999\ne1$, donc $0{,}333$ n’est pas exactement un tiers.')],r'Non : $0{,}333$ est une approximation de $\frac13$.')
],r'Une écriture décimale approchée ne remplace pas une fraction exacte dans une égalité.', [('7/4','1.75'),('45/100','9/20'),('0.333*3','0.999')])
add(2794,'Découverte - Fractions, quotients et comparaisons - Compléter des fractions égales','easy','Multiplier ou diviser les deux termes par le même nombre non nul.',[
 Q(r'Simplifier $\frac{18}{24}$.','Reconnaître un diviseur commun aux deux termes.', [('Choisir le diviseur commun',r'18 et 24 sont tous deux divisibles par 6.'),('Diviser les deux termes',math(r'\frac{18}{24}=\frac{18\div6}{24\div6}=\frac34'))],r'$\frac34$.'),
 Q(r'Compléter $\frac58=\frac{\square}{40}$.','Chercher le facteur qui transforme le dénominateur.', [('Trouver le facteur',math(r'8\times5=40')),('Appliquer aussi ce facteur au numérateur',math(r'5\times5=25'))],r'$\frac58=\frac{25}{40}$.'),
 Q(r'Un élève affirme $\frac35=\frac57$ en ajoutant 2 aux deux termes. Vérifier ces fractions au même dénominateur.','Tester l’égalité plutôt que généraliser une règle fausse.', [('Former des parts identiques',math(r'\frac35=\frac{21}{35}\qquad\frac57=\frac{25}{35}')),('Comparer',r'$21\ne25$ : les deux fractions ne sont pas égales.')],r'Faux : $\frac35<\frac57$.')
],r'Ajouter le même nombre aux deux termes ne conserve pas une fraction. La règle porte sur une multiplication ou une division commune.', [('18/24','3/4'),('5/8','25/40'),('3/5 < 5/7','True')])
add(2800,'Entraînement - Fractions, quotients et comparaisons - Construire un dénominateur commun','medium','Comparer sans utiliser d’approximation décimale.',[
 Q(r'Comparer $\frac58$ et $\frac7{12}$.','Transformer les deux fractions en vingt-quatrièmes.', [('Produire des fractions égales',math(r'\frac58=\frac{15}{24}\qquad\frac7{12}=\frac{14}{24}')),('Comparer les numérateurs',r'Les parts sont identiques et $15>14$.')],r'$\frac58>\frac7{12}$.'),
 Q(r'Comparer $\frac9{10}$ et $\frac{11}{12}$.','Choisir 60 comme dénominateur commun.', [('Changer les deux écritures',math(r'\frac9{10}=\frac{54}{60}\qquad\frac{11}{12}=\frac{55}{60}')),('Comparer',r'$54<55$, donc la seconde fraction est la plus grande.')],r'$\frac9{10}<\frac{11}{12}$.'),
 Q(r'Ranger $\frac34$, $\frac58$ et $\frac7{12}$ dans l’ordre croissant.','Exprimer les trois fractions avec les mêmes parts.', [('Écrire en vingt-quatrièmes',math(r'\frac34=\frac{18}{24}\qquad\frac58=\frac{15}{24}\qquad\frac7{12}=\frac{14}{24}')),('Trier les numérateurs',r'$14<15<18$.')],r'$\frac7{12}<\frac58<\frac34$.')
],r'Il n’est pas nécessaire de trouver le plus petit dénominateur commun ; il suffit d’en choisir un qui convient à toutes les fractions.', [('5/8 > 7/12','True'),('9/10 < 11/12','True'),('7/12 < 5/8 < 3/4','True')])
add(2801,'Entraînement - Fractions, quotients et comparaisons - Placer des fractions supérieures à un','medium',r'Chaque unité de cette droite est partagée en quatre intervalles égaux.\n\n[IMAGE_1]',[
 Q(r'Décomposer $\frac{11}{4}$ et $\frac74$ en somme d’un entier et d’une fraction inférieure à 1.','Effectuer la division euclidienne des numérateurs par 4.', [('Décomposer les numérateurs',math(r'11=4\times2+3\qquad7=4\times1+3')),('Diviser chaque terme par 4',math(r'\frac{11}4=2+\frac34\qquad\frac74=1+\frac34'))],r'$\frac{11}4=2+\frac34$ et $\frac74=1+\frac34$.'),
 Q(r'Placer $A\left(\frac{11}4\right)$ et $B\left(\frac74\right)$.','Partir de l’entier trouvé et compter les quarts supplémentaires.', [('Placer les deux points',r'$A$ est trois graduations après 2 ; $B$ trois graduations après 1.\n\n[IMAGE_2]')],r'$A$ est en $2{,}75$ et $B$ en $1{,}75$.'),
 Q(r'Comparer les deux fractions et préciser la distance entre $A$ et $B$.','Compter l’écart en quarts sur la même graduation.', [('Lire l’ordre',r'$A$ est à droite de $B$, donc $\frac{11}4>\frac74$.'),('Compter l’écart',math(r'\frac{11}4-\frac74=\frac44=1'))],r'$\frac{11}4>\frac74$ ; distance $AB=1$ unité.')
],r'Une fraction peut dépasser 1. Le dénominateur partage chaque unité, et non toute la droite.', [('11/4','2.75'),('7/4','1.75'),('11/4-7/4','1')])
add(2807,'Problème - Fractions, quotients et comparaisons - Une réserve et deux unités de référence','hard',r'Une réserve contient initialement 150 L. Le premier jour, on utilise $\frac25$ de la quantité initiale. Le deuxième jour, on utilise $\frac13$ de la quantité restante.',[
 Q('Calculer la quantité utilisée le premier jour puis celle qui reste.','Appliquer la première fraction à la réserve initiale.', [('Calculer la première utilisation',math(r'150\div5\times2=30\times2=60')),('Calculer la nouvelle réserve',math('150-60=90'))],r'60 L utilisés ; il reste 90 L.'),
 Q('Calculer la quantité utilisée le deuxième jour puis le volume final.','La seconde fraction s’applique aux 90 L restants, pas aux 150 L initiaux.', [('Calculer la seconde utilisation',math(r'90\div3=30')),('Calculer le volume final',math('90-30=60'))],r'30 L utilisés le deuxième jour ; il reste 60 L.'),
 Q('Quelle fraction de la réserve initiale a été utilisée au total ? Peut-on additionner directement les deux fractions de l’énoncé ?','Revenir à une même unité avant de comparer les portions.', [('Calculer la quantité totale utilisée',math('60+30=90')),('Exprimer cette quantité dans l’unité initiale',math(r'\frac{90}{150}=\frac35')+r'\n\nLes deux fractions initiales portent sur deux réserves de tailles différentes.')],r'$\frac35$ de la réserve initiale. On ne peut pas additionner directement $\frac25$ et $\frac13$.')
],r'Avant d’appliquer une fraction, écrire explicitement la quantité qui constitue l’unité de référence.', [('150*2/5','60'),('(150-60)/3','30'),('(60+30)/150','3/5')])
add(2808,'Problème - Fractions, quotients et comparaisons - Des fractions différentes pour la même quantité','hard',r'Alice utilise $\frac38$ d’une bouteille de 80 cL. Bilal utilise $\frac5{12}$ d’une bouteille de 72 cL.',[
 Q('Comparer les deux fractions comme nombres.','Les écrire avec un dénominateur commun.', [('Exprimer en vingt-quatrièmes',math(r'\frac38=\frac9{24}\qquad\frac5{12}=\frac{10}{24}')),('Comparer les parts',r'$9<10$.')],r'$\frac38<\frac5{12}$.'),
 Q('Qui utilise la plus grande quantité de liquide ?','Appliquer chaque fraction à sa propre quantité de référence.', [('Calculer pour Alice',math(r'80\div8\times3=10\times3=30')),('Calculer pour Bilal',math(r'72\div12\times5=6\times5=30'))],r'Ils utilisent la même quantité : 30 cL chacun.'),
 Q('Pourquoi les réponses des questions 1 et 2 ne se contredisent-elles pas ? Que se passerait-il avec deux bouteilles de 80 cL ?','Distinguer comparaison de fractions et comparaison de quantités.', [('Identifier la différence d’unités',r'Les fractions de départ ne portent pas sur la même quantité : 80 cL et 72 cL.'),('Comparer avec une unité commune',r'Avec deux bouteilles de 80 cL, la plus grande fraction donnerait aussi la plus grande quantité. Bilal utiliserait $\frac{100}{3}$ cL, donc plus que 30 cL.')],r'Les unités initiales étaient différentes. Avec deux bouteilles de 80 cL, Bilal utiliserait plus de liquide.')
],r'Comparer des fractions ne suffit à comparer les quantités correspondantes que lorsque les unités de référence sont identiques.', [('3/8 < 5/12','True'),('80*3/8','30'),('72*5/12','30'),('80*5/12','100/3')])

def block(eid,d):
    parts=['=== '+d['titre'],f'Id: {eid}','Difficulté: '+d['difficulte'],'','Énoncé:',MARK,d['introduction'].replace(r'\n\n','\n\n')]
    parts += ['', '\n'.join(f'{i}. '+q['question'] for i,q in enumerate(d['questions'],1)), '', 'Étapes:', MARK]
    for i,q in enumerate(d['questions'],1):
        parts += ['',f'## Question {i} : '+q['question'],'','::: methode',q['methode'],':::']
        for title,body in q['etapes']:
            parts += ['', '::: etape '+title, body.replace(r'\n\n','\n\n').replace(r'\n|','\n|'), ':::']
        parts += ['', '::: resultat', q['reponse'], ':::']
    parts += ['', '::: attention',d['note'],':::','','Solution:',MARK]
    parts += [f'{i}. '+q['reponse'] for i,q in enumerate(d['questions'],1)]
    return '\n'.join(parts)

TITRES_ETAPES={
261:['Réunir les quantités','Multiplier les besoins','Évaluer le prix des carnets','Ajouter les frais globaux','Calculer le reste du budget','Comparer les livraisons comptées'],
262:['Repérer les multiples ou les critères','Former le quotient et le reste','Organiser toutes les possibilités','Choisir parmi les possibilités','Calculer la quantité demandée','Vérifier les contraintes'],
263:['Identifier les signes','Comparer les abscisses','Mesurer la distance à zéro','Déterminer l’opposé','Mesurer la distance entre les points','Comparer toutes les distances'],
264:['Coder la hausse','Calculer la température de midi','Coder la baisse','Calculer la température finale','Évaluer la variation totale','Déterminer la variation de retour'],
265:['Identifier l’unité et les parts','Écrire une fraction égale','Calculer une part','Calculer la portion demandée','Déterminer la quantité restante','Comparer à la moitié'],
}

def apply_revision():
    for n in range(261,266):
        p=next(BASE.glob(f'{n}_*')); exfile=p/'exercices.txt'
        old=exfile.read_text(encoding='utf8')
        blocks=[b.strip() for b in re.split(r'^===[ \t]*$',old,flags=re.M) if re.search(r'^Id:',b,re.M)]
        corrfile=p/'figures/correspondance.json'; corr=json.loads(corrfile.read_text(encoding='utf8'))
        coverage=[]; new=[]
        for ordinal,b in enumerate(blocks,1):
            eid=int(re.search(r'^Id:\s*(\d+)',b,re.M)[1])
            if eid in EX:
                d=EX[eid]; new.append(block(eid,d)); coverage.append({'id':eid,'titre':d['titre'],'difficulte':d['difficulte'],'remplacement':True})
                corr['exercices'].pop(str(eid),None)
            else:
                # Les anciens problèmes à données seules changées sont des entraînements.
                title=b.splitlines()[0]
                if 'Difficulté: hard' in b:
                    b=b.replace('Difficulté: hard','Difficulté: medium',1)
                    title=title.replace('=== Problème -','=== Entraînement -',1)
                title=re.sub(r' - \d+\. ',f' - {ordinal}. ',title,count=1)
                b=title+'\n'+'\n'.join(b.splitlines()[1:])
                current=0
                lines=[]
                for line in b.splitlines():
                    m=re.match(r'## Question (\d+)',line)
                    if m: current=int(m[1])
                    if line=='::: etape Raisonner et calculer': line='::: etape '+TITRES_ETAPES[n][current-1]
                    lines.append(line)
                b='\n'.join(lines)
                b=re.sub(r'(\d+) objet\(s\)',lambda m:m[1]+(' objet' if m[1]=='1' else ' objets'),b)
                b=re.sub(r'(\d+) période\(s\) du premier ; (\d+) du second',lambda m:m[1]+(' période' if m[1]=='1' else ' périodes')+' du premier ; '+m[2]+(' période' if m[2]=='1' else ' périodes')+' du second',b)
                new.append(b); coverage.append({'id':eid,'titre':title.replace('=== ','',1),'difficulte':re.search(r'Difficulté: (\w+)',b)[1],'remplacement':False})
        exfile.write_text('\n\n===\n\n'.join(new)+'\n',encoding='utf8')
        corrfile.write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        (p/'revision_20261030.json').write_text(json.dumps({'notion':n,'exercices':coverage,'remplacements':[eid for eid in EX if any(c['id']==eid for c in coverage)]},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(n,len(new),'blocs,',sum(c['remplacement'] for c in coverage),'remplacements',flush=True)

if __name__=='__main__': apply_revision()
