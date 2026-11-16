// Calculateurs intégrés aux pages des ressources gratuites.
//
// Une page déclare « "outil": "<nom>" » dans son bloc d'informations et place
// [OUTIL] dans son texte (sinon le calculateur va en tête). Chaque outil est
// décrit ici (onglets, phrases à trous, exemple affiché sans JavaScript) ; son
// calcul est dans outils/<nom>.js, avec les fonctions communes de
// outils/commun.js, recopiés dans la page (aucun fichier à charger en plus).
//
// Phrase d'un onglet : liste de morceaux, soit du texte, soit un champ
// { k, aria, val, w } (w = largeur en caractères), soit un menu
// { k, aria, options: [[valeur, libellé], …] }.
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ICI = path.dirname(fileURLToPath(import.meta.url))
const e = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
const nb = (s) => String(s).replace(/ ([?!:;%])/g, ' $1')

export const OUTILS = {
  pourcentage: {
    titre: 'Calculateur de pourcentage',
    intro: 'Choisissez le calcul, tapez vos nombres : le résultat et le détail du calcul s’affichent tout de suite.',
    onglets: [
      {
        mode: 'de',
        libelle: 'x % d’un nombre',
        phrase: ['Prendre', { k: 't', aria: 'Pourcentage', val: '15', w: 5 }, '% de', { k: 'n', aria: 'Nombre', val: '80', w: 8 }]
      },
      {
        mode: 'quel',
        libelle: 'Quel pourcentage ?',
        phrase: [{ k: 'p', aria: 'Partie', val: '12', w: 7 }, 'sur un total de', { k: 'n', aria: 'Total', val: '80', w: 8 }, 'représente quel pourcentage ?']
      },
      {
        mode: 'varier',
        libelle: 'Augmenter ou baisser',
        phrase: [{ k: 'n', aria: 'Valeur de départ', val: '80', w: 8 }, { k: 'sens', aria: 'Sens', options: [['hausse', 'augmenté'], ['baisse', 'baissé']] }, 'de', { k: 't', aria: 'Pourcentage', val: '15', w: 5 }, '%']
      },
      {
        mode: 'taux',
        libelle: 'Taux d’évolution',
        phrase: ['Passer de', { k: 'a', aria: 'Valeur de départ', val: '80', w: 8 }, 'à', { k: 'b', aria: 'Valeur d’arrivée', val: '92', w: 8 }]
      }
    ],
    exemple: { res: '12', calc: '15 % de 80 = 80 × 15 ÷ 100 = 12' }
  },
  moyenne: {
    titre: 'Calculateur de moyenne',
    intro: 'Tapez vos notes et leurs coefficients (1 si toutes les notes comptent pareil). La moyenne se calcule à chaque saisie.',
    lignes: [['12', '2'], ['15', '1'], ['9', '3']],
    exemple: { res: '11', calc: '(12 × 2 + 15 + 9 × 3) ÷ (somme des coefficients 6)\n= 66 ÷ 6 = 11' }
  },
  duree: {
    titre: 'Calculateur de durée',
    intro: 'Écrivez les heures comme vous voulez : 8 h 45, 8h45 ou 8:45. Les minutes s’écrivent 45 min.',
    onglets: [
      {
        mode: 'entre',
        libelle: 'Entre deux heures',
        phrase: ['De', { k: 'a', aria: 'Heure de départ', val: '8 h 45', w: 6, texte: true }, 'à', { k: 'b', aria: 'Heure d’arrivée', val: '11 h 20', w: 6, texte: true }]
      },
      {
        mode: 'ajout',
        libelle: 'Heure d’arrivée',
        phrase: ['Partir à', { k: 'a', aria: 'Heure de départ', val: '14 h 50', w: 6, texte: true }, 'pendant', { k: 'd', aria: 'Durée', val: '1 h 25', w: 6, texte: true }]
      },
      {
        mode: 'versHm',
        libelle: 'Heures décimales → h min',
        phrase: [{ k: 'x', aria: 'Heures décimales', val: '2,75', w: 5 }, 'heures en heures et minutes']
      },
      {
        mode: 'versDec',
        libelle: 'h min → heures décimales',
        phrase: [{ k: 'd', aria: 'Durée en heures et minutes', val: '2 h 45', w: 6, texte: true }, 'en heures décimales']
      }
    ],
    exemple: { res: '2 h 35 min', calc: 'De 8 h 45 à 11 h 20 : 2 h 35 min (155 minutes)' }
  },
  fraction: {
    titre: 'Calculateur de fractions',
    intro: 'Tapez des nombres entiers : le résultat est donné en fraction simplifiée, avec chaque étape du calcul.',
    onglets: [
      {
        mode: 'operation',
        libelle: 'Calculer',
        phrase: [{ frac: ['a', 'b'], vals: ['3', '4'] }, { k: 'op', aria: 'Opération', options: [['+', '+'], ['-', '−'], ['*', '×'], ['/', '÷']] }, { frac: ['c', 'd'], vals: ['5', '6'] }]
      },
      {
        mode: 'simplifier',
        libelle: 'Simplifier',
        phrase: ['Simplifier', { frac: ['a', 'b'], vals: ['42', '56'] }]
      }
    ],
    exemple: { res: '19/12', calc: 'Même dénominateur 12 : 3/4 = 9/12 et 5/6 = 10/12\n9/12 + 10/12 = 19/12' }
  },
  arrondi: {
    titre: 'Calculateur d’arrondi',
    intro: 'Tapez un nombre et choisissez la précision : arrondi, troncature et encadrement s’affichent.',
    onglets: [
      {
        mode: 'arrondir',
        libelle: 'Arrondir',
        phrase: ['Arrondir', { k: 'x', aria: 'Nombre', val: '3,14159', w: 9, texte: true }, { k: 'p', aria: 'Précision', options: [['2', 'au centième'], ['1', 'au dixième'], ['3', 'au millième'], ['0', 'à l’unité'], ['-1', 'à la dizaine'], ['-2', 'à la centaine'], ['-3', 'au millier']] }]
      }
    ],
    exemple: { res: '3,14', calc: 'Chiffre suivant : 1 (moins de 5) : on garde le chiffre.\nArrondi au centième : 3,14' }
  },
  diviseurs: {
    titre: 'Diviseurs d’un nombre',
    intro: 'Tapez un nombre entier : critères de divisibilité, liste de ses diviseurs et décomposition en facteurs premiers.',
    onglets: [
      {
        mode: 'nombre',
        libelle: 'Diviseurs',
        phrase: ['Le nombre', { k: 'n', aria: 'Nombre entier', val: '360', w: 9 }]
      }
    ],
    exemple: { res: '360 n’est pas premier', calc: '24 diviseurs : 1 ; 2 ; 3 ; 4 ; 5 ; 6 ; 8 ; 9 ; 10 ; 12 ; 15 ; 18 ; 20 ; 24 ; 30 ; 36 ; 40 ; 45 ; 60 ; 72 ; 90 ; 120 ; 180 ; 360\nDécomposition en facteurs premiers : 360 = 2³ × 3² × 5' }
  }
}

function morceau(m, id) {
  if (typeof m === 'string') return `<span class="otc__mot">${e(nb(m))}</span>`
  if (m.options) {
    return `<select class="otc__menu" data-k="${m.k}" aria-label="${e(m.aria)}">${m.options.map(([v, l]) => `<option value="${e(v)}">${e(l)}</option>`).join('')}</select>`
  }
  if (m.frac) {
    const [kn, kd] = m.frac
    return `<span class="otc__frac">${morceau({ k: kn, aria: 'Numérateur', val: m.vals[0], w: 4 }, id)}<span class="otc__barre" aria-hidden="true"></span>${morceau({ k: kd, aria: 'Dénominateur', val: m.vals[1], w: 4 }, id)}</span>`
  }
  return `<input class="otc__champ" type="text" inputmode="${m.texte ? 'text' : 'decimal'}"${m.texte ? ' data-texte' : ''} autocomplete="off" spellcheck="false" data-k="${m.k}" aria-label="${e(m.aria)}" value="${e(m.val ?? '')}" style="--w:${m.w || 6}" id="${id}-${m.k}">`
}

// Calculateur de moyenne : lignes « note | coefficient » ajoutables.
function corpsMoyenne(o) {
  const ligne = ([n, c], i) => `<div class="otc__ligne">
      <span class="otc__num" data-num>Note ${i + 1}</span>
      <input class="otc__champ" type="text" inputmode="decimal" autocomplete="off" data-note aria-label="Note ${i + 1}" value="${n}" style="--w:5">
      <span class="otc__mot">coef.</span>
      <input class="otc__champ" type="text" inputmode="decimal" autocomplete="off" data-coef aria-label="Coefficient de la note ${i + 1}" value="${c}" style="--w:3">
      <button type="button" class="otc__suppr" data-suppr aria-label="Retirer la note ${i + 1}">×</button>
    </div>`
  return `<div class="otc__lignes" data-lignes>
    ${o.lignes.map(ligne).join('\n    ')}
  </div>
  <button type="button" class="otc__ajout" data-ajout>+ Ajouter une note</button>`
}

// Bloc HTML du calculateur (fonctionne sans JavaScript : l'exemple est affiché).
export function outilHtml(nom) {
  const o = OUTILS[nom]
  if (!o) throw new Error(`outil inconnu : ${nom}`)
  const id = `otc-${nom}`
  const plusieurs = (o.onglets || []).length > 1
  return `<section class="otc" data-outil="${nom}" aria-labelledby="${id}-titre">
  <div class="otc__tete">
    <p class="otc__kicker">Outil gratuit</p>
    <p class="otc__titre" id="${id}-titre">${e(o.titre)}</p>
    <p class="otc__intro">${e(nb(o.intro))}</p>
  </div>
  ${plusieurs ? `<div class="otc__onglets" role="tablist" aria-label="Type de calcul">${o.onglets.map((g, i) => `<button type="button" role="tab" class="otc__onglet" data-mode="${g.mode}" id="${id}-o-${g.mode}" aria-controls="${id}-p-${g.mode}" aria-selected="${i === 0}" tabindex="${i === 0 ? 0 : -1}">${e(nb(g.libelle))}</button>`).join('')}</div>` : ''}
  ${o.lignes ? corpsMoyenne(o) : ''}${(o.onglets || []).map((g, i) => `<div class="otc__panneau" data-panneau="${g.mode}" id="${id}-p-${g.mode}"${plusieurs ? ` role="tabpanel" aria-labelledby="${id}-o-${g.mode}"` : ''}${i ? ' hidden' : ''}>
    <p class="otc__phrase">${g.phrase.map((m) => morceau(m, `${id}-${g.mode}`)).join(' ')}</p>
  </div>`).join('\n  ')}
  <div class="otc__resultat" aria-live="polite">
    <p class="otc__res-lib">Résultat</p>
    <p class="otc__res" data-res>${e(nb(o.exemple.res))}</p>
    <p class="otc__calc" data-calc>${e(nb(o.exemple.calc))}</p>
  </div>
</section>`
}

// Scripts de l'outil, recopiés dans la page.
export function outilScript(nom) {
  const lire = (f) => fs.readFileSync(path.join(ICI, 'outils', f), 'utf8')
  // « ; » entre les fichiers : chacun commence par une parenthèse.
  return `<script>${lire('commun.js')};\n${lire(`${nom}.js`)};</script>`
}
