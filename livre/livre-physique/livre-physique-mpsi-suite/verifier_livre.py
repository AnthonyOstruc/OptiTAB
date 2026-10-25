"""Audit scientifique, structurel, liens, géométrie et rendu du livre unique."""
from pathlib import Path
import json,re,hashlib,subprocess,sys,math,importlib
import numpy as np
import fitz
from PIL import Image,ImageDraw
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from assembler_livre import OUT,balanced
from verifier_suite import numeric

def science():
    out=[]
    def ck(name,a,b,tol=1e-9):
        assert abs(a-b)<=tol,(name,a,b)
        out.append(dict(nom=name,valeur=float(a),attendu=float(b),tolerance=tol))
    for n in range(6,11):
        ch=importlib.import_module(f'chapitre{n:02}').create()
        out+=ch.checks
        for v in ch.checks:assert abs(v['valeur']-v['attendu'])<=v['tolerance'],v
        s=(OUT/f'chapitres/ch{n:02}.tex').read_text(encoding='utf-8')
        blocks=re.findall(r'\\begin\{verbatim\}(.*?)\\end\{verbatim\}',s,re.S)
        assert len(blocks)==1
        env={};exec(compile(blocks[0].strip(),f'chapitre-{n}-code-publie','exec'),env)
        if n==6:
            for q,xi,xc in env['peaks']:
                ck(f'C6-code-courant-Q{q}',xi,1,1.1e-4)
                ck(f'C6-code-tension-Q{q}',xc,math.sqrt(1-1/(2*q*q)) if q>1/math.sqrt(2) else .001,1.1e-4)
        if n==7:
            t=env['t'];e=env['e']
            # La grille inclut le dernier point ; l'enlever pour moyenner exactement 3 périodes.
            for fc,sig in env['outputs'].items():
                ck(f'C7-code-moyenne-{fc}',sig[:-1].mean(),1)
                H=1/(1+1j*env['n']*100/fc)
                ck(f'C7-code-efficace-{fc}',np.mean(sig[:-1]**2),1+np.sum((env['A']*abs(H))**2)/2)
        if n==8:
            for x,t in env['peaks'].items():ck(f'C8-code-retard-{x}',t,1+x/2,1e-12)
        if n==9:
            for i2,sig in env['profiles'].items():
                ck(f'C9-code-min-{i2}',sig.min(),(1-math.sqrt(i2))**2)
                ck(f'C9-code-max-{i2}',sig.max(),(1+math.sqrt(i2))**2)
        if n==10:
            for t,sig in env['profiles'].items():
                ck(f'C10-code-bord-gauche-{t}',sig[0],0)
                ck(f'C10-code-bord-droit-{t}',sig[-1],0)
            ck('C10-code-periodicite',np.max(abs(env['y'](.04)-env['y'](0))),0)
        plt.close('all')
    # Deux formes indépendantes de la réponse RLC ; lois des mailles et bilan de puissance.
    R,L,C,E=20.,.1,1e-5,2.
    for w in [100.,500.,1000.,2000.,10000.]:
        z=R+1j*(w*L-1/(w*C));i=E/z;uc=i/(1j*w*C)
        h=1/(1-L*C*w*w+1j*R*C*w)
        ck(f'C6-maille-{w}',abs(R*i+1j*w*L*i+uc-E),0)
        ck(f'C6-uc-transfert-{w}',abs(uc/E-h),0)
        ck(f'C6-puissance-{w}',(E*np.conj(i)).real/2,R*abs(i)**2/2)
    for q in [.4,.8,2.,5.,20.]:
        lo=math.sqrt(1+1/(4*q*q))-1/(2*q);hi=math.sqrt(1+1/(4*q*q))+1/(2*q)
        ck(f'C6-coupures-largeur-Q{q}',hi-lo,1/q)
        ck(f'C6-coupures-produit-Q{q}',lo*hi,1)
        if q>1/math.sqrt(2):
            xr=math.sqrt(1-1/(2*q*q));g=abs(1/(1-xr*xr+1j*xr/q))
            ck(f'C6-pic-Q{q}',g,q/math.sqrt(1-1/(4*q*q)))
    ck('C6-DM-C',1/(.08*(1000*math.pi)**2),1.2665147955292223e-6)
    ck('C6-DS-largeur',30/.06,500)
    # L'analyse nodale de la cascade est résolue sans partir du transfert annoncé.
    for w in [.01,.1,1.,10.,100.]:
        p=1j*w
        u,s=np.linalg.solve([[2+p,-1],[-1,1+p]],[1,0])
        ck(f'C7-cascade-nodale-{w}',abs(s-1/(1+3*p+p*p)),0)
        ck(f'C7-Butterworth-{w}',abs(1/(1-w*w+1j*math.sqrt(2)*w)),1/math.sqrt(1+w**4))
    ck('C7-D1-incompatibilite',float(100/math.sqrt(1/.95**2-1)>10000/math.sqrt(2499)),1)
    ck('C7-DM-ondulation',3/abs(1+1j*2*math.pi*1000*.016)+1/abs(1+1j*2*math.pi*3000*.016),.03315578533578753)
    # Somme complexe contre identité trigonométrique et formule d'intensité.
    for phase in np.linspace(0,2*math.pi,9):
        z1=3;z2=4*np.exp(1j*phase)
        ck(f'C9-Fresnel-{phase:.3f}',abs(z1+z2)**2,25+24*math.cos(phase))
        ck(f'C9-amplitudes-egales-{phase:.3f}',abs(2+2*np.exp(1j*phase)),4*abs(math.cos(phase/2)))
    # Approximation de Young testée par la géométrie exacte.
    for x in [.001,.003,.006]:
        D=2.;a=.0005;r1=math.sqrt(D*D+(x-a/2)**2);r2=math.sqrt(D*D+(x+a/2)**2)
        ck(f'C9-Young-approx-{x}',(r2-r1)/(a*x/D),1,5e-6)
    ck('C9-D2-contraste',2*math.sqrt(1/9)/(1+1/9),.6)
    ck('C9-DM-lame',-1.8*(1.5-1)*.6e-6/.00045,-.0012)
    # Conditions aux limites et somme de deux ondes pour les modes.
    for n in range(1,7):
        L=.8;c=40.;k=n*math.pi/L;w=c*k
        ck(f'C10-bord-L-n{n}',math.sin(k*L),0)
        ck(f'C10-frequence-n{n}',w/(2*math.pi),n*25)
        for x in [.1,.3,.6]:
            t=.003
            ck(f'C10-superposition-n{n}-x{x}',math.cos(w*t-k*x)-math.cos(w*t+k*x),2*math.sin(w*t)*math.sin(k*x))
    return out

def labels_in(s):
    labs=[]
    for m in re.finditer(r'\\Page\{',s):
        pos=m.end()-1
        for i in range(3):arg,pos=balanced(s,pos)
        labs.append(arg)
    return labs

def verify(render=False):
    B=OUT/'build';Q=B/'qa';Q.mkdir(exist_ok=True)
    parts=[(OUT/'liminaires.tex').read_text(encoding='utf-8')]+[(OUT/f'chapitres/ch{n:02}.tex').read_text(encoding='utf-8') for n in range(1,11)]
    tex='\n'.join(parts);aux=(B/'main.aux').read_text(encoding='utf-8');log=(B/'main.log').read_text(encoding='utf-8',errors='replace')
    labs=labels_in(tex);pos={}
    for lab in labs:
        m=re.search(r'\\newlabel\{'+re.escape(lab)+r'\}\{\{[^}]*\}\{(\d+)\}',aux);assert m,lab
        pos[lab]=int(m[1])
    doc=fitz.open(B/'main.pdf');expected=len(labs)+1
    pagination=list(pos.values())==list(range(2,expected+1)) and len(doc)==expected
    assert pagination,(len(doc),expected,[p for p in pos.items()][:15])
    for n,s in enumerate(parts[1:],1):
        exs=re.findall(r'\\ex\{(E\d+)\}',s);sols=re.findall(r'\\sol\{(E\d+)\}',s)
        assert exs==sols==[f'E{i:02}' for i in range(1,25)],(n,exs,sols)
        assert f'ch{n:02}-chapitre-{n:02}' in pos
    bad=[l for l in log.splitlines() if any(x in l for x in ['Overfull','Missing character','undefined references','multiply defined','Fatal error'])]
    outside=[];collisions=[];low=[]
    for i,p in enumerate(doc):
        spans=[s for b in p.get_text('dict')['blocks'] if b['type']==0 for l in b['lines'] for s in l['spans']]
        for s in spans:
            r=fitz.Rect(s['bbox'])
            if r.x0<-.5 or r.y0<-.5 or r.x1>p.rect.width+.5 or r.y1>p.rect.height+.5:outside.append(dict(page=i+1,texte=s['text'],bbox=list(r)))
            if i and s['size']>=8 and r.y1>p.rect.height-60 and r.y0<p.rect.height-58:low.append(dict(page=i+1,texte=s['text']))
        long=[s for s in spans if len(re.findall('[A-Za-zÀ-ÿ]',s['text']))>=4 and s['size']>=6.5]
        for j,s in enumerate(long):
            r=fitz.Rect(s['bbox'])
            for t in long[j+1:]:
                q=fitz.Rect(t['bbox']);hit=r&q
                if not hit.is_empty and hit.width>4 and hit.height>min(r.height,q.height)*.45 and hit.get_area()>min(r.get_area(),q.get_area())*.16:collisions.append(dict(page=i+1,a=s['text'],b=t['text']))
    links=[l for p in doc for l in p.get_links()];broken=[l for l in links if l['kind']==fitz.LINK_GOTO and not 0<=l.get('page',-1)<len(doc)]
    toc=doc.get_toc();roots=[t for t in toc if t[0]==1 and t[1].startswith('Chapitre ')]
    assert len(roots)==10,roots
    checks=science()
    old=[]
    for n in range(1,6):
        f=(OUT.parent/'livre-physique-mpsi/build/verification.json') if n==1 else (OUT.parent/f'livre-physique-mpsi-suite/chapitre-{n:02}/build/verification.json')
        if f.exists():
            prior=json.loads(f.read_text(encoding='utf-8'));old+=prior.get('controles',prior.get('controles_numeriques',[]))
    report=dict(pages=len(doc),pages_prevues=expected,pagination_conforme=pagination,positions=pos,chapitres=10,exercices=240,defis=30,dm=10,ds=10,tp=10,numerique=10,erreurs_compilation=bad,textes_hors_page=outside,collisions_candidates=collisions,textes_bas_page=low,liens=len(links),liens_invalides=broken,signets=len(toc),signets_chapitres=roots,controles_nouveaux=checks,controles_anterieurs=old,sha256=hashlib.sha256((B/'main.pdf').read_bytes()).hexdigest())
    (B/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:report[k] for k in ['pages','pages_prevues','pagination_conforme','erreurs_compilation','textes_hors_page','collisions_candidates','textes_bas_page','liens_invalides']},ensure_ascii=False),flush=True)
    print('Contrôles scientifiques nouveaux :',len(checks),'; contrôles antérieurs conservés :',len(old),flush=True)
    assert not bad and not outside and not broken
    if render:
        p=subprocess.run(['pdftoppm','-r','85','-png',str(B/'main.pdf'),str(Q/'page')],capture_output=True)
        assert p.returncode==0,p.stderr
        paths=sorted(Q.glob('page-*.png'));assert len(paths)==len(doc)
        # Six pages par planche ; chaque page est également disponible à pleine taille.
        for start in range(0,len(paths),6):
            sheet=Image.new('RGB',(2040,1920),'#e8ebef')
            for j,p in enumerate(paths[start:start+6]):
                im=Image.open(p).convert('RGB');im.thumbnail((650,920));tile=Image.new('RGB',(680,960),'#e8ebef');tile.paste(im,((680-im.width)//2,20));ImageDraw.Draw(tile).text((14,936),f'Page {start+j+1}',fill='black');sheet.paste(tile,((j%3)*680,(j//3)*960))
            sheet.save(Q/f'planche-{start+1:03}-{min(start+6,len(paths)):03}.jpg',quality=90)
        print('Rendu terminé :',len(paths),'pages.',flush=True)
    return report

if __name__=='__main__':verify('--rendu' in sys.argv)
