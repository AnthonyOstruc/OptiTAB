// Rendu des contenus hors navigateur : même moteur d'affichage que le site
// (format OptiTAB v1 et ancien format), formules composées par MathJax (même
// version que le site, en SVG, avec MathML pour l'accessibilité et les
// robots), et version Markdown pour les assistants d'IA.
import { createRequire } from 'node:module'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const FRONT = path.resolve(ICI, '..', '..')
const require = createRequire(path.join(FRONT, 'package.json'))

let moteur = null
let mathjaxPret = null

// Moteur d'affichage du site (src/utils/scientificRenderer.js), empaqueté pour Node.
async function chargerMoteur() {
  if (moteur) return moteur
  const esbuild = require('esbuild')
  const sortie = path.join(os.tmpdir(), `optitab-ressources-moteur-${process.pid}.mjs`)
  await esbuild.build({
    entryPoints: [path.join(FRONT, 'src/utils/scientificRenderer.js')],
    bundle: true,
    format: 'esm',
    platform: 'node',
    outfile: sortie,
    logLevel: 'error'
  })
  moteur = await import(pathToFileURL(sortie).href)
  return moteur
}

function chargerMathJax() {
  if (mathjaxPret) return mathjaxPret
  globalThis.MathJax = {
    loader: {
      paths: { mathjax: 'mathjax/es5' },
      require,
      load: ['adaptors/liteDOM', 'input/tex-full', 'output/svg', 'a11y/assistive-mml']
    },
    // Mêmes délimiteurs et extensions que le site (index.html).
    tex: {
      inlineMath: [['$', '$'], ['\\(', '\\)']],
      displayMath: [['$$', '$$'], ['\\[', '\\]']],
      packages: { '[+]': ['textmacros'] }
    },
    // Un seul jeu de glyphes par page.
    svg: { fontCache: 'global' },
    options: { enableAssistiveMml: true },
    startup: { typeset: false }
  }
  require('mathjax/es5/startup.js')
  mathjaxPret = globalThis.MathJax.startup.promise
  return mathjaxPret
}

export async function preparerRendu() {
  await Promise.all([chargerMoteur(), chargerMathJax()])
}

// Nettoyage du HTML produit : pas de script ni d'attribut d'événement, pas
// d'infobulle tirée d'un nom de fichier, images chargées à la demande.
function nettoyer(html) {
  return html
    .replace(/<script\b[\s\S]*?<\/script>/gi, '')
    .replace(/\son[a-z]+\s*=\s*("[^"]*"|'[^']*')/gi, '')
    .replace(/\stitle="V1 [^"]*"/g, '')
    .replace(/\stitle="[^"]*\.(png|jpe?g|svg|webp)"/gi, '')
}

// Contenu d'un cours, d'une fiche ou d'un exercice → HTML (formules encore en LaTeX).
export function contenuEnHtml(source, images = [], type = 'cours') {
  if (!source) return ''
  const { renderContentWithImages } = moteur
  const brut = type === 'fiche'
    ? String(source).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')
    : String(source)
  return nettoyer(renderContentWithImages(brut, images || [], { imageType: type === 'fiche' ? 'synthesis' : type }))
}

// Compose toutes les formules d'un fragment HTML (une seule passe par page :
// un seul jeu de glyphes). Renvoie le HTML et le nombre de formules.
export function composerFormules(fragment) {
  const MJ = globalThis.MathJax
  const doc = MJ._.mathjax.mathjax.document(`<!DOCTYPE html><html><head></head><body>${fragment}</body></html>`, {
    InputJax: MJ.startup.input,
    OutputJax: MJ.startup.output
  })
  doc.render()
  const adaptor = MJ.startup.adaptor
  const html = adaptor.innerHTML(adaptor.body(doc.document))
  return { html, formules: (html.match(/<mjx-container/g) || []).length }
}

// Feuille de style de MathJax (placement des formules, MathML réservé aux
// lecteurs d'écran), à joindre une fois à la feuille de style des pages.
export function feuilleMathJax() {
  const MJ = globalThis.MathJax
  return MJ.startup.adaptor.textContent(MJ.startup.output.styleSheet(MJ.startup.document))
}

// Texte brut d'un fragment HTML (descriptions, extraits).
export function texteBrut(html, max = 0) {
  let t = String(html || '')
    .replace(/<mjx-assistive-mml[\s\S]*?<\/mjx-assistive-mml>/g, '')
    .replace(/<(script|style|svg)[\s\S]*?<\/\1>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
    .replace(/\s+/g, ' ')
    .trim()
  if (max && t.length > max) t = t.slice(0, max - 1).replace(/\s+\S*$/, '') + '…'
  return t
}

const EXPOSANTS = { 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹', n: 'ⁿ', '+': '⁺', '-': '⁻', i: 'ⁱ', x: 'ˣ' }
const INDICES = { 0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉', n: 'ₙ', '+': '₊', '-': '₋', k: 'ₖ', i: 'ᵢ', p: 'ₚ', x: 'ₓ' }
const enPetit = (texte, table) => ([...texte].every((c) => table[c]) ? [...texte].map((c) => table[c]).join('') : null)

// LaTeX simplifié en texte lisible (pour les descriptions et le sommaire).
export function latexEnTexte(texte) {
  return String(texte || '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/\\(dfrac|frac)\{([^{}]*)\}\{([^{}]*)\}/g, '$2/$3')
    .replace(/\\(mathbb|mathrm|text|textbf|mathcal|operatorname|overrightarrow|vec)\{([^}]*)\}/g, '$2')
    .replace(/\\(left|right|displaystyle|,|;|!|quad|qquad)/g, ' ')
    .replace(/\\(times)/g, '×').replace(/\\(leqslant|leq|le)\b/g, '≤').replace(/\\(geqslant|geq|ge)\b/g, '≥')
    .replace(/\\(infty)/g, '∞').replace(/\\(pi)/g, 'π').replace(/\\(in)\b/g, '∈').replace(/\\(neq|ne)\b/g, '≠')
    .replace(/\^\{([^{}]+)\}|\^([A-Za-z0-9])/g, (m, a, b) => enPetit(a ?? b, EXPOSANTS) ?? `^(${a ?? b})`)
    .replace(/_\{([^{}]+)\}|_([A-Za-z0-9])/g, (m, a, b) => enPetit(a ?? b, INDICES) ?? `_${a ?? b}`)
    .replace(/\\([a-zA-Z]+)/g, '$1')
    .replace(/[{}$]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
}

// Objectifs d'un cours v1 (bloc « ::: objectifs … ::: »), pour la description.
export function objectifs(source) {
  const m = String(source || '').match(/:::\s*objectifs[^\n]*\n([\s\S]*?)\n:::/)
  return m ? latexEnTexte(m[1].replace(/^\s*[-*]\s*/gm, '')) : ''
}

const TITRES_BLOCS = {
  objectifs: 'Objectifs', definition: 'Définition', propriete: 'Propriété', theoreme: 'Théorème',
  methode: 'Méthode', exemple: 'Exemple', remarque: 'Remarque', attention: 'Attention',
  retenir: 'À retenir', formule: 'Formule', demonstration: 'Démonstration', vocabulaire: 'Vocabulaire',
  erreur: 'Erreur fréquente', astuce: 'Astuce', rappel: 'Rappel', notation: 'Notation'
}

// Contenu → Markdown propre (formules en LaTeX, figures avec leur description).
export function contenuEnMarkdown(source, images = []) {
  const texte = String(source || '')
  const parPosition = new Map((images || []).map((im) => [Number(im.position), im]))
  const image = (n) => {
    const im = parPosition.get(Number(n))
    return im ? `![${(im.alt_text_resolved || im.alt_text || 'Figure').replace(/[[\]]/g, '')}](${im.image})` : ''
  }
  if (!/^\s*<!--\s*optitab:1\s*-->/.test(texte)) {
    // Ancien format (HTML) : texte lisible, formules conservées.
    return texteBrut(texte.replace(/<\/(p|div|li|h[1-6]|tr)>/gi, '\n').replace(/<br\s*\/?>/gi, '\n'))
      .replace(/\[\s*IMAGE\s*_?\s*(\d+)\s*\]/gi, (_, n) => image(n))
  }
  return texte
    .replace(/^\s*<!--\s*optitab:1\s*-->\s*/, '')
    .replace(/^:::\s*tableau[^\n]*\n([\s\S]*?)\n:::\s*$/gm, (_, corps) => '```\n' + corps + '\n```')
    .replace(/^:::\s*([a-zé]+)\s*(.*)$/gim, (_, type, titre) => {
      const libelle = TITRES_BLOCS[type.toLowerCase()] || (type.charAt(0).toUpperCase() + type.slice(1))
      return `**${libelle}${titre.trim() ? ' : ' + titre.trim() : ''}**`
    })
    .replace(/^:::\s*$/gm, '')
    .replace(/\[\s*IMAGE\s*_?\s*(\d+)\s*\]/gi, (_, n) => image(n))
    .replace(/\n{3,}/g, '\n\n')
    .trim()
}
