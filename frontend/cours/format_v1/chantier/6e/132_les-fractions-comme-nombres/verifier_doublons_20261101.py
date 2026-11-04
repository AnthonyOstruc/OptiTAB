"""Régression : cinq scénarios, aucune perte d'identifiant ni autre bloc altéré."""
from pathlib import Path
from fractions import Fraction as F
import json,re,hashlib
HERE=Path(__file__).resolve().parent
changed={132:{3279,3286,3287,3292},134:{3376}}
checks=0
def check(v):
    global checks
    checks+=1
    assert v
check(F(5,8)<F(7,8)<1)
check(F(5,8)+F(3,8)==1)
check(F(12,3)==4 and 5*4==20 and 20-12==2*4==8)
check(F(2,4)==F(4,8)==F(1,2))
check(F(1,2)*2==1 and F(1,2)*2==2*F(1,2))
check(F(10,10)==1 and F(13,10)==F('1.3') and F(17,10)==F('1.7'))
check(1<F(13,10)<2 and 17-13==4 and F(4,10)==F('0.4'))
check(F(450,6)==75 and 450*2==900 and 1000-900==100)
check(13*75==975<=1000<1050==14*75)
check(1000-975==25 and 75-25==50)
for n,ids in changed.items():
    d=next(HERE.parent.glob(str(n)+'_*'))
    records=json.loads((d/'revision_20261030.json').read_text(encoding='utf-8'))
    before=json.loads((d/'sauvegardes/correction_doublons_2026-11-01/revision_20261030.json').read_text(encoding='utf-8'))
    check([e['id'] for e in records]==[e['id'] for e in before])
    check(all(a==b for a,b in zip(records,before) if a['id'] not in ids))
    check(len(set(e['titre'] for e in records))==len(records))
    check(len(set(e['introduction']+' '.join(q['question'] for q in e['questions']) for e in records))==len(records))
    def blocks(t):
        return {int(re.search(r'^Id: (\d+)',b,re.M)[1]):b for b in re.split(r'^===[ \t]*$',t,flags=re.M) if re.search(r'^Id: ',b,re.M)}
    actual=blocks((d/'exercices.txt').read_text(encoding='utf-8'))
    old=blocks((d/'sauvegardes/correction_doublons_2026-11-01/exercices.txt').read_text(encoding='utf-8'))
    check(list(actual)==list(old))
    check(all(actual[i]==old[i] for i in old if i not in ids))
    for eid in ids:
        record=next(e for e in records if e['id']==eid)
        check(record['introduction'] in actual[eid])
        for q in record['questions']:
            check(q['question'] in actual[eid] and q['reponse'] in actual[eid])
            check(all(body in actual[eid] for title,body in q['etapes']))
    print(n,len(records),'blocs, autres blocs strictement inchangés')
proof=dict(date='2026-11-01',statut='OK',controles=checks,erreurs=[],identifiants_modifies={n:sorted(ids) for n,ids in changed.items()})
(HERE/'verification_doublons_20261101.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf-8')
print(checks,'contrôles de régression OK')
