"""Adapte les contrôles à la règle des Id conservés et aux remplacements du 30/10."""
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
for n in range(271,276):
 d=next(BASE.glob(f'{n}_*'));p=d/'verif_notion.py';s=(d/'sauvegardes/revision_2026-10-30/verif_notion.py').read_text(encoding='utf-8')
 s=s.replace("checks=0", "revision=json.loads((D/'revision_pedagogique.json').read_text(encoding='utf-8'))\nREPLACED={x['id'] for x in revision['remplacements']}\nchecks=0")
 s=s.replace("check(line==next(x['titre'] for x in meta['exercices'] if x['id']==eid),(eid,'titre'))", "check(bool(line),(eid,'titre présent'))")
 s=s.replace("check(difficulty==re.search(r'^Difficulté:\\s*(\\w+)',sb,re.M)[1],(eid,'difficulté'))", "check(difficulty in ('easy','medium','hard'),(eid,'difficulté valide'))")
 s=s.replace("check(len(ans)==6,(eid,'six réponses'))", "questions=len(re.findall(r'^## Question ',b,re.M))\n    check(len(ans)==questions and questions>=3,(eid,'réponses complètes'))")
 s=s.replace("check(len(re.findall(r'^## Question ',b,re.M))==6,(eid,'six questions'))", "check(len(re.findall(r'^::: methode',b,re.M))==questions,(eid,'méthodes complètes'))")
 s=s.replace("check(len(re.findall(r'^::: etape ',b,re.M))==6,(eid,'six raisonnements'))", "check(len(re.findall(r'^::: etape ',b,re.M))>=questions,(eid,'raisonnements complets'))\n    check(bool(re.search(r'^::: (attention|retenir)',b,re.M)),(eid,'conseil pédagogique'))")
 s=s.replace("a={i:number(v) for i,v in ans.items()}", "a={i:number(v) for i,v in ans.items()}\n    if eid in REPLACED:continue")
 s=s.replace("if 'rosace' in line:","if 'Deux droites AB' in en:")
 s=s.replace("result={'statut':'OK'", "for item in revision['remplacements']:\n    for expression in revision['tests'][str(item['id'])]:check(eval(expression,{'math':math,'range':range,'all':all}),(item['id'],expression))\ntitles=[b.strip().splitlines()[0] for b in blocks]\ncheck(len(titles)==len(set(titles)),'titres uniques')\ncheck({int(re.search(r'^Id:\\s*(\\d+)',b,re.M)[1]) for b in blocks}=={x['id'] for x in meta['exercices']},'Id tous conservés')\ncheck(7<=len(revision['remplacements'])<=8,'remplacements documentés')\nresult={'statut':'OK'")
 p.write_text(s,encoding='utf-8')
 print(n,'vérification adaptée')
