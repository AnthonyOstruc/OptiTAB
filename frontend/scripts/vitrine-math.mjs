// Pré-rend en HTML (KaTeX) toutes les formules des exemples de l'accueil
// (src/config/vitrineExemples.js). La page n'embarque ainsi aucun moteur de
// formules : seule la feuille de style KaTeX, déjà chargée par main.js, sert.
// usage (depuis frontend/) : node scripts/vitrine-math.mjs
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import katex from 'katex'
import { vitrineExemples } from '../src/config/vitrineExemples.js'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const OUT = path.join(HERE, '..', 'src', 'config', 'vitrineMath.js')

// Toute propriété `tex` rencontrée dans les exemples est une formule à rendre.
const formules = new Set()
const collecter = (valeur) => {
  if (Array.isArray(valeur)) return valeur.forEach(collecter)
  if (!valeur || typeof valeur !== 'object') return
  if (typeof valeur.tex === 'string') formules.add(valeur.tex)
  Object.values(valeur).forEach(collecter)
}
collecter(vitrineExemples)

const rendu = {}
for (const tex of [...formules].sort()) {
  rendu[tex] = katex.renderToString(tex, { output: 'html', throwOnError: true })
}

fs.writeFileSync(
  OUT,
  '// Généré par scripts/vitrine-math.mjs à partir de vitrineExemples.js : ne pas modifier à la main.\n' +
    `export default ${JSON.stringify(rendu, null, 2)}\n`
)
console.log(`${formules.size} formules -> ${path.relative(process.cwd(), OUT)}`)
