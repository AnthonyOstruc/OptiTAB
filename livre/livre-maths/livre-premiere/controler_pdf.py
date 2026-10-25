"""Rendu de toutes les pages et contrôles du PDF réellement compilé."""
from pathlib import Path
import json
import hashlib
import re
import fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'build/qa'
OUT.mkdir(parents=True, exist_ok=True)
pdf = fitz.open(ROOT/'main.pdf')
assert len(pdf) > 150, f'Pagination inattendue pour le livre complet : {len(pdf)}'
summary, thumbnails, bad_boxes, blank_pages, note_pages = [], [], [], [], []
link_count = 0
for number, page in enumerate(pdf, 1):
    text = page.get_text()
    if text.strip() == 'Notes' and len(page.get_drawings()) >= 20:
        note_pages.append(number)
    elif len(text.strip()) < 12:
        blank_pages.append(number)
    assert '??' not in text, f'Renvoi non résolu page {number}'
    for forbidden in ('à compléter', 'Emplacement du', 'Tome 1', 'Chapitres 1 à 5', 'cinq premiers chapitres', '75 exercices', 'extquotesingle', 'Entra?nement', 'Probl?mes', 'v?rification', '\ufffd'):
        assert forbidden not in text, (number, forbidden)
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            for span in line.get('spans', []):
                x0,y0,x1,y1 = span['bbox']
                if min(x0,y0) < -1 or x1 > page.rect.width+1 or y1 > page.rect.height+1:
                    bad_boxes.append((number,span['text'],span['bbox']))
    for link in page.get_links():
        link_count += 1
        if link['kind'] == fitz.LINK_GOTO:
            assert 0 <= link['page'] < len(pdf), (number,link)
    # Chaque page est rendue à 110 dpi pour la relecture.
    pix = page.get_pixmap(dpi=110)
    pix.save(OUT/f'page-{number}.png')
    im = Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    im.thumbnail((360,510))
    tile = Image.new('RGB',(380,540),'#e5e7eb')
    tile.paste(im,((380-im.width)//2,22))
    ImageDraw.Draw(tile).text((10,5),str(number),fill='black')
    thumbnails.append(tile)
    summary.append(f'{number}: '+text[:100].replace('\n',' | '))
for start in range(0,len(thumbnails),6):
    sheet = Image.new('RGB',(1140,1080),'white')
    for offset,im in enumerate(thumbnails[start:start+6]):
        sheet.paste(im,((offset%3)*380,(offset//3)*540))
    sheet.save(OUT/f'planche-{start//6+1}.png')
assert not blank_pages, f'Pages blanches : {blank_pages}'
assert not bad_boxes, f'Texte hors page : {bad_boxes}'
assert link_count >= 420, f'Trop peu de liens : {link_count}'
log = (ROOT/'build/main.log').read_text(encoding='utf-8',errors='replace')
for pattern in ('Overfull', 'undefined references', 'multiply defined', 'Missing character', 'Label(s) may have changed'):
    assert pattern not in log, f'Avertissement à corriger : {pattern}'
aux = (ROOT/'build/main.aux').read_text(encoding='utf-8')
exercise_labels = re.findall(r'\\newlabel\{exo-(\d+)-(\d+)\}',aux)
answer_labels = re.findall(r'\\newlabel\{cor-(\d+)-(\d+)\}',aux)
assert len(exercise_labels) == len(answer_labels) == 210
assert set(exercise_labels) == set(answer_labels)
geometry_pages=dict(re.findall(r'\\newlabel\{(figgeo-[^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux))
exercise_pages=dict(re.findall(r'\\newlabel\{((?:exo|cor)-\d+-\d+)\}\{\{[^}]*\}\{(\d+)\}',aux))
assert len(geometry_pages)==72, f'Figures attendues : 72, obtenues : {len(geometry_pages)}'
for label,number in geometry_pages.items():
    _,chapter,exercise,kind=label.split('-')
    paired=('exo' if kind=='ex' else 'cor')+f'-{int(chapter)}-{int(exercise)}'
    assert exercise_pages[paired]==number, f'Figure séparée de son exercice : {label}'
new_pages=dict(re.findall(r'\\newlabel\{(figlivre-[^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux))
review=json.loads((ROOT/'revision-editoriale.json').read_text(encoding='utf-8'))
expected_new=sum(len([r for r in entry['visuels_'+side] if r.startswith('r')]) for entry in review['exercices'] for side in ('enonce','corrige'))
assert len(new_pages)==expected_new,(len(new_pages),expected_new)
for label,number in new_pages.items():
    ch,ex=re.search(r'figlivre-r(\d+)-(\d+)',label).groups()
    kind=label.rsplit('-',1)[-1]
    paired=('exo' if kind=='ex' else 'cor')+f'-{int(ch)}-{int(ex)}'
    assert exercise_pages[paired]==number, f'Représentation séparée de son texte : {label}'
block_sizes=re.findall(r'OTBLOC\|((?:ex|cor)-\d+-\d+)\|([\d.]+)pt',log)
assert len(block_sizes)==420, f'Blocs de lecture attendus : 420, obtenus : {len(block_sizes)}'
edition=json.loads((ROOT/'edition-france-manifeste.json').read_text(encoding='utf-8'))
all_pages=dict(re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}',aux))
for p in edition['pages']:
    assert p['label'] in all_pages, f'Page de parcours absente : {p["label"]}'
for fig in edition['figures']:
    assert all_pages.get(fig['label'])==all_pages[fig['page_label']], f'Figure du parcours séparée : {fig["label"]}'
edition_blocks=re.findall(r'OTEDITION\|([^|]+)\|([\d.]+)pt',log)
assert len(edition_blocks)==len(edition['pages'])
assert all(float(h)<=560 for _,h in edition_blocks)
assert set(n for n,h in edition_blocks)==set(p['label'] for p in edition['pages'])
report = {'pages':len(pdf),'links':link_count,'exercise_labels':len(exercise_labels),
          'answer_labels':len(answer_labels),'bookmarks':len(pdf.get_toc()),
          'geometry_figures_with_exercise':len(geometry_pages),
          'new_figures_with_exercise':len(new_pages),
          'reading_blocks_checked':len(block_sizes),
          'tallest_block_pt':max(float(h) for _,h in block_sizes),
          'exercices_total':edition['exercices_total'],'defis':edition['defis'],
          'sujets_blancs':edition['sujets_blancs'],
          'edition_reading_blocks':len(edition_blocks),
          'edition_figures_with_text':len(edition['figures']),
          'blank_pages':blank_pages,'note_pages':note_pages,'out_of_page_text':bad_boxes,
          'metadata':pdf.metadata,
          'source_sha256':hashlib.sha256((ROOT/'main.pdf').read_bytes()).hexdigest()}
(OUT/'controle-pdf.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'pages.txt').write_text('\n'.join(summary),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
