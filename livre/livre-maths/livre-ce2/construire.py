"""Livre CE2 original : construction, navigation et export des manifestes."""
from mise_en_page import *
from dessins import diagram

def couverture(b):
    c=b.c;b.page=1;b.current='couverture';b.dest['couverture']=1;b.pages.append(dict(numero=1,cle='couverture',titre='Couverture',adulte=False))
    c.bookmarkPage('couverture');c.setFillColor(NAVY);c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(HexColor('#122A66'));p=c.beginPath();p.moveTo(0,0);p.lineTo(W,0);p.lineTo(W,145*mm);p.curveTo(120*mm,105*mm,70*mm,150*mm,0,110*mm);p.close();c.drawPath(p,stroke=0,fill=1)
    c.drawImage(str(ASSETS/'logo-blanc.png'),20*mm,H-35*mm,width=48*mm,height=18*mm,preserveAspectRatio=True,mask='auto')
    b.text('LE LIVRE POUR APPRENDRE ET COMPRENDRE',20,49,172,10.3,bold=True,color=white)
    b.text('Mathématiques',20,68,174,35,leading=40,bold=True,color=white)
    b.text('CE2',18,92,174,82,leading=94,bold=True,color=white)
    b.text('Je cherche. Je représente.\nJe calcule. Je vérifie.',21,137,164,20,leading=27,color=white)
    b.rect(20,174,170,23,fill=HexColor('#244A9F'))
    b.text('36 chapitres illustrés · 324 exercices\n5 bilans · 360 problèmes oraux · Corrigés',26,180,159,13.4,leading=19,color=white)
    b.rect(20,211,170,45,fill=white)
    b.fig(('fraccompare',[[3,4],[6,8]]),215,36,x=25,w=78)
    b.text('3/4 = 6/8',112,228,70,21,bold=True,color=NAVY)
    b.text('COLLECTION OPTITAB',20,267,120,10,bold=True,color=white)
    b.text('France · Édition 2026-2027',20,273,170,11,color=white)
    b.outline('Bienvenue dans le livre de CE2','couverture')

from debut import liminaires,methodes


def exercices_page(b,items,start=1,chapter=None):
    t=83
    for j,e in enumerate(items):
        num=start+j;b.rect(17,t,9,9,fill=NAVY,r=2);b.text(str(num),19,t+1.2,6,12,bold=True,color=white)
        end=b.text(e.consigne,30,t,160,13.7,leading=18.1,maxbottom=t+28)
        if chapter:b.link(f'cor-{chapter}',17,t,9,9)
        if e.figure:
            height=48 if e.figure[0]=='mulblank' and e.figure[1]==2 else 46 if e.figure[0]=='perirect' else 44 if e.figure[0]=='blank4' and abs(e.figure[1])==3 else 39
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
    if n==20:footer='Dans les phrases, 1/4 note aussi la fraction écrite avec une barre horizontale sur le schéma.'
    b.text(footer,22,263,166,11.7,color=MUTED)
    b.begin(f'ch-{n}-lecon',ch.titre,f'CHAPITRE {n:02} · JE RETIENS',subtitle='Je comprends, puis j’essaie avec l’adulte.')
    t=83
    for i,rule in enumerate(ch.lecon,1):
        b.rect(17,t,176,29,fill=PALE if i%2 else MINT);b.text(str(i),22,t+6,10,16,bold=True,color=GREEN);b.text(rule,35,t+5,151,13.5,maxbottom=t+27);t+=33
    b.box('UN EXEMPLE EXPLIQUÉ',ch.exemple,185,43,fill=CREAM,size=12.8)
    b.box('À TOI, AVEC L’ADULTE',ch.guide,235,37,fill=MINT,size=13.5)
    methodes(b,ch)
    for j in range(3):
        b.begin(f'ch-{n}-ex-{j+1}',ch.titre,f'CHAPITRE {n:02} · '+['JE COMMENCE','JE M’ENTRAÎNE','JE CHERCHE'][j],subtitle='Date : ..................................   Prénom : ..................................')
        if n==36 and j==0:
            exercices_page(b,ch.exercices[:2],chapter=n)
            b.begin('ch-36-graphique','Le graphique de mon enquête','CHAPITRE 36 · JE CONSTRUIS',subtitle='Je reprends les résultats de mon tableau.')
            b.rect(17,83,9,9,fill=NAVY);b.text('3',19,84.2,6,12,bold=True,color=white);b.link('cor-36',17,83,9,9)
            b.text(ch.exercices[2].consigne,30,83,160,13.7,leading=18.1);b.fig(('graphsurvey',None),110,140,x=24,w=164)
            b.text('Axe horizontal : ........................................................\nAxe vertical : ............................................................',24,253,164,11.8)
            b.text('Une case coloriée représente une personne.',24,271,164,10.5,bold=True,color=GREEN)
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
            key='ch-36-graphique' if ch.numero==36 and i==3 else f'ch-{ch.numero}-ex-{(i-1)//3+1}'
            b.link(key,18,t,10,max(6,end-t));t=end+4
        b.box('POINT DE VIGILANCE',ch.vigilance,214,32,fill=CREAM,size=10.5)
        b.box('SI L’ENFANT HÉSITE',ch.aide,249,27,fill=MINT,size=10.6)
    for i,(title,period,items) in enumerate(BILANS,1):
        b.begin(f'cor-bilan-{i}',title,f'CORRIGÉ DU BILAN {i}',adult=True);t=83
        for j,e in enumerate(items,1):b.text(str(j)+'.',19,t,10,12,bold=True,color=NAVY);t=b.text(e.reponse,30,t,160,11.8,leading=16)+11
        b.box('POUR LA REPRISE','Repérer l’objectif à reprendre et revenir au chapitre correspondant. Proposer une nouvelle situation proche à un autre moment ; ne pas réduire les acquis à une note unique.',240,34,size=11.3)

from oral import oraux


def outils(b):
    from outils import construire_outils
    construire_outils(b)

def fin(b):
    for part in range(3):
        b.begin(f'programme-{part+1}','Repères du programme','CORRESPONDANCES POUR L’ADULTE',subtitle='Une proposition de parcours pour les apprentissages du CE2.',adult=True)
        if part==0:b.outline('Programme et sources','programme-1')
        t=81
        for title,chapters in COUVERTURE[part*12:(part+1)*12]:
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
    b.begin('bravo','Ce que je sais faire maintenant','MON PARCOURS DE CE2')
    b.box('JE MONTRE UNE RÉUSSITE','Je choisis une activité que je sais refaire.\nJ’explique ma démarche et ma vérification.',83,40,fill=MINT,size=14)
    b.text('Mon schéma ou ma construction',22,137,165,16,bold=True,color=GREEN);b.rect(20,152,170,69,fill=white,stroke=RULE)
    b.text('Ce que je veux encore apprendre à mieux faire :',22,236,165,13.2);b.lines(253,22,x=22,w=166)

def construire(path,refs=None):
    b=Livre(path,refs);couverture(b);liminaires(b)
    for ch in CHAPITRES:chapitre(b,ch)
    bilans(b);corriges(b);oraux(b);outils(b);fin(b);b.c.save();return b
if __name__=='__main__':
    assert len(CHAPITRES)==36
    a=construire(BUILD/'mise-en-page.pdf');b=construire(BUILD/'optitab-ce2-complet.pdf',a.dest);assert a.dest==b.dest
    meta=dict(pages=b.page,chapitres=36,exercices=324,bilans=5,questions_bilans=30,problemes_oraux=360,insertions_figures=b.figures,destinations=b.dest,plan=b.pages)
    (BUILD/'manifeste.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
    (BUILD/'blocs-texte.json').write_text(json.dumps(b.textblocks,ensure_ascii=False,indent=2),encoding='utf8')
    (BUILD/'blocs-figures.json').write_text(json.dumps(b.figureblocks,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in meta.items() if k not in ['destinations','plan']},ensure_ascii=False))
