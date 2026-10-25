"""Schémas vectoriels propres au CE2, avec les dessins communs de la collection."""
from math import pi,sin,cos
from reportlab.lib.colors import white
from reportlab.lib.units import mm
from dessins_communs import diagram as commun, NAVY,INK,GREEN,PALE,GREY

NEW={'place4','exchanges4','add4','sub4','blank4','shift4','splitproduct','doublechain','mulone','multwo','mulblank','groupsremainder','partwhole','comparetot','mixedgroups','timesbars','choices','choicetree','unitlength','fracjoin','segmentsmm','perirect','peritriangle','masscards','capacity','pricepair','eurocolumn','euroblank','minuteclocks','duration','polyproperties','circleparts','symmetry','symmetrymethod','graphscaled','datatable','graphsurvey'}

def diagram(c,spec,x,y,w,h):
    if not spec:return
    kind,data=spec
    if kind not in NEW:return commun(c,spec,x,y,w,h)
    c.saveState();c.translate(x,y);c.setLineWidth(1);c.setStrokeColor(NAVY)
    def text(s,xx,yy,size=12,bold=False,center=False):
        c.setFillColor(INK);c.setFont('Bold' if bold else 'Text',size)
        (c.drawCentredString if center else c.drawString)(xx,yy,str(s))
    def line(x1,y1,x2,y2,color=NAVY,width=1):
        c.setStrokeColor(color);c.setLineWidth(width);c.line(x1,y1,x2,y2)
    def rect(xx,yy,bw,bh,fill=white):
        c.setFillColor(fill);c.setStrokeColor(NAVY);c.setLineWidth(.9);c.rect(xx,yy,bw,bh,stroke=1,fill=1)
    def frac(n,d,xx,yy,size=12):
        text(n,xx,yy+6,size,center=True);line(xx-8,yy+2,xx+8,yy+2);text(d,xx,yy-12,size,center=True)
    def band(n,d,xx,yy,bw,bh=25):
        for j in range(d):rect(xx+j*bw/d,yy,bw/d,bh,PALE if j<n else white)
    def arrow(x1,y1,x2,y2,label=''):
        line(x1,y1,x2,y2);line(x2,y2,x2-5,y2+3);line(x2,y2,x2-5,y2-3)
        if label:text(label,(x1+x2)/2,y1+10,11,True,True)
    def grid(xx,yy,cols,rows,step):
        for i in range(cols+1):line(xx+i*step,yy,xx+i*step,yy+rows*step,GREY,.4)
        for j in range(rows+1):line(xx,yy+j*step,xx+cols*step,yy+j*step,GREY,.4)
    def poly(points,fill=PALE):
        p=c.beginPath()
        for i,pt in enumerate(points):(p.moveTo if i==0 else p.lineTo)(*pt)
        p.close();c.setFillColor(fill);c.setStrokeColor(NAVY);c.setLineWidth(1.4);c.drawPath(p,stroke=1,fill=1)
    if kind in ['place4','exchanges4','shift4']:
        cw=min(100,(w-40)/4);xx=(w-4*cw)/2;rh=24 if kind=='shift4' and h<125 else 30
        if kind=='place4':rows=[data];yy=(h-2*rh)/2
        elif kind=='exchanges4':rows=[[2,14,3,17],[3,4,4,7]];yy=15
        else:
            a,m=data;rows=[[int(q) for q in f'{a:04d}'],[int(q) for q in f'{a*m:04d}']];yy=11
            text(f'{a} × {m} = {a*m:,}'.replace(',',' '),w/2,h-12,14,True,True)
        for i,lab in enumerate(['milliers','centaines','dizaines','unités']):
            rect(xx+i*cw,yy+len(rows)*rh,cw,rh,PALE);text(lab,xx+(i+.5)*cw,yy+len(rows)*rh+10,11,True,True)
        for r,vals in enumerate(rows):
            for j,v in enumerate(vals):rect(xx+j*cw,yy+(len(rows)-1-r)*rh,cw,rh);text(v,xx+(j+.5)*cw,yy+(len(rows)-1-r)*rh+8,18,True,True)
    elif kind in ['add4','sub4','blank4']:
        nums=data if kind!='blank4' else [None]*abs(data);neg=kind=='sub4' or kind=='blank4' and data<0
        xs=[w/2-60,w/2-20,w/2+20,w/2+60];step=23;top=h-44
        for xx,lab in zip(xs,['m','c','d','u']):text(lab,xx,h-10,10,center=True)
        changed=None
        if kind=='sub4':
            orig=[int(q) for q in f'{nums[0]:04d}'];take=[int(q) for q in f'{nums[1]:04d}'];changed=orig[:]
            for j in range(3,0,-1):
                if changed[j]<take[j]:
                    k=j-1
                    while changed[k]==0:k-=1
                    changed[k]-=1
                    for z in range(k+1,j):changed[z]=9
                    changed[j]+=10
            for xx,a,b in zip(xs,orig,changed):
                if a!=b:text(b,xx,h-25,11,True,True)
        elif kind=='add4':
            carry=0
            for j in range(3,0,-1):
                total=sum(int(f'{v:04d}'[j]) for v in nums)+carry;carry=total//10
                if carry:text(carry,xs[j-1],h-25,10,True,True)
        for r,n in enumerate(nums):
            yy=top-r*step
            for j,xx in enumerate(xs):
                if n is None:rect(xx-10,yy-3,20,21)
                else:
                    digs=f'{n:04d}';text(digs[j],xx,yy,18,True,True)
                    if r==0 and changed and int(digs[j])!=changed[j]:line(xx-9,yy-1,xx+9,yy+14,INK,.7)
            if r:text('-' if neg else '+',xs[0]-28,yy,17,True)
        ly=top-len(nums)*step+8;line(xs[0]-30,ly,xs[-1]+20,ly,INK)
        if kind!='blank4':
            answer=nums[0]-nums[1] if neg else sum(nums)
            for xx,v in zip(xs,f'{answer:04d}'):text(v,xx,ly-25,19,True,True)
    elif kind=='splitproduct':
        a,b=data;first=a//10*10;second=a%10;xx=30;yy=20;bw=w-60;cut=bw*.69;bh=h-48
        rect(xx,yy,cut,bh,PALE);rect(xx+cut,yy,bw-cut,bh)
        for label,lx in [(f'{first} × {b} = {first*b}',xx+cut/2),(f'{second} × {b} = {second*b}',xx+cut+(bw-cut)/2)]:text(label,lx,yy+bh/2-5,13,True,True)
        text(f'{a} × {b}',w/2,h-15,15,True,True)
    elif kind=='doublechain':
        a,n=data;xs=[35+i*(w-70)/n for i in range(n+1)];cy=h/2
        for j,xx in enumerate(xs):rect(xx-26,cy-17,52,34,PALE);text(a*2**j,xx,cy-6,17,True,True)
        for j in range(n):arrow(xs[j]+29,cy,xs[j+1]-29,cy,'× 2')
    elif kind in ['mulone','multwo','mulblank']:
        blank=kind=='mulblank';two=(data==2 if blank else kind=='multwo');a,b=(None,None) if blank else data
        # Fixed four-digit result field; a three-digit factor can produce a four-digit result.
        step=27 if h>160 else 18;fs=17 if h>160 else 14;xs=[w/2-60+i*32 for i in range(4)];top=h-28
        def digits(n,yy,boxes=False):
            s=f'{n:4d}' if n is not None else '    '
            for j,xx in enumerate(xs):
                if boxes:rect(xx-8,yy-2,16,17)
                elif s[j]!=' ':text(s[j],xx,yy,fs,True,True)
        digits(a,top,blank);digits(b,top-step,blank);text('×',xs[0]-24,top-step,16,True)
        ly=top-step-6;line(xs[0]-26,ly,xs[-1]+16,ly,INK)
        if not blank and not two:
            digs=[int(q) for q in f'{a:03d}'];carry=0
            for j in range(2,0,-1):
                total=digs[j]*b+carry;carry=total//10
                if carry:text(carry,xs[j],h-11,9,True,True)
            digits(a*b,ly-step)
        elif two:
            digits(a*(b%10) if a is not None else None,ly-step,blank)
            digits(a*(b//10*10) if a is not None else None,ly-2*step,blank)
            text('+',xs[0]-24,ly-2*step,15,True);line(xs[0]-26,ly-2*step-6,xs[-1]+16,ly-2*step-6,INK)
            digits(a*b if a is not None else None,ly-3*step-8,blank)
            if not blank and h>180:
                text(f'× {b%10}',xs[-1]+35,ly-step,12)
                text(f'× {b//10*10}',xs[-1]+35,ly-2*step,12)
    elif kind=='groupsremainder':
        total,group=data;count,rest=divmod(total,group);cw=48;xx=(w-(count+1)*cw)/2;yy=h/2-24
        for j in range(count):
            rect(xx+j*cw,yy,40,50,PALE)
            for q in range(group):c.setFillColor(NAVY);c.circle(xx+j*cw+12+(q%2)*16,yy+10+(q//2)*15,3,stroke=0,fill=1)
        for q in range(rest):c.setFillColor(GREEN);c.circle(xx+count*cw+12,yy+10+q*15,4,stroke=0,fill=1)
        text('reste',xx+count*cw+12,yy-18,10,center=True)
    elif kind in ['partwhole','comparetot','timesbars']:
        xx=65;bw=w-110;bh=25
        if kind=='partwhole':
            total,part=data;yy=h/2-15;cut=bw*.42;rect(xx,yy,cut,bh,PALE);rect(xx+cut,yy,bw-cut,bh)
            text(part,xx+cut/2,yy+7,15,True,True);text('?',xx+cut+(bw-cut)/2,yy+7,15,True,True);text(f'{total} en tout',w/2,yy+42,14,True,True)
        elif kind=='comparetot':
            a,gap=data;yy=18
            rect(xx,yy+45,bw*.68,bh,PALE);text('Lina',4,yy+52,11);text(a,xx+bw*.34,yy+52,14,True,True)
            rect(xx,yy,bw*.68,bh,PALE);rect(xx+bw*.68,yy,bw*.32,bh);text('Noé',4,yy+7,11);text(a,xx+bw*.34,yy+7,14,True,True);text(f'+ {gap}',xx+bw*.84,yy+7,12,True,True)
            text('Ensemble : ?',w/2,h-14,14,True,True)
        else:
            a,n=data;yy=20;seg=bw/n;rect(xx,yy+45,seg,bh,PALE);text(a,xx+seg/2,yy+52,13,True,True)
            for i in range(n):rect(xx+i*seg,yy,seg,bh,PALE);text(a,xx+(i+.5)*seg,yy+7,13,True,True)
            text(f'{n} fois autant',w/2,h-14,14,True,True)
    elif kind=='mixedgroups':
        for side,(n,each) in enumerate([(3,8),(2,6)]):
            xx=25+side*w/2;yy=h/2-20
            for j in range(n):rect(xx+j*55,yy,45,40,PALE);text(each,xx+j*55+22.5,yy+12,16,True,True)
    elif kind=='choices':
        rows=[['','Haut 1','Haut 2','Haut 3'],['Bas A','A1','A2','A3'],['Bas B','B1','B2','B3']];cw=(w-50)/4;rh=28;xx=25;yy=(h-3*rh)/2
        for r,row in enumerate(rows):
            for j,lab in enumerate(row):rect(xx+j*cw,yy+(2-r)*rh,cw,rh,PALE if r==0 or j==0 else white);text(lab,xx+(j+.5)*cw,yy+(2-r)*rh+9,11,r==0 or j==0,True)
    elif kind=='choicetree':
        # Two choices, then three, then two. Each of the twelve leaves is one complete selection.
        xs=[24,w*.26,w*.55,w-40];leafgap=min(23,(h-45)/12);base=(h-11*leafgap)/2
        leafys=[base+i*leafgap for i in range(12)]
        text('Départ',xs[0],h/2+7,11,center=True)
        for a in range(2):
            ay=sum(leafys[a*6:a*6+6])/6;line(xs[0]+14,h/2,xs[1]-25,ay,GREY);text(f'Entrée {a+1}',xs[1],ay-3,11,True,True)
            for b in range(3):
                pos=a*6+b*2;by=(leafys[pos]+leafys[pos+1])/2;line(xs[1]+25,ay,xs[2]-22,by,GREY);text(f'Plat {b+1}',xs[2],by-3,11,center=True)
                for q in range(2):
                    cy=leafys[pos+q];line(xs[2]+22,by,xs[3]-24,cy,GREY);text(f'Dessert {q+1}',xs[3],cy-3,10,center=True)
    elif kind=='unitlength':
        denom,whole,num=data;unit=40*mm;xx=(w-3*unit)/2;yy=34
        line(xx,yy,xx+3*unit,yy)
        for j in range(3*denom+1):
            tx=xx+j*unit/denom;line(tx,yy-4,tx,yy+(9 if j%denom==0 else 4))
            if j%denom==0:text(f'{j//denom} u' if j else '0',tx,yy-19,11,center=True)
        end=xx+(whole+num/denom)*unit;line(xx,yy+34,end,yy+34,GREEN,3)
        for tx in [xx,end]:line(tx,yy+29,tx,yy+39,GREEN)
        text('Une unité u',xx+unit/2,h-12,11,True,True)
        line(xx,h-22,xx+unit,h-22,GREY)
    elif kind=='fracjoin':
        a,b,op=data;bw=(w-110)/2;yy=h/2-4
        band(*a,25,yy,bw,26);band(*b,w/2+30,yy,bw,26);frac(*a,25+bw/2,yy-21);frac(*b,w/2+30+bw/2,yy-21);text(op,w/2,yy+5,20,True,True)
    elif kind=='segmentsmm':
        xx=75
        for i,n in enumerate(data):
            yy=h-30-i*45;text(chr(65+i),xx-25,yy-4,12,True);line(xx,yy,xx+n*mm,yy,INK,1.6)
            for tx in [xx,xx+n*mm]:line(tx,yy-4,tx,yy+4)
    elif kind=='perirect':
        a,b=data;bw=a*10*mm;bh=b*10*mm;xx=(w-bw)/2;yy=(h-bh)/2
        rect(xx,yy,bw,bh);text(f'{a} cm',w/2,yy+bh+9,12,True,True);text(f'{b} cm',xx+bw+10,yy+bh/2-4,12,True)
    elif kind=='peritriangle':
        xx=w/2-50;yy=15;poly([(xx,yy),(xx+4*mm*10,yy),(xx,yy+3*mm*10)],white)
    elif kind=='masscards':
        cw=(w-60)/3
        for i,lab in enumerate(data):rect(25+i*cw,h/2-22,cw-12,44,PALE);text(lab,25+i*cw+(cw-12)/2,h/2-6,17,True,True)
    elif kind=='capacity':
        ch=h-34;bw=70
        for i,v in enumerate(data):
            xx=w*(.30+.40*i)-bw/2;yy=15
            c.setFillColor(PALE);c.rect(xx,yy,bw,ch*v/100,stroke=0,fill=1)
            line(xx,yy,xx+bw,yy);line(xx,yy,xx,yy+ch);line(xx+bw,yy,xx+bw,yy+ch)
            for n in range(0,101,20):line(xx+bw-10,yy+ch*n/100,xx+bw,yy+ch*n/100);text(n,xx+bw+7,yy+ch*n/100-3,9)
            text(chr(65+i),xx+bw/2,yy-12,11,True,True);text('cL',xx+bw/2,yy+ch+9,10,True,True)
    elif kind=='pricepair':
        for i,(price,cents) in enumerate([('2,05 €','205 centimes'),('2,50 €','250 centimes')]):
            xx=25+i*w/2;bw=w/2-45;rect(xx,h/2-31,bw,63,PALE);text(price,xx+bw/2,h/2+6,20,True,True);text(cents,xx+bw/2,h/2-18,12,center=True)
    elif kind in ['eurocolumn','euroblank']:
        blank=kind=='euroblank';a,b,op=(None,None,data) if blank else data
        xx=w/2-70;cell=26;top=h-22;rows=[a,b]
        if not blank:
            from decimal import Decimal
            va=Decimal(a.replace(',','.'));vb=Decimal(b.replace(',','.'));answer=va+vb if op=='+' else va-vb
        for r,s in enumerate(rows):
            yy=top-r*25
            chars=f'{s:>6}' if s else '   ,  '
            for j,ch in enumerate(chars):
                if blank and ch!=',':rect(xx+j*cell-8,yy-3,17,20)
                else:text(ch,xx+j*cell,yy,18,True,True)
            if r:text(op,xx-28,yy,18,True)
        ly=top-33;line(xx-32,ly,xx+5*cell+18,ly,INK)
        if not blank:
            ans=f'{answer:.2f}'.replace('.',',')
            for j,ch in enumerate(f'{ans:>6}'):text(ch,xx+j*cell,ly-27,19,True,True)
    elif kind=='minuteclocks':
        radius=min(47,h/2-7);cy=h/2;step=min(180,w/len(data))
        for i,(hour,minute) in enumerate(data):
            cx=(w-step*len(data))/2+(i+.5)*step;c.setStrokeColor(NAVY);c.setLineWidth(.9);c.circle(cx,cy,radius,stroke=1,fill=0)
            for j in range(60):
                angle=pi/2-j*pi/30;rr=radius-(6 if j%5==0 else 3);line(cx+rr*cos(angle),cy+rr*sin(angle),cx+radius*cos(angle),cy+radius*sin(angle),NAVY,.6)
            for j in range(1,13):
                angle=pi/2-j*pi/6;text(j,cx+(radius-13)*cos(angle),cy+(radius-13)*sin(angle)-3,9,center=True)
            if hour is not None:
                for value,length,lw in [((hour%12)+minute/60,radius*.50,3.2),(minute/5,radius*.78,1.3)]:
                    angle=pi/2-value*pi/6;line(cx,cy,cx+length*cos(angle),cy+length*sin(angle),INK,lw)
            c.setFillColor(INK);c.circle(cx,cy,1.6,stroke=0,fill=1)
    elif kind=='duration':
        start,end=data;middle=(start//60+1)*60;last=end//60*60;values=[start,middle,last,end];xs=[35,w*.34,w*.69,w-35];yy=38
        for i,(v,tx) in enumerate(zip(values,xs)):
            line(tx,yy-5,tx,yy+5);text(f'{v//60} h {v%60:02}',tx,yy-24,12,True,True)
            if i:arrow(xs[i-1]+3,yy,tx-3,yy,f'{v-values[i-1]} min')
    elif kind=='polyproperties':
        cy=h/2+7;xs=[w*.18,w*.50,w*.81]
        # A is an actual rotated square; C is an oblique rhombus without right angles.
        poly([(xs[0],cy+29),(xs[0]+29,cy),(xs[0],cy-29),(xs[0]-29,cy)])
        rect(xs[1]-42,cy-23,84,46)
        poly([(xs[2]-45,cy),(xs[2],cy+24),(xs[2]+45,cy),(xs[2],cy-24)])
        for i,tx in enumerate(xs):text(chr(65+i),tx,cy-48,12,True,True)
    elif kind=='circleparts':
        radius=42;cx=w/2;cy=h/2;c.setStrokeColor(NAVY);c.circle(cx,cy,radius,stroke=1,fill=0)
        line(cx-radius,cy,cx+radius,cy);line(cx,cy,cx,cy+radius,GREEN,1.5)
        for tx,ty,lab in [(cx-radius,cy,'A'),(cx+radius,cy,'B'),(cx,cy,'M')]:
            line(tx-2,ty,tx+2,ty);line(tx,ty-2,tx,ty+2);text(lab,tx+4,ty-16,11,True)
        text('rayon',cx+7,cy+23,11);text('diamètre',cx,cy-34,11,center=True)
    elif kind in ['symmetry','symmetrymethod']:
        orient,blank=data if kind=='symmetry' else ['v',False];cols,rows=10,6
        step=min(22 if kind=='symmetrymethod' else 16,(h-12)/rows,(w-40)/cols);xx=(w-cols*step)/2;yy=(h-rows*step)/2
        grid(xx,yy,cols,rows,step)
        if orient=='v':points=[(5,1),(3,1),(2,3),(3,5),(5,5)];axis=[(5,0),(5,6)];mirror=lambda a,b:(10-a,b)
        else:points=[(2,3),(2,5),(4,5),(5,4),(7,4),(7,3)];axis=[(0,3),(10,3)];mirror=lambda a,b:(a,6-b)
        c.setDash(4,3);line(xx+axis[0][0]*step,yy+axis[0][1]*step,xx+axis[1][0]*step,yy+axis[1][1]*step,GREEN,1.3);c.setDash()
        def stroke(pts,color=NAVY):
            for a,b in zip(pts,pts[1:]):line(xx+a[0]*step,yy+a[1]*step,xx+b[0]*step,yy+b[1]*step,color,1.8)
        stroke(points)
        if not blank:stroke([mirror(a,b) for a,b in points],GREEN)
    elif kind in ['graphscaled','graphsurvey']:
        if kind=='graphscaled':labels,values,scale=data;maxval=max(values);n=(maxval+scale-1)//scale
        else:labels=['0','1','2','3'];values=[0,0,0,0];scale=1;n=6
        xx=60;yy=29;span=w-95;step=(h-54)/n;col=span/len(labels)
        for j in range(n+1):
            line(xx,yy+j*step,xx+span,yy+j*step,GREY,.45);text(j*scale,xx-14,yy+j*step-3,10,center=True)
        for i,(lab,v) in enumerate(zip(labels,values)):
            bx=xx+(i+.22)*col;bw=col*.56
            if kind=='graphscaled':rect(bx,yy,bw,v/scale*step,PALE)
            else:
                for j in range(n):line(bx,yy+j*step,bx,yy+(j+1)*step,GREY,.4);line(bx+bw,yy+j*step,bx+bw,yy+(j+1)*step,GREY,.4)
            text(lab,xx+(i+.5)*col,yy-17,11,True,True)
        if kind=='graphsurvey':text('Titre : ........................................',w/2,h-10,12,center=True)
    elif kind=='datatable':
        rows=[['Atelier','Lundi','Mardi'],['Dessin','12','18'],['Théâtre','8','7']];cw=(w-60)/3;rh=28;xx=30;yy=(h-3*rh)/2
        for r,row in enumerate(rows):
            for j,v in enumerate(row):rect(xx+j*cw,yy+(2-r)*rh,cw,rh,PALE if r==0 or j==0 else white);text(v,xx+(j+.5)*cw,yy+(2-r)*rh+9,12,r==0 or j==0,True)
    c.restoreState()
