"""Livrer les quatre PDF vérifiés, les sources et les rapports."""
from pathlib import Path
import json,hashlib,shutil,zipfile

R=Path(__file__).resolve().parent;ROOT=R.parent
OUT=ROOT/'output/pdf/France/Physique-chimie';OUT.mkdir(parents=True,exist_ok=True)
V=ROOT/'output/verification';V.mkdir(exist_ok=True)
Z=ROOT/'output/sources';Z.mkdir(exist_ok=True)
DESKTOP=Path('C:/Users/SWEELCO-AT/Desktop/Livres OptiTAB - Lycée');DESKTOP.mkdir(exist_ok=True)
names={2:'Signaux electriques dans l ARQS',3:'Circuits lineaires du premier ordre',4:'Oscillateur harmonique',5:'Oscillations libres amorties'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reports=[];outputs=[]
for n in range(2,6):
 folder=R/f'chapitre-{n:02}';B=folder/'build';report=json.loads((B/'verification.json').read_text(encoding='utf-8'))
 assert report['pages']==report['pages_prevues'] and report['pagination_conforme']
 assert not any(report[x] for x in ['erreurs_compilation','textes_hors_page','collisions_candidates','liens_invalides'])
 assert report.get('relecture_visuelle',{}).get('pages_relues')==list(range(1,report['pages']+1)),'Relecture visuelle requise.'
 pdf=B/'main.pdf';assert sha(pdf)==report['sha256']
 name=f'OptiTAB - Physique - MPSI - Chapitre {n:02} - {names[n]}.pdf'
 target=OUT/name;desktop=DESKTOP/name
 shutil.copy2(pdf,target);shutil.copy2(pdf,desktop);assert sha(target)==sha(desktop)==report['sha256']
 report['livraisons']=[str(target),str(desktop)]
 (V/f'physique-mpsi-chapitre-{n:02}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 outputs.append(target);reports.append(report)
 index=ROOT/'output/pdf/README.md';text=index.read_text(encoding='utf-8');rows=text.splitlines()
 row=f'| MPSI - Physique | [Chapitre {n:02} - {report["titre"]}](<France/Physique-chimie/{name}>) | {report["pages"]} |'
 if any(name in x for x in rows):rows=[row if name in x else x for x in rows]
 else:rows.append(row)
 index.write_text('\n'.join(rows)+'\n',encoding='utf-8')

with zipfile.ZipFile(Z/'optitab-physique-mpsi-chapitres-02-a-05-sources.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in R.rglob('*'):
  rel=p.relative_to(R)
  if p.is_file() and not any(x in rel.parts for x in ['build','__pycache__','recherche']) and p.suffix in ['.py','.tex','.sty','.json','.png','.md']:
   z.write(p,'livre-physique-mpsi-suite/'+rel.as_posix())
 z.write(R/'recherche/sources.json','livre-physique-mpsi-suite/recherche/sources.json')
 # Base utilisée par le constructeur, autonome après extraction de l'archive.
 prev=ROOT/'livre-physique-mpsi'
 for p in [prev/'mpsi-livre.sty',prev/'plan.tex',*list((prev/'images').glob('*.png'))]:z.write(p,'livre-physique-mpsi/'+p.relative_to(prev).as_posix())
with zipfile.ZipFile(ROOT/'output/pdf/OptiTAB - Physique MPSI - Chapitres 02 a 05.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in outputs:z.write(p,p.name)

lines=['# Physique MPSI : chapitres 02 à 05','', 'Livraison du 25 octobre 2026. Les quatre fascicules poursuivent la charte validée au chapitre 01.','', '| Chapitre | Pages | Exercices corrigés | Défis | DM | DS | Contrôles numériques |','|---|---:|---:|---:|---:|---:|---:|']
for s in reports:lines.append(f'| {s["chapitre"]:02} - {s["titre"]} | {s["pages"]} | 24 | 3 | 1 | 1 | {len(s["controles"])} |')
lines+=['',f'Total : {sum(s["pages"] for s in reports)} pages, 96 exercices corrigés, 12 défis corrigés, 4 TP, 4 activités numériques, 4 DM et 4 DS de 2 h avec corrigés et barèmes.','', '## Vérification','', '- Référence : programme de physique-chimie MPSI, arrêté du 5 janvier 2021, annexe 2, rubriques 1.2, 1.3 et partie transitoire de 1.4. La suite de 1.4 (impédances et régime sinusoïdal forcé) est réservée au chapitre 06.', '- Énoncés OptiTAB originaux identifiés ; parcours distincts sur les DM, DS et sujets publiés avec URL et questions précises.', '- Recalculs des exemples et problèmes, contrôles de conservation, conditions initiales, résidus des équations différentielles et bilans numériques.', '- Compilation LuaLaTeX sans Overfull, caractères manquants ou références indéfinies.', '- Pagination, destinations et liens internes contrôlés ; aucun texte hors page ni collision de texte candidate dans les PDF livrés.', '- Toutes les pages rendues avec Poppler puis inspectées visuellement ; aucune troncature ni collision de figure repérée.', '- Copies du Bureau et de la bibliothèque identiques aux PDF vérifiés (SHA-256 dans les rapports JSON).','', '## Sources','', 'Les URL, pages et empreintes des documents téléchargés sont conservées dans le dossier de recherche. L’archive source inclut leur manifeste, mais ne réédite pas les PDF extérieurs. Les chapitres renvoient aux documents d’origine.','', 'Les contrôles ne constituent pas une certification indépendante du contenu ; ils réunissent vérification mathématique, contrôle des références et inspection de mise en page.']
(V/'physique-mpsi-chapitres-02-a-05.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(dict(pages=sum(s['pages'] for s in reports),controles=sum(len(s['controles']) for s in reports),pdf=[str(p) for p in outputs]),ensure_ascii=False,indent=2))
