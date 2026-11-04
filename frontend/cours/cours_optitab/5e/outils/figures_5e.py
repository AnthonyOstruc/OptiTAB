"""Schémas mathématiques reproductibles ; énoncé en bleu, correction en vert."""
from pathlib import Path
from fractions import Fraction
import json
import math
import re
import subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, Ellipse, Arc
from modele_5e import ROOT, FRONT

BLUE='#2563a6'
GREEN='#13804d'
INK='#20354c'
ORANGE='#dc8b13'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,'axes.labelcolor':INK})


def readable(value):
    return str(value).replace('{,}',',').replace('\\frac','').replace('{','').replace('}','')


def draw(spec,path,correction=False):
    kind=spec['type']
    fig,ax=plt.subplots(figsize=(7.5,3.7),layout='constrained')
    fig.patch.set_facecolor('white')
    color=GREEN if correction else BLUE
    ax.set_aspect('equal',adjustable='box')
    ax.axis('off')
    def point(x,y,name,dx=.12,dy=.16):
        ax.plot(x,y,'o',color=color,ms=5)
        ax.text(x+dx,y+dy,name,color=INK,fontsize=11)
    def segment(a,b,style='-',col=None):
        ax.plot([a[0],b[0]],[a[1],b[1]],style,color=col or color,lw=2)
    def note(txt):
        ax.text(.5,.01,txt,transform=ax.transAxes,ha='center',va='bottom',color=GREEN if correction else INK,fontsize=10,
            bbox=dict(facecolor='white',edgecolor='none',alpha=.95,pad=4))
    if kind=='table':
        ax.set_aspect('auto')
        rows=[[readable(c) for c in row] for row in spec['rows']]
        if correction and rows and '?' in rows[0] and len(spec['headers'])==4:
            hs=spec['headers']
            rate=Fraction(str(spec['rows'][0][1]))/int(hs[1])
            rows[0][2]=str(rate)
            rows[0][3]=str(rate*int(hs[3]))
        tb=ax.table(cellText=rows,colLabels=spec['headers'],loc='center',cellLoc='center',bbox=[.02,.25,.96,.55])
        tb.auto_set_font_size(False);tb.set_fontsize(11)
        for (r,c),cell in tb.get_celld().items():
            cell.set_edgecolor('#b6c8da');cell.set_linewidth(1.3)
            if r==0: cell.set_facecolor(color);cell.get_text().set_color('white')
            else: cell.set_facecolor('#f3f8fc')
        if correction: note('Le tableau conserve les grandeurs et les unités de l’énoncé.')
    elif kind=='numberline':
        points=spec['points'];lo=min(points.values())-2;hi=max(points.values())+2
        ax.annotate('',(hi,0),(lo,0),arrowprops=dict(arrowstyle='->',color=INK))
        for x in range(lo,hi):
            ax.plot([x,x],[-.07,.07],color='#8296aa');ax.text(x,-.3,str(x),ha='center',fontsize=9)
        for j,(p,x) in enumerate(points.items()): point(x,0,p,0,.18+.2*(j%2))
        if correction:
            d=-points['A'];point(d,0,'D = opposé de A',-.3,.75)
            ax.annotate('',(d,.6),(points['A'],.6),arrowprops=dict(arrowstyle='<->',color=GREEN))
        ax.set_xlim(lo-1,hi+1);ax.set_ylim(-.8,1.5)
    elif kind=='steps':
        ax.set_aspect('auto');ax.axis('on')
        vals=spec['values']
        ax.plot(range(len(vals)),vals,'o-',color=color,lw=2)
        ax.axhline(0,color='#8296aa',lw=1)
        ax.set_xticks(range(len(vals)),spec['labels']);ax.set_ylabel('Température (°C)')
        for j,v in enumerate(vals):ax.annotate(f'{v} °C',(j,v),xytext=(0,12),textcoords='offset points',ha='center')
        ax.margins(x=.15,y=.35);ax.grid(axis='y',alpha=.2)
        if correction:ax.set_title(f'Variation totale : {vals[-1]-vals[0]:+d} °C',color=GREEN)
    elif kind=='boxes':
        cap=spec['capacity'];rem=spec['remainder']
        for k in range(cap):
            ax.add_patch(Rectangle((k,0),.85,1,ec=color,fc='#dcebf6' if k<rem else 'white',lw=1.5))
            if k<rem:ax.text(k+.425,.5,'●',ha='center',va='center',color=color)
        ax.set_xlim(-.5,cap+.4);ax.set_ylim(-.8,2)
        ax.text(cap/2,1.5,'Dernière boîte : chaque case est une place',ha='center')
        note(f'{cap-rem} place(s) vide(s)' if correction else f'Les {spec["quotient"]} autres boîtes sont pleines.')
    elif kind=='fraction':
        d=spec['denominator'];a=spec['numerator']
        for k in range(d):ax.add_patch(Rectangle((k,0),1,1,ec='white',lw=2,fc=color if k<a else '#e4ebf1'))
        ax.set_xlim(-.3,d+.3);ax.set_ylim(-.7,2)
        ax.text(d/2,1.45,f'Une unité partagée en {d} parts égales',ha='center')
        note((f'Part colorée : {a}/{d} ; complément : {d-a}/{d}.' if correction else 'La bande entière représente le volume initial.'))
    elif kind=='grid':
        side=spec['side']
        for j in range(side+1):
            segment((0,j),(side,j),col='#9bbbd3');segment((j,0),(j,side),col='#9bbbd3')
        ax.set_xlim(-1,side+1);ax.set_ylim(-1,side+1)
        ax.text(side/2,-.65,f'{side} carreaux par côté',ha='center')
        if correction:ax.text(side/2,side+.4,f'{side} × {side} = {side*side} carreaux',ha='center',color=GREEN)
    elif kind=='rectangle':
        w,e,h=spec['width'],spec['extension'],spec['height']
        ax.add_patch(Rectangle((0,0),w,h,fc='#dcebf6',ec=color,lw=2));ax.add_patch(Rectangle((w,0),e,h,fc='#e0f3e9',ec=color,lw=2))
        ax.text(w/2,h/2,f'{h}x' if correction else 'Partie variable',ha='center',fontsize=10)
        ax.text(w+e/2,h/2,str(h*e) if correction else 'Partie fixe',ha='center',fontsize=10)
        ax.text(w/2,-.6,'x cm',ha='center');ax.text(w+e/2,-.6,f'{e} cm',ha='center');ax.text(-.5,h/2,f'{h} cm',ha='right')
        ax.set_xlim(-2,w+e+1);ax.set_ylim(-1.5,h+1)
    elif kind=='flow':
        ax.set_aspect('auto')
        for j,lab in enumerate(spec['labels']):
            ax.text(.17+.33*j,.55,lab,ha='center',va='center',transform=ax.transAxes,
                bbox=dict(boxstyle='round,pad=.8',ec=color,fc='#eff7fc'),fontsize=11)
            if j<2:ax.annotate('',xy=(.37+.33*j,.55),xytext=(.29+.33*j,.55),xycoords='axes fraction',arrowprops=dict(arrowstyle='->',color=color))
        if correction: note('Retirer la partie fixe, puis partager entre les pochettes.')
    elif kind=='percent':
        r=spec['rate']
        for y in range(10):
            for x in range(10):ax.add_patch(Rectangle((x,y),.92,.92,fc=color if 10*y+x<r else '#e4ebf1',ec='white'))
        ax.set_xlim(-1,11);ax.set_ylim(-1,11)
        if correction:note(f'{r} parts sur 100 sont remises ; {100-r} sont payées.')
    elif kind=='graph':
        ax.axis('on');ax.set_aspect('auto');a,b,x=spec['coefficient'],spec['fixed'],spec['max_x']
        xs=list(range(x+1));ax.plot(xs,[a*t+b for t in xs],'o-',color=color)
        ax.set_xlabel('Nombre d’activités');ax.set_ylabel('Prix (€)');ax.set_xticks(xs)
        ax.set_xlim(-.3,x+.5);ax.set_ylim(0,a*x+b+3);ax.grid(alpha=.2)
        if correction:ax.set_title(f'Prix pour 0 activité : {b} € → pas de proportionnalité',color=GREEN,fontsize=11)
    elif kind=='coordinates':
        ax.axis('on');x,y=spec['x'],spec['y']
        ax.axhline(0,color=INK,lw=1);ax.axvline(0,color=INK,lw=1)
        coords=[(-x,y),(x,y),(x,-y),(-x,-y)]
        ax.add_patch(Polygon(coords,fc='#eef6fc',ec=color,lw=2))
        for p,(a,b) in zip('ABCD',coords):point(a,b,p,.15,.2)
        if correction:
            segment(coords[0],coords[2],'--',GREEN);segment(coords[1],coords[3],'--',GREEN);point(0,0,'O')
        ax.set_xlim(-x-2,x+2);ax.set_ylim(-y-2,y+2);ax.set_xticks(range(-x,x+1));ax.set_yticks(range(-y,y+1));ax.grid(alpha=.15)
        ax.set_xlabel('Abscisse (m)');ax.set_ylabel('Ordonnée (m)')
    elif kind in ('intersect','parallel'):
        a=spec['angle'];s=math.tan(math.radians(a))
        if kind=='intersect':
            segment((-3,0),(3,0));segment((-2,-2*s),(2,2*s))
            point(0,0,'O',-.4,-.4);ax.text(-3,0,'A',ha='right');ax.text(3,0,'B');ax.text(-2,-2*s,'C',ha='right');ax.text(2,2*s,'D')
            ax.add_patch(Arc((0,0),1.6,1.6,theta1=180,theta2=180+a,ec=ORANGE,lw=2))
            ax.text(-1,-.45,f'{a}°',color=ORANGE)
            if correction:
                ax.text(.8,.3,f'{a}°',color=GREEN);ax.text(.3,-1,f'{180-a}°',color=GREEN)
            ax.set_xlim(-4,4);ax.set_ylim(min(-2*s,-2)-.5,max(2*s,2)+.5)
        else:
            segment((-3,1),(3,1));segment((-3,-1),(3,-1));segment((-2,-2*s),(2,2*s))
            xx=1/s;point(xx,1,'A',.15,.1);point(-xx,-1,'B',.15,.1)
            ax.text(-3.3,1,'d');ax.text(-3.3,-1,'e');ax.text(xx+.6,1.2,f'{a}°',color=ORANGE)
            ax.text(-3,2.6,'d ∥ e',color=INK)
            if correction:ax.text(-xx+.6,-.8,f'{a}°',color=GREEN)
            ax.set_xlim(-4,4);ax.set_ylim(-3,3)
    elif kind=='triangle_angles':
        a,b=map(math.radians,[spec['a'],spec['b']]);base=spec['base']
        xx=base*math.tan(b)/(math.tan(a)+math.tan(b));yy=xx*math.tan(a)
        ax.add_patch(Polygon([(0,0),(base,0),(xx,yy)],fill=False,ec=color,lw=2))
        point(0,0,'A',-.3,-.5);point(base,0,'B',.15,-.5);point(xx,yy,'C',0,.3)
        ax.text(.7,.3,f'{spec["a"]}°');ax.text(base-1,.3,f'{spec["b"]}°');ax.text(base/2,-.7,f'AB = {base} cm',ha='center')
        if correction:ax.text(xx,yy-.6,f'{180-spec["a"]-spec["b"]}°',ha='center',color=GREEN)
        ax.set_xlim(-1,base+1);ax.set_ylim(-1.5,yy+1.5)
        note('Schéma de travail : la construction en vraie grandeur se fait aux instruments.')
    elif kind=='triangle_area':
        b,h=spec['base'],spec['height'];x=b*.28
        ax.add_patch(Polygon([(0,0),(b,0),(x,h)],fill=False,ec=color,lw=2))
        segment((x,h),(x,0),'--',ORANGE);ax.add_patch(Rectangle((x,0),.35,.35,fill=False,ec=ORANGE))
        for p,(a,v) in {'A':(x,h),'B':(0,0),'C':(b,0),'H':(x,0),'M':(b/2,0)}.items():point(a,v,p,0,.16 if v else -.5)
        segment((x,h),(b/2,0),'--',GREEN)
        ax.text(x-.3,h/2,f'{h} m',ha='right');ax.text(b/2,-1,f'{b} m',ha='center')
        if correction:ax.text(b*.7,h*.6,f'Aire totale : {b*h/2:g} m²',color=GREEN,ha='center')
        ax.set_xlim(-1,b+1);ax.set_ylim(-1.8,h+1.5)
    elif kind=='symmetry':
        ax.axis('on');x,y=spec['x'],spec['y'];ax.axhline(0,color='#a7b6c4');ax.axvline(0,color=ORANGE,lw=1.8)
        coords=[(x,y),(x+2,y),(x,y+2)]
        ax.add_patch(Polygon(coords,fill=False,ec=BLUE,lw=2))
        for p,(a,b) in zip('ABC',coords):point(a,b,p)
        if correction:
            image=[(-a,b if spec['axial'] else -b) for a,b in coords]
            ax.add_patch(Polygon(image,fc='#e1f1e8',ec=GREEN,lw=2))
            for p,(a,b) in zip(['A′','B′','C′'],image):point(a,b,p)
        ax.set_xlim(-x-4,x+4);ax.set_ylim(-y-4,y+4);ax.grid(alpha=.15);ax.set_xlabel('Abscisse');ax.set_ylabel('Ordonnée')
        note('Axe vertical de symétrie' if spec['axial'] else 'Centre de symétrie : O(0 ; 0)')
    elif kind=='parallelogram':
        b,h,s=spec['base'],spec['height'],spec['side'];shift=math.sqrt(s*s-h*h)
        pts=[(0,0),(b,0),(b+shift,h),(shift,h)]
        ax.add_patch(Polygon(pts,fc='#edf6fc',ec=color,lw=2))
        for p,(x,y) in zip('ABCD',pts):point(x,y,p,0,.2 if y else -.5)
        segment((shift,h),(shift,0),'--',ORANGE);ax.add_patch(Rectangle((shift,0),.3,.3,fill=False,ec=ORANGE))
        ax.text(shift-.3,h/2,f'h = {h} m',ha='right',fontsize=10);ax.text(b/2,-.9,f'{b} m',ha='center');ax.text(b+shift/2+.3,h/2,f'{s} m',fontsize=10)
        if correction:segment(pts[0],pts[2],'--',GREEN);segment(pts[1],pts[3],'--',GREEN);point((b+shift)/2,h/2,'O')
        ax.set_xlim(-2,b+shift+3);ax.set_ylim(-1.7,h+1.5)
    elif kind=='prism':
        b,h,length=spec['base'],spec['height'],spec['length']
        shift=(length*.5,length*.3)
        pts=[(0,0),(b,0),(0,h)]
        back=[(x+shift[0],y+shift[1]) for x,y in pts]
        ax.add_patch(Polygon(pts,fc='#e7f2fa',ec=color,lw=2))
        for j in range(3):
            segment(pts[j],back[j],'--' if j==0 else '-')
            segment(back[j],back[(j+1)%3],'--' if j==0 else '-')
        ax.add_patch(Rectangle((0,0),.3,.3,fill=False,ec=ORANGE))
        ax.text(b/2,-.6,f'{b} cm',ha='center');ax.text(-.3,h/2,f'{h} cm',ha='right')
        ax.text(b+shift[0]/2+.2,shift[1]/2,f'{length} cm')
        ax.set_xlim(-2,b+shift[0]+2);ax.set_ylim(-1.4,h+shift[1]+1)
        if correction:note(f'Aire de base : {b*h/2:g} cm² ; volume : {b*h*length/2:g} cm³')
    elif kind=='cuboid':
        l,w,h=spec['length'],spec['width'],spec['height'];shift=w*.45
        for pts in [[(0,0),(l,0),(l,h),(0,h),(0,0)],[(0,h),(shift,h+shift),(l+shift,h+shift),(l,h)],[(l,0),(l+shift,shift),(l+shift,h+shift)]]:
            ax.plot(*zip(*pts),color=color,lw=2)
        for a,b in [((0,0),(shift,shift)),((shift,shift),(l+shift,shift)),((shift,shift),(shift,h+shift))]:segment(a,b,'--','#8296aa')
        ax.text(l/2,-.7,f'{l} dm',ha='center');ax.text(l+shift+.3,h/2,f'{h} dm');ax.text(l+shift/2+.3,shift/2,f'{w} dm',fontsize=10)
        if correction:note(f'Volume : {l*w*h} dm³ = {l*w*h} L')
        ax.set_xlim(-1,l+shift+3);ax.set_ylim(-1.5,h+shift+1)
    elif kind=='cylinder':
        r,h=spec['radius'],spec['height'];sy=.3*r
        ax.add_patch(Ellipse((0,h),2*r,2*sy,fill=False,ec=color,lw=2));ax.add_patch(Arc((0,0),2*r,2*sy,theta1=180,theta2=360,ec=color,lw=2));ax.add_patch(Arc((0,0),2*r,2*sy,theta1=0,theta2=180,ec='#8296aa',ls='--'))
        segment((-r,0),(-r,h));segment((r,0),(r,h));segment((0,h),(r,h),'--',ORANGE)
        ax.text(r/2,h+.3,f'r = {r} cm',ha='center');ax.text(r+.5,h/2,f'h = {h} cm')
        ax.set_xlim(-r-1,r+4);ax.set_ylim(-2,h+2)
        if correction:note(f'Aire de base : {r*r}π cm² ; volume : {r*r*h}π cm³')
    elif kind=='bars':
        ax.axis('on');ax.set_aspect('auto');vs=spec['values'];ax.bar(spec['labels'],vs,color=color,width=.55)
        ax.set_ylabel(spec['ylabel']);ax.set_ylim(0,max(vs)*1.3);ax.set_yticks(range(0,max(vs)+2,max(1,max(vs)//6)));ax.grid(axis='y',alpha=.2)
        for j,v in enumerate(vs):ax.text(j,v+.3,str(v),ha='center')
        if correction:ax.set_title(f'Effectif / somme des valeurs : {sum(vs)} (à interpréter selon le contexte)',color=GREEN,fontsize=10)
    elif kind=='urn':
        counts=[spec['red'],spec['blue'],spec['green']];cols=['#b83943','#2678bc','#258354'];total=sum(counts)
        k=0
        for count,col in zip(counts,cols):
            for _ in range(count):
                x,y=k%8,k//8;ax.add_patch(Circle((x,y),.32,fc=col,ec='white',lw=1));k+=1
        ax.set_xlim(-1,8);ax.set_ylim(-1,max(3,total//8+2))
        note(f'{total} jetons équiprobables ; P(rouge) = {counts[0]}/{total}' if correction else 'Chaque jeton a la même chance d’être tiré.')
    elif kind=='program':
        ax.set_aspect('auto');lines=spec['lines']
        for j,line in enumerate(lines):
            x=.14 if line.startswith('    ') else .06
            col='#e2a23a' if j==0 else '#e5a44c' if 'Répéter' in line else '#3c8bca'
            ax.text(x,.92-j*.16,line.strip(),transform=ax.transAxes,ha='left',va='center',fontsize=12,color='white',
                bbox=dict(boxstyle='round,pad=.55',facecolor=col,edgecolor='white'))
        note('Blocs pédagogiques de type Scratch ; l’indentation indique le contenu de la boucle.')
    else:
        raise ValueError(kind)
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(path,dpi=150,facecolor='white')
    plt.close(fig)
    # Les droites et bandes doivent rester grandes sur téléphone : retirer les
    # marges blanches issues du canevas, sans toucher aux tracés ni aux étiquettes.
    from PIL import Image,ImageChops
    with Image.open(path) as src:
        im=src.convert('RGB')
    mask=ImageChops.difference(im,Image.new('RGB',im.size,'white')).convert('L').point(lambda x:255 if x>30 else 0)
    bounds=mask.getbbox()
    if bounds:
        x0,y0,x1,y1=bounds
        im.crop((max(0,x0-18),max(0,y0-18),min(im.width,x1+18),min(im.height,y1+18))).save(path)


def render_course_figures(chapitres,book):
    """Rend les figures TikZ du livre : mêmes codages et légendes, pas de redessin approximatif."""
    from PIL import Image,ImageChops
    import fitz
    figures=list(dict.fromkeys(re.findall(r'@FIG:([^@]+)@',''.join(''.join(c.cours) for c in chapitres))))
    target=ROOT/'verifications/rendu-figures'
    target.mkdir(parents=True,exist_ok=True)
    tex=target/'figures-cours.tex'
    tex.write_text('\\documentclass[11pt,openany]{book}\n\\usepackage{optitab-livre}\n\\usepackage{figures-geometrie}\n\\begin{document}\n\\pagestyle{empty}\n'+
        '\n\\clearpage\n'.join('\\noindent\\input{figures/'+name+'.tex}' for name in figures)+'\n\\end{document}\n',encoding='utf-8')
    proc=subprocess.run(['lualatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(target),str(tex)],cwd=book,capture_output=True,text=True,encoding='utf-8',errors='replace')
    (target/'compilation.txt').write_text(proc.stdout+proc.stderr,encoding='utf-8')
    if proc.returncode: raise RuntimeError('Échec des figures du cours : '+proc.stdout[-2500:])
    doc=fitz.open(target/'figures-cours.pdf')
    assert len(doc)==len(figures),(len(doc),len(figures))
    for page,name in zip(doc,figures):
        pix=page.get_pixmap(matrix=fitz.Matrix(2.5,2.5),alpha=False)
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        diff=ImageChops.difference(im,Image.new('RGB',im.size,'white')).convert('L').point(lambda x:255 if x>35 else 0)
        bounds=diff.getbbox()
        assert bounds,name
        x0,y0,x1,y1=bounds
        im.crop((max(0,x0-20),max(0,y0-20),min(im.width,x1+20),min(im.height,y1+20))).save(ROOT/'images'/f'{name}_5e.png')
    draw(dict(type='flow',labels=['Parenthèses','× et ÷','+ et −']),ROOT/'images/cours-operations_5e.png')
    draw(dict(type='boxes',capacity=7,remainder=6,quotient=11,total=83),ROOT/'images/cours-divisibilite_5e.png')
    print(f'{len(figures)+2} figures de cours rendues.')
