/* Calculateur de pourcentage : x % d'un nombre, quel pourcentage,
 * augmenter ou diminuer de x %, taux d'évolution. */
(function () {
  'use strict'
  var C = window.OTC
  var f = C.fmt
  var eg = C.egal
  var M = C.MOINS

  C.outil('pourcentage', {
    de: function (v) {
      if (isNaN(v.t) || isNaN(v.n)) return null
      var r = v.n * v.t / 100
      return { res: f(r), calc: f(v.t) + ' % de ' + f(v.n) + ' = ' + f(v.n) + ' × ' + f(v.t) + ' ÷ 100 ' + eg(r) }
    },
    quel: function (v) {
      if (isNaN(v.p) || isNaN(v.n)) return null
      if (v.n === 0) return { erreur: 'Le total ne peut pas être égal à 0.' }
      var r = v.p / v.n * 100
      return { res: f(r, 2) + ' %', calc: f(v.p) + ' ÷ ' + f(v.n) + ' × 100 ' + eg(r, 2) + ' %' }
    },
    varier: function (v) {
      if (isNaN(v.n) || isNaN(v.t)) return null
      var s = v.sens === 'baisse' ? -1 : 1
      var cm = 1 + s * v.t / 100
      var r = v.n * cm
      return {
        res: f(r),
        calc: [
          'Coefficient multiplicateur : 1 ' + (s > 0 ? '+' : M) + ' ' + f(v.t) + ' ÷ 100 ' + eg(cm),
          f(v.n) + ' × ' + f(cm) + ' ' + eg(r)
        ]
      }
    },
    taux: function (v) {
      if (isNaN(v.a) || isNaN(v.b)) return null
      if (v.a === 0) return { erreur: 'La valeur de départ ne peut pas être égale à 0.' }
      var r = (v.b - v.a) / v.a * 100
      return {
        res: (r > 0 ? '+' : '') + f(r, 2) + ' %',
        calc: '(' + f(v.b) + ' ' + M + ' ' + f(v.a) + ') ÷ ' + f(v.a) + ' × 100 ' + eg(r, 2) + ' %'
      }
    }
  })
})()
