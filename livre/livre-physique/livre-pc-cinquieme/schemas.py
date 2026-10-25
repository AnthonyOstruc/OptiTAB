"""Illustrations vectorielles originales. Graduations calculées à partir des valeurs."""
from math import sin,cos,pi
from maquette import mm,white,NAVY,GREEN,INK,MUTED,RULE,PALE,MINT,CREAM,CYAN,TEAL,ORANGE

KINDS={'states','transfer','tilt','syringes','inverted','particles','powder','airtransfer','weighing','meniscus','cylinders','displacement','cubes','massvolume','equipment','balls','measurehero','graphwater','floating'}

def draw(c,spec,x,y,width,height):
    kind,data=spec
    if kind.startswith('pc_'):
        from schemas_complets import draw_full
        return draw_full(c,spec,x,y,width,height)
    if kind not in KINDS:raise ValueError(f'Schéma inconnu : {kind}')
    c.saveState();c.translate(x,y);c.scale(mm,mm);w=width/mm;h=height/mm
    def text(s,xx,yy,size=10.4,color=INK,bold=False,center=False):
        c.setFont('Bold' if bold else 'Body',size/mm);c.setFillColor(color)
        (c.drawCentredString if center else c.drawString)(xx,yy,str(s))
    def line(x1,y1,x2,y2,color=NAVY,lw=.35):
        c.setStrokeColor(color);c.setLineWidth(lw);c.line(x1,y1,x2,y2)
    def rect(xx,yy,ww,hh,fill=None,stroke=NAVY,r=0):
        c.setStrokeColor(stroke);c.setLineWidth(.35)
        if fill:c.setFillColor(fill)
        if r:c.roundRect(xx,yy,ww,hh,r,stroke=1,fill=bool(fill))
        else:c.rect(xx,yy,ww,hh,stroke=1,fill=bool(fill))
    def polygon(pts,fill=CYAN,stroke=NAVY):
        p=c.beginPath()
        for i,pt in enumerate(pts):(p.moveTo if i==0 else p.lineTo)(*pt)
        p.close();c.setFillColor(fill);c.setStrokeColor(stroke);c.setLineWidth(.35);c.drawPath(p,stroke=1,fill=1)
    def arrow(x1,y1,x2,y2,color=GREEN):
        line(x1,y1,x2,y2,color,.45);a=pi+__import__('math').atan2(y2-y1,x2-x1)
        for d in [-.4,.4]:line(x2,y2,x2+2.0*cos(a+d),y2+2.0*sin(a+d),color,.45)
    def leader(pts,color=MUTED):
        for a,b in zip(pts,pts[1:]):line(*a,*b,color,.25)
    def beaker(xx,yy,bw=25,bh=32,level=0,lid=False):
        if level:
            c.setFillColor(CYAN);c.rect(xx+.5,yy+.5,bw-1,level-.5,stroke=0,fill=1)
            line(xx+.5,yy+level,xx+bw-.5,yy+level,TEAL,.4)
        p=c.beginPath();p.moveTo(xx-1.8,yy+bh);p.lineTo(xx,yy+bh-1.5);p.lineTo(xx,yy+1.6);p.curveTo(xx,yy,xx+1,yy,xx+2,yy);p.lineTo(xx+bw-2,yy);p.curveTo(xx+bw,yy,xx+bw,yy+1,xx+bw,yy+2);p.lineTo(xx+bw,yy+bh)
        c.setStrokeColor(NAVY);c.setLineWidth(.45);c.drawPath(p)
        if lid:line(xx-1,yy+bh,xx+bw+1,yy+bh,NAVY,.6)
    def cube(xx,yy,side=10,color=CYAN):
        off=side*.32;polygon([(xx,yy),(xx+side,yy),(xx+side,yy+side),(xx,yy+side)],color)
        polygon([(xx,yy+side),(xx+off,yy+side+off),(xx+side+off,yy+side+off),(xx+side,yy+side)],PALE)
        polygon([(xx+side,yy),(xx+side+off,yy+off),(xx+side+off,yy+side+off),(xx+side,yy+side)],MINT)
    def cylinder(xx,yy,maxv=100,value=40,step=2,bh=52,bw=18,label=None,stone=False,number=True,floating=False):
        bottom=yy+6;scaleh=bh-12;right=xx+bw;level=bottom+scaleh*value/maxv
        if value:
            p=c.beginPath();p.moveTo(xx+.4,bottom);p.lineTo(right-.4,bottom);p.lineTo(right-.4,level+1.2)
            p.curveTo(right-2,level+1.2,xx+bw*.65,level,xx+bw/2,level)
            p.curveTo(xx+bw*.35,level,xx+2,level+1.2,xx+.4,level+1.2);p.close()
            c.setFillColor(CYAN);c.drawPath(p,stroke=0,fill=1)
            p=c.beginPath();p.moveTo(xx+.4,level+1.2);p.curveTo(xx+2,level+1.2,xx+bw*.35,level,xx+bw/2,level);p.curveTo(xx+bw*.65,level,right-2,level+1.2,right-.4,level+1.2)
            c.setStrokeColor(TEAL);c.setLineWidth(.35);c.drawPath(p)
        if stone:
            sy=level-2 if floating else bottom+4
            polygon([(xx+4,sy),(xx+10,sy-1),(xx+bw-3,sy+3),(xx+11,sy+8),(xx+5,sy+6)],PALE)
        line(xx,bottom,xx,bottom+scaleh+3);line(right,bottom,right,bottom+scaleh+3);line(xx,bottom,right,bottom)
        c.setStrokeColor(NAVY);c.setLineWidth(.35);c.ellipse(xx,yy+bh-6.5,right,yy+bh-3.5,stroke=1,fill=0)
        rect(xx+bw/2-2,yy+1.5,4,4.5,fill=PALE);rect(xx-4,yy,bw+8,1.5,fill=PALE)
        major=10 if maxv<=50 else 20 if maxv<=100 else 100
        for v in range(0,maxv+1,step):
            gy=bottom+scaleh*v/maxv;ismajor=v%major==0
            line(right-(4 if ismajor else 2),gy,right,gy,NAVY,.22)
            if ismajor and number:text(v,right+2,gy-1.1,8.8,color=MUTED)
        text('mL',right+2,yy+bh+1,9.5,bold=True)
        if label:text(label,xx+bw/2,yy-6,10.3,bold=True,center=True)
        return xx+bw/2,level
    def balance(cx,yy,value,container=True,fill=True,bw=38):
        rect(cx-bw/2,yy,bw,12,fill=PALE,r=1.8)
        rect(cx-bw/2+5,yy+2.5,bw-10,6.5,fill=NAVY,r=.6)
        text(str(value)+' g',cx,yy+4.1,12.3,color=white,bold=True,center=True)
        rect(cx-15,yy+12,30,2,fill=MINT)
        if container:beaker(cx-10,yy+14,20,23,11 if fill else 0)
    def basin_glass(cx,base,level,top,air=True,paper=False):
        # An inverted vessel: upper end closed, lower end open.
        left=cx-12;right=cx+12
        if air:
            c.setFillColor(white);c.rect(left+.5,level,right-left-1,top-level-.5,stroke=0,fill=1)
            line(left+.5,level,right-.5,level,TEAL,.35)
        line(left,base,left,top);line(left,top,right,top);line(right,top,right,base)
        if paper:rect(cx-7,top-5,14,2,fill=CREAM,stroke=MUTED)

    if kind=='states':
        centers=[w/6,w/2,5*w/6];yy=18;bh=min(34,h-26)
        for i,cx in enumerate(centers):
            beaker(cx-12,yy,24,bh,level=14 if i==1 else 0,lid=i==2)
            if i==0:cube(cx-7,yy+3,11)
            if i==2:text('air',cx,yy+bh/2,11,color=MUTED,center=True)
            text(['SOLIDE','LIQUIDE','GAZ'][i],cx,h-5,10.3,color=GREEN,bold=True,center=True)
            text(['Un glaçon','De l’eau','De l’air'][i],cx,7,11,bold=True,center=True)
    elif kind=='transfer':
        beaker(18,13,23,42,30);beaker(w-69,13,46,30,15)
        arrow(52,32,w-80,32);text('transvaser',w/2,39,10.4,center=True)
        text('Récipient étroit',30,3,10.5,center=True);text('Récipient large',w-46,3,10.5,center=True)
    elif kind=='tilt':
        blank=bool(data)
        for idx,(cx,angle) in enumerate([(w*.28,0),(w*.72,-22*pi/180)]):
            yy=12;factor=min(1,(h-12)/45);pts=[(-13,0),(13,0),(13,37),(-13,37)]
            pts=[(cx+(px*cos(angle)-py*sin(angle))*factor,yy+(px*sin(angle)+py*cos(angle))*factor) for px,py in pts]
            if not blank:
                level=yy+18*factor;clipped=[]
                for a,b in zip(pts,pts[1:]+pts[:1]):
                    if a[1]<=level:clipped.append(a)
                    if (a[1]<level<b[1]) or (b[1]<level<a[1]):
                        t=(level-a[1])/(b[1]-a[1]);clipped.append((a[0]+t*(b[0]-a[0]),level))
                polygon(clipped,CYAN,TEAL)
            for a,b in [(pts[3],pts[0]),(pts[0],pts[1]),(pts[1],pts[2])]:line(*a,*b)
            text(chr(65+idx),cx,3,11,bold=True,center=True)
    elif kind=='syringes':
        vals=data or [50,30];maxv=50;bw=51;bh=11
        for idx,v in enumerate(vals):
            xx=10+idx*w/2;yy=18
            rect(xx,yy,bw,bh)
            c.setFillColor(CYAN);c.rect(xx+.3,yy+.3,bw*v/maxv-.6,bh-.6,stroke=0,fill=1)
            for n in range(0,51,10):
                tx=xx+bw*n/maxv;line(tx,yy+bh-3,tx,yy+bh,NAVY,.2);text(n,tx,yy+bh+3,8.5,center=True)
            piston=xx+bw*v/maxv;line(piston,yy,piston,yy+bh,NAVY,.8);line(piston,yy+bh/2,xx+bw+10,yy+bh/2,NAVY,.65);line(xx+bw+10,yy+2,xx+bw+10,yy+bh-2,NAVY,.65)
            rect(xx-5,yy+3,5,5,fill=PALE);line(xx-6,yy+2,xx-6,yy+9,GREEN,.8)
            text(f'{v} mL',xx+bw/2,7,11,bold=True,center=True)
            text(['Avant','Après une poussée douce'][idx],xx+bw/2,h-5,10.2,color=GREEN,bold=True,center=True)
        text('Embout fermé · seringues sans aiguille',w/2,2.2,9.2,color=MUTED,center=True)
    elif kind=='inverted':
        level=h-12;basetop=h-5;bottom=9;left=15;bw=w-30
        c.setFillColor(CYAN);c.rect(left,bottom,bw,level-bottom,stroke=0,fill=1)
        line(left,bottom,left,basetop);line(left,bottom,left+bw,bottom);line(left+bw,bottom,left+bw,basetop);line(left,level,left+bw,level,TEAL)
        cx=w*.48;top=h-22;inside=bottom+5;basin_glass(cx,bottom+4,inside,top,True,True)
        text('papier sec',w-38,top-3,10.2,bold=True);leader([(w-40,top-2),(cx+9,top-2),(cx+6,top-4)])
        text('air piégé',w-38,inside+12,10.2);leader([(w-40,inside+13),(cx+13,inside+13),(cx+5,inside+10)])
        text('eau',left+5,level-8,10.6,color=TEAL,bold=True)
    elif kind=='particles':
        import random
        rng=random.Random(621);bw=(w-20)/3;bh=h-18;yy=11
        for idx in range(3):
            xx=3+idx*(w/3);rect(xx,yy,bw,bh)
            if idx==0:points=[(7+j*3.4,4+i*3.4) for i in range(4) for j in range(4)]
            elif idx==1:points=[(6+j*3.4+(i%2)*1.4,3+i*3.4) for i in range(4) for j in range(4)]
            else:points=[(4+j*(bw-8)/3+rng.uniform(-.7,.7),4+i*(bh-8)/3+rng.uniform(-.7,.7)) for i in range(4) for j in range(4)]
            for px,py in points:c.setFillColor(TEAL);c.circle(xx+px,yy+py,1.0,stroke=0,fill=1)
            text(['Solide : modèle ordonné','Liquide : particules proches','Gaz : particules espacées'][idx],xx+bw/2,3,9.8,bold=True,center=True)
    elif kind=='powder':
        bh=min(35,h-16);beaker(18,12,35,bh);beaker(w-60,12,35,bh,19)
        for i in range(5):
            for j in range(7):
                xx=20+j*4.5+(i%2)*1.5;yy=15+i*3
                polygon([(xx,yy),(xx+2.3,yy+.2),(xx+2.8,yy+1.9),(xx+1,yy+2.5)],PALE,MUTED)
        text('Sable : grains solides',36,3,10.8,bold=True,center=True);text('Eau liquide',w-43,3,10.8,bold=True,center=True)
    elif kind=='airtransfer':
        final=bool(data);water=h-15;bottom=9
        c.setFillColor(CYAN);c.rect(8,bottom,w-16,water-bottom,stroke=0,fill=1)
        line(8,bottom,8,h-5);line(8,bottom,w-8,bottom);line(w-8,bottom,w-8,h-5);line(8,water,w-8,water,TEAL)
        cxs=[w*.30,w*.70]
        for i,cx in enumerate(cxs):
            top=h-22;air=(i==1) if final else (i==0);basin_glass(cx,15,22,top,air,False);text('B' if i else 'A',cx,2,11,bold=True,center=True)
            if air:text('air',cx,(22+top)/2-1,10.7,center=True)
        text('Après transfert' if final else 'Situation de départ',w/2,h-5,10.5,bold=True,center=True)
    elif kind in ['weighing','measurehero','equipment']:
        if kind=='weighing':
            vals=data or ['48,6','0,0','74,5'];centers=[w/6,w/2,5*w/6]
            for idx,(cx,v) in enumerate(zip(centers,vals)):
                balance(cx,14,v,True,idx==2);text(['1 · Poser le récipient','2 · Faire la tare','3 · Ajouter le liquide'][idx],cx,4,10.1,bold=True,center=True)
            text('Récipient vide',centers[0],h-5,10.3,center=True);text('Même récipient',centers[1],h-5,10.3,center=True);text('Masse du liquide seule',centers[2],h-5,10.3,center=True)
        else:
            balance(w*.28,12,'74,5',True,True)
            cylinder(w*.66,12,maxv=100,value=58,bh=min(60,h-20),label=None)
            text('MASSE',w*.28,h-5,10.5,color=GREEN,bold=True,center=True);text('VOLUME',w*.75,h-5,10.5,color=GREEN,bold=True,center=True)
    elif kind=='meniscus':
        cx,level=cylinder(26,6,50,36,2,bh=h-14,bw=24)
        # The line of sight passes through the lowest point of the concave meniscus.
        eye=w-24;c.setDash(1.5,1.4);line(cx,level,eye-7,level,GREEN,.35);c.setDash()
        p=c.beginPath();p.moveTo(eye-7,level);p.curveTo(eye-3,level+4,eye+3,level+4,eye+7,level);p.curveTo(eye+3,level-4,eye-3,level-4,eye-7,level)
        c.setStrokeColor(NAVY);c.setLineWidth(.4);c.drawPath(p);c.circle(eye,level,1.6,stroke=1,fill=0)
        text('Œil à la bonne hauteur',eye-38,level-11,10.6,bold=True)
        text('Bas du ménisque',75,level+15,10.5,bold=True);leader([(74,level+13),(62,level+13),(cx,level)])
        text('1 division = 2 mL',75,h-8,10.5,color=GREEN,bold=True)
    elif kind in ['cylinders','displacement']:
        vals,maxv,step=data;count=len(vals);slot=w/count
        for idx,value in enumerate(vals):
            xx=slot*(idx+.5)-14
            cylinder(xx,10,maxv,value,step,bh=h-19,bw=19,label=chr(65+idx) if kind=='cylinders' else ['Avant','Après'][idx],stone=kind=='displacement' and idx==1)
    elif kind=='floating':
        cylinder(w/2-14,8,100,60,5,bh=h-15,bw=23,stone=True,floating=True)
    elif kind=='cubes':
        cube(25,16,20);cube(w-63,13,31)
        text('1 cm³',38,7,12.5,bold=True,center=True);text('1 dm³ = 1 L',w-44,5,12.5,bold=True,center=True)
        text('arête : 1 cm',26,h-5,10.3);text('arête : 1 dm',w-64,h-5,10.3)
    elif kind=='massvolume':
        for idx,(cx,label,val) in enumerate([(w*.28,'20 mL d’eau','20,0'),(w*.72,'20 mL de cette huile','18,0')]):
            balance(cx,14,val,True,True);text(label,cx,h-4,11,bold=True,center=True)
        text('Les balances ont été tarées avec les récipients vides.',w/2,3,9.8,color=MUTED,center=True)
    elif kind=='balls':
        for i in range(20):
            cx=12+(i%10)*(w-24)/9;cy=h-15-(i//10)*16;c.setFillColor(CYAN);c.setStrokeColor(TEAL);c.circle(cx,cy,3.8,stroke=1,fill=1)
        text('20 billes identiques',w/2,3,11,bold=True,center=True)
    elif kind=='graphwater':
        xx=17;yy=15;gw=w-42;gh=h-30
        for i in range(5):
            px=xx+gw*i/4;py=yy+gh*i/4;line(px,yy,px,yy+gh,RULE,.2);line(xx,py,xx+gw,py,RULE,.2)
            text(i*20,px,yy-5,9,center=True);text(i*20,xx-7,py-1,9,center=True)
        line(xx,yy,xx+gw,yy+gh,TEAL,.5)
        for i in range(1,5):c.setFillColor(TEAL);c.circle(xx+gw*i/4,yy+gh*i/4,1.1,stroke=0,fill=1)
        text('m (g)',xx-7,yy+gh+5,10.3,bold=True);text('V (mL)',xx+gw-7,3,10.3,bold=True)
    c.restoreState()
