"""Réécriture pédagogique des six notions du lot coordination ; sources immuables."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,ROUND_HALF_UP
import json,re
ROOT=Path(__file__).resolve().parent.parent
MARK='<!-- optitab:1 -->'
def d(v):
 v=F(v)
 if v.denominator==1:return str(v.numerator)
 den=v.denominator
 for prime in (2,5):
  while den%prime==0:den//=prime
 assert den==1,('Ecriture decimale non exacte',v)
 x=Decimal(v.numerator)/Decimal(v.denominator)
 return format(x,'f').rstrip('0').rstrip('.').replace('.','{,}')
def t(v):
 v=F(v);return str(v.numerator) if v.denominator==1 else rf'\frac{{{v.numerator}}}{{{v.denominator}}}'
def m(s):return '$'+s+'$'
def q(text,method,detail,result):return dict(question=text,methode=method,etape=detail,resultat=result)
def eq(s):return m(s)
def quantity(n,word):return f'{n} {word}'+('s' if n!=1 else '')
def g(n):return f'{n:,}'.replace(',',r'\,')
def pack(title,intro,qs,lesson):return dict(titre=title,intro=intro,questions=qs,retenir=lesson)

def numeration(j,l):
 if j==0:
  n=[1234015608,7008040090,9999999500][l];groups=[n//10**9,(n//10**6)%1000,(n//1000)%1000,n%1000]
  add=[1000,1000000,1000][l];v=n+add
  return pack('Lire les classes et les retenues',f'Le compteur d’une bibliothèque numérique indique {n:,} consultations. Les espaces séparent les classes de trois chiffres.'.replace(',',' '),[
   q('Décomposer ce nombre en milliards, millions, milliers et unités.','Regrouper les chiffres par trois à partir de la droite.',f'On lit quatre classes. Une classe vide doit être écrite avec des zéros pour maintenir les rangs.',quantity(groups[0],'milliard')+', '+quantity(groups[1],'million')+', '+quantity(groups[2],'millier')+' et '+quantity(groups[3],'unité')+'.'),
   q('Donner le chiffre des millions et le nombre de millions entiers.','Distinguer le chiffre d’un rang et la quantité de groupes complets.',f'La classe des millions vaut {groups[1]}. Son dernier chiffre indique les millions ; les milliards comptent aussi des millions.',f'Chiffre des millions : {groups[1]%10} ; nombre de millions entiers : {n//10**6}.'),
   q('Écrire une décomposition additive.','Multiplier chaque classe par la valeur de son unité.','$$\n'+r'\begin{aligned}'+ '\n'+rf'{g(n)}&={groups[0]}\times1\,000\,000\,000'+r'\\'+'\n'+rf'&\quad+{groups[1]}\times1\,000\,000'+r'\\'+'\n'+rf'&\quad+{groups[2]}\times1\,000+{groups[3]}'+'\n'+r'\end{aligned}'+'\n$$',quantity(groups[0],'milliard')+' + '+quantity(groups[1],'million')+' + '+quantity(groups[2],'millier')+' + '+quantity(groups[3],'unité')+'.'),
   q(f'Le compteur augmente de {add:,} consultations. Donner la nouvelle valeur et expliquer les retenues éventuelles.'.replace(',',' '),'Ajouter dans le bon rang, puis regrouper les classes si elles dépassent 999.',eq(rf'{g(n)}+{g(add)}={g(v)}')+' Une classe qui atteint 1 000 se reporte dans la classe immédiatement à gauche.',f'{v:,} consultations.'.replace(',',' '))],
   'Un chiffre indique un seul rang ; le nombre de millions comprend tous les groupes complets d’un million.')
 if j==1:
  a=[4107,30205,12008][l];x=F(a,1000);integer=a//1000;digits=[a//100%10,a//10%10,a%10]
  return pack('Le rôle des zéros dans une mesure',f'Une balance affiche {m(d(x))} kg. On utilise les rangs unités, dixièmes, centièmes et millièmes.',[
   q('Donner la partie entière et les trois chiffres après la virgule.','Lire chaque rang, y compris les rangs occupés par zéro.',f'À gauche de la virgule : {integer}. À droite, les rangs sont successivement dixièmes, centièmes et millièmes.',f'Partie entière : {integer} ; dixièmes : {digits[0]} ; centièmes : {digits[1]} ; millièmes : {digits[2]}.'),
   q('Décomposer cette mesure en unités et fractions d’unité.','Associer chaque chiffre à sa valeur.',eq(rf'{d(x)}={integer}+\frac{{{digits[0]}}}{{10}}+\frac{{{digits[1]}}}{{100}}+\frac{{{digits[2]}}}{{1000}}'),eq(rf'{integer}+\frac{{{digits[0]}}}{{10}}+\frac{{{digits[1]}}}{{100}}+\frac{{{digits[2]}}}{{1000}}')+' kg.'),
   q('Écrire la mesure en grammes.','Un kilogramme contient 1 000 grammes.',eq(rf'{d(x)}\times1000={a}'),f'{a} g.'),
   q('Peut-on supprimer le zéro intérieur situé après la virgule ? Peut-on ajouter un zéro tout à droite ?','Distinguer un zéro qui réserve un rang d’un zéro final.',f'Supprimer un zéro intérieur décale les chiffres suivants et change leur valeur. Ajouter un zéro final ne modifie aucun rang déjà présent.',f'Le zéro intérieur est nécessaire ; ajouter un zéro à droite ne change pas la mesure.')],
   'Les zéros intérieurs maintiennent les rangs. Les zéros finaux après la virgule peuvent être ajoutés ou retirés.')
 if j==2:
  values=[[F(45,1000),F(2375,100),F(6,10)],[F(8,1000),F(407,100),F(32,10)],[F(305,1000),F(12008,100),F(15,100)]][l]
  qs=[]
  for x in values:
   qs.append(q(f'Écrire {m(d(x))} sous forme d’une fraction décimale de dénominateur 1 000.','Compter le nombre de millièmes.',f'On peut compléter l’écriture avec des zéros jusqu’au rang des millièmes. '+eq(rf'{d(x)}=\frac{{{int(x*1000)}}}{{1000}}'),eq(rf'\frac{{{int(x*1000)}}}{{1000}}')+'.'))
  x=values[0]
  qs.append(q('Un élève affirme que tous ces nombres sont inférieurs à 1 parce qu’ils sont décimaux. A-t-il raison ?','Comparer la partie entière à 1.',f'Un nombre décimal peut être inférieur, égal ou supérieur à 1. Ici, '+m(d(values[1]))+' possède une partie entière non nulle.',f'Non : {m(d(values[1]))} est un nombre décimal supérieur à 1.'))
  return pack('Choisir une fraction décimale','On souhaite exprimer tous les nombres suivants en millièmes.',qs,'Décimal décrit une écriture possible, pas la taille du nombre.')
 if j==3:
  a,b=[(7,35),(12,8),(103,406)][l];den=100 if l<2 else 1000;x=F(a)+F(b,den)
  return pack('Recomposer un nombre mixte',f'Un nombre est égal à {m(rf"{a}+\frac{{{b}}}{{{den}}}")}.',[
   q('Écrire ce nombre avec une virgule.','Conserver la partie entière et placer la fraction au bon rang.',f'Le dénominateur {den} désigne des '+('centièmes.' if den==100 else 'millièmes.')+' '+eq(rf'{a}+\frac{{{b}}}{{{den}}}={d(x)}'),eq(d(x))+'.'),
   q(f'Écrire ce nombre sous la forme d’une fraction de dénominateur {den}.','Convertir d’abord les unités entières.',eq(rf'{a}=\frac{{{a*den}}}{{{den}}}')+' puis '+eq(rf'\frac{{{a*den}}}{{{den}}}+\frac{{{b}}}{{{den}}}=\frac{{{a*den+b}}}{{{den}}}'),eq(rf'\frac{{{a*den+b}}}{{{den}}}')+'.'),
   q('Donner le nombre de dixièmes entiers contenus dans ce nombre.','Compter les groupes complets d’un dixième.',eq(rf'{d(x)}\times10={d(x*10)}')+f' : on ne retient que les {int(x*10)} groupes complets.',f'{int(x*10)} dixièmes entiers.'),
   q('Ajouter un dixième, puis donner la nouvelle écriture décimale.','Un dixième correspond à dix centièmes ou cent millièmes.',eq(rf'{d(x)}+0{{,}}1={d(x+F(1,10))}'),eq(d(x+F(1,10)))+'.')],
   'Pour passer d’un nombre mixte à une fraction, les unités entières doivent être exprimées avec le même partage.')
 if j==4:
  a=[507,2004,7056][l];den=100 if l==0 else 1000;x=F(a,den);cent=int(x*100);digit=int(x*100)%10
  return pack('Relire une copie de numération',f'On étudie le nombre {m(d(x))}. Nora confond « chiffre des centièmes » et « nombre de centièmes entiers ».',[
   q('Donner le chiffre des centièmes et sa valeur dans le nombre.','Le deuxième chiffre après la virgule indique les centièmes.',f'Le chiffre est {digit}. Sa contribution est '+eq(rf'\frac{{{digit}}}{{100}}={d(F(digit,100))}')+'.',f'Chiffre : {digit} ; valeur : {m(d(F(digit,100)))}.'),
   q('Donner le nombre de centièmes entiers contenus dans le nombre.','Chaque unité entière contient 100 centièmes.',eq(rf'{d(x)}\times100={d(x*100)}')+f' : {cent} groupes de centièmes sont complets.',f'{cent} centièmes entiers.'),
   q('La phrase « le chiffre des centièmes vaut le nombre de centièmes » est-elle correcte ?','Un chiffre appartient à la liste de 0 à 9 ; un nombre de parts peut dépasser 9.',f'Ici, le chiffre est {digit}, tandis que l’on compte {cent} centièmes complets.',f'Non : {digit} et {cent} désignent deux informations différentes.'),
   q('Écrire ce nombre sous deux formes égales avec une virgule.','Ajouter des zéros finaux sans changer les rangs.',f'On peut ajouter un zéro à droite du dernier chiffre décimal : les rangs déjà écrits ne changent pas.',eq(d(x)+'='+d(x)+'0')+'.')],
   'Lire la question avant de répondre : le chiffre d’un rang et le nombre de parts de ce rang sont différents.')
 if j==5:
  aa,bb=[(3,4),(7,5),(9,8)][l];x=F(aa,bb)
  return pack('Décimal ou non décimal ?',f'On compare les fractions {m(t(x))} et '+m(r'\frac13')+'.',[
   q(f'Écrire {m(t(x))} avec un dénominateur 1 000.','Chercher combien de fois le dénominateur entre dans 1 000.',eq(rf'{bb}\times{1000//bb}=1000')+' donc '+eq(rf'\frac{{{aa}}}{{{bb}}}=\frac{{{aa*(1000//bb)}}}{{1000}}'),eq(rf'\frac{{{aa*(1000//bb)}}}{{1000}}')+'.'),
   q('En déduire son écriture décimale exacte.','Lire la fraction en millièmes.',eq(rf'\frac{{{aa*(1000//bb)}}}{{1000}}={d(x)}'),eq(d(x))+'.'),
   q(r'Effectuer les premières étapes de $1\div3$. Que devient le reste ?','Poursuivre le partage des unités en dixièmes puis en centièmes.',r'$10=3\times3+1$. À chaque nouveau rang, le reste 1 fournit encore 10 parts du rang suivant. Le chiffre 3 se répète sans fin.',r'$\frac13=0{,}333\ldots$ ; l’écriture décimale ne se termine pas.'),
   q(r'$\frac13=0{,}33$ est-il une égalité exacte ?','Vérifier en multipliant par 3.',r'$0{,}33\times3=0{,}99$, ce qui n’est pas égal à 1. $0{,}33$ est seulement une valeur approchée.',r'Non ; $\frac13\approx0{,}33$.')],
   'Un nombre décimal possède une écriture décimale finie. Une approximation ne s’écrit pas avec le signe égal.')
 a,b=[(2,75),(5,8),(12,405)][l];x=F(a)+F(b,1000)
 return pack('Une réserve mesurée en litres',f'Une réserve contient {a} L et {b} mL. On rappelle que 1 L vaut 1 000 mL.',[
  q('Donner la contenance en millilitres.','Convertir les litres puis additionner.',eq(rf'{a}\times1000+{b}={a*1000+b}'),f'{a*1000+b} mL.'),
  q('Donner la contenance en litres avec une virgule.','Partager le nombre de millilitres par 1 000.',eq(rf'\frac{{{a*1000+b}}}{{1000}}={d(x)}'),eq(d(x))+' L.'),
  q('Écrire la contenance en litres sous forme de nombre mixte.','Séparer les litres entiers et la fraction de litre.',f'Les {b} mL représentent '+m(rf'\frac{{{b}}}{{1000}}')+' L.',eq(rf'{a}+\frac{{{b}}}{{1000}}')+' L.'),
  q('On ajoute 250 mL. Quelle contenance obtient-on en litres ?','Additionner dans une même unité.',eq(rf'{a*1000+b}+250={a*1000+b+250}')+' mL, puis '+eq(rf'\frac{{{a*1000+b+250}}}{{1000}}={d(x+F(1,4))}'),eq(d(x+F(1,4)))+' L.')],
  'Le lien entre unités donne du sens aux écritures décimales : 1 mL est un millième de litre.')

def reperage(j,l):
 if j==0:
  origin=F([2,37,403][l],[1,10,100][l]);pas=F(1,[10,100,1000][l]);a=origin+3*pas;b=origin+8*pas
  return pack('Lire les intervalles d’une graduation',f'Sur une graduation régulière, le premier trait vaut {m(d(origin))} et le dixième intervalle se termine à {m(d(origin+10*pas))}. Il y a dix intervalles égaux. [IMAGE_1]',[
   q('Quelle est la valeur d’un intervalle ?','Diviser l’écart total par le nombre d’intervalles.',eq(rf'({d(origin+10*pas)}-{d(origin)})\div10={d(pas)}'),eq(d(pas))+'.'),
   q('Donner l’abscisse du point A situé trois intervalles après le premier trait.','Ajouter trois fois le pas.',eq(rf'{d(origin)}+3\times{d(pas)}={d(a)}'),eq(d(a))+'.'),
   q('Le point B est huit intervalles après le premier trait. Donner son abscisse puis la distance AB en unités.','Calculer B puis compter les intervalles séparant A et B.',eq(rf'{d(origin)}+8\times{d(pas)}={d(b)}')+' et '+eq(rf'{d(b)}-{d(a)}={d(5*pas)}'),f'B : {m(d(b))} ; AB : {m(d(5*pas))} unité.'),
   q('Un élève divise par 11 parce qu’il compte onze traits. Expliquer son erreur.','Compter les espaces entre les traits.',f'Dix intervalles possèdent onze extrémités. La valeur du pas dépend des dix espaces, pas du nombre de traits.',f'Il faut diviser par 10, car il y a dix intervalles.')],
   'La première vérification sur une droite graduée consiste à compter les intervalles.')
 if j==1:
  a=F([8,127,403][l],10**[1,1,2][l]);b=a-F([5,1,3][l],100);c=a+F(1,1000);v=[a,b,c,a]
  return pack('Ranger sans compter les chiffres',f'Quatre mesures sont {m(d(a))}, {m(d(b))}, {m(d(c))} et {m(d(a)+"0")}.',[
   q('Écrire les quatre nombres avec trois chiffres après la virgule.','Compléter par des zéros finaux.',', '.join(m(f'{Decimal(x.numerator)/Decimal(x.denominator):.3f}'.replace('.','{,}')) for x in v)+'.',' ; '.join(m(f'{Decimal(x.numerator)/Decimal(x.denominator):.3f}'.replace('.','{,}')) for x in v)+'.'),
   q('Lesquels sont égaux ? Justifier.','Les zéros finaux ne modifient pas la valeur.',eq(d(a)+'='+d(a)+'0'),f'La première et la quatrième mesure sont égales.'),
   q('Ranger les nombres dans l’ordre croissant, en signalant l’égalité.','Comparer les parties entières puis chaque rang décimal.',f'Après avoir écrit le même nombre de décimales, le premier rang différent permet de comparer.',eq(d(b)+r'\lt'+d(a)+'='+d(a)+'0'+r'\lt'+d(c))+'.'),
   q('Quel est l’écart entre la plus grande et la plus petite mesure ?','Soustraire la plus petite de la plus grande.',eq(rf'{d(c)}-{d(b)}={d(c-b)}'),eq(d(c-b))+'.')],
   'Le nombre de chiffres ne permet pas de comparer des décimaux.')
 if j==2:
  x=F([3476,9995,12004][l],1000);lo=x.numerator//x.denominator;ld=F(int(x*10),10);lc=F(int(x*100),100)
  return pack('Encadrer à plusieurs précisions',f'On étudie {m(d(x))}. On demande des encadrements entre deux graduations consécutives.',[
   q('Encadrer à l’unité.','Repérer les deux entiers consécutifs.',f'La partie entière est {lo} ; l’entier suivant est {lo+1}.',eq(rf'{lo}\lt{d(x)}\lt{lo+1}')+'.'),
   q('Encadrer au dixième.','Garder les dixièmes puis ajouter un dixième pour la borne supérieure.',eq(rf'{d(ld)}\lt{d(x)}\lt{d(ld+F(1,10))}'),eq(rf'{d(ld)}\lt{d(x)}\lt{d(ld+F(1,10))}')+'.'),
   q('Encadrer au centième.','Choisir deux centièmes consécutifs.',eq(rf'{d(lc)}\lt{d(x)}\lt{d(lc+F(1,100))}'),eq(rf'{d(lc)}\lt{d(x)}\lt{d(lc+F(1,100))}')+'.'),
   q('La borne inférieure au centième est-elle toujours l’arrondi au centième ? Expliquer ici.','Comparer les distances aux deux bornes.',eq(rf'{d(x)}-{d(lc)}={d(x-lc)}')+' et '+eq(rf'{d(lc+F(1,100))}-{d(x)}={d(lc+F(1,100)-x)}'),'Non, pas toujours. Ici, '+('la borne inférieure convient : ' if x-lc<F(5,1000) else 'on choisit la borne supérieure : ')+f'l’arrondi est {m(str((Decimal(x.numerator)/Decimal(x.denominator)).quantize(Decimal(".01"),rounding=ROUND_HALF_UP)).replace(".","{,}"))}.')],
   'Un encadrement donne deux bornes ; un arrondi donne une seule valeur proche.')
 if j==3:
  a=F([23,120,999][l],100);b=a+F(1,100);mid=(a+b)/2;low=(a+mid)/2
  return pack('Trouver des nombres entre deux centièmes',f'On cherche des nombres strictement compris entre {m(d(a))} et {m(d(b))}.',[
   q('Peut-on trouver un centième strictement entre ces deux nombres ?','Les deux bornes sont des centièmes consécutifs.',f'Leur écart est '+eq(rf'{d(b)}-{d(a)}=0{{,}}01')+'. Aucun centième supplémentaire ne se place entre eux.',f'Non, aucun nombre écrit avec seulement deux décimales ne convient.'),
   q('Trouver un millième situé entre les deux bornes.','Ajouter cinq millièmes à la borne inférieure.',eq(rf'{d(a)}+0{{,}}005={d(mid)}'),eq(d(mid))+'.'),
   q('Trouver un autre nombre entre la borne inférieure et le nombre précédent.','Partager encore l’intervalle en deux.',eq(rf'({d(a)}+{d(mid)})\div2={d(low)}'),eq(d(low))+'.'),
   q('Que répondrais-tu à « il n’y a plus de place entre ces deux décimaux » ?','Distinguer l’écriture choisie et l’existence de nombres.',f'En ajoutant des rangs décimaux, on peut partager encore chaque intervalle. Le milieu des deux bornes en donne un exemple.',f'Il reste toujours un nombre décimal entre deux décimaux distincts.')],
   'Deux graduations consécutives à une précision donnée peuvent contenir d’autres nombres plus précis.')
 if j==4:
  x=F([7364,9995,12005][l],1000);dec=Decimal(x.numerator)/Decimal(x.denominator);qs=[]
  for label,p in [('l’unité','1'),('au dixième','.1'),('au centième','.01')]:
   result=dec.quantize(Decimal(p),rounding=ROUND_HALF_UP)
   qs.append(q(f'Donner l’arrondi à {label}.' if label=='l’unité' else f'Donner l’arrondi {label}.','Regarder le premier chiffre situé après le rang demandé.',f'On repère les deux valeurs consécutives du rang demandé. Le chiffre suivant décide : de 0 à 4, on garde la borne inférieure ; de 5 à 9, on prend la borne supérieure.',eq(str(result).replace('.','{,}'))+'.'))
  qs.append(q('Doit-on partir de l’arrondi au dixième pour obtenir l’arrondi à l’unité ?','Toujours repartir du nombre initial.',f'Arrondir une valeur déjà arrondie peut cumuler les erreurs. Pour {m(d(x))}, on relit directement le chiffre des dixièmes.',f'Non : chaque arrondi se calcule à partir du nombre initial.'))
  return pack('Arrondir et gérer les retenues',f'Une mesure exacte vaut {m(d(x))}.',qs,'Ne pas confondre arrondi et troncature ; une retenue peut modifier la partie entière.')
 if j==5:
  a=F([8,12,99][l],10);b=a-F(5,100)
  return pack('Détecter des comparaisons fausses','On relit quatre affirmations. Pour chacune, expliquer le raisonnement.',[
   q(f'« {m(d(a))} est inférieur à {m(d(b))} parce qu’il a moins de décimales. » Vrai ou faux ?','Compléter avec des zéros.',eq(d(a)+'='+d(a)+'0')+' et '+eq(d(a)+r'\gt'+d(b)),f'Faux : {m(d(a))} est plus grand.'),
   q(r'« $4{,}09=4{,}9$. » Vrai ou faux ?','Comparer dixièmes et centièmes.',r'$4{,}09$ possède 0 dixième et 9 centièmes ; $4{,}9$ possède 9 dixièmes, soit 90 centièmes.',r'Faux : $4{,}09\lt4{,}90$.'),
   q(r'« $2{,}995$ s’arrondit à $2{,}99$ au centième. » Vrai ou faux ?','Le chiffre des millièmes est 5.',r'On choisit le centième supérieur. $2{,}99+0{,}01=3{,}00$.',r'Faux : l’arrondi au centième est $3{,}00$.'),
   q(r'« $0{,}33$ est exactement égal à $\frac13$. » Vrai ou faux ?','Contrôler le produit par 3.',r'$0{,}33\times3=0{,}99$ ; or $\frac13\times3=1$.',r'Faux : $0{,}33$ est une approximation de $\frac13$.')],
   'Une justification fondée sur les rangs est plus fiable qu’une comparaison du nombre de chiffres.')
 x=F([12495,7496,9994][l],1000);threshold=F([125,75,100][l],10);rnd=(Decimal(x.numerator)/Decimal(x.denominator)).quantize(Decimal('.1'),rounding=ROUND_HALF_UP)
 return pack('Un seuil exige une valeur précise',f'Une mesure vaut {m(d(x))} kg. Le seuil d’acceptation est {m(d(threshold))} kg : une mesure strictement inférieure est acceptée.',[
  q('Comparer la mesure exacte au seuil.','Comparer les nombres à la même précision.',eq(d(x)+r'\lt'+d(threshold)),f'La mesure exacte est inférieure au seuil.'),
  q('Donner l’arrondi au dixième de la mesure.','Lire le chiffre des centièmes.',f'Le premier chiffre après les dixièmes conduit à choisir '+m(str(rnd).replace('.','{,}'))+'.',eq(str(rnd).replace('.','{,}'))+' kg.'),
  q('Cet arrondi permet-il toujours de décider si la mesure est acceptée ?','Distinguer une valeur exacte d’une information arrondie.',f'L’arrondi peut devenir égal au seuil ou masquer un petit écart. On doit utiliser la valeur exacte disponible.',f'Il faut comparer {m(d(x))} au seuil exact ; cette mesure est acceptée.'),
  q('Calculer l’écart restant avant d’atteindre le seuil.','Soustraire la mesure au seuil.',eq(rf'{d(threshold)}-{d(x)}={d(threshold-x)}'),eq(d(threshold-x))+' kg.')],
  'Une valeur arrondie facilite la lecture ; une décision au voisinage d’un seuil demande la précision adaptée.')

def calcul(j,l):
 if j==0:
  a=F([127,2075,995][l],100);b=F([385,896,705][l],100);total=a+b;cash=F([10,35,20][l])
  return pack('Additionner puis rendre la monnaie',f'Deux achats coûtent {m(d(a))} € et {m(d(b))} €. On paie avec {m(d(cash))} €.',[
   q('Estimer le total avant de calculer.','Remplacer chaque prix par un entier proche.',f'Les prix sont proches de {round(a)} € et de {round(b)} €. Leur somme donne un contrôle de taille.',f'Un ordre de grandeur est {round(a)+round(b)} €.'),
   q('Calculer le montant exact.','Aligner les unités, les dixièmes et les centièmes.',eq(rf'{d(a)}+{d(b)}={d(total)}'),eq(d(total))+' €.'),
   q('Calculer la monnaie rendue.','Soustraire le total de la somme versée.',eq(rf'{d(cash)}-{d(total)}={d(cash-total)}'),eq(d(cash-total))+' €.'),
   q('Vérifier le résultat par une autre opération.','Ajouter dépense et monnaie.',eq(rf'{d(total)}+{d(cash-total)}={d(cash)}'),f'La dépense et la monnaie reconstituent {m(d(cash))} €.')],
   'Dans une opération posée sur des décimaux, on aligne les rangs, donc les virgules.')
 if j==1:
  x=F([456,307,7508][l],100);qs=[]
  for symbol,f in [(r'\times10',F(10)),(r'\times100',F(100)),(r'\div1000',F(1,1000)),(r'\times0{,}01',F(1,100))]:
   qs.append(q(f'Calculer {m(d(x)+symbol)} en expliquant la valeur des chiffres.','Utiliser les liens entre les unités de numération.',f'Chaque chiffre change de rang. Multiplier par 0,01 revient à diviser par 100. '+eq(d(x)+symbol+'='+d(x*f)),eq(d(x*f))+'.'))
  return pack('Changer d’unité de numération',f'On part chaque fois du même nombre {m(d(x))}.',qs,'La valeur de chaque chiffre change ; on complète par des zéros quand cela est nécessaire.')
 if j==2:
  a,b=[(F(23,10),F(14,10)),(F(125,100),F(24,10)),(F(305,100),F(16,10))][l]
  return pack('Comprendre le produit de deux décimaux',f'Un rectangle mesure {m(d(a))} cm sur {m(d(b))} cm.',[
   q('Quelle opération donne son aire ?','Multiplier les deux longueurs exprimées dans la même unité.',f'L’aire du rectangle est le produit longueur par largeur.',eq(d(a)+r'\times'+d(b))+r' $\mathrm{cm}^2$.'),
   q('Calculer le produit en utilisant des nombres entiers.','Remplacer les facteurs par des fractions décimales.',eq(rf'{d(a)}\times{d(b)}=\frac{{{int(a*100)}\times{int(b*10)}}}{{1000}}')+' puis '+eq(rf'\frac{{{int(a*b*1000)}}}{{1000}}={d(a*b)}'),eq(d(a*b))+r' $\mathrm{cm}^2$.'),
   q('La largeur est divisée par 10, la longueur ne change pas. Quelle est la nouvelle aire ?','Diviser aussi le produit par 10.',eq(rf'{d(a*b)}\div10={d(a*b/10)}'),eq(d(a*b/10))+r' $\mathrm{cm}^2$.'),
   q('Multiplier agrandit-il toujours un nombre positif ? Illustrer avec 0,5.','Multiplier par 0,5 revient à prendre la moitié.',eq(rf'{d(a)}\times0{{,}}5={d(a/2)}')+f', qui est inférieur à {m(d(a))}.',f'Non : multiplier un nombre positif par un facteur entre 0 et 1 le diminue.')],
   'Le placement de la virgule dans le produit doit être justifié et contrôlé par un ordre de grandeur.')
 if j==3:
  x=F([128,375,602][l],10)
  return pack('Choisir un calcul mental efficace',f'Calculer mentalement en expliquant chaque transformation. On utilise {m(d(x))}.',[
   q(f'Calculer {m(d(x)+r"\times5")}.','Multiplier par 10 puis prendre la moitié.',eq(rf'{d(x)}\times10={d(x*10)}')+' puis '+eq(rf'{d(x*10)}\div2={d(x*5)}'),eq(d(x*5))+'.'),
   q(f'Calculer {m(d(x)+r"\times0{,}5")}.','Prendre la moitié.',eq(rf'{d(x)}\div2={d(x/2)}'),eq(d(x/2))+'.'),
   q(f'Calculer {m(d(x)+r"\times9")}.','Prendre dix fois le nombre puis retirer une fois ce nombre.',eq(rf'{d(x*10)}-{d(x)}={d(x*9)}'),eq(d(x*9))+'.'),
   q(f'Calculer {m(d(x)+r"\times1{,}1")}.','Ajouter au nombre son dixième.',eq(rf'{d(x)}+{d(x/10)}={d(x*F(11,10))}'),eq(d(x*F(11,10)))+'.')],
   'Un calcul mental efficace utilise le sens des opérations et les relations entre les nombres.')
 if j==4:
  x=F([72,135,406][l],10)
  return pack('Diagnostiquer une erreur de virgule',f'On relit les calculs d’un élève à partir du nombre {m(d(x))}.',[
   q(f'Il écrit {m(d(x)+r"\times0{,}1="+d(x*10))}. Corriger.','Multiplier par un dixième rend le résultat dix fois plus petit.',eq(rf'{d(x)}\times0{{,}}1={d(x/10)}'),eq(d(x/10))+'.'),
   q(r'Il écrit $2{,}3\times1{,}4=32{,}2$. Corriger en contrôlant la taille du résultat.','Le produit est proche de deux fois un et demi.',r'$23\times14=322$ ; les deux facteurs comportent au total deux chiffres après la virgule, donc $2{,}3\times1{,}4=3{,}22$.',r'$3{,}22$.'),
   q(r'Il écrit $12{,}7+3{,}85=5{,}12$. Expliquer pourquoi c’est impossible puis corriger.','Une somme de deux nombres positifs dépasse chacun d’eux.',r'$5{,}12\lt12{,}7$ : le résultat est impossible. En alignant les rangs : $12{,}70+3{,}85=16{,}55$.',r'$16{,}55$.'),
   q(r'Il écrit $20-7{,}35=13{,}35$. Vérifier avec l’opération inverse.','Ajouter le résultat proposé et le nombre retiré.',r'$13{,}35+7{,}35=20{,}70$, différent de 20. Le bon calcul est $20{,}00-7{,}35=12{,}65$.',r'$12{,}65$.')],
   'Une opération inverse ou un ordre de grandeur permet de repérer une erreur avant de valider un résultat.')
 if j==5:
  n=4+l;p=F(25+3*l,10);fee=F(6);budget=F(100+30*l);count=n*(3+l+2);cost=count*p+fee
  return pack('Organiser la commande d’un club',f'Un club prépare {n} ateliers. Chacun reçoit {3+l} carnets bleus et 2 verts. Chaque carnet coûte {m(d(p))} €. La livraison coûte 6 € pour la commande entière. Le budget est {m(d(budget))} €.',[
   q('Combien de carnets faut-il au total ?','Compter d’abord un atelier puis multiplier.',eq(rf'{n}\times({3+l}+2)={count}'),f'{count} carnets.'),
   q('Calculer le prix des carnets seuls.','Multiplier la quantité totale par le prix unitaire.',eq(rf'{count}\times{d(p)}={d(count*p)}'),eq(d(count*p))+' €.'),
   q('Calculer le prix de la commande livrée.','La livraison se paie une seule fois.',eq(rf'{d(count*p)}+6={d(cost)}'),eq(d(cost))+' €.'),
   q('Le budget suffit-il ? Calculer la somme restante ou manquante.','Comparer au budget puis calculer l’écart.',eq(rf'{d(budget)}-{d(cost)}={d(budget-cost)}'),f'Oui ; il reste {m(d(budget-cost))} €.')],
   'Prendre en compte la portée de chaque prix : par objet, par atelier ou pour toute la commande.')
 a=F(125+25*l,100);p=F(28+2*l,10);bread=F(12+l,10);total=a*p+2*bread;paid=F(20)
 return pack('Vérifier un ticket au marché',f'On achète {m(d(a))} kg de pommes à {m(d(p))} € le kilogramme et deux pains à {m(d(bread))} € l’unité. On paie 20 €.',[
  q('Calculer le prix des pommes.','Multiplier la masse par le prix du kilogramme.',eq(rf'{d(a)}\times{d(p)}={d(a*p)}'),eq(d(a*p))+' €.'),
  q('Calculer le prix des pains puis le total.','Additionner les deux catégories d’achats.',eq(rf'2\times{d(bread)}={d(2*bread)}')+' puis '+eq(rf'{d(a*p)}+{d(2*bread)}={d(total)}'),'Pains : '+eq(d(2*bread))+' € ; total : '+eq(d(total))+' €.'),
  q('Calculer la monnaie.','Soustraire le total à 20 €.',eq(rf'20-{d(total)}={d(paid-total)}'),eq(d(paid-total))+' €.'),
  q('Le commerçant oublie un pain sur le ticket. De combien le total est-il trop petit ? Quel total affiche-t-il ?','Le prix oublié est celui d’un seul pain.',eq(rf'{d(total)}-{d(bread)}={d(total-bread)}'),f'Il manque {m(d(bread))} € ; le total affiché est {m(d(total-bread))} €.')],
  'Un ticket se vérifie ligne par ligne ; le résultat doit garder une unité.')

def division(j,l):
 if j==0:
  n,b=[(157,12),(284,23),(356,24)][l];quot,rem=divmod(n,b)
  return pack('Donner un sens au quotient et au reste',f'On partage {n} jetons entre {b} élèves, sans couper les jetons.',[
   q('Encadrer le nombre de jetons par deux multiples consécutifs du nombre d’élèves.','Chercher le plus grand multiple qui ne dépasse pas le dividende.',eq(rf'{b}\times{quot}={b*quot}')+' et '+eq(rf'{b}\times{quot+1}={b*(quot+1)}'),eq(rf'{b*quot}\le{n}\lt{b*(quot+1)}')+'.'),
   q('Combien de jetons reçoit chaque élève ? Combien en reste-t-il ?','Attribuer le quotient entier à chacun et garder les jetons non distribués.',eq(rf'{n}-{b*quot}={rem}'),f'{quot} jetons par élève ; reste : '+quantity(rem,'jeton')+'.'),
   q('Écrire l’égalité de la division euclidienne et la condition sur le reste.','Le reste doit être inférieur au diviseur.',eq(rf'{n}={b}\times{quot}+{rem}')+' avec '+eq(rf'0\le{rem}\lt{b}'),eq(rf'{n}={b}\times{quot}+{rem}')+' et '+eq(rf'0\le{rem}\lt{b}')+'.'),
   q('Combien de jetons faut-il ajouter pour donner un jeton de plus à chaque élève ?','Compléter le reste jusqu’à un groupe supplémentaire.',eq(rf'{b}-{rem}={b-rem}'),f'{b-rem} jetons.')],
   'Dans une division euclidienne, le quotient et le reste sont entiers et le reste est strictement inférieur au diviseur.')
 if j==1:
  total=F([168,275,438][l],10);n=[4,5,6][l];part=total/n
  return pack('Partager une dépense exactement',f'{n} amis se partagent également une dépense de {m(d(total))} €.',[
   q('Écrire la division qui donne la part de chacun.','Le total est partagé en parts égales.',f'Le nombre de parts est {n}.',eq(d(total)+r'\div'+str(n))+'.'),
   q('Calculer la part exacte de chacun.','On peut convertir la dépense en centimes.',eq(rf'{int(total*100)}\div{n}={int(part*100)}')+' centimes, donc '+m(d(part))+' €.',eq(d(part))+' €.'),
   q('Vérifier que les parts reconstituent la dépense.','Multiplier une part par le nombre d’amis.',eq(rf'{d(part)}\times{n}={d(total)}'),f'Les {n} parts totalisent {m(d(total))} €.'),
   q('Un ami avance le paiement pour deux personnes. Quelle somme doit-il avancer ?','Additionner deux parts égales.',eq(rf'2\times{d(part)}={d(2*part)}'),eq(d(2*part))+' €.')],
   'Choisir une unité plus petite peut transformer un partage décimal en partage entier.')
 if j==2:
  n,b=[(53,8),(95,12),(127,24)][l];quot,rem=divmod(n,b)
  return pack('Choisir le nombre de boîtes nécessaire',f'Une association range {n} objets dans des boîtes contenant au maximum {b} objets. Chaque objet doit être rangé.',[
   q('Effectuer la division euclidienne.','Chercher les boîtes entièrement remplies et les objets restants.',eq(rf'{n}={b}\times{quot}+{rem}'),f'Quotient {quot}, reste {rem}.'),
   q('Combien de boîtes faut-il au minimum ?','Tout reste non nul nécessite une boîte supplémentaire.',f'{quot} boîtes pleines contiennent {b*quot} objets. Les {rem} objets restants occupent une dernière boîte.',f'{quot+1} boîtes.'),
   q('Combien de places restent libres au total ?','Comparer la capacité totale au nombre d’objets.',eq(rf'{b}\times{quot+1}-{n}={b*(quot+1)-n}'),quantity(b*(quot+1)-n,'place')+' libre'+('s' if b*(quot+1)-n!=1 else '')+'.'),
   q('Pourquoi arrondir le quotient au plus proche ne donne-t-il pas toujours la réponse ?','Il faut respecter l’obligation de ranger tous les objets.',f'Même un seul objet restant exige une boîte. On prend l’entier supérieur dès que le reste est non nul.',f'On choisit le nombre de boîtes suffisant, pas un arrondi ordinaire.')],
   'Interpréter le quotient dépend de la question : objets par boîte, boîtes pleines ou boîtes nécessaires.')
 if j==3:
  a,b=[(10,3),(20,6),(25,6)][l];hund=a*100//b;rounded=(Decimal(a)/Decimal(b)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
  return pack('Distinguer partage exact et valeur approchée',f'On partage {a} L de jus en {b} parts égales. Le jus peut être partagé aussi finement que nécessaire.',[
   q('Donner la part exacte en litres sous forme fractionnaire.','Le quotient exact s’écrit avec une fraction.',f'La multiplication de cette fraction par {b} reconstitue {a}.',eq(rf'\frac{{{a}}}{{{b}}}')+' L.'),
   q('Encadrer cette part entre deux centièmes consécutifs.','Effectuer la division jusqu’aux centièmes puis examiner le reste.',eq(rf'{d(F(hund,100))}\lt\frac{{{a}}}{{{b}}}\lt{d(F(hund+1,100))}'),eq(rf'{d(F(hund,100))}\lt\frac{{{a}}}{{{b}}}\lt{d(F(hund+1,100))}')+' L.'),
   q('Donner l’arrondi au centième.','Lire le chiffre des millièmes pour choisir le centième le plus proche.',f'La division ne se termine pas. Le chiffre suivant les centièmes conduit à '+m(str(rounded).replace('.','{,}'))+'.',eq(str(rounded).replace('.','{,}'))+' L.'),
   q('Peut-on utiliser le signe égal entre la fraction exacte et cet arrondi ?','Multiplier l’arrondi par le nombre de parts.',eq(rf'{str(rounded).replace(".","{,}")}\times{b}={d(F(rounded)*b)}')+f', différent de {a}.',f'Non : on utilise le signe '+m(r'\approx')+'.')],
   'Une fraction garde le quotient exact même lorsque la division décimale ne s’arrête pas.')
 if j==4:
  n=[126,245,480][l]
  return pack('Tester un partage sans reste',f'On dispose de {n} cartes. On cherche des paquets identiques sans carte restante.',[
   q('Peut-on partager les cartes en paquets de 2 ? Justifier.','Un entier est divisible par 2 si son chiffre des unités est pair.',f'Le chiffre des unités de {n} est {n%10}.',('Oui' if n%2==0 else 'Non')+f' ; le reste dans la division par 2 est {n%2}.'),
   q('Peut-on faire des paquets de 3 ? Justifier.','Additionner les chiffres et tester la divisibilité par 3.',f'La somme des chiffres vaut {sum(map(int,str(n)))}.',('Oui' if n%3==0 else 'Non')+f' ; le reste dans la division par 3 est {n%3}.'),
   q('Peut-on faire des paquets de 5 ? Justifier.','Observer le chiffre des unités : 0 ou 5 est nécessaire et suffisant.',f'Le chiffre des unités est {n%10}.',('Oui' if n%5==0 else 'Non')+f' ; le reste dans la division par 5 est {n%5}.'),
   q('Donner l’égalité de la division par 9.','Rechercher le multiple de 9 immédiatement inférieur ou égal.',eq(rf'{n}=9\times{n//9}+{n%9}'),eq(rf'{n}=9\times{n//9}+{n%9}')+'.')],
   'Être divisible signifie que la division euclidienne a un reste nul.')
 if j==5:
  n,b=[(53,8),(94,12),(127,24)][l];quot,rem=divmod(n,b);fakeq=quot-1;faker=rem+b
  return pack('Corriger une division mal terminée',f'Un élève écrit '+eq(rf'{n}={b}\times{fakeq}+{faker}')+'.',[
   q('Cette égalité numérique est-elle vraie ?','Calculer le membre de droite.',eq(rf'{b}\times{fakeq}+{faker}={n}'),f'Oui, l’égalité est vraie.'),
   q('Décrit-elle une division euclidienne terminée ?','Vérifier la condition sur le reste.',f'Le reste proposé {faker} est supérieur ou égal au diviseur {b}. Un groupe supplémentaire peut encore être formé.',f'Non : le reste doit être strictement inférieur à {b}.'),
   q('Corriger le quotient et le reste.','Retirer un diviseur du reste et augmenter le quotient d’une unité.',eq(rf'{faker}-{b}={rem}')+' et '+eq(rf'{fakeq}+1={quot}'),f'Quotient {quot}, reste {rem}.'),
   q('Écrire la vérification complète.','Contrôler l’égalité et la condition sur le reste.',eq(rf'{n}={b}\times{quot}+{rem}')+' avec '+eq(rf'0\le{rem}\lt{b}'),eq(rf'{n}={b}\times{quot}+{rem}')+f', reste inférieur à {b}.')],
   'Une égalité dividende = diviseur × quotient + reste ne suffit pas sans la condition sur le reste.')
 n=96+24*l;cap=12;price=[F(75,10),F(81,10),F(85,10)][l];fixed=F(18);boxes=n//cap;total=boxes*price+fixed;part=total/6
 return pack('Préparer et financer une expédition',f'On expédie {n} objets en cartons de 12. Chaque carton plein coûte {m(d(price))} € à expédier. Les frais fixes sont de 18 €. Six équipes partagent également le coût.',[
  q('Combien de cartons pleins faut-il ?','Diviser la quantité par la capacité.',eq(rf'{n}\div12={boxes}'),f'{boxes} cartons.'),
  q('Calculer le coût total de l’expédition.','Multiplier le nombre de cartons par le prix puis ajouter les frais fixes.',eq(rf'{boxes}\times{d(price)}+18={d(total)}'),eq(d(total))+' €.'),
  q('Calculer la part de chaque équipe.','Partager le coût total en six parts égales.',eq(rf'{d(total)}\div6={d(part)}'),eq(d(part))+' €.'),
  q('Contrôler le partage et préciser si une équipe peut payer moins sans modifier le total.','Reconstituer le total avec les six parts.',eq(rf'6\times{d(part)}={d(total)}')+' Si une seule part diminue et les autres restent fixes, la somme diminue.',f'Le total est correct ; une équipe ne peut pas payer moins si toutes les autres parts restent identiques.')],
  'Dans un problème en plusieurs étapes, écrire ce que représente chaque résultat intermédiaire.')

def programmes(j,l):
 a=2+l;b=3+2*l;c=4+l
 if j==0:
  x=F([3,75,125][l],[1,10,100][l]);y=(x+b)*a-c
  return pack('Suivre les étapes dans le bon ordre',f'Programme : choisir un nombre, ajouter {b}, multiplier le résultat par {a}, puis retirer {c}. Le nombre choisi est {m(d(x))}.',[
   q('Quel nombre obtient-on après l’addition ?','Partir du nombre choisi.',eq(rf'{d(x)}+{b}={d(x+b)}'),eq(d(x+b))+'.'),
   q('Quel nombre obtient-on après la multiplication ?','Multiplier le résultat précédent, pas seulement le nombre initial.',eq(rf'{d(x+b)}\times{a}={d((x+b)*a)}'),eq(d((x+b)*a))+'.'),
   q('Donner le résultat final.','Appliquer la dernière consigne.',eq(rf'{d((x+b)*a)}-{c}={d(y)}'),eq(d(y))+'.'),
   q('Écrire le calcul en une expression avec des parenthèses.','Les parenthèses imposent d’additionner avant de multiplier.',eq(rf'({d(x)}+{b})\times{a}-{c}={d(y)}'),eq(rf'({d(x)}+{b})\times{a}-{c}')+'.')],
   'Chaque instruction agit sur le résultat de l’étape précédente.')
 if j==1:
  x=5+l
  return pack('Reconnaître deux ordres différents',f'Programme A : ajouter {b}, puis multiplier par {a}. Programme B : multiplier par {a}, puis ajouter {b}. Départ : {x}.',[
   q('Calculer le résultat de A.','Faire l’addition avant la multiplication.',eq(rf'({x}+{b})\times{a}={(x+b)*a}'),eq(str((x+b)*a))+'.'),
   q('Calculer le résultat de B.','Faire la multiplication avant l’addition.',eq(rf'{x}\times{a}+{b}={x*a+b}'),eq(str(x*a+b))+'.'),
   q('Comparer les résultats et calculer leur écart.','La quantité ajoutée est multipliée dans A, mais pas dans B.',eq(rf'{(x+b)*a}-{x*a+b}={b*(a-1)}'),f'A donne {b*(a-1)} de plus que B.'),
   q('Quel programme est traduit par des parenthèses autour de la somme initiale ?','Lire la portée de la multiplication.',f'Dans A, toute la somme est multipliée. Dans B, seul le nombre initial est multiplié.',f'Le programme A est traduit par une somme entre parenthèses.')],
   'Changer l’ordre de deux opérations peut changer le résultat.')
 if j==2:
  x=4+2*l;y=x*a+b
  return pack('Retrouver un nombre de départ',f'On multiplie un nombre par {a}, puis on ajoute {b}. Le résultat final est {y}.',[
   q('Quelle opération faut-il défaire en premier ?','Remonter le programme à partir de sa dernière instruction.',f'La dernière instruction est « ajouter {b} ». Son opération inverse est « soustraire {b} ».',f'Soustraire {b}.'),
   q('Quel nombre avait-on avant cette addition ?','Retirer la quantité ajoutée.',eq(rf'{y}-{b}={x*a}'),eq(str(x*a))+'.'),
   q('Retrouver le nombre initial.','Défaire la multiplication par une division.',eq(rf'{x*a}\div{a}={x}'),eq(str(x))+'.'),
   q('Vérifier en exécutant le programme dans le bon sens.','Substituer le nombre trouvé au départ.',eq(rf'{x}\times{a}+{b}={y}'),f'Le nombre {x} convient.')],
   'Pour remonter un programme, on inverse les opérations ET leur ordre.')
 if j==3:
  starts=[0,1,2,10+l];results=[(x+b)*a for x in starts]
  return pack('Compléter un tableau de programme',f'Programme : ajouter {b}, puis multiplier le résultat par {a}. On l’exécute avec les départs '+', '.join(map(str,starts))+'.',[
   *[q(f'Calculer le résultat pour le départ {x}.','Appliquer les deux étapes dans l’ordre.',eq(rf'({x}+{b})\times{a}={y}'),eq(str(y))+'.') for x,y in zip(starts[:3],results[:3])],
   q(f'Prévoir le résultat pour {starts[-1]}, puis contrôler avec le programme.','Une unité supplémentaire au départ ajoute le multiplicateur au résultat.',eq(rf'({starts[-1]}+{b})\times{a}={results[-1]}'),eq(str(results[-1]))+'.'),
   q('Le résultat double-t-il toujours quand le nombre de départ double ?','Tester les départs 1 et 2.',f'Pour 1 : {results[1]}. Pour 2 : {results[2]}. Or '+eq(rf'2\times{results[1]}={2*results[1]}')+f', différent de {results[2]}.',f'Non ; la quantité ajoutée au départ empêche cette règle générale.')],
   'Un tableau permet d’explorer une règle, puis d’expliquer une régularité.')
 if j==4:
  x=6+l;wrong=x*a+b;right=(x+b)*a
  return pack('Trouver l’étape oubliée',f'Programme : ajouter {b}, puis multiplier par {a}. Pour le départ {x}, un élève calcule {x} fois {a}, puis ajoute {b}.',[
   q('Quel résultat l’élève obtient-il ?','Exécuter exactement son calcul.',eq(rf'{x}\times{a}+{b}={wrong}'),eq(str(wrong))+'.'),
   q('Pourquoi son calcul ne suit-il pas le programme ?','Comparer l’ordre des opérations.',f'Le programme commence par une addition ; l’élève commence par une multiplication.',f'Il a interverti les deux instructions.'),
   q('Corriger le calcul.','Revenir à l’ordre annoncé.',eq(rf'({x}+{b})\times{a}={right}'),eq(str(right))+'.'),
   q('Calculer l’écart entre les deux résultats et expliquer son origine.','Comparer le traitement de la quantité ajoutée.',eq(rf'{right}-{wrong}={right-wrong}')+f' : dans le bon programme, les {b} unités ajoutées sont aussi multipliées par {a}.',eq(str(right-wrong))+'.')],
   'Un résultat numérique ne suffit pas : la suite des opérations doit traduire toutes les consignes.')
 if j==5:
  x=8+2*l;mid=x*a;final=mid+b
  return pack('Produire un programme à partir d’une histoire',f'Une activité coûte {a} € par séance et {b} € d’inscription, payés une seule fois. On suit {x} séances.',[
   q('Calculer le prix des séances seules.','Multiplier le prix unitaire par le nombre de séances.',eq(rf'{a}\times{x}={mid}'),f'{mid} €.'),
   q('Calculer le prix total.','Ajouter les frais fixes une seule fois.',eq(rf'{mid}+{b}={final}'),f'{final} €.'),
   q('Écrire le programme qui calcule le prix à partir du nombre de séances.','Repérer ce qui varie et ce qui reste fixe.',f'La quantité variable est le nombre de séances. Le tarif par séance multiplie cette quantité ; l’inscription se rajoute ensuite.',f'Multiplier le nombre de séances par {a}, puis ajouter {b}.'),
   q(f'Un élève paie {final+a} €. Combien de séances a-t-il suivies ?','Retirer les frais fixes puis diviser par le tarif.',eq(rf'({final+a}-{b})\div{a}={x+1}'),f'{x+1} séances.')],
   'Le programme doit traduire le contexte : frais fixes et prix par unité ne jouent pas le même rôle.')
 x=3+l
 return pack('Comparer un programme à une prédiction',f'Programme : multiplier par {a}, ajouter {a*b}, puis diviser le résultat par {a}.',[
  q(f'Exécuter le programme avec le départ {x}.','Noter chaque résultat intermédiaire.',eq(rf'{x}\times{a}={x*a}')+' ; '+eq(rf'{x*a}+{a*b}={a*(x+b)}')+' ; '+eq(rf'{a*(x+b)}\div{a}={x+b}'),eq(str(x+b))+'.'),
  q(f'Exécuter avec le départ {x+1}.','Appliquer les mêmes instructions.',eq(rf'(({x+1}\times{a})+{a*b})\div{a}={x+1+b}'),eq(str(x+1+b))+'.'),
  q('Proposer un programme plus court donnant le même résultat pour ces départs.','Observer la quantité ajoutée à chaque nombre de départ.',f'Le résultat dépasse chaque nombre choisi de {b}.',f'Ajouter {b} au nombre de départ.'),
  q('Expliquer pourquoi le programme court fonctionne pour tout nombre de départ positif.','Partager la somme en deux parts lors de la division.',f'La multiplication par {a}, suivie de la division par {a}, redonne le nombre initial. La quantité {a*b}, divisée par {a}, fournit {b}.',f'On retrouve toujours le nombre de départ augmenté de {b}.')],
  'Tester plusieurs cas suggère une règle ; expliquer le fonctionnement permet de la justifier.')

def inconnues(j,l):
 if j==0:
  k=3+l;bonus=4+2*l;x=5+l;total=k*x+bonus
  return pack('Des boîtes identiques et des objets isolés',f'On compte {total} crayons : {k} boîtes identiques et {bonus} crayons isolés. Chaque boîte contient le même nombre de crayons.',[
   q('Représenter la situation par une addition à trous.','Un même symbole représente le contenu de chaque boîte.',f'On additionne {k} contenus identiques puis les {bonus} crayons isolés.',eq(rf'{k}\times\square+{bonus}={total}')+'.'),
   q('Combien de crayons sont dans les boîtes ?','Retirer les crayons isolés.',eq(rf'{total}-{bonus}={k*x}'),f'{k*x} crayons.'),
   q('Combien y a-t-il de crayons dans une boîte ?','Partager en autant de parts égales que de boîtes.',eq(rf'{k*x}\div{k}={x}'),f'{x} crayons.'),
   q('Vérifier toutes les informations.','Reconstituer le total avec les boîtes et les crayons isolés.',eq(rf'{k}\times{x}+{bonus}={total}'),f'Chaque boîte contient {x} crayons, ce qui redonne le total.')],
   'Le même symbole garde la même valeur à chaque apparition.')
 if j==1:
  k=2+l;small=12+3*l;total=small*(k+1)
  return pack('Comparer deux collections par un schéma en barres',f'Mia possède une collection. Léo possède {k} fois autant d’objets que Mia. Ensemble, ils en ont {total}.',[
   q('Combien de parts égales représente le total ?','Prendre la collection de Mia comme une part.',f'Mia représente une part et Léo {k} parts identiques. [IMAGE_1]',f'{k+1} parts égales.'),
   q('Combien d’objets possède Mia ?','Diviser le total par le nombre de parts.',eq(rf'{total}\div{k+1}={small}'),f'{small} objets.'),
   q('Combien d’objets possède Léo ?','Prendre le nombre de parts annoncé.',eq(rf'{k}\times{small}={k*small}'),f'{k*small} objets.'),
   q('Vérifier la somme et le rapport.','Contrôler les deux conditions du problème.',eq(rf'{small}+{k*small}={total}')+' et '+eq(rf'{k*small}\div{small}={k}'),f'La somme vaut {total} et Léo a bien {k} fois autant d’objets.')],
   'Un total partagé selon une relation multiplicative se représente avec des parts égales.')
 if j==2:
  total=[50,78,104][l];gap=[14,18,26][l];small=(total-gap)//2;big=small+gap
  return pack('Deux quantités dont on connaît la somme et l’écart',f'Deux élèves ont ensemble {total} billes. La plus grande collection contient {gap} billes de plus que la petite.',[
   q('Que reste-t-il si l’on retire l’écart du total ?','Retirer ce qui dépasse de la grande collection.',eq(rf'{total}-{gap}={total-gap}')+' : il reste deux collections de la taille de la petite.',f'{total-gap} billes, réparties en deux parts égales.'),
   q('Trouver la petite collection.','Partager le reste en deux.',eq(rf'{total-gap}\div2={small}'),f'{small} billes.'),
   q('Trouver la grande collection.','Ajouter l’écart à la petite.',eq(rf'{small}+{gap}={big}'),f'{big} billes.'),
   q('Vérifier la somme et la différence.','Les deux conditions doivent être vraies.',eq(rf'{small}+{big}={total}')+' et '+eq(rf'{big}-{small}={gap}'),f'Somme {total} ; différence {gap}.')],
   'Retirer l’écart transforme le problème en partage de deux quantités égales.')
 if j==3:
  k=2+l;extra=5+l;x=7+l;right=k*x+extra
  return pack('Une balance en équilibre',f'Sur un plateau se trouvent {k} boîtes identiques et {extra} masses de 1 g. L’autre plateau porte une masse de {right} g. La balance est en équilibre.',[
   q('Quelle masse ont ensemble les boîtes ?','Enlever la même masse des deux plateaux conserve l’équilibre.',eq(rf'{right}-{extra}={k*x}'),f'{k*x} g.'),
   q('Quelle est la masse d’une boîte ?','Partager en parts identiques.',eq(rf'{k*x}\div{k}={x}'),f'{x} g.'),
   q('Vérifier l’équilibre avec la masse trouvée.','Additionner la masse des boîtes et des masses isolées.',eq(rf'{k}\times{x}+{extra}={right}'),f'Chaque plateau pèse {right} g.'),
   q('Pourquoi ne peut-on pas enlever des masses sur un seul plateau en conservant l’équilibre ?','L’égalité exige une même modification des deux côtés.',f'Enlever une masse à un seul côté rend ce côté plus léger. Il faut retirer des masses égales des deux côtés.',f'Une même opération sur les deux quantités conserve l’égalité.')],
   'La balance illustre une égalité : les deux plateaux représentent la même quantité.')
 if j==4:
  n=10+5*l;target=1+3*n
  return pack('Des carrés qui partagent un côté',r'On aligne des carrés avec des allumettes. Un carré utilise 4 allumettes. Chaque carré supplémentaire partage un côté avec le précédent et nécessite 3 nouvelles allumettes. [IMAGE_2]',[
   q('Combien d’allumettes faut-il pour 2 carrés puis pour 3 ?','Ajouter trois allumettes à chaque nouveau carré.',r'$4+3=7$ puis $7+3=10$.',r'7 puis 10 allumettes.'),
   q(f'Combien faut-il d’allumettes pour {n} carrés ?','Compter le premier carré et les ajouts suivants.',eq(rf'4+({n}-1)\times3={target}'),f'{target} allumettes.'),
   q(f'On dispose de {target+6} allumettes. Combien de carrés peut-on aligner sans reste ?','Retirer le côté initial puis partager en groupes de trois.',eq(rf'({target+6}-1)\div3={n+2}'),f'{n+2} carrés.'),
   q('Expliquer la règle avec des mots, sans devoir dessiner tous les carrés.','Repérer la partie fixe et la partie répétée.',r'Il y a un côté vertical initial, puis trois allumettes par carré : un côté en haut, un en bas et un nouveau côté vertical.',r'Nombre d’allumettes = 1 + 3 fois le nombre de carrés.')],
   'Un motif s’explique par sa structure ; on ne se contente pas de prolonger une liste.')
 if j==5:
  first=4+l;step=2+l;rank=12+3*l;v=first+(rank-1)*step
  return pack('Une frise avec une partie fixe',f'Une frise utilise {first} perles au rang 1. À chaque nouveau rang, on ajoute {step} perles.',[
   q('Donner les nombres de perles aux rangs 2 et 3.','Ajouter le même nombre de perles à chaque passage.',eq(rf'{first}+{step}={first+step}')+' puis '+eq(rf'{first+step}+{step}={first+2*step}'),f'{first+step} puis {first+2*step} perles.'),
   q(f'Combien de passages effectue-t-on du rang 1 au rang {rank} ?','Le rang 1 est déjà construit.',f'Pour aller de 1 à {rank}, on effectue {rank-1} changements de rang.',f'{rank-1} passages.'),
   q(f'Calculer le nombre de perles au rang {rank}.','Ajouter toutes les augmentations à la quantité initiale.',eq(rf'{first}+({rank}-1)\times{step}={v}'),f'{v} perles.'),
   q(f'Le nombre {v+1} peut-il être obtenu dans cette frise ?','Comparer à un rang connu et à la taille de chaque ajout.',f'Le rang {rank} utilise {v} perles et le suivant {v+step}. Le nombre {v+1} est strictement entre eux.',f'Non : les quantités progressent par ajouts de {step}, pas d’une perle.')],
   'Le nombre d’augmentations pour atteindre le rang demandé est un de moins que ce rang.')
 x=4+l;k=3+l;b=8+2*l;total=k*x+b
 return pack('Construire puis vérifier une histoire à trous',f'On veut donner du sens à l’égalité '+eq(rf'{k}\times\square+{b}={total}')+'.',[
  q('Proposer une histoire avec des sachets identiques et des objets isolés.','Associer chaque terme à une quantité concrète.',f'Les {k} sachets ont un même contenu inconnu. On ajoute {b} objets isolés pour atteindre le total.',f'{k} sachets identiques et {b} objets isolés contiennent au total {total} objets.'),
  q('Trouver le nombre manquant.','Retirer les objets isolés puis partager.',eq(rf'({total}-{b})\div{k}={x}'),eq(str(x))+'.'),
  q(f'Un élève propose {x+1}. Pourquoi ne convient-il pas ?','Tester le nombre dans l’égalité initiale.',eq(rf'{k}\times{x+1}+{b}={total+k}')+f', différent de {total}.',f'Il obtient {total+k} au lieu de {total}.'),
  q('De combien le total augmente-t-il si chaque sachet contient un objet supplémentaire ?','Chaque sachet reçoit un objet de plus.',f'Il y a {k} sachets. Un objet ajouté dans chacun fournit {k} objets supplémentaires.',f'Le total augmente de {k} objets.')],
  'Inventer un problème puis contrôler une réponse oblige à donner un sens à chaque terme.')

FUNCTIONS={129:numeration,130:reperage,131:calcul,133:division,150:programmes,151:inconnues}
def main():
 for code,fn in FUNCTIONS.items():
  folder=next(ROOT.glob(str(code)+'_*'));meta=json.loads((folder/'source_en_ligne/meta.json').read_text(encoding='utf-8'));oldids=[e['id'] for e in meta['exercices']]
  data=[];blocks=[]
  for l in range(3):
   for j in range(7):
    slot=l*7+j;eid=oldids[slot] if oldids else f'nouveau-{slot+1}'
    e=fn(j,l);e.update(id=eid,famille=j+1,niveau=l+1)
    label=['Découverte','Entraînement','Problème'][l];difficulty=['easy','medium','hard'][l]
    en=MARK+'\n'+e['intro'].replace(' [IMAGE_','\n\n[IMAGE_')+'\n\n'+'\n'.join(f'{i}. '+q['question'] for i,q in enumerate(e['questions'],1))
    et=MARK+'\n'
    for i,qq in enumerate(e['questions'],1):
     et+=f'\n## Question {i} : '+qq['question']+'\n\n::: methode\n'+qq['methode']+'\n:::\n\n::: etape Raisonnement et calcul\n'+qq['etape'].replace(' [IMAGE_','\n\n[IMAGE_')+'\n:::\n\n::: resultat\n'+qq['resultat']+'\n:::\n'
    et+='\n::: retenir\n'+e['retenir']+'\n:::\n'
    so=MARK+'\n'+'\n'.join(f'{i}. '+q['resultat'] for i,q in enumerate(e['questions'],1))
    title=f'{label} - {e["titre"]} - Parcours {l+1}'
    blocks.append(f'=== {title}\nId: {eid}\nDifficulté: {difficulty}\n\nÉnoncé:\n{en}\n\nÉtapes:\n{et}\nSolution:\n{so}')
    e['titre_final']=title;data.append(e)
  (folder/'exercices.txt').write_text('\n\n===\n\n'.join(blocks)+'\n',encoding='utf-8')
  (folder/'revision_pedagogique_6e.json').write_text(json.dumps({'notion':code,'exercices':data,'tous_remplaces':bool(oldids),'date':'2026-10-30'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print(code,len(data),'exercices',sum(len(e['questions']) for e in data),'questions',flush=True)
if __name__=='__main__':main()
