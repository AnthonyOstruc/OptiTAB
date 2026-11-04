from pathlib import Path
import re
p=Path(__file__).resolve().parent.parent/'17_solides/exercices.txt'
s=p.read_text(encoding='utf-8')
s=re.sub(r'\b(a|de|et|à|sur|avec|en)(?=\d)',r'\1 ',s)
p.write_text(s,encoding='utf-8')
