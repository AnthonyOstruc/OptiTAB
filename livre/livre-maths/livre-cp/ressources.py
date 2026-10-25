"""Bilans originaux et banque graduée de problèmes oraux."""
from modele import E
import random

BILANS=[
 ('Bilan 1 - Premiers nombres','Après les chapitres 1 à 8',[
 E('Compte les jetons et écris leur nombre.','8 jetons.',('tenframe',8)),
 E('Complète : 6 … 9 ; 10 … 7 ; 5 … 5. Utilise <, > ou =.','6 < 9 ; 10 > 7 ; 5 = 5.'),
 E('Calcule : 3 + 4 ; 8 - 2 ; 6 + … = 10.','7 ; 6 ; 4.',None,'3+4==7 and 8-2==6 and 6+4==10'),
 E('Écris 17 avec des dizaines et des unités.','1 dizaine et 7 unités ; 17 = 10 + 7.'),
 E('Dans A B A B A B…, quelle est la 7e lettre ?','A.'),
 E('Il y a 9 cubes. On en range 4. Combien sont encore sur la table ?','9 - 4 = 5 cubes.',None,'9-4==5')]),
 ('Bilan 2 - Jusqu’à 59','Après les chapitres 9 à 12 et les premières manipulations de mesures',[
 E('Écris le nombre représenté, puis écris-le en lettres.','43, quarante-trois.',('base10',43)),
 E('Range du plus petit au plus grand : 35 ; 53 ; 29 ; 40 ; 18.','18 < 29 < 35 < 40 < 53.'),
 E('Calcule : 34 + 10 ; 52 - 20 ; 39 + 1.','44 ; 32 ; 40.',None,'34+10==44 and 52-20==32 and 39+1==40'),
 E('Donne le double de 8 et la moitié de 20.','16 ; 10.'),
 E('Mesure ce segment avec la règle représentée.','6 cm.',('ruler',[0,6])),
 E('Un objet coûte 8 €. Tu donnes 10 €. Quelle monnaie reçoit-on ?','10 - 8 = 2 €.',None,'10-8==2')]),
 ('Bilan 3 - Jusqu’à 100','Après les chapitres 13 à 19 et 24',[
 E('Écris : soixante-dix-sept ; quatre-vingt-quatre ; cent.','77 ; 84 ; 100.'),
 E('Calcule : 38 + 6 ; 45 + 23 ; 60 - 7.','44 ; 68 ; 53.',None,'38+6==44 and 45+23==68 and 60-7==53'),
 E('Il y a 24 perles en tout, dont 9 bleues. Les autres sont vertes. Combien sont vertes ?','24 - 9 = 15 perles vertes.',('bar',[24,9,'?']),'24-9==15'),
 E('Il y a 4 paniers de 5 balles. Combien de balles en tout ?','5 + 5 + 5 + 5 = 20 balles.',None,'4*5==20'),
 E('18 cartes sont partagées également entre 3 enfants. Combien chacun reçoit-il ?','6 cartes chacun.',None,'18//3==6'),
 E('Lis l’heure, puis dis où se trouve la grande aiguille.','10 heures ; la grande aiguille est sur 12.',('clocks',[10]))]),
 ('Bilan 4 - Chercher et construire','Après les chapitres 20 et 25 à 30',[
 E('Il y a 26 enfants. 8 sortent, puis 5 entrent. Combien sont là à la fin ?','26 - 8 = 18 ; 18 + 5 = 23 enfants.',None,'26-8+5==23'),
 E('Pose et calcule : 37 + 28.','7 + 8 = 15 ; 3 + 2 + 1 = 6 dizaines. Résultat : 65.',('columnblank',2),'37+28==65'),
 E('Trace un rectangle de 4 carreaux sur 3 carreaux.','Deux côtés de 4 et deux côtés de 3 carreaux, sur les lignes du quadrillage.',('gridblank',None)),
 E('Décris les faces d’un cube.','Le cube a 6 faces carrées.'),
 E('Le pion regarde vers le haut. Il tourne à droite puis avance de 2 cases. Décris son déplacement.','Il se déplace de deux cases vers la droite du plan.'),
 E('Interroge 6 personnes sur leur choix entre deux jeux. Note les réponses puis construis deux barres.','Une réponse par personne ; total de 6 votes ; un carreau par personne ; noms des choix et titre.')]),
 ('Bilan 5 - Mon parcours de CP','Fin d’année, en plusieurs séances',[
 E('Décompose 92. Encadre-le entre deux dizaines. Écris 48 en lettres.','92 = 90 + 2 ; 90 < 92 < 100 ; quarante-huit.'),
 E('Calcule : 67 + 9 ; 80 - 6 ; 43 + 28. Donne la moitié de 46.','76 ; 74 ; 71 ; 23.',None,'67+9==76 and 80-6==74 and 43+28==71 and 46//2==23'),
 E('J’avais des cartes. J’en donne 7 et il m’en reste 25. Combien en avais-je ?','25 + 7 = 32 cartes.',('bar',[32,25,'?']),'25+7==32'),
 E('Avec 24 jetons, fais des paquets de 4. Combien de paquets ?','6 paquets de 4.',None,'24//4==6'),
 E('Un cahier coûte 6 €. Tu donnes 10 €. Quelle monnaie reçoit-on ? Trace ensuite un segment de 5 cm sur ta feuille.','On rend 4 €. Le segment tracé doit mesurer 5 cm.',None,'10-6==4'),
 E('Nomme une forme à 3 côtés, un solide à 6 faces carrées et montre 7 heures sur une horloge.','Triangle ; cube ; petite aiguille sur 7 et grande aiguille sur 12.')])
]

def problemes_oraux():
    rng=random.Random(20261023);semaines=[]
    themes=[('perles','une boîte'),('cartes','une enveloppe'),('crayons','un pot'),('cubes','un bac'),('images','un album'),('billes','un sac')]
    for week in range(1,37):
        cap=5 if week==1 else 8 if week==2 else 10 if week<=4 else 20 if week<=7 else 59 if week<=14 else 100
        noun,where=themes[(week-1)%len(themes)]
        def pair():
            a=rng.randint(2,max(2,cap//2));b=rng.randint(1,max(1,cap-a));return a,b,a+b
        a,b,total=pair()
        q=[]
        def add(s,ans,expr,why):
            assert eval(expr,{'__builtins__':{}},{})==ans,(week,s)
            assert 0<=ans<=100
            q.append(dict(enonce=s,reponse=ans,calcul=why,expression=expr))
        add(f'Lina a {a} {noun}. Noé lui donne {b} {noun}. Combien Lina en a-t-elle maintenant ?',total,f'{a}+{b}',f'{a} + {b} = {total}')
        a,b,total=pair()
        add(f'Il y a {total} {noun} dans {where}. On en prend {b}. Combien en reste-t-il ?',a,f'{total}-{b}',f'{total} - {b} = {a}')
        a,b,total=pair()
        add(f'Mila veut {total} {noun}. Elle en a déjà {a}. Combien lui en manque-t-il ?',b,f'{total}-{a}',f'{total} - {a} = {b}')
        a,b,total=pair()
        add(f'Sami donne {a} {noun}. Il lui en reste {b}. Combien en avait-il avant ?',total,f'{a}+{b}',f'{a} + {b} = {total}')
        a,b,total=pair()
        add(f'Aya reçoit {b} {noun}. Elle en a maintenant {total}. Combien en avait-elle avant ?',a,f'{total}-{b}',f'{total} - {b} = {a}')
        a,b,total=pair()
        add(f'Il y a {total} {noun} en tout : {b} sont sur la table et les autres dans une boîte. Combien sont dans la boîte ?',a,f'{total}-{b}',f'{total} - {b} = {a}')
        if week>=15:
            g=rng.randint(2,5);k=rng.randint(2,30//g)
            add(f'Il y a {g} boîtes. Chaque boîte contient {k} {noun}. Combien y en a-t-il en tout ?',g*k,f'{g}*{k}', ' + '.join([str(k)]*g)+f' = {g*k}')
        else:
            k=min(a,cap//3,10);g=3
            add(f'Trois boîtes contiennent chacune {k} {noun}. Combien y en a-t-il dans les trois boîtes ?',g*k,f'{g}*{k}',f'{k} + {k} + {k} = {g*k}')
        if week>=18:
            g=rng.randint(2,4);k=rng.randint(2,30//g);t=g*k
            add(f'{g} enfants se partagent équitablement {t} {noun}. Combien chacun reçoit-il ?',k,f'{t}//{g}',f'{g} parts égales de {k}')
        else:
            t=rng.randint(2,cap);taken=rng.randint(1,t-1)
            add(f'Il y avait {t} oiseaux dans un arbre. Il en reste {taken}. Combien d’oiseaux sont partis ?',t-taken,f'{t}-{taken}',f'{t} - {taken} = {t-taken}')
        if week>=20:
            k=rng.randint(2,5);g=rng.randint(2,30//k);t=k*g
            add(f'On range {t} {noun} dans des sachets de {k}. Combien de sachets peut-on remplir ?',g,f'{t}//{k}',f'{g} sachets de {k}')
        else:
            n=rng.randint(2,cap);given=rng.randint(1,n-1)
            add(f'Il faut {n} chaises pour les enfants. {given} chaises sont prêtes. Combien faut-il encore en apporter ?',n-given,f'{n}-{given}',f'{n} - {given} = {n-given}')
        if week>=22:
            start=rng.randint(12,25);out=rng.randint(2,8);inc=rng.randint(1,min(5,30-start+out));ans=start-out+inc
            add(f'Il y a {start} enfants. {out} sortent, puis {inc} entrent. Combien d’enfants sont là maintenant ?',ans,f'{start}-{out}+{inc}',f'{start} - {out} = {start-out} ; {start-out} + {inc} = {ans}')
        else:
            a,b,total=pair()
            add(f'Une collection contient {total} {noun}. On cache {a} {noun} sous une feuille. Combien restent visibles ?',b,f'{total}-{a}',f'{total} - {a} = {b}')
        assert len(q)==10
        semaines.append(dict(numero=week,plafond=cap,problemes=q))
    return semaines

COUVERTURE=[
 ('Dénombrer, représenter, lire et écrire jusqu’à 100','1, 2, 7, 9, 13'),
 ('Comparer, ranger, encadrer, placer sur une graduation','3, 10, 13'),
 ('Rangs jusqu’à vingtième et motifs organisés','8'),
 ('Sens de +, - et = ; liens entre les opérations','4, 5, 17'),
 ('Faits d’addition, compléments, doubles, moitiés','6, 11, 14 ; outils'),
 ('Calcul mental : 1, 2, dizaines, petits ajouts et + 9','12, 14'),
 ('Addition mentale, moitié d’un nombre pair','11, 15'),
 ('Retrait depuis une dizaine et échanges de dizaines','16'),
 ('Problèmes parties-tout, recherche du départ, deux étapes','17, 20'),
 ('Groupes identiques, partage et nombre de paquets','18, 19'),
 ('Moitié, demi et quart dans des manipulations','19'),
 ('Addition en colonnes de deux ou trois nombres','30'),
 ('Monnaie en euros entiers, achats et monnaie rendue','21'),
 ('Longueurs : comparaison, règle, cm, m et 1 m = 100 cm','22'),
 ('Masses : soupeser, balance, classement','23'),
 ('Heures entières, aiguilles et moments de la journée','24'),
 ('Formes, côtés, sommets, alignements et règle','25'),
 ('Reproduire, compléter, construire sur quadrillage','26'),
 ('Solides usuels, faces du cube et du pavé, assemblages','27'),
 ('Positions, plan de classe, déplacements et instructions','28'),
 ('Recueillir des données, tableau, barres, double entrée','29'),
]
