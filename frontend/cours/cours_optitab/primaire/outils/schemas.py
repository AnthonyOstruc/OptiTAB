"""Figures vectorielles originales, exportées en PNG lisibles sur téléphone."""
import io
import math
import textwrap
from pathlib import Path
import fitz
from PIL import Image,ImageChops
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor,white

for key,name in [('Primaire','arial.ttf'),('PrimaireGras','arialbd.ttf'),('Text','arial.ttf'),('Bold','arialbd.ttf')]:
    if key not in pdfmetrics.getRegisteredFontNames():pdfmetrics.registerFont(TTFont(key,'C:/Windows/Fonts/'+name))
BLUE='#245da5';GREEN='#23734d';PALE='#eaf2fb';INK='#23384e';GREY='#bdcbd8'

def save_png(data,path):
    doc=fitz.open(stream=data,filetype='pdf');pix=doc[0].get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
    im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
    diff=ImageChops.difference(im,Image.new('RGB',im.size,'white')).convert('L').point(lambda x:255 if x>30 else 0)
    bounds=diff.getbbox();assert bounds
    x0,y0,x1,y1=bounds
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    im.crop((max(0,x0-16),max(0,y0-16),min(im.width,x1+16),min(im.height,y1+16))).save(path)
    doc.close()

def draw(s,path,correction=False):
    W,H=480,250;buf=io.BytesIO();cv=canvas.Canvas(buf,pagesize=(W,H));color=GREEN if correction else BLUE
    def text(txt,x,y,size=17,bold=False,center=False,col=INK):
        cv.setFillColor(HexColor(col));cv.setFont('PrimaireGras' if bold else 'Primaire',size)
        (cv.drawCentredString if center else cv.drawString)(x,y,str(txt))
    def line(x1,y1,x2,y2,col=color,width=2,dash=None):
        cv.setStrokeColor(HexColor(col));cv.setLineWidth(width);cv.setDash(dash or []);cv.line(x1,y1,x2,y2);cv.setDash([])
    def rect(x,y,w,h,fill=None,col=color):
        cv.setStrokeColor(HexColor(col));cv.setLineWidth(1.5);cv.setFillColor(HexColor(fill) if fill else white);cv.rect(x,y,w,h,stroke=1,fill=1)
    def dot(x,y,label='',col=color):
        cv.setFillColor(HexColor(col));cv.circle(x,y,3,stroke=0,fill=1)
        if label:text(label,x+6,y+6,16,col=col)
    def note(txt):
        for j,row in enumerate(textwrap.wrap(txt,56)):text(row,240,28-j*19,15,center=True,col=color)
    kind=s['type']
    if kind=='place':
        digits=str(s['number']);labels=['u','d','c','m','dm','cm','M','dM','cM'][:len(digits)][::-1];cw=min(64,430/len(digits));start=(W-cw*len(digits))/2
        for j,(label,d) in enumerate(zip(labels,digits)):
            x=start+j*cw;rect(x,105,cw,44);rect(x,149,cw,34,PALE)
            text(label,x+cw/2,159,16,True,True);text(d,x+cw/2,118,23,True,True)
        note('Chaque chiffre garde son rang.' if not correction else 'Je regroupe par paquets de dix, cent ou mille.')
    elif kind in ('partwhole','comparison'):
        a,b=s['a'],s.get('b',s.get('difference'));top=165
        rect(30,top,275,42,PALE);text(a,167,top+13,20,True,True)
        rect(305,top,135,42,'#fff4d7');text(('− ' if s.get('minus') else '+ ')+str(b),372,top+13,20,True,True)
        total=a-b if s.get('minus') else a+b
        rect(30,85,410,42);text(str(total) if correction else '?',235,98,22,True,True,col=color)
        note('La deuxième quantité est la première plus l’écart.' if kind=='comparison' else 'Je relie le changement à la quantité de départ.')
    elif kind=='groups':
        groups,size=s['groups'],s['size'];shown=min(groups,8);cw=420/shown
        for j in range(shown):
            rect(25+j*cw,100,cw-6,70,PALE)
            text(size,25+j*cw+(cw-6)/2,126,18 if shown<7 else 16,True,True)
        text(f'{groups} groupes de {size}',240,205,20,True,True)
        if groups>shown:text('Seuls les premiers groupes sont dessinés.',240,72,14,center=True)
        note(f'Total des groupes : {groups*size}'+(f' ; reste : {s["remainder"]}' if s.get('remainder') else '') if correction else 'Tous les groupes ont la même quantité.')
    elif kind in ('fraction','unitlength'):
        d=s['denominator'];num=s.get('numerator',s.get('parts',1));cw=420/d
        for j in range(d):rect(30+j*cw,135,cw,45,'#9dc5ed' if j<num else None)
        text('Une unité entière',240,203,19,True,True)
        if s.get('split'):
            for j in range(2*d):rect(30+j*420/(2*d),65,420/(2*d),35,'#9dc5ed' if j<2*num else None)
        elif s.get('added') and correction:
            for j in range(d):rect(30+j*cw,65,cw,35,'#9dc5ed' if j<num else '#a5d8b5' if j<num+s['added'] else None)
        elif kind=='unitlength':text(f'{s["whole"]} unité(s) entière(s), puis {s["parts"]}/{d} u',240,85,19,center=True)
        note(f'{num} part(s) sur {d} ; tout : {d}/{d}' if correction else 'Les parts de l’unité sont de même taille.')
    elif kind in ('numberline','fractionline'):
        start=s.get('start',0);step=s.get('step',1);d=s.get('denominator',1);num=s.get('numerator',0)
        count=6 if kind=='numberline' else num+2; spacing=420/count
        line(30,130,455,130)
        for j in range(count+1):
            x=30+j*spacing;line(x,123,x,137)
            if kind=='numberline':label=start+j*step if j in (0,1,3,6) or correction else ''
            else:label=str(j//d) if j%d==0 else ''
            if label!='':text(label,x,92,14 if count>10 else 17,center=True)
        if kind=='fractionline':dot(30+num*spacing,130,'A');note(f'A : {num}/{d} = {num//d} + {num%d}/{d}' if correction else f'L’unité est partagée en {d} parts égales.')
        else:note(f'Un saut vaut {step}.' if correction else 'Lis la valeur d’une graduation.')
    elif kind=='program':
        for j,txt in enumerate(s['lines']):
            rect(90,180-j*56,300,42,PALE);text(txt,240,193-j*56,19,True,True)
            if j<2:line(240,178-j*56,240,168-j*56)
        note('Sortie : '+str(s['answer']) if correction else 'Lire les instructions dans l’ordre.')
    elif kind=='decimal':
        value=s['value'];whole,decimal=(value.split(',')+[''])[:2];labels=['unités','dixièmes','centièmes']+(['millièmes'] if s['denominator']==1000 else [])
        vals=[whole]+list(decimal.ljust(len(labels)-1,'0'));cw=440/len(labels)
        for j,(lab,v) in enumerate(zip(labels,vals)):
            rect(20+j*cw,110,cw,45);rect(20+j*cw,155,cw,35,PALE)
            text(lab,20+(j+.5)*cw,167,14,True,True);text(v,20+(j+.5)*cw,123,22,True,True)
        note('Des parts de plus en plus petites après la virgule.')
    elif kind=='prices':
        for j,(label,v) in enumerate(zip(s['labels'],s['values'])):
            rect(35+j*220,98,190,100,PALE);text(label,130+j*220,164,17,True,True);text(v,130+j*220,123,21,True,True,col=color)
        note('Je garde les euros et les centimes à leur place.')
    elif kind=='measure':
        rect(35,150,410,48,PALE);text(s['initial'],240,166,22,True,True)
        text('Utilisation / partage : '+s['used'],240,105,18,center=True)
        note('Résultat : '+s['answer'] if correction else 'Choisis une unité commune avant de calculer.')
    elif kind in ('rectangle','area'):
        L=s.get('length',s.get('cols'));w=s.get('width',s.get('rows'));bw=280;bh=min(130,bw*w/L);x=100;y=75
        rect(x,y,bw,bh,PALE)
        if s.get('grid') or kind=='area':
            for j in range(1,L):line(x+j*bw/L,y,x+j*bw/L,y+bh,GREY,.7)
            for j in range(1,w):line(x,y+j*bh/w,x+bw,y+j*bh/w,GREY,.7)
        text(str(L)+(' cm' if kind=='rectangle' else ' colonnes'),240,y+bh+15,18,True,True);text(str(w),65,y+bh/2,18,True,True)
        if kind=='area':rect(x+bw-bw/L,y+bh-bh/w,bw/L,bh/w,'#ffd9b0');note(f'A : {L*w} carreaux ; B : {L*w-1} carreaux' if correction else 'Le carré orange est retiré pour obtenir B.')
        else:note(f'Contour : {2*(L+w)} cm'+(f' ; aire : {L*w} cm²' if s.get('grid') else '') if correction else 'Schéma ; utilise les longueurs indiquées.')
    elif kind=='angles':
        for j,deg in enumerate([40,90,130]):
            x=45+j*155;y=110;length=72;ang=math.radians(deg)
            line(x,y,x+length,y);line(x,y,x+length*math.cos(ang),y+length*math.sin(ang))
            text('ABC'[j],x+25,78,19,True,True)
            if deg==90:line(x+12,y,x+12,y+12);line(x,y+12,x+12,y+12)
            if correction:text(['aigu','droit','obtus'][j],x+25,50,16,True,True,col=GREEN)
        note('Comparer les ouvertures avec un angle droit.')
    elif kind in ('timeline','clock'):
        h,minute=s['hour'],s['minute']
        if kind=='clock':
            x,y,r=240,140,76;cv.setStrokeColor(HexColor(color));cv.circle(x,y,r,stroke=1,fill=0)
            for number in range(1,13):
                angle=math.radians(90-number*30);text(number,x+math.cos(angle)*(r-15),y+math.sin(angle)*(r-15)-5,14,center=True)
            for val,length in [((h%12)*30+minute/2,42),(minute*6,60)]:
                angle=math.radians(90-val);line(x,y,x+length*math.cos(angle),y+length*math.sin(angle),width=3)
            dot(x,y)
        else:
            line(35,140,440,140);dot(45,140);dot(430,140)
            text(f'{h} h {minute:02}',45,175,19,True);text(f'+ {s["duration"]} min',240,95,20,True,True)
            text(s['answer'] if correction else '?',430,175,19,True,True)
        note('Fin : '+s['answer'] if correction else 'Une heure contient 60 minutes.')
    elif kind=='circle':
        x,y,r=240,140,76;cv.setStrokeColor(HexColor(color));cv.setLineWidth(2);cv.circle(x,y,r,stroke=1,fill=0)
        line(x-r,y,x+r,y);dot(x-r,y,'A');dot(x,y,'O');dot(x+r,y,'B')
        text(f'AB = {2*s["radius"]} cm',240,40,20,True,True)
        if correction:text(f'AO = OB = {s["radius"]} cm',240,20,17,center=True,col=GREEN)
    elif kind=='polygons':
        cm2=s['cm2'];nbs=[3,4,5,6] if cm2 else [3,4,4,4]
        for j,nb in enumerate(nbs):
            cx=65+j*116;cy=145;R=45;points=[]
            if not cm2 and j==1:points=[(cx-46,cy-28),(cx+46,cy-28),(cx+46,cy+28),(cx-46,cy+28)]
            elif not cm2 and j==2:points=[(cx-34,cy-34),(cx+34,cy-34),(cx+34,cy+34),(cx-34,cy+34)]
            elif not cm2 and j==3:points=[(cx-48,cy),(cx,cy+30),(cx+48,cy),(cx,cy-30)]
            else:points=[(cx+R*math.cos(math.radians(90+k*360/nb)),cy+R*math.sin(math.radians(90+k*360/nb))) for k in range(nb)]
            p=cv.beginPath();p.moveTo(*points[0]);[p.lineTo(*pt) for pt in points[1:]];p.close();cv.setFillColor(HexColor(PALE));cv.setStrokeColor(HexColor(color));cv.drawPath(p,stroke=1,fill=1)
            if not cm2 and j in (1,2):
                for k,(px,py) in enumerate(points):
                    prev=points[k-1];nxt=points[(k+1)%4];v1=(prev[0]-px,prev[1]-py);v2=(nxt[0]-px,nxt[1]-py);v1=tuple(v*8/math.hypot(*v1) for v in v1);v2=tuple(v*8/math.hypot(*v2) for v in v2)
                    line(px+v1[0],py+v1[1],px+v1[0]+v2[0],py+v1[1]+v2[1]);line(px+v2[0],py+v2[1],px+v1[0]+v2[0],py+v1[1]+v2[1])
            if not cm2 and j in (2,3):
                for k,p1 in enumerate(points):
                    p2=points[(k+1)%4];mx=(p1[0]+p2[0])/2;my=(p1[1]+p2[1])/2;dx=p2[0]-p1[0];dy=p2[1]-p1[1];norm=math.hypot(dx,dy);line(mx-4*dy/norm,my+4*dx/norm,mx+4*dy/norm,my-4*dx/norm)
            text('ABCD'[j],cx,65,20,True,True)
        note('Lis les codes et compte les côtés.')
    elif kind in ('symmetry','path'):
        step=22;ox=130;oy=48
        for j in range(11):line(ox+j*step,oy,ox+j*step,oy+8*step,GREY,.6)
        for j in range(9):line(ox,oy+j*step,ox+10*step,oy+j*step,GREY,.6)
        def pt(p):return ox+p[0]*step,oy+p[1]*step
        if kind=='path':
            x,y=s['start'];dot(*pt((x,y)),'D')
            if correction:
                line(*pt((x,y)),*pt((x+s['right'],y)));line(*pt((x+s['right'],y)),*pt((x+s['right'],y+s['up'])));dot(*pt((x+s['right'],y+s['up'])),'Arrivée')
        else:
            axis=s['axis'];off=s['offset']
            if axis=='oblique':line(*pt((1,1)),*pt((8,8)),dash=[5,4]);points=[(2,5),(2,7),(4,6)];images=[(y,x) for x,y in points]
            elif axis=='horizontal':line(*pt((0,4)),*pt((10,4)),dash=[5,4]);points=[(2,4+off),(4,7),(6,5)];images=[(x,8-y) for x,y in points]
            else:line(*pt((5,0)),*pt((5,8)),dash=[5,4]);points=[(5-off,2),(1,5),(3,6)];images=[(10-x,y) for x,y in points]
            for k,p1 in enumerate(points):line(*pt(p1),*pt(points[(k+1)%3]),BLUE);dot(*pt(p1),'ABC'[k],BLUE)
            if correction:
                for k,p1 in enumerate(images):line(*pt(p1),*pt(images[(k+1)%3]),GREEN);dot(*pt(p1),'ABC'[k]+'′',GREEN)
        note('Une case = un pas.' if kind=='path' else 'Le pliage doit superposer les deux triangles.')
    elif kind=='solid':
        pts=[(45,80),(135,80),(135,170),(45,170),(75,110),(165,110),(165,200),(75,200)]
        for u,v in [(0,1),(1,2),(2,3),(3,0),(3,7),(7,6),(6,2),(1,5),(5,6)]:line(*pts[u],*pts[v])
        for u,v in [(0,4),(4,5),(4,7)]:line(*pts[u],*pts[v],dash=[4,3])
        for x,y in [(1,0),(1,1),(1,2),(1,3),(0,2),(2,2)]:rect(265+x*34,65+y*34,34,34,PALE)
        text('Cube',100,40,18,True,True);text('Patron possible',330,40,18,True,True)
        if correction:note('6 faces ; 12 arêtes ; 8 sommets.')
    elif kind=='bars':
        vs=s['values'];labels=s['labels'];maxv=max(vs);scale=140/maxv
        for j in range(0,maxv+1,max(1,maxv//5)):
            y=70+j*scale;line(55,y,445,y,GREY,.6);text(j,38,y-5,14,center=True)
        for j,(label,v) in enumerate(zip(labels,vs)):
            x=90+j*125;rect(x,70,65,v*scale,'#8db5df');text(v,x+32,78+v*scale,17,True,True);text(label,x+32,45,16,center=True)
        text('Nombre d’élèves',240,230,18,True,True)
        if correction:note('Total : '+str(sum(vs))+' élèves.')
    elif kind=='tokens':
        colors=['#ba3e47','#3179c0','#2d8955'];labels=['rouges','bleus','vert(s)'];x=35;y=155
        for count,col,label in zip(s['counts'],colors,labels):
            for k in range(count):
                cv.setFillColor(HexColor(col));cv.circle(x+k*20,y,7,stroke=0,fill=1)
            text(f'{count} {label}',350,y-5,18,bold=True);y-=40
        note('Total : '+str(sum(s['counts']))+' jetons.' if correction else 'Même taille, même chance pour chaque jeton.')
    elif kind=='choices':
        colors,shapes=s['colors'],s['shapes'];text('Couleurs',100,220,18,True,True);text('Formes',320,220,18,True,True)
        for j in range(colors):
            y=180-j*60;dot(100,y,'C'+str(j+1))
            for k in range(shapes):
                yy=y+(k-(shapes-1)/2)*12;line(135,y,285,yy,width=1);text('F'+str(k+1),300,yy-5,14)
        note('Puis deux décors pour chaque couple couleur-forme.')
    else:raise ValueError(kind)
    cv.save();save_png(buf.getvalue(),path)
