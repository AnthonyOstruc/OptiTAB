from commun_redaction import ROOT
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent)) if False else None
fixes={27:[('On n’introduit pas ici l’écriture à virgule des longueurs ou des contenances.','Cette décomposition conserve les litres entiers et les centilitres restants.'),('$100:25=4$','$100'+chr(92)+'div25=4$')],28:[('L’écriture à virgule est ici utilisée pour la monnaie, sans vocabulaire de fractions décimales.','Vérifier les deux chiffres après la virgule : 05 désigne 5 centimes et 50 désigne 50 centimes.')],31:[('seuls vingt minutes','seules vingt minutes')]}
for code,pairs in fixes.items():
 d=next(ROOT.glob(f'{code:02}_*'))
 for file in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt']:
  p=d/file;s=p.read_text(encoding='utf-8')
  for old,new in pairs:s=s.replace(old,new)
  p.write_text(s,encoding='utf-8')
d=next(ROOT.glob('29_*'));p=d/'cours_nouveau.txt';s=p.read_text(encoding='utf-8');B=chr(92)
def col(a,b,op,total):return '$$'+B+'begin{array}{r}'+a+B+B+op+b+B+B+B+'hline '+total+B+'end{array}$$'
s=s.replace('Le total est 19,86 €.','Le total est 19,86 €.\n\n'+col('4{,}56','15{,}30','+','19{,}86'))
s=s.replace('Le résultat est 9,26 €.','Le résultat est 9,26 €.\n\n'+col('24{,}56','15{,}30','-','9{,}26'))
p.write_text(s,encoding='utf-8')
