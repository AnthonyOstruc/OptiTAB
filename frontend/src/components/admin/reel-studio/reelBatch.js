export const MAX_BATCH_REELS = 30

const MONTHS = [
  ['janv', 'janvier'], ['fevr', 'fevrier'], ['mars'], ['avr', 'avril'], ['mai'], ['juin'],
  ['juil', 'juillet'], ['aout'], ['sept', 'septembre'], ['oct', 'octobre'], ['nov', 'novembre'], ['dec', 'decembre'],
]
const MONTH_LABELS = ['janv', 'févr', 'mars', 'avr', 'mai', 'juin', 'juil', 'août', 'sept', 'oct', 'nov', 'déc']

export function normalizeReelDate(value) {
  const text = String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim()
  const match = text.match(/^(\d{1,2})(?:er)?\s+([a-z]+)\.?(?:\s+(\d{4}))?$/)
  if (!match) return ''
  const day = Number(match[1])
  const month = MONTHS.findIndex(names => names.includes(match[2]))
  const year = match[3] ? Number(match[3]) : 2024
  const leapYear = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0)
  const maxDays = [31, leapYear ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  if (month < 0 || year < 1 || day < 1 || day > maxDays[month]) return ''
  return `${day} ${MONTH_LABELS[month]}${match[3] ? ` ${match[3]}` : ''}`
}

export function buildReelBatchFormatHelp(reelFormat) {
  const batchInstructions = `Reel + — plusieurs reels par date :
- Utilise exactement la même méthode et le même format que pour un reel normal.
- Génère jusqu’à 30 reels pour les dates demandées, dans l’ordre de publication.
- Commence chaque reel par REEL: suivi uniquement de sa date : 1 oct, 2 oct, 3 oct, etc. L’année est facultative.
- Cette date est le titre du reel et de son onglet. Les champs TITLE des slides restent les titres du contenu.
- Recommence à SLIDE 1 pour chaque reel et termine sa description par END_INSTAGRAM_DESCRIPTION avant la date suivante.
- Réponds uniquement avec les reels complets. N’inclus pas les consignes dans les scripts et ne les répète pas entre les reels.

`
  return String(reelFormat)
    .replace('Structure:\nSLIDE', `${batchInstructions}Structure:\nREEL: <jour mois>\nSLIDE`)
    .replace('Mode Auto (IA décide le nombre de slides):\n', 'Mode Auto (IA décide le nombre de slides):\nREEL: 1 oct\n')
    .replace('Exemple prêt à copier:\n', 'Exemple prêt à copier:\nREEL: 1 oct\n')
}

export function parseReelBatch(text) {
  const items = []
  const errors = []
  let current = null
  let preamble = false
  for (const line of String(text || '').replace(/\r\n?/g, '\n').split('\n')) {
    const heading = line.match(/^\s*REEL\s*:\s*(.*?)\s*$/i)
    if (heading) {
      current = { title: heading[1], lines: [] }
      items.push(current)
    } else if (current) {
      current.lines.push(line)
    } else if (line.trim()) {
      preamble = true
    }
  }
  if (preamble || !items.length) errors.push('Commence chaque reel par sa date : REEL: 1 oct, puis REEL: 2 oct, etc.')
  if (items.length > MAX_BATCH_REELS) errors.push(`Une série peut contenir jusqu’à ${MAX_BATCH_REELS} reels.`)
  const dates = new Set()
  const projects = items.map((item, index) => {
    const template_text = item.lines.join('\n').trim()
    const title = normalizeReelDate(item.title)
    if (!title) errors.push(`Reel ${index + 1} : le titre doit être une date valide, par exemple 1 oct ou 1 oct 2026.`)
    else if (dates.has(title)) errors.push(`La date ${title} est utilisée plusieurs fois.`)
    dates.add(title)
    if (!template_text) errors.push(`Reel ${index + 1} : le script est vide.`)
    if (template_text.length > 100000) errors.push(`Reel ${index + 1} : le script est trop long.`)
    return { title: title || item.title, template_text }
  })
  return { projects, errors }
}

// Await the complete operation (including download) before starting another reel.
// A failure pauses the queue, including ambiguous network timeouts.
export async function runReelQueue(items, { process, shouldStop, onStart, onSuccess, onError }) {
  for (const item of items) {
    if (shouldStop()) break
    onStart(item)
    try {
      await process(item)
      onSuccess(item)
    } catch (error) {
      onError(item, error)
      break
    }
  }
}
