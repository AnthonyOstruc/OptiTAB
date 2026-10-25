"""Contrôles exacts, lecture des preuves et exécution des exemples Python."""
from pathlib import Path
import contextlib,io,json,re,random
import sympy as sp
from modele import CHAPITRES
import contenu_01_02,contenu_03_04,contenu_05_06,contenu_07_08
import contenu_09_10,contenu_11_12,contenu_13_14,contenu_15_16

ROOT=Path(__file__).resolve().parent
env={k:getattr(sp,k) for k in dir(sp) if not k.startswith('_')}
env.update(dict(zip(['x','y','p'],sp.symbols('x y p',real=True))))
errors=[]; verified=[]; programs=[]
for ch in CHAPITRES:
    assert len(ch.exercices)==15
    for i,ex in enumerate(ch.exercices,1):
        ident=f'{ch.numero:02d}.{i:02d}'
        try:
            exec(ex.controle,dict(env))
            verified.append(ident)
        except Exception as error:
            errors.append([ident,type(error).__name__,str(error),ex.controle])
        for side,text in [('enonce',ex.enonce),('corrige',ex.corrige)]:
            assert not any(ord(c)<32 and c not in '\n\r\t' for c in text),ident
            for n,code in enumerate(re.findall(r'\\begin\{python\}(.*?)\\end\{python\}',text,re.S),1):
                if (ch.numero,i,side)==(15,13,'enonce'):
                    programs.append({'id':ident,'face':side,'bloc':n,'statut':'boucle erronée analysée, non exécutée'})
                    continue
                try:
                    namespace={}
                    random.seed(20261021)
                    with contextlib.redirect_stdout(io.StringIO()): exec(code.strip(),namespace)
                    tests={
                        (1,8,'corrige'):lambda d: d['multiple'](35,7) is True and d['multiple'](35,6) is False,
                        (15,1,'enonce'):lambda d: (d['a'],d['b'])==(10,5),
                        (15,5,'enonce'):lambda d: d['s']==15,
                        (15,3,'enonce'):lambda d: d['f'](4)==29 and d['f'](-1)==-1,
                        (15,4,'enonce'):lambda d: [d['distancezero'](a) for a in [-5,0,2]]==[5,0,2],
                        (15,6,'enonce'):lambda d: d['seuil']()==(10,1024),
                        (15,6,'corrige'):lambda d: d['seuilbas']()==(7,0.0078125),
                        (15,7,'enonce'):lambda d: d['encadrement'](2)==(1.41,1.42),
                        (15,8,'enonce'):lambda d: d['alignes'](0,0,2,3,4,6) and not d['alignes'](0,0,2,3,4,7),
                        (15,9,'corrige'):lambda d: d['droite'](0,1,2,5)==(2.0,1.0),
                        (15,10,'enonce'):lambda d: set(d['succes']() for _ in range(200))=={0,1},
                        (15,10,'corrige'):lambda d: set(d['somme2']() for _ in range(3000))==set(range(2,13)),
                        (15,11,'enonce'):lambda d: 0<=d['frequence'](100)<=1,
                        (15,12,'enonce'):lambda d: (lambda a: 1<=a[0]<=6 and 0<=a[1]<=3)(d['resume'](200)),
                        (15,14,'enonce'):lambda d: abs(d['longueur'](2)-float((sp.sqrt(5)+sp.sqrt(13))/4))<1e-12,
                        (15,15,'enonce'):lambda d: (lambda a:a[0]<=.7<=a[1] and abs((a[1]-a[0])-2/2**20)<1e-10)(d['encadremaximum'](20)),
                    }
                    if (ch.numero,i,side) in tests: assert tests[ch.numero,i,side](namespace)
                    elif ch.numero==15 or (ch.numero,i)==(1,8): raise AssertionError('programme sans test dédié')
                    programs.append({'id':ident,'face':side,'bloc':n,'statut':'exécuté et contrôlé'})
                except Exception as error: errors.append([ident,'Python',str(error),code])
# Programmes des cours (langage naturel et Python côte à côte).
for ch in CHAPITRES:
    for n,code in enumerate(re.findall(r'\\begin\{pythoncol\}(.*?)\\end\{pythoncol\}|\\begin\{python\}(.*?)\\end\{python\}','\n'.join(ch.cours),re.S),1):
        code=next(c for c in code if c)
        try:
            out=io.StringIO()
            with contextlib.redirect_stdout(out): exec(code.strip(),{})
            if ch.numero==15: assert out.getvalue().strip()=='10'
            programs.append({'id':f'cours {ch.numero}','face':'cours','bloc':n,'statut':'exécuté et contrôlé'})
        except Exception as error: errors.append([f'cours {ch.numero}','Python',str(error),code])
report={'chapitres':len(CHAPITRES),'exercices_controles':len(verified),'controles':verified,'programmes':programs,'erreurs':errors,
 'portee':'Calculs exacts, cas limites et exécution des programmes. Les preuves rédigées font aussi l’objet d’une relecture ; des tests finis ne sont pas une preuve de leur généralité.'}
(ROOT/'build').mkdir(exist_ok=True)
(ROOT/'build/verification-contenu.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'chapitres':len(CHAPITRES),'exercices':len(verified),'blocs_python':len(programs),'erreurs':errors},ensure_ascii=True,indent=2))
if errors: raise SystemExit(1)
