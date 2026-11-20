// Convertisseur d'unités (page methodes/convertisseur-d-unites).
//
// SOURCE UNIQUE des unités : le convertisseur de la page (outils/convertisseur.js
// lit ces données, recopiées en JSON dans la page) et les tableaux du texte
// (contenu/methodes/convertisseur-d-unites/generer.py, qui les lit avec
// « node convertisseur.mjs --json » et compare chaque facteur à scipy.constants).
//
// Chaque unité : [code, nom, symbole, facteur] où facteur = valeur de 1 unité dans
// l'unité de référence de la grandeur (première du tableau « ref »). Températures :
// [code, nom, symbole, a, b] avec T (en K) = a × valeur + b.
const PI = Math.PI

export const GRANDEURS = [
  {
    id: 'longueur', nom: 'Longueur', ref: 'm', de: 'km', vers: 'm', valeur: 1,
    unites: [
      ['km', 'kilomètre', 'km', 1e3], ['hm', 'hectomètre', 'hm', 1e2], ['dam', 'décamètre', 'dam', 10], ['m', 'mètre', 'm', 1],
      ['dm', 'décimètre', 'dm', 0.1], ['cm', 'centimètre', 'cm', 0.01], ['mm', 'millimètre', 'mm', 1e-3],
      ['um', 'micromètre', 'µm', 1e-6], ['nm', 'nanomètre', 'nm', 1e-9], ['A', 'angström', 'Å', 1e-10],
      ['mi', 'mile', 'mi', 1609.344], ['M', 'mille marin', 'M', 1852], ['yd', 'yard', 'yd', 0.9144],
      ['ft', 'pied', 'ft', 0.3048], ['in', 'pouce', 'in', 0.0254],
      ['ua', 'unité astronomique', 'ua', 149597870700], ['al', 'année-lumière', 'al', 9460730472580800]
    ]
  },
  {
    id: 'masse', nom: 'Masse', ref: 'kg', de: 'kg', vers: 'g', valeur: 1,
    unites: [
      ['t', 'tonne', 't', 1e3], ['q', 'quintal', 'q', 100], ['kg', 'kilogramme', 'kg', 1], ['hg', 'hectogramme', 'hg', 0.1],
      ['dag', 'décagramme', 'dag', 0.01], ['g', 'gramme', 'g', 1e-3], ['dg', 'décigramme', 'dg', 1e-4],
      ['cg', 'centigramme', 'cg', 1e-5], ['mg', 'milligramme', 'mg', 1e-6], ['ug', 'microgramme', 'µg', 1e-9],
      ['lb', 'livre', 'lb', 0.45359237], ['oz', 'once', 'oz', 0.028349523125], ['ct', 'carat', 'ct', 2e-4]
    ]
  },
  {
    id: 'aire', nom: 'Aire', ref: 'm2', de: 'ha', vers: 'm2', valeur: 1,
    unites: [
      ['km2', 'kilomètre carré', 'km²', 1e6], ['ha', 'hectare', 'ha', 1e4], ['a', 'are', 'a', 100], ['m2', 'mètre carré', 'm²', 1],
      ['dm2', 'décimètre carré', 'dm²', 1e-2], ['cm2', 'centimètre carré', 'cm²', 1e-4], ['mm2', 'millimètre carré', 'mm²', 1e-6],
      ['acre', 'acre', 'ac', 4046.8564224], ['ft2', 'pied carré', 'ft²', 0.09290304], ['in2', 'pouce carré', 'in²', 6.4516e-4]
    ]
  },
  {
    id: 'volume', nom: 'Volume et contenance', ref: 'm3', de: 'L', vers: 'cm3', valeur: 1,
    unites: [
      ['m3', 'mètre cube', 'm³', 1], ['hL', 'hectolitre', 'hL', 0.1], ['daL', 'décalitre', 'daL', 0.01], ['L', 'litre', 'L', 1e-3],
      ['dL', 'décilitre', 'dL', 1e-4], ['cL', 'centilitre', 'cL', 1e-5], ['mL', 'millilitre', 'mL', 1e-6],
      ['dm3', 'décimètre cube', 'dm³', 1e-3], ['cm3', 'centimètre cube', 'cm³', 1e-6], ['mm3', 'millimètre cube', 'mm³', 1e-9],
      ['galUS', 'gallon américain', 'gal US', 3.785411784e-3], ['galUK', 'gallon impérial', 'gal UK', 4.54609e-3],
      ['bbl', 'baril de pétrole', 'bbl', 0.158987294928]
    ]
  },
  {
    id: 'temps', nom: 'Durée', ref: 's', de: 'h', vers: 's', valeur: 1,
    unites: [
      ['an', 'année de 365 jours', 'an', 31536000], ['sem', 'semaine', 'sem.', 604800], ['j', 'jour', 'j', 86400],
      ['h', 'heure', 'h', 3600], ['min', 'minute', 'min', 60], ['s', 'seconde', 's', 1], ['ms', 'milliseconde', 'ms', 1e-3],
      ['us', 'microseconde', 'µs', 1e-6], ['ns', 'nanoseconde', 'ns', 1e-9]
    ]
  },
  {
    id: 'vitesse', nom: 'Vitesse', ref: 'm/s', de: 'km/h', vers: 'm/s', valeur: 90,
    unites: [
      ['m/s', 'mètre par seconde', 'm/s', 1], ['km/h', 'kilomètre par heure', 'km/h', 1 / 3.6], ['km/s', 'kilomètre par seconde', 'km/s', 1e3],
      ['kn', 'nœud', 'kn', 1852 / 3600], ['mph', 'mile par heure', 'mph', 0.44704], ['ft/s', 'pied par seconde', 'ft/s', 0.3048]
    ]
  },
  {
    id: 'force', nom: 'Force', ref: 'N', de: 'kN', vers: 'N', valeur: 2.5,
    unites: [
      ['N', 'newton', 'N', 1], ['mN', 'millinewton', 'mN', 1e-3], ['daN', 'décanewton', 'daN', 10], ['kN', 'kilonewton', 'kN', 1e3],
      ['MN', 'méganewton', 'MN', 1e6], ['kgf', 'kilogramme-force', 'kgf', 9.80665], ['tf', 'tonne-force', 'tf', 9806.65],
      ['lbf', 'livre-force', 'lbf', 4.4482216152605], ['dyn', 'dyne', 'dyn', 1e-5]
    ]
  },
  {
    id: 'pression', nom: 'Pression', ref: 'Pa', de: 'bar', vers: 'Pa', valeur: 1,
    unites: [
      ['Pa', 'pascal', 'Pa', 1], ['hPa', 'hectopascal', 'hPa', 100], ['kPa', 'kilopascal', 'kPa', 1e3], ['MPa', 'mégapascal', 'MPa', 1e6],
      ['GPa', 'gigapascal', 'GPa', 1e9], ['bar', 'bar', 'bar', 1e5], ['mbar', 'millibar', 'mbar', 100],
      ['atm', 'atmosphère normale', 'atm', 101325], ['mmHg', 'millimètre de mercure', 'mmHg', 133.322387415],
      ['psi', 'livre par pouce carré', 'psi', 4.4482216152605 / 0.0254 ** 2], ['kgf/cm2', 'kilogramme-force par cm²', 'kgf/cm²', 98066.5],
      ['N/mm2', 'newton par mm²', 'N/mm²', 1e6]
    ]
  },
  {
    id: 'energie', nom: 'Énergie', ref: 'J', de: 'kWh', vers: 'J', valeur: 1,
    unites: [
      ['J', 'joule', 'J', 1], ['kJ', 'kilojoule', 'kJ', 1e3], ['MJ', 'mégajoule', 'MJ', 1e6], ['GJ', 'gigajoule', 'GJ', 1e9],
      ['Wh', 'wattheure', 'Wh', 3600], ['kWh', 'kilowattheure', 'kWh', 3.6e6], ['MWh', 'mégawattheure', 'MWh', 3.6e9],
      ['cal', 'calorie', 'cal', 4.184], ['kcal', 'kilocalorie', 'kcal', 4184], ['eV', 'électronvolt', 'eV', 1.602176634e-19],
      ['MeV', 'mégaélectronvolt', 'MeV', 1.602176634e-13], ['BTU', 'British thermal unit', 'BTU', 1055.05585262],
      ['tep', 'tonne équivalent pétrole', 'tep', 41.868e9]
    ]
  },
  {
    id: 'puissance', nom: 'Puissance', ref: 'W', de: 'ch', vers: 'kW', valeur: 100,
    unites: [
      ['W', 'watt', 'W', 1], ['mW', 'milliwatt', 'mW', 1e-3], ['kW', 'kilowatt', 'kW', 1e3], ['MW', 'mégawatt', 'MW', 1e6],
      ['GW', 'gigawatt', 'GW', 1e9], ['ch', 'cheval-vapeur', 'ch', 735.49875], ['hp', 'horsepower', 'hp', 745.69987158227022],
      ['kcal/h', 'kilocalorie par heure', 'kcal/h', 4184 / 3600], ['BTU/h', 'BTU par heure', 'BTU/h', 1055.05585262 / 3600]
    ]
  },
  {
    id: 'temperature', nom: 'Température', ref: 'K', de: 'C', vers: 'F', valeur: 20, affine: true,
    unites: [
      ['C', 'degré Celsius', '°C', 1, 273.15], ['K', 'kelvin', 'K', 1, 0], ['F', 'degré Fahrenheit', '°F', 5 / 9, 273.15 - 32 * 5 / 9]
    ]
  },
  {
    id: 'angle', nom: 'Angle', ref: 'rad', de: 'deg', vers: 'rad', valeur: 180,
    unites: [
      ['deg', 'degré', '°', PI / 180], ['rad', 'radian', 'rad', 1], ['gon', 'grade', 'gon', PI / 200],
      ['arcmin', 'minute d’arc', '′', PI / 10800], ['arcsec', 'seconde d’arc', '″', PI / 648000], ['tour', 'tour', 'tr', 2 * PI]
    ]
  },
  {
    id: 'donnees', nom: 'Données numériques', ref: 'o', de: 'Go', vers: 'Mo', valeur: 1,
    unites: [
      ['bit', 'bit', 'bit', 0.125], ['o', 'octet', 'o', 1], ['ko', 'kilooctet', 'ko', 1e3], ['Mo', 'mégaoctet', 'Mo', 1e6],
      ['Go', 'gigaoctet', 'Go', 1e9], ['To', 'téraoctet', 'To', 1e12], ['Kio', 'kibioctet', 'Kio', 1024],
      ['Mio', 'mébioctet', 'Mio', 1024 ** 2], ['Gio', 'gibioctet', 'Gio', 1024 ** 3], ['Tio', 'tébioctet', 'Tio', 1024 ** 4]
    ]
  },
  {
    id: 'frequence', nom: 'Fréquence', ref: 'Hz', de: 'tr/min', vers: 'Hz', valeur: 3000,
    unites: [
      ['Hz', 'hertz', 'Hz', 1], ['kHz', 'kilohertz', 'kHz', 1e3], ['MHz', 'mégahertz', 'MHz', 1e6], ['GHz', 'gigahertz', 'GHz', 1e9],
      ['tr/min', 'tour par minute', 'tr/min', 1 / 60], ['tr/s', 'tour par seconde', 'tr/s', 1]
    ]
  },
  {
    id: 'masse-volumique', nom: 'Masse volumique', ref: 'kg/m3', de: 'g/cm3', vers: 'kg/m3', valeur: 1,
    unites: [
      ['kg/m3', 'kilogramme par mètre cube', 'kg/m³', 1], ['g/cm3', 'gramme par centimètre cube', 'g/cm³', 1e3],
      ['g/mL', 'gramme par millilitre', 'g/mL', 1e3], ['kg/L', 'kilogramme par litre', 'kg/L', 1e3], ['g/L', 'gramme par litre', 'g/L', 1],
      ['lb/ft3', 'livre par pied cube', 'lb/ft³', 0.45359237 / 0.3048 ** 3]
    ]
  }
]

// ---------------------------------------------------------------- calcul (même code que outils/convertisseur.js)
const versRef = (u, x) => (u.length > 4 ? u[3] * x + u[4] : u[3] * x)
const depuisRef = (u, y) => (u.length > 4 ? (y - u[4]) / u[3] : y / u[3])
export const convertir = (g, de, vers, x) => {
  const U = Object.fromEntries(g.unites.map((u) => [u[0], u]))
  return depuisRef(U[vers], versRef(U[de], x))
}

const NNBSP = String.fromCharCode(0x202f)
const NBSP = String.fromCharCode(160)
const SUP = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' }
// Écriture française : n chiffres significatifs au plus (8 dans le convertisseur, 12 dans les
// tableaux de la page), puissance de 10 au-delà de 10¹² ou sous 10⁻⁶.
export function nombre(x, n = 8) {
  if (x === 0 || !isFinite(x)) return x === 0 ? '0' : '—'
  const a = Math.abs(x)
  if (a >= 1e12 || a < 1e-6) {
    const [m, ex] = x.toExponential(n - 1).split('e')
    const mant = String(Number(m)).replace('.', ',').replace('-', '−')
    return `${mant}${NBSP}×${NBSP}10${String(Number(ex)).split('').map((c) => SUP[c]).join('')}`
  }
  const s = Number(x.toPrecision(n)).toLocaleString('fr-FR', { maximumFractionDigits: 15, useGrouping: true })
  return s.replace(/[\s  ]/g, NNBSP).replace('-', '−')
}
export const exact = (x, n = 8) => {
  const a = Math.abs(x)
  const r = a >= 1e12 || a < 1e-6 ? Number(x.toExponential(n - 1)) : Number(x.toPrecision(n))
  return Math.abs(r - x) <= 1e-14 * Math.max(Math.abs(x), 1e-300)
}

// Nombre et symbole : espace insécable, sauf pour les angles (45°, 30′, 15″).
export const avec = (n, s) => (['°', '′', '″'].includes(s) ? `${n}${s}` : `${n}${NBSP}${s}`)

// Phrase d'explication sous le résultat (même texte que outils/convertisseur.js).
const FORMULES_T = {
  'C>F': '°F = °C × 1,8 + 32', 'F>C': '°C = (°F − 32) ÷ 1,8', 'C>K': 'K = °C + 273,15', 'K>C': '°C = K − 273,15',
  'F>K': 'K = (°F − 32) ÷ 1,8 + 273,15', 'K>F': '°F = (K − 273,15) × 1,8 + 32'
}
export function explication(g, de, vers) {
  const U = Object.fromEntries(g.unites.map((u) => [u[0], u]))
  if (de === vers) return 'Même unité : la valeur ne change pas.'
  if (g.affine) return `Formule : ${FORMULES_T[`${de}>${vers}`]}.`
  const k = convertir(g, de, vers, 1)
  const sd = U[de][2]
  const sv = U[vers][2]
  if (k >= 1) return `${avec(1, sd)} ${exact(k) ? '=' : '≈'} ${avec(nombre(k), sv)} : on multiplie par ${nombre(k)}.`
  const inv = 1 / k
  return `${avec(1, sv)} ${exact(inv) ? '=' : '≈'} ${avec(nombre(inv), sd)} : on divise par ${nombre(inv)}.`
}

const e = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
const options = (g, choisi) => g.unites.map((u) => `<option value="${e(u[0])}"${u[0] === choisi ? ' selected' : ''}>${e(u[1])} (${e(u[2])})</option>`).join('')

// Bloc HTML du convertisseur (avec le résultat de l'exemple, lisible sans JavaScript).
export function convertisseurHtml(id = 'longueur') {
  const g = GRANDEURS.find((x) => x.id === id)
  const U = Object.fromEntries(g.unites.map((u) => [u[0], u]))
  const y = convertir(g, g.de, g.vers, g.valeur)
  const donnees = JSON.stringify(GRANDEURS.map(({ id: i, nom, de, vers, valeur, affine, unites }) => ({ id: i, nom, de, vers, valeur, affine: !!affine, unites })))
  const tout = g.unites.map((u) => `<li><button type="button" data-vers-unite="${e(u[0])}"><strong>${nombre(convertir(g, g.de, u[0], g.valeur))}</strong> <span>${e(u[1])} (${e(u[2])})</span></button></li>`).join('')
  return `<section class="otc cv" data-outil="convertisseur" aria-labelledby="otc-convertisseur-titre">
  <div class="otc__tete">
    <p class="otc__kicker">Outil gratuit</p>
    <p class="otc__titre" id="otc-convertisseur-titre">Convertisseur d’unités</p>
    <p class="otc__intro">Choisissez la grandeur, tapez une valeur (la virgule est acceptée) : la conversion et toutes les équivalences s’affichent à chaque saisie.</p>
  </div>
  <div class="cv__grille">
    <label class="cv__champ cv__champ--grandeur"><span class="cv__lib">Grandeur</span>
      <select class="otc__menu" data-grandeur>${GRANDEURS.map((x) => `<option value="${x.id}"${x.id === id ? ' selected' : ''}>${e(x.nom)}</option>`).join('')}</select></label>
    <label class="cv__champ"><span class="cv__lib">Valeur</span>
      <input class="otc__champ cv__valeur" type="text" inputmode="decimal" autocomplete="off" spellcheck="false" data-valeur value="${e(nombre(g.valeur))}"></label>
    <label class="cv__champ"><span class="cv__lib">De</span>
      <select class="otc__menu" data-de>${options(g, g.de)}</select></label>
    <button type="button" class="cv__inverser" data-inverser aria-label="Inverser les deux unités" title="Inverser les unités">⇄</button>
    <label class="cv__champ"><span class="cv__lib">Vers</span>
      <select class="otc__menu" data-vers>${options(g, g.vers)}</select></label>
  </div>
  <div class="otc__resultat" aria-live="polite">
    <p class="otc__res-lib">Résultat</p>
    <p class="otc__res" data-res>${e(avec(nombre(g.valeur), U[g.de][2]))} ${exact(y) ? '=' : '≈'} ${e(avec(nombre(y), U[g.vers][2]))}</p>
    <p class="otc__calc" data-calc>${e(explication(g, g.de, g.vers))}</p>
  </div>
  <div class="cv__tout">
    <p class="cv__tout-titre" data-tout-titre>${e(avec(nombre(g.valeur), U[g.de][2]))} dans toutes les unités</p>
    <ul class="cv__liste" data-tout>${tout}</ul>
  </div>
  <script type="application/json" data-unites>${donnees.replace(/</g, '\\u003c')}</script>
</section>`
}

// node convertisseur.mjs --json : les données pour generer.py.
if (process.argv[1] && process.argv[1].endsWith('convertisseur.mjs') && process.argv.includes('--json')) {
  process.stdout.write(JSON.stringify(GRANDEURS))
}
