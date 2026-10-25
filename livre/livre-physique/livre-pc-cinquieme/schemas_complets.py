"""Schémas scientifiques vectoriels du manuel complet, repère 166 x 70 mm."""
from math import sin, cos, pi, atan2
from reportlab.lib.colors import HexColor
from maquette import mm, white, NAVY, GREEN, INK, MUTED, RULE, PALE, MINT, CREAM, CYAN, TEAL, ORANGE

def draw_full(c,spec,x,y,width,height):
    kind,data=spec; kind=kind.removeprefix('pc_')
    c.saveState();c.translate(x,y);c.scale(width/166,height/70)
    def T(s,x,y,size=10.5,color=INK,bold=False,center=False):
        c.setFont('Bold' if bold else 'Body',size/mm);c.setFillColor(color)
        for i,t in enumerate(str(s).split('\n')):
            (c.drawCentredString if center else c.drawString)(x,y-i*size*.43,t)
    def L(x1,y1,x2,y2,color=NAVY,lw=.4):
        c.setStrokeColor(color);c.setLineWidth(lw);c.line(x1,y1,x2,y2)
    def P(pts,fill=CYAN,stroke=NAVY):
        p=c.beginPath()
        for i,pt in enumerate(pts):(p.moveTo if i==0 else p.lineTo)(*pt)
        p.close();c.setFillColor(fill);c.setStrokeColor(stroke);c.setLineWidth(.35);c.drawPath(p,fill=1,stroke=1)
    def R(x,y,w,h,fill=PALE,stroke=NAVY):
        c.setFillColor(fill);c.setStrokeColor(stroke);c.setLineWidth(.35);c.roundRect(x,y,w,h,min(1.5,w/2,h/2),fill=1,stroke=1)
    def C(x,y,r,fill=CYAN,stroke=NAVY):
        c.setFillColor(fill);c.setStrokeColor(stroke);c.setLineWidth(.4);c.circle(x,y,r,fill=1,stroke=1)
    def A(x1,y1,x2,y2,color=GREEN):
        L(x1,y1,x2,y2,color,.45);a=atan2(y2-y1,x2-x1)+pi
        for d in [-.38,.38]:L(x2,y2,x2+2*cos(a+d),y2+2*sin(a+d),color,.45)
    def B(x,y,level=15,bw=27,bh=34,fill=CYAN):
        c.setFillColor(fill);c.rect(x+.4,y+.4,bw-.8,level-.4,fill=1,stroke=0)
        L(x+.4,y+level,x+bw-.4,y+level,TEAL)
        L(x,y,x,y+bh);L(x,y,x+bw,y);L(x+bw,y,x+bw,y+bh)
    def dot(x,y,color=TEAL,r=.8):C(x,y,r,color,color)
    def lamp(x,y,on=True):
        C(x,y,5.4,CREAM if on else PALE);L(x-3,y-3,x+3,y+3);L(x-3,y+3,x+3,y-3)
    def battery(x,y,vertical=False):
        if vertical:
            L(x-5,y+2,x+5,y+2,NAVY,.65);L(x-3,y-2,x+3,y-2,NAVY,.65);T('+',x-9,y+1,10)
        else:
            L(x-2,y-5,x-2,y+5,NAVY,.65);L(x+2,y-3,x+2,y+3,NAVY,.65);T('+',x-5,y+7,10);T('-',x+5,y+7,10)
    def plot(times,values,xlabel='t (min)',ylabel='θ (°C)',ymin=0,ymax=None):
        ymax=ymax if ymax is not None else max(values);xx=20;yy=14;ww=130;hh=44
        xmin=0;xmax=max(times)
        for i in range(5):
            py=yy+i*hh/4;v=ymin+(ymax-ymin)*i/4
            L(xx,py,xx+ww,py,RULE,.2);T(f'{v:g}'.replace('.',','),12,py-1,9.5,center=True)
        for v in times:
            px=xx+ww*v/xmax;L(px,yy,px,yy+hh,RULE,.2);T(f'{v:g}',px,yy-5,9.5,center=True)
        A(xx,yy,xx+ww+3,yy,NAVY);A(xx,yy,xx,yy+hh+3,NAVY)
        T(ylabel,3,65,10.5,bold=True);T(xlabel,143,2,10,center=True)
        coords=[(xx+ww*t/xmax,yy+hh*(v-ymin)/(ymax-ymin)) for t,v in zip(times,values)]
        for a,b in zip(coords,coords[1:]):L(*a,*b,TEAL,.6)
        for a,b in coords:dot(a,b)
    if kind=='changes':
        for x0,label in [(4,'SOLIDE'),(65,'LIQUIDE'),(126,'GAZ')]:R(x0,27,36,16);T(label,x0+18,33,11,bold=True,center=True)
        for a,b,up,down in [(40,65,'fusion','solidification'),(101,126,'vaporisation','liquéfaction')]:
            A(a,40,b,40);A(b,30,a,30);T(up,(a+b)/2,53,10,center=True);T(down,(a+b)/2,16,10,center=True)
        T('Apport d’énergie : vers la droite',83,65,10.5,GREEN,True,True)
        T('Retrait d’énergie : vers la gauche',83,3,10.5,MUTED,False,True)
    elif kind=='temperature':
        d=data or {};plot(d.get('t',[0,1,2,3,4,5]),d.get('v',[-10,-5,0,0,0,5]),ymin=d.get('min',-10),ymax=d.get('max',10))
    elif kind=='freeze_mass':
        for x0,label,level in [(21,'Eau liquide',20),(111,'Glace',24)]:
            R(x0-6,7,40,13);R(x0,10,28,6,NAVY);T('100,0 g',x0+14,11.5,11,white,True,True)
            B(x0+1,21,level,26,33);L(x0,54,x0+28,54);T(label,x0+14,61,11,bold=True,center=True)
        A(63,38,98,38);T('refroidir',81,45,10,center=True);T('Même récipient fermé',83,2,10,MUTED,center=True)
    elif kind=='particles_mix':
        for i,label in enumerate(['Une seule espèce','Deux espèces mélangées']):
            x0=9+i*83;R(x0,14,64,42,white)
            for k in range(12):
                xx=x0+9+(k%4)*15;yy=23+(k//4)*12
                C(xx,yy,1.8,TEAL if i==0 or k%3 else ORANGE,TEAL if i==0 or k%3 else ORANGE)
            T(label,x0+32,4,10.6,bold=True,center=True)
        T('Chaque couleur représente une espèce chimique.',83,64,10,MUTED,center=True)
    elif kind=='air':
        for k in range(100):
            col=TEAL if k<78 else GREEN if k<99 else ORANGE
            C(11+(k%10)*4.4,10+(k//10)*5,1.3,col,col)
        for i,(col,txt) in enumerate([(TEAL,'78 % de diazote'),(GREEN,'21 % de dioxygène'),(ORANGE,'1 % d’autres gaz')]):
            C(75,51-i*16,2,col,col);T(txt,82,49.5-i*16,12,bold=True)
        T('Air sec : valeurs arrondies en volume',83,65,10.5,MUTED,center=True)
    elif kind in ['mixtures','dissolve']:
        if kind=='mixtures':labels=['Une seule phase visible','Deux phases visibles'];levels=[1,2]
        else:labels=['Solvant + soluté','Solution','Solution saturée'];levels=[1,1,3]
        for i,(label,mode) in enumerate(zip(labels,levels)):
            cx=(i+.5)*166/len(labels);B(cx-14,16,23)
            if mode==2:
                c.setFillColor(CREAM);c.rect(cx-13.5,39,26,10,fill=1,stroke=0);L(cx-13.5,39,cx+12.5,39,ORANGE)
            if kind=='dissolve':
                if i==0 or i==2:
                    for k in range(10):R(cx-11+(k%5)*4.5,17+(k//5)*2.3,1.6,1.6,white)
                if i>0:
                    for k in range(10):dot(cx-10+(k%4)*6,23+(k//4)*6,ORANGE,.65)
            T(label,cx,5,10.5,bold=True,center=True)
        T('Observer à l’œil nu, après agitation puis repos.',83,63,10.5,MUTED,center=True)
    elif kind=='decant':
        for i,label in enumerate(['Au départ','Après repos']):
            xx=17+i*89;B(xx,14,33,32,42)
            for k in range(25):dot(xx+3+(k%7)*4,17+(k//7)*(7 if i==0 else 1.4),ORANGE,.65)
            T(label,xx+16,4,11,bold=True,center=True)
        A(62,37,97,37);T('repos',80,44,10,center=True)
    elif kind=='filter':
        P([(57,60),(109,60),(86,35),(86,23),(80,23),(80,35)],PALE)
        P([(62,59),(104,59),(83,39)],white)
        for k in range(12):dot(70+(k%6)*4.8,50+(k//6)*3,ORANGE,.8)
        B(68,2,9,30,18);L(83,23,83,16,TEAL);C(83,13,1,TEAL,TEAL)
        T('papier-filtre',4,58,10.5);L(30,56,65,56,MUTED,.25)
        T('résidu solide',111,53,10.5);L(110,50,96,51,MUTED,.25)
        T('entonnoir',112,34,10.5);L(110,33,92,38,MUTED,.25)
        T('filtrat',111,7,10.5);L(109,8,99,9,MUTED,.25)
    elif kind=='distill':
        C(24,24,13,white)
        p=c.beginPath();p.moveTo(11,24);p.arc(11,11,37,37,180,180);p.close();c.setFillColor(CYAN);c.drawPath(p,fill=1,stroke=0);L(11.3,24,36.7,24,TEAL)
        L(20,36,20,53);L(28,36,28,53);L(20,53,48,53);L(28,48,48,48)
        P([(48,55),(125,33),(127,24),(50,46)],PALE)
        L(49,51,126,28,TEAL,.6);L(126,28,139,24);L(139,24,139,17)
        B(132,9,7,25,17);R(10,8,29,3,CREAM);T('chauffage',3,1,10)
        A(70,45,101,36);T('vapeur d’eau',49,64,10.5)
        T('réfrigérant',95,58,10.5);T('eau liquide',126,62,10.5)
        L(119,58,122,32,MUTED,.25);T('distillat',127,1,10.5,bold=True)
        T('eau froide',69,17,10.2);A(86,20,91,34,TEAL)
    elif kind=='lime':
        B(20,15,19,35,35);B(111,15,19,35,35,fill=PALE)
        for k in range(40):dot(114+(k%8)*4,17+(k//8)*3,RULE,.5)
        T('Eau de chaux limpide',37,4,10.5,bold=True,center=True)
        T('Trouble blanc',128,4,10.5,bold=True,center=True)
        A(64,38,102,38);T('gaz contenant',83,54,10.5,center=True);T('du CO₂',83,48,10.5,center=True)
    elif kind=='reaction':
        for i,label in enumerate(['Avant : deux réactifs','Après : gaz formé']):
            xx=23+i*90;R(xx-9,5,45,11);T('152,0 g',xx+13.5,8,11,NAVY,True,True)
            pts=[(xx,18),(xx+27,18),(xx+20,42),(xx+18,42),(xx+18,50),(xx+10,50),(xx+10,42),(xx+8,42)]
            P(pts,white);p=c.beginPath()
            for j,pt in enumerate(pts):(p.moveTo if j==0 else p.lineTo)(*pt)
            p.close();c.saveState();c.clipPath(p,stroke=0,fill=0);c.setFillColor(CYAN);c.rect(xx,18,27,16,fill=1,stroke=0);L(xx,34,xx+27,34,TEAL);c.restoreState();c.setStrokeColor(NAVY);c.setLineWidth(.35);c.drawPath(p,fill=0,stroke=1)
            if i:C(xx+14,57,8,PALE)
            else:R(xx+10,50,8,4,PALE)
            T(label,xx+14,1,10.2,center=True)
        T('Ensemble fermé : aucune matière n’entre ni ne sort.',83,65,10.2,MUTED,center=True)
    elif kind=='solar':
        names=['Mercure','Vénus','Terre','Mars','Jupiter','Saturne','Uranus','Neptune']
        radii=[2,3,3.1,2.5,7,6,4.5,4.5]
        C(8,34,7,CREAM,ORANGE);T('Soleil',8,15,10.3,bold=True,center=True)
        for i,(name,r) in enumerate(zip(names,radii)):
            cx=27+i*18;C(cx,34,r,TEAL if i==2 else PALE)
            if i==5:c.setStrokeColor(MUTED);c.ellipse(cx-10,31,cx+10,37,stroke=1,fill=0)
            yy=54 if i%2 else 13;T(name,cx,yy,9.5,center=True);L(cx,34+r if i%2 else 34-r,cx,yy-3 if i%2 else yy+4,RULE,.25)
        T('Ordre des planètes : tailles et distances non à l’échelle.',83,65,10.5,MUTED,center=True)
    elif kind=='solar_scale':
        # Échelle réelle des distances moyennes des quatre planètes internes.
        L(12,26,151,26);C(12,26,2,CREAM,ORANGE)
        for km,name,up in [(58,'Mercure',False),(108,'Vénus',True),(150,'Terre',False),(228,'Mars',True)]:
            cx=12+km*.6;C(cx,26,1.4,TEAL);yy=44 if up else 10
            L(cx,26,cx,yy-4 if up else yy+5,RULE,.25);T(name,cx,yy,10.5,center=True)
        T('Soleil',12,44,10.5,center=True);L(12,61,42,61);L(12,59,12,63);L(42,59,42,63)
        T('30 mm ↔ 50 millions de km',46,59,10.5,bold=True)
    elif kind=='daynight':
        C(17,36,11,CREAM,ORANGE)
        for yy in [18,30,42,54]:A(37,yy,86,yy,ORANGE)
        C(111,36,20,CYAN)
        # Demi-disque sombre opposé au Soleil.
        p=c.beginPath();p.moveTo(111,16);p.arc(91,16,131,56,-90,180);p.close();c.setFillColor(NAVY);c.drawPath(p,fill=1,stroke=0)
        T('jour',93,4,11,bold=True);T('nuit',125,4,11,bold=True)
        T('Soleil',17,12,11,center=True);T('Terre',111,63,11,center=True)
    elif kind=='trajectories':
        L(8,36,47,36,TEAL,.7);A(24,36,37,36)
        c.setStrokeColor(TEAL);c.setLineWidth(.6);c.circle(83,36,17,stroke=1,fill=0);A(100,36,99,43)
        p=c.beginPath();p.moveTo(122,21);p.curveTo(127,53,144,10,158,49);c.setStrokeColor(TEAL);c.drawPath(p);A(151,32,155,40)
        for xx,txt in [(28,'Rectiligne'),(83,'Circulaire'),(140,'Curviligne')]:T(txt,xx,7,11,bold=True,center=True)
        T('La trajectoire dépend de l’observateur choisi.',83,65,10.5,MUTED,center=True)
    elif kind=='chrono':
        rows=data or [[0,1,2,3,4],[0,.4,1.1,2.3,4],[0,1.7,2.9,3.6,4]]
        for i,arr in enumerate(rows):
            yy=55-i*21;L(34,yy,154,yy,RULE,.3)
            for k,v in enumerate(arr):C(37+v*27,yy,1.8,TEAL);T(str(k),37+v*27,yy+4,8.8,center=True)
            T(chr(65+i),8,yy-1,11,bold=True)
        T('Positions relevées à intervalles de temps égaux →',83,2,10.3,MUTED,center=True)
    elif kind=='reference':
        R(28,20,111,31,PALE);R(34,33,20,12,CYAN);R(61,33,20,12,CYAN);R(106,33,23,12,CYAN)
        C(48,17,4,PALE);C(119,17,4,PALE);C(95,39,2.5,CREAM);L(95,36,95,26);L(90,32,100,32)
        T('Voyageur assis',91,60,10.5,center=True);L(92,56,95,43,MUTED,.25)
        L(10,9,156,9);T('Quai',12,2,10);A(143,42,160,42);T('train',146,51,10)
    elif kind=='speed':
        d=data or {'t':[0,1,2,3,4],'v':[0,3,6,9,12]};plot(d['t'],d['v'],'t (s)','d (m)',ymax=d.get('max',12))
    elif kind=='path':
        L(12,20,150,20,RULE,.4);p=c.beginPath();p.moveTo(12,20);p.curveTo(48,66,117,66,150,20);c.setStrokeColor(TEAL);c.setLineWidth(.7);c.drawPath(p)
        T('A',10,10,11,bold=True);T('B',151,10,11,bold=True);T('Trajet parcouru : 120 m',83,58,11,bold=True,center=True)
        T('Séparation en ligne droite : 80 m',83,8,10.5,MUTED,center=True)
    elif kind=='magnet':
        R(15,24,27,22,PALE);R(42,24,27,22,MINT);T('N',28.5,33,13,bold=True,center=True);T('S',55.5,33,13,bold=True,center=True)
        c.setStrokeColor(NAVY);c.setLineWidth(.7);c.roundRect(118,31,21,8,3,stroke=1,fill=0);c.roundRect(122,33,13,4,1.5,stroke=1,fill=0)
        A(113,35,82,35);T('aimant',42,10,11,bold=True,center=True);T('trombone en acier',126,10,11,bold=True,center=True)
        T('Attraction possible sans contact',83,62,11,GREEN,True,True)
    elif kind=='interaction':
        R(63,27,40,17,MINT);T('Objet étudié',83,34,11,bold=True,center=True)
        names=(data or ['Table','Terre','Main'])
        for i,(xx,yy,name) in enumerate([(2,27,names[0]),(122,27,names[1]),(63,53,names[2])]):
            R(xx,yy,40,13);T(name,xx+20,yy+4.5,10.5,center=True)
        L(42,34,63,34);c.setDash(2,1.5);L(103,34,122,34);c.setDash();L(83,44,83,53)
        T('trait plein : contact',42,9,10,MUTED,center=True);T('pointillés : à distance',124,9,10,MUTED,center=True)
    elif kind=='actions':
        R(7,20,38,21,PALE);T('Déformer',26,54,11,bold=True,center=True)
        for i in range(6):L(14+i*4,29,16+i*4,35);L(16+i*4,35,18+i*4,29)
        A(3,31,10,31);A(51,31,43,31)
        C(83,30,7,CYAN);A(91,30,109,30);T('Mettre en mouvement',83,54,10.5,bold=True,center=True)
        C(138,25,5,CYAN);A(119,25,131,25,TEAL);A(138,19,138,8);T('Modifier la trajectoire',138,54,10.1,bold=True,center=True)
    elif kind=='energy':
        d=data or ['Pile','Lampe','Lumière','Transfert thermique']
        R(3,28,41,23,PALE);R(62,28,42,23,MINT);R(123,40,40,18,CREAM);R(123,8,40,18,PALE)
        T(d[0],23.5,39,10.5,bold=True,center=True);T(d[1],83,39,10.5,bold=True,center=True)
        T(d[2],143,49,10.1,center=True);T(d[3],143,18,10,center=True)
        A(44,39,62,39);A(104,42,123,48);A(104,34,123,18)
        T('rayonnement' if d[0]=='Soleil' else 'électrique',53,46,9.0,MUTED,center=True)
        T('source / réserve',23,62,9.8,MUTED,center=True);T('convertisseur',83,62,9.8,MUTED,center=True)
    elif kind=='budget':
        d=data or [100,30,70];R(55,23,47,27,MINT);T('Convertisseur',78.5,34,11,bold=True,center=True)
        A(2,37,55,37);A(102,43,161,51);A(102,30,161,15)
        T(f'Entrée : {d[0]} J',26,45,10.5,bold=True,center=True)
        T(f'Utile : {d[1]} J',134,60,10.5,bold=True,center=True);T(f'Autre transfert : {d[2]} J',125,4,10.5,center=True)
    elif kind=='energy_choice':
        vals=data or [120,36];maximum=max(vals);barw=112
        for i,v in enumerate(vals):
            yy=42-i*25;T(chr(65+i),7,yy+5,11,bold=True);R(23,yy,barw*v/maximum,16,PALE if i==0 else MINT)
            T(f'{v} kWh',25+barw*v/maximum,yy+5,10.5,bold=True)
        T('Énergie sur la même période, pour le même service',83,65,10.5,MUTED,center=True)
        L(23,9,135,9,RULE,.3);T('0',23,3,9.5,center=True)
    elif kind=='resources':
        items=[('Soleil','renouvelable'),('Vent','renouvelable'),('Eau en mouvement','renouvelable'),('Charbon','non renouvelable'),('Pétrole','non renouvelable'),('Uranium','non renouvelable')]
        for i,(name,lab) in enumerate(items):
            xx=3+(i%3)*55;yy=38-(i//3)*34;R(xx,yy,50,27,MINT if i<3 else PALE)
            T(name,xx+25,yy+17,10.5,bold=True,center=True);T(lab,xx+25,yy+7,9.7,center=True)
    elif kind in ['circuit','test_material']:
        mode=data or 'closed'
        if mode in ['parallel','parallel_open']:
            L(20,13,146,13);L(20,13,20,32);battery(20,34,True);L(20,36,20,55);L(20,55,82.6,55);lamp(88,55,mode!='parallel_open');L(93.4,55,111,55)
            if mode=='parallel_open':
                L(111,55,122,61);L(122,55,146,55);C(111,55,.8,white);C(122,55,.8,white)
            else:L(111,55,146,55)
            L(50,55,50,35);L(50,35,82.6,35);lamp(88,35);L(93.4,35,146,35);L(146,55,146,13)
            for xx,yy in [(50,55),(146,35)]:dot(xx,yy,NAVY,.8)
            T('L₁',88,65,10.5,center=True);T('L₂',88,22,10.5,center=True)
        else:
            L(20,12,81,12);battery(83,12);L(85,12,146,12);L(20,12,20,53);L(20,53,49.6,53)
            if mode=='series':
                lamp(55,53);L(60.4,53,104.6,53);lamp(110,53);L(115.4,53,146,53)
                T('L₁',55,64,10.5,center=True);T('L₂',110,64,10.5,center=True)
            else:
                L(49.6,53,77.6,53);lamp(83,53,mode not in ['open','short']);L(88.4,53,146,53)
            L(146,12,146,29);L(146,39,146,53)
            if kind=='test_material':R(139,29,14,10,CREAM);T('échantillon',132,4,10.3,center=True)
            elif mode=='open':L(146,29,153,40);C(146,29,.8,white);C(146,39,.8,white)
            else:L(146,29,146,39)
            if mode=='short':
                L(65,53,65,65,ORANGE,.7);L(65,65,101,65,ORANGE,.7);L(101,65,101,53,ORANGE,.7)
                T('Fil de court-circuit',81,2,10.5,ORANGE,True,True)
            if mode=='direction':
                A(31,53,48,53);A(127,12,109,12)
        if kind!='test_material' and mode!='short':T('Schéma de principe : très basse tension scolaire',83,2,10,MUTED,center=True)
    elif kind=='symbols':
        battery(22,45);T('Pile',22,24,11,bold=True,center=True)
        lamp(66,45);T('Lampe',66,24,11,bold=True,center=True)
        C(108,45,6,white);T('M',108,43.5,11,bold=True,center=True);T('Moteur',108,24,11,bold=True,center=True)
        L(142,45,147,45);L(147,45,156,51);C(147,45,.8,white);C(156,45,.8,white);L(156,45,162,45)
        T('Interrupteur',151,24,10.5,bold=True,center=True)
        T('ouvert',151,18,10.5,center=True)
    elif kind=='motor':
        for i,label in enumerate(['Polarité A','Polarité inversée']):
            cx=40+i*86;C(cx,37,11,MINT);T('M',cx,35,13,bold=True,center=True)
            angles=[(40+j*100/30 if i else 140-j*100/30)*pi/180 for j in range(31)]
            pts=[(cx+18*cos(a),37+18*sin(a)) for a in angles]
            for a,b in zip(pts,pts[1:]):L(*a,*b,GREEN,.45)
            A(*pts[-3],*pts[-1],GREEN)
            T(label,cx,14,11,bold=True,center=True)
        T('Même moteur à courant continu ; branchement inversé.',83,65,10.5,MUTED,center=True)
    elif kind=='lightchain':
        C(15,37,9,CREAM,ORANGE);R(68,26,27,22,CYAN)
        p=c.beginPath();p.moveTo(138,37);p.curveTo(142,43,150,43,154,37);p.curveTo(150,31,142,31,138,37);p.close();c.setFillColor(white);c.setStrokeColor(NAVY);c.drawPath(p,fill=1,stroke=1);C(146,37,2,PALE)
        A(25,37,67,37,ORANGE);A(96,37,137,37,TEAL)
        T('Source',15,14,11,bold=True,center=True);T('Objet diffusant',82,14,11,bold=True,center=True);T('Œil',146,14,11,bold=True,center=True)
        T('La lumière entre dans l’œil.',83,62,11,GREEN,True,True)
    elif kind=='materials_light':
        for i,(label,mode) in enumerate([('Transparent',0),('Translucide',1),('Opaque',2)]):
            yy=54-i*21;R(69,yy-7,7,14,CYAN if mode<2 else NAVY);A(14,yy,67,yy,ORANGE)
            if mode==0:A(78,yy,147,yy,ORANGE)
            if mode==1:
                for dy in [-6,0,6]:A(78,yy,144,yy+dy,ORANGE)
            T(label,7,yy+6,10.2,bold=True)
        T('Représentation simplifiée de la transmission',83,1,10,MUTED,center=True)
    elif kind=='aligned':
        shifted=bool(data);C(9,34,3,CREAM,ORANGE)
        for i,xx in enumerate([43,83,123]):
            hole=42 if shifted and i==1 else 34;L(xx,12,xx,hole-2);L(xx,hole+2,xx,58)
        A(13,34,81 if shifted else 151,34,ORANGE)
        T('Source',12,3,10.5,center=True);T('Écrans percés',84,65,11,bold=True,center=True)
        if shifted:T('lumière arrêtée',83,3,10.5,center=True)
    elif kind=='shadow':
        # Source ponctuelle S(10,35), objet vertical x=62, de 28 à 42.
        screen=150;bottom=35-7*(screen-10)/(62-10);top=35+7*(screen-10)/(62-10)
        P([(62,28),(screen,bottom),(screen,top),(62,42)],PALE,RULE)
        C(10,35,2,CREAM,ORANGE);L(62,28,62,42,NAVY,1.5);L(screen,8,screen,62,NAVY,.6)
        A(10,35,screen,top,ORANGE);A(10,35,screen,bottom,ORANGE)
        L(screen,bottom,screen,top,TEAL,2)
        T('S',10,25,11,bold=True,center=True);T('Objet opaque',57,6,10.5,center=True)
        T('Zone d’ombre',106,34,10.5,center=True);T('Écran',150,66,10.5,center=True)
    elif kind=='shadows':
        sx,sy,ox,rad,screen=10,35,64,9,150
        dx=ox-sx;tx=ox-rad*rad/dx;dy=rad*(1-(rad/dx)**2)**.5
        extent=dy*(screen-sx)/(tx-sx)
        P([(tx,sy-dy),(screen,sy-extent),(screen,sy+extent),(tx,sy+dy)],PALE,RULE)
        C(ox,sy,rad,CYAN)
        p=c.beginPath();p.moveTo(ox,sy-rad);p.arc(ox-rad,sy-rad,ox+rad,sy+rad,-90,180);p.close();c.setFillColor(NAVY);c.drawPath(p,fill=1,stroke=0)
        C(sx,sy,2,CREAM,ORANGE);A(sx,sy,screen,sy-extent,ORANGE);A(sx,sy,screen,sy+extent,ORANGE)
        L(screen,5,screen,64);L(screen,sy-extent,screen,sy+extent,TEAL,1.8)
        T('Ombre propre',58,64,10.3,bold=True,center=True);L(60,59,68,39,MUTED,.25)
        T('Zone d’ombre',105,34,10.3,center=True);T('Ombre portée',139,1,10.3,bold=True,center=True);T('S',10,23,11,bold=True,center=True)
    elif kind=='vibration':
        L(9,15,63,15,NAVY,1);R(9,3,16,23,PALE)
        for dy in [-5,5]:
            p=c.beginPath();p.moveTo(25,15);p.curveTo(45,15,55,15+dy,68,15+dy);c.setStrokeColor(TEAL);c.setLineWidth(.5);c.drawPath(p)
        A(64,27,64,42);A(69,42,69,27)
        T('Règle qui vibre',42,58,11,bold=True,center=True)
        for k in range(5):
            xx=91+k*13;c.setStrokeColor(RULE);c.ellipse(xx,22,xx+8,47,stroke=1,fill=0)
        T('Air',114,55,11,center=True);T('Oreille',151,12,11,center=True)
        A(83,34,153,34,TEAL)
        p=c.beginPath();p.moveTo(154,45);p.curveTo(166,49,165,29,156,25);p.curveTo(153,23,153,22,155,22);c.setStrokeColor(NAVY);c.setLineWidth(.45);c.drawPath(p)
        p=c.beginPath();p.moveTo(156,38);p.curveTo(163,45,163,32,157,31);c.drawPath(p)
    elif kind=='echo':
        R(7,19,24,35,PALE);T('Source',19,43,10.3,bold=True,center=True);T('et',19,36,10,center=True);T('récepteur',19,29,10,center=True)
        L(150,13,150,59,NAVY,1.2)
        for yy in range(15,59,6):L(150,yy,155,yy+4,RULE,.45)
        A(33,49,146,49);A(146,25,33,25,TEAL)
        T('Aller : distance d',89,56,11,bold=True,center=True);T('Retour : distance d',89,15,11,bold=True,center=True)
        T('Mur',150,65,11,bold=True,center=True);T('Trajet total : deux fois la distance au mur',83,2,10.5,MUTED,center=True)
    elif kind=='vacuum_sound':
        for i,label in enumerate(['Air présent','Air fortement raréfié']):
            xx=20+i*88;R(xx,12,38,45,white);R(xx+9,23,20,15,PALE);T('sonnerie',xx+19,28,9.5,center=True)
            if not i:
                for k in range(12):dot(xx+5+(k%4)*9,43+(k//4)*4,TEAL,.7)
            T(label,xx+19,3,10.3,bold=True,center=True)
        T('Le son transmis à travers l’air s’atténue.',83,66,10.5,MUTED,center=True)
    elif kind=='soundtrace':
        configs=data or [(2,7),(4,7),(2,12)]
        for i,(freq,amp) in enumerate(configs):
            yy=55-i*22;L(25,yy,155,yy,RULE,.3);pts=[(25+t*130/240,yy+amp/2*sin(t*2*pi*freq/240)) for t in range(241)]
            for a,b in zip(pts,pts[1:]):L(*a,*b,TEAL,.35)
            T(chr(65+i),8,yy-1,11,bold=True)
        T('Même durée représentée sur les trois lignes',83,1,10.3,MUTED,center=True)
    elif kind=='signal':
        d=data or ['Émetteur','Signal lumineux','Récepteur']
        for xx,txt in [(3,d[0]),(119,d[2])]:R(xx,23,44,25,PALE);T(txt,xx+22,34,11,bold=True,center=True)
        A(48,36,118,36);T(d[1],83,49,10.5,center=True);T('Information interprétée grâce à un code partagé',83,6,10.3,MUTED,center=True)
    elif kind=='code':
        values=data or [1,0,1,1,0,0,1,0];x0=10;cell=18
        for i,v in enumerate(values):
            R(x0+i*cell,32,cell-2,18,CREAM if v else PALE);T('1' if v else '0',x0+i*cell+8,38,12,bold=True,center=True)
            T(str(i+1),x0+i*cell+8,21,9.5,center=True)
        A(10,12,155,12);T('Temps →',83,2,10.5,center=True);T('Un intervalle = une valeur du signal',83,62,11,bold=True,center=True)
    elif kind=='sensor':
        for xx,lab in [(3,'Température'),(63,'Capteur'),(123,'Affichage')]:R(xx,28,40,24,PALE);T(lab,xx+20,38,10.5,bold=True,center=True)
        A(44,40,62,40);A(104,40,122,40);T('grandeur mesurée',24,14,9.8,MUTED,center=True);T('signal électrique',110,14,9.8,MUTED,center=True)
    else:
        raise ValueError(f'Schéma complet inconnu : {kind}')
    c.restoreState()
