"""Partage les contrôles éprouvés du collège, avec les chemins de chaque niveau."""
from pathlib import Path

dest=Path(__file__).resolve().parent
source=dest.parents[1]/'6e/outils'
s=(source/'valider_6e.py').read_text(encoding='utf-8')
start=s.index('FRONT =');end=s.index('CATS =')
s=s[:start]+'''from config import FRONT, ROOT, GRADE, LABEL
DIR_C = ROOT
DIR_R = FRONT / 'cours/resume' / GRADE
DIR_E = FRONT / 'exercices' / GRADE
'''+s[end:]
s=s.replace('_6e.txt','_{GRADE}.txt').replace('if "6ème" not in','if LABEL not in')
s=s.replace('DIR_E.glob("exercice_*_{GRADE}.txt")','DIR_E.glob(f"exercice_*_{GRADE}.txt")')
s=s.replace('re.match(r"exercice_(.+)_6e"','re.match(rf"exercice_(.+)_{GRADE}"')
(dest/'valider.py').write_text(s,encoding='utf-8')
s=(source/'verifier_mathjax.cjs').read_text(encoding='utf-8')
s=s.replace("const root = path.resolve(__dirname,'..');","const grade = process.env.OPTITAB_NIVEAU || 'cm2';\nconst root = path.resolve(__dirname,'../../',grade);")
s=s.replace('_6e.txt','_${grade}.txt').replace('cours/resume/6e/','cours/resume/${grade}/').replace('exercices/6e/','exercices/${grade}/')
s=s.replace("path.join(__dirname,'../verifications/mathjax.json')","path.join(root,'verifications/mathjax.json')")
(dest/'verifier_mathjax.cjs').write_text(s,encoding='utf-8')
s=(source/'verifier_rendu.cjs').read_text(encoding='utf-8')
s=s.replace("const root=path.resolve(__dirname,'..');","const grade=process.env.OPTITAB_NIVEAU||'cm2';\nconst root=path.resolve(__dirname,'../../',grade);")
s=s.replace("'cours_'+slug+'_6e.txt'","'cours_'+slug+'_'+grade+'.txt'")
s=s.replace("'exercice_'+slug+'_6e.txt'","'exercice_'+slug+'_'+grade+'.txt'")
s=s.replace("'exercices/6e'","'exercices/'+grade").replace("'exercices/6e/images'","'exercices/'+grade+'/images'")
(dest/'verifier_rendu.cjs').write_text(s,encoding='utf-8')
print('Contrôles préparés.')
