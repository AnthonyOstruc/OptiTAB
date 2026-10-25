"""Compile le livre (LuaLaTeX) jusqu'à stabilisation des renvois, puis contrôle le journal.

Usage, depuis livre-terminale-2027 : python -I -X utf8 outils/compiler.py [nombre_max_de_passes]
Contrôles : zéro « Overfull », zéro caractère manquant, zéro référence indéfinie, plus de demande de recompilation.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent
LUA = Path(os.environ["LOCALAPPDATA"]) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64" / "lualatex.exe"
MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6


def empreinte():
    aux = R / "build" / "main.aux"
    return hashlib.sha256(aux.read_bytes()).hexdigest() if aux.exists() else ""


(R / "build").mkdir(exist_ok=True)
avant = empreinte()
for passe in range(1, MAX + 1):
    r = subprocess.run([str(LUA), "-interaction=nonstopmode", "-file-line-error", "-aux-directory=build", "main.tex"],
                       cwd=R, capture_output=True, text=True, encoding="utf-8", errors="replace")
    log = (R / "build" / "main.log").read_text(encoding="utf-8", errors="replace")
    apres = empreinte()
    rerun = "Rerun to get" in log or "Label(s) may have changed" in log
    print(f"passe {passe} : code {r.returncode}, aux {'stable' if apres == avant else 'modifié'}, rerun={rerun}")
    if r.returncode != 0:
        print(r.stdout[-3000:])
        sys.exit(1)
    shutil.copy2(R / "main.pdf", R / "build" / "apercu.pdf")  # copie lisible pendant la passe suivante
    if apres == avant and not rerun and passe >= 2:
        break
    avant = apres

overfull = re.findall(r"^Overfull .*$", log, flags=re.M)
manquants = re.findall(r"^Missing character.*$", log, flags=re.M)
indefinis = re.findall(r"^LaTeX Warning: (?:Reference|Citation) .* undefined.*$", log, flags=re.M)
pages = re.search(r"Output written on .*?\((\d+) pages", log)
print(f"pages : {pages.group(1) if pages else '?'}")
print(f"Overfull : {len(overfull)}")
for o in overfull:
    print("   ", o)
print(f"Caractères manquants : {len(manquants)}")
for m in sorted(set(manquants)):
    print("   ", m)
print(f"Références indéfinies : {len(indefinis)}")
for m in indefinis[:20]:
    print("   ", m)
