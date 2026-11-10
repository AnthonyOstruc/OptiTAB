// Blog OptiTAB (pages statiques, générées avec les ressources gratuites).
// Les articles sont des fichiers Markdown de frontend/contenu/blog/ : un bloc
// d'informations en JSON entre deux lignes « --- », puis le texte. Chaque
// article devient une page complète (texte, sommaire, FAQ, données
// structurées) lisible par Google et les assistants d'IA sans JavaScript.
// Les articles sont signés par l'équipe pédagogique, sans nom de personne
// (comme Groupe Réussite, Acadomia ou Kartable).
import fs from 'node:fs'
import path from 'node:path'
import { marked } from 'marked'
import { CLASSES } from './classes.mjs'
import { SITE, absolu, appelsAction, e, filAriane } from './pages.mjs'
import { ORGANISATION, ariane } from './seo.mjs'
import { slugifier } from './catalogue.mjs'

export const RACINE_BLOG = '/blog/'
export const urlArticle = (a) => `${RACINE_BLOG}${a.slug}/`

// Anciennes adresses du blog (articles retirés le 2026-11-03, catégories,
// étiquettes) : elles mènent à l'accueil du blog.
export const ANCIENNES_ADRESSES = [
  'comment-reviser-bac-maths-efficacement/',
  'erreurs-frequentes-bac-maths/',
  'comment-combler-lacunes-maths-lycee/',
  'categorie/',
  'tag/'
]

const SIGNATURE = 'l’équipe pédagogique OptiTAB'

const ICONES = {
  fleche: '<path d="M5 12h14M13 6l6 6-6 6"/>',
  horloge: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  calendrier: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  eclair: '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
  livre: '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>'
}
const icone = (nom, cls = 'rg-ico') => `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">${ICONES[nom]}</svg>`

const dateLongue = (iso) => new Date(`${iso}T12:00:00`).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
const sansBalises = (html) => String(html).replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim()
// Typographie française : espace insécable avant ? ! : ; (jamais de signe seul
// en début de ligne). Appliquée au texte seulement, pas aux balises.
const typo = (texte) => String(texte).replace(/ ([?!:;])/g, ' $1')
const typoHtml = (html) => String(html).split(/(<[^>]+>)/).map((morceau) => (morceau.startsWith('<') ? morceau : typo(morceau))).join('')

// ---------- Lecture des articles ----------

function lireArticle(fichier) {
  const source = fs.readFileSync(fichier, 'utf8').replace(/\r\n/g, '\n')
  const m = source.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/)
  if (!m) throw new Error(`${path.basename(fichier)} : bloc d'informations (--- … ---) introuvable`)
  const info = JSON.parse(m[1])
  for (const champ of ['slug', 'titre', 'description', 'publie']) {
    if (!info[champ]) throw new Error(`${path.basename(fichier)} : champ « ${champ} » manquant`)
  }
  const markdown = m[2].trim()

  // Titres de parties : identifiant stable pour le sommaire et les liens directs.
  const titres = []
  const vus = new Set()
  let html = marked.parse(markdown, { gfm: true }).replace(/<h2>([\s\S]*?)<\/h2>/g, (tout, interieur) => {
    let id = slugifier(sansBalises(interieur), 60)
    while (vus.has(id)) id += '-2'
    vus.add(id)
    titres.push({ id, texte: sansBalises(interieur) })
    return `<h2 id="${id}">${interieur}</h2>`
  })
  // Liens sortants : nouvel onglet, sans transmettre de droits.
  html = html.replace(/<a href="(https?:\/\/(?!www\.optitab\.net)[^"]+)"/g, '<a href="$1" target="_blank" rel="noopener nofollow"')
  // Tableaux comparatifs : chaque cellule reçoit le titre de sa colonne
  // (data-label), affiché devant la valeur quand le tableau passe en fiches
  // empilées sur téléphone (voir .bl-table dans blog.css).
  html = html.replace(/<div class="bl-table"[\s\S]*?<\/table>/g, (bloc) => {
    const titres = [...((bloc.match(/<thead>([\s\S]*?)<\/thead>/) || [])[1] || '').matchAll(/<th\b[^>]*>([\s\S]*?)<\/th>/g)]
      .map((m) => sansBalises(m[1]).replace(/"/g, '&quot;'))
    return bloc.replace(/<tr>([\s\S]*?)<\/tr>/g, (ligne, cellules) => {
      let k = 0
      return `<tr>${cellules.replace(/<(th scope="row"|td)>/g, (o, b) => `<${b} data-label="${titres[k++] || ''}">`)}</tr>`
    })
  })

  const mots = sansBalises(html).split(' ').filter(Boolean).length
  return {
    ...info,
    titre: typo(info.titre),
    modifie: info.modifie || info.publie,
    markdown,
    html: typoHtml(html),
    titres: titres.map((t) => ({ ...t, texte: typo(t.texte) })),
    mots,
    lecture: Math.max(1, Math.round(mots / 220)),
    enBref: (info.enBref || []).map(typo),
    faq: (info.faq || []).map(([q, r]) => [typo(q), typo(r)]),
    lireAussi: info.lireAussi || [],
    classes: (info.liensClasses || []).map((slug) => CLASSES.find((c) => c.slug === slug)).filter(Boolean)
  }
}

export function lireArticles(dossier) {
  if (!fs.existsSync(dossier)) return []
  const articles = fs.readdirSync(dossier)
    .filter((f) => f.endsWith('.md'))
    .map((f) => lireArticle(path.join(dossier, f)))
    .filter((a) => !a.brouillon)
  const slugs = new Set(articles.map((a) => a.slug))
  if (slugs.size !== articles.length) throw new Error('Deux articles ont la même adresse')
  for (const a of articles) {
    for (const s of a.lireAussi) if (!slugs.has(s)) throw new Error(`${a.slug} : « lireAussi » vers un article inconnu (${s})`)
    for (const [, lien] of a.html.matchAll(/href="\/blog\/([^"/#]+)\/?/g)) {
      if (!slugs.has(lien)) throw new Error(`${a.slug} : lien vers un article inconnu (/blog/${lien}/)`)
    }
  }
  // Ordre : date de publication (plus récent d'abord), puis « ordre » si indiqué.
  return articles.sort((a, b) => String(b.publie).localeCompare(String(a.publie)) || (a.ordre ?? 99) - (b.ordre ?? 99))
}

// ---------- Morceaux de page ----------

function ligneAuteur(a) {
  const date = a.modifie !== a.publie
    ? `Mis à jour le <time datetime="${a.modifie}">${dateLongue(a.modifie)}</time>`
    : `Publié le <time datetime="${a.publie}">${dateLongue(a.publie)}</time>`
  return `<div class="bl-byline">
      <span class="bl-byline__logo" aria-hidden="true"><img src="/favicon.png" alt="" width="26" height="26"></span>
      <div>
        <p class="bl-byline__nom">Par ${SIGNATURE}</p>
        <p class="bl-byline__meta"><span>${icone('calendrier')}${date}</span><span>${icone('horloge')}${a.lecture} min de lecture</span></p>
      </div>
    </div>`
}

// Encadré d'action placé au milieu de l'article, avant la 3e partie.
function encartMilieu() {
  return `<aside class="bl-pause" aria-label="Essayer OptiTAB">
  <div>
    <p class="bl-pause__titre">Essayez la méthode sur un vrai chapitre</p>
    <p>Cours, fiche de révision et exercices corrigés pas à pas : tout est gratuit, sans inscription, du CP à la Terminale.</p>
  </div>
  <a class="rg-btn rg-btn--primary" href="/ressources-gratuites/" data-cta-name="free_resources" data-cta-location="blog_article_milieu">Voir les cours gratuits ${icone('fleche')}</a>
</aside>`
}

function avecEncart(html) {
  let n = 0
  return html.replace(/<h2 /g, (tout) => (++n === 3 ? `${encartMilieu()}\n<h2 ` : tout))
}

function sommaire(a) {
  if (a.titres.length < 3) return ''
  return `<aside class="rg-toc bl-toc" aria-label="Sommaire de l’article">
    <details class="rg-toc__box" open><summary>Sommaire</summary><ol>${a.titres.map((t) => `<li><a href="#${t.id}">${e(t.texte)}</a></li>`).join('')}${a.faq.length ? '<li><a href="#questions-frequentes">Questions fréquentes</a></li>' : ''}</ol></details>
    <div class="bl-toc__cta">
      <p><strong>Un chapitre qui bloque ?</strong> Cours, fiches et exercices corrigés gratuits.</p>
      <a href="/ressources-gratuites/" data-cta-name="free_resources" data-cta-location="blog_sommaire">Voir les cours ${icone('fleche')}</a>
    </div>
  </aside>`
}

function blocClasses(a) {
  const classes = a.classes.length ? a.classes : CLASSES.filter((c) => c.cycle !== 'primaire')
  return `<section class="bl-classes" aria-labelledby="bl-classes-titre">
    <h2 id="bl-classes-titre">Cours de maths gratuits par classe</h2>
    <p>Chaque chapitre du programme, avec son cours, sa fiche de révision et ses exercices corrigés.</p>
    <ul>${classes.map((c) => `<li><a href="/ressources-gratuites/maths/${c.slug}/">${icone('livre')}Maths ${e(c.court)}</a></li>`).join('')}<li><a href="/ressources-gratuites/" class="bl-classes__tout">Toutes les classes ${icone('fleche')}</a></li></ul>
  </section>`
}

function blocFaq(a) {
  if (!a.faq.length) return ''
  return `<section class="rg-faq bl-faq" aria-labelledby="questions-frequentes">
    <h2 id="questions-frequentes">Questions fréquentes</h2>
    ${a.faq.map(([q, r]) => `<details class="rg-faq__item"><summary>${e(q)}</summary><p>${e(r)}</p></details>`).join('\n    ')}
  </section>`
}

function carte(a, { une = false, niveauTitre = 3 } = {}) {
  return `<article class="bl-card${une ? ' bl-card--une' : ''}">
    ${a.image ? `<a href="${urlArticle(a)}" class="bl-card__img" tabindex="-1" aria-hidden="true"><img src="${a.image}" alt="" width="1200" height="630"${une ? '' : ' loading="lazy"'}></a>` : ''}
    <div class="bl-card__body">
      <p class="bl-card__rubrique">${e(a.rubrique || 'Conseils')}</p>
      <h${niveauTitre} class="bl-card__titre"><a href="${urlArticle(a)}">${e(a.titre)}</a></h${niveauTitre}>
      ${une ? `<p class="bl-card__desc">${e(a.description)}</p>` : ''}
      <p class="bl-card__meta">${icone('horloge')}<span>${a.lecture} min de lecture</span></p>
      ${une ? `<a class="rg-btn rg-btn--primary bl-card__cta" href="${urlArticle(a)}">Lire l’article ${icone('fleche')}</a>` : `<a class="bl-card__lire" href="${urlArticle(a)}" tabindex="-1" aria-hidden="true">Lire l’article ${icone('fleche')}</a>`}
    </div>
  </article>`
}

// « D'autres articles pourraient vous intéresser » : ceux choisis dans
// « lireAussi », complétés par les plus récents.
function suggestions(a, articles) {
  const choisis = a.lireAussi.map((s) => articles.find((x) => x.slug === s)).filter(Boolean)
  const autres = articles.filter((x) => x.slug !== a.slug && !choisis.includes(x))
  const liste = [...choisis, ...autres].slice(0, 3)
  if (!liste.length) return ''
  return `<section class="bl-suggestions" aria-labelledby="bl-suggestions-titre">
  <div class="rg-wrap">
    <h2 id="bl-suggestions-titre">D’autres articles pourraient vous intéresser</h2>
    <div class="bl-grille">${liste.map((x) => carte(x)).join('')}</div>
  </div>
</section>`
}

// ---------- Pages ----------

export function pageArticle(a, articles) {
  return `<header class="rg-chap bl-head">
  <div class="rg-wrap">
    ${filAriane([['Accueil', '/'], ['Blog', RACINE_BLOG], [a.titreCourt || a.titre, urlArticle(a)]])}
    <p class="rg-kicker">${e(a.rubrique || 'Conseils')}</p>
    <h1 class="rg-h1 bl-h1">${e(a.titre)}</h1>
    ${a.chapo ? `<p class="rg-lead bl-chapo">${e(a.chapo)}</p>` : ''}
    ${ligneAuteur(a)}
  </div>
</header>
<div class="rg-wrap rg-reading${a.titres.length >= 3 ? ' rg-reading--toc' : ''}">
  ${sommaire(a)}
  <article class="rg-doc bl-article">
    ${a.image ? `<figure class="bl-cover"><img src="${a.image}" alt="${e(a.imageAlt || a.titre)}" width="1200" height="630" fetchpriority="high"></figure>` : ''}
    ${a.enBref.length ? `<section class="bl-bref" aria-label="En bref"><p class="bl-bref__titre">${icone('eclair')} L’essentiel</p><ul>${a.enBref.map((x) => `<li>${e(x)}</li>`).join('')}</ul></section>` : ''}
    <div class="bl-prose">
${avecEncart(a.html)}
    </div>
    <section class="bl-fin" aria-label="Passer à l’action">
      <p class="bl-fin__titre">Prêt à progresser en maths ?</p>
      <p>Commencez gratuitement : tous les cours et toutes les fiches sont en libre accès. Quand vous voulez aller plus loin, l’abonnement débloque tous les exercices corrigés et le suivi des progrès.</p>
      <div class="bl-fin__actions">
        <a class="rg-btn rg-btn--primary" href="/?compte=inscription" data-cta-name="signup" data-cta-location="blog_article_fin">Créer mon compte gratuit ${icone('fleche')}</a>
        <a class="rg-btn rg-btn--ghost" href="/tarifs" data-cta-name="pricing" data-cta-location="blog_article_fin">Voir les formules</a>
      </div>
      <p class="bl-fin__rassurance">Sans carte bancaire · Sans engagement · Ordinateur, tablette et téléphone</p>
    </section>
    ${blocFaq(a)}
    ${blocClasses(a)}
  </article>
</div>
${suggestions(a, articles)}
<div class="rg-wrap">${appelsAction(null, null, 'blog_article')}</div>`
}

export function pageBlog(articles) {
  const une = articles.find((a) => a.une) || articles[0]
  const autres = articles.filter((a) => a !== une)
  return `<header class="rg-chap bl-head bl-head--blog">
  <div class="rg-wrap">
    ${filAriane([['Accueil', '/'], ['Blog', RACINE_BLOG]])}
    <p class="rg-kicker">Le blog OptiTAB</p>
    <h1 class="rg-h1">Conseils et méthodes pour progresser en maths</h1>
    <p class="rg-lead">Travailler un chapitre, préparer le brevet ou le bac, choisir un cours particulier, accompagner son enfant : des conseils concrets, écrits par des professeurs de maths.</p>
  </div>
</header>
<div class="rg-wrap bl-liste">
  ${une ? carte(une, { une: true, niveauTitre: 2 }) : '<p class="bl-vide">Les premiers articles arrivent bientôt.</p>'}
  ${autres.length ? `<section aria-labelledby="bl-autres"><h2 id="bl-autres" class="bl-liste__titre">Tous les articles</h2><div class="bl-grille">${autres.map((a) => carte(a)).join('')}</div></section>` : ''}
  ${blocClasses({ classes: [] })}
</div>
<div class="rg-wrap">${appelsAction(null, null, 'blog_accueil')}</div>`
}

// ---------- Référencement ----------

const ORGA = { '@type': 'EducationalOrganization', '@id': ORGANISATION['@id'], name: ORGANISATION.name, url: ORGANISATION.url, logo: ORGANISATION.logo }
const AUTEUR = { '@type': 'Organization', name: 'Équipe pédagogique OptiTAB', url: `${SITE}/`, parentOrganization: { '@id': ORGANISATION['@id'] } }

export function jsonldArticle(a) {
  const url = absolu(urlArticle(a))
  return [
    {
      '@context': 'https://schema.org',
      '@type': 'BlogPosting',
      '@id': `${url}#article`,
      headline: a.titre.length > 110 ? a.titreSeo || a.titre.slice(0, 110) : a.titre,
      description: a.description,
      image: a.image ? [absolu(a.image)] : undefined,
      datePublished: `${a.publie}T08:00:00+01:00`,
      dateModified: `${a.modifie}T08:00:00+01:00`,
      author: AUTEUR,
      publisher: ORGA,
      mainEntityOfPage: { '@type': 'WebPage', '@id': url },
      isPartOf: { '@type': 'Blog', '@id': `${absolu(RACINE_BLOG)}#blog`, name: 'Le blog OptiTAB' },
      articleSection: a.rubrique || 'Conseils',
      keywords: (a.motsCles || []).join(', '),
      wordCount: a.mots,
      timeRequired: `PT${a.lecture}M`,
      inLanguage: 'fr-FR',
      isAccessibleForFree: true
    },
    a.faq.length ? {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: a.faq.map(([q, r]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: r } }))
    } : null,
    ariane([['Accueil', '/'], ['Blog', RACINE_BLOG], [a.titreCourt || a.titre, urlArticle(a)]])
  ].filter(Boolean)
}

export function jsonldBlog(articles) {
  return [
    { '@context': 'https://schema.org', ...ORGANISATION },
    {
      '@context': 'https://schema.org',
      '@type': 'Blog',
      '@id': `${absolu(RACINE_BLOG)}#blog`,
      name: 'Le blog OptiTAB',
      description: 'Conseils et méthodes pour progresser en maths, du collège au lycée.',
      url: absolu(RACINE_BLOG),
      inLanguage: 'fr-FR',
      publisher: ORGA,
      blogPost: articles.map((a) => ({
        '@type': 'BlogPosting',
        headline: a.titre,
        url: absolu(urlArticle(a)),
        datePublished: `${a.publie}T08:00:00+01:00`,
        dateModified: `${a.modifie}T08:00:00+01:00`,
        image: a.image ? absolu(a.image) : undefined,
        author: { '@type': 'Organization', name: AUTEUR.name }
      }))
    },
    ariane([['Accueil', '/'], ['Blog', RACINE_BLOG]])
  ]
}

// Balises propres aux articles (réseaux sociaux, date de publication).
export function metaArticle(a) {
  return [
    `<meta property="article:published_time" content="${a.publie}T08:00:00+01:00">`,
    `<meta property="article:modified_time" content="${a.modifie}T08:00:00+01:00">`,
    `<meta property="article:section" content="${e(a.rubrique || 'Conseils')}">`,
    a.image ? `<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="${e(a.imageAlt || a.titre)}">` : ''
  ].filter(Boolean).join('\n') + '\n'
}

// Version texte (Markdown) pour les assistants d'IA : les blocs HTML de
// l'article (schéma, encadrés, listes à cocher, « lire aussi ») deviennent du texte.
export function markdownArticle(a) {
  const corps = a.markdown
    .replace(/<figure class="bl-cycle"[\s\S]*?<\/figure>/g, (bloc) => {
      const titre = sansBalises((bloc.match(/<figcaption[^>]*>([\s\S]*?)<\/figcaption>/) || [])[1] || '')
      const etapes = [...bloc.matchAll(/<li>([\s\S]*?)<\/li>/g)].map((m, i) => {
        const nom = sansBalises((m[1].match(/<strong>([\s\S]*?)<\/strong>/) || [])[1] || '')
        const texte = sansBalises(m[1].replace(/<span class="bl-cycle__num">[\s\S]*?<\/span>|<strong>[\s\S]*?<\/strong>/g, ''))
        return `${i + 1}. **${nom}** : ${texte}`
      })
      const boucle = sansBalises((bloc.match(/<p class="bl-cycle__boucle">([\s\S]*?)<\/p>/) || [])[1] || '')
      return `**${titre}**\n\n${etapes.join('\n')}${boucle ? `\n\n${boucle}` : ''}`
    })
    .replace(/<aside class="bl-encart">([\s\S]*?)<\/aside>/g, (tout, interieur) => {
      const titre = sansBalises((interieur.match(/<p class="bl-encart__titre">([\s\S]*?)<\/p>/) || [])[1] || '')
      const texte = sansBalises(interieur.replace(/<p class="bl-encart__titre">[\s\S]*?<\/p>/, ''))
      return `> **${titre}** : ${texte}`
    })
    .replace(/<ul class="bl-check">([\s\S]*?)<\/ul>/g, (tout, interieur) => [...interieur.matchAll(/<li>([\s\S]*?)<\/li>/g)]
      .map((m) => `- ${m[1].replace(/<strong>([\s\S]*?)<\/strong>/g, '**$1**').replace(/<[^>]+>/g, '')}`).join('\n'))
    .replace(/<p class="bl-lire">([\s\S]*?)<\/p>/g, (tout, interieur) => `*${interieur.replace(/<a href="([^"]+)">([\s\S]*?)<\/a>/g, '[$2]($1)').replace(/<[^>]+>/g, '')}*`)
    .replace(/\]\(\//g, `](${SITE}/`)
  return `# ${a.titre}

> ${a.description}

Par ${SIGNATURE}. Publié le ${dateLongue(a.publie)}${a.modifie !== a.publie ? `, mis à jour le ${dateLongue(a.modifie)}` : ''}. Source : ${absolu(urlArticle(a))}

## L’essentiel

${a.enBref.map((x) => `- ${x}`).join('\n')}

${corps}
${a.faq.length ? `\n## Questions fréquentes\n\n${a.faq.map(([q, r]) => `### ${q}\n\n${r}`).join('\n\n')}\n` : ''}`
}

export function llmsBlog(articles) {
  if (!articles.length) return ''
  return `\n## Blog (conseils et méthodes)\n\n- [Le blog OptiTAB](${absolu(RACINE_BLOG)})\n${articles.map((a) => `- [${a.titre}](${absolu(urlArticle(a))}) : ${a.description} Version texte : ${absolu(urlArticle(a))}index.md`).join('\n')}\n`
}
