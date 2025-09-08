/**
 * Utilitaire pour le rendu scientifique des contenus (cours, exercices, etc.)
 */

/**
 * Traite le texte LaTeX et HTML de base
 */
export function unescapeLatex(text) {
  if (!text) return ''
  
  return text
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;(?!nbsp;)/g, '&')  // Ne pas toucher aux &nbsp;
    .replace(/\\/g, '\\')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
}

/**
 * Convertit le Markdown en HTML
 */
export function markdownToHtml(text) {
  if (!text) return ''
  
  let html = text
  
  // Traitement des titres (avec espacement)
  html = html.replace(/^#### (.*$)/gm, '<h4 style="margin-top: 1.5em; margin-bottom: 0.8em; color: #193e8e; font-weight: 600;">$1</h4>')
  html = html.replace(/^### (.*$)/gm, '<h3 style="margin-top: 2em; margin-bottom: 1em; color: #193e8e; font-weight: 600;">$1</h3>')
  html = html.replace(/^## (.*$)/gm, '<h2 style="margin-top: 2.5em; margin-bottom: 1.2em; color: #193e8e; font-weight: 600; font-size: 1.5em;">$1</h2>')
  html = html.replace(/^# (.*$)/gm, '<h1 style="margin-top: 3em; margin-bottom: 1.5em; color: #193e8e; font-weight: 700; font-size: 1.8em;">$1</h1>')
  
  // Traitement des listes avec puces
  const lines = html.split('\n')
  let processedLines = []
  let inList = false
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    const trimmedLine = line.trim()
    
    if (trimmedLine.startsWith('- ')) {
      if (!inList) {
        processedLines.push('<ul style="margin: 1em 0; padding-left: 0;">')
        inList = true
      }
      processedLines.push(`<li style="margin-bottom: 0.5em;">${trimmedLine.substring(2)}</li>`)
    } else {
      if (inList) {
        processedLines.push('</ul>')
        inList = false
      }
      if (trimmedLine) {
        // Préserver les espaces en les convertissant en entités HTML
        let processedLine = line
          .replace(/^ +/g, (match) => '&nbsp;'.repeat(match.length))  // Espaces au début
          .replace(/ +$/g, (match) => '&nbsp;'.repeat(match.length))  // Espaces à la fin
          .replace(/  +/g, (match) => '&nbsp;'.repeat(match.length))  // Espaces multiples au milieu
        
        processedLines.push(`<p style="margin-bottom: 1em; line-height: 1.6;">${processedLine}</p>`)
      } else if (line === '') {
        // Ligne vide
        processedLines.push(`<p style="margin-bottom: 1em; line-height: 1.6;">&nbsp;</p>`)
      }
    }
  }
  
  if (inList) {
    processedLines.push('</ul>')
  }
  
  html = processedLines.join('\n')
  
  // Gras et italique
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong style="color: #193e8e;">$1</strong>')
  html = html.replace(/\*([^*]+)\*/g, '<em style="color: #666;">$1</em>')
  
  return html
}

/**
 * Rendu du contenu avec images intégrées
 */
export function renderContentWithImages(content, images = []) {
  if (!content) return ''
  
  // D'abord, traiter le contenu Markdown
  let processedText = markdownToHtml(content)
  
  // Ensuite, traiter LaTeX et HTML de base
  processedText = unescapeLatex(processedText)
  
  // Si pas d'images, retourner le texte traité
  if (!images || images.length === 0) {
    return processedText
  }
  
  // Créer un mapping des images par position
  const imagesByPosition = {}
  images.forEach(img => {
    if (img.position) {
      imagesByPosition[img.position] = img
    }
  })
  
  // Remplacer les marqueurs [IMAGE_1], [IMAGE_2], etc. par les images
  processedText = processedText.replace(/\[IMAGE_(\d+)\]/g, (match, position) => {
    const image = imagesByPosition[parseInt(position)]
    if (image) {
      return `
        <div class="content-image-container" data-image-position="${position}" style="text-align: center; margin: 2em 0;">
          <img 
            src="${getImageUrl(image.image)}" 
            alt="Image ${image.image_type || 'illustration'} - position ${position}"
            class="content-image"
            style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);"
          />
          ${image.legende ? `<div class="image-legende" style="text-align: center; margin-top: 8px; font-style: italic; color: #666; font-size: 0.9em;">${image.legende}</div>` : ''}
        </div>
      `
    }
    return match // Garder le marqueur si l'image n'existe pas
  })
  
  return processedText
}

/**
 * Construit l'URL complète d'une image
 */
export function getImageUrl(imagePath, type = 'cours') {
  // Si imagePath est déjà une URL (blob: ou data:)
  if (imagePath && (imagePath.startsWith('blob:') || imagePath.startsWith('data:'))) {
    return imagePath
  }
  
  // Si imagePath est déjà un chemin complet (commence par /media/), l'utiliser tel quel
  if (imagePath && imagePath.startsWith('/media/')) {
    return `http://localhost:8000${imagePath}`
  }
  
  // Si imagePath est un chemin relatif, construire l'URL complète
  if (imagePath && imagePath.includes('/')) {
    return `http://localhost:8000/media/${imagePath}`
  }
  
  // Si imagePath est juste un nom de fichier, construire le chemin complet
  if (imagePath && !imagePath.startsWith('/')) {
    const folder = type === 'cours' ? 'cours_images' : 'exercice_images'
    return `http://localhost:8000/media/${folder}/${imagePath}`
  }
  
  return imagePath
}

/**
 * Rend le contenu MathJax
 */
export function renderMath() {
  // Attendre que MathJax soit disponible
  if (window.MathJax && window.MathJax.typesetPromise) {
    window.MathJax.typesetPromise()
  } else {
    // Si MathJax n'est pas encore chargé, attendre un peu
    setTimeout(() => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise()
      }
    }, 100)
  }
  
  // Retry multiple times if MathJax is not ready
  let retryCount = 0
  const maxRetries = 10
  
  const tryRender = () => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise()
    } else if (retryCount < maxRetries) {
      retryCount++
      setTimeout(tryRender, 200)
    }
  }
  
  setTimeout(tryRender, 100)
}

/**
 * Composable pour le rendu scientifique
 */
export function useScientificRenderer() {
  return {
    unescapeLatex,
    markdownToHtml,
    renderContentWithImages,
    getImageUrl,
    renderMath
  }
} 