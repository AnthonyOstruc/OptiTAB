import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

/**
 * Ajoute un watermark "OptiTAB" en filigrane sur la page
 */
function addWatermark(pdf) {
  // Sauvegarder l'état graphique
  pdf.saveGraphicsState()
  
  // Configuration du watermark
  pdf.setTextColor(200, 200, 200) // Gris très clair
  pdf.setFontSize(50)
  pdf.setFont('times', 'bold')
  
  // Position au centre de la page
  const centerX = 105 // Centre page A4 (210mm / 2)
  const centerY = 148 // Centre page A4 (297mm / 2)
  
  // Rotation de -45 degrés
  const angle = -45 * (Math.PI / 180)
  
  // Appliquer la rotation et dessiner le texte
  pdf.text('OptiTAB', centerX, centerY, {
    angle: angle,
    align: 'center'
  })
  
  // Restaurer l'état graphique
  pdf.restoreGraphicsState()
}

/**
 * Ajoute un footer à la page PDF
 */
function addFooter(pdf, pageNum, totalPages) {
  pdf.setFontSize(9)
  pdf.setTextColor(107, 114, 128) // Gris
  pdf.setFont('times', 'normal')
  
  // "OptiTAB" à gauche (position plus haute pour éviter les chevauchements)
  pdf.text('OptiTAB - Plateforme éducative', 15, 280)
  
  // Numéro de page à droite (position plus haute pour éviter les chevauchements)
  pdf.text(`Page ${pageNum} / ${totalPages}`, 195, 280, { align: 'right' })
}

/**
 * Découpe un grand canvas en tranches adaptées à la hauteur de contenu d'une page PDF
 */
function sliceCanvasForPages(sourceCanvas, imgWidthMm, contentHeightMm) {
  const slices = []
  const pxPerMm = sourceCanvas.width / imgWidthMm
  const targetHeightPx = Math.floor(contentHeightMm * pxPerMm)
  const bottomBufferPx = Math.floor(pxPerMm * 8) // 8mm de marge sécurité avant le pied de page (évite les coupes sur une ligne)
  const srcCtx = sourceCanvas.getContext('2d')
  const width = sourceCanvas.width
  const height = sourceCanvas.height

  const searchRadius = Math.max(40, Math.floor(pxPerMm * 4)) // fenêtre de recherche encore plus large
  const nonWhiteThreshold = Math.max(3, Math.floor(width * 0.004)) // tolérance plus stricte

  function isNearWhiteRow(y) {
    const data = srcCtx.getImageData(0, y, width, 1).data
    let nonWhite = 0
    for (let x = 0; x < width; x += 4) { // échantillonnage tous les 4px
      const i = x * 4
      const r = data[i]
      const g = data[i + 1]
      const b = data[i + 2]
      const a = data[i + 3]
      if (a > 0 && (r < 245 || g < 245 || b < 245)) {
        nonWhite++
        if (nonWhite > nonWhiteThreshold) return false
      }
    }
    return true
  }

  function findSafeCutY(targetY) {
    let bestY = targetY
    for (let offset = 0; offset <= searchRadius; offset++) {
      const down = Math.min(height - 1, targetY + offset)
      if (isNearWhiteRow(down)) return down
      const up = Math.max(0, targetY - offset)
      if (isNearWhiteRow(up)) return up
    }
    return Math.min(height, Math.max(0, targetY))
  }

  let currentY = 0
  while (currentY < height) {
    const lastPage = currentY + targetHeightPx >= height
    let cutY
    if (lastPage) {
      cutY = height
    } else {
      const target = currentY + targetHeightPx - bottomBufferPx
      cutY = findSafeCutY(target)
      if (cutY <= currentY + 40) {
        cutY = Math.min(height, currentY + targetHeightPx)
      }
    }

    const sliceHeight = Math.min(cutY - currentY, height - currentY)
    const slice = document.createElement('canvas')
    slice.width = width
    slice.height = sliceHeight
    const ctx = slice.getContext('2d')
    ctx.drawImage(sourceCanvas, 0, currentY, width, sliceHeight, 0, 0, width, sliceHeight)
    slices.push(slice)
    currentY += sliceHeight
  }

  return slices
}

/**
 * Utilitaire pour le rendu MathJax en HTML
 */
async function renderMathJax(element) {
  // Attendre que MathJax soit chargé et initialisé
  const ensureStartup = async () => {
    if (typeof window === 'undefined' || !window.MathJax) return
    if (window.MathJax.startup && window.MathJax.startup.promise) {
      try {
        await window.MathJax.startup.promise
      } catch (e) {}
    }
  }

  await ensureStartup()

  if (typeof window !== 'undefined' && window.MathJax && window.MathJax.typesetPromise) {
    try {
      // Forcer MathJax à regénérer le SVG dans l'élément temporaire
      await window.MathJax.typesetPromise([element])
      // Supprimer les balises d'accessibilité qui peuvent être rendues par html2canvas
      element.querySelectorAll('mjx-assistive-mml, .MJX_Assistive_MathML').forEach(el => el.parentNode && el.parentNode.removeChild(el))
      // Laisser le temps aux polices/positions d'être stabilisées
      await new Promise(resolve => setTimeout(resolve, 700))
    } catch (error) {
      console.warn('Erreur lors du rendu MathJax (PDF):', error)
    }
  }
}

/**
 * Crée un élément DOM temporaire pour le rendu
 */
function createTempElement(content, useMathJax = false) {
  const tempDiv = document.createElement('div')
  tempDiv.style.cssText = `
    position: absolute;
    top: -9999px;
    left: -9999px;
    width: 210mm;
    background: white;
    font-family: 'Times New Roman', serif;
    font-size: 12px;
    line-height: 1.6;
    color: #000;
    padding: 20px;
    box-sizing: border-box;
  `
  tempDiv.innerHTML = content
  document.body.appendChild(tempDiv)
  return tempDiv
}

/**
 * Nettoie et formate le contenu mathématique pour PDF
 */
function formatMathContent(text) {
  if (!text) return ''
  
  return text
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/\n\n/g, '<br/><br/>')
    .replace(/\n/g, '<br/>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
}

/**
 * Génère le HTML d'un exercice pour PDF avec solution et étapes optionnelles
 */
function generateExerciceHTML(exercice, includeSolution = true) {
  const titre = exercice.titre || exercice.nom || `Exercice ${exercice.id || ''}`
  const question = formatMathContent(exercice.question || exercice.instruction || exercice.contenu || '')
  const reponse = formatMathContent(exercice.reponse_correcte || exercice.solution || '')
  const etapes = formatMathContent(exercice.etapes || '')
  
  return `
    <div class="exercice-container">
      <div class="exercice-header">
        <h2 class="exercice-titre">${titre}</h2>
        ${exercice.points ? `<div class="exercice-points">${exercice.points} point(s)</div>` : ''}
      </div>
      
      <div class="section enonce-section">
        <h3 class="section-title">📋 Énoncé</h3>
        <div class="section-content">${question}</div>
      </div>
      
      ${includeSolution && etapes ? `
      <div class="section etapes-section">
        <h3 class="section-title">🔢 Méthode de résolution</h3>
        <div class="section-content">${etapes}</div>
      </div>
      ` : ''}
      
      ${includeSolution && reponse ? `
      <div class="section solution-section">
        <h3 class="section-title">✅ Solution</h3>
        <div class="section-content">${reponse}</div>
      </div>
      ` : ''}
    </div>
  `
}

/**
 * Génère le HTML d'un cours pour PDF
 */
function generateCoursHTML(cours) {
  const titre = cours.titre || `Cours ${cours.id || ''}`
  const description = cours.description || ''
  const contenu = formatMathContent(cours.contenu || '')
  const difficulty = cours.difficulty || 'medium'
  const difficultyLabels = {
    'easy': 'Facile',
    'medium': 'Moyen', 
    'hard': 'Difficile'
  }
  
  return `
    <div class="cours-container">
      <div class="cours-header">
        <h2 class="cours-titre">${titre}</h2>
        <div class="cours-difficulty ${difficulty}">${difficultyLabels[difficulty] || difficulty}</div>
      </div>
      
      ${description ? `
      <div class="section description-section">
        <h3 class="section-title">📖 Description</h3>
        <div class="section-content">${formatMathContent(description)}</div>
      </div>
      ` : ''}
      
      <div class="section contenu-section">
        <h3 class="section-title">📚 Contenu du cours</h3>
        <div class="section-content">${contenu}</div>
      </div>
    </div>
  `
}

/**
 * Génère les styles CSS pour le PDF
 */
function generatePDFStyles() {
  return `
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      
      body {
        font-family: 'Times New Roman', serif;
        font-size: 12px;
        line-height: 1.6;
        color: #1f2937;
        background: white;
        padding: 20px;
      }
      
      /* Masquer les contenus d'accessibilité MathJax (évite les doublons) */
      mjx-assistive-mml, .MJX_Assistive_MathML { display: none !important; }
      
      .pdf-header {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 30px;
        padding-bottom: 15px;
        border-bottom: 3px solid #1e40af;
      }
      
      .exercice-container {
        margin-bottom: 40px;
        page-break-inside: avoid;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        background: #fafbfc;
      }
      
      .cours-container {
        margin-bottom: 40px;
        page-break-inside: avoid;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 20px;
        background: #fafbfc;
      }
      
      .exercice-header {
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid #3b82f6;
      }
      
      .cours-header {
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid #10b981;
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
      }
      
      .exercice-titre {
        font-size: 16px;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 5px;
      }
      
      .cours-titre {
        font-size: 16px;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 5px;
        flex: 1;
      }
      
      .cours-difficulty {
        padding: 4px 8px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }
      
      .cours-difficulty.easy {
        background: #e8f5e8;
        color: #2e7d32;
      }
      
      .cours-difficulty.medium {
        background: #fff3e0;
        color: #f57c00;
      }
      
      .cours-difficulty.hard {
        background: #ffebee;
        color: #c62828;
      }
      
      .exercice-points {
        font-size: 11px;
        color: #6b7280;
        background: #f3f4f6;
        padding: 3px 8px;
        border-radius: 10px;
        display: inline-block;
      }
      
      .section {
        margin-bottom: 18px;
        page-break-inside: avoid;
      }
      
      .section-title {
        font-size: 13px;
        font-weight: bold;
        color: #374151;
        margin-bottom: 8px;
        padding: 6px 10px;
        background: #f1f5f9;
        border-left: 4px solid #3b82f6;
        border-radius: 4px;
      }
      
      .etapes-section .section-title {
        border-left-color: #8b5cf6;
        background: #faf5ff;
      }
      
      .solution-section .section-title {
        border-left-color: #10b981;
        background: #f0fdf4;
      }
      
      .section-content {
        padding: 12px;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        line-height: 1.8;
      }
      
      /* Styles pour MathJax */
      .MathJax, mjx-container {
        margin: 8px 0 !important;
        page-break-inside: avoid;
      }
      
      .MathJax_Display {
        margin: 12px 0 !important;
        text-align: center;
      }
      
      /* Images */
      img {
        max-width: 100%;
        height: auto;
        page-break-inside: avoid;
        border-radius: 4px;
        margin: 8px 0;
      }
      
      /* Formatage du texte */
      strong { color: #1f2937; font-weight: bold; }
      em { color: #374151; font-style: italic; }
      
      /* Éviter les coupures */
      .no-break { page-break-inside: avoid; }
    </style>
  `
}



/**
 * Génère un PDF pour un exercice unique avec solution et étapes
 */
export async function generateExercicePDF(exercice, filename = 'exercice', useMathJax = true, includeSolution = false) {
  try {
    const titre = exercice.titre || exercice.nom || 'Exercice'
    
    // Créer le contenu HTML
    const styles = generatePDFStyles()
    const exerciceHTML = generateExerciceHTML(exercice, includeSolution)
    
    const fullHTML = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        ${styles}
      </head>
      <body>
        <div class="pdf-header">${titre} - Exercice complet</div>
        ${exerciceHTML}
      </body>
      </html>
    `
    
    const tempElement = createTempElement(fullHTML, useMathJax)
    if (useMathJax) {
      await renderMathJax(tempElement)
    }

    const canvas = await html2canvas(tempElement, {
      scale: 2,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
      width: 794,
      height: 1123
    })

    document.body.removeChild(tempElement)

    const pdf = new jsPDF('portrait', 'mm', 'a4')
    const marginLeft = 5
    const marginTop = 12
    const imgWidth = 200
    const contentHeight = 250 // plus de marge en bas pour éviter la coupe

    const slices = sliceCanvasForPages(canvas, imgWidth, contentHeight)
    const totalPages = slices.length
    let pageNumber = 1

    slices.forEach((slice, index) => {
      if (index > 0) pdf.addPage()
      pdf.addImage(slice.toDataURL('image/jpeg', 0.95), 'JPEG', marginLeft, marginTop, imgWidth, (slice.height * imgWidth) / slice.width)
      addWatermark(pdf)
      addFooter(pdf, pageNumber, totalPages)
      pageNumber++
    })

    pdf.save(`${filename}.pdf`)
  } catch (error) {
    console.error('Erreur lors de la génération du PDF:', error)
    throw error
  }
}

/**
 * Génère un PDF pour une liste d'exercices avec étapes et solutions
 */
export async function generateExercicesListPDF(exercices, filename = 'exercices', useMathJax = true, includeSolution = false) {
  try {
    if (!Array.isArray(exercices) || exercices.length === 0) {
      throw new Error('Aucun exercice à exporter')
    }

    const pdfTitle = includeSolution 
      ? `Exercices avec solutions (${exercices.length} exercice(s))`
      : `Exercices - énoncés seuls (${exercices.length} exercice(s))`

    const styles = generatePDFStyles()
    const exercicesHTML = exercices.map(exercice => generateExerciceHTML(exercice, includeSolution)).join('')

    const fullHTML = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        ${styles}
      </head>
      <body>
        <div class="pdf-header">${pdfTitle}</div>
        ${exercicesHTML}
      </body>
      </html>
    `

    const tempElement = createTempElement(fullHTML, true)
    if (useMathJax) {
      await renderMathJax(tempElement)
    }

    const canvas = await html2canvas(tempElement, {
      scale: 2,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
      width: 794
    })

    document.body.removeChild(tempElement)

    const pdf = new jsPDF('portrait', 'mm', 'a4')
    const marginLeft = 5
    const marginTop = 12
    const imgWidth = 200
    const contentHeight = 250

    const slices = sliceCanvasForPages(canvas, imgWidth, contentHeight)
    const totalPages = slices.length
    let pageNumber = 1

    slices.forEach((slice, index) => {
      if (index > 0) pdf.addPage()
      pdf.addImage(slice.toDataURL('image/jpeg', 0.95), 'JPEG', marginLeft, marginTop, imgWidth, (slice.height * imgWidth) / slice.width)
      addWatermark(pdf)
      addFooter(pdf, pageNumber, totalPages)
      pageNumber++
    })

    pdf.save(`${filename}.pdf`)
  } catch (error) {
    console.error('Erreur lors de la génération du PDF de liste:', error)
    throw error
  }
}

/**
 * Génère un PDF pour une liste de cours
 */
export async function generateCoursPDF(cours, filename = 'cours', useMathJax = true) {
  try {
    if (!Array.isArray(cours) || cours.length === 0) {
      throw new Error('Aucun cours à exporter')
    }
    
    const pdfTitle = `Cours (${cours.length} cours)`
    
    // Créer le contenu HTML
    const styles = generatePDFStyles()
    const coursHTML = cours.map(coursItem => generateCoursHTML(coursItem)).join('')
    
    const fullHTML = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        ${styles}
      </head>
      <body>
        <div class="pdf-header">${pdfTitle}</div>
        ${coursHTML}
      </body>
      </html>
    `
    
    // Créer un élément temporaire pour le rendu
    const tempElement = createTempElement(fullHTML, true)
    
    // Rendu MathJax
    if (useMathJax) {
      await renderMathJax(tempElement)
    }
    
    // Générer le canvas avec html2canvas
    const canvas = await html2canvas(tempElement, {
      scale: 2,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
      width: 794
    })
    
    // Nettoyer l'élément temporaire
    document.body.removeChild(tempElement)
    
    // Créer le PDF et slicer le canvas
    const pdf = new jsPDF('portrait', 'mm', 'a4')
    const marginLeft = 5
    const marginTop = 12
    const imgWidth = 200
    const contentHeight = 250

    const slices = sliceCanvasForPages(canvas, imgWidth, contentHeight)
    const totalPages = slices.length
    let pageNumber = 1

    slices.forEach((slice, index) => {
      if (index > 0) pdf.addPage()
      pdf.addImage(slice.toDataURL('image/jpeg', 0.95), 'JPEG', marginLeft, marginTop, imgWidth, (slice.height * imgWidth) / slice.width)
      addWatermark(pdf)
      addFooter(pdf, pageNumber, totalPages)
      pageNumber++
    })
    
    // Télécharger
    pdf.save(`${filename}.pdf`)
    
  } catch (error) {
    console.error('Erreur lors de la génération du PDF de cours:', error)
    throw error
  }
}

/**
 * Génère un PDF à partir d'un élément HTML
 */
export async function generatePDFFromHTML(element, filename = 'document.pdf', options = {}) {
  try {
    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      allowTaint: true,
      backgroundColor: '#ffffff',
      ...options
    })
    
    const pdf = new jsPDF('portrait', 'mm', 'a4')
    const imgWidth = 210
    const pageHeight = 297
    const imgHeight = (canvas.height * imgWidth) / canvas.width
    let heightLeft = imgHeight
    let position = 0
    
    pdf.addImage(canvas.toDataURL('image/jpeg', 0.95), 'JPEG', 0, position, imgWidth, imgHeight)
    heightLeft -= pageHeight
    
    while (heightLeft >= 0) {
      position = heightLeft - imgHeight
      pdf.addPage()
      pdf.addImage(canvas.toDataURL('image/jpeg', 0.95), 'JPEG', 0, position, imgWidth, imgHeight)
      heightLeft -= pageHeight
    }
    
    pdf.save(filename)
    
  } catch (error) {
    console.error('Erreur lors de la génération du PDF HTML:', error)
    throw error
  }
}
