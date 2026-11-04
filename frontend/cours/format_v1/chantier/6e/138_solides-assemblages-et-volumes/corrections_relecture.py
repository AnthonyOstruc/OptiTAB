# -*- coding: utf-8 -*-
"""Corrections ciblées de la relecture finale, sans régénérer le lot."""
from pathlib import Path
import json

R = Path(__file__).resolve().parent.parent
edits = {
139: {
'10 minutes correspondent au nombre 2 ; 30 secondes correspondent au nombre 6.':
'À 10 min 30 s, la grande aiguille a dépassé légèrement le nombre 2 : elle est à mi-chemin entre les graduations de 10 et 11 minutes. La trotteuse pointe le nombre 6, qui correspond à 30 secondes.',
'Grande aiguille : 2 ; trotteuse : 6.':
'Grande aiguille : légèrement après 2 ; trotteuse : 6.',
},
148: {
'Y a-t-il plus de la moitié de 9 ?':
'Plus de la moitié des valeurs de la série sont-elles égales à 9 ?',
},
152: {
'Tester avec l’entrée 6 et repérer l’erreur si on obtient 14.':
'Tester avec l’entrée 6 et proposer une erreur possible si on obtient 14.',
'La séquence proposée respecte l’objectif.':
'Demander un nombre ; lui ajouter 2 ; doubler le résultat ; afficher ce résultat.',
'La sortie 14 correspond à $6\\times2+2$.':
'La sortie 14 peut provenir d’un échange des deux calculs : $6\\times2+2=14$. Ce test seul ne permet pas d’identifier une erreur unique.',
'16 ; une sortie 14 révèle un ordre de calcul incorrect.':
'16. Une erreur possible est de doubler 6 avant d’ajouter 2.',
}}
for n, mapping in edits.items():
    d = next(R.glob(f'{n}_*'))
    p = d/'exercices.txt'
    text = p.read_text(encoding='utf8')
    for before, after in mapping.items():
        assert before in text, (n,before)
        text = text.replace(before,after)
    p.write_text(text,encoding='utf8')
    p = d/'manifest_pedagogique.json'
    data = json.loads(p.read_text(encoding='utf8'))
    def patch(obj):
        if isinstance(obj,str):
            for before,after in mapping.items(): obj=obj.replace(before,after)
            return obj
        if isinstance(obj,list): return [patch(x) for x in obj]
        if isinstance(obj,dict): return {k:patch(v) for k,v in obj.items()}
        return obj
    p.write_text(json.dumps(patch(data),ensure_ascii=False,indent=2),encoding='utf8')
    print(n, 'corrections appliquées')
