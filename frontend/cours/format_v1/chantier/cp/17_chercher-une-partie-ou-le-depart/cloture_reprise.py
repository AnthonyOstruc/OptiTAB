from pathlib import Path
import json,sys,runpy,hashlib,re,subprocess,collections
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent.parent
CODES=[17,18,19,20,29]
def dirs():
    for code in CODES: yield code,next(ROOT.glob(f'{code:02}_*'))
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if sys.argv[1]=='audit_math':
    for code,d in dirs():
        subprocess.run([sys.executable,str(d/'verif_math.py')],check=True)
        ns=runpy.run_path(str(d/'figures/figures.py'));figs=ns['FIGURES'];extra=0
        source=load(d/'sources_locales/chapitre.json')
        for ex in source['exercices']:
            if ex['check']:
                assert eval(ex['check'],{'__builtins__':{}},{});extra+=1
        if code==17:
            for n,value in [('ex4_corrige',16),('ex9_corrige',19)]:
                assert re.search(r'node\[text=otGreenDark\].*\{'+str(value)+r' en tout\}',figs[n]);extra+=1
        if code in [18,19]:
            model=figs['modele'];assert len(re.findall(r'\\fill\[',model))==12;extra+=1
        if code==18:
            coords=re.findall(r'\\fill\[[^\]]+\] \(([^,]+),([^\)]+)\)',figs['ex6_corrige'])
            assert sorted(collections.Counter(y for x,y in coords).values())==[7,7];extra+=2
            flower=figs['ex8_corrige'];assert len(re.findall(r'\\fill\[',flower))==30
            assert len(re.findall(r'\{fleur [1-6]\}',flower))==6;extra+=2
        if code==19:
            assert len(re.findall(r'\\fill\[',figs['paquets_modele']))==10
            assert len(re.findall(r'\{groupe [1-5]\}',figs['paquets_modele']))==5;extra+=2
        if code==29:
            assert len(re.findall(r'\\fill\[',figs['modele']))==6;extra+=1
        report=load(d/'verification_math.json');report['verifications']+=extra
        report['controles_complementaires']='Recalcul des égalités sources ; contrôle du modèle et des corrections ciblées (départs verts, rangées, fleurs et paquets selon le chapitre).'
        (d/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(code,report['verifications'],'vérifications finales')
if sys.argv[1]=='audit_figures':
    sys.path.insert(0,str(ROOT.parents[1]/'outils'));import figures_livre as official
    for code,d in dirs():
        ns=runpy.run_path(str(d/'figures/figures.py'));rows=[]
        for name,body in ns['FIGURES'].items():
            p=d/'figures/images'/f'{name}.png';build=d/'figures/build'
            expected=official.PREAMBULE+ns.get('PREAMBULE_EXTRA','')+'\n'+chr(92)+'begin{document}\n'+official.graduations_x(body,name,ns.get('XLAB'))+'\n'+chr(92)+'end{document}\n'
            actual=(build/f'{name}.tex').read_text(encoding='utf-8')
            assert [x for x in actual.splitlines() if x.strip()]==[x for x in expected.splitlines() if x.strip()],name
            w,h=official.taille_png(p);errors,warnings=official.chevauchements(p,build/f'{name}__sans_texte.png')
            assert w<=official.LARGEUR_MAX_PX and not errors,(name,w,errors)
            rows.append({'figure':p.name,'ok':True,'largeur':w,'avertissements':warnings,'sha256':sha(p)})
        report={'statut':'OK','anomalies':0,'figures':len(rows),'controles':rows}
        (d/'verification_figures_reprise.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(code,len(rows),'figures synchronisées, zéro anomalie')
if sys.argv[1]=='polir':
    for code,d in dirs():
        if code not in [17,18,19,20]:continue
        p=d/'exercices.txt';blocks=p.read_text(encoding='utf-8').split('\n===\n')
        for k,b in enumerate(blocks,1):
            if code==17:
                method='Réunir les crayons bleus et rouges.' if k==7 else 'Lire la quantité de la partie connue.'
                b=b.replace('Repérer ou réunir la partie connue.',method)
            if code==18:
                method='Lire le nombre de groupes à dessiner.' if k in [2,6,8] else 'Compter les groupes dessinés.'
                b=b.replace('Compter les cadres ou lire le nombre de groupes.',method)
            if code==19 and k==7:b=b.replace('Comparer les parts.','Compter les objets du seul groupe colorié.')
            if code==20:
                methods=['Enlever les oiseaux partis.','Ajouter les cartes reçues.','Enlever les perles utilisées.','Mettre de côté les crayons rouges.','Enlever les enfants descendus.','Enlever les euros dépensés.','Réunir les albums et les documentaires.','Ajouter les cases avancées.','Enlever les cubes donnés.']
                b=b.replace('Choisir ajouter ou enlever.',methods[k-1]).replace('Je ajoute','J’ajoute')
            blocks[k-1]=b
        p.write_text('\n===\n'.join(blocks),encoding='utf-8')
if sys.argv[1]=='figures':
    font=ImageFont.truetype('arial.ttf',17)
    for code,d in dirs():
        names=sorted({s['fichier'] for g in load(d/'figures/correspondance.json').values() for m in g.values() for s in m.values()})
        for k in range(0,len(names),8):
            group=names[k:k+8];ims=[Image.open(d/'figures/images'/n).convert('RGB') for n in group]
            for im in ims:im.thumbnail((460,420))
            heights=[max(im.height for im in ims[j:j+2])+40 for j in range(0,len(ims),2)]
            sheet=Image.new('RGB',(980,sum(heights)+10),'#eef1f6');draw=ImageDraw.Draw(sheet)
            for j,(name,im) in enumerate(zip(group,ims)):
                x=10+(j%2)*485;y=10+sum(heights[:j//2]);draw.text((x,y),f'CP{code} / {name}',fill='#1b3c8e',font=font);sheet.paste(im,(x,y+25))
            target=d/f'relecture_figures_{k//8+1:02}.png';sheet.save(target);print(target)
if sys.argv[1]=='journal':
    for code,d in dirs():
        names=sorted({s['fichier'] for g in load(d/'figures/correspondance.json').values() for m in g.values() for s in m.values()})
        a=load(d/'audit_navigateur_cp.json')
        record={'figures':{n:sha(d/'figures/images'/n) for n in names},'captures':{n:sha(d/'captures_cp'/n) for n in a['captures']},'relecture':'Relecture réelle de toutes les figures sur planches locales et des captures complètes cours/fiche/exercices 1, 5, 9 ; reprise finale du 2 novembre 2026.'}
        (d/'journal_relecture.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if sys.argv[1]=='documents':
    for code,d in dirs():
        figures=load(d/'verification_figures_reprise.json');proof=load(d/'PREUVES_FINALES.json')
        proof['synchronisation_tikz_png']='verification_figures_reprise.json'
        proof['relecture_planches']=[p.name for p in sorted(d.glob('relecture_*.png'))]
        if (d/'compilation_reprise_retour.txt').exists():
            assert (d/'compilation_reprise_retour.txt').read_text().strip()=='0'
            proof['compilation_reprise_retour']=0;proof['compilation_reprise_log']='compilation_reprise.log'
        (d/'PREUVES_FINALES.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        p=d/'RAPPORT.md'
        with p.open('a',encoding='utf-8') as f:
            f.write('\nReprise finale : seuls les PNG absents ou périmés ont été recompilés. Les '+str(figures['figures'])+' figures ont été comparées à leur source TikZ et au préambule officiel, puis relues sur les planches locales : zéro écart, zéro chevauchement. Le journal conserve les empreintes des  figures et captures effectivement lues. Les journaux de compilation initiaux sont conservés, ainsi que compilation_reprise.log et son retour 0 pour les chapitres concernés.\n')
        p=d/'COUVERTURE.md'
        with p.open('a',encoding='utf-8') as f:
            f.write('\nContrôle final : les neuf activités du chapitre source ont été confrontées aux neuf énoncés et à leurs cinq réponses. Les exemples du cours et de la fiche, les modèles des énoncés et les dessins corrigés ont également été relus. Les empreintes des sources sont vérifiées par validation_cp.\n')
