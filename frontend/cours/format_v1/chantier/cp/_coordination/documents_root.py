from commun_redaction import ROOT
import json
def box(kind,title,text):return '::: '+kind+(' '+title if title else '')+'\n'+text+'\n:::\n'
S={
21:('La monnaie : les euros',['Je lis la valeur de chaque pièce ou billet.','Je réunis les valeurs, pas le nombre d’objets.','Pour payer, je forme le prix demandé.','Pour vérifier la monnaie, j’ajoute le prix et la somme rendue.'],'Un billet de10€ vaut plus que quatre pièces de2€. Compte leur valeur.','10pièces de1€ = 1billet de10€.\n\nPrix + monnaie rendue = somme donnée.'),
22:('Les longueurs : comparer et mesurer',['Pour comparer, j’aligne une extrémité des bandes.','Pour mesurer, je place le zéro au début du segment.','Je lis la graduation de l’autre extrémité.','Si le zéro est décalé, je compte l’écart entre les deux lectures.'],'Un dessin à l’écran change de taille avec le zoom. Lis les graduations. Pour tracer7cm, utilise ta vraie règle sur une feuille.','1m = 100cm.\n\nLe centimètre sert pour un crayon ; le mètre pour une porte.'),
23:('Les masses : comparer des objets',['Je soupèse les objets pour faire une première comparaison.','Je vérifie avec une balance bien réglée.','Le plateau le plus bas porte l’objet le plus lourd.','Si les plateaux restent au même niveau, les masses sont égales.'],'La taille ne donne pas la masse : une grosse boîte vide peut être plus légère qu’une petite boîte pleine.','Plateau plus bas : objet plus lourd.\n\nPlateaux au même niveau : masses égales, si la balance est réglée.'),
24:('Le repérage dans le temps : les heures entières',['Je repère les deux aiguilles et leur longueur.','Pour une heure entière, la grande aiguille pointe sur12.','Je lis le nombre indiqué par la petite aiguille.','Je précise le moment de la journée si c’est nécessaire.'],'Ne lis pas12heures seulement parce que la grande aiguille est sur12. L’heure se lit avec la petite aiguille.','Heure entière : grande aiguille sur12.\n\nLa petite aiguille indique l’heure. À12heures au milieu de la journée, il est midi.'),
25:('La géométrie plane : formes et alignements',['Je suis le contour pour compter les côtés.','Je compte chaque sommet une seule fois.','Je reconnais une forme même si elle est tournée.','Pour relier ou vérifier des points alignés, je place le bord de la règle sur eux.'],'Un disque est une forme plate. Une boule est un solide que l’on peut tenir et faire rouler.','Triangle : 3côtés et3sommets. Carré : 4côtés égaux et4coins droits. Rectangle : 4coins droits. Disque : une forme ronde et plate.'),
26:('La géométrie plane : construire sur quadrillage',['Je repère les sommets du modèle.','Je compte les carreaux entre les sommets.','Je place les mêmes sommets sur le quadrillage vide.','Je les relie à la règle et je compare les deux figures.'],'Compte les espaces entre les lignes : quatre carreaux relient cinq lignes. Un carreau n’est pas toujours un centimètre.','Pour ces carrés et rectangles, les côtés suivent les lignes du quadrillage.\n\nCarré : quatre côtés de même longueur.'),
27:('Les solides : reconnaître et construire',['Je manipule le solide et je le tourne.','Je repère ses faces plates, s’il en possède.','Je compte les faces une seule fois en les marquant.','Pour construire une boîte, j’assemble les faces bord contre bord.'],'Un dessin peut cacher des faces. Tourne l’objet pour les compter toutes.','Cube : 6faces carrées.\n\nPavé : 6faces rectangulaires, parfois carrées.\n\nUne boule n’a pas de face plate.'),
28:('Le repérage dans l’espace : positions et déplacements',['Je repère le départ et le sens du regard.','J’exécute une instruction à la fois.','Tourner change le regard, sur place. Avancer déplace le pion.','Je vérifie la place d’arrivée et le sens du regard.'],'La droite du pion dépend de son regard. Tourner à droite ne signifie pas avancer vers la droite du dessin.','Tourner : changer de direction sur place.\n\nAvancer : se déplacer dans le sens du regard.\n\nReculer : aller dans le sens opposé, sans se retourner.')}
for code,(title,method,warning,key) in S.items():
 d=next(ROOT.glob(f'{code:02}_*'));src=json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf-8'))
 # Les nombres et unités doivent rester distincts dans le français courant.
 import re
 clean=lambda s:re.sub(r'(?<=\d)(?=[A-Za-zÀ-ÿ€])|(?<=[A-Za-zÀ-ÿ])(?=\d)',' ',s)
 method=list(map(clean,method));warning=clean(warning);key=clean(key)
 text='Titre: '+title+'\n<!-- optitab:1 -->\n'+box('objectifs','',src['objectif'])
 text+='\n## I. J’observe et je manipule\n\n'+box('methode','Avec le matériel',src['manipulation'])+'\n[IMAGE_1]\n'
 text+='\n## II. Je comprends\n\n'+box('definition','Les repères','\n\n'.join(src['lecon']))
 text+='\n## III. Je fais pas à pas\n\n'+box('methode','', '\n'.join(f'{i}. {s}' for i,s in enumerate(method,1)))+box('exemple','',src['exemple'])
 text+='\n## IV. À toi de jouer\n\n'+box('exemple','',src['guide'])+box('resultat','Je vérifie',src['guide_reponse'])+box('attention','',warning)+box('retenir','',key)
 sheet='Titre: '+title+'\n<!-- optitab:1 -->\n'+box('retenir','',key)+'\n[IMAGE_1]\n\n## I. Ma méthode\n\n'+box('methode','','\n'.join(f'{i}. {s}' for i,s in enumerate(method[:3],1)))+'\n## II. Je vérifie\n\n'+box('exemple','',src['exemple'])+box('attention','',warning)
 if code==25:
  text=text.replace('\n## III.', '\n[IMAGE_2]\n\n## III.')
  sheet=sheet.replace('\n## II.', '\n[IMAGE_2]\n\n## II.')
 (d/'cours_nouveau.txt').write_text(text,encoding='utf-8');(d/'fiche_nouvelle.txt').write_text(sheet,encoding='utf-8')
 print(code,'cours et fiche préparés')
