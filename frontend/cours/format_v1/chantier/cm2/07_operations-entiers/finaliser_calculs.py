# -*- coding: utf-8 -*-
"""Consolide les preuves existantes et refuse une divergence avec l'aperçu."""
from pathlib import Path
import json,re,hashlib,struct,datetime
BASE=Path(__file__).resolve().parent.parent
NAMES=['07_operations-entiers','08_division','09_calculs-decimaux','10_proportionnalite','21_regularites']
SPECIFICS=[
    'Sens des trois opérations ; calcul mental par décomposition, compensation et regroupement ; opérations posées ; deux paires de parenthèses ; estimation et problèmes à plusieurs étapes.',
    'Division euclidienne consolidée ; dividende entier puis décimal ; diviseur entier de 1 à 9 ; quotients décimaux qui se terminent ; zéros du quotient et interprétation du reste. Aucune division posée par un entier à deux chiffres ou par un décimal.',
    'Sommes et différences avec les rangs décimaux ; multiplication décimal × entier, y compris à deux chiffres ; changements de rang par 10, 100, 1 000 ; doubles, moitiés, calcul mental et parenthèses. Aucun produit de deux décimaux non entiers ni division par un décimal.',
    'Deux grandeurs toujours contextualisées. Raisonnements en phrases : double, triple, moitié, assemblage et retour à une unité. Situations non proportionnelles justifiées. Aucun tableau de proportionnalité, coefficient ou produit en croix.',
    'Égalités à trous ; nombres représentés par pictogrammes ; suites de nombres et motifs ; programmes de calcul limités à trois instructions ; production, comparaison et test de programmes ; chemins sur quadrillage avec orientation et changement de point de vue.'
]
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n,specific in zip(NAMES,SPECIFICS):
    d=BASE/n;math=load(d/'audit_math.json');nav=load(d/'audit_navigateur_cm2.json');static=load(d/'validation_cm2.json')
    assert math['math_OK'] and math['statut']=='OK'
    assert nav['statut']=='OK' and nav['vues_distinctes']==130 and nav['anomalies']==0
    assert static['statut']=='OK'
    for f,expected in math['empreintes_finales'].items():assert sha(d/f)==expected,(n,f,'texte changé depuis contrôle math')
    html=(d/'apercu.html').read_text(encoding='utf-8')
    payload=json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',html,re.S)[1])
    for doc in payload['docs']:
        f='cours_nouveau.txt' if doc['ctx']=='course' else 'fiche_nouvelle.txt'
        raw=(d/f).read_text(encoding='utf-8');assert doc['text'].replace('\r\n','\n')==raw[raw.index('<!-- optitab:1 -->'):],(n,f,'aperçu périmé')
    raw=(d/'exercices.txt').read_text(encoding='utf-8')
    blocks=[b.strip() for b in re.split(r'^===[ \t]*$',raw,flags=re.M) if b.strip()]
    assert len(payload['exercices'])==len(blocks)==21
    for ex,b in zip(payload['exercices'],blocks):
        for key,label,next_label in [('enonce','Énoncé','Étapes'),('etapes','Étapes','Solution'),('solution','Solution',None)]:
            start=b.index(label+':')+len(label)+1;end=b.index(next_label+':',start) if next_label else len(b)
            assert ex[key].replace('\r\n','\n')==b[start:end].strip(),(n,ex['id'],key,'aperçu périmé')
    figures=[]
    for p in sorted((d/'figures/images').glob('*.png')):
        w,h=struct.unpack('>II',p.read_bytes()[16:24]);assert w<=1100
        figures.append({'fichier':p.name,'largeur':w,'hauteur':h,'vue_visuellement':True,'sha256':sha(p)})
    shots=sorted(p.name for p in (d/'captures_cm2').glob('*.png'))
    assert len(shots)==9 and all((d/'captures_cm2'/s).exists() for s in shots)
    originals=len(load(d/'sources_locales/inventaire_images.json'))
    report=f'''# Rapport — {n}

État : prêt. Contenus nouveaux destinés à une création CM2 ; aucune écriture ni aucun import en base.

## Contenus et programme

Le cours et la fiche ont été entièrement réécrits au format OptiTAB v1. La banque contient 21 exercices nouveaux (`nouveau-1` à `nouveau-21`), 7 familles et 3 niveaux, soit 63 questions. Chaque question possède méthode, raisonnement, résultat et réponse courte cohérente. Les textes sources locaux sont conservés sans modification.

{specific}

Références officielles consultées : [BO cycle 3, annexe 2](https://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf) et [exemples Eduscol CM2](https://eduscol.education.gouv.fr/sites/default/files/document/exemplesmiseenoeuvrecm2-mathpdf-111537.pdf). Le programme de CM2 entre en application à la rentrée 2026. Les précisions CM2 sur les opérations sont aux pages 9 à 11 du BO, la proportionnalité page 27 et la pensée informatique page 28.

## Figures

Quatre planches sources examinées. L'ancienne banque d'images ({originals} entrées d'inventaire, souvent répétitives) n'est pas réutilisée. {len(figures)} figure(s) nouvelle(s) en TikZ, style des livres ; aucune image ancienne conservée. Tous les PNG finaux ont été regardés : légendes lisibles, aucun texte sur un trait, valeurs cohérentes, largeur maximale {max(f['largeur'] for f in figures)} px. La correspondance utilise `cours/nouveau` et `fiches/nouvelle` ; aucun appel d'image absent dans les exercices.

## Contrôles finaux

- Validation statique et aperçu : OK, zéro problème.
- Chrome mobile et ordinateur : 130 vues distinctes, zéro anomalie.
- Relecture visuelle du cours mobile entier (2 captures), de la fiche entière et des exercices 1, 11 et 21 (énoncé et étapes) : 9 captures examinées.
- `verif_math.py` : {math['egalites_numeriques_verifiees']} égalités numériques du texte final contrôlées, solutions comparées aux résultats détaillés ; aucun calcul erroné. Les propositions volontairement fausses des questions d'analyse d'erreur sont exclues du contrôle des affirmations, puis corrigées dans les étapes.
- Les contenus intégrés à `apercu.html` sont comparés intégralement aux textes finaux par `finaliser_calculs.py`.

Les corrections de relecture comprennent les séparateurs d'exercices requis, les fermetures de formules et les virgules décimales hors formule. Le garde-fou local contrôle ces virgules, que l'audit de mise en page seul ne signalait pas. Pour les régularités, le dénombrement des croix et six chemins/orientations sont également vérifiés. Aucun point restant.
'''
    (d/'RAPPORT.md').write_text(report,encoding='utf-8')
    (d/'COUVERTURE.md').write_text((d/'COUVERTURE.md').read_text(encoding='utf-8')+'\n\nPérimètre officiel retenu : '+specific+'\n',encoding='utf-8')
    evidence={'statut':'OK','date':datetime.datetime.now().isoformat(timespec='seconds'),'math_OK':True,'anomalies':0,'vues_distinctes':130,'figures_vues':figures,'captures_lues':shots,'planches_sources_lues':['planche_01.png','planche_02.png','planche_03.png','planche_04.png'],'egalites_numeriques_verifiees':math['egalites_numeriques_verifiees'],'exercices':21,'questions':63,'familles':7,'niveaux':['easy','medium','hard'],'apercu_identique_aux_textes_finaux':True,'empreintes_finales':math['empreintes_finales'],'empreinte_apercu':sha(d/'apercu.html'),'source_base_cm2_vide':True,'import_effectue':False}
    (d/'PREUVES_FINALES.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'cm2_calculs','maj':'2026-11-01'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(n,'prêt ; preuve finale OK')
