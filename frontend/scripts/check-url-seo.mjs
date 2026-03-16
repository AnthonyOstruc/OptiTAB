function parseCliArgs(argv) {
  const options = {
    url: String(process.env.npm_config_url || '').trim(),
    timeoutMs: 30000
  }

  for (const arg of argv) {
    if (arg.startsWith('--url=')) {
      options.url = arg.slice('--url='.length).trim()
      continue
    }
    if (arg.startsWith('--timeout=')) {
      const raw = Number(arg.slice('--timeout='.length))
      if (Number.isFinite(raw) && raw > 0) options.timeoutMs = Math.floor(raw)
    }
  }

  return options
}

function normalizeWhitespace(value) {
  return String(value || '')
    .replace(/\s+/g, ' ')
    .trim()
}

async function run() {
  const options = parseCliArgs(process.argv.slice(2))
  if (!options.url) {
    throw new Error('Missing required argument: --url=<absolute-url>')
  }

  let targetUrl = ''
  try {
    targetUrl = new URL(options.url).toString()
  } catch {
    throw new Error(`Invalid URL: ${options.url}`)
  }

  const { chromium } = await import('playwright')
  const browser = await chromium.launch({ headless: true })
  const context = await browser.newContext()
  const page = await context.newPage()

  try {
    await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: options.timeoutMs })
    await page.waitForLoadState('networkidle', { timeout: options.timeoutMs })

    const result = {
      requestedUrl: targetUrl,
      navigatedUrl: page.url(),
      title: normalizeWhitespace(await page.title()),
      description: normalizeWhitespace(
        String(await page.locator('meta[name="description"]').first().getAttribute('content') || '')
      ),
      robots: normalizeWhitespace(
        String(await page.locator('meta[name="robots"]').first().getAttribute('content') || '')
      ),
      canonical: normalizeWhitespace(
        String(await page.locator('link[rel="canonical"]').first().getAttribute('href') || '')
      ),
      h1: normalizeWhitespace(String(await page.locator('h1').first().textContent().catch(() => '') || ''))
    }

    console.log(JSON.stringify(result, null, 2))
  } finally {
    await context.close()
    await browser.close()
  }
}

run().catch((error) => {
  console.error('[check-url-seo] fatal:', error instanceof Error ? error.message : String(error))
  process.exit(1)
})
