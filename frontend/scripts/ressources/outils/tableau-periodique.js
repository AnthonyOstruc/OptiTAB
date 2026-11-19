/* Tableau périodique interactif : fiche de l'élément touché.
 * Les données de chaque élément sont dans les attributs data-* de son bouton
 * (écrits à la construction par tableau-periodique.mjs). La fiche reprend la
 * même mise en page que celle écrite dans la page pour le fer. */
(function () {
  'use strict'
  var s = document.querySelector('[data-outil="tableau-periodique"]')
  if (!s) return
  var fiche = s.querySelector('[data-fiche]')
  var NBSP = String.fromCharCode(160)

  function esc(t) {
    return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] })
  }

  function ligne(terme, valeur) {
    return valeur === '' || valeur == null ? '' : '<div><dt>' + terme + '</dt><dd>' + valeur + '</dd></div>'
  }

  function famille(b) {
    var m = b.className.match(/tp--([a-z-]+)/)
    return m ? m[1] : ''
  }

  function montrer(b) {
    var d = b.dataset
    var masse = d.m.charAt(0) === '[' ? esc(d.m) + NBSP + '(élément radioactif)' : esc(d.m) + NBSP + 'g/mol'
    fiche.innerHTML = '<div class="tp__fiche-tete tp--' + famille(b) + '">'
      + '<span class="tp__fiche-z">' + esc(d.z) + '</span><span class="tp__fiche-s">' + esc(d.s) + '</span></div>'
      + '<div class="tp__fiche-corps"><p class="tp__fiche-nom">' + esc(d.n) + '</p><dl class="tp__fiche-dl">'
      + ligne('Numéro atomique', 'Z = ' + esc(d.z))
      + ligne('Masse molaire', masse)
      + ligne('Famille', esc(d.f))
      + ligne('Période', esc(d.p))
      + ligne('Groupe', esc(d.g))
      + ligne('Bloc', esc(d.b))
      + ligne('Électronégativité', d.en ? esc(d.en) : '')
      + ligne('Configuration électronique', d.c ? esc(d.c).replace(/(\d[spdf])(\d+)/g, '$1<sup>$2</sup>') : '')
      + ligne('Électrons de valence', d.v ? esc(d.v) : '')
      + '</dl></div>'
    var avant = s.querySelector('.tp__el[aria-pressed="true"]')
    if (avant) avant.setAttribute('aria-pressed', 'false')
    b.setAttribute('aria-pressed', 'true')
    // Sur téléphone, la fiche est sous le tableau : on la montre si elle est hors de l'écran.
    var r = fiche.getBoundingClientRect()
    if (r.top > window.innerHeight - 80) fiche.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
  }

  s.addEventListener('click', function (ev) {
    var b = ev.target.closest ? ev.target.closest('.tp__el') : null
    if (b) montrer(b)
  })
})()
