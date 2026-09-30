export const MAX_BATCH_REELS = 30

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
  if (preamble || !items.length) errors.push('Commence chaque reel par REEL: suivi de son nom (ex. REEL: 1 oct).')
  if (items.length > MAX_BATCH_REELS) errors.push(`Une série peut contenir jusqu’à ${MAX_BATCH_REELS} reels.`)
  const projects = items.map((item, index) => {
    const template_text = item.lines.join('\n').trim()
    if (!item.title || item.title.length > 255) errors.push(`Reel ${index + 1} : ajoute un nom de 1 à 255 caractères.`)
    if (!template_text) errors.push(`Reel ${index + 1} : le script est vide.`)
    if (template_text.length > 100000) errors.push(`Reel ${index + 1} : le script est trop long.`)
    return { title: item.title, template_text }
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
