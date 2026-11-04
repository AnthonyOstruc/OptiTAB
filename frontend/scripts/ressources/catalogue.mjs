// Catalogue des ressources gratuites, lu sur l'API publique (aucun jeton) :
// cours, fiches de synthèse et exercices gratuits, rangés par classe, thème
// et chapitre dans l'ordre du programme.
import { CLASSES, CLASSE_PAR_NOM } from './classes.mjs'

const TAILLE_PAGE = 20
const TAILLE_PAGE_LEGERE = 100
const ESSAIS = 6

const pause = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

async function lireJson(url) {
  let derniere
  for (let essai = 1; essai <= ESSAIS; essai++) {
    try {
      const reponse = await fetch(url, { headers: { Accept: 'application/json' }, signal: AbortSignal.timeout(90000) })
      if (!reponse.ok) {
        const erreur = new Error(`HTTP ${reponse.status}`)
        erreur.retentable = reponse.status === 408 || reponse.status === 429 || reponse.status >= 500
        const retryAfter = reponse.headers.get('retry-after')
        erreur.delai = retryAfter
          ? (/^\d+$/.test(retryAfter) ? Number(retryAfter) * 1000 : Date.parse(retryAfter) - Date.now())
          : 0
        await reponse.body?.cancel()
        throw erreur
      }
      return await reponse.json()
    } catch (e) {
      derniere = e
      if (e.retentable === false || essai === ESSAIS) break
      const delai = Math.min(60000, Math.max(Math.min(2000 * 2 ** (essai - 1), 30000), e.delai || 0))
      console.warn(`[ressources] ${e.message} ; nouvelle tentative ${essai + 1}/${ESSAIS} dans ${delai / 1000} s : ${url}`)
      await pause(delai)
    }
  }
  throw new Error(`Lecture impossible de ${url} : ${derniere?.message || derniere}`)
}

const estLibre = (item) => String(item.is_locked) !== 'true' && item.is_locked !== true && String(item.est_publie) !== 'false'

// Toutes les pages d'un type. `jusquAuxPayants` : l'API range les ressources
// gratuites en premier, on s'arrête à la première page sans ressource gratuite.
async function toutesLesPages(api, type, { jusquAuxPayants = false, leger = false } = {}) {
  const items = []
  for (let page = 1; ; page++) {
    if (page > 1000) throw new Error(`Pagination sans fin pour le catalogue ${type}`)
    const params = new URLSearchParams({ type, page: String(page), page_size: String(leger ? TAILLE_PAGE_LEGERE : TAILLE_PAGE) })
    if (leger) params.set('light', '1')
    else { params.set('full_content', '1'); params.set('include_images', '1') }
    const donnees = await lireJson(`${api}/api/free/learning-resources/?${params}`)
    const resultats = Array.isArray(donnees) ? donnees : donnees?.results
    if (!Array.isArray(resultats)) throw new Error(`Catalogue ${type} invalide, page ${page}`)
    items.push(...resultats)
    if (!Array.isArray(donnees) && donnees.next && !resultats.length) {
      throw new Error(`Catalogue ${type} incomplet, page ${page} vide avant la fin`)
    }
    if (jusquAuxPayants && !resultats.some(estLibre)) break
    if (Array.isArray(donnees) || !donnees.next) {
      if (!jusquAuxPayants && Number.isInteger(donnees.count) && items.length !== donnees.count) {
        throw new Error(`Catalogue ${type} incomplet : ${items.length}/${donnees.count} ressources`)
      }
      break
    }
  }
  console.log(`[ressources] catalogue ${type}${leger ? ' (léger)' : ''} : ${items.length} ressources lues`)
  return items
}

export function slugifier(texte, max = 72) {
  let s = String(texte || '')
    .normalize('NFD').replace(/\p{Diacritic}/gu, '')
    .replace(/[’']/g, ' ')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
  if (s.length > max) s = s.slice(0, max).replace(/-[^-]*$/, '')
  return s || 'chapitre'
}

const nombre = (v) => (v === null || v === undefined || v === '' ? null : Number(v))

export async function chargerCatalogue(api) {
  // Une seule requête à la fois : les contenus et leurs images sont volumineux,
  // et le backend Render dispose aussi de ses requêtes visiteurs à traiter.
  const cours = await toutesLesPages(api, 'course')
  const fiches = await toutesLesPages(api, 'summary')
  const exercices = await toutesLesPages(api, 'exercise', { jusquAuxPayants: true })
  const tousExercices = await toutesLesPages(api, 'exercise', { leger: true })

  // Nombre total d'exercices corrigés par chapitre (gratuits et réservés aux abonnés).
  const totalParChapitre = new Map()
  for (const e of tousExercices) totalParChapitre.set(String(e.notion), (totalParChapitre.get(String(e.notion)) || 0) + 1)

  const chapitres = new Map()
  for (const c of cours.filter(estLibre)) {
    const classe = CLASSE_PAR_NOM.get(c.niveau_nom)
    if (!classe || !c.notion) continue
    chapitres.set(String(c.notion), {
      notionId: String(c.notion),
      titre: String(c.notion_nom || c.titre).trim(),
      classe,
      themeId: String(c.theme_id),
      theme: String(c.theme_nom || '').trim(),
      ordre: nombre(c.ordre) ?? 999,
      cours: c,
      fiche: null,
      exercices: [],
      totalExercices: totalParChapitre.get(String(c.notion)) || 0,
      modifie: c.date_modification
    })
  }
  for (const f of fiches.filter(estLibre)) {
    const ch = chapitres.get(String(f.notion))
    if (ch && !ch.fiche) ch.fiche = f
  }
  for (const e of exercices.filter(estLibre)) {
    const ch = chapitres.get(String(e.notion))
    if (ch) ch.exercices.push(e)
  }

  const ordreDifficulte = { easy: 0, medium: 1, hard: 2 }
  const classes = []
  for (const classe of CLASSES) {
    const liste = [...chapitres.values()]
      .filter((ch) => ch.classe === classe)
      .sort((a, b) => a.ordre - b.ordre || Number(a.notionId) - Number(b.notionId))
    if (!liste.length) continue
    const vus = new Set()
    liste.forEach((ch, i) => {
      ch.numero = i + 1
      let slug = slugifier(ch.titre)
      while (vus.has(slug)) slug = `${slug}-${ch.notionId}`
      vus.add(slug)
      ch.slug = slug
      ch.exercices.sort((a, b) => (ordreDifficulte[a.difficulty] ?? 1) - (ordreDifficulte[b.difficulty] ?? 1) || Number(a.id) - Number(b.id))
      const dates = [ch.cours?.date_modification, ch.fiche?.date_modification, ...ch.exercices.map((e) => e.date_modification)].filter(Boolean).sort()
      ch.modifie = dates[dates.length - 1] || null
    })
    // Thèmes dans l'ordre de leur premier chapitre.
    const themes = []
    for (const ch of liste) {
      let t = themes.find((x) => x.id === ch.themeId)
      if (!t) themes.push((t = { id: ch.themeId, titre: ch.theme, chapitres: [] }))
      t.chapitres.push(ch)
    }
    liste.forEach((ch, i) => { ch.precedent = liste[i - 1] || null; ch.suivant = liste[i + 1] || null })
    classes.push({ ...classe, chapitres: liste, themes })
  }

  return {
    classes,
    chapitres: classes.flatMap((c) => c.chapitres),
    totaux: {
      cours: classes.reduce((n, c) => n + c.chapitres.filter((ch) => ch.cours).length, 0),
      fiches: classes.reduce((n, c) => n + c.chapitres.filter((ch) => ch.fiche).length, 0),
      exercicesGratuits: classes.reduce((n, c) => n + c.chapitres.reduce((m, ch) => m + ch.exercices.length, 0), 0),
      exercices: tousExercices.length
    }
  }
}
