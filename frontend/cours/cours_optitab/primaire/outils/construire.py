"""Construit les trois supports du site, leurs figures et leur manifeste."""
import argparse
import html
import io
import json
import re
import subprocess
import sys
import shutil
from config import GRADE,LABEL,ROOT,FRONT,BOOK,chapters,CATS
from modele_site import dm,render_exercice
from parcours import choisir,theme
from schemas import draw,save_png

# Le convertisseur de cours est celui déjà vérifié pour la sixième.
import importlib.util
source=ROOT.parent/'6e/outils/construire_6e.py'
raw=source.read_text(encoding='utf-8')
start=raw.index('BOX =');end=raw.index('\ndef build_pages(')
ns={'re':re,'dm':dm}
exec(raw[start:end],ns)
box,to_html,WRAP=ns['box'],ns['to_html'],ns['WRAP']

def primary_text(s):
    s=html.escape(s)
    return re.sub(r'(?<![\d/])(\d+)\s*/\s*(\d+)(?![\d/])',lambda x:'$\\frac{'+x[1]+'}{'+x[2]+'}$',s)

def course(c):
    figures=[]
    if GRADE.startswith('cm'):
        body=to_html('\n'.join(c.cours),figures)
        summary=[]
        for page in re.split(r'(?=\\essSection\{)','\n'.join(c.cours)):
            if not page.strip():continue
            heading=re.search(r'\\essSection\{\d+\}\{[^}]+\}',page)[0]
            items=re.findall(r'\\begin\{(definition|propriete|exemple|savoirfaire|attention)\}(?:\[([^]]+)\])?(.*?)\\end\{\1\}',page,re.S)
            chosen=[];example=False
            for kind,title,text in items:
                if kind=='exemple' and example:continue
                if kind=='exemple':example=True
                chosen.append(r'\begin{'+kind+'}'+('['+title+']' if title else '')+text+r'\end{'+kind+'}')
            summary.append(heading+'\n'+'\n'.join(chosen))
        resume=to_html('\n'.join(summary),[])
    else:
        figures=['cours-'+c.slug]
        body=box('Je prépare',primary_text(c.materiel),'#ffffff','#b6c8da')
        body+=box('Je manipule et je raconte',primary_text(c.manipulation),'#ecfdf5','#10b981')
        body+='<div style="text-align:center;">[IMAGE_1]</div>'
        for j,rule in enumerate(c.lecon,1):body+=box(f'Je retiens {j}',primary_text(rule))
        body+=box('Un exemple expliqué',primary_text(c.exemple),'#ecfdf5','#10b981')
        body+=box('À toi de chercher',primary_text(c.guide),'#ffffff','#b6c8da')
        body+=box('Correction de l’essai guidé',primary_text(c.guide_reponse),'#ecfdf5','#10b981')
        body+=box('Erreur à éviter',primary_text(c.vigilance),'#fff8dc','#e5a000')
        body+=box('Si tu hésites',primary_text(c.aide),'#ecfdf5','#10b981')
        resume=''.join(box('Repère '+str(j),primary_text(rule)) for j,rule in enumerate(c.lecon,1))
        resume+=box('Exemple',primary_text(c.exemple),'#ecfdf5','#10b981')
        resume+=box('Attention',primary_text(c.vigilance),'#fff8dc','#e5a000')
    if not figures:
        figures=['site-'+c.slug];body+='<div style="text-align:center;">[IMAGE_1]</div>'
    names=[name+'_'+GRADE+'.png' for name in figures]
    intro=box('Objectifs',' '.join(primary_text(s) for s in c.objectifs))
    body+=box('Pour progresser','Cherche une question à la fois. Dessine ou manipule si cela t’aide. Explique ton choix, puis vérifie avec le corrigé. Tu peux faire les six questions en plusieurs moments.','#ecfdf5','#10b981')
    header=f'=== {c.titre} - Programme {LABEL}\nDifficulté: medium\nOrdre: {c.numero}\nImages: '+', '.join(names)+f'\n\nTitre: {c.titre}\nDescription: Cours de mathématiques {LABEL}\n\n'
    (ROOT/f'cours_{c.slug}_{GRADE}.txt').write_text(header+WRAP+intro+body+'</div>\n',encoding='utf-8')
    resume+=box('Mon mémo',' • '.join(primary_text(s) for s in c.reperes),'#ecfdf5','#10b981')
    resume+='<div style="text-align:center;">[IMAGE_1]</div>'
    dest=FRONT/'cours/resume'/GRADE;dest.mkdir(parents=True,exist_ok=True)
    (dest/f'resume_{c.slug}_{GRADE}.txt').write_text(f'=== Résumé {c.titre} - {LABEL}\nImages: {names[0]}\n\nTitre: Résumé : {c.titre}\n\n'+WRAP+resume+'</div>\n',encoding='utf-8')
    return figures

def course_figures(cs,figures,book_figures):
    if GRADE.startswith('cm'):
        names=list(dict.fromkeys([name for items in figures.values() for name in items if not name.startswith('site-')]+list(book_figures)))
        target=ROOT/'verifications/rendu-figures';target.mkdir(exist_ok=True)
        tex=target/'figures-cours.tex'
        tex.write_text('\\documentclass[11pt,openany]{book}\n\\usepackage{optitab-livre}\n\\usepackage{figures-geometrie}\n\\begin{document}\n\\pagestyle{empty}\n'+ '\n\\clearpage\n'.join('\\noindent\\input{figures/'+name+'.tex}' for name in names)+'\n\\end{document}\n',encoding='utf-8')
        result=subprocess.run(['lualatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(target),str(tex)],cwd=BOOK,capture_output=True,text=True,encoding='utf-8',errors='replace')
        (target/'compilation.txt').write_text(result.stdout+result.stderr,encoding='utf-8')
        assert result.returncode==0,result.stdout[-2200:]
        import fitz
        doc=fitz.open(target/'figures-cours.pdf');assert len(doc)==len(names),(len(doc),len(names))
        for page,name in zip(doc,names):
            single=fitz.open();single.insert_pdf(doc,from_page=page.number,to_page=page.number)
            save_png(single.tobytes(),ROOT/'images'/f'{name}_{GRADE}.png');single.close()
        doc.close()
        for c in cs:
            for name in figures[c.slug]:
                if name.startswith('site-'):draw(choisir(c,0,0).figure,ROOT/'images'/f'{name}_{GRADE}.png',True)
    else:
        sys.path.insert(0,str(BOOK))
        from dessins import diagram
        from reportlab.pdfgen import canvas
        for c in cs:
            data=io.BytesIO();cv=canvas.Canvas(data,pagesize=(510,205));diagram(cv,c.figure,8,8,494,189);cv.save()
            save_png(data.getvalue(),ROOT/'images'/f'cours-{c.slug}_{GRADE}.png')
        for key,spec in book_figures.items():
            data=io.BytesIO();cv=canvas.Canvas(data,pagesize=(510,230));diagram(cv,spec,8,8,494,214);cv.save()
            save_png(data.getvalue(),ROOT/'images'/f'{key}_{GRADE}.png')
    for key in book_figures:
        name=f'{key}_{GRADE}.png'
        shutil.copy2(ROOT/'images'/name,FRONT/'exercices'/GRADE/'images'/name)

def build(render=True):
    from approfondir import append
    cs=chapters();manifest=[];specs={};figures={};book_figures={};qa=ROOT/'verifications';qa.mkdir(exist_ok=True)
    exdir=FRONT/'exercices'/GRADE;(exdir/'images').mkdir(parents=True,exist_ok=True);(ROOT/'images').mkdir(exist_ok=True)
    for ch in cs:
        figures[ch.slug]=course(ch);chunks=[]
        for level,(cat,diff) in enumerate(CATS):
            for i in range(7):
                e=choisir(ch,i,level);code=f'{ch.slug}_{GRADE}_{level+1}_{i+1}';names=[]
                if e.figure:
                    names=[code+'.png'];specs[code]=e.figure
                    if render:draw(e.figure,exdir/'images'/names[0])
                    if e.correction_figure:
                        names.append(code+'_corrige.png')
                        if render:draw(e.figure,exdir/'images'/names[1],True)
                extra,control=append(ch,e,i,level,book_figures)
                if extra:names.append(f'{extra}_{GRADE}.png')
                chunks.append(render_exercice(ch,e,cat,diff,i+1,names))
                manifest.append(dict(chapitre=ch.numero,slug=ch.slug,code=code,categorie=cat,titre=e.titre,niveau=level,indice=i,questions=len(e.questions),images=names,controles=[q.controle for q in e.questions if q.controle],controle_livre=control,theme=theme(ch)))
        (exdir/f'exercice_{ch.slug}_{GRADE}.txt').write_text('\n===\n\n'.join(chunks),encoding='utf-8')
        print(f'{LABEL} {ch.numero:02} {ch.slug} : cours, fiche, 21 exercices.',flush=True)
    (qa/'manifeste.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (qa/'figures.json').write_text(json.dumps(specs,ensure_ascii=False,indent=2),encoding='utf-8')
    (ROOT/'.gitignore').write_text('__pycache__/\nverifications/rendus/\nverifications/rendu-figures/\n',encoding='utf-8')
    if render:course_figures(cs,figures,book_figures)
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--sans-figures',action='store_true');args=parser.parse_args()
    build(not args.sans_figures)
