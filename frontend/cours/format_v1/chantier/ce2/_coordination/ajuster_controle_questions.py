from commun_redaction import ROOT
for code in [1,2,3,*range(15,24)]:
 p=next(ROOT.glob(f'{code:02}_*'))/'verif_math.py';s=p.read_text(encoding='utf-8')
 old="corrections='\\n'.join(b.split('Étapes:\\n',1)[1] for b in blocks)"
 new=old+"\n# Un intitulé peut citer l’égalité fausse d’un élève : ce sont les raisonnements qui sont affirmés vrais.\ncorrections=re.sub(r'^## Question[^\\n]*','',corrections,flags=re.M)"
 assert old in s
 if new not in s:s=s.replace(old,new)
 p.write_text(s,encoding='utf-8')
