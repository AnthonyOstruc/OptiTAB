"""Figures vectorielles calculées à partir des modèles du texte."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, Polygon
import numpy as np
from math import comb
ROOT=Path(__file__).resolve().parents[1]
NAVY='#1B3C8E';GREEN='#3B8544';MUTED='#667085';ORANGE='#D68A35'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.labelsize':10,
 'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#98A2B3',
 'axes.labelcolor':'#25334D','xtick.color':MUTED,'ytick.color':MUTED,
 'grid.alpha':.16,'pdf.fonttype':42,'savefig.facecolor':'white'})

def axes(n=1,height=2.55):
    fig,ax=plt.subplots(1,n,figsize=(6.2,height),layout='constrained')
    for a in np.atleast_1d(ax):a.grid();a.set_axisbelow(True)
    return fig,ax

def save(fig,folder,name):
    folder.mkdir(exist_ok=True,parents=True);fig.savefig(folder/(name+'.pdf'),bbox_inches='tight');plt.close(fig)

def node(ax,xy,label,color=NAVY,r=.17):
    ax.add_patch(Circle(xy,r,facecolor='white',edgecolor=color,lw=1.6,zorder=5))
    ax.text(*xy,label,ha='center',va='center',color=color,zorder=6,fontsize=10)

def arrow(ax,start,end,label='',rad=0,color=NAVY):
    arr=FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=12,lw=1.4,color=color,connectionstyle=f'arc3,rad={rad}',shrinkA=13,shrinkB=13)
    ax.add_patch(arr)
    if label:
        x,y=(np.array(start)+np.array(end))/2
        ax.text(x,y+(.18 if rad<=0 else -.25),label,ha='center',va='center',color=color,fontsize=9,bbox=dict(facecolor='white',edgecolor='none',pad=1))

def complementaires():
    folder=ROOT/'livre-maths-complementaires/images'
    fig,aa=axes(2);n=np.arange(16);u=150-50*.8**n
    aa[0].plot(n,u,'o-',color=NAVY,ms=3);aa[0].axhline(150,color=GREEN,ls='--');aa[0].set(xlabel='Jour n',ylabel='Volume (L)',ylim=(95,155))
    ax=aa[1];x=np.linspace(95,155,200);ax.plot(x,.8*x+30,color=NAVY,label='y = 0,8x + 30');ax.plot(x,x,color=MUTED,ls='--',label='y = x')
    val=100
    for k in range(10):
        new=.8*val+30;ax.plot([val,val,new],[val,new,new],color=GREEN,lw=1);val=new
    ax.set(xlabel='Volume uₙ (L)',ylabel='Volume suivant (L)',xlim=(95,155),ylim=(95,155));ax.legend(fontsize=8,loc='upper left');save(fig,folder,'c01-suite')
    fig,ax=axes(height=3.1);x=np.linspace(-2,2,300);z=np.linspace(.1,7.3,300)
    ax.plot(x,np.exp(x),color=NAVY,label='Exponentielle');ax.plot(z,np.log(z),color=GREEN,label='Logarithme');ax.plot([-2,7.5],[-2,7.5],ls='--',color=MUTED,label='y = x')
    ax.scatter([0,1],[1,0],color=[NAVY,GREEN],s=22);ax.set(xlim=(-2,7.5),ylim=(-2,7.5),xlabel='x',ylabel='y',aspect='equal');ax.legend(loc='upper left',fontsize=9);save(fig,folder,'c02-reciproques')
    fig,ax=axes();
    for a,b in [(-4,.84),(1.16,6)]:
        x=np.linspace(a,b,300);ax.plot(x,2+1/(x-1),color=NAVY)
    ax.axvline(1,color=ORANGE,ls='--',label='x = 1');ax.axhline(2,color=GREEN,ls='--',label='y = 2');ax.set(xlim=(-4,6),ylim=(-4,8),xlabel='x',ylabel='f(x)');ax.legend(loc='upper left',fontsize=9);save(fig,folder,'c03-asymptotes')
    fig,aa=axes(2);x=np.linspace(0,20,200);aa[0].plot(x,x*(20-x),color=NAVY);aa[0].scatter([10],[100],color=GREEN);aa[0].set(xlabel='Largeur x (m)',ylabel='Aire (m²)')
    ax=aa[1];ax.axis('off');ax.add_patch(Rectangle((.1,.2),.8,.5,fill=False,ec=NAVY,lw=2));ax.text(.5,.1,'Longueur : 20 − x',ha='center');ax.text(.5,.8,'Périmètre : 40 m',ha='center');ax.text(.93,.45,'x',ha='left');ax.set(xlim=(0,1.1),ylim=(0,1));save(fig,folder,'c04-optimisation')
    fig,aa=axes(2);x=np.linspace(-1.5,1.5,300);aa[0].plot(x,x*x,color=NAVY,label='x²');aa[0].plot([-1,1],[1,1],color=ORANGE,label='Corde');aa[0].plot(x,0*x,color=GREEN,label='Tangente en 0');aa[0].set(xlabel='x',ylabel='y',ylim=(-.4,2.5));aa[0].legend(fontsize=8)
    x=np.linspace(.25,3,300);aa[1].plot(x,np.log(x),color=NAVY,label='ln x');aa[1].plot(x,x-1,color=GREEN,label='Tangente en 1');aa[1].legend(fontsize=8);aa[1].set(xlabel='x',ylabel='y');save(fig,folder,'c05-convexite')
    fig,ax=axes();x=np.linspace(0,1,300);ax.plot(x,x,ls='--',color=MUTED,label='Égalité');ax.plot(x,x*x,color=NAVY,label='L(x) = x²');ax.plot(x,x**3,color=GREEN,label='L(x) = x³');ax.set(xlabel='Part cumulée de population',ylabel='Part cumulée de richesse',xlim=(0,1),ylim=(0,1));ax.legend(fontsize=9);save(fig,folder,'c05-lorenz')
    fig,ax=axes();t=np.linspace(0,15,300);ax.plot(t,20+60*np.exp(-.2*t),color=NAVY,label='Solution exacte');n=np.arange(16);ax.plot(n,20+60*.8**n,'o--',color=GREEN,ms=3,label='Euler, pas 1');ax.axhline(20,ls=':',color=MUTED);ax.set(xlabel='Temps (min)',ylabel='Température (°C)');ax.legend(fontsize=9);save(fig,folder,'c06-equadiff')
    fig,ax=axes();x=np.linspace(0,3,300);ax.plot(x,x-1,color=NAVY);ax.fill_between(x,x-1,0,where=x<=1,color=ORANGE,alpha=.25);ax.fill_between(x,x-1,0,where=x>=1,color=GREEN,alpha=.25);ax.axhline(0,color=MUTED,lw=.8);ax.set(xlabel='x',ylabel='f(x)');ax.text(.25,-.65,'−1/2',color=ORANGE);ax.text(2.2,.5,'+2',color=GREEN);save(fig,folder,'c07-aires')
    fig,ax=axes();x=np.linspace(0,1,300);ax.plot(x,x*x,color=NAVY,label='x²')
    for k in range(6):ax.add_patch(Rectangle((k/6,0),1/6,(k/6)**2,facecolor=GREEN,alpha=.2,edgecolor=GREEN,lw=1))
    ax.set(xlabel='x',ylabel='y',xlim=(0,1),ylim=(0,1.05));save(fig,folder,'c07-rectangles')
    fig,ax=axes(height=2.9);ax.axis('off');positions=[(0,1.5),(1.5,2.4),(1.5,.6),(3.5,2.8),(3.5,2),(3.5,1),(3.5,.2)]
    for i,j,label in [(0,1,'0,02'),(0,2,'0,98'),(1,3,'0,95'),(1,4,'0,05'),(2,5,'0,05'),(2,6,'0,95')]:
        a,b=positions[i],positions[j];ax.plot([a[0],b[0]],[a[1],b[1]],color=NAVY,lw=1);m=(np.array(a)+np.array(b))/2;ax.text(m[0],m[1]+.09,label,ha='center',color=GREEN,fontsize=9,bbox=dict(facecolor='white',edgecolor='none',pad=1))
    for xy,label in zip(positions,['','M','non M','+ : 190','− : 10','+ : 490','− : 9 310']):ax.text(xy[0],xy[1],label,ha='left',va='center',color=NAVY,bbox=dict(facecolor='white',edgecolor='none',pad=2))
    ax.set(xlim=(-.2,5),ylim=(-.1,3.2));save(fig,folder,'c08-bayes')
    fig,ax=axes(height=2.7);ax.axis('off')
    for lev in range(3):
        for k in range(2**lev):
            y=(k+.5)/2**lev;xx=lev
            for d in range(2):
                yy=(2*k+d+.5)/2**(lev+1);ax.plot([xx,xx+1],[y,yy],color=NAVY,alpha=.65);ax.text(xx+.48,(y+yy)/2+(.015 if d==0 else -.015),'p' if d==0 else '1−p',fontsize=8,color=GREEN,ha='center',bbox=dict(facecolor='white',edgecolor='none',pad=.4))
    for k in range(8):ax.text(3.06,(k+.5)/8,format(k,'03b').replace('0','S').replace('1','E'),va='center',fontsize=9)
    ax.set(xlim=(-.1,3.7),ylim=(0,1));save(fig,folder,'c09-bernoulli')
    fig,ax=axes();k=np.arange(11);pr=np.array([comb(10,int(j))*.3**j*.7**(10-j) for j in k]);ax.bar(k,pr,color=NAVY,width=.6);ax.set(xlabel='Nombre de succès k',ylabel='P(X = k)',xticks=k);save(fig,folder,'c09-binomiale')
    fig,aa=axes(2)
    for ax,n in zip(aa,[20,100]):
        k=np.arange(n+1);pr=[comb(n,int(j))*2.**(-n) for j in k];ax.vlines(k/n,0,pr,color=NAVY,lw=1.4);ax.set(xlabel='Fréquence',ylabel='Probabilité',title=f'n = {n}',xlim=(0,1))
    save(fig,folder,'c10-fluctuation')
    fig,aa=axes(2);k=np.arange(1,16);aa[0].bar(k,.25*.75**(k-1),color=NAVY,width=.55);aa[0].set(xlabel='Rang k',ylabel='P(X = k)');n=np.arange(16);aa[1].plot(n,.75**n,'o-',color=GREEN,ms=3);aa[1].set(xlabel='Essais n',ylabel='P(X > n)');save(fig,folder,'c11-geometrique')
    fig,aa=axes(2);x=np.linspace(0,12,300);aa[0].plot([0,10],[.1,.1],color=NAVY);aa[0].fill_between([2,6],[.1,.1],color=GREEN,alpha=.25);aa[0].set(xlabel='Temps (min)',ylabel='Densité',ylim=(0,.13),xlim=(0,12));aa[0].set_title('Uniforme sur [0,10]',fontsize=10)
    aa[1].plot(x,.2*np.exp(-.2*x),color=NAVY);aa[1].fill_between(x,0,.2*np.exp(-.2*x),where=(x>=2)&(x<=6),color=GREEN,alpha=.25);aa[1].set(xlabel='Temps (min)',ylabel='Densité',ylim=(0,.22));aa[1].set_title('Exponentielle, λ = 0,2',fontsize=10);save(fig,folder,'c11-densites')
    fig,ax=axes();x=np.array([1,2,3,4]);y=np.array([2,3,5,6]);xx=np.linspace(.5,4.5,100);ax.plot(xx,1.4*xx+.5,color=GREEN,label='Droite ajustée');ax.scatter(x,y,color=NAVY,zorder=4);ax.vlines(x,y,1.4*x+.5,color=ORANGE,lw=2);ax.scatter([2.5],[4],marker='D',color=ORANGE,zorder=5,label='Point moyen');ax.set(xlabel='x',ylabel='y');ax.legend(fontsize=9);save(fig,folder,'c12-regression')
    fig,ax=axes(height=1.9);ax.axis('off');p=[(.5,.85),(.15,.15),(.85,.15)];labels=['Température','Ventes de boissons','Baignades']
    for xy,label in zip(p,labels):ax.text(*xy,label,ha='center',va='center',fontsize=10,color=NAVY,bbox=dict(boxstyle='round,pad=.6',fc='#EDF2FC',ec='#D3DCEF'))
    for end in p[1:]:ax.annotate('',xy=(end[0],end[1]+.12),xytext=(p[0][0],p[0][1]-.12),arrowprops=dict(arrowstyle='->',color=GREEN,lw=1.6))
    ax.set(xlim=(0,1),ylim=(-.1,1.1));save(fig,folder,'c12-causalite')
    fig,ax=axes(height=2.5);ax.axis('off');coords=[(.12,.7),(.45,.7),(.8,.7),(.45,.2)];labels=['Initialiser\nn = 0, u = u₀','Seuil atteint ?','Rendre n, u','Mettre à jour\nu, puis n']
    for xy,label in zip(coords,labels):ax.text(*xy,label,ha='center',va='center',fontsize=9,color=NAVY,bbox=dict(boxstyle='round,pad=.65',fc='#EDF2FC',ec=NAVY))
    for i,j in [(0,1),(1,2),(1,3)]:ax.annotate('',xy=(coords[j][0]-.11 if j!=3 else coords[j][0],coords[j][1] if j!=3 else coords[j][1]+.12),xytext=(coords[i][0]+.11 if j!=3 else coords[i][0],coords[i][1] if j!=3 else coords[i][1]-.12),arrowprops=dict(arrowstyle='->',color=GREEN,lw=1.4))
    ax.annotate('',xy=(.35,.62),xytext=(.35,.27),arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=-.6',color=GREEN,lw=1.4));ax.text(.62,.8,'oui',color=GREEN,fontsize=9);ax.text(.48,.47,'non',color=GREEN,fontsize=9);ax.set(xlim=(-.06,1),ylim=(-.03,1));save(fig,folder,'c13-algorithme')

def expertes():
    folder=ROOT/'livre-maths-expertes/images'
    def plane(ax,lim):
        ax.axhline(0,color=MUTED,lw=.7);ax.axvline(0,color=MUTED,lw=.7)
        ax.set(xlabel='Partie réelle',ylabel='Partie imaginaire',xlim=lim[:2],ylim=lim[2:],aspect='equal')
    fig,aa=axes(2);plane(aa[0],(-1,4,-4,4));aa[0].scatter([2,2],[3,-3],c=[NAVY,GREEN],s=30);aa[0].plot([2,2],[-3,3],ls=':',color=MUTED);aa[0].text(2.15,3,'z',color=NAVY);aa[0].text(2.15,-3,'z̄',color=GREEN)
    aa[1].axis('off');aa[1].text(.05,.8,'z = 2 + 3i\nConjugué : 2 − 3i\n\nMême abscisse\nOrdonnées opposées',va='top',fontsize=12,color=NAVY);save(fig,folder,'e01-conjugaison')
    fig,aa=axes(2);ax=aa[0];plane(ax,(-.5,4,-.5,3));ax.annotate('',xy=(3,2),xytext=(0,0),arrowprops=dict(arrowstyle='->',lw=2,color=NAVY));ax.plot([0,3,3],[0,0,2],ls=':',color=GREEN);ax.text(3.1,2.05,'M');angle=np.linspace(0,np.arctan2(2,3),40);ax.plot(.8*np.cos(angle),.8*np.sin(angle),color=ORANGE);ax.text(.9,.2,'θ',color=ORANGE)
    aa[1].axis('off');aa[1].text(.05,.85,'z = 3 + 2i\n\n|z| = √13\ncos θ = 3/√13\nsin θ = 2/√13',va='top',fontsize=12,color=NAVY);save(fig,folder,'e02-module')
    fig,aa=axes(2)
    for ax in aa:plane(ax,(-2,4,-2,4))
    aa[0].add_patch(Circle((1,1),2,fill=False,ec=NAVY,lw=1.6));aa[0].scatter([1],[1],c=GREEN,s=22);aa[0].text(1.12,.75,'1 + i',fontsize=9)
    aa[1].axvline(0,color=GREEN,lw=2);aa[1].scatter([-1,1],[0,0],c=NAVY);aa[1].text(-1,-.5,'−1',ha='center');aa[1].text(1,-.5,'1',ha='center');save(fig,folder,'e02-lieux')
    fig,aa=axes(2);ax=aa[0];plane(ax,(-1.3,1.3,-.3,1.4));ax.add_patch(Circle((0,0),1,fill=False,ec='#98A2B3',lw=.8))
    for theta,label,col in [(np.pi/6,'π/6',NAVY),(np.pi/3,'π/3',GREEN),(np.pi/2,'π/2',ORANGE)]:
        p=(np.cos(theta),np.sin(theta));ax.annotate('',xy=p,xytext=(0,0),arrowprops=dict(arrowstyle='->',color=col,lw=1.6));ax.text(p[0]+.08,p[1]+.04,label,color=col,fontsize=10)
    aa[1].axis('off');aa[1].text(.05,.85,'Arguments : π/6 + π/3 = π/2\n\nModules : 2 × 3 = 6\n\nLe produit vaut 6i.',va='top',fontsize=11,color=NAVY);save(fig,folder,'e03-produit')
    fig,aa=axes(2);plane(aa[0],(-1,3,-2,2));aa[0].scatter([2,0,0],[0,1,-1],color=NAVY,s=28)
    for x,y,label in [(2,0,'2'),(0,1,'i'),(0,-1,'−i')]:aa[0].text(x+.12,y+.12,label,color=GREEN)
    aa[1].axis('off');aa[1].text(.05,.8,'P(z) = (z − 2)(z² + 1)\n\nRacines :\n2, i et −i',va='top',fontsize=12,color=NAVY);save(fig,folder,'e04-racines')
    fig,aa=axes(2);ax=aa[0];plane(ax,(-.5,3.6,-.5,2.8));ax.plot([1,3,1,1],[0,0,2,0],color=NAVY);ax.plot([1,1.22,1.22],[.22,.22,0],color=GREEN)
    for x,y,label in [(1,0,'A'),(3,0,'B'),(1,2,'C')]:ax.scatter([x],[y],color=NAVY,s=20);ax.text(x+.13,y+.12,label)
    aa[1].axis('off');aa[1].text(.03,.8,'(c − a)/(b − a) = i\n\nAC/AB = 1\nAngle (AB, AC) = π/2\n\nRectangle isocèle en A',va='top',fontsize=11,color=NAVY);save(fig,folder,'e05-quotient')
    fig,aa=axes(3,height=2.5)
    for ax,n in zip(aa,[3,4,6]):
        plane(ax,(-1.35,1.35,-1.35,1.35));theta=np.arange(n)*2*np.pi/n;px=np.cos(theta);py=np.sin(theta);ax.add_patch(Circle((0,0),1,fill=False,ec=MUTED,lw=.7));ax.plot(np.r_[px,px[0]],np.r_[py,py[0]],color=GREEN,lw=1);ax.scatter(px,py,color=NAVY,s=18,zorder=5);ax.set_title(f'n = {n}',fontsize=11);ax.set_xticks([-1,0,1]);ax.set_yticks([-1,0,1]);ax.set_xlabel('Re');ax.set_ylabel('Im')
    save(fig,folder,'e05-unite')
    fig,ax=axes(height=1.8);ax.axis('off');ax.annotate('',xy=(1,0),xytext=(0,0),arrowprops=dict(arrowstyle='->',color=NAVY));
    for xx,label in [(.1,'−54'),(.45,'−48'),(.8,'−42')]:ax.plot([xx,xx],[-.07,.07],color=MUTED);ax.text(xx,-.15,label,ha='center',fontsize=11)
    ax.scatter([.45+.35/6],[0],color=GREEN,s=35,zorder=5);ax.text(.45+.35/6,.17,'−47 = −48 + 1',ha='center',color=GREEN,fontsize=12);ax.set(xlim=(-.05,1.1),ylim=(-.4,.5));save(fig,folder,'e06-division')
    fig,aa=axes(2);ax=aa[0];ax.axis('off');theta=np.pi/2-np.arange(7)*2*np.pi/7;pts=np.c_[np.cos(theta),np.sin(theta)]
    for k in range(7):
        arrow(ax,pts[k],pts[(k+1)%7],color=GREEN);node(ax,pts[k],str(k),r=.16)
    ax.set(xlim=(-1.5,1.5),ylim=(-1.5,1.5),aspect='equal');aa[1].axis('off');aa[1].text(.05,.8,'Modulo 7\n\n11 = 1 × 7 + 4\n−3 = (−1) × 7 + 4\n\n11 et −3 ont le même reste.',va='top',fontsize=11,color=NAVY);save(fig,folder,'e06-modulo')
    fig,ax=axes(height=2.25);ax.axis('off');rows=[['252','198','1','54'],['198','54','3','36'],['54','36','1','18'],['36','18','2','0']]
    table=ax.table(cellText=rows,colLabels=['Dividende','Diviseur','Quotient','Reste'],loc='center',cellLoc='center');table.auto_set_font_size(False);table.set_fontsize(11);table.scale(1,1.7)
    for (r,c),cell in table.get_celld().items():cell.set_edgecolor('#D3DCEF');cell.set_facecolor('#EDF2FC' if r==0 else 'white');cell.set_text_props(color=NAVY)
    table[(3,3)].set_facecolor('#E8F3E8');save(fig,folder,'e07-euclide')
    fig,ax=axes(height=2.3);ax.axis('off');primes=[n for n in range(2,51) if all(n%d for d in range(2,int(n**.5)+1))]
    for n in range(1,51):
        x=(n-1)%10;y=4-(n-1)//10;col=GREEN if n in primes else MUTED
        ax.add_patch(Rectangle((x-.44,y-.36),.88,.72,facecolor='#E8F3E8' if n in primes else '#F4F5F7',ec='white'))
        ax.text(x,y,str(n),ha='center',va='center',fontsize=11,color=col,fontweight='bold' if n in primes else 'normal')
    ax.set(xlim=(-.6,9.6),ylim=(-.55,4.55));save(fig,folder,'e08-crible')
    fig,ax=axes(height=1.7);ax.axis('off')
    for start,matrix,name in [(0,[[1,2],[3,4]],'A'),(3,[[0,1],[1,0]],'B'),(6,[[2,1],[4,3]],'AB')]:
        ax.text(start+.45,1.2,name,color=NAVY,ha='center',fontsize=12)
        for i,row in enumerate(matrix):
            for j,val in enumerate(row):
                highlight=(start==0 and i==0) or (start==3 and j==1) or (start==6 and i==0 and j==1)
                ax.add_patch(Rectangle((start+j*.5,i*-.5),.5,.5,fc='#E8F3E8' if highlight else '#EDF2FC',ec='white'));ax.text(start+j*.5+.25,i*-.5+.25,str(val),ha='center',va='center',fontsize=12,color=GREEN if highlight else NAVY)
    ax.text(1.9,.1,'×',ha='center',fontsize=18,color=MUTED);ax.text(4.9,.1,'=',ha='center',fontsize=18,color=MUTED);ax.set(xlim=(-.3,7.3),ylim=(-.8,1.6));save(fig,folder,'e09-produit')
    fig,aa=axes(2);ax=aa[0];plane(ax,(-2,3,-1,3))
    for p,label,col in [((2,1),'M(2,1)',NAVY),((-1,2),'M′(−1,2)',GREEN)]:ax.annotate('',xy=p,xytext=(0,0),arrowprops=dict(arrowstyle='->',lw=1.8,color=col));ax.text(p[0]-.1,p[1]+.22,label,color=col,fontsize=10)
    aa[1].axis('off');aa[1].text(.05,.85,'Rotation de π/2\n\n(x, y) → (−y, x)\n\nMatrice : lignes (0, −1)\n                 et (1, 0)',va='top',fontsize=11,color=NAVY);save(fig,folder,'e09-transformation')
    fig,ax=axes();n=np.arange(13);ax.plot(n,2*(1-.5**n),'o-',color=NAVY,label='uₙ',ms=3);ax.plot(n,4*(1-.25**n),'s-',color=GREEN,label='vₙ',ms=3);ax.axhline(2,color=NAVY,ls=':',lw=.9);ax.axhline(4,color=GREEN,ls=':',lw=.9);ax.set(xlabel='Étape n',ylabel='Valeur',ylim=(-.2,4.4));ax.legend();save(fig,folder,'e10-evolution')
    positions=[(0,0),(1,1.5),(2,0),(3.5,0)];edges=[(0,1),(0,2),(1,2),(2,3)]
    def graph(ax):
        ax.axis('off')
        for i,j in edges:ax.plot([positions[i][0],positions[j][0]],[positions[i][1],positions[j][1]],color='#98A2B3',lw=1.5)
        for xy,label in zip(positions,'ABCD'):node(ax,xy,label)
        ax.set(xlim=(-.4,4),ylim=(-.5,2),aspect='equal')
    fig,aa=axes(2);graph(aa[0]);aa[1].axis('off');aa[1].text(.05,.85,'Ordre : 4\nArêtes : 4\n\ndeg A = 2     deg B = 2\ndeg C = 3     deg D = 1\n\nSomme des degrés : 8',va='top',fontsize=11,color=NAVY);save(fig,folder,'e11-graphe')
    fig,aa=axes(2);graph(aa[0]);arrow(aa[0],positions[0],positions[2],color=GREEN);arrow(aa[0],positions[2],positions[3],color=GREEN);aa[0].text(1,-.3,'1',color=GREEN,ha='center');aa[0].text(2.75,-.3,'2',color=GREEN,ha='center');aa[1].axis('off');aa[1].text(.03,.8,'Longueur 2, de A vers D :\nA → C → D\n\nRetours en A, longueur 2 :\nA → B → A\nA → C → A',va='top',fontsize=11,color=NAVY);save(fig,folder,'e11-parcours')
    def loop(ax,x,label):
        ax.add_patch(FancyArrowPatch((x-.12,.13),(x+.12,.13),connectionstyle='arc3,rad=-2.8',arrowstyle='-|>',mutation_scale=11,lw=1.3,color=NAVY))
        ax.text(x,1.02,label,ha='center',va='center',color=NAVY,fontsize=11)
    fig,ax=axes(height=2.4);ax.axis('off');p0,p1=(0,0),(3,0);arrow(ax,p0,p1,rad=-.3);arrow(ax,p1,p0,rad=-.3);node(ax,p0,'A',r=.2);node(ax,p1,'B',r=.2);loop(ax,0,'0,8');loop(ax,3,'0,7');ax.text(1.5,.63,'0,2',ha='center',color=GREEN);ax.text(1.5,-.63,'0,3',ha='center',color=GREEN);ax.set(xlim=(-.9,3.9),ylim=(-.95,1.35));save(fig,folder,'e12-markov2')
    fig,ax=axes(height=2.4);ax.axis('off')
    for i,label in enumerate('ABC'):node(ax,(2*i,0),label,r=.2);loop(ax,2*i,'1/2')
    for left,right,up,down in [(0,2,'1/2','1/4'),(2,4,'1/4','1/2')]:
        arrow(ax,(left,0),(right,0),rad=-.3);arrow(ax,(right,0),(left,0),rad=-.3);ax.text((left+right)/2,.5,up,ha='center',color=GREEN);ax.text((left+right)/2,-.5,down,ha='center',color=GREEN)
    ax.set(xlim=(-.7,4.7),ylim=(-.9,1.35));save(fig,folder,'e12-markov3')
    fig,ax=axes();P=np.array([[.5,.5,0],[.25,.5,.25],[0,.5,.5]]);rows=[np.array([1.,0.,0.])]
    for k in range(10):rows.append(rows[-1]@P)
    arr=np.array(rows)
    for j,label,col in zip(range(3),'ABC',[NAVY,GREEN,ORANGE]):ax.plot(range(11),arr[:,j],marker='o',ms=3,color=col,label=label)
    ax.set(xlabel='Nombre de transitions n',ylabel='Probabilité',ylim=(-.03,1.05));ax.legend();save(fig,folder,'e12-convergence')

if __name__=='__main__':
    import sys
    globals()[sys.argv[1]]()
