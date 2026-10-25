"""Contrôle de la passe éditoriale des 210 couples énoncé/corrigé.

Les contrôles de calcul ne remplacent pas la relecture des explications et des rendus.
"""
from pathlib import Path
from fractions import Fraction
from itertools import product
import json,re,math,hashlib
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
R=Path(__file__).resolve().parent
review=json.loads((R/'revision-editoriale.json').read_text(encoding='utf-8'))
checks=[]
def check(name,condition):
    assert condition,name
    checks.append(name)
def fmt(q):
    q=Fraction(q)
    return str(q.numerator) if q.denominator==1 else rf'\frac{{{q.numerator}}}{{{q.denominator}}}'
def texmath(s):
    s=s.replace(r'\pi','pi').replace(r'\sqrt e','sqrt(E)')
    s=re.sub(r'e\^\{([^}]+)\}',r'exp(\1)',s)
    s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
    s=re.sub(r'\\frac(\d)(\d)',r'((\1)/(\2))',s)
    s=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',s)
    s=re.sub(r'\\sqrt(\d)',r'sqrt(\1)',s)
    s=re.sub(r'\be\b','E',s)
    return parse_expr(s,local_dict={'E':S.E,'pi':S.pi,'exp':S.exp,'sqrt':S.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))

expected={(c,e) for c in range(1,15) for e in range(1,16)}
entries={(x['chapitre'],x['exercice']):x for x in review['exercices']}
check('210 couples uniques relus',set(entries)==expected and len(review['exercices'])==210)
sources={}
for folder,kind in [('chapitres','exercice'),('corriges','corrige')]:
    for c in range(1,15):
        p=next((R/folder).glob(f'{c:02}-*.tex'));text=p.read_text(encoding='utf-8')
        pattern=r'\\begin\{exercice\}\[(\d)\]\{([^}\n]+)\}(.*?)\\end\{exercice\}' if kind=='exercice' else r'\\begin\{corrige\}\{(\d+)\}\{([^}\n]+)\}(.*?)\\end\{corrige\}'
        blocks=list(re.finditer(pattern,text,re.S));check(f'{folder} {c} : quinze blocs',len(blocks)==15)
        for n,m in enumerate(blocks,1):
            body=m[3].strip();entry=entries[c,n];side='enonce' if kind=='exercice' else 'corrige'
            sources[c,n,side]=body
            check(f'{c}.{n} {side} : titre',m[2]==entry['titre'])
            possible={hashlib.sha256((body+'\n'*k).encode()).hexdigest() for k in range(3)}
            check(f'{c}.{n} {side} : texte relu inchangé',entry[side+'_sha256'] in possible)
            refs=re.findall(r'\\figure(?:Geo|Livre)(?:\[[^]]+\])?\{([^}]+)\}',body)
            check(f'{c}.{n} {side} : représentations présentes',refs==entry['visuels_'+side])
            for ref in refs:check(f'{c}.{n} {side} : source {ref}',(R/'figures'/f'{ref}.tex').exists())
            if kind=='corrige':
                check(f'{c}.{n} : démarche de résolution',r'\demarche{' in body or r'\methode{' in body)
                check(f'{c}.{n} : explication renseignée',len(entry['demarche'])>=35 and len(body)>=150)
            check(f'{c}.{n} {side} : pas de caractère de contrôle',not any(ord(x)<32 and x not in '\r\n' for x in body))

# Les représentations effectivement nécessaires sont exigées dans les deux versions.
for e in (5,6,7,8,9,10,11,12,13,14):
    for side in ('enonce','corrige'):check(f'9.{e} {side} : arbre',f'r09-{e:02}' in entries[9,e]['visuels_'+side])
for c,e,key in [(10,15,'r10-15-triangle'),(11,8,'r11-08-zone'),(11,9,'r11-09-zone'),(14,13,'r14-13-geometrie'),(14,14,'r14-14')]:
    for side in ('enonce','corrige'):check(f'{c}.{e} {side} : schéma requis',key in entries[c,e]['visuels_'+side])
for c,e,key in [(1,5,'r01-05-signes'),(4,4,'r04-04-var'),(4,8,'r04-08-var'),(5,13,'r05-13-var'),(9,2,'r09-02'),(10,10,'r10-10-issues'),(10,13,'r10-13-issues'),(11,3,'r11-03-boite'),(11,6,'r11-06-histogramme'),(12,1,'r12-01-trace'),(14,9,'r14-09-var')]:
    check(f'{c}.{e} : représentation demandée au corrigé',key in entries[c,e]['visuels_corrige'])
check('6.12 : rotation uniforme explicitée','uniforme' in sources[6,12,'enonce'])

tree_count=0;variation_count=0;x=S.symbols('x')
for key,asset in review['assets'].items():
    p=R/asset['fichier'];check(f'{key} : fichier fourni',p.exists())
    text=p.read_text(encoding='utf-8')
    check(f'{key} : caractères de contrôle absents',not any(ord(c)<32 and c not in '\r\n' for c in text))
    check(f'{key} : sauts de lignes valides',not re.search(r'\\n(?:\s|$)',text))
    if asset['type'].startswith('arbre'):
        tree_count+=1
        masses=list(map(Fraction,asset['feuilles']))
        check(f'{key} : feuilles entre 0 et 1',all(0<=q<=1 for q in masses))
        check(f'{key} : masse totale 1',sum(masses)==1)
        if asset['type']=='arbre':
            ps=list(map(Fraction,asset['probas']));qs=list(map(Fraction,asset['conditionnelles']))
            check(f'{key} : partition initiale',sum(ps)==1 and all(q>0 for q in ps))
            check(f'{key} : poids conditionnels',all(0<=q<=1 for q in qs))
            expected_masses=[w for p,q in zip(ps,qs) for w in (p*q,p*(1-q))]
            check(f'{key} : produits des chemins',masses==expected_masses)
            printed=re.findall(r'\$P=([^$]+)\$',text)
            check(f'{key} : probabilités imprimées',printed==list(map(fmt,masses)))
        else:
            n=asset['n'];p=Fraction(asset['p']);without=asset['sans_remise']
            names=('R','B') if key in ('r09-10','r09-11') else ('S','E')
            expected_masses=[]
            for bits in product((0,1),repeat=n):
                mass=Fraction(1)
                for d,b in enumerate(bits):
                    q=Fraction((3 if b==0 else 2)-bits[:d].count(b),5-d) if without else (p if b==0 else 1-p)
                    mass*=q
                expected_masses.append(mass)
                seq=''.join(names[b] for b in bits)
                check(f'{key} : feuille {seq}',f'{seq}:\\ {fmt(mass)}' in text)
            check(f'{key} : nombre de feuilles',len(masses)==2**n)
            check(f'{key} : poids successifs',masses==expected_masses)
            check(f'{key} : tous les nœuds',len(re.findall(r'\\coordinate \(N[01]*\)',text))==2**(n+1)-1)
    if asset['type']=='variations' and asset['fonction']:
        variation_count+=1
        f=S.sympify(asset['fonction'],locals={'x':x});xs=list(map(S.sympify,asset['points']))
        vals=list(map(texmath,asset['valeurs']))
        check(f'{key} : valeurs aux bornes et points critiques',all(S.simplify(f.subs(x,a)-b)==0 for a,b in zip(xs,vals)))
        signs=re.search(r'\\tkzTabLine\{([^}]+)\}',text)[1].split(',')
        derivative=S.diff(f,x)
        for j,(a,b) in enumerate(zip(xs,xs[1:])):
            sign='+' if float(derivative.subs(x,(a+b)/2))>0 else '-'
            check(f'{key} : signe intervalle {j+1}',signs[2*j+1]==sign)

# Le programme réellement ajouté au corrigé est exécuté, pas une copie du programme.
snippet=re.search(r'\\begin\{python\}\s*(.*?)\\end\{python\}',sources[6,15,'corrige'],re.S)[1]
scope={};exec(compile(snippet,'corrige-6-15','exec'),scope)
# Méthode d'Archimède : demi-périmètre du polygone à 6*2**k côtés, sans utiliser pi.
check('6.15 : programme sans pi','pi' not in snippet)
for k in range(6):
    n=6*2**k
    check(f'6.15 : demi-périmètre programmé k={k}',math.isclose(scope['archimede'](k),n*math.sin(math.pi/n),rel_tol=1e-9))
check('6.15 : 96 côtés et minoration d’Archimède',3+10/71<scope['archimede'](4)<math.pi and f"{scope['archimede'](4):.5f}"=='3.14103')
check('6.15 : valeur imprimée',r'\res{3{,}14103}' in sources[6,15,'corrige'])

report={'exercices_relus':210,'corriges_reecrits':sum(e['reecriture'] for e in entries.values()),
        'explications_complementaires':sum(e['explication_ajoutee'] for e in entries.values()),
        'nouveaux_visuels':len(review['assets']),'arbres_controles':tree_count,
        'tableaux_variations_controles':variation_count,'controles_reussis':len(checks),
        'notes':'La matrice explicite le choix des représentations pour chaque énoncé et chaque corrigé. Les tests soutiennent la relecture humaine, sans constituer une preuve formelle de tout le texte.',
        'controles':checks}
(R/'build/verification-relecture.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('controles','notes')},ensure_ascii=True,indent=2))
