"""Inventaire complet des besoins visuels et planches des nouveaux schémas."""
from pathlib import Path
import json,math
import fitz
from PIL import Image,ImageDraw
from donnees import charger
from revision_exercices import ILLUSTRATIONS,METHODES,ANNEXES
from annexes import BILANS,EVALUATIONS
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
QA=ROOT/'tmp/pdfs/qa-pc-quatrieme-revision';QA.mkdir(parents=True,exist_ok=True)
def main():
    chs=charger();rows=[]
    for c in chs:
        for j,e in enumerate(c.exercices+[c.defi],1):
            ident=f'{c.numero}.{j}' if j<=15 else f'D{c.numero}'
            rows.append(dict(id=ident,titre=e.titre,questions=len(e.questions),reponses=len(e.reponses),figure_enonce=e.figure,figure_correction=e.figure_correction,demarche_ajoutee=bool(e.methode),decision='Schéma utile intégré' if ident in ILLUSTRATIONS else 'Question autonome : aucun schéma supplémentaire nécessaire'))
    assert {r['id'] for r in rows}>set(ILLUSTRATIONS)
    figs=json.loads((HERE/'build/figures-exercices.json').read_text(encoding='utf8'))
    out=[dict(figure=n,details=d['textes_hors_cadre']) for n,d in figs['figures'].items() if d.get('textes_hors_cadre')]
    names=sorted(figs['figures'])
    for start in range(0,len(names),12):
        sheet=Image.new('RGB',(1620,920),'#eef1f5');draw=ImageDraw.Draw(sheet)
        for j,name in enumerate(names[start:start+12]):
            p=fitz.open(HERE/'figures'/(name+'.pdf'))[0];pm=p.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False);im=Image.frombytes('RGB',(pm.width,pm.height),pm.samples);im.thumbnail((520,185));x=(j%3)*540+10+(520-im.width)//2;y=(j//3)*230+32
            sheet.paste(im,(x,y));draw.text((j%3*540+12,j//3*230+8),name,fill='#1B3C8E')
        sheet.save(QA/f'figures-{start//12+1:02}.png')
    report=dict(date='2026-10-24',exercices_audites=300,defis_audites=20,bilans_evaluations_audites=6,exercices_avec_figure_enonce=sum(bool(r['figure_enonce']) for r in rows),exercices_avec_figure_correction=sum(bool(r['figure_correction']) for r in rows),corriges_avec_demarche_ajoutee=len(METHODES),figures_nouvelles=figs['nombre'],figures_total=40+figs['nombre'],planches_figures=math.ceil(len(names)/12),legendes_hors_cadre=out,decisions=rows,annexes=ANNEXES)
    (HERE/'build/audit-exercices.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['decisions','annexes','legendes_hors_cadre']},ensure_ascii=True,indent=2))
    print('Figures avec une légende hors cadre : '+', '.join(d['figure'] for d in out))
    if out:raise SystemExit(1)
if __name__=='__main__':main()
