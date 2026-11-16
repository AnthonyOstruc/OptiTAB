/* Calculateurs des ressources gratuites : fonctions communes.
 * Une page déclare un outil (<section data-outil="nom">) ; son fichier
 * outils/<nom>.js appelle OTC.outil(nom, modes) avec une fonction de calcul
 * par onglet. Chaque fonction reçoit les valeurs saisies (nombres déjà lus,
 * virgule acceptée ; listes et menus tels quels) et renvoie
 * { res, calc } ou { erreur } ou null (saisie incomplète). */
(function () {
  'use strict'
  var MOINS = '−'

  function lire(s) {
    s = String(s).replace(/[\s  ]/g, '').replace(',', '.').replace(MOINS, '-')
    if (!/^[-+]?(\d+\.?\d*|\.\d+)$/.test(s)) return NaN
    return parseFloat(s)
  }

  function arrondi(x, n) {
    var p = Math.pow(10, n)
    return Math.round(x * p) / p
  }

  // Écriture française : virgule, espace fine des milliers, vrai signe moins.
  function fmt(x, n) {
    if (!isFinite(x)) return '—'
    n = n == null ? 4 : n
    var r = arrondi(x, n)
    if (r === 0) r = 0
    var t = Math.abs(r).toLocaleString('fr-FR', { maximumFractionDigits: n })
    return (r < 0 ? MOINS : '') + t
  }

  // « = 12 » si la valeur affichée est exacte, « ≈ 3,3333 » sinon.
  function egal(x, n) {
    n = n == null ? 4 : n
    var exact = Math.abs(arrondi(x, n) - x) <= 1e-9 * Math.max(1, Math.abs(x))
    return (exact ? '= ' : '≈ ') + fmt(x, n)
  }

  function outil(nom, modes) {
    var s = document.querySelector('[data-outil="' + nom + '"]')
    if (!s) return
    var res = s.querySelector('[data-res]')
    var calc = s.querySelector('[data-calc]')
    var onglets = [].slice.call(s.querySelectorAll('[data-mode]'))
    var panneaux = [].slice.call(s.querySelectorAll('[data-panneau]'))
    var mode = null

    function valeurs(p) {
      var v = {}
      ;[].forEach.call(p.querySelectorAll('[data-k]'), function (champ) {
        var k = champ.getAttribute('data-k')
        if (champ.tagName === 'SELECT' || champ.hasAttribute('data-texte')) {
          v[k] = champ.value
          return
        }
        var brut = champ.value.trim()
        var x = lire(brut)
        v[k] = x
        champ.classList.toggle('is-faux', brut !== '' && isNaN(x))
      })
      return v
    }

    function maj() {
      var p = s.querySelector('[data-panneau="' + mode + '"]')
      var r = null
      try { r = modes[mode](valeurs(p)) } catch (e) { r = null }
      s.classList.toggle('is-vide', !r || !!r.erreur)
      if (!r) { res.textContent = '—'; calc.textContent = 'Saisissez des nombres (la virgule est acceptée).'; return }
      if (r.erreur) { res.textContent = '—'; calc.textContent = r.erreur; return }
      res.textContent = r.res
      calc.textContent = [].concat(r.calc || []).join('\n')
    }

    function choisir(m, focus) {
      mode = m
      onglets.forEach(function (t) {
        var actif = t.getAttribute('data-mode') === m
        t.setAttribute('aria-selected', actif ? 'true' : 'false')
        t.tabIndex = actif ? 0 : -1
        if (actif && focus) t.focus()
      })
      panneaux.forEach(function (p) { p.hidden = p.getAttribute('data-panneau') !== m })
      maj()
    }

    onglets.forEach(function (t, i) {
      t.addEventListener('click', function () { choisir(t.getAttribute('data-mode')) })
      t.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0
        if (!d) return
        e.preventDefault()
        var n = onglets[(i + d + onglets.length) % onglets.length]
        choisir(n.getAttribute('data-mode'), true)
      })
    })
    s.addEventListener('input', maj)
    s.addEventListener('change', maj)
    choisir(onglets.length ? onglets[0].getAttribute('data-mode') : panneaux[0].getAttribute('data-panneau'))
  }

  // Sur téléphone et tablette, le sommaire passe au-dessus du texte : on le
  // replie pour que le calculateur soit visible sans faire défiler.
  if (window.matchMedia && window.matchMedia('(max-width: 960px)').matches) {
    var sommaire = document.querySelector('.rg-toc__box')
    if (sommaire) sommaire.removeAttribute('open')
  }

  window.OTC = { lire: lire, fmt: fmt, egal: egal, outil: outil, MOINS: MOINS }
})()
