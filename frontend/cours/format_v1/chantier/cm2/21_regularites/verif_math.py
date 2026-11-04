# -*- coding: utf-8 -*-
"""Vérifie les calculs numériques du texte final, jamais les données du générateur.

Les égalités volontairement fausses dans les énoncés sont des questions d'analyse
d'erreur. Leurs corrections sont contrôlées dans Étapes et Solution.
"""
from pathlib import Path
from fractions import Fraction
import re,json,ast,hashlib
ICI=Path(__file__).resolve().parent
def evaluate(s):
    s=s.replace(r'\,','').replace('{,}','.').replace('&','').replace(r'\times','*').replace(r'\div','/').strip()
    if not re.fullmatch(r'[\d.\s()+*/-]+',s):raise ValueError(s)
    def ev(n):
        if isinstance(n,ast.Constant):return Fraction(str(n.value))
        if isinstance(n,ast.BinOp):
            a,b=ev(n.left),ev(n.right)
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
            if isinstance(n.op,ast.Mult):return a*b
            if isinstance(n.op,ast.Div):return a/b
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -ev(n.operand)
        raise ValueError(s)
    return ev(ast.parse(s,mode='eval').body)
def check(d):
    errors=[]; count=0;ignored=0;hashes={}
    for name in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt']:
        raw=(d/name).read_text(encoding='utf-8');hashes[name]=hashlib.sha256((d/name).read_bytes()).hexdigest()
        assert not any(c in raw for c in ['\t','\x08','\x0c']),name
        outside=re.sub(r'\$\$.*?\$\$|\$[^$]*\$', '', raw, flags=re.S)
        assert '{,}' not in outside,(name,'virgule LaTeX hors formule')
        text=raw
        if name=='exercices.txt':
            blocks=re.split(r'^===[ \t]*$',raw,flags=re.M)
            assert len(blocks)==21
            assert re.findall(r'^Id: (.*)$',raw,re.M)==[f'nouveau-{k}' for k in range(1,22)]
            text='\n'.join(b.split('Étapes:\n',1)[1] for b in blocks)
            # Les titres reprennent les questions, y compris les propositions
            # volontairement fausses à discuter. Vérifier le corps des corrigés.
            text=re.sub(r'^## Question .*$', '', text, flags=re.M)
            for b in blocks:
                en,rest=b.split('Étapes:\n',1);steps,solution=rest.split('Solution:\n',1)
                assert len(re.findall(r'^\d+\. ',en,re.M))==3
                assert len(re.findall(r'^## Question ',steps,re.M))==3
                for marker in ['::: methode','::: etape','::: resultat']:assert steps.count(marker)==3
                results=re.findall(r'::: resultat\n(.*?)\n:::',steps,re.S)
                solutions=[x for x in solution.splitlines() if re.match(r'\d+\. ',x)]
                assert [re.sub(r'^\d+\. ','',s) for s in solutions]==results
        formulas=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',text,re.S)
        for pair in formulas:
            formula=pair[0] or pair[1]
            formula=formula.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
            previous=None
            for row in formula.split(r'\\'):
                row=row.strip().replace('&','')
                if '=' not in row:continue
                sides=row.split('=')
                if not sides[0].strip() and previous is not None:sides[0]=previous
                try:values=[evaluate(s) for s in sides]
                except (ValueError,SyntaxError):ignored+=1;continue
                count+=1
                if any(v!=values[0] for v in values[1:]):errors.append({'fichier':name,'egalite':row})
                previous=sides[-1]
    extra=[]
    if d.name=='21_regularites':
        def walk(pos,direction,commands):
            x,y=ord(pos[0])-65,int(pos[1])-1
            for cmd in commands:
                if cmd=='G':direction=(direction-1)%4
                elif cmd=='D':direction=(direction+1)%4
                else:
                    dx,dy=[(0,1),(1,0),(0,-1),(-1,0)][direction]
                    x+=dx*cmd;y+=dy*cmd
            return chr(x+65)+str(y+1),direction
        assert walk('B2',1,[2,'G',1])==('D3',0)
        assert walk('D3',0,['G',2,'G',1])==('B2',2)
        assert walk('D4',2,['D',2,'G',1])==('B3',2)
        assert walk('C3',0,[2,'D',2,'D',1])==('E4',2)
        assert walk('E4',2,['D',2,'G',1])==('C3',2)
        assert walk('E4',2,['G',2])==('G4',1)
        assert [1+4*k for k in [1,2,3]]==[5,9,13]
        extra=['6 chemins/orientations simulés','motifs 5/9/13 vérifiés']
    report={'statut':'OK' if not errors else 'a_corriger','math_OK':not errors,'egalites_numeriques_verifiees':count,'expressions_symboliques_ou_comparaisons':ignored,'controles_complementaires':extra,'anomalies':errors,'empreintes_finales':hashes}
    (d/'audit_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert not errors,errors
    print(d.name,count,'égalités numériques vérifiées ; solutions/étapes cohérentes ; OK')
if __name__=='__main__':check(ICI)
