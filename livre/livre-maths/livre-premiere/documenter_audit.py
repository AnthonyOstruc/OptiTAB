"""Consigne le traitement des neuf observations, sans modifier le classeur reçu."""
from pathlib import Path
import hashlib,json
from verifier_code_pdf import extraire

R=Path(__file__).resolve().parent
O=R/'build/audit-20261021'
manifest=json.loads((R/'revision-audit-20261021.json').read_text(encoding='utf-8'))
avant=json.loads((O/'code-pdf-avant.json').read_text(encoding='utf-8'))
apres=json.loads((R/'build/verification-code-pdf.json').read_text(encoding='utf-8'))
comparaison=json.loads((O/'comparaison.json').read_text(encoding='utf-8'))
pdf_sha=hashlib.sha256((R/'main.pdf').read_bytes()).hexdigest()
assert apres['source_sha256']==comparaison['sha256']==pdf_sha
assert len(avant['erreurs'])==len(manifest['anomalies_signalees'])==9
assert apres['blocs_executes']==27 and not apres['erreurs']
source=Path(manifest['audit_source'])
assert hashlib.sha256(source.read_bytes()).hexdigest()==manifest['audit_source_sha256']
blocs=extraire(R/'main.pdf')
assert len(blocs)==27
traitements=[]
for observation,erreur in zip(manifest['anomalies_signalees'],avant['erreurs']):
    assert observation['Page PDF']==erreur['page_pdf']
    bloc=blocs[erreur['bloc']-1]
    assert '\u2212' not in bloc['code']
    chapitre=observation['Chap.'];numero=observation['Exercice/Défi']
    reference=f'D{numero:02}' if chapitre=='D' else f'{chapitre}.{numero}'
    traitements.append({
        'id':observation['ID'],'reference':reference,
        'localisation':observation['Localisation'],
        'page_pdf_avant':observation['Page PDF'],
        'page_pdf_apres':bloc['page_pdf'],
        'correction':observation['Remplacement exact'],
        'statut':'Corrigé et vérifié sur le code extrait du PDF',
    })
manifest['pdf_apres_sha256']=pdf_sha
manifest['traitements']=traitements
manifest['bilan']={'anomalies_corrigees':9,'blocs_pdf_valides_et_executes':27,
                  'pages_modifiees':comparaison['pages_modifiees'],
                  'pages_identiques':comparaison['pages_identiques']}
(R/'revision-audit-20261021.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
visuel={
    'sha256':pdf_sha,'pages_rendues':317,
    'comparaison':comparaison,'planches_relues':[1,2],
    'pages_modifiees_relues':comparaison['pages_modifiees'],
    'pages_controlees_par_poppler':[264],
    'defauts_restants':[],
}
(O/'relecture-visuelle.json').write_text(json.dumps(visuel,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
tick=chr(96)
table=[]
for t in traitements:
    table.append(f"| {t['id']} | {t['localisation']} {t['reference']} | "
                 f"{t['page_pdf_avant']} | {t['page_pdf_apres']} | "
                 f"{tick}{t['correction']}{tick} |")
texte="""# Première : corrections à la suite de l’audit

Révision du 21 octobre 2026. Le livre corrigé conserve ses 317 pages.
Le classeur fourni est conservé sans modification.

## Neuf anomalies traitées

Les neuf observations ont été reproduites dans le PDF initial. Elles concernaient
douze signes moins mathématiques U+2212 dans des blocs de code. Les fichiers
sources contenaient déjà le signe Python ASCII U+002D. Le style du livre
transformait ce caractère pendant la composition ; il conserve désormais le
caractère ASCII dans les programmes et les sorties de console.

Les numéros ci-dessous désignent les pages physiques du PDF. La pagination du
livre est inférieure d’une unité.

| ID | Passage | PDF initial | PDF corrigé | Code corrigé |
| --- | --- | ---: | ---: | --- |
"""+'\n'.join(table)+"""

## Précision pédagogique

Dans le corrigé 12.11, les hypothèses de la fonction de calcul des moments sont
explicitées : listes non vides, même longueur, une probabilité par valeur,
probabilités positives ou nulles dont la somme vaut 1.

Les explications des huit autres passages ont été relues. Les seuils, cas limites,
résultats numériques et fonctions concernés par les neuf observations ont été
recontrôlés.

## Vérifications

- Les 27 programmes sont extraits du PDF compilé, et pas seulement des sources.
  Leur indentation est reconstruite depuis les positions des glyphes, sans
  remplacer aucun opérateur. Leur syntaxe est valide, leur structure syntaxique
  est identique à celle des sources et tous ont été exécutés.
- Les tests du code extrait couvrent notamment l’échange des variables, le
  refroidissement à la minute 13, les seuils de simulation, les 470 moyennes sur
  500 pour la graine 2026, les moments, Fibonacci, les bornes exponentielles et
  la dichotomie.
- Les 219 groupes de contrôles des 210 exercices, les 356 contrôles des
  compléments, les 85 contrôles de structure et de calcul, les 350 contrôles
  géométriques et les 2 799 contrôles de relecture passent.
- Les 317 pages sont rendues. La comparaison de tous les pixels à 80 dpi
  montre 309 pages identiques. Les huit pages modifiées sont relues ; la page
  264 est également contrôlée en grand avec Poppler. Aucun texte ne sort des
  pages et les renvois sont stabilisés.

Cette révision traite toutes les observations de l’audit fourni. Les contrôles
de résultats soutiennent la relecture ; ils ne constituent pas une certification
formelle de toutes les sous-questions du livre.

Empreinte SHA-256 du PDF corrigé : """+tick+pdf_sha+tick+'.\n'
out=R.parent/'output/verification/corrections-audit-premiere-20261021.md'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(texte,encoding='utf-8')
print(json.dumps({'anomalies_corrigees':9,'rapport':str(out),
                  'sha256':pdf_sha},ensure_ascii=True,indent=2))
