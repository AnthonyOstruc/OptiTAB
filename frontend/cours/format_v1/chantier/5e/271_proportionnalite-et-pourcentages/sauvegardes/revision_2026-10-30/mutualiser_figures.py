# -*- coding: utf-8 -*-
"""Mutualisation de schémas de travail non gradués ; valeurs dans le texte."""
from pathlib import Path
import importlib.util, re, json
ROOT=Path(__file__).resolve().parent.parent
def load(path):
    spec=importlib.util.spec_from_file_location('figs',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m.FIGURES
def neutral(code,kind):
    # A schema can be shared when all numerical labels and graduations are absent.
    code=re.sub(r'\\node\[[^\]]*\][^;]*?\{\$[^;]*?\\circ[^;]*?;', '',code)
    if kind=='triangle':
        code=re.sub(r'\\node\[[^\]]*\][^;]*?\{\$[^;]*?\\text\{ cm\}[^;]*?;', '',code)
    if kind=='aire':
        code=re.sub(r'\\node\[[^\]]*\][^;]*?\{\$[^;]*?\\text\{ m\}[^;]*?;', '',code)
    return code

for d in ROOT.iterdir():
    if not d.is_dir() or not d.name[:3].isdigit() or not 272<=int(d.name[:3])<=275:continue
    n=int(d.name[:3]);fd=d/'figures';old=load(fd/'figures.py');corr=json.loads((fd/'correspondance.json').read_text(encoding='utf-8'));new={}
    if n==272:
        new['cours_repere']=old['cours_repere']
        new['jardin_schema']=r'''\begin{tikzpicture}
\draw[geoVecteur] (-3.3,0)--(3.3,0);\draw[geoVecteur] (0,-2.4)--(0,2.4);
\draw[geoTrait,fill=otSky,fill opacity=.4] (-2.5,1.6)--(2.5,1.6)--(2.5,-1.6)--(-2.5,-1.6)--cycle;
\node[anchor=south east,inner sep=4pt] at (-2.5,1.6) {$A$};
\node[anchor=south west,inner sep=4pt] at (2.5,1.6) {$B$};
\node[anchor=north west,inner sep=4pt] at (2.5,-1.6) {$C$};
\node[anchor=north east,inner sep=4pt] at (-2.5,-1.6) {$D$};
\node[anchor=north east,inner sep=4pt] at (0,0) {$O$};
\end{tikzpicture}'''
        for eid,positions in corr['exercices'].items():
            for p,it in positions.items():it.update(fichier='jardin_schema.png',alt='Schéma sans échelle : rectangle ABCD centré sur l’origine O ; coordonnées exactes dans l’énoncé.')
    elif n==273:
        new={k:neutral(old[src],'angles') for k,src in [('rosace_schema','rosace_40'),('rosace_schema_corrige','rosace_40_corrige'),('paralleles_schema','paralleles_45'),('paralleles_schema_corrige','paralleles_45_corrige')]}
        for kind,ids in corr.items():
            for eid,positions in ids.items():
                for p,it in positions.items():
                    rosace='secantes' in it['fichier'] or 'rosace' in it['fichier'];name=('rosace' if rosace else 'paralleles')+'_schema'+('_corrige' if kind=='exercices' and p=='2' else '')
                    it.update(fichier=name+'.png',alt='Schéma sans échelle : '+('droites sécantes AB et CD en O et bissectrice OE.' if rosace else 'droites parallèles d et e coupées par une sécante en A et B.'))
    elif n==274:
        new={'cours_angles':old['cours_angles'],'triangle_schema':neutral(old['triangle_5_35_45'],'triangle'),'aire_schema':neutral(old['aire_8_3'],'aire')}
        for kind,ids in corr.items():
            for eid,positions in ids.items():
                for p,it in positions.items():
                    name='cours_angles' if it['fichier']=='cours_angles.png' else ('aire_schema' if 'aire' in it['fichier'] or 'hauteur' in it['fichier'] else 'triangle_schema')
                    it.update(fichier=name+'.png',alt='Schéma du triangle ABC : '+('hauteur AH et médiane AM ; données dans le texte.' if name=='aire_schema' else 'angles et longueur de la base précisés dans le texte.'))
    else:
        for name,src in [('centrale_enonce','motif_2_1_enonce'),('centrale_corrige','motif_2_1_corrige'),('axiale_enonce','motif_3_1_enonce'),('axiale_corrige','motif_3_1_corrige')]:
            code=old[src]
            code=re.sub(r'\\draw\[otRule[^;]*;', '',code)
            code=re.sub(r'\\node\[coteTexte[^;]*;', '',code)
            # Use the same unit on both axes; omit numerical graduations.
            code=re.sub(r'\[x=[0-9.]+cm,y=[0-9.]+cm\]', '[x=.6cm,y=.6cm]',code)
            new[name]=code
        for kind,ids in corr.items():
            for eid,positions in ids.items():
                for p,it in positions.items():
                    if kind=='cours':central='centrale' in it['fichier'];enonce=False
                    else:
                        ex=next(x for x in re.split(r'^===\s*$',(d/'exercices.txt').read_text(encoding='utf-8'),flags=re.M) if f'Id: {eid}\n' in x)
                        central='symétrie centrale' in ex.split('Étapes:')[0];enonce=p=='1'
                    name=('centrale' if central else 'axiale')+('_enonce' if enonce else '_corrige')
                    it.update(fichier=name+'.png',alt='Schéma sans graduation : triangle ABC '+('et image A′B′C′ ' if not enonce else '')+'pour une symétrie '+('centrale de centre O.' if central else 'd’axe vertical.'))
    text=(d/'exercices.txt').read_text(encoding='utf-8')
    if n in (272,273,275):
        text=text.replace('[IMAGE_1]','[IMAGE_1]\n\n::: remarque Lecture du schéma\nSchéma sans échelle ni graduation numérique : les valeurs exactes sont celles de l’énoncé.\n:::')
    (d/'exercices.txt').write_text(text,encoding='utf-8')
    (fd/'figures.py').write_text('# -*- coding: utf-8 -*-\n"""Schémas de travail mutualisés, sans échelle numérique."""\nFIGURES = {\n'+''.join(repr(k)+': r"""\n'+v+'\n""",\n' for k,v in new.items())+'}\n',encoding='utf-8')
    (fd/'correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # Les éventuels anciens produits de compilation sont conservés.
    print(n,len(new),'figures utiles')
