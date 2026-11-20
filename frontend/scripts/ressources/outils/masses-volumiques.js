/* Masse volumique des matériaux : recherche et calcul de masse et de poids.
 * Données recopiées dans la page depuis materiaux.json (voir masses-volumiques.mjs).
 * Matériau à masse volumique (kg/m³) : masse = ρ × V, poids = masse × g.
 * Matériau de l'Eurocode (poids volumique en kN/m³) : poids = γ × V, masse = poids ÷ g. */
(function () {
  'use strict'
  var NBSP = String.fromCharCode(160)
  var NNBSP = String.fromCharCode(0x202f)

  function nombre(x, n) {
    return Number(x.toPrecision(n)).toLocaleString('fr-FR', { maximumFractionDigits: 6 }).replace(/[\s  ]/g, NNBSP)
  }
  function plage(v, f) { return v[0] === v[1] ? f(v[0]) : f(v[0]) + ' à ' + f(v[1]) }
  function valeur(m) {
    return m.rho ? plage(m.rho, function (x) { return nombre(x, 4) }) + NBSP + 'kg/m³'
      : plage(m.gamma, function (x) { return nombre(x, 3) }) + NBSP + 'kN/m³'
  }
  // Masse lisible : g, kg ou tonnes.
  function masse(kg) {
    if (kg >= 1000) return nombre(kg, 4) + NBSP + 'kg (' + nombre(kg / 1000, 4) + NBSP + 't)'
    if (kg >= 1) return nombre(kg, 4) + NBSP + 'kg'
    if (kg >= 0.001) return nombre(kg * 1000, 4) + NBSP + 'g'
    return nombre(kg * 1e6, 4) + NBSP + 'mg'
  }
  function poids(n) { return n >= 1000 ? nombre(n / 1000, 3) + NBSP + 'kN' : nombre(n, 3) + NBSP + 'N' }
  function sansAccents(s) { return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase() }
  function lire(s) {
    s = String(s).replace(/[\s  ]/g, '').replace(',', '.')
    if (!/^(\d+\.?\d*|\.\d+)$/.test(s)) return NaN
    return parseFloat(s)
  }

  var s = typeof document !== 'undefined' && document.querySelector('[data-outil="masses-volumiques"]')
  if (!s) return
  var D = JSON.parse(s.querySelector('[data-mv]').textContent)
  var G = D.g
  var parId = {}
  var nomCat = {}
  D.materiaux.forEach(function (m) { parId[m.id] = m; m.cle = sansAccents(m.nom) })
  D.categories.forEach(function (c) { nomCat[c.id] = c.nom })

  var q = s.querySelector('[data-q]')
  var liste = s.querySelector('[data-resultats]')
  var compte = s.querySelector('[data-compte]')
  var selM = s.querySelector('[data-materiau]')
  var champV = s.querySelector('[data-volume]')
  var selU = s.querySelector('[data-unite]')
  var lib = s.querySelector('.otc__res-lib')
  var res = s.querySelector('[data-res]')
  var calc = s.querySelector('[data-calc]')
  var populaires = liste.innerHTML

  function echap(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;') }
  function ligne(m) {
    return '<li><button type="button" data-choisir="' + echap(m.id) + '"><strong>' + echap(m.nom) + '</strong> <span class="mv__val">' +
      echap(valeur(m)) + '</span> <span class="mv__cat">' + echap(nomCat[m.cat]) + '</span></button></li>'
  }

  function chercher() {
    var t = sansAccents(q.value.trim())
    if (!t) { liste.innerHTML = populaires; compte.textContent = 'Recherches fréquentes :'; return }
    var mots = t.split(/\s+/)
    var trouves = D.materiaux.filter(function (m) {
      var texte = m.cle + ' ' + sansAccents(nomCat[m.cat])
      return mots.every(function (w) { return texte.indexOf(w) !== -1 })
    })
    compte.textContent = trouves.length ? trouves.length + ' résultat' + (trouves.length > 1 ? 's' : '') + ' :' : 'Aucun matériau trouvé. Essayez un autre mot, par exemple « métal » ou « bois ».'
    liste.innerHTML = trouves.slice(0, 12).map(ligne).join('')
  }

  function calculer() {
    var m = parId[selM.value]
    var brut = champV.value.trim()
    var v = lire(brut)
    var faux = brut !== '' && isNaN(v)
    champV.classList.toggle('is-faux', faux)
    champV.setAttribute('aria-invalid', faux ? 'true' : 'false')
    s.classList.toggle('is-vide', isNaN(v))
    var unite = selU.options[selU.selectedIndex].text.split(' ')[0]
    lib.textContent = (isNaN(v) ? 'Résultat' : 'Pour ' + nombre(v, 6) + NBSP + unite + ' de ' + m.nom)
    if (isNaN(v)) { res.textContent = '—'; calc.textContent = 'Saisissez un volume (la virgule est acceptée).'; return }
    var vol = v * parseFloat(selU.value)
    var lignes
    if (m.rho) {
      var m0 = m.rho[0] * vol
      var m1 = m.rho[1] * vol
      res.textContent = m0 === m1 ? masse(m0) : masse(m0) + ' à ' + masse(m1)
      lignes = ['Masse volumique : ' + valeur(m) + ', densité ' + plage(m.rho, function (x) { return nombre(x / 1000, 3) }) + '.',
        'Poids : ' + (m0 === m1 ? poids(m0 * G) : poids(m0 * G) + ' à ' + poids(m1 * G)) + ' (avec g = 9,81' + NBSP + 'N/kg).']
    } else {
      var p0 = m.gamma[0] * 1000 * vol
      var p1 = m.gamma[1] * 1000 * vol
      res.textContent = p0 === p1 ? poids(p0) : poids(p0) + ' à ' + poids(p1)
      lignes = ['Poids volumique de l’Eurocode : ' + valeur(m) + '.',
        'Masse correspondante : environ ' + (p0 === p1 ? masse(p0 / G) : masse(p0 / G) + ' à ' + masse(p1 / G)) + ' (poids ÷ 9,81).']
    }
    calc.textContent = lignes.join('\n')
  }

  q.addEventListener('input', chercher)
  liste.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-choisir]')
    if (!b) return
    selM.value = b.getAttribute('data-choisir')
    calculer()
    champV.focus()
  })
  selM.addEventListener('change', calculer)
  selU.addEventListener('change', calculer)
  champV.addEventListener('input', calculer)
  if (typeof window !== 'undefined') window.OTMasseVol = { masse: masse, poids: poids, valeur: valeur, nombre: nombre }
  calculer()
})()
