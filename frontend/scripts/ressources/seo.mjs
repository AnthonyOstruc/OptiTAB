// Référencement des ressources gratuites : données structurées (schema.org),
// plan du site avec images, llms.txt et versions Markdown pour les IA,
// correspondance des anciennes adresses.
import { CYCLES } from './classes.mjs'
import {
  RACINE, SITE, absolu, etapesAriane, titreExercice,
  urlClasse, urlCours, urlExercices, urlFiche, urlMarkdown
} from './pages.mjs'
import { contenuEnMarkdown, latexEnTexte } from './rendu.mjs'

export const ORGANISATION = {
  '@type': 'EducationalOrganization',
  '@id': `${SITE}/#organisation`,
  name: 'OptiTAB',
  url: `${SITE}/`,
  logo: `${SITE}/Logo_bg.png`,
  email: 'contact@optitab.net',
  sameAs: ['https://instagram.com/opti.tab', 'https://facebook.com/optitab', 'https://tiktok.com/@optitab']
}
const EDITEUR = { '@id': `${SITE}/#organisation` }

export const FAQ = [
  ['Les ressources OptiTAB sont-elles vraiment gratuites ?',
    'Oui. Tous les cours, toutes les fiches de révision et plusieurs exercices corrigés par chapitre sont en accès libre, sans inscription ni carte bancaire.'],
  ['Les cours suivent-ils le programme officiel ?',
    'Oui. Chaque classe, du CP à la Terminale, suit le programme de mathématiques de l’Éducation nationale, chapitre par chapitre.'],
  ['Comment sont faits les exercices corrigés ?',
    'Chaque exercice a une correction détaillée, étape par étape, puis les réponses. Ils vont du plus simple au plus complet : on cherche d’abord, puis on compare avec la correction.'],
  ['Que propose l’abonnement en plus ?',
    'Tous les exercices corrigés de chaque chapitre (plus de 3 900), le suivi des progrès, les exercices à revoir et un espace parent. <a href="/tarifs">Voir les formules</a>.'],
  ['Proposez-vous des cours particuliers de maths ?',
    'Oui : des cours particuliers en ligne en maths, physique-chimie et informatique, du collège à la prépa, avec un professeur expérimenté. <a href="/cours-particuliers">Découvrir les cours particuliers</a>.']
]

const texteSansBalises = (html) => String(html).replace(/<[^>]+>/g, '')

export function ariane(etapes) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: etapes.map(([nom, href], i) => ({ '@type': 'ListItem', position: i + 1, name: nom, item: absolu(href) }))
  }
}

function alignement(classe) {
  return {
    '@type': 'AlignmentObject',
    alignmentType: 'educationalLevel',
    educationalFramework: 'Programme de mathématiques de l’Éducation nationale (France)',
    targetName: classe.court
  }
}

export function jsonldChapitre(ch, page, { description, image, nbFormules }) {
  const url = absolu({ cours: urlCours(ch), fiche: urlFiche(ch), exercices: urlExercices(ch) }[page])
  const type = { cours: 'Cours', fiche: 'Fiche de révision', exercices: 'Exercices corrigés' }[page]
  const ressource = {
    '@context': 'https://schema.org',
    '@type': 'LearningResource',
    '@id': `${url}#ressource`,
    name: `${ch.titre} : ${type.toLowerCase()} de maths ${ch.classe.court}`,
    description,
    url,
    inLanguage: 'fr-FR',
    learningResourceType: type,
    educationalLevel: ch.classe.court,
    educationalAlignment: alignement(ch.classe),
    about: { '@type': 'Thing', name: ch.titre },
    teaches: ch.titre,
    keywords: [ch.titre, ch.theme, `maths ${ch.classe.court}`, type.toLowerCase()].join(', '),
    isAccessibleForFree: true,
    audience: { '@type': 'EducationalAudience', educationalRole: 'student' },
    isPartOf: { '@type': 'CollectionPage', '@id': `${absolu(urlClasse(ch.classe))}#collection`, name: `Maths ${ch.classe.court}` },
    provider: EDITEUR,
    publisher: EDITEUR,
    ...(ch.modifie ? { dateModified: ch.modifie } : {}),
    ...(image ? { image } : {}),
    ...(page === 'exercices' ? {
      hasPart: ch.exercices.map((ex, i) => ({
        '@type': 'LearningResource',
        name: `Exercice ${i + 1} : ${titreExercice(ex)}`,
        learningResourceType: 'Exercice corrigé',
        url: `${url}#exercice-${ex.id}`
      }))
    } : {})
  }
  return [ressource, ariane(etapesAriane(ch.classe, ch, page))]
}

export function jsonldClasse(classe) {
  const url = absolu(urlClasse(classe))
  return [{
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    '@id': `${url}#collection`,
    name: `Maths ${classe.court} : cours, fiches et exercices corrigés`,
    description: classe.intro,
    url,
    inLanguage: 'fr-FR',
    isAccessibleForFree: true,
    educationalLevel: classe.court,
    publisher: EDITEUR,
    mainEntity: {
      '@type': 'ItemList',
      numberOfItems: classe.chapitres.length,
      itemListElement: classe.chapitres.map((ch, i) => ({ '@type': 'ListItem', position: i + 1, name: ch.titre, url: absolu(urlCours(ch)) }))
    }
  }, ariane(etapesAriane(classe))]
}

export function jsonldAccueil(catalogue) {
  const url = absolu(RACINE)
  return [
    { '@context': 'https://schema.org', ...ORGANISATION },
    {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: 'Cours de maths gratuits du CP à la Terminale',
      url,
      inLanguage: 'fr-FR',
      isAccessibleForFree: true,
      publisher: EDITEUR,
      hasPart: catalogue.classes.map((c) => ({ '@type': 'CollectionPage', name: `Maths ${c.court}`, url: absolu(urlClasse(c)) }))
    },
    {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: FAQ.map(([q, r]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: texteSansBalises(r) } }))
    },
    ariane([['Accueil', '/'], ['Ressources gratuites', RACINE]])
  ]
}

// ---------- Plan du site (avec images) ----------
const xml = (t) => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')

export function planDuSite(entrees) {
  const lignes = entrees.map(({ chemin, modifie, images = [] }) => {
    const date = modifie ? `<lastmod>${String(modifie).slice(0, 10)}</lastmod>` : ''
    const imgs = images.slice(0, 50).map((u) => `<image:image><image:loc>${xml(u)}</image:loc></image:image>`).join('')
    return `<url><loc>${xml(absolu(chemin))}</loc>${date}${imgs}</url>`
  })
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
${lignes.join('\n')}
</urlset>
`
}

// ---------- Pour les assistants d'IA ----------
export function llmsTxt(catalogue) {
  const t = catalogue.totaux
  const classes = CYCLES.map((cy) => {
    const liste = catalogue.classes.filter((c) => c.cycle === cy.cle)
    return liste.length ? `\n## ${cy.titre}\n\n${liste.map((c) => `- [Maths ${c.court}](${absolu(urlClasse(c))}) : ${c.accroche} Version texte : ${absolu(urlClasse(c))}index.md`).join('\n')}` : ''
  }).join('\n')
  return `# OptiTAB : cours de maths gratuits, du CP à la Terminale

> OptiTAB publie en accès libre ${t.cours} cours de mathématiques complets, ${t.fiches} fiches de révision et ${t.exercicesGratuits} exercices corrigés pas à pas, du CP à la Terminale, conformes au programme de l’Éducation nationale (France). Chaque chapitre a une page « cours », une page « fiche de révision » et une page « exercices corrigés », ainsi qu’une version texte en Markdown (formules en LaTeX). OptiTAB propose aussi une plateforme d’entraînement sur abonnement (plus de 3 900 exercices corrigés, suivi des progrès) et des cours particuliers en ligne en maths, physique-chimie et informatique, du collège à la prépa.

- Accueil des ressources gratuites : ${absolu(RACINE)}
- Cours particuliers de maths en ligne : ${SITE}/cours-particuliers
- Tarifs de la plateforme : ${SITE}/tarifs
- Contact : contact@optitab.net
${classes}
`
}

export function markdownChapitre(ch) {
  const lignes = [
    `# ${ch.titre} : maths ${ch.classe.court}`,
    '',
    `Chapitre ${ch.numero} du programme de mathématiques de ${ch.classe.court} (thème : ${ch.theme}). Ressource gratuite OptiTAB.`,
    '',
    `- Cours : ${absolu(urlCours(ch))}`,
    ...(ch.fiche ? [`- Fiche de révision : ${absolu(urlFiche(ch))}`] : []),
    ...(ch.exercices.length ? [`- Exercices corrigés : ${absolu(urlExercices(ch))}`] : []),
    '',
    '## Cours',
    '',
    contenuEnMarkdown(ch.cours.contenu, ch.cours.images)
  ]
  if (ch.fiche) lignes.push('', '## Fiche de révision', '', contenuEnMarkdown(ch.fiche.contenu, ch.fiche.images))
  if (ch.exercices.length) {
    lignes.push('', '## Exercices corrigés')
    ch.exercices.forEach((ex, i) => {
      lignes.push('', `### Exercice ${i + 1} : ${titreExercice(ex)}`, '', contenuEnMarkdown(ex.contenu || ex.question, ex.images))
      if (ex.etapes) lignes.push('', '#### Correction détaillée', '', contenuEnMarkdown(ex.etapes, ex.images))
      if (ex.solution) lignes.push('', '#### Réponses', '', contenuEnMarkdown(ex.solution, ex.images))
    })
  }
  return lignes.join('\n') + '\n'
}

export function markdownClasse(classe) {
  return [
    `# Maths ${classe.court} : cours, fiches et exercices corrigés (OptiTAB)`,
    '',
    classe.intro,
    '',
    ...classe.themes.flatMap((t) => [`## ${t.titre}`, '', ...t.chapitres.map((ch) => `- [${ch.titre}](${absolu(urlCours(ch))}) : version texte ${absolu(urlMarkdown(ch))}`), ''])
  ].join('\n')
}

// ---------- Anciennes adresses → nouvelles pages ----------
export function correspondances(catalogue) {
  const table = { cours: {}, fiche: {}, notion: {}, exercice: {} }
  for (const ch of catalogue.chapitres) {
    table.cours[ch.cours.id] = urlCours(ch)
    if (ch.fiche) table.fiche[ch.fiche.id] = urlFiche(ch)
    table.notion[ch.notionId] = ch.exercices.length ? urlExercices(ch) : urlCours(ch)
    for (const ex of ch.exercices) table.exercice[ex.id] = `${urlExercices(ch)}#exercice-${ex.id}`
  }
  return table
}

export const descriptionCourte = (texte, max = 158) => {
  const t = latexEnTexte(texte)
  return t.length > max ? t.slice(0, max - 1).replace(/\s+\S*$/, '') + '…' : t
}
