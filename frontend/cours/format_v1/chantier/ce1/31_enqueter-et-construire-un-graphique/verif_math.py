# -*- coding: utf-8 -*-
"""Contrôle autonome : relit les textes livrés et recalcule avec Fraction.

Aucun import du générateur, du helper, des outils du site ou de la base.
"""
from pathlib import Path
from fractions import Fraction
import ast,json,re,hashlib
D=Path(__file__).resolve().parent
CODE=int(D.name[:2])

def value(s):
    s=s.replace(r'\times','*').replace(r'\,','').replace(' ','')
    old=None
    while old!=s:
        old=s;s=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
    if not re.fullmatch(r'[0-9()+*/.\-]+',s):raise ValueError(s)
    tree=ast.parse(s,mode='eval')
    def ev(x):
        if isinstance(x,ast.Expression):return ev(x.body)
        if isinstance(x,ast.Constant) and isinstance(x.value,(int,float)):return Fraction(str(x.value))
        if isinstance(x,ast.UnaryOp) and isinstance(x.op,ast.USub):return -ev(x.operand)
        if isinstance(x,ast.BinOp):
            a,b=ev(x.left),ev(x.right)
            if isinstance(x.op,ast.Add):return a+b
            if isinstance(x.op,ast.Sub):return a-b
            if isinstance(x.op,ast.Mult):return a*b
            if isinstance(x.op,ast.Div):return a/b
        raise ValueError(ast.dump(x))
    return ev(tree)

files={name:(D/name).read_text(encoding='utf8') for name in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt']}
count=0
for name,text in files.items():
    assert text.count(':::')%2==0,(name,'encadrés')
    assert not any(bad in text for bad in ['cat?gorie','P1','P2','avec l’adulte','\ufffd']),name
    for formula in re.findall(r'\$([^$]+)\$',text):
        if not any(sign in formula for sign in ['=','<','>']):continue
        pieces=re.split(r'(=|<|>)',formula)
        try:vals=[value(p) for p in pieces[::2]]
        except (ValueError,SyntaxError):continue # opération encore à compléter, mots ou variable
        for i,sign in enumerate(pieces[1::2]):
            a,b=vals[i:i+2]
            assert {'=':a==b,'<':a<b,'>':a>b}[sign],(name,formula,a,b)
            count+=1
    for a,b in re.findall(r'\\frac\{(\d+)\}\{(\d+)\}',text):
        assert int(b) in [2,3,4,5,6,8,10],(name,'dénominateur',b)
        assert 0<=int(a)<=int(b),(name,'fraction hors du tout',a,b)

text=files['exercices.txt'];blocks=re.split(r'^===\s*$',text,flags=re.M)[1:]
assert len(blocks)==9,len(blocks)
answers={}
for i,block in enumerate(blocks,1):
    assert re.search(rf'^Id: nouveau-{i}$',block,re.M)
    en,steps=block.split('Énoncé:\n',1)[1].split('Étapes:\n')
    steps,sol=steps.split('Solution:\n')
    assert len(re.findall(r'^\d\. ',en,re.M))==5,(i,'questions énoncé')
    assert len(re.findall(r'^## Question \d :',steps,re.M))==5,(i,'questions corrigé')
    results=re.findall(r'::: resultat\n(.*?)\n:::',steps,re.S)
    assert len(results)==5 and steps.count('::: methode')==5 and steps.count('::: etape')>=5,i
    expected='<!-- optitab:1 -->\n'+'\n'.join(f'{j}. {a}' for j,a in enumerate(results,1))
    assert sol.strip()==expected.strip(),(i,'solution et résultat divergent')
    for j,result in enumerate(results,1):answers[i,j]=result

independent=0
def check(i,j,expr,denominator=None):
    global independent
    expected=value(expr);assert expected.denominator==1,(i,j,expr)
    token=str(expected.numerator)
    if denominator is not None:
        token=r'\frac{'+token+'}{'+str(denominator)+'}'
        assert token in answers[i,j],(i,j,expr,answers[i,j])
    else:assert re.search(r'(?<!\d)'+re.escape(token)+r'(?!\d)',answers[i,j]),(i,j,expr,answers[i,j])
    independent+=1

if CODE==1:
    for i,v in [(1,325),(2,107),(3,508),(4,215),(7,427),(9,405)]:
        check(i,4,f'{v}+10');check(i,5,f'{v}-1');check(i,5,f'{v}+1')
    for i,j,expr in [(5,1,'398+1'),(5,1,'399+1'),(5,5,'401+1'),(6,2,'350+100'),(6,2,'350+200'),(6,2,'350+300'),(6,5,'(650-250)/100'),(8,1,'1000/100'),(8,2,'9*100'),(8,3,'1000-900'),(8,5,'8*100+20*10')]:check(i,j,expr)
elif CODE==2:
    for i,v in enumerate([416,627,280,305,789,583,236,297,407],1):
        check(i,2,f'{v//100}*100+{v%10}');check(i,4,str(v//10));check(i,5,f'{v}-10')
elif CODE==3:
    for i,j,e in [(1,1,'400+20'),(1,1,'400+50'),(1,1,'400+80'),(1,2,'(500-400)/10'),(1,3,'450-10'),(1,4,'480+20'),(4,3,'568-560'),(4,4,'570-568'),(5,1,'799+1'),(5,1,'802-1'),(5,4,'802-799-1'),(6,1,'6*100'),(6,2,'600-100'),(6,3,'600+200'),(6,4,'(1000-600)/100'),(7,3,'400-398'),(7,4,'403-400'),(7,5,'403-398'),(8,1,'241-240'),(8,2,'242+4'),(8,3,'242-4'),(8,5,'246-238'),(9,4,'500-490'),(9,5,'509-490')]:check(i,j,e)
elif CODE==4:
    for i,j,e in [(2,1,'63-1'),(2,4,'69+1'),(2,5,'70-63'),(3,1,'99+1'),(3,3,'100-1'),(3,4,'105-100'),(3,5,'100+1'),(5,1,'145+10'),(5,1,'145+20'),(5,3,'165+10'),(6,1,'16*2'),(6,1,'16*4'),(6,3,'64*2'),(7,1,'1+11*2'),(7,3,'23+2'),(8,1,'11+5'),(8,1,'11+5+6'),(8,3,'22+7'),(9,1,'100-37'),(9,2,'37-1'),(9,4,'37-1'),(9,5,'100-36')]:check(i,j,e)
    for i,motif,rank in [(1,'AB',39),(4,'ABC',60)]:
        assert 'lettre '+motif[(rank-1)%len(motif)] in answers[i,2]
        assert 'lettre '+motif[(rank-2)%len(motif)] in answers[i,3]
        assert 'lettre '+motif[rank%len(motif)] in answers[i,4]
        independent+=3
elif CODE==14:
    for i,e in enumerate(['360-145','238+174','500-367','186+57','302-48','125-89'],1):check(i,3,e)
    for i,j,e in [(1,5,'360-145-10'),(2,5,'238+174+8'),(3,5,'500-367-20'),(4,5,'186+57-50'),(5,5,'302-48+50'),(6,5,'89-10'),(7,2,'278+85'),(7,4,'278+85-350'),(8,3,'384+126'),(8,5,'384+126-100'),(9,3,'140+25'),(9,5,'140+25-30')]:check(i,j,e)
elif CODE==15:
    for i,e in enumerate(['125+28','238-196','175+46','304-78','140-95','125-125','38+12','63-9','240-185'],1):check(i,3,e)
    for i,delta in enumerate([28,42,46,78,45,0,12,9,55],1):check(i,5,'5' if i==6 else f'{delta}-5')
elif CODE==16:
    mids=['125+38','86+74','43-18','6*2','7*4','3+2','5*6','135+78','4*5']
    finals=['125+38-47','245-86-74','43-18+27','6*2+5','50-7*4','(3+2)*8','5*6+9','260-135-78','30-4*5']
    for i,(a,b) in enumerate(zip(mids,finals),1):check(i,2,a);check(i,4,b)
elif CODE==17:
    for i,(total,size,ceil) in enumerate([(36,4,False),(54,6,False),(80,10,False),(120,10,False),(25,10,True),(41,6,False),(150,5,False),(189,10,True),(75,6,False)],1):
        quotient,rem=divmod(total,size)
        check(i,2,f'{quotient}*{size}');check(i,3,f'{total}-{quotient}*{size}');check(i,4,str(quotient+int(ceil and rem>0)))
elif CODE==18:
    for i,b in [(1,5),(2,2),(3,3),(6,6),(8,4),(9,8)]:check(i,1,'1',b)
    check(7,4,'1',4);check(8,5,'1',3)
elif CODE==19:
    check(1,1,'3',8);check(1,5,'8-3');check(2,1,'3',4);check(2,5,'4-3');check(6,1,'5',5)
    check(7,1,'7',10);check(7,1,'4',10);check(9,1,'2',4);check(9,1,'1',2)
elif CODE==20:
    for i,a,c,b,op in [(1,1,3,6,'+'),(2,2,3,8,'+'),(3,5,2,6,'-'),(5,3,1,4,'+'),(6,4,3,10,'+'),(7,10,3,10,'-'),(8,1,2,4,'+')]:
        check(i,2,f'{a}{op}{c}');check(i,3,f'{a}{op}{c}',b);check(i,4,f'{b}-({a}{op}{c})',b)
    check(2,3,'4+2',10);check(3,3,'3-1',5);check(4,2,'5-2',5);check(4,3,'8-3',8);check(9,1,'1+3',6);check(9,2,'2+2',6);check(9,4,'6-4',6)
elif CODE==31:
    for i in range(1,10):check(i,2,'4+3+5' if i<=6 else '6+4+3')
    for i in [1,2,3,4,7,9]:check(i,5,'5-3' if i<=6 else '6-3')
    check(5,5,'12-11');check(6,5,'4+1+3+5');check(8,5,'6+4+3')
elif CODE==32:
    for i,j,e in [(1,1,'7'),(1,2,'8+5'),(1,3,'10+7'),(2,1,'8+5'),(3,1,'7-5'),(4,2,'4+3+6'),(4,3,'6-3'),(5,1,'4+3+6'),(6,1,'6-3'),(7,1,'10+7'),(8,2,'4+3+6'),(9,1,'5'),(9,2,'10+7')]:check(i,j,e)

# Chaque appel d’image doit avoir une correspondance, et inversement.
corr=json.loads((D/'figures/correspondance.json').read_text(encoding='utf8'))
for i,block in enumerate(blocks,1):
    assert set(re.findall(r'\[IMAGE_(\d+)\]',block))==set(corr['exercices'].get(f'nouveau-{i}',{})),('images',i)
assert set(re.findall(r'\[IMAGE_(\d+)\]',files['cours_nouveau.txt']))==set(corr['cours']['nouveau'])
figure_tree=ast.parse((D/'figures/figures.py').read_text(encoding='utf8'))
figs=ast.literal_eval(next(n.value for n in figure_tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FIGURES' for t in n.targets)))
shape_checks=0
if CODE in [18,19,20]:
    plans={18:{'cours_schema':[(1,4)],'ex1_schema':[(1,5)],'ex1_corrige':[(1,5)],'ex2_schema':[(0,2)],'ex2_corrige':[(1,2)],'ex3_schema':[(0,3)],'ex3_corrige':[(1,3)],'ex6_schema':[(1,6)],'ex6_corrige':[(1,6)],'ex7_schema':[(0,4)],'ex7_corrige':[(1,4)],'ex9_schema':[(0,8)],'ex9_corrige':[(1,8)]},19:{'cours_schema':[(2,5),(3,5)],'ex1_schema':[(3,8)],'ex1_corrige':[(3,8)],'ex2_schema':[(0,4)],'ex2_corrige':[(3,4)],'ex4_schema':[(1,3),(1,6)],'ex8_schema':[(1,2),(1,2)],'ex9_schema':[(2,4),(1,2)]},20:{'cours_schema':[(2,5),(1,5),(3,5)],'ex1_schema':[(1,6),(3,6)],'ex1_corrige':[(4,6)],'ex6_schema':[(0,10)],'ex6_corrige':[(7,10)]}}[CODE]
    for name,expected in plans.items():
        rows={}
        for color,x,y,right,top in re.findall(r'\\fill\[([^]]+)\] \(([-\d.]+),([-\d.]+)\) rectangle \(([-\d.]+),([-\d.]+)\);',figs[name]):
            rows.setdefault(Fraction(y),[]).append((color,Fraction(right)-Fraction(x)))
        actual=[]
        for y,row in sorted(rows.items(),reverse=True):
            actual.append((sum(color!='white' for color,width in row),len(row)))
            if not(CODE==18 and name=='ex7_schema'):
                widths=[w for color,w in row]
                assert float(max(widths)-min(widths))<1e-12,(name,'parts inégales')
        assert actual==expected,(name,actual,expected)
        shape_checks+=1
if CODE in [31,32]:
    for name,fig in figs.items():
        heights=[Fraction(y)/Fraction('0.43') for y in re.findall(r'\\draw\[draw=[^]]+\] \([\d.]+,0\) rectangle \([\d.]+,([\d.]+)\);',fig)]
        if CODE==32:expected=[4,3,6]
        elif name=='cours_schema':expected=[4,3,5]
        else:
            i=int(re.search(r'ex(\d+)',name)[1]);expected=[] if name.endswith('schema') else [4,3,5] if i<=6 else [6,4,3]
        assert heights==expected,(name,heights,expected)
        shape_checks+=1
if CODE==16:
    for name,expected in [('cours_schema',[83,83+25,83+25-46]),('ex1_corrige',[125,125+38,125+38-47])]:
        actual=list(map(int,re.findall(r'\{(\d+)\};',figs[name])))
        assert actual==expected,(name,actual,expected);shape_checks+=1
if CODE==15:
    assert '{Grande quantité : '+str(125+28)+'};' in figs['ex1_corrige'];shape_checks+=1
if CODE==14:
    assert '{'+str(360-145)+'};' in figs['ex1_corrige'];shape_checks+=1
if CODE==17:
    assert figs['ex1_corrige'].count('{'+str(36//4)+'};')==4;shape_checks+=1
source=json.loads((D/'sources_locales/chapitre.json').read_text(encoding='utf8'))
assert len(source['exercices'])==9
evidence={'chapitre':CODE,'questions':45,'relations_recalculees':count,'resultats_recalcules_independamment':independent,'figures_mathematiques_controlees':shape_checks,'source_sha256':hashlib.sha256((D/'sources_locales/chapitre.json').read_bytes()).hexdigest(),'fichiers_sha256':{n:hashlib.sha256(t.encode()).hexdigest() for n,t in files.items()}}
(D/'verification_math.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(f'CE1 {CODE:02} : 45 questions, {count} relations exactes, {independent} résultats recalculés indépendamment ; correspondances et solutions cohérentes.')
