"""Configuration commune aux parcours CM2, CM1, CE2 et CE1 du site."""
import json
import os
from pathlib import Path
from types import SimpleNamespace

GRADE = os.environ.get('OPTITAB_NIVEAU', 'cm2').lower()
assert GRADE in ('cm2', 'cm1', 'ce2', 'ce1'), GRADE
BASE = Path(__file__).resolve().parents[1]
FRONT = BASE.parents[2]
REPO = FRONT.parent
ROOT = BASE.parent / GRADE
BOOK = REPO / 'livre/livre-maths' / ('livre-' + GRADE)
LABEL = GRADE.upper()
LEVEL_ID = {'cm2':13,'cm1':12,'ce2':11,'ce1':10}[GRADE]
CATS = [('Découverte','easy'),('Entraînement','medium'),('Problème','hard')]

def chapters():
    return [SimpleNamespace(**c) for c in json.loads((ROOT/'sources/livre.json').read_text(encoding='utf-8'))]
