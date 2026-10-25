"""Livre seulement le PDF contrôlé et relu, puis vérifie les deux copies."""
from pathlib import Path
import hashlib,json,shutil,subprocess,re
ROOT=Path(__file__).resolve().parent
PDF=ROOT/'main.pdf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
qa=json.loads((ROOT/'recherches/verification-pdf.json').read_text(encoding='utf-8'))
contenu=json.loads((ROOT/'recherches/verification-contenu.json').read_text(encoding='utf-8'))
vue=json.loads((ROOT/'recherches/validation-visuelle.json').read_text(encoding='utf-8'))
assert qa['sha256']==vue['sha256']==sha(PDF)
assert not qa['erreurs'] and not contenu['echecs'] and vue['validee']
nom='OptiTAB - Physique-chimie - Seconde générale et technologique - Manuel complet.pdf'
targets=[ROOT.parent/'output/pdf/France/Physique-chimie'/nom,
         Path.home()/'Desktop/Livres OptiTAB - Lycée'/nom]
for target in targets:
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(PDF,target)
    assert sha(target)==qa['sha256']
report=dict(qa,copies=[str(p.resolve()) for p in targets],copies_identiques=True,
            controles_contenu=contenu['controles'],programme='BO spécial n° 1 du 22 janvier 2019, MENE1901634A',
            concordance=99,relecture_visuelle=vue)
out=ROOT.parent/'output/verification';out.mkdir(exist_ok=True)
(out/'physique-chimie-seconde-20261025.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
md=f'''# Physique-chimie Seconde - livraison du 25 octobre 2026

Manuel de {qa['pages']} pages, 20 chapitres, 240 exercices et 20 défis corrigés, six évaluations de 90 minutes avec 18 exercices et barèmes. Quatre ateliers numériques et des fiches pratiques de laboratoire complètent le cours.

- Programme BO 2019 vérifié sur Éduscol en octobre 2026 ; concordance détaillée de 99 points dans les sources.
- {qa['figures_sources']} sources de figures vectorielles, {qa['insertions_figures']} insertions dans les cours, énoncés et solutions ; variantes de construction complétées dans les corrigés.
- {contenu['controles']} contrôles de contenu sans échec : inventaire, questions et réponses, calculs, bilans, constructions optiques et barèmes.
- {qa['blocs_mesures']} blocs d'exercices et de corrigés mesurés à la compilation ; aucun débordement ni caractère manquant dans le journal stabilisé.
- Contrôle de toutes les pages : format A4, absence de texte hors page et de collision candidate, liens internes résolus, {qa['polices']} polices incorporées.
- Relecture des planches de toutes les pages, complétée par des vues détaillées des figures et des pages sensibles. Les espaces de notes et le verso de couverture sont intentionnels.
- PDF classé dans France / Physique-chimie et copie du Bureau identique.

SHA-256 : `{qa['sha256']}`

Sources et outils de reconstruction : `livre-pc-seconde/`. Recherche documentaire : `recherches/RECHERCHES.md`. Concordance : `recherches/COUVERTURE-PROGRAMME.md`. Rapports détaillés JSON conservés dans les sources.
'''
(out/'physique-chimie-seconde-20261025.md').write_text(md,encoding='utf-8')
(ROOT/'README.md').write_text(f'''# OptiTAB - Physique-chimie Seconde

Édition du 25 octobre 2026 : {qa['pages']} pages, programme français de Seconde générale et technologique (BO 2019, statut vérifié en 2026).

20 chapitres ; 240 exercices à trois niveaux ; 20 défis avec indications ; six évaluations originales de 90 minutes, corrigés et barèmes ; activités expérimentales ; quatre ateliers numériques. Les corrigés comportent les constructions utiles et des conseils ciblés.

## Reconstruire

Depuis ce dossier, avec Python, NumPy et LuaLaTeX (MiKTeX sous Windows, polices de la collection installées) :

```powershell
python structure.py
python figures.py
python verifier_contenu.py
python compiler.py
python verifier_pdf.py
```

La compilation se fait sur un instantané des sources et stabilise les renvois avant de produire `main.pdf`. Ne pas modifier les sources pendant la compilation. La relecture visuelle et le contrôle final restent nécessaires après toute modification.

Le livrable classé et sa copie du Bureau ont le même SHA-256 : `{qa['sha256']}`.

Les données d'entraînement sont construites. Le manuel est une publication indépendante de la collection ; aucune homologation du ministère n'est revendiquée.
''',encoding='utf-8')
print(json.dumps(dict(pages=qa['pages'],copies=[str(p) for p in targets],sha256=qa['sha256']),ensure_ascii=False,indent=2))
