/**
 * Composable pour la gestion des formes géométriques (points, segments, cercles)
 */
import { ref } from 'vue'
import { GRAPH_COLORS } from './graphConfig'

export function useGraphShapes() {
  // État des formes
  const points = ref([])
  const segments = ref([])
  const circles = ref([])
  
  // Champs de saisie pour les points
  const pointX = ref(0)
  const pointY = ref(0)
  
  // Champs de saisie pour les segments
  const segmentX1 = ref(0)
  const segmentY1 = ref(0)
  const segmentX2 = ref(1)
  const segmentY2 = ref(1)
  
  // Champs de saisie pour les cercles
  const circleH = ref(0)
  const circleK = ref(0)
  const circleR = ref(1)
  
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
  
  // === POINTS ===
  function addPoint(onUpdate) {
    const color = getNextColor()
    points.value.push({
      x: pointX.value,
      y: pointY.value,
      color: color
    })
    
    // Réinitialiser les champs
    pointX.value = 0
    pointY.value = 0
    
    if (onUpdate) onUpdate()
  }
  
  function removePoint(index, onUpdate) {
    points.value.splice(index, 1)
    if (onUpdate) onUpdate()
  }
  
  function drawPoints(traces) {
    points.value.forEach((point, index) => {
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
        name: `Point ${index + 1}: (${point.x}, ${point.y})`,
        showlegend: true,
        hovertemplate: `<b>Point ${index + 1}</b><br>(${point.x}, ${point.y})<extra></extra>`
      })
    })
  }
  
  // === SEGMENTS ===
  function addSegment(onUpdate) {
    const color = getNextColor()
    segments.value.push({
      x1: segmentX1.value,
      y1: segmentY1.value,
      x2: segmentX2.value,
      y2: segmentY2.value,
      color: color
    })
    
    // Réinitialiser les champs
    segmentX1.value = 0
    segmentY1.value = 0
    segmentX2.value = 1
    segmentY2.value = 1
    
    if (onUpdate) onUpdate()
  }
  
  function removeSegment(index, onUpdate) {
    segments.value.splice(index, 1)
    if (onUpdate) onUpdate()
  }
  
  function drawSegments(traces) {
    segments.value.forEach((segment, index) => {
      // Dessiner le segment
      traces.push({
        x: [segment.x1, segment.x2],
        y: [segment.y1, segment.y2],
        type: 'scatter',
        mode: 'lines',
        line: {
          color: segment.color,
          width: 3
        },
        name: `Segment ${index + 1}: [AB]`,
        showlegend: true,
        hovertemplate: `<b>Segment ${index + 1}</b><br>De (${segment.x1}, ${segment.y1}) à (${segment.x2}, ${segment.y2})<extra></extra>`
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
  
  // === CERCLES ===
  function addCircle(onUpdate) {
    if (circleR.value <= 0) {
      alert('Le rayon doit être supérieur à 0')
      return
    }
    
    const color = getNextColor()
    circles.value.push({
      h: circleH.value,
      k: circleK.value,
      r: circleR.value,
      color: color
    })
    
    // Réinitialiser les champs
    circleH.value = 0
    circleK.value = 0
    circleR.value = 1
    
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
          width: 2
        },
        name: `Cercle ${index + 1}: centre(${circle.h}, ${circle.k}), r=${circle.r}`,
        showlegend: true,
        hovertemplate: `<b>Cercle ${index + 1}</b><br>x: %{x:.3f}<br>y: %{y:.3f}<extra></extra>`
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
        hovertemplate: `<b>Centre du cercle ${index + 1}</b><br>(${circle.h}, ${circle.k})<extra></extra>`
      })
    })
  }
  
  // === UTILITAIRES ===
  function clearAllShapes() {
    points.value = []
    segments.value = []
    circles.value = []
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
    segmentX1,
    segmentY1,
    segmentX2,
    segmentY2,
    circleH,
    circleK,
    circleR,
    
    // Actions
    addPoint,
    removePoint,
    addSegment,
    removeSegment,
    addCircle,
    removeCircle,
    
    // Dessin
    drawPoints,
    drawSegments,
    drawCircles,
    drawAllShapes,
    
    // Utilitaires
    clearAllShapes,
    hasShapes,
    getNextColor,
    resetColorIndex
  }
}
