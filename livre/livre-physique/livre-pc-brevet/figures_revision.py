"""Schémas des exercices et corrections : tracés vectoriels, données explicites."""
from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle,Polygon,FancyArrowPatch
from matplotlib.ticker import FuncFormatter,ScalarFormatter
HERE=Path(__file__).resolve().parent;OUT=HERE/'figures'
N='#1B3C8E';G='#3B8544';R='#B94343';M='#667085';L='#E5EAF3';Y='#C69B42'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':N,'text.color':N,'axes.edgecolor':M,'xtick.color':M,'ytick.color':M})
REGISTRY={}
def cv(height=1.8):
    f,a=plt.subplots(figsize=(6.2,height));f.subplots_adjust(left=.01,right=.99,bottom=.03,top=.97)
    a.set(xlim=(0,16),ylim=(0,4.5));a.axis('off');return f,a
def tx(a,x,y,s,c=N,size=10,ha='center',va='center',**kw):
    a.text(x,y,s,fontsize=size,color=c,ha=ha,va=va,zorder=8,**kw)
def ln(a,pts,c=N,lw=1.3,**kw):a.plot(*zip(*pts),color=c,lw=lw,zorder=2,**kw)
def ar(a,p,q,c=G,label='',off=(0,.35)):
    a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=11,lw=1.3,color=c,zorder=5))
    if label:tx(a,(p[0]+q[0])/2+off[0],(p[1]+q[1])/2+off[1],label,c,9.5,bbox=dict(facecolor='white',edgecolor='none',pad=.3))
def bx(a,x,y,w,h,s='',fill=L,c=N):
    a.add_patch(Rectangle((x,y),w,h,fc=fill,ec=c,lw=1.1,zorder=3));tx(a,x+w/2,y+h/2,s,size=9.7)
def save(name,f,data=None):
    assert name not in REGISTRY,name
    for ax in f.axes:
        if ax.axison:
            fmt=FuncFormatter(lambda x,pos:f'{x:g}'.replace('.',','))
            for axis in [ax.xaxis,ax.yaxis]:
                if isinstance(axis.get_major_formatter(),ScalarFormatter):axis.set_major_formatter(fmt)
    f.canvas.draw();renderer=f.canvas.get_renderer();bounds=f.bbox
    for ax in f.axes:
        for artist in [ax.xaxis.label,ax.yaxis.label,ax.title,*ax.texts]:
            if not artist.get_visible() or not artist.get_text():continue
            r=artist.get_window_extent(renderer)
            assert r.x0>=bounds.x0-.5 and r.y0>=bounds.y0-.5 and r.x1<=bounds.x1+.5 and r.y1<=bounds.y1+.5,(name,'texte rogné',artist.get_text(),list(r.bounds))
    dest=OUT/(name+'.pdf');f.savefig(dest,metadata={'Title':'OptiTAB - '+name,'Author':'OptiTAB'})
    # Examiner ce qui est réellement écrit dans le PDF ; les ticks Matplotlib
    # préparés hors des limites ne sont pas tous dessinés.
    import fitz
    pdf=fitz.open(dest);page=pdf[0];outside=[]
    for b in page.get_text('dict')['blocks']:
        for line in b.get('lines',[]):
            for span in line['spans']:
                rect=fitz.Rect(span['bbox'])
                if rect.x0<-.7 or rect.y0<-.7 or rect.x1>page.rect.width+.7 or rect.y1>page.rect.height+.7:outside.append(dict(texte=span['text'],bbox=[round(v,1) for v in rect]))
    pdf.close()
    REGISTRY[name]=dict(data or {},textes_hors_cadre=outside);plt.close(f)
def plot(name,x,y,xlabel,ylabel,other=None,annotate=None,ylim=None,xlim=None):
    f,a=plt.subplots(figsize=(6.2,2.0));f.subplots_adjust(left=.13,right=.95,bottom=.26,top=.94)
    a.plot(x,y,'o-' if len(x)<=30 else '-',color=N,lw=1.5,ms=3.5)
    if other:
        for xx,yy,label,col in other:a.plot(xx,yy,'o-',color=col,label=label,lw=1.3,ms=3)
        a.legend(fontsize=9,framealpha=.94,loc='best')
    a.set(xlabel=xlabel,ylabel=ylabel)
    if ylim:a.set_ylim(ylim)
    if xlim:a.set_xlim(xlim)
    a.grid(color=L);a.set_axisbelow(True)
    if annotate:annotate(a)
    save(name,f,dict(x=list(map(float,x)),y=list(map(float,y))))
def note(a,s,xy,xytext):
    a.annotate(s,xy=xy,xytext=xytext,color=G,fontsize=9.4,arrowprops=dict(arrowstyle='->',color=G,lw=1),bbox=dict(fc='white',ec='none',pad=1))

def mol(a,x,y,s,k=1):
    atoms={'H2O':[(-.6,0,'H'),(0,.45,'O'),(.6,0,'H')], 'CO':[(-.45,0,'C'),(.45,0,'O')], 'CO2':[(-.8,0,'O'),(0,0,'C'),(.8,0,'O')], 'O2':[(-.4,0,'O'),(.4,0,'O')], 'N2':[(-.4,0,'N'),(.4,0,'N')], 'H2':[(-.4,0,'H'),(.4,0,'H')], 'CH4':[(0,0,'C'),(-.7,0,'H'),(.7,0,'H'),(0,.7,'H'),(0,-.7,'H')]}
    d=atoms[s];pairs=[(0,1),(1,2)] if s in ['H2O','CO2'] else [(0,j) for j in range(1,len(d))]
    for i,j in pairs:ln(a,[(x+d[i][0]*k,y+d[i][1]*k),(x+d[j][0]*k,y+d[j][1]*k)],M)
    colors={'H':'white','O':'#CE5F5F','C':'#596071','N':'#5979B3'}
    for dx,dy,atom in d:
        a.add_patch(Circle((x+dx*k,y+dy*k),.29*k,fc=colors[atom],ec=M,lw=.9,zorder=4));tx(a,x+dx*k,y+dy*k,atom,c=N if atom=='H' else 'white',size=9)

def exact_canvas(height_cm=3.5,width_cm=15.0):
    f=plt.figure(figsize=(width_cm/2.54,height_cm/2.54));a=f.add_axes([0,0,1,1]);a.set(xlim=(0,width_cm),ylim=(0,height_cm));a.axis('off');return f,a
def force(a,x,y,length,horizontal=True,sign=1,label='',c=G):
    q=(x+sign*length,y) if horizontal else (x,y+sign*length)
    a.plot([x,q[0]],[y,q[1]],color=c,lw=1.6,zorder=5)
    if horizontal:verts=[q,(q[0]-sign*.22,q[1]+.09),(q[0]-sign*.22,q[1]-.09)]
    else:verts=[q,(q[0]+.09,q[1]-sign*.22),(q[0]-.09,q[1]-sign*.22)]
    a.add_patch(Polygon(verts,fc=c,ec=c,zorder=5));a.add_patch(Circle((x,y),.03,fc=N,zorder=6))
    if label:tx(a,(x+q[0])/2+(0 if horizontal else 1.5),(y+q[1])/2+(.4 if horizontal else 0),label,c,10)
