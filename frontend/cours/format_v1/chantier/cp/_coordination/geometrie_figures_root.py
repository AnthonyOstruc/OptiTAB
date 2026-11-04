"""Modèles géométriques CP : coordonnées et corrections explicites."""
def construire(api):
 globals().update({k:api[k] for k in ('tex','node','pic','line','poly','cross','scope','dot')})
 return definitions()

def rect(x,y,w,h,color='otNavy',fill='otNavy!5'):
 return tex(f'@draw[{color},fill={fill}] ({x},{y}) rectangle ({x+w},{y+h});')
def title(s,t,x=3,y=-.7):return s+node(x,y,t,'font=@large,text=otGreenDark')
def shapes(c=False):
 s=scope(poly([(0,0),(1.7,0),(1.7,1.7),(0,1.7)],'otNavy,fill=otNavy!6'),1.2,4.5,'rotate=25')
 s+=poly([(4.4,4.2),(6.6,4.2),(5.2,6.2)],'otNavy,fill=otOrange!10')
 s+=tex('@draw[otNavy,fill=otGreen!12] (1.4,1.6) circle (.9);')+rect(4.3,.8,2.7,1.5)
 for x,y,l,n in [(1.5,3.5,'A','Carré'),(5.5,3.5,'B','Triangle'),(1.4,.15,'C','Disque'),(5.65,.15,'D','Rectangle')]:
  s+=node(x,y,l+(' : '+n if c else ''),'font=@large'+(',text=otGreenDark' if c else ''))
 return pic(s)
def triangle_square(c=False):
 s=poly([(0,0),(2,0),(.8,2)],'otNavy,fill=otNavy!5')+rect(4,0,2,2)
 s+=node(1,2.6,'Triangle','font=@large')+node(5,2.6,'Carré','font=@large')
 if c:
  for x,y in [(0,0),(2,0),(.8,2),(4,0),(6,0),(6,2),(4,2)]:s+=tex(f'@fill[otGreenDark] ({x},{y}) circle (2pt);')
  s+=node(1,-.7,'3 côtés, 3 sommets','font=@large,text=otGreenDark')+node(5,-.7,'4 côtés, 4 sommets','font=@large,text=otGreenDark')
 return pic(s)
def points(kind,c=False):
 pts={'AB':[(0,0),(6,2)],'alignes':[(0,0),(3,1),(6,2)],'non_alignes':[(0,0),(3,2),(6,0)],'triangle':[(0,0),(4,0),(1.3,2.8)],'prolonger':[(0,1),(4,2)]}[kind]
 s=''
 if c:
  path={'AB':pts,'alignes':[pts[0],pts[-1]],'non_alignes':[pts[0],pts[-1]],'triangle':pts+[pts[0]],'prolonger':[(-1,.75),(5,2.25)]}[kind]
  s+=line(path,'otGreenDark,line width=1.5pt')
 for i,(x,y) in enumerate(pts):s+=cross(x,y)+node(x,y+(.5 if kind in ('non_alignes','triangle') and i==len(pts)-1 or kind=='non_alignes' and i==1 else -.5),chr(65+i),'font=@large')
 if c and kind in ('alignes','non_alignes'):s+=node(3,-1.2,'Points '+('alignés' if kind=='alignes' else 'non alignés'),'font=@large,text=otGreenDark')
 return pic(s)
def square(c=False):return pic(rect(0,0,2.5,2.5)+ (node(1.25,-.6,'Carré','font=@large,text=otGreenDark') if c else ''))
def sphere(x=0,y=0,r=1):return tex(f'@draw[otNavy,fill=otNavy!7] ({x},{y}) circle ({r}); @draw[otMuted,dashed] ({x},{y}) ellipse ({r} and {r*.3});')
def disk_ball(c=False):
 s=tex('@draw[otNavy,fill=otOrange!10] (0,0) circle (1);')+sphere(4,0)
 if c:s+=node(0,-1.6,'Disque : plat','font=@large,text=otGreenDark')+node(4,-1.6,'Boule : en volume','font=@large,text=otGreenDark')
 return pic(s)
def grid_body():return tex('@draw[step=.55cm,otMuted!45,line width=.4pt] (0,0) grid (3.3,3.3);')
def grid_path(pts,c=False):return line([(x*.55,y*.55) for x,y in pts],'otGreenDark,line width=1.6pt' if c else 'otNavy,line width=1.4pt')
def grid(c=False,kind='blank'):
 s=grid_body()
 paths={'rect42':[(1,1),(5,1),(5,3),(1,3),(1,1)],'square2':[(1,1),(3,1),(3,3),(1,3),(1,1)],'square3':[(1,1),(4,1),(4,4),(1,4),(1,1)],'rect52':[(0,1),(5,1),(5,3),(0,3),(0,1)],'square4':[(1,1),(5,1),(5,5),(1,5),(1,1)]}
 if kind=='partial42':s+=grid_path([(1,1),(1,3),(5,3)])+(grid_path(paths['rect42'],True) if c else '')
 elif kind=='partial3':s+=grid_path([(1,4),(4,4)])+(grid_path(paths['square3'],True) if c else '')
 elif kind in paths:s+=grid_path(paths[kind],c)
 if kind=='square4':s+=grid_path([(3,1),(3,5)],True)
 return pic(s)
def copy_grid(triangle=False,c=False):
 pts=[(1,1),(5,1),(5,4),(1,1)] if triangle else [(1,1),(5,1),(5,3),(1,3),(1,1)]
 s=''
 for dx,completed,label in [(0,True,'Modèle'),(4.5,c,'Copie')]:
  a=grid_body()
  if completed:a+=grid_path(pts,c and dx>0)
  if triangle:
   for k,(x,y) in enumerate(pts[:3]):
    if completed or k==0:a+=cross(x*.55,y*.55)+node(x*.55+(.24 if k else -.24),y*.55+(.25 if k==2 else -.25),chr(65+k),'font=@small')
  a+=node(1.65,-.5,label,'font=@large');s+=scope(a,dx,0)
 return pic(s)
def triangles(c=False):
 if c:return pic(poly([(0,0),(4,0),(4,2),(0,2)],'otGreenDark,fill=otGreen!8')+line([(0,0),(4,2)],'otNavy')+node(2,-.6,'Un rectangle','font=@large,text=otGreenDark'))
 return pic(poly([(0,0),(4,0),(4,2)],'otNavy,fill=otNavy!6')+poly([(0,3),(4,5),(0,5)],'otNavy,fill=otOrange!10'))
def intervals(c=False):
 n=4 if c else 3;s=rect(0,0,n,1)
 for x in range(1,n):s+=line([(x,0),(x,1)])
 if c:s+=node(n/2,-.6,'5 lignes : 4 espaces','font=@large,text=otGreenDark')
 return pic(s)
def solid(w=2,h=2,d=.6):
 return poly([(0,0),(w,0),(w,h),(0,h)],'otNavy,fill=otNavy!6')+poly([(0,h),(d,h+d),(w+d,h+d),(w,h)],'otNavy,fill=otNavy!16')+poly([(w,0),(w+d,d),(w+d,h+d),(w,h)],'otNavy,fill=otNavy!10')
def solids(c=False):
 s=scope(solid(1.4,1.4,.5),0,4.2)+scope(solid(2,1.2,.5),3.2,4.2)+sphere(7,5,.75)
 s+=tex('@draw[otNavy,fill=otNavy!6] (.7,.3)--(.7,1.7) arc[start angle=180,end angle=0,x radius=.8,y radius=.25] --(2.3,.3) arc[start angle=0,end angle=-180,x radius=.8,y radius=.25]; @draw[otNavy,fill=otNavy!12] (1.5,1.7) ellipse (.8 and .25);')
 s+=tex('@draw[otNavy,fill=otOrange!10] (4.8,.3)--(5.6,2)--(6.4,.3) arc[start angle=0,end angle=-180,x radius=.8,y radius=.25]; @draw[otMuted,dashed] (4.8,.3) arc[start angle=180,end angle=0,x radius=.8,y radius=.25];')
 for x,y,l,n in [(.8,3.5,'A','Cube'),(4.3,3.5,'B','Pavé'),(7,3.5,'C','Boule'),(1.5,-.4,'D','Cylindre'),(5.6,-.4,'E','Cône')]:s+=node(x,y,l+(' : '+n if c else ''),'font=@large'+(',text=otGreenDark' if c else ''))
 return pic(s)
def cube_pave(c=False):
 s=solid()+scope(solid(3,1.6,.6),4,0)
 if c:s+=node(1,-.6,'Cube','font=@large,text=otGreenDark')+node(5.5,-.6,'Pavé droit','font=@large,text=otGreenDark')
 return pic(s)
def faces(cube=True,c=False):
 s=solid(2 if cube else 3,2 if cube else 1.7,.6) if c else ''
 if cube:
  for i in range(6):s+=rect((4 if c else 0)+(i%2)*1.6,(i//2)*1.6,1.2,1.2,'otGreenDark' if c else 'otNavy')
  s+=node(3 if c else 1.4,-.7,'6 faces carrées' if c else 'Six carrés identiques','font=@large,text=otGreenDark' if c else 'font=@large')
 else:
  for row,(w,h,label) in enumerate([(2.4,1.6,'6 cm sur 4 cm'),(2.4,.8,'6 cm sur 2 cm'),(1.6,.8,'4 cm sur 2 cm')]):
   for col in range(2):s+=rect((4.2 if c else 0)+col*2.8,row*2.8,w,h,'otGreenDark' if c else 'otNavy')
   if not c:s+=node(2.6,row*2.8-.5,label,'font=@large')
  if c:s+=node(5.5,-.7,'6 faces rectangulaires','font=@large,text=otGreenDark')
 return pic(s)
def three_cubes(c=False):
 s=solid(1.4,1.4,.45)+scope(solid(1.4,1.4,.45),1.4,0)+scope(solid(1.4,1.4,.45),0,1.4)
 if c:s+=node(1.6,-.65,'2 en bas, 1 au-dessus : 3 cubes','font=@large,text=otGreenDark')
 return pic(s)
def positions(c=False):
 s=''
 for x,l in [(0,'C' if c else 'A'),(2,'B'),(4,'A' if c else 'C')]:s+=rect(x,0,1,1)+node(x+.5,.5,l,'font=@Large')
 if c:s+=node(2.5,-.65,'B reste entre A et C','font=@large,text=otGreenDark')
 return pic(s)
def materials(c=False):
 if c:
  s=rect(1,1.3,4,.55)+rect(2.3,1.85,1.2,.6,'otOrange','otOrange!10')+poly([(1.6,.65),(4.3,.65),(4.6,.8),(4.3,.95),(1.6,.95)],'otNavy,fill=otNavy!6')
  s+=node(3,3.1,'Gomme sur le cahier','font=@large,text=otGreenDark')+node(3,-.1,'Crayon sous le cahier','font=@large,text=otGreenDark')
 else:
  s=rect(0,0,2.4,1.5)+rect(3.5,.4,1,.6,'otOrange','otOrange!10')+poly([(5.5,.4),(7.2,.4),(7.5,.55),(7.2,.7),(5.5,.7)])
  for x,l in [(1.2,'Cahier'),(4,'Gomme'),(6.5,'Crayon')]:s+=node(x,-.6,l,'font=@large')
 return pic(s)
def left_shapes(c=False):
 return pic(tex('@draw[otNavy,fill=otOrange!10] (0,0) circle (.9);')+rect(3,-.9,1.8,1.8) if c else rect(-1,-1,2,2,'otMuted','white')+rect(3,-1,2,2,'otMuted','white'))
def route(kind='up',c=False):
 s=tex('@draw[step=1cm,otMuted!45,line width=.4pt] (0,0) grid (5,5);')
 start=(2.5,2.5) if kind=='back' else (1.5,1.5)
 x,y=start;s+=dot(x,y)+node(x-.25,y-.25,'D','font=@small')
 arrow='otNavy,line width=1.7pt,-{Stealth[length=2mm]}'
 if c and kind in ('up','code','last'):
  pts=[start,(1.5,2.5),(3.5,2.5),(3.5,1.5)] if kind=='last' else [start,(1.5,3.5),(2.5,3.5)]
  s+=line(pts,'otGreenDark,line width=1.8pt,-{Stealth[length=2mm]}')
  end=pts[-1];s+=node(end[0]+.25,end[1]+.3,'A','font=@small,text=otGreenDark')
  if kind=='last':s+=line([(3.75,1.65),(3.75,1.2)],arrow)
 elif c and kind=='back':s+=line([start,(2.5,1.5)],'otGreenDark,line width=1.8pt,-{Stealth[length=2mm]}')+line([(2.75,1.4),(2.75,1.9)],arrow)
 elif c and kind=='right':s+=line([start,(x,y+.5)],'otGreenDark,line width=1.8pt,-{Stealth[length=2mm]}')+node(2.5,-.6,'Tourner sur place','font=@large,text=otGreenDark')
 else:
  s+=line([start,(x+.45,y) if kind=='right' else (x,y+.45)],arrow)
  if kind=='code':s+=cross(2.5,3.5)+node(2.75,3.7,'A','font=@small')
 return pic(s)
def classroom(c=False):
 s=rect(0,0,7,5,'otMuted','white')+rect(2.2,4.3,2.6,.25)+node(3.5,3.7,'Tableau','font=@large')
 for x,l in [(1,'Table 1'),(4.7,'Table 2')]:s+=rect(x,1.3,1.5,1.1)+node(x+.75,.75,l,'font=@large')
 s+=line([(0,.6),(.7,.6)],'otOrange,line width=2pt')+node(-.7,.7,'Porte','font=@large,rotate=90')
 if c:s+=cross(3,1.8,'otGreenDark')+node(3.5,-.65,'Croix : exemple de cachette','font=@large,text=otGreenDark')
 return pic(s)
def definitions():
 return {
 25:{'formes_quiz':shapes(),'formes_corrige':shapes(True),'triangle_carre':triangle_square(),'triangle_carre_corrige':triangle_square(True),'points_AB':points('AB'),'segment_AB_corrige':points('AB',True),'points_alignes':points('alignes'),'alignement_corrige':points('alignes',True),'points_non_alignes':points('non_alignes'),'non_alignement_corrige':points('non_alignes',True),'sommets_triangle':points('triangle'),'triangle_trace_corrige':points('triangle',True),'carre_sans_nom':square(),'carre_corrige':square(True),'points_prolonger':points('prolonger'),'droite_prolongee_corrige':points('prolonger',True),'disque_boule':disk_ball(),'disque_boule_corrige':disk_ball(True)},
 26:{'rectangle_4_2_cours':grid(True,'rect42'),'copier_rectangle_4_2':copy_grid(),'copier_rectangle_4_2_corrige':copy_grid(c=True),'grille_vierge':grid(),'carre_2_corrige':grid(True,'square2'),'rectangle_partiel_4_2':grid(kind='partial42'),'rectangle_4_2_corrige':grid(True,'partial42'),'carre_partiel_3':grid(kind='partial3'),'carre_3_corrige':grid(True,'partial3'),'copier_triangle_4_3':copy_grid(True),'copier_triangle_4_3_corrige':copy_grid(True,True),'rectangle_5_2_corrige':grid(True,'rect52'),'carre_4_partage_corrige':grid(True,'square4'),'triangles_a_assembler':triangles(),'triangles_rectangle_corrige':triangles(True),'quatre_lignes':intervals(),'cinq_lignes_corrige':intervals(True)},
 27:{'cinq_solides':solids(),'cinq_solides_corrige':solids(True),'cube':pic(solid()),'cube_faces_corrige':faces(True,True),'pave':pic(solid(3,1.7,.6)),'pave_faces_corrige':faces(False,True),'disque_boule':disk_ball(),'disque_boule_corrige':disk_ball(True),'cube_et_pave':cube_pave(),'cube_et_pave_corrige':cube_pave(True),'six_carres':faces(),'trois_cubes':three_cubes(),'trois_cubes_corrige':three_cubes(True),'cube_vue_trois_faces':pic(solid()),'six_rectangles':faces(False)},
 28:{'positions_A_B_C':positions(),'positions_A_B_C_corrige':positions(True),'materiel_cahier':materials(),'gomme_cahier_crayon_corrige':materials(True),'zones_a_completer':left_shapes(),'rond_gauche_carre_corrige':left_shapes(True),'depart_haut':route(),'trajet_2_1_corrige':route(c=True),'regard_droite':route('right'),'tourner_gauche_corrige':route('right',True),'depart_reculer':route('back'),'reculer_corrige':route('back',True),'plan_classe':classroom(),'plan_cachette_corrige':classroom(True),'trajet_a_coder':route('code'),'trajet_1_2_1_corrige':route('last',True)}}
