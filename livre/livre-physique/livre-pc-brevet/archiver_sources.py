from pathlib import Path
import requests,json,fitz
HERE=Path(__file__).resolve().parent/'recherche'
urls={
'dnb-reference-pc-2027.pdf':'https://eduscol.education.gouv.fr/sites/default/files/document/dnb-sujet-de-reference-physique-chimie-serie-generale-n01-129673.pdf',
'dnb-sciences-2026.pdf':'https://www.education.gouv.fr/sites/default/files/document/diplome-national-du-brevet-2026-sciences-serie-generale-517070.pdf',
'definition-epreuves-2027.html':'https://www.education.gouv.fr/bo/2026/Hebdo4/MENE2623228N'}
records=[]
for name,url in urls.items():
    try:
        r=requests.get(url,timeout=25);r.raise_for_status()
        if name.endswith('.pdf'):assert r.content.startswith(b'%PDF')
        (HERE/name).write_bytes(r.content)
        if name.endswith('.pdf'):
            doc=fitz.open(stream=r.content,filetype='pdf')
            (HERE/name.replace('.pdf','.txt')).write_text('\n'.join(p.get_text() for p in doc),encoding='utf8')
        records.append(dict(fichier=name,url=url,archive=True))
    except Exception as e:records.append(dict(fichier=name,url=url,archive=False,raison=str(e)))
(HERE/'archives.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(records,ensure_ascii=True))
