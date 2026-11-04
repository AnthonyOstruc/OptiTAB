"""Relit les documents livrés et les coordonnées TikZ ; aucune donnée en base."""
from pathlib import Path
import importlib.util,json,re,math,collections
P=Path(__file__).resolve().parent
D=json.loads((P/'donnees_pedagogiques.json').read_text(encoding='utf-8'))
spec=importlib.util.spec_from_file_location('figures_locales',P/'figures/figures.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
G=f.GEOMETRIE;code=D['chapitre'];checks=[]
def check(b,label):
 assert b,label
 checks.append(label)
text=(P/'exercices.txt').read_text(encoding='utf-8');blocks=[b.strip() for b in re.split(r'^===[ \t]*$',text,flags=re.M) if b.strip()]
check(len(blocks)==9,'9 exercices conservant les 9 compétences sources')
for i,(b,e) in enumerate(zip(blocks,D['exercices']),1):
 check(f'Id: nouveau-{i}\n' in b,f'ex{i} identifiant')
 enonce=b.split('Énoncé:\n',1)[1].split('Étapes:\n',1)[0];etapes=b.split('Étapes:\n',1)[1].split('Solution:\n',1)[0];solution=b.split('Solution:\n',1)[1]
 check(len(re.findall(r'^\d+\. ',enonce,re.M))==5,f'ex{i} cinq questions réelles')
 check(len(re.findall(r'^## Question ',etapes,re.M))==5,f'ex{i} cinq corrections')
 for j,(question,raison,reponse) in enumerate(e['questions'],1):
  check(f'{j}. {question}' in enonce,f'ex{i} Q{j} énoncé actuel')
  sec=re.search(rf'^## Question {j} :.*?(?=^## Question |\Z)',etapes,re.M|re.S)[0]
  check(all(f'::: {k}' in sec for k in ('methode','etape','resultat')),f'ex{i} Q{j} méthode étape résultat')
  check(raison in sec and reponse in sec,f'ex{i} Q{j} résultat développé actuel')
  check(f'{j}. {reponse}' in solution,f'ex{i} Q{j} solution actuelle')
 # Recalcul indépendant de TOUTES les égalités entières réellement présentes.
 for expression,result in re.findall(r'(?<![\w])([0-9]+(?:\s*[+−×]\s*[0-9]+)+)\s*=\s*([0-9]+)',b):
  check(eval(expression.replace('−','-').replace('×','*'),{'__builtins__':{}},{})==int(result),f'ex{i} calcul {expression}={result}')
for name in ('cours_nouveau.txt','fiche_nouvelle.txt'):
 s=(P/name).read_text(encoding='utf-8');check(s.startswith('Titre: ') and '<!-- optitab:1 -->' in s,name+' format')
 for expression,result in re.findall(r'(?<![\w])([0-9]+(?:\s*[+−×]\s*[0-9]+)+)\s*=\s*([0-9]+)',s):
  check(eval(expression.replace('−','-').replace('×','*'),{'__builtins__':{}},{})==int(result),name+' '+expression)
def lengths(p):return [math.dist(a,b) for a,b in zip(p,p[1:]+p[:1])]
def rights(p):
 return [abs((p[i-1][0]-b[0])*(p[(i+1)%len(p)][0]-b[0])+(p[i-1][1]-b[1])*(p[(i+1)%len(p)][1]-b[1]))<1e-8 for i,b in enumerate(p)]
def eq(a,b):return math.isclose(a,b,abs_tol=1e-8)
def drawpaths(name,style):
 bodies=re.findall(r'\\draw\['+re.escape(style)+r'\]\s*([^;]+);',f.FIGURES[name])
 return [[tuple(map(float,p)) for p in re.findall(r'\((-?[\d.]+),(-?[\d.]+)\)',s)] for s in bodies]
def samecoords(a,b):return len(a)==len(b) and all(eq(x,u) and eq(y,v) for (x,y),(u,v) in zip(a,b))
if code==32:
 for actual,expected in zip(drawpaths('quadrilateres','geoTrait'),G['quadrilateres']):check(samecoords(actual,expected),'TikZ quadrilatère correspondant aux coordonnées testées')
 a,b,c=G['quadrilateres'];check(all(rights(a)) and max(lengths(a))-min(lengths(a))<1e-8,'A carré tourné exact')
 check(all(rights(b)) and not eq(lengths(b)[0],lengths(b)[1]),'B rectangle non carré exact')
 check(not any(rights(c)) and max(lengths(c))-min(lengths(c))<1e-8,'C losange non carré exact')
 check([len(p) for p in G['polygones']]==[5,6],'pentagone hexagone exacts')
 check(G['angles']==[45,90,120],'angles aigu droit obtus sans codes révélateurs')
 for actual,angle in zip(drawpaths('angles','geoTrait'),G['angles']):
  a,b,c=actual;u=(a[0]-b[0],a[1]-b[1]);v=(c[0]-b[0],c[1]-b[1]);value=math.degrees(math.acos(sum(x*y for x,y in zip(u,v))/(math.hypot(*u)*math.hypot(*v))))
  check(eq(value,angle),'ouverture tracée TikZ '+str(angle))
 check('A est un carré.' in text and 'B est un rectangle' in text and 'C est un losange' in text,'classement actuel des figures')
if code==33:
 check([math.dist(G['milieu'][i],G['milieu'][i+1]) for i in [0,1]]==[4,4],'milieu 8 cm réel')
 for name,scale,w,h in [('rectangle',.8,7,3),('carre',.7,5,5)]:
  p=G[name];check(all(rights(p)) and eq(lengths(p)[0]/scale,w) and eq(lengths(p)[1]/scale,h),name+' angles et longueurs exacts')
  check(samecoords(drawpaths(name,'geoReponse')[0],p),name+' tracé TikZ conforme aux coordonnées')
 p=G['triangle'];check(rights(p)[0] and eq(math.dist(p[0],p[1])/.7,6) and eq(math.dist(p[0],p[2])/.7,4),'triangle rectangle 6 sur 4 exact')
 for name in ['cercle','diametre']:
  c=G[name];check(eq(math.dist(c['centre'],c['A']),c['rayon']) and eq(math.dist(c['centre'],c['B']),c['rayon']),name+' rayons exacts')
 check(eq(math.dist(G['diametre']['A'],G['diametre']['B']),6),'diamètre 6 cm exact')
 p=G['quadrillage'];moves=[(b[0]-a[0],b[1]-a[1]) for a,b in zip(p,p[1:]+p[:1])]
 check(moves==[(3,1),(1,2),(-3,-1),(-1,-2)],'déplacements de reproduction exacts')
 check('Depuis A : 3 carreaux à droite et 1 vers le haut.' in text,'déplacement A B actuel')
if code==34:
 # Comptage combinatoire des solides, indépendant des phrases de solution.
 for k in [3,4]:
  expected={'faces':k+1,'aretes':2*k,'sommets':k+1};name='triangulaire' if k==3 else 'carree'
  check(G['pyramides'][name]==expected,name+' faces arêtes sommets')
 check(G['cube_cache']['aretes_visibles']+G['cube_cache']['aretes_cachees']==12,'cube 12 arêtes visibles cachées')
 check(len(G['solides']['lettres'])==6,'six solides dessinés pour six annoncés')
 # Propagation exacte de repères 3D sur le réseau de carrés. Deux normales
 # identiques impliquent deux faces superposées, donc un faux patron.
 def neg(v):return tuple(-a for a in v)
 def faces(net):
  cells={tuple(c) for c in net};start=min(cells);seen={start:((1,0,0),(0,1,0),(0,0,1))};todo=[start];coherent=True
  while todo:
   x,y=todo.pop();u,v,n=seen[x,y]
   for dx,dy,frame in [(1,0,(neg(n),v,u)),(-1,0,(n,v,neg(u))),(0,1,(u,neg(n),v)),(0,-1,(u,n,neg(v)))]:
    other=(x+dx,y+dy)
    if other not in cells:continue
    if other in seen:coherent &= seen[other]==frame
    else:seen[other]=frame;todo.append(other)
  return coherent and len(seen)==6 and len({frame[2] for frame in seen.values()})==6
 check(faces(G['patrons']['A']),'patron A six normales 3D distinctes')
 check(not faces(G['patrons']['B']),'bande B se superpose après pliage')
 drawn=drawpaths('patrons','geoTrait')
 expectedA=[[(x*.8,y*.8),((x+1)*.8,y*.8),((x+1)*.8,(y+1)*.8),(x*.8,(y+1)*.8)] for x,y in G['patrons']['A']]
 expectedB=[[(x*.8,4.4),((x+1)*.8,4.4),((x+1)*.8,5.2),(x*.8,5.2)] for x,y in G['patrons']['B']]
 check(len(drawn)==12 and all(samecoords(a,b) for a,b in zip(drawn,expectedA+expectedB)),'douze carrés TikZ égaux et dispositions des patrons vérifiées')
 check('A se ferme en un cube à 6 faces.' in text and 'B ne ferme pas un cube.' in text,'prévisions actuelles cohérentes avec pliage 3D')
if code==35:
 for name in ['sym_v','sym_v_corrige','sym_h','sym_h_corrige']:
  g=G[name];axis=g['position'];expected=[(x,2*axis-y) if g['axe']=='h' else (2*axis-x,y) for x,y in g['points']]
  check([list(p) for p in expected]==g['reportes'],name+' report exact de tous sommets')
  check(samecoords(drawpaths(name,'geoTrait')[0],[(x*.6,y*.6) for x,y in g['points']]),name+' points réellement tracés')
  if name.endswith('_corrige'):check(samecoords(drawpaths(name,'geoReponse')[0],[(x*.6,y*.6) for x,y in g['reportes']]),name+' correction réellement tracée')
  check(eq(sum(lengths(g['points'])),sum(lengths(g['reportes']))),name+' longueurs conservées')
 p=G['sans_axe'];check(eq(lengths(p)[0],lengths(p)[2]) and not any(rights(p)) and not eq(lengths(p)[0],lengths(p)[1]),'parallélogramme non rectangle non losange')
 check('B se reporte à 3 carreaux à droite' in text and 'B se reporte à 3 carreaux au-dessous' in text,'reports énoncés actuels verticaux et horizontaux')
 check('Le carré possède 4 axes' in text and 'possède 2 axes de symétrie' in text,'nombres d’axes actuels')
if code==36:
 values=[0,1,2,1,0,3,2,1,1,0,2,1];counts=collections.Counter(values)
 check([counts[i] for i in range(4)]==G['fratrie']['valeurs']==[3,5,3,1],'dépouillement réel des 12 réponses')
 check(sum(G['fratrie']['valeurs'])==12,'total enquête')
 check(G['trajets']['valeurs']==[25,15,10] and G['trajets']['pas']==5,'hauteurs et échelle trajets')
 check(G['echelle']['valeurs']==[20,40,60] and G['echelle']['pas']==10,'hauteurs et échelle groupes')
 for name,g in G.items():
  check(all(v%g['pas']==0 for v in g['valeurs']) and g['max']==max(g['valeurs']),name+' graduations régulières')
  rectangles=re.findall(r'\\draw\[otNavy,fill=otNavy!45\]\s*\([\d.]+,0\) rectangle \([\d.]+,([\d.]+)\)',f.FIGURES[name])
  check(len(rectangles)==len(g['valeurs']) and all(eq(float(h),v/g['max']*3.6) for h,v in zip(rectangles,g['valeurs'])),name+' hauteurs réellement tracées TikZ')
  labels=re.findall(r'\\node\[anchor=east,text=otInk\] at \(-0.2,([\d.]+)\) \{(\d+)\}',f.FIGURES[name])
  check([int(v) for _,v in labels]==list(range(0,g['max']+1,g['pas'])),name+' graduations réellement dessinées')
 check('15 élèves viennent à vélo.' in text and '35 élèves viennent à pied ou en bus.' in text,'lectures graphique actuelles')
 check('50 élèves viennent en voiture.' in text and 100-sum(G['trajets']['valeurs'])==50,'complément voitures actuel')
 check('Le mardi compte 25 inscriptions.' in text and 'L’écart est de 5 inscriptions.' in text and (18+7)-(12+8)==5,'tableau double entrée actuel')
mapping=json.loads((P/'figures/correspondance.json').read_text(encoding='utf-8'));used=[]
for family,docs in mapping.items():
 for ident,positions in docs.items():
  for position,meta in positions.items():
   check(meta['fichier'].removesuffix('.png') in f.FIGURES,'figure référencée '+meta['fichier']);used.append(meta['fichier'])
report={'math_OK':True,'chapitre':code,'exercices':9,'questions':45,'controles':len(checks),'details':checks,'figures_referencees':sorted(set(used))}
(P/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False))
