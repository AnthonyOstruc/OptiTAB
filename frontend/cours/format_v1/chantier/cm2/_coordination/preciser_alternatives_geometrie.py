"""Textes alternatifs décrivant réellement les figures, pour tous leurs emplacements."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
ALTS={
13:{'angle':'Angle droit ABC de sommet B, avec ses deux côtés BA et BC.','types':'Trois angles : A aigu, B droit et C obtus, dessinés avec des orientations distinctes.','somme':'Un angle droit de 90 degrés et un angle de 45 degrés juxtaposés, formant 135 degrés.','pliage':'Angle droit partagé par un pli diagonal en deux angles égaux de 45 degrés.'},
14:{'polygones':'Triangle, quadrilatère, pentagone et hexagone, avec trois, quatre, cinq et six côtés.','triangles':'Triangle rectangle, triangle isocèle avec deux côtés codés égaux et triangle équilatéral avec trois côtés codés égaux.','quadrilateres':'Rectangle, losange et carré, présentés dans des orientations différentes.','trapeze':'Trapèze rectangle ABCD : bases AB et DC parallèles, angles droits en A et en D.'},
15:{'droites':'Deux droites parallèles d et e coupées par une droite f perpendiculaire, avec un angle droit codé.','cercle':'Disque de centre O, diamètre AB et rayon vertical ; l’intérieur et le bord sont distingués.','rectangle':'Rectangle ABCD, de longueur AB égale à 5 cm et de largeur BC égale à 3 cm, avec quatre angles droits codés.','compas':'Construction d’un triangle équilatéral ABC avec deux arcs de compas de même rayon se coupant en C.'},
16:{'axes':'Les quatre axes de symétrie d’un carré : deux diagonales et deux droites joignant les milieux des côtés opposés.','vertical':'Sur un quadrillage, une figure bleue et son image verte de part et d’autre d’un axe vertical orange.','horizontal':'Sur un quadrillage, une figure bleue au-dessus d’un axe horizontal et son image verte en dessous.','diagonal':'Sur un quadrillage, deux figures symétriques par rapport à une diagonale montante orange.','vertical_point':'A et son symétrique A prime sont sur la même ligne, à deux carreaux de chaque côté de l’axe vertical.','horizontal_point':'B et son symétrique B prime sont sur la même colonne, à un carreau de chaque côté de l’axe horizontal.','diagonal_point':'Depuis O sur l’axe diagonal, A se situe trois carreaux à droite et un en haut ; son image est un à droite et trois en haut.'},
17:{'pave':'Pavé droit en perspective, dont les trois arêtes cachées sont dessinées en pointillés.','cube':'Cube en perspective : faces avant, droite et dessus visibles ; trois arêtes cachées en pointillés.','familles':'Prisme droit à bases triangulaires à gauche et pyramide à base quadrilatérale à droite, avec arêtes cachées en pointillés.','patron_cube':'Patron de cube : carrés 1 à 4 en ligne ; carré 5 au-dessus du 2, carré 6 au-dessous.','patron_pave':'Patron de pavé de dimensions 4 cm, 3 cm et 2 cm, avec deux rectangles de chaque sorte : 4 sur 3, 4 sur 2 et 3 sur 2.'}}
for code,mapping in ALTS.items():
 d=next(ROOT.glob(f'{code:02}_*'));p=d/'figures/correspondance.json';corr=json.loads(p.read_text(encoding='utf-8'))
 for owners in corr.values():
  for positions in owners.values():
   for im in positions.values():im['alt']=mapping[Path(im['fichier']).stem]
 p.write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,'alternatives précises enregistrées')
