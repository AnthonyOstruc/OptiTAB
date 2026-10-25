"""Contrôle des constructions, de la navigation et du PDF final révisé."""
from pathlib import Path
import hashlib,json,re,sys,importlib.util
import fitz
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('collisions',ROOT.parent/'outils/collisions_physique_20261024.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
checks=[]
def check(label,value):checks.append(dict(controle=label,valide=bool(value)))
def block(path,env,n):
    return re.findall(r'\\begin\{'+env+r'\}.*?\\end\{'+env+r'\}',path.read_text(encoding='utf-8'),re.S)[n-1]

def main():
    pdf=ROOT/'main.pdf';doc=fitz.open(pdf);text='\n'.join(p.get_text() for p in doc)
    log=(ROOT/'build/main.log').read_text(encoding='utf-8',errors='replace')
    for token in ['Overfull','Missing character','undefined references','multiply defined','Label(s) may have changed']:
        check('Journal sans '+token,token not in log)
    check('27 chapitres complets',len(list((ROOT/'chapitres').glob('*.tex')))==27)
    meta=json.loads((ROOT/'build/revision-figures.json').read_text(encoding='utf-8'))
    files={int(p.name[:2]):p for p in (ROOT/'corriges').glob('*.tex')}
    for name in meta['figures']:
        ch=int(name[:2]);n=int(name[5:7]);s=block(files[ch],'corrige',n)
        check('Construction corrigée '+name,'\\schema[corrige]{rev-'+name+'}' in s)
        check('Figure sans caractère de contrôle '+name,not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\t]',(ROOT/'figures'/('rev-'+name+'.tex')).read_text(encoding='utf-8')))
    for ch,n,fig in [(17,4,'17-venturi'),(17,8,'17-venturi'),(23,2,'23-fronts')]:
        p=next((ROOT/'chapitres').glob(f'{ch:02}-*.tex'))
        check(f'Document local dans l’énoncé {ch}.{n}','\\schema{'+fig+'}' in block(p,'exercice',n))
    check('Convention de décharge explicitée',r'$u_R-u_C=0$' in block(files[26],'corrige',6))
    check('Couplage capacitif à travers un isolant',"Une couche isolante n’empêche pas" in block(files[26],'corrige',12))
    links=[l for p in doc for l in p.get_links()]
    check('Destinations de navigation valides',all(0<=l['page']<len(doc) for l in links if l['kind']==fitz.LINK_GOTO))
    check('Format A4',all(abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1 for p in doc))
    notes=[i+1 for i,p in enumerate(doc) if p.get_text().strip()=='Notes']
    check('Texte natif présent et pages de notes réglées',all(len(p.get_text().strip())>15 or (p.get_text().strip()=='Notes' and len(p.get_drawings())>=20) for p in doc))
    check('Aucun caractère de remplacement','\ufffd' not in text and '\x00' not in text)
    check('Renvois résolus','??' not in text)
    outside=[]
    for i,p in enumerate(doc):
        for b in p.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                for s in line['spans']:
                    r=fitz.Rect(s['bbox'])
                    if s['text'].strip() and (r.x0<-.5 or r.y0<-.5 or r.x1>p.rect.width+.5 or r.y1>p.rect.height+.5):outside.append([i+1,s['text']])
    check('Aucun texte hors page',not outside)
    collisions=module.candidates(pdf)
    check('Aucune collision de légendes détectée',not collisions)
    report=dict(pages=len(doc),chapitres=27,exercices=405,defis=27,sujets_bac=6,figures_nouvelles=18,corriges_completes_par_figures=23,enonces_completes_par_figures=3,controles=len(checks),echecs=sum(not c['valide'] for c in checks),liens=len(links),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),collisions=collisions,texte_hors_page=outside,pages_de_notes=notes,details=checks)
    (ROOT/'build/audit-revision.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False))
    assert report['echecs']==0,[c for c in checks if not c['valide']]
if __name__=='__main__':main()
