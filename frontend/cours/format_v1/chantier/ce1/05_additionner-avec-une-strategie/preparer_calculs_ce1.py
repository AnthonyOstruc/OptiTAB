"""Prépare exclusivement les chapitres CE1 05–13, sans compilation ni import.
Les sources restent intactes. Les résultats sont vérifiés dans les textes produits.
"""
from pathlib import Path
import json,re,ast

ROOT=Path(__file__).resolve().parent.parent
MARK='<!-- optitab:1 -->'
BS=chr(92)
PROGRAMME='https://www.education.gouv.fr/sites/default/files/document/Annexe%204%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20du%20cycle%202-403821.pdf'

def val(s):return eval(s,{'__builtins__':{}})
def tex(s):return str(s).replace('*',BS+'times ')
def f(s):return '$'+tex(s)+'$'
def eq(s):return f(s+'='+str(val(s)))
def boxes(t,b,title=''):return '::: '+t+(' '+title if title else '')+'\n'+b+'\n:::'
def task(prompt,method,work,result):return dict(question=prompt,methode=method,etapes=[work],resultat=result)
def chain(*expr):return '\n\n'.join(eq(e)+'.' for e in expr)

NAMES=['unités','dizaines','centaines','milliers']
def counted(number,name):return str(number)+' '+(name[:-1] if number==1 else name)
def add_columns(nums):
 carry=0;out=[]
 width=max(len(str(v)) for v in nums)
 for k in range(width):
  ds=[v//10**k%10 for v in nums];old=carry;total=sum(ds)+old
  expr='+'.join(map(str,ds))+('+'+str(old) if old else '')
  out.append(f'Au rang des {NAMES[k]}, '+eq(expr)+'.')
  carry=total//10
  if carry:out.append(counted(total,NAMES[k])+' donnent '+counted(total%10,NAMES[k])+' et '+counted(carry,NAMES[k+1])+f'. J’écris {total%10} dans ce rang et je reporte {carry} au rang suivant.')
  else:out.append(f"J’écris {total} dans ce rang ; aucune retenue ne part de ce rang.")
 if carry:out.append(f"Le nouveau rang des {NAMES[width]} contient {carry}.")
 out.append(eq('+'.join(map(str,nums)))+'.')
 return '\n\n'.join(out)

def sub_columns(a,b):
 width=len(str(a));digits=[a//10**i%10 for i in range(width)];out=[]
 for k in range(width):
  digit=b//10**k%10
  if digits[k]<digit:
   j=k+1
   while digits[j]==0:j+=1
   out.append(f"Au rang des {NAMES[k]}, {digits[k]} ne suffit pas pour retirer {digit}.")
   for t in range(j,k,-1):
    digits[t]-=1;digits[t-1]+=10
    out.append(f"J’échange 1 {NAMES[t][:-1]} contre 10 {NAMES[t-1]}. Il reste "+counted(digits[t],NAMES[t])+" et j’ai maintenant "+counted(digits[t-1],NAMES[t-1])+'.')
  out.append(f'Je retire les {NAMES[k]} : '+eq(f'{digits[k]}-{digit}')+'.')
  digits[k]-=digit
 out.append(eq(f'{a}-{b}')+'.')
 return '\n\n'.join(out)

def add_mental(a,b):
 if b%10==9:
  near=b+1
  return 'Je remplace '+f(str(b))+' par '+f(str(near))+', ce qui ajoute une unité de trop. Je la retire ensuite.\n\n'+chain(f'{a}+{near}',f'{a+near}-1',f'{a}+{b}')
 parts=[int(c)*10**k for k,c in enumerate(reversed(str(b))) if c!='0'][::-1]
 out=[f'Je décompose {b} : '+eq('+'.join(map(str,parts)))+'.'];cur=a
 for p in parts:out.append('J’ajoute '+str(p)+' : '+eq(f'{cur}+{p}')+'.');cur+=p
 out.append('Je conclus : '+eq(f'{a}+{b}')+'.')
 return '\n\n'.join(out)

def sub_mental(a,b):
 if b==9:
  return 'Retirer 10 enlève une unité de trop : je rends cette unité.\n\n'+chain(f'{a}-10',f'{a-10}+1',f'{a}-9')
 if b<10 and a%10<b:
  first=a%10;second=b-first
  if first:return f'Je sépare {b} en {first} et {second}. Le premier retrait atteint une dizaine entière.\n\n'+chain(f'{a}-{first}',f'{a-first}-{second}',f'{a}-{b}')
  return f'Je pars d’une dizaine entière. Je retire d’abord {b} de 10, puis je réunis ce reste avec {a-10}.\n\n'+chain(f'10-{b}',f'{a-10}+{10-b}',f'{a}-{b}')
 parts=[int(c)*10**k for k,c in enumerate(reversed(str(b))) if c!='0'][::-1];cur=a
 out=[f'Je sépare le retrait {b} en centaines, dizaines et unités : '+eq('+'.join(map(str,parts)))+'.']
 for p in parts:out.append('Je retire '+str(p)+' : '+eq(f'{cur}-{p}')+'.');cur-=p
 return '\n\n'.join(out)

def mul_work(a,b,code):
 if not a or not b:return 'Un facteur est zéro : il n’y a aucun groupe, ou aucun objet dans les groupes.\n\n'+eq(f'{a}*{b}')+'.'
 if a==1 or b==1:return 'Une seule fois une quantité garde cette quantité.\n\n'+eq(f'{a}*{b}')+'.'
 if code==12:
  if a==10 or b==10:
   x=b if a==10 else a
   return f'{x} unités deviennent {x} dizaines. Chaque chiffre prend une valeur dix fois plus grande : les unités deviennent des dizaines, les dizaines deviennent des centaines.\n\n'+eq(f'{a}*{b}')+'.'
  if 11<=b<=19:a,b=b,a
  if 11<=a<=19:
   low=a-10
   return f'Je sépare {a} en 10 et {low}. Je multiplie **les deux parties** par {b}, puis je réunis.\n\n'+chain(f'10*{b}',f'{low}*{b}',f'{10*b}+{low*b}',f'{a}*{b}')
 if code==13 and (a==2 or b==2):
  x=b if a==2 else a;parts=[int(c)*10**k for k,c in enumerate(reversed(str(x))) if c!='0'][::-1]
  return 'Le double réunit deux quantités égales. Je double séparément les morceaux du nombre.\n\n'+ '\n\n'.join(eq(f'{p}+{p}')+'.' for p in parts)+'\n\n'+eq('+'.join(str(2*p) for p in parts))+'.\n\n'+eq(f'{a}*{b}')+'.'
 if code==10 and (a==4 or b==4):
  x=b if a==4 else a
  return 'Quatre groupes se construisent en doublant deux fois.\n\n'+chain(f'{x}+{x}',f'{2*x}+{2*x}',f'{a}*{b}')
 if code==11:
  if a==9:return 'Je prends dix groupes puis j’en retire un.\n\n'+chain(f'10*{b}',f'{10*b}-{b}',f'{a}*{b}')
  if a==8:return 'Je prends quatre groupes, puis je double cette quantité.\n\n'+chain(f'4*{b}',f'{4*b}+{4*b}',f'{a}*{b}')
  if a>=6:return f'Je sépare les {a} groupes en cinq groupes et '+counted(a-5,'groupes')+'.\n\n'+chain(f'5*{b}',f'{a-5}*{b}',f'{5*b}+{(a-5)*b}',f'{a}*{b}')
 if code==13 and b==25:return 'Je compte les paquets de 25 en ajoutant 25 à chaque fois.\n\n'+eq('+'.join(['25']*a))+'.\n\n'+eq(f'{a}*{b}')+'.'
 if a<=10:return f'Je compte {a} groupes de {b}. Chaque nouveau groupe ajoute {b}.\n\n'+eq('+'.join([str(b)]*a))+'.\n\n'+eq(f'{a}*{b}')+'.'
 return f'Je compte {b} groupes de {a} en changeant l’ordre des facteurs.\n\n'+eq('+'.join([str(a)]*b))+'.\n\n'+eq(f'{a}*{b}')+'.'

def half_work(a,parts=None):
 if parts is None:parts=[int(c)*10**k for k,c in enumerate(reversed(str(a))) if c!='0'][::-1]
 if any(p%2 for p in parts):
  # Un nombre de dizaines impair se partage avec ses unités : 26=20+6.
  h=a//2;parts=[2*(h//10*10),2*(h%10)];parts=[p for p in parts if p]
 assert sum(parts)==a and all(p%2==0 for p in parts)
 out=['Je cherche deux parts égales. Je décompose '+str(a)+' en morceaux faciles à partager : '+eq('+'.join(map(str,parts)))+'.']
 for p in parts:out.append(f'La moitié de {p} est {p//2}, car '+eq(f'{p//2}+{p//2}')+'.')
 out.append('Je réunis les moitiés : '+eq('+'.join(str(p//2) for p in parts))+'.')
 out.append('Je vérifie : '+eq(f'{a//2}+{a//2}')+'.')
 return '\n\n'.join(out)

def calc(expr,code,prompt=None):
 if '//' in expr:
  a,b=map(int,expr.split('//'));assert b==2 and a%2==0
  return task(prompt or f'Trouve la moitié de {a}.','Je partage séparément des morceaux pairs, puis je réunis leurs moitiés.',half_work(a),f'La moitié de {a} est {a//2}.')
 if '+' in expr:
  nums=list(map(int,expr.split('+')))
  if code==6:method='J’aligne unités, dizaines et centaines ; je commence par les unités et je reporte chaque échange.';work=add_columns(nums)
  elif len(nums)==2:method='Je décompose le nombre ajouté ou je passe par la dizaine suivante en corrigeant l’unité de trop.';work=add_mental(*nums)
  else:method='Je réunis les groupes égaux un à un.';work=chain(expr)
 elif '-' in expr:
  a,b=map(int,expr.split('-'));method='J’aligne les rangs et j’échange une unité du rang supérieur quand le retrait est impossible.' if code==8 else 'Je retire les dizaines ou les centaines séparément ; pour un petit retrait, je passe par une dizaine.';work=sub_columns(a,b) if code==8 else sub_mental(a,b)
 else:
  a,b=map(int,expr.split('*'));method={9:'Je compte des groupes égaux ; changer leur organisation ne change pas le total.',10:'Je reconstruis le produit avec une table connue, des groupes égaux ou deux doubles.',11:'Je partage les groupes en cinq groupes et un complément, ou je pars de dix groupes.',12:'Je sépare dix et les unités restantes ; je multiplie chacune des deux parties.',13:'Je réunis deux quantités égales ou je compte les groupes de 25.'}[code];work=mul_work(a,b,code)
  if code==12 and 10 in (a,b):method='Je transforme des unités en dizaines ; chaque chiffre prend une valeur dix fois plus grande.'
 return task(prompt or 'Calcule '+f(expr)+'.',method,work,eq(expr)+'.')

TITLES={
5:['Comprendre le détour par vingt','Ajouter dizaines et centaines','Ajouter neuf, dix-neuf ou vingt-neuf','Compléter jusqu’à une dizaine ou une centaine','Décomposer le nombre ajouté','Choisir une addition courte','Compléter le stock de cahiers','Recevoir des livres','Corriger le sens de compensation'],
6:['Additionner sans retenue','Échanger dans deux rangs','Aligner un nombre plus court','Réunir trois quantités','Écrire un résultat avec des zéros','Atteindre mille','Réunir les feuilles','Totaliser les trois écoles','Placer un chiffre d’unités'],
7:['Retirer en deux sauts','Retirer dizaines et centaines','Franchir une dizaine','Retirer neuf','Choisir le bon découpage','Retrouver la quantité manquante','Prélever des vis','Prendre neuf feuilles','Contrôler le sens d’un retrait'],
8:['Soustraire sans échange','Échanger une dizaine','Faire passer un échange par zéro','Partir de cinq centaines','Aligner un petit nombre','Retirer à mille','Compléter un album','Distribuer des crayons','Vérifier une différence annoncée'],
9:['Lire une collection en lignes et colonnes','Écrire une addition répétée','Dessiner des groupes égaux','Classer les nombres pairs et impairs','Continuer une suite de nombres pairs','Multiplier par zéro ou par un','Compter les places','Former des paires de cubes','Changer l’organisation des groupes'],
10:['Compter cinq rangées de quatre','Relier les tables de deux, trois et quatre','Utiliser cinq et dix groupes','Retrouver un facteur','Construire la table de trois','Doubler deux fois','Remplir les boîtes de feutres','Partager les cartes','Fabriquer cinq cartes de calcul'],
11:['Lire six rangées de sept','S’appuyer sur les produits connus','Compléter les facteurs','Prendre dix groupes moins un','Doubler quatre groupes','Mémoriser les produits carrés','Compter les balles','Former des équipes de huit','Échanger les facteurs'],
12:['Donner aux chiffres une valeur dix fois plus grande','Compter les dizaines','Multiplier chaque partie','Calculer avec un facteur entre onze et dix-neuf','Décomposer le second facteur','Retrouver des dizaines','Réunir dix paquets','Compter les crayons de plusieurs boîtes','Ne pas oublier les unités'],
13:['Partager cinq-cent-soixante','Doubler des petits nombres','Partager en deux parts égales','Doubler des centaines','Prendre la moitié de centaines','Compter de vingt-cinq en vingt-cinq','Réunir deux classes','Partager les perles','Choisir des morceaux faciles à partager']}

def source_exprs(source):
 out=[]
 for cond in source.get('check','').split(' and '):
  s=cond.split('==')[0]
  if re.fullmatch(r'\d+(?:[+*\-]\d+)+',s):out.append(s)
 return out

def core(source,code,i):
 exprs=source_exprs(source)
 if code==13 and i in (1,3,5,8,9):
  nums={1:[560],3:[26,50,70,90],5:[300,500,600,1000],8:[486],9:[738]}[i]
  qs=[calc(f'{v}//2',13) for v in nums]
  if i==1:qs[0]['etapes']=[half_work(560,[400,160])]
  if i==9:qs[0]['etapes']=[half_work(738,[600,120,18])]
  result=' ; '.join(q['resultat'].rstrip('.') for q in qs)+'.'
  if i==8:result+=' Chaque part contient 243 perles.'
  return task(source['consigne'].replace('1 000','1\u00a0000'),qs[0]['methode'],'\n\n'.join(q['etapes'][0] for q in qs),result),f'{nums[0]}//2'
 if code==9 and i in (4,5,8,9):
  if i==4:
   work='Le chiffre des unités décide si l’on peut former des paires sans reste. Les chiffres 0, 2, 4, 6 et 8 terminent les nombres pairs.\n\n124 se termine par 4 et 678 par 8 : ils sont pairs. 305 se termine par 5 et 911 par 1 : ils sont impairs.'
   return task(source['consigne'],'Je regarde le chiffre des unités et je cherche s’il reste un objet après les paires.',work,'Pairs : 124 et 678. Impairs : 305 et 911.'),'124'
  if i==5:return task(source['consigne'],'Je pars de la borne paire et j’ajoute 2 jusqu’à la borne finale.',chain('768+2','770+2','772+2','774+2','776+2')+'\n\nAjouter 2 conserve la possibilité de former des paires sans reste. Les deux bornes demandées sont incluses.','768 ; 770 ; 772 ; 774 ; 776 ; 778.'),'768'
  if i==8:return task(source['consigne'],'Je cherche le plus grand nombre de groupes de deux qui ne dépasse pas 17.',chain('8*2','17-16','8*2+1')+'\n\nLes 16 premiers cubes forment 8 paires ; le dernier n’a pas de partenaire.','8 paires complètes et 1 cube isolé ; 17 est impair.'),'17'
  return task(source['consigne'],'Je compte le même rectangle dans les deux sens.',mul_work(3,8,9)+'\n\n'+mul_work(8,3,9)+'\n\nLes lignes deviennent les colonnes, mais aucun objet n’est ajouté ni retiré.',f('3*8=24')+' et '+f('8*3=24')+' : les deux totaux sont égaux.'),'3*8'
 if code==10 and i==5:
  work='Je pars de zéro groupe. Chaque groupe supplémentaire apporte 3 objets.\n\n'+'\n\n'.join(eq(f'{v}*3')+'.' for v in range(11))
  return task(source['consigne'],'J’ajoute 3 entre deux produits voisins.',work,'0 ; 3 ; 6 ; 9 ; 12 ; 15 ; 18 ; 21 ; 24 ; 27 ; 30.'),'5*3'
 if code==11 and i==9:exprs=['8*7']
 assert exprs,(code,i)
 qs=[calc(x,code) for x in exprs]
 prompt=source['consigne'];work='\n\n'.join(q['etapes'][0] for q in qs);result=' ; '.join(q['resultat'].rstrip('.') for q in qs)+'.'
 if code==5 and i==4:work='Je cherche le complément jusqu’au nombre demandé.\n\n'+chain('70-68','300-275')+'\n\nJe vérifie les deux compléments.\n\n'+work;result='Les nombres manquants sont 2 et 25.'
 if code==7 and i==6:work='Je cherche les petits écarts jusqu’aux nombres voisins.\n\n'+chain('350-346','700-695')+'\n\n'+work;result='Les nombres manquants sont 4 et 5.'
 if code in (10,11) and i in (4 if code==10 else 3,):result='Les facteurs manquants sont '+('6 ; 7 ; 6.' if code==10 else '6 ; 9 ; 8.')
 if code==12 and i==6:result='Les nombres manquants sont 45 et 280.'
 if code==12 and i==1:
  work+='\n\nLes 3 dizaines de 37 deviennent 3 centaines ; les 7 unités deviennent 7 dizaines. Il reste zéro unité isolée.'
  result=f('37*10=370')+' : 3 centaines, 7 dizaines et 0 unité isolée.'
 if code==9 and i==1:work+='\n\n'+mul_work(6,4,9);result=f('4*6=24')+' et '+f('6*4=24')+'.'
 if code==9 and i==3:work+='\n\nDessine cinq petits cercles séparés. Place trois points dans chacun : les cinq groupes ont la même taille.'
 if code==5 and i==9:work='Ajouter 30 au lieu de 29 ajoute déjà une unité de trop. Il faut retirer cette unité. Ajouter encore 1 donnerait '+eq('327+30+1')+', soit deux unités de trop.\n\n'+work
 if code==6 and i==9:work='Le 7 représente sept unités. Il se place sous le 4 des unités de 234 ; le placer sous le 2 reviendrait à ajouter 700.\n\n'+work
 if code==7 and i==9:prompt='Lina annonce un résultat de 405 pour le retrait '+f('402-7')+'. Vérifie puis corrige.';work='Un retrait de 7 doit donner moins que 402. Le résultat annoncé 405 est donc impossible.\n\n'+work
 if code==8 and i==9:prompt='Noé annonce 366 pour '+f('402-168')+'. Vérifie sa réponse par une addition, puis corrige.';work='Je teste d’abord la réponse proposée.\n\n'+chain('366+168')+'\n\n534 ne redonne pas 402 : la proposition est fausse. Je refais les échanges.\n\n'+qs[0]['etapes'][0]+'\n\nJe contrôle la bonne différence.\n\n'+chain('234+168');result=f('402-168=234')+'.'
 if code==12 and i==9:prompt='Noé calcule '+f('17*3')+' en faisant '+f('10*3+7')+'. Quelle partie manque ? Corrige.';work='Les 7 unités doivent aussi être prises trois fois. Le calcul incomplet donne '+eq('10*3+7')+' ; il manque deux autres groupes de 7.\n\n'+work
 if code==11 and i==9:work='Les facteurs peuvent changer de place : le rectangle contient les mêmes objets dans les deux sens.\n\n'+chain('7*8','8*7')+'\n\n'+work
 if code==10 and i==8:work='Les trois paquets doivent avoir la même taille. Je cherche un nombre qui, pris trois fois, donne 30.\n\n'+work;result='Chaque paquet contient 10 cartes.'
 if code==11 and i==8:work='Je cherche combien de groupes de huit forment exactement 56.\n\n'+work;result='Il y a 7 équipes de 8 enfants.'
 units={(5,7):'cahiers',(5,8):'livres',(6,7):'feuilles',(6,8):'élèves',(7,7):'vis',(7,8):'feuilles',(8,7):'places libres',(8,8):'crayons',(9,3):'points',(9,7):'places',(10,7):'feutres',(11,7):'balles',(12,7):'cartes',(12,8):'crayons',(13,7):'cartes'}
 if (code,i) in units:result=eq(exprs[0])+' : '+str(val(exprs[0]))+' '+units[(code,i)]+'.'
 return task(prompt,qs[0]['methode'],work,result),exprs[0]

def complement_add(code,expr,i):
 nums=list(map(int,expr.split('+')));a=nums[0];b=sum(nums[1:]);total=sum(nums)
 if code==6:
  u=sum(n%10 for n in nums);carry=u//10;t=sum(n//10%10 for n in nums)+carry
  q2=task('Reprends le rang des unités de l’addition de départ. Que faut-il écrire et reporter ?','Je compte uniquement les unités ; chaque paquet de dix devient une dizaine.',eq('+'.join(str(n%10) for n in nums))+'.\n\n'+counted(u,'unités')+' donnent '+counted(u%10,'unités')+' et '+counted(carry,'dizaines')+'.',f'J’écris {u%10} unité'+('s' if u%10!=1 else '')+f' et je reporte {carry} dizaine'+('s' if carry!=1 else '')+'.')
  q3=task('Calcule le rang des dizaines en tenant compte de la retenue des unités.','Je réunis les dizaines de tous les nombres et la retenue venue des unités.',eq('+'.join([str(n//10%10) for n in nums]+([str(carry)] if carry else [])))+'.\n\n'+counted(t,'dizaines')+' donnent '+counted(t%10,'dizaines')+' et '+counted(t//10,'centaines')+'.',f'J’écris {t%10} dizaine'+('s' if t%10!=1 else '')+f' et je reporte {t//10} centaine'+('s' if t//10!=1 else '')+'.')
 else:
  near=(b+9)//10*10
  q2=calc(f'{a}+{near}',5,'Calcule '+f(f'{a}+{near}')+' en ajoutant des dizaines ou des centaines entières.')
  if near!=b:q3=calc(f'{a+near}-{near-b}',7,'Après ce détour, retire '+counted(near-b,'unités')+' ajoutée'+('s' if near-b!=1 else '')+' en trop : '+f(f'{a+near}-{near-b}')+'.')
  else:q3=calc(f'{a}+{b+1}',5,'Que donne la même addition avec une unité de plus dans le nombre ajouté ?')
 q4=task('Complète '+f(f'{a}+'+BS+'ldots='+str(total))+'.','Je retire le premier terme au total pour retrouver l’autre partie.',f'La somme est {total} et la partie connue est {a}. La partie manquante correspond à leur différence.\n\n'+sub_mental(total,a)+'\n\nJe vérifie en réunissant les deux parties : '+eq(f'{a}+{b}')+'.',f'Le nombre manquant est {b}.')
 delta=10 if total<=990 else -10;newb=b+delta
 q5=calc(f'{a}+{newb}',code,'Le deuxième nombre '+('augmente' if delta>0 else 'diminue')+' de 10. Calcule '+f(f'{a}+{newb}')+'.')
 return [q2,q3,q4,q5]

def complement_sub(code,expr,i):
 a,b=map(int,expr.split('-'));v=a-b
 q2=calc(f'{v}+{b}',6 if code==8 else 5,'Vérifie le résultat de départ par l’addition '+f(f'{v}+{b}')+'.')
 if code==8:
  exchange=a%10<b%10
  q3=task('Au départ, peut-on retirer les unités sans échange ? Explique avec les chiffres de ce calcul.','Je compare les unités disponibles et les unités à retirer.','Le rang des unités contient '+counted(a%10,'unités')+f' et le retrait demande {b%10}. '+('Ce rang ne suffit pas. Je dois obtenir dix unités de plus par un échange, en passant par les dizaines et si besoin les centaines.' if exchange else 'Ce rang suffit ; je peux commencer sans échanger à ce rang.'),f"{'Un échange est nécessaire' if exchange else 'Aucun échange n’est nécessaire'} au rang des unités.")
 else:
  q3=calc(f'{a}-{b+1}',7,'Retire un objet de plus que dans le calcul de départ : '+f(f'{a}-{b+1}')+'.')
 q4=task('Complète '+f(str(v)+'+'+BS+'ldots='+str(a))+'.','Je cherche la quantité retirée en comparant le départ et ce qui reste.',f'Il faut passer de {v} à {a}. Je calcule l’écart entre ces deux nombres.\n\n'+(sub_columns(a,v) if code==8 else sub_mental(a,v))+'\n\nJe vérifie en ajoutant cet écart : '+eq(f'{v}+{b}')+'.',f'Il manque {b}.')
 q5=calc(f'{a}-{b-1}',code,'Retire un objet de moins que dans le calcul de départ : '+f(f'{a}-{b-1}')+'.')
 return [q2,q3,q4,q5]

def pair_tasks(i,expr):
 if i==4:
  return [task('Peut-on former des paires avec les 124 objets sans objet isolé ? Combien de paires ?','Je reconstitue le total avec deux fois le nombre de paires.',chain('62+62','62*2'),'62 paires et aucun objet isolé.'),task('Avec 305 objets, combien de paires complètes et combien d’objets isolés ?','Je cherche le nombre pair juste avant 305.',chain('152*2','305-304'),'152 paires et 1 objet isolé.'),task('Si l’on ajoute un objet à 678, le nombre obtenu est-il pair ?','Je calcule le nouveau total puis je regarde son chiffre des unités.',chain('678+1')+'\n\n679 finit par 9 : une unité reste sans partenaire.','679 est impair.'),task('Si l’on ajoute un objet à 911, peut-on tout mettre en paires ?','Je passe au nombre suivant : deux nombres consécutifs changent de parité.',chain('911+1','456*2'),'912 est pair ; on peut former 456 paires.')]
 if i==5:
  return [task('Quel nombre pair vient juste après 778 ?','Je passe au nombre pair suivant en ajoutant 2.',chain('778+2'),'780.'),task('Quel nombre pair vient juste avant 768 ?','Je reviens au nombre pair précédent en retirant 2.',chain('768-2'),'766.'),task('Pourquoi 773 n’est-il pas dans la liste ?','Je regarde son chiffre des unités.',chain('386*2','773-772')+'\n\nIl reste une unité après 386 paires.','773 est impair.'),task('Combien de nombres contient la liste de départ ?','Je compte les six nombres, en gardant les deux bornes.', '768 est le premier, 770 le deuxième, 772 le troisième, 774 le quatrième, 776 le cinquième et 778 le sixième.','La liste contient 6 nombres.')]
 if i==8:
  return [task('On ajoute un cube aux 17 cubes. Combien de paires peut-on former maintenant ?','Je complète la paire qui avait un cube isolé.',chain('17+1','9*2'),'9 paires et aucun cube isolé.'),task('On retire un cube aux 17 cubes. Combien de paires peut-on former ?','Je retire le cube isolé avant de compter les paires.',chain('17-1','8*2'),'8 paires et aucun cube isolé.'),task('On ajoute deux cubes aux 17 cubes. Combien de paires complètes et de cubes isolés ?','Deux cubes font une paire supplémentaire ; le cube isolé reste.',chain('17+2','9*2','19-18'),'9 paires et 1 cube isolé.'),task('Quel plus petit ajout permet d’obtenir un nombre pair à partir de 17 ?','Je complète le cube isolé avec un partenaire.',chain('17+1')+'\n\nUn cube suffit pour fermer la dernière paire.','Il faut ajouter 1 cube ; on obtient 18, qui est pair.')]
 return None

def complement_mul(code,expr,i):
 a,b=map(int,expr.split('*'));total=a*b
 if code==12:
  if a==10:a,b=b,a
  if b==10:
   q2=task('Décompose le produit de départ en centaines, dizaines et unités.','Je lis la valeur de chaque chiffre dans le produit par dix.',f'Le produit est {a*10}. Son chiffre des centaines est {a//10}, son chiffre des dizaines est {a%10} et celui des unités est zéro.\n\n'+eq(f'{a//10}*100+{a%10}*10+0')+'.',counted(a//10,'centaines')+', '+counted(a%10,'dizaines')+' et 0 unité isolée.')
   q3=task('Complète '+f(BS+'ldots*10='+str(a*10))+'.','Je compte combien de dizaines contient le résultat.',f'{a*10} unités forment {a} dizaines entières. Le nombre de dizaines est le facteur recherché.\n\n'+chain(f'{a}*10'),f'Le facteur manquant est {a}.')
   other=a+1 if a<99 else a-1
   q4=calc(f'{other}*10',12,f'Calcule {f(str(other)+"*10")} et compare avec le produit de départ.')
   difference=abs(other-a)*10;direction='plus' if other>a else 'moins'
   q4['etapes'][0]+='\n\nJe compare les deux produits : '+eq(f'{max(other,a)*10}-{min(other,a)*10}')+f'. Le nouveau produit est {difference} de {direction} que le produit de départ.'
   q4['resultat']+=f' Cela fait {difference} de {direction} que le produit de départ.'
   q5=task('Pourquoi le chiffre zéro apparaît-il au rang des unités ?','Je relie le produit à un nombre entier de dizaines.',f'{a} dizaines font '+f(str(a*10))+' unités. Toutes les unités sont regroupées par dix ; il reste zéro unité isolée.','Le rang des unités contient zéro, car le résultat compte des dizaines entières.')
   return[q2,q3,q4,q5]
  if 11<=b<=19:a,b=b,a
  low=a-10
  return[calc(f'10*{b}',12,'Calcule la partie correspondant à 10 groupes.'),calc(f'{low}*{b}',10,'Calcule la partie correspondant aux '+str(low)+' groupes restants.'),task('Que manque-t-il si l’on ne calcule que les dix premiers groupes ?','Je retrouve le produit de la partie restante.',f'Il y a {a} groupes en tout : après les dix premiers, il reste {low} groupes. Il faut compter leurs objets avant de réunir les deux parties.\n\n'+chain(f'{low}*{b}',f'{10*b}+{low*b}'),f'Il manque {low*b}, correspondant à {low} groupes de {b}.'),calc(f'{a-1}*{b}',12,'Enlève un groupe de '+str(b)+' au produit de départ : quel est le nouveau total ?')]
 q2=calc(f'{b}*{a}',code,'Change l’ordre des facteurs et calcule '+f(f'{b}*{a}')+'.')
 if a<10:q3=calc(f'{a+1}*{b}',code,f'Ajoute un groupe de {b} : calcule '+f(f'{a+1}*{b}')+'.')
 else:q3=calc(f'{a-1}*{b}',code,f'Retire un groupe de {b} : calcule '+f(f'{a-1}*{b}')+'.')
 q4=task('Complète '+f(BS+'ldots*'+str(b)+'='+str(total))+'.','Je retrouve le nombre de groupes qui reconstitue le total.',mul_work(a,b,code)+f'\n\nPour obtenir {total} objets avec {b} objets dans chaque groupe, il faut {a} groupe'+('s' if a!=1 else '')+'.',f'Le facteur manquant est {a}.')
 prev=max(a-1,0);q5=calc(f'{prev}*{b}',code,'Calcule le produit avec un groupe de moins que dans le produit de départ : '+f(f'{prev}*{b}')+'.')
 if a==10:q5=calc(f'8*{b}',code,'Retire deux groupes au produit de départ : calcule '+f(f'8*{b}')+'.')
 if a==0:q3=calc(f'2*{b}',code,'Compte maintenant deux groupes de '+str(b)+'.');q5=calc(f'3*{b}',code,'Compte maintenant trois groupes de '+str(b)+'.')
 if b==0:q4=task('Peut-on connaître le nombre de groupes si chaque groupe contient zéro objet et que le total vaut zéro ?','Je teste plusieurs nombres de groupes vides.',chain('1*0','2*0','5*0')+'\n\nPlusieurs nombres de groupes donnent le même total nul.','Non : tout nombre de groupes vides donne zéro objet.')
 return [q2,q3,q4,q5]

def complement_half(expr,i):
 a=int(expr.split('//')[0]);h=a//2
 return [calc(f'2*{h}',13,'Vérifie la moitié trouvée en calculant son double.'),calc(f'{a+2}//2',13,f'Trouve la moitié de {a+2}, soit deux objets de plus que le nombre de départ.'),calc(f'{a-2}//2',13,f'Trouve la moitié de {a-2}, soit deux objets de moins que le nombre de départ.'),task(f'Aya propose {h+1} pour la moitié de {a}. Vérifie et corrige.','Je double la proposition : le double doit redonner le nombre de départ.',chain(f'{h+1}+{h+1}',f'{h}+{h}')+f'\n\nLe premier double dépasse {a} de deux ; la proposition est trop grande d’une unité.',f'La moitié correcte de {a} est {h}.')]

def complement_double(x):
 return [calc(f'{2*x}//2',13,'Retrouve la moitié du double calculé au départ.'),calc(f'2*{x+10}',13,f'Le nombre de départ augmente de dix. Calcule le double de {x+10}.'),calc(f'{2*(x+10)}//2',13,f'Vérifie ce nouveau double : quelle est la moitié de {2*(x+10)} ?'),task(f'Noé propose {2*x+1} pour le double de {x}. Vérifie et corrige.','Je réunis deux quantités exactement égales ; chacune doit valoir le nombre de départ.',mul_work(2,x,13)+f'\n\nLa proposition {2*x+1} dépasse le double correct d’une unité.',f'Le double de {x} est {2*x}.')]

def items(code,source):
 out=[]
 for i,s in enumerate(source['exercices'],1):
  if code==10 and i==9:
   qs=[calc(e,10,'Carte '+str(j)+' : retrouve '+f(e)+' et explique comment tu fais.') for j,e in enumerate(['4*7','3*8','5*9','4*9','3*7'],1)]
   intro='Prépare cinq cartes de calcul. Sur le recto, écris le produit indiqué ; sur le verso, écris son résultat et une façon de le retrouver. Ces cinq cartes forment un exemple : tu peux ensuite choisir d’autres produits qui te font hésiter.'
  else:
   first,expr=core(s,code,i);qs=[first];intro='Travaille les calculs suivants et garde les étapes utiles pour expliquer tes réponses.'
   if code in (5,6):qs+=complement_add(code,expr,i)
   elif code in (7,8):
    if code==7 and i==6:expr='700-5'
    qs+=complement_sub(code,expr,i)
   elif code==9 and pair_tasks(i,expr):qs+=pair_tasks(i,expr)
   elif code==13 and '//' in expr:qs+=complement_half(expr,i)
   elif code==13 and i in (2,4,7):qs+=complement_double(135 if i==7 else int(expr.split('*')[1]))
   else:qs+=complement_mul(code,expr,i)
  # Détailler aussi les très courts calculs sur les paires.
  if code==9 and i in (4,5,8):
   for question in qs[1:]:
    if len(question['etapes'][0])<40:question['etapes'][0]=question['methode']+'\n\n'+question['etapes'][0]+'\n\n'+question['resultat']
  out.append(dict(titre=TITLES[code][i-1],enonce=intro,questions=qs,source=i))
 return out

COURSES={
5:r'''::: objectifs
Ajouter des dizaines ou des centaines ; décomposer un nombre ; choisir un détour court pour ajouter 9, 19 ou 29 ; trouver un complément.
:::

## I. Ajouter des dizaines ou des centaines
::: definition Additionner
Additionner, c’est réunir des quantités. Dans $234+60$, on ajoute six dizaines. Les quatre unités restent quatre unités.
:::
::: exemple
$234+60=294$.

$407+200=607$.

Un échange peut changer la centaine : $650+70=720$, car 65 dizaines et 7 dizaines font 72 dizaines.
:::

## II. Décomposer le nombre ajouté
::: methode Des morceaux faciles à ajouter
Sépare le nombre ajouté en centaines, dizaines et unités. Ajoute ces morceaux l’un après l’autre, en gardant une trace.
:::
::: exemple
Pour $246+132$, je sépare 132 en 100, 30 et 2.

$246+100=346$.

$346+30=376$.

$376+2=378$.

Donc $246+132=378$.
:::

## III. Passer par une dizaine voisine
::: propriete Ajouter presque une dizaine
19 est un de moins que 20 ; 29 est un de moins que 30. Si j’ajoute 20 au lieu de 19, je dois ensuite enlever l’unité ajoutée en trop.
:::
[IMAGE_1]
::: exemple
$246+20=266$.

$266-1=265$.

Donc $246+19=265$.
:::
::: attention Le sens de la correction
Après avoir ajouté trop, **retire** le surplus. Pour ajouter 29, ajouter 30 puis encore 1 ferait deux unités de trop.
:::

## IV. Trouver un complément
::: methode Atteindre un nombre repère
Pour compléter $275+\ldots=300$, atteins d’abord 280, puis 300. Il faut 5 puis 20.
:::
::: exemple
$275+5=280$.

$280+20=300$.

$5+20=25$ : le complément est 25. Je vérifie : $275+25=300$.
:::
::: retenir
Ajoute des morceaux faciles. Pour 9, 19 ou 29, ajoute 10, 20 ou 30 puis retire 1. Choisis la méthode qui demande le moins d’étapes et vérifie que la somme est plus grande que le départ quand tu ajoutes une quantité positive.
:::''',
6:r'''::: objectifs
Poser une addition de deux ou trois nombres, aligner les rangs et comprendre chaque retenue, jusqu’à un résultat de 1 000.
:::

## I. Placer chaque chiffre à son rang
::: definition Une colonne pour chaque rang
Les unités se placent sous les unités, les dizaines sous les dizaines et les centaines sous les centaines. Un nombre court se place à partir de la droite.
:::
::: exemple
Pour $405+78$, le 8 se place sous le 5 des unités et le 7 sous le 0 des dizaines. Le nombre 78 n’a pas de centaine.
:::

## II. Commencer par les unités
::: methode Calculer de droite à gauche
Additionne les unités. S’il y en a au moins dix, échange dix unités contre une dizaine : écris les unités restantes et reporte la dizaine. Continue aux dizaines, puis aux centaines.
:::
[IMAGE_1]
::: exemple Les échanges de 386 + 257
Unités : $6+7=13$. J’écris 3 unités et je reporte 1 dizaine.

Dizaines : $8+5+1=14$. J’écris 4 dizaines et je reporte 1 centaine.

Centaines : $3+2+1=6$. J’écris 6 centaines.

$$386+257=643$$
:::
::: propriete La retenue a une valeur
La retenue qui arrive aux dizaines vaut une dizaine ; celle qui arrive aux centaines vaut une centaine. Elle vient d’un échange et s’ajoute une seule fois.
:::

## III. Additionner trois nombres
::: methode Réunir toute une colonne
Aligne les trois nombres. Dans chaque colonne, compte les chiffres des trois nombres **et** la retenue qui arrive.
:::
::: exemple
Pour $186+47+238$ : unités, $6+7+8=21$, soit 1 unité et 2 dizaines ; dizaines, $8+4+3+2=17$, soit 7 dizaines et 1 centaine ; centaines, $1+0+2+1=4$.

$$186+47+238=471$$
:::

## IV. Écrire zéro et atteindre mille
::: exemple
Dans $579+321$, les unités donnent $9+1=10$ et les dizaines donnent $7+2+1=10$. Il reste zéro unité et zéro dizaine ; les centaines donnent $5+3+1=9$.

$$579+321=900$$

Dans $642+358$, les échanges conduisent à dix centaines : $642+358=1000$.
:::
::: attention
N’oublie pas les zéros qui gardent les rangs. Dans 900, le 9 représente neuf centaines. Un chiffre d’unités ne se place jamais sous les centaines.
:::
::: retenir
Aligne les rangs ; commence à droite ; écris chaque retenue au rang suivant. Pour contrôler, retrouve l’un des nombres en retirant l’autre à la somme.
:::''',
7:r'''::: objectifs
Retirer mentalement des dizaines, des centaines ou un petit nombre ; franchir une dizaine ; retirer 9 par un détour.
:::

## I. Comprendre le retrait
::: definition Soustraire
Dans $541-20$, on retire 20 à 541. Quand on retire une quantité positive, le résultat est plus petit que le nombre de départ.
:::
::: exemple
$541-20=521$ : je retire deux dizaines.

$765-200=565$ : je retire deux centaines.
:::

## II. Passer par une dizaine
::: methode Couper le retrait en deux
Pour retirer 7 de 523, je retire d’abord les 3 unités qui me conduisent à 520. Il reste encore 4 à retirer, car $3+4=7$.
:::
[IMAGE_1]
::: exemple
$523-3=520$.

$520-4=516$.

Donc $523-7=516$.
:::
::: exemple Partir d’un nombre rond
Pour $600-4$, je garde 590 et je prends 4 dans les dix dernières unités : $10-4=6$, puis $590+6=596$.
:::

## III. Retirer neuf
::: propriete Un détour à corriger
9 est un de moins que 10. Retirer 10 enlève donc une unité de trop : il faut la rendre en ajoutant 1.
:::
::: exemple
$375-10=365$.

$365+1=366$.

Donc $375-9=366$.
:::
::: attention
Après avoir retiré trop, ajoute le surplus retiré. Retirer encore 1 aggraverait l’erreur.
:::

## IV. Retrouver la quantité enlevée
::: methode Relier soustraction et addition
Dans $700-\ldots=695$, cherche combien il faut ajouter à 695 pour retrouver 700.
:::
::: exemple
$695+5=700$, donc il faut retirer 5 à 700 pour obtenir 695.
:::
::: retenir
Retire des morceaux faciles. Pour franchir une dizaine, sépare le petit retrait. Pour retirer 9, retire 10 puis ajoute 1. Vérifie le résultat en ajoutant la quantité retirée.
:::''',
8:r'''::: objectifs
Poser une soustraction par échanges, traverser un rang qui contient zéro et vérifier une différence par une addition.
:::

## I. Aligner les rangs
::: definition La différence
La soustraction $402-168$ cherche ce qui reste après avoir retiré 168 à 402. 402 est le départ, 168 la quantité retirée ; le résultat est la différence.
:::
::: methode Préparer le calcul
Écris les unités sous les unités, les dizaines sous les dizaines, les centaines sous les centaines. Commence par la droite. Le nombre du bas se retire à celui du haut.
:::

## II. Échanger avant de retirer
::: propriete Garder la même quantité
Une centaine s’échange contre dix dizaines ; une dizaine s’échange contre dix unités. Ces échanges changent l’écriture, mais gardent la quantité de départ.
:::
[IMAGE_1]
::: exemple 402 − 168
Les 2 unités ne suffisent pas pour retirer 8 ; il n’y a aucune dizaine isolée. J’échange 1 des 4 centaines contre 10 dizaines : j’ai 3 centaines, 10 dizaines et 2 unités.

J’échange ensuite 1 de ces dizaines contre 10 unités : j’ai 3 centaines, 9 dizaines et 12 unités.

$300+90+12=402$.

Je retire les unités : $12-8=4$ ; les dizaines : $9-6=3$ ; les centaines : $3-1=2$.

$$402-168=234$$
:::

## III. Traverser plusieurs zéros
::: exemple Retirer à mille
Pour $1000-375$, j’échange le millier contre 10 centaines. J’échange ensuite une centaine contre 10 dizaines, puis une dizaine contre 10 unités. J’obtiens 9 centaines, 9 dizaines et 10 unités.

$900+90+10=1000$.

Unités : $10-5=5$ ; dizaines : $9-7=2$ ; centaines : $9-3=6$.

$$1000-375=625$$
:::

## IV. Vérifier avec une addition
::: methode Reconstituer le départ
Ajoute la différence et la quantité retirée. Tu dois retrouver exactement le nombre de départ.
:::
::: exemple
Pour vérifier $402-168=234$, je calcule $234+168=402$.
:::
::: attention
Ne soustrais pas systématiquement le plus petit chiffre au plus grand : l’ordre des deux nombres doit rester le même. Si un rang ne suffit pas, fais un échange.
:::
::: retenir
Aligne, commence à droite, échange si besoin. Note les quantités obtenues après chaque échange ; vérifie par l’addition qui reconstitue le départ.
:::''',
9:r'''::: objectifs
Relier une multiplication à des groupes égaux, lire une collection dans deux sens et reconnaître les nombres pairs ou impairs.
:::

## I. Compter des groupes égaux
::: definition Une addition répétée
$3\times4$ se lit « trois fois quatre » : trois groupes de quatre objets.

$$4+4+4=12$$

$$3\times4=12$$
:::
[IMAGE_1]
::: methode Dessiner pour compter
Dessine un groupe pour chaque quantité répétée. Chaque groupe doit contenir le même nombre d’objets. Le produit est le nombre total d’objets.
:::

## II. Changer l’organisation
::: propriete Changer l’ordre des facteurs
Dans un rectangle de points, les lignes peuvent devenir les colonnes. Aucun point n’est ajouté ni retiré : l’ordre des facteurs ne change pas le produit.
:::
::: exemple
$3\times4=12$ et $4\times3=12$.

Trois groupes de quatre et quatre groupes de trois ont le même total.
:::
::: exemple Zéro et un
$1\times8=8$ : un groupe de huit.

$0\times6=0$ : aucun groupe de six.

$5\times0=0$ : cinq groupes vides.
:::

## III. Former des paires
::: definition Pair ou impair
Un nombre est **pair** si tous les objets peuvent être rangés par deux sans reste. Un nombre est **impair** si un objet reste seul.
:::
::: exemple
$8\times2=16$ : 16 objets forment huit paires.

$8\times2+1=17$ : avec 17 objets, il y a huit paires et un objet isolé. 17 est impair.
:::

## IV. Regarder le chiffre des unités
::: propriete
Les nombres qui se terminent par 0, 2, 4, 6 ou 8 sont pairs. Ceux qui se terminent par 1, 3, 5, 7 ou 9 sont impairs. Une dizaine complète forme déjà cinq paires : seules les unités isolées peuvent laisser un reste.
:::
::: exemple
124 et 678 sont pairs ; 305 et 911 sont impairs. Pour passer d’un nombre pair au suivant, ajoute 2.
:::
::: attention
Des groupes de tailles différentes ne forment pas une addition répétée du même nombre. Compte toujours le nombre de groupes et le nombre d’objets dans chaque groupe.
:::
::: retenir
Une multiplication compte des groupes égaux. Changer l’ordre des facteurs garde le total. Pour la parité, regarde le chiffre des unités ou forme des paires.
:::''',
10:r'''::: objectifs
Construire les tables de 2, 3, 4, 5 et 10 ; retrouver un produit voisin ; trouver un facteur manquant et expliquer une méthode de mémorisation.
:::

## I. Construire une table
::: definition Ajouter un groupe à la fois
Dans la table de 3, chaque groupe contient 3 objets. Pour passer d’un produit au suivant, j’ajoute 3.
:::
[IMAGE_1]
::: exemple
$5\times3=15$.

$15+3=18$.

Donc $6\times3=18$.
:::

## II. Quelques points d’appui
::: methode Retrouver les premières tables
- La table de 2 donne les doubles.
- Dans la table de 3, ajoute 3 à chaque nouveau groupe.
- Pour multiplier par 4, double deux fois.
- Dans la table de 5, les résultats se terminent par 0 ou 5.
- La table de 10 compte les dizaines.
:::
::: exemple Deux doubles
$9+9=18$.

$18+18=36$.

Donc $4\times9=36$.
:::

## III. La table de trois
| Nombre de groupes | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Total | 0 | 3 | 6 | 9 | 12 | 15 | 18 | 21 | 24 | 27 | 30 |

::: conseil Apprendre en expliquant
Écris un produit sur une carte et son résultat au dos. Avant de retourner la carte, dis comment tu peux retrouver le résultat avec un dessin, un double ou un produit voisin. Reprends plus souvent les cartes qui te font hésiter.
:::

## IV. Trouver un facteur ou partager
::: methode Reconstituer le total
Dans $4\times\ldots=24$, cherche le nombre dont quatre groupes donnent 24. Pour partager 30 cartes en trois paquets égaux, cherche le nombre qui donne 30 quand il est pris trois fois.
:::
::: exemple
$4\times6=24$ : le facteur manquant est 6.

$3\times10=30$ : chacun des trois paquets contient 10 cartes.
:::
::: attention
Ajouter un groupe de 3 augmente le total de **3**, pas de 1. Les facteurs décrivent les groupes ; le produit compte tous les objets.
:::
::: retenir
Reconstruis un résultat avant de le mémoriser : groupes égaux, produit voisin, doubles, cinq ou dix groupes. Un facteur manquant se retrouve en reconstituant le total.
:::''',
11:r'''::: objectifs
Construire et mémoriser les tables de 6, 7, 8 et 9 en utilisant des produits déjà connus ; retrouver des facteurs manquants.
:::

## I. Utiliser cinq groupes et un complément
::: methode Décomposer les groupes
Pour sept groupes de sept, compte cinq groupes de sept puis encore deux groupes de sept. Les deux morceaux réunis comptent les sept groupes.
:::
[IMAGE_1]
::: exemple
$5\times7=35$.

$2\times7=14$.

$35+14=49$.

Donc $7\times7=49$.
:::

## II. Ajouter ou retirer un groupe
::: propriete Produits voisins
Un groupe supplémentaire de 7 ajoute 7 au total. Un groupe de 7 en moins retire 7 au total.
:::
::: exemple
À partir de $7\times7=49$, je calcule $49+7=56$ : $8\times7=56$.

Pour neuf groupes de sept, je pars de dix groupes : $10\times7=70$, puis $70-7=63$. Donc $9\times7=63$.
:::

## III. Doubler un produit connu
::: methode De quatre à huit groupes
Huit groupes, c’est deux fois quatre groupes. Calcule quatre groupes puis double ce total.
:::
::: exemple
$4\times6=24$.

$24+24=48$.

Donc $8\times6=48$.
:::
::: propriete Changer l’ordre
$7\times8=56$ et $8\times7=56$. Le même rectangle se compte dans les deux sens.
:::

## IV. Se donner des repères et vérifier
| Produit | Résultat | Appui possible |
|---|---|---|
| $6\times6$ | 36 | $5\times6=30$, puis $30+6=36$ |
| $7\times7$ | 49 | $35+14=49$ |
| $8\times8$ | 64 | $4\times8=32$, puis $32+32=64$ |
| $9\times9$ | 81 | $10\times9=90$, puis $90-9=81$ |

::: exemple Retrouver un facteur
Dans $8\times\ldots=48$, le facteur manquant est 6, car $8\times6=48$. Avec 56 enfants en équipes de huit, il y a 7 équipes, car $7\times8=56$.
:::
::: attention
Ajouter un groupe signifie ajouter autant d’objets qu’il y en a dans ce groupe. Pour passer de sept groupes de huit à huit groupes de huit, ajoute 8.
:::
::: retenir
Utilise cinq groupes et un complément, dix groupes moins un, le double de quatre groupes ou l’ordre échangé des facteurs. Revois les produits à plusieurs moments pour les mémoriser.
:::''',
12:r'''::: objectifs
Multiplier par 10 en comprenant les rangs ; calculer avec un facteur de 11 à 19 en séparant dix et les unités restantes.
:::

## I. Compter des dizaines
::: propriete Multiplier par dix
Multiplier un nombre entier par 10 donne à chacun de ses chiffres une valeur dix fois plus grande. Les unités deviennent des dizaines et les dizaines deviennent des centaines.
:::
[IMAGE_1]
::: exemple
$37\times10=370$ : les 3 dizaines deviennent 3 centaines et les 7 unités deviennent 7 dizaines. Il reste zéro unité isolée.

$60\times10=600$ : les 6 dizaines deviennent 6 centaines.
:::
::: attention
Le zéro final garde la place des unités. Explique le changement de valeur des chiffres plutôt que de réciter seulement « j’ajoute un zéro ».
:::

## II. Séparer dix et les unités restantes
::: methode Multiplier chaque morceau
Pour calculer $14\times6$, sépare 14 en 10 et 4. Calcule dix groupes de six, puis quatre groupes de six. Réunis ces deux totaux.
:::
[IMAGE_2]
::: exemple
$10\times6=60$.

$4\times6=24$.

$60+24=84$.

Donc $14\times6=84$.
:::

## III. Décomposer l’autre facteur
::: propriete Un même total dans les deux sens
L’ordre des facteurs ne change pas le produit. Dans $7\times15$, on peut séparer 15 en 10 et 5, puis multiplier ces deux parties par 7.
:::
::: exemple
$7\times10=70$.

$7\times5=35$.

$70+35=105$.

Donc $7\times15=105$.
:::

## IV. Contrôler la décomposition
::: attention Ne rien oublier
Dans $17\times3$, la partie 7 doit aussi être multipliée par 3 : $10\times3=30$, $7\times3=21$, puis $30+21=51$. Ajouter seulement 7 ne compte qu’un groupe de 7 au lieu de trois.
:::
::: methode Retrouver un nombre de dizaines
Pour compléter $\ldots\times10=450$, compte les dizaines de 450. Il y en a 45, donc $45\times10=450$.
:::
::: retenir
Multiplier par 10 transforme les valeurs de position. Pour un facteur de 11 à 19, sépare 10 et le reste ; multiplie chaque morceau, puis additionne les deux produits.
:::''',
13:r'''::: objectifs
Calculer des doubles et des moitiés ; décomposer en morceaux faciles à partager ; utiliser les repères 25, 50, 75 et 100.
:::

## I. Le double
::: definition Deux quantités égales
Le double d’un nombre réunit deux fois cette quantité. Le double de 135 se calcule par $135+135$ ou $2\times135$.
:::
::: exemple
$100+100=200$ ; $30+30=60$ ; $5+5=10$.

$200+60+10=270$.

Le double de 135 est 270.
:::

## II. La moitié
::: definition Deux parts égales
Prendre la moitié d’une quantité, c’est la partager en deux parts égales. Les deux moitiés réunies redonnent la quantité entière.
:::
::: methode Choisir des morceaux faciles
Sépare le nombre en morceaux dont tu connais les moitiés. Prends la moitié de chaque morceau puis réunis les résultats.
:::
[IMAGE_1]
::: exemple
$470=400+70$.

La moitié de 400 est 200 ; celle de 70 est 35.

$200+35=235$.

La moitié de 470 est 235. Je vérifie : $235+235=470$.
:::

## III. Choisir une autre décomposition
::: exemple
Pour la moitié de 738, je choisis $738=600+120+18$.

La moitié de 600 est 300 ; celle de 120 est 60 ; celle de 18 est 9.

$300+60+9=369$.

Je vérifie : $369+369=738$.
:::
::: attention
Un chiffre impair ne se partage pas toujours seul. Pour 70, pense à $70=60+10$ : les moitiés 30 et 5 donnent $30+5=35$.
:::

## IV. Les repères de vingt-cinq
| Groupes de 25 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Total | 25 | 50 | 75 | 100 |

::: exemple
$2\times25=50$ ; $3\times25=75$ ; $4\times25=100$.

Deux fois 50 font 100 : la moitié de 100 est 50. Deux fois 25 font 50 : la moitié de 50 est 25.
:::
::: retenir
Double : réunis deux quantités égales. Moitié : forme deux parts égales. Utilise une décomposition adaptée et contrôle toujours une moitié en la doublant.
:::'''}

SUMMARIES={
5:('Des additions mentales rapides','Ajoute les centaines, les dizaines puis les unités du nombre ajouté. Pour 9, 19 ou 29, ajoute 10, 20 ou 30 puis retire 1.','246+20=266','266-1=265','246+19=265','Après avoir ajouté trop, retire le surplus ; ne l’ajoute pas une deuxième fois.'),
6:('Additionner en colonnes','Aligne les rangs. Commence par les unités. Échange dix unités d’un rang contre une du rang suivant et ajoute chaque retenue une seule fois.','6+7=13','8+5+1=14','3+2+1=6','Une retenue venue des unités vaut une dizaine. Garde les zéros des rangs vides.'),
7:('Soustraire de tête','Retire les centaines ou les dizaines séparément. Pour franchir une dizaine, coupe le petit retrait. Pour retirer 9, retire 10 puis rends 1.','523-3=520','520-4=516','523-7=516','Après avoir retiré trop, rends le surplus en l’ajoutant.'),
8:('Soustraire par échanges','Aligne les rangs et commence à droite. Si un rang ne suffit pas, échange une unité du rang supérieur. Passe par les rangs nuls si besoin.','300+90+12=402','402-168=234','234+168=402','Ne change pas l’ordre des chiffres pour éviter un échange. Vérifie par l’addition qui reconstitue le départ.'),
9:('Groupes égaux et paires','Une multiplication compte des groupes de même taille. Changer l’ordre des facteurs garde le total. Un nombre pair se range par deux sans reste.','3*4=12','4*3=12','8*2+1=17','Pairs : chiffres des unités 0, 2, 4, 6 ou 8. Impairs : 1, 3, 5, 7 ou 9.'),
10:('Retrouver les premières tables','Table de 2 : doubles. Table de 3 : ajoute 3. Table de 4 : double deux fois. Table de 5 : compte de 5 en 5. Table de 10 : compte les dizaines.','9+9=18','18+18=36','4*9=36','Un groupe supplémentaire de 3 ajoute 3 objets, pas un seul.'),
11:('Construire les autres tables','Pars de cinq groupes et ajoute un complément. Pour neuf groupes, prends dix groupes moins un. Pour huit groupes, double quatre groupes.','5*7=35','2*7=14','35+14=49','Changer l’ordre des facteurs garde le produit : si tu sais sept fois huit, tu sais huit fois sept.'),
12:('Multiplier par dix et décomposer','Par dix, les unités deviennent des dizaines et les dizaines deviennent des centaines. Pour un facteur de 11 à 19, sépare dix et le reste ; multiplie les deux parties.','10*6=60','4*6=24','60+24=84','Dans quatorze fois six, il faut multiplier aussi les quatre unités par six.'),
13:('Doubles et moitiés','Le double réunit deux quantités égales. Pour une moitié, partage des morceaux faciles puis réunis leurs moitiés. Vérifie une moitié en la doublant.','470=400+70','200+35=235','235+235=470','Une moitié est une part ; les deux moitiés réunies redonnent le nombre de départ.')}

def summary(code):
 title,method,e1,e2,e3,warning=SUMMARIES[code]
 out=f'Titre: Résumé : {title}\n\n{MARK}\n'+boxes('objectifs','Retrouver la méthode essentielle et les points à vérifier.')+'\n\n## I. La méthode\n'+boxes('methode',method)+'\n\n[IMAGE_1]\n\n## II. Un exemple\n'+boxes('exemple','\n\n'.join(f(e)+'.' for e in (e1,e2,e3)))+'\n\n## III. Le contrôle\n'+boxes('attention',warning)
 if code==5:out+='\n\n'+boxes('retenir','Un complément se retrouve en atteignant une dizaine ou une centaine voisine. Vérifie ensuite l’addition complète.')
 if code==6:out+='\n\n'+boxes('retenir',f('386+257=643')+'. Une addition peut faire apparaître un nouveau rang : '+f('642+358=1000')+'.')
 if code==10:out+='\n\n'+boxes('retenir','Pour un facteur manquant, retrouve le nombre de groupes qui reconstitue le total. Écris les calculs difficiles sur des cartes et explique comment les retrouver.')
 if code==13:out+='\n\n'+boxes('retenir','Les repères de 25 : 25, 50, 75, 100 ; deux fois 25 font 50, quatre fois 25 font 100.')
 return out+'\n'

def node(x,y,text,color='otInk',small=False):return BS+f'node[text={color}'+(',font='+BS+'small' if small else '')+f'] at ({x},{y}) '+'{'+text+'};'

def columns(nums,sub=False,answer=True):
 result=nums[0]-nums[1] if sub else sum(nums)
 width=max(3,len(str(max(nums))),len(str(result)));ls=[BS+'begin{tikzpicture}[x=1.6cm,y=0.72cm]'];names=NAMES[:width][::-1]
 for x,name in enumerate(names):ls.append(node(x,1.2,name,'otNavy',True))
 for row,v in enumerate(nums):
  for k,c in enumerate(str(v)[::-1]):ls.append(node(width-1-k,-row,'$'+c+'$'))
  if row:ls.append(node(-.65,-row,'$'+('-' if sub else '+')+'$','otNavy'))
 y=-(len(nums)-1)-.58;ls.append(BS+f'draw[otNavy,line width=0.8pt] (-0.35,{y}) -- ({width-.65},{y});')
 if answer:
  result=nums[0]-nums[1] if sub else sum(nums)
  for k,c in enumerate(str(result)[::-1]):ls.append(node(width-1-k,y-.65,'$'+c+'$','otGreenDark'))
 ls.append(BS+'end{tikzpicture}');return '\n'.join(ls)

def jumps(vals,labels):
 ls=[BS+'begin{tikzpicture}[x=2.25cm,y=1cm]'];positions={v:i for i,v in enumerate(sorted(set(vals)))};xs=[positions[v] for v in vals]
 ls.append(BS+f'draw[otRule,line width=0.7pt] (-0.25,0) -- ({len(vals)-.75},0);')
 for x,v in zip(xs,vals):ls.append(BS+f'fill[otNavy] ({x},0) circle (2pt);');ls.append(node(x,-.4,'$'+str(v)+'$','otNavy'))
 for k,lab in enumerate(labels):
  start,end=xs[k],xs[k+1];bend='left' if end>start else 'right';height=.73 if abs(end-start)==1 else 1.3
  if k and vals[k-1]<vals[k] and end<start:bend='left';height=-.95
  ls.append(BS+f'draw[otGreenDark,line width=1pt,-{{Stealth[length=2mm]}}] ({start},0.15) to[bend {bend}=35] ({end},0.15);');ls.append(node((start+end)/2,height,'$'+lab+'$','otGreenDark'))
 ls.append(BS+'end{tikzpicture}');return '\n'.join(ls)

def array(rows,cols,split=None):
 ls=[BS+'begin{tikzpicture}[x=0.44cm,y=0.44cm]']
 for r in range(rows):
  for c in range(cols):ls.append(BS+f'fill['+('otGreenDark' if split and r>=split else 'otNavy')+f'] ({c},{-r}) circle (2.4pt);')
 ls.append(node((cols-1)/2,1.15,f'{cols} points par ligne','otNavy',True))
 ls.append(node((cols-1)/2,-rows-.45,f'{rows} lignes','otGreenDark',True));ls.append(BS+'end{tikzpicture}');return '\n'.join(ls)

def half_diagram(a,parts):
 ls=[BS+'begin{tikzpicture}[x=1.6cm,y=1cm]'];mid=(len(parts)-1)/2
 ls.append(node(mid,2.1,'$'+str(a)+'$','otNavy'))
 for k,p in enumerate(parts):
  ls.append(BS+f'draw[otRule,line width=0.8pt] ({mid},1.78) -- ({k},1.22);');ls.append(node(k,.95,'$'+str(p)+'$','otNavy'));ls.append(BS+f'draw[otGreenDark,-{{Stealth[length=2mm]}}] ({k},0.63) -- ({k},0.12);');ls.append(node(k,-.18,'$'+str(p//2)+'$','otGreenDark'))
 ls.append(node(mid,-.9,'Chaque morceau est partagé en deux.','otNavy',True));ls.append(BS+'end{tikzpicture}');return '\n'.join(ls)

def value10(x):
 ls=[BS+'begin{tikzpicture}[x=1.6cm,y=0.82cm]'];names=['centaines','dizaines','unités']
 for k,nam in enumerate(names):ls.append(node(k,1.1,nam,'otNavy',True))
 for row,v,color in [(0,x,'otInk'),(-1.5,x*10,'otGreenDark')]:
  for k,c in enumerate(str(v)[::-1]):ls.append(node(2-k,row,'$'+c+'$',color))
 for k,c in enumerate(str(x)[::-1]):ls.append(BS+f'draw[otGreenDark,-{{Stealth[length=2mm]}}] ({2-k-.12},-.35) -- ({1-k+.12},-1.13);')
 ls.append(node(3.25,-.75,r'$\times10$','otGreenDark'));ls.append(BS+'end{tikzpicture}');return '\n'.join(ls)

def split_product(a,b):
 low=a-10;ls=[BS+'begin{tikzpicture}[x=1cm,y=1cm]']
 ls.append(BS+'draw[otNavy,line width=0.9pt] (0,0) rectangle (5,1.6);');ls.append(BS+'draw[otNavy,line width=0.8pt] (3.1,0) -- (3.1,1.6);')
 ls+=[node(1.55,2,'10 groupes','otNavy',True),node(4.05,2,f'{low} groupes','otNavy',True),node(1.55,.8,'$10'+BS+f'times {b}={10*b}$','otGreenDark'),node(4.05,.8,'$'+str(low)+BS+f'times {b}={low*b}$','otGreenDark'),node(2.5,-.55,f'{a} groupes de {b} : {a*b} objets','otNavy',True),BS+'end{tikzpicture}']
 return '\n'.join(ls)

def build_figures(code,items,source):
 fig={};course={5:jumps([246,266,265],['+20','-1']),6:columns([386,257]),7:jumps([523,520,516],['-3','-4']),8:columns([402,168],True),9:array(3,4),10:array(6,3),11:array(7,7,5),12:value10(37),13:half_diagram(470,[400,70])}[code]
 fig['cours_methode']=course
 correspond={'cours':{'nouveau':{'1':{'fichier':'cours_methode.png','alt':{5:'Deux étapes pour ajouter dix-neuf à 246 : ajouter vingt puis retirer un.',6:'Addition en colonnes de 386 et 257, avec le résultat 643 aligné par rang.',7:'Deux retraits successifs pour passer de 523 à 520 puis à 516.',8:'Soustraction en colonnes de 402 et 168 donnant 234, chiffres alignés par rang.',9:'Collection rectangulaire de trois lignes de quatre points.',10:'Six lignes de trois points pour lire le produit six fois trois.',11:'Sept lignes de sept points, séparées en cinq lignes puis deux lignes.',12:'Les chiffres de 37 changent de rang lorsque ce nombre est multiplié par dix.',13:'470 séparé en 400 et 70, puis moitiés 200 et 35 de chaque morceau.'}[code]}}},'fiches':{'nouvelle':{'1':{'fichier':'cours_methode.png','alt':'Schéma de la méthode essentielle : '+source['titre'].lower()+'.'}}},'exercices':{}}
 if code==12:fig['cours_decomposition']=split_product(14,6);correspond['cours']['nouveau']['2']={'fichier':'cours_decomposition.png','alt':'Quatorze groupes de six séparés en dix groupes et quatre groupes, soit soixante et vingt-quatre.'}
 for i,item in enumerate(items,1):
  src=source['exercices'][i-1];shape=None
  if code==6:
   expr=source_exprs(src)[0];shape=columns(list(map(int,expr.split('+'))));alt='Correction de l’addition en colonnes : '+expr.replace('+',' plus ')+', chiffres de même rang alignés.'
  elif code==8:
   expr=source_exprs(src)[0];shape=columns(list(map(int,expr.split('-'))),True);alt='Correction de la soustraction en colonnes : '+expr.replace('-',' moins ')+', chiffres de même rang alignés.'
  elif src.get('figure'):
   typ,args=src['figure']
   if typ=='compensation':a,near,correction=args;shape=jumps([a,a+near,a+near+correction],[f'+{near}',str(correction)])
   elif typ=='backjumps':shape=jumps(args,[str(args[1]-args[0]),str(args[2]-args[1])])
   elif typ=='array':shape=array(*args)
   elif typ=='halftree':shape=half_diagram(args[0],args[1:])
   elif typ=='productsplit':shape=split_product(*args)
   elif typ=='times10':shape=value10(args)
   alt='Représentation du calcul demandé : '+src['consigne']
  if shape:
   name=f'ex{i}_support';fig[name]=shape
   if code in(6,8):item['questions'][0]['etapes'].insert(0,'[IMAGE_1]')
   else:item['enonce']+='\n\n[IMAGE_1]'
   correspond['exercices'][f'nouveau-{i}']={'1':{'fichier':name+'.png','alt':alt}}
 return fig,correspond

VERIFY=r'''"""Vérification autonome : relit et recalcule les égalités des vrais fichiers finaux."""
from pathlib import Path
import ast,json,re
P=Path(__file__).resolve().parent
def compute(s):
 tree=ast.parse(s,mode='eval')
 def rec(n):
  if isinstance(n,ast.Expression):return rec(n.body)
  if isinstance(n,ast.Constant) and isinstance(n.value,int):return n.value
  if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Add,ast.Sub,ast.Mult)):
   a,b=rec(n.left),rec(n.right)
   return a+b if isinstance(n.op,ast.Add) else a-b if isinstance(n.op,ast.Sub) else a*b
  raise ValueError(s)
 return rec(tree)
total=0
for name in ('cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt'):
 text=(P/name).read_text(encoding='utf-8');assert '\x0c' not in text and '\x08' not in text
 for m in re.finditer(r'\${1,2}([^$]+)\${1,2}',text):
  formula=m[1].strip().replace('\\times','*').replace(' ','')
  if '=' not in formula or '\\' in formula:continue
  parts=formula.split('=')
  if all(re.fullmatch(r'[0-9+*()\-]+',p) for p in parts):
   values=[compute(p) for p in parts];assert len(set(values))==1,(name,m[1],values);total+=1
  assert not any(int(v)>1000 for v in re.findall(r'\d+',formula)),(name,formula)
 # Les phrases de partage et de parité sont vérifiées dans les textes produits.
 for a,b in re.findall(r'[Ll]a moitié de (\d+) est (\d+)',text):assert int(a)==2*int(b),(name,a,b)
 for a,b in re.findall(r'[Ll]e double de (\d+) est (\d+)',text):assert 2*int(a)==int(b),(name,a,b)
text=(P/'exercices.txt').read_text(encoding='utf-8')
blocks=re.split(r'^===\n',text,flags=re.M)[1:];assert len(blocks)==9,len(blocks)
for i,block in enumerate(blocks,1):
 assert f'Id: nouveau-{i}\n' in block
 en,rest=block.split('Énoncé:\n',1)[1].split('Étapes:\n',1);steps,sol=rest.split('Solution:\n',1)
 qs=re.findall(r'^\d+\. ',en,re.M);assert len(qs)>=5,(i,len(qs))
 assert len(re.findall(r'^## Question \d+ :',steps,re.M))==len(qs)
 assert steps.count('::: methode\n')==steps.count('::: resultat\n')==len(qs)
 results=re.findall(r'::: resultat\n(.*?)\n:::',steps,re.S)
 answers=re.findall(r'^\d+\. (.*)$',sol,re.M)
 assert results==answers,(i,'Résultats et solutions différents')
 for p in re.findall(r'## Question .*?(?=\n## Question |\Z)',steps,re.S):
  assert len(re.search(r'::: etape .*?\n(.*?)\n:::',p,re.S)[1])>=40
  # Résoudre à nouveau les calculs à trou à partir des vraies questions finales.
  prompt=p.split('\n',1)[0]
  hole=re.search(r'\$([^$]*\\ldots[^$]*)\$',prompt)
  if hole:
   formula=hole[1].replace('\\times','*').replace('\\ldots','X').replace(' ','')
   left,right=formula.split('=')
   difference=lambda x:compute(left.replace('X',str(x)))-compute(right.replace('X',str(x)))
   intercept=difference(0);slope=difference(1)-intercept
   assert slope and difference(2)==intercept+2*slope,(i,prompt,'Relation non affine')
   candidates=[-intercept//slope] if (-intercept)%slope==0 and 0<=-intercept//slope<=1000 else []
   assert len(candidates)==1,(i,prompt,candidates)
   result=re.search(r'::: resultat\n(.*?)\n:::',p,re.S)[1]
   assert re.findall(r'\d+',result)==[str(candidates[0])],(i,prompt,result)
 # Les calculs numériques des neuf compétences sources doivent être présents
 # dans le raisonnement final et y avoir leur bonne valeur.
 source=json.loads((P/'sources_locales/chapitre.json').read_text(encoding='utf-8'))['exercices'][i-1]
 first=re.search(r'## Question 1 :.*?(?=\n## Question 2 :)',steps,re.S)[0]
 final_formulas=[s.replace('\\times','*').replace(' ','') for s in re.findall(r'\$([^$]+)\$',first)]
 for condition in source.get('check','').split(' and '):
  expr=condition.split('==')[0]
  if re.fullmatch(r'\d+(?:[+*\-]\d+)+',expr):
   expected=compute(expr)
   assert any(t==expr+'='+str(expected) for t in final_formulas),(i,expr,expected,'Calcul source absent')
 if P.name.startswith('09_') and i==4:
  result=re.search(r'::: resultat\n(.*?)\n:::',first,re.S)[1]
  even,odd=result.split('Impairs :')
  assert all(int(x)%2==0 for x in re.findall(r'\d+',even))
  assert all(int(x)%2==1 for x in re.findall(r'\d+',odd))
 if P.name.startswith('09_') and i==5:
  result=re.search(r'::: resultat\n(.*?)\n:::',first,re.S)[1]
  bounds=list(map(int,re.findall(r'\d+',source['consigne'])))
  assert list(map(int,re.findall(r'\d+',result)))==list(range(bounds[0],bounds[1]+1,2))
mapping=json.loads((P/'figures/correspondance.json').read_text(encoding='utf-8'))
assert 'nouveau' in mapping['cours'] and 'nouvelle' in mapping['fiches']
assert len(re.findall(r'^\| \d+ \|', (P/'COUVERTURE.md').read_text(encoding='utf-8'),re.M))==9
ns={};exec((P/'figures/figures.py').read_text(encoding='utf-8'),ns)
for section in mapping.values():
 for places in section.values():
  for pic in places.values():assert Path(pic['fichier']).stem in ns['FIGURES']
assert 'multiplication posée' not in (P/'cours_nouveau.txt').read_text(encoding='utf-8').lower()
print(P.name,': 9 exercices,',sum(len(re.findall(r'^## Question ',b,re.M)) for b in blocks),'questions ;',total,'égalités recalculées ; solutions identiques ; correspondances TikZ valides.')
'''

def write(code):
 d=next(ROOT.glob(f'{code:02}_*'));source=json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf-8'));data=items(code,source)
 fig,correspond=build_figures(code,data,source);blocks=[]
 for i,item in enumerate(data,1):
  level='easy' if i<=3 else 'medium' if i<=6 else 'hard';kind='Découverte' if i<=3 else 'Entraînement' if i<=6 else 'Problème';qs=item['questions']
  en=MARK+'\n'+item['enonce']+'\n\n'+'\n'.join(f"{j}. {q['question']}" for j,q in enumerate(qs,1))
  steps=MARK+'\n'
  for j,q in enumerate(qs,1):
   steps+=f"\n## Question {j} : {q['question']}\n\n"+boxes('methode',q['methode'])+'\n\n'+boxes('etape','\n\n'.join(q['etapes']),'Calculer et expliquer')+'\n\n'+boxes('resultat',q['resultat'])+'\n'
  sol=MARK+'\n'+'\n'.join(f"{j}. {q['resultat']}" for j,q in enumerate(qs,1))
  images='Images: '+','.join(v['fichier'] for v in correspond['exercices'].get(f'nouveau-{i}',{}).values())+'\n' if f'nouveau-{i}' in correspond['exercices'] else ''
  blocks.append(f"===\n{kind} - {item['titre']}\nId: nouveau-{i}\nDifficulté: {level}\n{images}\nÉnoncé:\n{en}\n\nÉtapes:\n{steps}\nSolution:\n{sol}\n")
 (d/'exercices.txt').write_text('\n'.join(blocks),encoding='utf-8')
 (d/'cours_nouveau.txt').write_text('Titre: '+source['titre']+'\n\n'+MARK+'\n'+COURSES[code]+'\n',encoding='utf-8')
 (d/'fiche_nouvelle.txt').write_text(summary(code),encoding='utf-8')
 figures=d/'figures';figures.mkdir(exist_ok=True)
 (figures/'figures.py').write_text('"""Figures TikZ style livre. Compiler seulement sur créneau autorisé."""\nFIGURES = '+repr(fig)+'\n',encoding='utf-8')
 (figures/'correspondance.json').write_text(json.dumps(correspond,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (d/'verif_math.py').write_text(VERIFY,encoding='utf-8')
 cover='# Couverture des neuf exercices sources\n\nSource locale : `sources_locales/chapitre.json`, exercices 1 à 9, conservés en lecture seule. Chacun est développé en cinq questions avec méthode, raisonnement et résultat.\n\n| Source | Compétence et consigne initiale | Exercice final | Questions |\n|---|---|---|---|\n'
 for i,s in enumerate(source['exercices'],1):cover+=f"| {i} | {s['consigne'].replace('|','/')} | nouveau-{i} — {TITLES[code][i-1]} | 1 à 5 |\n"
 cover+='\nLes questions 2 à 5 prolongent le calcul ou la compétence initiale : opérations voisines, contrôle inverse, facteurs manquants, échanges ou justification. Aucun des neuf exercices sources n’est abandonné.\n'
 (d/'COUVERTURE.md').write_text(cover,encoding='utf-8')
 report=f'''# Rapport — {source['titre']}

État : textes, figures TikZ et contrôle mathématique prêts ; compilation et contrôle visuel attendent le créneau de l’orchestrateur.

- Cours et fiche entièrement réécrits en format v1, exemples expliqués et conseils adressés à l’enfant.
- Neuf exercices sources développés en neuf exercices `nouveau-1` à `nouveau-9`, cinq questions chacun : 45 questions. Les méthodes sont calculatoires et les raisonnements explicites. Les solutions reprennent exactement les résultats encadrés.
- Domaine numérique : nombres entiers et résultats jusqu’à 1 000. Multiplications par sens, tables, doubles et décomposition ; aucune technique de multiplication posée. Soustraction posée par échanges. Partages expliqués par produits ou doubles.
- {len(fig)} figures TikZ préparées, aucune ancienne image conservée. Figures numériques en colonnes lorsque le calcul posé est travaillé. Correspondances `cours:nouveau`, `fiches:nouvelle`, `exercices:nouveau-N`.
- `verif_math.py` autonome relit les trois fichiers finaux, recalcule les égalités, contrôle les moitiés, les neuf blocs, les 45 méthodes, l’identité résultat/solution et les correspondances des figures.
- Aucun accès en base, aucun `manage.py`, aucun import, aucun changement des sources.

Programme de référence : [programme de mathématiques du cycle 2 applicable depuis 2025]({PROGRAMME}). Repérage transmis par l’orchestrateur. La couverture exacte des neuf sources figure dans `COUVERTURE.md`.

À effectuer avant statut prêt : compilation LuaLaTeX, lecture de chaque image, validation de syntaxe, aperçu et contrôle téléphone/ordinateur. Aucun contrôle visuel n’est déclaré effectué avant cela.
'''
 (d/'RAPPORT.md').write_text(report,encoding='utf-8')
 (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'ce1_calculs','maj':'2026-11-02','detail':'Textes et contrôles prêts ; compilation et QA visuelle attendues.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code, len(data),'exercices',sum(len(x['questions']) for x in data),'questions',len(fig),'figures')

if __name__=='__main__':
 for code in range(5,14):write(code)
