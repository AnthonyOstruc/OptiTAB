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
  // Réduire les espacements par défaut autour des titres pour éviter les grands blancs
  html = html.replace(/^#### (.*$)/gm, '<h4 style="margin-top: 0.5em; margin-bottom: 0.5em; color: #193e8e; font-weight: 600;">$1</h4>')
  html = html.replace(/^### (.*$)/gm, '<h3 style="margin-top: 0.6em; margin-bottom: 0.5em; color: #193e8e; font-weight: 600;">$1</h3>')
  html = html.replace(/^## (.*$)/gm, '<h2 style="margin-top: 0.7em; margin-bottom: 0.5em; color: #193e8e; font-weight: 600; font-size: 1.5em;">$1</h2>')
  html = html.replace(/^# (.*$)/gm, '<h1 style="margin-top: 0.8em; margin-bottom: 0.6em; color: #193e8e; font-weight: 700; font-size: 1.8em;">$1</h1>')
  
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

  // Détecter si le contenu est déjà du HTML structuré
  const looksLikeHtml = /<\s*(h[1-6]|p|div|table|ul|ol|li|img|section|article|header|footer|span|br|hr)\b/i.test(content)

  // Si c'est du HTML, ne pas passer par le convertisseur Markdown pour éviter
  // l'injection de <p> vides et les espaces excessifs entre les blocs.
  let processedText = looksLikeHtml ? content : markdownToHtml(content)
  
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
            style="max-width: 100%; height: auto;"
          />
          ${image.caption || image.legende ? `<div class="image-legende" style="text-align: center; margin-top: 8px; font-style: italic; color: #666; font-size: 0.9em;">${image.caption || image.legende}</div>` : ``}
        </div>
      `
    }
    return match // Garder le marqueur si l'image n'existe pas
  })
  
  return processedText
}

/**
 * Construit l'URL compl�te d'une image
 */
export function getImageUrl(imagePath, type = 'cours') {
  // Si imagePath est déjà une URL (blob: ou data:)
  if (imagePath && (imagePath.startsWith('blob:') || imagePath.startsWith('data:'))) {
    return imagePath
  }
  // Si imagePath est une URL absolue http(s), la renvoyer telle quelle
  if (imagePath && /^(https?:)?\/\//i.test(imagePath)) {
    return imagePath
  }

  // Détecter l'environnement et construire l'URL de base
  const isProduction = window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
  // En production, permettre la surcharge via VITE_MEDIA_BASE_URL / VITE_API_BASE_URL
  let prodMediaBase = null
  try {
    // import.meta.env est remplacé au build par Vite
    // eslint-disable-next-line no-undef
    prodMediaBase = (import.meta && import.meta.env)
      ? (import.meta.env.VITE_MEDIA_BASE_URL || import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL)
      : null
  } catch (_) {
    prodMediaBase = null
  }
  const baseUrl = isProduction
    ? (prodMediaBase || 'https://optitab-backend.onrender.com')
    : 'http://localhost:8000'

  // Si imagePath est déjà un chemin complet (commence par /media/), l'utiliser tel quel
  if (imagePath && imagePath.startsWith('/media/')) {
    return `${baseUrl}${imagePath}`
  }
  // Si l'API renvoie "media/..." (sans slash initial)
  if (imagePath && imagePath.startsWith('media/')) {
    return `${baseUrl}/${imagePath}`
  }

  // Si imagePath est un chemin relatif, construire l'URL compl�te
  if (imagePath && imagePath.includes('/')) {
    return `${baseUrl}/media/${imagePath}`
  }

  // Si imagePath est juste un nom de fichier, construire le chemin complet
  if (imagePath && !imagePath.startsWith('/')) {
    let folder = 'cours_images'
    if (type === 'exercice' || type === 'exercices') folder = 'exercice_images'
    else if (type === 'synthesis' || type === 'sheet' || type === 'sheets') folder = 'synthesis_images'
    else if (type === 'quiz') folder = 'quiz_images'
    return `${baseUrl}/media/${folder}/${imagePath}`
  }

  return imagePath
}

/**
 * Rend le contenu MathJax - Force le rendu même si le contenu est en cache
 * Cette fonction réinitialise complètement le rendu pour éviter les problèmes de cache
 */
export function renderMath() {
  // Fonction pour forcer le rendu MathJax
  const forceRender = () => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      try {
        // Vider le cache de MathJax pour forcer un nouveau rendu
        if (window.MathJax.typesetClear) {
          window.MathJax.typesetClear()
        }
        // Forcer le rendu complet
        window.MathJax.typesetPromise()
          .catch((err) => {
            console.warn('[MathJax] Erreur lors du rendu:', err)
          })
      } catch (error) {
        console.warn('[MathJax] Erreur:', error)
      }
    }
  }
  
  // Première tentative immédiate
  forceRender()
  
  // Deuxième tentative après un court délai (au cas où MathJax n'est pas encore prêt)
  setTimeout(forceRender, 50)
  
  // Retry multiple times if MathJax is not ready
  let retryCount = 0
  const maxRetries = 8
  
  const tryRender = () => {
    if (window.MathJax && window.MathJax.typesetPromise) {
      forceRender()
    } else if (retryCount < maxRetries) {
      retryCount++
      setTimeout(tryRender, 150)
    } else {
      console.warn('[MathJax] MathJax n\'est pas disponible après plusieurs tentatives')
    }
  }
  
  // Tentatives supplémentaires pour s'assurer que MathJax est chargé
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




