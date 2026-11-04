"""Copie locale du contrôleur : contourne uniquement le blocage de fermeture Chrome."""
from pathlib import Path
D=Path(__file__).resolve().parent
OUTILS=D.parent.parent.parent/'outils'
code=(OUTILS/'controle_apercu.mjs').read_text(encoding='utf-8')
code=code.replace("const here = path.dirname(fileURLToPath(import.meta.url))", "const here = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../outils')")
code=code.replace('await browser.close()', 'await Promise.race([browser.close(), new Promise((resolve) => setTimeout(resolve, 2000))])')
code=code.replace('process.exit(problems ? 2 : 0)', "await new Promise((resolve) => process.stdout.write('', resolve)); process.exit(problems ? 2 : 0)")
code=code.replace("querySelectorAll('mjx-merror')", "querySelectorAll('mjx-merror, .mjx-merror, [data-mjx-error]')")
(D/'controle_apercu_local.mjs').write_text(code,encoding='utf-8')
print('Copie locale prête : audit inchangé, fermeture bornée à 2 secondes.')
