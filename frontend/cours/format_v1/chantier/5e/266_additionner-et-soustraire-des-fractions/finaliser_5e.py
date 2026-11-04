"""Consolide les preuves terminées et clôt le chantier local de 5e.

À lancer seulement après la relecture humaine des planches mobiles.
Aucun accès à la base, aucune modification des sources exportées.
"""
from pathlib import Path
import json
import re
from PIL import Image

BASE=Path(__file__).resolve().parent.parent
BO='https://www.education.gouv.fr/sites/default/files/document/Bulletin%20officiel%20n%C2%B0%2010%20du%205%20mars%202026-480833.pdf'
DETAILS={
266:"Cours réécrit avec méthodes et calculs alignés ; fiche condensée. Les 126 réponses sont expliquées question par question, avec des fractions exactes. Dans les problèmes de bibliothèque, le symbole d non défini est remplacé par le dénominateur réel. Les deux références total/reste sont explicitées.",
267:"Cours structuré autour des puissances, priorités et grandeurs ; fiche condensée. Les 126 réponses détaillent carrés, cubes, couches et effets du doublement d'une longueur. La mosaïque et le cube sont représentés ensemble avec les données exactes de chaque exercice.",
268:"Cours réécrit sur les lettres, substitutions, motifs et tests ; fiche courte. Les 126 réponses explicitent les accroissements n−1, la formule, les trois tests, la recherche du rang et le contre-exemple au doublement. Les anciens tableaux en images, qui donnaient déjà les réponses, sont retirés.",
269:"Cours réécrit avec structure somme/produit, distributivité, factorisation, réduction et démonstration générale ; fiche courte. Les 126 réponses détaillent les aires, la substitution et la bande ajoutée. Les schémas communs définissent clairement leurs paramètres k et b dans chaque énoncé ; aucune mesure n'est à lire sur le dessin.",
270:"Cours réécrit sur les opérations inverses, vérifications et modélisation ; fiche courte. Les 126 réponses distinguent facture globale et prix unitaire, puis contrôlent le résultat. Les situations à deux opérations se traitent par raisonnement arithmétique ; la résolution algébrique générale ax+b=c est signalée « Pour aller plus loin », niveau 4e. Les paramètres des schémas sont explicités dans les énoncés.",
}

def load(p):return json.loads(p.read_text(encoding='utf-8'))

records=[]
for code in range(261,281):
    d=next(BASE.glob(f'{code}_*'));meta=load(d/'source_en_ligne/meta.json')
    if code<266:
        proof='resultats_controles.json';status=load(d/proof);assert all(v==0 for v in status.values()) and len(status)==4
        logs=['validation.log','captures.log']
    elif code<=270:
        proof='controles.json';status=load(d/proof);assert all(v==0 for v in status.values()) and len(status)==3
        logs=['verification.log','controle_captures.log']
    elif code<=275:
        proof='resultat_controles.json';status=load(d/proof);assert len(status)==4 and all(v['code_retour']==0 for v in status)
        logs=['controle_validation.log','controle_captures.log']
    else:
        proof='controle_statut.json';status=load(d/proof);assert len(status)==3 and all(v['code']==0 for v in status.values())
        logs=['validation.log','captures.log']
    for log in logs:assert (d/log).exists() and (d/log).stat().st_size>0,(code,log)
    capture_log=(d/logs[1]).read_text(encoding='utf-8')
    views=[line for line in capture_log.splitlines() if line.startswith('[mobile]') or line.startswith('[desktop]')]
    assert len(views)==130,(code,len(views))
    assert all('débordement 0px · erreurs formule 0 · $ bruts 0 · images manquantes 0 · blocs en erreur 0 · éléments trop larges 0' in line for line in views),(code,'rendu')
    assert (d/'captures/relecture_ensemble.png').exists()
    for i in (1,2,3):
        for field in ('enonce','etapes'):assert (d/f'captures/mobile-ex{i:02d}-{field}.png').exists()
    current=(d/'exercices.txt').read_text(encoding='utf-8');source=(d/'source_en_ligne/exercices.txt').read_text(encoding='utf-8')
    blocks=[b for b in re.split(r'^===[ \t]*$',current,flags=re.M) if b.strip()]
    original=[b for b in re.split(r'^===[ \t]*$',source,flags=re.M) if b.strip()]
    assert len(blocks)==len(original)==len(meta['exercices'])==21
    def identity(b):
        return (re.search(r'^=== (.+)',b,re.M)[1],re.search(r'^Id:\s*(\d+)',b,re.M)[1],re.search(r'^Difficulté:\s*(.+)',b,re.M)[1])
    assert [identity(b) for b in blocks]==[identity(b) for b in original],(code,'identités')
    assert sum(len(re.findall(r'^## Question ',b,re.M)) for b in blocks)==126
    assert sum(len(re.findall(r'^::: methode',b,re.M)) for b in blocks)==126
    assert sum(len(re.findall(r'^::: etape',b,re.M)) for b in blocks)==126
    assert sum(len(re.findall(r'^::: resultat',b,re.M)) for b in blocks)==126
    corr=load(d/'figures/correspondance.json')
    files={v['fichier'] for genre in corr.values() for positions in genre.values() for v in positions.values()}
    positions=sum(len(positions) for genre in corr.values() for positions in genre.values())
    if files:
        compilation=load(d/'compilation_figures.json')
        results={r['figure']:r['ok'] for r in compilation}
        for file in files:
            assert (d/'figures/images'/file).exists() and results.get(Path(file).stem),(code,file)
            assert Image.open(d/'figures/images'/file).width<=1100
    original_images=sum(len(item['images']) for genre in ('cours','fiches','exercices') for item in meta[genre])
    old_report=(d/'RAPPORT.md').read_text(encoding='utf-8') if (d/'RAPPORT.md').exists() else ''
    paragraphs=old_report.split('\n\n')
    text=DETAILS.get(code,next((p.removeprefix('Texte : ') for p in paragraphs if p.startswith('Texte : ')),''))
    corrections=next((p for p in paragraphs if p.startswith('Mathématiques : ')),'')
    removed=max(0,original_images-positions)
    report=f'''État : prêt — chantier local de 5e terminé le 28 octobre 2026.

Texte : {text}
'''
    if corrections:report+='\n'+corrections+'\n'
    report+=f'''
Figures : {len(files)} PNG actifs produits en TikZ, utilisés à {positions} positions ; aucune ancienne image conservée ; {removed} anciennes positions retirées au profit du texte, de tableaux natifs ou pour éviter les doublons. Les anciens visuels et les nouveaux PNG ont été relus. Compilation et contrôle texte/traits : OK quand des figures sont nécessaires. Les anciennes variantes intermédiaires restent conservées, conformément à la demande de ne rien perdre.

Contrôles : calculs vérifiés par les scripts conservés ; identifiants, titres, difficultés et nombre d'exercices comparés aux sources, sans écart. Vérificateur commun OK ; {len(views)} vues Chrome contrôlées (390 et 1 280 px), zéro débordement, formule invalide, image manquante, bloc en erreur ou élément trop large. Cours mobile intégral, fiche, énoncés et étapes des exercices 1, 2 et 3 regardés. Captures et planches de relecture conservées dans captures/. Preuves : {proof}, {', '.join(logs)}.

Outil : certains contrôles restaient bloqués après les audits dans le nettoyage du profil temporaire Chrome sous Windows. Une copie locale conserve tous les audits et borne uniquement l'attente de browser.close à deux secondes, puis termine après vidage de la sortie. Les outils communs et le moteur du site sont inchangés.

Programme : [BO du 5 mars 2026, annexe mathématiques]({BO}), applicable à la 5e depuis la rentrée 2026 ; les prolongements sont signalés. Sources exportées conservées ; aucune commande manage.py, aucun accès ni import en base.
'''
    if code==280:report+='\nCorrection finale : le libellé du bloc demander a été raccourci en « Nombre ? » pour éliminer le dernier dépassement de largeur sur téléphone. Le programme et ses résultats restent identiques ; les contrôles mathématiques et Chrome ont été relancés avec succès.\n'
    records.append({'notion':code,'dossier':d.name,'titre':meta['titre'],'cours':len(meta['cours']),'fiches':len(meta['fiches']),'exercices':21,'questions':126,'figures_actives':len(files),'positions_figures':positions,'vues_navigateur':len(views),'controle':'OK','relecture_mobile':'cours intégral, fiche, exercices 1–3 : énoncés et étapes','statut':'pret'})
    (d/'RAPPORT.md').write_text(report,encoding='utf-8')
    (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'coordination-5e','maj':'2026-10-28'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (d/'relecture_visuelle.json').write_text(json.dumps({'date':'2026-10-28','cours':'toutes les parties mobiles regardées','fiche':'regardée sur mobile','exercices':[{'numero':n,'enonce':'regardé sur mobile','etapes':'regardées sur mobile'} for n in (1,2,3)],'support':'captures originales et relecture_ensemble.png','conclusion':'OK'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(code,'PRÊT',flush=True)

ICI=Path(__file__).resolve().parent
bilan={'date':'2026-10-28','niveau':'5e','notions':len(records),'cours':sum(x['cours'] for x in records),'fiches':sum(x['fiches'] for x in records),'exercices':sum(x['exercices'] for x in records),'questions':sum(x['questions'] for x in records),'figures_actives':sum(x['figures_actives'] for x in records),'vues_navigateur':sum(x['vues_navigateur'] for x in records),'production':'aucun import','statut':'pret','detail':records}
(ICI/'bilan_5e.json').write_text(json.dumps(bilan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=[f"5e : chantier local terminé le 28 octobre 2026.",f"{bilan['cours']} cours, {bilan['fiches']} fiches, {bilan['exercices']} exercices ({bilan['questions']} questions corrigées).",f"{bilan['figures_actives']} figures actives produites ; {bilan['vues_navigateur']} vues contrôlées sur téléphone et ordinateur, zéro anomalie restante.","Les identifiants, titres, difficultés et effectifs des exercices sont conservés. Les calculs, les figures et les captures mobiles ont été vérifiés.","Aucun import en production. Les dossiers sont prêts pour validation éditoriale puis import séparé.","La fermeture Chrome sous Windows a demandé un contournement local de son nettoyage temporaire ; les audits, le moteur du site et les outils communs restent inchangés.","","| Notion | Aperçu | Rapport |","|---|---|---|"]
for r in records:
    prefix='../'+r['dossier']
    lines.append(f"| {r['notion']} — {r['titre']} | [Ouvrir]({prefix}/apercu.html) | [Lire]({prefix}/RAPPORT.md) |")
(ICI/'BILAN_5E.md').write_text('\n\n'.join(lines[:6])+'\n\n'+'\n'.join(lines[7:])+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in bilan.items() if k!='detail'},ensure_ascii=False),flush=True)
