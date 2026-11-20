// Prévient les moteurs IndexNow (Bing, donc Copilot et la recherche de ChatGPT,
// Yandex, Seznam, Naver…) qu'une page a été ajoutée ou modifiée, sans attendre
// leur prochain passage. Google n'utilise pas IndexNow : pour lui, le plan du site
// et la Search Console suffisent.
//
// À lancer APRÈS le déploiement (les pages et la clé doivent être en ligne) :
//   node scripts/ressources/indexnow.mjs --url /ressources-gratuites/methodes/convertisseur-d-unites/
//   node scripts/ressources/indexnow.mjs --depuis 2026-11-20
//   node scripts/ressources/indexnow.mjs --prefixe /ressources-gratuites/maths/ --profondeur 3
//   node scripts/ressources/indexnow.mjs --toutes
// Ajouter --essai pour voir la liste sans rien envoyer.
//
// Les adresses viennent des plans du site EN LIGNE (sitemap-ressources.xml et
// sitemap.xml) : une adresse absente du plan est refusée, pour ne jamais signaler
// une page qui n'existe pas. Ne pas renvoyer la même page plusieurs fois par jour.
//
// La clé est le fichier public/<CLE>.txt (servi à la racine du site) : ne pas le
// supprimer ni le renommer, sinon Bing refuse les envois (erreur 403).

const SITE = 'https://www.optitab.net'
const HOTE = 'www.optitab.net'
const CLE = '972077ebf71c7764ee5ced535382ebee'
const PLANS = ['/sitemap-ressources.xml', '/sitemap.xml']
const API = 'https://api.indexnow.org/indexnow'
const MAX = 10000 // limite IndexNow par envoi

function options(argv) {
  const o = { urls: [], depuis: null, prefixe: null, profondeur: null, toutes: false, essai: false }
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (a === '--url') o.urls.push(argv[++i])
    else if (a === '--depuis') o.depuis = argv[++i]
    else if (a === '--prefixe') o.prefixe = argv[++i]
    else if (a === '--profondeur') o.profondeur = Number(argv[++i])
    else if (a === '--toutes') o.toutes = true
    else if (a === '--essai') o.essai = true
    else throw new Error(`Option inconnue : ${a}`)
  }
  if (o.depuis && !/^\d{4}-\d{2}-\d{2}$/.test(o.depuis)) throw new Error('--depuis attend une date AAAA-MM-JJ')
  if (!o.urls.length && !o.depuis && !o.prefixe && !o.toutes) {
    throw new Error('Préciser --url, --depuis, --prefixe ou --toutes (voir l’en-tête du fichier).')
  }
  return o
}

async function texte(url) {
  const r = await fetch(url, { headers: { 'User-Agent': 'OptiTAB-IndexNow/1.0' } })
  if (!r.ok) throw new Error(`${url} : HTTP ${r.status}`)
  return r.text()
}

// Toutes les pages des plans du site en ligne, avec leur date de modification.
async function pagesEnLigne() {
  const pages = new Map()
  for (const plan of PLANS) {
    const xml = await texte(SITE + plan)
    for (const m of xml.matchAll(/<url>\s*<loc>([^<]+)<\/loc>(?:\s*<lastmod>([^<]+)<\/lastmod>)?/g)) {
      pages.set(m[1].trim(), (m[2] || '').slice(0, 10))
    }
  }
  return pages
}

function choisir(pages, o) {
  const absolue = (u) => (u.startsWith('http') ? u : SITE + (u.startsWith('/') ? u : '/' + u))
  const choix = new Set()
  for (const u of o.urls) {
    const a = absolue(u)
    if (!pages.has(a)) throw new Error(`Absente des plans du site en ligne : ${a}`)
    choix.add(a)
  }
  for (const [u, date] of pages) {
    if (o.toutes) choix.add(u)
    if (o.depuis && date && date >= o.depuis) choix.add(u)
    if (o.prefixe && u.startsWith(absolue(o.prefixe))) {
      const niveaux = new URL(u).pathname.split('/').filter(Boolean).length
      if (!o.profondeur || niveaux <= o.profondeur) choix.add(u)
    }
  }
  return [...choix]
}

async function main() {
  const o = options(process.argv.slice(2))

  const cle = (await texte(`${SITE}/${CLE}.txt`).catch((e) => `introuvable (${e.message})`)).trim()
  if (cle !== CLE) {
    const msg = `Clé absente ou différente en ligne : « ${cle.slice(0, 60)} ». Déployer d’abord le site.`
    if (!o.essai) throw new Error(msg)
    console.log('Attention : ' + msg)
  }

  const urls = choisir(await pagesEnLigne(), o)
  if (!urls.length) { console.log('Aucune page à signaler.'); return }
  if (urls.length > MAX) throw new Error(`${urls.length} adresses : maximum ${MAX} par envoi.`)
  console.log(`${urls.length} page(s) à signaler :`)
  for (const u of urls.slice(0, 15)) console.log('  ' + u.replace(SITE, ''))
  if (urls.length > 15) console.log(`  … et ${urls.length - 15} autres`)
  if (o.essai) { console.log('Essai : rien n’a été envoyé.'); return }

  const r = await fetch(API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'OptiTAB-IndexNow/1.0' },
    body: JSON.stringify({ host: HOTE, key: CLE, keyLocation: `${SITE}/${CLE}.txt`, urlList: urls })
  })
  const SENS = {
    200: 'reçu',
    202: 'reçu (clé en cours de vérification)',
    400: 'requête invalide',
    403: 'clé refusée (fichier de clé absent ou différent)',
    422: 'adresses refusées (hors du site ou mal formées)',
    429: 'trop d’envois : réessayer plus tard'
  }
  const corps = (await r.text()).slice(0, 300)
  console.log(`IndexNow : HTTP ${r.status} — ${SENS[r.status] || 'réponse inattendue'}${corps ? ` — ${corps}` : ''}`)
  if (r.status !== 200 && r.status !== 202) process.exitCode = 1
}

main().catch((e) => { console.error('IndexNow : ' + e.message); process.exitCode = 1 })
