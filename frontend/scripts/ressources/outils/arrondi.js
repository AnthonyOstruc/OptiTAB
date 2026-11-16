/* Calculateur d'arrondi : calcul exact sur l'écriture décimale (sans les
 * erreurs des nombres à virgule flottante : 2,675 au centième = 2,68). */
(function () {
  'use strict'
  var C = window.OTC
  var M = C.MOINS
  var NOMS = { '-3': 'au millier', '-2': 'à la centaine', '-1': 'à la dizaine', '0': 'à l’unité', '1': 'au dixième', '2': 'au centième', '3': 'au millième' }

  // « −2,675 » → { neg, N (BigInt des chiffres), e (nombre de décimales) }
  function decimal(s) {
    s = String(s).replace(/[\s  ]/g, '').replace(',', '.').replace(M, '-')
    var m = s.match(/^([-+]?)(\d*)\.?(\d*)$/)
    if (!m || (m[2] + m[3]) === '' || m[3].length > 15 || m[2].length > 15) return null
    return { neg: m[1] === '-', N: BigInt((m[2] || '0') + m[3]), e: m[3].length }
  }

  // BigInt q (unités de 10^-p) → écriture française.
  function ecrire(q, p, neg) {
    var s
    if (p <= 0) s = (q * (10n ** BigInt(-p))).toString()
    else {
      s = q.toString().padStart(p + 1, '0')
      s = s.slice(0, -p) + ',' + s.slice(-p)
    }
    var ent = s.split(',')[0].replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
    s = ent + (s.indexOf(',') >= 0 ? ',' + s.split(',')[1] : '')
    var nul = q === 0n
    return (neg && !nul ? M : '') + s
  }

  C.outil('arrondi', {
    arrondir: function (v) {
      var x = decimal(v.x)
      if (!x) return v.x.trim() === '' ? null : { erreur: 'Écrivez un nombre, par exemple 3,14159.' }
      var p = parseInt(v.p, 10)
      var nom = NOMS[String(p)]
      var dec = x.e - p
      var q, t, r, chiffre
      if (dec <= 0) {
        q = x.N * (10n ** BigInt(-dec)); t = q
        chiffre = null
      } else {
        var div = 10n ** BigInt(dec)
        t = x.N / div
        r = x.N % div
        q = 2n * r >= div ? t + 1n : t
        chiffre = Number(r / (10n ** BigInt(dec - 1)))
      }
      var arr = ecrire(q, p, x.neg), tr = ecrire(t, p, x.neg)
      var lignes = []
      if (chiffre === null) lignes.push('Le nombre n’a pas de chiffre après ce rang : il ne change pas.')
      else lignes.push('Chiffre suivant : ' + chiffre + (chiffre >= 5 ? ' (5 ou plus) : on arrondit au-dessus.' : ' (moins de 5) : on garde le chiffre.'))
      lignes.push('Arrondi ' + nom + ' : ' + arr)
      lignes.push('Troncature ' + nom + ' : ' + tr)
      if (chiffre !== null && r !== 0n) {
        var bas = x.neg ? ecrire(t + 1n, p, true) : tr, haut = x.neg ? tr : ecrire(t + 1n, p, false)
        lignes.push('Encadrement : ' + bas + ' < ' + ecrire(x.N, x.e, x.neg) + ' < ' + haut)
      }
      return { res: arr, calc: lignes }
    }
  })
})()
