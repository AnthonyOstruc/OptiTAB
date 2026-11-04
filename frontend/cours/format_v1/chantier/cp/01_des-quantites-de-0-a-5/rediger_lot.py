from pathlib import Path
import sys,json,re
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'_coordination'))
from commun_redaction import q,ex,write,table

WORDS={0:'zéro',1:'un',2:'deux',3:'trois',4:'quatre',5:'cinq',6:'six',7:'sept',8:'huit',9:'neuf',10:'dix',11:'onze',12:'douze',13:'treize',14:'quatorze',15:'quinze',16:'seize',17:'dix-sept',18:'dix-huit',19:'dix-neuf',20:'vingt',30:'trente',40:'quarante',50:'cinquante',60:'soixante',80:'quatre-vingts',100:'cent'}
def mot(n):
 if n in WORDS:return WORDS[n]
 if n<70:
  d,u=divmod(n,10);return WORDS[10*d]+('-et-un' if u==1 else '-'+WORDS[u])
 if n<80:return 'soixante'+('-et-onze' if n==71 else '-'+mot(n-60))
 return 'quatre-vingt-'+mot(n-80)

FIGS={};MAP={};ITEMS=[];CODE=0
def pic(name,body):
 FIGS[name]=r'\begin{tikzpicture}[x=1cm,y=1cm,font=\large]'+body+r'\end{tikzpicture}'
 return name
def node(x,y,text,color='otNavy'):
 return rf'\node[text={color}] at ({x},{y}) {{{text}}};'
def dots(values,answer=False,large=False):
 s=''
 for row,n in enumerate(values):
  y=-row*1.25;s+=node(-.55,y,chr(65+row))
  if not n:s+=r'\draw[otRule,dashed] (0,'+str(y-.3)+') rectangle (2,'+str(y+.3)+');'
  for k in range(n):s+=rf'\fill[otNavy!80] ({(k%10)*.43},{y-(k//10)*.38}) circle ({.13 if not large else .18 if row==0 else .10});'
  if answer:s+=node(5,y,str(n),'otGreenDark')
 return s
def frame(n,answer=False):
 s=''
 for k in range(10):
  x=(k%5)*.65;y=-(k//5)*.65
  s+=rf'\draw[otNavy] ({x-.3},{y-.3}) rectangle ({x+.3},{y+.3});'
  if k<n:s+=rf'\fill[otNavy] ({x},{y}) circle (.18);'
 if answer:s+=node(1.3,-1.35,rf'$5+{n-5}={n}$' if n>=5 else str(n),'otGreenDark')
 return s
def base(n,answer=False):
 d,u=divmod(n,10);s=''
 for j in range(d):
  x=j*.40
  s+=rf'\draw[otNavy,fill=otSky] ({x},0) rectangle ({x+.25},2.5);'
  for k in range(1,10):s+=rf'\draw[otNavy] ({x},{k*.25})--({x+.25},{k*.25});'
 for j in range(u):
  x=d*.4+.55+(j%3)*.4;y=(j//3)*.4
  s+=rf'\draw[otNavy,fill=otSky] ({x},{y}) rectangle ({x+.25},{y+.25});'
 s+=node(max(.7,d*.2),3,'Chaque barre contient 10 cubes.')
 if answer:s+=node(max(.7,d*.2),-.55,f'{d} dizaines et {u} unités : {n}','otGreenDark')
 return s
def line(lo,hi,missing=(),answer=False,mark=None):
 s=rf'\draw[otNavy] (0,0)--({(hi-lo)*.6},0);'
 for n in range(lo,hi+1):
  x=(n-lo)*.6;s+=rf'\draw[otNavy] ({x},-.10)--({x},.10);'
  if n not in missing or answer:s+=node(x,-.42,str(n),'otGreenDark' if n in missing else 'otNavy')
  else:s+=node(x,-.42,'?')
 if mark is not None:
  x=(mark-lo)*.6;s+=rf'\draw[otGreenDark,->,line width=1pt] ({x},.7)--({x},.2);'+node(x,1.05,str(mark),'otGreenDark')
 return s
def seq(chars,answer=False,selected=None):
 s=r'\draw[otNavy,->] (0,1)--(1.2,1);'+node(3.4,1,'Départ à gauche')
 for k,c in enumerate(chars):
  x=(k%10)*.58;y=-(k//10)*1.1;s+=node(x,y,c)
  if answer:s+=node(x,y-.6,str(k+1),'otGreenDark')
  if selected==k+1:s+=rf'\draw[otGreenDark] ({x-.24},{y-.24}) rectangle ({x+.24},{y+.24});'
 return s
def shapes(count,answer=False):
 s=r'\draw[otNavy,->] (0,1)--(1.2,1);'+node(3.4,1,'Départ à gauche')
 for k in range(count):
  x=k*.7
  if k%3==0:s+=rf'\draw[otNavy,fill=otSky] ({x},0) circle (.20);'
  elif k%3==1:s+=rf'\draw[otNavy,fill=otSky] ({x-.2},-.2) rectangle ({x+.2},.2);'
  else:s+=rf'\draw[otNavy,fill=otSky] ({x-.22},-.2)--({x+.22},-.2)--({x},.22)--cycle;'
  if answer:s+=node(x,-.55,str(k+1),'otGreenDark')
 return s
def attach(idx,body,completed,alt):
 a=pic(f'ex{idx}_enonce',body);b=pic(f'ex{idx}_corrige',completed)
 return {'1':{'fichier':a+'.png','alt':alt},'2':{'fichier':b+'.png','alt':'Corrigé : '+alt}}
def Q(prompt,method,reason,result,op,args,expected):
 z=q(prompt,method,reason,result);z['controle']={'operation':op,'entrees':args,'attendu':expected};return z
def numeral(n,direction='chiffres'):
 if direction=='chiffres':return Q(f'Écris en chiffres : « {mot(n)} ».','Relier le mot au nombre.',f'Je dis « {mot(n)} ». Je cherche son écriture avec des chiffres.',str(n),'word',[mot(n)],n)
 return Q(f'Lis {n} à voix haute.' if n>50 else f'Écris {n} en lettres.','Dire le nom du nombre.',f'Je reconnais {n}. Son nom est « {mot(n)} ».',mot(n),'name',[n],mot(n))
def count(n,context='jetons'):
 return Q(f'Pose {n} {context}. Touche chacun une seule fois. Combien en as-tu ?','Compter chaque objet une seule fois.',f'Je déplace chaque objet compté. Le dernier nombre dit est {n}.',f'Il y a {n} {context}.','identity',[n],n)
def draw(n):
 return Q(f'Dessine {n} ronds. Comment vérifies-tu ton dessin ?','Faire un rond pour chaque nombre dit.',f'Je dis les nombres de 1 à {n} en dessinant. Je recompte les ronds sans en oublier.',f'Le dessin contient {n} ronds.','identity',[n],n)
def compare(a,b):
 sign='<' if a<b else '>' if a>b else '='
 reason=(f'Je compare {a//10} dizaines et {b//10} dizaines.' if a//10!=b//10 else f'Les dizaines sont égales. Je compare {a%10} et {b%10} unités.') if max(a,b)>10 else 'Je mets les objets par deux, un de chaque groupe. Je regarde si un groupe en a encore.'
 return Q(f'Complète avec <, > ou = : {a} … {b}.','Comparer les deux nombres.',reason,f'${a} {sign} {b}$.','compare',[a,b],sign)
def order(values,reverse=False):
 ordered=sorted(values,reverse=reverse);sep=' > ' if reverse else ' < '
 return Q('Range du plus '+('grand au plus petit' if reverse else 'petit au plus grand')+' : '+' ; '.join(map(str,values))+'.','Choisir le plus '+('grand' if reverse else 'petit')+', puis recommencer.',f'Je place d’abord {ordered[0]}. Puis je compare les nombres qui restent. Je les place dans le même sens.','$'+sep.join(map(str,ordered))+'$.','sort',[values,reverse],ordered)
def before(n,after=False):
 ans=n+1 if after else n-1
 return Q(f'Écris le nombre juste {"après" if after else "avant"} {n}.','Avancer d’un nombre.' if after else 'Reculer d’un nombre.',f'Dans la suite, je lis : {n-1} ; {n} ; {n+1}.',str(ans),'shift',[n,1 if after else -1],ans)
def sequence(start,step,missing,length=5):
 arr=[start+i*step for i in range(length)];shown=['…' if i in missing else str(v) for i,v in enumerate(arr)];answers=[arr[i] for i in missing]
 return Q('Complète : '+' ; '.join(shown)+'.',f'Avancer de {step} en {step}.','Je repars du premier nombre. Je trouve : '+' ; '.join(map(str,arr))+'.',' ; '.join(map(str,answers))+'.','sequence',[start,step,missing],answers)
def decomp(n):
 d,u=divmod(n,10)
 return Q(f'Décompose {n} en dizaines et unités.','Faire des paquets de dix.',f'Je forme {d} paquets de 10. Il reste {u} objets seuls.',f'{n} = {d*10} + {u} : {d} dizaines et {u} unités. Je lis « {mot(n)} ».','decompose',[n],[d,u])
def total(a,b,story='jetons'):
 return Q(f'Il y a {a} {story} dans une boîte et {b} sur la table. Combien en tout ?','Réunir les deux groupes.',f'Je compte les deux groupes ensemble. ${a}+{b}={a+b}$.',f'Il y a {a+b} {story}.','sum',[a,b],a+b)
def missing(a,target,story='jetons'):
 return Q(f'Il faut {target} {story}. Tu en as {a}. Combien en manque-t-il ?','Compter ce qui manque pour atteindre le but.',f'Je cherche le nombre à ajouter à {a} pour avoir {target}. ${a}+{target-a}={target}$.',f'Il manque {target-a} {story}.','difference',[target,a],target-a)
def unchanged(n,action):
 return Q(f'Tu as {n} cubes. {action} Combien en as-tu maintenant ?','Vérifier si on ajoute ou enlève un cube.',f'On n’ajoute rien. On n’enlève rien. Je recompte : il y a encore {n} cubes.',f'Il y a toujours {n} cubes.','identity',[n],n)
def A(title,intro,questions,fig=None):
 if fig:
  intro+='\n\n[IMAGE_1]';questions[0]['etapes'].append('[IMAGE_2]')
 ITEMS.append(ex(title,intro,questions,figures=fig))
def begin(code):
 global CODE,FIGS,MAP,ITEMS
 CODE=code;FIGS={};MAP={};ITEMS=[]

def build01():
 begin(1)
 fig=attach(1,dots([5]),dots([5],True),'Une collection de cinq jetons, à compter un par un.')
 z=Q('Compte les jetons de la ligne A.','Toucher chaque jeton une fois.','Je dis : un, deux, trois, quatre, cinq. Le dernier mot indique la quantité.','Il y a 5 jetons.','identity',[5],5)
 A('Compter sans oublier','Compte lentement. Tu peux déplacer les jetons.',[z]+[count(n) for n in [1,2,3,4]],fig)
 fig=attach(2,dots([1])+node(1.3,.7,'Modèle de rond'),dots([2,4],True),'Un rond modèle ; puis les deux dessins corrigés de deux et quatre ronds.')
 A('Dessiner une quantité','Le rond montré est un modèle. Fais tes dessins sur une feuille.',[draw(n) for n in [2,4,1,3,5]],fig)
 A('La boîte vide','Une boîte vide ne contient aucun jeton.',[
 Q('Une boîte est vide. Quel nombre de jetons écris-tu ?','Reconnaître une quantité nulle.','Il n’y a aucun jeton. Aucun se note 0.','0 jeton.','identity',[0],0),
 Q('Une boîte contient 3 jetons. Retire les 3. Combien reste-t-il ?','Enlever tous les objets.','Je retire un jeton, puis un autre, puis le dernier. La boîte est vide.','0 jeton.','difference',[3,3],0),
 Q('Dans la boîte vide, pose 1 jeton. Combien y en a-t-il ?','Vérifier que la boîte n’est plus vide.','Un jeton est maintenant dans la boîte.','1 jeton.','sum',[0,1],1),numeral(0),compare(0,1)])
 A('La suite de zéro à cinq','Lis les nombres dans l’ordre.',[sequence(0,1,[2,4],6)]+[sequence(s,1,m) for s,m in [(1,[1,3]),(0,[1,3]),(1,[2,4]),(0,[0,4])]])
 fig=attach(5,dots([3,5]),dots([3,5],True),'Deux groupes A et B contenant trois et cinq jetons.')
 qs=[Q('Quel groupe contient 3 jetons ?','Compter chaque groupe.','A contient 3 jetons. B en contient 5.','Le groupe A.','choose',[[3,5],3],'A'),Q('Quel groupe contient 5 jetons ?','Compter les objets de B.','Je compte les cinq jetons de B.','Le groupe B.','choose',[[3,5],5],'B'),compare(3,5),draw(3),count(5)]
 A('Reconnaître le bon groupe','Observe A et B.',qs,fig)
 A('Des mots aux chiffres','Seul, lis le mot puis écris le chiffre. À deux, fais dicter les mots sans les regarder.',[numeral(n) for n in [2,0,5,3,4]])
 A('Déplacer ne change pas le nombre','Tu peux faire les essais avec de vrais cubes.',[unchanged(n,a) for n,a in [(3,'Écarte-les.'),(5,'Rapproche-les.'),(2,'Mets-les en ligne.'),(4,'Mets-les en carré.'),(1,'Change-le de place.')]])
 fig=attach(8,dots([4]),dots([2,2],True),'Quatre jetons à ranger ; corrigé en deux lignes de deux.')
 A('Ranger autrement','Pose quatre jetons comme sur le modèle. Garde toujours les mêmes jetons.',[unchanged(4,a) for a in ['Range-les en deux lignes.','Range-les en une ligne.','Fais deux petits groupes.','Écarte les deux groupes.','Réunis-les en un groupe.']],fig)
 fig=attach(9,dots([5]),dots([5,5],True),'Cinq enfants représentés par des jetons ; corrigé avec un crayon pour chacun.')
 qs=[]
 for n in [5,2,4,1,3]:qs.append(Q(f'Il y a {n} enfants. Dessine un crayon par enfant. Combien de crayons faut-il ?','Associer un crayon à chaque enfant.',f'Je fais une marque pour chaque enfant. Il faut autant de crayons que d’enfants.',f'Il faut {n} crayons.','identity',[n],n))
 A('Un objet pour chacun','Un jeton représente un enfant. Dessine les crayons sur ta feuille.',qs,fig)
 finish('Les nombres entiers : de 0 à 5',4,dots([4],True),[
 ('Compter une collection','Pour savoir combien il y a d’objets, je touche chaque objet une seule fois. Le dernier nombre dit donne la quantité.'),('Zéro','Une boîte vide contient 0 objet. Je dis « zéro ». Je compte : 0 ; 1 ; 2 ; 3 ; 4 ; 5.'),('Représenter et conserver une quantité','Je peux dessiner autant de ronds que d’objets. Si je déplace les objets sans en ajouter ni en enlever, leur nombre ne change pas.')], 'Je déplace les objets déjà comptés. Je ne compte pas deux fois le même.','4 jetons déplacés restent 4 jetons. Une boîte vide contient 0 jeton.')

def build02():
 begin(2)
 fig=attach(1,frame(9),frame(9,True),'Une boîte de dix cases avec neuf cases occupées.')
 qs=[Q('Combien de cases sont occupées ?','Voir cinq et encore quatre.','La première ligne est pleine : 5. La seconde contient 4 jetons. $5+4=9$.','9 cases sont occupées.','sum',[5,4],9)]+[total(5,n) for n in [1,2,3,5]]
 A('Voir cinq et encore','Chaque case contient au plus un jeton.',qs,fig)
 fig=attach(2,frame(0),frame(6,True),'Une boîte vide comme support de dessin ; corrigé avec six jetons.')
 A('Dessiner de six à dix','Dessine dans une boîte de dix cases. Remplis d’abord cinq cases.',[Q(f'Dessine {n} ronds. Combien sont après les cinq premiers ?','Séparer cinq et le reste.',f'Je dessine 5 ronds, puis {n-5}. $5+{n-5}={n}$.',f'5 ronds et encore {n-5} : {n} ronds.','difference',[n,5],n-5) for n in [6,7,8,9,10]],fig)
 A('Relier les mots aux nombres','Lis à voix haute : 10 ; 6 ; 8. Puis lis chaque mot et écris le nombre.',[numeral(n) for n in [6,8,10,7,9]])
 A('Compléter la suite','On avance d’un nombre à chaque place.',[sequence(5,1,[2,4],6)]+[sequence(s,1,m) for s,m in [(6,[1,3]),(5,[1,3]),(6,[2,4]),(5,[0,4])]])
 A('Les voisins des nombres','Cherche dans la suite de 0 à 10.',[before(9),before(9,True),before(7),before(7,True),before(10)])
 A('Écouter et écrire','Seul, lis le mot. À deux, fais-le dicter sans le regarder.',[numeral(n) for n in [7,9,6,10,8]])
 A('Les crayons du pot','Cinq crayons sont déjà rangés dans le pot.',[total(5,n,'crayons') for n in [2,1,3,4,5]])
 fig=attach(8,frame(8),frame(8,True)+node(1.3,-1.9,'2 cases vides','otGreenDark'),'Boîte de dix cases contenant huit jetons et deux cases libres.')
 A('Les cases libres','Une boîte contient dix cases. Les cases libres sont sans jeton.',[missing(n,10,'jetons') for n in [8,9,7,6,5]],fig)
 fig=attach(9,frame(0),frame(10,True),'Boîte vide pour fabriquer dix ; corrigé en deux lignes pleines de cinq.')
 qs=[Q('Montre 10 doigts. Combien de mains de 5 doigts utilises-tu ?','Compter cinq sur chaque main.','Une main montre 5 doigts. Deux mains montrent $5+5=10$ doigts.','2 mains de 5 doigts.','sum',[1,1],2),Q('Fabrique 10 avec deux groupes de 5 jetons. Combien as-tu ?','Réunir les deux groupes.','$5+5=10$. Les deux groupes contiennent dix jetons.','10 jetons.','sum',[5,5],10),missing(6,10),missing(7,10),missing(9,10)]
 A('Fabriquer dix de plusieurs façons','Utilise tes mains, puis des jetons. Le dessin de boîte est un support.',qs,fig)
 finish('Les nombres entiers : de 6 à 10',8,frame(8,True),[('Reconnaître les quantités','Je remplis une première ligne de cinq. Puis je regarde les jetons de la seconde ligne.'),('Les nombres de six à dix','6 : six ; 7 : sept ; 8 : huit ; 9 : neuf ; 10 : dix. Je compte de 5 à 10 : 5 ; 6 ; 7 ; 8 ; 9 ; 10.'),('Dix cases en tout','Une boîte de dix a deux lignes de cinq cases. 10, c’est 5 et encore 5. Je peux compter les cases libres pour compléter la boîte.')],'Je regarde cinq et encore quelques jetons. Je vérifie en touchant chaque jeton.','8, c’est 5 et encore 3. Dans une boîte de dix, il reste 2 cases libres.')

def build03():
 begin(3)
 fig=attach(1,dots([5,7]),dots([5,7],True),'Deux collections de cinq et sept jetons, A et B.')
 A('Comparer deux groupes','Observe les deux groupes. Tu peux faire des paires sur ta feuille.',[Q('Quel groupe contient le plus de jetons ?','Compter puis comparer.','A contient 5 jetons. B en contient 7. B en a deux de plus.','Le groupe B.','choose',[[5,7],7],'B'),Q('Quel groupe contient le moins de jetons ?','Chercher la plus petite quantité.','5 est plus petit que 7. A contient 5 jetons.','Le groupe A.','choose',[[5,7],5],'A'),compare(5,7),missing(5,7),compare(7,5)],fig)
 A('Choisir le signe','La pointe du signe regarde le plus petit nombre.',[compare(a,b) for a,b in [(3,6),(8,4),(5,5),(0,2),(9,7)]])
 A('Ranger en ordre croissant','Croissant signifie du plus petit au plus grand.',[order(v) for v in [[7,2,5],[6,1,4],[8,3,5],[9,0,2],[5,1,3]]])
 A('Choisir le plus grand','Compare chaque paire.',[Q(f'Quel nombre est le plus grand : {a} ou {b} ?','Comparer les quantités.',f'{min(a,b)} est plus petit que {max(a,b)}.',str(max(a,b)),'max',[[a,b]],max(a,b)) for a,b in [(6,9),(8,7),(0,3),(4,2),(5,10)]])
 fig=attach(5,dots([6]),dots([6,6],True),'Six jetons modèles ; corrigé avec six ronds pour faire autant.')
 A('Dessiner autant','Fais un rond pour chaque jeton. La première ligne montre six jetons.',[draw(n) for n in [6,3,5,7,4]],fig)
 A('Ranger en ordre décroissant','Décroissant signifie du plus grand au plus petit.',[order(v,True) for v in [[1,9,4,6],[2,8,5,3],[7,0,4,2],[10,6,1,5],[3,9,2,7]]])
 fig=attach(7,dots([7,5]),dots([7,5],True),'Sept enfants et cinq chaises représentés par deux collections.')
 qs=[]
 for a,b in [(7,5),(6,4),(8,7),(5,5),(9,6)]:
  ans=a-b;qs.append(Q(f'Il y a {a} enfants et {b} chaises. Combien de chaises manque-t-il pour asseoir chacun ?','Donner une chaise à chaque enfant.',f'{b} enfants ont une chaise. Je compte les enfants encore debout : {ans}.',f'Il manque {ans} chaise'+('s.' if ans!=1 else '.'),'difference',[a,b],ans))
 A('Une chaise pour chacun','Un jeton représente un enfant ou une chaise selon la ligne.',qs,fig)
 A('Qui en a le moins ?','Noé et Inès comparent leurs cartes.',[Q(f'Noé a {a} cartes. Inès en a {b}. Qui en a le moins ?','Comparer les nombres de cartes.',f'{min(a,b)} est plus petit que {max(a,b)}.',('Noé' if a<b else 'Inès')+' en a le moins.','less_owner',[a,b],'Noé' if a<b else 'Inès') for a,b in [(8,6),(3,7),(9,4),(5,8),(10,7)]])
 fig=attach(9,dots([4,6],large=True),dots([4,6],True,large=True),'Quatre gros jetons et six jetons : la quantité se compare en comptant.')
 qs=[Q(f'Zoé a {a} gros cubes. Tom a {b} petits cubes. Zoé dit qu’elle en a plus. A-t-elle raison ?','Compter sans se laisser tromper par la taille.',f'Je compare les nombres. ${a}<{b}$. Un gros cube reste un seul cube.',f'Non. Tom a plus de cubes : {b} contre {a}.','compare',[a,b],'<') for a,b in [(4,6),(3,5),(5,7),(2,4),(6,8)]]
 A('La taille ne donne pas le nombre','Compte les objets. Leur taille et leur écart ne changent pas la quantité.',qs,fig)
 finish('Les nombres entiers : comparer des quantités',4,dots([4,6],True),[('Autant','Deux collections ont autant d’objets si chaque objet de l’une a un partenaire dans l’autre. Exemple : 5 = 5.'),('Plus et moins','Je fais des paires, un objet de chaque groupe. Le groupe qui garde des objets seuls en a plus. 4 < 6 : quatre est plus petit que six. 6 > 4 : six est plus grand que quatre.'),('Ranger','Dans l’ordre croissant, je vais du plus petit au plus grand : 2 < 5 < 7. Dans l’ordre décroissant, je vais du plus grand au plus petit : 7 > 5 > 2.')],'Je compte ou je fais des paires. Je ne compare pas la taille des objets.','A contient 4 jetons et B en contient 6. B en a plus ; A en a moins.')

def build07():
 begin(7)
 fig=attach(1,base(18),base(18,True),'Une barre de dix cubes et huit cubes isolés.')
 A('Lire des dizaines et unités','Chaque barre contient dix cubes.',[decomp(n) for n in [18,12,15,17,20]],fig)
 A('Compléter dix et encore','Trouve la partie manquante.',[Q(f'Complète : {n} = 10 + …','Chercher ce qui reste après dix.',f'Dans {n}, je prends 10. Il reste {n-10}.',f'{n} = 10 + {n-10}.','difference',[n,10],n-10) for n in [12,17,20,11,19]])
 fig=attach(3,base(10),base(14,True),'Une barre modèle de dix ; corrigé d’une dizaine et quatre unités.')
 A('Dessiner les dizaines','Dessine une barre comme le modèle. Ajoute les cubes isolés.',[Q(f'Dessine 1 dizaine et {u} unités. Écris le nombre.','Une barre représente dix cubes.',f'Je dessine une barre de dix et {u} cubes seuls. $10+{u}={10+u}$.',f'{10+u}, {mot(10+u)}.','sum',[10,u],10+u) for u in [4,2,6,8,9]],fig)
 A('Lire de onze à vingt','Lis chaque nombre à voix haute.',[numeral(n,'lettres') for n in [11,15,19,20,16]])
 A('La suite jusqu’à vingt','On avance d’un nombre.',[sequence(15,1,[2,4],6)]+[sequence(s,1,m) for s,m in [(11,[1,3]),(14,[1,4]),(16,[1,2]),(12,[2,4])]])
 A('Des mots aux nombres','Seul, lis le mot. À deux, demande une dictée sans voir les mots.',[numeral(n) for n in [13,16,18,20,14]])
 A('Le sachet de dix perles','Le sachet contient dix perles.',[total(10,u,'perles') for u in [5,2,6,8,9]])
 A('Atteindre deux dizaines','Deux paquets de dix contiennent vingt bâtonnets.',[missing(n,20,'bâtonnets') for n in [19,18,17,16,15]])
 fig=attach(9,base(14),base(14,True),'Quatorze cubes groupés en une dizaine et quatre unités.')
 A('La valeur des chiffres','Le chiffre placé à gauche indique les dizaines.',[
 Q('Léo dit : « Dans 14, le 1 vaut un seul cube. » Corrige sa phrase.','Regarder la place du chiffre.','Dans 14, le 1 indique une dizaine. Une dizaine contient 10 cubes.','Le 1 vaut 10 cubes, pas 1 cube.','digit',[14,1],10),
 Q('Dans 14, que vaut le chiffre 4 ?','Regarder la place des unités.','Le 4 indique quatre cubes seuls.','4 unités.','digit',[14,4],4),decomp(14),compare(14,4),
 Q('Échange les dix cubes de la barre contre des cubes seuls. Combien de cubes as-tu en tout avec les quatre unités ?','Un échange conserve la quantité.','La barre donne 10 cubes. Avec les 4 cubes seuls, je garde $10+4=14$ cubes.','14 cubes.','sum',[10,4],14)],fig)
 finish('Les nombres entiers : dizaines et unités de 11 à 20',16,base(16,True),[('Une dizaine','Dix unités forment une dizaine. Je peux échanger dix cubes seuls contre une barre de dix cubes.'),('Une dizaine et des unités','Dans 16, le 1 indique une dizaine. Le 6 indique six unités seules. 16 = 10 + 6. Je dis « seize ».'),('Lire jusqu’à vingt','11 : onze ; 12 : douze ; 13 : treize ; 14 : quatorze ; 15 : quinze ; 16 : seize ; 17 : dix-sept ; 18 : dix-huit ; 19 : dix-neuf ; 20 : vingt. 20, c’est deux dizaines.')],'Je garde la barre entière. Je compte les unités après dix.','13 = 10 + 3 : une dizaine et trois unités. 20 = 10 + 10.')

ORD=['premier','deuxième','troisième','quatrième','cinquième','sixième','septième','huitième','neuvième','dixième','onzième','douzième','treizième','quatorzième','quinzième','seizième','dix-septième','dix-huitième','dix-neuvième','vingtième']
def rank(chars,k):
 return Q(f'Dans la file « {" ; ".join(map(str,chars))} », quel élément est au rang {k} en partant de la gauche ?','Partir de la gauche et compter les places.',f'Je compte les places de 1 à {k}. À la place {k}, je trouve {chars[k-1]}.',str(chars[k-1]),'rank',[chars,k],chars[k-1])
def motif(pattern,k):
 arr=(pattern*20)[:20]
 return Q(f'Le motif « {" ; ".join(pattern)} » se répète. Quel élément est au rang {k} ?','Recopier le petit groupe qui se répète.',f'Je prolonge jusqu’au rang {k} : '+ ' ; '.join(arr[:k])+'. Je compte chaque place.',arr[k-1],'pattern',[pattern,k],arr[k-1])
def build08():
 begin(8)
 fig=attach(1,seq(list('ABCDE')),seq(list('ABCDE'),True,3),'File des lettres A à E, à lire depuis la gauche.')
 A('Trouver une place','La flèche montre le départ. Lis de gauche à droite.',[rank(list('ABCDE'),k) for k in [3,1,5,2,4]],fig)
 A('Les personnes devant','Dans chaque question, tu comptes ta propre place.',[Q(f'Tu es au rang {k}. Combien de personnes sont devant toi ?','Enlever sa propre place du rang.',f'Les places avant toi vont de 1 à {k-1}. Cela fait {k-1} personnes.',f'{k-1} personnes.','difference',[k,1],k-1) for k in [5,3,8,12,20]])
 A('Nommer les rangs','Lis le nombre puis donne le nom du rang.',[Q(f'Comment nomme-t-on le rang {k} ?','Relier le nombre à sa place dans la file.',f'Je récite les rangs dans l’ordre jusqu’à {k}. Le rang {k} se dit « {ORD[k-1]} ».',ORD[k-1],'ordinal',[k],ORD[k-1]) for k in [3,5,10,15,20]])
 fig=attach(4,seq(list('ABBABBA??')),seq(list('ABBABBABB'),True),'Motif A B B à prolonger par deux lettres.')
 A('Continuer un motif','Le groupe A B B se répète. Les points d’interrogation sont à remplacer.',[motif(list('ABB'),k) for k in [8,9,10,11,12]],fig)
 A('Le rang et la valeur','Dans toutes les questions, utilise cette file : 2 ; 4 ; 6 ; 8 ; 10.',[rank([2,4,6,8,10],k) for k in [4,1,5,2,3]])
 fig=attach(6,seq(list('ABABABABAB')),seq(list('ABABABABABABABABABAB'),True,19),'Début d’un motif A B ; corrigé prolongé jusqu’à la vingtième place.')
 A('Aller jusqu’au vingtième','Le motif A B se répète. Écris la suite sur ta feuille jusqu’à vingt places.',[motif(list('AB'),k) for k in [19,20,17,18,15]],fig)
 A('Les enfants derrière','Une file contient dix enfants. Le premier est à l’avant.',[Q(f'Mila est au rang {k} dans la file de 10. Combien d’enfants sont derrière elle ?','Compter les places après la sienne.',f'Les places après {k} sont '+ ' ; '.join(map(str,range(k+1,11)))+f'. Cela fait {10-k} places.',f'{10-k} enfants.','difference',[10,k],10-k) for k in [7,6,8,9,5]])
 fig=attach(8,shapes(3),shapes(8,True),'Le motif rond, carré, triangle ; corrigé prolongé au huitième rang.')
 A('Une frise de formes','Dessine la frise : un rond, un carré, un triangle. Recommence le même groupe.',[motif(['rond','carré','triangle'],k) for k in [8,7,9,10,11]],fig)
 fig=attach(9,seq(['o']*20),seq(['o']*20,True,20),'Vingt jetons en deux lignes successives de dix ; départ à gauche de la première ligne.')
 A('Changer le sens de lecture','Numérote vingt jetons de gauche à droite sur une seule ligne chez toi. Ici, la deuxième ligne continue la première.',[Q(f'Un jeton est au rang {k} en partant de la gauche dans une file de 20. Quel est son rang depuis la droite ?','Repartir de l’autre extrémité.',f'Il y a {20-k} jetons à sa droite. Depuis la droite, il arrive juste après eux : {20-k}+1={21-k}.',f'Rang {21-k} : {ORD[20-k]}.','reverse_rank',[20,k],21-k) for k in [20,19,18,15,1]],fig)
 finish('Les nombres ordinaux : rangs et suites de motifs',5,seq(list('ABABAB'),True),[('Le rang','Le rang indique une position. Je dois connaître le départ et le sens. Je touche chaque place en comptant.'),('De premier à vingtième','1 : premier ; 2 : deuxième ; 3 : troisième ; 4 : quatrième ; 5 : cinquième ; 6 : sixième ; 7 : septième ; 8 : huitième ; 9 : neuvième ; 10 : dixième ; 11 : onzième ; 12 : douzième ; 13 : treizième ; 14 : quatorzième ; 15 : quinzième ; 16 : seizième ; 17 : dix-septième ; 18 : dix-huitième ; 19 : dix-neuvième ; 20 : vingtième.'),('Prolonger un motif','Je cherche le petit groupe qui se répète. Dans A B A B A B, le groupe A B se répète. La cinquième lettre est A.')],'Je distingue le rang et la quantité. Le cinquième a quatre personnes devant lui.','Dans A B C A B C, la quatrième lettre est A. Changer le départ peut changer le rang.')

def regroup(d,u):
 n=10*d+u;dd,uu=divmod(n,10)
 return Q(f'Tu as {d} dizaines et {u} unités seules. Regroupe les unités par dix. Combien as-tu en tout ?','Échanger dix unités contre une dizaine.',f'{u} unités donnent {u//10} nouvelle'+('s dizaines' if u//10>1 else ' dizaine')+f' et {u%10} unités. Avec les {d} dizaines, cela fait {dd} dizaines et {uu} unités.',f'{10*d} + {u} = {n}.','regroup',[d,u],n)
def build09():
 begin(9)
 fig=attach(1,base(52),base(52,True),'Cinq barres de dix et deux cubes seuls : quantité à lire.')
 A('Lire des collections groupées','Chaque barre contient dix cubes.',[decomp(n) for n in [52,34,43,26,58]],fig)
 A('Décomposer les nombres','Écris les dizaines puis les unités.',[decomp(n) for n in [26,40,58,31,49]])
 A('Écrire en chiffres','Lis le mot. Puis écris le nombre.',[numeral(n) for n in [39,21,50,47,32]])
 A('Écrire en lettres jusqu’à cinquante','Écris le nom complet de chaque nombre.',[numeral(n,'lettres') for n in [24,35,46,50,41]])
 A('Franchir une dizaine','Le nombre qui suit 39 est 40.',[sequence(s,1,m) for s,m in [(37,[2,3]),(27,[2,3]),(47,[2,3]),(35,[1,3]),(54,[1,3])]])
 fig=attach(6,base(30)+node(1.3,-.55,'Ajoute 12 cubes seuls.'),base(42,True),'Trois dizaines et douze unités à regrouper ; corrigé en quatre dizaines et deux unités.')
 A('Échanger dix unités','Prépare les dizaines. Ajoute les unités puis fais un nouveau paquet de dix.',[regroup(d,u) for d,u in [(3,12),(2,14),(4,13),(1,16),(3,18)]],fig)
 A('Ranger les crayons','On range les crayons dans des paquets de dix. On garde les autres seuls.',[Q(f'Range {n} crayons. Combien de paquets complets et de crayons isolés ?','Faire le plus de paquets de dix possible.',f'Je fais {n//10} paquets de dix. Cela utilise {n//10*10} crayons. Il reste {n%10} crayons.',f'{n//10} paquets et {n%10} crayons isolés.','decompose',[n],list(divmod(n,10))) for n in [47,32,58,40,26]])
 A('Une petite dictée de nombres','Seul, lis le mot. À deux, fais dicter sans regarder.',[numeral(n) for n in [32,45,59,28,51]])
 fig=attach(9,base(25)+r'\begin{scope}[xshift=4cm]'+base(52)+r'\end{scope}',base(25,True)+r'\begin{scope}[yshift=-4.5cm]'+base(52,True)+r'\end{scope}','Vingt-cinq et cinquante-deux : mêmes chiffres, valeurs différentes.')
 # Éviter une planche trop large en énoncé : empiler les deux quantités.
 FIGS['ex9_enonce']=FIGS['ex9_enonce'].replace('xshift=4cm','yshift=-4.5cm')
 qs=[Q('Dans 25, que vaut le chiffre 2 ?','Regarder la colonne des dizaines.','Le 2 est à gauche : il indique 2 dizaines. Deux dizaines valent 20.','20.','digit',[25,2],20),Q('Dans 52, que vaut le chiffre 2 ?','Regarder la colonne des unités.','Le 2 est à droite : il indique 2 unités.','2.','digit',[52,2],2),compare(25,52),Q('Dans 34, que vaut le chiffre 3 ?','Repérer les dizaines.','Le 3 indique trois dizaines, donc 30.','30.','digit',[34,3],30),Q('Dans 43, que vaut le chiffre 3 ?','Repérer les unités.','Le 3 indique trois unités.','3.','digit',[43,3],3)]
 A('La place change la valeur','Compare les deux représentations.',qs,fig)
 finish('Les nombres entiers : lire et écrire jusqu’à 59',34,base(34,True),[('Des dizaines et des unités','Je fais des paquets de dix. Le chiffre de gauche indique les dizaines. Le chiffre de droite indique les unités seules. 34 = 30 + 4.'),('Lire et écrire','20 : vingt ; 30 : trente ; 40 : quarante ; 50 : cinquante. 21 : vingt-et-un ; 34 : trente-quatre ; 46 : quarante-six ; 59 se lit « cinquante-neuf ». Je m’entraîne à écrire les noms jusqu’à cinquante.'),('Faire un échange','Dix unités seules deviennent une dizaine. Trois dizaines et douze unités font quatre dizaines et deux unités : 30 + 12 = 42. Dans 25, le 2 vaut 20 ; dans 52, il vaut 2.')],'Je groupe d’abord par dix. Je lis les dizaines puis les unités.','42 = 40 + 2. Le chiffre 4 vaut 40. Ne confonds pas 34 et 43.')

def build10():
 begin(10)
 fig=attach(1,line(30,40,[32,35,38]),line(30,40,[32,35,38],True),'Ligne de trente à quarante : trois graduations sans nombre.')
 qs=[Q(f'Quel nombre manque {n-30} intervalles après 30 ?','Compter les espaces entre les traits.',f'Chaque intervalle vaut 1. Depuis 30, je fais {n-30} pas : j’arrive à {n}.',str(n),'sum',[30,n-30],n) for n in [32,35,38]]+[Q('Combien vaut un intervalle sur cette ligne ?','Lire deux graduations voisines.','Les deux premiers traits portent 30 et 31. L’écart est 1.','1.','difference',[31,30],1),Q('Combien d’intervalles séparent 30 et 40 ?','Compter les espaces, sans compter le point de départ.','Je fais dix pas de 1 pour aller de 30 à 40.','10 intervalles.','difference',[40,30],10)]
 A('Lire une ligne graduée','Les traits sont régulièrement espacés. Chaque espace vaut un.',qs,fig)
 A('Comparer les nombres','Compare les dizaines. Si elles sont égales, compare les unités.',[compare(a,b) for a,b in [(28,31),(46,43),(50,50),(39,40),(52,49)]])
 A('Ranger des nombres','Range du plus petit au plus grand.',[order(v) for v in [[41,14,39,50,28],[32,23,45,54,19],[17,48,36,29,50],[40,9,27,33,51],[46,24,57,38,15]]])
 A('Avant et après une dizaine','Récite la suite autour du nombre demandé.',[before(40),before(40,True),before(30),before(30,True),before(50)])
 fig=attach(5,line(35,40),line(35,40,answer=True,mark=37),'Ligne graduée de trente-cinq à quarante ; corrigé avec trente-sept repéré.')
 qs=[]
 for a,b in [(36,39),(31,34),(42,45),(26,29),(51,54)]:
  qs.append(Q(f'Donne un nombre strictement entre {a} et {b}.','Choisir un nombre après le premier et avant le second.',f'Après {a}, je trouve {a+1}. Il est encore plus petit que {b}.',f'Par exemple {a+1}. {a+2} convient aussi.','between',[a,b],a+1))
 A('Entre deux nombres','Le nombre choisi ne doit être égal à aucune des deux bornes.',qs,fig)
 A('Entre deux dizaines','Cherche la dizaine juste avant et celle juste après.',[Q(f'Encadre {n} entre deux dizaines entières.','Repérer la famille de la dizaine.',f'{n} est plus grand que {n//10*10} et plus petit que {(n//10+1)*10}.',f'${n//10*10} < {n} < {(n//10+1)*10}$.','bound',[n],[n//10*10,(n//10+1)*10]) for n in [47,32,26,58,19]])
 A('Comparer des collections de cartes','Mina et Adam comptent leurs cartes.',[Q(f'Mina a {a} cartes. Adam en a {b}. Qui en a le plus ?','Comparer les dizaines puis les unités.',f'{max(a,b)} est plus grand que {min(a,b)}.',('Mina' if a>b else 'Adam')+' en a le plus.','more_owner',[a,b],'Mina' if a>b else 'Adam') for a,b in [(38,35),(42,39),(26,29),(51,48),(34,37)]])
 fig=attach(8,line(30,40),line(30,40,mark=34),'Ligne graduée de trente à quarante pour avancer un pion de deux cases.')
 A('Avancer sur la ligne','Chaque case vaut un. Pour chaque question, repars du nombre annoncé.',[Q(f'Le pion part de {n}. Il avance de 2 cases. Où arrive-t-il ?','Compter deux espaces vers la droite.',f'Premier pas : {n+1}. Deuxième pas : {n+2}.',str(n+2),'sum',[n,2],n+2) for n in [32,34,36,31,37]],fig)
 fig=attach(9,line(20,26,[23,24,25]),line(20,26,[23,24,25],True,25),'Ligne de vingt à vingt-six pour vérifier trois intervalles après vingt-deux.')
 qs=[Q('Tom place 25 trois intervalles après 22. Est-ce correct ?','Compter les intervalles depuis 22.','Depuis 22, je passe par 23, puis 24, puis 25. Cela fait trois pas.','Oui : 22 + 3 = 25.','sum',[22,3],25)]+[Q(f'Où arrive-t-on {k} intervalles après {a} ?','Ne pas compter le départ comme un pas.',f'J’avance de {k} espaces. ${a}+{k}={a+k}$.',str(a+k),'sum',[a,k],a+k) for a,k in [(20,3),(21,2),(23,3),(22,2)]]
 A('Vérifier les espaces','Tous les espaces ont la même valeur : un.',qs,fig)
 finish('Les nombres entiers : comparer, ranger et repérer',35,line(30,40,mark=35),[('Comparer','Je compare d’abord les dizaines. Si elles sont égales, je compare les unités. 36 < 42 car trois dizaines sont moins que quatre dizaines. 46 > 43 car six unités sont plus que trois unités.'),('Ranger et encadrer','Croissant : du plus petit au plus grand. 14 < 28 < 39 < 41 < 50. Encadrer 47 par les dizaines donne 40 < 47 < 50.'),('La ligne graduée','Les intervalles égaux montrent le même écart. Je lis deux graduations voisines pour connaître cet écart. Ici chaque intervalle vaut 1. 35 est cinq intervalles après 30.')],'Je compte les espaces parcourus. Le point de départ n’est pas le premier pas.','De 32, deux pas vers la droite mènent à 34. 39 vient juste avant 40 ; 41 vient juste après.')

def build13():
 begin(13)
 fig=attach(1,base(71),base(71,True),'Sept dizaines et une unité : quantité soixante-et-onze.')
 A('Lire les dizaines jusqu’à cent','Chaque barre contient dix cubes. Lis aussi le nom du nombre à voix haute.',[decomp(n) for n in [71,86,93,60,100]],fig)
 A('Des noms aux chiffres','Lis chaque nom puis écris le nombre.',[numeral(n) for n in [68,75,92,81,99]])
 A('Décomposer jusqu’à cent','Les noms sont parfois irréguliers. Les paquets de dix restent réguliers.',[decomp(n) for n in [69,80,97,100,74]])
 A('Franchir quatre-vingts','On avance d’un nombre à chaque place.',[sequence(s,1,m) for s,m in [(78,[2,3]),(68,[2,3]),(88,[2,3]),(95,[2,4]),(76,[1,3])]])
 A('Compter de deux en deux','Ajoute deux à chaque fois. Tous les nombres restent au plus égaux à cent.',[sequence(s,2,m) for s,m in [(89,[2,3,4]),(80,[1,3]),(70,[2,4]),(91,[1,3]),(60,[2,3])]])
 A('Ranger les grands nombres','Range du plus grand au plus petit.',[order(v,True) for v in [[76,67,100,89,98],[82,72,92,62,99],[61,81,71,91,100],[95,59,85,68,78],[66,96,86,76,60]]])
 A('Les places de l’album','L’album a cent places. Une image occupe une place.',[missing(n,100,'images') for n in [90,80,70,60,100]])
 fig=attach(8,base(80)+node(2,-.55,'Ajoute 12 crayons seuls.'),base(92,True),'Huit dizaines et douze crayons seuls ; corrigé en neuf dizaines et deux unités.')
 A('Regrouper encore une dizaine','Dix crayons isolés peuvent faire un paquet de dix.',[regroup(d,u) for d,u in [(8,12),(6,15),(7,14),(8,19),(7,20)]],fig)
 A('Lire et écrire jusqu’à cent','Seul, lis les noms puis écris les chiffres. À deux, fais une dictée sans regarder les mots.',[numeral(n) for n in [60,79,81,94,100]])
 finish('Les nombres entiers : de 60 à 100',86,base(86,True),[('Des paquets de dix','74 contient sept dizaines et quatre unités. 74 = 70 + 4. Le nom peut être irrégulier, mais les dizaines et les unités ne changent pas.'),('Les noms à connaître','60 : soixante ; 70 : soixante-dix ; 71 : soixante-et-onze ; 80 : quatre-vingts ; 81 : quatre-vingt-un ; 90 : quatre-vingt-dix ; 100 : cent. 86 se lit « quatre-vingt-six » ; 93 se lit « quatre-vingt-treize ».'),('Atteindre cent','100, c’est dix dizaines. Après 99 vient 100. Pour comparer, je regarde les dizaines puis les unités. 89 < 98 < 100.')],'Je peux dire le nom à voix haute et montrer les paquets de dix pour vérifier.','93 = 90 + 3. Huit dizaines et douze unités donnent neuf dizaines et deux unités : 92.')

def finish(title,n,example,sections,method,remember):
 d=next(ROOT.glob(f'{CODE:02}_*'))
 pic('lecon',example)
 def accords(t):
  return re.sub(r'(?<!\d)1 (jetons|cubes|ronds|crayons|bâtonnets|images|dizaines|unités|paquets|personnes|enfants|places|mains)\b',lambda m:'1 '+m[1][:-1],t)
 for item in ITEMS:
  for question in item['questions']:
   for key in ['question','methode','resultat']:question[key]=accords(question[key])
   question['etapes']=[accords(t) for t in question['etapes']]
 for key in FIGS:FIGS[key]=accords(FIGS[key])
 caption={1:'Voici quatre jetons.',2:'Voici huit jetons : cinq et encore trois.',3:'A contient quatre jetons. B en contient six.',7:'Voici seize cubes : une dizaine et six unités.',8:'Le groupe A B se répète. La cinquième lettre est A.',9:'Voici trente-quatre cubes : trois dizaines et quatre unités.',10:'La flèche montre trente-cinq.',13:'Voici quatre-vingt-six cubes : huit dizaines et six unités.'}[CODE]
 intro='::: objectifs\n'+json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf-8'))['objectif']+'\n:::\n'
 course=f'Titre: {title}\n\n<!-- optitab:1 -->\n'+intro
 for i,(head,text) in enumerate(sections):course+=f'\n## {"I II III".split()[i]}. {head}\n\n::: '+('definition' if i==0 else 'propriete')+f'\n{text}\n:::\n'+ ('\n'+caption+'\n\n[IMAGE_1]\n' if i==0 else '')
 caution={1:'Réciter les nombres ne suffit pas. Je touche chaque objet une seule fois.',2:'La boîte montre une quantité. Elle ne donne pas la forme du chiffre.',3:'La taille et l’écartement des objets ne donnent pas leur nombre.',7:'Dans 14, le 1 placé à gauche vaut dix cubes.',8:'Le rang change si je change le départ.',9:'Ne confonds pas 34 et 43. La place de chaque chiffre compte.',10:'Je compte les espaces, pas le point de départ.',13:'Le nom oral est parfois irrégulier. Je vérifie avec les paquets de dix.'}[CODE]
 course+='\n::: methode Pour réussir\n'+method+'\n:::\n\n::: exemple\n'+remember+'\n:::\n\n::: attention\n'+caution+'\n:::\n\n::: retenir\n'+remember+'\n:::\n'
 memo={1:'0 : zéro ; 1 : un ; 2 : deux ; 3 : trois ; 4 : quatre ; 5 : cinq.',2:'6 : six ; 7 : sept ; 8 : huit ; 9 : neuf ; 10 : dix.',3:'Autant : =. Plus petit : <. Plus grand : >.',7:'11 : onze ; 12 : douze ; 13 : treize ; 14 : quatorze ; 15 : quinze ; 16 : seize ; 17 : dix-sept ; 18 : dix-huit ; 19 : dix-neuf ; 20 : vingt.',8:'1 : premier ; 2 : deuxième ; 3 : troisième ; 10 : dixième ; 20 : vingtième. Un motif est un petit groupe qui se répète.',9:'20 : vingt ; 30 : trente ; 40 : quarante ; 50 : cinquante.',10:'Croissant : du plus petit au plus grand. Décroissant : du plus grand au plus petit.',13:'70 : soixante-dix ; 80 : quatre-vingts ; 90 : quatre-vingt-dix ; 100 : cent. Cent, c’est dix dizaines.'}[CODE]
 fiche=f'Titre: {title}\n\n<!-- optitab:1 -->\n::: retenir\n'+sections[0][1]+'\n:::\n\n'+caption+'\n\n[IMAGE_1]\n\n::: propriete\n'+memo+'\n:::\n\n::: methode\n'+method+'\n:::\n\n::: exemple\n'+remember+'\n:::\n\n::: attention\n'+caution+'\n:::\n'
 (d/'cours_nouveau.txt').write_text(course,encoding='utf-8');(d/'fiche_nouvelle.txt').write_text(fiche,encoding='utf-8')
 if CODE in [7,9,13]:ITEMS[0]['questions'][0]['question']='Écris le nombre représenté. Combien de dizaines et d’unités vois-tu ?'
 if CODE==8:ITEMS[8]['questions'][0]['question']='Entoure le vingtième jeton en partant de la gauche. Quel est son rang en partant de la droite ?'
 write(CODE,ITEMS)
 correspond={'cours':{'nouveau':{'1':{'fichier':'lecon.png','alt':'Exemple visuel expliqué : '+title}}},'fiches':{'nouvelle':{'1':{'fichier':'lecon.png','alt':'Mémo visuel : '+title}}},'exercices':{f'nouveau-{i}':it['figures'] for i,it in enumerate(ITEMS,1) if it['figures']}}
 (d/'figures/correspondance.json').write_text(json.dumps(correspond,ensure_ascii=False,indent=2),encoding='utf-8')
 (d/'figures/figures.py').write_text('# Figures TikZ, compilation par outils/figures_livre.py\nFIGURES = {\n'+''.join(repr(k)+': r"""'+v+'""",\n' for k,v in FIGS.items())+'}\n',encoding='utf-8')
 sources=json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf-8'))['exercices']
 (d/'COUVERTURE.md').write_text('# Couverture des neuf activités sources\n\n'+ '\n\n'.join(f'## Activité {i}\n\nSource : « {src["consigne"]} »\n\nReprise : exercice nouveau-{i}, « {it["titre"]} ». Cinq questions avec méthode, raisonnement et réponse.\nPremière question : {it["questions"][0]["question"]}' for i,(src,it) in enumerate(zip(sources,ITEMS),1))+'\n\nLes dictées conservent une modalité orale avec un adulte et proposent une lecture autonome. Les constructions restent des dessins ou manipulations, avec modèle et corrigé.\n',encoding='utf-8')
 (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'cp_nombres','maj':'2026-11-02'},ensure_ascii=False),encoding='utf-8')

if __name__=='__main__':
 for f in [build01,build02,build03,build07,build08,build09,build10,build13]:f()
