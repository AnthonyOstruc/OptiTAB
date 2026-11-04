// Génère les pages statiques des ressources gratuites (lancé après « vite
// build », voir « postbuild » dans package.json). Chaque page contient tout
// son texte, ses formules (SVG + MathML) et ses figures : Google et les
// assistants d'IA la lisent sans exécuter de JavaScript.
//
//   node scripts/ressources/generer.mjs [--sortie dossier] [--classes 3e,terminale] [--limite 3]
//
// Source : l'API publique des ressources gratuites (RESSOURCES_API_BASE, par
// défaut l'API de production). En cas d'échec de lecture, la construction
// échoue : l'hébergeur garde alors la version en ligne précédente.
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { chargerCatalogue, slugifier } from './catalogue.mjs'
import {
  composerFormules, contenuEnHtml, feuilleMathJax, latexEnTexte, objectifs, preparerRendu, texteBrut
} from './rendu.mjs'
import {
  RACINE, absolu, gabarit, pageAccueil, pageClasse, pageCours, pageExercices, pageFiche, pageRedirection,
  titreExercice, urlClasse, urlCours, urlExercices, urlFiche, urlMarkdown
} from './pages.mjs'
import {
  ANCIENNES_ADRESSES, RACINE_BLOG, jsonldArticle, jsonldBlog, lireArticles, llmsBlog,
  markdownArticle, metaArticle, pageArticle, pageBlog, urlArticle
} from './blog.mjs'
import {
  FAQ, correspondances, descriptionCourte, jsonldAccueil, jsonldChapitre, jsonldClasse,
  llmsTxt, markdownChapitre, markdownClasse, planDuSite
} from './seo.mjs'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const FRONT = path.resolve(ICI, '..', '..')

const args = process.argv.slice(2)
const option = (nom, defaut) => {
  const i = args.indexOf(`--${nom}`)
  return i >= 0 ? args[i + 1] : defaut
}
const SORTIE = path.resolve(option('sortie', path.join(FRONT, 'dist')))
const API = (process.env.RESSOURCES_API_BASE || 'https://optitab-backend.onrender.com').replace(/\/+$/, '')
const FILTRE_CLASSES = option('classes', '') ? option('classes').split(',') : null
const LIMITE = Number(option('limite', 0)) || 0

const debut = Date.now()
const journal = (...m) => console.log('[ressources]', ...m)

function ecrire(chemin, contenu) {
  const cible = path.join(SORTIE, chemin.replace(/^\/+/, ''))
  fs.mkdirSync(path.dirname(cible), { recursive: true })
  fs.writeFileSync(cible, contenu)
}
const ecrirePage = (url, html) => ecrire(`${url}index.html`, html)

// Mesure d'audience (consentement + Google Tag Manager), reprise telle quelle
// du index.html construit par Vite pour rester identique au reste du site.
function suiviDuSite() {
  const fichier = path.join(SORTIE, 'index.html')
  if (!fs.existsSync(fichier)) return { suivi: '', suiviCorps: '' }
  const html = fs.readFileSync(fichier, 'utf8')
  const scripts = html.match(/<script>[\s\S]*?<\/script>/g) || []
  const consentement = scripts.find((s) => s.includes('optitab_cookie_consent_v1')) || ''
  const gtm = scripts.find((s) => s.includes('googletagmanager.com/gtm.js')) || ''
  const noscript = (html.match(/<noscript><iframe src="https:\/\/www\.googletagmanager\.com[\s\S]*?<\/noscript>/) || [''])[0]
  if (gtm.includes('%VITE_GTM_ID%')) return { suivi: consentement, suiviCorps: '' }
  return { suivi: [consentement, gtm].filter(Boolean).join('\n'), suiviCorps: noscript }
}

function feuilleDeStyle() {
  const parties = [
    fs.readFileSync(path.join(ICI, 'ressources.css'), 'utf8'),
    fs.readFileSync(path.join(ICI, 'blog.css'), 'utf8'),
    '/* Contenus de cours (styles du site) */',
    fs.readFileSync(path.join(FRONT, 'src/styles/scientific-content.css'), 'utf8'),
    fs.readFileSync(path.join(FRONT, 'src/styles/optitab-doc.css'), 'utf8'),
    '/* Formules (MathJax) */',
    feuilleMathJax()
  ]
  const css = parties.join('\n')
  const empreinte = crypto.createHash('sha1').update(css).digest('hex').slice(0, 10)
  const chemin = `${RACINE}assets/ressources.${empreinte}.css`
  ecrire(chemin, css)
  return chemin
}

// Titres de parties (h2) : identifiant pour le sommaire et les liens directs.
function titresEtAncres(html) {
  const titres = []
  const vus = new Set()
  const sortie = html.replace(/<h2\b([^>]*)>([\s\S]*?)<\/h2>/g, (tout, attributs, interieur) => {
    const num = (interieur.match(/class="otm-h2-num"[^>]*>([\s\S]*?)<\/span>/) || [])[1]
    const texteHtml = (interieur.match(/class="otm-h2-text"[^>]*>([\s\S]*?)<\/span>/) || [])[1] || interieur
    const texte = latexEnTexte(texteBrut(texteHtml))
    if (!texte || /\sid="/.test(attributs)) return tout
    let id = slugifier(texte, 48)
    while (vus.has(id)) id += '-2'
    vus.add(id)
    titres.push({ id, num: num ? texteBrut(num) : '', texte, html: texteHtml.trim() })
    return `<h2${attributs} id="${id}">${interieur}</h2>`
  })
  return { html: sortie, titres }
}

const premiereImage = (...listes) => {
  for (const l of listes) {
    const im = (l || []).find((x) => x && x.image)
    if (im) return im.image
  }
  return null
}
const imagesDe = (...listes) => listes.flatMap((l) => (l || []).map((x) => x && x.image).filter(Boolean))

let totalFormules = 0
const latexRestant = []
function finaliser(url, page) {
  const { html, formules } = composerFormules(page.contenu)
  totalFormules += formules
  // Contrôle : aucune formule ne doit rester en LaTeX brut dans le texte affiché.
  const texte = html.replace(/<(pre|code|script|style)[\s\S]*?<\/\1>/gi, '').replace(/<[^>]+>/g, ' ')
  const restes = texte.match(/\\\(|\\\[|\$\$|\$[^$\s][^$<]{0,80}\$/g)
  if (restes) latexRestant.push(`${url} : ${restes.slice(0, 2).join(' | ')}`)
  ecrirePage(url, gabarit({ ...page, contenu: html, chemin: url }))
}

async function main() {
  journal(`lecture du catalogue sur ${API}…`)
  const catalogue = await chargerCatalogue(API)
  if (FILTRE_CLASSES || LIMITE) {
    catalogue.classes = catalogue.classes
      .filter((c) => !FILTRE_CLASSES || FILTRE_CLASSES.includes(c.slug))
      .map((c) => {
        if (!LIMITE) return c
        const garder = new Set(c.chapitres.slice(0, LIMITE))
        return { ...c, chapitres: c.chapitres.filter((ch) => garder.has(ch)), themes: c.themes.map((t) => ({ ...t, chapitres: t.chapitres.filter((ch) => garder.has(ch)) })).filter((t) => t.chapitres.length) }
      })
    catalogue.chapitres = catalogue.classes.flatMap((c) => c.chapitres)
  }
  if (!catalogue.chapitres.length) throw new Error('Aucun chapitre gratuit lu : construction arrêtée.')
  journal(`${catalogue.classes.length} classes, ${catalogue.chapitres.length} chapitres, ${catalogue.totaux.exercicesGratuits} exercices gratuits`)

  await preparerRendu()
  const ctx = { css: feuilleDeStyle(), ...suiviDuSite() }
  const plan = []

  for (const ch of catalogue.chapitres) {
    const { classe } = ch
    // Cours
    const brutCours = contenuEnHtml(ch.cours.contenu, ch.cours.images, 'cours')
    const { html: htmlCours, titres } = titresEtAncres(brutCours)
    const obj = objectifs(ch.cours.contenu) || latexEnTexte(texteBrut(ch.cours.excerpt || brutCours, 400))
    const descCours = descriptionCourte(`Cours de maths ${classe.court} : ${ch.titre}. ${obj}`)
    const imageCours = premiereImage(ch.cours.images)
    const nbFigures = (htmlCours.match(/<img\b/g) || []).length
    const infos = [
      titres.length > 1 ? `${titres.length} parties` : 'Cours complet',
      nbFigures ? `${nbFigures} schéma${nbFigures > 1 ? 's' : ''}` : '',
      ch.cours.lecture_duree ? `Lecture ${String(ch.cours.lecture_duree).replace('~', '≈ ')}` : '',
      'Conforme au programme'
    ].filter(Boolean)
    finaliser(urlCours(ch), {
      titre: `${ch.titre} – Cours de maths ${classe.court}`,
      description: descCours,
      contenu: pageCours(ch, { html: htmlCours, titres, infos }),
      catalogue, ctx, type: 'article', image: imageCours, markdown: urlMarkdown(ch),
      jsonld: jsonldChapitre(ch, 'cours', { description: descCours, image: imageCours })
    })
    plan.push({ chemin: urlCours(ch), modifie: ch.modifie, images: imagesDe(ch.cours.images) })

    // Fiche de révision
    if (ch.fiche) {
      const htmlFiche = contenuEnHtml(ch.fiche.contenu, ch.fiche.images, 'fiche')
      const descFiche = descriptionCourte(`Fiche de révision de maths ${classe.court} : ${ch.titre}. L’essentiel à retenir : définitions, propriétés et méthodes, sur une page à relire ou imprimer.`)
      const imageFiche = premiereImage(ch.fiche.images, ch.cours.images)
      finaliser(urlFiche(ch), {
        titre: `${ch.titre} – Fiche de révision ${classe.court}`,
        description: descFiche,
        contenu: pageFiche(ch, { html: htmlFiche }),
        catalogue, ctx, type: 'article', image: imageFiche, markdown: urlMarkdown(ch),
        jsonld: jsonldChapitre(ch, 'fiche', { description: descFiche, image: imageFiche })
      })
      plan.push({ chemin: urlFiche(ch), modifie: ch.modifie, images: imagesDe(ch.fiche.images) })
    }

    // Exercices corrigés
    if (ch.exercices.length) {
      const rendus = ch.exercices.map((ex) => ({
        ex,
        enonce: contenuEnHtml(ex.contenu || ex.question, ex.images, 'exercice'),
        etapes: contenuEnHtml(ex.etapes, ex.images, 'exercice'),
        solution: contenuEnHtml(ex.solution, ex.images, 'exercice')
      }))
      const descExos = descriptionCourte(`${ch.exercices.length} exercices corrigés de maths ${classe.court} sur ${ch.titre.charAt(0).toLowerCase() + ch.titre.slice(1)}, avec correction détaillée pas à pas : ${ch.exercices.map(titreExercice).join(' ; ')}.`)
      const imageExos = premiereImage(...ch.exercices.map((x) => x.images), ch.cours.images)
      finaliser(urlExercices(ch), {
        titre: `${ch.titre} – Exercices corrigés ${classe.court}`,
        description: descExos,
        contenu: pageExercices(ch, rendus),
        catalogue, ctx, type: 'article', image: imageExos, markdown: urlMarkdown(ch),
        jsonld: jsonldChapitre(ch, 'exercices', { description: descExos, image: imageExos })
      })
      plan.push({ chemin: urlExercices(ch), modifie: ch.modifie, images: imagesDe(...ch.exercices.map((x) => x.images)) })
    }

    ecrire(urlMarkdown(ch), markdownChapitre(ch))
  }

  // Pages des classes
  for (const classe of catalogue.classes) {
    const description = descriptionCourte(`Maths ${classe.court} : cours complets, fiches de révision et exercices corrigés gratuits, chapitre par chapitre. ${classe.accroche}`)
    finaliser(urlClasse(classe), {
      titre: `Maths ${classe.court} : cours, fiches et exercices corrigés gratuits`,
      description,
      contenu: pageClasse(classe, catalogue),
      catalogue, ctx,
      jsonld: jsonldClasse(classe),
      motsCles: `cours maths ${classe.court}, exercices corrigés ${classe.court}, fiche révision maths ${classe.court}`
    })
    ecrire(`${urlClasse(classe)}index.md`, markdownClasse(classe))
    const dernier = classe.chapitres.map((ch) => ch.modifie).filter(Boolean).sort().pop()
    plan.unshift({ chemin: urlClasse(classe), modifie: dernier })
  }

  // Accueil des ressources
  finaliser(RACINE, {
    titre: 'Cours de maths gratuits du CP à la Terminale : cours, fiches, exercices corrigés',
    description: `${catalogue.totaux.cours} cours de maths complets, ${catalogue.totaux.fiches} fiches de révision et ${catalogue.totaux.exercicesGratuits} exercices corrigés pas à pas, du CP à la Terminale, conformes au programme. Gratuit, sans inscription.`,
    contenu: pageAccueil(catalogue, FAQ),
    catalogue, ctx,
    jsonld: jsonldAccueil(catalogue)
  })
  plan.unshift({ chemin: RACINE, modifie: new Date().toISOString() })

  // Anciennes pages d'accueil des ressources → nouvel accueil.
  for (const ancien of ['cours/', 'exercices/', 'syntheses/', 'maths/']) ecrirePage(`${RACINE}${ancien}`, pageRedirection(RACINE))
  // Anciennes adresses de cours, fiches et exercices (lues par l'application).
  ecrire(`${RACINE}redirections.json`, JSON.stringify(correspondances(catalogue)))

  // Blog (articles écrits dans contenu/blog/)
  const articles = lireArticles(path.join(FRONT, 'contenu', 'blog'))
  for (const a of articles) {
    const url = urlArticle(a)
    ecrirePage(url, gabarit({
      titre: a.titreSeo || a.titre,
      description: a.description,
      chemin: url,
      contenu: pageArticle(a, articles),
      catalogue, ctx, type: 'article', actif: null,
      image: a.image ? absolu(a.image) : undefined,
      markdown: `${url}index.md`,
      motsCles: (a.motsCles || []).join(', '),
      meta: metaArticle(a),
      jsonld: jsonldArticle(a)
    }))
    ecrire(`${url}index.md`, markdownArticle(a))
    plan.push({ chemin: url, modifie: a.modifie, images: a.image ? [absolu(a.image)] : [] })
  }
  ecrirePage(RACINE_BLOG, gabarit({
    titre: 'Blog : conseils et méthodes pour progresser en maths',
    description: 'Conseils concrets pour progresser en maths du collège au lycée : méthodes de travail, brevet, bac, aide aux parents. Écrit par un professeur de maths.',
    chemin: RACINE_BLOG,
    contenu: pageBlog(articles),
    catalogue, ctx, actif: null,
    image: articles[0]?.image ? absolu(articles[0].image) : undefined,
    jsonld: jsonldBlog(articles)
  }))
  plan.push({ chemin: RACINE_BLOG, modifie: articles[0]?.modifie })
  for (const ancien of ANCIENNES_ADRESSES) ecrirePage(`${RACINE_BLOG}${ancien}`, pageRedirection(RACINE_BLOG, 'Blog'))
  journal(`blog : ${articles.length} article(s)`)

  ecrire('sitemap-ressources.xml', planDuSite(plan))
  ecrire('llms.txt', llmsTxt(catalogue) + llmsBlog(articles))
  retirerAnciennesAdresses()

  journal(`${plan.length} pages, ${totalFormules} formules composées, en ${Math.round((Date.now() - debut) / 1000)} s → ${SORTIE}`)
  if (latexRestant.length) {
    journal(`ATTENTION : LaTeX non composé sur ${latexRestant.length} page(s) :`)
    latexRestant.slice(0, 15).forEach((l) => journal('   ', l))
  }
}

// Les anciennes adresses des ressources gratuites quittent les plans du site
// généraux : les nouvelles pages (et le blog) sont dans sitemap-ressources.xml.
function retirerAnciennesAdresses() {
  for (const nom of ['sitemap.xml', 'sitemap-images.xml']) {
    const fichier = path.join(SORTIE, nom)
    if (!fs.existsSync(fichier)) continue
    const xml = fs.readFileSync(fichier, 'utf8')
    const nettoye = xml.replace(/\s*<url>(?:(?!<\/url>)[\s\S])*?\/(?:ressources-gratuites|blog)(?:(?!<\/url>)[\s\S])*?<\/url>/g, '')
    if (nettoye !== xml) fs.writeFileSync(fichier, nettoye)
  }
}

main().catch((erreur) => {
  console.error('[ressources] ÉCHEC :', erreur?.stack || erreur)
  process.exit(1)
})
