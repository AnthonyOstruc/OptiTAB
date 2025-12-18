/**
 * Utilitaires mathématiques pour la conversion LaTeX/JS et l'évaluation de fonctions
 */

/**
 * Convertit une expression LaTeX en JavaScript évaluable
 * @param {string} latex - Expression LaTeX
 * @returns {string} - Expression JavaScript
 */
export function convertLatexToJS(latex) {
  let js = String(latex || '')
  
  // 0) Normaliser certains tokens LaTeX
  js = js.replace(/\\left/g, '')
  js = js.replace(/\\right/g, '')
  
  // 0.5) Normaliser les signes moins
  js = js.replace(/([+\-*/^(])[\s]*-[\s]*([a-zA-Z0-9().]+)/g, '$1(-$2)')
  if (js.trim().startsWith('-')) {
    js = '(0' + js + ')'
  }
  
  // 1) Fractions
  js = js.replace(/\\frac{([^}]*)}{([^}]*)}/g, '(($1)/($2))')
  
  // 2) Racines
  js = js.replace(/\\sqrt\[([^\]]+)\]{([^}]+)}/g, 'Math.pow($2, 1/($1))')
  js = js.replace(/\\sqrt{([^}]+)}/g, 'Math.sqrt($1)')
  
  // 3) Constantes
  js = js.replace(/\\pi\b/g, 'Math.PI')
  js = js.replace(/\\e\b/g, 'Math.E')
  
  // 4) Exponentielles / Logs
  js = js.replace(/\\exp\(([^)]+)\)/g, 'Math.exp($1)')
  js = js.replace(/\\ln\(([^)]+)\)/g, 'Math.log($1)')
  js = js.replace(/\\log\(([^)]+)\)/g, 'Math.log10($1)')
  js = js.replace(/\\log_\{([^}]+)\}\(([^)]+)\)/g, '(Math.log($2)/Math.log($1))')
  
  // 5) Trigonométrie
  const trigAll = ['sin','cos','tan','sinh','cosh','tanh','arcsin','arccos','arctan']
  for (const fn of trigAll) {
    const target = fn.startsWith('arc') ? 'a' + fn.slice(3) : fn
    const powRegex = new RegExp('\\\\' + fn + '\\^\\{([^}]+)\\}\\(([^)]+)\\)', 'g')
    js = js.replace(powRegex, 'Math.pow(Math.' + target + '($2),$1)')
    const callRegex = new RegExp('\\\\' + fn + '\\(([^)]+)\\)', 'g')
    js = js.replace(callRegex, 'Math.' + target + '($1)')
  }
  
  // Fonctions réciproques
  js = js.replace(/\\sec\(([^)]+)\)/g, '(1/Math.cos($1))')
  js = js.replace(/\\csc\(([^)]+)\)/g, '(1/Math.sin($1))')
  js = js.replace(/\\cot\(([^)]+)\)/g, '(1/Math.tan($1))')
  
  // Fonctions sans parenthèses
  js = js.replace(/\\sin\s+([a-zA-Z0-9]+)/g, 'Math.sin($1)')
  js = js.replace(/\\cos\s+([a-zA-Z0-9]+)/g, 'Math.cos($1)')
  js = js.replace(/\\tan\s+([a-zA-Z0-9]+)/g, 'Math.tan($1)')
  js = js.replace(/\\ln\s+([a-zA-Z0-9]+)/g, 'Math.log($1)')
  js = js.replace(/\\log\s+([a-zA-Z0-9]+)/g, 'Math.log10($1)')
  js = js.replace(/\\exp\s+([a-zA-Z0-9]+)/g, 'Math.exp($1)')
  
  // 6) Valeur absolue - gérer différentes syntaxes
  // \vert ou \lvert \rvert
  js = js.replace(/\\l?vert([^\\]+)\\r?vert/g, 'Math.abs($1)')
  // |expr|
  js = js.replace(/\|([^|]+)\|/g, 'Math.abs($1)')
  // \abs{expr}
  js = js.replace(/\\abs\{([^}]+)\}/g, 'Math.abs($1)')
  // Nettoyer les doubles parenthèses
  js = js.replace(/Math\.abs\(([^)]+)\)\)/g, 'Math.abs($1))')
  
  // 7) Puissances
  js = js.replace(/\^\{([^}]+)\}/g, '**($1)')
  js = js.replace(/\^([a-zA-Z0-9]+)/g, '**$1')
  
  // 8) e isolé
  js = js.replace(/\be\b/g, 'Math.E')
  
  // 9) Multiplication implicite
  js = js.replace(/\)\s*\(/g, ')*(')
  js = js.replace(/(\d|x)\s*\(/g, '$1*(')
  js = js.replace(/\)\s*(x|Math\.)/g, ')*$1')
  js = js.replace(/(\d|x)\s*(Math\.)/g, '$1*$2')
  js = js.replace(/(\d)(x)/g, '$1*$2')
  js = js.replace(/(x)(\d)/g, '$1*$2')
  
  return js
}

/**
 * Évalue une fonction JavaScript pour une valeur x donnée
 * @param {string} expression - Expression JavaScript
 * @param {number} x - Valeur de x
 * @returns {number} - Résultat ou NaN
 */
export function evaluateFunction(expression, x) {
  let expr = expression.replace(/x/g, `(${x})`)
  expr = expr.replace(/\s+/g, '')
  
  try {
    const result = Function('"use strict"; return (' + expr + ')')()
    if (typeof result === 'number' && isFinite(result) && !isNaN(result)) {
      return result
    }
    return NaN
  } catch (error) {
    console.warn(`Erreur d'évaluation pour x=${x}:`, error.message)
    return NaN
  }
}

/**
 * Génère les données x,y pour tracer une fonction
 * @param {string} latexExpression - Expression LaTeX
 * @param {number} xMin - Borne min de x
 * @param {number} xMax - Borne max de x
 * @param {number} yMin - Borne min de y (optionnel, pour filtrage)
 * @param {number} yMax - Borne max de y (optionnel, pour filtrage)
 * @param {number} numPoints - Nombre de points
 * @returns {Object} - { x: [], y: [], jsExpression }
 */
export function generateFunctionData(latexExpression, xMin, xMax, yMin = -10, yMax = 10, numPoints = 3000) {
  const jsExpression = convertLatexToJS(latexExpression)
  
  console.log('Expression LaTeX:', latexExpression)
  console.log('Expression JS convertie:', jsExpression)
  
  const xValues = []
  const yValues = []
  const step = (xMax - xMin) / numPoints
  
  // Filtrage très permissif pour voir toute la courbe même avec de grandes valeurs
  const yLimit = Math.max(Math.abs(yMax), Math.abs(yMin)) * 100
  
  let lastWasValid = false
  
  for (let i = 0; i <= numPoints; i++) {
    const xi = xMin + i * step
    const yi = evaluateFunction(jsExpression, xi)
    
    // Vérifier que la valeur est valide
    if (!isNaN(yi) && isFinite(yi) && Math.abs(yi) <= yLimit) {
      xValues.push(xi)
      yValues.push(yi)
      lastWasValid = true
    } else {
      // Si la valeur n'est pas valide et qu'on avait des points valides avant,
      // ajouter un point null pour créer une discontinuité visible dans Plotly
      if (lastWasValid && xValues.length > 0) {
        xValues.push(xi)
        yValues.push(null)
        lastWasValid = false
      }
    }
  }
  
  console.log(`Points générés: ${xValues.length}`)
  if (xValues.length > 0) {
    console.log('Premiers points:', xValues.slice(0, 5), yValues.slice(0, 5))
    console.log('Derniers points:', xValues.slice(-5), yValues.slice(-5))
  } else {
    console.warn('⚠️ Aucun point valide généré pour:', latexExpression)
  }
  
  return { x: xValues, y: yValues, jsExpression }
}

/**
 * Dérivée numérique
 * @param {Function} jsFunc - Fonction JavaScript
 * @param {number} x0 - Point de dérivation
 * @param {number} h - Pas
 * @returns {number}
 */
export function numericalDerivative(jsFunc, x0, h = 0.0001) {
  const y1 = jsFunc(x0 + h)
  const y2 = jsFunc(x0 - h)
  return (y1 - y2) / (2 * h)
}

/**
 * Intégrale numérique par méthode de Simpson
 * @param {Function} jsFunc - Fonction JavaScript
 * @param {number} a - Borne inférieure
 * @param {number} b - Borne supérieure
 * @param {number} n - Nombre de subdivisions
 * @returns {number}
 */
export function numericalIntegral(jsFunc, a, b, n = 1000) {
  const h = (b - a) / n
  let sum = jsFunc(a) + jsFunc(b)
  
  for (let i = 1; i < n; i++) {
    const x = a + i * h
    const y = jsFunc(x)
    if (isFinite(y)) {
      sum += (i % 2 === 0) ? 2 * y : 4 * y
    }
  }
  
  return (h / 3) * sum
}

/**
 * Méthode de bisection pour trouver un zéro
 * @param {Function} func - Fonction
 * @param {number} a - Borne gauche
 * @param {number} b - Borne droite
 * @param {number} tolerance - Tolérance
 * @param {number} maxIter - Iterations max
 * @returns {number|null}
 */
export function findZero(func, a, b, tolerance = 0.001, maxIter = 50) {
  let fa = func(a)
  let fb = func(b)
  
  if (!isFinite(fa) || !isFinite(fb)) return null
  if (fa * fb > 0) return null
  
  for (let i = 0; i < maxIter; i++) {
    const mid = (a + b) / 2
    const fmid = func(mid)
    
    if (!isFinite(fmid)) return null
    if (Math.abs(fmid) < tolerance || (b - a) / 2 < tolerance) {
      return mid
    }
    
    if (fa * fmid < 0) {
      b = mid
      fb = fmid
    } else {
      a = mid
      fa = fmid
    }
  }
  
  return (a + b) / 2
}

/**
 * Méthode de bisection pour trouver l'intersection de deux fonctions
 */
export function bisectionMethod(js1, js2, a, b, tolerance = 0.001, maxIter = 50) {
  const diff = (x) => js1(x) - js2(x)
  return findZero(diff, a, b, tolerance, maxIter)
}
