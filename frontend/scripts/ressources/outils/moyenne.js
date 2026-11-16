/* Calculateur de moyenne : notes et coefficients, lignes ajoutables. */
(function () {
  'use strict'
  var C = window.OTC
  var f = C.fmt
  var s = document.querySelector('[data-outil="moyenne"]')
  if (!s) return
  var lignes = s.querySelector('[data-lignes]')
  var modele = lignes.querySelector('.otc__ligne').cloneNode(true)
  var res = s.querySelector('[data-res]')
  var calc = s.querySelector('[data-calc]')

  function numeroter() {
    ;[].forEach.call(lignes.querySelectorAll('.otc__ligne'), function (l, i) {
      l.querySelector('[data-num]').textContent = 'Note ' + (i + 1)
      l.querySelector('[data-note]').setAttribute('aria-label', 'Note ' + (i + 1))
      l.querySelector('[data-coef]').setAttribute('aria-label', 'Coefficient de la note ' + (i + 1))
      l.querySelector('[data-suppr]').setAttribute('aria-label', 'Retirer la note ' + (i + 1))
    })
  }

  function maj() {
    var somme = 0, coefs = 0, termes = [], ok = true, n = 0, simple = true
    ;[].forEach.call(lignes.querySelectorAll('.otc__ligne'), function (l) {
      var cn = l.querySelector('[data-note]'), cc = l.querySelector('[data-coef]')
      var bn = cn.value.trim(), bc = cc.value.trim()
      var note = C.lire(bn), coef = bc === '' ? 1 : C.lire(bc)
      cn.classList.toggle('is-faux', bn !== '' && isNaN(note))
      cc.classList.toggle('is-faux', bc !== '' && (isNaN(coef) || coef < 0))
      if (bn === '') return
      if (isNaN(note) || isNaN(coef) || coef < 0) { ok = false; return }
      n++
      if (coef !== 1) simple = false
      somme += note * coef
      coefs += coef
      termes.push(coef === 1 ? f(note) : f(note) + ' × ' + f(coef))
    })
    s.classList.toggle('is-vide', !ok || !n || coefs === 0)
    if (!ok) { res.textContent = '—'; calc.textContent = 'Vérifiez les valeurs en rouge (la virgule est acceptée).'; return }
    if (!n) { res.textContent = '—'; calc.textContent = 'Saisissez au moins une note.'; return }
    if (coefs === 0) { res.textContent = '—'; calc.textContent = 'La somme des coefficients ne peut pas être égale à 0.'; return }
    var m = somme / coefs
    res.textContent = f(m, 2)
    calc.textContent = simple
      ? '(' + termes.join(' + ') + ') ÷ ' + n + ' = ' + f(somme) + ' ÷ ' + n + ' ' + C.egal(m, 2)
      : '(' + termes.join(' + ') + ') ÷ (somme des coefficients ' + f(coefs) + ')\n= ' + f(somme) + ' ÷ ' + f(coefs) + ' ' + C.egal(m, 2)
  }

  s.querySelector('[data-ajout]').addEventListener('click', function () {
    var l = modele.cloneNode(true)
    l.querySelector('[data-note]').value = ''
    l.querySelector('[data-coef]').value = '1'
    lignes.appendChild(l)
    numeroter()
    l.querySelector('[data-note]').focus()
    maj()
  })
  lignes.addEventListener('click', function (e) {
    var b = e.target.closest('[data-suppr]')
    if (!b) return
    var toutes = lignes.querySelectorAll('.otc__ligne')
    if (toutes.length === 1) { toutes[0].querySelector('[data-note]').value = ''; maj(); return }
    b.closest('.otc__ligne').remove()
    numeroter()
    maj()
  })
  s.addEventListener('input', maj)
  numeroter()
  maj()
})()
