// Horloge interactive (page methodes/lire-l-heure).
//
// Deux panneaux : « Explorer » (on avance les aiguilles, l'heure s'écrit en
// chiffres, en mots et sur 24 heures) et « S'entraîner » (une horloge, quatre
// réponses, trois niveaux CP, CE1, CE2). Le cadran est écrit dans la page à la
// construction (lisible sans JavaScript) ; outils/horloge.js le fait vivre.

// Cadran en SVG : rayon 92 dans un carré de 200, centre (100, 100).
// Avec « minutes » : les nombres 5, 10… 55 autour du cadran (zone de 236 × 236).
export function cadranSvg({ h, m, minutes = false, attribut = '', titre = '' }) {
  const cx = 100
  const cy = 100
  const pt = (r, deg) => {
    const a = (deg * Math.PI) / 180
    return [+(cx + r * Math.sin(a)).toFixed(2), +(cy - r * Math.cos(a)).toFixed(2)]
  }
  const traits = Array.from({ length: 60 }, (_, k) => {
    const cinq = k % 5 === 0
    const [x1, y1] = pt(cinq ? 80 : 85, k * 6)
    const [x2, y2] = pt(90, k * 6)
    return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cinq ? 'hl-t5' : 'hl-t1'}"/>`
  }).join('')
  const nombres = Array.from({ length: 12 }, (_, k) => {
    const n = k + 1
    const [x, y] = pt(67, n * 30)
    return `<text x="${x}" y="${y}" class="hl-n">${n}</text>`
  }).join('')
  const autour = minutes
    ? Array.from({ length: 12 }, (_, k) => {
        const mn = k * 5
        const [x, y] = pt(106, mn * 6)
        return `<text x="${x}" y="${y}" class="hl-mn">${String(mn).padStart(2, '0')}</text>`
      }).join('')
    : ''
  const angleH = ((h % 12) * 30 + m * 0.5).toFixed(1)
  const angleM = (m * 6).toFixed(1)
  const vue = minutes ? '-18 -18 236 236' : '0 0 200 200'
  return `<svg class="hl-cadran" viewBox="${vue}" role="img" aria-label="${titre}" ${attribut}>
      <circle cx="100" cy="100" r="96" class="hl-bord"/>
      <circle cx="100" cy="100" r="92" class="hl-fond"/>
      ${traits}${nombres}${autour}
      <line x1="100" y1="100" x2="100" y2="54" class="hl-ah" data-aiguille="h" transform="rotate(${angleH} 100 100)"/>
      <line x1="100" y1="100" x2="100" y2="24" class="hl-am" data-aiguille="m" transform="rotate(${angleM} 100 100)"/>
      <circle cx="100" cy="100" r="5.5" class="hl-centre"/>
    </svg>`
}

const BOUTONS = [[-60, '− 1 h'], [60, '+ 1 h'], [-5, '− 5 min'], [5, '+ 5 min'], [-1, '− 1 min'], [1, '+ 1 min']]

export function horlogeHtml() {
  // Heure de départ : 9 h 15 (textes identiques à ceux que calcule outils/horloge.js).
  return `<section class="otc hl" data-outil="horloge" aria-labelledby="otc-horloge-titre">
  <div class="otc__tete">
    <p class="otc__kicker">Outil gratuit</p>
    <p class="otc__titre" id="otc-horloge-titre">Horloge interactive pour apprendre l’heure</p>
    <p class="otc__intro">Avancez les aiguilles et lisez l’heure en chiffres et en mots, puis entraînez-vous : CP (heures entières), CE1 (demi-heures et quarts d’heure) ou CE2 (minutes).</p>
  </div>
  <div class="otc__onglets" role="tablist" aria-label="Mode">
    <button type="button" role="tab" class="otc__onglet" data-mode="explorer" id="hl-o-explorer" aria-controls="hl-p-explorer" aria-selected="true">Explorer l’horloge</button>
    <button type="button" role="tab" class="otc__onglet" data-mode="quiz" id="hl-o-quiz" aria-controls="hl-p-quiz" aria-selected="false" tabindex="-1">S’entraîner</button>
  </div>
  <div class="hl__panneau" data-panneau="explorer" id="hl-p-explorer" role="tabpanel" aria-labelledby="hl-o-explorer">
    <div class="hl__grille">
      ${cadranSvg({ h: 9, m: 15, minutes: true, attribut: 'data-cadran="explorer"', titre: 'Horloge qui indique 9 h 15' })}
      <div class="hl__lecture" aria-live="polite">
        <p class="hl__num" data-num>9 h 15</p>
        <p class="hl__mots" data-mots>neuf heures et quart du matin</p>
        <p class="hl__24" data-vingtquatre>Sur 24 heures : neuf heures quinze</p>
      </div>
    </div>
    <div class="hl__boutons">${BOUTONS.map(([pas, texte]) => `<button type="button" class="hl__btn" data-pas="${pas}">${texte}</button>`).join('')}<button type="button" class="hl__btn hl__btn--large" data-pas="720">Matin ⇄ après-midi (12 h)</button></div>
  </div>
  <div class="hl__panneau" data-panneau="quiz" id="hl-p-quiz" role="tabpanel" aria-labelledby="hl-o-quiz" hidden>
    <div class="hl__niveaux" role="radiogroup" aria-label="Niveau">
      <button type="button" role="radio" class="hl__niveau" data-niveau="cp" aria-checked="false">CP : heures entières</button>
      <button type="button" role="radio" class="hl__niveau" data-niveau="ce1" aria-checked="true">CE1 : quarts d’heure</button>
      <button type="button" role="radio" class="hl__niveau" data-niveau="ce2" aria-checked="false">CE2 : minutes</button>
    </div>
    <div class="hl__grille">
      ${cadranSvg({ h: 3, m: 30, attribut: 'data-cadran="quiz"', titre: 'Horloge à lire' })}
      <div class="hl__question">
        <p class="hl__consigne">Quelle heure indique l’horloge ?</p>
        <div class="hl__choix" data-choix></div>
        <p class="hl__retour" data-retour aria-live="polite"></p>
        <div class="hl__suite"><button type="button" class="rg-btn rg-btn--primary rg-btn--sm" data-suivant>Nouvelle horloge</button><span class="hl__score" data-score></span></div>
      </div>
    </div>
  </div>
</section>`
}
