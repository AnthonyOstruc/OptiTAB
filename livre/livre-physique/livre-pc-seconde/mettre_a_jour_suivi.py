from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
q=json.loads((ROOT/'recherches/verification-pdf.json').read_text(encoding='utf-8'))
ncontroles=json.loads((ROOT/'recherches/verification-contenu.json').read_text(encoding='utf-8'))['controles']
p=ROOT.parent.parent/'SUIVI-LIVRES.md';s=p.read_text(encoding='utf-8')
lines=s.splitlines();found=0
for i,line in enumerate(lines):
    if line.startswith('| Physique-chimie — Seconde |'):
        cells=line.split('|');validation=cells[4]
        cells[2]=' `livre-pc-seconde/` ';cells[3]=' ✅ Terminé '
        cells[5]=f' Livré le 25/10/2026 — {q["pages"]} pages, programme BO 2019 vérifié sur Éduscol en 2026 ; 20 chapitres, 240 exercices corrigés, 20 défis avec indications, 6 évaluations de 90 min avec barèmes, 4 ateliers numériques ; 48 sources de figures et {q["insertions_figures"]} insertions dans le cours, les énoncés et les solutions ; {ncontroles} contrôles de contenu, relecture des pages et contrôles de débordement ; PDF classé et copie du Bureau identiques '
        assert cells[4]==validation
        lines[i]='|'.join(cells);found+=1
assert found==1
s='\n'.join(lines)+'\n'
s=s.replace('Dernière mise à jour : 24 octobre 2026','Dernière mise à jour : 25 octobre 2026')
s=s.replace('## Ce qui reste (au 24/10/2026)','## Ce qui reste (au 25/10/2026)')
new=f'**Physique-chimie Seconde générale et technologique livrée** le 25/10/2026 ({q["pages"]} pages ; 20 chapitres, 240 exercices, 20 défis et six évaluations corrigés ; programme, calculs, schémas et mise en page contrôlés ; PDF classé et copie du Bureau identiques).\n\n'
if '**Physique-chimie Seconde générale et technologique livrée**' not in s:
    s=s.replace('**Physique-chimie Première spécialité livrée**',new+'**Physique-chimie Première spécialité livrée**',1)
stats={}
for key,start,end in [('Mathématiques','# 1. MATHÉMATIQUES','# 2.'),('Physique-chimie','# 2. PHYSIQUE','# 3.')]:
    text=s.split(start,1)[1].split(end,1)[0]
    counts=[0,0,0]
    for line in text.splitlines():
        cells=line.split('|')
        if len(cells)<7:continue
        statut=cells[3].strip()
        if statut.startswith('✅'):counts[0]+=1
        elif statut.startswith('🟧'):counts[1]+=1
        elif statut.startswith('⬜'):counts[2]+=1
    stats[key]=counts
    pattern=r'^\| '+re.escape(key)+r' \|.*$'
    s=re.sub(pattern,'| '+key+' | '+' | '.join(str(x) for x in counts)+' | **'+str(sum(counts))+'** |',s,count=1,flags=re.M)
totals=[sum(v[i] for v in stats.values()) for i in range(3)]
s=re.sub(r'^\| \*\*Total\*\* \|.*$', '| **Total** | '+' | '.join('**'+str(x)+'**' for x in totals)+' | **'+str(sum(totals))+'** |',s,count=1,flags=re.M)
s=s.replace('**Physique-chimie à faire (19)**','**Physique-chimie à faire ('+str(stats['Physique-chimie'][2])+')**')
s=s.replace('   - Seconde (1) ;\n','')
p.write_text(s,encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False))
