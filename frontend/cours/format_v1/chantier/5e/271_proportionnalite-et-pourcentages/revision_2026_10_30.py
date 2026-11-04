# -*- coding: utf-8 -*-
"""Révision pédagogique du lot 271–275 ; sauvegardes préalables obligatoires."""
from pathlib import Path
import re,json,math,importlib.util
BASE=Path(__file__).resolve().parent.parent
NEW={};TESTS={};FIGS={};MAPS={}
def Q(q,m,a,b,r):return (q,m,a.split('|',1),b.split('|',1),r)
def add(n,eid,title,level,intro,qs,checks,figure=None):
    NEW[eid]={'notion':n,'titre':title,'difficulte':level,'intro':intro,'questions':qs,'figure':figure}
    TESTS[eid]=checks
def box(k,t,title=''):return f'::: {k}'+(' '+title if title else '')+'\n'+t+'\n:::\n'
def aligned(*lines):return '$$\n\\begin{aligned}\n'+(' '+r'\\'+'\n').join(lines)+'\n\\end{aligned}\n$$'
def pic(s):return '\\begin{tikzpicture}\n'+s+'\n\\end{tikzpicture}'
def node(x,y,l,anchor='south',color='otInk'):
    return rf'\node[anchor={anchor},text={color},inner sep=4pt] at ({x},{y}) {{$ {l} $}};'+'\n'
def figure(n,name,tex):FIGS.setdefault(n,{})[name]=tex;return name

# 271 : chaque remplacement apporte une compétence différente.
add(271,2917,'Pourcentage d’un effectif', 'easy',r'Un club compte 40 adhérents, dont 14 pratiquent le basket.',[
Q(r'Quelle fraction des adhérents pratique le basket ?',r'Comparer la partie au total.',r'Choisir le total|La référence est l’ensemble des 40 adhérents ; la partie comporte 14 personnes.',r'Écrire la proportion|La proportion est $\frac{14}{40}=\frac7{20}$.',r'$\frac7{20}$.'),
Q(r'Exprimer cette proportion en pourcentage.',r'Écrire une fraction de dénominateur 100.',r'Multiplier les deux termes|$\frac7{20}=\frac{7\times5}{20\times5}=\frac{35}{100}$.',r'Interpréter|35 personnes sur 100 représentent la même proportion que 14 sur 40.',r'$35\,\%$.'),
Q(r'Calculer le nombre d’adhérents qui ne pratiquent pas le basket, puis leur pourcentage.',r'Calculer le complément.',r'Compter les autres|$40-14=26$ adhérents.',r'Compléter à 100 %|$100\,\%-35\,\%=65\,\%$. On vérifie $40\times\frac{65}{100}=26$.',r'26 adhérents, soit $65\,\%$.')],[r'14/40==7/20==35/100',r'40-14==26 and 40*65/100==26'])
add(271,2920,r'Un tableau trompeur',r'easy',r'Voici le tarif d’une livraison.\n\n| Masse (kg) | 1 | 2 | 3 |\n|---|---|---|---|\n| Prix (€) | 5 | 8 | 11 |',[
Q(r'Le prix est-il proportionnel à la masse ?',r'Comparer deux quotients.',r'Calculer les prix par kilogramme|$5\div1=5$ et $8\div2=4$.',r'Conclure sur le coefficient|Les quotients sont différents : aucun même nombre ne multiplie toutes les masses pour donner les prix.',r'Non, ce n’est pas une proportionnalité.'),
Q(r'Expliquer ce tableau avec un forfait de départ et un prix par kilogramme.',r'Observer l’augmentation du prix.',r'Repérer la part variable|Quand la masse augmente de 1 kg, le prix augmente de 3 €.',r'Retrouver la part fixe|Pour 1 kg, $5-3=2$ €. La règle est « 2 € de forfait, puis 3 € par kilogramme ».',r'Forfait de 2 €, puis 3 €/kg.'),
Q(r'Avec cette règle, calculer le prix de 5 kg.',r'Appliquer le tarif complet.',r'Calculer la part variable|$5\times3=15$ €.',r'Ajouter une seule fois le forfait|$15+2=17$ €. Le forfait ne se répète pas pour chaque kilogramme.',r'17 €.')],[r'5/1!=8/2',r'[2+3*x for x in (1,2,3)]==[5,8,11]',r'2+3*5==17'])
add(271,2924,r'Lire une échelle de randonnée',r'medium',r'Une carte est à l’échelle $1:25\,000$. Un sentier mesure $6{,}4$ cm sur la carte.',[
Q(r'Calculer la longueur réelle du sentier en kilomètres.',r'Passer d’abord aux centimètres réels.',r'Utiliser l’échelle|$6{,}4\times25\,000=160\,000$ cm.',r'Convertir|$160\,000\div100=1\,600$ m, puis $1\,600\div1\,000=1{,}6$ km.',r'$1{,}6$ km.'),
Q(r'Quelle longueur représente sur cette carte un trajet de 3 km ?',r'Mettre les longueurs dans la même unité, puis diviser.',r'Convertir le trajet réel|$3$ km $=300\,000$ cm.',r'Passer au dessin|$300\,000\div25\,000=12$ cm.',r'12 cm.'),
Q(r'La carte est agrandie en doublant toutes ses longueurs. Quelle est sa nouvelle échelle ?',r'Comparer une même longueur réelle aux deux dessins.',r'Examiner 1 cm du premier dessin|Il représente 25 000 cm réels et devient 2 cm sur l’agrandissement.',r'Revenir à 1 cm du nouveau dessin|$25\,000\div2=12\,500$ cm réels par centimètre dessiné.',r'$1:12\,500$.')],[r'6.4*25000/100000==1.6',r'300000/25000==12',r'25000/2==12500'])
add(271,2927,r'Augmenter puis réduire un prix',r'medium',r'Un abonnement coûte 50 €. Son prix augmente de $12\,\%$. Un bon de réduction de 6 € est ensuite appliqué.',[
Q(r'Calculer le montant de l’augmentation, puis le nouveau prix.',r'Calculer la part de 50 € correspondant à 12 %.',r'Calculer l’augmentation|$50\times\frac{12}{100}=6$ €.',r'Ajouter au prix initial|$50+6=56$ €.',r'Augmentation : 6 € ; nouveau prix : 56 €.'),
Q(r'Quel prix paie-t-on avec le bon ?',r'Distinguer une réduction en euros d’un taux.',r'Appliquer le bon au prix augmenté|Le bon retire 6 € du prix de 56 €.',r'Calculer|$56-6=50$ €.',r'50 €.'),
Q(r'Le bon de 6 € représente-t-il une réduction de 12 % du prix de 56 € ?',r'Vérifier le montant correspondant au taux annoncé.',r'Calculer 12 % du nouveau prix|$56\times\frac{12}{100}=6{,}72$ €.',r'Comparer les deux montants|$6\ne6{,}72$ : la référence a changé, donc le même montant ne représente plus le même pourcentage.',r'Non : $12\,\%$ de 56 € valent $6{,}72$ €.')],[r'50*12/100==6 and 50+6==56',r'56-6==50',r'56*12/100==6.72'])
add(271,2931,r'Représenter le prix des pommes',r'medium',r'Les pommes coûtent 3 € par kilogramme. On choisit la masse en abscisse et le prix en ordonnée.',[
Q(r'Compléter les prix de 0 kg, 1 kg, 2 kg et 3 kg.',r'Multiplier chaque masse par 3.',r'Utiliser le prix unitaire|Le coefficient de la masse vers le prix est 3.',r'Calculer les quatre valeurs|$0\times3=0$, $1\times3=3$, $2\times3=6$, $3\times3=9$ €.',r'0 €, 3 €, 6 € et 9 €.'),
Q(r'Placer les quatre points dans un repère et expliquer leur alignement.',r'Utiliser les couples (masse ; prix).',r'Écrire les coordonnées|$O(0\,;0)$, $A(1\,;3)$, $B(2\,;6)$, $C(3\,;9)$.',r'Interpréter le graphique|Le prix est proportionnel à la masse : les points sont alignés sur une droite passant par l’origine. Des masses intermédiaires ont ici un sens.',r'Les quatre points sont alignés avec l’origine.'),
Q(r'Lire puis calculer le prix de 2,5 kg.',r'Comparer la lecture graphique au calcul exact.',r'Lire la droite|À l’abscisse $2{,}5$, on lit l’ordonnée $7{,}5$.',r'Contrôler le prix|$2{,}5\times3=7{,}5$ €.',r'$7{,}50$ €.')],[r'[3*x for x in (0,1,2,3)]==[0,3,6,9]',r'2.5*3==7.5'], r'pommes')
add(271,2934,r'Choisir le meilleur lot',r'hard',r'Un magasin vend des lots de 3 cahiers à $4{,}50$ €. Un autre vend des lots de 5 cahiers à 7 €. On doit acheter exactement 30 cahiers ; les cahiers d’un même magasin sont identiques.',[
Q(r'Comparer les prix unitaires dans les deux magasins.',r'Revenir au prix d’un cahier.',r'Premier magasin|$4{,}50\div3=1{,}50$ € par cahier.',r'Second magasin|$7\div5=1{,}40$ € par cahier.',r'$1{,}50$ € et $1{,}40$ € par cahier.'),
Q(r'Calculer la dépense pour 30 cahiers dans chaque magasin.',r'Compter les lots entiers puis calculer le prix.',r'Premier achat|$30\div3=10$ lots, puis $10\times4{,}50=45$ €.',r'Second achat|$30\div5=6$ lots, puis $6\times7=42$ €.',r'45 € au premier ; 42 € au second.'),
Q(r'Le premier magasin propose 10 % de remise sur cet achat. Quel magasin devient le moins cher ?',r'Appliquer la remise au total, puis comparer.',r'Calculer la remise|$45\times\frac{10}{100}=4{,}50$ €, donc $45-4{,}50=40{,}50$ €.',r'Comparer après réduction|$40{,}50<42$ : le premier magasin est moins cher de $42-40{,}50=1{,}50$ €.',r'Le premier : $40{,}50$ €, économie de $1{,}50$ €.')],[r'4.5/3==1.5 and 7/5==1.4',r'30/3*4.5==45 and 30/5*7==42',r'45*(1-10/100)==40.5 and 42-40.5==1.5'])
add(271,2935,r'Une recette et un budget à respecter',r'hard',r'Pour 8 personnes, une recette demande 600 g de fruits. On prépare 20 parts. Les fruits coûtent $4{,}80$ € par kilogramme et sont vendus par sachets de 500 g.',[
Q(r'Calculer la masse de fruits nécessaire pour 20 parts.',r'Revenir à la masse d’une part.',r'Calculer une part|$600\div8=75$ g.',r'Adapter la recette|$20\times75=1\,500$ g, soit $1{,}5$ kg.',r'$1\,500$ g, soit $1{,}5$ kg.'),
Q(r'Combien de sachets acheter et combien coûtent-ils au total ?',r'Comparer la masse nécessaire au contenu d’un sachet.',r'Compter les sachets|$1\,500\div500=3$ sachets.',r'Calculer le prix|$1{,}5\times4{,}80=7{,}20$ €.',r'3 sachets pour $7{,}20$ €.'),
Q(r'Pour une autre préparation, seuls 80 % des 20 invités mangent une part. Peut-on acheter seulement deux sachets ?',r'Calculer l’effectif puis la masse nécessaire avant de décider.',r'Déterminer le besoin|$20\times\frac{80}{100}=16$ parts, puis $16\times75=1\,200$ g.',r'Tenir compte des sachets entiers|Deux sachets donnent $2\times500=1\,000$ g, insuffisants. Il faut toujours 3 sachets, avec $1\,500-1\,200=300$ g restants.',r'Non : 3 sachets sont nécessaires ; il reste 300 g.')],[r'600/8*20==1500 and 1500/500==3',r'math.isclose(1.5*4.8,7.2)',r'20*80/100*75==1200 and 1200>2*500 and 1500-1200==300'])

# 272 : coordonnées, pas des axes, lectures directes et inverses, dépendance non proportionnelle.
add(272,2938,r'Placer des points sur les axes',r'easy',r'Dans un repère orthogonal, on considère $A(-3\,;2)$, $B(0\,;-2)$ et $C(4\,;0)$.',[
Q(r'Placer les trois points.',r'Lire l’abscisse avant l’ordonnée.',r'Repérer horizontalement|Pour $A$, partir vers la gauche jusqu’à $-3$ ; pour $C$, aller à droite jusqu’à 4.',r'Compléter verticalement|$A$ est à l’ordonnée 2 ; $B$ est sur l’axe vertical à $-2$ ; $C$ est sur l’axe horizontal.',r'$A(-3\,;2)$, $B(0\,;-2)$, $C(4\,;0)$ placés.'),
Q(r'Quels points appartiennent à un axe ?',r'Chercher la coordonnée nulle.',r'Axe vertical|$B$ a une abscisse nulle.',r'Axe horizontal|$C$ a une ordonnée nulle ; aucune coordonnée de $A$ n’est nulle.',r'B est sur l’axe vertical ; C est sur l’axe horizontal.'),
Q(r'Placer D pour que A et D soient sur une même horizontale et C et D sur une même verticale.',r'Croiser une abscisse et une ordonnée connues.',r'Choisir l’abscisse|Même verticale que $C$ : $x_D=4$.',r'Choisir l’ordonnée|Même horizontale que $A$ : $y_D=2$.',r'$D(4\,;2)$.')],[r'(4,2)[0]==4 and (4,2)[1]==2'], r'points_axes')
add(272,2940,r'Lire des graduations différentes',r'easy',r'Le graphique donne la hauteur d’eau dans une cuve. Les graduations horizontales sont espacées de 2 minutes ; les verticales de 5 litres. La cuve se remplit régulièrement.\n\n[IMAGE_1]',[
Q(r'Lire la quantité d’eau après 4 minutes.',r'Lire d’abord l’unité et le pas de chaque axe.',r'Repérer le temps|4 minutes se trouvent à la deuxième graduation après 0.',r'Lire la hauteur du point|Le point de la droite à cette abscisse a pour ordonnée 10 litres.',r'10 L.'),
Q(r'À quel instant la cuve contient-elle 15 litres ?',r'Effectuer une lecture inverse.',r'Partir de l’ordonnée|Repérer 15 L, puis rejoindre la droite horizontalement.',r'Revenir à l’axe des temps|On lit l’abscisse 6 minutes.',r'À 6 min.'),
Q(r'Exprimer par une phrase la régularité du remplissage.',r'Comparer deux augmentations correspondantes.',r'Lire une variation|En 2 minutes, la quantité augmente de 5 L.',r'Vérifier sur un autre intervalle|Entre 4 et 6 minutes, elle passe de 10 à 15 L : encore 5 L en 2 minutes.',r'La quantité augmente de 5 L toutes les 2 min.')],[r'(10/4)==(15/6)==2.5'], r'cuve')
add(272,2944,r'Un périmètre dépend d’une longueur',r'medium',r'Un rectangle a une largeur fixe de 3 cm et une longueur $L$, en centimètres, supérieure ou égale à 3.',[
Q(r'Exprimer son périmètre P en fonction de L.',r'Additionner les quatre côtés.',r'Repérer les paires de côtés|Le rectangle possède deux côtés de longueur $L$ et deux de longueur 3.',r'Regrouper|$P=L+3+L+3=2L+6$.',r'$P=2L+6$ (en cm).'),
Q(r'Compléter le tableau pour L = 3, 4 et 6 cm.',r'Remplacer la lettre par chaque valeur.',r'Calculer les deux premières valeurs|$2\times3+6=12$ et $2\times4+6=14$ cm.',r'Calculer la dernière|$2\times6+6=18$ cm.',r'12 cm, 14 cm et 18 cm.'),
Q(r'Le périmètre est-il proportionnel à L ? Quelle longueur donne un périmètre de 20 cm ?',r'Séparer la vérification du modèle et la recherche d’une donnée.',r'Comparer les quotients|$12\div3=4$ tandis que $14\div4=3{,}5$ : pas de proportionnalité.',r'Retrouver la longueur|Enlever les 6 cm des deux largeurs : $20-6=14$ ; les deux longueurs valent donc $14\div2=7$ cm.',r'Non ; $L=7$ cm.')],[r'[2*x+6 for x in (3,4,6)]==[12,14,18]',r'12/3!=14/4',r'(20-6)/2==7'])
add(272,2946,r'Une aire n’est pas un périmètre',r'medium',r'On fabrique des carrés de côté $c$ cm, avec $c=1$, 2, 3 ou 4.',[
Q(r'Donner une formule de l’aire A en fonction de c et calculer les quatre aires.',r'Multiplier le côté par lui-même.',r'Écrire la formule|$A=c\times c=c^2$, en cm$^2$.',r'Remplacer c|Pour les côtés 1, 2, 3 et 4 cm, on obtient 1, 4, 9 et 16 cm$^2$.',r'$A=c^2$ ; 1, 4, 9 et 16 cm$^2$.'),
Q(r'Quand le côté double de 2 à 4 cm, l’aire double-t-elle ?',r'Comparer les deux aires.',r'Calculer le changement|L’aire passe de $2\times2=4$ à $4\times4=16$ cm$^2$.',r'Comparer au double|$16\div4=4$ : l’aire est multipliée par 4, et non par 2.',r'Non : l’aire est multipliée par 4.'),
Q(r'Placer les quatre points (c ; A). Sont-ils alignés avec l’origine ?',r'Comparer la représentation à une proportionnalité.',r'Écrire les couples|$(1\,;1)$, $(2\,;4)$, $(3\,;9)$ et $(4\,;16)$.',r'Contrôler l’alignement avec O|Les quotients $A/c$ valent 1, 2, 3 et 4. Ils ne sont pas égaux ; les points ne sont pas alignés avec l’origine.',r'Non ; les points sont placés sur la figure corrigée.')],[r'[x*x for x in (1,2,3,4)]==[1,4,9,16]',r'16/4==4'], r'aires_carres')
add(272,2949,r'Une promenade avec une pause',r'medium',r'Le graphique indique la distance totale parcourue depuis le départ pendant une promenade. Les segments entre les points décrivent le déplacement.\n\n[IMAGE_1]',[
Q(r'Lire la distance parcourue au bout de 20 min.',r'Lire la hauteur du point d’abscisse 20.',r'Repérer 20 min|Suivre la verticale d’abscisse 20 jusqu’au graphique.',r'Lire l’ordonnée|Le point est à 1 km du départ.',r'1 km.'),
Q(r'Sur quel intervalle de temps la personne fait-elle une pause ?',r'Chercher un segment horizontal.',r'Observer la distance|Entre 20 et 30 min, la distance totale reste égale à 1 km.',r'Interpréter|Une distance totale qui ne change pas signifie qu’aucune nouvelle distance n’est parcourue.',r'Entre 20 et 30 min.'),
Q(r'Calculer la distance parcourue entre 30 et 50 min et comparer aux 20 premières minutes.',r'Calculer la différence de deux distances cumulées.',r'Après la pause|$2{,}5-1=1{,}5$ km en 20 min.',r'Comparer|Au début, 1 km a été parcouru en 20 min. La personne parcourt ensuite 0,5 km de plus pendant une même durée.',r'$1{,}5$ km ; allure plus rapide après la pause.')],[r'2.5-1==1.5 and 1.5>1'], r'promenade')
add(272,2954,r'Comparer deux tarifs sur un graphique',r'hard',r'Pour $n$ activités, le tarif A est $P_A=3n$ euros et le tarif B est $P_B=2n+4$ euros. Seuls les nombres entiers d’activités de 0 à 6 sont autorisés.',[
Q(r'Calculer les deux prix pour 2, 4 et 6 activités.',r'Remplacer n dans chacune des deux formules.',r'Tarif A|$3\times2=6$, $3\times4=12$, $3\times6=18$ €.',r'Tarif B|$2\times2+4=8$, $2\times4+4=12$, $2\times6+4=16$ €.',r'A : 6, 12, 18 € ; B : 8, 12, 16 €.'),
Q(r'Représenter les deux séries de points et déterminer quand les tarifs sont égaux.',r'Placer (nombre d’activités ; prix) pour chaque offre.',r'Choisir les axes|Le nombre d’activités est en abscisse ; le prix, en ordonnée. On garde les points séparés.',r'Repérer la rencontre|Les deux séries contiennent le point $(4\,;12)$ : les tarifs sont égaux pour 4 activités.',r'4 activités pour 12 €.'),
Q(r'Quelle offre choisir pour chacun des nombres entiers de 0 à 6 ?',r'Comparer les prix à nombre d’activités égal.',r'Avant la rencontre|Pour $n=0,1,2,3$, A coûte respectivement 0, 3, 6, 9 €, contre 4, 6, 8, 10 € pour B.',r'Après la rencontre|Pour 5 et 6 activités, B coûte 14 et 16 €, contre 15 et 18 € pour A.',r'A de 0 à 3 ; égalité à 4 ; B pour 5 ou 6.')],[r'[3*n for n in (2,4,6)]==[6,12,18]',r'[2*n+4 for n in (2,4,6)]==[8,12,16]',r'[n for n in range(7) if 3*n==2*n+4]==[4]'], r'tarifs')
add(272,2956,r'Retrouver une donnée avec un budget',r'hard',r'Une visite coûte 7 € d’entrée puis $2{,}50$ € par atelier. Lina dispose de 23 €. Un atelier ne peut pas être acheté partiellement.',[
Q(r'Exprimer le prix total P de n ateliers.',r'Séparer le forfait et la part qui dépend de n.',r'Coût variable|$n$ ateliers coûtent $2{,}5n$ euros.',r'Coût total|Ajouter l’entrée une seule fois : $P=7+2{,}5n$.',r'$P=7+2{,}5n$.'),
Q(r'Calculer les prix pour 6 et 7 ateliers.',r'Vérifier les deux nombres entiers voisins du budget.',r'Six ateliers|$7+2{,}5\times6=7+15=22$ €.',r'Sept ateliers|$7+2{,}5\times7=7+17{,}5=24{,}5$ €.',r'22 € et $24{,}50$ €.'),
Q(r'Quel est le nombre maximal d’ateliers et combien reste-t-il ?',r'Tenir compte du caractère entier du nombre d’ateliers.',r'Comparer au budget|$22\le23$ mais $24{,}5>23$ ; 7 ateliers sont impossibles.',r'Calculer le reste|Avec 6 ateliers, $23-22=1$ €. On ne peut pas convertir ce reste en une fraction d’atelier.',r'6 ateliers ; reste : 1 €.')],[r'7+2.5*6==22 and 7+2.5*7==24.5',r'22<=23<24.5 and 23-22==1'])

# 273 : vocabulaire, contre-exemple, utilisation directe et réciproque.
add(273,2959,r'Partager un angle droit',r'easy',r'Les demi-droites $[OA)$ et $[OB)$ forment un angle droit. Une demi-droite $[OC)$ est à l’intérieur de cet angle et $\widehat{AOC}=34^\circ$.',[
Q(r'Calculer l’angle COB.',r'Partager la mesure d’un angle droit.',r'Repérer les angles adjacents|$\widehat{AOC}+\widehat{COB}=\widehat{AOB}=90^\circ$.',r'Soustraire l’angle connu|$\widehat{COB}=90^\circ-34^\circ=56^\circ$.',r'$56^\circ$.'),
Q(r'On trace la bissectrice OD de COB. Calculer COD et DOB.',r'Partager la mesure en deux parts égales.',r'Utiliser la définition|La bissectrice impose $\widehat{COD}=\widehat{DOB}$.',r'Calculer la moitié|$56^\circ\div2=28^\circ$.',r'$28^\circ$ chacun.'),
Q(r'Calculer AOD.',r'Additionner deux angles adjacents dans la bonne configuration.',r'Repérer la décomposition|$\widehat{AOD}=\widehat{AOC}+\widehat{COD}$.',r'Additionner|$34^\circ+28^\circ=62^\circ$.',r'$62^\circ$.')],[r'90-34==56 and 56/2==28 and 34+28==62'],r'angle_droit')
add(273,2961,r'Prouver que deux droites sont parallèles',r'medium',r'Une sécante coupe $(d)$ et $(e)$ en $A$ et $B$. Les angles marqués sur la figure sont alternes internes et mesurent chacun $58^\circ$. Le parallélisme n’est pas donné.\n\n[IMAGE_1]',[
Q(r'Pourquoi la paire marquée est-elle alterne-interne ?',r'Vérifier les trois critères de position.',r'Repérer les sommets|Les deux angles ont des sommets différents : $A$ et $B$.',r'Repérer les positions|Ils sont entre les droites $(d)$ et $(e)$ et de part et d’autre de la sécante.',r'Sommets différents, intérieurs, côtés opposés de la sécante.'),
Q(r'Démontrer le parallélisme de d et e.',r'Utiliser la réciproque de la propriété des angles alternes internes.',r'Énoncer l’égalité connue|Les deux angles alternes internes mesurent $58^\circ$ : ils sont égaux.',r'Appliquer la réciproque|Si deux angles alternes internes sont égaux, alors les deux droites coupées par la sécante sont parallèles.',r'$(d)\parallel(e)$.'),
Q(r'Calculer l’angle adjacent à l’angle de 58° en A, situé au-dessous de d et de l’autre côté de la sécante.',r'Reconnaître deux angles formant un angle plat.',r'Repérer le supplément|Ces deux angles adjacents ont pour somme $180^\circ$.',r'Calculer|$180^\circ-58^\circ=122^\circ$.',r'$122^\circ$.')],[r'58==58 and 180-58==122'],r'reciproque')
add(273,2965,r'Deux perpendiculaires à une même droite',r'medium',r'Les droites $(d)$ et $(e)$ sont perpendiculaires à une droite $(s)$. Une autre sécante $(t)$ forme avec $(d)$ l’angle aigu de $37^\circ$ marqué sur la figure.\n\n[IMAGE_1]',[
Q(r'Justifier que d et e sont parallèles.',r'Utiliser la propriété des perpendiculaires communes.',r'Lire les deux hypothèses|$(d)\perp(s)$ et $(e)\perp(s)$.',r'Citer la propriété|Deux droites perpendiculaires à une même droite sont parallèles.',r'$(d)\parallel(e)$.'),
Q(r'Calculer l’angle correspondant marqué en B.',r'Réinvestir le parallélisme démontré.',r'Identifier la paire|Les deux angles sont correspondants pour la sécante $(t)$.',r'Conclure|Les droites étant parallèles, ces angles sont égaux.',r'$37^\circ$.'),
Q(r'Calculer l’angle obtus adjacent à cet angle en B.',r'Compléter à 180 degrés.',r'Repérer l’angle plat|Les deux angles adjacents forment une demi-rotation.',r'Soustraire|$180^\circ-37^\circ=143^\circ$.',r'$143^\circ$.')],[r'180-37==143'],r'perpendiculaires')
add(273,2967,r'Ne pas confondre égalité et parallélisme',r'medium',r'Deux droites $(d)$ et $(e)$ sont coupées par une sécante. Une paire d’angles correspondants mesure $64^\circ$ et $67^\circ$.',[
Q(r'Les droites peuvent-elles être parallèles ?',r'Comparer les mesures qu’imposerait un parallélisme.',r'Supposer un parallélisme|Des angles correspondants devraient alors avoir la même mesure.',r'Comparer aux données|$64^\circ\ne67^\circ$ ; cette condition nécessaire n’est pas satisfaite.',r'Non : les angles correspondants ne sont pas égaux.'),
Q(r'Quelle mesure pourrait-on donner au second angle pour prouver le parallélisme ?',r'Utiliser la réciproque avec des angles correspondants.',r'Choisir une mesure égale|Le second angle doit mesurer $64^\circ$.',r'Justifier le choix|Deux angles correspondants égaux permettraient de conclure au parallélisme.',r'$64^\circ$.'),
Q(r'Si seuls deux angles opposés par le sommet en une même intersection étaient égaux, cela prouverait-il le parallélisme ?',r'Distinguer une propriété locale d’une relation entre les deux intersections.',r'Rappeler la propriété|Deux angles opposés par le sommet sont toujours égaux, quelles que soient les autres droites.',r'Conclure|Cette égalité ne donne aucune information sur l’autre intersection.',r'Non : il faut une information reliant les deux intersections.')],[r'64!=67'])
add(273,2971,r'Une droite parallèle à la base d’un triangle',r'hard',r'Dans le triangle $ABC$, $\widehat{ABC}=48^\circ$ et $\widehat{ACB}=67^\circ$. Par $A$, on trace la parallèle $(d)$ à $(BC)$. Les points $D$, $A$, $E$ sont dans cet ordre sur $(d)$, avec D du côté de B.\n\n[IMAGE_1]',[
Q(r'Justifier la mesure de DAB.',r'Repérer des angles alternes internes.',r'Choisir la sécante|La droite $(AB)$ coupe les parallèles $(d)$ et $(BC)$.',r'Utiliser l’égalité|Les angles $\widehat{DAB}$ et $\widehat{ABC}$ sont alternes internes, donc égaux.',r'$48^\circ$.'),
Q(r'Justifier la mesure de CAE.',r'Utiliser l’autre côté du triangle comme sécante.',r'Identifier la configuration|La droite $(AC)$ coupe les mêmes parallèles.',r'Reporter l’angle|Les angles $\widehat{CAE}$ et $\widehat{ACB}$ sont alternes internes.',r'$67^\circ$.'),
Q(r'Calculer BAC en utilisant l’angle plat DAE.',r'Retrancher les deux angles reportés.',r'Décomposer l’angle plat|$\widehat{DAB}+\widehat{BAC}+\widehat{CAE}=180^\circ$.',r'Calculer|$\widehat{BAC}=180^\circ-48^\circ-67^\circ=65^\circ$.',r'$65^\circ$.')],[r'180-48-67==65'],r'triangle_parallele')
add(273,2974,r'Une somme d’angles qui prouve un parallélisme',r'hard',r'Une sécante coupe $(d)$ en $A$ et $(e)$ en $B$. Les deux angles intérieurs du même côté de la sécante, marqués sur la figure, mesurent $112^\circ$ en A et $68^\circ$ en B.\n\n[IMAGE_1]',[
Q(r'Calculer en A l’autre angle intérieur adjacent à celui de 112°.',r'Former un angle plat en A.',r'Repérer la somme|Les deux angles intérieurs en $A$ sont adjacents et supplémentaires.',r'Soustraire|$180^\circ-112^\circ=68^\circ$.',r'$68^\circ$.'),
Q(r'Comparer cet angle à l’angle donné en B et conclure.',r'Faire apparaître une paire d’angles alternes internes égaux.',r'Comparer les mesures|L’angle obtenu en $A$ et celui de $B$ valent tous deux $68^\circ$.',r'Appliquer la réciproque|Ils sont alternes internes : leur égalité prouve que $(d)$ et $(e)$ sont parallèles.',r'$(d)\parallel(e)$.'),
Q(r'Peut-on utiliser la même conclusion si l’angle en B vaut 70° au lieu de 68° ?',r'Vérifier ce qu’impliquerait le parallélisme.',r'Comparer les angles nécessaires|L’angle en $A$ resterait $68^\circ$, différent de $70^\circ$.',r'Conclure|Si les droites étaient parallèles, les angles alternes internes seraient égaux. Elles ne pourraient donc pas être parallèles.',r'Non ; avec 70°, les droites ne sont pas parallèles.')],[r'180-112==68 and 112+68==180',r'68!=70'],r'somme_paralleles')
add(273,2977,r'Construire une bissectrice au compas',r'medium',r'Tracer un angle $\widehat{AOB}=70^\circ$, puis construire sa bissectrice au compas. La figure corrigée montre un modèle réduit ; les arcs de construction sont à conserver.',[
Q(r'Décrire la première étape au compas.',r'Placer deux points à même distance du sommet.',r'Tracer un premier arc|Avec le centre $O$, tracer un arc qui coupe $[OA)$ en $M$ et $[OB)$ en $N$.',r'Identifier les longueurs égales|Le même rayon a servi : $OM=ON$.',r'Un arc de centre O donne M et N avec OM = ON.'),
Q(r'Comment obtenir un point P de la bissectrice, différent de O ?',r'Construire un point à égale distance de M et N.',r'Tracer deux arcs|Avec le même rayon, tracer un arc de centre $M$ puis un arc de centre $N$, qui se coupent à l’intérieur de l’angle.',r'Tracer la demi-droite|Appeler $P$ leur intersection intérieure puis tracer $[OP)$. Les triangles $OMP$ et $ONP$ se superposent : les angles en $O$ sont égaux.',r'La demi-droite [OP) est la bissectrice.'),
Q(r'Calculer les deux angles obtenus et indiquer un contrôle au rapporteur.',r'Partager 70 degrés en deux mesures égales.',r'Calculer|$70^\circ\div2=35^\circ$.',r'Contrôler|Au rapporteur, vérifier $\widehat{AOP}=\widehat{POB}=35^\circ$ sans remplacer la construction au compas par une simple mesure.',r'$35^\circ$ chacun.')],[r'70/2==35'],r'bissectrice')

# 274 : nouvelles constructions et raisonnements avec des données réellement différentes.
add(274,2980,r'Trois longueurs : possible, aplati ou impossible',r'easy',r'On propose trois triplets de longueurs, en centimètres : (3 ; 4 ; 5), (2 ; 3 ; 5) et (2 ; 3 ; 6).',[
Q(r'Quels triplets permettent un triangle non aplati ?',r'Comparer le plus grand côté à la somme des deux autres.',r'Premier triplet|$5<3+4=7$ : un triangle non aplati est possible.',r'Deux autres triplets|$5=2+3$ donne des points alignés ; $6>2+3$ ne permet pas de triangle.',r'Seul le triplet (3 ; 4 ; 5).'),
Q(r'Construire ABC avec AB = 5 cm, AC = 3 cm et BC = 4 cm.',r'Utiliser deux arcs de compas.',r'Tracer la base|Tracer $[AB]$ de 5 cm à la règle graduée.',r'Placer C|Tracer un arc de centre $A$, rayon 3 cm, et un arc de centre $B$, rayon 4 cm. Choisir une intersection et la relier à $A$ et $B$.',r'Triangle ABC construit avec les deux arcs conservés.'),
Q(r'Pourquoi les deux intersections possibles des arcs donnent-elles deux triangles de mêmes dimensions ?',r'Observer la symétrie par rapport à la base.',r'Comparer les distances|Chaque intersection est à 3 cm de $A$ et 4 cm de $B$.',r'Comparer les positions|Les deux intersections sont symétriques par rapport à $(AB)$. Les deux triangles se superposent par cette symétrie.',r'Ils sont symétriques par rapport à (AB).')],[r'5<3+4 and 5==2+3 and 6>2+3',r'math.dist((0,0),(1.8,2.4))==3 and math.dist((5,0),(1.8,2.4))==4'],r'trois_cotes')
add(274,2981,r'Deux côtés et l’angle compris',r'medium',r'Construire $ABC$ tel que $AB=5$ cm, $AC=4$ cm et $\widehat{BAC}=60^\circ$.',[
Q(r'Dans quel ordre effectuer la construction ?',r'Commencer par le côté et l’angle dont le sommet est connu.',r'Tracer le premier côté|Tracer $[AB]$ de 5 cm.',r'Construire l’angle|Au rapporteur, tracer une demi-droite issue de $A$ faisant $60^\circ$ avec $[AB)$.',r'Tracer AB, puis une demi-droite à 60° en A.'),
Q(r'Comment placer C et terminer le triangle ?',r'Reporter la seconde longueur sur la demi-droite.',r'Utiliser le compas|Avec le centre $A$ et le rayon 4 cm, couper la demi-droite au point $C$.',r'Fermer le triangle|Relier $C$ à $B$ ; contrôler $AB=5$ cm, $AC=4$ cm et l’angle de $60^\circ$.',r'C est à 4 cm de A sur la demi-droite ; relier B à C.'),
Q(r'Pourquoi faut-il préciser « angle compris entre les deux côtés donnés » ?',r'Identifier les côtés qui forment l’angle.',r'Lire les demi-droites|Les côtés $[AB]$ et $[AC]$ se rencontrent en $A$.',r'Éviter une autre construction|L’angle de $60^\circ$ doit donc être en $A$ : le placer en $B$ ne respecterait pas les données.',r'Le sommet de l’angle donné est $A$.')],[r'math.isclose(math.hypot(2,2*math.sqrt(3)),4)',r'math.isclose(math.degrees(math.atan2(2*math.sqrt(3),2)),60)'],r'deux_cotes_angle')
add(274,2984,r'Reconnaître puis exploiter un triangle isocèle',r'medium',r'Le triangle $ABC$ est isocèle en $A$ et $\widehat{BAC}=44^\circ$.',[
Q(r'Calculer les angles ABC et ACB.',r'Utiliser l’égalité des angles à la base puis la somme des angles.',r'Calculer la somme restante|$180^\circ-44^\circ=136^\circ$.',r'Partager également|$\widehat{ABC}=\widehat{ACB}=136^\circ\div2=68^\circ$.',r'$68^\circ$ chacun.'),
Q(r'M est le milieu de BC. Quelles droites remarquables sont portées par AM ?',r'Utiliser l’axe de symétrie d’un triangle isocèle.',r'Identifier la médiane|La droite $(AM)$ joint le sommet $A$ au milieu du côté opposé.',r'Utiliser la symétrie|Dans ce triangle isocèle, $(AM)$ est aussi perpendiculaire à $(BC)$ ; elle porte la hauteur et la médiatrice de la base.',r'Médiane, hauteur et médiatrice de [BC].'),
Q(r'Calculer BAM.',r'Utiliser le partage de l’angle au sommet par l’axe de symétrie.',r'Reconnaître la bissectrice|La symétrie échange $B$ et $C$ et conserve $(AM)$.',r'Diviser la mesure|$\widehat{BAM}=44^\circ\div2=22^\circ$.',r'$22^\circ$.')],[r'(180-44)/2==68 and 44/2==22'],r'isocele')
add(274,2987,r'Trouver un centre équidistant',r'medium',r'Un triangle a pour sommets $A(0\,;0)$, $B(6\,;0)$ et $C(2\,;4)$ dans un repère dont l’unité vaut 1 cm.',[
Q(r'Construire les médiatrices de AB et AC, puis leur intersection O.',r'Utiliser le milieu et la perpendicularité.',r'Construire la première|Le milieu de $[AB]$ est $(3\,;0)$ : sa médiatrice est la verticale passant par ce point.',r'Construire la seconde|Tracer la perpendiculaire à $(AC)$ par le milieu $(1\,;2)$ de $[AC]$. Elle rencontre la première en $O(3\,;1)$.',r'$O(3\,;1)$. Cette lecture se vérifie par les constructions.'),
Q(r'Pourquoi le cercle de centre O passant par A passe-t-il aussi par B et C ?',r'Exploiter deux appartenances à des médiatrices.',r'Première égalité|$O$ est sur la médiatrice de $[AB]$, donc $OA=OB$.',r'Seconde égalité|$O$ est sur la médiatrice de $[AC]$, donc $OA=OC$. Les trois distances sont égales.',r'O est le centre du cercle circonscrit.'),
Q(r'Un point X est seulement sur la médiatrice de AB. Peut-on affirmer que XA = XC ?',r'Distinguer les deux propriétés de médiatrice.',r'Ce qui est certain|L’appartenance à la première médiatrice donne uniquement $XA=XB$.',r'Ce qui manque|Pour conclure $XA=XC$, il faudrait aussi savoir que $X$ appartient à la médiatrice de $[AC]$.',r'Non : seule l’égalité XA = XB est garantie.')],[r'math.dist((3,1),(0,0))==math.dist((3,1),(6,0))==math.dist((3,1),(2,4))'],r'mediatrices')
add(274,2991,r'Une hauteur à l’extérieur du triangle',r'medium',r'On donne $B(0\,;0)$, $C(6\,;0)$ et $A(-2\,;3)$ dans un repère dont l’unité vaut 1 cm.',[
Q(r'Tracer la hauteur issue de A et nommer son pied H.',r'Tracer par A la perpendiculaire à la droite BC.',r'Repérer la droite du côté|$(BC)$ est horizontale ; sa perpendiculaire par $A$ est verticale.',r'Trouver le pied|La verticale d’abscisse $-2$ rencontre $(BC)$ en $H(-2\,;0)$, à l’extérieur du segment $[BC]$.',r'$H(-2\,;0)$. La hauteur est extérieure.'),
Q(r'Calculer l’aire du triangle ABC.',r'Choisir la base et sa hauteur correspondante.',r'Lire les longueurs|$BC=6$ cm et $AH=3$ cm.',r'Appliquer la formule|$\mathcal A=\frac{6\times3}{2}=9$ cm$^2$.',r'9 cm$^2$.'),
Q(r'Pourquoi ne doit-on pas prendre BH comme base du triangle ABC ?',r'Vérifier quels points sont les sommets du triangle étudié.',r'Identifier le bon côté|$[BC]$ est un côté du triangle $ABC$ ; $[BH]$ n’en est pas un.',r'Repérer l’erreur de calcul|$BH\times AH\div2$ calculerait l’aire du triangle $ABH$, et non celle de $ABC$.',r'La base choisie doit être BC, pas BH.')],[r'6*3/2==9',r'math.dist((-2,3),(-2,0))==3'],r'hauteur_exterieure')
add(274,2994,r'Une aire, deux unités et une hauteur inconnue',r'hard',r'Un triangle a une base de $0{,}8$ m et une hauteur correspondante de 35 cm.',[
Q(r'Calculer son aire en cm².',r'Convertir les longueurs avant de multiplier.',r'Exprimer la base en centimètres|$0{,}8$ m $=80$ cm.',r'Calculer|$\mathcal A=\frac{80\times35}{2}=1\,400$ cm$^2$.',r'$1\,400$ cm$^2$.'),
Q(r'Donner cette aire en m².',r'Utiliser une unité carrée ou refaire le calcul en mètres.',r'Convertir la hauteur|35 cm $=0{,}35$ m.',r'Calculer en mètres|$\mathcal A=\frac{0{,}8\times0{,}35}{2}=0{,}14$ m$^2$. Cela correspond à $1\,400\div10\,000$.',r'$0{,}14$ m$^2$.'),
Q(r'Un second triangle a la même aire et une base de 56 cm. Calculer sa hauteur correspondante.',r'Retrouver le produit base × hauteur.',r'Doubler l’aire|$b\times h=2\mathcal A=2\times1\,400=2\,800$ cm$^2$.',r'Diviser par la base|$h=2\,800\div56=50$ cm. Contrôle : $56\times50\div2=1\,400$.',r'50 cm.')],[r'80*35/2==1400',r'math.isclose(.8*.35/2,.14)',r'2*1400/56==50'])
add(274,2998,r'Un angle extérieur dans un triangle isocèle',r'hard',r'$ABC$ est isocèle en $A$. Les points $B$, $C$ et $D$ sont alignés dans cet ordre et $\widehat{ACD}=124^\circ$.\n\n[IMAGE_1]',[
Q(r'Calculer l’angle intérieur ACB.',r'Relier l’angle extérieur à son supplémentaire.',r'Utiliser l’alignement|Les demi-droites $[CB)$ et $[CD)$ sont opposées.',r'Soustraire à 180°|$\widehat{ACB}=180^\circ-124^\circ=56^\circ$.',r'$56^\circ$.'),
Q(r'Calculer ABC puis BAC.',r'Utiliser successivement le caractère isocèle et la somme des angles.',r'Angles à la base|$AB=AC$, donc $\widehat{ABC}=\widehat{ACB}=56^\circ$.',r'Angle au sommet|$\widehat{BAC}=180^\circ-56^\circ-56^\circ=68^\circ$.',r'$\widehat{ABC}=56^\circ$ ; $\widehat{BAC}=68^\circ$.'),
Q(r'Vérifier que l’angle extérieur ACD est la somme des deux angles intérieurs qui ne lui sont pas adjacents.',r'Comparer les mesures calculées.',r'Choisir les bons angles|Les angles intérieurs non adjacents à $\widehat{ACD}$ sont ceux en $A$ et en $B$.',r'Vérifier la somme|$68^\circ+56^\circ=124^\circ$.',r'$68^\circ+56^\circ=124^\circ$.')],[r'180-124==56',r'180-2*56==68 and 68+56==124'],r'angle_exterieur')

# 275 : centres non confondus avec l’origine, axe oblique et invariants.
add(275,3001,r'Un centre qui n’est pas l’origine',r'medium',r'Dans un repère à même unité sur les deux axes, le centre de symétrie est $S(1\,;-1)$. On donne $A(3\,;2)$ et $B(-2\,;0)$.',[
Q(r'Construire l’image A′ de A par la symétrie de centre S.',r'Faire de S le milieu du segment AA′.',r'Compter le déplacement vers S|De $A$ à $S$, on se déplace de 2 unités à gauche et 3 vers le bas.',r'Reproduire le déplacement|En partant de $S$, refaire le même déplacement : $A\prime(-1\,;-4)$.',r'$A\prime(-1\,;-4)$.'),
Q(r'Construire de même B′ et donner ses coordonnées.',r'Reproduire le déplacement de B à S.',r'Compter les unités|De $B(-2\,;0)$ à $S(1\,;-1)$ : 3 unités à droite et 1 vers le bas.',r'Reporter au-delà de S|On obtient $B\prime(4\,;-2)$.',r'$B\prime(4\,;-2)$.'),
Q(r'L’image du point O(0 ; 0) est-elle O ? Justifier.',r'Seul le centre est invariant par un demi-tour.',r'Compter de O à S|De $O$ à $S$ : 1 unité à droite et 1 vers le bas.',r'Reporter au-delà de S|L’image est $O\prime(2\,;-2)$, différente de $O$. Le centre fixe est $S$.',r'Non : $O\prime(2\,;-2)$.')],[r'(2*1-3,2*(-1)-2)==(-1,-4)',r'(2*1-(-2),2*(-1)-0)==(4,-2)',r'(2*1,2*(-1))==(2,-2)'],r'centre_decale')
add(275,3003,r'Une symétrie d’axe oblique',r'medium',r'Le repère utilise la même unité sur les deux axes. L’axe $(d)$ est la diagonale passant par $O(0\,;0)$ et $I(1\,;1)$. On donne $A(1\,;3)$ et $B(4\,;2)$.',[
Q(r'Construire A′ par symétrie d’axe d.',r'Tracer la perpendiculaire à l’axe puis reporter la même distance.',r'Repérer le pied|La perpendiculaire par $A$ rencontre $(d)$ en $H(2\,;2)$.',r'Reporter de l’autre côté|De $A$ à $H$, on va 1 à droite et 1 vers le bas. En répétant, on obtient $A\prime(3\,;1)$.',r'$A\prime(3\,;1)$.'),
Q(r'Construire B′ et donner ses coordonnées.',r'Utiliser le même principe de médiatrice.',r'Repérer le milieu sur l’axe|Le point $K(3\,;3)$ est le pied de la perpendiculaire par $B$.',r'Reporter le déplacement|De $B$ à $K$ : 1 à gauche et 1 vers le haut ; en répétant, $B\prime(2\,;4)$.',r'$B\prime(2\,;4)$.'),
Q(r'Donner deux points qui restent à leur place et justifier.',r'Utiliser l’invariance des points de l’axe.',r'Choisir des points de l’axe|$O$ et $I$ appartiennent à $(d)$.',r'Citer la propriété|Tout point situé sur l’axe d’une symétrie axiale est sa propre image.',r'O et I restent à leur place.')],[r'(1+3)/2==2 and (3+1)/2==2',r'(4+2)/2==3 and (2+4)/2==3',r'(3-1)*(1-3)+(3-1)*(3-1)==0'],r'axe_oblique')
add(275,3005,r'L’image d’un cercle',r'easy',r'Un cercle a pour centre $C(3\,;1)$ et pour rayon 2 unités. On considère le demi-tour de centre $O(0\,;0)$. Le repère utilise la même unité sur les deux axes.',[
Q(r'Construire l’image C′ du centre.',r'Utiliser le milieu du segment joignant un point à son image.',r'Aligner avec O|Tracer la droite $(CO)$.',r'Reporter la distance|Placer $C\prime$ de l’autre côté de $O$ avec $OC\prime=OC$, soit $C\prime(-3\,;-1)$.',r'$C\prime(-3\,;-1)$.'),
Q(r'Construire le cercle image et préciser son rayon.',r'Conserver les distances au centre.',r'Transformer le centre|Le centre du cercle image est $C\prime$.',r'Reporter le rayon|La symétrie conserve les longueurs : tracer le cercle de centre $C\prime$ et de rayon 2 unités.',r'Centre C′, rayon 2 unités.'),
Q(r'P(5 ; 1) est sur le cercle initial. Vérifier que son image est sur le cercle image.',r'Transformer P puis comparer sa distance au centre image.',r'Trouver P′|Le demi-tour donne $P\prime(-5\,;-1)$.',r'Calculer la distance|$C\prime$ et $P\prime$ ont la même ordonnée et leurs abscisses sont séparées de 2 unités. Donc $C\prime P\prime=2$.',r'$P\prime(-5\,;-1)$ appartient au cercle image.')],[r'math.dist((-3,-1),(-5,-1))==2'],r'cercle_image')
add(275,3008,r'Retrouver un centre de symétrie',r'medium',r'On sait que $A(-2\,;1)$ et $A\prime(4\,;3)$ sont images l’un de l’autre par une symétrie centrale. On donne aussi $B(0\,;4)$, dans le même repère.',[
Q(r'Construire le centre S et donner ses coordonnées.',r'Chercher le milieu de AA′.',r'Repérer la moitié du déplacement|De $A$ à $A\prime$, on va de 6 unités à droite et 2 vers le haut. La moitié est 3 à droite et 1 vers le haut.',r'Placer le milieu|À partir de $A(-2\,;1)$, on obtient $S(1\,;2)$.',r'$S(1\,;2)$.'),
Q(r'Construire B′ par la même symétrie.',r'Reporter au-delà du centre le déplacement de B à S.',r'De B à S|1 unité à droite et 2 vers le bas.',r'De S à B′|Le même déplacement donne $B\prime(2\,;0)$.',r'$B\prime(2\,;0)$.'),
Q(r'Le point T(1 ; 3) pourrait-il aussi être le centre ?',r'Vérifier la définition, pas seulement un alignement visuel.',r'Utiliser le milieu connu|Le milieu unique de $[AA\prime]$ est $S(1\,;2)$.',r'Comparer les points|$T\ne S$ : il ne peut pas être le milieu de ce segment, donc ne convient pas.',r'Non : le centre est le milieu unique S de [AA′].')],[r'((-2+4)/2,(1+3)/2)==(1,2)',r'(2*1-0,2*2-4)==(2,0)'],r'centre_inconnu')
add(275,3012,r'Deux transformations différentes d’un même point',r'medium',r'On donne $A(3\,;-2)$. On étudie séparément la symétrie centrale de centre $O(0\,;0)$ et la symétrie axiale d’axe vertical passant par $O$.',[
Q(r'Construire l’image Ac par le demi-tour.',r'Changer les deux déplacements depuis l’origine.',r'Placer de l’autre côté de O|Le déplacement « 3 à droite, 2 vers le bas » devient « 3 à gauche, 2 vers le haut ».',r'Lire le point|On obtient $A_c(-3\,;2)$.',r'$A_c(-3\,;2)$.'),
Q(r'Construire l’image Aa par la symétrie axiale.',r'Conserver la hauteur et changer de côté de l’axe.',r'Repérer la perpendiculaire|Elle est horizontale à l’ordonnée $-2$.',r'Reporter la distance|À 3 unités à gauche de l’axe, on obtient $A_a(-3\,;-2)$.',r'$A_a(-3\,;-2)$.'),
Q(r'Ces deux images sont-elles confondues ? Dans quel cas le seraient-elles pour un point de l’axe horizontal ?',r'Comparer les ordonnées et examiner un cas particulier.',r'Comparer les points obtenus|Les ordonnées 2 et $-2$ sont différentes : $A_c\ne A_a$.',r'Examiner un point (x ; 0)|Ses deux images ont pour coordonnées $(-x\,;0)$ ; pour un point de l’axe horizontal, elles coïncident.',r'Non pour A ; oui pour un point de l’axe horizontal.')],[r'(-3,2)!=(-3,-2)',r'all((-x,-0)==(-x,0) for x in range(-5,6))'],r'deux_symetries')
add(275,3015,r'Le centre d’un motif rectangulaire',r'hard',r'Les sommets d’un rectangle sont $A(-3\,;2)$, $B(5\,;2)$, $C(5\,;-2)$ et $D(-3\,;-2)$, dans un repère à même unité sur les deux axes.',[
Q(r'Placer les sommets et proposer un centre de symétrie S.',r'Chercher le milieu commun des diagonales.',r'Diagonale AC|De $A$ à $C$, le déplacement est 8 à droite et 4 vers le bas ; sa moitié est 4 à droite et 2 vers le bas.',r'Placer le milieu|À partir de $A$, cela donne $S(1\,;0)$. On obtient le même milieu avec $B$ et $D$.',r'$S(1\,;0)$.'),
Q(r'Démontrer que le demi-tour de centre S conserve le rectangle.',r'Vérifier les images des quatre sommets.',r'Première paire|$S$ est le milieu de $[AC]$, donc $A$ et $C$ s’échangent.',r'Seconde paire|$S$ est aussi le milieu de $[BD]$, donc $B$ et $D$ s’échangent. Les côtés sont envoyés sur les côtés opposés.',r'Le rectangle est envoyé sur lui-même.'),
Q(r'Calculer son aire et celle de son image, puis expliquer pourquoi l’égalité des aires ne suffit pas à prouver le centre proposé.',r'Séparer un invariant et la définition d’un centre.',r'Calculer l’aire|La longueur vaut 8 et la largeur 4 : $8\times4=32$ unités d’aire. L’image a aussi une aire de 32.',r'Justifier la limite de cet argument|Tout demi-tour conserve une aire, même si son centre n’est pas un centre de symétrie de la figure. Il faut vérifier la coïncidence des images des sommets.',r'32 unités d’aire pour chacune ; l’aire seule ne suffit pas.')],[r'((-3+5)/2,(2-2)/2)==(1,0)',r'8*4==32'],r'rectangle_centre')
add(275,3019,r'Deux symétries successives',r'hard',r'Dans un repère à même unité sur les deux axes, on donne $A(2\,;1)$. On applique d’abord le demi-tour de centre $O(0\,;0)$, puis la symétrie d’axe vertical passant par $O$.',[
Q(r'Construire le point intermédiaire B, image de A par le demi-tour.',r'Appliquer seulement la première transformation.',r'Utiliser le centre O|$O$ doit être le milieu de $[AB]$.',r'Lire les coordonnées|Les deux signes changent : $B(-2\,;-1)$.',r'$B(-2\,;-1)$.'),
Q(r'Construire C, image de B par la symétrie axiale.',r'Repartir du point intermédiaire, pas du point initial.',r'Conserver l’ordonnée|La symétrie d’axe vertical garde l’ordonnée $-1$.',r'Changer le côté de l’axe|L’abscisse $-2$ devient 2, donc $C(2\,;-1)$.',r'$C(2\,;-1)$.'),
Q(r'Pour cet exemple, quelle symétrie unique envoie directement A sur C ? Le vérifier sur D(4 ; 3).',r'Observer la coordonnée conservée et vérifier sur un autre point.',r'Identifier la transformation directe|De $(2\,;1)$ à $(2\,;-1)$, l’abscisse reste identique et l’ordonnée change de signe : symétrie d’axe horizontal.',r'Contrôler un autre point|$D(4\,;3)$ devient $(-4\,;-3)$ par le demi-tour, puis $(4\,;-3)$ par l’axe vertical : c’est bien son symétrique par l’axe horizontal.',r'La symétrie d’axe horizontal, également vérifiée pour D.')],[r'(-(-2),-1)==(2,-1)',r'(-(-4),-3)==(4,-3)'],r'successives')

add(273,2972,r'Deux bissectrices et un angle droit',r'hard',r'Les points $A$, $O$, $B$ sont alignés dans cet ordre. La demi-droite $[OC)$ est dans le demi-plan supérieur et $\widehat{COB}=64^\circ$. Les demi-droites $[OP)$ et $[OQ)$ sont les bissectrices respectives de $\widehat{COB}$ et $\widehat{AOC}$.',[
Q(r'Calculer AOC puis COQ.',r'Utiliser un angle plat puis la définition de la bissectrice.',r'Calculer le supplément|$\widehat{AOC}=180^\circ-64^\circ=116^\circ$.',r'Partager l’angle|$\widehat{COQ}=116^\circ\div2=58^\circ$.',r'$116^\circ$ puis $58^\circ$.'),
Q(r'Calculer POC puis POQ.',r'Additionner les deux demi-angles adjacents.',r'Première bissectrice|$\widehat{POC}=64^\circ\div2=32^\circ$.',r'Calculer l’angle entre les bissectrices|$\widehat{POQ}=32^\circ+58^\circ=90^\circ$.',r'$32^\circ$ puis $90^\circ$.'),
Q(r'Pourquoi obtient-on encore 90° si la mesure initiale de COB change ?',r'Utiliser la somme des deux angles supplémentaires.',r'Considérer la somme initiale|Les angles adjacents $\widehat{COB}$ et $\widehat{AOC}$ ont toujours une somme de $180^\circ$.',r'Partager la somme en deux|L’angle entre leurs bissectrices est la somme de leurs moitiés, donc la moitié de $180^\circ$, soit $90^\circ$.',r'Les deux bissectrices sont perpendiculaires.')],[r'180-64==116 and 116/2==58',r'64/2+116/2==90',r'all(t/2+(180-t)/2==90 for t in range(1,180))'],r'bissectrices_supplementaires')

# FIN DES DONNÉES PÉDAGOGIQUES

def graph(xmax,ymax,xt,yt,series,answers=(),xlabel=r'\text{Donnée}',ylabel=r'\text{Valeur}'):
    s=rf'\begin{{scope}}[x={6/xmax}cm,y={3.5/ymax}cm]'+'\n'
    for x in xt:
        if x:s+=rf'\draw[otRule,line width=.3pt] ({x},0)--({x},{ymax});\node[coteTexte,anchor=north,font=\small] at ({x},0) {{$ {str(x).replace(".","{,}")} $}};'+'\n'
    for y in yt:
        if y:s+=rf'\draw[otRule,line width=.3pt] (0,{y})--({xmax},{y});\node[coteTexte,anchor=east,font=\small] at (0,{y}) {{$ {str(y).replace(".","{,}")} $}};'+'\n'
    s+=rf'\draw[geoVecteur] (0,0)--({xmax*1.06},0);\draw[geoVecteur] (0,0)--(0,{ymax*1.08});'
    s+=node(0,0,'0','north east')+node(xmax/2,-ymax*.18,xlabel,'north')+node(0,ymax*1.1,ylabel,'south west')
    for points,color,connect in series:
        if connect:s+=r'\draw['+color+r',line width=1pt] '+'--'.join(f'({x},{y})' for x,y in points)+';\n'
        for x,y in points:s+=rf'\fill[{color}] ({x},{y}) circle (2pt);'+'\n'
    for x,y in answers:
        s+=rf'\draw[geoAide] ({x},0)--({x},{y})--(0,{y});\fill[otGreenDark] ({x},{y}) circle (2.5pt);'+'\n'
    return pic(s+'\n\\end{scope}')

def geoplan(points,segments=(),polygons=(),circles=(),labels=None):
    labels=labels or {};coords=[(x,y) for x,y,*_ in points.values()]+[(0,0)]
    for x,y,r,color in circles:coords.extend([(x-r,y-r),(x+r,y+r)])
    xmin=math.floor(min(x for x,y in coords))-1;xmax=math.ceil(max(x for x,y in coords))+1
    ymin=math.floor(min(y for x,y in coords))-1;ymax=math.ceil(max(y for x,y in coords))+1
    unit=min(.62,6.5/(xmax-xmin));s=rf'\begin{{scope}}[x={unit}cm,y={unit}cm]'+'\n'
    s+=rf'\draw[otRule,line width=.25pt,step=1] ({xmin},{ymin}) grid ({xmax},{ymax});\draw[geoVecteur] ({xmin},0)--({xmax+.35},0);\draw[geoVecteur] (0,{ymin})--(0,{ymax+.35});'+'\n'
    omitx={x for x,y,*_ in points.values() if y==0};omity={y for x,y,*_ in points.values() if x==0}
    step=2 if xmax-xmin>12 else 1
    for x in range(xmin,xmax+1):
        if x and x%step==0 and x not in omitx:s+=rf'\node[coteTexte,anchor=north,font=\small] at ({x},0) {{$ {x} $}};'+'\n'
    for y in range(ymin,ymax+1):
        if y and y not in omity and (unit>=.42 or y%2==0):
            anchor='south east' if y>0 else 'north east'
            s+=rf'\node[coteTexte,anchor={anchor},font=\small] at (0,{y}) {{$ {y} $}};'+'\n'
    if not any(x==y==0 for x,y,*_ in points.values()):s+=node(0,0,'0','north east')
    for names,color in polygons:
        s+=r'\draw['+color+r',line width=1pt] '+'--'.join(f'({points[k][0]},{points[k][1]})' for k in names)+'--cycle;\n'
    for a,b,style in segments:
        s+=rf'\draw[{style}] ({points[a][0]},{points[a][1]})--({points[b][0]},{points[b][1]});'+'\n'
    for x,y,r,color in circles:s+=rf'\draw[{color},line width=1pt] ({x},{y}) circle ({r});'+'\n'
    for name,(x,y,color,anchor) in points.items():
        if name in labels and labels[name] is None:continue
        s+=rf'\fill[{color}] ({x},{y}) circle (2pt);'+'\n'
        lx,ly,an=labels.get(name,(x,y,anchor));s+=node(lx,ly,name,an,color)
    return pic(s+'\n\\end{scope}')

def old_motif(x,y,central):
    ss=-1 if central else 1
    pts={'O':(0,0,'otInk','north east'),'A':(x,y,'otNavy','south east'),'B':(x+2,y,'otNavy','south west'),'C':(x,y+2,'otNavy','south east'),"A'":(-x,ss*y,'otGreenDark','north west' if central else 'south west'),"B'":(-x-2,ss*y,'otGreenDark','north east' if central else 'south east'),"C'":(-x,ss*(y+2),'otGreenDark','north west' if central else 'south west')}
    return geoplan(pts,polygons=[(['A','B','C'],'otNavy'),(["A'","B'","C'"],'otGreenDark')])

def constructed_triangle(L,a,b):
    # Coordinates are scaled by one common factor; angles and length ratios are exact.
    cx=5*math.tan(math.radians(b))/(math.tan(math.radians(a))+math.tan(math.radians(b)));cy=cx*math.tan(math.radians(a))
    oy=(cx*cx+cy*cy-5*cx)/(2*cy);rad=math.hypot(2.5,oy)
    s=rf'\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at ({cx},{cy});\coordinate(O) at (2.5,{oy});'
    s+=rf'\draw[otGreenDark!70,line width=.7pt] (O) circle ({rad});\draw[geoTrait] (A)--(B)--(C)--cycle;\fill[otGreenDark] (O) circle (2pt);'
    s+=node(0,0,'A','east')+node(5,0,'B','west')+node(cx,cy,'C','south')+node(2.5,oy,'O','south west' if oy>0 else 'north','otGreenDark')
    s+=node(2.5,oy-rad-.4,rf'AB={L}\text{{ cm}}','north')
    for angle,origin,ang in [(a,(0,0),a/2),(b,(5,0),180-b/2)]:
        x0,y0=origin;s+=node(x0+1.1*math.cos(math.radians(ang)),y0+1.1*math.sin(math.radians(ang)),rf'{angle}^\circ','center','otOrange')
    s+=node(cx,cy+.6,rf'{180-a-b}^\circ','south','otGreenDark')
    # Independent numerical check of the displayed circle.
    assert math.isclose(math.dist((2.5,oy),(cx,cy)),rad,abs_tol=1e-10)
    return pic(s)

def parallel(a,kind,corr=False):
    dx=1/math.tan(math.radians(a));s=rf'\coordinate(A) at ({dx},1);\coordinate(B) at ({-dx},-1);'
    s+=rf'\draw[geoTrait] (-3.1,1)--(3.1,1) (-3.1,-1)--(3.1,-1) ({-1.55*dx},-1.55)--({1.65*dx},1.65);'
    s+=node(-3.1,1,'(d)','south west')+node(-3.1,-1,'(e)','south west')+node(dx,1,'A','north west')+node(-dx,-1,'B','north west')
    if kind=='perp':
        s+=r'\draw[geoTrait] (-2.4,-1.5)--(-2.4,1.6);\draw[otNavy] (-2.4,.78)--(-2.18,.78)--(-2.18,1) (-2.4,-.78)--(-2.18,-.78)--(-2.18,-1);'
        s+=node(-2.4,1.65,'(s)','south')
        starts=[(dx,1,0,a,a,'otOrange'),(-dx,-1,0,a,a if corr else None,'otGreenDark')]
    elif kind=='somme':starts=[(dx,1,180+a,360,180-a,'otOrange'),(-dx,-1,0,a,a,'otOrange')]
    elif kind=='correspondants':starts=[(dx,1,0,a,a,'otOrange'),(-dx,-1,0,a,a,'otGreenDark')]
    else:starts=[(dx,1,180,180+a,a,'otOrange'),(-dx,-1,0,a,a,'otOrange')]
    if corr and kind=='somme':starts.append((dx,1,180,180+a,a,'otGreenDark'))
    if corr and kind=='alt':starts.append((dx,1,180+a,360,180-a,'otGreenDark'))
    for x,y,t1,t2,val,color in starts:
        if val is None:continue
        s+=rf'\draw[{color}] ({x+.7*math.cos(math.radians(t1))},{y+.7*math.sin(math.radians(t1))}) arc[start angle={t1},end angle={t2},radius=.7];'
        mid=(t1+t2)/2;s+=node(x+1.12*math.cos(math.radians(mid)),y+1.12*math.sin(math.radians(mid)),rf'{val}^\circ','center',color)
    return pic(s)

# Graphiques exacts : données en bleu, réponses/lectures en vert.
figure(271,'r30_pommes_corrige',graph(3,9,[0,1,2,2.5,3],[0,3,6,7.5,9],[([(0,0),(1,3),(2,6),(3,9)],'otGreenDark',True)],[(2.5,7.5)],r'\text{Masse (kg)}',r'\text{Prix (€)}'))
figure(272,'r30_points_axes_corrige',geoplan({'A':(-3,2,'otNavy','south east'),'B':(0,-2,'otNavy','east'),'C':(4,0,'otNavy','south west'),'D':(4,2,'otGreenDark','south west')},[('A','D','geoAide'),('C','D','geoAide')]))
for corr in (False,True):
    suffix='_corrige' if corr else '_enonce'
    figure(272,'r30_cuve'+suffix,graph(8,20,[0,2,4,6,8],[0,5,10,15,20],[([(0,0),(8,20)],'otNavy',True)],[(4,10),(6,15)] if corr else [],r'\text{Temps (min)}',r'\text{Volume (L)}'))
    figure(272,'r30_promenade'+suffix,graph(50,3,[0,10,20,30,40,50],[0,1,2,3],[([(0,0),(20,1),(30,1),(50,2.5)],'otNavy',True)],[(20,1),(30,1),(50,2.5)] if corr else [],r'\text{Temps (min)}',r'\text{Distance (km)}'))
figure(272,'r30_aires_carres_corrige',graph(4,16,[0,1,2,3,4],[0,4,8,12,16],[([(1,1),(2,4),(3,9),(4,16)],'otGreenDark',False)],[],r'\text{Côté (cm)}',r'\text{Aire (cm}^2\text{)}'))
figure(272,'r30_tarifs_corrige',graph(6,18,list(range(7)),[0,3,6,9,12,15,18],[([(n,3*n) for n in range(7)],'otNavy',False),([(n,2*n+4) for n in range(7)],'otOrange',False)],[(4,12)],r'\text{Nombre d’activités}',r'\text{Prix (€) : A bleu, B orange}'))

# Angles : toutes les mesures inscrites correspondent aux directions effectives.
s=r'\draw[geoTrait] (0,3)--(0,0)--(3,0);\draw[geoTrait] (0,0)--(34:3);\draw[geoReponse] (0,0)--(62:3.2);\draw[otNavy] (.22,0)--(.22,.22)--(0,.22);'
for x,y,l,an in [(0,0,'O','north east'),(3,0,'A','south west'),(0,3,'B','south'),(3*math.cos(math.radians(34)),3*math.sin(math.radians(34)),'C','south west'),(3.2*math.cos(math.radians(62)),3.2*math.sin(math.radians(62)),'D','south')]:s+=node(x,y,l,an)
s+=node(1.4*math.cos(math.radians(17)),1.4*math.sin(math.radians(17)),r'34^\circ','center','otOrange')
s+=node(2.2*math.cos(math.radians(48)),2.2*math.sin(math.radians(48)),r'28^\circ','center','otGreenDark')
figure(273,'r30_angle_droit_corrige',pic(s))
s=r'\draw[geoTrait] (-3,0)--(3,0) (0,0)--(64:3);\draw[geoReponse] (0,0)--(32:2.9) (0,0)--(122:2.9);'
for angle,name in [(0,'B'),(180,'A'),(64,'C'),(32,'P'),(122,'Q')]:s+=node(3.2*math.cos(math.radians(angle)),3.2*math.sin(math.radians(angle)),name,'south' if angle>0 and angle<180 else 'north')
s+=node(0,0,'O','north')+node(0,-.65,r'\widehat{POQ}=32^\circ+58^\circ=90^\circ','north','otGreenDark')
figure(273,'r30_bissectrices_supplementaires_corrige',pic(s))
for name,a,kind in [('reciproque',58,'alt'),('perpendiculaires',37,'perp'),('somme_paralleles',68,'somme')]:
    for corr in (False,True):figure(273,'r30_'+name+('_corrige' if corr else '_enonce'),parallel(a,kind,corr))
ax=5*math.tan(math.radians(67))/(math.tan(math.radians(48))+math.tan(math.radians(67)));ay=ax*math.tan(math.radians(48))
for corr in (False,True):
    s=rf'\draw[geoTrait] (0,0)--(5,0)--({ax},{ay})--cycle;\draw[geoTrait] (-.8,{ay})--(5.8,{ay});'
    for x,y,l,an in [(0,0,'B','north east'),(5,0,'C','north west'),(ax,ay,'A','south'),(-.8,ay,'D','south'),(5.8,ay,'E','south')]:s+=node(x,y,l,an)
    s+=node(.9*math.cos(math.radians(24)),.9*math.sin(math.radians(24)),r'48^\circ','center','otOrange')+node(5+.9*math.cos(math.radians(146.5)),.9*math.sin(math.radians(146.5)),r'67^\circ','center','otOrange')
    if corr:
        s+=node(ax,ay-.85,r'65^\circ','center','otGreenDark')
        s+=node(ax+1.1*math.cos(math.radians(204)),ay+1.1*math.sin(math.radians(204)),r'48^\circ','center','otGreenDark')
        s+=node(ax+1.1*math.cos(math.radians(-33.5)),ay+1.1*math.sin(math.radians(-33.5)),r'67^\circ','center','otGreenDark')
    figure(273,'r30_triangle_parallele'+('_corrige' if corr else '_enonce'),pic(s))
r0=1.7;rp=2.3;px=rp*math.cos(math.radians(35));py=rp*math.sin(math.radians(35));nx=r0*math.cos(math.radians(70));ny=r0*math.sin(math.radians(70));rc=math.dist((r0,0),(px,py));am=math.degrees(math.atan2(py,px-r0));an=math.degrees(math.atan2(py-ny,px-nx))
s=rf'\draw[geoTrait] (0,0)--(3.1,0) (0,0)--(70:3.1);\draw[otOrange] ({r0},0) arc[start angle=0,end angle=70,radius={r0}];\draw[geoReponse] (0,0)--({px},{py});'
for x,y,angle in [(r0,0,am),(nx,ny,an)]:s+=rf'\draw[otGreenDark!65] ({x+rc*math.cos(math.radians(angle-18))},{y+rc*math.sin(math.radians(angle-18))}) arc[start angle={angle-18},end angle={angle+18},radius={rc}];'
for x,y,l,anc in [(0,0,'O','north east'),(3.1,0,'A','south west'),(3.1*math.cos(math.radians(70)),3.1*math.sin(math.radians(70)),'B','south'),(r0,0,'M','north'),(nx,ny,'N','south east'),(px,py,'P','south west')]:s+=node(x,y,l,anc,'otGreenDark' if l=='P' else 'otInk')
figure(273,'r30_bissectrice_corrige',pic(s))

# Triangles construits à partir des longueurs ou des angles exacts.
s=r'\coordinate(A) at (0,0);\coordinate(B) at (5,0);\coordinate(C) at (1.8,2.4);\draw[geoReponse] (A)--(B)--(C)--cycle;\draw[geoAide] (0,0)--(1.8,-2.4)--(5,0);'
for x,y,l,a in [(0,0,'A','east'),(5,0,'B','west'),(1.8,2.4,'C','south'),(1.8,-2.4,"C'",'north')]:s+=node(x,y,l,a,'otGreenDark' if l.startswith('C') else 'otInk')
for ox,oy,r,ang in [(0,0,3,math.degrees(math.atan2(2.4,1.8))),(5,0,4,math.degrees(math.atan2(2.4,-3.2)))]:
    for sign in (-1,1):
        t=sign*ang;s+=rf'\draw[otOrange!85] ({ox+r*math.cos(math.radians(t-12))},{oy+r*math.sin(math.radians(t-12))}) arc[start angle={t-12},end angle={t+12},radius={r}];'
s+=node(2.5,.25,r'5\text{ cm}','south')+node(.4,1.3,r'3\text{ cm}','east')+node(3.8,1.3,r'4\text{ cm}','west')
figure(274,'r30_trois_cotes_corrige',pic(s))
h=2*math.sqrt(3);s=rf'\draw[geoReponse] (0,0)--(5,0)--(2,{h})--cycle;\draw[otOrange] (.65,0) arc[start angle=0,end angle=60,radius=.65];\draw[geoAide] (45:4) arc[start angle=45,end angle=75,radius=4];'
s+=node(0,0,'A','east')+node(5,0,'B','west')+node(2,h,'C','south')+node(2.5,-.4,r'5\text{ cm}','north')+node(.4,2,r'4\text{ cm}','east')+node(1,.28,r'60^\circ','center','otOrange')
figure(274,'r30_deux_cotes_angle_corrige',pic(s))
h=1.6*math.tan(math.radians(68));s=rf'\coordinate(A) at (0,{h});\coordinate(B) at (-1.6,0);\coordinate(C) at (1.6,0);\coordinate(M) at (0,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoReponse] (A)--(M);\codage{{A}}{{B}}\codage{{A}}{{C}}\angledroit{{A}}{{M}}{{C}}'
for x,y,l,a in [(0,h,'A','south'),(-1.6,0,'B','north east'),(1.6,0,'C','north west'),(0,0,'M','north')]:s+=node(x,y,l,a)
s+=node(.5,h+.5,r'\widehat{BAC}=44^\circ','south west','otOrange')+node(0,-.85,r'\widehat{BAM}=22^\circ','north','otGreenDark')
figure(274,'r30_isocele_corrige',pic(s))
s=r'\coordinate(A) at (0,0);\coordinate(B) at (6,0);\coordinate(C) at (2,4);\coordinate(O) at (3,1);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoReponse] (O) circle (3.16227766);\draw[geoAide] (3,-2.3)--(3,4.7) (-.5,2.75)--(6.5,-.75);\fill[otGreenDark] (O) circle (2pt);'
s+=node(0,0,'A','east')+node(6,0,'B','west')+node(2,4,'C','south')+node(3.4,1.4,'O','south','otGreenDark')
figure(274,'r30_mediatrices_corrige',pic(s))
s=r'\coordinate(A) at (-2,3);\coordinate(B) at (0,0);\coordinate(C) at (6,0);\coordinate(H) at (-2,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoAide] (H)--(B);\draw[geoReponse] (A)--(H);\angledroit{A}{H}{C}'
for x,y,l,a in [(-2,3,'A','south'),(0,0,'B','north'),(6,0,'C','north west'),(-2,0,'H','north')]:s+=node(x,y,l,a)
s+=node(-2.3,1.5,r'3\text{ cm}','east','otGreenDark')+node(3,-.6,r'6\text{ cm}','north')+node(3,2.2,r'\mathcal A=9\text{ cm}^2','south','otGreenDark')
figure(274,'r30_hauteur_exterieure_corrige',pic(s))
h=1.8*math.tan(math.radians(56))
for corr in (False,True):
    s=rf'\coordinate(A) at (0,{h});\coordinate(B) at (-1.8,0);\coordinate(C) at (1.8,0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoTrait] (1.8,0)--(3.6,0);\codage{{A}}{{B}}\codage{{A}}{{C}}'
    for x,y,l,a in [(0,h,'A','south'),(-1.8,0,'B','north east'),(1.8,0,'C','north'),(3.6,0,'D','north west')]:s+=node(x,y,l,a)
    s+=node(2.35,1,r'124^\circ','center','otOrange')
    if corr:s+=node(0,h-.85,r'68^\circ','center','otGreenDark')+node(-1.05,.4,r'56^\circ','center','otGreenDark')+node(1.05,.4,r'56^\circ','center','otGreenDark')
    figure(274,'r30_angle_exterieur'+('_corrige' if corr else '_enonce'),pic(s))

# Symétries : coordonnées précises et unité identique sur les deux axes.
figure(275,'r30_centre_decale_corrige',geoplan({'A':(3,2,'otNavy','south west'),'B':(-2,0,'otNavy','south east'),'S':(1,-1,'otOrange','south'),"A'":(-1,-4,'otGreenDark','north east'),"B'":(4,-2,'otGreenDark','south west'),'O':(0,0,'otInk','north east'),"O'":(2,-2,'otGreenDark','north east')},[('A',"A'",'geoAide'),('B',"B'",'geoAide')],labels={'S':(1.4,-.7,'south west')}))
figure(275,'r30_axe_oblique_corrige',geoplan({'O':(0,0,'otInk','north east'),'I':(1,1,'otOrange','south east'),'A':(1,3,'otNavy','south east'),'B':(4,2,'otNavy','south west'),"A'":(3,1,'otGreenDark','south west'),"B'":(2,4,'otGreenDark','south west'),'U':(-1,-1,'otOrange','east'),'V':(5,5,'otOrange','west')},[('U','V','geoTrait'),('A',"A'",'geoAide'),('B',"B'",'geoAide')],labels={'U':None,'V':None}).replace(r'\end{scope}',node(5,5,'(d)','west')+r'\end{scope}'))
figure(275,'r30_cercle_image_corrige',geoplan({'O':(0,0,'otInk','north east'),'C':(3,1,'otNavy','south'),"C'":(-3,-1,'otGreenDark','south'),'P':(5,1,'otNavy','west'),"P'":(-5,-1,'otGreenDark','east')},circles=[(3,1,2,'otNavy'),(-3,-1,2,'otGreenDark')]))
figure(275,'r30_centre_inconnu_corrige',geoplan({'A':(-2,1,'otNavy','south east'),"A'":(4,3,'otNavy','south west'),'B':(0,4,'otNavy','east'),"B'":(2,0,'otGreenDark','south west'),'S':(1,2,'otGreenDark','south')},[('A',"A'",'geoAide'),('B',"B'",'geoAide')],labels={'S':(1.4,2.5,'south')}))
figure(275,'r30_deux_symetries_corrige',geoplan({'O':(0,0,'otInk','north east'),'A':(3,-2,'otNavy','south west'),'A_c':(-3,2,'otGreenDark','south east'),'A_a':(-3,-2,'otGreenDark','north east')},[('A','A_c','geoAide'),('A','A_a','geoAide')]))
figure(275,'r30_rectangle_centre_corrige',geoplan({'A':(-3,2,'otNavy','south east'),'B':(5,2,'otNavy','south west'),'C':(5,-2,'otNavy','north west'),'D':(-3,-2,'otNavy','north east'),'S':(1,0,'otGreenDark','south')},[('A','C','geoAide'),('B','D','geoAide')],[(['A','B','C','D'],'otNavy')],labels={'S':(1,.5,'south')}))
figure(275,'r30_successives_corrige',geoplan({'O':(0,0,'otInk','north east'),'A':(2,1,'otNavy','south west'),'B':(-2,-1,'otOrange','north east'),'C':(2,-1,'otGreenDark','north west')},[('A','B','geoAide'),('B','C','geoAide')]))

# Choisir pour O le secteur libre entre les traits de construction.
for name,newanchor in [('r30_centre_decale_corrige','south west'),('r30_axe_oblique_corrige','south east'),('r30_cercle_image_corrige','south west'),('r30_successives_corrige','south east')]:
    FIGS[275][name]=FIGS[275][name].replace(node(0,0,'O','north east'),node(0,0,'O',newanchor))
FIGS[275]['r30_centre_decale_corrige']=FIGS[275]['r30_centre_decale_corrige'].replace(node(1.4,-.7,'S','south west','otOrange'),node(1.2,-1.4,'S','north west','otOrange'))
FIGS[275]['r30_cercle_image_corrige']=FIGS[275]['r30_cercle_image_corrige'].replace(r'coteTexte,anchor=north,font=\small',r'coteTexte,anchor=south,font=\small')

def exact_rosace(a):
    s=rf'\coordinate(O) at (0,0);\coordinate(A) at (-3,0);\coordinate(B) at (3,0);\coordinate(C) at ({180+a}:2.6);\coordinate(D) at ({a}:2.6);\coordinate(E) at ({180+a/2}:2.8);'
    s+=r'\draw[geoTrait] (A)--(B) (C)--(D);\draw[geoAide] (O)--(E);'
    s+=rf'\draw[otOrange] (-.7,0) arc[start angle=180,end angle={180+a},radius=.7];\draw[geoReponse] (.7,0) arc[start angle=0,end angle={a},radius=.7];'
    for name,an in [('A','south east'),('B','south west'),('O','south east'),('C','north east'),('D','south west'),('E','north west')]:s+=rf'\node[anchor={an},inner sep=4pt] at ({name}) {{$ {name} $}};'
    bottom=min(-2.6*math.sin(math.radians(a)),-2.8*math.sin(math.radians(a/2)))
    s+=node(0,bottom-.5,rf'\widehat{{AOC}}={a}^\circ','north','otOrange')+node(0,bottom-1.1,rf'\widehat{{BOD}}={a}^\circ','north','otGreenDark')
    return pic(s)

def improve_calculations(text):
    def transform(m):
        expression=m[1]
        if expression.count('=')<2 or len(expression)<25 or '\\begin' in expression:return m[0]
        pieces=expression.split('=')
        if any(not p.strip() for p in pieces):return m[0]
        return '\n\n'+aligned(pieces[0]+'&='+pieces[1],*['&='+p for p in pieces[2:]])+'\n\n'
    return re.sub(r'(?<!\$)\$([^$\n]+)\$(?!\$)',transform,text)

NOTES={
271:r'Vérifier la référence du pourcentage, l’unité de l’échelle et le caractère entier des achats avant de conclure.',
272:r'Lire les unités des axes et ne pas inverser abscisse et ordonnée. Des points alignés ne suffisent pas à prouver une proportionnalité.',
273:r'Citer l’hypothèse qui autorise la propriété. Un angle opposé par le sommet n’est pas un angle correspondant.',
274:r'Une construction se justifie avec les données et les codages. Choisir la hauteur correspondant à la base et convertir les longueurs avant le calcul.',
275:r'Pour un demi-tour, contrôler le milieu ; pour une symétrie axiale, contrôler la médiatrice. Une aire conservée ne suffit pas à identifier une figure image.'}
CUSTOM_NOTES={
2917:'Le total de référence reste 40 adhérents ; la partie choisie change quand on passe au complément.',
2920:'Une augmentation du prix de 3 € par kilogramme ne suffit pas : le forfait fixe empêche la proportionnalité.',
2924:'Une échelle compare deux longueurs exprimées dans la même unité. Un agrandissement du dessin change son échelle.',
2927:'Le même montant en euros ne représente pas le même pourcentage de deux prix différents.',
2931:'La droite doit passer par l’origine. Lire le prix sur l’axe vertical, après avoir repéré la masse sur l’axe horizontal.',
2934:'Comparer les prix après les remises et vérifier que le nombre de lots permet exactement l’achat demandé.',
2935:'Le nombre de sachets est entier : on achète assez de fruits, sans arrondir la masse nécessaire vers le bas.',
2938:'Un point d’abscisse nulle appartient à l’axe vertical ; un point d’ordonnée nulle appartient à l’axe horizontal.',
2940:'Le pas d’un axe se lit avec ses graduations : un carreau ne vaut pas toujours une unité.',
2944:'Le périmètre additionne quatre côtés ; le terme fixe des deux largeurs empêche ici la proportionnalité avec la longueur.',
2946:'Si le côté d’un carré double, son aire quadruple. Une dépendance croissante peut être non proportionnelle.',
2949:'La distance affichée est cumulée. Pour une portion du trajet, soustraire la valeur initiale à la valeur finale.',
2954:'Comparer les deux prix pour le même nombre d’activités. Ne pas inventer un nombre non entier d’activités entre les points.',
2956:'Le quotient du budget restant par le prix d’un atelier ne donne un achat possible que si le nombre retenu est entier.',
2959:'Des angles complémentaires ont une somme de 90° ; des angles supplémentaires, une somme de 180°.',
2961:'L’égalité d’angles alternes internes permet de prouver le parallélisme : c’est le sens réciproque de la propriété.',
2965:'Écrire le parallélisme démontré avant de l’utiliser pour comparer des angles aux deux intersections.',
2967:'Une égalité d’angles opposés par le sommet est vraie à une seule intersection ; elle ne prouve pas un parallélisme.',
2971:'La parallèle au côté opposé permet de retrouver la somme des angles du triangle à partir d’un angle plat.',
2972:'Les bissectrices de deux angles adjacents supplémentaires sont perpendiculaires : la moitié de leur somme vaut 90°.',
2974:'Deux angles intérieurs du même côté ne sont pas alternes internes. Faire apparaître le supplémentaire avant de conclure.',
2977:'Une bissectrice se construit avec des distances égales ; la mesure au rapporteur sert ensuite à contrôler.',
2980:'L’inégalité triangulaire doit être stricte pour obtenir un triangle non aplati ; l’égalité donne trois points alignés.',
2981:'L’angle compris a pour sommet l’extrémité commune des deux côtés donnés. Ne pas le placer à un autre sommet.',
2984:'Dans « isocèle en A », A est le sommet principal ; les angles égaux sont ceux en B et C.',
2987:'Une seule médiatrice donne une seule égalité de distances ; deux médiatrices permettent de trouver le centre circonscrit.',
2991:'La hauteur est perpendiculaire à la droite portant le côté opposé ; son pied peut être hors du segment.',
2994:'Une conversion de m² en cm² multiplie par 10 000, alors qu’une conversion de mètres en centimètres multiplie par 100.',
2998:'L’angle extérieur est supplémentaire de l’angle intérieur adjacent ; ils n’ont pas la même mesure.',
3001:'Changer les deux signes des coordonnées convient au centre O, mais pas à un centre quelconque. Ici, utiliser le milieu S.',
3003:'Pour un axe oblique, reporter une distance perpendiculairement à l’axe ; un simple déplacement horizontal ne convient pas.',
3005:'Le centre du cercle se transforme, mais son rayon reste identique.',
3008:'Le centre de symétrie est le milieu du segment joignant un point à son image : il est alors unique.',
3012:'Le centre est un point ; l’axe est une droite. Ces deux transformations n’ont généralement pas la même image.',
3015:'Un centre de symétrie doit renvoyer la figure sur elle-même. L’égalité des aires ne prouve pas cette coïncidence.',
3019:'Pour deux transformations successives, appliquer la seconde au point intermédiaire, pas au point initial.'}
HEADINGS={271:['Revenir à une personne','Adapter la quantité','Préciser le sens du coefficient','Retrouver le nombre de parts','Appliquer un doublement','Tester l’effet d’un forfait'],272:['Lire le couple ordonné','Repérer le signe de l’ordonnée','Comparer les ordonnées','Compter les unités horizontalement','Calculer hauteur et aire','Justifier le milieu commun'],273:['Identifier la configuration','Choisir les angles liés','Utiliser un angle plat','Exploiter l’égalité justifiée','Partager par une bissectrice','Vérifier la conclusion'],274:['Utiliser la donnée géométrique','Choisir la propriété adaptée','Préparer les mesures','Effectuer la construction','Justifier la propriété obtenue','Contrôler la construction'],275:['Construire l’image du premier point','Lire les coordonnées de l’image','Transformer les deux autres sommets','Utiliser les longueurs conservées','Calculer puis conserver l’aire','Appliquer une seconde fois la symétrie']}

for d in sorted(BASE.iterdir()):
    if not d.is_dir() or not d.name[:3].isdigit() or not 271<=int(d.name[:3])<=275:continue
    n=int(d.name[:3]);backup=d/'sauvegardes/revision_2026-10-30';assert backup.is_dir(),'Sauvegarde obligatoire'
    # Always derive this revision from the immutable backup, so reruns do not duplicate notes.
    text=(backup/'exercices.txt').read_text(encoding='utf-8');meta=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('old',backup/'figures/figures.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    figures=dict(old.FIGURES);figures.update(FIGS.get(n,{}));corr=json.loads((backup/'figures/correspondance.json').read_text(encoding='utf-8'));blocks=[];changes=[]
    for b in [x.strip() for x in re.split(r'^===\s*$',text,flags=re.M) if x.strip()]:
        eid=int(re.search(r'^Id:\s*(\d+)',b,re.M)[1]);oldtitle=b.splitlines()[0].replace('===','',1).strip()
        if eid in NEW:
            e=NEW[eid];prefix={'easy':'Découverte','medium':'Entraînement','hard':'Problème'}[e['difficulte']]
            title=f"{prefix} - {meta['titre']} - {e['titre']}"
            intro=e['intro'].replace(r'\n','\n');enonce=intro+'\n\n'+'\n'.join(f'{i}. {q[0]}' for i,q in enumerate(e['questions'],1));steps=[];answers=[]
            for i,(question,method,one,two,result) in enumerate(e['questions'],1):
                steps.append(f'## Question {i} : {question}\n\n'+box('methode',method)+'\n'+box('etape',improve_calculations(one[1]),one[0])+'\n'+box('etape',improve_calculations(two[1]),two[0])+'\n'+box('resultat',result))
                answers.append(f'{i}. {result}')
            corr['exercices'].pop(str(eid),None)
            if e['figure']:
                name='r30_'+e['figure'];corr['exercices'][str(eid)]={'2':{'fichier':name+'_corrige.png','alt':'Figure corrigée exacte : '+e['titre']+' ; éléments de réponse en vert.'}}
                if '[IMAGE_1]' in intro:corr['exercices'][str(eid)]['1']={'fichier':name+'_enonce.png','alt':'Données graphiques exactes : '+e['titre']+'.'}
                steps.append('[IMAGE_2]')
            steps.append(box('attention' if e['difficulte']=='hard' else 'retenir',CUSTOM_NOTES.get(eid,NOTES[n])))
            b='=== '+title+f"\nId: {eid}\nDifficulté: {e['difficulte']}\n\nÉnoncé:\n<!-- optitab:1 -->\n"+enonce+'\n\nÉtapes:\n<!-- optitab:1 -->\n'+'\n'.join(steps)+'\n\nSolution:\n<!-- optitab:1 -->\n'+'\n'.join(answers)
            changes.append({'id':eid,'ancien_titre':oldtitle,'nouveau_titre':title,'difficulte':e['difficulte'],'competence':e['titre'],'questions':len(e['questions'])})
        else:
            if eid==2975:
                # This block duplicated the 60° exercise exactly; keep it as a decimal-half consolidation.
                for oldvalue,newvalue in [('120','105'),('60','75'),('30','37{,}5')]:b=re.sub(r'(?<!\d)'+oldvalue+r'(?!\d)',lambda m:newvalue,b)
            en=b.split('Énoncé:',1)[1].split('Étapes:',1)[0]
            if n==271:
                p,m=map(int,re.search(r'pour (\d+) personnes demande (\d+) g',en).groups());q=int(re.search(r'pour (\d+) personnes \?',en)[1]);level='easy';short=f'Recette : {m} g pour {p} personnes, cible {q}'
            elif n==272:
                if 'jardin rectangulaire' in en:
                    a,h=map(int,re.search(r'A\(-([0-9]+) ; ([0-9]+)\)',en).groups());level='easy';short=f'Jardin de {2*a} m sur {2*h} m';name=f'r30_jardin_{a}_{h}'
                    figures[name]=geoplan({'O':(0,0,'otGreenDark','north east'),'A':(-a,h,'otNavy','south east'),'B':(a,h,'otNavy','south west'),'C':(a,-h,'otNavy','north west'),'D':(-a,-h,'otNavy','north east')},polygons=[(['A','B','C','D'],'otNavy')])
                    corr['exercices'][str(eid)]={'2':{'fichier':name+'.png','alt':f'Rectangle exact de {2*a} m sur {2*h} m, placé dans le repère ; coordonnées conformes à l’énoncé.'}}
                else:
                    f,k=map(int,re.search(r'coûte (\d+) €.*puis (\d+) €',en).groups());level='medium';short=f'Tarif : entrée {f} €, puis {k} € par activité'
            elif n==273:
                a=int(re.search(r'mesure (\d+)°',en)[1]);ros='rosace' in oldtitle;level='easy' if ros else 'medium';short=('Sécantes et bissectrice : ' if ros else 'Parallèles et sécante : ')+f'{a}°';name=f'r30_'+('rosace' if ros else 'paralleles')+f'_{a}'
                figures[name]=exact_rosace(a) if ros else parallel(a,'correspondants',True)
                corr['exercices'][str(eid)]={'2':{'fichier':name+'.png','alt':f'Configuration exacte avec angle de {a} degrés, angles ou constructions de réponse en vert.'}}
                b=b.replace('Les positions des autres angles sont indiquées sur la figure.','Repérer les angles à partir de leur position autour des intersections.')
            elif n==274:
                level='medium'
                if 'On veut construire' in en:
                    L,a,bb=map(int,re.search(r'AB = (\d+) cm.*BAC = (\d+)°.*ABC = (\d+)°',en).groups());short=f'Construire : côté {L} cm et angles {a}°, {bb}°';name=f'r30_construction_{L}_{a}_{bb}'
                    figures[name]=constructed_triangle(L,a,bb);corr['exercices'][str(eid)]={'2':{'fichier':name+'.png','alt':f'Triangle ABC exact : AB vaut {L} cm, angles {a}, {bb}, {180-a-bb} degrés ; cercle circonscrit et centre O en vert.'}}
                    b=b.replace('Une figure de travail à main levée est fournie ; elle n’est pas à mesurer.','Réaliser d’abord un schéma à main levée, puis la construction à la règle et au rapporteur.')
                else:
                    base,h=map(int,re.search(r'BC de (\d+) m.*mesure (\d+) m',en).groups());short=f'Base {base} m, hauteur {h} m : médiane et aires'
                    # Base/height geometry is now exact, not one schema with unrelated proportions.
                    sc=min(.65,6/base);s=rf'\begin{{scope}}[x={sc}cm,y={sc}cm]\coordinate(B) at (0,0);\coordinate(C) at ({base},0);\coordinate(A) at ({base/3},{h});\coordinate(H) at ({base/3},0);\coordinate(M) at ({base/2},0);\draw[geoTrait] (A)--(B)--(C)--cycle;\draw[geoAide] (A)--(H);\draw[geoReponse] (A)--(M);\angledroit{{A}}{{H}}{{C}}\codage{{B}}{{M}}\codage{{M}}{{C}}'
                    for xx,yy,ll,an in [(0,0,'B','north east'),(base,0,'C','north west'),(base/3,h,'A','south'),(base/3,0,'H','north'),(base/2,0,'M','north')]:s+=node(xx,yy,ll,an)
                    s+='\\end{scope}';name=f'r30_mediane_{base}_{h}';figures[name]=pic(s);corr['exercices'][str(eid)]={'2':{'fichier':name+'.png','alt':f'Triangle de base {base} m et hauteur {h} m, proportions exactes, médiane AM verte et hauteur AH perpendiculaire.'}}
            else:
                x,y=map(int,re.search(r'A\((\d+) ; (\d+)\)',en).groups());central='centrale' in en;level='easy';short=('Demi-tour' if central else 'Axe vertical')+f' : triangle de sommet A({x} ; {y})';name=f'r30_motif_{x}_{y}';figures[name]=old_motif(x,y,central)
                corr['exercices'][str(eid)]={'2':{'fichier':name+'.png','alt':f'Construction exacte dans un repère à même unité : triangle de sommet A({x} ; {y}) et image verte par '+('demi-tour de centre O.' if central else 'symétrie d’axe vertical.')}}
            prefix={'easy':'Découverte','medium':'Entraînement'}[level];title=f"{prefix} - {meta['titre']} - {short}"
            b=re.sub(r'^===.*$', '=== '+title,b,count=1,flags=re.M);b=re.sub(r'^Difficulté:.*$', 'Difficulté: '+level,b,flags=re.M)
            # Remove generic input diagrams; coordinates/directions fully define each construction.
            b=b.replace('[IMAGE_1]','');b=re.sub(r'::: remarque Lecture du schéma\n.*?\n:::\n?','',b,flags=re.S)
            corr['exercices'].get(str(eid),{}).pop('1',None)
            chunks=re.split(r'(^## Question \d+[^\n]*\n)',b,flags=re.M)
            for i in range(1,len(chunks),2):
                number=int(re.search(r'Question (\d+)',chunks[i])[1]);body=chunks[i+1]
                body=body.replace('::: etape Mise en œuvre','::: etape '+HEADINGS[n][number-1])
                # A long existing reasoning becomes two explicit steps, rather than one generic block.
                pattern=r'(::: etape [^\n]+\n)(.*?)(\n:::)'
                def split_step(m):
                    content=m[2];parts=re.split(r'(?<=[.!?])\s+',content,maxsplit=1)
                    if len(content)>180 and len(parts)==2 and len(parts[1])>45:return m[1]+improve_calculations(parts[0])+m[3]+'\n\n'+box('etape',improve_calculations(parts[1]),'Calculer puis vérifier')
                    return m[1]+improve_calculations(content)+m[3]
                chunks[i+1]=re.sub(pattern,split_step,body,flags=re.S)
            b=''.join(chunks)
            pos=b.index('Solution:');b=b[:pos]+box('retenir',NOTES[n])+'\n'+b[pos:]
            changes.append({'id':eid,'ancien_titre':oldtitle,'nouveau_titre':title,'difficulte':level,'competence':'Consolidation : '+short,'questions':6,'conserve':True})
        blocks.append(re.sub(r'\n{4,}','\n\n\n',b))
    (d/'exercices.txt').write_text('\n\n===\n\n'.join(blocks)+'\n',encoding='utf-8')
    for c in meta['cours']:
        p=backup/f"cours_{c['id']}.txt";t=p.read_text(encoding='utf-8')
        if n==271:
            t=t.replace('## IV. Échelles et grandeurs',box('methode',r'Calculer d’abord le montant du pourcentage sur la quantité de référence. Pour une augmentation, ajouter ce montant ; pour une réduction, le soustraire. Si la référence change, recalculer le pourcentage sur la nouvelle quantité.','Augmenter ou réduire')+'\n## IV. Échelles et grandeurs')
            addition=box('exemple',r'Pour des pommes à 3 € le kilogramme, on place les points $(0\,;0)$, $(1\,;3)$, $(2\,;6)$ et $(3\,;9)$. La droite passe par l’origine ; à $2{,}5$ kg on lit $7{,}50$ €.','Représenter une proportionnalité')+'\n[IMAGE_1]\n\n'
            t=t.replace('::: retenir\n',addition+'::: retenir\n');corr['cours'][str(c['id'])]={'1':{'fichier':'r30_pommes_corrige.png','alt':'Proportionnalité : prix de 3 euros par kilogramme et lecture du prix de 2,5 kg.'}}
        elif n==272:
            addition=box('exemple',r'Une cuve reçoit 5 L toutes les 2 min. À 4 min on lit 10 L ; inversement, 15 L sont atteints à 6 min. Une graduation horizontale ne représente pas nécessairement la même quantité qu’une graduation verticale.','Lecture directe et lecture inverse')+'\n[IMAGE_2]\n\n';t=t.replace('::: retenir\n',addition+'::: retenir\n');corr['cours'][str(c['id'])]['2']={'fichier':'r30_cuve_corrige.png','alt':'Remplissage de 5 litres toutes les 2 minutes : lectures de 10 litres à 4 minutes et de 15 litres à 6 minutes.'}
        elif n==273:t=t.replace('## II. Deux droites sécantes',box('definition',r'Deux angles sont complémentaires quand la somme de leurs mesures est $90^\circ$. Par exemple, $34^\circ$ et $56^\circ$ sont complémentaires.','Angles complémentaires')+'\n## II. Deux droites sécantes')
        elif n==274:
            corr['cours'][str(c['id'])]['2']={'fichier':'r30_mediane_8_3.png','alt':'Triangle de base 8 m et hauteur 3 m, avec hauteur AH et médiane AM distinctes ; proportions exactes.'}
            addition=box('exemple',r'Dans un repère à même unité, prendre $A(0\,;0)$, $B(6\,;0)$ et $C(2\,;4)$. Les médiatrices de $[AB]$ et $[AC]$ se rencontrent en $O(3\,;1)$. Le cercle de centre $O$ passe par les trois sommets. La construction est visible en vert.','Construire le cercle circonscrit')+'\n[IMAGE_3]\n\n'
            t=t.replace('## IV. Calculer une aire',addition+'## IV. Calculer une aire');corr['cours'][str(c['id'])]['3']={'fichier':'r30_mediatrices_corrige.png','alt':'Médiatrices de AB et AC, centre O(3 ; 1) et cercle passant par A(0 ; 0), B(6 ; 0) et C(2 ; 4).'}
        elif n==275:
            t=t.replace(r'Pour la symétrie d’axe vertical passant par $O$, son image est $A\prime(-2\,;1)$',r'Pour la symétrie d’axe vertical dessinée, le point $A(3\,;1)$ a pour image $A\prime(-3\,;1)$')
            t=t.replace("Pour la symétrie d’axe vertical passant par $O$, son image est $A'(-2\\,;1)$", "Pour la symétrie d’axe vertical dessinée, le point $A(3\\,;1)$ a pour image $A'(-3\\,;1)$")
            corr['cours'][str(c['id'])]['1']={'fichier':'r30_motif_3_1.png','alt':'Symétrie d’axe vertical : triangle A(3 ; 1), B(5 ; 1), C(3 ; 3) et image exacte en vert.'}
            corr['cours'][str(c['id'])]['2']={'fichier':'r30_motif_2_1.png','alt':'Demi-tour de centre O : triangle A(2 ; 1), B(4 ; 1), C(2 ; 3) et image exacte en vert.'}
        (d/p.name).write_text(t,encoding='utf-8')
    used={v['fichier'].removesuffix('.png') for ids in corr.values() for positions in ids.values() for v in positions.values()}
    figures={name:code for name,code in figures.items() if name in used};assert used==set(figures),(n,used-set(figures))
    (d/'figures/figures.py').write_text('# -*- coding: utf-8 -*-\n"""Figures exactes de la révision du 30 octobre 2026."""\nFIGURES={\n'+''.join(repr(name)+': r"""\n'+code+'\n""",\n' for name,code in figures.items())+'}\n',encoding='utf-8')
    (d/'figures/correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    revision={'date':'2026-10-30','notion':n,'remplacements':[x for x in changes if not x.get('conserve')],'consolidations':[x for x in changes if x.get('conserve')],'tests':{str(eid):exprs for eid,exprs in TESTS.items() if NEW[eid]['notion']==n},'figures_uniques':len(figures)}
    (d/'revision_pedagogique.json').write_text(json.dumps(revision,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'geometrie-revision','maj':'2026-10-30'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(n,len(revision['remplacements']),'remplacements,',len(figures),'figures',flush=True)
