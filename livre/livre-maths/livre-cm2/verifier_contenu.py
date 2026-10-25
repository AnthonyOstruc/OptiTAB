"""Contrôles exacts des données originales, séparés du rendu LaTeX."""
from pathlib import Path
import importlib, json, math
import sympy as s
from modele import CHAPITRES

ROOT=Path(__file__).resolve().parent
(ROOT/'build').mkdir(exist_ok=True)
for p in sorted(ROOT.glob('contenu_*.py')):
    importlib.import_module(p.stem)

def environnement():
    names=['Rational','sqrt','expand','simplify','solve','solveset','factorint','isprime','divisors','gcd','ilcm','degree','S','pi','sin','cos','tan','N','Abs','binomial']
    env={name:getattr(s,name) for name in names}
    env.update(x=s.Symbol('x',real=True),n=s.Symbol('n',integer=True),ceil=math.ceil,math=math)
    return env

def verifier():
    erreurs=[]; total=0; details=[]
    for c in CHAPITRES:
        for i,e in enumerate(c.exercices,1):
            total+=1
            try:
                assert e.methode.strip() and e.controle.strip() and e.corrige.strip()
                exec(e.controle,environnement())
                details.append({'type':'chapitre','chapitre':c.numero,'exercice':i,'titre':e.titre,'statut':'réussi'})
            except Exception as ex: erreurs.append([c.numero,i,e.titre,type(ex).__name__,str(ex)])
    from approfondissements import DEFIS
    from bilans import BILANS
    from donnees_scripts import verifier_scripts
    for i,d in enumerate(DEFIS,1):
        total+=1
        try:
            exec(d.controle,environnement())
            details.append({'type':'défi','numero':i,'titre':d.titre,'statut':'réussi'})
        except Exception as ex:erreurs.append(['defi',i,d.titre,type(ex).__name__,str(ex)])
    for b in BILANS:
        for i,(_,_,k) in enumerate(b.automatismes,1):
            total+=1
            try:
                exec(k,environnement())
                details.append({'type':'automatisme','sujet':b.lettre,'numero':i,'statut':'réussi'})
            except Exception as ex:erreurs.append(['bilan-auto',b.lettre,i,str(ex)])
        for i,p in enumerate(b.problemes,1):
            total+=1
            try:
                exec(p.controle,environnement())
                details.append({'type':'problème','sujet':b.lettre,'numero':i,'titre':p.titre,'statut':'réussi'})
            except Exception as ex:erreurs.append(['bilan-probleme',b.lettre,i,str(ex)])
    for c in CHAPITRES:
        if c.numero in [15,16,17,18]:
            assert all(e.figure for e in c.exercices),(c.numero,'figure absente')
    assert len({c.numero for c in CHAPITRES})==len(CHAPITRES)==21
    assert len(DEFIS)==21 and all(len(d.indices)==2 for d in DEFIS)
    assert all(len(b.automatismes)==12 and len(b.problemes)==4 for b in BILANS)
    resultat={'chapitres':len(CHAPITRES),'controles_exercices_defis_sujets':total,'tests_scripts':verifier_scripts(),'erreurs':erreurs,'details':details}
    (ROOT/'build/controles-calculs.json').write_text(json.dumps(resultat,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in resultat.items() if k!='details'},ensure_ascii=True,indent=2))
    assert not erreurs
    return resultat

if __name__=='__main__': verifier()
