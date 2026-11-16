// Titres des pages pour Google (<title>) : 65 caractères au plus, sinon
// Google les coupe par « … » dans ses résultats.
//
// Les titres des chapitres viennent de la base (« Organisation et gestion de
// données : mener une enquête, construire des tableaux et des diagrammes –
// Cours de maths CP ») : les plus longs ont ici une version courte rédigée à
// la main, distincte dans chaque classe et qui garde les mots-clés. Le titre
// affiché sur la page (h1) ne change pas. Un titre long inconnu est raccourci
// par la règle de secours (sous-titre retiré, puis découpe aux virgules).
export const MAX_TITRE = 65
const MARQUE = ' | OptiTAB'

// Titre du chapitre (avant « – Cours de maths CP ») → version courte.
const CHAPITRES = {
  // CP
  'Organisation et gestion de données : mener une enquête, construire des tableaux et des diagrammes': 'Enquêtes, tableaux et diagrammes',
  'Résoudre des problèmes : partager équitablement ou former des paquets': 'Problèmes de partage et de paquets',
  'Résoudre des problèmes : chercher une partie ou la quantité initiale': 'Problèmes : partie ou quantité initiale',
  'Résoudre des problèmes : réunir des groupes de même taille': 'Problèmes : groupes de même taille',
  'Calcul mental : ajouter et soustraire 1, 2 ou des dizaines': 'Calcul mental : 1, 2 ou des dizaines',
  'Calcul mental : soustraire par décomposition et échange': 'Calcul mental : soustraire en décomposant',
  'Calcul mental : additionner en décomposant': 'Calcul mental : ajouter en décomposant',
  'Le repérage dans l’espace : positions et déplacements': 'Se repérer : positions et déplacements',
  'Le repérage dans le temps : les heures entières': 'Repérage dans le temps : heures entières',
  'Les nombres entiers : dizaines et unités de 11 à 20': 'Dizaines et unités de 11 à 20',
  'Les nombres entiers : comparer, ranger et repérer': 'Comparer, ranger et repérer les nombres',
  'Les nombres entiers : lire et écrire jusqu’à 59': 'Lire et écrire les nombres jusqu’à 59',
  'Les nombres entiers : comparer des quantités': 'Nombres entiers : comparer des quantités',
  'Les nombres ordinaux : rangs et suites de motifs': 'Nombres ordinaux : rangs et motifs',
  'La géométrie plane : construire sur quadrillage': 'Géométrie : construire sur quadrillage',
  'La géométrie plane : formes et alignements': 'Géométrie : formes et alignements',
  // CE2, CM1, CM2
  'Multiplier par 10, par 100 et par des dizaines': 'Multiplier par 10, 100 et des dizaines',
  'Enquêter, lire et construire des graphiques': 'Lire et construire des graphiques',
  'Comparer, encadrer et arrondir les décimaux': 'Encadrer et arrondir les décimaux',
  'Fractions décimales et écriture à virgule': 'Fractions décimales et nombres à virgule',
  'Additionner, soustraire et multiplier des entiers': 'Additionner, soustraire, multiplier',
  'Longueurs, masses, contenances et périmètres': 'Longueurs, masses, contenances',
  'Raisonner en situation de proportionnalité': 'Raisonner avec la proportionnalité',
  'Organiser, représenter et lire des données': 'Organiser et lire des données',
  // Collège
  'Repérage et grandeurs en fonction d’une autre': 'Grandeur en fonction d’une autre',
  'Translations, agrandissements et réductions': 'Translations et agrandissements',
  'Relier des grandeurs et lire des graphiques': 'Grandeurs et lecture de graphiques',
  'Puissances, racines et écriture scientifique': 'Puissances et écriture scientifique',
  'Théorème de Thalès et triangles semblables': 'Thalès et triangles semblables',
  // Seconde
  'Utiliser les notions de multiple, diviseur et de nombre premier': 'Multiples et nombres premiers',
  'Utiliser l’information chiffrée et statistique descriptive': 'Information chiffrée et statistiques',
  'Représenter algébriquement et graphiquement les fonctions': 'Représenter les fonctions',
  'Utiliser les variables et les instructions élémentaires': 'Variables et instructions',
  'Étudier les variations et les extremums d’une fonction': 'Variations et extremums',
  'Se constituer un répertoire de fonctions de référence': 'Fonctions de référence',
  'Représenter et caractériser les droites du plan': 'Équations de droites du plan',
  'Modéliser le hasard, calculer des probabilités': 'Probabilités : modéliser le hasard',
  // Première
  'Dérivation, variations et courbes représentatives': 'Dérivation et variations',
  'Équations, fonctions polynômes du second degré': 'Polynômes du second degré',
  'Probabilités conditionnelles et indépendance': 'Probabilités conditionnelles',
  'Calcul vectoriel et produit scalaire': 'Calcul vectoriel, produit scalaire',
  'Algorithmes du programme de Première': 'Algorithmes du programme',
  // Terminale
  'Manipulation des vecteurs, des droites et des plans de l’espace': 'Vecteurs et plans de l’espace',
  'Représentations paramétriques et équations cartésiennes': 'Représentations paramétriques',
  'Continuité des fonctions d’une variable réelle': 'Continuité des fonctions',
  'Orthogonalité et distances dans l’espace': 'Orthogonalité et distances',
  'Concentration, loi des grands nombres': 'Loi des grands nombres',
  'Algorithmes du programme de Terminale': 'Algorithmes du programme',
  'Schéma de Bernoulli et loi binomiale': 'Bernoulli et loi binomiale'
}

// Titres complets fabriqués ailleurs (accueil des ressources).
const PAGES = {
  'Cours de maths gratuits du CP à la Terminale : cours, fiches, exercices corrigés': 'Cours de maths gratuits du CP à la Terminale'
}

const SUFFIXE = / – ((?:Cours de maths|Fiche de révision|Exercices corrigés) .+)$/

// Règle de secours : sous-titre retiré, puis découpe aux virgules.
function raccourcir(tete, fin) {
  if ((tete + fin).length <= MAX_TITRE) return tete + fin
  const avant = tete.split(' : ')[0]
  if (avant !== tete && avant.length >= 15 && (avant + fin).length <= MAX_TITRE) return avant + fin
  const morceaux = tete.split(', ')
  while (morceaux.length > 1 && (morceaux.join(', ') + fin).length > MAX_TITRE) morceaux.pop()
  const t = morceaux.join(', ')
  if ((t + fin).length <= MAX_TITRE) return t + fin
  const mots = t.split(' ')
  while (mots.length > 2 && (mots.join(' ') + fin).length > MAX_TITRE) mots.pop()
  while (mots.length > 2 && /^(de|des|du|d’|la|le|les|l’|et|ou|à|en|au|aux|un|une|par|pour|sur)$/i.test(mots[mots.length - 1])) mots.pop()
  return mots.join(' ') + fin
}

// Titre de la page : avec « | OptiTAB » s'il tient, sinon sans, sinon raccourci.
export function titreDePage(titre) {
  let t = PAGES[titre] || titre
  const m = t.match(SUFFIXE)
  if (m) {
    const tete = t.slice(0, m.index)
    if (CHAPITRES[tete]) t = `${CHAPITRES[tete]} – ${m[1]}`
  }
  if ((t + MARQUE).length <= MAX_TITRE) return t + MARQUE
  if (t.length <= MAX_TITRE) return t
  return m ? raccourcir(t.slice(0, t.length - m[0].length), m[0]) : raccourcir(t, '')
}
