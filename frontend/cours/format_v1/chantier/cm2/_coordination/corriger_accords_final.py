"""Retouches grammaticales bornées, sans changement de nombres ni de raisonnement."""
from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
for code in (3,5,16):
 d=next(ROOT.glob(f'{code:02}_*'));backup=d/'sauvegardes/relecture_accords';backup.mkdir(parents=True,exist_ok=True)
 def correct(text):
  text=text.replace('les 1 carreaux sont reportés','le carreau est reporté')
  text=text.replace('Deux pliages successifs : 2 et 1 carreaux','Deux pliages successifs : 2 carreaux puis 1 carreau')
  for plural,singular in [('carreaux','carreau'),('objets','objet'),('parts','part')]:text=re.sub(r'(?<!\d)1 '+plural+r'\b','1 '+singular,text)
  return text
 targets=[d/'exercices.txt']
 if (d/'verification_questions.json').exists():targets.append(d/'verification_questions.json')
 for p in targets:
  text=p.read_text(encoding='utf-8');new=correct(text)
  if new!=text:
   if not (backup/p.name).exists():(backup/p.name).write_bytes(p.read_bytes())
   p.write_text(new,encoding='utf-8')
 manifest=d/'empreintes_finales.json'
 if manifest.exists():
  hashes=json.loads(manifest.read_text(encoding='utf-8'))
  for name in hashes:hashes[name]=hashlib.sha256((d/name).read_bytes()).hexdigest()
  manifest.write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
 print(code,'accords corrigés ; sauvegarde conservée')
