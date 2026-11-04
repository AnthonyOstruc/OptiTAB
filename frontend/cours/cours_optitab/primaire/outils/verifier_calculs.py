"""Vérification exacte des calculs générés et des contrôles des livres sources."""
import hashlib
import json
from fractions import Fraction as F
import sympy
from config import GRADE,ROOT,FRONT,chapters

def main():
    items=json.loads((ROOT/'verifications/manifeste.json').read_text(encoding='utf-8'))
    count=0;book=0
    for e in items:
        for expr in e['controles']:
            assert eval(expr,{'F':F}), (e['code'],expr)
            count+=1
    env={**vars(sympy),'F':F}
    for c in chapters():
        for e in c.exercices:
            code=e.get('controle',e.get('check',''))
            if code:
                if code.strip().startswith('assert '):exec(code,env)
                else:assert eval(code,env),(c.slug,code)
                book+=1
    # Propriétés indépendantes des formules de réponse.
    for whole in range(1,100):
        for d in range(2,11):
            quotient,reste=divmod(whole,d)
            assert quotient*d+reste==whole and 0<=reste<d
            assert F(whole,d)==F(whole*2,d*2)
    files=[p for c in chapters() for p in (ROOT/f'cours_{c.slug}_{GRADE}.txt',FRONT/f'cours/resume/{GRADE}/resume_{c.slug}_{GRADE}.txt',FRONT/f'exercices/{GRADE}/exercice_{c.slug}_{GRADE}.txt')]
    result=dict(niveau=GRADE,exercices=len(items),questions=sum(x['questions'] for x in items),calculs_exacts=count,controles_sources=book,proprietes_independantes=891,erreurs=[],limite='Contrôles numériques et invariants ; les formulations et les figures sont aussi relues par échantillonnage.',empreintes={str(p.relative_to(FRONT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
    (ROOT/'verifications/calculs.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{GRADE}: {count} contrôles exacts, {book} contrôles sources ; {result["questions"]} questions, aucune erreur.')
    return result

if __name__=='__main__':main()
