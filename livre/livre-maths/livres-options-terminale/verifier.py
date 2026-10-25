from pathlib import Path
import sys,re,json,hashlib,ast,math
import fitz
from PIL import Image,ImageOps,ImageDraw
from construire import load

ROOT=Path(__file__).resolve().parents[1]
option=sys.argv[1];book=ROOT/('livre-maths-'+option);data=load(option)
checks=[]
def check(name,ok,detail=None):
    checks.append(dict(controle=name,valide=bool(ok),detail=detail))
    if not ok:print('ECHEC',name,detail)

for i,c in enumerate(data.CHAPTERS,1):
    check(f'Chapitre {i} : 12 exercices',len(c['ex'])==12)
    for j,e in enumerate(c['ex'],1):
        check(f'{i}.{j} : réponses à toutes les questions',len(e['q'])==len(e['a']) and all(e['a']))
        check(f'{i}.{j} : progression',e['level']==(1 if j<=4 else 2 if j<=8 else 3))

log=(book/'build/main.log').read_text(encoding='utf-8',errors='replace')
check('Aucun caractère manquant','Missing character' not in log)
check('Aucun renvoi indéfini',not re.search(r'(?:Reference|Hyper reference).*?undefined|undefined references',log))
over=re.findall(r'Overfull \\[hv]box[^\n]*',log)
check('Aucun débordement de boîte',not over,over)
check('Renvois stabilisés','Rerun to get' not in log and 'Label(s) may have changed' not in log)
aux=(book/'build/main.aux').read_text(encoding='utf-8')
for i,c in enumerate(data.CHAPTERS,1):
    for j in range(1,len(c['ex'])+1):
        check(f'{i}.{j} : énoncé et solution dans le PDF',f'\\newlabel{{exo-{i}-{j}}}' in aux and f'\\newlabel{{cor-{i}-{j}}}' in aux)

snippets=[]
for f in sorted(book.rglob('*.tex')):
    if 'build' in f.parts:continue
    for idx,code in enumerate(re.findall(r'\\begin\{python\}\s*\n(.*?)\\end\{python\}',f.read_text(encoding='utf8'),re.S),1):
        ast.parse(code);namespace={};exec(compile(code,str(f),'exec'),namespace)
        snippets.append(dict(source=f.relative_to(book).as_posix(),numero=idx,code=code))
        check(f'Python : {f.name}/{idx} syntaxe et exécution',True)
        if 'seuil_reserve' in namespace:check('Seuil exécuté : réserve',namespace['seuil_reserve'](145)==11)
        if 'dichotomie' in namespace:
            a,b=namespace['dichotomie'](lambda x:x**3+x-1,0,1,1e-6)
            check('Dichotomie exécutée : signe et précision',a**3+a-1<=0<=b**3+b-1 and b-a<=1e-6)
        if 'euler_refroidissement' in namespace:check('Euler exécuté : étapes et temps',namespace['euler_refroidissement'](1,2)==[(0.,80.),(1.,68.),(2.,58.4)])
        if 'rectangles' in namespace:check('Rectangles exécutés',abs(namespace['rectangles'](lambda x:x*x,0,1,4)-7/32)<1e-14)
        if 'binom_cumul' in namespace:check('Cumul exécuté',abs(namespace['binom_cumul'](4,.2,1)-.8192)<1e-14)
        if 'frequences' in namespace:
            vals=namespace['frequences'](100,.5,1000)
            check('Échantillons : taille, bornes et moyenne',len(vals)==1000 and all(0<=v<=1 for v in vals) and abs(sum(vals)/len(vals)-.5)<.015)
        if 'termes_affines' in namespace:check('Suite exécutée : indices',namespace['termes_affines'](0,2,1,3)==[0,1,3,7])
        if 'moyenne_des' in namespace:
            m,s,p=namespace['moyenne_des'](100,5000)
            check('Simulation moyennes : dispersion',abs(m-3.5)<.02 and abs(s-math.sqrt(35/12)/10)<.01 and 0<=p<=1,[m,s,p])
        if 'bezout' in namespace:
            for a,b in [(252,198),(35,12),(7,26),(17,0)]:
                d,u,v=namespace['bezout'](a,b)
                check(f'Bézout exécuté {a},{b}',d==math.gcd(a,b) and a*u+b*v==d)
        if 'crible' in namespace:
            check('Crible exécuté 20',namespace['crible'](20)==[2,3,5,7,11,13,17,19])
            check('Crible bornes 0 et 1',namespace['crible'](0)==namespace['crible'](1)==[])
        if 'facteurs' in namespace:check('Décomposition exécutée',namespace['facteurs'](180)==[2,2,3,3,5] and namespace['facteurs'](223)==[223])
        if 'distribution' in namespace:
            r=namespace['distribution']([1,0],[[.8,.2],[.3,.7]],2)
            check('Distribution exécutée',max(abs(a-b) for a,b in zip(r,[.7,.3]))<1e-14)

pdf=book/'build/main.pdf';doc=fitz.open(pdf)
check('Format A4',all(abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1 for p in doc))
check('Toutes les pages comportent du texte',all(len(p.get_text().strip())>25 for p in doc))
text='\n'.join(p.get_text() for p in doc)
check('Aucun marqueur de remplacement','\ufffd' not in text and '\x00' not in text)
check('Aucun renvoi en attente','??' not in text)
links=[link for p in doc for link in p.get_links()]
check('Liens de navigation',len(links)>2*len(data.CHAPTERS)*12,len(links))
check('Destinations des liens internes',all(0<=l['page']<len(doc) for l in links if l['kind']==fitz.LINK_GOTO))
outside=[]
for n,p in enumerate(doc,1):
    for b in p.get_text('dict')['blocks']:
        if 'lines' not in b:continue
        for line in b['lines']:
            for span in line['spans']:
                r=fitz.Rect(span['bbox'])
                if r.x0<-.5 or r.y0<-.5 or r.x1>p.rect.width+.5 or r.y1>p.rect.height+.5:outside.append([n,span['text'],list(r)])
check('Aucun texte hors page',not outside,outside[:20])
check('Métadonnées titre',data.NOM in doc.metadata['title'])
figs=list((book/'images').glob('*.pdf'))
check('Figures vectorielles présentes',len(figs)>=15,len(figs))
if hasattr(data,'COVERAGE'):
    for code,desc,ch,ex in data.COVERAGE:check(f'Programme {code}',ch<=len(data.CHAPTERS) and f'{code}' in text)

qa=ROOT/'tmp/pdfs'/('qa-'+option);qa.mkdir(parents=True,exist_ok=True)
for n,p in enumerate(doc,1):
    target=qa/f'page-{n:03}.png'
    p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(target)
for start in range(0,len(doc),12):
    sheet=Image.new('RGB',(3*420,4*620),'#e7eaf0');draw=ImageDraw.Draw(sheet)
    for j in range(start,min(start+12,len(doc))):
        im=Image.open(qa/f'page-{j+1:03}.png');im.thumbnail((400,580))
        x=(j-start)%3*420+(420-im.width)//2;y=(j-start)//3*620+24
        sheet.paste(im,(x,y));draw.text((x,y-18),f'Page PDF {j+1}',fill='#1B3C8E')
    sheet.save(qa/f'planche-{start//12+1:02}.png')
report=dict(option=data.NOM,pages=len(doc),exercices=sum(len(c['ex']) for c in data.CHAPTERS),questions=sum(len(e['q']) for c in data.CHAPTERS for e in c['ex']),figures=len(figs),liens=len(links),signets=len(doc.get_toc()),sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),controles=checks,python=snippets)
(book/'build/verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['controles','python']},ensure_ascii=False,indent=2))
print('Contrôles :',len(checks),'Échecs :',sum(not c['valide'] for c in checks))
sys.exit(1 if any(not c['valide'] for c in checks) else 0)
