/**
 * Composable pour l'analyse graphique (intersections, racines, tangentes, aires)
 */
import { ref } from 'vue'
import { convertLatexToJS, evaluateFunction, findZero, bisectionMethod, numericalIntegral, numericalDerivative } from './mathUtils'
import { SPECIAL_COLORS } from './graphConfig'

export function useGraphAnalysis(graphFunctions, xMin, xMax, yMin, yMax) {
  // Intersections entre courbes
  const showIntersections = ref(false)
  const intersectionPoints = ref([])
  const hiddenIntersections = ref([])
  const intersectionRefs = ref([])
  
  // Noms personnalisés persistants pour les intersections (clé = coordonnées arrondies)
  const intersectionCustomNames = ref({})
  const axisIntersectionCustomNames = ref({})
  
  // Intersections avec les axes
  const showAxisIntersections = ref(false)
  const axisIntersectionPoints = ref([])
  const hiddenAxisIntersections = ref([])
  
  // Asymptotes
  const verticalAsymptotes = ref('')
  const horizontalAsymptotes = ref('')
  
  // Intégrale graphique
  const showIntegralArea = ref(false)
  const integralA = ref(0)
  const integralB = ref(1)
  const integralFunc1Index = ref(0)
  const integralFunc2Index = ref(-1)
  const integralResult = ref(null)
  
  // Aire entre courbes
  const showAreaBetweenCurves = ref(false)
  const areaCurve1Index = ref(0)
  const areaCurve2Index = ref(1)
  const areaA = ref(null)
  const areaB = ref(null)
  const areaBetweenResult = ref(null)
  
  // Tangente
  const showTangent = ref(false)
  const tangentFuncIndex = ref(0)
  const tangentX = ref(0)
  const tangentEquation = ref('')
  
  // Racines
  const showRoots = ref(false)
  const rootsPoints = ref([])

  const MAX_FUNCTION_NAME_LENGTH = 10

  function sanitizeFunctionName(value) {
    const raw = (value ?? '').toString().trim()
    if (!raw) return ''

    let cleaned = raw.replace(/[^a-zA-Z0-9]/g, '')
    cleaned = cleaned.replace(/^[0-9]+/, '')
    cleaned = cleaned.slice(0, MAX_FUNCTION_NAME_LENGTH)

    if (!cleaned || !/^[a-zA-Z]/.test(cleaned)) return ''
    return cleaned
  }

  function getFunctionDisplayName(func, index) {
    const custom = sanitizeFunctionName(func?.name)
    return custom || `f${index + 1}`
  }

  // Génère une clé unique pour un point d'intersection
  function getIntersectionKey(func1Index, func2Index, x, y) {
    return `${func1Index}-${func2Index}-${x.toFixed(3)}-${y.toFixed(3)}`
  }

  function getAxisIntersectionKey(funcIndex, axis, x, y) {
    return `${funcIndex}-${axis}-${x.toFixed(3)}-${y.toFixed(3)}`
  }

  // === ASYMPTOTES ===
  function addManualAsymptotes(traces) {
    // Asymptotes verticales
    if (verticalAsymptotes.value.trim()) {
      const values = verticalAsymptotes.value.split(',').map(v => parseFloat(v.trim())).filter(v => !isNaN(v))
      values.forEach(x => {
        traces.push({
          x: [x, x],
          y: [yMin.value, yMax.value],
          type: 'scatter',
          mode: 'lines',
          line: { color: SPECIAL_COLORS.asymptote, width: 2, dash: 'dash' },
          name: `x = ${x}`,
          showlegend: true,
          hovertemplate: `<b>Asymptote verticale</b><br>x = ${x}<extra></extra>`
        })
      })
    }
    
    // Asymptotes horizontales
    if (horizontalAsymptotes.value.trim()) {
      const values = horizontalAsymptotes.value.split(',').map(v => parseFloat(v.trim())).filter(v => !isNaN(v))
      values.forEach(y => {
        traces.push({
          x: [xMin.value, xMax.value],
          y: [y, y],
          type: 'scatter',
          mode: 'lines',
          line: { color: SPECIAL_COLORS.asymptote, width: 2, dash: 'dash' },
          name: `y = ${y}`,
          showlegend: true,
          hovertemplate: `<b>Asymptote horizontale</b><br>y = ${y}<extra></extra>`
        })
      })
    }
  }

  // === INTERSECTIONS ENTRE COURBES ===
  function findIntersections(func1, func2) {
    const intersections = []
    
    // Cas: Intersection entre droite verticale (x=a) et fonction normale
    if (func1.type === 'vertical' && func2.type === 'function') {
      const x = func1.value
      const js = convertLatexToJS(func2.latex)
      const y = evaluateFunction(js, x)
      if (isFinite(y) && y >= yMin.value && y <= yMax.value) {
        intersections.push({ x, y })
      }
    }
    
    if (func1.type === 'function' && func2.type === 'vertical') {
      const x = func2.value
      const js = convertLatexToJS(func1.latex)
      const y = evaluateFunction(js, x)
      if (isFinite(y) && y >= yMin.value && y <= yMax.value) {
        intersections.push({ x, y })
      }
    }
    
    // Cas: Intersection entre droite horizontale et fonction
    if (func1.type === 'horizontal' && func2.type === 'function') {
      const yTarget = func1.value
      const js = convertLatexToJS(func2.latex)
      findHorizontalIntersections(js, yTarget, xMin.value, xMax.value, intersections)
    }
    
    if (func1.type === 'function' && func2.type === 'horizontal') {
      const yTarget = func2.value
      const js = convertLatexToJS(func1.latex)
      findHorizontalIntersections(js, yTarget, xMin.value, xMax.value, intersections)
    }
    
    // Cas: Intersection entre droite verticale et horizontale
    if (func1.type === 'vertical' && func2.type === 'horizontal') {
      intersections.push({ x: func1.value, y: func2.value })
    }
    if (func1.type === 'horizontal' && func2.type === 'vertical') {
      intersections.push({ x: func2.value, y: func1.value })
    }
    
    // Cas: Intersection entre deux fonctions normales
    if (func1.type === 'function' && func2.type === 'function') {
      const js1 = convertLatexToJS(func1.latex)
      const js2 = convertLatexToJS(func2.latex)
      findFunctionIntersections(js1, js2, xMin.value, xMax.value, intersections)
    }
    
    return intersections
  }
  
  function findHorizontalIntersections(js, yTarget, xStart, xEnd, intersections) {
    const numSamples = 1000
    const step = (xEnd - xStart) / numSamples
    
    for (let i = 0; i < numSamples; i++) {
      const x1 = xStart + i * step
      const x2 = xStart + (i + 1) * step
      const y1 = evaluateFunction(js, x1)
      const y2 = evaluateFunction(js, x2)
      
      if (isFinite(y1) && isFinite(y2)) {
        const diff1 = y1 - yTarget
        const diff2 = y2 - yTarget
        
        if (diff1 * diff2 <= 0 && Math.abs(diff1) < 100 && Math.abs(diff2) < 100) {
          const xIntersect = findZeroForHorizontal(js, yTarget, x1, x2)
          if (xIntersect !== null) {
            const isDuplicate = intersections.some(p => Math.abs(p.x - xIntersect) < 0.1)
            if (!isDuplicate) {
              intersections.push({ x: xIntersect, y: yTarget })
            }
          }
        }
      }
    }
  }
  
  function findZeroForHorizontal(jsFunc, yTarget, a, b, tolerance = 0.001, maxIter = 50) {
    const func = (x) => evaluateFunction(jsFunc, x) - yTarget
    return findZero(func, a, b, tolerance, maxIter)
  }
  
  function findFunctionIntersections(js1, js2, xStart, xEnd, intersections) {
    const numSamples = 1000
    const step = (xEnd - xStart) / numSamples
    
    for (let i = 0; i < numSamples; i++) {
      const x1 = xStart + i * step
      const x2 = xStart + (i + 1) * step
      
      const y1_f1 = evaluateFunction(js1, x1)
      const y2_f1 = evaluateFunction(js1, x2)
      const y1_f2 = evaluateFunction(js2, x1)
      const y2_f2 = evaluateFunction(js2, x2)
      
      if (isFinite(y1_f1) && isFinite(y2_f1) && isFinite(y1_f2) && isFinite(y2_f2)) {
        const diff1 = y1_f1 - y1_f2
        const diff2 = y2_f1 - y2_f2
        
        if (diff1 * diff2 <= 0 && Math.abs(diff1) < 100 && Math.abs(diff2) < 100) {
          const jsFunc1 = (x) => evaluateFunction(js1, x)
          const jsFunc2 = (x) => evaluateFunction(js2, x)
          const xIntersect = bisectionMethod(jsFunc1, jsFunc2, x1, x2)
          
          if (xIntersect !== null) {
            const yIntersect = evaluateFunction(js1, xIntersect)
            const isDuplicate = intersections.some(p => 
              Math.abs(p.x - xIntersect) < 0.1 && Math.abs(p.y - yIntersect) < 0.1
            )
            if (!isDuplicate && isFinite(yIntersect)) {
              intersections.push({ x: xIntersect, y: yIntersect })
            }
          }
        }
      }
    }
  }

  function calculateIntersections(traces) {
    intersectionPoints.value = []
    
    for (let i = 0; i < graphFunctions.value.length; i++) {
      for (let j = i + 1; j < graphFunctions.value.length; j++) {
        const func1 = graphFunctions.value[i]
        const func2 = graphFunctions.value[j]
        const intersections = findIntersections(func1, func2)
        
        intersections.forEach(point => {
          const isHidden = hiddenIntersections.value.some(hidden => 
            hidden.func1Index === i + 1 && 
            hidden.func2Index === j + 1 && 
            Math.abs(hidden.x - point.x) < 0.01 && 
            Math.abs(hidden.y - point.y) < 0.01
          )
          
          if (!isHidden) {
            const key = getIntersectionKey(i + 1, j + 1, point.x, point.y)
            const customName = intersectionCustomNames.value[key] || ''
            const xCoord = Math.abs(point.x) < 0.01 ? 0 : Number(point.x.toFixed(2))
            const yCoord = Math.abs(point.y) < 0.01 ? 0 : Number(point.y.toFixed(2))
            const name1 = getFunctionDisplayName(func1, i)
            const name2 = getFunctionDisplayName(func2, j)
            const defaultName = `${name1} ∩ ${name2}`
            
            intersectionPoints.value.push({
              x: point.x,
              y: point.y,
              func1: func1.expression,
              func2: func2.expression,
              func1Index: i + 1,
              func2Index: j + 1,
              color1: func1.color,
              color2: func2.color,
              name: customName || defaultName,
              key: key,
              defaultName: defaultName
            })
            
            const displayName = customName || defaultName
            
            traces.push({
              x: [point.x],
              y: [point.y],
              type: 'scatter',
              mode: 'markers+text',
              name: `${displayName}: (${xCoord}, ${yCoord})`,
              text: [customName || ''],
              textposition: 'top right',
              textfont: {
                size: 11,
                color: SPECIAL_COLORS.intersection
              },
              marker: {
                color: SPECIAL_COLORS.intersection,
                size: 10,
                symbol: 'circle',
                line: { color: 'white', width: 2 }
              },
              showlegend: true,
              legendgroup: 'intersections',
              hovertemplate: `<b>${displayName}</b><br>(${point.x.toFixed(3)}, ${point.y.toFixed(3)})<extra></extra>`
            })
          }
        })
      }
    }
  }

  // === INTERSECTIONS AVEC LES AXES ===
  function calculateAxisIntersections(traces) {
    axisIntersectionPoints.value = []
    
    graphFunctions.value.forEach((func, funcIndex) => {
      if (func.type !== 'function') return
      
      const js = convertLatexToJS(func.latex)
      
      // Intersection avec l'axe X (y = 0)
      const xIntersections = findAxisIntersections(js, 'x')
      xIntersections.forEach(x => {
        const isHidden = hiddenAxisIntersections.value.some(h => 
          h.funcIndex === funcIndex + 1 && h.axis === 'x' && Math.abs(h.value - x) < 0.01
        )
        
        if (!isHidden) {
          const xCoord = Math.abs(x) < 0.01 ? 0 : Number(x.toFixed(3))
          const axisKey = getAxisIntersectionKey(funcIndex + 1, 'x', x, 0)
          const axisCustomName = axisIntersectionCustomNames.value[axisKey] || ''
          const defaultAxisName = `${getFunctionDisplayName(func, funcIndex)} ∩ Ox`
          
          axisIntersectionPoints.value.push({
            x: x,
            y: 0,
            funcIndex: funcIndex + 1,
            axis: 'x',
            expression: func.expression,
            name: axisCustomName || defaultAxisName,
            key: axisKey,
            defaultName: defaultAxisName
          })
          
          const axisDisplayName = axisCustomName || defaultAxisName
          
          traces.push({
            x: [x],
            y: [0],
            type: 'scatter',
            mode: 'markers',
            name: `${axisDisplayName}: (${xCoord}, 0)`,
            marker: {
              color: SPECIAL_COLORS.axisIntersection,
              size: 8,
              symbol: 'circle',
              line: { color: 'white', width: 2 }
            },
            showlegend: true,
            legendgroup: 'axisIntersections'
          })
        }
      })
      
      // Intersection avec l'axe Y (x = 0)
      const yValue = evaluateFunction(js, 0)
      if (isFinite(yValue) && yValue >= yMin.value && yValue <= yMax.value) {
        const isHidden = hiddenAxisIntersections.value.some(h => 
          h.funcIndex === funcIndex + 1 && h.axis === 'y'
        )
        
        if (!isHidden) {
          const yCoord = Math.abs(yValue) < 0.01 ? 0 : Number(yValue.toFixed(3))
          const axisKeyY = getAxisIntersectionKey(funcIndex + 1, 'y', 0, yValue)
          const axisCustomNameY = axisIntersectionCustomNames.value[axisKeyY] || ''
          const defaultAxisNameY = `${getFunctionDisplayName(func, funcIndex)} ∩ Oy`
          
          axisIntersectionPoints.value.push({
            x: 0,
            y: yValue,
            funcIndex: funcIndex + 1,
            axis: 'y',
            expression: func.expression,
            name: axisCustomNameY || defaultAxisNameY,
            key: axisKeyY,
            defaultName: defaultAxisNameY
          })
          
          const axisDisplayNameY = axisCustomNameY || defaultAxisNameY
          
          traces.push({
            x: [0],
            y: [yValue],
            type: 'scatter',
            mode: 'markers',
            name: `${axisDisplayNameY}: (0, ${yCoord})`,
            marker: {
              color: SPECIAL_COLORS.axisIntersection,
              size: 8,
              symbol: 'diamond',
              line: { color: 'white', width: 2 }
            },
            showlegend: true,
            legendgroup: 'axisIntersections'
          })
        }
      }
    })
  }

  function findAxisIntersections(jsFunc, axis) {
    const intersections = []
    const numSamples = 1000
    const step = (xMax.value - xMin.value) / numSamples
    
    for (let i = 0; i < numSamples; i++) {
      const x1 = xMin.value + i * step
      const x2 = xMin.value + (i + 1) * step
      const y1 = evaluateFunction(jsFunc, x1)
      const y2 = evaluateFunction(jsFunc, x2)
      
      if (isFinite(y1) && isFinite(y2) && y1 * y2 <= 0 && Math.abs(y1) < 1000 && Math.abs(y2) < 1000) {
        const func = (x) => evaluateFunction(jsFunc, x)
        const root = findZero(func, x1, x2)
        if (root !== null) {
          const isDuplicate = intersections.some(r => Math.abs(r - root) < 0.1)
          if (!isDuplicate) intersections.push(root)
        }
      }
    }
    
    return intersections
  }

  // === RACINES ===
  function calculateRoots(traces) {
    rootsPoints.value = []
    
    graphFunctions.value.forEach((func, funcIndex) => {
      if (func.type !== 'function') return
      
      const js = convertLatexToJS(func.latex)
      const roots = findRoots(js)
      
      roots.forEach(root => {
        rootsPoints.value.push({
          x: root,
          funcIndex: funcIndex + 1,
          expression: func.expression
        })
        
        traces.push({
          x: [root],
          y: [0],
          type: 'scatter',
          mode: 'markers',
          name: `Racine ${getFunctionDisplayName(func, funcIndex)}: x = ${root.toFixed(3)}`,
          marker: {
            color: '#f97316',
            size: 10,
            symbol: 'x',
            line: { width: 2 }
          },
          showlegend: true
        })
      })
    })
  }

  function findRoots(jsFunc) {
    return findAxisIntersections(jsFunc, 'x')
  }

  // === TANGENTE ===
  function addTangentToGraph(traces) {
    const funcIndex = tangentFuncIndex.value
    if (funcIndex < 0 || funcIndex >= graphFunctions.value.length) return
    
    const func = graphFunctions.value[funcIndex]
    if (func.type !== 'function') return
    
    const js = convertLatexToJS(func.latex)
    const x0 = tangentX.value
    const y0 = evaluateFunction(js, x0)
    
    if (!isFinite(y0)) return
    
    const jsFunc = (x) => evaluateFunction(js, x)
    const slope = numericalDerivative(jsFunc, x0)
    
    if (!isFinite(slope)) return
    
    // y = slope * (x - x0) + y0
    const tangentFunc = (x) => slope * (x - x0) + y0
    const xVals = [xMin.value, xMax.value]
    const yVals = xVals.map(tangentFunc)
    
    tangentEquation.value = `y = ${slope.toFixed(3)}(x - ${x0}) + ${y0.toFixed(3)}`
    
    traces.push({
      x: xVals,
      y: yVals,
      type: 'scatter',
      mode: 'lines',
      line: { color: SPECIAL_COLORS.tangent, width: 2, dash: 'dot' },
      name: `Tangente en x=${x0}`,
      showlegend: true
    })
    
    // Point de tangence
    traces.push({
      x: [x0],
      y: [y0],
      type: 'scatter',
      mode: 'markers',
      marker: {
        color: SPECIAL_COLORS.tangent,
        size: 8,
        symbol: 'circle'
      },
      showlegend: false
    })
  }

  // === INTÉGRALE GRAPHIQUE ===
  function addIntegralAreaToGraph(traces) {
    const funcIndex = integralFunc1Index.value
    if (funcIndex < 0 || funcIndex >= graphFunctions.value.length) return
    
    const func = graphFunctions.value[funcIndex]
    if (func.type !== 'function') return
    
    const js = convertLatexToJS(func.latex)
    const a = integralA.value
    const b = integralB.value
    
    if (a >= b) return
    
    const numPoints = 200
    const step = (b - a) / numPoints
    const xValues = [a]
    const yValues = [0]
    
    for (let i = 0; i <= numPoints; i++) {
      const x = a + i * step
      const y = evaluateFunction(js, x)
      xValues.push(x)
      yValues.push(isFinite(y) ? y : 0)
    }
    
    xValues.push(b)
    yValues.push(0)
    
    traces.push({
      x: xValues,
      y: yValues,
      type: 'scatter',
      mode: 'lines',
      fill: 'toself',
      fillcolor: SPECIAL_COLORS.integralArea,
      line: { color: 'transparent' },
      name: `∫[${a},${b}] ${getFunctionDisplayName(func, funcIndex)}(x)dx`,
      showlegend: true
    })
  }

  function calculateIntegralArea() {
    const funcIndex = integralFunc1Index.value
    if (funcIndex < 0 || funcIndex >= graphFunctions.value.length) return
    
    const func = graphFunctions.value[funcIndex]
    if (func.type !== 'function') return
    
    const js = convertLatexToJS(func.latex)
    const jsFunc = (x) => evaluateFunction(js, x)
    const result = numericalIntegral(jsFunc, integralA.value, integralB.value)
    
    integralResult.value = result
  }

  // === AIRE ENTRE COURBES ===
  function addAreaBetweenCurvesToGraph(traces) {
    const idx1 = areaCurve1Index.value
    const idx2 = areaCurve2Index.value
    
    if (idx1 === idx2 || idx1 >= graphFunctions.value.length || idx2 >= graphFunctions.value.length) return
    
    const func1 = graphFunctions.value[idx1]
    const func2 = graphFunctions.value[idx2]
    
    if (func1.type !== 'function' || func2.type !== 'function') return
    
    const js1 = convertLatexToJS(func1.latex)
    const js2 = convertLatexToJS(func2.latex)
    
    let a = areaA.value
    let b = areaB.value
    
    if ((a === null || a === '') && (b === null || b === '')) {
      const ints = findIntersectionPointsNumeric(js1, js2, xMin.value, xMax.value)
      if (ints.length >= 2) {
        a = ints[0]
        b = ints[1]
      } else {
        a = xMin.value
        b = xMax.value
      }
    } else {
      a = Number(a) || xMin.value
      b = Number(b) || xMax.value
    }
    
    if (a >= b) return
    
    const numPoints = 200
    const step = (b - a) / numPoints
    const xValues = []
    const y1Values = []
    const y2Values = []
    
    for (let i = 0; i <= numPoints; i++) {
      const x = a + i * step
      xValues.push(x)
      y1Values.push(evaluateFunction(js1, x) || 0)
      y2Values.push(evaluateFunction(js2, x) || 0)
    }
    
    traces.push({
      x: xValues,
      y: y2Values,
      type: 'scatter',
      mode: 'lines',
      line: { width: 0 },
      showlegend: false
    })
    
    traces.push({
      x: xValues,
      y: y1Values,
      fill: 'tonexty',
      type: 'scatter',
      mode: 'lines',
      line: { width: 0 },
      fillcolor: SPECIAL_COLORS.areaBetweenCurves,
      name: 'Aire entre courbes',
      showlegend: true
    })
  }

  function findIntersectionPointsNumeric(js1, js2, xStart, xEnd) {
    const intersections = []
    const step = (xEnd - xStart) / 1000
    
    for (let x = xStart; x < xEnd; x += step) {
      const y1 = evaluateFunction(js1, x)
      const y2 = evaluateFunction(js2, x)
      const y1Next = evaluateFunction(js1, x + step)
      const y2Next = evaluateFunction(js2, x + step)
      
      if (isFinite(y1) && isFinite(y2) && isFinite(y1Next) && isFinite(y2Next)) {
        if ((y1 - y2) * (y1Next - y2Next) < 0) {
          intersections.push(x + step / 2)
        }
      }
    }
    
    return intersections
  }

  function calculateAreaBetweenCurves() {
    const idx1 = areaCurve1Index.value
    const idx2 = areaCurve2Index.value
    
    if (idx1 === idx2 || idx1 >= graphFunctions.value.length || idx2 >= graphFunctions.value.length) return
    
    const func1 = graphFunctions.value[idx1]
    const func2 = graphFunctions.value[idx2]
    
    if (func1.type !== 'function' || func2.type !== 'function') return
    
    const js1 = convertLatexToJS(func1.latex)
    const js2 = convertLatexToJS(func2.latex)
    
    let a = Number(areaA.value) || xMin.value
    let b = Number(areaB.value) || xMax.value
    
    const diffFunc = (x) => Math.abs(evaluateFunction(js1, x) - evaluateFunction(js2, x))
    const result = numericalIntegral(diffFunc, a, b)
    
    areaBetweenResult.value = result
  }

  // === UTILITAIRES ===
  function removeIntersection(index) {
    const point = intersectionPoints.value[index]
    if (point) {
      hiddenIntersections.value.push({
        func1Index: point.func1Index,
        func2Index: point.func2Index,
        x: point.x,
        y: point.y
      })
    }
  }

  function removeAxisIntersection(index) {
    const point = axisIntersectionPoints.value[index]
    if (point) {
      hiddenAxisIntersections.value.push({
        funcIndex: point.funcIndex,
        axis: point.axis,
        value: point.axis === 'x' ? point.x : point.y
      })
    }
  }

  // Renommer un point d'intersection
  function renameIntersection(index, newName) {
    const point = intersectionPoints.value[index]
    if (point) {
      point.name = newName || point.defaultName
      if (newName && newName !== point.defaultName) {
        intersectionCustomNames.value[point.key] = newName
      } else {
        delete intersectionCustomNames.value[point.key]
      }
    }
  }

  function renameAxisIntersection(index, newName) {
    const point = axisIntersectionPoints.value[index]
    if (point) {
      point.name = newName || point.defaultName
      if (newName && newName !== point.defaultName) {
        axisIntersectionCustomNames.value[point.key] = newName
      } else {
        delete axisIntersectionCustomNames.value[point.key]
      }
    }
  }

  function clearAnalysis() {
    intersectionPoints.value = []
    axisIntersectionPoints.value = []
    hiddenIntersections.value = []
    hiddenAxisIntersections.value = []
    intersectionCustomNames.value = {}
    axisIntersectionCustomNames.value = {}
    rootsPoints.value = []
    integralResult.value = null
    areaBetweenResult.value = null
    tangentEquation.value = ''
  }

  return {
    // Intersections
    showIntersections,
    intersectionPoints,
    hiddenIntersections,
    intersectionRefs,
    calculateIntersections,
    removeIntersection,
    renameIntersection,
    
    // Axes
    showAxisIntersections,
    axisIntersectionPoints,
    hiddenAxisIntersections,
    calculateAxisIntersections,
    removeAxisIntersection,
    renameAxisIntersection,
    
    // Asymptotes
    verticalAsymptotes,
    horizontalAsymptotes,
    addManualAsymptotes,
    
    // Intégrale
    showIntegralArea,
    integralA,
    integralB,
    integralFunc1Index,
    integralFunc2Index,
    integralResult,
    addIntegralAreaToGraph,
    calculateIntegralArea,
    
    // Aire entre courbes
    showAreaBetweenCurves,
    areaCurve1Index,
    areaCurve2Index,
    areaA,
    areaB,
    areaBetweenResult,
    addAreaBetweenCurvesToGraph,
    calculateAreaBetweenCurves,
    
    // Tangente
    showTangent,
    tangentFuncIndex,
    tangentX,
    tangentEquation,
    addTangentToGraph,
    
    // Racines
    showRoots,
    rootsPoints,
    calculateRoots,
    
    // Utilitaires
    clearAnalysis
  }
}
