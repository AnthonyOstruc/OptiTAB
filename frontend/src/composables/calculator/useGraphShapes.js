/**
 * Composable pour la gestion des formes géométriques (points, segments, cercles)
 */
import { ref } from 'vue'
import { GRAPH_COLORS } from './graphConfig'
import { convertLatexToJS } from './mathUtils'

export function useGraphShapes() {
  // État des formes
  const points = ref([])
  const segments = ref([])
  const circles = ref([])
  
  // Champs de saisie pour les points
  const pointX = ref('0')
  const pointY = ref('0')
  const pointName = ref('')
  const pointsInput = ref('')
  
  // Compteur pour auto-nommage des points
  let pointAutoIndex = 0
  
  // Champs de saisie pour les segments
  const segmentX1 = ref(0)
  const segmentY1 = ref(0)
  const segmentX2 = ref(1)
  const segmentY2 = ref(1)
  const segmentIsVector = ref(false)
  const segmentName = ref('')
  
  // Compteur pour auto-nommage des segments
  let segmentAutoIndex = 0
  
  // Champs de saisie pour les cercles
  const circleH = ref(0)
  const circleK = ref(0)
  const circleR = ref(1)
  const circleName = ref('')
  
  // Compteur pour auto-nommage des cercles
  let circleAutoIndex = 0
  
  // Compteur pour les couleurs
  let colorIndex = 0
  
  function getNextColor() {
    const color = GRAPH_COLORS[colorIndex % GRAPH_COLORS.length]
    colorIndex++
    return color
  }
  
  function resetColorIndex() {
    colorIndex = 0
  }

  function parseCoordinateValue(rawValue) {
    if (typeof rawValue === 'number') {
      return Number.isFinite(rawValue) ? rawValue : NaN
    }

    const raw = String(rawValue ?? '').trim()
    if (!raw) return NaN

    // Accepter la notation usuelle: e, pi, π, 2e, e^2, 3/2...
    let normalized = raw
      .replace(',', '.')
      .replace(/π/g, 'pi')
      .replace(/\bpi\b/gi, 'Math.PI')

    const jsExpr = convertLatexToJS(normalized).replace(/\s+/g, '')
    if (!jsExpr || /\bx\b/i.test(jsExpr)) return NaN

    try {
      const value = Function(`"use strict"; return (${jsExpr});`)()
      return (typeof value === 'number' && Number.isFinite(value)) ? value : NaN
    } catch {
      return NaN
    }
  }
  
  // === POINTS ===
  function addPoint(onUpdate) {
    const xValue = parseCoordinateValue(pointX.value)
    const yValue = parseCoordinateValue(pointY.value)
    if (!Number.isFinite(xValue) || !Number.isFinite(yValue)) {
      alert('Coordonnées invalides. Exemple: x = e, y = 1')
      return
    }

    const color = getNextColor()
    pointAutoIndex++
    const name = pointName.value.trim() || `P${pointAutoIndex}`
    points.value.push({
      x: xValue,
      y: yValue,
      color: color,
      name: name,
      showName: true,
      showCoords: true,
      showInLegend: true
    })
    
    // Réinitialiser les champs
    pointX.value = '0'
    pointY.value = '0'
    pointName.value = ''
    
    if (onUpdate) onUpdate()
  }
  
  function addMultiplePoints(onUpdate) {
    const input = pointsInput.value.trim()
    if (!input) return
    
    // Regex pour matcher A(1,2), A(e,1), A(2e,pi/2), etc.
    const pointRegex = /([A-Za-zÀ-ÿ_]\w*)\s*\(\s*([A-Za-z0-9π\\.+\-*/^]+)\s*[,;]\s*([A-Za-z0-9π\\.+\-*/^]+)\s*\)/g
    let match
    let count = 0
    
    while ((match = pointRegex.exec(input)) !== null) {
      const name = match[1]
      const x = parseCoordinateValue(match[2])
      const y = parseCoordinateValue(match[3])
      if (!Number.isFinite(x) || !Number.isFinite(y)) {
        alert(`Coordonnées invalides pour ${name}. Exemple valide: ${name}(e,1)`)
        return
      }
      const color = getNextColor()
      pointAutoIndex++
      
      points.value.push({
        x: x,
        y: y,
        color: color,
        name: name,
        showName: true,
        showCoords: true,
        showInLegend: true
      })
      count++
    }
    
    if (count > 0) {
      pointsInput.value = ''
      if (onUpdate) onUpdate()
    }
  }
  
  function getPointDisplayName(index) {
    const point = points.value[index]
    return point ? point.name : `P${index + 1}`
  }
  
  function removePoint(index, onUpdate) {
    points.value.splice(index, 1)
    if (onUpdate) onUpdate()
  }
  
  function drawPoints(traces) {
    points.value.forEach((point, index) => {
      const displayName = point.name || `P${index + 1}`
      traces.push({
        x: [point.x],
        y: [point.y],
        type: 'scatter',
        mode: 'markers',
        marker: {
          color: point.color,
          size: 10,
          symbol: 'circle',
          line: {
            color: 'white',
            width: 2
          }
        },
        name: `${displayName} (${point.x}, ${point.y})`,
        showlegend: point.showInLegend !== false,
        hovertemplate: `<b>${displayName}</b><br>(${point.x}, ${point.y})<extra></extra>`
      })
    })
  }
  
  // === SEGMENTS ===
  function addSegment(onUpdate) {
    const color = getNextColor()
    segmentAutoIndex++
    const isVec = segmentIsVector.value
    const defaultPrefix = isVec ? 'V' : 'S'
    const name = segmentName.value.trim() || `${defaultPrefix}${segmentAutoIndex}`
    segments.value.push({
      x1: segmentX1.value,
      y1: segmentY1.value,
      x2: segmentX2.value,
      y2: segmentY2.value,
      color: color,
      isVector: isVec,
      name: name,
      showName: false,
      showCoords: false,
      showInLegend: true,
      lineDash: 'solid',
      lineWidth: 3
    })
    
    // Réinitialiser les champs
    segmentX1.value = 0
    segmentY1.value = 0
    segmentX2.value = 1
    segmentY2.value = 1
    segmentName.value = ''
    
    if (onUpdate) onUpdate()
  }
  
  function removeSegment(index, onUpdate) {
    segments.value.splice(index, 1)
    if (onUpdate) onUpdate()
  }
  
  function drawSegments(traces) {
    segments.value.forEach((segment, index) => {
      const label = segment.name || (segment.isVector ? `V${index + 1}` : `S${index + 1}`)
      const notation = segment.isVector ? `→` : `[AB]`
      // Dessiner le segment/vecteur
      traces.push({
        x: [segment.x1, segment.x2],
        y: [segment.y1, segment.y2],
        type: 'scatter',
        mode: 'lines',
        line: {
          color: segment.color,
          width: segment.lineWidth || 3,
          dash: segment.lineDash || 'solid'
        },
        name: `${label}: ${notation}`,
        showlegend: segment.showInLegend !== false,
        hovertemplate: `<b>${label}</b><br>De (${segment.x1}, ${segment.y1}) à (${segment.x2}, ${segment.y2})<extra></extra>`
      })
      
      // Ajouter les points d'extrémité
      traces.push({
        x: [segment.x1, segment.x2],
        y: [segment.y1, segment.y2],
        type: 'scatter',
        mode: 'markers',
        marker: {
          color: segment.color,
          size: 8,
          symbol: 'circle',
          line: {
            color: 'white',
            width: 2
          }
        },
        showlegend: false,
        hovertemplate: `<b>Extrémité</b><br>(%{x}, %{y})<extra></extra>`
      })
    })
  }
  
  // Génère les annotations flèches pour les vecteurs
  function getVectorAnnotations() {
    const annotations = []
    segments.value.forEach((segment) => {
      if (!segment.isVector) return
      annotations.push({
        x: segment.x2,
        y: segment.y2,
        xref: 'x',
        yref: 'y',
        text: '',
        showarrow: true,
        axref: 'x',
        ayref: 'y',
        ax: segment.x1,
        ay: segment.y1,
        arrowhead: 2,
        arrowsize: 1,
        arrowwidth: 2.5,
        arrowcolor: segment.color
      })
    })
    return annotations
  }
  
  // === CERCLES ===
  function addCircle(onUpdate) {
    if (circleR.value <= 0) {
      alert('Le rayon doit être supérieur à 0')
      return
    }
    
    const color = getNextColor()
    circleAutoIndex++
    const name = circleName.value.trim() || `C${circleAutoIndex}`
    circles.value.push({
      h: circleH.value,
      k: circleK.value,
      r: circleR.value,
      color: color,
      name: name,
      showName: true,
      showInLegend: true,
      lineDash: 'solid',
      lineWidth: 2
    })
    
    // Réinitialiser les champs
    circleH.value = 0
    circleK.value = 0
    circleR.value = 1
    circleName.value = ''
    
    if (onUpdate) onUpdate()
  }
  
  function removeCircle(index, onUpdate) {
    circles.value.splice(index, 1)
    if (onUpdate) onUpdate()
  }
  
  function drawCircles(traces) {
    circles.value.forEach((circle, index) => {
      const numPoints = 200
      const xValues = []
      const yValues = []
      
      // Générer les points du cercle : (x-h)² + (y-k)² = r²
      for (let i = 0; i <= numPoints; i++) {
        const theta = (2 * Math.PI * i) / numPoints
        const x = circle.h + circle.r * Math.cos(theta)
        const y = circle.k + circle.r * Math.sin(theta)
        xValues.push(x)
        yValues.push(y)
      }
      
      traces.push({
        x: xValues,
        y: yValues,
        type: 'scatter',
        mode: 'lines',
        line: {
          color: circle.color,
          width: circle.lineWidth || 2,
          dash: circle.lineDash || 'solid'
        },
        name: `${circle.name || 'C' + (index + 1)}: centre(${circle.h}, ${circle.k}), r=${circle.r}`,
        showlegend: circle.showInLegend !== false,
        hovertemplate: `<b>${circle.name || 'C' + (index + 1)}</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>`
      })
      
      // Ajouter un point au centre du cercle
      traces.push({
        x: [circle.h],
        y: [circle.k],
        type: 'scatter',
        mode: 'markers',
        marker: {
          color: circle.color,
          size: 6,
          symbol: 'circle'
        },
        name: `Centre (${circle.h}, ${circle.k})`,
        showlegend: false,
        hovertemplate: `<b>Centre de ${circle.name || 'C' + (index + 1)}</b><br>(${circle.h}, ${circle.k})<extra></extra>`
      })
    })
  }
  
  // === UTILITAIRES ===
  function clearAllShapes() {
    points.value = []
    segments.value = []
    circles.value = []
    pointAutoIndex = 0
    segmentAutoIndex = 0
    circleAutoIndex = 0
  }
  
  function hasShapes() {
    return points.value.length > 0 || segments.value.length > 0 || circles.value.length > 0
  }
  
  function drawAllShapes(traces) {
    if (points.value.length > 0) drawPoints(traces)
    if (segments.value.length > 0) drawSegments(traces)
    if (circles.value.length > 0) drawCircles(traces)
  }
  
  return {
    // État
    points,
    segments,
    circles,
    
    // Champs de saisie
    pointX,
    pointY,
    pointName,
    pointsInput,
    segmentX1,
    segmentY1,
    segmentX2,
    segmentY2,
    segmentIsVector,
    segmentName,
    circleH,
    circleK,
    circleR,
    circleName,
    
    // Actions
    addPoint,
    addMultiplePoints,
    removePoint,
    getPointDisplayName,
    addSegment,
    removeSegment,
    addCircle,
    removeCircle,
    
    // Dessin
    drawPoints,
    drawSegments,
    drawCircles,
    drawAllShapes,
    getVectorAnnotations,
    
    // Utilitaires
    clearAllShapes,
    hasShapes,
    getNextColor,
    resetColorIndex
  }
}
