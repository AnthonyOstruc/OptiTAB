"""Exporte après les contrôles mathématiques et visuels du PDF final."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'output'
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
qa=read('build/qa/controle-pdf.json')
visual=read('build/qa/relecture-visuelle.json')
maths=read('build/verification-contenu.json')
extra=read('build/verification-complements.json')
programme=read('build/couverture-programme.json')
digest=hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest()
assert qa['sha256']==visual['sha256']==digest
assert not qa['texte_hors_page'] and not qa['pages_vides'] and not visual['defauts_restants']
assert maths['exercices_controles']==240 and not maths['erreurs']
assert extra['groupes_de_controles']==82 and not extra['erreurs']
assert extra['questions_flash']==40 and extra['capacites_automatismes_couvertes']==30
assert len(programme['groupes_editoriaux'])==64 and len(programme['approfondissements_programme'])==14
assert programme['attendus_officiels']==programme['attendus_presents']==len(programme['matrice_officielle'])
assert all(o['statut']=='présent' and o['lieux'] for o in programme['matrice_officielle'])
assert qa['figures_avec_leur_texte']==207
for sub in ['pdf','sources','verification']:(OUT/sub).mkdir(parents=True,exist_ok=True)
target=OUT/'pdf/France/Mathématiques/OptiTAB - Mathématiques - Seconde générale et technologique - Manuel complet.pdf'
target.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(ROOT/'main.pdf',target)
report=f"""# Vérification du livre OptiTAB de Seconde

Édition du 23 octobre 2026, après audit de conformité au programme. Seconde générale et technologique, France.

- {qa['pages']} pages ; 16 chapitres ; 256 exercices corrigés : 240 exercices de chapitre et 16 défis facultatifs.
- Quatre séries de questions flash corrigées : 40 questions couvrant les 30 capacités de la partie « Automatismes ».
- Deux bilans originaux corrigés : 20 automatismes et 6 problèmes, barème éditorial sur 20 pour chacun.
- 13 démonstrations de référence, dont les 11 démonstrations identifiées dans le programme.
- 103 fichiers de représentations vectorielles, avec 207 insertions dans les énoncés, corrigés et ateliers, et des tableaux de variations dans le cours et les solutions.
- {qa['signets']} signets et {qa['liens']} liens contrôlés.

## Programme et recherches

Le [programme officiel du BO du 2 avril 2026](https://www.education.gouv.fr/bo/2026/Hebdo14/MENE2602914A) s’applique en 2026-2027. Son annexe de 13 pages a été lue intégralement. La matrice du livre repère 64 groupes éditoriaux de contenus et capacités. Les 14 pistes d’approfondissement explicitement nommées sont toutes traitées ; elles restent facultatives. L’ordre du livre est un choix pédagogique.

## Audit de conformité du 23 octobre 2026

Texte relu : arrêté du 26-2-2026 (JO du 27-3-2026), BO n° 14 du 2 avril 2026, NOR MENE2602914A, annexe pages 333 à 345 du [PDF du BO]({programme['bo_pdf']}). La matrice officielle de `seconde-programme.json` rattache {programme['attendus_officiels']} attendus (contenus, capacités, démonstrations, algorithmes, approfondissements, vocabulaire, algorithmique et 30 capacités d’automatismes) à des lieux du livre, tous contrôlés dans les sources.

Écarts corrigés :
- Tableaux : la commande de filet supérieur était mangée par un échappement Python ; « oprule » s’affichait à la place du filet dans les tableaux de 14 pages (19 occurrences). Corrigé, et contrôle ajouté à la construction et au PDF.
- Automatismes (partie transversale) : aucune ressource dédiée hors des bilans. Ajout de quatre séries de questions flash corrigées (40 questions, 30 capacités couvertes).
- Algorithmique : affectation notée par une flèche et passage langage naturel / Python (cours 15, ex. 15.1) ; première puissance inférieure à un seuil (15.6) ; écriture d’une fonction aléatoire (15.10) ; atelier de filtres réécrit avec deux listes et une fréquence conditionnelle.
- Vocabulaire ensembliste et logique : réunion, intersection, complémentaire (notations barre et E privé de A), Card, proposition (cours 16, ex. 16.1).
- Fonctions affines : taux d’accroissement, signe et tableau de signes (cours 6, ex. 7.1).
- Comparaison multiplicative par quotient (cours 4, ex. 3.10) ; vecteurs : représentants, vecteur position, base orthonormée (cours 8) ; notation Card dans les probabilités conditionnelles (cours 14).
- Notations hors programme retirées : partie entière (cours 1) et partie entière supérieure (cours 12) ; vocabulaire « paire / impaire » des fonctions (cours 6). Remarque sur la notation officielle des intervalles avec virgule (cours 2).
- Chaîne : gabarit de charte figé dans `livre-seconde/gabarit` ; la construction ne lit plus `livre-premiere`.

Version précédente archivée : `output/archives/optitab-seconde-complet-avant-audit-2026-10-23.pdf`.

Les [ressources Éduscol](https://eduscol.education.gouv.fr/6858/accompagner-les-eleves-en-mathematiques-4e-3e-et-2de) ont servi à vérifier la variété des tâches et la place du raisonnement. Deux exercices utilisent des données Insee avec source, date et champ précis ; les autres données sont construites. Les exercices sont originaux. Sources consultées le 21 octobre 2026 ; programme officiel relu le 23 octobre 2026.

## Calculs et pédagogie

240 groupes de contrôles concernent les exercices de chapitre : calculs exacts ou symboliques, énumérations et cas limites. {extra['groupes_de_controles']} groupes supplémentaires contrôlent les défis, les bilans et les questions flash. Les programmes exécutables, y compris celui du cours 15, sont exécutés et leurs fonctions testées ; la boucle volontairement erronée de l’exercice 15.13 est analysée sans être exécutée.

Les domaines, conditions de division, signes, bornes et unités sont explicités. Les preuves ont été relues ; les tests finis ne constituent pas une preuve générale automatique du texte. Les estimations par classes et les simulations sont distinguées des résultats exacts. Une seconde passe a ajouté une activité corrigée de lecture de nuage de points et une définition explicite de l’équivalence logique. Les 64 renvois d’exemples de la matrice ont été réexaminés pour pointer vers un exercice pertinent.

## Mise en page

Pagination et renvois stabilisés ; aucun débordement, caractère manquant ou renvoi non résolu dans le journal. Les 480 blocs d’énoncés et de corrigés et les {qa['blocs_annexes']} blocs d’annexes sont contrôlés. Les 207 insertions visuelles restent avec leur texte. Toutes les pages ont été rendues et relues sur planches ; les pages sensibles et figures sont aussi inspectées en détail. Les pages de notes sont intentionnelles.

Empreinte SHA-256 du PDF livré : {digest}.
"""
(OUT/'verification/verification-seconde-complet.md').write_text(report,encoding='utf-8')
for source,name in [
 ('build/verification-contenu.json','seconde-calculs.json'),
 ('build/verification-complements.json','seconde-complements.json'),
 ('build/couverture-programme.json','seconde-programme.json'),
 ('build/qa/controle-pdf.json','seconde-controle-pdf.json'),
 ('build/qa/relecture-visuelle.json','seconde-relecture-visuelle.json'),
 ('manifeste-seconde.json','seconde-manifeste.json')]:
    shutil.copy2(ROOT/source,OUT/'verification'/name)
archive=OUT/'sources/optitab-seconde-complet-sources.zip'
files=[p for p in ROOT.rglob('*') if p.is_file() and 'build' not in p.relative_to(ROOT).parts and p.suffix in ['.tex','.sty','.py','.json','.md','.png']]
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(files):z.write(p,p.relative_to(ROOT.parent))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for p in files:assert z.read(p.relative_to(ROOT.parent).as_posix())==p.read_bytes(),str(p)
assert hashlib.sha256(target.read_bytes()).hexdigest()==digest
print(json.dumps({'pages':qa['pages'],'exercices':256,'chapitres':16,'bilans':2,'pdf':str(target),'sources':str(archive),'sha256':digest},ensure_ascii=True,indent=2))
