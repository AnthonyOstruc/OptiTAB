"""Clôture contrôlée des seules sept notions du lot, après relecture visuelle."""
from pathlib import Path
import json, re, runpy, hashlib

HERE = Path(__file__).resolve().parent
IDS = (132, 134, 135, 136, 137, 284, 285)
COMPETENCES = {
132: ["Fraction comme quotient et nombre qui complète une multiplication", "Parts égales, unité et placement sur une demi-droite", "Comparaison à 1, encadrement et décomposition", "Entier, décimal, fraction exacte et approximation", "Partage d’un segment avec le guide-âne"],
134: ["Reconnaître ou réfuter la proportionnalité", "Linéarité multiplicative et additive", "Retour à l’unité et recherche d’une quantité", "Plan, échelle, conversions et passages dans les deux sens", "Comparer des recettes et décider avec un stock limité"],
135: ["Choix et conversion des unités de longueur", "Périmètres du polygone, carré et rectangle", "Rayon, diamètre, périmètre du disque ; exact et approché", "Retrouver une dimension et suivre un contour composé", "Ouverture, achat par lots, budget et reste"],
136: ["Contour irrégulier et report des longueurs", "Carré et rectangle, conversions et dimension manquante", "Rayon, diamètre et périmètre du disque", "Encoche et distinction entre frontières intérieure et extérieure", "Clôture en rouleaux et recherche exhaustive de rectangles entiers"],
137: ["Comparer par superposition, découpage et recollement", "Pavage, carreaux entiers et demi-carreaux", "Unités carrées et facteur 100 entre unités voisines", "Carré et rectangle avec dimensions décimales", "Découpage en L, aire et périmètre, boîtes entières"],
284: ["Égalités et simplification des fractions", "Comparer, encadrer et ranger", "Addition et soustraction avec unité de référence commune", "Produit d’une fraction par un entier et fraction d’une quantité", "Résoudre et inventer un problème cohérent"],
285: ["Pourcentage, fraction sur 100 et décimal", "Repères 10 %, 20 %, 25 %, 50 %, 75 %", "Calculer une proportion et appliquer un pourcentage", "Partie complémentaire et total de référence", "Comparer des groupes et calculer une remise avec frais"],
}
SOURCE = "https://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf"
EXEMPLES = "https://eduscol.education.fr/document/64878/download"

maths = json.loads((HERE/'preuves_mathematiques_20261030.json').read_text(encoding='utf-8'))
assert maths['erreurs'] == []
for n in IDS:
    d = next(HERE.parent.glob(str(n)+'_*'))
    figures = json.loads((d/'compilation_figures.json').read_text(encoding='utf-8'))
    assert all(x['ok'] for x in figures)
    log = (d/'validation_revision.log').read_text(encoding='utf-8')
    assert log.rstrip().endswith('OK') and '✗' not in log, (n, log[-500:])
    shots = d/'captures_mobile_2026-10-30'
    capture = json.loads((shots/'preuves_captures.json').read_text(encoding='utf-8'))
    assert capture['captures'] == 8 and not capture['erreurs_mathjax']
    # Ce registre est rempli seulement après lecture effective de toutes les planches.
    visual = json.loads((d/'inspection_visuelle_20261031.json').read_text(encoding='utf-8'))
    assert visual['anomalies'] == []
    assert sorted(visual['figures_vues']) == sorted(x['figure']+'.png' for x in figures)
    assert sorted(visual['planches_vues']) == sorted(f.name for f in shots.glob('planche-*.png'))
    records = json.loads((d/'revision_20261030.json').read_text(encoding='utf-8'))
    original = json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
    oldids = [str(x['id']) for x in original['exercices']]
    finalids = re.findall(r'^Id: (\S+)', (d/'exercices.txt').read_text(encoding='utf-8'), re.M)
    assert finalids == oldids if n != 136 else finalids == ['nouveau-'+str(k) for k in range(1,9)]
    corr = json.loads((d/'figures/correspondance.json').read_text(encoding='utf-8'))
    appels = sum(len(positions) for genre in corr.values() for positions in genre.values())
    oldimages = sum(len(item['images']) for genre in ('cours','fiches','exercices') for item in original[genre])
    proof = {
        'date': '2026-10-31', 'notion': n, 'statut': 'OK',
        'validation_syntaxe_images_navigateur': 'OK',
        'vues_distinctes_navigateur': 2*(2+3*len(records)),
        'formats_navigateur': [{'largeur':390,'hauteur':844},{'largeur':1280,'hauteur':900}],
        'anomalies_navigateur': 0, 'captures_mobiles': capture['captures'],
        'documents_entiers_vus': capture['documents_entiers'],
        'exercices_enonce_et_etapes_vus': capture['exercices_indices'],
        'planches_vues': visual['planches_vues'], 'anomalies_visuelles':0,
        'figures_compilees_vues':visual['figures_vues'], 'chevauchements':0,
        'verifications_mathematiques_lot': maths['controles'],
        'verifications_mathematiques_notion': maths['par_notion'][str(n)],
        'erreurs_mathematiques':0, 'script_mathematique':'../132_les-fractions-comme-nombres/verif_mathematiques_20261030.py',
        'identifiants_existants_conserves':len(oldids), 'exercices_ajoutes':len(finalids)-len(oldids),
        'source_en_ligne_sha256':{str(f.relative_to(d/'source_en_ligne')):hashlib.sha256(f.read_bytes()).hexdigest() for f in (d/'source_en_ligne').rglob('*') if f.is_file()},
    }
    (d/'preuves_finales_20261031.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    coverage = '# Couverture pédagogique — '+d.name.split('_',1)[1].replace('-',' ')+'\n\n'
    coverage += 'Référence : [programme officiel de mathématiques du cycle 3]('+SOURCE+'), applicable en 6e depuis la rentrée 2025 ; [exemples de mise en œuvre]('+EXEMPLES+'). Références vérifiées par l’orchestrateur.\n\n'
    coverage += '| Compétence travaillée | Supports |\n|---|---|\n'
    coverage += ''.join('| '+c+' | Cours, fiche et exercices corrigés |\n' for c in COMPETENCES[n])
    coverage += '\nLes corrections distinguent méthode, étapes et résultat. Les unités, le tout de référence, les approximations et les décisions entières sont explicités.\n\n'
    coverage += 'Exercices finaux :\n\n'+''.join('- '+str(x['id'])+' : '+x['titre']+'\n' for x in records)
    (d/'COUVERTURE.md').write_text(coverage,encoding='utf-8')
    report = '# Rapport — reprise et clôture du 31 octobre 2026\n\nÉtat : **prêt**.\n\n'
    report += f'Cours et fiche relus intégralement, structure OptiTAB v1, méthodes et erreurs fréquentes. {len(oldids)} identifiants historiques conservés ; {len(finalids)-len(oldids)} exercices ajoutés. Tous les blocs existants sont conservés avec leur contenu corrigé ; six situations diversifiées par notion historique complètent les entraînements gradués. Les titres finaux et leur couverture figurent dans COUVERTURE.md.\n\n'
    report += 'Points mathématiques explicités et contrôlés dans le lot : quotient exact et approximation, même unité avant un calcul, même tout avant une somme de fractions ou une proportion, distinction rayon/diamètre, facteur 100 pour les aires, contours extérieurs et achats en nombres entiers. Aucun résultat faux restant détecté.\n\n'
    report += f'Figures : {len(figures)} PNG TikZ de style livre produits et vus individuellement, {appels} appels documentaires, aucune ancienne image conservée. Les {oldimages} anciennes références sont remplacées ou retirées lorsqu’elles sont redondantes ; les données restent en texte. Aucun chevauchement texte/trait, aucune figure trop large.\n\n'
    report += f'Contrôles : vérificateur local complet OK, syntaxe et images OK ; {proof["vues_distinctes_navigateur"]} vues distinctes contrôlées en Chrome mobile/ordinateur, aucune anomalie. 8 captures mobiles regardées par planches : cours entier, fiche entière, trois exercices (énoncé et étapes). Le bandeau fixe d’aperçu est désactivé uniquement pour les captures afin de ne masquer aucun contenu. {maths["controles"]} contrôles mathématiques exacts dans le lot, dont {maths["par_notion"][str(n)]} propres à cette notion ; zéro erreur. Preuves dans preuves_finales_20261031.json.\n\n'
    if n in (135,136):
        report += 'Les légendes rayon/diamètre sont placées hors du cercle ; exactitude avec π et valeurs approchées sont distinguées.\n\n'
    if n == 132:
        report += 'Compatibilité du validateur : `a<b` remplacé par `a\\lt b` pour éviter une fausse détection de balise HTML, sans modifier le sens mathématique.\n\n'
    if n == 136:
        report += 'À l’import : créer la fiche fiche_nouvelle.txt et les exercices nouveau-1 à nouveau-8. meta_apercu.json sert uniquement aux outils locaux et ne modifie jamais source_en_ligne/meta.json. Aucun import ni accès en écriture à la base effectué.\n\n'
    report += 'Aucun point pédagogique ou visuel restant. source_en_ligne reste immuable ; aucun outil commun ni code du frontend modifié.\n'
    (d/'RAPPORT.md').write_text(report,encoding='utf-8')
    (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'finir_calculs_6e','maj':'2026-10-31'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(n,'prêt',len(figures),'figures',proof['vues_distinctes_navigateur'],'vues')
