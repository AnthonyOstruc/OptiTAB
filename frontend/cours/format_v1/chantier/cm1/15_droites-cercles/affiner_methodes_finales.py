"""Remplace les méthodes hors sujet repérées à la relecture pédagogique."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent.parent
CHANGES={
17:{
(1,1):'Plier suivant la droite proposée et vérifier la superposition exacte.',
(1,2):'Plier suivant la droite proposée et vérifier la superposition exacte.',
(11,3):'Compter les cases de cette ligne et ajouter leurs images de l’autre côté du pli.',
},
18:{(9,2):'Compter les cubes de l’étage considéré, y compris ceux qui sont cachés.'},
}
for number,changes in CHANGES.items():
    directory=next(ROOT.glob(f'{number:02}_*'))
    manifest=json.loads((directory/'donnees_questions.json').read_text(encoding='utf-8'))
    text=(directory/'exercices.txt').read_text(encoding='utf-8')
    sections=re.split(r'(?=^=== (?:Découverte|Entraînement|Problème) - )',text,flags=re.M)
    for (exercise,question),method in changes.items():
        idx=next(i for i,s in enumerate(sections) if f'Id: nouveau-{exercise}\n' in s)
        manifest[exercise-1]['questions'][question-1]['methode']=method
        pattern=rf'(## Question {question} : .*?\n\n::: methode\n).*?(\n:::)'
        sections[idx],count=re.subn(pattern,lambda m:m[1]+method+m[2],sections[idx],count=1,flags=re.S)
        assert count==1
    text=''.join(sections)
    if number==17:
        old=manifest[1]['contexte']
        new='On étudie un rectangle non carré, un carré et un triangle isocèle non équilatéral. Dessine chacun sur papier, puis vérifie les axes par pliage. Le rectangle ci-dessous donne un premier exemple.'
        assert old in text
        text=text.replace(old,new)
        manifest[1]['contexte']=new
    (directory/'donnees_questions.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (directory/'exercices.txt').write_text(text,encoding='utf-8')
