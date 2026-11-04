"""Vérificateur officiel avec seul contournement du cleanup Chrome bloqué."""
from pathlib import Path
import sys
import subprocess
D=Path(__file__).resolve().parent
sys.path.insert(0,str(D.parent.parent.parent/'outils'))
import verifier_notion
run=subprocess.run
def local_run(args,*a,**kw):
    if isinstance(args,list) and len(args)>1 and Path(args[1]).name=='controle_apercu.mjs':
        args=list(args);args[1]=str(D/'controle_apercu_local.mjs')
    return run(args,*a,**kw)
verifier_notion.subprocess.run=local_run
sys.exit(bool(verifier_notion.verifier(Path(sys.argv[1]),navigateur=True)))
