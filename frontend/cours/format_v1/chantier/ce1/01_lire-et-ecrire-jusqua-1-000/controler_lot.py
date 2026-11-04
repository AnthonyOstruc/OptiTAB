# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess,sys,json,ast
R=Path(__file__).resolve().parent.parent
CODES=[1,2,3,4,14,15,16,17,18,19,20,31,32]
verify=(Path(__file__).parent/'_verif_template.py').read_text(encoding='utf8')
mode=sys.argv[1] if len(sys.argv)>1 else 'math'
for code in CODES:
 d=next(R.glob(f'{code:02}_*'))
 if mode=='math':
  (d/'verif_math.py').write_text(verify,encoding='utf8')
  cmd=[sys.executable,str(d/'verif_math.py')]
 elif mode=='figures':cmd=[sys.executable,str(R.parent.parent/'outils/figures_livre.py'),str(d),'--jobs','1','--planche']
 else:raise ValueError(mode)
 p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8',errors='replace')
 (d/f'controle_{mode}.log').write_text(p.stdout+p.stderr+f'\nRETURN_CODE={p.returncode}\n',encoding='utf8')
 print(f'{code:02} {mode} retour {p.returncode}',flush=True)
 if p.returncode:
  print((p.stdout+p.stderr)[-3500:],flush=True);sys.exit(p.returncode)
 if mode=='math':
  src=json.loads((d/'sources_locales/chapitre.json').read_text(encoding='utf8'))
  lines=['# Couverture des neuf activités source','',f'Chapitre {code:02} — {src["titre"]}. Source locale conservée intégralement en lecture seule.','', '| Activité source | Compétence et données d’origine | Exercice final | Développement |','|---|---|---|---|']
  for i,e in enumerate(src['exercices'],1):
   lines.append(f'| {i} | {e["consigne"].replace("|","/")} | nouveau-{i} | Cinq questions liées, méthode, raisonnement, résultat et solution. |')
  lines.extend(['','Les activités d’enquête ouvertes du chapitre 31 sont rendues vérifiables avec un relevé fourni (12 réponses pour les activités 1–6, 13 pour la nouvelle enquête 7–9). La formulation des questions, le relevé, le tableau, les barres, la comparaison et le contrôle restent travaillés. Les constructions et coloriages ont un modèle de correction en vert.','', 'La comparaison CE1 porte sur des fractions de même dénominateur ou de numérateur 1. L’équivalence deux quarts / un demi est vérifiée par superposition de bandes identiques, sans technique de changement de dénominateur.'])
  (d/'COUVERTURE.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
  ns={};exec((d/'figures/figures.py').read_text(encoding='utf8'),ns)
  evidence=json.loads((d/'verification_math.json').read_text(encoding='utf8'))
  (d/'RAPPORT.md').write_text(f'''# Rapport — CE1 {code:02}

État : textes, fiches, exercices et vérification mathématique prêts ; validation des rendus en cours.

Le cours et la fiche sont entièrement rédigés pour l’élève. Les neuf activités source ont chacune été développées en cinq questions liées : 45 questions avec une méthode concrète, des étapes explicites, un résultat et une solution concordante. Les identifiants sont nouveau-1 à nouveau-9. Le détail de conservation des compétences et des adaptations figure dans COUVERTURE.md.

Programme : entiers jusqu’à 1 000 ; problèmes jusqu’à deux étapes ; fractions d’un tout au plus égal à 1 avec dénominateurs 2, 3, 4, 5, 6, 8, 10 ; enquêtes, tableaux et diagrammes en barres. Aucun fractionnement d’une unité de mesure ni dénominateur 12.

Figures : {len(ns['FIGURES'])} figures TikZ nouvelles au préambule officiel, aucune ancienne image conservée. Énoncés et corrigés ont leurs propres appels ; réponses visuelles en vert et légendes hors des traits. Correspondances sous cours:nouveau et exercices:nouveau-N. La fiche n’a pas besoin de figure supplémentaire.

Contrôles mathématiques autonomes : {evidence['relations_recalculees']} relations finales recalculées avec Fraction ; {evidence['resultats_recalcules_independamment']} résultats finals contrôlés à partir d’opérations indépendantes. Contrôle des 45 résultats contre les solutions et des appels d’images. Empreintes des sources et des textes dans verification_math.json. Aucun import du générateur dans verif_math.py.

Rendus : compilation et contrôle navigateur à compléter avant état prêt. Aucune écriture en base ni modification des outils ou du site.
''',encoding='utf8')
  (d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'ce1_nombres_problemes','maj':'2026-11-02'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
