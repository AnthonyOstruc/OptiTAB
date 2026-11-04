"""Contrôle de concurrence anticipé : lecture seule des 26 notions en base."""
from pathlib import Path
import os,sys,json,re,datetime
sys.stdout.reconfigure(encoding='utf-8')
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent;BACKEND=ICI.parents[5]/'backend';OUTILS=ROOT.parents[1]/'outils'
os.chdir(BACKEND);sys.path.insert(0,str(BACKEND));os.environ.setdefault('DJANGO_SETTINGS_MODULE','backendAPI.settings')
import django
django.setup()
from cours.models import Cours
from synthesis.models import SynthesisSheet
from curriculum.models import Exercice
script=OUTILS/'importer_v1.py';source=script.read_text(encoding='utf-8');ns={'__file__':str(script),'__name__':'controle_lecture_6e'}
exec(compile(source.rstrip()[:-len('main()')],str(script),'exec'),ns)
rows=[]
for d in sorted(ROOT.iterdir()):
 if not (d/'source_en_ligne/meta.json').exists():continue
 meta=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'));errors=[]
 for genre,Model,field,prefix in [('cours',Cours,'contenu','cours_'),('fiches',SynthesisSheet,'summary','fiche_')]:
  for item in meta[genre]:
   obj=Model.objects.get(id=item['id']);expected=(d/'source_en_ligne'/f'{prefix}{obj.id}.txt').read_bytes().decode('utf-8')
   if 'Titre: '+obj.titre+'\n\n'+(getattr(obj,field) or '').replace('\r\n','\n')!=expected:errors.append(f'{genre} {obj.id} modifie')
 original=ns['blocs_source'](d/'source_en_ligne/exercices.txt')
 for item in meta['exercices']:
  obj=Exercice.objects.get(id=item['id']);names=[Path(im.image.name).name for im in ns['images_en_base']('exercices',obj.id)]
  if ns['bloc_export'](obj,names)!=original.get(obj.id):errors.append(f'exercice {obj.id} modifie')
 for genre in ('cours','fiches','exercices'):
  for item in meta[genre]:
   actual={(im.position,im.image.name) for im in ns['images_en_base'](genre,item['id'])};expected={(im['position'],im['nom']) for im in item['images']}
   if actual!=expected:errors.append(f'images {genre} {item["id"]} modifiees')
 if not meta['cours'] and Cours.objects.filter(notion_id=meta['notion']).exists():errors.append('cours cree depuis export')
 if not meta['fiches'] and SynthesisSheet.objects.filter(notion_id=meta['notion']).exists():errors.append('fiche creee depuis export')
 if not meta['exercices'] and Exercice.objects.filter(notion_id=meta['notion']).exists():errors.append('exercices crees depuis export')
 rows.append({'notion':meta['notion'],'ecarts':errors});print(meta['notion'],'OK' if not errors else errors,flush=True)
report={'date':datetime.datetime.now().isoformat(timespec='seconds'),'lecture_seule':True,'notions':rows,'statut':'OK' if all(not r['ecarts'] for r in rows) else 'conflits'}
(ICI/'concurrence_initiale_6e.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if report['statut']=='OK' else 2)
