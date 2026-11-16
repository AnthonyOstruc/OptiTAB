/* Diviseurs d'un nombre : critères de divisibilité, liste des diviseurs,
 * nombre premier, décomposition en facteurs premiers. */
(function () {
  'use strict'
  var C = window.OTC
  var MAX = 1e12

  function sommeChiffres(n) { return String(n).split('').reduce(function (s, c) { return s + +c }, 0) }

  function facteurs(n) {
    var out = [], d = 2
    while (d * d <= n) {
      var k = 0
      while (n % d === 0) { n /= d; k++ }
      if (k) out.push([d, k])
      d += d === 2 ? 1 : 2
    }
    if (n > 1) out.push([n, 1])
    return out
  }

  function diviseurs(fac) {
    var l = [1]
    fac.forEach(function (pk) {
      var nl = []
      l.forEach(function (x) { for (var i = 0, p = 1; i <= pk[1]; i++, p *= pk[0]) nl.push(x * p) })
      l = nl
    })
    return l.sort(function (a, b) { return a - b })
  }

  var SUP = { 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' }
  function puiss(k) { return String(k).split('').map(function (c) { return SUP[c] }).join('') }

  C.outil('diviseurs', {
    nombre: function (v) {
      var n = v.n
      if (isNaN(n)) return null
      if (n !== Math.floor(n) || n < 1) return { erreur: 'Saisissez un nombre entier supérieur ou égal à 1.' }
      if (n > MAX) return { erreur: 'Saisissez un nombre inférieur ou égal à 1 000 000 000 000.' }
      var s = sommeChiffres(n), u = n % 10, deux = n % 100
      var crit = [
        ['2', n % 2 === 0, 'chiffre des unités ' + u + (n % 2 === 0 ? ' pair' : ' impair')],
        ['3', s % 3 === 0, 'somme des chiffres ' + s + (s % 3 === 0 ? ', multiple de 3' : ', pas multiple de 3')],
        ['4', n % 4 === 0, 'nombre formé par les deux derniers chiffres : ' + deux + (n % 4 === 0 ? ', multiple de 4' : ', pas multiple de 4')],
        ['5', n % 5 === 0, 'chiffre des unités ' + u],
        ['9', s % 9 === 0, 'somme des chiffres ' + s + (s % 9 === 0 ? ', multiple de 9' : ', pas multiple de 9')],
        ['10', n % 10 === 0, 'chiffre des unités ' + u]
      ]
      var fac = facteurs(n)
      var premier = n > 1 && fac.length === 1 && fac[0][1] === 1
      var lignes = crit.map(function (c) { return (c[1] ? '✓ divisible par ' : '✗ pas divisible par ') + c[0] + ' (' + c[2] + ')' })
      var divs = diviseurs(fac)
      lignes.push('')
      lignes.push(divs.length + ' diviseur' + (divs.length > 1 ? 's' : '') + ' : ' + (divs.length <= 200 ? divs.map(function (d) { return C.fmt(d, 0) }).join(' ; ') : divs.slice(0, 200).map(function (d) { return C.fmt(d, 0) }).join(' ; ') + ' …'))
      if (n > 1) lignes.push('Décomposition en facteurs premiers : ' + C.fmt(n, 0) + ' = ' + fac.map(function (pk) { return pk[0] + (pk[1] > 1 ? puiss(pk[1]) : '') }).join(' × '))
      return { res: n === 1 ? '1 n’est pas premier' : premier ? C.fmt(n, 0) + ' est premier' : C.fmt(n, 0) + ' n’est pas premier', calc: lignes }
    }
  })
})()
