"""Rédaction du lot calculs CP, exclusivement dans les neuf dossiers attribués."""
from pathlib import Path
import sys,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'_coordination'))
from commun_redaction import q,ex,write,table
CODES=[4,5,6,11,12,14,15,16,30]
TITRES={4:'Comprendre et utiliser l’addition',5:'Comprendre et utiliser la soustraction',6:'Mémoriser les compléments à 10',11:'Connaître les doubles et les moitiés',12:'Calcul mental : ajouter et soustraire 1, 2 ou des dizaines',14:'Calcul mental : passer par la dizaine',15:'Calcul mental : additionner en décomposant',16:'Calcul mental : soustraire par décomposition et échange',30:'Addition posée : alignement et retenue'}
SEEDS={4:[(4,3),(2,1),(2,4),(6,0),(3,2),(2,5),(3,4),(2,6),(4,2)],5:[(8,3),(4,1),(9,4),(7,0),(6,2),(8,5),(9,2),(6,4),(5,2)],6:[(7,3),(2,8),(3,7),(6,4),(4,6),(0,10),(4,6),(7,3),(5,5)],11:[(5,5),(7,7),(6,6),(8,8),(30,30),(40,40),(9,9),(7,7),(24,24)],12:[(29,1),(27,10),(24,20),(35,20),(64,30),(28,20),(32,20),(46,-10),(100,-90)],14:[(36,7),(47,3),(8,6),(48,5),(26,9),(30,9),(27,6),(72,9),(38,5)],15:[(23,15),(41,26),(28,14),(46,27),(24,36),(12,23,15),(34,28),(45,37),(58,24)],16:[(50,7),(20,3),(70,4),(32,5),(43,18),(51,24),(30,7),(42,16),(40,6)],30:[(32,24),(45,7),(26,38),(47,29),(18,6,24),(59,41),(36,27),(28,16),(34,5)]}
def form(s):return '$'+s+'$'
def eq(a,op,b):return form(f'{a}{op}{b}={a+b if op=="+" else a-b}')
def add_reason(nums):
    if len(nums)>2:
        a,b,c=nums;return f'Je réunis d’abord deux nombres : {eq(a,"+",b)}. Puis {eq(a+b,"+",c)}.'
    a,b=nums
    if max(a,b)<=10:
        if b==0:return f'Je garde les {a} jetons. Ajouter zéro ne change rien : {eq(a,"+",b)}.'
        return f'Je pars de {a}. J’ajoute {b} jetons. Je compte {a+b} jetons en tout : {eq(a,"+",b)}.'
    da,db=a//10*10,b//10*10;ua,ub=a%10,b%10
    return f'Je sépare dizaines et unités. {eq(da,"+",db)}. {eq(ua,"+",ub)}. Je réunis : {eq(da+db,"+",ua+ub)}.'
def sub_reason(a,b):
    if a<=10:return f'Je pose {a} jetons. J’en écarte {b}. Il en reste {a-b}. Je vérifie : {eq(a-b,"+",b)}.'
    if b%10==0:return f'J’enlève {b//10} dizaines. Les unités ne changent pas. {eq(a,"-",b)}. Je vérifie : {eq(a-b,"+",b)}.'
    if a%10 < b%10:
        d=a//10*10-10;u=a%10+10
        return f'J’échange une dizaine contre dix unités. {form(f"{a}={d}+{u}")}. J’enlève {b//10} dizaines et {b%10} unités. {eq(d,"-",b//10*10)}. {eq(u,"-",b%10)}. Je réunis : {eq(d-b//10*10,"+",u-b%10)}.'
    return f'Je retire d’abord {b//10*10}, puis {b%10}. {eq(a,"-",b//10*10)}. {eq(a-b//10*10,"-",b%10)}.'
def bridge(a,b):
    if b==9:return f'J’ajoute une dizaine : {eq(a,"+",10)}. J’ai ajouté un de trop. Je retire un : {eq(a+10,"-",1)}.'
    gap=10-a%10 if a%10 else 0
    if not gap or b<gap:return add_reason((a,b))
    return f'Il manque {gap} pour atteindre {a+gap}. Je partage {b} en {gap} et {b-gap}. {eq(a,"+",gap)}. Puis {eq(a+gap,"+",b-gap)}.'
def col_reason(nums):
    u=sum(n%10 for n in nums);r=u//10;d=sum(n//10 for n in nums)+r
    s=' + '.join(str(n%10) for n in nums)
    return f'J’aligne les unités. Je commence à droite : {form(s+"="+str(u))}. '+(f'J’écris {u%10} unités. J’échange dix unités contre une dizaine. Je retiens {r} dizaine. ' if r else f'J’écris {u} unités. Il n’y a pas de retenue. ')+f'Je compte ensuite {d} dizaines. '+('Dix dizaines font cent. ' if d==10 else '')+f'Le total est {sum(nums)}.'
def dots(a,b,done=False,remove=False):
    s=[r'\begin{tikzpicture}[x=0.52cm,y=0.65cm]']
    if remove:
        for i in range(a):
            x=i%5;y=-(i//5)
            col='otGreenDark' if done and i<a-b else 'otNavy'
            s.append(fr'\draw[draw={col},fill={col}!12,line width=.8pt] ({x},{y}) circle (.16);')
            if i>=a-b:s.append(fr'\draw[otOrange,line width=1pt] ({x-.19},{y-.19})--({x+.19},{y+.19});')
        if done:s.append(fr'\node[text=otGreenDark] at (2,-2.4) {{{a-b} restent}};')
    else:
        for j,n in enumerate((a,b)):
            for i in range(n):
                x=j*5.2+i%5;y=-(i//5)
                col='otGreenDark' if done and j else 'otNavy'
                s.append(fr'\fill[{col}] ({x},{y}) circle (.15);')
        if done:s.append(fr'\node[text=otGreenDark] at (4.1,-2.1) {{$ {a}+{b}={a+b} $}};')
    s.append(r'\end{tikzpicture}');return '\n'.join(s)
def frame(n,done=False):
    s=[r'\begin{tikzpicture}[x=.75cm,y=.75cm]']
    for i in range(10):
        x=i%5;y=-(i//5)
        s.append(fr'\draw[otRule] ({x-.5},{y-.5}) rectangle ({x+.5},{y+.5});')
        if i<n or done:s.append(fr'\fill[{"otNavy" if i<n else "otGreenDark"}] ({x},{y}) circle (.18);')
    if done:s.append(fr'\node[text=otGreenDark] at (2,-2.1) {{$ {n}+{10-n}=10 $}};')
    s.append(r'\end{tikzpicture}');return '\n'.join(s)
def jumps(a,b,done=False):
    gap=10-a%10 if a%10 else 0
    end=a+b
    s=[r'\begin{tikzpicture}[x=1cm,y=1cm]',r'\draw[otMuted,->] (-.2,0)--(5.4,0);']
    vals=[str(a),str(a+gap) if gap else str(a+10),str(end)] if done else [str(a),'?','?']
    for x,t in zip([0,2.5,5],vals):
        s+=[fr'\draw[otMuted] ({x},-.08)--({x},.08);',fr'\node[below,text={"otGreenDark" if done and x else "otNavy"},yshift=-3pt] at ({x},-.08) {{{t}}};']
    for x,t in [(0,str(gap)),(2.5,str(b-gap))]:
        s.append(fr'\draw[{"otGreenDark" if done else "otNavy"},->] ({x},.2) to[bend left=45] ({x+2.5},.2);')
        s.append(fr'\node[text={"otGreenDark" if done else "otNavy"}] at ({x+1.25},1.05) {{+{t if done else "?"}}};')
    s.append(r'\end{tikzpicture}');return '\n'.join(s)
def base(n,remove=0,done=False,extra=0):
    # Les barres et les cubes sont des objets à manipuler, pas un tableau de données.
    d=n//10;u=n%10
    if remove and u<remove%10:d-=1;u+=10
    if done:
        total=n+extra-remove;d=total//10;u=total%10
    s=[r'\begin{tikzpicture}[x=.55cm,y=.55cm]']
    for j in range(d):
        col='otGreenDark' if done else 'otNavy'
        s.append(fr'\draw[{col},fill={col}!10] ({j*.65},0) rectangle ({j*.65+.38},2);')
        for k in range(1,10):s.append(fr'\draw[{col}!50] ({j*.65},{k*.2})--({j*.65+.38},{k*.2});')
    off=max(d*.65+.5,1)
    for j in range(u):
        x=off+(j%5)*.55;y=(j//5)*.55
        s.append(fr'\draw[{"otGreenDark" if done else "otNavy"},fill={"otGreenDark" if done else "otNavy"}!10] ({x},{y}) rectangle ({x+.34},{y+.34});')
    text=f'{n+extra-remove} en tout' if done else 'Une barre vaut dix cubes.'
    s.append(fr'\node[text={"otGreenDark" if done else "otNavy"}] at (3,-.8) {{{text}}};')
    s.append(r'\end{tikzpicture}');return '\n'.join(s)
def tree(a,b,done=False):
    s=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
    for x,n in [(0,a),(3.5,b)]:
        s.append(fr'\node[text=otNavy] at ({x},1.5) {{{n}}};')
        s.append(fr'\draw[otMuted] ({x-.1},1.15)--({x-.7},.55);')
        s.append(fr'\draw[otMuted] ({x+.1},1.15)--({x+.7},.55);')
        for dx,t in [(-.8,str(n//10*10)),(.8,str(n%10))]:s.append(fr'\node[text={"otGreenDark" if done else "otNavy"}] at ({x+dx},.2) {{{t if done else "?"}}};')
    if done:s.append(fr'\node[text=otGreenDark] at (1.75,-.65) {{$ {a}+{b}={a+b} $}};')
    s.append(r'\end{tikzpicture}');return '\n'.join(s)
def column(nums,done=False):
    s=[r'\begin{tikzpicture}[x=.72cm,y=.65cm]']
    xs=[0,1,2]
    for x,t in zip(xs,['C','D','U']):s.append(fr'\node[text=otMuted] at ({x},1) {{{t}}};')
    if done:
        carry=sum(n%10 for n in nums)//10
        if carry:s.append(fr'\node[text=otGreenDark] at (1,.4) {{\scriptsize {carry}}};')
    for j,n in enumerate(nums):
        for k,ch in enumerate(str(n)[::-1]):s.append(fr'\node[text=otNavy] at ({2-k},{-j-.3}) {{{ch}}};')
    y=-len(nums)-.05
    s.append(fr'\node[text=otNavy] at (-.8,{-len(nums)+.7}) {{+}};')
    s.append(fr'\draw[otNavy] (-.4,{y})--(2.5,{y});')
    if done:
        for k,ch in enumerate(str(sum(nums))[::-1]):s.append(fr'\node[text=otGreenDark] at ({2-k},{y-.55}) {{{ch}}};')
    else:
        for x in xs:s.append(fr'\node[text=otMuted] at ({x},{y-.55}) {{\ldots}};')
    s.append(r'\end{tikzpicture}');return '\n'.join(s)
def special_reason(code,i,src,nums):
    a,b=nums[:2]
    if code==4:return add_reason(nums)+(' Le signe égal relie deux quantités égales.' if i==9 else '')
    if code==5:return sub_reason(a,b)
    if code==6:return f'Je garde {a} jetons. Je compte les places vides jusqu’à dix : il en manque {10-a}. {eq(a,"+",10-a)}.'
    if code==11:
        if i==9:return 'Je décompose 48 en 40 et 8. Je partage 40 : 20 dans chaque part. Je partage 8 : 4 dans chaque part. '+eq(20,'+',4)+'. Je vérifie : '+eq(24,'+',24)+'.'
        return f'Pour un double, je réunis deux groupes identiques. Pour une moitié, je fais deux parts égales. Ici, {eq(a,"+",a)}. Chaque part contient {a} objets.'
    if code==12:return add_reason((a,b)) if b>=0 else sub_reason(a,-b)
    if code==14:return bridge(a,b)
    if code==15:return add_reason(nums)
    if code==16:return sub_reason(a,b)+(' La quantité totale reste la même pendant l’échange.' if i==9 else '')
    return col_reason(nums)
def enrich(code,nums,i):
    a,b=nums[:2];qs=[]
    if code==4:
        qs+=[q(f'Calcule {form(f"{b}+{a}")}.','Changer l’ordre des deux groupes.',add_reason((b,a)),eq(b,'+',a)),q(f'Complète : {form(f"{a}+\\ldots={a+b}")}.','Chercher le groupe manquant.',f'Le total est {a+b}. Le premier groupe contient {a}. Le second contient {b}. {eq(a,"+",b)}.',f'Le nombre manquant est {b}.'),q(f'Ajoute encore un jeton au total {a+b}. Combien en as-tu ?','Avancer d’un nombre.',f'Après {a+b}, je dis {a+b+1}. {eq(a+b,"+",1)}.',f'J’ai {a+b+1} jetons.'),q(f'Compare {form(f"{a}+{b}")} et {form(f"{a}+{b}+1")}. Quel total est le plus grand ?','Comparer deux collections.',f'Le premier total est {a+b}. Le second est {a+b+1}. Il contient un jeton de plus.',f'{a+b+1} est plus grand que {a+b}.')]
    elif code==5:
        r=a-b
        qs+=[q(f'Vérifie le retrait de {b} parmi {a} avec une addition.','Remettre les objets enlevés.',f'Il reste {r}. Je remets {b}. {eq(r,"+",b)}.',eq(r,'+',b)),q(f'Complète : {form(f"{a}-\\ldots={r}")}.','Chercher les jetons écartés.',f'Je passe de {a} à {r}. J’ai retiré {b} jetons. {eq(a,"-",b)}.',f'Il manque {b}.'),q(f'Que reste-t-il si tu n’enlèves aucun des {a} jetons ?','Enlever zéro.',f'Aucun jeton ne quitte le groupe. {eq(a,"-",0)}.',f'Il reste {a} jetons.'),q(f'Que reste-t-il si tu enlèves les {a} jetons ?','Enlever toute la collection.',f'Tous les jetons sont écartés. {eq(a,"-",a)}.',f'Il reste 0 jeton.')]
    elif code==6:
        c=(a+2)%11;v=(a+4)%11;w=(a+6)%11
        qs+=[q(f'Complète : {form(f"{c}+\\ldots=10")}.','Compter les places qui manquent.',f'Je compte de {c} jusqu’à 10. {eq(c,"+",10-c)}.',f'Il manque {10-c}.'),q(f'Complète : {form(f"10=\\ldots+{v}")}.','Chercher la première part.',f'Le total vaut dix. Une part vaut {v}. {eq(10-v,"+",v)}.',f'Il manque {10-v}.'),q(f'Calcule {form(f"10-{a}")}.','Retrouver l’autre part de dix.',f'Je retire une part de {a}. L’autre part vaut {10-a}. {eq(10,"-",a)}.',eq(10,'-',a)),q(f'Une boîte a dix places. {w} sont occupées. Combien sont libres ?','Utiliser un complément dans une situation.',f'Je cherche ce qu’il faut ajouter à {w}. {eq(w,"+",10-w)}.',f'{10-w} places sont libres.')]
    elif code==11:
        n=i%9+1;m=(n+1)%10+1;k=(n+3)%10+1
        qs+=[q(f'Quel est le double de {n} ?','Réunir deux groupes égaux.',add_reason((n,n)),f'Le double de {n} est {2*n}.'),q(f'Quelle est la moitié de {2*m} ?','Faire deux parts égales.',f'Je mets {m} dans chaque part. {eq(m,"+",m)}.',f'La moitié de {2*m} est {m}.'),q(f'On partage {n+m} jetons : {n} dans une boîte et {m} dans l’autre. Est-ce un partage égal ?','Comparer les deux parts.',f'Le total convient : {eq(n,"+",m)}. Mais {n} et {m} sont différents.',f'Non. Les parts de {n} et {m} jetons sont différentes.'),q(f'Sam dit que la moitié de {2*k} est {k-1}. Corrige sa réponse.','Vérifier avec deux parts identiques.',f'Deux parts de {k-1} donnent seulement {2*(k-1)}. {eq(k-1,"+",k-1)}. Il faut deux parts de {k} : {eq(k,"+",k)}.',f'La moitié de {2*k} est {k}.')]
    elif code==30:
        other=(*nums[:-1],nums[-1]-1);label=form('+'.join(map(str,other)))
        us=sum(x%10 for x in other);carry=us//10;ds=sum(x//10 for x in other)+carry
        qs+=[q(f'Autre calcul : {label}. Combien font les unités ensemble ?','Ajouter seulement les unités.',form('+'.join(str(x%10) for x in other)+'='+str(us))+'. Je n’ajoute pas encore les dizaines.',f'J’obtiens {us} unités.'),q(f'Pour {label}, faut-il une retenue ? Explique.','Chercher un groupe de dix unités.',f'Je peux former {carry} groupe de dix unités. Il reste {us%10} unités.',f'La retenue est {carry} dizaine.' if carry else 'Il n’y a pas de retenue.'),q(f'Pour {label}, combien de dizaines as-tu après l’échange ?','Ajouter les dizaines et la retenue.',form('+'.join([*(str(x//10) for x in other),str(carry)])+'='+str(ds))+'. Une retenue compte comme une dizaine.',f'J’ai {ds} dizaines.'),q(f'Calcule le total de {label}. Vérifie de tête.','Décomposer les nombres.',add_reason(other),form('+'.join(map(str,other))+'='+str(sum(other))))]
    else:
        minus=code==16 or (code==12 and b<0);b=abs(b);r=a-b if minus else a+b
        if minus:
            qs+=[q(f'Vérifie {form(f"{a}-{b}")} avec une addition.','Remettre ce qui a été retiré.',f'Je repars de {r}. Je remets {b}. {eq(r,"+",b)}.',eq(r,'+',b)),q(f'Complète : {form(f"{a}-\\ldots={r}")}.','Chercher la quantité retirée.',f'Le retrait est {b}. {eq(a,"-",b)}.',f'Il manque {b}.'),q(f'Calcule {form(f"{a}-1")}.','Reculer d’un nombre.',sub_reason(a,1),eq(a,'-',1)),q(f'Calcule {form(f"{a}-10")}.','Retirer une dizaine.',sub_reason(a,10),eq(a,'-',10))]
        else:
            calc=bridge if code==14 else lambda x,y:add_reason((x,y))
            qs+=[q(f'Complète : {form(f"{a}+\\ldots={r}")}.','Retrouver le nombre ajouté.',f'Je cherche la part qui fait passer de {a} à {r}. {eq(a,"+",b)}.',f'Il manque {b}.'),q(f'Calcule aussi {form(f"{b}+{a}")}.','Changer l’ordre des nombres.',add_reason((b,a)),eq(b,'+',a)),q(f'Calcule {form(f"{a}+1")}.','Avancer d’un nombre.',f'Je dis le nombre après {a}. {eq(a,"+",1)}.',eq(a,'+',1)),q(f'Calcule {form(f"{a}+{9 if code==14 else 10}")}.','Ajouter dix puis enlever un.' if code==14 else 'Ajouter une dizaine.',calc(a,9 if code==14 else 10),eq(a,'+',9 if code==14 else 10))]
    # Une activité source peut déjà demander le calcul de contrôle ou le trou.
    # Varier alors les nombres : chaque question reste un vrai travail nouveau.
    if code==4:
        qs[0]=q(f'Réunis {b+1} jetons et encore {a}. Écris le total.','Réunir deux nouveaux groupes.',add_reason((b+1,a)),eq(b+1,'+',a))
        qs[1]=q(f'Complète : {form(f"{a}+\\ldots={a+b+1}")}.','Chercher la nouvelle part manquante.',f'Le total vaut {a+b+1}. Je garde une part de {a}. {eq(a,"+",b+1)}.',f'Il manque {b+1}.')
        qs[2]=q(f'Ajoute deux jetons au total {a+b}. Combien en as-tu ?','Avancer deux fois.',f'Après {a+b}, je dis {a+b+1}, puis {a+b+2}. {eq(a+b,"+",2)}.',f'J’ai {a+b+2} jetons.')
    elif code==5:
        r=a-b
        qs[0]=q(f'Autre retrait : tu enlèves {b} parmi {a+1}. Vérifie avec une addition.','Remettre les jetons retirés.',f'Il reste {r+1} jetons. Je remets {b} jetons. {eq(r+1,"+",b)}.',eq(r+1,'+',b))
        qs[1]=q(f'Complète : {form(f"{a+1}-\\ldots={r+1}")}.','Chercher le nouveau retrait.',f'Je pars de {a+1}. Pour garder {r+1}, j’enlève {b}. {eq(a+1,"-",b)}.',f'Il manque {b}.')
        qs[2]=q(f'Que reste-t-il si tu n’enlèves aucun des {a+1} jetons ?','Enlever zéro.',f'Aucun jeton ne quitte le groupe. {eq(a+1,"-",0)}.',f'Il reste {a+1} jetons.')
    elif code in (12,14,15) and nums[1]>=0:
        qs[0]=q(f'Complète : {form(f"{a+1}+\\ldots={a+b+1}")}.','Retrouver la quantité ajoutée.',f'Je passe de {a+1} à {a+b+1}. {eq(a+1,"+",b)}.',f'Il manque {b}.')
    if code==11 and i in (5,6):
        qs=[q('Quelle est la moitié de 60 ?','Faire deux parts de trois dizaines.',f'Je mets 30 dans chaque part. {eq(30,"+",30)}.','La moitié de 60 est 30.'),q('Quel est le double de 50 ?','Réunir deux groupes de cinq dizaines.',f'Je réunis 50 et 50. {eq(50,"+",50)}.','Le double de 50 est 100.'),q('On partage 60 jetons : 20 dans une boîte et 40 dans l’autre. Est-ce égal ?','Comparer les parts.',f'Le total convient : {eq(20,"+",40)}. Mais les parts 20 et 40 sont différentes.','Non. Il faut 30 jetons dans chaque boîte.'),q('Sam dit que la moitié de 80 est 30. Corrige.','Contrôler le total des deux parts.',f'Deux parts de 30 donnent 60 : {eq(30,"+",30)}. Deux parts de 40 donnent 80 : {eq(40,"+",40)}.','La moitié de 80 est 40.')]
        if i==5:qs[1]=q('Quelle est la moitié de 100 ?','Faire deux parts de cinq dizaines.',f'Je mets 50 dans chaque part. {eq(50,"+",50)}.','La moitié de 100 est 50.')
        if i==6:qs[0]=q('Quel est le double de 20 ?','Réunir deux groupes de deux dizaines.',f'Je réunis 20 et 20. {eq(20,"+",20)}.','Le double de 20 est 40.')
    if code==11 and i==3:qs[1]=q('Quelle est la moitié de 16 ?','Faire deux parts égales.',f'Je mets 8 dans chaque part. {eq(8,"+",8)}.','La moitié de 16 est 8.')
    if code==11 and i in (5,6):qs[2]=q('Sam propose 20 et 40 comme les deux moitiés de 60. Est-ce juste ?','Comparer les deux parts.',f'Le total convient : {eq(20,"+",40)}. Mais les parts sont différentes. Les deux moitiés sont égales : {eq(30,"+",30)}.','Non. La moitié de 60 est 30.')
    if code==6 and i in (4,7):
        v=4 if i==4 else 5
        qs[2]=q(f'Calcule {form(f"10-{v}")}.','Retrouver l’autre part de dix.',f'Je retire {v} jetons de dix. {eq(10,"-",v)}. Je contrôle : {eq(10-v,"+",v)}.',eq(10,'-',v))
    if code==12 and nums[1]>=0:
        qs[2]=q(f'Calcule {form(f"{a}+2")}.','Avancer de deux nombres.',f'Après {a}, je dis {a+1}, puis {a+2}. {eq(a,"+",2)}.',eq(a,'+',2))
        v=20 if nums[1]==10 else 10
        qs[3]=q(f'Calcule {form(f"{a}+{v}")}.','Ajouter des dizaines.',add_reason((a,v)),eq(a,'+',v))
    if code==12 and i==8:qs[3]=q('Calcule $46-20$.','Retirer deux dizaines.',sub_reason(46,20),eq(46,'-',20))
    if code==14:qs[3]=q(f'Calcule {form(f"{a}+8")}.','Passer par la dizaine si elle est atteinte.',bridge(a,8),eq(a,'+',8))
    if code==11 and i==9:
        qs=[]
        for number in [68,84]:
            tens=number//10*10;units=number%10;half=number//2
            qs.append(q(f'Cherche la moitié de {number}. Décompose en {tens} et {units}.','Partager les dizaines, puis les unités.',f'La moitié de {tens} est {tens//2}. La moitié de {units} est {units//2}. {eq(tens//2,"+",units//2)}. Je vérifie : {eq(half,"+",half)}.',f'La moitié de {number} est {half}.'))
        qs.append(q('20 et 28 sont-ils les deux moitiés de 48 ? Explique.','Vérifier le total et l’égalité des parts.',f'{eq(20,"+",28)}. Le total convient. Mais les parts sont différentes. {eq(24,"+",24)}.','Non. La moitié de 48 est 24.'))
        qs.append(q('Sam trouve 22 pour la moitié de 46. Corrige par décomposition.','Partager 40 et 6 séparément.',f'La moitié de 40 est 20. La moitié de 6 est 3. {eq(20,"+",3)}. Je contrôle : {eq(23,"+",23)}.','La moitié de 46 est 23.'))
    return qs
def run(codes=CODES):
  for code in codes:
    d=next(ROOT.glob(f'{code:02}_*'));src=json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf-8'))
    if code==14:src['vigilance']='Écris chaque étape séparément. Le signe égal relie toujours deux quantités égales.'
    figures={};corr={'cours':{'nouveau':{}},'fiches':{'nouvelle':{}},'exercices':{}}
    def put(name,tikz):figures[name]=tikz;return {'fichier':name+'.png','alt':'Schéma de calcul : '+name.replace('_',' ')}
    def diagram(nums,done=False):
      a,b=nums[:2]
      if code==4:return dots(a,b,done)
      if code==5:return dots(a,b,done,True)
      if code==6:return frame(a,done)
      if code==11:return dots(a,b,done)
      if code==12:return base(a,done=done,extra=b)
      if code==14:return jumps(a,b,done)
      if code==15:return tree(a,b,done)
      if code==16:return base(a,remove=b,done=done)
      return column(nums,done)
    course_seed={4:(3,2),5:(7,3),6:(6,4),11:(4,4),12:(36,10),14:(28,5),15:(27,36),16:(40,6),30:(28,35)}[code]
    mainfig=put('cours_modele',diagram(course_seed,True));corr['cours']['nouveau']['1']=mainfig;corr['fiches']['nouvelle']['1']=mainfig
    source_lessons='\n'.join('- '+x for x in src['lecon'])
    c=f'Titre: {TITRES[code]}\n\n<!-- optitab:1 -->\n::: objectifs\n{src["objectif"]}\nJe raconte ma méthode. Je vérifie mon résultat.\n:::\n\n## I. Manipuler pour comprendre\n\n::: methode Avec des objets\n{src["materiel"]}\n\n{src["manipulation"]}\n:::\n\n::: definition Les mots du calcul\n{source_lessons}\n:::\n\n## II. Une méthode pas à pas\n\n[IMAGE_1]\n\n::: exemple\n{src["exemple"]}\n\n{special_reason(code,0,src,course_seed)}\n:::\n\n## III. À toi de jouer\n\n::: methode Essaie avant de lire\n{src["guide"]}\n:::\n\n::: exemple Pour vérifier\n{src["guide_reponse"]}\n:::\n\n::: attention\n{src["vigilance"]}\n:::\n\n::: retenir\n{src["lecon"][-1]}\nJe peux utiliser des jetons pour expliquer.\n:::\n'
    if code==6:c+='\n'+table(['Première part','Autre part','Total'],[[str(n),str(10-n),'10'] for n in range(6)])+'\n'
    if code==11:c+='\n'+table(['Nombre','Double'],[[str(n),str(n+n)] for n in [1,2,3,4,5,6,7,8,9,10,20,30,40,50]])+'\nLa moitié permet de lire ce tableau dans l’autre sens.\n'
    if code in (12,30):c+='\n::: remarque Quand travailler ces calculs ?\n'+('Les calculs avec des nombres plus grands que 59 se reprennent après l’étude des nombres jusqu’à 100.' if code==12 else 'L’addition posée se travaille en fin de CP, après les méthodes de calcul mental.')+'\n:::\n'
    if code==30:c+='\n::: notation Les colonnes du modèle\nC signifie centaines. D signifie dizaines. U signifie unités.\n:::\n'
    (d/'cours_nouveau.txt').write_text(c,encoding='utf-8')
    f=f'Titre: {TITRES[code]}\n\n<!-- optitab:1 -->\n::: objectifs\n{src["objectif"]}\n:::\n\n## I. Je retiens\n\n::: retenir\n{source_lessons}\n:::\n\n[IMAGE_1]\n\n## II. Je fais et je vérifie\n\n::: methode\n{special_reason(code,0,src,course_seed)}\n:::\n\n::: attention\n{src["vigilance"]}\n:::\n'
    if code==30:f+='\n::: notation Les colonnes\nC signifie centaines. D signifie dizaines. U signifie unités.\n:::\n'
    (d/'fiche_nouvelle.txt').write_text(f,encoding='utf-8')
    items=[]
    for i,(source,nums) in enumerate(zip(src['exercices'],SEEDS[code]),1):
      prompt=source['consigne'].replace('L’adulte dit 0, puis 3, puis 6. Donne à chaque fois','Lis les nombres 0, 3 et 6. Donne pour chacun').replace('À reprendre après 100 :','Après l’étude des nombres jusqu’à 100 :').replace('Après 100 :','Après l’étude des nombres jusqu’à 100 :')
      if code==15 and i==9:prompt='Maya calcule 58 + 24. Elle annonce 712. Explique son erreur. Donne le bon total.'
      reason=special_reason(code,i,src,nums)
      # Reprendre la réponse source entièrement ; le raisonnement explique le premier cas.
      result=source['reponse']
      if code==6 and i==9:result='Les deux boîtes contiennent : '+ ' ; '.join(f'{n} et {10-n}' for n in range(11))+'.'
      if code==11 and i==9:reason=special_reason(code,9,src,nums)
      if code==4 and i==9:reason='Je compte chaque côté. '+eq(4,'+',2)+'. '+eq(5,'+',1)+'. Les deux côtés valent 6. Le signe égal convient.'
      if code==5 and i==9:reason='Je pars de 5 cubes. J’en enlève 2. '+sub_reason(5,2)+' Le premier nombre doit être la quantité de départ.'
      if code==6 and i==9:reason='Je commence avec zéro jeton dans la première boîte et dix dans l’autre. Je déplace un jeton à la fois vers la première boîte. Je trouve 0 et 10, puis 1 et 9, puis 2 et 8. Je continue jusqu’à 10 et 0. Le total reste dix. Le premier nombre passe par tous les nombres de 0 à 10 : je n’oublie aucun partage.'
      if code==6 and i==6:reason='Pour chaque nombre, je cherche les places encore libres. '+eq(0,'+',10)+'. '+eq(3,'+',7)+'. '+eq(6,'+',4)+'.'
      if code==15 and i==9:reason=add_reason(nums)+' On additionne 70 et 12. On ne colle pas les chiffres.'
      if code==30 and i==9:reason='Le 5 est un nombre d’unités. Je le place sous le 4. '+col_reason(nums)
      intro='Tu peux prendre des jetons. Explique tes gestes avec des mots.'
      hasfigure=i==1 or (code in (4,5) and i==3) or (code==12 and i==3) or (code==16 and i in (4,5,6,9)) or code==30
      if hasfigure:
        if code==11 and max(nums)>10:raise AssertionError('grand groupe à dessiner')
        m={};m['1']=put(f'ex{i}_modele',diagram(nums,False));m['2']=put(f'ex{i}_corrige',diagram(nums,True));corr['exercices'][f'nouveau-{i}']=m
        intro+='\n\n[IMAGE_1]'
        reason+='\n\n[IMAGE_2]'
      questions=[q(prompt,'Manipuler et calculer dans l’ordre.',reason,result)]+enrich(code,nums,i)
      # Les résultats de calcul sont aussi explicitement recalculables dans le texte final.
      if source['check']:
        checks=[]
        for term in source['check'].split(' and '):
          left,right=term.split('==')
          if '*' in left:
            n=int(left.split('*')[1]);checks.append(f'Deux parts de {n} : {eq(n,"+",n)}');continue
          if '//' in left:
            if '+' in left:continue
            n=int(left.split('//')[0]);h=n//2;checks.append(f'Deux parts égales de {h} : {eq(h,"+",h)}');continue
          checks.append(form(left+'='+right))
        if checks:questions[0]['etapes'].append('Je vérifie les calculs : '+ ' ; '.join(checks)+'.')
      items.append(ex(f'{src["titre"]} : atelier {i}',intro,questions))
    write(code,items)
    (d/'figures/figures.py').write_text('# -*- coding: utf-8 -*-\n"""Figures TikZ de calcul CP, sans réponses dans les modèles."""\nFIGURES = '+repr(figures)+'\n',encoding='utf-8')
    (d/'figures/correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    coverage='# Couverture des activités sources\n\nChaque ligne conserve l’activité entière dans la question 1. Les questions 2 à 5 renforcent le même savoir-faire.\n\n'+table(['Source','Exercice final','Activité conservée'],[[str(i),f'nouveau-{i}',s['consigne']] for i,s in enumerate(src['exercices'],1)])+'\n\nLa manipulation, les trois points de leçon, l’exemple, le guidage et la vigilance sont repris dans le cours.\n'
    (d/'COUVERTURE.md').write_text(coverage,encoding='utf-8')
    (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'cp_calculs','maj':'2026-11-02'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':run(list(map(int,sys.argv[1:])) or CODES)
