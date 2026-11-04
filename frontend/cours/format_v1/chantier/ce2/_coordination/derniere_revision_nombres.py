from commun_redaction import ROOT
import re
for code in [19]:
 d=next(ROOT.glob(f'{code:02}_*'))
 for name in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','situations_verifiees.json']:
  p=d/name;s=p.read_text(encoding='utf-8')
  for a,b in [('cat?gorie','catégorie'),('derni?res','dernières'),('?num?re','énumère'),('possibilit?s','possibilités'),('premi?re','première')]:s=s.replace(a,b)
  p.write_text(s,encoding='utf-8')
lists={3:['Je compare le nombre de chiffres, puis les chiffres de gauche à droite.','Pour ranger, je place d’abord le plus petit nombre, puis les suivants.','Sur une droite, je compte les intervalles et je trouve la valeur d’un pas.','Je vérifie les nombres placés avec les graduations voisines.'],18:['Je repère quelle quantité sert de point de départ.','Pour « de plus », je dessine le supplément puis je l’ajoute.','Pour « fois autant », je répète des groupes égaux ; pour partager, je cherche des parts égales.','Je vérifie à qui correspond chaque quantité dans l’histoire.'],19:['Je choisis un élément de la première catégorie et je le garde fixe.','Je l’associe à tous les choix de la catégorie suivante.','Je recommence pour chaque premier choix, avec un tableau ou un arbre.','Je compte les possibilités et je vérifie qu’aucune ne manque ou ne se répète.']}
for code,steps in lists.items():
 d=next(ROOT.glob(f'{code:02}_*'))
 for name in ['cours_nouveau.txt','fiche_nouvelle.txt']:
  p=d/name;s=p.read_text(encoding='utf-8');body='\n'.join(f'{i}. {x}' for i,x in enumerate(steps,1))
  s=re.sub(r'(::: methode[^\n]*\n)1\.[\s\S]*?(\n:::)',lambda m:m[1]+body+m[2],s)
  p.write_text(s,encoding='utf-8')
