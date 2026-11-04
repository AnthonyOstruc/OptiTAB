"""Situations suivies : six questions, calcul exact et démarche pour chacune."""
from fractions import Fraction as F
from config import GRADE
from modele_site import q, ex, m, n

NOMS=['Lina','Noé','Mila','Adam','Inès','Sami','Lou']
OBJETS=['livres','cartes','perles','images','jetons','graines','briques']

def f(v): return m(n(v))
def frac(a,b): return m(r'\frac{'+str(a)+'}{'+str(b)+'}')
def lit(v): return str(v).replace('.',',')
def nombre_lettres(v):
    """Orthographe rectifiée ; utilisé seulement pour les entiers positifs."""
    petits=['zéro','un','deux','trois','quatre','cinq','six','sept','huit','neuf','dix','onze','douze','treize','quatorze','quinze','seize']
    def bas(x):
        if x<17:return petits[x]
        if x<20:return 'dix-'+petits[x-10]
        if x<70:
            d,u=divmod(x,10);s=['','','vingt','trente','quarante','cinquante','soixante'][d]
            return s+('-et-un' if u==1 else '-'+petits[u] if u else '')
        if x<80:return 'soixante-'+('et-onze' if x==71 else bas(x-60))
        if x==80:return 'quatre-vingts'
        return 'quatre-vingt-'+bas(x-80)
    def groupe(x,terminal=True):
        if x<100:return 'quatre-vingt' if x==80 and not terminal else bas(x)
        c,r=divmod(x,100);s=('' if c==1 else bas(c)+'-')+'cent'
        if not r:return s+('s' if c>1 and terminal else '')
        return s+'-'+bas(r)
    if v<1000:return groupe(v)
    out=[]
    for unit,label in [(1000000,'million'),(1000,'mille')]:
        k,v=divmod(v,unit)
        if k:out.append(('' if k==1 and unit==1000 else groupe(k,unit!=1000)+'-')+label+('s' if unit==1000000 and k>1 else ''))
    if v:out.append(groupe(v))
    return '-'.join(out)

def a(text,method,result,control='',calc=''):
    return q(text,method,result,calc,control)
def c(text,method,expr,value,unit=''):
    assert eval(expr,{'F':F})==value,(text,expr,value)
    expected=f'F({value.numerator},{value.denominator})' if isinstance(value,F) else repr(value)
    tex=expr.replace('**', '^').replace('//',r'\div ').replace('*',r'\times ').replace(' ', '')
    # Les fractions Python servent aux contrôles ; leur écriture n'est jamais montrée.
    # // compte les groupes COMPLETS : ce n'est pas une égalité de division exacte.
    calcul='' if 'F(' in expr or '//' in expr else m(tex)+ ' = '+f(value)
    return q(text,method,f(value)+(' '+unit if unit else ''),calcul,f'({expr}) == {expected}')

def numeration(i,l):
    ce=GRADE.startswith('ce');cm2=GRADE=='cm2'
    v=(234+i*71+l*112) if GRADE=='ce1' else (2346+i*317+l*1021) if ce else (12405203+i*1123001+l*10040000) if cm2 else (23405+i*12301+l*101020)
    rank=10 if GRADE=='ce1' else 100 if ce else 1000
    digits=list(str(v));unit=10 if l==0 else 100
    low=(v//unit)*unit;high=low+unit
    title=['Le stock de la classe','Des étiquettes à vérifier','Le registre de la bibliothèque'][l]
    qs=[a(f'Écris {v} en lettres.','Je lis les classes et les rangs, de gauche à droite.',nombre_lettres(v)+'.'),
        a('Décompose ce nombre en milliers, centaines, dizaines et unités, selon les rangs présents.','Je donne à chaque chiffre la valeur de son rang.',' + '.join(f(int(d)*10**(len(digits)-j-1)) for j,d in enumerate(digits) if int(d))+'.',f'{v}=='+ '+'.join(str(int(d)*10**(len(digits)-j-1)) for j,d in enumerate(digits) if int(d))),
        c(f'Combien de paquets complets de {rank} contient ce stock ?','Je compte tous les paquets entiers ; ce nombre peut avoir plusieurs chiffres.',f'{v}//{rank}',v//rank,'paquets'),
        c(f'Combien d’objets restent hors de ces paquets de {rank} ?','Je retire la quantité contenue dans les paquets complets.',f'{v}-{v//rank}*{rank}',v%rank,'objets'),
        a(f'Encadre le stock entre deux multiples consécutifs de {unit}.','Je cherche le multiple inférieur ou égal au nombre, puis le suivant.',f'{f(low)} '+('≤' if low==v else '<')+f' {f(v)} < {f(high)}.',f'{low}<={v}<{high}'),
        c(f'On reçoit encore {unit} objets. Quel est le nouveau stock ?','J’ajoute le paquet reçu ; je surveille les changements de rang.',f'{v}+{unit}',v+unit,'objets')]
    return ex(title,f'Le registre indique {f(v)} objets. Aide {NOMS[i]} à écrire et à contrôler ce nombre.',qs,'Un chiffre indique un rang ; un nombre de paquets compte tous les paquets complets.',dict(type='place',number=v),True)

def comparer_nombres(i,l):
    v=231+i*61+l*103 if GRADE=='ce1' else 2341+i*307+l*1001
    step=10 if l==0 else 100
    values=[v+step,v-1,v+1,v]
    low=v//step*step; high=low+step
    return ex('Les relevés du compteur',f'Un compteur a affiché ces nombres dans le désordre : '+ ' ; '.join(f(x) for x in values)+'.',[
        a('Quel est le plus petit relevé ?','Je compare les chiffres de gauche à droite.',f(v-1),f'{v-1}==min({values})'),
        a('Range les quatre relevés dans l’ordre croissant.','Je commence par le plus petit puis je compare les nombres restants.',' < '.join(f(x) for x in sorted(values))),
        c(f'Quel est l’écart entre {v} et {v+step} ?','Je cherche ce qu’il faut ajouter au premier pour atteindre le second.',f'{v+step}-{v}',step),
        a(f'Encadre {v} entre deux multiples consécutifs de {step}.','Je repère les deux bornes entre lesquelles se trouve le nombre.',f'{f(low)} < {f(v)} < {f(high)}.' if low!=v else f'{f(low)} ≤ {f(v)} < {f(high)}.'),
        c(f'Quel nombre est situé juste après {v+step} ?','Sur la suite des entiers, j’avance d’une unité.',f'{v+step}+1',v+step+1),
        c(f'On avance de 3 graduations de {step} à partir de {v}. Où arrive-t-on ?','Je calcule la valeur des trois sauts, puis je l’ajoute au départ.',f'{v}+3*{step}',v+3*step)],
        'Je lis toujours la valeur d’un pas avant d’utiliser une graduation.',dict(type='numberline',start=v,step=step),True)

def addition(i,l,subtract=False,compensation=False):
    small=GRADE=='ce1'; a0=236+i*31+l*77 if small else 1246+i*213+l*1007
    b0=38+i*3 if compensation else 47+i*7+l*23 if small else 378+i*47+l*209
    if compensation:b0=[9,19,29,39,18,28,38][i]
    if subtract and a0<=b0:a0=b0+257
    sign='-' if subtract else '+'; total=a0-b0 if subtract else a0+b0
    delta=10 if small else 100
    intro=f'La réserve contient {f(a0)} {OBJETS[i]}. '+(f'On en distribue {f(b0)}.' if subtract else f'On reçoit {f(b0)} {OBJETS[i]} supplémentaires.')
    qs=[a('Quelle opération permet de trouver le nouveau stock ?','Je décide si la réserve augmente ou diminue.',m(f'{a0}{sign}{b0}')+'.'),
        c('Calcule le nouveau stock.','Je peux poser le calcul en alignant les rangs ; je commence par les unités.' if not compensation else 'Je passe par la dizaine voisine, puis je corrige l’écart.',f'{a0}{sign}{b0}',total,OBJETS[i]),
        c('Vérifie le résultat avec l’opération inverse.','Je refais le chemin en sens inverse pour retrouver le stock de départ.',f'{total}'+('+' if subtract else '-')+str(b0),a0,OBJETS[i]),
        c(f'On reçoit ensuite {delta} objets. Quel est le stock ?','J’utilise le résultat précédent et j’ajoute la nouvelle livraison.',f'{total}+{delta}',total+delta,OBJETS[i]),
        c(f'On réserve {10+i} objets pour un atelier. Combien restent disponibles ?','Réserver des objets diminue la quantité disponible.',f'{total+delta}-{10+i}',total+delta-10-i,OBJETS[i]),
        a(f'{NOMS[i]} annonce {total+delta-10-i+1} objets disponibles. Son résultat est-il correct ?','Je compare sa proposition au résultat calculé, puis je précise l’écart.',f'Non. Il y a {f(total+delta-10-i)} objets disponibles ; sa réponse contient un objet de trop.',f'{total+delta-10-i+1}-({total+delta-10-i})==1')]
    return ex('La réserve évolue',intro,qs,'Une addition réunit ou augmente ; une soustraction retire ou cherche un écart.',dict(type='partwhole',a=a0,b=b0,minus=subtract),True)

def multiplication(i,l,kind='normal'):
    if GRADE=='ce1':unit=11+i if kind=='decompose' else 3+i;count=2+l*2
    elif GRADE=='ce2':unit=24+i*3+l*11;count=3+l if kind!='two' else 12+i+l*3
    else:unit=124+i*27+l*103;count=4+l*7
    if kind=='tables':unit=3+i;count=2+l*3
    if kind=='ten':unit=12+i*3;count=10 if GRADE=='ce1' or l==0 else 100 if l==1 else 20
    if kind=='double':unit=12+i*3;count=4 if l==0 else 8
    total=unit*count
    part=(unit//10)*10 if unit>=10 else unit-1
    return ex('Préparer des lots identiques',f'Pour un atelier, {NOMS[i]} prépare {count} lots de {unit} {OBJETS[i]} chacun. Tous les lots sont identiques.',[
        a('Écris l’addition qui représente les lots.','Chaque lot apporte la même quantité. Je répète le même terme.', ' + '.join(f(unit) for _ in range(count)) if count<=8 else f'{count} termes tous égaux à {unit}.'),
        a('Quelle multiplication représente cette situation ?','Un facteur compte les lots, l’autre les objets dans un lot.',m(f'{count}'+r'\times'+str(unit))+'.'),
        c('Combien d’objets faut-il en tout ?','Je multiplie la quantité d’un lot par le nombre de lots.',f'{unit}*{count}',total,OBJETS[i]),
        c(f'Calcule aussi en séparant {unit} en {part} et {unit-part}.','Je multiplie les deux parties par le même nombre, puis je réunis les produits.',f'{part}*{count}+{unit-part}*{count}',total,OBJETS[i]),
        c('Un lot supplémentaire est demandé. Quel est le nouveau total ?','J’ajoute la quantité d’un seul lot au total précédent.',f'{total}+{unit}',total+unit,OBJETS[i]),
        c(f'On possède {total+unit+5+i} objets. Combien resteront après les {count+1} lots ?','Je retire la quantité nécessaire au stock disponible.',f'{total+unit+5+i}-{total+unit}',5+i,OBJETS[i])],
        'Je distingue le nombre de lots et la quantité dans chaque lot. Leur produit donne le total.',dict(type='groups',groups=count,size=unit),True)

def doubles(i,l):
    v=(25+i*5+l*10) if GRADE=='ce1' else (75+i*15+l*25)
    return ex('Deux équipes identiques',f'Une équipe reçoit {v} jetons. Une deuxième équipe doit recevoir exactement la même quantité.',[
        c('Combien de jetons faut-il pour les deux équipes ?','Le double, c’est deux fois la même quantité.',f'{v}*2',v*2,'jetons'),
        c('Si les deux équipes rendent leurs jetons, quelle est la moitié du total ?','Je partage le total en deux parts égales pour retrouver une équipe.',f'{2*v}//2',v,'jetons'),
        c('Chaque équipe reçoit 5 jetons supplémentaires. Quel est le nouveau total ?','Deux équipes gagnent chacune 5 jetons : le total augmente de 10.',f'{2*v}+2*5',2*v+10,'jetons'),
        c('Les jetons sont répartis entre deux équipes égales. Combien chacune reçoit-elle maintenant ?','Je prends la moitié du nouveau total.',f'{2*v+10}//2',v+5,'jetons'),
        c('Deux autres équipes identiques rejoignent les deux premières. Combien faut-il de jetons ?','Je double encore le total des deux équipes.',f'{2*v+10}*2',4*v+20,'jetons'),
        a('Pourquoi doubler puis prendre la moitié redonne-t-il le départ ?','Je décris ce que font les deux actions successives.','Doubler réunit deux parts égales ; prendre la moitié permet de retrouver une seule de ces parts.')],
        'Le double et la moitié font le chemin dans les deux sens.',dict(type='groups',groups=2,size=v),True)

def division(i,l):
    d=3+i%6;quot=12+i*3+l*11 if GRADE.startswith('cm') else 3+i+l*2
    rest=(i+l)%d;total=d*quot+rest
    return ex('Ranger toute la collection',f'La classe possède {total} {OBJETS[i]}. Une boîte contient au maximum {d} objets. On remplit d’abord les boîtes entièrement.',[
        a('Quel calcul cherche le nombre de boîtes complètes ?','Je cherche combien de groupes de même taille sont contenus dans le total.',f'Partager {total} en groupes de {d}'+(' ; '+m(f'{total}'+r'\div'+str(d))+'.' if GRADE!='ce1' else '.')),
        c('Combien de boîtes complètes peut-on remplir ?','J’utilise les multiples du nombre d’objets par boîte ; le dernier ne doit pas dépasser le stock.',f'{total}//{d}',quot,'boîtes'),
        c('Combien d’objets restent hors des boîtes complètes ?','Je retire les objets déjà rangés dans les boîtes pleines.',f'{total}-{quot}*{d}',rest,'objets'),
        c('Vérifie en reconstituant toute la collection.','Je compte les objets rangés puis j’ajoute ceux qui restent.',f'{quot}*{d}+{rest}',total,'objets'),
        a('Combien de boîtes faut-il pour transporter TOUS les objets ?','S’il reste des objets, il faut une boîte de plus, même si elle n’est pas pleine.',f(quot+(rest>0))+' boîtes.',f'{quot+(rest>0)}==({total}+{d}-1)//{d}'),
        c('Combien d’objets faudrait-il ajouter pour remplir une boîte de plus que le nombre de boîtes déjà complètes ?','Je compare le total actuel à la capacité de la boîte complète suivante.',f'{quot+1}*{d}-{total}',d-rest,'objets')],
        'Je lis la question : boîtes pleines et boîtes nécessaires pour tout transporter ne répondent pas à la même demande.',dict(type='groups',groups=quot,size=d,remainder=rest),True)

def multiples(i,l):
    d=3+i; k=5+l*3;total=d*k
    return ex('Des rangées régulières',f'Une salle contient {k} rangées de {d} chaises chacune. On veut tester plusieurs organisations.',[
        a(f'Écris les cinq premiers multiples non nuls de {d}.','Je compte de la même quantité en partant de zéro.', ' ; '.join(f(d*j) for j in range(1,6))+'.'),
        c('Combien de chaises la salle contient-elle ?','Chaque rangée apporte autant de chaises.',f'{d}*{k}',total,'chaises'),
        a(f'{total} est-il un multiple de {d} ?','Un produit donne une preuve : je cite les deux facteurs.',f'Oui : {k} rangées de {d} donnent {total}.',f'{total}%{d}==0'),
        a(f'Peut-on faire des rangées complètes de {d} avec une chaise de plus ?','Je teste le partage et j’interprète le reste.',f'Non : après {k} rangées complètes, il resterait 1 chaise.',f'({total}+1)%{d}==1'),
        c(f'Combien manque-t-il de chaises pour obtenir {k+2} rangées ?','Je compare la capacité voulue au total actuel.',f'{d}*{k+2}-{total}',2*d,'chaises'),
        a(f'Le nombre {total} a-t-il {k} comme diviseur ? Justifie.','Je relis le produit dans l’autre sens.',f'Oui : {total} = {k} × {d}. On peut former {d} rangées de {k} chaises.',f'{total}%{k}==0')],
        'Un produit exact donne à la fois des multiples et des diviseurs.',dict(type='groups',groups=k,size=d),True)

def regularites(i,l):
    start=4+i; add=2+l; mult=2+l; end=(start+add)*mult
    return ex('Une machine à calculer',f'La machine ajoute {add}, puis multiplie le résultat par {mult}. {NOMS[i]} y entre {start}.',[
        c('Quel nombre obtient-on après la première instruction ?','Je traite uniquement l’ajout, sans anticiper l’étape suivante.',f'{start}+{add}',start+add),
        c('Quel nombre sort de la machine ?','Je multiplie le résultat de la première étape.',f'{start+add}*{mult}',end),
        c(f'Quel nombre sort si on entre {start+1} ?','Je recommence les deux étapes dans le même ordre.',f'({start+1}+{add})*{mult}',end+mult),
        c('De combien la sortie a-t-elle augmenté quand l’entrée a augmenté de 1 ?','Je compare les deux sorties ; le second calcul multiplie l’unité supplémentaire.',f'{end+mult}-{end}',mult),
        c(f'Une sortie vaut {end+2*mult}. Quel nombre a été entré ?','Je défais les étapes en sens inverse : partager, puis enlever l’ajout.',f'{end+2*mult}//{mult}-{add}',start+2),
        a('Complète les quatre premières sorties pour quatre entrées consécutives à partir du départ.','J’ajoute à chaque fois le même écart à la sortie précédente.',' ; '.join(f(end+j*mult) for j in range(4))+'.')],
        'L’ordre des instructions compte. Pour revenir en arrière, je défais les opérations dans l’ordre inverse.',dict(type='program',lines=[f'Entrée : {start}',f'Ajouter {add}',f'Multiplier par {mult}'],answer=end),True)

def fractions(i,l,kind='read'):
    ce1=GRADE=='ce1';d=([2,3,4,5,6,8,10][i] if ce1 else [4,6,8,10,12,6,8][i] if GRADE=='ce2' else [4,6,8,10,12,15,20][i] if GRADE=='cm1' else [6,8,12,15,20,30,60][i])
    a0=max(1,d//2-1); b0=1 if l==0 else max(1,min(2,d-a0-1)); used=a0+b0
    if kind=='compare':a0=max(1,d//2);b0=max(1,a0-1);used=a0
    intro=f'Une bande unité est partagée en {d} parts égales. {NOMS[i]} colorie {a0} parts en bleu.'
    qs=[a('Quel est le dénominateur ? Que signifie-t-il ?','Je compte toutes les parts égales qui composent l’unité.',f'{d} : l’unité est partagée en {d} parts égales.'),
        a('Écris la fraction coloriée.','Le numérateur compte les parts colorées ; le dénominateur garde le partage.',frac(a0,d)+'.'),
        a('Quelle fraction de la bande est encore blanche ?','Je retire les parts colorées du nombre total de parts.',frac(d-a0,d)+'.',f'{d}-{a0}=={d-a0}')]
    if kind=='compare':
        qs += [a(f'Une deuxième bande identique a {b0} parts coloriées sur {d}. Laquelle a la plus grande fraction coloriée ?','Le partage est identique : je compare les nombres de parts.',f'La première : {frac(a0,d)} > {frac(b0,d)}.',f'F({a0},{d})>F({b0},{d})'),
            a('Combien de parts faudrait-il colorier en plus sur la deuxième pour égaler la première ?','Je cherche l’écart entre les nombres de parts.',f(a0-b0)+' part(s).',f'{a0}-{b0}=={a0-b0}'),
            a(f'Pour le même tout, une part sur {d} est-elle plus petite qu’une part sur {max(1,d//2)} ?','Davantage de parts égales dans le même tout donne des parts plus petites.',f'Oui : {frac(1,d)} < {frac(1,max(1,d//2))}.',f'F(1,{d})<F(1,{max(1,d//2)})')]
    elif kind=='equal':
        # Choisir un partage qui peut être doublé sans sortir des douzièmes.
        return fractions_egales(i,l)
    else:
        qs += [a(f'On colorie {b0} part(s) blanche(s) en vert. Quelle fraction est maintenant coloriée en tout ?','Je réunis les parts colorées ; leur taille reste la même.',frac(used,d)+'.',f'F({a0},{d})+F({b0},{d})==F({used},{d})'),
            a('Quelle fraction manque maintenant pour colorier toute la bande ?','Je compare le nombre de parts colorées au nombre de parts de l’unité.',frac(d-used,d)+'.',f'1-F({used},{d})==F({d-used},{d})'),
            a('On efface uniquement le vert. Quelle fraction reste coloriée ?','Je retire les parts ajoutées et je retrouve la situation initiale.',frac(a0,d)+'.',f'F({used},{d})-F({b0},{d})==F({a0},{d})')]
    return ex('Une bande à partager',intro,qs,'Le partage doit être équitable. Quand la taille des parts ne change pas, je garde le dénominateur.',dict(type='fraction',denominator=d,numerator=a0,added=b0 if kind!='compare' else 0),True)

def fractions_egales(i,l):
    d=[2,3,4,6,2,3,4][i];a0=1 if l==0 else d-1
    return ex('Deux découpages du même tout',f'Une bande est partagée en {d} parts égales ; {a0} part(s) sont colorées. On partage ensuite CHAQUE part en deux.',[
        a('Quelle fraction est coloriée au départ ?','Je compte les parts prises parmi toutes les parts égales.',frac(a0,d)+'.'),
        c('Combien de petites parts l’unité contient-elle après le nouveau découpage ?','Chaque ancienne part donne deux petites parts.',f'{d}*2',2*d,'parts'),
        c('Combien de petites parts colorées obtient-on ?','Les parties colorées sont elles aussi partagées en deux.',f'{a0}*2',2*a0,'parts'),
        a('Écris la nouvelle fraction de surface coloriée.','J’utilise le nombre de petites parts colorées et le total de petites parts.',frac(2*a0,2*d)+'.'),
        a('La surface coloriée a-t-elle changé ? Écris une égalité de fractions.','Découper plus finement ne retire ni n’ajoute de surface.',f'Non : {frac(a0,d)} = {frac(2*a0,2*d)}.',f'F({a0},{d})==F({2*a0},{2*d})'),
        a('Quelle fraction du tout reste blanche, avec le nouveau découpage ?','Je compte les petites parts non colorées.',frac(2*(d-a0),2*d)+'.',f'1-F({2*a0},{2*d})==F({2*(d-a0)},{2*d})')],
        'Des écritures différentes peuvent représenter la même quantité d’un même tout.',dict(type='fraction',denominator=d,numerator=a0,split=True),True)

def fraction_quantite(i,l):
    d=3+i%5;part=6+i*2+l*5;total=d*part;take=1 if l==0 else d-1
    return ex('Partager puis choisir des parts',f'La classe répartit {total} graines en {d} parts égales. Elle utilise {take} part(s) pour un potager.',[
        a('Quelle fraction du stock utilise-t-elle ?','Je compte les parts utilisées sur le nombre total de parts égales.',frac(take,d)+'.'),
        c('Combien de graines contient une part ?','Je partage la quantité totale en parts égales.',f'{total}//{d}',part,'graines'),
        c('Combien de graines sont utilisées ?','Je multiplie la quantité d’une part par le nombre de parts choisies.',f'{part}*{take}',part*take,'graines'),
        c('Combien de graines restent dans la réserve ?','Je retire les graines utilisées du stock initial.',f'{total}-{part*take}',total-part*take,'graines'),
        a('Quelle fraction du stock initial représente la réserve ?','Je compte les parts non utilisées.',frac(d-take,d)+'.'),
        c('Deux classes réalisent exactement le même projet. Combien utilisent-elles de graines ensemble ?','Je double la quantité utilisée par une classe.',f'{part*take}*2',2*part*take,'graines')],
        'Prendre une fraction d’une quantité : partager selon le dénominateur, puis choisir le nombre de parts indiqué.',dict(type='fraction',denominator=d,numerator=take,total=total),True)

def decimaux(i,l,kind='read'):
    scale=1000 if GRADE=='cm2' else 100;v=F(3*scale+125+i*17+l*203,scale);step=F(1,10 if l==0 else scale)
    floor=v.numerator//v.denominator;digits=scale*(v-floor)
    qs=[a('Écris le relevé sous la forme d’une fraction décimale.','Je compte les chiffres après la virgule pour choisir 100 ou 1 000.',frac(int(v*scale),scale)+'.',f'F({int(v*scale)},{scale})==F({v.numerator},{v.denominator})'),
        a('Quelle est sa partie entière ?','La partie entière compte les unités complètes avant la virgule.',f(floor)+'.'),
        a('Décompose le relevé en un entier et une fraction inférieure à 1.','Je sépare les unités entières et le reste de l’unité.',f'{f(floor)} + {frac(int(digits),scale)}.',f'{floor}+F({int(digits)},{scale})==F({v.numerator},{v.denominator})'),
        a('Encadre ce relevé entre deux entiers consécutifs.','Je garde les unités complètes puis je prends l’entier suivant.',f'{f(floor)} < {f(v)} < {f(floor+1)}.'),
        c(f'Le relevé augmente de {f(step)}. Quel nombre obtient-on ?','Je repère le rang de l’augmentation et j’additionne dans les mêmes unités.',f'F({v.numerator},{v.denominator})+F({step.numerator},{step.denominator})',v+step),
        a(f'Compare ce nouveau relevé avec {f(v)}. Justifie.','L’augmentation est positive : le nouveau relevé est plus grand.',f'{f(v+step)} > {f(v)}.',f'F({(v+step).numerator},{(v+step).denominator})>F({v.numerator},{v.denominator})')]
    return ex('Un relevé précis',f'Un instrument affiche {f(v)} unités. On veut interpréter cette écriture sans confondre dixièmes, centièmes et millièmes.',qs,
        'La position d’un chiffre détermine sa valeur ; un zéro final après la virgule ne change pas le nombre.',dict(type='decimal',value=lit(float(v)),denominator=scale),True)

def calculs_decimaux(i,l):
    u=F(235+i*17+l*101,100);v=F(147+i*9,100);budget=10+l*5
    return ex('Les achats de l’atelier',f'Un carnet coûte {f(u)} €. Un crayon coûte {f(v)} €. {NOMS[i]} dispose de {budget} €.',[
        c('Quel est le prix d’un carnet et d’un crayon ?','J’aligne les virgules pour réunir les euros avec les euros et les centimes avec les centimes.',f'F({u.numerator},{u.denominator})+F({v.numerator},{v.denominator})',u+v,'€'),
        c('Combien reste-t-il après cet achat ?','J’écris le budget avec des centimes puis je soustrais le montant payé.',f'{budget}-F({(u+v).numerator},{(u+v).denominator})',budget-u-v,'€'),
        c('Combien coûtent deux carnets ?','Je peux doubler le prix ou le multiplier par 2.',f'F({u.numerator},{u.denominator})*2',2*u,'€'),
        c('Quel est l’écart de prix entre le carnet et le crayon ?','Je soustrais le plus petit prix au plus grand.',f'F({u.numerator},{u.denominator})-F({v.numerator},{v.denominator})',u-v,'€'),
        c('Un ami achète le même duo. Combien coûtent les deux duos ?','Je double le prix du duo complet, sans oublier le crayon.',f'F({(u+v).numerator},{(u+v).denominator})*2',2*(u+v),'€'),
        a(f'{NOMS[i]} affirme que {f(u)} et {m(n(u)+"0")} désignent le même prix. A-t-on le droit d’ajouter ce zéro final ?','Je distingue un zéro final après la virgule d’un zéro placé au milieu du nombre.','Oui : ajouter un zéro tout à droite après la virgule ne change pas la valeur du prix.')],
        'Je garde les rangs alignés et je vérifie le prix avec les centimes.',dict(type='prices',labels=['Carnet','Crayon'],values=[lit(float(u)),lit(float(v))]),True)

def fraction_nombre(i,l):
    d=4+i%5;whole=1+l;reste=1+i%(d-1);num=whole*d+reste
    return ex('Une fraction sur la ligne',f'L’unité de la demi-droite est partagée en {d} parts égales. Le point A se trouve à {num} petits pas après zéro.',[
        a('Quelle fraction représente un petit pas ?','Je regarde en combien de parts égales l’unité a été partagée.',frac(1,d)+'.'),
        a('Quelle fraction repère A ?','Chaque pas ajoute une part ; je compte tous les pas depuis zéro.',frac(num,d)+'.'),
        c('Combien d’unités entières a-t-on dépassées ?','Je compte les groupes complets de parts qui font une unité.',f'{num}//{d}',whole,'unités'),
        a('Décompose cette fraction en un entier et une fraction inférieure à 1.','Je sépare les unités complètes et les pas restants.',f'{f(whole)} + {frac(reste,d)}.',f'F({num},{d})=={whole}+F({reste},{d})'),
        a('Entre quels entiers consécutifs se trouve A ?','Les unités entières donnent la borne inférieure ; l’unité suivante donne la borne supérieure.',f'{f(whole)} < {frac(num,d)} < {f(whole+1)}.',f'{whole}<F({num},{d})<{whole+1}'),
        a('Quelle fraction repère le point situé un petit pas après A ?','J’ajoute une part du même partage, sans changer la taille des pas.',frac(num+1,d)+'.',f'F({num},{d})+F(1,{d})==F({num+1},{d})')],
        'Une fraction est aussi un nombre ; elle peut dépasser une unité.',dict(type='fractionline',denominator=d,numerator=num),True)

def division_decimale(i,l):
    d=2+i%4;v=F((12+i*3+l*5)*d,10);share=v/d
    return ex('Partager une longueur précisément',f'Un ruban de {f(v)} m doit être partagé en {d} morceaux de même longueur, sans perte.',[
        a('Quelle opération cherche la longueur d’un morceau ?','Le nombre de morceaux est connu ; je partage la longueur totale.',f'{f(v)} divisé par {d}.'),
        c('Combien de décimètres mesure tout le ruban ?','Un mètre vaut dix décimètres ; cela permet ici de travailler avec un entier.',f'F({v.numerator},{v.denominator})*10',int(v*10),'dm'),
        c('Combien de décimètres mesure un morceau ?','Je partage les décimètres en parts égales.',f'{int(v*10)}//{d}',int(share*10),'dm'),
        a('Exprime la longueur d’un morceau en mètres.','Dix décimètres forment un mètre : un décimètre vaut un dixième de mètre.',f(share)+' m.',f'F({int(share*10)},10)==F({share.numerator},{share.denominator})'),
        c('Vérifie en réunissant les morceaux.','Le produit du nombre de morceaux par leur longueur doit retrouver tout le ruban.',f'F({share.numerator},{share.denominator})*{d}',v,'m'),
        c('On fabrique deux rubans identiques avant de les partager. Quelle longueur totale de ruban faut-il ?','Je double la longueur initiale, pas le nombre de mètres d’un seul morceau.',f'F({v.numerator},{v.denominator})*2',2*v,'m')],
        'Partager un décimal par un entier garde le sens du partage ; je peux changer d’unité pour comprendre les chiffres du quotient.',dict(type='measure',kind='length',initial=lit(float(v))+' m',used=str(d)+' morceaux',answer=lit(float(share))+' m chacun'),True)

def comparer_decimaux(i,l):
    a0=F(345+i*101+l*20,100);b0=a0+F(5,100);base=a0.numerator//a0.denominator
    nearest=F((int(a0*100)+5)//10,10)
    return ex('Comparer des résultats précis',f'Deux relevés sont {f(a0)} et {f(b0)}. Ils sont exprimés dans la même unité.',[
        a('Quelle partie entière ont-ils en commun ?','Je lis les unités complètes avant la virgule.',f(base)+'.'),
        a('Quel relevé est le plus grand ? Justifie avec les centièmes.','Je compare des parts de même taille, après avoir comparé les parties entières.',f'{f(b0)} > {f(a0)}.',f'F({b0.numerator},{b0.denominator})>F({a0.numerator},{a0.denominator})'),
        c('Quel est l’écart entre les deux relevés ?','Je soustrais le plus petit du plus grand.',f'F({b0.numerator},{b0.denominator})-F({a0.numerator},{a0.denominator})',F(5,100)),
        a('Encadre le premier relevé entre deux dixièmes consécutifs.','Je cherche le dixième juste avant puis le suivant.',f'{f(F(int(a0*10),10))} ≤ {f(a0)} < {f(F(int(a0*10)+1,10))}.'),
        a('Quel est son arrondi au dixième le plus proche ?','Je compare les distances aux deux dixièmes voisins ; à égale distance, je retiens le plus grand.',f(nearest)+'.'),
        a('Ajouter un zéro final à ces relevés change-t-il leur ordre ?','Un zéro final après la virgule ne change aucune valeur.','Non. Les nombres et leur ordre restent identiques.')],
        'Pour comparer des décimaux, je compare des rangs de même valeur et non le nombre de chiffres après la virgule.',dict(type='decimal',value=lit(float(a0)),denominator=100),True)
