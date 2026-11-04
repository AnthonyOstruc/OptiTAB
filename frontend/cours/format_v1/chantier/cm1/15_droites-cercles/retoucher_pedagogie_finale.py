"""Précisions pédagogiques de la relecture, sur les seuls livrables finaux."""
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parent.parent
for number in (16,17):
    directory=next(ROOT.glob(f'{number:02}_*'))
    manifest=json.loads((directory/'donnees_questions.json').read_text(encoding='utf-8'))
    text=(directory/'exercices.txt').read_text(encoding='utf-8')
    if number==16:
        sections=re.split(r'(?=^=== (?:Découverte|Entraînement|Problème) - )',text,flags=re.M)
        # Les deux questions sur les côtés demandent le compas et les codes,
        # et non un contrôle d'angle à l'équerre.
        first=next(i for i,s in enumerate(sections) if 'Id: nouveau-1\n' in s)
        for question in (2,3):
            item=manifest[0]['questions'][question-1]
            old=item['methode']
            item['methode']='Comparer les codes de longueur aux définitions des triangles isocèles et équilatéraux.'
            pattern=rf'(## Question {question} : .*?\n\n::: methode\n).*?(\n:::)'
            sections[first],count=re.subn(pattern,lambda m:m[1]+item['methode']+m[2],sections[first],count=1,flags=re.S)
            assert count==1
        text=''.join(sections)
    else:
        old='Un axe peut-il passer par l’intérieur d’une figure sans la partager en parties superposables ?'
        new='Une droite peut-elle passer par l’intérieur d’une figure sans la partager en parties superposables ?'
        assert manifest[1]['questions'][4]['question']==old
        manifest[1]['questions'][4]['question']=new
        text=text.replace(old,new)
    (directory/'donnees_questions.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (directory/'exercices.txt').write_text(text,encoding='utf-8')
