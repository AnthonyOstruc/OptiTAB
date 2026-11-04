import assert from 'node:assert/strict'
import test from 'node:test'
import { chargerCatalogue } from './catalogue.mjs'

const cours = Array.from({ length: 21 }, (_, i) => ({
  id: i + 1, notion: i + 1, titre: `Chapitre ${i + 1}`, niveau_nom: 'CP',
  theme_id: 1, theme_nom: 'Nombres', ordre: i + 1, is_locked: false
}))
const fiches = cours.map(c => ({ ...c, id: c.id + 100 }))
const exercices = Array.from({ length: 150 }, (_, i) => ({
  id: i + 200, notion: i % 21 + 1, is_locked: i >= 3
}))

function simuler(t, intercepter = () => null) {
  const requetes = []
  const attentes = []
  let actives = 0
  let maximum = 0
  t.mock.method(console, 'log', () => {})
  t.mock.method(console, 'warn', () => {})
  t.mock.method(globalThis, 'setTimeout', (callback, delai) => {
    attentes.push(delai)
    queueMicrotask(callback)
    return 0
  })
  t.mock.method(globalThis, 'fetch', async adresse => {
    const url = new URL(adresse)
    requetes.push(url)
    actives++
    maximum = Math.max(maximum, actives)
    try {
      await Promise.resolve()
      const remplacement = intercepter(url)
      if (remplacement) return remplacement
      const type = url.searchParams.get('type')
      const liste = type === 'course' ? cours : type === 'summary' ? fiches : exercices
      const taille = Number(url.searchParams.get('page_size'))
      const page = Number(url.searchParams.get('page'))
      const debut = (page - 1) * taille
      return Response.json({
        count: liste.length,
        results: liste.slice(debut, debut + taille),
        next: debut + taille < liste.length ? 'page-suivante' : null
      })
    } finally {
      actives--
    }
  })
  return { requetes, attentes, maximum: () => maximum }
}

test('lots réduits, requêtes successives et pagination complète', async t => {
  const simulation = simuler(t)
  const catalogue = await chargerCatalogue('https://catalogue.test')
  assert.deepEqual(catalogue.totaux, { cours: 21, fiches: 21, exercicesGratuits: 3, exercices: 150 })
  assert.equal(simulation.maximum(), 1)
  for (const url of simulation.requetes) {
    const leger = url.searchParams.has('light')
    assert.equal(url.searchParams.get('page_size'), leger ? '100' : '20')
    assert.equal(url.searchParams.get('full_content'), leger ? null : '1')
    assert.equal(url.searchParams.get('include_images'), leger ? null : '1')
  }
  assert.deepEqual(simulation.requetes.map(u => u.searchParams.get('type')),
    ['course', 'course', 'summary', 'summary', 'exercise', 'exercise', 'exercise', 'exercise'])
})

test('502 transitoires : récupération sans perdre de pages', async t => {
  let erreurs = 0
  const simulation = simuler(t, url => {
    if (url.searchParams.get('type') === 'summary' && erreurs++ < 2) {
      return new Response('Bad Gateway', { status: 502 })
    }
  })
  const catalogue = await chargerCatalogue('https://catalogue.test')
  assert.equal(catalogue.totaux.fiches, 21)
  assert.deepEqual(simulation.attentes, [2000, 4000])
})

test('502 persistants : échec explicite après six essais, sans attente finale', async t => {
  const simulation = simuler(t, () => new Response('Bad Gateway', { status: 502 }))
  await assert.rejects(chargerCatalogue('https://catalogue.test'), /HTTP 502/)
  assert.equal(simulation.requetes.length, 6)
  assert.deepEqual(simulation.attentes, [2000, 4000, 8000, 16000, 30000])
})

test('404 : arrêt immédiat', async t => {
  const simulation = simuler(t, () => new Response('Not Found', { status: 404 }))
  await assert.rejects(chargerCatalogue('https://catalogue.test'), /HTTP 404/)
  assert.equal(simulation.requetes.length, 1)
  assert.deepEqual(simulation.attentes, [])
})

test('429 : respect du délai Retry-After', async t => {
  let premier = true
  const simulation = simuler(t, () => {
    if (!premier) return null
    premier = false
    return new Response('Too Many Requests', { status: 429, headers: { 'Retry-After': '5' } })
  })
  await chargerCatalogue('https://catalogue.test')
  assert.deepEqual(simulation.attentes, [5000])
})

test('erreur réseau transitoire : nouvelle tentative', async t => {
  let premier = true
  const simulation = simuler(t, () => {
    if (!premier) return null
    premier = false
    throw new TypeError('fetch failed')
  })
  const catalogue = await chargerCatalogue('https://catalogue.test')
  assert.equal(catalogue.totaux.cours, 21)
  assert.deepEqual(simulation.attentes, [2000])
})

test('réponse JSON invalide : nouvelle tentative', async t => {
  let premier = true
  const simulation = simuler(t, () => {
    if (!premier) return null
    premier = false
    return new Response('<html>upstream error</html>')
  })
  await chargerCatalogue('https://catalogue.test')
  assert.deepEqual(simulation.attentes, [2000])
})

test('catalogue tronqué : le build échoue plutôt que de publier des pages manquantes', async t => {
  simuler(t, () => Response.json({ count: 21, results: cours.slice(0, 20), next: null }))
  await assert.rejects(chargerCatalogue('https://catalogue.test'), /incomplet : 20\/21/)
})

test('page vide avant la fin : refus du catalogue incomplet', async t => {
  simuler(t, url => url.searchParams.get('type') === 'exercise'
    ? Response.json({ count: 150, results: [], next: 'page-suivante' }) : null)
  await assert.rejects(chargerCatalogue('https://catalogue.test'), /page 1 vide avant la fin/)
})
