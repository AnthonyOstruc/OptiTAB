"""Vérificateur officiel, avec redirection du seul contrôleur Chrome vers sa copie locale."""
from pathlib import Path
import sys
D=Path(__file__).resolve().parent;OUTILS=D.parent.parent.parent/'outils'
sys.path.insert(0,str(OUTILS))
import verifier_notion as ver
run_original=ver.subprocess.run
def run(cmd,*args,**kwargs):
    if len(cmd)>1 and Path(cmd[1]).name=='controle_apercu.mjs':cmd=[cmd[0],str(D/'controle_apercu_local.mjs'),*cmd[2:]]
    return run_original(cmd,*args,**kwargs)
ver.subprocess.run=run
print('Vérificateur officiel ; fermeture Chrome bornée dans la copie locale du contrôleur.',flush=True)
sys.exit(1 if ver.verifier(sys.argv[1],True) else 0)
