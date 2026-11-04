// Adresses des ressources gratuites (pages statiques générées par
// scripts/ressources ; mêmes adresses que scripts/ressources/classes.mjs).
export const RESSOURCES_GRATUITES = '/ressources-gratuites/'

// Nom de la classe en base (niveau_nom) → adresse de sa page.
const PAGES_DES_CLASSES = {
  CP: 'cp',
  CE1: 'ce1',
  CE2: 'ce2',
  CM1: 'cm1',
  CM2: 'cm2',
  '6ème': '6e',
  '5ème': '5e',
  '4ème': '4e',
  '3ème': '3e',
  '2nde': 'seconde',
  '1ère': 'premiere',
  Terminale: 'terminale'
}

export const ressourcesDeLaClasse = (niveau) =>
  PAGES_DES_CLASSES[niveau] ? `${RESSOURCES_GRATUITES}maths/${PAGES_DES_CLASSES[niveau]}/` : RESSOURCES_GRATUITES
