"""Compilation LuaLaTeX et refus des débordements détectés dans le journal."""
from pathlib import Path
import subprocess, hashlib, re
R=Path(__file__).resolve().parent
B=R/'build'; B.mkdir(exist_ok=True)
for i in range(1,6):
    aux=B/'main.aux'
    before=hashlib.sha256(aux.read_bytes()).hexdigest() if aux.exists() else ''
    print(f'Passe {i}',flush=True)
    p=subprocess.run(['lualatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory=build','main.tex'],cwd=R,capture_output=True)
    output=(p.stdout+p.stderr).decode('utf-8',errors='replace')
    (B/f'compilation-{i}.txt').write_text(output,encoding='utf-8')
    log=(B/'main.log').read_text(encoding='utf-8',errors='replace')
    if 'Output written on' not in log or 'Fatal error' in log:
        raise RuntimeError(output[-4500:])
    after=hashlib.sha256(aux.read_bytes()).hexdigest()
    if after==before and 'Rerun to get' not in log and 'undefined references' not in log:
        break
else:
    raise RuntimeError('Renvois non stabilisés.')
issues=[line for line in log.splitlines() if any(t in line for t in ('Overfull','Missing character','multiply defined','undefined references'))]
if issues:
    raise RuntimeError('\n'.join(issues))
print(re.search(r'Output written on[^\n]*',log).group(),flush=True)
