"""Adaptation initiale et ciblée du constructeur de la collection."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'construire.py'
s=p.read_text(encoding='utf8')
s=s.replace('import json,importlib','import json,importlib,re')
s=s.replace("style.replace('Première · Spécialité','Troisième · Brevet 2027')","style.replace('Première · Spécialité','Quatrième · France')")
s=s.replace('Mathématiques - Troisième - Brevet 2027 - Livre complet','Mathématiques - Quatrième - Livre complet')
s=s.replace('France 2026-2027 : 18 chapitres, 288 exercices corrigés, deux brevets blancs','France 2026-2027 : 18 chapitres, 288 exercices corrigés, deux bilans annuels')
s=s.replace(r'\newcommand{\otDecoalgorithmique}',r'\newcommand{\otDecocalcul}{\otDecoensembles}'+'\n'+r'\newcommand{\otDecostatistiques}{\otDecostatistique}'+'\n'+r'\newcommand{\otDecoalgorithmique}')
old="""        text+='\\\\pagestyle{otMain}\\\\essentiel\\\\fontsize{11}{15}\\\\selectfont\\n'+'\\n\\\\clearpage\\n'.join(c.cours)
        if c.numero==15:
            text+=r'\\phantomsection\\label{cours-pavage}'+'\\n'+visual('pavage','fig-cours-pavage','cours-pavage')
"""
new="""        text+='\\\\pagestyle{otMain}\\\\essentiel\\\\fontsize{11}{15}\\\\selectfont\\n'
        for j,cours in enumerate(c.cours,1):
            if j>1:text+='\\\\clearpage\\n'
            lab=f'cours-{c.numero}-{j}'
            text+='\\\\phantomsection\\\\label{'+lab+'}\\n'
            cours=re.sub(r'@FIG:([^@]+)@',lambda m:visual(m.group(1),'fig-'+lab+'-'+m.group(1),lab),cours)
            text+=cours+'\\n'
"""
assert old in s
s=s.replace(old,new)
s=s.replace(".replace('Deux sujets blancs originaux','Deux brevets blancs originaux')",".replace('Deux sujets blancs originaux','Deux bilans annuels originaux')")
s=s.replace('exercices corrigés de Troisième','exercices corrigés de Quatrième')
s=s.replace('Deux brevets blancs originaux permettent de préparer\\n       la session 2027, avec des automatismes et des problèmes rédigés.','Deux bilans annuels originaux permettent de\\n       faire le point, avec des automatismes et des problèmes rédigés.')
s=s.replace("'Réussir sa Troisième'","'Réussir sa Quatrième'")
s=s.replace('288 exercices progressifs et deux brevets blancs corrigés','288 exercices progressifs et deux bilans annuels corrigés')
s=s.replace('Aucun défi n’ajoute une exigence officielle au brevet.','Les défis sont facultatifs et approfondissent les outils du programme.')
start=s.index("    text=edition('bilans-guide'")
end=s.index("    cor=''\n    for b in BILANS:",start)
s=s[:start]+"""    text=edition('bilans-guide','Deux bilans annuels','Sujets originaux · Réviser en reliant les notions','Durée conseillée : 2 heures · Barème d’entraînement sur 20',r'''
Ces évaluations sont des créations du livre pour la Quatrième. Elles n’ont
pas de statut d’examen officiel. Le temps et le barème ci-dessous sont des
repères pour une séance autonome ; ils peuvent être adaptés en classe.
\\editionEtape{Automatismes : environ 20 minutes}
Douze questions courtes, conseillées sans calculatrice : 6 points, soit
0,5 point par réponse. Écrire les étapes utiles, même lorsqu’elles sont brèves.
\\editionEtape{Problèmes : environ 1 h 40}
Quatre problèmes indépendants, calculatrice autorisée : 14 points.
Chaque problème vaut 3,5 points : trois questions à 1 point et 0,5 point
pour la clarté de la rédaction, les unités et les contrôles.
\\editionEtape{Travailler après l’évaluation}
Comparer les démarches, relever les erreurs par notion, puis refaire
les questions utiles sans correction. Un résultat faux peut accompagner
une démarche partiellement juste : identifier précisément l’étape à reprendre.
\\editionEtape{Préparer une autre séance}
Revenir au cours et à deux exercices du chapitre concerné. Le second
bilan peut être fait plus tard pour vérifier que la méthode est devenue disponible.
''','Deux bilans annuels')
"""+s[end:]
s=s.replace("f'Brevet blanc {b.lettre}'","f'Bilan {b.lettre}'").replace("f'Brevet {b.lettre}","f'Bilan {b.lettre}")
s=s.replace('Corrigés des brevets blancs','Corrigés des bilans')
s=s.replace("niveau='Troisième - DNB série générale',session=2027,date='2026-10-21'","niveau='Quatrième - France',annee_scolaire='2026-2027',date='2026-10-22'")
s=s.replace('brevets_blancs=2','bilans_annuels=2').replace('problemes_brevets=8','problemes_bilans=8')
s=s.replace('manifeste-troisieme.json','manifeste-quatrieme.json')
p.write_text(s,encoding='utf8')
# Contrôles de même structure, avec les nouveaux fichiers du volume.
for name in ['controler_pdf.py','verifier_contenu.py']:
    p=ROOT/name;t=p.read_text(encoding='utf8').replace('manifeste-troisieme.json','manifeste-quatrieme.json').replace('brevet-auto','bilan-auto').replace('brevet-probleme','bilan-probleme')
    p.write_text(t,encoding='utf8')
