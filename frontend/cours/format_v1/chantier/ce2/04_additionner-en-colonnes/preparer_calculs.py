# -*- coding: utf-8 -*-
"""Préparation reproductible des onze chapitres de calcul attribués (04–14).
Les sources sont lues seulement. Aucune base ni compilation n'est appelée.
"""
from pathlib import Path
import json,re,ast

ROOT=Path(__file__).resolve().parent.parent
MARK='<!-- optitab:1 -->'
PROGRAMME='https://www.education.gouv.fr/sites/default/files/document/Annexe%204%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20du%20cycle%202-403821.pdf'
def n(v): return f'{v:,}'.replace(',',r'\,')
def tex(s):
    s=re.sub(r'\d+',lambda m:n(int(m[0])),str(s))
    return s.replace('//',r'\div ').replace('*',r'\times ')
def formula(expr): return '$'+tex(expr)+'$'
def eq(expr): return formula(expr+' = '+str(eval(expr,{'__builtins__':{}})))
def display(expr): return '$$\n'+tex(expr+' = '+str(eval(expr,{'__builtins__':{}})))+'\n$$'
def box(typ,title,body): return f'::: {typ}'+(' '+title if title else '')+'\n'+body+'\n:::'
def task(prompt,method,work,result):return dict(prompt=prompt,method=method,work=work,result=result)

def add_work(values):
    carry=0;lines=[]
    names=['unités','dizaines','centaines','milliers','dizaines de milliers']
    for k in range(max(len(str(v)) for v in values)):
        ds=[v//10**k%10 for v in values];expr='+'.join(map(str,ds))+('+'+str(carry) if carry else '')
        total=sum(ds)+carry
        lines.append(f'Pour les {names[k]}, je calcule {eq(expr)}.')
        if k<max(len(str(v)) for v in values)-1:
            lines.append(f"J'écris {total%10} et je reporte {total//10} au rang suivant." if total>=10 else f"J'écris {total} ; il n'y a pas de retenue.")
        carry=total//10
    lines.append(display('+'.join(map(str,values))))
    return '\n\n'.join(lines)

def sub_work(a,b):
    width=max(len(str(a)),len(str(b)));ds=[a//10**i%10 for i in range(width)];lines=[]
    names=['unités','dizaines','centaines','milliers','dizaines de milliers']
    for i in range(width):
        digit=b//10**i%10
        if ds[i]<digit:
            j=i+1
            while ds[j]==0:j+=1
            ds[j]-=1
            for k in range(j-1,i,-1):ds[k]=9
            ds[i]+=10
            lines.append(f"Pour les {names[i]}, il n'y en a pas assez. J'échange une unité d'un rang supérieur, en passant par les rangs vides si besoin. J'ai alors {ds[i]} {names[i]} disponibles.")
        lines.append(f'Au rang des {names[i]}, {eq(str(ds[i])+"-"+str(digit))}.')
        ds[i]-=digit
    lines.append(display(f'{a}-{b}'))
    return '\n\n'.join(lines)

def mul_work(a,b,code):
    if 0 in (a,b):return 'Un produit avec un facteur zéro vaut zéro : il n’y a aucun objet à compter.\n\n'+display(f'{a}*{b}')
    if 1 in (a,b):return 'Un seul groupe garde la quantité de ce groupe.\n\n'+display(f'{a}*{b}')
    if code==11:
        # Le facteur 4 ou 8 peut être écrit à gauche dans la source.
        if a in (4,8) and b not in (4,8):a,b=b,a
        if b in (4,8):
            steps=2 if b==4 else 3;cur=a;lines=[]
            for _ in range(steps):lines.append('Je double : '+eq(f'{cur}+{cur}')+'.');cur*=2
            return '\n\n'.join(lines)+'\n\n'+display(f'{a}*{b}')
    if code in (12,13):
        lines=[]
        for k in range(len(str(b))):
            digit=b//10**k%10;carry=0
            lines.append('Je multiplie par '+('les unités' if k==0 else 'les dizaines')+f' du second facteur : {formula(str(digit*10**k))}.')
            for j,c in enumerate(reversed(str(a))):
                x=int(c);v=x*digit+carry;expr=f'{x}*{digit}'+(f'+{carry}' if carry else '')
                lines.append(eq(expr)+'. '+(f"J'écris {v%10} et je retiens {v//10}." if j<len(str(a))-1 else f"J'écris {v} à gauche des chiffres déjà trouvés."))
                carry=v//10
            lines.append('Cette ligne représente '+eq(f'{a}*{digit*10**k}')+'.')
        if b>=10:lines.append('Je réunis les deux lignes : '+eq(f'{a*(b%10)}+{a*(b//10)*10}')+'.')
        return '\n\n'.join(lines)+'\n\n'+display(f'{a}*{b}')
    if code==9:
        if b in (10,100):return f"Chaque chiffre prend une valeur {b} fois plus grande. Les rangs devenus vides sont écrits avec des zéros.\n\n"+display(f'{a}*{b}')
        if b%10==0:return 'Je compte les dizaines : '+eq(f'{a}*{b//10}')+'.\n\nCe nombre de dizaines vaut '+eq(f'{a*(b//10)}*10')+'.'
    if a<10 and b>=10:a,b=b,a
    high=a//10*10;low=a%10
    if high==0:return 'Je retrouve le résultat dans la table de multiplication.\n\n'+display(f'{a}*{b}')
    return f'Je sépare {formula(str(a))} en {formula(str(high))} et {formula(str(low))}.\n\n'+eq(f'{high}*{b}')+' ; '+eq(f'{low}*{b}')+'.\n\nJe réunis les deux produits : '+eq(f'{high*b}+{low*b}')+'.\n\n'+display(f'{a}*{b}')

def arithmetic_work(expr,code):
    if code==14 and expr=='35//8+1':
        return 'Je remplis quatre pages : '+eq('4*8')+'. Il reste '+eq('35-32')+'.\n\nCes trois photos occupent une page supplémentaire : '+eq('4+1')+'.'
    if code==6 and re.fullmatch(r'\d+\+\d+',expr):
        a,b=map(int,expr.split('+'));near=(b+9)//10*10;diff=near-b
        return 'Je passe par la dizaine suivante, puis j’enlève ce que j’ai ajouté en trop.\n\n'+eq(f'{a}+{near}')+' ; '+eq(f'{a+near}-{diff}')+'.\n\n'+display(expr)
    tree=ast.parse(expr,mode='eval').body
    if isinstance(tree,ast.BinOp) and isinstance(tree.op,ast.Add) and all(isinstance(x,(ast.Constant,ast.BinOp)) for x in [tree.left,tree.right]) and '*' not in expr and '/' not in expr:
        return add_work(list(map(int,expr.split('+'))))
    if re.fullmatch(r'\d+-\d+',expr):
        a,b=map(int,expr.split('-'))
        if code==6:
            near=(b+9)//10*10;diff=near-b
            return f'Je retire la dizaine suivante, puis je rends ce que j’ai retiré en trop.\n\n'+eq(f'{a}-{near}')+' ; '+eq(f'{a-near}+{diff}')+'.\n\n'+display(expr)
        return sub_work(a,b)
    if re.fullmatch(r'\d+\*\d+',expr):return mul_work(*map(int,expr.split('*')),code)
    if re.fullmatch(r'\d+//\d+',expr):
        a,b=map(int,expr.split('//'));q,r=divmod(a,b)
        if code==8 and b==2:
            high=a//100*100 if a>=100 else a//10*10;low=a-high
            parts=[v for v in (high,low) if v]
            return 'Je cherche deux parts égales. Je sépare le nombre en morceaux faciles à partager.\n\n'+'\n\n'.join(f'La moitié de {part} est {part//2}, car '+eq(f'2*{part//2}')+'.' for part in parts)+'\n\nJe réunis ces moitiés : '+eq('+'.join(str(v//2) for v in parts))+f'.\n\nLa moitié de {a} est {q}.'
        detail=''
        if q>=10:
            parts=[int(c)*10**i for i,c in enumerate(reversed(str(q))) if c!='0'][::-1]
            detail='Je construis le partage par morceaux :\n\n'+' ; '.join(eq(f'{b}*{part}') for part in parts)+'.\n\nJe réunis les parts obtenues : '+eq('+'.join(map(str,parts)))+'.\n\n'
        return 'Je cherche combien de groupes complets je peux faire.\n\n'+detail+eq(f'{b}*{q}')+'.\n\n'+(f'Il reste {r} objet'+('s' if r!=1 else '')+'.\n\n'+eq(f'{b}*{q}+{r}')+'.' if r else display(expr))
    if re.fullmatch(r'\d+\*\d+\+\d+',expr):
        product,rest=expr.split('+');p=eval(product)
        return 'Je compte d’abord les objets dans les groupes : '+eq(product)+'.\n\nJ’ajoute ensuite le reste : '+eq(f'{p}+{rest}')+'.\n\n'+display(expr)
    return 'Je calcule dans l’ordre indiqué.\n\n'+display(expr)

def numeric_task(expr,code,prompt=None):
    methods={4:'J’aligne les unités et je commence à droite ; j’échange dix unités d’un rang contre une du rang suivant.',5:'J’aligne les rangs ; si un rang ne suffit pas, je fais un échange avant de retirer.',6:'Je passe par la dizaine suivante et je corrige ce détour dans le sens opposé.',7:'Je retrouve le produit dans une table ou je m’appuie sur un produit connu.',8:'Je m’appuie sur deux parts égales pour retrouver un double ou une moitié.',9:'Je compte des dizaines ou des centaines et je respecte la valeur des rangs.',10:'Je sépare un facteur en deux parties, je multiplie les deux parties puis je réunis.',11:'Je double deux fois pour quatre groupes, trois fois pour huit groupes.',12:'Je multiplie de droite à gauche ; j’ajoute chaque retenue au produit du rang suivant.',13:'Je multiplie par les unités puis par les dizaines ; j’additionne les deux lignes.',14:'Je cherche le produit qui reconstitue le total et je précise le rôle du reste.'}
    return task(prompt or 'Calcule '+formula(expr)+'.',methods[code],arithmetic_work(expr,code),eq(expr)+'.')

FALLBACK={7:{4:'6*3',6:'9*4',8:'2*24'},8:{4:'3*25',6:'6*10'},9:{1:'427*10',9:'305*10'}}
TITLES={
4:['Aligner les termes','Échanger dans plusieurs rangs','Aligner des nombres de tailles différentes','Réunir trois nombres','Atteindre un millier entier','Choisir le calcul mental','Réunir les bibliothèques','Totaliser une collecte','Corriger un alignement'],
5:['Soustraire sans échange','Échanger les unités','Traverser un zéro','Partir de milliers entiers','Aligner un nombre court','Choisir une méthode courte','Compter les enveloppes restantes','Trouver la distance restante','Vérifier une réponse proposée'],
6:['Lire le détour','Ajouter presque une dizaine','Ajouter une dizaine moins un','Retirer une dizaine moins un','Choisir le bon détour','Retrouver un nombre manquant','Recevoir de nouveaux livres','Diminuer un stock','Corriger le sens de compensation'],
7:['Lire un rectangle','Utiliser les tables','Retrouver un facteur','Reconnaître des multiples','Multiplier par zéro, un ou dix','Nommer facteurs et produit','Compter les pommes','Reconnaître pair et impair','Ajouter un groupe entier'],
8:['Calculer des doubles','Calculer des moitiés','Doubler des centaines','Les repères de vingt-cinq','Compléter un produit égal à soixante','Chercher toutes les paires','Réunir deux collectes égales','Partager des feuilles en deux','Vérifier une moitié'],
9:['Comprendre le changement de rang','Multiplier par dix','Multiplier par cent','Multiplier des dizaines','Trouver un facteur manquant','S’appuyer sur les tables','Compter les trombones','Distribuer des feuilles','Expliquer le rôle du zéro'],
10:['Partager un rectangle','Séparer dizaines et unités','Additionner deux produits','Compléter une décomposition','Utiliser un nombre voisin','Choisir sa méthode','Compter les crayons','Compter les places','Multiplier chaque partie'],
11:['Lire deux doubles','Multiplier par quatre','Multiplier par huit','Compléter deux doubles','Doubler de grands nombres','Choisir un calcul rapide','Réunir quatre classes','Peser huit paquets','Compter les groupes doublés'],
12:['Poser sans retenue','Garder la retenue','Passer aux milliers','Garder le rang vide','Obtenir des milliers entiers','Vérifier par décomposition','Compter des étiquettes','Distribuer aux classes','Ajouter la retenue au bon moment'],
13:['Comprendre les deux lignes','Multiplier les dizaines','Poser avec trois chiffres','Conserver les rangs vides','Calculer un grand produit','Multiplier par trente','Compter les sièges','Compter les feuilles reçues','Donner sa valeur à une dizaine'],
14:['Relier produit et divisions','Diviser avec les tables','Partager équitablement','Former des boîtes complètes','Interpréter un reste','Prévoir une page supplémentaire','Fabriquer des bracelets','Partager une somme en centimes','Terminer un groupement']}

def core_task(src,code,index):
    checks=src['check'].split(' and ') if src['check'] else []
    expressions=[]
    for c in checks:
        expr=c.split('==')[0]
        if '%' not in expr:expressions.append(expr)
    if not expressions:expressions=[FALLBACK[code][index]]
    # Une consigne avec une figure reçoit sa représentation dans l'énoncé.
    prompt=src['consigne']
    if src.get('figure'):prompt+='\n\n[IMAGE_1]'
    works=[arithmetic_work(x,code) for x in expressions]
    if not src['check']:
        works.append(src['reponse'])
    if code==7 and index==4:
        works=[f'Un multiple de 6 se retrouve dans sa table : {eq("6*3")}, {eq("6*5")} et {eq("6*7")}. Les nombres 25 et 49 ne sont pas dans cette table.']
    if code==7 and index==8:works.append('Un nombre est pair quand on peut le partager en groupes de deux sans reste. Le nombre 9 est impair et '+eq('3*3')+'.')
    if code==8 and index==6:works=['Je teste les petits facteurs et je retrouve les paires :\n\n'+'\n\n'.join(eq(f'{a}*{60//a}') for a in (1,2,3,4,5,6))+'.\n\nAprès 6, on retrouve les mêmes paires dans l’autre sens : la liste est complète.']
    if code==14 and index==6:works.append('Quatre pages pleines ne suffisent pas : les trois photos restantes prennent une cinquième page. La dernière page peut ne pas être pleine.')
    if code==14 and index==8:works.append('Je partage les centimes : chaque enfant reçoit 320 centimes. Cela fait 3 euros et 20 centimes, soit 3,20 €.')
    if code==14 and index==9:works.append('Un reste de 7 permet encore un groupe de 5. Je forme ce groupe : le reste devient 2, inférieur à 5. Le groupement est alors terminé.')
    if code==4 and index==9:works.insert(0,'Le 5 de 57 est un chiffre de dizaines : je le place sous le 8 des dizaines de 3 486. Le 7 des unités est sous le 6.')
    if code==5 and index==9:works.insert(0,'Je teste la réponse de Lina par l’addition. La somme 5 002 ne redonne pas 4 002 : sa réponse est fausse.')
    if code==6 and index==9:works.insert(0,'Retirer 30 enlève un de trop. Il faut rendre cette unité en ajoutant 1, et non en la retirant.')
    if code==7 and index==9:works.insert(0,'Passer de sept groupes à huit groupes demande un groupe entier de 7, et non une seule unité.')
    if code==8 and index==9:works.insert(0,'Le double de 50 vaut 100 : 50 ne peut donc pas être la moitié de 150.')
    if code==9 and index==9:works.insert(0,'Lina a raison : les 3 centaines deviennent 3 milliers et les 5 unités deviennent 5 dizaines. Le rang des unités devient vide.')
    if code==10 and index==9:works.insert(0,'Le nombre 32 est séparé en 30 et 2. Les deux parties doivent être multipliées par 4.')
    if code==11 and index==9:works.insert(0,'Doubler 23 puis ajouter 23 ne donne que trois groupes. Pour quatre groupes, je double le premier double.')
    if code==12 and index==9:works.insert(0,'La retenue 3 vient des 32 unités. Elle représente 3 dizaines et doit être ajoutée au produit des dizaines.')
    if code==13 and index==9:works.insert(0,'Le 1 du facteur 12 représente une dizaine. La seconde ligne vaut donc 340, et non 34.')
    primary=expressions[0]
    if code==5 and index==9:primary='4002-1678'
    if code==7 and index==9:primary='7*8'
    return task(prompt,'Je repère ce qui est demandé, puis j’applique la méthode du chapitre.','\n\n'.join(works),src['reponse']),primary

def companion_tasks(code,expr,index):
    # Quatre questions courtes prolongent l'objectif précis du calcul de départ.
    nums=list(map(int,re.findall(r'\d+',expr)));a=nums[0];b=nums[1] if len(nums)>1 else 2
    if code==4:
        total=eval(expr);terms=expr.split('+');first=int(terms[0]);rest=sum(map(int,terms[1:]))
        units='+'.join(str(int(v)%10) for v in terms)
        return [numeric_task(units,4,'Reprends seulement le rang des unités du calcul de départ : '+formula(units)+'.'),
        task('Décompose le résultat du calcul de départ en milliers, centaines, dizaines et unités.','Je lis la valeur de chaque chiffre.',f'Le nombre {formula(str(total))} contient {total//1000} milliers, {total//100%10} centaines, {total//10%10} dizaines et {total%10} unités.',eq(f'{total//1000}*1000+{total//100%10}*100+{total//10%10}*10+{total%10}')+'.'),
        numeric_task(f'{total}-{first}',5,'Vérifie en retirant le premier terme à la somme : '+formula(f'{total}-{first}')+'.'),
        numeric_task(f'{first}+{rest+10}',4,'Si l’on ajoute encore 10 objets au total de départ, quel total obtient-on ? Calcule '+formula(f'{first}+{rest+10}')+'.')]
    if code==5:
        diff=a-b
        return [numeric_task(f'{diff}+{b}',4,'Vérifie la soustraction principale par '+formula(f'{diff}+{b}')+'.'),
        task('Pourquoi faut-il parfois faire un échange avant de retirer les unités ?','Je compare les chiffres des unités.',f'Je dois retirer {b%10} unités et il y en a {a%10} au départ. '+('Il faut échanger une dizaine contre dix unités.' if a%10<b%10 else 'Ce rang a assez d’unités : aucun échange n’est nécessaire pour commencer.'),'Un échange change l’écriture des rangs, sans changer la quantité.'),
        numeric_task(f'{a}-{b-1}',5,'Que reste-t-il si l’on retire un objet de moins ? Calcule '+formula(f'{a}-{b-1}')+'.'),
        numeric_task(f'{diff}+1',4,'Compare les deux différences en calculant '+formula(f'{diff}+1')+'.')]
    if code==6:
        sign='-' if '-' in expr else '+';near=(b+9)//10*10;delta=near-b;mid=a-near if sign=='-' else a+near
        return [numeric_task(f'{a}{sign}{near}',6,'Calcule la première étape du détour : '+formula(f'{a}{sign}{near}')+'.'),
        numeric_task(f'{mid}'+('+' if sign=='-' else '-')+str(delta),6,'Corrige le détour : '+formula(f'{mid}'+('+' if sign=='-' else '-')+str(delta))+'.'),
        task('Explique pourquoi la correction va dans ce sens.','Je repère si j’ai ajouté ou retiré trop.',f'La dizaine choisie dépasse {b} de {delta}. '+('J’ai retiré trop : je dois rendre cette quantité.' if sign=='-' else 'J’ai ajouté trop : je dois enlever cette quantité.'),'Pour compenser, je corrige dans le sens opposé au premier détour.'),
        numeric_task(f'{a+10}{sign}{b}',6,'Recommence avec un nombre de départ augmenté de 10 : '+formula(f'{a+10}{sign}{b}')+'.')]
    if code==8:
        if index in (4,5,6):
            if index==4:
                return [numeric_task('25+25',4,'Trouve le double de 25.'),numeric_task('50//2',8,'Retrouve la moitié de 50.'),numeric_task('75+25',4,'Ajoute un groupe de 25 au total 75.'),task('Pourquoi 75 est-il un multiple de 25 ?','Je cherche un produit par 25.',eq('3*25')+'.','75 est obtenu avec trois groupes de 25 : c’est un multiple de 25.')]
            return [numeric_task('30+30',4,'Vérifie le repère : deux parts égales de 30.'),numeric_task('60//2',8,'Trouve la moitié de 60.'),numeric_task('4*15',10,'Vérifie le repère : quatre groupes de 15.'),task('Comment vérifier que 15 est bien la moitié de 30 ?','Je cherche le double de la moitié proposée.',eq('15+15')+'.','Deux parts de 15 reconstituent 30 : 15 est bien sa moitié.')]
        base=a//b if '//' in expr else b if a==2 else a
        total=base*2
        return [numeric_task(f'{base}+{base}',4,'Reprends le double de '+formula(str(base))+'.'),numeric_task(f'{total}//2',8,'Vérifie en retrouvant la moitié de '+formula(str(total))+'.'),numeric_task(f'{base+5}*2',8,'Trouve le double de '+formula(str(base+5))+'.'),task('Comment vérifier une moitié à l’aide d’un double ?','Je réunis deux parts égales à la moitié proposée.',eq(f'{base}+{base}')+f'. Deux parts de {base} reconstituent {total}.',f'Le double de {base} est {total}, donc la moitié de {total} est {base}.')]
    if code==7:
        if '//' in expr:a,b=a//b,2
        p=a*b
        return [numeric_task(f'{b}*{a}',7,'Calcule le produit dans l’autre sens : '+formula(f'{b}*{a}')+'.'),
        numeric_task(f'{p}//{b}',14,'Retrouve une part avec '+formula(f'{p}//{b}')+'.'),
        numeric_task(f'{a}*{b+1}',10,'Ajoute un groupe identique : calcule '+formula(f'{a}*{b+1}')+'.'),
        task('Dans '+formula(f'{a}*{b}={p}')+', nomme les facteurs et le produit.','Les facteurs sont multipliés ; le produit est le résultat.',f'Les deux facteurs sont {a} et {b}. Leur produit vaut {p}.',f'Les facteurs sont {a} et {b} ; le produit est {p}.')]
    if code in (9,10,11,12,13):
        if code==9 and a<10 and b%10==0:
            groups=a*(b//10)
            return [numeric_task(f'{a}*{b//10}',7,'Retrouve le nombre de dizaines avec la table : '+formula(f'{a}*{b//10}')+'.'),numeric_task(f'{groups}*10',9,'Écris ce nombre de dizaines en unités : '+formula(f'{groups}*10')+'.'),numeric_task(f'{a*b}//10',14,'Vérifie le nombre de dizaines dans le résultat avec '+formula(f'{a*b}//10')+'.'),numeric_task(f'{a+1}*{b}',9,'Ajoute un groupe de '+str(b)+' : calcule '+formula(f'{a+1}*{b}')+'.')]
        if code==10 and a<10 and b>=10:a,b=b,a
        if code==11 and a in (4,8) and b not in (4,8):a,b=b,a
        if code==13:
            units=b%10;tens=b-units
            return [numeric_task(f'{a}*{units}',12,'Calcule la ligne des unités : '+formula(f'{a}*{units}')+'.'),
            numeric_task(f'{a}*{tens}',9,'Calcule la ligne des dizaines : '+formula(f'{a}*{tens}')+'.'),
            numeric_task(f'{a*units}+{a*tens}',4,'Réunis les deux lignes : '+formula(f'{a*units}+{a*tens}')+'.'),
            task('Explique pourquoi la ligne des dizaines se termine par un zéro.','Je donne sa valeur au chiffre des dizaines.',f'La seconde ligne multiplie par {tens}, qui représente {tens//10} dizaines. Le produit compte des dizaines entières : il n’y a aucune unité isolée.','Je réserve le rang des unités et je recommence les retenues sur chaque ligne.')]
        if code==11:
            return [numeric_task(f'{a}+{a}',4,'Trouve le premier double de '+formula(str(a))+'.'),numeric_task(f'{a*2}+{a*2}',4,'Double encore le premier résultat.'),numeric_task(f'{a*4}+{a*4}',4,'Double une troisième fois pour obtenir huit groupes.'),task('Combien de doubles successifs faut-il pour multiplier par 4, puis par 8 ?','Je compte les groupes après chaque double.','Un double fait deux groupes ; le double suivant fait quatre groupes ; le troisième fait huit groupes.','Deux doubles donnent le produit par 4 ; trois doubles donnent le produit par 8.')]
        high=a//10*10;low=a%10
        next_a=a+1 if (a+1)*b<=10000 else a-1
        return [numeric_task(f'{high}*{b}',9 if code==9 else 10,'Calcule la partie des dizaines : '+formula(f'{high}*{b}')+'.'),numeric_task(f'{low}*{b}',7,'Calcule la partie des unités : '+formula(f'{low}*{b}')+'.'),numeric_task(f'{high*b}+{low*b}',4,'Réunis les deux parties : '+formula(f'{high*b}+{low*b}')+'.'),numeric_task(f'{next_a}*{b}',code,'Recommence avec un objet '+('de plus' if next_a>a else 'de moins')+' dans chacun des '+str(b)+' groupes : '+formula(f'{next_a}*{b}')+'.')]
    if code==14:
        # Le premier calcul du problème donne le total et la taille d'un groupe.
        q,r=divmod(a,b)
        sharing=index in (3,5,8)
        return [numeric_task(f'{b}*{q}',10,('Combien d’objets ont été distribués en tout ?' if sharing else 'Combien d’objets les groupes complets utilisent-ils ?')+' Calcule '+formula(f'{b}*{q}')+'.'),numeric_task(f'{a}-{b*q}',5,'Retrouve ce qui reste : '+formula(f'{a}-{b*q}')+'.'),task('Peut-on encore '+('donner un objet à chaque enfant avec le reste ?' if sharing else 'faire un groupe complet avec le reste ?'),'Je compare le reste '+('au nombre d’enfants.' if sharing else 'à la taille d’un groupe.'),f'Le reste est {r}. '+(f'Donner encore un objet à chacun des {b} enfants demanderait {b} objets : il n’y en a pas assez.' if sharing else f'Un groupe demande {b} objets. Le reste est plus petit que la taille d’un groupe.'),'Non, '+('le partage est terminé.' if sharing else 'le groupement est terminé.')),numeric_task(f'{b}*{q}+{r}',4,'Recompose le total avec '+('les parts' if sharing else 'les groupes')+' et le reste : '+formula(f'{b}*{q}+{r}')+'.')]

def column_figure(values,op,result,name):
    # Chiffres dans des colonnes espacées ; le trait reste loin des textes.
    lines=[r'\begin{tikzpicture}[x=1.25cm,y=0.68cm]']
    for k,label in enumerate(('milliers','centaines','dizaines','unités')):
        lines.append(r'\node[text=otNavy,font=\small] at ('+str(k)+',1) {'+label+'};')
    for row,v in enumerate(values):
        for k,c in enumerate(str(v).rjust(4)):
            if c!=' ':lines.append(r'\node[text=otInk] at ('+str(k)+','+str(-row)+') {$'+c+'$};')
        if row:lines.append(r'\node[text=otNavy] at (-0.7,'+str(-row)+') {$'+op+'$};')
    y=-len(values)+.5
    lines.append(r'\draw[otNavy,line width=0.8pt] (-0.4,'+str(y-.12)+') -- (3.4,'+str(y-.12)+');')
    if result is not None:
        for k,c in enumerate(str(result).rjust(4)):
            if c!=' ':lines.append(r'\node[text=otGreenDark] at ('+str(k)+','+str(-len(values)-.25)+') {$'+c+'$};')
    lines.append(r'\end{tikzpicture}');return '\n'.join(lines)

def array_figure(rows,cols):
    lines=[r'\begin{tikzpicture}[x=0.5cm,y=0.5cm]']
    for r in range(rows):
        for c in range(cols):lines.append(r'\fill[otNavy] ('+f'{c},{-r}'+r') circle (2.8pt);')
    lines.extend([r'\node[anchor=north,text=otNavy] at ('+str((cols-1)/2)+','+str(-rows)+') {'+str(rows)+' rangées de '+str(cols)+' points};',r'\end{tikzpicture}']);return '\n'.join(lines)

def multwo_figure(a,b):
    rows=[a,b,a*(b%10),a*(b//10)*10,a*b];ys=[0,-1,-2.25,-3.25,-4.5]
    lines=[r'\begin{tikzpicture}[x=1cm,y=.68cm]']
    for row,(v,y) in enumerate(zip(rows,ys)):
        for k,c in enumerate(str(v).rjust(4)):
            if c!=' ':lines.append(r'\node[text='+('otGreenDark' if row==4 else 'otInk')+'] at ('+str(k)+','+str(y)+') {$'+c+'$};')
    lines.extend([r'\node[text=otNavy] at (-.7,-1) {$\times$};',r'\node[text=otNavy] at (-.7,-3.25) {$+$};',r'\node[text=otNavy,anchor=west] at (3.8,-2.25) {$\times '+str(b%10)+'$};',r'\node[text=otNavy,anchor=west] at (3.8,-3.25) {$\times '+str(b//10*10)+'$};',r'\draw[otNavy] (-.4,-1.6) -- (3.4,-1.6);',r'\draw[otNavy] (-.4,-3.85) -- (3.4,-3.85);',r'\end{tikzpicture}'])
    return '\n'.join(lines)

def chain_figure(values,labels):
    lines=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    for i,v in enumerate(values):
        lines.append(r'\node[text='+('otGreenDark' if i==len(values)-1 else 'otNavy')+'] at ('+str(i*2.5)+',0) {$'+n(v)+'$};')
        if i:
            lines.append(r'\draw[otMuted,-{Stealth[length=2mm]}] ('+str((i-1)*2.5+.65)+',0) -- ('+str(i*2.5-.65)+',0);')
            lines.append(r'\node[text=otNavy] at ('+str(i*2.5-1.25)+',.55) {$'+labels[i-1]+'$};')
    lines.append(r'\end{tikzpicture}');return '\n'.join(lines)

def split_figure(a,b):
    hi=a//10*10;lo=a%10
    return '\n'.join([r'\begin{tikzpicture}[x=1cm,y=1cm]',r'\filldraw[fill=otSky,draw=otNavy] (0,0) rectangle (3,1.5);',r'\filldraw[fill=otGreen!12,draw=otNavy] (3,0) rectangle (4.3,1.5);',r'\node[text=otNavy] at (1.5,1.85) {$'+str(hi)+'$};',r'\node[text=otNavy] at (3.65,1.85) {$'+str(lo)+'$};',r'\node[text=otNavy,anchor=east] at (-.2,.75) {$'+str(b)+'$};',r'\node[text=otNavy] at (1.5,.75) {$'+str(hi)+r'\times '+str(b)+'$};',r'\node[text=otGreenDark] at (3.65,.75) {$'+str(lo)+r'\times '+str(b)+'$};',r'\end{tikzpicture}'])

def group_figure(a,b):
    q,r=divmod(a,b);lines=[r'\begin{tikzpicture}[x=0.38cm,y=0.38cm]']
    # Groupes disposés sur deux lignes au maximum ; reste séparé à droite.
    for k in range(q):
        gx=(k%4)*4;gy=-(k//4)*5
        lines.append(r'\draw[otNavy,rounded corners=2pt] ('+f'{gx-.6},{gy+.6}'+') rectangle ('+f'{gx+2.6},{gy-2.6}'+');')
        for j in range(b):lines.append(r'\fill[otNavy] ('+f'{gx+j%3},{gy-j//3}'+r') circle (2pt);')
    for j in range(r):lines.append(r'\fill[otGreenDark] ('+f'{16+j%3},{-j//3}'+r') circle (2pt);')
    lines.append(r'\node[text=otGreenDark,anchor=north] at (17,-3) {reste};');lines.append(r'\end{tikzpicture}');return '\n'.join(lines)

def share_figure(total,parts):
    lines=[r'\begin{tikzpicture}[x=1cm,y=1cm]',r'\node[text=otNavy] at (2.4,2) {'+str(total)+' images à partager};']
    for k in range(parts):
        x=k%2*2.6;y=-(k//2)*1.8
        lines.extend([r'\filldraw[fill=otSky,draw=otNavy] ('+f'{x},{y}'+') rectangle ('+f'{x+2.2},{y+1.4}'+');',r'\node[text=otNavy] at ('+f'{x+1.1},{y+.95}'+') {enfant '+str(k+1)+'};',r'\node[text=otNavy] at ('+f'{x+1.1},{y+.4}'+r') {$?$ images};'])
    lines.append(r'\end{tikzpicture}');return '\n'.join(lines)

def figure_from_spec(spec):
    kind,args=spec
    if kind in ('add4','blank4'):return column_figure([2786,1457],'+',4243,'')
    if kind=='mulblank':return column_figure([23,12],r'\times',276,'') if args==2 else column_figure([123,3],r'\times',369,'')
    if kind=='mulone':return column_figure(args,r'\times',args[0]*args[1],'')
    if kind=='multwo':return multwo_figure(*args)
    if kind=='array':return array_figure(*args)
    if kind=='compensation':a,b,c=args;return chain_figure([a,a+b,a+b+c],[str(b) if b<0 else '+'+str(b),str(c) if c<0 else '+'+str(c)])
    if kind=='doublechain':a,k=args;return chain_figure([a*2**i for i in range(k+1)],[r'\times 2']*k)
    if kind=='shift4':a,b=args;return chain_figure([a,a*b],[r'\times '+str(b)])
    if kind=='splitproduct':return split_figure(*args)
    if kind=='groupsremainder':return group_figure(*args)
    if kind=='sharebar':return share_figure(*args)
    raise ValueError(spec)

COURSE_EXAMPLES={4:'2786+1457',5:'4002-1678',6:'1246+38',7:'8*7',8:'150//2',9:'724*10',10:'24*6',11:'27*8',12:'246*3',13:'234*16',14:'38//6'}
GUIDED={4:['1685+2247'],5:['3205-1487'],6:['2305-29'],7:['9*7'],8:['75*2','4*15'],9:['8*60'],10:['37*4'],11:['45*4'],12:['325*4'],13:['125*24'],14:['56//7']}
HELPS={4:'Je dessine un échange : dix unités deviennent une dizaine. Puis je refais le calcul avec les chiffres.',5:'Je dessine les rangs et je dis quel rang donne une unité et quel rang reçoit dix unités.',6:'Je note mes deux étapes sur l’ardoise et j’explique pourquoi je dois ajouter ou enlever pour corriger.',7:'Je dessine des groupes égaux. Je retrouve un produit oublié grâce à un produit que je connais.',8:'Je dessine deux parts égales. Pour vérifier une moitié, je cherche son double.',9:'Je déplace des cartes chiffres dans un tableau de rangs et je dis la nouvelle valeur de chaque chiffre.',10:'Je dessine un rectangle coupé en deux parties. Chaque partie correspond à un produit.',11:'Je note chaque double et je compte les groupes : deux, puis quatre, puis huit.',12:'Je dis ce que représente ma retenue. Je l’ajoute après la multiplication du rang suivant.',13:'À côté des deux lignes, je peux noter « fois les unités » et « fois les dizaines ».',14:'Je dessine les parts ou les groupes et je dis si je cherche la taille d’une part ou le nombre de groupes.'}
WARNINGS={5:'Je garde la même quantité quand je fais un échange. Je suis la méthode apprise en classe, sans mélanger les écritures.',6:'Si j’ai ajouté trop, j’enlève pour corriger. Si j’ai retiré trop, j’ajoute pour corriger.',8:'La moitié n’est pas toujours un nombre de dizaines entières : la moitié de 150 est 75, car deux parts de 75 font 150.',9:'Je donne d’abord sa nouvelle valeur à chaque chiffre. Les zéros servent à écrire les rangs devenus vides.',14:'Dans un groupement terminé, le reste est plus petit que la taille d’un groupe. Si des objets restent, j’explique ce qu’ils deviennent.'}

VERIFIER=r'''# -*- coding: utf-8 -*-
"""Audit autonome : relit les vrais textes, recompose chaque égalité et réponse.
Ne charge pas le générateur. Analyse AST arithmétique indépendante et Fraction.
"""
from pathlib import Path
from fractions import Fraction
import ast,json,re,hashlib,runpy
P=Path(__file__).resolve().parent
def value(s):
 s=s.replace(r'\,','').replace(r'\times','*').replace(r'\div','/').replace(' ','')
 t=ast.parse(s,mode='eval').body
 def walk(x):
  if isinstance(x,ast.Constant) and isinstance(x.value,int):return Fraction(x.value)
  if isinstance(x,ast.UnaryOp) and isinstance(x.op,ast.USub):return -walk(x.operand)
  if isinstance(x,ast.BinOp):
   a,b=walk(x.left),walk(x.right)
   if isinstance(x.op,ast.Add):return a+b
   if isinstance(x.op,ast.Sub):return a-b
   if isinstance(x.op,ast.Mult):return a*b
   if isinstance(x.op,ast.Div):return a/b
   if isinstance(x.op,ast.FloorDiv):return a//b
   if isinstance(x.op,ast.Mod):return a%b
  raise ValueError(s)
 return walk(t)
texts={f:(P/f).read_text(encoding='utf8') for f in ('cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt')}
equalities=0
for f,content in texts.items():
 for m in re.finditer(r'(?<!\$)\${1,2}([^$]+)\${1,2}',content):
  s=m[1].strip()
  if '=' not in s:continue
  parts=s.split('=')
  try: vals=list(map(value,parts))
  except (ValueError,SyntaxError):raise AssertionError((f,'égalité non vérifiée',s))
  assert all(x==vals[0] for x in vals),(f,s,vals)
  assert all(0<=v<=10000 for v in vals),(f,'borne CE2',s)
  equalities+=1
blocks=re.split(r'^===[ \t]*$',texts['exercices.txt'],flags=re.M)
blocks=[b for b in blocks if b.strip()]
assert len(blocks)==9
source=json.loads((P/'sources_locales/chapitre.json').read_text(encoding='utf8'))
questions=0
for i,b in enumerate(blocks,1):
 assert re.search(r'^Id: nouveau-'+str(i)+r'$',b,re.M)
 enonce=b.split('Énoncé:\n')[1].split('Étapes:\n')[0]
 steps=b.split('Étapes:\n')[1].split('Solution:\n')[0]
 solution=b.split('Solution:\n')[1]
 qs=re.findall(r'^(\d+)\. (.+)',enonce,re.M)
 assert len(qs)==5,(i,len(qs))
 assert [int(k) for k,_ in qs]==[1,2,3,4,5]
 assert len(re.findall(r'^## Question ',steps,re.M))==5
 assert len(re.findall(r'^::: methode',steps,re.M))==5
 assert len(re.findall(r'^::: resultat',steps,re.M))==5
 # Les réponses de chaque question sont identiques dans résultat et solution.
 results=re.findall(r'^::: resultat\n([\s\S]*?)\n:::',steps,re.M)
 sols=re.findall(r'^\d+\. (.*)',solution,re.M)
 assert results==sols,(i,'résultat/solution')
 assert results[0]==source['exercices'][i-1]['reponse'],(i,'réponse source altérée')
 assert source['exercices'][i-1]['consigne'] in enonce,(i,'couverture source')
 # Les calculs issus du livre sont recomposés indépendamment depuis leur AST.
 for check in source['exercices'][i-1]['check'].split(' and '):
  if not check:continue
  lhs,rhs=check.split('==');assert value(lhs)==value(rhs),(i,check)
  if '%' not in lhs:
   actual_numbers=[int(x.replace(' ','')) for x in re.findall(r'\d+(?: \d{3})*',results[0])]
   if int(value(rhs)) not in actual_numbers:
    assert source['exercices'][i-1]['consigne'].startswith('Complète'),(i,'résultat numérique absent de la réponse',rhs,results[0])
    # Pour une égalité à compléter, la réponse est un terme ou un facteur.
    assert set(map(int,re.findall(r'\d+',lhs))) & set(actual_numbers),(i,'terme ou facteur manquant non retrouvé')
 questions+=len(qs)
figures=runpy.run_path(str(P/'figures/figures.py'))['FIGURES']
figures_checked=0
for name,tikz in figures.items():
 # Recomposer les opérations posées depuis les chiffres réellement dessinés.
 rows={}
 for color,x,y,digit in re.findall(r'\\node\[text=(otInk|otGreenDark)\] at \((\d+),(-?[\d.]+)\) \{\$(\d)\$\};',tikz):
  rows.setdefault((color,float(y)),{})[int(x)]=int(digit)
 if not rows:continue
 def number(ds):return sum(d*10**(3-k) for k,d in ds.items())
 inputs=[number(v) for (color,y),v in sorted(rows.items(),key=lambda kv:-kv[0][1]) if color=='otInk']
 result=[number(v) for (color,y),v in rows.items() if color=='otGreenDark']
 if not result:continue
 if r'\times' in tikz:
  assert inputs[0]*inputs[1]==result[0],(name,inputs,result)
  if len(inputs)==4:
   assert inputs[2]==inputs[0]*(inputs[1]%10)
   assert inputs[3]==inputs[0]*(inputs[1]//10)*10
   assert inputs[2]+inputs[3]==result[0]
 elif '{$-$}' in tikz:assert inputs[0]-inputs[1]==result[0]
 else:assert sum(inputs)==result[0]
 figures_checked+=1
report={'statut':'OK','math_OK':True,'exercices':len(blocks),'questions':questions,'egalites_recomposees':equalities,'empreintes':{f:hashlib.sha256(s.encode('utf8')).hexdigest() for f,s in texts.items()}}
report['figures_operations_recomposees']=figures_checked
(P/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
'''

def prepare(d):
    j=json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf8'));code=j['numero']
    (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'ce2_calculs','maj':'2026-11-02'},ensure_ascii=False,indent=2),encoding='utf8')
    figs={};corr={'cours':{'nouveau':{}},'fiches':{'nouvelle':{}},'exercices':{}}
    # Une figure du cours et les seules figures utiles demandées par le livre.
    if code==5:course_fig=column_figure([4002,1678],'-',2324,'')
    elif code==8:course_fig=chain_figure([75,150],[r'\times 2'])
    elif code==7:course_fig=array_figure(8,7)
    else:course_fig=figure_from_spec(j.get('figure') or ['array',[8,7]])
    figs['cours_methode']=course_fig
    alt='Représentation du calcul expliqué dans le cours : '+j['titre'].lower()+'.'
    corr['cours']['nouveau']['1']={'fichier':'cours_methode.png','alt':alt}
    corr['fiches']['nouvelle']['1']={'fichier':'cours_methode.png','alt':alt}
    example=COURSE_EXAMPLES[code]
    lesson='\n\n'.join(box('propriete',f'Repère {i}',t) for i,t in enumerate(j['lecon'],1))
    warning=WARNINGS.get(code,j['vigilance'])
    course=f'Titre: {j["titre"]}\n{MARK}\n\n'+box('objectifs','',j['objectif']+'\n\n- Expliquer les étapes avec des mots simples.\n- Contrôler le résultat obtenu.')+'\n\n## I. Comprendre\n\n'+lesson+'\n\n## II. Faire pas à pas\n\n'+box('methode','Je cherche avant de calculer','Je lis la consigne. Je repère les nombres et ce qu’ils comptent. Je choisis une méthode puis je garde les étapes utiles sur mon ardoise.')+'\n\n[IMAGE_1]\n\n'+box('exemple','Un calcul expliqué',arithmetic_work(example,code))+'\n\n### À toi, avec de l’aide\n\n'+j['guide']+'\n\n'+box('exemple','Je vérifie ma recherche','\n\n'.join(arithmetic_work(e,code) for e in GUIDED[code])+'\n\n'+j['guide_reponse'])+'\n\n## III. Vérifier et choisir\n\n'+box('attention','Le piège à éviter',warning)+'\n\n'+box('conseil','Si je bloque',HELPS[code])+'\n\n'+box('retenir','',j['objectif'])+'\n'
    if code==14:course=course.replace('## II. Faire pas à pas','Une division peut chercher le nombre de parts ou la taille de chaque part. Quand le partage est exact, on utilise le signe $\\div$. Par exemple, '+eq('24//4')+'. Avec un reste, on donne séparément le nombre de groupes et le reste.\n\n## II. Faire pas à pas')
    fiche=f'Titre: {j["titre"]} — fiche\n{MARK}\n\n## I. Les repères\n\n'+box('retenir','', '\n'.join('- '+x for x in j['lecon']))+'\n\n## II. Ma méthode\n\n'+box('methode','',j['objectif']+' Je note les résultats intermédiaires puis je contrôle la réponse.')+'\n\n[IMAGE_1]\n\n'+box('attention','',warning)+'\n'
    (d/'cours_nouveau.txt').write_text(course,encoding='utf8');(d/'fiche_nouvelle.txt').write_text(fiche,encoding='utf8')
    blocks=[];coverage=[]
    for i,src in enumerate(j['exercices'],1):
        main,expr=core_task(src,code,i);tasks=[main]+companion_tasks(code,expr,i)
        for t in tasks:
            if re.fullmatch(r'\$[^$]+\$\.',t['result']):t['result']=t['result'][:-1]
        if src.get('figure'):
            spec=src['figure'];fig='ex'+str(i)+'_support'
            # Les grilles vides de l'ancien livre deviennent des dispositions adaptées.
            if spec[0] in ('blank4','mulblank'):
                match=re.findall(r'\d+',expr);values=list(map(int,match));op='-' if '-' in expr else r'\times' if '*' in expr else '+'
                figs[fig]=column_figure(values,op,None,'')
            else:figs[fig]=figure_from_spec(spec)
            corr['exercices'][f'nouveau-{i}']={'1':{'fichier':fig+'.png','alt':'Support du premier calcul : '+TITLES[code][i-1].lower()+'.'}}
        typ='Découverte' if i==1 else 'Problème' if i in (7,8) else 'Entraînement'
        title=f'{typ} - {TITLES[code][i-1]}'
        enonce=MARK+'\n'+('\n\n'.join(f'{k}. {t["prompt"]}' for k,t in enumerate(tasks,1)))
        steps=MARK+'\n\n'+'\n\n'.join(f'## Question {k} : Je cherche et j’explique\n\n'+box('methode','',t['method'])+'\n\n'+box('etape','Mon raisonnement',t['work'])+'\n\n'+box('resultat','',t['result']) for k,t in enumerate(tasks,1))
        solution=MARK+'\n'+'\n'.join(f'{k}. {t["result"]}' for k,t in enumerate(tasks,1))
        blocks.append(f'=== {title}\nId: nouveau-{i}\nDifficulté: '+('easy' if i==1 else 'medium' if i<7 else 'hard')+f'\n\nÉnoncé:\n{enonce}\n\nÉtapes:\n{steps}\n\nSolution:\n{solution}\n')
        coverage.append(f'| {i} | nouveau-{i} | {src["consigne"].replace("|","/")} | Q1 conserve la compétence et les données ; Q2–Q5 explicitent, contrôlent ou prolongent le même calcul. |')
    (d/'exercices.txt').write_text('\n===\n'.join(blocks),encoding='utf8')
    (d/'figures/figures.py').write_text('# -*- coding: utf-8 -*-\n"""Figures TikZ au style livre ; compiler avec outils/figures_livre.py --jobs 1."""\nFIGURES = '+repr(figs)+'\n',encoding='utf8')
    (d/'figures/correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    (d/'verif_math.py').write_text(VERIFIER,encoding='utf8')
    (d/'COUVERTURE.md').write_text(f'# Couverture — {j["titre"]}\n\nLes neuf exercices du livre sont conservés, enrichis en cinq questions chacun (45 questions). Aucun exercice ajouté ; aucune compétence retirée. Les données et demandes d’origine restent dans la question 1.\n\n| Source | Identifiant | Consigne originale | Traitement |\n|---|---|---|---|\n'+'\n'.join(coverage)+f'\n\nProgramme officiel vérifié le 2 novembre 2026 : [cycle 2]({PROGRAMME}), pages 19–23 ; nombres et résultats limités à 10 000. Multiplications posées par deux chiffres explicitement attendues p.20. La division est travaillée par partage, groupement et multiplication, sans algorithme posé formel. Les écritures à virgule ne figurent que dans le problème de monnaie du chapitre 14.\n',encoding='utf8')
    (d/'RAPPORT.md').write_text(f'# {j["titre"]}\n\nÉtat : textes, calculs et définitions des figures préparés. Relecture graphique finale en attente du créneau de compilation.\n\nNeuf exercices source conservés, cinq questions avec méthode, étapes et résultat chacun. Cours explicite et fiche courte au format v1. Vérification indépendante par `verif_math.py`, qui relit les livrables, recompose les égalités et compare résultats et solutions.\n\nFigures : '+str(len(figs))+' nouvelles figures TikZ, aucune image en ligne à conserver. Les dispositions, décompositions et groupements sont adaptés aux données.\n\nAucun accès à la base ; aucun changement des outils ou des sources.\n',encoding='utf8')
    (d/'PREUVES_FINALES.json').write_text(json.dumps({'statut':'en_cours','math_OK':False,'figures_vues':[],'captures_lues':[],'anomalies':None},ensure_ascii=False,indent=2),encoding='utf8')
    print(code,len(figs),'figures définies, 9 exercices, 45 questions')

if __name__=='__main__':
    for d in sorted(ROOT.iterdir()):
        if d.name[:2].isdigit() and 4<=int(d.name[:2])<=14:prepare(d)
