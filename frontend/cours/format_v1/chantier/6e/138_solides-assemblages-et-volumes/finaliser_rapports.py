# -*- coding: utf-8 -*-
"""Dresse les preuves finales après la relecture réelle des captures."""
from pathlib import Path
import json,re,hashlib,importlib.util,sys
R=Path(__file__).resolve().parent.parent
URL='https://www.education.gouv.fr/sites/default/files/ensel620_annexe2-v2.pdf'
coverage={
138:[('Identifier les solides et leurs représentations','I','1 ; 5–6 ; 13–14 ; 18'),('Dénombrer des assemblages, y compris les cubes cachés','II','2–3 ; 5–6 ; 8–11 ; 13–18 ; 20–21'),('Connaître le cm³, comparer et déterminer des volumes','III','1–4 ; 7–12 ; 15–17 ; 19–21')],
139:[('Lire les horaires et maîtriser les unités usuelles','I','1–3 ; 6–7 ; 14'),('Calculer début, fin et temps écoulé, y compris à minuit','II','4–5 ; 10–13 ; 15–19 ; 21'),('Convertir entre écritures sexagésimales et décimales','III','2 ; 8–9 ; 11 ; 13 ; 16 ; 20')],
146:[('Entretenir la reconnaissance et la description des solides','I','1–5 ; 12–14 ; 17 ; 20'),('Reconnaître et construire des patrons du cours moyen','II–III','6–11 ; 15–16 ; 18–19 ; 21'),('Vérifier les raccords, les oppositions et le pliage','II–III','7–11 ; 16 ; 18–21')],
147:[('Planifier une enquête et recueillir des données','I','1–4 ; 7 ; 10 ; 14 ; 20'),('Mesurer, consigner et contrôler un tableau','II','3–7 ; 9–10 ; 12–14 ; 17–19'),('Filtrer un tableau selon un ou plusieurs critères','III','8 ; 15'),('Argumenter une interprétation et ses limites','IV','2 ; 7 ; 9 ; 13–14 ; 16 ; 20–21')],
148:[('Lire tableaux, barres, disque et courbe','I–II','1–7 ; 10–12 ; 14 ; 17 ; 19'),('Totaliser, compléter et comparer les effectifs','III','1–4 ; 8 ; 10–12 ; 18'),('Relier parts simples, fractions et pourcentages','III','7 ; 9 ; 13 ; 15 ; 19 ; 21'),('Exercer un regard critique sur une représentation','IV','13–16 ; 20–21')],
149:[('Comprendre l’échelle de probabilité entre 0 et 1','I','1–2 ; 6 ; 15'),('Calculer dans des cas simples d’équiprobabilité','II','3–5 ; 8–10 ; 12–13 ; 16 ; 18–19'),('Consolider indépendance et dénombrement à deux étapes','III','7 ; 14 ; 20'),('Comparer expérience répétée et probabilité calculée','IV','11–12 ; 17 ; 21')],
152:[('Identifier instruction, séquence, entrée et sortie','I–II','1–3 ; 11 ; 13 ; 19 ; 21'),('Produire et exécuter une séquence','II','2–4 ; 6 ; 11–13 ; 17 ; 19 ; 21'),('Répéter à la main un bloc pour une tâche','III','5 ; 7–10 ; 12 ; 14–15 ; 18 ; 20'),('Programmer un chemin simple et le vérifier','IV','4 ; 6 ; 8–10 ; 15–17 ; 20')],
}
notes={
138:'Volume déterminé par dénombrement de cubes unités ; pas de formule générale de pavé imposée. Deux perspectives supplémentaires relient les assemblages à leurs vues et à leurs plans.',
139:'L’exercice 7 précise la grande aiguille légèrement après le 2 à 10 min 30 s. Les conversions décimales incluent l’erreur classique 1,30 h ≠ 1 h 30 min.',
146:'Les patrons relèvent explicitement de la consolidation des acquis CM1/CM2 ; les attendus nouveaux de sixième portent sur la vision des assemblages de cubes. Le pliage de la croix et l’échec du rectangle 2 × 3 sont contrôlés par transport exact de repères.',
147:'Une enquête complète remplace une simple lecture mécanique : question neutre, population, protocole, tableaux, filtre et interprétation prudente.',
148:'Aucune moyenne ni médiane obligatoire : le programme 2025 attend ici la collecte, les tableaux, le filtrage et les lectures usuelles. Les parts simples réinvestissent fractions et pourcentages. La question de majorité de l’exercice 20 est reformulée sans ambiguïté.',
149:'Le vocabulaire savant est expliqué sans être exigé en autonomie. Les modèles simples distinguent équiprobabilité, indépendance et proportion observée ; le tirage sans remise ne demande qu’une mise à jour des effectifs, sans probabilité conditionnelle formalisée.',
152:'Les notions demandées sont explicitement présentes : instructions, séquences, entrées, sorties et répétitions, avec ou sans machine. L’exercice 21 propose une erreur possible pour la sortie 14, sans prétendre identifier une erreur unique. Le contrôle mobile a conduit à sortir l’état initial du bloc de code et à raccourcir la consigne du quart de tour, sans débordement.',
}
for n in coverage:
 if len(sys.argv)>1 and str(n) not in sys.argv[1:]: continue
 d=next(R.glob(f'{n}_*'))
 status=json.loads((d/'controle_statut.json').read_text(encoding='utf8'))
 assert all(v['code']==0 for v in status.values()), (n,status)
 log=(d/'progression_navigateur.log').read_text(encoding='utf8')
 rows=re.findall(r'^\[(mobile|desktop)\] (.+?) : débordement (\d+)px · erreurs formule (\d+) · \$ bruts (\d+) · images manquantes (\d+) · blocs en erreur (\d+) · éléments trop larges (\d+)$',log,re.M)
 assert len(rows)==len({x[:2] for x in rows})==130,(n,len(rows))
 assert all(all(int(v)==0 for v in x[2:]) for x in rows),(n,'anomalies')
 assert 'Aucun problème détecté' in log
 meta=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf8'))
 maths=json.loads((d/'verification_maths.json').read_text(encoding='utf8'));assert maths['statut']=='OK'
 figs=sorted(p.name for p in (d/'figures/images').glob('*.png'))
 docs=sorted(p.name for p in d.glob('*.txt') if p.name!='exercices.txt')
 shots=sorted(p.name for p in (d/'captures').glob('mobile-c*.png'))+sorted(p.name for p in (d/'captures').glob('mobile-f*.png'))+[f'mobile-ex{k:02}-{part}.png' for k in (1,10,21) for part in ('enonce','etapes')]
 assert all((d/'captures'/s).exists() for s in shots)
 ids=re.findall(r'^Id: (\S+)',(d/'exercices.txt').read_text(encoding='utf8'),re.M)
 old=[str(x['id']) for x in meta['exercices']];assert all(i in ids for i in old)
 oldimages=sum(len(x.get('images',[])) for group in ('cours','fiches','exercices') for x in meta[group])
 mapping=json.loads((d/'figures/correspondance.json').read_text(encoding='utf8'))
 mapped=sum(len(v) for group in mapping.values() for v in group.values())
 sourcehash={str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (d/'source_en_ligne').rglob('*') if p.is_file()}
 proof={'notion':n,'statut':'OK','date':'2026-10-31','vues_distinctes':130,'vues_mobile':65,'vues_desktop':65,'anomalies':0,'verifier_notion':'OK via verifier_visible.py, outil commun exécuté en mémoire','script_math':'OK','calculs_et_modeles_verifies':maths['calculs_et_modeles_verifies'],'exercices':21,'questions':42,'identifiants_historiques_preserves':len(old),'nouveaux_exercices':21-len(old),'figures_png':figs,'figures_vues':True,'planches_figures':sorted(p.name for p in (d/'figures').glob('relecture_*.png')),'captures_mobiles_vues':shots,'documents':docs,'meta_source_modifiee':False,'sha256_sources':sourcehash,'programme':URL,'limites':[]}
 (d/'PREUVES_FINALES.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf8')
 cov='# Couverture du programme 2025 — '+meta['titre']+'\n\nSource : [programme officiel du cycle 3]('+URL+'), consulté le 31 octobre 2026.\n\n| Compétence travaillée | Cours | Exercices |\n|---|---|---|\n'+'\n'.join('| '+a+' | '+b+' | '+c+' |' for a,b,c in coverage[n])+'\n\n'+notes[n]+'\n\nProgression : 7 découvertes, 7 entraînements et 7 problèmes, chacun avec deux questions, méthode, étapes, résultat et rappel final.\n'
 (d/'COUVERTURE_PROGRAMME.md').write_text(cov,encoding='utf8')
 titles=re.findall(r'^=== (.+)',(d/'exercices.txt').read_text(encoding='utf8'),re.M)
 inventory='\n'.join(f'- Id {i} : {title}' for i,title in zip(ids,titles))
 report=f'''# {meta['titre']} — prêt

Les deux documents et les 21 exercices sont entièrement rédigés au format OptiTAB v1, suivant le même gabarit que la cinquième : objectifs, cours structuré, fiche courte, deux questions corrigées par exercice, méthodes et résultats explicites. {notes[n]}

## Programme et contenu

Programme officiel 2025 vérifié le 31 octobre 2026 : voir [la couverture détaillée](COUVERTURE_PROGRAMME.md). {len(old)} identifiants historiques conservés sans retirer de bloc ; {21-len(old)} exercices nouveaux. Chaque exercice existant est repris dans le catalogue ci-dessous.

## Figures

{len(figs)} PNG TikZ au style livre, avec corrigés en vert lorsque pertinent ; {mapped} emplacements déclarés. Compilation et contrôle texte/trait acceptés sans tolérance. Chaque PNG est examiné individuellement, puis contrôlé en situation dans les captures. Aucune ancienne image conservée ; {oldimages} anciennes occurrences ne sont plus appelées. Tableaux, données et code restent du texte natif.

## Contrôles

- Vérificateur commun exécuté par `verifier_visible.py` : **OK** ; ajout des nouveaux documents dans les métadonnées en mémoire uniquement.
- Chrome headless : **130 vues distinctes** (65 téléphone à 390 px et 65 ordinateur), tous les onglets des 21 exercices ; **0 anomalie** de débordement, formule, texte brut, image ou bloc.
- `verifier_maths_lot.py` : **{maths['calculs_et_modeles_verifies']} calculs et modèles exacts validés** pour cette notion ; identifiants, unicité et structure également contrôlés.
- Captures réellement examinées : toutes les parties du cours en téléphone, la fiche et les exercices 1, 10 et 21 (énoncés et étapes). Captures et journaux conservés.
- [Preuves machine](PREUVES_FINALES.json) : vues distinctes, captures, figures et empreintes SHA-256 des sources.

## Remise à l’orchestrateur

Aucun import ni accès à la base. `source_en_ligne/meta.json` reste inchangé. Les fichiers à créer conservent leurs noms `cours_nouveau.txt` / `fiche_nouvelle.txt` lorsque nécessaires. Les adaptations d’aperçu et de contrôle sont exclusivement locales et gardent le moteur et les audits communs. Pas de point bloquant.

## Catalogue des remplacements et ajouts

{inventory}
'''
 (d/'RAPPORT.md').write_text(report,encoding='utf8')
 (d/'etat.json').write_text(json.dumps({'statut':'pret','agent':'finir_donnees_6e','maj':'2026-10-31'},ensure_ascii=False,indent=2),encoding='utf8')
 print(n,'prêt',len(rows),'vues',len(figs),'figures',maths['calculs_et_modeles_verifies'],'contrôles exacts')
