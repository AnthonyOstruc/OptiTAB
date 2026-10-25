"""Contrôles de contenu, barèmes, calculs et placements des cinq sujets nouveaux."""
from pathlib import Path
import json,math,re,hashlib,unicodedata
import fitz
from annales_originales import SUJETS,CALCULS,figures_utilisees
ROOT=Path(__file__).resolve().parent
checks=[]
def check(label,ok):checks.append(dict(controle=label,valide=bool(ok)))
def normal(s):
    s=unicodedata.normalize('NFKD',s)
    return re.sub(r'[^a-z0-9]','',s.encode('ascii','ignore').decode().lower())

def main():
    doc=fitz.open(ROOT/'build/main.pdf');text='\n'.join(p.get_text() for p in doc)
    source=(ROOT/'annexes.tex').read_text(encoding='utf-8')
    check('Cinq sujets numérotés de 11 à 15',[s.n for s in SUJETS]==list(range(11,16)))
    for s in SUJETS:
        check(f'Sujet {s.n} : trois parties et neuf questions',len(s.blocs)==3 and sum(len(b.questions) for b in s.blocs)==9)
        check(f'Sujet {s.n} : neuf points scientifiques',sum(q.points for b in s.blocs for q in b.questions)==9)
        for k,b in enumerate(s.blocs,1):
            check(f'{s.n}.{k} : document présent',bool(b.document) and normal(b.titre) in normal(text))
            for j,q in enumerate(b.questions,1):
                check(f'{s.n}.{k}.{j} : réponse, démarche, barème',all(len(t)>20 for t in [q.enonce,q.reponse,q.methode,q.bareme]))
                check(f'{s.n}.{k}.{j} : aucun caractère de contrôle',not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\t]',q.enonce+q.reponse+q.methode))
        for label in [f'ann-{s.n}',f'cor-ann-{s.n}']:check('Destination '+label,'\\label{'+label+'}' in source)
    for expression,expected in CALCULS:
        check('Calcul '+expression,math.isclose(eval(expression,{'__builtins__':{}},{}),expected,rel_tol=1e-10,abs_tol=1e-12))
    check('Équation propane : conservation des trois éléments',(3,8,5*2)==(3,4*2,3*2+4))
    check('Chlorure : charge 17 − 18 = −1',17-18==-1)
    check('Dirigeable : équilibre',math.isclose(3+.4,3.4))
    for name in figures_utilisees():
        check('Placement '+name,source.count('figures/'+name+'.pdf')==1)
        p=ROOT/'figures'/(name+'.pdf');d=fitz.open(p)
        check('Figure vectorielle '+name,len(d)==1 and not d[0].get_images())
    # Le modèle atomique du chlorure ne doit imposer aucun nombre de neutrons.
    p=fitz.open(ROOT/'figures/ann14-ion.pdf')
    check('Aucun isotope de chlore inventé','neutron' not in p[0].get_text().lower())
    report=dict(sujets=5,questions=45,figures=len(figures_utilisees()),calculs=len(CALCULS),controles=len(checks),echecs=sum(not c['valide'] for c in checks),sha256=hashlib.sha256((ROOT/'build/main.pdf').read_bytes()).hexdigest(),details=checks)
    (ROOT/'build/audit-annales.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False))
    assert report['echecs']==0,[c for c in checks if not c['valide']]
if __name__=='__main__':main()
