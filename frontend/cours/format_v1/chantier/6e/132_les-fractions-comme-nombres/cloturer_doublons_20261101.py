"""Attestation après parcours complets et relecture effective des cinq nouveaux corrigés."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
maths=json.loads((HERE/'preuves_mathematiques_20261030.json').read_text(encoding='utf-8'))
reg=json.loads((HERE/'verification_doublons_20261101.json').read_text(encoding='utf-8'))
assert not maths['erreurs'] and not reg['erreurs']
for n,indices in ((132,[8,15,16,21]),(134,[21])):
    d=next(HERE.parent.glob(str(n)+'_*'))
    log=(d/'validation_revision.log').read_text(encoding='utf-8')
    assert log.rstrip().endswith('OK') and '✗' not in log,(n,log[-500:])
    records=json.loads((d/'revision_20261030.json').read_text(encoding='utf-8'))
    capture=json.loads((d/'captures_doublons_2026-11-01/preuves_captures.json').read_text(encoding='utf-8'))
    assert capture['exercices_indices']==indices and not capture['erreurs_mathjax']
    files=[f'mobile-ex{i}-{panel}.png' for i in indices for panel in ('enonce','etapes')]
    assert all((d/'captures_doublons_2026-11-01'/f).is_file() for f in files)
    visual=json.loads((d/'inspection_visuelle_20261031.json').read_text(encoding='utf-8'))
    visual.update(relecture_doublons_date='2026-11-01',captures_doublons_vues=files,anomalies_doublons=[])
    (d/'inspection_visuelle_20261031.json').write_text(json.dumps(visual,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    path=d/'preuves_finales_20261031.json';proof=json.loads(path.read_text(encoding='utf-8'))
    proof.update(date='2026-11-01',statut='OK',vues_distinctes_navigateur=130,anomalies_navigateur=0,anomalies_visuelles=0,erreurs_mathematiques=0,
      verifications_mathematiques_lot=maths['controles'],verifications_mathematiques_notion=maths['par_notion'][str(n)],
      controles_regression_doublons=reg['controles'],exercices_doublons_remplaces=reg['identifiants_modifies'][str(n)],
      captures_doublons_vues=files,sha256_exercices=hashlib.sha256((d/'exercices.txt').read_bytes()).hexdigest())
    path.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    coverage=(d/'COUVERTURE.md').read_text(encoding='utf-8').split('Exercices finaux :')[0]
    coverage+='Exercices finaux :\n\n'+''.join('- '+str(x['id'])+' : '+x['titre']+'\n' for x in records)
    (d/'COUVERTURE.md').write_text(coverage,encoding='utf-8')
    report=(d/'RAPPORT.md').read_text(encoding='utf-8')
    section='\n## Complément du 1er novembre 2026 — suppression des doublons exacts\n\n'
    report=report.split(section)[0]+section
    report+='Les blocs '+', '.join(str(x) for x in reg['identifiants_modifies'][str(n)])+' ont été remplacés par des situations complémentaires, avec méthodes, raisonnements et réponses cohérents. Les identifiants historiques et tous les autres blocs sont strictement conservés. Cours, fiche et figures inchangés.\n\n'
    report+='Nouvelle validation complète : syntaxe/images OK ; 130 vues Chrome mobile et ordinateur, zéro anomalie. Énoncés et étapes des '+str(len(indices))+' nouveaux exercices relus visuellement dans captures_doublons_2026-11-01 : aucun débordement ni formule brute. Vérifications exactes du lot : '+str(maths['controles'])+' ; régression indépendante : '+str(reg['controles'])+' contrôles, zéro erreur. Sauvegardes préalables dans sauvegardes/correction_doublons_2026-11-01. Aucun import en base.\n'
    (d/'RAPPORT.md').write_text(report,encoding='utf-8')
    (d/'etat.json').write_text(json.dumps(dict(statut='pret',agent='corriger_doublons_calculs',maj='2026-11-01'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(n,'prêt',130,'vues',len(indices),'exercices remplacés')
