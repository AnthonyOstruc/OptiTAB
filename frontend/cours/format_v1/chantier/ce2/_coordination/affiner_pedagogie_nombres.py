from commun_redaction import ROOT
import re
codes=[1,2,3,*range(15,24)]
base={1:'Repère chaque chiffre dans son rang : milliers, centaines, dizaines et unités.',2:'Utilise les échanges de dix unités d’un rang contre une unité du rang suivant.',3:'Compare à partir du rang le plus à gauche ; sur une droite, lis d’abord la valeur d’un intervalle.',15:'Repère le tout, les parties et ce qui est cherché avant de choisir l’opération.',16:'Calcule la première quantité inconnue, puis utilise-la pour répondre à la question finale.',17:'Explique ce que compte chaque groupe avant de multiplier, puis traite ce qui reste à chercher.',18:'Distingue une quantité ajoutée d’une quantité répétée plusieurs fois.',19:'Fixe un premier choix, puis associe-lui tous les choix de la catégorie suivante.',20:'Partage chaque part en un même nombre de petites parts pour représenter une quantité inchangée.',21:'Compare des parts de même taille ; si nécessaire, redécoupe une des bandes.',22:'Repère l’unité de longueur et le nombre de parts égales qui la composent.',23:'Compte les parts ajoutées ou retirées en gardant des parts de même taille.'}
def method(code,prompt):
 p=prompt.lower()
 if code==19:return 'Fixe un choix dans la première catégorie et énumère les choix restants, sans doublon ni oubli.'
 if code in (20,21,22,23) and ('vérif' in p or 'contrôl' in p):return 'Représente les parts sur des bandes identiques et vérifie la quantité obtenue.'
 if 'vérif' in p or 'contrôl' in p:return 'Reconstitue la quantité de départ avec une opération inverse ou un second calcul.'
 if 'lettres' in p and code in (1,2):return 'Lis les rangs de gauche à droite, en sautant les rangs dont le chiffre est zéro.'
 if 'numérateur' in p:return 'Lis le nombre de parts prises, écrit au-dessus de la barre de fraction.'
 if 'dénominateur' in p and ('pourquoi' not in p):return 'Repère en combien de parts égales l’unité a été partagée.'
 if ('rang' in p or 'valeur' in p or 'chiffre' in p) and code in (1,2):return 'Repère la colonne du chiffre : sa place indique combien vaut chacune de ses unités.'
 if ('dizaines entières' in p):return 'Forme le plus de groupes de dix possible, puis garde les unités restantes.'
 if ('centaines entières' in p):return 'Forme le plus de groupes de cent possible, puis garde les unités restantes.'
 if 'erreur' in p or 'corrige' in p or 'pourquoi' in p and code in (1,2):return 'Représente la quantité annoncée, puis compare-la à l’écriture proposée.'
 if code==3 and ('intervall' in p or 'gradu' in p):return 'Compte les intervalles égaux et partage l’écart entre deux nombres connus.'
 if code==3 and ('range' in p or 'ordre' in p):return 'Compare les nombres à partir de la gauche et place chaque nombre dans le bon ordre.'
 if code in (15,16,17,18) and ('opération' in p or 'pourquoi' in p):return 'Raconte ce qui se passe : réunir, retirer, comparer ou répéter une quantité.'
 if 'schéma' in p or 'dessin' in p or 'représente' in p:return 'Utilise le schéma pour relier chaque donnée à la quantité qu’elle représente.'
 if code==19 and ('combien' in p or 'nombre' in p):return 'Compte les possibilités pour chaque premier choix, sans doublon ni oubli.'
 if code in (20,21,23) and ('manque' in p or 'reste' in p):return 'Compte les parts du tout, puis retire les parts déjà prises dans la même unité de partage.'
 if code in (20,21) and ('compare' in p or 'grande' in p or 'petite' in p):return 'Prends des bandes de même longueur et compare les portions recouvertes.'
 if code==22 and ('entière' in p or 'unités' in p):return 'Compte les unités complètes, puis décris la portion d’unité restante.'
 return base[code]
warnings={1:('Ne confonds pas 6 034 et 6 304 : dans le premier, il n’y a pas de centaine isolée ; dans le second, il y en a trois.','Lis les rangs en les montrant du doigt pour distinguer 6 034 et 6 304.'),2:(None,'Forme des paquets et distingue le chiffre d’un rang du nombre total de groupes entiers.'),3:(None,'Compare de gauche à droite ; sur une droite, vérifie que les intervalles représentent toujours le même écart.'),15:(None,'Rejoue l’histoire avec de petits nombres et replace la quantité inconnue dans ton schéma.'),16:(None,'Écris ce que compte chaque résultat intermédiaire, avec son unité.'),17:('Traite les étapes dans l’ordre : un résultat intermédiaire sert à trouver la suite. Vérifie ce que compte chaque nombre.','Dessine une étape, calcule, puis raconte ce qui reste à chercher.'),18:('Représente « fois autant » avec des parts égales répétées. Pour « de plus », ajoute seulement le supplément indiqué.','Juxtapose des bandes égales pour « fois autant » et ajoute une petite extension pour « de plus ».'),19:(None,'Fixe un premier choix et essaie toutes les possibilités avant de passer au suivant.'),20:('Compare toujours des portions d’un même tout ou de touts de même taille. Les parts d’une fraction doivent être égales.','Plie et superpose deux bandes identiques avant de compléter les écritures.'),21:('Le nombre de parts ne suffit pas : il faut aussi regarder leur taille. Pour comparer, partage des bandes de même longueur de façon identique.','Utilise des bandes identiques et nomme la taille des parts avant de les compter.'),22:(None,'Reporte l’unité et ses quarts en gardant la bande unité visible.'),23:('Avant de réunir ou de retirer des fractions, représente des parts de même taille. Vérifie que tu comptes bien les mêmes parts.','Change la taille des parts par découpage, puis écris ce que montre le dessin.')}
for code in codes:
 d=next(ROOT.glob(f'{code:02}_*'));p=d/'exercices.txt';text=p.read_text(encoding='utf-8')
 def blockfix(m):
  b=m[0];en=b.split('Énoncé:')[1].split('Étapes:')[0];qs=re.findall(r'^\d+\. (.+)',en,re.M)
  for i,prompt in enumerate(qs,1):
   pattern=rf'(^## Question {i} :)[^\n]*\n\n::: methode\n[^\n]*\n:::'
   b,n=re.subn(pattern,lambda x:x[1]+' '+prompt+'\n\n::: methode\n'+method(code,prompt)+'\n:::',b,flags=re.M);assert n==1,(code,i)
  return b
 text=re.sub(r'(?:^===.*\n)(?:(?!^===).)*',blockfix,text,flags=re.M|re.S) if False else text
 # Garder les séparateurs et identifiants byte pour byte, corriger chaque bloc possédant un énoncé.
 pieces=re.split(r'(^===[ \t]*$)',text,flags=re.M)
 for i,b in enumerate(pieces):
  if 'Énoncé:' in b:pieces[i]=blockfix(re.match(r'[\s\S]*',b))
 p.write_text(''.join(pieces),encoding='utf-8')
 for i,name in enumerate(['cours_nouveau.txt','fiche_nouvelle.txt']):
  p=d/name;s=p.read_text(encoding='utf-8');warning=warnings[code][i]
  if warning:s=re.sub(r'(::: attention[^\n]*\n).*?(\n:::)',lambda m:m[1]+warning+m[2],s,flags=re.S)
  p.write_text(s,encoding='utf-8')
 print(code,'méthodes et conseils adaptés à l’élève')
