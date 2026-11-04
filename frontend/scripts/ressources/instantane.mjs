// Export public versionné : le build Render ne dépend pas du backend Django.
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import { gzipSync, gunzipSync } from 'node:zlib'
import { fileURLToPath } from 'node:url'
import { construireCatalogue, lireSourcesCatalogue } from './catalogue.mjs'

export const DOSSIER_INSTANTANE = fileURLToPath(new URL('../../contenu/ressources/', import.meta.url))
const VERSION = 1
const empreinte = contenu => crypto.createHash('sha256').update(contenu).digest('hex')

function validerSources(sources) {
  for (const nom of ['cours', 'fiches', 'exercices', 'tousExercices']) {
    const liste = sources?.[nom]
    if (!Array.isArray(liste) || !liste.length) throw new Error(`Export incomplet : ${nom} absent ou vide`)
    const ids = new Set()
    for (const item of liste) {
      if (item?.id == null || ids.has(String(item.id))) throw new Error(`Export invalide : identifiant absent ou répété dans ${nom}`)
      ids.add(String(item.id))
      if (nom === 'tousExercices') {
        if (Object.keys(item).some(cle => !['id', 'notion'].includes(cle))) {
          throw new Error('Export invalide : le décompte des exercices doit contenir uniquement des identifiants')
        }
      } else if (String(item.is_locked) === 'true' || String(item.est_publie) === 'false') {
        throw new Error(`Export invalide : ressource non publique dans ${nom}`)
      }
    }
  }
  const catalogue = construireCatalogue(sources)
  if (!catalogue.classes.length || !catalogue.chapitres.length) throw new Error('Export sans chapitre exploitable')
  return catalogue
}

export function ecrireInstantane(sources, { dossier = DOSSIER_INSTANTANE, api, date = new Date().toISOString() } = {}) {
  const catalogue = validerSources(sources)
  const contenu = gzipSync(Buffer.from(JSON.stringify(sources)), { level: 9 })
  const manifeste = {
    version: VERSION,
    genereLe: date,
    source: api,
    sha256: empreinte(contenu),
    ressources: Object.fromEntries(Object.entries(sources).map(([nom, liste]) => [nom, liste.length])),
    classes: catalogue.classes.length,
    chapitres: catalogue.chapitres.length,
    totaux: catalogue.totaux
  }
  fs.mkdirSync(dossier, { recursive: true })
  const donnees = path.join(dossier, 'catalogue.json.gz')
  const metadata = path.join(dossier, 'catalogue.json')
  const temporaireDonnees = `${donnees}.${process.pid}.tmp`
  const temporaireMetadata = `${metadata}.${process.pid}.tmp`
  try {
    fs.writeFileSync(temporaireDonnees, contenu)
    fs.writeFileSync(temporaireMetadata, JSON.stringify(manifeste, null, 2) + '\n')
    fs.renameSync(temporaireDonnees, donnees)
    fs.renameSync(temporaireMetadata, metadata)
  } finally {
    fs.rmSync(temporaireDonnees, { force: true })
    fs.rmSync(temporaireMetadata, { force: true })
  }
  return { manifeste, catalogue, octets: contenu.length }
}

export function lireInstantane(dossier = DOSSIER_INSTANTANE) {
  const manifeste = JSON.parse(fs.readFileSync(path.join(dossier, 'catalogue.json'), 'utf8'))
  const contenu = fs.readFileSync(path.join(dossier, 'catalogue.json.gz'))
  if (manifeste.version !== VERSION) throw new Error('Version de l’export des ressources non prise en charge')
  if (!Number.isFinite(Date.parse(manifeste.genereLe))) throw new Error('Date de l’export des ressources invalide')
  if (empreinte(contenu) !== manifeste.sha256) throw new Error('Export des ressources corrompu : empreinte SHA-256 incorrecte')
  const sources = JSON.parse(gunzipSync(contenu).toString('utf8'))
  const catalogue = validerSources(sources)
  for (const [nom, liste] of Object.entries(sources)) {
    if (manifeste.ressources?.[nom] !== liste.length) throw new Error(`Export des ressources incomplet : ${nom}`)
  }
  const attendu = { classes: manifeste.classes, chapitres: manifeste.chapitres, ...manifeste.totaux }
  const obtenu = { classes: catalogue.classes.length, chapitres: catalogue.chapitres.length, ...catalogue.totaux }
  if (JSON.stringify(attendu) !== JSON.stringify(obtenu)) throw new Error('Export des ressources incohérent avec son manifeste')
  return { catalogue, manifeste }
}

async function main() {
  if (process.argv.includes('--actualiser')) {
    const api = (process.env.RESSOURCES_API_BASE || 'https://optitab-backend.onrender.com').replace(/\/+$/, '')
    console.log(`[ressources] actualisation de l’export public depuis ${api}`)
    const sources = await lireSourcesCatalogue(api)
    const { manifeste, octets } = ecrireInstantane(sources, { api })
    console.log(`[ressources] export vérifié : ${manifeste.classes} classes, ${manifeste.chapitres} chapitres, ${Math.round(octets / 1024)} Ko compressés`)
  } else if (!process.argv.includes('--verifier')) {
    throw new Error('Utiliser --verifier ou --actualiser')
  }
  const { manifeste } = lireInstantane()
  console.log(`[ressources] export local vérifié du ${manifeste.genereLe} : ${manifeste.chapitres} chapitres ; aucun appel API nécessaire au build`)
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(erreur => {
    console.error('[ressources] ÉCHEC :', erreur)
    process.exitCode = 1
  })
}
