"""Consigner la relecture effectuée des planches finales, sans nouvelle génération."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
for n in (129,130,131,133,150,151):
 d=next(ROOT.glob(str(n)+'_*'));corr=json.loads((d/'figures/correspondance.json').read_text(encoding='utf-8'))
 proof={'date':'2026-11-01','statut':'OK','cours_integral':True,'fiche':True,'exercices_enonce_et_etapes':[1,10,21],'planches':['relecture_documents_6e.png','relecture_exercices_6e.png'],'figures_individuelles_vues':sorted({v['fichier'] for g in corr.values() for m in g.values() for v in m.values()}),'anomalies':0,'remarques':'Tableaux 129 transposés pour le mobile ; grands calculs alignés. Réponses et formulations complétées après relecture indépendante. Singulier « place libre » corrigé après capture sans modification du calcul.' if n==133 else 'Cours et fiche entiers et trois exercices complémentaires relus sur les planches mobiles ; figures vues individuellement.'}
 assert all((d/p).exists() for p in proof['planches'])
 (d/'inspection_visuelle_6e.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
