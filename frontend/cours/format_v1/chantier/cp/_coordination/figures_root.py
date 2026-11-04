"""Figures vectorielles CP21–28 ; données explicites, gabarits réutilisés, style officiel."""
from commun_redaction import ROOT
import json,math
B=chr(92)
def tex(s):return s.replace('@',B)
def node(x,y,t,opts=''):return tex(f'@node[{opts}] at ({x},{y}) {{{t}}};\n')
def pic(s,opts=''):return tex('@begin{tikzpicture}[line width=1pt,text=otInk'+(','+opts if opts else '')+']\n'+s+'\n@end{tikzpicture}')
def line(points,opts='otNavy'):return tex('@draw['+opts+'] '+'--'.join(f'({x},{y})' for x,y in points)+';\n')
def poly(points,opts='otNavy'):return line(points+[points[0]],opts)
def dot(x,y):return tex(f'@fill[otNavy] ({x},{y}) circle (1.5pt);')
def cross(x,y,color='otNavy'):return line([(x-.065,y-.065),(x+.065,y+.065)],color)+line([(x-.065,y+.065),(x+.065,y-.065)],color)
def scope(s,x,y,opts=''):return tex(f'@begin{{scope}}[shift={{({x},{y})}}'+(','+opts if opts else '')+']')+s+tex('@end{scope}')
def caption(s,t,y=-.7):return s+node(3.2,y,t,'font=@large,text=otGreenDark') if t else s
def money_body(values):
 s=''
 for i,v in enumerate(values):
  x=i*2.05
  if v>=5:s+=tex(f'@draw[otNavy,fill=otNavy!7,rounded corners=2pt] ({x-.78},-.47) rectangle ({x+.78},.47);')
  else:s+=tex(f'@draw[otNavy,fill=otOrange!12] ({x},0) circle (.57);')
  s+=node(x,0,str(v)+' €','font=@Large')
 return s
def money(values,total=False,title=''):
 s=money_body(values)
 if total:s+=node((len(values)-1)*1.025,-1.05,str(sum(values))+' € en tout','font=@large,text=otGreenDark')
 if title:s+=node((len(values)-1)*1.025,1,title,'font=@large')
 return pic(s)
def money_pair(correct=False):
 s=scope(money_body([10]),0,1.8)+node(-1.05,1.8,'A','font=@large')+scope(money_body([2]*4),0,0)+node(-1.05,0,'B','font=@large')
 if correct:s+=node(3,-1.1,'A : 10 € ; B : 8 €','font=@large,text=otGreenDark')
 return pic(s)
def bar(total,a,left,right,top=None,title=''):
 x=7*a/total;s=tex(f'@draw[otNavy,fill=otNavy!6] (0,0) rectangle ({x},.65); @draw[otGreenDark,fill=otGreen!10] ({x},0) rectangle (7,.65);')
 s+=node(x/2,.325,left,'font=@large')+node((x+7)/2,.325,right,'font=@large,text=otGreenDark')
 s+=line([(0,.83),(0,1.02),(7,1.02),(7,.83)],'otMuted')+node(3.5,1.43,top or str(total)+' €','font=@large')
 if title:s+=node(3.5,-.55,title,'font=@large,text=otGreenDark')
 return pic(s)
def ruler(a,b=None,correct=False):
 s=tex('@draw[otNavy!20,fill=otNavy!4] (0,0) rectangle (7,-.8);')
 for i in range(21):
  x=i*.35;s+=line([(x,0),(x,-(.28 if i%2==0 else .15))],'otMuted,line width=.6pt')
  if i%2==0:s+=node(x,-.55,str(i//2),'font=@large')
 if b is not None:
  s+=line([(a*.7,.52),(b*.7,.52)],'otGreenDark,line width=2.2pt')
  for v in (a,b):s+=line([(v*.7,.05),(v*.7,.7)],'otMuted,densely dashed')+node(v*.7,1.05,str(v)+' cm','font=@large')
  if correct:s+=node(3.5,-1.35,str(b-a)+' cm entre les deux extrémités','font=@large,text=otGreenDark')
 else:s+=cross(0,.52)+node(0,1.02,'$A$','font=@large')
 return pic(s)
def bands(correct=False,report=False):
 s='';values=[5,7] if report else [5,3,7];labels=['A','B'] if report else ['A','B','C']
 for i,(n,l) in enumerate(zip(values,labels)):
  y=-i*1.15;s+=tex(f'@draw[otNavy,fill=otNavy!7] (0,{y}) rectangle ({n*.8},{y+.5});')+node(-.45,y+.25,l,'font=@large')
  if not report:
   for k in range(1,n):s+=line([(k*.8,y),(k*.8,y+.5)],'otMuted,line width=.6pt')
 if correct:s+=node(2.8,-len(values)*1.15-.05,'B dépasse A' if report else 'B, puis A, puis C','font=@large,text=otGreenDark')
 return pic(s)
def length_bar(total,parts,labels,correct=False,title=''):
 s='';x=0
 for p,l in zip(parts,labels):
  w=7*p/total;s+=tex(f'@draw[otNavy,fill=otNavy!6] ({x},0) rectangle ({x+w},.7);')+node(x+w/2,.35,l,'font=@large');x+=w
 s+=node(3.5,1.2,title,'font=@large')
 if correct:s+=node(3.5,-.6,'Vérifie avec les longueurs indiquées','font=@small,text=otGreenDark')
 return pic(s)
def objects_length(correct=False):
 s=poly([(0,1.4),(2.7,1.4),(3,1.55),(2.7,1.7),(0,1.7)])+line([(0,1.55),(2.7,1.55)],'otOrange')+node(1.5,.9,'Crayon','font=@large')
 s+=tex('@draw[otNavy,fill=otNavy!5] (4.7,0) rectangle (6.8,3.6); @fill[otOrange] (6.45,1.7) circle (.07);')+node(5.75,-.45,'Porte','font=@large')
 if correct:s+=node(1.5,.25,'cm','font=@large,text=otGreenDark')+node(5.75,-1,'m','font=@large,text=otGreenDark')
 return pic(s)
def metre(correct=False):
 s=tex('@draw[otNavy,fill=otNavy!5] (0,0) rectangle (7,.5);')
 for i in range(11):
  s+=line([(i*.7,0),(i*.7,.5)],'otMuted,line width=.6pt')+node(i*.7,-.4,str(i*10),'font=@small')
 s+=node(3.5,1.02,'1 m','font=@large')+node(7.8,-.4,'cm','font=@small')
 if correct:s+=node(3.5,-1,'1 m = 100 cm','font=@large,text=otGreenDark')
 return pic(s)
def balance_body(state='equal',labels=('A','B'),cubes=False):
 delta={'equal':0,'left':-.4,'right':.4}[state];s=tex('@draw[otNavy,fill=otNavy!8] (2.7,-.55)--(3.3,-.55)--(3,2.6)--cycle;')+line([(.4,2.6+delta),(5.6,2.6-delta)],'otNavy,line width=2pt')
 for x,d,l in [(1,delta,labels[0]),(5,-delta,labels[1])]:
  y=.35+d;s+=line([(x-.55,2.6+d),(x-.8,y),(x+.8,y),(x+.55,2.6+d)],'otMuted')+line([(x-.9,y),(x+.9,y)],'otNavy,line width=1.5pt')
  if cubes and x==5:
   for k in range(3):s+=tex(f'@draw[otGreenDark,fill=otGreen!10] ({x-.68+k*.45},{y+.02}) rectangle ({x-.25+k*.45},{y+.47});')
  elif l:
   half=.65 if len(l)>1 else .4
   s+=tex(f'@draw[otNavy,fill=otNavy!7,rounded corners=2pt] ({x-half},{y+.02}) rectangle ({x+half},{y+.9});')+node(x,y+.47,l,'font=@small' if len(l)>1 else 'font=@large')
 return s
def balance(state='equal',correct=False,labels=('A','B'),cubes=False):
 s=balance_body(state,labels,cubes)
 if correct:
  label=('Masses égales' if state=='equal' else labels[0 if state=='left' else 1]+' est plus lourd')
  if cubes:label='Un exemple après essais'
  s+=node(3,-1.05,label,'font=@large,text=otGreenDark')
 return pic(s)
def comparisons(equal=False):
 return pic(balance_body('equal' if equal else 'left',('A','B'))+scope(balance_body('left',('C','A') if equal else ('B','C')),0,-4.4))
def ordered_boxes():
 s=''
 for x,l in [(0,'C'),(2.3,'B'),(4.6,'A')]:s+=tex(f'@draw[otNavy,fill=otNavy!5] ({x},0) rectangle ({x+1.3},1.3);')+node(x+.65,.65,l,'font=@Large')
 s+=node(3,-.65,'De la plus légère à la plus lourde','font=@large,text=otGreenDark')
 return pic(s)
def boxes_sizes(correct=False):
 s=tex('@draw[otNavy,fill=otNavy!5] (0,0) rectangle (2.5,3); @draw[otNavy,fill=otNavy!5] (4,0) rectangle (5.5,1.5);')+node(1.25,-.45,'Vide','font=@large')+node(4.75,-.45,'Cailloux','font=@large')
 for x,y in [(4.35,.35),(4.8,.55),(5.15,.35)]:s+=tex(f'@fill[otMuted] ({x},{y}) circle (.13);')
 if correct:s+=node(2.8,-1.1,'Il faut comparer les masses','font=@large,text=otGreenDark')
 return pic(s)
def clock_body(h=None,minute=True):
 s=tex('@draw[otNavy] (0,0) circle (1.75);')
 for i in range(12):s+=tex(f'@draw[otMuted] ({90-i*30}:1.58)--({90-i*30}:1.72);')
 for i in range(1,13):s+=node(round(1.32*math.cos(math.radians(90-30*i)),5),round(1.32*math.sin(math.radians(90-30*i)),5),str(i),'font=@large')
 if h is not None:
  s+=tex(f'@draw[otNavy,line width=2pt,-{{Stealth[length=2mm]}}] (0,0)--({90-30*(h%12)}:.78);')
  if minute:s+=tex('@draw[otGreenDark,line width=1.4pt,-{Stealth[length=2mm]}] (0,0)--(90:1.06);')
  s+=dot(0,0)
 return s
def clock(h=None,correct=False,title='',minute=True):
 s=clock_body(h,minute)
 if title or correct:s+=node(0,-2.2,title or str(h)+' heures','font=@large,text=otGreenDark')
 return pic(s)
def clocks(hours,correct=False,labels=('A','B')):
 s=''
 for x,h,l in zip((0,4.3),hours,labels):
  t=clock_body(h)+node(0,2.15,l,'font=@large')
  if correct:t+=node(0,-2.2,str(h)+' heures','font=@large,text=otGreenDark')
  s+=scope(t,x,0)
 return pic(s)

F={21:{'monnaie_8':money([5,2,1]),'monnaie_17':money([10,5,2]),'monnaie_17_corrige':money([10,5,2],True),'monnaie_8_corrige':money([5,2,1],True),'comparer_10_8':money_pair(),'comparer_10_8_corrige':money_pair(True),'banque_10_2':money([10,2],title='En plusieurs exemplaires'),'monnaie_24_corrige':money([10,10,2,2],True),'prix_13_paye_20':bar(20,13,'13 €','?'),'monnaie_7_corrige':bar(20,13,'13 €','7 €',title='13 € + 7 € = 20 €'),'prix_28_avoir_35':bar(35,28,'28 €','?'),'reste_7_corrige':bar(35,28,'28 €','7 €',title='28 € + 7 € = 35 €'),'prix_4_9':bar(13,4,'4 €','9 €',top='Total ?'),'payer_13_corrige':bar(13,4,'4 €','9 €',top='13 €',title='4 € + 9 € = 13 €'),'billets_20_10':money([20,10]),'manque_6_corrige':bar(36,30,'30 €','6 €',title='30 € + 6 € = 36 €'),'magasin_prix_choisi':bar(20,10,'Prix choisi','?',top='20 €'),'monnaie_8_exemple':bar(20,12,'12 €','8 €',title='Exemple : 12 € + 8 € = 20 €')},
22:{'regle_0_6':ruler(0,6),'regle_0_5':ruler(0,5),'regle_0_5_corrige':ruler(0,5,True),'bandes_5_3_7':bands(),'bandes_5_3_7_corrige':bands(True),'regle_a_tracer_7':ruler(0),'segment_7_corrige':ruler(0,7,True),'regle_2_8':ruler(2,8),'regle_2_8_corrige':ruler(2,8,True),'crayon_porte':objects_length(),'crayon_porte_corrige':objects_length(True),'bande_metre':metre(),'bande_metre_corrige':metre(True),'bande_12_coupe_4':length_bar(12,[4,8],['4 cm','?'],title='12 cm avant la coupe'),'bande_8_corrige':length_bar(12,[4,8],['4 cm','8 cm'],True,'12 cm = 4 cm + 8 cm'),'rubans_8_6':length_bar(14,[8,6],['8 cm','6 cm'],title='Longueur totale ?'),'rubans_14_corrige':length_bar(14,[8,6],['8 cm','6 cm'],True,'14 cm en tout'),'reports_A_B':bands(report=True),'reports_A_B_corrige':bands(True,True)},
23:{'balance_A_lourde':balance('left'),'balance_A_lourde_corrige':balance('left',True),'balance_B_lourde':balance('right'),'balance_B_lourde_corrige':balance('right',True),'balance_egale':balance(),'balance_egale_corrige':balance(correct=True),'boites_tailles':boxes_sizes(),'boites_tailles_corrige':boxes_sizes(True),'comparaisons_A_B_C':comparisons(),'ordre_C_B_A':ordered_boxes(),'A_egal_B_C_lourd':comparisons(True),'C_plus_lourd_B':balance('left',True,('C','B')),'balance_boite_cubes':balance('left',labels=('Boîte','')),'balance_exemple_cubes':balance(correct=True,labels=('Boîte',''),cubes=True)},
24:{'cadran_vierge':clock(),'horloge_8':clock(8),'horloges_4_9':clocks([4,9]),'horloges_4_9_corrige':clocks([4,9],True),'horloge_6_corrige':clock(6,True),'horloge_11_corrige':clock(11,True),'horloge_8_sans_grande':clock(8,minute=False),'horloge_8_corrige':clock(8,True),'horloge_12':clock(12),'horloge_midi_corrige':clock(12,title='12 heures : midi'),'horloge_8_matin_corrige':clock(8,title='8 heures du matin'),'horloges_7_9':clocks([7,9],labels=('Lever','Classe')),'horloges_7_9_corrige':clocks([7,9],True,('Lever','Classe')),'horloge_2_corrige':clock(2,True),'horloge_5':clock(5),'horloge_5_corrige':clock(5,True)}}

# GEOMETRIE_CP : définitions ajoutées ici, avant l’installation des fichiers.
from geometrie_figures_root import construire
F[23]['balance_B_lourde_corrige']=balance('left',True,('B','A'))
F.update(construire(globals()))
COURSE={21:'monnaie_8_corrige',22:'regle_0_6',23:'balance_A_lourde_corrige',24:'horloge_8_corrige',25:'formes_corrige',26:'rectangle_4_2_cours',27:'cinq_solides_corrige',28:'trajet_2_1_corrige'}
ALTS={
'monnaie_8':'Un billet de5euros et deux pièces, de2euros et de1euro.','monnaie_17':'Deux billets de10euros et de5euros, puis une pièce de2euros.','monnaie_17_corrige':'Correction : les deux billets de10et5euros et la pièce de2euros représentent17euros.','monnaie_8_corrige':'Correction :5euros,2euros et1euro réunis font8euros.','comparer_10_8':'A possède un billet de10euros ; B possède quatre pièces de2euros.','comparer_10_8_corrige':'Comparaison corrigée : A possède10euros ; les quatre pièces de B valent8euros.','banque_10_2':'Types de monnaie disponibles en plusieurs exemplaires : billet de10euros et pièce de2euros.','monnaie_24_corrige':'Correction : deux billets de10euros et deux pièces de2euros, soit24euros.','prix_13_paye_20':'Barre d’un paiement de20euros : prix13euros et monnaie inconnue.','monnaie_7_corrige':'Correction :13euros de prix et7euros rendus reforment20euros.','prix_28_avoir_35':'Barre de35euros disponibles, dont28euros dépensés et un reste à chercher.','reste_7_corrige':'Correction :28euros dépensés et7euros restants reforment35euros.','prix_4_9':'Deux prix de4euros et9euros, avec le total à chercher.','payer_13_corrige':'Correction : les prix de4euros et9euros donnent13euros.','billets_20_10':'Deux billets :20euros et10euros.','manque_6_corrige':'Correction :30euros disponibles et6euros manquants donnent le prix de36euros.','magasin_prix_choisi':'Paiement de20euros : le prix est à choisir et la monnaie à compléter.','monnaie_8_exemple':'Exemple corrigé du magasin : prix12euros, monnaie8euros, paiement20euros.',
'bandes_5_3_7':'Trois bandes A,B,C alignées au départ, partagées en unités de dessin égales.','bandes_5_3_7_corrige':'Correction du rangement des bandes : B, puis A, puis C.','regle_a_tracer_7':'Règle graduée en centimètres et point A au départ ; le segment reste à tracer.','segment_7_corrige':'Correction du tracé : segment allant du zéro à la graduation7cm.','crayon_porte':'Un crayon et une porte : deux objets pour choisir entre centimètres et mètres.','crayon_porte_corrige':'Unités adaptées : centimètres pour le crayon, mètres pour la porte.','bande_metre':'Bande d’un mètre partagée en dix intervalles de dix centimètres.','bande_metre_corrige':'Correction : dix morceaux de dix centimètres représentent un mètre, soit cent centimètres.','bande_12_coupe_4':'Bande de12cm séparée en un morceau coupé de4cm et un reste à chercher.','bande_8_corrige':'Correction : une bande de12cm se partage en4cm coupés et8cm restants.','rubans_8_6':'Deux rubans de8cm et6cm placés bout à bout, sans chevauchement.','rubans_14_corrige':'Correction : les rubans de8cm et6cm totalisent14cm.','reports_A_B':'Deux reports de longueurs A et B, alignés à la même extrémité.','reports_A_B_corrige':'Comparaison des reports : B dépasse A, leurs départs étant alignés.',
'balance_A_lourde':'Balance réglée : le plateau de A est plus bas que celui de B.','balance_A_lourde_corrige':'Correction : A est plus lourd, son plateau est le plus bas.','balance_B_lourde':'Balance réglée : le plateau de B est plus bas que celui de A.','balance_B_lourde_corrige':'Correction : B est plus lourd, son plateau est le plus bas.','balance_egale':'Balance réglée avec les boîtes A et B sur des plateaux de même hauteur.','balance_egale_corrige':'Correction : les plateaux au même niveau indiquent des masses égales.','boites_tailles':'Une grosse boîte vide et une petite boîte contenant des cailloux, sans indication de masse.','boites_tailles_corrige':'Deux tailles de boîtes ; il faut comparer les masses plutôt que leur hauteur.','comparaisons_A_B_C':'Deux balances : A est plus lourd que B ; B est plus lourd que C.','ordre_C_B_A':'Rangement corrigé de la plus légère à la plus lourde : C,B,A.','A_egal_B_C_lourd':'Une balance montre A et B égaux ; une seconde montre C plus lourd que A.','C_plus_lourd_B':'Conclusion corrigée : C est plus lourd que B.','balance_boite_cubes':'Une boîte sur un plateau et le plateau opposé vide, à compléter avec des cubes.','balance_exemple_cubes':'Un exemple après essais : une boîte est équilibrée par trois cubes identiques.',
'cadran_vierge':'Cadran numéroté de1à12, sans aiguilles, à reproduire.','horloge_8_sans_grande':'Cadran : la petite aiguille pointe sur8 ; la grande aiguille manque.','horloge_midi_corrige':'Cadran corrigé : les deux aiguilles pointent sur12, il est midi.','horloge_8_matin_corrige':'Cadran corrigé indiquant huit heures du matin.'}
ALTS.update({
'formes_quiz':'Quatre formes A, B, C, D : carré tourné, triangle, disque et rectangle.', 'formes_corrige':'Formes nommées : A carré tourné, B triangle, C disque, D rectangle.',
'triangle_carre':'Un triangle et un carré, avec leurs contours distincts.', 'triangle_carre_corrige':'Triangle : trois côtés et sommets ; carré : quatre côtés et sommets marqués.',
'points_AB':'Deux points A et B à relier à la règle.', 'segment_AB_corrige':'Les points A et B reliés par un segment droit.',
'points_alignes':'Trois points A, B et C à tester avec le bord de la règle.', 'alignement_corrige':'Une même ligne droite passe par A, B et C.',
'points_non_alignes':'Trois points A, B et C ; B est au-dessus de la ligne passant par A et C.', 'non_alignement_corrige':'La ligne passant par A et C ne passe pas par B : ils ne sont pas alignés.',
'sommets_triangle':'Trois points A, B et C non alignés pour construire un triangle.', 'triangle_trace_corrige':'Les trois points A, B et C reliés pour former un triangle fermé.',
'carre_sans_nom':'Une figure à quatre côtés de même longueur et quatre coins droits.', 'carre_corrige':'La figure est reconnue et nommée carré.',
'points_prolonger':'Deux points A et B avant le tracé à prolonger.', 'droite_prolongee_corrige':'La ligne droite passant par A et B est prolongée des deux côtés.',
'disque_boule':'Un modèle de disque plat et un modèle de boule en volume.', 'disque_boule_corrige':'Comparaison corrigée : disque plat et boule en volume.',
'rectangle_4_2_cours':'Rectangle de quatre carreaux de longueur et deux de largeur sur quadrillage.',
'copier_rectangle_4_2':'Un rectangle de quatre carreaux sur deux et un quadrillage vide pour la copie.', 'copier_rectangle_4_2_corrige':'Le rectangle de quatre carreaux sur deux est reproduit sur le second quadrillage.',
'grille_vierge':'Quadrillage vide pour construire la figure demandée.', 'carre_2_corrige':'Carré de deux carreaux de côté, tracé sur les lignes du quadrillage.',
'rectangle_partiel_4_2':'Rectangle à compléter : côté du haut de quatre carreaux et côté gauche de deux carreaux.', 'rectangle_4_2_corrige':'Le rectangle de quatre carreaux sur deux est fermé par les deux côtés manquants.',
'carre_partiel_3':'Un côté de trois carreaux d’un carré à compléter.', 'carre_3_corrige':'Le carré de trois carreaux de côté est complété sur le quadrillage.',
'copier_triangle_4_3':'Triangle ABC : de A à B quatre carreaux à droite, puis de B à C trois vers le haut ; quadrillage à compléter.', 'copier_triangle_4_3_corrige':'Le triangle ABC est reproduit avec les mêmes écarts sur le second quadrillage.',
'rectangle_5_2_corrige':'Rectangle de cinq carreaux sur deux, suivant les lignes du quadrillage.', 'carre_4_partage_corrige':'Carré de quatre carreaux partagé au milieu en deux rectangles de deux carreaux sur quatre.',
'triangles_a_assembler':'Deux triangles identiques à assembler bord contre bord.', 'triangles_rectangle_corrige':'Les deux triangles sont assemblés en un rectangle, leur côté commun étant la diagonale.',
'quatre_lignes':'Quatre lignes verticales délimitent trois espaces.', 'cinq_lignes_corrige':'Cinq lignes verticales délimitent les quatre espaces demandés.',
'cinq_solides':'Cinq solides A à E : cube, pavé, boule, cylindre et cône.', 'cinq_solides_corrige':'Les cinq solides sont nommés : cube, pavé, boule, cylindre, cône.',
'cube':'Vue d’un cube montrant trois de ses faces.', 'cube_faces_corrige':'Un cube et les six faces carrées qui le composent.',
'pave':'Vue d’un pavé droit montrant trois de ses faces.', 'pave_faces_corrige':'Un pavé droit et ses six faces rectangulaires, identiques deux par deux.',
'cube_et_pave':'Un cube et un pavé droit allongé à comparer.', 'cube_et_pave_corrige':'Les deux objets sont nommés cube et pavé droit.',
'six_carres':'Six carrés identiques, modèles réduits des faces à assembler.', 'six_rectangles':'Trois paires de rectangles : six sur quatre, six sur deux, quatre sur deux centimètres ; modèles réduits.',
'trois_cubes':'Assemblage de deux cubes côte à côte en bas et d’un cube au-dessus de celui de gauche.', 'trois_cubes_corrige':'Deux cubes en bas et un au-dessus donnent trois cubes au total.',
'cube_vue_trois_faces':'Vue opaque d’un cube : trois faces visibles, trois faces cachées.',
'positions_A_B_C':'Trois objets A, B, C alignés de gauche à droite.', 'positions_A_B_C_corrige':'Après échange de A et C, la rangée devient C, B, A ; B reste entre les deux.',
'materiel_cahier':'Un cahier, une gomme et un crayon séparés, avant leur placement.', 'gomme_cahier_crayon_corrige':'Disposition corrigée vue de côté : gomme sur le cahier, crayon sous le cahier.',
'zones_a_completer':'Deux zones vides côte à côte pour dessiner les formes.', 'rond_gauche_carre_corrige':'Un rond est dessiné à gauche d’un carré.',
'depart_haut':'Pion en D, orienté vers le haut, sur un quadrillage.', 'trajet_2_1_corrige':'Depuis D, trajet de deux cases vers le haut puis une à droite, jusqu’à A.',
'regard_droite':'Pion en D orienté vers la droite du dessin.', 'tourner_gauche_corrige':'Après le virage à gauche sur place, le pion reste en D et regarde vers le haut.',
'depart_reculer':'Pion en D orienté vers le haut avant de reculer.', 'reculer_corrige':'Le pion recule d’une case vers le bas tout en gardant le regard orienté vers le haut.',
'plan_classe':'Exemple de plan de classe : porte, tableau et deux tables.', 'plan_cachette_corrige':'Sur le plan, une croix près de la première table indique un exemple de cachette.',
'trajet_a_coder':'Départ D orienté vers le haut, arrivée A deux cases au-dessus et une à droite.', 'trajet_1_2_1_corrige':'Trajet : une case vers le haut, deux à droite, une vers le bas ; arrivée deux cases à droite de D, regard vers le bas.'})
def alt(name):
 import re
 if name in ALTS:s=ALTS[name]
 elif name.startswith('regle_'):
  a,b=re.search(r'regle_(\d+)_(\d+)',name).groups();s=f'Règle graduée en centimètres et segment repéré entre les graduations {a} et {b}.'
 elif name.startswith('horloges_'):
  hs=re.search(r'horloges_(\d+)_(\d+)',name).groups();s=f'Deux cadrans : petites aiguilles sur {hs[0]} et {hs[1]}, grandes aiguilles sur12.'
 elif name.startswith('horloge_'):
  h=re.search(r'horloge_(\d+)',name)[1];s=f'Cadran : petite aiguille sur{h} et grande aiguille sur12.'
 else:raise AssertionError(('Texte alternatif manquant',name))
 return re.sub(r'(?<=\d)(?=[A-Za-zÀ-ÿ€])|(?<=[A-Za-zÀ-ÿ])(?=\d)',' ',s)
def installer(codes):
 for code in codes:
  d=next(ROOT.glob(f'{code:02}_*'));data=json.loads((d/'donnees_exercices_root.json').read_text(encoding='utf-8'))
  names={COURSE[code]}|{name.removesuffix('.png') for e in data for name in e['figures'].values()}
  unique={};aliases={};seen={}
  for name,s in F[code].items():
   if name not in names:continue
   if s not in seen:seen[s]=name;unique[name]=s
   aliases[name]=seen[s]
  assert names<=set(aliases),(code,names-set(aliases))
  def im(name):return {'fichier':aliases[name]+'.png','alt':alt(name)}
  corr={'cours':{'nouveau':{'1':im(COURSE[code])}},'fiches':{'nouvelle':{'1':im(COURSE[code])}},'exercices':{}}
  if code==25:
   corr['cours']['nouveau']['2']=im('alignement_corrige');corr['fiches']['nouvelle']['2']=im('alignement_corrige')
  for e in data:corr['exercices'][e['id']]={pos:im(name.removesuffix('.png')) for pos,name in e['figures'].items()}
  (d/'figures/figures.py').write_text('# -*- coding: utf-8 -*-\nFIGURES = '+repr(unique)+'\nTOLERE = {}\n',encoding='utf-8')
  (d/'figures/correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print(code,len(unique),'figures définies',flush=True)
if __name__=='__main__':
 import sys
 installer([int(x) for x in sys.argv[1:]] or sorted(F))
