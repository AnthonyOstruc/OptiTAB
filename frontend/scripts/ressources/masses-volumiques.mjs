// Outil de la page « Masse volumique des matériaux » : rechercher un matériau,
// calculer la masse et le poids d'un volume.
//
// Données : contenu/physique-chimie/masse-volumique-des-materiaux/materiaux.json,
// écrit et vérifié par le generer.py de cette page (mêmes valeurs que ses
// tableaux). Elles sont recopiées en JSON dans la page pour outils/masses-volumiques.js.
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const FICHIER = path.join(ICI, '..', '..', 'contenu', 'physique-chimie', 'masse-volumique-des-materiaux', 'materiaux.json')
const NBSP = String.fromCharCode(160)
const NNBSP = String.fromCharCode(0x202f)
const e = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')

// Recherches fréquentes, affichées avant toute saisie.
const POPULAIRES = ['liquides-eau-a-20-c', 'metaux-acier', 'autres-beton-arme', 'metaux-aluminium', 'bois-chene',
  'sols-sable-sec', 'gaz-air', 'liquides-huile-d-olive']

const nombre = (x, n) => Number(x.toPrecision(n)).toLocaleString('fr-FR', { maximumFractionDigits: 6 }).replace(/[\s  ]/g, NNBSP)
const masse = (kg) => (kg >= 1000 ? `${nombre(kg, 4)}${NBSP}kg (${nombre(kg / 1000, 4)}${NBSP}t)` : `${nombre(kg, 4)}${NBSP}kg`)
const plage = (v, f) => (v[0] === v[1] ? f(v[0]) : `${f(v[0])} à ${f(v[1])}`)

export function valeur(m) {
  return m.rho ? `${plage(m.rho, (x) => nombre(x, 4))}${NBSP}kg/m³` : `${plage(m.gamma, (x) => nombre(x, 3))}${NBSP}kN/m³`
}

export function masseVolumiqueHtml() {
  const D = JSON.parse(fs.readFileSync(FICHIER, 'utf8'))
  const parId = Object.fromEntries(D.materiaux.map((m) => [m.id, m]))
  const nomCat = Object.fromEntries(D.categories.map((c) => [c.id, c.nom]))
  for (const id of POPULAIRES) if (!parId[id]) throw new Error(`masses-volumiques : matériau inconnu ${id}`)
  const defaut = parId[D.defaut]
  const groupes = D.categories.map((c) => `<optgroup label="${e(c.nom)}">${D.materiaux.filter((m) => m.cat === c.id)
    .map((m) => `<option value="${e(m.id)}"${m.id === D.defaut ? ' selected' : ''}>${e(m.nom)}</option>`).join('')}</optgroup>`).join('')
  const ligne = (m) => `<li><button type="button" data-choisir="${e(m.id)}"><strong>${e(m.nom)}</strong> <span class="mv__val">${e(valeur(m))}</span> <span class="mv__cat">${e(nomCat[m.cat])}</span></button></li>`
  const kg = defaut.rho[0]
  return `<section class="otc mv" data-outil="masses-volumiques" aria-labelledby="otc-mv-titre">
  <div class="otc__tete">
    <p class="otc__kicker">Outil gratuit</p>
    <p class="otc__titre" id="otc-mv-titre">Trouver une masse volumique, calculer une masse</p>
    <p class="otc__intro">Tapez le nom d’un matériau pour trouver sa masse volumique, puis indiquez un volume : la masse et le poids s’affichent tout de suite.</p>
  </div>
  <div class="mv__recherche">
    <label class="mv__lib" for="mv-q">Rechercher un matériau</label>
    <input class="otc__champ mv__q" id="mv-q" type="search" data-q placeholder="acier, béton, huile, chêne, sable…" autocomplete="off" spellcheck="false">
    <p class="mv__compte" data-compte aria-live="polite">Recherches fréquentes :</p>
    <ul class="mv__resultats" data-resultats>${POPULAIRES.map((id) => ligne(parId[id])).join('')}</ul>
  </div>
  <div class="mv__calcul">
    <label class="mv__champ mv__champ--materiau"><span class="mv__lib">Matériau</span>
      <select class="otc__menu" data-materiau>${groupes}</select></label>
    <label class="mv__champ"><span class="mv__lib">Volume</span>
      <input class="otc__champ" type="text" inputmode="decimal" autocomplete="off" data-volume value="1"></label>
    <label class="mv__champ"><span class="mv__lib">Unité</span>
      <select class="otc__menu" data-unite><option value="1" selected>m³</option><option value="0.001">litres (L, dm³)</option><option value="0.000001">cm³ (mL)</option></select></label>
  </div>
  <div class="otc__resultat" aria-live="polite">
    <p class="otc__res-lib">Pour 1${NBSP}m³ de ${e(defaut.nom)}</p>
    <p class="otc__res" data-res>${masse(kg)}</p>
    <p class="otc__calc" data-calc>Masse volumique : ${e(valeur(defaut))}, densité ${nombre(kg / 1000, 3)}.\nPoids : ${nombre(kg * D.g / 1000, 3)}${NBSP}kN (avec g = 9,81${NBSP}N/kg).</p>
  </div>
  <script type="application/json" data-mv>${JSON.stringify(D).replace(/</g, '\\u003c')}</script>
</section>`
}
