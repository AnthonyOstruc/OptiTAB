"""Adaptation locale du contrôleur officiel pour les nouveaux contenus CP."""
from pathlib import Path
import json,re,sys,subprocess,contextlib,hashlib,datetime
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;OUTILS=ROOT.parents[1]/'outils'
sys.stdout.reconfigure(encoding='utf-8');sys.path.insert(0,str(OUTILS))
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def charger_meta(d):
 m=load(d/'source_en_ligne/meta.json')
 assert m['creation_cp'] and not any(m[g] for g in ('cours','fiches','exercices'))
 m['titre']=(d/'cours_nouveau.txt').read_text(encoding='utf-8').splitlines()[0].removeprefix('Titre: ').strip()
 m['cours']=[{'id':'nouveau','titre':m['titre'],'images':[]}]
 m['fiches']=[{'id':'nouvelle','titre':m['titre'],'images':[]}]
 for b in re.split(r'^===[ \t]*$',(d/'exercices.txt').read_text(encoding='utf-8'),flags=re.M):
  if not b.strip():continue
  ident=re.search(r'^Id:\s*(nouveau-\d+)\s*$',b,re.M);assert ident
  m['exercices'].append({'id':ident[1],'titre':b.strip().splitlines()[0].removeprefix('=== ').strip(),'images':[]})
 return m

if __name__=='__main__':
 preview=(OUTILS/'apercu_notion.mjs').read_text(encoding='utf-8')
 preview=preview.replace('const here = path.dirname(fileURLToPath(import.meta.url))','const here = '+json.dumps(str(OUTILS)))
 preview=preview.replace("const meta = JSON.parse(read(path.join(dir, 'source_en_ligne', 'meta.json')))","const meta = JSON.parse(read(path.join(dir, 'source_en_ligne', 'meta.json')));\nmeta.titre=read(path.join(dir,'cours_nouveau.txt')).split(/\\r?\\n/)[0].replace(/^Titre: /,'').trim();\nmeta.cours=[{id:'nouveau',titre:meta.titre,images:[]}];meta.fiches=[{id:'nouvelle',titre:meta.titre,images:[]}];")
 # Idempotent write: concurrent validators only ever use identical content.
 target=ICI/'apercu_cp.mjs'
 if not target.exists() or target.read_text(encoding='utf-8')!=preview:target.write_text(preview,encoding='utf-8')
 source=(OUTILS/'verifier_notion.py').read_text(encoding='utf-8')
 source=source.replace('meta = json.loads((dossier / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))','meta = charger_meta(dossier)')
 ns={'__file__':str(OUTILS/'verifier_notion.py'),'__name__':'validation_locale_cp','charger_meta':charger_meta}
 exec(compile(source,str(OUTILS/'verifier_notion.py'),'exec'),ns)
 run=subprocess.run
 def local_run(args,*a,**kw):
  if isinstance(args,list) and len(args)>1 and Path(args[1]).name=='apercu_notion.mjs':args=[args[0],str(ICI/'apercu_cp.mjs'),*args[2:]]
  return run(args,*a,**kw)
 ns['subprocess'].run=local_run
 codes=[int(x) for x in sys.argv[1:] if x.isdigit()];assert codes,'Indiquer les numéros des chapitres.'
 for code in codes:
  d=next(ROOT.glob(f'{code:02}_*'));meta=charger_meta(d)
  for name,expected in load(d/'sources_locales/empreintes_sources.json').items():
   assert hashlib.sha256((ICI.parents[4]/name).read_bytes()).hexdigest()==expected,(code,name,'source modifiee')
  with (d/'validation_cp.log').open('w',encoding='utf-8') as log,contextlib.redirect_stdout(log):problems=ns['verifier'](d,navigateur=False)
  report={'date':datetime.datetime.now().isoformat(timespec='seconds'),'statut':'OK' if not problems else 'a_corriger','problemes':problems,'notion':code}
  (d/'validation_cp.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  assert not problems,(code,problems)
  if '--navigateur' in sys.argv:
   result=run(['node',str(ICI/'controle_navigateur_cp.mjs'),str(d)],capture_output=True,text=True,encoding='utf-8')
   (d/'controle_navigateur_cp.log').write_text(result.stdout+'\n'+result.stderr,encoding='utf-8')
   assert result.returncode==0,(code,result.stdout[-3000:],result.stderr[-1500:])
  print(code,'OK',flush=True)
