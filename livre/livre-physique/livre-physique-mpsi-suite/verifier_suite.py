"""Contrôle de chaque fascicule et rendu Poppler pour relecture visuelle."""
from pathlib import Path
import json,re,subprocess,hashlib,sys,math
import fitz
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent

def numeric(n):
    checks=[]
    def ck(name,a,b,tol=1e-9):
        assert abs(a-b)<=tol,(name,a,b)
        checks.append(dict(nom=name,valeur=float(a),attendu=float(b),tolerance=tol))
    if n==2:
        # Conservation indépendante sur un réseau à deux potentiels.
        VA,VB=np.linalg.solve([[2.5,-1],[-1,2]],[6,0])
        I=np.array([6-VA,VA/2,VA-VB,VB])
        ck('réseau-nœud-A',I[0]-I[1]-I[2],0)
        ck('réseau-nœud-B',I[2]-I[3],0)
        ck('réseau-puissances',6*I[0],I[0]**2+2*I[1]**2+I[2]**2+I[3]**2)
        for R in [0.4,2,10,100]:
            i=12/(R+2);ck(f'Thevenin-bilan-{R}',12*i,2*i*i+R*i*i)
        x=4.0
        for k in range(30):x=2+2*x/(2+x)
        ck('source-DM2-échelle',x,1+math.sqrt(5))
        rs=1000*(1.02/2.02+.5);u0=5*.02/(2*2.02)
        ck('D1-erreur-charge',1-(u0*1e5/(1e5+rs))/u0,.00994951722785864,1e-12)
    if n==3:
        # L'équation et les états initial/final sont vérifiés par leurs formes analytiques.
        for U0,E,tau in [(0,5,.001),(8,3,.01),(2,10,.002)]:
            for t in [0,tau,5*tau]:
                u=E+(U0-E)*math.exp(-t/tau);du=-(U0-E)/tau*math.exp(-t/tau)
                ck(f'RC-résidu-{U0}-{t}',tau*du+u,E)
            C=2e-6;wg=C*E*(E-U0);wj=C*(E-U0)**2/2;de=C*(E**2-U0**2)/2
            ck(f'RC-énergie-{U0}',wg,wj+de)
        for hratio in [.01,.1,.5]:
            N=round(1/hratio);u=0
            for k in range(N):u+=hratio*(1-u)
            ck(f'Euler-récurrence-{hratio}',u,1-(1-hratio)**N)
        rv=1/(1/3e5+1/1e6);tau=1/(1/1e5+1/rv)*1e-5;uf=12*rv/(1e5+rv)
        ck('DM-seuil-avec-voltmètre',-tau*math.log(1-6/uf),.880,0.001)
    if n==4:
        w=10;x0=.03;v0=.4
        for t in [0,.03,.1,.3,1]:
            x=x0*math.cos(w*t)+v0/w*math.sin(w*t)
            v=-w*x0*math.sin(w*t)+v0*math.cos(w*t)
            a=-w*w*x
            ck(f'harmonique-équation-{t}',a+w*w*x,0)
            ck(f'harmonique-énergie-{t}',.2*v*v/2+20*x*x/2,.025)
        # Une étape RK / Euler sert à vérifier l'activité numérique et sa dérive.
        h=.01;x=.05;v=0;E0=(v*v+w*w*x*x)/2
        for k in range(100):x,v=x+h*v,v-h*w*w*x
        ck('Euler-énergie-100-pas',(v*v+w*w*x*x)/2/E0,1.01**100)
        # Raccord à la coupure dans le problème LC.
        L=.01;C=1e-5;E=5;w=1/math.sqrt(L*C);theta=math.pi/2
        us=E*(1-math.cos(theta));i=C*E*w*math.sin(theta)
        ck('D2-énergie-LC',C*us**2/2+L*i**2/2,.00025)
    if n==5:
        ck('TP-second-pic-simule',4*math.exp(-100*2*math.pi/math.sqrt(1000**2-100**2)),2.127,.0005)
        w=10;a=2;x0=.05;v0=0;wd=math.sqrt(w*w-a*a);A=x0;B=(v0+a*x0)/wd
        for t in [0,.05,.3,1]:
            F=A*math.cos(wd*t)+B*math.sin(wd*t)
            Fp=-A*wd*math.sin(wd*t)+B*wd*math.cos(wd*t)
            x=math.exp(-a*t)*F;v=math.exp(-a*t)*(Fp-a*F)
            acc=math.exp(-a*t)*((a*a-wd*wd)*F-2*a*Fp)
            ck(f'amorti-équation-{t}',acc+2*a*v+w*w*x,0)
            ck(f'amorti-énergie-{t}',v*acc+w*w*x*v,-2*a*v*v)
        ck('amorti-initial-x',A,x0);ck('amorti-initial-v',-a*A+wd*B,v0)
        # Vérifier le seuil critique et la fraction d'énergie à même phase.
        z=6.63835206799;ck('critique-seuil',(1+z)*math.exp(-z),.01,1e-11)
        ck('DM-fraction-perdue',1-math.exp(-2*math.log(1.5)),5/9)
        # L'activité RK4 : comparer à l'exact et fermer le bilan énergétique.
        h=.001;y=np.array([.05,0.]);loss=0.;initial=(y[1]**2+100*y[0]**2)/2
        def f(z):return np.array([z[1],-5*z[1]-100*z[0]])
        for k in range(4000):
            old=y.copy();k1=f(y);k2=f(y+h*k1/2);k3=f(y+h*k2/2);k4=f(y+h*k3)
            y+=h*(k1+2*k2+2*k3+k4)/6;loss+=h*5*(old[1]**2+y[1]**2)/2
        wda=math.sqrt(100-2.5**2);exact=.05*math.exp(-10)*(math.cos(4*wda)+2.5/wda*math.sin(4*wda))
        ck('RK4-exact',y[0],exact,1e-10)
        ck('RK4-bilan',.5*(y[1]**2+100*y[0]**2)+loss,initial,1e-7)
    return checks

def verify(n,render=True):
    R=ROOT/f'chapitre-{n:02}';B=R/'build';Q=B/'qa';Q.mkdir(exist_ok=True)
    manifest=json.loads((R/'manifest.json').read_text(encoding='utf-8'))
    checks=manifest['controles']+numeric(n)
    for c in checks:assert abs(c['valeur']-c['attendu'])<=c['tolerance'],c
    tex=(R/'contenu.tex').read_text(encoding='utf-8')
    # Exécuter le code exactement tel qu'il sera lu dans le PDF.
    snippets=re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',tex,flags=re.S)
    assert len(snippets)==1
    env={};exec(compile(snippets[0].strip(),'activite-publiee','exec'),env)
    if n==2:assert abs(env['VA']-3)<1e-12 and abs(env['VB']-1.5)<1e-12
    if n==3:assert np.isfinite(env['u']).all() and abs(env['e'].max()-5)<1e-8 and 0<=env['u'].min()<=env['u'].max()<5
    if n==4:assert abs(env['energy'][-1]/env['energy'][0]-(1+env['h']**2*env['w']**2)**env['N'])<1e-9
    if n==5:assert abs(env['energy'][-1]+env['loss'][-1]-env['energy'][0])<1e-7
    checks.append(dict(nom='code-publie-execute',valeur=1,attendu=1,tolerance=0))
    assert not any(ord(x)<32 and x not in '\n\r\t' for x in tex)
    exs=re.findall(r'\\ex\{(E\d+)\}',tex);sols=re.findall(r'\\sol\{(E\d+)\}',tex)
    assert exs==sols==[f'E{i:02}' for i in range(1,25)]
    log=(B/'main.log').read_text(encoding='utf-8',errors='replace')
    bad=[s for s in log.splitlines() if any(x in s for x in ['Overfull','Missing character','undefined references','multiply defined','Fatal error'])]
    aux=(B/'main.aux').read_text(encoding='utf-8');labels=re.findall(r'\\Page\{[^}]*\}\{[^}]*\}\{([^}]*)\}',tex)
    loc={}
    for lab in labels:
        m=re.search(r'\\newlabel\{'+re.escape(lab)+r'\}\{\{[^}]*\}\{(\d+)\}',aux);assert m,lab
        loc[lab]=int(m.group(1))
    doc=fitz.open(B/'main.pdf');outside=[];collisions=[]
    for i,p in enumerate(doc):
        spans=[s for b in p.get_text('dict')['blocks'] if b['type']==0 for l in b['lines'] for s in l['spans']]
        for s in spans:
            b=fitz.Rect(s['bbox'])
            if b.x0<-.5 or b.y0<-.5 or b.x1>p.rect.width+.5 or b.y1>p.rect.height+.5:outside.append(dict(page=i+1,texte=s['text'],bbox=list(b)))
        long=[s for s in spans if len(re.findall(r'[A-Za-zÀ-ÿ]',s['text']))>=4 and s['size']>=6.5]
        for j,s in enumerate(long):
            r=fitz.Rect(s['bbox'])
            for t in long[j+1:]:
                q=fitz.Rect(t['bbox']);hit=r&q
                if not hit.is_empty and hit.width>4 and hit.height>min(r.height,q.height)*.45 and hit.get_area()>min(r.get_area(),q.get_area())*.16:collisions.append(dict(page=i+1,a=s['text'],b=t['text']))
    links=[l for p in doc for l in p.get_links()]
    broken=[l for l in links if l['kind']==fitz.LINK_GOTO and not 0<=l.get('page',-1)<len(doc)]
    expected=1+len(labels);pagination=list(loc.values())==list(range(2,expected+1)) and len(doc)==expected
    figs=re.findall(r'\\fig\{([^}]+)\}',tex)
    report=dict(chapitre=n,titre=manifest['titre'],pages=len(doc),pages_prevues=expected,pagination_conforme=pagination,positions=loc,exercices=len(exs),defis=3,dm=1,ds=1,sources=manifest['sources'],placements_figures=len(figs),figures_distinctes=len(set(figs)),controles=checks,erreurs_compilation=bad,textes_hors_page=outside,collisions_candidates=collisions,liens=len(links),liens_invalides=broken,sha256=hashlib.sha256((B/'main.pdf').read_bytes()).hexdigest())
    (B/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k in ['chapitre','pages','pages_prevues','pagination_conforme','erreurs_compilation','textes_hors_page','collisions_candidates']},ensure_ascii=False),flush=True)
    if render:
        for pattern in ['page-*.png','planche-*.jpg']:
            for old in Q.glob(pattern):old.unlink()
        p=subprocess.run(['pdftoppm','-r','100','-png',str(B/'main.pdf'),str(Q/'page')],capture_output=True)
        assert p.returncode==0,p.stderr
        paths=sorted(Q.glob('page-*.png'));assert len(paths)==len(doc)
        for start in range(0,len(paths),4):
            sheet=Image.new('RGB',(1360,1920),'#e8ebef')
            for j,p in enumerate(paths[start:start+4]):
                im=Image.open(p).convert('RGB');im.thumbnail((650,920))
                tile=Image.new('RGB',(680,960),'#e8ebef');tile.paste(im,((680-im.width)//2,22));ImageDraw.Draw(tile).text((14,936),f'Chapitre {n:02} / Page {start+j+1}',fill='black');sheet.paste(tile,((j%2)*680,(j//2)*960))
            sheet.save(Q/f'planche-{start+1:02}-{start+min(4,len(paths)-start):02}.jpg',quality=88)
    assert not bad and not outside and not broken and pagination,'Corriger le rapport avant livraison.'
    return report

if __name__=='__main__':
    ns=[int(x) for x in sys.argv[1:] if x.isdigit()] or [2,3,4,5]
    for n in ns:verify(n,'--sans-rendu' not in sys.argv)
