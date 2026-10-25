"""Matériel autonome et fiches de référence à imprimer à 100 %."""
from mise_en_page import mm,H,white,NAVY,GREEN,MUTED,RULE,MINT,PALE

def construire_outils(b):
    b.begin('outils-intro','Matériel et fiches outils','À PHOTOCOPIER ET À MANIPULER');b.outline('Matériel et fiches outils','outils-intro')
    for top,title,body in [(83,'Pour comprendre','Photocopier les outils, déplacer les cartes, superposer les bandes et expliquer les échanges. Les bandes de fractions d’un tout et les règles en fractions d’unité ont des usages différents.'),(141,'Pour construire','Utiliser le quadrillage, le papier pointé et les patrons. L’adulte accompagne le découpage et les gestes au compas. Les solides s’assemblent avec du ruban adhésif.'),(199,'Pour imprimer','A4 à 100 %, sans ajustement. Le repère ci-dessous doit mesurer exactement 5 cm. Vérifier avant les mesures et les constructions.')]:
        b.text(title,20,top,172,16,bold=True,color=GREEN);b.text(body,20,top+14,172,13.2)
    b.line(32,252,82,color=NAVY,width=2)
    for x in [32,82]:b.c.setStrokeColor(NAVY);b.c.line(x*mm,H-248*mm,x*mm,H-256*mm)
    b.text('5 cm',48,261,35,12,bold=True)
    b.begin('outil-numeration','Milliers, centaines, dizaines, unités','TABLEAUX À PHOTOCOPIER')
    b.text('Place des chiffres ou des cartes. Explique les échanges : dix unités d’un rang forment une unité du rang suivant.',20,82,172,13.2)
    for top in [111,166,221]:
        for j,lab in enumerate(['milliers','centaines','dizaines','unités']):
            x=23+j*41;b.rect(x,top,41,43,fill=white,stroke=RULE,r=0);b.text(lab,x+2,top+5,38,11.2,bold=True,color=GREEN);b.line(x,top+16,x+41)
    b.begin('outil-cartes','Des cartes pour les échanges','MATÉRIEL À DÉCOUPER')
    b.text('Une carte vaut la quantité écrite. Dix cartes de 100 unités peuvent être échangées contre une carte de 1 000 unités.',20,82,172,13.2)
    for r in range(5):
        for j,v in enumerate([1000,100,10,1]):
            x=23+j*42;top=114+r*31;b.rect(x,top,38,25,fill=MINT,stroke=NAVY,r=0);b.text(f'{v:,}'.replace(',',' '),x+4,top+5,31,16,bold=True,color=NAVY)
    b.begin('outil-mots','Écrire les nombres en lettres','OUTIL POUR LA NUMÉRATION')
    words=[(0,'zéro'),(1,'un'),(2,'deux'),(3,'trois'),(4,'quatre'),(5,'cinq'),(6,'six'),(7,'sept'),(8,'huit'),(9,'neuf'),(10,'dix'),(11,'onze'),(12,'douze'),(13,'treize'),(14,'quatorze'),(15,'quinze'),(16,'seize'),(20,'vingt'),(30,'trente'),(40,'quarante')]
    for i,(n,s) in enumerate(words):b.text(f'{n}   {s}',23+(i//10)*84,83+(i%10)*9,80,12.5)
    b.box('LES AUTRES REPÈRES','50 : cinquante · 60 : soixante · 70 : soixante-dix\n80 : quatre-vingts · 90 : quatre-vingt-dix\n100 : cent · 1 000 : mille · 10 000 : dix-mille',181,41,size=12.1)
    b.box('POUR L’ADULTE','Les éléments des nombres sont reliés par des traits d’union. Cent et vingt prennent un s lorsqu’ils sont multipliés et terminent le nombre : deux-cents, quatre-vingts. Mille est invariable : deux-mille ; deux-cent-un ; quatre-vingt-un.',231,44,size=10.8)
    for op,key,title in [('+','addition','Les tables d’addition'),('×','multiplication','Les tables de multiplication')]:
        b.begin('outil-table-'+key,title,'OUTIL POUR MÉMORISER',subtitle='Cache une case, cherche le résultat, puis vérifie.')
        step=14;left=21;top=86
        for r in range(12):
            for j in range(12):
                v=op if r==0 and j==0 else str(j-1) if r==0 else str(r-1) if j==0 else str((r-1)+(j-1) if op=='+' else (r-1)*(j-1))
                b.rect(left+j*step,top+r*step,step,step,fill=MINT if r==0 or j==0 else white,stroke=RULE,r=0);b.text(v,left+j*step+2.7,top+r*step+4,step-3,11.8,bold=r==0 or j==0)
        b.text('Cherche aussi un facteur ou un terme manquant.',22,263,168,12,color=MUTED)
    b.begin('outil-faits','Doubles, moitiés et produits utiles','FICHE DE RÉFÉRENCE')
    b.text('La flèche indique le double. Pour trouver une moitié, lis dans l’autre sens.',20,82,172,12.7)
    for i in range(1,21):b.text(f'{i} → {2*i}',27+((i-1)//10)*85,106+((i-1)%10)*8.3,76,12.7)
    b.box('DOUBLES À REPRENDRE','25 → 50 ; 30 → 60 ; 35 → 70 ; 40 → 80 ; 45 → 90\n50 → 100 ; 60 → 120 ; 75 → 150\n100 → 200 ; 150 → 300 ; 200 → 400 ; 250 → 500\n300 → 600 ; 400 → 800 ; 500 → 1 000 ; 600 → 1 200',194,47,size=11.2)
    b.box('LES MULTIPLES DE 25 ET LES PRODUITS DE 60','25 ; 50 ; 75 ; 100\n60 = 1 × 60 = 2 × 30 = 3 × 20 = 4 × 15 = 5 × 12 = 6 × 10',248,28,size=10.7)
    b.begin('outil-fractions','Des fractions d’un même tout','BANDES À DÉCOUPER')
    b.text('Toutes ces bandes représentent un tout identique. Découpe les bandes entières, puis leurs parts pour superposer et comparer.',20,82,172,12.7)
    for i,n in enumerate(range(2,13)):
        top=111+i*14.7;b.text(f'{n} parts',19,top+3,29,10.5,bold=True,color=GREEN)
        for j in range(n):b.rect(51+j*132/n,top,132/n,10,fill=MINT if j==0 else white,stroke=NAVY,r=0)
    b.begin('outil-regles-fractions','Mesurer en fractions de l’unité u','RÈGLES À DÉCOUPER')
    b.text('L’unité u mesure 4 cm sur cette fiche imprimée à 100 %. Chaque règle utilise la même unité. Découpe en gardant les graduations.',20,82,172,12.7)
    for row,den in enumerate([4,8,10]):
        top=117+row*47;b.text(f'Règle en {den} parts par unité',23,top,165,12.2,bold=True,color=GREEN)
        left=40;yt=top+23;b.line(left,yt,left+120,color=NAVY)
        for j in range(3*den+1):
            x=left+j*40/den;b.c.setStrokeColor(NAVY);b.c.setLineWidth(.7);b.c.line(x*mm,H-yt*mm,x*mm,H-(yt-(5 if j%den==0 else 2.8))*mm)
            if j%den==0:
                b.c.setFont('Text',10.5);b.c.setFillColor(MUTED)
                b.c.drawCentredString(x*mm,H-(yt+7)*mm,'0' if j==0 else f'{j//den} u')
    b.box('POUR RETROUVER L’UNITÉ','Une bande de 1/4 u se reporte quatre fois. Une bande de 1/10 u se reporte dix fois. Dans chaque cas, les morceaux sont mis bout à bout.',250,26,size=10.3)
    b.begin('outil-monnaie','Pièces et billets du magasin','MONNAIE DE JEU À DÉCOUPER')
    b.text('c signifie centime. 100 centimes valent 1 euro.',20,82,172,13.4)
    b.fig(('centcoins',[1,2,5,10]),107,36);b.fig(('centcoins',[20,50,100,200]),153,36)
    b.fig(('money',[5,10,20,50]),204,34);b.fig(('money',[10,20,50]),250,24)
    b.begin('outil-horloges','Des horloges à compléter','OUTIL À PHOTOCOPIER')
    b.text('Chaque petit intervalle vaut une minute. Dessine les deux aiguilles et fais avancer la petite entre les heures.',20,82,172,13)
    for top in [111,166,221]:b.fig(('minuteclocks',[[None,0],[None,0]]),top,46)
    b.begin('outil-grille','Un quadrillage pour construire','OUTIL À PHOTOCOPIER')
    b.text('Un carreau mesure 1 cm à l’impression à 100 %. Vérifie les longueurs et les angles avec les instruments.',20,82,172,13)
    for j in range(17):b.c.setStrokeColor(RULE);b.c.setLineWidth(.4);b.c.line((25+j*10)*mm,H-111*mm,(25+j*10)*mm,H-271*mm)
    for j in range(17):b.line(25,111+j*10,185,width=.4)
    b.begin('outil-points','Du papier pointé pour chercher','OUTIL À PHOTOCOPIER')
    b.text('Deux points voisins horizontalement ou verticalement sont distants de 1 cm.',20,82,172,13)
    b.c.setFillColor(MUTED)
    for i in range(17):
        for j in range(17):b.c.circle((25+i*10)*mm,H-(111+j*10)*mm,.45*mm,stroke=0,fill=1)
    for orient in ['vertical','horizontal']:
        b.begin('outil-symetrie-'+orient,'Créer une figure symétrique','QUADRILLAGE AVEC AXE '+orient.upper())
        b.text('Dessine une demi-figure, complète de l’autre côté de l’axe, puis vérifie par pliage ou calque.',20,82,172,13)
        for j in range(17):b.c.setStrokeColor(RULE);b.c.setLineWidth(.4);b.c.line((25+j*10)*mm,H-111*mm,(25+j*10)*mm,H-271*mm)
        for j in range(17):b.line(25,111+j*10,185,width=.4)
        b.c.setStrokeColor(GREEN);b.c.setLineWidth(1.2);b.c.setDash(4,3)
        if orient=='vertical':b.c.line(105*mm,H-111*mm,105*mm,H-271*mm)
        else:b.c.line(25*mm,H-191*mm,185*mm,H-191*mm)
        b.c.setDash()
    b.begin('outil-patrons','Deux assemblages à essayer','MATÉRIEL POUR LES PATRONS DU CUBE')
    b.text('Prévois ce qui se passera au pliage. Découpe les contours des deux assemblages sur des copies. Plie et vérifie : lequel permet de fermer un cube ?',20,82,172,12.7)
    cells=[(1,0),(0,1),(1,1),(2,1),(1,2),(1,3)];side=25;left=68;top=115
    b.text('A',43,121,20,15,bold=True,color=GREEN)
    for i,j in cells:
        for a,bb,neighbor in [((i,j),(i+1,j),(i,j-1)),((i,j+1),(i+1,j+1),(i,j+1)),((i,j),(i,j+1),(i-1,j)),((i+1,j),(i+1,j+1),(i+1,j))]:
            b.c.setStrokeColor(NAVY);b.c.setLineWidth(.9)
            if neighbor in cells:b.c.setDash(3,2)
            else:b.c.setDash()
            b.c.line((left+a[0]*side)*mm,H-(top+a[1]*side)*mm,(left+bb[0]*side)*mm,H-(top+bb[1]*side)*mm)
    b.c.setDash();b.text('B',19,236,15,15,bold=True,color=GREEN)
    for i in range(6):b.rect(35+i*25,233,25,25,fill=white,stroke=NAVY,r=0)
    b.text('Les carrés ont un côté de 2 cm et 5 mm. Les pointillés intérieurs de A indiquent les plis.',20,267,172,10.6,color=MUTED)
    b.begin('outil-pave','Six faces pour construire un pavé','MATÉRIEL À DÉCOUPER')
    b.text('Assemble les faces avec du ruban adhésif. Le pavé a des longueurs de 4 cm, 3 cm et 2 cm.',20,82,172,13)
    for row,(ww,hh) in enumerate([(40,30),(40,20),(30,20)]):
        for col in range(2):b.rect(42+col*88,119+row*51,ww,hh,fill=white,stroke=NAVY,r=0)
    b.text('Tu obtiens deux faces de chaque type. Vérifie les arêtes qui doivent se rejoindre.',20,266,172,11.1,color=MUTED)
    b.begin('outil-pyramide','Les faces d’une pyramide','MATÉRIEL À DÉCOUPER AVEC L’ADULTE')
    b.text('La base est un carré. Les quatre autres faces sont des triangles identiques. Assemble les bords avec du ruban adhésif.',20,82,172,13)
    b.rect(84,110,40,40,fill=white,stroke=NAVY,r=0)
    for row in range(2):
        for col in range(2):
            x=36+col*100;top=171+row*54;p=b.c.beginPath();p.moveTo(x*mm,H-(top+40)*mm);p.lineTo((x+40)*mm,H-(top+40)*mm);p.lineTo((x+20)*mm,H-top*mm);p.close();b.c.setStrokeColor(NAVY);b.c.drawPath(p,stroke=1,fill=0)
    b.text('Le côté du carré et la base de chaque triangle mesurent 4 cm.',20,270,172,11.2,color=MUTED)
    groups=[
    ('A · Faits d’addition · 1 minute',['8 + 7','9 + 6','7 + 7','6 + 8','4 + 9','5 + 8','3 + 9','6 + 6','7 + 4','8 + 8','9 + 9','5 + 7','4 + 8','6 + 5','10 + 0'],'15 ; 15 ; 14 ; 14 ; 13 ; 13 ; 12 ; 12 ; 11 ; 16 ; 18 ; 12 ; 12 ; 11 ; 10.'),
    ('B · Faits de multiplication · 1 minute',['7 × 8','6 × 9','8 × 8','9 × 7','6 × 6','4 × 8','9 × 9','7 × 6','8 × 3','5 × 9','4 × 7','6 × 8'],'56 ; 54 ; 64 ; 63 ; 36 ; 32 ; 81 ; 42 ; 24 ; 45 ; 28 ; 48.'),
    ('C · Faits usuels · 1 minute',['double de 75','moitié de 150','double de 600','moitié de 800','double de 35','moitié de 90','3 × 25','4 × … = 60','moitié de 1 200','double de 45','5 × … = 60','double de 250'],'150 ; 75 ; 1 200 ; 400 ; 70 ; 45 ; 75 ; 15 ; 600 ; 90 ; 12 ; 500.'),
    ('D · Procédures · 3 minutes',['2 478 + 38','4 205 - 29','72 × 100','8 × 40','37 × 6','45 × 4','25 × 8','1 504 - 9','3 206 + 28','89 × 4','406 × 10','6 432 - 29','75 × 8','4 001 - 39','35 × 4'],'2 516 ; 4 176 ; 7 200 ; 320 ; 222 ; 180 ; 200 ; 1 495 ; 3 234 ; 356 ; 4 060 ; 6 403 ; 600 ; 3 962 ; 140.')]
    for part in range(2):
        b.begin('outil-fluence-'+str(part+1),'Observer les progrès en calcul','FICHE POUR L’ADULTE',adult=True)
        b.text('Proposer après apprentissage, à plusieurs dates. Cacher les fiches de référence. Garder les adaptations habituelles.',20,82,172,11.8)
        for row,(title,qs,answers) in enumerate(groups[part*2:(part+1)*2]):
            top=111+row*83;b.text(title,20,top,172,12.2,bold=True,color=GREEN)
            for i,q in enumerate(qs):
                suffix='' if '…' in q else ' = …';b.text(q+suffix,23+(i%3)*56,top+15+(i//3)*10,54,10.8)
            b.text('Réponses : '+answers,23,top+66,168,9.3,leading=11.8,color=MUTED)
