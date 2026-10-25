"""Publie uniquement le PDF commun, après contrôle et relecture visuelle complets."""
from pathlib import Path
import json,hashlib,shutil,zipfile
from assembler_livre import ROOT,OUT

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def deliver():
    report=json.loads((OUT/'build/verification.json').read_text(encoding='utf-8'))
    pdf=OUT/'build/main.pdf'
    assert report['sha256']==sha(pdf)
    assert report['pagination_conforme'] and report['chapitres']==10
    for key in ['erreurs_compilation','textes_hors_page','collisions_candidates','textes_bas_page','liens_invalides']:assert not report[key],key
    visual=report['relecture_visuelle']
    assert visual['pages_relues']==list(range(1,report['pages']+1))
    imgs=sorted((OUT/'build/qa').glob('page-*.png'))
    assert len(imgs)==report['pages']
    assert visual['empreintes_pages']=={p.name:sha(p) for p in imgs}
    filename='OptiTAB - Physique - MPSI - Ondes et signaux - Chapitres 01 a 10.pdf'
    repo=ROOT.parent
    destinations=[repo/'output/pdf/France/Physique-chimie'/filename,Path('C:/Users/SWEELCO-AT/Desktop/Livres OptiTAB - Lycée')/filename]
    for target in destinations:
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(pdf,target);assert sha(target)==report['sha256']
    vr=repo/'output/verification';vr.mkdir(exist_ok=True)
    shutil.copy2(OUT/'build/verification.json',vr/'physique-mpsi-chapitres-01-a-10.json')
    (vr/'physique-mpsi-chapitres-01-a-10.md').write_text(f'''# OptiTAB Physique MPSI : volume unique

{report['pages']} pages, pagination continue, 10 chapitres, 240 exercices corrigés,
30 défis, 10 TP, 10 activités numériques, 10 DM et 10 DS corrigés avec barèmes.

Les rubriques 1.1 à 1.6 du programme MPSI sont développées dans les chapitres 1 à 9.
Le chapitre 10 sur les cordes est explicitement identifié comme approfondissement.
Les chapitres 11 à 28 du sommaire annuel sont annoncés sans pages fictives.

- Compilation sans débordement, caractère manquant ni référence indéfinie.
- Pagination de toutes les ouvertures et sections vérifiée.
- {report['liens']} liens ; aucun lien interne invalide.
- {report['signets']} signets, dont dix entrées principales de chapitre.
- {len(report['controles_nouveaux'])} contrôles scientifiques nouveaux ; {len(report['controles_anterieurs'])} contrôles antérieurs conservés.
- Codes publiés des cinq nouveaux chapitres exécutés et confrontés aux lois analytiques.
- Toutes les pages rendues avec Poppler puis relues visuellement ; figures et pages denses réinspectées.
- Aucun texte hors page ni collision détectée ou constatée à la relecture finale.

SHA-256 : `{report['sha256']}`.

Les anciens fascicules restent des versions antérieures. La livraison de référence
est désormais le seul PDF commun, sans couvertures ou sommaires répétés.
''',encoding='utf-8')
    readme=repo/'output/pdf/README.md';s=readme.read_text(encoding='utf-8');lines=[l for l in s.splitlines() if not l.startswith('| MPSI - Physique |')]
    lines.append(f'| MPSI - Physique | [Ondes et signaux - Chapitres 01 à 10 réunis](<France/Physique-chimie/{filename}>) | {report["pages"]} |')
    readme.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    archive=repo/'output/sources/optitab-physique-mpsi-chapitres-01-a-10-sources.zip';archive.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in OUT.rglob('*'):
            if p.is_file() and 'build' not in p.relative_to(OUT).parts and '__pycache__' not in p.parts:
                z.write(p,'livre-physique-mpsi-integral/'+p.relative_to(OUT).as_posix())
        z.write(OUT/'build/verification.json','controle/verification.json')
        for name in ['sources.json','sources-06-a-10.json']:
            z.write(ROOT/'recherche'/name,'controle/'+name)
    report['livraison']=[str(p) for p in destinations]
    (vr/'physique-mpsi-chapitres-01-a-10.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(pdf=[str(p) for p in destinations],pages=report['pages'],sha256=report['sha256'],sources=str(archive)),ensure_ascii=False),flush=True)

if __name__=='__main__':deliver()
