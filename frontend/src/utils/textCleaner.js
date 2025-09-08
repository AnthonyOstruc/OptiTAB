export function normalizeAccents(text) {
  if (!text) return text;
  return text
    .normalize('NFC')
    // Corrections for common decomposed accent sequences
    .replace(/e\u0301/g, 'é') // é
    .replace(/e\u0300/g, 'è') // è
    .replace(/a\u0300/g, 'à') // à
    .replace(/o\u0302/g, 'ô') // ô
    .replace(/u\u0302/g, 'û') // û
    .replace(/i\u0302/g, 'î') // î
    .replace(/e\u0302/g, 'ê') // ê
    .replace(/u\u0300/g, 'ù') // ù
    .replace(/c\u0327/g, 'ç') // ç
    .replace(/A\u0300/g, 'À')
    .replace(/E\u0301/g, 'É')
    .replace(/E\u0300/g, 'È')
    .replace(/O\u0302/g, 'Ô')
    .replace(/U\u0302/g, 'Û')
    .replace(/I\u0302/g, 'Î')
    .replace(/E\u0302/g, 'Ê')
    .replace(/U\u0300/g, 'Ù')
    .replace(/C\u0327/g, 'Ç');
}

export function fixAccentSpacing(text) {
  if (!text) return text;
  return text
    .replace(/\s+é/g, 'é')
    .replace(/\s+è/g, 'è')
    .replace(/\s+à/g, 'à')
    .replace(/\s+ô/g, 'ô')
    .replace(/\s+û/g, 'û')
    .replace(/\s+î/g, 'î')
    .replace(/\s+ê/g, 'ê')
    .replace(/\s+ù/g, 'ù')
    .replace(/\s+ç/g, 'ç')
    .replace(/\s+É/g, 'É')
    .replace(/\s+È/g, 'È')
    .replace(/\s+À/g, 'À')
    .replace(/\s+Ô/g, 'Ô')
    .replace(/\s+Û/g, 'Û')
    .replace(/\s+Î/g, 'Î')
    .replace(/\s+Ê/g, 'Ê')
    .replace(/\s+Ù/g, 'Ù')
    .replace(/\s+Ç/g, 'Ç');
}

export function cleanText(text) {
  if (!text) return text;
  let cleaned = normalizeAccents(text);
  cleaned = fixAccentSpacing(cleaned);
  // Only fix specific known issues without aggressive word splitting
  cleaned = cleaned
    .replace(/Typede/g, 'Type de')
    .replace(/fonctionidentifié/g, 'fonction identifié')
    .replace(/intégrationparparties/g, 'intégration par parties')
    .replace(/produitde/g, 'produit de')
    .replace(/fonctioncomposée/g, 'fonction composée')
    .replace(/fonctionrationnelle/g, 'fonction rationnelle')
    .replace(/fonctiontrigonométrique/g, 'fonction trigonométrique')
    .replace(/fonctionexponentielle/g, 'fonction exponentielle')
    .replace(/fonctionlogarithmique/g, 'fonction logarithmique')
    .replace(/intégraleindéfinie/g, 'intégrale indéfinie')
    .replace(/intégraledéfinie/g, 'intégrale définie')
    .replace(/décompositionenfractions/g, 'décomposition en fractions')
    .replace(/changementdevariable/g, 'changement de variable')
    .replace(/linéaritédel/g, 'linéarité de l')
    .replace(/règledepuissance/g, 'règle de puissance')
    .replace(/intégrationd/g, 'intégration d')
    .replace(/intégrationdirecte/g, 'intégration directe')
    .replace(/fonctionpolynomiale/g, 'fonction polynomiale')
    .replace(/fonctionconstante/g, 'fonction constante')
    // Only add spaces around colons when they're missing
    .replace(/([a-zA-ZÀ-ÿ]):/g, '$1 :')
    .replace(/:\s*([a-zA-ZÀ-ÿ])/g, ': $1')
    // Remove aggressive word splitting rules that were causing issues
    // .replace(/([a-zÀ-ÿ])([A-ZÀ-ÿ])/g, '$1 $2') // REMOVED - was splitting words incorrectly
    // .replace(/([a-zA-ZÀ-ÿ])-/g, '$1 -') // REMOVED - was adding unwanted spaces
    // .replace(/-\s*([a-zA-ZÀ-ÿ])/g, '- $1') // REMOVED - was adding unwanted spaces
    .replace(/\s+/g, ' ') // collapse multiple spaces
    .trim();
  return cleaned;
}

// Utility to render inline math inside regular text nodes using KaTeX
import katex from 'katex';

export function renderInlineMath(text, el) {
  if (!el) return;
  const cleanedText = cleanText(text);
  const parts = cleanedText.split(/(\$[^$]+\$)/g);
  el.innerHTML = '';
  parts.forEach((part) => {
    if (part.startsWith('$') && part.endsWith('$')) {
      const math = part.slice(1, -1);
      const span = document.createElement('span');
      try {
        katex.render(math, span, { throwOnError: false, displayMode: false });
      } catch (e) {
        span.textContent = part;
      }
      el.appendChild(span);
    } else if (part) {
      el.appendChild(document.createTextNode(part));
    }
  });
} 