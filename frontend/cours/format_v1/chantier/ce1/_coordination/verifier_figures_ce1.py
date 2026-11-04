from pathlib import Path
import sys,json,runpy,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;sys.path.insert(0,str(ROOT.parents[1]/'outils'))
import figures_livre as official
rows=[]
for d in sorted(ROOT.glob('[0-9][0-9]_*')):
 ns=runpy.run_path(str(d/'figures/figures.py'))
 for name,code in ns['FIGURES'].items():
  p=d/'figures/images'/f'{name}.png';build=d/'figures/build';expected=official.PREAMBULE+ns.get('PREAMBULE_EXTRA','')+'\n'+chr(92)+'begin{document}\n'+official.graduations_x(code,name,ns.get('XLAB'))+'\n'+chr(92)+'end{document}\n'
  # Certaines premières compilations normalisent les lignes vides du corps TikZ.
  texpath=build/f'{name}.tex';actual=texpath.read_text(encoding='utf-8') if texpath.exists() else ''
  if not p.exists() or [x for x in actual.splitlines() if x.strip()]!=[x for x in expected.splitlines() if x.strip()]:
   rows.append({'chapitre':int(d.name[:2]),'figure':p.name,'ok':False,'erreurs':['Figure absente ou pas recompilée depuis la dernière modification TikZ.'],'avertissements':[],'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None})
   continue
  w,h=official.taille_png(p);errors,warnings=official.chevauchements(p,build/f'{name}__sans_texte.png')
  assert w<=official.LARGEUR_MAX_PX,(d.name,name,w)
  rows.append({'chapitre':int(d.name[:2]),'figure':p.name,'ok':not errors,'erreurs':errors,'avertissements':warnings,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
report={'statut':'OK' if all(x['ok'] for x in rows) else 'a_corriger','figures':len(rows),'anomalies':[x for x in rows if not x['ok']],'controles':rows}
(HERE/'controle_figures_ce1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='controles'},ensure_ascii=False));assert report['statut']=='OK'
