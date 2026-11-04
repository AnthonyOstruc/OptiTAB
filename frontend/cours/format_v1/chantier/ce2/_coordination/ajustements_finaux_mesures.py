from commun_redaction import ROOT
import re,json
d=next(ROOT.glob('28_*'));p=d/'exercices.txt';s=p.read_text(encoding='utf-8')
s=s.replace('On donne une pièce ou un billet représentant 5 €.','On donne un billet de 5 €.')
old='Peut-on payer cette somme avec seulement quatre pièces ?';new='Remplace la pièce de 20 c par deux pièces de 10 c. Quelle somme obtiens-tu et combien de pièces utilises-tu ?'
blocks=re.split(r'(^===[ \t]*$)',s,flags=re.M)
for k,b in enumerate(blocks):
 if 'Id: nouveau-5\n' not in b:continue
 b=b.replace(old,new)
 section='## Question 5 : '+new+'\n\n::: methode\nÉchange une pièce contre deux pièces de même valeur totale.\n:::\n\n::: etape Raisonner\n$10+10=20$ centimes : la somme reste 3,75 €. Une pièce est remplacée par deux ; on utilise donc une pièce de plus.\n:::\n\n::: resultat\nToujours 3,75 €, avec 6 pièces.\n:::\n'
 b=re.sub(r'## Question 5 :[\s\S]*?(?=Solution:)',lambda _:section,b)
 a,c=b.split('Solution:',1);c=re.sub(r'^5\. .+', '5. Toujours 3,75 €, avec 6 pièces.',c,flags=re.M);blocks[k]=a+'Solution:'+c
p.write_text(''.join(blocks),encoding='utf-8')
