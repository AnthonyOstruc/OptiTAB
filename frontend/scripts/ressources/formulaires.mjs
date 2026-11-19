// Formulaires et tables de maths (ressources gratuites).
//
// Deux rubriques, même moteur :
//   - formulaires (contenu/formulaires/) : les formules à connaître par thème
//     (trigonométrie, dérivées, développements limités, aires…) ;
//   - tables (contenu/tables/) : les tableaux de référence à consulter ou
//     imprimer (multiplication, conversions, chiffres romains, loi normale…) ;
//   - maternelle (contenu/maternelle/) : une page par thème et par section,
//     activités illustrées du cahier OptiTAB avec leur réponse, conseils aux
//     parents et jeux (champs propres : section, activites) ;
//   - physique-chimie (contenu/physique-chimie/) : formules et fiches de
//     physique-chimie, avec leur propre section sur l'accueil des ressources.
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
import { fileURLToPath } from 'node:url'
import { slugifier } from './catalogue.mjs'
import { RACINE, SITE, absolu, appelsAction, e, encartProf, filAriane, ligneAide, urlCours, urlFiche } from './pages.mjs'
import { contenuEnHtml, contenuEnMarkdown, latexEnTexte, texteBrut } from './rendu.mjs'
import { ORGANISATION, ariane } from './seo.mjs'
import { OUTILS, outilHtml, outilScript } from './outils.mjs'
import { MAX_TITRE } from './titres.mjs'

// ---------- Rubriques ----------

export const RUBRIQUES = {
  // Poser les opérations : une page par opération, chaque méthode expliquée
  // étape par étape (figures calculées par contenu/operations/poser.py).
  operation: {
    dossier: 'operations',
    racine: `${RACINE}operations/`,
    court: 'Opérations posées',
    titre: 'Poser les opérations',
    kicker: 'Opération posée',
    lead: 'Addition, soustraction, multiplication et division posées : chaque méthode expliquée étape par étape, avec des schémas clairs, les erreurs à éviter et la vérification. À consulter ou imprimer.',
    accroche: 'Chaque opération posée expliquée étape par étape, avec les différentes méthodes.',
    titreSeo: 'Poser une addition, soustraction, multiplication, division',
    description: 'Comment poser une addition, une soustraction, une multiplication et une division : les méthodes expliquées étape par étape avec des schémas, gratuites.',
    typeRessource: ['Méthode', 'Fiche de révision'],
    autres: 'Les autres opérations posées',
    imprimer: 'Imprimer la méthode',
    lies: 'Revoir le cours et s’entraîner',
    article: 'La méthode',
    lieu: 'operation',
    libelleTexte: 'Méthode d’opération posée gratuite'
  },
  // Méthodes de calcul : une méthode pas à pas par page, avec en tête un
  // calculateur (champ « outil », voir outils.mjs).
  methode: {
    dossier: 'methodes',
    racine: `${RACINE}methodes/`,
    court: 'Méthodes de calcul',
    titre: 'Méthodes de calcul',
    kicker: 'Méthode de calcul',
    lead: 'Pourcentages, moyennes, durées, fractions, arrondis : chaque méthode expliquée pas à pas avec des exemples, et un calculateur gratuit pour vérifier vos résultats.',
    accroche: 'Chaque méthode expliquée pas à pas, avec un calculateur pour vérifier.',
    titreSeo: 'Méthodes de calcul et calculateurs gratuits : %, moyenne, durée',
    description: 'Méthodes de calcul expliquées pas à pas avec un calculateur gratuit : pourcentages, moyennes, durées, fractions, arrondis. Exemples et erreurs à éviter.',
    typeRessource: ['Méthode', 'Calculateur'],
    autres: 'Les autres méthodes de calcul',
    imprimer: 'Imprimer la méthode',
    lies: 'Revoir le cours et s’entraîner',
    article: 'La méthode',
    lieu: 'methode',
    libelleTexte: 'Méthode de calcul gratuite'
  },
  // Fiches à imprimer : une page par opération et par classe, avec des PDF
  // (fiches et corrigés) générés par contenu/fiches/generer_fiches.py.
  fiche: {
    dossier: 'fiches',
    racine: `${RACINE}fiches-a-imprimer/`,
    court: 'Fiches à imprimer',
    titre: 'Fiches de maths à imprimer',
    kicker: 'Fiche à imprimer',
    lead: 'Des fiches de calcul gratuites à imprimer en PDF, du CE1 à la 6e, avec un corrigé où chaque calcul est posé en entier : additions, soustractions, multiplications et divisions.',
    accroche: 'Des fiches de calcul en PDF, avec leur corrigé posé, du CE1 à la 6e.',
    titreSeo: 'Fiches de maths à imprimer (PDF) avec corrigé, du CE1 à la 6e',
    description: 'Fiches de maths gratuites à imprimer en PDF avec corrigé, du CE1 à la 6e : additions, soustractions, multiplications et divisions posées.',
    typeRessource: ['Fiche d’exercices', 'Exercices corrigés'],
    autres: 'Les autres fiches à imprimer',
    imprimer: 'Imprimer la page',
    lies: 'Revoir le cours',
    article: 'La fiche',
    lieu: 'fiche',
    libelleTexte: 'Fiche de maths gratuite à imprimer',
    sections: [
      ['ce1', 'CE1', '7 à 8 ans'],
      ['ce2', 'CE2', '8 à 9 ans'],
      ['cm1', 'CM1', '9 à 10 ans'],
      ['cm2', 'CM2', '10 à 11 ans'],
      ['6e', 'Sixième', '11 à 12 ans']
    ],
    bientot: ''
  },
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
    lieu: 'formulaire',
  },
  table: {
    dossier: 'tables',
    racine: `${RACINE}tables/`,
    court: 'Tables',
    titre: 'Tables de maths',
    kicker: 'Table de maths',
    lead: 'Les tables et tableaux les plus utilisés : multiplication, conversions, chiffres romains, loi normale, nombres premiers… à consulter ou imprimer.',
    accroche: 'Les tableaux de référence les plus utilisés, à consulter ou imprimer.',
    titreSeo: 'Tables de maths : multiplication, conversions, loi normale',
    description: 'Tables de maths gratuites à consulter ou imprimer : table de multiplication, tableau de conversion, chiffres romains, loi normale, nombres premiers et plus.',
    typeRessource: ['Table de référence'],
    autres: 'Les autres tables de maths',
    imprimer: 'Imprimer la table',
    lies: 'Revoir le cours',
    article: 'La table',
    lieu: 'table',
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
// Physique-chimie : les formules à connaître, expliquées une à une (première
// page : les formules du brevet). « accueil: 'section' » : tant que la rubrique
// n'a qu'une page, sa page de liste la montre en grande carte (vedette).
RUBRIQUES.physique = {
  dossier: 'physique-chimie',
  racine: `${RACINE}physique-chimie/`,
  court: 'Physique-chimie',
  titre: 'Physique-chimie',
  titreH1: 'Physique-chimie : formules et fiches gratuites',
  kicker: 'Physique-chimie',
  lead: 'Les formules de physique-chimie à connaître, expliquées une à une : le sens de chaque lettre et son unité, un exemple corrigé et le piège à éviter. À consulter ou à imprimer.',
  accroche: 'Les formules à connaître, expliquées une à une avec leurs unités, un exemple corrigé et le piège à éviter.',
  titreSeo: 'Physique-chimie : formules et fiches de révision gratuites',
  description: 'Tableau périodique interactif et formules de physique-chimie expliquées, du collège à la prépa : brevet, mécanique, électricité, mole, concentration.',
  typeRessource: ['Formulaire', 'Fiche de révision'],
  autres: 'Les autres fiches de physique-chimie',
  imprimer: 'Imprimer le formulaire',
  lies: 'Revoir le cours',
  article: 'Le formulaire',
  lieu: 'physique',
  libelleTexte: 'Formulaire de physique-chimie gratuit',
  appel: 'physique',
  accueil: 'section'
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
  const titreGoogle = info.titreSeo || info.titre
  if (titreGoogle.length > MAX_TITRE) throw new Error(`${categorie} ${nom} : titre pour Google trop long (${titreGoogle.length} > ${MAX_TITRE}) : « ${titreGoogle} »`)
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
  // Seule exception : une figure « carte » (aperçu des cartes de la liste, au
  // même cadre pour toute la rubrique) n'est pas dans le texte.
  for (const fig of figures) if (!fig.carte && !appels.includes(fig.position)) throw new Error(`${categorie} ${nom} : figure ${fig.nom} jamais appelée`)
  if (info.vignette && !figures.some((fig) => fig.nom === info.vignette)) throw new Error(`${categorie} ${nom} : vignette ${info.vignette} introuvable dans les figures`)
  if (info.outil && !OUTILS[info.outil]) throw new Error(`${categorie} ${nom} : outil inconnu (${info.outil})`)
  for (const t of info.telechargements || []) {
    for (const url of [t.pdf, t.corrige].filter(Boolean)) {
      if (!fs.existsSync(path.join(PUBLIC, url))) throw new Error(`${categorie} ${nom} : PDF introuvable (${url}) — lancer contenu/fiches/generer_fiches.py`)
    }
  }
  if (!info.outil && /\[OUTIL\]/.test(contenu)) throw new Error(`${categorie} ${nom} : [OUTIL] sans champ « outil »`)

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
  // Téléchargements (fiches PDF) : à la place de [TELECHARGEMENTS], ou en tête.
  if (f.telechargements?.length) {
    const bloc = blocTelechargements(f)
    const marque = /<p\b[^>]*>\s*\[TELECHARGEMENTS\]\s*<\/p>/
    html = marque.test(html) ? html.replace(marque, bloc) : `${bloc}\n${html}`
  }
  // Calculateur : à la place de [OUTIL], ou en tête du texte.
  if (f.outil) {
    const bloc = outilHtml(f.outil)
    const marque = /<p\b[^>]*>\s*\[OUTIL\]\s*<\/p>/
    html = marque.test(html) ? html.replace(marque, bloc) : `${bloc}\n${html}`
  }
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

const PUBLIC = fileURLToPath(new URL('../../public/', import.meta.url))
const taille = (url) => {
  const o = fs.statSync(path.join(PUBLIC, url)).size
  return o < 1024 * 1024 ? `${Math.max(1, Math.round(o / 1024))} Ko` : `${(o / 1024 / 1024).toFixed(1).replace('.', ',')} Mo`
}

// Boutons de téléchargement des fiches PDF et de leurs corrigés.
function blocTelechargements(f) {
  return `<section class="fm-pdf" aria-label="Télécharger les fiches">
  ${f.telechargements.map((t) => `<div class="fm-pdf__ligne">
    <p class="fm-pdf__titre">${e(t.titre)}</p>
    <div class="fm-pdf__boutons">
      <a class="rg-btn rg-btn--primary fm-pdf__btn" href="${t.pdf}" download data-cta-name="fiche_pdf" data-cta-location="ressources_${rubrique(f).lieu}">${icone('imprimer')} ${e(t.libelle || 'Fiche')} (PDF, ${taille(t.pdf)})</a>
      ${t.corrige ? `<a class="rg-btn rg-btn--ghost fm-pdf__btn" href="${t.corrige}" download data-cta-name="corrige_pdf" data-cta-location="ressources_${rubrique(f).lieu}">${icone('check')} Corrigé (PDF, ${taille(t.corrige)})</a>` : ''}
    </div>
  </div>`).join('\n  ')}
</section>`
}

// « À voir aussi » : pages proches des autres rubriques (champ « liees »,
// clés « dossier/slug », par exemple « tables/pourcentages-evolution »).
// Évite que deux pages se fassent concurrence : chacune renvoie vers l'autre.
function pagesLiees(f, formulaires) {
  const liees = (f.liees || []).map((cle) => {
    const x = formulaires.find((p) => `${RUBRIQUES[p.categorie].dossier}/${p.slug}` === cle)
    if (!x) throw new Error(`${f.categorie} ${f.slug} : page liée inconnue (${cle})`)
    return x
  })
  if (!liees.length) return ''
  return `<section class="rg-next fm-lies" aria-labelledby="fm-voir-titre">
      <h2 class="rg-next__title" id="fm-voir-titre">${icone('tableau')} À voir aussi</h2>
      <div class="rg-next__grid">
        ${liees.map((x) => `<a class="rg-next__card" href="${urlFormulaire(x)}">${icone('tableau')}<span><strong>${e(typo(x.titre))}</strong><small>${e(RUBRIQUES[x.categorie].titre)}${x.resume ? ` · ${e(x.resume)}` : ''}</small></span></a>`).join('\n        ')}
      </div>
    </section>`
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
        <h${niveauTitre} class="fm-card__titre">${e(typo(f.titre))}</h${niveauTitre}>
        ${f.resume ? `<span class="fm-card__resume">${e(f.resume)}</span>` : ''}
      </span>
    </a>`
}

// Grande carte d'une rubrique qui n'a encore qu'une page (accueil des ressources).
function vedette(f) {
  const fig = f.figures.find((x) => x.nom === f.vignette) || f.figures[0]
  return `<a class="fm-vedette" href="${urlFormulaire(f)}">
      ${fig ? `<span class="fm-vedette__visuel"><img src="${urlFigure(f, fig.nom)}" alt="" width="${fig.largeur}" height="${fig.hauteur}" loading="lazy" decoding="async"></span>` : ''}
      <span class="fm-vedette__corps">
        <span class="fm-vedette__kicker">${e([...f.niveaux, f.theme].filter(Boolean).join(' · '))}</span>
        <h3 class="fm-vedette__titre">${e(typo(f.titre))}</h3>
        ${f.chapo ? `<span class="fm-vedette__texte">${e(f.chapo)}</span>` : ''}
        ${f.resume ? `<span class="fm-vedette__resume">${e(f.resume)}</span>` : ''}
        <span class="fm-vedette__lien">Voir le formulaire ${icone('fleche')}</span>
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
// Physique-chimie : les maths de 3e, ou celles du lycée pour une page sans
// partie de collège (mécanique, électrocinétique…).
function appelFinal(r, lieu, f = null) {
  if (r.appel === 'physique') {
    const lycee = f && f.niveaux.length > 0 && !f.niveaux.includes('Collège')
    const maths = lycee
      ? `<p class="rg-cta__kicker">Bac</p>
    <h2 class="rg-cta__title">Réviser aussi les maths du lycée</h2>
    <p>Dérivées, vecteurs, équations différentielles : les cours, les fiches de révision et les exercices corrigés de maths du lycée, gratuits et conformes au programme.</p>
    <a class="rg-btn rg-btn--primary" href="${RACINE}maths/terminale/" data-cta-name="maths_terminale" data-cta-location="${lieu}">Voir les maths de Terminale ${icone('fleche')}</a>`
      : `<p class="rg-cta__kicker">Brevet</p>
    <h2 class="rg-cta__title">Réviser aussi les maths du brevet</h2>
    <p>Les cours, les fiches de révision et les exercices corrigés de maths de 3e, gratuits et conformes au programme.</p>
    <a class="rg-btn rg-btn--primary" href="${RACINE}maths/3e/" data-cta-name="maths_3e" data-cta-location="${lieu}">Voir les maths de 3e ${icone('fleche')}</a>`
    return `<section class="rg-ctas" aria-label="Aller plus loin">
  <div class="rg-cta rg-cta--plateforme">
    ${maths}
  </div>
  <div class="rg-cta rg-cta--prof">
    <p class="rg-cta__kicker">Cours particuliers</p>
    <h2 class="rg-cta__title">Un prof de physique-chimie, en ligne</h2>
    <p>Des séances individuelles à distance pour comprendre le cours, refaire les exercices et préparer le brevet ou le bac, avec un professeur expérimenté.</p>
    <a class="rg-btn rg-btn--green" href="/cours-particuliers" data-cta-name="tutoring" data-cta-location="${lieu}">Réserver un cours particulier ${icone('fleche')}</a>
  </div>
</section>`
  }
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

// Physique-chimie : pas d'abonnement dans cette matière, les cours particuliers
// sont la seule offre. Une ligne d'aide en haut (à côté d'Imprimer), puis des
// encadrés dans la page, car le bas d'une longue page est peu lu : un au milieu,
// ou deux (au tiers et aux deux tiers de la longueur) à partir de 10 parties.
// Moins de 4 parties : aucun.
const AIDE_PHYSIQUE = 'Besoin d’aide en physique-chimie\u00a0?'
const ENCARTS_PHYSIQUE = [
  {
    titre: 'Une notion reste floue\u00a0?',
    texte: 'Un prof t’explique les formules et refait les exercices avec toi, en cours particulier en ligne, du collège à la prépa.',
    lieu: 'ressources_physique_milieu'
  },
  {
    titre: 'Un exercice te bloque\u00a0?',
    texte: 'Un prof de physique-chimie le reprend avec toi, pas à pas, en cours particulier en ligne.',
    lieu: 'ressources_physique_milieu_2'
  }
]

function avecEncartProf(f, html) {
  if (rubrique(f).appel !== 'physique') return html
  const parties = [...html.matchAll(/<h2\b/g)].map((m) => m.index)
  if (parties.length < 4) return html
  // Début de partie le plus proche du tiers, des deux tiers ou du milieu de la page
  // (jamais la première partie, ni deux fois la même).
  const cibles = parties.length >= 10 ? [1 / 3, 2 / 3] : [1 / 2]
  const places = []
  for (const t of cibles) {
    const libres = parties.map((_, k) => k).filter((k) => k > 0 && !places.includes(k))
    places.push(libres.reduce((a, b) => (Math.abs(parties[b] - t * html.length) < Math.abs(parties[a] - t * html.length) ? b : a)))
  }
  // De la fin vers le début : les positions des parties restent justes.
  return places.map((k, rang) => [parties[k], encartProf(ENCARTS_PHYSIQUE[rang])]).reverse()
    .reduce((h, [i, encart]) => `${h.slice(0, i)}${encart}\n${h.slice(i)}`, html)
}

export function pageFormulaire(f, rendu, formulaires) {
  const r = rubrique(f)
  const [figure, figures] = r.motFigure || ['schéma', 'schémas']
  const nbFigures = f.figures.filter((fig) => !fig.carte).length
  const infos = [
    f.activites ? pluriel(f.activites, 'activité', 'activités') : pluriel(rendu.titres.length, 'partie', 'parties'),
    nbFigures ? pluriel(nbFigures, figure, figures) : '',
    `Mis à jour le ${dateLongue(f.modifie)}`
  ].filter(Boolean)
  return `<header class="rg-chap fm-head">
  <div class="rg-wrap">
    ${filAriane(etapes(f))}
    <p class="rg-kicker">${r.kicker}${f.theme ? ` · ${e(f.theme)}` : ''}</p>
    <h1 class="rg-h1">${e(typo(f.titre))}</h1>
    ${f.chapo ? `<p class="rg-lead">${e(f.chapo)}</p>` : ''}
    <ul class="rg-infos">${infos.map((i) => `<li>${e(i)}</li>`).join('')}</ul>
    ${f.niveaux.length && r.legende !== false ? `<p class="fm-legende"><span class="fm-legende__titre">Niveau de chaque partie :</span>${pastilles(f.niveaux)}</p>` : ''}
  </div>
</header>
<div class="rg-wrap rg-reading rg-reading--toc">
  ${sommaire(f, rendu.titres)}
  <article class="rg-doc rg-doc--fiche fm-doc fm-doc--${f.categorie}">
    <div class="rg-doc__tools">${r.appel === 'physique' ? ligneAide(AIDE_PHYSIQUE, 'ressources_physique_haut') : ''}<button type="button" class="rg-btn rg-btn--ghost rg-btn--sm" data-imprimer>${icone('imprimer')} ${r.imprimer}</button></div>
    <div class="sci-doc rg-sci fm-sci">${avecEncartProf(f, rendu.html)}</div>${f.outil ? `\n    ${outilScript(f.outil)}` : ''}
    ${pagesLiees(f, formulaires)}
    ${chapitresLies(f)}
    ${blocFaq(f)}
  </article>
</div>
<div class="rg-wrap">
  ${autresFormulaires(f, formulaires)}
  ${appelFinal(r, `ressources_${r.lieu}`, f)}
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
    : liste.length === 1 && r.accueil === 'section'
      ? vedette(liste[0])
      : `<div class="fm-grille">${liste.map((f) => carte(f, 2)).join('')}</div>`
  return `<header class="rg-chap fm-head">
  <div class="rg-wrap">
    ${filAriane(etapesRubrique(r))}
    <p class="rg-kicker">Ressources gratuites · Sans inscription</p>
    <h1 class="rg-h1">${e(typo(r.titreH1 || r.titre))}</h1>
    <p class="rg-lead">${r.lead}</p>
  </div>
</header>
<div class="rg-wrap fm-hub fm-hub--${categorie}">
  ${grille}
  ${r.bientot ? `<p class="fm-bientot">${e(r.bientot)}</p>` : ''}
  ${appelFinal(r, `ressources_${r.dossier}`)}
</div>`
}

// ---------- Accueil des ressources gratuites ----------
// Données des blocs de l'accueil, mis en page par pageAccueil (pages.mjs) :
// la ligne « Maternelle » du choix de la classe, l'accès rapide et les rubriques.

// Accès rapide : les pages qui répondent aux recherches les plus fréquentes
// (pourcentage, moyenne, tables, conversions, formules du collège et du lycée).
const ACCES_RAPIDE = [
  ['table', 'table-de-multiplication'],
  ['methode', 'calculer-un-pourcentage'],
  ['physique', 'tableau-periodique'],
  ['table', 'tableau-de-conversion'],
  ['formulaire', 'pythagore-thales-trigonometrie'],
  ['methode', 'calculer-une-moyenne'],
  ['methode', 'lire-l-heure'],
  ['formulaire', 'aires-perimetres-volumes'],
  ['methode', 'calculer-avec-des-fractions'],
  ['operation', 'division-posee'],
  ['formulaire', 'second-degre'],
  ['physique', 'formules-physique-chimie-brevet']
]

// Rubriques de l'accueil, dans l'ordre : icône (pages.mjs) et ce qu'elles contiennent.
const RUBRIQUES_ACCUEIL = [
  ['formulaire', 'formule', (n) => pluriel(n, 'formulaire', 'formulaires')],
  ['table', 'table', (n) => pluriel(n, 'table', 'tables')],
  ['methode', 'calcul', (n) => `${pluriel(n, 'méthode', 'méthodes')} et calculateurs`],
  ['operation', 'operation', (n) => pluriel(n, 'opération expliquée', 'opérations expliquées')],
  ['fiche', 'imprimer', (n, liste) => pluriel(liste.reduce((k, f) => k + (f.telechargements || []).length, 0), 'fiche PDF', 'fiches PDF')],
  ['physique', 'physique', (n) => pluriel(n, 'fiche', 'fiches')]
]

export function donneesAccueil(pages) {
  const page = (categorie, slug) => {
    const f = pages.find((x) => x.categorie === categorie && x.slug === slug)
    if (!f) throw new Error(`accueil des ressources : page inconnue (${categorie}/${slug})`)
    return f
  }
  const acces = ACCES_RAPIDE.map(([categorie, slug]) => {
    const f = page(categorie, slug)
    return { titre: typo(f.titreCourt || f.titre), url: urlFormulaire(f) }
  })
  const rubriques = RUBRIQUES_ACCUEIL.map(([categorie, ico, compte]) => {
    const r = RUBRIQUES[categorie]
    const liste = pages.filter((f) => f.categorie === categorie)
    if (!liste.length) return null
    return { cle: categorie, titre: typo(r.titre), texte: typo(r.accroche), compte: compte(liste.length, liste), url: r.racine, icone: ico }
  }).filter(Boolean)
  const m = RUBRIQUES.maternelle
  const maternelle = {
    titre: typo(m.titre),
    url: m.racine,
    sections: m.sections.map(([cle, titre]) => {
      const n = pages.filter((f) => f.categorie === 'maternelle' && f.section === cle).length
      return n ? { titre, meta: pluriel(n, 'thème', 'thèmes'), url: `${m.racine}#section-${cle}` } : null
    }).filter(Boolean)
  }
  return { acces, rubriques, maternelle }
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
    // Fiches PDF : documents associés à la ressource.
    f.telechargements?.length ? {
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      name: `${f.titre} : fichiers PDF`,
      itemListElement: f.telechargements.flatMap((t) => [[t.titre, t.pdf], [`${t.titre} : corrigé`, t.corrige]]).filter(([, u]) => u)
        .map(([nom, u], i) => ({ '@type': 'ListItem', position: i + 1, item: { '@type': 'DigitalDocument', name: nom, url: absolu(u), encodingFormat: 'application/pdf', isAccessibleForFree: true } }))
    } : null,
    // Calculateur de la page : application web gratuite.
    f.outil ? {
      '@context': 'https://schema.org',
      '@type': 'WebApplication',
      name: OUTILS[f.outil].titre,
      url: `${url}#otc-${f.outil}-titre`,
      applicationCategory: 'EducationalApplication',
      operatingSystem: 'Tous (navigateur web)',
      inLanguage: 'fr-FR',
      isAccessibleForFree: true,
      offers: { '@type': 'Offer', price: '0', priceCurrency: 'EUR' },
      publisher: ORGA
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
  const pdfs = (f.telechargements || []).map((t) => `- ${t.titre} : [fiche (PDF)](${absolu(t.pdf)})${t.corrige ? ` · [corrigé (PDF)](${absolu(t.corrige)})` : ''}`).join('\n')
  const outil = f.outil ? `> ${OUTILS[f.outil].titre} gratuit en ligne : ${absolu(urlFormulaire(f))}` : ''
  const corps = contenuEnMarkdown(f.contenu.replace(/^\[OUTIL\]\s*$/m, 'OUTIL_EN_LIGNE').replace(/^\[TELECHARGEMENTS\]\s*$/m, 'PDF_EN_LIGNE'), images)
    .replace(/^.*PDF_EN_LIGNE.*$/m, pdfs)
    .replace(/^.*OUTIL_EN_LIGNE.*$/m, outil)
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
