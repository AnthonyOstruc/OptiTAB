/* Simulateur de note du brevet : calcul à chaque saisie.
 * Mêmes formules que scripts/ressources/brevet.mjs (règles officielles depuis la
 * session 2026). window.OTBrevet expose le calcul : contenu/methodes/simulateur-brevet/
 * generer.py le compare à sa propre version Python sur des milliers de cas. */
(function () {
  'use strict'
  var NBSP = String.fromCharCode(160)
  var COEF = { francais: 2, maths: 2, hg: 1.5, emc: 0.5, sciences: 2, oral: 2 }
  var SEUILS = [[10, 'obtenir le brevet'], [12, 'la mention assez bien'], [14, 'la mention bien'], [16, 'la mention très bien'], [18, 'les félicitations du jury']]

  function controleContinu(moyennes, option) {
    var n = 0, somme = 0
    for (var i = 0; i < moyennes.length; i++) if (moyennes[i] != null) { n++; somme += moyennes[i] }
    if (!n) return null
    var bonus = option != null && option > 10 ? option - 10 : 0
    return Math.min(20, (somme + bonus) / n)
  }
  function moyenneEpreuves(notes) {
    var s = 0
    for (var k in COEF) { if (notes[k] == null) return null; s += COEF[k] * notes[k] }
    return s / 10
  }
  function noteFinale(cc, ep) { return 0.4 * cc + 0.6 * ep }
  function mention(n) {
    return n >= 18 ? 'très bien avec les félicitations du jury' : n >= 16 ? 'très bien' : n >= 14 ? 'bien' : n >= 12 ? 'assez bien' : ''
  }
  function aViser(cc, seuil) { return (seuil - 0.4 * cc) / 0.6 }
  // Note finale au centième (le verdict suit le nombre affiché) ; note à viser au centième supérieur.
  function arrondi(x) { return Math.round(x * 100 + 1e-7) / 100 }
  function plafond(x) { return Math.ceil(x * 100 - 1e-7) / 100 }

  var calcul = { controleContinu: controleContinu, moyenneEpreuves: moyenneEpreuves, noteFinale: noteFinale, mention: mention, aViser: aViser, arrondi: arrondi, plafond: plafond }
  if (typeof window !== 'undefined') window.OTBrevet = calcul

  var s = typeof document !== 'undefined' && document.querySelector('[data-outil="brevet"]')
  if (!s) return

  function fmt(x) { return x.toFixed(2).replace('.', ',') }
  function sur20(x) { return fmt(x) + NBSP + '/' + NBSP + '20' }
  // Lecture d'une note : vide → null ; « 13,5 » accepté ; hors de 0..20 → NaN.
  function lire(input) {
    var v = String(input.value).replace(/\s/g, '').replace(',', '.')
    if (v === '') return null
    var x = /^\d+(\.\d+)?$/.test(v) ? parseFloat(v) : NaN
    var ok = !isNaN(x) && x <= 20
    input.classList.toggle('is-erreur', !ok)
    input.setAttribute('aria-invalid', ok ? 'false' : 'true')
    return ok ? x : NaN
  }

  var typeOption = s.querySelector('[data-option-type]')
  var champOption = s.querySelector('[data-option]')

  function calculer() {
    var invalide = false
    var moyennes = Array.prototype.map.call(s.querySelectorAll('[data-cc]'), function (i) {
      var x = lire(i); if (x !== x) invalide = true; return x
    })
    var opt = null
    if (typeOption.value) { opt = lire(champOption); if (opt !== opt) invalide = true }
    var notes = {}
    Array.prototype.forEach.call(s.querySelectorAll('[data-ep]'), function (i) {
      var x = lire(i); if (x !== x) invalide = true; notes[i.getAttribute('data-ep')] = x
    })
    var resCc = s.querySelector('[data-res-cc]'), resEp = s.querySelector('[data-res-ep]')
    var resNote = s.querySelector('[data-res-note]'), resVerdict = s.querySelector('[data-res-verdict]')
    var resCalc = s.querySelector('[data-res-calc]'), resViser = s.querySelector('[data-res-viser]')
    if (invalide) {
      resVerdict.textContent = 'Vérifiez les notes en rouge : chaque note doit être comprise entre 0 et 20.'
      return
    }
    var cc = controleContinu(moyennes, opt)
    var ep = moyenneEpreuves(notes)
    resCc.textContent = cc == null ? '—' : sur20(cc)
    resEp.textContent = ep == null ? 'à compléter' : sur20(ep)
    resViser.innerHTML = cc == null ? '' : SEUILS.map(function (x) {
      var v = aViser(cc, x[0])
      var val = v <= 0 ? 'déjà assuré' : v > 20 ? 'hors d’atteinte' : sur20(plafond(v))
      return '<li><span>Pour ' + x[1] + ' (' + x[0] + '/20)</span><strong>' + val + '</strong></li>'
    }).join('')
    if (cc == null || ep == null) {
      resNote.textContent = '—'
      resVerdict.textContent = cc == null ? 'Entrez au moins une moyenne de contrôle continu.' : 'Entrez les six notes d’épreuves pour obtenir la note finale.'
      resCalc.textContent = ''
      return
    }
    var n = arrondi(noteFinale(cc, ep))
    resNote.textContent = sur20(n)
    var m = mention(n)
    resVerdict.textContent = n < 10
      ? 'Non admis : il manque ' + fmt(10 - n) + NBSP + 'point' + (10 - n >= 2 ? 's' : '') + ' sur 20.'
      : (m ? 'Admis avec la mention ' + m + '.' : 'Admis, sans mention.')
    resVerdict.className = 'bv__verdict ' + (n < 10 ? 'is-non' : 'is-oui')
    resCalc.textContent = '0,4 × ' + fmt(cc) + ' + 0,6 × ' + fmt(ep) + ' = ' + fmt(n)
  }

  typeOption.addEventListener('change', function () {
    champOption.disabled = !typeOption.value
    if (!typeOption.value) { champOption.value = ''; champOption.classList.remove('is-erreur') }
    calculer()
  })
  s.addEventListener('input', calculer)
  calculer()
})()
