// Formulaires de maths (ressources gratuites) : tableaux des formules à
// connaître (trigonométrie, dérivées, développements limités, aires…).
//
// Chaque formulaire est un dossier de contenu/formulaires/<slug>/ :
//   formulaire.md        bloc d'informations en JSON entre « --- », puis le
//                        texte au format OptiTAB v1 (mêmes encadrés et tableaux
//                        que les fiches du site) ; « {Collège} », « {Lycée} » ou
//                        « {Supérieur} » à la fin d'un titre de partie = niveau ;
//   figures/figures.py   figures (style des livres), compilées par
//                        cours/format_v1/outils/figures_livre.py ;
//   figures/images/*.png figures produites, appelées par [IMAGE_n] dans
//                        l'ordre de la liste « figures » du bloc d'informations.
//
// Chaque formulaire devient une page complète (texte, formules en SVG + MathML,
// figures, sommaire, questions fréquentes, données structurées) lisible par
// Google et les assistants d'IA sans JavaScript, et une version Markdown.
import fs from 'node:fs'
import path from 'node:path'
import { slugifier } from './catalogue.mjs'
import { RACINE, SITE, absolu, appelsAction, e, filAriane, urlCours, urlFiche } from './pages.mjs'
import { contenuEnHtml, contenuEnMarkdown, latexEnTexte, texteBrut } from './rendu.mjs'
import { ORGANISATION, ariane } from './seo.mjs'

export const RACINE_FORMULAIRES = `${RACINE}formulaires/`
export const urlFormulaire = (f) => `${RACINE_FORMULAIRES}${f.slug}/`
const urlFigure = (f, nom) => `${urlFormulaire(f)}${nom}.png`

// Niveaux (pastille à la fin d'un titre de partie, ordre d'affichage).
export const NIVEAUX = ['Collège', 'Lycée', 'Supérieur']
const cleNiveau = (n) => slugifier(n, 20)

const ICONES = {
  fleche: '<path d="M5 12h14M13 6l6 6-6 6"/>',
  imprimer: '<path d="M6 9V3h12v6M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><path d="M6 14h12v7H6z"/>',
  cours: '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
  check: '<path d="m5 12 5 5L20 7"/>',
  tableau: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 10v10"/>'
}
const icone = (nom, cls = 'rg-ico') => `<svg class="${cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">${ICONES[nom]}</svg>`

const dateLongue = (iso) => new Date(`${iso}T12:00:00`).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
const pluriel = (n, un, plusieurs) => `${n} ${n > 1 ? plusieurs : un}`
// Typographie française : espace insécable avant ? ! : ; (jamais de signe seul en début de ligne).
const typo = (texte) => String(texte).replace(/ ([?!:;])/g, ' $1')

// Taille d'une image PNG (en-tête IHDR).
function taillePng(fichier) {
  const tete = Buffer.alloc(24)
  const fd = fs.openSync(fichier, 'r')
  fs.readSync(fd, tete, 0, 24, 0)
  fs.closeSync(fd)
  return { largeur: tete.readUInt32BE(16), hauteur: tete.readUInt32BE(20) }
}

// ---------- Lecture ----------

function lireFormulaire(dossier, catalogue) {
  const fichier = path.join(dossier, 'formulaire.md')
  const nom = path.basename(dossier)
  const source = fs.readFileSync(fichier, 'utf8').replace(/\r\n/g, '\n')
  const m = source.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/)
  if (!m) throw new Error(`formulaire ${nom} : bloc d'informations (--- … ---) introuvable`)
  const info = JSON.parse(m[1])
  for (const champ of ['slug', 'titre', 'description', 'publie']) {
    if (!info[champ]) throw new Error(`formulaire ${nom} : champ « ${champ} » manquant`)
  }
  if (info.slug !== nom) throw new Error(`formulaire ${nom} : le slug (${info.slug}) doit être le nom du dossier`)
  if (info.description.length > 160) throw new Error(`formulaire ${nom} : description trop longue (${info.description.length} > 160)`)
  const contenu = m[2].trim()
  if (!contenu.startsWith('<!-- optitab:1 -->')) throw new Error(`formulaire ${nom} : le texte doit commencer par <!-- optitab:1 -->`)

  // Figures : [IMAGE_n] = n-ième figure de la liste ; chacune doit exister et être appelée.
  const figures = (info.figures || []).map((fig, i) => {
    const png = path.join(dossier, 'figures', 'images', `${fig.nom}.png`)
    if (!fs.existsSync(png)) throw new Error(`formulaire ${nom} : figure introuvable (${fig.nom}.png) — compiler figures/figures.py`)
    if (!fig.alt || fig.alt.length < 15) throw new Error(`formulaire ${nom} : texte alternatif manquant pour ${fig.nom}`)
    const { largeur, hauteur } = taillePng(png)
    return { ...fig, position: i + 1, png, largeur: Math.round(largeur / 2), hauteur: Math.round(hauteur / 2) }
  })
  const appels = [...contenu.matchAll(/\[IMAGE_(\d+)\]/g)].map((x) => Number(x[1]))
  for (const n of appels) if (!figures[n - 1]) throw new Error(`formulaire ${nom} : [IMAGE_${n}] sans figure`)
  for (const fig of figures) if (!appels.includes(fig.position)) throw new Error(`formulaire ${nom} : figure ${fig.nom} jamais appelée`)

  // Chapitres liés « classe/chapitre » : ils doivent exister dans les ressources.
  const chapitres = (info.chapitresLies || []).map((cle) => {
    const [classe, slug] = cle.split('/')
    const ch = catalogue.chapitres.find((c) => c.classe.slug === classe && c.slug === slug)
    if (!ch) throw new Error(`formulaire ${nom} : chapitre lié inconnu (${cle})`)
    return ch
  })

  return {
    ...info,
    titreCourt: info.titreCourt || info.titre,
    modifie: info.modifie || info.publie,
    niveaux: info.niveaux || [],
    motsCles: info.motsCles || [],
    chapo: info.chapo ? typo(info.chapo) : '',
    resume: info.resume ? typo(info.resume) : '',
    faq: (info.faq || []).map(([q, r]) => [typo(q), typo(r)]),
    contenu,
    figures,
    chapitres
  }
}

export function lireFormulaires(dossier, catalogue) {
  if (!fs.existsSync(dossier)) return []
  const liste = fs.readdirSync(dossier, { withFileTypes: true })
    .filter((d) => d.isDirectory() && fs.existsSync(path.join(dossier, d.name, 'formulaire.md')))
    .map((d) => lireFormulaire(path.join(dossier, d.name), catalogue))
    .filter((f) => !f.brouillon)
  return liste.sort((a, b) => (a.ordre ?? 99) - (b.ordre ?? 99) || a.titre.localeCompare(b.titre, 'fr'))
}

// Figures à recopier à côté de la page : [chemin source, adresse publiée].
export const figuresAPublier = (f) => f.figures.map((fig) => [fig.png, urlFigure(f, fig.nom)])

// ---------- Rendu ----------

// Contenu → HTML (formules encore en LaTeX), titres de parties avec ancre et
// pastille de niveau, sommaire.
export function rendreFormulaire(f) {
  const images = f.figures.map((fig) => ({
    position: fig.position,
    image: absolu(urlFigure(f, fig.nom)),
    alt_text: fig.alt,
    width: fig.largeur,
    height: fig.hauteur
  }))
  let html = contenuEnHtml(f.contenu, images, 'cours')
    // Figures servies par le site lui-même (adresse relative).
    .split(`src="${SITE}${RACINE_FORMULAIRES}`).join(`src="${RACINE_FORMULAIRES}`)
    // Tableaux dont la première colonne est un libellé en mots (« Carré de
    // côté c », « Produit »…) : libellé à gauche ; à deux colonnes (fm-t2),
    // le libellé passe au-dessus de sa formule sur téléphone. Les tableaux
    // dont la première colonne est une formule restent tels quels.
    .replace(/<table class="otm-table">([\s\S]*?)<\/table>/g, (tout, interieur) => {
      const premieres = [...interieur.matchAll(/<tr><td\b[^>]*>((?:(?!<\/td>)[\s\S])*)<\/td>/g)].map((m) => m[1].replace(/\$[^$]*\$/g, ''))
      if (!premieres.length || !premieres.every((t) => /[a-zé]{3,}/i.test(t))) return tout
      const colonnes = (((interieur.match(/<thead><tr>([\s\S]*?)<\/tr><\/thead>/) || [])[1] || '').match(/<th\b/g) || []).length
      return `<table class="otm-table ${colonnes === 2 ? 'fm-t2' : 'fm-libelles'}">${interieur}</table>`
    })

  const titres = []
  const vus = new Set()
  html = html.replace(/<h2\b([^>]*)>([\s\S]*?)<\/h2>/g, (tout, attributs, interieur) => {
    const num = texteBrut((interieur.match(/class="otm-h2-num"[^>]*>([\s\S]*?)<\/span>/) || [])[1] || '')
    let texteHtml = (interieur.match(/class="otm-h2-text"[^>]*>([\s\S]*?)<\/span>/) || [])[1] || interieur
    const niveau = (texteHtml.match(/\s*\{([^{}]+)\}\s*$/) || [])[1] || ''
    if (niveau && !NIVEAUX.includes(niveau)) throw new Error(`formulaire ${f.slug} : niveau inconnu « ${niveau} » (${NIVEAUX.join(', ')})`)
    texteHtml = texteHtml.replace(/\s*\{[^{}]+\}\s*$/, '').trim()
    const texte = latexEnTexte(texteBrut(texteHtml))
    let id = slugifier(texte, 48)
    while (vus.has(id)) id += '-2'
    vus.add(id)
    titres.push({ id, num, texte, html: texteHtml, niveau })
    const pastille = niveau ? ` <span class="fm-niveau fm-niveau--${cleNiveau(niveau)}">${e(niveau)}</span>` : ''
    const nouveau = interieur.replace(/(class="otm-h2-text"[^>]*>)[\s\S]*?(<\/span>)/, `$1${texteHtml}${pastille}$2`)
    return `<h2${attributs} id="${id}">${nouveau}</h2>`
  })
  return { html, titres }
}

// ---------- Morceaux de page ----------

function pastilles(niveaux) {
  return niveaux.map((n) => `<span class="fm-niveau fm-niveau--${cleNiveau(n)}">${e(n)}</span>`).join('')
}

function sommaire(f, titres) {
  return `<aside class="rg-toc fm-toc" aria-label="Sommaire du formulaire">
    <details class="rg-toc__box" open><summary>Sommaire</summary><ol>${titres.map((t) => `<li><a href="#${t.id}"><span class="rg-toc__num">${e(t.num)}</span><span>${t.html}</span></a></li>`).join('')}${f.faq.length ? '<li><a href="#questions-frequentes"><span class="rg-toc__num">?</span><span>Questions fréquentes</span></a></li>' : ''}</ol></details>
  </aside>`
}

function chapitresLies(f) {
  if (!f.chapitres.length) return ''
  return `<section class="rg-next fm-lies" aria-labelledby="fm-lies-titre">
      <h2 class="rg-next__title" id="fm-lies-titre">${icone('check')} Revoir le cours de ces formules</h2>
      <div class="rg-next__grid">
        ${f.chapitres.map((ch) => `<a class="rg-next__card" href="${urlCours(ch)}">${icone('cours')}<span><strong>${e(ch.titre)}</strong><small>Maths ${e(ch.classe.court)} · cours, fiche${ch.exercices.length ? ' et exercices corrigés' : ''}</small></span></a>`).join('\n        ')}
      </div>
    </section>`
}

function blocFaq(f) {
  if (!f.faq.length) return ''
  return `<section class="rg-faq fm-faq" aria-labelledby="questions-frequentes">
    <h2 id="questions-frequentes">Questions fréquentes</h2>
    ${f.faq.map(([q, r]) => `<details class="rg-faq__item"><summary>${e(q)}</summary><p>${e(r)}</p></details>`).join('\n    ')}
  </section>`
}

// Carte épurée : un aperçu (la figure « vignette »), le titre tel qu'on le
// cherche sur Google, une ligne de mots-clés.
function carte(f, niveauTitre = 3) {
  const fig = f.figures.find((x) => x.nom === f.vignette) || f.figures[0]
  return `<a class="fm-card" href="${urlFormulaire(f)}">
      ${fig ? `<span class="fm-card__visuel"><img src="${urlFigure(f, fig.nom)}" alt="${e(`${f.titre} : ${fig.alt}`)}" width="${fig.largeur}" height="${fig.hauteur}" loading="lazy" decoding="async"></span>` : ''}
      <span class="fm-card__corps">
        <h${niveauTitre} class="fm-card__titre">${e(f.titre)}</h${niveauTitre}>
        ${f.resume ? `<span class="fm-card__resume">${e(f.resume)}</span>` : ''}
      </span>
    </a>`
}

function autresFormulaires(f, formulaires) {
  // Les trois formulaires les plus proches (ordre du programme) : une rangée.
  const rang = (x) => Math.abs((x.ordre ?? 99) - (f.ordre ?? 99))
  const autres = formulaires.filter((x) => x.slug !== f.slug).sort((a, b) => rang(a) - rang(b) || (a.ordre ?? 99) - (b.ordre ?? 99)).slice(0, 3)
  if (!autres.length) return ''
  return `<section class="fm-autres" aria-labelledby="fm-autres-titre">
    <h2 id="fm-autres-titre">Les autres formulaires de maths</h2>
    <div class="fm-grille">${autres.map((x) => carte(x)).join('')}</div>
  </section>`
}

const etapes = (f) => [['Accueil', '/'], ['Ressources gratuites', RACINE], ['Formulaires', RACINE_FORMULAIRES], ...(f ? [[f.titreCourt, urlFormulaire(f)]] : [])]

// ---------- Pages ----------

export function pageFormulaire(f, rendu, formulaires) {
  const infos = [
    pluriel(rendu.titres.length, 'partie', 'parties'),
    f.figures.length ? pluriel(f.figures.length, 'schéma', 'schémas') : '',
    `Mis à jour le ${dateLongue(f.modifie)}`
  ].filter(Boolean)
  return `<header class="rg-chap fm-head">
  <div class="rg-wrap">
    ${filAriane(etapes(f))}
    <p class="rg-kicker">Formulaire de maths${f.theme ? ` · ${e(f.theme)}` : ''}</p>
    <h1 class="rg-h1">${e(f.titre)}</h1>
    ${f.chapo ? `<p class="rg-lead">${e(f.chapo)}</p>` : ''}
    <ul class="rg-infos">${infos.map((i) => `<li>${e(i)}</li>`).join('')}</ul>
    ${f.niveaux.length ? `<p class="fm-legende"><span class="fm-legende__titre">Niveau de chaque partie :</span>${pastilles(f.niveaux)}</p>` : ''}
  </div>
</header>
<div class="rg-wrap rg-reading rg-reading--toc">
  ${sommaire(f, rendu.titres)}
  <article class="rg-doc rg-doc--fiche fm-doc">
    <div class="rg-doc__tools"><button type="button" class="rg-btn rg-btn--ghost rg-btn--sm" data-imprimer>${icone('imprimer')} Imprimer le formulaire</button></div>
    <div class="sci-doc rg-sci fm-sci">${rendu.html}</div>
    ${chapitresLies(f)}
    ${blocFaq(f)}
  </article>
</div>
<div class="rg-wrap">
  ${autresFormulaires(f, formulaires)}
  ${appelsAction(null, null, 'ressources_formulaire')}
</div>`
}

export function pageFormulaires(formulaires) {
  return `<header class="rg-chap fm-head">
  <div class="rg-wrap">
    ${filAriane(etapes(null))}
    <p class="rg-kicker">Ressources gratuites · Sans inscription</p>
    <h1 class="rg-h1">Formulaires de maths</h1>
    <p class="rg-lead">Toutes les formules à connaître, du collège au supérieur, à consulter ou imprimer.</p>
  </div>
</header>
<div class="rg-wrap fm-hub">
  <div class="fm-grille">${formulaires.map((f) => carte(f, 2)).join('')}</div>
  ${appelsAction(null, null, 'ressources_formulaires')}
</div>`
}

// Bloc « Formulaires » de l'accueil des ressources gratuites.
export function blocAccueilFormulaires(formulaires) {
  if (!formulaires.length) return ''
  return `<section class="rg-cycle fm-accueil" aria-labelledby="cycle-formulaires">
    <div class="rg-cycle__head"><h2 id="cycle-formulaires">Formulaires de maths</h2><p>Toutes les formules à connaître, à consulter ou imprimer.</p></div>
    <div class="fm-grille">${formulaires.map((f) => carte(f)).join('')}</div>
  </section>`
}

// ---------- Référencement ----------

const ORGA = { '@type': 'EducationalOrganization', '@id': ORGANISATION['@id'], name: ORGANISATION.name, url: ORGANISATION.url, logo: ORGANISATION.logo }

export function jsonldFormulaire(f, titres) {
  const url = absolu(urlFormulaire(f))
  return [
    {
      '@context': 'https://schema.org',
      '@type': 'LearningResource',
      '@id': `${url}#formulaire`,
      name: f.titre,
      headline: f.titreSeo || f.titre,
      description: f.description,
      url,
      inLanguage: 'fr-FR',
      isAccessibleForFree: true,
      learningResourceType: ['Formulaire', 'Fiche de révision'],
      educationalLevel: f.niveaux,
      about: { '@type': 'Thing', name: f.titreCourt },
      teaches: titres.map((t) => t.texte),
      keywords: f.motsCles.join(', '),
      image: f.figures.map((fig) => absolu(urlFigure(f, fig.nom))),
      datePublished: f.publie,
      dateModified: f.modifie,
      author: ORGA,
      publisher: ORGA
    },
    f.faq.length ? {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: f.faq.map(([q, r]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: r } }))
    } : null,
    ariane(etapes(f))
  ].filter(Boolean)
}

export function jsonldFormulaires(formulaires) {
  return [
    {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: 'Formulaires de maths',
      url: absolu(RACINE_FORMULAIRES),
      inLanguage: 'fr-FR',
      isAccessibleForFree: true,
      publisher: ORGA,
      mainEntity: {
        '@type': 'ItemList',
        itemListElement: formulaires.map((f, i) => ({ '@type': 'ListItem', position: i + 1, name: f.titre, url: absolu(urlFormulaire(f)) }))
      }
    },
    ariane(etapes(null))
  ]
}

// Version texte (Markdown) pour les assistants d'IA.
export function markdownFormulaire(f) {
  const images = f.figures.map((fig) => ({ position: fig.position, image: absolu(urlFigure(f, fig.nom)), alt_text: fig.alt }))
  const corps = contenuEnMarkdown(f.contenu, images)
    .replace(/^(##\s.*?)\s*\{([^{}]+)\}\s*$/gm, '$1 ($2)')
  return `# ${f.titre}

> ${f.description}

Formulaire gratuit OptiTAB (niveaux : ${f.niveaux.join(', ')}). Mis à jour le ${dateLongue(f.modifie)}. Source : ${absolu(urlFormulaire(f))}

${corps}
${f.chapitres.length ? `\n## Cours associés\n\n${f.chapitres.map((ch) => `- [${ch.titre} (maths ${ch.classe.court})](${absolu(urlCours(ch))}) · [fiche](${absolu(urlFiche(ch))})`).join('\n')}\n` : ''}${f.faq.length ? `\n## Questions fréquentes\n\n${f.faq.map(([q, r]) => `### ${q}\n\n${r}`).join('\n\n')}\n` : ''}`
}

export function llmsFormulaires(formulaires) {
  if (!formulaires.length) return ''
  return `\n## Formulaires de maths\n\n- [Tous les formulaires](${absolu(RACINE_FORMULAIRES)})\n${formulaires.map((f) => `- [${f.titre}](${absolu(urlFormulaire(f))}) : ${f.description} Version texte : ${absolu(urlFormulaire(f))}index.md`).join('\n')}\n`
}
