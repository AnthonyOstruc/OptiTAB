"""Figures CE1, données explicites et géométrie vérifiable ; aucune écriture hors CE1."""
from commun_redaction import ROOT
import json, math, runpy
B=chr(92)
def tex(s):return s.replace('@',B)
def node(x,y,t,opts=''):return tex(f'@node[{opts}] at ({x},{y}) {{{t}}};\n')
def pic(s,opts=''):return tex('@begin{tikzpicture}[line width=1pt,text=otInk'+(','+opts if opts else '')+']\n'+s+'\n@end{tikzpicture}')
def line(points,opts='otNavy'):
 return tex('@draw['+opts+'] '+'--'.join(f'({x},{y})' for x,y in points)+';\n')
def dot(x,y):return tex(f'@fill[otNavy] ({x},{y}) circle (1.5pt);')
def ruler(start,end):
 s=tex('@draw[otNavy!20,fill=otNavy!4] (0,0) rectangle (7,-.8);')
 for i in range(21):
  x=i*.35;s+=line([(x,0),(x,-(.28 if i%2==0 else .14))],'otMuted,line width=.6pt')
  if i%2==0:s+=node(x,-.54,str(i//2),'font=@large')
 s+=line([(start*.7,.55),(end*.7,.55)],'otGreenDark,line width=2.2pt')
 for v in (start,end):s+=line([(v*.7,.05),(v*.7,.72)],'otMuted,densely dashed')+node(v*.7,1.08,str(v)+' cm','font=@large')
 return pic(s)
def balance(values):
 s=tex('@draw[otNavy,fill=otNavy!8] (3.7,-.7)--(4.3,-.7)--(4,2.3)--cycle; @draw[otNavy,line width=2pt] (.6,2.3)--(7.4,2.3);')
 for x in (1.4,6.2):s+=tex(f'@draw[otMuted] ({x-.85},2.3)--({x-1.1},.3)--({x+1.1},.3)--({x+.85},2.3); @draw[otNavy,line width=1.4pt] ({x-1.2},.3)--({x+1.2},.3);')
 s+=tex('@draw[otNavy,fill=otNavy!10,rounded corners=2pt] (.8,.32) rectangle (2,1.35);')+node(1.4,.85,'?','font=@Large')+node(1.4,-.2,'Objet','font=@large')
 for x,v in zip((5.4,6.2,7),values):s+=tex(f'@draw[otGreenDark,fill=otGreen!12] ({x-.36},.32) rectangle ({x+.36},1.05);')+node(x,.7,str(v),'font=@small')
 return pic(s+node(6.2,-.2,'Masses en g','font=@large'))
def coins(values):
 s=''
 for i,v in enumerate(values):
  x=i*1.65;s+=tex(f'@draw[otNavy,fill=otOrange!15] ({x},0) circle (.69);')+node(x,0,(str(v//100)+' €') if v>=100 else str(v)+' c','font=@large')
 return pic(s)
def clock(h,m):
 s=tex('@draw[otNavy] (0,0) circle (1.75);')
 for i in range(60):
  a=90-i*6;r=1.58 if i%5==0 else 1.66
  s+=tex(f'@draw[otMuted,line width={.8 if i%5==0 else .4}pt] ({a}:{r})--({a}:1.73);')
 for i in range(1,13):s+=node(round(1.32*math.cos(math.radians(90-30*i)),5),round(1.32*math.sin(math.radians(90-30*i)),5),str(i),'font=@large')
 if h is not None:s+=tex(f'@draw[otNavy,line width=2pt,-{{Stealth[length=2mm]}}] (0,0)--({90-30*(h%12)-m/2}:0.78); @draw[otGreenDark,line width=1.4pt,-{{Stealth[length=2mm]}}] (0,0)--({90-6*m}:1.06); @fill[otNavy] (0,0) circle (.055);')
 return s
def pair(a,b,labels=('A','B')):
 s=''
 for x,(h,m),label in zip((0,4.3),(a,b),labels):s+=tex(f'@begin{{scope}}[shift={{({x},0)}}]')+clock(h,m)+node(0,2.18,label,'font=@large')+tex('@end{scope}')
 return pic(s)
def timeline(labels,positions,durations):
 s=line([(-.2,0),(7.7,0)],'otNavy,-{Stealth[length=2mm]}')
 for i,(l,x) in enumerate(zip(labels,positions)):s+=line([(x,-.1),(x,.1)])+node(x,-.45 if i%2==0 else -.94,l,'font=@large')
 for i,d in enumerate(durations):
  a,b=positions[i:i+2];s+=line([(a,.5),(b,.5)],'otGreenDark,{Stealth[length=1.4mm]}-{Stealth[length=1.4mm]}')+node((a+b)/2,.97,d,'font=@large,text=otGreenDark')
 return pic(s)
def angles():
 s=''
 for x,a,label in [(0,90,'A'),(3,45,'B'),(6,120,'C')]:
  s+=tex(f'@begin{{scope}}[shift={{({x},0)}}] @draw[otNavy] (0,0)--(1.7,0); @draw[otNavy] (0,0)--({a}:1.7); @draw[otOrange] (.4,0) arc[start angle=0,end angle={a},radius=.4];')+node(.45,-.55,label,'font=@large')+tex('@end{scope}')
 return pic(s)
def polygon(points,labels=None,green=False):
 s=line(points+[points[0]],'otGreenDark' if green else 'otNavy')
 if labels:
  for (x,y),(l,dx,dy) in zip(points,labels):s+=dot(x,y)+node(x+dx,y+dy,'$'+l+'$','font=@large')
 return s
def rect(w,h,partial=False,circle=False):
 coords=[(0,0),(w,0),(w,h),(0,h)];labels=[('A',-.3,-.4),('B',.3,-.4),('C',.3,.4),('D',-.3,.4)]
 if partial:
  s=line([(w,0),(0,0),(0,h)])
  for (x,y),(l,dx,dy) in zip(coords,labels):
   if l!='C':s+=dot(x,y)+node(x+dx,y+dy,'$'+l+'$','font=@large')
 else:s=polygon(coords,labels,True)
 s+=node(w/2,-.85,str(w)+' cm','font=@large')+node(-.85,h/2,str(h)+' cm','font=@large')
 s+=line([(.25,0),(.25,.25),(0,.25)],'otOrange')
 if not partial:
  for x,y,dx,dy in [(w,0,-1,1),(w,h,-1,-1),(0,h,1,-1)]:s+=line([(x+dx*.25,y),(x+dx*.25,y+dy*.25),(x,y+dy*.25)],'otOrange')
 if circle:s+=tex(f'@draw[otNavy] (0,0) circle ({h});')
 return pic(s)
def triangle():
 s=polygon([(0,0),(4,0),(0,3)],[('A',-.3,-.4),('B',.3,-.4),('C',-.3,.4)],True)
 s+=node(2,-.55,'4 cm','font=@large')+node(-.8,1.5,'3 cm','font=@large')+line([(.3,0),(.3,.3),(0,.3)],'otOrange')
 return pic(s)
def gridcopy(points):
 s=''
 for ox,title,model in [(0,'Modèle',True),(4.5,'À reproduire',False)]:
  s+=tex(f'@begin{{scope}}[shift={{({ox},0)}},x=.55cm,y=.55cm] @draw[otNavy!18,line width=.4pt,step=1] (0,0) grid (6,6);')+node(3,6.85,title,'font=@large')
  labels=[('A',-.48,-.45),('B',.48,.35),('C',.48,-.35),('D',-.4,-.5)]
  if len(points)==3:labels[2]=('C',-.48,.35)
  if model:s+=polygon(points,labels[:len(points)])
  else:
   x,y=points[0];s+=dot(x,y)+node(x-.48,y-.45,'$A$','font=@large')
  s+=tex('@end{scope}')
 return pic(s)
def circle():
 return pic(tex('@draw[otNavy] (0,0) circle (2.4); @draw[otGreenDark] (0,0)--(2.4,0);')+dot(0,0)+dot(2.4,0)+node(0,-.42,'$O$','font=@large')+node(2.82,0,'$A$','font=@large')+node(1.2,.42,'3 cm','font=@large'))
def aligned():
 s=line([(-.5,-1/6),(6.5,13/6)],'otMuted')
 for x,y,l in [(0,0,'A'),(3,1,'B'),(6,2,'C')]:s+=dot(x,y)+node(x,y-.5,'$'+l+'$','font=@large')
 return pic(s)
def midpoint():
 s=line([(0,0),(6,0)],'otGreenDark')
 for x,l in [(0,'A'),(3,'M'),(6,'B')]:s+=dot(x,0)+node(x,-.45,'$'+l+'$','font=@large')
 for x in (1.5,4.5):s+=node(x,.5,'3 cm','font=@large')+line([(x,-.1),(x,.1)],'otOrange')
 return pic(s)
def pyramid():
 s=line([(0,0),(3,0),(4,1)])
 s+=line([(4,1),(1,1),(0,0)],'otMuted,densely dashed')
 for p in [(0,0),(3,0),(4,1)]:s+=line([p,(2,3.4)])
 s+=line([(1,1),(2,3.4)],'otMuted,densely dashed')
 return pic(s)
def net():
 s=tex('@draw[otNavy,fill=otNavy!5] (0,0)--(4,0)--(4,4)--(0,4)--cycle;')
 for a,b,c in [((0,0),(4,0),(2,-4)),((4,0),(4,4),(8,2)),((4,4),(0,4),(2,8)),((0,4),(0,0),(-4,2))]:s+=polygon([a,b,c])
 s+=tex('@draw[otOrange,densely dashed] (0,0)--(4,0)--(4,4)--(0,4)--cycle;')
 return pic(s,'x=.55cm,y=.55cm')
def stack():
 # Faces extérieures de trois cubes : deux au sol, un au-dessus du cube gauche.
 s=''
 for pts in [[(0,0),(2,0),(2,4),(0,4)],[(2,0),(4,0),(4,2),(2,2)],[(0,4),(.65,4.65),(2.65,4.65),(2,4)],[(2,4),(2.65,4.65),(2.65,2.65),(2,2)],[(2,2),(2.65,2.65),(4.65,2.65),(4,2)],[(4,0),(4.65,.65),(4.65,2.65),(4,2)]]:s+=polygon(pts)
 s+=line([(0,2),(2,2)])
 return pic(s)
def route(answer=False):
 s=tex('@draw[otNavy!22,line width=.5pt,step=1] (0,0) grid (5,5);')
 s+=tex('@fill[otNavy] (1.5,1.5) circle (.075);')+node(1.22,1.22,'$D$','font=@small')
 if answer:s+=line([(1.5,1.5),(1.5,3.5),(2.5,3.5)],'otGreenDark,line width=2pt,-{Stealth[length=2mm]}')+dot(2.5,3.5)
 else:s+=line([(1.5,1.5),(1.5,1.9)],'otGreenDark,line width=1.5pt,-{Stealth[length=1.6mm]}')
 return pic(s+node(2.5,-.5,'Départ : regarde vers le haut','font=@small'))

F={21:{'regle_2_9':ruler(2,9),'regle_1_8':ruler(1,8)},22:{'balance_350':balance([200,100,50]),'balance_720':balance([500,200,20])},23:{'pieces_235':coins([200,20,10,5]),'pieces_165':coins([100,50,10,5])},24:{'horloge_8_15':pic(clock(8,15)),'horloges_8_30_8_45':pair((8,30),(8,45),('8 h 30','8 h 45')),'horloges_9_15_11_30':pair((9,15),(11,30)),'horloges_14_15_17_45':pair((14,15),(17,45)),'cadran_vierge':pic(clock(None,None))},25:{'frise_8_30_9_15':timeline(['8 h 30','9 h','9 h 15'],[0,4.8,7.2],['30 min','15 min']),'frise_9_30_10_15':timeline(['9 h 30','10 h','10 h 15'],[0,4.8,7.2],['30 min','15 min']),'frise_15_45_16_15':timeline(['15 h 45','16 h','16 h 15'],[0,3.6,7.2],['15 min','15 min'])},26:{'angles_droit_aigu_obtus':angles(),'trois_formes':pic(polygon([(0,1.1),(1.1,2.2),(2.2,1.1),(1.1,0)])+node(1.1,-.55,'A','font=@large')+polygon([(3.2,0),(5.8,0),(5.8,1.5),(3.2,1.5)])+node(4.5,-.55,'B','font=@large')+polygon([(6.7,0),(8.5,0),(6.7,1.8)])+node(7.5,-.55,'C','font=@large')),'triangle_4_3_corrige':triangle(),'pentagone':pic(polygon([(0,0),(2.6,0),(3.6,1.8),(1.3,3),(-1,1.8)]))},27:{'cercle_O_A':circle(),'points_alignes':aligned(),'milieu_6_corrige':midpoint()},28:{'carre_oblique_a_reproduire':gridcopy([(1,3),(3,5),(5,3),(3,1)]),'rectangle_6_3':rect(6,3),'rectangle_5_3_corrige':rect(5,3),'rectangle_deux_cotes':rect(4,2,True),'triangle_4_3_corrige':triangle(),'triangle_a_reproduire':gridcopy([(1,1),(5,1),(1,4)]),'carre_diagonale_corrige':rect(3,3)[:-len(tex('@end{tikzpicture}'))]+line([(0,0),(3,3)],'otNavy')+tex('@end{tikzpicture}'),'rectangle_cercle_corrige':rect(6,2,circle=True)},29:{'pyramide':pyramid(),'faces_pyramide':net(),'assemblage_trois_cubes':stack()},30:{'plan_depart':route(),'trajet_2_1_corrige':route(True)}}
prior=runpy.run_path(str(next((ROOT.parent/'ce2').glob('34_*/figures/figures.py'))))['FIGURES']
F[29].update({'six_solides':prior['solides'],'cube':prior['cube_cache']})
courses={21:'regle_2_9',22:'balance_350',23:'pieces_235',24:'horloge_8_15',25:'frise_8_30_9_15',26:'angles_droit_aigu_obtus',27:'cercle_O_A',28:'rectangle_6_3',29:'six_solides',30:'trajet_2_1_corrige'}
ALTS={
 'balance_350':'Balance en équilibre : un objet et des masses de 200 g, 100 g et 50 g.',
 'balance_720':'Balance en équilibre : un objet et des masses de 500 g, 200 g et 20 g.',
 'pieces_235':'Quatre pièces : 2 euros, 20 centimes, 10 centimes et 5 centimes.',
 'pieces_165':'Quatre pièces : 1 euro, 50 centimes, 10 centimes et 5 centimes.',
 'horloge_8_15':'Cadran indiquant huit heures et quart, avec la petite aiguille déjà avancée après 8.',
 'horloges_8_30_8_45':'Deux exemples : huit heures et demie et neuf heures moins le quart.',
 'horloges_9_15_11_30':'Horloges du matin A et B, avec les deux aiguilles correctement positionnées.',
 'horloges_14_15_17_45':'Horloges A et B observées l’après-midi ; chaque petite aiguille avance entre les heures.',
 'cadran_vierge':'Cadran à douze nombres et soixante graduations, sans aiguilles, à reproduire.',
 'frise_8_30_9_15':'Frise de 8 h 30 à 9 h 15, partagée à 9 h : trente minutes puis quinze minutes.',
 'frise_9_30_10_15':'Frise de 9 h 30 à 10 h 15, partagée à 10 h : trente minutes puis quinze minutes.',
 'frise_15_45_16_15':'Frise de 15 h 45 à 16 h 15, partagée à 16 h en deux quarts d’heure égaux.',
 'trois_formes':'Trois figures A, B et C : un carré tourné, un rectangle allongé et un triangle rectangle.',
 'triangle_4_3_corrige':'Construction corrigée : triangle ABC rectangle en A, avec AB de 4 cm et AC de 3 cm.',
 'pentagone':'Polygone fermé à cinq côtés droits sans croisement, présenté sans nom pour le reconnaître.',
 'cercle_O_A':'Cercle de centre O passant par A ; le segment OA représente trois centimètres.',
 'points_alignes':'Trois points A, B et C sur un même trait oblique ; les lettres sont décalées du trait.',
 'milieu_6_corrige':'Segment AB partagé en son milieu M : AM et MB mesurent chacun trois centimètres.',
 'carre_oblique_a_reproduire':'Carré ABCD oblique sur un quadrillage et quadrillage de reproduction avec le seul départ A.',
 'rectangle_6_3':'Rectangle ABCD de six centimètres sur trois, avec codage des quatre angles droits.',
 'rectangle_5_3_corrige':'Rectangle ABCD construit : AB de cinq centimètres, AD de trois et quatre angles droits.',
 'rectangle_deux_cotes':'Début de rectangle : seuls AB de quatre centimètres et AD de deux centimètres sont tracés.',
 'triangle_a_reproduire':'Triangle ABC sur un quadrillage : quatre carreaux horizontalement et trois verticalement.',
 'carre_diagonale_corrige':'Carré ABCD de trois centimètres de côté, partagé par la diagonale AC en deux triangles.',
 'rectangle_cercle_corrige':'Rectangle ABCD de six centimètres sur deux et cercle de centre A passant par D.',
 'pyramide':'Pyramide à base carrée, avec la liaison vers le sommet arrière représentée en pointillés.',
 'cube':'Cube en perspective : les arêtes cachées sont représentées en pointillés.'}
for code,figs in F.items():
 d=next(ROOT.glob(f'{code:02}_*'))
 (d/'figures/figures.py').write_text('# -*- coding: utf-8 -*-\nFIGURES = '+repr(figs)+'\nTOLERE = {}\n',encoding='utf-8')
 def im(name):
  details={'regle_2_9':'Règle graduée en centimètres et segment entre les graduations 2 et 9.','regle_1_8':'Règle graduée en centimètres et segment entre les graduations 1 et 8.','six_solides':'Six solides A à F : cube, pavé, boule, cylindre, cône et pyramide à base carrée.','faces_pyramide':'Modèle réduit : un carré entouré de quatre triangles identiques, à plier le long des côtés du carré.','angles_droit_aigu_obtus':'Trois ouvertures d’angles A, B et C à comparer avec le coin de l’équerre.','plan_depart':'Quadrillage : départ D et petite flèche indiquant la direction initiale vers le haut.','trajet_2_1_corrige':'Trajet depuis D : deux cases vers le haut puis une case vers la droite.','assemblage_trois_cubes':'Assemblage de deux cubes côte à côte au sol et d’un troisième au-dessus du cube gauche.'}
  return {'fichier':name+'.png','alt':details.get(name,ALTS.get(name,''))}
 corr={'cours':{'nouveau':{'1':im(courses[code])}},'fiches':{'nouvelle':{}},'exercices':{}}
 if code==24:corr['cours']['nouveau']['2']=im('horloges_8_30_8_45')
 for e in json.loads((d/'donnees_exercices_root.json').read_text(encoding='utf-8')):
  if e['figures']:corr['exercices'][e['id']]={k:im(v.removesuffix('.png')) for k,v in e['figures'].items()}
 for owners in corr.values():
  for images in owners.values():
   for i in images.values():assert i['fichier'].removesuffix('.png') in figs,i
 (d/'figures/correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,len(figs),'figures définies')
