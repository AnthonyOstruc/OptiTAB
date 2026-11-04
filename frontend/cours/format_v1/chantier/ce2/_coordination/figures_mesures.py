from commun_redaction import ROOT
import json,math
B=chr(92)
def tex(s):return s.replace('@',B)
def picture(s):return tex('@begin{tikzpicture}[line width=0.9pt,text=otInk]\n'+s+'\n@end{tikzpicture}')
def node(x,y,t,opts=''):return tex(f'@node[{opts}] at ({x},{y}) {{{t}}};\n')
def ruler(y,end,label):
 s=tex(f'@draw[otNavy!12,fill=otNavy!4] (0,{y}) rectangle (8,{y-0.7});\n')
 for v in range(101):
  x=v*.08;ln=.26 if v%10==0 else .18 if v%5==0 else .1
  s+=tex(f'@draw[otMuted,line width=0.5pt] ({x},{y})--({x},{y-ln});\n')
  if v%10==0:s+=node(x,y-.49,str(v),'font=@small')
 s+=tex(f'@draw[otGreenDark,line width=2pt] (0.8,{y+0.55})--({end*.08},{y+0.55});\n')
 for v in (10,end):
  s+=tex(f'@draw[otMuted,densely dashed] ({v*.08},{y+.05})--({v*.08},{y+.65});\n')
  s+=node(v*.08,y+.96,str(v)+' mm','font=@small,text=otNavy')
 s+=node(-.4,y+.55,label,'text=otGreenDark,font=@bfseries')
 return s
def clock(h,m):
 s=tex('@draw[otNavy,line width=1pt] (0,0) circle (1.75);\n')
 for i in range(60):
  angle=90-i*6;r=1.58 if i%5==0 else 1.66
  s+=tex(f'@draw[otMuted,line width={0.8 if i%5==0 else 0.4}pt] ({angle}:{r})--({angle}:1.73);\n')
 for i in range(1,13):s+=node(round(1.32*math.cos(math.radians(90-30*i)),4),round(1.32*math.sin(math.radians(90-30*i)),4),str(i),'font=@large')
 if h is not None:
  s+=tex(f'@draw[otNavy,line width=2pt,-{{Stealth[length=2mm]}}] (0,0)--({90-30*(h%12)-m/2}:0.78);\n@draw[otGreenDark,line width=1.4pt,-{{Stealth[length=2mm]}}] (0,0)--({90-6*m}:1.06);\n@fill[otNavy] (0,0) circle (0.055);')
 return picture(s)
def timeline(labels,positions,durations):
 s=tex('@draw[otNavy,-{Stealth[length=2mm]}] (-.2,0)--(8.1,0);\n')
 for i,(label,x) in enumerate(zip(labels,positions)):
  s+=tex(f'@draw[otNavy] ({x},-.1)--({x},.1);')+node(x,-.45 if i%2==0 else -.92,label,'font=@large')
 for i,d in enumerate(durations):
  a,b=positions[i],positions[i+1]
  s+=tex(f'@draw[otGreenDark,{{Stealth[length=1.4mm]}}-{{Stealth[length=1.4mm]}}] ({a},.5)--({b},.5);')+node((a+b)/2,.94,d,'font=@small,text=otGreenDark')
 return picture(s)
F={}
F[24]={'regle_53':picture(ruler(0,63,'')),'deux_regles':picture(ruler(0,63,'A')+ruler(-2.2,82,'B'))}
s=tex('@draw[otNavy,line width=1.2pt] (0,0) rectangle (6,3);')
for x,y,t in [(3,3.42,'6 cm'),(3,-.42,'6 cm'),(-.65,1.5,'3 cm'),(6.65,1.5,'3 cm')]:s+=node(x,y,t,'font=@large')
rect=picture(s)
F[25]={'rectangle_6_3':rect,'triangle_3_4_5':picture(tex('@draw[otNavy,line width=1.2pt] (0,0)--(4,0)--(0,3)--cycle;')+node(2,-.45,'4 cm','font=@large')+node(-.65,1.5,'3 cm','font=@large')+node(2.5,1.9,'5 cm','font=@large'))}
s=tex('@draw[otNavy,fill=otNavy!8] (3.7,-.7)--(4.3,-.7)--(4,2.3)--cycle; @draw[otNavy,line width=2pt] (.6,2.3)--(7.4,2.3);')
for x in (1.4,6.2):s+=tex(f'@draw[otMuted] ({x-.85},2.3)--({x-1.1},.3)--({x+1.1},.3)--({x+.85},2.3); @draw[otNavy,line width=1.4pt] ({x-1.2},.3)--({x+1.2},.3);')
s+=tex('@draw[otNavy,fill=otNavy!10,rounded corners=2pt] (.8,.32) rectangle (2,1.35);')+node(1.4,.85,'?','font=@Large')+node(1.4,-.2,'Objet','font=@large')
for x,l in [(5.4,'500'),(6.2,'200'),(7,'50')]:s+=tex(f'@draw[otGreenDark,fill=otGreen!12] ({x-.36},.32) rectangle ({x+.36},1.05);')+node(x,.7,l,'font=@small')
s+=node(6.2,-.2,'Masses en g','font=@large')
F[26]={'balance_750':picture(s)}
s=''
for x,level,label in [(0,100,'A'),(4.2,60,'B')]:
 s+=tex(f'@fill[otNavy!15] ({x},0) rectangle ({x+1.4},{level*.03}); @draw[otNavy,line width=1pt] ({x},3.8)--({x},0)--({x+1.4},0)--({x+1.4},3.8); @draw[otGreenDark,line width=1.1pt] ({x},{level*.03})--({x+1.4},{level*.03});')
 for v in range(0,121,20):s+=tex(f'@draw[otMuted] ({x+1.25},{v*.03})--({x+1.65},{v*.03});')+node(x+2.06,v*.03,str(v),'font=@small')
 s+=node(x+.7,4.25,label,'font=@Large,text=otNavy')+node(x+2.06,4,'cL','font=@small')
F[27]={'recipients_100_60':picture(s)}
s=''
for i,l in enumerate(['2 €','1 €','50 c','20 c','5 c']):
 x=i*1.55;s+=tex(f'@draw[otNavy,fill=otOrange!15,line width=1pt] ({x},0) circle (.64);')+node(x,0,l,'font=@large')
F[28]={'pieces_375':picture(s)};F[29]={}
F[30]={'horloge_8_20':clock(8,20),'horloge_10_35':clock(10,35),'horloge_15_42':clock(15,42),'horloge_11_55':clock(11,55),'cadran_vierge':clock(None,None)}
F[31]={'frise_9_20_10_05':timeline(['9 h 20','10 h','10 h 05'],[0,6.4,7.2],['40 min','5 min']),'frise_8_50_9_10':timeline(['8 h 50','9 h','9 h 10'],[0,3.6,7.2],['10 min','10 min'])}
course={24:'regle_53',25:'rectangle_6_3',26:'balance_750',27:'recipients_100_60',28:'pieces_375',30:'horloge_8_20',31:'frise_9_20_10_05'}
alts={'regle_53':'Segment dont les extrémités sont repérées à 10 mm et 63 mm sur une règle graduée.','deux_regles':'Deux règles de même échelle : A entre 10 et 63 mm, B entre 10 et 82 mm.','rectangle_6_3':'Rectangle dont les quatre côtés sont cotés : 6 cm, 3 cm, 6 cm et 3 cm.','triangle_3_4_5':'Triangle avec les trois longueurs de côtés : 3 cm, 4 cm et 5 cm.','balance_750':'Balance en équilibre : un objet à gauche et trois masses de 500 g, 200 g et 50 g à droite.','recipients_100_60':'Deux récipients A et B gradués en centilitres, avec des traits espacés de 20 cL.','pieces_375':'Cinq pièces représentant 2 euros, 1 euro, 50 centimes, 20 centimes et 5 centimes.','cadran_vierge':'Cadran sans aiguilles, avec les douze nombres et les soixante graduations de minutes.','frise_9_20_10_05':'Frise de 9 h 20 à 10 h 05 : un intervalle de 40 minutes puis un intervalle de 5 minutes.','frise_8_50_9_10':'Frise de 8 h 50 à 9 h 10 : deux intervalles successifs de dix minutes.'}
for code,figs in F.items():
 d=next(ROOT.glob(f'{code:02}_*'));(d/'figures/figures.py').write_text('# -*- coding: utf-8 -*-\n"""Figures TikZ ; compilation officielle figures_livre.py."""\nFIGURES = '+repr(figs)+'\n',encoding='utf-8')
 def im(name):return {'fichier':name+'.png','alt':alts.get(name,'Horloge à deux aiguilles avec les soixante graduations et la position exacte de chaque aiguille.')}
 corr={'cours':{'nouveau':{'1':im(course[code])} if code in course else {}},'fiches':{'nouvelle':{}},'exercices':{}}
 for e in json.loads((d/'donnees_exercices_root.json').read_text(encoding='utf-8')):
  if e['figures']:corr['exercices'][e['id']]={k:im(v.removesuffix('.png')) for k,v in e['figures'].items()}
 (d/'figures/correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,len(figs),'figures définies')
