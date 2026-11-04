"""Construit les 20 cours, 20 fiches et 420 exercices du site, sans accès réseau."""
import argparse
import importlib
import json
import re
import sys
from hashlib import sha256
from pathlib import Path
from modele_5e import ROOT, FRONT, REPO, CATS, dm, render_exercice

sys.path.insert(0, str(ROOT / 'sources'))
import nombres, algebre, geometrie, donnees
from variantes import choisir
BUILDERS = nombres.BUILDERS | algebre.BUILDERS | geometrie.BUILDERS | donnees.BUILDERS

BOOK = REPO / 'livre/livre-maths/livre-cinquieme'
sys.path.insert(0, str(BOOK))
for source in sorted(BOOK.glob('contenu_*.py')):
    importlib.import_module(source.stem)
from modele import CHAPITRES

BOX = {
    'definition': ('Définition', '#e8f4fd', '#3498db'),
    'propriete': ('Propriété', '#e8f4fd', '#3498db'),
    'exemple': ('Exemple expliqué', '#ecfdf5', '#10b981'),
    'savoirfaire': ('Méthode', '#ecfdf5', '#10b981'),
    'attention': ('Erreur à éviter', '#fff8dc', '#e5a000'),
}
WRAP = '<div style="background:#f9f9f9;padding:20px;border-radius:12px;font-family:Arial,sans-serif;line-height:1.7;color:#2c3e50;">'


def box(titre, contenu, couleur='#e8f4fd', bord='#3498db'):
    return f'<div style="background:{couleur};border-left:5px solid {bord};padding:15px;margin:16px 0;border-radius:6px;"><p style="margin:0;"><strong>{titre} :</strong> {contenu}</p></div>'


def table_html(match):
    raw = match[1].replace('\\toprule', '').replace('\\midrule', '\\\\').replace('\\bottomrule', '')
    rows = [r.strip() for r in re.split(r'\\\\', raw) if r.strip()]
    out = ['<div style="overflow-x:auto;margin:15px 0;"><table style="width:100%;min-width:300px;border:2px solid #3498db;border-collapse:collapse;">']
    for j,row in enumerate(rows):
        tag='th' if j==0 else 'td'
        out.append('<tr>')
        for cell in row.split('&'):
            style='background:#3498db;color:white;' if j==0 else 'background:white;'
            out.append(f'<{tag} style="border:1px solid #b6c8da;padding:10px;text-align:center;{style}">{cell.strip()}</{tag}>')
        out.append('</tr>')
    return ''.join(out)+'</table></div>'


def to_html(raw, figures):
    raw = re.sub(r'\\begin\{center\}\\renewcommand\{\\arraystretch\}\{1\.35\}\\begin\{tabular\}\{[^}]*\}(.*?)\\end\{tabular\}\\end\{center\}', table_html, raw, flags=re.S)
    raw = re.sub(r'\\essSection\{(\d+)\}\{([^}]+)\}', lambda x: f'<h2 style="color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:8px;">{x[1]}. {x[2]}</h2>', raw)
    def env(match):
        kind,title,text = match[1],match[2],match[3]
        label,col,border=BOX[kind]
        return box(title or label,text,col,border)
    raw = re.sub(r'\\begin\{(definition|propriete|exemple|savoirfaire|attention)\}(?:\[([^]]+)\])?(.*?)\\end\{\1\}',env,raw,flags=re.S)
    raw = re.sub(r'\\texttt\{([^}]+)\}',lambda x:'<code>'+x[1].replace('*','&#42;')+'</code>',raw)
    def figure(match):
        nom=match[1]
        if nom not in figures: figures.append(nom)
        return f'<div style="text-align:center;margin:18px 0;">[IMAGE_{figures.index(nom)+1}]</div>'
    raw = re.sub(r'@FIG:([^@]+)@',figure,raw)
    raw=raw.replace('\\%', '%').replace('~',' ')
    raw=dm(raw)
    # Une longue égalité reste consultable sur téléphone sans élargir la page.
    return re.sub(r'\$([^$\n]+)\$',lambda x: '<span style="display:inline-block;max-width:100%;overflow-x:auto;vertical-align:middle;padding:3px 0;">'+x[0]+'</span>' if len(x[1])>28 else x[0],raw)


def build_pages(c):
    figures=[]
    objectifs=' '.join(c.objectifs)
    intro = box('Objectifs du chapitre',objectifs)
    intro += box('Avant de commencer',' '.join(c.prerequis),'#ffffff','#b6c8da')
    body=to_html('\n'.join(c.cours),figures)
    if not figures:
        figures.append('cours-'+c.slug)
        body+='\n<div style="text-align:center;">[IMAGE_1]</div>'
    conclusion=box('Comment travailler','Lire les exemples, refaire les calculs sans regarder, puis avancer dans les 7 exercices Découverte, les 7 Entraînements et les 7 Problèmes. Chaque exercice comporte au moins six questions corrigées.','#ecfdf5','#10b981')
    names=[f'{f}_5e.png' for f in figures]
    head=f'=== {c.titre} - Programme 5ème\nDifficulté: medium\nOrdre: {c.numero}\nImages: '+', '.join(names)+f'\n\nTitre: {c.titre}\nDescription: Cours de 5ème : '+objectifs+'\n\n'
    (ROOT/f'cours_{c.slug}_5e.txt').write_text(head+WRAP+intro+body+conclusion+'</div>\n',encoding='utf-8')
    # La fiche reprend les propriétés et un exemple par section, avec tous les pièges.
    resume=[]
    for page in c.cours:
        section=re.search(r'\\essSection\{\d+\}\{[^}]+\}',page)[0]
        items=re.findall(r'\\begin\{(definition|propriete|exemple|savoirfaire|attention)\}(?:\[([^]]+)\])?(.*?)\\end\{\1\}',page,re.S)
        kept=[]
        seen_example=False
        for kind,title,text in items:
            if kind=='exemple':
                if seen_example: continue
                seen_example=True
            kept.append(r'\begin{'+kind+'}'+('['+title+']' if title else '')+text+r'\end{'+kind+'}')
        resume.append(section+'\n'+'\n'.join(kept))
    fiche=to_html('\n'.join(resume),[])
    fiche+=box('Mémo du chapitre',' • '.join(c.reperes),'#ecfdf5','#10b981')
    fiche+='\n<div style="text-align:center;">[IMAGE_1]</div>'
    header=f'=== Résumé {c.titre} - 5ème\nImages: {names[0]}\n\nTitre: Résumé : {c.titre}\n\n'
    dest=FRONT/'cours/resume/5e'
    dest.mkdir(parents=True,exist_ok=True)
    (dest/f'resume_{c.slug}_5e.txt').write_text(header+WRAP+fiche+'</div>\n',encoding='utf-8')
    return figures


def build(slugs=None, render=True):
    from figures_5e import draw, render_course_figures
    manifest=[]
    figure_specs={}
    exdir=FRONT/'exercices/5e'
    (exdir/'images').mkdir(parents=True,exist_ok=True)
    (ROOT/'images').mkdir(parents=True,exist_ok=True)
    for c in CHAPITRES:
        if slugs and c.slug not in slugs: continue
        figures=build_pages(c)
        chunks=[]
        for level,(cat,diff) in enumerate(CATS):
            for indice in range(7):
                e=choisir(c.slug,indice,level,BUILDERS[c.slug])
                code=f'{c.slug}_5e_{level+1}_{indice+1}'
                names=[]
                if e.figure:
                    names=[code+'.png']
                    figure_specs[code]=e.figure
                    if render: draw(e.figure,exdir/'images'/names[0])
                if e.correction_figure:
                    names.append(code+'_corrige.png')
                    if render: draw(e.figure,exdir/'images'/names[1],True)
                chunks.append(render_exercice(c,e,cat,diff,indice+1,names))
                manifest.append(dict(chapitre=c.numero,slug=c.slug,code=code,categorie=cat,
                    titre=e.titre,niveau=level,indice=indice,questions=len(e.questions),images=names,
                    controles=[x.controle for x in e.questions if x.controle]))
        (exdir/f'exercice_{c.slug}_5e.txt').write_text('\n===\n\n'.join(chunks),encoding='utf-8')
        print(f'{c.numero:02} {c.slug}: cours, fiche, 21 exercices, '+str(sum(e['questions'] for e in manifest if e['slug']==c.slug))+' questions')
    qa=ROOT/'verifications'
    qa.mkdir(exist_ok=True)
    (qa/'manifeste.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    (qa/'figures.json').write_text(json.dumps(figure_specs,ensure_ascii=False,indent=2),encoding='utf-8')
    if render: render_course_figures(CHAPITRES,BOOK)
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('slugs',nargs='*')
    parser.add_argument('--sans-figures',action='store_true')
    args=parser.parse_args()
    build(None if not args.slugs or args.slugs==['all'] else args.slugs,not args.sans_figures)
