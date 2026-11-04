"""Révision éditoriale locale 261–265. Aucune connexion à la base."""
from pathlib import Path
from fractions import Fraction as F
import json
import re
import math

ROOT = Path(__file__).resolve().parent.parent
MARK = '<!-- optitab:1 -->'

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + '\n', encoding='utf-8')

def num(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    if x.denominator & (x.denominator - 1) == 0 or 10**8 % x.denominator == 0:
        return f'{float(x):.8f}'.rstrip('0').rstrip('.').replace('.', '{,}')
    return rf'\frac{{{x.numerator}}}{{{x.denominator}}}'

def frac(a, b):
    return rf'\frac{{{a}}}{{{b}}}'

def eq(s):
    if s.count('=') >= 2 and not any(x in s for x in ('<','>',r'\le',r'\ge',r'\quad',r'\begin')):
        first, *rest = s.split('=')
        s = r'\begin{aligned}' + first + '&=' + (r'\\&='.join(rest)) + r'\end{aligned}'
    return '$$' + s + '$$'

def box(kind, text, title=''):
    return f'::: {kind}' + (' ' + title if title else '') + '\n' + text + '\n:::'

def questions(statement):
    return re.findall(r'^\d+\. (.+)$', statement, re.M)

def make_ex(header, statement, methods, workings, answers, note, image=None):
    qs = questions(statement)
    assert len(qs) == len(methods) == len(workings) == len(answers) == 6
    steps = []
    for i, (q, m, w, a) in enumerate(zip(qs, methods, workings, answers), 1):
        steps.append(f'## Question {i} : {q}\n\n' + box('methode', m) + '\n\n' + box('etape', w, 'Raisonner et calculer') + '\n\n' + box('resultat', a))
    if image:
        steps.append(image)
    steps.append(box('retenir', note))
    return header.rstrip() + '\n\nÉnoncé:\n' + MARK + '\n' + statement.strip() + '\n\nÉtapes:\n' + MARK + '\n' + '\n\n'.join(steps) + '\n\nSolution:\n' + MARK + '\n' + '\n'.join(f'{i}. {a}' for i, a in enumerate(answers, 1))

def numberline(points, lo, hi, corrected=False):
    unit = 7.0 / (hi-lo)
    lines = [rf'\begin{{tikzpicture}}[x={unit:.6f}cm,y=1cm]', rf'\draw[geoVecteur] ({lo-.4},0)--({hi+.6},0);']
    for x in range(lo, hi+1):
        lines.append(rf'\draw[otMuted] ({x},-.06)--({x},.06);')
    for label, x in points:
        color = 'otGreenDark' if 'D' in label else 'otNavy'
        lines += [rf'\fill[{color}] ({x},0) circle (1.8pt);', rf'\node[above=7pt,text={color}] at ({x},0) {{${label}$}};', rf'\node[below=7pt,text=otMuted] at ({x},0) {{${x}$}};']
    lines.append(r'\end{tikzpicture}')
    return '\n'.join(lines)

def bars(a, b, c, d):
    # Même unité de référence, deux barres exactement de même longueur.
    lines = [r'\begin{tikzpicture}[x=1cm,y=1cm]']
    for name, n, den, y in [('Alice',a,b,1),('Bilal',c,d,0)]:
        lines += [rf'\node[anchor=west,text=otInk] at (0,{y+.65}) {{{name} : ${frac(n,den)}$}};', rf'\fill[otNavy!18] (0,{y}) rectangle ({7*n/den},{y+.35});', rf'\draw[geoTrait] (0,{y}) rectangle (7,{y+.35});']
        for i in range(1,den):
            lines.append(rf'\draw[otMuted,line width=.35pt] ({7*i/den},{y})--({7*i/den},{y+.35});')
    lines += [r'\end{tikzpicture}']
    return '\n'.join(lines)

def revise(p):
    n = int(p.name[:3])
    write(p/'etat.json', json.dumps({'statut':'en_cours','agent':'calculs','maj':'2026-10-28'},ensure_ascii=False,indent=2))
    meta = json.loads((p/'source_en_ligne/meta.json').read_text(encoding='utf8'))
    source = (p/'exercices.txt').read_text(encoding='utf8')
    blocks = [b.strip() for b in re.split(r'^===[ \t]*$', source, flags=re.M) if re.search(r'^Id:',b,re.M)]
    assert len(blocks) == 21
    figs = {}
    corr = {'cours':{},'fiches':{},'exercices':{}}
    revised = []
    for b in blocks:
        header, content = b.split('Énoncé:',1)
        eid = int(re.search(r'^Id: (\d+)',header,re.M)[1])
        statement = content.split('Étapes:')[0].replace(MARK,'').strip()
        statement = re.sub(r'\n?\[IMAGE_\d+\]\n?', '\n', statement)
        statement = re.sub(r'\n{3,}', '\n\n', statement)
        if n == 263:
            statement = statement.replace('une abscisse négative ?', 'une abscisse strictement négative ?')
        old_steps = content.split('Étapes:',1)[1].split('Solution:',1)[0]
        # Tous les anciens appels sont remplacés explicitement ou retirés.
        header = re.sub(r'^Image:.*\n?', '', header, flags=re.M)
        note = ''
        if n == 261 and 'Un club prépare' in statement:
            vals = re.search(r'prépare (\d+) ateliers.*?reçoit (\d+) carnets.*?et (\d+) carnets.*?coûte \$(.*?)\$.*?dispose de \$(.*?)\$',statement,re.S)
            k,a,c = map(int,vals.group(1,2,3)); price,budget = [F(s.replace('{,}','.')) for s in vals.group(4,5)]
            count=k*(a+c); cost=count*price; total=cost+6
            methods=['Additionner les deux effectifs de carnets.','Multiplier le nombre par atelier par le nombre d’ateliers.','Traduire les regroupements avant de calculer.','Ajouter la livraison une seule fois.','Soustraire le coût total du budget.','Comparer les frais comptés à tort aux frais réels.']
            workings=[eq(f'{a}+{c}={a+c}'),eq(rf'{k}\times({a}+{c})={k}\times{a+c}={count}'),eq(rf'{k}\times({a}+{c})\times {num(price)}={count}\times {num(price)}={num(cost)}'),eq(f'{num(cost)}+6={num(total)}'),eq(f'{num(budget)}-({num(cost)}+6)={num(budget)}-{num(total)}={num(budget-total)}'),eq(rf'{k}\times6-6={6*k}-6={6*k-6}')]
            answers=[f'{a+c} carnets.',f'{count} carnets.',f'${k}\\times({a}+{c})\\times {num(price)}={num(cost)}$ €.',f'${num(total)}$ €.',f'${num(budget-total)}$ €.',f'{6*k-6} € de trop.']
            note='Les parenthèses regroupent les besoins d’un atelier. La livraison concerne toute la commande.'
        elif n == 261:
            vals = re.findall(r'\$(.*?)\$',statement)[:2]; v,c = [F(x.replace('{,}','.')) for x in vals]
            q=int(v//c); rem=v-q*c
            methods=['Diviser le volume total par la capacité d’une bouteille.','Multiplier les deux nombres par 100.','Encadrer le volume par deux multiples de la capacité.','Soustraire le volume déjà versé.','Prévoir une bouteille supplémentaire pour le reste.','Compléter la dernière bouteille jusqu’à sa capacité.']
            workings=[f'Chaque bouteille contient ${num(c)}$ L : on cherche combien de fois cette quantité entre dans ${num(v)}$ L.',eq(rf'{num(v)}\div {num(c)}={num(100*v)}\div {num(100*c)}'),eq(rf'{q}\times {num(c)}={num(q*c)}\le {num(v)}<{num((q+1)*c)}'),eq(f'{num(v)}-{num(q*c)}={num(rem)}'),f'Le reste est ${num(rem)}$ L, strictement positif. Les {q} bouteilles pleines ne suffisent donc pas.',eq(f'{num(c)}-{num(rem)}={num(c-rem)}')]
            answers=[f'${num(v)}\\div {num(c)}$.',f'${num(100*v)}\\div {num(100*c)}$.',f'{q} bouteilles.',f'${num(rem)}$ L.',f'{q+1} bouteilles.',f'${num(c-rem)}$ L.']
            note='Un quotient théorique, un nombre de bouteilles pleines et un nombre de bouteilles nécessaires répondent à trois questions différentes.'
        elif n == 262 and 'association' in statement:
            a,c=map(int,re.search(r'ranger (\d+) objets.*?maximum (\d+) objets',statement,re.S).groups()); q,r=divmod(a,c); nb=q+bool(r); missing=nb*c-a
            methods=['Chercher deux multiples consécutifs du diviseur.','Décomposer en boîtes pleines et objets restants.','Vérifier les deux bornes imposées au reste.','Tenir compte du reste pour ranger tous les objets.','Comparer la capacité totale au nombre d’objets.','Vérifier la divisibilité, puis compléter au multiple suivant.']
            workings=[eq(rf'{c}\times{q}={c*q}\le {a}<{c*(q+1)}={c}\times{q+1}'),eq(rf'{a}={c}\times{q}+{r}'),eq(rf'0\le {r}<{c}'),f'Il reste {r} objet(s) après les {q} boîtes pleines : '+eq(f'{q}+1={nb}'),eq(rf'{nb}\times{c}-{a}={nb*c}-{a}={missing}'),f'Le reste vaut {r}, donc il est non nul. '+eq(f'{a}+{missing}={nb*c}')]
            answers=[f'${c*q}\\le {a}<{c*(q+1)}$.',f'Quotient {q} ; reste {r}.',f'$0\\le {r}<{c}$ : le reste convient.',f'{nb} boîtes.',f'{missing} places.',f'Non ; ajouter {missing} objets permet d’obtenir {nb*c} objets.']
            note='Dans une division euclidienne, le reste est toujours inférieur au diviseur. Une boîte partiellement remplie compte comme une boîte.'
        elif n == 262 and 'cartes rouges' in statement:
            a,c=map(int,re.search(r'possède (\d+) cartes rouges et (\d+) cartes bleues',statement).groups()); da=[d for d in range(1,a+1) if a%d==0]; dc=[d for d in range(1,c+1) if c%d==0]; common=sorted(set(da)&set(dc)); g=max(common); ds=sum(map(int,str(a)))
            methods=['Appliquer les critères de divisibilité par 2 et par 3.','Partager chaque couleur séparément en six.','Énumérer les diviseurs de chaque effectif.','Lire le plus grand diviseur commun dans la liste.','Partager chaque couleur entre les lots retenus.','Vérifier la composition de chaque lot, couleur par couleur.']
            workings=[f'{a} est pair. La somme de ses chiffres vaut {ds}, multiple de 3. '+eq(rf'{a}\div2={a//2}\quad;\quad {a}\div3={a//3}'),eq(rf'{a}\div6={a//6}\quad;\quad {c}\div6={c//6}'),f'Diviseurs de {a} : '+', '.join(map(str,da))+'.\n\n'+f'Diviseurs de {c} : '+', '.join(map(str,dc))+'.\n\nOn conserve seulement les nombres présents dans les deux listes.',f'La liste commune est '+', '.join(map(str,common))+f'. Son maximum est {g}.',eq(rf'{a}\div{g}={a//g}\quad;\quad {c}\div{g}={c//g}'),f'Par exemple, {a+c} divise le total {a+c}, mais il est supérieur à chacun des deux effectifs : on ne peut pas répartir une carte de chaque couleur dans chacun de ces lots.']
            answers=[f'Oui : {a} est pair et sa somme de chiffres vaut {ds}, multiple de 3.',f'Oui : {a//6} cartes rouges et {c//6} cartes bleues par lot.',', '.join(map(str,common))+'.',f'{g} lots.',f'{a//g} cartes rouges et {c//g} cartes bleues par lot.','Le nombre de lots doit diviser chacun des deux effectifs, pas seulement leur somme.']
            note='Des lots identiques sans reste imposent un diviseur commun aux effectifs de toutes les catégories.'
        elif n == 262:
            a,c=map(int,re.search(r'toutes les (\d+) secondes.*?toutes les (\d+) secondes',statement).groups()); t=math.lcm(a,c)
            la=[a*i for i in range(1,t//a+1)]; lc=[c*i for i in range(1,t//c+1)]
            methods=['Écrire les cinq premiers multiples strictement positifs.','Faire la même liste avec la seconde période.','Chercher le premier multiple strictement positif commun.','Diviser l’instant commun par chaque période.','Ajouter chaque fois la durée du cycle commun.','Tester si la somme est un multiple de chaque période.']
            workings=[eq(rf'{a}\times1={a},\quad {a}\times2={2*a},\quad\ldots,\quad {a}\times5={5*a}'),eq(rf'{c}\times1={c},\quad {c}\times2={2*c},\quad\ldots,\quad {c}\times5={5*c}'),f'Jusqu’à la première rencontre :\n\n- Premier signal : '+', '.join(map(str,la))+'.\n- Second signal : '+', '.join(map(str,lc))+'.',eq(rf'{t}\div{a}={t//a}\quad;\quad {t}\div{c}={t//c}'),eq(rf'{t}+{t}={2*t}\quad;\quad {2*t}+{t}={3*t}'),('Ici, la somme fonctionne, mais elle ne donne pas nécessairement le premier instant commun. ' if (a+c)%a==0 and (a+c)%c==0 else f'Ici, {a}+{c}={a+c} n’est pas divisible par les deux périodes. ')+r'Contre-exemple général : pour des périodes de 4 s et 6 s, la somme 10 s n’est multiple ni de 4 ni de 6.']
            answers=[', '.join(str(a*i) for i in range(1,6))+' s.',', '.join(str(c*i) for i in range(1,6))+' s.',f'{t} s.',f'{t//a} période(s) du premier ; {t//c} du second.',f'{2*t} s et {3*t} s.','Une rencontre exige un multiple des deux périodes ; leur somme n’a pas toujours cette propriété.']
            note='Pour des rendez-vous périodiques, chercher des multiples communs ; pour des partages sans reste, chercher des diviseurs communs.'
        elif n == 263:
            a,c,d=map(int,re.search(r'abscisses (-?\d+), (-?\d+) et (-?\d+)',statement).groups()); pts={'A':a,'B':c,'C':d,'O':0}; order=sorted(pts,key=lambda z:-abs(pts[z])); groups=[]
            for distance in sorted(set(abs(v) for v in pts.values()),reverse=True):
                groups.append(' et '.join(k for k in pts if abs(pts[k])==distance))
            ties=[' et '.join(k for k in pts if abs(pts[k])==dist) for dist in set(map(abs,pts.values())) if sum(abs(v)==dist for v in pts.values())>1]
            rank=' ; puis '.join(groups)+'. '+('À égalité : '+ ' ; '.join(ties)+'.' if ties else 'Aucune égalité.')
            methods=['Repérer les abscisses strictement inférieures à zéro.','Lire la droite de gauche à droite.','Mesurer le nombre d’unités entre le point et l’origine.','Garder la distance à zéro et changer de côté.','Additionner les distances à zéro de deux points de côtés opposés.','Comparer les distances à zéro, sans conserver le signe.']
            workings=[f'$a_A={a}<0$ et $a_C={d}<0$ ; $a_B={c}>0$ et $a_O=0$.',eq('<'.join(map(str,sorted(pts.values())))),f'De ${a}$ à $0$, on parcourt ${-a}$ unités. Une distance est positive ou nulle.',f'L’opposé de ${a}$ est ${-a}$ : les deux nombres sont de part et d’autre de zéro à la même distance.',eq(f'{-a}+{c}={c-a}'), '| Point | $A$ | $B$ | $C$ | $O$ |\n|---|---|---|---|---|\n'+f'| Distance à zéro | ${abs(a)}$ | ${abs(c)}$ | ${abs(d)}$ | $0$ |\n\nDeux distances égales donnent une égalité dans le classement.']
            answers=['$A$ et $C$.','$'+'<'.join(map(str,sorted(pts.values())))+'$.',f'{-a} unités.',f'$D$ a pour abscisse ${-a}$.',f'{c-a} unités.',rank]
            note='Le classement des abscisses et celui des distances à zéro ne répondent pas à la même question.'
            name=f'droite_{eid}'; figs[name]=numberline([(k,v) for k,v in pts.items()],a-1,c+1)
            statement=statement.replace('\n\n1.', '\n\n[IMAGE_1]\n\n1.',1)
            corr['exercices'][str(eid)]={'1':{'fichier':name+'.png','alt':f'Droite graduée : A({a}), C({d}), O(0) et B({c}), unité constante.'}}
        elif n == 264:
            initial,up,down=map(int,re.search(r'de (-?\d+) °C.*?de (\d+) °C.*?de (\d+) °C',statement).groups()); noon=initial+up; final=noon-down; delta=final-initial
            signed=lambda x: '+'+str(x) if x>0 else str(x)
            methods=['Associer une hausse à une variation positive.','Ajouter la hausse à la température initiale.','Associer une baisse à une variation négative.','Ajouter la variation de l’après-midi à la température de midi.','Calculer valeur finale moins valeur initiale.','Calculer valeur initiale moins valeur finale.']
            workings=[f'Le mot « augmente » indique le signe $+$ ; la distance de cette variation à zéro est ${up}$.',eq(f'({initial})+(+{up})={noon}'),f'Le mot « baisse » indique le signe $-$ ; la variation est donc ${-down}$ °C.',eq(f'({noon})+(-{down})={noon}-{down}={final}'),eq(f'({final})-({initial})={final}+{-initial}={signed(delta)}')+'\n\nContrôle par les variations : '+eq(f'{up}-{down}={signed(delta)}'),eq(f'({initial})-({final})={signed(-delta)}')+f'\n\nCette variation est l’opposée de ${signed(delta)}$ °C.']
            answers=[f'$+{up}$ °C.',f'${noon}$ °C.',f'${-down}$ °C.',f'${final}$ °C.',f'${signed(delta)}$ °C.',f'${signed(-delta)}$ °C.']
            note='Une température est une valeur ; une variation est une différence. Pour revenir à la valeur de départ, prendre la variation opposée.'
        elif n == 265 and 'Un atelier possède' in statement:
            total,a,c=map(int,re.search(r'possède (\d+) L.*?\\frac\{(\d+)\}\{(\d+)\}',statement).groups()); part=F(total,c); taken=part*a; left=F(c-a,c)
            methods=['Identifier le partage de l’unité et les parts prises.','Multiplier les deux termes par le même nombre non nul.','Diviser la quantité totale en parts égales.','Multiplier une part par le nombre de parts réservées.','Retirer de l’unité les parts réservées.','Comparer le double du numérateur au dénominateur.']
            workings=[f'La réserve initiale constitue l’unité. On la partage en {c} parts égales et on en réserve {a}.',eq(frac(a,c)+'='+frac(a*2,c*2)),eq(rf'{total}\div {c}={num(part)}'),eq(rf'{total}\div {c}\times {a}={num(part)}\times {a}={num(taken)}'),eq(frac(c,c)+'-'+frac(a,c)+'='+frac(c-a,c)+'='+num(left)),eq(rf'2\times {a}={2*a}'+('>' if 2*a>c else '=' if 2*a==c else '<')+str(c))+'\n\n'+('La fraction est strictement supérieure à un demi.' if 2*a>c else 'La fraction vaut exactement un demi : elle ne dépasse pas la moitié.' if 2*a==c else 'La fraction est strictement inférieure à un demi.')]
            answers=[f'{c} parts égales ; {a} part'+(' est réservée.' if a==1 else 's sont réservées.'),'$'+frac(a*2,c*2)+'$.',f'${num(part)}$ L.',f'${num(taken)}$ L.','$'+frac(c-a,c)+'$'+(' (soit $'+num(left)+'$).' if F(c-a,c).denominator!=c else '.'),('Oui' if 2*a>c else 'Non')+' : $'+frac(a,c)+('>' if 2*a>c else '=' if 2*a==c else '<')+frac(1,2)+'$.']
            note='Toujours préciser l’unité de référence. Pour prendre une fraction d’une quantité, diviser par le dénominateur puis multiplier par le numérateur.'
        else:
            vals=re.findall(r'\\frac\{(\d+)\}\{(\d+)\}',statement); (a,c),(d,e)=[tuple(map(int,v)) for v in vals]; length=int(re.search(r'mesurait (\d+) cm',statement)[1]); aa=a*(e//c); diff=F(aa-d,e)
            methods=['Vérifier que les deux fractions concernent la même unité.','Multiplier numérateur et dénominateur par 2.','Comparer les numérateurs de parts devenues identiques.','Soustraire les numérateurs au même dénominateur.','Calculer séparément la fraction de la longueur pour chacun.','Donner un contre-exemple avec le même numérateur.']
            workings=['Un quart de 8 cm vaut 2 cm, mais un quart de 12 cm vaut 3 cm. Une même fraction ne donne donc pas toujours la même longueur.',eq(frac(a,c)+'='+frac(2*a,2*c)),eq(frac(aa,e)+'>'+frac(d,e))+f'\n\nLes parts ont la même taille et ${aa}>{d}$.',eq(frac(aa,e)+'-'+frac(d,e)+'='+frac(aa-d,e)+'='+num(diff)),eq(r'\begin{aligned}'+rf'L_A&={length}\div {c}\times {a}={num(F(length*a,c))}\\L_B&={length}\div {e}\times {d}={num(F(length*d,e))}'+r'\end{aligned}'),eq(frac(1,4)+'<'+frac(1,2))+'\n\nPartager la même unité en davantage de parts égales rend chacune plus petite.']
            answers=['Les fractions doivent représenter des parts de la même longueur initiale.','$'+frac(a,c)+'='+frac(aa,e)+'$.',f'Alice, car ${aa}>{d}$ à dénominateur commun.','$'+frac(aa-d,e)+'='+num(diff)+'$.',f'Alice : ${num(F(length*a,c))}$ cm ; Bilal : ${num(F(length*d,e))}$ cm.','Non : $'+frac(1,4)+'<'+frac(1,2)+'$, bien que $4>2$.']
            note='Comparer des fractions exige des parts comparables. Le numérateur ou le dénominateur seul ne suffit pas.'
            name=f'rubans_{eid}'; figs[name]=bars(a,c,d,e)
            statement=statement.replace('\n\n1.', '\n\n[IMAGE_1]\n\n1.',1)
            corr['exercices'][str(eid)]={'1':{'fichier':name+'.png','alt':f'Rubans de même longueur : Alice utilise {a}/{c} et Bilal {d}/{e}.'}}
        revised.append(make_ex(header,statement,methods,workings,answers,note))
    write(p/'exercices.txt','\n\n===\n\n'.join(revised))
    write(p/'figures/figures.py', '# -*- coding: utf-8 -*-\n"""Figures TikZ de la notion ; compilation par outils/figures_livre.py."""\nFIGURES = '+repr(figs))
    write(p/'figures/correspondance.json',json.dumps(corr,ensure_ascii=False,indent=2))
    print(n,':',len(revised),'exercices ;',len(figs),'figures')

if __name__=='__main__':
    for p in sorted(ROOT.iterdir()):
        if p.name[:3] in {'261','262','263','264','265'}:
            revise(p)
