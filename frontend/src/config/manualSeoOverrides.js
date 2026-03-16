import { normalizePathname } from '../composables/useDynamicSeo.js'

export const MANUAL_SEO_OVERRIDES_BY_PATH = Object.freeze({
  '/': {
    title: 'Plateforme de maths: cours, exercices corriges et fiches | OptiTAB',
    description:
      'Travaille les maths du college a la prepa avec des cours clairs, des exercices corriges pas a pas et des fiches de revision efficaces.',
    type: 'service',
    level: 'college a prepa',
    subject: 'mathematiques',
    notion: 'plateforme maths',
    primaryKeyword: 'plateforme maths en ligne',
    searchIntent: 'apprendre'
  },
  '/cours-particuliers': {
    title: 'Cours particuliers de maths en ligne du college a la prepa | OptiTAB',
    description:
      'Cours particuliers de maths en ligne de la 6e a la prepa : explications claires, suivi regulier, exercices cibles et accompagnement pas a pas.',
    h1: 'Cours particuliers de maths en ligne',
    type: 'service',
    level: 'college a prepa',
    subject: 'mathematiques',
    notion: 'cours particuliers',
    primaryKeyword: 'cours particuliers maths en ligne',
    searchIntent: 'trouver un cours particulier'
  },
  '/tarifs': {
    title: 'Tarifs maths en ligne: abonnement sans engagement | OptiTAB',
    description:
      "Compare les offres OptiTAB pour acceder aux cours de maths, exercices corriges et fiches de revision, avec annulation possible a tout moment.",
    type: 'service',
    level: 'college a prepa',
    subject: 'mathematiques',
    notion: 'tarifs',
    primaryKeyword: 'tarifs cours de maths en ligne',
    searchIntent: 'comparer une offre'
  },
  '/ressources-gratuites': {
    title: 'Ressources gratuites de maths: cours, exercices corriges et fiches | OptiTAB',
    description:
      'Accede a des ressources gratuites de maths pour comprendre, t entrainer et reviser: cours clairs, exercices corriges et fiches de synthese.',
    type: 'hub',
    level: 'college a prepa',
    subject: 'mathematiques',
    notion: 'ressources gratuites',
    primaryKeyword: 'ressources gratuites maths',
    searchIntent: 'apprendre'
  },
  '/ressources-gratuites/cours': {
    title: 'Cours de maths gratuits du college a la prepa | OptiTAB',
    description:
      'Comprends chaque notion avec des cours de maths progressifs, des explications claires et des exemples adaptes au niveau college, lycee et prepa.',
    type: 'niveau',
    level: 'college a prepa',
    subject: 'mathematiques',
    notion: 'cours de maths',
    primaryKeyword: 'cours de maths gratuits',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/exercices': {
    title: 'Exercices corriges de maths du college a la prepa | OptiTAB',
    description:
      'Entraine-toi avec des exercices corriges de maths classes par chapitre, niveau et notion pour progresser en methode et gagner en autonomie.',
    type: 'niveau',
    level: 'college a prepa',
    subject: 'mathematiques',
    notion: 'exercices corriges',
    primaryKeyword: 'exercices corriges maths',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/syntheses': {
    title: 'Fiches de revision de maths du college a la prepa | OptiTAB',
    description:
      'Revise rapidement avec des fiches de maths claires: formules essentielles, methodes et points a retenir pour controles, brevet, bac et prepa.',
    type: 'niveau',
    level: 'college a prepa',
    subject: 'mathematiques',
    notion: 'fiches de revision',
    primaryKeyword: 'fiche revision maths',
    searchIntent: 'reviser'
  },
  '/about': {
    title: 'Methode OptiTAB: progresser en maths avec rigueur',
    description:
      'Decouvre la methode OptiTAB pour apprendre les maths: explications claires, entrainement guide et suivi pedagogique du college a la prepa.',
    type: 'service',
    level: 'college a prepa',
    subject: 'mathematiques',
    notion: 'methode pedagogique',
    primaryKeyword: 'methode cours de maths',
    searchIntent: 'comprendre'
  },
  '/contact': {
    title: 'Contact OptiTAB: WhatsApp et email',
    description:
      'Contacte OptiTAB pour une question, un accompagnement ou un cours particulier de maths. Reponse rapide par WhatsApp ou email.',
    type: 'service',
    level: 'college a prepa',
    subject: 'mathematiques',
    notion: 'contact',
    primaryKeyword: 'contact cours de maths',
    searchIntent: 'contacter'
  },
  '/ressources-gratuites/cours/france/lycee/maths/maths-bases-methodes-factorisation-mise-en-forme-factorisee-methodes-et-techniques-175': {
    title: 'Factorisation: methodes et mise en forme factorisee (Bases) | OptiTAB',
    description:
      'Apprends les methodes de factorisation: facteur commun, identites remarquables et strategies de mise en forme factorisee pour gagner en fiabilite.',
    type: 'cours',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'factorisation',
    primaryKeyword: 'cours factorisation',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/cours/france/lycee/maths/premiere-1er-suites-numeriques-153': {
    title: 'Suites numeriques en Premiere: cours complet et methodes | OptiTAB',
    description:
      'Comprends les suites numeriques en Premiere: definition, sens de variation, suites arithmetiques et geometriques, avec methodes et exemples.',
    type: 'cours',
    level: '1re',
    subject: 'mathematiques',
    notion: 'suites numeriques',
    primaryKeyword: 'cours suites numeriques premiere',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/cours/france/lycee/maths/seconde-resoudre-des-problemes-de-geometrie-223': {
    title: 'Problemes de geometrie en Seconde: methodes de resolution | OptiTAB',
    description:
      'Travaille la geometrie en Seconde avec une methode claire: projetes orthogonaux, distances, raisonnements et resolutions de problemes types.',
    type: 'cours',
    level: '2nde',
    subject: 'mathematiques',
    notion: 'geometrie',
    primaryKeyword: 'cours geometrie seconde',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/cours/france/lycee/maths/terminal-bac-factorisation-mise-en-forme-factorisee-methodes-et-techniques-115': {
    title: 'Factorisation en Terminale: methodes et techniques efficaces | OptiTAB',
    description:
      'Maitrise la factorisation en Terminale avec des techniques utiles en bac: identites remarquables, transformations algebriques et methodes fiables.',
    type: 'cours',
    level: 'terminale',
    subject: 'mathematiques',
    notion: 'factorisation',
    primaryKeyword: 'cours factorisation terminale',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/cours/france/lycee/maths/terminal-bac-la-derivation-88': {
    title: 'Cours de derivation en Terminale: methode et applications | OptiTAB',
    description:
      "Maitrise la derivation en Terminale avec rappels essentiels, regles de calcul, tangente, convexite et applications guidees.",
    primaryKeyword: 'cours derivation terminale',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/cours/france/lycee/maths/terminal-bac-la-fonction-logarithme-neperien-90': {
    title: 'Fonction logarithme neperien en Terminale: cours complet | OptiTAB',
    description:
      "Comprends la fonction logarithme neperien en Terminale: definition, proprietes, derivation, limites et methodes d'application.",
    primaryKeyword: 'cours logarithme neperien terminale',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/cours/france/lycee/maths/terminal-bac-les-primitives-93': {
    title: 'Primitives en Terminale: cours, methodes et applications | OptiTAB',
    description:
      'Comprends les primitives en Terminale: definition, techniques de calcul, reconnaissance de formes et applications en calcul integral.',
    type: 'cours',
    level: 'terminale',
    subject: 'mathematiques',
    notion: 'primitives',
    primaryKeyword: 'cours primitives terminale',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/cours/france/lycee/maths/terminal-bac-les-structures-conditionnelles-et-la-logique-en-python-103': {
    title: 'Structures conditionnelles en Python (Terminale): cours pas a pas | OptiTAB',
    description:
      'Maitrise if, elif, else et les operateurs logiques en Python pour Terminale, avec des exemples progressifs et des methodes de raisonnement.',
    type: 'cours',
    level: 'terminale',
    subject: 'mathematiques',
    notion: 'python conditionnelles',
    primaryKeyword: 'python terminale conditionnelles',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/cours/france/lycee/maths/terminal-bac-matrices-112': {
    title: 'Matrices en Terminale: cours complet et methodes de calcul | OptiTAB',
    description:
      'Travaille les matrices en Terminale: definitions, operations, calculs matriciels et techniques utiles pour resoudre des problemes types.',
    type: 'cours',
    level: 'terminale',
    subject: 'mathematiques',
    notion: 'matrices',
    primaryKeyword: 'cours matrices terminale',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/cours/france/prepa/maths/mpsi-mp2i-equations-differentielles-lineaires-129': {
    title: 'Equations differentielles lineaires en MPSI-MP2I: cours | OptiTAB',
    description:
      'Comprends les equations differentielles lineaires en prepa MPSI-MP2I: structure des solutions, methodes de resolution et applications classiques.',
    type: 'cours',
    level: 'prepa',
    subject: 'mathematiques',
    notion: 'equations differentielles lineaires',
    primaryKeyword: 'cours equations differentielles mpsi',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/cours/france/prepa/maths/mpsi-mp2i-nombres-complexes-123': {
    title: 'Nombres complexes en MPSI-MP2I: cours et methodes | OptiTAB',
    description:
      'Maitrise les nombres complexes en prepa MPSI-MP2I: forme algebrique, trigonometrie, calculs et interpretations geometriques.',
    type: 'cours',
    level: 'prepa',
    subject: 'mathematiques',
    notion: 'nombres complexes',
    primaryKeyword: 'cours nombres complexes mpsi',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/cours/france/prepa/maths/mpsi-mp2i-raisonnement-et-vocabulaire-ensembliste-120': {
    title: 'Raisonnement et vocabulaire ensembliste en MPSI-MP2I | OptiTAB',
    description:
      'Renforce ton raisonnement mathematique en prepa: logique, ensembles, implications et vocabulaire formel pour rediger avec precision.',
    type: 'cours',
    level: 'prepa',
    subject: 'mathematiques',
    notion: 'logique et ensembles',
    primaryKeyword: 'raisonnement ensembliste mpsi',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/cours/france/prepa/maths/mpsi-mp2i-sommes-et-produits-121': {
    title: 'Sommes et produits en MPSI-MP2I: cours et techniques | OptiTAB',
    description:
      'Travaille les sommes et produits en prepa MPSI-MP2I: notations sigma/pi, manipulations algebriques et methodes utiles en exercices.',
    type: 'cours',
    level: 'prepa',
    subject: 'mathematiques',
    notion: 'sommes et produits',
    primaryKeyword: 'cours sommes et produits mpsi',
    searchIntent: 'comprendre'
  },
  '/ressources-gratuites/syntheses/france/lycee/maths/maths-bases-methodes-resume-arithmetique-121': {
    title: 'Fiche de revision: arithmetique (Bases et methodes) | OptiTAB',
    description:
      'Retrouve les essentiels d arithmetique: divisibilite, congruences, PGCD, Bezout et Gauss dans une fiche claire pour reviser efficacement.',
    type: 'synthese',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'arithmetique',
    primaryKeyword: 'fiche arithmetique',
    searchIntent: 'reviser'
  },
  '/ressources-gratuites/syntheses/france/lycee/maths/maths-bases-methodes-resume-combinatoire-et-denombrement-98': {
    title: 'Fiche de revision: combinatoire et denombrement | OptiTAB',
    description:
      'Revise permutations, arrangements, combinaisons et coefficients binomiaux avec une fiche de denombrement concise et operationnelle.',
    type: 'synthese',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'combinatoire et denombrement',
    primaryKeyword: 'fiche combinatoire denombrement',
    searchIntent: 'reviser'
  },
  '/ressources-gratuites/syntheses/france/lycee/maths/premiere-1er-resume-fonction-exponentielle-79': {
    title: 'Fiche de revision sur la fonction exponentielle en Premiere | OptiTAB',
    description:
      'Retrouve l essentiel de la fonction exponentielle en Premiere: proprietes, variations, derivee et methodes de calcul utiles en controle.',
    type: 'synthese',
    level: '1re',
    subject: 'mathematiques',
    notion: 'fonction exponentielle',
    primaryKeyword: 'fiche exponentielle premiere',
    searchIntent: 'reviser'
  },
  '/ressources-gratuites/syntheses/france/lycee/maths/terminal-bac-resume-limites-des-fonctions-73': {
    title: 'Fiche de revision: limites de fonctions en Terminale | OptiTAB',
    description:
      'Retrouve l essentiel des limites de fonctions en Terminale: definitions, operations, formes indeterminees, theoremes et asymptotes.',
    primaryKeyword: 'fiche revision limites fonctions terminale',
    searchIntent: 'reviser'
  },
  '/ressources-gratuites/syntheses/france/lycee/maths/terminal-bac-resume-nombres-complexes-47': {
    title: 'Fiche de revision sur les nombres complexes en Terminale | OptiTAB',
    description:
      'Revise les nombres complexes en Terminale avec une fiche synthese: formes, calculs, conjugue, module, argument et applications geometriques.',
    type: 'synthese',
    level: 'terminale',
    subject: 'mathematiques',
    notion: 'nombres complexes',
    primaryKeyword: 'fiche nombres complexes terminale',
    searchIntent: 'reviser'
  },
  '/ressources-gratuites/syntheses/france/prepa/maths/mpsi-mp2i-resume-sommes-et-produits-58': {
    title: 'Fiche de revision: sommes et produits en MPSI-MP2I | OptiTAB',
    description:
      'Retrouve les formules et methodes sur les sommes et produits en prepa MPSI-MP2I dans une fiche concise pour revision rapide.',
    type: 'synthese',
    level: 'prepa',
    subject: 'mathematiques',
    notion: 'sommes et produits',
    primaryKeyword: 'fiche sommes et produits mpsi',
    searchIntent: 'reviser'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/terminal-bac-derivation-87': {
    title: 'Exercices corriges sur la derivation en Terminale | OptiTAB',
    description:
      'Entraine-toi en derivation avec des exercices corriges pas a pas en Terminale: calcul de derivees, variations, tangentes et convexite.',
    type: 'exercice',
    level: 'terminale',
    subject: 'mathematiques',
    notion: 'derivation',
    primaryKeyword: 'exercices corriges derivation terminale',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/premiere-1er-suites-numeriques-153': {
    title: 'Exercices corriges sur les suites numeriques en Premiere | OptiTAB',
    description:
      'Travaille les suites numeriques avec des exercices corriges en Premiere: suites arithmetiques, geometriques, sens de variation et methodes.',
    type: 'exercice',
    level: '1re',
    subject: 'mathematiques',
    notion: 'suites numeriques',
    primaryKeyword: 'exercices suites numeriques premiere',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/seconde-notion-de-fonction-178': {
    title: 'Exercices corriges sur la notion de fonction en Seconde | OptiTAB',
    description:
      'Entraine-toi en Seconde sur la notion de fonction: images, antecedents, lecture graphique et exercices corriges pour consolider les bases.',
    type: 'exercice',
    level: '2nde',
    subject: 'mathematiques',
    notion: 'notion de fonction',
    primaryKeyword: 'exercices notion de fonction seconde',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/terminal-bac-equations-differentielles-90': {
    title: 'Exercices corriges sur les equations differentielles en Terminale | OptiTAB',
    description:
      'Progresse avec des exercices corriges sur les equations differentielles en Terminale: verification, resolution et interpretation.',
    type: 'exercice',
    level: 'terminale',
    subject: 'mathematiques',
    notion: 'equations differentielles',
    primaryKeyword: 'exercices equations differentielles terminale',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/terminal-bac-arithmetique-103': {
    title: 'Exercices corriges sur l arithmetique en Terminale | OptiTAB',
    description:
      'Exerce-toi sur l arithmetique en Terminale avec des corrections detaillees: divisibilite, congruences, raisonnement et methodes types.',
    type: 'exercice',
    level: 'terminale',
    subject: 'mathematiques',
    notion: 'arithmetique',
    primaryKeyword: 'exercices arithmetique terminale',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/terminal-bac-graphes-et-matrices-104': {
    title: 'Exercices corriges sur graphes et matrices en Terminale | OptiTAB',
    description:
      'Travaille graphes et matrices en Terminale avec des exercices corriges: modelisation, calcul matriciel et interpretation pas a pas.',
    type: 'exercice',
    level: 'terminale',
    subject: 'mathematiques',
    notion: 'graphes et matrices',
    primaryKeyword: 'exercices graphes matrices terminale',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/terminal-bac-limites-des-fonctions-82': {
    title: 'Exercices corriges sur les limites de fonctions en Terminale | OptiTAB',
    description:
      'Entraine-toi sur les limites de fonctions en Terminale avec des exercices corriges: formes indeterminees, theoremes et methodes de calcul.',
    type: 'exercice',
    level: 'terminale',
    subject: 'mathematiques',
    notion: 'limites de fonctions',
    primaryKeyword: 'exercices limites terminale',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/maths-bases-methodes-puissances-229': {
    title: 'Exercices corriges sur les puissances (Bases et methodes) | OptiTAB',
    description:
      'Renforce les regles de calcul sur les puissances avec des exercices corriges progressifs pour automatiser les bonnes methodes.',
    type: 'exercice',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'puissances',
    primaryKeyword: 'exercices puissances corriges',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/maths-bases-methodes-theoreme-de-pythagore-et-sa-reciproque-226': {
    title: 'Exercices corriges sur le theoreme de Pythagore | OptiTAB',
    description:
      'Entraine-toi avec des exercices corriges sur le theoreme de Pythagore et sa reciproque: methodes, justifications et applications.',
    type: 'exercice',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'theoreme de pythagore',
    primaryKeyword: 'exercices pythagore corriges',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/maths-bases-methodes-arithmetique-219': {
    title: 'Exercices corriges d arithmetique (Bases et methodes) | OptiTAB',
    description:
      'Entraine-toi en arithmetique avec des exercices corriges sur divisibilite, congruences et raisonnements types pour consolider la methode.',
    type: 'exercice',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'arithmetique',
    primaryKeyword: 'exercices corriges arithmetique',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/maths-bases-methodes-combinatoire-et-denombrement-196': {
    title: 'Exercices corriges de combinatoire et denombrement | OptiTAB',
    description:
      'Travaille la combinatoire avec des exercices corriges sur permutations, arrangements et combinaisons pour progresser pas a pas.',
    type: 'exercice',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'combinatoire et denombrement',
    primaryKeyword: 'exercices combinatoire denombrement',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/maths-bases-methodes-continuite-des-fonctions-203': {
    title: 'Exercices corriges sur la continuite des fonctions | OptiTAB',
    description:
      'Entraine-toi sur la continuite des fonctions avec des exercices corriges: lecture de conditions, raisonnement et application de theoremes.',
    type: 'exercice',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'continuite des fonctions',
    primaryKeyword: 'exercices continuite fonctions',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/maths-bases-methodes-derivation-207': {
    title: 'Exercices corriges sur la derivation (Bases et methodes) | OptiTAB',
    description:
      'Renforce tes automatismes en derivation avec des exercices corriges progressifs: regles de calcul, tangente et etude de variations.',
    type: 'exercice',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'derivation',
    primaryKeyword: 'exercices derives corriges',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/maths-bases-methodes-developpement-184': {
    title: 'Exercices corriges sur le developpement algebraique | OptiTAB',
    description:
      'Entraine-toi au developpement avec des exercices corriges: distributivite, doubles distributivites et simplifications utiles en calcul litteral.',
    type: 'exercice',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'developpement',
    primaryKeyword: 'exercices developpement algebraique',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/maths-bases-methodes-equations-differentielles-210': {
    title: 'Exercices corriges sur les equations differentielles | OptiTAB',
    description:
      'Progresse sur les equations differentielles avec des exercices corriges: verification de solutions, resolution et interpretation.',
    type: 'exercice',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'equations differentielles',
    primaryKeyword: 'exercices equations differentielles corriges',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/maths-bases-methodes-equations-du-2nd-degre-189': {
    title: 'Exercices corriges sur les equations du second degre | OptiTAB',
    description:
      'Travaille les equations du second degre avec des exercices corriges: discriminant, racines et methodes de resolution selon les cas.',
    type: 'exercice',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'equations du second degre',
    primaryKeyword: 'exercices second degre corriges',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/maths-bases-methodes-equations-fonctions-polynomes-du-second-degre-222': {
    title: 'Exercices corriges: fonctions polynomes du second degre | OptiTAB',
    description:
      'Entraine-toi sur les fonctions polynomes du second degre avec des exercices corriges: forme canonique, sommet et interpretation graphique.',
    type: 'exercice',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'fonctions polynomes du second degre',
    primaryKeyword: 'exercices fonction polynome second degre',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/maths-bases-methodes-equations-simples-1er-degre-188': {
    title: 'Exercices corriges sur les equations du premier degre | OptiTAB',
    description:
      'Maitrise les equations du premier degre avec des exercices corriges: isolement de l inconnue, verifications et methode fiable.',
    type: 'exercice',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'equations simples premier degre',
    primaryKeyword: 'exercices equations premier degre',
    searchIntent: 's exercer'
  },
  '/ressources-gratuites/exercices/france/lycee/maths/maths-bases-methodes-factorisation-187': {
    title: 'Exercices corriges sur la factorisation (Bases et methodes) | OptiTAB',
    description:
      'Entraine-toi a factoriser avec des exercices corriges: facteur commun, identites remarquables et transformations algebriques utiles.',
    type: 'exercice',
    level: 'bases et methodes',
    subject: 'mathematiques',
    notion: 'factorisation',
    primaryKeyword: 'exercices factorisation corriges',
    searchIntent: 's exercer'
  }
})

function normalizeManualSeoEntry(entry) {
  if (!entry || typeof entry !== 'object') return null
  const title = String(entry.title || '').trim()
  const description = String(entry.description || '').trim()
  if (!title && !description) return null
  return {
    ...entry,
    title: title || undefined,
    description: description || undefined
  }
}

export function getManualSeoOverrideByPath(pathname) {
  const normalized = normalizePathname(pathname)
  if (!normalized) return null
  const entry = MANUAL_SEO_OVERRIDES_BY_PATH[normalized]
  return normalizeManualSeoEntry(entry)
}

export function listManualSeoOverridePaths() {
  return Object.keys(MANUAL_SEO_OVERRIDES_BY_PATH)
}

export function listManualSeoOverrides() {
  return Object.entries(MANUAL_SEO_OVERRIDES_BY_PATH).map(([path, entry]) => ({
    path,
    ...entry
  }))
}
