"""Extrait de validation : sommaire complet et deux chapitres entièrement rédigés."""
from maquette import *
from contenu import PLAN,SOURCES,CH1,CH2

TITRES={1:'La matière et ses états',2:'Mesurer une masse et un volume'}

def page(b,key,title,chap,sub='',rub='L’ESSENTIEL'):
    b.begin(key,title,f'CHAPITRE {chap:02} · {rub}',chapter=chap,chapter_title=TITRES[chap],subtitle=sub)

def couverture(b,bande='SOMMAIRE COMPLET ET DEUX PREMIERS CHAPITRES'):
    b.page=1;b.key='couverture';b.dest['couverture']=1;b.pages.append(dict(page=1,key='couverture',title='Couverture',chapter=0));b.c.bookmarkPage('couverture')
    b.c.setFillColor(NAVY);b.c.rect(0,0,W,H,stroke=0,fill=1)
    b.c.setFillColor(DARK);p=b.c.beginPath();p.moveTo(0,0);p.lineTo(W,0);p.lineTo(W,150*mm);p.curveTo(110*mm,105*mm,80*mm,140*mm,0,100*mm);p.close();b.c.drawPath(p,stroke=0,fill=1)
    b.c.drawImage(str(ROOT/'images/logo-blanc.png'),22*mm,H-35*mm,width=49*mm,height=18*mm,preserveAspectRatio=True,mask='auto')
    b.p('COLLÈGE · CINQUIÈME',23,48,165,11,font='Bold',color=white)
    b.p('Physique-chimie',21,66,169,35,font='Head',color=white)
    b.p('5e',19,90,170,76,leading=82,font='Title',color=white)
    b.line(23,128,49,color=HexColor('#6BB578'),width=2)
    b.p('Observer. Comprendre.\nExpérimenter et raisonner.',23,138,162,21,leading=27,font='Title',color=white)
    b.rect(21,176,168,20,fill=HexColor('#2C4F9C'))
    b.p(bande,26,181,158,10.3,font='Bold',color=white)
    b.rect(21,208,168,49,fill=white,r=3)
    b.fig(('states',None),210,44,x=25,w=160)
    b.p('Cours illustrés · Activités · Exercices progressifs · Corrigés détaillés',23,266,165,10.5,color=white)
    b.p('Programme français de cycle 4 · Édition 2026-2027',23,274,165,10.6,color=white,maxbottom=285)
    b.c.addOutlineEntry('Couverture','couverture',0,False)

def debut(b):
    b.begin('mode','Un manuel pour comprendre','LA DÉMARCHE OPTITAB',subtitle='Des observations concrètes aux explications scientifiques.',outline=True)
    cards=[('1 · Observer','Je décris les faits et je formule une question.'),('2 · Chercher','Je propose une hypothèse et un protocole pour la tester.'),('3 · Mesurer','Je choisis l’instrument, je relève les résultats et je compare.'),('4 · Expliquer','Je m’appuie sur les résultats, je conclus et je communique.')]
    for i,(lab,body) in enumerate(cards):b.box(lab,body,86+(i//2)*45,37,x=22+(i%2)*86,w=80,size=11.6,fill=PALE if i<2 else MINT)
    b.p('Des exercices qui font progresser',22,184,166,15,font='Bold',color=NAVY)
    t=196
    for label,body in [('NIVEAU 1 · JE DÉMARRE','Reconnaître, nommer et appliquer une consigne simple.'),('NIVEAU 2 · JE M’ENTRAÎNE','Lire un schéma, mesurer, calculer et expliquer une méthode.'),('NIVEAU 3 · JE RAISONNE','Croiser des données, critiquer un protocole et argumenter.')]:
        b.p(label,23,t,164,9.6,font='Bold',color=GREEN);t=b.p(body,23,t+5.5,164,11.4)+5
    b.box('LE CADRE DE CET EXTRAIT','Le programme de référence est celui du cycle 4, BO du 30 juillet 2020, confirmé par Éduscol pour 2026-2027. La répartition en 5e proposée ici est éditoriale. Ouvrage OptiTAB indépendant ; seuls les chapitres 1 et 2 sont rédigés dans cet extrait.',247,30,size=10.3)
    for part,groups in enumerate([PLAN[:2],PLAN[2:]],1):
        b.begin(f'sommaire-{part}','Sommaire général',f'LE PARCOURS DE CINQUIÈME · {part}/2',subtitle='Vingt chapitres pour explorer les quatre thèmes du programme.',outline=part==1)
        start=1 if part==1 else 12;t=82
        for letter,theme,chapters in groups:
            b.rect(22,t,9,9,fill=NAVY);b.p(letter,24,t+1.7,7,11,font='Bold',color=white)
            b.p(theme,35,t+1,151,12.7,font='Bold',color=NAVY);t+=15
            for title,desc in chapters:
                n=start;key=f'ch-{n}-ouverture';b.p(f'{n:02}',23,t,12,11.5,font='Bold',color=GREEN)
                b.p(title,37,t,126,11.7,font='Bold' if n<=2 else 'Body')
                status=f'p. {b.refs.get(key,"…")}' if n<=2 else 'prévu'
                b.p(status,170,t,18,10.4,color=NAVY if n<=2 else MUTED,font='Bold' if n<=2 else 'Body')
                if n<=2:b.link(key,22,t,166,9)
                t+=11;start+=1
            t+=8
        if part==2:
            b.box('DANS CET EXTRAIT','Les chapitres 1 et 2 comprennent le cours, les activités, 30 exercices, 2 défis et leurs corrigés. Les chapitres 3 à 20 figurent au plan et seront développés après validation.',247,29,size=10.8)
        else:b.p('Les titres et les numéros de page des deux chapitres inclus sont cliquables.',23,269,164,10,color=MUTED)

def ouverture(b,n,question,objectifs,fig):
    b.begin(f'ch-{n}-ouverture',TITRES[n],f'CHAPITRE {n:02} · ORGANISATION ET TRANSFORMATIONS DE LA MATIÈRE',chapter=n,chapter_title=TITRES[n],outline=True)
    b.p(question,23,82,164,17,font='Bold',color=NAVY)
    b.fig(fig,104,72,caption='Observer le dispositif, puis relier chaque observation à une propriété ou à une grandeur.')
    b.rect(22,194,166,57,fill=MINT)
    b.p('À LA FIN DU CHAPITRE, JE SAIS…',27,199,156,10,font='Bold',color=GREEN)
    b.bullets(objectifs,211,x=28,w=152,size=11.8,gap=3)
    b.p('Prends ton cahier : conserve tes essais, tes schémas et tes explications.',23,264,164,11,color=MUTED)

def cours1(b):
    ouverture(b,1,'Un verre « vide » est-il vraiment vide ?',[
        'Distinguer solide, liquide et gaz à partir de propriétés observables.',
        'Expliquer que l’air occupe un volume et peut être comprimé.',
        'Utiliser un modèle simple et distinguer observation et interprétation.'
    ],('states',None))
    page(b,'ch-1-etats','Trois états, des propriétés',1)
    t=b.section(1,'Décrire avant de classer',80)
    b.p('Une même matière peut exister sous différents états physiques. On précise les conditions de l’étude, notamment la température. Pour comparer, on observe la forme, le volume occupé et l’effet d’une compression douce.',22,t,166,12)
    b.fig(('states',None),118,59)
    b.table([
        ['Propriété','Solide compact','Liquide','Gaz'],
        ['Forme propre','Oui','Non','Non'],
        ['Volume propre','Oui','Oui','Non'],
        ['Compression douce','Très faible effet','Très faible effet','Volume réduit']
    ],186,[48,39,39,40],rowheight=13,size=10.6)
    b.box('POUR BIEN COMPARER','On étudie ici un solide compact, un liquide et un gaz dans les conditions usuelles. Les déformations, les changements de température et les fortes pressions peuvent modifier certaines propriétés.',246,28,fill=CREAM,size=10.9,accent=ORANGE)
    page(b,'ch-1-liquide','Un liquide change de forme',1)
    t=b.section(2,'Transvaser ne fait pas disparaître la matière',80)
    b.p('Sans perte de liquide et sans changement de température, transvaser une même quantité d’eau modifie sa forme et sa hauteur dans le récipient, mais ne modifie pas son volume.',22,t,166,12)
    b.fig(('transfer',None),116,64,caption='Le récipient large donne une hauteur d’eau plus faible, pour la même quantité d’eau.')
    b.p('La surface libre d’un liquide au repos',22,193,166,14,font='Bold',color=NAVY)
    b.fig(('tilt',False),206,48,x=25,w=105)
    b.p('Loin des parois, une surface libre suffisamment étendue est plane et horizontale. Elle reste horizontale quand le récipient immobile est incliné.',136,210,49,11.3)
    b.p('Près des parois, la surface peut se courber : nous apprendrons à lire ce ménisque au chapitre 2.',23,264,164,10.7,color=MUTED)
    page(b,'ch-1-gaz','L’air est une matière',1)
    t=b.section(3,'Un gaz occupe l’espace accessible',80)
    b.p('L’air est invisible, mais il occupe une place et possède une masse. Dans un récipient fermé, il se répartit dans l’espace accessible. Son volume peut diminuer lorsqu’on le comprime, ou augmenter si on lui offre davantage d’espace.',22,t,166,12)
    b.fig(('syringes',[50,30]),125,53,caption='Une seringue fermée permet d’observer la compressibilité de l’air. La quantité d’air reste la même si rien ne fuit.')
    b.box('UNE OBSERVATION, UNE INTERPRÉTATION','Observation : le piston avance et le volume occupé diminue.\nInterprétation : l’air est compressible. Il ne disparaît pas.',196,31,size=11.7)
    b.box('NE PAS CONFONDRE VAPEUR ET BROUILLARD','La vapeur d’eau est un gaz invisible. Le brouillard et les nuages visibles contiennent de fines gouttelettes d’eau liquide, parfois aussi des cristaux de glace. Une « fumée blanche » ne prouve donc pas que l’on voit un gaz.',237,37,fill=CREAM,size=11.2,accent=ORANGE)
    page(b,'ch-1-activite','Le verre protège-t-il le papier ?',1,rub='ACTIVITÉ D’INVESTIGATION')
    b.p('Question : que contient un verre que l’on pense vide ?',22,81,166,14,font='Bold',color=NAVY)
    b.p('Matériel : bac d’eau, gobelet transparent rigide et papier. Activité en classe avec le professeur. Utiliser un récipient adapté et ne pas forcer.',22,93,166,11.2,color=MUTED)
    b.fig(('inverted',None),116,72,caption='Gobelet entièrement sous l’eau, ouverture vers le bas. Garder le gobelet vertical pendant la première observation. Schéma non à l’échelle.')
    b.bullets([
        '<b>Avant :</b> formule une hypothèse sur l’état du papier après immersion.',
        '<b>Tester :</b> coince le papier au fond, retourne le gobelet, puis descends-le verticalement. Fais valider le montage.',
        '<b>Observer :</b> relève l’état du papier. Incline ensuite le gobelet et décris les bulles ainsi que l’entrée de l’eau.'
    ],207,size=11.6,gap=3)
    b.box('POUR CONCLURE','Écris deux observations et une explication. Si tu ne réalises pas la manipulation, exploite le document : papier sec au départ ; des bulles s’échappent et l’eau entre quand on incline le gobelet.',247,29,size=10.8,fill=MINT,accent=GREEN)
    page(b,'ch-1-modele','Un premier modèle de la matière',1)
    b.box('MODÉLISER','Un modèle est une représentation simplifiée. Ici, chaque point représente une particule. Il aide à relier l’organisation de la matière à ses propriétés, mais ce n’est pas une photographie.',82,34,size=11.7)
    b.fig(('particles',None),128,65,caption='Même nombre de points et même taille des points dans les trois cases. Le modèle dessiné pour le solide est un modèle ordonné simplifié.')
    b.bullets([
        '<b>Solide :</b> les particules restent proches et vibrent autour de positions fixes dans ce modèle. Cela explique une forme propre.',
        '<b>Liquide :</b> les particules sont proches et peuvent se déplacer les unes par rapport aux autres.',
        '<b>Gaz :</b> les particules sont espacées et se déplacent dans tout l’espace accessible. Les espaces entre elles peuvent diminuer lors d’une compression.'
    ],213,size=11.6,gap=3)
    b.p('Les points ne sont ni des gouttes ni des grains visibles. Ils ne grossissent pas simplement parce que le volume du gaz augmente.',23,263,164,10.7,color=MUTED)
    page(b,'ch-1-bilan','L’essentiel à retenir',1,rub='SYNTHÈSE ET MÉTHODE')
    b.box('LES QUATRE IDÉES CLÉS','Un solide compact possède une forme et un volume propres.\nUn liquide possède un volume propre et prend la forme du récipient.\nUn gaz occupe l’espace accessible et peut être comprimé.\nInvisible ne signifie pas absent : l’air est une matière.',82,49,size=12)
    t=b.section('→','Expliquer avec une preuve',144)
    b.bullets(['Je nomme <b>ce qui a été observé</b>.','Je cite la <b>propriété</b> que cette observation permet d’utiliser.','Je relie les deux avec une phrase : « J’observe…, donc… ».'],t,size=12,gap=4)
    b.box('UN EXEMPLE DE RÉDACTION','« Dans la seringue fermée, le volume de l’air diminue lorsque le piston avance. Comme l’air ne s’échappe pas, cette observation montre qu’un gaz est compressible. »',210,34,size=12,fill=MINT,accent=GREEN)
    b.p('Avant les exercices : sais-tu expliquer pourquoi du sable qui coule peut rester solide et pourquoi on ne voit pas la vapeur d’eau ?',23,258,164,11.3,color=MUTED)

def cours2(b):
    ouverture(b,2,'Un même volume implique-t-il une même masse ?',[
        'Mesurer une masse et lire un volume avec les instruments adaptés.',
        'Utiliser la tare, les conversions et le déplacement d’eau.',
        'Distinguer les deux grandeurs et exploiter une proportionnalité simple.'
    ],('measurehero',None))
    page(b,'ch-2-masse','Mesurer une masse',2)
    b.box('GRANDEUR ET UNITÉ','La masse, notée m, est une grandeur que l’on mesure avec une balance. L’unité du Système international est le kilogramme (kg). Au laboratoire, on utilise souvent le gramme (g).',82,34,size=12)
    b.p('Peser un liquide avec la tare',22,129,166,15,font='Bold',color=NAVY)
    b.fig(('weighing',['48,6','0,0','74,5']),144,62,caption='« Vide » signifie ici sans liquide : le récipient contient de l’air. Après la tare, garder le même récipient ; l’affichage donne la masse de liquide ajoutée.')
    b.box('SI L’ON N’A PAS FAIT LA TARE','Masse du liquide = masse du récipient plein - masse du récipient vide.\nExemple : 123,1 g - 48,6 g = 74,5 g.',220,29,size=12,fill=MINT,accent=GREEN)
    b.p('Poser la balance à plat et attendre que l’affichage se stabilise. « Masse » et « poids » désignent des grandeurs différentes.',23,260,164,11.2,color=MUTED)
    page(b,'ch-2-volume','Lire un volume au bon endroit',2)
    b.p('Le volume, noté V, mesure l’espace occupé. Son unité SI est le mètre cube (m³). Pour un liquide au laboratoire, on utilise souvent une éprouvette graduée en millilitres (mL).',22,82,166,12)
    b.fig(('meniscus',None),111,91,caption='Pour l’eau dans une éprouvette usuelle, lire le bas du ménisque. Ici V = 36 mL.')
    b.bullets([
        'Poser l’éprouvette sur un support <b>horizontal</b>.',
        'Repérer l’<b>unité</b>, puis compter les intervalles entre deux valeurs connues.',
        'Placer l’<b>œil à la hauteur</b> du bas du ménisque et noter valeur + unité.'
    ],221,size=11.7,gap=3)
    b.p('Une division vaut ici 10 mL ÷ 5 = 2 mL. Compter les intervalles, pas le nombre de traits.',23,264,164,10.8,color=GREEN)
    page(b,'ch-2-unites','Convertir en gardant la grandeur',2)
    b.table([
        ['Masse','Volume'],
        ['1 kg = 1 000 g','1 L = 1 000 mL'],
        ['1 g = 1 000 mg','1 L = 1 dm³'],
        ['0,250 kg = 250 g','1 mL = 1 cm³']
    ],83,[83,83],rowheight=13,size=12)
    b.fig(('cubes',None),148,61,caption='Le cm³ est le volume d’un cube d’arête 1 cm. Le dm³ est le volume d’un cube d’arête 1 dm. Représentation non à l’échelle.')
    b.box('UNE MÉTHODE SIMPLE','Repérer la grandeur, choisir l’équivalence puis calculer.\n0,35 L = 0,35 × 1 000 mL = 350 mL.\n750 g = 750 ÷ 1 000 kg = 0,750 kg.',228,38,size=12)
    page(b,'ch-2-deplacement','Mesurer un solide par déplacement d’eau',2)
    b.p('Une éprouvette permet aussi de mesurer le volume d’un solide de forme irrégulière. On compare le volume lu avant et après immersion complète.',22,82,166,12)
    b.fig(('displacement',[[40,58],100,2]),108,88,caption='Le solide est entièrement dans l’eau. Les graduations sont identiques sur les deux éprouvettes.')
    b.box('LIRE, SOUSTRAIRE ET EXPRIMER','Volume du solide = volume final - volume initial.\nV = 58 mL - 40 mL = 18 mL = 18 cm³.',212,29,size=12,fill=MINT,accent=GREEN)
    b.box('LES CONDITIONS DU PROTOCOLE','Le solide ne doit pas se dissoudre, absorber l’eau ni réagir avec elle. Éviter les bulles. L’objet doit être entièrement immergé et l’éprouvette assez grande pour ne pas déborder.',248,28,fill=CREAM,size=11,accent=ORANGE)
    page(b,'ch-2-comparer','Masse et volume : deux grandeurs',2)
    b.p('À volume égal, deux matières différentes peuvent avoir des masses différentes. On ne convertit donc pas des mL en g sans une information sur la matière étudiée.',22,82,166,12)
    b.fig(('massvolume',None),113,64,caption='Résultats d’une expérience donnée : 20 mL d’eau, environ 20 g ; 20 mL de cette huile, 18 g. Données pédagogiques arrondies.')
    b.table([['Volume d’eau','20 mL','40 mL','60 mL','80 mL'],['Masse approximative','20 g','40 g','60 g','80 g']],196,[54,28,28,28,28],rowheight=13,size=11)
    b.box('POUR UNE MÊME SUBSTANCE','À température fixée, la masse est proportionnelle au volume. Pour l’eau usuelle à température ambiante, 1 mL a une masse d’environ 1 g. Ce repère n’est ni une égalité entre unités ni une règle pour tous les liquides.',237,38,size=11.7,fill=MINT,accent=GREEN)
    page(b,'ch-2-activite','Préparer et vérifier une mesure',2,rub='ACTIVITÉ EXPÉRIMENTALE')
    b.p('Mission : préparer 50 mL d’eau et déterminer leur masse.',22,82,166,14,font='Bold',color=NAVY)
    b.bullets([
        '<b>Choisir :</b> éprouvette adaptée, balance, récipient sec et eau. Vérifier la capacité et la graduation.',
        '<b>Mesurer :</b> préparer 50 mL d’eau en lisant à hauteur du ménisque.',
        '<b>Peser :</b> faire la tare avec le récipient sec, transférer l’eau sans perte puis relever la masse.'
    ],97,size=11.7,gap=4)
    b.table([['Essai','Volume préparé','Masse mesurée'],['1','........................','........................'],['2','........................','........................'],['3','........................','........................']],158,[27,69,70],rowheight=13,size=11.5)
    b.box('ANALYSER LES RÉSULTATS','Compare les essais. Une masse voisine de 50 g est attendue pour 50 mL d’eau à température ambiante. Si l’écart est important, vérifie la tare, la lecture et les pertes au transfert avant de conclure.',225,35,size=11.7)
    b.p('Activité en classe avec le professeur. Relever les résultats réellement obtenus, même s’ils diffèrent de la valeur attendue.',23,266,164,10.4,color=MUTED)
    page(b,'ch-2-bilan','La méthode en quatre questions',2,rub='SYNTHÈSE')
    t=83
    for lab,body in [('1 · Quelle grandeur ?','Masse m ou volume V ? Je ne mélange pas les deux.'),('2 · Quel instrument et quelle unité ?','Balance et g ou kg ; éprouvette et mL ou L. Un résultat comporte une valeur et une unité.'),('3 · Quel protocole ?','Tare ou différence pour une masse ; bas du ménisque pour un liquide ; différence avant/après pour un solide immergé.'),('4 · Mon résultat est-il cohérent ?','Je contrôle l’unité, l’ordre de grandeur et les conditions de mesure. Une différence de volumes doit rester positive dans l’expérience d’immersion.')]:
        b.box(lab,body,t,34,size=11.8,fill=PALE if int(lab[0])%2 else MINT);t+=40
    b.p('La physique-chimie demande autant de soin dans le choix de la méthode que dans le calcul.',23,258,164,12,color=GREEN,font='Bold')

def ex_height(b,e):
    h=max(8,b.p(e.titre,w=142,size=13.4,font='Bold',measure=True))+4
    if e.document:h+=b.p(e.document,w=158,size=11.1,measure=True)+8
    if e.figure:h+=e.hauteur+3+(b.p(e.caption,w=166,size=9.5,measure=True)+3 if e.caption else 0)
    for q in e.questions:h+=max(5,b.p(q,w=157,size=11.8,measure=True))+2
    return h+7

def render_ex(b,e,chapter,top):
    key=f'ex-{chapter}-{e.n}';b.dest[key]=b.page;b.c.bookmarkPage(key);b.exercises.append(dict(chapter=chapter,n=e.n,page=b.page))
    b.rect(22,top,19,8,fill=NAVY);b.p(f'{chapter:02}.{e.n:02}',23.7,top+1.3,16,10.5,font='Bold',color=white);b.link(f'cor-{chapter}-{e.n}',22,top,19,8)
    t=max(top+8,b.p(e.titre,45,top,142,13.4,font='Bold'))+4
    if e.document:
        ph=b.p(e.document,w=158,size=11.1,measure=True);b.rect(22,t,166,ph+5,fill=PALE);b.p(e.document,26,t+2.5,158,11.1,maxbottom=t+ph+5);t+=ph+8
    if e.figure:t=b.fig(e.figure,t,e.hauteur,caption=e.caption or None)+3
    for idx,q in enumerate(e.questions):
        b.p(chr(97+idx)+'.',23,t,6,11.8,font='Bold',color=GREEN);t=b.p(q,31,t,157,11.8)+2
    b.line(22,t+3,188);return t+6

def exercices(b,chapter,items):
    groups=[('Je démarre','NIVEAU 1',items[:5]),('Je m’entraîne','NIVEAU 2',items[5:11]),('Je raisonne','NIVEAU 3',items[11:])]
    for part,(title,level,group) in enumerate(groups,1):
        k=1;page(b,f'ch-{chapter}-ex-{part}-{k}',title,chapter,sub='Réponds dans ton cahier. Les numéros ouvrent les corrigés.',rub=level);t=82
        for e in group:
            if t+ex_height(b,e)>274:
                k+=1;page(b,f'ch-{chapter}-ex-{part}-{k}',title,chapter,sub='Réponds dans ton cahier. Explique tes réponses.',rub=level);t=82
            t=render_ex(b,e,chapter,t)
        if t<233:b.box('POUR PROGRESSER','Avant le corrigé, cherche une propriété, un schéma ou une étape de méthode qui peut t’aider. Après correction, explique l’erreur puis refais une question proche.',246,29,size=11.1,fill=MINT,accent=GREEN)

def defis(b,n):
    if n==1:
        page(b,'defi-1','Transférer de l’air sous l’eau',1,rub='DÉFI · PRENDRE UNE INITIATIVE')
        b.p('Deux gobelets transparents rigides sont retournés dans un bac d’eau. A contient de l’air ; B est entièrement rempli d’eau. Comment transférer une partie de l’air de A vers B, sans les sortir de l’eau ?',22,82,166,12.5)
        b.fig(('airtransfer',False),120,79,caption='Les ouvertures des gobelets sont dirigées vers le bas. Situation schématisée.')
        b.bullets(['Propose une disposition et un geste. Fais un schéma légendé.','Prévois le trajet de l’air et ce qui arrive à l’eau dans B.','Justifie ta proposition avec une propriété étudiée dans le chapitre.'],217,size=11.8,gap=3)
        b.p('Indice progressif : les bulles d’air remontent dans l’eau. Le test éventuel se réalise avec le professeur et du matériel adapté.',23,264,164,10.6,color=MUTED)
    else:
        page(b,'defi-2','Une bille trop petite pour être lue seule',2,rub='DÉFI · PRENDRE UNE INITIATIVE')
        b.p('Le volume d’une seule bille est trop petit pour être facilement lu avec l’éprouvette disponible. On dispose de vingt billes identiques et d’une balance.',22,82,166,12.5)
        b.fig(('balls',None),111,47)
        b.box('DONNÉES À EXPLOITER','Avec les 20 billes entièrement immergées, le volume passe de 40 mL à 50 mL. La masse totale des 20 billes est de 78,0 g. On suppose les billes identiques, insolubles et sans bulle accrochée.',174,36,size=12)
        b.bullets(['Explique pourquoi mesurer plusieurs billes est utile.','Détermine le volume moyen d’une bille, en cm³.','Détermine sa masse moyenne et explique les limites de la mesure.'],226,size=11.8,gap=3)

def corriges(b,chapter,items):
    groups=[items[:5],items[5:11],items[11:]]
    for part,group in enumerate(groups,1):
        page(b,f'cor-{chapter}-groupe-{part}',f'Corrigés expliqués · {group[0].n:02} à {group[-1].n:02}',chapter,rub='COMPRENDRE ET SE CORRIGER');t=82
        for e in group:
            key=f'cor-{chapter}-{e.n}';b.dest[key]=b.page;b.c.bookmarkPage(key)
            b.p(f'{chapter:02}.{e.n:02}',22,t,18,11.5,font='Bold',color=NAVY);b.link(f'ex-{chapter}-{e.n}',22,t,18,8)
            t=b.p(e.reponse,44,t,144,11.4,leading=14.7,maxbottom=244)+6
        if t<240:b.box('UN RÉFLEXE UTILE','Revenir à l’énoncé, repérer ce qui a été demandé et vérifier chaque unité. Un résultat juste doit être accompagné d’une explication adaptée à la question.',247,29,size=11,fill=MINT,accent=GREEN)
    if chapter==1:
        page(b,'cor-defi-1','Le trajet de l’air',1,rub='CORRIGÉ DU DÉFI')
        b.p('Une solution consiste à placer l’ouverture de B au-dessus de celle de A, puis à incliner doucement A pour libérer des bulles. Les bulles remontent et entrent dans B ; elles y remplacent une partie de l’eau.',22,82,166,12.3)
        b.fig(('airtransfer',True),120,76,caption='État après un transfert suffisant : A contient davantage d’eau et B contient de l’air.')
        b.box('CE QU’IL FALLAIT JUSTIFIER','L’air est une matière qui occupe un volume et peut se déplacer. L’eau peut être remplacée par de l’air dans un récipient. La réussite dépend de la position des ouvertures : les bulles doivent pouvoir atteindre l’intérieur de B.',215,38,size=11.7)
        b.p('Accepter tout montage équivalent, correctement légendé et compatible avec le trajet ascendant des bulles.',23,265,164,11,color=MUTED)
    else:
        page(b,'cor-defi-2','Passer du lot à une bille',2,rub='CORRIGÉ DU DÉFI')
        b.box('1 · MESURER UN VOLUME TOTAL','Le lot déplace 50 mL - 40 mL = 10 mL d’eau. Ce volume total est plus facile à distinguer sur les graduations que le volume d’une bille isolée.',83,36,size=12)
        b.box('2 · TROUVER UN VOLUME MOYEN','Les billes sont supposées identiques : 10 mL ÷ 20 = 0,5 mL par bille, soit 0,5 cm³.',130,31,size=12,fill=MINT,accent=GREEN)
        b.box('3 · TROUVER UNE MASSE MOYENNE','78,0 g ÷ 20 = 3,9 g par bille. Cette division concerne la masse ; elle ne convertit pas un volume en masse.',173,31,size=12)
        b.box('4 · DISCUTER LA MESURE','Les lectures restent approximatives. Il faut éviter les bulles, immerger toutes les billes et ne pas perdre d’eau. Le calcul donne une moyenne et n’invente pas une graduation plus fine. Si les billes diffèrent, on ne connaît pas exactement chaque bille.',216,42,size=11.6,fill=CREAM,accent=ORANGE)

def fin(b):
    b.begin('programme','Des repères pour la suite','PROGRAMME ET PROGRESSION',outline=True)
    b.p('Le programme national définit les attendus sur les trois années du cycle 4. Le plan de ce manuel propose une progression de 5e ; l’équipe pédagogique peut organiser les apprentissages autrement.',22,82,166,12)
    b.table([
        ['Thème officiel','Chapitres prévus'],
        ['Organisation et transformations de la matière','1 à 8'],
        ['Mouvement et interactions','9 à 11'],
        ['Énergie, transferts et conversions','12 à 16'],
        ['Signaux pour observer et communiquer','17 à 20']
    ],116,[130,36],rowheight=15,size=11.6)
    b.box('LES DEUX CHAPITRES INCLUS','États de la matière, propriétés observables et modèle simple ; mesures de masse et de volume, unités, lecture d’instruments et proportionnalité pour une même substance. Ces apprentissages s’appuient sur les repères de début de cycle.',207,35,size=11.5,fill=MINT,accent=GREEN)
    b.p('La grandeur quotient « masse volumique », les équations de réaction, les forces et les lois électriques formalisées seront approfondies aux niveaux suivants conformément à la progressivité du cycle.',23,253,164,11.4,color=MUTED)
    for part in range(2):
        b.begin(f'sources-{part+1}','Références et choix éditoriaux',f'SOURCES CONSULTÉES LE 23 OCTOBRE 2026 · {part+1}/2',outline=part==0);t=82
        for i,(title,desc,url) in enumerate(SOURCES[part*3:(part+1)*3],start=part*3+1):
            b.p(f'{i}. {title}',22,t,166,13,font='Bold',color=NAVY);b.url(url,22,t,166,8)
            t=b.p(desc,22,t+10,166,11.6)+5
            t=b.p(url.replace('https://',''),22,t,166,9.2,color=MUTED)+13
        if part==1:
            b.box('CRÉATIONS ORIGINALES','Textes, situations, exercices, corrigés et schémas ont été créés pour cet ouvrage. Les sources officielles servent de références au programme et aux démarches. Les données présentées comme pédagogiques sont des exemples à exploiter, non des mesures réalisées par l’élève.',226,44,size=11.1)

def construire(path,refs=None):
    b=Livre(path,refs);couverture(b);debut(b);cours1(b);exercices(b,1,CH1);defis(b,1);cours2(b);exercices(b,2,CH2);defis(b,2);corriges(b,1,CH1);corriges(b,2,CH2);fin(b);b.save();return b

if __name__=='__main__':
    a=construire(BUILD/'mise-en-page.pdf');b=construire(BUILD/'optitab-physique-chimie-5e-apercu.pdf',a.dest)
    assert a.dest==b.dest
    meta=dict(pages=b.page,chapitres_rediges=2,chapitres_au_sommaire=20,exercices=30,defis=2,insertions_schemas=len(b.figures),destinations=b.dest,plan=b.pages,exercices_pages=b.exercises)
    (BUILD/'manifeste.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf8')
    (BUILD/'blocs-texte.json').write_text(json.dumps(b.blocks,ensure_ascii=False,indent=2),encoding='utf8')
    (BUILD/'blocs-figures.json').write_text(json.dumps(b.figures,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in meta.items() if k not in ['destinations','plan','exercices_pages']},ensure_ascii=False))
