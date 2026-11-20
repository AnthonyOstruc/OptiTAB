/* Convertisseur d'unités : conversion à chaque saisie.
 * Les unités viennent de scripts/ressources/convertisseur.mjs (recopiées en JSON
 * dans la page) ; le calcul, l'écriture des nombres et l'explication sont les
 * mêmes que dans ce module (contenu/methodes/convertisseur-d-unites/generer.py
 * vérifie que les deux donnent les mêmes résultats). window.OTConv expose le calcul. */
(function () {
  'use strict'
  var NBSP = String.fromCharCode(160)
  var NNBSP = String.fromCharCode(0x202f)
  var SUP = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' }
  var FORMULES_T = {
    'C>F': '°F = °C × 1,8 + 32', 'F>C': '°C = (°F − 32) ÷ 1,8', 'C>K': 'K = °C + 273,15', 'K>C': '°C = K − 273,15',
    'F>K': 'K = (°F − 32) ÷ 1,8 + 273,15', 'K>F': '°F = (K − 273,15) × 1,8 + 32'
  }

  function versRef(u, x) { return u.length > 4 ? u[3] * x + u[4] : u[3] * x }
  function depuisRef(u, y) { return u.length > 4 ? (y - u[4]) / u[3] : y / u[3] }
  function unite(g, code) { for (var i = 0; i < g.unites.length; i++) if (g.unites[i][0] === code) return g.unites[i] }
  function convertir(g, de, vers, x) { return depuisRef(unite(g, vers), versRef(unite(g, de), x)) }

  function nombre(x, n) {
    n = n || 8
    if (x === 0) return '0'
    if (!isFinite(x)) return '—'
    var a = Math.abs(x)
    if (a >= 1e12 || a < 1e-6) {
      var p = x.toExponential(n - 1).split('e')
      var mant = String(Number(p[0])).replace('.', ',').replace('-', '−')
      return mant + NBSP + '×' + NBSP + '10' + String(Number(p[1])).split('').map(function (c) { return SUP[c] }).join('')
    }
    var s = Number(x.toPrecision(n)).toLocaleString('fr-FR', { maximumFractionDigits: 15, useGrouping: true })
    return s.replace(/[\s  ]/g, NNBSP).replace('-', '−')
  }
  function exact(x, n) {
    n = n || 8
    var a = Math.abs(x)
    var r = a >= 1e12 || a < 1e-6 ? Number(x.toExponential(n - 1)) : Number(x.toPrecision(n))
    return Math.abs(r - x) <= 1e-14 * Math.max(Math.abs(x), 1e-300)
  }
  function avec(n, s) { return s === '°' || s === '′' || s === '″' ? n + s : n + NBSP + s }
  function explication(g, de, vers) {
    if (de === vers) return 'Même unité : la valeur ne change pas.'
    if (g.affine) return 'Formule : ' + FORMULES_T[de + '>' + vers] + '.'
    var k = convertir(g, de, vers, 1)
    var sd = unite(g, de)[2]
    var sv = unite(g, vers)[2]
    if (k >= 1) return avec('1', sd) + ' ' + (exact(k) ? '=' : '≈') + ' ' + avec(nombre(k), sv) + ' : on multiplie par ' + nombre(k) + '.'
    var inv = 1 / k
    return avec('1', sv) + ' ' + (exact(inv) ? '=' : '≈') + ' ' + avec(nombre(inv), sd) + ' : on divise par ' + nombre(inv) + '.'
  }
  // Lecture d'une valeur : « 2,5 », « 1 500 », « −40 », « 3e8 » ; NaN si ce n'est pas un nombre.
  function lire(s) {
    s = String(s).replace(/[\s  ]/g, '').replace(',', '.').replace('−', '-')
    if (!/^[-+]?(\d+\.?\d*|\.\d+)(e[-+]?\d+)?$/i.test(s)) return NaN
    return parseFloat(s)
  }

  var calcul = { convertir: convertir, nombre: nombre, exact: exact, explication: explication, lire: lire }
  if (typeof window !== 'undefined') window.OTConv = calcul

  var s = typeof document !== 'undefined' && document.querySelector('[data-outil="convertisseur"]')
  if (!s) return
  var GRANDEURS = JSON.parse(s.querySelector('[data-unites]').textContent)
  var G = {}
  GRANDEURS.forEach(function (g) { G[g.id] = g })

  var selG = s.querySelector('[data-grandeur]')
  var champ = s.querySelector('[data-valeur]')
  var selDe = s.querySelector('[data-de]')
  var selVers = s.querySelector('[data-vers]')
  var res = s.querySelector('[data-res]')
  var calc = s.querySelector('[data-calc]')
  var liste = s.querySelector('[data-tout]')
  var titreListe = s.querySelector('[data-tout-titre]')

  function echap(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;') }
  function remplir(sel, g, choisi) {
    sel.innerHTML = g.unites.map(function (u) {
      return '<option value="' + echap(u[0]) + '"' + (u[0] === choisi ? ' selected' : '') + '>' + echap(u[1]) + ' (' + echap(u[2]) + ')</option>'
    }).join('')
  }

  function maj() {
    var g = G[selG.value]
    var brut = champ.value.trim()
    var x = lire(brut)
    var faux = brut !== '' && isNaN(x)
    champ.classList.toggle('is-faux', faux)
    champ.setAttribute('aria-invalid', faux ? 'true' : 'false')
    s.classList.toggle('is-vide', isNaN(x))
    if (isNaN(x)) {
      res.textContent = '—'
      calc.textContent = 'Saisissez un nombre (la virgule est acceptée).'
      liste.innerHTML = ''
      titreListe.textContent = ''
      return
    }
    var de = selDe.value
    var vers = selVers.value
    var ud = unite(g, de)
    if (g.affine && versRef(ud, x) < -1e-9) {
      res.textContent = '—'
      calc.textContent = 'Impossible : c’est en dessous du zéro absolu (0 K = −273,15 °C = −459,67 °F).'
      s.classList.add('is-vide')
      liste.innerHTML = ''
      titreListe.textContent = ''
      return
    }
    var y = convertir(g, de, vers, x)
    res.textContent = avec(nombre(x), ud[2]) + ' ' + (exact(y) ? '=' : '≈') + ' ' + avec(nombre(y), unite(g, vers)[2])
    calc.textContent = explication(g, de, vers)
    titreListe.textContent = avec(nombre(x), ud[2]) + ' dans toutes les unités'
    liste.innerHTML = g.unites.map(function (u) {
      return '<li><button type="button" data-vers-unite="' + echap(u[0]) + '"' + (u[0] === vers ? ' aria-current="true"' : '') + '><strong>' +
        nombre(convertir(g, de, u[0], x)) + '</strong> <span>' + echap(u[1]) + ' (' + echap(u[2]) + ')</span></button></li>'
    }).join('')
  }

  function choisirGrandeur(id, garderValeur) {
    var g = G[id]
    if (!g) return
    selG.value = id
    remplir(selDe, g, g.de)
    remplir(selVers, g, g.vers)
    if (!garderValeur || isNaN(lire(champ.value))) champ.value = nombre(g.valeur)
    maj()
  }

  selG.addEventListener('change', function () { choisirGrandeur(selG.value, true) })
  selDe.addEventListener('change', maj)
  selVers.addEventListener('change', maj)
  champ.addEventListener('input', maj)
  s.querySelector('[data-inverser]').addEventListener('click', function () {
    var d = selDe.value
    selDe.value = selVers.value
    selVers.value = d
    maj()
  })
  liste.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-vers-unite]')
    if (!b) return
    selVers.value = b.getAttribute('data-vers-unite')
    maj()
  })
  // Lien direct vers une grandeur : …/convertisseur-d-unites/#pression
  function depuisAncre() {
    var id = decodeURIComponent((location.hash || '').slice(1))
    if (G[id]) {
      choisirGrandeur(id, false)
      s.scrollIntoView({ block: 'start' })
    }
  }
  window.addEventListener('hashchange', depuisAncre)
  if (G[decodeURIComponent((location.hash || '').slice(1))]) depuisAncre()
  else maj()
})()
