import assert from 'node:assert/strict'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import test from 'node:test'
import { gunzipSync } from 'node:zlib'
import { construireCatalogue } from './catalogue.mjs'
import { ecrireInstantane, lireInstantane } from './instantane.mjs'

const sources = () => ({
  cours: [{ id: 1, notion: 1, titre: 'Nombres', niveau_nom: 'CP', theme_id: 1, theme_nom: 'Nombres', contenu: 'Cours public', is_locked: false }],
  fiches: [{ id: 2, notion: 1, contenu: 'Fiche publique', is_locked: false }],
  exercices: [{ id: 3, notion: 1, question: 'Exercice public', is_locked: false }],
  tousExercices: [{ id: 3, notion: 1 }, { id: 4, notion: 1 }]
})

function dossierTemporaire(t) {
  const dossier = fs.mkdtempSync(path.join(os.tmpdir(), 'optitab-instantane-test-'))
  t.after(() => {
    assert.ok(path.resolve(dossier).startsWith(path.resolve(os.tmpdir()) + path.sep))
    fs.rmSync(dossier, { recursive: true, force: true })
  })
  return dossier
}

test('export complet et lecture sans aucun accès réseau', t => {
  const dossier = dossierTemporaire(t)
  const brut = sources()
  ecrireInstantane(brut, { dossier, api: 'https://catalogue.test' })
  t.mock.method(globalThis, 'fetch', () => { throw new Error('Réseau indisponible') })
  const { catalogue, manifeste } = lireInstantane(dossier)
  assert.deepEqual(catalogue.totaux, construireCatalogue(brut).totaux)
  assert.equal(catalogue.chapitres[0].cours.contenu, 'Cours public')
  assert.equal(catalogue.chapitres[0].fiche.contenu, 'Fiche publique')
  assert.equal(catalogue.chapitres[0].exercices[0].question, 'Exercice public')
  assert.equal(manifeste.chapitres, 1)
  assert.equal(globalThis.fetch.mock.calls.length, 0)
  const exporte = JSON.parse(gunzipSync(fs.readFileSync(path.join(dossier, 'catalogue.json.gz'))))
  assert.deepEqual(exporte.tousExercices[1], { id: 4, notion: 1 })
})

test('fichier corrompu : build refusé', t => {
  const dossier = dossierTemporaire(t)
  ecrireInstantane(sources(), { dossier })
  fs.appendFileSync(path.join(dossier, 'catalogue.json.gz'), 'corruption')
  assert.throws(() => lireInstantane(dossier), /SHA-256/)
})

test('manifeste incohérent : build refusé', t => {
  const dossier = dossierTemporaire(t)
  ecrireInstantane(sources(), { dossier })
  const fichier = path.join(dossier, 'catalogue.json')
  const manifeste = JSON.parse(fs.readFileSync(fichier, 'utf8'))
  manifeste.chapitres = 10
  fs.writeFileSync(fichier, JSON.stringify(manifeste))
  assert.throws(() => lireInstantane(dossier), /incohérent/)
})

test('export absent ou incomplet : build refusé', t => {
  const dossier = dossierTemporaire(t)
  assert.throws(() => lireInstantane(dossier), /ENOENT/)
  assert.throws(() => ecrireInstantane({ ...sources(), fiches: [] }, { dossier }), /incomplet/)
})

test('textes payants ou champs supplémentaires réservés : export refusé', t => {
  const dossier = dossierTemporaire(t)
  const payant = sources()
  payant.exercices[0].is_locked = true
  assert.throws(() => ecrireInstantane(payant, { dossier }), /non publique/)
  const complet = sources()
  complet.tousExercices[1].solution = 'Texte réservé'
  assert.throws(() => ecrireInstantane(complet, { dossier }), /uniquement des identifiants/)
})

test('nouvel export validé remplace l’ancien', t => {
  const dossier = dossierTemporaire(t)
  ecrireInstantane(sources(), { dossier })
  const nouveau = sources()
  nouveau.cours[0].contenu = 'Cours public actualisé'
  ecrireInstantane(nouveau, { dossier })
  assert.equal(lireInstantane(dossier).catalogue.chapitres[0].cours.contenu, 'Cours public actualisé')
  assert.deepEqual(fs.readdirSync(dossier).sort(), ['catalogue.json', 'catalogue.json.gz'])
})
