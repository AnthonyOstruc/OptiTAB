"""Même contrôle officiel, délai borné pour le nettoyage Chrome sous Windows.

Ne modifie aucun outil commun. Les audits et captures restent identiques.
"""
from pathlib import Path
import json
D=Path(__file__).resolve().parent
OUTILS=D.parent.parent.parent/'outils'
source=(OUTILS/'controle_apercu.mjs').read_text(encoding='utf-8')
source=source.replace('const here = path.dirname(fileURLToPath(import.meta.url))','const here = '+json.dumps(str(OUTILS)))
source=source.replace('await browser.close()',"await Promise.race([browser.close(), new Promise((resolve) => setTimeout(resolve, 2000))])")
(D/'controle_apercu_local.mjs').write_text(source,encoding='utf-8')
print('Contrôleur local prêt, audits et limites de concurrence inchangés.')
