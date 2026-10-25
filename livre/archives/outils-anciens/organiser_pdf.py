"""Classe les livrables PDF par pays et matière, sans modifier leur contenu."""
from pathlib import Path
import hashlib, json
import fitz

ROOT=Path(__file__).resolve().parents[1]
PDF_ROOT=(ROOT/'output/pdf').resolve()
CATALOGUE=[
    ('optitab-maternelle-ps.pdf','Mathématiques','Petite section (PS)',"Cahier d’activités"),
    ('optitab-maternelle-ms.pdf','Mathématiques','Moyenne section (MS)',"Cahier d’activités"),
    ('optitab-maternelle-gs.pdf','Mathématiques','Grande section (GS)',"Cahier d’activités"),
    ('optitab-cp-complet.pdf','Mathématiques','CP','Manuel complet'),
    ('optitab-ce1-complet.pdf','Mathématiques','CE1','Manuel complet'),
    ('optitab-ce2-complet.pdf','Mathématiques','CE2','Manuel complet'),
    ('optitab-cm1-complet.pdf','Mathématiques','CM1','Manuel complet'),
    ('optitab-cm2-complet.pdf','Mathématiques','CM2','Manuel complet'),
    ('optitab-sixieme-complet.pdf','Mathématiques','Sixième (6e)','Manuel complet'),
    ('optitab-cinquieme-complet.pdf','Mathématiques','Cinquième (5e)','Manuel complet'),
    ('optitab-quatrieme-complet.pdf','Mathématiques','Quatrième (4e)','Manuel complet'),
    ('optitab-troisieme-brevet-complet.pdf','Mathématiques','Troisième (3e) - Brevet 2027','Manuel complet'),
    ('optitab-seconde-complet.pdf','Mathématiques','Seconde générale et technologique','Manuel complet'),
    ('optitab-premiere-complet.pdf','Mathématiques','Première spécialité','Manuel complet'),
    ('optitab-physique-chimie-5e-complet.pdf','Physique-chimie','Cinquième (5e)','Manuel complet'),
    ('optitab-physique-chimie-terminale.pdf','Physique-chimie','Terminale spécialité','Manuel complet'),
]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    report=ROOT/'output/verification/classement-pdf.json'
    previous={}
    if report.exists():
        previous={p['ancien_nom']:p for p in json.loads(report.read_text(encoding='utf8'))['livres']}
    plan=[]
    for old,matter,level,kind in CATALOGUE:
        source=(PDF_ROOT/old).resolve()
        name=f'OptiTAB - {matter} - {level} - {kind}.pdf'
        target=(PDF_ROOT/'France'/matter/name).resolve()
        assert source.is_relative_to(PDF_ROOT) and target.is_relative_to(PDF_ROOT)
        assert source.suffix==target.suffix=='.pdf'
        if source.exists() and target.exists():raise FileExistsError(f'Destination déjà occupée : {target}')
        current=source if source.exists() else target
        if not current.is_file():raise FileNotFoundError(current)
        with fitz.open(current) as doc:pages=len(doc)
        plan.append(dict(source=source,target=target,matiere=matter,niveau=level,type=kind,pages=pages,sha256=digest(current)))
    # Les nouveaux livres déjà livrés avec la même convention sont aussi indexés.
    known={p['source'] for p in plan}|{p['target'] for p in plan}
    for current in sorted(PDF_ROOT.rglob('*.pdf')):
        current=current.resolve()
        if current in known:continue
        parts=current.relative_to(PDF_ROOT).parts
        assert len(parts)==3 and parts[0]=='France',f'PDF à classer explicitement : {current}'
        matter=parts[1];prefix=f'OptiTAB - {matter} - '
        assert current.name.startswith(prefix),f'Nom à harmoniser : {current}'
        description=current.stem[len(prefix):].rsplit(' - ',1)
        assert len(description)==2
        level,kind=description
        with fitz.open(current) as doc:pages=len(doc)
        plan.append(dict(source=current,target=current,matiere=matter,niveau=level,type=kind,pages=pages,sha256=digest(current)))
    assert len({p['target'] for p in plan})==len(plan)
    # Tous les chemins et toutes les collisions sont contrôlés avant le premier déplacement.
    for item in plan:
        source,target=item['source'],item['target']
        target.parent.mkdir(parents=True,exist_ok=True)
        if source!=target and source.exists():source.rename(target)
        assert target.is_file() and digest(target)==item['sha256']
        if source!=target:assert not source.exists()
    assert not list(PDF_ROOT.glob('*.pdf')),'Un PDF non classé subsiste à la racine.'
    entries=[]
    for p in plan:
        old=previous.get(p['source'].name,{})
        original_sha=old.get('sha256_au_classement',old.get('sha256',p['sha256']))
        entries.append(dict(pays='France',matiere=p['matiere'],niveau=p['niveau'],type=p['type'],pages=p['pages'],
                            ancien_nom=p['source'].name,chemin=p['target'].relative_to(ROOT).as_posix(),
                            sha256=p['sha256'],sha256_au_classement=original_sha,
                            mis_a_jour_depuis_classement=original_sha!=p['sha256']))
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(dict(pdf_classes=len(entries),contenus_identiques=True,livres=entries),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    index=['# Bibliothèque OptiTAB\n\n','Les livres sont classés par pays, puis par matière.\n\n','## France\n\n']
    for matter in dict.fromkeys(p['matiere'] for p in plan):
        index+=['### '+matter+'\n\n','| Niveau | Ouvrage | Pages |\n','| --- | --- | ---: |\n']
        for p in plan:
            if p['matiere']!=matter:continue
            rel=p['target'].relative_to(PDF_ROOT).as_posix()
            index.append(f"| {p['niveau']} | [{p['type']}](<{rel}>) | {p['pages']} |\n")
        index.append('\n')
    (PDF_ROOT/'README.md').write_text(''.join(index),encoding='utf8')
    print(json.dumps(dict(pdf_classes=len(entries),mathematiques=sum(p['matiere']=='Mathématiques' for p in plan),
                         physique_chimie=sum(p['matiere']=='Physique-chimie' for p in plan),contenus_identiques=True,index=str(PDF_ROOT/'README.md')),ensure_ascii=False))

if __name__=='__main__':main()
