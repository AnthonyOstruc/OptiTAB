/**
 * Configuration et constantes pour le graphique
 */

// Couleurs pour les fonctions
export const GRAPH_COLORS = [
  '#3b82f6', // blue
  '#ef4444', // red
  '#10b981', // green
  '#f59e0b', // amber
  '#8b5cf6', // violet
  '#ec4899', // pink
  '#06b6d4', // cyan
  '#84cc16', // lime
  '#f97316', // orange
  '#6366f1'  // indigo
]

// Couleurs pour les éléments spéciaux
export const SPECIAL_COLORS = {
  intersection: '#ff0000',
  axisIntersection: '#22c55e',
  tangent: '#9333ea',
  asymptote: '#64748b',
  integralArea: 'rgba(59, 130, 246, 0.3)',
  areaBetweenCurves: 'rgba(16, 185, 129, 0.3)'
}

// Configuration par défaut des axes
export const DEFAULT_AXIS_CONFIG = {
  xMin: -10,
  xMax: 10,
  yMin: -10,
  yMax: 10
}

/**
 * Détecte si on est sur mobile
 * @returns {boolean}
 */
export function isMobile() {
  if (typeof window === 'undefined') return false
  return window.innerWidth <= 768
}

/**
 * Crée le layout pour le graphique vide ou avec fonctions
 * @param {Object} options - Options de configuration
 * @returns {Object} - Layout Plotly
 */
export function createGraphLayout(options = {}) {
  const {
    xMin = -10,
    xMax = 10,
    yMin = -10,
    yMax = 10,
    showGrid = true,
    showAxes = true,
    showTicks = true
  } = options

  const mobile = isMobile()
  
  // Configuration MOBILE
  if (mobile) {
    return {
      xaxis: {
        range: [xMin, xMax],
        gridcolor: '#e5e7eb',
        showgrid: showGrid,
        zerolinecolor: '#374151',
        zerolinewidth: showAxes ? 2 : 0,
        zeroline: showAxes,
        fixedrange: false,
        showline: showAxes,
        linecolor: '#374151',
        linewidth: 1.5,
        mirror: false,
        // MOBILE: Graduations tous les 2
        tickmode: 'array',
        tickvals: [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10],
        showticklabels: showTicks,
        ticks: showTicks ? 'outside' : '',
        tickfont: { size: 9 }
      },
      yaxis: {
        range: [yMin, yMax],
        gridcolor: '#e5e7eb',
        showgrid: showGrid,
        zerolinecolor: '#374151',
        zerolinewidth: showAxes ? 2 : 0,
        zeroline: showAxes,
        fixedrange: false,
        showline: showAxes,
        linecolor: '#374151',
        linewidth: 1.5,
        mirror: false,
        // MOBILE: Graduations tous les 2
        tickmode: 'array',
        tickvals: [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10],
        showticklabels: showTicks,
        ticks: showTicks ? 'outside' : '',
        tickfont: { size: 9 }
      },
      annotations: [], // Pas de labels x/y sur mobile
      plot_bgcolor: 'white',
      paper_bgcolor: 'white',
      margin: { t: 10, r: 10, b: 30, l: 30 },
      hovermode: 'closest',
      autosize: true,
      legend: {
        font: { size: 10 },
        bgcolor: 'rgba(255, 255, 255, 0.95)',
        bordercolor: '#e5e7eb',
        borderwidth: 1,
        x: 0.5,
        y: -0.12,
        xanchor: 'center',
        yanchor: 'top',
        orientation: 'h',
        itemsizing: 'constant',
        itemwidth: 20,
        tracegroupgap: 3
      }
    }
  }
  
  // Configuration DESKTOP
  return {
    xaxis: {
      title: {
        text: 'x',
        font: { size: 16, color: '#1e3a8a' },
        standoff: 10
      },
      range: [xMin, xMax],
      gridcolor: '#e5e7eb',
      showgrid: showGrid,
      zerolinecolor: '#374151',
      zerolinewidth: showAxes ? 2 : 0,
      zeroline: showAxes,
      fixedrange: false,
      showline: showAxes,
      linecolor: '#374151',
      linewidth: 2,
      mirror: false,
      tickmode: 'linear',
      dtick: 1,
      tick0: 0,
      ticklabelstep: 2,
      showticklabels: showTicks,
      ticks: showTicks ? 'outside' : '',
      tickfont: { size: 12 },
      scaleanchor: 'y',
      scaleratio: 1
    },
    yaxis: {
      title: {
        text: 'y',
        font: { size: 16, color: '#1e3a8a' },
        standoff: 10
      },
      range: [yMin, yMax],
      gridcolor: '#e5e7eb',
      showgrid: showGrid,
      zerolinecolor: '#374151',
      zerolinewidth: showAxes ? 2 : 0,
      zeroline: showAxes,
      fixedrange: false,
      showline: showAxes,
      linecolor: '#374151',
      linewidth: 2,
      tickmode: 'linear',
      dtick: 1,
      tick0: 0,
      mirror: false,
      ticklabelstep: 2,
      showticklabels: showTicks,
      ticks: showTicks ? 'outside' : '',
      tickfont: { size: 12 }
    },
    annotations: createAxisAnnotations(xMax, yMax),
    plot_bgcolor: 'white',
    paper_bgcolor: 'white',
    margin: { t: 60, r: 60, b: 60, l: 80 },
    hovermode: 'closest',
    autosize: true,
    legend: {
      font: { size: 13 },
      bgcolor: 'rgba(255, 255, 255, 0.95)',
      bordercolor: '#e5e7eb',
      borderwidth: 1,
      x: 1.02,
      y: 1,
      xanchor: 'left',
      yanchor: 'top',
      orientation: 'v',
      itemsizing: 'constant',
      itemwidth: 30,
      tracegroupgap: 5
    }
  }
}

/**
 * Crée les annotations pour les flèches des axes
 */
export function createAxisAnnotations(xMax, yMax) {
  return [
    // Flèche pour l'axe X
    {
      x: xMax,
      y: 0,
      xref: 'x',
      yref: 'y',
      text: '',
      showarrow: true,
      axref: 'x',
      ayref: 'y',
      ax: xMax * 0.95,
      ay: 0,
      arrowhead: 2,
      arrowsize: 1,
      arrowwidth: 2,
      arrowcolor: '#374151'
    },
    // Label "x"
    {
      x: xMax,
      y: 0,
      xref: 'x',
      yref: 'y',
      text: '<b>x</b>',
      showarrow: false,
      xanchor: 'left',
      yanchor: 'middle',
      xshift: 8,
      yshift: 0,
      font: {
        size: 16,
        color: '#1e3a8a',
        family: 'Arial, sans-serif'
      }
    },
    // Flèche pour l'axe Y
    {
      x: 0,
      y: yMax,
      xref: 'x',
      yref: 'y',
      text: '',
      showarrow: true,
      axref: 'x',
      ayref: 'y',
      ax: 0,
      ay: yMax * 0.95,
      arrowhead: 2,
      arrowsize: 1,
      arrowwidth: 2,
      arrowcolor: '#374151'
    },
    // Label "y"
    {
      x: 0,
      y: yMax,
      xref: 'x',
      yref: 'y',
      text: '<b>y</b>',
      showarrow: false,
      xanchor: 'center',
      yanchor: 'bottom',
      xshift: -10,
      yshift: 20,
      font: {
        size: 16,
        color: '#1e3a8a',
        family: 'Arial, sans-serif'
      }
    }
  ]
}

/**
 * Configuration Plotly par défaut
 */
export const PLOTLY_CONFIG = {
  responsive: true,
  displayModeBar: true,
  displaylogo: false,
  scrollZoom: false,
  staticPlot: false,
  editable: false,
  modeBarButtonsToRemove: [
    'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'zoom2d',
    'pan2d', 'select2d', 'lasso2d', 'resetScale2d'
  ]
}

/**
 * Configuration des opérations disponibles
 */
export const OPERATIONS = [
  {
    id: 'derivative',
    name: 'Dérivée',
    description: 'Calculer la dérivée d\'une fonction',
    placeholder: { text: 'Fonction à dériver (ex: ', latex: '(x+1)^{2}' }
  },
  {
    id: 'integral',
    name: 'Intégrale',
    description: 'Calculer l\'intégrale d\'une fonction',
    placeholder: { text: 'Fonction à intégrer (ex: ', latex: 'x^{2}' }
  },
  {
    id: 'limit',
    name: 'Limite',
    description: 'Calculer la limite d\'une fonction',
    placeholder: { text: 'Fonction pour la limite (ex: ', latex: '\\frac{x^{2}-1}{x-1}' }
  },
  {
    id: 'expand',
    name: 'Développement',
    description: 'Développer une expression',
    placeholder: { text: 'Expression à développer (ex: ', latex: '(x+1)^{2}' }
  },
  {
    id: 'factor',
    name: 'Factorisation',
    description: 'Factoriser une expression',
    placeholder: { text: 'Expression à factoriser (ex: ', latex: 'x^{2}-1' }
  },
  {
    id: 'graph',
    name: 'Graphique',
    description: 'Tracer le graphique d\'une fonction',
    placeholder: { text: 'Fonction à tracer (ex: ', latex: 'x^{2}, \\sin(x), \\ln(x)' }
  }
]

/**
 * Outils pour le clavier mathématique
 */
export const KEYBOARD_TOOLS = {
  algebra: [
    { label: '', slot: 'fraction', insert: '\\frac' },
    { label: '', slot: 'sqrt', insert: '\\sqrt{}' },
    { label: '', slot: 'nsqrt', insert: '\\sqrt[n]{}' },
    { label: '', slot: 'exposant', insert: '^\\square' },
    { label: 'ln', insert: '\\ln(' },
    { label: '', slot: 'exp', insert: '\\exp(' }
  ],
  trigonometry: [
    { label: 'sin', insert: '\\sin(' },
    { label: 'cos', insert: '\\cos(' },
    { label: 'tan', insert: '\\tan(' },
    { label: 'csc', insert: '\\csc(' },
    { label: 'sec', insert: '\\sec(' },
    { label: 'cot', insert: '\\cot(' },
    { label: 'arcsin', insert: '\\arcsin(' },
    { label: 'arccos', insert: '\\arccos(' },
    { label: 'arctan', insert: '\\arctan(' }
  ],
  exponential: [
    { label: 'exp', insert: '\\exp(' },
    { label: 'ln', insert: '\\ln(' },
    { label: 'log', insert: '\\log(' },
    { label: 'log₁₀', insert: '\\log_{10}(' },
    { label: 'log₂', insert: '\\log_{2}(' },
    { label: 'e^x', insert: 'e^{' },
    { label: '10^x', insert: '10^{' },
    { label: '2^x', insert: '2^{' }
  ],
  special: [
    { label: '|x|', insert: '\\left|' },
    { label: '√', insert: '\\sqrt{' },
    { label: '∛', insert: '\\sqrt[3]{' },
    { label: 'ⁿ√', insert: '\\sqrt[n]{' },
    { label: 'π', insert: '\\pi' },
    { label: 'e', insert: 'e' },
    { label: 'sinh', insert: '\\sinh(' },
    { label: 'cosh', insert: '\\cosh(' },
    { label: 'tanh', insert: '\\tanh(' }
  ]
}
