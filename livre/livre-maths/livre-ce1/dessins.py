"""Schémas vectoriels CE1 ; les figures communes sont incluses dans le dossier."""
from math import pi,sin,cos
from reportlab.lib.colors import HexColor,white
from reportlab.lib.units import mm
from dessins_base import diagram as base_diagram
NAVY=HexColor('#1B3C8E');INK=HexColor('#1C2130');GREEN=HexColor('#3B8544');PALE=HexColor('#E0ECE3');GREY=HexColor('#A7B1C0')
NEW={'hundreds','placevalue','scaledline','markedline','compensation','backjumps','addition3','column3blank','subtraction3','array','productsplit','times10','halftree','comparebars','sharebar','fracbar','plainband','fraccompare','fracoperation','massweights','centcoins','timeclocks','timeline','angles','geoforms','circle','obliquegrid','solids6','databars','survey3','surveygraph','doubledata'}
def diagram(c,spec,x,y,w,h):
    if not spec:return
    kind,data=spec
    if kind not in NEW:return base_diagram(c,spec,x,y,w,h)
    c.saveState();c.translate(x,y);c.setLineWidth(1);c.setStrokeColor(NAVY);c.setFillColor(INK)
    def text(s,xx,yy,size=12,bold=False,center=False):
        c.setFont('Bold' if bold else 'Text',size);c.setFillColor(INK)
        (c.drawCentredString if center else c.drawString)(xx,yy,str(s))
    def line(x1,y1,x2,y2,color=NAVY,width=1):
        c.setStrokeColor(color);c.setLineWidth(width);c.line(x1,y1,x2,y2)
    def cross(xx,yy,label=''):
        line(xx-3,yy,xx+3,yy);line(xx,yy-3,xx,yy+3)
        if label:text(label,xx+6,yy+5,11,True)
    def frac(n,d,xx,yy,size=14):
        text(n,xx,yy+7,size,False,True);line(xx-8,yy+3,xx+8,yy+3);text(d,xx,yy-13,size,False,True)
    def fractionbar(n,d,xx,yy,bw,bh=26):
        for i in range(d):
            c.setFillColor(PALE if i<n else white);c.setStrokeColor(NAVY);c.setLineWidth(1)
            c.rect(xx+i*bw/d,yy,bw/d,bh,stroke=1,fill=1)
    def grid(xx,yy,cols,rows,step=16):
        for i in range(cols+1):line(xx+i*step,yy,xx+i*step,yy+rows*step,GREY,.45)
        for j in range(rows+1):line(xx,yy+j*step,xx+cols*step,yy+j*step,GREY,.45)
    if kind=='hundreds':
        cents,t=divmod(data,100);tens,ones=divmod(t,10);xx=18;yy=h/2-25
        for k in range(cents):
            bx=xx+k*56;c.setFillColor(PALE);c.setStrokeColor(GREEN);c.rect(bx,yy,50,50,stroke=1,fill=1)
            for j in range(1,10):line(bx+j*5,yy,bx+j*5,yy+50,GREEN,.35);line(bx,yy+j*5,bx+50,yy+j*5,GREEN,.35)
        bx=xx+max(cents,1)*56+22
        for k in range(tens):
            c.setFillColor(PALE);c.setStrokeColor(GREEN);c.rect(bx+k*11,yy,5,50,stroke=1,fill=1)
            for j in range(1,10):line(bx+k*11,yy+j*5,bx+k*11+5,yy+j*5,GREEN,.45)
        ux=bx+max(tens,1)*11+24
        for k in range(ones):c.setFillColor(white);c.setStrokeColor(NAVY);c.rect(ux+(k%5)*10,yy+(k//5)*10,5,5,stroke=1,fill=1)
    elif kind in ['placevalue','times10']:
        vals=data if kind=='placevalue' else [data//10,data%10,0]
        if kind=='times10':text(f'{data} × 10 = {data*10}',w/2,h-13,17,True,True)
        xx=w/2-120;yy=10;cw=80;rh=32
        for j in range(3):line(xx,yy+j*rh,xx+3*cw,yy+j*rh,GREY)
        for i in range(4):line(xx+i*cw,yy,xx+i*cw,yy+2*rh,GREY)
        for i,lab in enumerate(['centaines','dizaines','unités']):text(lab,xx+(i+.5)*cw,yy+rh+12,11,True,True);text(vals[i],xx+(i+.5)*cw,yy+9,20,True,True)
    elif kind in ['scaledline','markedline']:
        a,b,step,extra=data;xx=25;yy=h/2-2;length=w-50;count=(b-a)//step
        line(xx,yy,w-17,yy);line(w-17,yy,w-23,yy+3);line(w-17,yy,w-23,yy-3)
        for i,n in enumerate(range(a,b+1,step)):
            nx=xx+i*length/count;line(nx,yy-4,nx,yy+4)
            hidden=n==extra if kind=='markedline' else n in extra
            text('…' if hidden else n,nx,yy-22,11,False,True)
            if kind=='markedline' and n==extra:
                c.setFillColor(GREEN);c.circle(nx,yy,4,stroke=0,fill=1);text('?',nx,yy+17,15,True,True)
    elif kind=='compensation':
        a,b,d=data;values=[a,a+b,a+b+d];xs=[50,w/2,w-50];yy=h/2
        for xx,v in zip(xs,values):
            c.setFillColor(PALE);c.setStrokeColor(NAVY);c.roundRect(xx-31,yy-18,62,36,5,stroke=1,fill=1);text(v,xx,yy-6,17,True,True)
        for i,v in enumerate([b,d]):
            x1=xs[i]+35;x2=xs[i+1]-35;line(x1,yy,x2,yy);line(x2,yy,x2-5,yy+4);line(x2,yy,x2-5,yy-4);text(f'{v:+}',(x1+x2)/2,yy+13,13,True,True)
    elif kind=='backjumps':
        a,b,d=data;yy=26;coords=[w-35,35+(w-70)*(b-d)/(a-d),35];vals=[a,b,d]
        line(22,yy,w-22,yy)
        for xx,n in zip(coords,vals):line(xx,yy-4,xx,yy+4);text(n,xx,yy-22,16,True,True)
        for i in range(2):
            x1,x2=coords[i:i+2];p=c.beginPath();p.moveTo(x1,yy+5);p.curveTo(x1-5,h-15,x2+5,h-15,x2,yy+5);c.setStrokeColor(NAVY);c.drawPath(p);text(str(vals[i+1]-vals[i]),(x1+x2)/2,h-17,13,True,True)
    elif kind in ['addition3','subtraction3','column3blank']:
        nums=data if kind!='column3blank' else [None]*abs(data);negative=kind=='subtraction3' or kind=='column3blank' and data<0
        xs=[w/2-36,w/2,w/2+36]
        for i,label in enumerate(['c','d','u']):text(label,xs[i],h-10,10,False,True)
        if kind=='subtraction3':
            a,b=nums;orig=[a//100,a//10%10,a%10];take=[b//100,b//10%10,b%10];new=orig[:]
            if new[2]<take[2]:
                if new[1]==0:new[0]-=1;new[1]+=10
                new[1]-=1;new[2]+=10
            if new[1]<take[1]:new[0]-=1;new[1]+=10
            for i,v in enumerate(new):
                if v!=orig[i]:text(v,xs[i],h-25,11,True,True)
        elif kind=='addition3':
            carry=0
            for i in [2,1]:
                total=sum((v//(10**(2-i)))%10 for v in nums)+carry;carry=total//10
                if carry:text(carry,xs[i-1],h-25,10,True,True)
        for j,n in enumerate(nums):
            yy=h-47-j*24
            for i,xx in enumerate(xs):
                if n is None:c.setStrokeColor(GREY);c.rect(xx-10,yy-3,20,22)
                else:
                    digs=[n//100,n//10%10,n%10];text(digs[i],xx,yy,19,True,True)
                    if kind=='subtraction3' and j==0 and new[i]!=orig[i]:line(xx-9,yy-1,xx+9,yy+14,INK,.8)
            if j:text('-' if negative else '+',xs[0]-30,yy,18,True)
        ly=h-52-len(nums)*24;line(xs[0]-34,ly+15,xs[-1]+17,ly+15,INK)
        if kind!='column3blank':
            result=nums[0]-nums[1] if negative else sum(nums)
            for xx,v in zip(xs,[result//100,result//10%10,result%10]):text(v,xx,ly-7,20,True,True)
    elif kind=='array':
        rows,cols=data;step=min(17,(h-20)/max(rows,1),(w-50)/max(cols,1));xx=(w-(cols-1)*step)/2;yy=(h+(rows-1)*step)/2
        for r in range(rows):
            for q in range(cols):c.setFillColor(PALE);c.setStrokeColor(NAVY);c.circle(xx+q*step,yy-r*step,min(4.5,step*.28),stroke=1,fill=1)
    elif kind=='productsplit':
        a,b=data;xx=35;yy=18;bw=w-70;bh=min(65,h-45);cut=bw*10/a
        c.setFillColor(PALE);c.setStrokeColor(NAVY);c.rect(xx,yy,bw,bh,stroke=1,fill=1);line(xx+cut,yy,xx+cut,yy+bh)
        text(f'10 × {b} = {10*b}',xx+cut/2,yy+bh/2-5,14,True,True);text(f'{a-10} × {b} = {(a-10)*b}',xx+cut+(bw-cut)/2,yy+bh/2-5,13,True,True);text(f'{a} × {b}',w/2,yy+bh+11,15,True,True)
    elif kind=='halftree':
        total,a,b=data;text(f'{total} = {a} + {b}',w/2,h-17,18,True,True)
        text(f'moitié de {a} : {a//2}',w*.27,h/2,13,False,True);text(f'moitié de {b} : {b//2}',w*.73,h/2,13,False,True)
        for xx in [w*.27,w*.73]:line(w/2,h-24,xx,h/2+16);line(xx,h/2-8,w/2,31)
        text(f'{a//2} + {b//2} = {total//2}',w/2,8,17,True,True)
    elif kind=='comparebars':
        small,gap=data;total=small+gap;xx=70;bw=w-105;yy=24;bh=24
        for by,length in [(yy,bw*small/total),(yy+44,bw)]:c.setFillColor(PALE);c.setStrokeColor(NAVY);c.rect(xx,by,length,bh,stroke=1,fill=1)
        text('petite',8,yy+7,11);text('grande',8,yy+51,11);text(small,xx+bw*small/total/2,yy+7,13,True,True)
        cut=xx+bw*small/total;line(cut,yy+44,cut,yy+44+bh);text(f'+ {gap}',cut+(xx+bw-cut)/2,yy+51,12,True,True)
    elif kind=='sharebar':
        total,parts=data;xx=30;yy=h/2-15;bw=w-60
        for i in range(parts):c.setFillColor(white);c.setStrokeColor(NAVY);c.rect(xx+i*bw/parts,yy,bw/parts,30,stroke=1,fill=1);text('?',xx+(i+.5)*bw/parts,yy+8,17,True,True)
        text(f'{total} en tout',w/2,yy+44,15,True,True)
    elif kind=='plainband':fractionbar(0,1,30,h/2-15,w-60,30)
    elif kind=='fracbar':
        n,d,label=data;yy=h/2-8 if label else h/2-15;fractionbar(n,d,30,yy,w-60,30)
        if label:frac(n,d,w/2,yy-22,14)
    elif kind=='fraccompare':
        for i,(n,d) in enumerate(data):
            yy=h-38-i*53;fractionbar(n,d,53,yy,w-100,26);frac(n,d,25,yy+7,12)
    elif kind=='fracoperation':
        a,b,d,op=data;yy=h/2-15;bw=(w-100)/2;fractionbar(a,d,25,yy,bw,30);fractionbar(b,d,w/2+25,yy,bw,30);text(op,w/2,yy+7,21,True,True)
        frac(a,d,25+bw/2,yy-22,12);frac(b,d,w/2+25+bw/2,yy-22,12)
    elif kind=='massweights':
        step=98;xx=(w-step*len(data))/2
        for i,v in enumerate(data):
            px=xx+i*step;c.setFillColor(PALE);c.setStrokeColor(NAVY);c.roundRect(px+8,h/2-22,82,44,5,stroke=1,fill=1);text(f'{v} g',px+49,h/2-6,15,True,True)
    elif kind=='centcoins':
        step=80;xx=(w-step*len(data))/2
        for i,v in enumerate(data):
            px=xx+(i+.5)*step;c.setFillColor(PALE);c.setStrokeColor(NAVY);c.circle(px,h/2,28,stroke=1,fill=1);text(f'{v//100} €' if v>=100 else f'{v} c',px,h/2-5,14,True,True)
    elif kind=='timeclocks':
        r=min(43,h/2-4);step=min(142,w/len(data));cy=h/2
        for i,(hour,minute) in enumerate(data):
            cx=w/2+(i-(len(data)-1)/2)*step;c.setFillColor(white);c.setStrokeColor(NAVY);c.setLineWidth(1);c.circle(cx,cy,r,stroke=1,fill=1)
            for n in range(1,13):
                a=pi/2-n*pi/6;text(n,cx+cos(a)*r*.78,cy+sin(a)*r*.78-3,9.5,False,True)
            am=pi/2-minute*2*pi/60;ah=pi/2-(hour%12+minute/60)*pi/6
            line(cx,cy,cx+cos(am)*r*.63,cy+sin(am)*r*.63,INK,1.8);line(cx,cy,cx+cos(ah)*r*.41,cy+sin(ah)*r*.41,INK,3.6)
            c.setFillColor(INK);c.circle(cx,cy,2,stroke=0,fill=1)
    elif kind=='timeline':
        mins=[a*60+b for a,b in data];xx=[35+(w-70)*(m-mins[0])/(mins[-1]-mins[0]) for m in mins];yy=29
        line(25,yy,w-20,yy)
        for px,(hr,mn) in zip(xx,data):line(px,yy-5,px,yy+5);text(f'{hr} h {mn:02}',px,yy-22,13,True,True)
        for i in range(len(xx)-1):text(f'{mins[i+1]-mins[i]} min',(xx[i]+xx[i+1])/2,yy+25,13,True,True)
    elif kind=='angles':
        step=w/len(data)
        for i,a in enumerate(data):
            xx=step*(i+.5)-20;yy=25;length=46;line(xx,yy,xx+length,yy,INK,1.6);line(xx,yy,xx+length*cos(a*pi/180),yy+length*sin(a*pi/180),INK,1.6)
            if a==90:line(xx+10,yy,xx+10,yy+10);line(xx+10,yy+10,xx,yy+10)
            text(chr(65+i),xx+10,yy-18,12,True,True)
    elif kind=='geoforms':
        xs=[75,225,365];cy=h/2
        c.setFillColor(PALE);c.setStrokeColor(NAVY)
        p=c.beginPath();p.moveTo(xs[0],cy+30);p.lineTo(xs[0]+30,cy);p.lineTo(xs[0],cy-30);p.lineTo(xs[0]-30,cy);p.close();c.drawPath(p,stroke=1,fill=1)
        c.rect(xs[1]-40,cy-22,80,44,stroke=1,fill=1)
        p=c.beginPath();p.moveTo(xs[2]-30,cy-23);p.lineTo(xs[2]+30,cy-23);p.lineTo(xs[2]-30,cy+24);p.close();c.drawPath(p,stroke=1,fill=1)
        line(xs[2]-22,cy-23,xs[2]-22,cy-15);line(xs[2]-22,cy-15,xs[2]-30,cy-15)
        for i,xx in enumerate(xs):text(chr(65+i),xx,cy-47,12,True,True)
    elif kind=='circle':
        cx=w/2;cy=h/2;r=min(38,h/2-15);c.setStrokeColor(NAVY);c.circle(cx,cy,r,stroke=1,fill=0);cross(cx,cy,'O');cross(cx+r,cy,'A');line(cx,cy,cx+r,cy,GREY,.8)
    elif kind=='obliquegrid':
        step=16;yy=(h-5*step)/2
        xs=[25,w/2+25] if data else [w/2-4*step]
        for xx in xs:grid(xx,yy,8,5,step)
        xx=xs[0];pts=[(2,1),(4,2),(3,4),(1,3)];p=c.beginPath()
        for i,(a,b) in enumerate(pts):(p.moveTo if i==0 else p.lineTo)(xx+a*step,yy+b*step)
        p.close();c.setStrokeColor(NAVY);c.setLineWidth(1.8);c.drawPath(p)
    elif kind=='solids6':
        c.saveState();c.scale(.82,.82);base_diagram(c,('solids',None),0,0,w,h/.82);c.restoreState()
        xx=w-42;yy=h/2-15
        pts=[(xx-21,yy),(xx+15,yy),(xx+26,yy+9),(xx-9,yy+9)];ap=(xx,yy+46)
        c.setFillColor(PALE);c.setStrokeColor(NAVY)
        for indexes in [(0,1),(1,2)]:
            p=c.beginPath();p.moveTo(*pts[indexes[0]]);p.lineTo(*pts[indexes[1]]);p.lineTo(*ap);p.close();c.drawPath(p,stroke=1,fill=1)
        line(*pts[0],*pts[3],GREY,.6);line(*pts[3],*pts[2],GREY,.6);line(*pts[3],*ap,GREY,.6);text('F',xx,yy-24,12,True,True)
    elif kind=='databars':
        labels,values=data;xx=70;yy=18;bw=w-120;maxn=max(values)+1;step=min(14,(h-35)/maxn);col=bw/len(values)
        for n in range(maxn+1):line(xx,yy+n*step,xx+bw,yy+n*step,GREY,.4);text(n,xx-15,yy+n*step-3,9,False,True)
        for i,(lab,v) in enumerate(zip(labels,values)):
            bx=xx+(i+.25)*col;c.setFillColor(PALE);c.setStrokeColor(NAVY);c.rect(bx,yy,col*.5,v*step,stroke=1,fill=1);text(lab,bx+col*.25,yy-14,10,True,True)
    elif kind=='survey3':
        xx=50;yy=10;cw=150;rh=24
        for j in range(5):line(xx,yy+j*rh,xx+2*cw,yy+j*rh,GREY)
        for i in range(3):line(xx+i*cw,yy,xx+i*cw,yy+4*rh,GREY)
        for i,lab in enumerate(['Choix','Lecture','Dessin','Ballon']):text(lab,xx+10,yy+(3-i)*rh+8,12,i==0)
        text('Nombre de votes',xx+cw+8,yy+3*rh+8,12,True)
    elif kind=='surveygraph':
        xx=65;yy=24;span=w-115;step=min(25,(h-45)/12);col=span/3
        for n in range(13):line(xx,yy+n*step,xx+span,yy+n*step,GREY,.4);text(n,xx-18,yy+n*step-4,11,False,True)
        for i,lab in enumerate(['Lecture','Dessin','Ballon']):
            bx=xx+(i+.25)*col
            for j in range(12):c.setStrokeColor(GREY);c.rect(bx,yy+j*step,col*.5,step)
            text(lab,bx+col*.25,yy-18,12,True,True)
    elif kind=='doubledata':
        rows=[['','Lundi','Mardi'],['À pied','8','10'],['À vélo','5','7']];xx=50;yy=12;cw=102;rh=27
        for j in range(4):line(xx,yy+j*rh,xx+3*cw,yy+j*rh,GREY)
        for i in range(4):line(xx+i*cw,yy,xx+i*cw,yy+3*rh,GREY)
        for r,row in enumerate(rows):
            for q,v in enumerate(row):text(v,xx+(q+.5)*cw,yy+(2-r)*rh+9,12,r==0 or q==0,True)
    c.restoreState()
