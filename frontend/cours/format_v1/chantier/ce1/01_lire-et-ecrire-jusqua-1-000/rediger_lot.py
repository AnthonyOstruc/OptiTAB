# -*- coding: utf-8 -*-
"""Rédaction locale du lot nombres, problèmes, fractions et données CE1.

Les sources locales restent en lecture seule. Pas de compilation dans ce script.
"""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(R/'_coordination'))
from commun_redaction import q,ex,write,table

def Q(p,m,r,a):return q(p,m,r,a)
def E(t,intro,*qs):return ex(t,intro,list(qs))
def calc(p,expr,value,unit='',m='Effectue le calcul en séparant les centaines, les dizaines et les unités.',why=''):
    return Q(p,m,why+'\n\n$'+expr+'='+str(value)+'$.',f'${value}$'+(' '+unit if unit else '')+'.')
def parts(v):return v//100,(v//10)%10,v%10
def dec(v):
    c,d,u=parts(v)
    return f'${v}={c*100}+{d*10}+{u}$'
def digits(v):
    c,d,u=parts(v)
    return f'{c} centaines, {d} dizaines et {u} unités'
def number_questions(v,words):
    c,d,u=parts(v)
    return [Q('Écris le nombre en chiffres et en lettres.','Réunis les centaines, les dizaines et les unités avant de lire le nombre.',f'{c} centaines valent {c*100}, {d} dizaines valent {d*10} et les unités valent {u}. '+dec(v)+'.',f'${v}$ : {words}.'),
    Q('Quelle quantité le chiffre des centaines représente-t-il ?','Une centaine représente cent objets.',f'Le chiffre {c} occupe le rang des centaines : ${c}\\times100={c*100}$.',f'${c*100}$ unités.'),
    Q('Décompose le nombre en centaines, dizaines et unités.','Garde les rangs dans l’ordre ; un zéro signifie que ce rang est vide.',f'On lit {digits(v)}. La somme doit redonner le nombre.',dec(v)+'.'),
    Q('Écris le nombre obtenu en ajoutant une dizaine.','Ajoute dix unités ; échange dix dizaines contre une centaine si nécessaire.',f'Une dizaine vaut 10 unités. ${v}+10={v+10}$.',f'${v+10}$.'),
    Q('Écris les deux nombres qui encadrent immédiatement le nombre de départ.','Retire une unité pour le précédent ; ajoute une unité pour le suivant.',f'${v}-1={v-1}$ et ${v}+1={v+1}$. Les trois nombres se suivent.',f'${v-1}<{v}<{v+1}$.')]

def nombres():
    its=[]
    its.append(ex('Des plaques et des barres','Le matériel contient 3 plaques de 100, 2 barres de 10 et 5 cubes unités.\n\n[IMAGE_1]',number_questions(325,'trois-cent-vingt-cinq')))
    qs=number_questions(107,'cent-sept')
    qs[0]=Q('Écris en chiffres : cent-sept ; quatre-cent-soixante ; neuf-cent-deux.','Traduis les mots en centaines, dizaines et unités, en gardant les rangs vides.', 'Cent-sept : 100 et 7, sans dizaine. Quatre-cent-soixante : 400 et 60, sans unité. Neuf-cent-deux : 900 et 2, sans dizaine.','$107$ ; $460$ ; $902$.')
    its.append(ex('Les rangs que l’on n’entend pas','On étudie cent-sept, quatre-cent-soixante et neuf-cent-deux. Les questions 2 à 5 portent sur cent-sept.',qs))
    qs=number_questions(508,'cinq-cent-huit')
    qs[0]=Q('Lis les nombres 180, 508, 790 et 1 000.','Lis les centaines puis la partie qui reste ; 1 000 se lit mille.','180 contient 100 et 80 ; 508 contient 500 et 8 ; 790 contient 700 et 90. Dix centaines forment 1 000.','180 : cent-quatre-vingts ; 508 : cinq-cent-huit ; 790 : sept-cent-quatre-vingt-dix ; 1 000 : mille.')
    its.append(ex('Lire sans oublier le zéro','On lit 180, 508, 790 et 1 000. Les questions 2 à 5 portent sur 508.',qs))
    qs=number_questions(215,'deux-cent-quinze')
    qs[0]=Q('Écris en lettres 215, 381 et 600.','Lis d’abord les centaines ; termine par les dizaines et unités.','215 contient 200 et 15 ; 381 contient 300 et 81 ; 600 contient six centaines sans autre unité.','deux-cent-quinze ; trois-cent-quatre-vingt-un ; six-cents.')
    its.append(ex('Des chiffres aux mots','On écrit 215, 381 et 600. Les questions 2 à 5 portent sur 215.',qs))
    its.append(E('Passer une centaine','Voici une suite de nombres qui avancent d’une unité : 397 ; 398 ; … ; … ; 401.',
    Q('Quels nombres manquent ?','Ajoute une unité à chaque fois ; après 399, échange dix dizaines contre une centaine.','$398+1=399$ puis $399+1=400$.','$399$ et $400$.'),
    Q('Quel nombre est juste avant 397 ?','Recule d’une unité.','$397-1=396$.','$396$.'),
    Q('Décompose 399.','Lis chaque rang.','Le 3 représente 300, le premier 9 représente 90 et le dernier 9 représente 9.','$399=300+90+9$.'),
    Q('Combien de centaines et d’unités isolées contient 400 ?','Regroupe les 400 unités en plaques de cent.','$4\\times100=400$ ; aucune dizaine ni unité ne reste.','4 centaines et 0 unité isolée.'),
    Q('Continue la suite de deux nombres après 401.','Ajoute encore une unité à chaque étape.','$401+1=402$ ; $402+1=403$.','$402$ ; $403$.')))
    its.append(E('Avancer de cent en cent','La suite commence par 250 ; 350 ; … ; … ; …',
    Q('Quel est le pas de cette suite ?','Cherche ce qui est ajouté entre les deux premiers nombres.','$350-250=100$.','On ajoute $100$.'),
    Q('Complète les trois places vides.','Ajoute une centaine à chaque nombre.','$350+100=450$, $450+100=550$, $550+100=650$.','$450$ ; $550$ ; $650$.'),
    Q('Quels chiffres ne changent pas dans cette suite ?','Compare les rangs des cinq nombres.','250, 350, 450, 550 et 650 ont tous 5 dizaines et 0 unité.','Le chiffre des dizaines reste 5 ; celui des unités reste 0.'),
    Q('Quel nombre précède 250 avec le même pas ?','Retire une centaine.','$250-100=150$.','$150$.'),
    Q('Combien d’ajouts de 100 séparent 250 et 650 ?','Compte les passages : 250 vers 350, puis 450, 550, 650.','Il y a quatre passages ; $250+4\\times100=650$.','4 ajouts de 100.')))
    qs=number_questions(427,'quatre-cent-vingt-sept');qs[0]=Q('Combien de cubes contient le stock ?','Ajoute les quantités contenues dans les boîtes et les cubes isolés.','Les grandes boîtes contiennent $4\\times100=400$ cubes. Les petites contiennent $2\\times10=20$ cubes. $400+20+7=427$.','$427$ cubes.')
    its.append(ex('Un stock bien rangé','Un stock contient 4 boîtes de 100 cubes, 2 boîtes de 10 et 7 cubes isolés.',qs))
    its.append(E('Construire mille','Tu prépares des plaques de 100 cubes pour atteindre 1 000 cubes.',
    Q('Combien de plaques faut-il ?','Compte de cent en cent jusqu’à mille.','100, 200, 300, 400, 500, 600, 700, 800, 900, 1 000 : dix plaques.','10 plaques de 100.'),
    calc('Combien de cubes contiennent 9 plaques ?',r'9\times100',900,'cubes',m='Une plaque contient 100 cubes ; répète cette quantité neuf fois.'),
    calc('Combien manque-t-il alors pour obtenir 1 000 cubes ?','1000-900',100,'cubes',m='Cherche le complément de 900 à 1 000.'),
    Q('Combien de barres de 10 remplace une plaque ?','Dix dizaines forment une centaine.','$10\\times10=100$.','10 barres de 10.'),
    Q('Avec 8 plaques et 20 barres de 10, atteint-on 1 000 cubes ?','Échange les vingt dizaines contre deux centaines.','$8\\times100=800$, $20\\times10=200$ et $800+200=1000$.','Oui : $1000$ cubes.')))
    qs=number_questions(405,'quatre-cent-cinq');qs[0]=Q('Lina écrit 45 pour quatre-cent-cinq. Corrige son écriture.','Place 4 au rang des centaines et garde la place vide des dizaines.','45 signifie 4 dizaines et 5 unités, soit 40 et 5. Ici, on veut 400 et 5 : il faut écrire un zéro entre 4 et 5.','$405$ : quatre-cent-cinq.')
    its.append(ex('Le zéro garde une place','Lina écrit 45 pour quatre-cent-cinq. On étudie le nombre qu’elle voulait écrire.',qs))
    write(1,its)

def decomposition():
    scenarios=[(416,4,1,6),(627,5,12,7),(280,0,28,0),(305,3,0,5),(789,7,8,9),(583,5,8,3),(236,2,3,6),(297,2,8,17),(407,4,0,7)]
    originals=[
    ('Les rangs de 416','Le tableau contient 4 centaines, 1 dizaine et 6 unités.\n\n[IMAGE_1]','Décompose 416 en centaines, dizaines et unités.','$416=400+10+6$.'),
    ('Douze dizaines à échanger','Tu as 5 centaines, 12 dizaines et 7 unités.','Quel nombre as-tu ?','$500+120+7=627$.'),
    ('Des unités aux dizaines','Tu disposes de 28 dizaines ; tu étudies aussi 6 centaines.','Complète : 28 dizaines = … unités ; 6 centaines = … dizaines.','$28\\times10=280$ unités ; $6\\times10=60$ dizaines.'),
    ('Deux écritures de 305','Tu veux représenter 305 avec des centaines, dizaines et unités.','Propose deux représentations de 305.','3 centaines et 5 unités ; ou 30 dizaines et 5 unités.'),
    ('Recomposer des quantités','Voici trois sommes : 700 + 80 + 9 ; 400 + 6 ; 90 + 500. Les questions suivantes portent sur la première.','Recompose les trois nombres.','$700+80+9=789$ ; $400+6=406$ ; $90+500=590$.'),
    ('Chiffre et nombre de dizaines','On étudie 583.','Quel est le chiffre des dizaines ? Combien y a-t-il de dizaines entières ?','Le chiffre est 8 ; il y a 58 dizaines entières et 3 unités.'),
    ('Commander 236 timbres','Les timbres sont vendus par plaques de 100, carnets de 10 ou à l’unité.','Trouve trois commandes pour avoir exactement 236 timbres.','2 plaques, 3 carnets et 6 unités ; 1 plaque, 13 carnets et 6 unités ; 23 carnets et 6 unités.'),
    ('Dix-sept unités à regrouper','Une collection contient 2 centaines, 8 dizaines et 17 unités.','Regroupe la collection et écris son nombre.','$200+80+17=297$ : 2 centaines, 9 dizaines et 7 unités.'),
    ('Le quatre de 407','Noé dit : « Dans 407, le 4 vaut 4. »','Que représente le chiffre 4 ?','4 centaines, donc $400$ unités.')]
    its=[]
    for (v,c,d,u),(title,intro,p,a) in zip(scenarios,originals):
        cc,dd,uu=parts(v)
        reason=f'Chaque centaine vaut 100 et chaque dizaine vaut 10. ${c}\\times100+{d}\\times10+{u}={v}$. '
        if v==583:reason+='Les 5 centaines donnent 50 dizaines ; avec 8 dizaines, cela donne 58 dizaines et 3 unités.'
        if v==236:reason+='Une plaque se remplace par 10 carnets : les 3 carnets deviennent 13, puis 23 si on échange les deux plaques.'
        its.append(E(title,intro,Q(p,'Échange les groupes de dix sans modifier la quantité totale.',reason,a),
        Q(f'Quelle quantité représentent ensemble les centaines et les unités de {v}, sans les dizaines ?','Garde la valeur des centaines et celle des unités, puis réunis-les.',f'Dans {v}, les centaines valent {cc*100}, les unités valent {uu} et les dizaines valent {dd*10}. Sans ces dizaines, il reste ${cc*100}+{uu}={cc*100+uu}$.',f'${cc*100+uu}$ unités.'),
        Q('Remplace une centaine par des dizaines. Donne une autre représentation.','Une centaine s’échange contre dix dizaines.',f'On garde {cc-1} centaines, on ajoute 10 aux {dd} dizaines, et on garde {uu} unités.',f'{cc-1} centaines, {dd+10} dizaines et {uu} unités.'),
        Q('Combien de dizaines entières peut-on former ? Combien d’unités restent ?','Remplace toutes les centaines par des dizaines, sans regrouper les unités restantes.',f'${cc}\\times10+{dd}={v//10}$. Les {uu} unités ne suffisent pas à faire une autre dizaine.',f'{v//10} dizaines entières et {uu} unités.'),
        Q('Retire une dizaine de la quantité de départ. Quelle quantité reste ?','Retirer une dizaine revient à retirer dix unités.',f'${v}-10={v-10}$. On peut vérifier en rajoutant la dizaine : ${v-10}+10={v}$.',f'${v-10}$ unités.')))
    write(2,its)

def comparer():
    its=[]
    its.append(E('Les pas de dix','Sur la ligne, deux graduations voisines sont séparées de 10.\n\n[IMAGE_1]',
    Q('Complète les trois graduations sans étiquette.','Compte les intervalles depuis 400 ; chacun vaut 10.','Deux intervalles après 400 : $400+20=420$ ; cinq : $400+50=450$ ; huit : $400+80=480$.','$420$ ; $450$ ; $480$.'),
    Q('Combien y a-t-il d’intervalles de 400 à 500 ?','Compte les espaces entre deux traits, en ajoutant dix à chaque passage.','400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500 : dix passages.','10 intervalles.'),
    Q('Quelle graduation vient juste avant 450 ?','Recule d’un pas de dix.','$450-10=440$.','$440$.'),
    Q('Quelle graduation vient deux intervalles après 480 ?','Avance deux fois de dix.','$480+10=490$ puis $490+10=500$.','$500$.'),
    Q('Range les trois nombres trouvés du plus grand au plus petit.','Sur une ligne, les nombres augmentent vers la droite.','480 est à droite de 450, lui-même à droite de 420.','$480>450>420$.')))
    its.append(E('Comparer les bons rangs','On compare les couples 306 et 360 ; 721 et 719 ; 500 et 500.',
    Q('Complète les trois comparaisons avec le signe qui convient.','Compare les centaines, puis les dizaines si les centaines sont égales.','306 et 360 ont 3 centaines : 0 dizaine est inférieur à 6 dizaines. 721 et 719 ont 7 centaines : 2 dizaines dépassent 1 dizaine. Les deux derniers nombres sont identiques.','$306<360$ ; $721>719$ ; $500=500$.'),
    Q('Quel nombre est le plus petit parmi les six nombres écrits ?','Repère la plus petite centaine puis la plus petite dizaine.','Les nombres à 3 centaines précèdent les autres ; 306 précède 360.','$306$.'),
    Q('Range 306, 360 et 500 dans l’ordre croissant.','Place d’abord les nombres à trois centaines, puis le nombre à cinq centaines.','Entre les deux nombres à trois centaines, 306 a moins de dizaines.','$306<360<500$.'),
    Q('Encadre 719 entre deux dizaines consécutives.','Cherche la dizaine juste avant et celle juste après.','719 dépasse 710 mais n’atteint pas 720.','$710<719<720$.'),
    Q('Quel nombre est juste après 719 ? Compare-le à 721.','Ajoute une unité puis compare les unités.','$719+1=720$ ; 720 et 721 ont les mêmes centaines et dizaines, mais $0<1$.','$720<721$.')))
    its.append(E('Cinq étiquettes à ranger','Les étiquettes portent 423 ; 342 ; 432 ; 324 ; 400.',
    Q('Range les cinq nombres du plus petit au plus grand.','Regroupe par centaines puis compare les dizaines et les unités.','Les nombres à 3 centaines sont 324 et 342 ; les autres sont 400, 423, 432. Dans chaque groupe, on compare ensuite les dizaines.','$324<342<400<423<432$.'),
    Q('Quel est le plus grand nombre ?','Choisis le nombre à droite dans le rangement croissant.','432 vient après tous les autres nombres.','$432$.'),
    Q('Quel nombre vient immédiatement avant 423 dans ce rangement ?','Relis les étiquettes dans l’ordre trouvé.','Le rangement contient 400, puis 423, puis 432.','$400$.'),
    Q('Encadre 342 entre deux centaines consécutives.','Une centaine commence par un multiple de cent.','342 a 3 centaines et reste inférieur à 4 centaines.','$300<342<400$.'),
    Q('Insère 430 à sa place dans le rangement.','Compare 430 aux nombres à quatre centaines.','430 dépasse 423 mais a 2 unités de moins que 432.','$324<342<400<423<430<432$.')))
    its.append(E('Autour de 568','On cherche à situer 568 avec précision.',
    Q('Encadre 568 entre deux centaines consécutives.','Lis le chiffre des centaines et prends la centaine suivante.','568 dépasse 500 et reste inférieur à 600.','$500<568<600$.'),
    Q('Encadre 568 entre deux dizaines consécutives.','Prends la dizaine inférieure et ajoute dix pour la suivante.','568 contient 56 dizaines et 8 unités ; la dizaine suivante est 570.','$560<568<570$.'),
    Q('Quelle est la distance entre 560 et 568 ?','Cherche le complément de 560 à 568.','$568-560=8$.','8 unités.'),
    Q('Quelle est la distance entre 568 et 570 ?','Complète 568 jusqu’à la dizaine suivante.','$570-568=2$.','2 unités.'),
    Q('568 est-il plus près de 560 ou de 570 ?','Compare les deux distances calculées.','La distance à 570 est 2 et celle à 560 est 8 ; $2<8$.','568 est plus près de 570.')))
    its.append(E('Entre 799 et 802','On cherche les nombres entiers strictement compris entre 799 et 802.',
    Q('Écris tous les nombres possibles.','Compte d’une unité à partir de 799, en t’arrêtant avant 802.','799, 800, 801, 802 : seuls les deux nombres du milieu conviennent.','$800$ et $801$.'),
    Q('Quel est le plus petit nombre possible ?','Choisis le premier entier après 799.','$799+1=800$.','$800$.'),
    Q('Quel est le plus grand nombre possible ?','Choisis le dernier entier avant 802.','$802-1=801$.','$801$.'),
    Q('Combien de nombres conviennent ?','Compte les entiers trouvés sans compter les bornes.','Les deux étiquettes sont 800 et 801.','2 nombres.'),
    Q('Encadre 801 entre deux dizaines consécutives.','Prends 800 puis la dizaine suivante.','801 dépasse 800 et n’atteint pas 810.','$800<801<810$.')))
    its.append(E('Une ligne jusqu’à mille','Les traits avancent de 100 en 100. Le point A est marqué.\n\n[IMAGE_1]',
    Q('Quel nombre le point A représente-t-il ?','Compte les intervalles de cent depuis zéro.','A se trouve six intervalles après zéro : $6\\times100=600$.','$600$.'),
    Q('Quel est le nombre au trait juste avant A ?','Recule d’un intervalle de cent.','$600-100=500$.','$500$.'),
    Q('Quel est le nombre deux traits après A ?','Avance de deux centaines.','$600+200=800$.','$800$.'),
    Q('Combien d’intervalles séparent A de 1 000 ?','Compte les passages par 700, 800, 900 et 1 000.','Quatre passages ajoutent quatre centaines : $600+400=1000$.','4 intervalles.'),
    Q('Place B au nombre 400. Est-il à gauche ou à droite de A ?','Les nombres les plus petits sont à gauche.','$400<600$ ; B se place quatre intervalles après zéro.','B est à gauche de A.')))
    its.append(E('Deux écoles','Une école accueille 398 élèves, une autre 403 élèves.',
    Q('Quelle école a le plus d’élèves ?','Compare d’abord les centaines.','403 a quatre centaines ; 398 n’en a que trois.','$403>398$ : la seconde école.'),
    Q('Quel effectif est inférieur à 400 ?','Compare chaque effectif à la centaine 400.','398 est avant 400 ; 403 est après.','$398<400$.'),
    Q('Combien faut-il ajouter à 398 pour atteindre 400 ?','Avance unité par unité jusqu’à 400.','$398+2=400$.','2 élèves.'),
    Q('Combien dépasse-t-on 400 avec 403 ?','Cherche le complément de 400 à 403.','$403-400=3$.','3 élèves.'),
    Q('Quel est l’écart entre les deux effectifs ?','Passe par 400 et réunis les deux petits écarts.','De 398 à 400 : 2 ; de 400 à 403 : 3. $2+3=5$.','5 élèves.')))
    its.append(E('Quatre intervalles','Une règle des nombres porte 240, 241, 242, puis continue avec le même pas.',
    Q('Quelle est la valeur d’un intervalle ?','Compare deux graduations voisines.','$241-240=1$.','1 unité.'),
    Q('Quel nombre se trouve quatre intervalles après 242 ?','Avance de quatre unités.','243, 244, 245, 246 : le quatrième passage arrive à 246.','$242+4=246$.'),
    Q('Quel nombre se trouve quatre intervalles avant 242 ?','Recule de quatre unités.','$242-4=238$.','$238$.'),
    Q('Encadre 246 entre deux dizaines consécutives.','Cherche les dizaines voisines.','246 est après 240 et avant 250.','$240<246<250$.'),
    Q('Combien d’intervalles séparent 238 de 246 ?','Calcule la distance entre les deux graduations.','$246-238=8$.','8 intervalles.')))
    its.append(E('Les centaines d’abord','Lina range 509 avant 490 parce que 0 est plus petit que 9.',
    Q('Explique son erreur et écris le bon ordre.','Compare les centaines avant les dizaines.','490 a 4 centaines ; 509 en a 5. Les dizaines ne décident donc pas de cette comparaison.','$490<509$.'),
    Q('Encadre 509 entre deux centaines consécutives.','Repère les centaines voisines.','509 dépasse 500 et reste inférieur à 600.','$500<509<600$.'),
    Q('Encadre 490 et 509 par une même centaine placée entre eux.','Cherche la centaine qui termine les quatre centaines et commence les cinq centaines.','490 est avant 500 ; 509 est après 500.','$490<500<509$.'),
    Q('Combien manque-t-il à 490 pour atteindre 500 ?','Cherche le complément à la centaine suivante.','$500-490=10$.','10 unités.'),
    Q('Quel est l’écart entre 490 et 509 ?','Passe par 500.','De 490 à 500 : 10 ; de 500 à 509 : 9. $10+9=19$.','19 unités.')))
    write(3,its)

def suites():
    its=[]
    for motif,rank in [('AB',39),('ABC',60)]:
        k=len(motif);letter=motif[(rank-1)%k];before=motif[(rank-2)%k];after=motif[rank%k]
        its.append(E('Le motif '+motif, f'La suite commence par {" ".join(motif*3)} et continue toujours avec le même motif. On compte depuis la gauche.\n\n[IMAGE_1]',
        Q('Quel est le motif le plus court qui se répète ?','Repère le premier groupe qui recommence sans changement.',f'Après {" ".join(motif)}, les mêmes {k} lettres recommencent dans le même ordre.',f'{" ".join(motif)} : {k} lettres.'),
        Q(f'Quelle lettre se trouve au rang {rank} ?','Fais des groupes complets du motif, puis cherche la place dans le dernier groupe.',f'${rank//k}\\times{k}={rank//k*k}$.'+(f' Il reste {rank%k} lettre après ces groupes.' if rank%k else ' Le rang demandé termine ce groupe complet.'),f'La lettre {letter}.'),
        Q(f'Quelle lettre se trouve au rang {rank-1} ?','Recule d’une lettre dans le motif, en reprenant à la fin si nécessaire.',f'Juste avant {letter}, le motif porte {before}.',f'La lettre {before}.'),
        Q(f'Quelle lettre se trouve au rang {rank+1} ?','Avance d’une lettre ; après la fin du motif, reprends au début.',f'Juste après {letter}, le motif porte {after}.',f'La lettre {after}.'),
        Q(f'Quelle lettre se trouve au rang {rank+k} ?','Ajouter un motif complet garde la même place dans le motif.',f'${rank}+{k}={rank+k}$ : on avance de {k} lettres et on retrouve {letter}.',f'La lettre {letter}.')))
    # Remettre l’activité ABC au quatrième rang de la source.
    abc=its.pop()
    its.append(E('Une arrivée à la course','Un coureur arrive 63e ; les arrivées sont toutes à des places différentes.',
    Q('Combien de coureurs sont arrivés avant lui ?','Retire le coureur lui-même du nombre des 63 premiers.','$63-1=62$.','62 coureurs.'),
    Q('Quel rang précède le sien ?','Recule d’une place.','$63-1=62$.','62e.'),
    Q('Quel rang suit le sien ?','Avance d’une place.','$63+1=64$.','64e.'),
    Q('Quel est le rang d’un coureur ayant 69 coureurs devant lui ?','Ajoute sa propre place au nombre de coureurs qui le précèdent.','$69+1=70$.','70e.'),
    Q('Parmi les 70 premiers, combien sont derrière le coureur arrivé 63e ?','Ne compte pas les 63 premiers, qui incluent ce coureur.','$70-63=7$ ; ce sont les rangs 64 à 70.','7 coureurs.')))
    its.append(E('Après le quatre-vingt-dix-neuvième','On numérote les places d’une file de 1 à 105.',
    Q('Quel rang suit quatre-vingt-dix-neuvième ?','Ajoute une place au rang 99.','$99+1=100$.','Centième : 100e.'),
    Q('Quel rang précède le 99e ?','Recule d’une place.','$99-1=98$.','98e.'),
    Q('Combien de personnes sont devant la 100e ?','Retire la personne elle-même des cent premières.','$100-1=99$.','99 personnes.'),
    Q('Combien de personnes sont derrière la 100e dans cette file ?','Compte les places de 101 à 105.','$105-100=5$.','5 personnes.'),
    Q('Quelle place occupe une personne qui a 100 personnes devant elle ?','Ajoute la place de cette personne à celles qui sont devant.','$100+1=101$.','101e.')))
    its.append(abc)
    for title,start,rule,vals in [('De dix en dix',125,'plus10',[125,135,145,155,165]),('Doubler à chaque fois',2,'double',[2,4,8,16,32,64]),('Les nombres impairs',1,'plus2',list(range(1,24,2))),('Des pas qui grandissent',1,'croissant',[1,2,4,7,11,16,22])]:
        if rule=='plus10':
            p='Continue : 125 ; 135 ; 145 ; … ; …';a='$155$ ; $165$.';r='$135-125=10$ et $145-135=10$. On ajoute 10 : $145+10=155$ et $155+10=165$.';nextv=175;expr='165+10';prev=115;before='125-10'
        elif rule=='double':
            p='Continue : 2 ; 4 ; 8 ; 16 ; … ; …';a='$32$ ; $64$.';r='Chaque nombre vaut deux fois le précédent : $16\\times2=32$ puis $32\\times2=64$.';nextv=128;expr=r'64\times2';prev=1;before='2-1'
        elif rule=='plus2':
            p='Quel est le 12e nombre de la suite 1 ; 3 ; 5 ; 7 ; … ?';a='$23$.';r='On ajoute 2 à chaque rang. Les rangs 5 à 12 portent 9, 11, 13, 15, 17, 19, 21, 23.';nextv=25;expr='23+2';prev=0;before='1-1'
        else:
            p='Continue : 1 ; 2 ; 4 ; 7 ; 11 ; … ; …';a='$16$ ; $22$.';r='Les écarts sont 1, 2, 3, 4. On ajoute ensuite 5 puis 6 : $11+5=16$ et $16+6=22$.';nextv=29;expr='22+7';prev=0;before='1-1'
        last=vals[-1]
        its.append(E(title,'La règle indiquée par les premiers nombres continue de la même manière.',
        Q(p,'Cherche ce qui change entre deux nombres voisins ; applique la même règle.',r,a),
        Q('Écris les quatre premiers nombres.','Repars du début et applique trois fois la règle.',f'On part de {start} ; les quatre premiers nombres sont {", ".join(map(str,vals[:4]))}.',' ; '.join(map(str,vals[:4]))+'.'),
        Q(f'Quel nombre vient après {last} ?','Continue avec le même pas, le double, ou le pas suivant selon la règle.',f'${expr}={nextv}$.',f'${nextv}$.'),
        Q('Combien de nombres as-tu écrits dans la suite complète de la première question ?','Compte les rangs à partir de 1, sans sauter de nombre.',f'La suite complétée est : {", ".join(map(str,vals))}.',f'{len(vals)} nombres.'),
        Q('Un camarade recopie le dernier nombre au rang suivant. Explique pourquoi cela ne convient pas.','Une nouvelle place doit respecter le changement de la suite.',f'Après {last}, la règle donne {nextv} et non {last}. Le nombre doit donc encore augmenter.',f'Il faut écrire ${nextv}$, pas ${last}$.')))
    its.append(E('Dans la file','Tu es 37e dans une file de 100 personnes. On compte depuis le début de la file.',
    Q('Combien de personnes sont derrière toi ?','Retire les 37 premières personnes, y compris toi, du total.','$100-37=63$.','63 personnes.'),
    Q('Combien de personnes sont devant toi ?','Dans les 37 premières personnes, enlève ta propre place.','$37-1=36$.','36 personnes.'),
    Q('Vérifie le total en réunissant les personnes devant, toi et celles derrière.','Ta place compte pour une seule personne.','$36+1+63=100$.','On retrouve 100 personnes.'),
    Q('Si tu avances d’une place, quel est ton nouveau rang ?','Avancer vers le début diminue le rang d’une unité.','$37-1=36$.','36e.'),
    Q('À cette nouvelle place, combien de personnes sont derrière toi ?','Le total reste 100 ; retire les 36 premières personnes.','$100-36=64$.','64 personnes.')))
    write(4,its)

def single_story(title,intro,a,b,op,unit,target,role,follow):
    v=a+b if op=='+' else a-b
    method='Réunis les deux parties pour retrouver le tout.' if role=='tout' else 'Retire la partie connue du tout pour trouver la partie inconnue.'
    if role=='depart-don':method='Remets les objets donnés avec ceux qui restent pour reconstruire le départ.'
    if role=='depart-recu':method='Retire ce qui a été reçu du total final pour reconstruire le départ.'
    reverse=f'{v}-{b}={a}' if op=='+' else f'{v}+{b}={a}'
    rel=f'{a}+{b}={v}' if op=='+' else f'{b}+{v}={a}'
    return E(title,intro,
    Q('Que cherche-t-on ? La quantité cherchée sera-t-elle plus grande ou plus petite que '+str(a)+' ?', 'Replace l’inconnue dans l’histoire avant de choisir un calcul.',method+f' La quantité cherchée est donc '+('plus grande' if op=='+' else 'plus petite')+f' que {a}.',target+' ; '+('plus grande' if op=='+' else 'plus petite')+f' que {a}.'),
    Q('Écris le calcul qui permet de répondre.','Choisis l’opération à partir du rôle du tout, des parties ou du changement.',method,f'${a}{op}{b}$.'),
    Q('Effectue le calcul et réponds à la question de l’histoire.',method,
      (f'Pour ajouter {b}, on ajoute {b//100*100}, puis {(b//10)%10*10}, puis {b%10}. ' if op=='+' else f'On cherche ce qui manque entre {b} et {a}. ')+f'${a}{op}{b}={v}$.',f'${v}$ {unit}.'),
    Q('Vérifie ta réponse avec l’opération inverse.','Retrouve une quantité connue pour contrôler la réponse.',f'${reverse}$. On retrouve bien {a}.',f'La réponse est vérifiée : ${reverse}$.'),
    Q(follow[0],follow[1],follow[2],follow[3]))

def problemes_simples():
    its=[]
    rows=[('Les perles bleues','Il y a 360 perles en tout, dont 145 vertes. Les autres sont bleues.\n\n[IMAGE_1]',360,145,'-','perles bleues','Le nombre de perles bleues','partie',('Si 10 perles bleues sont retirées, combien de perles bleues restent ?','Retire seulement les dix perles bleues du résultat trouvé.','$215-10=205$.','$205$ perles bleues.')),
    ('Réunir les deux bacs','Un bac contient 238 cubes et un autre 174. On veut connaître le nombre total de cubes.',238,174,'+','cubes','Le total des cubes','tout',('On ajoute 8 cubes au premier bac. Quel est le nouveau total ?','Le second bac ne change pas ; ajoute huit au total précédent.','$412+8=420$.','$420$ cubes.')),
    ('Les places de l’album','Un album a 500 places et contient déjà 367 photos. Combien de places sont libres ?',500,367,'-','places libres','Le nombre de places libres','partie',('On colle encore 20 photos. Combien de places restent libres ?','Chaque nouvelle photo occupe une place libre.','$133-20=113$.','$113$ places libres.')),
    ('Avant le don','Tu donnes 57 images et il t’en reste 186. Combien en avais-tu au départ ?',186,57,'+','images au départ','Le nombre d’images avant le don','depart-don',('Si tu avais donné seulement 50 images, combien t’en resterait-il avec le même départ ?','Repars du départ retrouvé et retire le nouveau don.','$243-50=193$.','$193$ images.')),
    ('Avant de recevoir','Tu reçois 48 cartes et tu en as maintenant 302. Combien en avais-tu au départ ?',302,48,'-','cartes au départ','Le nombre de cartes avant de recevoir les 48 cartes','depart-recu',('Avec ce même départ, combien aurais-tu de cartes après en avoir reçu 50 ?','Ajoute le nouveau cadeau au départ retrouvé.','$254+50=304$.','$304$ cartes.')),
    ('Les fruits cueillis','Un arbre portait 125 fruits. Il en reste 89. Combien de fruits ont été cueillis ?',125,89,'-','fruits cueillis','Le nombre de fruits cueillis','partie',('On cueille encore 10 fruits. Combien de fruits restent dans l’arbre ?','Pars des 89 fruits encore sur l’arbre.','$89-10=79$.','$79$ fruits.'))]
    for row in rows:its.append(single_story(*row))
    its.append(E('L’album sera-t-il assez grand ?','Un album peut contenir 350 photos. Lina a 278 photos et Noé en a 85.',
    Q('Faut-il comparer 350 à 278 ou au total des deux collections ?','Pour ranger toutes les photos, réunis les deux collections.','L’album doit accueillir les photos de Lina et celles de Noé. Comparer seulement 278 à 350 oublierait Noé.','Il faut comparer 350 au total des deux collections.'),
    calc('Combien de photos faut-il ranger ?','278+85',363,'photos',m='Réunis les deux collections pour trouver toutes les photos à ranger.',why='On réunit deux parties : les 278 photos de Lina et les 85 de Noé.'),
    Q('L’album suffit-il ?','Compare le nombre de photos à la capacité de l’album.','$363>350$ : les photos sont plus nombreuses que les places.','Non, l’album ne suffit pas.'),
    calc('Combien de places manque-t-il ?','363-350',13,'places',m='Cherche l’écart entre le nombre de photos et le nombre de places.'),
    Q('Vérifie le nombre de places manquantes.','Ajoute les places manquantes aux places disponibles.','$350+13=363$. On obtient exactement le nombre de photos.','13 places supplémentaires permettent de ranger les 363 photos.')))
    its.append(single_story('Reconstituer la réserve','Une réserve a perdu 126 feuilles et en contient encore 384. Combien y en avait-il au départ ?',384,126,'+','feuilles au départ','Le nombre de feuilles avant la perte','depart-don',('Avec ce même départ, combien resterait-il après une perte de 100 feuilles ?','Retire la nouvelle perte du départ retrouvé.','$510-100=410$.','$410$ feuilles.')))
    its.append(E('Inventer une histoire de départ','On veut une histoire où l’on donne 25 objets et dont la réponse se calcule avec 140 + 25.',
    Q('Dans cette histoire, que représente 140 ?','Pour retrouver un départ après un don, réunis le reste et le don.','Le don est 25. L’autre quantité ajoutée doit être ce qui reste après le don.','140 représente le nombre d’objets qui restent.'),
    Q('Écris une histoire avec des cartes et une question sur le départ.','Place le don avant le reste et demande la quantité initiale.','On connaît ce qui a quitté la collection et ce qui est encore là.','J’ai donné 25 cartes et il m’en reste 140. Combien en avais-je au départ ?'),
    calc('Résous cette histoire.','140+25',165,'cartes au départ',m='Remets les cartes données avec celles qui restent.'),
    Q('Vérifie le départ en rejouant le don.','Retire les 25 cartes du départ retrouvé.','$165-25=140$. Le reste est bien celui de l’énoncé.','La réponse $165$ cartes est vérifiée.'),
    Q('Avec le même départ, si tu donnes 30 cartes, combien en reste-t-il ?','Conserve le départ 165 et change seulement le don.','$165-30=135$.','$135$ cartes.')))
    write(14,its)

def comparison_story(title,intro,small,delta,unit,mode,names):
    big=small+delta;whoS,whoB=names
    if mode=='big':expr=f'{small}+{delta}';v=big;unknown=whoB;known=small
    elif mode=='small':expr=f'{big}-{delta}';v=small;unknown=whoS;known=big
    else:expr=f'{big}-{small}';v=delta;unknown='l’écart';known=big
    return E(title,intro,
    Q('Quelle quantité doit être la plus grande ?','Traduis « de plus » ou « de moins » avant de calculer.',f'{whoS} correspond à la petite quantité ; {whoB} correspond à la grande quantité. L’écart est ajouté à la petite pour obtenir la grande.',whoB+'.'),
    Q('Écris le calcul qui répond à la question.','Grande quantité = petite quantité + écart ; retire la quantité connue pour trouver ce qui manque.',f'On cherche {unknown}. '+('Il faut réunir la petite quantité et l’écart.' if mode=='big' else 'Il faut retirer l’écart de la grande quantité.' if mode=='small' else 'Il faut retirer la petite quantité de la grande.'),f'${expr}$.'),
    Q('Calcule et réponds.','Effectue l’opération choisie en conservant l’unité.',f'${expr}={v}$.',f'${v}$ {unit}.'),
    Q('Vérifie la comparaison.','Ajoute l’écart à la petite quantité : on doit retrouver la grande.',f'${small}+{delta}={big}$. Les deux quantités diffèrent donc bien de {delta}.',f'${small}+{delta}={big}$.'),
    Q(f'Si la petite quantité augmente de 5 et que la grande ne change pas, quel devient l’écart ?', 'Recalcule la petite quantité, puis retire-la de la grande.',f'${small}+5={small+5}$ ; ${big}-{small+5}={delta-5}$.',f'${delta-5}$ {unit}.'))

def comparer_quantites():
    rows=[('Les cartes de Noé','Lina a 125 cartes. Noé en a 28 de plus. Combien Noé en a-t-il ?\n\n[IMAGE_1]',125,28,'cartes','big',('Lina','Noé')),
    ('L’écart entre les écoles','Une école a 238 élèves et une autre en a 196. Quel est l’écart entre les effectifs ?',196,42,'élèves','delta',('L’école de 196 élèves','L’école de 238 élèves')),
    ('Le bac rouge','Le bac bleu contient 175 cubes. Il en a 46 de moins que le bac rouge. Combien le bac rouge en contient-il ?',175,46,'cubes','big',('Le bac bleu','Le bac rouge')),
    ('Les perles de Zoé','Mila a 304 perles, soit 78 de plus que Zoé. Combien Zoé en a-t-elle ?',226,78,'perles','small',('Zoé','Mila')),
    ('Deux ficelles','Une ficelle mesure 140 cm, l’autre 95 cm. De combien la première est-elle plus longue ?',95,45,'cm','delta',('La ficelle de 95 cm','La ficelle de 140 cm')),
    ('Autant de cartes','Lina et Sami ont chacun 125 cartes. Quel est l’écart entre leurs collections ?',125,0,'carte','delta',('Lina','Sami')),
    ('Le prix de l’autre jeu','Un jeu coûte 38 €. Il coûte 12 € de moins qu’un autre jeu. Quel est le prix de l’autre jeu ?',38,12,'€','big',('Le jeu à 38 €','L’autre jeu')),
    ('Corriger la comparaison','Lina dit : « J’ai 63 billes, soit 9 de plus que Noé. Donc Noé en a 72. » Corrige sa réponse.',54,9,'billes','small',('Noé','Lina')),
    ('Inventer un écart','On choisit deux collections : 240 cartes pour A et 185 cartes pour B. On veut inventer une question dont le calcul est 240 - 185.',185,55,'cartes','delta',('B','A'))]
    its=[]
    for row in rows:
        item=comparison_story(*row)
        if row[2]==125 and row[3]==0:
            item['questions'][0]=Q('Quelle collection est la plus grande ?','Compare les deux nombres avant de chercher un écart.','Les deux collections ont 125 cartes : aucune ne dépasse l’autre.','Les deux collections sont égales.')
            item['questions'][4]=Q('Lina reçoit 5 cartes et Sami garde ses 125 cartes. Quel devient l’écart ?','Calcule la nouvelle collection de Lina, puis la différence.','$125+5=130$ et $130-125=5$.','5 cartes.')
        if row[0]=='Corriger la comparaison':
            item['questions'][2]['etapes'].insert(0,'Noé a moins que Lina. Ajouter 9 donnerait une collection plus grande et contredirait l’histoire.')
        if row[0]=='Inventer un écart':
            item['questions'][1]=Q('Invente une question dont le calcul est 240 - 185.','Demande combien la grande collection dépasse la petite.','A possède davantage de cartes ; on cherche leur écart.','Combien A possède-t-il de cartes de plus que B ?')
        its.append(item)
    write(15,its)

def deux_etapes():
    data=[('Les prêts de livres','Il y a 125 livres. On en apporte 38, puis on en prête 47. Combien en reste-t-il ?\n\n[IMAGE_1]',125,38,'+',47,'-', 'livres','Le nombre de livres après l’apport','Le prêt retire 47 livres.'),
    ('Les perles vertes','Une boîte contient 245 perles, dont 86 rouges et 74 bleues. Les autres sont vertes. Combien sont vertes ?',86,74,'+',245,'R-','perles vertes','Le total des perles rouges et bleues','On retire ce total de toutes les perles.'),
    ('Le trajet du bus','Un bus contient 43 voyageurs. 18 descendent, puis 27 montent. Combien y a-t-il de voyageurs ?',43,18,'-',27,'+','voyageurs','Le nombre de voyageurs après la descente','La montée ajoute 27 voyageurs.'),
    ('Les crayons et le cahier','Tu achètes 6 crayons à 2 € chacun et un cahier à 5 €. Combien paies-tu ?',6,2,'*',5,'+','€','Le prix des six crayons','On ajoute ensuite le prix du cahier.'),
    ('La monnaie sur cinquante euros','Tu achètes 7 jeux à 4 € chacun et tu donnes 50 €. Combien reçois-tu de monnaie ?',7,4,'*',50,'R-','€ de monnaie','Le prix des sept jeux','On retire le prix des jeux de la somme donnée.'),
    ('Les fournitures de huit enfants','Pour 8 enfants, il faut un cahier à 3 € et une pochette à 2 € par enfant. Quel est le coût total ?',3,2,'+',8,'*','€','Le coût pour un enfant','On répète ce coût pour les huit enfants.'),
    ('Les sacs de balles','On prépare 5 sacs de 6 balles, puis on ajoute 9 balles isolées. Combien de balles y a-t-il ?',5,6,'*',9,'+','balles','Le nombre de balles dans les cinq sacs','On ajoute ensuite les balles isolées.'),
    ('Les places encore libres','Il y a 260 places. On en réserve 135 le matin et 78 l’après-midi. Combien restent libres ?',135,78,'+',260,'R-','places libres','Le total des places réservées','On retire les places réservées de la capacité totale.'),
    ('Les quatre livres de Lina','Lina reçoit 30 €. Elle achète 4 livres à 5 € chacun. Elle dit qu’il lui reste 26 €. Explique et corrige.',4,5,'*',30,'R-','€','Le prix des quatre livres','On retire le prix des achats des 30 € reçus.')]
    its=[]
    for title,intro,a,b,op,c,op2,unit,inter,why2 in data:
        mid=a+b if op=='+' else a-b if op=='-' else a*b
        first=f'{a}'+(r'\times' if op=='*' else op)+str(b)
        second=f'{c}-{mid}' if op2=='R-' else f'{mid}'+(r'\times' if op2=='*' else op2)+str(c)
        final=c-mid if op2=='R-' else mid+c if op2=='+' else mid-c if op2=='-' else mid*c
        midunit='€' if 'prix' in inter.lower() or 'coût' in inter.lower() else 'livres' if 'livres' in inter else 'perles rouges et bleues' if 'perles' in inter else 'voyageurs' if 'voyageurs' in inter else 'balles' if 'balles' in inter else 'places réservées'
        m1='Multiplie le nombre de groupes par la quantité dans chaque groupe.' if op=='*' else 'Réunis les deux quantités nécessaires à cette première étape.' if op=='+' else 'Retire d’abord la quantité qui quitte la situation.'
        check=f'{final}+{mid}={c}' if op2=='R-' else f'{final}-{c}={mid}' if op2=='+' else f'{final}+{c}={mid}' if op2=='-' else f'{c}'+r'\times'+f'{mid}={final}'
        its.append(E(title,intro,
        Q('Que faut-il trouver en premier ?','Cherche une quantité nécessaire au calcul final mais encore inconnue.',inter+'. '+('Un seul objet ne suffit pas : il faut le prix de tous les objets achetés.' if op=='*' else 'Cette quantité servira dans la deuxième étape.'),inter+'.'),
        Q('Calcule cette première quantité.',m1,f'${first}={mid}$. Ce résultat concerne '+inter.lower()+'.',f'${mid}$ {midunit}.'),
        Q('Quel calcul permet maintenant de répondre à la question finale ?','Réutilise le résultat intermédiaire avec la donnée qui reste.',why2+f' On utilise {mid} et {c}.',f'${second}$.'),
        Q('Effectue ce calcul et conclus.','Calcule la deuxième étape puis écris l’unité demandée.',f'${second}={final}$.',f'${final}$ {unit}.'),
        Q('Vérifie le résultat de la deuxième étape.','Reconstitue la quantité avant la dernière opération ou répète les groupes.',f'${check}$. '+('Lina avait retiré 4 au lieu du prix des quatre livres ; il fallait retirer 20.' if title=='Les quatre livres de Lina' else 'Les quantités connues sont bien retrouvées.'),f'La vérification donne ${check}$.')))
    write(16,its)

def partager():
    data=[('Les cartes des quatre enfants',36,4,'share','cartes','enfants'),('Les équipes de six',54,6,'groups','enfants','équipes'),('Dix parts de perles',80,10,'share','perles','parts'),('Les paquets de dix cartes',120,10,'groups','cartes','paquets'),('Les pages pour vingt-cinq photos',25,10,'ceil','photos','pages'),('Les boîtes complètes',41,6,'floor','œufs','boîtes'),('Les cartes de cinq groupes',150,5,'share','cartes','groupes'),('Les pages pour cent-quatre-vingt-neuf images',189,10,'ceil','images','pages'),('Vérifier les treize boîtes',75,6,'floor','œufs','boîtes')]
    its=[]
    for title,total,size,mode,unit,groups in data:
        quotient,rem=divmod(total,size)
        if mode=='share':intro=f'On partage équitablement {total} {unit} entre {size} {groups}. Combien chaque part contient-elle ?';ans=f'{quotient} {unit} par part.'
        else:intro=f'On range {total} {unit} dans des {groups} de {size} places. '+('Toutes les photos ou images doivent être rangées.' if mode=='ceil' else 'On utilise seulement des groupes complets.' if mode=='floor' else 'Combien de groupes peut-on former ?');ans=f'{quotient+(mode=="ceil" and rem>0)} {groups}.'
        if total==75:intro='Pour vendre 75 œufs en boîtes complètes de 6, Noé propose 13 boîtes. Vérifie sa proposition.'
        if total==36:intro+='\n\n[IMAGE_1]'
        result=quotient+(mode=='ceil' and rem>0)
        why='Le nombre de parts est connu ; on cherche le contenu de chaque part.' if mode=='share' else 'Le contenu d’un groupe est connu ; on cherche combien de groupes on peut former.'
        conclusion='Le partage est exact : chaque part a le même contenu.' if not rem else 'Les objets restants doivent être placés dans un groupe supplémentaire.' if mode=='ceil' else 'Les objets restants ne remplissent pas une boîte complète.'
        its.append(E(title,intro,
        Q('Cherche-t-on le nombre de groupes ou le contenu d’une part ?','Distingue le nombre de parts du nombre d’objets dans chaque part.',why,'Le contenu d’une part.' if mode=='share' else 'Le nombre de groupes.'),
        Q('Quel produit donne le total, ou le plus grand total qui ne le dépasse pas ?','Utilise les multiples de '+str(size)+' et arrête-toi avant de dépasser le total.',f'${quotient}\\times{size}={quotient*size}$ ; ${(quotient+1)}\\times{size}={(quotient+1)*size}$ dépasserait {total}.',f'${quotient}\\times{size}={quotient*size}$.'),
        Q('Combien d’objets restent après ces groupes ?','Retire du total les objets déjà placés.',f'${total}-{quotient*size}={rem}$.',f'{rem} {unit} restent.'),
        Q('Réponds à la question de départ.','Relis si tous les objets doivent être rangés ou si seuls les groupes complets comptent.',conclusion+(' Les treize boîtes demanderaient $13\\times6=78$ œufs, soit plus que 75.' if total==75 else ''),ans),
        Q('Vérifie que tous les objets sont comptés.','Réunis les objets des groupes complets et les objets restants.',f'${quotient}\\times{size}+{rem}={total}$. '+('Le reste est inférieur à '+str(size)+', donc on ne peut pas former un groupe complet supplémentaire.' if rem else 'Aucun objet ne reste hors du partage.'),f'${quotient}\\times{size}+{rem}={total}$.')))
    write(17,its)

def f(a,b):return r'\frac{'+str(a)+'}{'+str(b)+'}'
WORDS={2:'demi',3:'tiers',4:'quart',5:'cinquième',6:'sixième',8:'huitième',10:'dixième'}
def unit_fraction(title,b,intro=None,action='observe'):
    name=WORDS[b]
    intro=intro or f'La bande représente un tout. Elle est partagée en {b} parts égales ; une seule est coloriée.'
    intro+='\n\n[IMAGE_1]'
    p='Quelle fraction du tout est coloriée ?' if action=='observe' else f'Colorie un {name} de cette bande.'
    r=f'Le tout contient {b} parts de même taille. Une seule est prise : on écrit 1 au-dessus de la barre et {b} au-dessous.'
    return E(title,intro,
    Q(p,'Compte les parts égales du tout puis les parts choisies.',r,f'${f(1,b)}$ : un {name}.'),
    Q('Que signifie le nombre écrit en bas de la fraction ?','Le nombre en bas décrit le partage du tout, même si peu de parts sont coloriées.',f'Le dénominateur {b} indique que le tout a été partagé en {b} parts égales.',f'{b} parts égales dans le tout.'),
    Q('Que signifie le nombre écrit en haut de la fraction ?','Le nombre en haut compte les parts choisies.',f'Une seule part est choisie parmi les {b} parts ; le numérateur est donc 1.','1 part choisie.'),
    Q(f'Combien de parts de cette taille faut-il pour recouvrir le tout ?','Remets ensemble toutes les parts du partage.',f'Il faut les {b} parts : ${f(b,b)}=1$.',f'{b} parts.'),
    Q('Un camarade prend une part d’un partage inégal. Peut-il lui donner le même nom ?','Une fraction de ce type exige un partage en parts égales.',f'Le nom « {name} » exige {b} parts égales ; compter {b} morceaux de tailles différentes ne suffit pas.','Non : les parts doivent être égales.'))

def decouvrir_fractions():
    its=[unit_fraction('Une part sur cinq',5),unit_fraction('Construire une moitié',2,'La bande entière est à partager en deux parts égales.',action='colorie'),unit_fraction('Une part sur trois',3,'La bande est déjà partagée en trois parts égales.',action='colorie')]
    its[1]['questions'][0]['question']='Partage la bande en deux parts égales, puis colorie une moitié.'
    for denoms,title in [([2,3,4,5],'Nommer les premières fractions'),([6,8,10],'Sixièmes, huitièmes et dixièmes')]:
        b=denoms[-1]
        qs=unit_fraction(title,b)['questions']
        qs[0]=Q('Lis les fractions : '+' ; '.join('$'+f(1,d)+'$' for d in denoms)+'.','Associe le nombre de parts égales au nom d’une part.', 'Le 1 indique une part choisie. Le nombre du bas indique en combien de parts égales le tout est partagé.',' ; '.join('un '+WORDS[d] for d in denoms)+'.')
        its.append(ex(title,f'On lit plusieurs fractions. Pour les questions 2 à 5, on étudie ${f(1,b)}$.',qs))
    its.append(unit_fraction('Une part parmi six',6))
    its.append(E('Des morceaux inégaux','Lina découpe une bande en quatre morceaux de tailles différentes.\n\n[IMAGE_1]',
    Q('Une part est-elle forcément un quart du tout ?','Vérifie l’égalité des parts avant de nommer une fraction.','Il y a quatre morceaux, mais ils n’ont pas la même taille. On ne peut donc pas affirmer qu’un morceau vaut un quart.','Non : quatre morceaux inégaux ne constituent pas un partage en quarts.'),
    Q('Quel point du partage faut-il corriger ?','Un quart signifie une part parmi quatre parts égales.','Il faut conserver quatre parts mais leur donner la même aire.','Il faut obtenir quatre parts égales.'),
    Q('Sur une nouvelle bande, fais un partage correct en quarts.','Partage d’abord en deux moitiés, puis chaque moitié en deux parts égales.','Deux moitiés découpées chacune en deux donnent quatre parts de même taille.','Quatre parts égales.'),
    Q('Écris la fraction correspondant à une de ces nouvelles parts.','Compte une part choisie sur les quatre parts égales.','Le numérateur est 1 ; le dénominateur est 4.',f'${f(1,4)}$.'),
    Q('Combien de quarts reconstituent cette nouvelle bande ?','Réunis toutes les parts du partage égal.',f'Les quatre parts recouvrent le tout : ${f(4,4)}=1$.','4 quarts.')))
    its.append(E('Le contenu partagé entre quatre verres','On partage tout le contenu d’une bouteille entre quatre verres identiques. On verse la même quantité dans chaque verre.',
    Q('Quelle fraction du contenu initial reçoit chaque verre ?','Le tout est le contenu initial ; les quatre verres reçoivent des parts égales.','Il y a quatre parts égales et chaque verre reçoit une de ces parts.',f'${f(1,4)}$ : un quart du contenu initial.'),
    Q('Quel est le tout dans cette situation ?','Repère la quantité avant son partage.','Les verres sont les récipients des parts, tandis que la bouteille contenait la quantité à partager.','Tout le contenu initial de la bouteille.'),
    Q('Pourquoi faut-il verser la même quantité dans chaque verre ?','Le nom de quart exige quatre parts égales.','Si un verre reçoit davantage qu’un autre, les quatre parts ne sont plus égales.','Pour que chaque part soit un quart du contenu initial.'),
    Q('Combien de parts a-t-on versées quand les quatre verres sont remplis ?','Compte tous les verres ayant reçu une part.','Quatre verres ont reçu chacun une part, donc les quatre parts du partage ont été distribuées.','4 quarts.'),
    Q('Si un verre reste vide et que les trois autres se partagent également tout le contenu, chaque part est-elle encore un quart ?','Recompte les parts égales réellement formées.','Le tout est alors partagé entre trois verres, donc en trois parts égales.',f'Non : chaque part est ${f(1,3)}$, un tiers.')))
    its.append(unit_fraction('Colorier un huitième',8,'La bande est partagée en huit parts égales. Colorie une seule part.',action='colorie'))
    write(18,its)

def read_fraction(title,a,b,intro,action=False):
    return E(title,intro+'\n\n[IMAGE_1]',
    Q('Colorie la fraction demandée.' if action else 'Quelle fraction est coloriée ?','Compte les parts égales du tout, puis les parts à prendre.',f'Le tout a {b} parts égales ; on en choisit {a}.',f'${f(a,b)}$.'),
    Q('Quel est le numérateur et que compte-t-il ?','Le nombre du haut compte les parts choisies.',f'Il y a {a} parts choisies ; on écrit {a} en haut.',f'Numérateur : {a}, nombre de parts choisies.'),
    Q('Quel est le dénominateur et que décrit-il ?','Le nombre du bas décrit le partage du tout.',f'Le tout comporte {b} parts égales ; on écrit {b} en bas.',f'Dénominateur : {b}, nombre de parts égales du tout.'),
    Q('La partie choisie est-elle plus petite que le tout ?','Compare le nombre de parts prises au nombre de parts du tout.',f'${a}<{b}$ ; toutes les parts du tout ne sont pas prises.',f'Oui : ${f(a,b)}<1$.'),
    Q('Combien de parts de cette taille restent à choisir pour recouvrir le tout ?','Compte les parts encore non choisies.',f'Le tout a {b} parts, dont {a} déjà prises : ${b}-{a}={b-a}$.',f'{b-a} parts.'))

def compare_fraction(title,pairs,intro):
    a,b,c,d=pairs[0]
    sign='<' if a*d<c*b else '>' if a*d>c*b else '='
    same=b==d
    why=f'Les parts ont la même taille ({WORDS[b]}s) ; {a} parts '+('sont moins que' if sign=='<' else 'sont plus que' if sign=='>' else 'sont autant que')+f' {c} parts.' if same else f'On prend le même nombre de parts. Le partage en {min(b,d)} parts donne des parts plus grandes que le partage en {max(b,d)} parts.'
    results=[];reasons=[]
    for aa,bb,cc,dd in pairs:
        ss='<' if aa*dd<cc*bb else '>' if aa*dd>cc*bb else '='
        results.append('$'+f(aa,bb)+ss+f(cc,dd)+'$')
        reasons.append(f'{aa} parts sur {bb} sont comparées à {cc} parts sur {dd}.'+(f' Le nombre de parts prises décide, car les parts sont de même taille.' if bb==dd else f' Avec le même numérateur, le plus petit dénominateur donne les plus grandes parts.'))
    return E(title,intro,
    Q('Compare les fractions indiquées.','À dénominateur égal, compare les numérateurs ; pour deux fractions de numérateur 1, compare la taille des parts.',' '.join(reasons)+' '+why,' ; '.join(results)+'.'),
    Q('Quel est le tout utilisé pour comparer ?','Les bandes doivent représenter des touts identiques.','Une même fraction peut désigner des quantités différentes si les touts changent ; ici, les bandes entières sont identiques.','Le même tout, ou deux touts identiques.'),
    Q('Pour la première comparaison, les parts ont-elles la même taille ?','Compare les dénominateurs : ils décrivent le partage du tout.',f'Les dénominateurs sont {b} et {d}. '+('Ils sont égaux : le partage est le même.' if same else 'Ils sont différents : les parts n’ont pas la même taille.'),'Oui : même dénominateur.' if same else 'Non : les dénominateurs sont différents.'),
    Q('Dans la première comparaison, quelle est la plus petite fraction ?','Relis le signe trouvé : la pointe du signe est dirigée vers la plus petite fraction.',why,'$'+(f(a,b) if sign=='<' else f(c,d))+'$.'),
    Q('Un camarade dit : « Un plus grand dénominateur donne toujours une plus grande fraction. » Corrige cette phrase.','Pour un même tout et un même numérateur, davantage de parts signifie des parts plus petites.','Partager le même gâteau en dix parts donne des parts plus petites que le partager en cinq. Prendre une part sur dix donne moins que prendre une part sur cinq.',f'À numérateur égal, le plus grand dénominateur donne la plus petite fraction : ${f(1,10)}<{f(1,5)}$.'))

def lire_fractions():
    its=[read_fraction('Trois parts parmi huit',3,8,'Une bande est partagée en huit parts égales ; trois sont coloriées.'),read_fraction('Construire trois quarts',3,4,'Colorie trois quarts de la bande partagée en quatre parts égales.',True),
    compare_fraction('Comparer des parts de même taille',[(2,6,5,6),(4,8,3,8)],f'Compare ${f(2,6)}$ et ${f(5,6)}$, puis ${f(4,8)}$ et ${f(3,8)}$.'),
    compare_fraction('Un tiers et un sixième',[(1,3,1,6)],f'Deux bandes identiques montrent ${f(1,3)}$ et ${f(1,6)}$.\n\n[IMAGE_1]'),
    compare_fraction('Une part, deux partages',[(1,5,1,10),(1,8,1,4)],f'Les touts sont identiques. Compare ${f(1,5)}$ à ${f(1,10)}$, puis ${f(1,8)}$ à ${f(1,4)}$.')]
    its.append(E('Le tout entier','On hésite entre cinq cinquièmes et quatre cinquièmes pour représenter un tout entier.',
    Q('Quelle fraction correspond au tout entier ?','Le tout est reconstitué quand toutes ses parts sont prises.',f'Le tout contient cinq parts égales ; il faut les cinq : ${f(5,5)}=1$.',f'${f(5,5)}=1$.'),
    Q('Que représente le 5 du bas ?','Le dénominateur décrit le partage du tout.','Le tout a été partagé en cinq parts égales.','5 parts égales.'),
    Q('Que représente le 5 du haut ?','Le numérateur compte les parts choisies.','Toutes les cinq parts sont prises.','5 parts choisies.'),
    Q('Pourquoi quatre cinquièmes ne représentent-ils pas le tout ?','Compare les parts prises au nombre total de parts.','Quatre parts sur cinq sont prises ; il reste une part non prise.',f'${f(4,5)}<1$ : il manque une part.'),
    Q('Écris une autre fraction représentant un tout partagé en huit parts égales.','Prends les huit parts du tout.',f'Huit parts prises sur huit donnent ${f(8,8)}=1$.',f'${f(8,8)}=1$.')))
    item=compare_fraction('Les coloriages de Lina et Noé',[(7,10,4,10)],'Lina colorie sept dixièmes d’une bande. Noé colorie quatre dixièmes d’une bande identique.')
    item['questions'][0]['question']='Qui a colorié la plus grande partie ? Écris la comparaison.'
    item['questions'][0]['resultat']=f'Lina : ${f(7,10)}>{f(4,10)}$.'
    its.append(item)
    its.append(E('Des touts de tailles différentes','Une petite bande et une grande bande sont chacune partagées en deux parts égales.\n\n[IMAGE_1]',
    Q('Leurs moitiés ont-elles forcément la même taille ?','Compare les bandes entières avant de comparer leurs parts.','Chaque moitié vaut une part sur deux de sa propre bande. Comme les bandes entières sont de tailles différentes, leurs moitiés peuvent être différentes.','Non : les touts sont de tailles différentes.'),
    Q('Quelle fraction de sa bande représente chaque moitié ?','Chaque bande est partagée en deux parts égales.','Une des deux parts égales de chaque tout est une moitié.',f'${f(1,2)}$ de sa propre bande.'),
    Q('Peut-on comparer leurs quantités avec les seuls nombres un demi et un demi ?','Les fractions décrivent une proportion du tout, pas sa taille initiale.','Le même nom « un demi » s’applique aux deux parts, mais les touts ne sont pas identiques.','Non : il faut aussi connaître les touts.'),
    Q('Comment modifier la situation pour comparer seulement les fractions ?','Utilise deux touts identiques.','Deux bandes de même taille, chacune partagée en deux parts égales, donnent des moitiés de même taille.','Prendre deux bandes identiques.'),
    Q('Avec deux bandes identiques, leurs moitiés sont-elles égales ?','Le tout et le partage sont alors identiques.','Une moitié recouvre exactement l’autre moitié.',f'Oui : ${f(1,2)}={f(1,2)}$.')))
    its.append(E('Deux quarts et une moitié','Deux bandes identiques montrent deux quarts et une moitié.\n\n[IMAGE_1]',
    Q('Deux quarts recouvrent-ils une moitié ?','Superpose les deux bandes en alignant leurs extrémités.','Le milieu de la bande est après deux des quatre parts égales et après une des deux moitiés.',f'Oui : ${f(2,4)}={f(1,2)}$.'),
    Q('Combien de quarts composent un tout ?','Compte les quatre parts égales de la première bande.',f'Le tout contient quatre quarts : ${f(4,4)}=1$.','4 quarts.'),
    Q('Combien de moitiés composent un tout ?','Compte les deux parts égales de la seconde bande.',f'Le tout contient deux moitiés : ${f(2,2)}=1$.','2 moitiés.'),
    Q('Une seule part d’un quart est-elle plus petite qu’une moitié ?','Le partage en quatre donne des parts plus petites que le partage en deux.','Deux quarts couvrent une moitié, donc un seul quart n’en couvre que la moitié.',f'${f(1,4)}<{f(1,2)}$.'),
    Q('Que doit-on vérifier avant de superposer les parts ?','L’égalité des fractions se vérifie avec des touts identiques.','Si une bande entière est plus grande, les morceaux ne permettent plus la même comparaison.','Les bandes entières doivent être identiques.')))
    write(19,its)

def frac_operation(title,a,c,b,op,intro):
    v=a+c if op=='+' else a-c
    operation=f(a,b)+op+f(c,b)
    return E(title,intro,
    Q('Quel est le dénominateur commun et que signifie-t-il ?','Les parts à réunir ou à enlever doivent appartenir au même tout et avoir la même taille.',f'Le tout est partagé en {b} parts égales ; chaque part est un {WORDS[b]}.',f'Le dénominateur est {b}.'),
    Q('Combien de parts obtient-on après l’opération ?','Ajoute ou retire seulement le nombre de parts choisies.',f'On part de {a} parts et on '+('ajoute' if op=='+' else 'retire')+f' {c} parts : ${a}{op}{c}={v}$.',f'{v} parts.'),
    Q('Écris le calcul et la fraction obtenue.','Garde le dénominateur : la taille des parts ne change pas.',f'On a {v} parts sur les {b} parts du tout.',f'${operation}={f(v,b)}$.'),
    Q('Combien de parts manque-t-il pour compléter le tout ?','Retire le nombre de parts obtenues du nombre total de parts.',f'${b}-{v}={b-v}$.',f'${f(b-v,b)}$ : {b-v} parts.'),
    Q('Vérifie que la fraction obtenue et son complément reconstituent le tout.','Réunis les parts coloriées et les parts encore libres.',f'${v}+{b-v}={b}$ : toutes les parts sont réunies.',f'${f(v,b)}+{f(b-v,b)}=1$.'))

def calculer_fractions():
    its=[frac_operation('Réunir des sixièmes',1,3,6,'+','On réunit un sixième et trois sixièmes du même tout, sans recouvrir deux fois une part.\n\n[IMAGE_1]'),
    frac_operation('Des huitièmes et des dixièmes',2,3,8,'+',f'Calcule ${f(2,8)}+{f(3,8)}$, puis ${f(4,10)}+{f(2,10)}$. Les questions 1, 2, 4 et 5 portent sur le premier calcul.'),
    frac_operation('Enlever des parts',5,2,6,'-',f'Calcule ${f(5,6)}-{f(2,6)}$, puis ${f(3,5)}-{f(1,5)}$. Les questions 1, 2, 4 et 5 portent sur le premier calcul.')]
    its[1]['questions'][2]=Q('Calcule les deux sommes.','Compte les parts de même taille dans chaque somme ; garde leur dénominateur.',f'$2+3=5$ donc ${f(2,8)}+{f(3,8)}={f(5,8)}$. $4+2=6$ donc ${f(4,10)}+{f(2,10)}={f(6,10)}$.',f'${f(5,8)}$ ; ${f(6,10)}$.')
    its[2]['questions'][2]=Q('Calcule les deux différences.','Retire le nombre de parts et garde la taille de chaque part.',f'$5-2=3$ et $3-1=2$. Les parts restent respectivement des sixièmes et des cinquièmes.',f'${f(5,6)}-{f(2,6)}={f(3,6)}$ ; ${f(3,5)}-{f(1,5)}={f(2,5)}$.')
    its.append(E('Compléter jusqu’au tout',f'On cherche les fractions manquantes : ${f(2,5)}+\\ldots=1$ et ${f(3,8)}+\\ldots=1$.',
    Q('Combien de cinquièmes forment le tout ?','Écris le tout avec le dénominateur 5.',f'Le tout comporte cinq parts égales : ${f(5,5)}=1$.','5 cinquièmes.'),
    Q('Quel complément faut-il ajouter à deux cinquièmes ?','Compte les parts manquantes : cinq en tout moins deux déjà prises.','$5-2=3$.',f'${f(3,5)}$.'),
    Q('Quel complément faut-il ajouter à trois huitièmes ?','Écris le tout comme huit huitièmes et retire les trois parts déjà prises.','$8-3=5$.',f'${f(5,8)}$.'),
    Q('Vérifie la première somme.','Réunis les deux parts déjà prises et les trois parts ajoutées.',f'${f(2,5)}+{f(3,5)}={f(5,5)}=1$.',f'${f(2,5)}+{f(3,5)}=1$.'),
    Q('Vérifie la deuxième somme.','Réunis les trois parts déjà prises et les cinq parts ajoutées.',f'${f(3,8)}+{f(5,8)}={f(8,8)}=1$.',f'${f(3,8)}+{f(5,8)}=1$.')))
    its.append(frac_operation('Les quatre quarts du tout',3,1,4,'+',f'On réunit ${f(3,4)}$ et ${f(1,4)}$ d’un même tout.'))
    its.append(frac_operation('Deux couleurs sur dix parts',4,3,10,'+','Une bande contient dix parts égales. Quatre sont bleues et trois autres sont vertes. Quelle fraction est coloriée ?\n\n[IMAGE_1]'))
    item=frac_operation('Le reste en rouge',10,3,10,'-',f'Lina colorie ${f(3,10)}$ d’une figure en bleu et le reste en rouge. Quelle fraction est rouge ?')
    item['questions'][2]['question']='Quelle fraction est rouge ? Écris le calcul.'
    its.append(item)
    item=frac_operation('Les parts restent des quarts',1,2,4,'+',f'Noé écrit ${f(1,4)}+{f(2,4)}={f(3,8)}$. Explique et corrige.')
    item['questions'][2]=Q('Corrige le calcul de Noé et explique son erreur.','Le dénominateur décrit la taille des parts ; une addition ne change pas ce partage.','On réunit un quart et deux quarts : $1+2=3$. Les morceaux restent des quarts, on ne les transforme pas en huitièmes.',f'${f(1,4)}+{f(2,4)}={f(3,4)}$.')
    # Ne pas conserver l’égalité fausse comme calcul affirmé dans l’énoncé.
    item['enonce']='Noé affirme : « Un quart plus deux quarts font trois huitièmes. » Explique et corrige.'
    its.append(item)
    its.append(E('Fabriquer quatre sixièmes','Avec des morceaux d’un même tout partagé en six parts égales, on veut obtenir quatre sixièmes par addition.',
    Q('Propose une somme avec un sixième comme premier terme.','Cherche combien de parts ajouter à une part pour en obtenir quatre.','$4-1=3$ : il faut ajouter trois parts.',f'${f(1,6)}+{f(3,6)}={f(4,6)}$.'),
    Q('Propose une somme de deux fractions égales.','Partage les quatre parts à réunir en deux groupes égaux.','$2+2=4$ : deux parts dans chaque groupe.',f'${f(2,6)}+{f(2,6)}={f(4,6)}$.'),
    Q('Pourquoi garde-t-on le dénominateur 6 ?','Les morceaux proviennent tous du même partage en six parts égales.','Le nombre de morceaux pris change, tandis que la taille d’un morceau reste un sixième.','Les parts restent des sixièmes.'),
    Q('Quel complément manque-t-il pour retrouver le tout ?','Le tout contient six parts et quatre sont déjà prises.','$6-4=2$.',f'${f(2,6)}$.'),
    Q('Vérifie le complément.','Réunis les quatre parts choisies et les deux restantes.',f'${f(4,6)}+{f(2,6)}={f(6,6)}=1$.',f'${f(4,6)}+{f(2,6)}=1$.')))
    write(20,its)

def data_questions(labels,counts):
    total=sum(counts);imax=counts.index(max(counts));imin=counts.index(min(counts));hi=max(counts);lo=min(counts)
    return [Q('Complète le tableau des effectifs.','Regroupe les réponses identiques ; une personne produit une seule marque.','Compte séparément chaque choix : '+', '.join(f'{l} : {v}' for l,v in zip(labels,counts))+'.',table(['Choix','Effectif'],list(zip(labels,counts)))),
    Q('Combien de personnes ont répondu ?','Additionne tous les effectifs ; chaque réponse doit être comptée une fois.','$'+'+'.join(map(str,counts))+f'={total}$.',f'{total} personnes.'),
    Q('Construis un diagramme en barres : une case représente une personne.','Nomme chaque barre et colorie autant de cases que l’effectif de ce choix.','L’échelle va de un en un. Les hauteurs doivent être '+', '.join(f'{v} pour {l}' for l,v in zip(labels,counts))+'.','Barres de hauteurs '+', '.join(map(str,counts))+', dans l’ordre des choix.'),
    Q('Quel choix est le plus fréquent ?','Compare les hauteurs ou les effectifs, sans comparer la longueur des mots. ',f'Le plus grand effectif est {hi}, pour {labels[imax]}.',f'{labels[imax]} : {hi} réponses.'),
    Q('Quel écart sépare le choix le plus fréquent du moins fréquent ?','Retire le plus petit effectif du plus grand.',f'${hi}-{lo}={hi-lo}$.',f'{hi-lo} réponses.')]

def enquetes():
    its=[]
    labels=['Lecture','Dessin','Ballon'];c=[4,3,5]
    raw='Lecture, Ballon, Dessin, Ballon, Lecture, Dessin, Lecture, Ballon, Dessin, Ballon, Lecture, Ballon.'
    for i,title in enumerate(['Recueillir une réponse par personne','Des marques au tableau','Dessiner les barres','Annoncer le choix préféré','Contrôler les deux totaux','Une seule réponse autorisée','Préparer une nouvelle enquête','Deux représentations des réponses','Ce que raconte une hauteur'],1):
        ll=labels if i<=6 else ['Pomme','Poire','Banane'];cc=c if i<=6 else [6,4,3]
        qs=data_questions(ll,cc)
        intro='Douze personnes ont répondu à la question « Quelle activité préfères-tu : lecture, dessin ou ballon ? » Une seule réponse est autorisée.\n\n'+raw if i<=6 else 'Treize personnes répondent à la question « Quel fruit préfères-tu : pomme, poire ou banane ? » Chacune choisit un seul fruit.\n\n'+table(['Réponse','Marques'],[['Pomme','I I I I I I'],['Poire','I I I I'],['Banane','I I I']])
        if i==1:
            intro='Mène une enquête auprès de 6 à 12 personnes sur leur préférence : lecture, dessin ou ballon. Une seule réponse est autorisée. Pour les questions 2 à 5, utilise le relevé d’exemple ci-dessous, recueilli auprès de douze personnes.\n\n'+raw
            qs[0]=Q('Pose la question à 6 à 12 personnes et note les réponses, une marque par personne.','Prépare trois lignes, puis demande à chaque personne de choisir une seule activité.','Ton relevé dépend des personnes interrogées. Il doit compter une marque par personne. Dans l’exemple fourni, on obtient quatre marques pour Lecture, trois pour Dessin et cinq pour Ballon.','Un relevé personnel de 6 à 12 marques, une par personne. Exemple fourni :\n\n'+table(['Choix','Marques'],[['Lecture','I I I I'],['Dessin','I I I'],['Ballon','I I I I I']]))
        if i==3:intro+='\n\n[IMAGE_1]'
        if i==4:
            qs[0]=Q('Annonce le choix le plus fréquent avec son effectif.','Compte d’abord les réponses pour comparer des quantités précises.','Lecture reçoit 4 réponses, Dessin 3 et Ballon 5. Le plus grand effectif est 5.','Ballon : 5 réponses.')
            qs[3]=Q('Dessin est-il à égalité avec Lecture ?','Deux choix sont à égalité seulement si leurs effectifs sont égaux.','$3<4$ : les deux effectifs sont différents.','Non : Dessin a 3 réponses et Lecture 4.')
        if i==5:
            qs[4]=Q('Le graphique a 11 cases coloriées au total. Peut-il être correct ?','Le total des cases doit être le même que le total des réponses.','$4+3+5=12$ ; $12-11=1$. Il manque une case, mais il faut comparer chaque barre au tableau pour savoir laquelle corriger.','Non : il doit y avoir 12 cases coloriées, il manque 1 case.')
        if i==6:
            intro+='\n\nUne treizième personne répond d’abord « lecture et dessin ». Sa réponse n’est pas encore ajoutée au relevé.'
            qs[0]=Q('Que dois-tu lui demander avant d’ajouter sa réponse ?','La règle autorise un seul choix par personne.','Compter deux choix ajouterait deux réponses pour une seule personne et fausserait le total.','Lui demander de choisir une seule activité ; compter ensuite une seule réponse.')
            qs[4]=Q('Cette personne choisit finalement Lecture. Quels sont les nouveaux effectifs et le total ?','Ajoute une seule réponse à Lecture et conserve les autres effectifs.','$4+1=5$ ; $5+3+5=13$.','Lecture : 5 ; Dessin : 3 ; Ballon : 5 ; total : 13.')
        if i==7:
            qs[0]=Q('Écris la question d’enquête et les trois choix possibles.','Une question claire doit permettre une seule réponse parmi des choix distincts.','Les choix Pomme, Poire et Banane sont des fruits différents et chaque personne en choisit un.','Quel fruit préfères-tu : pomme, poire ou banane ?')
        if i==8:
            intro+='\n\n[IMAGE_1]'
            qs[4]=Q('Comment vérifier que le tableau et les barres racontent les mêmes résultats ?','Compare chaque barre à sa ligne, puis compare les totaux.','Les hauteurs doivent être 6, 4 et 3 ; $6+4+3=13$ cases au total. Un total juste ne suffit pas si deux barres ont été échangées.','Pomme : 6 ; Poire : 4 ; Banane : 3 ; total : 13.')
        if i==9:
            qs[0]=Q('Explique ce que représente la hauteur de la barre Pomme.','Relie le nom de la barre à l’échelle d’une personne par case.','La barre Pomme contient six cases ; chacune représente une réponse pour ce fruit.','La hauteur 6 représente les 6 personnes qui ont choisi Pomme.')
        qs[2]['etapes'].append('[IMAGE_2]' if i in [3,8] else '[IMAGE_1]')
        its.append(ex(title,intro,qs))
    write(31,its)

def lire_donnees():
    tbl=table(['Déplacement','Lundi','Mardi'],[['À pied',8,10],['À vélo',5,7]])
    graph='Les barres représentent les votes pour une activité : Lecture, Dessin ou Ballon. Une graduation vaut un vote.\n\n[IMAGE_1]'
    base_table=[
    Q('Combien d’élèves viennent à vélo le mardi ?','Croise la ligne À vélo avec la colonne Mardi.','La case au croisement de ces deux étiquettes contient 7.','7 élèves.'),
    calc('Combien d’élèves viennent à pied ou à vélo le lundi ?','8+5',13,'élèves',m='Additionne les deux effectifs de la colonne Lundi.'),
    calc('Combien d’élèves viennent à pied ou à vélo le mardi ?','10+7',17,'élèves',m='Additionne les deux effectifs de la colonne Mardi.'),
    Q('Quel jour compte le plus d’élèves à vélo ? Quel est l’écart ?','Compare les deux cases de la ligne À vélo.','Mardi compte 7 élèves contre 5 lundi ; $7-5=2$.','Mardi, avec 2 élèves de plus.'),
    calc('De combien le total du mardi dépasse-t-il celui du lundi ?','17-13',4,'élèves',m='Compare les totaux des colonnes, et non une seule ligne.')]
    titles=['La bonne case du tableau','Le total du lundi','Comparer les deux jours','Le vote préféré','Le nombre de votants','L’écart entre deux jeux','Le total du mardi','Des barres sans noms','Inventer deux questions']
    its=[]
    import copy
    for i,title in enumerate(titles,1):
        if i in [4,5,6,8]:
            qs=data_questions(['Lecture','Dessin','Ballon'],[4,3,6]);intro=graph
            qs[0]=Q('Quel jeu reçoit le plus de votes ? Combien de votes vont à Dessin ?','Lis le nom sous chaque barre et sa hauteur sur l’échelle.','Les hauteurs sont 4 pour Lecture, 3 pour Dessin et 6 pour Ballon. Six est le plus grand effectif.','Ballon : 6 votes ; Dessin : 3 votes.')
            qs[2]=Q('Combien de votes de plus vont à Ballon qu’à Dessin ?','Calcule l’écart entre les deux hauteurs.','$6-3=3$.','3 votes.')
            qs[3]=Q('Combien de votes vont à Lecture ?','Repère la barre Lecture, puis lis sa hauteur sur l’échelle.','Le sommet de la barre Lecture correspond à la graduation 4.','4 votes.')
            qs[4]=Q('Deux nouvelles personnes choisissent Dessin. Quel est le nouveau total des votes ?','Ajoute les deux nouveaux votes au total précédent.','$4+3+6=13$ puis $13+2=15$.','15 votes.')
            if i==5:qs[0],qs[1]=qs[1],qs[0]
            if i==6:qs[0],qs[2]=qs[2],qs[0]
            if i==8:
                intro='Un premier graphique a des barres de hauteurs 4, 3 et 6, mais aucun nom sous les barres. On fournit ensuite le graphique complet ci-dessous.\n\n[IMAGE_1]'
                qs[0]=Q('Pourquoi le premier graphique ne permet-il pas de savoir qui a reçu 6 votes ?','Une hauteur donne un effectif ; le nom de la barre indique ce qui a été compté.','Sans les noms, on ne peut pas associer 6 à Lecture, Dessin ou Ballon.','Il manque les noms des choix sous les barres.')
        else:
            intro='Le tableau indique les élèves venant à pied ou à vélo, pour chaque jour.\n\n'+tbl
            qs=copy.deepcopy(base_table)
            if i==2:qs[0],qs[1]=qs[1],qs[0]
            if i==3:qs[0],qs[3]=qs[3],qs[0]
            if i==7:qs[0],qs[2]=qs[2],qs[0]
            if i==9:
                qs[0]=Q('Invente une question dont la réponse se lit dans une seule case, puis réponds.','Choisis une ligne et une colonne précises.','La ligne À vélo et la colonne Lundi se croisent sur 5.','Combien d’élèves viennent à vélo lundi ? 5 élèves.')
                qs[1]=Q('Invente une question demandant une addition, puis réponds.','Réunis les deux déplacements pour un même jour.','La colonne Mardi contient 10 et 7 : $10+7=17$.','Combien viennent à pied ou à vélo mardi ? 17 élèves.')
        its.append(ex(title,intro,qs))
    write(32,its)

COURS={
1:(
'Prépare 2 plaques de 100, 3 barres de 10 et 4 unités. Remplace les 3 barres par 30 cubes : la quantité ne change pas. Lis le nombre 234.',
['Je compte les centaines, puis les dizaines, puis les unités.','J’écris un chiffre à chaque rang, même si une colonne est vide.','Je lis les centaines puis ce qui reste. Dix centaines se lisent mille.'],
'Dans 234, les 2 centaines donnent 200, les 3 dizaines donnent 30 et les 4 unités donnent 4.\n\n$234=200+30+4$.\n\nOn lit « deux-cent-trente-quatre ». Dans 204, le zéro garde la place des dizaines : $204=200+0+4$.',
'Écris trois-cent-six en chiffres, puis explique le zéro.',
'306 : 3 centaines, aucune dizaine isolée et 6 unités. $306=300+0+6$.',
'Ne confonds pas 306 et 360 : dans 306, le 6 vaut six unités ; dans 360, il vaut six dizaines.'),
2:(
'Prépare 2 centaines, 4 dizaines et 3 unités. Échange une centaine contre dix dizaines. Tu as maintenant 1 centaine, 14 dizaines et 3 unités : toujours 243.',
['Je transforme chaque centaine en 100 et chaque dizaine en 10.','Je regroupe dix unités en une dizaine, puis dix dizaines en une centaine.','Je peux refaire les échanges dans l’autre sens pour trouver une autre représentation.'],
'5 centaines, 12 dizaines et 7 unités donnent $500+120+7=627$.\n\nLes 12 dizaines s’échangent contre 1 centaine et 2 dizaines. On obtient 6 centaines, 2 dizaines et 7 unités.\n\nDans 583, le chiffre des dizaines est 8, mais il y a $50+8=58$ dizaines entières et 3 unités.',
'Représente 305 sans utiliser de plaque de cent.',
'30 dizaines et 5 unités : $30\\times10+5=305$.',
'Le chiffre des dizaines et le nombre de dizaines entières ne sont pas la même chose. Dans 416, le chiffre est 1 mais il y a 41 dizaines entières.'),
3:(
'Écris 306 et 360 sur deux étiquettes. Les deux nombres ont trois centaines. Compare alors leurs dizaines : aucune dans 306, six dans 360.',
['Je compare les centaines ; si elles sont égales, je compare les dizaines, puis les unités.','Sur une ligne, je cherche combien vaut l’espace entre deux traits voisins.','Pour encadrer, je choisis une borne plus petite et une borne plus grande.'],
'$306<360$ car, après les trois centaines communes, 0 dizaine est inférieur à 6 dizaines.\n\nSur la ligne de 300 à 400, dix intervalles égaux donnent un pas de 10 : après 300 viennent 310, 320, 330.\n\n$500<568<600$ et $560<568<570$. Le second encadrement est plus précis.',
'Une ligne porte 240, 250, 260. Quel nombre est trois intervalles après 260 ?',
'Le pas est 10. On passe par 270, 280 puis 290 : $260+30=290$.',
'On compare d’abord les centaines : 490 est plus petit que 509, même si son chiffre des dizaines est plus grand.'),
4:(
'Aligne des jetons A, B, C, A, B, C. Montre le départ à gauche et compte les places à partir de 1. Le troisième et le sixième jeton portent C.',
['Pour un rang, je fixe le départ, le sens et la première place.','Pour un motif, je repère le plus petit groupe répété et je fais des groupes complets.','Pour une suite de nombres, je teste ce qui change entre deux nombres voisins.'],
'Dans A B C A B C…, trois lettres forment un motif. $20\\times3=60$ : la 60e lettre termine le vingtième motif, donc c’est C.\n\nDans 125 ; 135 ; 145…, on ajoute 10 : $145+10=155$.\n\nDans 2 ; 4 ; 8 ; 16…, on double : $16\\times2=32$.',
'Tu es 37e dans une file de 100 personnes. Combien sont devant toi et derrière toi ?',
'Devant : $37-1=36$. Derrière : $100-37=63$. Vérification : $36+1+63=100$.',
'Le rang 37 ne signifie pas qu’il y a 37 personnes devant toi : ta propre place compte parmi les 37 premières.'),
14:(
'Dessine une barre pour 245 objets. Une partie contient 128 objets et l’autre est inconnue. Les deux parties réunies doivent recouvrir exactement la barre du tout.',
['Je raconte l’histoire dans l’ordre : départ, changement, arrivée.','Je repère si je cherche le tout, une partie ou le départ.','Je réunis les parties pour le tout ; je retire une partie connue pour trouver l’autre.','Je vérifie en reconstruisant la situation avec ma réponse.'],
'360 perles, dont 145 vertes : les bleues sont la partie inconnue. $360-145=215$. Vérification : $145+215=360$.\n\nTu donnes 57 images et il en reste 186 : le départ doit être plus grand que le reste. Remets le don : $186+57=243$.\n\nTu reçois 48 cartes et tu en as 302 : le départ était plus petit. Retire le cadeau : $302-48=254$.',
'Un album de 500 places contient 367 photos. Combien de places sont libres ?',
'$500-367=133$ places libres. Avec $367+133=500$, on retrouve toutes les places.',
'Le mot « donne » ne commande pas toujours une soustraction : si tu cherches le départ, tu dois remettre ce qui a été donné.'),
15:(
'Dessine une barre de 148 objets, puis une autre avec la même première partie et 35 objets supplémentaires. La seconde barre représente la grande quantité.',
['Je nomme la petite et la grande quantité avant de calculer.','La grande quantité est la petite plus l’écart.','Pour trouver la petite quantité, je retire l’écart de la grande ; pour trouver l’écart, je retire la petite de la grande.'],
'Lina a 125 cartes ; Noé en a 28 de plus. Noé en a davantage : $125+28=153$.\n\nMila a 304 perles, soit 78 de plus que Zoé. Zoé en a moins que Mila : $304-78=226$.\n\nDeux écoles ont 238 et 196 élèves. Leur écart est $238-196=42$ élèves.',
'Un bac bleu a 175 cubes, soit 46 de moins que le bac rouge. Combien le bac rouge contient-il de cubes ?',
'Le bac rouge est le plus rempli. $175+46=221$ cubes. Vérification : $221-175=46$.',
'« De moins » ne veut pas toujours dire retirer : le bac bleu a moins que le rouge, donc on ajoute l’écart pour trouver le rouge.'),
16:(
'Pars de 83 jetons. Ajoute 25 jetons, puis retire-en 46. Garde une trace de la quantité après l’ajout avant de faire le retrait.',
['Je cherche une première quantité nécessaire mais encore inconnue.','Je calcule cette quantité et j’écris ce qu’elle représente.','Je réutilise ce résultat dans le second calcul.','Je réponds avec l’unité et je vérifie les deux étapes.'],
'Il y a 125 livres ; on en apporte 38 puis on en prête 47.\n\nAprès l’apport : $125+38=163$ livres.\n\nAprès le prêt : $163-47=116$ livres.\n\nPour un achat de six crayons à 2 € et d’un cahier à 5 €, calcule d’abord tous les crayons : $6\\times2=12$, puis $12+5=17$ €. Le nombre de crayons n’est pas leur prix.',
'Un bus transporte 43 voyageurs. 18 descendent puis 27 montent. Combien de voyageurs sont dans le bus ?',
'Après la descente : $43-18=25$. Après la montée : $25+27=52$ voyageurs.',
'Ne mélange pas le nombre d’objets et leur prix. Pour quatre livres à 5 €, la dépense est $4\\times5=20$ €, pas 4 €.'),
17:(
'Prépare 24 jetons en quatre groupes de six. Tu peux demander soit le nombre de groupes, soit le contenu de chaque groupe : la réponse ne porte pas sur la même chose.',
['Je repère ce qui est connu : le nombre de parts ou la taille d’un groupe.','Je cherche un produit donnant le total, ou le plus grand produit qui ne le dépasse pas.','Je calcule le reste et je vérifie qu’il est plus petit qu’un groupe.','Je relis la question : tous les objets doivent-ils être rangés, ou seulement les groupes complets comptent-ils ?'],
'36 cartes partagées entre quatre enfants : $4\\times9=36$, donc 9 cartes chacun.\n\n41 œufs, boîtes complètes de six : $6\\times6=36$ et $41-36=5$. On vend 6 boîtes ; les 5 œufs restants ne font pas une boîte complète.\n\n25 photos sur des pages de dix places : deux pages pleines et cinq photos restantes exigent une troisième page.',
'On range 189 images sur des pages de dix places. Combien de pages faut-il ?',
'$18\\times10=180$ et $189-180=9$. Il faut 19 pages pour ranger aussi les 9 images restantes.',
'Le reste ne donne pas automatiquement une unité de réponse en plus : une page supplémentaire est nécessaire pour tout ranger, mais on ne vend pas une boîte incomplète.'),
18:(
'Prends une bande en papier. Plie-la en deux parts égales ; une part est un demi. Repars d’une autre bande et partage-la en quatre parts égales ; une part est un quart.',
['Je désigne le tout avant le partage.','Je vérifie que toutes les parts sont égales.','Je compte le nombre total de parts égales, puis le nombre de parts choisies.'],
'La bande entière est partagée en quatre parts égales. Une part coloriée est un quart : $'+f(1,4)+'$.\n\nLe nombre du bas, 4, indique le nombre de parts égales du tout. Le nombre du haut, 1, indique une part choisie.\n\nOn lit $'+f(1,2)+'$ « un demi », $'+f(1,3)+'$ « un tiers », $'+f(1,4)+'$ « un quart », puis un cinquième, un sixième, un huitième ou un dixième.',
'Une bande est partagée en huit parts égales et une seule est coloriée. Nomme et écris la fraction coloriée.',
'Un huitième : $'+f(1,8)+'$. Le 8 décrit le partage du tout et le 1 la part coloriée.',
'Quatre morceaux inégaux ne forment pas des quarts. Il faut quatre parts égales du même tout.'),
19:(
'Prends deux bandes identiques partagées chacune en cinq parts égales. Colorie deux parts de la première et trois de la seconde. Aligne les bandes pour comparer.',
['Je vérifie que les touts sont identiques.','Je lis le numérateur, qui compte les parts prises, et le dénominateur, qui décrit le partage.','À même dénominateur, je compare le nombre de parts prises.','Pour deux fractions de numérateur 1, le partage en davantage de parts donne de plus petites parts.'],
'$'+f(2,5)+'<'+f(3,5)+'$ : les parts ont la même taille, mais trois parts sont plus que deux.\n\n$'+f(1,3)+'>'+f(1,6)+'$ : on prend une part dans chaque cas ; partager le même tout en six donne des parts plus petites que le partager en trois.\n\nQuand toutes les parts sont prises, on obtient le tout : $'+f(5,5)+'=1$.',
'Compare quatre huitièmes et trois huitièmes d’un même tout.',
'$'+f(4,8)+'>'+f(3,8)+'$ : quatre parts de même taille sont plus que trois.',
'Deux fractions se comparent ici avec un même tout ou des touts identiques. Une moitié d’une grande bande n’a pas forcément la même taille qu’une moitié d’une petite bande.'),
20:(
'Découpe une bande en cinq parts égales. Mets deux morceaux d’un côté et un autre à côté. Trois morceaux sur les cinq sont réunis ; la taille d’un morceau n’a pas changé.',
['Je vérifie que les parts concernent le même tout et ont le même dénominateur.','Pour ajouter ou enlever, je calcule sur les numérateurs.','Je garde le dénominateur, car les parts gardent leur taille.','Pour compléter le tout, je compte les parts qui manquent.'],
'$'+f(2,5)+'+'+f(1,5)+'='+f(3,5)+'$ : deux parts et une part font trois parts.\n\n$'+f(5,6)+'-'+f(2,6)+'='+f(3,6)+'$ : de cinq parts, on en retire deux.\n\nPour compléter $'+f(2,5)+'$ jusqu’au tout, il manque trois parts : $'+f(2,5)+'+'+f(3,5)+'=1$.',
'Calcule trois quarts plus un quart. Explique le résultat.',
'$'+f(3,4)+'+'+f(1,4)+'='+f(4,4)+'=1$. Les quatre quarts reconstituent le tout.',
'On n’ajoute pas les dénominateurs : un quart plus deux quarts fait trois quarts. Les morceaux restent des quarts.'),
31:(
'Pose une question avec des choix distincts : « Préfères-tu la lecture, le dessin ou le ballon ? » Prévois une seule réponse par personne. Note une marque par réponse dans la bonne ligne.',
['Je formule une question claire et des réponses possibles distinctes.','Je recueille une réponse par personne et je regroupe les marques par choix.','Je compte les marques pour remplir le tableau des effectifs.','Je dessine une barre par choix avec la même échelle pour toutes les barres.','Je vérifie chaque effectif et le total des cases.'],
'Douze personnes répondent : Lecture reçoit 4 réponses, Dessin 3 et Ballon 5.\n\n$4+3+5=12$ : le total des effectifs est bien celui des participants.\n\nAvec une case pour une personne, les barres ont les hauteurs 4, 3 et 5. Ballon est le choix le plus fréquent ; il dépasse Dessin de $5-3=2$ réponses.',
'Un graphique représente ces réponses avec des barres de 4, 3 et 4 cases. Est-il correct ?',
'Non : la barre Ballon doit avoir 5 cases. Le graphique contient seulement $4+3+4=11$ cases, au lieu de 12.',
'Une personne ne doit pas compter deux fois. Un total juste ne suffit pas : vérifie aussi que chaque barre correspond au bon choix.'),
32:(
'Lis les étiquettes d’un tableau avant les nombres. Pour « à vélo le mardi », suis la ligne À vélo et la colonne Mardi jusqu’à leur croisement.',
['Je lis le titre, les lignes, les colonnes ou les noms des barres.','Dans un tableau, je croise la bonne ligne et la bonne colonne.','Dans un graphique, je lis l’échelle avant la hauteur.','Pour un total, j’additionne les catégories concernées ; pour un écart, je soustrais leurs effectifs.'],
table(['Déplacement','Lundi','Mardi'],[['À pied',8,10],['À vélo',5,7]])+'\n\nÀ vélo le mardi : 7 élèves. Total du lundi : $8+5=13$ élèves. Total du mardi : $10+7=17$ élèves.\n\nPour comparer les cyclistes : $7-5=2$ ; il y en a deux de plus le mardi.',
'Un graphique donne Lecture : 4 votes, Dessin : 3 votes et Ballon : 6 votes. Combien de personnes ont voté ?',
'$4+3+6=13$ personnes. Les trois choix sont réunis pour trouver le total.',
'La plus haute barre indique le plus grand effectif ; son nom indique à quoi cet effectif correspond. Sans le nom ou l’échelle, la lecture est incomplète.')}

def cours_fiches():
    for code,(manip,method,worked,prompt,answer,warning) in COURS.items():
        d=next(R.glob(f'{code:02}_*'));s=json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf8'))
        definitions='\n\n'.join(s['lecon'])
        methodtext='\n'.join(f'{i}. {x}' for i,x in enumerate(method,1))
        course=f'''Titre: {s['titre']}

<!-- optitab:1 -->
::: objectifs
{s['objectif']}
:::

## I. Je construis et j’observe

::: methode Avec du matériel ou un dessin
{manip}
:::

[IMAGE_1]

## II. Je comprends

::: definition
{definitions}
:::

## III. Je sais faire

::: methode Les gestes pour réussir
{methodtext}
:::

::: exemple Un raisonnement expliqué
{worked}
:::

## IV. J’essaie et je vérifie

::: exemple À toi de chercher
{prompt}
:::

::: resultat Je vérifie
{answer}
:::

::: attention L’erreur à éviter
{warning}
:::

::: retenir
{definitions}
:::
'''
        fiche=f'''Titre: Résumé : {s['titre']}

<!-- optitab:1 -->
::: objectifs
{s['objectif']}
:::

## I. Les idées essentielles

::: retenir
{definitions}
:::

## II. Ma méthode

::: methode
{methodtext}
:::

## III. Un exemple à garder

{prompt}

::: resultat
{answer}
:::

::: attention
{warning}
:::
'''
        (d/'cours_nouveau.txt').write_text(course,encoding='utf8');(d/'fiche_nouvelle.txt').write_text(fiche,encoding='utf8')

def tikz(lines):return '\\begin{tikzpicture}[x=1cm,y=1cm,font=\\large,text=otInk,line width=.8pt]\n'+'\n'.join(lines)+'\n\\end{tikzpicture}'
def node(x,y,text,color='otInk',extra=''):return f'\\node[text={color}{","+extra if extra else ""}] at ({x},{y}) {{{text}}};'
def fraction_bands(rows,green=False,lengths=None,unequal=False):
    out=[]
    for row,(a,b,label) in enumerate(rows):
        y=(len(rows)-1-row)*1.55;w=(lengths or [7]*len(rows))[row]
        cuts=[0,1,2.5,5,7] if unequal else [i*w/b for i in range(b+1)]
        for j in range(b):
            color=('otGreen!35' if green else 'otNavy!25') if j<a else 'white'
            out.append(f'\\fill[{color}] ({cuts[j]},{y}) rectangle ({cuts[j+1]},{y+.55});')
        out.append(f'\\draw[otNavy] (0,{y}) rectangle ({w},{y+.55});')
        for cut in cuts[1:-1]:out.append(f'\\draw[otNavy] ({cut},{y}) -- ({cut},{y+.55});')
        if label:out.append(node(w/2,y-.35,label,'otGreenDark' if green else 'otInk'))
    return tikz(out)
def material(v):
    c,d,u=parts(v);out=[]
    for count,row,step,size,lab in [(c,2.5,1.05,.75,'centaines'),(d,1.3,.55,.3,'dizaines'),(u,.3,.42,.2,'unités')]:
        for i in range(count):out.append(f'\\draw[otNavy,fill=otSky] ({i*step},{row}) rectangle ({i*step+size},{row+(.65 if lab=="centaines" else .5 if lab=="dizaines" else .2)});')
        out.append(node(6,row+.2,f'{count} {lab}'))
    return tikz(out)
def place(v):
    c,d,u=parts(v);out=[]
    for i,(h,x) in enumerate(zip(['Centaines','Dizaines','Unités'],[c,d,u])):
        out.extend([f'\\draw[otNavy,fill=otSky] ({i*2.35},0) rectangle ({i*2.35+2.2},1.35);',node(i*2.35+1.1,1.9,h),node(i*2.35+1.1,.68,str(x))])
    return tikz(out)
def numberline(start,end,step,missing=(),point=None):
    out=[r'\draw[otNavy,-{Stealth}] (-.15,0) -- (7.9,0);'];intervals=(end-start)//step
    for i,v in enumerate(range(start,end+1,step)):
        x=i*7.5/intervals;out.append(f'\\draw[otNavy] ({x},-.08) -- ({x},.08);')
        out.append(node(x,-.43,'?' if v in missing else str(v),'otInk',r'font=\normalsize'))
        if v==point:out.extend([f'\\fill[otNavy] ({x},0) circle (2pt);',node(x,.45,'$A$')])
    return tikz(out)
def pattern(text):return tikz([node(i*.75,0,letter) for i,letter in enumerate(text)]+[node(2.6,-.65,'Départ à gauche ; rangs à partir de 1','otMuted',r'font=\normalsize')])
def bar(total,left,right='?',green=False):
    x=7*left/total;out=[r'\draw[otNavy,fill=otSky] (0,1.4) rectangle (7,1.95);',node(3.5,2.35,f'Tout : {total}'),f'\\draw[otNavy,fill=otSky] (0,0) rectangle ({x},.55);',f'\\draw[otNavy,fill={"otGreen!25" if green else "white"}] ({x},0) rectangle (7,.55);',node(x/2,-.4,str(left)),node((x+7)/2,-.4,str(right),'otGreenDark' if green else 'otInk')]
    return tikz(out)
def comparebars(s,delta,answer='?',green=False):
    total=s+delta;x=7*s/total
    return tikz([f'\\draw[otNavy,fill=otSky] (0,1.4) rectangle ({x},1.95);',node(x/2,2.35,str(s)),f'\\draw[otNavy,fill=otSky] (0,0) rectangle ({x},.55);',f'\\draw[otNavy,fill={"otGreen!25" if green else "white"}] ({x},0) rectangle (7,.55);',node((x+7)/2,-.4,f'Écart : {delta}'),node(x/2,-.4,str(s)),node(3.5,-1,f'Grande quantité : {answer}','otGreenDark' if green else 'otInk')])
def story(a,b,c,blank=False):
    mid=a+b;end=mid+c
    return tikz([node(0,0,str(a)),r'\draw[otNavy,-{Stealth}] (.65,0) -- (2.5,0);',node(1.6,.55,f'+{b}'),node(3.2,0,'?' if blank else str(mid),'otGreenDark' if not blank else 'otInk'),r'\draw[otNavy,-{Stealth}] (3.85,0) -- (5.7,0);',node(4.75,.55,str(c)),node(6.5,0,'?' if blank else str(end),'otGreenDark' if not blank else 'otInk')])
def groups(n,size,answer=False):
    out=[]
    for i in range(n):
        x=i*1.8;out.append(f'\\draw[otNavy,rounded corners=3pt] ({x},0) rectangle ({x+1.5},1.6);')
        for j in range(size):out.append(f'\\fill[{"otGreenDark" if answer else "otNavy"}] ({x+.4+(j%2)*.65},{.3+(j//2)*.45}) circle (2.2pt);')
    out.append(node(n*1.8/2-.15,-.45,f'{n} groupes de {size}'))
    return tikz(out)
def sharebar(total,n,answer=False):
    rows=[];w=7/n
    for i in range(n):rows.append(f'\\draw[otNavy,fill={"otGreen!25" if answer else "otSky"}] ({i*w},0) rectangle ({(i+1)*w},.6);');rows.append(node((i+.5)*w,-.4,str(total//n) if answer else '?','otGreenDark' if answer else 'otInk'))
    rows.append(node(3.5,1.1,f'{total} cartes, {n} parts égales'))
    return tikz(rows)
def graph(labels,counts,answer=False,blank=False):
    out=[];h=max(counts)+1
    for y in range(h+1):out.append(f'\\draw[otRule] (0,{y*.43}) -- (6.5,{y*.43});');out.append(node(-.35,y*.43,str(y),'otMuted',r'font=\normalsize'))
    out.extend([f'\\draw[otMuted] (0,0) -- (0,{h*.43+.15});',r'\draw[otMuted] (0,0) -- (6.5,0);'])
    for i,(label,count) in enumerate(zip(labels,counts)):
        x=.7+2*i
        if not blank:
            out.append(f'\\draw[draw={"otGreenDark" if answer else "otNavy"},fill={"otGreen!35" if answer else "otNavy!25"}] ({x},0) rectangle ({x+1},{count*.43});')
        out.append(node(x+.5,-.48,label,'otInk',r'font=\normalsize'))
    out.append(node(3.25,h*.43+.6,'Une graduation = une réponse','otMuted',r'font=\normalsize'))
    return tikz(out)

def figures():
    courses={1:material(234),2:place(243),3:numberline(300,400,10),4:pattern('ABCABC'),14:bar(245,128),15:comparebars(148,35),16:story(83,25,-46),17:groups(4,6),18:fraction_bands([(1,4,'Une part sur quatre parts égales')]),19:fraction_bands([(2,5,'Deux cinquièmes'),(3,5,'Trois cinquièmes')]),20:fraction_bands([(2,5,'Deux cinquièmes'),(1,5,'Un cinquième'),(3,5,'Trois cinquièmes réunis')]),31:graph(['Lecture','Dessin','Ballon'],[4,3,5]),32:graph(['Lecture','Dessin','Ballon'],[4,3,6])}
    extra={1:{1:[(material(325),'3 centaines, 2 dizaines et 5 unités') ]},2:{1:[(place(416),'Tableau : 4 centaines, 1 dizaine, 6 unités')]},3:{1:[(numberline(400,500,10,[420,450,480]),'Droite de 400 à 500 : trois étiquettes à compléter')],6:[(numberline(0,1000,100,point=600),'Point A placé sur la sixième graduation de cent')]},4:{1:[(pattern('ABABAB'),'Motif A B répété depuis la gauche')],4:[(pattern('ABCABC'),'Motif A B C répété depuis la gauche')]},14:{1:[(bar(360,145),'360 perles : 145 vertes et une partie bleue inconnue'),(bar(360,145,215,True),'Correction : 145 perles vertes et 215 bleues') ]},15:{1:[(comparebars(125,28),'125 cartes et 28 cartes supplémentaires'),(comparebars(125,28,153,True),'Correction : la grande collection contient 153 cartes')]},16:{1:[(story(125,38,-47,True),'125 livres, apport de 38 puis prêt de 47'),(story(125,38,-47),'Correction : 163 livres puis 116 livres')]},17:{1:[(sharebar(36,4),'36 cartes partagées en quatre parts égales'),(sharebar(36,4,True),'Correction : quatre parts de neuf cartes')]}}
    for code in COURS:
        d=next(R.glob(f'{code:02}_*'));fd=d/'figures';fd.mkdir(exist_ok=True)
        fs={'cours_schema':courses[code]};corr={'cours':{'nouveau':{'1':{'fichier':'cours_schema.png','alt':f'Schéma expliqué du cours : {json.loads((d/"sources_locales/chapitre.json").read_text(encoding="utf8"))["titre"]}'}}},'fiches':{},'exercices':{}}
        sets=extra.get(code,{})
        if code==18:
            for i,b,a in [(1,5,1),(2,2,0),(3,3,0),(6,6,1),(9,8,0)]:
                sets[i]=[(fraction_bands([(a,b,'Bande entière partagée en parts égales')]),f'Bande partagée en {b} parts égales, {a} coloriée'),(fraction_bands([(1,b,f'Un {WORDS[b]}')],True),f'Correction : une part sur {b} parts égales')]
            sets[2][0]=(fraction_bands([(0,1,'Bande entière à partager')]),'Bande entière sans séparation, à partager en deux parts égales')
            sets[7]=[(fraction_bands([(0,4,'Quatre morceaux inégaux')],unequal=True),'Quatre morceaux de tailles différentes'),(fraction_bands([(1,4,'Un quart : une part sur quatre parts égales')],True),'Correction du partage en quatre parts égales')]
        if code==19:
            for i,a,b,blank in [(1,3,8,False),(2,3,4,True)]:sets[i]=[(fraction_bands([(0 if blank else a,b,'Bande entière en parts égales')]),f'Bande en {b} parts égales'),(fraction_bands([(a,b,'$'+f(a,b)+'$')],True),f'Correction : {a} parts choisies sur {b}')]
            sets[4]=[(fraction_bands([(1,3,'Un tiers'),(1,6,'Un sixième')]),'Bandes identiques : un tiers et un sixième')]
            sets[8]=[(fraction_bands([(1,2,'Moitié de la petite bande'),(1,2,'Moitié de la grande bande')],lengths=[4,7]),'Moitiés de deux bandes entières de tailles différentes')]
            sets[9]=[(fraction_bands([(2,4,'Deux quarts'),(1,2,'Une moitié')]),'Deux quarts et une moitié de bandes identiques')]
        if code==20:
            sets[1]=[(fraction_bands([(1,6,'Une part choisie'),(3,6,'Trois autres parts choisies')]),'Un sixième et trois sixièmes à réunir sur un même tout'),(fraction_bands([(4,6,'Quatre sixièmes')],True),'Correction : quatre parts sur six sont réunies')]
            sets[6]=[(fraction_bands([(0,10,'Dix parts égales à colorier')]),'Bande partagée en dix parts égales'),(fraction_bands([(7,10,'Sept dixièmes coloriés')],True),'Correction : quatre parts bleues et trois autres parts donnent sept dixièmes')]
        if code==31:
            sets={}
            for i in range(1,10):
                labels=['Lecture','Dessin','Ballon'] if i<=6 else ['Pomme','Poire','Banane'];counts=[4,3,5] if i<=6 else [6,4,3]
                sets[i]=([(graph(labels,counts,blank=True),'Repère à compléter : une graduation par réponse')] if i in [3,8] else [])+[(graph(labels,counts,True),'Correction du diagramme : '+', '.join(f'{l} {v}' for l,v in zip(labels,counts)))]
        if code==32:sets={i:[(graph(['Lecture','Dessin','Ballon'],[4,3,6]),'Votes : Lecture 4, Dessin 3, Ballon 6')] for i in [4,5,6,8]}
        text=(d/'exercices.txt').read_text(encoding='utf8')
        blocks=text.split('===\n')
        for i,pics in sets.items():
            corr['exercices'][f'nouveau-{i}']={}
            for j,(fig,alt) in enumerate(pics,1):
                name=f'ex{i}_{"corrige" if j==2 or code==31 and not(i in [3,8] and j==1) else "schema"}'
                fs[name]=fig;corr['exercices'][f'nouveau-{i}'][str(j)]={'fichier':name+'.png','alt':alt}
            # Les corrigés ajoutés aux problèmes et coloriages sont placés après la question numérique utile.
            if len(pics)==2 and code!=31:
                bl=blocks[i]
                at=bl.find('::: resultat',bl.find('## Question 3'))
                if '[IMAGE_2]' not in bl:blocks[i]=bl[:at]+'[IMAGE_2]\n\n'+bl[at:]
        text='===\n'.join(blocks);(d/'exercices.txt').write_text(text,encoding='utf8')
        (fd/'figures.py').write_text('# -*- coding: utf-8 -*-\n"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""\nFIGURES = {\n'+''.join('    '+repr(k)+': r"""\n'+v+'\n""",\n' for k,v in fs.items())+'}\n',encoding='utf8')
        (fd/'correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

if __name__=='__main__':
    nombres();decomposition();comparer();suites();problemes_simples();comparer_quantites();deux_etapes();partager();decouvrir_fractions();lire_fractions();calculer_fractions();enquetes();lire_donnees();cours_fiches();figures()
