import test from 'node:test'
import assert from 'node:assert/strict'
import { parseReelBatch, runReelQueue } from './reelBatch.js'

test('batch import preserves script content, slide titles and descriptions', () => {
  const script = 'SLIDE 1 | hook\nTITLE: Mon titre\nKATEX: \\frac{1}{2}\nVOICE: Un demi.\n---\nSLIDE 2 | result\nTEXT: Résultat\nINSTAGRAM_DESCRIPTION:\n#maths\nEND_INSTAGRAM_DESCRIPTION'
  const parsed = parseReelBatch(`REEL: 1 oct\r\n${script}\n\nREEL: 2 oct\n${script}`)
  assert.deepEqual(parsed.errors, [])
  assert.deepEqual(parsed.projects.map(item => item.title), ['1 oct', '2 oct'])
  assert.equal(parsed.projects[0].template_text, script)
})

test('batch import validates limits, missing names, missing scripts and unexpected preamble', () => {
  const make = count => Array.from({ length: count }, (_, i) => `REEL: ${i + 1} oct\nSLIDE 1 | hook\nTITLE: Test`).join('\n')
  assert.equal(parseReelBatch(make(30)).errors.length, 0)
  for (const source of ['', make(31), 'REEL: \nTITLE: Test', 'REEL: 1 oct', 'Texte perdu\nREEL: 1 oct\nTITLE: Test']) {
    assert.ok(parseReelBatch(source).errors.length > 0)
  }
})

test('queue waits for generation and download before starting the next reel', async () => {
  const events = []
  await runReelQueue([1, 2, 3], {
    shouldStop: () => false,
    onStart: id => events.push(`start ${id}`),
    process: async id => {
      await new Promise(resolve => setTimeout(resolve, 5))
      events.push(`generated ${id}`)
      await new Promise(resolve => setTimeout(resolve, 5))
      events.push(`downloaded ${id}`)
    },
    onSuccess: id => events.push(`done ${id}`),
    onError: () => assert.fail('Unexpected failure'),
  })
  assert.deepEqual(events, [1, 2, 3].flatMap(id => [`start ${id}`, `generated ${id}`, `downloaded ${id}`, `done ${id}`]))
})

test('queue pauses on failure and stops after the current reel on request', async () => {
  const complete = []
  const failed = []
  await runReelQueue([1, 2, 3], {
    shouldStop: () => false, onStart: () => {},
    process: async id => { if (id === 2) throw new Error('Network timeout') },
    onSuccess: id => complete.push(id), onError: id => failed.push(id),
  })
  assert.deepEqual(complete, [1])
  assert.deepEqual(failed, [2])
  let stop = false
  await runReelQueue([3, 4], {
    shouldStop: () => stop, onStart: () => {},
    process: async () => { stop = true },
    onSuccess: id => complete.push(id), onError: () => assert.fail(),
  })
  assert.deepEqual(complete, [1, 3])
})
