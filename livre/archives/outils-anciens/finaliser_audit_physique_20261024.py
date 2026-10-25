"""Vérifie les copies livrées et consigne la portée exacte de la révision."""
from pathlib import Path
import json,hashlib,re
import fitz
root=Path(__file__).resolve().parents[1]
out=root/'output/verification'
desktop=Path('C:/Users/SWEELCO-AT/Desktop/Livres OptiTAB - Lycée')

def read(p):return json.loads((root/p).read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

settings=[
 ('Cinquième (5e)','livre-pc-cinquieme/template-terminale/main.pdf','livre-pc-cinquieme/template-terminale/build/qa/controles.json','livre-pc-cinquieme/template-terminale/build/audit-revision.json','OptiTAB - Physique-chimie - Cinquième (5e) - Manuel complet.pdf'),
 ('Quatrième (4e)','livre-pc-quatrieme/build/main.pdf','livre-pc-quatrieme/build/verification.json',None,'OptiTAB - Physique-chimie - Quatrième (4e) - Manuel complet.pdf'),
 ('Troisième / Brevet 2027','livre-pc-brevet/build/main.pdf','livre-pc-brevet/build/verification.json','livre-pc-brevet/build/audit-annales.json','OptiTAB - Physique-chimie - Troisième (3e) - Brevet 2027 - Manuel complet.pdf'),
 ('Terminale spécialité','livre-pc-terminale/main.pdf','livre-pc-terminale/build/audit-revision.json',None,'OptiTAB - Physique-chimie - Terminale spécialité - Manuel complet.pdf')]
books=[]
for level,source,qa,revision,name in settings:
    source=root/source
    target=root/'output/pdf/France/Physique-chimie'/name
    sha=digest(source)
    checks=read(qa)
    assert checks['sha256']==sha
    assert checks.get('echecs',0)==0
    if revision:
        rev=read(revision)
        assert rev['echecs']==0 and rev['sha256']==sha
    assert digest(target)==digest(desktop/name)==sha
    with fitz.open(target) as doc:pages=len(doc)
    assert pages==checks['pages']
    books.append(dict(niveau=level,pages=pages,sha256=sha,pdf=str(target.resolve()),copie_bureau=str((desktop/name).resolve()),copies_identiques=True,rapport=qa,revision=revision,modifie_ce_passage=level!='Quatrième (4e)'))

report=dict(date='2026-10-24',valide=True,livres=books,sujets_brevet=dict(total=15,ajoutes=5,duree_minutes=30,discipline='Physique-chimie',questions_ajoutees=45,figures_ajoutees=28,calculs_ajoutes=22,controles_annales=208,echecs=0,creation_originale=True,annales_etudiees=[2025,2026,2027]),premiere=dict(statut='en cours de rédaction',chapitres_sources_audites=20,chapitres_pdf_initial=12,corrections_sources=['06-lewis.tex : exercices 12 et 14, énoncés et corrigés'],epreuve_isolee_pages=295,epreuve_isolee_livree=False,controle_final_a_refaire_sur_manuel_termine=True),portee=['Relecture de la présence et de la cohérence des documents nécessaires aux cours, énoncés et solutions.','Rendus complets par planches pour la mise en page, plus figures nouvelles et pages critiques à grande résolution avec Poppler.','Contrôles ciblés des calculs, constructions, liens, marges, caractères et débordements ; ils ne constituent pas une démonstration automatique de toute la prose.','Quatrième : nouvelle vérification sans modification du PDF déjà révisé.','Première : corrections intégrées aux sources et compilées dans une épreuve isolée ; contrôle final du livre en rédaction à reprendre après son achèvement.'],sources=['https://eduscol.education.gouv.fr/4362/enseigner-au-cycle-4','https://eduscol.education.gouv.fr/5739/ressources-d-accompagnement-du-programme-de-physique-chimie-au-cycle-4','https://www.education.gouv.fr/bo/2026/Hebdo4/MENE2623228N','https://www.education.gouv.fr/sites/default/files/2025-06/dipl-me-national-du-brevet-2025---sciences-440574.pdf','https://www.education.gouv.fr/sites/default/files/document/diplome-national-du-brevet-2026-sciences-serie-generale-517070.pdf','https://eduscol.education.gouv.fr/5607/les-epreuves-du-dnb'])
(out/'audit-physique-chimie-20261024.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# Révision des manuels de physique-chimie - 24 octobre 2026\n\n','Les copies classées par pays et matière et celles du Bureau ont été comparées par SHA-256. Les anciennes éditions sont conservées dans `output/archives/revision-physique-chimie-20261024/`.\n\n','| Manuel | Pages | Résultat |\n','| --- | ---: | --- |\n']
for b in books:md.append(f"| {b['niveau']} | {b['pages']} | Copies identiques, contrôles réussis |\n")
md+=['\nLa Cinquième reçoit 45 modèles vectoriels nouveaux, des documents locaux dans les exercices concernés, 27 démarches supplémentaires et des figures dans les défis et bilans utiles. Les 763 contrôles du PDF et 471 contrôles de révision passent. Les 29 planches et 18 preuves Poppler finales ont été inspectées.\n\n','La Quatrième conserve sa version révisée de 289 pages : 1 419 contrôles, dont 209 calculs, sans échec. La nouvelle vérification des marges et collisions ne signale aucun défaut.\n\n','Le Brevet conserve ses 270 exercices, 18 investigations et 18 défis. Il réunit désormais 15 sujets originaux PC de 30 min. Les cinq sujets ajoutés comportent 45 questions, 28 figures et 22 calculs supplémentaires. Réponses, démarches, barèmes et remédiations sont inclus. Contrôles : 3 240 pour le PDF, 533 pour la révision initiale et 208 pour les nouveaux sujets, sans échec. Les annales officielles de 2025 et 2026 et le sujet de référence 2027 ont été étudiés pour les attendus ; leurs questions et leurs figures ne sont pas reproduites. Le contrôle textuel ciblé ne trouve aucune séquence de douze mots commune aux nouveaux documents/questions et aux trois archives.\n\n','La Terminale conserve ses 27 chapitres, 405 exercices, 27 défis et six sujets type bac. Dix-huit constructions nouvelles et cinq reprises de figures existantes complètent 23 corrigés ; trois énoncés reçoivent leur document local. Le chevauchement des légendes de 12.11 est réparé. Les conventions RC et le couplage capacitif sont explicités. Les 28 scripts numériques et les 54 contrôles complémentaires passent. Les 36 planches du PDF final et 25 preuves Poppler sont inspectées.\n\n','La Première est en rédaction. L’audit des sources disponibles couvre 20 chapitres ; le PDF disponible au départ en comportait 12. Deux précisions scientifiques au chapitre 6 ont été intégrées aux sources et vérifiées dans une copie isolée. Cette épreuve de 295 pages reste interne. Le contrôle final devra être repris sur le manuel terminé.\n\n','Les contrôles ciblés complètent la relecture scientifique et visuelle ; ils ne prouvent pas automatiquement toutes les phrases des ouvrages.\n\n','## Sources primaires consultées\n\n']
md += [f'- {s}\n' for s in report['sources']]
(out/'audit-physique-chimie-20261024.md').write_text(''.join(md),encoding='utf-8')

# Mises à jour limitées aux informations de cette révision ; la colonne de
# validation personnelle et les lignes des autres travaux sont conservées.
p=root/'SUIVI-LIVRES.md'
s=p.read_text(encoding='utf-8')
rows=s.splitlines()
for i,line in enumerate(rows):
    if line.startswith('| Physique-chimie — Cinquième |'):
        fields=line.split('|');fields[3]=' ✅ Terminé ';fields[5]=' Livré et révisé le 24/10/2026 — 346 pages, 20 chapitres, 300 exercices, 20 défis et quatre bilans ; 194 figures vectorielles distinctes, 61 énoncés et 85 corrigés d’exercices illustrés, figures complémentaires dans les défis et bilans utiles, 27 démarches enrichies ; 763 contrôles du PDF et 471 contrôles de révision sans échec ; 29 planches et 18 preuves Poppler finales inspectées ; PDF classé et copie du Bureau identiques '
        rows[i]='|'.join(fields)
    elif line.startswith('| Physique-chimie — Troisième |'):
        fields=line.split('|');fields[5]=' Livré et révisé le 24/10/2026 — 327 pages, 18 chapitres, 270 exercices corrigés, 18 investigations et 18 défis, 239 figures ; 15 sujets originaux PC de 30 min, dont cinq nouveaux dossiers au format des annales, avec 45 questions et 28 figures supplémentaires ; corrigés expliqués, barèmes /10 et remédiation ; 3 240 contrôles du PDF dont 241 calculs, 533 contrôles de révision et 208 contrôles des nouveaux sujets sans échec ; programme cycle 4 et format DNB vérifiés sur sources officielles ; PDF classé et copie du Bureau identiques '
        rows[i]='|'.join(fields)
    elif line.startswith('| Physique-chimie — Terminale spécialité |'):
        fields=line.split('|');fields[5]=' Livré le 23/10 et révisé le 24/10/2026 — 709 pages, 27 chapitres, 405 exercices corrigés, 27 défis et six sujets type bac ; 18 constructions nouvelles, 23 corrigés et trois énoncés enrichis de figures, légendes de 12.11 réajustées, explications RC précisées ; 28 scripts numériques et 54 contrôles complémentaires réussis ; 36 planches et 25 preuves Poppler finales inspectées ; PDF classé et copie du Bureau identiques '
        rows[i]='|'.join(fields)
    elif line.startswith('**Physique-chimie Terminale livrée**'):
        rows[i]='**Physique-chimie Terminale livrée et révisée** le 24/10/2026 (709 pages, figures complétées et chevauchement de légendes corrigé ; PDF classé et copie du Bureau identiques).'
    elif line.startswith('**Physique-chimie Troisième / Brevet 2027 livrée et révisée**'):
        rows[i]='**Physique-chimie Troisième / Brevet 2027 livrée et révisée** le 24/10/2026 (327 pages, 239 figures et 15 sujets originaux PC de 30 minutes, dont cinq nouveaux dossiers au format des annales avec documents et corrigés pédagogiques ; copies classée et du Bureau identiques).'
    elif line.strip().startswith('- PC Cinquième : manuel complet en cours'):
        rows[i]='   - PC Cinquième : **terminé et livré** le 24/10/2026 (346 pages, figures et corrigés complétés ; PDF classé et copie du Bureau identiques).'
    elif line.startswith('| Physique-chimie | 3 | 2 |'):
        rows[i]=line.replace('| 3 | 2 |','| 4 | 1 |')
    elif line.startswith('| **Total** | **20** | **3** |'):
        rows[i]=line.replace('| **20** | **3** |','| **21** | **2** |')
    elif line.startswith('1. **En cours (3)**'):
        rows[i]=line.replace('(3)','(2)')
s='\n'.join(rows)+'\n'
# Retirer de la liste "En cours" la ligne désormais livrée, sans toucher aux
# descriptions des travaux Première et MPSI qui progressent indépendamment.
s=s.replace('   - PC Cinquième : **terminé et livré** le 24/10/2026 (346 pages, figures et corrigés complétés ; PDF classé et copie du Bureau identiques).\n','')
p.write_text(s,encoding='utf-8')

p=root/'livre-pc-brevet/README.md';s=p.read_text(encoding='utf-8')
s=s.replace('Les dix sujets sont les **volets PC de 30 minutes**','Les quinze sujets sont des **volets PC de 30 minutes**')
s=s.replace('Les deux PDF officiels consultés pour analyser les attendus sont archivés.','Les trois PDF officiels consultés pour analyser les attendus sont archivés.')
s=s.replace('python livre-pc-brevet/verifier.py\n','python livre-pc-brevet/verifier.py\npython livre-pc-brevet/auditer_annales.py\n')
s=s.replace('`brevets.py`, les dix sujets ;','`brevets.py`, les dix premiers sujets ; `annales_originales.py` et `figures_annales.py`, les cinq dossiers supplémentaires ;')
p.write_text(s,encoding='utf-8')
print(json.dumps(dict(livres=len(books),pages=[b['pages'] for b in books],copies_identiques=True),ensure_ascii=False))
