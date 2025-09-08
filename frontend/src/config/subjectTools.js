// Configuration des outils par matière
export const subjectTools = {
  maths: {
    name: 'Mathématiques',
    icon: '🧮',
    tools: {
      algebra: {
        name: 'Algèbre',
        items: [
          [
            { label: '', slot: 'fraction', insert: '\\frac' },
            { label: '', slot: 'sqrt', insert: '\\sqrt{}' },
            { label: '', slot: 'nsqrt', insert: '\\sqrt[n]{}' },
            { label: '', slot: 'exposant', insert: '^\\square' },
            { label: 'ln', insert: '\\ln(' },
            { label: '', slot: 'exp', insert: '\\exp(' }
          ]
        ]
      },
      trigonometry: {
        name: 'Trigonométrie',
        items: [
          [
            { label: 'sin', insert: '\\sin(' },
            { label: 'cos', insert: '\\cos(' },
            { label: 'tan', insert: '\\tan(' },
            { label: 'arcsin', insert: '\\arcsin(' },
            { label: 'arccos', insert: '\\arccos(' },
            { label: 'arctan', insert: '\\arctan(' }
          ]
        ]
      },
      calculus: {
        name: 'Calcul différentiel',
        actions: [
          { label: 'Dériver', action: 'derive' },
          { label: 'Intégrer', action: 'integrate' },
          { label: 'Résoudre équation', action: 'solve' }
        ]
      }
    }
  },
  
  physics: {
    name: 'Physique',
    icon: '⚡',
    tools: {
      mechanics: {
        name: 'Mécanique',
        actions: [
          { label: 'Vitesse', action: 'calculateVelocity' },
          { label: 'Accélération', action: 'calculateAcceleration' },
          { label: 'Force', action: 'calculateForce' }
        ]
      },
      electricity: {
        name: 'Électricité',
        actions: [
          { label: 'Résistance', action: 'calculateResistance' },
          { label: 'Puissance', action: 'calculatePower' },
          { label: 'Intensité', action: 'calculateCurrent' }
        ]
      },
      waves: {
        name: 'Ondes',
        actions: [
          { label: 'Fréquence', action: 'calculateFrequency' },
          { label: 'Longueur d\'onde', action: 'calculateWavelength' }
        ]
      }
    }
  },
  
  chemistry: {
    name: 'Chimie',
    icon: '🧪',
    tools: {
      stoichiometry: {
        name: 'Stœchiométrie',
        actions: [
          { label: 'Équilibrer équation', action: 'balanceEquation' },
          { label: 'Calculer moles', action: 'calculateMoles' },
          { label: 'Concentration', action: 'calculateConcentration' }
        ]
      },
      solutions: {
        name: 'Solutions',
        actions: [
          { label: 'Dilution', action: 'calculateDilution' },
          { label: 'pH', action: 'calculatePH' }
        ]
      }
    }
  }
}

// Fonction utilitaire pour obtenir les outils d'une matière
export function getSubjectTools(subjectId) {
  return subjectTools[subjectId] || subjectTools.maths
}

// Fonction utilitaire pour obtenir une catégorie d'outils
export function getToolCategory(subjectId, categoryId) {
  const subject = getSubjectTools(subjectId)
  return subject.tools[categoryId] || null
}

// Fonction utilitaire pour obtenir toutes les catégories d'une matière
export function getToolCategories(subjectId) {
  const subject = getSubjectTools(subjectId)
  return Object.keys(subject.tools).map(key => ({
    id: key,
    ...subject.tools[key]
  }))
} 