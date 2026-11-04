from pathlib import Path
import sys,json,math
BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE/'_coordination'))
from commun_redaction import q,ex,write,table

def block(kind,title,text):return f'::: {kind} {title}\n{text}\n:::'
def picture(body):return '\\begin{tikzpicture}[x=1cm,y=1cm,font=\\large]\n'+body+'\n\\end{tikzpicture}'
def bar(total,part,answer=False):
 w=6;cut=w*part/total
 return picture(f'\\draw[geoTrait,fill=otSky] (0,0) rectangle (6,.65);\n\\draw[geoTrait] ({cut},0)--({cut},.65);\n'+f'\\node[text=otNavy] at (3,1.1) {{{total} en tout}};\n\\node[text=otNavy] at ({cut/2},-.45) {{{part}}};\n\\node[text='+('otGreenDark' if answer else 'otNavy')+f'] at ({(cut+6)/2},-.45) '+'{'+str(total-part if answer else '?')+'};')
def groups(values,blank=False,green=False,firstonly=False):
 body=''
 for i,v in enumerate(values):
  x=(i%3)*2.25;y=-(i//3)*1.65
  body+=f'\\draw[geoTrait] ({x},{y}) rectangle ++(1.9,1.15);\n'
  if not blank:
   for j in range(v):body+=f'\\fill[{"otGreenDark" if green and (not firstonly or i==0) else "otNavy"}] ({x+.3+(j%4)*.4},{y+.3+(j//4)*.48}) circle (.085);\n'
  body+=f'\\node[text=otMuted] at ({x+.95},{y-.27}) '+'{'+f'groupe {i+1}'+'};\n'
 return picture(body)
def story(n,a,b,answer=False):
 vals=[n,n+a,n+a+b];body=''
 for i,v in enumerate(vals):
  x=i*2.5
  body+=f'\\draw[geoTrait,fill=otSky] ({x},0) rectangle ++(1.4,.8);\n\\node[text='+('otGreenDark' if answer and i else 'otNavy')+f'] at ({x+.7},.4) '+'{'+str(v if answer or i==0 else '?')+'};\n'
  if i<2:
   d=[a,b][i];body+=f'\\draw[geoVecteur] ({x+1.5},.4)--({x+2.4},.4);\n\\node[text=otNavy] at ({x+1.95},1.05) '+'{'+('+' if d>=0 else '')+str(d)+'};\n'
 return picture(body)
def rows(points,blank=False):
 body=''
 for i in range(2):
  y=-i*1.4;body+=f'\\draw[geoTrait] (0,{y}) rectangle ++(5,.7);\n'
  if not blank:
   for k in range(points):body+=f'\\fill[otGreenDark] ({.4+k*.65},{y+.35}) circle (.085);\n'
  body+=f'\\node[text=otNavy] at (2.5,{y-.3}) '+'{'+f'rangée {i+1}'+'};\n'
 return picture(body)
def flowers(blank=False):
 body=''
 for i in range(6):
  x=(i%3)*2.25;y=-(i//3)*1.7
  body+=f'\\draw[geoTrait] ({x},{y}) rectangle ++(1.9,1.2);\n\\draw[geoTrait] ({x+.95},{y+.6}) circle (.10);\n'
  if not blank:
   for k in range(5):
    a=math.pi/2+2*math.pi*k/5
    body+=f'\\fill[otGreenDark] ({x+.95+.35*math.cos(a):.5f},{y+.6+.35*math.sin(a):.5f}) circle (.12);\n'
  body+=f'\\node[text=otNavy] at ({x+.95},{y-.27}) '+'{'+f'fleur {i+1}'+'};\n'
 return picture(body)
def chart(labels,values,blank=False,green=False):
 body='';m=max(8,max(values));step=.30
 for i,label in enumerate(labels):
  x=i*2
  for k in range(m):body+=f'\\draw[otRule] ({x},{k*step}) rectangle ++(.8,{step});\n'
  if not blank:
   for k in range(values[i]):body+=f'\\fill[{"otGreenDark" if green else "otNavy"}!65] ({x+.03},{k*step+.025}) rectangle ++(.74,{step-.05});\n'
  body+=f'\\node[text=otNavy] at ({x+.4},-.45) '+'{'+label+'};\n'
 body+=f'\\node[anchor=west,text=otMuted] at (0,{m*step+.45}) '+'{1 case : 1 personne};\n'
 body+=f'\\node[anchor=west,text=otNavy] at (0,{m*step+1}) '+'{'+('Les animaux préférés' if labels[0]=='chat' else 'Les jeux préférés')+'};'
 return picture(body)
def register(figs,corr,i,stem,fig1,fig2,desc):
 figs[stem+'_enonce']=fig1;figs[stem+'_corrige']=fig2
 corr['exercices'][f'nouveau-{i}']={str(k):{'fichier':stem+s+'.png','alt':desc+(' à compléter.' if k==1 else ' complété en vert.')} for k,s in [(1,'_enonce'),(2,'_corrige')]}
def finish(code,title,course,fiche,items,figs,corr,coverage):
 d=next(BASE.glob(f'{code:02}_*'));(d/'figures').mkdir(exist_ok=True)
 canonical={};unique={};aliases={}
 for name,body in figs.items():
  if body not in canonical:canonical[body]=name;unique[name]=body
  aliases[name+'.png']=canonical[body]+'.png'
 for group in corr.values():
  for positions in group.values():
   for spec in positions.values():spec['fichier']=aliases[spec['fichier']]
 figs=unique
 write(code,items)
 (d/'cours_nouveau.txt').write_text('Titre: '+title+'\n<!-- optitab:1 -->\n'+course+'\n',encoding='utf-8')
 (d/'fiche_nouvelle.txt').write_text('Titre: '+title+'\n<!-- optitab:1 -->\n'+fiche+'\n',encoding='utf-8')
 (d/'figures/figures.py').write_text('FIGURES = '+repr(figs)+'\n',encoding='utf-8')
 (d/'figures/correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2),encoding='utf-8')
 (d/'COUVERTURE.md').write_text('# Couverture des neuf activités sources\n\n'+'\n'.join(f'{i}. Source {i} → exercice nouveau-{i} : {s}.' for i,s in enumerate(coverage,1))+'\n\nChaque exercice comporte cinq questions liées, une méthode, une démarche et une réponse pour chaque question.\n',encoding='utf-8')
 (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'cp_problemes_donnees','maj':'2026-11-02'}),encoding='utf-8')

def init(fig):
 return {'modele':fig},{'cours':{'nouveau':{'1':{'fichier':'modele.png','alt':'Exemple de la méthode expliqué dans le cours.'}}},'fiches':{'nouvelle':{'1':{'fichier':'modele.png','alt':'Schéma de la méthode à retenir.'}}},'exercices':{}}

def parties():
 figs,corr=init(bar(18,7,True));items=[]
 data=[('Les billes',20,8,'Il y a 20 billes en tout. 8 sont vertes. Les autres sont jaunes.','billes jaunes'),('Les additions à trou',13,7,'Complète $7+?=13$. Puis complète $24+?=30$.','unités manquantes'),('Les oiseaux',16,9,'16 oiseaux étaient dans un arbre. Il en reste 9. Les autres se sont envolés.','oiseaux envolés'),('Les images du départ',16,4,'J’avais des images. J’en donne 4. Il m’en reste 12.','images au départ'),('Les cubes du départ',21,6,'J’avais des cubes. J’en reçois 6. J’en ai maintenant 21.','cubes au départ'),('Les places libres',50,32,'Un album a 50 places. 32 sont occupées.','places libres'),('Les crayons verts',27,18,'Lina a 27 crayons. 10 sont bleus. 8 sont rouges. Les autres sont verts.','crayons verts'),('Les perles restantes',64,29,'Une boîte contient 64 perles. 29 sont prises. Utilise des dizaines.','perles restantes'),('Une erreur à corriger',19,5,'Un enfant dit : « J’ai donné 5 cartes. Il m’en reste 14. J’en avais donc 9. »','cartes au départ')]
 for i,(name,total,part,intro,obj) in enumerate(data,1):
  ans=total-part;register(figs,corr,i,f'ex{i}',bar(total,part),bar(total,part,True),'Barre du tout et de ses deux parties')
  if i in (4,9):
   remaining=ans
   # Dans ces histoires, le tout initial est précisément l’inconnue.
   figs[f'ex{i}_enonce']=bar(total,part).replace(f'{{{total} en tout}}','{? au départ}').replace('{?};',f'{{{remaining}}};')
   figs[f'ex{i}_corrige']=bar(total,part,True).replace('text=otNavy] at (3,1.1)','text=otGreenDark] at (3,1.1)').replace('text=otGreenDark] at ('+str((6*part/total+6)/2),'text=otNavy] at ('+str((6*part/total+6)/2))
   questions=[q('Combien reste-t-il à la fin ?','Lire la fin de l’histoire.',f'La phrase dit qu’il reste {remaining} objets.',f'Il reste {remaining} objets.'),q('Combien a-t-on donné ?','Repérer ce qui est sorti.',f'On a donné {part} objets. Ils faisaient partie du départ.',f'On a donné {part} objets.'),q('Quel calcul retrouve le départ ?','Remettre les objets donnés.',f'Je réunis les {remaining} objets restants et les {part} objets donnés.',f'Je calcule ${remaining}+{part}$.'),q('Combien y avait-il au départ ?','Additionner les deux parties.',f'${remaining}+{part}={total}$.\n\n[IMAGE_2]',f'Il y avait {total} {obj}.'),q('Vérifie en redonnant les objets.','Rejouer la scène.',f'${total}-{part}={remaining}$. '+('Avec 9 cartes, il resterait $9-5=4$ cartes. 9 ne convient pas.' if i==9 else 'On retrouve bien la quantité de la fin.'),f'${total}-{part}={remaining}$ : le départ est bien {total}.')]
  else:
   knownprompt='Combien de crayons bleus et rouges y a-t-il ensemble ?' if i==7 else 'Quelle quantité est connue dans une partie ?'
   knownstep='$10+8=18$. Je réunis les crayons bleus et rouges.' if i==7 else f'Je lis {part} dans l’histoire. Cette partie est connue.'
   extra=q('Complète aussi $24+?=30$.','Compter de 24 à 30.','Je peux ajouter 6. $24+6=30$.','Il manque 6.') if i==2 else q('Vérifie en réunissant les deux parties.','Recomposer le tout.',f'${part}+{ans}={total}$. Le tout est retrouvé.',f'${part}+{ans}={total}$.')
   questions=[q('Quel est le tout à retrouver sur la barre ?','Repérer la quantité entière.',f'Le tout contient {total} objets.',f'Le tout vaut {total}.'),q(knownprompt,'Repérer ou réunir la partie connue.',knownstep,f'La partie connue vaut {part}.'),q('Quel calcul trouve la partie manquante ?','Enlever la partie connue du tout.',f'Je pars de {total}. J’enlève {part}.',f'Je calcule ${total}-{part}$.'),q('Trouve la quantité qui manque.','Calculer puis compléter la barre.',f'${total}-{part}={ans}$.\n\n[IMAGE_2]',f'La quantité cherchée est {ans} {obj}.'),extra]
  if i==6:questions[3]['etapes']=['Je retire les 30 places occupées : $50-30=20$. Puis les 2 autres : $20-2=18$.\n\n[IMAGE_2]']
  if i==8:questions[3]['etapes']=['J’échange une dizaine : $64=50+14$.\n\nJe retire les unités : $14-9=5$. Je retire les dizaines : $50-20=30$.\n\nJe réunis : $30+5=35$.\n\n[IMAGE_2]']
  items.append(ex(name,intro+'\n\n[IMAGE_1]\n\nLa barre montre le tout et ses parties.',questions))
 course=block('objectifs','',"Chercher une partie. Retrouver la quantité du départ. Vérifier sa réponse.")+ '\n\n## I. Le tout et ses parties\n\n'+block('definition','Une partie manquante','Le tout réunit toutes les parties. Si une partie manque, je la cherche.')+'\n\n'+block('exemple','Les perles','Il y a 18 perles. 7 sont rouges. Les autres sont bleues.\n\n$18-7=11$. Il y a 11 perles bleues.\n\n[IMAGE_1]\n\nJe vérifie : $7+11=18$.')+'\n\n## II. Retrouver le départ\n\n'+block('methode','Rejouer l’histoire','Je lis ce qui reste. Je remets ce qui a été donné.\n\nIl reste 12 images après en avoir donné 4.\n\n$12+4=16$. Il y avait 16 images.')+'\n\n## III. Manipuler pour comprendre\n\n'+block('methode','Les jetons cachés','Prends 12 jetons. Cache-en une partie. Laisse 5 jetons visibles.\n\nCherche les jetons cachés : $12-5=7$. Découvre la boîte pour vérifier.')+'\n\n'+block('attention','Lire la question','Le mot « donne » ne choisit pas le calcul. Si je cherche le départ, je remets les objets donnés.')+'\n\n'+block('retenir','','Une partie se trouve en enlevant l’autre du tout. Je vérifie en réunissant les parties.')
 fiche='## I. Chercher une partie\n\n'+block('methode','','Je repère le tout. J’enlève la partie connue.\n\n$18-7=11$.\n\n[IMAGE_1]\n\nJe vérifie : $7+11=18$.')+'\n\n## II. Chercher le départ\n\n'+block('retenir','','Il reste 12 après un don de 4. Je remets 4 : $12+4=16$.\n\nJe lis toujours la question avant de calculer.')
 for group,key in [('cours','nouveau'),('fiches','nouvelle')]:corr[group][key]['2']={'fichier':'ex4_corrige.png','alt':'Quantité initiale retrouvée en réunissant les douze objets restants et les quatre objets donnés.'}
 course=course.replace('Il y avait 16 images.','Il y avait 16 images.\n\n[IMAGE_2]')
 fiche=fiche.replace('Je remets 4 : $12+4=16$.','Je remets 4 : $12+4=16$.\n\n[IMAGE_2]')
 finish(17,'Résoudre des problèmes : chercher une partie ou la quantité initiale',course,fiche,items,figs,corr,[x[0] for x in data])

def equal_groups():
 figs,corr=init(groups([4,4,4],green=True));items=[]
 data=[('Compter les groupes',[3,3,3,3],False),('Dessiner trois groupes',[2,2,2],True),('Deux additions répétées',[5,5,5],False),('Les paquets de cartes',[5,5,5,5],False),('Les paniers de balles',[6,6,6],False),('Deux rangées de points',[7,7],True),('Les voitures remplies',[4,4,4,4,4],False),('Les fleurs identiques',[5,5,5,5,5,5],True),('Des groupes différents',[3,3,4],False)]
 for i,(name,values,draw) in enumerate(data,1):
  count=len(values);v=values[0];total=sum(values);addition='+'.join(map(str,values));register(figs,corr,i,f'ex{i}',groups(values,blank=draw),groups(values,green=True),'Groupes de jetons et leur dénombrement')
  if i==6:figs['ex6_enonce']=rows(7,blank=True);figs['ex6_corrige']=rows(7)
  if i==8:figs['ex8_enonce']=flowers(blank=True);figs['ex8_corrige']=flowers()
  if i==9:
   intro='Trois boîtes contiennent 3, 3 et 4 jetons.';qs=[q('Combien y a-t-il de boîtes ?','Compter les contours.','Chaque contour montre une boîte. Il y en a trois.','Il y a 3 boîtes.'),q('Les boîtes ont-elles autant de jetons ?','Comparer les contenus.','Les deux premières ont 3 jetons. La dernière en a 4.','Non, les contenus sont différents.'),q('Peut-on dire « trois groupes de trois » ?','Vérifier chaque groupe.','La dernière boîte n’a pas 3 jetons.','Non : la dernière contient 4 jetons.'),q('Combien y a-t-il de jetons en tout ?','Additionner les contenus.','$3+3=6$, puis $6+4=10$.\n\n[IMAGE_2]','Il y a 10 jetons.'),q('Comment obtenir trois groupes de trois ?','Retirer seulement le jeton en trop.','Je retire 1 jeton de la dernière boîte. $4-1=3$.\n\n$3+3+3=9$.','Je retire 1 jeton. Il reste 9 jetons.')]
  else:
   context={1:'Observe les groupes dessinés.',2:'Dessine 3 groupes de 2 ronds dans les cadres vides.',3:'Observe 3 groupes de 5 jetons. Tu chercheras aussi le total de 4 groupes de 2.',4:'Il y a 4 paquets. Chaque paquet contient 5 cartes.',5:'Il y a 3 paniers. Chaque panier contient 6 balles.',6:'Dessine 2 rangées de 7 points. Utilise un cadre par rangée.',7:'Chaque voiture transporte 4 enfants. Il y a 5 voitures remplies.',8:'Une fleur a 5 pétales. Dessine 6 fleurs identiques. Un cadre représente une fleur.'}[i]
   intro=context
   last=q('Calcule aussi $2+2+2+2$.','Réunir quatre groupes de deux.','$2+2=4$, puis $4+2=6$, puis $6+2=8$.','Le total est 8.') if i==3 else q('Que devient le total si on retire un groupe ?','Enlever seulement le contenu d’un groupe.',f'${total}-{v}={total-v}$. Les autres groupes restent.',f'Il reste {total-v} objets.')
   qs=[q('Combien de groupes faut-il compter ou dessiner ?','Compter les cadres ou lire le nombre de groupes.',f'Il y a {count} groupes dans cette situation.',f'Il y a {count} groupes.'),q('Combien d’objets faut-il dans chaque groupe ?','Lire le contenu d’un seul groupe.',f'Chaque groupe contient {v} objets. Tous les groupes ont la même taille.',f'Chaque groupe contient {v} objets.'),q('Écris l’addition qui réunit tous les groupes.','Écrire une quantité par groupe.',f'Je répète {v}, une fois pour chacun des {count} groupes.',f'${addition}$.'),q('Trouve le nombre total d’objets. Complète ton dessin si besoin.','Compter tous les objets sans en oublier.',f'${addition}={total}$.\n\n[IMAGE_2]',f'Il y a {total} objets en tout.'),last]
  if i==9:
   figs['ex9_repare']=groups([3,3,3],green=True)
   corr['exercices']['nouveau-9']['3']={'fichier':'ex9_repare.png','alt':'Trois groupes de trois après retrait du jeton en trop.'}
   qs[4]['etapes'][0]+='\n\n[IMAGE_3]'
  items.append(ex(name,intro+'\n\n[IMAGE_1]',qs))
 course=block('objectifs','','Reconnaître des groupes de même taille. Dessiner les groupes. Trouver le total.')+'\n\n## I. Des groupes identiques\n\n'+block('definition','','Chaque groupe contient autant d’objets que les autres.')+'\n\n'+block('exemple','Trois boîtes','Il y a 3 boîtes de 4 jetons.\n\n[IMAGE_1]\n\nJe compte $4+4+4=12$ jetons. Je peux dire « trois fois quatre ».')+'\n\n## II. Dessiner et compter\n\n'+block('methode','','Je dessine un contour par groupe. Je mets autant de points dans chaque contour.\n\nJ’écris une quantité par groupe. Je les additionne dans l’ordre.')+'\n\n## III. À toi de manipuler\n\n'+block('methode','Deux groupes de cinq','Prends deux boîtes. Mets 5 jetons dans chacune.\n\n$5+5=10$. Compte tous les jetons pour vérifier.')+'\n\n'+block('attention','','Avec 3, 3 et 4 jetons, les groupes sont différents. Je ne dis pas « trois groupes de trois ».')+'\n\n'+block('retenir','','Une addition répétée réunit des groupes de même taille. Je compte tous les groupes.')
 fiche='## I. Reconnaître les groupes\n\n'+block('retenir','','Chaque groupe doit contenir autant d’objets.\n\n[IMAGE_1]\n\n3 groupes de 4 : $4+4+4=12$.')+'\n\n## II. Trouver le total\n\n'+block('methode','','Je dessine les groupes. Je compte les objets d’un groupe. J’écris un nombre par groupe.\n\nJe vérifie en comptant tous les objets.')
 finish(18,'Résoudre des problèmes : réunir des groupes de même taille',course,fiche,items,figs,corr,[x[0] for x in data])

def share():
 figs,corr=init(groups([4,4,4],green=True));items=[]
 figs['paquets_modele']=groups([2,2,2,2,2],green=True)
 for group,key in [('cours','nouveau'),('fiches','nouvelle')]:corr[group][key]['2']={'fichier':'paquets_modele.png','alt':'Dix jetons rangés en cinq paquets de deux jetons.'}
 data=[('Douze jetons pour deux',12,2,'parts'),('Des paquets de cinq',15,5,'paquets'),('Dix-huit cartes pour trois',18,3,'parts'),('Des tours de quatre',20,4,'paquets'),('Vingt-quatre perles pour quatre',24,4,'parts'),('Deux collections égales',12,2,'parts'),('Quatre collections égales',16,4,'parts'),('Des équipes de six',24,6,'paquets'),('Réparer le partage',10,2,'erreur')]
 for i,(name,total,k,kind) in enumerate(data,1):
  if kind=='paquets':size=k;count=total//k
  else:count=k;size=total//k
  vals=[size]*count;fig1=groups(vals,blank=True)
  if i==9:fig1=groups([6,4])
  register(figs,corr,i,f'ex{i}',fig1,groups(vals,green=True),'Partage équitable en groupes égaux')
  if i==7:figs[f'ex{i}_corrige']=groups(vals,green=True,firstonly=True)
  if kind=='paquets':
   intro=f'Prends {total} jetons. Fais des paquets de {size} jetons. Les cadres sont une aide. Tu peux en laisser vides.'
   if i==4:intro='Avec 20 cubes, fais des tours de 4 cubes. Tu peux utiliser un jeton par cube. Chaque paquet de 4 jetons représente une tour. Les cadres sont une aide. Tu peux en laisser vides.'
   if i==8:intro='24 enfants forment des équipes de 6. Représente chaque enfant par un jeton. Chaque paquet de 6 jetons représente une équipe. Les cadres sont une aide. Tu peux en laisser vides.'
   # Aucun nombre de cadres ne doit dévoiler le nombre de paquets.
   figs[f'ex{i}_enonce']=groups([0]*6,blank=True)
   qs=[q('Combien de jetons faut-il utiliser ?','Lire le total à ranger.',f'Je prends exactement {total} jetons.',f'Il faut {total} jetons.'),q('Combien faut-il dans un paquet ?','Lire la taille demandée.',f'Je mets {size} jetons ensemble. Je fais pareil pour chaque paquet.',f'Il faut {size} jetons par paquet.'),q('Construis les paquets. Combien obtiens-tu de paquets complets ?','Former un paquet après l’autre.',f'Je prends {size} jetons à chaque fois. Je peux faire {count} paquets.\n\n[IMAGE_2]',f'J’obtiens {count} paquets.'),q('Écris une addition pour vérifier.','Réunir tous les paquets.',f'Il y a {count} nombres dans l’addition.',f'${"+".join(map(str,vals))}={total}$.'),q('Reste-t-il des jetons sans paquet ?','Compter ce qui n’a pas été rangé.',f'Les paquets utilisent les {total} jetons. ${total}-{total}=0$.','Il reste 0 jeton.')]
  else:
   intro=f'Prends {total} jetons. Partage-les entre {count} enfants. Chacun doit recevoir autant.'
   if i==3:intro='Partage 18 cartes entre 3 enfants. Tu peux utiliser un jeton par carte. Chacun doit recevoir autant.'
   if i==5:intro='Partage 24 perles entre 4 enfants. Tu peux utiliser un jeton par perle. Chacun doit recevoir autant.'
   if i==6:intro+=' Trace deux contours pour séparer les deux collections.'
   if i==7:intro+=' Trace quatre contours pour séparer les quatre collections. Colorie un seul de ces groupes.'
   if i==9:intro='Lina partage 10 cartes entre deux enfants. Elle donne 6 cartes au premier et 4 au second.'
   qs=[q('Combien d’objets faut-il partager ?','Compter le tout.',f'Le tout contient {total} objets.',f'Il faut partager {total} objets.'),q('Combien de parts égales faut-il faire ?','Compter les enfants.',f'Un enfant reçoit une part. Il y a {count} enfants.',f'Il faut {count} parts égales.'),q('Distribue un objet à chacun, puis recommence. Combien chacun reçoit-il ?','Faire des tours de distribution.',f'Je donne un objet à chacun à chaque tour. Après {size} tours, tout est distribué.\n\n[IMAGE_2]',f'Chacun reçoit {size} objets.'),q('Vérifie le total avec une addition.','Réunir les parts égales.',f'Je compte une part par enfant.',f'${"+".join(map(str,vals))}={total}$.'),q('Le partage proposé par Lina est-il équitable ? Comment le corriger ?' if i==9 else ('Combien d’objets sont dans le groupe colorié ?' if i==7 else 'Comment sais-tu que le partage est équitable ?'),'Comparer les parts.',('6 et 4 sont différents. Je déplace une carte du premier enfant vers le second. $6-1=5$ et $4+1=5$.' if i==9 else (f'Le groupe colorié est l’un des {count} groupes. Il contient {size} objets.' if i==7 else f'Chaque enfant reçoit {size} objets. Il n’en reste aucun.')),('Non. Il faut donner 5 cartes à chacun.' if i==9 else (f'Le groupe colorié contient {size} objets.' if i==7 else f'Le partage est équitable : {size} objets pour chacun.')))]
  items.append(ex(name,intro+'\n\n[IMAGE_1]',qs))
 course=block('objectifs','','Partager en parts égales. Former des paquets. Vérifier le total.')+'\n\n## I. Donner autant à chacun\n\n'+block('definition','','Un partage est équitable quand chacun reçoit autant.')+'\n\n'+block('methode','Distribuer','Prends 12 jetons et 3 assiettes. Donne un jeton à chaque assiette. Recommence.\n\nAprès 4 tours, chaque assiette a 4 jetons.\n\n[IMAGE_1]\n\nJe vérifie : $4+4+4=12$.')+'\n\n## II. Former des paquets\n\n'+block('exemple','Des paquets de deux','Prends 10 jetons. Entoure 2 jetons. Recommence tant que tu le peux.\n\nTu obtiens 5 paquets. $2+2+2+2+2=10$.')+'\n\n## III. Vérifier le partage\n\n'+block('methode','','Je compare les groupes. Je recompte tous les objets. Je regarde s’il en reste.')+'\n\n'+block('attention','','6 cartes pour l’un et 4 pour l’autre, ce n’est pas équitable. Avec 10 cartes pour deux enfants, chacun doit recevoir 5 cartes.')
 fiche='## I. Partager en parts égales\n\n'+block('methode','','Je donne un objet à chacun. Je recommence. Je compare les parts.\n\n[IMAGE_1]\n\n$4+4+4=12$. Chacun reçoit 4 jetons.')+'\n\n## II. Former des paquets\n\n'+block('retenir','','Je fais des groupes de la taille demandée. Je compte les groupes.\n\nAvec 10 jetons, je fais 5 paquets de 2. Je vérifie : $2+2+2+2+2=10$.')
 course=course.replace('Tu obtiens 5 paquets. $2+2+2+2+2=10$.','Tu obtiens 5 paquets. $2+2+2+2+2=10$.\n\n[IMAGE_2]')
 fiche=fiche.replace('Avec 10 jetons, je fais 5 paquets de 2.','Avec 10 jetons, je fais 5 paquets de 2.\n\n[IMAGE_2]\n\n')
 finish(19,'Résoudre des problèmes : partager équitablement ou former des paquets',course,fiche,items,figs,corr,[x[0]+(' ; activité de bande remplacée par une collection concrète en parts égales, sans fraction' if j in (6,7) else '') for j,x in enumerate(data,1)])

def two_steps():
 figs,corr=init(story(18,-5,4,True));items=[]
 data=[('Les oiseaux',20,-6,3,'Il y a 20 oiseaux. 6 partent, puis 3 arrivent.','oiseaux'),('Les cartes reçues',8,7,4,'J’ai 8 cartes. Je reçois 7 cartes, puis 4 autres.','cartes'),('Les perles utilisées',25,-8,-5,'Il y a 25 perles. On en utilise 8, puis 5.','perles'),('Les crayons verts',24,-7,-9,'Une boîte contient 24 crayons. 7 sont rouges et 9 sont bleus. Les autres sont verts.','crayons verts'),('Le bus',23,-10,6,'Un bus contient 23 enfants. 10 descendent, puis 6 montent.','enfants'),('Les achats',15,-4,-6,'J’ai 15 euros. Je paie 4 euros, puis 6 euros.','euros'),('Les livres',9,8,6,'Une étagère porte 9 albums, 8 documentaires et 6 bandes dessinées. Je réunis ces livres.','livres'),('Le pion',12,7,-4,'Un jeu a 30 cases. Le pion part de 12. Il avance de 7, puis recule de 4.','case'),('L’erreur de Hugo',22,-5,3,'J’ai 22 cubes. J’en donne 5, puis j’en reçois 3. Hugo répond 14.','cubes')]
 for i,(name,n,a,b,intro,unit) in enumerate(data,1):
  mid=n+a;end=mid+b;ca=f'{n}{a:+d}';cb=f'{mid}{b:+d}';register(figs,corr,i,f'ex{i}',story(n,a,b),story(n,a,b,True),'Deux changements dans leur ordre')
  last=q('Pourquoi Hugo trouve-t-il 14 ? Corrige son erreur.','Rejouer le dernier changement.','$22-5=17$. Hugo a enlevé 3 : $17-3=14$. Il faut ajouter les 3 cubes reçus.','$17+3=20$. Il y a 20 cubes.') if i==9 else q('Vérifie le dernier changement en revenant en arrière.','Annuler le dernier changement.',f'${end}{-b:+d}={mid}$. On retrouve le résultat du premier changement.',f'${end}{-b:+d}={mid}$.')
  qs=[q('Quelle quantité faut-il prendre au départ ?','Lire le début de l’histoire.',f'Je pars de {n}.',f'Le départ est {n}.'),q('Quel calcul décrit le premier changement ?','Choisir ajouter ou enlever.',f'Je '+('ajoute' if a>0 else 'retire')+f' {abs(a)} au nombre du départ.',f'Je calcule ${ca}$.'),q('Quel nombre gardes-tu après ce premier calcul ?','Garder le résultat pour la suite.',f'${ca}={mid}$. Ce nombre sert au deuxième calcul.',f'Je garde {mid}.'),q('Trouve le résultat final. Complète les deux cases.','Appliquer le deuxième changement au résultat gardé.',f'${cb}={end}$.\n\n[IMAGE_2]',f'Le résultat final est {end}'+(' : le pion est sur la case '+str(end)+'.' if unit=='case' else ' '+unit+'.')),last]
  items.append(ex(name,intro+'\n\n[IMAGE_1]\n\nLes flèches montrent les changements.',qs))
 course=block('objectifs','','Suivre deux changements. Garder le premier résultat. Répondre à la question.')+'\n\n## I. Suivre l’ordre de l’histoire\n\n'+block('exemple','Les enfants','18 enfants sont là. 5 partent. Puis 4 arrivent.\n\n$18-5=13$. Il reste 13 enfants après le départ.\n\n$13+4=17$. Il y a 17 enfants à la fin.\n\n[IMAGE_1]')+'\n\n## II. Garder une trace\n\n'+block('methode','','Je dessine une case par état. Je garde le résultat du premier calcul. Je pars de ce résultat pour le second calcul.')+'\n\n## III. Manipuler et vérifier\n\n'+block('methode','À toi de jouer','Pose 12 cubes. Ajoute 6 cubes, puis retire 3 cubes.\n\n$12+6=18$. Puis $18-3=15$.\n\nCompte les cubes : il doit y en avoir 15.')+'\n\n'+block('attention','','Je ne repars pas du nombre du début pour le deuxième calcul. Je repars du résultat gardé.')+'\n\n'+block('retenir','','Je lis dans l’ordre. Je fais un calcul par changement. Je réponds avec une phrase.')
 fiche='## I. Deux changements, deux calculs\n\n'+block('methode','','Je pars de 18. Je retire 5. Je garde 13. Puis j’ajoute 4.\n\n[IMAGE_1]\n\n$18-5=13$, puis $13+4=17$.')+'\n\n## II. Vérifier\n\n'+block('retenir','','Je rejoue l’histoire avec des jetons. Je compte à la fin.\n\nPour le deuxième calcul, je pars du premier résultat.')
 finish(20,'Résoudre des problèmes en deux étapes',course,fiche,items,figs,corr,[x[0] for x in data])

def survey():
 labels=['chat','chien'];votes=['chat','chien','chat','chat','chien','chat','chien','chat'];values=[5,3]
 game=['ballon','corde','cache-cache'];gv=['ballon','corde','ballon','cache-cache','corde','ballon','cache-cache','ballon','corde'];gcounts=[4,3,2]
 figs,corr=init(chart(['chat','chien'],[4,2],green=True));items=[]
 animalintro='Exemple autonome : huit personnes ont répondu, une seule fois chacune.\n\nRelevé : '+', '.join(votes)+'.'
 gameintro='Exemple autonome : neuf personnes ont répondu, une seule fois chacune.\n\nRelevé : '+', '.join(gv)+'.'
 def aq(question,method,step,result):return q(question,method,step,result)
 for i in range(1,10):
  labs,counts=(game,gcounts) if i>=7 else (labels,values)
  register(figs,corr,i,f'ex{i}',chart(labs,counts,blank=True),chart(labs,counts,green=True),'Diagramme à construire : une case par personne')
  filled=table(['Choix','Nombre de réponses'],[[x,y] for x,y in zip(labs,counts)])
  empty=table(['Choix','Nombre de réponses'],[[x,'…'] for x in labs])
  if i==1:
   intro='Fais ta propre enquête auprès de 6 à 12 personnes. Pose la même question : « Préfères-tu chat ou chien ? » Note une réponse par personne.\n\n'+animalintro
   qs=[aq('Écris la question et les deux choix pour ton enquête.','Garder une question identique.','Je demande à chacun de choisir un seul animal.','Question : « Préfères-tu chat ou chien ? » Choix : chat, chien.'),aq('Interroge 6 à 12 personnes. Note les réponses dans l’ordre.','Écrire un mot à chaque réponse.','Tes réponses dépendent des personnes. Écris un seul choix par personne.','Réponse personnelle : une liste de 6 à 12 choix, un par personne.'),aq('Dans l’exemple, combien de personnes ont répondu ?','Compter les mots du relevé.','Le relevé contient huit réponses.','8 personnes ont répondu.'),aq('Dans l’exemple, compte les votes pour chaque animal.','Pointer chaque réponse une seule fois.','Chat apparaît 5 fois. Chien apparaît 3 fois.\n\n'+filled,'Chat : 5. Chien : 3.'),aq('Vérifie ton relevé personnel. Puis vérifie le total de l’exemple.','Comparer nombre de réponses et nombre de personnes.','Dans ton enquête, chaque personne donne une réponse. Pour l’exemple, $5+3=8$.\n\n[IMAGE_2]','Le nombre de tes réponses doit égaler celui des personnes. Dans l’exemple : 8.')]
  elif i==2:
   intro='Reprends les réponses de ton enquête personnelle sur chat et chien. Recopie et complète ce tableau.\n\n'+empty+'\n\n'+animalintro
   qs=[aq('Compte tes réponses « chat ». Complète la ligne chat.','Faire une marque par réponse chat.','Ton nombre dépend de ton enquête. Ne compte pas les réponses chien.','La ligne chat contient ton nombre de votes chat.'),aq('Compte tes réponses « chien ». Complète la ligne chien.','Compter seulement les réponses chien.','Chaque réponse chien remplit une marque.','La ligne chien contient ton nombre de votes chien.'),aq('Vérifie le total de ton tableau.','Réunir les deux nombres.','Additionne les deux nombres de ton tableau. Compare avec le nombre de personnes interrogées.','Le total doit être le nombre de personnes de ton enquête.'),aq('Complète un autre tableau pour l’exemple fourni.','Compter les mots du relevé.','Je trouve cinq chats et trois chiens.\n\n'+filled,'Exemple : chat 5 ; chien 3.'),aq('Représente le tableau de l’exemple avec des cases.','Prendre une case par personne.','Je colorie 5 cases pour chat et 3 pour chien.\n\n[IMAGE_2]','Le diagramme a une barre de 5 cases et une de 3 cases.')]
  elif i==3:
   intro='Construis le diagramme de ton enquête personnelle : une case pour une personne. Nomme les deux barres.\n\n'+animalintro
   qs=[aq('Que représente une case dans ton diagramme ?','Choisir une règle simple.','Une personne donne un vote. Une case montre ce vote.','Une case représente une personne.'),aq('Construis tes deux barres avec les nombres de ton tableau.','Colorier autant de cases que de votes.','Pars du bas. Garde la même ligne de départ.','Réponse personnelle : une barre chat et une barre chien, aux hauteurs de ton tableau.'),aq('Pour l’exemple, combien de cases faut-il pour chat ?','Compter chat dans le relevé.','Le mot chat apparaît cinq fois.','Il faut 5 cases pour chat.'),aq('Pour l’exemple, combien de cases faut-il pour chien ?','Compter chien dans le relevé.','Le mot chien apparaît trois fois.','Il faut 3 cases pour chien.'),aq('Construis le diagramme de l’exemple et vérifie son total.','Additionner les cases des deux barres.','$5+3=8$.\n\n[IMAGE_2]','5 cases pour chat et 3 pour chien : 8 personnes.')]
  elif i==4:
   intro='Compare les résultats de ton enquête personnelle. Tu peux trouver un gagnant ou une égalité.\n\n'+animalintro
   qs=[aq('Dans ton enquête, quel animal a le plus de votes ?','Comparer les deux nombres de ton tableau.','Le plus grand nombre indique le plus de votes. Si les nombres sont égaux, il y a égalité.','Réponse personnelle : chat, chien, ou égalité, selon ton tableau.'),aq('Dans l’exemple, quel animal a le plus de votes ?','Compter les deux catégories.','Chat a 5 votes. Chien a 3 votes. 5 est plus grand que 3.','Chat a le plus de votes.'),aq('Combien chat a-t-il de votes en plus dans l’exemple ?','Chercher l’écart.','$5-3=2$.','Chat a 2 votes de plus.'),aq('Dessine les barres de l’exemple pour vérifier.','Comparer les hauteurs.','La barre chat a 5 cases. La barre chien a 3 cases.\n\n[IMAGE_2]','La barre chat dépasse la barre chien de 2 cases.'),aq('Avec 3 votes chat et 3 votes chien, qui gagne ?','Comparer deux nombres égaux.','Les deux nombres sont 3. Les barres auraient la même hauteur.','Il y a égalité.')]
  elif i==5:
   intro='Recopie ce tableau à double entrée. Dans chaque case, dessine la forme de la ligne avec le décor de la colonne.\n\n'+table(['Forme','Bleu','Hachuré'],[['Rond','…','…'],['Carré','…','…']])
   # Native table only; diagram not needed for these classification cells.
   corr['exercices'][f'nouveau-{i}']={}
   del figs[f'ex{i}_enonce'];del figs[f'ex{i}_corrige']
   qs=[aq('Que faut-il dessiner dans la case rond et bleu ?','Croiser la ligne et la colonne.','La ligne dit rond. La colonne dit bleu.','Un rond bleu.'),aq('Que faut-il dessiner dans la case rond et hachuré ?','Lire les deux indications.','Je garde la forme ronde. Je trace des hachures dedans.','Un rond hachuré.'),aq('Que faut-il dessiner dans la case carré et bleu ?','Croiser carré et bleu.','La ligne donne un carré. La colonne demande du bleu.','Un carré bleu.'),aq('Que faut-il dessiner dans la case carré et hachuré ?','Croiser carré et hachuré.','Je dessine un carré avec des hachures à l’intérieur.','Un carré hachuré.'),aq('Combien de cases as-tu remplies ? Compare les deux formes d’une même ligne.','Compter les croisements.',table(['Forme','Bleu','Hachuré'],[['Rond','Rond bleu','Rond hachuré'],['Carré','Carré bleu','Carré hachuré']])+'\n\nIl y a deux cases par ligne : $2+2=4$. Sur une ligne, la forme reste la même.','4 cases. Sur une même ligne, seule la décoration change.')]
  elif i==6:
   intro='Huit personnes ont été interrogées sur chat ou chien. Une personne a répondu deux fois.\n\nRelevé avec le doublon : '+', '.join(votes+['chien'])+'.\n\nLa dernière réponse chien est la deuxième réponse de cette personne. On garde seulement sa première réponse.\n\n'+animalintro
   qs=[aq('Combien de réponses compte le relevé avec le doublon ?','Compter tous les mots, même le doublon.','Il y a les huit réponses du premier relevé et une réponse en trop. $8+1=9$.','Il y a 9 réponses écrites.'),aq('Quelle réponse faut-il supprimer ?','Garder un seul vote par personne.','La dernière réponse chien est celle qui a été donnée une deuxième fois.','Il faut supprimer la dernière réponse chien.'),aq('Compte les votes après la correction.','Recompter le relevé sans le doublon.','On retrouve le relevé de huit personnes.\n\n'+filled,'Chat : 5. Chien : 3.'),aq('Construis les deux barres corrigées.','Prendre une case par vote gardé.','Je colorie 5 cases chat et 3 cases chien.\n\n[IMAGE_2]','Barres corrigées : 5 cases et 3 cases.'),aq('Vérifie que le total convient.','Comparer votes et personnes.','$5+3=8$. Il y a bien huit personnes.','8 votes pour 8 personnes.')]
  elif i==7:
   intro='Prépare ta propre enquête avec trois jeux : ballon, corde, cache-cache. Interroge de 3 à 19 personnes. Chaque personne choisit un seul jeu.\n\n'+gameintro
   qs=[aq('Écris la question et les trois choix.','Présenter la même question à tous.','Je propose toujours les mêmes trois jeux.','Question : « Quel jeu préfères-tu : ballon, corde ou cache-cache ? »'),aq('Interroge de 3 à 19 personnes. Note un choix par personne.','Recueillir réellement les réponses.','Écris les choix dans l’ordre. Ne note pas deux votes pour une personne.','Réponse personnelle : une liste de 3 à 19 réponses, une par personne.'),aq('Compte les trois choix de ton enquête et construis ton tableau.','Classer chaque réponse une seule fois.','Crée trois lignes : ballon, corde et cache-cache. Compte les réponses de chaque ligne.','Réponse personnelle : trois effectifs dont le total est le nombre de personnes.'),aq('Pour l’exemple, compte les votes de chaque jeu.','Pointer les neuf mots du relevé.','Ballon apparaît 4 fois, corde 3 fois et cache-cache 2 fois.\n\n'+filled,'Ballon : 4. Corde : 3. Cache-cache : 2.'),aq('Représente l’exemple et vérifie le total.','Construire une barre par jeu.','$4+3=7$, puis $7+2=9$.\n\n[IMAGE_2]','Trois barres de 4, 3 et 2 cases. Le total est 9.')]
  elif i==8:
   intro='Reprends ton enquête personnelle avec les trois jeux. Construis trois tours de cubes : un cube par vote.\n\n'+gameintro
   qs=[aq('Combien de tours faut-il construire ?','Prendre une tour par choix.','Les choix sont ballon, corde et cache-cache.','Il faut 3 tours.'),aq('Construis les tours de ton enquête. Nomme chacune.','Utiliser les nombres de ton tableau.','Prends autant de cubes que de votes pour chaque jeu. Écris le nom du jeu près de sa tour.','Réponse personnelle : trois tours dont les hauteurs suivent ton tableau.'),aq('Vérifie le nombre total de tes cubes.','Réunir les trois tours.','Le nombre de cubes doit être le nombre de personnes de ton enquête.','Un cube par personne : les deux nombres doivent être égaux.'),aq('Construis les tours de l’exemple. Combien faut-il de cubes dans chacune ?','Compter les réponses du relevé.','Je compte 4 ballon, 3 corde et 2 cache-cache.\n\n[IMAGE_2]','Ballon : 4 cubes. Corde : 3 cubes. Cache-cache : 2 cubes.'),aq('Quelle tour de l’exemple est la plus haute ? De combien dépasse-t-elle la plus basse ?','Comparer les hauteurs.','4 est le plus grand nombre. 2 est le plus petit. $4-2=2$.','La tour ballon dépasse la tour cache-cache de 2 cubes.')]
  else:
   intro='Transforme tes trois tours de cubes en un diagramme sur ton cahier. Choisis un titre. Utilise une case par personne.\n\n'+gameintro
   qs=[aq('Choisis un titre qui dit le sujet de ton enquête.','Nommer ce qui a été demandé.','Ton titre doit parler des jeux préférés.','Titre possible : « Les jeux préférés des personnes interrogées ».'),aq('Trace et nomme les trois barres de ton enquête.','Garder une barre pour chaque choix.','Pars de la même ligne. Écris ballon, corde et cache-cache sous les barres.','Réponse personnelle : trois barres nommées, une par jeu.'),aq('Colorie les cases selon tes tours et vérifie ton dessin.','Remplacer chaque cube par une case.','Compare chaque hauteur avec le nombre de ton tableau. Le total des cases doit être le nombre de personnes.','Réponse personnelle : une case par cube et par vote.'),aq('Construis aussi le diagramme de l’exemple fourni.','Compter les choix puis colorier les cases.','Le relevé donne 4, 3 et 2 votes.\n\n[IMAGE_2]','Ballon : 4 cases. Corde : 3 cases. Cache-cache : 2 cases.'),aq('Quel jeu a le plus de votes dans l’exemple ? Vérifie le total.','Lire les hauteurs et additionner.','4 est plus grand que 3 et 2. $4+3+2=9$.','Ballon a le plus de votes. Le total est 9 personnes.')]
  names=['Mener une enquête','Construire le tableau','Construire les deux barres','Comparer les résultats','Lire les deux entrées','Corriger un double vote','Trois choix de jeux','Construire les tours','Passer des tours au diagramme']
  if i==5:
   rond=r'$\color{#1B3C8E}{\Large\bullet}$'
   carre=r'$\color{#1B3C8E}{\blacksquare}$'
   completed=table(['Forme','Bleu','Hachuré'],[['Rond',rond,'◍ (rond hachuré)'],['Carré',carre,'▨ (carré hachuré)']])
   qs[0]['resultat']='Un rond bleu : '+rond+'.'
   qs[1]['resultat']='Un rond hachuré : ◍.'
   qs[2]['resultat']='Un carré bleu : '+carre+'.'
   qs[3]['resultat']='Un carré hachuré : ▨.'
   qs[4]['etapes']=[completed+'\n\nDeux cases par ligne : $2+2=4$. Sur une ligne, la forme reste la même.']
  items.append(ex(names[i-1],intro+ ('\n\n[IMAGE_1]\n\nGrille pour l’exemple autonome.' if i!=5 else ''),qs))
 course=block('objectifs','','Poser une question. Recueillir des réponses. Construire un tableau et un diagramme.')+'\n\n## I. Faire une enquête\n\n'+block('methode','','Choisis de deux à cinq réponses possibles. Interroge moins de 40 personnes. Pose la même question à chacun. Note un seul choix par personne.')+'\n\n'+block('exemple','À toi de jouer','Demande à six personnes : « Préfères-tu chat ou chien ? » Note les réponses dans l’ordre. Tes résultats dépendent des personnes.\n\nExemple de relevé : chat, chien, chat, chat, chien, chat.')+'\n\n## II. Construire un tableau\n\n'+block('methode','','Compte chaque catégorie. Écris son nombre dans la bonne ligne.\n\n'+table(['Animal','Votes'],[['Chat',4],['Chien',2]])+'\n\n$4+2=6$. Le total est bien six personnes.')+'\n\n## III. Construire un diagramme\n\n'+block('methode','','Construis une tour par choix. Prends un cube par vote. Remplace chaque cube par une case. Donne un titre au diagramme.\n\n[IMAGE_1]\n\nLa barre chat a 4 cases. La barre chien a 2 cases. Chat a le plus de votes.')+'\n\n## IV. Croiser deux indications\n\n'+block('exemple','Le tableau à double entrée',table(['Forme','Bleu','Hachuré'],[['Rond','Rond bleu','Rond hachuré'],['Carré','Carré bleu','Carré hachuré']])+'\n\nUne case croise une ligne et une colonne. La ligne donne la forme. La colonne donne le décor.')+'\n\n'+block('retenir','','Une personne compte pour un vote. Le total du tableau et le total des cases doivent être le nombre de personnes.')
 fiche='## I. Recueillir et compter\n\n'+block('methode','','Je pose la même question à chacun. Je propose deux à cinq choix. Une personne donne un seul vote. Je compte chaque choix.\n\n'+table(['Animal','Votes'],[['Chat',4],['Chien',2]])+'\n\n$4+2=6$ personnes.')+'\n\n## II. Représenter\n\n'+block('retenir','','Une case représente une personne. Je nomme chaque barre.\n\n[IMAGE_1]\n\nLe total des cases doit être le total des votes.')+'\n\n## III. Double entrée\n\n'+block('retenir','','Je lis la ligne et la colonne. Ligne carré et colonne bleu : je dessine un carré bleu.')
 shapes=table(['Forme','Bleu','Hachuré'],[['Rond',r'$\color{#1B3C8E}{\Large\bullet}$','◍'],['Carré',r'$\color{#1B3C8E}{\blacksquare}$','▨']])
 course=course.replace(table(['Forme','Bleu','Hachuré'],[['Rond','Rond bleu','Rond hachuré'],['Carré','Carré bleu','Carré hachuré']]),shapes)
 fiche+='\n\n'+shapes
 finish(29,'Organisation et gestion de données : mener une enquête, construire des tableaux et des diagrammes',course,fiche,items,figs,corr,names)

if __name__=='__main__':
 parties();equal_groups();share();two_steps();survey()
