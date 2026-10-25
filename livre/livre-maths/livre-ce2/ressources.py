"""Bilans, correspondances et banque orale originale du CE2."""
from modele import E
import random

BILANS=[
('Bilan 1 - Les nombres et les calculs','P1-P2',[
 E('Écris 6 045 en lettres et décompose-le.','six-mille-quarante-cinq ; 6 045 = 6 000 + 40 + 5.'),
 E('Combien de centaines entières contient 4 873 ? Quel est le chiffre des centaines ?','48 centaines entières ; chiffre des centaines : 8.'),
 E('Range : 7 092 ; 7 290 ; 6 999 ; 7 029 ; 7 209.','6 999 < 7 029 < 7 092 < 7 209 < 7 290.'),
 E('Pose et calcule 3 786 + 2 457.','6 243.',('blank4',2),'3786+2457==6243'),
 E('Pose et calcule 5 004 - 2 678.','2 326.',None,'5004-2678==2326'),
 E('Calcule mentalement : 2 478 + 38 ; 4 205 - 29.','2 516 ; 4 176.',None,'2478+38==2516 and 4205-29==4176')]),
('Bilan 2 - Les produits et les fractions','P2-P3',[
 E('Complète : 7 × … = 56 ; 60 = 4 × … ; double de 75 = … .','8 ; 15 ; 150.',None,'7*8==56 and 4*15==60 and 2*75==150'),
 E('Calcule : 72 × 100 ; 8 × 40 ; 37 × 6.','7 200 ; 320 ; 222.',None,'72*100==7200 and 8*40==320 and 37*6==222'),
 E('Calcule 45 × 8 avec trois doubles.','45 → 90 → 180 → 360.',None,'45*8==360'),
 E('Complète : 3/4 = …/12 ; 2/3 = …/6. Compare 3/4 et 5/8.','9 ; 4 ; 3/4 = 6/8 > 5/8.',None,'F(3,4)==F(9,12) and F(2,3)==F(4,6) and F(3,4)>F(5,8)'),
 E('Écris 5 euros et 6 centimes avec une virgule. Puis calcule 5,06 € + 2,75 €.','5,06 € ; 7,81 €.',None,'506+275==781'),
 E('Lina a 185 cartes. Noé en a 38 de plus. Combien en ont-ils ensemble ?','Noé : 223 cartes ; ensemble : 408 cartes.',None,'185+(185+38)==408')]),
('Bilan 3 - Résoudre et mesurer en fractions','P3-P4',[
 E('Pose et calcule 248 × 6, puis 125 × 24.','1 488 ; 3 000.',None,'248*6==1488 and 125*24==3000'),
 E('On a 45 photos. Une page peut en contenir 8. Combien de pages faut-il ?','6 pages : 5 pages pleines et une page de 5 photos.',None,'45//8+1==6'),
 E('Un jeu coûte 18 €. Un coffret coûte 3 fois plus. Quel est le prix du coffret ?','54 €.',None,'18*3==54'),
 E('Avec 2 entrées, 3 plats et 2 desserts, combien de menus complets peut-on composer ?','12 menus ; on peut les vérifier dans un arbre.',None,'2*3*2==12'),
 E('Calcule : 1/2 + 3/8 ; 5/6 - 1/3.','7/8 ; 3/6, soit 1/2.',None,'F(1,2)+F(3,8)==F(7,8) and F(5,6)-F(1,3)==F(1,2)'),
 E('Sur ta feuille, trace 2 u + 3/4 u avec la règle en quarts des outils.','Avec l’unité u de 4 cm, le segment mesure 11 cm ; deux unités puis trois quarts.')]),
('Bilan 4 - Grandeurs et géométrie','P4',[
 E('Exprime 3 m et 4 cm en cm ; 2 kg et 50 g en g ; 4 L et 5 cL en cL.','304 cm ; 2 050 g ; 405 cL.'),
 E('Quel est le périmètre d’un rectangle de côtés 7 cm et 4 cm ?','7 + 4 + 7 + 4 = 22 cm.',None,'7+4+7+4==22'),
 E('Un objet coûte 12,75 €. Tu donnes 20 €. Pose le calcul pour chercher la monnaie.','20,00 € - 12,75 € = 7,25 €.',None,'2000-1275==725'),
 E('Sur une feuille séparée, construis un triangle rectangle avec des côtés de l’angle droit de 5 cm et 3 cm.','Deux côtés perpendiculaires de 5 cm et 3 cm ; troisième côté tracé ; angle droit codé.'),
 E('Un cercle a un rayon de 4 cm. Quelle est la longueur d’un diamètre ?','8 cm.',None,'2*4==8'),
 E('Décris une pyramide à base carrée : faces, arêtes et sommets.','5 faces, dont 1 carré et 4 triangles ; 8 arêtes ; 5 sommets.')]),
('Bilan 5 - Mon parcours de CE2','P5, en plusieurs séances',[
 E('Calcule 9 998 + 2, 4 005 - 1 768 et 348 × 23. Choisis des méthodes adaptées.','10 000 ; 2 237 ; 8 004.',None,'9998+2==10000 and 4005-1768==2237 and 348*23==8004'),
 E('Un gâteau perd 1/3 puis 1/4 de son tout. Quelle fraction reste ?','1/3 = 4/12 et 1/4 = 3/12 ; reste : 5/12.',None,'1-F(1,3)-F(1,4)==F(5,12)'),
 E('Lis cette heure pour l’après-midi, puis ajoute une durée de 35 minutes.','15 h 42 ; arrivée à 16 h 17.',('minuteclocks',[[15,42]]),'15*60+42+35==16*60+17'),
 E('On achète 3 objets à 8 € chacun et un objet à 5 €. On donne 40 €. Quelle monnaie reçoit-on ?','24 + 5 = 29 € d’achats ; monnaie : 11 €.',None,'40-(3*8+5)==11'),
 E('Dans le tableau, quel est le total du mardi ? Quel est l’écart avec lundi ?','Mardi : 18 + 7 = 25 ; lundi : 12 + 8 = 20 ; écart : 5.',('datatable',None),'18+7==25 and 25-(12+8)==5'),
 E('Complète la figure pour la rendre symétrique par rapport à l’axe.','Chaque sommet est reporté à la même distance de l’autre côté de l’axe ; les sommets sont reliés dans le même ordre.',('symmetry',['v',True]))])
]

COUVERTURE=[
('Lire, écrire et représenter les nombres jusqu’à 10 000','1'),
('Relations de numération, échanges et décompositions','2'),
('Comparer, encadrer, intercaler et graduer','3'),
('Addition posée ; termes et somme','4'),
('Soustraction posée ; termes et différence','5'),
('Ajouter 8, 9, 18, 19, 28, 29, 38, 39 ; retirer 9, 19, 29, 39','6'),
('Tables dans les deux sens ; facteurs, produit et multiples','7 ; outils'),
('Doubles, moitiés, multiples de 25 et décompositions de 60','8 ; outils'),
('Multiplier par 10, 100 et par des dizaines entières','9'),
('Produits d’un nombre de 11 à 99 par un chiffre','10'),
('Multiplier par 4 et par 8 avec des doubles','11'),
('Multiplication posée par un chiffre','12'),
('Multiplication posée d’un nombre à 2 ou 3 chiffres par 2 chiffres','13'),
('Sens de la division, symbole ÷ et relation avec ×','14'),
('Problèmes parties-tout, départ et comparaison additive','15'),
('Problèmes additifs en deux étapes, comparaison puis total','16'),
('Problèmes mixtes en deux ou trois étapes','17'),
('Comparaison multiplicative : fois plus, fois moins','18'),
('Produits cartésiens ; tableaux et arbres de choix','19'),
('Égalités entre fractions d’un même tout','20'),
('Comparer à dénominateur égal, numérateur égal ou avec un multiple','21'),
('Mesurer et tracer en unités entières et fractions d’unité','22 ; outils'),
('Additions et soustractions de fractions ; compléments au tout','23'),
('Longueurs : km, m, dm, cm et mm ; relations et estimations','24'),
('Contour, comparaison et mesure de périmètres','25'),
('Masses : g, kg, t ; relations, pesée et estimation','26'),
('Contenances : transvaser, estimer, convertir L, dL, cL','27'),
('Prix à virgule, euros et centimes ; rendre la monnaie','28'),
('Additions et soustractions posées de montants en euros','29'),
('Lire et placer les aiguilles à la minute ; notation sur 24 h','30'),
('Durées en h et min sur une journée ; départ et arrivée','31'),
('Polygones, propriétés, diagonales, angles droits, aigus, obtus','32'),
('Point, droite, segment, milieu, cercle, disque, rayon, diamètre','32, 33'),
('Construire des figures ; solides, éléments cachés et patrons de cube','33, 34 ; outils'),
('Axes de symétrie ; compléter sur quadrillage ou papier pointé','35 ; outils'),
('Enquêtes, caractères numériques, échelles et problèmes de données','36'),
]

def problemes_oraux():
    rng=random.Random(20261025);weeks=[]
    nouns=['cartes','perles','images','cubes','billes','crayons']
    for week in range(1,37):
        cap=3000 if week<=7 else 10000;q=[];noun=nouns[(week-1)%len(nouns)]
        def add(s,ans,expr,why,typ):
            assert eval(expr,{'__builtins__':{}},{})==ans,(week,s)
            q.append(dict(enonce=s,reponse=ans,expression=expr,calcul=why,type=typ))
        a=rng.randint(1100,cap//2);b=rng.randint(125,cap-a);t=a+b
        if week%3==0:add(f'Après avoir donné {b} {noun}, Lina en a encore {a}. Combien en avait-elle au départ ?',t,f'{a}+{b}',f'{a} + {b} = {t}','départ')
        elif week%3==1:add(f'Une réserve contient {a} {noun}. Elle en reçoit {b}. Quel est le nouveau total ?',t,f'{a}+{b}',f'{a} + {b} = {t}','tout')
        else:add(f'Il y a {t} {noun}, dont {a} dans une boîte. Les autres sont dans un sac. Combien sont dans le sac ?',b,f'{t}-{a}',f'{t} - {a} = {b}','partie')
        small=rng.randint(100,650);gap=rng.randint(18,250);large=small+gap
        add(f'Mila a {large} {noun}, soit {gap} de plus que Sami. Combien Sami en a-t-il ?',small,f'{large}-{gap}',f'{large} - {gap} = {small}','comparaison additive')
        a=rng.randint(40,180);gap=rng.randint(12,60)
        if week%2:add(f'Noé a {a} livres. La bibliothèque de Lina en a {gap} de plus. Combien de livres ont-ils ensemble ?',2*a+gap,f'{a}+({a}+{gap})',f'Lina : {a+gap} ; ensemble : {a} + {a+gap} = {2*a+gap}','comparaison et total')
        else:
            gap=min(gap,a-1);add(f'Lina a {a} livres, soit {gap} de plus que Noé. Combien de livres ont-ils ensemble ?',2*a-gap,f'{a}+({a}-{gap})',f'Noé : {a-gap} ; ensemble : {a} + {a-gap} = {2*a-gap}','comparaison et total')
        a=rng.randint(12,49) if week<22 else rng.randint(105,248);b=rng.randint(2,8) if week<22 else rng.randint(12,24)
        add(f'On prépare {b} paquets de {a} étiquettes chacun. Combien d’étiquettes en tout ?',a*b,f'{a}*{b}',f'{a} × {b} = {a*b}','produit')
        group=rng.randint(3,8);n=rng.randint(4,10);rest=rng.randint(1,group-1);t=group*n
        if week%3==0:add(f'On range {t+rest} photos sur des pages de {group} places. Combien de pages faut-il ?',n+1,f'({t+rest}+{group}-1)//{group}',f'{n} pages pleines et une page de {rest} photos','groupement avec reste')
        else:add(f'{t} {noun} sont partagés équitablement entre {group} enfants. Combien chacun en reçoit-il ?',n,f'{t}//{group}',f'{t} ÷ {group} = {n}','partage')
        price=rng.randint(125,1875);paid=2000;ans=paid-price
        add(f'Un achat coûte {price//100},{price%100:02} €. Tu donnes 20 €. Combien de centimes doit-on te rendre ?',ans,f'{paid}-{price}',f'{paid} - {price} = {ans} centimes','monnaie')
        if week%3==1:
            a=rng.randint(1,5);b=rng.randint(10,90);total=a*100+b;take=rng.randint(15,90)
            add(f'Un ruban mesure {a} m et {b} cm. On coupe {take} cm. Combien de centimètres restent ?',total-take,f'{total}-{take}',f'{total} - {take} = {total-take} cm','longueur')
        elif week%3==2:
            start=9*60+rng.randint(10,50);duration=rng.randint(35,95);end=start+duration
            add(f'Une visite commence à {start//60} h {start%60:02} et se termine à {end//60} h {end%60:02}. Combien de minutes dure-t-elle ?',duration,f'{end}-{start}',f'{end} - {start} = {duration} min après conversion en minutes','durée')
        else:
            litres=rng.randint(2,5);take=rng.randint(25,175)
            add(f'Un récipient contient {litres} L. On utilise {take} cL. Combien de centilitres restent ?',litres*100-take,f'{litres*100}-{take}',f'{litres*100} - {take} = {litres*100-take} cL','contenance')
        a=rng.randint(6,24);factor=rng.randint(2,5)
        add(f'Une petite boîte contient {a} {noun}. Une grande en contient {factor} fois autant. Combien dans la grande ?',a*factor,f'{a}*{factor}',f'{a} × {factor} = {a*factor}','comparaison multiplicative')
        a=rng.randint(2,4);b=rng.randint(2,5)
        if week>=15:
            z=2;add(f'Pour une tenue, on choisit un chapeau parmi {a}, un haut parmi {b} et un pantalon parmi {z}. Combien de tenues complètes différentes ?',a*b*z,f'{a}*{b}*{z}',f'{a} × {b} × {z} = {a*b*z}','trois choix')
        else:add(f'On choisit un pain parmi {a} et une garniture parmi {b}. Combien de sandwichs différents peut-on préparer ?',a*b,f'{a}*{b}',f'{a} × {b} = {a*b}','deux choix')
        a=rng.randint(2,4);b=rng.randint(3,8);z=rng.randint(2,9);paid=a*b+z+rng.randint(3,20);ans=paid-a*b-z
        add(f'Tu achètes {a} carnets à {b} € et un stylo à {z} €. Tu donnes {paid} €. Quelle monnaie reçoit-on ?',ans,f'{paid}-({a}*{b}+{z})',f'Carnets : {a*b} € ; achats : {a*b+z} € ; monnaie : {ans} €','trois étapes')
        assert len(q)==10
        weeks.append(dict(numero=week,plafond=cap,problemes=q))
    return weeks
