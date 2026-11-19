// Simulateur de note du brevet (page methodes/simulateur-brevet).
//
// Règles officielles (arrêté du 10 avril 2025, JO du 12 avril 2025 ; confirmées
// pour la session 2027 par le BO spécial n° 4 du 17 septembre 2026 ; mémento
// Éduscol de décembre 2025) :
//   note finale = 40 % × contrôle continu + 60 % × moyenne des épreuves ;
//   contrôle continu = (somme des moyennes annuelles des enseignements
//     obligatoires de 3e + points au-dessus de 10 d'UN enseignement facultatif)
//     ÷ nombre d'enseignements obligatoires, sans dépasser 20 ;
//   épreuves : français 2, mathématiques 2, histoire-géographie 1,5, EMC 0,5,
//     sciences 2, oral 2 ; diplôme si note finale ≥ 10 ; mentions 12, 14, 16, 18.
// Le calcul est fait ici pour l'exemple affiché sans JavaScript, et dans
// outils/brevet.js pour la saisie (même formules ; contrôle croisé par
// contenu/methodes/simulateur-brevet/generer.py).

export const MATIERES = [
  ['francais', 'Français', 13], ['maths', 'Mathématiques', 12], ['lv1', 'Langue vivante 1', 14],
  ['lv2', 'Langue vivante 2', 13], ['hg', 'Histoire-géographie', 12], ['emc', 'Enseignement moral et civique', 14],
  ['svt', 'Sciences de la vie et de la Terre', 12], ['pc', 'Physique-chimie', 11], ['techno', 'Technologie', 13],
  ['eps', 'Éducation physique et sportive', 15], ['arts', 'Arts plastiques', 15], ['musique', 'Éducation musicale', 14]
]
export const EPREUVES = [
  ['francais', 'Français', 2, 12], ['maths', 'Mathématiques', 2, 11], ['hg', 'Histoire-géographie', 1.5, 13],
  ['emc', 'Enseignement moral et civique', 0.5, 15], ['sciences', 'Sciences', 2, 12], ['oral', 'Oral de soutenance', 2, 15]
]
export const OPTIONS = [
  ['', 'Aucune option'], ['lca', 'Latin ou grec (langues et cultures de l’Antiquité)'],
  ['lce', 'Langues et cultures européennes'], ['lcr', 'Langue et culture régionales'], ['chant', 'Chant choral'],
  ['lsf', 'Langue des signes française']
]
export const SEUILS = [[10, 'obtenir le brevet'], [12, 'la mention assez bien'], [14, 'la mention bien'], [16, 'la mention très bien'], [18, 'les félicitations du jury']]

const NBSP = String.fromCharCode(160)
const e = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
const fmt = (x) => x.toFixed(2).replace('.', ',')
const virgule = (x) => String(x).replace('.', ',')
// Note finale arrondie au centième : le verdict suit toujours le nombre affiché.
export const arrondi = (x) => Math.round(x * 100 + 1e-7) / 100
// Note à viser arrondie au centième supérieur : l'obtenir suffit toujours.
export const plafond = (x) => Math.ceil(x * 100 - 1e-7) / 100

export function controleContinu(moyennes, option = null) {
  const notes = moyennes.filter((m) => m != null)
  if (!notes.length) return null
  const bonus = option != null && option > 10 ? option - 10 : 0
  return Math.min(20, (notes.reduce((s, m) => s + m, 0) + bonus) / notes.length)
}
export const moyenneEpreuves = (notes) => EPREUVES.reduce((s, [k, , c]) => s + c * notes[k], 0) / 10
export const noteFinale = (cc, ep) => 0.4 * cc + 0.6 * ep
export function mention(n) {
  if (n >= 18) return 'très bien avec les félicitations du jury'
  if (n >= 16) return 'très bien'
  if (n >= 14) return 'bien'
  if (n >= 12) return 'assez bien'
  return ''
}
export const aViser = (cc, seuil) => (seuil - 0.4 * cc) / 0.6

export function verdict(note) {
  const n = arrondi(note)
  if (n < 10) return `Non admis : il manque ${fmt(10 - n)}${NBSP}point${10 - n >= 2 ? 's' : ''} sur 20.`
  const m = mention(n)
  return m ? `Admis avec la mention ${m}.` : 'Admis, sans mention.'
}

export function lignesAViser(cc) {
  return SEUILS.map(([s, quoi]) => {
    const v = aViser(cc, s)
    const val = v <= 0 ? 'déjà assuré' : v > 20 ? 'hors d’atteinte' : `${fmt(plafond(v))}${NBSP}/${NBSP}20`
    return `<li><span>Pour ${e(quoi)} (${s}/20)</span><strong>${val}</strong></li>`
  }).join('')
}

function champ(nom, id, libelle, valeur, extra = '') {
  return `<label class="bv__champ" for="${id}"><span class="bv__lib">${e(libelle)}${extra}</span><input id="${id}" type="text" inputmode="decimal" autocomplete="off" spellcheck="false" ${nom} value="${e(virgule(valeur))}" aria-describedby="bv-sur20"></label>`
}

export function brevetHtml() {
  const moy = MATIERES.map(([, , v]) => v)
  const cc = controleContinu(moy)
  const notes = Object.fromEntries(EPREUVES.map(([k, , , v]) => [k, v]))
  const ep = moyenneEpreuves(notes)
  const n = arrondi(noteFinale(cc, ep))
  return `<section class="otc bv" data-outil="brevet" aria-labelledby="otc-brevet-titre">
  <div class="otc__tete">
    <p class="otc__kicker">Outil gratuit</p>
    <p class="otc__titre" id="otc-brevet-titre">Simulateur de note du brevet</p>
    <p class="otc__intro">Entrez vos moyennes annuelles de 3e et vos notes, réelles ou estimées, aux épreuves : la note finale, la mention et la note à viser se calculent à chaque saisie. Règles officielles en vigueur depuis la session 2026.</p>
    <p class="bv__aide" id="bv-sur20">Notes sur 20, avec une virgule si besoin (13,5). Laissez vide une matière dont vous êtes dispensé.</p>
  </div>
  <fieldset class="bv__bloc">
    <legend>1. Contrôle continu : vos moyennes annuelles de 3e <span>(40 % de la note)</span></legend>
    <div class="bv__grille">${MATIERES.map(([k, lib, v]) => champ(`data-cc="${k}"`, `bv-cc-${k}`, lib, v)).join('')}</div>
    <div class="bv__option">
      <label class="bv__champ" for="bv-option-type"><span class="bv__lib">Option suivie en 3e</span>
        <select id="bv-option-type" data-option-type>${OPTIONS.map(([v, l]) => `<option value="${v}">${e(l)}</option>`).join('')}</select></label>
      <label class="bv__champ" for="bv-option"><span class="bv__lib">Moyenne annuelle de l’option</span><input id="bv-option" type="text" inputmode="decimal" autocomplete="off" data-option value="" disabled></label>
    </div>
    <p class="bv__sous">Contrôle continu : <strong data-res-cc>${fmt(cc)}${NBSP}/${NBSP}20</strong></p>
  </fieldset>
  <fieldset class="bv__bloc">
    <legend>2. Épreuves terminales : vos notes <span>(60 % de la note)</span></legend>
    <div class="bv__grille">${EPREUVES.map(([k, lib, c, v]) => champ(`data-ep="${k}"`, `bv-ep-${k}`, lib, v, ` <em>coef.${NBSP}${virgule(c)}</em>`)).join('')}</div>
    <p class="bv__sous">Moyenne des épreuves : <strong data-res-ep>${fmt(ep)}${NBSP}/${NBSP}20</strong></p>
  </fieldset>
  <div class="bv__resultat" aria-live="polite">
    <p class="otc__res-lib">Votre note finale au brevet</p>
    <p class="bv__note" data-res-note>${fmt(n)}${NBSP}/${NBSP}20</p>
    <p class="bv__verdict" data-res-verdict>${verdict(n)}</p>
    <p class="bv__calc" data-res-calc>0,4 × ${fmt(cc)} + 0,6 × ${fmt(ep)} = ${fmt(n)}</p>
  </div>
  <div class="bv__viser">
    <p class="bv__viser-titre">Note à obtenir aux épreuves, avec ce contrôle continu</p>
    <ul data-res-viser>${lignesAViser(cc)}</ul>
  </div>
</section>`
}
