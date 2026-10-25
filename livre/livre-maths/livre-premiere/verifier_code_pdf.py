"""Contrôle les programmes extraits du PDF, avant toute exécution.

L'indentation est reconstruite depuis les positions des glyphes. Aucun opérateur
ou caractère n'est remplacé : une conversion typographique erronée doit échouer.
"""
from pathlib import Path
from collections import Counter
import argparse,ast,hashlib,json,math,random,re
import fitz

ROOT=Path(__file__).resolve().parent
# 27 programmes initiaux, plus la liste des pentes des sécantes (corrigé 3.6, audit du 23 octobre 2026).
NOMBRE_BLOCS=28

def extraire(pdf_path):
    programmes=[]
    with fitz.open(pdf_path) as pdf:
        for numero,page in enumerate(pdf,1):
            lignes=[]
            etiquettes=[]
            for bloc in page.get_text('dict')['blocks']:
                for ligne in bloc.get('lines',[]):
                    spans=ligne['spans']
                    for span in spans:
                        if span['text'].strip()=='PYTHON':
                            etiquettes.append(fitz.Rect(span['bbox']))
                    mono=[s for s in spans if 'FiraMono' in s['font']]
                    if mono:
                        lignes.append({
                            'rect':fitz.Rect(ligne['bbox']),
                            'texte':''.join(s['text'] for s in mono),
                            'taille':mono[0]['size'],
                        })
            fonds=[d['rect'] for d in page.get_drawings()
                   if d.get('fill') is not None and d['rect'].height>20]
            for etiquette in etiquettes:
                candidats=[r for r in fonds if r.contains(etiquette)]
                assert candidats,(numero,'Fond du bloc Python absent')
                cadre=min(candidats,key=lambda r:r.width*r.height)
                code=[l for l in lignes if cadre.contains(l['rect'])]
                assert code,(numero,'Bloc Python vide')
                code.sort(key=lambda l:l['rect'].y0)
                origine=min(l['rect'].x0 for l in code)
                reconstruit=[]
                for ligne in code:
                    espaces=(ligne['rect'].x0-origine)/(ligne['taille']*.6)
                    assert abs(espaces-round(espaces))<.15,(numero,espaces)
                    reconstruit.append(' '*round(espaces)+ligne['texte'])
                programmes.append({
                    'page_pdf':numero,'code':'\n'.join(reconstruit)+'\n',
                })
    return programmes

def sources():
    blocs=[]
    for dossier in ['chapitres','corriges','annexes']:
        for p in sorted((ROOT/dossier).glob('*.tex')):
            for source in re.findall(r'\\begin\{python\}\s*(.*?)\\end\{python\}',p.read_text(encoding='utf-8'),re.S):
                blocs.append(source.strip()+'\n')
    return blocs

def empreinte_ast(code):
    return ast.dump(ast.parse(code),include_attributes=False)

def verifier(pdf_path,preflight=False):
    blocs=extraire(pdf_path)
    erreurs=[];signatures=[];scopes=[]
    for i,b in enumerate(blocs,1):
        try:
            signatures.append(empreinte_ast(b['code']))
        except SyntaxError as e:
            erreurs.append({'bloc':i,'page_pdf':b['page_pdf'],
                            'erreur':str(e),'code':b['code']})
    attendus=sources() if not preflight else []
    if not erreurs and not preflight:
        assert len(blocs)==len(attendus)==NOMBRE_BLOCS
        assert Counter(signatures)==Counter(map(empreinte_ast,attendus)),\
            'Le programme extrait du PDF differe de sa source.'
    # Exécuter uniquement après validation syntaxique et fidélité aux sources.
    if not erreurs and (preflight or len(blocs)==len(attendus)):
        for b in blocs:
            ns={};random.seed(2026)
            exec(compile(b['code'],str(pdf_path)+':'+str(b['page_pdf']),'exec'),ns)
            scopes.append(ns)
        if not preflight:
            def trouver(nom):
                ns=[s for s in scopes if nom in s]
                assert len(ns)==1,nom
                return ns[0]
            ns=next(s for s in scopes if 'a' in s and 'b' in s)
            assert (ns['a'],ns['b'])==(5,3)
            assert next(s['t'] for s in scopes if 't' in s)==13
            ns=trouver('tirage')
            for u,v in [(0,-1),(.499,-1),(.5,2),(.799,2),(.8,5),(.999,5)]:
                ns['random']=lambda u=u:u
                assert ns['tirage']()==v
            ns=next(s for s in scopes if 'compteur' in s and 'proportion' in s)
            assert ns['compteur']==470 and ns['proportion']==.94
            assert [trouver('f')['f'](x) for x in [0,2,5]]==[2,0,12]
            ns=trouver('moments');mu,var=ns['moments']([-1,0,2],[.2,.5,.3])
            assert math.isclose(mu,.4) and math.isclose(var,1.24)
            assert ns['moments']([3],[1])==(3,0)
            fn=trouver('fibonacci')['fibonacci']
            assert fn(0)==[0] and fn(1)==[0,1]
            assert fn(7)==[0,1,1,2,3,5,8,13]
            assert fn(16)[-1]==987<1000<fn(17)[-1]==1597
            fn=trouver('bornes_exponentielle')['bornes_exponentielle']
            for n in [1,10,100,1000]:
                bas,haut=fn(n)
                assert bas<math.exp(.5)<haut
            fn=trouver('encadrer_racine')['encadrer_racine']
            assert fn(0)==(0.,1.)
            assert fn(10)==(698/1024,699/1024)
            for n in [0,1,4,10,20]:
                a,b=fn(n)
                assert b-a==2**(-n) and a**3+a-1<=0<=b**3+b-1
            fn=trouver('secantes')['secantes']
            assert fn(0.5,4)==[0.5,1.5,2.5,3.5] and fn(1,0)==[]
            fn=trouver('archimede')['archimede']
            assert fn(0)==3 and 3+10/71<fn(4)<math.pi and round(fn(4),5)==3.14103
            fn=trouver('newton')['newton']
            assert fn(1)==1.5 and abs(fn(5)-math.sqrt(2))<1e-14
    return {
        'pdf':str(pdf_path),'source_sha256':hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
        'blocs_extraits':len(blocs),'blocs_syntaxiquement_valides':len(signatures),
        'blocs_executes':len(scopes),'pages_code':sorted({b['page_pdf'] for b in blocs}),
        'equivalence_ast_avec_les_sources':not erreurs and not preflight,
        'reconstruction_indentation':'Positions PDF des glyphes, sans substitution de caracteres.',
        'erreurs':erreurs,
    }

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--pdf',type=Path,default=ROOT/'main.pdf')
    ap.add_argument('--rapport',type=Path,default=ROOT/'build/verification-code-pdf.json')
    ap.add_argument('--preflight',action='store_true')
    args=ap.parse_args()
    rapport=verifier(args.pdf,args.preflight)
    args.rapport.parent.mkdir(parents=True,exist_ok=True)
    args.rapport.write_text(json.dumps(rapport,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in rapport.items() if k!='erreurs'}|
                     {'erreurs':len(rapport['erreurs'])},ensure_ascii=True,indent=2))
    if rapport['erreurs']:raise SystemExit(1)
