// Formulaires et tables de maths (ressources gratuites).
//
// Deux rubriques, même moteur :
//   - formulaires (contenu/formulaires/) : les formules à connaître par thème
//     (trigonométrie, dérivées, développements limités, aires…) ;
//   - tables (contenu/tables/) : les tableaux de référence à consulter ou
//     imprimer (multiplication, conversions, chiffres romains, loi normale…) ;
//   - maternelle (contenu/maternelle/) : une page par thème et par section,
//     activités illustrées du cahier OptiTAB avec leur réponse, conseils aux
//     parents et jeux (champs propres : section, activites).
//
// Chaque page est un dossier <rubrique>/<slug>/ :
//   formulaire.md        bloc d'informations en JSON entre « --- », puis le
//                        texte au format OptiTAB v1 (mêmes encadrés et tableaux
//                        que les fiches du site) ; « {Collège} », « {Lycée} » ou
//                        « {Supérieur} » à la fin d'un titre de partie = niveau ;
//   figures/figures.py   figures (style des livres), compilées par
//                        cours/format_v1/outils/figures_livre.py ;
//   figures/images/*.png figures produites, appelées par [IMAGE_n] dans
//                        l'ordre de la liste « figures » du bloc d'informations.
//
// Chaque page est complète (texte, formules en SVG + MathML, figures,
// sommaire, questions fréquentes, données structurées) et lisible par Google
// et les assistants d'IA sans JavaScript ; elle a aussi une version Markdown.
import fs from 'node:fs'
import path from 'node:path'
import { slugifier } from './catalogue.mjs'
import { RACINE, SITE, absolu, appelsAction, e, filAriane, urlCours, urlFiche } from './pages.mjs'
import { contenuEnHtml, contenuEnMarkdown, latexEnTexte, texteBrut } from './rendu.mjs'
import { ORGANISATION, ariane } from './seo.mjs'

// ---------- Rubriques ----------

export const RUBRIQUES = {
  formulaire: {
    dossier: 'formulaires',
    racine: `${RACINE}formulaires/`,
    court: 'Formulaires',
    titre: 'Formulaires de maths',
    kicker: 'Formulaire de maths',
    lead: 'Toutes les formules à connaître, du collège au supérieur, à consulter ou imprimer.',
    accroche: 'Toutes les formules à connaître, à consulter ou imprimer.',
    titreSeo: 'Formulaires de maths gratuits : toutes les formules à connaître',
    description: 'Formulaires de maths gratuits : les formules à connaître réunies dans des tableaux clairs, avec schémas, du collège au supérieur. À consulter ou imprimer.',
    typeRessource: ['Formulaire', 'Fiche de révision'],
    autres: 'Les autres formulaires de maths',
    imprimer: 'Imprimer le formulaire',
    lies: 'Revoir le cours de ces formules',
    article: 'Le formulaire',
    lieu: 'formulaire'
  },
  table: {
    dossier: 'tables',
    racine: `${RACINE}tables/`,
    court: 'Tables',
    titre: 'Tables de maths',
    kicker: 'Table de maths',
    lead: 'Les tables et tableaux les plus utilisés : multiplication, conversions, chiffres romains, loi normale, nombres premiers… à consulter ou imprimer.',
    accroche: 'Les tableaux de référence les plus utilisés, à consulter ou imprimer.',
    titreSeo: 'Tables de maths gratuites : multiplication, conversions, loi normale',
    description: 'Tables de maths gratuites à consulter ou imprimer : table de multiplication, tableau de conversion, chiffres romains, loi normale, nombres premiers et plus.',
    typeRessource: ['Table de référence'],
    autres: 'Les autres tables de maths',
    imprimer: 'Imprimer la table',
    lies: 'Revoir le cours',
    article: 'La table',
    lieu: 'table'
  },
  // Maths en maternelle : une page par thème et par section (activités du
  // cahier OptiTAB, figures avec leur réponse, conseils aux parents, jeux).
  maternelle: {
    dossier: 'maternelle',
    racine: `${RACINE}maternelle/`,
    court: 'Maternelle',
    titre: 'Maths en maternelle',
    kicker: 'Maths en maternelle',
    lead: 'Des fiches de maths de maternelle gratuites, à faire à la maison ou à imprimer : activités illustrées de la petite à la grande section avec la bonne réponse, conseils pour les parents et jeux simples, conformes au programme de l’école maternelle.',
    accroche: 'Activités illustrées à faire avec votre enfant, avec la bonne réponse et des conseils.',
    titreSeo: 'Maths en maternelle : fiches et activités gratuites à imprimer',
    description: 'Fiches de maths de maternelle gratuites à imprimer : activités illustrées avec la bonne réponse, conseils aux parents et jeux, conformes au programme.',
    typeRessource: ['Activité', 'Fiche à imprimer'],
    autres: 'Les autres activités de maternelle',
    imprimer: 'Imprimer les activités',
    lies: 'Et ensuite, au CP',
    article: 'En maternelle',
    lieu: 'maternelle',
    // Particularités de la rubrique : pas de légende des niveaux (toute la page
    // est d'une seule section), « illustrations » plutôt que « schémas », pages
    // de la liste groupées par section, appel vers les maths du CP (pas d'offre
    // d'abonnement ni de cours particuliers en maternelle).
    legende: false,
    libelleTexte: 'Fiche de maths de maternelle gratuite',
    motFigure: ['illustration', 'illustrations'],
    sections: [
      ['petite-section', 'Petite section', 'avant 4 ans'],
      ['moyenne-section', 'Moyenne section', 'à partir de 4 ans'],
      ['grande-section', 'Grande section', 'à partir de 5 ans']
    ],
    bientot: '',
    appel: 'cp'
  }
}
const rubrique = (f) => RUBRIQUES[f.categorie || 'formulaire']

export const RACINE_FORMULAIRES = RUBRIQUES.formulaire.racine
export const urlFormulaire = (f) => `${rubrique(f).racine}${f.slug}/`
const urlFigure = (f, nom) => `${urlFormulaire(f)}${nom}.png`

// Niveaux (pastille à la fin d'un titre de partie, ordre d'affichage).
export const NIVEAUX = ['Maternelle', 'Primaire', 'Collège', 'Lycée', 'Supérieur']
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
// Typographie française : espace insécable avant ? ! : ; (jamais de signe seul en
// début de ligne), guillemets « » jamais seuls en bout de ligne, et espace fine insécable dans les milliers (« 1 000 » jamais coupé).
const typo = (texte) => String(texte).replace(/ ([?!:;])/g, ' $1').replace(/« /g, '«\u00A0').replace(/ »/g, '\u00A0»').replace(/(\d) (?=\d{3}\b)/g, '$1 ')

// Taille d'une image PNG (en-tête IHDR).
function taillePng(fichier) {
  const tete = Buffer.alloc(24)
  const fd = fs.openSync(fichier, 'r')
  fs.readSync(fd, tete, 0, 24, 0)
  fs.closeSync(fd)
  return { largeur: tete.readUInt32BE(16), hauteur: tete.readUInt32BE(20) }
}

// ---------- Lecture ----------

function lireFormulaire(dossier, catalogue, categorie) {
  const fichier = path.join(dossier, 'formulaire.md')
  const nom = path.basename(dossier)
  const source = fs.readFileSync(fichier, 'utf8').replace(/\r\n/g, '\n')
  const m = source.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/)
  if (!m) throw new Error(`${categorie} ${nom} : bloc d'informations (--- … ---) introuvable`)
  const info = JSON.parse(m[1])
  for (const champ of ['slug', 'titre', 'description', 'publie']) {
    if (!info[champ]) throw new Error(`${categorie} ${nom} : champ « ${champ} » manquant`)
  }
  if (info.slug !== nom) throw new Error(`${categorie} ${nom} : le slug (${info.slug}) doit être le nom du dossier`)
  if (info.description.length > 160) throw new Error(`${categorie} ${nom} : description trop longue (${info.description.length} > 160)`)
  const contenu = m[2].trim()
  if (!contenu.startsWith('<!-- optitab:1 -->')) throw new Error(`${categorie} ${nom} : le texte doit commencer par <!-- optitab:1 -->`)

  // Figures : [IMAGE_n] = n-ième figure de la liste ; chacune doit exister et être appelée.
  const figures = (info.figures || []).map((fig, i) => {
    const png = path.join(dossier, 'figures', 'images', `${fig.nom}.png`)
    if (!fs.existsSync(png)) throw new Error(`${categorie} ${nom} : figure introuvable (${fig.nom}.png) — compiler figures/figures.py`)
    if (!fig.alt || fig.alt.length < 15) throw new Error(`${categorie} ${nom} : texte alternatif manquant pour ${fig.nom}`)
    const { largeur, hauteur } = taillePng(png)
    return { ...fig, position: i + 1, png, largeur: Math.round(largeur / 2), hauteur: Math.round(hauteur / 2) }
  })
  const appels = [...contenu.matchAll(/\[IMAGE_(\d+)\]/g)].map((x) => Number(x[1]))
  for (const n of appels) if (!figures[n - 1]) throw new Error(`${categorie} ${nom} : [IMAGE_${n}] sans figure`)
  for (const fig of figures) if (!appels.includes(fig.position)) throw new Error(`${categorie} ${nom} : figure ${fig.nom} jamais appelée`)

  // Chapitres liés « classe/chapitre » : ils doivent exister dans les ressources.
  const chapitres = (info.chapitresLies || []).map((cle) => {
    const [classe, slug] = cle.split('/')
    const ch = catalogue.chapitres.find((c) => c.classe.slug === classe && c.slug === slug)
    if (!ch) throw new Error(`${categorie} ${nom} : chapitre lié inconnu (${cle})`)
    return ch
  })

  return {
    ...info,
    categorie,
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

// Lit une rubrique (contenu/formulaires ou contenu/tables).
export function lireFormulaires(dossier, catalogue, categorie = 'formulaire') {
  if (!fs.existsSync(dossier)) return []
  const liste = fs.readdirSync(dossier, { withFileTypes: true })
    .filter((d) => d.isDirectory() && fs.existsSync(path.join(dossier, d.name, 'formulaire.md')))
    // Aperçu d'une seule page de maternelle (RESSOURCES_MATERNELLE_SEULE=<slug>) : les autres
    // pages en cours de rédaction ne bloquent pas la génération. Sans la variable (production), rien ne change.
    .filter((d) => categorie !== 'maternelle' || !process.env.RESSOURCES_MATERNELLE_SEULE || d.name === process.env.RESSOURCES_MATERNELLE_SEULE)
    .map((d) => lireFormulaire(path.join(dossier, d.name), catalogue, categorie))
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
    .split(`src="${SITE}${RACINE}`).join(`src="${RACINE}`)
    // Tableaux dont la première colonne est un libellé en mots (« Carré de
    // côté c », « Produit »…) : libellé à gauche ; à deux colonnes (fm-t2),
    // le libellé passe au-dessus de sa formule sur téléphone. Les grands
    // tableaux de nombres (6 colonnes ou plus) passent en grille compacte
    // (fm-grille-n). Les autres restent tels quels.
    .replace(/<table class="otm-table">([\s\S]*?)<\/table>/g, (tout, interieur) => {
      const colonnes = (((interieur.match(/<thead><tr>([\s\S]*?)<\/tr><\/thead>/) || [])[1] || '').match(/<th\b/g) || []).length
      const premieres = [...interieur.matchAll(/<tr><td\b[^>]*>((?:(?!<\/td>)[\s\S])*)<\/td>/g)].map((m) => m[1].replace(/\$[^$]*\$/g, ''))
      const libelles = premieres.length && premieres.every((t) => /[a-zé]{3,}/i.test(t))
      if (colonnes >= 6) return `<table class="otm-table fm-grille-n${libelles ? ' fm-libelles' : ''}">${interieur}</table>`
      if (!libelles) {
        // Deux colonnes « symbole | explication en phrases » (alphabet grec…) :
        // la colonne de texte se lit mieux alignée à gauche.
        const dernieres = [...interieur.matchAll(/<td\b[^>]*>((?:(?!<\/td>)[\s\S])*)<\/td><\/tr>/g)]
          .map((m) => m[1].replace(/\$[^$]*\$/g, '').replace(/<[^>]+>/g, '').trim())
        const long = dernieres.length && dernieres.reduce((n, t) => n + t.length, 0) / dernieres.length > 40
        return colonnes === 2 && long ? `<table class="otm-table fm-texte">${interieur}</table>` : tout
      }
      return `<table class="otm-table ${colonnes === 2 ? 'fm-t2' : 'fm-libelles'}">${interieur}</table>`
    })

  const titres = []
  const vus = new Set()
  html = html.replace(/<h2\b([^>]*)>([\s\S]*?)<\/h2>/g, (tout, attributs, interieur) => {
    const num = texteBrut((interieur.match(/class="otm-h2-num"[^>]*>([\s\S]*?)<\/span>/) || [])[1] || '')
    let texteHtml = (interieur.match(/class="otm-h2-text"[^>]*>([\s\S]*?)<\/span>/) || [])[1] || interieur
    const niveau = (texteHtml.match(/\s*\{([^{}]+)\}\s*$/) || [])[1] || ''
    if (niveau && !NIVEAUX.includes(niveau)) throw new Error(`${f.categorie} ${f.slug} : niveau inconnu « ${niveau} » (${NIVEAUX.join(', ')})`)
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
  return `<aside class="rg-toc fm-toc" aria-label="Sommaire">
    <details class="rg-toc__box" open><summary>Sommaire</summary><ol>${titres.map((t) => `<li><a href="#${t.id}"><span class="rg-toc__num">${e(t.num)}</span><span>${t.html}</span></a></li>`).join('')}${f.faq.length ? '<li><a href="#questions-frequentes"><span class="rg-toc__num">?</span><span>Questions fréquentes</span></a></li>' : ''}</ol></details>
  </aside>`
}

function chapitresLies(f) {
  if (!f.chapitres.length) return ''
  return `<section class="rg-next fm-lies" aria-labelledby="fm-lies-titre">
      <h2 class="rg-next__title" id="fm-lies-titre">${icone('check')} ${rubrique(f).lies}</h2>
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
  // Les trois pages les plus proches de la même rubrique (ordre) : une rangée.
  const rang = (x) => Math.abs((x.ordre ?? 99) - (f.ordre ?? 99))
  const autres = formulaires.filter((x) => x.slug !== f.slug && x.categorie === f.categorie)
    .sort((a, b) => rang(a) - rang(b) || (a.ordre ?? 99) - (b.ordre ?? 99)).slice(0, 3)
  if (!autres.length) return ''
  return `<section class="fm-autres" aria-labelledby="fm-autres-titre">
    <h2 id="fm-autres-titre">${rubrique(f).autres}</h2>
    <div class="fm-grille">${autres.map((x) => carte(x)).join('')}</div>
  </section>`
}

const etapesRubrique = (r) => [['Accueil', '/'], ['Ressources gratuites', RACINE], [r.court, r.racine]]
const etapes = (f) => [...etapesRubrique(rubrique(f)), [f.titreCourt, urlFormulaire(f)]]

// ---------- Pages ----------

// Appel de fin de page : l'offre du site, ou (maternelle) les maths du CP.
function appelFinal(r, lieu) {
  if (r.appel !== 'cp') return appelsAction(null, null, lieu)
  return `<section class="rg-ctas rg-ctas--seul" aria-label="Aller plus loin">
  <div class="rg-cta rg-cta--plateforme">
    <p class="rg-cta__kicker">Après la maternelle</p>
    <h2 class="rg-cta__title">Les maths du CP, gratuites et en ligne</h2>
    <p>Des cours illustrés, des fiches et des exercices corrigés pour accompagner votre enfant dès le CP, conformes au programme.</p>
    <a class="rg-btn rg-btn--primary" href="${RACINE}maths/cp/" data-cta-name="maths_cp" data-cta-location="${lieu}">Voir les maths du CP ${icone('fleche')}</a>
  </div>
</section>`
}

export function pageFormulaire(f, rendu, formulaires) {
  const r = rubrique(f)
  const [figure, figures] = r.motFigure || ['schéma', 'schémas']
  const infos = [
    f.activites ? pluriel(f.activites, 'activité', 'activités') : pluriel(rendu.titres.length, 'partie', 'parties'),
    f.figures.length ? pluriel(f.figures.length, figure, figures) : '',
    `Mis à jour le ${dateLongue(f.modifie)}`
  ].filter(Boolean)
  return `<header class="rg-chap fm-head">
  <div class="rg-wrap">
    ${filAriane(etapes(f))}
    <p class="rg-kicker">${r.kicker}${f.theme ? ` · ${e(f.theme)}` : ''}</p>
    <h1 class="rg-h1">${e(f.titre)}</h1>
    ${f.chapo ? `<p class="rg-lead">${e(f.chapo)}</p>` : ''}
    <ul class="rg-infos">${infos.map((i) => `<li>${e(i)}</li>`).join('')}</ul>
    ${f.niveaux.length && r.legende !== false ? `<p class="fm-legende"><span class="fm-legende__titre">Niveau de chaque partie :</span>${pastilles(f.niveaux)}</p>` : ''}
  </div>
</header>
<div class="rg-wrap rg-reading rg-reading--toc">
  ${sommaire(f, rendu.titres)}
  <article class="rg-doc rg-doc--fiche fm-doc fm-doc--${f.categorie}">
    <div class="rg-doc__tools"><button type="button" class="rg-btn rg-btn--ghost rg-btn--sm" data-imprimer>${icone('imprimer')} ${r.imprimer}</button></div>
    <div class="sci-doc rg-sci fm-sci">${rendu.html}</div>
    ${chapitresLies(f)}
    ${blocFaq(f)}
  </article>
</div>
<div class="rg-wrap">
  ${autresFormulaires(f, formulaires)}
  ${appelFinal(r, `ressources_${r.lieu}`)}
</div>`
}

// Page d'une rubrique (liste de ses pages).
export function pageFormulaires(liste, categorie = 'formulaire') {
  const r = RUBRIQUES[categorie]
  // Rubrique découpée en sections (maternelle : grande, moyenne, petite
  // section) : un titre par section qui a des pages, puis une ligne « bientôt ».
  const perdues = r.sections ? liste.filter((f) => !r.sections.some(([cle]) => cle === f.section)) : []
  if (perdues.length) throw new Error(`${categorie} ${perdues[0].slug} : champ « section » absent ou inconnu (${r.sections.map(([cle]) => cle).join(', ')})`)
  const grille = r.sections
    ? r.sections.map(([cle, titre, age]) => {
        const pages = liste.filter((f) => f.section === cle)
        if (!pages.length) return ''
        return `<section class="fm-section" aria-labelledby="section-${cle}">
    <h2 class="fm-section__titre" id="section-${cle}">${e(titre)} <span>${e(age)}</span></h2>
    <div class="fm-grille">${pages.map((f) => carte(f, 3)).join('')}</div>
  </section>`
      }).join('\n  ')
    : `<div class="fm-grille">${liste.map((f) => carte(f, 2)).join('')}</div>`
  return `<header class="rg-chap fm-head">
  <div class="rg-wrap">
    ${filAriane(etapesRubrique(r))}
    <p class="rg-kicker">Ressources gratuites · Sans inscription</p>
    <h1 class="rg-h1">${r.titre}</h1>
    <p class="rg-lead">${r.lead}</p>
  </div>
</header>
<div class="rg-wrap fm-hub fm-hub--${categorie}">
  ${grille}
  ${r.bientot ? `<p class="fm-bientot">${e(r.bientot)}</p>` : ''}
  ${appelFinal(r, `ressources_${r.dossier}`)}
</div>`
}

// Blocs « Formulaires » et « Tables » de l'accueil des ressources gratuites.
export function blocAccueilFormulaires(pages) {
  return Object.entries(RUBRIQUES).map(([categorie, r]) => {
    const liste = pages.filter((f) => f.categorie === categorie)
    if (!liste.length) return ''
    return `<section class="rg-cycle fm-accueil" aria-labelledby="cycle-${r.dossier}">
    <div class="rg-cycle__head"><h2 id="cycle-${r.dossier}"><a href="${r.racine}">${r.titre}</a></h2><p>${r.accroche}</p></div>
    <div class="fm-grille">${liste.map((f) => carte(f)).join('')}</div>
  </section>`
  }).join('\n')
}

// ---------- Référencement ----------

const ORGA = { '@type': 'EducationalOrganization', '@id': ORGANISATION['@id'], name: ORGANISATION.name, url: ORGANISATION.url, logo: ORGANISATION.logo }

export function jsonldFormulaire(f, titres) {
  const url = absolu(urlFormulaire(f))
  return [
    {
      '@context': 'https://schema.org',
      '@type': 'LearningResource',
      '@id': `${url}#ressource`,
      name: f.titre,
      headline: f.titreSeo || f.titre,
      description: f.description,
      url,
      inLanguage: 'fr-FR',
      isAccessibleForFree: true,
      learningResourceType: rubrique(f).typeRessource,
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

export function jsonldFormulaires(liste, categorie = 'formulaire') {
  const r = RUBRIQUES[categorie]
  return [
    {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: r.titre,
      url: absolu(r.racine),
      inLanguage: 'fr-FR',
      isAccessibleForFree: true,
      publisher: ORGA,
      mainEntity: {
        '@type': 'ItemList',
        itemListElement: liste.map((f, i) => ({ '@type': 'ListItem', position: i + 1, name: f.titre, url: absolu(urlFormulaire(f)) }))
      }
    },
    ariane(etapesRubrique(r))
  ]
}

// Version texte (Markdown) pour les assistants d'IA.
export function markdownFormulaire(f) {
  const images = f.figures.map((fig) => ({ position: fig.position, image: absolu(urlFigure(f, fig.nom)), alt_text: fig.alt }))
  const corps = contenuEnMarkdown(f.contenu, images)
    .replace(/^(##\s.*?)\s*\{([^{}]+)\}\s*$/gm, '$1 ($2)')
  return `# ${f.titre}

> ${f.description}

${rubrique(f).libelleTexte || `${rubrique(f).kicker} gratuit`} OptiTAB${f.niveaux.length ? ` (niveaux : ${f.niveaux.join(', ')})` : ''}. Mis à jour le ${dateLongue(f.modifie)}. Source : ${absolu(urlFormulaire(f))}

${corps}
${f.chapitres.length ? `\n## Cours associés\n\n${f.chapitres.map((ch) => `- [${ch.titre} (maths ${ch.classe.court})](${absolu(urlCours(ch))}) · [fiche](${absolu(urlFiche(ch))})`).join('\n')}\n` : ''}${f.faq.length ? `\n## Questions fréquentes\n\n${f.faq.map(([q, r]) => `### ${q}\n\n${r}`).join('\n\n')}\n` : ''}`
}

export function llmsFormulaires(pages) {
  return Object.entries(RUBRIQUES).map(([categorie, r]) => {
    const liste = pages.filter((f) => f.categorie === categorie)
    if (!liste.length) return ''
    return `\n## ${r.titre}\n\n- [${r.titre} : la liste](${absolu(r.racine)})\n${liste.map((f) => `- [${f.titre}](${absolu(urlFormulaire(f))}) : ${f.description} Version texte : ${absolu(urlFormulaire(f))}index.md`).join('\n')}\n`
  }).join('')
}
