"""Schémas vectoriels originaux. Coordonnées en points, dessin dans une zone."""
from math import sin,cos,pi
from reportlab.lib.colors import HexColor,white
from reportlab.lib.units import mm

NAVY=HexColor('#1B3C8E'); INK=HexColor('#1C2130'); GREEN=HexColor('#3B8544')
PALE=HexColor('#EEF4F1'); GREY=HexColor('#A7B1C0'); ORANGE=HexColor('#B96514')

def diagram(c,spec,x,y,w,h):
    """x,y = coin inférieur gauche. Tous les dessins sont contenus dans w,h."""
    if not spec:return
    kind,data=spec
    c.saveState();c.translate(x,y)
    c.setStrokeColor(NAVY);c.setFillColor(INK);c.setLineWidth(1)
    def txt(s,xx,yy,size=12,bold=False,center=False):
        c.setFont('Bold' if bold else 'Text',size);c.setFillColor(INK)
        (c.drawCentredString if center else c.drawString)(xx,yy,str(s))
    def dot(xx,yy,r=7,fill=True):
        c.setFillColor(PALE if fill else white);c.setStrokeColor(NAVY)
        c.circle(xx,yy,r,stroke=1,fill=1)
        if fill:
            c.setFillColor(NAVY);c.circle(xx,yy,r*.47,stroke=0,fill=1)
    def dots(n,xx,yy,step=19,cols=10):
        for i in range(n):dot(xx+(i%cols)*step,yy-(i//cols)*step)
    def base(n,xx,yy,unit=8):
        tens,ones=divmod(n,10)
        for i in range(tens):
            c.setFillColor(PALE);c.setStrokeColor(GREEN)
            c.rect(xx+i*(unit+8),yy,unit,unit*10,stroke=1,fill=1)
            for j in range(1,10):c.line(xx+i*(unit+8),yy+j*unit,xx+i*(unit+8)+unit,yy+j*unit)
        bx=xx+tens*(unit+8)+18
        for i in range(ones):
            c.setFillColor(white);c.setStrokeColor(NAVY)
            c.rect(bx+(i%5)*(unit+5),yy+(i//5)*(unit+5),unit,unit,stroke=1,fill=1)
    def grid(xx,yy,cols=7,rows=5,step=17):
        c.setStrokeColor(GREY);c.setLineWidth(.5)
        for a in range(cols+1):c.line(xx+a*step,yy,xx+a*step,yy+rows*step)
        for b in range(rows+1):c.line(xx,yy+b*step,xx+cols*step,yy+b*step)
        c.setStrokeColor(NAVY);c.setLineWidth(1.6)
    def gridshape(shape,a,b,xx,yy,step=17,partial=False):
        c.setStrokeColor(NAVY);c.setLineWidth(2.3)
        if partial:
            c.line(xx,yy+b*step,xx+a*step,yy+b*step)
            if shape=='rectangle':c.line(xx,yy,xx,yy+b*step)
        elif shape in ['rectangle','square']:c.rect(xx,yy,a*step,b*step,stroke=1,fill=0)
        else:
            p=c.beginPath();p.moveTo(xx,yy);p.lineTo(xx+a*step,yy);p.lineTo(xx+a*step,yy+b*step);p.close();c.drawPath(p)
    if kind=='dots':
        n=data;step=24 if n<=10 else 20
        dots(n,max(20,(w-min(n,10)*step)/2),h/2+10,step)
    elif kind=='tenframe':
        step=min(30,h/2-5);xx=(w-5*step)/2;yy=(h-2*step)/2
        for i in range(10):
            a=i%5;b=1-i//5;c.setFillColor(white);c.setStrokeColor(GREY)
            c.rect(xx+a*step,yy+b*step,step,step,stroke=1,fill=1)
            if i<data:dot(xx+(a+.5)*step,yy+(b+.5)*step,step*.23)
    elif kind in ['collections','parts']:
        ns=data
        for j,n in enumerate(ns):
            xx=25+j*w/len(ns);cw=w/len(ns)-30
            c.setStrokeColor(GREY);c.roundRect(xx-10,10,cw,h-20,8,stroke=1,fill=0)
            if kind=='collections':txt(chr(65+j),xx+5,h-29,12,True)
            step=min(20,(cw-15)/max(1,min(n,5)))
            dots(n,xx+9,h/2+6,step,5)
        if kind=='parts':txt('+',w/2, h/2,22,True,True)
    elif kind=='remove':
        total,rem=data;xx=(w-total*25)/2;yy=h/2
        for i in range(total):
            dot(xx+i*25,yy,7)
            if i>=total-rem:
                c.setStrokeColor(INK);c.setLineWidth(1.4);c.line(xx+i*25-9,yy-9,xx+i*25+9,yy+9)
    elif kind=='base10':base(data,(w-260)/2,h/2-33)
    elif kind in ['pattern','sequence']:
        step=min(42,(w-30)/len(data));xx=(w-step*len(data))/2
        for i,ch in enumerate(data):
            c.setFillColor(PALE if i%2==0 else white);c.setStrokeColor(GREY)
            c.roundRect(xx+i*step+2,h/2-16,step-4,34,5,stroke=1,fill=1)
            txt(ch,xx+(i+.5)*step,h/2-6,18,True,True)
        if kind=='sequence':
            txt('Départ',xx,h/2+37,10)
            c.setStrokeColor(NAVY);c.line(xx,h/2+30,xx+65,h/2+30)
            c.line(xx+65,h/2+30,xx+59,h/2+34);c.line(xx+65,h/2+30,xx+59,h/2+26)
    elif kind in ['numberline','missingline']:
        a,b=data[:2];missing=data[2] if kind=='missingline' else [];xx=22;yy=h/2;step=(w-44)/(b-a)
        c.line(xx,yy,w-15,yy);c.line(w-15,yy,w-21,yy+3);c.line(w-15,yy,w-21,yy-3)
        for i,n in enumerate(range(a,b+1)):
            nx=xx+i*step;c.line(nx,yy-4,nx,yy+4)
            txt('…' if n in missing else n,nx,yy-23,12,False,True)
    elif kind=='jumps':
        a,b,d=data;pts=[(45,a),(45+(w-90)*(b-a)/(d-a),b),(w-45,d)];yy=25
        c.line(35,yy,w-25,yy)
        for xx,n in pts:c.line(xx,yy-5,xx,yy+5);txt(n,xx,yy-21,17,True,True)
        for j in range(2):
            x1,n1=pts[j];x2,n2=pts[j+1];p=c.beginPath();p.moveTo(x1,yy+6);p.curveTo(x1+10,h-10,x2-10,h-10,x2,yy+6);c.drawPath(p)
            txt('+'+str(n2-n1),(x1+x2)/2,h-17,13,True,True)
    elif kind=='sumtree':
        a,b=data;t=a//10*10+b//10*10;u=a%10+b%10
        txt(f'{a} + {b}',w/2,h-18,21,True,True)
        for xx,s in [(w*.28,f'{a//10*10} + {b//10*10} = {t}'),(w*.72,f'{a%10} + {b%10} = {u}')]:
            c.line(w/2,h-24,xx,h/2+15);txt(s,xx,h/2-3,15,False,True)
            c.line(xx,h/2-12,w/2,32)
        txt(f'{t} + {u} = {a+b}',w/2,8,18,True,True)
    elif kind=='exchange':
        total,remove=data
        base(total-10,25,22,6.5)
        dots(10,w-167,h/2+13,21,5)
        for i in range(remove):
            xx=w-167+(i%5)*21;yy=h/2+13-(i//5)*21;c.setStrokeColor(INK);c.line(xx-7,yy-7,xx+7,yy+7)
        txt(f'{total} = {total-10} + 10',w/2,h-14,13,True,True)
    elif kind=='bar':
        total,known,unknown=data;xx=35;yy=h/2-18;bw=w-70;bh=34;cut=bw*known/total
        c.setFillColor(PALE);c.setStrokeColor(NAVY);c.rect(xx,yy,bw,bh,stroke=1,fill=1);c.line(xx+cut,yy,xx+cut,yy+bh)
        txt(known,xx+cut/2,yy+10,16,True,True);txt(unknown,xx+cut+(bw-cut)/2,yy+10,16,True,True)
        c.line(xx,yy+bh+12,xx+bw,yy+bh+12);txt(f'{total} en tout',w/2,yy+bh+20,14,True,True)
    elif kind=='groups':
        n,k=data;cols=min(n,3);rows=(n+cols-1)//cols;bw=min(115,w/cols-15);bh=min(65,h/rows-9)
        for i in range(n):
            xx=(i%cols)*(w/cols)+8;yy=h-(i//cols+1)*(h/rows)+3
            c.setStrokeColor(GREY);c.roundRect(xx,yy,bw,bh,7,stroke=1,fill=0)
            step=16;dots(k,xx+15,yy+bh-16,step,4)
    elif kind=='fraction':
        parts,colored=data;xx=35;yy=h/2-20;bw=w-70
        for i in range(parts):
            c.setFillColor(PALE if i<colored else white);c.setStrokeColor(NAVY);c.rect(xx+i*bw/parts,yy,bw/parts,40,stroke=1,fill=1)
    elif kind in ['story','storyblank']:
        a,b,d=data;vals=[str(a),str(a+b),str(a+b+d)] if kind=='story' else [str(a),'…','…'];xs=[55,w/2,w-55]
        for xx,s in zip(xs,vals):
            c.setFillColor(PALE);c.setStrokeColor(NAVY);c.roundRect(xx-28,h/2-20,56,40,7,stroke=1,fill=1);txt(s,xx,h/2-7,19,True,True)
        for j,v in enumerate([b,d]):
            xx1=xs[j]+31;xx2=xs[j+1]-31;c.line(xx1,h/2,xx2,h/2);c.line(xx2,h/2,xx2-6,h/2+4);c.line(xx2,h/2,xx2-6,h/2-4);txt(f'{v:+}',(xx1+xx2)/2,h/2+13,14,True,True)
    elif kind=='money':
        sizes=[58 if n>=5 else 37 for n in data];total=sum(sizes)+14*(len(data)-1);xx=(w-total)/2
        for n,sz in zip(data,sizes):
            c.setFillColor(PALE);c.setStrokeColor(NAVY)
            if n>=5:c.roundRect(xx,h/2-19,sz,38,4,stroke=1,fill=1)
            else:c.circle(xx+sz/2,h/2,sz/2,stroke=1,fill=1)
            txt(f'{n} €',xx+sz/2,h/2-5,15,True,True);xx+=sz+14
    elif kind=='ruler':
        start,end=data;step=10*mm;xx=(w-10*step)/2;yy=23
        c.setFillColor(PALE);c.setStrokeColor(GREY);c.rect(xx,yy,10*step,30,stroke=1,fill=1)
        for n in range(11):c.setStrokeColor(NAVY);c.line(xx+n*step,yy+30,xx+n*step,yy+19);txt(n,xx+n*step,yy+5,10,False,True)
        c.setStrokeColor(INK);c.setLineWidth(2.5);c.line(xx+start*step,yy+42,xx+end*step,yy+42)
        for n in [start,end]:c.line(xx+n*step,yy+37,xx+n*step,yy+47)
    elif kind=='lengths':
        for i,n in enumerate(data):
            yy=h-20-i*24;txt(chr(65+i),10,yy-4,12,True);c.setFillColor(PALE);c.setStrokeColor(NAVY);c.rect(40,yy-7,n*30,14,stroke=1,fill=1)
    elif kind=='balance':
        mode=data;mid=w/2;left=mid-90;right=mid+90;cy=h*.58;delta=16 if mode=='left' else (-16 if mode=='right' else 0)
        c.setStrokeColor(INK);c.setLineWidth(2);c.line(mid,12,mid,cy);c.line(mid-35,12,mid+35,12);c.line(left,cy-delta,right,cy+delta)
        for xx,yy,label in [(left,cy-delta,'A'),(right,cy+delta,'B')]:
            c.line(xx,yy,xx,yy-21);c.line(xx-30,yy-21,xx+30,yy-21);c.setFillColor(PALE);c.rect(xx-13,yy-19,26,25,stroke=1,fill=1);txt(label,xx,yy-11,12,True,True)
    elif kind in ['clocks','blankclocks']:
        hours=data if kind=='clocks' else [None]*data;r=min(43,h/2-5);step=min(145,w/len(hours))
        for j,hour in enumerate(hours):
            cx=w/2+(j-(len(hours)-1)/2)*step;cy=h/2;c.setFillColor(white);c.setStrokeColor(NAVY);c.circle(cx,cy,r,stroke=1,fill=1)
            for n in range(1,13):
                a=pi/2-n*pi/6;txt(n,cx+cos(a)*r*.77,cy+sin(a)*r*.77-3,10,False,True)
            if hour is not None:
                c.setStrokeColor(INK);c.setLineWidth(2);c.line(cx,cy,cx,cy+r*.58)
                a=pi/2-hour*pi/6;c.setLineWidth(3.8);c.line(cx,cy,cx+cos(a)*r*.41,cy+sin(a)*r*.41)
                c.setFillColor(INK);c.circle(cx,cy,2.5,stroke=0,fill=1)
    elif kind=='shapes':
        xs=[52,153,255,360];cy=h/2
        c.setFillColor(PALE);c.setStrokeColor(NAVY)
        c.rect(xs[0]-23,cy-23,46,46,stroke=1,fill=1)
        p=c.beginPath();p.moveTo(xs[1]-25,cy-22);p.lineTo(xs[1]+25,cy-22);p.lineTo(xs[1]+(25 if data=='cutout' else 4),cy+25);p.close();c.drawPath(p,stroke=1,fill=1)
        c.circle(xs[2],cy,25,stroke=1,fill=1);c.rect(xs[3]-34,cy-19,68,38,stroke=1,fill=1)
        for i,xx in enumerate(xs):txt(chr(65+i) if data=='quiz' else ['carré','triangle','disque','rectangle'][i],xx,cy-42,11,True,True)
    elif kind=='points':
        for xx,yy,label in data:
            px=40+xx*45;py=20+yy*23;c.setStrokeColor(NAVY);c.line(px-3,py,px+3,py);c.line(px,py-3,px,py+3);txt(label,px+6,py+5,12,True)
    elif kind in ['gridshape','copygrid','partial','gridblank']:
        step=17;yy=(h-5*step)/2
        if kind=='copygrid':
            for xx in [35,w/2+35]:grid(xx,yy,7,5,step)
            shape,a,b=data;gridshape(shape,a,b,35+step,yy+step,step)
        else:
            xx=(w-10*step)/2;grid(xx,yy,10,5,step)
            if kind!='gridblank':
                shape,a,b=data;gridshape(shape,a,b,xx+step,yy+step,step,kind=='partial')
    elif kind=='solids':
        xs=[37,124,211,298,385];yy=h/2-13
        for i,xx in enumerate(xs):
            c.setStrokeColor(NAVY);c.setFillColor(PALE)
            if i in [0,1]:
                bw=34 if i==0 else 51;bh=34 if i==0 else 25;d=11
                c.rect(xx-bw/2,yy,bw,bh,stroke=1,fill=1)
                p=c.beginPath();p.moveTo(xx-bw/2,yy+bh);p.lineTo(xx-bw/2+d,yy+bh+d);p.lineTo(xx+bw/2+d,yy+bh+d);p.lineTo(xx+bw/2,yy+bh);p.close();c.drawPath(p,stroke=1,fill=1)
                p=c.beginPath();p.moveTo(xx+bw/2,yy);p.lineTo(xx+bw/2+d,yy+d);p.lineTo(xx+bw/2+d,yy+bh+d);p.lineTo(xx+bw/2,yy+bh);p.close();c.drawPath(p,stroke=1,fill=1)
            elif i==2:
                c.circle(xx,yy+19,23,stroke=1,fill=1);c.ellipse(xx-23,yy+11,xx+23,yy+27,stroke=1,fill=0)
            elif i==3:
                c.rect(xx-21,yy,42,39,stroke=1,fill=1);c.ellipse(xx-21,yy-7,xx+21,yy+7,stroke=1,fill=1);c.ellipse(xx-21,yy+32,xx+21,yy+46,stroke=1,fill=1)
            else:
                p=c.beginPath();p.moveTo(xx-23,yy);p.lineTo(xx,yy+47);p.lineTo(xx+23,yy);p.close();c.drawPath(p,stroke=1,fill=1);c.ellipse(xx-23,yy-7,xx+23,yy+7,stroke=1,fill=1)
            txt(chr(65+i),xx,yy-27,12,True,True)
    elif kind=='assembly':
        s=33;xx=w/2-40;yy=14
        for a,b in [(0,0),(1,0),(0,1)]:
            dx=xx+a*s;dy=yy+b*s;c.setFillColor(PALE);c.setStrokeColor(NAVY);c.rect(dx,dy,s,s,stroke=1,fill=1)
        txt('Vue de face du modèle',w/2,h-9,11,False,True)
    elif kind in ['route','routeblank']:
        step=22;xx=w/2-3*step;yy=8;grid(xx,yy,6,4,step)
        px=xx+1.5*step;py=yy+.5*step;dot(px,py,5);txt('Départ',xx-60,py-4,10)
        c.setLineWidth(2);c.line(px,py,px,py+13);c.line(px,py+13,px-4,py+8);c.line(px,py+13,px+4,py+8)
        if kind=='route':
            c.setStrokeColor(GREEN);c.setLineWidth(2.3);c.line(px,py,px,py+2*step);c.line(px,py+2*step,px+step,py+2*step)
    elif kind in ['bars','barblank']:
        blank=kind=='barblank';span=280 if blank else 140;xx=w/2-span/2;yy=22 if blank else 15;rows=12 if blank else 5;step=min(26 if blank else 12,(h-40 if blank else h-24)/rows)
        for n in range(rows+1):
            c.setStrokeColor(GREY);c.setLineWidth(.4);c.line(xx,yy+n*step,xx+span,yy+n*step);txt(n,xx-17,yy+n*step-3,11.2 if blank else 9,False,True)
        for i,label in enumerate(['Chat','Chien']):
            bx=xx+(45 if blank else 20)+i*(125 if blank else 70);bw=60 if blank else 35
            if kind=='bars':c.setFillColor(PALE);c.setStrokeColor(NAVY);c.rect(bx,yy,35,data[i]*step,stroke=1,fill=1)
            else:
                for j in range(rows):c.setStrokeColor(GREY);c.rect(bx,yy+j*step,bw,step,stroke=1,fill=0)
            txt(label,bx+bw/2,yy-(15 if blank else 12),13 if blank else 10,True,True)
    elif kind=='surveytable':
        xx=50;yy=12;cw=150;rh=26
        for j in range(4):c.line(xx,yy+j*rh,xx+2*cw,yy+j*rh)
        for i in range(3):c.line(xx+i*cw,yy,xx+i*cw,yy+3*rh)
        for j,lab in enumerate(['Animal','Chat','Chien']):txt(lab,xx+12,yy+(2-j)*rh+9,13,j==0)
        txt('Nombre de votes',xx+cw+12,yy+2*rh+9,12,True)
    elif kind=='doubletable':
        xx=48;yy=8;cw=100;rh=29
        for j in range(4):c.line(xx,yy+j*rh,xx+3*cw,yy+j*rh)
        for i in range(4):c.line(xx+i*cw,yy,xx+i*cw,yy+3*rh)
        txt('Bleu',xx+cw*1.5,yy+2*rh+10,12,True,True);txt('Hachuré',xx+cw*2.5,yy+2*rh+10,12,True,True)
        txt('Rond',xx+10,yy+rh+9,12);txt('Carré',xx+10,yy+9,12)
    elif kind in ['column','columnblank']:
        xx=w/2;yy=15;rh=23
        nums=data if kind=='column' else [None]*data
        txt('d',xx, h-10,11,False,True);txt('u',xx+32,h-10,11,False,True)
        for j,n in enumerate(nums):
            rowy=h-35-j*rh
            if n is not None:
                txt(n//10,xx,rowy,21,True,True);txt(n%10,xx+32,rowy,21,True,True)
            else:
                c.setStrokeColor(GREY);c.rect(xx-10,rowy-3,20,22);c.rect(xx+22,rowy-3,20,22)
            if j:txt('+',xx-33,rowy,18,True)
        ly=h-40-len(nums)*rh;c.setStrokeColor(INK);c.line(xx-40,ly+14,xx+47,ly+14)
        if kind=='column':
            result=sum(nums);txt(result//10,xx,ly-9,21,True,True);txt(result%10,xx+32,ly-9,21,True,True)
            if sum(n%10 for n in nums)>=10:txt('1',xx-13,h-19,10,True)
    else:raise ValueError(f'Figure inconnue : {kind}')
    c.restoreState()
