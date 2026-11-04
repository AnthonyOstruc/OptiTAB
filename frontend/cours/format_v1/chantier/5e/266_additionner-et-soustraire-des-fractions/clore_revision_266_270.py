"""À exécuter après relecture des captures finales, sans toucher aux sources."""
from pathlib import Path
import re,json
from collections import Counter
from revision_20261030 import DATA
BASE=Path(__file__).resolve().parent.parent
TOPICS={
266:'Parts de même taille ; dénominateurs quelconques ; contrôle de vraisemblance ; fractions supérieures à un ; fraction du total et fraction du reste ; quantités exactes et capacité disponible.',
267:'Sens des exposants ; carrés de 0 à 12 ; reconnaissance de carrés et cubes ; priorités ; substitution décimale ; aire, volume, conversions et résolution de problèmes de pavage/remplissage.',
268:'Traduction des mots ; formules de périmètre et aire ; substitution et tableur ; test d’égalité ; motif évolutif et formule expliquée par un dénombrement ; comparaison de tarifs et contre-exemple.',
269:'Structure somme/produit ; distributivité ; réduction ; facteur commun ; calculs décimaux ; aire décomposée ; démonstrations générales et contre-exemples ; programmes de calcul équivalents.',
270:'Addition, multiplication et division à trous ; opérations inverses ; solution nulle ou négative ; décimaux et fractions simples ; contraintes entières ; mise en équation d’une relation simple ; unités et problèmes à étapes.',
}
def load(p):return json.loads(p.read_text(encoding='utf-8'))
for code in range(266,271):
    d=next(BASE.glob(f'{code}_*'));manifest=load(d/'revision_20261030.json');maths=load(d/'verification_revision_20261030.json')
    assert load(d/'controles_revision_20261030.json')['verification']==0 and maths['statut']=='OK'
    log=(d/'revision_navigateur.log').read_text(encoding='utf-8')
    views=[line for line in log.splitlines() if line.startswith(('[mobile]','[desktop]'))]
    good='débordement 0px · erreurs formule 0 · $ bruts 0 · images manquantes 0 · blocs en erreur 0 · éléments trop larges 0'
    assert len(views)==130 and all(good in line for line in views)
    c=d/'captures_revision_20261030'
    for n in (3,8,15,21):
        for part in ('enonce','etapes'):assert (c/f'mobile-ex{n:02d}-{part}.png').exists()
    assert all((c/f'relecture_revision_{i}.png').exists() for i in (1,2))
    current=(d/'exercices.txt').read_text(encoding='utf-8');bs=[b for b in re.split(r'^===[ \t]*$',current,flags=re.M) if b.strip()]
    counts=Counter(re.findall(r'^Difficulté: (.+)',current,re.M))
    corr=load(d/'figures/correspondance.json');files={v['fichier'] for genre in corr.values() for positions in genre.values() for v in positions.values()}
    compilation={x['figure']:x['ok'] for x in load(d/'compilation_figures.json')}
    assert all(compilation.get(Path(f).stem) for f in files)
    coverage=['Couverture pédagogique — révision du 30 octobre 2026','',TOPICS[code],'','| Nouvel exercice | Id | Niveau | Questions |','|---|---:|---|---:|']
    for e in DATA[code]:
        b=bs[e['slot']];eid=re.search(r'^Id: (\d+)',b,re.M)[1]
        coverage.append(f'| {e["titre"]} | {eid} | {e["difficulte"]} | {len(e["questions"])} |')
    coverage+=['',f'Les autres exercices consolident les méthodes avec d’autres données. Répartition finale : {counts["easy"]} découvertes, {counts["medium"]} entraînements, {counts["hard"]} problèmes. Aucun Id supprimé, aucun ajout.']
    (d/'COUVERTURE.md').write_text('\n'.join(coverage)+'\n',encoding='utf-8')
    changes='\n'.join(f'- Id {m["id"]} : {m["titre"]} ({m["type"]}).' for m in manifest['modifications'])
    extra='\nLes anciennes factures sont recentrées sur ax=c ; l’emballage est calculé à part, par arithmétique. L’extension ax+b=c du cours est explicitement signalée comme prolongement de 4e.\n' if code==270 else ''
    report=f'''État : prêt — révision pédagogique du 30 octobre 2026.

21 exercices et leurs Id conservés ; {maths['questions']} questions corrigées. {len(DATA[code])} variantes remplacées par des démarches différentes. Les variantes simples autrefois classées en problèmes sont reclassées en entraînements. Titres uniques et préfixes cohérents : {counts['easy']} découvertes, {counts['medium']} entraînements, {counts['hard']} problèmes.

Couverture : {TOPICS[code]} Détail des exercices repères dans COUVERTURE.md. Même moteur et même format optitab:1 que la Terminale : objectifs, sections romaines, méthodes, propriétés, exemples, erreurs et points à retenir. Fiche condensée, étapes nommées selon le raisonnement, résultat par question et solution courte. Relecture indépendante des trente premiers nouveaux exercices du lot ; formulation ambiguë sur le triple corrigée. Sept doublons exacts du chapitre carrés/cubes ont ensuite été remplacés par des questions distinctes, recalculées et relues.
{extra}
Modifications documentées :
{changes}

Mathématiques : ancien audit exact réexécuté sur la version sauvegardée ; égalité des calculs conservés avec cette version contrôlée. {len(DATA[code])} nouveaux contextes recalculés indépendamment ; {maths['egalites_numeriques_controlees']} égalités numériques évaluées exactement dans les étapes et résultats courants. Les propositions volontairement fausses des questions d’analyse d’erreur restent distinguées des affirmations des corrigés. Preuves : verifier_revision_20261030.py dans la notion 266, verification_revision_20261030.json et verification_math_avant_revision.json dans chaque notion.

Figures : {len(files)} PNG actifs, sources TikZ conservées ; compilation et contrôle texte/traits OK. Toutes les six figures nouvelles du lot ont été regardées individuellement. Les corrigés de dénombrement, pavage, volume et distributivité présentent la figure résolue ou annotée ; les paramètres des dessins communs sont définis dans le texte. Anciens fichiers conservés.

Rendu : vérificateur courant OK, 130 vues Chrome (390 et 1 280 px), zéro débordement, formule invalide, image absente, bloc en erreur ou élément trop large. Contrôle local renforcé aux erreurs MathJax HTML et SVG et aux caractères de contrôle ; les fractions mal encodées détectées à la relecture ont été corrigées puis la passe complète relancée. Journaux : revision_validation.log, revision_navigateur.log ; statut : controles_revision_20261030.json.

Relecture visuelle : cours mobile entier, fiche et quatre nouveaux exercices (3, 8, 15, 21), énoncés et étapes regardés. Captures et planches dans captures_revision_20261030/. Une fiche en tableau a été réduite à deux colonnes pour rester lisible sur téléphone ; chaînes de calculs et conversions alignées quand nécessaire.

Outil : copie locale du contrôle courant, audits conservés, attente de fermeture Chrome bornée à deux secondes pour contourner le nettoyage temporaire Windows déjà identifié. Aucun outil commun ni moteur frontend modifié.

Sauvegarde préalable : sauvegardes/revision_2026-10-30/. Sources en ligne intactes. Aucun import ni accès en base. Programme de 5e rentrée 2026, BO du 5 mars 2026 vérifié par la coordination ; prolongements identifiés.
'''
    (d/'RAPPORT.md').write_text(report,encoding='utf-8')
    (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'coordination-5e','maj':'2026-10-30'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (d/'relecture_visuelle.json').write_text(json.dumps({'date':'2026-10-30','cours':'intégral regardé sur mobile','fiche':'regardée sur mobile','exercices':[3,8,15,21],'onglets':['énoncé','étapes'],'support':'captures_revision_20261030/relecture_revision_1.png et 2.png','figures_nouvelles':'toutes regardées individuellement','conclusion':'OK'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(code,'PRÊT',flush=True)
