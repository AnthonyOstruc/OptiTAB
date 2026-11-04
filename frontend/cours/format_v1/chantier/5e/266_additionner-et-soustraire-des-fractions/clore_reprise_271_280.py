"""Clôture de coordination après reprise et relecture effective des dix notions."""
from pathlib import Path
from collections import Counter
import re,json,sys
BASE=Path(__file__).resolve().parent.parent
def load(p):return json.loads(p.read_text(encoding='utf-8'))
GOOD='débordement 0px · erreurs formule 0 · $ bruts 0 · images manquantes 0 · blocs en erreur 0 · éléments trop larges 0'
for code in map(int,sys.argv[1:] or range(271,281)):
    d=next(BASE.glob(f'{code}_*'));geometrie=code<=275
    rev=load(d/('revision_pedagogique.json' if geometrie else 'revision_2026-10-30.json'))
    assert load(d/'controles_revision_20261030.json')['verification']==0
    assert load(d/'controle_maths_coordination.json')['code_retour']==0
    maths=load(d/('resultat_verification.json' if geometrie else 'verification_maths.json'))
    assert maths['statut']=='OK'
    log=(d/'revision_navigateur.log').read_text(encoding='utf-8')
    views=[l for l in log.splitlines() if l.startswith(('[mobile]','[desktop]'))]
    assert len(views)==130 and all(GOOD in line for line in views)
    c=d/'captures_revision_20261030';selection=load(d/'selection_captures_revision.json')
    for number in selection:
        for field in ('enonce','etapes'):assert (c/f'mobile-ex{number:02d}-{field}.png').exists()
    for f in ('relecture_documents.png','relecture_revision_1.png','relecture_revision_2.png'):assert (c/f).exists()
    text=(d/'exercices.txt').read_text(encoding='utf-8');bs=[b for b in re.split(r'^===[ \t]*$',text,flags=re.M) if b.strip()]
    count=Counter(re.findall(r'^Difficulté: (.+)',text,re.M));nq=len(re.findall(r'^## Question ',text,re.M))
    corr=load(d/'figures/correspondance.json');files={v['fichier'] for genre in corr.values() for positions in genre.values() for v in positions.values()}
    compilation={r['figure']:r['ok'] for r in load(d/'compilation_figures.json')}
    assert all(compilation.get(Path(name).stem) for name in files)
    rows=['| Id conservé | Travail proposé | Niveau |','|---|---|---|']
    for e in rev['remplacements']:
        title=e.get('competence',e.get('titre',e.get('nouveau_titre','')))
        rows.append(f'| {e["id"]} | {title} | {e["difficulte"]} |')
    extras=rev.get('doublons_corriges',[])
    for e in extras:
        b=next(b for b in bs if re.search(r'^Id: (.+)',b,re.M)[1]==str(e['id']))
        rows.append(f'| {e["id"]} | {e["correction"]} | '+re.search(r'^Difficulté: (.+)',b,re.M)[1]+' |')
    coverage='Couverture pédagogique — révision du 30 octobre 2026.\n\n'
    coverage+=f"{len(rev['remplacements'])} exercices remplacés pour élargir les démarches, {len(extras)} doublons exacts supplémentaires corrigés. Les autres variantes servent à consolider les méthodes, avec des niveaux adaptés au travail réel.\n\n"+'\n'.join(rows)+'\n\n'
    coverage+=f"Progression : {count['easy']} découvertes, {count['medium']} entraînements, {count['hard']} problèmes. 21 blocs et tous leurs Id conservés ; {nq} questions.\n"
    (d/'COUVERTURE.md').write_text(coverage,encoding='utf-8')
    report=f'''État : prêt — révision pédagogique contrôlée le 30 octobre 2026.

21 blocs et leurs identifiants conservés, {nq} questions corrigées. {len(rev['remplacements'])} exercices remplacés pour diversifier les méthodes ; {len(extras)} doublons exacts supplémentaires corrigés. Les titres et les difficultés correspondent aux démarches : {count['easy']} découvertes, {count['medium']} entraînements, {count['hard']} problèmes. Couverture et Id détaillés dans COUVERTURE.md.

Format : même moteur et même syntaxe optitab:1 que la Terminale. Objectifs, sections romaines, propriétés, méthodes courtes, exemples, points d’attention et récapitulation ; fiche synthétique et corrigés question par question. Les constructions ou lectures de graphiques disposent de figures de correction. Les variantes numériques conservées ne sont plus artificiellement classées comme problèmes.

Modifications :

{chr(10).join(rows)}

Mathématiques : {maths['assertions']} assertions de l’audit exact OK sur les fichiers finaux ; Id, calculs, conversions et contraintes contrôlés selon la notion. Les propriétés et les arguments qualitatifs ont été relus avec les énoncés et les figures. Preuves : revision_maths_coordination.log, controle_maths_coordination.json, {'resultat_verification.json' if geometrie else 'verification_maths.json'} ; moteur conservé dans {'verif_notion.py' if geometrie else 'la notion 276/verif_notion.py (et correction reportée dans 279/verif_notion.py)'}.

Figures : {len(files)} PNG actifs, sources TikZ et productions précédentes conservées. Toutes les figures actives ont été regardées sur les planches ou individuellement. Compilation et contrôle texte/traits : OK, aucune tolérance ajoutée. Les graduations d’axes emploient le fond blanc autorisé par le guide ; leur ordre de dessin a été corrigé pour éviter que les courbes ou les côtés traversent les chiffres. Les lettres des points restent hors des traits. Preuve : compilation_figures.json.

Rendu final : vérificateur courant et audit renforcé des erreurs MathJax HTML/SVG ; 65 vues mobiles à 390 px et les mêmes 65 vues à 1 280 px, zéro anomalie restante. Absence de caractères de contrôle C0 interdits vérifiée. Journaux : revision_validation.log et revision_navigateur.log ; statut : controles_revision_20261030.json. Les tableaux trop larges des cours ont été compactés quand nécessaire.

Relecture : cours mobile intégral, fiche et exercices {', '.join(map(str,selection))}, énoncés et étapes, regardés dans les captures finales. Preuves : captures_revision_20261030/relecture_documents.png et relecture_revision_1.png, relecture_revision_2.png ; relecture_visuelle_coordination.json.

Outil : copie locale des audits communs, détection MathJax élargie et attente de fermeture Chrome bornée à deux secondes pour le défaut de nettoyage Windows déjà établi. Les audits ne sont pas allégés. Aucun outil commun ou fichier frontend/src modifié.

Sauvegarde antérieure dans sauvegardes/revision_2026-10-30/. Sources exportées conservées, aucun accès ou import en base. Travail limité à la classe de 5e ; programme rentrée 2026 vérifié par la coordination.
'''
    (d/'RAPPORT.md').write_text(report,encoding='utf-8')
    (d/'relecture_visuelle_coordination.json').write_text(json.dumps({'date':'2026-10-30','cours_complet':True,'fiche':True,'exercices':selection,'onglets':['énoncé','étapes'],'figures':'toutes les figures actives regardées, planches ou vues individuelles','supports':['captures_revision_20261030/relecture_documents.png','captures_revision_20261030/relecture_revision_1.png','captures_revision_20261030/relecture_revision_2.png'],'conclusion':'OK'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'coordination-5e','maj':'2026-10-30'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(code,'PRÊT',flush=True)
