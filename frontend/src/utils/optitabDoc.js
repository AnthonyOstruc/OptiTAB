/**
 * OptiTAB Doc — format de contenu structuré, version 1.
 *
 * Un contenu (cours, fiche, énoncé, étapes, solution) commence par le
 * marqueur `<!-- optitab:1 -->`. Le reste est du texte structuré :
 * encadrés `::: definition Titre … :::`, titres `##`, listes, formules
 * `$…$` / `$$…$$`, tableaux `| … |`, tableaux de variations
 * `::: tableau` (syntaxe tkz-tab, comme les livres), images `[IMAGE_N]`.
 *
 * Spécification complète : frontend/cours/format_v1/FORMAT.md
 *
 * Module sans dépendance (pas de Vue) : utilisé par le site, l'aperçu et
 * les outils de vérification.
 */

const MARKER_RE = /^\s*<!--\s*optitab:1\s*-->[ \t]*(?:\r?\n)?/

export const OPTITAB_MARKER = '<!-- optitab:1 -->'

export function isOptitabDoc(text) {
  return typeof text === 'string' && MARKER_RE.test(text)
}

/* Identifiant stable dérivé du contenu : le même texte produit toujours
   le même HTML, sinon Vue réécrirait le v-html à chaque rendu et
   effacerait les formules déjà composées par MathJax. */
function hashString(text) {
  let h = 2166136261
  for (let i = 0; i < text.length; i += 1) {
    h ^= text.charCodeAt(i)
    h = Math.imul(h, 16777619)
  }
  return (h >>> 0).toString(36)
}

/* ------------------------------------------------------------------ */
/*  Encadrés                                                           */
/* ------------------------------------------------------------------ */

const BOXES = {
  definition: 'Définition',
  theoreme: 'Théorème',
  propriete: 'Propriété',
  methode: 'Méthode',
  attention: 'Attention',
  exemple: 'Exemple',
  demonstration: 'Démonstration',
  remarque: 'Remarque',
  retenir: 'À retenir',
  rappel: 'Rappel',
  notation: 'Notation',
  formule: '',
  resultat: 'Résultat',
  etape: 'Étape',
  point: '',
  objectifs: 'Objectifs',
  prerequis: 'Prérequis',
  conseil: 'Conseil'
}

const ALIASES = {
  savoirfaire: 'methode',
  'savoir-faire': 'methode',
  erreur: 'attention',
  piege: 'attention',
  astuce: 'conseil',
  conclusion: 'resultat',
  reponse: 'resultat',
  solution: 'resultat',
  verification: 'point',
  variations: 'tableau',
  signes: 'tableau',
  tableau: 'tableau'
}

function stripAccents(s) {
  return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '')
}

function normalizeKind(raw) {
  const k = stripAccents(raw).toLowerCase().trim()
  if (ALIASES[k]) return ALIASES[k]
  if (Object.prototype.hasOwnProperty.call(BOXES, k)) return k
  return k
}

/* ------------------------------------------------------------------ */
/*  Utilitaires                                                        */
/* ------------------------------------------------------------------ */

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function indentOf(line) {
  const m = line.match(/^[ \t]*/)
  return m ? m[0].replace(/\t/g, '    ').length : 0
}

function dedent(lines) {
  let min = Infinity
  for (const l of lines) {
    if (!l.trim()) continue
    min = Math.min(min, indentOf(l))
  }
  if (!Number.isFinite(min) || min === 0) return lines.slice()
  return lines.map((l) => (l.trim() ? l.replace(/\t/g, '    ').slice(min) : ''))
}

/** Découpe une chaîne aux virgules (ou autre séparateur) hors {}, (), [] et $…$. */
function splitTop(str, sep = ',') {
  const parts = []
  let depth = 0
  let inMath = false
  let buf = ''
  for (let i = 0; i < str.length; i += 1) {
    const c = str[i]
    if (c === '\\' && i + 1 < str.length) {
      buf += c + str[i + 1]
      i += 1
      continue
    }
    if (c === '$') inMath = !inMath
    if (!inMath) {
      if (c === '{' || c === '(' || c === '[') depth += 1
      else if ((c === '}' || c === ')' || c === ']') && depth > 0) depth -= 1
    }
    if (c === sep && depth === 0 && !inMath) {
      parts.push(buf.trim())
      buf = ''
      continue
    }
    buf += c
  }
  parts.push(buf.trim())
  return parts
}

/** Découpe une ligne de tableau `| a | b |` aux barres hors formules. */
function splitPipeRow(line) {
  let s = line.trim()
  if (s.startsWith('|')) s = s.slice(1)
  if (s.endsWith('|') && !s.endsWith('\\|')) s = s.slice(0, -1)
  const cells = []
  let inMath = false
  let buf = ''
  for (let i = 0; i < s.length; i += 1) {
    const c = s[i]
    if (c === '\\' && i + 1 < s.length) {
      buf += c + s[i + 1]
      i += 1
      continue
    }
    if (c === '$') inMath = !inMath
    if (c === '|' && !inMath) {
      cells.push(buf.trim())
      buf = ''
      continue
    }
    buf += c
  }
  cells.push(buf.trim())
  return cells
}

function stripDollars(tex) {
  const t = String(tex || '').trim()
  if (t.length >= 2 && t.startsWith('$') && t.endsWith('$')) return t.replace(/^\$+|\$+$/g, '').trim()
  return t
}

/* ------------------------------------------------------------------ */
/*  Analyse en blocs                                                   */
/* ------------------------------------------------------------------ */

const LIST_RE = /^([ \t]*)([-*•]|\d{1,3}[.)])[ \t]+(.*)$/
const FENCE_OPEN_RE = /^(:{3,})[ \t]*([^\s:][^\s]*)[ \t]*(.*)$/
const FENCE_CLOSE_RE = /^:{3,}[ \t]*$/
const HEADING_RE = /^(#{2,4})[ \t]+(.*)$/
const IMAGE_RE = /^\[\s*IMAGE\s*_?\s*\d+\s*\]$/i
const CODE_FENCE_RE = /^```\s*([A-Za-z0-9_+-]*)\s*$/

function startsBlock(raw) {
  const t = raw.trim()
  return (
    CODE_FENCE_RE.test(t) ||
    FENCE_OPEN_RE.test(t) ||
    FENCE_CLOSE_RE.test(t) ||
    t.startsWith('$$') ||
    HEADING_RE.test(t) ||
    IMAGE_RE.test(t) ||
    t.startsWith('|') ||
    LIST_RE.test(raw)
  )
}

function parseBlocks(lines) {
  const nodes = []
  const n = lines.length
  let i = 0

  while (i < n) {
    const raw = lines[i]
    const line = raw.trim()
    if (!line) {
      i += 1
      continue
    }

    // Bloc de code ```python … ``` (indentation conservée)
    const code = line.match(CODE_FENCE_RE)
    if (code) {
      const base = indentOf(raw)
      const body = []
      let j = i + 1
      while (j < n && !/^\s*```\s*$/.test(lines[j])) {
        const l = lines[j].replace(/\t/g, '    ')
        body.push(indentOf(l) >= base ? l.slice(base) : l.trimStart())
        j += 1
      }
      while (body.length && !body[body.length - 1].trim()) body.pop()
      nodes.push({ type: 'code', lang: (code[1] || 'python').toLowerCase(), text: body.join('\n') })
      i = j + 1
      continue
    }

    // Encadré ::: type Titre … :::
    const fence = line.match(FENCE_OPEN_RE)
    if (fence) {
      const inner = []
      let depth = 1
      let j = i + 1
      while (j < n) {
        const t = lines[j].trim()
        if (FENCE_CLOSE_RE.test(t)) {
          depth -= 1
          if (depth === 0) break
        } else if (FENCE_OPEN_RE.test(t)) {
          depth += 1
        }
        inner.push(lines[j])
        j += 1
      }
      const kind = normalizeKind(fence[2])
      const title = fence[3].trim()
      if (kind === 'tableau') {
        nodes.push({ type: 'tabvar', lines: inner, title })
      } else {
        nodes.push({ type: 'box', kind, rawKind: fence[2], title, children: parseBlocks(dedent(inner)) })
      }
      i = j + 1
      continue
    }
    if (FENCE_CLOSE_RE.test(line)) {
      i += 1
      continue
    }

    // Formule centrée $$ … $$ (une ou plusieurs lignes)
    if (line.startsWith('$$')) {
      let j = i
      let tex
      const rest = line.slice(2)
      if (rest.trimEnd().endsWith('$$') && rest.trim().length >= 2) {
        tex = rest.trimEnd().slice(0, -2)
      } else {
        const parts = [rest]
        j = i + 1
        while (j < n && !lines[j].trimEnd().endsWith('$$')) {
          parts.push(lines[j])
          j += 1
        }
        if (j < n) parts.push(lines[j].trimEnd().slice(0, -2))
        tex = parts.join('\n')
      }
      nodes.push({ type: 'math', tex: tex.trim() })
      i = j + 1
      continue
    }

    const h = line.match(HEADING_RE)
    if (h) {
      nodes.push({ type: 'heading', level: h[1].length, text: h[2].trim() })
      i += 1
      continue
    }

    if (IMAGE_RE.test(line)) {
      nodes.push({ type: 'image', token: line.replace(/\s+/g, '') })
      i += 1
      continue
    }

    if (line.startsWith('|')) {
      const rows = []
      let j = i
      while (j < n && lines[j].trim().startsWith('|')) {
        rows.push(lines[j].trim())
        j += 1
      }
      nodes.push(parsePipeTable(rows))
      i = j
      continue
    }

    if (LIST_RE.test(raw)) {
      const [node, next] = parseList(lines, i)
      nodes.push(node)
      i = next
      continue
    }

    // Paragraphe
    const para = [line]
    let j = i + 1
    while (j < n) {
      const t = lines[j].trim()
      if (!t || startsBlock(lines[j])) break
      para.push(t)
      j += 1
    }
    nodes.push({ type: 'para', text: para.join(' ') })
    i = j
  }
  return nodes
}

function parseList(lines, start) {
  const first = lines[start].match(LIST_RE)
  const baseIndent = indentOf(first[1])
  const ordered = /\d/.test(first[2])
  const items = []
  let cur = null
  let i = start

  while (i < lines.length) {
    const raw = lines[i]
    if (!raw.trim()) {
      let k = i + 1
      while (k < lines.length && !lines[k].trim()) k += 1
      if (k >= lines.length) break
      const nx = lines[k]
      const m = nx.match(LIST_RE)
      const sameList = m && indentOf(m[1]) === baseIndent && /\d/.test(m[2]) === ordered
      if (sameList || indentOf(nx) > baseIndent) {
        if (cur) cur.lines.push('')
        i += 1
        continue
      }
      break
    }
    const m = raw.match(LIST_RE)
    if (m && indentOf(m[1]) === baseIndent) {
      if (/\d/.test(m[2]) !== ordered) break
      cur = { lines: [m[3]], number: ordered ? Number.parseInt(m[2], 10) : null }
      items.push(cur)
      i += 1
      continue
    }
    if (indentOf(raw) > baseIndent && cur) {
      cur.lines.push(raw)
      i += 1
      continue
    }
    break
  }

  for (const it of items) {
    const [head, ...rest] = it.lines
    it.children = parseBlocks([head, ...dedent(rest)])
  }
  return [{ type: 'list', ordered, start: items[0]?.number || 1, items }, i]
}

function parsePipeTable(rows) {
  const parsed = rows.map(splitPipeRow)
  const sepRe = /^:?-{2,}:?$/
  let header = null
  let align = []
  let body = parsed
  if (parsed.length >= 2 && parsed[1].every((c) => sepRe.test(c.replace(/\s+/g, '')))) {
    header = parsed[0]
    align = parsed[1].map((c) => {
      const t = c.replace(/\s+/g, '')
      if (t.startsWith(':') && t.endsWith(':')) return 'center'
      if (t.endsWith(':')) return 'right'
      if (t.startsWith(':')) return 'left'
      return ''
    })
    body = parsed.slice(2)
  }
  return { type: 'table', header, align, body }
}

/* ------------------------------------------------------------------ */
/*  Rendu du texte (formules protégées, gras, italique, typographie)   */
/* ------------------------------------------------------------------ */

function formatText(escaped) {
  return escaped
    .replace(/\*\*(?=\S)([\s\S]+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*\w\\])\*(?=\S)([^*]+?)\*(?!\*)/g, '$1<em>$2</em>')
    // Espaces insécables avant la ponctuation haute (typographie française)
    .replace(/ ([:;!?»])/g, ' $1')
    .replace(/« /g, '« ')
}

export function renderInline(text) {
  const src = String(text ?? '')
  // 1) Formules remplacées par des repères : le gras et l'italique peuvent
  //    ainsi entourer une formule (**$x$ est réel**, *$\sin$ et $\cos$*).
  const maths = []
  const codes = []
  let plain = ''
  let i = 0
  while (i < src.length) {
    const c = src[i]
    if (c === '`') {
      const end = src.indexOf('`', i + 1)
      if (end > i) {
        codes.push(src.slice(i + 1, end))
        plain += `\u0001${codes.length - 1}\u0001`
        i = end + 1
        continue
      }
    }
    if (c === '\\' && src[i + 1] === '$') {
      plain += '\\$'
      i += 2
      continue
    }
    if (c === '$') {
      const delim = src[i + 1] === '$' ? '$$' : '$'
      let j = i + delim.length
      let end = -1
      while (j < src.length) {
        if (src[j] === '\\') {
          j += 2
          continue
        }
        if (src.startsWith(delim, j)) {
          end = j
          break
        }
        j += 1
      }
      if (end > i) {
        maths.push(src.slice(i, end + delim.length))
        plain += `\u0000${maths.length - 1}\u0000`
        i = end + delim.length
        continue
      }
    }
    plain += c
    i += 1
  }

  // 2) Mise en forme du texte, puis ponctuation collée aux formules en ligne
  //    (jamais de « ) » ou de « , » orphelin en début de ligne)
  let html = formatText(escapeHtml(plain).replace(/&lt;br\s*\/?&gt;/gi, '<br>'))
  html = html.replace(/([(«[])?\u0000(\d+)\u0000([),.;:!?»\]]{1,3}|-[A-Za-zÀ-ÿ]+)?/g, (m, lead, k, trail) => {
    const tex = maths[Number(k)]
    const math = escapeHtml(tex)
    if ((lead || trail) && !tex.startsWith('$$')) {
      return `<span class="otm-nb">${lead || ''}${math}${trail || ''}</span>`
    }
    return `${lead || ''}${math}${trail || ''}`
  })
  // Code en ligne `x = 3` (jamais lu comme une formule)
  html = html.replace(/\u0001(\d+)\u0001/g, (m, k) => `<code class="otm-c">${escapeHtml(codes[Number(k)])}</code>`)
  return html
}

/* ------------------------------------------------------------------ */
/*  Code (coloration Python, même palette que l'environnement des livres) */
/* ------------------------------------------------------------------ */

const PY_KEYWORDS = new Set([
  'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else',
  'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or',
  'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
])
const PY_BUILTINS = new Set([
  'print', 'range', 'len', 'int', 'float', 'str', 'list', 'abs', 'round', 'sum', 'min', 'max', 'input', 'type',
  'bool', 'dict', 'set', 'tuple', 'enumerate', 'zip', 'sorted', 'append', 'sqrt', 'randint', 'random', 'floor'
])

function highlightPython(code) {
  const re = /(#[^\n]*)|([rRfFbB]{0,2}"(?:\\.|[^"\\\n])*"|[rRfFbB]{0,2}'(?:\\.|[^'\\\n])*')|\b(\d+(?:\.\d+)?)\b|\b([A-Za-z_][A-Za-z0-9_]*)\b/g
  let out = ''
  let last = 0
  let m
  while ((m = re.exec(code))) {
    out += escapeHtml(code.slice(last, m.index))
    if (m[1]) out += `<span class="tk-c">${escapeHtml(m[1])}</span>`
    else if (m[2]) out += `<span class="tk-s">${escapeHtml(m[2])}</span>`
    else if (m[3]) out += `<span class="tk-n">${m[3]}</span>`
    else if (PY_KEYWORDS.has(m[4])) out += `<span class="tk-k">${m[4]}</span>`
    else if (PY_BUILTINS.has(m[4])) out += `<span class="tk-b">${m[4]}</span>`
    else out += m[4]
    last = re.lastIndex
  }
  return out + escapeHtml(code.slice(last))
}

function renderCode(node) {
  const lang = node.lang === 'py' ? 'python' : node.lang
  const body = lang === 'python' ? highlightPython(node.text) : escapeHtml(node.text)
  const label = { python: 'Python', console: 'Affichage', texte: '' }[lang] ?? lang
  return (
    `<div class="otm-code otm-code--${escapeHtml(lang)}">` +
    (label ? `<span class="otm-code-lang">${escapeHtml(label)}</span>` : '') +
    `<pre><code>${body}</code></pre></div>`
  )
}

/* ------------------------------------------------------------------ */
/*  Tableau de variations / de signes (syntaxe tkz-tab)                */
/* ------------------------------------------------------------------ */

function parseVarEntry(entry) {
  const e = entry.trim()
  if (!e || /^R\/?$/.test(e)) return { skip: true }
  const slash = e.indexOf('/')
  const prefix = (slash >= 0 ? e.slice(0, slash) : e).replace(/\s+/g, '')
  const vals = slash >= 0 ? splitTop(e.slice(slash + 1), '/').map(stripDollars) : []
  const pos = (s) => (s === '+' ? 'top' : s === '-' ? 'bottom' : 'middle')

  let m = prefix.match(/^([+-])D([+-])$/)
  if (m) {
    return {
      left: { pos: pos(m[1]), tex: vals[0] ?? '' },
      right: { pos: pos(m[2]), tex: vals[1] ?? vals[0] ?? '' },
      bar: 'middle'
    }
  }
  m = prefix.match(/^D([+-])$/)
  if (m) return { left: null, right: { pos: pos(m[1]), tex: vals[0] ?? '' }, bar: 'left' }
  m = prefix.match(/^([+-])D$/)
  if (m) return { left: { pos: pos(m[1]), tex: vals[0] ?? '' }, right: null, bar: 'right' }
  m = prefix.match(/^([+=-])[CH]?$/)
  if (m) {
    const v = { pos: pos(m[1]), tex: vals[0] ?? '' }
    return { left: v, right: v, bar: 'none' }
  }
  return { left: { pos: 'middle', tex: vals[0] ?? stripDollars(e) }, right: { pos: 'middle', tex: vals[0] ?? stripDollars(e) }, bar: 'none' }
}

function arrowSvg(id, from, to) {
  const y = (p) => (p === 'top' ? 24 : p === 'bottom' ? 76 : 50)
  const y1 = y(from)
  const y2 = y(to)
  return (
    `<svg class="otm-tv-arrow" aria-hidden="true" focusable="false">` +
    `<defs><marker id="${id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto">` +
    `<path d="M0,0.6 L10,5 L0,9.4 L2.6,5 Z" fill="currentColor"/></marker></defs>` +
    `<line x1="9%" y1="${y1}%" x2="91%" y2="${y2}%" stroke="currentColor" stroke-width="1.35" stroke-linecap="round" marker-end="url(#${id})"/>` +
    `</svg>`
  )
}

function renderTabvar(node, ctx) {
  const rows = node.lines.map((l) => l.trim()).filter(Boolean)
  const parsed = rows.map((r) => {
    const m = r.match(/^(.+?)\s+:\s+(.*)$/) || r.match(/^(.+?)\s*:\s*(.*)$/)
    return m ? { label: stripDollars(m[1]), entries: splitTop(m[2]) } : null
  })
  if (!parsed.length || parsed.some((p) => !p)) {
    return '<div class="otm-error">Tableau de variations mal formé</div>'
  }

  const xs = parsed[0].entries.map(stripDollars)
  const n = xs.length
  const cols = ['auto']
  for (let s = 0; s < 2 * n - 1; s += 1) cols.push(s % 2 === 0 ? 'auto' : 'minmax(var(--otm-tv-gap-min), var(--otm-tv-gap-max))')

  const cells = []
  const cell = (row, col, span, cls, html, extra = '') =>
    cells.push(
      `<div class="otm-tv-cell ${cls}" style="grid-row:${row};grid-column:${col}${span > 1 ? ` / span ${span}` : ''}"${extra}>${html}</div>`
    )
  const math = (tex) => (tex ? escapeHtml(`$${tex}$`) : '')
  // Libellé : formule pure (f'(x)) ou texte avec formules (« Signe de $x+2$ »)
  const label = (txt) => (/\$/.test(txt) || /^[A-Za-zÀ-ÿ]{3,}[\s'’]/.test(txt) || /^[A-Za-zÀ-ÿ]{4,}$/.test(txt) ? `<span class="otm-tv-lab">${renderInline(txt)}</span>` : math(txt))
  // Case de signe : signe, formule ou mot (« convexe »)
  const word = (t) => /^[A-Za-zÀ-ÖØ-öø-ÿ'’\- ]{3,}$/.test(t)
  const token = (t) => (word(t) ? `<span class="otm-tv-txt">${escapeHtml(t)}</span>` : /\$/.test(t) && !/^\$[^$]*\$$/.test(t) ? renderInline(t) : math(stripDollars(t)))
  const lastRow = parsed.length

  // Ligne des x
  cell(1, 1, 1, 'otm-tv-label otm-tv-head', label(parsed[0].label))
  for (let s = 0; s < 2 * n - 1; s += 1) {
    const isVal = s % 2 === 0
    cell(1, 2 + s, 1, `otm-tv-head ${isVal ? 'otm-tv-x' : 'otm-tv-gap'}`, isVal ? math(xs[s / 2]) : '')
  }

  for (let r = 1; r < parsed.length; r += 1) {
    const row = r + 1
    const { label: lab, entries } = parsed[r]
    const last = row === lastRow ? ' otm-tv-last' : ''

    if (entries.length === 2 * n - 1) {
      // Ligne de signes : , +, z, -, d, +,
      cell(row, 1, 1, `otm-tv-label otm-tv-sign-row${last}`, label(lab))
      entries.forEach((tok, s) => {
        const t = tok.trim()
        const isVal = s % 2 === 0
        let cls = 'otm-tv-sign'
        let html = ''
        if (isVal) {
          if (t === 'z') {
            cls += ' otm-tv-z'
            html = `<span class="otm-tv-zero">${math('0')}</span>`
          } else if (t === 'd') {
            cls += ' otm-tv-d'
          } else if (t === 't') {
            cls += ' otm-tv-t'
          } else if (t) {
            html = token(t)
          }
        } else if (t === 'h' || t === '||') {
          cls += ' otm-tv-h'
        } else if (t === '+' || t === '-') {
          html = math(t)
        } else if (t) {
          html = token(t)
        }
        cell(row, 2 + s, 1, `${cls}${last}`, html)
      })
      continue
    }

    if (entries.length === n) {
      // Ligne de variations : -/0, +/\frac12, -D+/a/b, R, +/1
      cell(row, 1, 1, `otm-tv-label otm-tv-var-row${last}`, label(lab))
      const nodes = entries.map(parseVarEntry)
      nodes.forEach((nd, k) => {
        if (nd.skip) return
        let html
        if (nd.bar === 'none') {
          html = `<span class="otm-tv-v otm-tv-v--${nd.left.pos}">${math(nd.left.tex)}</span>`
        } else {
          const side = (v, where) =>
            v
              ? `<span class="otm-tv-side otm-tv-side--${where} otm-tv-v--${v.pos}">${math(v.tex)}</span>`
              : `<span class="otm-tv-side otm-tv-side--${where}"></span>`
          html = `${side(nd.left, 'l')}<span class="otm-tv-bar" aria-hidden="true"></span>${side(nd.right, 'r')}`
        }
        cell(row, 2 + 2 * k, 1, `otm-tv-var otm-tv-varval otm-tv-bar-${nd.bar}${last}`, html)
      })
      // Flèches entre valeurs successives (R : la flèche traverse)
      let k = 0
      while (k < n - 1) {
        if (nodes[k].skip || !nodes[k].right) {
          k += 1
          continue
        }
        let m = k + 1
        while (m < n && nodes[m].skip) m += 1
        if (m >= n) break
        const from = nodes[k].right
        const to = nodes[m].left
        const startCol = 2 + 2 * k + 1
        const span = 2 * (m - k) - 1
        if (from && to) {
          ctx.arrowCount += 1
          const id = `otm-ah-${ctx.uid}-${ctx.arrowCount}`
          cell(row, startCol, span, `otm-tv-var otm-tv-arrowcell${last}`, arrowSvg(id, from.pos, to.pos))
        }
        k = m
      }
      // Cellules d'intervalles restées vides ; entre deux doubles barres
      // (fonction non définie sur l'intervalle) : zone hachurée
      for (let s = 1; s < 2 * n - 1; s += 2) {
        const left = Math.floor(s / 2)
        let a = left
        while (a >= 0 && nodes[a].skip) a -= 1
        let b = left + 1
        while (b < n && nodes[b].skip) b += 1
        const covered = a >= 0 && b < n && nodes[a].right && nodes[b].left
        if (covered) continue
        const interdit = a >= 0 && b < n && !nodes[a].right && !nodes[b].left
        cell(row, 2 + s, 1, `otm-tv-var${interdit ? ' otm-tv-h' : ''}${last}`, '')
      }
      // Colonnes R : rien à dessiner (la flèche les couvre)
      continue
    }

    return `<div class="otm-error">Tableau : la ligne « ${escapeHtml(lab)} » doit avoir ${n} ou ${2 * n - 1} éléments (elle en a ${entries.length})</div>`
  }

  const title = node.title ? `<div class="otm-tv-title">${renderInline(node.title)}</div>` : ''
  return (
    `<figure class="otm-tv-figure">${title}<div class="otm-scroll">` +
    `<div class="otm-tv" role="img" aria-label="Tableau de variations" style="grid-template-columns:${cols.join(' ')}">` +
    `${cells.join('')}</div></div></figure>`
  )
}

/* ------------------------------------------------------------------ */
/*  Rendu des blocs                                                    */
/* ------------------------------------------------------------------ */

function renderPipeTable(node) {
  const al = (k) => (node.align[k] ? ` style="text-align:${node.align[k]}"` : '')
  const head = node.header
    ? `<thead><tr>${node.header.map((c, k) => `<th${al(k)}>${renderInline(c)}</th>`).join('')}</tr></thead>`
    : ''
  const body = `<tbody>${node.body
    .map((row) => `<tr>${row.map((c, k) => `<td${al(k)}>${renderInline(c)}</td>`).join('')}</tr>`)
    .join('')}</tbody>`
  return `<div class="otm-scroll"><table class="otm-table">${head}${body}</table></div>`
}

function renderList(node, ctx) {
  const tag = node.ordered ? 'ol' : 'ul'
  const start = node.ordered && node.start !== 1 ? ` start="${node.start}" style="counter-reset:otm-li ${node.start - 1}"` : ''
  const items = node.items
    .map((it) => {
      const kids = it.children
      const body =
        kids.length === 1 && kids[0].type === 'para'
          ? renderInline(kids[0].text)
          : kids.length && kids[0].type === 'para'
            ? `${renderInline(kids[0].text)}${renderNodes(kids.slice(1), ctx)}`
            : renderNodes(kids, ctx)
      return `<li><div class="otm-li">${body}</div></li>`
    })
    .join('')
  return `<${tag} class="otm-${node.ordered ? 'olist' : 'list'}"${start}>${items}</${tag}>`
}

function renderHeading(node, ctx) {
  const text = node.text
  if (node.level === 2) {
    ctx.stepCounter = 0
    const q = text.match(/^Question\s+([A-Z]?\d+[a-z]?)\s*[:.)-]?\s*(.*)$/i)
    if (q) {
      return (
        `<h2 class="otm-q"><span class="otm-q-num" aria-label="Question ${escapeHtml(q[1])}">${escapeHtml(q[1])}</span>` +
        `<span class="otm-q-text">${renderInline(q[2])}</span></h2>`
      )
    }
    const num = text.match(/^((?:[IVXLC]+|\d+|[A-Z])[.)])\s+(.*)$/)
    if (num) {
      return `<h2 class="otm-h2"><span class="otm-h2-num">${escapeHtml(num[1].replace(/[.)]$/, ''))}</span><span class="otm-h2-text">${renderInline(num[2])}</span></h2>`
    }
    return `<h2 class="otm-h2"><span class="otm-h2-text">${renderInline(text)}</span></h2>`
  }
  return `<h${node.level} class="otm-h${node.level}">${renderInline(text)}</h${node.level}>`
}

function renderBox(node, ctx) {
  const kind = node.kind
  let label = Object.prototype.hasOwnProperty.call(BOXES, kind) ? BOXES[kind] : node.rawKind
  let title = node.title

  if (kind === 'etape') {
    ctx.stepCounter += 1
    label = `Étape ${ctx.stepCounter}`
  } else if (kind === 'point') {
    label = title || 'Point'
    title = ''
  } else if (!Object.prototype.hasOwnProperty.call(BOXES, kind)) {
    label = node.rawKind.charAt(0).toUpperCase() + node.rawKind.slice(1)
  }

  const body = renderNodes(node.children, ctx)
  const qed = kind === 'demonstration' ? '<span class="otm-qed" aria-hidden="true"></span>' : ''
  const head =
    label || title
      ? `<div class="otm-box-head">${label ? `<span class="otm-box-label">${escapeHtml(label)}</span>` : ''}${
          title ? `<span class="otm-box-title">${renderInline(title)}</span>` : ''
        }</div>`
      : ''
  const cls = Object.prototype.hasOwnProperty.call(BOXES, kind) ? kind : 'autre'
  return `<section class="otm-box otm-box--${cls}">${head}<div class="otm-box-body">${body}${qed}</div></section>`
}

function renderNodes(nodes, ctx) {
  return nodes
    .map((node) => {
      switch (node.type) {
        case 'para':
          return `<p>${renderInline(node.text)}</p>`
        case 'math':
          return `<div class="otm-math">${escapeHtml(`$$${node.tex}$$`)}</div>`
        case 'heading':
          return renderHeading(node, ctx)
        case 'image':
          return `<div class="otm-figure">${escapeHtml(node.token)}</div>`
        case 'table':
          return renderPipeTable(node)
        case 'list':
          return renderList(node, ctx)
        case 'box':
          return renderBox(node, ctx)
        case 'tabvar':
          return renderTabvar(node, ctx)
        case 'code':
          return renderCode(node)
        default:
          return ''
      }
    })
    .join('')
}

/**
 * Rend un document OptiTAB en HTML.
 * @param {string} source  texte commençant par le marqueur optitab:1
 * @param {{context?: 'course'|'sheet'|'exercise'|'statement'|'solution'}} options
 */
export function renderOptitabDoc(source, options = {}) {
  const context = options.context || 'course'
  const ctx = { uid: hashString(`${context}|${source}`), stepCounter: 0, arrowCount: 0, context }
  const text = String(source || '')
    .replace(MARKER_RE, '')
    .replace(/\r\n?/g, '\n')
  const nodes = parseBlocks(text.split('\n'))
  return `<div class="otm otm--${context}">${renderNodes(nodes, ctx)}</div>`
}

/** Texte brut (pour les extraits, le référencement et les recherches). */
export function optitabToPlainText(source) {
  return String(source || '')
    .replace(MARKER_RE, '')
    .replace(/^:{3,}.*$/gm, ' ')
    .replace(/^#{2,4}\s+/gm, '')
    .replace(/\[\s*IMAGE\s*_?\s*\d+\s*\]/gi, ' ')
    .replace(/\*\*|\|/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}
