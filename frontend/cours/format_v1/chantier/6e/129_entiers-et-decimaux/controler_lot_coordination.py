"""Validation commune et aperçu fidèle, y compris les nouveaux documents 6e.

Les outils et exports communs restent inchangés ; seul le manifeste en mémoire
est enrichi pour les documents qui n'ont pas encore d'identifiant en base.
"""
from pathlib import Path
import sys,json,subprocess,contextlib,os,shutil,re
sys.stdout.reconfigure(encoding='utf-8')
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;OUTILS=ROOT.parents[1]/'outils'
def charger_meta(dossier):
 meta=json.loads((dossier/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
 if (dossier/'cours_nouveau.txt').exists():meta['cours'].append({'id':'nouveau','titre':meta['titre'],'images':[]})
 if (dossier/'fiche_nouvelle.txt').exists():meta['fiches'].append({'id':'nouvelle','titre':meta['titre'],'images':[]})
 if (dossier/'exercices.txt').exists():
  for b in re.split(r'^===[ \t]*$',(dossier/'exercices.txt').read_text(encoding='utf-8'),flags=re.M):
   ident=re.search(r'^Id:\s*(nouveau-\d+)\s*$',b,re.M)
   if ident:meta['exercices'].append({'id':ident[1],'titre':b.strip().splitlines()[0].replace('=== ','',1),'images':[]})
 return meta

preview=(OUTILS/'apercu_notion.mjs').read_text(encoding='utf-8')
preview=preview.replace('const here = path.dirname(fileURLToPath(import.meta.url))','const here = '+json.dumps(str(OUTILS)))
needle="const meta = JSON.parse(read(path.join(dir, 'source_en_ligne', 'meta.json')))"
assert needle in preview
preview=preview.replace(needle,needle+"\nif (fs.existsSync(path.join(dir,'cours_nouveau.txt'))) meta.cours.push({id:'nouveau',titre:meta.titre,images:[]});\nif (fs.existsSync(path.join(dir,'fiche_nouvelle.txt'))) meta.fiches.push({id:'nouvelle',titre:meta.titre,images:[]});")
(ICI/'apercu_6e_local.mjs').write_text(preview,encoding='utf-8')
browser=(OUTILS/'controle_apercu.mjs').read_text(encoding='utf-8')
browser=browser.replace('const here = path.dirname(fileURLToPath(import.meta.url))','const here = '+json.dumps(str(OUTILS)))
browser=browser.replace("querySelectorAll('mjx-merror')","querySelectorAll('mjx-merror, .mjx-merror, [data-mjx-error]')")
browser=browser.replace('(i === 1 || (i === 0 && k < 2))','([0,7,14].includes(k) && i < 2)')
browser=browser.replace('await browser.close()',"await Promise.race([browser.close(),new Promise(r=>setTimeout(r,2000))])")
(ICI/'controle_navigateur_6e.mjs').write_text(browser,encoding='utf-8')
source=(OUTILS/'verifier_notion.py').read_text(encoding='utf-8')
source=source.replace('meta = json.loads((dossier / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))','meta = charger_meta(dossier)')
namespace={'__file__':str(OUTILS/'verifier_notion.py'),'__name__':'controle_notion_locale_6e','charger_meta':charger_meta}
sys.path.insert(0,str(OUTILS));exec(compile(source,str(OUTILS/'verifier_notion.py'),'exec'),namespace)
run=subprocess.run
def local_run(args,*a,**kw):
 if isinstance(args,list) and len(args)>1:
  if Path(args[1]).name=='apercu_notion.mjs':args=[args[0],str(ICI/'apercu_6e_local.mjs'),*args[2:]]
  elif Path(args[1]).name=='controle_apercu.mjs':
   d=Path(args[2]).parent
   args=[args[0],str(ICI/'controle_navigateur_6e.mjs'),args[2],str(d/'captures_6e')]
   result=run(args,*a,**kw)
   (d/'controle_navigateur_6e.log').write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
   return result
 return run(args,*a,**kw)
namespace['subprocess'].run=local_run
for code in map(int,[x for x in sys.argv[1:] if x.isdigit()] or (129,130,131,133,150,151)):
 d=next(ROOT.glob(str(code)+'_*'))
 # Chaque notion garde un script mathématique autonome.
 target=d/'verif_math_6e.py'
 shutil.copyfile(ICI/'verifier_maths_coordination.py',target)
 math=run([sys.executable,str(target)],capture_output=True,text=True,encoding='utf-8',stdin=subprocess.DEVNULL)
 (d/'verification_math_6e.log').write_text(math.stdout+math.stderr,encoding='utf-8')
 assert math.returncode==0,math.stdout+math.stderr
 with (d/'validation_6e.log').open('w',encoding='utf-8') as log,contextlib.redirect_stdout(log):
  problems=namespace['verifier'](d,navigateur='--sans-navigateur' not in sys.argv)
 report={'notion':code,'date':'2026-10-30','problemes':problems,'statut':'OK' if not problems else 'a_corriger','nouveaux_documents_valides_en_memoire':not bool(json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'))['fiches'])}
 (d/'validation_6e.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,'OK' if not problems else problems,flush=True)
 if problems:raise SystemExit(2)
