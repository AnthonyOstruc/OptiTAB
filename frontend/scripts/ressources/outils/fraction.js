/* Calculateur de fractions : simplifier, additionner, soustraire,
 * multiplier, diviser (entiers, résultats exacts et simplifiés). */
(function () {
  'use strict'
  var C = window.OTC
  var M = C.MOINS

  function pgcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t } return a }
  function entier(x) { return !isNaN(x) && Math.floor(x) === x && Math.abs(x) <= 1e9 }
  function ecr(n, d) {
    if (d < 0) { n = -n; d = -d }
    var s = (n < 0 ? M : '') + Math.abs(n)
    return d === 1 ? s : s + '/' + d
  }
  function simplifier(n, d) {
    if (d < 0) { n = -n; d = -d }
    var g = pgcd(n, d) || 1
    return { n: n / g, d: d / g, g: g }
  }
  function lignesSimplif(n, d) {
    var s = simplifier(n, d)
    var out = []
    if (s.g > 1) out.push(ecr(n, d) + ' = ' + ecr(s.n * s.g, s.d * s.g) + ' : on divise le numérateur et le dénominateur par ' + s.g + ', d’où ' + ecr(s.n, s.d))
    if (s.d !== 1 && Math.abs(s.n) > s.d) {
      var q = Math.trunc(s.n / s.d)
      out.push('Partie entière : ' + ecr(s.n, s.d) + ' = ' + (q < 0 ? M : '') + Math.abs(q) + ' ' + (s.n < 0 ? M : '+') + ' ' + ecr(Math.abs(s.n - q * s.d), s.d))
    }
    if (s.d !== 1) out.push('Valeur décimale ' + C.egal(s.n / s.d, 4))
    return { s: s, lignes: out }
  }

  C.outil('fraction', {
    simplifier: function (v) {
      if (!entier(v.a) || !entier(v.b)) return v.a === v.a && v.b === v.b ? { erreur: 'Utilisez des nombres entiers.' } : null
      if (v.b === 0) return { erreur: 'Le dénominateur ne peut pas être égal à 0.' }
      var r = lignesSimplif(v.a, v.b)
      if (r.s.g === 1 && r.s.d === Math.abs(v.b)) r.lignes.unshift(ecr(v.a, v.b) + ' est déjà irréductible : ' + Math.abs(v.a) + ' et ' + Math.abs(v.b) + ' n’ont pas de diviseur commun autre que 1.')
      return { res: ecr(r.s.n, r.s.d), calc: r.lignes }
    },
    operation: function (v) {
      var x = [v.a, v.b, v.c, v.d]
      if (x.some(function (t) { return isNaN(t) })) return null
      if (!x.every(entier)) return { erreur: 'Utilisez des nombres entiers.' }
      if (v.b === 0 || v.d === 0) return { erreur: 'Un dénominateur ne peut pas être égal à 0.' }
      var a = v.a, b = v.b, c = v.c, d = v.d, op = v.op, n, den, etapes = []
      var A = ecr(a, b), B = ecr(c, d)
      if (op === '+' || op === '-') {
        var m = Math.abs(b * d) / pgcd(b, d)
        var ka = m / b, kc = m / d
        var sgn = op === '+' ? '+' : M
        etapes.push('Même dénominateur ' + m + ' : ' + A + ' = ' + ecr(a * ka, m) + ' et ' + B + ' = ' + ecr(c * kc, m))
        n = op === '+' ? a * ka + c * kc : a * ka - c * kc
        den = m
        etapes.push(ecr(a * ka, m) + ' ' + sgn + ' ' + ecr(c * kc, m) + ' = ' + ecr(n, den))
      } else if (op === '*') {
        n = a * c; den = b * d
        etapes.push(A + ' × ' + B + ' = (' + a + ' × ' + c + ') / (' + b + ' × ' + d + ') = ' + ecr(n, den))
      } else {
        if (c === 0) return { erreur: 'On ne peut pas diviser par 0.' }
        n = a * d; den = b * c
        etapes.push('Diviser par ' + B + ', c’est multiplier par son inverse ' + ecr(d, c))
        etapes.push(A + ' × ' + ecr(d, c) + ' = ' + ecr(n, den))
      }
      var r = lignesSimplif(n, den)
      return { res: ecr(r.s.n, r.s.d), calc: etapes.concat(r.lignes) }
    }
  })
})()
