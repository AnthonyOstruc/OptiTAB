// Tableau périodique interactif (page physique-chimie/tableau-periodique).
//
// La grille des 118 éléments est écrite dans la page à la construction, à partir
// de contenu/physique-chimie/tableau-periodique/elements.json (données vérifiées
// par construire_elements.py) : tout est lisible sans JavaScript. Le script
// outils/tableau-periodique.js affiche la fiche de l'élément touché.
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const DONNEES = path.resolve(ICI, '../../contenu/physique-chimie/tableau-periodique/elements.json')
const e = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')

export const FAMILLES = [
  ['alcalin', 'Métaux alcalins'],
  ['alcalino-terreux', 'Métaux alcalino-terreux'],
  ['transition', 'Métaux de transition'],
  ['metal-pauvre', 'Métaux pauvres'],
  ['lanthanide', 'Lanthanides'],
  ['actinide', 'Actinides'],
  ['metalloide', 'Métalloïdes'],
  ['non-metal', 'Non-métaux'],
  ['halogene', 'Halogènes'],
  ['gaz-noble', 'Gaz nobles']
]
const NOM_FAMILLE = Object.fromEntries(FAMILLES)
// Au singulier dans la fiche d'un élément.
const UNE_FAMILLE = {
  alcalin: 'métal alcalin', 'alcalino-terreux': 'métal alcalino-terreux', transition: 'métal de transition',
  'metal-pauvre': 'métal pauvre', lanthanide: 'lanthanide', actinide: 'actinide', metalloide: 'métalloïde',
  'non-metal': 'non-métal', halogene: 'halogène', 'gaz-noble': 'gaz noble'
}

let cache = null
export function elements() {
  if (!cache) {
    cache = JSON.parse(fs.readFileSync(DONNEES, 'utf8'))
    if (cache.length !== 118) throw new Error(`tableau périodique : ${cache.length} éléments au lieu de 118`)
  }
  return cache
}

// Place dans la grille : colonne = groupe, ligne = période + 1 (la ligne 1 porte les
// numéros des groupes 1 et 18). Lanthanides et actinides : lignes 10 et 11, à partir
// de la colonne 3 (la ligne 9 sert d'espace).
function place(el) {
  if (el.groupe) return [el.groupe, el.periode + 1]
  const debut = el.periode === 6 ? 57 : 89
  return [3 + el.z - debut, el.periode === 6 ? 10 : 11]
}

// Ligne des numéros de groupe : au-dessus du premier élément de chaque colonne.
const HAUT_DU_GROUPE = { 1: 1, 2: 2, 13: 2, 14: 2, 15: 2, 16: 2, 17: 2, 18: 1 }
const hautDuGroupe = (g) => HAUT_DU_GROUPE[g] || 4

const ESC_NBSP = String.fromCharCode(160) // espace insécable entre la valeur et l'unité

// Informations de la fiche (données de l'élément, en clair dans la page).
function donnees(el) {
  return {
    z: el.z, s: el.s, n: el.nom, m: el.m, f: UNE_FAMILLE[el.famille], p: el.periode,
    g: el.groupe || (el.periode === 6 ? 'lanthanides' : 'actinides'), b: el.bloc,
    en: el.en || '', c: el.config || '', v: el.valence ?? ''
  }
}

// « 1s2 2s2 2p5 » → 1s² 2s² 2p⁵ (même règle dans outils/tableau-periodique.js).
const exposants = (t) => t.replace(/(\d[spdf])(\d+)/g, '$1<sup>$2</sup>')

export function fiche(el) {
  const d = donnees(el)
  const ligne = (terme, valeur) => (valeur === '' || valeur == null ? '' : `<div><dt>${terme}</dt><dd>${valeur}</dd></div>`)
  const masse = d.m.startsWith('[') ? `${e(d.m)}${ESC_NBSP}(élément radioactif)` : `${e(d.m)}${ESC_NBSP}g/mol`
  return `<div class="tp__fiche-tete tp--${el.famille}">
      <span class="tp__fiche-z">${d.z}</span>
      <span class="tp__fiche-s">${e(d.s)}</span>
    </div>
    <div class="tp__fiche-corps">
      <p class="tp__fiche-nom">${e(d.n)}</p>
      <dl class="tp__fiche-dl">
        ${ligne('Numéro atomique', `Z = ${d.z}`)}
        ${ligne('Masse molaire', masse)}
        ${ligne('Famille', e(d.f))}
        ${ligne('Période', d.p)}
        ${ligne('Groupe', e(d.g))}
        ${ligne('Bloc', e(d.b))}
        ${ligne('Électronégativité', e(d.en))}
        ${ligne('Configuration électronique', exposants(e(d.c)))}
        ${ligne('Électrons de valence', d.v)}
      </dl>
    </div>`
}

export function tableauPeriodiqueHtml() {
  const els = elements()
  const fer = els[25]
  const cases = els.map((el) => {
    const [col, lig] = place(el)
    const d = donnees(el)
    const attributs = Object.entries(d).map(([k, v]) => `data-${k}="${e(v)}"`).join(' ')
    return `<li style="grid-column:${col};grid-row:${lig}"><button type="button" class="tp__el tp--${el.famille}" ${attributs} aria-pressed="${el.z === 26}" aria-label="${e(`${el.nom}, ${el.s}, numéro atomique ${el.z}`)}"><span class="tp__z">${el.z}</span><span class="tp__s">${e(el.s)}</span></button></li>`
  }).join('')
  const groupes = Array.from({ length: 18 }, (_, i) => i + 1)
    .map((g) => `<li class="tp__groupe" style="grid-column:${g};grid-row:${hautDuGroupe(g)}" aria-hidden="true">${g}</li>`).join('')
  const renvois = `<li class="tp__renvoi tp--lanthanide" style="grid-column:3;grid-row:7" aria-hidden="true">57-71</li>`
    + `<li class="tp__renvoi tp--actinide" style="grid-column:3;grid-row:8" aria-hidden="true">89-103</li>`
  const legende = FAMILLES.map(([cle, nom]) => `<li><span class="tp__pastille tp--${cle}" aria-hidden="true"></span>${e(nom)}</li>`).join('')
  return `<section class="tp" data-outil="tableau-periodique" aria-labelledby="otc-tableau-periodique-titre">
  <div class="tp__tete">
    <p class="otc__kicker">Outil gratuit</p>
    <p class="otc__titre" id="otc-tableau-periodique-titre">Tableau périodique interactif</p>
    <p class="otc__intro">Touchez un élément pour afficher sa fiche : masse molaire, famille, position, électronégativité et, jusqu’au chlore et à l’argon, configuration électronique.</p>
  </div>
  <p class="tp__glisser" aria-hidden="true">Faites glisser le tableau →</p>
  <div class="tp__defile" tabindex="0" role="region" aria-label="Tableau périodique des 118 éléments (défilement horizontal sur téléphone)">
    <ol class="tp__grille">${groupes}${renvois}${cases}</ol>
  </div>
  <ul class="tp__legende" aria-label="Familles d’éléments">${legende}</ul>
  <div class="tp__fiche" data-fiche aria-live="polite">
    ${fiche(fer)}
  </div>
</section>`
}

export { NOM_FAMILLE }
