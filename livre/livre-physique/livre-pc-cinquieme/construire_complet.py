"""Manuel complet : pagination, sommaire cliquable et corrigés expliqués."""
from maquette import *
import construire as pilote
from contenu import CH1,CH2,PLAN,SOURCES
from programme_complet import TITRES,THEMES,SOURCES_COMPLEMENTAIRES
from chapitres_matiere import CHAPITRES_MATIERE

CHAPITRES=CHAPITRES_MATIERE[:]
try:
    from chapitres_mouvement import CHAPITRES_MOUVEMENT
    CHAPITRES+=CHAPITRES_MOUVEMENT
    from chapitres_energie import CHAPITRES_ENERGIE
    CHAPITRES+=CHAPITRES_ENERGIE
    from chapitres_signaux import CHAPITRES_SIGNAUX
    CHAPITRES+=CHAPITRES_SIGNAUX
except ModuleNotFoundError:
    pass  # Les passes intermédiaires permettent de relire chaque thème rédigé.
pilote.TITRES.update(TITRES)
FULL=ROOT/'build-complet';FULL.mkdir(exist_ok=True)

def pg(b,key,title,n,rub='L’ESSENTIEL',sub='',outline=False):
    b.begin(key,title,f'CHAPITRE {n:02} · {rub}',chapter=n,chapter_title=TITRES[n],subtitle=sub,outline=outline)

def cover(b):
    pilote.couverture(b,'MANUEL COMPLET · COURS, EXERCICES ET CORRIGÉS')

def front(b):
    b.begin('mode','Un manuel pour comprendre','LA DÉMARCHE OPTITAB',subtitle='Observer, expérimenter, mesurer et argumenter.',outline=True)
    for i,(title,body) in enumerate([
        ('1 · OBSERVER','Décrire les faits, préciser les conditions et poser une question.'),
        ('2 · CHERCHER','Formuler une hypothèse et proposer un test qui pourrait la mettre à l’épreuve.'),
        ('3 · MESURER','Choisir l’instrument, noter les résultats avec leurs unités et contrôler le protocole.'),
        ('4 · EXPLIQUER','Relier les observations aux connaissances et rédiger une conclusion argumentée.')]):
        b.box(title,body,83+(i//2)*46,39,x=22+(i%2)*86,w=80,size=11.2,fill=PALE if i<2 else MINT)
    b.p('Trois niveaux pour progresser',22,181,166,15,font='Bold',color=NAVY)
    t=195
    for label,body in [('JE DÉMARRE','Reconnaître, nommer et appliquer.'),('JE M’ENTRAÎNE','Lire un schéma, mesurer, calculer et expliquer.'),('JE RAISONNE','Croiser des données, critiquer une méthode et argumenter.')]:
        b.p(label,23,t,164,9.7,font='Bold',color=GREEN);t=b.p(body,23,t+5,164,11.6)+5
    b.box('LE CADRE DU MANUEL','Programme français du cycle 4 : BO du 30 juillet 2020, référence confirmée pour 2026-2027. La progression de 5e est un choix pédagogique. Manuel OptiTAB indépendant, sans validation institutionnelle revendiquée.',248,29,size=10.6)
    number=1
    for part,groups in enumerate([PLAN[:2],PLAN[2:]],1):
        b.begin(f'sommaire-{part}','Sommaire général',f'LE PARCOURS DE CINQUIÈME · {part}/2',subtitle='Les titres et les numéros de page sont cliquables.',outline=part==1);t=82
        for letter,theme,chapters in groups:
            b.rect(22,t,9,9,fill=NAVY);b.p(letter,24,t+1.7,7,11,font='Bold',color=white)
            b.p(theme,35,t+1,151,12.7,font='Bold',color=NAVY);t+=15
            for title,_ in chapters:
                key=f'ch-{number}-ouverture';b.p(f'{number:02}',23,t,12,11.5,font='Bold',color=GREEN)
                b.p(title,37,t,126,11.7);b.p(str(b.refs.get(key,'…')),172,t,16,10.8,font='Bold',color=NAVY)
                if key in b.refs:b.link(key,22,t,166,9)
                t+=11;number+=1
            t+=8
        if part==2:
            b.box('POUR RETROUVER UNE MÉTHODE','Les corrigés, les quatre bilans, le lexique et les références sont réunis en fin de livre. Les numéros des exercices mènent à leur corrigé ; les numéros des corrigés reviennent à l’énoncé.',247,29,size=10.7)
    b.begin('reperes','Tes outils pour toute l’année','MÉTHODES ET NAVIGATION',outline=True)
    sections=[('Travailler en sécurité','securite'),('Corrigés des exercices','cor-1-groupe-1'),('Activités et défis : éléments de réponse','solutions-3'),('Bilans des quatre thèmes','bilan-A'),('Lexique scientifique','lexique-1'),('Grandeurs et conversions','unites'),('Références et choix de progression','programme')]
    t=83
    for title,key in sections:
        b.p(title,23,t,137,13,font='Bold',color=NAVY);b.p(str(b.refs.get(key,'…')),171,t,17,12,font='Bold',color=NAVY)
        if key in b.refs:b.link(key,22,t,166,11)
        b.line(22,t+10,188);t+=22
    b.box('UNE MÉTHODE QUI FONCTIONNE','Cherche d’abord seul, écris tes essais et explique ta réponse. Utilise le corrigé pour comprendre l’erreur, puis refais la question sans regarder la solution.',250,27,size=11.3,fill=MINT,accent=GREEN)
    b.begin('securite','Travailler avec soin','DÉMARCHE EXPÉRIMENTALE',outline=True)
    b.box('AVANT DE COMMENCER','Lire la consigne entière, identifier la question et faire vérifier le montage par le professeur. Les manipulations de chimie, de chauffage et d’électricité sont réalisées en classe selon ses consignes.',82,35,size=11.8)
    b.bullets([
        'Ne jamais goûter un échantillon ni sentir directement un produit. Lire les étiquettes et utiliser les protections demandées.',
        'Porter les lunettes et autres protections prévues par le protocole. Organiser une paillasse dégagée et attacher les cheveux si nécessaire.',
        'Pour l’électricité : utiliser exclusivement le matériel scolaire de très basse tension ; ne jamais manipuler une prise du secteur.',
        'Ne pas regarder le Soleil, un laser ou une source intense. Les activités de lumière utilisent des lampes adaptées.',
        'Limiter le niveau sonore ; s’éloigner des sources fortes et interrompre une exposition gênante.',
        'Trier les déchets selon la consigne ; demander avant de jeter une solution. Se laver les mains après les manipulations.'
    ],130,size=11.6,gap=4)
    b.box('UNE TRACE SCIENTIFIQUE','Question → hypothèse → protocole → observations et mesures → interprétation → conclusion. Une conclusion peut rester limitée : le préciser fait partie du travail scientifique.',246,31,size=11.4,fill=MINT,accent=GREEN)

def ouverture(b,ch):
    n=ch.n;b.begin(f'ch-{n}-ouverture',TITRES[n],f'CHAPITRE {n:02} · {THEMES[n]}',chapter=n,chapter_title=TITRES[n],outline=True)
    end=b.p(ch.question,23,82,164,17,font='Bold',color=NAVY)
    b.fig(ch.lecons[0].schema,max(108,end+7),66)
    b.rect(22,193,166,60,fill=MINT);b.p('À LA FIN DU CHAPITRE, JE SAIS…',27,198,156,10,font='Bold',color=GREEN)
    b.bullets(ch.objectifs,211,x=28,w=152,size=11.8,gap=4)
    b.p('Avant de lire : propose une réponse à la question, puis garde une trace de ton raisonnement.',23,264,164,11,color=MUTED)

def lecon(b,ch,k,le):
    pg(b,f'ch-{ch.n}-cours-{k}',le.titre,ch.n)
    bh=b.p(le.texte,w=166,size=12,measure=True)
    rh=max(27,b.p(le.retenir,w=158,size=11.4,measure=True)+15)
    mh=max(27,b.p(le.methode,w=158,size=11.4,measure=True)+15)
    cap=b.p(le.legende,w=166,size=9.5,measure=True)
    fh=min(72,276-(82+bh+5+cap+2+7+rh+5+mh))
    if fh<53:raise ValueError(f'Leçon trop longue {ch.n}.{k} : figure {fh:.1f}')
    t=b.p(le.texte,22,82,166,12)+5
    t=b.fig(le.schema,t,fh,caption=le.legende)+7
    b.box('À RETENIR',le.retenir,t,rh,size=11.4);t+=rh+5
    b.box('UNE MÉTHODE CONCRÈTE',le.methode,t,mh,size=11.4,fill=MINT,accent=GREEN)

def activite(b,ch):
    ac=ch.activite;pg(b,f'ch-{ch.n}-activite',ac.titre,ch.n,'ACTIVITÉ · CHERCHER ET CONCLURE')
    t=b.p(ac.mission,22,82,166,13,font='Bold',color=NAVY)+6
    t=b.bullets(ac.etapes,t,size=11.4,gap=3)+4
    qh=sum(b.p(q,w=157,size=11.6,measure=True)+3 for q in ac.questions)
    cap=b.p(ac.legende,w=166,size=9.5,measure=True)
    fh=min(65,274-t-cap-2-7-qh)
    if fh<38:raise ValueError(f'Activité trop longue {ch.n} : {fh:.1f}')
    t=b.fig(ac.schema,t,fh,caption=ac.legende)+7
    for i,q in enumerate(ac.questions,1):
        b.p(str(i)+'.',23,t,6,11.6,font='Bold',color=GREEN);t=b.p(q,31,t,157,11.6)+3

def synthese(b,ch):
    pg(b,f'ch-{ch.n}-bilan','L’essentiel à retenir',ch.n,'SYNTHÈSE ET AUTOÉVALUATION');t=82
    for i,s in enumerate(ch.bilan,1):
        h=max(24,b.p(s,w=158,size=11.7,measure=True)+15)
        b.box(f'REPÈRE {i}',s,t,h,size=11.7,fill=PALE if i%2 else MINT,accent=NAVY if i%2 else GREEN);t+=h+4
    h=max(28,b.p(ch.erreur,w=158,size=11.4,measure=True)+15)
    b.box('UNE ERREUR À ÉVITER',ch.erreur,max(t,244),h,size=11.4,fill=CREAM,accent=ORANGE)

def defi(b,ch):
    d=ch.defi;pg(b,f'defi-{ch.n}',d.titre,ch.n,'DÉFI · PRENDRE UNE INITIATIVE')
    t=b.p(d.situation,22,82,166,12.3)+7
    t=b.fig(d.schema,t,65)+8
    t=b.bullets(d.questions,t,size=11.8,gap=4)
    h=max(25,b.p(d.aide,w=158,size=11.2,measure=True)+15)
    b.box('INDICE PROGRESSIF',d.aide,max(t+4,249),h,size=11.2,fill=MINT,accent=GREEN)

def exercices_equilibres(b,ch):
    """Éviter de laisser un court exercice seul sur une page de fin de niveau."""
    for part,(title,level,items) in enumerate([
        ('Je démarre','NIVEAU 1',ch.exercices[:5]),
        ('Je m’entraîne','NIVEAU 2',ch.exercices[5:11]),
        ('Je raisonne','NIVEAU 3',ch.exercices[11:])],1):
        pages=[];group=[];height=0
        for e in items:
            h=pilote.ex_height(b,e)
            if group and height+h>192:pages.append(group);group=[];height=0
            group.append(e);height+=h
        if group:pages.append(group)
        if len(pages)>1 and len(pages[-1])==1 and len(pages[-2])>=3:
            candidate=[pages[-2][-1]]+pages[-1]
            if sum(pilote.ex_height(b,e) for e in candidate)<=192:
                pages[-2].pop();pages[-1]=candidate
        for k,group in enumerate(pages,1):
            pg(b,f'ch-{ch.n}-ex-{part}-{k}',title,ch.n,level,sub='Réponds dans ton cahier. Les numéros ouvrent les corrigés.');t=82
            for e in group:t=pilote.render_ex(b,e,ch.n,t)
            if t<233:b.box('POUR PROGRESSER','Avant le corrigé, cherche une propriété, un schéma ou une étape de méthode qui peut t’aider. Après correction, explique l’erreur puis refais une question proche.',246,29,size=11.1,fill=MINT,accent=GREEN)

def solutions(b,ch):
    # Les trois groupes de corrigés réutilisent la navigation validée.
    groups=[ch.exercices[:5],ch.exercices[5:11],ch.exercices[11:]]
    for part,group in enumerate(groups,1):
        pg(b,f'cor-{ch.n}-groupe-{part}',f'Corrigés expliqués · {group[0].n:02} à {group[-1].n:02}',ch.n,'COMPRENDRE ET SE CORRIGER');t=82
        for e in group:
            key=f'cor-{ch.n}-{e.n}';b.dest[key]=b.page;b.c.bookmarkPage(key)
            b.p(f'{ch.n:02}.{e.n:02}',22,t,18,11.5,font='Bold',color=NAVY);b.link(f'ex-{ch.n}-{e.n}',22,t,18,8)
            t=b.p(e.reponse,44,t,144,11.4,leading=14.7,maxbottom=274)+6
        if t<237:b.box('POUR CONSOLIDER','Repère l’idée utilisée dans le corrigé. Cache la réponse puis reprends la question en rédigeant ta propre explication, avec les unités et les conditions utiles.',247,29,size=11.1,fill=MINT,accent=GREEN)
    pg(b,f'solutions-{ch.n}','Activité et défi : comprendre',ch.n,'ÉLÉMENTS DE RÉPONSE');t=82
    for label,title,body,key in [('ACTIVITÉ',ch.activite.titre,ch.activite.correction,f'ch-{ch.n}-activite'),('DÉFI',ch.defi.titre,ch.defi.correction,f'defi-{ch.n}')]:
        b.p(label,22,t,166,10,font='Bold',color=GREEN);t+=7
        b.p(title,22,t,166,14,font='Bold',color=NAVY);b.link(key,22,t,166,10);t+=13
        t=b.p(body,22,t,166,11.8)+13
    if t<240:b.box('D’AUTRES RÉPONSES SONT POSSIBLES','Une activité ouverte peut admettre plusieurs protocoles ou formulations. La réponse doit respecter les observations, les conditions expérimentales et les connaissances du chapitre.',247,29,size=11.2)

def fin(b):
    b.begin('programme','Programme et progression','LES CHOIX DU MANUEL',outline=True)
    b.p('Le programme national définit les attendus sur les trois années du cycle 4. Ce manuel propose une progression complète pour la 5e, construite à partir des repères de début de cycle. L’équipe pédagogique peut organiser les apprentissages autrement.',22,82,166,12)
    b.table([['Thème du programme','Chapitres'],['Organisation et transformations de la matière','1 à 8'],['Mouvement et interactions','9 à 11'],['Énergie, transferts et conversions','12 à 16'],['Signaux pour observer et communiquer','17 à 20']],120,[130,36],rowheight=15,size=11.6)
    b.box('UNE PROGRESSION SUR TROIS ANNÉES','Les modèles atomiques détaillés, les équations de réaction, la grandeur quotient masse volumique, la modélisation formelle des forces et les lois électriques sont approfondis aux niveaux suivants. Ici, les circuits, les interactions et les transferts d’énergie sont étudiés surtout par observations et raisonnements simples.',208,44,size=11.4,fill=MINT,accent=GREEN)
    b.p('Le titre « manuel complet » désigne cette progression de 5e ; il ne prétend pas traiter à lui seul tous les attendus de fin de 3e.',23,262,164,10.8,color=MUTED)
    sources=SOURCES+SOURCES_COMPLEMENTAIRES
    for part in range((len(sources)+2)//3):
        b.begin(f'sources-{part+1}','Références et choix éditoriaux',f'SOURCES CONSULTÉES LE 23 OCTOBRE 2026 · {part+1}',outline=part==0);t=82
        for i,(title,desc,url) in enumerate(sources[part*3:(part+1)*3],part*3+1):
            b.p(f'{i}. {title}',22,t,166,13,font='Bold',color=NAVY);b.url(url,22,t,166,9)
            t=b.p(desc,22,t+11,166,11.4)+4;t=b.p(url.replace('https://',''),22,t,166,9.2,color=MUTED)+12
        if part==(len(sources)+2)//3-1:
            b.box('CRÉATIONS ORIGINALES','Textes, exercices, corrigés et schémas sont des créations pour cet ouvrage. Les documents officiels servent de références de programme et de démarche. Les séries annoncées comme pédagogiques sont des exemples à exploiter, pas des mesures effectuées par l’élève.',235,41,size=11.1)

def construire(path,refs=None):
    b=Livre(path,refs,complet=True);cover(b);front(b)
    pilote.cours1(b);pilote.exercices(b,1,CH1);pilote.defis(b,1)
    pilote.cours2(b);pilote.exercices(b,2,CH2);pilote.defis(b,2)
    for ch in CHAPITRES:
        ouverture(b,ch)
        for k,le in enumerate(ch.lecons,1):lecon(b,ch,k,le)
        activite(b,ch);synthese(b,ch);exercices_equilibres(b,ch);defi(b,ch)
    try:
        from annexes_completes import bilans,annexes,corrections_bilans
        bilans(b)
    except ModuleNotFoundError:pass
    b.c.addOutlineEntry('Corrigés des exercices','cor-1-groupe-1',0,False)
    pilote.corriges(b,1,CH1);pilote.corriges(b,2,CH2)
    for ch in CHAPITRES:solutions(b,ch)
    try:corrections_bilans(b);annexes(b)
    except NameError:pass
    fin(b);b.save();return b

if __name__=='__main__':
    a=construire(FULL/'pagination.pdf');b=construire(FULL/'optitab-physique-chimie-5e-complet.pdf',a.dest)
    assert a.dest==b.dest
    meta=dict(pages=b.page,chapitres_rediges=len(CHAPITRES)+2,chapitres_au_sommaire=20,exercices=len(b.exercises),defis=len(CHAPITRES)+2,insertions_schemas=len(b.figures),destinations=b.dest,plan=b.pages,exercices_pages=b.exercises)
    for name,data in [('manifeste',meta),('blocs-texte',b.blocks),('blocs-figures',b.figures)]:
        (FULL/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in meta.items() if k not in ['destinations','plan','exercices_pages']},ensure_ascii=False))
