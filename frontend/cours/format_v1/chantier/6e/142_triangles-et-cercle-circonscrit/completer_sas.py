# -*- coding: utf-8 -*-
"""Une vraie construction avec deux côtés et l'angle compris (ID conservé)."""
from pathlib import Path
import re,json,runpy,math
D=Path(__file__).resolve().parent
p=D/'exercices.txt';t=p.read_text(encoding='utf-8')
rows=[
('Comment commencer la construction ?','Construire l’angle compris entre les deux côtés connus.',
 ('Tracer la base','Tracer le segment $[AB]$ de longueur 6 cm.'),
 ('Fixer la direction de $C$',r'Placer le centre du rapporteur en $A$, le zéro sur $[AB)$, puis repérer $60^\circ$ au-dessus de la base. Tracer la demi-droite correspondante.'),
 r'La demi-droite issue de $A$ forme $60^\circ$ avec $[AB)$.'),
('Comment placer le point $C$ puis terminer ?',
 'Reporter la seconde longueur sur la direction construite.',
 ('Régler le compas','Ouvrir le compas à 4 cm à l’aide de la règle graduée.'),
 ('Reporter puis relier','Piquer en $A$ ; l’arc coupe la demi-droite en $C$. Tracer $[BC]$.'),
 r'$C$ est sur la demi-droite et $AC=4$ cm ; relier $B$ à $C$.'),
('Quels contrôles garantissent les trois données ?',
 'Mesurer exactement les éléments imposés.',
 ('Contrôler les côtés','La règle doit donner $AB=6$ cm et $AC=4$ cm.'),
 ('Contrôler l’angle',r'Replacer le rapporteur en $A$, sur $[AB)$ : la mesure de $\widehat{BAC}$ doit être $60^\circ$. Le point $C$ est au-dessus de $(AB)$.'),
 r'Vérifier $AB=6$ cm, $AC=4$ cm et $\widehat{BAC}=60^\circ$.')]
def box(k,text,title=''):return f'::: {k} {title}'.rstrip()+'\n'+text+'\n:::\n'
s='Entraînement — Construire avec deux côtés et leur angle\nId: 3505\nDifficulté: medium\nImage: triangle_sas.png\n\nÉnoncé:\n<!-- optitab:1 -->\n'
s+=r'Construire $ABC$ avec $AB=6$ cm, $AC=4$ cm et $\widehat{BAC}=60^\circ$, le point $C$ au-dessus de $(AB)$. La longueur $BC$ n’est pas imposée.'+'\n\n'
s+='\n'.join(f'{i}. {r[0]}' for i,r in enumerate(rows,1))+'\n\nÉtapes:\n<!-- optitab:1 -->\n'
for i,(q,m,e1,e2,result) in enumerate(rows,1):s+=f'\n## Question {i} : {q}\n\n'+box('methode',m)+box('etape',e1[1],e1[0])+box('etape',e2[1],e2[0])+box('resultat',result)
s+='\n### Figure de contrôle\n\n[IMAGE_1]\n\nLe dessin est réduit : les mesures de l’énoncé guident la construction sur papier.\n\n'+box('attention',r'L’angle donné est en $A$, entre les deux côtés de longueurs connues. Ne pas placer les $60^\circ$ en $B$.')
s+='\nSolution:\n<!-- optitab:1 -->\n'+'\n'.join(f'{i}. {r[-1]}' for i,r in enumerate(rows,1))
blocks=re.split(r'^===[ \t]*$',t,flags=re.M)
for i,b in enumerate(blocks):
 if re.search(r'^Id: 3505\s*$',b,re.M):blocks[i]='\n\n'+s+'\n\n'
p.write_text('===\n'.join(blocks),encoding='utf-8')
fp=D/'figures/figures.py';figs=runpy.run_path(str(fp))['FIGURES'];figs.pop('triangle_1_3',None)
figs['triangle_sas']=r'''\begin{tikzpicture}
\draw[geoReponse] (0,0)--(5,0)--(1.666667,2.886751)--cycle;
\draw[geoTrait] (.8,0) arc (0:60:.8);
\node[anchor=north east,inner sep=4pt] at (0,0) {$A$};
\node[anchor=north west,inner sep=4pt] at (5,0) {$B$};
\node[anchor=south,inner sep=4pt] at (1.666667,2.886751) {$C$};
\node[anchor=north,inner sep=4pt] at (2.5,-.35) {$AB=6$ cm ; $AC=4$ cm ; $\widehat{BAC}=60^\circ$};
\end{tikzpicture}'''
fp.write_text('# -*- coding: utf-8 -*-\nFIGURES = '+repr(figs)+'\n',encoding='utf-8')
cp=D/'figures/correspondance.json';c=json.loads(cp.read_text(encoding='utf-8'));c['exercices']['3505']['1']={'fichier':'triangle_sas.png','alt':'Triangle construit avec AB de 6 cm, AC de 4 cm et angle BAC de 60 degrés.'};cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
vp=D/'verification_math.json';v=json.loads(vp.read_text(encoding='utf-8'));v['checks']['3505']=['math.isclose(math.hypot(2,2*math.sqrt(3)),4)','math.isclose(math.degrees(math.atan2(2*math.sqrt(3),2)),60)'];vp.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
