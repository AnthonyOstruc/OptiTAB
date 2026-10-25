"""Matériel à photocopier et fiches de mémorisation du CE1."""
from mise_en_page import mm,H,white,NAVY,GREEN,MUTED,RULE,MINT,PALE

def construire_outils(b):
    b.begin('outils-intro','Matériel et fiches outils','À PHOTOCOPIER ET À MANIPULER',subtitle='Utiliser des copies pour conserver le livre.');b.outline('Matériel et fiches outils','outils-intro')
    for top,title,body in [(83,'Pour comprendre','Les plaques, les bandes de fractions et la monnaie de jeu permettent de vérifier une idée. Faire raconter ce que représentent les pièces du matériel.'),(137,'Pour construire','L’adulte accompagne les découpages et les premiers gestes au compas. Les faces se joignent avec du ruban adhésif ou de la pâte.'),(191,'Pour imprimer','A4, taille réelle à 100 %, sans ajustement. Ce repère doit mesurer exactement 5 cm avec une vraie règle.')]:
        b.text(title,20,top,172,17,bold=True,color=GREEN);b.text(body,20,top+15,172,13.4)
    b.line(32,250,82,color=NAVY,width=2)
    for x in [32,82]:b.c.setStrokeColor(NAVY);b.c.line(x*mm,H-246*mm,x*mm,H-254*mm)
    b.text('5 cm',48,258,35,12,bold=True)
    b.begin('outil-centaines','Plaques, barres et unités','MATÉRIEL À DÉCOUPER')
    b.text('Une plaque vaut 100 unités. Une barre vaut 10 unités.',20,82,172,13.4)
    for pos in range(4):
        x=28+(pos%2)*86;top=108+(pos//2)*64
        b.rect(x,top,50,50,fill=MINT,stroke=GREEN,r=0)
        for k in range(1,10):b.line(x,top+k*5,x+50,color=GREEN,width=.4);b.c.line((x+k*5)*mm,H-top*mm,(x+k*5)*mm,H-(top+50)*mm)
    for pos in range(4):
        x=28+pos*14
        for k in range(10):b.rect(x,227+k*5,5,5,fill=MINT,stroke=GREEN,r=0)
    for pos in range(20):b.rect(90+(pos%10)*9,245+(pos//10)*14,5,5,fill=PALE,stroke=NAVY,r=0)
    b.begin('outil-numeration','Centaines, dizaines, unités','OUTIL À PHOTOCOPIER')
    b.text('Place les chiffres ou le matériel. Fais les échanges et explique la valeur des rangs.',20,82,172,13.4)
    for top in [110,163,216]:
        for i,label in enumerate(['centaines','dizaines','unités']):
            x=24+i*54;b.rect(x,top,54,43,fill=white,stroke=RULE,r=0);b.text(label,x+5,top+5,45,12,bold=True,color=GREEN);b.line(x,top+16,x+54)
    b.begin('outil-mots','Écrire les nombres en lettres','OUTIL POUR LA NUMÉRATION')
    words=[(0,'zéro'),(1,'un'),(2,'deux'),(3,'trois'),(4,'quatre'),(5,'cinq'),(6,'six'),(7,'sept'),(8,'huit'),(9,'neuf'),(10,'dix'),(11,'onze'),(12,'douze'),(13,'treize'),(14,'quatorze'),(15,'quinze'),(16,'seize'),(20,'vingt'),(30,'trente'),(40,'quarante')]
    for i,(n,s) in enumerate(words):col=i//10;row=i%10;b.text(f'{n}   {s}',23+col*84,83+row*9,80,12.5)
    b.box('LES AUTRES REPÈRES','50 : cinquante · 60 : soixante · 70 : soixante-dix\n80 : quatre-vingts · 90 : quatre-vingt-dix\n100 : cent · 1 000 : mille',181,41,size=12.2)
    b.box('POUR L’ADULTE','Dans ce livre, les éléments des nombres sont reliés par des traits d’union. Cent et vingt prennent un s quand ils sont multipliés et terminent le nombre : deux-cents, quatre-vingts ; deux-cent-un, quatre-vingt-un. Mille est invariable.',231,44,size=10.8)
    for op,key,title in [('+','addition','Les tables d’addition'),('×','multiplication','Les tables de multiplication')]:
        b.begin('outil-table-'+key,title,'OUTIL POUR MÉMORISER',subtitle='Cache une case, cherche le résultat, puis vérifie.')
        step=14;left=21;top=86
        for r in range(12):
            for col in range(12):
                value=op if r==0 and col==0 else str(col-1) if r==0 else str(r-1) if col==0 else str((r-1)+(col-1) if op=='+' else (r-1)*(col-1))
                b.rect(left+col*step,top+r*step,step,step,fill=MINT if r==0 or col==0 else white,stroke=RULE,r=0);b.text(value,left+col*step+2.7,top+r*step+4,step-3,11.8,bold=r==0 or col==0)
        b.text('Retrouve aussi un nombre manquant dans une égalité.',22,263,168,12,color=MUTED)
    b.begin('outil-doubles','Doubles et moitiés utiles','FICHE DE RÉFÉRENCE')
    b.text('Le double de chaque nombre est indiqué à droite. Pour lire une moitié, pars du résultat et reviens au nombre de départ.',20,82,172,13)
    for i in range(1,16):col=(i-1)//8;row=(i-1)%8;b.text(f'{i} → {2*i}',28+col*84,114+row*11,75,15)
    b.box('D’AUTRES DOUBLES À CONNAÎTRE','20 → 40 ; 25 → 50 ; 30 → 60 ; 35 → 70\n40 → 80 ; 45 → 90 ; 50 → 100\n100 → 200 ; 150 → 300 ; 200 → 400\n250 → 500 ; 300 → 600 ; 500 → 1 000',217,57,size=12.5)
    b.begin('outil-fractions','Des bandes de fractions','MATÉRIEL À DÉCOUPER')
    b.text('Chaque bande représente le même tout. Découpe d’abord les bandes entières, puis leurs parts. Superpose pour comparer.',20,82,172,13)
    for i,n in enumerate([2,3,4,5,6,8,10]):
        top=113+i*22;b.text(f'{n} parts',19,top+4,29,11.2,bold=True,color=GREEN)
        for j in range(n):b.rect(51+j*132/n,top,132/n,13,fill=MINT if j==0 else white,stroke=NAVY,r=0)
    b.text('Une part de la dernière bande est un dixième du tout.',20,271,172,11.5,color=MUTED)
    b.begin('outil-monnaie','Pièces et billets du magasin','MONNAIE DE JEU À DÉCOUPER')
    b.text('c signifie centime. 100 centimes valent 1 euro.',20,82,172,13.4)
    b.fig(('centcoins',[1,2,5,10]),107,36);b.fig(('centcoins',[20,50,100,200]),153,36)
    b.fig(('money',[5,10,20,50]),204,34);b.fig(('money',[10,20,50]),250,24)
    b.begin('outil-horloges','Des horloges à compléter','OUTIL À PHOTOCOPIER')
    b.text('Dessine les deux aiguilles. Pense à faire avancer la petite aiguille entre deux heures.',20,82,172,13.4)
    for top in [110,166,222]:b.fig(('blankclocks',2),top,46)
    b.begin('outil-grille','Un quadrillage pour construire','OUTIL À PHOTOCOPIER')
    b.text('Un carreau mesure 1 cm à l’impression à 100 %. Vérifie les longueurs et les angles avec les instruments.',20,82,172,13.4)
    for i in range(17):b.c.setStrokeColor(RULE);b.c.setLineWidth(.4);b.c.line((25+i*10)*mm,H-111*mm,(25+i*10)*mm,H-271*mm)
    for j in range(17):b.line(25,111+j*10,185,width=.4)
    b.begin('outil-points','Du papier pointé pour chercher','OUTIL À PHOTOCOPIER')
    b.text('Place les sommets, puis relie-les. Les intervalles entre deux points voisins mesurent 1 cm.',20,82,172,13.4)
    b.c.setFillColor(MUTED)
    for i in range(17):
        for j in range(17):b.c.circle((25+i*10)*mm,H-(111+j*10)*mm,.45*mm,stroke=0,fill=1)
    b.begin('outil-cube','Six faces pour construire un cube','MATÉRIEL À DÉCOUPER AVEC L’ADULTE')
    b.text('Ces six carrés identiques sont les faces du cube. Assemble-les en observant un cube réel.',20,82,172,13.4)
    for i in range(6):b.rect(40+(i%2)*78,115+(i//2)*53,40,40,fill=white,stroke=NAVY,r=0)
    b.text('Les côtés mesurent 4 cm à l’impression à 100 %.',20,268,172,11.5,color=MUTED)
    b.begin('outil-pyramide','Les faces d’une pyramide','MATÉRIEL À DÉCOUPER AVEC L’ADULTE')
    b.text('La base est un carré. Les quatre autres faces sont des triangles identiques. Assemble les bords avec du ruban adhésif.',20,82,172,13.4)
    b.rect(84,110,40,40,fill=white,stroke=NAVY,r=0)
    for row in range(2):
        for col in range(2):
            x=36+col*100;top=171+row*54;p=b.c.beginPath();p.moveTo(x*mm,H-(top+40)*mm);p.lineTo((x+40)*mm,H-(top+40)*mm);p.lineTo((x+20)*mm,H-top*mm);p.close();b.c.setStrokeColor(NAVY);b.c.drawPath(p,stroke=1,fill=0)
    b.text('Le côté du carré et la base de chaque triangle mesurent 4 cm.',20,270,172,11.2,color=MUTED)
    groups=[
      ('A · Faits d’addition · 1 minute',['3 + 7','6 + 8','9 + 4','5 + 5','7 + 6','4 + 8','8 + 2','6 + 9','7 + 7','4 + 5','10 + 0','9 + 9'],'10 ; 14 ; 13 ; 10 ; 13 ; 12 ; 10 ; 15 ; 14 ; 9 ; 10 ; 18.'),
      ('B · Faits de multiplication · 1 minute',['7 × 8','6 × 4','9 × 3','5 × 7','8 × 8','6 × 9','4 × 7','9 × 9'],'56 ; 24 ; 27 ; 35 ; 64 ; 54 ; 28 ; 81.'),
      ('C · Doubles et moitiés usuels · 1 minute',['double de 15','moitié de 70','double de 250','moitié de 500','double de 35','moitié de 26','double de 150','moitié de 1 000'],'30 ; 35 ; 500 ; 250 ; 70 ; 13 ; 300 ; 500.'),
      ('D · Calculs par procédure · 3 minutes',['234 + 60','746 + 80','72 × 10','357 + 19','680 + 29','246 - 9','523 - 7','moitié de 470','14 × 6','18 × 4','765 - 200','354 + 500'],'294 ; 826 ; 720 ; 376 ; 709 ; 237 ; 516 ; 235 ; 84 ; 72 ; 565 ; 854.')]
    for part in range(2):
        b.begin('outil-fluence-'+str(part+1),'Observer les progrès en calcul','FICHE POUR L’ADULTE',adult=True)
        b.text('Après l’apprentissage, relever les réussites à plusieurs dates. Laisser les fiches de référence hors de vue pendant l’observation.',20,82,172,11.8)
        for row,(title,qs,answers) in enumerate(groups[part*2:(part+1)*2]):
            top=115+row*81;b.text(title,20,top,172,12.3,bold=True,color=GREEN)
            for i,q in enumerate(qs):b.text(q+' = …',23+(i%3)*56,top+15+(i//3)*11,54,11.6)
            b.text('Réponses : '+answers,23,top+63,168,9.7,color=MUTED)
