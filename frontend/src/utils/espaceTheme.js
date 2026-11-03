import {
  AcademicCapIcon,
  ChartPieIcon,
  CodeBracketIcon,
  CubeTransparentIcon,
  PresentationChartLineIcon,
  SparklesIcon,
  Squares2X2Icon,
  VariableIcon
} from '@heroicons/vue/24/outline'

// Une couleur et une icône par thème du programme (Analyse, Probabilités…),
// pour repérer chaque partie d'un coup d'œil. Couleurs accordées au logo.
const PALETTE = [
  { c: '#1b3c8e', bg: '#eef1f8' }, // marine
  { c: '#3b8544', bg: '#eaf4ea' }, // vert
  { c: '#6d45b8', bg: '#f2edfa' }, // violet
  { c: '#b8620f', bg: '#fdf2e4' }, // orange
  { c: '#0e7482', bg: '#e6f4f5' }, // sarcelle
  { c: '#b03a5f', bg: '#fbecf1' } // framboise
]

const ICONES = [
  [/analyse|fonction|suite|d[ée]riv|int[ée]gr/i, PresentationChartLineIcon],
  [/probab|statist|d[ée]nombr|al[ée]atoire/i, ChartPieIcon],
  [/g[ée]om|espace|vecteur|trigono/i, CubeTransparentIcon],
  [/algo|program|informatique|python/i, CodeBracketIcon],
  [/expert|complexe|arithm|matrice/i, SparklesIcon],
  [/bac|brevet|examen|sujet/i, AcademicCapIcon],
  [/alg[èe]bre|calcul|nombre|[ée]quation/i, VariableIcon]
]

export function iconeTheme(titre = '') {
  return ICONES.find(([re]) => re.test(titre))?.[1] || Squares2X2Icon
}

// Index stable de chaque thème dans l'ordre du programme.
export function indexThemes(chapitres = []) {
  const index = new Map()
  chapitres.forEach((c) => { if (!index.has(c.theme_id)) index.set(c.theme_id, index.size) })
  return index
}

export function visuelTheme(titre, index = 0) {
  const p = PALETTE[index % PALETTE.length]
  return { icone: iconeTheme(titre), style: { '--t': p.c, '--t-bg': p.bg } }
}
