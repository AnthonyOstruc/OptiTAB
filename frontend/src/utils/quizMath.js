/**
 * Quiz — lecture et comparaison des réponses écrites par l'élève.
 *
 * L'élève tape une réponse comme sur une calculatrice : 2e^(3x), ln(2)/3,
 * √5, 1/2, 0,5, x²+1… Le texte est analysé (virgule décimale, multiplication
 * implicite, symboles × ÷ − √ ² π), puis comparé à la réponse attendue :
 *   - nombre : même valeur (valeur exacte) ou à la tolérance près (arrondi) ;
 *   - expression : mêmes valeurs en plusieurs points de l'intervalle choisi.
 * Module sans dépendance : utilisé par le site et par les contrôles du chantier.
 */

const FONCTIONS = {
  exp: Math.exp,
  ln: Math.log,
  log: Math.log10,
  sqrt: Math.sqrt,
  sin: Math.sin,
  cos: Math.cos,
  tan: Math.tan,
  abs: Math.abs
}

const TEX_FONCTIONS = { ln: '\\ln', log: '\\log', sin: '\\sin', cos: '\\cos', tan: '\\tan', exp: '\\exp' }

const EXPOSANTS = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-', '⁺': '+', 'ˣ': 'x' }

/** Normalise la saisie : symboles usuels, espaces, virgule décimale. */
export function normaliser(texte) {
  return String(texte ?? '')
    .replace(/[−–—]/g, '-')
    .replace(/[×·∙]/g, '*')
    .replace(/÷/g, '/')
    .replace(/π/g, 'pi')
    .replace(/√/g, 'sqrt')
    // exposants tapés au clavier du téléphone : e⁻¹, x², eˣ
    .replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ˣ]+/g, (m) => `^(${[...m].map((c) => EXPOSANTS[c]).join('')})`)
    // accolades et crochets comme parenthèses : e^{2x}
    .replace(/[{[]/g, '(')
    .replace(/[}\]]/g, ')')
    .replace(/(\d),(\d)/g, '$1.$2')
    .replace(/\s+/g, '')
    // point de multiplication « x.e^x » (le point décimal reste entre deux chiffres)
    .replace(/(^|[^\d])\.(?=\d)/g, '$10.')
    .replace(/\.(?!\d)|(?<!\d)\./g, '*')
    .replace(/\*\*/g, '^')
    .toLowerCase()
}

/* ------------------------------------------------------------------ */
/*  Découpage en jetons                                                */
/* ------------------------------------------------------------------ */

function jetons(src, variable) {
  const out = []
  let i = 0
  while (i < src.length) {
    const c = src[i]
    if (/[0-9.]/.test(c)) {
      let j = i
      while (j < src.length && /[0-9.]/.test(src[j])) j += 1
      const t = src.slice(i, j)
      if ((t.match(/\./g) || []).length > 1) throw new Error('nombre mal écrit')
      out.push({ t: 'num', v: Number(t) })
      i = j
      continue
    }
    if (/[a-z]/.test(c)) {
      let j = i
      while (j < src.length && /[a-z]/.test(src[j])) j += 1
      let mot = src.slice(i, j)
      // Découpe un mot collé : « xe », « 2ex », « xln » … en noms connus
      while (mot) {
        const fn = Object.keys(FONCTIONS).find((f) => mot.startsWith(f))
        if (fn) {
          out.push({ t: 'fn', v: fn })
          mot = mot.slice(fn.length)
        } else if (mot.startsWith('pi')) {
          out.push({ t: 'const', v: 'pi' })
          mot = mot.slice(2)
        } else if (mot[0] === 'e') {
          out.push({ t: 'const', v: 'e' })
          mot = mot.slice(1)
        } else if (variable && mot[0] === variable) {
          out.push({ t: 'var', v: variable })
          mot = mot.slice(1)
        } else if (!variable && /[xyt]/.test(mot[0])) {
          throw new Error('la réponse attendue est un nombre')
        } else {
          throw new Error(`symbole inconnu « ${mot[0]} »`)
        }
      }
      i = j
      continue
    }
    if ('+-*/^()'.includes(c)) {
      out.push({ t: c })
      i += 1
      continue
    }
    throw new Error(`caractère inconnu « ${c} »`)
  }
  // Multiplication implicite : 2x, 2(x+1), )(, x e, 3sqrt…
  const res = []
  const finValeur = (k) => k && (k.t === 'num' || k.t === 'var' || k.t === 'const' || k.t === ')')
  const debutValeur = (k) => k && (k.t === 'num' || k.t === 'var' || k.t === 'const' || k.t === 'fn' || k.t === '(')
  for (const k of out) {
    if (finValeur(res[res.length - 1]) && debutValeur(k)) res.push({ t: '*', implicite: true })
    res.push(k)
  }
  return res
}

/* ------------------------------------------------------------------ */
/*  Analyse (priorités : + - < * / < signe < ^ ; ^ à droite)           */
/* ------------------------------------------------------------------ */

function analyser(liste) {
  let p = 0
  const voir = () => liste[p]
  const prendre = (t) => {
    if (!liste[p] || liste[p].t !== t) throw new Error(t === ')' ? 'parenthèse non fermée' : 'expression incomplète')
    p += 1
  }

  function somme() {
    let g = produit()
    while (voir() && (voir().t === '+' || voir().t === '-')) {
      const op = liste[p++].t
      g = { op, a: g, b: produit() }
    }
    return g
  }
  function produit() {
    let g = signe()
    while (voir() && (voir().t === '*' || voir().t === '/')) {
      const k = liste[p++]
      g = { op: k.t, a: g, b: signe(), implicite: !!k.implicite }
    }
    return g
  }
  function signe() {
    if (voir() && voir().t === '-') {
      p += 1
      return { op: 'neg', a: signe() }
    }
    if (voir() && voir().t === '+') {
      p += 1
      return signe()
    }
    return puissance()
  }
  function puissance() {
    const base = atome()
    if (voir() && voir().t === '^') {
      p += 1
      return { op: '^', a: base, b: signe() }
    }
    return base
  }
  function atome() {
    const k = voir()
    if (!k) throw new Error('expression incomplète')
    p += 1
    if (k.t === 'num') return { num: k.v }
    if (k.t === 'var') return { var: k.v }
    if (k.t === 'const') return { cst: k.v }
    if (k.t === '(') {
      const e = somme()
      prendre(')')
      return { op: '()', a: e }
    }
    if (k.t === 'fn') {
      // ln 2, ln(2), sqrt5, exp(x)
      if (voir() && voir().t === '(') return { fn: k.v, a: atome() }
      return { fn: k.v, a: puissance() }
    }
    throw new Error('expression mal écrite')
  }

  if (!liste.length) throw new Error('réponse vide')
  const arbre = somme()
  if (p < liste.length) throw new Error(liste[p].t === ')' ? 'parenthèse en trop' : 'expression mal écrite')
  return arbre
}

/** Analyse une saisie. Renvoie { arbre } ou { erreur }. */
export function lire(texte, variable = 'x') {
  try {
    return { arbre: analyser(jetons(normaliser(texte), variable)) }
  } catch (e) {
    return { erreur: e.message || 'expression mal écrite' }
  }
}

/* ------------------------------------------------------------------ */
/*  Évaluation et écriture LaTeX                                       */
/* ------------------------------------------------------------------ */

export function evaluer(arbre, valeurs = {}) {
  if ('num' in arbre) return arbre.num
  if ('var' in arbre) return valeurs[arbre.var] ?? NaN
  if ('cst' in arbre) return arbre.cst === 'e' ? Math.E : Math.PI
  if (arbre.fn) return FONCTIONS[arbre.fn](evaluer(arbre.a, valeurs))
  const a = evaluer(arbre.a, valeurs)
  switch (arbre.op) {
    case '()': return a
    case 'neg': return -a
    case '+': return a + evaluer(arbre.b, valeurs)
    case '-': return a - evaluer(arbre.b, valeurs)
    case '*': return a * evaluer(arbre.b, valeurs)
    case '/': return a / evaluer(arbre.b, valeurs)
    case '^': return a ** evaluer(arbre.b, valeurs)
    default: return NaN
  }
}

const sansParentheses = (n) => (n.op === '()' ? n.a : n)

export function versTex(n) {
  if ('num' in n) return String(n.num).replace('.', '{,}')
  if ('var' in n) return n.var
  if ('cst' in n) return n.cst === 'e' ? 'e' : '\\pi'
  if (n.fn === 'sqrt') return `\\sqrt{${versTex(sansParentheses(n.a))}}`
  if (n.fn === 'abs') return `\\left|${versTex(sansParentheses(n.a))}\\right|`
  if (n.fn) {
    const x = sansParentheses(n.a)
    const simple = 'num' in x || 'var' in x || 'cst' in x
    const arg = simple ? ` ${versTex(x)}` : `\\left(${versTex(x)}\\right)`
    return `${TEX_FONCTIONS[n.fn]}${arg}`
  }
  switch (n.op) {
    case '()': return `\\left(${versTex(n.a)}\\right)`
    case 'neg': return `-${versTex(n.a)}`
    case '+': return `${versTex(n.a)}+${versTex(n.b)}`
    case '-': return `${versTex(n.a)}-${versTex(n.b)}`
    case '*': {
      // 2x, 3e^{x}, x\ln x : sans signe ; 2 × 3, x × (−1) : avec le signe ×
      const chiffreApres = 'num' in n.b || (n.b.op === '^' && 'num' in n.b.a) || n.b.op === 'neg'
      return `${versTex(n.a)}${chiffreApres ? '\\times ' : ''}${versTex(n.b)}`
    }
    case '/': return `\\dfrac{${versTex(sansParentheses(n.a))}}{${versTex(sansParentheses(n.b))}}`
    case '^': return `${versTex(n.a)}^{${versTex(sansParentheses(n.b))}}`
    default: return ''
  }
}

/* ------------------------------------------------------------------ */
/*  Comparaison                                                         */
/* ------------------------------------------------------------------ */

function proches(a, b, tolerance) {
  if (!Number.isFinite(a) || !Number.isFinite(b)) return false
  if (tolerance != null) return Math.abs(a - b) <= tolerance + 1e-12
  return Math.abs(a - b) <= 1e-9 * Math.max(1, Math.abs(a), Math.abs(b))
}

/**
 * Retire ce qui entoure la réponse sans en faire partie : « x = 4 »,
 * « f'(x) = … », l'unité tapée à la fin (« 4,32 V »).
 */
export function nettoyerSaisie(saisie, q = {}) {
  let s = String(saisie ?? '').trim()
  const egal = s.lastIndexOf('=')
  if (egal >= 0 && /^[\s\w'’()]*$/.test(s.slice(0, egal))) s = s.slice(egal + 1).trim()
  if (q.unite) {
    const u = String(q.unite).trim().toLowerCase()
    if (u && s.toLowerCase().endsWith(u)) s = s.slice(0, -u.length).trim()
  }
  return s
}

/**
 * Compare la saisie de l'élève à une réponse attendue.
 * @param {string} saisie
 * @param {{reponses: string[], nature?: 'nombre'|'expression', variable?: string,
 *          tolerance?: number|null, intervalle?: [number, number]}} q
 * @returns {{ok: boolean, erreur?: string}}
 */
export function comparer(saisie, q) {
  const variable = q.variable || 'x'
  const lu = lire(nettoyerSaisie(saisie, q), q.nature === 'expression' ? variable : null)
  if (lu.erreur) return { ok: false, erreur: lu.erreur }
  const attendus = (q.reponses || []).map((r) => lire(r, q.nature === 'expression' ? variable : null).arbre).filter(Boolean)
  if (q.nature === 'expression') {
    const [a, b] = q.intervalle || [0.3, 2.7]
    const points = [0, 1, 2, 3, 4, 5, 6].map((k) => a + ((b - a) * (k + 0.37)) / 7)
    return {
      ok: attendus.some((att) => points.every((x) => proches(evaluer(lu.arbre, { [variable]: x }), evaluer(att, { [variable]: x }), null)))
    }
  }
  const v = evaluer(lu.arbre)
  if (!Number.isFinite(v)) return { ok: false, erreur: 'cette valeur n’existe pas' }
  return { ok: attendus.some((att) => proches(v, evaluer(att), q.tolerance ?? null)) }
}
