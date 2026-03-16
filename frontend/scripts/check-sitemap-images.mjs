const DEFAULT_SITEMAP_URL = 'https://www.optitab.net/sitemap-images.xml'
const DEFAULT_CONCURRENCY = 8

function parseCliArgs(argv) {
  const options = {
    sitemap: DEFAULT_SITEMAP_URL,
    concurrency: DEFAULT_CONCURRENCY,
    samplePages: 0,
    sampleImages: 0
  }

  for (const arg of argv) {
    if (arg.startsWith('--sitemap=')) {
      const value = arg.slice('--sitemap='.length).trim()
      if (value) options.sitemap = value
      continue
    }
    if (arg.startsWith('--concurrency=')) {
      const raw = Number(arg.slice('--concurrency='.length))
      if (Number.isFinite(raw) && raw > 0) options.concurrency = Math.max(1, Math.min(20, Math.floor(raw)))
      continue
    }
    if (arg.startsWith('--sample-pages=')) {
      const raw = Number(arg.slice('--sample-pages='.length))
      if (Number.isFinite(raw) && raw > 0) options.samplePages = Math.floor(raw)
      continue
    }
    if (arg.startsWith('--sample-images=')) {
      const raw = Number(arg.slice('--sample-images='.length))
      if (Number.isFinite(raw) && raw > 0) options.sampleImages = Math.floor(raw)
    }
  }

  return options
}

function uniq(values) {
  return [...new Set(values.filter(Boolean))]
}

function pick(values, size) {
  if (!size || size <= 0 || size >= values.length) return [...values]
  const copy = [...values]
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1))
    const t = copy[i]
    copy[i] = copy[j]
    copy[j] = t
  }
  return copy.slice(0, size)
}

async function mapWithConcurrency(items, mapper, concurrency) {
  if (!items.length) return []
  const results = new Array(items.length)
  let idx = 0

  async function worker() {
    while (idx < items.length) {
      const i = idx
      idx += 1
      results[i] = await mapper(items[i], i)
    }
  }

  const workers = Array.from({ length: Math.min(concurrency, items.length) }, () => worker())
  await Promise.all(workers)
  return results
}

async function checkUrl(url, method = 'HEAD') {
  try {
    const res = await fetch(url, { method, redirect: 'follow' })
    return { url, ok: res.status >= 200 && res.status < 400, status: res.status }
  } catch (error) {
    return { url, ok: false, status: null, error: error instanceof Error ? error.message : String(error) }
  }
}

async function run() {
  const options = parseCliArgs(process.argv.slice(2))

  const sitemapRes = await fetch(options.sitemap, { method: 'GET', redirect: 'follow' })
  const xml = await sitemapRes.text()

  if (sitemapRes.status !== 200) {
    throw new Error(`Sitemap fetch failed: ${options.sitemap} -> HTTP ${sitemapRes.status}`)
  }

  const pageLocs = uniq([...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => String(m[1] || '').trim()))
  const imageLocs = uniq(
    [...xml.matchAll(/<image:loc>([^<]+)<\/image:loc>/g)].map((m) => String(m[1] || '').trim())
  )

  const pagesToCheck = pick(pageLocs, options.samplePages)
  const imagesToCheck = pick(imageLocs, options.sampleImages)

  const [pageResults, imageResults] = await Promise.all([
    mapWithConcurrency(pagesToCheck, (url) => checkUrl(url, 'GET'), options.concurrency),
    mapWithConcurrency(imagesToCheck, (url) => checkUrl(url, 'HEAD'), options.concurrency)
  ])

  const pageFailures = pageResults.filter((r) => !r.ok)
  const imageFailures = imageResults.filter((r) => !r.ok)

  console.log(
    JSON.stringify(
      {
        sitemap: options.sitemap,
        sitemapStatus: sitemapRes.status,
        pageLocCount: pageLocs.length,
        imageLocCount: imageLocs.length,
        checkedPages: pagesToCheck.length,
        checkedImages: imagesToCheck.length,
        pageFailures: pageFailures.length,
        imageFailures: imageFailures.length
      },
      null,
      2
    )
  )

  if (pageFailures.length > 0 || imageFailures.length > 0) {
    console.error('[sitemap-images-check] FAIL')
    for (const failure of [...pageFailures, ...imageFailures].slice(0, 30)) {
      console.error(
        `- ${failure.url} status=${failure.status == null ? 'ERR' : failure.status}${failure.error ? ` error=${failure.error}` : ''}`
      )
    }
    process.exit(1)
  }

  console.log('[sitemap-images-check] PASS')
}

run().catch((error) => {
  console.error('[sitemap-images-check] fatal:', error instanceof Error ? error.message : String(error))
  process.exit(1)
})
