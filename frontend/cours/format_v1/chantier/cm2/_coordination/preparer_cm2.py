"""Inventaire et export local CM2, exclusivement en lecture de la base."""
from pathlib import Path
import os,sys,json,hashlib,datetime
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;REPO=ICI.parents[5];OUTILS=ROOT.parents[1]/'outils'
os.chdir(REPO/'backend');sys.path.insert(0,str(REPO/'backend'));os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
sys.stdout.reconfigure(encoding='utf-8')
import django
django.setup()
from curriculum.models import MatiereContexte,Notion,Exercice
from cours.models import Cours
from synthesis.models import SynthesisSheet
contexts=list(MatiereContexte.objects.filter(niveau__nom__icontains='CM2').select_related('niveau','niveau__pays','matiere'))
print(json.dumps([{'id':c.id,'niveau':c.niveau.nom,'pays':c.niveau.pays.nom,'matiere':c.matiere.titre} for c in contexts],ensure_ascii=False),flush=True)
if not contexts:
 from pays.models import Niveau
 print('NIVEAUX',json.dumps(list(Niveau.objects.filter(pays__nom__iexact='France').values('id','nom','ordre')),ensure_ascii=False),flush=True)
 print('CONTEXTES',json.dumps(list(MatiereContexte.objects.filter(matiere_id=1).values('id','niveau__nom','niveau__pays__nom')),ensure_ascii=False),flush=True)
if '--exporter' not in sys.argv:raise SystemExit(0)
contexts=[c for c in contexts if c.matiere_id==1 and c.niveau.pays.nom.lower()=='france'];assert len(contexts)==1
ctx=contexts[0];notions=list(Notion.objects.filter(theme__contexte=ctx).select_related('theme').order_by('id'));assert notions
source=(OUTILS/'exporter.py').read_text(encoding='utf-8').split('\nargs = sys.argv[1:]')[0]
ns={'__file__':str(OUTILS/'exporter.py'),'__name__':'export_cm2_lecture_seule'}
exec(compile(source,str(OUTILS/'exporter.py'),'exec'),ns);ns['NIVEAUX'][ctx.id]='cm2'
sys.path.insert(0,str(OUTILS));import convertir_notion
rows=[];flags=[]
for n in notions:
 d=ROOT/f"{n.id}_{ns['slug'](n.titre)}"
 if not (d/'source_en_ligne/meta.json').exists():ns['exporter_notion'](n)
 assert (d/'source_en_ligne/meta.json').exists()
 if not (d/'etat.json').exists():
  warnings,problems=convertir_notion.convertir(d)
  (d/'conversion_initiale.json').write_text(json.dumps({'avertissements':warnings,'problemes':problems},ensure_ascii=False,indent=2),encoding='utf-8')
  (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'a_attribuer','maj':datetime.date.today().isoformat()},indent=2),encoding='utf-8')
 m=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
 hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (d/'source_en_ligne').iterdir() if p.is_file()}
 manifest=d/'empreintes_sources.json'
 if manifest.exists():assert json.loads(manifest.read_text(encoding='utf-8'))==hashes
 else:manifest.write_text(json.dumps(hashes,indent=2),encoding='utf-8')
 row={'notion':n.id,'titre':n.titre,'dossier':d.name,'cours':len(m['cours']),'fiches':len(m['fiches']),'exercices':len(m['exercices']),'images':sum(len(o['images']) for g in ('cours','fiches','exercices') for o in m[g])}
 rows.append(row);flags.append({'notion':n.id,'est_actif':n.est_actif})
 print(json.dumps(row,ensure_ascii=False),flush=True)
for name,content in [('inventaire_initial_cm2.json',rows),('contexte_cm2.json',{'id':ctx.id,'niveau':ctx.niveau_id,'matiere':ctx.matiere_id}),('activations_initiales_notions.json',flags)]:
 p=ICI/name
 if not p.exists():p.write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('TOTAL',json.dumps({k:sum(r[k] for r in rows) for k in ('cours','fiches','exercices','images')}),flush=True)
