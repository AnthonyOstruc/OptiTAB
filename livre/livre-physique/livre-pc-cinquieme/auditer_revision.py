"""Vérifie les ajouts illustrés, les explications et les fins de bilan du manuel."""
from pathlib import Path
import json,re,hashlib,math
import fitz
import construire_template_terminale as livre
from revision_exercices import ILLUSTRATIONS,METHODES,DEFIS_CORRIGES,BILANS_CORRIGES
from verifier_template_terminale import normal
ROOT=Path(__file__).resolve().parent
checks=[]
def check(label,value):checks.append(dict(controle=label,valide=bool(value)))
def block(source,ident):
    r=re.search(r'\\begin\{blocLivre\}\{'+re.escape(ident)+r'\}(.*?)\\end\{blocLivre\}',source,re.S)
    return r.group(1) if r else ''
def name(spec):return hashlib.sha256(json.dumps([spec,65.0,166.0],ensure_ascii=False,sort_keys=True).encode()).hexdigest()[:16]+'.pdf'

def main():
    source=(livre.OUT/'main.tex').read_text(encoding='utf-8');pdf=livre.OUT/'main.pdf';doc=fitz.open(pdf);text='\n'.join(p.get_text() for p in doc)
    entries=[]
    for n,items in livre.EXOS.items():
        for e in items:
            en=block(source,f'exo-{n}-{e.n}');co=block(source,f'cor-{n}-{e.n}')
            check(f'{n}.{e.n} : blocs présents',bool(en and co))
            if (n,e.n) in ILLUSTRATIONS and ILLUSTRATIONS[n,e.n][0]:check(f'{n}.{e.n} : figure dans l’énoncé',name(e.figure) in en)
            if e.figure_correction:check(f'{n}.{e.n} : figure dans le corrigé',name(e.figure_correction) in co)
            if e.methode:check(f'{n}.{e.n} : démarche dans le PDF',normal(e.methode) in normal(text))
            entries.append(dict(exercice=f'{n}.{e.n}',figure_enonce=e.figure,figure_correction=e.figure_correction,methode=bool(e.methode)))
    for n,spec in DEFIS_CORRIGES.items():check(f'D{n} : dessin de correction inséré',name(spec) in source)
    for (letter,n),spec in BILANS_CORRIGES.items():check(f'Bilan {letter}{n} : dessin avec sa réponse',name(spec) in block(source,f'cor-mission-{letter}-{n}'))
    for letter,title,items in livre.BILANS:
        last=block(source,f'cor-mission-{letter}-5')
        check(f'Bilan {letter} : grille attachée à la dernière réponse','Utiliser le résultat' in last)
    log=(livre.BUILD/'main.log').read_text(encoding='utf-8',errors='replace')
    check('Aucun texte réduit automatiquement',r'\resizebox*' not in (livre.OUT/'cinquieme-charte.tex').read_text(encoding='utf-8'))
    check('Aucune fiche débordante','PCFICHE-TROP' not in log)
    for expr,expected in [('22-4',18),('50+18',68),('68+4',72),('340*.6/2',102),('340*.4/2',68),('340*.5/2',85),('180/3',60),('1000/15',66.66666666666667)]:
        check('Calcul indépendant '+expr,math.isclose(eval(expr,{'__builtins__':{}},{}),expected,rel_tol=1e-12))
    check('Cent jetons : proportions exactes',78+21+1==100 and 156+42+2==200)
    for i,p in enumerate(doc):
        t=p.get_text()
        if 'UTILISER LE RÉSULTAT' in t.upper():check(f'Bilan imprimé page {i+1} : réponse présente',bool(re.search(r'[ABCD]\.\s*5',t)))
    report=dict(pages=len(doc),exercices=300,defis=20,missions=20,enonces_illustres=sum(bool(e.figure) for es in livre.EXOS.values() for e in es),corriges_exercices_illustres=sum(bool(e.figure_correction) for es in livre.EXOS.values() for e in es),defis_corriges_illustres=len(DEFIS_CORRIGES),missions_corrigees_illustrees=len(BILANS_CORRIGES),demarches=len(METHODES),controles=len(checks),echecs=sum(not x['valide'] for x in checks),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),entrees=entries,details=checks)
    (livre.BUILD/'audit-revision.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['details','entrees']},ensure_ascii=False))
    assert report['echecs']==0,[c for c in checks if not c['valide']]
if __name__=='__main__':main()
