"""Identifie honnêtement le PDF isolé : 12 chapitres, pas un manuel achevé."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'tmp/pdfs/audit-physique-20261024/premiere-sources'
style=ROOT/'optitab-livre.sty';s=style.read_text(encoding='utf-8')
for old,new in [(r'\otNbExosChapitres}{315}',r'\otNbExosChapitres}{180}'),(r'\otNbDefis}{21}',r'\otNbDefis}{12}'),(r'\otNbExosTotal}{336}',r'\otNbExosTotal}{192}'),(r'\otNbSujets}{6}',r'\otNbSujets}{0}')]:s=s.replace(old,new)
style.write_text(s,encoding='utf-8')
p=ROOT/'couverture/premiere.tex';s=p.read_text(encoding='utf-8').replace('Année complète','Chapitres 1 à 12')
p.write_text(s,encoding='utf-8')
p=ROOT/'liminaires/titre.tex';s=p.read_text(encoding='utf-8')
s=s.replace(r'\otNbExosTotal\ exercices progressifs et \otNbSujetsLettres\ devoirs surveillés corrigés',r'180 exercices et 12 défis corrigés · Version en cours de rédaction')
p.write_text(s,encoding='utf-8')
p=ROOT/'liminaires/avant-propos.tex';s=p.read_text(encoding='utf-8')
start=s.index('Il réunit');end=s.index(r'\par\vspace{3.5mm}',start)
s=s[:start]+r'Cette version révisée contient les \textbf{chapitres 1 à 12}, soit 180 exercices et 12 défis corrigés. Le plan complet de 21 chapitres reste visible au sommaire ; les chapitres suivants et les devoirs surveillés sont en cours de rédaction et ne font pas partie de ce PDF.'+s[end:]
p.write_text(s,encoding='utf-8')
p=ROOT/'main.tex';s=p.read_text(encoding='utf-8').replace('Physique-Chimie - Première spécialité - Livre complet','Physique-Chimie - Première spécialité - Chapitres 1 à 12')
p.write_text(s,encoding='utf-8')
print('Version partielle identifiée ; sources du livre en construction préservées.')
