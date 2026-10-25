"""Livre CE1 original : construction, navigation et export des manifestes."""
from mise_en_page import *
from dessins import diagram

def couverture(b):
    c=b.c;b.page=1;b.current='couverture';b.dest['couverture']=1;b.pages.append(dict(numero=1,cle='couverture',titre='Couverture',adulte=False))
    c.bookmarkPage('couverture');c.setFillColor(NAVY);c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(HexColor('#122A66'));p=c.beginPath();p.moveTo(0,0);p.lineTo(W,0);p.lineTo(W,145*mm);p.curveTo(120*mm,105*mm,70*mm,150*mm,0,110*mm);p.close();c.drawPath(p,stroke=0,fill=1)
    c.drawImage(str(ASSETS/'logo-blanc.png'),20*mm,H-35*mm,width=48*mm,height=18*mm,preserveAspectRatio=True,mask='auto')
    b.text('LE LIVRE POUR APPRENDRE ET COMPRENDRE',20,49,172,10.3,bold=True,color=white)
    b.text('Mathématiques',20,68,174,35,leading=40,bold=True,color=white)
    b.text('CE1',18,92,174,82,leading=94,bold=True,color=white)
    b.text('Je cherche. Je représente.\nJe calcule. Je vérifie.',21,137,164,20,leading=27,color=white)
    b.rect(20,174,170,23,fill=HexColor('#244A9F'))
    b.text('32 chapitres illustrés · 288 exercices\n5 bilans · 360 problèmes oraux · Corrigés',26,180,159,13.4,leading=19,color=white)
    b.rect(20,216,170,37,fill=white)
    b.fig(('array',[3,4]),218,32,x=25,w=70)
    b.text('3 × 4 = 12',113,228,69,21,bold=True,color=NAVY)
    b.text('COLLECTION OPTITAB',20,267,120,10,bold=True,color=white)
    b.text('France · Édition 2026-2027',20,273,170,11,color=white)
    b.outline('Bienvenue dans le livre de CE1','couverture')

def liminaires(b):
    b.begin('bienvenue','Mon livre de mathématiques','BIENVENUE EN CE1',subtitle='Des objets, des schémas et des mots pour comprendre.')
    b.box('CE LIVRE APPARTIENT À','Prénom : ........................................................\nClasse : ............................................................',82,40)
    t=136
    for lab,body in [('Je cherche','Je peux manipuler, faire un dessin et garder mes essais.'),('Je représente','Je choisis un schéma qui montre les informations utiles.'),('Je calcule','Je choisis une méthode adaptée aux nombres.'),('Je vérifie','Je relis la question, je contrôle le résultat et je l’explique.')]:
        b.text(lab,22,t,165,16,bold=True,color=GREEN);t=b.text(body,22,t+11,165,14)+10
    b.begin('mode','Comment utiliser ce livre','POUR L’ADULTE',adult=True)
    sections=[('Un chapitre, plusieurs moments','Manipuler et verbaliser pendant la découverte ; expliquer la leçon ; faire quelques exercices puis y revenir. Les trois pages d’exercices ne forment pas une séance unique. Les bilans se proposent aussi en plusieurs temps.'),('Accompagner la lecture','Lire les énoncés lorsque le décodage freine l’enfant. Faire reformuler l’histoire et la question. Accepter les gestes, les objets ou une réponse orale avant de demander une trace écrite.'),('Faire comprendre les méthodes','Relier les objets, les schémas et les calculs. Montrer une procédure, accompagner un premier essai puis proposer une situation proche. Les corrigés donnent une démarche possible et des critères pour les activités ouvertes.'),('Observer les besoins','Demander « Comment as-tu fait ? ». Revenir à un cas plus simple si nécessaire, puis reprendre le même objectif un autre jour. Les points de vigilance et les pistes d’aide figurent avec les corrigés.'),('Organiser l’année','Au moins deux tiers du temps sont consacrés aux nombres, au calcul et aux problèmes. Alterner les autres domaines. Les chapitres sont rangés pour retrouver une notion ; la page suivante précise les périodes et les reprises.'),('Imprimer et manipuler','A4, taille réelle à 100 %, sans ajustement. Contrôler le repère de 5 cm dans les outils. Photocopier les pages de matériel. Les couleurs servent de repères ; les traits et légendes restent utilisables en noir et blanc.')]
    t=81
    for title,body in sections:
        b.text(title,19,t,172,12.6,bold=True,color=GREEN);t=b.text(body,19,t+8,172,11.3,leading=15)+7
    b.begin('progression','Une progression sur cinq périodes','POUR L’ADULTE',adult=True)
    periods=[('P1 · Entrer dans le CE1','Centaine dès le début (1-2), comparaison et rangs (3-4), calculs mentaux et addition posée (5-7). Commencer la multiplication et les premières tables (9-10). Problèmes (14-15), mesures concrètes (21-22), formes et repérage (26, 30).'),('P2 · Étendre et représenter','Atteindre 1 000 au plus tard en P2 (1-3). Poursuivre les tables et multiplier par 10 (9-12). Fractions unitaires dès P2 (18). Introduire les centimes au plus tard en P2 (23). Cercles, alignements et milieux (27). Poursuivre les problèmes (14-17).'),('P3 · Structurer les procédures','Soustraction posée au plus tard en P3 (8), doubles et moitiés (13), construction progressive des autres tables (11). Fractions non unitaires (19), prix à virgule dès P3 (23), heures et quarts d’heure (24), solides (29).'),('P4 · Comparer, calculer et construire','Comparaisons de fractions au plus tard dès P4 (19) et calculs de fractions (20). Problèmes mixtes et partages (16-17), durées (25), constructions (28), données et tableaux (31-32). Reprendre les méthodes déjà rencontrées.'),('P5 · Consolider et transférer','Reprises ciblées dans tous les domaines, problèmes nouveaux, enquêtes et jeux. Renforcer les faits numériques et l’autonomie. Le bilan final est réparti sur plusieurs séances et sert à choisir les dernières reprises.')]
    t=81
    for title,body in periods:
        b.text(title,19,t,172,12.5,bold=True,color=GREEN);t=b.text(body,19,t+8,172,11.2,leading=15)+8
    b.box('LES PROBLÈMES DE LA SEMAINE','La banque comprend 36 semaines de 10 histoires à lire. Adapter les nombres aux acquis et choisir les problèmes en lien avec les notions enseignées.',242,32,size=11.3)
    for part in range(2):
        b.begin(f'sommaire-{part+1}','Sommaire' if part==0 else 'Sommaire et ressources','PARCOURS DU LIVRE',subtitle='Les titres et les numéros de page sont cliquables.')
        if part==0:b.outline('Sommaire','sommaire-1')
        t=82
        for ch in CHAPITRES[part*16:(part+1)*16]:
            key=f'ch-{ch.numero}-decouverte';b.text(f'{ch.numero:02}',19,t,12,11.6,bold=True,color=GREEN);b.text(ch.titre,34,t,142,11.8);b.text(str(b.refs.get(key,'…')),179,t,14,11.6,bold=True,color=NAVY);b.link(key,18,t,176,8);t+=9
        if part:
            t+=5
            for title,key in [('Les cinq bilans','bilan-1-1'),('Les corrigés expliqués','corriges-intro'),('360 problèmes oraux pour l’adulte','oral-intro'),('Matériel et fiches outils','outils-intro'),('Programme et sources','programme-1')]:
                b.text(title,20,t,155,11.3,bold=True,color=NAVY);b.text(str(b.refs.get(key,'…')),179,t,15,11.3);b.link(key,18,t,176,8);t+=8
    b.begin('rituels','Des reprises qui font progresser','POUR L’ADULTE',adult=True)
    t=82
    for title,body in [('Les faits numériques','Reprendre les additions dans les deux sens et les tables de multiplication en ordre varié. Demander aussi un terme ou un facteur manquant. Les tables se construisent sur toute l’année.'),('Des procédures explicites','Ajouter 9, 19, 29 ; enlever 9 ; franchir une dizaine ; multiplier par 10 ; décomposer un facteur de 11 à 19 ; chercher une moitié. Faire nommer les étapes et alléger progressivement les traces.'),('La fluence en fin de CE1','Repères du programme : 12 égalités d’addition en 1 minute ; 8 égalités de multiplication en 1 minute ; 8 faits multiplicatifs usuels en 1 minute ; 12 calculs par procédure en 3 minutes. Les fiches outils se proposent après l’apprentissage.'),('L’évaluation sert à aider','Comparer les progrès de l’enfant à ses propres réussites précédentes. Les temps limités ne remplacent ni l’enseignement des méthodes ni l’observation des raisonnements. Maintenir les adaptations habituelles.'),('Les histoires à résoudre','Lire sans annoncer l’opération. Demander une représentation, une réponse avec l’unité et un contrôle. Les problèmes de la banque ne remplacent pas les autres situations de la semaine.')]:
        b.text(title,19,t,172,12.8,bold=True,color=GREEN);t=b.text(body,19,t+9,172,11.7,leading=15.6)+10
    b.begin('suivi','Mes progrès au fil de l’année','À COMPLÉTER AVEC L’ADULTE',subtitle='Je peux réussir avec du matériel, avec un schéma, puis de façon autonome.')
    t=83
    for label in ['Lire et représenter jusqu’à 1 000','Comparer et placer les nombres','Expliquer une addition ou une soustraction','Calculer avec une méthode','Retrouver les résultats des tables','Lire et représenter des fractions','Résoudre une histoire en une ou deux étapes','Utiliser des mesures et la monnaie','Lire l’heure et calculer une durée','Construire avec la règle, l’équerre et le compas','Décrire un solide et suivre un plan','Construire et lire des tableaux et graphiques']:
        b.text(label,20,t,138,12);b.c.setStrokeColor(RULE)
        for x in [165,176,187]:b.c.rect(x*mm,H-(t+4)*mm,4*mm,4*mm)
        b.line(19,t+10,193);t+=14
    b.text('Trois observations à des dates différentes :\n........................ / ........................ / ........................',20,258,172,10.7,color=MUTED)

def exercices_page(b,items,start=1,chapter=None):
    t=83
    for j,e in enumerate(items):
        num=start+j;b.rect(17,t,9,9,fill=NAVY,r=2);b.text(str(num),19,t+1.2,6,12,bold=True,color=white)
        end=b.text(e.consigne,30,t,160,13.7,leading=18.1,maxbottom=t+28)
        if chapter:b.link(f'cor-{chapter}',17,t,9,9)
        if e.figure:
            height=44 if e.figure[0]=='column3blank' else 39
            b.fig(e.figure,end+2,height,x=28,w=160);bottom=end+height+4
            if bottom<t+61:b.lines(bottom+1,h=max(0,t+61-bottom-1),x=31,w=157)
        elif any(word in e.consigne.lower() for word in ['trace','dessine','construis','reproduis']):
            b.rect(30,end+8,159,max(14,t+60-end-8),fill=white,stroke=RULE,r=0)
        else:b.lines(end+12,h=max(8,t+58-end-12),x=31,w=157)
        if j<len(items)-1:b.line(17,t+65,193)
        t+=67

def chapitre(b,ch):
    n=ch.numero;key=f'ch-{n}-decouverte'
    b.begin(key,ch.titre,f'CHAPITRE {n:02} · {ch.domaine}',subtitle='Je découvre avec des objets et des schémas.');b.outline(f'{n:02}. {ch.titre}',key)
    b.box('MON OBJECTIF',ch.objectif,83,29,size=13.7)
    b.text('Je prépare',20,121,169,12,bold=True,color=GREEN);b.text(ch.materiel,20,130,169,12.7)
    b.box('JE MANIPULE ET JE RACONTE',ch.manipulation,151,49,fill=MINT,size=13.7)
    b.fig(ch.figure,207,48)
    footer='Observe le schéma. Montre ce que tu reconnais et explique-le.'
    if n==18:footer='Dans les phrases, 1/4 note aussi la fraction écrite avec une barre horizontale sur le schéma.'
    b.text(footer,22,263,166,11.7,color=MUTED)
    b.begin(f'ch-{n}-lecon',ch.titre,f'CHAPITRE {n:02} · JE RETIENS',subtitle='Je comprends, puis j’essaie avec l’adulte.')
    t=83
    for i,rule in enumerate(ch.lecon,1):
        b.rect(17,t,176,29,fill=PALE if i%2 else MINT);b.text(str(i),22,t+6,10,16,bold=True,color=GREEN);b.text(rule,35,t+5,151,13.5,maxbottom=t+27);t+=33
    b.box('UN EXEMPLE EXPLIQUÉ',ch.exemple,185,43,fill=CREAM,size=12.8)
    b.box('À TOI, AVEC L’ADULTE',ch.guide,235,37,fill=MINT,size=13.5)
    if n==23:
        b.begin('ch-23-virgule','Écrire les euros et les centimes','CHAPITRE 23 · MÉTHODE À REPRENDRE EN P3')
        b.box('DEUX EUROS ET CINQ CENTIMES','2,05 € : 2 euros entiers et 5 centimes.\nLe zéro évite de confondre 5 centimes avec 50 centimes.',83,43,size=14)
        b.fig(('centcoins',[200,5]),133,34)
        b.box('DEUX EUROS ET CINQUANTE CENTIMES','2,50 € : 2 euros entiers et 50 centimes.\nCette somme est plus grande que 2,05 €.',177,43,fill=MINT,size=14)
        b.fig(('centcoins',[200,50]),226,34)
        b.text('Je peux vérifier en centimes : 205 < 250.',22,269,166,12.8,bold=True,color=GREEN)
    for j in range(3):
        b.begin(f'ch-{n}-ex-{j+1}',ch.titre,f'CHAPITRE {n:02} · '+['JE COMMENCE','JE M’ENTRAÎNE','JE CHERCHE'][j],subtitle='Date : ..................................   Prénom : ..................................')
        if n==31 and j==0:
            exercices_page(b,ch.exercices[:2],chapter=n)
            b.begin('ch-31-graphique','Le graphique de mon enquête','CHAPITRE 31 · JE CONSTRUIS',subtitle='Je reprends les résultats de mon tableau.')
            b.rect(17,83,9,9,fill=NAVY);b.text('3',19,84.2,6,12,bold=True,color=white);b.link('cor-31',17,83,9,9)
            b.text(ch.exercices[2].consigne,30,83,160,13.7,leading=18.1);b.fig(('surveygraph',None),110,140,x=24,w=164)
            b.text('Une case coloriée représente une personne.',24,260,164,13.5,bold=True,color=GREEN)
        else:exercices_page(b,ch.exercices[j*3:(j+1)*3],j*3+1,n)

def bilans(b):
    for i,(title,period,items) in enumerate(BILANS,1):
        for j in range(2):
            key=f'bilan-{i}-{j+1}';b.begin(key,title,f'BILAN {i} · '+('PREMIÈRE PARTIE' if j==0 else 'DEUXIÈME PARTIE'),subtitle='À proposer en plusieurs moments, après les apprentissages.')
            if j==0:b.outline(title,key)
            exercices_page(b,items[j*3:(j+1)*3],j*3+1)

def corriges(b):
    b.begin('corriges-intro','Comprendre les réponses','CORRIGÉS ET ACCOMPAGNEMENT',adult=True);b.outline('Corrigés expliqués','corriges-intro')
    b.box('CHERCHER AVANT DE CONSULTER','Faire expliquer la démarche avant de lire la réponse. Les corrigés proposent des méthodes et des critères ; les tracés libres et les enquêtes peuvent avoir plusieurs réponses valables.',83,45,size=13)
    b.text('Pour un calcul',20,141,172,15,bold=True,color=GREEN);b.text('Contrôler le sens de l’opération et l’ordre de grandeur. Vérifier une soustraction avec une addition ; recomposer un partage ; retrouver un produit avec les tables ou un dessin.',20,154,172,13)
    b.text('Pour un tracé ou une manipulation',20,196,172,15,bold=True,color=GREEN);b.text('Contrôler les longueurs, les angles, les positions ou le nombre de parts. Une construction géométrique doit respecter toutes les contraintes. Utiliser les instruments et les objets réels.',20,209,172,13)
    b.box('NAVIGATION','Cliquer sur un numéro d’exercice ouvre son corrigé. Dans les corrigés, cliquer sur le numéro ramène à la page de travail.',249,27,size=11.3)
    for ch in CHAPITRES:
        b.begin(f'cor-{ch.numero}',ch.titre,f'CORRIGÉ DU CHAPITRE {ch.numero:02}',adult=True);b.outline(f'Corrigé {ch.numero:02}',f'cor-{ch.numero}',1)
        b.link(f'ch-{ch.numero}-ex-1',17,37,176,9);b.text('Avec l’adulte',19,81,172,10.7,bold=True,color=GREEN);t=b.text(ch.guide_reponse,19,88,172,11.2,leading=14.6)+7
        for i,e in enumerate(ch.exercices,1):
            b.text(str(i)+'.',19,t,10,11.5,bold=True,color=NAVY);end=b.text(e.reponse,30,t,161,11.2,leading=14.6,maxbottom=210)
            key='ch-31-graphique' if ch.numero==31 and i==3 else f'ch-{ch.numero}-ex-{(i-1)//3+1}'
            b.link(key,18,t,10,max(6,end-t));t=end+4
        b.box('POINT DE VIGILANCE',ch.vigilance,214,32,fill=CREAM,size=10.5)
        b.box('SI L’ENFANT HÉSITE',ch.aide,249,27,fill=MINT,size=10.6)
    for i,(title,period,items) in enumerate(BILANS,1):
        b.begin(f'cor-bilan-{i}',title,f'CORRIGÉ DU BILAN {i}',adult=True);t=83
        for j,e in enumerate(items,1):b.text(str(j)+'.',19,t,10,12,bold=True,color=NAVY);t=b.text(e.reponse,30,t,160,11.8,leading=16)+11
        b.box('POUR LA REPRISE','Repérer l’objectif à reprendre et revenir au chapitre correspondant. Proposer une nouvelle situation proche à un autre moment ; ne pas réduire les acquis à une note unique.',240,34,size=11.3)

def oraux(b):
    b.begin('oral-intro','360 problèmes à raconter','BANQUE ORALE POUR L’ADULTE',adult=True);b.outline('Banque de problèmes oraux','oral-intro')
    b.box('36 SEMAINES · 10 HISTOIRES PAR SEMAINE','Lire les énoncés sans révéler la réponse ni l’opération. L’enfant peut manipuler, dessiner ou calculer. Les réponses de ces pages sont réservées à l’adulte.',83,44,size=13.4)
    t=141
    for title,body in [('Semaines 1 à 7','Additions, retraits, parties inconnues, comparaison, départ et petits problèmes en deux étapes. La centaine est utilisée dès le début. Produits et partages simples ; longueurs.'),('Semaines 8 à 14','Extension du champ additif jusqu’à 1 000, problèmes sur les centimes et tables. À partir de la semaine 12, une histoire mixte avec produit puis retrait.'),('Semaines 15 à 36','Produits avec un facteur de 11 à 19, poursuite des partages et des problèmes mixtes. Des groupements avec reste apparaissent à partir de la semaine 20.'),('Adapter aux acquis','L’ordre des semaines constitue une banque de propositions. Diminuer les nombres pour une structure nouvelle. Compléter avec les fractions, les durées, les constructions et les enquêtes du livre.')]:
        b.text(title,20,t,170,12.5,bold=True,color=GREEN);t=b.text(body,20,t+8,170,11.6,leading=15.5)+9
    for week in problemes_oraux():
        n=week['numero'];b.begin(f'oral-{n}',f'Semaine {n:02} · Dix petites histoires','PROBLÈMES ORAUX',subtitle=f'Champ additif jusqu’à {week["plafond"]} · Lire à l’enfant.',adult=True);t=81
        for i,p in enumerate(week['problemes'],1):
            b.text(str(i),18,t,9,10.8,bold=True,color=GREEN);end=b.text(p['enonce'],29,t,162,10.9,leading=14.1)
            end=b.text('Réponse : '+str(p['reponse'])+' · '+p['calcul'],29,end+1.2,162,9.6,leading=12.3,color=MUTED);b.line(29,end+2,191);t=end+5.4

def outils(b):
    from outils import construire_outils
    construire_outils(b)

def fin(b):
    for part in range(2):
        b.begin(f'programme-{part+1}','Repères du programme','CORRESPONDANCES POUR L’ADULTE',subtitle='Une proposition de parcours pour les apprentissages du CE1.',adult=True)
        if part==0:b.outline('Programme et sources','programme-1')
        t=81
        for title,chapters in COUVERTURE[part*14:(part+1)*14]:
            b.text(title,19,t,172,10.8,bold=True,color=NAVY);t=b.text('Chapitres '+chapters,19,t+6.7,172,10.3,color=MUTED)+2.1
    b.begin('aider','Aider l’enfant à progresser','NOTES PÉDAGOGIQUES',adult=True);t=82
    for title,body in [('Les chiffres sont inversés','Faire représenter 306 puis 360, puis relier chaque chiffre à sa valeur. Reprendre les échanges entre unités, dizaines et centaines.'),('Les retenues sont oubliées','Faire l’opération avec du matériel et écrire au fur et à mesure. Une retenue n’est pas une règle isolée : elle représente un échange.'),('Les tables sont fragiles','Construire les produits avec des groupes ou des rectangles ; retrouver un résultat à partir d’un autre ; poser des questions dans un ordre varié et espacer les rappels.'),('Les fractions sont comparées comme des entiers','Reprendre des touts identiques. Montrer qu’un plus grand nombre de parts égales donne des parts plus petites. Toujours faire nommer le tout.'),('Le mot de l’énoncé dicte l’opération','Faire rejouer l’histoire, identifier le connu et l’inconnu, puis dessiner. Le mot « plus » ne signifie pas toujours qu’il faut additionner.'),('Une tâche cumule trop de difficultés','Lire l’énoncé, réduire les quantités ou proposer un matériel. Garder le même objectif et alléger ce qui gêne l’accès au raisonnement.')]:
        b.text(title,19,t,172,12.4,bold=True,color=GREEN);t=b.text(body,19,t+8,172,11.4,leading=15.2)+9
    for part in range(2):
        b.begin(f'sources-{part+1}','Sources et statut des activités','RÉFÉRENCES CONSULTÉES LE 23 OCTOBRE 2026',adult=True);t=82
        for idx,(title,description,url) in enumerate(SOURCES[part*3:(part+1)*3],start=part*3+1):
            b.text(f'{idx}. {title}',19,t,172,12.2,bold=True,color=NAVY);b.c.linkURL(url,(19*mm,H-(t+9)*mm,191*mm,H-t*mm),relative=0,thickness=0)
            t=b.text(description,19,t+10,172,11.3,leading=15)+4;t=b.text(url.replace('https://',''),19,t,172,9.1,leading=12,color=MUTED)+13
        if part==1:
            b.box('ACTIVITÉS ORIGINALES','Les leçons, exercices, bilans, problèmes et schémas sont des créations pour la collection OptiTAB. Les ressources officielles ont servi à définir les compétences et les familles de tâches. Ce livre indépendant ne porte aucun label ministériel.',217,45,size=11.2)
    b.begin('bravo','Ce que je sais faire maintenant','MON PARCOURS DE CE1')
    b.box('JE MONTRE UNE RÉUSSITE','Je choisis une activité que je sais refaire.\nJ’explique ma démarche et ma vérification.',83,40,fill=MINT,size=14)
    b.text('Mon schéma ou ma construction',22,137,165,16,bold=True,color=GREEN);b.rect(20,152,170,69,fill=white,stroke=RULE)
    b.text('Ce que je veux encore apprendre à mieux faire :',22,236,165,13.2);b.lines(253,22,x=22,w=166)

def construire(path,refs=None):
    b=Livre(path,refs);couverture(b);liminaires(b)
    for ch in CHAPITRES:chapitre(b,ch)
    bilans(b);corriges(b);oraux(b);outils(b);fin(b);b.c.save();return b
if __name__=='__main__':
    assert len(CHAPITRES)==32
    a=construire(BUILD/'mise-en-page.pdf');b=construire(BUILD/'optitab-ce1-complet.pdf',a.dest);assert a.dest==b.dest
    meta=dict(pages=b.page,chapitres=32,exercices=288,bilans=5,questions_bilans=30,problemes_oraux=360,insertions_figures=b.figures,destinations=b.dest,plan=b.pages)
    (BUILD/'manifeste.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
    (BUILD/'blocs-texte.json').write_text(json.dumps(b.textblocks,ensure_ascii=False,indent=2),encoding='utf8')
    (BUILD/'blocs-figures.json').write_text(json.dumps(b.figureblocks,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in meta.items() if k not in ['destinations','plan']},ensure_ascii=False))
