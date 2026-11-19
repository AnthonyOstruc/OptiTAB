/* Horloge interactive : explorer l'heure et s'entraîner à la lire.
 * Les fonctions de lecture (chiffres, mots, 24 heures) sont exposées dans
 * window.OTHeure : contenu/methodes/lire-l-heure/generer.py les compare, pour
 * les 1 440 minutes de la journée, à celles qui écrivent les corrigés des fiches. */
(function () {
  'use strict'
  var NB = ['zéro', 'une', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze',
    'treize', 'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf']
  var DIZ = { 2: 'vingt', 3: 'trente', 4: 'quarante', 5: 'cinquante' }
  var NBSP = String.fromCharCode(160)

  // 0 à 59 en lettres, au féminin (« vingt et une » minutes, « une » heure).
  function nombre(n) {
    if (n < 20) return NB[n]
    var d = Math.floor(n / 10), u = n % 10
    if (u === 0) return DIZ[d]
    if (u === 1) return DIZ[d] + ' et une'
    return DIZ[d] + '-' + NB[u]
  }

  function deux(n) { return (n < 10 ? '0' : '') + n }

  // « 9 h 15 », « 14 h 05 », « 7 h 00 »
  function chiffres(h, m) { return h + NBSP + 'h' + NBSP + deux(m) }

  // Lecture officielle sur 24 heures : « quatorze heures quinze », « zéro heure cinq »
  function vingtQuatre(h, m) {
    var heures = h === 0 ? 'zéro heure' : h === 1 ? 'une heure' : nombre(h) + ' heures'
    return heures + (m ? ' ' + nombre(m) : '')
  }

  function nomHeure(h) {
    if (h % 24 === 0) return 'minuit'
    if (h === 12) return 'midi'
    var k = h % 12
    return k === 1 ? 'une heure' : nombre(k) + ' heures'
  }

  function moment(h) {
    if (h === 0 || h === 12) return ''
    return h < 12 ? ' du matin' : h < 18 ? ' de l’après-midi' : ' du soir'
  }

  // Ce que l'on dit : « trois heures et quart de l'après-midi », « midi moins le quart »
  function parle(h, m) {
    if (m === 0) return nomHeure(h) + moment(h)
    if (m === 15) return nomHeure(h) + ' et quart' + moment(h)
    if (m === 30) return nomHeure(h) + (h % 12 === 0 ? ' et demi' : ' et demie') + moment(h)
    if (m >= 35 && m % 5 === 0) {
      var h2 = (h + 1) % 24
      return nomHeure(h2) + (m === 45 ? ' moins le quart' : ' moins ' + nombre(60 - m)) + moment(h2)
    }
    return nomHeure(h) + ' ' + nombre(m) + moment(h)
  }

  var lecture = { chiffres: chiffres, vingtQuatre: vingtQuatre, parle: parle, nombre: nombre }
  if (typeof window !== 'undefined') window.OTHeure = lecture

  var s = typeof document !== 'undefined' && document.querySelector('[data-outil="horloge"]')
  if (!s) return

  function poser(svg, h, m, titre) {
    svg.querySelector('[data-aiguille="h"]').setAttribute('transform', 'rotate(' + ((h % 12) * 30 + m * 0.5) + ' 100 100)')
    svg.querySelector('[data-aiguille="m"]').setAttribute('transform', 'rotate(' + (m * 6) + ' 100 100)')
    svg.setAttribute('aria-label', titre)
  }

  // ---------- Onglets ----------
  var onglets = s.querySelectorAll('.otc__onglet')
  Array.prototype.forEach.call(onglets, function (o) {
    o.addEventListener('click', function () {
      Array.prototype.forEach.call(onglets, function (x) {
        var actif = x === o
        x.setAttribute('aria-selected', actif ? 'true' : 'false')
        x.tabIndex = actif ? 0 : -1
        s.querySelector('[data-panneau="' + x.getAttribute('data-mode') + '"]').hidden = !actif
      })
      if (o.getAttribute('data-mode') === 'quiz' && !question) nouvelle()
    })
  })

  // ---------- Explorer ----------
  var total = 9 * 60 + 15
  var cadran = s.querySelector('[data-cadran="explorer"]')
  function montrer() {
    var h = Math.floor(total / 60), m = total % 60
    poser(cadran, h, m, 'Horloge qui indique ' + chiffres(h, m))
    s.querySelector('[data-num]').textContent = chiffres(h, m)
    s.querySelector('[data-mots]').textContent = parle(h, m)
    s.querySelector('[data-vingtquatre]').textContent = 'Sur 24 heures : ' + vingtQuatre(h, m)
  }
  Array.prototype.forEach.call(s.querySelectorAll('[data-pas]'), function (b) {
    b.addEventListener('click', function () {
      total = (total + parseInt(b.getAttribute('data-pas'), 10) + 1440) % 1440
      montrer()
    })
  })

  // ---------- S'entraîner ----------
  var niveau = 'ce1', question = null, bons = 0, faits = 0
  var cadranQuiz = s.querySelector('[data-cadran="quiz"]')
  var zoneChoix = s.querySelector('[data-choix]')
  var retour = s.querySelector('[data-retour]')
  var score = s.querySelector('[data-score]')

  function hasard(n) { return Math.floor(Math.random() * n) }

  function tirer() {
    var h = 1 + hasard(12)
    if (niveau === 'cp') return [h, 0]
    if (niveau === 'ce1') return [h, [0, 15, 30, 45][hasard(4)]]
    return [h, hasard(3) ? 5 * hasard(12) : hasard(60)]
  }

  function texte(h, m) { return niveau === 'cp' ? h + NBSP + 'h' : chiffres(h, m) }

  // Réponses pièges : aiguilles inversées, heure suivante lue trop tôt, nombre
  // de la grande aiguille pris pour les minutes, puis heures voisines.
  function pieges(h, m) {
    var p = []
    var surNombre = m % 5 === 0 ? (m === 0 ? 12 : m / 5) : 0
    if (niveau !== 'cp' && surNombre && surNombre !== h) p.push([surNombre, (h * 5) % 60])
    if (m >= 30) p.push([h % 12 + 1, m])
    if (niveau !== 'cp' && surNombre && m) p.push([h, surNombre])
    p.push([h % 12 + 1, m], [(h + 10) % 12 + 1, m], [h, (m + 30) % 60], [(h + 5) % 12 + 1, (m + 15) % 60])
    return p
  }

  function nouvelle() {
    var t = tirer(), h = t[0], m = t[1]
    question = { h: h, m: m, repondu: false }
    poser(cadranQuiz, h, m, 'Horloge à lire')
    var choix = [texte(h, m)]
    pieges(h, m).forEach(function (q) {
      var c = texte(q[0], q[1])
      if (choix.length < 4 && choix.indexOf(c) < 0) choix.push(c)
    })
    while (choix.length < 4) {
      var r = texte(1 + hasard(12), niveau === 'cp' ? 0 : 5 * hasard(12))
      if (choix.indexOf(r) < 0) choix.push(r)
    }
    choix.sort(function () { return Math.random() - 0.5 })
    zoneChoix.innerHTML = choix.map(function (c) {
      return '<button type="button" class="hl__reponse" data-reponse="' + c + '">' + c + '</button>'
    }).join('')
    retour.textContent = ''
    retour.className = 'hl__retour'
  }

  zoneChoix.addEventListener('click', function (ev) {
    var b = ev.target.closest ? ev.target.closest('[data-reponse]') : null
    if (!b || !question || question.repondu) return
    question.repondu = true
    faits++
    var juste = texte(question.h, question.m)
    var ok = b.getAttribute('data-reponse') === juste
    if (ok) bons++
    Array.prototype.forEach.call(zoneChoix.children, function (x) {
      x.disabled = true
      if (x.getAttribute('data-reponse') === juste) x.classList.add('is-juste')
      else if (x === b) x.classList.add('is-faux')
    })
    // Une horloge à aiguilles ne dit pas si c'est le matin ou l'après-midi.
    var mots = parle(question.h, question.m).replace(/ (du matin|de l’après-midi|du soir)$/, '')
    retour.textContent = (ok ? 'Bravo ! ' : 'Pas tout à fait. ') + 'Il est ' + juste + ' : ' + mots + '. '
      + (ok ? '' : 'La petite aiguille donne l’heure, la grande donne les minutes.')
    retour.className = 'hl__retour ' + (ok ? 'is-juste' : 'is-faux')
    score.textContent = bons + ' / ' + faits
  })

  s.querySelector('[data-suivant]').addEventListener('click', nouvelle)

  Array.prototype.forEach.call(s.querySelectorAll('[data-niveau]'), function (b) {
    b.addEventListener('click', function () {
      niveau = b.getAttribute('data-niveau')
      Array.prototype.forEach.call(s.querySelectorAll('[data-niveau]'), function (x) {
        x.setAttribute('aria-checked', x === b ? 'true' : 'false')
      })
      bons = 0; faits = 0; score.textContent = ''
      nouvelle()
    })
  })
})()
