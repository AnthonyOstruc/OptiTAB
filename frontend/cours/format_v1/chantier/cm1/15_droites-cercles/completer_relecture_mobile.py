"""Derniers ajustements constatés sur les captures mobiles finales."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent.parent
for number in (17,18):
    directory=next(ROOT.glob(f'{number:02}_*'))
    manifest=json.loads((directory/'donnees_questions.json').read_text(encoding='utf-8'))
    text=(directory/'exercices.txt').read_text(encoding='utf-8')
    changes={
        17:{
            (1,4):'Tester la superposition exacte par pliage suivant la droite proposée.',
            (15,2):'Chercher une figure connue possédant plusieurs axes pour tester la phrase.',
            (15,4):'Comparer la phrase aux deux règles : même ligne pour un axe vertical, même colonne pour un axe horizontal.',
        },
        18:{(8,2):'Soustraire le nombre de carrés déjà présents aux six faces d’un cube.'},
    }[number]
    sections=re.split(r'(?=^=== (?:Découverte|Entraînement|Problème) - )',text,flags=re.M)
    for (exercise,question),method in changes.items():
        idx=next(i for i,s in enumerate(sections) if f'Id: nouveau-{exercise}\n' in s)
        manifest[exercise-1]['questions'][question-1]['methode']=method
        pattern=rf'(## Question {question} : .*?\n\n::: methode\n).*?(\n:::)'
        sections[idx],count=re.subn(pattern,lambda m:m[1]+method+m[2],sections[idx],count=1,flags=re.S)
        assert count==1
    text=''.join(sections)
    if number==18:
        old='[IMAGE_2]\n\n1. Quel solide possède six faces carrées ?'
        assert old in text
        text=text.replace(old,'[IMAGE_2]\n\n[IMAGE_3]\n\n[IMAGE_4]\n\n1. Quel solide possède six faces carrées ?',1)
        path=directory/'figures/correspondance.json'
        mapping=json.loads(path.read_text(encoding='utf-8'))
        mapping['exercices']['nouveau-1']['3']=dict(mapping['exercices']['nouveau-2']['1'])
        mapping['exercices']['nouveau-1']['4']=dict(mapping['exercices']['nouveau-3']['1'])
        path.write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (directory/'donnees_questions.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (directory/'exercices.txt').write_text(text,encoding='utf-8')
