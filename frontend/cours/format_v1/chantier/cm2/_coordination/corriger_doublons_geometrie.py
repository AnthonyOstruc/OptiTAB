"""Remplace six répétitions exactes par des tâches complémentaires, IDs conservés."""
from pathlib import Path
import json,re
from rediger_exercices_root import ex,q,render
ROOT=Path(__file__).resolve().parent.parent
changes={
(13,9):ex('Des angles dans d’autres orientations','Un gabarit d’angle droit coïncide avec D. L’angle E est plus ouvert que ce gabarit, sans atteindre un angle plat. F est moins ouvert que le gabarit. Les trois angles sont dessinés dans des orientations différentes.',[
 q('Classer D et donner sa mesure.','Utiliser la superposition au gabarit d’angle droit.','Le gabarit coïncide exactement avec D, quelle que soit son orientation.','D est droit et mesure 90°.'),
 q('Classer E et F en justifiant.','Comparer chaque ouverture à celle d’un angle droit.','E dépasse l’ouverture de l’angle droit sans être plat ; F est moins ouvert que l’angle droit.','E est obtus et F est aigu.'),
 q('Si on prolonge les deux côtés de F, devient-il obtus ?','Distinguer longueur des traits et ouverture.','Prolonger les côtés ne les fait pas tourner ; leur ouverture reste la même.','Non : F reste aigu.')]),
(13,11):ex('Reproduire un angle obtus sur une nouvelle demi-droite','Un angle obtus est dessiné sur une feuille. Ailleurs, on place un point T et on trace une demi-droite d’origine T.',[
 q('Comment reproduire cet angle en T sans rapporteur ?','Fabriquer puis déplacer un gabarit de l’ouverture.','Décalquer les deux côtés de l’angle, placer le sommet du gabarit en T, faire coïncider un côté avec la demi-droite donnée, puis tracer le second côté.','Utiliser un gabarit ou un calque, en conservant l’ouverture obtuse.'),
 q('Comment contrôler la reproduction ?','Superposer les deux ouvertures.','Faire coïncider les sommets et un côté ; vérifier que le second côté coïncide aussi.','La superposition des deux côtés confirme l’égalité des angles.'),
 q('Un élève a obtenu un angle aigu. Sa reproduction peut-elle être correcte ?','Comparer les deux angles au gabarit d’angle droit.','L’angle initial est plus ouvert qu’un angle droit ; un angle aigu est moins ouvert. Ils ne peuvent donc pas se superposer.','Non : il n’a pas conservé l’ouverture de l’angle obtus.')]),
(15,9):ex('Construire deux perpendiculaires et comparer leurs directions','Sur une droite (d), placer deux points distincts P et Q.',[
 q('Construire la droite perpendiculaire à (d) passant par P.','Faire coïncider un côté de l’équerre avec (d).','Placer le sommet de l’angle droit de l’équerre en P, puis tracer la droite qui suit l’autre côté.','Une première droite perpendiculaire à (d), passant par P.'),
 q('Construire la droite perpendiculaire à (d) passant par Q.','Recommencer la construction au second point.','Déplacer l’équerre jusqu’à Q en gardant un côté sur (d), puis tracer la seconde perpendiculaire.','Une seconde droite perpendiculaire à (d), passant par Q.'),
 q('Quelle relation lie les deux nouvelles droites ?','Comparer deux droites perpendiculaires à une même droite.','Les points P et Q sont distincts sur (d). Les deux nouvelles droites sont donc distinctes et ont la même direction.','Les deux nouvelles droites sont parallèles.')]),
(15,13):ex('Ordonner un programme et déterminer un rayon','Voici trois instructions : A. Construire un rectangle ABCD avec AB = 6 cm et BC = 4 cm. B. Tracer le cercle de centre A passant par M. C. Placer le milieu M du segment [AB].',[
 q('Quelle instruction exécuter en premier ?','Repérer les objets nécessaires aux instructions suivantes.','Pour placer M, il faut déjà disposer du segment [AB]. Pour tracer le cercle, il faut déjà disposer de A et M.','L’instruction A doit être exécutée en premier.'),
 q('Donner l’ordre complet des trois instructions.','Construire chaque objet avant de l’utiliser.','Après le rectangle, placer le milieu M ; le cercle peut ensuite être tracé.','Ordre : A, puis C, puis B.'),
 q('Quel est le rayon du cercle obtenu ?','Utiliser la définition du milieu du segment.','AB mesure 6 cm. Comme M est son milieu, $AM=6\\div2=3$ cm. Le cercle a pour centre A et passe par M.','Le rayon est 3 cm.')]),
(16,13):ex('Corriger un symétrique par rapport à un axe horizontal','Un axe est horizontal. B est à 1 carreau au-dessus. Zoé place B’ à 1 carreau en dessous, mais une colonne à droite de B.',[
 q('Zoé a-t-elle placé le bon symétrique ?','Contrôler à la fois la distance à l’axe et la direction.','Les distances à l’axe sont égales, mais B et B’ ne sont pas sur la même colonne.','Non : la distance correcte ne suffit pas.'),
 q('Comment corriger la position de B’ ?','Rester sur la perpendiculaire à l’axe passant par B.','Déplacer B’ d’une colonne vers la gauche, sans changer sa hauteur. Il se trouve alors 1 carreau sous l’axe, sur la colonne de B.','Placer B’ sur la même colonne que B, 1 carreau sous l’axe.'),
 q('Quels contrôles peut-on maintenant effectuer sur le segment BB’ ?','Vérifier le pliage et le milieu.','Le segment BB’ est vertical et l’axe est horizontal. Le point où ils se coupent est à 1 carreau de chaque extrémité.','BB’ est perpendiculaire à l’axe et l’axe le coupe en son milieu.')]),
(17,11):ex('Lire les arêtes cachées d’un prisme','On représente un prisme droit à bases triangulaires. Il possède neuf arêtes au total, dont trois sont cachées dans le dessin. La figure de gauche présente cette famille de solides.\n\n[IMAGE_1]',[
 q('Comment distinguer les arêtes cachées sur le dessin ?','Utiliser la convention de la perspective.','Les arêtes cachées sont dessinées en pointillés, les arêtes visibles en traits continus.','Les trois arêtes cachées sont en pointillés.'),
 q('Combien d’arêtes restent visibles ?','Retirer les arêtes cachées du nombre total d’arêtes.','$9-3=6$.','Six arêtes sont visibles.'),
 q('Une face latérale inclinée dans le dessin cesse-t-elle d’être rectangulaire ?','Distinguer le solide réel et sa représentation.','Les faces latérales d’un prisme droit sont des rectangles. La perspective peut les faire apparaître inclinées sur la feuille.','Non : les trois faces latérales réelles restent rectangulaires.')])}
for code in sorted({c for c,_ in changes}):
 d=next(ROOT.glob(f'{code:02}_*'));p=d/'exercices.txt';blocks=[b.strip() for b in re.split(r'^===[ \t]*$',p.read_text(encoding='utf-8'),flags=re.M) if b.strip()]
 backup=d/'sauvegardes/relecture_doublons';backup.mkdir(parents=True,exist_ok=True)
 if not (backup/'exercices.txt').exists():(backup/'exercices.txt').write_bytes(p.read_bytes())
 for (c,ident),item in changes.items():
  if c!=code:continue
  assert f'Id: nouveau-{ident}\n' in blocks[ident-1]
  blocks[ident-1]=render(item,ident,1).strip()
 p.write_text('\n\n===\n\n'.join(blocks)+'\n\n===\n',encoding='utf-8')
 corrfile=d/'figures/correspondance.json';corr=json.loads(corrfile.read_text(encoding='utf-8'))
 if code==13:corr['exercices'].pop('nouveau-9',None)
 if code==17:corr['exercices']['nouveau-11']={'1':{'fichier':'familles.png','alt':'Prisme droit à base triangulaire à gauche et pyramide à droite ; arêtes cachées en pointillés.'}}
 corrfile.write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,'doublons remplacés ; identifiants conservés')
