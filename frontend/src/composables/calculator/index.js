/**
 * Composables pour le calculateur scientifique
 * Export centralisé de tous les composables
 */

// Utilitaires mathématiques
export {
  convertLatexToJS,
  evaluateFunction,
  generateFunctionData,
  numericalDerivative,
  numericalIntegral,
  findZero,
  bisectionMethod
} from './mathUtils'

// Configuration du graphique
export {
  GRAPH_COLORS,
  SPECIAL_COLORS,
  DEFAULT_AXIS_CONFIG,
  createGraphLayout,
  createAxisAnnotations,
  PLOTLY_CONFIG,
  OPERATIONS,
  KEYBOARD_TOOLS,
  isMobile
} from './graphConfig'

// Composable principal du graphique
export { useGraph } from './useGraph'

// Formes géométriques
export { useGraphShapes } from './useGraphShapes'

// Analyse graphique
export { useGraphAnalysis } from './useGraphAnalysis'

// Clavier mathématique
export { useMathKeyboard } from './useMathKeyboard'
