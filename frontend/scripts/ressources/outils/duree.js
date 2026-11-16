/* Calculateur de durées : entre deux heures, heure d'arrivée,
 * heures décimales vers heures et minutes, et inversement. */
(function () {
  'use strict'
  var C = window.OTC
  var f = C.fmt

  // « 8 h 45 », « 8h45 », « 8:45 », « 8 h », « 45 min » → minutes (ou NaN).
  function horaire(s) {
    s = String(s).toLowerCase().replace(/[\s  ]/g, '')
    var m = s.match(/^(\d{1,3})(?:h|:)(\d{1,2})?(?:min)?$/) || s.match(/^(\d{1,3})$/)
    if (m) {
      var mn = m[2] ? parseInt(m[2], 10) : 0
      return mn < 60 ? parseInt(m[1], 10) * 60 + mn : NaN
    }
    m = s.match(/^(\d{1,4})min$/)
    return m ? parseInt(m[1], 10) : NaN
  }

  function hm(min, horloge) {
    var h = Math.floor(min / 60), m = Math.round(min - h * 60)
    if (m === 60) { h++; m = 0 }
    if (horloge) return h + ' h ' + (m < 10 ? '0' : '') + m
    if (!h) return m + ' min'
    return h + ' h' + (m ? ' ' + m + ' min' : '')
  }

  C.outil('duree', {
    entre: function (v) {
      var a = horaire(v.a), b = horaire(v.b)
      if (isNaN(a) || isNaN(b)) return null
      if (a >= 1440 || b >= 1440) return { erreur: 'Une heure s’écrit entre 0 h 00 et 23 h 59.' }
      var lendemain = b < a
      var d = (b - a + 1440) % 1440
      return {
        res: hm(d),
        calc: lendemain
          ? ['De ' + hm(a, true) + ' à minuit : ' + hm(1440 - a), 'Puis de minuit à ' + hm(b, true) + ' : ' + hm(b), 'Total : ' + hm(d) + ' (arrivée le lendemain)']
          : ['De ' + hm(a, true) + ' à ' + hm(b, true) + ' : ' + hm(d) + ' (' + d + ' minutes)']
      }
    },
    ajout: function (v) {
      var a = horaire(v.a), d = horaire(v.d)
      if (isNaN(a) || isNaN(d)) return null
      if (a >= 1440) return { erreur: 'L’heure de départ s’écrit entre 0 h 00 et 23 h 59.' }
      var t = a + d, jours = Math.floor(t / 1440)
      return {
        res: hm(t % 1440, true),
        calc: hm(a, true) + ' + ' + hm(d) + ' = ' + hm(t, true) + (jours ? ', soit ' + hm(t % 1440, true) + (jours === 1 ? ' le lendemain' : ' ' + jours + ' jours plus tard') : '')
      }
    },
    versHm: function (v) {
      if (isNaN(v.x) || v.x < 0) return null
      var h = Math.floor(v.x), min = (v.x - h) * 60
      return {
        res: hm(Math.round(v.x * 60)),
        calc: [f(v.x) + ' h = ' + h + ' h + ' + f(v.x - h) + ' h', f(v.x - h) + ' h = ' + f(v.x - h) + ' × 60 min ' + C.egal(min, 2) + ' min']
      }
    },
    versDec: function (v) {
      var t = horaire(v.d)
      if (isNaN(t)) return null
      var h = Math.floor(t / 60), m = t - h * 60
      return {
        res: f(t / 60, 4) + ' h',
        calc: [hm(t) + ' = ' + h + ' h + ' + m + ' min', m + ' min = ' + m + ' ÷ 60 h ' + C.egal(m / 60, 4) + ' h']
      }
    }
  })
})()
