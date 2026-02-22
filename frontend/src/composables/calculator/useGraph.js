/**
 * Composable principal pour le graphique
 */
import { ref, nextTick, watch } from 'vue'
import Plotly from 'plotly.js-dist-min'
import katex from 'katex'
import { GRAPH_COLORS, createGraphLayout, PLOTLY_CONFIG } from './graphConfig'
import { generateFunctionData } from './mathUtils'

export function useGraph() {
  // Références
  const graphContainer = ref(null)
  const functionExpressionRefs = ref([])
  
  // État des bornes
  const xMin = ref(-10)
  const xMax = ref(10)
  const yMin = ref(-10)
  const yMax = ref(10)
  
  // Options d'affichage
  const showGrid = ref(true)
  const showAxes = ref(true)
  const showTicks = ref(true)
  
  // Fonctions tracées
  const graphFunctions = ref([])

  const MAX_FUNCTION_NAME_LENGTH = 30

  function sanitizeFunctionName(value) {
    const raw = (value ?? '').toString().trim()
    if (!raw) return ''
    return raw.slice(0, MAX_FUNCTION_NAME_LENGTH)
  }

  function getFunctionDisplayName(func, index) {
    const custom = sanitizeFunctionName(func?.name)
    return custom || `f${index + 1}`
  }

  function splitFunctionNameParts(name) {
    const match = name.match(/^([a-zA-Z]+)([0-9]+)$/)
    if (match) return { base: match[1], sub: match[2] }
    return { base: name, sub: '' }
  }

  function getFunctionNameHtml(func, index) {
    const display = getFunctionDisplayName(func, index)
    const parts = splitFunctionNameParts(display)
    return `${parts.base}${parts.sub ? `<sub>${parts.sub}</sub>` : ''}`
  }

  function getFunctionLatexLabel(func, index) {
    const display = getFunctionDisplayName(func, index)
    const match = display.match(/^([a-zA-Z]+)([0-9]+)$/)
    if (match) return `${match[1]}_{${match[2]}}`
    return display
  }
  
  // Compteur de couleurs
  let colorIndex = 0
  
  function getNextColor() {
    const color = GRAPH_COLORS[colorIndex % GRAPH_COLORS.length]
    colorIndex++
    return color
  }
  
  function resetColorIndex() {
    colorIndex = 0
  }

  /**
   * Initialise un graphique vide
   */
  function initializeGraph() {
    if (!graphContainer.value) return
    
    clearGraph()
    
    const layout = createGraphLayout({
      xMin: xMin.value,
      xMax: xMax.value,
      yMin: yMin.value,
      yMax: yMax.value,
      showGrid: showGrid.value,
      showAxes: showAxes.value,
      showTicks: showTicks.value
    })
    
    Plotly.newPlot(graphContainer.value, [], layout, PLOTLY_CONFIG)
      .catch((err) => {
        console.error('Erreur Plotly (initializeGraph):', err)
      })
  }

  /**
   * Ajoute une fonction au graphique
   * @param {string} expression - Expression LaTeX
   * @param {Object} options - Options (type, value pour droites)
   */
  function addFunction(expression, options = {}) {
    const color = getNextColor()
    
    // Détecter le type de fonction
    let type = options.type || 'function'
    let value = options.value || null
    
    const verticalMatch = expression.match(/^x\s*=\s*([\-\d\.]+)$/)
    const horizontalMatch = expression.match(/^y\s*=\s*([\-\d\.]+)$/)
    
    if (verticalMatch) {
      type = 'vertical'
      value = parseFloat(verticalMatch[1])
    } else if (horizontalMatch) {
      type = 'horizontal'
      value = parseFloat(horizontalMatch[1])
    }
    
    graphFunctions.value.push({
      name: '',
      expression: expression,
      color: color,
      latex: expression,
      type: type,
      value: value
    })
    
    return graphFunctions.value.length - 1
  }

  /**
   * Supprime une fonction du graphique
   * @param {number} index - Index de la fonction
   */
  function removeFunction(index) {
    graphFunctions.value.splice(index, 1)
  }

  /**
   * Édite une fonction (la charge pour modification)
   * @param {number} index - Index de la fonction
   * @returns {Object} - La fonction supprimée
   */
  function editFunction(index) {
    const func = graphFunctions.value[index]
    if (func) {
      removeFunction(index)
      return func
    }
    return null
  }

  /**
   * Génère les traces pour toutes les fonctions
   * @returns {Array} - Tableau de traces Plotly
   */
  function generateFunctionTraces() {
    const traces = []
    
    graphFunctions.value.forEach((func, index) => {
      try {
        const funcNameHtml = getFunctionNameHtml(func, index)
        if (func.type === 'vertical') {
          // Droite verticale x = constante
          traces.push({
            x: [func.value, func.value],
            y: [yMin.value, yMax.value],
            type: 'scatter',
            mode: 'lines',
            line: { color: func.color, width: 2 },
            name: `${funcNameHtml}(x) = x = ${func.value}`,
            showlegend: true
          })
        } else if (func.type === 'horizontal') {
          // Droite horizontale y = constante
          traces.push({
            x: [xMin.value, xMax.value],
            y: [func.value, func.value],
            type: 'scatter',
            mode: 'lines',
            line: { color: func.color, width: 2 },
            name: `${funcNameHtml}(x) = y = ${func.value}`,
            showlegend: true
          })
        } else {
          // Fonction normale
          const data = generateFunctionData(func.latex, xMin.value, xMax.value, yMin.value, yMax.value)
          traces.push({
            x: data.x,
            y: data.y,
            type: 'scatter',
            mode: 'lines',
            line: { color: func.color, width: 2 },
            name: `${funcNameHtml}(x) = ${func.expression}`,
            showlegend: true,
            connectgaps: false,
            hovertemplate: `<b>${funcNameHtml}</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>`
          })
        }
      } catch (error) {
        console.error(`Erreur pour la fonction ${index + 1}:`, error)
      }
    })
    
    return traces
  }

  /**
   * Trace toutes les fonctions sur le graphique
   * @param {Array} additionalTraces - Traces supplémentaires (formes, analyses, etc.)
   */
  function plotAllFunctions(additionalTraces = []) {
    if (!graphContainer.value) return
    
    const traces = [...generateFunctionTraces(), ...additionalTraces]
    
    const layout = createGraphLayout({
      xMin: xMin.value,
      xMax: xMax.value,
      yMin: yMin.value,
      yMax: yMax.value,
      showGrid: showGrid.value,
      showAxes: showAxes.value,
      showTicks: showTicks.value
    })
    
    Plotly.newPlot(graphContainer.value, traces, layout, PLOTLY_CONFIG)
      .then(() => {
        nextTick(() => renderFunctionExpressions())
      })
      .catch((err) => {
        console.error('Erreur Plotly (plotAllFunctions):', err)
      })
  }

  /**
   * Efface le graphique
   */
  function clearGraph() {
    graphFunctions.value = []
    if (graphContainer.value) {
      Plotly.purge(graphContainer.value)
    }
  }

  /**
   * Réinitialise le zoom
   */
  function resetZoom() {
    if (graphContainer.value && graphFunctions.value.length > 0) {
      Plotly.relayout(graphContainer.value, {
        'xaxis.range': [xMin.value, xMax.value],
        'yaxis.range': [yMin.value, yMax.value]
      })
    }
  }

  /**
   * Met à jour les bornes du graphique
   */
  function updateBounds(newXMin, newXMax, newYMin, newYMax) {
    xMin.value = newXMin
    xMax.value = newXMax
    yMin.value = newYMin
    yMax.value = newYMax
  }

  /**
   * Rend les expressions LaTeX dans les éléments référencés
   */
  function renderFunctionExpressions() {
    graphFunctions.value.forEach((func, index) => {
      const el = functionExpressionRefs.value[index]
      if (el) {
        try {
          katex.render(`${getFunctionLatexLabel(func, index)}(x) = ${func.latex}`, el, {
            throwOnError: false,
            displayMode: false
          })
        } catch (e) {
          el.textContent = `${getFunctionDisplayName(func, index)}(x) = ${func.expression}`
        }
      }
    })
  }

  /**
   * Vérifie si le graphique a des fonctions
   */
  function hasFunctions() {
    return graphFunctions.value.length > 0
  }

  return {
    // Références
    graphContainer,
    functionExpressionRefs,
    
    // État
    xMin,
    xMax,
    yMin,
    yMax,
    showGrid,
    showAxes,
    showTicks,
    graphFunctions,
    
    // Actions
    initializeGraph,
    addFunction,
    removeFunction,
    editFunction,
    plotAllFunctions,
    clearGraph,
    resetZoom,
    updateBounds,
    
    // Utilitaires
    generateFunctionTraces,
    renderFunctionExpressions,
    hasFunctions,
    getNextColor,
    resetColorIndex
  }
}
