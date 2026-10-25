from modele import E
import random

BILANS=[
 ('Bilan 1 - Nombres et additions','P1-P2',[
 E('Écris le nombre représenté, puis écris-le en lettres.','243 ; deux-cent-quarante-trois.',('hundreds',243)),
 E('Décompose 507. Écris combien il contient de dizaines entières.','507 = 500 + 7. Il contient 50 dizaines entières et 7 unités.'),
 E('Range : 381 ; 318 ; 401 ; 380 ; 299.','299 < 318 < 380 < 381 < 401.'),
 E('Calcule mentalement : 234 + 80 ; 375 + 19.','314 ; 394.',None,'234+80==314 and 375+19==394'),
 E('Pose et calcule 286 + 157.','443.',('column3blank',2),'286+157==443'),
 E('Tu es 42e dans une file. Combien de personnes sont devant toi ?','41 personnes.')]),
 ('Bilan 2 - Calculs et monnaie','P2-P3',[
 E('Calcule mentalement : 462 - 9 ; 603 - 7.','453 ; 596.',None,'462-9==453 and 603-7==596'),
 E('Pose et calcule 502 - 168.','334. Vérification : 334 + 168 = 502.',('column3blank',-2),'502-168==334'),
 E('Calcule : 7 × 8 ; 6 × 9 ; 8 × 4. Complète : 5 × … = 45.','56 ; 54 ; 32 ; 9.',None,'7*8==56 and 6*9==54 and 8*4==32 and 5*9==45'),
 E('Calcule : 37 × 10 ; 14 × 6.','370 ; 84.',None,'37*10==370 and 14*6==84'),
 E('Donne la moitié de 470 et le double de 250.','235 ; 500.',None,'470//2==235 and 2*250==500'),
 E('Écris 3 € et 5 centimes avec une virgule. Compare ce prix à 3,50 €.','3,05 €. C’est moins que 3,50 €.')]),
 ('Bilan 3 - Fractions et problèmes','P3-P4',[
 E('Écris la fraction coloriée et nomme son numérateur.','3/5 ; numérateur 3.',('fracbar',[3,5,False])),
 E('Compare, pour un même tout : 1/3 et 1/6 ; 2/8 et 5/8.','1/3 > 1/6 ; 2/8 < 5/8.',None,'F(1,3)>F(1,6) and F(2,8)<F(5,8)'),
 E('Calcule : 2/5 + 1/5 ; 5/8 - 2/8. Complète : 3/10 + … = 1.','3/5 ; 3/8 ; 7/10.',None,'F(2,5)+F(1,5)==F(3,5) and F(5,8)-F(2,8)==F(3,8) and F(3,10)+F(7,10)==1'),
 E('Lina a donné 76 cartes. Il lui en reste 185. Combien en avait-elle au départ ?','185 + 76 = 261 cartes.',None,'185+76==261'),
 E('Lina a 138 perles, soit 45 de plus que Noé. Combien Noé en a-t-il ?','138 - 45 = 93 perles.',None,'138-45==93'),
 E('25 photos sont rangées sur des pages de 10 places. Combien de pages faut-il ?','3 pages : deux pleines et une avec 5 photos.')]),
 ('Bilan 4 - Mesurer et construire','P4',[
 E('Exprime 1 m et 35 cm en cm. Combien de grammes valent 1 kg ?','135 cm ; 1 000 g.'),
 E('Tu achètes 4 cahiers à 3 € chacun. Tu donnes 20 €. Quelle monnaie reçoit-on ?','4 × 3 = 12 € ; 20 - 12 = 8 €.',None,'20-4*3==8'),
 E('Lis l’heure pour l’après-midi.','15 h 45, ou quatre heures moins le quart de l’après-midi.',('timeclocks',[[15,45]])),
 E('Une activité va de 8 h 30 à 9 h 15. Quelle est sa durée ?','30 min puis 15 min : 45 min.',None,'30+15==45'),
 E('Construis sur ta feuille un rectangle de 6 cm sur 3 cm. Code les angles droits.','Quatre angles droits ; deux côtés de 6 cm et deux de 3 cm.'),
 E('Décris les faces et les sommets d’une pyramide à base carrée.','5 faces : 1 carré et 4 triangles ; 5 sommets.')]),
 ('Bilan 5 - Mon parcours de CE1','P5, en plusieurs séances',[
 E('Écris en lettres 708 et encadre-le entre deux dizaines consécutives.','sept-cent-huit ; 700 < 708 < 710.'),
 E('Calcule : 528 + 29 ; 704 - 186 ; 17 × 4 ; moitié de 350.','557 ; 518 ; 68 ; 175.',None,'528+29==557 and 704-186==518 and 17*4==68 and 350//2==175'),
 E('Colorie trois quarts de la bande. Quelle fraction manque pour avoir le tout ?','3 parts sur 4 ; il manque 1/4.',('fracbar',[0,4,False]),'1-F(3,4)==F(1,4)'),
 E('Un objet coûte 2,65 € et un autre 1,35 €. Tu donnes 5 €. Quelle monnaie reçoit-on ?','265 + 135 = 400 centimes ; 500 - 400 = 100 centimes, soit 1 €.',None,'265+135==400 and 500-400==100'),
 E('Dans le tableau, combien viennent à vélo mardi ? Combien viennent à pied et à vélo mardi en tout ?','7 ; 10 + 7 = 17.',('doubledata',None),'10+7==17'),
 E('Trace un cercle de centre O passant par A sur ta feuille, puis code un petit trajet avec un départ et une orientation précis.','Le cercle garde son centre et son ouverture ; le trajet peut être suivi sans information manquante.')])
]

COUVERTURE=[
 ('Lire, écrire, dénombrer jusqu’à 1 000','1 ; outils nombres'),
 ('Échanger unités, dizaines et centaines ; décomposer','2'),
 ('Comparer, encadrer, ranger et lire une graduation','3'),
 ('Rangs jusqu’à centième ; motifs et suites évolutives','4'),
 ('Faits d’addition ; calculs mentaux et compensations','5, 7 ; outils'),
 ('Addition et soustraction en colonnes','6, 8'),
 ('Sens de ×, commutativité et parité','9'),
 ('Tables de multiplication de 0 à 10','10, 11 ; outils tables'),
 ('Multiplier par 10 ; produits avec un facteur de 11 à 19','12'),
 ('Doubles, moitiés et multiples de 25','13 ; outils'),
 ('Problèmes parties-tout, départ et comparaison','14, 15'),
 ('Problèmes en deux étapes, dont problèmes mixtes','16'),
 ('Groupements, partages et interprétation d’un reste','17'),
 ('Fractions d’un tout : lire et représenter','18'),
 ('Numérateur, dénominateur et comparaisons de fractions','19'),
 ('Calculs sur fractions de même dénominateur ; complément','20'),
 ('Longueurs : cm, m, km, mesure et estimation','21'),
 ('Masses : g, kg, pesée, comparaison et estimation','22'),
 ('Euros, centimes, écriture à virgule, achats et monnaie','23'),
 ('Heures, demi-heures, quarts et notation sur 24 heures','24'),
 ('Durées en h et min ; problèmes sur une même journée','25'),
 ('Formes, angles droits, aigus, obtus et codage','26'),
 ('Alignements, milieu par pliage, cercle et compas','27'),
 ('Constructions sur papier quadrillé, pointé et uni','28 ; outils'),
 ('Solides, faces, arêtes, sommets et assemblages','29'),
 ('Positions, plans et instructions de déplacement','30'),
 ('Recueil de données et construction de graphiques','31'),
 ('Lecture de tableaux, double entrée et graphiques','32'),
]

def problemes_oraux():
    rng=random.Random(20261024);weeks=[]
    nouns=['cartes','perles','crayons','cubes','images','billes']
    for week in range(1,37):
        cap=200 if week<=2 else 500 if week<=7 else 1000;q=[];noun=nouns[(week-1)%6]
        def pair(limit=cap):
            a=rng.randint(20,max(20,limit//2));b=rng.randint(5,max(5,limit-a));return a,b,a+b
        def add(s,ans,expr,why,typ='additif'):
            assert eval(expr,{'__builtins__':{}},{})==ans,(week,s)
            q.append(dict(enonce=s,reponse=ans,expression=expr,calcul=why,type=typ))
        a,b,t=pair();add(f'Lina a {a} {noun}. Elle en reçoit {b}. Combien en a-t-elle maintenant ?',t,f'{a}+{b}',f'{a} + {b} = {t}')
        a,b,t=pair();add(f'Une réserve contient {t} {noun}. On en prend {b}. Combien restent dans la réserve ?',a,f'{t}-{b}',f'{t} - {b} = {a}')
        a,b,t=pair();add(f'Il y a {t} {noun} en tout. {a} sont sur la table et les autres dans une boîte. Combien sont dans la boîte ?',b,f'{t}-{a}',f'{t} - {a} = {b}')
        a,b,t=pair();add(f'Sami donne {b} {noun}. Il lui en reste {a}. Combien en avait-il avant ?',t,f'{a}+{b}',f'{a} + {b} = {t}')
        a,b,t=pair();add(f'Mila possède {t} {noun}, soit {b} de plus que Noé. Combien Noé en possède-t-il ?',a,f'{t}-{b}',f'{t} - {b} = {a}')
        start=rng.randint(15,30) if week<=2 else rng.randint(70,max(70,cap//2));inc=rng.randint(5,20);out=rng.randint(5,min(start,35));ans=start+inc-out
        add(f'Il y a {start} livres. On apporte {inc} livres, puis on en prête {out}. Combien de livres restent ?',ans,f'{start}+{inc}-{out}',f'{start} + {inc} = {start+inc} ; {start+inc} - {out} = {ans}','deux étapes')
        g=rng.randint(2,5 if week<=6 else 10);k=rng.randint(2,10) if week<=14 else rng.randint(11,19)
        add(f'On prépare {g} boîtes contenant chacune {k} {noun}. Combien d’objets y a-t-il au total ?',g*k,f'{g}*{k}',f'{g} × {k} = {g*k}','produit')
        g=rng.randint(2,5 if week<=6 else 10);k=rng.randint(2,10);t=g*k
        if week>=20 and week%4==0:
            rest=rng.randint(1,g-1);t+=rest
            add(f'On range {t} photos sur des pages de {g} places. Combien de pages faut-il pour toutes les ranger ?',k+1,f'{k}+1',f'{k} pages pleines et une page avec {rest} photos','groupement avec reste')
        else:add(f'{g} enfants se partagent équitablement {t} {noun}. Combien chacun reçoit-il ?',k,f'{t}//{g}',f'{g} parts de {k}','partage')
        if week>=8:
            price=rng.randrange(105,480,5);paid=500;ans=paid-price
            add(f'Un objet coûte {price//100} € et {price%100:02} centimes. Tu donnes 5 €. Combien de centimes doit-on rendre ?',ans,f'500-{price}',f'500 - {price} = {ans} centimes','monnaie')
        else:
            a,b,t=pair(100);add(f'Un ruban mesure {t} cm. On coupe {b} cm. Combien de centimètres restent ?',a,f'{t}-{b}',f'{t} - {b} = {a} cm','longueur')
        if week>=12:
            g=rng.randint(2,8);price=rng.randint(2,5);paid=g*price+rng.randint(2,20);ans=paid-g*price
            add(f'Tu achètes {g} cahiers à {price} € chacun. Tu donnes {paid} €. Quelle somme doit-on rendre ?',ans,f'{paid}-{g}*{price}',f'{g} × {price} = {g*price} ; {paid} - {g*price} = {ans} €','mixte')
        else:
            a,b,t=pair();add(f'Lina reçoit {b} {noun} et en a maintenant {t}. Combien en avait-elle avant ?',a,f'{t}-{b}',f'{t} - {b} = {a}')
        assert len(q)==10
        weeks.append(dict(numero=week,plafond=cap,problemes=q))
    return weeks
