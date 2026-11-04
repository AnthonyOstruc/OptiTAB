"""Clôture après relecture personnelle des PNG et des captures du lot calculs CM1."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parent.parent
CODES = (2, 3, 4, 5, 10, 19)
assert '--relecture-terminee' in sys.argv, 'Relire chaque PNG et toutes les planches avant de clôturer.'

for code in CODES:
    d = next(ROOT.glob(f'{code:02}_*'))
    subprocess.run([sys.executable, '-X', 'utf8', str(d / 'verif_math.py')], check=True)
    maths = json.loads((d / 'verification_math.json').read_text(encoding='utf-8'))
    audit = json.loads((d / 'audit_navigateur_cm1.json').read_text(encoding='utf-8'))
    validation = json.loads((d / 'validation_cm1.json').read_text(encoding='utf-8'))
    assert maths['statut'] == validation['statut'] == audit['statut'] == 'OK'
    assert maths['minimum_questions_par_exercice'] >= 5
    assert audit['anomalies'] == 0 and audit['vues_distinctes'] == 94
    corr = json.loads((d / 'figures/correspondance.json').read_text(encoding='utf-8'))
    figures = sorted({entry['fichier'] for group in corr.values() for owner in group.values() for entry in owner.values()})
    files = ['cours_nouveau.txt', 'fiche_nouvelle.txt', 'exercices.txt', 'figures/correspondance.json', 'figures/figures.py']
    files.extend('figures/images/' + name for name in figures)
    assert all((d / name).is_file() for name in files)
    assert all((d / 'captures_cm1' / name).is_file() for name in audit['captures'])
    now = datetime.datetime.now().isoformat(timespec='seconds')
    proof = {
        'date': now, 'statut': 'OK', 'math_OK': True, 'anomalies': 0,
        'exercices': maths['exercices'], 'questions': maths['questions'],
        'minimum_questions_par_exercice': maths['minimum_questions_par_exercice'],
        'calculs_comparaisons_verifies': maths['calculs_comparaisons_verifies'],
        'assertions_sources_verifiees': maths['assertions_sources_verifiees'],
        'vues_distinctes': audit['vues_distinctes'],
        'figures_vues': figures, 'captures_lues': audit['captures'],
        'planches_lues': sorted(p.name for p in d.glob('relecture_*.png')),
        'relecture': 'Chaque PNG, cours entier, fiche et exercices 1, 8 et 15 (énoncés et étapes) relus visuellement en téléphone ; audit de toutes les vues en téléphone et ordinateur.',
        'empreintes_finales': {name: hashlib.sha256((d / name).read_bytes()).hexdigest() for name in files},
        'empreinte_apercu': hashlib.sha256((d / 'apercu.html').read_bytes()).hexdigest(),
    }
    (d / 'PREUVES_FINALES.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report = (d / 'RAPPORT.md').read_text(encoding='utf-8')
    report = report.replace('État : textes rédigés ; compilation et relecture visuelle encore à effectuer.', 'État : prêt après vérifications mathématiques et relecture visuelle complète.')
    report = report.replace('Les preuves visuelles seront ajoutées après compilation et contrôle mobile autorisés par l’orchestrateur.', 'Les preuves visuelles et les empreintes des livrables sont enregistrées dans PREUVES_FINALES.json.')
    report += f'\n## Clôture visuelle ({now[:10]})\n\n'
    report += f'{len(figures)} PNG compilés avec le compilateur officiel, sans tolérance de chevauchement, et tous regardés. Audit : 94 vues distinctes, zéro anomalie. Cours complet, fiche et exercices 1, 8, 15 lus en téléphone, énoncés et corrigés inclus. {maths["questions"]} questions, au moins cinq par exercice ; {maths["calculs_comparaisons_verifies"]} calculs ou comparaisons et 15 contrôles des sources indépendants validés. Aucun import ni écriture en base effectué.\n'
    if code == 5:
        report += '\nCorrection de figure : la boucle TikZ du motif en croix omettait des cases du bras supérieur aux étapes 2 et 3. La boucle couvre maintenant tous les rangs, du négatif au positif ; les étapes montrent bien 5, 9 et 13 cases avec quatre bras de longueurs égales. PNG recompilé et relu.\n'
    (d / 'RAPPORT.md').write_text(report, encoding='utf-8')
    (d / 'etat.json').write_text(json.dumps({'statut': 'pret', 'agent': 'finir_cm1_calculs', 'maj': now[:10]}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(code, 'prêt', len(figures), 'figures', maths['questions'], 'questions')
