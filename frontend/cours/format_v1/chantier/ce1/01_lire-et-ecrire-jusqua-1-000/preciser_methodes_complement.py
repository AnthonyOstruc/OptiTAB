from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent.parent
def changer(code,methods):
 p=next(ROOT.glob(f'{code:02}_*'))/'exercices.txt'
 blocks=re.split(r'^===\s*$',p.read_text(encoding='utf-8'),flags=re.M)[1:]
 for i,items in methods.items():
  b=blocks[i-1];matches=list(re.finditer(r'::: methode\n(.*?)\n:::',b,re.S))
  assert len(matches)==5
  for j,new in sorted(items.items(),reverse=True):
   m=matches[j-1];b=b[:m.start(1)]+new+b[m.end(1):]
  blocks[i-1]=b
 p.write_text('===\n'+('\n===\n'.join(b.strip()+'\n' for b in blocks)),encoding='utf-8')

actions14={
1:('Compare la partie bleue cherchée à l’ensemble des 360 perles.','Retire les 145 perles vertes des 360 perles du tout.','Réunis les perles bleues trouvées et les 145 perles vertes pour retrouver les 360 perles.'),
2:('Le total doit contenir tous les cubes des deux bacs.','Réunis les 238 cubes du premier bac et les 174 du second.','Retire les 174 cubes du second bac du total pour retrouver les 238 cubes du premier.'),
3:('Les places libres sont une partie des 500 places de l’album.','Retire les 367 places occupées des 500 places de l’album.','Réunis les places libres et les 367 places occupées pour retrouver les 500 places.'),
4:('Imagine les images avant le don : elles comprennent aussi les 57 images données.','Remets les 57 images données avec les 186 images restantes.','Rejoue le don de 57 images à partir du départ retrouvé : il doit rester 186 images.'),
5:('Imagine les cartes avant le cadeau : les 48 nouvelles cartes ne sont pas encore là.','Retire les 48 cartes reçues des 302 cartes présentes maintenant.','Ajoute les 48 cartes reçues au départ retrouvé pour obtenir les 302 cartes actuelles.'),
6:('Les fruits cueillis sont une partie des 125 fruits présents au départ.','Retire les 89 fruits restants des 125 fruits du départ.','Réunis les fruits cueillis et les 89 fruits restants pour retrouver les 125 fruits.'),
8:('Imagine la réserve avant la perte : elle comprend les 126 feuilles perdues et les 384 restantes.','Remets les 126 feuilles perdues avec les 384 feuilles restantes.','Retire les 126 feuilles perdues du départ retrouvé pour obtenir les 384 feuilles restantes.'),
}
changer(14,{i:{1:a,2:b,4:c} for i,(a,b,c) in actions14.items()})
changer(15,{
 1:{2:'Ajoute aux 125 cartes de Lina les 28 cartes que Noé a de plus.'},
 2:{2:'Retire les 196 élèves de la petite école des 238 élèves de la grande.'},
 3:{2:'Ajoute aux 175 cubes du bac bleu les 46 cubes que le bac rouge a de plus.'},
 4:{2:'Retire des 304 perles de Mila les 78 perles qu’elle a de plus que Zoé.'},
 5:{2:'Retire les 95 centimètres de la petite ficelle des 140 centimètres de la grande.'},
 6:{2:'Soustrais les deux effectifs égaux de 125 cartes pour mesurer leur différence.'},
 7:{2:'Ajoute les douze euros d’écart au prix de trente-huit euros du jeu le moins cher.'},
 8:{2:'Lina possède neuf billes de plus : retire ces neuf billes des 63 billes de Lina.'},
})
changer(19,{
3:{1:'Compare deux et cinq parts de même taille, puis quatre et trois parts de même taille.'},
4:{1:'Superpose les bandes identiques : une des trois parts est plus grande qu’une des six parts.'},
5:{1:'Pour chaque couple, compare une seule part de chaque partage : davantage de parts dans le tout donne une part plus petite.'},
7:{1:'Les dixièmes ont la même taille : compare les sept parts de Lina aux quatre parts de Noé.'},
})
p=next(ROOT.glob('19_*'))/'exercices.txt';t=p.read_text(encoding='utf-8')
t=t.replace('À numérateur égal, le plus grand dénominateur donne la plus petite fraction','Pour deux fractions de numérateur 1, le plus grand dénominateur donne la plus petite fraction')
t=t.replace('Pour un même tout et un même numérateur, davantage de parts signifie des parts plus petites.','Pour un même tout, compare une seule part de chaque partage : plus le partage contient de parts, plus chacune est petite.')
t=t.replace('Avec le même numérateur, le plus petit dénominateur donne les plus grandes parts.','Avec une seule part choisie, le plus petit dénominateur donne la plus grande part.')
t=t.replace('1 parts sur','1 part sur').replace('1 part sur 3 sont comparées','1 part sur 3 est comparée').replace('1 part sur 5 sont comparées','1 part sur 5 est comparée').replace('1 part sur 8 sont comparées','1 part sur 8 est comparée').replace('1 parts.','1 part.')
p.write_text(t,encoding='utf-8')
changer(20,{i:{2:m} for i,m in {
1:'Réunis une part et trois autres parts du partage en six.',
2:'Réunis les deux parts et les trois autres parts du partage en huit.',
3:'Pars des cinq parts prises et enlève deux parts du partage en six.',
5:'Réunis trois quarts et le dernier quart du tout.',
6:'Compte les quatre parts bleues et les trois autres parts vertes, sans compter deux fois la même part.',
7:'Le tout contient dix parts ; retire les trois parts bleues pour compter les parts rouges.',
8:'Réunis un quart et deux autres quarts ; compte les parts sans changer leur taille.',
}.items()})
p=next(ROOT.glob('31_*'))/'exercices.txt';t=p.read_text(encoding='utf-8');blocks=re.split(r'^===\s*$',t,flags=re.M)[1:]
blocks[6]=blocks[6].replace('1. Écris la question d’enquête et les trois choix possibles.','1. Prépare une nouvelle enquête sur un sujet de ton choix, avec deux à cinq réponses possibles. Écris la question et les choix.')
blocks[6]=blocks[6].replace('## Question 1 : Écris la question d’enquête et les trois choix possibles.','## Question 1 : Prépare une nouvelle enquête avec deux à cinq choix.')
blocks[6]=blocks[6].replace('Treize personnes répondent à la question','Pour les questions 2 à 5, utilise cet exemple. Treize personnes répondent à la question',1)
blocks[6]=blocks[6].replace('Une question claire doit permettre une seule réponse parmi des choix distincts.','Choisis un sujet, formule une question claire et propose deux à cinq choix distincts ; demande une seule réponse par personne.')
blocks[6]=blocks[6].replace('::: resultat\n', '::: resultat\n',1)
# Le résultat fourni est un modèle, non l’unique sujet d’enquête autorisé.
blocks[6]=blocks[6].replace('Quel fruit préfères-tu : pomme, poire ou banane ?', 'Quel fruit préfères-tu : pomme, poire ou banane ?')
p.write_text('===\n'+('\n===\n'.join(b.strip()+'\n' for b in blocks)),encoding='utf-8')
print('Méthodes et ouverture des enquêtes précisées : 14,15,19,20,31.')
